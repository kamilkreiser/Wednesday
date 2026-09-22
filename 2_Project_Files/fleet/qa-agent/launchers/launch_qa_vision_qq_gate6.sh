#!/bin/bash
# launch_qa_vision_qq_gate6.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 6, 2026-09-23) on
# Datasec/Vision_Sales_Portal, TWO repos, TWO targets, BOTH ROUND 2 of 2:
#   IO1R2  P   fix/portal-async-route-errors-2026-09-23     TIER 1  (gate 5's IO1 = gate 4's I10-O1; ROUND 2 of 2; on main 6f197ca)
#   BCR2   QQ  fix/qq-bounded-browser-close-2026-09-23      TIER 2  (gate 5's BC; ROUND 2 of 2; STALE base 3bfbfa2, main is now d4426f8)
# Portal S-1 (fix/feedback-report-auth-2026-09-22 @ 89af8ba) is GO from gate 2 and NOT in this gate — but it now overlaps IO1R2 in
# server/errors.js and server/routes/feedback.js and sits on a pre-I10 base; the brief's §12 makes the gate measure that.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it carries no
# head of its own — refuses any placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW,
# and appends the verified table to the agent's prompt. The only shas it carries are GATED ANCHORS (a83140e = IO1 round 1,
# aa89010 = BC round 1): facts about what gate 5 gated, not heads.
#
# AUTHORITY: Tuesday's gate-5 rulings (daily note 2026-09-23 04:02 and 04:37) — IO1 returns for a one-line round 2 carrying IO1-F1
# plus the two authorised pre-existing MAJORs (IO1-O2, IO1-O3), with IO1-F2/F3/P1 ticketed only; BC returns with gate 5's two probed
# fix-shapes plus a child-process exit cell. Batching is Kam's standing rule of 2026-09-18. Kam's cap rule is C-62 (a Major at round
# 2 of 2 is ticketed; only a third round on the same class needs his word). Merges after this gate are Tuesday's GO. Deploys HELD for Kam.
#
# PATTERN: launch_qa_vision_qq_gate5.sh. CHANGES:
#   - no SLOT this gate: the PIN table is 4 rows (MAIN-P MAIN-Q IO1R2 BCR2) and NO row may be OUT, so gate 5's exit 41 is gone.
#   - exit 7: base is MAIN or a STALE BASE (NOTE); BCR2 is EXPECTED stale (A9 + CF5R2 merged after gate 5), IO1R2 is not.
#   - exit 9: anchors — IO1R2 contains a83140e AND its server/asyncErrors.js blob EQUALS a83140e's (round 2 does not touch the patch);
#     BCR2 contains aa89010; IO1R2's base wires I10's lastResortHandler; BCR2's base calls closeBrowser only from the two test files.
#   - exit 22: exact file sets — IO1R2 9 files over main, BCR2 13 over 3bfbfa2.
#   - exit 73 IO1R2, 74 BCR2: content guards keyed on the ACTUAL code at each pinned head (drafted 04:4x AEST). 73 pins the res.destroy
#     fix, the two serverError imports, pool.on('error') and the four new cells, and REFUSES round 1's un-destroyed headersSent line.
#     74 proves lib/pdf.js differs ONLY inside closeBrowser(), package.json only in test scripts, and pins the stdio loop, the NaN-proof
#     bound, both after(() => closeBrowser()) call sites and the child-process cell + its two fixtures.
#   - exit 57: premises on the MAIN rows (portal main wires lastResortHandler; express 4.22.2; QQ main carries A9 + CF5R2 — advisory).
#   - exit 63: lockfiles — every row's lockfile equals its BASE's (neither target changes a dependency).
#   - exit 62: the Vision floor discipline with gate-6 database names (vsp_qa_g6_, the _test suffix; never g1..g5).
#   - exit 76 (new): the ROUND-2-of-2 cap — C-62 quoted in both files and the ships/tickets instruction in the prompt.
#   - exit 20: the QUESTIONS route ('[Wednesday -> QA/Vision-gate6] ANSWER'); exit 70: the safety-check line.
#   - exit 31/39: gate 5's report, its harnesses and its Vision floor instrument are on disk and named.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 3434 (%0), NexusAI 8360 (%44), NexusAI gate-7-r2 QA 40615 (%50).
#   - exit 75: the standing lines — controls fail independently, PRIOR WORK verified against history, merge-tree from the gate's OWN
#     object dirs, no writes in either repo, three head readings, NOT TESTED, no production — in both files.
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate6' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate6.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..76 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparands, BUILT so that no sed of the placeholder text can reach them.
PH_SCTS='@SELFCHECK''_TS@'
PH_SCNOTE='@SELFCHECK''_NOTE@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate6.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate6.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G5_DIR="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate5"
G5_REPORT="$G5_DIR/report.md"
G5_FLOOR="$G5_DIR/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate6/report.md"
NEG_SEATS='1613 3434 8360 40615'   # Vision builder (%41), Tuesday (%0), NexusAI (%44), NexusAI gate-7-r2 QA (%50) at drafting
# Gated anchors (not heads): the round-1 heads gate 5 gated.
ANCHOR_IO1='a83140ebcbbd29b50f054e3b088c5cbed43efa09'
ANCHOR_BC='aa8901067aec9bb0ff8ec6f296f51e9cd029b572'

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 6: I10-O1 async route errors round 2 of 2 (tier 1, portal) + bounded browser.close round 2 of 2 (tier 2, QuickQuote), heads as pinned at launch'

