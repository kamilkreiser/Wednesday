#!/bin/bash
# launch_qa_nexusai_gate_batch3.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch #3"), FIVE targets,
# FIVE verdicts, ONE report (2026-09-27). All five are NexusAI lane 2, author seat NexusAI-N, all TIER 1:
#   A — RD-324: rd-324-ledger-union-s84n @ 168d850 = e10e7d9 (off 7c47ec4) + merge 11666d3 (3beea5c) + merge 1904765. Ledger door union. 4137/248.
#   B — RD-684: rd-684-redrive-carries-surviving-target-s84n @ 7085ee7 = b5d6525 (off 11666d3) + merge 1904765 (b474c85) + D-F1 cells. 4140/248.
#   C — RD-685: rd-685-hardlinked-store-s84n @ 9d7076b = 724326f (off 5628e75) + merge 1904765 (5adaedb) + sibling-site follow-up. C-169. 4141/248.
#   D — RD-424: rd-424-backup-after-write-s84n @ 2ce26eb = fa7ffe6 (off 7c47ec4) + merge 5f2683c. NOT merged forward onto 1904765. C-164. 4044/243.
#   E — RD-314: rd-314-law-window-after-source-s84n @ ce148d5 = 8dd5de7 (off 7c47ec4) + merge 11666d3. NOT merged forward. 4022/238.
#   Main at drafting 1904765 (batch #1 fully merged; 4133/247). A, B, C all edit the erasure module; B x C conflict in ONE content hunk
#   (drafter's merge-tree in a scratch object dir); the gate resolves it in ITS OWN clone as a canonical union (RD-684's block first),
#   an EMULATION, predicted blob 1f708e2. D and E are file-disjoint (counts only) and are gated on merged-forward trees of the gate's own.
#   Predicted merged counts(M0) + 36 / + 5 = 4169/252 at 1904765.
#
# AUTHORITY: Tuesday's batch #3 commission (2026-09-27); READY mails from NexusAI-N, copies in briefs/ (RD-324 and RD-684: updated + first).
# Merges: Tuesday's GO (Kam 2026-09-25 ~22:0x). This gate is FINDINGS-ONLY: no fix, no push, no deploy, nothing to Partner Center/demo/prod.
#
# PATTERN: launch_qa_nexusai_gate_batch1.sh (guard families 9 6 7 8 18 22 75 23 35 70 31 39 10 17 11 12-15 20 19 24 53 71 76 77 78 79 38 32 40),
# prompt EMBEDDED. CHANGES, each deliberate:
#   - 7/8: per-ticket bases (1904765 x3, 5f2683c, 11666d3) and every chain exact with parents; main's parents exact.
#   - 18b: main must be 1904765 or a descendant in the object store (never fetched), and its movement must not touch the five deltas NOR
#     jsonStorage / azureLogAnalytics / customerDataFiles / recoveryLocations (the semantic-overlap files).
#   - 75: A's tip is the merge of 1904765; B's tip is cell+counts only; C's tip is the erasure module + cell + counts.
#   - 23: EXPECTED OVERLAPS: A∩B = A∩C = B∩C = {erasure module, counts}; every pair with D or E = counts only.
#   - 80 (NEW): the B x C conflict re-measured by merge-tree in a FRESH mktemp object dir (the NexusAI store as a read-only alternate):
#     exactly {erasure module, counts}; A x B and A x C counts only; M x D and M x E counts only. Refuse on any other result.
#   - 81 (NEW): the brief carries the canonical-union rule, the predicted blob, the merge-order table and the C-102 sweep section.
#   - 38: negative-control seats re-read 2026-09-27 08:55:47 AEST (NexusAI-P exited, NexusAI-N started, during drafting).
#   - 40: the routing line QA/NexusAI-batch3 must exist (checked AFTER the stamp; Tuesday adds it).
#   - 32: SELF-CHECK stamp, placeholder 2026-09-27 08:58 (comparand built by concatenation). LAST refusal before --check exits.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-batch3' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote) plus ONE merge-tree family
# (guard 80) whose objects go to a fresh mktemp dir, never to NexusAI's store; grep, ps, tmux.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch3.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..81 a guard refused
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
BRIEF="$BRIEFS/2026-09-27_nexusai-gate-batch3-rd324-rd684-rd685-rd424-rd314.md"
READY_A="$BRIEFS/2026-09-27_nexusai-rd324-READY-updated-mail.txt"
READY_A0="$BRIEFS/2026-09-26_nexusai-rd324-READY-mail.txt"
READY_B="$BRIEFS/2026-09-27_nexusai-rd684-READY-updated-mail.txt"
READY_B0="$BRIEFS/2026-09-26_nexusai-rd684-READY-mail.txt"
READY_C="$BRIEFS/2026-09-27_nexusai-rd685-READY-mail.txt"
READY_D="$BRIEFS/2026-09-26_nexusai-rd424-READY-mail.txt"
READY_E="$BRIEFS/2026-09-26_nexusai-rd314-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_N="$NX/session-tools/s84n"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
LANEPLAN="$NX/5_Project_History/2026-09-25_S84M_lane-plan.md"
PREV_B1="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/report.md"
PREV_G="$QA_DIR/projects/nexusai/reports/2026-09-25-gate-rd579-rd639/report.md"
B1_EV="$QA_DIR/projects/nexusai/reports/2026-09-26-gate-batch1/evidence"
PREV_FLOORLIB="$B1_EV/qa-floorlib.sh"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-27-gate-batch3/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch3'

