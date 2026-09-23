#!/bin/bash
# launch_qa_vision_qq_gate4.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 4, 2026-09-22) on
# Datasec/Vision_Sales_Portal, TWO repos, SIX targets + slot FU:
#   N    QQ  fix/qq-phone-overflow-2026-09-22            TIER 2 customer-visible (A-6 ROUND 2 of 2; on main 763269d via c1abc05)
#   CF5  QQ  fix/qq-otp-refund-provider-only-2026-09-22  TIER 1  (C-F5 + C2-F2; on main 763269d)
#   I9   QQ  fix/qq-error-log-no-body-2026-09-22         TIER 1  (item 9; STALE base 51e9286)
#   I10  P   fix/portal-413-passthrough-2026-09-22       TIER 2  (item 10; STALE base f065675)
#   Q5   QQ  fix/qq-qs-advisory-2026-09-22               TIER 2  (item 5, lockfile only; STALE base 51e9286)
#   P5B  QQ  fix/qq-puppeteer-25-2026-09-22              TIER 2  (item 5b, PRODUCTION RUNTIME, Kam's decision 14; STALE 51e9286)
#   FU   QQ  fix/qq-gate3-followups-2026-09-22           TIER 2  (SLOT; K-F1 + L-F1 + M-N2 + K-O1, tests only; on main 763269d)
# Portal S-1 (fix/feedback-report-auth-2026-09-22 @ 89af8ba) is GO from gate 2 and NOT in this gate (waits on Kam's card).
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it
# carries no head of its own — refuses any placeholder, verifies every row against the object store and against origin by
# `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are GATED ANCHORS and
# BUILDER BASE COMMITS (ac0a8d2 / c1abc05 for N; 320a169 / 103340c for Q5; 3d0167e / 0d45100 for P5B; 51e9286 = the old main
# Q5/P5B merged) and the two dependency lockfile blobs: facts about what was gated or built, not heads.
#
# AUTHORITY: READY mails from the Vision_Sales_Portal agent (item 9 11:41Z, item 10 11:46Z, item 11 = items 5/5b 11:58Z,
# C-F5 12:35Z, N round 2 12:48Z, gate-3 follow-ups 12:52Z) and Tuesday's commission (~22:50) and slot-FU message (~22:53).
# Tuesday's C-F5 ruling (22:37). Batching is Kam's standing rule of 2026-09-18. Merges after this gate are Tuesday's GO.
# Deploys HELD for Kam; P5B additionally waits on Kam's decision 14.
#
# PATTERN: launch_qa_vision_qq_gate3.sh. CHANGES:
#   - exit 40: the PIN table (9 rows: MAIN-P MAIN-Q N CF5 I9 I10 Q5 P5B FU); only FU may be OUT.
#   - exit 41: the SLOT-FU line vs row FU vs the brief's SLOT-FU sections vs the prompt's [SLOT-FU BEGIN] block. Markers are
#     matched at LINE START, so the brief's own instruction line that names them cannot count as a section (gate 3's latent bug).
#   - exit 7: base is MAIN, OR another IN row's head, OR a STALE BASE (NOTE); I9/I10/Q5/P5B are expected stale, N/CF5/FU not.
#   - exit 9: anchors — N contains ac0a8d2 and c1abc05 = merge(ac0a8d2, 763269d-row); CF5's base carries gate 3's gated C-F3
#     refund line; Q5 = merge(320a169, 51e9286); P5B = merge(3d0167e, 51e9286); FU's package.json delta is one test:print line.
#   - exit 22: per-target exact file sets over their bases.
#   - exit 57, 58, 65-68, 71: per-target content guards keyed on the ACTUAL code at each pinned head (drafted 22:5x-23:1x).
#   - exit 63: lockfiles — N/CF5/I9/FU equal the QQ MAIN row's lockfile; I10 equals portal MAIN's; Q5 and P5B equal their pinned
#     blobs, Q5 = exactly 3 version bumps vs its base, P5B = puppeteer-core 25.0.2 and no extract-zip.
#   - exit 62: the Vision floor discipline with gate-4 database names (vsp_qa_g4_, the _test suffix; never g1/g2/g3).
#   - exit 20: the QUESTIONS route (tuesday-agent@, the QUESTION subject, the '[Wednesday -> QA/Vision-gate4] ANSWER' reply).
#   - exit 70 (new): the safety-check line (record and continue; authorised defensive QA on loopback), in both files.
#   - exit 31/39: gate 3's report, its harnesses and its Vision floor instrument are on disk and named.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 45678 (%0), NexusAI 8360 (%44).
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate4' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate4.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..71 a guard refused
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
PH_SLOTFU='@SLOT''_FU@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate4.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate4.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G3_DIR="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate3"
G3_REPORT="$G3_DIR/report.md"
G3_FLOOR="$G3_DIR/evidence/qa-floorcount.py"
N_SHOTS="$VSP/5_Project_History/a6-phone-layout-2026-09-22-r2-2246"
REPORT="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate4/report.md"
NEG_SEATS='1613 45678 8360'   # Vision builder (%41), Tuesday (%0), NexusAI (%44) at drafting
# Gated anchors / builder base commits (not heads).
ANCHOR_N='ac0a8d2536a8b991c51546e7f482df10ce0a5eb1'
FWD_N='c1abc05'
OLD_MAIN_Q='51e92867930efd4c98b28dc5d95baf82219b3edb'
Q5_ORIG='320a1698603015c4b07d71ba055a4201076af094'
Q5_MERGE='103340c'
P5B_ORIG='3d0167ebe1909a301ac881c30f55f717c7801dd3'
P5B_MERGE='0d45100'
Q5_LOCK='70ebda71097d6046f385ca7fdf3eee5d7e6cbd36'
P5B_LOCK='cdd7699dd7510c5592461a9d3c96fcd4cdc8195e'

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 4: C-F5 + item 9 (tier 1) + A-6 round 2 + item 10 + qs advisory + puppeteer 25 + gate-3 follow-ups (tier 2), heads as pinned at launch'

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
EXPECT_IDS='MAIN-P MAIN-Q N CF5 I9 I10 Q5 P5B FU'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "9" ] || { echo "REFUSING: PIN table carries rows beyond the nine expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  case "$ST" in IN|OUT) ;; *) echo "REFUSING: PIN row $ID status is '$ST' (IN or OUT only; unfilled?)" >&2; exit 40 ;; esac
  case "$ID" in FU) ;; *) [ "$ST" = "IN" ] || { echo "REFUSING: only row FU may be OUT (row $ID is $ST)" >&2; exit 40; } ;; esac
  if [ "$ST" = "IN" ]; then
    printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN row $ID still carries a placeholder: $R" >&2; exit 40; }
    is40 "$(fld "$ID" 4)" || { echo "REFUSING: PIN row $ID head is not a 40-hex sha: '$(fld "$ID" 4)'" >&2; exit 40; }
    case "$ID" in
      MAIN-*) [ "$(fld "$ID" 3)" = "main" ] || { echo "REFUSING: row $ID branch must be main" >&2; exit 40; } ;;
      *) is40 "$(fld "$ID" 5)" || { echo "REFUSING: PIN row $ID base is not a 40-hex sha" >&2; exit 40; }
         printf '%s' "$(fld "$ID" 6)" | grep -Eq '^[1-9][0-9]*$' || { echo "REFUSING: PIN row $ID commits is not a positive integer" >&2; exit 40; } ;;
    esac
    [ "$(repo_fn "$(fld "$ID" 2)")" != "x" ] || { echo "REFUSING: PIN row $ID repo must be portal or quickquote" >&2; exit 40; }
  fi