q() { git --no-optional-locks -C "$QQ_REPO" "$@"; }
p() { git --no-optional-locks -C "$P_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
repo_fn() { case "$1" in portal) echo p ;; quickquote) echo q ;; *) echo x ;; esac; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
for R in "$QQ_REPO" "$P_REPO"; do
  [ -d "$R/.git" ] || [ -f "$R/.git" ] || { echo "repo under test missing: $R" >&2; exit 5; }
done

# 40 — parse the PIN table from the brief (the ONLY source of heads). Output: id repo branch head base commits status (TAB).
PIN="$(python3 - "$BRIEF" <<'PY'
import sys, re
s = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r'<!-- PIN-HEADS:BEGIN -->(.*?)<!-- PIN-HEADS:END -->', s, re.S)
if not m:
    print('NO-BLOCK'); sys.exit(0)
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('| id ') or set(line) <= set('|-: '):
        continue
    cells = [c.strip().strip('`') for c in line.strip('|').split('|')]
    print('\t'.join(cells))
PY
)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
EXPECT_IDS='MAIN-P MAIN-Q IO1R2 BCR2'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "4" ] || { echo "REFUSING: PIN table carries rows beyond the four expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  [ "$ST" = "IN" ] || { echo "REFUSING: PIN row $ID status is '$ST' — no row may be OUT in this gate (IN only; unfilled?)" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN row $ID still carries a placeholder: $R" >&2; exit 40; }
  is40 "$(fld "$ID" 4)" || { echo "REFUSING: PIN row $ID head is not a 40-hex sha: '$(fld "$ID" 4)'" >&2; exit 40; }
  case "$ID" in
    MAIN-*) [ "$(fld "$ID" 3)" = "main" ] || { echo "REFUSING: row $ID branch must be main" >&2; exit 40; } ;;
    *) is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
       printf '%s' "$(fld "$ID" 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row $ID commits is not a positive integer" >&2; exit 40; } ;;
  esac
  [ "$(repo_fn "$(fld "$ID" 2)")" != "x" ] || { echo "REFUSING: PIN row $ID repo must be portal or quickquote" >&2; exit 40; }
done
[ "$(fld MAIN-P 2)" = "portal" ] && [ "$(fld MAIN-Q 2)" = "quickquote" ] || { echo "REFUSING: MAIN-P must be portal, MAIN-Q quickquote" >&2; exit 40; }
[ "$(fld IO1R2 2)" = "portal" ]   || { echo "REFUSING: row IO1R2 must be the portal repo" >&2; exit 40; }
[ "$(fld BCR2 2)" = "quickquote" ] || { echo "REFUSING: row BCR2 must be the quickquote repo" >&2; exit 40; }
exp_branch() { case "$1" in
  IO1R2) echo fix/portal-async-route-errors-2026-09-23 ;; BCR2) echo fix/qq-bounded-browser-close-2026-09-23 ;; esac; }
