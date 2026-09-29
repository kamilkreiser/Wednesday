#!/bin/bash
# launch_qa_nexusai_gate_batch9.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 9"), TWO members (+ an OPTIONAL third),
# one verdict per ticket, ONE report (2026-09-29).
#   A — RD-618 FIX ROUND 2 (TIER 1, ROUND 2 OF 2 — a NO GO goes to KAM, no round 3): rd-618-csp-intake-residue-s86m @ 874c4f5 =
#       7e4cd2e (on 1904765) -> 4334b96 (batch 7's NO GO head) -> 874c4f5 (A-F1 per-request cap, A-F2 userinfo on unparseable URLs, A-F3 non-entity
#       body-parser errors answered with type+status only). NOT forward-merged (merge-base with main = 1904765). Built by NexusAI-M. 4146/248.
#       Cross-change partner (C-68): RD-646+RD-647 608a1cd (batch 7's x-rows), kept on a merged tree.
#   B — RD-723 (TIER 2, through-code): rd-723-rd638-e2-budget-s86n @ 19fc17c = 816c33a (on 6ae20af) -> 9282763 (merge of main dd15ce1) -> 19fc17c
#       (counts _updated only). rd638's two cells get jest budgets; no asserted value may change (guard 93). Built by NexusAI-N. 4191/252.
#   OPTIONAL — RD-466 (NexusAI-O): NOT READY at drafting. Stamp O_BRANCH/O_HEAD/O_READY below ONLY when its READY is on disk; empty = not a member.
#   A and B share NO path but the counts file (guard 23). Predicted merged counts at M0 = dd15ce1: MT1 (M0 + B + A) 4204/253; MT2 (+ 608a1cd) 4215/254.
#
# AUTHORITY: Tuesday's batch 9 commission (2026-09-29); READY mails copied in briefs/.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, no browser.
#
# PATTERN: launch_qa_nexusai_gate_batch8.sh (guard families 9 6 7 8 18 18b 22 93 94 95 92 23 35 70 80 31 39 10 17 11 12-15 20 19 24 53 71 76 77 78 79
# 81 38 32 40), prompt EMBEDDED, --check mode. CHANGES, each deliberate:
#   - 7/8: A's merge-base with main is 1904765 (A is NOT forward-merged); B's is dd15ce1 (B contains main at drafting). Chains as SETS of "sha parents".
#   - 18b: main must be dd15ce1 or a descendant; main's movement since dd15ce1 touching A's cell file, the CSP report service or B's file REFUSES;
#     touching the server entry point (RD-681 does) is a NOTE (C-68). NOTEs when main carries RD-648's harness, 608a1cd, or a queued merge.
#   - 93: RD-723 "no asserted value changed" — constant-substitution compare (declared values parsed from the head), control fires ("true false").
#   - 94: RD-618's premises (cap, userinfo regex, the handler's three branches, no err.message in added lines, S5/S6/R6/R7). 95: 608a1cd's premises
#     (the named error is type-less, statusCode 503; CENSUS-B/M). 96: C-187 applies (image-content-exposure 94e6e4c on A and 608a1cd, 9ede5fd on main).
#     97: RD-723's premises (h.stop's 20 s bound vs the comment's "5 s each"; the budget constants).
#   - 92: the harness's REQUIRE population (22 at dd15ce1 and 19fc17c; 23 at 874c4f5 — rd618 is a consumer).
#   - 80: a REAL merge-tree, in a SCRATCH object dir under $TMPDIR (GIT_OBJECT_DIRECTORY; NexusAI's objects as a read-only alternate) — nothing is
#     written into NexusAI. Pairs: A x main, B x main, A x B, A x 608a1cd, B x 608a1cd. Each must conflict on the counts file only (or merge clean).
#   - 60: the OPTIONAL RD-466 member — validated only when stamped; the prompt says "not a member" otherwise.
#   - 38: negative-control seats are @STAMP@ until Tuesday stamps them (a placeholder here refuses, via 32).
#   - 40: the routing line QA/NexusAI-batch9 must exist (checked AFTER the stamp; Tuesday adds it).
#   - 32: SELF-CHECK stamp. LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch9' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §9); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep) plus merge-tree with a scratch
# GIT_OBJECT_DIRECTORY outside NexusAI; node/python over `git show` output; grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch9.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..97 a guard refused
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
BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch9-rd618r2-rd723.md"
READY_A="$BRIEFS/2026-09-29_nexusai-rd618-r2-READY-mail.txt"
READY_B="$BRIEFS/2026-09-29_nexusai-rd723-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_M="$NX/session-tools/s86m"
EV_N="$NX/session-tools/s86n"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
PREV_B7="$RPTS/2026-09-29-gate-batch7/report.md"
PREV_B8="$RPTS/2026-09-29-gate-batch8/report.md"
PREV_B7_BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch7-rd618-rd628-rd652-rd646.md"
PREV_B8_BRIEF="$BRIEFS/2026-09-29_nexusai-gate-batch8-rd648-rd609-rd700.md"
B7_EV="$RPTS/2026-09-29-gate-batch7/evidence"
B8_EV="$RPTS/2026-09-29-gate-batch8/evidence"
PREV_FLOORLIB="$B8_EV/qa-floorlib.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-09-29-gate-batch9/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch9'

MAIN_SHA='dd15ce1ae8277cc9450e62b11b584a40d2226bf3'      # origin main at drafting (12:21:29 and 12:26:29 AEST; Tuesday's 10:49 reading agrees)
BASE1='1904765007e9447ac6c980f9840c0689a02abe6c'         # A's base = merge-base(A, main) = merge-base(A, B) = merge-base(A, D)
A_R1='7e4cd2efd7f4f2ff28bbf6fb9cd07be02789240d'; A_PARENT='4334b96d91132d933bc30b6b8dbd63e2031552cc'
B_BASE='6ae20afc4a3b4a0fd78362f7ebb002b55755cfaf'; B_OWN='816c33a7b6657d9c2eb857ef21bccaabd17212d8'; B_MRG='92827633f6ebd46eb5c42f0bdbaa72c11a2cc886'
A_BRANCH='rd-618-csp-intake-residue-s86m'
A_HEAD="${QA_A_HEAD_OVERRIDE:-874c4f503d0f37a032014e562972b17e903e1072}"
B_BRANCH='rd-723-rd638-e2-budget-s86n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-19fc17ca5aa41e3be3a6b9d174a5d627f4a33145}"
D_BRANCH='rd-646-647-redis-fail-closed-recovers-s86m'
D_SHA='608a1cd99adcc69f6d2cdc552f170e89710adb02'          # the cross-change partner (C-68) — pinned; a moved branch is a NOTE
# queued merges ahead of this batch — context only (NOTE if main carries one)
R648_HEAD='b12a475fa73b439eea49cc9f692ef915af478253'
QUEUED='faea66b1bce5c17a2fef282c808821b3bf0825c6 9d7076b0368f02ca030a904a2ce45de93739238e ce148d5d8332606654c189cd14f3aadee227a407 006b05609708bddeeea572ab5a1c7d404cbbe1dc 8f9d92197e0acf642b4fe2938673861e2a12c5aa b12a475fa73b439eea49cc9f692ef915af478253'

