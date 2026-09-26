#!/bin/bash
# launch_qa_nexusai_gate_batch4.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #4", lane 3, the image-content
# gate), FIVE targets, FIVE verdicts, ONE report (2026-09-27):
#   A — RD-418 (TIER 1): rd-418-dockerignore-r3-s84o @ 5a782c1 = 8de8e5c (off 7c47ec4) + 42095e8 (forward merge of 5628e75) + counts.
#       .dockerignore round 3 + Dockerfile (root JSON opt-in, docs/test-files out). REAL IMAGE leg. 4131/245.
#   B — RD-425 (TIER 1): rd-425-guard-all-shipped-s84o @ 8823458 = 1fd5d0f (off 12b5edc) + 7c9dcb7 (forward merge of 5628e75) + counts.
#       Five root dev scripts leave the image; the identifier guard covers every shipped file. REAL IMAGE leg. 4126/244.
#   C — RD-698 (TIER 1): rd-698-mixed-encoding-s84o @ 44bc804 = 2dfaf28 (off 5628e75) + 09c07b3 (forward merge of 1904765) + counts.
#       The carrier gates check both readings of a NUL-bearing file (batch-1 A-F1). 4149/248.
#   D — RD-699 (TIER 2): rd-699-decode-branch-cells-s84o @ 02fe76a, ONE commit STACKED on RD-698's head 44bc804. Tests only;
#       RD-703's BE cell parked per C-130. 4159/249.
#   E — RD-443 (TIER 2): rd-443-guard-residue-s84o @ 8e27dc2 = 20bf99c (off 11666d3) + 1eae175 (forward merge of 12b5edc) + counts.
#       Tests only (rd327 + rd385). 4025/238.
#   Main at drafting 1904765 (batch 1 complete). NOT file-disjoint: A∩B = .dockerignore, A∩C = the image-manifest helper, B∩E = the rd385
#   cell file; all auto-merge, counts the only conflict (drafter's merge-tree in a scratch object dir, four orders agree). The gate RE-PINS
#   main (M0), merges M0 + 698, 699, 418, 425, 443 in its OWN scratch clone, regenerates counts once (predicted counts(M0) + 47/+3;
#   4180/250 at 1904765), and builds REAL images: base M0, M0+418, M0+425, COMBINED M0+418+425, and the full merged head.
#   A batch-3 gate (lane 2, erasure) may run concurrently and share the jest lock: plain FIFO, never touched.
#
# AUTHORITY: Tuesday's batch #4 commission (2026-09-27); READY mails from NexusAI-O, copies in briefs/. Merges: Tuesday's GO
# (Kam 2026-09-25 ~22:0x "merge once tested").
#
# PATTERN: launch_qa_nexusai_gate_batch1.sh (guard families 9 6 7 8 18 22 75 23 35 70 31 39 10 17 11 12-15 20 19 24 53 71 76 77 78 79 38 32
# 40), prompt EMBEDDED. CHANGES, each deliberate:
#   - 7/8: per-ticket bases (5628e75 x2, 1904765, 44bc804, 12b5edc) and main's seven-commit line 5628e75..1904765 exact.
#   - 75: every tip is counts-only; each forward merge adds nothing beyond the ticket's own files over its base.
#   - 23: EXPECTED OVERLAPS: A∩B = {.dockerignore, counts}, A∩C = {helper, counts}, B∩E = {rd385, counts}; every other pair = counts.
#   - 81 (NEW): THE RD-698 HOLD — rd447's cell file is byte-identical to main's at every head that carries it (refuse if amended).
#   - 80 (NEW): the brief carries the image-leg rules (docker lock, COMBINED, git archive only, container reap, label) — H-16.
#   - 82 (NEW): the brief and prompt carry the second-gate (batch-3) rule.
#   - 40: the routing line QA/NexusAI-batch4 must exist (Tuesday adds it; the drafter could not — outside fleet/qa-agent/).
#   - 32: SELF-CHECK stamp, placeholder 2026-09-27 09:00 (comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch4' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), grep, ps, tmux, command -v.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch4.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..82 a guard refused
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
BRIEF="$BRIEFS/2026-09-27_nexusai-gate-batch4-rd418-rd425-rd698-rd699-rd443.md"
READY_A="$BRIEFS/2026-09-27_nexusai-rd418-READY-mail.txt"
READY_B="$BRIEFS/2026-09-27_nexusai-rd425-READY-mail.txt"
READY_C="$BRIEFS/2026-09-27_nexusai-rd698-READY-mail.txt"
READY_D="$BRIEFS/2026-09-27_nexusai-rd699-READY-mail.txt"
READY_E="$BRIEFS/2026-09-26_nexusai-rd443-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_O="$NX/session-tools/s84o"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
LANE_PLAN="$NX/5_Project_History/2026-09-25_S84M_lane-plan.md"
PREV_B1="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/report.md"
B1_EV="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/evidence"
PREV_FLOORLIB="$B1_EV/qa-floorlib.sh"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-27-gate-batch4/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch4'