done
[ "$(fld MAIN-P 2)" = "portal" ] && [ "$(fld MAIN-Q 2)" = "quickquote" ] || { echo "REFUSING: MAIN-P must be portal, MAIN-Q quickquote" >&2; exit 40; }
[ "$(fld I10 2)" = "portal" ] || { echo "REFUSING: row I10 must be the portal repo" >&2; exit 40; }
for ID in N CF5 I9 Q5 P5B FU; do [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: row $ID must be the quickquote repo" >&2; exit 40; }; done
exp_branch() { case "$1" in
  N) echo fix/qq-phone-overflow-2026-09-22 ;; CF5) echo fix/qq-otp-refund-provider-only-2026-09-22 ;;
  I9) echo fix/qq-error-log-no-body-2026-09-22 ;; I10) echo fix/portal-413-passthrough-2026-09-22 ;;
  Q5) echo fix/qq-qs-advisory-2026-09-22 ;; P5B) echo fix/qq-puppeteer-25-2026-09-22 ;;
  FU) echo fix/qq-gate3-followups-2026-09-22 ;; esac; }
for ID in N CF5 I9 I10 Q5 P5B FU; do
  [ "$(fld "$ID" 7)" = "IN" ] || continue
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS="$(printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" && $1!~/^MAIN-/ {print $1}' | tr '\n' ' ')"
isin() { case " $IN_IDS " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# 41 — slot FU: the SLOT line, the row, the brief's SLOT sections and the prompt's block must agree. Line-start markers only.
SV="$(grep -m1 '^SLOT-FU: ' "$BRIEF" | sed 's/^SLOT-FU: //')"
[ -n "$SV" ] || { echo "REFUSING: the brief has no 'SLOT-FU: ' line" >&2; exit 41; }
[ "$SV" != "$PH_SLOTFU" ] || { echo "REFUSING: SLOT-FU is unfilled — Tuesday sets IN or OUT" >&2; exit 41; }
case "$SV" in IN|OUT) ;; *) echo "REFUSING: SLOT-FU line is '$SV' (IN or OUT only)" >&2; exit 41 ;; esac
[ "$SV" = "$(fld FU 7)" ] || { echo "REFUSING: SLOT-FU says $SV but PIN row FU is $(fld FU 7)" >&2; exit 41; }
NB="$(grep -c '^<!-- SLOT-FU:BEGIN -->' "$BRIEF")"; NE="$(grep -c '^<!-- SLOT-FU:END -->' "$BRIEF")"
HASP=0; grep -q '^\[SLOT-FU BEGIN\]' "$PROMPT_FILE" && grep -q '^\[SLOT-FU END\]' "$PROMPT_FILE" && HASP=1
if [ "$SV" = "IN" ]; then
  [ "$NB" = "2" ] && [ "$NE" = "2" ] && [ "$HASP" = "1" ] || { echo "REFUSING: SLOT-FU is IN but the brief's two SLOT-FU sections ($NB/$NE markers) or the prompt block ($HASP) are missing" >&2; exit 41; }