# OPTIONAL member — Tuesday stamps these three ONLY when RD-466's READY is on disk (full 40-hex head, branch, READY path). Empty = not a member.
O_BRANCH=''
O_HEAD=''
O_READY=''

COUNTS_FILE='scripts/verify-expected-counts.json'
SERVER_SRC='backend/server.js'   # used by git only; the PROMPT never names it (guard 24)
CSP_SRC='backend/services/cspReport.js'
A_TEST='__tests__/rd618-csp-intake-residue.test.js'
B_TEST='__tests__/rd638-export-always-ends.test.js'
HARNESS='__tests__/helpers/rd395-server-harness.js'
ICE='__tests__/image-content-exposure.test.js'
D_TEST='__tests__/rd646-647-redis-fail-closed-recovers.test.js'
SERVER_BASE_BLOB='bc099b245b01e701150cdd3cbbc74068bbcea0c8'     # 1904765 and dd15ce1
SERVER_PARENT_BLOB='c5bd870f704e726745067b0d79025dbc3f862c4d'   # 4334b96
SERVER_HEAD_BLOB='e076121f4214dd6930697d9ab98bb6252b367294'     # 874c4f5
SERVER_D_BLOB='4ddf75f452c3bc9f733e3af9ad42a31db554ba81'        # 608a1cd
CSP_BASE_BLOB='f102d26b01e77f6ac838042b18cc9ac120c41032'
CSP_PARENT_BLOB='fa868ea7f0466d9f7904992acb555e704dc13791'
CSP_HEAD_BLOB='4b38e90138fe466586b7badb6266c28c4a1500b9'
A_TEST_PARENT_BLOB='2b5130b8ee9a89ebe1c6bea138488f870089ce67'
A_TEST_HEAD_BLOB='8bbfcc713615a7afee3da9e78f04b031063f5f32'
B_TEST_BASE_BLOB='e7789e5731151ca84c1ac6d55cafc440cd3474ce'
B_TEST_HEAD_BLOB='fc121f5d295997d5ec15e29a1c92063172197845'
HARNESS_BLOB='2453a3fa7840de9d71267169b02ecea4a37015b6'
HARNESS_R648_BLOB='c826c1eae31015c1e470c43fbdc3beebed34b652'
ICE_OLD_BLOB='94e6e4c9a316a30b3e27a77e7783b4cca02a5e72'
ICE_NEW_BLOB='9ede5fd94a1bcf6e9ba18749418e23b7106e98da'
A_EXPECTED_FILES="$A_TEST
$SERVER_SRC
$CSP_SRC
$COUNTS_FILE"
B_EXPECTED_FILES="$B_TEST
$COUNTS_FILE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
HARNESS_POP_MAIN='22'
HARNESS_POP_A='23'
NEG_SEATS='62649 9959 38362 20317 64933'   # Tuesday stamps: NexusAI-M, -N, -O, -P and her own claude pid, space-separated, each named in the brief's §10 in backticks

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 9: RD-618 r2 · RD-723'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch9] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, CodeQL at any head without a PR, a real browser's Reporting API delivery, a real Redis server (only a loopback stand-in and a refusing port), a boot slower than the delays driven here, any browser, any deploy, real Azure, Partner Center, the demo, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
harness_pop() { g grep -l -E "require\([^)]*rd395-server-harness" "$1" -- __tests__ 2>/dev/null | wc -l | tr -d ' '; }
# RD-723 "no asserted value changed": in the head, parse each new constant's DECLARED value, drop the declarations and the two budget arguments,
# substitute each constant by its declared value, strip comments, collapse whitespace; compare with the base stripped. Prints "equal ctl" (want
# "true false"). Control: the head with `E2_EXPORT_WITHIN_MS = 15000` declared as 16000 must NOT compare equal.
values_equal() { node -e '
const cp=require("child_process");const [R,a,b,p]=process.argv.slice(1);
const rd=(s)=>cp.execFileSync("git",["-C",R,"show",s+":"+p]).toString();
const strip=(s)=>s.replace(/\/\*[\s\S]*?\*\//g,"").replace(/^\s*\/\/.*$/gm,"").replace(/\s+/g," ").trim();
const NAMES=["E1_SETTLE_MS","MARGIN_MS","E2_BOOT_MS","E2_SETTLE_SLEEP_MS","E2_EXPORT_WITHIN_MS","E2_STOP_MS","E2_BUDGET_MS"];
function norm(H){
  const vals={};
  for(const n of NAMES){const m=H.match(new RegExp("^const "+n+" = ([0-9]+);$","m")); if(m) vals[n]=m[1];}
  let s=H.replace(new RegExp("^const ("+NAMES.join("|")+") = [^;\\n]*;\\n","gm"),"");
  s=s.split("}, E1_SETTLE_MS + MARGIN_MS);").join("});").split("}, E2_BUDGET_MS);").join("});");
  for(const n of Object.keys(vals)) s=s.replace(new RegExp("\\b"+n+"\\b","g"),vals[n]);
  return strip(s);
}
const B=strip(rd(a)),H=rd(b);
const M=H.replace("const E2_EXPORT_WITHIN_MS = 15000;","const E2_EXPORT_WITHIN_MS = 16000;");
const ctl=(M===H)||(norm(M)===B);   // "false" ONLY when the control mutation landed AND the compare saw it
console.log(String(norm(H)===B)+" "+String(ctl));' "$REPO" "$1" "$2" "$3" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 9", with TWO members, one verdict per ticket and ONE report: RD-618 FIX ROUND 2 (TIER 1, ROUND 2 OF 2: the anonymous CSP report intake gets a per-request entry cap, a userinfo strip for values the URL parser rejects, and an error handler that answers other body-parser refusals with their own status and logs only type and status) and RD-723 (TIER 2, through-code: rd638's two cells get jest budgets built from their own bounds; no asserted value may change). ROUND CAP: RD-618 is at round 2 of 2 under the two-NO-GO cap, so a NO GO on RD-618 goes to Kam, not to a round 3. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no browser.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-29_nexusai-gate-batch9-rd618r2-rd723.md
It opens with TUESDAY'S RULINGS (a) to (f): apply them, do not re-rule them. Then the charter it names, then the two READY mails it names, then the prior reports it names: batch 7 (RD-618's NO GO at 4334b96 with A-F1 MAJOR, A-F2 and A-F3 Minor; the cross-change cell x1-x7 with RD-646+RD-647 608a1cd; the body-parser error-type table) and batch 8 (the most recent gate: its lessons — a K2 full verify cannot pass today, S-1 to S-5 — are carried in the brief's PRIOR ROUND). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-618: branch rd-618-csp-intake-residue-s86m at 874c4f503d0f37a032014e562972b17e903e1072 (7e4cd2e on 1904765007e9447ac6c980f9840c0689a02abe6c, then 4334b96d91132d933bc30b6b8dbd63e2031552cc, batch 7's NO GO head, then 874c4f5; NOT forward-merged). RD-723: rd-723-rd638-e2-budget-s86n at 19fc17ca5aa41e3be3a6b9d174a5d627f4a33145 (816c33a on 6ae20af, a forward merge of main dd15ce1ae8277cc9450e62b11b584a40d2226bf3, counts _updated only). Main at drafting was dd15ce1. The two deltas share NO path but the counts file. RD-618's semantic cross is with RD-646+RD-647 608a1cd99adcc69f6d2cdc552f170e89710adb02 (C-68): keep batch 7's census cross-change cell on a merged tree. OPTIONAL: RD-466 (NexusAI-O) is a member ONLY if the launcher's closing line says so; otherwise report "RD-466: not a member" and do not measure the brief's OPTIONAL TARGET section.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b): RD-681 via PR #32, then batch 3 (RD-685, RD-314), then batch 8 (RD-700, RD-609, RD-648, whose branch is now b12a475) are queued ahead of you, and batch 7's GO members may land. Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MT1 = M0 + RD-723 + RD-618 predicted 4204/253 at M0 = dd15ce1; MT2 = MT1 + 608a1cd predicted 4215/254), the tests census (296 / 298), the harness population, C-187's applicability, which partners are already in. If M0 changes the server entry point (RD-681 does), the merged intake is a COMBINED file no parent holds: parse it and run the C-68 sets on it. Never re-base mid-gate.

