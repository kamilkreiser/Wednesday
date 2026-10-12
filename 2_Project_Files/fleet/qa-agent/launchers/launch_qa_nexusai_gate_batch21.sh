#!/bin/bash
# launch_qa_nexusai_gate_batch21.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 21"), FOUR members (+ TWO generic ADDENDUM SLOTS),
# one verdict per ticket, ONE report (drafted 2026-10-12 ~14:55–~15:40 AEDT by a read-only drafting agent for Tuesday; the drafter ran only --check).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start. A TIERED gate (tier-1 cells run; tier-2 cells / full verifies may be NAMED NOT RUN, ruling o).
#   A — RD-775 (TIER 1; CodeQL #69) rd-775-readiness-key-s92r @ 537741c (= refs/pull/70/head): THREE commits on 41c5a47. aiReadiness 7db38ea -> 578e7e7. 4387/274.
#   B — RD-131 (TIER 2 + ONE browser leg + a formula-cell control) rd-131-fleet-health-drum-csv-s87n @ e7d2cd1: TWO commits on 7d11359. index.js ae59c25 -> 8ab3664. 4391/274.
#   C — RD-807 F-807-1 fix round (TIER 2, test-only) rd-807-incidents-prototype-key-s89r @ ff5d725: THREE commits on 9b15a99 (gate 19's GO WITH FINDINGS), base 4332fb0. Old lock e9063d4. 4312/265.
#   D — RD-821 r3 F-821-1 (TIER 2, tooling): a CANDIDATE FILE, NOT installed — session-tools/s96o/nexusai-lock.sh.new sha256 3c33f5ae… vs installed session-tools/nexusai-lock.sh fd223bd2…
#       (BOTH pinned, guard 90). Tested ONLY on scratch NEXUSAI_LOCK_BASE dirs (ruling s, H-34) — never the live lock.
#   THE CROSSES (C-68): A x B meet in rd464-ai-readiness-service; C's route cell on M0's moved server entry point; B x rd385.
#   SLOTS — S1, S2 (generic) join ONLY by the brief's JOINS lines (guard 89). EMPTY.
#   Main at drafting b6c506a (RD-657; counts 4421/276; lock 19477a9). Predicted MTF 4448/279.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch21' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch21.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-21 drafting commission (2026-10-12). READY mails copied in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings: sqlite3 cached prebuild; full verifies UNBELTED with 4 conditions; npm_config_update_notifier=false on EVERY npm call; ruling (b) + its
# EXTENSION (gate 20's ruling (c), answer-starvation.txt) — lock-starved full verifies / tier-2 cell holds NAMED NOT RUN; the browser driver; C-190 + its
# ADDENDUM: BOTH CodeQL thresholds; C-209 (pre-existing alerts closed post-merge); C-141 ADDENDA 6/7: --replace for re-files, only a merge HOLD's tag says
# "merge" (gate tags are qa-b21-*); RULING (i)'s BY-HAND GATE YIELD IS RETIRED from gate 21 on (gate 19's RELEASE item 5).
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert, NEVER swaps the lock tool; no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch20.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the LIVE
# negative-control seat derivation 38R, the ADDENDUM-SLOT JOINS parser 89, route-line and stamp guards last). CHANGES, each deliberate:
#   - FOUR members on THREE merge-bases + ONE non-git member (D): guard 90 pins D's two sha256s (REFUSE on a mismatch), checks the 23-line diff and the
#     candidate's new rule, and that O's harness refuses an unscoped base. No D sha in any ls-remote.
#   - 18b: main moving is a NOTE; a member-ONLY path moving REFUSES; a member already on main REFUSES (as gate 20).
#   - 98: THREE locks (e9063d4 at C and its parents; d6d3b6e at A, B and their bases; 19477a9 at M0 — d6d3b6e with only the root version changed).
#   - 89: TWO GENERIC slots (ticket and branch are Tuesday's to write; no slot was pre-named).
#   - 38R: the coordinator pane may be named 'tuesday' OR 'wednesday' (at drafting this machine's Tuesday seat runs in a pane named 'wednesday'); exactly one.
#     QA/NexusAI-batch20 joins the peer list.
#   - 41: ruling (i)'s yield is RETIRED — the prompt/brief must say so and must not instruct a by-hand yield; gate 20's qa-file20.sh (which carries it) is named for removal.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); shasum / diff / bash -n over session-tools files; python/grep over `git show` output; ls, ps, tmux list-panes, test -e.
# It writes nothing and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch21.sh [--check]
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
BRIEF="$BRIEFS/2026-10-12_nexusai-gate-batch21.md"
BRIEF20="$BRIEFS/2026-10-08_nexusai-gate-batch20.md"
READY_A="$BRIEFS/2026-10-08_nexusai-rd775-READY-mail.txt"
READY_B="$BRIEFS/2026-10-12_nexusai-rd131-READY-mail.txt"
READY_C="$BRIEFS/2026-10-12_nexusai-rd807-f8071-READY-mail.txt"
READY_D="$BRIEFS/2026-10-12_nexusai-rd821r3-READY-mail.txt"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
BROWSER_ANS="$STAGED/2026-10-04_qa_batch13_browser_driver_answer.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
O_ANSWER="$STAGED/2026-10-12_nexusai_O_S96O_plan_ANSWER.md"
N_ANSWER="$STAGED/2026-10-12_nexusai_N_S94N_plan_ANSWER.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
PBRIEF_A="$NX/qa-briefs/2026-10-08_nexusai-rd775-tier1-gate.md"
PBRIEF_C="$NX/qa-briefs/2026-10-12_nexusai-rd807-f8071-fixround-tier2-gate21.md"
ST="$NX/session-tools"
LOCKQ="$ST/locks/queue-jest"
LOCKTOOL="$ST/nexusai-lock.sh"
CANDIDATE="$ST/s96o/nexusai-lock.sh.new"
LOCK_SHA_INST='fd223bd2a72d38143d0466fcbcc6762f9bc7f82815084d1a3c53422acc2d7700'   # RD-821 round 2, INSTALLED (gate 19) — D's base, PINNED
LOCK_SHA_CAND='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3 candidate — D's head, PINNED
C57_RUNNER="$ST/c57-id-superset.sh"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$ST/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B20_DIR="$RPTS/2026-10-08-gate-batch20"
B20_REPORT="$B20_DIR/report.md"
B20_INST="$B20_DIR/evidence/inst"
B20_STARVE="$B20_DIR/evidence/answer-starvation.txt"
B19_DIR="$RPTS/2026-10-07-gate-batch19"
B19_BODY0="$B19_DIR/body-0.md"
B19_BODY2="$B19_DIR/body-2.md"
B19_F3="$B19_DIR/evidence/f3-placement.txt"
B19_RACE="$B19_DIR/evidence/inst/qa-d807race19.js"
B19_RACE_SHA='face4538dfc4e9595c72460ebb74e08d775161240ad2d150c91a2b1042a9bbad'
B19_F3SH="$B19_DIR/evidence/inst/qa-f3-19.sh"
B19_F3SH_SHA='9edd3427f0c7ed28da2c4bababb32f876a377190bcca436251de8a1a66711dad'
PREV_FLOORLIB="$B20_INST/qa-floorlib20.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-12-gate-batch21/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch21'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'

MAIN_SHA='b6c506a7248a847df8bedbe1590e200c8516c3f0'      # origin main at drafting (14:56:28 AEDT; RD-657 last)
MB_A='41c5a47b3301a7172726b6bef867a5586b8fa89a'          # A's base = merge-base(A, M0)
MB_B='7d11359b585a8ca62075700bc77960bc8784ea48'          # B's base = merge-base(B, M0)
C_BASE='9b15a99bce539d8eb63a5b4bac052cd18ea45d19'        # C's gate-range base: RD-807 round 1 (gate 19, GO WITH FINDINGS)
C_RED='408115cb3e076bbb5f3bcecb5e815b5f92cda110'         # C's red-first commit
MB_C='4332fb06a349b8a189e9ec70022ff9290d2fadf5'          # merge-base(C, M0) — RD-807 round 1's base
B90='90b255682d00a17c203ab1a2395953cdb9a682ab'           # RD-816 (proxy-addr 2.0.8 lock)
A_BRANCH='rd-775-readiness-key-s92r'
A_HEAD="${QA_A_HEAD_OVERRIDE:-537741ce9d1d52f80588ca5a11088182b864960c}"
B_BRANCH='rd-131-fleet-health-drum-csv-s87n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-e7d2cd1b03928c74fe3148a93e0185adae436d27}"
C_BRANCH='rd-807-incidents-prototype-key-s89r'
C_HEAD="${QA_C_HEAD_OVERRIDE:-ff5d725478c310a36c83be5575345395b2f7bb90}"
PR70_REF='refs/pull/70/head'

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
SV='backend/server.js'
AIR='backend/services/aiReadiness.js'
IDX='static/js/index.js'
INC='backend/incidents.js'
T775='__tests__/rd775-readiness-key-no-hash.test.js'
T464='__tests__/rd464-ai-readiness-service.test.js'
T131='__tests__/rd131-fleet-health-drum-csv.test.js'
T385='__tests__/rd385-shipped-root-markdown-identifiers.test.js'
T807='__tests__/rd807-incidents-prototype-key.test.js'
P807='__tests__/helpers/rd807-prototype-probe-preload.js'
W807='__tests__/helpers/rd807-torn-write-widener.js'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
DKF='Dockerfile'
DIG='.dockerignore'

