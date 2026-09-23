#!/bin/bash
# launch_qa_vision_qq_gate3.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 3, 2026-09-22) on
# Datasec/Vision_Sales_Portal, TWO repos, FOUR targets + slots M and N:
#   C  A-1 QQ   feat/qq-otp-send-budget-2026-09-22        TIER 1 narrow  (round 2: clock, C-F1/F2/F3; STALE base 49d7027)
#   B  S-2 P    fix/reminder-push-redaction-2026-09-22    TIER 1 narrow  (round 2: B-F1 fresh-DB fixture; STALE base 289e2d9)
#   K  QQ       fix/qq-feedback-followups-2026-09-22      TIER 2         (A1-F1 + A1-F2; STALE base 1f3df8d)
#   L  QQ       fix/qq-small-sweep-2026-09-22             TIER 2         (A-7 + A-8 + A-10; STALE base 1f3df8d)
#   M  QQ       fix/qq-d-f1-header-order-2026-09-22       TIER 2         (SLOT; D-F1 test-only cell)
#   N  QQ       fix/qq-phone-overflow-2026-09-22          TIER 2         (SLOT; A-6 phone layout, customer-visible, v2.32)
# Portal S-1 (fix/feedback-report-auth-2026-09-22 @ 89af8ba) is GO from gate 2 and NOT in this gate (waits on Kam's card).
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it
# carries no head of its own — refuses any placeholder, verifies every row against the object store and against origin by
# `git ls-remote` NOW, and appends the verified table to the agent's prompt. The only shas it carries are the GATED ANCHORS
# (fb23f64 for B, 3c8d3a4 / 4b946d0 / 49d7027 for C): facts about what round 1 gated, not heads.
#
# AUTHORITY: READY mails from the Vision_Sales_Portal agent (B-F1 10:43Z, A-7/A-8/A-10 09:59Z, C round 2 11:12Z) and Tuesday's
# rulings (C: fix in C + fold C-F1/F2/F3 + gate 3 narrow, 20:55; slots M and N IN, ~21:15). C-01..C-05 (Vision CLARIFICATIONS)
# govern item 1 (K) and item 3 (on main). Batching is Kam's standing rule of 2026-09-18. Merges after this gate are Tuesday's GO.
# Deploys HELD for Kam.
#
# PATTERN: launch_qa_vision_qq_gate2.sh. CHANGES:
#   - exit 40: the PIN table (8 rows: MAIN-P MAIN-Q B C K L M N); only M and N may be OUT.
#   - exit 41: SLOT-M and SLOT-N lines vs rows M/N vs the brief's SLOT sections vs the prompt's [SLOT-X BEGIN] blocks.
#   - exit 7: base is MAIN, OR another IN row's head (a named stack), OR a STALE BASE: an ancestor of MAIN that equals
#     merge-base(head, MAIN) — printed as a NOTE (a forward merge is owed at merge time; §12 measures it).
#   - exit 9 (new): gated anchors — B contains fb23f64 and B's delta over fb23f64 is the one test file; dispatcher.js is
#     byte-identical at fb23f64 and B; C contains 3c8d3a4; 4b946d0's parents are exactly 3c8d3a4 + 49d7027.
#   - exit 22: per-target exact file sets over their bases.
#   - exit 56, 58, 65-68: per-target content drift guards (strings the brief quotes, read from the pinned head).
#   - exit 63: no target changes its repo's lockfile (vs the MAIN row); both files carry the offline-install rule.
#   - exit 62: the Vision floor discipline with gate-3 database names (vsp_qa_g3_, the _test suffix; never g1/g2).
#   - exit 69: ntfy is never contacted (ntfy.invalid stub rule) and FX egress blocked, in both files.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 45678 (%0), NexusAI 8360 (%44).
#   - exit 24 carried: the prompt must not carry either app's literal server entry path.
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate3' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-remote.
# --check is READ-ONLY: it runs every guard and exits before any identity dir is made or any agent is started.
# Usage: launch_qa_vision_qq_gate3.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..69 a guard refused
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
PH_SLOTM='@SLOT''_M@'
PH_SLOTN='@SLOT''_N@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate3.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate3.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G2_DIR="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate2"
G2_REPORT="$G2_DIR/report.md"
G5_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py"
G5_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorlib.sh"
N_SHOTS="$VSP/5_Project_History/a6-phone-layout-2026-09-22-2053"
REPORT="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate3/report.md"
NEG_SEATS='1613 45678 8360'   # Vision builder (%41), Tuesday (%0), NexusAI (%44) at drafting
# Gated anchors (what round 1 gated; not heads).
ANCHOR_B='fb23f64ab335a67b7e761e95528bcd4a604ed7ec'
ANCHOR_C='3c8d3a41733f7f2aa49591a71abfa8fcc1c9cbbe'
FWD_C='4b946d0'
FWD_C_MAIN='49d7027bcb627b001ed3de4c2cb560c234375261'

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 3: A-1 round 2 + S-2 round 2 (tier 1) + item-1 follow-ups + A-7/A-8/A-10 + D-F1 + A-6 (tier 2), heads as pinned at launch'

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
EXPECT_IDS='MAIN-P MAIN-Q B C K L M N'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "8" ] || { echo "REFUSING: PIN table carries rows beyond the eight expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  case "$ST" in IN|OUT) ;; *) echo "REFUSING: PIN row $ID status is '$ST' (IN or OUT only; unfilled?)" >&2; exit 40 ;; esac
  case "$ID" in MAIN-*|M|N) ;; *) [ "$ST" = "IN" ] || { echo "REFUSING: only rows M and N may be OUT (row $ID is $ST)" >&2; exit 40; } ;; esac
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
[ "$(fld B 2)" = "portal" ] || { echo "REFUSING: row B must be the portal repo" >&2; exit 40; }
for ID in C K L M N; do [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: row $ID must be the quickquote repo" >&2; exit 40; }; done
exp_branch() { case "$1" in
  B) echo fix/reminder-push-redaction-2026-09-22 ;; C) echo feat/qq-otp-send-budget-2026-09-22 ;;
  K) echo fix/qq-feedback-followups-2026-09-22 ;; L) echo fix/qq-small-sweep-2026-09-22 ;;
  M) echo fix/qq-d-f1-header-order-2026-09-22 ;; N) echo fix/qq-phone-overflow-2026-09-22 ;; esac; }
