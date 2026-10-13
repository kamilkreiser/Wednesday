#!/bin/bash
# launch_qa_nexusai_gate_batch22.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 22"), THREE members (+ TWO generic ADDENDUM SLOTS),
# one verdict per ticket, ONE report (drafted 2026-10-13 ~11:15–~11:55 AEDT by a read-only drafting agent for Tuesday; the drafter ran only --check).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start. A TIERED gate (tier-1 cells run; tier-2 cells / full verifies may be NAMED NOT RUN, ruling o).
#   A — RD-838 (TIER 1; data destruction; ROUND 3 of the RD-640 class by Kam's ruling, C-213 — a NO GO returns to Tuesday, no round 4)
#       rd-838-erasure-chain-canonical-key-s94n @ 380bec3: ac3ca02 + 380bec3 on the forward merge 5bfdc93 (= RD-640 r2 b214f6f + main 08a81e2).
#       Lands ALL of RD-640: dataErasure 1f708e2 -> 26f7187 (+149/-22 over main). 4480/281. Red control: b214f6f (dataErasure 343348d).
#   B — RD-839 (TIER 1; anonymous admin route) rd-839-erasure-status-window-paths-s94n @ 057a69d: TWO commits on cc42c42. server.js c8ca2b3 -> b669e02. 4458/280.
#   C — RD-840 + RD-841 (TIER 2 + ONE browser leg) rd-840-841-sustainability-feedback-s96o @ 88bba37: THREE commits on 08a81e2. 4462/280.
#   THE CROSSES (C-68): A x B (B's route serves A's failure records); C x B (C's browser leg boots the entry point B changes).
#   SLOTS — S1, S2 (generic) join ONLY by the brief's JOINS lines (guard 89). EMPTY.
#   Main at drafting 944ca97 (RD-823; counts 4450/279; lock 19477a9). Predicted MTF 4503/283 (order B, A, C).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch22' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch22.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-22 drafting commission (2026-10-13). READY mails copied in briefs/. RD-838's round 3: Kam, live board 2026-10-13 09:46:48 AEDT,
# card nexusai-rd838-rd640-round3-1013 = a (C-213). RD-840+841: Kam, 09:46:43, card nexusai-sustainability-feedback-rd840-rd841-1013 = a.
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings: sqlite3 cached prebuild; full verifies UNBELTED with 4 conditions; npm_config_update_notifier=false on EVERY npm call; ruling (b) + its
# EXTENSION (gate 20's ruling (c), answer-starvation.txt) — lock-starved full verifies / tier-2 cell holds NAMED NOT RUN; the browser driver; C-190 + its
# ADDENDUM: BOTH CodeQL thresholds; C-209; C-141 ADDENDA 6/7: --replace for re-files, only a merge HOLD's tag says "merge" (gate tags are qa-b22-*);
# RULING (i)'s BY-HAND GATE YIELD IS RETIRED (gate 19's RELEASE item 5). The installed jest-lock tool is RD-821 r3 (sha256 3c33f5ae…, swapped after gate 21's GO).
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert, NEVER swaps the lock tool; no fix, no deploy, nothing to Partner Center/demo/prod/any human, no az, no docker, NO npm registry (H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch21.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the LIVE
# negative-control seat derivation 38R, the ADDENDUM-SLOT JOINS parser 89, route-line and stamp guards last). CHANGES, each deliberate:
#   - THREE members on THREE merge-bases (08a81e2, cc42c42, 08a81e2) and ONE lock (19477a9); a red-control tree b214f6f on e9063d4 (guard 98).
#   - 90: the RD-821 member is gone; the INSTALLED tool is now pinned at 3c33f5ae… (REFUSE if moved), the old fd223bd2… named as .pre-1012-o-r3.
#   - 80: the merge-tree reader runs awk under LC_ALL=C and REFUSES on a non-zero pipe status (gate 21's reader failed OPEN on rd-721's woff blobs: brief WRONG 18);
#         B is also merge-treed onto the four C-212 heads re-read by ls-remote (counts-only or clean, else REFUSE).
#   - 18b/23: backend/server.js moving on main is a NOTE (C-212 lets it auto-merge with B; guard 80 decides), not a member-only refusal.
#   - 38R: the coordinator pane may be named 'tuesday' OR 'wednesday' (as gate 21); every live 'QA/*' pane other than this gate's own joins as a peer negative control.
#   - 32: the T-rulings are 'RULED: @STAMP@' slots — the one stamp-placeholder check covers them.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); shasum / bash -n over session-tools files; python/grep over `git show` output; ls, ps, tmux list-panes, test -e.
# It writes nothing and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch22.sh [--check]
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
BRIEF="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF21="$BRIEFS/2026-10-12_nexusai-gate-batch21.md"
READY_A="$BRIEFS/2026-10-13_nexusai-rd838-READY-mail.txt"
READY_B="$BRIEFS/2026-10-13_nexusai-rd839-READY-mail.txt"
READY_C="$BRIEFS/2026-10-13_nexusai-rd840-841-READY-mail.txt"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
BROWSER_ANS="$STAGED/2026-10-04_qa_batch13_browser_driver_answer.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
G21_RELEASE="$STAGED/2026-10-12_nexusai_gate21_RELEASE.md"
N_PLAN="$STAGED/2026-10-13_nexusai_N_ANSWER_plan_rd838_rd839.md"
N_839READY="$STAGED/2026-10-13_nexusai_N_ANSWER_rd839_ready.md"
N_GO838="$STAGED/2026-10-13_nexusai_N_GO_rd838.md"
O_PLAN="$STAGED/2026-10-13_nexusai_O_ANSWER_plan_rd840_rd841.md"
O_BRIEF="$STAGED/2026-10-13_nexusai_O_BRIEF_rd840_rd841.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
LOCKQ="$ST/locks/queue-jest"
LOCKTOOL="$ST/nexusai-lock.sh"
LOCKOLD="$ST/nexusai-lock.sh.pre-1012-o-r3"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED after gate 21's GO — PINNED
LOCK_SHA_OLD='fd223bd2a72d38143d0466fcbcc6762f9bc7f82815084d1a3c53422acc2d7700'    # RD-821 round 2, kept as .pre-1012-o-r3
C57_RUNNER="$ST/c57-id-superset.sh"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$ST/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B21_DIR="$RPTS/2026-10-12-gate-batch21"
B21_REPORT="$B21_DIR/report.md"
B21_INST="$B21_DIR/evidence/inst"
B20_STARVE="$RPTS/2026-10-08-gate-batch20/evidence/answer-starvation.txt"
B19_DIR="$RPTS/2026-10-07-gate-batch19"
B19_BODY0="$B19_DIR/body-0.md"
B19_BODY1="$B19_DIR/body-1.md"
B19_INST="$B19_DIR/evidence/inst"
B19_MXA="$B19_DIR/evidence/matrix-A-head.jsonl"
B19_MXF="$B19_DIR/evidence/matrix-fixprobe.jsonl"
PREV_FLOORLIB="$B21_INST/qa-floorlib21.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-13-gate-batch22/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch22'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'

MAIN_SHA='944ca97fd384af55628c6669db522b734b2578e2'      # origin main at drafting (11:17:31 AEDT; RD-823 last)
MB_A='08a81e2af34044276e30af962fb4c9234fbc1a3c'          # merge-base(A, M0) = merge-base(C, M0) — RD-795's landing
MB_B='cc42c424c1b8bc0938a1201652acc94a531ee1cc'          # merge-base(B, M0) — RD-591's landing
MB_C="$MB_A"
A_R2='b214f6f063955f95606bf22e19afb7f076de1b4b'          # RD-640 round 2 (gate 19 NO GO) — A's red control
A_R1='588ec6311320eab91deca9bf9dbd0f4afed3a287'          # RD-640 round 1
A_MRG='5bfdc934bee3496d4f137a19f7a52c17e5f6eebf'         # A's forward merge (b214f6f + 08a81e2)
A_RED='ac3ca02f7f5fc98e93379ae36e0d53542bec24ba'         # A's red-first commit
B_RED='b0417d90856c8987f54ca85c55a7cdcdb9fee631'         # B's red-first commit
C_RED='b67542746b123bb60d5c50d63bca461eb236be9c'         # C's red-first commit
C_FIX='b2a9f19dbe0205570fc2b5b9bbda42a00cfe9ff1'         # C's change (88bba37 = counts only on it)
A_BRANCH='rd-838-erasure-chain-canonical-key-s94n'
A_HEAD="${QA_A_HEAD_OVERRIDE:-380bec32258337ef08eb7e8560077670b8c29264}"
B_BRANCH='rd-839-erasure-status-window-paths-s94n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-057a69d960d12ba090fea160ba8dfee4c70a0aa6}"
C_BRANCH='rd-840-841-sustainability-feedback-s96o'
C_HEAD="${QA_C_HEAD_OVERRIDE:-88bba375d836e2d2edca0046ad8db84818d8e818}"
R2_BRANCH='rd-640-eloop-and-tree-cells-s87n'
# C-212's four overlapping server.js heads (NOT members; re-read by ls-remote; B is merge-treed onto whatever they are now)
H212_BRANCHES='rd-721-icons-vendor-s91p rd-761-law-endpoint-policy-s89r rd-794-ollama-runtime-slice-s89r rd-819-ai-config-empty-body-s89r'
RD721_DRAFT='64ee3096c6ff81ac07d6292d61d062819458c3b5'    # rd-721 at drafting — holds the vendored Bootstrap Icons bytes T6 (a) serves
BI_CSS_BLOB='7d93a97888561db08eb7a166abad952824374186'
BI_WOFF2_BLOB='52b12533e4da87cb83e50039430cd027b48f931a'
BI_CSS_SHA='0695565c51d65e053ff5181928e607604feac73004726c67d27e8cca6bb120ec'
BI_WOFF2_SHA='eba8243051339456fed8f7767ae87a2b37199b83c21a6ea76c18254fa4959f66'

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
SV='backend/server.js'
DE='backend/dataErasure.js'
AUTH='backend/services/authEnforcement.js'
T640='__tests__/rd640-eloop-and-tree-cells.test.js'
TEV='__tests__/erasure-verdict-is-derived-from-failures.test.js'
T838='__tests__/rd838-chain-canonical-key-and-cap.test.js'
T839='__tests__/rd839-erasure-status-window-paths.test.js'
T840='__tests__/rd840-841-sustainability-feedback.test.js'
SUI='static/js/sustainability-ui.js'
SCSS='static/css/sustainability.css'
TOK='static/css/tokens.css'
DBT='scripts/derive-brand-tokens.js'
BMD='docs/BRAND.md'
E2E='tests/e2e/sustainability-layout.spec.js'
DARK='static/css/dark-mode.css'
IDXH='static/index.html'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
BTC='__tests__/brand-token-conformance.test.js'
DKF='Dockerfile'
DIG='.dockerignore'

DE_M_BLOB='1f708e276482e5224ab9793d878e59ed0867b125'      # M0, 08a81e2, cc42c42, B, C
DE_R2_BLOB='343348df5476a4d8a434c469c64253a8618e92cc'     # b214f6f, 5bfdc93, ac3ca02 (the red control)
DE_A_BLOB='26f718781fc3b6aa7ae4af7fa8130ff2e0365c30'
T640_BLOB='a8175604945a16e86ee04c18d26221c624dd1031'      # b214f6f = A
TEV_M_BLOB='4b75b241b3f039810f2e9ab5f6619f3b6da0928c'
TEV_A_BLOB='13c4d6356f39e687ec537a076a5df913818f040c'     # b214f6f = A
T838_BLOB='21bb3d9803e43d839a0cf0f7616e2f4130f6474d'
SV_M_BLOB='c8ca2b38d5bfddb795933bb152269d7c2f4490ae'      # M0, cc42c42, 08a81e2, A, C
SV_B_BLOB='b669e02601254f663d2c1431614456339fd74010'
T839_BLOB='ad0d44dab60cda851f9e653818db73e58f48d34d'
T840_BLOB='2da9ee388462696a3f8aac806b84b222b8d3d329'
SUI_M_BLOB='e2aaa46db070920bb28cffc89edb982d18989e69'; SUI_C_BLOB='99a721ea2080a18ec3a63bf94df456d66155bec8'
SCSS_M_BLOB='451c7c651f31d010559c8e2ab606820db2530fd3'; SCSS_C_BLOB='abc08fa0330326132d83bfa906c01423b4a0e12a'
TOK_M_BLOB='de6e0fe44aeaf107a0ed0b8bd966975016bb6aec'; TOK_C_BLOB='54f8f4088dfb3f230643185e3bd48e2f51ab367d'
DBT_M_BLOB='d94423a06beda02ff09074ad3641650439f7bf82'; DBT_C_BLOB='2741449971d7d559590984a712f335974c64145f'
BMD_M_BLOB='f61478156a54b5388f98128d70317d528e7b6155'; BMD_C_BLOB='75313b7f96118754cdc8d7d97b386b1921c694b7'
E2E_M_BLOB='3c8dbbf4f9320f1aaf5d17533ec54260a79bc29d'; E2E_C_BLOB='a8a6b6966a644e3acb9bbdc71736ed501f3f9325'
DARK_BLOB='e90297efa71f59c12e823277be5daaa8bc6f1fc4'
LOCK_NEW='19477a9329f17e529c208d91d172b95b47fc1bb5'        # M0, every member and base
LOCK_OLD='e9063d44757007324b8c55fa58c03c03dfe552ae'        # b214f6f only (proxy-addr 2.0.7)
PKG_NEW='384805d9e286718bb34ffd05be01c62c00806cf5'
PKG_OLD='cdb1168783a92179afe20be67b37976203b904f8'
TS_BLOB='bb45cd78c927d76e03a43ec29188d79e9d176b60'
TSH_BLOB='f612fb4815aaa358795acc977d59a0a9cba09670'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
R549_BLOB='1988b468dd596b3fb62c6aad865bc6609ffa99dd'
R465_BLOB='f16b811756f70ddcd37ec43197383c5434cff6e4'

A_EXPECTED_FILES="$DE
$T640
$TEV
$T838
$COUNTS_FILE"
A_OWN_EXPECTED_FILES="$DE
$T838
$COUNTS_FILE"
B_EXPECTED_FILES="$SV
$T839
$COUNTS_FILE"
C_EXPECTED_FILES="$SUI
$SCSS
$TOK
$DBT
$BMD
$T840
$E2E
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 22'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch22] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any member head (no member has a pull request), CodeQL at any member head (no PR), the erasure walk on Linux (its 40-link resolver; RD-838's Docker leg is relayed) or on a network filesystem, Windows-style paths in the erasure-status body beyond the shapes named, a real deployment's first-run window, the demo (behind RD-76 SSO) and its synthetic feed as deployed, any deployed environment, the Sustainability tab with Bootstrap's CDN stylesheet loaded (the browser leg is belted; Bootstrap Icons only from RD-721's vendored bytes if ruled), headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, off-host requests aborted), Kam's screenshot review (O's set, through Tuesday), real Azure, a real Docker image build (the shipped-blob legs are a manifest evaluation), Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
titles() { g show "${1}:${2}" 2>/dev/null | grep -E '^[[:space:]]*(test|it)(\.each\(.*\))?\(' | sed -E 's/^[[:space:]]+//'; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
lockver() { g cat-file -p "$1" 2>/dev/null | grep -A1 "\"node_modules/$2\": {" | grep -o '"version": "[^"]*"' | head -1 | cut -d'"' -f4; }
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
# awk runs under LC_ALL=C (a UTF-8 awk dies on binary blobs and prints NOTHING — brief WRONG 18); a non-zero pipe status is reported as MTFAIL, never as "clean".
conflicts() { local b out st
  b="$(g merge-base "$1" "$2" 2>/dev/null)" || { echo "MTFAIL(no-merge-base)"; return 1; }
  out="$(g merge-tree "$b" "$1" "$2" 2>/dev/null | LC_ALL=C awk '/^  (base|our|their) /{f=$4} /^\+<<<<<<</{c[f]=1} END{for(k in c) print k}'; echo "PIPE ${PIPESTATUS[0]} ${PIPESTATUS[1]}")"
  st="$(printf '%s\n' "$out" | tail -1)"
  [ "$st" = "PIPE 0 0" ] || { echo "MTFAIL($st)"; return 1; }
  printf '%s\n' "$out" | sed '$d' | sed '/^$/d' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 22", with THREE members and TWO generic ADDENDUM SLOTS, one verdict per ticket and ONE report. It is a FRESH gate, and a TIERED one. The members: RD-838 (TIER 1, NexusAI-N: an erasure's symlink-chain walk keys a loop by the canonical hop path instead of device + inode — gate 19's F-640-1, a hard-linked symlink in a long chain ending at data read as a loop and falsely purged — and its cap counts LINKS — gate 19's F-640-2, a 256-link chain to nothing kept forever; it is ROUND 3 OF THE RD-640 CLASS, past the two-NO-GO cap ONLY by Kam's ruling of 2026-10-13 09:46:48 AEDT, card nexusai-rd838-rd640-round3-1013 = a, C-213, so a NO GO returns to Tuesday and there is no round 4; merging it lands ALL of RD-640, rounds 1 and 2, whose round 2 gate 19 NO-GO'd, so its verdict covers that whole change), RD-839 (TIER 1, NexusAI-N: the erasure-status admin route withholds absolute paths outside DATA_DIR from a caller with no signed-in admin in the first-run window — gate 19's N-640-1 — while a signed-in admin and open mode after setup are unchanged and the stored record is byte-identical, C-212), and RD-840 + RD-841 (TIER 2 + ONE local browser leg, NexusAI-O: on the Sustainability tab the metric values align with the unit drawn before them, the Improvements tiles are lighter and fill the column, and every figure control draws the circled i; Kam ruled "Do both" and the screenshots go to him through Tuesday before any demo deploy). THE CROSSES (C-68): RD-838 and RD-839 meet semantically — RD-839's route serves the failure records RD-838's erasure writes, and RD-640's kept-chain error text carries an absolute end path — and RD-840 + RD-841's browser leg boots the server entry point RD-839 changes. The SLOTS are members ONLY if the brief carries their JOINS lines — the launcher tells you below. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its head AND the merged tree. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, nothing to Partner Center, the demo, production or any human, no az, no docker, no image build, no npm registry, and no browser except the ONE local browser leg the brief names (c2, with c4, c6 and y3).

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-13_nexusai-gate-batch22.md
It opens with the drafter's WRONG OR UNVERIFIED list (every place a READY or the commission contradicts the source, each marked MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1-T10 as Tuesday stamped them, Tuesday's rulings for these members verbatim, and the carried rulings (a) to (s)) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the three member READY mails it names (read each WHOLE), the clarifications the brief names at source (C-213, C-212 with its ADDENDUM, and C-139 ADDENDUM 3 first), gate 19's verdict body (body-0.md) and its RD-640 rows (body-1.md section 2) — the PRIOR ROUND for RD-838 — and gate 21's report (the structural template and the instrument source). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window; adversarial rows are written as the property, the input shape and the expected result — you write your own drivers.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones — every one is an authorised, findings-only measurement of Datasec's own product in your own trees, your own loopback servers, your own mktemp DATA_DIRs and plant roots; no row contacts a non-loopback address and no row touches the live jest queue except your own holds through the installed tool. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-838: rd-838-erasure-chain-canonical-key-s94n at 380bec32258337ef08eb7e8560077670b8c29264 (ac3ca02 red-first cells and 380bec3 the fix, on the forward merge 5bfdc93 of RD-640 round 2 b214f6f063955f95606bf22e19afb7f076de1b4b and main 08a81e2af34044276e30af962fb4c9234fbc1a3c; counts 4480/281); its red control is b214f6f (the erasure module blob 343348d). RD-839: rd-839-erasure-status-window-paths-s94n at 057a69d960d12ba090fea160ba8dfee4c70a0aa6 (TWO commits on cc42c424c1b8bc0938a1201652acc94a531ee1cc; counts 4458/280). RD-840 + RD-841: rd-840-841-sustainability-feedback-s96o at 88bba375d836e2d2edca0046ad8db84818d8e818 (THREE commits on 08a81e2; counts 4462/280). No member has a builder full verify OF ITS COMMITTED HEAD (brief WRONG 1): yours decides. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b): the merge turn order names many tickets (gate 21's members among them, and four that touch the same server entry point RD-839 changes). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (the brief's proposed order MT-B 4459/280, MT-BA 4490/282, MTF 4503/283; predicted at M0 = 944ca97fd384af55628c6669db522b734b2578e2, 4450/279), the tests census (336 at MTF), new ids 53 and missing 0 for every member. If a member is in your M0, mail a QUESTION; if anything landed, name it and re-derive every C-68 set on it (y7). Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the installed lock tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. The Datasec CodeQL org policy: a commit reaches main only after CodeQL scanned it on a PR, and alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. No member has a PR: CodeQL is NOT RUN and the CI Build is NOT RUN at every member head — say so; re-check with gh READ ONLY (repo datasecau/Reporting_Dashboard_Au), and if a PR has appeared, read its CodeQL in every state and its Build. C-185 on M0 (ruling h): the known-failing set is {rd549 O4, rd549 C2/C10 — each only when envReached alone differs}; ANY rd465 O-1 failure on M0, a head or a merged tree is a STOP; a known-set failure is named and classified, never waved; no re-run is a clearance. The shared C-57 runner's "failed" count reads its own install (RD-837): read each verify's VERDICT line and the id-superset result, never the C-57 failed count.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-838: a0 RED-AT-PARENT (the red-control erasure module reddens H at four levels, C1-256 and C2-256; and RD-640's own cells redden on main's module); a1 the head clean; a2 GATE 19'S REPRODUCERS — your copies of gate 19's own F-640-1 (the hard-linked symlink shape at four levels plus the smoke arm) and F-640-2 (255/256/257 to data and to nothing) reproducers, run against 380bec3 AND against b214f6f as the red control (the head tree with only the erasure module swapped, and b214f6f's own tree) — the control must reproduce the false purge and the kept-forever chain, or the row is VOID; a3 THE NEVER-FOLLOW ROW — gate 19's whole matrix at the head: targets touched 0; a4 the walk table; a5 new shapes; a6 mutants (tier 1, in a hold); a7 C-68; a8 the kept-failure text on an A-only arm and on the tree with both; a9 manifest evaluation, NO image built; a10 CodeQL READ ONLY; a11 prior work. RD-839: b0 RED-AT-PARENT; b1 the head clean; b2 THE WINDOW ROW — callers by states on real local servers, the failure records made by the product's own purge, withheld exactly where C-212 says; b3 THE SHAPES ROW — every shape the product writes first, then the planted blind shapes (T4); b4 the stored record byte-identical and the re-drive unchanged; b5 mutants (tier 1); b6 the C-212 partition onto main and the four overlapping heads; b7 C-68; b8 manifest; b9 CodeQL READ ONLY plus one regex timing; b10 prior work; b11 gate 19's N-640-1 request re-run, main as the control. RD-840 + RD-841: c0 RED-AT-PARENT; c1 the head clean; c2 THE BROWSER LEG — your tree of the head and of its base, open mode, USE_AZURE_LOG_ANALYTICS=true and SYNTHETIC_DEMO_FEED=true, light AND dark through the product's own theme control, three widths, values aligned, tiles filling and on the style-guide ground (dark unchanged at #262626), every control one bi-info-circle hidden from the accessibility tree with its name, hook, kpi code and evidence card unchanged; never plant, edit or inject DOM; the glyph's render only as Tuesday ruled T6; c3 THE STYLE-GUIDE ROW — every declared colour in every changed rule resolves to tokens.css with its comment, comments stripped first; c4 the e2e cells through your own config copy; c5 your own mutants (the READY declares none); c6 screenshots — yours are evidence, NOT Kam's set; c7 C-68; c8 the old heads' conflict sets; c9 manifest; c10 CodeQL READ ONLY; c11 prior work. THE CROSSES: y1 RD-838 x RD-839 — the anonymous window against RD-838's real kept-chain records; y2 the pair merges together; y3 RD-840 + RD-841's browser arm on the final tree; y4 both orders; y5 the locks; y6 C-185; y7 main moved; y8 the shipped set.

THE LIVE LOCK BASE (ruling s, H-34): no row exercises the lock tool. Your own holds are the only live tickets you ever file, through the INSTALLED tool (RD-821 round 3, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792), tagged qa-b22-. Read the live queue at start, around every hold and at end; any qa-b22- entry that is not your current hold is a STOP and a QUESTION. A changed sha256 of the installed tool is a finding.

PRIOR WORK (ruling r): verify each READY's PRIOR WORK section claim by claim against history for anything it says was replaced or removed (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every member's verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff in Tuesday's ruled order (T1; the proposal: RD-839 MT-B, RD-838 MT-BA, RD-840 + RD-841 MTF; slots where T1 puts them). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES), reading its EXIT CODE and its name-only conflict list, never a text scrape (brief WRONG 18). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MTF on node_modules proven for M0's lock 19477a9 with proxy-addr 2.0.8 read from the tree's own path (RD-827, C-205): predicted 4503/283, re-based on YOUR M0; the measurement decides. A second clone in the reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes). C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes package.json or the lock. ONE lock for every member, base, M0 and merged tree: 19477a9 (proxy-addr 2.0.8); the red-control tree b214f6f alone is on e9063d4 (proxy-addr 2.0.7) under T2. EACH TREE USES ITS OWN INSTALL, RESOLVED FROM ITS OWN LOCK (RD-827). There is NO npm registry exception in this gate. ONCE PER LOCK: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline — and EVERY npm invocation, the first one included, carries npm_config_update_notifier=false; prove the cache copy's _update-notifier-last-checked marker absent or unchanged. An ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install, never npm audit, never npx playwright install. sqlite3's binding: the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in your tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on it is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree of the same lock; never from another gate's trees.

THE BROWSER LEG (ruling q, H-32): Playwright 1.62.1 from YOUR OWN tree's node_modules, channel chrome (the local Google Chrome), HEADLESS, NO browser download — prove ~/Library/Caches/ms-playwright unchanged before and after; only http://127.0.0.1:<port> of a server YOU booted from YOUR tree, open mode, SESSION_SECRET UNSET; every non-127.0.0.1 request aborted by the page route AND the belt — the ONE exception, only if Tuesday ruled T6 (a), is serving RD-721's vendored Bootstrap Icons bytes (read from git, sha256-checked, the page's own SRI check as the landing control) to the page by route.fulfill, with no network; never plant, edit or inject DOM; every caption "local run of <sha> — NOT the demo; Chrome headless via Playwright 1.62.1; synthetic feed". If Chrome or Playwright cannot launch, c2 is NOT RUN, named — never replaced by a jsdom render. Your screenshots are evidence, not Kam's set; you send nothing to Kam.

FULL VERIFY of each head and of MTF through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers, servers, the browser), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 380bec3 4480/281, 057a69d 4458/280, 88bba37 4462/280, MTF 4503/283. RULING (b) and its EXTENSION (carried as ruling (o)): if the full verifies, the counts regeneration or the TIER-2 cell holds remain lock-starved about 2 h after filing, deliver with them NAMED NOT RUN — never "skipped" — and say in the NOT TESTED section that each member's merge hold full verify plus its PR's CI Build plus the builder's own proof hold are the gate's NOT-RUN coverage, and any red there outside C-185's known set at merge is a STOP, not a re-run. The TIER-1 cell rows (a0, a1, a6, b0, b1, b5) are NOT covered by that extension: they run, and a TIER-1 verdict whose cell rows did not run is PROVISIONAL and releases nothing. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-34 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker; mask GUIDs; the outside-path markers are needles too. H-2: seed BEFORE; every boot is a NEW process — declare it per row. H-3: a LANDING CONTROL for every plant, stored record, listener, observer, browser observer, route fulfil, filer and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd; symlink texts read back with readlink. H-15: no preload into a product process except a read-only observer from your tree. H-16: every plant checked to be what the product will treat it as (the hard-linked symlink is ONE symlink inode, nlink 2). H-17: your own censuses use pgrep, never ps. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths; path lists built in bash, the PASS/FAIL line count equal to the list. H-25: comment-aware censuses. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading, gates 19 to 21's consolidation): ONE focused hold at a time, at most about 40 minutes of planned jest, rows GROUPED into as few holds as fit and a hold whose plan would overrun SPLIT, never stretched; the TIER-1 holds are filed FIRST; every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output; each hold carries a wait deadline, and BEFORE it fires you file --replace on your own still-waiting ticket under the SAME tag. H-29: other gates' evidence is method only. H-31: offline node_modules per lock, the notifier off, and the cached sqlite3 prebuild. H-32: NO image built (the shipped-blob rows are a manifest evaluation); ONE local browser leg. H-33: plants, stored values, listeners and children counted and reaped or quarantined, never rm; every outside target lives in your own plant root. H-34: the live lock base. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch22.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; other gates' trees and report dirs are never touched; copy instruments BY COPY from gate 21's evidence/inst (its HOLD21.sh and env21.sh hard-code gate 21's dirs and its qa-floorlib21.sh carries stale ROOT and NEG defaults: re-point and correct your copies; its qa-file21.sh already has the retired yield removed) and gate 19's RD-640 instruments qa-matrix19.js, qa-matrix-run19.sh, qa-matrix-sum19.py, qa-a2-19.js, qa-lib19.js and qa-child19.js (hash each copy against the brief's sha256; re-point what sources env19.sh). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, probe, measure, screen, mutate or census scripts in place. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, no swap of the lock tool. No Azure (no az at all), no Microsoft, Azure OpenAI or Log Analytics host, no login host, no CDN, no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with the builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, hashes, reads, merge-trees in scratch objects, the offline npm ci, plain-node, server, browser and e2e rows, census greps); then file your holds tagged qa-b22-, one at a time, through the INSTALLED tool only; no tag of yours contains the word "merge" (C-141 ADDENDUM 7: only a merge HOLD's tag does). If a MERGE ticket is queued ahead of you, wait behind it. RULING (i)'s BY-HAND GATE YIELD IS RETIRED: you NEVER stop your own waiter to re-file behind a merge that filed after you — the installed tool places merges; if you see a live merge sort ahead of your own waiting ticket after you filed, quote it once (observe only), never re-file because of it. AT A WAIT DEADLINE, first in line or not: use --replace on your own still-waiting ticket BEFORE its deadline fires (C-141 ADDENDUM 6: a SAME-PLACE handover; it is refused once the old waiter has left, so a late re-file lands at the tail) and confirm from the queue listing that the old ticket went to released/ as ticket-left-* and your place is unchanged; never two live holds; a duplicate-tag refusal takes a -r<N> suffix, said in the report; you never move ahead of anything that was ahead of you; one report line per re-file with the queue place before and after FROM THE QUEUE LISTING. Once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result, including every server you boot outside a hold; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver, server, browser arm, matrix arm and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the three member branches, rd-640-eloop-and-tree-cells-s87n, the four C-212 heads and main (and each SLOT's branch if it joins), plus the installed lock tool's sha256 — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so; it must be 944ca97 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch22. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch22] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-13-gate-batch22/report.md
Write its VERDICTS and FINDINGS table early and keep it current: gate 19's session died before it assembled its report, and its verdict body was the only record.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 22
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-838 @ 380bec3 with gate 19's reproducers, the never-follow row and the cap, RD-839 @ 057a69d with the window and shapes rows, RD-840+841 @ 88bba37 with the browser leg and the style-guide row; a SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured in both orders, the C-57 and C-133 result, THE CROSSES, which rows ran on Opus 4.8 (or none), which full verifies and TIER-2 cell holds ran and which are NAMED NOT RUN under ruling (b) extended, and "CodeQL NOT RUN (no PR) for RD-838, RD-839, RD-840+841". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A9, L-B1 to L-B9, L-C1 to L-C9 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-213, C-212 with its ADDENDUM, C-139 with ADDENDA 2 and 3, C-141 with ADDENDA 5, 6 and 7, C-205, C-210, C-185 with its ADDENDA, C-190 with its ADDENDUM, C-209, C-192, C-02 and C-40 are the clarifications this batch leans on; C-01, C-20, C-34, C-49, C-57, C-68, C-76, C-89, C-97, C-102, C-104, C-112, C-115, C-125, C-130, C-133, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any member head (no member has a pull request), CodeQL at any member head (no PR), the erasure walk on Linux (its 40-link resolver; RD-838's Docker leg is relayed) or on a network filesystem, Windows-style paths in the erasure-status body beyond the shapes named, a real deployment's first-run window, the demo (behind RD-76 SSO) and its synthetic feed as deployed, any deployed environment, the Sustainability tab with Bootstrap's CDN stylesheet loaded (the browser leg is belted; Bootstrap Icons only from RD-721's vendored bytes if ruled), headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, off-host requests aborted), Kam's screenshot review (O's set, through Tuesday), real Azure, a real Docker image build (the shipped-blob legs are a manifest evaluation), Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
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
for S in "$MAIN_SHA" "$MB_A" "$MB_B" "$A_R2" "$A_R1" "$A_MRG" "$A_RED" "$B_RED" "$C_RED" "$C_FIX" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$RD721_DRAFT"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases with main and the stacks.
mb_is() { [ "$(g merge-base "$1" "$2" 2>/dev/null)" = "$3" ]; }
mb_is "$A_HEAD" "$MAIN_SHA" "$MB_A" || { echo "REFUSING: merge-base(RD-838, 944ca97) is not 08a81e2 — re-brief" >&2; exit 7; }
mb_is "$B_HEAD" "$MAIN_SHA" "$MB_B" || { echo "REFUSING: merge-base(RD-839, 944ca97) is not cc42c42 — re-brief" >&2; exit 7; }
mb_is "$C_HEAD" "$MAIN_SHA" "$MB_C" || { echo "REFUSING: merge-base(RD-840+841, 944ca97) is not 08a81e2 — re-brief" >&2; exit 7; }
for PAIR in "$A_R2 $A_HEAD" "$A_R1 $A_R2" "$MB_A $A_HEAD" "$MB_B $MB_A" "$MB_A $MAIN_SHA" "$MB_B $MAIN_SHA"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  g merge-base --is-ancestor "$X" "$Y" 2>/dev/null || { echo "REFUSING: ${X:0:7} is not an ancestor of ${Y:0:7} — a stack or base moved; re-brief" >&2; exit 7; }
done
if g merge-base --is-ancestor "$A_R2" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: RD-640 r2 (b214f6f) is already on 944ca97 — the brief's 'A lands all of RD-640' premise (WRONG 2) is stale; re-brief" >&2; exit 7; fi

# 8 — chains exact: A = 5bfdc93 (merge of b214f6f + 08a81e2) -> ac3ca02 -> 380bec3; B 2 on cc42c42; C 3 on 08a81e2; 08a81e2..A = 7 commits, 2 merges.
chain_ok() { local base="$1" head="$2" n="$3" mg="$4" got m
  got="$(g rev-list --count "${base}..${head}" 2>/dev/null)"; m="$(g rev-list --merges --count "${base}..${head}" 2>/dev/null)"
  [ "$got" = "$n" ] && [ "$m" = "$mg" ] && g merge-base --is-ancestor "$base" "$head" 2>/dev/null; }
[ "$(g rev-parse "${A_HEAD}^" 2>/dev/null)" = "$A_RED" ] && [ "$(g rev-parse "${A_RED}^" 2>/dev/null)" = "$A_MRG" ] \
  && [ "$(g rev-parse "${A_MRG}^1" 2>/dev/null)" = "$A_R2" ] && [ "$(g rev-parse "${A_MRG}^2" 2>/dev/null)" = "$MB_A" ] \
  || { echo "REFUSING: RD-838 is not 380bec3 <- ac3ca02 <- 5bfdc93 (= b214f6f + 08a81e2)" >&2; exit 8; }
chain_ok "$MB_A" "$A_HEAD" 7 2 || { echo "REFUSING: 08a81e2..380bec3 is not 7 commits with 2 merges (RD-640 r1/r2 + RD-838)" >&2; exit 8; }
chain_ok "$MB_B" "$B_HEAD" 2 0 || { echo "REFUSING: RD-839 is not TWO non-merge commits on cc42c42" >&2; exit 8; }
chain_ok "$MB_C" "$C_HEAD" 3 0 || { echo "REFUSING: RD-840+841 is not THREE non-merge commits on 08a81e2" >&2; exit 8; }
[ "$(g rev-parse "${B_HEAD}^" 2>/dev/null)" = "$B_RED" ] && [ "$(g rev-parse "${C_HEAD}^" 2>/dev/null)" = "$C_FIX" ] && [ "$(g rev-parse "${C_FIX}^" 2>/dev/null)" = "$C_RED" ] \
  || { echo "REFUSING: the red-first / fix commits of RD-839 or RD-840+841 are not as briefed" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the three member branches exactly the pins (REFUSE); main and the red-control branch read.
H212_REFS=''; for b in $H212_BRANCHES; do H212_REFS="$H212_REFS refs/heads/$b"; done
# shellcheck disable=SC2086
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "refs/heads/$R2_BRANCH" $H212_REFS || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "refs/heads/$A_BRANCH $A_HEAD" "refs/heads/$B_BRANCH $B_HEAD" "refs/heads/$C_BRANCH $C_HEAD"; do
  RF="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]${RF}\$" || {
    echo "REFUSING: origin $RF is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
R2_NOW="$(ref_now "$R2_BRANCH")"
[ "$R2_NOW" = "$A_R2" ] || echo "NOTE: origin $R2_BRANCH is '${R2_NOW:-absent}', not b214f6f — the red control stays PINNED to b214f6f by sha (a2)" >&2
# 18b — main MAY move (ruling b). It must be 944ca97 or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member-ONLY path moved REFUSES; anything else is a NOTE.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 944ca97 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$A_R2"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
ONLY_PATHS="$(printf '%s\n' "$DE" "$T640" "$TEV" "$T838" "$T839" "$SUI" "$SCSS" "$TOK" "$DBT" "$BMD" "$T840" "$E2E" "$PKG" | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ONLY_PATHS") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 944ca97..${M_ORIGIN:0:7} and touched a member-only path: $HIT — re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$SV" "$LOCK" "$TS" "$TSH" "$R465" "$R549" "$DKF" "$DIG" "$DARK" "$IDXH" "$BTC" '__tests__/helpers/image-manifest.js' | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— C-68 sets / node_modules proofs / the crosses run on M0's blobs (brief ruling b, y7); a server.js move forms a COMBINED server.js with RD-839 (C-212: guard 80 decides; b6)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 944ca97) — the gate re-pins M0 itself and re-bases every prediction" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED jest-lock tool PINNED by sha256 (REFUSE if moved); the old one named; the live default base; --replace present.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED jest-lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… (RD-821 r3, swapped after gate 21's GO) — find out who changed it; re-brief" >&2; exit 90; }
OLD_NOW="$(fsha "$LOCKOLD")"
[ "$OLD_NOW" = "$LOCK_SHA_OLD" ] || echo "NOTE: $LOCKOLD is '${OLD_NOW:-absent}', not fd223bd2… (the swap's kept copy) — named in the report" >&2
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks}"' "$LOCKTOOL" || { echo "REFUSING: the installed tool's default lock base is not the LIVE base as briefed (H-34's premise)" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL has no --replace — ruling (i)'s re-file instrument is missing" >&2; exit 90; }

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no package change; product paths as commissioned.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MB_A" "$A_HEAD" "$A_EXPECTED_FILES" "RD-838 (08a81e2..380bec3, lands RD-640)"
chk_delta "$A_MRG" "$A_HEAD" "$A_OWN_EXPECTED_FILES" "RD-838 own (5bfdc93..380bec3)"
chk_delta "$MB_B" "$B_HEAD" "$B_EXPECTED_FILES" "RD-839 (cc42c42..057a69d)"
chk_delta "$MB_C" "$C_HEAD" "$C_EXPECTED_FILES" "RD-840+841 (08a81e2..88bba37)"
[ "$(g diff --name-only "$C_FIX" "$C_HEAD" 2>/dev/null)" = "$COUNTS_FILE" ] || { echo "REFUSING: 88bba37 over b2a9f19 is not the counts file only (WRONG 1's premise)" >&2; exit 22; }
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$MB_A" "$A_HEAD" "$DE")" = "149 22" ] && [ "$(ns "$A_R2" "$A_HEAD" "$DE")" = "18 6" ] && [ "$(ns "$MB_A" "$A_HEAD" "$T640")" = "467 0" ] \
  && [ "$(ns "$MB_A" "$A_HEAD" "$TEV")" = "16 5" ] && [ "$(ns "$MB_A" "$A_HEAD" "$T838")" = "261 0" ] \
  || { echo "REFUSING: RD-838's numstats are not dataErasure +149/-22 (over main) / +18/-6 (over b214f6f), rd640 +467, erasure-verdict +16/-5, rd838 +261" >&2; exit 22; }