AIR_M_BLOB='7db38ea21272be246908d9605626fd12299f5d89'     # 41c5a47, M0
AIR_A_BLOB='578e7e7967152efd832e21e70644f15eaec1eb44'
T775_BLOB='0cca0e04ee6e81ccd237d6907cb56a608d16bfda'
T464_BLOB='035f48937c55c3282709f28140897621088c2c97'     # M0 = A
IDX_M_BLOB='ae59c25d70df6c4d4053eef950cd3b495a1e6554'     # 7d11359, M0
IDX_B_BLOB='8ab366490df18dddcbcb907c1173d70dab251b49'
T131_BLOB='098c5fcfd40b135ac6145785b8494151b60a05cc'
INC_M_BLOB='740be8d51afcce97db77169e1bdcc8580f652f05'     # 4332fb0, M0
INC_C_BLOB='988969aa46ea3e4e185d92eeeadeb85ac42c9340'     # 9b15a99 = ff5d725 (round 1)
T807_R1_BLOB='16cfdeb1e0e150b2ac69092242a2c970a901b03d'   # 9b15a99
T807_BLOB='790c0248078a096520fdc8440fc1bbad35936223'
P807_R1_BLOB='6f6b8a1f0cfdb999bb805c18c6e15198dfa8f83f'   # 9b15a99 (the in-place writer)
P807_BLOB='722e2b93216a9d7067b74811026007fc1ebdcc7a'
W807_BLOB='b917f8a6a7a1b3d8838e98a4ad920eb565ecc92f'
SV_M_BLOB='c8ca2b38d5bfddb795933bb152269d7c2f4490ae'      # M0
SV_AB_BLOB='703f4297778ffc137e83eed88aed409fc86874bc'     # A, B and their bases
SV_C_BLOB='2684acda2190ac2578008f8055a131fe6cd9a7f1'      # C and 4332fb0
LOCK_OLD='e9063d44757007324b8c55fa58c03c03dfe552ae'        # 4332fb0, 9b15a99, 408115c, C (proxy-addr 2.0.7)
LOCK_MID='d6d3b6e42aa604320f3b70f8e9048bfac044f277'        # 41c5a47, A, 7d11359, B (proxy-addr 2.0.8)
LOCK_NEW='19477a9329f17e529c208d91d172b95b47fc1bb5'        # M0 (= d6d3b6e with the root version 1.3.0 -> 2.2.1 only)
PKG_OLD='cdb1168783a92179afe20be67b37976203b904f8'
PKG_NEW='384805d9e286718bb34ffd05be01c62c00806cf5'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'
TSH_BLOB='f612fb4815aaa358795acc977d59a0a9cba09670'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
R549_BLOB='4a3564265683f936c99e69789049e3dd5dff9b3b'
R465_BLOB='f16b811756f70ddcd37ec43197383c5434cff6e4'

A_EXPECTED_FILES="$T775
$AIR
$COUNTS_FILE"
B_EXPECTED_FILES="$T131
$COUNTS_FILE
$IDX"
C_EXPECTED_FILES="$P807
$W807
$T807
$COUNTS_FILE"
C_MB_EXPECTED_FILES="$P807
$W807
$T807
$INC
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 21'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch21] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any member head without a pull_request Build (RD-775's included unless the gate's read finds one on 537741c), CodeQL at any head without a PR, main's CodeQL alert #69 (closure read only after merge, C-209), a real Azure OpenAI endpoint, a real Log Analytics or Azure Monitor endpoint (the drum table came from the synthetic feed), real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO) and its synthetic feed as deployed, any deployed environment, headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, off-host requests aborted), the probe rename on Windows or a network filesystem, the jest-lock candidate as INSTALLED or on the live queue (every arm ran on a scratch lock base; the swap is not the gate's), the docker lock kind beyond one arm, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
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
conflicts() { local b; b="$(g merge-base "$1" "$2" 2>/dev/null)" || return 1
  g merge-tree "$b" "$1" "$2" 2>/dev/null | awk '/^  (base|our|their) /{f=$4} /^\+<<<<<<</{c[f]=1} END{for(k in c) print k}' | sort; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 21", with FOUR members and TWO generic ADDENDUM SLOTS, one verdict per ticket and ONE report. It is a FRESH gate, and a TIERED one. The members: RD-775 (TIER 1, NexusAI-R: the AI readiness cache identifies an API key by an opaque per-instance id instead of a sha256 digest — CodeQL #69 js/insufficient-password-hash — with the id map capped at 64 and ids never reused; it is PR #70's head, whose CodeQL condition is part of its verdict, and #69's own closure is a post-merge read under C-209), RD-131 (TIER 2 + ONE local browser leg + a formula-cell control, NexusAI-N: both Fleet Health exports carry the Drum Status table through one helper), RD-807 F-807-1 fix round (TIER 2 through code, TEST-ONLY, round 1 of 2 of the fix round, NexusAI-R: the probe preload writes temp file + rename so a reader never sees the probe torn, plus a widener shim and a control cell that make the race visible; it sits on RD-807 round 1 at 9b15a99bce539d8eb63a5b4bac052cd18ea45d19, gate 19's GO WITH FINDINGS, which is NOT re-verdicted here), and RD-821 round 3 F-821-1 (TIER 2 through code, TOOLING, NexusAI-O: a CANDIDATE jest-lock tool, NOT installed, at session-tools/s96o/nexusai-lock.sh.new sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792, against the installed session-tools/nexusai-lock.sh sha256 fd223bd2a72d38143d0466fcbcc6762f9bc7f82815084d1a3c53422acc2d7700). RD-821's fix is a DEVIATION from gate 19's described fix shape, RULED (a) by Tuesday: you test it against the INVARIANT — a merge never passes the queued ticket P just ahead of the first waiting builder — and that merge-first is preserved ahead of every later builder, not against the old wording. THE CROSSES (C-68): RD-775 and RD-131 meet in one cell file (rd464-ai-readiness-service reads both modules), RD-807's route cell boots main's moved server entry point, and RD-131's readers include rd385, which main moved. The SLOTS are members ONLY if the brief carries their JOINS lines — the launcher tells you below. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its head AND (for the three git members) the merged tree. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry, and no browser except the ONE local browser leg the brief names (b2).

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-12_nexusai-gate-batch21.md
It opens with the drafter's WRONG OR UNVERIFIED list (every place a READY, a project brief or the commission contradicts the source, each marked MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1-T10 as Tuesday stamped them, and the carried rulings (a) to (s)) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the four member READY mails it names (read each WHOLE), the two project briefs (RD-775's and RD-807's, read WHOLE), the clarifications the brief names at source (C-209 and C-141 with its ADDENDA 5, 6 and 7 first), gate 19's verdict body (body-0.md) and its RD-821 section (body-2.md section 7 with evidence/f3-placement.txt), gate 19's RELEASE, and gate 20's report (the structural template and the instrument source). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window; adversarial rows are written as the property, the input shape and the expected result — you write your own drivers.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones — every one is an authorised, findings-only measurement of Datasec's own product and tooling in your own trees, your own loopback servers, your own mktemp dirs and your own scratch lock bases; no row contacts a non-loopback address and no row touches the live jest queue except your own holds through the installed tool. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-775: rd-775-readiness-key-s92r at 537741ce9d1d52f80588ca5a11088182b864960c (= refs/pull/70/head; gate range 41c5a47b3301a7172726b6bef867a5586b8fa89a..537741c, THREE commits; counts 4387/274). RD-131: rd-131-fleet-health-drum-csv-s87n at e7d2cd1b03928c74fe3148a93e0185adae436d27 (TWO commits on 7d11359b585a8ca62075700bc77960bc8784ea48; counts 4391/274). RD-807 fix round: rd-807-incidents-prototype-key-s89r at ff5d725478c310a36c83be5575345395b2f7bb90 (gate range 9b15a99..ff5d725, THREE commits, test-only; round 1 sits on 4332fb06a349b8a189e9ec70022ff9290d2fadf5; counts 4312/265; the OLD lock e9063d4, proxy-addr 2.0.7, correct for that tree). RD-821 round 3: the two sha256s above; the gate range is the diff of the two files, 23 changed lines. No git member has a builder full verify OF ITS HEAD (brief WRONG 3, 7, 13): yours decides. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b): the merge turn order names many tickets (gate 20's and gate 19's members among them). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (the brief's proposed order MT-C 4434/277, MT-B 4443/278, MTF 4448/279; predicted at M0 = b6c506a7248a847df8bedbe1590e200c8516c3f0, 4421/276), the tests census (329 at MTF), new ids 27 and missing 0 for every member. If a member is in your M0, mail a QUESTION; if anything landed, name it and re-derive every C-68 set on it (y7). Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash RD-821's two files at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. The Datasec CodeQL org policy: a commit reaches main only after CodeQL scanned it on a PR, and alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed; its closure is read after the merge, on main, by number. RD-775's PR #70 exists: read it with gh READ ONLY (the repo is datasecau/Reporting_Dashboard_Au) — the alerts on refs/pull/70/head in every state, beside THE CONTROL state=fixed on refs/pull/58/head = EXACTLY #256-#259 (an empty set on #70 is not a control), any NEW alert at either threshold, #69 on main named as the post-merge landing condition, and whether a pull_request Build ran on 537741c (if not, Linux is NOT RUN, never passed). RD-131 and RD-807 have no PR: CodeQL is NOT RUN and the CI Build is NOT RUN at those heads — say so; RD-821 is a shell file outside the repo (CodeQL not applicable). A red npm-audit at RD-807's head (on the pre-RD-816 lock) is proxy-addr GHSA-jqcg-44mw-7w3h only — name it (C-210: not reachable). C-185 on M0 (ruling h): the known-failing set is {rd549 O4, rd549 C2/C10 — each only when envReached alone differs}; ANY rd465 O-1 failure on M0, a head or a merged tree is a STOP; a known-set failure is named and classified, never waved; no re-run is a clearance. The shared C-57 runner links a proxy-addr 2.0.7 install, so its rd816 "failed 3" is a known runner artefact (RD-837): read each verify's VERDICT line and the id-superset result, never the C-57 failed count.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-775: a0 RED-AT-PARENT (the base aiReadiness reddens SOURCE and the bound cell; the no-leak cell and both CONTROLs stay green); a1 the head clean; a2 THE KEY ROW — a real local server with a loopback stand-in for Azure OpenAI and a low-entropy marker key, status read twice, the key changed, read again, every log, response, error and DATA_DIR file scanned, the stand-in seeing the key as the control; a3 THE BOUND ROW — the cap, a re-seen key re-probed, ids never reused, and the verdict cache's growth measured (WRONG 1, T3); a4 the cache semantics unchanged; a5 the builder's two mutants plus your own, including the raw key in the cache-key string, which no cell is predicted to see; a6 THE CODEQL CONDITION; a7 C-68; a8 manifest evaluation, NO image built; a9 prior work. RD-131: b0 RED-AT-PARENT; b1 the head clean; b2 THE BROWSER LEG — your tree of the head and of its base, open mode, USE_AZURE_LOG_ANALYTICS=true and SYNTHETIC_DEMO_FEED=true so REAL drum rows render from the synthetic feed (never planted DOM), both exports downloaded and read back, the drum sections equal to the on-screen rows cell for cell, the consumables section unchanged, every off-host attempt counted and aborted; b3 THE FORMULA-CELL CONTROL — leading = + - @ TAB CR, drum bytes equal to consumables bytes for each (neutralising is RD-835's), in the browser only through a real local data path, else NOT RUN there; b4 the count, alert and shape row; b5 escaping; b6 mutants; b7 C-68; b8 manifest; b9 CodeQL READ ONLY; b10 prior work. RD-807: c0 RED-AT-PARENT (the in-place preload reddens T2 only); c1 the head clean; c2 THE TORN-READ ROW — your copy of gate 19's reproducer against the head and base preloads, 200,000 reads, plain and widened, the base reading empty as the control; c3 THE LOAD ROW — the rd807 file inside the merged-tree unions at two workers, three repeats (T6); c4 mutants; c5 T1 has teeth (M3 repeated); c6 the precondition cell still sees a dead probe; c7 the leftover temp file (C-208); c8 C-68 on main's server entry point; c9 CodeQL READ ONLY; c10 prior work. RD-821: d0 RED-AT-BASE (the installed tool's two gap-0 low-pid rows pass P); d1 THE INVARIANT ROW — the full gap/pid/P-kind matrix plus a wrapped-pid row: P passed in 0 rows; d2 MERGE-FIRST PRESERVED — with later builders behind X; d3 a third ticket at P's ns + 1 (T5); d4 the warning and one docker-kind arm; d5 the round-2 arms and --replace, --after, FIFO and refusals unchanged; d6 the tag reader; d7 mutants of a copy of the candidate; d8 prior work; d9 the live install and queue untouched. THE CROSSES: y1 RD-775 x RD-131 in rd464-ai-readiness-service; y2 RD-807's route cell on main's server entry point; y3 RD-131 x rd385; y4 both orders; y5 the locks; y6 C-185; y7 main moved; y8 the shipped set.

