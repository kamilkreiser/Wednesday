#!/bin/bash
# daily_sweep.sh — Kam's 15:00 Sydney sweep (panel, 2026-09-10 11:41):
#   "create a new schedule to archive items that have been deployed, merged, or
#    completed at the end of the day, and add to this schedule to archive,
#    deploy, or merge any items that are ready to do so."
#   "Do this at 3pm Sydney time."   (11:41:58)
#
# WHAT IT DOES, AND THE LINE IT DRAWS
#   ARCHIVE  — EXECUTES. Linear archive is reversible (unarchive), so it is the
#              one action safe to run unattended.
#   MERGE    — LISTS candidates and their exact blocker. Does NOT merge on its
#              own; a merge is irreversible-ish and this seat's standing rules
#              put it behind a live coordinator. Promote once proven.
#   DEPLOY   — LISTS only, always. Demo-affecting actions ALWAYS pause for Kam
#              (his own standing rule), and 2026-09-10 showed a demo deploy
#              return five green signals and change nothing.
#
# ⚠ THE TRAP THIS SCRIPT EXISTS TO AVOID, measured 2026-09-10 before it was written:
#   The KS board has FOUR states of Linear type `completed`, and one of them is
#   "Tested Not Deployed" — which means the exact opposite of shipped. A filter on
#   state TYPE would archive precisely the work that is waiting to go out. So the
#   archive set is an explicit ALLOW-LIST OF STATE NAMES and never a type test.
#
# SCOPE: this seat coordinates Secuura + Wednesday's own board. Datasec belongs to
# the other coordinator and is never touched (hard rule 2).
#
# Usage: daily_sweep.sh            # normal run (archive executes)
#        daily_sweep.sh --report   # report only, change nothing
#   env: DRYRUN=1 / WEDNESDAY_DRYRUN=1  same as --report
#        WEDNESDAY_TEST_HOUR=15          exercise the window guard off-hours
set -u

SELF_DIR="$(cd -P "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd -P "$SELF_DIR/../.." && pwd)"
LOG_DIR="$SELF_DIR/logs"; STATE_DIR="$SELF_DIR/state"
mkdir -p "$LOG_DIR" "$STATE_DIR"
LOG="$LOG_DIR/sweep_$(date +%F).log"
log(){ echo "$(date '+%F %T') $*" >> "$LOG"; }
TODAY="$(date +%F)"

DRYRUN="${WEDNESDAY_DRYRUN:-${DRYRUN:-0}}"
[ "${1:-}" = "--report" ] && DRYRUN=1
[ -n "${1:-}" ] && [ "${1:-}" != "--report" ] && { echo "usage: daily_sweep.sh [--report]" >&2; exit 2; }

# ── SEAT GUARD — the inner half of hard rule 2 ─────────────────────────────
# This sweep archives SECUURA and WEDNESDAY tickets. If it is ever armed on the
# Datasec coordinator's machine, it would archive another client's board on a
# timer with nobody watching. The installer arms it for Wednesday only; this
# refuses independently, because a guard that lives only in the installer is a
# guard that a hand-copied plist walks straight past.
SEAT="${WED_AGENT:-wednesday}"
if [ "$SEAT" != "wednesday" ]; then
  log "REFUSED: WED_AGENT=$SEAT — the daily sweep is Wednesday's seat only (it sweeps Secuura + WED)"
  exit 0
fi
case "$PROJECT_DIR" in
  */WEDNESDAY) : ;;
  *) log "REFUSED: PROJECT_DIR=$PROJECT_DIR is not a WEDNESDAY tree"; exit 0 ;;
esac

# ── GUARDS ──────────────────────────────────────────────────────────────────
if [ -f "$STATE_DIR/last_sweep" ] && [ "$(cat "$STATE_DIR/last_sweep")" = "$TODAY" ]; then
  log "skip: already swept today"; exit 0
