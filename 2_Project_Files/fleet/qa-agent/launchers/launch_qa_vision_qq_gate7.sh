#!/bin/bash
# launch_qa_vision_qq_gate7.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 7, 2026-09-23) on
# Datasec/Vision_Sales_Portal, TWO repos, TWO targets:
#   BCR3   QQ  fix/qq-bounded-browser-close-2026-09-23        TIER 2 through-code WITH ONE DECLARED TIER-1 TOUCH (lib/pdf.js closeBrowser)
#              ROUND 3 of the BC class; carries the forward merge 983f916, so its base IS QuickQuote main d4426f8 (NOT stale)
#   IO1F1  P   fix/portal-io1r2-f1-completed-response-2026-09-23  TIER 1; the fix for gate 6's ticketed IO1R2-F1; on portal main f95f625
# IO1R2 itself is FINISHED AND MERGED: portal main f95f625 is the merge of the gated 992da21. IO1F1 is ROUND 1 of the IO1R2-F1 class.
# Portal S-1 (fix/feedback-report-auth-2026-09-22 @ 89af8ba) is GO from gate 2 and NOT in this gate; the brief's §12 re-measures it.
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it carries no
# head of its own — refuses any placeholder, verifies every row against the object store and against origin by `git ls-remote` NOW,
# and appends the verified table to the agent's prompt. The only shas it carries are GATED ANCHORS (992da21 = gate 6's gated IO1R2 head,
# f8dec9c = gate 6's gated BCR2 head, 983f916 = the forward merge inside BCR3): facts about what gate 6 gated, not heads.
#
# AUTHORITY: Tuesday's rulings of 2026-09-23 06:28 and 06:34 AEST (daily note 0_Brain/daily_tuesday/2026-09-23.md) — the gate's
# setImmediate shape is WITHDRAWN (measured not to fix it), the end-marker is approved with the mount position asserted in a cell, the
# flag lives on res, cells red on BOTH 992da21 and the setImmediate shape, a mid-body fault still breaks, and arm (e) (a store callback
# that never returns) is MEASURED then bounded or named; for BCR3 the bound is a HANG GUARD not a latency assertion, the branch stays
# (the cap is NOT spent), lib/pdf.js's shipped default changes too, and BCR3 goes first. Batching is Kam's standing rule of 2026-09-18.
# Kam's cap rule is C-62; Tuesday ruled it NOT SPENT here. Merges after this gate are Tuesday's GO. Deploys HELD for Kam; live
# QuickQuote is v2.30 and waits on Kam's typed word.
#
# PATTERN: launch_qa_vision_qq_gate6.sh. CHANGES:
#   - exit 7: NEITHER row is expected stale this gate (BCR3 carries its own forward merge); a stale row still passes but prints a NOTE.
#   - exit 9: anchors — BCR3 contains f8dec9c AND 983f916, and 983f916's parents are exactly f8dec9c + d4426f8; portal main contains
#     992da21; IO1F1's server/asyncErrors.js blob EQUALS portal main's (this branch does not touch the I10-O1 patch); at BCR3's base
#     closeBrowser is referenced only by lib/pdf.js and the two test files; portal main wires I10's lastResortHandler.
#   - exit 22: exact file sets — IO1F1 6 files over main, BCR3 15 over main (BACKLOG.md and test/logo-inset.mjs are new vs gate 6's 13).
#   - exit 73 IO1F1, 74 BCR3: content guards keyed on the ACTUAL code at each pinned head (drafted 08:3x AEST). 73 pins markAppEnd, the
#     Symbol flag, the 30 s grace, the single app.use(markAppEnd), the mount-position cell, the arm-(e) cell and the archiver mid-body
#     cell, and REFUSES round 2's un-marked writableEnded destroy. 74 proves lib/pdf.js differs ONLY inside closeBrowser(), package.json
#     only in test scripts, and pins all four 30000s, the 6 s cell, the one-number cell, logo-inset's closeBounded and the QA_CLOSE_MS
#     fallback; it REFUSES a 5000 default.
#   - exit 57: premises on the MAIN rows (portal main wires lastResortHandler; express 4.22.2 + express-session 1.19.0; toolVersion 2.33
#     at BOTH main and BCR3 — advisory).
#   - exit 63: lockfiles — every row's lockfile equals its BASE's (neither target changes a dependency).
#   - exit 62: the Vision floor discipline with gate-7 database names (vsp_qa_g7_, the _test suffix; never g1..g6).
#   - exit 76: the cap — C-62 quoted in both files AND Tuesday's "THE CAP IS NOT SPENT" ruling.
#   - exit 77 (new): the PORTAL coordinator rulings, verbatim in both files (setImmediate WITHDRAWN; red on BOTH 992da21 and the
#     setImmediate shape; the flag never module scope; arm (e) = a store callback that NEVER RETURNS).
#   - exit 78 (new): the QUICKQUOTE coordinator rulings, verbatim in both files (the bound is a HANG GUARD not a latency assertion;
#     re-establish the no-production-caller claim rather than re-assert it, with gate 6's zero-calls JSON quoted; settle the
#     phone-layout contradiction).
#   - exit 20: the QUESTIONS route ('[Wednesday -> QA/Vision-gate7] ANSWER'); exit 70: the safety-check line.
#   - exit 31/39: gate 6's report, its sections (BCR2.md / IO1R2.md / CONVENTIONS.md), its harnesses and its floor instrument.
#   - exit 38: negative-control seats Vision builder 17056 (%53), Tuesday 3434 (%0), Tuesday 51683 (%52), NexusAI 8360 (%44).
#     Gate 6's controls 1613 and 40615 have BOTH exited.
#   - exit 75: the standing lines — controls fail independently, PRIOR WORK verified against history, merge-tree from the gate's OWN
#     object dirs, no writes in either repo, three head readings, NOT TESTED, no production — in both files.
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate7' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate7.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..78 a guard refused
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate7.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate7.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G6_DIR="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate6"
G6_REPORT="$G6_DIR/report.md"
G6_FLOOR="$G6_DIR/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate7/report.md"
NEG_SEATS='17056 3434 51683 8360'   # Vision builder (%53), Tuesday (%0), Tuesday (%52), NexusAI (%44) at drafting
# Gated anchors (not heads): what gate 6 gated, and the forward merge BCR3 carries.
ANCHOR_IO1R2='992da21aae9d08596cbd877fa3e95c7e636804d6'
ANCHOR_BCR2='f8dec9c6b9898e05182a15ee1a0babd591a442c4'
FWD_MERGE='983f9168b00f8858cd2e99634f46db1193e0970e'

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — gate 7: bounded browser.close round 3 (tier 2 with one declared tier-1 touch, QuickQuote) + IO1R2-F1 end-marker (tier 1, portal), heads as pinned at launch'

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
EXPECT_IDS='MAIN-P MAIN-Q IO1F1 BCR3'
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
[ "$(fld IO1F1 2)" = "portal" ]   || { echo "REFUSING: row IO1F1 must be the portal repo" >&2; exit 40; }
[ "$(fld BCR3 2)" = "quickquote" ] || { echo "REFUSING: row BCR3 must be the quickquote repo" >&2; exit 40; }
exp_branch() { case "$1" in
  IO1F1) echo fix/portal-io1r2-f1-completed-response-2026-09-23 ;; BCR3) echo fix/qq-bounded-browser-close-2026-09-23 ;; esac; }