THE LIVE LOCK BASE (ruling s, H-34): every invocation of either copy of the lock tool for RD-821's rows goes through YOUR guard, which REFUSES an unset NEXUSAI_LOCK_BASE (the tool's default is the LIVE base) and any base outside your own qa-trees batch21 lock-bases dir; prove the guard with three controls (live refused, unset refused, yours accepted) before the first arm; export the variable in the same shell that execs the tool, per row. A builder's arms run filed on the live queue today for about 31 seconds because one export was missing — that must not happen here. Read the live queue before and after every arms run: entries carrying any of your arm tags must be 0, else STOP, withdraw only your own pids by the tool's clean path, and mail a QUESTION. Copy O's and gate 19's harnesses, re-point and hash them; never run them in place. RD-821's arms run unbelted (the tool's own ps, no socket) — say so.

PRIOR WORK (ruling r): verify each READY's PRIOR WORK section claim by claim against history for anything it says was replaced or removed (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every git member's verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff in Tuesday's ruled order (T1; the proposal: RD-807 MT-C, RD-131 MT-B, RD-775 MTF; slots where T1 puts them). RD-821 never enters a tree. Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MTF on node_modules proven for M0's lock 19477a9 with proxy-addr 2.0.8 read from the tree's own path (RD-827, C-205): predicted 4448/279, re-based on YOUR M0; the measurement decides. A second clone in the reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes). C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes package.json or the lock. THREE locks (T2): e9063d4 (proxy-addr 2.0.7) at RD-807's own tree and its parents; d6d3b6e (proxy-addr 2.0.8) at RD-775's and RD-131's heads and bases; 19477a9 (proxy-addr 2.0.8, d6d3b6e with only the root version changed) at M0 and every merged tree. EACH TREE USES ITS OWN INSTALL, RESOLVED FROM ITS OWN LOCK (RD-827). There is NO npm registry exception in this gate. ONCE PER LOCK: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline — and EVERY npm invocation, the first one included, carries npm_config_update_notifier=false; prove the cache copy's _update-notifier-last-checked marker absent or unchanged. An ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install, never npm audit, never npx playwright install. sqlite3's binding: the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in your tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on it is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree of the same lock; never from another gate's trees.

THE BROWSER LEG (ruling q, H-32): Playwright 1.62.1 from YOUR OWN tree's node_modules, channel chrome (the local Google Chrome), HEADLESS, NO browser download — prove ~/Library/Caches/ms-playwright unchanged before and after; only http://127.0.0.1:<port> of a server YOU booted from YOUR tree, open mode, SESSION_SECRET UNSET; every non-127.0.0.1 request aborted by the page route AND the belt; never plant, edit or inject DOM rows; every caption "local run of <sha> — NOT the demo; Chrome headless via Playwright 1.62.1; synthetic feed". If Chrome or Playwright cannot launch, b2 is NOT RUN, named — never replaced by a jsdom render.

