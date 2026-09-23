#!/bin/bash
# launch_qa_vision_qq_gate1.sh — cross-project QA agent, ONE BATCHED gate (Vision/QuickQuote gate 1, 2026-09-22) on
# Datasec/Vision_Sales_Portal, TWO repos:
#   TARGET A — item 1, feedback CCs Tuesday. TIER 2.
#              A1 QuickQuote fix/qq-feedback-cc-tuesday-2026-09-22 @ bd3e3cf, one commit off QQ main 47eb533.
#              A2 portal     fix/feedback-mail-cc-tuesday-2026-09-22 @ ce01ba9, one commit off portal main ef5a9c0.
#   TARGET B — item 2, Devices (MFPs/SFPs). TIER 2. QuickQuote fix/qq-mfp-sfp-label-2026-09-22 @ 72f6c0c, off 47eb533.
#   TARGET C — item 3, reopen an old quote by number, creator only. TIER 1. QuickQuote feat/qq-open-old-quote-2026-09-22
#              @ 642b06b, off 47eb533.
#   TARGET D — item 4, portal mail HTML escaping. TIER 1. Portal fix/mail-html-escape-2026-09-22 @ d11eed6 (fix a68b53a,
#              then a BACKLOG-only commit), off ef5a9c0.
#   All heads are KNOWN at drafting — no environment pin. Each is re-read by ls-remote right before launch (18).
#
# AUTHORITY: READY FOR QA from the Vision_Sales_Portal agent: item 1 2026-09-22T08:21:17Z, item 2 08:22:58Z, item 3 08:33:17Z,
# item 4 08:40:37Z. Kam's C-01/C-02 (feedback CC, start now) and Tuesday's C-05 ruling (creator only) in Vision's
# CLARIFICATIONS.md. Batching is Kam's standing rule of 2026-09-18. Merges after this gate are Tuesday's GO. Deploys HELD for Kam.
#
# PATTERN: launch_qa_nexusai_gate6_rd619_rd607_pr31.sh (there is no earlier Vision/QuickQuote gate launcher). CHANGES:
#   - TWO repos: every git guard names its repo (q = QuickQuote, p = portal).
#   - NO jest lock on this project (Vision has none; the NexusAI lock is NOT borrowed). Guard 59 is replaced by 62: the
#     brief and prompt carry the Vision port/Postgres/env -i discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY).
#   - exit 55: B is EXACTLY the two index.html lines (label, toolVersion 2.30 -> 2.31) + the root test file.
#   - exit 56: A — both repos' default recipient list is 'kreiser.org@me.com,tuesday-agent@agentmail.to', under the
#     variable names the brief records (QQ FEEDBACK_NOTIFY_EMAIL, portal FEEDBACK_NOTIFY_EMAILS).
#   - exit 57: C — the server regex, the creator-only route and the allowlist are present, and the allowlist names none of
#     the margin / word / feedback-draft / FX ids (a drift guard on what the brief describes, not a test).
#   - exit 58: D — the helper exists at D, the dispatcher escapes at D, and main still carries the unescaped line the
#     brief calls LIVE (presence controls both ways).
#   - exit 63: no target changes a lockfile, and both files carry the offline-install rule. The builders' node_modules
#     vs the gated lockfiles is ADVISORY (they moved during drafting: 18:41 matched, 18:50 did not).
#   - exit 64: prod hosts named as NEVER in both files; the launcher UNSETS every product/provider variable before exec.
#   - exit 11: AZURE_CONFIG_DIR / GH_CONFIG_DIR point at fresh EMPTY dirs — this gate needs neither, and an inherited
#     identity is how a local gate reaches datasec-sales-portal-rg. CLAUDE_CONFIG_DIR pinned to Tuesday's project store.
#   - exit 38: negative-control seats Vision 1613 (%41), Tuesday 63076 (%0).
#   - exit 24 carried: the prompt must not carry either app's literal server entry path.
#   - exit 32: SELF-CHECK timestamp and note placeholders stamped by the coordinator before launch (LAST guard, so --check
#     shows every other guard first). Placeholder comparands are BUILT BY CONCATENATION so a sed of the placeholder text
#     cannot reach them.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/Vision-gate1' "bash '<this file>'"), NEVER nohup.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_vision_qq_gate1.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..64 a guard refused
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
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate1-feedback-label-reopen.md"
PROMPT_FILE="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_vision-qq-gate1-feedback-label-reopen.prompt.txt"
VSP='/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal'
QQ_REPO="$VSP/Quoting Tool/hpas-quoting-tool"
P_REPO="$VSP/2_Project_Files"
CLAR="$VSP/1_Project_Definition/CLARIFICATIONS.md"
G5_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorcount.py"
G5_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate5-rd615-rd616/evidence/qa-floorlib.sh"
REPORT="$QA_DIR/projects/vision/reports/2026-09-22-vision-qq-gate1/report.md"