C-190 (new since batch 8): every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code. You READ ONLY whether each branch has a PR and its CodeQL result; with no PR, CodeQL is NOT RUN at that head — say so.

RD-618 (TIER 1, round 2 of 2). POSITIVE CONTROL FIRST, RED-AT-PARENT: the head's 13 cells against 4334b96's two product files — S5, S6, R6, R7 red, the other 9 green; quote each failing assertion. Then 13/13 at the head, and the builder's three mutants re-derived INDEPENDENTLY (M-F1 cap removed: S6 and R6 only; M-F2 fallback userinfo strip removed: S5 only; M-F3 non-entity errors passed on again: R7 only). Then your own: M-F3m (the non-entity log line also carries the error message: R7 must redden — the log line never echoing err.message is then GUARDED), M-F1c (cap 11), M-typeless (the type-less next(err) line removed: the drafter READS 13/13 green — guarded by no cell in rd618). Decide A-F1, A-F2 and A-F3 each CLOSED, NARROWED or OPEN by measurement with its red-at-parent arm: s3 (batch 7's unparseable-URL shapes at parent and head) and s3b (the drafter's residuals: userinfo containing ? or #, a leading whitespace value, a backslash authority, a blob wrapper, an upper-case scheme — predictions, not verdicts); s6 (the 319-report 16,270-byte array: at most 10 violation lines and one cap line) and s6a (ring arithmetic: 60 requests a minute times 10 entries is 600 a minute against a 500-entry ring — say whether A-F1 is closed against its own oracle or narrowed to a residue), s6b (a cap line that fires when no cap applied); s7 (charset and encoding markers: 415, marker count 0 beside a control marker that is found) and s7b (request.aborted — the READY's NOT TESTED, discharge it: no crash, no headers-sent error); s4, s8, s9 as regressions. THE CROSS CELL (C-68) on MT2: x1 rd646 + rd618 + rd495 + rd607 by name (the builder's 43/43), x2 Redis refusing: a valid report gets RD-646's NAMED 503 through the type-less next(err), x3 the POSITIVE CONTROL for "type-less errors still go to next()": M-typeless on MT2 must redden CENSUS-B and CENSUS-M with exactly POST /api/csp-report -> 400, x4 RD-646's error given a string type, x5 Redis up and no Redis configured, x6 the coverage view. C-187 APPLIES to RD-618 (it carries image-content-exposure blob 94e6e4c, main has 9ede5fd): predicted missing 2 = C-187's pair, ACCOUNTED only when its (a) and (b) are measured; any other missing id is a STOP.

RD-723 (TIER 2, through-code). POSITIVE CONTROL FIRST, RED-AT-BASE: rd638 at M0 with a listen-delay preload of 2,500 ms acting ONLY in the server child — E2 red with "Exceeded timeout of 5000 ms for a test"; then the head with and without the delay (E2 green, over 5,000 ms with it). t3: the preload's LANDING CONTROL in the same arm — its stderr line once per server child with that child's pid, zero times for the jest worker; delay 0 as the negative control. t4: no asserted value changed — TWO independent instruments (constant substitution against the base, and a token or AST compare of every expect argument and every literal passed to settleWithin, sleep and bootServer), each with a control that is caught; any other change is a Major AND a WRONG item. t6: the stop term — h.stop waits 20 s after SIGTERM (the comment says 5 s each; the drafter READ 120 + 3 + 15 + 20 = 158 s = the budget, zero margin): measure with a server that ignores SIGTERM. t7: a boot slower than bootTimeoutMs must fail with the harness's own message inside the budget, not jest's timeout. t8: the budget does not mask the property — RD-638's own fix removed, E2 red with NOT SETTLED inside the budget. t9 C-185: after RD-723 merges the known-failing set is empty. t10 C-68 with RD-648's harness.

H-15 EXCEPTION (declared, scoped): only rows t1-t3, t6, t7 may pass a preload through NODE_OPTIONS, because the harness spawns rd638's server from inside the cell with the parent's environment and no preload argument; the preload self-gates on the server entry point and t3's landing control is mandatory in the same arm. Everywhere else preloads go in argv with -r.

THE MERGED TREE — part of every verdict (brief section 8). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff 19fc17c, 874c4f5 (MT1); in a separate clone from MT1, merge --no-ff 608a1cd (MT2) unless M0 already holds it. Re-measure every pair by merge-tree in a SCRATCH object dir first — the drafter ran merge-tree in its own scratch object dir: every pair conflicted on the counts file only, and the server entry point merged CLEANLY with 608a1cd and with RD-681 (clean is not unchanged — C-68). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1: predicted 4204/253, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file, the side control run inside the clone that owns the objects. The id-superset control LIKE WITH LIKE, all K1, a copy of batch 7's script proven first to STOP on a planted missing id. On MT1, one hold: every C-68 set by name (the harness union — rd618 and rd638 both require it; the intake readers), rows a2, s6, s7, t2, t9, the full verify, one mutant per ticket; on MT2 x1-x6. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

THE NEGATIVE-ASSERTION SWEEP (brief section 3b, C-102). RD-618 adds early returns to the intake's error handler and a slice that drops entries: for every negative cell among its callers (rd618 R2 R3 R5 R7, rd495's refusals, rd607, rd646's census and every rd646 cell that posts to the intake) show the refusal comes from the branch it is NAMED for, by the log line the handler writes or coverage. RD-723 lengthens how long a cell may run: show E2 still reaches its own red (t8). Self-test first (a positive control, a negative control, a non-empty population) or ABORT. Report population, negative cells, still reaching, disarmed.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only (batch 8 measured that a K2 full verify cannot pass today). Predicted 874c4f5 4146/248, 19fc17c 4191/252, M0 = dd15ce1 4191/252, MT1 4204/253. Every failure by NAME; rd638-export-always-ends E2 is C-185's known CI failure — at M0 it is t1's natural red, at the head it is a finding. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-21 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed before, read raw. H-3: a LANDING CONTROL for every hook, preload, planted report or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server under the network belt, and prove the belt lets a loopback REFUSAL through before trusting "Redis down". H-7: mutants only through a quoted tool with a negative control. H-8: the exact new text present and the old absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon reachable before measuring its absence. H-11: /bin/bash explicitly; every sha:path braced; never set -- or declare -A in the default shell. H-12: list every modified or deleted test file before the C-57 control, and every stale-parent file RD-618 carries at an old blob. H-13: NUL-safe tree censuses. H-14: every driver ends with an END record or the run is VOID. H-15: preloads with -r in argv, never NODE_OPTIONS — except the declared RD-723 rows above. H-16: a plant is what the product will treat it as. H-17: absolute tool paths, and prove the thing STARTED before reading its rc. H-18: zsh eats :s and a leading =; reject the empty-input hash as a VOID read. H-19: gitleaks canaries as real keys. H-20 (standing, from batch 7's ruling f; a hung jest held the NexusAI lock 4.5 h on 2026-09-28): EVERY jest invocation inside a hold carries --forceExit AND runs under a per-step hard deadline (qa-to.sh; targeted 600 s, the C-68 union 2400 s, a full verify 2700 s); a fired deadline aborts that step, is reported by name, and the lock releases through your wrapper's own exit. H-21: every file you mutate is restored in a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, and its hash compared to the pinned blob after every hold; a tree left mutated is quarantined, never reused.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch9.*), status-checked before use (batch 8's S-1). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold scripts. Symlinks, chmod, sockets, held ports, env files and scratch git repos ONLY under your own mktemp dirs. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, never merge anything anywhere the fleet can see. No Azure (no az at all), no demo, no docker, no Partner Center. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 10 of the brief exactly. QUEUE, NEVER TAKE OVER: the NexusAI seats share session-tools/nexusai-lock.sh with you. Every jest run and every server boot goes through it with a tag starting qa-b9- (C-141 gate-class, ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield). When a merge ticket is already queued, file yours with --after that merge ticket's tag (C-141 ADDENDUM 4's tool), never ahead of it; expect a busy queue while RD-681, batch 3 and batch 8 merge. Hold the lock once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of batch 8's copied instrument first); record the foreign count beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request and run has a per-step DEADLINE and a client timeout, every server, Redis stand-in and preloaded child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether either branch has a PR, its CodeQL result, and M0's CI Build and its failing set against C-185's known set, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: both branches, 608a1cd's branch, the queued merges and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be dd15ce1 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch9. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch9] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 9: RD-618 r2 · RD-723
Lead the body with one line per ticket (RD-618 r2: <GO|GO WITH FINDINGS|NO GO> @ 874c4f5 (round 2 of 2 — NO GO goes to Kam) · RD-723: … @ 19fc17c · RD-466: … or not a member), then one line naming M0, your recommended merge order, the merged counts you measured, A-F1 / A-F2 / A-F3 each CLOSED / NARROWED / OPEN, the cross cell's result (x1 count, x3 red?), and the C-57 result with C-187's pair. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list as the brief quotes it, every declared limit L-A1 to L-A4 and L-B1 to L-B2 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, CodeQL at any head without a PR, a real browser's Reporting API delivery, a real Redis server (only a loopback stand-in and a refusing port), a boot slower than the delays driven here, any browser, any deploy, real Azure, Partner Center, the demo, and Windows.
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
for S in "$MAIN_SHA" "$BASE1" "$A_R1" "$A_PARENT" "$A_HEAD" "$B_BASE" "$B_OWN" "$B_MRG" "$B_HEAD" "$D_SHA" "$R648_HEAD" $QUEUED; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: A's with main, B and 608a1cd is 1904765; B's with main is dd15ce1 (B contains main at drafting); 1904765 and 6ae20af are on main.
g merge-base --is-ancestor "$BASE1" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 1904765 is not an ancestor of dd15ce1 — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$B_BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 6ae20af is not an ancestor of dd15ce1 — re-brief" >&2; exit 7; }
for PAIR in "$A_HEAD $MAIN_SHA" "$A_HEAD $B_HEAD" "$A_HEAD $D_SHA"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  [ "$(g merge-base "$X" "$Y" 2>/dev/null)" = "$BASE1" ] || { echo "REFUSING: merge-base(${X:0:7}, ${Y:0:7}) is not 1904765 — re-brief" >&2; exit 7; }
done
[ "$(g merge-base "$B_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(19fc17c, dd15ce1) is not dd15ce1 — RD-723 no longer contains main at drafting" >&2; exit 7; }

# 8 — chains exact, parents exact (compared as sorted SETS of "sha parents" lines).
chainset() { g log --format='%H %P' "${1}..${2}" 2>&1 | sort | tr '\n' '|'; }
want() { printf '%s\n' "$@" | sort | tr '\n' '|'; }
[ "$(chainset "$BASE1" "$A_HEAD")" = "$(want "$A_HEAD $A_PARENT" "$A_PARENT $A_R1" "$A_R1 $BASE1")" ] || { echo "REFUSING: 1904765..RD-618 is not exactly 7e4cd2e -> 4334b96 -> 874c4f5" >&2; exit 8; }
[ "$(chainset "$MAIN_SHA" "$B_HEAD")" = "$(want "$B_HEAD $B_MRG" "$B_MRG $B_OWN $MAIN_SHA" "$B_OWN $B_BASE")" ] || { echo "REFUSING: dd15ce1..RD-723 is not exactly 816c33a (on 6ae20af) -> 9282763 (merge of dd15ce1) -> 19fc17c" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the two ticket branches exactly the pinned heads (REFUSE on mismatch); 608a1cd's branch a NOTE.
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
D_NOW="$(g ls-remote origin "refs/heads/$D_BRANCH" 2>/dev/null | awk '{print $1}')"
[ "$D_NOW" = "$D_SHA" ] || echo "NOTE: origin $D_BRANCH is '${D_NOW:-absent}', not 608a1cd — the cross cell stays pinned on 608a1cd; the gate names the move (C-68)" >&2
# 18b — main MAY move (ruling b). It must be dd15ce1 or a descendant IN THE OBJECT STORE; its movement since dd15ce1 must not touch A's cell file, the
# CSP report service or B's file. The server entry point moving (RD-681) is a NOTE (C-68), not a refusal.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from dd15ce1 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$A_TEST" "$CSP_SRC" "$B_TEST" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved dd15ce1..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from dd15ce1) — the gate re-pins M0 itself and re-bases every prediction" >&2
printf '%s\n' "$MOVED" | grep -qxF "$SERVER_SRC" && echo "NOTE: main's movement changes the server entry point — RD-618's intake merges into a COMBINED file; the gate parses it and re-runs the C-68 sets (C-68)" >&2
printf '%s\n' "$MOVED" | grep -qxF "$HARNESS" && echo "NOTE: main's movement changes the harness (RD-648?) — rd618 and rd638 run under it on M0; the gate says so (brief t10)" >&2
Q_IN=''
for H in $QUEUED "$D_SHA"; do g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null && Q_IN="$Q_IN ${H:0:7}"; done
[ -z "$Q_IN" ] || echo "NOTE: origin main carries queued/partner commit(s):$Q_IN — the gate re-bases counts, census and C-68 populations on M0" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; RD-723 touches no product path.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$A_PARENT" "$A_HEAD" "$A_EXPECTED_FILES" "RD-618 r2 (4334b96..874c4f5)"
chk_delta "$BASE1" "$A_HEAD" "$A_EXPECTED_FILES" "RD-618 (1904765..874c4f5)"
chk_delta "$MAIN_SHA" "$B_HEAD" "$B_EXPECTED_FILES" "RD-723 (dd15ce1..19fc17c)"
[ -z "$(g diff --name-only "$MAIN_SHA" "$B_HEAD" -- backend static docs 2>/dev/null)" ] || { echo "REFUSING: RD-723 touches product or docs — commissioned as test-only" >&2; exit 22; }
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$A_PARENT" "$A_HEAD" "$SERVER_SRC")" = "17 4" ] && [ "$(ns "$A_PARENT" "$A_HEAD" "$CSP_SRC")" = "15 3" ] && [ "$(ns "$A_PARENT" "$A_HEAD" "$A_TEST")" = "59 1" ] || { echo "REFUSING: RD-618 r2's numstats are not server +17/-4, cspReport +15/-3, cells +59/-1 (brief WRONG 1)" >&2; exit 22; }
[ "$(ns "$MAIN_SHA" "$B_HEAD" "$B_TEST")" = "23 7" ] || { echo "REFUSING: RD-723's rd638 change is not +23/-7" >&2; exit 22; }
[ "$(g diff "$MAIN_SHA" "$B_HEAD" -- "$COUNTS_FILE" 2>/dev/null | grep -E '^[+-] ' | grep -vc '"_updated"')" = "0" ] || { echo "REFUSING: RD-723's counts change is not _updated only" >&2; exit 22; }

# 93 — RD-723: no asserted value changed (constant-substitution compare; control must fire: "true false"); blobs as briefed.
[ "$(values_equal "$MAIN_SHA" "$B_HEAD" "$B_TEST")" = "true false" ] || { echo "REFUSING: RD-723's $B_TEST is not equal to dd15ce1's after constant substitution and budget removal (or the control did not fire) — Tuesday's no-asserted-value-change condition" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$B_TEST")" = "$B_TEST_BASE_BLOB" ] && [ "$(blob "$B_BASE" "$B_TEST")" = "$B_TEST_BASE_BLOB" ] && [ "$(blob "$B_HEAD" "$B_TEST")" = "$B_TEST_HEAD_BLOB" ] && [ "$(blob "$B_OWN" "$B_TEST")" = "$B_TEST_HEAD_BLOB" ] || { echo "REFUSING: rd638 blobs are not e7789e5 (6ae20af, dd15ce1) -> fc121f5 (816c33a, 19fc17c)" >&2; exit 93; }

# 94 — RD-618 r2's premises at source.
UI_TXT="const noUserinfo = s.replace(/^([a-z][a-z0-9+.-]*:\/\/)[^/?#]*@/i, '\$1');"
[ "$(cnt "$A_HEAD" "$CSP_SRC" 'const CSP_REPORT_MAX_ENTRIES_PER_REQUEST = 10;')" = "1" ] && [ "$(cnt "$A_PARENT" "$CSP_SRC" 'CSP_REPORT_MAX_ENTRIES_PER_REQUEST')" = "0" ] || { echo "REFUSING: the per-request cap (10) is not present once at 874c4f5 and absent at 4334b96" >&2; exit 94; }
[ "$(cnt "$A_HEAD" "$CSP_SRC" '.slice(0, CSP_REPORT_MAX_ENTRIES_PER_REQUEST);')" = "1" ] && [ "$(cnt "$A_HEAD" "$CSP_SRC" "$UI_TXT")" = "1" ] || { echo "REFUSING: the cap's slice or the fallback userinfo regex is not as briefed" >&2; exit 94; }
[ "$(cnt "$A_HEAD" "$SERVER_SRC" "if (!err || typeof err.type !== 'string') return next(err);")" = "1" ] && [ "$(cnt "$A_HEAD" "$SERVER_SRC" 'CSP report refused (${status}): ${err.type}; nothing stored')" = "1" ] && [ "$(cnt "$A_HEAD" "$SERVER_SRC" 'const status = Number.isInteger(err.status) ? err.status : 400;')" = "1" ] || { echo "REFUSING: the intake's three-branch error handler is not as briefed" >&2; exit 94; }
[ "$(g diff "$A_PARENT" "$A_HEAD" -- "$SERVER_SRC" "$CSP_SRC" 2>/dev/null | grep '^+' | grep -c 'err.message')" = "0" ] || { echo "REFUSING: an added line in RD-618 r2 names err.message" >&2; exit 94; }
for T in "test('S5 — " "test('S6 — " "test('R6 — " "test('R7 — "; do
  [ "$(cnt "$A_HEAD" "$A_TEST" "$T")" = "1" ] && [ "$(cnt "$A_PARENT" "$A_TEST" "$T")" = "0" ] || { echo "REFUSING: cell '$T' is not new at 874c4f5" >&2; exit 94; }
done
[ "$(blob "$A_PARENT" "$SERVER_SRC")" = "$SERVER_PARENT_BLOB" ] && [ "$(blob "$A_HEAD" "$SERVER_SRC")" = "$SERVER_HEAD_BLOB" ] && [ "$(blob "$BASE1" "$SERVER_SRC")" = "$SERVER_BASE_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SERVER_SRC")" = "$SERVER_BASE_BLOB" ] || { echo "REFUSING: server blobs are not bc099b2 (1904765, dd15ce1), c5bd870 (4334b96), e076121 (874c4f5)" >&2; exit 94; }
[ "$(blob "$A_PARENT" "$CSP_SRC")" = "$CSP_PARENT_BLOB" ] && [ "$(blob "$A_HEAD" "$CSP_SRC")" = "$CSP_HEAD_BLOB" ] && [ "$(blob "$MAIN_SHA" "$CSP_SRC")" = "$CSP_BASE_BLOB" ] || { echo "REFUSING: cspReport blobs are not f102d26 (dd15ce1), fa868ea (4334b96), 4b38e90 (874c4f5)" >&2; exit 94; }
[ "$(blob "$A_PARENT" "$A_TEST")" = "$A_TEST_PARENT_BLOB" ] && [ "$(blob "$A_HEAD" "$A_TEST")" = "$A_TEST_HEAD_BLOB" ] || { echo "REFUSING: rd618 cell blobs are not 2b5130b -> 8bbfcc7" >&2; exit 94; }
[ "$(blob "$M_ORIGIN" "$SERVER_SRC")" = "$SERVER_BASE_BLOB" ] || echo "NOTE: the server entry point on origin main ${M_ORIGIN:0:7} is not bc099b2 — RD-618 merges into a combined file there (C-68)" >&2

# 95 — the cross partner 608a1cd: its named error is TYPE-LESS with statusCode 503; its census cells exist.
[ "$(blob "$D_SHA" "$SERVER_SRC")" = "$SERVER_D_BLOB" ] || { echo "REFUSING: 608a1cd's server is not 4ddf75f" >&2; exit 95; }
[ "$(cnt "$D_SHA" "$SERVER_SRC" 'e.statusCode = 503;')" = "1" ] && [ "$(cnt "$D_SHA" "$SERVER_SRC" "e.code = 'RATE_LIMIT_STORE_UNAVAILABLE';")" = "1" ] || { echo "REFUSING: 608a1cd's named error is not statusCode 503 / RATE_LIMIT_STORE_UNAVAILABLE" >&2; exit 95; }
[ "$(cnt "$D_SHA" "$D_TEST" "test('CENSUS-B — ")" = "1" ] && [ "$(cnt "$D_SHA" "$D_TEST" "test('CENSUS-M — ")" = "1" ] || { echo "REFUSING: 608a1cd's CENSUS-B / CENSUS-M cells are not as briefed" >&2; exit 95; }

# 96 — C-187 APPLIES: image-content-exposure at the old blob on A and 608a1cd, the new one on main.
[ "$(blob "$BASE1" "$ICE")" = "$ICE_OLD_BLOB" ] && [ "$(blob "$A_HEAD" "$ICE")" = "$ICE_OLD_BLOB" ] && [ "$(blob "$D_SHA" "$ICE")" = "$ICE_OLD_BLOB" ] && [ "$(blob "$MAIN_SHA" "$ICE")" = "$ICE_NEW_BLOB" ] && [ "$(blob "$B_HEAD" "$ICE")" = "$ICE_NEW_BLOB" ] || { echo "REFUSING: image-content-exposure blobs are not 94e6e4c (1904765, 874c4f5, 608a1cd) / 9ede5fd (dd15ce1, 19fc17c) — C-187's premise" >&2; exit 96; }
[ "$(blob "$M_ORIGIN" "$ICE")" = "$ICE_NEW_BLOB" ] || echo "NOTE: image-content-exposure on origin main ${M_ORIGIN:0:7} is not 9ede5fd — C-187 says that is a STOP unless re-ruled; the gate measures it" >&2

# 97 — RD-723's premises: the constants, the budget sum, h.stop's 20 s bound (the comment says "5 s each"), no testTimeout anywhere.
for T in 'const E1_SETTLE_MS = 10000;' 'const MARGIN_MS = 10000;' 'const E2_BOOT_MS = 120000;' 'const E2_SETTLE_SLEEP_MS = 3000;' 'const E2_EXPORT_WITHIN_MS = 15000;' 'const E2_STOP_MS = 10000;' \
         'const E2_BUDGET_MS = E2_BOOT_MS + E2_SETTLE_SLEEP_MS + E2_EXPORT_WITHIN_MS + E2_STOP_MS + MARGIN_MS;' '}, E1_SETTLE_MS + MARGIN_MS);' '}, E2_BUDGET_MS);' '(SIGTERM grace then SIGKILL, 5 s each)'; do
  [ "$(cnt "$B_HEAD" "$B_TEST" "$T")" = "1" ] || { echo "REFUSING: '$T' is not present once in rd638 at 19fc17c" >&2; exit 97; }
done
[ "$(cnt "$MAIN_SHA" "$HARNESS" 'const stopBy = Date.now() + 20000;')" = "1" ] && [ "$(blob "$MAIN_SHA" "$HARNESS")" = "$HARNESS_BLOB" ] && [ "$(blob "$B_HEAD" "$HARNESS")" = "$HARNESS_BLOB" ] && [ "$(blob "$A_HEAD" "$HARNESS")" = "$HARNESS_BLOB" ] || { echo "REFUSING: the harness is not 2453a3f with h.stop's 20 s bound (brief WRONG 6)" >&2; exit 97; }
[ "$(blob "$R648_HEAD" "$HARNESS")" = "$HARNESS_R648_BLOB" ] || echo "NOTE: RD-648's b12a475 harness is not c826c1e — brief §1 and t10 need re-reading" >&2
[ "$(g show "${B_HEAD}:package.json" 2>/dev/null | grep -c 'testTimeout')" = "0" ] && [ "$(cnt "$B_HEAD" "$B_TEST" 'jest.setTimeout')" = "0" ] || { echo "REFUSING: a testTimeout / jest.setTimeout exists — the READY's CAUSE no longer holds" >&2; exit 97; }

# 92 — the harness's REQUIRE population (not a name grep): 22 at dd15ce1 and 19fc17c, 23 at 874c4f5 (rd618 is a consumer); main-now noted.
[ "$(harness_pop "$MAIN_SHA")" = "$HARNESS_POP_MAIN" ] && [ "$(harness_pop "$B_HEAD")" = "$HARNESS_POP_MAIN" ] || { echo "REFUSING: harness require-population at dd15ce1/19fc17c is not $HARNESS_POP_MAIN — re-brief" >&2; exit 92; }
[ "$(harness_pop "$A_HEAD")" = "$HARNESS_POP_A" ] || { echo "REFUSING: harness require-population at 874c4f5 is '$(harness_pop "$A_HEAD")', not $HARNESS_POP_A — re-brief" >&2; exit 92; }
[ "$(g grep -l -E "require\([^)]*rd395-server-harness" "$A_HEAD" -- "$A_TEST" 2>/dev/null | wc -l | tr -d ' ')" = "1" ] && [ "$(g grep -l -E "require\([^)]*rd395-server-harness" "$B_HEAD" -- "$B_TEST" 2>/dev/null | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: rd618 / rd638 do not both require the harness" >&2; exit 92; }
HP_NOW="$(harness_pop "$M_ORIGIN")"
[ "$HP_NOW" = "$HARNESS_POP_MAIN" ] || echo "NOTE: at origin main ${M_ORIGIN:0:7} the harness require-population is ${HP_NOW:-?} (brief: $HARNESS_POP_MAIN at dd15ce1) — the gate re-derives it on M0" >&2

# 23 — EXPECTED OVERLAPS: A's and B's deltas (each over its own merge-base with main) share the counts file and nothing else.
COMMON="$(comm -12 <(g diff --name-only "$BASE1" "$A_HEAD" 2>/dev/null | sort) <(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort) | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
[ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: RD-618 and RD-723 share '${COMMON:-<nothing>}', expected '$COUNTS_FILE' only" >&2; exit 23; }

# 35 — counts at every pinned sha.
for PAIR in "$BASE1 4133 247" "$A_R1 4141 248" "$A_PARENT 4142 248" "$A_HEAD 4146 248" "$MAIN_SHA 4191 252" "$B_BASE 4176 250" "$B_OWN 4176 250" "$B_HEAD 4191 252" "$D_SHA 4144 248"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$BASE1" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$A_PARENT" "$B_HEAD" "$D_SHA"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge premise by a REAL merge-tree in a scratch object dir OUTSIDE NexusAI (NexusAI's objects are a read-only alternate).
MT_OBJ="$(mktemp -d "${TMPDIR:-/tmp}/qa-b9-mergetree.XXXXXX")" || { echo "REFUSING: cannot make a scratch object dir for guard 80" >&2; exit 80; }
mtree() { GIT_OBJECT_DIRECTORY="$MT_OBJ" GIT_ALTERNATE_OBJECT_DIRECTORIES="$REPO/.git/objects" git -C "$REPO" merge-tree --write-tree --name-only "$1" "$2" 2>&1; }
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$A_HEAD $B_HEAD" "$A_HEAD $D_SHA" "$B_HEAD $D_SHA"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  OUT="$(mtree "$X" "$Y")"; RC=$?
  CONF="$(printf '%s\n' "$OUT" | sed -n '2,/^$/p' | sed '/^$/d' | tr '\n' ' ' | sed 's/ $//')"
  { [ "$RC" = "0" ] && [ -z "$CONF" ]; } || { [ "$RC" = "1" ] && [ "$CONF" = "$COUNTS_FILE" ]; } || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} rc=$RC conflicted '${CONF:-?}' — not counts-only (80); scratch objects in $MT_OBJ" >&2; exit 80; }
done
[ -d "$REPO/.git/objects" ] || { echo "REFUSING: $REPO/.git/objects is not a directory — the alternate would be wrong" >&2; exit 80; }

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$PREV_B7" "$PREV_B8" "$PREV_B7_BRIEF" "$PREV_B8_BRIEF" \
         "$EV_M/rd618c-hold.log" "$EV_M/rd618c-hold.sh" "$EV_M/mx618c.log" "$EV_M/mx618x646.sh" \
         "$EV_N/rd723/hold.sh" "$EV_N/rd723/hold.out" "$EV_N/rd723/slow-boot-preload.js" "$EV_N/rd723/A1-main-nodelay.json" "$EV_N/rd723/A2-main-delay2500.json" \
         "$EV_N/rd723/B1-branch-delay2500.json" "$EV_N/rd723/B2-branch-nodelay.json" "$EV_N/rd723/verify.log" "$EV_N/rd723/named.log" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$B7_EV/qa-a-probe.js" "$B7_EV/qa-d-probe.js" "$B7_EV/qa-census-pop.py" "$B7_EV/qa-cov7.js" "$B7_EV/qa-mutate.py" "$B7_EV/qa-clone.sh" \
         "$B7_EV/qa-merge.sh" "$B7_EV/qa-c57-id-superset.sh" "$B7_EV/q-merged-identity.py" "$B7_EV/qa-codeonly.js" "$B7_EV/qa-to.sh" "$B7_EV/qa-holdlib.sh" \
         "$B7_EV/qa-jestwrap.sh" "$B7_EV/qa-runj.sh" "$B7_EV/qa-h1-selftest.sh" "$B7_EV/qa-h1-scan.py" "$B7_EV/qa-netbelt.sb" "$B7_EV/qa-netbelt-ctl.js" \
         "$B7_EV/qa-srvlib.js" "$B7_EV/qa-lockcheck.js" "$B7_EV/qa-ssprint.sh" \
         "$B8_EV/qa-floorlib.sh" "$B8_EV/qa-floorcount.py" "$B8_EV/qa-c112-census.py" "$B8_EV/qa-passset.py" "$B8_EV/qa-sweep.py" "$B8_EV/qa-sink-ctl.js" \
         "$B8_EV/qa-slow-health-preload.js" "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-618 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:12}" "$READY_B" || { echo "REFUSING: the RD-723 READY does not name ${B_HEAD:0:12}" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4146/4146 tests passed across 248 suites' "$EV_M/rd618c-hold.log" && grep -qF 'VERDICT: PASS — 4191/4191 tests passed across 252 suites' "$EV_N/rd723/verify.log" && grep -qF 'Tests:       43 passed, 43 total' "$EV_M/mx618c.log" || { echo "REFUSING: a builder log no longer carries the READY's result line" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B7" "$PREV_B8" "$READY_A" "$READY_B"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 60 — the OPTIONAL member RD-466: validated only when stamped.
O_LINE="RD-466 (NexusAI-O) is NOT a member of this gate: report \"RD-466: not a member\" and do not measure the brief's OPTIONAL TARGET section."
if [ -n "$O_HEAD$O_BRANCH$O_READY" ]; then
  [[ "$O_HEAD" =~ ^[0-9a-f]{40}$ ]] && [ -n "$O_BRANCH" ] && [ -s "$O_READY" ] || { echo "REFUSING: RD-466 is half-stamped (O_HEAD 40-hex, O_BRANCH and an on-disk O_READY are all required)" >&2; exit 60; }
  [ "$(g cat-file -t "$O_HEAD" 2>&1)" = "commit" ] || { echo "REFUSING: RD-466 head $O_HEAD is not in the object store" >&2; exit 60; }
  g ls-remote origin "refs/heads/$O_BRANCH" 2>/dev/null | grep -q "^${O_HEAD}[[:space:]]" || { echo "REFUSING: origin refs/heads/$O_BRANCH is not $O_HEAD" >&2; exit 60; }
  if g merge-base --is-ancestor "$O_HEAD" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: RD-466 ${O_HEAD:0:7} is already on main" >&2; exit 60; fi
  [ "$(cnt "$O_HEAD" "$ICE" 'expect(globs.length).toBeGreaterThanOrEqual(6);')" = "1" ] || { echo "REFUSING: RD-466's PRECONDITION wildcard floor does not read 6 at ${O_HEAD:0:7} (brief §OPT o1)" >&2; exit 60; }
  grep -qF "${O_HEAD:0:7}" "$O_READY" || { echo "REFUSING: the RD-466 READY does not name ${O_HEAD:0:7}" >&2; exit 60; }
  grep -qF "$O_READY" "$BRIEF" || { echo "REFUSING: brief §OPT does not name the RD-466 READY $O_READY" >&2; exit 60; }
  O_LINE="RD-466 (NexusAI-O) IS A MEMBER (TIER 2, through-code): branch $O_BRANCH at $O_HEAD, READY $O_READY — measure the brief's OPTIONAL TARGET section o1-o4 and give it its own verdict."
fi

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-618 is TIER 1' 'RD-723 is TIER 2 (through-code)' 'ROUND 2 OF 2' 'goes to KAM, not to a round 3' 'One verdict PER ticket' 'TIER 1 AT FULL WEIGHT' 'TIER 2 AT THROUGH-CODE WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-618 FIX ROUND 2 (TIER 1, ROUND 2 OF 2' 'RD-723 (TIER 2, through-code' 'goes to Kam, not to a round 3' 'one verdict per ticket'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$BASE1" "$A_PARENT" "$MAIN_SHA" "$D_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$A_R1" "$B_BASE" "$B_OWN" "$B_MRG" "$R648_HEAD"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
done
for S in "$SERVER_BASE_BLOB" "$SERVER_PARENT_BLOB" "$SERVER_HEAD_BLOB" "$CSP_PARENT_BLOB" "$CSP_HEAD_BLOB" "$A_TEST_PARENT_BLOB" "$A_TEST_HEAD_BLOB" \
         "$B_TEST_BASE_BLOB" "$B_TEST_HEAD_BLOB" "$HARNESS_BLOB" "$LOCK_BLOB" "$ICE_OLD_BLOB" "$ICE_NEW_BLOB"; do
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
WORDS="RD-618 RD-723 RD-646+RD-647 RD-466 A-F1 A-F2 A-F3 C-57 C-68 C-89 C-104 C-112 C-125 C-141 ADDENDUM C-174 C-185 C-187 C-190 C-49 C-102
RED-AT-PARENT RED-AT-BASE M-F1 M-F2 M-F3 M-F3m M-F1c M-typeless s3b s6a s6b s7b x1 x3 x4 x6 t3 t4 t6 t7 t8 t9 t10 MT1 MT2 CENSUS-B CENSUS-M
L-A1 L-A4 L-B1 L-B2 H-1 H-15 H-19 H-20 H-21 --forceExit trap%on%EXIT deadline err.message NODE_OPTIONS LANDING%CONTROL
4204/253 4215/254 4146/248 4191/252 missing%2 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request
POSITIVE%CONTROL%FIRST NEGATIVE-ASSERTION%SWEEP node%--check VOID EXCLUSIVE qa-b9- QUEUE,%NEVER%TAKE%OVER --after DEADLINE HEARTBEAT
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN CodeQL
Prior%work FOREGROUND never%push NEVER%merge Partner%Center batch%7 batch%8 M0"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## OPTIONAL TARGET' '^## 8. THE MERGED TREE' '^## 10. Floor discipline' \
         '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-B1 L-B2; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
# every builder's NOT TESTED list is carried verbatim (distinctive fragments, checked in the READY AND the brief)
for PAIR in "$READY_A|- A real browser's Reporting API delivery (the cells POST the array shape directly)." \
            "$READY_A|- The demo revision (RD-76; nothing deployed)." \
            "$READY_A|- A 415 caused by other body-parser types (request.aborted and similar) — the same code path, not driven." \
            "$READY_B|NOT TESTED: CI itself (Linux) until the branch's Build runs; whether 120 s is ever the true boot cost (it is the cell's own bootTimeoutMs, not a new number)."; do
  F="${PAIR%%|*}"; T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the NOT TESTED fragment '$T' verbatim" >&2; exit 19; }
done
# the rulings the brief rests on are quoted from source and still say so
for PAIR in "A Major at round 2 of 2 is ticketed, not sent to Kam." \
            "Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code" \
            "Main's CI known-failing set is {rd638-export-always-ends E2}, BY NAME, until RD-723 merges" \
            "Any OTHER missing id is still a STOP." \
            "a clean merge-tree and a changed measured surface are not in tension"; do
  grep -qF -- "$PAIR" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$PAIR' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$PAIR" "$BRIEF" || { echo "REFUSING: brief does not quote '$PAIR'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b9-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
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
for w in 'RED-AT-PARENT' 'RED-AT-BASE' 'M-typeless' 'guarded by no rd618 cell' 'C-187 APPLIES' 'missing 2' 'C-190' 'NEVER opens, comments on, approves or merges a PR' \
         'declared exception' '4204/253' '4215/254' 'zero margin' '20,000 ms' 'ADD ONLY IF Tuesday stamps it with a head sha' \
         'K2 (`git archive`) FULL verify cannot pass today' 'RE-BASE EVERY PREDICTION' 'COMBINED' 'H-20' 'H-21' 'NEVER merges and never pushes'; do
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
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 96 97 92 23 35 70 80 31 39 10 17 60 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 38); stamp NOT complete." >&2
  echo "  merge-tree scratch objects (guard 80): $MT_OBJ" >&2
  echo "REFUSING: a stamp placeholder remains (the brief's SELF-CHECK line / Self-check note / §10 seats, or this launcher's NEG_SEATS) — the coordinator re-reads end-to-end and stamps them before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7} at $PIN_TS (18); $D_BRANCH ${D_NOW:0:7} (pinned 608a1cd)"
  echo "  main ${M_ORIGIN:0:7} (dd15ce1 or a descendant; no member path moved) (18b); harness population there ${HP_NOW:-?} (92); queued/partner on main:${Q_IN:- none}"
  echo "  merge-bases (7); chains (8); deltas (22); RD-723 values (93); RD-618 premises (94); 608a1cd (95); C-187 (96); RD-723 premises (97)"
  echo "  overlaps (23); counts (35); package-lock ${LOCK_BLOB:0:7} (70); merge-tree counts-only (80, $MT_OBJ); evidence (31); RD-466 (60): ${O_HEAD:-not a member}"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS (38)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

$O_LINE

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$D_BRANCH = ${D_NOW:-absent} (the cross cell stays on 608a1cd); refs/heads/main = $M_ORIGIN (dd15ce1 or a descendant; no member path moved since dd15ce1; harness require-population there ${HP_NOW:-unread}; queued/partner commits on it:${Q_IN:- none}). Merge-tree (scratch objects, counts-only) held for main x each member, the member pair, and each member x 608a1cd. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
