# context-statusline

Status line that shows the model, the reasoning effort, how full the context
window is, and the state of the prompt cache:

```
Opus 5 (1M context) | high effort | 12% ctx (118k/1000k) | cache 42m
```

The percentage is green below 60, yellow from 60, and red from 85.

The effort part comes from the `effort` field and is absent for a model that
has no reasoning effort. It is dim for `low`, `medium`, and `high`, and magenta
for `xhigh` and `max`, because those two cost noticeably more.

The cache part comes from the `prompt_cache` field. A warm cache is green and
names the time left before it expires. A cold cache is yellow and says `cache
cold`, which means the next turn pays to write the prompt again. The part is
absent before the first request of a session, and also when the API reports no
caching at all.

The script reads the session JSON on standard input and takes both numbers
from the `context_window` field, so the percentage matches what `/context`
shows. Claude Code sizes the window there, which is the only reliable way to
get it: a 1M window can come from an entitlement rather than from the `[1m]`
model id, `CLAUDE_CODE_MAX_CONTEXT_TOKENS` overrides it, and auto-compact
imposes a 200k window on a 1M model.

The context part is absent when Claude Code sends no `context_window`, and also
at the start of a session, because the number counts the tokens of the last
completed request and is therefore 0 until the first request lands. Every part
except the model is optional, so a fresh session shows the model alone.

## Why this plugin needs a manual step

Claude Code does not accept a status line from a plugin. The manifest has no
`statusLine` key, and a plugin `settings.json` applies only the `agent` and
`subagentStatusLine` keys. So this plugin only delivers the script, and
`~/.claude/settings.json` points at the delivered copy.

## Install

1. Add this repo as marketplace:

   ```
   /plugin marketplace add vikmind/claude-setup
   ```

2. Install `context-statusline`:

   ```
   /plugin install context-statusline@claude-setup
   ```

3. Add this block to `~/.claude/settings.json`:

   ```json
   "statusLine": {
     "type": "command",
     "command": "python3 \"$(ls -dt ~/.claude/plugins/cache/claude-setup/context-statusline/*/statusline.py | head -1)\""
   }
   ```

   Claude Code runs the command through a shell, so the shell expands `~`, the
   pattern, and the command substitution.

   The path holds the plugin version, and the cache keeps more than one version
   after an upgrade. A bare pattern would therefore expand to several paths, and
   `python3` would run the first one and read the rest as arguments. `ls -dt`
   sorts by install time, so `head -1` always names the newest install.

4. Check the result:

   ```
   echo '{"model":{"display_name":"Opus 5"}}' \
     | python3 "$(ls -dt ~/.claude/plugins/cache/claude-setup/context-statusline/*/statusline.py | head -1)"
   ```

   This prints the model alone. The other parts need `effort`,
   `context_window`, and `prompt_cache` in the input, so they are absent here. A
   live session shows the complete line.

## Requirements

python3, and a Claude Code version that sends `context_window`, `effort`, and
`prompt_cache` in the status line input.
