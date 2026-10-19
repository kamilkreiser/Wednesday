#!/bin/bash
# brief_seat.sh (TUESDAY's) — run a Claude build seat in a Datasec project folder with a brief FILE as its commission.
# It runs INSIDE a cockpit pane:
#   cockpit.sh add <Datasec/Name> "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '<project dir>' '<absolute brief path>'"
#
# WHY (2026-10-16, Tuesday s108): Friday handed Tuesday HPSM-POC, the MPS Calculator and Security Composer. Their
# own Launch_Claude.command takes "the NEWEST file in 1_Project_Definition/Briefs/" as the commission and names
# Friday as coordinator, and Tuesday may not write into a project's Briefs folder (hard rule 1). Friday launched
# them with 2_Project_Files/friday/brief_seat.sh, which runs the seat under FRIDAY's own Datasec identity
# (friday_as.sh -> FRIDAY/4_Credentials/clients/datasec). Her handover says: use your own identity, never hers.
# So this copy differs from Friday's in exactly three ways:
#   1. identity = the PROJECT's own config dirs (4_Credentials/.azure, .gh-config), exactly as its launcher exports them;
#   2. the brief is an ABSOLUTE path in Tuesday's tree (read-only to the seat; the brief's step 0 copies it in);
#   3. the prompt names Tuesday, and the model is read from models_latest.json (never typed).
set -u
DIR="${1:?project dir}"; BRIEF="${2:?absolute brief path}"
SELF_DIR="$(cd "$(dirname "$0")" && pwd)"; TREE="$(cd "$SELF_DIR/../.." && pwd)"
[ -d "$DIR" ] || { echo "brief_seat: no such project dir: $DIR" >&2; exit 2; }
[ -f "$BRIEF" ] || { echo "brief_seat: no such brief: $BRIEF" >&2; exit 2; }
case "$DIR" in */!CODING/Datasec/*) ;; *) echo "brief_seat: REFUSED — $DIR is not a Datasec project (Tuesday's scope is Datasec only)" >&2; exit 2 ;; esac
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$TREE/0_Brain/dashboard/data/models_latest.json")" \
  || { echo "brief_seat: could not read the opus model id from models_latest.json" >&2; exit 2; }
cd "$DIR" || exit 2
unset GH_TOKEN GITHUB_TOKEN GH_ENTERPRISE_TOKEN AZURE_CLIENT_ID AZURE_CLIENT_SECRET AZURE_TENANT_ID
export AZURE_CONFIG_DIR="$DIR/4_Credentials/.azure"
export GH_CONFIG_DIR="$DIR/4_Credentials/.gh-config"
if [ -x "$DIR/.tools/dotnet/dotnet" ]; then
  export DOTNET_ROOT="$DIR/.tools/dotnet"; export PATH="$DOTNET_ROOT:$PATH"; export DOTNET_CLI_TELEMETRY_OPTOUT=1
fi
echo "brief_seat: dir=$DIR"; echo "brief_seat: brief=$BRIEF"; echo "brief_seat: model=$MODEL"
echo "brief_seat: gh=$(gh api user -q .login 2>&1 | head -1)"
PROMPT="ultrathink

You are a build seat launched by Tuesday (Kam's Datasec coordinator seat) in the project folder $(basename "$DIR"). Friday handed this project to Tuesday on 2026-10-15; Tuesday is your coordinator now. Read ./CLAUDE.md and 1_Project_Definition/CLARIFICATIONS.md first, then execute the brief ${BRIEF} exactly (it lives in Tuesday's tree, read-only to you). Your wrap is the STATUS file the brief names; questions go to tuesday-agent@agentmail.to. Never delete (quarantine). Secrets stay in 4_Credentials/ and 3_Access_Keys/."
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