fi
HOUR="$((10#${WEDNESDAY_TEST_HOUR:-$(date +%H)}))"
# launchd coalesces a missed job to the next wake; a sweep firing at 04:00 would
# archive a day nobody has finished. Window, not a point.
if [ "$HOUR" -lt 14 ] || [ "$HOUR" -gt 17 ]; then
  log "skip: outside the 14:00-17:59 window (hour=$HOUR)"; exit 0
fi

# FIRST RUN IS ALWAYS A REPORT. Night one is observed, not trusted: this script
# archives in bulk and the first run meets a backlog nobody has reviewed.
FIRST_RUN=0
[ -f "$STATE_DIR/sweep_armed" ] || { FIRST_RUN=1; DRYRUN=1; }

# ── CREDENTIALS (read at point of use; never echoed) ────────────────────────
SEC_ENV="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env"
getval(){ grep -E "^$1=" "$2" 2>/dev/null | head -1 | cut -d= -f2- | tr -d "\"'"; }
KS_KEY="$(getval LINEAR_API_KEY "$SEC_ENV")"
GH_TOKEN="$(getval GH_TOKEN "$SEC_ENV")"; export GH_TOKEN
WED_KEY="$(getval LINEAR_API_KEY "$PROJECT_DIR/4_Credentials/.env")"

REPORT="$LOG_DIR/sweep_report_$TODAY.md"
: > "$REPORT"
say(){ printf '%s\n' "$*" >> "$REPORT"; }

say "# Daily sweep — $TODAY $(date +%H:%M) $(date +%Z)"
say ""
if [ "$FIRST_RUN" = "1" ]; then
  say "**FIRST RUN — REPORT ONLY. Nothing was changed.** Night one is observed rather than trusted:"
  say "this sweep archives in bulk and the first run meets a backlog nobody has reviewed. Arm it with"
  say "\`touch $STATE_DIR/sweep_armed\` once the numbers below look right."
  say ""
elif [ "$DRYRUN" = "1" ]; then
  say "**REPORT ONLY (dry run). Nothing was changed.**"; say ""
fi

# ── 1. ARCHIVE — the only action that executes ──────────────────────────────
# Allow-list of state NAMES. "Tested Not Deployed" is deliberately absent: it is
# Linear type `completed` and means NOT shipped.
ARCHIVE_STATES='["Done","Deployed to UAT","Deployed To Prod","Canceled","Duplicate"]'
ARCHIVE_CAP=60   # a bigger set is reported, never executed — see the cap note below