for ID in IO1R2 BCR2; do
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS='IO1R2 BCR2'
grep -q '<fill at launch>' "$BRIEF" && { echo "REFUSING: the brief still carries a '<fill at launch>' marker" >&2; exit 40; }

# 6 / 7 / 8 — per row: commit in its repo; base ancestor AND merge-base; exact commit count; base is MAIN or a STALE BASE.
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; H="$(fld "$ID" 4)"
  T="$($G cat-file -t "$H" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: row $ID head $H is not a commit in its repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
STALE=''
for ID in $IN_IDS; do
  REPO="$(fld "$ID" 2)"; G="$(repo_fn "$REPO")"; H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"
  T="$($G cat-file -t "$BASE" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: row $ID base $BASE is not a commit (got '$T')" >&2; exit 6; }
  MAINH="$( [ "$REPO" = portal ] && fld MAIN-P 4 || fld MAIN-Q 4 )"
  OK=0; [ "$BASE" = "$MAINH" ] && OK=1
  if [ "$OK" = 0 ] && $G merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null \
     && [ "$($G merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
    OK=1; STALE="$STALE $ID"
    echo "NOTE: row $ID is a STALE-BASE row: base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7} and the merge-base; a forward merge is owed at merge time (§12)" >&2
  fi
  [ "$OK" = 1 ] || { echo "REFUSING: row $ID base ${BASE:0:7} is neither its repo's MAIN row nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7; }
  $G merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: row $ID base ${BASE:0:7} is not an ancestor of ${H:0:7}" >&2; exit 7; }
  [ "$($G merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(row $ID base, head) is not the base" >&2; exit 7; }
  GOTN="$($G rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: row $ID has $GOTN commits over its base, the table says $N" >&2; $G log --format='%h %s' "${BASE}..${H}" >&2; exit 8; }
done
case " $STALE " in *" BCR2 "*) ;; *) echo "NOTE: row BCR2 was expected to be STALE-BASE (A9 + CF5R2 merged after gate 5) and is not — the brief's §12 and correction (a)/(b) may be stale" >&2 ;; esac
case " $STALE " in *" IO1R2 "*) echo "NOTE: row IO1R2 was expected to sit on the MAIN row and is STALE-BASE — portal main moved; the brief's §12 expectation for it may be stale" >&2 ;; esac

# 9 — gated anchors and base premises.
p merge-base --is-ancestor "$ANCHOR_IO1" "$(fld IO1R2 4)" 2>/dev/null \
  || { echo "REFUSING: IO1R2's head does not contain gate 5's gated round-1 head a83140e — not a round 2; re-brief" >&2; exit 9; }
