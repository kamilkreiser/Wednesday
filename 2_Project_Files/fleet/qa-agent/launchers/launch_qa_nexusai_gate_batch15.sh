#!/bin/bash
# launch_qa_nexusai_gate_batch15.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 15"), TWO members (+ an ADDENDUM SLOT),
# one verdict per ticket, ONE report (drafted 2026-10-05 16:06:53–16:33:02 AEDT by a read-only drafting agent for Tuesday).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-719 (TIER 1, vendored third-party code shipped to users) rd-719-vendor-chartjs-s86p @ 7861a06: 0cb584d (red cells) on 3b6c9ec, then the vendoring + counts. 4240/257.
#   B — RD-424 round 2 "D-F2" (TIER 1, data-erasure safety) rd-424-backup-after-write-s84n @ cca852c: 2ce26eb (round 1) -> 08655ee (merge d4386e7) -> 15568c9 -> ef1c1ed -> cca852c. 4265/260.
#   SLOT — RD-735 round 2 (TIER 2) joins ONLY by the brief's line "ADDENDUM RD-735 JOINS @ <sha> | READY <path>" (guard 89). EMPTY at drafting by the commission's
#          design; origin rd-735-csp-intake-residue-r3-s86m moved 7d853b0 -> 7e2cc9f DURING drafting (16:13:09) and its READY is on disk (brief WRONG 1).
#   Main at drafting b7bb1e9 (RD-693 via PR #46; before it RD-685 d4386e7). Predicted MT1 4273/262 (MT2 4300/265 if the slot joins).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch15' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch15.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's 11:38 note (RD-719's four checks) and the batch-15 commission (~15:45 AEDT); READY mails copied in briefs/. THE MODEL RULE: Kam, live
# board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# sqlite3 binding: Tuesday's 04:55Z ruling to gate 14 (fleet/briefs_staged/2026-10-05_qa_b14_sqlite3_ANSWER.md), carried as ruling (m) with its three conditions.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (node_modules offline only, H-31), no browser download.
#
# PATTERN: launch_qa_nexusai_gate_batch14.sh (prompt EMBEDDED, --check mode, pin guards, THE MODEL RULE, floor, H-rules, the LIVE negative-control seat
# derivation 38R naming the coordinator pane 'tuesday', route-line and stamp guards last) + gate 13's ADDENDUM-SLOT JOINS parser (89). CHANGES, each deliberate:
#   - members/bases/chains/deltas/premises for two members (guards 6 7 8 22 93 94 23 35 70 80 31).
#   - 93: RD-719's identity premise — sha384(vendored) == the integrity value the ROOT commit 8eb94ce pinned (log -S finds only 8eb94ce).
#   - 94: RD-424's premises — the four-site scope functions, D5's slip at 15568c9, the ledger label producers in M0's dataErasure.js.
#   - 89: the RD-735 SLOT — EMPTY (a NOTE names origin's head and the READY on disk) or ONE JOINS line, fully re-checked.
#   - 38R: gate 14's claude added as a negative control if its pane is live (the peer gate); gates 12/13 have delivered.
#   - one lock in play for the members (e9063d4); the SLOT's 9064763 checked only if it joins.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python/openssl/shasum over `git show` output; grep, ls, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch15.sh [--check]
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
BRIEF="$BRIEFS/2026-10-05_nexusai-gate-batch15.md"
BRIEF14="$BRIEFS/2026-10-05_nexusai-gate-batch14.md"
BRIEF_B3="$BRIEFS/2026-09-27_nexusai-gate-batch3-rd324-rd684-rd685-rd424-rd314.md"
READY_A="$BRIEFS/2026-10-05_nexusai-rd719-READY-mail.txt"
READY_B="$BRIEFS/2026-10-05_nexusai-rd424-r2-READY-mail.txt"
READY_C_SEEN="$BRIEFS/2026-10-05_nexusai-rd735-r2-READY-mail.txt"
SQLITE_RULING="$TUE/2_Project_Files/fleet/briefs_staged/2026-10-05_qa_b14_sqlite3_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_P="$NX/session-tools/s86p"
EV_N="$NX/session-tools/s87n"
EV_M="$NX/session-tools/s86m"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B13_DIR="$RPTS/2026-10-04-gate-batch13"
B13_INST="$B13_DIR/evidence/inst"
B12_DIR="$RPTS/2026-09-30-gate-batch12"
B12_REPORT="$B12_DIR/report.md"
B12_UNIT="$B12_DIR/evidence/qa-unit-b12.js"
B12_UNIT_SHA='1f735ce129c77087b2255b4e0a1428a6456d2d30a2061aa0c8c9b88866bd7153'
PREV_B3="$RPTS/2026-09-27-gate-batch3/report.md"
PREV_FLOORLIB="$B13_INST/qa-floorlib13.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-05-gate-batch15/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch15'
ROUTE_NAME14='QA/NexusAI-batch14'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'

MAIN_SHA='b7bb1e964173f0f91ea0f401794836f5f90bb057'      # origin main at drafting (16:07:25 and 16:13:09 AEDT; RD-693 via PR #46)
M_CF='cf0462f941c62c243417bb8076afbc0fe38312ef'          # gate 14's drafting base (ancestor check only)
M685='d4386e7dbaf7a634aed48648709cd254b49721c8'          # RD-685's main — B's merge-base
M692='3b6c9ec52cc6def9a47b3baff8b293fa27359e99'          # RD-692's main — A's merge-base
M1904='1904765007e9447ac6c980f9840c0689a02abe6c'         # the SLOT's merge-base
ROOT8='8eb94ce3568690d41a2e30a76e35b2687f265ba6'         # the root commit: the Chart.js integrity pin's origin
A_BRANCH='rd-719-vendor-chartjs-s86p'
A_HEAD="${QA_A_HEAD_OVERRIDE:-7861a0669e032f288e7a2c22ea74ad0efa8034a0}"
A_RED='0cb584d99d356958724901264b46df2ec6748e45'
B_BRANCH='rd-424-backup-after-write-s84n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-cca852c2f8b6902d05668b1e5be36a8c70881c58}"
B_FIX='ef1c1edf22b6c4793bf12ce241275fd5daeadbf2'
B_RED='15568c934c79a64ce586a47f125eabd119af98bb'
B_MRG='08655ee1eed6338c683dfdb3212cf7dcb821497f'
B_R1='2ce26eba9752554844bd885903826f409c7d22be'
C_BRANCH='rd-735-csp-intake-residue-r3-s86m'
C_R1='7d853b0e0b666b37d220dd05ac0727b5160555d2'           # RD-735 round 1 (gate 12's head)
C618='874c4f503d0f37a032014e562972b17e903e1072'           # RD-618 r2 (the SLOT is stacked on it; NOT on main)
C_SEEN='7e2cc9f7d0f777d2689f97f547f7d11b4f2b9078'         # origin at 16:13:09 (round 2); NOT pinned as a member — the JOINS line decides

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
VEN='static/vendor/chart-3.9.1.min.js'
IDX='static/index.html'
R719='__tests__/rd719-chartjs-vendored.test.js'
REC='__tests__/rd719-chartjs-3.9.1-provenance.json'
SRV='backend/server.js'
JS='backend/jsonStorage.js'
DE='backend/dataErasure.js'
CDF='backend/customerDataFiles.js'
R424='__tests__/rd424-backup-after-write.test.js'
DF2='__tests__/rd424-df2-freeze-named-stores.test.js'
G1='__tests__/rd407-concurrent-settings-writers.test.js'
G2='__tests__/rd407-r2-missing-mid-swap.test.js'
G3='__tests__/backup-rotation-through-setsetting.test.js'
G4='__tests__/rd452-restore-never-downgrades-group.test.js'
G5='__tests__/rd535-restore-never-reopens-configured.test.js'
CSPR='backend/services/cspReport.js'
R735B='__tests__/rd735-r2-linear-trim-and-hostless-userinfo.test.js'
R204='__tests__/rd204-vendor-coverage.test.js'
R490='__tests__/rd490-open-access-banner-browser.test.js'
DOMJS='__tests__/helpers/dom.js'
DKF='Dockerfile'
DIG='.dockerignore'
TS='__tests__/helpers/test-server.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'

