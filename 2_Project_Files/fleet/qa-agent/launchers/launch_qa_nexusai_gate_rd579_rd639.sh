#!/bin/bash
# launch_qa_nexusai_gate_rd579_rd639.sh — cross-project QA agent, ONE batched TIER 1 gate on Datasec/NexusAI, TWO targets,
# TWO verdicts, ONE report (2026-09-25):
#   A — RD-579 (TIER 1): rd-579-ai-config-clear-s84m @ cac9cf6, ONE commit off 0677388 (main is NOT its base).
#       Delta: the rd579 cell file, the server entry point (clear + AOAI save), the counts file. Counts 3974/234 -> 3982/235.
#   B — RD-639 (TIER 1): rd-639-erasure-symlink-s84n @ fe53540, ONE commit off main 7c47ec4.
#       Delta: the rd639 cell file, backend/dataErasure.js (purgeNow's live-store branch), the counts file. 3978/235 -> 4004/236.
#   The two are FILE-DISJOINT except scripts/verify-expected-counts.json; the gate verifies each head and the merged tree
#   7c47ec4 + cac9cf6 + fe53540 (built in its OWN scratch clone), counts regenerated once (predicted 4012/237).
#
# AUTHORITY: READY mails from NexusAI-M (RD-579, 12:50:25Z) and NexusAI-N (RD-639, 12:53:38Z), copies in briefs/.
# Tuesday's commission + ADDITION (batch under the 09-18 batch-gates rule). Merges: Tuesday's GO (C-127).
#
# PATTERN: launch_qa_nexusai_gate8.sh (guard families 6 7 8 18 22 35 70 31 39 10 17 11 12-15 19 20 24 53 38 32), with the
# prompt EMBEDDED as in launch_qa_nexusai_package_gate_221.sh (no separate .prompt.txt). CHANGES, each deliberate:
#   - two heads + main pinned; ls-remote re-check of BOTH branches (18). main moving past 7c47ec4 is a NOTE, not a refusal:
#     the merged-tree premise names 7c47ec4 and the gate reports what moved (C-68).
#   - exit 23: FILE-DISJOINTNESS — 0677388..cac9cf6, 0677388..7c47ec4 and 7c47ec4..fe53540 intersect in the counts file only.
#   - exit 75: the builders' evidence is tied to the committed files by sha256 prefix (server entry point 6eb4c675b5900f3f at
#     cac9cf6; dataErasure.js e75914eeb26d at fe53540), and the red-proof premise holds (server entry point identical at
#     0677388 and 7c47ec4; dataErasure.js identical at 0677388, 7c47ec4 and cac9cf6).
#   - exit 40: the routing line QA/NexusAI-g579-639 exists (checked AFTER the stamp so --check refuses on the stamp only).
#   - exit 32: SELF-CHECK stamp, placeholder @STAMP@ (comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-g579-639' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), shasum, grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_rd579_rd639.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..75 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-gate-rd579-rd639.md"
READY_A="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd579-READY-mail.txt"
READY_B="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-rd639-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EVID_M="$NX/session-tools/s84m"
EVID_N="$NX/session-tools/s84n/rd639"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
PRIOR_A="$QA_DIR/projects/nexusai/reports/2026-09-20-rd464-r3-60c76d7-tier1/report.md"
PRIOR_B="$QA_DIR/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/report.md"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
G7R1_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorlib.sh"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-g579-639'

MAIN_SHA='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'     # origin main at drafting = RD-639's base; NOT RD-579's
PORT_SHA='c5d053b542935c0d1ef8e47f0ba3f18fea9917a0'     # RD-665 port on main (C-162), 7c47ec4's parent
BASE_A='0677388ab031ffaf569a52f6c0301af48f44aece'       # RD-579's only parent
A_BRANCH='rd-579-ai-config-clear-s84m'
A_HEAD="${QA_A_HEAD_OVERRIDE:-cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1}"
B_BRANCH='rd-639-erasure-symlink-s84n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c}"