BASE_SHA='7c47ec467f585e9db5daf3a82cdb96deae0b1e7a'      # the build base of e10e7d9, fa7ffe6, 8dd5de7
MAIN_M2='11666d3c4f615190646914270016419fffa642e2'       # RD-314's (and RD-684's build) base
MAIN_D='5f2683cd198067016d56a32ec4e1f46f4e45dcc6'        # RD-424's merge-forward base (batch #2's RD-428 merge)
MAIN_C='5628e750ebb967b8c6a8e2ca6eb12d9fa5d9b1a4'        # RD-685's build base
MAIN_SHA='1904765007e9447ac6c980f9840c0689a02abe6c'      # origin main at drafting (RD-627a's merge; batch #1 complete)
MAIN_P1='057016de2b2929c23f643b7346413199f370d3ce'       # 1904765's first parent (RD-627a head)
MAIN_P2='748cecec2a883a117560824ac5615c268dfe0800'       # 1904765's second parent (the RD-533 merge)
A_BRANCH='rd-324-ledger-union-s84n'
A_BUILD='e10e7d903eff71da65b5b7f52b19a17d30115cef'
A_FWD1='3beea5c523aeb21ed42fa719bafe0de7136578a5'
A_HEAD="${QA_A_HEAD_OVERRIDE:-168d8501d7414a876fcd963ea0689922735e7902}"
B_BRANCH='rd-684-redrive-carries-surviving-target-s84n'
B_BUILD='b5d65255153c52538ae8910d5f8d6648b691d483'
B_FWD='b474c85e8150b877e46acd657ad1772117e26420'
B_HEAD="${QA_B_HEAD_OVERRIDE:-7085ee7610d6576342e2e8f24afcdd66c9aa5adf}"
C_BRANCH='rd-685-hardlinked-store-s84n'
C_BUILD='724326f1164624e9fa86ce635ef16c68fa4e9062'
C_FWD='5adaedb5a8e28add95ea28f63121bc78255a6231'
C_HEAD="${QA_C_HEAD_OVERRIDE:-9d7076b0368f02ca030a904a2ce45de93739238e}"
D_BRANCH='rd-424-backup-after-write-s84n'
D_BUILD='fa7ffe635c689c3499faae28947b41559be2c7c1'
D_HEAD="${QA_D_HEAD_OVERRIDE:-2ce26eba9752554844bd885903826f409c7d22be}"
E_BRANCH='rd-314-law-window-after-source-s84n'
E_BUILD='8dd5de79fd96730b47a273e90a33c48ce8dcfa4d'
E_HEAD="${QA_E_HEAD_OVERRIDE:-ce148d5d8332606654c189cd14f3aadee227a407}"

COUNTS_FILE='scripts/verify-expected-counts.json'
ERASURE='backend/dataErasure.js'
A_EXPECTED_FILES="__tests__/rd324-ledger-guard-union.test.js
$ERASURE
$COUNTS_FILE"
B_EXPECTED_FILES="__tests__/rd684-redrive-keeps-surviving-target.test.js
$ERASURE
$COUNTS_FILE"
C_EXPECTED_FILES="__tests__/rd685-hardlinked-store.test.js
$ERASURE
$COUNTS_FILE"
D_EXPECTED_FILES="__tests__/backup-rotation-through-setsetting.test.js
__tests__/rd407-concurrent-settings-writers.test.js
__tests__/rd407-r2-missing-mid-swap.test.js
__tests__/rd424-backup-after-write.test.js
__tests__/rd452-restore-never-downgrades-group.test.js
__tests__/rd535-restore-never-reopens-configured.test.js
backend/jsonStorage.js
$COUNTS_FILE"
E_EXPECTED_FILES="__tests__/rd314-law-window-after-source.test.js
backend/azureLogAnalytics.js
$COUNTS_FILE"
SEMANTIC_FILES="backend/jsonStorage.js
backend/azureLogAnalytics.js
backend/customerDataFiles.js
backend/recoveryLocations.js
$ERASURE"

