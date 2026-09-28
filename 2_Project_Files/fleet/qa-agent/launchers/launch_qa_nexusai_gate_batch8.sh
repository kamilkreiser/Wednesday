#!/bin/bash
# launch_qa_nexusai_gate_batch8.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 8"), THREE members, three verdicts,
# ONE report (2026-09-29). All three lane 2, built by NexusAI-N (S86N, also their merge author); all TIER 2, through-code; all TEST-ONLY:
#   A — RD-648: rd-648-harness-boot-residuals-s86n @ e1c7b21 = 87cf0a0 (red cells, on 1904765) -> fd53262 (the fix) -> c09e832 (merge of main
#       3d05567) -> e1c7b21 (counts). bootServer's /api/health fetch bounded by AbortSignal.timeout; H1 + K1 cells; two preloads. 4189/253.
#   B — RD-609: rd-609-gate-table-archive-name-s86n @ 8f9d921 = 0b50c23 (on 02fe76a) -> f4989e4 (merge of 3d05567) -> 8f9d921 (counts).
#       handover-gate-table decides at COLLECTION time (C-183); a CONTROL cell in both trees. 4188/252.
#   C — RD-700: rd-700-rd411-control-comment-s86n @ 006b056 = e05bea4 (on 02fe76a) -> a0481c6 (merge of 3d05567) -> 006b056 (counts _updated
#       only). Six comment lines in rd411 (guard 93 proves comment-only). 4187/252.
#   NO CROSS-CHANGE CELL: the three deltas share only the counts file (guard 23). The semantic overlap is RD-648's harness under its consumers (C-68).
#   Predicted merged counts(M0) + 3 / + 1 = 4194/253 at M0 = dd15ce1.
#
# AUTHORITY: Tuesday's batch 8 commission (2026-09-29); READY mails copied in briefs/.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones) and NEVER pushes; no fix, no deploy, nothing to Partner Center/demo/prod,
# no az, no docker, no browser.
#
# PATTERN: launch_qa_nexusai_gate_batch7.sh (guard families 9 6 7 8 18 18b 22 93 94 95 92 23 35 70 80 31 39 10 17 11 12-15 20 19 24 53 71 76 77 78 79
# 81 38 32 40), prompt EMBEDDED. CHANGES, each deliberate:
#   - 7/8: every head's merge-base with main is 3d05567 (NOT main dd15ce1); each head is a 3-commit chain whose own commit sits on an OLDER base
#     (1904765 for A, 02fe76a for B and C) with main 3d05567 merged forward. Chains compared as SETS of "sha parents" lines.
#   - 18b: main must be dd15ce1 or a descendant; main's movement since 3d05567 touching ANY member path but the counts file refuses. NOTEs when it
#     touches a harness consumer, the gate-table doc, rd411's helper, or the server entry point, or carries a batch 7 head.
#   - 93: RD-700 comment-only (code-equal after comment strip, control fires). 94: RD-609's premises. 95: RD-648's premises. 92: the harness's
#     require-consumer population (22 at 3d05567, 23 at e1c7b21).
#   - 80: NOT a merge-tree run. The drafter was forbidden `merge-tree --write-tree` against NexusAI and had to run --check; guard 80 proves the same
#     premise by PATH DISJOINTNESS over each merge-base (every head pair, and each head x main's movement since 3d05567): only the counts file shared.
#     The gate re-measures by real merge-tree in its own scratch object dir (brief §8.1).
#   - 38: negative-control seats are @STAMP@ until Tuesday stamps them (a placeholder here refuses, via 32).
#   - 40: the routing line QA/NexusAI-batch8 must exist (checked AFTER the stamp; Tuesday adds it).
#   - 32: SELF-CHECK stamp. LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch8' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §9); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep) only — NO merge-tree;
# node/python over `git show` output; grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch8.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..95 a guard refused
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
BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch8-rd648-rd609-rd700.md"
READY_A="$BRIEFS/2026-09-29_nexusai-rd648-READY-mail.txt"
READY_B="$BRIEFS/2026-09-29_nexusai-rd609-READY-mail.txt"
READY_C="$BRIEFS/2026-09-29_nexusai-rd700-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_N="$NX/session-tools/s86n"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
PREV_G6="$RPTS/2026-09-22-gate6-rd619-rd607-pr31/report.md"
PREV_F7="$RPTS/2026-09-21-rd516-fixround-rd604-batch/report.md"
PREV_B1="$RPTS/2026-09-26-gate-batch1/report.md"
PREV_B7="$RPTS/2026-09-29-gate-batch7/report.md"
PREV_B7_BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch7-rd618-rd628-rd652-rd646.md"
B7_EV="$RPTS/2026-09-29-gate-batch7/evidence"
PREV_FLOORLIB="$B7_EV/qa-floorlib.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-09-29-gate-batch8/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch8'

