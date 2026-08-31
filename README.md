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

## Let Claude Code do the manual steps

After the two `/plugin install` commands, paste this prompt into a Claude Code
session and it does both manual steps for you:

```
Finish the setup of my claude-setup plugins.

1. Read ~/.claude/plugins/cache/claude-setup/tmux-attention/*/README.md and
   ~/.claude/plugins/cache/claude-setup/context-statusline/*/README.md, and
   follow the install section of each, starting at the manual step. The
   /plugin install part is already done.
2. Copy the `source-file` line and the `statusLine` block from those READMEs
   exactly as written. The wildcards and the command substitution are
   deliberate, so keep them.
3. Do not edit ~/.tmux.conf or ~/.claude/settings.json if the line or the block
   is already there.
4. Run the check that each README gives, and report the output.

Then tell me to restart my Claude Code sessions, because Claude Code reads the
hooks and the status line at startup.
```

The prompt reads the installed copies under
`~/.claude/plugins/cache/claude-setup/`, so it needs no clone of this
repository. Claude Code asks before it writes to either file.

## License

MIT. See `LICENSE`.