FULL VERIFY of each git head and of MTF through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers, servers, the browser), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 537741c 4387/274, e7d2cd1 4391/274, ff5d725 4312/265, MTF 4448/279. RULING (b) and its EXTENSION (carried as ruling (o)): if the full verifies, the counts regeneration or the TIER-2 cell holds remain lock-starved about 2 h after filing, deliver with them NAMED NOT RUN — never "skipped" — and say in the NOT TESTED section that each member's merge hold full verify plus its PR's CI Build plus the builder's own proof hold are the gate's NOT-RUN coverage, and any red there outside C-185's known set at merge is a STOP, not a re-run. The TIER-1 cell rows (RD-775's a0, a1, a5) are NOT covered by that extension: they run, and a TIER-1 verdict whose cell rows did not run is PROVISIONAL and releases nothing. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file (bash -n a mutated lock-tool copy) and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-34 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker; mask GUIDs; RD-775's key marker is a needle too. H-2: seed BEFORE; every boot is a NEW process — declare it per row. H-3: a LANDING CONTROL for every stored value, stand-in, listener, observer, browser observer, scratch lock base, filer and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd; request bodies byte-exact from a file. H-15: preloads with -r in argv; only test-only observers from your tree and RD-807's own preload and widener. H-16: every plant checked to be what the product will treat it as. H-17: your own censuses use pgrep, never ps. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading, gates 19 and 20's consolidation): ONE focused hold at a time, at most about 40 minutes of planned jest, rows GROUPED into as few holds as fit and a hold whose plan would overrun SPLIT, never stretched; the TIER-1 hold H1 is filed FIRST; every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output; each hold carries a wait deadline, and BEFORE it fires you file --replace on your own still-waiting ticket under the SAME tag. H-29: other gates' evidence is method only. H-31: offline node_modules per lock, the notifier off, and the cached sqlite3 prebuild. H-32: NO image built (the shipped-blob rows are a manifest evaluation); ONE local browser leg. H-33: stored values, stand-ins, listeners, filers and children counted and reaped or quarantined, never rm. H-34: the live lock base guard. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch21.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; other gates' trees and report dirs are never touched; copy instruments BY COPY from gate 20's evidence/inst (its HOLD20.sh and env20.sh hard-code gate 20's dirs and its qa-floorlib20.sh carries stale ROOT and NEG defaults: re-point and correct your copies; its qa-file20.sh CARRIES THE RETIRED YIELD — your copy removes that block and you quote the diff) and gate 19's qa-d807race19.js and qa-f3-19.sh (hash each copy against the brief's sha256). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, probe, measure, screen, mutate, arms or census scripts in place. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, no swap of the lock tool. No Azure (no az at all), no Microsoft, Azure OpenAI or Log Analytics host, no login host, no CDN, no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with the builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, hashes, reads, merge-trees in scratch objects, the offline npm ci, plain-node, server, browser and lock-arms rows, census greps); then file your holds tagged qa-b21-, one at a time, through the INSTALLED tool only; no tag of yours contains the word "merge" (C-141 ADDENDUM 7: only a merge HOLD's tag does). If a MERGE ticket is queued ahead of you, wait behind it. RULING (i)'s BY-HAND GATE YIELD IS RETIRED from gate 21 on (gate 19's RELEASE, item 5): you NEVER stop your own waiter to re-file behind a merge that filed after you — the installed tool places merges; if you see a live merge sort ahead of your own waiting ticket after you filed, quote it for row d9, never re-file because of it. AT A WAIT DEADLINE, first in line or not: use --replace on your own still-waiting ticket BEFORE its deadline fires (C-141 ADDENDUM 6: a SAME-PLACE handover; it is refused once the old waiter has left, so a late re-file lands at the tail) and confirm from the queue listing that the old ticket went to released/ as ticket-left-* and your place is unchanged; never two live holds; a duplicate-tag refusal takes a -r<N> suffix, said in the report; you never move ahead of anything that was ahead of you; one report line per re-file with the queue place before and after FROM THE QUEUE LISTING. Once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result, including every server you boot outside a hold; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver, server, browser arm, lock-arms row and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the three member branches, refs/pull/70/head and main (and each SLOT's branch if it joins), plus RD-821's two sha256s — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head or hash that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so; it must be b6c506a or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch21. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch21] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-12-gate-batch21/report.md
Write its VERDICTS and FINDINGS table early and keep it current: gate 19's session died before it assembled its report, and its verdict body was the only record.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 21
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-775 @ 537741c with its key row and CodeQL condition, RD-131 @ e7d2cd1 with the browser leg and the formula-cell control, RD-807 @ ff5d725 with the torn-read and load rows, RD-821 r3 @ sha256 3c33f5ae with the invariant and merge-first; a SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured in both orders, the C-57 and C-133 result, THE CROSSES, which rows ran on Opus 4.8 (or none), which full verifies and TIER-2 cell holds ran and which are NAMED NOT RUN under ruling (b) extended, and "CodeQL NOT RUN (no PR) for RD-131, RD-807; not applicable to RD-821; PR #70 read for RD-775". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A9, L-B1 to L-B9, L-C1 to L-C9, L-D1 to L-D7 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-209, C-141 with ADDENDA 5, 6 and 7, C-208, C-205, C-210, C-185 with its ADDENDA, C-190 with its ADDENDUM, C-192, C-02 and C-40 are the clarifications this batch leans on; C-01, C-20, C-34, C-49, C-57, C-68, C-76, C-89, C-97, C-102, C-104, C-112, C-115, C-125, C-130, C-133, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any member head without a pull_request Build (RD-775's included unless the gate's read finds one on 537741c), CodeQL at any head without a PR, main's CodeQL alert #69 (closure read only after merge, C-209), a real Azure OpenAI endpoint, a real Log Analytics or Azure Monitor endpoint (the drum table came from the synthetic feed), real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO) and its synthetic feed as deployed, any deployed environment, headed Chrome, Firefox, Safari and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only, off-host requests aborted), the probe rename on Windows or a network filesystem, the jest-lock candidate as INSTALLED or on the live queue (every arm ran on a scratch lock base; the swap is not the gate's), the docker lock kind beyond one arm, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
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
for S in "$MAIN_SHA" "$MB_A" "$MB_B" "$C_BASE" "$C_RED" "$MB_C" "$B90" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases with main and the stacks.
mb_is() { [ "$(g merge-base "$1" "$2" 2>/dev/null)" = "$3" ]; }
mb_is "$A_HEAD" "$MAIN_SHA" "$MB_A" || { echo "REFUSING: merge-base(RD-775, b6c506a) is not 41c5a47 — re-brief" >&2; exit 7; }
mb_is "$B_HEAD" "$MAIN_SHA" "$MB_B" || { echo "REFUSING: merge-base(RD-131, b6c506a) is not 7d11359 — re-brief" >&2; exit 7; }
mb_is "$C_HEAD" "$MAIN_SHA" "$MB_C" || { echo "REFUSING: merge-base(RD-807, b6c506a) is not 4332fb0 — re-brief" >&2; exit 7; }
for PAIR in "$C_BASE $C_HEAD" "$C_RED $C_HEAD" "$MB_C $C_BASE" "$MB_A $MAIN_SHA" "$MB_B $MAIN_SHA" "$MB_C $MAIN_SHA" "$MB_B $MB_A" "$B90 $MB_A" "$B90 $MB_B"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  g merge-base --is-ancestor "$X" "$Y" 2>/dev/null || { echo "REFUSING: ${X:0:7} is not an ancestor of ${Y:0:7} — a stack or base moved; re-brief" >&2; exit 7; }
done
if g merge-base --is-ancestor "$B90" "$MB_C" 2>/dev/null; then echo "REFUSING: 90b2556 is an ancestor of 4332fb0 — RD-807's old-lock premise (WRONG 11) is stale; re-brief" >&2; exit 7; fi
if g merge-base --is-ancestor "$C_BASE" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: RD-807 round 1 (9b15a99) is already on b6c506a — the brief's carried-round-1 premise is stale; re-brief" >&2; exit 7; fi

# 8 — chains exact: A 3 on 41c5a47; B 2 on 7d11359; C 3 on 9b15a99 (6 on 4332fb0); none with a merge.
chain_ok() { local base="$1" head="$2" n="$3" mg="$4" got m
  got="$(g rev-list --count "${base}..${head}" 2>/dev/null)"; m="$(g rev-list --merges --count "${base}..${head}" 2>/dev/null)"
  [ "$got" = "$n" ] && [ "$m" = "$mg" ] && g merge-base --is-ancestor "$base" "$head" 2>/dev/null; }
chain_ok "$MB_A" "$A_HEAD" 3 0  || { echo "REFUSING: RD-775 is not THREE non-merge commits on 41c5a47" >&2; exit 8; }
chain_ok "$MB_B" "$B_HEAD" 2 0  || { echo "REFUSING: RD-131 is not TWO non-merge commits on 7d11359" >&2; exit 8; }
chain_ok "$C_BASE" "$C_HEAD" 3 0 || { echo "REFUSING: RD-807's fix round is not THREE non-merge commits on 9b15a99" >&2; exit 8; }
chain_ok "$MB_C" "$C_HEAD" 6 0  || { echo "REFUSING: RD-807 (round 1 + fix round) is not SIX non-merge commits on 4332fb0" >&2; exit 8; }
[ "$(g rev-parse "${C_RED}^" 2>/dev/null)" = "$C_BASE" ] || { echo "REFUSING: RD-807's red-first commit 408115c is not directly on 9b15a99" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the three member branches + PR #70's head exactly the pins (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "$PR70_REF" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "refs/heads/$A_BRANCH $A_HEAD" "$PR70_REF $A_HEAD" "refs/heads/$B_BRANCH $B_HEAD" "refs/heads/$C_BRANCH $C_HEAD"; do
  RF="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]${RF}\$" || {
    echo "REFUSING: origin $RF is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY move (ruling b). It must be b6c506a or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member-ONLY path moved REFUSES; anything else is a NOTE.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from b6c506a — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$C_BASE"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
ONLY_PATHS="$(printf '%s\n' "$AIR" "$T775" "$IDX" "$T131" "$INC" "$T807" "$P807" "$W807" "$PKG" | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$ONLY_PATHS") <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved b6c506a..${M_ORIGIN:0:7} and touched a member-only path: $HIT — re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$SV" "$LOCK" "$TS" "$TSH" "$R465" "$R549" "$DKF" "$DIG" "$T464" "$T385" '__tests__/helpers/image-manifest.js' | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— C-68 sets / node_modules proofs / the crosses run on M0's blobs (brief ruling b, y7)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from b6c506a) — the gate re-pins M0 itself and re-bases every prediction" >&2
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — RD-821 round 3 (D): BOTH files PINNED by sha256 (REFUSE if either moved); the 23-line diff; the candidate's rule; the live default base; O's harness guard.
INST_NOW="$(fsha "$LOCKTOOL")"; CAND_NOW="$(fsha "$CANDIDATE")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED jest-lock tool's sha256 is '${INST_NOW:-absent}', not fd223bd2… — swapped or edited before gate 21's verdict; re-brief (and raise it)" >&2; exit 90; }
[ "$CAND_NOW" = "$LOCK_SHA_CAND" ] || { echo "REFUSING: the RD-821 candidate's sha256 is '${CAND_NOW:-absent}', not 3c33f5ae… — the candidate moved; re-read O's READY and re-brief" >&2; exit 90; }
DL="$(diff "$LOCKTOOL" "$CANDIDATE" 2>/dev/null | grep -c '^[<>]')"
[ "$DL" = "23" ] || { echo "REFUSING: diff installed vs candidate is $DL changed lines, not 23 (WRONG 14)" >&2; exit 90; }
grep -qF 'if [ "$me" -gt "$p_pid" ]; then v=$pn; else v=$((pn + 1)); fi' "$CANDIDATE" && grep -qF 'behind=1' "$CANDIDATE" && grep -qF 'filed directly after $p_tag (not passed), so builder $x_tag stays ahead' "$CANDIDATE" \
  || { echo "REFUSING: the candidate's gap-0/1 rule / behind flag / warning are not as briefed (d1/d4's premise)" >&2; exit 90; }