[ -n "$(p rev-parse "$ANCHOR_IO1:server/asyncErrors.js" 2>/dev/null)" ] \
  && [ "$(p rev-parse "$ANCHOR_IO1:server/asyncErrors.js" 2>/dev/null)" = "$(p rev-parse "$(fld IO1R2 4):server/asyncErrors.js" 2>/dev/null)" ] \
  || { echo "REFUSING: IO1R2's server/asyncErrors.js differs from gate 5's round-1 head a83140e — the brief says round 2 carries the patch module unchanged; re-brief" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_BC" "$(fld BCR2 4)" 2>/dev/null \
  || { echo "REFUSING: BCR2's head does not contain gate 5's gated round-1 head aa89010 — not a round 2; re-brief" >&2; exit 9; }
p show "$(fld IO1R2 5):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: IO1R2's base does not wire I10's lastResortHandler — the brief's premise is stale" >&2; exit 9; }
CALLERS="$(q grep -l 'closeBrowser' "$(fld BCR2 5)" -- stage3 2>/dev/null | sed "s#^$(fld BCR2 5):##" | grep -v '^stage3/lib/pdf\.js$' | grep -v '/node_modules/' | sort)"
[ "$CALLERS" = "$(sorted 'stage3/test/fx-provenance.mjs
stage3/test/typed-rates.mjs')" ] || { echo "REFUSING: at BCR2's base closeBrowser is referenced outside the two test files the brief names:" >&2; printf '%s\n' "$CALLERS" >&2; exit 9; }

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets.
FS_IO1R2='BACKLOG.md
server/asyncErrors.js
server/asyncErrors.test.js
server/db.js
server/errors.js
server/index.js
server/routes/admin.js
server/routes/feedback.js
test/db/async-faults.test.js'
FS_BCR2='stage3/lib/pdf.js
stage3/package.json
stage3/test/email-collector.mjs
stage3/test/fixtures/browser-file.mjs
stage3/test/fixtures/hang-close.cjs
stage3/test/fx-provenance.mjs
stage3/test/lib-close-shared.test.mjs
stage3/test/lib-close.mjs
stage3/test/lib-close.test.mjs
stage3/test/phone-layout.mjs
stage3/test/print-fit.mjs
stage3/test/typed-rates.mjs
stage3/test/xlsx-parity.mjs'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in IO1R2 BCR2; do
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done

# Content guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 73 — IO1R2 (I10-O1 round 2): the res.destroy fix, the two serverError imports, the idle pool handler, the four new cells.
has IO1R2 server/errors.js "if (!res.headersSent) return void res.status(500).json({ error: 'Internal error', ref });" \
  || { echo "REFUSING: IO1R2's errors.js lacks the round-2 pre-headers branch (return void ...) — re-brief" >&2; exit 73; }
has IO1R2 server/errors.js 'if (!res.writableEnded) res.destroy(e instanceof Error ? e : new Error(String(e)));' \
  || { echo "REFUSING: IO1R2's errors.js does not destroy a response whose headers were already sent — IO1-F1 is not fixed the way the brief says; re-brief" >&2; exit 73; }
has IO1R2 server/errors.js "if (!res.headersSent) res.status(500).json({ error: 'Internal error', ref });" \
  && { echo "REFUSING: IO1R2's errors.js still carries round 1's un-ended headersSent branch verbatim" >&2; exit 73; }
for F in server/routes/feedback.js server/routes/admin.js; do
  has IO1R2 "$F" "const { serverError } = require('../errors');" \
    || { echo "REFUSING: IO1R2 does not import serverError in $F — IO1-O2 is not fixed; re-brief" >&2; exit 73; }
done
has IO1R2 server/db.js "pool.on('error', (err) => {" \
  || { echo "REFUSING: IO1R2's db.js registers no pool.on('error') — IO1-O3 is not fixed; re-brief" >&2; exit 73; }
has IO1R2 server/asyncErrors.test.js 'IO1-F1: a rejection AFTER the response started closes the connection instead of hanging the client' \
  || { echo "REFUSING: IO1R2 has no IO1-F1 regression cell in the unit suite — re-brief" >&2; exit 73; }
for S in 'IO1-O2: a fault in the UNAUTHENTICATED GET /api/feedback/summary logs the real fault' \
         'IO1-O2 + IO1-F1: the streaming backup route faulted MID-STREAM breaks the connection and logs the real fault' \
         'IO1-O3: a dropped IDLE pooled connection does not kill the process'; do
  has IO1R2 test/db/async-faults.test.js "$S" || { echo "REFUSING: IO1R2's DB-fault suite lacks the cell: $S — re-brief" >&2; exit 73; }
done
has IO1R2 test/db/async-faults.test.js 'serverError is not defined' \
  || { echo "REFUSING: IO1R2's new cells do not assert against the ReferenceError the missing import produced — re-brief" >&2; exit 73; }
has IO1R2 server/index.js "require('./asyncErrors');" || { echo "REFUSING: IO1R2 no longer requires ./asyncErrors in the portal's app module" >&2; exit 73; }
# 74 — BCR2 (bounded close round 2): lib/pdf.js may change ONLY inside closeBrowser(); package.json only in test scripts.
python3 - "$(q show "$(fld BCR2 5):stage3/lib/pdf.js" 2>/dev/null)" "$(q show "$(fld BCR2 4):stage3/lib/pdf.js" 2>/dev/null)" <<'PY' || { echo "REFUSING: BCR2 changes stage3/lib/pdf.js OUTSIDE closeBrowser() (renderQuotePdf / the launch / exports / a new helper) — the brief gates a closeBrowser-only change; re-brief" >&2; exit 74; }
import sys
def strip(s):
    # the function takes parameters (closeBrowser(ms = 5000)) and its leading /* For tests ... */ comment belongs to it
    f = s.find('async function closeBrowser(')
    if f < 0: sys.exit(1)
    c = s.rfind('/* For tests', 0, f)
    i = c if (c >= 0 and s.find('*/', c) < f) else f
    j = s.find('{', s.find(')', f)); d = 0
    for k in range(j, len(s)):
        if s[k] == '{': d += 1
        elif s[k] == '}':
            d -= 1
            if d == 0: return s[:i] + '<<closeBrowser>>' + s[k+1:]
    sys.exit(1)
sys.exit(0 if strip(sys.argv[1]) == strip(sys.argv[2]) else 1)
PY
PJ="$(q diff "$(fld BCR2 5)" "$(fld BCR2 4)" 2>/dev/null -- stage3/package.json | grep -E '^[+-]' | grep -v '^[+-][+-]')"
BADPJ="$(printf '%s\n' "$PJ" | grep -vE '^[+-]    "test(:[a-z]+)?": ')"
[ -z "$BADPJ" ] || { echo "REFUSING: BCR2's stage3/package.json delta is not test scripts only:" >&2; printf '%s\n' "$BADPJ" >&2; exit 74; }
for F in stage3/lib/pdf.js stage3/test/lib-close.mjs; do
  has BCR2 "$F" 'const limit = Number.isFinite(Number(ms)) && Number(ms) > 0 ? Number(ms) : 5000;' \
    || { echo "REFUSING: BCR2's $F has no NaN-proof bound (the BC-F2 coercion the brief quotes) — re-brief" >&2; exit 74; }
  has BCR2 "$F" 'for (const s of child.stdio || [])' \
    || { echo "REFUSING: BCR2's $F does not destroy the child's stdio after the kill (the BC-F1 fix the brief quotes) — re-brief" >&2; exit 74; }
done
for F in stage3/test/typed-rates.mjs stage3/test/fx-provenance.mjs; do
  has BCR2 "$F" 'after(() => closeBrowser());' \
    || { echo "REFUSING: BCR2's $F does not wrap the close hook — BC-F2's call site is unfixed; re-brief" >&2; exit 74; }
  has BCR2 "$F" 'after(closeBrowser);' \
    && { echo "REFUSING: BCR2's $F still passes closeBrowser as the hook itself (node:test would hand it a TestContext — BC-F2)" >&2; exit 74; }
done
has BCR2 stage3/test/lib-close.test.mjs 'BC-F1 (child process): a whole test FILE whose close() never returns still exits on its own' \
  && has BCR2 stage3/test/lib-close.test.mjs 'BC-F2: a bound that is not a number (node:test hands after() its TestContext) does not kill a healthy Chrome' \
  || { echo "REFUSING: BCR2's cells are not the child-process and NaN-bound cells the brief quotes — re-brief" >&2; exit 74; }
for F in stage3/test/fixtures/browser-file.mjs stage3/test/fixtures/hang-close.cjs; do
  [ -n "$(q rev-parse "$(fld BCR2 4):$F" 2>/dev/null)" ] || { echo "REFUSING: BCR2 lacks the child-process cell's fixture $F — re-brief" >&2; exit 74; }
done
has BCR2 stage3/package.json 'test/lib-close.test.mjs' \
  || { echo "REFUSING: BCR2's test:print does not run lib-close.test.mjs — the child-process cell would never run" >&2; exit 74; }
# 57 — premises on the MAIN rows.
p show "$(fld MAIN-P 4):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: portal main does not wire lastResortHandler — IO1R2's premise (serverError answers the faults) is stale" >&2; exit 57; }
python3 - "$(p show "$(fld IO1R2 4):package-lock.json" 2>/dev/null)" <<'PY' || { echo "REFUSING: IO1R2's lockfile does not resolve express 4.22.2 — the brief's line-by-line comparison names 4.22.2" >&2; exit 57; }
import sys, json
b = json.loads(sys.argv[1])["packages"]
sys.exit(0 if b.get("node_modules/express", {}).get("version") == "4.22.2" else 1)
PY
q merge-base --is-ancestor '5d787d24a7b2ed8d33d319bd495b35ee0dbd96be' "$(fld MAIN-Q 4)" 2>/dev/null \
  || echo "NOTE: QuickQuote main does not contain gate 5's A9 head 5d787d2 — the brief's STALE-BASE story for BCR2 and its §12/(a)/(b) corrections may be stale" >&2