QQ_MAIN='47eb533034108c5c92d6b36af44554528ffc71ec'
P_MAIN='ef5a9c0b942c71b8c3b08feec22ae23dbe622581'
# Target A
A1_BRANCH='fix/qq-feedback-cc-tuesday-2026-09-22'
A1_HEAD="${QA_A1_HEAD_OVERRIDE:-bd3e3cf730cfda7d29c74c389e46c8c9d62b2005}"
A1_FILES='stage3/lib/mail.js
stage3/package.json
stage3/server.js
stage3/test/mail.test.mjs
stage3/test/server.test.mjs'
A2_BRANCH='fix/feedback-mail-cc-tuesday-2026-09-22'
A2_HEAD="${QA_A2_HEAD_OVERRIDE:-ce01ba95fa9e074f0e5ed8d4e429600cf0eadb24}"
A2_FILES='BACKLOG.md
server/email/index.js
server/feedbackNotify.js
server/feedbackNotify.test.js
server/routes/feedback.js'
A_DEFAULT='kreiser.org@me.com,tuesday-agent@agentmail.to'
# Target B
B_BRANCH='fix/qq-mfp-sfp-label-2026-09-22'
B_HEAD="${QA_B_HEAD_OVERRIDE:-72f6c0cc93d52da98ca2205496522b9d82875b26}"
B_FILES='index.html
quote-engine.test.mjs'
# Target C
C_BRANCH='feat/qq-open-old-quote-2026-09-22'
C_HEAD="${QA_C_HEAD_OVERRIDE:-642b06b4857155cdfdadab2228aad751fb45ce44}"
C_FILES='BACKLOG.md
CLAUDE.md
stage3/lib/pdf.js
stage3/lib/store.js
stage3/server.js
stage3/strip.js
stage3/test/server.test.mjs'
# Target D
D_BRANCH='fix/mail-html-escape-2026-09-22'
D_HEAD="${QA_D_HEAD_OVERRIDE:-d11eed6af2bbb8b96e1985d26da8eccf5205612b}"
D_FIX='a68b53a600c301a045ec83d00a90ca02c70308b8'
D_CHAIN='d11eed6af2bbb8b96e1985d26da8eccf5205612b
a68b53a600c301a045ec83d00a90ca02c70308b8'
D_FILES='BACKLOG.md
server/email/escape.test.js
server/email/escapeHtml.js
server/email/index.js
server/reminders/dispatcher.js'
D_FIX_FILES='server/email/escape.test.js
server/email/escapeHtml.js
server/email/index.js
server/reminders/dispatcher.js'
NEG_SEATS='1613 63076'   # Vision builder (%41), Tuesday (%0) at drafting

SUBJECT='[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision/QuickQuote gate 1: item 1 @ bd3e3cf + ce01ba9 (tier 2) + item 2 @ 72f6c0c (tier 2) + item 3 @ 642b06b (tier 1) + item 4 @ d11eed6 (tier 1)'

q() { git --no-optional-locks -C "$QQ_REPO" "$@"; }
p() { git --no-optional-locks -C "$P_REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }

[ -d "$QA_DIR" ]      || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]       || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ] || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
for R in "$QQ_REPO" "$P_REPO"; do
  [ -d "$R/.git" ] || [ -f "$R/.git" ] || { echo "repo under test missing: $R" >&2; exit 5; }