else
  [ "$NB$NE$HASP" = "000" ] || { echo "REFUSING: SLOT-FU is OUT but a brief SLOT-FU section ($NB/$NE) or the prompt block ($HASP) is still present — delete them" >&2; exit 41; }
fi
SLOT_FU="$SV"
grep -q '<fill at launch>' "$BRIEF" && { echo "REFUSING: the brief still carries a '<fill at launch>' marker" >&2; exit 41; }

# 6 / 7 / 8 — per IN row: commit in its repo; base ancestor AND merge-base; exact commit count; base is MAIN, a named IN head,
# or a STALE BASE (an ancestor of MAIN equal to merge-base(head, MAIN)).
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
  for O in $IN_IDS; do [ "$O" != "$ID" ] && [ "$(fld "$O" 2)" = "$REPO" ] && [ "$(fld "$O" 4)" = "$BASE" ] && OK=1; done
  if [ "$OK" = 0 ] && $G merge-base --is-ancestor "$BASE" "$MAINH" 2>/dev/null \
     && [ "$($G merge-base "$H" "$MAINH" 2>/dev/null)" = "$BASE" ]; then
    OK=1; STALE="$STALE $ID"
    echo "NOTE: row $ID is a STALE-BASE row: base ${BASE:0:7} is an ancestor of MAIN ${MAINH:0:7} and the merge-base; a forward merge is owed at merge time (§12)" >&2
  fi
  [ "$OK" = 1 ] || { echo "REFUSING: row $ID base ${BASE:0:7} is neither its repo's MAIN row, another IN row's head, nor merge-base(head, MAIN) on MAIN — re-pin" >&2; exit 7; }
  $G merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: row $ID base ${BASE:0:7} is not an ancestor of ${H:0:7}" >&2; exit 7; }
  [ "$($G merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(row $ID base, head) is not the base" >&2; exit 7; }
  GOTN="$($G rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: row $ID has $GOTN commits over its base, the table says $N" >&2; $G log --format='%h %s' "${BASE}..${H}" >&2; exit 8; }
done
for ID in I9 I10 Q5 P5B; do isin "$ID" || continue
  case " $STALE " in *" $ID "*) ;; *) echo "NOTE: row $ID was expected to be STALE-BASE (brief §PIN shape) and is not — the brief's §12 predictions for it may be stale" >&2 ;; esac