SHA384='sha384-9MhbyIRcBVQiiC7FSd7T38oJNj2Zh+EfxS7/vjhBi4OOT78NlHSnzM31EZRWR1LZ'
VEN_SHA256='fbc45926e6b46845a0f905552a0e0b1331049bff1115ecf94dbe0904d895e710'
LOCK_M_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'     # 3b6c9ec, d4386e7, M0, A, B
LOCK_OLD_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'   # 1904765, 2ce26eb, the SLOT (pre-RD-741)
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'
VEN_BLOB='8f69759e05cd5be36a211b468823602fe30245f8'
IDX_M_BLOB='25b7bd84c251095fc5569ed90ecb9be3471c6b71'
IDX_A_BLOB='7bf527dc07248235222f0712295df9f60415cc0b'
R719_BLOB='fe52ff51aafa3a81360445b01fd1005587e82193'
REC_BLOB='0278e92bd2f18237cb058994c82601d9c52931c3'
SRV_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'
JS_M_BLOB='296e78f18362b55625304bdf89f6501815bc2a46'
JS_R1_BLOB='a63d8629786805756aa54e7f3b3cb4385f60121d'
JS_B_BLOB='2abb5cf487d75f2ce1730a028ade1b39cde31fd2'
DF2_BLOB='082682232741010da6ff2d62ddeb5fdc99fc1535'
DF2_RED_BLOB='b738075cd8eda4eb2a7a0d5d1c93602a1a9332d2'
DE_BLOB='1f708e276482e5224ab9793d878e59ed0867b125'
CSPR_R1_BLOB='6608eaece05c92c50303d5e738aef250e63c5455'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'
R204_BLOB='1517719'                                        # short id: prefix guard

A_EXPECTED_FILES="$VEN
$IDX
$R719
$REC
$COUNTS_FILE"
B_EXPECTED_FILES="$JS
$R424
$DF2
$G1
$G2
$G3
$G4
$G5
$COUNTS_FILE"
B_OWN_EXPECTED_FILES="$JS
$R424
$DF2
$COUNTS_FILE"
C_EXPECTED_FILES="$CSPR
$R735B
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 15'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch15] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Docker image build or image diff (the tier-1 image leg is a manifest evaluation), byte-identity of the vendored Chart.js to the official 3.9.1 release beyond the sha384 the root commit pinned (no network), the demo (behind RD-76 SSO), any deployed environment, any browser but local Chrome headless via Playwright against a local run, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
sblob() { local b; b="$(blob "$1" "$2")"; printf '%s' "${b:0:7}"; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
titles() { g show "${1}:${2}" 2>/dev/null | grep -E '^[[:space:]]*(test|it|describe)(\.each\(.*\))?\(' | sed -E 's/^[[:space:]]+//'; }
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

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 15", with TWO members and an ADDENDUM SLOT, one verdict per ticket and ONE report. It is a FRESH gate. The members: RD-719 (TIER 1, vendored third-party code shipped to users: NexusAI-P vendors Chart.js 3.9.1 into static/vendor/chart-3.9.1.min.js so the dashboard's trend charts draw on an install with no internet access; index.html loads it same-origin and keeps its integrity attribute; C-182; it answers batch-5a gate X-1, and RD-721 cannot start until this gate returns GO) and RD-424 round 2 (TIER 1, data-erasure safety: NexusAI-N narrows the R-1 erasure freeze in the shipped JsonStorage to ONLY the stores the FAILED ledger of an unfinished erasure names, at four freeze sites, keeping the full freeze for 'purging' and for an empty or untraceable ledger — Tuesday ACCEPTED both shapes in the C-164 ADDENDUM of 2026-10-05; it answers batch-3 gate finding D-F2). The SLOT: RD-735 round 2 (TIER 2, NexusAI-M: the f4 fix, the EDGE_C0_OR_SPACE trim made linear, plus f1's shapes) is a member ONLY if the brief's ADDENDUM SLOT carries a JOINS line — the launcher tells you below which it is. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict: one verdict per ticket. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry, no browser download.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-05_nexusai-gate-batch15.md
It opens with TUESDAY'S RULINGS (a) to (n) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the READY mails it names (read each WHOLE; RD-424's PRIOR WORK is its ADDENDUM, appended in the same file), then gate 14's stamped brief (the base of your instrument rules H-1 to H-33; gate 14 is LIVE: read only, never its trees, never its report dir), gate 12's report (its RESUME METHOD NOTE, and RD-735's f4 row if the slot joins), and the batch-3 report (RD-424's prior round: rows r1 to r12 and the r8 composition this round answers). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones (RD-719's swapped-file and SRI-tamper arms, RD-424's planted ledgers, symlink and hard-link erasures and torn stores, and, if the slot joins, RD-735's C0-run timing inputs and forged-report shapes) — every one is an authorised, findings-only measurement in your own trees. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-719: rd-719-vendor-chartjs-s86p at 7861a0669e032f288e7a2c22ea74ad0efa8034a0 (the red-first cells 0cb584d99d356958724901264b46df2ec6748e45 on main 3b6c9ec52cc6def9a47b3baff8b293fa27359e99, then the vendoring and counts; NOT on M0). RD-424 round 2: rd-424-backup-after-write-s84n at cca852c2f8b6902d05668b1e5be36a8c70881c58 (round 1 2ce26eba9752554844bd885903826f409c7d22be, gated in batch 3; the merge of main d4386e7dbaf7a634aed48648709cd254b49721c8 as 08655ee1eed6338c683dfdb3212cf7dcb821497f; red cells 15568c934c79a64ce586a47f125eabd119af98bb; fix and counts ef1c1edf22b6c4793bf12ce241275fd5daeadbf2; test-only hardening cca852c). The SLOT, if it joins: rd-735-csp-intake-residue-r3-s86m over round 1 7d853b0e0b666b37d220dd05ac0727b5160555d2, stacked on RD-618 874c4f503d0f37a032014e562972b17e903e1072, which is NOT on main. The members share NO path but the counts file. They share SEMANTIC surfaces: RD-719 adds a 199,560-byte shipped file under static/, so every test that walks the shipped set or static/ reads it on the merged tree (a10, y1); RD-424 changes when the shipped server backs up and restores a store, which every DATA_DIR-booting cell reaches (b10, y2). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MTa = M0 + RD-719 4256/260; MT1 = + RD-424 4273/262; MT2 = + the SLOT 4300/265, only if it joins; predicted at M0 = b7bb1e964173f0f91ea0f401794836f5f90bb057), the tests census (306 at MT1), new ids 21 (48 with the SLOT), missing 0. Gate 14 (QA/NexusAI-batch14) is LIVE and its eight members may land on main before or during your gate: if they are in your M0, re-derive every C-68 set on it. Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included). No PR exists for any member branch at drafting: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY (the repo is datasecau/Reporting_Dashboard_Au). C-185 on M0 (ruling h): RD-733 has merged, so both rd465 O-1 cells have LEFT the known set; the known-failing set is {rd549 O4 only when envReached alone differs}. ANY rd465 O-1 failure is a STOP, named and mailed; a local failure of O4 is named and classified, never waved. RD-719's head carries rd465 at its pre-RD-733 blob (stale-parent): say so beside any rd465 result there.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-719: a0 RED-AT-PARENT first (rd719 on 0cb584d: V1 to V4 red; the head with only index.html restored: V2 and V3 red); a2 IDENTITY OFFLINE — the vendored bytes' sha384 equals the integrity value the ROOT commit 8eb94ce pinned, and the record, with a one-byte-appended control; then state plainly what stays UNPROVEN offline (the pin's own provenance; no official 3.9.1 artefact on this machine) — the R-NET download runs ONLY if Tuesday stamped it; a3 LICENCE AND ATTRIBUTION — both MIT banners (Chart.js and the embedded @kurkle/color v0.2.1) in the shipped bytes, and whether any licence TEXT ships (a ruling, not a verdict); a4 CSP — no new script source, 'self' present, the real header from a local run; a5 THE IMAGE LEG as a MANIFEST EVALUATION (the gates' own shippedFiles over git ls-files with the real .dockerignore at M0, head and MT1, said as "manifest evaluation, NO image built"; a docker build is NOT RUN); a6 THE BROWSER LEG — a LOCAL RUN of 7861a06 and of 3b6c9ec, OFFLINE (every non-loopback request aborted), open mode, SESSION_SECRET UNSET, Playwright 1.62.1 from YOUR tree with channel chrome (the local Chrome) headless, no browser download, 127.0.0.1 only, never bundled Chromium; landed on the dashboard (not the wizard); Chart.js loaded from vendor/, painted canvases; an SRI tamper copy is refused; every caption says "local run of <sha>, open mode — NOT the demo"; a7 AUTH ENFORCED — the vendored path is outside STATIC_ASSET_PREFIXES: a session seeded BEFORE boot, with and without the cookie, or NOT RUN named; a8 C-182's Measure FIRST (does any jsdom harness execute the same-origin script); a9 mutants incl. your own M-swap (file, record and attribute replaced together: predicted no cell red); a10 C-68 with the vendored file proven IN each walker's population; a12 prior work. RD-424 round 2: b0 RED-AT-PARENT first — the head's cells against round 1's product a63d862: D1, D2, D3, D5 red and D4 x6 green; D5 RE-MEASURED because N disclosed its own slip (at 15568c9 D5 asserted toBeUndefined where getSetting returns null, so that red is VOID): D5's failing assertion must be its cost_centers line, never the getSetting line; b2 the shapes at EVERY freeze site (startup backup, writeFile pre and post, restoreFromBackupsIfNeeded, initializeFiles): one named store only; FREEZE_ALL for an absent, non-array or empty ledger, an untraceable entry, and 'purging'; restore fail-CLOSED and rotation fail-OPEN on an unreadable record; b3 EVERY ledger label shape M0's purge writes driven through _storeOfLedgerLabel — never the WRONG store; b4 r8 ON A REAL loopback SERVER on MT1 (symlink and hard link, five writes, tear, boot reads W5, not empty); b5 R-1 kept — no copy of a named store's pre-erasure needle anywhere; b6 mutants M-all, M-none, M-label, M-skip plus your own; b7 kept; b8 D-P1; b9 D-F1/D-F3 status only; b10 C-68 (every jsonStorage requirer); b11 prior work. If the SLOT joins: c0 RED-AT-PARENT; c1 THE f4 LADDER — reproduce gate 12's quadratic timing at 7d853b0 (8.06/32.2/129.3/2009 ms at n=4k/8k/16k/64k) and show it FLAT at the new head, with an n-DOUBLING CONTROL beside the timer's noise floor; c2-c8. Cross cells y1-y6 on MT1.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class. RD-424's (and the SLOT's) is an ADDENDUM.

