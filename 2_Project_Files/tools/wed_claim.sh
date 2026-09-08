#!/bin/bash
# wed_claim.sh — ownership claims for WEDNESDAY-PROJECT (WED) work, so two coordinators
# never build the same thing twice.
#
# KAM'S RULE (panel, 2026-09-08, verbatim):
#   "from now on, any work on wednesday, take ownership so both agents dont work on the
#    same things"
#
# WHY A TOOL AND NOT A HABIT. Client work is already split by his 2026-09-07 11:01
# ruling — Secuura is the Studio's, Datasec is the laptop's. WED work is the half with
# NO owner, and it is exactly where the duplication risk lives. Measured the same
# morning: s150 read "item (b) is STILL NOT STARTED" out of a handover it had inherited
# from the other seat, repeated it to Kam, and began sizing a build of a chat filter
# that had existed since 2026-09-07. Nothing but opening the file stopped it. A claim
# that lives only in a handover is a claim the other seat cannot see.
#
# HOW IT SURVIVES TWO MACHINES. Both seats share one git repo and push constantly, so
# the claims file IS the shared surface. Every claim pulls first and pushes immediately:
# the push is the publication. If both seats claim at once, the second push rebases and
# the claimer SEES the other's claim before proceeding — the race resolves itself into
# a warning rather than into duplicated work.
#
# Usage:
#   wed_claim.sh claim   "<item>"   [--force]   take ownership; warns on an open claim
#   wed_claim.sh release "<item>"   [note]      mark done/dropped, with an optional note
#   wed_claim.sh list    [open|all]             default open
#   wed_claim.sh check   "<item>"                rc 0 = free, rc 3 = claimed by someone
# Exit: 0 ok · 2 usage · 3 already claimed (claim without --force, or check) · 4 git problem
set -u

# SELF-LOCATING (2026-09-08). This was hardcoded to '/Volumes/KK_T9_External_HDD/WEDNESDAY',
# the DEAD T9 path. On the Studio seat every write went to a nonexistent file and the tool
# still printed 'claim recorded locally' — a claim that did not exist. Same defect that was
# fixed in safe_push.sh on 2026-09-07; this sibling was written the same day and missed.
SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LEDGER="$PROJECT_DIR/0_Brain/tasks/WED-OWNERSHIP.md"
SEAT="$(hostname -s 2>/dev/null || hostname 2>/dev/null)"
NOW="$(date '+%Y-%m-%d %H:%M')"

usage() { echo "usage: wed_claim.sh claim|release|list|check ..." >&2; exit 2; }
CMD="${1:-}"; [ -n "$CMD" ] || usage

# The ledger is worthless if it is not current, so every command pulls first.
# --autostash because the dashboard writes constantly; never a write verb elsewhere.
sync_in() {
  # 2026-09-08: this line used to end `>/dev/null 2>&1`. On 2026-09-08 ~11:2x it
  # conflicted on chat_log.json against the other seat, left GIT CONFLICT MARKERS
  # in it, and the commit that followed PUSHED them — because the failure was
  # sent to /dev/null and nothing looked afterwards. A conflict you cannot see is
  # a conflict you commit. stderr is kept, and the two irreplaceable files are
  # checked AFTER the pull, every time.
  local out rc
  out="$(git -C "$PROJECT_DIR" pull --rebase --autostash 2>&1)"; rc=$?
  if [ $rc -ne 0 ]; then
    echo "wed_claim: WARNING — pull failed; this view may be stale and a claim may race" >&2
    printf '%s\n' "$out" | tail -5 >&2
  fi
  . "$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_store_guard.sh"
  guard_data_dir "$PROJECT_DIR/0_Brain/dashboard/data" || {
    echo "wed_claim: REFUSING to continue — repair the file above first." >&2; exit 8; }
}