done
for ID in N CF5 FU; do isin "$ID" || continue
  case " $STALE " in *" $ID "*) echo "NOTE: row $ID was expected to sit on the MAIN row and is STALE-BASE — main moved; the brief's §12 predictions for it may be stale" >&2 ;; esac
done

# 9 — gated anchors and builder base commits.
q merge-base --is-ancestor "$ANCHOR_N" "$(fld N 4)" 2>/dev/null || { echo "REFUSING: N's head does not contain the gated round-1 head ac0a8d2 — not a round 2; re-brief" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$FWD_N" 2>/dev/null)" = "$ANCHOR_N $(fld MAIN-Q 4)" ] \
  || { echo "REFUSING: N's forward merge $FWD_N does not have parents ac0a8d2 + the MAIN-Q row as the brief says" >&2; exit 9; }
q merge-base --is-ancestor "$FWD_N" "$(fld N 4)" 2>/dev/null || { echo "REFUSING: N's head does not contain its forward merge $FWD_N" >&2; exit 9; }
q show "$(fld CF5 5):stage3/server.js" 2>/dev/null | grep -qF 'const refundHits = () => { ipBudget.refund(src, now); globalBudget.refund("*", now); };' \
  || { echo "REFUSING: CF5's base does not carry gate 3's gated C-F3 refund line — the brief's before/after is stale" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$Q5_MERGE" 2>/dev/null)" = "$Q5_ORIG $OLD_MAIN_Q" ] && q merge-base --is-ancestor "$Q5_MERGE" "$(fld Q5 4)" 2>/dev/null \
  || { echo "REFUSING: Q5's head is not (or does not contain) the merge of 320a169 + 51e9286 the brief describes" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$P5B_MERGE" 2>/dev/null)" = "$P5B_ORIG $OLD_MAIN_Q" ] && q merge-base --is-ancestor "$P5B_MERGE" "$(fld P5B 4)" 2>/dev/null \
  || { echo "REFUSING: P5B's head is not (or does not contain) the merge of 3d0167e + 51e9286 the brief describes" >&2; exit 9; }
if isin FU; then
  PJ="$(q diff "$(fld FU 5)" "$(fld FU 4)" -- stage3/package.json 2>/dev/null | grep -E '^[+-]' | grep -v '^[+-][+-]')"
  [ "$(printf '%s\n' "$PJ" | wc -l | tr -d ' ')" = "2" ] && printf '%s\n' "$PJ" | grep -q '^-    "test:print": ' \
    && printf '%s\n' "$PJ" | grep -q '^+    "test:print": .*test/email-collector\.mjs",$' \
    || { echo "REFUSING: FU's stage3/package.json delta is not exactly the one test:print line — FU is not tests-only; re-brief" >&2; printf '%s\n' "$PJ" >&2; exit 9; }
fi

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets.
FS_N='BACKLOG.md
index.html
stage3/package.json
stage3/test/phone-layout.mjs'
FS_CF5='BACKLOG.md
stage3/lib/mail.js
stage3/lib/sendFailure.js
stage3/server.js
stage3/test/mail.test.mjs
stage3/test/server.test.mjs'
FS_I9='stage3/server.js
stage3/test/server.test.mjs'
FS_I10='server/errors.js
server/errors.test.js
server/index.js
test/db/routes.test.js'
FS_Q5='stage3/package-lock.json'
FS_P5B='stage3/Dockerfile
stage3/package-lock.json
stage3/package.json'
FS_FU='stage3/package.json
stage3/test/email-collector.mjs
stage3/test/server.test.mjs'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in $IN_IDS; do
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done

# Content guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 68 — N (A-6 round 2)
for S in 'toolVersion: "2.32",' '@media screen and (max-width: 600px) {' '@media screen and (max-width: 480px) {' \
         '.svc-row, .svc-head { grid-template-columns: 1.1rem minmax(4.5rem, 1fr) minmax(4.5rem, 1fr); row-gap: .35rem; }' \
         '.svc-row input[type="number"] { min-width: 0; }' '@media screen and (max-width: 359px) {' \
         'main { grid-template-columns: minmax(0, 1fr); }'; do
  has N index.html "$S" || { echo "REFUSING: N's index.html lacks: $S — re-brief" >&2; exit 68; }
