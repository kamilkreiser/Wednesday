#!/bin/bash
# launch_qa_nexusai_gate_batch1.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #1"), FIVE targets,
# FIVE verdicts, ONE report (2026-09-26):
#   A — RD-447 (TIER 1): rd-447-utf16-scan-s84o @ 911e706 (one commit off 7c47ec4, change + counts). Helper decodes UTF-16/32. 4033/236.
#   B — RD-411 (TIER 1): rd-411-machine-labels-s84o @ ed01f7e = 7be79f0 (off 7c47ec4) + d81cd97 (forward merge of 11666d3) + counts.
#       Same helper, machine-shaped labels. 4040/238.
#   C — RD-533 (TIER 2): rd-533-listen-eaddrinuse-s84m @ 95c3c9a (one commit off 7c47ec4). Listen error -> named failure + exit 1. 3982/236.
#   D — RD-627a (TIER 1): rd-627a-erasure-tmp-siblings-s84n @ 057016d = 9fb9431 (off 7c47ec4) + forward merge of 11666d3 (counts
#       regenerated inside the merge). Erasure reaches interrupted-write .tmp siblings. 4017/238.
#   E — RD-315 (TIER 1): rd-315-no-fabricated-completion-s84m @ 1524fca (one commit off 0863711). /api/database undated rows -> null. 3990/237.
#   Main at drafting 12b5edc (= RD-200's head, fast-forwarded). NOT file-disjoint: A∩B = the helper, C∩E∩main(RD-579) = the server entry
#   point; both auto-merge (drafter's merge-tree in a scratch object dir). The gate RE-PINS main (M0) at its start and verifies the merged
#   tree M0 + all five in its OWN scratch clone, counts regenerated once (predicted counts(M0) + 96/+5; 4117/243 at 12b5edc).
#
# AUTHORITY: Tuesday's batch #1 commission (2026-09-26); READY mails from NexusAI-O (RD-411), -M (RD-533, RD-315), -N (RD-627a, updated),
# copies in briefs/; RD-447's READY is not on disk (facts relayed by the commission). Merges: Tuesday's GO (Kam 2026-09-25 ~22:0x).
#
# PATTERN: launch_qa_nexusai_gate_batch2.sh (guard families 9 6 7 8 18 22 75 23 35 70 31 39 10 17 11 12-15 20 19 24 53 71 76 77 38 32 40),
# prompt EMBEDDED. CHANGES, each deliberate:
#   - 18: FIVE ticket branches must equal the pinned heads (refuse on mismatch). MAIN IS EXPECTED TO MOVE (P merging RD-444/RD-428):
#     main must be 12b5edc or a descendant present in the object store (never fetched), and 12b5edc..main must share no path with the
#     five deltas except the counts file — else REFUSE (re-brief). The launcher's reading of main is passed to the gate as a hint; the
#     gate re-pins M0 itself.
#   - 7/8: per-ticket bases (7c47ec4 x2, 11666d3 x2, 0863711) and main's seven-commit line exact.
#   - 75: only RD-411's tip is counts-only; the two forward merges (d81cd97, 057016d) added nothing of main's beyond main's own files.
#   - 23: EXPECTED OVERLAPS instead of disjointness: A∩B = {helper, counts}, C∩E = {server entry point, counts}, C∩M = {same}; all else counts.
#   - 78 (NEW, from batch #2's S-3): the brief carries the byte-plant rule (Buffer + xxd) — H-9.
#   - 79 (NEW, from batch #2's S-2/S-1): the brief carries H-7/H-8 (quoted mutant tool, insertion-aware landing rule).
#   - 40: the routing line QA/NexusAI-batch1 exists (checked AFTER the stamp so --check refuses on the stamp only).
#   - 32: SELF-CHECK stamp, placeholder @STAMP@ (comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch1' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch1.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..79 a guard refused
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
BRIEF="$BRIEFS/2026-09-26_nexusai-gate-batch1-rd447-rd411-rd533-rd627a-rd315.md"
READY_B="$BRIEFS/2026-09-26_nexusai-rd411-READY-mail.txt"
READY_C="$BRIEFS/2026-09-26_nexusai-rd533-READY-mail.txt"
READY_D="$BRIEFS/2026-09-26_nexusai-rd627a-READY-updated-mail.txt"
READY_D0="$BRIEFS/2026-09-26_nexusai-rd627a-READY-mail.txt"
READY_E="$BRIEFS/2026-09-26_nexusai-rd315-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_O="$NX/session-tools/s84o"
EV_M="$NX/session-tools/s84m"
EV_N="$NX/session-tools/s84n/rd627a"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
PREV_B2="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/report.md"
PREV_G="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md"
B2_EV="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch2-rd428-rd444-rd200/evidence"
PREV_FLOORLIB="$B2_EV/qa-floorlib.sh"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch1'