grep -qF 'filed at $x_tag'"'"'s ns, so $x_tag may stay ahead' "$LOCKTOOL" || { echo "REFUSING: the installed tool's round-2 fallback (filed at X's ns) is not as briefed (d0's control)" >&2; exit 90; }
for F in "$LOCKTOOL" "$CANDIDATE"; do
  grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks}"' "$F" || { echo "REFUSING: $F's default lock base is not the LIVE base as briefed (H-34's premise)" >&2; exit 90; }
  bash -n "$F" 2>/dev/null || { echo "REFUSING: $F does not parse (bash -n)" >&2; exit 90; }
  grep -qF -- '--replace' "$F" || { echo "REFUSING: $F has no --replace — ruling (i)'s re-file instrument / d5's premise is missing" >&2; exit 90; }
done
grep -qF 'REFUSED: lock base $NEXUSAI_LOCK_BASE is not a scratch base' "$ST/s96o/f821-arms.sh" || echo "NOTE: O's f821-arms.sh no longer carries its scratch-base refusal — the gate's own H-34 guard is the only one" >&2

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no package change; product paths as commissioned.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MB_A" "$A_HEAD" "$A_EXPECTED_FILES" "RD-775 (41c5a47..537741c)"
chk_delta "$MB_B" "$B_HEAD" "$B_EXPECTED_FILES" "RD-131 (7d11359..e7d2cd1)"
chk_delta "$C_BASE" "$C_HEAD" "$C_EXPECTED_FILES" "RD-807 fix round (9b15a99..ff5d725)"
chk_delta "$MB_C" "$C_HEAD" "$C_MB_EXPECTED_FILES" "RD-807 (4332fb0..ff5d725)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$MB_A" "$A_HEAD" "$AIR")" = "27 4" ] && [ "$(ns "$MB_A" "$A_HEAD" "$T775")" = "124 0" ] \
  || { echo "REFUSING: RD-775's numstats are not aiReadiness +27/-4, rd775 +124" >&2; exit 22; }
[ "$(ns "$MB_B" "$B_HEAD" "$IDX")" = "43 0" ] && [ "$(ns "$MB_B" "$B_HEAD" "$T131")" = "178 0" ] \
  || { echo "REFUSING: RD-131's numstats are not index.js +43, rd131 +178" >&2; exit 22; }
[ "$(ns "$C_BASE" "$C_HEAD" "$P807")" = "7 1" ] && [ "$(ns "$C_BASE" "$C_HEAD" "$W807")" = "34 0" ] && [ "$(ns "$C_BASE" "$C_HEAD" "$T807")" = "87 0" ] \
  || { echo "REFUSING: RD-807 fix round's numstats are not preload +7/-1, widener +34, rd807 +87" >&2; exit 22; }
for PAIR in "$A_HEAD $MB_A" "$B_HEAD $MB_B" "$C_HEAD $MB_C"; do
  H="${PAIR%% *}"; Bz="${PAIR#* }"
  [ -z "$(g diff --name-only "$Bz" "$H" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} changes package-lock.json/package.json over its base — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
prod() { g diff --name-only "$1" "$2" -- backend static docs Dockerfile .dockerignore .github model-config.js 2>/dev/null | sort; }
[ "$(prod "$MB_A" "$A_HEAD")" = "$AIR" ] || { echo "REFUSING: RD-775 touches a product path beyond aiReadiness.js" >&2; exit 22; }
[ "$(prod "$MB_B" "$B_HEAD")" = "$IDX" ] || { echo "REFUSING: RD-131 touches a product path beyond static/js/index.js" >&2; exit 22; }
[ -z "$(prod "$C_BASE" "$C_HEAD")" ] || { echo "REFUSING: RD-807's fix round touches a product path — it is commissioned TEST-ONLY" >&2; exit 22; }

# 93 — RD-775's premises at source (incl. WRONG 1-2).
[ "$(blob "$MB_A" "$AIR")" = "$AIR_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$AIR")" = "$AIR_M_BLOB" ] && [ "$(blob "$A_HEAD" "$AIR")" = "$AIR_A_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$T775")" = "$T775_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T775")" ] && [ "$(blob "$A_HEAD" "$T464")" = "$T464_BLOB" ] && [ "$(blob "$MAIN_SHA" "$T464")" = "$T464_BLOB" ] \
  || { echo "REFUSING: RD-775's blobs are not aiReadiness 7db38ea -> 578e7e7 / rd775 0cca0e0 (new) / rd464-ai-readiness-service 035f489" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$AIR" 'createHash')" = "0" ] && [ "$(cnt "$MB_A" "$AIR" "crypto.createHash('sha256')")" = "1" ] && [ "$(cnt "$A_HEAD" "$AIR" 'const READINESS_KEY_ID_CAP = 64;')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$AIR" 'if (keyIds.size >= keyIdCap) keyIds.clear();')" = "1" ] && [ "$(cnt "$A_HEAD" "$AIR" '`key#${keyIdOf(a.apiKey)}`')" = "1" ] \
  || { echo "REFUSING: aiReadiness.js at 537741c is not the no-hash id map with the 64 cap as briefed (a2/a3's premise)" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$AIR" 'verdicts.set(')" = "1" ] && [ "$(cnt "$A_HEAD" "$AIR" 'verdicts.delete')" = "0" ] || echo "NOTE: aiReadiness.js's verdict cache now has an eviction — brief WRONG 1 / T3 may be stale" >&2
[ "$(g show "${A_HEAD}:${T775}" 2>/dev/null | grep -cE '^[[:space:]]*test\(')" = "5" ] || { echo "REFUSING: rd775 is not 5 test() cells" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$SV" "const aiReadiness = createAiReadiness({ aiGate });")" = "1" ] || { echo "REFUSING: the server entry point does not build aiReadiness with the default cap as briefed" >&2; exit 93; }

# 95 — RD-131's premises at source (incl. WRONG 5, 8, 9).
[ "$(blob "$MB_B" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$B_HEAD" "$IDX")" = "$IDX_B_BLOB" ] \
  && [ "$(blob "$B_HEAD" "$T131")" = "$T131_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T131")" ] \
  || { echo "REFUSING: RD-131's blobs are not index.js ae59c25 -> 8ab3664 / rd131 098c5fc (new)" >&2; exit 95; }
[ "$(cnt "$B_HEAD" "$IDX" 'function fleetHealthDrumCsvRows(esc) {')" = "1" ] && [ "$(cnt "$B_HEAD" "$IDX" 'fleetHealthDrumCsvRows(esc);')" = "2" ] \
  && [ "$(cnt "$B_HEAD" "$IDX" "'=== DRUM STATUS ===\\n'")" = "1" ] && [ "$(cnt "$B_HEAD" "$IDX" "'=== FLEET HEALTH - DRUM STATUS ===\\n'")" = "1" ] \
  && [ "$(cnt "$B_HEAD" "$IDX" 'if (cells.length < 6) continue;')" = "3" ] && [ "$(cnt "$MB_B" "$IDX" 'if (cells.length < 6) continue;')" = "2" ] \
  || { echo "REFUSING: RD-131's helper / its two call sites / the 6-cell skip are not as briefed (b2/b4's premise)" >&2; exit 95; }
ESC_FRAG='.toString().replace(/"/g, '\''""'\'')}"'
[ "$(cnt "$B_HEAD" "$IDX" "$ESC_FRAG")" -ge 2 ] 2>/dev/null && [ "$(cnt "$B_HEAD" "$IDX" "$ESC_FRAG")" -ge "$(cnt "$B_HEAD" "$IDX" 'const esc = (val) =>')" ] \
  || echo "NOTE: the exports' esc is no longer quote-doubling only — brief WRONG 8 / b3's prediction may be stale" >&2
[ "$(g show "${B_HEAD}:${T131}" 2>/dev/null | grep -cE '^[[:space:]]*test\(')" = "9" ] || { echo "REFUSING: rd131 is not 9 test() cells (F1-F6, A1-A3)" >&2; exit 95; }
[ "$(cnt "$MAIN_SHA" "$SV" "const USE_SYNTHETIC_FEED = process.env.SYNTHETIC_DEMO_FEED === 'true' || process.env.SYNTHETIC_DEMO_FEED === '1';")" = "1" ] \
  && [ "$(cnt "$MAIN_SHA" "$SV" "const USE_AZURE_LOG_ANALYTICS = process.env.USE_AZURE_LOG_ANALYTICS === 'true' || process.env.USE_AZURE_LOG_ANALYTICS === '1';")" = "1" ] \
  || { echo "REFUSING: the synthetic-feed / Log Analytics switches the browser leg uses are not at b6c506a as briefed (b2's premise)" >&2; exit 95; }

# 96 — RD-807's premises at source (incl. WRONG 10-12).
[ "$(blob "$MB_C" "$INC")" = "$INC_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$INC")" = "$INC_M_BLOB" ] && [ "$(blob "$C_BASE" "$INC")" = "$INC_C_BLOB" ] && [ "$(blob "$C_HEAD" "$INC")" = "$INC_C_BLOB" ] \
  && [ "$(blob "$C_BASE" "$T807")" = "$T807_R1_BLOB" ] && [ "$(blob "$C_HEAD" "$T807")" = "$T807_BLOB" ] \
  && [ "$(blob "$C_BASE" "$P807")" = "$P807_R1_BLOB" ] && [ "$(blob "$C_HEAD" "$P807")" = "$P807_BLOB" ] && [ "$(blob "$C_HEAD" "$W807")" = "$W807_BLOB" ] && [ -z "$(blob "$C_BASE" "$W807")" ] \
  || { echo "REFUSING: RD-807's blobs are not incidents 740be8d -> 988969a (round 1, unchanged by the fix round) / rd807 16cfdeb -> 790c024 / preload 6f6b8a1 -> 722e2b9 / widener b917f8a (new)" >&2; exit 96; }
