#!/bin/bash
# Launch_Cockpit.command — double-click to start the FLEET COCKPIT.
# Delegation v2 (WED-50): one iTerm2 window, Wednesday in the left column
# (this replaces double-clicking Launch_Wednesday.command), agents in rows on
# the right as they're added. Idempotent: if the fleet session already runs,
# it just opens an iTerm2 window attached to it.

set -u
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ "$SOURCE" != /* ]] && SOURCE="$DIR/$SOURCE"
done
PROJECT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
COCKPIT="$PROJECT_DIR/2_Project_Files/fleet/cockpit/cockpit.sh"

[ -x "$COCKPIT" ] || { echo "cockpit.sh missing/not executable"; read -n 1; exit 1; }

"$COCKPIT" up

if [ -d /Applications/iTerm.app ]; then
  osascript <<'EOS'
tell application "iTerm"
  activate
  create window with default profile command "/opt/homebrew/bin/tmux -CC attach -t fleet"
end tell
EOS
else
  echo "iTerm2 not installed (PORTABILITY 14) — attaching plain tmux here."
  exec tmux attach -t fleet
fi
