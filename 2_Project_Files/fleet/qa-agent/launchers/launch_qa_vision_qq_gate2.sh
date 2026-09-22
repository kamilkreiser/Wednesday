#!/bin/bash
# launch_qa_vision_qq_gate2.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 2, 2026-09-22) on
# Datasec/Vision_Sales_Portal, TWO repos, NINE targets + slot J:
#   A  S-1 portal  fix/feedback-report-auth-2026-09-22       TIER 1  (report/summary need a session or the coordinator secret)
#   B  S-2 portal  fix/reminder-push-redaction-2026-09-22    TIER 1  (ntfy pushes redacted; rebased onto G)
#   G  portal      integration/portal-gate2-2026-09-22       TIER 1  (main + gate-1 item 4 + item 1 portal: gate 1's NOT RUN legs)
#   C  A-1 QQ      feat/qq-otp-send-budget-2026-09-22        TIER 1  (sign-in-code budgets)
#   D  A-2 QQ      feat/qq-security-headers-2026-09-22       TIER 2
#   E  A-3 QQ      feat/qq-sign-out-2026-09-22               TIER 2
#   F  A-4 QQ      fix/qq-pdf-fx-provenance-2026-09-22       TIER 2  (customer-visible PDF text)
#   H  item 3 QQ   feat/qq-open-old-quote-2026-09-22         TIER 1  (ROUND 2 of 2, rebased)
#   I  A-5 QQ      fix/qq-dockerignore-2026-09-22            TIER 2  (build recipe only)
#   J  O-1 QQ      fix/qq-typed-ps-rates-o1-2026-09-22       TIER 1  (SLOT; IN or OUT per the brief's SLOT-J line)
#
# THE HEADS LIVE IN ONE PLACE: the brief's PIN-HEADS table (between the PIN-HEADS markers). This launcher PARSES it — it
# carries no sha of its own — refuses any placeholder, verifies every row against the object store and against origin by
# `git ls-remote` NOW, and appends the verified table to the agent's prompt. (Gate 1 hard-coded its heads here; gate 2's heads
# were moving during drafting — QuickQuote main 47eb533 -> 1f3df8d and a full rebase round — so they are filled at launch.)
#
# AUTHORITY: READY FOR QA from the Vision_Sales_Portal agent (S-1 + A-1 09:19Z, S-2 + A-2 09:29Z; A-3, A-4, A-5, O-1 and the
# rebase round later on 2026-09-22) and Tuesday's scope update after gate 1's verdict. C-01..C-05 (Vision CLARIFICATIONS) govern
# G and H. Batching is Kam's standing rule of 2026-09-18. Merges after this gate are Tuesday's GO. Deploys HELD for Kam.
#
# PATTERN: launch_qa_vision_qq_gate1.sh. CHANGES:
#   - exit 40: the PIN table is parsed from the brief; every expected row present once; IN rows fully filled (no '@'), 40-hex.
#   - exit 41: SLOT-J line vs row J vs the brief's SLOT-J section vs the prompt's [SLOT-J BEGIN] block — all consistent.
#   - exit 6/7/8: per row — commit in ITS repo; base is ancestor AND merge-base; rev-list --count == commits; base is the repo's
#     MAIN row head or another IN row's head in the same repo (stacking must be named, never implied).
#   - exit 18: EVERY row (mains included) re-read by `git ls-remote origin refs/heads/<branch>` now; refuse on mismatch.
#   - exit 22: per-target file set over its base — exact for A B C D E F I J; subset-of-allowed + required files for G and H.
#   - exit 55-59, 65-68: per-target content drift guards (strings the brief quotes, read from the pinned head).
#   - exit 63: no target changes its repo's lockfile (vs the MAIN row); both files carry the offline-install rule.
#   - exit 62: the Vision floor discipline with gate-2 database names (vsp_qa_g2_).
#   - exit 69: ntfy is never contacted (ntfy.invalid stub rule) in both files.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 45678 (%0), gate-1 QA 87320 (%43; advisory if exited).
#   - exit 24 carried: the prompt must not carry either app's literal server entry path.
#   - exit 32: SELF-CHECK timestamp and note stamped by the coordinator (LAST guard, so --check shows every other guard first).
#     Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate2' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# READ-ONLY toward both repos: only cat-file, rev-parse, merge-base, log, rev-list, diff, show, ls-remote.
# Usage: launch_qa_vision_qq_gate2.sh [--check]
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
PH_SLOTJ='@SLOT''_J@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate2-s1-s2-a1-a2.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate2-s1-s2-a1-a2.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
POLLER='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Feedback_System/2_Project_Files/packages/coordinator/poller.js'
G1_REPORT="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate1/report.md"
G5_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py"
G5_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorlib.sh"
REPORT="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate2/report.md"
NEG_SEATS='1613 45678 87320'   # Vision builder (%41), Tuesday (%0), gate-1 QA (%43) at drafting

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 2: S-1 + S-2 + portal integration (tier 1) + item 3 round 2 (tier 1) + A-1 (tier 1) + A-2..A-5 (tier 2), heads as pinned at launch'

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
EXPECT_IDS='MAIN-P MAIN-Q A B G C D E F H I J'
for ID in $EXPECT_IDS; do
  N="$(printf '%s\n' "$PIN" | awk -F'\t' -v id="$ID" '$1==id' | wc -l | tr -d ' ')"
  [ "$N" = "1" ] || { echo "REFUSING: PIN table must carry exactly one row '$ID' (found $N)" >&2; exit 40; }