done
has N index.html '.svc-row, .svc-head { grid-template-columns: 1.1rem minmax(0, 1fr) auto;' \
  && { echo "REFUSING: N still carries round 1's auto input track (the N-F1 cause) — not what the brief says" >&2; exit 68; }
for S in 'for (const w of [320, 350, 360, 375, 390, 481, 520, 543]) for (const dark of [false, true]) {' \
         'assert.ok(r.rateBox >= 60,' 'assert.deepEqual(r.narrow, [], "a number input too narrow to show its value");' \
         'assert.deepEqual(r.overlaps, [], "two controls overlap");'; do
  has N stage3/test/phone-layout.mjs "$S" || { echo "REFUSING: N's gate file lacks: $S — re-brief" >&2; exit 68; }
done
has N stage3/package.json 'test/phone-layout.mjs' || { echo "REFUSING: N's test:print does not run phone-layout.mjs" >&2; exit 68; }
q show "$(fld MAIN-Q 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.31",' \
  || echo "NOTE: QuickQuote main is no longer at toolVersion 2.31 — N's 2.32 may collide; the brief assumes 2.31 on main" >&2
q diff "$(fld N 5)" "$(fld N 4)" -- index.html 2>/dev/null | grep -E '^[+-]' | grep -v '^[+-][+-]' | grep -qF '@media print' \
  && { echo "REFUSING: N adds or removes a @media print line — the brief says print is untouched; re-brief" >&2; exit 68; }
[ "$(ls "$N_SHOTS" 2>/dev/null | grep -c '\.png$')" = "68" ] && [ -s "$N_SHOTS/README.md" ] && [ -s "$N_SHOTS/shots.json" ] \
  || echo "NOTE: the builder's A-6 round-2 screenshot folder is not 68 PNGs + README + shots.json at $N_SHOTS — §3 Q7 will say so" >&2
# 58 — CF5 (C-F5 + C2-F2)
for S in 'function isProviderWide(e) {' 'const NO_PROVIDER = "MAIL_NO_PROVIDER";' \
         'if (status === 429 || (status !== null && status >= 500 && status <= 599)) return true;' \
         'if (e.name === "TypeError" && e.message === "fetch failed") return true;'; do
  has CF5 stage3/lib/sendFailure.js "$S" || { echo "REFUSING: CF5's sendFailure.js lacks: $S — re-brief" >&2; exit 58; }
done
for S in 'const OTP_REFUND_CAP_PER_HOUR = 6;' 'otpRefundCapPerHour = OTP_REFUND_CAP_PER_HOUR,' \
         'if (refundCap.waitMs(src, at) > 0) {' 'return isProviderWide(e) ? "failed" : "rejected";' \
         'outcome.then(r => { if (r === "failed") refundHits(); });' 'if (early === "failed" || early === "rejected") {' \
         '}); } catch (e) { refundHits(); throw e; }' \
         'could not send the code — mail delivery is failing right now; try again in a few minutes'; do
  has CF5 stage3/server.js "$S" || { echo "REFUSING: CF5's server lacks: $S — re-brief" >&2; exit 58; }
done
has CF5 stage3/server.js 'const refundHits = () => { ipBudget.refund(src, now); globalBudget.refund("*", now); };' \
  && { echo "REFUSING: CF5's server still carries the uncapped refund line — C-F5 is not what the brief says" >&2; exit 58; }
has CF5 stage3/lib/mail.js '{ status: r.status });' && has CF5 stage3/lib/mail.js '{ code: NO_PROVIDER });' \
  || { echo "REFUSING: CF5's mail.js does not tag the Agent Mail status / no-provider code as the brief says" >&2; exit 58; }
has CF5 stage3/test/server.test.mjs 'C2-F2: a provider failure refunds the GLOBAL hit too (fails if only the global refund is dropped)' \
  && has CF5 stage3/test/server.test.mjs 'C-F5: 100 junk-address attempts from one source reach 429 within the budget' \
  || { echo "REFUSING: CF5's C-F5 / C2-F2 cells are not what the brief quotes — re-brief" >&2; exit 58; }
# 65 — I9 (item 9)
has I9 stage3/server.js 'console.error("[stage3] client error", status, err.type || "(untyped)");' \
  && has I9 stage3/server.js 'console.error("[stage3]", (err && err.stack) || String(err));' \
  && has I9 stage3/test/server.test.mjs 'ITEM 9: a malformed-JSON body never reaches the error log' \
  || { echo "REFUSING: I9's handler lines / cell are not what the brief quotes — re-brief" >&2; exit 65; }
