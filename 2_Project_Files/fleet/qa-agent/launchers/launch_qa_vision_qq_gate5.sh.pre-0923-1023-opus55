#!/bin/bash
# launch_qa_vision_qq_gate5.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 5, 2026-09-23) on
# Datasec/Vision_Sales_Portal, TWO repos, THREE targets + slot BC:
#   A9     QQ  fix/qq-logo-ink-inset-2026-09-23             TIER 2 customer-visible (A-9, v2.33; STALE base 763269d)
#   CF5R2  QQ  fix/qq-otp-refund-provider-only-2026-09-22   TIER 1  (CF5 ROUND 2 of 2; on main 3bfbfa2 via 1435686)
#   IO1    P   fix/portal-async-route-errors-2026-09-23     TIER 1  (gate 4's I10-O1; on main 6f197ca)
#   BC     QQ  fix/qq-bounded-browser-close-2026-09-23      TIER 2  (SLOT; bounded browser.close(); touches lib/pdf.js closeBrowser)
# Portal S-1 (fix/feedback-report-auth-2026-09-22 @ 89af8ba) is GO from gate 2 and NOT in this gate (waits on Kam's card).
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it
# carries no head of its own — refuses any placeholder (row BC ships as one until Tuesday pins it), verifies every row against
# the object store and against origin by `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only
# shas it carries are GATED ANCHORS (bfb8210 = CF5 round 1, 1435686 = its forward merge): facts about what was gated, not heads.
#
# AUTHORITY: READY mails from the Vision_Sales_Portal agent (A-9 14:31Z, CF5 round 2 15:24Z, I10-O1 15:33Z) and Tuesday's rulings
# (daily note 2026-09-23 01:05, 01:26, 01:35: CF5 round 2 rule; I10-O1 -> gate 5 tier 1; bounded close incl. lib/pdf.js -> gate 5).
# Batching is Kam's standing rule of 2026-09-18. Merges after this gate are Tuesday's GO. Deploys HELD for Kam.
#
# PATTERN: launch_qa_vision_qq_gate4.sh. CHANGES:
#   - exit 40: the PIN table (6 rows: MAIN-P MAIN-Q A9 CF5R2 IO1 BC); only BC may be OUT; the BC placeholder is named.
#   - exit 41: the SLOT-BC line vs row BC vs the brief's SLOT-BC sections vs the prompt's [SLOT-BC BEGIN] block (line-start markers).
#   - exit 7: base is MAIN or a STALE BASE (NOTE); A9 is expected stale, CF5R2/IO1/BC not.
#   - exit 9: anchors — CF5R2 contains bfb8210 and 1435686 = merge(bfb8210, MAIN-Q row); A9's base carries item 20's fixed inset
#     line; IO1's base carries I10's lastResortHandler wiring; BC's base calls closeBrowser only from the two test files.
#   - exit 22: exact file sets for A9 / CF5R2 / IO1; BC's delta must be a SUBSET of {BACKLOG.md, stage3/package.json,
#     stage3/lib/pdf.js, stage3/test/*} (its delta was not on origin at drafting).
#   - exit 72 A9, 58 CF5R2, 73 IO1, 74 BC: content guards keyed on the ACTUAL code at each pinned head (drafted 01:4x AEST).
#     74 proves lib/pdf.js (if touched) differs ONLY inside closeBrowser(), and package.json only in test scripts.
#   - exit 57: premises on the MAIN rows (QQ main at 2.32; portal main wires lastResortHandler; portal express 4.22.2).
#   - exit 63: lockfiles — every IN row's lockfile equals its BASE's (no target changes a dependency).
#   - exit 62: the Vision floor discipline with gate-5 database names (vsp_qa_g5_, the _test suffix; never g1..g4).
#   - exit 20: the QUESTIONS route ('[Wednesday -> QA/Vision-gate5] ANSWER'); exit 70: the safety-check line.
#   - exit 31/39: gate 4's report, its harnesses and its Vision floor instrument are on disk and named.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 3434 (%0), NexusAI 8360 (%44).
#   - exit 75 (new): the standing lines — controls fail independently, PRIOR WORK verified against history, merge-tree from the
#     gate's OWN object dirs, no writes in either repo, three head readings — in both files.
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate5' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, grep, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate5.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..75 a guard refused
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
PH_SLOTBC='@SLOT''_BC@'
PH_BC='@BC''_'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate5.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-23_vision-qq-gate5.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G4_DIR="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate4"
G4_REPORT="$G4_DIR/report.md"
G4_FLOOR="$G4_DIR/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/vision/reports/2026-09-23-vision-qq-gate5/report.md"
NEG_SEATS='1613 3434 8360'   # Vision builder (%41), Tuesday (%0), NexusAI (%44) at drafting
# Gated anchors (not heads).
ANCHOR_CF5='bfb82100aa42772d5c5225811e8ff98f6a31279f'
FWD_CF5='1435686'

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 5: CF5 round 2 + I10-O1 async route errors (tier 1) + A-9 logo inset + bounded browser.close (tier 2), heads as pinned at launch'

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
EXPECT_IDS='MAIN-P MAIN-Q A9 CF5R2 IO1 BC'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "6" ] || { echo "REFUSING: PIN table carries rows beyond the six expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  case "$ST" in IN|OUT) ;; *) echo "REFUSING: PIN row $ID status is '$ST' (IN or OUT only; unfilled?)" >&2; exit 40 ;; esac
  case "$ID" in BC) ;; *) [ "$ST" = "IN" ] || { echo "REFUSING: only row BC may be OUT (row $ID is $ST)" >&2; exit 40; } ;; esac
  if [ "$ST" = "IN" ]; then
    [ "$ID" = "BC" ] && printf '%s' "$R" | grep -qF "$PH_BC" && {
      echo "REFUSING: PIN row BC is still the placeholder — the bounded browser.close() head is NOT PINNED. Pin head/base/commits from 'git ls-remote origin' (and re-read the brief's §BC against the pinned delta), or set SLOT-BC OUT: $R" >&2; exit 40; }
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
[ "$(fld IO1 2)" = "portal" ] || { echo "REFUSING: row IO1 must be the portal repo" >&2; exit 40; }
for ID in A9 CF5R2 BC; do [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: row $ID must be the quickquote repo" >&2; exit 40; }; done
exp_branch() { case "$1" in
  A9) echo fix/qq-logo-ink-inset-2026-09-23 ;; CF5R2) echo fix/qq-otp-refund-provider-only-2026-09-22 ;;
  IO1) echo fix/portal-async-route-errors-2026-09-23 ;; BC) echo fix/qq-bounded-browser-close-2026-09-23 ;; esac; }
