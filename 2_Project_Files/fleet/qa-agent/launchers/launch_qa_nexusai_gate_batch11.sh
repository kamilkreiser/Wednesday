#!/bin/bash
# launch_qa_nexusai_gate_batch11.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 11"), TWO members, one verdict per ticket,
# ONE report (2026-09-30).
#   A — RD-591 (TIER 1, through-code, test harness only — Tuesday's ruling): rd-591-worktree-band-s86n @ 67b840b, six commits over faea66b (two forward
#       merges; NOT forward-merged onto main 5531d7b). test-server.js bands ports by worktree slot and guardServer() refuses/names dials from outside the
#       test's process tree; wired into 5 stand-ins (rd486 rd516 rd523 rd545 rd549, C-177 as corrected); rd549 stamps arrival with arrivalTime(req)
#       (C-177 ADDENDUM option (b)); new rd591 cells. Built by NexusAI-N. 4208/254.
#   B — RD-735 (TIER 2, through-code): rd-735-csp-intake-residue-r3-s86m @ 7d853b0, ONE commit on RD-618 round 2 874c4f5 (batch 9 GO WITH FINDINGS, NOT on
#       main; cut from 1904765). Per-address entry budget on the CSP intake, the wider userinfo strip, R7 /i, the cap line. Built by NexusAI-M. 4152/249.
#   Cross partner (L-B1, C-68): RD-646/647 608a1cd (queued; 1904765-cut) on MT2.
#   A and B share NO path but the counts file (guard 23). Predicted merged counts at M0 = 5531d7b: MT1 (M0 + 874c4f5 + B + A) 4242/257; MT2 (+ 608a1cd) 4253/258.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch11' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch11.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's batch 11 commission (2026-09-30 ~01:4x AEST); READY mails copied in briefs/.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, no browser.
#
# PATTERN: launch_qa_nexusai_gate_batch10.sh (prompt EMBEDDED, --check mode, stamp last). CHANGES, each deliberate:
#   - 18 / 18b / 60-less: every ls-remote is RETRIED up to 5 x ~10 s on a publickey denial (C-192); a failed read REFUSES as UNKNOWN, never as a value.
#   - 7/8: A's merge-base with main is faea66b and its chain is SIX commits (two forward merges); B is ONE commit on 874c4f5; 874c4f5 is three on 1904765.
#   - 18b: main must be 5531d7b or a descendant; RD-618 / RD-646+647 landing is EXPECTED (NOTE); main touching an A path or rd735 REFUSES; touching
#     server.js / cspReport.js / rd618 is a NOTE (RD-618's own landing touches exactly those).
#   - 93: RD-591's premises (guard, arrivalTime, the lsof/ps lookup, the 5 wirings, rd549's stamp and envReached lines, rd591's 13 titles, the rd554 sentence).
#     94: RD-735's premises (the budget, AUTHORITY, edge trim, the 429, trust proxy, R7 /i, rd735's 6 titles). 96: C-187's ADDENDUM premises (it APPLIES to B).
#   - 92: helpers/test-server require-population (54 at faea66b and 5531d7b, 55 at 67b840b).
#   - 80: the merge premise by the READ-ONLY three-argument `git merge-tree <base> <a> <b>` (writes NO objects anywhere), not --write-tree: each pair must
#     carry conflict markers in the counts file ONLY. The gate re-measures with --write-tree in its own scratch objects (brief §8.1).
#   - 97 (browser) and 60 (optional members) are GONE: no browser leg, no optional member. 41 (new): a NOTE for any merge ticket in the jest queue (read-only ls/grep).
#   - 38: negative-control seats are a stamp placeholder until Tuesday stamps them (refuses via 32). 40: the routing line QA/NexusAI-batch11 must exist
#     (checked AFTER the stamp; Tuesday adds it to fleet/inbox_routing.conf). 32: SELF-CHECK stamp, LAST refusal before --check exits.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §9); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python over `git show` output; grep, ls, tmux, test -e. It writes nothing anywhere.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch11.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..96 a guard refused
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
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
BRIEF="$BRIEFS/2026-09-30_nexusai-gate-batch11-rd591-rd735.md"
READY_A="$BRIEFS/2026-09-30_nexusai-rd591-READY-mail.txt"
READY_B="$BRIEFS/2026-09-30_nexusai-rd735-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_N="$NX/session-tools/s86n/rd591"
EV_M="$NX/session-tools/s86m"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
PREV_B10="$RPTS/2026-09-29-gate-batch10/report.md"
PREV_B10_BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch10-rd733-rd703.md"
PREV_B9="$RPTS/2026-09-29-gate-batch9/report.md"
B10_EV="$RPTS/2026-09-29-gate-batch10/evidence"
PREV_FLOORLIB="$B10_EV/qa-floorlib.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-09-30-gate-batch11/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch11'

MAIN_SHA='5531d7b83dab22906091d8a02014d4ff69cea574'      # origin main at drafting (01:48:06 AEST; = refs/pull/34/head, RD-466)
A_BASE='faea66b1bce5c17a2fef282c808821b3bf0825c6'        # merge-base(RD-591, main)
O_BASE='1904765007e9447ac6c980f9840c0689a02abe6c'        # merge-base(RD-735, main) = merge-base(RD-618, main) = merge-base(A, B) = RD-646/647's parent
A_BRANCH='rd-591-worktree-band-s86n'
A_HEAD="${QA_A_HEAD_OVERRIDE:-67b840b89b755b59268873a544b8d5ddd7ee54e0}"
B_BRANCH='rd-735-csp-intake-residue-r3-s86m'
B_HEAD="${QA_B_HEAD_OVERRIDE:-7d853b0e0b666b37d220dd05ac0727b5160555d2}"
Q_BRANCH='rd-618-csp-intake-residue-s86m'
Q_SHA='874c4f503d0f37a032014e562972b17e903e1072'          # RD-618 round 2 — B's base, NOT a member; a moved branch REFUSES (B stands on it)
X_BRANCH='rd-646-647-redis-fail-closed-recovers-s86m'
X_SHA='608a1cd99adcc69f6d2cdc552f170e89710adb02'          # the cross partner (L-B1) — pinned; a moved branch is a NOTE
R466_SHA='3f7e263bf69f571d79aeae6ecc7b48ce6730d4c2'       # RD-466's head (on main via 01fb77e/5531d7b)
R418_SHA='8de8e5c446023847362cd470375db4fb6ceaf645'       # RD-418 (C-187)
A_CHAIN='47d88551678018920fc1f07c3f6bffcfd4fc44af 4fcfbae2525526fac926d205d515a7ef09f04b84 5e00f0afd3a6b1f1bb128fc830e1341dbf72ab97 67b840b89b755b59268873a544b8d5ddd7ee54e0 a2a93b2bd87e3a56e3de0400f606ffcdc8814e67 c79926a3dbf62fb0be4214e1a9fe3fcce7de34cd'
A_PARENT='5e00f0afd3a6b1f1bb128fc830e1341dbf72ab97'
Q_CHAIN='4334b96d91132d933bc30b6b8dbd63e2031552cc 7e4cd2efd7f4f2ff28bbf6fb9cd07be02789240d 874c4f503d0f37a032014e562972b17e903e1072'