BASE_SHA='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'      # RD-447, RD-533, RD-411's and RD-627a's build base
MAIN_M1='0863711261afc5f3323b8c4fc480d65109b17ba7'       # merge 1 (RD-579) — RD-315's base
MAIN_M2='11666d3c4f615190646914270016419fffa642e2'       # merge 2 (RD-639) — RD-411's and RD-627a's forward-merge base
MAIN_SHA='12b5edc31ee4ef52415d1cbffbbb0504d7f4715c'      # origin main at drafting (RD-200's head, fast-forwarded)
RD579='cac9cf641c86ff89a48aa42d7447cdcfbbeaa6c1'
RD639='fe53540fbaf628fa3ca5eb790d023ecf5ae71f0c'
RD200_BUILD='4f97260c5c4682913cd785ff8569ce1bc490fe70'
RD200_FWD='c01190d0dcc416554074e751a86eca45398cede3'
A_BRANCH='rd-447-utf16-scan-s84o'
A_HEAD="${QA_A_HEAD_OVERRIDE:-911e706859cbbe49ef32d4166ab9b3271bf98d08}"
B_BRANCH='rd-411-machine-labels-s84o'
B_BUILD='7be79f041a98e09655d067aedc9d8dcbc0e03ac4'
B_FWD='d81cd973ed175735b509b22f4af5e0b98f067ae8'
B_HEAD="${QA_B_HEAD_OVERRIDE:-ed01f7eb02430de74ccaaa6d6f265c7638e5aab4}"
C_BRANCH='rd-533-listen-eaddrinuse-s84m'
C_HEAD="${QA_C_HEAD_OVERRIDE:-95c3c9a9d39429f9093270e283e531f3cda4e88d}"
D_BRANCH='rd-627a-erasure-tmp-siblings-s84n'
D_BUILD='9fb94311b010c3d4355418eface0e1dc3ecd3795'
D_HEAD="${QA_D_HEAD_OVERRIDE:-057016de2b2929c23f643b7346413199f370d3ce}"
E_BRANCH='rd-315-no-fabricated-completion-s84m'
E_HEAD="${QA_E_HEAD_OVERRIDE:-1524fca7ec72b23a4f000b77872a4158f8e14f86}"

COUNTS_FILE='scripts/verify-expected-counts.json'
HELPER='__tests__/helpers/image-manifest.js'
SERVER='backend/server.js'
A_EXPECTED_FILES="$HELPER
__tests__/rd447-utf16-text-is-decoded.test.js
$COUNTS_FILE"
B_EXPECTED_FILES="$HELPER
__tests__/rd411-machine-shaped-labels.test.js
$COUNTS_FILE"
B_BUILD_FILES="$HELPER
__tests__/rd411-machine-shaped-labels.test.js"
C_EXPECTED_FILES="__tests__/rd533-listen-error-fails-loudly.test.js
$SERVER
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/rd627a-erasure-tmp-siblings.test.js
backend/customerDataFiles.js
backend/dataErasure.js
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/rd315-api-database-no-fabricated-completion.test.js
$SERVER
$COUNTS_FILE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='88756 10246 10643 11987 91386'   # NexusAI-M %11, -N %12, -O %13, -P %14, Tuesday %0 — read 2026-09-26 09:09:53 AEST

SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-447: '
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch1] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, the Log Analytics path of /api/database, a real browser render of an undated row, text encodings other than UTF-8, UTF-16 and UTF-32, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI with FIVE targets, FIVE verdicts and ONE report: RD-447 (TIER 1), RD-411 (TIER 1), RD-533 (TIER 2), RD-627a (TIER 1) and RD-315 (TIER 1). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict; a finding that exists only in a COMPOSITION is graded on the merged tree and named against both tickets it joins.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-26_nexusai-gate-batch1-rd447-rd411-rd533-rd627a-rd315.md
Then the charter it names, then the four READY mails it names (RD-627a has two: read both; RD-447 has none on disk — its facts are RELAYED in the brief and cross-read against the builder's logs), then the two previous batched gate reports it names (2026-09-26-gate-batch2-rd428-rd444-rd200 and 2026-09-25-gate-rd579-rd639) — their method and their self-corrections, which the brief's section 3a turns into rules H-1 to H-12 that bind you. Every builder statement is a CLAIM, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-447: branch rd-447-utf16-scan-s84o at 911e706859cbbe49ef32d4166ab9b3271bf98d08, one commit off 7c47ec467f585e9db5daf3a82cdb96deae0b1e7a (change and counts together); the image-manifest test helper and one new cell file. RD-411: branch rd-411-machine-labels-s84o at ed01f7eb02430de74ccaaa6d6f265c7638e5aab4 = 7be79f041a98e09655d067aedc9d8dcbc0e03ac4 (off 7c47ec4), forward-merged onto main 11666d3c4f615190646914270016419fffa642e2 at d81cd973ed175735b509b22f4af5e0b98f067ae8, plus counts; the SAME helper, a different hunk. RD-533: branch rd-533-listen-eaddrinuse-s84m at 95c3c9a9d39429f9093270e283e531f3cda4e88d, one commit off 7c47ec4; the listen callback in the server entry point. RD-627a: branch rd-627a-erasure-tmp-siblings-s84n at 057016de2b2929c23f643b7346413199f370d3ce = 9fb94311b010c3d4355418eface0e1dc3ecd3795 (off 7c47ec4) merged forward onto 11666d3 (counts regenerated inside the merge); the erasure purge and the customer-data file list. RD-315: branch rd-315-no-fabricated-completion-s84m at 1524fca7ec72b23a4f000b77872a4158f8e14f86, one commit off 0863711261afc5f3323b8c4fc480d65109b17ba7; the two /api/database transforms in the server entry point. These deltas are NOT file-disjoint: RD-447 and RD-411 both edit the helper; RD-533, RD-315 and main's RD-579 all edit the server entry point. The drafter's merge-tree says both auto-merge and only the counts file conflicts — prove it yourself.

MAIN IS MOVING. Main at drafting was 12b5edc31ee4ef52415d1cbffbbb0504d7f4715c (RD-200's head, fast-forwarded); NexusAI-P is merging RD-444 and RD-428 tonight. RE-PIN main at your start and call it M0: it must be 12b5edc or a descendant, and 12b5edc..M0 must share no path with the five deltas except the counts file (else STOP and ask). Your merged tree is M0 plus all five. If main moves again during your gate, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

RD-447 (TIER 1) — WIDE TEXT DECODED. POSITIVE CONTROL FIRST: the cell file red at 7c47ec4 (RELAYED 40 red / 15 green, but the builder's separate red log says 40/9/49 — resolve which) and 55/55 at the head. Mutants M-A1 to M-A8 (M-A2, the reader back to utf8, reddens only ONE cell — say which, and whether it catches a caller that bypasses the reader). Every row a1 to a19 of table 2a. The seven consumers that read text, and which of them reads bytes and which a UTF-8 string. The real tree's wide files. Prior work: the RD-429 gate's F1.

RD-411 (TIER 1) — MACHINE-SHAPED LABELS. POSITIVE CONTROL FIRST: 24 red / 4 green at base, 28/28 at the head. Mutants M-B1 to M-B7, including whether any cell pins the 24-character window (RD-386's question is Kam's). The newly-labelled-lines census over every shipped file. labelForm edge shapes. Prior work: S59's WIP c026e94.

THE COMPOSITION (RD-447 x RD-411) — NEITHER BUILDER HAS RUN IT. A UTF-16 or UTF-32 file carrying a machine-shaped label beside a GUID (AZURE_TENANT_ID=, "tenantId":, tenant_id:, TenantID, AADTenantId) is found by NEITHER head alone and only by the merged helper: rows a4 to a10, with the near-miss controls a11, the reviewed-file reopen a18, and a19 — the REAL shipped tree has no unreviewed carrier on the merged tree, beside a detector-live control. Plant every wide row as BYTES with a Node Buffer and check its first bytes with xxd before use (H-9); never build a wide plant with echo, printf, a heredoc or JSON.stringify. The composition's own mutant M-AB must take a4 to 0.

RD-533 (TIER 2) — A SERVER THAT CANNOT LISTEN. POSITIVE CONTROL FIRST: three B cells red at 7c47ec4, the A control green, 4/4 at the head, with a landing control that A really holds the port before B starts. Mutants M-C1 to M-C6. Rows c1 to c9: a real two-server EADDRINUSE on loopback (separate and SHARED DATA_DIR — did B's pre-listen boot write into A's store?), the file log transport, and the EACCES-shaped case c4 (PORT is a raw string, so a socket path inside your own chmod-500 directory reaches listen), a low port on this Mac, an out-of-range port, a non-node holder, a loopback-only holder, SIGTERM inside the 250 ms window. The harness consumers and the C-68 set of 10 suites. The Express once('error') residue is pre-existing: census it, do not grade it on RD-533.

RD-627a (TIER 1) — ERASURE REACHES INTERRUPTED-WRITE COPIES. POSITIVE CONTROL FIRST, in YOUR tree: T1, T2, T4 red on 11666d3's product code, POPULATION and T3 green; 5/5 at the head. Mutants M-D1 to M-D7 (M-D4: no cell guards the unlistable-directory failure — name the gap). Rows d1 to d14 on a REAL DATA_DIR of your own, through the product path and on a real loopback server, the ledger and erasure-audit.jsonl read RAW: bare and pid-suffixed siblings, directory siblings, a SYMLINKED sibling to a file and to a directory outside DATA_DIR (link gone, target intact, failure naming it), dangling, inside-DATA_DIR links in both loop orders, the RD-639 live-store symlink rule meeting a symlinked sibling in one loop iteration, the sweeper re-drive (the known B-F1 / RD-684 hole — measure and name it), every T3 control and .machine-id itself surviving, an unlistable DATA_DIR, a hard-linked sibling, a sibling born after the listing, and backups/. The RD-639 rule re-run by name on the merged tree.

RD-315 (TIER 1) — NO FABRICATED COMPLETION. POSITIVE CONTROL FIRST: print and scan red at 0863711 with the REQUEST TIME quoted, control and findability green, 4/4 at the head; seed through the product's own SimpleDatabase BEFORE boot. Mutants M-E1 to M-E5. Rows e1 to e8, including the empty-string completion, reachability of a doubly-undated row, and what sorts or filters do with null. THE CENSUS (census only, not a fix): every new Date(), Date.now() and new Date().toISOString() site in the server entry point on the merged tree, classified now-stamp / fallback-for-a-missing-time / default window / other, starting from the drafter's seven candidates and proven complete by finding RD-315's own two lines at 0863711. A remaining fallback is a new-ticket recommendation, not RD-315's verdict, unless it sits in the two /api/database transforms.

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 911e706, ed01f7e, 95c3c9a, 057016d, 1524fca (RD-447 before RD-411, as the builder asked). Predict before each merge whether the counts file conflicts, and explain any clean merge with a side control; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Resolve the counts by REGENERATION, never by hand: npm run verify -- --maxWorkers=2 --update-counts ONCE on the tree after ALL FIVE merges. Predicted counts(M0) plus 96 tests and 5 suites — 4117/243 if M0 is 12b5edc — a prediction; the measurement decides. Build a second clone in reverse order and prove the two root trees identical apart from the counts file: two files are CONTENT-merged here, so order matters more than last time. Blob identities per the brief; C-112's condition stated beside the conclusion — one helper file is identical to NEITHER parent by construction, so the composed helper is proven by behaviour, not by the superset. id-superset control with batch #2's adapted copy of the C-57 script, six parents (missing 0 predicted: no branch modifies or deletes a test file; if one misses, C-133 and its rename ADDENDUM verbatim). On the merged tree, one hold: the composition rows, rd447, rd411, rd533, rd315, rd579, rd627a, rd639 and all the C-68 sets by name, the full verify, then one mutant per ticket and M-AB. C-89 on your clone. Count the repo's object files before and after and account for any delta by mtime. Nothing leaves your clone.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET. Predicted 911e706 4033/236, ed01f7e 4040/238, 95c3c9a 3982/236, 057016d 4017/238, 1524fca 3990/237, merged counts(M0) plus 96/5. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-12 (brief section 3a) — the last two gates broke each of these once. H-1: the ONLY SESSION_SECRET printer is the one the brief quotes (it prints SET with a length, or UNSET — never a value); self-test it with a throwaway before the first hold, scan every hold's logs for the throwaway afterwards, and let the scan's own control plant a DIFFERENT marker. H-2: never construct a product storage object on a DATA_DIR you are measuring after its server booted or its erasure ran. H-3: a LANDING CONTROL for every hook, preload, signal handler, race-writer, mutant or live sweeper before the measured run; a failed instrument makes a VOID arm, re-run and reported as a self-correction. H-4: the HEARTBEAT is a separate child process of the hold wrapper, aborted if absent 90 s after the grant, and you report the max gap per hold (at most 120 s). H-5: restore your own perturbations (modes, links, held ports) before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server runs under the network belt with its landing control. H-7: mutants only through a quoted tool with a negative control. H-8: an insertion's landing rule is the exact new text present and the old text absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon is reachable before measuring its absence. H-11: every script under /bin/bash, every sha:path braced. H-12: list every modified or deleted test file before the C-57 control.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch1.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree (C-28). Symlinks, hard links, chmod, held ports and scratch git repos ONLY under your own mktemp dirs. Findings-only: no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see (merges are Tuesday's GO). No Azure (no az at all), no demo, no public host, no Log Analytics. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 11 of the brief exactly. QUEUE, NEVER TAKE OVER: four NexusAI seats (M, N, O, P) share session-tools/nexusai-lock.sh with you. Every jest run, server boot and erasure drive goes through it with a tag starting qa-b1- (C-141 gate-class, and its ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield; C-110), the lock held once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's five negative-control seats classifying foreign in the same run; a hold with no live negative control aborts; your own deliberately failing second servers are ours and must be reaped. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request and erasure drive has a per-step DEADLINE and a client timeout, every server is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether any of the five branches has a PR, and M0's CI Build, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: all five branches and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. The same builder seats are working other tickets now: if a branch moves, your verdict still names the pinned sha and you say so.

QUESTIONS: your routing name is QA/NexusAI-batch1. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch1] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-26-gate-batch1/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-447: <GO|GO WITH FINDINGS|NO GO> @ 911e706 · RD-411: <GO|GO WITH FINDINGS|NO GO> @ ed01f7e · RD-533: <GO|GO WITH FINDINGS|NO GO> @ 95c3c9a · RD-627a: <GO|GO WITH FINDINGS|NO GO> @ 057016d · RD-315: <GO|GO WITH FINDINGS|NO GO> @ 1524fca
Lead the body with one sentence per ticket, then one line naming M0. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a planted GUID, a needle or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, every declared limit L-A1 to L-A3, L-B1 to L-B4, L-C1 to L-C5, L-D1 to L-D4 and L-E1 to L-E3 discharged with a measurement or left standing and named (C-112), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, the Log Analytics path of /api/database, a real browser render of an undated row, text encodings other than UTF-8, UTF-16 and UTF-32, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$BASE_SHA" "$MAIN_M1" "$MAIN_M2" "$MAIN_SHA" "$RD579" "$RD639" "$RD200_BUILD" "$RD200_FWD" "$A_HEAD" "$B_BUILD" "$B_FWD" "$B_HEAD" \
         "$C_HEAD" "$D_BUILD" "$D_HEAD" "$E_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — bases against main-at-drafting: RD-447/RD-533 off 7c47ec4; RD-411/RD-627a contain 11666d3; RD-315 off 0863711.
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main, RD-447) is not 7c47ec4" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$B_HEAD" 2>/dev/null)" = "$MAIN_M2" ]  || { echo "REFUSING: merge-base(main, RD-411) is not 11666d3" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$C_HEAD" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(main, RD-533) is not 7c47ec4" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$D_HEAD" 2>/dev/null)" = "$MAIN_M2" ]  || { echo "REFUSING: merge-base(main, RD-627a) is not 11666d3" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$E_HEAD" 2>/dev/null)" = "$MAIN_M1" ]  || { echo "REFUSING: merge-base(main, RD-315) is not 0863711" >&2; exit 7; }