[ "$(ns "$MB_B" "$B_HEAD" "$SV")" = "68 1" ] && [ "$(ns "$MB_B" "$B_HEAD" "$T839")" = "249 0" ] \
  || { echo "REFUSING: RD-839's numstats are not server.js +68/-1, rd839 +249" >&2; exit 22; }
[ "$(ns "$MB_C" "$C_HEAD" "$SUI")" = "27 28" ] && [ "$(ns "$MB_C" "$C_HEAD" "$SCSS")" = "39 13" ] && [ "$(ns "$MB_C" "$C_HEAD" "$TOK")" = "2 2" ] \
  && [ "$(ns "$MB_C" "$C_HEAD" "$DBT")" = "8 2" ] && [ "$(ns "$MB_C" "$C_HEAD" "$BMD")" = "10 2" ] && [ "$(ns "$MB_C" "$C_HEAD" "$T840")" = "211 0" ] && [ "$(ns "$MB_C" "$C_HEAD" "$E2E")" = "117 0" ] \
  || { echo "REFUSING: RD-840+841's numstats are not as briefed (ui.js +27/-28, css +39/-13, tokens +2/-2, generator +8/-2, BRAND +10/-2, cells +211, e2e +117)" >&2; exit 22; }
for PAIR in "$A_HEAD $MB_A" "$B_HEAD $MB_B" "$C_HEAD $MB_C"; do
  H="${PAIR%% *}"; Bz="${PAIR#* }"
  [ -z "$(g diff --name-only "$Bz" "$H" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} changes package-lock.json/package.json over its base — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
prod() { g diff --name-only "$1" "$2" -- backend static docs Dockerfile .dockerignore .github model-config.js 2>/dev/null | sort; }
[ "$(prod "$MB_A" "$A_HEAD")" = "$DE" ] || { echo "REFUSING: RD-838 touches a product path beyond dataErasure.js" >&2; exit 22; }
[ "$(prod "$MB_B" "$B_HEAD")" = "$SV" ] || { echo "REFUSING: RD-839 touches a product path beyond server.js" >&2; exit 22; }
[ "$(prod "$MB_C" "$C_HEAD")" = "$(sorted "$BMD
$SCSS
$TOK
$SUI")" ] || { echo "REFUSING: RD-840+841 touches a product path beyond BRAND.md / sustainability.css / tokens.css / sustainability-ui.js" >&2; exit 22; }

# 93 — RD-838's premises at source (incl. WRONG 2, 3, 16).
[ "$(blob "$MB_A" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$A_R2" "$DE")" = "$DE_R2_BLOB" ] && [ "$(blob "$A_MRG" "$DE")" = "$DE_R2_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$DE")" = "$DE_A_BLOB" ] && [ "$(blob "$A_HEAD" "$T838")" = "$T838_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T838")" ] \
  && [ "$(blob "$A_HEAD" "$T640")" = "$T640_BLOB" ] && [ "$(blob "$A_R2" "$T640")" = "$T640_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T640")" ] \
  && [ "$(blob "$A_HEAD" "$TEV")" = "$TEV_A_BLOB" ] && [ "$(blob "$MAIN_SHA" "$TEV")" = "$TEV_M_BLOB" ] \
  || { echo "REFUSING: RD-838's blobs are not dataErasure 1f708e2 (main) / 343348d (b214f6f) / 26f7187 (head), rd838 21bb3d9, rd640 a817560, erasure-verdict 4b75b24 -> 13c4d63" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$DE" 'const id = cur;')" = "1" ] && [ "$(cnt "$A_R2" "$DE" 'const id = cur;')" = "0" ] && [ "$(cnt "$A_R2" "$DE" 'const id = `${st.dev}:${st.ino}`;')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$DE" 'const id = `${st.dev}:${st.ino}`;')" = "0" ] && [ "$(cnt "$A_HEAD" "$DE" 'for (let hops = 0; hops <= LINK_WALK_LIMIT; hops++) {')" = "1" ] \
  && [ "$(cnt "$A_R2" "$DE" 'for (let hops = 0; hops < LINK_WALK_LIMIT; hops++) {')" = "1" ] && [ "$(cnt "$A_HEAD" "$DE" 'const LINK_WALK_LIMIT = 256;')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$DE" 'cur = path.join(fs.realpathSync(path.dirname(cur)), path.basename(cur));')" = "1" ] \
  || { echo "REFUSING: dataErasure.js at 380bec3 / b214f6f is not the canonical-path key + link cap / dev:ino key + iteration cap as briefed (a0/a2's premise)" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$DE" 'but ends at an existing path, so the link is kept: ${walk.end}')" = "1" ] && [ "$(cnt "$A_HEAD" "$DE" "kept.code = 'ELOOP_CHAIN';")" = "1" ] \
  || echo "NOTE: RD-640's kept-chain message no longer embeds the absolute end path — brief WRONG 3 / y1 / a8 may be stale" >&2