COUNTS_FILE='scripts/verify-expected-counts.json'
TS='__tests__/helpers/test-server.js'
H395='__tests__/helpers/rd395-server-harness.js'
H554='__tests__/helpers/rd554-restore-harness.js'
R486='__tests__/rd486-ai-test-key-forwarding.test.js'
R516='__tests__/rd516-ai-test-ssrf.test.js'
R523='__tests__/rd523-aoai-redirect-refused.test.js'
R545='__tests__/rd545-ai-test-limit-survives-ai-off.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
R591='__tests__/rd591-cross-seat-isolation.test.js'
SRV='backend/server.js'
CSP='backend/services/cspReport.js'
R618='__tests__/rd618-csp-intake-residue.test.js'
R735='__tests__/rd735-csp-intake-residue-r3.test.js'
R646='__tests__/rd646-647-redis-fail-closed-recovers.test.js'
ICE='__tests__/image-content-exposure.test.js'
TS_BASE_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'    # 1904765, faea66b, 5531d7b, 874c4f5, 7d853b0, 608a1cd
TS_HEAD_BLOB='bb45cd78c927d76e03a43ec29188d79e9d176b60'    # 67b840b
R549_BASE_BLOB='4a3564265683f936c99e69789049e3dd5dff9b3b'
R549_HEAD_BLOB='1988b468dd596b3fb62c6aad865bc6609ffa99dd'
R591_BLOB='6ae80ce05bb0db5c7bb54be61845aa1e9f2acce2'
H554_BLOB='028fa30bb2d4f6c36fef1e01ed2952861d055399'
H395_BLOB='2453a3f'                                          # prefix; everywhere
SRV_O_BLOB='bc099b245b01e701150cdd3cbbc74068bbcea0c8'
SRV_M_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'
SRV_Q_BLOB='e076121f4214dd6930697d9ab98bb6252b367294'
SRV_B_BLOB='86dc63f0c66e70f63ef3b807f72464158781b329'
SRV_X_BLOB='4ddf75f452c3bc9f733e3af9ad42a31db554ba81'
CSP_O_BLOB='f102d26b01e77f6ac838042b18cc9ac120c41032'
CSP_Q_BLOB='4b38e90138fe466586b7badb6266c28c4a1500b9'
CSP_B_BLOB='6608eaece05c92c50303d5e738aef250e63c5455'
R618_Q_BLOB='8bbfcc713615a7afee3da9e78f04b031063f5f32'
R618_B_BLOB='1007b660b27cb3ad7b9af9b2c36395d5ebd186cc'
R735_BLOB='4925b58d98f0841fbb012d06d163139bea5ebd72'
R646_BLOB='ee838ecd1e2234fec15b8a3f89d4328c56e3b849'
ICE_O_BLOB='94e6e4c9a316a30b3e27a77e7783b4cca02a5e72'     # 1904765, 874c4f5, 7d853b0, 608a1cd
ICE_F_BLOB='9ede5fd94a1bcf6e9ba18749418e23b7106e98da'     # faea66b, 67b840b
ICE_M_BLOB='7e3262b001088991f7b3660c0a2949139f80510a'     # 5531d7b = 3f7e263
LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
A_EXPECTED_FILES="$TS
$R486
$R516
$R523
$R545
$R549
$R591
$COUNTS_FILE"
B_EXPECTED_FILES="$SRV
$CSP
$R618
$R735
$COUNTS_FILE"
Q_EXPECTED_FILES="$SRV
$CSP
$R618
$COUNTS_FILE"
TS_POP_BASE='54'   # faea66b and 5531d7b
TS_POP_A='55'      # 67b840b
NEG_SEATS="62649 9959 38362 20317 62677"  # Tuesday stamps: NexusAI-M, -N, -O, -P and her own claude pid, space-separated, each named in the brief's §10 in backticks

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 11: RD-591 · RD-735'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch11] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head (no PR exists, so no CI Build and no lsof/ps on a Linux runner), CodeQL at any head without a PR, two real concurrent seats' full suites against each other, multi-replica deployments, a real ingress in front of the CSP intake, a real Redis, any browser, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ts_pop() { g grep -l -E "require\([^)]*helpers/test-server['\"]" "$1" -- __tests__ 2>/dev/null | wc -l | tr -d ' '; }
# C-192: ls-remote retried up to 5 x ~10 s on a publickey denial; sets LSR_OUT on success (no subshell, so LSR_ATTEMPTS counts), returns 1 (UNKNOWN) otherwise.
LSR_ATTEMPTS=0
LSR_OUT=''
lsr() { local out rc i
  LSR_OUT=''
  for i in 1 2 3 4 5; do
    LSR_ATTEMPTS=$((LSR_ATTEMPTS + 1))
    out="$(g ls-remote origin "$@" 2>&1)"; rc=$?
    if [ "$rc" = "0" ]; then LSR_OUT="$out"; return 0; fi
    printf '%s\n' "$out" | grep -qi 'publickey' || { printf '%s\n' "$out" >&2; return 1; }
    [ "$i" = "5" ] || sleep 10
  done
  printf '%s\n' "$out" >&2; return 1; }