THE MERGED TREE — part of every verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff RD-719 (MTa), RD-424 (MT1) (and the SLOT, MT2, only if it joins). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1 on node_modules proven for M0's lock: predicted 4273/262, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0; any missing id is a STOP. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes the lock or package.json, so there is NO npm registry exception in this gate. ONE lock is in play for both members and every merged tree (M0's e9063d4); the SLOT, if it joins, carries a second (9064763). For each lock ONCE: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline; an ENOTCACHED is NOT RUN for that lock (name it, mail a QUESTION) — never go online, never npm install, never npx playwright install. sqlite3's binding: Tuesday ruled (04:55Z, to gate 14, carried here) that the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in each lock's tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on this binding is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from one of your proven trees; never from gate 14's (live) or gates 12/13's trees.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only, each on node_modules PROVEN for its own lock. Predicted 7861a06 4240/257, cca852c 4265/260, MT1 4273/262 (SLOT 4160/250, MT2 4300/265). Every builder verify ran on a working tree before its commit or on a pre-counts commit with --update-counts; yours decides. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker; the same scan covers a7's seeded session token. H-2: seed BEFORE boot; RD-424's "boot" is a construction in a NEW process — declare it per row. H-3: a LANDING CONTROL for every plant, planted ledger, link, torn store, mutant, route abort or seeded session. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd. H-15: preloads with -r in argv; no exception this batch. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and lock waits have run 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly under the SAME tag if not granted. H-29: gate 14 is live; its evidence is method only. H-31: offline node_modules and the cached sqlite3 prebuild. H-32: the tier-1 image leg is a manifest evaluation, NO image built; the browser leg is Playwright with the local Chrome, headless, loopback only, offline, no download, captioned as a local run. H-33: plants, links, servers and Chrome counted and reaped or quarantined, never rm. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch15.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gate 14's trees and report dir are a live PEER gate's — never touch them; copy instruments BY COPY from gate 13's evidence/inst (its HOLD13.sh hard-codes its own evidence dir and its qa-floorlib13.sh carries stale ROOT and NEG defaults: re-point and correct your copies). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, red, shots or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry, no browser download. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gate 14 (QA/NexusAI-batch14, tags qa-b14-) — a PEER gate: FIFO, never touched — and the four builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, plain-node rows, census greps, the browser leg); then file your holds tagged qa-b15-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG); once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; your own browser-leg and r8 servers must classify OURS; record the foreign count beside every result; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, server boot, request, browser step, node driver and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the member branches, the SLOT's branch and main — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be b7bb1e9 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch15. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch15] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch15/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 15
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-719 @ 7861a06 with the red at base, sha384 against the 8eb94ce pin, identity to the official release said as unproven offline unless R-NET ran, the licence banners and text, the CSP, the image leg as a manifest evaluation, NO image built, the browser leg as a local run of 7861a06, offline — NOT the demo, and M-swap; RD-424 round 2 @ cca852c with the red at round 1's product, D5's line, r8 on a real server, needle copies, the shapes per site and the ledger labels; the SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured, the C-57 result, any combined blob, which rows ran on Opus 4.8 (or none), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR)". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A7, L-B1 to L-B5 (L-C1 to L-C6 if the slot joins) and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-02, C-12, C-164 with its ADDENDA, C-182 with its ADDENDUM, C-185 with its ADDENDA, C-190 and C-192 are the clarifications this batch leans on; C-17, C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141 with ADDENDUM 5, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Docker image build or image diff (the tier-1 image leg is a manifest evaluation), byte-identity of the vendored Chart.js to the official 3.9.1 release beyond the sha384 the root commit pinned (no network), the demo (behind RD-76 SSO), any deployed environment, any browser but local Chrome headless via Playwright against a local run, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped; sqlite3's binding from its cached prebuild), and Windows.
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
for S in "$MAIN_SHA" "$M_CF" "$M685" "$M692" "$M1904" "$ROOT8" "$A_HEAD" "$A_RED" "$B_HEAD" "$B_FIX" "$B_RED" "$B_MRG" "$B_R1" "$C_R1" "$C618"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: each member's own base with main; the bases are on main; the SLOT's stack is NOT on main.
for S in "$M_CF" "$M685" "$M692" "$M1904" "$ROOT8"; do
  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not an ancestor of b7bb1e9 — re-brief" >&2; exit 7; }