for ID in A9 CF5R2 IO1 BC; do
  [ "$(fld "$ID" 7)" = "IN" ] || continue
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS="$(printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" && $1!~/^MAIN-/ {print $1}' | tr '\n' ' ')"
isin() { case " $IN_IDS " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# 41 — slot BC: the SLOT line, the row, the brief's SLOT sections and the prompt's block must agree. Line-start markers only.
SV="$(grep -m1 '^SLOT-BC: ' "$BRIEF" | sed 's/^SLOT-BC: //')"
[ -n "$SV" ] || { echo "REFUSING: the brief has no 'SLOT-BC: ' line" >&2; exit 41; }
[ "$SV" != "$PH_SLOTBC" ] || { echo "REFUSING: SLOT-BC is unfilled — Tuesday sets IN or OUT" >&2; exit 41; }
case "$SV" in IN|OUT) ;; *) echo "REFUSING: SLOT-BC line is '$SV' (IN or OUT only)" >&2; exit 41 ;; esac
[ "$SV" = "$(fld BC 7)" ] || { echo "REFUSING: SLOT-BC says $SV but PIN row BC is $(fld BC 7)" >&2; exit 41; }
NB="$(grep -c '^<!-- SLOT-BC:BEGIN -->' "$BRIEF")"; NE="$(grep -c '^<!-- SLOT-BC:END -->' "$BRIEF")"
HASP=0; grep -q '^\[SLOT-BC BEGIN\]' "$PROMPT_FILE" && grep -q '^\[SLOT-BC END\]' "$PROMPT_FILE" && HASP=1
if [ "$SV" = "IN" ]; then
  [ "$NB" = "2" ] && [ "$NE" = "2" ] && [ "$HASP" = "1" ] || { echo "REFUSING: SLOT-BC is IN but the brief's two SLOT-BC sections ($NB/$NE markers) or the prompt block ($HASP) are missing" >&2; exit 41; }