done

# 6 — every pinned sha is a commit in ITS repo's object store.
for S in $QQ_MAIN $A1_HEAD $B_HEAD $C_HEAD; do
  T="$(q cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in QuickQuote (got '$T') — this launcher never fetches" >&2; exit 6; }
done
for S in $P_MAIN $A2_HEAD $D_HEAD $D_FIX; do
  T="$(p cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in the portal (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — per target: base is ancestor AND merge-base; base..head is EXACTLY the chain; parents exact.
check_chain() { # repo-fn label base head chain
  local G="$1" L="$2" BASE="$3" H="$4" C="$5" GOTC
  $G merge-base --is-ancestor "$BASE" "$H" 2>/dev/null || { echo "REFUSING: $BASE is not an ancestor of $L $H" >&2; exit 7; }
  [ "$($G merge-base "$BASE" "$H" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base($BASE, $L) is not $BASE" >&2; exit 7; }
  GOTC="$($G log --format=%H "${BASE}..${H}" 2>&1)"
  [ "$GOTC" = "$C" ] || { echo "REFUSING: ${BASE:0:7}..$L is not exactly the commissioned chain. Got:" >&2; printf '%s\n' "$GOTC" >&2; exit 8; }
}
parents_are() { # repo-fn commit expected-parents...
  local G="$1" c="$2"; shift 2
  local GOT; GOT="$($G log -1 --format='%H %P' "$c" 2>/dev/null)"
  [ "$GOT" = "$c $*" ] || { echo "REFUSING: parents of $c are '${GOT#* }', not '$*'" >&2; exit 8; }
}
check_chain q A1 "$QQ_MAIN" "$A1_HEAD" "$A1_HEAD"; parents_are q "$A1_HEAD" "$QQ_MAIN"
check_chain q B  "$QQ_MAIN" "$B_HEAD"  "$B_HEAD";  parents_are q "$B_HEAD"  "$QQ_MAIN"
check_chain q C  "$QQ_MAIN" "$C_HEAD"  "$C_HEAD";  parents_are q "$C_HEAD"  "$QQ_MAIN"
check_chain p A2 "$P_MAIN"  "$A2_HEAD" "$A2_HEAD"; parents_are p "$A2_HEAD" "$P_MAIN"
check_chain p D  "$P_MAIN"  "$D_HEAD"  "$D_CHAIN"; parents_are p "$D_FIX" "$P_MAIN"; parents_are p "$D_HEAD" "$D_FIX"

# 18 — RE-PIN: every head at origin, by ls-remote, read NOW (immediately before launch).
repin() { # repo-fn branch head
  local G="$1" BR="$2" H="$3" L
  L="$($G ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: $H is not at refs/heads/$BR on origin — that head moved or was never pushed; re-brief" >&2; printf '%s\n' "$L" >&2; exit 18; }
}
repin q "$A1_BRANCH" "$A1_HEAD"; repin q "$B_BRANCH" "$B_HEAD"; repin q "$C_BRANCH" "$C_HEAD"
repin p "$A2_BRANCH" "$A2_HEAD"; repin p "$D_BRANCH" "$D_HEAD"

