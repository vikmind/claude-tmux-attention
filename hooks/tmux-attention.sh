#!/bin/sh
# Mark this Claude session's tmux window when it needs attention, and clear the
# mark again. The mark is the window option @claude_attention, rendered by
# window-status-format in ~/.tmux.conf.
#
# Usage: tmux-attention.sh set|clear

[ -n "$TMUX" ] && [ -n "$TMUX_PANE" ] || exit 0
command -v tmux >/dev/null 2>&1 || exit 0

win=$(tmux display-message -p -t "$TMUX_PANE" '#{window_id}' 2>/dev/null)
[ -n "$win" ] || exit 0

case "$1" in
  set)
    # Do not mark a window the user is already looking at.
    looking=$(tmux display-message -p -t "$TMUX_PANE" \
      '#{&&:#{window_active},#{session_attached}}' 2>/dev/null)
    [ "$looking" = "1" ] && exit 0
    tmux set-option -w -t "$win" @claude_attention 1
    ;;
  clear)
    tmux set-option -w -t "$win" -u @claude_attention
    ;;
esac
exit 0