else
  [ "$NB$NE$HASP" = "000" ] || { echo "REFUSING: SLOT-BC is OUT but a brief SLOT-BC section ($NB/$NE) or the prompt block ($HASP) is still present — delete them" >&2; exit 41; }
fi
SLOT_BC="$SV"
grep -q '<fill at launch>' "$BRIEF" && { echo "REFUSING: the brief still carries a '<fill at launch>' marker" >&2; exit 41; }

# 6 / 7 / 8 — per IN row: commit in its repo; base ancestor AND merge-base; exact commit count; base is MAIN or a STALE BASE.
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
for ID in A9; do isin "$ID" || continue
  case " $STALE " in *" $ID "*) ;; *) echo "NOTE: row $ID was expected to be STALE-BASE (brief §PIN shape) and is not — the brief's §12 expectations for it may be stale" >&2 ;; esac
done
for ID in CF5R2 IO1 BC; do isin "$ID" || continue
  case " $STALE " in *" $ID "*) echo "NOTE: row $ID was expected to sit on the MAIN row and is STALE-BASE — main moved; the brief's §12 expectations for it may be stale" >&2 ;; esac
done

# 9 — gated anchors and base premises.
q merge-base --is-ancestor "$ANCHOR_CF5" "$(fld CF5R2 4)" 2>/dev/null || { echo "REFUSING: CF5R2's head does not contain the gated round-1 head bfb8210 — not a round 2; re-brief" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$FWD_CF5" 2>/dev/null)" = "$ANCHOR_CF5 $(fld MAIN-Q 4)" ] \
  || { echo "REFUSING: CF5R2's forward merge $FWD_CF5 does not have parents bfb8210 + the MAIN-Q row as the brief says" >&2; exit 9; }
q merge-base --is-ancestor "$FWD_CF5" "$(fld CF5R2 4)" 2>/dev/null || { echo "REFUSING: CF5R2's head does not contain its forward merge $FWD_CF5" >&2; exit 9; }
q show "$(fld A9 5):index.html" 2>/dev/null | grep -qF -- '--logo-ink-inset: calc(.5rem + 18.9px);' \
  || { echo "REFUSING: A9's base does not carry item 20's fixed --logo-ink-inset line — the brief's before/after is stale" >&2; exit 9; }
