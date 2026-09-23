#!/bin/bash
# Launch_Friday.command — Kam's LAPTOP seat. Named Friday by Kam, live board 2026-09-23 10:49:26:
#   "to avoid confusion, I'm thinking of changing the name of my laptop agent to Friday and creating a
#    new folder. That way the agents won't get confused… Friday will work on both Secura and Dataset
#    projects from this laptop."
#
# SAME SHAPE AS Launch_Tuesday.command, for the same reason: ONE shared launcher, parameterised by
# WED_AGENT, so three seats can never drift into three copies of the boot ritual. This file only
#   (1) refuses to run anywhere but a tree named FRIDAY — double-clicked inside WEDNESDAY or TUESDAY it
#       would otherwise boot a Friday identity on another seat's brain and handover;
#   (2) on the FIRST launch runs 2_Project_Files/friday/first_run.sh (the logins); and
#   (3) loads the laptop's workspace path, then hands over to the shared launcher.
#
# WHAT IS FRIDAY'S ALONE: _ledger_friday.md · 0_Brain/daily_friday/ · NEXT-PICKUP-FRIDAY.md · the
# friday-laptop-agent@agentmail.to inbox · the FRIDAY tab of the live board (partition "Friday") · her own
# Claude login (4_Credentials/.claude) · and one identity folder PER CLIENT (4_Credentials/clients/).
# WHAT IS SHARED: this repo, the persona, the voice protocol, people/kam.md, the W and M lessons.
set -u
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
HERE="$(cd -P "$(dirname "$SOURCE")" && pwd)"

case "$(basename "$HERE")" in
  FRIDAY|Friday|friday) ;;
  *)
    echo "Launch_Friday: REFUSING — this copy lives in '$HERE', which is not a FRIDAY tree." >&2
    echo "  Friday runs from her own folder (made by Install_Friday.command). Launching her from another" >&2
    echo "  seat's tree would boot Friday on that seat's brain and handover." >&2
    printf 'Press Enter to close… '; read -r _; exit 2 ;;
esac

SHARED="$HERE/Launch_Wednesday.command"
if [ ! -f "$SHARED" ]; then
  echo "Launch_Friday: the shared launcher is missing at $SHARED — the clone is broken; re-run Install_Friday.command." >&2
  exit 2
fi

export WED_AGENT="friday"

# ── FIRST RUN: the configuration Kam asked for ("asks me for the relevant logins") ──
if [ ! -f "$HERE/4_Credentials/.friday_configured" ]; then
  bash "$HERE/2_Project_Files/friday/first_run.sh"; FR_RC=$?
  if [ "$FR_RC" -ne 0 ]; then
    echo ""
    echo "Setup stopped before the end (rc=$FR_RC). Nothing is lost — double-click Launch_Friday.command to resume."
    printf 'Press Enter to close… '; read -r _; exit 1
  fi
fi

# ── The laptop's workspace (!CODING + Notes (MASTER)), chosen at setup ──
if [ -f "$HERE/4_Credentials/friday.conf" ]; then
  # shellcheck disable=SC1091
  . "$HERE/4_Credentials/friday.conf"
  export WED_WORKSPACE
fi

exec bash "$SHARED"