LOCK_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'
UNION_BLOB='1f708e2'   # drafter's canonical union of the erasure module on M + A + B + C (either order)
NEG_SEATS='62649 9959 47349 67576 20317'   # NexusAI-M %19, -N %21, Tuesday %0, Vision_Sales_Portal %20, -P %22 — re-read 2026-09-27 08:55:47/08:56:40 AEST

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-324 · RD-684 · RD-685 · RD-424 · RD-314'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch3] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, Azure Files (SMB) hard-link semantics, a live Log Analytics workspace or any KQL execution, production mode, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "${1}:${2}" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI with FIVE targets, FIVE verdicts and ONE report: RD-324 (TIER 1), RD-684 (TIER 1), RD-685 (TIER 1), RD-424 (TIER 1) and RD-314 (TIER 1). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict; a finding that exists only in a COMPOSITION is graded on the merged tree and named against both tickets it joins. TIER 1 AT FULL WEIGHT, FINDINGS-ONLY: no fixes, no pushes, no deploys, nothing to Partner Center, the demo or production.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-27_nexusai-gate-batch3-rd324-rd684-rd685-rd424-rd314.md
Then the charter it names, then the seven READY mails it names (RD-324 and RD-684 each have an updated READY and a first READY: read both), then the batch #1 gate report it names (2026-09-26-gate-batch1: its D-F1 and D-C1 are what RD-684 and RD-685 claim to close, and its self-corrections are rules H-13 to H-16) and the RD-639 gate report (2026-09-25-gate-rd579-rd639). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE TARGETS. RD-324: branch rd-324-ledger-union-s84n at 168d8501d7414a876fcd963ea0689922735e7902 = e10e7d903eff71da65b5b7f52b19a17d30115cef merged forward onto 11666d3c4f615190646914270016419fffa642e2 and then onto main 1904765007e9447ac6c980f9840c0689a02abe6c; the erasure ledger's door keeps a union by entry identity. RD-684: branch rd-684-redrive-carries-surviving-target-s84n at 7085ee7610d6576342e2e8f24afcdd66c9aa5adf = b5d65255153c52538ae8910d5f8d6648b691d483 merged forward onto 1904765 at b474c85e8150b877e46acd657ad1772117e26420 plus the D-F1 cells; a surviving symlink target is carried across re-drives. RD-685: branch rd-685-hardlinked-store-s84n at 9d7076b0368f02ca030a904a2ce45de93739238e = 724326f1164624e9fa86ce635ef16c68fa4e9062 merged forward onto 1904765 at 5adaedb5a8e28add95ea28f63121bc78255a6231 plus the sibling-site follow-up; a hard-linked name is refused (C-169). RD-424: branch rd-424-backup-after-write-s84n at 2ce26eba9752554844bd885903826f409c7d22be = fa7ffe635c689c3499faae28947b41559be2c7c1 merged forward onto 5f2683cd198067016d56a32ec4e1f46f4e45dcc6 only — NOT onto 1904765; the store writer backs up after the write, with a five-file fixture grant (C-164). RD-314: branch rd-314-law-window-after-source-s84n at ce148d5d8332606654c189cd14f3aadee227a407 = 8dd5de79fd96730b47a273e90a33c48ce8dcfa4d merged forward onto 11666d3 only — NOT onto 1904765; the Log Analytics window goes right after the source. RD-324, RD-684 and RD-685 all edit the erasure module that RD-627a (already on main) also edited.

THE MERGE-TREES AND THE MERGE ORDER. The drafter measured, in a scratch object dir: RD-324 x RD-684 and RD-324 x RD-685 counts only (the erasure module auto-merges); RD-684 x RD-685 ONE content hunk in the erasure module plus counts; every pair with RD-424 or RD-314 counts only. RD-424 and RD-314 were never merge-treed by the author against the others: re-measure all ten pairs yourself, in a SCRATCH object dir of your own (GIT_OBJECT_DIRECTORY set to your dir, the NexusAI objects as a read-only alternate), and record NexusAI's object count before and after. The drafter proposes the merge order RD-324, RD-684, RD-685, RD-424, RD-314 with predicted counts 4137/248, 4144/249, 4152/250, 4159/251, 4169/252, and a C-68 re-run set BY NAME for each merge (for RD-684 x RD-685: rd684 + rd685 + rd639 + rd627a + every erasure-*). Challenge the order, confirm or correct the predicted end state, and derive every C-68 set properly in your own clone with a positive control.

THE ONE CONTENT HUNK — A CANONICAL UNION, AN EMULATION. C-57 says any conflicting file other than the counts file STOPS the fleet's merge; inside YOUR OWN clone you resolve it as an emulation, labelled so: RD-684's block in full, its closing brace, a blank line, the doc opener, then RD-685's block in full. It is NOT a concatenation of the two sides: the hunk excludes the shared doc opener and the shared closing brace, and the literal concatenation does not parse. Prove it three ways: node --check rc 0; the resolved file versus each side equals exactly the other ticket's own diff over 1904765; and its blob equals the drafter's prediction 1f708e2 once RD-324 is in. Both merge orders must give the same blob with the canonical order. Say in the verdict mail that the merged-tree verdict carries only to a real resolution with the same blob.

RD-424 AND RD-314 ARE ON OLDER BASES. Gate each head as pushed, AND on a merged-forward tree of your own: fwd-424 = M0 merged with 2ce26eb, fwd-314 = M0 merged with ce148d5, each in your own scratch clone, counts regenerated (predicted 4140/248 and 4143/248). You never push, never write a ref in NexusAI, and never merge into the author's branch: the fleet's merge-forward is the author's job after your verdict.

RD-324 (TIER 1). POSITIVE CONTROL FIRST: U1 and U2 red on 1904765's product code, U3 and U4 green, 4/4 at the head. Mutants M-A1 to M-A6 (M-A4: nothing pins the stated "prior wins" behaviour change). Rows g1 to g10 — g6 first: a sorted replacer array drops NESTED keys, so two file-less entries differing only inside a nested object may be one identity; and g10, the ledger on the merged tree where RD-684's richer entry meets the union. Prior work: re-gate 8's N8-6 fix shape.