for ID in B C K L M N; do
  [ "$(fld "$ID" 7)" = "IN" ] || continue
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS="$(printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" && $1!~/^MAIN-/ {print $1}' | tr '\n' ' ')"
isin() { case " $IN_IDS " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }

# 41 — slots M and N: the SLOT line, the row, the brief's SLOT section and the prompt's block must agree.
for S in M N; do
  eval "PH=\"\$PH_SLOT$S\""
  SV="$(grep -m1 "^SLOT-$S: " "$BRIEF" | sed "s/^SLOT-$S: //")"
  [ -n "$SV" ] || { echo "REFUSING: the brief has no 'SLOT-$S: ' line" >&2; exit 41; }
  [ "$SV" != "$PH" ] || { echo "REFUSING: SLOT-$S is unfilled — Tuesday sets IN or OUT" >&2; exit 41; }
  case "$SV" in IN|OUT) ;; *) echo "REFUSING: SLOT-$S line is '$SV' (IN or OUT only)" >&2; exit 41 ;; esac
  [ "$SV" = "$(fld "$S" 7)" ] || { echo "REFUSING: SLOT-$S says $SV but PIN row $S is $(fld "$S" 7)" >&2; exit 41; }
  HASB=0; grep -q "<!-- SLOT-$S:BEGIN -->" "$BRIEF" && grep -q "<!-- SLOT-$S:END -->" "$BRIEF" && HASB=1
  HASP=0; grep -qF "[SLOT-$S BEGIN]" "$PROMPT_FILE" && grep -qF "[SLOT-$S END]" "$PROMPT_FILE" && HASP=1
  if [ "$SV" = "IN" ]; then
    [ "$HASB$HASP" = "11" ] || { echo "REFUSING: SLOT-$S is IN but the brief section ($HASB) or the prompt block ($HASP) is missing" >&2; exit 41; }
  else
    [ "$HASB$HASP" = "00" ] || { echo "REFUSING: SLOT-$S is OUT but the brief section ($HASB) or the prompt block ($HASP) is still present — delete both" >&2; exit 41; }
  fi
  eval "SLOT_$S=\"\$SV\""