for ID in IO1F1 BCR3; do
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS='IO1F1 BCR3'
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
    echo "NOTE: row $ID is a STALE-BASE row: base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7} and the merge-base; a forward merge is owed at merge time (§12). THE BRIEF EXPECTS NEITHER ROW TO BE STALE — §12 and correction (a) may be stale." >&2
  fi
  [ "$OK" = 1 ] || { echo "REFUSING: row $ID base ${BASE:0:7} is neither its repo's MAIN row nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7; }
  $G merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: row $ID base ${BASE:0:7} is not an ancestor of ${H:0:7}" >&2; exit 7; }
  [ "$($G merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(row $ID base, head) is not the base" >&2; exit 7; }
  $G merge-base --is-ancestor "$H" "$MAINH" 2>/dev/null \
    && { echo "REFUSING: row $ID is ALREADY ON MAIN (${H:0:7} is an ancestor of ${MAINH:0:7}) — the brief says neither target is on main; re-brief" >&2; exit 7; }
  GOTN="$($G rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: row $ID has $GOTN commits over its base, the table says $N" >&2; $G log --format='%h %s' "${BASE}..${H}" >&2; exit 8; }
done

# 9 — gated anchors and base premises.
q merge-base --is-ancestor "$ANCHOR_BCR2" "$(fld BCR3 4)" 2>/dev/null \
  || { echo "REFUSING: BCR3's head does not contain gate 6's gated head f8dec9c — not a round 3 of the BC class; re-brief" >&2; exit 9; }