# read-only merge prediction: the three-argument merge-tree writes NO objects; prints the paths carrying conflict markers.
conflicts() { local b; b="$(g merge-base "$1" "$2" 2>/dev/null)" || return 1
  g merge-tree "$b" "$1" "$2" 2>/dev/null | awk '/^  (base|our|their) /{f=$4} /^\+<<<<<<</{c[f]=1} END{for(k in c) print k}' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 11", with TWO members, one verdict per ticket and ONE report: RD-591 (TIER 1, through-code, test harness only: the shared test helper bands ports by worktree and makes counting stand-ins REFUSE and NAME dials from outside the test's process tree, wired into five stand-ins, and rd549 now stamps a request's arrival at the socket's accept time) and RD-735 (TIER 2, through-code: the anonymous CSP intake gets a per-address stored-entry budget and a wider userinfo strip; it is STACKED on RD-618 round 2, which is not on main). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no browser.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-gate-batch11-rd591-rd735.md
It opens with TUESDAY'S RULINGS (a) to (i): apply them, do not re-rule them. Then the charter it names, then the two READY mails it names, then the batch 10 report it names (the most recent gate; its self-corrections S-1 to S-8 are folded into your instrument rules H-22 to H-26 — a nested sandbox-exec exits 71; /bin/ps is setuid and EPERMs inside the sandbox, so use pgrep; --setupFilesAfterEnv is an array option, so test paths go first; quote every path with a space; zsh eats a bare ===== line; a bare END is not END ok) and batch 9's report for RD-618's findings A-F1r, A-F2r, A-F3c and A-N2. Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-591: branch rd-591-worktree-band-s86n at 67b840b89b755b59268873a544b8d5ddd7ee54e0; merge-base with main faea66b1bce5c17a2fef282c808821b3bf0825c6, six commits including two forward merges; NOT forward-merged onto today's main (its READY's "main faea66b merged forward" was true when main was faea66b). RD-735: rd-735-csp-intake-residue-r3-s86m at 7d853b0e0b666b37d220dd05ac0727b5160555d2, one commit on RD-618 round 2 874c4f503d0f37a032014e562972b17e903e1072, which is cut from 1904765007e9447ac6c980f9840c0689a02abe6c. Main at drafting was 5531d7b83dab22906091d8a02014d4ff69cea574 (RD-466 via PR #34). The two deltas share NO path but the counts file; they share a SEMANTIC surface — RD-735's server-booting cells take their ports from the helper RD-591 rewrites (C-68). The cross partner for RD-735's own NOT TESTED item is RD-646/647 608a1cd99adcc69f6d2cdc552f170e89710adb02 (queued): run rd646 on a merged tree carrying both (MT2). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b): four builder seats are merging one at a time tonight; RD-618 and RD-646/647 landing is expected. Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MTa = M0 + 874c4f5 4223/255, MTb = + RD-735 4229/256, MT1 = + RD-591 4242/257, MT2 = + 608a1cd 4253/258, predicted at M0 = 5531d7b), the tests census (301 / 303), the helper's importer population (55 / 56), which partners are already in. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree and name any combined blob. GitHub SSH is intermittently denying auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included). No PR exists for either branch or for RD-618 at drafting: CodeQL is NOT RUN at either head — say so; re-read with gh READ ONLY. C-185 with its ADDENDUM: main's CI known-failing set is {rd638-export-always-ends E2, rd465 O-1 only with the checkEntraStatus TypeError}.

RD-591 (TIER 1 — the guard decides whether security cells can pass for the WRONG reason). g0 FIRST, an instrument landing: the guard shells out to lsof and to the setuid /bin/ps, so under your sandbox belt it may read every child's dial as unattributable and refuse it — run rd591 B1 and B4 belted and unbelted and decide by measurement where guarded cells run (H-23); an unattributable refusal in a run makes that run's green negative cells VOID. POSITIVE CONTROL FIRST: g1 RED-AT-PARENT (rd591 against faea66b's helper), g4 the rd549 red arm must read red ON envReached (the diff exactly envReached true -> false inside the toEqual, never a timeout; quote it; your own connect-delay preload, landed only in the spawned server), s1 an SSRF/redirect product mutant red at the head as at M0 (the guard must not hide a real dial — green at the head only is a Blocker). Then: g2 arrivalTime and keep-alive (sequential, pipelined, first CALL vs first request, unguarded); g3 THE "vanished = handed over and counted" verdict — a dialer that is NOT a descendant of the jest worker connects to an rd549-shaped stand-in, writes a complete request and closes at once: does a foreign dial land in the counted requests before readiness, so a positive-arrival cell passes on it? build the cell and show it, or give the timing distribution; g5 the stamp isolated (the pre-(b) stamp red under a 3 s guard delay, arrivalTime green); g6 non-rd549 cells unaffected — the 55 importers and the harness requirers, pass sets BY NAME main vs head, LOST 0, durations; g7 the named limits MEASURED, not taken (lookup cost now, the unguarded reservePort users, the same-worker leak, CI's lsof and ps UNVERIFIED, the rd554 sentence at helpers/rd554-restore-harness.js:88-89 and which half becomes false); g8 the slot of every live worktree and every tree of yours, naming any shared slot; g9 the builder's mutants M-c, M-d, M-e re-derived plus your own. THE NEGATIVE-ASSERTION SWEEP covers every negative cell over a guarded stand-in (C-102).

RD-735 (TIER 2 — the budget SHAPE is the gate's to judge, ruling c). POSITIVE CONTROL FIRST: e0 RED-AT-PARENT against 874c4f5's two product files (exactly S7, B1, B2, R8, R9), then 19/19. Try to DEFEAT the 60-per-60-s budget: e2 one address through the real intake and the window edge; e3 many addresses through X-Forwarded-For with trust proxy 1 and no ingress; e4 the 10,000-key eviction resetting a LIVE budget (maxKeys drops the oldest-inserted key even if live); e5 window edges and a clock step; e6 the builder's M1, M2, M4 and your own. A-F2r: f1 batch 9's shapes; f2 the READY's own trade-off (https://h?x=a@b parses — which variant reaches the fallback?); f3 every shape that KEEPS userinfo (a non-C0 Unicode space before the scheme, a tab or newline inside the scheme, a non-special scheme's opaque path, triple slash, case, %40); f4 linear time. M3b: r1-r3 re-derive the isolated form and show why the builder's first M3 could not isolate A-F3c. r4 the cap and budget lines. x1 RD-735's cells under RD-591's harness on MT1; x2 rd646 on MT2 with the 503-vs-429 order MEASURED; x3 the COMBINED server entry point blob on every merged tree.

THE MERGED TREE — part of every verdict (brief section 8). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff 874c4f5 (MTa), 7d853b0 (MTb), 67b840b (MT1); in a separate clone from MT1, merge --no-ff 608a1cd (MT2) unless M0 already holds it. Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only, and the server entry point merged textually clean into a COMBINED blob. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1: predicted 4242/257, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file, the side control run inside the clone that owns the objects. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 2 = C-187's pair, because C-187's ADDENDUM APPLIES to the 1904765-cut side — ACCOUNTED only when (a1)-(a4) and (b) are each MEASURED; any other missing id is a STOP; new 32. C-68 union by name. On MT1, ONE hold. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 67b840b 4208/254, 7d853b0 4152/249, M0 = 5531d7b 4210/254, MT1 4242/257. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-26 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-3: a LANDING CONTROL for every preload, dialer, plant, clock seam or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-15: preloads with -r in argv; ONE exception is declared in this batch (the rd549 connect-delay preload may ride NODE_OPTIONS only if argv cannot reach the spawned server, gated to the server process, proven absent from jest's own stderr). H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh; targeted 600 s, unions 2400 s, full verify 2700 s, dialer runs 180 s). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-23: the guard under your belt, decided by g0. H-24: jest array options after the test paths. H-26: C-192 retries. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch11.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, preload or guard-arm scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no npm registry, no Partner Center. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 10 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with FOUR builder seats doing merges one at a time. Do ALL lock-free work first; then file ONE hold tagged qa-b11-; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4); once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of batch 10's copied instrument first); record the foreign count beside every result; count every dialer you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, dialer, request and jest run has a per-step DEADLINE and a client timeout, every server and dialer is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: no PR at drafting, so CI NOT RUN and CodeQL NOT RUN at either head; M0's CI Build 36589067630 was in progress at drafting — read its result with gh READ ONLY or say you could not. CI's lsof and ps for RD-591 are UNVERIFIED until a PR's Build runs.

RE-PIN at start, mid and end: both branches, RD-618's branch, RD-646/647's branch and main — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head (or RD-618's) that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be 5531d7b or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch11. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch11] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 11: RD-591 · RD-735
Lead the body with one line per ticket (RD-591: <GO|GO WITH FINDINGS|NO GO> @ 67b840b (g3 foreign-vanished counted: yes/no; rd549 red arm on envReached: yes/no; LOST <n>) · RD-735: … @ 7d853b0 (budget defeated by: none/route; userinfo kept in: <n> shapes; rd646 on MT2: <n>/<n>)), then one line naming M0, your recommended merge order, the merged counts you measured, the C-57 result (missing / accounted / other), and "CodeQL NOT RUN (no PR); CI lsof UNVERIFIED". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list and named limits as the brief quotes them, every declared limit L-A1 to L-A8 and L-B1 to L-B5 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-115, C-173, C-177 with its ADDENDUM, C-187 with its ADDENDUM and C-192 are the clarifications this batch leans on; C-57, C-68, C-102, C-112, C-125, C-141 and C-174 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head (no PR exists, so no CI Build and no lsof/ps on a Linux runner), CodeQL at any head without a PR, two real concurrent seats' full suites against each other, multi-replica deployments, a real ingress in front of the CSP intake, a real Redis, any browser, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows.
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
for S in "$MAIN_SHA" "$A_BASE" "$O_BASE" "$A_HEAD" "$B_HEAD" "$Q_SHA" "$X_SHA" "$R466_SHA" "$R418_SHA" $A_CHAIN $Q_CHAIN; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: A's with main is faea66b; B's, RD-618's, RD-646/647's and A x B's are 1904765; RD-618 is under B; both bases on main.
g merge-base --is-ancestor "$A_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: faea66b is not an ancestor of 5531d7b — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$O_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 1904765 is not an ancestor of 5531d7b — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$A_BASE" ] || { echo "REFUSING: merge-base(67b840b, 5531d7b) is not faea66b — re-brief" >&2; exit 7; }
for PAIR in "$B_HEAD $MAIN_SHA" "$Q_SHA $MAIN_SHA" "$X_SHA $MAIN_SHA" "$A_HEAD $B_HEAD"; do
  [ "$(g merge-base ${PAIR} 2>/dev/null)" = "$O_BASE" ] || { echo "REFUSING: merge-base(${PAIR% *}, ${PAIR#* }) is not 1904765 — re-brief" >&2; exit 7; }
done
g merge-base --is-ancestor "$Q_SHA" "$B_HEAD" 2>/dev/null || { echo "REFUSING: RD-618 874c4f5 is not an ancestor of RD-735 7d853b0 — B is not stacked as briefed" >&2; exit 7; }

# 8 — chains exact.
[ "$(g rev-list "${A_BASE}..${A_HEAD}" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$A_CHAIN" ] || { echo "REFUSING: faea66b..RD-591 is not exactly the six briefed commits" >&2; exit 8; }
[ "$(g rev-parse "${A_HEAD}^1" 2>/dev/null)" = "$A_PARENT" ] && [ "$(g log -1 --format=%P "$A_HEAD" 2>/dev/null | wc -w | tr -d ' ')" = "1" ] || { echo "REFUSING: 67b840b is not one parent 5e00f0a" >&2; exit 8; }
[ "$(g log --format='%H %P' "${Q_SHA}..${B_HEAD}" 2>/dev/null)" = "$B_HEAD $Q_SHA" ] || { echo "REFUSING: 874c4f5..RD-735 is not exactly one commit 7d853b0 on 874c4f5" >&2; exit 8; }
[ "$(g rev-list "${O_BASE}..${Q_SHA}" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$Q_CHAIN" ] || { echo "REFUSING: 1904765..RD-618 is not exactly 7e4cd2e 4334b96 874c4f5" >&2; exit 8; }
[ "$(g log --format='%H %P' "${O_BASE}..${X_SHA}" 2>/dev/null)" = "$X_SHA $O_BASE" ] || { echo "REFUSING: 1904765..RD-646/647 is not exactly one commit 608a1cd" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the two ticket branches and RD-618's exactly the pins (REFUSE); RD-646/647 a NOTE.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$Q_BRANCH" "refs/heads/$X_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$Q_BRANCH $Q_SHA"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
X_NOW="$(printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$X_BRANCH" '$2==r{print $1}')"
[ "$X_NOW" = "$X_SHA" ] || echo "NOTE: origin $X_BRANCH is '${X_NOW:-absent}', not 608a1cd — the cross cell stays pinned on 608a1cd; the gate names the move (C-68)" >&2
# 18b — main MAY move (ruling b). It must be 5531d7b or a descendant IN THE OBJECT STORE; a member already on it REFUSES.
M_ORIGIN="$(printf '%s\n' "$LSR_ALL" | awk '$2=="refs/heads/main"{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 5531d7b — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$TS" "$R486" "$R516" "$R523" "$R545" "$R549" "$R591" "$R735" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 5531d7b..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$SRV" "$CSP" "$R618" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— expected if RD-618 or RD-646/647 landed; B's C-68 set runs on the combined blobs (brief ruling b)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 5531d7b) — the gate re-pins M0 itself and re-bases every prediction" >&2
printf '%s\n' "$MOVED" | grep -qxF "$H395" && echo "NOTE: main's movement changes the rd395 harness — B's server-booting cells run under it on M0 (C-68)" >&2
Q_IN=''
g merge-base --is-ancestor "$Q_SHA" "$M_ORIGIN" 2>/dev/null && Q_IN="$Q_IN RD-618(874c4f5)"
g merge-base --is-ancestor "$X_SHA" "$M_ORIGIN" 2>/dev/null && Q_IN="$Q_IN RD-646/647(608a1cd)"
[ -z "$Q_IN" ] || echo "NOTE: origin main carries:$Q_IN — the gate skips that merge step and re-bases counts, census and C-68 populations on M0" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; A touches no product/package path.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$A_BASE" "$A_HEAD" "$A_EXPECTED_FILES" "RD-591 (faea66b..67b840b)"
chk_delta "$Q_SHA" "$B_HEAD" "$B_EXPECTED_FILES" "RD-735 (874c4f5..7d853b0)"
chk_delta "$O_BASE" "$Q_SHA" "$Q_EXPECTED_FILES" "RD-618 (1904765..874c4f5)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$A_BASE" "$A_HEAD" "$TS")" = "251 10" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R591")" = "345 0" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R549")" = "3 2" ] \
  && [ "$(ns "$A_BASE" "$A_HEAD" "$R486")" = "2 1" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R516")" = "2 1" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R523")" = "2 1" ] && [ "$(ns "$A_BASE" "$A_HEAD" "$R545")" = "2 1" ] \
  || { echo "REFUSING: RD-591's numstats are not test-server +251/-10, rd591 +345, rd549 +3/-2, four stand-ins +2/-1" >&2; exit 22; }