has I9 stage3/server.js 'console.error("[stage3]", err);' && { echo "REFUSING: I9 still logs the whole error object — not what the brief says" >&2; exit 65; }
q show "$(fld MAIN-Q 4):stage3/server.js" 2>/dev/null | grep -qF 'console.error("[stage3]", err);' \
  || echo "NOTE: QuickQuote main no longer logs the whole error object — §5 Q1's positive control on main may not reproduce; use the base" >&2
# 66 — I10 (item 10)
has I10 server/errors.js 'function lastResortHandler(err, req, res, next) {' \
  && has I10 server/errors.js "413: 'Request body too large'," \
  && has I10 server/errors.js 'console.warn(`[client error ${status}] ${where}: ${err.type || '"'"'(untyped)'"'"'}`);' \
  && has I10 server/index.js 'app.use(lastResortHandler);' \
  && has I10 test/db/routes.test.js "oversized JSON body returns 413, not 500 (item 10)" \
  || { echo "REFUSING: I10's handler / wiring / cells are not what the brief quotes — re-brief" >&2; exit 66; }
has I10 server/index.js "if (err.type === 'entity.parse.failed') {" && { echo "REFUSING: I10 still carries the old inline handler" >&2; exit 66; }
# 67 — Q5 and P5B (dependencies)
has Q5 stage3/package.json '"express": "^4.19.2",' || { echo "REFUSING: Q5's package.json is not the expected one" >&2; exit 67; }
python3 - "$(q show "$(fld Q5 5):stage3/package-lock.json" 2>/dev/null)" "$(q show "$(fld Q5 4):stage3/package-lock.json" 2>/dev/null)" <<'PY' || { echo "REFUSING: Q5's lockfile is not exactly body-parser 1.20.8 + express 4.22.3 + qs 6.16.0 over its base — re-brief" >&2; exit 67; }
import sys, json
a = json.loads(sys.argv[1])["packages"]; b = json.loads(sys.argv[2])["packages"]
ch = {k: b.get(k, {}).get("version") for k in set(a) | set(b) if a.get(k, {}).get("version") != b.get(k, {}).get("version")}
sys.exit(0 if ch == {"node_modules/body-parser": "1.20.8", "node_modules/express": "4.22.3", "node_modules/qs": "6.16.0"} else 1)
PY
has P5B stage3/Dockerfile 'FROM node:22-bookworm-slim' && has P5B stage3/Dockerfile 'RUN npm ci --omit=dev' \
  && has P5B stage3/package.json '"puppeteer-core": "^25.0.2"' \
  || { echo "REFUSING: P5B's Dockerfile base / npm ci / puppeteer-core range is not what the brief quotes — re-brief" >&2; exit 67; }
has P5B stage3/Dockerfile 'FROM node:20-bookworm-slim' && { echo "REFUSING: P5B still carries the node:20 base" >&2; exit 67; }
python3 - "$(q show "$(fld P5B 4):stage3/package-lock.json" 2>/dev/null)" <<'PY' || { echo "REFUSING: P5B's lockfile is not puppeteer-core 25.0.2 without extract-zip — re-brief" >&2; exit 67; }
import sys, json
b = json.loads(sys.argv[1])["packages"]
ok = b.get("node_modules/puppeteer-core", {}).get("version") == "25.0.2" and not any(k.endswith("node_modules/extract-zip") for k in b)
sys.exit(0 if ok else 1)
PY
# 71 — FU (gate-3 follow-ups)
if isin FU; then
  has FU stage3/test/email-collector.mjs 'const CHROME_IDS = ["toggleAdvanced", "toggleDarkMode", "advWord", "fbMsg"];' \
    && has FU stage3/test/email-collector.mjs 'L-F1: the collector posts the quote inputs and NONE of the page chrome' \
    && has FU stage3/test/server.test.mjs 'K-F1: a REJECTING feedback mail still answers 201' \
    && has FU stage3/test/server.test.mjs 'assert.equal(r.headers.get("strict-transport-security"), "max-age=31536000",' \
    && has FU stage3/test/server.test.mjs 'assert.equal(r.headers.get("referrer-policy"), "no-referrer",' \
    && has FU stage3/test/server.test.mjs 'const a = await cooldownApp({ otpResendCooldownMs: 60 * 1000, clock: () => now });' \
    || { echo "REFUSING: FU's K-F1 / L-F1 / M-N2 / K-O1 cells are not what the brief quotes — re-brief" >&2; exit 71; }