done
[ "$(g merge-base "$A_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$M692" ] || { echo "REFUSING: merge-base(RD-719, b7bb1e9) is not 3b6c9ec — re-brief" >&2; exit 7; }
[ "$(g merge-base "$B_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$M685" ] || { echo "REFUSING: merge-base(RD-424, b7bb1e9) is not d4386e7 — re-brief" >&2; exit 7; }
if g merge-base --is-ancestor "$C618" "$MAIN_SHA" 2>/dev/null; then echo "NOTE: RD-618 874c4f5 is now ON main — the brief's c6 / L-C4 premise (the SLOT brings RD-618 with it) is stale" >&2; fi

# 8 — chains exact.
[ "$(g log --format='%H %P' "${M692}..${A_HEAD}" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$A_HEAD $A_RED $A_RED $M692" ] \
  || { echo "REFUSING: 3b6c9ec..RD-719 is not exactly 0cb584d -> 7861a06" >&2; exit 8; }
[ "$(g rev-parse "${B_HEAD}^1" 2>/dev/null)" = "$B_FIX" ] && [ -z "$(g rev-parse --verify -q "${B_HEAD}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${B_FIX}^1" 2>/dev/null)" = "$B_RED" ] && [ -z "$(g rev-parse --verify -q "${B_FIX}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${B_RED}^1" 2>/dev/null)" = "$B_MRG" ] && [ -z "$(g rev-parse --verify -q "${B_RED}^2" 2>/dev/null)" ] \
  && [ "$(g rev-parse "${B_MRG}^1" 2>/dev/null)" = "$B_R1" ] && [ "$(g rev-parse "${B_MRG}^2" 2>/dev/null)" = "$M685" ] \
  || { echo "REFUSING: RD-424 is not cca852c -> ef1c1ed -> 15568c9 -> 08655ee (merge of 2ce26eb + d4386e7)" >&2; exit 8; }
g merge-base --is-ancestor "$C_R1" "$C618" 2>/dev/null && { echo "REFUSING: the SLOT's stack is inverted (7d853b0 under 874c4f5)" >&2; exit 8; }
g merge-base --is-ancestor "$C618" "$C_R1" 2>/dev/null || { echo "REFUSING: RD-735 round 1 7d853b0 is not stacked on RD-618 874c4f5" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the two member branches exactly the pins (REFUSE); main and the SLOT's branch read.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
C_NOW="$(ref_now "$C_BRANCH")"
# 18b — main MAY move (ruling b). It must be b7bb1e9 or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from b7bb1e9 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$VEN" "$IDX" "$R719" "$REC" "$JS" "$R424" "$DF2" "$G1" "$G2" "$G3" "$G4" "$G5" "$PKG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved b7bb1e9..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$LOCK" "$SRV" "$DE" "$CDF" "$DKF" "$DIG" "$TS" "$R465" "$R549" "$R204" "$R490" "$DOMJS" "$CSPR" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the C-68 sets and node_modules proofs run on M0's blobs (brief ruling b)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from b7bb1e9; gate 14's members may have landed) — the gate re-pins M0 itself and re-bases every prediction" >&2
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$M692" "$A_HEAD" "$A_EXPECTED_FILES" "RD-719 (3b6c9ec..7861a06)"
chk_delta "$M685" "$B_HEAD" "$B_EXPECTED_FILES" "RD-424 (d4386e7..cca852c)"
chk_delta "$B_MRG" "$B_HEAD" "$B_OWN_EXPECTED_FILES" "RD-424 round 2's own (08655ee..cca852c)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$M692" "$A_HEAD" "$VEN")" = "13 0" ] && [ "$(ns "$M692" "$A_HEAD" "$IDX")" = "1 1" ] && [ "$(ns "$M692" "$A_HEAD" "$R719")" = "101 0" ] && [ "$(ns "$M692" "$A_HEAD" "$REC")" = "11 0" ] \
  || { echo "REFUSING: RD-719's numstats are not vendored +13, index.html +1/-1, rd719 +101, record +11" >&2; exit 22; }
[ "$(ns "$B_MRG" "$B_HEAD" "$JS")" = "129 10" ] && [ "$(ns "$B_MRG" "$B_HEAD" "$R424")" = "14 6" ] && [ "$(ns "$B_MRG" "$B_HEAD" "$DF2")" = "254 0" ] && [ "$(ns "$M685" "$B_HEAD" "$JS")" = "151 9" ] \
  || { echo "REFUSING: RD-424's numstats are not jsonStorage +129/-10 (own) / +151/-9 (over d4386e7), rd424 +14/-6, df2 +254" >&2; exit 22; }
# 22b — ruling (m): no member touches the lock or package.json; product paths as commissioned.
for PAIR in "$M692 $A_HEAD" "$M685 $B_HEAD"; do
  [ -z "$(g diff --name-only "${PAIR% *}" "${PAIR#* }" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${PAIR#* } changes package-lock.json/package.json — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
[ -z "$(g diff --name-only "$M692" "$A_HEAD" -- backend docs Dockerfile .dockerignore .github 2>/dev/null)" ] || { echo "REFUSING: RD-719 touches backend/docs/image paths (commissioned: static/ + tests only; CSP unchanged)" >&2; exit 22; }
[ "$(g diff --name-only "$M685" "$B_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" = "$JS" ] || { echo "REFUSING: RD-424 touches a product path beyond $JS" >&2; exit 22; }

# 93 — RD-719's premises at source: the identity pin, the banners, the page, the CSP, the cells.
[ "$(blob "$A_HEAD" "$VEN")" = "$VEN_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$VEN")" ] && [ -z "$(blob "$A_RED" "$VEN")" ] \
  && [ "$(blob "$M692" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$A_RED" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$A_HEAD" "$IDX")" = "$IDX_A_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$R719")" = "$R719_BLOB" ] && [ "$(blob "$A_RED" "$R719")" = "$R719_BLOB" ] && [ "$(blob "$A_HEAD" "$REC")" = "$REC_BLOB" ] && [ -z "$(blob "$A_RED" "$REC")" ] \
  || { echo "REFUSING: RD-719's blobs are not vendored 8f69759 / index.html 25b7bd8 -> 7bf527d / rd719 fe52ff5 (also at 0cb584d) / record 0278e92" >&2; exit 93; }
VEN_384="sha384-$(g show "${A_HEAD}:${VEN}" 2>/dev/null | openssl dgst -sha384 -binary | openssl base64 -A)"
VEN_256="$(g show "${A_HEAD}:${VEN}" 2>/dev/null | shasum -a 256 | cut -d' ' -f1)"
[ "$VEN_384" = "$SHA384" ] && [ "$VEN_256" = "$VEN_SHA256" ] && [ "$(g cat-file -s "${A_HEAD}:${VEN}" 2>/dev/null)" = "199560" ] \
  || { echo "REFUSING: the vendored file's sha384/sha256/size are not the briefed values (a2's premise)" >&2; exit 93; }
[ "$(cnt "$ROOT8" "$IDX" "integrity=\"$SHA384\"")" = "1" ] && [ "$(cnt "$MAIN_SHA" "$IDX" "integrity=\"$SHA384\"")" = "1" ] && [ "$(cnt "$A_HEAD" "$IDX" "<script src=\"vendor/chart-3.9.1.min.js\" integrity=\"$SHA384\" crossorigin=\"anonymous\"></script>")" = "1" ] \
  || { echo "REFUSING: the integrity pin is not in index.html at the root commit 8eb94ce, M0 and RD-719's head as briefed (a2's premise)" >&2; exit 93; }
PIN_ORIGIN="$(g log --format=%H -S"$SHA384" "$MAIN_SHA" -- "$IDX" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')"
[ "$PIN_ORIGIN" = "$ROOT8" ] || { echo "REFUSING: git log -S of the sha384 pin on main is '$PIN_ORIGIN', not the root commit 8eb94ce alone (a2's premise)" >&2; exit 93; }
REC_CHK="$(g show "${A_HEAD}:${REC}" 2>/dev/null | python3 -c 'import json,sys; r=json.load(sys.stdin); print(r.get("sha384"), r.get("sha256"), r.get("bytes"))' 2>/dev/null)"
[ "$REC_CHK" = "$SHA384 $VEN_SHA256 199560" ] || { echo "REFUSING: the provenance record's sha384/sha256/bytes are not the vendored file's ('$REC_CHK')" >&2; exit 93; }
[ "$(g show "${A_HEAD}:${VEN}" 2>/dev/null | head -c 40 | grep -cF 'Chart.js v3.9.1')" = "1" ] && [ "$(cnt "$A_HEAD" "$VEN" 'Released under the MIT License')" = "2" ] && [ "$(cnt "$A_HEAD" "$VEN" '@kurkle/color v0.2.1')" = "1" ] \
  || { echo "REFUSING: the vendored file's banners are not Chart.js v3.9.1 + @kurkle/color v0.2.1, two MIT lines (a3's premise)" >&2; exit 93; }
for S in "$M692" "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(blob "$S" "$SRV")" = "$SRV_BLOB" ] || { echo "REFUSING: the server entry point at ${S:0:7} is not 0d7e387 (a4's 'CSP unchanged' premise)" >&2; exit 93; }
done
[ "$(cnt "$A_HEAD" "$SRV" "const STATIC_ASSET_PREFIXES = ['/static/', '/css/', '/js/', '/fonts/', '/img/'];")" = "1" ] && [ "$(cnt "$A_HEAD" "$SRV" '"https://cdn.jsdelivr.net"')" -ge 1 ] \
  || { echo "REFUSING: STATIC_ASSET_PREFIXES or the jsDelivr scriptSrc entry is not as briefed (a4/a7's premise)" >&2; exit 93; }
[ "$(g show "${A_HEAD}:${R719}" 2>/dev/null | grep -cE '^[[:space:]]+test\(')" = "4" ] && [ "$(cnt "$A_HEAD" "$R719" "fs.readdirSync(path.join(ROOT, 'static'))")" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$R719" "expect(sha384(VENDORED)).toBe(rec.sha384);")" = "1" ] \
  || { echo "REFUSING: rd719 is not four cells with V1 against the RECORD and a top-level static/ page list (a9's premise)" >&2; exit 93; }
[ "$(sblob "$A_HEAD" "$R204")" = "$R204_BLOB" ] && [ "$(blob "$A_HEAD" "$R204")" = "$(blob "$MAIN_SHA" "$R204")" ] || { echo "REFUSING: rd204-vendor-coverage moved (C-182: not touched)" >&2; exit 93; }
[ "$(cnt "$MAIN_SHA" "$DOMJS" "document.body.innerHTML = body.replace(/<script[\\s\\S]*?<\\/script>/gi, '');")" = "1" ] || echo "NOTE: helpers/dom.js no longer strips <script> as the brief READS (a8) — re-derive" >&2
if [ -d "$NPM_CACHE/index-v5" ] && grep -r -l -F -m1 -- 'chart.js/-/chart.js-3.9.1.tgz' "$NPM_CACHE/index-v5" >/dev/null 2>&1; then
  echo "NOTE: the local npm cache NOW holds chart.js-3.9.1.tgz — an offline reference for a2 exists (WRONG 3 is stale; the gate may use it, offline)" >&2; fi

# 94 — RD-424's premises at source: the scope functions at four sites, D5's slip, the ledger label producers on M0.
[ "$(blob "$M685" "$JS")" = "$JS_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$JS")" = "$JS_M_BLOB" ] && [ "$(blob "$B_R1" "$JS")" = "$JS_R1_BLOB" ] && [ "$(blob "$B_MRG" "$JS")" = "$JS_R1_BLOB" ] \
  && [ "$(blob "$B_RED" "$JS")" = "$JS_R1_BLOB" ] && [ "$(blob "$B_FIX" "$JS")" = "$JS_B_BLOB" ] && [ "$(blob "$B_HEAD" "$JS")" = "$JS_B_BLOB" ] \
  || { echo "REFUSING: jsonStorage.js is not 296e78f (M0) / a63d862 (round 1, 08655ee, 15568c9) / 2abb5cf (ef1c1ed, head)" >&2; exit 94; }
for T in '_erasureFreezeScope() {' '_erasureRestoreScope() {' '_storeFrozen(filePath, scope) {' '_storesNamedByLedger(record) {' '_storeOfLedgerLabel(label, dirs) {' \
         "if (status === 'purging') return JsonStorage.FREEZE_ALL;" 'return hits.length === 1 ? hits[0] : null;' 'return scope.has(path.basename(filePath));' \
         'const frozen = this._storeFrozen(filePath, this._erasureFreezeScope());'; do
  [ "$(cnt "$B_HEAD" "$JS" "$T")" = "1" ] || { echo "REFUSING: jsonStorage.js at cca852c lacks '$T' once (b2/b3's premise)" >&2; exit 94; }
done
[ "$(cnt "$MAIN_SHA" "$JS" '_erasureFreezeScope')" = "0" ] || { echo "REFUSING: M0's jsonStorage already carries _erasureFreezeScope" >&2; exit 94; }
[ "$(blob "$B_HEAD" "$DF2")" = "$DF2_BLOB" ] && [ "$(blob "$B_RED" "$DF2")" = "$DF2_RED_BLOB" ] \
  && [ "$(cnt "$B_RED" "$DF2" "expect(await booted.getSetting('orgName')).toBeUndefined();")" = "1" ] && [ "$(cnt "$B_HEAD" "$DF2" "expect(await booted.getSetting('orgName')).toBeNull();")" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$DF2" 'toBeUndefined')" = "0" ] && [ "$(g show "${B_HEAD}:${DF2}" 2>/dev/null | grep -cE '^[[:space:]]+test(\.each)?\(')" = "5" ] \
  || { echo "REFUSING: rd424-df2 is not 0826822 with D5 toBeNull (head) / b738075 with toBeUndefined (15568c9) and five test()/test.each blocks (b0's premise)" >&2; exit 94; }
[ "$(g show "${B_HEAD}:${DF2}" 2>/dev/null | sed -n '252p' | grep -cF "expect(readJson(path.join(dir, 'cost_centers.json'))).toEqual([{ id: 'cc-keep' }]);")" = "1" ] \
  || echo "NOTE: rd424-df2's line 252 at the head is no longer D5's cost_centers assertion — b0 quotes by text anyway" >&2
[ "$(diff <(titles "$B_R1" "$R424") <(titles "$B_HEAD" "$R424") >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: RD-424 round 2 changed an rd424-backup-after-write title" >&2; exit 94; }
for P in "$G1" "$G2" "$G3" "$G4" "$G5"; do
  [ "$(blob "$B_MRG" "$P")" = "$(blob "$B_HEAD" "$P")" ] || { echo "REFUSING: round 2 changed the C-164 granted file $P (b7's premise)" >&2; exit 94; }
done
for S in "$MAIN_SHA" "$B_HEAD"; do [ "$(blob "$S" "$DE")" = "$DE_BLOB" ] || { echo "REFUSING: dataErasure.js at ${S:0:7} is not 1f708e2 (b3's premise)" >&2; exit 94; }; done
[ "$(cnt "$MAIN_SHA" "$DE" 'failed.push({ file: `${label}/`, error: e.message });')" = "1" ] && [ "$(cnt "$MAIN_SHA" "$DE" 'failed.push({ file: `memory:${hook.name}`, error: e.message });')" = "1" ] \
  && [ "$(cnt "$MAIN_SHA" "$DE" 'failed.push({ file: childLabel, error: hardLinkRefusal });')" = "1" ] \
  || { echo "REFUSING: M0's dataErasure.js ledger producers (label/, memory:<hook>, the hard-link childLabel) are not as briefed (b3's premise)" >&2; exit 94; }
[ "$(blob "$MAIN_SHA" "$CDF")" = "$(blob "$B_HEAD" "$CDF")" ] || { echo "REFUSING: customerDataFiles.js differs between M0 and RD-424" >&2; exit 94; }
grep -qF 'ADDENDUM (PRIOR WORK)' "$READY_B" && grep -qF 'SLIP, disclosed' "$READY_B" || { echo "REFUSING: RD-424's READY file does not carry its PRIOR WORK ADDENDUM and the disclosed slip" >&2; exit 94; }

# 95 — the SLOT's standing premises (READ for both states): round 1's regex; origin's head now (NOTE).
[ "$(blob "$C_R1" "$CSPR")" = "$CSPR_R1_BLOB" ] && [ "$(cnt "$C_R1" "$CSPR" 'EDGE_C0_OR_SPACE')" -ge 1 ] || { echo "REFUSING: RD-735 round 1's cspReport.js is not 6608eae with EDGE_C0_OR_SPACE (c1's base premise)" >&2; exit 95; }
[ "$(blob "$C_R1" "$LOCK")" = "$LOCK_OLD_BLOB" ] || { echo "REFUSING: RD-735 round 1's lock is not 9064763" >&2; exit 95; }
[ -s "$B12_UNIT" ] && [ "$(shasum -a 256 "$B12_UNIT" 2>/dev/null | cut -d' ' -f1)" = "$B12_UNIT_SHA" ] || { echo "REFUSING: gate 12's qa-unit-b12.js (the f4 instrument) is absent or not 1f735ce1…7153" >&2; exit 95; }
grep -qF '8.06 / 32.2 / 129.3 / 2009 ms' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the f4 ladder the brief quotes" >&2; exit 95; }

# 98 — shared blobs: image inputs and test-server identical at M0 and both heads; the lock as briefed.
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] \
    || { echo "REFUSING: Dockerfile / .dockerignore / test-server at ${S:0:7} are not 12aab55 / 3e45ec5 / cff1e54 (a5's premise)" >&2; exit 98; }
done

# 23 — EXPECTED OVERLAPS by each member's own delta: the counts file only; and neither member touches what main changed since its base.
OVA="$(comm -12 <(g diff --name-only "$M692" "$A_HEAD" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort) <(g diff --name-only "$M685" "$B_HEAD" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort))"
[ -z "$OVA" ] || { echo "REFUSING: RD-719 and RD-424 share a path beyond the counts file: $OVA" >&2; exit 23; }
for PAIR in "$M692 $A_HEAD" "$M685 $B_HEAD"; do
  OVM="$(comm -12 <(g diff --name-only "${PAIR% *}" "$MAIN_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort) <(g diff --name-only "${PAIR% *}" "${PAIR#* }" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort))"
  [ -z "$OVM" ] || { echo "REFUSING: main changed a path ${PAIR#* } also changes since its base: $OVM — a COMBINED blob the brief does not predict" >&2; exit 23; }