MAIN_SHA='dd15ce1ae8277cc9450e62b11b584a40d2226bf3'      # origin main at drafting (05:53:27 and 05:56:36 AEST); a descendant of MB
MB='3d05567c55adc7f8c74a064949223f3aedd61fff'            # every member's merge-base with main (and with each other)
BASE1='1904765007e9447ac6c980f9840c0689a02abe6c'         # RD-648's own base
BASE2='02fe76ad74ab7297a2ec807603fd8b67f547336c'         # RD-609's and RD-700's own base
A_RED='87cf0a0cbec4fa8818c2ef14b68e389ff4e755a0'; A_FIX='fd53262566685a149412f2b297f34b9a50b51544'; A_MRG='c09e832d89ad28fccd73824121213b6a429bd8f9'
B_OWN='0b50c230a4919c3ab21bba82dd97d1a5df3a2af2'; B_MRG='f4989e4a468590c44b0e7b208d53623a107f2e3f'
C_OWN='e05bea40c1e1cab0329c0360e67a817a108bfe97'; C_MRG='a0481c6db662fab672e3fbea9012a86f3937c2b5'
A_BRANCH='rd-648-harness-boot-residuals-s86n'
A_HEAD="${QA_A_HEAD_OVERRIDE:-e1c7b215e3c163ef1590e74369d50257bfa9fd1a}"
B_BRANCH='rd-609-gate-table-archive-name-s86n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-8f9d92197e0acf642b4fe2938673861e2a12c5aa}"
C_BRANCH='rd-700-rd411-control-comment-s86n'
C_HEAD="${QA_C_HEAD_OVERRIDE:-006b05609708bddeeea572ab5a1c7d404cbbe1dc}"
# batch 7's heads — context only (NOTE if main carries one: RD-648's C-68 population grows)
B7_HEADS='4334b96d91132d933bc30b6b8dbd63e2031552cc a5799f3ba444fba82b8f8f34529b5493751a9b48 09e2e6accf172f574dec22bdaedc47e104076edd 608a1cd99adcc69f6d2cdc552f170e89710adb02 ab1272678fe40e23cff86ff749601572dc8cb64b'