RD-684 (TIER 1). POSITIVE CONTROL FIRST: F1, F3, F4, F5 and F6 red on 1904765 (F6 is the batch #1 gate's D-F1), F2 and F6b green, 7/7 at the head, the live sweeper's landing control proven. Mutants M-B1 to M-B7 (M-B2: F6 depends on parsing RD-627a's failure text; M-B4: nothing pins "only ENOENT resolves"). Rows h1 to h12 — h12 is D-F1's closure on a REAL loopback server: anonymous health must stay DEGRADED after the LIVE re-drive.

RD-685 (TIER 1). POSITIVE CONTROL FIRST: (a), (a-tree), (a-copy), (c) and (e) red on 1904765, (b), (d), (e2) green, 8/8 at the head, nlink proven in every fixture. Re-derive M-EXC and M-SIB, then M-C1 to M-C7 (M-C1, the eager census, is round 1's defect and the positive control of the negative-assertion sweep). Rows k1 to k16 — k12 first: after a refusal, an app write or an operator deleting OUR name changes the inode, and the drafter predicts the next run certifies purged while the outside name holds the erased bytes, the false certificate C-169 names; and k15: with DATA_DIR given with a trailing slash or as a relative path the census never counts a name as inside, so the exception may never fire.

RD-424 (TIER 1). POSITIVE CONTROL FIRST at 5f2683c and at 1904765, 7/7 at the head and on fwd-424; the five granted files' assertions byte-identical per cell (C-164). Re-derive M-ROT, M-RETRY, M-GRP and M-POST, then M-D1 to M-D5. Rows r1 to r12 — r8 first, the COMPOSITION: an erasure that RD-684 or RD-685 keeps purged_incomplete keeps the R-1 freeze on, so every write skips its backups; measure it on the merged tree against fwd-424. Then r9, a clearing write. One REAL server boot after a tear (L-D1).

RD-314 (TIER 1). POSITIVE CONTROL FIRST: S1, S2 and five S3 shapes red on 11666d3's and 1904765's query layer, 10/10 at the head and on fwd-314, the cells' own splitter proven independent of the product's. Mutants M-E1 to M-E7. Rows q1 to q17 on the exported function and through the query executor with axios stubbed at the wire and the network belt on — q5 (a sample inside a union operand), q11 (a triple-backtick string) and q13 (queries whose later stages drop columns) first. No workspace is ever contacted.

THE NEGATIVE-ASSERTION SWEEP (brief section 3b, C-102). The members add refusals and early paths to shared functions. For every negative-asserting existing cell among the callers, measure — with jest coverage of the product file, through the lock, at M0 and on the merged tree — whether it still reaches the line it is named for. Self-test first (a positive control, a negative control, a non-empty population) or ABORT. Census existing fixtures that create hard links. Report population, negative cells, still reaching, disarmed.

THE MERGED TREE — part of every verdict. In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; merges and commits in the clone ONLY): M0, then merge --no-ff 168d850, 7085ee7, 9d7076b, 2ce26eb, ce148d5. Predict each merge before it; anything other than the counts file and the one erasure hunk conflicting STOPS. C-104: resolve and stage before any census or run. Counts by REGENERATION once after all five: predicted 4169/252 at M0 = 1904765, a prediction; the measurement decides. A second clone in reverse order, the union canonical, root trees identical apart from the counts file. C-112's condition beside the conclusion (294 test files predicted, none content-merged; the erasure module identical to no parent, proven by behaviour). id-superset control with batch #1's adapted C-57 copy, six parents, missing 0 predicted (RD-424 MODIFIES five test files: H-12; C-133 and its ADDENDUM only if it misses). On the merged tree, one hold: every C-68 set by name, the merged columns of the composition rows, the sweep, the full verify, then one mutant per ticket (M-A1, M-B1, M-EXC, M-POST, M-E1) and M-BC. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by mtime. Nothing leaves your clone.

FULL VERIFY of each head, of fwd-424, of fwd-314 and of the merged tree through the lock, SESSION_SECRET UNSET. Predicted 168d850 4137/248, 7085ee7 4140/248, 9d7076b 4141/248, 2ce26eb 4044/243, ce148d5 4022/238, fwd-424 4140/248, fwd-314 4143/248, merged 4169/252. Every failure by NAME; re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-16 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: never construct a product storage object on a DATA_DIR you are measuring after its server booted or its erasure ran. H-3: a LANDING CONTROL for every hook, preload, sweeper in LIVE mode, kill-inside-backup hook or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-5: restore your own perturbations before any hash. H-6: every extractor and census gets a positive control; quote every path (the QA path has spaces and a bang); every server under the network belt. H-7: mutants only through a quoted tool with a negative control. H-8: the exact new text present and the old absent once it is removed. H-9: byte-level plants via Buffer and xxd. H-10: prove the phenomenon reachable (the link, nlink and inode, the tear, the re-drive) before measuring its absence. H-11: /bin/bash explicitly; every sha:path braced; never set -- or declare -A in the default shell. H-12: list every modified or deleted test file before the C-57 control. H-13: NUL-safe tree censuses. H-14: every driver ends with an END record or the run is VOID. H-15: preloads with -r in argv, never NODE_OPTIONS. H-16: a sibling plant is checked with isInterruptedWriteOf first.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/batch3.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-tree, cat-file, rev-parse, merge-base, grep, ls-remote, archive, count-objects); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean, or merge-tree --write-tree without your own scratch object directory there, and never work in its 2_Project_Files checkout or any builder worktree (C-28). Symlinks, hard links, chmod, held ports and scratch git repos ONLY under your own mktemp dirs. Findings-only: never push, no commits outside your clone, no tickets, no edits in NexusAI, never merge anything anywhere the fleet can see. No Azure (no az at all), no demo, no public host, no Log Analytics. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 11 of the brief exactly. QUEUE, NEVER TAKE OVER: the NexusAI seats share session-tools/nexusai-lock.sh with you. Every jest run, server boot and erasure drive goes through it with a tag starting qa-b3- (C-141 gate-class, ADDENDUM 2 and 3: each new qa ticket earns a fresh, self-applied yield; C-110). When a merge ticket is already queued, file yours with --after that merge ticket's tag (C-141 ADDENDUM 4's tool), never ahead of it. Hold the lock once per multi-run measurement as a tracked child of your seat. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the brief's five negative-control seats classifying foreign in the same run (correct the stale ROOT and NEG defaults of batch #1's copied instrument first); record the foreign count beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request and erasure drive has a per-step DEADLINE and a client timeout, every server is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