fi
# 57 — the premises the stale-base rows inherit from main: M's six headers and express.json limit on QQ main.
q show "$(fld MAIN-Q 4):stage3/server.js" 2>/dev/null | grep -qF '"Strict-Transport-Security": "max-age=31536000",' \
  && q show "$(fld MAIN-Q 4):stage3/server.js" 2>/dev/null | grep -qF 'app.use(express.json({ limit: "256kb" }));' \
  || { echo "REFUSING: QuickQuote main's header / parser lines are not what the brief assumes" >&2; exit 57; }

# 63 — lockfiles per target.
PL="$(p rev-parse "$(fld MAIN-P 4):package-lock.json" 2>/dev/null)"
QL="$(q rev-parse "$(fld MAIN-Q 4):stage3/package-lock.json" 2>/dev/null)"
[ -n "$PL" ] && [ -n "$QL" ] || { echo "REFUSING: a MAIN lockfile is unreadable — guard 63 would be vacuous" >&2; exit 63; }
for ID in $IN_IDS; do
  case "$ID" in
    I10) W="$PL"; GOT="$(p rev-parse "$(fld "$ID" 4):package-lock.json" 2>/dev/null)" ;;
    Q5)  W="$Q5_LOCK"; GOT="$(q rev-parse "$(fld "$ID" 4):stage3/package-lock.json" 2>/dev/null)" ;;
    P5B) W="$P5B_LOCK"; GOT="$(q rev-parse "$(fld "$ID" 4):stage3/package-lock.json" 2>/dev/null)" ;;
    *)   W="$QL"; GOT="$(q rev-parse "$(fld "$ID" 4):stage3/package-lock.json" 2>/dev/null)" ;;
  esac
  [ "$GOT" = "$W" ] || { echo "REFUSING: row $ID's lockfile is ${GOT:0:7}, the brief expects ${W:0:7} — a dependency change; re-brief" >&2; exit 63; }
done
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" && grep -qiE 'never npm audit|no .npm audit.|never .npm audit.' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; entry by entry; never npm audit)" >&2; exit 63; }
done

