#!/bin/bash
# resume_seat.sh (TUESDAY's) — reopen a DEAD build seat's own Claude session, with its full context, in a cockpit pane:
#   cockpit.sh add <Datasec/Name> "BRIEF_SEAT_LEVEL=<opus|sonnet> bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/resume_seat.sh' '<project dir>' '<session id>' '<absolute brief path>'"
#
# WHY (2026-10-26 s185): at 21:03 a browser sign-in on this machine killed the tmux session, and with it five live
# seats mid-step (B752 B754 B755 B756 B757). A fresh brief_seat launch would refuse at its own REFUSE checks (its
# .tools/bNNN dirs and worktrees exist) and would lose every step's context. Claude Code keeps each session's
# transcript, so `claude --resume <id>` brings the seat back as itself. The identity is set EXACTLY as brief_seat.sh
# sets it (the project's own config dirs, tokens unset); the model is read from models_latest.json, never typed.
set -u
DIR="${1:?project dir}"; SID="${2:?session id}"; BRIEF="${3:?absolute brief path}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"; TREE="$(cd "$SELF_DIR/../.." && pwd)"
[ -d "$DIR" ] || { echo "resume_seat: no such project dir: $DIR" >&2; exit 2; }
[ -f "$BRIEF" ] || { echo "resume_seat: no such brief: $BRIEF" >&2; exit 2; }
case "$DIR" in */!CODING/Datasec/*) ;; *) echo "resume_seat: REFUSED — $DIR is not a Datasec project (Tuesday's scope is Datasec only)" >&2; exit 2 ;; esac
case "$SID" in *[!0-9a-f-]*|"") echo "resume_seat: REFUSED — '$SID' is not a session id" >&2; exit 2 ;; esac
SLUG="$(printf '%s' "$DIR" | sed 's/[^A-Za-z0-9]/-/g')"
[ -f "$HOME/.claude/projects/$SLUG/$SID.jsonl" ] || { echo "resume_seat: REFUSED — no transcript $SID under $SLUG" >&2; exit 2; }
LEVEL="${BRIEF_SEAT_LEVEL:-opus}"
case "$LEVEL" in opus|sonnet) ;; *) echo "resume_seat: REFUSED — BRIEF_SEAT_LEVEL '$LEVEL' is not opus or sonnet" >&2; exit 2 ;; esac
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"][sys.argv[2]]["model_id"])' "$TREE/0_Brain/dashboard/data/models_latest.json" "$LEVEL")" \
  || { echo "resume_seat: could not read the $LEVEL model id from models_latest.json" >&2; exit 2; }
cd "$DIR" || exit 2
unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN AZURE_CLIENT_ID AZURE_CLIENT_SECRET AZURE_TENANT_ID
export AZURE_CONFIG_DIR="$DIR/4_Credentials/.azure"
export GH_CONFIG_DIR="$DIR/4_Credentials/.gh-config"
if [ -x "$DIR/.tools/dotnet/dotnet" ]; then
  export DOTNET_ROOT="$DIR/.tools/dotnet"; export PATH="$DOTNET_ROOT:$PATH"; export DOTNET_CLI_TELEMETRY_OPTOUT=1
fi
echo "resume_seat: dir=$DIR"; echo "resume_seat: session=$SID"; echo "resume_seat: brief=$BRIEF"; echo "resume_seat: model=$MODEL"
PROMPT="Tuesday here (your coordinator). Your pane and EVERY process you had started died at about 21:03 AEDT: a browser sign-in on this machine killed the whole terminal session. Nothing was deleted. This is the same session reopened, with your context. Before any further step: (1) assume every background shell, server, browser and battery you started is GONE; check with ps by your recorded pids and lsof on your own ports, and re-run whatever was mid-flight; (2) any lock or heavy-slot holder file of yours dated before 21:04 is stale: move it into your quarantine (never delete) and say so in STATUS; (3) re-read the last lines of your STATUS file and your brief's ${BRIEF} hard stop; (4) write a STATUS line naming this interruption, then keep working your brief to its last line exactly as before. Same rules, same fences."
exec claude --dangerously-skip-permissions --model "$MODEL" --resume "$SID" "$PROMPT"