q merge-base --is-ancestor '309e6c7e96e0f7694c597252849c8689f9b58e90' "$(fld MAIN-Q 4)" 2>/dev/null \
  || echo "NOTE: QuickQuote main does not contain gate 5's CF5R2 head 309e6c7 — the brief's account of what merged after gate 5 may be stale" >&2
q show "$(fld MAIN-Q 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.33",' \
  || echo "NOTE: QuickQuote main is no longer at toolVersion 2.33 — the brief's version note for BCR2 may be stale" >&2

# 63 — lockfiles: neither target changes a dependency (each row's lockfile equals its base's).
for ID in $IN_IDS; do
  case "$ID" in IO1R2) LF='package-lock.json'; G=p ;; *) LF='stage3/package-lock.json'; G=q ;; esac
  W="$($G rev-parse "$(fld "$ID" 5):$LF" 2>/dev/null)"; GOT="$($G rev-parse "$(fld "$ID" 4):$LF" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOT" = "$W" ] || { echo "REFUSING: row $ID's lockfile is ${GOT:0:7}, its base's is ${W:0:7} — a dependency change the brief does not gate; re-brief" >&2; exit 63; }
done
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" && grep -qiE 'never npm audit|no .npm audit.|never .npm audit.' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; entry by entry; never npm audit)" >&2; exit 63; }
done