# 31 — the settled-decisions file and gate 3's report (the PRIOR ROUND) are on disk and named, with the harnesses the brief copies.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G3_REPORT" ] || { echo "REFUSING: gate 3's report is absent: $G3_REPORT — N is its round 2" >&2; exit 31; }
grep -qF "$G3_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 3's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }
for H in qa-run.py qa-chrome-egressblock.sh qa-egress-monitor.py qa-netlog-scan.py lockcmp.py lockwalk.py mktree-qq.sh mktree-portal.sh \
         qa-mkdb.cjs qa-dbcheck.cjs qa-harness-c2-budget.mjs qa-lib-c2-stage3.cjs qa-harness-c2-login.mjs qa-preload-c2-entry.cjs \
         qa-harness-n-render.cjs qa-harness-n-server.cjs qa-lib-n-stage3.cjs qa-lib-n-png.cjs qa-harness-n-probe-inputs.cjs \
         qa-harness-n-probe-band.cjs N-pdfcompare.sh qa-harness-l-a10.cjs qa-harness-k.mjs qa-harness-m-d-http.cjs; do
  [ -s "$G3_DIR/evidence/$H" ] || { echo "REFUSING: gate 3's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done

# 39 — the floor instrument the brief names is on disk.
[ -s "$G3_FLOOR" ] || { echo "REFUSING: gate 3's floor instrument missing: $G3_FLOOR" >&2; exit 39; }
grep -qF "$G3_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G3_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'N (A-6 round 2, phone layout) is TIER 2, CUSTOMER-VISIBLE' 'CF5 (C-F5 + C2-F2, provider-only refund) is TIER 1' \
         'I9 (item 9, QuickQuote error log) is TIER 1' 'I10 (item 10, portal 413 pass-through) is TIER 2' \
         'Q5 (item 5, qs advisory) is TIER 2' 'P5B (item 5b, puppeteer 25 + node 22) is TIER 2' \
         'FU (gate-3 follow-ups, tests only) is TIER 2' 'ROUND 2 of 2: the cap'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
for T in 'TARGET N — A-6 ROUND 2 of 2 (TIER 2, CUSTOMER-VISIBLE' 'TARGET CF5 — C-F5 + C2-F2 (TIER 1' 'TARGET I9 — item 9 (TIER 1' \
         'TARGET I10 — item 10 (TIER 2' 'TARGET Q5 — item 5 (TIER 2' 'TARGET P5B — item 5b (TIER 2, PRODUCTION RUNTIME CHANGE' \
         'a second NO-GO ships nothing'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
[ "$SLOT_FU" = "OUT" ] || grep -qF 'TARGET FU — gate-3 follow-ups (TIER 2' "$PROMPT_FILE" || { echo "REFUSING: prompt's slot FU block does not declare TARGET FU — gate-3 follow-ups (TIER 2" >&2; exit 12; }
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
  grep -qF '[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>' "$FL" && grep -qF '[Wednesday -> QA/Vision-gate4] ANSWER' "$FL" \
    && grep -qi 'proceed on the safest reading' "$FL" && grep -qi 'read it with your verdict key' "$FL" || {
    echo "REFUSING: $FL lacks the QUESTIONS route (QUESTION subject, the [Wednesday -> QA/Vision-gate4] ANSWER reply, safest reading, verdict key)" >&2; exit 20; }
done
# 70 — the safety-check line, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'If a response is cut off by a safety check, record it and continue with the next item' "$FL" \
    && grep -qF "authorised defensive QA of Datasec's own product on loopback" "$FL" || {
    echo "REFUSING: $FL lacks the safety-check line (record and continue; authorised defensive QA on loopback)" >&2; exit 70; }
done
WORDS="SEPARATELY%PER%TARGET STALE-BASE merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN S-1 bash c1abc05 N-F1 N-F2 N-F3 N-F4 320,%375,%390,%481,%512%and%543 light%AND%dark heavy-advanced masthead pixel-identical pdftotext 2.32 a6-phone-layout-2026-09-22-r2-2246 POSITIVE%CONTROL provider-wide 6%per%source the%cap C2-F2 putOtp RestError Failed the%global%refund%dropped markers advWord /api/quote/email /auth/request /auth/verify stack Request%body%too%large Invalid%JSON%body FRESHLY%CREATED npm%audit UNVERIFIED body-parser%1.20.8 express%4.22.3 qs%6.16.0 Q5%x%P5B node:22-bookworm-slim puppeteer-core%25.0.2 decision%14 image%build%is%NOT%RUN Node%22%is%NOT%TESTED"
[ "$SLOT_FU" = "OUT" ] || WORDS="$WORDS K-F1 L-F1 M-N2 K-O1 SPLIT-middleware test:print fbMsg toggleAdvanced"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q 'NOT IN THIS GATE — portal S-1' "$BRIEF" || { echo "REFUSING: brief lacks the S-1-not-in-this-gate note" >&2; exit 19; }
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
  grep -q 'EXCLUSIVE' "$FL" && grep -q 'work-g4' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule (EXCLUSIVE, work-g4)" >&2; exit 61; }
done
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-4 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g4_' "$FL" && grep -q '<epoch>_test' "$FL" \
    && grep -q 'vsp_qa_g1_' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -q 'vsp_qa_g3_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g4_ DBs ending _test and never vsp_qa_g1_/g2_/g3_, no jest lock)" >&2; exit 62; }
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

# 38 — the brief names every negative-control seat; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — the brief tells the gate to say so and use the others" >&2
done

# Advisory: the local Postgres not answering makes the portal runtime legs NOT RUN.
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — I10's runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 41 6 7 8 9 18 22 68 58 65 66 67 71 57 63 31 39 10 17 12 13 14 15 20 70 19 24 53 60 61 62 64 69 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, commit count, gated anchors, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" { printf "  %-7s %-11s %-44s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  [ "$SLOT_FU" = "OUT" ] && printf '  FU is OUT: no slot FU in this gate.\n')"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); SLOT-FU $SLOT_FU consistent (41); commits, bases (incl. stale), counts (6 7 8); anchors (9); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: N A-6 r2 (68) CF5 C-F5 (58) I9 item 9 (65) I10 item 10 (66) Q5/P5B deps (67) FU follow-ups (71) main premises (57)"
  echo "  lockfiles per target (63); CLARIFICATIONS + gate-3 report + harnesses (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + QUESTIONS route (20); safety-check line (70); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate4-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