done
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
for ID in B C K L; do isin "$ID" || continue
  case " $STALE " in *" $ID "*) ;; *) echo "NOTE: row $ID was expected to be STALE-BASE (brief §PIN shape) and is not — the brief's §12 predictions for it may be stale" >&2 ;; esac
done

# 9 — gated anchors: round 2 must BUILD ON what round 1 gated.
p merge-base --is-ancestor "$ANCHOR_B" "$(fld B 4)" 2>/dev/null || { echo "REFUSING: B's head does not contain the gated fb23f64 — not a round 2; re-brief" >&2; exit 9; }
[ "$(p diff --name-only "$ANCHOR_B" "$(fld B 4)" 2>/dev/null)" = "test/db/reminder-push.test.js" ] \
  || { echo "REFUSING: B's delta over the gated fb23f64 is not exactly test/db/reminder-push.test.js — B is no longer test-only; re-brief" >&2; p diff --name-only "$ANCHOR_B" "$(fld B 4)" >&2; exit 9; }
[ "$(p rev-parse "$ANCHOR_B:server/reminders/dispatcher.js" 2>/dev/null)" = "$(p rev-parse "$(fld B 4):server/reminders/dispatcher.js" 2>/dev/null)" ] \
  || { echo "REFUSING: dispatcher.js differs between the gated fb23f64 and B's head" >&2; exit 9; }
q merge-base --is-ancestor "$ANCHOR_C" "$(fld C 4)" 2>/dev/null || { echo "REFUSING: C's head does not contain the gated 3c8d3a4 — not a round 2; re-brief" >&2; exit 9; }
[ "$(q log -1 --format='%P' "$FWD_C" 2>/dev/null)" = "$ANCHOR_C $FWD_C_MAIN" ] \
  || { echo "REFUSING: C's forward merge $FWD_C does not have parents 3c8d3a4 + 49d7027 as the brief says" >&2; exit 9; }
q merge-base --is-ancestor "$FWD_C" "$(fld C 4)" 2>/dev/null || { echo "REFUSING: C's head does not contain the forward merge $FWD_C" >&2; exit 9; }

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets.
FS_B='DEV-SESSION-SUMMARY.md
docker-compose.yml
server/reminders/dispatcher.js
test/db/reminder-push.test.js'
FS_C='BACKLOG.md
stage3/server.js
stage3/test/server.test.mjs'
FS_K='stage3/server.js
stage3/test/server.test.mjs'
FS_L='BACKLOG.md
stage3/server.js
stage3/strip.js
stage3/test/server.test.mjs
stage3/test/strip.test.mjs'
FS_M='stage3/test/server.test.mjs'
FS_N='BACKLOG.md
index.html
stage3/package.json
stage3/test/phone-layout.mjs'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in $IN_IDS; do
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done

# Content drift guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 56 — B (S-2 round 2): the redaction as gated, and the B-F1 fixture.
has B server/reminders/dispatcher.js 'title: `Reminder #${rem.id} due`,' \
  && has B server/reminders/dispatcher.js "body: 'Open the Vision Sales Portal (PRO dashboard → Reminders) to read it.'," \
  && has B server/reminders/dispatcher.js 'escapeHtml(rem.body || rem.title)' \
  && has B docker-compose.yml 'NTFY_TOPIC: ${NTFY_TOPIC:-}' \
  && has B test/db/reminder-push.test.js 'await buildDigest();' \
  && has B test/db/reminder-push.test.js "const { runDigest, buildDigest } = require('../../server/feedbackDigest');" \
  || { echo "REFUSING: B's redaction / compose default / B-F1 fixture is not what the brief quotes — re-brief" >&2; exit 56; }