BASE_7C='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'       # RD-418's fix base
BASE_116='11666d3c4f615190646914270016419fffa642e2'      # RD-443's fix base
MAIN_12B='12b5edc31ee4ef52415d1cbffbbb0504d7f4715c'      # RD-425's fix base; RD-443's forward-merge base
MAIN_5628='5628e750ebb967b8c6a8e2ca6eb12d9fa5d9b1a4'     # RD-418/RD-425's forward-merge base; RD-698's fix base
MAIN_SHA='1904765007e9447ac6c980f9840c0689a02abe6c'      # origin main at drafting (batch 1 complete)
ML_5220='52203351ee2c72bd1826807d1505a2d5aa8aac3e'       # main line 5628e75..1904765
ML_748C='748cecec2a883a117560824ac5615c268dfe0800'
ML_1524='1524fca7ec72b23a4f000b77872a4158f8e14f86'
ML_0570='057016de2b2929c23f643b7346413199f370d3ce'
ML_95C3='95c3c9a9d39429f9093270e283e531f3cda4e88d'
ML_9FB9='9fb94311b010c3d4355418eface0e1dc3ecd3795'
ML_0863='0863711261afc5f3323b8c4fc480d65109b17ba7'
A_BRANCH='rd-418-dockerignore-r3-s84o'
A_BUILD='8de8e5c446023847362cd470375db4fb6ceaf645'
A_FWD='42095e8eb6979b6a85e044a45d658508f77e28a9'
A_HEAD="${QA_A_HEAD_OVERRIDE:-5a782c10698a6e678ca89957ec661f48daf9c8f8}"
B_BRANCH='rd-425-guard-all-shipped-s84o'
B_BUILD='1fd5d0f8407586f71f7ca9c4f6b5566a4093d37b'
B_FWD='7c9dcb7c9cf2f3396d57b03ea4298269e9736de3'
B_HEAD="${QA_B_HEAD_OVERRIDE:-8823458b963360ffd212f9b19a0efddea5ba9e66}"
C_BRANCH='rd-698-mixed-encoding-s84o'
C_BUILD='2dfaf2823abf07dd89000c1c51a7d73107f91c46'
C_FWD='09c07b36bda2e6c99b006a1b1f1107d9ae830677'
C_HEAD="${QA_C_HEAD_OVERRIDE:-44bc804abd0a12cc6a7f913cda59e9a2634ec7d8}"
D_BRANCH='rd-699-decode-branch-cells-s84o'
D_HEAD="${QA_D_HEAD_OVERRIDE:-02fe76ad74ab7297a2ec807603fd8b67f547336c}"
E_BRANCH='rd-443-guard-residue-s84o'
E_BUILD='20bf99c71ad43ea48db8c97c8101a1bc3217087e'
E_FWD='1eae175e541c9151899951aafee01db31a67e009'
E_HEAD="${QA_E_HEAD_OVERRIDE:-8e27dc22c168f87a2a11946f7606ec36a67c6895}"

