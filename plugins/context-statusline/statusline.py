#!/usr/bin/env python3
"""Claude Code status line: model | effort | context-window fill % | cache.

Reads the session JSON on stdin. Claude Code reports the context window
there, so the percentage agrees with what /context shows.
"""
import json
import sys
import time

data = json.load(sys.stdin)

model = data.get("model") or {}
model_name = model.get("display_name") or model.get("id") or "Claude"

parts = ["\033[36m%s\033[0m" % model_name]

# Claude Code sends `effort` only for models that have a reasoning effort.
level = (data.get("effort") or {}).get("level")
if level:
    # xhigh and max cost noticeably more, so they get a colour of their own.
    color = "\033[35m" if level in ("xhigh", "max") else "\033[2m"
    parts.append("%s%s effort\033[0m" % (color, level))

context_window = data.get("context_window") or {}
used = context_window.get("total_input_tokens")
window = context_window.get("context_window_size")

# Claude Code reports the tokens of the last completed request, so this is 0
# until the first request lands. Show nothing rather than a false 0%.
if isinstance(used, int) and used > 0 and isinstance(window, int) and window > 0:
    pct = min(100, used / window * 100)
    if pct >= 85:
        color = "\033[31m"   # red
    elif pct >= 60:
        color = "\033[33m"   # yellow
    else:
        color = "\033[32m"   # green
    parts.append("%s%.0f%% ctx\033[0m \033[2m(%.0fk/%.0fk)\033[0m"
                 % (color, pct, used / 1000, window / 1000))

# Claude Code sends `prompt_cache` once the session has made a request, and
# `caching_observed` says whether the API reported any caching at all.
cache = data.get("prompt_cache") or {}
if cache.get("caching_observed"):
    if not cache.get("warm"):
        parts.append("\033[33mcache cold\033[0m")
    else:
        expires_at = cache.get("expires_at")
        left = expires_at - time.time() if isinstance(expires_at, (int, float)) else None
        if left is None:
            parts.append("\033[32mcache warm\033[0m")
        else:
            parts.append("\033[32mcache %s\033[0m"
                         % ("<1m" if left < 60 else "%.0fm" % (left / 60)))

print(" \033[2m|\033[0m ".join(parts))