done
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "12" ] || { echo "REFUSING: PIN table carries rows beyond the twelve expected ($EXPECT_IDS)" >&2; exit 40; }
row()   { printf '%s\n' "$PIN" | awk -F'\t' -v id="$1" '$1==id'; }
fld()   { row "$1" | awk -F'\t' -v n="$2" '{print $n}'; }   # 2 repo 3 branch 4 head 5 base 6 commits 7 status
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
for ID in $EXPECT_IDS; do
  R="$(row "$ID")"; ST="$(fld "$ID" 7)"
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN row $ID does not have 7 cells: $R" >&2; exit 40; }
  case "$ST" in IN|OUT) ;; *) echo "REFUSING: PIN row $ID status is '$ST' (IN or OUT only; unfilled?)" >&2; exit 40 ;; esac
  case "$ID" in MAIN-*|J) ;; *) [ "$ST" = "IN" ] || { echo "REFUSING: only row J may be OUT (row $ID is $ST)" >&2; exit 40; } ;; esac
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
for ID in A B G; do [ "$(fld "$ID" 2)" = "portal" ] || { echo "REFUSING: row $ID must be the portal repo" >&2; exit 40; }; done
for ID in C D E F H I J; do [ "$(fld "$ID" 2)" = "quickquote" ] || { echo "REFUSING: row $ID must be the quickquote repo" >&2; exit 40; }; done
exp_branch() { case "$1" in
  A) echo fix/feedback-report-auth-2026-09-22 ;; B) echo fix/reminder-push-redaction-2026-09-22 ;;
  G) echo integration/portal-gate2-2026-09-22 ;; C) echo feat/qq-otp-send-budget-2026-09-22 ;;
  D) echo feat/qq-security-headers-2026-09-22 ;; E) echo feat/qq-sign-out-2026-09-22 ;;
  F) echo fix/qq-pdf-fx-provenance-2026-09-22 ;; H) echo feat/qq-open-old-quote-2026-09-22 ;;
  I) echo fix/qq-dockerignore-2026-09-22 ;; J) echo fix/qq-typed-ps-rates-o1-2026-09-22 ;; esac; }
for ID in A B G C D E F H I J; do
  [ "$(fld "$ID" 7)" = "IN" ] || continue
  [ "$(fld "$ID" 3)" = "$(exp_branch "$ID")" ] || { echo "REFUSING: row $ID branch is '$(fld "$ID" 3)', the brief's target is '$(exp_branch "$ID")' — re-brief" >&2; exit 40; }
done
IN_IDS="$(printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" && $1!~/^MAIN-/ {print $1}' | tr '\n' ' ')"