# 58 — C (A-1 round 2): clock, C-F2 text, C-F1 validation, C-F3 refund.
for S in 'const now = clock().getTime();' 'if (!rec || clock().getTime() > Number(rec.expiresAt))' \
         'return tooSoon(ipWait, "too many sign-in codes requested from your network");' \
         'return tooSoon(globalWait, "sign-in is busy right now");' \
         'function budgetSetting(name, value, fallback) {' 'refund(key, at) {' \
         'const refundHits = () => { ipBudget.refund(src, now); globalBudget.refund("*", now); };' \
         '}); } catch (e) { refundHits(); throw e; }' 'outcome.then(r => { if (r === "failed") refundHits(); });' \
         'const OTP_IP_BUDGET_PER_HOUR = 6;' 'const OTP_GLOBAL_BUDGET_PER_HOUR = 20;' 'trustForwardedFor = !!process.env.WEBSITE_SITE_NAME'; do
  has C stage3/server.js "$S" || { echo "REFUSING: C's server lacks: $S — re-brief" >&2; exit 58; }
done
for S in 'try again later");' 'sign-in is busy right now — try again'; do
  has C stage3/server.js "$S" && { echo "REFUSING: C's server still carries the round-1 refusal text '$S' — C-F2 is not what the brief says" >&2; exit 58; }
done
has C stage3/server.js '"Content-Security-Policy": CSP' && echo "NOTE: C's head now carries D's security headers — its base moved past 49d7027; §3 Q8 assumes it does not" >&2
# 65 — K (item-1 follow-ups)
has K stage3/server.js 'feedbackNotify = process.env.FEEDBACK_NOTIFY_EMAIL || process.env.FEEDBACK_NOTIFY_EMAILS || DEFAULT_FEEDBACK_NOTIFY,' \
  && has K stage3/test/server.test.mjs 'A1-F1: the feedback submission does not wait for the notification mail' \
  && has K stage3/test/server.test.mjs 'A1-F2: FEEDBACK_NOTIFY_EMAILS' \
  || { echo "REFUSING: K's precedence line / A1 cells are not what the brief quotes — re-brief" >&2; exit 65; }
p show "$(fld MAIN-P 4):server/feedbackNotify.js" 2>/dev/null | grep -qF 'return env.FEEDBACK_NOTIFY_EMAILS || env.FEEDBACK_NOTIFY_EMAIL ||' \
  || echo "NOTE: portal main's feedbackNotify.js no longer reads EMAILS || EMAIL — the brief's opposite-precedence comparison (§5 Q1) is stale" >&2
# 66 — L (small sweep)
has L stage3/strip.js '"public/index.html", Buffer.byteLength(html), "bytes;",' \
  && has L stage3/strip.js 'const NOT_QUOTE = new Set(["toggleAdvanced", "toggleDarkMode", "advWord", "fbMsg"]);' \
  && has L stage3/strip.js 'if (!el.id || NOT_QUOTE.has(el.id)) return;' \
  && has L stage3/server.js 'app.get("/favicon.ico", (req, res) => res.status(204).end());' \
  || { echo "REFUSING: L's A-7 / A-10 / A-8 lines are not what the brief quotes — re-brief" >&2; exit 66; }
# 67 — M (D-F1): the cell, and main's order it pins.
if isin M; then
  has M stage3/test/server.test.mjs 'D-F1: bodies the parser rejects (malformed 400, oversized 413) still carry the security headers' \
    || { echo "REFUSING: M's D-F1 cell is not what the brief quotes — re-brief" >&2; exit 67; }
  python3 - "$(q show "$(fld M 4):stage3/server.js" 2>/dev/null | cat)" <<'PY' || { echo "REFUSING: at M's head the header middleware is not registered before express.json (or a marker is missing) — the premise of the cell" >&2; exit 67; }
