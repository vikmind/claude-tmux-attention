#!/usr/bin/env python3
"""Claude Code status line: model | cwd | context-window fill %.

Reads the session JSON on stdin. Claude Code reports the context window
there, so the percentage agrees with what /context shows.
"""
import json
import os
import sys

data = json.load(sys.stdin)

model = data.get("model") or {}
model_name = model.get("display_name") or model.get("id") or "Claude"

cwd = (data.get("workspace") or {}).get("current_dir") or data.get("cwd") or os.getcwd()
short_cwd = os.path.basename(cwd.rstrip("/")) or cwd

parts = ["\033[36m%s\033[0m" % model_name, "\033[2m%s\033[0m" % short_cwd]

context_window = data.get("context_window") or {}
used = context_window.get("total_input_tokens")
window = context_window.get("context_window_size")

if isinstance(used, int) and isinstance(window, int) and window > 0:
    pct = min(100, used / window * 100)
    if pct >= 85:
        color = "\033[31m"   # red
    elif pct >= 60:
        color = "\033[33m"   # yellow
    else:
        color = "\033[32m"   # green
    parts.append("%s%.0f%% ctx\033[0m \033[2m(%.0fk/%.0fk)\033[0m"
                 % (color, pct, used / 1000, window / 1000))

print(" \033[2m|\033[0m ".join(parts))