# 8 — chains exact, parents exact (each ticket over its merge-base with main; main's own line).
[ "$(g log --format='%H %P' "${BASE_SHA}..${A_HEAD}" 2>&1)" = "$A_HEAD $BASE_SHA" ] || { echo "REFUSING: 7c47ec4..RD-447 is not exactly 911e706" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_M2}..${B_HEAD}" 2>&1)" = "$B_HEAD $B_FWD
$B_FWD $B_BUILD $MAIN_M2
$B_BUILD $BASE_SHA" ] || { echo "REFUSING: 11666d3..RD-411 is not exactly 7be79f0, d81cd97 (merge of 11666d3), ed01f7e" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_SHA}..${C_HEAD}" 2>&1)" = "$C_HEAD $BASE_SHA" ] || { echo "REFUSING: 7c47ec4..RD-533 is not exactly 95c3c9a" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_M2}..${D_HEAD}" 2>&1)" = "$D_HEAD $D_BUILD $MAIN_M2
$D_BUILD $BASE_SHA" ] || { echo "REFUSING: 11666d3..RD-627a is not exactly 9fb9431 then 057016d (merge of 11666d3)" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_M1}..${E_HEAD}" 2>&1)" = "$E_HEAD $MAIN_M1" ] || { echo "REFUSING: 0863711..RD-315 is not exactly 1524fca" >&2; exit 8; }
[ "$(g log --format='%H %P' "${BASE_SHA}..${MAIN_SHA}" 2>&1)" = "$MAIN_SHA $RD200_FWD
$RD200_FWD $RD200_BUILD $MAIN_M2
$MAIN_M2 $RD639 $MAIN_M1
$MAIN_M1 $RD579 $BASE_SHA
$RD200_BUILD $BASE_SHA
$RD639 $BASE_SHA
$RD579 0677388ab031ffaf569a52f6c0301af48f44aece" ] || { echo "REFUSING: 7c47ec4..12b5edc is not RD-579, RD-639, their merges and RD-200 — re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the five ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main: EXPECTED to move. It must be 12b5edc or a descendant IN THE OBJECT STORE, and its movement must not touch the five deltas.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 12b5edc — main was rewritten; re-brief" >&2; exit 18; }
ALLD="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES" "$D_EXPECTED_FILES" "$E_EXPECTED_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLD") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 12b5edc..${M_ORIGIN:0:7} and touched a file of the five deltas: $HIT — the merged-tree premise changes; re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 12b5edc, $(printf '%s\n' "$MOVED" | sed '/^$/d' | wc -l | tr -d ' ') paths, none in the five deltas) — the gate re-pins M0 itself" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$BASE_SHA" "$A_HEAD" "$A_EXPECTED_FILES" "RD-447 (7c47ec4..911e706)"
chk_delta "$MAIN_M2"  "$B_HEAD" "$B_EXPECTED_FILES" "RD-411 (11666d3..ed01f7e)"
chk_delta "$BASE_SHA" "$C_HEAD" "$C_EXPECTED_FILES" "RD-533 (7c47ec4..95c3c9a)"
chk_delta "$MAIN_M2"  "$D_HEAD" "$D_EXPECTED_FILES" "RD-627a (11666d3..057016d)"
chk_delta "$MAIN_M1"  "$E_HEAD" "$E_EXPECTED_FILES" "RD-315 (0863711..1524fca)"

