#!/bin/bash
# Install EVERY scheduled job this seat needs, for whichever seat is running.
#
# WHY (2026-09-16): nine launchd jobs keep a coordinator alive on this Mac, and
# install_scheduler.command armed THREE of them. The other six — chatsync, dailysweep,
# nassync, ornith-loop, ornith-night, ornith-receipt — existed only as loaded jobs on
# Wednesday's Mac, with no plist on the drive and no installer entry, so a new machine got
# three of nine and Tuesday's machine got none. The job that puts her replies on Kam's one
# page had never run on her machine, not once, and nothing anywhere said so.
#
# The plists are now TRACKED templates in scheduler/jobs/*.plist.template with two
# placeholders — @PROJECT_DIR@ and @SEAT@ — because the live ones hardcoded
# /Volumes/DevMASTER/WEDNESDAY, which is the travel-pointer defect (2026-08-25) pointed at
# launchd: on another machine those jobs load and fail with EX_CONFIG forever, silently.
#
# Usage:
#   install_all_jobs.sh            install/refresh every job for this seat
#   install_all_jobs.sh --check    report only; exit 1 if any job is missing or unloaded
#   WED_AGENT=tuesday install_all_jobs.sh    (on Tuesday's machine, from HER tree)
#
# Idempotent: unload-then-load each time, so a re-run repairs a drifted job rather than
# duplicating it. Never deletes a plist it did not write.
set -u
SELF="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF/../.." && pwd)"
JOBS="$SELF/jobs"
AGENTS="$HOME/Library/LaunchAgents"
# SEAT RESOLUTION — the TREE decides, and a disagreement REFUSES.
#
# Written this way because the first arm of this script proved why: WED_AGENT is exported by
# the launcher into every shell, so `SEAT="${WED_AGENT:-}"` let an INHERITED value decide the
# seat for a tree it had nothing to do with — the script cheerfully installed com.wednesday.*
# jobs pointing at a scratch directory, overwriting the real ones. Recoverable only because it
# backs up before overwriting and the templates are tracked.
#
# So: the folder name is the discriminator, because it is LOCAL to the thing being identified
# and an environment variable is not (2026-09-09_the-seat-resolver..., 2026-08-05 identities
# float by design). Two independent sources are cross-checked and disagreement refuses rather
# than picking one (2026-09-09_a-guard-refuses-malformed-input... rule 2: refuse on a
# DISAGREEMENT, not just on a bad value). A stale-but-valid WED_AGENT is exactly the shape
# that guard exists for.
TREE_SEAT="$(basename "$PROJECT_DIR" | tr '[:upper:]' '[:lower:]')"
case "$TREE_SEAT" in tuesday|wednesday|friday) ;; *) TREE_SEAT="" ;; esac
ENV_SEAT="${WED_AGENT:-}"
if [ -n "$TREE_SEAT" ] && [ -n "$ENV_SEAT" ] && [ "$TREE_SEAT" != "$ENV_SEAT" ]; then
  echo "REFUSED — the tree says '$TREE_SEAT' and WED_AGENT says '$ENV_SEAT'." >&2
  echo "  These are two independent sources and they disagree, so this script will not pick one." >&2
  echo "  Tree: $PROJECT_DIR" >&2
  echo "  Run it from the seat's own tree with WED_AGENT unset, or fix the variable." >&2
  exit 2
fi
SEAT="${TREE_SEAT:-}"
if [ -z "$SEAT" ]; then
  echo "REFUSED — cannot tell which seat this tree is: $PROJECT_DIR" >&2
  echo "  The folder name is the discriminator and it is not WEDNESDAY, TUESDAY or FRIDAY." >&2
  echo "  WED_AGENT alone is NOT accepted here: it is inherited from whatever shell you are in," >&2
  echo "  and a seat that guesses its own identity is the failure the two-agent split prevents." >&2
  echo "  Run this from the seat's own tree." >&2
  exit 2
fi
check="${1:-}"
# FRIDAY (2026-09-23, Kam 10:49): the laptop seat sleeps and travels and runs NO Studio services, so it gets NO
# scheduled jobs by default. A clear NO-OP, not a refusal: exit 0 for install and --check alike, so doctor and
# the launcher read "nothing to do" rather than "jobs missing". Nothing is written, loaded or unloaded.
if [ "$SEAT" = "friday" ]; then
  echo "friday seat: no scheduled jobs are installed on the laptop"
  exit 0
fi
[ -d "$JOBS" ] || { echo "REFUSED — no templates at $JOBS" >&2; exit 2; }