import sys
s = sys.argv[1]
a = s.find('"Content-Security-Policy": CSP'); b = s.find('app.use(express.json(')
sys.exit(0 if 0 <= a < b else 1)
PY
fi
# 68 — N (A-6)
if isin N; then
  has N index.html 'toolVersion: "2.32",' && has N index.html '@media screen and (max-width: 480px) {' \
    && has N index.html 'main { grid-template-columns: minmax(0, 1fr); }' && has N stage3/package.json 'test/phone-layout.mjs' \
    || { echo "REFUSING: N's version / 480px screen block / minmax track / test wiring is not what the brief quotes — re-brief" >&2; exit 68; }
  q show "$(fld MAIN-Q 4):index.html" 2>/dev/null | grep -qF 'toolVersion: "2.31",' \
    || echo "NOTE: QuickQuote main is no longer at toolVersion 2.31 — N's 2.32 may collide; the brief assumes 2.31 on main" >&2
  q diff "$(fld N 5)" "$(fld N 4)" -- index.html 2>/dev/null | grep -E '^[+-]' | grep -v '^[+-][+-]' | grep -qF '@media print' \
    && { echo "REFUSING: N adds or removes a @media print line — the brief says print is untouched; re-brief" >&2; exit 68; }
  [ "$(ls "$N_SHOTS" 2>/dev/null | grep -c '\.png$')" = "24" ] && [ -s "$N_SHOTS/README.md" ] \
    || echo "NOTE: the builder's A-6 screenshot folder is not 24 PNGs + README at $N_SHOTS — §N Q1's comparison will say so" >&2
fi

# 63 — no target changes its repo's lockfile (vs the MAIN row); the offline-install rule in both files.
PL="$(p rev-parse "$(fld MAIN-P 4):package-lock.json" 2>/dev/null)"
QL="$(q rev-parse "$(fld MAIN-Q 4):stage3/package-lock.json" 2>/dev/null)"
[ -n "$PL" ] && [ -n "$QL" ] || { echo "REFUSING: a MAIN lockfile is unreadable — guard 63 would be vacuous" >&2; exit 63; }
for ID in $IN_IDS; do
  if [ "$(fld "$ID" 2)" = portal ]; then W="$PL"; GOT="$(p rev-parse "$(fld "$ID" 4):package-lock.json" 2>/dev/null)"
  else W="$QL"; GOT="$(q rev-parse "$(fld "$ID" 4):stage3/package-lock.json" 2>/dev/null)"; fi
  [ "$GOT" = "$W" ] || { echo "REFUSING: row $ID changes its lockfile (${GOT:0:7} vs main ${W:0:7}) — a dependency change; re-brief" >&2; exit 63; }
done
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; node_modules proven against the gated lockfile entry by entry)" >&2; exit 63; }
done