# 75 — RD-411's tip is counts-only; both forward merges added nothing beyond the ticket's own files over 11666d3.
[ "$(g diff --name-only "$B_FWD" "$B_HEAD" 2>/dev/null)" = "$COUNTS_FILE" ] || { echo "REFUSING: d81cd97..ed01f7e is not counts-only" >&2; exit 75; }
GOT="$(g diff --name-only "$MAIN_M2" "$B_FWD" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$B_BUILD_FILES")" ] || { echo "REFUSING: the forward merge d81cd97 differs from 11666d3 by more than RD-411's two files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 75; }
[ -z "$(g diff --name-only "$MAIN_M1" "$MAIN_SHA" -- "$SERVER" 2>/dev/null)" ] || { echo "REFUSING: main touched the server entry point after 0863711 — RD-315's base premise changed" >&2; exit 75; }

# 23 — EXPECTED OVERLAPS (not disjointness): A∩B = helper+counts; C∩E = server+counts; C∩M = server+counts; every other pair = counts.
DA="$(g diff --name-only "$BASE_SHA" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_M2" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$BASE_SHA" "$C_HEAD" 2>/dev/null | sort)"
DD="$(g diff --name-only "$MAIN_M2" "$D_HEAD" 2>/dev/null | sort)"
DE="$(g diff --name-only "$MAIN_M1" "$E_HEAD" 2>/dev/null | sort)"
DM="$(g diff --name-only "$BASE_SHA" "$MAIN_SHA" 2>/dev/null | sort)"
for PAIR in A_B A_C A_D A_E A_M B_C B_D B_E C_D C_E C_M D_E; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | tr '\n' ' ' | sed 's/ $//')"
  case "$PAIR" in
    A_B) WANT="$HELPER $COUNTS_FILE" ;;
    C_E|C_M) WANT="$SERVER $COUNTS_FILE" ;;
    *) WANT="$COUNTS_FILE" ;;
  esac
  [ "$COMMON" = "$WANT" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '$WANT'" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$BASE_SHA 3978 235" "$MAIN_M1 3986 236" "$MAIN_M2 4012 237" "$MAIN_SHA 4021 238" "$A_HEAD 4033 236" "$B_BUILD 3978 235" \
            "$B_FWD 4012 237" "$B_HEAD 4040 238" "$C_HEAD 3982 236" "$D_BUILD 3983 236" "$D_HEAD 4017 238" "$E_HEAD 3990 237"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$BASE_SHA" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_B" "$READY_C" "$READY_D" "$READY_D0" "$READY_E" "$CLAR" "$PREV_B2" "$PREV_G" \
         "$EV_O/rd447-hold.log" "$EV_O/rd447-red-7c47ec4.log" "$EV_O/rd447-verify.log" "$EV_O/rd411-hold.log" "$EV_O/rd411-verify.log" \
         "$EV_M/rd533-hold.log" "$EV_M/rd533-probe-7c47ec4.log" "$EV_M/rd533-red-at-7c47ec4.log" "$EV_M/rd315-hold.log" "$EV_M/rd315-red-at-0863711.log" \
         "$EV_N/mf/A-newmain.log" "$EV_N/mf/B-merged.log" "$EV_N/mf/C1-update.log" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$B2_EV/qa-floorcount.py" "$B2_EV/qa-dispatch.sh" "$B2_EV/qa-mutate.py" "$B2_EV/qa-c57-id-superset.sh" "$B2_EV/qa-netbelt.sb" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-411 READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-533 READY does not name ${C_HEAD:0:7}" >&2; exit 31; }