[ "$(titles "$A_HEAD" "$T838" | wc -l | tr -d ' ')" = "6" ] || { echo "REFUSING: rd838 is not 6 test lines (12 ids: H x4, C1 x2 + 1, C2 x3, U1, U2)" >&2; exit 93; }
[ "$(titles "$MAIN_SHA" "$TEV")" = "$(titles "$A_HEAD" "$TEV")" ] || { echo "REFUSING: the erasure-verdict cell's titles differ main vs RD-838 — the 'missing 0' prediction (H-12) is stale" >&2; exit 93; }

# 95 — RD-839's premises at source (incl. WRONG 6-9).
[ "$(blob "$MB_B" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$B_HEAD" "$SV")" = "$SV_B_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$C_HEAD" "$SV")" = "$SV_M_BLOB" ] \
  && [ "$(blob "$B_HEAD" "$T839")" = "$T839_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T839")" ] \
  || { echo "REFUSING: RD-839's blobs are not server.js c8ca2b3 -> b669e02 / rd839 ad0d44d (new)" >&2; exit 95; }
[ "$(cnt "$B_HEAD" "$SV" 'async function erasurePathsWithheldFor(req) {')" = "1" ] && [ "$(cnt "$B_HEAD" "$SV" 'function withholdOutsidePaths(filesFailed, dir) {')" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$SV" "if (req.user && req.user.role === 'admin') return false;")" = "1" ] && [ "$(cnt "$B_HEAD" "$SV" '&& !roots.some((r) => p === r || p.startsWith(r + path.sep));')" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$SV" "v = v.replace(/(^|[\\s:'\"(=])(\\/[^\\s'\"),]+)/g,")" = "1" ] && [ "$(cnt "$B_HEAD" "$SV" 'const w = withholdOutsidePaths(filesFailed, dataDir);')" = "1" ] \
  || { echo "REFUSING: RD-839's helpers / admin test / inside test / backstop / call site are not as briefed (b2/b3's premise)" >&2; exit 95; }
[ "$(cnt "$B_HEAD" "$AUTH" 'if (!(firstRunComplete && hasUsers)) return false;')" = "1" ] || echo "NOTE: adminGateRefuses' setup-window line moved — brief WRONG 8 / T5 may be stale" >&2
[ "$(titles "$B_HEAD" "$T839" | wc -l | tr -d ' ')" = "9" ] || { echo "REFUSING: rd839 is not 9 test lines (W0-W5, A0, A1, O1)" >&2; exit 95; }

# 96 — RD-840 + RD-841's premises at source (incl. WRONG 10-14) and RD-721's vendored bytes (T6 (a)).
[ "$(blob "$MB_C" "$SUI")" = "$SUI_M_BLOB" ] && [ "$(blob "$C_HEAD" "$SUI")" = "$SUI_C_BLOB" ] && [ "$(blob "$MB_C" "$SCSS")" = "$SCSS_M_BLOB" ] && [ "$(blob "$C_HEAD" "$SCSS")" = "$SCSS_C_BLOB" ] \
  && [ "$(blob "$MB_C" "$TOK")" = "$TOK_M_BLOB" ] && [ "$(blob "$C_HEAD" "$TOK")" = "$TOK_C_BLOB" ] && [ "$(blob "$MB_C" "$DBT")" = "$DBT_M_BLOB" ] && [ "$(blob "$C_HEAD" "$DBT")" = "$DBT_C_BLOB" ] \
  && [ "$(blob "$MB_C" "$BMD")" = "$BMD_M_BLOB" ] && [ "$(blob "$C_HEAD" "$BMD")" = "$BMD_C_BLOB" ] && [ "$(blob "$MB_C" "$E2E")" = "$E2E_M_BLOB" ] && [ "$(blob "$C_HEAD" "$E2E")" = "$E2E_C_BLOB" ] \
  && [ "$(blob "$C_HEAD" "$T840")" = "$T840_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T840")" ] && [ "$(blob "$MB_C" "$DARK")" = "$DARK_BLOB" ] && [ "$(blob "$C_HEAD" "$DARK")" = "$DARK_BLOB" ] \
  && [ "$(blob "$MAIN_SHA" "$SUI")" = "$SUI_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SCSS")" = "$SCSS_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$TOK")" = "$TOK_M_BLOB" ] \
  || { echo "REFUSING: RD-840+841's blobs are not as briefed (ui.js e2aaa46 -> 99a721e, css 451c7c6 -> abc08fa, tokens de6e0fe -> 54f8f40, generator, BRAND, e2e, cells 2da9ee3; dark-mode e90297e unchanged)" >&2; exit 96; }
[ "$(cnt "$C_HEAD" "$SUI" "i.className = 'bi bi-info-circle';")" = "1" ] && [ "$(cnt "$C_HEAD" "$SUI" "i.setAttribute('aria-hidden', 'true');")" = "1" ] \
  && [ "$(cnt "$C_HEAD" "$SUI" 'function eyeGlyph')" = "0" ] && [ "$(cnt "$MB_C" "$SUI" 'function eyeGlyph')" = "1" ] && [ "$(cnt "$C_HEAD" "$SUI" '}, [infoGlyph()]);')" = "1" ] \
  && [ "$(cnt "$C_HEAD" "$SCSS" 'grid-template-areas: "lbl unit val eye";')" = "1" ] && [ "$(cnt "$C_HEAD" "$SCSS" 'background: #f8f9fa;              /* --nx-surface-page (RD-840) */')" = "1" ] \
  && [ "$(cnt "$C_HEAD" "$SCSS" 'flex: 1 1 150px;')" = "1" ] && [ "$(cnt "$C_HEAD" "$DARK" 'body.dark-mode .nx-sus-fig {')" = "1" ] \
  || { echo "REFUSING: RD-840+841's glyph / grid / tile ground / fill / dark rule are not as briefed (c2/c3's premise)" >&2; exit 96; }
[ "$(cnt "$C_HEAD" "$E2E" "document.fonts.check('13px \"bootstrap-icons\"')")" = "1" ] && [ "$(cnt "$C_HEAD" "$IDXH" 'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css')" = "1" ] \
  && [ -z "$(g ls-tree -r --name-only "$C_HEAD" -- static/vendor 2>/dev/null | grep -i 'bootstrap-icons')" ] \
  || echo "NOTE: the glyph cell's font check / index.html's CDN line / the absence of vendored icons at the head moved — brief WRONG 10 / T6 may be stale" >&2
[ "$(g cat-file -p "$BI_CSS_BLOB" 2>/dev/null | shasum -a 256 | cut -c1-64)" = "$BI_CSS_SHA" ] && [ "$(g cat-file -p "$BI_WOFF2_BLOB" 2>/dev/null | shasum -a 256 | cut -c1-64)" = "$BI_WOFF2_SHA" ] \
  && [ "$(blob "$RD721_DRAFT" 'static/vendor/bootstrap-icons-1.10.0/font/bootstrap-icons.css')" = "$BI_CSS_BLOB" ] \
  || echo "NOTE: RD-721's vendored Bootstrap Icons blobs are not as briefed (7d93a97 / 52b1253 with sha256 0695565c… / eba82430…) — T6 (a) has no source; the gate uses T6 (b)" >&2
[ "$(titles "$C_HEAD" "$T840" | wc -l | tr -d ' ')" = "13" ] || { echo "REFUSING: rd840-841 is not 13 test lines" >&2; exit 96; }

# 98 — shared blobs; the locks as briefed; proxy-addr per lock (RD-827).
for S in "$MAIN_SHA" "$MB_A" "$MB_B" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_NEW" ] && [ "$(blob "$S" "$PKG")" = "$PKG_NEW" ] || { echo "REFUSING: lock / package.json at ${S:0:7} are not 19477a9 / 384805d (T2)" >&2; exit 98; }
done
[ "$(blob "$A_R2" "$LOCK")" = "$LOCK_OLD" ] && [ "$(blob "$A_R2" "$PKG")" = "$PKG_OLD" ] || { echo "REFUSING: lock / package.json at b214f6f are not e9063d4 / cdb1168 (T2's red-control tree)" >&2; exit 98; }
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] && [ "$(blob "$S" "$TSH")" = "$TSH_BLOB" ] && [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] \
    && [ "$(blob "$S" "$R549")" = "$R549_BLOB" ] && [ "$(blob "$S" "$R465")" = "$R465_BLOB" ] \
    || { echo "REFUSING: test-server / helper / Dockerfile / .dockerignore / rd549 / rd465 at ${S:0:7} are not as briefed (bb45cd7 …)" >&2; exit 98; }