p show "$(fld IO1 5):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: IO1's base does not wire I10's lastResortHandler — the brief's premise is stale" >&2; exit 9; }
if isin BC; then
  CALLERS="$(q grep -l 'closeBrowser' "$(fld BC 5)" -- stage3 2>/dev/null | sed "s#^$(fld BC 5):##" | grep -v '^stage3/lib/pdf\.js$' | grep -v '/node_modules/' | sort)"
  [ "$CALLERS" = "$(sorted 'stage3/test/fx-provenance.mjs
stage3/test/typed-rates.mjs')" ] || { echo "REFUSING: at BC's base closeBrowser is referenced outside the two test files the brief names:" >&2; printf '%s\n' "$CALLERS" >&2; exit 9; }
fi

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets (BC: a subset rule).
FS_A9='BACKLOG.md
index.html
stage3/package.json
stage3/test/logo-inset.mjs'
FS_CF5R2='BACKLOG.md
stage3/lib/mail.js
stage3/lib/sendFailure.js
stage3/server.js
stage3/test/mail.test.mjs
stage3/test/server.test.mjs'
FS_IO1='BACKLOG.md
server/asyncErrors.js
server/asyncErrors.test.js
server/index.js
test/db/async-faults.test.js'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in A9 CF5R2 IO1; do
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
if isin BC; then
  GOT="$(delta BC)"
  [ -n "$GOT" ] || { echo "REFUSING: BC's delta over its base is empty" >&2; exit 22; }
  BAD="$(printf '%s\n' "$GOT" | grep -vE '^(BACKLOG\.md|stage3/package\.json|stage3/lib/pdf\.js|stage3/test/[^/]+)$')"
  [ -z "$BAD" ] || { echo "REFUSING: BC touches files outside {BACKLOG.md, stage3/package.json, stage3/lib/pdf.js, stage3/test/*} — not the through-code change the brief gates:" >&2; printf '%s\n' "$BAD" >&2; exit 22; }
  printf '%s\n' "$GOT" | grep -qx 'stage3/lib/pdf.js' \
    && echo "NOTE: BC touches stage3/lib/pdf.js — the brief's §BC production clauses (byte-unchanged renderer, 0 production calls, 0-pixel PDF) are LIVE" >&2 \
    || echo "NOTE: BC does NOT touch stage3/lib/pdf.js — the brief's §BC production clauses report 'not applicable'; Tuesday's ruling expected a closeBrowser() change" >&2
fi

# Content guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 72 — A9 (A-9)
for S in '--logo-ink-inset: calc(.5rem + min(18.9px, (100% - 1rem) * 59 / 1080));' 'toolVersion: "2.33",'; do
  has A9 index.html "$S" || { echo "REFUSING: A9's index.html lacks: $S — re-brief" >&2; exit 72; }
done
has A9 index.html '--logo-ink-inset: calc(.5rem + 18.9px);' && { echo "REFUSING: A9 still carries item 20's fixed inset — not what the brief says" >&2; exit 72; }
has A9 stage3/package.json 'test/logo-inset.mjs' || { echo "REFUSING: A9's test:print does not run logo-inset.mjs" >&2; exit 72; }
has A9 stage3/test/logo-inset.mjs 'const TOLERANCE_PX = 0.5;' \
  && has A9 stage3/test/logo-inset.mjs 'for (const w of [1280, 768, 430, 390, 375, 320]) for (const dark of [false, true]) {' \
  || { echo "REFUSING: A9's gate file is not the 24-cell, 0.5 px file the brief quotes — re-brief" >&2; exit 72; }
q diff "$(fld A9 5)" "$(fld A9 4)" -- index.html 2>/dev/null | grep -E '^[+-]' | grep -v '^[+-][+-]' | grep -qF '@media print' \
  && { echo "REFUSING: A9 adds or removes a @media print line — the brief says print is untouched; re-brief" >&2; exit 72; }
# 58 — CF5R2 (CF5 round 2)
for S in 'function isProviderWide(e) {' 'const NO_PROVIDER = "MAIL_NO_PROVIDER";' \
         'if (status === 429 || (status !== null && status >= 500 && status <= 599)) return true;'; do
  has CF5R2 stage3/lib/sendFailure.js "$S" || { echo "REFUSING: CF5R2's sendFailure.js lacks: $S — re-brief" >&2; exit 58; }
done
for S in 'const OTP_REFUND_CAP_PER_HOUR = 6;' 'const refundHits = (kind) => {' \
         'if (kind === "store") { ipBudget.refund(src, now); return; }' \
         '}); } catch (e) { refundHits("store"); throw e; }' \
         'outcome.then(r => { if (r === "failed") refundHits("provider"); });' \
         'if (refundCap.waitMs(src, at) > 0) {' \
         'could not send the code — mail delivery is failing right now; try again in a few minutes'; do
  has CF5R2 stage3/server.js "$S" || { echo "REFUSING: CF5R2's server lacks: $S — re-brief" >&2; exit 58; }
done
has CF5R2 stage3/server.js 'catch (e) { refundHits(); throw e; }' && { echo "REFUSING: CF5R2 still carries round 1's un-kinded putOtp refund" >&2; exit 58; }
python3 - "$(q show "$(fld CF5R2 4):stage3/server.js" 2>/dev/null)" <<'PY' || { echo "REFUSING: in CF5R2's refundHits the global refund is not FIRST and unconditional (before the store branch and the cap check), or is refunded twice — CF5-F1 is not fixed the way the brief says" >&2; exit 58; }
import sys
s = sys.argv[1]; i = s.find('const refundHits = (kind) => {')
if i < 0: sys.exit(1)
body = s[i:s.find('\n    };', i)]
g = body.find('globalBudget.refund("*", now);'); st = body.find('if (kind === "store")'); cap = body.find('refundCap.waitMs(')
sys.exit(0 if (g >= 0 and st > g and cap > st and body.count('globalBudget.refund(') == 1) else 1)
PY
has CF5R2 stage3/test/server.test.mjs 'CF5-F1: after a 60-min provider outage with 4 offices retrying, a FRESH office signs in at recovery' \
  && has CF5R2 stage3/test/server.test.mjs 'CF5-F2: a throwing putOtp is OUR failure' \
  && has CF5R2 stage3/test/server.test.mjs 'C2-F2: a provider failure refunds the GLOBAL hit too (fails if only the global refund is dropped)' \
  && has CF5R2 stage3/test/server.test.mjs 'C-F5: 100 junk-address attempts from one source reach 429 within the budget' \
  || { echo "REFUSING: CF5R2's CF5-F1 / CF5-F2 / C2-F2 / C-F5 cells are not what the brief quotes — re-brief" >&2; exit 58; }
for F in stage3/lib/sendFailure.js stage3/lib/mail.js; do
  [ "$(q rev-parse "$ANCHOR_CF5:$F" 2>/dev/null)" = "$(q rev-parse "$(fld CF5R2 4):$F" 2>/dev/null)" ] \
    || echo "NOTE: CF5R2's $F differs from round 1 bfb8210's — the brief says round 2 leaves it unchanged; §4 measures it" >&2
done
# 73 — IO1 (I10-O1)
for S in "const Layer = require('express/lib/router/layer');" "const PATCHED = Symbol.for('vision.asyncErrors');" \
         "throw new Error('asyncErrors: express Layer is not the Express 4 shape this patch was written for');" \
         'Layer.prototype.handle_request = function handle(req, res, next) {' \
         "ret.then(undefined, (err) => next(err || new Error('async handler rejected without a reason')));"; do
  has IO1 server/asyncErrors.js "$S" || { echo "REFUSING: IO1's asyncErrors.js lacks: $S — re-brief" >&2; exit 73; }
done
has IO1 server/index.js "require('./asyncErrors');" || { echo "REFUSING: IO1 does not require ./asyncErrors in the portal's app module" >&2; exit 73; }
python3 - "$(p show "$(fld IO1 4):server/index.js" 2>/dev/null)" <<'PY' || { echo "REFUSING: IO1's require('./asyncErrors') is not above the first route module require — the brief says 'before any router'" >&2; exit 73; }
import sys
s = sys.argv[1]; a = s.find("require('./asyncErrors');"); r = s.find("require('./routes/")
sys.exit(0 if a >= 0 and r > a else 1)
PY
has IO1 test/db/async-faults.test.js 'DB fault in the UNAUTHENTICATED POST /api/auth/login: 500 with a ref, and sign-in works once the DB is back' \
  && has IO1 server/asyncErrors.test.js 'control: a 4-argument error handler is still skipped for ordinary requests' \
  || { echo "REFUSING: IO1's cells are not what the brief quotes — re-brief" >&2; exit 73; }
# 74 — BC (bounded close): lib/pdf.js may change ONLY inside closeBrowser(); package.json only in test scripts.
if isin BC; then
  if printf '%s\n' "$(delta BC)" | grep -qx 'stage3/lib/pdf.js'; then
    python3 - "$(q show "$(fld BC 5):stage3/lib/pdf.js" 2>/dev/null)" "$(q show "$(fld BC 4):stage3/lib/pdf.js" 2>/dev/null)" <<'PY' || { echo "REFUSING: BC changes stage3/lib/pdf.js OUTSIDE closeBrowser() (renderQuotePdf / the launch / exports / a new helper) — the brief gates a closeBrowser-only change; re-brief" >&2; exit 74; }
import sys
def strip(s):
    # the function may take parameters (closeBrowser(ms = 5000)) and its leading /* For tests ... */ comment belongs to it
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
  fi
  if printf '%s\n' "$(delta BC)" | grep -qx 'stage3/package.json'; then
    PJ="$(q diff "$(fld BC 5)" "$(fld BC 4)" -- stage3/package.json 2>/dev/null | grep -E '^[+-]' | grep -v '^[+-][+-]')"
    BADPJ="$(printf '%s\n' "$PJ" | grep -vE '^[+-]    "test(:[a-z]+)?": ')"
    [ -z "$BADPJ" ] || { echo "REFUSING: BC's stage3/package.json delta is not test scripts only:" >&2; printf '%s\n' "$BADPJ" >&2; exit 74; }
  fi
fi
# 57 — premises on the MAIN rows.
q show "$(fld MAIN-Q 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.32",' \
  || echo "NOTE: QuickQuote main is no longer at toolVersion 2.32 — A9's 2.33 premise may be stale" >&2
p show "$(fld MAIN-P 4):server/index.js" 2>/dev/null | grep -qF 'app.use(lastResortHandler);' \
  || { echo "REFUSING: portal main does not wire lastResortHandler — IO1's premise (serverError answers the faults) is stale" >&2; exit 57; }
python3 - "$(p show "$(fld IO1 4):package-lock.json" 2>/dev/null)" <<'PY' || { echo "REFUSING: IO1's lockfile does not resolve express 4.22.2 — the brief's line-by-line comparison names 4.22.2" >&2; exit 57; }
import sys, json
b = json.loads(sys.argv[1])["packages"]
sys.exit(0 if b.get("node_modules/express", {}).get("version") == "4.22.2" else 1)
PY

# 63 — lockfiles: no target changes a dependency (each IN row's lockfile equals its base's).
for ID in $IN_IDS; do
  case "$ID" in IO1) LF='package-lock.json'; G=p ;; *) LF='stage3/package-lock.json'; G=q ;; esac
  W="$($G rev-parse "$(fld "$ID" 5):$LF" 2>/dev/null)"; GOT="$($G rev-parse "$(fld "$ID" 4):$LF" 2>/dev/null)"
  [ -n "$W" ] && [ "$GOT" = "$W" ] || { echo "REFUSING: row $ID's lockfile is ${GOT:0:7}, its base's is ${W:0:7} — a dependency change the brief does not gate; re-brief" >&2; exit 63; }