CI: whether any of the five branches has a PR, and M0's CI Build, are UNVERIFIED by the drafter — read them with gh READ ONLY or say you could not. CI NOT RUN at a head with no PR.

RE-PIN at start, mid and end: all five branches and main — three timestamped readings with the branch name beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main may move: call main at your start M0; it must be 1904765 or a descendant whose movement touches none of the five deltas; if it moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch3. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch3] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-27-gate-batch3/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-324 · RD-684 · RD-685 · RD-424 · RD-314
Lead the body with one line per ticket (RD-324: <GO|GO WITH FINDINGS|NO GO> @ 168d850 · RD-684: … @ 7085ee7 · RD-685: … @ 9d7076b · RD-424: … @ 2ce26eb and fwd-424 · RD-314: … @ ce148d5 and fwd-314), then one line naming M0, your recommended merge order, and the erasure-module blob your union produced. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a planted needle or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list as the brief quotes it, every declared limit L-A1, L-B1 to L-B3, L-C1 to L-C3, L-D1 to L-D4 and L-E1 to L-E3 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. That section must carry this line verbatim:
Not tested by this gate: Linux or CI at any branch head unless a PR's CI Build exists, Azure Container Apps, Azure Files (SMB) hard-link semantics, a live Log Analytics workspace or any KQL execution, production mode, and Windows.
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
for S in "$BASE_SHA" "$MAIN_M2" "$MAIN_D" "$MAIN_C" "$MAIN_SHA" "$MAIN_P1" "$MAIN_P2" "$A_BUILD" "$A_FWD1" "$A_HEAD" "$B_BUILD" "$B_FWD" "$B_HEAD" \
         "$C_BUILD" "$C_FWD" "$C_HEAD" "$D_BUILD" "$D_HEAD" "$E_BUILD" "$E_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — bases against main-at-drafting: A, B, C contain 1904765; D's merge-base is 5f2683c; E's is 11666d3.
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(g merge-base "$MAIN_SHA" "$H" 2>/dev/null)" = "$MAIN_SHA" ] || { echo "REFUSING: merge-base(main, ${H:0:7}) is not 1904765" >&2; exit 7; }
done
[ "$(g merge-base "$MAIN_SHA" "$D_HEAD" 2>/dev/null)" = "$MAIN_D" ]  || { echo "REFUSING: merge-base(main, RD-424) is not 5f2683c" >&2; exit 7; }
[ "$(g merge-base "$MAIN_SHA" "$E_HEAD" 2>/dev/null)" = "$MAIN_M2" ] || { echo "REFUSING: merge-base(main, RD-314) is not 11666d3" >&2; exit 7; }