done
[ "$(lockver "$LOCK_OLD" proxy-addr)" = "2.0.7" ] && [ "$(lockver "$LOCK_NEW" proxy-addr)" = "2.0.8" ] \
  && [ "$(lockver "$LOCK_OLD" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_NEW" playwright)" = "1.62.1" ] \
  || { echo "REFUSING: proxy-addr is not 2.0.7 (e9063d4) / 2.0.8 (19477a9), or playwright is not 1.62.1 in both (T2, ruling q)" >&2; exit 98; }

# 23 — EXPECTED OVERLAPS (beyond the counts file): none with main since any base; no member pair shares a path.
own() { g diff --name-only "$(g merge-base "$1" "$MAIN_SHA")" "$1" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
mside() { g diff --name-only "$(g merge-base "$1" "$MAIN_SHA")" "$MAIN_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
for X in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  OV="$(comm -12 <(own "$X") <(mside "$X"))"; [ -z "$OV" ] || { echo "REFUSING: main since ${X:0:7}'s base changed a path it changes: $OV — a COMBINED blob the brief does not predict" >&2; exit 23; }
done
L3="A:$A_HEAD B:$B_HEAD C:$C_HEAD"
for x in $L3; do for y in $L3; do
  a="${x%%:*}"; b="${y%%:*}"; [[ "$a" < "$b" ]] || continue
  OV="$(comm -12 <(own "${x#*:}") <(own "${y#*:}") | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$OV" ] || { echo "REFUSING: $a x $b share '$OV' beyond the counts file — the brief predicts none" >&2; exit 23; }
done; done
[ "$(cnt "$B_HEAD" "$SV" 'const filesFailed = erasure.getFailureDetail();')" = "1" ] || echo "NOTE: RD-839's route no longer reads erasure.getFailureDetail() — cross y1 may be stale" >&2

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$MB_B 4449 279" "$MB_A 4449 279" "$MAIN_SHA 4450 279" "$A_R2 4317 265" "$A_HEAD 4480 281" "$B_HEAD 4458 280" "$C_HEAD 4462 280"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$MB_B" "$MB_A" "$MAIN_SHA" "$A_R2" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "332 332 332 310 334 333 333 " ] || { echo "REFUSING: the __tests__ census (cc42c42 08a81e2 M0 b214f6f A B C) is '$CENSUS', not '332 332 332 310 334 333 333'" >&2; exit 35; }

# 70 — the lock on origin main; the npm cache, the sqlite3 prebuild, Chrome, and the carried rulings (NOTEs where the gate decides, REFUSALs where a ruling is missing).
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_NEW" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not 19477a9 — another lock is in play; prove node_modules before any run (H-31)" >&2
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in proxy-addr/-/proxy-addr-2.0.7.tgz proxy-addr/-/proxy-addr-2.0.8.tgz sqlite3/-/sqlite3-5.1.7.tgz playwright/-/playwright-1.62.1.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -d "$CHROME_APP" ] || echo "NOTE: $CHROME_APP is absent — c2 (the browser leg) will be NOT RUN, named (ruling q)" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" && grep -qF 'merge hold full verify + PR Build are the gate' "$RULING_B" \
  || { echo "REFUSING: Tuesday's ruling (b) (lock-starved full verifies NAMED NOT RUN) is not at $RULING_B as quoted" >&2; exit 70; }
[ -s "$B20_STARVE" ] && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$B20_STARVE" || { echo "REFUSING: ruling (o)'s EXTENSION (gate 20's ruling (c)) is not at $B20_STARVE as quoted" >&2; exit 70; }
[ -s "$BROWSER_ANS" ] && grep -qF 'Playwright 1.62.1 from YOUR tree' "$BROWSER_ANS" && grep -qF "headless (channel 'chrome'), no download" "$BROWSER_ANS" \
  || { echo "REFUSING: Tuesday's browser-driver ruling (ruling q) is not at $BROWSER_ANS as quoted" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" \
  || { echo "REFUSING: the RETIREMENT of ruling (i)'s yield is not in gate 19's RELEASE as quoted" >&2; exit 70; }
[ -s "$G21_RELEASE" ] && grep -qF 'RD-821 SWAP (O): AUTHORISED now that the gate says GO.' "$G21_RELEASE" \
  || { echo "REFUSING: gate 21's RELEASE (the authority for the installed RD-821 r3 tool) is not at $G21_RELEASE as quoted" >&2; exit 70; }
grep -qF 'ln -s ../../worktrees/mkt-rc-selfcontained-s62/node_modules' "$C57_RUNNER" || echo "NOTE: the shared C-57 runner no longer links the old install — RD-837 may be fixed; ruling (e)'s note may be stale" >&2

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean; a reader failure REFUSES.
MT_PAIRS=0
mt_check() { local X="$1" Y="$2" label="$3" CONF
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  case "$CONF" in *MTFAIL*) echo "REFUSING: the merge-tree reader FAILED on $label (${CONF}) — an unreadable merge is UNKNOWN, never clean (80; WRONG 18)" >&2; exit 80 ;; esac
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree $label carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
}
mt_check "$M_ORIGIN" "$A_HEAD" "main x RD-838"; mt_check "$M_ORIGIN" "$B_HEAD" "main x RD-839"; mt_check "$M_ORIGIN" "$C_HEAD" "main x RD-840+841"
mt_check "$A_HEAD" "$B_HEAD" "RD-838 x RD-839"; mt_check "$A_HEAD" "$C_HEAD" "RD-838 x RD-840+841"; mt_check "$B_HEAD" "$C_HEAD" "RD-839 x RD-840+841"
# C-212 (+ ADDENDUM): RD-839 onto the four overlapping server.js heads AS THEY ARE NOW — counts-only or clean, else a STOP. A head absent from origin is a NOTE.
H212_DESC=''
for b in $H212_BRANCHES; do
  hs="$(ref_now "$b")"
  if [ -z "$hs" ]; then echo "NOTE: origin $b is absent (landed and deleted, or renamed) — C-212's merge-tree onto it is moot; main carries it if it landed" >&2; H212_DESC="$H212_DESC $b absent;"; continue; fi
  [ "$(g cat-file -t "$hs" 2>&1)" = "commit" ] || { echo "REFUSING: origin $b = $hs is not in the object store — C-212's merge-tree cannot be read; wait for a fetch" >&2; exit 80; }
  if g merge-base --is-ancestor "$hs" "$M_ORIGIN" 2>/dev/null; then H212_DESC="$H212_DESC $b ${hs:0:7} (on main);"; continue; fi
  mt_check "$hs" "$B_HEAD" "$b ${hs:0:7} x RD-839 (C-212)"
  H212_DESC="$H212_DESC $b ${hs:0:7} counts-only/clean;"