COUNTS_FILE='scripts/verify-expected-counts.json'
SERVER_FILE='backend/server.js'
ERASURE_FILE='backend/dataErasure.js'
A_TEST='__tests__/rd579-ai-config-clear-truthful.test.js'
B_TEST='__tests__/rd639-erasure-live-store-symlink.test.js'
A_EXPECTED_FILES="$A_TEST
$SERVER_FILE
$COUNTS_FILE"
B_EXPECTED_FILES="$B_TEST
$ERASURE_FILE
$COUNTS_FILE"
MAIN_EXPECTED_FILES='__tests__/rd665-standard-availability-test.test.js
azure-marketplace/combined/mainTemplate.json
scripts/verify-expected-counts.json'

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
A_SERVER_SHA256='6eb4c675b5900f3f'     # S84M's "restored to the same sha" (shasum -a 256 prefix)
B_ERASURE_SHA256='e75914eeb26d'        # S84N's "committed dataErasure.js hash equals the verified run's"
NEG_SEATS='88756 10246 10643 11987 60235'   # NexusAI-M %11, -N %12, -O %13, -P %14, Tuesday %0 — read 2026-09-25 22:55 AEST

SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-579: '
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-g579-639] ANSWER'
NOTTESTED_LINE='Not tested by this gate: a real browser (the wizard'"'"'s rendering of a 400 or of a 500 from clear), Linux or CI at either branch head (no PR exists), a store on a real second disk or network mount, Windows junctions, and the export side of a symlinked store (C-139).'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "$1:$2" 2>/dev/null; }
sha256_at() { g show "$1:$2" 2>/dev/null | shasum -a 256 | cut -c1-"$3"; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched TIER 1 gate on Datasec/NexusAI with TWO targets, TWO verdicts and ONE report: RD-579 (TIER 1) and RD-639 (TIER 1). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes the other's verdict.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-gate-rd579-rd639.md
Then the charter it names, then both READY mails it names, then the two prior gate findings it names (RD-464 r3 F-1 for RD-579; gate 4 F-A1 for RD-639). Every builder statement is a CLAIM, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-579: branch rd-579-ai-config-clear-s84m at cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1, one commit whose only parent is 0677388ab031ffaf569a52f6c0301af48f44aece — main is NOT its base. It changes the server entry point's POST /api/setup/ai-config/clear and the Azure OpenAI branch of POST /api/setup/ai-config (describe that file; never write its path in anything you run). RD-639: branch rd-639-erasure-symlink-s84n at fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c, one commit off main 7c47ec467f585e9db5daf3a82cdb96deae0b1e7a; it changes purgeNow's live-store branch in the erasure module. Main 7c47ec4 is c5d053b542935c0d1ef8e47f0ba3f18fea9917a0 (the RD-665 port, C-162) plus its counts. The two branches are FILE-DISJOINT except scripts/verify-expected-counts.json — prove it.

RD-579 — ATTACK THE THREE CLAIMS ON DISK, NOT IN THE RESPONSE. (1) clear decides from the stored Azure OpenAI fields and removes an orphan; (2) a save carrying a key, deployment or version with NO endpoint in the body and none stored answers 400 NOTHING_TO_SAVE and WRITES NOTHING — compare the WHOLE settings file before and after, bytes and key set, including aiEnabled, the last-write and confirmation markers and llmProvider; (3) a key-only rotation over a stored endpoint is unchanged — prove the stored ENC: key blob actually CHANGED. POSITIVE CONTROL FIRST: the head's cells red at 0677388 and at 7c47ec4 (S1 C1 C2 red, S0 S2 C0 C3 C4 green), 8/8 at the head, same window. Re-derive M1-M4 yourself, then M5 and M6 (the read-back removed or blinded: predicted NO cell reddens, which measures the declared-unguarded 500 branch) and M7 (the key not nulled on the orphan branch: predicted C1 red). THE CONTROL THAT CAN FAIL: drive the 500 branch with a preload in YOUR tree that makes the key's setSetting a no-op; state whether "Nothing is reported as removed" is true after the other fields were already nulled with no audit row. The "raw stored fields" are DECRYPTED reads: an ENC: key no candidate can decrypt reads as null — measure whether clear answers cleared over it. AUTHORIZATION, the full matrix: open window, open window after first run, sign-in configured and enforced (anonymous, viewer, admin), and signInUnproven; clear follows confirmAuthority and save follows adminGateRefuses — tabulate both; every refused call leaves the settings file byte-identical and writes no audit row. AUDIT: read every AI_CONFIG_CLEARED and AI_MODEL_CONFIG row; orphanedFields must be names only. NO SECRET in any response, server output, audit file or log — with a planted-token POSITIVE CONTROL that finds it first. REGRESSION on every other ai-config caller: the brief's scoped git grep list (16 test files, the wizard and settings callers, boot hydration, the loader, GET /api/setup/ai-model, confirm) — run the whole set, named, with per-file counts. Prior-work check: what the READY says was KEPT is byte-for-byte kept; RD-464 r3 F-1's own repro now answers correctly.

RD-639 — ASSERT THE EFFECT, NOT THE BOOKKEEPING (RD-575's lesson): purged is correct only if no byte of that store is readable anywhere afterwards. REAL symlinks under your own mktemp dirs: store -> file outside DATA_DIR, -> directory outside, -> another listed store inside DATA_DIR (both loop orders), -> an infrastructure file inside DATA_DIR, a dangling link, a chain, a relative link, a link to / or HOME or DATA_DIR itself, ELOOP and EACCES, and the HARD-link class sibling (pre-existing; report its class, not as RD-639's regression). Hash every target byte, DATA_DIR and a sentinel tree BESIDE DATA_DIR before and after; read the ledger RAW from disk. Any deletion outside DATA_DIR is a Blocker; any purged over surviving bytes is a Major. POSITIVE CONTROL FIRST: the head's cells red at 7c47ec4 (every L1, L2, L3; POPULATION and L4 green), 26/26 at the head; count L1's rows yourself (the brief measured 22, the READY says 23). The builder ran NO mutant table: run M-B1 (a link always purged), M-B2 (every store a failure), M-B3 (follow and delete the target — proves "never followed" bites), M-B4 (non-ENOENT realpath errors swallowed — predicted no cell reddens). THE RE-DRIVE: after run 1 the link is gone and the ledger says purged_incomplete; the sweeper re-drives; predict run 2 ok:true, status purged, filesFailed [] while the outside target still holds every byte (purgeNow's final write replaces the ledger) — MEASURE IT, grade it on RD-639, and say whether P-6 has the same hole at the base. Drive once through the admin route and the sweeper on a loopback server you booted. Where does the absolute target path in the failure text travel, and can a non-admin read it?

THE MERGED TREE — part of both verdicts. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; local user config; merges and commits in the clone ONLY): 7c47ec4, merge --no-ff cac9cf6, merge --no-ff fe53540. Predicted: each merge conflicts ONLY in the counts file — anything else STOPS (C-57). Resolve by REGENERATION, never by hand: npm run verify -- --maxWorkers=2 --update-counts ONCE on the tree after BOTH merges. Predicted 4012/237 (and main + RD-579 alone 3986/236, the builder's prediction) — predictions; the measurement decides. Build the other order too and prove the two results' trees identical apart from the counts file. Blob identities: the server entry point equals cac9cf6's, the erasure module equals fe53540's. id-superset control with a COPY of session-tools/c57-id-superset.sh (missing 0 predicted; C-133 only if it misses) and C-112's condition stated beside the conclusion. On the merged tree, one hold: rd579 (8), rd639 (26), both C-68 re-run sets, the full verify, then M1 and M-B1 again. C-89 on your clone. Nothing leaves your clone.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET (env -u SESSION_SECRET; print SET or UNSET as each hold's first line, the NAME only). Predicted cac9cf6 3982/235, fe53540 4004/236, merged 4012/237. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated file and quote the exit code, assert each anchor matched once and the marker is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/g579-639.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean or merge-tree --write-tree there, and never work in its 2_Project_Files checkout or any builder worktree (C-28). Count the repo's object files before and after and account for any delta by mtime. Symlinks, hard links and chmod ONLY under your own mktemp dirs. Findings-only: no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see (C-127: merges are Tuesday's GO). No Azure (no az at all), no demo, no public host, no real AI endpoint: every key and endpoint is fake and any AI sink is a loopback recorder. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 8 of the brief exactly. QUEUE, NEVER TAKE OVER: four NexusAI seats (M, N, O, P) share session-tools/nexusai-lock.sh with you. Every jest run goes through it with a tag starting qa-rd579- (C-141 gate-class; C-110), the lock held once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's five negative-control seats classifying foreign in the same run; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe and request has a per-step DEADLINE and a client timeout, every server is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: main 7c47ec4 Build 36133932540 GREEN 3978/3978 is RELAYED by the builder, not read by the drafter — confirm with gh READ ONLY or say you could not. CI NOT RUN at either branch head (no PR).