# 22 — each target's delta over its base is EXACTLY its commissioned file set.
chk_files() { # repo-fn label base head expected
  local GOT; GOT="$($1 diff --name-only "$3" "$4" 2>/dev/null | sort)"
  [ "$GOT" = "$(sorted "$5")" ] || { echo "REFUSING: $2's delta over ${3:0:7} is not exactly the commissioned files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
}
chk_files q A1 "$QQ_MAIN" "$A1_HEAD" "$A1_FILES"
chk_files q B  "$QQ_MAIN" "$B_HEAD"  "$B_FILES"
chk_files q C  "$QQ_MAIN" "$C_HEAD"  "$C_FILES"
chk_files p A2 "$P_MAIN"  "$A2_HEAD" "$A2_FILES"
chk_files p D  "$P_MAIN"  "$D_HEAD"  "$D_FILES"
# 50 — D's per-commit file sets: the fix is the four code/test files, the head commit is BACKLOG.md only.
[ "$(p diff --name-only "$D_FIX^" "$D_FIX" 2>/dev/null | sort)" = "$(sorted "$D_FIX_FILES")" ] || { echo "REFUSING: ${D_FIX:0:7} file set is not the four escaping files" >&2; exit 50; }
[ "$(p diff --name-only "$D_FIX" "$D_HEAD" 2>/dev/null)" = "BACKLOG.md" ] || { echo "REFUSING: ${D_HEAD:0:7} is not BACKLOG-only over ${D_FIX:0:7}" >&2; exit 50; }

# 55 — B is EXACTLY the label line and the version line in index.html, plus the root test file (+12/-0).
NS="$(q diff --numstat "$QQ_MAIN" "$B_HEAD" 2>/dev/null | sort)"
[ "$NS" = "$(printf '2\t2\tindex.html\n12\t0\tquote-engine.test.mjs\n' | sort)" ] || { echo "REFUSING: B's numstat is not index.html 2/2 + quote-engine.test.mjs 12/0 (got: $NS)" >&2; exit 55; }
MINUS="$(q diff -U0 "$QQ_MAIN" "$B_HEAD" -- index.html 2>/dev/null | grep -E '^-[^-]' | sed 's/^-[[:space:]]*//' | sort)"
PLUS="$(q diff -U0 "$QQ_MAIN" "$B_HEAD" -- index.html 2>/dev/null | grep -E '^\+[^+]' | sed 's/^+[[:space:]]*//' | sort)"
[ "$MINUS" = "$(printf '%s\n%s' '<label for="devices">Devices (MFPs)</label>' 'toolVersion: "2.30",' | sort)" ] \
  && [ "$PLUS" = "$(printf '%s\n%s' '<label for="devices">Devices (MFPs/SFPs)</label>' 'toolVersion: "2.31",' | sort)" ] || {
  echo "REFUSING: B's index.html lines are not exactly the label and 2.30 -> 2.31 (got -[$MINUS] +[$PLUS])" >&2; exit 55; }

# 56 — A: both repos default to Kam + Tuesday, under the variable names the brief records.
A1_SRC="$(q show "$A1_HEAD:stage3/server.js" 2>/dev/null)"
A2_SRC="$(p show "$A2_HEAD:server/feedbackNotify.js" 2>/dev/null)"
[ -n "$A1_SRC" ] && [ -n "$A2_SRC" ] || { echo "REFUSING: A's sources unreadable — guard 56 would be vacuous" >&2; exit 56; }
printf '%s\n' "$A1_SRC" | grep -qF "const DEFAULT_FEEDBACK_NOTIFY = \"$A_DEFAULT\";" \
  && printf '%s\n' "$A1_SRC" | grep -qF 'process.env.FEEDBACK_NOTIFY_EMAIL || DEFAULT_FEEDBACK_NOTIFY' \
  && printf '%s\n' "$A2_SRC" | grep -qF "const DEFAULT_FEEDBACK_NOTIFY = '$A_DEFAULT';" \
  && printf '%s\n' "$A2_SRC" | grep -qF 'env.FEEDBACK_NOTIFY_EMAILS || DEFAULT_FEEDBACK_NOTIFY' || {
  echo "REFUSING: A's default recipients or variable names are not what the brief records (QQ FEEDBACK_NOTIFY_EMAIL, portal FEEDBACK_NOTIFY_EMAILS, '$A_DEFAULT'); re-brief" >&2; exit 56; }

# 57 — C: server regex, creator-only route, and an allowlist that names no margin / word / draft / FX id.
C_SRC="$(q show "$C_HEAD:stage3/server.js" 2>/dev/null)"
[ -n "$C_SRC" ] || { echo "REFUSING: C's server unreadable — guard 57 would be vacuous" >&2; exit 57; }
printf '%s\n' "$C_SRC" | grep -qF 'const SERVER_QNUM_RE = /^DSQ-\d{8}-\d{6}-H\d{2}$/;' \
  && printf '%s\n' "$C_SRC" | grep -qF 'app.get("/api/quote/:qnum", requireAuth,' \
  && printf '%s\n' "$C_SRC" | grep -qF 'if (row.creator !== req.session.email) return notFound();' \
  && printf '%s\n' "$C_SRC" | grep -qF 'quoteRetentionDays = process.env.QUOTE_RETENTION_DAYS || 365' || {
  echo "REFUSING: C's server does not carry the number regex / creator-only route / creator check / retention setting the brief describes; re-brief" >&2; exit 57; }
ALLOW="$(printf '%s\n' "$C_SRC" | awk '/^const QUOTE_FIELD_IDS = \[/,/\];/' ; printf '%s\n' "$C_SRC" | awk '/^const QUOTE_CHECK_IDS = \[/,/\];/')"
[ -n "$ALLOW" ] || { echo "REFUSING: C's allowlists not found — guard 57 would be vacuous" >&2; exit 57; }
if printf '%s\n' "$ALLOW" | grep -q -i -E '"(cp[A-Za-z]+|advWord|fbMsg|fxRate|psv[A-Za-z]+|margin|buyPrice)"'; then
  echo "REFUSING: C's stored allowlist names a margin / HPAM-word / feedback-draft / FX / PS-rate id — the brief says it does not; re-brief" >&2; exit 57
fi

# 58 — D: the helper and the escaped dispatcher line at D; main still carries the LIVE unescaped line (presence controls).
[ "$(p cat-file -t "$D_HEAD:server/email/escapeHtml.js" 2>/dev/null)" = "blob" ] || { echo "REFUSING: escapeHtml.js absent at D" >&2; exit 58; }
p show "$D_HEAD:server/reminders/dispatcher.js" 2>/dev/null | grep -qF 'escapeHtml(rem.body || rem.title)' || { echo "REFUSING: D's dispatcher does not escape rem.body/title as briefed" >&2; exit 58; }
p show "$D_HEAD:server/email/index.js" 2>/dev/null | grep -qF '<pre>${escapeHtml(text)}</pre>' || { echo "REFUSING: D's text-only fallback is not escapeHtml(text) as briefed" >&2; exit 58; }
p show "$P_MAIN:server/reminders/dispatcher.js" 2>/dev/null | grep -qF '<p>${rem.body || rem.title}</p>' || { echo "REFUSING: main's dispatcher no longer carries the unescaped line the brief calls LIVE — re-brief" >&2; exit 58; }

# 63 — no target changes a lockfile; the builders' installed node_modules match the gated lockfile entry by entry.
QL="$(q rev-parse "$QQ_MAIN:stage3/package-lock.json" 2>/dev/null)"
for S in $A1_HEAD $B_HEAD $C_HEAD; do
  [ -n "$QL" ] && [ "$(q rev-parse "$S:stage3/package-lock.json" 2>/dev/null)" = "$QL" ] || { echo "REFUSING: stage3/package-lock.json differs at $S — a target changes dependencies; re-brief" >&2; exit 63; }
done
PL="$(p rev-parse "$P_MAIN:package-lock.json" 2>/dev/null)"
for S in $A2_HEAD $D_HEAD; do
  [ -n "$PL" ] && [ "$(p rev-parse "$S:package-lock.json" 2>/dev/null)" = "$PL" ] || { echo "REFUSING: package-lock.json differs at $S — a target changes dependencies; re-brief" >&2; exit 63; }
done
nm_match() { # repo sha subdir-prefix
  python3 - "$1" "$2" "$3" <<'PY'
import json, subprocess, sys
repo, sha, pfx = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    lock = json.loads(subprocess.check_output(['git', '--no-optional-locks', '-C', repo, 'show', f'{sha}:{pfx}package-lock.json']))['packages']
    nm = json.load(open(f'{repo}/{pfx}node_modules/.package-lock.json'))['packages']
except Exception as e:
    print(f'unreadable: {e}'); sys.exit(1)
L = {k: v.get('version') for k, v in lock.items() if k.startswith('node_modules/')}
N = {k: v.get('version') for k, v in nm.items() if k.startswith('node_modules/')}
bad = [k for k in sorted(set(L) | set(N)) if L.get(k) != N.get(k)]
if not L or bad:
    print(f'{len(L)} locked / {len(N)} installed, {len(bad)} mismatched: {bad[:8]}'); sys.exit(1)
print(f'{len(L)}/{len(N)} match')
PY
}
# ADVISORY, not a refusal: the builders' installed trees moved during drafting (18:41 matched, 18:50 did not), and the
# brief's sanctioned install is `npm ci --offline --ignore-scripts` in the gate's own tree — so a mismatch only means the
# builder's tree cannot be copied. The refusal is on the RULE being absent from the two files.
NM_QQ="$(nm_match "$QQ_REPO" "$QQ_MAIN" 'stage3/')" || echo "NOTE: QuickQuote stage3/node_modules is not the gated set ($NM_QQ) — the gate must use npm ci --offline, not a copy" >&2
NM_P="$(nm_match "$P_REPO" "$P_MAIN" '')" || echo "NOTE: portal node_modules is not the gated set ($NM_P) — the gate must use npm ci --offline, not a copy" >&2
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'npm ci --offline --ignore-scripts' "$FL" && grep -q 'entry by entry' "$FL" || {
    echo "REFUSING: $FL lacks the dependency rule (npm ci --offline --ignore-scripts; node_modules proven against the gated lockfile entry by entry)" >&2; exit 63; }
done

# 31 — the settled-decisions file and the rulings the brief quotes are on disk.
[ -s "$CLAR" ] || { echo "REFUSING: Vision CLARIFICATIONS.md absent: $CLAR" >&2; exit 31; }
for C in 'C-01.' 'C-04.' 'C-05.'; do
  grep -qF "**$C" "$CLAR" || { echo "REFUSING: $CLAR lacks $C — the brief quotes it" >&2; exit 31; }
done

# 39 — gate 5's floor instrument, which the brief names as the method, is on disk.
[ -s "$G5_FLOOR" ] && [ -s "$G5_FLOORLIB" ] || { echo "REFUSING: gate 5's floor instrument missing: $G5_FLOOR / $G5_FLOORLIB" >&2; exit 39; }
grep -qF "$G5_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G5_FLOOR" >&2; exit 39; }

grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
grep -qF "$REPORT" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the report path $REPORT" >&2; exit 10; }
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }

# 12 — tiers declared in both files.
grep -q 'A (item 1, feedback CC) is TIER 2' "$BRIEF" && grep -q 'B (item 2, label) is TIER 2' "$BRIEF" \
  && grep -q 'C (item 3, reopen by number) is TIER 1' "$BRIEF" && grep -q 'D (item 4, mail HTML escaping) is TIER 1' "$BRIEF" \
  && grep -q 'TARGET A — item 1 (TIER 2' "$PROMPT_FILE" && grep -q 'TARGET B — item 2 (TIER 2' "$PROMPT_FILE" \
  && grep -q 'TARGET C — item 3 (TIER 1' "$PROMPT_FILE" && grep -q 'TARGET D — item 4 (TIER 1' "$PROMPT_FILE" || {
  echo "REFUSING: brief and prompt do not both declare A 'TIER 2', B 'TIER 2', C 'TIER 1', D 'TIER 1'" >&2; exit 12; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
grep -qF "$BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt must name the brief path" >&2; exit 14; }
for S in $QQ_MAIN $P_MAIN $A1_HEAD $A2_HEAD $B_HEAD $C_HEAD $D_HEAD $D_FIX; do
  grep -qF "$S" "$PROMPT_FILE" && grep -qF "$S" "$BRIEF" || { echo "REFUSING: prompt and brief must both name $S" >&2; exit 14; }
