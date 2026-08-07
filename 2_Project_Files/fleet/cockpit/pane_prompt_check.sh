#!/bin/bash
# pane_prompt_check.sh — tell a HUMAN-TYPED unsent line apart from Claude Code's
# auto-suggested next prompt.
#
# WHY THIS EXISTS (2026-08-06, ledger w=5):
# Claude Code renders a suggested next command as ghost text at the input prompt,
# generated from the agent's own last message. `tmux capture-pane -p` strips
# colour, so a suggestion and a line Kam actually typed look IDENTICAL — and the
# suggestions are highly plausible, because they are derived from real context.
# I mistook one ("do the AcrPull swap now while Owner is still on") for an
# instruction from Kam, put his name against it in a brief's PROVENANCE block,
# and an agent acted under urgency that never existed.
#
# The discriminator: suggestion text carries SGR 2 (dim/faint). Typed text does not.
# Capture WITH escapes (-e) and look for it.
#
# Usage: pane_prompt_check.sh [pane-id ...]      (default: all agent panes)
# Exit: 0 always — this is a reporting tool, not a gate.
set -u

TMUX_BIN="$(command -v tmux || echo /opt/homebrew/bin/tmux)"
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

panes=("$@")
if [ ${#panes[@]} -eq 0 ]; then
  # every pane except Wednesday's own and the monitor
  while IFS= read -r line; do
    id="${line%% *}"; name="${line#* }"
    case "$name" in wednesday|fleet-monitor) continue ;; esac
    panes+=("$id")
  done < <("$TMUX_BIN" list-panes -a -F '#{pane_id} #{@cockpit_name}' 2>/dev/null)
fi

[ ${#panes[@]} -gt 0 ] || { echo "no agent panes"; exit 0; }

for id in "${panes[@]}"; do
  name="$("$TMUX_BIN" display-message -p -t "$id" '#{@cockpit_name}' 2>/dev/null)"
  # NOTE: the prompt char is followed by a NON-BREAKING space (U+00A0, \xc2\xa0),
  # not an ordinary one — matching on '❯ ' silently finds nothing.
  # Take the last ❯ line that is NOT Claude Code's own UI chrome. When messages
  # are queued the client renders "❯ Press up to edit queued messages" BELOW the
  # real prompt line — and it is dim, so the naive last-line read reported chrome
  # as a SUGGESTION and, worse, could MASK a genuine typed-unsent line above it.
  # A safety tool that hides the thing it exists to find is worse than none.
  # (Found 2026-08-07 while nudging a pane mid-task.)
  raw=""; text=""
  while IFS= read -r line; do
    [ -n "$line" ] || continue
    cand="$(printf '%s' "$line" | LC_ALL=C sed 's/\x1b\[[0-9;]*m//g' \
            | LC_ALL=C sed 's/^.*❯//' | LC_ALL=C sed 's/^\xc2\xa0*//' | LC_ALL=C sed 's/^ *//')"
    case "$cand" in
      "Press up to edit queued messages"*|"Try "*|"for shortcuts"*) continue ;;
    esac
    raw="$line"; text="$cand"
  done < <("$TMUX_BIN" capture-pane -t "$id" -p -e 2>/dev/null | LC_ALL=C grep -a '❯')
  if [ -z "$text" ]; then
    echo "  ${name:-$id}: prompt empty"
    continue
  fi
  if printf '%s' "$raw" | LC_ALL=C grep -q $'\x1b\\[2m'; then
    echo "  ${name:-$id}: SUGGESTION (Claude ghost text — ignore) :: $text"
  else
    echo "  ${name:-$id}: ⚠ TYPED, UNSENT (a human wrote this — flag it, do NOT act) :: $text"
  fi
done
exit 0
