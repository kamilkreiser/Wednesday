#!/bin/bash
# launch_qa_nexusai_gate_batch17.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 17"), TWO members (+ an ADDENDUM SLOT),
# one verdict per ticket, ONE report (drafted 2026-10-06 06:21:13–06:41 AEDT by a read-only drafting agent for Tuesday).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-640 (TIER 1, erasure behaviour = data-destruction class; round 1 of 2) rd-640-eloop-and-tree-cells-s87n @ 588ec63: ONE commit on e91ff4e.
#       backend/dataErasure.js 1f708e2 -> 6002d71 (links resolving to nothing removed at every level; P-3 lstat); rd640 (10 ids); the GRANTED
#       erasure-verdict re-plant. 4272/261.
#   B — RD-697 (TIER 2, test-only) rd-697-purge-edge-cells-s87n @ a6c8f0e: ONE commit on e91ff4e. rd627a +T5 +T6. 4264/260.
#   THE CROSS (C-68): RD-697's T5/T6 test RD-627a's branches in the SAME product file RD-640 changes -> both orders + T5/T6 on the RD-640 product.
#   SLOT — RD-791 (F-A7) joins ONLY by the brief's line "ADDENDUM RD-791 JOINS @ <sha> ON <branch> TIER <1|2> | READY <path>" (guard 89). EMPTY.
#   Main at drafting 2f0ae4a (RD-609 via PR; counts 4263/260). Predicted MT1 4275/261. RD-648 then RD-618 merge next (main WILL move).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch17' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch17.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's RD-640 READY ack (fleet/briefs_staged/2026-10-06_nexusai_N_rd640_ready_ack.md: "RD-640 (tier 1) and RD-697 (tier 2) go to
# GATE BATCH 17 together") and the batch-17 commission (~06:20 AEDT); READY mails copied in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings: sqlite3 cached prebuild (2026-10-05_qa_b14_sqlite3_ANSWER.md); full verifies UNBELTED with 4 conditions (2026-10-05_qa_b14_belt_ANSWER.md);
# npm_config_update_notifier=false on EVERY npm call (2026-10-05_qa_gate16_notifier_ANSWER.md); the first-in-line re-file at a wait deadline
# (2026-10-06_qa_gate14_refile_ANSWER.md); C-190 + its ADDENDUM: BOTH CodeQL thresholds.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert; no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (node_modules offline only, H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch15.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the
# LIVE negative-control seat derivation 38R naming the coordinator pane 'tuesday', the ADDENDUM-SLOT JOINS parser 89, route-line and stamp guards
# last) + gate 16's carried rulings. CHANGES, each deliberate:
#   - members/bases/chains/deltas/premises for RD-640 and RD-697 (guards 6 7 8 22 93 94 98 23 35 70 80 31).
#   - 93: RD-640's premises — _linkTargetOrNull (ENOENT|ELOOP), P-3 statSync -> lstatSync at the store and the copy, the reason line, the GRANT.
#   - 94: RD-697's premises — T5/T6 added, titles kept, and the M-D4 / M-D7 anchors present once in BOTH products (THE CROSS's premise).
#   - 89: the SLOT is RD-791 (no branch at drafting), so the JOINS line carries its branch and tier.
#   - 38R: the NexusAI-P pane is GONE and -R is live (06:23:30): the five builder names are candidates, each LIVE one must carry exactly one claude,
#          'tuesday' is REQUIRED, at least three builder seats must be live; gates 14 and 15 added as peers if live (gate 16 delivered).
#   - no image build and no browser leg (the shipped change is one backend file: a manifest evaluation, READ).
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python/shasum over `git show` output; grep, ls, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch17.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..99 a guard refused
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
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
BRIEF="$BRIEFS/2026-10-06_nexusai-gate-batch17.md"
BRIEF15="$BRIEFS/2026-10-05_nexusai-gate-batch15.md"
BRIEF16="$BRIEFS/2026-10-05_nexusai-gate-batch16.md"
READY_A="$BRIEFS/2026-10-06_nexusai-rd640-READY-mail.txt"
READY_B="$BRIEFS/2026-10-06_nexusai-rd697-READY-mail.txt"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
REFILE_ANS="$STAGED/2026-10-06_qa_gate14_refile_ANSWER.md"
UNBELT15_ANS="$STAGED/2026-10-06_qa_gate15_unbelted_ANSWER.md"
ACK640="$STAGED/2026-10-06_nexusai_N_rd640_ready_ack.md"
WIDEN640="$STAGED/2026-10-06_nexusai_N_rd640_widen_ANSWER.md"
GRANT640="$STAGED/2026-10-06_nexusai_N_rd640_fixture_GRANT.md"
SCOPE640="$STAGED/2026-10-05_nexusai_N_rd640_scope_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_N="$NX/session-tools/s87n"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B16_DIR="$RPTS/2026-10-05-gate-batch16"
B16_REPORT="$B16_DIR/report.md"
B16_INST="$B16_DIR/evidence/inst"
B12_REPORT="$RPTS/2026-09-30-gate-batch12/report.md"
G4_REPORT="$RPTS/2026-09-22-gate4-rd575-rd524r2/report.md"
B1_REPORT="$RPTS/2026-09-26-gate-batch1/report.md"
PREV_FLOORLIB="$B16_INST/qa-floorlib16.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-06-gate-batch17/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch17'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

MAIN_SHA='2f0ae4a5a623eab73a1750d13535a18f8c0f5f5b'      # origin main at drafting (06:21:24 AEDT; RD-609 via PR)
BASE='e91ff4e7419bfe76880d23b19d1c17dbcd395626'          # RD-314's counts commit — both members' parent and merge-base
A_BRANCH='rd-640-eloop-and-tree-cells-s87n'
A_HEAD="${QA_A_HEAD_OVERRIDE:-588ec6311320eab91deca9bf9dbd0f4afed3a287}"
B_BRANCH='rd-697-purge-edge-cells-s87n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-a6c8f0e275336d24a96d13ad60c0e5248da30bd3}"
RD648='b12a475fa73b439eea49cc9f692ef915af478253'          # context: next to merge (s87n-merge-rd648 queued at drafting)
RD618='953a0e67f3c7240e53b7f97ab009b2caaab5f246'          # context: gate 16 GO WITH FINDINGS, merges after RD-648
C_BRANCH_HINT='rd-791'                                     # the SLOT's ticket; no branch on origin at drafting

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
DE='backend/dataErasure.js'
R640='__tests__/rd640-eloop-and-tree-cells.test.js'
EVD='__tests__/erasure-verdict-is-derived-from-failures.test.js'
R627='__tests__/rd627a-erasure-tmp-siblings.test.js'
JS='backend/jsonStorage.js'
CDF='backend/customerDataFiles.js'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
DKF='Dockerfile'
DIG='.dockerignore'