# 31 — the settled-decisions file and gate 5's report (the PRIOR ROUND) are on disk and named, with the harnesses the brief copies.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G5_REPORT" ] || { echo "REFUSING: gate 5's report is absent: $G5_REPORT — both targets are its round 2" >&2; exit 31; }
for S in sections/IO1.md sections/BC.md sections/CONVENTIONS.md; do
  [ -s "$G5_DIR/$S" ] || { echo "REFUSING: gate 5's $S is absent — the brief names it as the prior round / working method" >&2; exit 31; }
done
grep -qF "$G5_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 5's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }
for H in qa-run.py qa-chrome-egressblock.sh qa-chrome-lock.py qa-egress-monitor.py qa-egress-posctl.mjs qa-netlog-scan.py qa-floorcount.py \
         lockcmp.py lockwalk.py mktree-qq.sh mktree-portal.sh qa-mkdb.cjs qa-dbcheck.cjs qa-harness-floorctl.mjs \
         qa-harness-io1-edges.cjs qa-harness-io1-boot.cjs qa-harness-lead-io1-hang.cjs qa-io1-preload-fetchguard.cjs \
         qa-io1-preload-hidelayer.cjs IO1-count-async.py \
         qa-bc-preload.mjs qa-harness-bc-emailed.cjs qa-harness-bc-concurrent.mjs qa-lib-bc-stage3.cjs qa-lib-bc-png.cjs \
         BC-pdfcompare.sh BC-diag2.sh; do
  [ -s "$G5_DIR/evidence/$H" ] || { echo "REFUSING: gate 5's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done

# 39 — the floor instrument the brief names is on disk.
[ -s "$G5_FLOOR" ] || { echo "REFUSING: gate 5's floor instrument missing: $G5_FLOOR" >&2; exit 39; }
grep -qF "$G5_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G5_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'IO1R2 (I10-O1 round 2, portal async route errors) is TIER 1' \
         'BCR2 (bounded browser.close() round 2) is TIER 2, through-code' \
         'BOTH TARGETS ARE ROUND 2 of 2'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
for T in 'TARGET IO1R2 — I10-O1 async route errors ROUND 2 of 2 (TIER 1, portal)' \
         'TARGET BCR2 — bounded browser.close() ROUND 2 of 2 (TIER 2 through-code' \
         'a second NO-GO ships the parts that closed and tickets the rest'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
# 76 — the ROUND-2-of-2 cap rule, quoted, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'C-62' "$FL" && grep -qF 'A Major at round 2 of 2 is ticketed, not sent to Kam' "$FL" \
    && grep -qF 'a third round on that class' "$FL" || {
    echo "REFUSING: $FL does not carry Kam's round-2 cap rule verbatim (C-62; 'A Major at round 2 of 2 is ticketed, not sent to Kam'; a third round on that class needs Kam)" >&2; exit 76; }
done
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -q '@[A-Z_]*@' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries a placeholder — placeholders belong in the brief only" >&2; exit 14; }
grep -q 'appended the verified table' "$PROMPT_FILE" || { echo "REFUSING: prompt must tell the agent the verified PIN table is appended" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
# 20 (cont.) — the QUESTIONS route, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF '[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>' "$FL" && grep -qF '[Wednesday -> QA/Vision-gate6] ANSWER' "$FL" \
    && grep -qi 'proceed on the safest reading' "$FL" && grep -qi 'read it with your verdict key' "$FL" || {
    echo "REFUSING: $FL lacks the QUESTIONS route (QUESTION subject, the [Wednesday -> QA/Vision-gate6] ANSWER reply, safest reading, verdict key)" >&2; exit 20; }
done
# 70 — the safety-check line, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'If a response is cut off by a safety check, record it and continue with the next item' "$FL" \
    && grep -qF "authorised defensive QA of Datasec's own product on loopback" "$FL" || {
    echo "REFUSING: $FL lacks the safety-check line (record and continue; authorised defensive QA on loopback)" >&2; exit 70; }
done
WORDS="SEPARATELY%PER%TARGET STALE-BASE merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN S-1 bash POSITIVE%CONTROL \
I10-O1 handle_request next(err) 4-arg refuse-to-boot express%4.22.2 res.destroy writableEnded serverError pg_terminate_backend \
/api/feedback/summary IO1-F1 IO1-O2 IO1-O3 IO1-F2 FRESHLY%CREATED \
BC-F1 BC-F2 closeBrowser renderQuotePdf byte-unchanged 0%differing%pixels TimeoutNaNWarning chrome_crashpad_handler child-process \
test:print work-g6 vsp_qa_g6_ 992da21 f8dec9c a83140e aa89010 3bfbfa2 d4426f8 6f197ca CI"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q 'NOT IN THIS GATE:\*\* portal' "$BRIEF" || { echo "REFUSING: brief lacks the S-1-not-in-this-gate note" >&2; exit 19; }
grep -qi 'do not fail on' "$BRIEF" || { echo "REFUSING: brief lacks the report-only / ticketed items instruction (do not fail on)" >&2; exit 19; }
# 24 — neither app's literal server entry path in the prompt: this agent's argv would read as a server to any argv-grep counter.
if grep -q -E 'stage3/server\.js|server/index\.js' "$PROMPT_FILE"; then
  echo "REFUSING: the prompt contains a literal server entry path — this agent would read as a FOREIGN SERVER to an argv-grep floor check (RD-591 c.37901). Describe it; do not name it." >&2; exit 24
fi

# 53 — per-step DEADLINE, HEARTBEAT every 2 minutes, abort at 5 minutes silent, server killed in a finally.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'DEADLINE' "$FL" && grep -q 'HEARTBEAT' "$FL" && grep -q '2 minutes' "$FL" && grep -q '5 minutes' "$FL" && grep -q 'finally' "$FL" || {
    echo "REFUSING: $FL lacks the DEADLINE / HEARTBEAT rule (2 minutes, 5 minutes, finally)" >&2; exit 53; }
done
# 60 — a red arm counts only if the mutant still parses, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'node --check' "$FL" && grep -qi 'VOID' "$FL" || { echo "REFUSING: $FL lacks the parse-before-red rule (node --check; a non-parsing mutant is VOID)" >&2; exit 60; }
done
# 61 — the gate's trees are EXCLUSIVE to it, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'EXCLUSIVE' "$FL" && grep -q 'work-g6' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule (EXCLUSIVE, work-g6)" >&2; exit 61; }
done
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-6 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g6_' "$FL" && grep -q '<epoch>_test' "$FL" \
    && grep -q 'vsp_qa_g1_' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -q 'vsp_qa_g3_' "$FL" && grep -q 'vsp_qa_g4_' "$FL" \
    && grep -q 'vsp_qa_g5_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g6_ DBs ending _test and never vsp_qa_g1_..g5_, no jest lock)" >&2; exit 62; }