COUNTS_FILE='scripts/verify-expected-counts.json'
SERVER_SRC='backend/server.js'   # used by git only; the PROMPT never names it (guard 24)
HARNESS='__tests__/helpers/rd395-server-harness.js'
HARNESS_BASE_BLOB='2453a3fa7840de9d71267169b02ecea4a37015b6'
HARNESS_HEAD_BLOB='c826c1eae31015c1e470c43fbdc3beebed34b652'
GATE_TEST='__tests__/handover-gate-table.test.js'
GATE_TEST_BASE_BLOB='4b512626beabd555a41724f7aa91b4d016611e13'
GATE_TEST_HEAD_BLOB='58d39943bd508ae21ad31b57d650cc73c533626a'
GATE_DOC='docs/sustainability/S29_RESTAND_HANDOVER.md'
GATE_DOC_BLOB='d42f9779e390143857da80980f526c63a6f7102a'
RD411='__tests__/rd411-machine-shaped-labels.test.js'
RD411_BASE_BLOB='2b149569e72d051475429fead72200f686182432'
RD411_HEAD_BLOB='da2a19e22ce8937f86ef63234ca52454bcc5988b'
IMG_MANIFEST='__tests__/helpers/image-manifest.js'
A_EXPECTED_FILES="$HARNESS
__tests__/helpers/rd648-accepts-never-answers-preload.js
__tests__/helpers/rd648-ignores-sigterm-preload.js
__tests__/rd648-harness-boot-residuals.test.js
$COUNTS_FILE"
B_EXPECTED_FILES="$GATE_TEST
$COUNTS_FILE"
C_EXPECTED_FILES="$RD411
$COUNTS_FILE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
HARNESS_POP_MB='22'
HARNESS_POP_A='23'
NEG_SEATS='62649 9959 38362 20317 40885'   # Tuesday stamps: NexusAI-M, -N, -O, -P and her own claude pid, space-separated, each named in the brief's §10 in backticks

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 8: RD-648 · RD-609 · RD-700'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch8] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, a real network stall (only a loopback socket sink), a very slow CI boot, a C-57 run on CI, any browser, any deploy, real Azure, Partner Center, the demo, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
# harness population: files under __tests__ that REQUIRE the harness (a name-only grep also counts comment mentions — RD-648 READY's 25).
harness_pop() { g grep -l -E "require\([^)]*rd395-server-harness" "$1" -- __tests__ 2>/dev/null | wc -l | tr -d ' '; }
# comment-only: both blobs, block + line comments stripped, whitespace collapsed, compared; prints "equal ctrl" (want "true false").
# Control: the base with its first `const` turned into `let` must NOT compare equal to itself.
code_equal() { node -e '
const cp=require("child_process");const [R,a,b,p]=process.argv.slice(1);
const rd=(s)=>cp.execFileSync("git",["-C",R,"show",s+":"+p]).toString();
const strip=(s)=>s.replace(/\/\*[\s\S]*?\*\//g,"").replace(/^\s*\/\/.*$/gm,"").replace(/\s+/g," ");
const A=rd(a),B=rd(b);
const M=A.replace(/\bconst\b/,"let");
const ctl=(M===A)||(strip(A)===strip(M));   // "false" ONLY when the mutation landed AND the strip-compare saw it
console.log(String(strip(A)===strip(B))+" "+String(ctl));' "$REPO" "$1" "$2" "$3" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 8", with THREE members, one verdict per ticket and ONE report: RD-648 (TIER 2, through-code: the shared server-boot test harness's health fetch bounded by a timeout, plus a cell for its SIGKILL escalation); RD-609 (TIER 2, through-code: the handover gate-table SHA cell decides at collection time which of two differently NAMED cells to register, C-183); and RD-700 (TIER 2, through-code: six comment lines in the rd411 test file). All three are TEST-ONLY and built by NexusAI-N. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. TIER 2 AT THROUGH-CODE WEIGHT, FINDINGS-ONLY: you NEVER merge anything the fleet can see and NEVER push; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no browser.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-gate-batch8-rd648-rd609-rd700.md
It opens with TUESDAY'S RULINGS (a) to (e): apply them, do not re-rule them. Then the charter it names, then the three READY mails it names, then the prior reports it names: gate 6 (F-6, the residuals RD-648 closes), the rd516 fix-round report (F-7, the vacuous pass RD-609 closes; the READY calls it "gate-1 F-7"), batch 1 (B-F1, the mislabelled control RD-700 annotates) and batch 7 (the instruments, and its self-correction S-6: a history-less git tree reddens the gate-table resolve cell). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-648: branch rd-648-harness-boot-residuals-s86n at e1c7b215e3c163ef1590e74369d50257bfa9fd1a (87cf0a0 red cells on 1904765, fd53262 the fix, c09e832 a forward merge of main 3d05567c55adc7f8c74a064949223f3aedd61fff, then counts). RD-609: rd-609-gate-table-archive-name-s86n at 8f9d92197e0acf642b4fe2938673861e2a12c5aa (0b50c23 on 02fe76a, a forward merge of 3d05567, counts). RD-700: rd-700-rd411-control-comment-s86n at 006b05609708bddeeea572ab5a1c7d404cbbe1dc (e05bea4 on 02fe76a, a forward merge of 3d05567, counts: _updated only). Main at drafting was dd15ce1ae8277cc9450e62b11b584a40d2226bf3, a descendant of 3d05567 that no member contains. The three deltas share NO path but the counts file, so this batch has no cross-change cell; the overlap git cannot see is RD-648's harness under every file that requires it (C-68).

TREE KINDS (RD-609 makes the kind part of the id set). K1: a history-bearing checkout (your own git clone --shared). K2: a git archive extract with no .git anywhere above it. K3: a history-less repo (batch 7's S-6 arm; row p3 only). Name the kind beside EVERY result. Full verifies of the heads and M0 run in K1 so S-6 does not recur; add ONE K2 verify of the merged tree.

RD-648 (TIER 2, through-code). POSITIVE CONTROL FIRST: the cell file against the base harness (blob 2453a3f): H1 red, K1 green; then 2/2 at the head; re-derive M-a (the SIGKILL line removed: K1 red). Rows h3 (a FLAT 5 s timeout with no deadline term: the drafter READS H1 still green, so "bounded by the deadline" is guarded by no cell) and h4 (the 250 ms floor removed) first, then h5 (slow-but-live health: the boot must still succeed on retry), h6 (the overrun past a 15 s deadline), h7 (leak census: children, socket sink, ports, the rd648 temp dir the cell never removes), h8 (the C-68 union: every file that REQUIRES the harness — 22 at 3d05567, not the builder's 25, three of which only mention it in a comment — pass sets by name at M0 and on the merged tree, per-file time), h9 (AbortSignal.timeout on this node and CI's). Gate 6's F-6 (a) and (c): closed or not, by measurement.

RD-609 (TIER 2, through-code). POSITIVE CONTROL FIRST: the BASE file in K2 PASSES its resolve cell having checked nothing (F-7's defect, the console.warn in the log). Then p1 (K1: old title present and green, new absent; K2: the reverse; CONTROL green in both), p2 (the builder's row mutant in K2 AND K1: in K1 the resolve cell stays green because gateRows drops the malformed row, and only the cell titled CONTROL reports it), p3 (K3: the resolve cell red, unchanged by RD-609 — say whether that is inside C-183's ruling), p4 (a malformed row after a blank line inside the section: the drafter READS it reported by nothing), p5 (the builder's format probes re-derived through the real file), p6 (C-57 LIKE WITH LIKE, then one mixed comparison where the title pair is ACCOUNTED under C-133's ADDENDUM per C-183), p7 (the collection-time git spawn). C-183 clause by clause.

RD-700 (TIER 2, through-code). The comment-only claim is Tuesday's condition: prove with TWO independent instruments, each with a control that fires, that no executable line of the rd411 file changed; if any did, it goes in your WRONG list and is a Major. Then c2: the comment's two facts MEASURED at batch 1's B-red7 (7c47ec4's product with the 2b14956 cell file): that cell red with "Expected: 1, Received: 0", and every OTHER cell in the CONTROLS block green. c3 (28/28, pass sets by name), c4 (the counts file differs by _updated only).

THE MERGED TREE — part of every verdict (brief section 8). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 006b056, 8f9d921, e1c7b21. Re-measure every pair (three head pairs, M0 x each) by merge-tree in a SCRATCH object dir first — the drafter measured only path disjointness (the counts file is the one shared path) and ran no merge-tree. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once after all merges: predicted 4194/253 at M0 = dd15ce1, a prediction re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file. C-133's C-112 control (298 test files predicted at M0 = dd15ce1, none identical to no parent). Ruling (c), the id-superset control LIKE WITH LIKE: predicted missing 0 (main since 3d05567 only added titles; C-187's image-content-exposure pair does NOT apply here); any missing id is named with its file's blob history and C-133's mechanical test, never assumed, and is still a STOP. On the merged tree, one hold: every C-68 set by name, the rows the brief lists, the full verify(s), then one mutant per ticket. If M0 carries batch 7 members, their harness consumers (rd618, rd652) join the union; if not, name for the merge author that whichever lands second re-runs them. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by mtime. Nothing leaves your clone; never push.

THE NEGATIVE-ASSERTION SWEEP (brief section 3b, C-102). RD-648 adds an abort inside the harness's health loop; RD-609 moves an early return to collection time. For every negative-asserting cell among their callers (rd619, rd533, rd510 and every harness consumer that asserts a boot failure; handover-gate-table), show the failure it asserts is produced by the check it is NAMED for, with the harness's thrown message or coverage. Self-test first (a positive control, a negative control, a non-empty population) or ABORT. Report population, negative cells, still reaching, disarmed.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not). Predicted e1c7b21 4189/253, 8f9d921 4188/252, 006b056 4187/252, M0 = dd15ce1 4191/252, merged 4194/253. Every failure by NAME; rd638-export-always-ends E2 is C-185's known CI failure, not a local excuse. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-21 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed before, read raw. H-3: a LANDING CONTROL for every hook, preload, planted row or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server under the network belt, and prove the belt lets the loopback socket sink through. H-7: mutants only through a quoted tool with a negative control. H-8: the exact new text present and the old absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon reachable before measuring its absence (the sink accepts and never answers; a K2 tree really is not a checkout). H-11: /bin/bash explicitly; every sha:path braced; never set -- or declare -A in the default shell. H-12: list every modified or deleted test file before the C-57 control (predicted: three, one per head — the harness helper, the gate-table test whose ids change by tree kind, and the rd411 test). H-13: NUL-safe tree censuses. H-14: every driver ends with an END record or the run is VOID. H-15: preloads with -r in argv, never NODE_OPTIONS. H-16: a plant is what the product will treat it as. H-17: absolute tool paths, and prove the thing STARTED before reading its rc. H-18: reject the empty-input hash as a VOID read. H-19: gitleaks canaries as real keys. H-20 (standing, from batch 7's ruling f; a hung jest held the NexusAI lock 4.5 h on 2026-09-28): EVERY jest invocation inside a hold carries --forceExit AND runs under a per-step hard deadline (qa-to.sh; targeted 600 s, the C-68 union 2400 s, a full verify 2700 s); a fired deadline aborts that step, is reported by name, and the lock releases through your wrapper's own exit. H-21: every file you mutate is restored in a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, and its hash compared to the pinned blob after every hold; a tree left mutated is quarantined, never reused.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch8.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree. Never write into the builder's session-tools: copy, then hash at start and end; never run its hold scripts. Symlinks, chmod, sockets, held ports, env files and scratch git repos ONLY under your own mktemp dirs. Findings-only: never push, no commits outside your clones, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see. No Azure (no az at all), no demo, no docker, no Partner Center. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 10 of the brief exactly. QUEUE, NEVER TAKE OVER: the NexusAI seats share session-tools/nexusai-lock.sh with you. Every jest run and every server boot goes through it with a tag starting qa-b8- (C-141 gate-class, ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield). When a merge ticket is already queued, file yours with --after that merge ticket's tag (C-141 ADDENDUM 4's tool), never ahead of it; expect a busy queue while batch 7's members and batch 6 merge. Hold the lock once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of batch 7's copied instrument first); record the foreign count beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request and run has a per-step DEADLINE and a client timeout, every server, socket sink and preloaded child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether any of the three branches has a PR, and M0's CI Build and its failing set against C-185's known set, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: all three branches and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move (ruling b: batch 7's members and batch 6 are merging): call main at your start M0 and say so; it must be dd15ce1 or a descendant; if it now carries batch 7 members, re-derive the harness population on M0 and name every consumer it added; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch8. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch8] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch8/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 8: RD-648 · RD-609 · RD-700
Lead the body with one line per ticket (RD-648: <GO|GO WITH FINDINGS|NO GO> @ e1c7b21 · RD-609: … @ 8f9d921 · RD-700: … @ 006b056), then one line naming M0, your recommended merge order, the merged counts you measured, the harness C-68 union's result (population, pass sets equal by name?), and the C-57 result per tree kind. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list as the brief quotes it, every declared limit L-A1 to L-A3, L-B1 to L-B2 and L-C1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, a real network stall (only a loopback socket sink), a very slow CI boot, a C-57 run on CI, any browser, any deploy, real Azure, Partner Center, the demo, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$MB" "$BASE1" "$BASE2" "$A_RED" "$A_FIX" "$A_MRG" "$B_OWN" "$B_MRG" "$C_OWN" "$C_MRG" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — every head's merge-base with main-at-drafting AND with each other is 3d05567; 3d05567 is on main.
g merge-base --is-ancestor "$MB" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 3d05567 is not an ancestor of dd15ce1 — re-brief" >&2; exit 7; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$MB" ] || { echo "REFUSING: merge-base(dd15ce1, ${H:0:7}) is not 3d05567 — re-brief" >&2; exit 7; }
done
for PAIR in "$A_HEAD $B_HEAD" "$A_HEAD $C_HEAD" "$B_HEAD $C_HEAD"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  [ "$(g merge-base "$X" "$Y" 2>/dev/null)" = "$MB" ] || { echo "REFUSING: merge-base(${X:0:7}, ${Y:0:7}) is not 3d05567" >&2; exit 7; }
done