[ "$(cnt "$C_HEAD" "$P807" 'const tmp = `${file}.${process.pid}.tmp`;')" = "1" ] && [ "$(cnt "$C_HEAD" "$P807" 'fs.renameSync(tmp, file);')" = "1" ] \
  && [ "$(cnt "$C_BASE" "$P807" 'fs.writeFileSync(file, JSON.stringify(out));')" = "1" ] && [ "$(cnt "$C_HEAD" "$W807" 'Atomics.wait(cell, 0, 0, ms);')" = "1" ] \
  || { echo "REFUSING: the temp+rename preload / the in-place base / the widener's stall are not as briefed (c0/c2's premise)" >&2; exit 96; }
[ -z "$(comm -23 <(titles "$C_BASE" "$T807" | sort) <(titles "$C_HEAD" "$T807" | sort))" ] && [ "$(titles "$C_HEAD" "$T807" | wc -l | tr -d ' ')" = "9" ] \
  || { echo "REFUSING: rd807 loses a test title across the fix round, or is not 9 test lines (13 ids) — the 'missing 0' prediction is stale" >&2; exit 96; }
[ "$(cnt "$C_HEAD" "$T807" "env: { ...process.env, RD807_PROBE_FILE: file, RD807_TEAR_STALL_MS: '40' },")" = "1" ] || echo "NOTE: rd807's child env spread is not as briefed — WRONG 12 may be stale" >&2

# 98 — shared blobs; the THREE locks as briefed; proxy-addr per lock (RD-827).
for S in "$MB_A" "$A_HEAD" "$MB_B" "$B_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_MID" ] && [ "$(blob "$S" "$PKG")" = "$PKG_OLD" ] || { echo "REFUSING: lock / package.json at ${S:0:7} are not d6d3b6e / cdb1168 (T2)" >&2; exit 98; }
done
for S in "$MB_C" "$C_BASE" "$C_RED" "$C_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_OLD" ] && [ "$(blob "$S" "$PKG")" = "$PKG_OLD" ] || { echo "REFUSING: lock / package.json at ${S:0:7} are not e9063d4 / cdb1168 (T2)" >&2; exit 98; }
done
[ "$(blob "$MAIN_SHA" "$LOCK")" = "$LOCK_NEW" ] && [ "$(blob "$MAIN_SHA" "$PKG")" = "$PKG_NEW" ] || { echo "REFUSING: lock / package.json at b6c506a are not 19477a9 / 384805d (T2)" >&2; exit 98; }
[ "$(g diff "$LOCK_MID" "$LOCK_NEW" 2>/dev/null | grep -c '^[-+] ')" = "4" ] && [ "$(g diff "$LOCK_MID" "$LOCK_NEW" 2>/dev/null | grep '^[-+] ' | grep -vc '"version": "')" = "0" ] \
  || { echo "REFUSING: 19477a9 is not d6d3b6e with only the root version changed (WRONG 17 / T2)" >&2; exit 98; }
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] && [ "$(blob "$S" "$TSH")" = "$TSH_BLOB" ] && [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] \
    && [ "$(blob "$S" "$R549")" = "$R549_BLOB" ] && [ "$(blob "$S" "$R465")" = "$R465_BLOB" ] \
    || { echo "REFUSING: test-server / helper / Dockerfile / .dockerignore / rd549 / rd465 at ${S:0:7} are not as briefed (cff1e54 …)" >&2; exit 98; }
done
[ "$(blob "$MAIN_SHA" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$A_HEAD" "$SV")" = "$SV_AB_BLOB" ] && [ "$(blob "$B_HEAD" "$SV")" = "$SV_AB_BLOB" ] && [ "$(blob "$C_HEAD" "$SV")" = "$SV_C_BLOB" ] \
  || { echo "REFUSING: the server entry point's blobs are not c8ca2b3 (M0) / 703f429 (A, B) / 2684acd (C) — y2's premise" >&2; exit 98; }
[ "$(lockver "$LOCK_OLD" proxy-addr)" = "2.0.7" ] && [ "$(lockver "$LOCK_MID" proxy-addr)" = "2.0.8" ] && [ "$(lockver "$LOCK_NEW" proxy-addr)" = "2.0.8" ] \
  && [ "$(lockver "$LOCK_OLD" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_MID" playwright)" = "1.62.1" ] && [ "$(lockver "$LOCK_NEW" playwright)" = "1.62.1" ] \
  || { echo "REFUSING: proxy-addr is not 2.0.7 (e9063d4) / 2.0.8 (d6d3b6e, 19477a9), or playwright is not 1.62.1 in all three (T2, ruling q)" >&2; exit 98; }

# 23 — EXPECTED OVERLAPS (beyond the counts file): none with main since any base; no member pair shares a path; the A x B semantic meeting is in rd464-ai-readiness-service.
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
[ "$(cnt "$MAIN_SHA" "$T464" 'aiReadiness')" -ge 1 ] 2>/dev/null && [ "$(cnt "$MAIN_SHA" "$T464" 'js/index.js')" -ge 1 ] 2>/dev/null \
  || echo "NOTE: rd464-ai-readiness-service no longer reads both aiReadiness and static/js/index.js — cross y1 may be stale" >&2
[ "$(cnt "$MAIN_SHA" "$T385" 'js/index.js')" -ge 1 ] 2>/dev/null || echo "NOTE: rd385 no longer reads static/js/index.js — cross y3 may be stale" >&2

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$MB_A 4382 273" "$A_HEAD 4387 274" "$MB_B 4382 273" "$B_HEAD 4391 274" "$MB_C 4299 264" "$C_BASE 4310 265" "$C_RED 4310 265" "$C_HEAD 4312 265" "$MAIN_SHA 4421 276"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$MB_A" "$A_HEAD" "$MB_B" "$B_HEAD" "$MB_C" "$C_BASE" "$C_RED" "$C_HEAD" "$MAIN_SHA"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "319 320 319 320 309 311 312 312 324 " ] || { echo "REFUSING: the __tests__ census (41c5a47 A 7d11359 B 4332fb0 9b15a99 408115c C M0) is '$CENSUS', not '319 320 319 320 309 311 312 312 324'" >&2; exit 35; }

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
[ -d "$CHROME_APP" ] || echo "NOTE: $CHROME_APP is absent — b2 (the browser leg) will be NOT RUN, named (ruling q)" >&2
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
[ -s "$O_ANSWER" ] && grep -qF 'Gate 21 tests against the invariant, not against the wording.' "$O_ANSWER" \
  && grep -qF 'The swap happens only after gate 21' "$O_ANSWER" || { echo "REFUSING: Tuesday's ruling (a) on RD-821 r3 (test the invariant; no swap before a GO) is not at $O_ANSWER as quoted" >&2; exit 70; }
[ -s "$N_ANSWER" ] && grep -qF 'Never plant DOM rows.' "$N_ANSWER" || { echo "REFUSING: Tuesday's Q2 (a) ruling for RD-131's browser leg is not at $N_ANSWER as quoted" >&2; exit 70; }
grep -qF 'ln -s ../../worktrees/mkt-rc-selfcontained-s62/node_modules' "$C57_RUNNER" || echo "NOTE: the shared C-57 runner no longer links the 2.0.7 install — RD-837 may be fixed; WRONG 21 may be stale" >&2

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean.
MT_PAIRS=0
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$M_ORIGIN $C_HEAD" "$A_HEAD $B_HEAD" "$A_HEAD $C_HEAD" "$B_HEAD $C_HEAD"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — READYs, the project briefs, builder evidence, prior reports, gate 20/19's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$PBRIEF_A" "$PBRIEF_C" "$CLAR" "$C133" "$BRIEF20" "$B20_REPORT" "$B19_BODY0" "$B19_BODY2" "$B19_F3" "$B19_RACE" "$B19_F3SH" \
         "$ST/s92r/hold-05.log" "$ST/s87n/rd131-hold2.out" "$ST/s87n/union-rd131.lst" "$ST/s94n/rd131-browser2.out" "$ST/s94n/rd131-browser2/after-fleet-health.csv" \
         "$ST/s97r/hold-01.sh" "$ST/s97r/hold-01.log" "$ST/s97r/jira-807-02.txt" \
         "$ST/s96o/arms-inst.log" "$ST/s96o/arms-new.log" "$ST/s96o/r2-arms-inst.log" "$ST/s96o/r2-arms-new.log" "$ST/s96o/f821-arms.sh" "$ST/s96o/slip-log.md" "$ST/s96o/c-rd821r3.txt" "$C57_RUNNER" \
         "$B20_INST/HOLD20.sh" "$B20_INST/env20.sh" "$B20_INST/qa-holdlib20.sh" "$B20_INST/qa-floorlib20.sh" "$B20_INST/qa-floorcount.py" "$B20_INST/qa-to.sh" "$B20_INST/qa-jestwrap.sh" "$B20_INST/qa-jsum.js" \
         "$B20_INST/qa-runj20.sh" "$B20_INST/qa-mut20.py" "$B20_INST/qa-mutlib20.sh" "$B20_INST/qa-merge20.sh" "$B20_INST/qa-build20.sh" "$B20_INST/qa-npm20.sh" "$B20_INST/qa-file20.sh" \
         "$B20_INST/qa-wait20.py" "$B20_INST/qa-verify20.sh" "$B20_INST/qa-h1-selftest20.sh" "$B20_INST/qa-h1-scan.py" "$B20_INST/qa-mail.py" "$B20_INST/qa-mailread.py" "$B20_INST/qa-lockcheck.py" \
         "$B20_INST/qa-ssprint.sh" "$B20_INST/qa-netbelt.sb" "$B20_INST/qa-netbelt-nodns.sb" "$B20_INST/qa-netbelt-ctl.js" "$B20_INST/qa-c57-id-superset.sh" "$B20_INST/qa-cov-setup.js" \
         "$B20_INST/qa-srv20.js" "$B20_INST/qa-manifest20.js" "$B20_INST/qa-c3.js" "$B20_INST/qa-qlist20.sh" "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "${C_HEAD:0:7}" "$READY_C" && grep -qF "${C_BASE:0:7}" "$READY_C" \
  && grep -qF "$LOCK_SHA_CAND" "$READY_D" && grep -qF "$LOCK_SHA_INST" "$READY_D" && grep -qF "${A_HEAD:0:7}" "$PBRIEF_A" && grep -qF "${C_HEAD:0:7}" "$PBRIEF_C" \
  && grep -qF 'PRIOR WORK' "$READY_A" && grep -qF 'PRIOR WORK' "$READY_B" && grep -qF 'PRIOR WORK' "$READY_C" && grep -qF 'PRIOR WORK' "$READY_D" \
  && grep -qF 'PRIOR WORK (C-49)' "$PBRIEF_A" && grep -qF 'PRIOR WORK (C-49)' "$PBRIEF_C" && grep -qF 'DEVIATION' "$READY_D" \
  || { echo "REFUSING: a READY does not name its head (or RD-821 its two sha256s), a PRIOR WORK section is missing, or RD-821's DEVIATION is not declared" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4387/4387 tests passed across 274 suites (jest exit 0)' "$ST/s92r/hold-05.log" && grep -qF '=== start fix=be8fb61' "$ST/s92r/hold-05.log" \
  && grep -qF 'VERDICT: PASS — 4391/4391 tests passed across 274 suites (jest exit 0)' "$ST/s87n/rd131-hold2.out" \
  && grep -qF 'Full verify at 3705e03: VERDICT: PASS — 4312/4312' "$ST/s97r/jira-807-02.txt" \
  && [ "$(grep -c 'DEMO-HP' "$ST/s94n/rd131-browser2/after-fleet-health.csv")" = "20" ] \
  || { echo "REFUSING: a builder log no longer carries the line the brief quotes (WRONG 3, 6, 7, 13's premise)" >&2; exit 31; }