done

# 35 — counts at every pinned sha; __tests__ census at M0 and the heads.
for PAIR in "$M692 4236 256" "$A_RED 4236 256" "$A_HEAD 4240 257" "$M_CF 4240 257" "$M685 4248 258" "$MAIN_SHA 4252 259" "$B_R1 4044 243" "$B_MRG 4248 258" "$B_RED 4248 258" \
            "$B_FIX 4265 260" "$B_HEAD 4265 260" "$M1904 4133 247" "$C618 4146 248" "$C_R1 4152 249"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$MAIN_SHA" "$A_RED" "$A_HEAD" "$B_HEAD"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "302 300 301 303 " ] || { echo "REFUSING: the __tests__ census (M0 0cb584d A B) is '$CENSUS', not '302 300 301 303'" >&2; exit 35; }

# 70 — package-lock: one blob for the members, exactly where the brief says; package.json identical.
for S in "$M692" "$M685" "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_M_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not e9063d4" >&2; exit 70; }; done
[ "$(blob "$B_R1" "$LOCK")" = "$LOCK_OLD_BLOB" ] || { echo "REFUSING: package-lock at round 1 2ce26eb is not 9064763 (the brief's lock map)" >&2; exit 70; }
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: package.json at ${S:0:7} is not cdb1168" >&2; exit 70; }; done
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_M_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not e9063d4 — another lock is in play; prove node_modules before any run (H-31)" >&2
# 70b — H-31's premise: the local npm cache and the sqlite3 prebuild (NOTEs only — the gate decides and names an ENOTCACHED).
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in axios/-/axios-1.20.0.tgz http-cache-semantics/-/http-cache-semantics-4.3.0.tgz sqlite3/-/sqlite3-5.1.7.tgz playwright/-/playwright-1.62 playwright-core/-/playwright-core-1.62; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(shasum -a 256 "$PREBUILD" 2>/dev/null | cut -d' ' -f1)"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
# 70c — ruling (n): Playwright 1.62.1 in M0's lock and a local Google Chrome (NOTEs only: the browser leg is NOT RUN, named, without them).
PWV="$(g show "${MAIN_SHA}:${LOCK}" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["packages"].get("node_modules/playwright",{}).get("version",""))' 2>/dev/null)"
[ "$PWV" = "1.62.1" ] || echo "NOTE: M0's lock carries playwright '${PWV:-none}', not 1.62.1 — ruling (n) names 1.62.1" >&2
[ -x "$CHROME_APP" ] || echo "NOTE: no local Google Chrome at $CHROME_APP — RD-719's browser leg (a6/a7/y6) will be NOT RUN" >&2

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean.
MT_PAIRS=0
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$A_HEAD $B_HEAD"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — builder evidence, prior reports, gate 13's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$CLAR" "$PREV_B3" "$BRIEF_B3" "$BRIEF14" "$B12_REPORT" "$B12_UNIT" "$B12_DIR/evidence/unit-b-HEAD.txt" "$B12_DIR/evidence/unit-b-PB.txt" "$C133" "$SQLITE_RULING" \
         "$EV_P/rd719-hold.log" "$EV_P/rd719-hold.sh" "$EV_P/rd719-shots/run2.log" "$EV_P/rd719-shots/shots.js" "$EV_P/rd719-vendor/chart.min.js" \
         "$EV_N/rd424-df2-red.out" "$EV_N/rd424-df2-green.out" "$EV_N/rd424-cq-harden.out" "$EV_N/rd424-cq-harden.sh" "$EV_N/rd424-r5-base.out" "$EV_N/set-rd424-df2.lst" \
         "$NX/session-tools/nexusai-lock.sh" \
         "$B13_INST/HOLD13.sh" "$B13_INST/qa-holdlib13.sh" "$B13_INST/qa-floorlib13.sh" "$B13_INST/qa-floorcount.py" "$B13_INST/qa-to.sh" "$B13_INST/qa-jestwrap.sh" "$B13_INST/qa-jsum.js" \
         "$B13_INST/qa-runj13.sh" "$B13_INST/qa-mut13.py" "$B13_INST/qa-mutlib13.sh" "$B13_INST/qa-merge13.sh" "$B13_INST/qa-mt13.sh" "$B13_INST/qa-pin13.sh" "$B13_INST/qa-build13.sh" \
         "$B13_INST/qa-h1-selftest13.sh" "$B13_INST/qa-h1-scan.py" "$B13_INST/qa-mail.py" "$B13_INST/qa-mailread.py" "$B13_INST/qa-lockcheck.py" "$B13_INST/qa-ssprint.sh" \
         "$B13_INST/qa-netbelt.sb" "$B13_INST/qa-netbelt-nodns.sb" "$B13_INST/qa-netbelt-ctl.js" "$B13_INST/qa-blobcensus13.py" "$B13_INST/qa-titles13.py" "$B13_INST/qa-lost13.py" \
         "$B13_INST/qa-c57-id-superset.sh" "$B13_INST/qa-c68census.py" "$B13_INST/qa-cov-setup.js" "$B13_INST/qa-b7tok.js" "$B13_INST/qa-chrome-ctl.js" "$B13_INST/qa-c3.js" "$B13_INST/qa-boot13.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" || { echo "REFUSING: a READY does not name its head" >&2; exit 31; }