grep -qF "${D_HEAD:0:7}" "$READY_D" || { echo "REFUSING: the RD-627a updated READY does not name ${D_HEAD:0:7}" >&2; exit 31; }
grep -qF "${E_HEAD:0:7}" "$READY_E" || { echo "REFUSING: the RD-315 READY does not name ${E_HEAD:0:7}" >&2; exit 31; }
grep -qF "${A_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-411 READY does not name RD-447's head ${A_HEAD:0:7} (the batch pairing)" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B2" "$PREV_G" "$READY_B" "$READY_C" "$READY_D" "$READY_D0" "$READY_E"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-447 is TIER 1' 'RD-411 is TIER 1' 'RD-533 is TIER 2' 'RD-627a is TIER 1' 'RD-315 is TIER 1' 'One verdict PER ticket'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-447 (TIER 1)' 'RD-411 (TIER 1)' 'RD-533 (TIER 2)' 'RD-627a (TIER 1)' 'RD-315 (TIER 1)' 'FIVE verdicts'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$MAIN_SHA" "$BASE_SHA" "$MAIN_M1" "$MAIN_M2" "$B_BUILD" "$B_FWD" "$D_BUILD"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
for FL in brief prompt; do
  if [ "$FL" = brief ]; then SRC="$(cat "$BRIEF")"; else SRC="$PROMPT"; fi
  case "$SRC" in *"$SUBJECT_STEM"*"@ 911e706 · RD-411: "*"@ ed01f7e · RD-533: "*"@ 95c3c9a · RD-627a: "*"@ 057016d · RD-315: "*"@ 1524fca"*) ;;
    *) echo "REFUSING: $FL must carry the five-verdict subject" >&2; exit 15 ;; esac