done

# 31 — READYs, builder evidence, prior reports, gate 21/19's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$CLAR" "$C133" "$BRIEF21" "$B21_REPORT" "$B19_BODY0" "$B19_BODY1" "$B19_MXA" "$B19_MXF" \
         "$N_PLAN" "$N_839READY" "$N_GO838" "$O_PLAN" "$O_BRIEF" \
         "$ST/s94n/rd838-proof.out" "$ST/s94n/rd838-proof.sh" "$ST/s94n/rd838-red.out" "$ST/s94n/set-rd838.lst" \
         "$ST/s94n/rd839-proof.out" "$ST/s94n/rd839-proof.r1.out" "$ST/s94n/rd839-proof.sh" "$ST/s94n/set-rd839.lst" \
         "$ST/s96o/rd840-proof.log" "$ST/s96o/pw-chrome.config.js" "$ST/s96o/shots.js" "$ST/s96o/surface.sh" "$ST/s96o/slip-log.md" \
         "$ST/s96o/screens/before-facts.json" "$ST/s96o/screens/after-facts.json" "$C57_RUNNER" \
         "$B21_INST/HOLD21.sh" "$B21_INST/env21.sh" "$B21_INST/qa-holdlib21.sh" "$B21_INST/qa-floorlib21.sh" "$B21_INST/qa-floorcount.py" "$B21_INST/qa-to.sh" "$B21_INST/qa-jestwrap.sh" "$B21_INST/qa-jsum.js" \
         "$B21_INST/qa-runj21.sh" "$B21_INST/qa-mut21.py" "$B21_INST/qa-mutlib21.sh" "$B21_INST/qa-merge21.sh" "$B21_INST/qa-build21.sh" "$B21_INST/qa-npm21.sh" "$B21_INST/qa-file21.sh" \
         "$B21_INST/qa-verify21.sh" "$B21_INST/qa-h1-selftest21.sh" "$B21_INST/qa-h1-scan.py" "$B21_INST/qa-mail.py" "$B21_INST/qa-mailread.py" "$B21_INST/qa-lockcheck.py" \
         "$B21_INST/qa-ssprint.sh" "$B21_INST/qa-netbelt.sb" "$B21_INST/qa-netbelt-nodns.sb" "$B21_INST/qa-netbelt-ctl.js" "$B21_INST/qa-c57-id-superset21.sh" "$B21_INST/qa-cov-setup.js" \
         "$B21_INST/qa-srv21.js" "$B21_INST/qa-manifest21.js" "$B21_INST/qa-b2-21.js" "$B21_INST/qa-pin21.sh" "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