COUNTS_FILE='scripts/verify-expected-counts.json'
HELPER='__tests__/helpers/image-manifest.js'
DOCKERIGNORE='.dockerignore'
RD385='__tests__/rd385-shipped-root-markdown-identifiers.test.js'
RD447='__tests__/rd447-utf16-text-is-decoded.test.js'
A_EXPECTED_FILES="$DOCKERIGNORE
Dockerfile
$HELPER
__tests__/image-content-exposure.test.js
__tests__/rd418-dockerignore-round3.test.js
$COUNTS_FILE"
B_EXPECTED_FILES="$DOCKERIGNORE
$RD385
$COUNTS_FILE"
C_EXPECTED_FILES="$HELPER
__tests__/rd698-mixed-encoding-file.test.js
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js
__tests__/rd699-decode-branches-behaviour.test.js
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/rd327-build-digest-on-public-health.test.js
$RD385
$COUNTS_FILE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
NEG_SEATS='62649 9959 20317 47349'   # NexusAI-M %19, -N %21, -P %22, Tuesday %0 — read 2026-09-27 08:57:09 AEST (O had no pane)

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-418 · RD-425 · RD-698 · RD-699 · RD-443'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch4] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, the release pipeline's own image build and any registry, a build context other than a git archive of a committed sha plus the gate's own plants, text encodings other than UTF-8, UTF-16 and UTF-32, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI — batch #4, lane 3, the image-content gate — with FIVE targets, FIVE verdicts and ONE report: RD-418 (TIER 1), RD-425 (TIER 1), RD-698 (TIER 1), RD-699 (TIER 2) and RD-443 (TIER 2). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree (and, for RD-418 and RD-425, the COMBINED image). A finding on one ticket never becomes another's verdict; a finding that exists only in a COMPOSITION is graded on the merged tree or the combined image and named against both tickets it joins.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch4-rd418-rd425-rd698-rd699-rd443.md
Then the charter it names, then the five READY mails it names (read each WHOLE), then the batch-1 gate report it names (2026-09-26-gate-batch1) — its findings A-F1 and A-F2 became RD-698 and RD-699, its method and its self-corrections are your inheritance, and the brief's section 3a turns them into rules H-1 to H-17 that bind you. Every builder statement is a CLAIM, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a: I, G, R, T) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-418: branch rd-418-dockerignore-r3-s84o at 5a782c10698a6e678ca89957ec661f48daf9c8f8 = 8de8e5c446023847362cd470375db4fb6ceaf645 (off 7c47ec467f585e9db5daf3a82cdb96deae0b1e7a) forward-merged onto 5628e750ebb967b8c6a8e2ca6eb12d9fa5d9b1a4 at 42095e8eb6979b6a85e044a45d658508f77e28a9, plus counts; the .dockerignore, the Dockerfile, the image-manifest helper's case-pair hunk, image-content-exposure's re-anchored cells and a new cell file. RD-425: branch rd-425-guard-all-shipped-s84o at 8823458b963360ffd212f9b19a0efddea5ba9e66 = 1fd5d0f8407586f71f7ca9c4f6b5566a4093d37b (off 12b5edc31ee4ef52415d1cbffbbb0504d7f4715c) forward-merged onto 5628e75 at 7c9dcb7c9cf2f3396d57b03ea4298269e9736de3, plus counts; an appended .dockerignore block and an appended describe in the rd385 cell file. RD-698: branch rd-698-mixed-encoding-s84o at 44bc804abd0a12cc6a7f913cda59e9a2634ec7d8 = 2dfaf2823abf07dd89000c1c51a7d73107f91c46 (off 5628e75) forward-merged onto main 1904765007e9447ac6c980f9840c0689a02abe6c at 09c07b36bda2e6c99b006a1b1f1107d9ae830677, plus counts; the helper's scanReadings and a new cell file. RD-699: branch rd-699-decode-branch-cells-s84o at 02fe76ad74ab7297a2ec807603fd8b67f547336c, ONE commit STACKED on RD-698's head 44bc804; a new cell file and a PARKED file under the helpers directory (RD-703, C-130). RD-443: branch rd-443-guard-residue-s84o at 8e27dc22c168f87a2a11946f7606ec36a67c6895 = 20bf99c71ad43ea48db8c97c8101a1bc3217087e (off 11666d3c4f615190646914270016419fffa642e2) forward-merged onto 12b5edc at 1eae175e541c9151899951aafee01db31a67e009, plus counts; rd327 and rd385 cells. These deltas are NOT file-disjoint: RD-418 and RD-425 both edit .dockerignore; RD-418 and RD-698 both edit the helper; RD-425 and RD-443 both edit the rd385 cell file. The drafter's merge-tree says all three auto-merge to blobs identical to NEITHER parent, and only the counts file conflicts — prove it yourself; the semantic overlaps U1 to U8 in the brief are UNMEASURED and are yours to measure.

MAIN IS MOVING. Main at drafting was 1904765007e9447ac6c980f9840c0689a02abe6c (batch 1 complete). RE-PIN main at your start and call it M0: it must be 1904765 or a descendant, and 1904765..M0 must share no path with the five deltas except the counts file (else STOP and ask). Moved backend or static files still change what the guards scan: re-run the brief's rows g1 and g6 on M0. Your merged tree is M0 plus all five. If main moves again during your gate, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

RD-418 (TIER 1) — WHAT SHIPS. POSITIVE CONTROL FIRST: image-content-exposure and rd418 against 5628e75's files (RELAYED 9 red — say what "red at base" proves for the three re-anchored ARM cells, C-131, C-40), 68/68 at the head. Mutants M-A1 to M-A10, including the helper accepting a non-pair bracket and the base stage's surviving package*.json glob. Rows i1 to i21 of table I for the base and RD-418 alone, the helper's model against the real image, the RD-477 floor, prior work (C-163's root-commit claims, S59's WIP c026e94).

RD-425 (TIER 1) — THE GUARD OVER EVERY SHIPPED FILE. POSITIVE CONTROL FIRST: 4 red at 5628e75's .dockerignore, 105/105 at the head. Mutants M-B1 to M-B8. Rows g1 to g8: the guard over the MERGED shipped set (RD-418 changes that population twice), the population named, the string reader against wide and mixed files beside RD-698's gates, the REVIEWED hashes against main's newer server entry point, erasure and customer-data files. Conditions 1 and 2 (C-167) re-measured with positive controls. Disclosures: the C-28 fetch in the READY, and a second earlier fetch in the builder's session log that no READY carries.