DE_M_BLOB='1f708e276482e5224ab9793d878e59ed0867b125'       # e91ff4e, M0, RD-697
DE_A_BLOB='6002d71c21f552ee4e745fda98053fec7c845471'       # RD-640
R640_BLOB='8a34dde5de4e27a8a75e79bca33a03a2adc7ec0c'
EVD_M_BLOB='4b75b241b3f039810f2e9ab5f6619f3b6da0928c'
EVD_A_BLOB='13c4d6356f39e687ec537a076a5df913818f040c'
R627_M_BLOB='9ea9de9e9b5a03c73452a0bbfe92ac1129376554'
R627_B_BLOB='fa16069f5e0a99954f7048ce4a78f9d803d19cf6'
LOCK_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'
JS_BLOB='296e78f18362b55625304bdf89f6501815bc2a46'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'
DE_M_SHA16='079a2cff8a2c18b2'                              # sha256 prefix of 1f708e2's content (RD-697's "main's product")
DE_A_SHA16='243deb4f36b1994f'                              # sha256 prefix of 6002d71's content (RD-640's "fix")
EVD_A_SHA16='641c7103734d62c1'                             # sha256 prefix of 13c4d63's content (the re-planted cell)

A_EXPECTED_FILES="$DE
$R640
$EVD
$COUNTS_FILE"
B_EXPECTED_FILES="$R627
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 17'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch17] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at either branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), the DAC cells under CI's runner user, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, any browser, a real customer volume (network mounts, other filesystems), a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
titles() { g show "${1}:${2}" 2>/dev/null | grep -E '^[[:space:]]*(test|it|describe)(\.each\(.*\))?\(' | sed -E 's/^[[:space:]]+//'; }
sha16() { g show "${1}:${2}" 2>/dev/null | shasum -a 256 | cut -c1-16; }
# multi-line anchor count in a blob (python, exact text)
acount() { g show "${1}:${2}" 2>/dev/null | python3 -c 'import sys; s=sys.stdin.read(); print(s.count(sys.argv[1]))' "$3" 2>/dev/null; }
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

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 17", with TWO members and an ADDENDUM SLOT, one verdict per ticket and ONE report. It is a FRESH gate. The members, both built by NexusAI-N (S87N): RD-640 (TIER 1, erasure behaviour = data-destruction class, round 1 of 2 under the cap: an erasure now removes a link that resolves to nothing — dangling ENOENT or looping ELOOP — at EVERY level (the directory-store tree, a store's interrupted-write tmp sibling, the store itself, a recovery copy) and records it purged with a logged reason; every OTHER resolution failure (EACCES and the rest) stays a failure with the link KEPT, because recording it purged would be a false erasure receipt; P-3's existence checks for a store and a recovery copy use lstatSync, not statSync; a link is never followed to delete its target; plus Tuesday's GRANTED re-plant of one erasure-verdict fixture; C-139 ADDENDUM 2; it answers gate 4's F-A5 and F-A3) and RD-697 (TIER 2, test-only: cells T5 and T6 for RD-627a's unlistable-data-directory and directory-shaped-tmp-sibling branches, red under the batch-1 gate's mutants M-D4 and M-D7; it answers batch-1 finding D-F2). Both members touch the erasure surface, and RD-697's cells test branches in the SAME product file RD-640 changes, so this gate carries THE CROSS (C-68): the merged tree in BOTH orders and RD-697's T5/T6 re-run ON THE RD-640 PRODUCT. The SLOT (RD-791, the export side split from RD-640 as F-A7) is a member ONLY if the brief's ADDENDUM SLOT carries a JOINS line — the launcher tells you below which it is. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree: one verdict per ticket. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry, no browser.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-06_nexusai-gate-batch17.md
It opens with the drafter's WRONG OR UNVERIFIED list, then TUESDAY'S RULINGS (a) to (n) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the two READY mails it names (read each WHOLE), Tuesday's four RD-640 rulings it names (scope, widen, fixture GRANT, READY ack), C-139 with its ADDENDUM and ADDENDUM 2 at source, gate 16's report (DELIVERED: its S-1 notifier lesson, its re-file log and its belt pair; its evidence/inst is the newest delivered instrument set), the gate-4 report (RD-640's prior round: F-A5, F-A3, F-A7) and the batch-1 report (RD-697's prior round: D-F2, M-D4, M-D7, rows d3 and d11a). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones (symlink loops, dangling and over-long chains, links to targets OUTSIDE DATA_DIR, EACCES-denied directories, product mutants that make the erasure skip, swallow or follow) — every one is an authorised, findings-only measurement in your own trees and your own mktemp dirs. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-640: rd-640-eloop-and-tree-cells-s87n at 588ec6311320eab91deca9bf9dbd0f4afed3a287 (ONE commit on e91ff4e7419bfe76880d23b19d1c17dbcd395626; backend/dataErasure.js 1f708e2 -> 6002d71; rd640 10 ids; the GRANTED erasure-verdict re-plant; counts 4272/261; NOT on M0). RD-697: rd-697-purge-edge-cells-s87n at a6c8f0e275336d24a96d13ad60c0e5248da30bd3 (ONE commit on e91ff4e; rd627a +T5 +T6; counts 4264/260; no product file; NOT on M0). The members share NO path but the counts file; they share the erasure surface semantically (THE CROSS, brief section 6). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b) — and it WILL: N's RD-648 merge ticket was queued at drafting and M's RD-618 follows. Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MTa = M0 + RD-697 4265/260; MTb = M0 + RD-640 4273/261; MT1 4275/261; predicted at M0 = 2f0ae4a5a623eab73a1750d13535a18f8c0f5f5b, 4263/260), the tests census (304 at MT1), new ids 12, missing 0. If gate 15's members (RD-719, RD-424 round 2, RD-735 round 2) or RD-648 or RD-618 are in your M0, re-derive every C-68 set on it (y5); if RD-424 round 2 is in it, its freeze scope reads filesFailed labels, and RD-640 adds a recovery-copy failure source — drive one EACCES copy link on MT1 and say which store it freezes. Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. No PR exists for either member at drafting: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY (the repo is datasecau/Reporting_Dashboard_Au). C-185 on M0 (ruling h): the known-failing set is {rd549 O4 only when envReached alone differs}; ANY rd465 O-1 failure is a STOP, named and mailed; a local failure of O4 is named and classified, never waved; gate 16's OBS-1 (sustainability-logger-live, fetch failed), if it recurs, is named with undici's err.cause and never cleared by a re-run.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-640: a0 RED-AT-PARENT first (the head's whole rd640 file on the head tree with only dataErasure.js restored to 1f708e2: E1-E5 and D1 red, K1-K3 and T1 green); a2 THE ERRNO MEASURED FIRST (realpathSync and realpathSync.native on a self-loop, a two-link loop, dangling, dangling through an outside link, EACCES, ENOTDIR, and a 33-hop and a 41-hop non-cyclic chain ending at a REAL outside file — quote each code); a3 THE ATTACK ROW — never follow a link to delete its target, at ALL FOUR levels, targets OUTSIDE DATA_DIR (file, directory, link-to-link) and an unlisted file inside, sha256 + size + inode + nlink + mtime and the outside listing before and after every purge and re-drive, with a modified-copy positive control; a4 THE SHAPES at every level (loop, two-link loop through outside, dangling, dangling through outside, EACCES kept as a failure and never purged, EPERM where producible, ENOTDIR, and ELOOP-BY-LENGTH with real data at the chain end — measured and named, Tuesday rules); a5 the reason line once per removed link and never otherwise; a6 THE GRANTED FIXTURE (C-97): assertions byte-identical, red from YOUR OWN product mutant M-p3-skip with the ABSENT-file control green, the old spy red on the new product, green for the right reason; a7 the real process and the sweeper re-drive (gate 4's A4 recipe); a8 needles; a9 the builder's six mutants (M-loopfail, M-anyerr, M-swallow, M-p3-store, M-p3-copy, M-copy-catchall) plus M-p3-skip, re-derived INDEPENDENTLY on the WHOLE erasure union, plus your own M-noReason, M-enoentOnly, M-anyNull, M-followTree, M-statCopyOnly, M-statStoreOnly; a10 F-A3 (iv), (v) and coexist; a12 C-68 (every dataErasure requirer, re-derived); a13 shipped blobs as a manifest evaluation, NO image built; a14 prior work. RD-697: b0 RED-UNDER-MUTANT first (C-98: the cells are green on main's product by design) — M-D4 and M-D7 re-derived INDEPENDENTLY, each on the whole rd627a file and the union, every red named; b2 batch 1's own M-D4 shape too; b3 green for the right reason by coverage (T5 reaches the (data directory) push, T6 reaches _purgeTree from _removeInterruptedWrite); b4-b7. THE CROSS: y1 RD-697's rd627a on RD-640's product before any merge, M-D4 and M-D7 re-derived ON 6002d71, coverage on both products — RD-640 changed P-3 to lstat: do T5 and T6 still reach their branches?; y2 both merge orders; y3 RD-640's mutants over RD-697's file; y4-y7.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff RD-697 (MTa), then RD-640 (MT1). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1 on node_modules proven for M0's lock: predicted 4275/261, re-based on YOUR M0; the measurement decides. A second clone in reverse order (RD-640 first = MTb), root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0; any missing id is a STOP. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). Neither member changes the lock or package.json, so there is NO npm registry exception in this gate. ONE lock is in play (e9063d4). ONCE: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline — and EVERY npm invocation, the first one included, carries npm_config_update_notifier=false (gate 16's S-1: the notifier made a registry GET despite --offline; Tuesday's ruling binds every later gate); prove the cache copy's _update-notifier-last-checked marker absent or unchanged. An ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install, never npx playwright install. sqlite3's binding: Tuesday ruled (04:55Z, to gate 14, carried here) that the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in your tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on this binding is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree; never from gate 14's or gate 15's (live) or gates 12/13/16's trees.

FULL VERIFY of each head and of MT1 through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 588ec63 4272/261, a6c8f0e 4264/260, MT1 4275/261. Both builder verifies ran on a WORKING TREE before the commit with --update-counts; yours decides. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed BEFORE; every purge and re-drive is a NEW process — declare it per row. H-3: a LANDING CONTROL for every link, loop, chain, chmod, outside target, mutant and spy. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd; link texts read back with readlink. H-15: preloads with -r in argv; no exception this batch. H-16: every plant checked to be what the product will treat it as (gate 16's S-2). H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate, and every chmod you make, is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and lock waits have run 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly under the SAME tag if not granted. H-29: gates 14 and 15 are live; their evidence is method only. H-31: offline node_modules, the notifier off, and the cached sqlite3 prebuild. H-32: NO image built (the shipped-blob rows are a manifest evaluation); no browser. H-33: links, loops, outside targets, chmod'd dirs and children counted and reaped or quarantined, never rm; a link you plant never points outside your own mktemp dirs. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch17.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gates 14's and 15's trees and report dirs are LIVE PEER gates' — never touch them; copy instruments BY COPY from gate 16's evidence/inst (its HOLD16.sh hard-codes its own evidence dir and its qa-floorlib16.sh carries stale ROOT and NEG defaults: re-point and correct your copies; its qa-file16b.sh carries the first-in-line re-file sequence and its qa-verify16.sh the notifier-off verify). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, probe, measure or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry, no browser. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gates 14 and 15 (QA/NexusAI-batch14 and -batch15, tags qa-b14- and qa-b15-) — PEER gates: FIFO, never touched — and the builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, plain-node rows, census greps); then file your holds tagged qa-b17-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG). AT A WAIT DEADLINE WHILE FIRST IN LINE (Tuesday's ruling to gate 14, carried by ruling i): do NOT plain re-file — file the replacement under the SAME tag with --after YOUR OWN still-waiting ticket, confirm it is queued, and only then withdraw the old ticket by the C-141 clean path (SIGTERM your own waiter; the ticket goes to released/ as ticket-left-*; never delete a ticket file); never two live holds; a duplicate-tag refusal takes a -r<N> suffix, said in the report; you never move ahead of anything that was ahead of you; one report line per re-file with the queue place before and after FROM THE QUEUE LISTING. Once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver, purge process and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: both member branches and main (and the SLOT's branch if it joins) — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main WILL move: call main at your start M0 and say so; it must be 2f0ae4a or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch17. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch17] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-06-gate-batch17/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 17
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-640 @ 588ec63 with the red at main's product, the attack row's target identity at each level, dangling/loop removed and purged per level, EACCES kept per level, ELOOP-by-length and ENOTDIR as measured, the reason line, the GRANT, the six builder mutants on the union, the re-drive, F-A3 (iv)/(v)/coexist; RD-697 @ a6c8f0e with M-D4 and M-D7 in both shapes, the branches reached, and THE CROSS on 6002d71; the SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured in both orders, the C-57 result, any combined blob, which rows ran on Opus 4.8 (or none), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR)". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A7, L-B1 to L-B3 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-139 with its ADDENDUM and ADDENDUM 2, C-97, C-98, C-185 with its ADDENDA, C-190 with its ADDENDUM and C-192 are the clarifications this batch leans on; C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141 with ADDENDUM 5, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at either branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), the DAC cells under CI's runner user, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, any browser, a real customer volume (network mounts, other filesystems), a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
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
for S in "$MAIN_SHA" "$BASE" "$A_HEAD" "$B_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: the base is on main; each member's merge-base with main (and with each other) is the base.
g merge-base --is-ancestor "$BASE" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: e91ff4e is not an ancestor of 2f0ae4a — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(RD-640, 2f0ae4a) is not e91ff4e — re-brief" >&2; exit 7; }
[ "$(g merge-base "$B_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(RD-697, 2f0ae4a) is not e91ff4e — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$B_HEAD" 2>/dev/null)" = "$BASE" ] || { echo "REFUSING: merge-base(RD-640, RD-697) is not e91ff4e — re-brief" >&2; exit 7; }