# 8 — chains exact, parents exact (compared as sorted SETS of "sha parents" lines; the merge commits carry two parents).
chainset() { g log --format='%H %P' "${MB}..${1}" 2>&1 | sort | tr '\n' '|'; }
want() { printf '%s\n' "$@" | sort | tr '\n' '|'; }
[ "$(chainset "$A_HEAD")" = "$(want "$A_HEAD $A_MRG" "$A_MRG $A_FIX $MB" "$A_FIX $A_RED" "$A_RED $BASE1")" ] || { echo "REFUSING: 3d05567..RD-648 is not exactly 87cf0a0 (on 1904765) -> fd53262 -> c09e832 (merge of 3d05567) -> e1c7b21" >&2; exit 8; }
[ "$(chainset "$B_HEAD")" = "$(want "$B_HEAD $B_MRG" "$B_MRG $B_OWN $MB" "$B_OWN $BASE2")" ] || { echo "REFUSING: 3d05567..RD-609 is not exactly 0b50c23 (on 02fe76a) -> f4989e4 (merge of 3d05567) -> 8f9d921" >&2; exit 8; }
[ "$(chainset "$C_HEAD")" = "$(want "$C_HEAD $C_MRG" "$C_MRG $C_OWN $MB" "$C_OWN $BASE2")" ] || { echo "REFUSING: 3d05567..RD-700 is not exactly e05bea4 (on 02fe76a) -> a0481c6 (merge of 3d05567) -> 006b056" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the three ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main MAY move (ruling b). It must be dd15ce1 or a descendant IN THE OBJECT STORE; its movement since 3d05567 must not touch any member path
# but the counts file. Movement that changes what the members' cells read or boot is a NOTE (C-68), not a refusal.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from dd15ce1 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
ALLM="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MB" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLM") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 3d05567..${M_ORIGIN:0:7} and touched a member path other than the counts file: $HIT — re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from dd15ce1) — the gate re-pins M0 itself and re-bases its counts prediction" >&2
for P in "$GATE_DOC" "$IMG_MANIFEST" "$SERVER_SRC"; do
  printf '%s\n' "$MOVED" | grep -qxF "$P" && [ "$M_ORIGIN" != "$MAIN_SHA" ] && echo "NOTE: main's movement changes $P — a member's cells read or boot it; the gate re-runs the affected cells by name on M0 (C-68)" >&2
done
CONS_MOVED="$(comm -12 <(g grep -l -E "require\([^)]*rd395-server-harness" "$M_ORIGIN" -- __tests__ 2>/dev/null | sed "s/^${M_ORIGIN}://" | sort) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$CONS_MOVED" ] || echo "NOTE: main's movement since 3d05567 touches harness consumers: $CONS_MOVED— RD-648's C-68 union on M0 includes them" >&2
B7_IN=''
for H in $B7_HEADS; do g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null && B7_IN="$B7_IN ${H:0:7}"; done
[ -z "$B7_IN" ] || echo "NOTE: origin main carries batch 7 member(s):$B7_IN — RD-648's harness population on M0 grows (brief §8.7)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta over 3d05567 is EXACTLY the commissioned file set; RD-648's harness change is +7/-1; no product path anywhere.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MB" "$A_HEAD" "$A_EXPECTED_FILES" "RD-648 (3d05567..e1c7b21)"
chk_delta "$MB" "$B_HEAD" "$B_EXPECTED_FILES" "RD-609 (3d05567..8f9d921)"
chk_delta "$MB" "$C_HEAD" "$C_EXPECTED_FILES" "RD-700 (3d05567..006b056)"
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ -z "$(g diff --name-only "$MB" "$H" -- backend static docs 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} touches product or docs — commissioned as test-only" >&2; exit 22; }
done
[ "$(g diff --numstat "$MB" "$A_HEAD" -- "$HARNESS" 2>/dev/null | cut -f1,2 | tr '\t' ' ')" = "7 1" ] || { echo "REFUSING: RD-648's harness change is not +7/-1" >&2; exit 22; }
[ "$(g diff --numstat "$MB" "$C_HEAD" -- "$RD411" 2>/dev/null | cut -f1,2 | tr '\t' ' ')" = "6 0" ] || { echo "REFUSING: RD-700's rd411 change is not +6/-0" >&2; exit 22; }