ensure() {
  [ -f "$LEDGER" ] || cat > "$LEDGER" <<'HDR'
# WED ownership — who is doing which Wednesday-project item

**Kam's rule (panel, 2026-09-08, verbatim):** *"from now on, any work on wednesday, take
ownership so both agents dont work on the same things"*

Client work is already split (Secuura = Studio seat, Datasec = laptop seat). **This file is
for WED work — Wednesday's own project — which is the half with no owner.**

**Claim BEFORE starting, release when done.** Written by `2_Project_Files/tools/wed_claim.sh`,
which pulls before every read and pushes immediately after every write, so the other seat
sees the claim rather than discovering it in a conflict.

| Claimed (local) | Seat | Item | State | Released / note |
|---|---|---|---|---|
HDR
}

# An OPEN claim is a row whose State column reads OPEN, matched case-insensitively on the
# item text. Deliberately a substring match: near-miss wordings are the whole risk here,
# so this errs toward warning rather than toward silence.
find_open() {
  grep -i "^| .* | .* | .*$1.* | OPEN |" "$LEDGER" 2>/dev/null
}

case "$CMD" in
  claim)
    ITEM="${2:-}"; [ -n "$ITEM" ] || usage
    FORCE="${3:-}"
    sync_in; ensure
    EXIST="$(find_open "$ITEM")"
    if [ -n "$EXIST" ] && [ "$FORCE" != "--force" ]; then
      echo "wed_claim: REFUSED — an OPEN claim already matches \"$ITEM\":" >&2
      echo "$EXIST" >&2
      echo "If it is genuinely a different piece of work, re-run with --force and say so in the item text." >&2
      exit 3
    fi
    printf '| %s | %s | %s | OPEN | |\n' "$NOW" "$SEAT" "$ITEM" >> "$LEDGER"
    git -C "$PROJECT_DIR" add "$LEDGER" >/dev/null 2>&1
    git -C "$PROJECT_DIR" commit -q -m "WED claim: $ITEM ($SEAT)" >/dev/null 2>&1
    git -C "$PROJECT_DIR" push -q >/dev/null 2>&1 || { echo "wed_claim: claim recorded locally but PUSH FAILED — the other seat cannot see it yet" >&2; exit 4; }
    echo "claimed by $SEAT and published: $ITEM"
    ;;
  release)
    ITEM="${2:-}"; [ -n "$ITEM" ] || usage
    NOTE="${3:-done}"
    sync_in; ensure
    python3 - "$LEDGER" "$ITEM" "$NOTE" "$NOW" <<'PY'
import sys
led,item,note,now=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]
lines=open(led).read().split("\n"); hit=False
for i,l in enumerate(lines):
    if l.startswith("| ") and item.lower() in l.lower() and "| OPEN |" in l:
        lines[i]=l.replace("| OPEN |","| CLOSED |").rstrip()
        if lines[i].endswith("|"): lines[i]=lines[i][:-1]+" %s %s |"%(now,note)
        hit=True
open(led,"w").write("\n".join(lines))
print("released" if hit else "wed_claim: no OPEN claim matched — nothing changed")
PY
    git -C "$PROJECT_DIR" add "$LEDGER" >/dev/null 2>&1
    git -C "$PROJECT_DIR" commit -q -m "WED release: $ITEM ($SEAT)" >/dev/null 2>&1
    git -C "$PROJECT_DIR" push -q >/dev/null 2>&1 || echo "wed_claim: release recorded locally but PUSH FAILED" >&2
    ;;
  check)
    ITEM="${2:-}"; [ -n "$ITEM" ] || usage
    sync_in; ensure
    EXIST="$(find_open "$ITEM")"
    [ -z "$EXIST" ] && { echo "free: $ITEM"; exit 0; }
    echo "CLAIMED:"; echo "$EXIST"; exit 3
    ;;
  list)
    sync_in; ensure
    if [ "${2:-open}" = "all" ]; then grep '^| 20' "$LEDGER" 2>/dev/null || echo "(no claims yet)"
    else grep '^| 20' "$LEDGER" 2>/dev/null | grep '| OPEN |' || echo "(no open claims)"; fi
    ;;
  *) usage ;;
esac