done
if grep -qF "$PH_SCTS" "$PROMPT_FILE" || grep -qF "$PH_SCNOTE" "$PROMPT_FILE"; then echo "REFUSING: the prompt carries a self-check placeholder — it belongs in the brief only" >&2; exit 14; fi
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -q 'tuesday-agent@agentmail.to' "$PROMPT_FILE" \
  && grep -qF "$SUBJECT" "$PROMPT_FILE" && grep -qF "$SUBJECT" "$BRIEF" || {
  echo "REFUSING: prompt must say MAIL YOUR VERDICT and name tuesday-agent@agentmail.to; prompt and brief must carry the verdict subject" >&2; exit 15; }
grep -qF '/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env' "$PROMPT_FILE" || { echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20; }
grep -q 'QUESTION: <topic>' "$PROMPT_FILE" && grep -qi 'no inbox routing line' "$PROMPT_FILE" || { echo "REFUSING: prompt must say QA/Datasec-Vision has no inbox routing line and how to ask (QUESTION: <topic>, proceed on the safest reading)" >&2; exit 20; }
WORDS="FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS FAKE%provider failing%mailbox BYTE-IDENTICAL READ%THE%ROW QUOTE_RETENTION_DAYS H01..H99 503 ADVANCED price-custom enumeration timing session%fixation IDOR Retention%honesty a68b53a PARSING sendEmail javascript: data: double-escaping LEGITIMATE%SHAPES NOT%TESTED SEPARATELY%PER%TARGET merge-tree print%as%a%real%PDF MFPs/SFPs env%-i"
for w in $WORDS; do
  w="${w//%/ }"
  grep -q -- "$w" "$PROMPT_FILE" || { echo "REFUSING: prompt must carry '$w'" >&2; exit 19; }