q merge-base --is-ancestor "$FWD_MERGE" "$(fld BCR3 4)" 2>/dev/null \
  || { echo "REFUSING: BCR3's head does not contain the forward merge 983f916 — the brief's 'not stale' story is wrong; re-brief" >&2; exit 9; }
MP="$(q log -1 --format='%P' "$FWD_MERGE" 2>/dev/null)"
[ "$MP" = "$ANCHOR_BCR2 $(fld MAIN-Q 4)" ] \
  || { echo "REFUSING: 983f916's parents are '$MP', the brief says f8dec9c + QuickQuote main $(fld MAIN-Q 4) — re-brief" >&2; exit 9; }
p merge-base --is-ancestor "$ANCHOR_IO1R2" "$(fld MAIN-P 4)" 2>/dev/null \
  || { echo "REFUSING: portal main does not contain gate 6's gated IO1R2 head 992da21 — the brief's premise that IO1R2 is MERGED is stale" >&2; exit 9; }
p merge-base --is-ancestor "$ANCHOR_IO1R2" "$(fld IO1F1 4)" 2>/dev/null \
  || { echo "REFUSING: IO1F1's head does not contain 992da21 — it is not built on the merged IO1R2 work; re-brief" >&2; exit 9; }
[ -n "$(p rev-parse "$(fld MAIN-P 4):server/asyncErrors.js" 2>/dev/null)" ] \
  && [ "$(p rev-parse "$(fld MAIN-P 4):server/asyncErrors.js" 2>/dev/null)" = "$(p rev-parse "$(fld IO1F1 4):server/asyncErrors.js" 2>/dev/null)" ] \
  || { echo "REFUSING: IO1F1's server/asyncErrors.js differs from portal main's — the brief says this branch does not touch the I10-O1 patch; re-brief" >&2; exit 9; }