done
# 64 — production named as NEVER in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'NEVER the live' "$FL" && grep -q 'datasec-sales-portal.azurewebsites.net' "$FL" && grep -q 'datasec-sales-portal-rg' "$FL" \
    && grep -q 'hpas-quickquote' "$FL" || {
    echo "REFUSING: $FL does not name both live apps (datasec-sales-portal.azurewebsites.net / datasec-sales-portal-rg, hpas-quickquote) as NEVER" >&2; exit 64; }
done
# 69 — ntfy is never contacted, and the renderer's FX egress is blocked, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'ntfy.invalid' "$FL" && grep -qi 'never contact ntfy.sh' "$FL" && grep -q 'FX' "$FL" || {
    echo "REFUSING: $FL lacks the ntfy/FX egress rule (NEVER contact ntfy.sh, NTFY_SERVER=http://ntfy.invalid, block the renderer's FX calls)" >&2; exit 69; }
done
# 75 — the standing lines, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY' "$FL" && grep -qF 'PRIOR WORK' "$FL" && grep -qF 'OWN object dir' "$FL" \
    && grep -qF 'no writes in either repo' "$FL" && grep -qF 'start / mid / end' "$FL" && grep -qF 'NOT TESTED' "$FL" \
    && grep -qi 'no production' "$FL" || {
    echo "REFUSING: $FL lacks a standing line (controls fail independently; PRIOR WORK vs history; merge-tree from OWN object dirs; no writes in either repo; start / mid / end readings; NOT TESTED; no production)" >&2; exit 75; }