RE-PIN at start, mid and end: both branches and main — three timestamped readings with the branch name beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. RD-639's builder is stacking RD-627a and RD-324 on its branch: if it moves, your RD-639 verdict still names fe53540 and you say so.

QUESTIONS: your routing name is QA/NexusAI-g579-639. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-g579-639] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-579: <GO|GO WITH FINDINGS|NO GO> @ cac9cf6 · RD-639: <GO|GO WITH FINDINGS|NO GO> @ fe53540
Lead the body with one sentence per ticket. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, every declared limit L-A1..L-A4 and L-B1..L-B4 discharged with a measurement or left standing and named (C-112), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: a real browser (the wizard's rendering of a 400 or of a 500 from clear), Linux or CI at either branch head (no PR exists), a store on a real second disk or network mount, Windows junctions, and the export side of a symlinked store (C-139).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$PORT_SHA" "$BASE_A" "$A_HEAD" "$B_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — bases: RD-579 is off 0677388 (NOT main); RD-639 is off main; 0677388 is an ancestor of main; main is NOT in RD-579.
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$BASE_A" ] || { echo "REFUSING: merge-base(main, RD-579) is not 0677388" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$B_HEAD" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, RD-639) is not main 7c47ec4" >&2; exit 7; }
g merge-base --is-ancestor "$BASE_A" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 0677388 is not an ancestor of main" >&2; exit 7; }
if g merge-base --is-ancestor "$MAIN_SHA" "$A_HEAD" 2>/dev/null; then
  echo "REFUSING: main 7c47ec4 IS an ancestor of RD-579 — the branch was re-cut; re-brief" >&2; exit 7; fi