RD-698 (TIER 1) — BOTH READINGS. THE HOLD FIRST, measured: rd447's cell file byte-identical to main's at every head and on the merged tree, its bytes-vs-string tripwire cell present verbatim, and still RED for a NUL-bearing shipped plant. Nobody amends that cell; you never propose amending it. POSITIVE CONTROL FIRST: exactly 7 red at 5628e75's and 1904765's helper, 187/187 at the head. Mutants M-C1 to M-C7. Rows r1 to r14 (a20, a20odd, a21, a22, the controls, the reverse mix, the BE tail on the bytes path, a non-ASCII label, the two-reading fingerprint against a real review entry). Say whether RD-698's cells are the regression test the batch-1 gate specified — through the DEFAULT reader — or less. Its C-68 set is all ten helper consumers; the builder ran five.

RD-699 (TIER 2) — THE DECODER'S BRANCHES. Re-derive the builder's five arms and re-run the batch-1 gate's own arms M-A2, M-A5, M-A6, M-A7 and M-AB (the RD-447 x RD-411 composition's own mutant) at 02fe76a and on the merged tree. THE PARK, INSIDE THE LOCK: jest --listTests lists rd699 and omits the parked file, with a positive control that a copy placed in the collected tree is listed, runs and is red. RD-703 (the big-endian string rule) is filed, parked per C-130 and NOT in scope: never grade it, never fix it. L-D1 and L-D2; the on-disk probe absent after a full verify.

RD-443 (TIER 2) — THREE WIDER DETECTORS. POSITIVE CONTROL FIRST, including the base run the builder did not do (L-E4). Mutants M-E4 to M-E7. Rows t1 to t6, including the wider TICKET rule over the real shipped root markdown on the merged tree.

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 44bc804 (RD-698), 02fe76a (RD-699), 5a782c1 (RD-418), 8823458 (RD-425), 8e27dc2 (RD-443) — RD-698 before RD-699 is FIXED; the rest is the drafter's proposal and your second clone proves order independence (O3: 8e27dc2, 8823458, 5a782c1, 44bc804, 02fe76a). Predict before each merge whether the counts file conflicts, and explain any clean merge with a side control; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run — every helper consumer enumerates with git ls-files. Resolve the counts by REGENERATION, never by hand: npm run verify -- --maxWorkers=2 --update-counts ONCE on the tree after ALL FIVE merges. Predicted counts(M0) plus 47 tests and 3 suites — 4180/250 if M0 is 1904765 — a prediction; the measurement decides; also the per-step counts. C-112's condition stated beside the conclusion: TWO files are CONTENT-merged to NEITHER parent, the helper and the rd385 cell file, and rd385 carries test ids, so the byte-identity shortcut does NOT apply. id-superset control with the batch-1 gate's copy of the C-57 script, six parents: the drafter predicts the exact pass MISSES 2 ids — two image-content-exposure cells RD-418 retitled as re-anchors — apply C-133 and its rename ADDENDUM verbatim, and if the rulings are not a grant in its sense, STOP, name it and ask. On the merged tree, one hold: U1 to U8, the helper consumers, the .dockerignore and Dockerfile readers, rd385 both describes, the merged columns of tables G, R and T, the full verify, one mutant per ticket. C-89 on your clone. Record the repo's git count-objects before and after and account for any delta. Nothing leaves your clone.

