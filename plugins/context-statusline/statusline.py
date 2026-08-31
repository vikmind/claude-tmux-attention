#!/usr/bin/env python3
"""Claude Code status line: model | cwd | context-window fill %.

Reads the session JSON on stdin, then derives context usage from the
latest main-chain assistant turn in the transcript.
"""
import json
import os
import sys

data = json.load(sys.stdin)

model = data.get("model", {}) or {}
model_id = model.get("id", "") or ""
model_name = model.get("display_name") or model_id or "Claude"

cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd") or os.getcwd()
short_cwd = os.path.basename(cwd.rstrip("/")) or cwd

# Context window: 1M for [1m] models and Fable 5, otherwise the standard 200k.
window = 1_000_000 if ("[1m]" in model_id or "fable" in model_id.lower()) else 200_000

context_tokens = None
path = data.get("transcript_path")
if path and os.path.exists(path):
    try:
        with open(path, "r") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if entry.get("type") != "assistant" or entry.get("isSidechain"):
                    continue
                usage = (entry.get("message") or {}).get("usage")
                if not usage:
                    continue
                context_tokens = (
                    usage.get("input_tokens", 0)
                    + usage.get("cache_creation_input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0)
                )
    except OSError:
        pass

parts = ["\033[36m%s\033[0m" % model_name, "\033[2m%s\033[0m" % short_cwd]

if context_tokens is not None:
    pct = context_tokens / window * 100
    used_k = context_tokens / 1000
    win_k = window // 1000
    if pct >= 85:
        color = "\033[31m"   # red
    elif pct >= 60:
        color = "\033[33m"   # yellow
    else:
        color = "\033[32m"   # green
    parts.append("%s%.0f%% ctx\033[0m \033[2m(%.0fk/%dk)\033[0m" % (color, pct, used_k, win_k))

print(" \033[2m|\033[0m ".join(parts))