# 8 — chains exact, parents exact.
[ "$(g log --format='%H %P' "${BASE_A}..${A_HEAD}" 2>&1)" = "$A_HEAD $BASE_A" ] || {
  echo "REFUSING: 0677388..RD-579 is not exactly one commit with parent 0677388" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${B_HEAD}" 2>&1)" = "$B_HEAD $MAIN_SHA" ] || {
  echo "REFUSING: 7c47ec4..RD-639 is not exactly one commit with parent 7c47ec4" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_A}..${MAIN_SHA}" 2>&1)" = "$MAIN_SHA $PORT_SHA
$PORT_SHA $BASE_A" ] || { echo "REFUSING: 0677388..main is not exactly c5d053b then 7c47ec4 — main's line moved; re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: both branches exactly the pinned heads. main moving is a NOTE (the gate reports it; C-68).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not 7c47ec4 — the brief's merged tree names 7c47ec4; tell the gate what moved (it re-pins anyway)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
GOT="$(g diff --name-only "$BASE_A" "$A_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$A_EXPECTED_FILES")" ] || { echo "REFUSING: RD-579's delta over 0677388 is not the three files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_EXPECTED_FILES")" ] || { echo "REFUSING: RD-639's delta over 7c47ec4 is not the three files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$BASE_A" "$MAIN_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$MAIN_EXPECTED_FILES")" ] || { echo "REFUSING: 0677388..main is not the RD-665 port's three files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 23 — FILE-DISJOINTNESS: the three deltas pairwise share the counts file only.
DA="$(g diff --name-only "$BASE_A" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
DM="$(g diff --name-only "$BASE_A" "$MAIN_SHA" 2>/dev/null | sort)"
for PAIR in "A_B" "A_M" "B_M"; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY"))"
  [ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: deltas $X and $Y share more (or other) than the counts file: ${COMMON:-<nothing>}" >&2; exit 23; }
done

# 35 — counts at all four shas.
for PAIR in "$BASE_A 3974 234" "$MAIN_SHA 3978 235" "$A_HEAD 3982 235" "$B_HEAD 4004 236"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree).
for S in "$BASE_A" "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 75 — evidence tied to the committed files; the red-proof premise by blob.
[ "$(sha256_at "$A_HEAD" "$SERVER_FILE" 16)" = "$A_SERVER_SHA256" ] || { echo "REFUSING: sha256 of RD-579's server entry point is not $A_SERVER_SHA256… — the builder's evidence is not this file" >&2; exit 75; }
[ "$(sha256_at "$B_HEAD" "$ERASURE_FILE" 12)" = "$B_ERASURE_SHA256" ] || { echo "REFUSING: sha256 of RD-639's erasure module is not $B_ERASURE_SHA256… — the builder's evidence is not this file" >&2; exit 75; }
[ -n "$(blob "$BASE_A" "$SERVER_FILE")" ] && [ "$(blob "$BASE_A" "$SERVER_FILE")" = "$(blob "$MAIN_SHA" "$SERVER_FILE")" ] \
  && [ "$(blob "$MAIN_SHA" "$SERVER_FILE")" = "$(blob "$B_HEAD" "$SERVER_FILE")" ] || {
  echo "REFUSING: the server entry point differs between 0677388, 7c47ec4 and RD-639 — the brief's red-proof/disjointness premise is gone" >&2; exit 75; }