p show "$(fld IO1F1 5):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: IO1F1's base does not wire I10's lastResortHandler — the brief's premise is stale" >&2; exit 9; }
CALLERS="$(q grep -l 'closeBrowser' "$(fld BCR3 5)" -- stage3 2>/dev/null | sed "s#^$(fld BCR3 5):##" | grep -v '/node_modules/' | sort)"
[ "$CALLERS" = "$(sorted 'stage3/lib/pdf.js
stage3/test/fx-provenance.mjs
stage3/test/typed-rates.mjs')" ] || { echo "REFUSING: at BCR3's base closeBrowser is referenced outside the three files the brief names:" >&2; printf '%s\n' "$CALLERS" >&2; exit 9; }

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets.
FS_IO1F1='BACKLOG.md
server/errors.js
server/errors.test.js
server/index.js
test/db/async-faults.test.js
test/db/completed-response.test.js'
FS_BCR3='BACKLOG.md
stage3/lib/pdf.js
stage3/package.json
stage3/test/email-collector.mjs
stage3/test/fixtures/browser-file.mjs
stage3/test/fixtures/hang-close.cjs
stage3/test/fx-provenance.mjs
stage3/test/lib-close-shared.test.mjs
stage3/test/lib-close.mjs
stage3/test/lib-close.test.mjs
stage3/test/logo-inset.mjs
stage3/test/phone-layout.mjs
stage3/test/print-fit.mjs
stage3/test/typed-rates.mjs
stage3/test/xlsx-parity.mjs'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in IO1F1 BCR3; do
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done

# Content guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 73 — IO1F1 (the IO1R2-F1 end-marker): the marker, the Symbol flag, the grace, the single mount, the cells.
has IO1F1 server/errors.js "const APP_ENDED = Symbol('vision.appEnded');" \
  || { echo "REFUSING: IO1F1's errors.js has no Symbol-keyed APP_ENDED — Tuesday's condition 3 (the flag lives on res, never module scope) is not met the way the brief says; re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'function markAppEnd(req, res, next) {' \
  || { echo "REFUSING: IO1F1's errors.js defines no markAppEnd middleware — re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'const settings = { appEndGraceMs: 30000 };' \
  || { echo "REFUSING: IO1F1's errors.js has no 30 s appEndGraceMs — arm (e) is unbounded, or the shape changed; re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'if (!res[APP_ENDED]) return void res.destroy(err);' \
  || { echo "REFUSING: IO1F1's errors.js does not break a mid-body stream fault at once (Tuesday's condition 5); re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'const t = setTimeout(() => { if (!res.writableEnded) res.destroy(err); }, settings.appEndGraceMs);' \
  || { echo "REFUSING: IO1F1's errors.js has no grace timer — arm (e) is not bounded the way the brief says; re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'module.exports = { serverError, lastResortHandler, markAppEnd, APP_ENDED, settings };' \
  || { echo "REFUSING: IO1F1's errors.js exports are not the brief's — re-brief" >&2; exit 73; }
has IO1F1 server/errors.js 'if (!res.writableEnded) res.destroy(e instanceof Error ? e : new Error(String(e)));' \
  && { echo "REFUSING: IO1F1's errors.js still carries round 2's un-marked writableEnded destroy verbatim — IO1R2-F1 is not fixed" >&2; exit 73; }
has IO1F1 server/errors.js 'setImmediate' \
  && { echo "REFUSING: IO1F1's errors.js carries a setImmediate — that shape was MEASURED NOT TO FIX IT and is WITHDRAWN (Tuesday, 2026-09-23)" >&2; exit 73; }
has IO1F1 server/index.js "const { serverError, lastResortHandler, markAppEnd } = require('./errors');" \
  || { echo "REFUSING: IO1F1's app module does not import markAppEnd — re-brief" >&2; exit 73; }
MOUNTS="$(p show "$(fld IO1F1 4):server/index.js" 2>/dev/null | grep -cF 'app.use(markAppEnd);')"
[ "$MOUNTS" = "1" ] || { echo "REFUSING: IO1F1 mounts markAppEnd $MOUNTS times — Tuesday's condition 1 says ONCE" >&2; exit 73; }
p show "$(fld IO1F1 4):server/index.js" 2>/dev/null \
  | awk '/session\(/{s=NR} /app\.use\(markAppEnd\);/{m=NR} END{exit !(s>0 && m>s)}' \
  || { echo "REFUSING: IO1F1 does not mount markAppEnd AFTER the session middleware — Tuesday's condition 1" >&2; exit 73; }
has IO1F1 test/db/completed-response.test.js 'the end-marker is mounted IMMEDIATELY after the session middleware (before it, the fix is silently undone)' \
  || { echo "REFUSING: IO1F1 has no cell asserting the mount POSITION — Tuesday's condition 1 says it is asserted in a cell, not a comment; re-brief" >&2; exit 73; }
has IO1F1 test/db/completed-response.test.js "assert.equal(names[s + 1], 'markAppEnd'" \
  || { echo "REFUSING: IO1F1's position cell does not assert the layer that FOLLOWS session — re-brief" >&2; exit 73; }
has IO1F1 test/db/completed-response.test.js "'mounted once'" \
  || { echo "REFUSING: IO1F1's position cell does not assert the marker is mounted ONCE — re-brief" >&2; exit 73; }
has IO1F1 test/db/completed-response.test.js 'IO1R2-F1: signed in, the handler answers and THEN faults (release throws after COMMIT): the rep still gets the quote' \
  || { echo "REFUSING: IO1F1 has no cell on the REAL generate route — re-brief" >&2; exit 73; }
has IO1F1 server/errors.test.js 'IO1R2-F1 arm (e): a session store that NEVER answers: the faulted request still ends (after the grace), it does not hang' \
  || { echo "REFUSING: IO1F1 has no arm-(e) cell (a store callback that NEVER RETURNS) — the ruling Kam most wanted measured; re-brief" >&2; exit 73; }
for S in 'guard: a response that started but the app never ended (a stream faulted mid-body) is broken at once' \
         'guard: a response that has already finished is left alone (the writableEnded check)' \
         'guard: the app ended its answer and it finishes within the grace: never broken (the marker check)' \
         'guard: the app ended its answer but it never finishes: broken once the grace runs out'; do
  has IO1F1 server/errors.test.js "$S" || { echo "REFUSING: IO1F1's unit suite lacks the guard cell: $S — re-brief" >&2; exit 73; }
done
has IO1F1 test/db/async-faults.test.js 'QA: archive failed mid-stream' \
  || { echo "REFUSING: IO1F1's backup-route cell does not fault the ARCHIVE mid-body — gate 6's IO1R2-P1 is unfixed; re-brief" >&2; exit 73; }
has IO1F1 test/db/async-faults.test.js 'assert.match(r.status, /socket hang up|ECONNRESET|aborted/' \
  || { echo "REFUSING: IO1F1's backup-route cell still passes on a hang (gate 6 IO1R2-P1) — re-brief" >&2; exit 73; }
# 74 — BCR3 (bounded close round 3): lib/pdf.js may change ONLY inside closeBrowser(); package.json only in test scripts.
python3 - "$(q show "$(fld BCR3 5):stage3/lib/pdf.js" 2>/dev/null)" "$(q show "$(fld BCR3 4):stage3/lib/pdf.js" 2>/dev/null)" <<'PY' || { echo "REFUSING: BCR3 changes stage3/lib/pdf.js OUTSIDE closeBrowser() (renderQuotePdf / the launch / exports / a new helper) — the brief gates a closeBrowser-only change; re-brief" >&2; exit 74; }
import sys
def strip(s):
    # the function takes parameters (closeBrowser(ms = 30000)) and its leading /* For tests ... */ comment belongs to it
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
PJ="$(q diff "$(fld BCR3 5)" "$(fld BCR3 4)" 2>/dev/null -- stage3/package.json | grep -E '^[+-]' | grep -v '^[+-][+-]')"
BADPJ="$(printf '%s\n' "$PJ" | grep -vE '^[+-]    "test(:[a-z]+)?": ')"
[ -z "$BADPJ" ] || { echo "REFUSING: BCR3's stage3/package.json delta is not test scripts only:" >&2; printf '%s\n' "$BADPJ" >&2; exit 74; }
has BCR3 stage3/lib/pdf.js 'async function closeBrowser(ms = 30000) {' \
  || { echo "REFUSING: BCR3's SHIPPED lib/pdf.js closeBrowser default is not 30000 — the declared tier-1 touch is not what the brief gates; re-brief" >&2; exit 74; }
has BCR3 stage3/lib/pdf.js 'async function closeBrowser(ms = 5000) {' \
  && { echo "REFUSING: BCR3's lib/pdf.js still carries the 5000 ms default" >&2; exit 74; }
has BCR3 stage3/test/lib-close.mjs 'export async function closeBounded(browser, ms = 30000) {' \
  || { echo "REFUSING: BCR3's test helper default is not 30000 — the bound did not move in BOTH modules; re-brief" >&2; exit 74; }
for F in stage3/lib/pdf.js stage3/test/lib-close.mjs; do
  has BCR3 "$F" 'const limit = Number.isFinite(Number(ms)) && Number(ms) > 0 ? Number(ms) : 30000;' \
    || { echo "REFUSING: BCR3's $F NaN-proof fallback is not 30000 — the bound is FOUR numbers and one of them did not move; re-brief" >&2; exit 74; }
  has BCR3 "$F" 'for (const s of child.stdio || [])' \
    || { echo "REFUSING: BCR3's $F lost the stdio-release loop (the BC-F1 fix gate 6 gated) — re-brief" >&2; exit 74; }
done
has BCR3 stage3/lib/pdf.js '30 s is a HANG guard, not a speed check' \
  || { echo "REFUSING: BCR3's lib/pdf.js does not record the bound as a HANG GUARD, not a latency assertion (Tuesday's ruling) — re-brief" >&2; exit 74; }
has BCR3 stage3/test/lib-close.test.mjs 'a SLOW but healthy close (6 s, slower than the old 5 s bound) is not killed: the default is a hang guard' \
  || { echo "REFUSING: BCR3 has no cell proving a healthy close slower than the OLD bound survives — the defect round 3 exists for is unguarded; re-brief" >&2; exit 74; }
has BCR3 stage3/test/lib-close.test.mjs 'the default bound is ONE number, in the test helper and in the shipped lib/pdf.js alike' \
  || { echo "REFUSING: BCR3 has no cell tying the two modules' defaults together — re-brief" >&2; exit 74; }
has BCR3 stage3/test/lib-close.test.mjs 'assert.deepEqual(all, [30000, 30000, 30000, 30000]' \
  || { echo "REFUSING: BCR3's one-number cell does not assert all FOUR 30000s — re-brief" >&2; exit 74; }
has BCR3 stage3/test/logo-inset.mjs 'import { closeBounded } from "./lib-close.mjs";' \
  || { echo "REFUSING: BCR3's logo-inset.mjs (A9's file, new to this set) does not import closeBounded — re-brief" >&2; exit 74; }
has BCR3 stage3/test/logo-inset.mjs 'after(async () => { await closeBounded(browser); });' \
  || { echo "REFUSING: BCR3's logo-inset.mjs close is still unbounded — round 3's first reason does not hold; re-brief" >&2; exit 74; }
has BCR3 stage3/test/fixtures/browser-file.mjs 'Number(process.env.QA_CLOSE_MS) || undefined' \
  || { echo "REFUSING: BCR3's browser-file fixture does not fall back to the module default — the brief's QA_CLOSE_MS warning is stale; re-brief" >&2; exit 74; }
for S in 'test/logo-inset.mjs' 'test/lib-close.test.mjs' 'test/lib-close-shared.test.mjs'; do
  has BCR3 stage3/package.json "$S" || { echo "REFUSING: BCR3's test:print line does not run $S — the merged eight-file line the brief counts is wrong" >&2; exit 74; }
done
for F in stage3/test/fixtures/browser-file.mjs stage3/test/fixtures/hang-close.cjs; do
  [ -n "$(q rev-parse "$(fld BCR3 4):$F" 2>/dev/null)" ] || { echo "REFUSING: BCR3 lacks the child-process cell's fixture $F — re-brief" >&2; exit 74; }
done
# 57 — premises on the MAIN rows.
p show "$(fld MAIN-P 4):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: portal main does not wire lastResortHandler — IO1F1's premise is stale" >&2; exit 57; }
python3 - "$(p show "$(fld IO1F1 4):package-lock.json" 2>/dev/null)" <<'PY' || { echo "REFUSING: IO1F1's lockfile does not resolve express 4.22.2 AND express-session 1.19.0 — the brief names both" >&2; exit 57; }
import sys, json
b = json.loads(sys.argv[1])["packages"]
ok = (b.get("node_modules/express", {}).get("version") == "4.22.2"
      and b.get("node_modules/express-session", {}).get("version") == "1.19.0")
sys.exit(0 if ok else 1)
PY
q show "$(fld MAIN-Q 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.33",' \
  || echo "NOTE: QuickQuote main is no longer at toolVersion 2.33 — the brief's version note may be stale" >&2
q show "$(fld BCR3 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.33",' \
  || echo "NOTE: BCR3 is no longer at toolVersion 2.33 — the brief says main and BCR3 carry the SAME version" >&2

# 63 — lockfiles: neither target changes a dependency (each row's lockfile equals its base's).
for ID in $IN_IDS; do
  case "$ID" in IO1F1) LF='package-lock.json'; G=p ;; *) LF='stage3/package-lock.json'; G=q ;; esac
  W="$($G rev-parse "$(fld "$ID" 5):$LF" 2>/dev/null)"; GOT="$($G rev-parse "$(fld "$ID" 4):$LF" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOT" = "$W" ] || { echo "REFUSING: row $ID's lockfile is ${GOT:0:7}, its base's is ${W:0:7} — a dependency change the brief does not gate; re-brief" >&2; exit 63; }