# 41 — slot J: the SLOT-J line, row J, the brief's SLOT-J section and the prompt's block must agree.
SJ="$(grep -m1 '^SLOT-J: ' "$BRIEF" | sed 's/^SLOT-J: //')"
[ "$SJ" != "$PH_SLOTJ" ] || { echo "REFUSING: SLOT-J is unfilled — Tuesday sets IN or OUT" >&2; exit 41; }
case "$SJ" in IN|OUT) ;; *) echo "REFUSING: SLOT-J line is '$SJ' (IN or OUT only)" >&2; exit 41 ;; esac
[ "$SJ" = "$(fld J 7)" ] || { echo "REFUSING: SLOT-J says $SJ but PIN row J is $(fld J 7)" >&2; exit 41; }
HASB=0; grep -q '<!-- SLOT-J:BEGIN -->' "$BRIEF" && grep -q '<!-- SLOT-J:END -->' "$BRIEF" && HASB=1
HASP=0; grep -qF '[SLOT-J BEGIN]' "$PROMPT_FILE" && grep -qF '[SLOT-J END]' "$PROMPT_FILE" && HASP=1
if [ "$SJ" = "IN" ]; then
  [ "$HASB$HASP" = "11" ] || { echo "REFUSING: SLOT-J is IN but the brief section ($HASB) or the prompt block ($HASP) is missing" >&2; exit 41; }
  grep -q '<fill at launch>' "$BRIEF" && { echo "REFUSING: the brief still carries a '<fill at launch>' marker" >&2; exit 41; }
else
  [ "$HASB$HASP" = "00" ] || { echo "REFUSING: SLOT-J is OUT but the brief section ($HASB) or the prompt block ($HASP) is still present — delete both" >&2; exit 41; }
fi

# 6 / 7 / 8 — per IN row: commit in its repo; base ancestor AND merge-base; exact commit count; base is MAIN or a named IN head.
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; H="$(fld "$ID" 4)"
  T="$($G cat-file -t "$H" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: row $ID head $H is not a commit in its repo (got '$T') — this launcher never fetches" >&2; exit 6; }
done
for ID in $IN_IDS; do
  REPO="$(fld "$ID" 2)"; G="$(repo_fn "$REPO")"; H="$(fld "$ID" 4)"; BASE="$(fld "$ID" 5)"; N="$(fld "$ID" 6)"
  T="$($G cat-file -t "$BASE" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: row $ID base $BASE is not a commit (got '$T')" >&2; exit 6; }
  MAINH="$( [ "$REPO" = portal ] && fld MAIN-P 4 || fld MAIN-Q 4 )"
  OK=0; [ "$BASE" = "$MAINH" ] && OK=1
  for O in $IN_IDS; do [ "$O" != "$ID" ] && [ "$(fld "$O" 2)" = "$REPO" ] && [ "$(fld "$O" 4)" = "$BASE" ] && OK=1; done
  [ "$OK" = 1 ] || { echo "REFUSING: row $ID base ${BASE:0:7} is neither its repo's MAIN row nor another IN row's head — name the stack" >&2; exit 7; }
  $G merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: row $ID base ${BASE:0:7} is not an ancestor of ${H:0:7}" >&2; exit 7; }
  [ "$($G merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(row $ID base, head) is not the base" >&2; exit 7; }
  GOTN="$($G rev-list --count "${BASE}..${H}" 2>/dev/null)"
  [ "$GOTN" = "$N" ] || { echo "REFUSING: row $ID has $GOTN commits over its base, the table says $N" >&2; $G log --format='%h %s' "${BASE}..${H}" >&2; exit 8; }
done
# The main a target sits on must still be an ancestor of the repo's current MAIN row (a target cut from a stale main is flagged).
for ID in $IN_IDS; do
  REPO="$(fld "$ID" 2)"; G="$(repo_fn "$REPO")"; MAINH="$( [ "$REPO" = portal ] && fld MAIN-P 4 || fld MAIN-Q 4 )"
  $G merge-base --is-ancestor "$MAINH" "$(fld "$ID" 4)" 2>/dev/null || echo "NOTE: row $ID does not contain its repo's MAIN row ${MAINH:0:7} — it is cut from an older main; §12's merge predictions assume it" >&2
done