[ "$(shasum -a 256 "$EV_P/rd719-vendor/chart.min.js" 2>/dev/null | cut -d' ' -f1)" = "$VEN_SHA256" ] || { echo "REFUSING: the builder's fetch copy is not the vendored file's sha256 (a2's RELAYED source)" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4240/4240 tests passed across 257 suites (jest exit 0)' "$EV_P/rd719-hold.log" && grep -qF 'Tests:       4 failed, 4 total' "$EV_P/rd719-hold.log" \
  && grep -qF 'Tests:       66 passed, 66 total' "$EV_P/rd719-hold.log" && grep -qF 'RED at the head (cells only' "$EV_P/rd719-hold.log" && ! grep -qF '=== HEAD ' "$EV_P/rd719-hold.log" \
  && grep -qF '"paintedCanvases":4,"chartSrc":["vendor/chart-3.9.1.min.js"],"blockedHosts":["cdn.jsdelivr.net"]' "$EV_P/rd719-shots/run2.log" \
  && grep -qF 'browser = await chromium.launch(); }' "$EV_P/rd719-shots/shots.js" \
  && grep -qF '=== HEAD 08655ee' "$EV_N/rd424-df2-red.out" && grep -qF 'Tests:       4 failed, 12 passed, 16 total' "$EV_N/rd424-df2-red.out" \
  && grep -qF 'VERDICT: PASS — 4265/4265 tests passed across 260 suites (jest exit 0)' "$EV_N/rd424-df2-green.out" && grep -qF 'Tests:       458 passed, 458 total' "$EV_N/rd424-df2-green.out" \
  && grep -qF 'fixed sha 74a0283f787baf61' "$EV_N/rd424-df2-green.out" && grep -qF '> 252 |' "$EV_N/rd424-cq-harden.out" && grep -qF 'R5 must stay red' "$EV_N/rd424-cq-harden.out" \
  && grep -qF 'Tests:       6 passed, 6 total' "$EV_N/rd424-cq-harden.out" && grep -qF 'Tests:       5 failed, 1 passed, 6 total' "$EV_N/rd424-r5-base.out" \
  && grep -qF '2009.011ms' "$B12_DIR/evidence/unit-b-HEAD.txt" \
  || { echo "REFUSING: a builder log or prior evidence no longer carries the line the brief quotes (WRONG 7-10's premise)" >&2; exit 31; }