[ -n "$(blob "$BASE_A" "$ERASURE_FILE")" ] && [ "$(blob "$BASE_A" "$ERASURE_FILE")" = "$(blob "$MAIN_SHA" "$ERASURE_FILE")" ] \
  && [ "$(blob "$MAIN_SHA" "$ERASURE_FILE")" = "$(blob "$A_HEAD" "$ERASURE_FILE")" ] || {
  echo "REFUSING: the erasure module differs between 0677388, 7c47ec4 and RD-579 — re-brief" >&2; exit 75; }

# 31 — builder evidence, prior findings, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$PRIOR_A" "$PRIOR_B" \
         "$EVID_M/rd579-green.log" "$EVID_M/rd579-red-at-0677388.log" "$EVID_M/rd579-mutations.sh" "$EVID_M/rd579-mutations.log" "$EVID_M/rd579-verify.log" \
         "$EVID_N/hold.sh" "$EVID_N/hold.out" "$EVID_N/A-base.log" "$EVID_N/B-fixed.log" "$EVID_N/C-verify.log" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" "$G7R1_FLOOR" "$G7R1_FLOORLIB"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-579 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "$B_HEAD" "$READY_B" || { echo "REFUSING: the RD-639 READY does not name $B_HEAD" >&2; exit 31; }

# 39 — the floor instrument is named in the brief.
grep -qF "$G7R1_FLOOR" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $G7R1_FLOOR" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PRIOR_A" "$PRIOR_B" "$READY_A" "$READY_B"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-579 is TIER 1' 'RD-639 is TIER 1' 'One verdict PER ticket'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-579 (TIER 1)' 'RD-639 (TIER 1)' 'TWO verdicts'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$MAIN_SHA" "$BASE_A" "$PORT_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
for FL in brief prompt; do
  if [ "$FL" = brief ]; then grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
  else case "$PROMPT" in *"$SUBJECT_STEM"*"@ cac9cf6 · RD-639: "*"@ fe53540"*) ;; *) echo "REFUSING: prompt must carry the two-verdict subject" >&2; exit 15 ;; esac; fi
done
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-579 RD-639 RD-464 F-1 F-A1 RD-575 RD-627a RD-324 NOTHING_TO_SAVE POSITIVE%CONTROL%FIRST M5 M6 M7 M-B1 M-B2 M-B3 M-B4
THE%RE-DRIVE HARD-link infrastructure%file DATA_DIR Blocker DECRYPTED confirmAuthority adminGateRefuses signInUnproven
AI_CONFIG_CLEARED orphanedFields FILE-DISJOINT git%clone%--shared REGENERATION 4012/237 3986/236 3982/235 4004/236
id-superset C-57 C-68 C-89 C-112 C-125 C-127 C-133 C-141 C-110 C-28 C-162 node%--check VOID EXCLUSIVE qa-rd579-
QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME
READ%ONLY PROBED RELAYED CI%NOT%RUN Prior-work%check FOREGROUND"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 4. TARGET A' '^## 5. TARGET B' \
         '^## 6. THE MERGED TREE' '^## 8. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-rd579-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 8 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N O P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 22 23 35 70 75 31 39 10 17 11 12 13 14 15 20 19 24 53 71 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7} and $B_BRANCH == ${B_HEAD:0:7} at $PIN_TS (18); main ${M_ORIGIN:0:7}"
  echo "  RD-579 one commit off 0677388 (not main); RD-639 one commit off main; main = 0677388 + c5d053b + 7c47ec4 (7 8)"
  echo "  deltas exact (22); file-disjoint but the counts file (23); counts 3974/234 3978/235 3982/235 4004/236 (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); evidence sha256 ties + red-proof blobs (75); evidence (31)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/main = ${M_ORIGIN:-unreadable}. These are the start-of-gate pins; take your own three readings anyway."

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