done
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-447 RD-411 RD-533 RD-627a RD-315 RD-639 RD-579 RD-429 RD-386 H-1 H-12 M0 MAIN%IS%MOVING COMPOSITION M-AB
POSITIVE%CONTROL%FIRST M-A1 M-A8 M-B1 M-B7 M-C1 M-C6 M-D1 M-D7 M-E1 M-E5 a4 a19 c4 d14 e8 AZURE_TENANT_ID AADTenantId Buffer xxd
EADDRINUSE EACCES SIGTERM once('error') .machine-id erasure-audit.jsonl B-F1 RD-684 hard-linked SimpleDatabase REQUEST%TIME
THE%CENSUS Date.now() 24-character%window 40/9/49 reverse%order CONTENT-merged NEITHER%parent
git%clone%--shared REGENERATION 4117/243 4033/236 4040/238 3982/236 4017/238 3990/237 id-superset C-57 C-68 C-89 C-104 C-112
C-125 C-133 ADDENDUM C-141 C-110 C-28 node%--check VOID EXCLUSIVE qa-b1- QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT
2%minutes 5%minutes finally LANDING%CONTROL SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED
CI%NOT%RUN Prior%work FOREGROUND"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' '^## 8. TARGET E' '^## 9. THE MERGED TREE' \
         '^## 11. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A3 L-B1 L-B4 L-C1 L-C5 L-D1 L-D4 L-E1 L-E3; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
  case "$PROMPT" in *"$L"*) ;; *) echo "REFUSING: prompt lacks declared limit $L (C-112)" >&2; exit 19 ;; esac
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b1-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main is moving'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — rd579-rd639 S-1's lesson: the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — S-4's lesson: the heartbeat is a separate child, aborted if absent at 90 s, max gap reported.
for w in 'separate child' 'within 90 s' 'max gap'; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat rule fragment '$w' (H-4)" >&2; exit 77; }
done

# 78 — batch #2 S-3's lesson: byte-level plants via Buffer, verified with xxd (H-9).
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant rule fragment '$w' (H-9)" >&2; exit 78; }
done

# 79 — batch #2 S-1/S-2's lessons: quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 11 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N O P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 75 23 35 70 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7}, $D_BRANCH == ${D_HEAD:0:7}, $E_BRANCH == ${E_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (12b5edc or a descendant; moved paths touch none of the five deltas) (18b)"
  echo "  bases 7c47ec4/11666d3/7c47ec4/11666d3/0863711 (7); chains exact (8); deltas exact (22); RD-411 tip counts-only (75)"
  echo "  overlaps exactly helper (A∩B) and server entry point (C∩E, C∩M) + counts (23); counts at twelve shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); evidence (31); H-1 printer (76); H-4 (77); H-9 (78); H-7/H-8 (79)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/main = $M_ORIGIN (a descendant of 12b5edc whose movement touches none of the five deltas). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