done
grep -q 'RULED BY KAM, AND SETTLED' "$BRIEF" || { echo "REFUSING: brief lacks the RULED BY KAM section" >&2; exit 19; }
grep -q '^## PRIOR ROUND' "$BRIEF" || { echo "REFUSING: brief lacks the PRIOR ROUND section" >&2; exit 19; }
grep -q '^## 2a. LEGITIMATE SHAPES' "$BRIEF" || { echo "REFUSING: brief lacks §2a LEGITIMATE SHAPES (three checkers in this gate)" >&2; exit 19; }
grep -q 'ADVERSARIAL PASS' "$BRIEF" && grep -q 'ADVERSARIAL PASS' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt must both carry C's ADVERSARIAL PASS" >&2; exit 19; }
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
# 62 — the Vision floor/port discipline (no jest lock): builder ports, the local Postgres, env -i, the real-send key, in both.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q '4848' "$FL" && grep -q '8080' "$FL" && grep -q '5433' "$FL" && grep -q 'env -i' "$FL" \
    && grep -q 'AGENTMAIL_API_KEY' "$FL" && grep -q 'vsp_qa_g1_' "$FL" && grep -qi 'no jest lock' "$FL" || {
    echo "REFUSING: $FL lacks the Vision floor/port discipline (4848, 8080, 5433, env -i, AGENTMAIL_API_KEY, vsp_qa_g1_ DBs, no jest lock)" >&2; exit 62; }
done
# 64 — production named as NEVER in both files.
for FL in "$BRIEF" "$PROMPT_FILE"; do
  grep -q 'NEVER the live' "$FL" && grep -q 'datasec-sales-portal.azurewebsites.net' "$FL" && grep -q 'datasec-sales-portal-rg' "$FL" \
    && grep -q 'hpas-quickquote' "$FL" || {
    echo "REFUSING: $FL does not name both live apps (datasec-sales-portal.azurewebsites.net / datasec-sales-portal-rg, hpas-quickquote) as NEVER" >&2; exit 64; }
done

# 38 — the brief names BOTH negative-control seats; advisory if one is no longer running.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's §8 before launch" >&2
done

# Advisory only: a moved main changes §7's merge pairs; the local Postgres not answering makes the portal runtime legs NOT RUN.
M="$(q ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M" = "$QQ_MAIN" ] || echo "NOTE: QuickQuote origin main is now ${M:-unreadable}, not ${QQ_MAIN:0:7} — §7's pairs name it: re-measure / re-brief before launch" >&2
M="$(p ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M" = "$P_MAIN" ] || echo "NOTE: portal origin main is now ${M:-unreadable}, not ${P_MAIN:0:7} — §7's pairs name it: re-measure / re-brief before launch" >&2
lsof -nP -iTCP:5433 -sTCP:LISTEN >/dev/null 2>&1 || echo "NOTE: nothing is listening on :5433 — the portal runtime legs will be NOT RUN (the gate may not start a container)" >&2

