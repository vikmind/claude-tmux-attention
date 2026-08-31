# claude-setup

My Claude Code setup, as a plugin marketplace with two plugins.

| Plugin | What it does | Manual step |
|---|---|---|
| [`tmux-attention`](plugins/tmux-attention) | Marks the tmux window of a session that waits for your input | one `source-file` line in `~/.tmux.conf` |
| [`context-statusline`](plugins/context-statusline) | Status line with model, directory, and context-window fill | one `statusLine` block in `~/.claude/settings.json` |

## Install

```
/plugin marketplace add vikmind/claude-setup
/plugin install tmux-attention@claude-setup
/plugin install context-statusline@claude-setup
```

Then do the manual step for each plugin. Both READMEs give the exact line, and
both lines point into `~/.claude/plugins/cache/claude-setup/`, so neither needs a
clone of this repository.

A plugin can register hooks by itself, which is why `tmux-attention` needs no
`settings.json` edit. A plugin cannot register a status line or tmux
configuration, so those two parts stay manual.

## License

MIT. See `LICENSE`.