# 8 — chains exact, parents exact; main's own parents.
[ "$(g log --format='%H %P' "${MAIN_SHA}..${A_HEAD}" 2>&1)" = "$A_HEAD $A_FWD1 $MAIN_SHA
$A_FWD1 $A_BUILD $MAIN_M2
$A_BUILD $BASE_SHA" ] || { echo "REFUSING: 1904765..RD-324 is not exactly e10e7d9, 3beea5c (merge of 11666d3), 168d850 (merge of 1904765)" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${B_HEAD}" 2>&1)" = "$B_HEAD $B_FWD
$B_FWD $B_BUILD $MAIN_SHA
$B_BUILD $MAIN_M2" ] || { echo "REFUSING: 1904765..RD-684 is not exactly b5d6525, b474c85 (merge of 1904765), 7085ee7" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_SHA}..${C_HEAD}" 2>&1)" = "$C_HEAD $C_FWD
$C_FWD $C_BUILD $MAIN_SHA
$C_BUILD $MAIN_C" ] || { echo "REFUSING: 1904765..RD-685 is not exactly 724326f, 5adaedb (merge of 1904765), 9d7076b" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_D}..${D_HEAD}" 2>&1)" = "$D_HEAD $D_BUILD $MAIN_D
$D_BUILD $BASE_SHA" ] || { echo "REFUSING: 5f2683c..RD-424 is not exactly fa7ffe6 then 2ce26eb (merge of 5f2683c)" >&2; exit 8; }
[ "$(g log --format='%H %P' "${MAIN_M2}..${E_HEAD}" 2>&1)" = "$E_HEAD $E_BUILD $MAIN_M2
$E_BUILD $BASE_SHA" ] || { echo "REFUSING: 11666d3..RD-314 is not exactly 8dd5de7 then ce148d5 (merge of 11666d3)" >&2; exit 8; }
[ "$(g log -1 --format='%P' "$MAIN_SHA" 2>&1)" = "$MAIN_P1 $MAIN_P2" ] || { echo "REFUSING: 1904765's parents are not 057016d 748cece — re-brief" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote: the five ticket branches exactly the pinned heads (REFUSE on mismatch).
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  L="$(g ls-remote origin "refs/heads/$BR" 2>&1)"
  printf '%s\n' "$L" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
done
# 18b — main: it may move. It must be 1904765 or a descendant IN THE OBJECT STORE, and its movement must touch neither the five deltas
# nor the semantic-overlap files.
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}')" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 1904765 — main was rewritten; re-brief" >&2; exit 18; }
ALLD="$( { printf '%s\n' "$A_EXPECTED_FILES" "$B_EXPECTED_FILES" "$C_EXPECTED_FILES" "$D_EXPECTED_FILES" "$E_EXPECTED_FILES" "$SEMANTIC_FILES"; } | sed '/^$/d' | grep -vxF "$COUNTS_FILE" | sort -u)"
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ALLD") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 1904765..${M_ORIGIN:0:7} and touched a file of the five deltas or the semantic overlaps: $HIT — the merged-tree premise changes; re-brief" >&2; exit 18; }
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 1904765, $(printf '%s\n' "$MOVED" | sed '/^$/d' | wc -l | tr -d ' ') paths, none in the five deltas) — the gate re-pins M0 itself" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MAIN_SHA" "$A_HEAD" "$A_EXPECTED_FILES" "RD-324 (1904765..168d850)"
chk_delta "$MAIN_SHA" "$B_HEAD" "$B_EXPECTED_FILES" "RD-684 (1904765..7085ee7)"
chk_delta "$MAIN_SHA" "$C_HEAD" "$C_EXPECTED_FILES" "RD-685 (1904765..9d7076b)"
chk_delta "$MAIN_D"   "$D_HEAD" "$D_EXPECTED_FILES" "RD-424 (5f2683c..2ce26eb)"
chk_delta "$MAIN_M2"  "$E_HEAD" "$E_EXPECTED_FILES" "RD-314 (11666d3..ce148d5)"

# 75 — tips: B's tip is cell + counts; C's tip is the erasure module + cell + counts; main since D's and E's bases touches only the counts file of theirs.
[ "$(g diff --name-only "$B_FWD" "$B_HEAD" 2>/dev/null | sort)" = "$(sorted "__tests__/rd684-redrive-keeps-surviving-target.test.js
$COUNTS_FILE")" ] || { echo "REFUSING: b474c85..7085ee7 is not the RD-684 cell file + counts only" >&2; exit 75; }
[ "$(g diff --name-only "$C_FWD" "$C_HEAD" 2>/dev/null | sort)" = "$(sorted "$C_EXPECTED_FILES")" ] || { echo "REFUSING: 5adaedb..9d7076b is not the erasure module + RD-685 cell + counts" >&2; exit 75; }
for PAIR in "$MAIN_D D" "$MAIN_M2 E"; do
  BASE="${PAIR%% *}"; X="${PAIR#* }"; eval "WANTF=\"\$${X}_EXPECTED_FILES\""
  COMMON="$(comm -12 <(g diff --name-only "$BASE" "$MAIN_SHA" 2>/dev/null | sort) <(sorted "$WANTF") | tr '\n' ' ' | sed 's/ $//')"
  [ "$COMMON" = "$COUNTS_FILE" ] || { echo "REFUSING: main since ${BASE:0:7} shares '${COMMON:-<nothing>}' with target $X's files, expected the counts file only" >&2; exit 75; }
done

# 23 — EXPECTED OVERLAPS: A∩B = A∩C = B∩C = erasure module + counts; every pair with D or E = counts only.
DA="$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)"
DB="$(g diff --name-only "$MAIN_SHA" "$B_HEAD" 2>/dev/null | sort)"
DC="$(g diff --name-only "$MAIN_SHA" "$C_HEAD" 2>/dev/null | sort)"
DD="$(g diff --name-only "$MAIN_D" "$D_HEAD" 2>/dev/null | sort)"
DE="$(g diff --name-only "$MAIN_M2" "$E_HEAD" 2>/dev/null | sort)"
for PAIR in A_B A_C A_D A_E B_C B_D B_E C_D C_E D_E; do
  X="${PAIR%%_*}"; Y="${PAIR#*_}"; eval "SX=\"\$D$X\""; eval "SY=\"\$D$Y\""
  COMMON="$(comm -12 <(printf '%s\n' "$SX") <(printf '%s\n' "$SY") | tr '\n' ' ' | sed 's/ $//')"
  case "$PAIR" in
    A_B|A_C|B_C) WANT="$ERASURE $COUNTS_FILE" ;;
    *) WANT="$COUNTS_FILE" ;;
  esac
  [ "$COMMON" = "$WANT" ] || { echo "REFUSING: deltas $X and $Y share '${COMMON:-<nothing>}', expected '$WANT'" >&2; exit 23; }