NPNG="$(ls "$ST/s96o/screens/" 2>/dev/null | grep -c '\.png$')"
[ "$NPNG" = "16" ] || echo "NOTE: O's screens/ holds $NPNG PNGs, not 16 — c6 / T7 read what is there" >&2
# gate 19's RD-640 instruments, pinned (a2-a4 copy them).
for PAIR in "qa-matrix19.js 2d6356dd07047fa9bc4a545f921ee68198635baba17ee448577449291f67247d" "qa-matrix-run19.sh 080ba04a78d8713a2538ad22b63421a26dd508f64c266ef74be5b131337aedba" \
            "qa-matrix-sum19.py c90b3d773de2f2a7f736b2c41cd63789da1963d974453dc60336cf23db1841d0" "qa-a2-19.js b37a6b4634eb72b440723bfd6beaa350e71b3d20b02447e3fde5e1b4faf047a6" \
            "qa-lib19.js fe4bc79f1e4b93ca9e8321216a833c92dbd2facddc9c734e8ff30c34c3d7460f" "qa-child19.js 581350071b5938edcaa05d62c2b78c23dd27f8989f1734de24b97e44509439a1"; do
  F="${PAIR%% *}"; W="${PAIR#* }"
  [ "$(fsha "$B19_INST/$F")" = "$W" ] || { echo "REFUSING: gate 19's $F is not sha256 ${W:0:12}… (a2-a4's instrument; the brief pins it)" >&2; exit 31; }
  grep -qF "$W" "$BRIEF" || { echo "REFUSING: brief does not pin $F's sha256" >&2; exit 31; }
done
grep -qF "'hl-data'" "$B19_INST/qa-matrix19.js" || grep -qF '"hl-data"' "$B19_INST/qa-matrix19.js" || grep -qF 'hl-data' "$B19_INST/qa-matrix19.js" \
  || { echo "REFUSING: gate 19's qa-matrix19.js carries no hl-data shape (F-640-1's reproducer)" >&2; exit 31; }
grep -qF 'c256-nothing' "$B19_INST/qa-matrix-run19.sh" || { echo "REFUSING: gate 19's qa-matrix-run19.sh carries no c256-nothing shape (F-640-2's reproducer)" >&2; exit 31; }
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "$A_HEAD" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "$B_HEAD" "$READY_B" && grep -qF "$C_HEAD" "$READY_C" \
  && grep -qF 'PRIOR WORK' "$READY_A" && grep -qF 'PRIOR WORK' "$READY_B" && grep -qF 'PRIOR WORK' "$READY_C" && grep -qiF 'round 3 of the RD-640 class' "$READY_A" \
  || { echo "REFUSING: a READY does not name its head, a PRIOR WORK section is missing, or RD-838's READY does not declare its round" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4480/4480 tests passed across 281 suites (jest exit 0)' "$ST/s94n/rd838-proof.out" && grep -qF 'HEAD 5bfdc93 dirty' "$ST/s94n/rd838-proof.out" \
  && grep -qF 'VERDICT: PASS — 4458/4458 tests passed across 280 suites (jest exit 0)' "$ST/s94n/rd839-proof.out" && grep -qF 'HEAD cc42c42 dirty' "$ST/s94n/rd839-proof.out" \
  && grep -qF 'VERDICT: PASS — 4462/4462 tests passed across 280 suites (jest exit 0)' "$ST/s96o/rd840-proof.log" && grep -qF '=== HEAD b2a9f19 tracked-diffs []' "$ST/s96o/rd840-proof.log" \
  || { echo "REFUSING: a builder log no longer carries the line the brief quotes (WRONG 1's premise)" >&2; exit 31; }