THE IMAGE LEGS — RD-418 AND RD-425 TOGETHER, brief section 9a. A change to what ships is a sensitive surface: build REAL images of base M0, M0 plus RD-418, M0 plus RD-425, the COMBINED M0 plus both, and the full merged head, each from a git archive of a COMMITTED sha plus the same plants (H-16: never from a tree that ran jest — RD-699's probe lives in the static directory), every build and container run through session-tools/nexusai-lock.sh docker with a qa-b4- tag. Diff each file set (files and directories) against the base: the COMBINED LEAVES must be exactly the union of the two, nothing ENTERS, and the full merged image must equal the combined one byte for byte. Start every image with a throwaway SESSION_SECRET passed by name, never in argv, never printed, and check /api/health from inside the container; start it again WITHOUT one as the control that must refuse (C-15); scan the startup log for missing files. Compare the helper's model of what ships with the real image. Remove every container of yours in a finally; never touch, remove or prune any image or container not created by this gate; never push; never log in to a registry.

FULL VERIFY of each head and of the merged tree through the lock, SESSION_SECRET UNSET. Predicted 5a782c1 4131/245, 8823458 4126/244, 44bc804 4149/248, 02fe76a 4159/249, 8e27dc2 4025/238, merged counts(M0) plus 47/3. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, the helper reads every mutated .dockerignore or Dockerfile without a throw, each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-17 (brief section 3a) — earlier gates broke each of these once. H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway before the first hold, scan every hold's and every image leg's logs for the throwaway afterwards, and let the scan's own control plant a DIFFERENT marker. H-3: a LANDING CONTROL for every hook, plant, probe cleanup and container. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant; report the max gap per hold (at most 120 s). H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang). H-7 and H-8: mutants only through a quoted tool with a negative control; the exact new text present and the old text absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon is reachable before measuring its absence. H-11: every script under /bin/bash, every sha:path braced. H-12: list every modified test file before the C-57 control. H-13: NUL-safe path censuses. H-14: a GUID redactor that matches hyphen or space separators. H-15: no inline loops under zsh. H-16: image contexts only from git archive of a committed sha, listed before every build. H-17: a plant that lands in the wrong class is VOID for its row.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch4.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory, and never work in its 2_Project_Files checkout or any builder worktree (C-28). A sha missing from the local object store is UNMEASURED — never fetch it. Plants and scratch git repos ONLY under your own mktemp dirs. Findings-only: no fixes, no pushes, no deploys, no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see (merges are Tuesday's GO). Nothing to Partner Center, the demo or production. No Azure (no az at all), no public host, no registry. No mail to any human. Never rm: quarantine; leave your own docker images tagged and list them.

FLOOR DISCIPLINE — section 11 of the brief exactly. QUEUE, NEVER TAKE OVER: NexusAI builder seats share session-tools/nexusai-lock.sh with you. Every jest run — including jest --listTests — every docker build and every container run goes through it with a tag starting qa-b4- (C-110; C-141 gate-class, and its ADDENDUM 2, 3 and 4: each new qa ticket earns a fresh, self-applied yield; use --after only to sit directly behind a queued merge ticket or your own previous ticket, never to jump anyone), the lock held once per multi-run measurement as a tracked child of your seat, never the jest and docker locks at once. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every build, container step, jest run and verify has a per-step DEADLINE, every container is removed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

THE SECOND GATE. A batch-3 gate (lane 2, the erasure files) may be running concurrently and sharing the jest lock. You never touch its worktrees, trees, clones, processes, lock tickets or report. Between the two gates the queue is plain FIFO: never jump, interrupt, move or signal one of its tickets; wait while it holds (C-141 does not cover gate tickets among themselves). Its erasure servers count as FOREIGN in your counter — record them. If its merges move main, apply the main-is-moving rule.

CI: whether any of the five branches has a PR, and M0's CI Build, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: all five branches and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. The same builder seats are working other tickets now: if a branch moves, your verdict still names the pinned sha and you say so.

QUESTIONS: your routing name is QA/NexusAI-batch4. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch4] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch4/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-418 · RD-425 · RD-698 · RD-699 · RD-443
Lead the body with ONE line per ticket in the form "RD-<n>: <GO|GO WITH FINDINGS|NO GO> @ <short sha> — <one sentence>", then one line naming M0 and the combined-image result. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a planted GUID, the throwaway secret, a canary or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, every declared limit L-A1 to L-A5, L-B1 to L-B5, L-C1 to L-C4, L-D1 to L-D2 and L-E1 to L-E4 discharged with a measurement or left standing and named (C-112), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. Prior work: every C-49 question in the brief answered. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, the release pipeline's own image build and any registry, a build context other than a git archive of a committed sha plus the gate's own plants, text encodings other than UTF-8, UTF-16 and UTF-32, and Windows.
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
for S in "$BASE_7C" "$BASE_116" "$MAIN_12B" "$MAIN_5628" "$MAIN_SHA" "$ML_5220" "$ML_748C" "$ML_1524" "$ML_0570" "$ML_95C3" "$ML_9FB9" "$ML_0863" \
         "$A_BUILD" "$A_FWD" "$A_HEAD" "$B_BUILD" "$B_FWD" "$B_HEAD" "$C_BUILD" "$C_FWD" "$C_HEAD" "$D_HEAD" "$E_BUILD" "$E_FWD" "$E_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases with main-at-drafting.
[ "$(g merge-base "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$MAIN_5628" ] || { echo "REFUSING: merge-base(main, RD-418) is not 5628e75" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$B_HEAD" 2>/dev/null)" = "$MAIN_5628" ] || { echo "REFUSING: merge-base(main, RD-425) is not 5628e75" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$C_HEAD" 2>/dev/null)" = "$MAIN_SHA" ]  || { echo "REFUSING: RD-698 does not contain main 1904765" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$D_HEAD" 2>/dev/null)" = "$MAIN_SHA" ]  || { echo "REFUSING: RD-699 does not contain main 1904765" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$E_HEAD" 2>/dev/null)" = "$MAIN_12B" ]  || { echo "REFUSING: merge-base(main, RD-443) is not 12b5edc" >&2; exit 7; }

