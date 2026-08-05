#!/bin/bash
# Launch_Cockpit.command — double-click to start the FLEET COCKPIT.
# Delegation v2 (WED-50): one iTerm2 window, Wednesday in the left column
# (this replaces double-clicking Launch_Wednesday.command), agents in rows on
# the right as they're added. Idempotent: if the fleet session already runs,
# it just opens an iTerm2 window attached to it.
#
# PREFLIGHT (Kam, 2026-08-05): check machine deps BEFORE launching the view.
# tmux is hard-required (PORTABILITY 13, brew install offered); iTerm2 is soft
# (PORTABILITY 14, falls back to plain tmux in this window); lost exec bits on
# the cockpit scripts self-heal (PORTABILITY 16). Failures pause so they're
# read, not lost with the window.

set -u
# Double-clicked .command files get a bare PATH — add brew + claude locations.
export PATH="/opt/homebrew/bin:/usr/local/bin:$HOME/.local/bin:$PATH"

SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
PROJECT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
COCKPIT_DIR="$PROJECT_DIR/2_Project_Files/fleet/cockpit"
COCKPIT="$COCKPIT_DIR/cockpit.sh"

pause_exit() { echo; echo "Press any key to close..."; read -n 1 -s; exit "${1:-1}"; }

echo "=== FLEET COCKPIT preflight — $(hostname -s) ==="
echo "    project: $PROJECT_DIR"

# --- Self-heal exec bits (PORTABILITY 16: copies can strip them) ---
for f in "$COCKPIT" "$COCKPIT_DIR/monitor.sh" "$PROJECT_DIR/Launch_Wednesday.command"; do
  if [ -f "$f" ] && [ ! -x "$f" ]; then
    chmod +x "$f" && echo "  ✓ restored exec bit: ${f#"$PROJECT_DIR"/}"
  fi
done

FAIL=0

# --- Cockpit files ---
if [ -x "$COCKPIT" ]; then echo "  ✓ cockpit.sh"
else echo "  ✗ cockpit.sh missing at $COCKPIT"; FAIL=1; fi
if [ -f "$COCKPIT_DIR/cockpit.conf" ]; then echo "  ✓ cockpit.conf"
else echo "  ✗ cockpit.conf missing at $COCKPIT_DIR/cockpit.conf"; FAIL=1; fi

# --- claude CLI (the panes are Claude sessions — nothing works without it) ---
if command -v claude >/dev/null; then echo "  ✓ claude CLI ($(command -v claude))"
else echo "  ✗ claude CLI missing — install Claude Code + log in (PORTABILITY 1)"; FAIL=1; fi

# --- Homebrew (needed only to install the below) ---
if command -v brew >/dev/null; then BREW=1; echo "  ✓ homebrew"
else BREW=0; echo "  ⚠ homebrew missing — can't offer installs (https://brew.sh)"; fi

# --- tmux: the cockpit engine (hard — PORTABILITY 13) ---
if ! command -v tmux >/dev/null; then
  echo "  ✗ tmux missing — the cockpit engine (PORTABILITY 13)"
  if [ "$BREW" = 1 ]; then
    printf "    Install tmux now via Homebrew? [y/N] "
    read -r REPLY
    if [[ "$REPLY" =~ ^[Yy] ]]; then
      brew install tmux || echo "    brew install tmux FAILED (output above)"
    fi
  fi
  command -v tmux >/dev/null || FAIL=1
fi
command -v tmux >/dev/null && echo "  ✓ tmux $(tmux -V | awk '{print $2}')"

# --- iTerm2: the cockpit glass (soft — PORTABILITY 14) ---
ITERM=0
if [ -d /Applications/iTerm.app ]; then
  ITERM=1; echo "  ✓ iTerm2"
else
  echo "  ⚠ iTerm2 missing — cockpit glass (PORTABILITY 14)"
  if [ "$BREW" = 1 ]; then
    printf "    Install iTerm2 now via Homebrew? [y/N] "
    read -r REPLY
    if [[ "$REPLY" =~ ^[Yy] ]]; then
      brew install --cask iterm2 && ITERM=1
    fi
  fi
  [ "$ITERM" = 1 ] || echo "    → will attach plain tmux in this window instead"
fi

if [ "$FAIL" = 1 ]; then
  echo
  echo "PREFLIGHT FAILED — fix the ✗ items above (details in PORTABILITY.md),"
  echo "then double-click this launcher again."
  pause_exit 1
fi
echo "Preflight OK."
echo

# --- Resume vs fresh (Kam, 2026-08-05): quitting iTerm2 only closes the
# glass — the tmux session (and Wednesday's context) keeps running. That is
# the persistence FEATURE (overnight work survives), so re-launching resumes
# by default. This prompt is the explicit door to a FRESH context. ---
TMUX_BIN="$(command -v tmux)"
if "$TMUX_BIN" has-session -t fleet 2>/dev/null; then
  echo "A fleet session is ALREADY RUNNING (Wednesday's context is live in it)."
  PANES=$("$TMUX_BIN" list-panes -t fleet -F '#{@cockpit_name}' 2>/dev/null | grep -v '^$' | paste -sd ', ' -)
  echo "  live panes: ${PANES:-unknown}"
  AGENTS=$("$TMUX_BIN" list-panes -t fleet -F '#{@cockpit_name}' 2>/dev/null | grep -vE '^(wednesday|fleet-monitor)?$' || true)
  echo
  echo "  [R]esume  — reattach to the running session (default; context intact)"
  echo "  [F]resh   — kill it and boot clean (context is LOST unless Wednesday"
  echo "              wrapped first — if unsure, Resume and say 'let's wrap')"
  echo "  [Q]uit    — do nothing"
  printf "Choice [R/f/q] then Enter: "
  # Line read, NOT read -n 1: a single-char read leaves the user's Enter in the
  # buffer, and the YES confirm below then consumes it as an empty answer and
  # silently aborts to Resume (Kam hit exactly this 2026-08-06 — "clicked
  # fresh but it resumed").
  read -r CHOICE
  CHOICE="${CHOICE:0:1}"
  case "$CHOICE" in
    [Ff])
      if [ -n "$AGENTS" ]; then
        echo "  ⚠ AGENT PANES ARE LIVE: $AGENTS"
        printf "  Kill them too? Their unwrapped work is lost. Type YES to proceed: "
        read -r CONFIRM
        [ "$CONFIRM" = "YES" ] || { echo "  Aborted — resuming instead."; CHOICE=R; }
      fi
      if [[ "$CHOICE" =~ ^[Ff]$ ]]; then
        "$TMUX_BIN" kill-session -t fleet
        echo "  fleet session killed — booting fresh."
      fi
      ;;
    [Qq]) exit 0 ;;
    *) : ;;  # resume
  esac
fi

"$COCKPIT" up || { echo "cockpit.sh up failed (output above)"; pause_exit 1; }


if [ "$ITERM" = 1 ]; then
  osascript <<EOS
tell application "iTerm"
  activate
  create window with default profile command "$TMUX_BIN -CC attach -t fleet"
end tell
EOS
else
  exec "$TMUX_BIN" attach -t fleet
fi