grep -qF 'F-640-1' "$B19_BODY0" && grep -qF 'F-640-2' "$B19_BODY0" && grep -qF 'N-640-1' "$B19_BODY0" && grep -qF 'RD-640 round 2 of 2 (TIER 1)' "$B19_BODY1" \
  || { echo "REFUSING: gate 19's verdict body / RD-640 rows no longer read as the brief quotes" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B21_REPORT" || { echo "REFUSING: gate 21's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-51735\}' "$B21_INST/qa-floorlib21.sh" || echo "NOTE: gate 21's qa-floorlib21.sh ROOT default is no longer 51735 — the brief's 'STALE defaults' line names the old value" >&2
grep -qF 'REMOVED in batch21: the by-hand merge yield (retired)' "$B21_INST/qa-file21.sh" || echo "NOTE: gate 21's qa-file21.sh no longer says the yield is removed — the gate checks its copy for a yield block before use" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | 20' "$BRIEF21" || echo "NOTE: gate 21's brief does not read as stamped — the template reference may be stale" >&2

# 83 — the C-133 script is the RD-658 version the brief names (ruling l / H-30).
C133_NOW="$(fsha "$C133")"
[ "$C133_NOW" = "$C133_SHA" ] || echo "NOTE: session-tools/s78g/c133-accounting.py sha256 is '${C133_NOW:-unreadable}', not 6f938bfc…f972f — the gate names the version it used (H-30)" >&2

# 39 — the floor instruments are named in the brief.
for f in "$PREV_FLOORLIB" "$G7R1_FLOOR"; do
  grep -qF "$f" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument $f" >&2; exit 39; }
done

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "$B21_INST/" "$B19_INST/" "2026-10-13_nexusai-rd838-READY-mail.txt" "2026-10-13_nexusai-rd839-READY-mail.txt" "2026-10-13_nexusai-rd840-841-READY-mail.txt" \
         "2026-10-12_nexusai-gate-batch21.md" "2026-10-12_nexusai_gate19_RELEASE.md" "2026-10-12_nexusai_gate21_RELEASE.md" "2026-10-13_nexusai_N_GO_rd838.md" \
         "2026-10-13_nexusai_N_ANSWER_plan_rd838_rd839.md" "2026-10-13_nexusai_N_ANSWER_rd839_ready.md" "2026-10-13_nexusai_O_ANSWER_plan_rd840_rd841.md" "2026-10-13_nexusai_O_BRIEF_rd840_rd841.md" \
         "answer-starvation.txt" "qa-matrix19.js" "qa-a2-19.js" "matrix-A-head.jsonl" "matrix-fixprobe.jsonl" "body-0.md" "body-1.md" "qa-file21.sh" "/reports/2026-10-07-gate-batch19/"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in '**RD-838 is TIER 1**' '**RD-839 is TIER 1**' '**RD-840 + RD-841 is TIER 2 + ONE BROWSER LEG.**' 'THIS IS A TIERED GATE' 'a NO GO returns to Tuesday, never a round 4' \
         'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'THE BROWSER DRIVER' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' 'THE CROSSES' '--replace' 'qa-b22-' 'RETIRED' 'H-34' 'C-213' 'C-212'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-838 (TIER 1' 'ROUND 3 OF THE RD-640 CLASS' 'RD-839 (TIER 1' 'RD-840 + RD-841 (TIER 2 + ONE local browser leg' 'no round 4' \
         'TIERED' 'one verdict per ticket' 'THE CROSSES' 'manifest evaluation' 'NO image built' 'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' \
         'Playwright 1.62.1' 'channel chrome' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-b22-' 'RETIRED' 'never plant' 'C-213' 'C-212' 'GATE 19'"'"'S REPRODUCERS' 'red control'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$MAIN_SHA" "$MB_A" "$MB_B" "$A_R2" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$DE_M_BLOB" "$DE_R2_BLOB" "$DE_A_BLOB" "$T640_BLOB" "$TEV_M_BLOB" "$TEV_A_BLOB" "$T838_BLOB" "$SV_M_BLOB" "$SV_B_BLOB" "$T839_BLOB" "$T840_BLOB" \
         "$SUI_M_BLOB" "$SUI_C_BLOB" "$SCSS_M_BLOB" "$SCSS_C_BLOB" "$TOK_M_BLOB" "$TOK_C_BLOB" "$DBT_C_BLOB" "$BMD_C_BLOB" "$E2E_C_BLOB" "$DARK_BLOB" \
         "$LOCK_NEW" "$LOCK_OLD" "$A_MRG" "$A_RED" "$B_RED" "$C_RED" "$C_FIX" "$A_R1" "$RD721_DRAFT" "$BI_CSS_BLOB" "$BI_WOFF2_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
for S in "$C133_SHA" "$PREBUILD_SHA" "$BI_CSS_SHA" "$BI_WOFF2_SHA"; do grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }; done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 22' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 22 has no priority member" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
# the gate's own tags must never read as a merge ticket (C-141 ADDENDUM 7): no 'qa-b22-…merge…' tag suggested anywhere.
[ "$(grep -oE 'qa-b22-[A-Za-z0-9_-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-b22- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-b22-[A-Za-z0-9_-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-b22- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED: neither the brief nor the prompt may instruct one; both must say it is retired. Then the jest queue as the launch finds it (read-only ls/grep).
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield (gate 19's RELEASE item 5)" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  BQ="$(grep -l '^tag=qa-b2[12]' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ qa-b21*/qa-b22* ticket(s) in the jest queue now — a live gate's: FIFO, never touched (or a stale gate-22 ticket: read before launch)" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)) is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31 (RE-BASED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-33 (RE-BASED' "$BRIEF" && grep -qF 'H-34 (RE-BASED' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-34 (re-based)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-838 RD-839 RD-840 RD-841 RD-640 RD-721 RD-827 RD-837 C-213 C-212 C-139 C-141 C-205 C-210 C-185 C-190 C-209 C-192 C-02 C-40
C-01 C-20 C-34 C-49 C-57 C-68 C-76 C-89 C-97 C-102 C-104 C-112 C-115 C-125 C-130 C-133 C-174 C-186 ADDENDA%5,%6%and%7 RED-AT-PARENT F-640-1 F-640-2 N-640-1
a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 y1 y2 y3 y4 y5 y6 y7 y8
MT-B MT-BA MTF M0 SLOTS JOINS NEVER-FOLLOW%ROW WINDOW%ROW SHAPES%ROW BROWSER%LEG STYLE-GUIDE%ROW b214f6f 343348d #262626 bi-info-circle tokens.css
USE_AZURE_LOG_ANALYTICS=true SYNTHETIC_DEMO_FEED=true 4503/283 4450/279 4459/280 4490/282 4480/281 4458/280 4462/280 new%ids%53 missing%0 19477a9 e9063d4 2.0.8 2.0.7 proxy-addr
L-A1 L-A9 L-B1 L-B9 L-C1 L-C9 L-Y1 H-1 H-2 H-3 H-4 H-9 H-15 H-16 H-17 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 SCRATCH%object%dir git%clone%--shared REGENERATION ms-playwright route.fulfill
id-superset pull%request STOP POSITIVE%CONTROL%FIRST node%--check bash%-n VOID EXCLUSIVE qa-b22- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --replace SAME-PLACE%handover DEADLINE HEARTBEAT 2%minutes 5%minutes finally
SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center
npm%install --offline ENOTCACHED HOLD21.sh qa-floorlib21.sh qa-file21.sh qa-matrix19.js qa-a2-19.js Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> instrument never%fixes
GROUPED SPLIT never%dismissed PROVISIONAL WRONG%18 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 4b. TARGET B' '^## 4c. TARGET C' \
         '^## 6. THE CROSSES' '^## 7. THE MERGED TREE' '^## 8. CI' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOTS' '^## PROVENANCE' '^### MERGE ORDER' \
         '^### TARGET A' '^### TARGET B' '^### TARGET C' '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# the round-N rule (template, 2026-09-10): the PRIOR ROUND block names round N-1's report path.
grep -qE '^PRIOR ROUND \(RD-838\): round 2 of the RD-640 class gated `b214f6f063955f95606bf22e19afb7f076de1b4b`, verdict \*\*NO GO\*\*' "$BRIEF" && grep -qF 'ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/`' "$BRIEF" \
  || { echo "REFUSING: the brief's PRIOR ROUND block does not name round 2's sha, verdict and report path (template round-N rule)" >&2; exit 19; }
# the WRONG list sits ABOVE the rulings (the commission's order), and every WRONG item is marked MEASURED or READ-ONLY-INFERRED somewhere in its line.
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-A8 L-A9 L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-B9 L-C1 L-C2 L-C3 L-C4 L-C5 L-C6 L-C7 L-C8 L-C9 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 c11 y1 y2 y3 y4 y5 y6 y7 y8; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
for R in s-0 s-1 s-2 s-3 s-4 s-5; do
  grep -qF "**$R " "$BRIEF" || { echo "REFUSING: brief lacks the SLOT row $R" >&2; exit 19; }
done
# the T-ruling slots: T1..T10 each present as 'RULED:' (stamped or not).
for n in 1 2 3 4 5 6 7 8 9 10; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# every builder's stated scope / limits / interpretation lines and Tuesday's rulings carried verbatim (each line checked in its source AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; NP) F="$N_PLAN" ;; NR) F="$N_839READY" ;; NG) F="$N_GO838" ;; OP) F="$O_PLAN" ;; OB) F="$O_BRIEF" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|The demo (RD-76); CodeQL (no PR); the git-reading suites on Linux (no .git in the container copy); a network filesystem; ENOTDIR's own ruling (U2 pins today's behaviour, which gate 19 a5 recorded as the accepted cost; RD-824 holds the question, and U2 changes with it).
A|M-noCanonStrKey is not separate any more: with the canonical-path key it IS M-noCanon (its dev:ino anchor no longer exists).
A|No unmerged rd-* head touches dataErasure.js, the rd640 file, the erasure-verdict cell or rd838 (git diff --name-only origin/main...<head>, every head, after main 944ca97).
B|The Linux runner (no PR, so no CI Build; this was macOS, where the outside path is /private/var/...); CodeQL (no PR); Windows-style absolute paths (the backstop matches POSIX tokens only); the demo (RD-76). A signed-in admin IN the window cannot exist on a real deployment without sign-in configured; not driven.
B|No jsonStorage at all (the gate cannot tell the window): withheld, the safe direction.
C|Offline install: the i comes from the Bootstrap Icons CDN like every other tab's icons, so without internet it disappears there too. RD-721 (P's vendoring, order item 20) fixes all of them.
C|My browser runs let the page load its CDN assets (Bootstrap, Bootstrap Icons, PapaParse), as the demo does. A strict off-host belt like the gate's will block the font, and no bi-* glyph then renders: the RD-841 glyph cell needs the font.
C|The synthetic feed rolls with the clock, so figures differ slightly between before and after (e.g. 36,780 -> 36,788). Not from this change.
C|No demo render (RD-76). No image built. CodeQL not run (no PR; the change is CSS, a DOM glyph and tests).
NG|Decision nexusai-rd838-rd640-round3-1013: a — Yes, round 3 under RD-838
NG|N builds RD-838 on RD-640's branch with the two fixes and the missing cells; full tier-1 gate; merges in turn only on a GO.
NP|In the route only, when the caller was admitted without a signed-in admin AND the deployment is in the first-run window, withhold outside-DATA_DIR absolute paths (survivingTarget AND the matching text in error) behind a fixed marker, with pathsWithheld: true and the one-sentence pointer to where the full path lives. Signed-in admin unchanged; open mode after setup unchanged (C-02 is Kam's by-design ruling, not ours to narrow here); stored data unchanged byte for byte (C-139 ADDENDUM 3).
NP|Your edit stays inside the erasure-status route handler (and a helper beside it, if you need one). The READY carries a merge-tree of your head onto each of the four overlapping heads (rd-721, rd-761, rd-794, rd-819) and onto main
NR|That is the standing C-89 counts conflict that every forward merge resolves by regenerating the counts once at its merge turn; it is NOT a C-212 stop.
NR|a conflict confined to the counts file is C-89 and is reported, not stopped on; any conflict in any OTHER file is still a STOP.
OB|Decision nexusai-sustainability-feedback-rd840-rd841-1013: a — Do both
OB|Build RD-840 and RD-841; screenshots in both themes to you before any demo deploy.
OP|Dark keeps #262626 (--nx-surface-raised dark), unchanged.
OP|Use `<i class="bi bi-info-circle" aria-hidden="true">` inside the existing button, the same glyph and mechanism the other tabs use. Keep the button, its aria-label, the nx-eye hook and wireDisclosure exactly as they are.
OP|every literal resolves to a token with its comment (brand-token-conformance must stay green)
OP|Tuesday sends them to Kam before any demo deploy.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
It applies to RD-838 only and does not lift the cap for any other class.
Open mode after setup is unchanged: C-02 is Kam's by-design ruling, not narrowed here.
it is REPORTED, not stopped on.
An ELOOP does NOT prove a loop
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
Its closure is read AFTER the merge, on main's push analysis, by alert number
is a SAME-PLACE handover.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
Its id-superset verdict is unaffected, but its "failed" count now reads the install, not the tree
is NOT REACHABLE in NexusAI's configuration
A local run serves every page and API with no sign-in.
A check must be able to fail on the thing it claims to be about.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
A missing id is ACCOUNTED, not a STOP, only when BOTH of these hold for its file
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
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
A cell that fails for a known, ticketed reason is PARKED outside the suite, never `test.skip`ped inside it.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b22-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may MOVE' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' \
         'ticket-left-*' 'never two live holds' '-r<N>' 'Every finding names its instrument' 'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'no round 4'; do
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
for w in 'RED-AT-PARENT' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4503/283' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         '19477a9' 'e9063d4' 'proxy-addr' 'RD-827' 'RD-837' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' \
         'hl-data' 'c256-nothing' 'linkat' 'nlink 2' 'canonical' 'LINK_WALK_LIMIT' 'ELOOP_CHAIN' 'C-213' 'round 3' 'F-640-1' 'F-640-2' 'N-640-1' 'never-follow' \
         'erasurePathsWithheldFor' 'withholdOutsidePaths' 'pathsWithheld' 'firstRunComplete && hasUsers' 'C-212' 'C-139 ADDENDUM 3' 'rd-721' 'rd-761' 'rd-794' 'rd-819' \
         'bi bi-info-circle' 'aria-hidden' '#262626' '#f8f9fa' 'tokens.css' 'BRAND.md' 'brand-token-conformance' 'route.fulfill' 'SRI' 'NOT Kam' 'never plant' \
         'Playwright 1.62.1' "channel: 'chrome'" 'ms-playwright' 'ANY rd465 O-1 failure' 'ADDENDUM SLOTS' 'S1 SLOT' 'S2 SLOT' \
         'WRONG 1' 'WRONG 2' 'WRONG 3' 'WRONG 6' 'WRONG 8' 'WRONG 10' 'WRONG 12' 'WRONG 18' 'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib21.sh' 'HOLD21.sh' 'qa-file21.sh' \
         'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31' 'never dismissed' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the ADDENDUM SLOTS (GENERIC): each EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
SLOT_STATE=''
SLOT_DESC=''
slot() {   # $1 = S1|S2
  local id="$1" J E sha br tier rdy now base PP tk RC
  J="$(grep -E "^ADDENDUM $id RD-[0-9]+ JOINS @ [0-9a-f]{40} ON [A-Za-z0-9._/-]+ TIER [12] \\| READY /" "$BRIEF" 2>/dev/null)"
  E="$(grep -c "^$id SLOT: EMPTY\$" "$BRIEF" 2>/dev/null)"
  if [ -z "$J" ]; then
    [ "$E" = "1" ] || { echo "REFUSING: the $id slot is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
    SLOT_STATE="$SLOT_STATE Slot $id is EMPTY: no ticket joins through it; say so in the report."
    SLOT_DESC="$SLOT_DESC $id EMPTY;"; return 0
  fi
  [ "$(printf '%s\n' "$J" | grep -c .)" = "1" ] && [ "$E" = "0" ] || { echo "REFUSING: the $id slot has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  tk="$(printf '%s\n' "$J" | sed -E 's/^ADDENDUM [^ ]+ (RD-[0-9]+) JOINS .*/\1/')"
  sha="$(printf '%s\n' "$J" | sed -E 's/^.* JOINS @ ([0-9a-f]{40}) .*/\1/')"
  br="$(printf '%s\n' "$J" | sed -E 's/^.* ON ([A-Za-z0-9._/-]+) TIER .*/\1/')"
  tier="$(printf '%s\n' "$J" | sed -E 's/^.* TIER ([12]) .*/\1/')"
  rdy="$(printf '%s\n' "$J" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  for X in "$A_BRANCH" "$B_BRANCH" "$C_BRANCH"; do [ "$br" != "$X" ] || { echo "REFUSING: the $id slot names a member's branch $br (89)" >&2; exit 89; }; done
  lsr "refs/heads/$br" || { echo "REFUSING: ls-remote of the $id branch failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN (C-192) (89)" >&2; exit 89; }
  now="$(printf '%s\n' "$LSR_OUT" | awk -v r="refs/heads/$br" '$2==r{print $1}')"
  [ "$now" = "$sha" ] || { echo "REFUSING: the $id ADDENDUM names $sha but origin $br is '${now:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$sha" 2>&1)" = "commit" ] || { echo "REFUSING: $tk $sha is not in the object store (89)" >&2; exit 89; }
  [ -s "$rdy" ] && grep -qF "${sha:0:7}" "$rdy" || { echo "REFUSING: $tk's READY '$rdy' is absent or does not name ${sha:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$sha" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: $tk ${sha:0:7} is already on main (89)" >&2; exit 89; fi
  base="$(g merge-base "$sha" "$M_ORIGIN")"
  [ -z "$(g diff --name-only "$base" "$sha" -- "$PKG" "$LOCK" 2>/dev/null)" ] || { echo "REFUSING: $tk changes package.json or the lock over its base (89)" >&2; exit 89; }
  PP="$(g diff --name-only "$base" "$sha" 2>/dev/null | grep -v '^__tests__/' | grep -vxF "$COUNTS_FILE" | tr '\n' ' ' | sed 's/ $//')"
  echo "NOTE: $tk ($id) touches product paths: '${PP:-none (test-only)}' — the gate names them under s-0" >&2
  for X in "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
    RC="$(conflicts "$X" "$sha" | tr '\n' ' ' | sed 's/ $//')"
    case "$RC" in *MTFAIL*) echo "REFUSING: the merge-tree reader FAILED on ${X:0:7} x $tk (${RC}) (89)" >&2; exit 89 ;; esac
    [ -z "$RC" ] || [ "$RC" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x $tk conflicts beyond the counts file: '$RC' (89)" >&2; exit 89; }
    MT_PAIRS=$((MT_PAIRS + 1))
  done
  SLOT_STATE="$SLOT_STATE $tk JOINS this gate per the brief's ADDENDUM SLOTS ($id), at $sha (origin $br, re-pinned by the launcher), TIER $tier as Tuesday wrote it, READY $rdy — gate it by the brief's generic slot rows (s-0..s-5) and merge it where T1 puts it."
  SLOT_DESC="$SLOT_DESC $id $tk JOINS @ ${sha:0:7} ($br, tier $tier);"
}
slot S1
slot S2

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell.
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
# the coordinator (gate 21's T8): a pane named 'tuesday' OR 'wednesday' on this machine — exactly one of the two names live, exactly one pane.
COORD_NAME=''
for NAME in tuesday wednesday; do
  if [ -n "$(pane_pid_of "$NAME" | sed '/^$/d')" ]; then
    [ -z "$COORD_NAME" ] || { echo "REFUSING: panes named BOTH 'tuesday' and 'wednesday' are live — the coordinator's negative control is ambiguous (T8)" >&2; exit 38; }
    COORD_NAME="$NAME"
  fi
done
[ -n "$COORD_NAME" ] || { echo "REFUSING: no tmux pane named 'tuesday' or 'wednesday' — the coordinator's negative control is required (T8)" >&2; exit 38; }
[ "$COORD_NAME" = "tuesday" ] || echo "NOTE: the coordinator's pane is named '$COORD_NAME' on this machine — used as the coordinator's negative control" >&2
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R "$COORD_NAME"; do
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "$NP" = "0" ]; then
    echo "NOTE: no tmux pane named '$NAME' — that builder seat is not a negative control this launch" >&2; continue
  fi
  [ "$NP" = "1" ] || { echo "REFUSING: more than one tmux pane named '$NAME': '$PP' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
  [ "$NAME" = "$COORD_NAME" ] || NEG_BUILDERS=$((NEG_BUILDERS + 1))
done
NEG_SEATS="${NEG_SEATS# }"
[ "$NEG_BUILDERS" -ge 3 ] || { echo "REFUSING: only $NEG_BUILDERS live builder seat(s) among M/N/O/P/R — at least three negative controls are required" >&2; exit 38; }
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
# every live 'QA/*' pane other than this gate's own is a PEER negative control (a live claude under it, exactly one).
PEERS="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep '^QA/' | grep -vxF "$ROUTE_NAME" | sort -u)"
while IFS= read -r PEER; do
  [ -n "$PEER" ] || continue
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer QA seat);"
    echo "NOTE: $PEER has a live claude — a PEER QA seat: FIFO, never touched; added as a negative control" >&2
  fi
done <<EOF_PEERS
$PEERS
EOF_PEERS

# 86 — no live gate-22 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 22 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note + every 'RULED: @STAMP@' slot, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
NSTAMP="$(grep -cF "$PH_STAMP" "$BRIEF")"
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 90 22 93 95 96 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 89 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-838 $A_HEAD · RD-839 $B_HEAD · RD-840+841 $C_HEAD · red control $R2_BRANCH ${R2_NOW:0:12} · lock tool sha256 ${INST_NOW:0:12}… · SLOTS:$SLOT_DESC" >&2
  echo "  C-212 heads:$H212_DESC" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): $NSTAMP stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T10) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 3 member branches at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192); red control $R2_BRANCH ${R2_NOW:0:7}"
  echo "  main ${M_ORIGIN:0:7} (944ca97 or a descendant; no member-only path moved; no member on it) (18b)"
  echo "  installed jest-lock tool 3c33f5ae… pinned; live default base named; --replace present (90)"
  echo "  merge-bases + stacks (7); chains (8); deltas + no package change + product paths (22); premises (93 95 96); locks + proxy-addr (98)"
  echo "  overlaps (23); counts + census (35); npm cache + sqlite3 prebuild + Chrome + the carried rulings (70); $MT_PAIRS three-argument merge-trees counts-only or clean, reader under LC_ALL=C (80, 89); C-212 heads:$H212_DESC; evidence (31); C-133 script (83)"
  echo "  yield RETIRED (41); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); SLOTS:$SLOT_DESC (89); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$R2_BRANCH = ${R2_NOW:-absent} (the red control is pinned to $A_R2 by sha); refs/heads/main = $M_ORIGIN (944ca97 or a descendant; no member-only path moved since 944ca97; no member on it). The installed jest-lock tool $LOCKTOOL sha256 $INST_NOW equals the pin. $MT_PAIRS three-argument merge-trees (read-only, no objects written, the reader under LC_ALL=C) were counts-only or clean across main, every member pair and RD-839 onto the C-212 heads:$H212_DESC These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOTS:$SLOT_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