# 32 — the coordinator stamps the self-check (timestamp AND note) before launch. LAST, so --check shows every other guard.
if grep -qF "$PH_SCTS" "$BRIEF" || grep -qF "$PH_SCNOTE" "$BRIEF" \
   || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (6 7 8 18 22 50 55 56 57 58 63 31 39 10 17 12 13 14 15 20 19 24 53 60 61 62 64 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  A1 $A1_HEAD at origin (18); one commit off ${QQ_MAIN:0:7} (7, 8); five files (22); default + FEEDBACK_NOTIFY_EMAIL (56)"
  echo "  A2 $A2_HEAD at origin (18); one commit off ${P_MAIN:0:7} (7, 8); five files (22); default + FEEDBACK_NOTIFY_EMAILS (56)"
  echo "  B  $B_HEAD at origin (18); one commit off ${QQ_MAIN:0:7}; label + 2.30->2.31 only (22, 55)"
  echo "  C  $C_HEAD at origin (18); one commit off ${QQ_MAIN:0:7}; seven files (22); regex, creator-only route, retention, clean allowlist (57)"
  echo "  D  $D_HEAD at origin (18); a68b53a -> d11eed6 off ${P_MAIN:0:7}, parents exact (8); five files, per-commit sets (22, 50); escaping at D, live line on main (58)"
  echo "  lockfiles unchanged by every target; node_modules QQ $NM_QQ, portal $NM_P (63); CLARIFICATIONS C-01/C-04/C-05 (31); gate-5 floor instrument (39); report does not exist yet (17); seats $NEG_SEATS named (38)"
  echo "  tier (12); directive (13); brief+shas (14); mail (15); key absolute + question route (20); names (19); no server path (24); deadline/heartbeat (53); parse-before-red (60); exclusive trees (61); Vision floor (62); prod NEVER (64); self-check stamped (32)"
  exit 0
fi

# 11 — no inherited identity: this gate needs neither az nor gh, so both point at fresh EMPTY directories.
ID_TMP="$(mktemp -d "${TMPDIR:-/tmp}/qa-vision-gate1-id.XXXXXX")" || { echo "REFUSING: cannot create the empty identity dir" >&2; exit 11; }
mkdir -p "$ID_TMP/azure-empty" "$ID_TMP/gh-empty" || { echo "REFUSING: cannot create the empty identity dirs under $ID_TMP" >&2; exit 11; }
# ls -A of TWO dirs prints a "dir:" header for each even when both are empty, so each is tested alone (fixed 2026-09-22 after the first launch refused here).
{ [ -z "$(ls -A "$ID_TMP/azure-empty")" ] && [ -z "$(ls -A "$ID_TMP/gh-empty")" ]; } || { echo "REFUSING: the identity dirs under $ID_TMP are not empty" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_TMP/azure-empty"
export GH_CONFIG_DIR="$ID_TMP/gh-empty"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
# 64 (cont.) — nothing a product process could use to reach a real provider or database is inherited from this shell.
unset DATABASE_URL TEST_DATABASE_URL E2E_CLEANUP_DATABASE_URL AGENTMAIL_API_KEY AGENTMAIL_INBOX ACS_CONNECTION_STRING \
      ACS_EMAIL_CONNECTION_STRING ACS_EMAIL_SENDER MAIL_SENDER TABLES_CONNECTION_STRING SESSION_SECRET HPAM_WORD \
      ADVANCED_UNLOCK_SECRET SALES_COPY_EMAIL FEEDBACK_NOTIFY_EMAIL FEEDBACK_NOTIFY_EMAILS QUOTE_RETENTION_DAYS APPROVALS_INBOX \
      NTFY_TOPIC NTFY_SERVER FEEDBACK_CRON LEAD_BOT_API_KEY BOT_USER_ID WEBSITE_SITE_NAME PORT NODE_ENV
echo "identity: AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR GH_CONFIG_DIR=$GH_CONFIG_DIR (empty) CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR" >&2

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$(cat "$PROMPT_FILE")"
