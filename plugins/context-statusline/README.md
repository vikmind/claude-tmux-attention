# context-statusline

Status line that shows the model, the current directory, and how full the
context window is:

```
Opus 5 (1M context) | bulk-action-model | 12% ctx (118k/1000k)
```

The percentage is green below 60, yellow from 60, and red from 85.

The script reads the session JSON on standard input, then derives the context
usage from the last main-chain assistant turn in the transcript. It assumes a
1M window for `[1m]` models and for Fable 5, and 200k for every other model.

## Why this plugin needs a manual step

Claude Code does not accept a status line from a plugin. The manifest has no
`statusLine` key, and a plugin `settings.json` applies only the `agent` and
`subagentStatusLine` keys. So this plugin only delivers the script, and
`~/.claude/settings.json` points at the delivered copy.

## Install

1. Install the plugin:

   ```
   /plugin marketplace add vikmind/claude-setup
   /plugin install context-statusline@claude-setup
   ```

2. Add this block to `~/.claude/settings.json`:

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

3. Check the result:

   ```
   echo '{"model":{"display_name":"Opus 5"},"workspace":{"current_dir":"/tmp"}}' \
     | python3 "$(ls -dt ~/.claude/plugins/cache/claude-setup/context-statusline/*/statusline.py | head -1)"
   ```

   This prints the model and the directory. The context part needs a
   `transcript_path` in the input, so it is absent here. A new session shows the
   complete line.

## Requirements

python3.
