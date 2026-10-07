#!/bin/bash
# launch_qa_nexusai_gate_batch19.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 19"), SEVEN members (+ TWO ADDENDUM SLOTS),
# one verdict per ticket (RD-801 and RD-822 are two), ONE report (drafted 2026-10-07 ~14:28–~15:30 AEDT by a read-only drafting agent for Tuesday;
# the second drafter of this gate — the first was stopped by the safeguards, its partial is quarantined and is NEVER launched).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-640 r2 of 2 (TIER 1, erasure) rd-640-eloop-and-tree-cells-s87n @ b214f6f: TWO commits on e944c9c (a merge of main d97039f into round 1 588ec63). dataErasure 6002d71 -> 343348d. 4317/265.
#   B — RD-794 (TIER 1, runtime Ollama path removed) rd-794-ollama-runtime-slice-s89r @ cd171f9: SEVEN commits on 3e6d02d. server.js 0d7e387 -> a3db7da; model-config 35064f1 -> 6cc7986. 4274/262.
#   C — RD-819 (TIER 1, STACKED on B) rd-819-ai-config-empty-body-s89r @ fdd07af: gate range cd171f9..fdd07af (9 commits, 2 forward merges of B). server.js a3db7da -> d0ba5e8. 4282/263.
#   D — RD-807 (TIER 1, prototype-key incidents) rd-807-incidents-prototype-key-s89r @ 9b15a99: THREE commits on 4332fb0. incidents.js 740be8d -> 988969a. 4310/265.
#   E — RD-801 + RD-822 (TIER 2, two items) rd-801-feedback-log-injection-s87o @ 6613113: THREE commits on d97039f. NEW logSafe.js; feedback.js 054ab21 -> a0cb126. 4317/266.
#   F — RD-821 round 2 (TIER 2, the jest-lock TOOL): session-tools/nexusai-lock.sh sha256 fd223bd2… (installed 2026-10-06T18:05:50Z); kept copies 051f18d6… (r1) and 2c892f00… (pre).
#   G — RD-721 Icons (TIER 1, auth-gate static bypass, C-206) rd-721-icons-vendor-s91p @ 64ee309: SIX commits on 8853e36. server.js 2684acd -> c5b7ce1. 4328/269. ONE browser leg (g9).
#   THE CROSSES (C-68): server.js is changed by main's RD-618 (since B's base), B, C and G — a COMBINED blob on every merged tree carrying B; RD-697 (on main) x RD-640.
#   SLOTS — S1 (RD-761 fix round) and S2 (RD-802) join ONLY by the brief's JOINS lines (guard 89). EMPTY.
#   Main at drafting 8b7ae54 (RD-697 after RD-736 and RD-719; counts 4320/267; lock d6d3b6e). Predicted MTF 4407/276.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch19' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch19.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-19 redraft commission and her rulings file fleet/briefs_staged/2026-10-07_gate19_drafter_report_and_rulings.md (ruling 1 SUPERSEDED: RD-761 is
# slot S1; ruling 3: RD-821's placement measured with a controlled pid; ruling 4: no browser leg for RD-794). READY mails copied in briefs/. THE MODEL RULE: Kam, live board
# 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings: sqlite3 cached prebuild (2026-10-05_qa_b14_sqlite3_ANSWER.md); full verifies UNBELTED with 4 conditions (2026-10-05_qa_b14_belt_ANSWER.md);
# npm_config_update_notifier=false on EVERY npm call (2026-10-05_qa_gate16_notifier_ANSWER.md); ruling (b) — lock-starved full verifies NAMED NOT RUN
# (2026-10-06_nexusai_g18_ruling_b_deliver_now.md); the browser driver (2026-10-04_qa_batch13_browser_driver_answer.md); C-190 + its ADDENDUM: BOTH CodeQL thresholds;
# C-141 ADDENDA 6/7: --replace for re-files, only a merge HOLD's tag says "merge" (gate tags are qa-b19-*).
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert; no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (node_modules offline only, H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch18.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the LIVE
# negative-control seat derivation 38R, the ADDENDUM-SLOT JOINS parser 89, route-line and stamp guards last). CHANGES, each deliberate:
#   - SEVEN members on FIVE bases; C is STACKED on B (its range carries two forward merges) (guards 6 7 8 22 23 35 80).
#   - 93 A, 94 B, 95 C, 96 D, 97 E, 99 G: each member's premises at source; 90 (NEW): F is a FILE — the installed tool and both kept copies re-hashed.
#   - 18b: main moving and touching server.js is a NOTE; a member-ONLY path moving REFUSES; a member already on main REFUSES.
#   - 98: TWO locks (e9063d4 at A-E and their bases; d6d3b6e at M0, 8853e36, G) — checked as briefed; proxy-addr version read from each lock.
#   - 89: TWO slots (S1 RD-761 fix round — the failed PR head 72ca5d3 is refused; S2 RD-802 — must descend from E).
#   - 38R: no peer QA gate was live at drafting; any live QA/NexusAI-batch1x pane is added as a negative control.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python/shasum over `git show` output and over session-tools files; grep, ls, ps, tmux, test -e. It writes nothing and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch19.sh [--check]
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
BRIEF="$BRIEFS/2026-10-07_nexusai-gate-batch19.md"
BRIEF18="$BRIEFS/2026-10-06_nexusai-gate-batch18.md"
RULINGS19="$STAGED/2026-10-07_gate19_drafter_report_and_rulings.md"
READY_A="$BRIEFS/2026-10-07_nexusai-rd640-r2b-READY-mail.txt"
READY_B="$BRIEFS/2026-10-07_nexusai-rd794-cd171f9-READY-mail.txt"
READY_C="$BRIEFS/2026-10-07_nexusai-rd819-fdd07af-READY-mail.txt"
READY_D="$BRIEFS/2026-10-07_nexusai-rd807-READY-mail.txt"
READY_E="$BRIEFS/2026-10-07_nexusai-rd801-rd822-READY-mail.txt"
READY_F="$BRIEFS/2026-10-07_nexusai-rd821-READY-mail.txt"
READY_F2="$BRIEFS/2026-10-07_nexusai-rd821-r2-READY-mail.txt"
READY_G="$BRIEFS/2026-10-07_nexusai-rd721-icons-READY-mail.txt"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
BROWSER_ANS="$STAGED/2026-10-04_qa_batch13_browser_driver_answer.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
PBRIEF_B="$NX/qa-briefs/2026-10-06_nexusai-rd794-tier1-gate.md"
PBRIEF_C="$NX/qa-briefs/2026-10-06_nexusai-rd819-tier1-gate.md"
PBRIEF_D="$NX/qa-briefs/2026-10-07_nexusai-rd807-tier1-gate.md"
ST="$NX/session-tools"
EV_N="$ST/s87n"
EV_R="$ST/s89r"
EV_R2="$ST/s92r"
EV_O="$ST/s87o"
EV_P="$ST/s91p"
LOCKQ="$ST/locks/queue-jest"
LOCKTOOL="$ST/nexusai-lock.sh"
LOCK_R1="$ST/nexusai-lock.sh.pre-1007-o-r2"
LOCK_PRE="$ST/nexusai-lock.sh.pre-1006-o"
LOCK_SHA='fd223bd2a72d38143d0466fcbcc6762f9bc7f82815084d1a3c53422acc2d7700'
LOCK_R1_SHA='051f18d6b76d2c097040793b3f128ac86116ce5bd42c44013beae8b228d50244'
LOCK_PRE_SHA='2c892f003aa87fb85a94ad4c5357679633965a425f4d258bde08125b9cd1abe1'
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$ST/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B18_DIR="$RPTS/2026-10-06-gate-batch18"
B18_REPORT="$B18_DIR/report.md"
B18_INST="$B18_DIR/evidence/inst"
B17_REPORT="$RPTS/2026-10-06-gate-batch17/report.md"
B17_INST="$RPTS/2026-10-06-gate-batch17/evidence/inst"
B17_UNION="$RPTS/2026-10-06-gate-batch17/evidence/union-erasure.lst"
B15_REPORT="$RPTS/2026-10-05-gate-batch15/report.md"
B12_REPORT="$RPTS/2026-09-30-gate-batch12/report.md"
PREV_FLOORLIB="$B18_INST/qa-floorlib18.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-07-gate-batch19/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch19'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'

MAIN_SHA='8b7ae5451a53b85ea2805b5d98ed9f2964669d54'      # origin main at drafting (14:28:14 AEDT; RD-697 after RD-736, RD-719)
BASE_A='e944c9c50da84326e3843140c14916e833e3e213'        # A's parent: merge of main d97039f into round 1 588ec63
MB_AE='d97039fe33b2f3b63899b27d591f3317e7eaa8a0'         # merge-base(A, M0) = merge-base(E, M0)
BASE_BC='3e6d02d48876b01d43b0360026a66c78d191ed70'       # B's base = merge-base(B, M0) = merge-base(C, M0)
BASE_D='4332fb06a349b8a189e9ec70022ff9290d2fadf5'        # D's base
BASE_G='8853e3628382d3ec7fcc653cb7be7bbf210a3eda'        # G's base (RD-719's landing, on M0)
A_R2A='092ed9ef41e4c8df4167f25aa970009e9832784d'         # RD-640 round 2's first commit (WITHDRAWN as a target; a0's red arm)
S1_FAILED='72ca5d3993fd1aeb1e18e75ac6ad1278ae2edd2e'     # RD-761's FAILED PR head (PR #58) — a JOINS line naming it is refused
RD761_R1='141d7ea77242f7d56fa4b8596d4fc2ce1bb75bd3'      # RD-761 round 1 (gate 18)
A_BRANCH='rd-640-eloop-and-tree-cells-s87n'
A_HEAD="${QA_A_HEAD_OVERRIDE:-b214f6f063955f95606bf22e19afb7f076de1b4b}"
B_BRANCH='rd-794-ollama-runtime-slice-s89r'
B_HEAD="${QA_B_HEAD_OVERRIDE:-cd171f953a4cba86379b2343a5bd31f9cb74f0c1}"
C_BRANCH='rd-819-ai-config-empty-body-s89r'
C_HEAD="${QA_C_HEAD_OVERRIDE:-fdd07af0796453e581eec15b83025d39113b7447}"
D_BRANCH='rd-807-incidents-prototype-key-s89r'
D_HEAD="${QA_D_HEAD_OVERRIDE:-9b15a99bce539d8eb63a5b4bac052cd18ea45d19}"
E_BRANCH='rd-801-feedback-log-injection-s87o'
E_HEAD="${QA_E_HEAD_OVERRIDE:-661311351166ea80006e088356c179f125a3ebec}"
G_BRANCH='rd-721-icons-vendor-s91p'
G_HEAD="${QA_G_HEAD_OVERRIDE:-64ee3096c6ff81ac07d6292d61d062819458c3b5}"
S1_BRANCH='rd-761-law-endpoint-policy-s89r'
S2_HINT='rd-802'

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
SV='backend/server.js'
DE='backend/dataErasure.js'
MC='model-config.js'
LLI='backend/llm/index.js'
OLA='backend/llm/ollamaAdapter.js'
INC='backend/incidents.js'
FB='backend/routes/feedback.js'
LS='backend/logSafe.js'
T640='__tests__/rd640-eloop-and-tree-cells.test.js'
TEV='__tests__/erasure-verdict-is-derived-from-failures.test.js'
T627='__tests__/rd627a-erasure-tmp-siblings.test.js'
T794='__tests__/rd794-ollama-runtime-removed.test.js'
TPARK='__tests__/helpers/rd819-parked-NOT-RUN/rd819-w5-azure-empty-body.test.js'
T819='__tests__/rd819-ai-config-empty-body.test.js'
T807='__tests__/rd807-incidents-prototype-key.test.js'
T807P='__tests__/helpers/rd807-prototype-probe-preload.js'
T801='__tests__/rd801-feedback-log-injection.test.js'
T822='__tests__/rd822-coordinator-reason-validator.test.js'
TDOM='__tests__/helpers/dom.js'
T385='__tests__/rd385-shipped-root-markdown-identifiers.test.js'
T442='__tests__/rd442-licence-terms-of-service.test.js'
T721I='__tests__/rd721-bootstrap-icons-vendored.test.js'
T721V='__tests__/rd721-vendor-static-bypass.test.js'
T721D='__tests__/rd721-dom-harness-skips-icons.test.js'
T721J='__tests__/rd721-bootstrap-icons-1.10.0-provenance.json'
VNOT='static/vendor/THIRD-PARTY-NOTICES.txt'
VCSS='static/vendor/bootstrap-icons-1.10.0/font/bootstrap-icons.css'
VW2='static/vendor/bootstrap-icons-1.10.0/font/fonts/bootstrap-icons.woff2'
VW1='static/vendor/bootstrap-icons-1.10.0/font/fonts/bootstrap-icons.woff'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
DKF='Dockerfile'
DIG='.dockerignore'
ICON_PAGES='admin chart-details feedback-admin first-run-setup index legal login settings testing'

DE_M_BLOB='1f708e276482e5224ab9793d878e59ed0867b125'     # d97039f, M0
DE_R1_BLOB='6002d71c21f552ee4e745fda98053fec7c845471'    # e944c9c (round 1)
DE_R2A_BLOB='110ad2b9b28f0ed2e3a2d65b1d888822153d9228'   # 092ed9e
DE_A_BLOB='343348df5476a4d8a434c469c64253a8618e92cc'
T640_BLOB='a8175604945a16e86ee04c18d26221c624dd1031'
TEV_M_BLOB='4b75b241b3f039810f2e9ab5f6619f3b6da0928c'
TEV_A_BLOB='13c4d6356f39e687ec537a076a5df913818f040c'
T627_A_BLOB='9ea9de9e9b5a03c73452a0bbfe92ac1129376554'   # A's (pre-RD-697)
T627_M_BLOB='fa16069f5e0a99954f7048ce4a78f9d803d19cf6'   # M0 (RD-697)
SV_Z_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'     # 3e6d02d
SV_M_BLOB='2684acda2190ac2578008f8055a131fe6cd9a7f1'     # M0, 8853e36, d97039f, 4332fb0, A, D, E
SV_B_BLOB='a3db7da12cbdf43518ba386a3f58d465bb9534db'
SV_C_BLOB='d0ba5e8dcfbb7522dd25d18fde96308380f8e8d2'
SV_G_BLOB='c5b7ce164fa9ea79768fba715b5f79a9220616bb'
MC_M_BLOB='35064f155d63df40b8097515bef219fb63b1025d'
MC_B_BLOB='6cc798694135732f708b967dbdd167c83ed0cefa'
LLI_M_BLOB='db23e47a4b6ba5f316f25ec0624077738360abd1'
LLI_B_BLOB='f0e377de16023776b061408268ccd7d405569216'
OLA_M_BLOB='ea7f177bbaa0a8090daad331c795d85b32b2c173'
T794_BLOB='d3df8be945d7f3a89a115a049871a377c404affe'
TPARK_BLOB='550d6c9da3e3c84f754d7c859ea7ff06217d2fdb'
T819_BLOB='9064371fa094a2cf42f82a9706bdf8c62c5b632a'
INC_M_BLOB='740be8d51afcce97db77169e1bdcc8580f652f05'
INC_D_BLOB='988969aa46ea3e4e185d92eeeadeb85ac42c9340'
T807_BLOB='16cfdeb1e0e150b2ac69092242a2c970a901b03d'
T807P_BLOB='6f6b8a1f0cfdb999bb805c18c6e15198dfa8f83f'
FB_M_BLOB='054ab21719f7ca9655e7966dac9f18ddf421b5bf'
FB_E_BLOB='a0cb126f7946958cea4307c9073b8dc522b722b2'
LS_E_BLOB='196ab46a8a333a6e3ccd8489ce7bc371e6f77dae'
T801_BLOB='a3723511db938a874516805e81d3a74caea1581d'
T822_BLOB='50bc66f354ef55d07f6eea375abe5d30d7484bba'
TDOM_M_BLOB='3f913ff542d504c6f642f582c86d6d8711f1689f'
TDOM_G_BLOB='fbba61fd6c412fbe3827237fab54796c4d04c2ff'
T385_M_BLOB='d1b26f30e1816c231b1654ca00ba314d468cb217'
T385_G_BLOB='88e87132e41066de4f71dcbb8c6bb75cda2d4bd8'
T442_M_BLOB='8778a71cc5bcb6489f644a8766e256d4ff91c174'
T442_G_BLOB='32006e8390b50b265442404693f75bf325db41e3'
T721I_BLOB='8fc8abab6895922c8d7d04d57c10644c90c75419'
T721V_BLOB='4815dff4337423eba0fd0c9df2f5c3b6efa65a54'
T721D_BLOB='96c37ebfeb6c087213c5f25f7d1b480318313fcf'
T721J_BLOB='7ad63f9327a9fdb72f6d291971f74037d411b617'
VNOT_BLOB='ceb72a1691116afd54abd5f41c0b579ae1daf270'
VCSS_BLOB='7d93a97888561db08eb7a166abad952824374186'
VW2_BLOB='52b12533e4da87cb83e50039430cd027b48f931a'
VW1_BLOB='18d21d457558d4dc2e231a8f6ee585fada9c6bab'
LOGIN_M_BLOB='89be2caf4d1b553cf63c8252825eafa484594602'
LOGIN_G_BLOB='11046a786be18bb5e02747661da2d13f554a175d'
LOCK_OLD='e9063d44757007324b8c55fa58c03c03dfe552ae'        # 3e6d02d, d97039f, 4332fb0, A-E (proxy-addr 2.0.7)
LOCK_NEW='d6d3b6e42aa604320f3b70f8e9048bfac044f277'        # 8853e36, M0, G (proxy-addr 2.0.8)
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'
TSH_BLOB='f612fb4815aaa358795acc977d59a0a9cba09670'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
R549_BLOB='4a3564265683f936c99e69789049e3dd5dff9b3b'
R465_BLOB='f16b811756f70ddcd37ec43197383c5434cff6e4'
DE_A_SHA16='cc5630b5c810a702'                               # sha256 prefix of 343348d's content (N's "proven sha")
R385_HASH='7606fba789de0cb79081df3ecf2002b8e7c73da0d5157d54b0537161fe21db15'

A_EXPECTED_FILES="$DE
$T640
$COUNTS_FILE"
B_EXPECTED_FILES="__tests__/helpers/rd395-llm-mock-preload.js
$TPARK
__tests__/llm-provider-default-azure-openai.test.js
__tests__/rd395-ai-enabled-gate.test.js
__tests__/rd395-ai-enabled-writer.test.js
__tests__/rd395-ai-toggle-write.test.js
__tests__/rd395-raw-model-calls.test.js
__tests__/rd423-test-ai-does-not-crash-server.test.js
$T794
__tests__/security-fixes.test.js
$LLI
$OLA
$SV
$MC
$COUNTS_FILE"
C_EXPECTED_FILES="$TPARK
$T819
$SV
$COUNTS_FILE"
D_EXPECTED_FILES="$T807P
$T807
$INC
$COUNTS_FILE"
E_EXPECTED_FILES="$T801
$T822
$LS
$FB
$COUNTS_FILE"
G_EXPECTED_FILES="$TDOM
$T385
$T442
$T721J
$T721I
$T721D
$T721V
$SV
$COUNTS_FILE
static/admin.html
static/chart-details.html
static/feedback-admin.html
static/first-run-setup.html
static/index.html
static/legal.html
static/login.html
static/settings.html
static/testing.html
$VNOT
$VCSS
$VW1
$VW2"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 19'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch19] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any member head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Ollama runtime or Azure OpenAI endpoint, a real Entra tenant or token, real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, CDN requests aborted), the live jest queue under RD-821's arms (scratch bases only), a real customer volume (network mounts, other filesystems), Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), a real Telegram coordinator, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
titles() { g show "${1}:${2}" 2>/dev/null | grep -E '^[[:space:]]*(test|it)(\.each\(.*\))?\(' | sed -E 's/^[[:space:]]+//'; }   # test/it lines only (b8's title diff)
sha16() { g show "${1}:${2}" 2>/dev/null | shasum -a 256 | cut -c1-16; }
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
conflicts() { local b; b="$(g merge-base "$1" "$2" 2>/dev/null)" || return 1
  g merge-tree "$b" "$1" "$2" 2>/dev/null | awk '/^  (base|our|their) /{f=$4} /^\+<<<<<<</{c[f]=1} END{for(k in c) print k}' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 19", with SEVEN members and TWO ADDENDUM SLOTS, one verdict per ticket and ONE report. It is a FRESH gate. The members: RD-640 round 2 of 2 (TIER 1, data erasure, NexusAI-N S87N: on an ELOOP the erasure walks the link chain hop by hop, resolving each hop's directory the kernel's way and keying loops by device and inode; a chain that ends at real data is KEPT as a named failure, a proven loop or a chain to nothing is removed and recorded purged; C-139 ADDENDA 2 and 3; round 2 of 2, so a NO GO ships nothing on this class), RD-794 (TIER 1, NexusAI-R S92R: the runtime Ollama path is removed — adapter, LLM case, ai-test and ai-config Ollama branches, the Ollama allow-list — and an unknown or prototype-named LLM_PROVIDER resolves by an own-key lookup to azure-openai with ONE boot warning; C-51, C-203), RD-819 (TIER 1, STACKED on RD-794, gate range cd171f9..fdd07af: an ai-config body that would store no AI setting is refused 400 NOTHING_TO_SAVE before any write; never merges alone, C-199 ADDENDUM), RD-807 (TIER 1, NexusAI-R: incident ids are looked up as own keys only and the three prototype names are never ids), RD-801 and RD-822 (TIER 2 through code, NexusAI-O, TWO separate items and TWO verdicts: four feedback log lines neutralised by a new logSafe helper, and the coordinator-reason validator corrected so spaced reasons are accepted and control characters refused), RD-821 round 2 (TIER 2 through code, NexusAI-O: the jest-lock TOOL itself, already installed, judged by its sha256 — a same-place handover by --replace and merge-first placement that never passes a gate), and RD-721 round 1 Icons (TIER 1, NexusAI-P S91P: Bootstrap Icons vendored same-origin and /vendor/ added to the auth gate's static-asset bypass, inert extensions only, C-206; it carries the ONE local browser leg). The server entry point is changed by main's RD-618 since RD-794's base, by RD-794, by RD-819 and by RD-721, so a COMBINED blob is predicted on every merged tree carrying RD-794, and RD-697 (now on main) meets RD-640's product: this gate carries THE CROSSES (C-68). The SLOTS (S1: RD-761's fix round; S2: RD-802, stacked on RD-801) are members ONLY if the brief carries their JOINS lines — the launcher tells you below. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its head AND the merged tree. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry, and no browser except the ONE local browser leg the brief names (g9).

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-07_nexusai-gate-batch19.md
It opens with the drafter's WRONG OR UNVERIFIED list (every place a READY or project brief contradicts the source, each marked MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1-T9 as Tuesday stamped them, and the carried rulings (a) to (q)) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the seven READY mails it names (read each WHOLE; RD-821's on disk is ROUND 1's, and round 2's claims are C-141 ADDENDUM 6's ROUND 2 paragraph and the s87o r2 logs, as T3 rules), R's project-side briefs for RD-794, RD-819 and RD-807 (read WHOLE), the clarifications the brief names at source, the gate-17 report (RD-640's prior round), the gate-18 report and stamped brief (the structural template, ruling (b), and RD-761's prior round) and the gate-15 report (RD-721's neighbour). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window; adversarial rows are written as the property, the input shape and the expected result — you write your own drivers.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones — every one is an authorised, findings-only measurement of Datasec's own product in your own trees, your own loopback servers, your own mktemp dirs and your own scratch lock bases; no row contacts a non-loopback address and no row touches the live jest queue except your own holds through the tool. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-640: rd-640-eloop-and-tree-cells-s87n at b214f6f063955f95606bf22e19afb7f076de1b4b (TWO commits on e944c9c50da84326e3843140c14916e833e3e213, itself a forward merge of main d97039fe33b2f3b63899b27d591f3317e7eaa8a0 into round 1; 092ed9ef41e4c8df4167f25aa970009e9832784d is WITHDRAWN as a target and is a0's red arm; counts 4317/265). RD-794: rd-794-ollama-runtime-slice-s89r at cd171f953a4cba86379b2343a5bd31f9cb74f0c1 (SEVEN commits on 3e6d02d48876b01d43b0360026a66c78d191ed70; counts 4274/262). RD-819: rd-819-ai-config-empty-body-s89r at fdd07af0796453e581eec15b83025d39113b7447 (nine commits over RD-794's head, two of them forward merges of RD-794; counts 4282/263). RD-807: rd-807-incidents-prototype-key-s89r at 9b15a99bce539d8eb63a5b4bac052cd18ea45d19 (THREE commits on 4332fb06a349b8a189e9ec70022ff9290d2fadf5; counts 4310/265). RD-801 and RD-822: rd-801-feedback-log-injection-s87o at 661311351166ea80006e088356c179f125a3ebec (THREE commits on d97039f; counts 4317/266). RD-821: the installed session-tools/nexusai-lock.sh at sha256 fd223bd2a72d38143d0466fcbcc6762f9bc7f82815084d1a3c53422acc2d7700 (round 1 kept as nexusai-lock.sh.pre-1007-o-r2, sha256 051f18d6b76d2c097040793b3f128ac86116ce5bd42c44013beae8b228d50244). RD-721: rd-721-icons-vendor-s91p at 64ee3096c6ff81ac07d6292d61d062819458c3b5 (SIX commits on 8853e3628382d3ec7fcc653cb7be7bbf210a3eda, RD-719's landing; counts 4328/269). No member has a builder full verify OF ITS HEAD (brief WRONG 10): yours decides. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (the brief's proposed order MT-A 4339/268, MT-D 4350/269, MT-E 4369/271, MT-G 4390/274, MT-B 4399/275, MTF 4407/276; predicted at M0 = 8b7ae5451a53b85ea2805b5d98ed9f2964669d54, 4320/267), the tests census (324 at MTF), new ids 96, missing EXACTLY the 9 ids of RD-794's C-133 table (8 renamed + W5 moved), each C-133-accounted, and missing 0 for every other member. If a member, RD-761's fix round or RD-802 is in your M0, re-derive every C-68 set on it (y7) and mail a QUESTION. Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Every READY says no PR exists until the merge turn: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY (the repo is datasecau/Reporting_Dashboard_Au). If S1 joins, its verdict condition includes PR #58's CodeQL run clearing alerts #256-#259. A red npm-audit at a head built before RD-816 (90b2556) is proxy-addr GHSA-jqcg-44mw-7w3h only — name it. C-185 on M0 (ruling h): the known-failing set is {rd549 O4, rd549 C2/C10 — each only when envReached alone differs}; ANY rd465 O-1 failure on M0, a head or a merged tree is a STOP; any other rd549 failure on a tree carrying RD-794 or RD-819 is a STOP; a known-set failure is named and classified, never waved; no re-run is a clearance.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-640: a0 RED-AT-PARENT first (W1 and W2 red at 092ed9e's product); a2 the errno and the walk measured first; a3 THE NEVER-FOLLOW ROW at all four levels with a modified COPY target as the control; a4 THE F1/W ROW (chains that end at real data kept and named, loops including the directory-link loop and chains to nothing removed and purged); a5 the walk's edges; a6 F2; a7 F3; a8 Y5; a9 where the absolute end path lands; a10 the builder's six mutants re-derived on the whole union plus your own; a11 C-68 with RD-697's cells; a12 manifest evaluation, NO image built; a13 CodeQL READ ONLY; a14 prior work. RD-794: b0 RED-AT-PARENT; b2 THE NOTHING-DIALS ROW — your own loopback listener named as the Ollama endpoint in ai-test and ai-config bodies, at boot and from a stored upgraded store, with the base arm reaching it as the control; b3 the provider and the one warning across known, unknown, prototype-named and control-character values; b4 getModelByName; b5 the remainder sites (service-status, models/health, validate-all on onnx-local — brief WRONG 1-4); b6 an upgraded deployment; b7 the re-anchored cells bite their mutants; b8 the 9 missing ids under C-133; b9 C-68. RD-819: c0 RED-AT-PARENT; c2 THE NO-WRITE ROW in the open window, the RD-437 state and a configured deployment, the store hashed before and after and a confirmed config still confirmed; c3 non-string values; c4 real bodies unchanged; c5 M819 and M819-trim; c6 the moved cell; c7 C-199 ADDENDUM's conditions. RD-807: d0 RED-AT-PARENT; d2 THE PROTOTYPE ROW — prototype-named ids at the real routes, the server process's own prototype state read by a test-only probe preload, the base arm polluting as the control; d3-d7. RD-801 and RD-822: e0 RED-AT-PARENT; e2 no forged log line from any control character; e3 logSafe never throws; e4 the validator; e5 the mutants; e6 C-68; e7 the other console lines. RD-821: f0 COPIES AND THE BASE GUARD first (the tool defaults to the LIVE base — every arm asserts its base is yours); f1 every round-2 arm on all three tool versions; f2 --replace; f3 THE PLACEMENT ROW — a merge filed against a gate and a builder in every ns geometry (gap of two or more, one, and zero) with controlled pids, never passing the gate (brief WRONG 13; Tuesday's ruling 3); f4 the tag reader; f5 the exit-3 race; f6 RD-755; f7 the live install READ ONLY. RD-721: g0 RED-AT-PARENT; g2 the vendored bytes; g3 THE BYPASS ROW — a real server with auth ENFORCED by a seeded store, anonymous requests for inert, non-inert and path-shaped /vendor/ requests sent literally, never a gated body, a non-inert file or a file outside static; g4 session activity; g5 the guards are exact (the notices exclusion, the rd385 reviewed entry, the skip list); g6 the twelve mutants plus your own; g7 the jsdom harness; g8 C-68; g9 THE BROWSER LEG; g10 manifest evaluation. THE CROSSES: y1 the server entry point combined (RD-618, RD-721, RD-794, RD-819); y2 RD-697 x RD-640; y3 both orders; y4 the locks; y5 RD-721 x RD-794's AI pages; y6 C-185; y7 main moved; y8 the shipped set.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff in Tuesday's ruled order (T1; the proposal: RD-640 MT-A, RD-807 MT-D, RD-801/822 MT-E, RD-721 MT-G, RD-794 MT-B, RD-819 MTF; S2 right after RD-801/822 and S1 right before RD-794 if they join). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MTF on node_modules proven for M0's lock d6d3b6e with proxy-addr 2.0.8 read from the tree's own path (RD-827, C-205): predicted 4407/276, re-based on YOUR M0; the measurement decides. A second clone in the reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes); the shared C-57 tool's "failed" count reads the install, not the tree (RD-827) — the id-superset verdict is the property. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes package.json or the lock. TWO locks (T2): e9063d4 (proxy-addr 2.0.7) at RD-640, RD-794, RD-819, RD-807 and RD-801/822; d6d3b6e (proxy-addr 2.0.8) at M0, RD-721 and every merged tree. There is NO npm registry exception in this gate. ONCE PER LOCK: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline — and EVERY npm invocation, the first one included, carries npm_config_update_notifier=false; prove the cache copy's _update-notifier-last-checked marker absent or unchanged. An ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install, never npm audit, never npx playwright install. sqlite3's binding: the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in your tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on it is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree of the same lock; never from another gate's trees.

THE BROWSER LEG (ruling q, H-32): Playwright 1.62.1 from YOUR OWN tree's node_modules, channel chrome (the local Google Chrome), HEADLESS, NO browser download — prove ~/Library/Caches/ms-playwright unchanged before and after; only http://127.0.0.1:<port> of a server YOU booted from YOUR tree with auth ENFORCED by a seeded store (T7), SESSION_SECRET UNSET; every non-127.0.0.1 request aborted by the page route AND the belt (login's Bootstrap CSS comes from a CDN and will not load — name it, never a finding against RD-721); measure icon glyphs by computed style and the vendored requests' status, not pixels; every caption "local run of <sha>, auth ENFORCED by a seeded store — NOT the demo; Chrome headless via Playwright 1.62.1". If Chrome or Playwright cannot launch, g9 is NOT RUN, named — never replaced by a jsdom render. The ONE kind of preload you may load into a server you boot is a TEST-ONLY probe that reads the server's own prototype state (d2), by -r in argv, with its landing control.

FULL VERIFY of each head and of MTF through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers, servers, the browser), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted b214f6f 4317/265, cd171f9 4274/262, fdd07af 4282/263, 9b15a99 4310/265, 6613113 4317/266, 64ee309 4328/269, MTF 4407/276. RULING (b) (Tuesday to gate 18, carried as ruling (o)): if ONLY the full verifies or the counts regeneration remain lock-starved about 2 h after filing, deliver with them NAMED NOT RUN — never "skipped" — and say in the NOT TESTED section that each member's merge hold full verify plus its PR's CI Build are the gate's NOT-RUN full verify, and any red there outside C-185's known set at merge is a STOP, not a re-run. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed BEFORE; every boot and every purge is a NEW process — declare it per row. H-3: a LANDING CONTROL for every link, loop, chain, chmod, outside target, stored value, listener, probe, controlled pid and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd; link texts read back with readlink; request bodies and raw paths byte-exact from a file. H-15: preloads with -r in argv; the ONE kind allowed is the read-only prototype probe. H-16: every plant checked to be what the product will treat it as. H-17: your own censuses use pgrep, never ps; RD-821's arms need the tool's own ps and run outside the belt (they open no socket). H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate, and every chmod you make, is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output; each hold carries a wait deadline, and BEFORE it fires you file --replace on your own still-waiting ticket under the SAME tag. H-29: other gates' evidence is method only. H-31: offline node_modules per lock, the notifier off, and the cached sqlite3 prebuild. H-32: NO image built (the shipped-blob rows are a manifest evaluation); ONE local browser leg. H-33: links, loops, outside targets, listeners, scratch lock bases, chmod'd dirs and children counted and reaped or quarantined, never rm; a link you plant never points outside your own mktemp dirs. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch19.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; other gates' trees and report dirs are never touched; copy instruments BY COPY from gate 18's evidence/inst (its HOLD18.sh hard-codes its own evidence dir and its qa-floorlib18.sh carries stale ROOT and NEG defaults: re-point and correct your copies; its qa-file18.sh predates RD-821, so your re-file instrument is your own, built on --replace) and gate 17's erasure instruments for RD-640. RD-821's harnesses hard-code their ROOT under session-tools: copy them, re-point ROOT to your own dir, and give every arm a FRESH NEXUSAI_LOCK_BASE of your own. In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, probe, measure, screen, mutate or lock-arm scripts in place. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no Microsoft host, no Ollama host, no CDN, no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with the builder seats (any live QA/NexusAI-batch1x pane is a PEER gate: FIFO, never touched); merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, plain-node, server, browser and lock-arm rows, census greps); then file your holds tagged qa-b19-, one at a time; no tag of yours contains the word "merge" (C-141 ADDENDUM 7: only a merge HOLD's tag does). If a MERGE ticket is queued ahead of you, wait behind it; if one files BEFORE your grant, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG). AT A WAIT DEADLINE, first in line or not: use --replace on your own still-waiting ticket BEFORE its deadline fires (C-141 ADDENDUM 6: a SAME-PLACE handover; it is refused once the old waiter has left, so a late re-file lands at the tail) and confirm from the queue listing that the old ticket went to released/ as ticket-left-* and your place is unchanged; never two live holds; a duplicate-tag refusal takes a -r<N> suffix, said in the report; you never move ahead of anything that was ahead of you; one report line per re-file with the queue place before and after FROM THE QUEUE LISTING. Once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result, including every server you boot outside a hold; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver, server, browser arm, lock arm, purge process and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the six member branches and main (and each SLOT's branch if it joins) — three timestamped readings with the branch name and attempt count beside each sha — and RD-821's installed sha256 three times. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so; it must be 8b7ae54 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch19. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch19] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 19
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-640 @ b214f6f, RD-794 @ cd171f9, RD-819 @ fdd07af, RD-807 @ 9b15a99, RD-801 and RD-822 @ 6613113 as two lines, RD-821 by its sha256, RD-721 @ 64ee309 with the browser leg; a SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured in both orders, the C-57 and C-133 result, the combined server-entry-point blob id, THE CROSSES, which rows ran on Opus 4.8 (or none), which full verifies ran and which are NAMED NOT RUN under ruling (b), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR)". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A8, L-B1 to L-B11, L-C1 to L-C8, L-D1 to L-D6, L-E1 to L-E5, L-F1 to L-F7, L-G1 to L-G8 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-139 with its ADDENDA 2 and 3, C-141 with ADDENDA 5, 6 and 7, C-199 with its ADDENDUM, C-203 with its ADDENDA, C-51, C-130, C-131, C-14 with its ADDENDUM, C-206, C-205, C-185 with its ADDENDA, C-190 with its ADDENDUM and C-192 are the clarifications this batch leans on; C-49, C-57, C-68, C-76, C-89, C-97, C-102, C-104, C-112, C-115, C-125, C-133, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any member head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Ollama runtime or Azure OpenAI endpoint, a real Entra tenant or token, real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, CDN requests aborted), the live jest queue under RD-821's arms (scratch bases only), a real customer volume (network mounts, other filesystems), Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), a real Telegram coordinator, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$BASE_A" "$MB_AE" "$BASE_BC" "$BASE_D" "$BASE_G" "$A_R2A" "$S1_FAILED" "$RD761_R1" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases with main and the stack.
mb_is() { [ "$(g merge-base "$1" "$2" 2>/dev/null)" = "$3" ]; }
mb_is "$A_HEAD" "$MAIN_SHA" "$MB_AE"   || { echo "REFUSING: merge-base(RD-640, 8b7ae54) is not d97039f — re-brief" >&2; exit 7; }
mb_is "$B_HEAD" "$MAIN_SHA" "$BASE_BC" || { echo "REFUSING: merge-base(RD-794, 8b7ae54) is not 3e6d02d — re-brief" >&2; exit 7; }
mb_is "$C_HEAD" "$MAIN_SHA" "$BASE_BC" || { echo "REFUSING: merge-base(RD-819, 8b7ae54) is not 3e6d02d — re-brief" >&2; exit 7; }
mb_is "$D_HEAD" "$MAIN_SHA" "$BASE_D"  || { echo "REFUSING: merge-base(RD-807, 8b7ae54) is not 4332fb0 — re-brief" >&2; exit 7; }
mb_is "$E_HEAD" "$MAIN_SHA" "$MB_AE"   || { echo "REFUSING: merge-base(RD-801/822, 8b7ae54) is not d97039f — re-brief" >&2; exit 7; }
mb_is "$G_HEAD" "$MAIN_SHA" "$BASE_G"  || { echo "REFUSING: merge-base(RD-721, 8b7ae54) is not 8853e36 — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$B_HEAD" "$C_HEAD" 2>/dev/null || { echo "REFUSING: RD-794 cd171f9 is not an ancestor of RD-819 — the stack moved (C-199 ADDENDUM); re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$MB_AE" "$BASE_A" 2>/dev/null && g merge-base --is-ancestor "$BASE_G" "$MAIN_SHA" 2>/dev/null \
  || { echo "REFUSING: d97039f is not under e944c9c, or 8853e36 is not on 8b7ae54 — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$A_R2A" "$A_HEAD" 2>/dev/null || { echo "REFUSING: 092ed9e is not an ancestor of RD-640's head (a0's red arm)" >&2; exit 7; }

# 8 — chains exact: A 2 on e944c9c; B 7 on 3e6d02d; C 9 (2 merges) on cd171f9; D 3; E 3; G 6.
chain_ok() { local base="$1" head="$2" n="$3" mg="$4" got m
  got="$(g rev-list --count "${base}..${head}" 2>/dev/null)"; m="$(g rev-list --merges --count "${base}..${head}" 2>/dev/null)"
  [ "$got" = "$n" ] && [ "$m" = "$mg" ] && g merge-base --is-ancestor "$base" "$head" 2>/dev/null; }
chain_ok "$BASE_A" "$A_HEAD" 2 0  || { echo "REFUSING: RD-640 is not TWO non-merge commits on e944c9c" >&2; exit 8; }
chain_ok "$BASE_BC" "$B_HEAD" 7 0 || { echo "REFUSING: RD-794 is not SEVEN non-merge commits on 3e6d02d" >&2; exit 8; }
chain_ok "$B_HEAD" "$C_HEAD" 9 2  || { echo "REFUSING: RD-819 is not NINE commits (two forward merges) on cd171f9" >&2; exit 8; }
chain_ok "$BASE_D" "$D_HEAD" 3 0  || { echo "REFUSING: RD-807 is not THREE non-merge commits on 4332fb0" >&2; exit 8; }
chain_ok "$MB_AE" "$E_HEAD" 3 0   || { echo "REFUSING: RD-801/822 is not THREE non-merge commits on d97039f" >&2; exit 8; }
chain_ok "$BASE_G" "$G_HEAD" 6 0  || { echo "REFUSING: RD-721 is not SIX non-merge commits on 8853e36" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the six member branches exactly the pins (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "refs/heads/$D_BRANCH" "refs/heads/$E_BRANCH" "refs/heads/$G_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD" "$G_BRANCH $G_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY move (ruling b). It must be 8b7ae54 or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member-ONLY path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 8b7ae54 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
ONLY_PATHS="$(printf '%s\n' "$DE" "$MC" "$LLI" "$OLA" "$INC" "$FB" "$LS" "$T640" "$TEV" "$T794" "$TPARK" "$T819" "$T807" "$T807P" "$T801" "$T822" "$TDOM" "$T385" "$T442" "$T721I" "$T721V" "$T721D" "$T721J" "$VNOT" "$VCSS" "$VW1" "$VW2" "$PKG" | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ONLY_PATHS") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
HITS="$(printf '%s\n' "$MOVED" | grep -E '^static/[a-z-]+\.html$' | tr '\n' ' ')"
[ -z "$HIT" ] || { echo "REFUSING: main moved 8b7ae54..${M_ORIGIN:0:7} and touched a member-only path: $HIT — re-brief" >&2; exit 18; }
[ -z "$HITS" ] || echo "NOTE: main's movement touches static pages ${HITS}— RD-721's nine pages may combine; the gate measures (y7)" >&2
HITB="$(comm -12 <(printf '%s\n' "$SV" "$LOCK" "$TS" "$TSH" "$R465" "$R549" "$DKF" "$DIG" "$T627" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the combined server entry point / C-68 sets / node_modules proofs run on M0's blobs (brief ruling b, y7)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 8b7ae54) — the gate re-pins M0 itself and re-bases every prediction" >&2
if g merge-base --is-ancestor "$S1_FAILED" "$M_ORIGIN" 2>/dev/null; then echo "NOTE: RD-761 (72ca5d3 or a descendant) is now on origin main — slot S1 cannot join; y7 applies" >&2; fi
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no package change; product paths as commissioned.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$BASE_A" "$A_HEAD" "$A_EXPECTED_FILES" "RD-640 (e944c9c..b214f6f)"
chk_delta "$BASE_BC" "$B_HEAD" "$B_EXPECTED_FILES" "RD-794 (3e6d02d..cd171f9)"
chk_delta "$B_HEAD" "$C_HEAD" "$C_EXPECTED_FILES" "RD-819 (cd171f9..fdd07af)"
chk_delta "$BASE_D" "$D_HEAD" "$D_EXPECTED_FILES" "RD-807 (4332fb0..9b15a99)"
chk_delta "$MB_AE" "$E_HEAD" "$E_EXPECTED_FILES" "RD-801/822 (d97039f..6613113)"
chk_delta "$BASE_G" "$G_HEAD" "$G_EXPECTED_FILES" "RD-721 (8853e36..64ee309)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$BASE_A" "$A_HEAD" "$DE")" = "68 4" ] && [ "$(ns "$BASE_A" "$A_HEAD" "$T640")" = "209 0" ] || { echo "REFUSING: RD-640's numstats are not dataErasure +68/-4, rd640 +209 (WRONG-list premise)" >&2; exit 22; }
[ "$(ns "$BASE_BC" "$B_HEAD" "$SV")" = "11 103" ] && [ "$(ns "$BASE_BC" "$B_HEAD" "$MC")" = "28 97" ] && [ "$(ns "$BASE_BC" "$B_HEAD" "$OLA")" = "0 172" ] \
  && [ "$(ns "$BASE_BC" "$B_HEAD" "$LLI")" = "0 4" ] && [ "$(ns "$BASE_BC" "$B_HEAD" "$T794")" = "180 0" ] && [ "$(ns "$BASE_BC" "$B_HEAD" "$TPARK")" = "115 0" ] \
  || { echo "REFUSING: RD-794's numstats are not as briefed (§1)" >&2; exit 22; }
[ "$(ns "$B_HEAD" "$C_HEAD" "$SV")" = "18 0" ] && [ "$(ns "$B_HEAD" "$C_HEAD" "$T819")" = "186 0" ] && [ "$(ns "$B_HEAD" "$C_HEAD" "$TPARK")" = "0 115" ] \
  || { echo "REFUSING: RD-819's numstats are not server.js +18/-0, rd819 +186, parked -115 (WRONG 5's premise)" >&2; exit 22; }
[ "$(ns "$BASE_D" "$D_HEAD" "$INC")" = "15 2" ] && [ "$(ns "$BASE_D" "$D_HEAD" "$T807")" = "148 0" ] && [ "$(ns "$BASE_D" "$D_HEAD" "$T807P")" = "37 0" ] \
  || { echo "REFUSING: RD-807's numstats are not incidents +15/-2, rd807 +148, probe +37" >&2; exit 22; }
[ "$(ns "$MB_AE" "$E_HEAD" "$LS")" = "43 0" ] && [ "$(ns "$MB_AE" "$E_HEAD" "$FB")" = "9 5" ] && [ "$(ns "$MB_AE" "$E_HEAD" "$T801")" = "149 0" ] && [ "$(ns "$MB_AE" "$E_HEAD" "$T822")" = "100 0" ] \
  || { echo "REFUSING: RD-801/822's numstats are not logSafe +43, feedback +9/-5, rd801 +149, rd822 +100" >&2; exit 22; }
[ "$(ns "$BASE_G" "$G_HEAD" "$SV")" = "6 1" ] && [ "$(ns "$BASE_G" "$G_HEAD" "$VCSS")" = "2018 0" ] && [ "$(ns "$BASE_G" "$G_HEAD" "$VNOT")" = "63 0" ] && [ "$(ns "$BASE_G" "$G_HEAD" "$T385")" = "1 0" ] \
  || { echo "REFUSING: RD-721's numstats are not server.js +6/-1, css +2018, notices +63, rd385 +1" >&2; exit 22; }
for PAIR in "$A_HEAD $MB_AE" "$B_HEAD $BASE_BC" "$C_HEAD $BASE_BC" "$D_HEAD $BASE_D" "$E_HEAD $MB_AE" "$G_HEAD $BASE_G"; do
  H="${PAIR%% *}"; Bz="${PAIR#* }"
  [ -z "$(g diff --name-only "$Bz" "$H" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} changes package-lock.json/package.json over its base — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
prod() { g diff --name-only "$1" "$2" -- backend static docs Dockerfile .dockerignore .github "$MC" 2>/dev/null | sort; }
[ "$(prod "$MB_AE" "$A_HEAD")" = "$DE" ] || { echo "REFUSING: RD-640 touches a product path beyond $DE" >&2; exit 22; }
[ "$(prod "$BASE_BC" "$B_HEAD")" = "$(sorted "$LLI
$OLA
$SV
$MC")" ] || { echo "REFUSING: RD-794 touches a product path beyond the llm index/adapter, the server entry point and model-config (static/ included)" >&2; exit 22; }
[ "$(prod "$B_HEAD" "$C_HEAD")" = "$SV" ] || { echo "REFUSING: RD-819 touches a product path beyond the server entry point" >&2; exit 22; }
[ "$(prod "$BASE_D" "$D_HEAD")" = "$INC" ] || { echo "REFUSING: RD-807 touches a product path beyond $INC" >&2; exit 22; }
[ "$(prod "$MB_AE" "$E_HEAD")" = "$(sorted "$LS
$FB")" ] || { echo "REFUSING: RD-801/822 touches a product path beyond logSafe.js and routes/feedback.js" >&2; exit 22; }
[ "$(prod "$BASE_G" "$G_HEAD" | grep -v '^static/' )" = "$SV" ] || { echo "REFUSING: RD-721 touches a non-static product path beyond the server entry point" >&2; exit 22; }

# 93 — RD-640's premises at source.
[ "$(blob "$MB_AE" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$DE")" = "$DE_M_BLOB" ] && [ "$(blob "$BASE_A" "$DE")" = "$DE_R1_BLOB" ] \
  && [ "$(blob "$A_R2A" "$DE")" = "$DE_R2A_BLOB" ] && [ "$(blob "$A_HEAD" "$DE")" = "$DE_A_BLOB" ] && [ "$(blob "$A_HEAD" "$T640")" = "$T640_BLOB" ] \
  && [ "$(blob "$MAIN_SHA" "$TEV")" = "$TEV_M_BLOB" ] && [ "$(blob "$A_HEAD" "$TEV")" = "$TEV_A_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T640")" ] \
  && [ "$(blob "$A_HEAD" "$T627")" = "$T627_A_BLOB" ] && [ "$(blob "$MAIN_SHA" "$T627")" = "$T627_M_BLOB" ] \
  || { echo "REFUSING: RD-640's blobs are not as briefed (1f708e2 / 6002d71 / 110ad2b -> 343348d; rd640 a817560; erasure-verdict 4b75b24 -> 13c4d63; rd627a 9ea9de9 at A vs fa16069 at M0)" >&2; exit 93; }
[ "$(sha16 "$A_HEAD" "$DE")" = "$DE_A_SHA16" ] || { echo "REFUSING: N's proven sha cc5630b5c810a702 no longer matches 343348d (WRONG 10's premise)" >&2; exit 93; }
for T in 'const id = `${st.dev}:${st.ino}`;' 'cur = path.join(fs.realpathSync(path.dirname(cur)), path.basename(cur));' 'function _walkLinkChain(p) {' 'const LINK_WALK_LIMIT = 256;'; do
  [ "$(cnt "$A_HEAD" "$DE" "$T")" = "1" ] || { echo "REFUSING: dataErasure.js at b214f6f lacks '$T' exactly once (a2/a4's premise)" >&2; exit 93; }
done
[ "$(cnt "$A_R2A" "$DE" 'cur = path.join(fs.realpathSync(path.dirname(cur)), path.basename(cur));')" = "0" ] && [ "$(cnt "$MAIN_SHA" "$DE" 'function _walkLinkChain(p) {')" = "0" ] \
  || { echo "REFUSING: 092ed9e already has the kernel walk, or M0 has _walkLinkChain (a0's premise)" >&2; exit 93; }
[ "$(g show "${A_HEAD}:${T640}" 2>/dev/null | grep -cE '^[[:space:]]+test(\.each\(.*\))?\(')" = "18" ] && [ "$(cnt "$A_HEAD" "$T640" 'test.each([33, 41])(')" = "1" ] \
  || { echo "REFUSING: rd640 is not 18 test lines with ONE test.each([33, 41]) (19 ids)" >&2; exit 93; }
for T in "test('W1 " "test('W2 " "test('F2 " "test('F3 " "test('Y5 "; do
  [ "$(cnt "$A_HEAD" "$T640" "$T")" = "1" ] || { echo "REFUSING: rd640 lacks the cell '$T' exactly once" >&2; exit 93; }
done

# 94 — RD-794's premises at source (incl. WRONG 1-3).
[ "$(blob "$BASE_BC" "$SV")" = "$SV_Z_BLOB" ] && [ "$(blob "$B_HEAD" "$SV")" = "$SV_B_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SV")" = "$SV_M_BLOB" ] \
  && [ "$(blob "$BASE_BC" "$MC")" = "$MC_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$MC")" = "$MC_M_BLOB" ] && [ "$(blob "$B_HEAD" "$MC")" = "$MC_B_BLOB" ] \
  && [ "$(blob "$MAIN_SHA" "$LLI")" = "$LLI_M_BLOB" ] && [ "$(blob "$B_HEAD" "$LLI")" = "$LLI_B_BLOB" ] && [ "$(blob "$MAIN_SHA" "$OLA")" = "$OLA_M_BLOB" ] && [ -z "$(blob "$B_HEAD" "$OLA")" ] \
  && [ "$(blob "$B_HEAD" "$T794")" = "$T794_BLOB" ] && [ "$(blob "$B_HEAD" "$TPARK")" = "$TPARK_BLOB" ] \
  || { echo "REFUSING: RD-794's blobs are not as briefed (server.js 0d7e387 -> a3db7da, M0 2684acd; model-config 35064f1 -> 6cc7986; llm index db23e47 -> f0e377d; adapter removed)" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$MC" "const activeConfig = Object.prototype.hasOwnProperty.call(PROVIDERS, LLM_PROVIDER) ? PROVIDERS[LLM_PROVIDER] : PROVIDERS['azure-openai'];")" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$MC" '  models: {},')" = "1" ] && [ "$(cnt "$B_HEAD" "$MC" 'Nothing in backend/ read it; getModelByName now answers null.')" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$MC" 'return (modelName && MODEL_CONFIG.models[modelName]) || null;')" = "1" ] \
  || { echo "REFUSING: model-config.js at cd171f9 is not as briefed (own-key activeConfig; models {}; the 'Nothing in backend/ read it' comment; getModelByName) (b3/b4, WRONG 3)" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$SV" 'MODEL_CONFIG.models[modelId]')" = "2" ] && [ "$(cnt "$B_HEAD" "$SV" '/api/tags')" = "3" ] \
  && [ "$(cnt "$B_HEAD" "$SV" "app.get('/api/service-status', async (req, res) => {")" = "1" ] && [ "$(cnt "$B_HEAD" "$SV" "app.get('/api/models/health/:modelId', async (req, res) => {")" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$SV" "app.get('/api/status'")" = "0" ] \
  || { echo "REFUSING: the remainder sites at cd171f9 are not as briefed (2 models[modelId] readers, 3 /api/tags, service-status + models/health, no /api/status route) (b5, WRONG 1-4)" >&2; exit 94; }
[ "$(cnt "$BASE_BC" "$SV" 'isOllamaEndpointAllowed')" = "3" ] && [ "$(cnt "$B_HEAD" "$SV" 'isOllamaEndpointAllowed')" = "1" ] \
  || { echo "REFUSING: isOllamaEndpointAllowed is not 3 -> 1 (comment only) across RD-794" >&2; exit 94; }
GONE=0
for F in llm-provider-default-azure-openai rd395-ai-enabled-gate rd395-ai-enabled-writer rd395-ai-toggle-write rd395-raw-model-calls rd423-test-ai-does-not-crash-server security-fixes; do
  P="__tests__/$F.test.js"
  N="$(comm -23 <(titles "$BASE_BC" "$P" | sort) <(titles "$B_HEAD" "$P" | sort) | grep -c .)"; GONE=$((GONE + N))
  [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$BASE_BC" "$P")" ] || { echo "REFUSING: $P moved on main since 3e6d02d — C-133 condition (2) for B's missing ids may fail; re-brief (b8)" >&2; exit 94; }
done
[ "$GONE" = "9" ] || { echo "REFUSING: RD-794's static title diff loses $GONE ids, not the 9 its C-133 table names (b8, ruling e)" >&2; exit 94; }

# 95 — RD-819's premises at source.
[ "$(blob "$C_HEAD" "$SV")" = "$SV_C_BLOB" ] && [ "$(blob "$C_HEAD" "$T819")" = "$T819_BLOB" ] && [ -z "$(blob "$C_HEAD" "$TPARK")" ] && [ "$(blob "$C_HEAD" "$MC")" = "$MC_B_BLOB" ] \
  || { echo "REFUSING: RD-819's blobs are not server.js d0ba5e8 / rd819 9064371 / parked file removed / model-config = B's" >&2; exit 95; }
[ "$(cnt "$C_HEAD" "$SV" "const rd819Blank = (v) => v === undefined || v === null || (typeof v === 'string' && v.trim() === '');")" = "1" ] && [ "$(cnt "$B_HEAD" "$SV" 'rd819Blank')" = "0" ] \
  || { echo "REFUSING: rd819Blank is not 0 -> 1 across RD-819 (c2/c3's premise, WRONG 5)" >&2; exit 95; }
[ "$(g show "${C_HEAD}:${T819}" 2>/dev/null | grep -cE '^[[:space:]]+test\(')" = "8" ] || { echo "REFUSING: rd819 is not 8 test() cells" >&2; exit 95; }
[ "$(g diff -M10% --name-status "$B_HEAD" "$C_HEAD" 2>/dev/null | grep -c "^R033[[:space:]]$TPARK")" = "1" ] || { echo "REFUSING: the parked W5 -> rd819 move is not R033 (WRONG 6's premise)" >&2; exit 95; }

# 96 — RD-807's premises at source.
[ "$(blob "$BASE_D" "$INC")" = "$INC_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$INC")" = "$INC_M_BLOB" ] && [ "$(blob "$D_HEAD" "$INC")" = "$INC_D_BLOB" ] \
  && [ "$(blob "$D_HEAD" "$T807")" = "$T807_BLOB" ] && [ "$(blob "$D_HEAD" "$T807P")" = "$T807P_BLOB" ] \
  || { echo "REFUSING: RD-807's blobs are not incidents 740be8d -> 988969a / rd807 16cfdeb / probe 6f6b8a1" >&2; exit 96; }
for T in 'function _ownIncident(all, incidentId) {' "const RESERVED_IDS = new Set(['__proto__', 'constructor', 'prototype']);"; do
  [ "$(cnt "$D_HEAD" "$INC" "$T")" = "1" ] || { echo "REFUSING: incidents.js at 9b15a99 lacks '$T' exactly once (d2's premise)" >&2; exit 96; }
done
[ "$(cnt "$BASE_D" "$INC" 'const inc = all[incidentId];')" = "1" ] && [ "$(cnt "$D_HEAD" "$INC" 'const inc = all[incidentId];')" = "0" ] \
  || { echo "REFUSING: the base's plain lookup is not 1 -> 0 (d0/d4's premise)" >&2; exit 96; }

# 97 — RD-801/822's premises at source.
[ "$(blob "$MB_AE" "$FB")" = "$FB_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$FB")" = "$FB_M_BLOB" ] && [ "$(blob "$E_HEAD" "$FB")" = "$FB_E_BLOB" ] \
  && [ "$(blob "$E_HEAD" "$LS")" = "$LS_E_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$LS")" ] && [ "$(blob "$E_HEAD" "$T801")" = "$T801_BLOB" ] && [ "$(blob "$E_HEAD" "$T822")" = "$T822_BLOB" ] \
  || { echo "REFUSING: RD-801/822's blobs are not feedback 054ab21 -> a0cb126 / logSafe 196ab46 (new) / rd801 a372351 / rd822 50bc66f" >&2; exit 97; }
[ "$(cnt "$MB_AE" "$FB" '/[ --]/.test(reason)')" = "1" ] && [ "$(cnt "$E_HEAD" "$FB" '/[ --]/.test(reason)')" = "0" ] && [ "$(cnt "$E_HEAD" "$FB" '/[\x00-\x1F\x7F]/.test(reason)')" = "1" ] \
  && [ "$(cnt "$E_HEAD" "$FB" 'logSafe(')" = "4" ] && [ "$(cnt "$E_HEAD" "$LS" 's = s.replace(/[\r\n]/g,')" = "1" ] \
  || { echo "REFUSING: the validator / logSafe wrapping is not as briefed (e2/e4's premise)" >&2; exit 97; }

# 99 — RD-721's premises at source.
[ "$(blob "$BASE_G" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$G_HEAD" "$SV")" = "$SV_G_BLOB" ] && [ "$(blob "$MAIN_SHA" "$TDOM")" = "$TDOM_M_BLOB" ] && [ "$(blob "$G_HEAD" "$TDOM")" = "$TDOM_G_BLOB" ] \
  && [ "$(blob "$MAIN_SHA" "$T385")" = "$T385_M_BLOB" ] && [ "$(blob "$G_HEAD" "$T385")" = "$T385_G_BLOB" ] && [ "$(blob "$MAIN_SHA" "$T442")" = "$T442_M_BLOB" ] && [ "$(blob "$G_HEAD" "$T442")" = "$T442_G_BLOB" ] \
  && [ "$(blob "$G_HEAD" "$T721I")" = "$T721I_BLOB" ] && [ "$(blob "$G_HEAD" "$T721V")" = "$T721V_BLOB" ] && [ "$(blob "$G_HEAD" "$T721D")" = "$T721D_BLOB" ] && [ "$(blob "$G_HEAD" "$T721J")" = "$T721J_BLOB" ] \
  && [ "$(blob "$G_HEAD" "$VNOT")" = "$VNOT_BLOB" ] && [ "$(blob "$G_HEAD" "$VCSS")" = "$VCSS_BLOB" ] && [ "$(blob "$G_HEAD" "$VW2")" = "$VW2_BLOB" ] && [ "$(blob "$G_HEAD" "$VW1")" = "$VW1_BLOB" ] \
  && [ "$(blob "$MAIN_SHA" static/login.html)" = "$LOGIN_M_BLOB" ] && [ "$(blob "$G_HEAD" static/login.html)" = "$LOGIN_G_BLOB" ] \
  || { echo "REFUSING: RD-721's blobs are not as briefed (server.js 2684acd -> c5b7ce1; dom/rd385/rd442; rd721 x3 + provenance; the four vendored files; login)" >&2; exit 99; }
[ "$(cnt "$G_HEAD" "$SV" "const STATIC_ASSET_PREFIXES = ['/static/', '/css/', '/js/', '/fonts/', '/img/', '/vendor/'];")" = "1" ] \
  && [ "$(cnt "$MAIN_SHA" "$SV" "const STATIC_ASSET_PREFIXES = ['/static/', '/css/', '/js/', '/fonts/', '/img/'];")" = "1" ] \
  || { echo "REFUSING: STATIC_ASSET_PREFIXES is not exactly + '/vendor/' across RD-721 (g3's premise, C-206)" >&2; exit 99; }
[ "$(cnt "$G_HEAD" "$TDOM" "const SKIPPED_VENDOR_STYLESHEETS = ['static/vendor/bootstrap-icons-1.10.0/font/bootstrap-icons.css'];")" = "1" ] \
  && [ "$(cnt "$G_HEAD" "$T385" "$R385_HASH")" = "1" ] && [ "$(cnt "$G_HEAD" "$T442" "const THIRD_PARTY_NOTICES = 'static/vendor/THIRD-PARTY-NOTICES.txt';")" = "1" ] \
  || { echo "REFUSING: the three exact guards (dom.js skip list, rd385 reviewed hash, rd442 notices exclusion) are not as briefed (g5's premise)" >&2; exit 99; }
for P in $ICON_PAGES; do
  [ "$(cnt "$G_HEAD" "static/$P.html" 'vendor/bootstrap-icons-1.10.0/font/bootstrap-icons.css')" = "1" ] && [ "$(cnt "$G_HEAD" "static/$P.html" 'bootstrap-icons@')" = "0" ] \
    || { echo "REFUSING: static/$P.html at 64ee309 does not load the vendored icons stylesheet once with no CDN icons ref (I3/I4's premise)" >&2; exit 99; }
done
[ "$(cnt "$G_HEAD" static/login.html 'cdn.jsdelivr.net/npm/bootstrap@5.3.0')" = "1" ] || echo "NOTE: login.html at 64ee309 no longer loads Bootstrap's CSS from the CDN — brief WRONG 16 / T7 may be stale" >&2

# 90 — RD-821: the INSTALLED tool and both kept copies are the pinned files; the round-2 arms' evidence is on disk.
[ "$(fsha "$LOCKTOOL")" = "$LOCK_SHA" ] || { echo "REFUSING: the installed lock tool's sha256 is '$(fsha "$LOCKTOOL")', not fd223bd2… (RD-821 round 2) — re-read C-141 ADDENDUM 6 and re-brief" >&2; exit 90; }
[ "$(fsha "$LOCK_R1")" = "$LOCK_R1_SHA" ] && [ "$(fsha "$LOCK_PRE")" = "$LOCK_PRE_SHA" ] || { echo "REFUSING: the kept copies are not 051f18d6… (pre-1007-o-r2) and 2c892f00… (pre-1006-o)" >&2; exit 90; }
for f in "$EV_O/lock-arms.sh" "$EV_O/lock-arm9.sh" "$EV_O/lock-arm10.sh" "$EV_O/lock-arms-r2final.log" "$EV_O/lock-arms-r2.log" "$EV_O/lock-arm9.log" "$EV_O/lock-swap-1007-r2.txt" "$EV_O/lock-arms.log"; do
  [ -s "$f" ] || { echo "REFUSING: RD-821 evidence absent: $f" >&2; exit 90; }
done
grep -qF 'ARM 9 r2final merge-vs-gate pid: order [H qa-g1 s-merge-m1 b1 ]' "$EV_O/lock-arms-r2final.log" && grep -qF 'ARM 10 r2final ps-fails: rc=2 refused=1 old-still-queued=yes' "$EV_O/lock-arms-r2final.log" \
  && grep -qF "new sha256 $LOCK_SHA" "$EV_O/lock-swap-1007-r2.txt" && grep -qF 'ROUND 2, installed 2026-10-06T18:05:50Z' "$CLAR" \
  || { echo "REFUSING: RD-821 round 2's arm log / swap record / C-141 ADDENDUM 6 ROUND 2 paragraph no longer read as the brief quotes" >&2; exit 90; }
grep -qF 'ROOT="/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s87o/lock-arms-scratch"' "$EV_O/lock-arms.sh" || echo "NOTE: lock-arms.sh no longer hard-codes ROOT under session-tools — f0's re-point instruction may be moot" >&2
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || echo "NOTE: the tool's NEXUSAI_LOCK_BASE default line changed — f0's base guard reads it at source" >&2
if [ -s "$READY_F2" ]; then grep -qF "${LOCK_SHA:0:8}" "$READY_F2" || { echo "REFUSING: $READY_F2 is present but does not name fd223bd2 (T3)" >&2; exit 90; }
else echo "NOTE: no RD-821 round-2 READY at $READY_F2 — T3's default applies (the gate reads C-141 ADDENDUM 6 ROUND 2 + the r2 logs as the claim)" >&2; fi

# 98 — shared blobs; the TWO locks as briefed; proxy-addr per lock (RD-827).
for S in "$BASE_BC" "$MB_AE" "$BASE_D" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_OLD" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: lock / package.json at ${S:0:7} are not e9063d4 / cdb1168 (T2)" >&2; exit 98; }
done
for S in "$BASE_G" "$MAIN_SHA" "$G_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_NEW" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] && [ "$(blob "$S" "$TSH")" = "$TSH_BLOB" ] \
    && [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] && [ "$(blob "$S" "$R549")" = "$R549_BLOB" ] && [ "$(blob "$S" "$R465")" = "$R465_BLOB" ] \
    || { echo "REFUSING: lock / package.json / test-server / helper / Dockerfile / .dockerignore / rd549 / rd465 at ${S:0:7} are not as briefed (d6d3b6e …)" >&2; exit 98; }
done
[ "$(lockver "$LOCK_OLD" proxy-addr)" = "2.0.7" ] && [ "$(lockver "$LOCK_NEW" proxy-addr)" = "2.0.8" ] \
  && [ "$(lockver "$LOCK_OLD" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_NEW" playwright)" = "1.62.1" ] \
  || { echo "REFUSING: proxy-addr is not 2.0.7 (e9063d4) / 2.0.8 (d6d3b6e), or playwright is not 1.62.1 in both (T2, ruling q)" >&2; exit 98; }
for P in "$R549" "$R465"; do
  [ "$(blob "$B_HEAD" "$P")" = "$(blob "$MAIN_SHA" "$P")" ] && [ "$(blob "$C_HEAD" "$P")" = "$(blob "$MAIN_SHA" "$P")" ] || { echo "REFUSING: $P differs between M0 and RD-794/RD-819" >&2; exit 98; }
done

# 23 — EXPECTED OVERLAPS (beyond the counts file): B x C = B's stack; B x G and C x G = the server entry point; every other member pair none;
#       main since each base meets B and C at the server entry point only, and nobody else.
own() { g diff --name-only "$(g merge-base "$1" "$MAIN_SHA")" "$1" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
mside() { g diff --name-only "$(g merge-base "$1" "$MAIN_SHA")" "$MAIN_SHA" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
for X in "$A_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do
  OV="$(comm -12 <(own "$X") <(mside "$X"))"; [ -z "$OV" ] || { echo "REFUSING: main since ${X:0:7}'s base changed a path it changes: $OV — a COMBINED blob the brief does not predict" >&2; exit 23; }
done
for X in "$B_HEAD" "$C_HEAD"; do
  OV="$(comm -12 <(own "$X") <(mside "$X"))"; [ "$OV" = "$SV" ] || { echo "REFUSING: main since 3e6d02d and ${X:0:7} share '$OV', not exactly the server entry point" >&2; exit 23; }
done
L7="A:$A_HEAD B:$B_HEAD C:$C_HEAD D:$D_HEAD E:$E_HEAD G:$G_HEAD"
for x in $L7; do for y in $L7; do
  a="${x%%:*}"; b="${y%%:*}"; [[ "$a" < "$b" ]] || continue
  OV="$(comm -12 <(own "${x#*:}") <(own "${y#*:}") | tr '\n' ' ' | sed 's/ $//')"
  case "$a$b" in
    BC) [ -n "$OV" ] || { echo "REFUSING: RD-794 and RD-819 share no path — the stack is not as briefed" >&2; exit 23; } ;;
    BG|CG) [ "$OV" = "$SV" ] || { echo "REFUSING: $a x $b share '$OV', not exactly the server entry point" >&2; exit 23; } ;;
    *) [ -z "$OV" ] || { echo "REFUSING: $a x $b share '$OV' beyond the counts file — the brief predicts none" >&2; exit 23; } ;;
  esac
done; done

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$BASE_BC 4265 261" "$MB_AE 4298 264" "$BASE_D 4299 264" "$BASE_G 4307 266" "$MAIN_SHA 4320 267" "$A_HEAD 4317 265" "$B_HEAD 4274 262" "$C_HEAD 4282 263" "$D_HEAD 4310 265" "$E_HEAD 4317 266" "$G_HEAD 4328 269"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$BASE_BC" "$MB_AE" "$BASE_D" "$BASE_G" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "306 309 309 312 313 310 308 308 311 311 316 " ] || { echo "REFUSING: the __tests__ census (3e6d02d d97039f 4332fb0 8853e36 M0 A B C D E G) is '$CENSUS', not '306 309 309 312 313 310 308 308 311 311 316'" >&2; exit 35; }

# 70 — the lock on origin main; the npm cache, the sqlite3 prebuild, Chrome, and the carried rulings (NOTEs where the gate decides, REFUSALs where a ruling is missing).
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_NEW" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not d6d3b6e — another lock is in play; prove node_modules before any run (H-31)" >&2
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in proxy-addr/-/proxy-addr-2.0.7.tgz proxy-addr/-/proxy-addr-2.0.8.tgz sqlite3/-/sqlite3-5.1.7.tgz playwright/-/playwright-1.62.1.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -d "$CHROME_APP" ] || echo "NOTE: $CHROME_APP is absent — g9 (the browser leg) will be NOT RUN, named (ruling q)" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" && grep -qF 'merge hold full verify + PR Build are the gate' "$RULING_B" \
  || { echo "REFUSING: Tuesday's ruling (b) (lock-starved full verifies NAMED NOT RUN) is not at $RULING_B as quoted" >&2; exit 70; }
[ -s "$BROWSER_ANS" ] && grep -qF 'Playwright 1.62.1 from YOUR tree' "$BROWSER_ANS" && grep -qF "headless (channel 'chrome'), no download" "$BROWSER_ANS" \
  || { echo "REFUSING: Tuesday's browser-driver ruling (ruling q) is not at $BROWSER_ANS as quoted" >&2; exit 70; }
[ -s "$RULINGS19" ] && grep -qF 'Browser leg for RD-794: NO.' "$RULINGS19" && grep -qF 'the gate measures it with a controlled pid' "$RULINGS19" \
  || { echo "REFUSING: Tuesday's gate-19 rulings file is not at $RULINGS19 as quoted (rulings 3, 4)" >&2; exit 70; }

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean.
MT_PAIRS=0
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$M_ORIGIN $C_HEAD" "$M_ORIGIN $D_HEAD" "$M_ORIGIN $E_HEAD" "$M_ORIGIN $G_HEAD" \
            "$A_HEAD $B_HEAD" "$A_HEAD $D_HEAD" "$A_HEAD $E_HEAD" "$A_HEAD $G_HEAD" "$B_HEAD $D_HEAD" "$B_HEAD $E_HEAD" "$B_HEAD $G_HEAD" \
            "$C_HEAD $D_HEAD" "$C_HEAD $E_HEAD" "$C_HEAD $G_HEAD" "$D_HEAD $E_HEAD" "$D_HEAD $G_HEAD" "$E_HEAD $G_HEAD" "$A_HEAD $C_HEAD"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — READYs, project briefs, builder evidence, prior reports, gate 18/17's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$READY_F" "$READY_G" "$PBRIEF_B" "$PBRIEF_C" "$PBRIEF_D" "$CLAR" "$C133" "$RULINGS19" "$BRIEF18" \
         "$B18_REPORT" "$B17_REPORT" "$B17_UNION" "$B15_REPORT" "$B12_REPORT" \
         "$EV_N/rd640-r2b-hold.out" "$EV_N/union-erasure-rd640r2.lst" "$EV_N/rd640r2b/linux-union.log" "$EV_R/hold-12.log" "$EV_R/hold-11.log" "$EV_R2/hold-13.log" \
         "$EV_O/rd801-hold.log" "$EV_O/rd801-red.log" "$EV_P/rd721-hold2/verify.log" "$EV_P/rd721-icons-hold2.log" "$LOCKTOOL" \
         "$B18_INST/HOLD18.sh" "$B18_INST/qa-holdlib18.sh" "$B18_INST/qa-floorlib18.sh" "$B18_INST/qa-floorcount.py" "$B18_INST/qa-to.sh" "$B18_INST/qa-jestwrap.sh" "$B18_INST/qa-jsum.js" \
         "$B18_INST/qa-runj18.sh" "$B18_INST/qa-mut18.py" "$B18_INST/qa-mutlib18.sh" "$B18_INST/qa-merge18.sh" "$B18_INST/qa-build18.sh" "$B18_INST/qa-npm18.sh" "$B18_INST/qa-file18.sh" \
         "$B18_INST/qa-wait18.py" "$B18_INST/qa-verify18.sh" "$B18_INST/qa-h1-selftest18.sh" "$B18_INST/qa-h1-scan.py" "$B18_INST/qa-mail.py" "$B18_INST/qa-mailread.py" "$B18_INST/qa-lockcheck.py" \
         "$B18_INST/qa-ssprint.sh" "$B18_INST/qa-netbelt.sb" "$B18_INST/qa-netbelt-nodns.sb" "$B18_INST/qa-netbelt-ctl.js" "$B18_INST/qa-c57-id-superset.sh" "$B18_INST/qa-census18.py" \
         "$B18_INST/qa-cov-setup.js" "$B18_INST/qa-srv18.js" "$B17_INST/qa-matrix17.js" "$B17_INST/qa-matrix-run17.sh" "$B17_INST/qa-lib17.js" "$B17_INST/qa-a2-errno.js" "$B17_INST/qa-a7.js" "$B17_INST/qa-a13.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "${C_HEAD:0:7}" "$READY_C" && grep -qF "${B_HEAD:0:7}" "$READY_C" \
  && grep -qF "${D_HEAD:0:7}" "$READY_D" && grep -qF "${E_HEAD:0:7}" "$READY_E" && grep -qF "${G_HEAD:0:7}" "$READY_G" && grep -qF "${LOCK_R1_SHA:0:16}" "$READY_F" \
  && grep -qF 'PRIOR WORK' "$READY_B" && grep -qF 'PRIOR WORK' "$READY_C" && grep -qF 'PRIOR WORK' "$READY_E" && grep -qF 'PRIOR WORK' "$READY_F" && grep -qF 'PRIOR WORK' "$READY_G" \
  && grep -qF 'PRIOR WORK (C-49)' "$PBRIEF_D" \
  || { echo "REFUSING: a READY does not name its head (or RD-821's names round 1's sha), or a PRIOR WORK section is missing" >&2; exit 31; }
grep -qF 'Tests:       2 failed, 17 passed, 19 total' "$EV_N/rd640-r2b-hold.out" && grep -qF 'Tests:       326 passed, 326 total' "$EV_N/rd640-r2b-hold.out" \
  && grep -qF 'VERDICT: PASS — 4317/4317 tests passed across 265 suites (jest exit 0)' "$EV_N/rd640-r2b-hold.out" && grep -qF '=== EXIT restore cc5630b5c810a702' "$EV_N/rd640-r2b-hold.out" \
  && grep -qF '=== done 2026-10-06T21:25:00Z' "$EV_N/rd640-r2b-hold.out" && grep -qF 'uid 1000 node v24.21.0' "$EV_N/rd640r2b/linux-union.log" \
  && grep -qF 'VERDICT: PASS — 4274/4274 tests passed across 262 suites (jest exit 0)' "$EV_R/hold-12.log" && grep -qF 'VERDICT: PASS — 4282/4282 tests passed across 263 suites (jest exit 0)' "$EV_R/hold-12.log" \
  && grep -qF '=== start 794=b1e8ecd 819=d508fca' "$EV_R/hold-12.log" && grep -qF '=== start branch=fdd07af red=ce5b5db' "$EV_R2/hold-13.log" \
  && grep -qF 'VERDICT: PASS — 4310/4310 tests passed across 265 suites (jest exit 0)' "$EV_R/hold-11.log" \
  && grep -qF '=== HEAD 686bf53' "$EV_O/rd801-hold.log" && grep -qF 'expectation UPDATED — tests=4317 suites=266' "$EV_O/rd801-hold.log" && grep -qF 'Tests:       19 passed, 19 total' "$EV_O/rd801-hold.log" \
  && grep -qF 'VERDICT: PASS — 4328/4328 tests passed across 269 suites (jest exit 0)' "$EV_P/rd721-hold2/verify.log" \
  || { echo "REFUSING: a builder log no longer carries the line the brief quotes (WRONG 9/10's premise)" >&2; exit 31; }
[ "$(diff <(sort "$B17_UNION") <(sort "$EV_N/union-erasure-rd640r2.lst") | grep -c '^>')" = "4" ] && [ "$(diff <(sort "$B17_UNION") <(sort "$EV_N/union-erasure-rd640r2.lst") | grep -c '^<')" = "0" ] \
  || { echo "REFUSING: N's union is not gate 17's 18 + 4 (WRONG 9's premise)" >&2; exit 31; }
grep -qF 'GO WITH FINDINGS' "$B18_REPORT" && grep -qF 'STATUS: DELIVERED' "$B18_REPORT" && grep -qF 'GO WITH FINDINGS' "$B17_REPORT" || { echo "REFUSING: gate 17/18's reports do not read as delivered" >&2; exit 31; }
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-64937\}' "$B18_INST/qa-floorlib18.sh" || echo "NOTE: gate 18's qa-floorlib18.sh ROOT default is no longer 64937 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF18" || echo "NOTE: gate 18's brief does not read as stamped by Tuesday — the brief calls it the stamped template" >&2

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
for P in "$B17_REPORT" "$B18_REPORT" "$B15_REPORT" "$BRIEF18" "$PBRIEF_B" "$PBRIEF_C" "$PBRIEF_D" "$B18_INST/" "$B17_INST/" "$RULINGS19" \
         "2026-10-07_nexusai-rd640-r2b-READY-mail.txt" "2026-10-07_nexusai-rd794-cd171f9-READY-mail.txt" "2026-10-07_nexusai-rd819-fdd07af-READY-mail.txt" \
         "2026-10-07_nexusai-rd807-READY-mail.txt" "2026-10-07_nexusai-rd801-rd822-READY-mail.txt" "2026-10-07_nexusai-rd821-READY-mail.txt" "2026-10-07_nexusai-rd721-icons-READY-mail.txt" \
         "2026-10-06_nexusai_g18_ruling_b_deliver_now.md"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in '**RD-640 is TIER 1 (data erasure), ROUND 2 OF 2' '**RD-794 is TIER 1' '**RD-819 is TIER 1' '**RD-807 is TIER 1' '**RD-801 and RD-822 are TIER 2, THROUGH CODE, two separate items.**' \
         '**RD-821 is TIER 2, THROUGH CODE (a tool).**' '**RD-721 Icons is TIER 1**' 'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' \
         'THE BROWSER DRIVER' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' 'THE CROSSES' '--replace' 'qa-b19-'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-640 round 2 of 2 (TIER 1, data erasure' 'RD-794 (TIER 1' 'RD-819 (TIER 1, STACKED on RD-794' 'RD-807 (TIER 1' 'RD-801 and RD-822 (TIER 2 through code' 'RD-821 round 2 (TIER 2 through code' \
         'RD-721 round 1 Icons (TIER 1' 'one verdict per ticket' 'THE CROSSES' 'manifest evaluation' 'NO image built' 'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' \
         'Playwright 1.62.1' 'channel chrome' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-b19-'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD" "$MAIN_SHA" "$BASE_A" "$MB_AE" "$BASE_BC" "$BASE_D" "$BASE_G" "$A_R2A" "$LOCK_SHA" "$LOCK_R1_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$DE_M_BLOB" "$DE_R1_BLOB" "$DE_R2A_BLOB" "$DE_A_BLOB" "$T627_A_BLOB" "$T627_M_BLOB" "$SV_Z_BLOB" "$SV_M_BLOB" "$SV_B_BLOB" "$SV_C_BLOB" "$SV_G_BLOB" "$MC_M_BLOB" "$MC_B_BLOB" \
         "$INC_M_BLOB" "$INC_D_BLOB" "$FB_M_BLOB" "$FB_E_BLOB" "$LS_E_BLOB" "$T819_BLOB" "$TPARK_BLOB" "$T794_BLOB" "$LOCK_OLD" "$LOCK_NEW" "$PKG_BLOB" "$S1_FAILED" "$RD761_R1"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
for S in "$DE_A_SHA16" "$R385_HASH" "$LOCK_PRE_SHA"; do grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }; done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 19' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 19 has no priority member" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
# the gate's own tags must never read as a merge ticket (C-141 ADDENDUM 7): no 'qa-b19-…merge…' tag suggested anywhere.
[ "$(grep -oE 'qa-b19-[A-Za-z0-9_-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-b19- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
case "$PROMPT" in *qa-b19-*merge*) [ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-b19-[A-Za-z0-9_-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-b19- tag containing 'merge'" >&2; exit 15; } ;; esac

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)) is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31 (RE-BASED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-33 (RE-BASED' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-33 (re-based)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-640 RD-794 RD-819 RD-807 RD-801 RD-822 RD-821 RD-721 RD-761 RD-802 RD-697 RD-618 RD-827 RD-816 C-49 C-51 C-57 C-68 C-76 C-89 C-97 C-102 C-104 C-112 C-115 C-125 C-130 C-131 C-133 C-139 C-141 C-14 C-174 C-185 C-186 C-190 C-192 C-199 C-203 C-205 C-206
ADDENDA%2%and%3 ADDENDA%5,%6%and%7 RED-AT-PARENT a0 a2 a3 a4 a5 a9 a10 a11 a12 a13 a14 b0 b2 b3 b4 b5 b6 b7 b8 b9 c0 c2 c3 c4 c5 c6 c7 d0 d2 e0 e2 e3 e4 e5 e6 e7 f0 f1 f2 f3 f4 f5 f6 f7 g0 g2 g3 g4 g5 g6 g7 g8 g9 g10 y1 y2 y3 y4 y5 y6 y7 y8
MT-A MT-D MT-E MT-G MT-B MTF M0 S1 S2 NEVER-FOLLOW F1/W NOTHING-DIALS NO-WRITE PROTOTYPE PLACEMENT BYPASS BROWSER%LEG W1 W2 M819 M819-trim getModelByName service-status models/health validate-all onnx-local
4407/276 4320/267 4339/268 4350/269 4369/271 4390/274 4399/275 4317/265 4274/262 4282/263 4310/265 4317/266 4328/269 new%ids%96 EXACTLY%the%9 missing%0 e9063d4 d6d3b6e 2.0.7 2.0.8 proxy-addr
L-A1 L-A8 L-B1 L-B11 L-C1 L-C8 L-D1 L-D6 L-E1 L-E5 L-F1 L-F7 L-G1 L-G8 L-Y1 H-1 H-2 H-3 H-4 H-9 H-15 H-16 H-17 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 SCRATCH%object%dir git%clone%--shared REGENERATION ms-playwright NEXUSAI_LOCK_BASE LIVE%base controlled%pids
id-superset pull%request STOP JOINS SLOTS POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b19- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --after --replace UNCHANGED%tag DEADLINE HEARTBEAT 2%minutes 5%minutes finally
SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center
npm%install --offline ENOTCACHED HOLD18.sh qa-floorlib18.sh qa-file18.sh Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> GHSA-jqcg-44mw-7w3h #256-#259 PR%#58 seeded%store auth%ENFORCED instrument never%fixes"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 4b. TARGET B' '^## 4c. TARGET C' '^## 4d. TARGET D' '^## 4e. TARGET E' '^## 4f. TARGET F' '^## 4g. TARGET G' \
         '^## 6. THE CROSSES' '^## 7. THE MERGED TREE' '^## 8. CI' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOTS' '^## PROVENANCE' '^### MERGE ORDER' \
         '^### TARGET A' '^### TARGET B' '^### TARGET C' '^### TARGET D' '^### TARGET E' '^### TARGET F' '^### TARGET G' '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# the WRONG list sits ABOVE the rulings (the commission's order), and every WRONG item is marked MEASURED or READ-ONLY-INFERRED somewhere in its line.
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|superseded|Counts and census' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-A8 L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-B9 L-B10 L-B11 L-C1 L-C2 L-C3 L-C4 L-C5 L-C6 L-C7 L-C8 \
         L-D1 L-D2 L-D3 L-D4 L-D5 L-D6 L-E1 L-E2 L-E3 L-E4 L-E5 L-F1 L-F2 L-F3 L-F4 L-F5 L-F6 L-F7 L-G1 L-G2 L-G3 L-G4 L-G5 L-G6 L-G7 L-G8 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 c0 c1 c2 c3 c4 c5 c6 c7 c8 d0 d1 d2 d3 d4 d5 d6 d7 \
         e0 e1 e2 e3 e4 e5 e6 e7 e8 e9 f0 f1 f2 f3 f4 f5 f6 f7 f8 g0 g1 g2 g3 g4 g5 g6 g7 g8 g9 g10 g11 g12 y1 y2 y3 y4 y5 y6 y7 y8; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
for R in s1-0 s1-1 s1-2 s1-3 s1-4 s1-5 s2-0 s2-1 s2-2 s2-3 s2-4; do
  grep -qF "**$R " "$BRIEF" || { echo "REFUSING: brief lacks the SLOT row $R" >&2; exit 19; }
done
# every builder's stated scope / limits / interpretation lines carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; D) F="$READY_D" ;; E) F="$READY_E" ;; F) F="$READY_F" ;; G) F="$READY_G" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|Round 2 of 2: a NO GO ships nothing on this class and the residue is ticketed.
A|092ed9e is WITHDRAWN (not gated; it carries the #1b false receipt).
A|DELIBERATE REDUNDANCY (declared): W1 is caught by the dev+ino key AND by the canonical directory, each alone.
A|NOT RUN: CodeQL (no PR until the merge turn); a CI Build on this head (Build runs only for PR/main).
A|Measured: backend/dataErasure.js +68/-4 vs e944c9c
B|The two /api/status sites are reachable on any provider (env-controlled host; RD-478).
B|No real Ollama or Azure OpenAI endpoint was contacted.
B|RD-819 is stacked on this head (C-199 ADDENDUM). RD-794 lands first, and RD-819 lands in a later turn.
B|Survivor named: MG-vc-fn (RD-820).
C|Nothing replaced: W5 was moved back with git mv.
C|A whitespace key inside an OTHERWISE-real body still saves a blank key (outside the narrow scope).
C|Non-string values (RD-547's class).
C|{"azureOpenAIEndpoint":" "} is refused 400 by the existing format check;
D|ONE product file (backend/incidents.js)
D|the downstream for...in effect (inferred, not enumerated)
D|the route with sign-in configured
E|NOT TESTED: the CodeQL outcome (the PR run); a real Telegram coordinator (the route is driven from localhost); multipart titles (JSON only; the log line is the same).
E|Whether CodeQL accepts logSafe as a sanitizer THROUGH a function call is measured by the PR run, never assumed.
F|the --replace "old waiter ACQUIRED in the gap" self-withdraw (exit 3): a race I could not provoke deterministically. The code path is read, not run.
F|docker-kind arms not separately run (the path is kind-agnostic).
G|server.js: '/vendor/' added to STATIC_ASSET_PREFIXES, nothing else (C-206). Inert extensions only, so /vendor/*.js stays gated.
G|whether the trash glyph change reads as a defect to a human eye.
G|testing: 11/11, 7 px LIGHT only = antialiasing at the corners of the green "Run" button, not an icon. Unexplained render noise.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
Merge order is fixed: RD-794 first, RD-819 on top in a LATER turn, never in the same push.
is a SAME-PLACE handover.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
A merge is now placed strictly after the last gate/merge ticket and strictly before the first builder, in (ns, pid) order, and never passes a gate or an earlier merge.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
An ELOOP does NOT prove a loop
A loop is the same link met twice by identity (device + inode), because a loop through a directory symlink never repeats a path string.
The KEPT failure's text carries the ABSOLUTE path where the chain ends.
THIRD-PARTY NOTICES ARE OUTSIDE C-14.
SVG and HTML never pass.
`backend/llm/ollamaAdapter.js` is removed through git in the slice's PR, with NO quarantine copy.
LLM_PROVIDER=ollama resolves to azure-openai with ONE boot warning
Dependent cells are rewritten, never deleted.
A partner cell that passes without reaching its code is a check that cannot fail.
A real body keeps today's behaviour.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
NexusAI ships one deployment: containers with Azure OpenAI (GPT). No VM, no local model, no local-model setup.
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
Addendum 2's "once PER WAITING GATE TICKET" means once per gate TAG.
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
When a fix reddens an older test, the FIXTURE changes, never the policy
A cell that fails for a known, ticketed reason is PARKED outside the suite, never `test.skip`ped inside it.
the removal wins
Its id-superset verdict is unaffected, but its "failed" count now reads the install, not the tree
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b19-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main is MOVING' '--after' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' 'UNCHANGED tag' \
         'ticket-left-*' 'never two live holds' '-r<N>' 'Every finding names its instrument' 'NOT TESTED' 'The tester never fixes'; do
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
for w in 'RED-AT-PARENT' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4407/276' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' 'd6d3b6e' 'proxy-addr' 'RD-827' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' \
         '_walkLinkChain' 'device+inode' 'rd627a' 'fa16069' 'NOTHING_TO_SAVE' 'rd819Blank' '_ownIncident' 'RESERVED_IDS' 'logSafe' 'STATIC_ASSET_PREFIXES' '/vendor/' 'SKIPPED_VENDOR_STYLESHEETS' \
         'THIRD-PARTY-NOTICES.txt' 'NEXUSAI_LOCK_BASE' 'is_merge' 'gap of 0' 'controlled pids' '/api/service-status' '/api/models/health/:modelId' 'MODEL_CONFIG.models[modelId]' 'getModelByName' \
         'R033' 'C-133' 'EXACTLY the 9' 'Playwright 1.62.1' "channel: 'chrome'" 'ms-playwright' 'GHSA-jqcg-44mw-7w3h' 'ANY rd465 O-1 failure' 'ADDENDUM SLOTS' 'S1 SLOT' 'S2 SLOT' \
         'WRONG 1' 'WRONG 8' 'WRONG 11' 'WRONG 13' 'WRONG 16' 'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib18.sh' 'HOLD18.sh' 'qa-file18.sh' 'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the ADDENDUM SLOTS: each EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
SLOT_STATE=''
SLOT_DESC=''
slot() {   # $1 = S1|S2, $2 = ticket, $3 = branch must equal ('' = must contain $4), $4 = branch hint
  local id="$1" tk="$2" want="$3" hint="$4" J E sha br tier rdy now base
  J="$(grep -E "^ADDENDUM $id $tk JOINS @ [0-9a-f]{40} ON [A-Za-z0-9._/-]+ TIER [12] \\| READY /" "$BRIEF" 2>/dev/null)"
  E="$(grep -c "^$id SLOT: EMPTY\$" "$BRIEF" 2>/dev/null)"
  if [ -z "$J" ]; then
    [ "$E" = "1" ] || { echo "REFUSING: the $id ($tk) slot is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
    SLOT_STATE="$SLOT_STATE $tk ($id) is NOT a member of this gate (its slot is EMPTY): do not gate it; say so in the report."
    SLOT_DESC="$SLOT_DESC $id EMPTY;"; return 0
  fi
  [ "$(printf '%s\n' "$J" | grep -c .)" = "1" ] && [ "$E" = "0" ] || { echo "REFUSING: the $id slot has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  sha="$(printf '%s\n' "$J" | sed -E 's/^.* JOINS @ ([0-9a-f]{40}) .*/\1/')"
  br="$(printf '%s\n' "$J" | sed -E 's/^.* ON ([A-Za-z0-9._/-]+) TIER .*/\1/')"
  tier="$(printf '%s\n' "$J" | sed -E 's/^.* TIER ([12]) .*/\1/')"
  rdy="$(printf '%s\n' "$J" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  if [ -n "$want" ]; then [ "$br" = "$want" ] || { echo "REFUSING: the $id branch '$br' is not $want (89)" >&2; exit 89; }
  else case "$br" in *"$hint"*) ;; *) echo "REFUSING: the $id branch '$br' does not name $hint (89)" >&2; exit 89 ;; esac; fi
  lsr "refs/heads/$br" || { echo "REFUSING: ls-remote of the $id branch failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN (C-192) (89)" >&2; exit 89; }
  now="$(printf '%s\n' "$LSR_OUT" | awk -v r="refs/heads/$br" '$2==r{print $1}')"
  [ "$now" = "$sha" ] || { echo "REFUSING: the $id ADDENDUM names $sha but origin $br is '${now:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$sha" 2>&1)" = "commit" ] || { echo "REFUSING: $tk $sha is not in the object store (89)" >&2; exit 89; }
  [ -s "$rdy" ] && grep -qF "${sha:0:7}" "$rdy" || { echo "REFUSING: $tk's READY '$rdy' is absent or does not name ${sha:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$sha" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: $tk ${sha:0:7} is already on main (89)" >&2; exit 89; fi
  if [ "$id" = "S1" ]; then
    [ "$sha" != "$S1_FAILED" ] || { echo "REFUSING: the S1 JOINS line names 72ca5d3, RD-761's FAILED PR head — the fix round must name its new head (89)" >&2; exit 89; }
    g merge-base --is-ancestor "$S1_FAILED" "$sha" 2>/dev/null || echo "NOTE: RD-761's fix head ${sha:0:7} does not descend from 72ca5d3 — the gate reads s1-0's scope from its own merge-base" >&2
  else
    g merge-base --is-ancestor "$E_HEAD" "$sha" 2>/dev/null || { echo "REFUSING: RD-802 ${sha:0:7} is not stacked on RD-801 6613113 (89)" >&2; exit 89; }
  fi
  base="$(g merge-base "$sha" "$M_ORIGIN")"
  [ -z "$(g diff --name-only "$base" "$sha" -- "$PKG" "$LOCK" 2>/dev/null)" ] || { echo "REFUSING: $tk changes package.json or the lock over its base (89)" >&2; exit 89; }
  [ -z "$(g diff --name-only "$base" "$sha" -- static 2>/dev/null)" ] || echo "NOTE: $tk touches static/ — the brief's slot rows do not predict it; the gate names it" >&2
  for X in "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$G_HEAD"; do
    RC="$(conflicts "$X" "$sha" | tr '\n' ' ' | sed 's/ $//')"
    [ -z "$RC" ] || [ "$RC" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x $tk conflicts beyond the counts file: '$RC' (89)" >&2; exit 89; }
    MT_PAIRS=$((MT_PAIRS + 1))
  done
  SLOT_STATE="$SLOT_STATE $tk JOINS this gate per the brief's ADDENDUM SLOTS ($id), at $sha (origin $br, re-pinned by the launcher), TIER $tier as Tuesday wrote it, READY $rdy — gate it by the brief's $id rows and merge it where T1 puts it."
  SLOT_DESC="$SLOT_DESC $id JOINS @ ${sha:0:7} ($br, tier $tier);"
}
slot S1 RD-761 "$S1_BRANCH" ''
slot S2 RD-802 '' "$S2_HINT"

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  BQ="$(grep -l '^tag=qa-b1' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate (qa-b1*) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

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
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R tuesday; do
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
for PEER in 'QA/NexusAI-batch14' 'QA/NexusAI-batch15' 'QA/NexusAI-batch16' 'QA/NexusAI-batch17' 'QA/NexusAI-batch18'; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
    echo "NOTE: $PEER has a live claude — a PEER gate: FIFO, never touched; added as a negative control" >&2
  fi
done

# 86 — no live gate-19 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 19 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 96 97 99 90 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-640 $A_HEAD · RD-794 $B_HEAD · RD-819 $C_HEAD · RD-807 $D_HEAD · RD-801/822 $E_HEAD · RD-721 $G_HEAD · RD-821 sha256 ${LOCK_SHA:0:16}… · SLOTS:$SLOT_DESC" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 6 member branches at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192); RD-821 installed sha256 fd223bd2… + both kept copies (90)"
  echo "  main ${M_ORIGIN:0:7} (8b7ae54 or a descendant; no member-only path moved; no member on it) (18b)"
  echo "  merge-bases (7); chains (8); deltas + no package change + product paths (22); premises (93 94 95 96 97 99); locks + proxy-addr (98)"
  echo "  overlaps (23); counts + census (35); npm cache + sqlite3 prebuild + Chrome + the carried rulings (70); $MT_PAIRS three-argument merge-trees counts-only or clean (80, 89); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); SLOTS:$SLOT_DESC (89); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/$G_BRANCH = $G_HEAD; refs/heads/main = $M_ORIGIN (8b7ae54 or a descendant; no member-only path moved since 8b7ae54; no member on it). RD-821's installed tool sha256 = $LOCK_SHA. $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOTS:$SLOT_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
