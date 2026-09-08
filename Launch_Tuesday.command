#!/bin/bash
# Launch_Tuesday.command — the DATASEC seat (Kam ruled the name 2026-09-08 11:56).
#
# WHY THIS IS TWENTY LINES AND NOT A SECOND COPY OF THE LAUNCHER.
# Launch_Wednesday.command is 450 lines of boot ritual that has already taken four
# seats down once through a single unescaped quote (2026-09-02). Two copies of it
# would drift, and the drift would be invisible until a seat booted wrong. So there
# is ONE launcher, parameterised by WED_AGENT, and this file only sets the identity
# and hands over. Everything Tuesday needs — her ledger, her scope paragraph, her own
# Claude auth namespace, and NOT starting a second dashboard — follows from that one
# variable inside the shared script.
#
# WHAT IS HERS ALONE: _ledger_laptop_datasec.md (historical filename, kept so 86K of
# that seat's corrections and every link to them survive) · her daily notes, pickup and
# claims file · her AgentMail inbox · her Claude account · CLAUDE_CONFIG_DIR under this
# tree's 4_Credentials/ · everything inside !CODING/Datasec/.
# WHAT IS SHARED: this repo, the persona, the voice protocol, people/kam.md, and the
# W and M tier lessons. One Wednesday learned them; Tuesday does not start at zero.
set -u
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
HERE="$(cd -P "$(dirname "$SOURCE")" && pwd)"

SHARED="$HERE/Launch_Wednesday.command"
if [ ! -f "$SHARED" ]; then
  echo "Launch_Tuesday: the shared launcher is missing at $SHARED" >&2
  echo "  This tree is a clone of the Wednesday repo; if that file is gone, the clone" >&2
  echo "  is broken rather than incomplete. Re-clone rather than reconstructing it." >&2
  exit 2
fi

# The launcher FILE is the authority on identity — never the hostname. The headless
# Datasec Mac's hostname is not known yet, and a seat that guesses its own client is
# precisely the failure the two-agent split exists to prevent.
export WED_AGENT="tuesday"

exec bash "$SHARED"