[ "$(grep -c . "$EV_N/set-rd424-df2.lst")" = "31" ] && [ "$(grep -c '^#' "$EV_N/set-rd424-df2.lst")" = "1" ] || echo "NOTE: set-rd424-df2.lst is no longer 30 paths + 1 comment (WRONG 11)" >&2
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" && grep -qF 'File **one focused hold at a time** (≤~40 min of jest)' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE the brief quotes (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-32659\}' "$B13_INST/qa-floorlib13.sh" || echo "NOTE: gate 13's qa-floorlib13.sh ROOT default is no longer 32659 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF14" || echo "NOTE: gate 14's brief does not read as stamped by Tuesday — the brief calls it the stamped base" >&2
grep -qF 'D-F2' "$PREV_B3" && grep -qF 'GO WITH FINDINGS' "$PREV_B3" || { echo "REFUSING: the batch-3 report does not carry RD-424's D-F2 / verdict the brief quotes" >&2; exit 31; }

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
for P in "$PREV_B3" "$BRIEF_B3" "$BRIEF14" "$B12_REPORT" "$READY_A" "$READY_B" "$B13_INST/"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-719 and RD-424 round 2 are TIER 1.' 'RD-735 round 2 (SLOT) is TIER 2' 'NO docker, NO image build' 'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' \
         'IS PART OF H-31' 'THE BROWSER DRIVER'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-719 (TIER 1, vendored third-party code' 'RD-424 round 2 (TIER 1, data-erasure safety' 'RD-735 round 2 (TIER 2' 'one verdict per ticket' 'manifest evaluation, NO image built' 'NOT the demo'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$MAIN_SHA" "$M685" "$M692" "$A_RED" "$B_FIX" "$B_RED" "$B_MRG" "$B_R1" "$C_R1" "$C618"; do
  grep -qF -- "$S" "$BRIEF" || grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$M_CF" "$M1904" "$ROOT8" "$LOCK_M_BLOB" "$LOCK_OLD_BLOB" "$PKG_BLOB" "$VEN_BLOB" "$IDX_M_BLOB" "$IDX_A_BLOB" "$R719_BLOB" "$REC_BLOB" "$SRV_BLOB" "$JS_M_BLOB" "$JS_R1_BLOB" "$JS_B_BLOB" \
         "$DF2_BLOB" "$DF2_RED_BLOB" "$DE_BLOB" "$CSPR_R1_BLOB" "$DKF_BLOB" "$DIG_BLOB" "$TS_BLOB" "$R204_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 15' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 15 has no priority member" >&2; exit 15; fi
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

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; READY lines verbatim; clarification quotes.
WORDS="RD-719 RD-424 RD-735 RD-721 RD-618 RD-733 C-02 C-12 C-17 C-49 C-57 C-68 C-89 C-102 C-104 C-112 C-115 C-125 C-141 ADDENDUM%5 C-164 C-174 C-182 C-185 C-186 C-190 C-192
RED-AT-PARENT a0 a2 a3 a4 a5 a6 a7 a8 a9 a10 a12 b0 b2 b3 b4 b5 b6 b10 b11 c0 c1 y1 y2 MTa MT1 MT2 M0 D-F2 D5 toBeUndefined cost_centers FREEZE_ALL _storeOfLedgerLabel purging W5 M-all M-none M-label M-skip M-swap
L-A1 L-A7 L-B1 L-B5 L-C1 L-C6 L-Y1 H-1 H-2 H-3 H-9 H-15 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
4273/262 4256/260 4300/265 4240/257 4265/260 4160/250 8eb94ce sha384 @kurkle/color STATIC_ASSET_PREFIXES R-NET EDGE_C0_OR_SPACE n-DOUBLING%CONTROL 8.06/32.2/129.3/2009 manifest%evaluation NO%image%built
Playwright%1.62.1 channel%chrome headless no%browser%download 127.0.0.1 OFFLINE SRI _prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline e9063d4 9064763
exits%71 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request missing%0 new%ids%21 stale-parent STOP JOINS ADDENDUM%SLOT
POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b15- qa-b14- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --after UNCHANGED%tag DEADLINE HEARTBEAT PEER%gate
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child
Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center batch-3 gate%12 gate%14 npm%install --offline ENOTCACHED HOLD13.sh qa-floorlib13.sh Never%rm datasecau/Reporting_Dashboard_Au"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. THE MERGED TREE' '^## 8. CI' \
         '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOT' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^### TARGET C' \
         '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-B1 L-B2 L-B3 L-B4 L-B5 L-C1 L-C2 L-C3 L-C4 L-C5 L-C6 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 c0 c1 c2 c3 c4 c5 c6 c7 c8 y1 y2 y3 y4 y5 y6; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
