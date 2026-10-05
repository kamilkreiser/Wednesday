#!/bin/bash
# install_night.command — arms the Ornith night job on THIS Mac (Kam, panel 2026-09-14 18:15:36:
# "lets use Ornith at night in the downtime (when no other agents run) … Set this up as a rule").
# Double-click from Finder or run in a terminal. Idempotent: re-running replaces the job.
# Same shape as scheduler/install_scheduler.command (WED-16): the plist is written to
# ~/Library/LaunchAgents (machine-local — PORTABILITY.md item 15), the script it points at
# lives on the drive, and WED_AGENT travels in EnvironmentVariables because launchd hands a
# job a minimal environment (2026-09-09 lesson: the label is not enough).
#
# What it installs:
#   com.<agent>.ornith-night → 23:30 daily → local-model/night/night_run.sh
# The runner's OWN gates decide whether anything runs (23:00–06:00 clock window, fleet pane
# census, no QA gate process, load < 8, Ollama up) — launchd only knocks. A missed fire
# (Mac asleep) is coalesced to the next wake; the clock gate then refuses outside the window.
#
# WEDNESDAY'S SEAT ONLY: the queue is Secuura's backlog and the source checkout is Wednesday's
# drive. Arming this as com.tuesday.ornith-night would have the Datasec coordinator's Mac
# working another client's tickets on a timer — refused here, as the daily sweep is.
#
# `--render-only <path>` writes the substituted plist to <path> and touches launchctl NOT AT ALL
# (how the plist was lint-checked at build time without arming the job).
#
# Requires: the drive-local Ollama serving (tools/ollama/ollama serve with OLLAMA_MODELS at
# local-model/models — see PORTABILITY item 14/15); the runner refuses cleanly (G5) if not.

set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "$AGENTS_DIR" "$SELF_DIR/log"

AGENT="${WED_AGENT:-wednesday}"
case "$AGENT" in
  wednesday) ;;
  tuesday) echo "install_night: REFUSING — the Ornith night job is Wednesday's seat only (it works the Secuura backlog from Wednesday's drive)." >&2; exit 2 ;;
  *) echo "install_night: REFUSING — WED_AGENT='$AGENT' is not a known agent." >&2; exit 2 ;;
esac
if [ ! -f "$SELF_DIR/night_run.sh" ]; then
  echo "install_night: REFUSING — no night_run.sh beside this installer at $SELF_DIR" >&2; exit 3
fi
if [ ! -f "$SELF_DIR/queue.md" ]; then
  echo "install_night: WARNING — no queue.md beside the runner; the job will exit 4 (queue empty) until one exists" >&2
fi

LABEL="com.$AGENT.ornith-night"
PLIST="$AGENTS_DIR/$LABEL.plist"
TEMPLATE="$SELF_DIR/com.wednesday.ornith-night.plist"
if [ "${1:-}" = "--render-only" ]; then
  PLIST="${2:?--render-only needs a path}"
fi
# The tracked template is the shape of record; the installed copy carries THIS machine's paths.
sed -e "s|__NIGHT_RUN__|$SELF_DIR/night_run.sh|g" \
    -e "s|__AGENT__|$AGENT|g" \
    -e "s|__HOME__|$HOME|g" \
    -e "s|__LABEL__|$LABEL|g" \
    "$TEMPLATE" > "$PLIST"
if [ "${1:-}" = "--render-only" ]; then
  echo "rendered (NOT installed) → $PLIST"; plutil -lint "$PLIST"; exit $?
fi
launchctl bootout "gui/$(id -u)/$LABEL" 2>/dev/null || true
launchctl bootstrap "gui/$(id -u)" "$PLIST"
echo "installed $LABEL → 23:30 daily → $SELF_DIR/night_run.sh"

echo ""
echo "── verification ──"
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  echo "OK: $LABEL loaded"
else
  echo "FAILED: $LABEL not loaded"
fi
echo ""
echo "Logs: $SELF_DIR/log/night_<date>.log (decisions) · $HOME/Library/Logs/${AGENT}_ornith-night.{out,err} (launchd stdio)"
echo "Queue: $SELF_DIR/queue.md · results: $SELF_DIR/done.md + local-model/runs/<date>_<ticket>-ornith35b-night/"
echo "Disarm: launchctl bootout gui/$(id -u)/$LABEL"