sweep_team(){  # $1=team key  $2=api key  $3=label
  local TKEY="$1" AKEY="$2" LABEL="$3"
  [ -n "$AKEY" ] || { say "- **$LABEL**: no Linear key available — skipped, NOT assumed empty."; return; }
  python3 - "$TKEY" "$AKEY" "$LABEL" "$REPORT" "$DRYRUN" "$ARCHIVE_CAP" "$ARCHIVE_STATES" <<'PY'
import sys, json, urllib.request
tkey, akey, label, report = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
dry, cap, states = sys.argv[5] == "1", int(sys.argv[6]), json.loads(sys.argv[7])
out = open(report, "a")

def call(query, variables=None):
    body = {"query": query}
    if variables: body["variables"] = variables
    r = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps(body).encode(),
                               headers={"Authorization": akey, "Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(r, timeout=45).read().decode())

Q = "query($t:String!,$s:[String!]!){ issues(filter:{ team:{ key:{ eq:$t } }, state:{ name:{ in:$s } } }, first:250){ pageInfo{ hasNextPage } nodes{ id identifier title state{ name } } } }"
try:
    d = call(Q, {"t": tkey, "s": states})
except Exception as e:
    out.write("- **%s**: query FAILED (%s) — REPORTED, not treated as zero.\n" % (label, e)); raise SystemExit
if d.get("errors"):
    out.write("- **%s**: API errors — %s. REPORTED, not zero.\n" % (label, json.dumps(d["errors"])[:200])); raise SystemExit
iss = (d.get("data") or {}).get("issues")
if iss is None:
    out.write("- **%s**: no issues field — %s. REPORTED, not zero.\n" % (label, json.dumps(d)[:180])); raise SystemExit
nodes = iss["nodes"]
if iss["pageInfo"]["hasNextPage"]:
    out.write("- **%s**: MORE THAN 250 matches — this is a PAGE, not a total. Refusing to quote a count or act on it.\n" % label); raise SystemExit
if not nodes:
    out.write("- **%s**: nothing to archive (0 in %s).\n" % (label, ", ".join(states))); raise SystemExit
by = {}
for n in nodes: by[n["state"]["name"]] = by.get(n["state"]["name"], 0) + 1
out.write("- **%s**: **%d** archivable — %s\n" % (label, len(nodes), " · ".join("%s %d" % (k, v) for k, v in sorted(by.items()))))
if len(nodes) > cap:
    out.write("  - OVER THE CAP OF %d — reported, NOT archived. A first bulk archive of this size is a decision, not a chore. Raise with Kam.\n" % cap); raise SystemExit
if dry:
    for n in nodes[:15]: out.write("  - would archive %s (%s) %s\n" % (n["identifier"], n["state"]["name"], n["title"][:64]))
    if len(nodes) > 15: out.write("  - ...and %d more\n" % (len(nodes) - 15))
    raise SystemExit
ok = fail = 0
for n in nodes:
    try:
        res = call("mutation($id:String!){ issueArchive(id:$id){ success } }", {"id": n["id"]})
        if ((res.get("data") or {}).get("issueArchive") or {}).get("success"): ok += 1
        else:
            fail += 1; out.write("  - FAILED %s: %s\n" % (n["identifier"], json.dumps(res)[:120]))
    except Exception as e:
        fail += 1; out.write("  - FAILED %s: %s\n" % (n["identifier"], e))
out.write("  - archived **%d**, failed **%d** (reversible — unarchive in Linear)\n" % (ok, fail))
PY
}

say "## 1. Archived (executes — Linear archive is reversible)"
say ""
sweep_team "KS"  "$KS_KEY"  "Secuura/Platform K"
sweep_team "WED" "$WED_KEY" "Wednesday's own board"
say ""

# ── 2. MERGE — listed with the exact blocker, never merged unattended ───────
say "## 2. Ready to merge — LISTED, not merged"
say ""
if [ -z "$GH_TOKEN" ]; then
  say "- no GitHub token available — skipped, NOT assumed empty."
else
  # NEVER discard stderr (own rule, ledger): the first version sent gh 2>/dev/null
  # and the report could only say "unreadable", which is a failure you cannot diagnose.
  PRJSON="$(gh pr list --repo Secuura/Distributed_Secuura --state open --limit 100 \
              --json number,title,isDraft,reviewDecision,mergeable,mergeStateStatus 2>"$LOG_DIR/gh_err.$$")"
  GHRC=$?
  if [ "$GHRC" -ne 0 ] || [ -z "$PRJSON" ]; then
    say "- \`gh pr list\` FAILED (rc=$GHRC) — REPORTED, not treated as zero: $(head -c 300 "$LOG_DIR/gh_err.$$" | tr '\n' ' ')"
  else
    printf %s "$PRJSON" > "$LOG_DIR/pr.$$"
    python3 - "$REPORT" "$LOG_DIR/pr.$$" <<'PY'
import sys, json
out = open(sys.argv[1], "a")
try: prs = json.load(open(sys.argv[2]))
except Exception as e:
    out.write("- PR list unparseable (%s) — REPORTED, not treated as zero.\n" % e); raise SystemExit
live = [x for x in prs if not x["isDraft"]]
ready = [x for x in live if x["reviewDecision"] == "APPROVED" and x["mergeable"] == "MERGEABLE"]
blocked = [x for x in live if x["reviewDecision"] == "APPROVED" and x["mergeable"] != "MERGEABLE"]
out.write("- %d open non-draft PRs · **%d approved AND mergeable** · %d approved but blocked\n" % (len(live), len(ready), len(blocked)))
for x in ready: out.write("  - READY **#%d** %s\n" % (x["number"], x["title"][:70]))
for x in blocked: out.write("  - BLOCKED #%d approved but %s / %s — %s\n" % (x["number"], x["mergeable"], x["mergeStateStatus"], x["title"][:52]))
if not ready and not blocked:
    out.write("  - nothing approved is waiting. If that looks wrong, the approval bottleneck is the agent GitHub identity (Kam ruled it 2026-08-26, unactioned).\n")
PY
  fi
  rm -f "$LOG_DIR/gh_err.$$" "$LOG_DIR/pr.$$"
fi
say ""
say "## 3. Ready to deploy — LISTED ONLY, always"
say ""
if [ -n "$KS_KEY" ]; then
  python3 - "$REPORT" "$KS_KEY" <<'PY'
import sys, json, urllib.request
out = open(sys.argv[1], "a"); akey = sys.argv[2]
Q = "query{ issues(filter:{ team:{ key:{ eq:\"KS\" } }, state:{ name:{ eq:\"Tested Not Deployed\" } } }, first:250){ pageInfo{ hasNextPage } nodes{ identifier title } } }"
try:
    r = urllib.request.Request("https://api.linear.app/graphql", data=json.dumps({"query": Q}).encode(),
                               headers={"Authorization": akey, "Content-Type": "application/json"})
    d = json.loads(urllib.request.urlopen(r, timeout=45).read().decode())
except Exception as e:
    out.write("- query FAILED (%s) — REPORTED, not treated as zero.\n" % e); raise SystemExit
if d.get("errors"):
    out.write("- API errors — %s. REPORTED, not zero.\n" % json.dumps(d["errors"])[:200]); raise SystemExit
iss = (d.get("data") or {}).get("issues")
if iss is None:
    out.write("- no issues field — %s. REPORTED, not zero.\n" % json.dumps(d)[:180]); raise SystemExit
if iss["pageInfo"]["hasNextPage"]:
    out.write("- MORE THAN 250 — a page, not a total. Not quoting a count.\n"); raise SystemExit
n = iss["nodes"]
out.write("- **%d** ticket(s) in **Tested Not Deployed** — tested, NOT shipped. Deliberately NOT archived by section 1.\n" % len(n))
for i in n[:20]: out.write("  - %s %s\n" % (i["identifier"], i["title"][:70]))
if len(n) > 20: out.write("  - ...and %d more\n" % (len(n) - 20))
out.write("- **Deploying is Kam's signature class and this sweep never does it.**\n")
PY
else
  say "- no Linear key for KS — skipped, NOT assumed empty."
fi
say ""
say "---"
say "_Archive executes; merge and deploy are listed. Datasec is the other coordinator's and is never touched._"

[ "$DRYRUN" = "1" ] || echo "$TODAY" > "$STATE_DIR/last_sweep"
log "sweep complete (dryrun=$DRYRUN first_run=$FIRST_RUN) -> $REPORT"

# ── Put it where Kam reads, not only in a log nobody opens ──────────────────
# BUT NOT WHEN BEING EXERCISED. WEDNESDAY_TEST_HOUR is the test hook, and five
# test runs while building this put five duplicate sweep reports into Kam's chat
# — polluting the exact surface this fleet built the chat mirror to protect.
# A tool that writes to the principal's reading surface must be silent under its
# own test hook, or every exercise costs him a scroll.
if [ -n "${WEDNESDAY_TEST_HOUR:-}" ]; then
  log "exercise run (WEDNESDAY_TEST_HOUR set) — chat mirror SUPPRESSED; report at $REPORT"
elif [ -x "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" ] || [ -f "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" ]; then
  SUMMARY="$(sed -n '1,40p' "$REPORT")"
  bash "$PROJECT_DIR/2_Project_Files/tools/chat_reply.sh" --project WED "DAILY SWEEP $TODAY. Full report: 2_Project_Files/scheduler/logs/sweep_report_$TODAY.md

$SUMMARY" >> "$LOG" 2>&1 || log "WARN chat_reply failed"
fi
echo "report: $REPORT"