# 93 — RD-700 is comment-only, measured (control must fire: "true false"); blobs as briefed.
[ "$(code_equal "$MB" "$C_HEAD" "$RD411")" = "true false" ] || { echo "REFUSING: RD-700's $RD411 is not code-equal to 3d05567's after comment strip (or the control did not fire) — Tuesday's comment-only condition" >&2; exit 93; }
[ "$(blob "$MB" "$RD411")" = "$RD411_BASE_BLOB" ] && [ "$(blob "$C_HEAD" "$RD411")" = "$RD411_HEAD_BLOB" ] && [ "$(blob "$BASE2" "$RD411")" = "$RD411_BASE_BLOB" ] || { echo "REFUSING: rd411 blobs are not 2b14956 (02fe76a, 3d05567) -> da2a19e" >&2; exit 93; }
[ "$(g diff "$MB" "$C_HEAD" -- "$COUNTS_FILE" 2>/dev/null | grep -E '^[+-] ' | grep -vc '"_updated"')" = "0" ] || { echo "REFUSING: RD-700's counts change is not _updated only" >&2; exit 93; }

# 94 — RD-609's premises: the title pair, the collection-time switch, the CONTROL cell, the base's early return, the table doc unchanged.
OLD_T='every SHA in the table resolves to a real commit in this repository'
NEW_T='NOT A GIT CHECKOUT — every SHA in the table is well-formed; resolving it to a commit was NOT checked'
CTL_T='CONTROL — the SHA-format check finds a malformed SHA planted in a copy of the table'
[ "$(g show "${B_HEAD}:${GATE_TEST}" 2>/dev/null | grep -cF "test('$OLD_T'")" = "1" ] && [ "$(g show "${B_HEAD}:${GATE_TEST}" 2>/dev/null | grep -cF "test('$NEW_T'")" = "1" ] && [ "$(g show "${B_HEAD}:${GATE_TEST}" 2>/dev/null | grep -cF "test('$CTL_T'")" = "1" ] || { echo "REFUSING: RD-609's three titles are not each registered once at 8f9d921" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$GATE_TEST" 'if (IN_GIT_CHECKOUT) {')" = "1" ] && [ "$(cnt "$B_HEAD" "$GATE_TEST" "execFileSync('git', ['rev-parse', '--git-dir']")" = "1" ] || { echo "REFUSING: RD-609's collection-time switch is not as briefed" >&2; exit 94; }
[ "$(cnt "$MB" "$GATE_TEST" 'NOT a git checkout — SHA resolution was NOT checked')" = "1" ] && [ "$(cnt "$B_HEAD" "$GATE_TEST" 'console.warn(')" = "0" ] || { echo "REFUSING: the base's warn-and-return (F-7's defect) or its removal at the head is not as briefed" >&2; exit 94; }
[ "$(cnt "$MB" "$GATE_TEST" "test('$NEW_T'")" = "0" ] || { echo "REFUSING: the NOT-A-CHECKOUT title already exists at 3d05567" >&2; exit 94; }
for S in "$BASE2" "$MB" "$B_HEAD" "$MAIN_SHA" "$M_ORIGIN"; do
  [ "$(blob "$S" "$GATE_DOC")" = "$GATE_DOC_BLOB" ] || { if [ "$S" = "$M_ORIGIN" ]; then echo "NOTE: the gate-table doc changed on origin main ${M_ORIGIN:0:7} — RD-609's cells read a different table on M0" >&2; else echo "REFUSING: $GATE_DOC at ${S:0:7} is not d42f977" >&2; exit 94; fi; }
done
[ "$(blob "$MB" "$GATE_TEST")" = "$GATE_TEST_BASE_BLOB" ] && [ "$(blob "$B_HEAD" "$GATE_TEST")" = "$GATE_TEST_HEAD_BLOB" ] || { echo "REFUSING: gate-table test blobs are not 4b51262 -> 58d3994" >&2; exit 94; }

# 95 — RD-648's premises: the bounded fetch at the head only; the grace and default deadline; H1/K1 as briefed.
TO_TXT='signal: AbortSignal.timeout(Math.max(250, Math.min(5000, deadline - Date.now()))),'
[ "$(cnt "$A_HEAD" "$HARNESS" "$TO_TXT")" = "1" ] && [ "$(cnt "$MB" "$HARNESS" 'AbortSignal.timeout(')" = "0" ] || { echo "REFUSING: the bounded health fetch is not present once at e1c7b21 and absent at 3d05567" >&2; exit 95; }
[ "$(cnt "$A_HEAD" "$HARNESS" 'const BOOT_FAIL_TERM_GRACE_MS = 5000;')" = "1" ] && [ "$(cnt "$A_HEAD" "$HARNESS" 'bootTimeoutMs = 180000 }')" = "1" ] || { echo "REFUSING: the harness grace (5000) or default deadline (180000) is not as briefed" >&2; exit 95; }
[ "$(blob "$MB" "$HARNESS")" = "$HARNESS_BASE_BLOB" ] && [ "$(blob "$BASE1" "$HARNESS")" = "$HARNESS_BASE_BLOB" ] && [ "$(blob "$A_HEAD" "$HARNESS")" = "$HARNESS_HEAD_BLOB" ] || { echo "REFUSING: harness blobs are not 2453a3f (1904765, 3d05567) -> c826c1e" >&2; exit 95; }
[ "$(cnt "$A_HEAD" __tests__/rd648-harness-boot-residuals.test.js "boot('rd648-accepts-never-answers-preload.js', 3000)")" = "1" ] && [ "$(cnt "$A_HEAD" __tests__/rd648-harness-boot-residuals.test.js 'withinEightSeconds: r.ms < 8000')" = "1" ] || { echo "REFUSING: H1 is not the 3 s deadline / 8 s bound the brief's row h3 reasons from" >&2; exit 95; }
[ "$(blob "$MAIN_SHA" "$HARNESS")" = "$HARNESS_BASE_BLOB" ] || { echo "REFUSING: the harness on dd15ce1 is not 2453a3f" >&2; exit 95; }

# 92 — the harness's REQUIRE population (not a name grep): 22 at 3d05567, 23 at e1c7b21; main-now noted.
[ "$(harness_pop "$MB")" = "$HARNESS_POP_MB" ] || { echo "REFUSING: harness require-population at 3d05567 is '$(harness_pop "$MB")', not $HARNESS_POP_MB — re-brief" >&2; exit 92; }
[ "$(harness_pop "$A_HEAD")" = "$HARNESS_POP_A" ] || { echo "REFUSING: harness require-population at e1c7b21 is '$(harness_pop "$A_HEAD")', not $HARNESS_POP_A — re-brief" >&2; exit 92; }
HP_NOW="$(harness_pop "$M_ORIGIN")"
[ "$HP_NOW" = "$HARNESS_POP_MB" ] || echo "NOTE: at origin main ${M_ORIGIN:0:7} the harness require-population is ${HP_NOW:-?} (brief: $HARNESS_POP_MB at 3d05567) — the gate re-derives it on M0" >&2

# 23 — EXPECTED OVERLAPS: every pair of deltas shares the counts file and nothing else.
dset() { g diff --name-only "$MB" "$1" 2>/dev/null | sort; }
DA="$(dset "$A_HEAD")"; DB="$(dset "$B_HEAD")"; DC="$(dset "$C_HEAD")"
for SPEC in "A B" "A C" "B C"; do
  X="${SPEC%% *}"; Y="${SPEC#* }"
  eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
  [ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '$COUNTS_FILE' only" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$MB 4187 252" "$MAIN_SHA 4191 252" "$A_HEAD 4189 253" "$B_HEAD 4188 252" "$C_HEAD 4187 252" "$A_RED 4133 247" "$A_FIX 4133 247" "$BASE2 4159 249"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$MB" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge premise by PATH DISJOINTNESS (no merge-tree here; see header): every head pair and each head x main's movement since 3d05567
# share the counts file and nothing else. Two deltas with disjoint non-counts paths cannot conflict textually on anything but that file.
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  COMMON="$(comm -12 <(dset "$H") <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$COMMON" ] || [ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: ${H:0:7} and main's movement to ${M_ORIGIN:0:7} share '$COMMON' — not counts-only (80)" >&2; exit 80; }
done

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$CLAR" "$PREV_G6" "$PREV_F7" "$PREV_B1" "$PREV_B7" "$PREV_B7_BRIEF" \
         "$EV_N/rd648/consumers.txt" "$EV_N/rd648/red-hold.out" "$EV_N/rd648/run1-clean.log" "$EV_N/rd648/run2-mutant-Ma.log" "$EV_N/rd648/green-hold.out" \
         "$EV_N/ready3/rd648-verify.log" "$EV_N/ready3/rd648-named.log" "$EV_N/ready3/rd609-verify.log" "$EV_N/ready3/rd609-named.log" \
         "$EV_N/ready3/rd700-verify.log" "$EV_N/ready3/rd700-named.log" "$EV_N/rd609-format-probe.txt" "$EV_N/rd609/main-archive.log" \
         "$EV_N/rd609/branch-archive.log" "$EV_N/rd609/branch-checkout.log" "$EV_N/rd609/branch-archive-mutant.log" "$EV_N/rd609/rd700-branch.log" \
         "$EV_N/rd609/rd700-main.log" "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$B7_EV/qa-floorlib.sh" "$B7_EV/qa-floorcount.py" "$B7_EV/qa-to.sh" "$B7_EV/qa-holdlib.sh" "$B7_EV/qa-jestwrap.sh" "$B7_EV/qa-runj.sh" \
         "$B7_EV/qa-mutate.py" "$B7_EV/qa-merge.sh" "$B7_EV/qa-clone.sh" "$B7_EV/qa-c57-id-superset.sh" "$B7_EV/q-merged-identity.py" "$B7_EV/qa-ssprint.sh" \
         "$B7_EV/qa-h1-selftest.sh" "$B7_EV/qa-h1-scan.py" "$B7_EV/qa-netbelt.sb" "$B7_EV/qa-netbelt-ctl.js" "$B7_EV/qa-srvlib.js" \
         "$B7_EV/qa-lockcheck.js" "$B7_EV/qa-codeonly.js" "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-648 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-609 READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-700 READY does not name ${C_HEAD:0:7}" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4189/4189 tests passed across 253 suites' "$EV_N/ready3/rd648-verify.log" && grep -qF 'VERDICT: PASS — 4188/4188 tests passed across 252 suites' "$EV_N/ready3/rd609-verify.log" && grep -qF 'VERDICT: PASS — 4187/4187 tests passed across 252 suites' "$EV_N/ready3/rd700-verify.log" || { echo "REFUSING: a builder verify log no longer carries the READY's VERDICT line" >&2; exit 31; }
[ "$(sed '/^$/d' "$EV_N/rd648/consumers.txt" | wc -l | tr -d ' ')" = "26" ] || echo "NOTE: the builder's consumers.txt is no longer 26 lines (brief WRONG 1 reads it as 25 + rd648)" >&2

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_G6" "$PREV_F7" "$PREV_B1" "$PREV_B7" "$READY_A" "$READY_B" "$READY_C"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-648 is TIER 2 (through-code)' 'RD-609 is TIER 2 (through-code)' 'RD-700 is TIER 2 (through-code)' 'One verdict PER ticket' 'TIER 2 AT THROUGH-CODE WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-648 (TIER 2, through-code' 'RD-609 (TIER 2, through-code' 'RD-700 (TIER 2, through-code' 'one verdict per ticket' 'TIER 2 AT THROUGH-CODE WEIGHT'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$MB" "$MAIN_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$A_RED" "$A_FIX" "$B_OWN" "$C_OWN"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
done
for S in "$HARNESS_BASE_BLOB" "$HARNESS_HEAD_BLOB" "$LOCK_BLOB" "$GATE_DOC_BLOB" "$RD411_BASE_BLOB" "$RD411_HEAD_BLOB"; do
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

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-648 RD-609 RD-700 F-6 F-7 B-F1 S-6 C-57 C-68 C-89 C-104 C-112 C-125 C-133 C-141 ADDENDUM C-174 C-183 C-185 C-187 C-49 C-102
M-a h3 h4 h5 h6 h7 h8 h9 p1 p2 p3 p4 p5 p6 p7 c2 c3 c4 B-red7 K1 K2 K3 LIKE%WITH%LIKE CONTROL gateRows 22%at%3d05567 AbortSignal.timeout
L-A1 L-A3 L-B1 L-B2 L-C1 H-1 H-19 H-20 H-21 --forceExit trap%on%EXIT deadline no%cross-change%cell
4194/253 4189/253 4188/252 4187/252 4191/252 298 missing%0 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset
POSITIVE%CONTROL%FIRST NEGATIVE-ASSERTION%SWEEP node%--check VOID EXCLUSIVE qa-b8- QUEUE,%NEVER%TAKE%OVER --after DEADLINE HEARTBEAT
2%minutes 5%minutes finally LANDING%CONTROL SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN
Prior%work FOREGROUND never%push NEVER%merge Partner%Center batch%7"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 8. THE MERGED TREE' '^## 10. Floor discipline' \
         '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^### TARGET C'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-B1 L-B2 L-C1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
# every builder's NOT TESTED list is carried verbatim (distinctive fragments, checked in the READY AND the brief)
for PAIR in "$READY_A|The timeout under a real network stall, as opposed to a local socket sink. Linux CI (the next Build on the branch will say)." \
            "$READY_A|Whether 5 s per attempt is right for a very slow CI boot: the overall deadline still governs, and the cap only stops ONE hanging attempt from eating it." \
            "$READY_B|NOT TESTED: a C-57 run in an archive tree; CI (Linux)." \
            "$READY_C|NOT TESTED: nothing beyond the file; a comment changes no behaviour."; do
  F="${PAIR%%|*}"; T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the NOT TESTED fragment '$T' verbatim" >&2; exit 19; }
done
# the rulings the brief rests on are quoted from source and still say so
for PAIR in "the handover-gate-table SHA-resolution cell decides at COLLECTION time" \
            "A C-57 id-superset compares like with like (both checkouts, or both archives)." \
            "short-lived branches (plain C-57 applies unchanged)" \
            "a clean merge-tree and a changed measured surface are not in tension"; do
  grep -qF -- "$PAIR" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$PAIR' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$PAIR" "$BRIEF" || { echo "REFUSING: brief does not quote '$PAIR'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b8-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT'; do
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

# 81 — this batch's own premises are in the brief.
for w in 'no cross-change cell' 'LIKE WITH LIKE' 'THREE tree KINDS' 'S-6' '4194/253' '22 files `require` the harness' 'reported by nothing' \
         'guarded by no cell' 'C-187' 'does NOT apply here' 'comment-only' 'H-20' 'H-21' 'NEVER merges and never pushes' 'PATH DISJOINTNESS'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 38 — negative-control seats: stamped by Tuesday (a placeholder here refuses via 32), named in the brief, live now.
UNSTAMPED_SEATS=0
case "$NEG_SEATS" in *"$PH_STAMP"*) UNSTAMPED_SEATS=1; echo "NOTE: NEG_SEATS in this launcher is still a stamp placeholder — Tuesday stamps the live seat pids" >&2 ;; esac
if [ "$UNSTAMPED_SEATS" = "0" ]; then
  for P in $NEG_SEATS; do
    grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
    [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 10 before launch" >&2
  done
fi
if command -v tmux >/dev/null 2>&1; then
  for N in M N P O; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check AND the seats. LAST refusal, so --check shows every other guard first.
if [ "$UNSTAMPED_SEATS" = "1" ] || grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 92 23 35 70 80 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 38); stamp NOT complete." >&2
  echo "REFUSING: a stamp placeholder remains (the brief's SELF-CHECK line / Self-check note / §10 seats, or this launcher's NEG_SEATS) — the coordinator re-reads end-to-end and stamps them before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (dd15ce1 or a descendant; no member path but the counts file moved) (18b); harness population there ${HP_NOW:-?} (92); batch 7 on main:${B7_IN:- none}"
  echo "  merge-bases (7); chains (8); deltas (22); RD-700 comment-only (93); RD-609 premises (94); RD-648 premises (95)"
  echo "  overlaps (23); counts (35); package-lock ${LOCK_BLOB:0:7} (70); path disjointness vs main's movement (80); evidence (31)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS (38)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/main = $M_ORIGIN (dd15ce1 or a descendant; no member path but the counts file moved since 3d05567; harness require-population there ${HP_NOW:-unread}; batch 7 members on it:${B7_IN:- none}). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