done
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" && grep -qiE 'never npm audit|no .npm audit.|never .npm audit.' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; entry by entry; never npm audit)" >&2; exit 63; }
done

# 31 — the settled-decisions file and gate 6's report (the PRIOR ROUND) are on disk and named, with the harnesses the brief copies.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G6_REPORT" ] || { echo "REFUSING: gate 6's report is absent: $G6_REPORT — it is the PRIOR ROUND for both targets" >&2; exit 31; }
for S in sections/BCR2.md sections/IO1R2.md sections/CONVENTIONS.md; do
  [ -s "$G6_DIR/$S" ] || { echo "REFUSING: gate 6's $S is absent — the brief names it as the prior round / working method" >&2; exit 31; }
done
grep -qF "$G6_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 6's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }
for H in qa-run.py qa-chrome-egressblock.sh qa-chrome-lock.py qa-egress-monitor.py qa-egress-posctl.mjs qa-netlog-scan.py qa-floorcount.py \
         lockcmp.py lockwalk.py mktree-qq.sh mktree-portal.sh qa-mkdb.cjs qa-dbcheck.cjs qa-harness-floorctl.mjs \
         qa-harness-io1-edges.cjs qa-harness-io1-boot.cjs qa-harness-lead-io1-hang.cjs qa-io1-preload-fetchguard.cjs \
         qa-io1-preload-hidelayer.cjs IO1-count-async.py \
         qa-bc-preload.mjs qa-harness-bc-emailed.cjs qa-harness-bc-concurrent.mjs qa-lib-bc-stage3.cjs qa-lib-bc-png.cjs \
         BC-pdfcompare.sh BC-diag2.sh; do
  [ -s "$G6_DIR/evidence/$H" ] || { echo "REFUSING: gate 6's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done
# 31 (cont.) — the 5,018 ms evidence file the brief sets against the builder's claim must be readable, or the contradiction is unsourced.
grep -rqF 'real close() returned after 5018ms' "$G6_DIR/evidence" 2>/dev/null \
  || { echo "REFUSING: gate 6's 5,018 ms observation is not in its evidence — the brief's correction (e) has no source; re-brief" >&2; exit 31; }

# 39 — the floor instrument the brief names is on disk.
[ -s "$G6_FLOOR" ] || { echo "REFUSING: gate 6's floor instrument missing: $G6_FLOOR" >&2; exit 39; }
grep -qF "$G6_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G6_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'IO1F1 (IO1R2-F1 end-marker, portal completed-response) is TIER 1' \
         'BCR3 (bounded browser.close() round 3) is TIER 2, through-code, WITH ONE DECLARED TIER-1 TOUCH' \
         'NEITHER TARGET IS ON MAIN'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
for T in 'TARGET IO1F1 — IO1R2-F1 the end-marker (TIER 1, portal)' \
         'TARGET BCR3 — bounded browser.close() ROUND 3 (TIER 2 with ONE DECLARED TIER-1 TOUCH: lib/pdf.js closeBrowser, QuickQuote)' \
         'a third round on that class would need Kam'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
# 76 — the cap: C-62 verbatim AND Tuesday's ruling that it is NOT spent, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'C-62' "$FL" && grep -qF 'A Major at round 2 of 2 is ticketed, not sent to Kam' "$FL" \
    && grep -qF 'a third round on that class' "$FL" && grep -qF 'THE CAP IS NOT SPENT' "$FL" || {
    echo "REFUSING: $FL does not carry Kam's cap rule verbatim (C-62; 'A Major at round 2 of 2 is ticketed, not sent to Kam'; a third round on that class) AND Tuesday's ruling that THE CAP IS NOT SPENT" >&2; exit 76; }
done
# 77 — the PORTAL coordinator rulings, verbatim, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'MEASURED NOT TO FIX IT and is WITHDRAWN' "$FL" \
    && grep -qF 'RED on BOTH 992da21 AND on the setImmediate shape' "$FL" \
    && grep -qF 'never module scope' "$FL" \
    && grep -qF 'a store callback that NEVER RETURNS' "$FL" \
    && grep -qF '61-of-62-byte' "$FL" || {
    echo "REFUSING: $FL lacks a PORTAL coordinator ruling verbatim (setImmediate MEASURED NOT TO FIX IT and is WITHDRAWN; cells RED on BOTH 992da21 AND on the setImmediate shape; the flag never module scope; arm (e) = a store callback that NEVER RETURNS; the truncated 61-of-62-byte body)" >&2; exit 77; }
done
# 78 — the QUICKQUOTE coordinator rulings, verbatim, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'bound is a HANG GUARD, not a latency assertion' "$FL" \
    && grep -qF 'establish it, do not re-assert it' "$FL" \
    && grep -qF '{"closeBrowser":0' "$FL" \
    && grep -qF 'The gate must settle that' "$FL" \
    && grep -qF '5,018 ms' "$FL" || {
    echo "REFUSING: $FL lacks a QUICKQUOTE coordinator ruling verbatim (the bound is a HANG GUARD, not a latency assertion; re-establish it, do not re-assert it; gate 6's {\"closeBrowser\":0 ...} firing-spy result; the 5,018 ms contradiction the gate must settle)" >&2; exit 78; }
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
  grep -qF '[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>' "$FL" && grep -qF '[Wednesday -> QA/Vision-gate7] ANSWER' "$FL" \
    && grep -qi 'proceed on the safest reading' "$FL" && grep -qi 'read it with your verdict key' "$FL" || {
    echo "REFUSING: $FL lacks the QUESTIONS route (QUESTION subject, the [Wednesday -> QA/Vision-gate7] ANSWER reply, safest reading, verdict key)" >&2; exit 20; }
done
# 70 — the safety-check line, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'If a response is cut off by a safety check, record it and continue with the next item' "$FL" \
    && grep -qF "authorised defensive QA of Datasec's own product on loopback" "$FL" || {
    echo "REFUSING: $FL lacks the safety-check line (record and continue; authorised defensive QA on loopback)" >&2; exit 70; }
done
WORDS="SEPARATELY%PER%TARGET merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN S-1 bash positive%control \
markAppEnd APP_ENDED setImmediate WITHDRAWN writableEnded express-session arm%(e) 30,000%ms \
closeBrowser renderQuotePdf logo-inset phone-layout 2,032%ms 1,680%ms TimeoutNaNWarning QA_CLOSE_MS test:print \
byte-unchanged 0%differing%pixels load%average work-g7 vsp_qa_g7_ 992da21 15cd733 58c9094 983f916 f8dec9c d4426f8 f95f625 CI"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q 'NOT IN THIS GATE:\*\* portal' "$BRIEF" || { echo "REFUSING: brief lacks the S-1-not-in-this-gate note" >&2; exit 19; }
grep -qi 'do not fail on' "$BRIEF" || { echo "REFUSING: brief lacks the report-only / ticketed items instruction (do not fail on)" >&2; exit 19; }
grep -qF 'v2.30' "$BRIEF" && grep -qF 'v2.30' "$PROMPT_FILE" || { echo "REFUSING: both files must say that live QuickQuote is v2.30 and waits on Kam's typed word" >&2; exit 19; }
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
  grep -q 'EXCLUSIVE' "$FL" && grep -q 'work-g7' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule (EXCLUSIVE, work-g7)" >&2; exit 61; }
done
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-7 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g7_' "$FL" && grep -q '<epoch>_test' "$FL" \
    && grep -q 'vsp_qa_g1_' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -q 'vsp_qa_g3_' "$FL" && grep -q 'vsp_qa_g4_' "$FL" \
    && grep -q 'vsp_qa_g5_' "$FL" && grep -q 'vsp_qa_g6_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g7_ DBs ending _test and never vsp_qa_g1_..g6_, no jest lock)" >&2; exit 62; }
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
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — IO1F1's runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 6 7 8 9 18 22 73 74 57 63 31 39 10 17 12 76 77 78 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, not-already-on-main, commit count, gated anchors, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '{ printf "  %-7s %-11s %-52s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}")"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); commits, bases (incl. stale), not-on-main, counts (6 7 8); anchors — f8dec9c + 983f916 in BCR3 with its parents checked, 992da21 on portal main and in IO1F1, asyncErrors.js unchanged (9); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: IO1F1 the end-marker (73) BCR3 bounded close round 3 (74) main premises (57)"
  echo "  lockfiles per target (63); CLARIFICATIONS + gate-6 report + sections + harnesses + the 5,018 ms evidence (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); cap C-62 NOT SPENT (76); portal rulings (77); quickquote rulings (78); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + QUESTIONS route (20); safety-check line (70); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); standing lines (75); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate7-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
      OTP_IP_BUDGET_PER_HOUR OTP_GLOBAL_BUDGET_PER_HOUR PORT NODE_ENV QA_CLOSE_MS
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

PROMPT="$(cat "$PROMPT_FILE")

$PIN_BLOCK"
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