# 8 — chains exact: each member is ONE non-merge commit on e91ff4e.
for H in "$A_HEAD" "$B_HEAD"; do
  [ "$(g rev-parse "${H}^1" 2>/dev/null)" = "$BASE" ] && [ -z "$(g rev-parse --verify -q "${H}^2" 2>/dev/null)" ] \
    || { echo "REFUSING: ${H:0:7} is not ONE non-merge commit on e91ff4e" >&2; exit 8; }
done

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the two member branches exactly the pins (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY (and will) move (ruling b). It must be 2f0ae4a or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 2f0ae4a — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$DE" "$R640" "$EVD" "$R627" "$PKG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 2f0ae4a..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief (THE CROSS's premise moved)" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$LOCK" "$JS" "$CDF" "$TS" "$TSH" "$R465" "$R549" "$DKF" "$DIG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the C-68 sets and node_modules proofs run on M0's blobs (brief ruling b, y5)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 2f0ae4a; RD-648 / RD-618 / gate 15's members may have landed) — the gate re-pins M0 itself and re-bases every prediction" >&2
for X in "$RD648" "$RD618"; do
  if [ "$(g cat-file -t "$X" 2>&1)" = "commit" ] && g merge-base --is-ancestor "$X" "$M_ORIGIN" 2>/dev/null; then echo "NOTE: ${X:0:7} is now on origin main (y5 applies)" >&2; fi
done
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no lock/package change; product paths as commissioned.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$BASE" "$A_HEAD" "$A_EXPECTED_FILES" "RD-640 (e91ff4e..588ec63)"
chk_delta "$BASE" "$B_HEAD" "$B_EXPECTED_FILES" "RD-697 (e91ff4e..a6c8f0e)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$BASE" "$A_HEAD" "$DE")" = "73 22" ] && [ "$(ns "$BASE" "$A_HEAD" "$R640")" = "258 0" ] && [ "$(ns "$BASE" "$A_HEAD" "$EVD")" = "16 5" ] \
  || { echo "REFUSING: RD-640's numstats are not dataErasure +73/-22, rd640 +258, erasure-verdict +16/-5" >&2; exit 22; }
[ "$(ns "$BASE" "$B_HEAD" "$R627")" = "34 0" ] || { echo "REFUSING: RD-697's numstat is not rd627a +34/-0 (WRONG 1's measurement)" >&2; exit 22; }
for H in "$A_HEAD" "$B_HEAD"; do
  [ -z "$(g diff --name-only "$BASE" "$H" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} changes package-lock.json/package.json — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
[ "$(g diff --name-only "$BASE" "$A_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" = "$DE" ] || { echo "REFUSING: RD-640 touches a product path beyond $DE" >&2; exit 22; }
[ -z "$(g diff --name-only "$BASE" "$B_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" ] || { echo "REFUSING: RD-697 touches a product path — it is commissioned test-only (re-tier)" >&2; exit 22; }

# 93 — RD-640's premises at source.
[ "$(blob "$BASE" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$B_HEAD" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$A_HEAD" "$DE")" = "$DE_A_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$R640")" = "$R640_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$R640")" ] \
  && [ "$(blob "$BASE" "$EVD")" = "$EVD_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$EVD")" = "$EVD_M_BLOB" ] && [ "$(blob "$A_HEAD" "$EVD")" = "$EVD_A_BLOB" ] \
  || { echo "REFUSING: RD-640's blobs are not dataErasure 1f708e2 -> 6002d71 / rd640 8a34dde / erasure-verdict 4b75b24 -> 13c4d63" >&2; exit 93; }
[ "$(sha16 "$BASE" "$DE")" = "$DE_M_SHA16" ] && [ "$(sha16 "$A_HEAD" "$DE")" = "$DE_A_SHA16" ] && [ "$(sha16 "$A_HEAD" "$EVD")" = "$EVD_A_SHA16" ] \
  || { echo "REFUSING: the builder's sha256 stamps (079a2cff… / 243deb4f… / 641c7103…) no longer match the blobs (WRONG 3's premise)" >&2; exit 93; }
for T in 'function _linkTargetOrNull(p) {' "if (e.code === 'ENOENT' || e.code === 'ELOOP') return null;" 'function _noteLinkResolvedToNothing(label) {' \
         "logger.info('🗑️  Erasure removed a link that resolved to nothing (dangling or looping); no target was touched', { file: label });" \
         '                    fs.lstatSync(copy.path);' '                fs.lstatSync(full);' 'linkTarget = _linkTargetOrNull(child);' 'linkTarget = _linkTargetOrNull(full);' \
         'linkTarget = _linkTargetOrNull(copy.path);' 'liveLinkTarget = _linkTargetOrNull(full);' 'const copyRefusal = !isLink ? _hardLinkRefusal(copy.path, listedNames) : null;'; do
  [ "$(cnt "$A_HEAD" "$DE" "$T")" = "1" ] || { echo "REFUSING: dataErasure.js at 588ec63 lacks '$T' exactly once (a2-a5's premise)" >&2; exit 93; }
done
[ "$(cnt "$MAIN_SHA" "$DE" 'fs.statSync(copy.path);')" = "1" ] && [ "$(cnt "$MAIN_SHA" "$DE" 'fs.statSync(full);')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$DE" 'fs.statSync(copy.path);')" = "0" ] && [ "$(cnt "$A_HEAD" "$DE" 'fs.statSync(full);')" = "0" ] \
  && [ "$(cnt "$A_HEAD" "$DE" 'fs.statSync(_statePath());')" = "2" ] && [ "$(cnt "$MAIN_SHA" "$DE" '_linkTargetOrNull')" = "0" ] \
  || { echo "REFUSING: P-3's statSync -> lstatSync move (store + copy) or the two remaining state-file statSync calls are not as briefed" >&2; exit 93; }
[ "$(g show "${A_HEAD}:${R640}" 2>/dev/null | grep -cE '^[[:space:]]+test\(')" = "10" ] || { echo "REFUSING: rd640 is not ten test() cells" >&2; exit 93; }
for T in "test('E1 " "test('E2 " "test('E3 " "test('E4 " "test('E5 " "test('D1 " "test('K1 " "test('K2 " "test('K3 " "test('T1 "; do
  [ "$(cnt "$A_HEAD" "$R640" "$T")" = "1" ] || { echo "REFUSING: rd640 lacks the cell '$T' exactly once (E1-E5, D1, K1-K3, T1)" >&2; exit 93; }
done
[ "$(cnt "$A_HEAD" "$R640" "expect(fs.readFileSync(target, 'utf8')).toBe('CANARY-rd640-k1');")" = "1" ] || { echo "REFUSING: K1's outside-target read is not as briefed (WRONG 10)" >&2; exit 93; }
[ "$(g grep -c 'resolved to nothing' "$A_HEAD" -- __tests__ 2>/dev/null | grep -v 'brand-token-conformance' | grep -c .)" = "0" ] \
  || echo "NOTE: a test at 588ec63 now mentions 'resolved to nothing' — WRONG 9 (the reason line guarded by no cell) may be stale" >&2
[ "$(diff <(titles "$BASE" "$EVD") <(titles "$A_HEAD" "$EVD") >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: the GRANT changed an erasure-verdict title" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$EVD" "jest.spyOn(fs, 'lstatSync')")" = "1" ] && [ "$(cnt "$BASE" "$EVD" "jest.spyOn(fs, 'lstatSync')")" = "0" ] && [ "$(cnt "$A_HEAD" "$EVD" "jest.spyOn(fs, 'statSync')")" = "1" ] \
  || { echo "REFUSING: the GRANTED re-plant is not a statSync + lstatSync spy pair (a6's premise)" >&2; exit 93; }
P3SKIP="                if (e.code === 'ENOENT') continue;
                failed.push({ file: fname, error: \`could not stat: \${e.message}\` });
                continue;"
[ "$(acount "$A_HEAD" "$DE" "$P3SKIP")" = "1" ] || { echo "REFUSING: M-p3-skip's anchor (the store P-3 catch) is not present once at 588ec63 (a6's premise)" >&2; exit 93; }

# 94 — RD-697's premises at source, and THE CROSS's: the M-D4 / M-D7 anchors present once in BOTH products.
[ "$(blob "$BASE" "$R627")" = "$R627_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R627")" = "$R627_M_BLOB" ] && [ "$(blob "$A_HEAD" "$R627")" = "$R627_M_BLOB" ] && [ "$(blob "$B_HEAD" "$R627")" = "$R627_B_BLOB" ] \
  || { echo "REFUSING: rd627a is not 9ea9de9 (e91ff4e, M0, RD-640) -> fa16069 (RD-697)" >&2; exit 94; }
TD="$(diff <(titles "$BASE" "$R627") <(titles "$B_HEAD" "$R627") 2>/dev/null | grep -E '^[<>]')"
[ "$(printf '%s\n' "$TD" | grep -c '^>')" = "2" ] && [ "$(printf '%s\n' "$TD" | grep -c '^<')" = "0" ] && printf '%s\n' "$TD" | grep -qF "test('T5 " && printf '%s\n' "$TD" | grep -qF "test('T6 " \
  || { echo "REFUSING: RD-697's title diff is not exactly +T5 +T6 (b5's premise)" >&2; exit 94; }
[ "$(g show "${B_HEAD}:${R627}" 2>/dev/null | grep -cE '^[[:space:]]+test\(')" = "7" ] || { echo "REFUSING: rd627a at a6c8f0e is not seven test() cells" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$R627" 'fs.chmodSync(s.dir, 0o311);')" = "1" ] && [ "$(cnt "$B_HEAD" "$R627" 'fs.chmodSync(s.dir, 0o755);')" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$R627" "const sib = 'settings.json.tmp.4242.dd';")" = "1" ] || { echo "REFUSING: T5's 0311/0755 chmod pair or T6's directory sibling is not as briefed" >&2; exit 94; }
MD4="failed.push({ file: '(data directory)', error:"
MD7="    if (st.isDirectory()) {
        _purgeTree(full, label, purged, failed, census);
        return;
    }"
for S in "$MAIN_SHA" "$A_HEAD"; do
  [ "$(acount "$S" "$DE" "$MD4")" = "1" ] && [ "$(acount "$S" "$DE" "$MD7")" = "1" ] \
    || { echo "REFUSING: the M-D4 / M-D7 anchors are not present exactly once in dataErasure.js at ${S:0:7} (THE CROSS's premise, y1)" >&2; exit 94; }
done

# 98 — shared blobs identical at M0 and both heads; the image inputs as briefed.
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$JS")" = "$JS_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] \
    && [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] \
    || { echo "REFUSING: lock / package.json / jsonStorage / test-server / Dockerfile / .dockerignore at ${S:0:7} are not e9063d4 / cdb1168 / 296e78f / cff1e54 / 12aab55 / 3e45ec5" >&2; exit 98; }
done
for P in "$CDF" "$TSH" "$R465" "$R549"; do
  [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$A_HEAD" "$P")" ] && [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$B_HEAD" "$P")" ] || { echo "REFUSING: $P differs between M0 and a member" >&2; exit 98; }
done

# 23 — EXPECTED OVERLAPS: the members share only the counts file; main since the base touched no member path.
OVA="$(comm -12 <(g diff --name-only "$BASE" "$A_HEAD" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort) <(g diff --name-only "$BASE" "$B_HEAD" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort))"
[ -z "$OVA" ] || { echo "REFUSING: RD-640 and RD-697 share a path beyond the counts file: $OVA" >&2; exit 23; }
for H in "$A_HEAD" "$B_HEAD"; do
  OVM="$(comm -12 <(g diff --name-only "$BASE" "$MAIN_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort) <(g diff --name-only "$BASE" "$H" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort))"
  [ -z "$OVM" ] || { echo "REFUSING: main changed a path ${H:0:7} also changes since e91ff4e: $OVM — a COMBINED blob the brief does not predict" >&2; exit 23; }
done

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$BASE 4262 260" "$MAIN_SHA 4263 260" "$A_HEAD 4272 261" "$B_HEAD 4264 260"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$BASE" "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "303 303 304 303 " ] || { echo "REFUSING: the __tests__ census (e91ff4e M0 A B) is '$CENSUS', not '303 303 304 303'" >&2; exit 35; }

# 70 — the lock on origin main; the npm cache, the sqlite3 prebuild and the carried rulings (NOTEs where the gate decides, REFUSALs where a ruling is missing).
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not e9063d4 — another lock is in play; prove node_modules before any run (H-31)" >&2
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in axios/-/axios-1.20.0.tgz http-cache-semantics/-/http-cache-semantics-4.3.0.tgz sqlite3/-/sqlite3-5.1.7.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(shasum -a 256 "$PREBUILD" 2>/dev/null | cut -d' ' -f1)"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$REFILE_ANS" ] && grep -qF 'file the replacement under the SAME tag with --after YOUR OWN still-waiting ticket, confirm it is queued, and only then withdraw the old ticket' "$REFILE_ANS" \
  || { echo "REFUSING: Tuesday's first-in-line re-file ruling (ruling i) is not at $REFILE_ANS as quoted" >&2; exit 70; }

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean.
MT_PAIRS=0
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$A_HEAD $B_HEAD"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — READYs, rulings, builder evidence, prior reports, gate 16's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$ACK640" "$WIDEN640" "$GRANT640" "$SCOPE640" "$UNBELT15_ANS" "$BRIEF15" "$BRIEF16" "$B16_REPORT" "$B12_REPORT" "$G4_REPORT" "$B1_REPORT" "$C133" \
         "$EV_N/rd640-hold2.out" "$EV_N/rd640-hold3.out" "$EV_N/rd640-hold.sh" "$EV_N/rd640-hold3.sh" "$EV_N/rd640-measure.out" "$EV_N/rd697-hold.out" "$EV_N/rd697-hold.sh" \
         "$NX/session-tools/nexusai-lock.sh" \
         "$B16_INST/HOLD16.sh" "$B16_INST/qa-holdlib16.sh" "$B16_INST/qa-floorlib16.sh" "$B16_INST/qa-floorcount.py" "$B16_INST/qa-to.sh" "$B16_INST/qa-jestwrap.sh" "$B16_INST/qa-jsum.js" \
         "$B16_INST/qa-runj16.sh" "$B16_INST/qa-mut16.py" "$B16_INST/qa-mutlib16.sh" "$B16_INST/qa-merge16.sh" "$B16_INST/qa-pin16.sh" "$B16_INST/qa-build16.sh" "$B16_INST/qa-file16b.sh" \
         "$B16_INST/qa-wait16.py" "$B16_INST/qa-verify16.sh" "$B16_INST/qa-h1-selftest16.sh" "$B16_INST/qa-h1-scan.py" "$B16_INST/qa-mail.py" "$B16_INST/qa-mailread.py" "$B16_INST/qa-lockcheck.py" \
         "$B16_INST/qa-ssprint.sh" "$B16_INST/qa-netbelt.sb" "$B16_INST/qa-netbelt-nodns.sb" "$B16_INST/qa-netbelt-ctl.js" "$B16_INST/qa-blobcensus16.py" "$B16_INST/qa-c57-id-superset.sh" \
         "$B16_INST/qa-c57ctl16.py" "$B16_INST/qa-c68census.py" "$B16_INST/qa-cov-setup.js" "$B16_INST/qa-plant16.js" "$B16_INST/qa-endacct16.sh" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF 'PRIOR WORK' "$READY_A" && grep -qF 'PRIOR WORK' "$READY_B" \
  || { echo "REFUSING: a READY does not name its head or carry its PRIOR WORK section" >&2; exit 31; }
grep -qF 'RD-640 (tier 1) and RD-697 (tier 2) go to GATE BATCH 17 together.' "$ACK640" && grep -qF 'ACCEPTED, not vetoed.' "$ACK640" \
  && grep -qF 'TIER 1 gate: this changes erasure behaviour (data destruction class). Round 1 of 2 under the cap.' "$WIDEN640" \
  && grep -qF 'RED PROOF FROM THE PRODUCT, not from the fixture' "$GRANT640" \
  || { echo "REFUSING: Tuesday's RD-640 ack / widen ANSWER / fixture GRANT no longer carry the lines the brief quotes" >&2; exit 31; }
grep -qF 'Tests:       6 failed, 4 passed, 10 total' "$EV_N/rd640-hold2.out" && grep -qF 'Tests:       38 passed, 38 total' "$EV_N/rd640-hold2.out" \
  && grep -qF 'FAIL __tests__/erasure-verdict-is-derived-from-failures.test.js' "$EV_N/rd640-hold2.out" && grep -qF 'main sha 079a2cff8a2c18b2' "$EV_N/rd640-hold2.out" \
  && grep -qF 'expectation UPDATED — tests=4272 suites=261' "$EV_N/rd640-hold3.out" && grep -qF 'VERDICT: PASS — 4272/4272 tests passed across 261 suites (jest exit 0)' "$EV_N/rd640-hold3.out" \
  && grep -qF '=== done 2026-10-05T18:40:59Z' "$EV_N/rd640-hold3.out" && grep -qF 'restored E 243deb4f36b1994f' "$EV_N/rd640-hold3.out" && ! grep -qF '=== HEAD ' "$EV_N/rd640-hold3.out" \
  && grep -qF 'expectation UPDATED — tests=4264 suites=260' "$EV_N/rd697-hold.out" && grep -qF 'VERDICT: PASS — 4264/4264 tests passed across 260 suites (jest exit 0)' "$EV_N/rd697-hold.out" \
  && grep -qF '=== done 2026-10-05T13:38:14Z' "$EV_N/rd697-hold.out" && ! grep -qF '=== HEAD ' "$EV_N/rd697-hold.out" \
  && grep -qF 'erasure-reaches-attachments.test.js __tests__/rd684-redrive-keeps-surviving-target.test.js __tests__/rd685-hardlinked-store.test.js' "$EV_N/rd640-hold.sh" \
  || { echo "REFUSING: a builder log or script no longer carries the line the brief quotes (WRONG 3-5's premise)" >&2; exit 31; }
grep -qF 'F-A5' "$G4_REPORT" && grep -qF 'a self-referencing link inside the tree can never be removed' "$G4_REPORT" && grep -qF 'D-F2' "$B1_REPORT" && grep -qF 'M-D7' "$B1_REPORT" \
  || { echo "REFUSING: the gate-4 / batch-1 reports no longer carry F-A5 / D-F2 as the brief quotes" >&2; exit 31; }
grep -qF 'GO WITH FINDINGS' "$B16_REPORT" && grep -qF 'update-notifier' "$B16_REPORT" || { echo "REFUSING: gate 16's report does not read as delivered with its S-1 notifier lesson" >&2; exit 31; }
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-53572\}' "$B16_INST/qa-floorlib16.sh" || echo "NOTE: gate 16's qa-floorlib16.sh ROOT default is no longer 53572 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF16" || echo "NOTE: gate 16's brief does not read as stamped by Tuesday — the brief calls it the stamped source of the carried rulings" >&2

# 83 — the C-133 script is the RD-658 version the brief names (ruling l / H-30).
C133_NOW="$(shasum -a 256 "$C133" 2>/dev/null | cut -d' ' -f1)"
[ "$C133_NOW" = "$C133_SHA" ] || echo "NOTE: session-tools/s78g/c133-accounting.py sha256 is '${C133_NOW:-unreadable}', not 6f938bfc…f972f — the gate names the version it used (H-30)" >&2

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$G4_REPORT" "$B1_REPORT" "$B16_REPORT" "$B12_REPORT" "$BRIEF15" "$BRIEF16" "$READY_A" "$READY_B" "$B16_INST/"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in '**RD-640 is TIER 1' '**RD-697 is TIER 2 (test-only).**' 'No image build and no browser leg' 'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' \
         'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'AT A WAIT DEADLINE WHILE FIRST IN LINE' 'THE CROSS'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-640 (TIER 1, erasure behaviour = data-destruction class' 'RD-697 (TIER 2, test-only' 'one verdict per ticket' 'THE CROSS' 'manifest evaluation, NO image built' 'UNBELTED' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'AT A WAIT DEADLINE WHILE FIRST IN LINE'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$MAIN_SHA" "$BASE"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$DE_M_BLOB" "$DE_A_BLOB" "$R640_BLOB" "$EVD_M_BLOB" "$EVD_A_BLOB" "$R627_M_BLOB" "$R627_B_BLOB" "$LOCK_BLOB" "$PKG_BLOB" "$JS_BLOB" "$DKF_BLOB" "$DIG_BLOB" "$TS_BLOB" "$RD648" "$RD618"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
for S in "$DE_M_SHA16" "$DE_A_SHA16" "$EVD_A_SHA16"; do grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name the stamp $S" >&2; exit 14; }; done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 17' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 17 has no priority member" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)) is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31 (RE-BASED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-33 (RE-BASED' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-33 (re-based)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-640 RD-697 RD-791 RD-648 RD-618 RD-424 C-49 C-57 C-68 C-89 C-97 C-98 C-102 C-104 C-112 C-115 C-125 C-139 C-141 ADDENDUM%5 ADDENDUM%2 C-174 C-185 C-186 C-190 C-192
RED-AT-PARENT RED-UNDER-MUTANT a0 a2 a3 a4 a5 a6 a7 a8 a9 a10 a12 a13 a14 b0 b2 b3 y1 y2 y3 y5 MTa MTb MT1 M0 F-A5 F-A3 F-A7 D-F2 M-D4 M-D7 T5 T6 E1-E5 D1 K1-K3
M-loopfail M-anyerr M-swallow M-p3-store M-p3-copy M-copy-catchall M-p3-skip M-noReason M-anyNull ELOOP ENOENT EACCES ENOTDIR ELOOP-BY-LENGTH lstatSync statSync realpathSync
OUTSIDE%DATA_DIR byte-identical GRANTED false%erasure%receipt resolves%to%nothing re-drive sweeper 6002d71 1f708e2 e9063d4 4275/261 4273/261 4265/260 4272/261 4264/260 4263/260
L-A1 L-A7 L-B1 L-B3 L-Y1 H-1 H-2 H-3 H-9 H-15 H-16 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION
id-superset pull%request missing%0 new%ids%12 STOP JOINS ADDENDUM%SLOT POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b17- qa-b14- qa-b15- MERGES%GO%FIRST
QUEUE,%NEVER%TAKE%OVER --after UNCHANGED%tag DEADLINE HEARTBEAT PEER%gates 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center gate%4 batch-1 gate%16
npm%install --offline ENOTCACHED HOLD16.sh qa-floorlib16.sh qa-file16b.sh qa-verify16.sh Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> OBS-1 err.cause"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. THE CROSS' '^## 7. THE MERGED TREE' '^## 8. CI' \
         '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOT' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' \
         '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# the WRONG list sits ABOVE the rulings (the commission's order)
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-B1 L-B2 L-B3 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 b0 b1 b2 b3 b4 b5 b6 b7 y1 y2 y3 y4 y5 y6 y7; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
# every builder's stated scope / limits / interpretation lines carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|Drivable as plain jest/node on a temp DATA_DIR; no server, no auth, no browser leg.
A|If you want the reason IN the ledger, that is a ledger schema change and I would ask first.
A|(v) NOT PROVEN: no export cell reddens when _filesUnder keeps links (erasure-reaches-attachments, rd631, rd616-617 all green). coexist NOT PROVEN: rd631 stays green with sessions unredacted. These are findings, reported as they are.
A|F-A6 closed by RD-631 4ff2d45; F-A7 split to RD-791.
B|Test code only (__tests__/rd627a-erasure-tmp-siblings.test.js +36, counts +2). No product file. Drivable as plain jest on a temp DATA_DIR; no server, no auth, no browser leg.
B|The product is unchanged; T1-T4 and POPULATION are unchanged.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
is UNLINKED and recorded in `purged`, with the reason "link resolved to nothing"
recording it purged would be a false erasure receipt
Never follow a link to delete its target, at any level (unchanged).
erasure removing too much is the safe direction
When a fix reddens an older test, the FIXTURE changes, never the policy
A cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX, never the defect that exists before it
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
a FAILED ls-remote is UNKNOWN, never a value.
absence of a port clash is NOT evidence of a quiet floor.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
counts as known ONLY when the received object differs from the expected in `envReached` alone
Both O-1 cells LEAVE the set when RD-733 merges.
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
No re-run is used as a clearance
THE TURN PASSES
Addendum 2's "once PER WAITING GATE TICKET" means once per gate TAG.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b17-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' 'PEER gate' 'UNCHANGED tag' \
         'ticket-left-*' 'never two live holds' '-r<N>'; do
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
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify' 'readlink'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant rule fragment '$w' (H-9)" >&2; exit 78; }
done

# 79 — quoted mutant tool with a negative control; insertion-aware landing rule (H-7, H-8).
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing rule fragment '$w' (H-7/H-8)" >&2; exit 79; }
done

# 81 — this batch's own premises (and the carried lessons) are in the brief.
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4275/261' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' 'shippedFiles' \
         '_linkTargetOrNull' 'lstatSync' 'ELOOP' 'ENOTDIR' 'EACCES' 'OUTSIDE DATA_DIR' 'byte-identical' 'false erasure receipt' 'resolved to nothing' 'M-loopfail' 'M-anyerr' 'M-swallow' \
         'M-p3-store' 'M-p3-copy' 'M-copy-catchall' 'M-p3-skip' 'M-D4' 'M-D7' 'T5' 'T6' 'GRANT' 'C-97' 'C-98' 'F-A5' 'F-A3' 'F-A7' 'D-F2' 'NOT PROVEN' 're-drive' 'MAXSYMLINKS' \
         '2f0ae4a' 'ANY rd465 O-1 failure' 'ADDENDUM SLOT' 'RD-791 SLOT' 'WRONG 7' 'WRONG 8' 'WRONG 13' 'OBS-1' 'S-1' 'S-6' 'qa-floorlib16.sh' 'HOLD16.sh' 'qa-file16b.sh' \
         'ADDENDUM 5' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31' 'Tuesday rules at stamp'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the RD-791 ADDENDUM SLOT: EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
C_JOINS="$(grep -E '^ADDENDUM RD-791 JOINS @ [0-9a-f]{40} ON [A-Za-z0-9._/-]+ TIER [12] \| READY /' "$BRIEF" 2>/dev/null)"
C_EMPTY="$(grep -c '^RD-791 SLOT: EMPTY$' "$BRIEF" 2>/dev/null)"
C_STATE=''
SLOT_DESC=''
C_NOW=''
if [ -n "$C_JOINS" ]; then
  [ "$(printf '%s\n' "$C_JOINS" | grep -c .)" = "1" ] && [ "$C_EMPTY" = "0" ] || { echo "REFUSING: the RD-791 ADDENDUM SLOT has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  C_SHA="$(printf '%s\n' "$C_JOINS" | sed -E 's/^ADDENDUM RD-791 JOINS @ ([0-9a-f]{40}) .*/\1/')"
  C_BRANCH="$(printf '%s\n' "$C_JOINS" | sed -E 's/^.* ON ([A-Za-z0-9._/-]+) TIER .*/\1/')"
  C_TIER="$(printf '%s\n' "$C_JOINS" | sed -E 's/^.* TIER ([12]) .*/\1/')"
  C_READY="$(printf '%s\n' "$C_JOINS" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  case "$C_BRANCH" in *"$C_BRANCH_HINT"*) ;; *) echo "REFUSING: the SLOT's branch '$C_BRANCH' does not name $C_BRANCH_HINT (89)" >&2; exit 89 ;; esac
  lsr "refs/heads/$C_BRANCH" || { echo "REFUSING: ls-remote of the SLOT's branch failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN (C-192) (89)" >&2; exit 89; }
  C_NOW="$(printf '%s\n' "$LSR_OUT" | awk -v r="refs/heads/$C_BRANCH" '$2==r{print $1}')"
  [ "$C_NOW" = "$C_SHA" ] || { echo "REFUSING: the RD-791 ADDENDUM names $C_SHA but origin $C_BRANCH is '${C_NOW:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$C_SHA" 2>&1)" = "commit" ] || { echo "REFUSING: RD-791 $C_SHA is not in the object store (89)" >&2; exit 89; }
  [ -s "$C_READY" ] && grep -qF "${C_SHA:0:7}" "$C_READY" || { echo "REFUSING: RD-791's READY '$C_READY' is absent or does not name ${C_SHA:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$C_SHA" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: RD-791 ${C_SHA:0:7} is already on main (89)" >&2; exit 89; fi
  [ -z "$(g diff --name-only "$(g merge-base "$C_SHA" "$M_ORIGIN")" "$C_SHA" -- "$LOCK" "$PKG" 2>/dev/null)" ] || echo "NOTE: RD-791 changes the lock or package.json — ruling (m) does not cover it; Tuesday rules" >&2
  for X in "$M_ORIGIN" "$A_HEAD" "$B_HEAD"; do
    RC="$(conflicts "$X" "$C_SHA" | tr '\n' ' ' | sed 's/ $//')"
    [ -z "$RC" ] || [ "$RC" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x RD-791 conflicts beyond the counts file: '$RC' (89)" >&2; exit 89; }
    MT_PAIRS=$((MT_PAIRS + 1))
  done
  C_STATE="RD-791 (F-A7) JOINS this gate per the brief's ADDENDUM SLOT, at $C_SHA (origin $C_BRANCH, re-pinned by the launcher), TIER $C_TIER as Tuesday wrote it, READY $C_READY — gate it by the brief's ADDENDUM SLOT rows (c0-c5) and C-139's ADDENDUM at source; merge it LAST (MT2)."
  SLOT_DESC="JOINS @ ${C_SHA:0:7} ($C_BRANCH, tier $C_TIER)"
else
  [ "$C_EMPTY" = "1" ] || { echo "REFUSING: the RD-791 ADDENDUM SLOT is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
  C_STATE="RD-791 is NOT a member of this gate (the brief's ADDENDUM SLOT is EMPTY): do not gate it; say so in the report."
  SLOT_DESC="EMPTY"
fi

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  for PT in qa-b14- qa-b15-; do
    BQ="$(grep -l "$PT" "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
    [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate ($PT) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
  done
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell.
# CHANGED for batch 17 (brief WRONG 12): the builder panes are CANDIDATES (P is gone, R is new at drafting): each LIVE one must carry exactly one claude;
# 'tuesday' is REQUIRED; at least three builder seats must be live. REFUSES otherwise.
command -v tmux >/dev/null 2>&1 || { echo "REFUSING: tmux not found — cannot derive the negative-control seats" >&2; exit 38; }
PANES="$(tmux list-panes -a -F '#{pane_pid} #{@cockpit_name}' 2>/dev/null)"
[ -n "$PANES" ] || { echo "REFUSING: tmux list-panes returned nothing — cannot derive the negative-control seats" >&2; exit 38; }
PSTAB="$(ps -axo pid=,ppid=,comm= 2>/dev/null)"
[ -n "$PSTAB" ] || { echo "REFUSING: ps returned nothing" >&2; exit 38; }
claude_under() {   # prints the claude pids among the descendants (depth <= 5) of pane pid $1
  printf '%s\n' "$PSTAB" | awk -v root="$1" '
    { pid[NR]=$1; pp[NR]=$2; c=$3; sub(/^.*\//,"",c); cm[NR]=c }
    END { lvl[root]=0; for (d=1; d<=5; d++) for (i=1;i<=NR;i++) if ((pp[i] in lvl) && !(pid[i] in lvl) && lvl[pp[i]]==d-1) lvl[pid[i]]=d;
          for (i=1;i<=NR;i++) if ((pid[i] in lvl) && pid[i]!=root && cm[i]=="claude") print pid[i] }'; }
pane_pid_of() { printf '%s\n' "$PANES" | awk -v n="$1" '{p=$1; $1=""; sub(/^ /,""); if ($0==n) print p}'; }
NEG_SEATS=''; NEG_DESC=''; NEG_BUILDERS=0
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R tuesday; do   # the coordinator pane is named 'tuesday' on this seat (gate 14's launcher fix, s97, 2026-10-05)
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "$NP" = "0" ]; then
    [ "$NAME" = "tuesday" ] && { echo "REFUSING: no tmux pane named 'tuesday' — the coordinator's negative control is required" >&2; exit 38; }
    echo "NOTE: no tmux pane named '$NAME' — that builder seat is not a negative control this launch" >&2; continue
  fi
  [ "$NP" = "1" ] || { echo "REFUSING: more than one tmux pane named '$NAME': '$PP' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
  [ "$NAME" = "tuesday" ] || NEG_BUILDERS=$((NEG_BUILDERS + 1))
done
NEG_SEATS="${NEG_SEATS# }"
[ "$NEG_BUILDERS" -ge 3 ] || { echo "REFUSING: only $NEG_BUILDERS live builder seat(s) among M/N/O/P/R — at least three negative controls are required" >&2; exit 38; }
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
for PEER in 'QA/NexusAI-batch14' 'QA/NexusAI-batch15' 'QA/NexusAI-batch16'; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
  else
    echo "NOTE: no live claude under a pane named $PEER — that peer gate finished or its pane is gone" >&2
  fi
done

# 86 — no live gate-17 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 17 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-640 $A_HEAD · RD-697 $B_HEAD · SLOT RD-791: $SLOT_DESC" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 2 member branches at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192)"
  echo "  main ${M_ORIGIN:0:7} (2f0ae4a or a descendant; no member path moved) (18b)"
  echo "  merge-bases (7); chains (8); deltas + no lock change + product paths (22); premises (93 94 98)"
  echo "  overlaps (23); counts + census (35); lock + npm cache + sqlite3 prebuild + the carried rulings (70); $MT_PAIRS three-argument merge-trees counts-only or clean (80, 89); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); RD-791 SLOT $SLOT_DESC (89); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/main = $M_ORIGIN (2f0ae4a or a descendant; no member path moved since 2f0ae4a). $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOT: $C_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