done
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" && grep -qiE 'never npm audit|no .npm audit.|never .npm audit.' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; entry by entry; never npm audit)" >&2; exit 63; }
done

# 31 — the settled-decisions file and gate 4's report (the PRIOR ROUND) are on disk and named, with the harnesses the brief copies.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G4_REPORT" ] || { echo "REFUSING: gate 4's report is absent: $G4_REPORT — CF5R2 is its round 2" >&2; exit 31; }
grep -qF "$G4_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 4's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }
for H in qa-run.py qa-chrome-egressblock.sh qa-egress-monitor.py qa-egress-posctl.mjs qa-netlog-scan.py lockcmp.py lockwalk.py \
         mktree-qq.sh mktree-portal.sh qa-mkdb.cjs qa-dbcheck.cjs qa-harness-floorctl.mjs qa-harness-cf5.mjs qa-lib-cf5-stage3.cjs \
         qa-harness-cf5-c2contract.mjs qa-harness-cf5-login.mjs qa-harness-lead-cf5.cjs CF5-mutate.py qa-harness-i10.cjs \
         qa-i10-preload-fetchguard.cjs I10-crash.sh qa-harness-n-render.cjs qa-harness-n-server.cjs qa-lib-n-stage3.cjs qa-lib-n-png.cjs \
         qa-harness-n-probe-sweep.cjs qa-harness-n-probe-crops.cjs N-pdfcompare.sh qa-harness-p5b-emailed.cjs qa-lib-p5b-png.cjs P5B-pdfcompare.sh; do
  [ -s "$G4_DIR/evidence/$H" ] || { echo "REFUSING: gate 4's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done
[ -s "$G4_DIR/sections/CONVENTIONS.md" ] || { echo "REFUSING: gate 4's sections/CONVENTIONS.md is absent — the brief names it as the working method" >&2; exit 31; }

# 39 — the floor instrument the brief names is on disk.
[ -s "$G4_FLOOR" ] || { echo "REFUSING: gate 4's floor instrument missing: $G4_FLOOR" >&2; exit 39; }
grep -qF "$G4_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G4_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'A9 (A-9, logo ink inset) is TIER 2, CUSTOMER-VISIBLE' 'CF5R2 (CF5 round 2, provider-only refund) is TIER 1' \
         'ROUND 2 of 2: the cap' 'IO1 (I10-O1, portal async route errors) is TIER 1'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
[ "$SLOT_BC" = "OUT" ] || grep -qF 'BC (bounded browser.close()) is TIER 2' "$BRIEF" || { echo "REFUSING: brief does not declare BC's tier" >&2; exit 12; }
for T in 'TARGET A9 — A-9 logo ink inset (TIER 2, CUSTOMER-VISIBLE' 'TARGET CF5R2 — CF5 ROUND 2 of 2 (TIER 1' \
         'TARGET IO1 — I10-O1 async route errors (TIER 1' 'a second NO-GO ships the parts that closed and tickets the rest'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
[ "$SLOT_BC" = "OUT" ] || grep -qF 'TARGET BC — bounded browser.close() (TIER 2' "$PROMPT_FILE" || { echo "REFUSING: prompt's slot BC block does not declare TARGET BC — bounded browser.close() (TIER 2" >&2; exit 12; }
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
  grep -qF '[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>' "$FL" && grep -qF '[Wednesday -> QA/Vision-gate5] ANSWER' "$FL" \
    && grep -qi 'proceed on the safest reading' "$FL" && grep -qi 'read it with your verdict key' "$FL" || {
    echo "REFUSING: $FL lacks the QUESTIONS route (QUESTION subject, the [Wednesday -> QA/Vision-gate5] ANSWER reply, safest reading, verdict key)" >&2; exit 20; }
done
# 70 — the safety-check line, in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -qF 'If a response is cut off by a safety check, record it and continue with the next item' "$FL" \
    && grep -qF "authorised defensive QA of Datasec's own product on loopback" "$FL" || {
    echo "REFUSING: $FL lacks the safety-check line (record and continue; authorised defensive QA on loopback)" >&2; exit 70; }
done
WORDS="SEPARATELY%PER%TARGET STALE-BASE merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN S-1 bash POSITIVE%CONTROL A-9 --logo-ink-inset 2.33 light%AND%dark pixel-identical pdftotext logo-inset.mjs after%A-6 CF5-F1 CF5-F2 C-F5 C2-F2 CF5-F3 1435686 bfb8210 putOtp UNCAPPED Retry-After ROUND%2%of%2 I10-O1 handle_request next(err) 26%of%81 /api/auth/login headers%are%sent 4-arg refuse-to-boot express%4.22.2 /api/health 20/26 FRESHLY%CREATED"
[ "$SLOT_BC" = "OUT" ] || WORDS="$WORDS closeBrowser renderQuotePdf byte-unchanged 0%differing%pixels forced%close() fx-provenance typed-rates N-C1"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q 'NOT IN THIS GATE:\*\* portal S-1' "$BRIEF" || { echo "REFUSING: brief lacks the S-1-not-in-this-gate note" >&2; exit 19; }
grep -q 'REPORT, DO NOT FAIL ON' "$BRIEF" || { echo "REFUSING: brief lacks the CF5R2 known-and-Kam's report-only items" >&2; exit 19; }
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
  grep -q 'EXCLUSIVE' "$FL" && grep -q 'work-g5' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule (EXCLUSIVE, work-g5)" >&2; exit 61; }
done
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-5 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g5_' "$FL" && grep -q '<epoch>_test' "$FL" \
    && grep -q 'vsp_qa_g1_' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -q 'vsp_qa_g3_' "$FL" && grep -q 'vsp_qa_g4_' "$FL" \
    && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g5_ DBs ending _test and never vsp_qa_g1_..g4_, no jest lock)" >&2; exit 62; }
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
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — IO1's runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 41 6 7 8 9 18 22 72 58 73 74 57 63 31 39 10 17 12 13 14 15 20 70 19 24 53 60 61 62 64 69 75 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, commit count, gated anchors, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" { printf "  %-7s %-11s %-44s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  [ "$SLOT_BC" = "OUT" ] && printf '  BC is OUT: no slot BC in this gate.\n')"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); SLOT-BC $SLOT_BC consistent (41); commits, bases (incl. stale), counts (6 7 8); anchors (9); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: A9 A-9 (72) CF5R2 round 2 (58) IO1 I10-O1 (73) BC bounded close (74) main premises (57)"
  echo "  lockfiles per target (63); CLARIFICATIONS + gate-4 report + harnesses (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + QUESTIONS route (20); safety-check line (70); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); standing lines (75); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate5-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
exec claude --dangerously-skip-permissions --model claude-opus-5 "$PROMPT"