done

# 35 — counts at every pinned sha.
for PAIR in "$BASE_SHA 3978 235" "$MAIN_M2 4012 237" "$MAIN_D 4037 242" "$MAIN_C 4120 244" "$MAIN_SHA 4133 247" \
            "$A_BUILD 3982 236" "$A_FWD1 4016 238" "$A_HEAD 4137 248" "$B_BUILD 4017 238" "$B_FWD 4138 248" "$B_HEAD 4140 248" \
            "$C_BUILD 4126 245" "$C_FWD 4139 248" "$C_HEAD 4141 248" "$D_BUILD 3985 236" "$D_HEAD 4044 243" "$E_BUILD 3988 236" "$E_HEAD 4022 238"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done

# 70 — package-lock identical everywhere (one node_modules serves every tree), main-now included.
for S in "$BASE_SHA" "$MAIN_M2" "$MAIN_D" "$MAIN_SHA" "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" package-lock.json)" = "$LOCK_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not ${LOCK_BLOB:0:7}" >&2; exit 70; }
done

# 80 — the merge-tree premise, re-measured in a FRESH scratch object dir (never NexusAI's store): B x C = {erasure module, counts};
# A x B, A x C counts only; M x D, M x E counts only.
MT_OBJ="$(mktemp -d "${TMPDIR:-/tmp}/qa-b3-mtobj.XXXXXX")" || { echo "REFUSING: cannot make a scratch object dir" >&2; exit 80; }
mt_conf() { GIT_OBJECT_DIRECTORY="$MT_OBJ" GIT_ALTERNATE_OBJECT_DIRECTORIES="$REPO/.git/objects" \
  git --no-optional-locks -C "$REPO" merge-tree --write-tree --name-only "$1" "$2" 2>/dev/null | awk 'NR==1{next} /^$/{exit} {print}' | sort | tr '\n' ' ' | sed 's/ $//'; }
[ "$(mt_conf "$B_HEAD" "$C_HEAD")" = "$ERASURE $COUNTS_FILE" ] || { echo "REFUSING: merge-tree RD-684 x RD-685 no longer conflicts in exactly {erasure module, counts} — re-brief" >&2; exit 80; }
for PAIR in "$A_HEAD $B_HEAD" "$A_HEAD $C_HEAD" "$MAIN_SHA $D_HEAD" "$MAIN_SHA $E_HEAD"; do
  X="${PAIR%% *}"; Y="${PAIR#* }"
  [ "$(mt_conf "$X" "$Y")" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} is not a counts-only conflict — re-brief" >&2; exit 80; }
done

# 31 — builder evidence, prior reports, standing references and tools on disk.
for f in "$READY_A" "$READY_A0" "$READY_B" "$READY_B0" "$READY_C" "$READY_D" "$READY_E" "$CLAR" "$LANEPLAN" "$PREV_B1" "$PREV_G" \
         "$EV_N/rd324/hold.out" "$EV_N/rd324/mf/hold.out" "$EV_N/rd324/mf2/hold.out" "$EV_N/rd684/hold.out" "$EV_N/rd684/mf/hold.out" \
         "$EV_N/rd685/hold.out" "$EV_N/rd685/mf/hold.out" "$EV_N/rd424/r2/hold.out" "$EV_N/rd424/mf/hold.out" "$EV_N/rd314/hold.out" "$EV_N/rd314/mf/hold.out" \
         "$EV_N/merge-tree-rd324-vs-rd684.txt" "$EV_N/merge-tree-rd685.txt" \
         "$NX/session-tools/nexusai-lock.sh" "$NX/session-tools/c57-id-superset.sh" \
         "$PREV_FLOORLIB" "$B1_EV/qa-floorcount.py" "$B1_EV/qa-dispatch.sh" "$B1_EV/qa-mutate.py" "$B1_EV/qa-c57-id-superset.sh" "$B1_EV/qa-netbelt.sb" \
         "$B1_EV/qa-d-probe-v2.js" "$B1_EV/qa-preload-sweeper-tick.js" "$B1_EV/q-merged-identity.py" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" || { echo "REFUSING: the RD-324 updated READY does not name ${A_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: the RD-684 updated READY does not name ${B_HEAD:0:7}" >&2; exit 31; }
grep -qF "${C_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-685 READY does not name ${C_HEAD:0:7}" >&2; exit 31; }
grep -qF "${D_HEAD:0:7}" "$READY_D" || { echo "REFUSING: the RD-424 READY does not name ${D_HEAD:0:7}" >&2; exit 31; }
grep -qF "${E_HEAD:0:7}" "$READY_E" || { echo "REFUSING: the RD-314 READY does not name ${E_HEAD:0:7}" >&2; exit 31; }
grep -qF "${B_HEAD:0:7}" "$READY_C" || { echo "REFUSING: the RD-685 READY does not name RD-684's head ${B_HEAD:0:7} (its merge-tree pairing)" >&2; exit 31; }

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$PREV_B1" "$PREV_G" "$READY_A" "$READY_A0" "$READY_B" "$READY_B0" "$READY_C" "$READY_D" "$READY_E"; do
  grep -qF "$P" "$BRIEF" || grep -qF "${P#$QA_DIR/}" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-324 is TIER 1' 'RD-684 is TIER 1' 'RD-685 is TIER 1' 'RD-424 is TIER 1' 'RD-314 is TIER 1' 'One verdict PER ticket' 'TIER 1 AT FULL WEIGHT'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-324 (TIER 1)' 'RD-684 (TIER 1)' 'RD-685 (TIER 1)' 'RD-424 (TIER 1)' 'RD-314 (TIER 1)' 'FIVE verdicts' 'TIER 1 AT FULL WEIGHT'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$MAIN_SHA" "$MAIN_M2" "$MAIN_D" "$A_BUILD" "$B_BUILD" "$B_FWD" "$C_BUILD" "$C_FWD" \
         "$D_BUILD" "$E_BUILD"; do
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
WORDS="RD-324 RD-684 RD-685 RD-424 RD-314 RD-627a RD-639 C-169 C-164 C-102 H-1 H-16 M0 COMPOSITION EMULATION 1f708e2 M-BC
POSITIVE%CONTROL%FIRST M-A1 M-A6 M-B1 M-B7 M-EXC M-SIB M-C1 M-C7 M-ROT M-POST M-D1 M-D5 M-E1 M-E7 g6 g10 h12 k12 k15 r8 r9 q5 q11 q13 q17
D-F1 D-C1 NEGATIVE-ASSERTION%SWEEP fwd-424 fwd-314 4169/252 4137/248 4140/248 4141/248 4044/243 4022/238 4143/248 SCRATCH%object%dir
does%not%parse reverse%order git%clone%--shared REGENERATION id-superset C-57 C-68 C-89 C-104 C-112 C-125 C-133 ADDENDUM C-141 --after C-110 C-28
node%--check VOID EXCLUSIVE qa-b3- QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT 2%minutes 5%minutes finally LANDING%CONTROL SESSION_SECRET%UNSET
NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CI%NOT%RUN Prior%work FOREGROUND never%push"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## RULED BY KAM, NOT YET IN AN ARTEFACT' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' '^## 8. TARGET E' \
         '^## 9. THE MERGED TREE' '^## 11. Floor discipline' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-B1 L-B3 L-C1 L-C3 L-D1 L-D4 L-E1 L-E3; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
  case "$PROMPT" in *"$L"*) ;; *) echo "REFUSING: prompt lacks declared limit $L (C-112)" >&2; exit 19 ;; esac