# 18 — RE-PIN: every row, mains included, at origin, by ls-remote, read NOW (immediately before launch).
for ID in MAIN-P MAIN-Q $IN_IDS; do
  G="$(repo_fn "$(fld "$ID" 2)")"; BR="$(fld "$ID" 3)"; H="$(fld "$ID" 4)"
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: row $ID: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-pin" >&2; printf '%s\n' "$L" >&2; exit 18; }
done
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each target's delta over its base: exact sets, or (G, H) a subset of the allowed set carrying the required files.
FS_A='BACKLOG.md
DEV-SESSION-SUMMARY.md
Reference_doc/feedback-system-overview.md
scripts/e2e-feedback-test.js
server/routes/feedback.js
test/db/feedback-auth.test.js'
FS_B='DEV-SESSION-SUMMARY.md
docker-compose.yml
server/reminders/dispatcher.js
test/db/reminder-push.test.js'
FS_C='BACKLOG.md
stage3/server.js
stage3/test/server.test.mjs'
FS_D="$FS_C"
FS_E='BACKLOG.md
stage3/strip.js
stage3/test/server.test.mjs
stage3/test/strip.test.mjs'
FS_F='BACKLOG.md
stage3/lib/pdf.js
stage3/package.json
stage3/strip.js
stage3/test/fx-provenance.mjs
stage3/test/strip.test.mjs'
FS_I='.dockerignore
BACKLOG.md
stage3/Dockerfile'
FS_J='stage3/lib/pdf.js
stage3/package.json
stage3/test/typed-rates.mjs'
ALLOW_G='BACKLOG.md
server/email/escape.test.js
server/email/escapeHtml.js
server/email/index.js
server/feedbackNotify.js
server/feedbackNotify.test.js
server/reminders/dispatcher.js
server/routes/feedback.js'
REQ_G='server/email/escapeHtml.js
server/feedbackNotify.js
server/reminders/dispatcher.js
server/email/index.js'
ALLOW_H='BACKLOG.md
CLAUDE.md
stage3/lib/pdf.js
stage3/lib/store.js
stage3/package.json
stage3/server.js
stage3/strip.js
stage3/test/server.test.mjs
stage3/test/store.test.mjs
stage3/test/strip.test.mjs'
REQ_H='stage3/server.js
stage3/lib/store.js
stage3/test/store.test.mjs'
delta() { local G; G="$(repo_fn "$(fld "$1" 2)")"; $G diff --name-only "$(fld "$1" 5)" "$(fld "$1" 4)" 2>/dev/null | sort; }
for ID in A B C D E F I J; do
  case " $IN_IDS " in *" $ID "*) ;; *) continue ;; esac
  eval "EXP=\"\$FS_$ID\""
  GOT="$(delta "$ID")"
  [ "$GOT" = "$(sorted "$EXP")" ] || { echo "REFUSING: row $ID's delta over its base is not exactly the briefed file set. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
done
for ID in G H; do
  eval "AL=\"\$ALLOW_$ID\"; RQ=\"\$REQ_$ID\""
  GOT="$(delta "$ID")"
  EXTRA="$(comm -23 <(printf '%s\n' "$GOT") <(sorted "$AL"))"
  MISS="$(comm -13 <(printf '%s\n' "$GOT") <(sorted "$RQ"))"
  [ -z "$EXTRA" ] && [ -z "$MISS" ] || { echo "REFUSING: row $ID's delta: files outside the briefed set [$EXTRA] / required files missing [$MISS]" >&2; exit 22; }
done

# Content drift guards: the strings the brief quotes, read from each pinned head (never a checkout).
has() { # row path fixed-string
  local G; G="$(repo_fn "$(fld "$1" 2)")"
  $G show "$(fld "$1" 4):$2" 2>/dev/null | grep -qF -- "$3"
}
# 55 — A (S-1)
for S in 'function requireSessionOrCoordinator(req, res, next) {' "router.get('/report', requireSessionOrCoordinator," \
         "router.get('/summary', requireSessionOrCoordinator," 'return a.length === b.length && crypto.timingSafeEqual(a, b);'; do
  has A server/routes/feedback.js "$S" || { echo "REFUSING: A's feedback.js lacks: $S — re-brief" >&2; exit 55; }
done
p show "$(fld MAIN-P 4):server/routes/feedback.js" 2>/dev/null | grep -qF "router.get('/report', requireSessionOrCoordinator," \
  && { echo "REFUSING: portal MAIN already carries S-1's gate — A has merged; re-brief" >&2; exit 55; }
has A .cursor/rules/check-feedback-workflow.mdc 'curl -s http://localhost:4848/api/feedback/report' \
  && has A .cursor/rules/check-feedback-workflow.mdc 'curl -s https://datasec-sales-portal.azurewebsites.net/api/feedback/report' \
  || { echo "REFUSING: the .cursor break-list lines the brief quotes are not at A's head — re-brief" >&2; exit 55; }
[ "$(sed -n 43p "$POLLER" 2>/dev/null | sed 's/^[[:space:]]*//')" = 'const resp = await fetch(project.feedbackUrl, fetchOptions);' ] \
  || echo "NOTE: Feedback_System poller.js:43 is no longer the header-less fetch the brief quotes (not a git repo; it drifts) — the gate re-reads it" >&2
# 56 — B (S-2), and item 4's escaping kept on B when B sits on G
has B server/reminders/dispatcher.js 'title: `Reminder #${rem.id} due`,' \
  && has B server/reminders/dispatcher.js "body: 'Open the Vision Sales Portal (PRO dashboard → Reminders) to read it.'," \
  && has B server/reminders/dispatcher.js 'result = await sendNtfy(push.title, push.body);' \
  && has B docker-compose.yml 'NTFY_TOPIC: ${NTFY_TOPIC:-}' || { echo "REFUSING: B's redaction / compose default is not what the brief quotes — re-brief" >&2; exit 56; }
if [ "$(fld B 5)" = "$(fld G 4)" ]; then
  has B server/reminders/dispatcher.js 'escapeHtml(rem.body || rem.title)' || { echo "REFUSING: B sits on G but its dispatcher lost item 4's escapeHtml — the rebase dropped the fix" >&2; exit 56; }
else
  echo "NOTE: B's base is not G's head — the brief expects S-2 rebased onto the integration branch; §4 Q2/Q7 assume it" >&2
fi
# 57 — G (portal integration)
[ "$(p cat-file -t "$(fld G 4):server/email/escapeHtml.js" 2>/dev/null)" = "blob" ] \
  && has G server/reminders/dispatcher.js 'escapeHtml(rem.body || rem.title)' \
  && has G server/email/index.js '<pre>${escapeHtml(text)}</pre>' \
  && has G server/feedbackNotify.js "kreiser.org@me.com,tuesday-agent@agentmail.to" \
  && has G server/routes/feedback.js 'notifyFeedback(' || { echo "REFUSING: G does not carry both item 4 (escapeHtml helper, dispatcher, fallback) and item 1 (feedbackNotify, route call) — re-brief" >&2; exit 57; }
# 58 — C (A-1)
for S in 'const OTP_IP_BUDGET_PER_HOUR = 6;' 'const OTP_GLOBAL_BUDGET_PER_HOUR = 20;' 'trustForwardedFor = !!process.env.WEBSITE_SITE_NAME' \
         'too many sign-in codes requested from your network — try again later' 'sign-in is busy right now — try again in a few minutes'; do
  has C stage3/server.js "$S" || { echo "REFUSING: C's server lacks: $S — re-brief" >&2; exit 58; }
done
# 59 — D (A-2)
for S in "\"frame-ancestors 'none'\"," "\"script-src 'self' 'unsafe-inline'\"," '"Cache-Control": "no-store",' '"X-Frame-Options": "DENY",'; do
  has D stage3/server.js "$S" || { echo "REFUSING: D's headers lack: $S — re-brief" >&2; exit 59; }
done
# 65 — E (A-3): both strings, the POST, and the offline file carries no button (presence control on strip.js)
for S in 'b.textContent = "Sign out";' 'b.textContent = "Sign-out failed — retry";' 'const r = await fetch("/auth/logout", { method: "POST" });'; do
  has E stage3/strip.js "$S" || { echo "REFUSING: E's strip.js lacks: $S — re-brief" >&2; exit 65; }
done
has E index.html 'btnSignOut' && { echo "REFUSING: E's offline index.html carries btnSignOut — the brief says the offline file has none" >&2; exit 65; }
# 66 — F (A-4)
has F stage3/lib/pdf.js '/^[0-9A-Za-z ,:-]{1,32}$/.test(String(fx.date || ""))' \
  && has F stage3/lib/pdf.js 'module.exports = { renderQuotePdf, closeBrowser };' \
  && has F stage3/package.json 'test/fx-provenance.mjs' || { echo "REFUSING: F's bound regex / closeBrowser / test:print wiring is not what the brief quotes — re-brief" >&2; exit 66; }
# 67 — H (item 3 round 2): the purge, the four minors, the regex, the creator check
for S in 'const SERVER_QNUM_RE = /^DSQ-\d{8}-\d{6}-H\d{2}$/;' 'app.purgeQuotes = async () => {' 'const QUOTE_STATE_MAX_CHARS = 30000;' \
         'const REOPEN_MAX = 30, REOPEN_WINDOW_MS = 10 * 60 * 1000;' 'if (row.creator !== req.session.email) return notFound();'; do
  has H stage3/server.js "$S" || { echo "REFUSING: H's server lacks: $S — re-brief" >&2; exit 67; }
done
has H stage3/strip.js 'It could not be saved for reopening later, so keep the email.' || { echo "REFUSING: H's stored:false note is not the quoted string — re-brief" >&2; exit 67; }
python3 - "$(q show "$(fld H 4):stage3/server.js" 2>/dev/null | cat)" <<'PY' || { echo "REFUSING: in H the creator check does not precede the retention delete (the C-F2 fix the brief describes)" >&2; exit 67; }
import sys
s = sys.argv[1]
i = s.find('app.get("/api/quote/:qnum"')
c = s.find('if (row.creator !== req.session.email) return notFound();', i)
d = s.find('await store.deleteQuote(qnum);', i)
sys.exit(0 if i >= 0 and 0 <= c < d else 1)
PY
# 68 — I (A-5) and J (O-1)
q show "$(fld I 4):.dockerignore" 2>/dev/null | grep -qx '\*\*/node_modules' && has I stage3/Dockerfile 'RUN npm ci --omit=dev' \
  || { echo "REFUSING: I's .dockerignore / Dockerfile is not what the brief quotes — re-brief" >&2; exit 68; }
if [ "$SJ" = "IN" ]; then
  has J stage3/lib/pdf.js 'const first = ["currency", "fxRate"].filter(id => pass3.includes(id));' && has J stage3/package.json 'test/typed-rates.mjs' \
    || { echo "REFUSING: J's pass-3 ordering / test wiring is not what the brief quotes — re-brief" >&2; exit 68; }
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

# 31 — the settled-decisions file and gate 1's report (the PRIOR ROUND for G and H) are on disk and named.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-05.'; do grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief relies on it" >&2; exit 31; }; done
[ -s "$G1_REPORT" ] || { echo "REFUSING: gate 1's report is absent: $G1_REPORT — G and H are its round 2" >&2; exit 31; }
grep -qF "$(dirname "$G1_REPORT")" "$BRIEF" || { echo "REFUSING: the brief does not name gate 1's report path (PRIOR ROUND)" >&2; exit 31; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 31; }

# 39 — the floor instrument the brief names is on disk.
[ -s "$G5_FLOOR" ] && [ -s "$G5_FLOORLIB" ] || { echo "REFUSING: gate 5's floor instrument missing: $G5_FLOOR / $G5_FLOORLIB" >&2; exit 39; }
grep -qF "$G5_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G5_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
for T in 'A (S-1, feedback report auth) is TIER 1' 'B (S-2, reminder push redaction) is TIER 1' 'C (A-1, sign-in-code budgets) is TIER 1' \
         'D (A-2, security headers) is TIER 2' 'E (A-3, sign out) is TIER 2' 'F (A-4, PDF FX provenance) is TIER 2' \
         'G (portal integration: main + gate-1 item 4 + item 1' 'H (item 3, reopen by number, ROUND 2 of 2' 'I (A-5, `.dockerignore`' 'J (O-1,'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare: $T" >&2; exit 12; }
done
for T in 'TARGET A — S-1 (TIER 1' 'TARGET B — S-2 (TIER 1' 'TARGET C — A-1 (TIER 1' 'TARGET D — A-2 (TIER 2' 'TARGET E — A-3 (TIER 2' \
         'TARGET F — A-4 (TIER 2' 'TARGET G — portal integration main + item 4 + item 1 (TIER 1' 'TARGET H — item 3 ROUND 2 (TIER 1' 'TARGET I — A-5 (TIER 2'; do
  grep -qF -- "$T" "$PROMPT_FILE" || { echo "REFUSING: prompt does not declare: $T" >&2; exit 12; }
done
[ "$SJ" = "OUT" ] || grep -qF 'TARGET J — O-1 (TIER 1' "$PROMPT_FILE" || { echo "REFUSING: prompt's slot J block does not declare TARGET J — O-1 (TIER 1" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
grep -q '@[A-Z_]*@' "$PROMPT_FILE" && { echo "REFUSING: the prompt carries a placeholder — placeholders belong in the brief only" >&2; exit 14; }
grep -q 'appended the verified table' "$PROMPT_FILE" || { echo "REFUSING: prompt must tell the agent the verified PIN table is appended" >&2; exit 14; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-Vision has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="SEPARATELY%PER%TARGET ADVERSARIAL%PASS LEGITIMATE%SHAPES NEGATIVE BYTE-IDENTICAL READ%THE%ROW range-diff Sign-out%failed%—%retry pdftotext BEFORE%and%AFTER timingSafeEqual X-Coordinator-Secret BREAK%LIST ntfy.invalid X-Forwarded-For /64 'unsafe-inline' Max-Age=0 file:// fxState CONFIG.fxProviders exits%on%its%own ENOTCACHED dispatchDue PARSED stored:false .dockerignore F8's%single-rate%invariant merge-tree NOT%TESTED env%-i EGRESS%INCLUDING%CHROME%CHILDREN"
for w in $WORDS; do
  w="${w//%/ }"
  grep -qF -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES" >&2; exit 19; }
for T in A C F H; do
  grep -q "ADVERSARIAL PASS ($T)" "$BRIEF" || { echo "REFUSING: brief lacks ADVERSARIAL PASS ($T)" >&2; exit 19; }
done
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
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, gate-2 DBs.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g2_' "$FL" && grep -q 'vsp_qa_g1_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g2_ DBs and never vsp_qa_g1_, no jest lock)" >&2; exit 62; }
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
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — the portal runtime legs (A, B, G) will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (40 41 6 7 8 18 22 55 56 57 58 59 65 66 67 68 63 31 39 10 17 12 13 14 15 20 19 24 53 60 61 62 64 69 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# The verified PIN table, appended to the agent's prompt.
PIN_BLOCK="$(printf 'PINNED HEADS — verified by the launcher at %s (cat-file, base ancestry and merge-base, commit count, and git ls-remote origin for every row):\n' "$PIN_TS"
  printf '%s\n' "$PIN" | awk -F'\t' '$7=="IN" { printf "  %-7s %-11s %-42s %s  base %s  commits %s\n", $1, $2, $3, $4, ($5=="-"?"-":substr($5,1,12)), $6 }'
  [ "$SJ" = "OUT" ] && printf '  J is OUT: no slot J in this gate.\n')"

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  printf '%s\n' "$PIN_BLOCK"
  echo "  PIN parsed from the brief (40); SLOT-J $SJ consistent (41); commits, bases, counts (6 7 8); origin re-read $PIN_TS (18); file sets (22)"
  echo "  content: A S-1 (55) B S-2 (56) G integration (57) C budgets (58) D headers (59) E sign-out (65) F provenance (66) H round 2 (67) I/J (68)"
  echo "  lockfiles unchanged vs mains (63); CLARIFICATIONS + gate-1 report (31); floor instrument (39); report absent (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); directive (13); brief + no prompt placeholders (14); mail (15); key absolute + question route (20); words (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); ntfy/FX egress (69); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate2-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
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