# 8 — chains exact, parents exact (each ticket over its merge-base with main; main's own line since 5628e75).
[ "$(g log --format='%H %P' "${MAIN_5628}..${A_HEAD}" 2>&1)" = "$A_HEAD $A_FWD
$A_FWD $A_BUILD $MAIN_5628
$A_BUILD $BASE_7C" ] || { echo "REFUSING: 5628e75..RD-418 is not exactly 8de8e5c, 42095e8 (merge of 5628e75), 5a782c1" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_5628}..${B_HEAD}" 2>&1)" = "$B_HEAD $B_FWD
$B_FWD $B_BUILD $MAIN_5628
$B_BUILD $MAIN_12B" ] || { echo "REFUSING: 5628e75..RD-425 is not exactly 1fd5d0f, 7c9dcb7 (merge of 5628e75), 8823458" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${C_HEAD}" 2>&1)" = "$C_HEAD $C_FWD
$C_FWD $C_BUILD $MAIN_SHA
$C_BUILD $MAIN_5628" ] || { echo "REFUSING: 1904765..RD-698 is not exactly 2dfaf28, 09c07b3 (merge of 1904765), 44bc804" >&2; exit 8; }
[ "$(g log --format='%H %P' "${C_HEAD}..${D_HEAD}" 2>&1)" = "$D_HEAD $C_HEAD" ] || { echo "REFUSING: RD-699 is not exactly one commit on RD-698's head 44bc804" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_12B}..${E_HEAD}" 2>&1)" = "$E_HEAD $E_FWD
$E_FWD $E_BUILD $MAIN_12B
$E_BUILD $BASE_116" ] || { echo "REFUSING: 12b5edc..RD-443 is not exactly 20bf99c, 1eae175 (merge of 12b5edc), 8e27dc2" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_5628}..${MAIN_SHA}" 2>&1)" = "$MAIN_SHA $ML_0570 $ML_748C
$ML_748C $ML_95C3 $ML_5220
$ML_5220 $ML_1524 $MAIN_5628
$ML_1524 $ML_0863
$ML_0570 $ML_9FB9 $BASE_116
$ML_95C3 $BASE_7C
$ML_9FB9 $BASE_7C" ] || { echo "REFUSING: 5628e75..1904765 is not the three batch-1 merges (RD-315, RD-533, RD-627a) — re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the five ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main: may move (batch-3's lane-2 merges). It must be 1904765 or a descendant IN THE OBJECT STORE, and must not touch the five deltas.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 1904765 — main was rewritten; re-brief" >&2; exit 18; }
ALLD="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES" "$D_EXPECTED_FILES" "$E_EXPECTED_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLD") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 1904765..${M_ORIGIN:0:7} and touched a file of the five deltas: $HIT — the merged-tree premise changes; re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 1904765, $(printf '%s\n' "$MOVED" | sed '/^$/d' | wc -l | tr -d ' ') paths, none in the five deltas) — the gate re-pins M0 itself and re-runs g1/g6" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MAIN_5628" "$A_HEAD" "$A_EXPECTED_FILES" "RD-418 (5628e75..5a782c1)"
chk_delta "$MAIN_5628" "$B_HEAD" "$B_EXPECTED_FILES" "RD-425 (5628e75..8823458)"
chk_delta "$MAIN_SHA"  "$C_HEAD" "$C_EXPECTED_FILES" "RD-698 (1904765..44bc804)"
chk_delta "$C_HEAD"    "$D_HEAD" "$D_EXPECTED_FILES" "RD-699 (44bc804..02fe76a)"
chk_delta "$MAIN_12B"  "$E_HEAD" "$E_EXPECTED_FILES" "RD-443 (12b5edc..8e27dc2)"

# 75 — every tip is counts-only; each forward merge adds nothing beyond the ticket's own files over its base.
for PAIR in "$A_FWD $A_HEAD RD-418" "$B_FWD $B_HEAD RD-425" "$C_FWD $C_HEAD RD-698" "$E_FWD $E_HEAD RD-443"; do
  set -- $PAIR
  [ "$(g diff --name-only "$1" "$2" 2>/dev/null)" = "$COUNTS_FILE" ] || { echo "REFUSING: $3's tip ${2:0:7} over ${1:0:7} is not counts-only" >&2; exit 75; }