done
# every builder's NOT TESTED list is carried verbatim (one distinctive fragment from each READY, checked in the READY AND the brief)
for PAIR in "$READY_A0|a product caller that would reach the barrier with new entries" \
            "$READY_B0|A real server's public /api/health after the re-drive" \
            "$READY_C|Hard links on a real Azure Files share" \
            "$READY_C|Races: a new hard link created mid-purge." \
            "$READY_D|Concurrent writers on the post-write rotation" \
            "$READY_E|KQL forms beyond the six shapes"; do
  F="${PAIR%%|*}"; T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the NOT TESTED fragment '$T' verbatim" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b3-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push'; do
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

# 81 — this batch's own premises are in the brief: the canonical union and its blob, the C-57 stop, the merge order, the sweep.
for w in "$UNION_BLOB" 'CANONICAL UNION' 'EMULATION' 'Any other conflicting file still stops' '4169/252' 'rd684 + rd685 + rd639 + rd627a + every `erasure-*`' \
         'still reach the check it is NAMED for' 'fwd-424' 'fwd-314' 'H-13' 'H-16'; do
  grep -qF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 38 — negative-control seats named in the brief; advisory if one has exited or a pane's claude changed.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 11 before launch" >&2
done
if command -v tmux >/dev/null 2>&1; then
  for N in M N P; do
    tmux list-panes -a -F '#{@cockpit_name}' 2>/dev/null | grep -qx "Datasec/NexusAI-$N" || echo "NOTE: no tmux pane named Datasec/NexusAI-$N now (the seats churned during drafting) — re-read the seats before launch" >&2
  done
fi

# 32 — the coordinator stamps the self-check. LAST refusal, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 18b 22 75 23 35 70 80 31 39 10 17 11 12 13 14 15 20 19 24 53 71 76 77 78 79 81 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

# 40 — the answer route exists (after the stamp: Tuesday adds it, never this launcher).
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $A_BRANCH == ${A_HEAD:0:7}, $B_BRANCH == ${B_HEAD:0:7}, $C_BRANCH == ${C_HEAD:0:7}, $D_BRANCH == ${D_HEAD:0:7}, $E_BRANCH == ${E_HEAD:0:7} at $PIN_TS (18)"
  echo "  main ${M_ORIGIN:0:7} (1904765 or a descendant; moved paths touch none of the deltas or semantic overlaps) (18b)"
  echo "  bases 1904765 x3 / 5f2683c / 11666d3 (7); chains exact (8); deltas exact (22); tips (75); overlaps (23); counts at eighteen shas (35)"
  echo "  package-lock ${LOCK_BLOB:0:7} everywhere (70); merge-tree premise in scratch $MT_OBJ (80); evidence (31); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81)"
  echo "  route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/main = $M_ORIGIN (1904765 or a descendant whose movement touches none of the five deltas). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
