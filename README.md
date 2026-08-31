# claude-tmux-attention

Adds `❗` to the tmux window of a Claude Code session that waits for your input.
The mark disappears when you look at that window, or when you send the next
prompt.

Useful when you run several Claude Code sessions in tmux windows and you want to
see which one needs you.

## How it works

Three parts:

1. `hooks/tmux-attention.sh` sets the tmux window option `@claude_attention` on
   the window that holds the session. The Claude Code `Notification` hook calls
   it with `set`. The `UserPromptSubmit` hook calls it with `clear`.
2. `tmux/claude-attention.conf` renders the option in the window status, and
   removes the option again on `session-window-changed` and
   `client-session-changed`.
3. `hooks/hooks.json` registers both hooks, so `~/.claude/settings.json` needs no
   edit.

The script marks nothing when the window is already the active window of an
attached session, because you are looking at it.

The script uses a window option and not `rename-window`, because
`rename-window` permanently disables `automatic-rename` for that window.

## Install

1. Add this repository as a plugin marketplace, then enable the plugin:

   ```
   /plugin marketplace add vikmind/claude-tmux-attention
   /plugin install tmux-attention@claude-tmux-attention
   ```

2. Add one line to `~/.tmux.conf`. The install puts the whole plugin, the tmux
   configuration included, under `~/.claude/plugins/cache/`, so no clone is
   necessary:

   ```
   source-file -q ~/.claude/plugins/cache/claude-tmux-attention/tmux-attention/*/tmux/claude-attention.conf
   ```

   The path holds the plugin version. The `*` keeps the line correct after an
   upgrade. tmux expands the pattern itself, and the file sets every option with
   `set -g`, so sourcing more than one cached version does no harm.

   Then run `tmux source-file ~/.tmux.conf`. Because `-q` hides a wrong path,
   check the result:

   ```
   tmux show -g window-status-format
   ```

   The value has to start with `#{?@claude_attention,`.

3. Restart the Claude Code sessions. Claude Code reads hooks at startup.

To work from a clone instead, source `tmux/claude-attention.conf` from the clone
and give Claude Code the clone as a local marketplace.

## Requirements

tmux 3.3 or later, for user options in formats.

## Options

The `Notification` hook fires when Claude Code asks for a permission and when a
session waits for input for about 60 seconds. To also mark the window at the end
of every turn, add a `Stop` entry to `hooks/hooks.json` that runs the script with
`set`. This marks the window much more often.

## License

MIT. See `LICENSE`.