done
chk_fwd() { local base="$1" fwd="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$base" "$fwd" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$(printf '%s\n' "$want" | grep -vxF "$COUNTS_FILE")")" ] || { echo "REFUSING: $label's forward merge differs from its base by more than the ticket's own files. Got:" >&2; printf '%s\n' "$got" >&2; exit 75; }; }
chk_fwd "$MAIN_5628" "$A_FWD" "$A_EXPECTED_FILES" "RD-418"
chk_fwd "$MAIN_5628" "$B_FWD" "$B_EXPECTED_FILES" "RD-425"
chk_fwd "$MAIN_SHA"  "$C_FWD" "$C_EXPECTED_FILES" "RD-698"
chk_fwd "$MAIN_12B"  "$E_FWD" "$E_EXPECTED_FILES" "RD-443"

# 23 — EXPECTED OVERLAPS: A∩B = .dockerignore+counts; A∩C = helper+counts; B∩E = rd385+counts; every other pair (and vs main-since-base) = counts.
DA="$(g diff --name-only "$MAIN_5628" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_5628" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
DD="$(g diff --name-only "$C_HEAD" "$D_HEAD" 2>/dev/null | sort)"
DE="$(g diff --name-only "$MAIN_12B" "$E_HEAD" 2>/dev/null | sort)"
DM="$(g diff --name-only "$MAIN_5628" "$MAIN_SHA" 2>/dev/null | sort)"
DN="$(g diff --name-only "$MAIN_12B" "$MAIN_SHA" 2>/dev/null | sort)"
for PAIR in A_B A_C A_D A_E B_C B_D B_E C_D C_E D_E A_M B_M E_N; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | tr '\n' ' ' | sed 's/ $//')"
  case "$PAIR" in
    A_B) WANT="$DOCKERIGNORE $COUNTS_FILE" ;;
    A_C) WANT="$HELPER $COUNTS_FILE" ;;
    B_E) WANT="$RD385 $COUNTS_FILE" ;;
    *) WANT="$COUNTS_FILE" ;;
  esac
  [ "$COMMON" = "$WANT" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '$WANT'" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$BASE_7C 3978 235" "$BASE_116 4012 237" "$MAIN_12B 4021 238" "$MAIN_5628 4120 244" "$MAIN_SHA 4133 247" \
            "$A_BUILD 3978 235" "$A_FWD 4120 244" "$A_HEAD 4131 245" "$B_BUILD 4021 238" "$B_FWD 4120 244" "$B_HEAD 4126 244" \
            "$C_BUILD 4120 244" "$C_FWD 4133 247" "$C_HEAD 4149 248" "$D_HEAD 4159 249" "$E_BUILD 4012 237" "$E_FWD 4021 238" "$E_HEAD 4025 238"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 81 — THE RD-698 HOLD: rd447's cell file (with its bytes-vs-string tripwire) byte-identical to main's at every head that carries it.
R447_MAIN="$(blob "$MAIN_SHA" "$RD447")"
[ -n "$R447_MAIN" ] || { echo "REFUSING: $RD447 is absent at main 1904765" >&2; exit 81; }
for S in "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do
  [ "$(blob "$S" "$RD447")" = "$R447_MAIN" ] || { echo "REFUSING: $RD447 at ${S:0:7} differs from main's — the HOLD on rd447's tripwire cell is broken; re-brief" >&2; exit 81; }
done
g show "${MAIN_SHA}:${RD447}" 2>/dev/null | grep -qF "every shipped tracked file scans to the same text from bytes as from a UTF-8 read" || {
  echo "REFUSING: rd447's tripwire cell title not found at main 1904765" >&2; exit 81; }

# 31 — builder evidence, prior report, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$CLAR" "$LANE_PLAN" "$PREV_B1" \
         "$EV_O/rd418-arms.log" "$EV_O/rd418-final.log" "$EV_O/rd418-pair.log" "$EV_O/rd418-health.log" "$EV_O/rd418-build.sh" \
         "$EV_O/rd425-hold.log" "$EV_O/rd425-verify.log" "$EV_O/rd425-pair.log" "$EV_O/rd425-health.log" \
         "$EV_O/rd698-hold.log" "$EV_O/rd698-verify.log" "$EV_O/rd699-final.log" "$EV_O/rd443-hold.log" "$EV_O/rd443-verify.log" \
         "$EV_O/session-log.txt" "$EV_O/yield-log.txt" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$B1_EV/qa-floorcount.py" "$B1_EV/qa-dispatch.sh" "$B1_EV/qa-holdlib.sh" "$B1_EV/qa-mutate.py" \
         "$B1_EV/qa-c57-id-superset.sh" "$B1_EV/qa-netbelt.sb" "$B1_EV/qa-ssprint.sh" "$B1_EV/qa-h1-scan.py" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-418 READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-425 READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-698 READY does not name ${C_HEAD:0:7}" >&2; exit 31; }