[ "$(ns "$Q_SHA" "$B_HEAD" "$SRV")" = "18 5" ] && [ "$(ns "$Q_SHA" "$B_HEAD" "$CSP")" = "49 6" ] && [ "$(ns "$Q_SHA" "$B_HEAD" "$R735")" = "144 0" ] && [ "$(ns "$Q_SHA" "$B_HEAD" "$R618")" = "3 1" ] \
  || { echo "REFUSING: RD-735's numstats are not server +18/-5, cspReport +49/-6, rd735 +144, rd618 +3/-1" >&2; exit 22; }
[ -z "$(g diff --name-only "$A_BASE" "$A_HEAD" -- backend static docs Dockerfile .dockerignore package.json package-lock.json .github 2>/dev/null)" ] || { echo "REFUSING: RD-591 touches a product, docs, image, package or workflow path — commissioned as test-harness only" >&2; exit 22; }

# 93 — RD-591's premises at source.
[ "$(cnt "$A_HEAD" "$TS" 'function guardServer(server, { attributionDelayMs = 0 } = {}) {')" = "1" ] && [ "$(cnt "$A_BASE" "$TS" 'function guardServer(')" = "0" ] || { echo "REFUSING: guardServer is not new at 67b840b" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" 'function arrivalTime(req) {')" = "1" ] && [ "$(cnt "$A_HEAD" "$TS" 'if (s && s.rd591AcceptedAt && !s.rd591ArrivalUsed) { s.rd591ArrivalUsed = true; return s.rd591AcceptedAt; }')" = "1" ] || { echo "REFUSING: arrivalTime is not the briefed first-CALL form" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" 'sock.rd591AcceptedAt = Date.now();   // before any lookup')" = "1" ] || { echo "REFUSING: the accept-time stamp is not set before the lookup as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" "if (a.verdict === 'vanished') {")" = "1" ] && [ "$(cnt "$A_HEAD" "$TS" 'handed over and counted, not refused.')" = "1" ] || { echo "REFUSING: the 'vanished = handed over and counted' branch is not as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" "execFile('lsof', ['-nP', \`-iTCP@\${at}:\${sock.remotePort}\`, '-Fpf']")" = "1" ] && [ "$(cnt "$A_HEAD" "$TS" "execFile('ps', ['-axww', '-o', 'pid=,ppid=,command=']")" = "1" ] || { echo "REFUSING: the lsof/ps lookup (H-23's premise) is not as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" 'const SLOT_COUNT = Math.floor((49152 - BAND_BASE) / SLOT_SPAN);')" = "1" ] && [ "$(cnt "$A_HEAD" "$TS" 'const MAX_WORKERS_PER_SLOT = 16;')" = "1" ] && [ "$(cnt "$A_HEAD" "$TS" 'const BAND_SIZE = 40;')" = "1" ] || { echo "REFUSING: the slot arithmetic (15 slots x 16 workers x 40) is not as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$TS" 'attributePeer, guardServer, arrivalTime,')" = "1" ] || { echo "REFUSING: test-server does not export guardServer and arrivalTime as briefed" >&2; exit 93; }
for F in "$R486" "$R516" "$R523" "$R545" "$R549"; do
  [ "$(cnt "$A_HEAD" "$F" '// RD-591: refuse and name any dial from outside this test process tree')" = "1" ] && [ "$(cnt "$A_HEAD" "$F" "require('./helpers/test-server');")" = "1" ] && [ "$(g show "${A_HEAD}:${F}" 2>/dev/null | grep -c 'guardServer')" -ge 2 ] \
    || { echo "REFUSING: $F is not wired with ONE guardServer line plus the import (C-177)" >&2; exit 93; }
done
[ "$(cnt "$A_HEAD" "$R549" 'requests.push({ at: arrivalTime(req), url: req.url });')" = "1" ] && [ "$(cnt "$A_BASE" "$R549" 'requests.push({ at: Date.now(), url: req.url });')" = "1" ] || { echo "REFUSING: rd549's stamp is not Date.now() -> arrivalTime(req) as briefed" >&2; exit 93; }
# (patterns in single-quoted variables: macOS bash 3.2 brace-expands a double-quoted {a, b} nested inside $(…) — measured while drafting)
P_C2='envReached: r.boot.envRequests > 0 }).toEqual({ hydrated: false, planted: 0, envReached: true });'
P_O4=".toEqual({ hydrated: false, bootPlanted: 0, envReached: true, status: 'pending', chatPlanted: 0 });"
for S in "$A_BASE" "$A_HEAD"; do
  [ "$(cnt "$S" "$R549" "$P_C2")" = "1" ] && [ "$(cnt "$S" "$R549" "$P_O4")" = "1" ] \
    || { echo "REFUSING: rd549's C2/C10 and O4 envReached assertions are not as briefed at ${S:0:7} (g4's premise)" >&2; exit 93; }
done
for T in "it('A0 CONTROL — " "it('A1 — " "it('A2 — " "it('A3 — " "it('B0 CONTROL — " "it('B1 CONTROL — " "it('B2 — " "it('B3 — " "it('B4 — " "it('B5 — " "it('B6 — " "it('B7 — " "it('B8 — "; do
  [ "$(cnt "$A_HEAD" "$R591" "$T")" = "1" ] || { echo "REFUSING: rd591 cell '$T' is not present once at 67b840b" >&2; exit 93; }
done
for S in "$A_HEAD" "$MAIN_SHA"; do
  [ "$(cnt "$S" "$H554" 'run, so two concurrent jest runs on this machine still share 39000+.')" = "1" ] && [ "$(blob "$S" "$H554")" = "$H554_BLOB" ] || { echo "REFUSING: the rd554 sentence (L-A5) is not at ${S:0:7} in $H554 blob 028fa30" >&2; exit 93; }
done
[ "$(blob "$A_BASE" "$TS")" = "$TS_BASE_BLOB" ] && [ "$(blob "$MAIN_SHA" "$TS")" = "$TS_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$TS")" = "$TS_HEAD_BLOB" ] && [ "$(blob "$B_HEAD" "$TS")" = "$TS_BASE_BLOB" ] && [ "$(blob "$X_SHA" "$TS")" = "$TS_BASE_BLOB" ] \
  || { echo "REFUSING: test-server blobs are not cff1e54 (faea66b, 5531d7b, 7d853b0, 608a1cd) -> bb45cd7 (67b840b)" >&2; exit 93; }
[ "$(blob "$A_BASE" "$R549")" = "$R549_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$R549")" = "$R549_HEAD_BLOB" ] && [ "$(blob "$A_HEAD" "$R591")" = "$R591_BLOB" ] || { echo "REFUSING: rd549 / rd591 blobs are not 4a35642 -> 1988b46 / 6ae80ce" >&2; exit 93; }
for S in "$A_HEAD" "$MAIN_SHA" "$B_HEAD" "$X_SHA"; do
  case "$(blob "$S" "$H395")" in "$H395_BLOB"*) ;; *) echo "REFUSING: the rd395 harness at ${S:0:7} is not 2453a3f" >&2; exit 93 ;; esac
  [ "$(cnt "$S" "$H395" "const { reservePort, readBody } = require('./test-server');")" = "1" ] || { echo "REFUSING: the rd395 harness does not take reservePort from test-server at ${S:0:7} (x1's premise)" >&2; exit 93; }
done
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BASE_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 merges into a combined helper (C-68)" >&2

# 94 — RD-735's premises at source.
P_EDGE="$(printf 'const EDGE_C0_OR_SPACE = /^[\\u0000-\\u%s]+|[\\u0000-\\u%s]+$/g;' 0020 0020)"   # built by printf: the drafter's tool turned a literal backslash-u-0020 into a space
[ "$(cnt "$B_HEAD" "$CSP" 'function createCspEntryBudget({ windowMs, max, maxKeys = 10000, clock = Date.now } = {}) {')" = "1" ] && [ "$(cnt "$Q_SHA" "$CSP" 'createCspEntryBudget')" = "0" ] || { echo "REFUSING: createCspEntryBudget is not new at 7d853b0 with maxKeys 10000 and a clock seam" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$CSP" 'while (used.size > maxKeys) used.delete(used.keys().next().value);')" = "1" ] || { echo "REFUSING: the oldest-key eviction (e4's premise) is not as briefed" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$CSP" 'const AUTHORITY = /^((?:[a-z][a-z0-9+.-]*:)?[\\/]{2})([^/\\]*)/i;')" = "1" ] && [ "$(cnt "$B_HEAD" "$CSP" "$P_EDGE")" = "1" ] || { echo "REFUSING: AUTHORITY / the edge trim are not as briefed" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$CSP" 'const CSP_REPORT_RATE = Object.freeze({ windowMs: 60 * 1000, max: 60 });')" = "1" ] && [ "$(cnt "$B_HEAD" "$CSP" 'const CSP_REPORT_MAX_ENTRIES_PER_REQUEST = 10;')" = "1" ] || { echo "REFUSING: the 60/60 s rate or the 10-entry cap is not as briefed" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$SRV" 'const granted = entries.length ? _cspEntryBudget.take(req.ip, entries.length) : 0;')" = "1" ] && [ "$(cnt "$B_HEAD" "$SRV" 'if (budgetSpent) return res.status(429).end();')" = "1" ] || { echo "REFUSING: the intake's budget step / 429 is not as briefed" >&2; exit 94; }
for S in "$Q_SHA" "$B_HEAD" "$MAIN_SHA"; do
  [ "$(cnt "$S" "$SRV" "app.set('trust proxy', 1);")" = "1" ] || { echo "REFUSING: trust proxy 1 (e3's premise) is not set once at ${S:0:7}" >&2; exit 94; }
done
[ "$(cnt "$B_HEAD" "$R618" '/rd618r7(charset|encoding)marker/i.test(log)')" = "1" ] && [ "$(cnt "$Q_SHA" "$R618" '/rd618r7(charset|encoding)marker/.test(log)')" = "1" ] || { echo "REFUSING: rd618 R7's regex is not case-sensitive at 874c4f5 and /i at 7d853b0" >&2; exit 94; }
for T in "test('S7 — " "test('S8 — CONTROL" "test('B1 — " "test('B2 — " "describe('R8 — " "describe('R9 — "; do
  [ "$(cnt "$B_HEAD" "$R735" "$T")" = "1" ] || { echo "REFUSING: rd735 cell '$T' is not present once at 7d853b0" >&2; exit 94; }
done
[ "$(blob "$O_BASE" "$SRV")" = "$SRV_O_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$A_HEAD" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$Q_SHA" "$SRV")" = "$SRV_Q_BLOB" ] && [ "$(blob "$B_HEAD" "$SRV")" = "$SRV_B_BLOB" ] && [ "$(blob "$X_SHA" "$SRV")" = "$SRV_X_BLOB" ] \
  || { echo "REFUSING: server entry point blobs are not bc099b2 / 0d7e387 (main, A) / e076121 / 86dc63f / 4ddf75f" >&2; exit 94; }
[ "$(blob "$O_BASE" "$CSP")" = "$CSP_O_BLOB" ] && [ "$(blob "$MAIN_SHA" "$CSP")" = "$CSP_O_BLOB" ] && [ "$(blob "$Q_SHA" "$CSP")" = "$CSP_Q_BLOB" ] && [ "$(blob "$B_HEAD" "$CSP")" = "$CSP_B_BLOB" ] \
  || { echo "REFUSING: cspReport blobs are not f102d26 (1904765, main) / 4b38e90 / 6608eae" >&2; exit 94; }
[ "$(blob "$Q_SHA" "$R618")" = "$R618_Q_BLOB" ] && [ "$(blob "$B_HEAD" "$R618")" = "$R618_B_BLOB" ] && [ "$(blob "$B_HEAD" "$R735")" = "$R735_BLOB" ] && [ "$(blob "$X_SHA" "$R646")" = "$R646_BLOB" ] \
  && [ -z "$(blob "$MAIN_SHA" "$R618")" ] && [ -z "$(blob "$MAIN_SHA" "$R646")" ] || { echo "REFUSING: rd618 / rd735 / rd646 blobs are not 8bbfcc7 -> 1007b66 / 4925b58 / ee838ec (and absent at 5531d7b)" >&2; exit 94; }
[ "$(blob "$M_ORIGIN" "$SRV")" = "$SRV_M_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s server entry point is not 0d7e387 — B merges into a different combined blob (C-68)" >&2

# 96 — C-187's ADDENDUM APPLIES to the 1904765-cut side (ruling e): its premises (a1), (a2), (a3) at source.
[ "$(blob "$O_BASE" "$ICE")" = "$ICE_O_BLOB" ] && [ "$(blob "$Q_SHA" "$ICE")" = "$ICE_O_BLOB" ] && [ "$(blob "$B_HEAD" "$ICE")" = "$ICE_O_BLOB" ] && [ "$(blob "$X_SHA" "$ICE")" = "$ICE_O_BLOB" ] || { echo "REFUSING: (a1) image-content-exposure is not 94e6e4c at 1904765, 874c4f5, 7d853b0, 608a1cd" >&2; exit 96; }
[ "$(blob "$MAIN_SHA" "$ICE")" = "$ICE_M_BLOB" ] && [ "$(blob "$R466_SHA" "$ICE")" = "$ICE_M_BLOB" ] && [ "$(blob "$A_BASE" "$ICE")" = "$ICE_F_BLOB" ] && [ "$(blob "$A_HEAD" "$ICE")" = "$ICE_F_BLOB" ] || { echo "REFUSING: (a2) image-content-exposure is not 7e3262b at 5531d7b = 3f7e263 (and 9ede5fd at faea66b, 67b840b)" >&2; exit 96; }
[ "$(g log --format=%H "${O_BASE}..${MAIN_SHA}" -- "$ICE" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' "$R466_SHA" "$R418_SHA" | sort | tr '\n' ' ' | sed 's/ $//')" ] || { echo "REFUSING: (a3) git log 1904765..5531d7b -- image-content-exposure is not exactly 8de8e5c + 3f7e263" >&2; exit 96; }
[ "$(blob "$M_ORIGIN" "$ICE")" = "$ICE_M_BLOB" ] || echo "NOTE: image-content-exposure on origin main ${M_ORIGIN:0:7} is not 7e3262b — C-187's ADDENDUM (a2) must be re-measured; any other change is a STOP" >&2

# 92 — helpers/test-server REQUIRE population: 54 at faea66b and 5531d7b, 55 at 67b840b; main-now noted.
[ "$(ts_pop "$A_BASE")" = "$TS_POP_BASE" ] && [ "$(ts_pop "$MAIN_SHA")" = "$TS_POP_BASE" ] && [ "$(ts_pop "$A_HEAD")" = "$TS_POP_A" ] || { echo "REFUSING: test-server require-population is not 54 (faea66b, 5531d7b) / 55 (67b840b) — re-brief" >&2; exit 92; }
g grep -l -E "require\([^)]*helpers/test-server['\"]" "$A_HEAD" -- "$R591" >/dev/null 2>&1 || { echo "REFUSING: rd591 does not require helpers/test-server at 67b840b (the census's positive control)" >&2; exit 92; }
TP_NOW="$(ts_pop "$M_ORIGIN")"
[ "$TP_NOW" = "$TS_POP_BASE" ] || echo "NOTE: at origin main ${M_ORIGIN:0:7} the test-server require-population is ${TP_NOW:-?} (brief: 54 at 5531d7b) — the gate re-derives it on M0" >&2

# 23 — EXPECTED OVERLAPS: A and B share the counts file and nothing else; B x RD-646/647 share the server entry point (a NOTE, x2's premise).
COMMON="$(comm -12 <(g diff --name-only "$A_BASE" "$A_HEAD" 2>/dev/null | sort) <(g diff --name-only "$O_BASE" "$B_HEAD" 2>/dev/null | sort) | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
[ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: RD-591 and RD-735(+RD-618) share '${COMMON:-<nothing>}', expected '$COUNTS_FILE' only" >&2; exit 23; }
COMMONX="$(comm -12 <(g diff --name-only "$O_BASE" "$X_SHA" 2>/dev/null | sort) <(g diff --name-only "$O_BASE" "$B_HEAD" 2>/dev/null | sort) | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
[ "$COMMONX" = "$SRV $COUNTS_FILE" ] || { echo "REFUSING: RD-735(+RD-618) and RD-646/647 share '${COMMONX:-<nothing>}', expected the server entry point and the counts file" >&2; exit 23; }

# 35 — counts at every pinned sha.
for PAIR in "$O_BASE 4133 247" "$A_BASE 4195 253" "$A_HEAD 4208 254" "$Q_SHA 4146 248" "$B_HEAD 4152 249" "$X_SHA 4144 248" "$MAIN_SHA 4210 254"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$O_BASE" "$A_BASE" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$Q_SHA" "$B_HEAD" "$X_SHA"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair's conflict markers in the counts file ONLY.
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $Q_SHA" "$M_ORIGIN $B_HEAD" "$A_HEAD $B_HEAD" "$B_HEAD $X_SHA" "$M_ORIGIN $X_SHA" "$A_HEAD $X_SHA"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  if g merge-base --is-ancestor "$Y" "$X" 2>/dev/null; then continue; fi   # already contained (e.g. RD-618 landed)
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$PREV_B10" "$PREV_B10_BRIEF" "$PREV_B9" \
         "$EV_N/lookup-cost.out" "$EV_N/r7-hold.out" "$EV_N/r7-hold.sh" "$EV_N/r7/2-redarm.log" "$EV_N/r7/4-verify.log" "$EV_N/slow-connect-preload.js" \
         "$EV_N/rd549-guard-arm.js" "$EV_N/importers-merged.txt" "$EV_N/vanish-probe.js" \
         "$EV_M/rd735-hold.log" "$EV_M/rd735-hold.sh" "$EV_M/rd735-m3b.log" "$EV_M/rd735-m3b.sh" "$EV_M/rd735-verify-full.log" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$B10_EV/qa-floorlib.sh" "$B10_EV/qa-floorcount.py" "$B10_EV/qa-to.sh" "$B10_EV/qa-holdlib.sh" "$B10_EV/qa-jestwrap.sh" "$B10_EV/qa-runj10.sh" \
         "$B10_EV/qa-mut10.py" "$B10_EV/qa-mutlib10.sh" "$B10_EV/qa-merge10.sh" "$B10_EV/qa-c57-id-superset.sh" "$B10_EV/qa-c112-census.py" "$B10_EV/qa-c68census.py" \
         "$B10_EV/qa-h1-selftest.sh" "$B10_EV/qa-h1-scan.py" "$B10_EV/qa-jsum.js" "$B10_EV/qa-mail.py" "$B10_EV/qa-mailread.py" "$B10_EV/qa-ssprint.sh" \
         "$B10_EV/qa-netbelt.sb" "$B10_EV/qa-netbelt-ctl.js" "$B10_EV/qa-cov-setup.js" "$B10_EV/qa-srvlib.js" "$B10_EV/qa-sweep-analyze.py" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:12}" "$READY_A" || { echo "REFUSING: the RD-591 READY does not name ${A_HEAD:0:12}" >&2; exit 31; }
grep -qF "$B_HEAD" "$READY_B" && grep -qF "${Q_SHA:0:7}" "$READY_B" || { echo "REFUSING: the RD-735 READY does not name $B_HEAD and its base 874c4f5" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4208/4208 tests passed across 254 suites' "$EV_N/r7-hold.out" && grep -qF 'VERDICT: PASS — 4152/4152 tests passed across 249 suites' "$EV_M/rd735-verify-full.log" \
  && grep -qF '"envReached": false' "$EV_N/r7/2-redarm.log" && grep -qF 'HEAD 5e00f0a dirty' "$EV_N/r7-hold.out" || { echo "REFUSING: a builder log no longer carries the result line the brief quotes" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B10" "$PREV_B9" "$READY_A" "$READY_B"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-591 is TIER 1 (through-code' 'RD-735 is TIER 2 (through-code)' 'One verdict PER ticket' 'TIER 1 AND TIER 2 AT THROUGH-CODE WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-591 (TIER 1, through-code' 'RD-735 (TIER 2, through-code' 'one verdict per ticket'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$A_BASE" "$O_BASE" "$Q_SHA" "$MAIN_SHA" "$X_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$TS_BASE_BLOB" "$TS_HEAD_BLOB" "$R549_BASE_BLOB" "$R549_HEAD_BLOB" "$R591_BLOB" "$H554_BLOB" "$SRV_O_BLOB" "$SRV_M_BLOB" "$SRV_Q_BLOB" "$SRV_B_BLOB" "$SRV_X_BLOB" \
         "$CSP_O_BLOB" "$CSP_Q_BLOB" "$CSP_B_BLOB" "$R618_Q_BLOB" "$R618_B_BLOB" "$R735_BLOB" "$R646_BLOB" "$ICE_O_BLOB" "$ICE_F_BLOB" "$ICE_M_BLOB" "$LOCK_BLOB" "$H395_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the verdict subject exactly" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; READY lines verbatim; clarification quotes.
WORDS="RD-591 RD-735 RD-618 RD-646/647 RD-466 C-49 C-57 C-68 C-89 C-102 C-104 C-112 C-115 C-125 C-141 ADDENDUM C-173 C-174 C-177 C-185 C-187 C-190 C-192
RED-AT-PARENT g0 g1 g2 g3 g4 g5 g6 g7 g8 g9 s1 e0 e2 e3 e4 e5 e6 f1 f2 f3 f4 r1 r3 r4 x1 x2 x3 MTa MTb MT1 MT2 M0
L-A1 L-A8 L-B1 L-B5 H-1 H-15 H-20 H-21 H-22 H-23 H-24 H-26 --forceExit trap%on%EXIT deadline LANDING%CONTROL envReached arrivalTime vanished unattributable
X-Forwarded-For maxKeys M3b rd646 setuid pgrep exits%71 END%ok =====
4242/257 4208/254 4152/249 4210/254 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request missing%2
POSITIVE%CONTROL%FIRST NEGATIVE-ASSERTION%SWEEP node%--check VOID EXCLUSIVE qa-b11- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --after DEADLINE HEARTBEAT
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN CodeQL%is%NOT%RUN UNKNOWN
Prior%work FOREGROUND never%push NEVER%merge Partner%Center batch%10 COMBINED"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 8. THE MERGED TREE' '^## 9. CI' '^## 10. Floor discipline' '^## WRONG OR UNVERIFIED' \
         '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-A8 L-B1 L-B2 L-B3 L-B4 L-B5; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
# every builder's NOT TESTED list and named limits carried verbatim (each line checked in the READY AND the brief); A| = RD-591's READY, B| = RD-735's.
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|- The guard delays every OUT-OF-PROCESS connection by its lookup: lsof ~57 ms plus a ps table ~31 ms (lookup-cost.out). The ps table could be cached; lsof cannot be avoided. A cell measuring arrival against a readiness instant must use arrivalTime(). Scanned all 25 guarded test files: only rd549 (handled) and rd591 B7 (the guard's own cell).
A|- Only listenInBand/listenOnReservedPort servers and the 5 wired stand-ins are guarded. reservePort() users that bind their own servers are not.
A|- A server leaked by an EARLIER file in the SAME jest worker still descends from that worker, so it reads as own: the guard separates seats and orphans, not suites within one worker.
A|- CI needs lsof for out-of-process peers (ubuntu-latest ships it): UNVERIFIED until the branch's Build runs.
A|- rd554-restore-harness's header ("two concurrent jest runs still share 39000+") becomes false; that is not this file, so it is not edited here.
A|NOT TESTED: two REAL concurrent seats' full suites against each other (the orphan and foreign cells stand in for it); a macOS/Linux difference in lsof output; Linux CI.
B|- The cross cell with RD-646/647 (608a1cd) on this head. The budget runs only AFTER the limiter has passed, so the named 503 comes first in principle, but rd646 was NOT run on 7d853b0 + 608a1cd. It should run on whichever lands second.
B|- Multi-replica: the budget is per process, as the ring is.
B|- The demo.
B|an ambiguous forged value such as https://h?x=a@b is logged as https://b
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
a FAILED ls-remote is UNKNOWN, never a value.
the pair stays ACCOUNTED when main (or the merged tree) carries RD-466
rd549 may stamp its env stand-in's request arrival at the socket's ACCEPT time
a red arm with a REQUESTER-side delay must still read red
proof that each stand-in's counted cells keep main's pass set.
absence of a port clash is NOT evidence of a quiet floor.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
O-1 counts as known ONLY while its failure is
A declared limit is where the evidence stops — not a place it is cleared.
band test ports by worktree (a stable hash of the worktree path) PLUS a stand-in that rejects and logs foreign traffic (C-115).
NEVER KILL BY PATTERN.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b11-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms (H-1).
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — the heartbeat is a separate child, aborted if absent at 90 s, max gap reported (H-4).
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 78 — byte-level plants via Buffer, verified with xxd (H-9).
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant rule fragment '$w' (H-9)" >&2; exit 78; }
done

# 79 — quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 81 — this batch's own premises (and batch 10's folded lessons) are in the brief.
for w in 'RED-AT-PARENT' 'ADDENDUM APPLIES' 'missing 2' '(a1)' '(a4)' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4242/257' '4253/258' \
         'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' 'NEVER merges and never pushes' 'CodeQL is NOT RUN at either' \
         'vanished' 'arrivalTime' 'envReached' 'X-Forwarded-For' 'maxKeys' 'M3b' 'rd646' 'COMBINED' 'ONE exception is declared in this batch' \
         'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' 'THREE-ARGUMENT' 'Blocker'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §10 clause 1)" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38 — negative-control seats: stamped by Tuesday (a placeholder here refuses via 32), named in the brief, live now.
UNSTAMPED_SEATS=0
case "$NEG_SEATS" in *"$PH_STAMP"*) UNSTAMPED_SEATS=1; echo "NOTE: NEG_SEATS in this launcher is still a stamp placeholder — Tuesday stamps the live seat pids" >&2 ;; esac
if [ "$UNSTAMPED_SEATS" = "0" ]; then
  for P in $NEG_SEATS; do
    grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
    pgrep -x claude 2>/dev/null | grep -qx "$P" || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 10 before launch" >&2
  done
fi
if command -v tmux >/dev/null 2>&1; then
  for N in M N P O; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check AND the seats. LAST refusal, so --check shows every other guard first.
if [ "$UNSTAMPED_SEATS" = "1" ] || grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 96 92 23 35 70 80 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 41 38); stamp NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192)" >&2
  echo "REFUSING: a stamp placeholder remains (the brief's SELF-CHECK line / Self-check note / §10 seats, or this launcher's NEG_SEATS) — the coordinator re-reads end-to-end and stamps them before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $Q_BRANCH == ${Q_SHA:0:7} at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192); $X_BRANCH ${X_NOW:0:7} (pinned 608a1cd)"
  echo "  main ${M_ORIGIN:0:7} (5531d7b or a descendant; no A path or rd735 moved) (18b); test-server population there ${TP_NOW:-?} (92); on main:${Q_IN:- none}"
  echo "  merge-bases (7); chains (8); deltas (22); RD-591 premises (93); RD-735 premises (94); C-187 ADDENDUM premises (96)"
  echo "  overlaps (23); counts (35); package-lock ${LOCK_BLOB:0:7} (70); three-argument merge-trees counts-only (80); evidence (31)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); queue (41); route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS (38)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$Q_BRANCH = $Q_SHA (RD-735's base); refs/heads/$X_BRANCH = ${X_NOW:-absent} (the cross cell stays on 608a1cd); refs/heads/main = $M_ORIGIN (5531d7b or a descendant; no RD-591 path or rd735 moved since 5531d7b; test-server require-population there ${TP_NOW:-unread}; already on it:${Q_IN:- none}). Three-argument merge-trees (read-only, no objects written) were counts-only for main x each member, main x RD-618, the member pair, and RD-735 / main / RD-591 x 608a1cd. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