done

# 38 — the brief names every negative-control seat; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — the brief tells the gate to say so and use the others" >&2
done

# Advisory: the local Postgres not answering makes the portal runtime legs NOT RUN.
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — IO1R2's runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 7 8 9 18 22 73 74 57 63 31 39 10 17 12 76 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, commit count, gated anchors, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-44s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); commits, bases (incl. stale), counts (6 7 8); anchors — round-1 heads contained, asyncErrors.js unchanged (9); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: IO1R2 I10-O1 round 2 (73) BCR2 bounded close round 2 (74) main premises (57)"
  echo "  lockfiles per target (63); CLARIFICATIONS + gate-5 report + sections + harnesses (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); round-2 cap C-62 (76); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + QUESTIONS route (20); safety-check line (70); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); standing lines (75); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate6-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL E2E_CLEANUP_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING SESSION_SECRET HPAM_WORD \
      ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS QUOTE_RETENTION_DAYS APPROVALS_INBOX \
      NTFY_TOPIC NTFY_SERVER FEEDBACK_CRON REMINDER_CRON LEAD_BOT_API_KEY BOT_USER_ID WEBSITE_SITE_NAME COORDINATOR_SECRET \
      OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR PORT NODE_ENV
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$(cat "$PROMPT_FILE")

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "claude-opus-5-5[1m]" --fallback-model claude-opus-5 "$PROMPT"