mkdir -p "$AGENTS"
missing=0; installed=0; current=0
for t in "$JOBS"/*.plist.template; do
  [ -f "$t" ] || continue
  job="$(basename "$t" .plist.template)"
  # Ornith is the STUDIO's (Kam 2026-09-22: "Ornith is a studio agent. not a Datasec workflow") — the three
  # ornith-* jobs are Wednesday's only. On any other seat they refused every cycle (G5: no ollama) and posted
  # duplicate receipts to the panel (Tuesday's 2026-09-22 04:26Z coordination; she booted them out by hand).
  case "$job" in ornith-*) if [ "$SEAT" != "wednesday" ]; then echo "skip $job — Ornith is Wednesday's; seat is $SEAT"; continue; fi ;; esac
  label="com.$SEAT.$job"
  target="$AGENTS/$label.plist"
  # @HOME@ is a placeholder for the SAME reason as @PROJECT_DIR@ (2026-09-16, Tuesday's first run):
  # the templates hardcoded /Users/kam_code/Library/Logs/wednesday_*, which is the Studio's home and
  # does not exist on the mini. All nine jobs loaded and died with EX_CONFIG(78) before running a line,
  # writing no log — so the FDA failure underneath them was invisible. A log path is a travel pointer too.
  # @NASHOUR@/@NASMIN@ (2026-09-21, Tuesday): the nassync template hardcoded 03:30 for EVERY seat,
  # and this renderer substituted only PROJECT_DIR/SEAT/HOME — so installing nassync on Tuesday's
  # machine scheduled her leg at the SAME MINUTE as Wednesday's. That contradicts Kam's instruction
  # of 2026-09-08 14:57 ("Get Tuesday to sync at 11pm, and I think you should sync at 3 or 4am") and
  # puts TWO concurrent unison legs on the same NAS replicas with confirmbigdel = false. A schedule
  # is a per-seat fact and a template that cannot express it is a template that collides silently.
  case "$SEAT" in
    tuesday)   NASHOUR=23; NASMIN=0  ;;
    wednesday) NASHOUR=3;  NASMIN=30 ;;
    *)         NASHOUR=3;  NASMIN=30 ;;
  esac
  rendered="$(sed -e "s|@PROJECT_DIR@|$PROJECT_DIR|g" -e "s|@SEAT@|$SEAT|g" -e "s|@HOME@|$HOME|g" -e "s|@NASHOUR@|$NASHOUR|g" -e "s|@NASMIN@|$NASMIN|g" "$t")"

  loaded=0
  launchctl list 2>/dev/null | /usr/bin/grep -q "	$label\$" && loaded=1
  same=0
  [ -f "$target" ] && [ "$rendered" = "$(cat "$target")" ] && same=1

  if [ "$check" = "--check" ]; then
    # DRIFT: the on-disk plist and what launchd actually LOADED are two different facts, and
    # until 2026-09-16 this only ever compared the first one. That night all nine of Tuesday's
    # jobs had correct plists on disk and a STALE in-memory copy, because the fix reached the
    # files without an unload/load — so this printed "9 current, 0 missing" over jobs still
    # running the old config and failing EX_CONFIG(78). A check that reads the file instead of
    # the running system is a check that cannot see the failure it exists for.
    drift=""
    if [ "$loaded" = 1 ]; then
      # plutil, not a grep over XML: the key and its string share a line in these templates,
      # and a hand-rolled extractor that returns empty would report DRIFT on a healthy job.
      want_err="$(/usr/bin/plutil -extract StandardErrorPath raw "$target" 2>/dev/null)"
      have_err="$(launchctl print "gui/$(id -u)/$label" 2>/dev/null | /usr/bin/grep -i 'stderr path' | /usr/bin/sed 's/.*= //' | tr -d ' \t')"
      if [ -n "$want_err" ] && [ -n "$have_err" ] && [ "$want_err" != "$have_err" ]; then
        drift=" LOADED-DRIFT(launchd has: $have_err)"
      fi
    fi
    if [ "$same" = 1 ] && [ "$loaded" = 1 ] && [ -z "$drift" ]; then
      printf "  ok       %-16s loaded and matching the template\n" "$job"; current=$((current+1))
    else
      printf "  MISSING  %-16s on-disk-matches=%s loaded=%s%s\n" "$job" "$same" "$loaded" "$drift"; missing=$((missing+1))
    fi
    continue
  fi

  if [ "$same" = 1 ] && [ "$loaded" = 1 ]; then
    printf "  unchanged %-16s\n" "$job"; current=$((current+1)); continue
  fi
  # Keep whatever was there before overwriting it — never delete (Kam 2026-08-26).
  [ -f "$target" ] && cp "$target" "$target.pre-$(date +%Y%m%d_%H%M%S)"
  printf '%s\n' "$rendered" > "$target"
  launchctl unload "$target" 2>/dev/null
  if launchctl load "$target" 2>/dev/null; then
    printf "  installed %-16s (%s)\n" "$job" "$label"; installed=$((installed+1))
  else
    printf "  FAILED    %-16s launchctl load refused — read: launchctl error output above\n" "$job"; missing=$((missing+1))
  fi
done

echo
if [ "$check" = "--check" ]; then
  echo "jobs for seat '$SEAT': $current current, $missing missing"
  [ "$missing" -eq 0 ]
  exit $?
fi
echo "jobs for seat '$SEAT': $installed installed/refreshed, $current already current, $missing failed"
[ "$missing" -eq 0 ]