# every builder's stated limits / design / scope lines carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|The demo image (RD-76); the built Docker image (I did not build it; "static/ ships wholesale" is from the Dockerfile and .dockerignore, read, not a built-image listing).
A|Offline, the page is still unstyled and 4 console errors remain on the branch: the other CDN libraries (Bootstrap, Bootstrap Icons, Font Awesome, PapaParse), which is RD-721's scope, sequenced after this gate.
A|Viewports other than 1366x900; dark mode not captured (the change is a script URL; no CSS).
A|NOT changed: CSP (scriptSrc already allows 'self'; the CDN hosts stay for RD-721's libraries), static/js/index.js, any other page.
B|Design choices for your veto: (1) the full freeze for an empty ledger and for any untraceable entry; (2) 'purging' stays a full freeze (the ruling names purged_incomplete only).
B|NOT IN SCOPE: D-F1 (RD-747, a clearing write reverted), D-F3 (on RD-420), C-F1 (RD-744).
B|SLIP, disclosed: D5 first asserted getSetting(...) toBeUndefined; getSetting answers null.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A local run serves every page and API with no sign-in.
Shipped documents carry no internal identifiers or named individuals.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
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
Five test files are granted to lane 2 for RD-424 only
covers ONLY the stores, and their recovery copies, named in the erasure's FAILED ledger.
No positive evidence, no narrowing.
stays a FULL freeze.
Whether the code does all this is the gate's question (gate 15, tier 1, with RD-719).
The gate includes a real image diff.
starts EXECUTING a same-origin script it used to skip as a CDN URL
NOTHING starts until RD-719's gate (batch 15) returns GO
Never unify silently: a version change is a visual change.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b15-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' 'PEER gate' 'UNCHANGED tag'; do
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

# 81 — this batch's own premises (and the carried lessons) are in the brief.
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4273/262' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' '9064763' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' 'shippedFiles' \
         '8eb94ce' 'sha384' 'R-NET' '@kurkle/color' 'STATIC_ASSET_PREFIXES' 'M-swap' 'scriptSrc' 'SRI' "channel: 'chrome'" 'ms-playwright' 'Playwright 1.62.1' 'bundled Chromium' \
         'D5' 'toBeUndefined' 'FREEZE_ALL' '_storeOfLedgerLabel' 'r8' 'W5' 'purging' 'M-all' 'M-none' 'M-label' 'M-skip' 'memory:<hook>' 'cost_centers' \
         'EDGE_C0_OR_SPACE' '2009' 'n-DOUBLING CONTROL' 'b7bb1e9' 'ANY rd465 O-1 failure' 'ADDENDUM SLOT' 'RD-735 SLOT' 'WRONG 1' 'WRONG 2' 'WRONG 3' 'WRONG 4' \
         'qa-floorlib13.sh' 'HOLD13.sh' 'ADDENDUM 5' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the RD-735 ADDENDUM SLOT: EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
C_JOINS="$(grep -E '^ADDENDUM RD-735 JOINS @ [0-9a-f]{40} \| READY /' "$BRIEF" 2>/dev/null)"
C_EMPTY="$(grep -c '^RD-735 SLOT: EMPTY$' "$BRIEF" 2>/dev/null)"
C_STATE=''
SLOT_DESC=''
if [ -n "$C_JOINS" ]; then
  [ "$(printf '%s\n' "$C_JOINS" | grep -c .)" = "1" ] && [ "$C_EMPTY" = "0" ] || { echo "REFUSING: the RD-735 ADDENDUM SLOT has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  C_SHA="$(printf '%s\n' "$C_JOINS" | sed -E 's/^ADDENDUM RD-735 JOINS @ ([0-9a-f]{40}) .*/\1/')"
  C_READY="$(printf '%s\n' "$C_JOINS" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  [ "$C_NOW" = "$C_SHA" ] || { echo "REFUSING: the RD-735 ADDENDUM names $C_SHA but origin $C_BRANCH is '${C_NOW:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$C_SHA" 2>&1)" = "commit" ] || { echo "REFUSING: RD-735 $C_SHA is not in the object store (89)" >&2; exit 89; }
  [ -s "$C_READY" ] && grep -qF "${C_SHA:0:7}" "$C_READY" || { echo "REFUSING: RD-735's READY '$C_READY' is absent or does not name ${C_SHA:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$C_SHA" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: RD-735 ${C_SHA:0:7} is already on main (89)" >&2; exit 89; fi
  g merge-base --is-ancestor "$C_R1" "$C_SHA" 2>/dev/null || { echo "REFUSING: RD-735 ${C_SHA:0:7} does not descend from round 1 7d853b0 (never rebased?) (89)" >&2; exit 89; }
  CGOT="$(g diff --name-only "$C_R1" "$C_SHA" 2>/dev/null | sort)"
  [ "$CGOT" = "$(sorted "$C_EXPECTED_FILES")" ] || { echo "REFUSING: RD-735's delta over 7d853b0 is not cspReport.js + the r2 cell file + counts. Got: $(printf '%s ' $CGOT) (89)" >&2; exit 89; }
  [ "$(cnt "$C_SHA" "$CSPR" 'EDGE_C0_OR_SPACE')" = "0" ] && [ "$(cnt "$C_SHA" "$CSPR" 'function urlTrim(value) {')" = "1" ] || { echo "REFUSING: RD-735's cspReport.js still carries EDGE_C0_OR_SPACE or lacks urlTrim (89)" >&2; exit 89; }
  [ "$(blob "$C_SHA" "$LOCK")" = "$LOCK_OLD_BLOB" ] || echo "NOTE: RD-735 ${C_SHA:0:7}'s lock is not 9064763 — prove its node_modules (H-31)" >&2
  for X in "$M_ORIGIN" "$A_HEAD" "$B_HEAD"; do
    RC="$(conflicts "$X" "$C_SHA" | tr '\n' ' ' | sed 's/ $//')"
    [ -z "$RC" ] || [ "$RC" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x RD-735 conflicts beyond the counts file: '$RC' (89)" >&2; exit 89; }
    MT_PAIRS=$((MT_PAIRS + 1))
  done
  C_STATE="RD-735 round 2 JOINS this gate per the brief's ADDENDUM SLOT, at $C_SHA (origin $C_BRANCH, re-pinned by the launcher), READY $C_READY — gate it by the brief's section 2a C rows (c0-c8), section 6 and limits L-C1 to L-C6; merge it LAST (step c, MT2); it brings RD-618 874c4f503d0f37a032014e562972b17e903e1072 with it (c6)."
  SLOT_DESC="JOINS @ ${C_SHA:0:7}"
else
  [ "$C_EMPTY" = "1" ] || { echo "REFUSING: the RD-735 ADDENDUM SLOT is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
  C_STATE="RD-735 round 2 is NOT a member of this gate (the brief's ADDENDUM SLOT is EMPTY): do not gate it; say so in the report."
  SLOT_DESC="EMPTY"
  if [ -n "$C_NOW" ] && [ "$C_NOW" != "$C_R1" ]; then
    RDY_NOTE='no READY on disk names it'
    [ -s "$READY_C_SEEN" ] && grep -qF "${C_NOW:0:7}" "$READY_C_SEEN" && RDY_NOTE="its READY is on disk ($READY_C_SEEN)"
    echo "NOTE: the RD-735 SLOT is EMPTY but origin $C_BRANCH is ${C_NOW:0:7} (round 2) and $RDY_NOTE — Tuesday folds it in at stamp or leaves it out (brief WRONG 1)" >&2
  fi
fi

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  BQ="$(grep -l 'qa-b14-' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate (qa-b14-) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell. REFUSES when any of the five is missing.
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
NEG_SEATS=''; NEG_DESC=''
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P tuesday; do   # the coordinator pane is named 'tuesday' on this seat (gate 14's launcher fix, s97, 2026-10-05)
  PP="$(pane_pid_of "$NAME")"
  [ "$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named '$NAME', found: '${PP:-none}' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
done
NEG_SEATS="${NEG_SEATS# }"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "5" ] || { echo "REFUSING: the five derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
for PEER in "$ROUTE_NAME14"; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
  else
    echo "NOTE: no live claude under a pane named $PEER — that peer gate finished or its pane is gone" >&2
  fi
done

# 86 — no live gate-15 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 15 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 22b 93 94 95 98 23 35 70 70b 70c 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-719 $A_HEAD · RD-424 $B_HEAD · SLOT RD-735: $SLOT_DESC (origin ${C_NOW:0:7})" >&2
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
  echo "  main ${M_ORIGIN:0:7} (b7bb1e9 or a descendant; no member path moved) (18b)"
  echo "  merge-bases (7); chains (8); deltas + no lock change (22, 22b); premises (93 94 95 98)"
  echo "  overlaps (23); counts + census (35); lock + npm cache + sqlite3 prebuild + browser (70, 70b, 70c); $MT_PAIRS three-argument merge-trees counts-only or clean (80, 89); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); RD-735 SLOT $SLOT_DESC (89); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/main = $M_ORIGIN (b7bb1e9 or a descendant; no member path moved since b7bb1e9); refs/heads/$C_BRANCH = ${C_NOW:-absent}. $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOT: $C_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