grep -qF "${D_HEAD:0:7}" "$READY_D" || { echo "REFUSING: the RD-699 READY does not name ${D_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_D" || { echo "REFUSING: the RD-699 READY does not name RD-698's head ${C_HEAD:0:7} (the stack)" >&2; exit 31; }
grep -qF "${E_HEAD:0:7}" "$READY_E" || { echo "REFUSING: the RD-443 READY does not name ${E_HEAD:0:7}" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B1" "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-418 is TIER 1' 'RD-425 is TIER 1' 'RD-698 is TIER 1' 'RD-699 is TIER 2' 'RD-443 is TIER 2' 'One verdict PER ticket'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-418 (TIER 1)' 'RD-425 (TIER 1)' 'RD-698 (TIER 1)' 'RD-699 (TIER 2)' 'RD-443 (TIER 2)' 'FIVE verdicts'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$MAIN_SHA" "$MAIN_5628" "$MAIN_12B" "$BASE_7C" "$BASE_116" \
         "$A_BUILD" "$A_FWD" "$B_BUILD" "$B_FWD" "$C_BUILD" "$C_FWD" "$E_BUILD" "$E_FWD"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject exactly" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the verdict subject exactly" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="RD-418 RD-425 RD-698 RD-699 RD-443 RD-703 RD-447 RD-411 A-F1 A-F2 H-1 H-17 M0 MAIN%IS%MOVING COMPOSITION COMBINED HOLD
POSITIVE%CONTROL%FIRST M-A1 M-A10 M-B1 M-B8 M-C1 M-C7 M-E4 M-E7 M-AB i1 i21 g1 g8 r1 r14 t1 t6 U1 U8 Buffer xxd
.dockerignore Dockerfile package*.json scanReadings tripwire C-130 --listTests SESSION_SECRET%passed%by%name refuse union
git%archive nexusai-lock.sh%docker qa-b4- /api/health finally batch-3 FIFO
git%clone%--shared REGENERATION 4180/250 4131/245 4126/244 4149/248 4159/249 4025/238 id-superset C-57 C-68 C-89 C-104 C-112
C-125 C-133 ADDENDUM C-141 C-110 C-28 C-15 C-163 C-167 node%--check VOID EXCLUSIVE QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT
2%minutes 5%minutes LANDING%CONTROL SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED
CI%NOT%RUN Prior%work FOREGROUND"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^### THE UNMEASURED INTERACTIONS' '^### The proposed MERGE ORDER' \
         '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' \
         '^## 8. TARGET E' '^## 9. THE MERGED TREE' '^## 9a. THE IMAGE LEGS' '^## 11. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A5 L-B1 L-B5 L-C1 L-C4 L-D1 L-D2 L-E1 L-E4; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
  case "$PROMPT" in *"$L"*) ;; *) echo "REFUSING: prompt lacks declared limit $L (C-112)" >&2; exit 19 ;; esac
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b4-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main is moving'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 — the brief carries the ONE safe SESSION_SECRET printer verbatim and names the forbidden idioms.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done

# 77 — the heartbeat is a separate child, aborted if absent at 90 s, max gap reported.
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

# 80 — the image-leg rules (H-16, section 9a).
for w in 'H-16' 'nexusai-lock.sh docker' 'COMBINED' 'git archive' 'docker rm -f' 'label=qa-gate=batch4' 'Never `docker' 'WITHOUT `SESSION_SECRET`'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the image-leg rule fragment '$w' (section 9a / H-16)" >&2; exit 80; }
done
command -v docker >/dev/null 2>&1 || echo "NOTE: no docker CLI on PATH for this shell — the image legs (section 9a) will be NOT RUN unless the gate's shell has one" >&2

# 82 — the second-gate rule (batch-3) in brief and prompt.
for w in 'batch-3' 'plain FIFO' 'never touch' 'gate tickets among themselves'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the second-gate rule fragment '$w'" >&2; exit 82; }
done
case "$PROMPT" in *"THE SECOND GATE"*"batch-3"*"FIFO"*) ;; *) echo "REFUSING: prompt lacks the second-gate rule" >&2; exit 82 ;; esac

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 11 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 75 23 35 70 81 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 80 82 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7}, $D_BRANCH == ${D_HEAD:0:7}, $E_BRANCH == ${E_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (1904765 or a descendant; moved paths touch none of the five deltas) (18b)"
  echo "  bases 5628e75/5628e75/1904765/44bc804/12b5edc (7); chains exact (8); deltas exact (22); tips counts-only (75)"
  echo "  overlaps exactly .dockerignore (A∩B), helper (A∩C), rd385 (B∩E) + counts (23); counts at eighteen shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); RD-698 HOLD rd447 ${R447_MAIN:0:7} (81); evidence (31); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); images (80); second gate (82)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/main = $M_ORIGIN (a descendant of 1904765 whose movement touches none of the five deltas). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