grep -qF 'F-807-1' "$B19_BODY0" && grep -qF 'F-821-1' "$B19_BODY0" && grep -qF 'f3 THE PLACEMENT ROW' "$B19_BODY2" && grep -qF 'merge passed P: YES' "$B19_F3" \
  || { echo "REFUSING: gate 19's verdict body / RD-821 section / f3-placement evidence no longer read as the brief quotes" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B20_REPORT" || { echo "REFUSING: gate 20's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
[ "$(fsha "$B19_RACE")" = "$B19_RACE_SHA" ] || { echo "REFUSING: gate 19's qa-d807race19.js is not sha256 face4538… (c2's instrument; RD-807's READY names it)" >&2; exit 31; }
[ "$(fsha "$B19_F3SH")" = "$B19_F3SH_SHA" ] || { echo "REFUSING: gate 19's qa-f3-19.sh is not sha256 9edd3427… (d0/d1's instrument)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-54487\}' "$B20_INST/qa-floorlib20.sh" || echo "NOTE: gate 20's qa-floorlib20.sh ROOT default is no longer 54487 — the brief's 'STALE defaults' line names the old value" >&2
grep -qF 're-file --after <that merge tag>' "$B20_INST/qa-file20.sh" || echo "NOTE: gate 20's qa-file20.sh no longer carries the yield block the brief tells the gate to remove (WRONG 20)" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | 20' "$BRIEF20" || echo "NOTE: gate 20's brief does not read as stamped — the template reference may be stale" >&2

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
for P in "$B20_INST/" "$PBRIEF_A" "$PBRIEF_C" "2026-10-08_nexusai-rd775-READY-mail.txt" "2026-10-12_nexusai-rd131-READY-mail.txt" "2026-10-12_nexusai-rd807-f8071-READY-mail.txt" \
         "2026-10-12_nexusai-rd821r3-READY-mail.txt" "2026-10-08_nexusai-gate-batch20.md" "2026-10-12_nexusai_gate19_RELEASE.md" "2026-10-12_nexusai_O_S96O_plan_ANSWER.md" \
         "2026-10-12_nexusai_N_S94N_plan_ANSWER.md" "answer-starvation.txt" "qa-d807race19.js" "qa-f3-19.sh" "f3-placement.txt" "body-0.md" "qa-file20.sh"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in '**RD-775 is TIER 1**' '**RD-131 is TIER 2 + ONE BROWSER LEG + a FORMULA-CELL CONTROL.**' '**RD-807 F-807-1 is TIER 2, THROUGH CODE, TEST-ONLY, round 1 of 2 of the fix round.**' \
         '**RD-821 round 3 is TIER 2, THROUGH CODE, TOOLING, round 1 of 2 of the fix.**' 'THIS IS A TIERED GATE' \
         'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'THE BROWSER DRIVER' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' 'THE CROSSES' '--replace' 'qa-b21-' 'RETIRED' 'THE LIVE LOCK BASE' 'H-34' 'INVARIANT'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-775 (TIER 1' 'RD-131 (TIER 2 + ONE local browser leg + a formula-cell control' 'RD-807 F-807-1 fix round (TIER 2 through code, TEST-ONLY' 'RD-821 round 3 F-821-1 (TIER 2 through code, TOOLING' \
         'TIERED' 'one verdict per ticket' 'THE CROSSES' 'manifest evaluation' 'NO image built' 'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' \
         'Playwright 1.62.1' 'channel chrome' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-b21-' 'RETIRED' 'INVARIANT' 'THE LIVE LOCK BASE' 'H-34' 'never plant'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$MAIN_SHA" "$MB_A" "$MB_B" "$C_BASE" "$MB_C" "$LOCK_SHA_INST" "$LOCK_SHA_CAND"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$AIR_M_BLOB" "$AIR_A_BLOB" "$T775_BLOB" "$T464_BLOB" "$IDX_M_BLOB" "$IDX_B_BLOB" "$T131_BLOB" "$INC_M_BLOB" "$INC_C_BLOB" "$T807_R1_BLOB" "$T807_BLOB" \
         "$P807_R1_BLOB" "$P807_BLOB" "$W807_BLOB" "$SV_M_BLOB" "$SV_AB_BLOB" "$SV_C_BLOB" "$LOCK_OLD" "$LOCK_MID" "$LOCK_NEW" "$PKG_OLD" "$PKG_NEW" "$C_RED" "$B90"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
for S in "$C133_SHA" "$PREBUILD_SHA" "$B19_RACE_SHA" "$B19_F3SH_SHA"; do grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }; done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 21' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 21 has no priority member" >&2; exit 15; fi
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
# the gate's own tags must never read as a merge ticket (C-141 ADDENDUM 7): no 'qa-b21-…merge…' tag suggested anywhere.
[ "$(grep -oE 'qa-b21-[A-Za-z0-9_-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-b21- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-b21-[A-Za-z0-9_-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-b21- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED: neither the brief nor the prompt may instruct one; both must say it is retired. Then the jest queue as the launch finds it (read-only ls/grep).
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield (gate 19's RELEASE item 5)" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  BQ="$(grep -l '^tag=qa-b2[01]' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ qa-b20*/qa-b21* ticket(s) in the jest queue now — a live gate's: FIFO, never touched (or a stale gate-21 ticket: read before launch)" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 82 — THE MODEL RULE (Kam 2026-09-30 09:07, card (b)) is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31 (RE-BASED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-33 (RE-BASED' "$BRIEF" && grep -qF 'H-34 (NEW' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-33 (re-based)/H-34 (new)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-775 RD-131 RD-807 RD-821 RD-835 RD-827 RD-816 RD-837 C-209 C-141 C-208 C-205 C-210 C-185 C-190 C-192 C-02 C-40
C-01 C-20 C-34 C-49 C-57 C-68 C-76 C-89 C-97 C-102 C-104 C-112 C-115 C-125 C-130 C-133 C-174 C-186 ADDENDA%5,%6%and%7 RED-AT-PARENT RED-AT-BASE
a0 a2 a3 a4 a5 a6 a7 a8 a9 b0 b2 b3 b4 b5 b6 b7 b8 b9 b10 c0 c2 c3 c4 c5 c6 c7 c8 c9 c10 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 y1 y2 y3 y4 y5 y6 y7 y8
MT-C MT-B MTF M0 SLOTS JOINS KEY%ROW BOUND%ROW CODEQL%CONDITION BROWSER%LEG FORMULA-CELL%CONTROL TORN-READ%ROW LOAD%ROW INVARIANT%ROW MERGE-FIRST%PRESERVED
PR%#70 refs/pull/70/head refs/pull/58/head state=fixed #256-#259 #69 rd464-ai-readiness-service rd385 USE_AZURE_LOG_ANALYTICS=true SYNTHETIC_DEMO_FEED=true
4448/279 4421/276 4434/277 4443/278 4387/274 4391/274 4312/265 new%ids%27 missing%0 e9063d4 d6d3b6e 19477a9 2.0.7 2.0.8 proxy-addr
L-A1 L-A9 L-B1 L-B9 L-C1 L-C9 L-D1 L-D7 L-Y1 H-1 H-2 H-3 H-4 H-9 H-15 H-16 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 SCRATCH%object%dir git%clone%--shared REGENERATION ms-playwright
id-superset pull%request STOP POSITIVE%CONTROL%FIRST node%--check bash%-n VOID EXCLUSIVE qa-b21- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --replace SAME-PLACE%handover DEADLINE HEARTBEAT 2%minutes 5%minutes finally
SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center
npm%install --offline ENOTCACHED HOLD20.sh qa-floorlib20.sh qa-file20.sh qa-d807race19.js qa-f3-19.sh Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> GHSA-jqcg-44mw-7w3h instrument never%fixes
NEXUSAI_LOCK_BASE scratch%lock%bases 31%seconds GROUPED SPLIT never%dismissed PROVISIONAL"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 4b. TARGET B' '^## 4c. TARGET C' '^## 4d. TARGET D' \
         '^## 6. THE CROSSES' '^## 7. THE MERGED TREE' '^## 8. CI' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOTS' '^## PROVENANCE' '^### MERGE ORDER' \
         '^### TARGET A' '^### TARGET B' '^### TARGET C' '^### TARGET D' '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# the WRONG list sits ABOVE the rulings (the commission's order), and every WRONG item is marked MEASURED or READ-ONLY-INFERRED somewhere in its line.
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|Counts and census' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-A8 L-A9 L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-B9 L-C1 L-C2 L-C3 L-C4 L-C5 L-C6 L-C7 L-C8 L-C9 \
         L-D1 L-D2 L-D3 L-D4 L-D5 L-D6 L-D7 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 b0 b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 d0 d1 d2 d3 d4 d5 d6 d7 d8 d9 y1 y2 y3 y4 y5 y6 y7 y8; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
for R in s-0 s-1 s-2 s-3 s-4 s-5; do
  grep -qF "**$R " "$BRIEF" || { echo "REFUSING: brief lacks the SLOT row $R" >&2; exit 19; }
done
# every builder's stated scope / limits / interpretation lines carried verbatim (each line checked in its source AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; AP) F="$PBRIEF_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; CP) F="$PBRIEF_C" ;; D) F="$READY_D" ;; O) F="$O_ANSWER" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|NOT TESTED: #69 pre-merge; no real Azure OpenAI; NO CI Build on 537741c (only npm-audit push 37721133519 success, and CodeQL); the cap value is a judgement.
AP|No mutant for the no-leak cell: nothing in the product connects the key to a result, so there is nothing to mutate.
AP|The map holds raw keys in process memory.
B|The jest proof and the browser leg ran on the uncommitted tree whose index.js is byte-identical to e7d2cd1; the test file and counts were committed unchanged.
B|Synthetic feed only: no real Log Analytics workspace drove the drum table (C-20/C-34 territory; the demo's own render is behind RD-76).
B|The demo is NOT exercised; same commit, local run only.
B|Formula-cell neutralising stays RD-835's (F6 pins drum = consumables behaviour exactly).
C|The C-68 union under load and the Linux CI runner. The only loaded run was the one full verify.
C|M3 is probabilistic in principle.
C|The rename on Windows or a network filesystem (CI is Linux; this was APFS).
C|A leftover .tmp if the child dies between the write and the rename.
C|The forward merge onto main b6c506a (lock 2.0.8). That is the merge turn's job, with a fresh RD-827 own install, C-57 and C-68.
C|No PR CodeQL run (no PR exists for this branch yet) and no CI Build.
C|a retry on empty would also mask a dead or stale probe, which the precondition cell exists to see
D|A third live ticket at P's ns + 1 (the merge would sort by pid against it; by reading it is behind X, so it is a builder or a later gate).
D|The docker kind (the code path is kind-agnostic, not run).
D|The swap itself: after gate 21 GO only, no holder AND an empty queue read and quoted, atomic mv, the old file kept as nexusai-lock.sh.pre-1012-o-r3.
D|Live probe after a swap (none, because there is no swap).
O|Gate 21 tests against the invariant, not against the wording.
O|do NOT swap the candidate into session-tools/nexusai-lock.sh on an idle lock alone. The swap happens only after gate 21's verdict on RD-821 round 3 is GO
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
Its closure is read AFTER the merge, on main's push analysis, by alert number
is a SAME-PLACE handover.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
Addendum 2's "once PER WAITING GATE TICKET" means once per gate TAG.
A test's probe-hygiene cell FAILS ON ANY ENTRY in its probe directory, not only on its own pid's.
Leftovers are never cleaned up silently, because a cleanup would hide the crash that left them.
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
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b21-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may MOVE' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' \
         'ticket-left-*' 'never two live holds' '-r<N>' 'Every finding names its instrument' 'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'refused rc 99'; do
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
for w in 'RED-AT-PARENT' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4448/279' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' 'd6d3b6e' '19477a9' 'proxy-addr' 'RD-827' 'RD-837' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' \
         'keyIdOf' 'READINESS_KEY_ID_CAP' 'keyIdCap' 'verdicts.set' 'C-209' 'refs/pull/70/head' 'refs/pull/58/head' 'state=fixed' '#256-#259' '#69' \
         'fleetHealthDrumCsvRows' 'DRUM STATUS' 'USE_AZURE_LOG_ANALYTICS=true' 'SYNTHETIC_DEMO_FEED=true' 'never plant' 'RD-835' 'formula' \
         'renameSync' 'RD807_TEAR_STALL_MS' 'T1 CONTROL' 'precondition' 'qa-d807race19.js' 'C-208' \
         'NEXUSAI_LOCK_BASE' 'scratch lock base' 'f3-placement.txt' 'qa-f3-19.sh' 'INVARIANT' 'P is never passed' 'merge-first' 'behind' 'ruling (a)' 'DEVIATION' \
         'Playwright 1.62.1' "channel: 'chrome'" 'ms-playwright' 'GHSA-jqcg-44mw-7w3h' 'ANY rd465 O-1 failure' 'ADDENDUM SLOTS' 'S1 SLOT' 'S2 SLOT' \
         'WRONG 1' 'WRONG 8' 'WRONG 14' 'WRONG 16' 'WRONG 19' 'WRONG 20' 'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib20.sh' 'HOLD20.sh' 'qa-file20.sh' \
         'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31' 'never dismissed' 'RETIRED' 'wednesday' 'PROVISIONAL'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the ADDENDUM SLOTS (GENERIC): each EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
SLOT_STATE=''
SLOT_DESC=''
slot() {   # $1 = S1|S2
  local id="$1" J E sha br tier rdy now base PP tk
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
# the coordinator (T8): a pane named 'tuesday' OR 'wednesday' on this machine — exactly one of the two names live, exactly one pane.
COORD_NAME=''
for NAME in tuesday wednesday; do
  if [ -n "$(pane_pid_of "$NAME" | sed '/^$/d')" ]; then
    [ -z "$COORD_NAME" ] || { echo "REFUSING: panes named BOTH 'tuesday' and 'wednesday' are live — the coordinator's negative control is ambiguous (T8)" >&2; exit 38; }
    COORD_NAME="$NAME"
  fi
done
[ -n "$COORD_NAME" ] || { echo "REFUSING: no tmux pane named 'tuesday' or 'wednesday' — the coordinator's negative control is required (T8)" >&2; exit 38; }
[ "$COORD_NAME" = "tuesday" ] || echo "NOTE: the coordinator's pane is named '$COORD_NAME' on this machine (brief WRONG 19, T8) — used as the coordinator's negative control" >&2
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
for PEER in 'QA/NexusAI-batch18' 'QA/NexusAI-batch19' 'QA/NexusAI-batch20'; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
    echo "NOTE: $PEER has a live claude — a PEER gate: FIFO, never touched; added as a negative control" >&2
  fi
done

# 86 — no live gate-21 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 21 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
if grep -qE '^- \*\*\(T[0-9]+\)[^_]*: \*\*\s*______' "$BRIEF" || grep -qE '^- \*\*\(T[0-9]+\) [^*]*:\*\* ______' "$BRIEF"; then STAMP_OK=0; T_BLANK=1; else T_BLANK=0; fi
T_NOTE=''; [ "$T_BLANK" = "1" ] && T_NOTE=' / a blank T-ruling'
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 90 22 93 95 96 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 89 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-775 $A_HEAD (= $PR70_REF) · RD-131 $B_HEAD · RD-807 $C_HEAD · RD-821 r3 sha256 cand ${CAND_NOW:0:12}… / inst ${INST_NOW:0:12}… · SLOTS:$SLOT_DESC" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note${T_NOTE}) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 3 member branches + $PR70_REF at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192)"
  echo "  main ${M_ORIGIN:0:7} (b6c506a or a descendant; no member-only path moved; no member on it) (18b)"
  echo "  RD-821: installed fd223bd2… and candidate 3c33f5ae… pinned; 23-line diff; live default base named (90)"
  echo "  merge-bases + stacks (7); chains (8); deltas + no package change + product paths (22); premises (93 95 96); locks + proxy-addr (98)"
  echo "  overlaps (23); counts + census (35); npm cache + sqlite3 prebuild + Chrome + the carried rulings (70); $MT_PAIRS three-argument merge-trees counts-only or clean (80, 89); evidence (31); C-133 script (83)"
  echo "  yield RETIRED (41); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); SLOTS:$SLOT_DESC (89); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD (= $PR70_REF); refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/main = $M_ORIGIN (b6c506a or a descendant; no member-only path moved since b6c506a; no member on it). RD-821: installed $LOCKTOOL sha256 $INST_NOW and candidate $CANDIDATE sha256 $CAND_NOW, both equal to the pins. $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOTS:$SLOT_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