# 31 — the settled-decisions file and gate 2's report (the PRIOR ROUND for C and B) are on disk and named.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G2_REPORT" ] || { echo "REFUSING: gate 2's report is absent: $G2_REPORT — C and B are its round 2" >&2; exit 31; }
grep -qF "$G2_DIR" "$BRIEF" || { echo "REFUSING: the brief does not name gate 2's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }
for H in qa-harness-c-budget.mjs qa-harness-c-login.mjs qa-harness-h.mjs qa-lib-h.cjs qa-harness-b-push.cjs qa-run.py qa-chrome-egressblock.sh; do
  [ -s "$G2_DIR/evidence/$H" ] || { echo "REFUSING: gate 2's harness $H is not on disk — the brief tells the gate to copy it" >&2; exit 31; }
done

# 39 — the floor instrument the brief names is on disk.
[ -s "$G5_FLOOR" ] && [ -s "$G5_FLOORLIB" ] || { echo "REFUSING: gate 5's floor instrument missing: $G5_FLOOR / $G5_FLOORLIB" >&2; exit 39; }
grep -qF "$G5_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G5_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'C (A-1 round 2, sign-in-code budgets) is TIER 1' 'B (S-2 round 2, reminder push redaction) is TIER 1' \
         'K (item-1 follow-ups, A1-F1 + A1-F2) is TIER 2' 'L (small sweep, A-7 + A-8 + A-10) is TIER 2' \
         'M (D-F1, header-order cell) is TIER 2' 'N (A-6, phone layout) is TIER 2'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
for T in 'TARGET C — A-1 ROUND 2 (TIER 1, NARROW' 'TARGET B — S-2 ROUND 2 (TIER 1, NARROW' 'TARGET K — item-1 follow-ups (TIER 2' 'TARGET L — small sweep (TIER 2'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
[ "$SLOT_M" = "OUT" ] || grep -qF 'TARGET M — D-F1 (TIER 2' "$PROMPT_FILE" || { echo "REFUSING: prompt's slot M block does not declare TARGET M — D-F1 (TIER 2" >&2; exit 12; }
[ "$SLOT_N" = "OUT" ] || grep -qF 'TARGET N — A-6 (TIER 2, CUSTOMER-VISIBLE' "$PROMPT_FILE" || { echo "REFUSING: prompt's slot N block does not declare TARGET N — A-6 (TIER 2, CUSTOMER-VISIBLE" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -q '@[A-Z_]*@' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries a placeholder — placeholders belong in the brief only" >&2; exit 14; }
grep -q 'appended the verified table' "$PROMPT_FILE" || { echo "REFUSING: prompt must tell the agent the verified PIN table is appended" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-Vision has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="SEPARATELY%PER%TARGET ADVERSARIAL%PASS LEGITIMATE%SHAPES STALE-BASE 4b946d0 union DERIVED exactly%the%contract%change putOtp clock() C-F1 C-F2 C-F3 FRESHLY%CREATED PROVE%it%is%fresh Byte%compare SET%and%UNSET buildDigest ntfy.invalid FEEDBACK_NOTIFY_EMAILS opposite%order real%BYTES favicon advWord QUOTE%MISMATCH X-Forwarded-For /64 merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN S-1 bash"
[ "$SLOT_M" = "OUT" ] || WORDS="$WORDS RED%when%the%body%parser%is%moved vacuous"
[ "$SLOT_N" = "OUT" ] || WORDS="$WORDS 320,%375%and%390 light%AND%dark pixel-identical pdftotext masthead 2.32"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
grep -q 'ADVERSARIAL PASS (C)' "$BRIEF" || { echo "REFUSING: brief lacks ADVERSARIAL PASS (C)" >&2; exit 19; }
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
  grep -q 'EXCLUSIVE' "$FL" || { echo "REFUSING: $FL lacks the tree-exclusivity rule" >&2; exit 61; }
done
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-3 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g3_' "$FL" && grep -q '<epoch>_test' "$FL" \
    && grep -q 'vsp_qa_g1_' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g3_ DBs ending _test and never vsp_qa_g1_/g2_, no jest lock)" >&2; exit 62; }
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
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — B's runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 41 6 7 8 9 18 22 56 58 65 66 67 68 63 31 39 10 17 12 13 14 15 20 19 24 53 60 61 62 64 69 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, commit count, gated anchors, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" { printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  printf '  STALE-BASE rows (forward merge owed at merge time):%s\n' "${STALE:- none}"
  [ "$SLOT_M" = "OUT" ] && printf '  M is OUT: no slot M in this gate.\n'
  [ "$SLOT_N" = "OUT" ] && printf '  N is OUT: no slot N in this gate.\n')"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); SLOT-M $SLOT_M / SLOT-N $SLOT_N consistent (41); commits, bases (incl. stale), counts (6 7 8); gated anchors (9); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: B S-2 r2 (56) C A-1 r2 (58) K follow-ups (65) L sweep (66) M D-F1 (67) N A-6 (68)"
  echo "  lockfiles unchanged vs mains (63); CLARIFICATIONS + gate-2 report + harnesses (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + question route (20); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate3-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
