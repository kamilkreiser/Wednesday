#!/bin/bash
# launch_qa_nexusai_gate_batch18.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 18"), THREE members (+ an ADDENDUM SLOT),
# one verdict per ticket, ONE report (drafted 2026-10-06 13:59:49–~14:30 AEDT by a read-only drafting agent for Tuesday).
# A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-761 (TIER 1, LA endpoint allow-list at the sink + writer admin gate; round 1 of 2) rd-761-law-endpoint-policy-s89r @ 141d7ea: EIGHT commits on 2f0ae4a.
#       NEW lawEndpointPolicy.js beaa819; azureLogAnalytics.js 595e71f -> bd0a382; server.js 0d7e387 -> cebee78; rd761 x2 + intercept preload; two fixture-only files. 4336/262.
#   B — RD-791 (TIER 1, privacy: the export never follows a store link) rd-791-export-store-links-s87n @ b79e02e: ONE commit on 2f0ae4a. dataExport.js b31a4e0 -> 55dabbd. 4269/261.
#   C — RD-756 (TIER 2, test-only: P9) rd-756-projection-role-shapes-s86m @ 5afdc01: TWO commits on RD-603's gated head 3529d53 (NOT on main; 4 commits on fae2aa1).
#       rd603 ead177e -> 2db462e. 4260/256. Lock f74a4e8 (an OLDER lock than M0's e9063d4 — brief WRONG 5).
#   THE CROSSES (C-68): server.js is changed by main's RD-618, A, and RD-603 (C's stack) — a COMBINED blob on every merged tree; RD-761's health fields meet RD-603's projection.
#   SLOT — RD-816 joins ONLY by the brief's line "ADDENDUM RD-816 JOINS @ <sha> ON <branch> TIER <1|2> | READY <path>" (guard 89). EMPTY.
#   Main at drafting 8e79499 (RD-618 (b1) after RD-648; counts 4279/262). Predicted MTF 4388/266. RD-671 merges next (main WILL move).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch18' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch18.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-18 drafter commission (daily note 2026-10-06 13:59) and her rulings on the members (RD-791 tier 1 at 08:38; RD-756 held for batch 18 at 08:17;
# RD-761's log-line ruling 22:27:12Z and affected-files ruling 00:45:19Z; RD-816 into batch 18 at 13:14). READY mails copied in briefs/. THE MODEL RULE: Kam, live board
# 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings: sqlite3 cached prebuild (2026-10-05_qa_b14_sqlite3_ANSWER.md); full verifies UNBELTED with 4 conditions (2026-10-05_qa_b14_belt_ANSWER.md);
# npm_config_update_notifier=false on EVERY npm call (2026-10-05_qa_gate16_notifier_ANSWER.md); the first-in-line re-file at a wait deadline
# (2026-10-06_qa_gate14_refile_ANSWER.md); the browser driver (2026-10-04_qa_batch13_browser_driver_answer.md); C-190 + its ADDENDUM: BOTH CodeQL thresholds.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves/updates a PR, never
# dismisses an alert; no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (node_modules offline only, H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch17.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules, the
# LIVE negative-control seat derivation 38R naming the coordinator pane 'tuesday', the ADDENDUM-SLOT JOINS parser 89, route-line and stamp guards
# last). CHANGES, each deliberate:
#   - THREE members; C is STACKED (its chain is checked down to fae2aa1 through RD-603 3529d53) (guards 6 7 8 22 23 35 80 31).
#   - 93: RD-761's premises; 94: RD-791's premises; 95 (NEW): RD-756's premises and RD-603's (not a member) shape.
#   - 18b: main moving and touching server.js is a NOTE (server.js is already a combined path); a member-ONLY path moving REFUSES.
#   - 22/98: TWO locks are in play (e9063d4 at M0/A/B; f74a4e8 at C and RD-603) — checked as briefed, never assumed one.
#   - 70: the browser-driver ruling (ruling o) must be on disk; Playwright in M0's lock; Chrome present (NOTE if not).
#   - 89: the SLOT is RD-816 (not on origin at drafting), so the JOINS line carries its branch and tier; its lock delta must be the proxy-addr entry only.
#   - 38R: peers are gates 14, 15 and 17 (all LIVE at drafting); gate 16 delivered.
#   - ONE browser leg (a9) and no image build.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python/shasum over `git show` output; grep, ls, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch18.sh [--check]
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
BRIEF="$BRIEFS/2026-10-06_nexusai-gate-batch18.md"
BRIEF14="$BRIEFS/2026-10-05_nexusai-gate-batch14.md"
BRIEF16="$BRIEFS/2026-10-05_nexusai-gate-batch16.md"
BRIEF17="$BRIEFS/2026-10-06_nexusai-gate-batch17.md"
READY_A="$BRIEFS/2026-10-06_nexusai-rd761-READY-mail.txt"
READY_B="$BRIEFS/2026-10-06_nexusai-rd791-READY-mail.txt"
READY_C="$BRIEFS/2026-10-06_nexusai-rd756-READY-mail.txt"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
REFILE_ANS="$STAGED/2026-10-06_qa_gate14_refile_ANSWER.md"
UNBELT15_ANS="$STAGED/2026-10-06_qa_gate15_unbelted_ANSWER.md"
BROWSER_ANS="$STAGED/2026-10-04_qa_batch13_browser_driver_answer.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
PBRIEF_A="$NX/qa-briefs/2026-10-06_nexusai-rd761-tier1-gate.md"
EV_R="$NX/session-tools/s89r"
EV_N="$NX/session-tools/s87n"
EV_M="$NX/session-tools/s86m"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B16_DIR="$RPTS/2026-10-05-gate-batch16"
B16_REPORT="$B16_DIR/report.md"
B16_INST="$B16_DIR/evidence/inst"
B12_REPORT="$RPTS/2026-09-30-gate-batch12/report.md"
B13_REPORT="$RPTS/2026-10-04-gate-batch13/report.md"
G4_REPORT="$RPTS/2026-09-22-gate4-rd575-rd524r2/report.md"
PREV_FLOORLIB="$B16_INST/qa-floorlib16.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-06-gate-batch18/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch18'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
CHROME_APP='/Applications/Google Chrome.app'

MAIN_SHA='8e794994833c041cd653e081a3d274bb8e802a73'      # origin main at drafting (13:59:49 AEDT; RD-618 (b1) after RD-648)
BASE_AB='2f0ae4a5a623eab73a1750d13535a18f8c0f5f5b'       # A's and B's parent / merge-base
BASE_C='fae2aa12cd6d27c6a46e690ce57c15052f164472'        # RD-603's base = C's merge-base with main, A and B
RD603='3529d5313a24807d555b1bcb33fb85f204880366'         # RD-603's gated head (gate 13), NOT a member, NOT on main; C's parent chain
RD603_BRANCH='rd-603-health-projection-s86m'
A_BRANCH='rd-761-law-endpoint-policy-s89r'
A_HEAD="${QA_A_HEAD_OVERRIDE:-141d7ea77242f7d56fa4b8596d4fc2ce1bb75bd3}"
B_BRANCH='rd-791-export-store-links-s87n'
B_HEAD="${QA_B_HEAD_OVERRIDE:-b79e02ec9706ff4c20d9b56d29f418d61f7181d1}"
C_BRANCH='rd-756-projection-role-shapes-s86m'
C_HEAD="${QA_C_HEAD_OVERRIDE:-5afdc017caa8def15c2d79939987659485bf276d}"
RD671='3ef057f343c2cc9f93ab416d2c420646d8c349d0'          # context: N's next merge (s87n-merge-rd671 queued first at drafting)
RD640='588ec6311320eab91deca9bf9dbd0f4afed3a287'          # context: gate 17's RD-640 (y5)
S_BRANCH_HINT='rd-816'                                     # the SLOT's ticket; no origin branch at drafting (local 931f621)

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
LP='backend/services/lawEndpointPolicy.js'
AL='backend/azureLogAnalytics.js'
SV='backend/server.js'
DX='backend/dataExport.js'
HP='backend/services/healthProjection.js'
T761P='__tests__/rd761-law-endpoint-policy.test.js'
T761W='__tests__/rd761-law-writers.test.js'
T761H='__tests__/helpers/rd761-law-intercept-preload.js'
TBOOT='__tests__/boot-probe-log-redaction.test.js'
TDISC='__tests__/discover-tables-tenant-mask.test.js'
T791='__tests__/rd791-export-store-links.test.js'
T603='__tests__/rd603-health-projection.test.js'
TS='__tests__/helpers/test-server.js'
TSH='__tests__/test-server-helper.test.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'
DKF='Dockerfile'
DIG='.dockerignore'

LP_A_BLOB='beaa81970286ff0128306ff03552904ad0e790ed'
AL_M_BLOB='595e71f7cfa7281869fe28f7331006860933ad13'      # 2f0ae4a, M0, B
AL_A_BLOB='bd0a38208280b9ccf85ff434d1c1ce87e9dd6c1b'
SV_Z_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'      # fae2aa1, 2f0ae4a, B
SV_M_BLOB='2684acda2190ac2578008f8055a131fe6cd9a7f1'      # M0 (RD-618)
SV_A_BLOB='cebee781ad8114ec6e28b5b7904dfefa738060f3'
SV_C_BLOB='2b907e82ce4186ab6b52c5ff22655521c71070db'      # RD-603 and C
T761P_BLOB='429e097012c303647131a84c8115ddc7ff28b857'
T761W_BLOB='1f08fead9a4f6b5f0d56f2b7ff6ff9235af124bb'
T761H_BLOB='09c7d7a8e95e3062d3b25df8e9929c7ff85f4b1c'
TBOOT_Z_BLOB='0c0a282abe68c8bcf48edc4c7c7fc52a62a4cdb3'
TBOOT_A_BLOB='1fb62bd6aa8191ae9b293c95ae506ca7b6fd5575'
TDISC_Z_BLOB='2dc442e9c09fa8ba9234ccfc6f98244e01323d37'
TDISC_A_BLOB='4acd09aaade7f35b01171c78373988f5f3671349'
DX_M_BLOB='b31a4e00dd18ed961db8d5d27af91b74a6bc1f87'      # 2f0ae4a, M0, A, C
DX_B_BLOB='55dabbd5eafb37ae5f30e5510b3405bcc98d4efc'
T791_BLOB='e7a2885c722e7bea3f92cfd5fd493b7ed2944dd9'
T603_P_BLOB='ead177eddbe8aa754ddb84ba32a6dd69e4177561'
T603_C_BLOB='2db462ef9d80bdf91a17150a213ce2cb1a48d05d'
HP_BLOB='e9e863c33de88bd6ee03a40371915b1fa2aadf5e'
LOCK_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'      # 2f0ae4a, M0, A, B
LOCK_C_BLOB='f74a4e8679491d6c1a496c96b405b15673dbc0fb'    # fae2aa1, RD-603, C
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'
TSH_BLOB='f612fb4815aaa358795acc977d59a0a9cba09670'
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
DX_M_SHA16='a4f2686dd990e33d'                              # sha256 prefix of b31a4e0's content (N's "main sha")
DX_B_SHA16='46af6f228bf6d13f'                              # sha256 prefix of 55dabbd's content (N's "fix")

A_EXPECTED_FILES="$LP
$AL
$SV
$T761P
$T761W
$T761H
$TBOOT
$TDISC
$COUNTS_FILE"
B_EXPECTED_FILES="$DX
$T791
$COUNTS_FILE"
C_EXPECTED_FILES="$T603
$COUNTS_FILE"
P_EXPECTED_FILES="$SV
$HP
$T603
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 18'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch18] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any member head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR (RD-761's alerts #23-#26 included), a real Microsoft or Azure Monitor endpoint (the allowed hosts reach only a local stand-in), a real Entra tenant or token, a real Key Vault, real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, headed Chrome and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only), a real customer volume (network mounts, other filesystems), Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
titles() { g show "${1}:${2}" 2>/dev/null | grep -E '^[[:space:]]*(test|it|describe)(\.each\(.*\))?\(' | sed -E 's/^[[:space:]]+//'; }
sha16() { g show "${1}:${2}" 2>/dev/null | shasum -a 256 | cut -c1-16; }
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

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 18", with THREE members and an ADDENDUM SLOT, one verdict per ticket and ONE report. It is a FRESH gate. The members: RD-761 (TIER 1, security control on a credential-bearing path, round 1 of 2, built by NexusAI-R S89R: the Log Analytics endpoint is an exact-host allow-list enforced at the SINK — api.loganalytics.azure.com, .io and .us mapped to CONSTANT base URLs, decided BEFORE any token is minted, so a refused endpoint mints no token and sends nothing; the FALLBACK source path keeps its own check; maxRedirects 0 on the three bearer-carrying calls; the tenant is GUID-checked at the writers and before the service-principal token; the four endpoint/tenant writers take the setup-mode-aware admin gate with the open window unchanged (C-178); a stored off-list endpoint is refused at use and never rewritten, and the health route says why with no host; two pre-existing log lines carry the HOST only; two older cells changed their FIXTURE only (C-97); C-203), RD-791 (TIER 1, privacy, built by NexusAI-N S87N: the customer data export never follows a store that is a symbolic link — it withholds and names it, never marks it redacted, writes the link text nowhere, and names a dangling or looping one; erasure unchanged; C-139 ADDENDUM 1; it answers gate 4's F-A7) and RD-756 (TIER 2, test-only, built by NexusAI-M S86M: cell P9 guards RD-603's health projection for six role shapes; it is STACKED on RD-603's gated head 3529d5313a24807d555b1bcb33fb85f204880366, which is NOT on main; it answers gate 13's L-B2). The server entry point is changed by main's RD-618, by RD-761 and by RD-603 (carried by RD-756), so a COMBINED blob is predicted on every merged tree, and RD-761's new health fields meet RD-603's projection: this gate carries THE CROSSES (C-68). The SLOT (RD-816, proxy-addr 2.0.7 -> 2.0.8, lockfile only) is a member ONLY if the brief's ADDENDUM SLOT carries a JOINS line — the launcher tells you below which it is. Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree: one verdict per ticket. RD-603 is NOT re-verdicted (gate 13's verdict stands; C-68 re-runs only). FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry, and no browser except the ONE local browser leg the brief names (a9).

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-06_nexusai-gate-batch18.md
It opens with the drafter's WRONG OR UNVERIFIED list, then TUESDAY'S RULINGS (T1-T9 as Tuesday stamped them, and the carried rulings (a) to (o)) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the three READY mails it names (read each WHOLE) and R's project-side brief for RD-761 (read WHOLE), C-203 with its ADDENDUM and C-139 with its ADDENDUM at source, the gate-4 report (RD-791's prior round: F-A7), the gate-13 report (RD-756's prior round: RD-603 at 3529d53, row b9, L-B2), gate 16's report (DELIVERED: its S-1 notifier lesson, its re-file log and its belt pair; its evidence/inst is the newest delivered instrument set) and gate 14's brief (the browser-leg shape). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones (attacker-shaped and off-list endpoints, userinfo/port/query URLs, non-GUID tenants, redirects, symlinked, dangling and looping store links, links to targets OUTSIDE DATA_DIR, product mutants that send the configured string or mint a token before the check) — every one is an authorised, findings-only measurement in your own trees, your own loopback servers and your own mktemp dirs, and no row contacts a real Microsoft host. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-761: rd-761-law-endpoint-policy-s89r at 141d7ea77242f7d56fa4b8596d4fc2ce1bb75bd3 (EIGHT commits on 2f0ae4a5a623eab73a1750d13535a18f8c0f5f5b — its READY said 10, R corrected it; counts 4336/262; NOT on M0; its builder full verify is at 3b547e3, so the gate's own full verify of 141d7ea is owed). RD-791: rd-791-export-store-links-s87n at b79e02ec9706ff4c20d9b56d29f418d61f7181d1 (ONE commit on 2f0ae4a; dataExport.js b31a4e0 -> 55dabbd; rd791 6 ids; counts 4269/261; NOT on M0). RD-756: rd-756-projection-role-shapes-s86m at 5afdc017caa8def15c2d79939987659485bf276d (TWO commits on RD-603 3529d53, which is four commits on fae2aa12cd6d27c6a46e690ce57c15052f164472 — a stale parent 49 commits behind 2f0ae4a, on the OLDER lock f74a4e8; counts 4260/256; no product file). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b) — and it WILL: N's RD-671 merge ticket is queued first on the lock at drafting, and RD-816 may follow at its GO. Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MT1 = M0 + RD-791 4285/263; MT2 = + RD-761 4358/265; MT-603 = + RD-603 4382/266 per T1; MTF = + RD-756 4388/266; predicted at M0 = 8e794994833c041cd653e081a3d274bb8e802a73, 4279/262), the tests census (312 at MTF), new ids 109, missing 0 for RD-761 and RD-791, and C-133's base-aware accounting for RD-756's stale-parent stack. If RD-671, RD-816 or gates 14/15/17's members are in your M0, re-derive every C-68 set on it (y7). Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. No PR exists for any member, nor for RD-603 or RD-816, at drafting: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY (the repo is datasecau/Reporting_Dashboard_Au). The npm-audit on main and on any PR is RED on proxy-addr 2.0.7 (GHSA-jqcg-44mw-7w3h) until RD-816 lands: that is RD-816's advisory, named, NEVER a member finding. C-185 on M0 (ruling h): the known-failing set is {rd549 O4 only when envReached alone differs}; ANY rd465 O-1 failure on M0, a member head built on 2f0ae4a, or a merged tree is a STOP, named and mailed; at RD-756's stale-parent head (pre-RD-733, pre-RD-723) apply Tuesday's T3; a local failure of O4 is named and classified, never waved; gate 16's OBS-1 (sustainability-logger-live, fetch failed), if it recurs, is named with undici's err.cause and never cleared by a re-run.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-761: a0 RED-AT-PARENT first (the head's two rd761 files and the two fixture-only files with only the Log Analytics client and the server entry point restored to 2f0ae4a's, the policy module kept; then the all-three arm); a2 THE POLICY MEASURED FIRST (every URL shape: case, trailing dot, port, userinfo, @ and backslash tricks, path, query, fragment, IDN, .cn, regional, non-string); a3 THE SINK ATTACK ROW — no token and no request for a refused endpoint at the primary, the FALLBACK, service-principal with a non-GUID tenant, five consecutive refusals through the breaker, and a 302 from the stand-in never followed, with the ALLOWED arm sent as the positive control; a4 the four writers on a configured deployment (viewer 403, admin 400 off-list and non-GUID, nothing persisted, the audit by host); a5 the open window unchanged (C-178) and the RD-437 residual named; a6 a stored off-list endpoint at boot (no request, no token, DEGRADED, the store never rewritten, the host absent from every anonymous and viewer health body); a7 the log lines host-only at every surface with the 0e3cd71 leak as the positive control; a8 the fixture-only files (C-97); a9 THE BROWSER LEG — a local run, open mode, fresh DATA_DIR, Playwright 1.62.1 from your own tree with channel chrome, headless, the wizard CLICKED THROUGH to its Data Source step for off-list, Azure China, userinfo, Global and Government, the result box read from the DOM; a10 the builder's mutants (M1, M2, M3, M4, M5, M8, M6+M7) re-derived INDEPENDENTLY on both rd761 files plus the union, plus your own M-hostlog, M-breakerFirst, M-gateOne, M-guidAnchor, M-allowCase, M-redirect3; a11 C-68; a12 CodeQL READ ONLY; a13 shipped blobs as a manifest evaluation, NO image built, and the admin-gate census; a14 prior work. RD-791: b0 RED-AT-PARENT first; b2 gate 4's F-A7 shapes re-run; b3 THE ARCHIVE-BYTES ROW — for every store name a link to an OUTSIDE target, the raw zip scanned for every needle, link text and outside path, with the base arm finding them as the control; b4 the shapes (loop, two-link loop, dangling, dangling through outside, EACCES, ELOOP-BY-LENGTH ending at real data, ENOTDIR, the warn line); b5 L-B1's remaining silent skip; b6 the builder's three mutants (M-follow, M-silent-dangling, M-exists) on the whole export union plus your own M-noWarn, M-redacted, M-linkText, M-statFollow; b7 C-68; b8 prior work. RD-756: c0 RED-UNDER-MUTANT first (C-98: P9 is green by design) — M1 and M2 re-derived INDEPENDENTLY on the whole rd603 file and its neighbours; c2 your own mutants for what P9 does not see; c3 green for the right reason by coverage; c4-c6. THE CROSSES: y1 the server entry point combined with main's RD-618; y2 THE HEALTH CROSS — RD-761's health fields through RD-603's projection on MT-603 and MTF, driven for anonymous, viewer and admin; y3 both A/B orders; y4-y8.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every verdict (brief section 7). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff RD-791 (MT1), RD-761 (MT2), RD-603 3529d53 as a NAMED non-member step (MT-603, per T1), RD-756 (MTF). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only, with the server entry point "changed in both" and combined cleanly. Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MTF on node_modules proven for M0's lock: predicted 4388/266, re-based on YOUR M0; the measurement decides. A second clone with RD-761 before RD-791, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0 for RD-761 and RD-791; for RD-756's stale-parent stack a missing id is ACCOUNTED only under C-133's two conditions, listed with its removing commit, else a STOP. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes package.json; RD-761 and RD-791 carry M0's lock e9063d4; RD-756's head (and RD-603's) carries the OLDER lock f74a4e8 (Tuesday's T2 rules its head verify). There is NO npm registry exception in this gate. ONCE PER LOCK: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline — and EVERY npm invocation, the first one included, carries npm_config_update_notifier=false (gate 16's S-1); prove the cache copy's _update-notifier-last-checked marker absent or unchanged. An ENOTCACHED is NOT RUN (name it, mail a QUESTION) — never go online, never npm install, never npm audit, never npx playwright install. sqlite3's binding: Tuesday ruled (04:55Z, to gate 14, carried here) that the offline unpack of sqlite3's CACHED prebuild from an APFS clone of ~/.npm/_prebuilds, inside the strict belt, IS PART OF H-31 — under three conditions: (1) the sha256 of the cached tarball and of the unpacked node_sqlite3.node in your tree; (2) say that CI builds the binding by its own install step (Linux, a different binary), so a local green on this binding is not evidence about CI's; (3) every row that boots the server or opens the DB names the binding source once ("sqlite3 binding: cached prebuild, offline"). Every other tree clones node_modules from your proven tree of the same lock; never from gate 14's, 15's or 17's (live) or gates 12/13/16's trees.

THE BROWSER LEG (ruling o, H-32): Playwright 1.62.1 from YOUR OWN tree's node_modules, channel chrome (the local Google Chrome 153), HEADLESS, NO browser download — prove ~/Library/Caches/ms-playwright unchanged before and after; only http://127.0.0.1:<port> of a server YOU booted from YOUR tree; every non-127.0.0.1 request aborted by the page route AND the belt; every caption "local run of <sha>, open mode — NOT the demo; Chrome 153 headless via Playwright 1.62.1". If Chrome or Playwright cannot launch, a9 is NOT RUN, named — never replaced by a jsdom render. The ONE preload you may load into a server you boot is R's test-only Log Analytics intercept preload, by -r in argv, for the ALLOWED-endpoint stand-in only (H-15, T4), its ledger read after every run.

FULL VERIFY of each head and of MTF through the lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n: every other jest run stays belted — cells, mutants, C-68 unions, drivers, servers, the browser), with its four conditions: the test-server-helper control pair (belted red, quote it; unbelted green; same tree, same window); any belted verify kept as evidence; each unbelted verify says "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; any other failure read on its merits, never blamed on the belt without a belted/unbelted pair. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only. Predicted 141d7ea 4336/262, b79e02e 4269/261, 5afdc01 4260/256 (on f74a4e8 per T2), MTF 4388/266. RD-791's and RD-756's builder verifies ran on a WORKING TREE before the commit with --update-counts, and RD-761 has none at its head; yours decides. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-2: seed BEFORE; every boot and every export is a NEW process — declare it per row. H-3: a LANDING CONTROL for every stored endpoint, link, loop, chain, chmod, outside target, stub, intercept and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd; link texts read back with readlink; URL plants byte-exact from a file. H-15: preloads with -r in argv; the ONE exception is R's intercept preload for the stand-in. H-16: every plant checked to be what the product will treat it as (gate 16's S-2). H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate, and every chmod you make, is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and lock waits have run 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly under the SAME tag if not granted. H-29: gates 14, 15 and 17 are live; their evidence is method only. H-31: offline node_modules per lock, the notifier off, and the cached sqlite3 prebuild. H-32: NO image built (the shipped-blob rows are a manifest evaluation); ONE local browser leg. H-33: links, loops, outside targets, stand-ins, chmod'd dirs and children counted and reaped or quarantined, never rm; a link you plant never points outside your own mktemp dirs; every planted hostname is *.invalid or an allowed host routed to YOUR stand-in. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch18.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gates 14's, 15's and 17's trees and report dirs are LIVE PEER gates' — never touch them; copy instruments BY COPY from gate 16's evidence/inst (its HOLD16.sh hard-codes its own evidence dir and its qa-floorlib16.sh carries stale ROOT and NEG defaults: re-point and correct your copies; its qa-file16b.sh carries the first-in-line re-file sequence and its qa-verify16.sh the notifier-off verify). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, probe, measure, screen or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no Microsoft host, no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gates 14, 15 and 17 (QA/NexusAI-batch14, -batch15, -batch17, tags qa-b14-, qa-b15-, qa-b17-) — PEER gates: FIFO, never touched — and the builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, plain-node, server and browser rows, census greps); then file your holds tagged qa-b18-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG). AT A WAIT DEADLINE WHILE FIRST IN LINE (Tuesday's ruling to gate 14, carried by ruling i): do NOT plain re-file — file the replacement under the SAME tag with --after YOUR OWN still-waiting ticket, confirm it is queued, and only then withdraw the old ticket by the C-141 clean path (SIGTERM your own waiter; the ticket goes to released/ as ticket-left-*; never delete a ticket file); never two live holds; a duplicate-tag refusal takes a -r<N> suffix, said in the report; you never move ahead of anything that was ahead of you; one report line per re-file with the queue place before and after FROM THE QUEUE LISTING. Once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result, including every server you boot outside a hold; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver, server, browser arm, export process and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the three member branches, rd-603-health-projection-s86m and main (and the SLOT's branch if it joins) — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main WILL move: call main at your start M0 and say so; it must be 8e79499 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch18. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch18] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-06-gate-batch18/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 18
Lead the body with one line per ticket, in the forms the brief's section 11 gives (RD-761 @ 141d7ea with the red at the base, the sink attack row — tokens and requests for a refused endpoint across primary, fallback, boot and breaker, the allowed arm sent to the constant, the redirect not followed — the policy shapes, the writers, the open window, the log and body markers, the stored-at-boot result, the fixture assertions, the browser leg, the builder mutants on the union; RD-791 @ b79e02e with the red at the base, the archive bytes, the F-A7 shapes, dangling and loop named, redacted never set on a link, ELOOP-by-length as measured, L-B1, the builder mutants on the union; RD-756 @ 5afdc01 with M1 and M2, your own mutants' survivors, reached for the right reason, the head verify as ruled; the SLOT's line only if it joined), then one line naming M0, your recommended merge order, the merged counts you measured in both orders, the C-57 and C-133 result, the combined server-entry-point blob id, THE HEALTH CROSS, which rows ran on Opus 4.8 (or none), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR); npm-audit red on proxy-addr = RD-816's". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A8, L-B1 to L-B4, L-C1 to L-C4 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-203 with its ADDENDUM, C-139 with its ADDENDUM, C-178, C-76, C-97, C-98, C-133, C-185 with its ADDENDA, C-190 with its ADDENDUM and C-192 are the clarifications this batch leans on; C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141 with ADDENDUM 5, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any member head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR (RD-761's alerts #23-#26 included), a real Microsoft or Azure Monitor endpoint (the allowed hosts reach only a local stand-in), a real Entra tenant or token, a real Key Vault, real Azure, a real Docker image build (the shipped-blob leg is a manifest evaluation), the demo (behind RD-76 SSO), any deployed environment, headed Chrome and the Claude-in-Chrome driver (the browser leg is Chrome headless via Playwright, local only), a real customer volume (network mounts, other filesystems), Linux's symlink-hop limit and errno behaviour (macOS only; CI is Linux), Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
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
for S in "$MAIN_SHA" "$BASE_AB" "$BASE_C" "$RD603" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: A and B on 2f0ae4a; C (via RD-603) on fae2aa1.
g merge-base --is-ancestor "$BASE_AB" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: 2f0ae4a is not an ancestor of 8e79499 — re-brief" >&2; exit 7; }
g merge-base --is-ancestor "$BASE_C" "$BASE_AB" 2>/dev/null || { echo "REFUSING: fae2aa1 is not an ancestor of 2f0ae4a — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$BASE_AB" ] || { echo "REFUSING: merge-base(RD-761, 8e79499) is not 2f0ae4a — re-brief" >&2; exit 7; }
[ "$(g merge-base "$B_HEAD" "$MAIN_SHA" 2>/dev/null)" = "$BASE_AB" ] || { echo "REFUSING: merge-base(RD-791, 8e79499) is not 2f0ae4a — re-brief" >&2; exit 7; }
[ "$(g merge-base "$A_HEAD" "$B_HEAD" 2>/dev/null)" = "$BASE_AB" ] || { echo "REFUSING: merge-base(RD-761, RD-791) is not 2f0ae4a — re-brief" >&2; exit 7; }
for X in "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(g merge-base "$C_HEAD" "$X" 2>/dev/null)" = "$BASE_C" ] || { echo "REFUSING: merge-base(RD-756, ${X:0:7}) is not fae2aa1 — re-brief" >&2; exit 7; }
done
g merge-base --is-ancestor "$RD603" "$C_HEAD" 2>/dev/null || { echo "REFUSING: RD-603 3529d53 is not an ancestor of RD-756 — the stack moved; re-brief" >&2; exit 7; }

# 8 — chains exact: A = 8 non-merge commits on 2f0ae4a; B = ONE; C = TWO on 3529d53; RD-603 = FOUR on fae2aa1.
chain_ok() { local base="$1" head="$2" n="$3" got m
  got="$(g rev-list --count "${base}..${head}" 2>/dev/null)"; m="$(g rev-list --merges --count "${base}..${head}" 2>/dev/null)"
  [ "$got" = "$n" ] && [ "$m" = "0" ] && g merge-base --is-ancestor "$base" "$head" 2>/dev/null; }
chain_ok "$BASE_AB" "$A_HEAD" 8 || { echo "REFUSING: RD-761 is not EIGHT non-merge commits on 2f0ae4a (brief WRONG 1)" >&2; exit 8; }
chain_ok "$BASE_AB" "$B_HEAD" 1 || { echo "REFUSING: RD-791 is not ONE non-merge commit on 2f0ae4a" >&2; exit 8; }
chain_ok "$RD603" "$C_HEAD" 2 || { echo "REFUSING: RD-756 is not TWO non-merge commits on RD-603 3529d53" >&2; exit 8; }
chain_ok "$BASE_C" "$RD603" 4 || { echo "REFUSING: RD-603 is not FOUR non-merge commits on fae2aa1" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the three member branches and RD-603 exactly the pins (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "refs/heads/$RD603_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$RD603_BRANCH $RD603"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY (and will) move (ruling b). It must be 8e79499 or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member-ONLY path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 8e79499 — main was rewritten; re-brief" >&2; exit 18; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$RD603"; do
  if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
done
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$LP" "$AL" "$DX" "$HP" "$T761P" "$T761W" "$T761H" "$TBOOT" "$TDISC" "$T791" "$T603" "$PKG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 8e79499..${M_ORIGIN:0:7} and touched a member-only path: $HIT — re-brief" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$SV" "$LOCK" "$TS" "$TSH" "$R465" "$R549" "$DKF" "$DIG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the combined server entry point / C-68 sets / node_modules proofs run on M0's blobs (brief ruling b, y7)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 8e79499; RD-671 / RD-816 / peer gates' members may have landed) — the gate re-pins M0 itself and re-bases every prediction" >&2
for X in "$RD671" "$RD640"; do
  if [ "$(g cat-file -t "$X" 2>&1)" = "commit" ] && g merge-base --is-ancestor "$X" "$M_ORIGIN" 2>/dev/null; then echo "NOTE: ${X:0:7} is now on origin main (y5/y7 apply)" >&2; fi
done
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed; no package.json change; product paths as commissioned; the lock as briefed.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$BASE_AB" "$A_HEAD" "$A_EXPECTED_FILES" "RD-761 (2f0ae4a..141d7ea)"
chk_delta "$BASE_AB" "$B_HEAD" "$B_EXPECTED_FILES" "RD-791 (2f0ae4a..b79e02e)"
chk_delta "$RD603" "$C_HEAD" "$C_EXPECTED_FILES" "RD-756 (3529d53..5afdc01)"
chk_delta "$BASE_C" "$RD603" "$P_EXPECTED_FILES" "RD-603 (fae2aa1..3529d53, not a member)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$BASE_AB" "$A_HEAD" "$LP")" = "138 0" ] && [ "$(ns "$BASE_AB" "$A_HEAD" "$AL")" = "54 7" ] && [ "$(ns "$BASE_AB" "$A_HEAD" "$SV")" = "65 14" ] \
  && [ "$(ns "$BASE_AB" "$A_HEAD" "$T761P")" = "328 0" ] && [ "$(ns "$BASE_AB" "$A_HEAD" "$T761W")" = "447 0" ] && [ "$(ns "$BASE_AB" "$A_HEAD" "$T761H")" = "51 0" ] \
  && [ "$(ns "$BASE_AB" "$A_HEAD" "$TBOOT")" = "10 3" ] && [ "$(ns "$BASE_AB" "$A_HEAD" "$TDISC")" = "9 2" ] \
  || { echo "REFUSING: RD-761's numstats are not as briefed (§1)" >&2; exit 22; }
[ "$(ns "$BASE_AB" "$B_HEAD" "$DX")" = "29 2" ] && [ "$(ns "$BASE_AB" "$B_HEAD" "$T791")" = "160 0" ] || { echo "REFUSING: RD-791's numstats are not dataExport +29/-2, rd791 +160" >&2; exit 22; }
[ "$(ns "$RD603" "$C_HEAD" "$T603")" = "24 0" ] || { echo "REFUSING: RD-756's numstat is not rd603 +24/-0" >&2; exit 22; }
for H in "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
  [ -z "$(g diff --name-only "$(g merge-base "$H" "$MAIN_SHA")" "$H" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${H:0:7} changes package-lock.json/package.json over its base — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
[ "$(g diff --name-only "$BASE_AB" "$A_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null | sort)" = "$(sorted "$LP
$AL
$SV")" ] || { echo "REFUSING: RD-761 touches a product path beyond the policy module, the LA client and the server entry point (static/ included)" >&2; exit 22; }
[ "$(g diff --name-only "$BASE_AB" "$B_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" = "$DX" ] || { echo "REFUSING: RD-791 touches a product path beyond $DX" >&2; exit 22; }
[ -z "$(g diff --name-only "$RD603" "$C_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" ] || { echo "REFUSING: RD-756 touches a product path — it is commissioned test-only (re-tier)" >&2; exit 22; }

# 93 — RD-761's premises at source.
[ "$(blob "$A_HEAD" "$LP")" = "$LP_A_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$LP")" ] \
  && [ "$(blob "$BASE_AB" "$AL")" = "$AL_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$AL")" = "$AL_M_BLOB" ] && [ "$(blob "$A_HEAD" "$AL")" = "$AL_A_BLOB" ] \
  && [ "$(blob "$BASE_AB" "$SV")" = "$SV_Z_BLOB" ] && [ "$(blob "$MAIN_SHA" "$SV")" = "$SV_M_BLOB" ] && [ "$(blob "$A_HEAD" "$SV")" = "$SV_A_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$T761P")" = "$T761P_BLOB" ] && [ "$(blob "$A_HEAD" "$T761W")" = "$T761W_BLOB" ] && [ "$(blob "$A_HEAD" "$T761H")" = "$T761H_BLOB" ] \
  && [ "$(blob "$BASE_AB" "$TBOOT")" = "$TBOOT_Z_BLOB" ] && [ "$(blob "$A_HEAD" "$TBOOT")" = "$TBOOT_A_BLOB" ] \
  && [ "$(blob "$BASE_AB" "$TDISC")" = "$TDISC_Z_BLOB" ] && [ "$(blob "$A_HEAD" "$TDISC")" = "$TDISC_A_BLOB" ] \
  || { echo "REFUSING: RD-761's blobs are not as briefed (beaa819 / 595e71f -> bd0a382 / 0d7e387 -> cebee78, M0 2684acd / rd761 x2 + preload / the fixture files)" >&2; exit 93; }
for T in 'function endpointHostForLog(raw) {' 'function lawEndpointRefusalMessage(host) {' "const LAW_ENDPOINT_NOT_ALLOWED = 'LAW_ENDPOINT_NOT_ALLOWED';" 'function resolveLawApiBase(raw) {'; do
  [ "$(cnt "$A_HEAD" "$LP" "$T")" = "1" ] || { echo "REFUSING: lawEndpointPolicy.js at 141d7ea lacks '$T' exactly once (a2's premise)" >&2; exit 93; }
done
[ "$(cnt "$A_HEAD" "$AL" 'apiEndpointHost: endpointHostForLog(this.apiEndpoint),')" = "1" ] && [ "$(cnt "$BASE_AB" "$AL" 'apiEndpointHost: endpointHostForLog(this.apiEndpoint),')" = "0" ] \
  && [ "$(cnt "$A_HEAD" "$AL" 'maxRedirects: 0')" = "3" ] && [ "$(cnt "$BASE_AB" "$AL" 'maxRedirects: 0')" = "0" ] \
  || { echo "REFUSING: the LA client's host-only log line or its three maxRedirects: 0 are not as briefed (a3/a7's premise)" >&2; exit 93; }
GATE_LINE='if (!(await requireAdminFor(req, res))) return;'
[ "$(cnt "$BASE_AB" "$SV" "$GATE_LINE")" = "4" ] && [ "$(cnt "$MAIN_SHA" "$SV" "$GATE_LINE")" = "4" ] && [ "$(cnt "$A_HEAD" "$SV" "$GATE_LINE")" = "8" ] \
  || { echo "REFUSING: the admin-gate line count is not 4 (2f0ae4a, M0) -> 8 (141d7ea) — the four writers (a4's premise, WRONG 11)" >&2; exit 93; }
for T in 'function lawWriteRefusal(body, req, route) {' "health.azureLogAnalytics.reason = 'endpoint-not-allowed';" "apiEndpointHost: req.body?.apiEndpoint ? endpointHostForLog(req.body.apiEndpoint) : 'default',"; do
  [ "$(cnt "$A_HEAD" "$SV" "$T")" = "1" ] && [ "$(cnt "$BASE_AB" "$SV" "$T")" = "0" ] || { echo "REFUSING: the server entry point at 141d7ea lacks '$T' exactly once (or 2f0ae4a has it)" >&2; exit 93; }
done
[ "$(cnt "$BASE_AB" "$SV" 'INVALID_ENDPOINT_URL')" = "1" ] && [ "$(cnt "$A_HEAD" "$SV" 'INVALID_ENDPOINT_URL')" = "0" ] || { echo "REFUSING: INVALID_ENDPOINT_URL is not 1 -> 0 (a14 (6)'s premise)" >&2; exit 93; }
for F in "$TBOOT" "$TDISC"; do
  [ "$(diff <(titles "$BASE_AB" "$F") <(titles "$A_HEAD" "$F") >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: the fixture-only file $F changed a title (a8's premise)" >&2; exit 93; }
  [ "$(diff <(g show "${BASE_AB}:${F}" | grep -F 'expect(') <(g show "${A_HEAD}:${F}" | grep -F 'expect(') >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: the fixture-only file $F changed an expect( line (a8's premise, C-97)" >&2; exit 93; }
done
[ -z "$(g diff --name-only "$BASE_AB" "$A_HEAD" -- static 2>/dev/null)" ] && [ "$(cnt "$A_HEAD" static/first-run-setup.html 'api.loganalytics.azure.cn')" -ge 1 ] \
  || { echo "REFUSING: static/ moved under RD-761, or the wizard no longer offers Azure China (a9 / L-A1's premise)" >&2; exit 93; }
[ "$(cnt "$A_HEAD" static/js/first-run-setup.js 'Configuration Saved Successfully')" -ge 1 ] && [ "$(cnt "$A_HEAD" static/js/first-run-setup.js "apiFetch('/api/setup/log-analytics'")" -ge 1 ] \
  || { echo "REFUSING: the wizard's Log Analytics save is not where a9 drives it" >&2; exit 93; }

# 94 — RD-791's premises at source.
[ "$(blob "$BASE_AB" "$DX")" = "$DX_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$DX")" = "$DX_M_BLOB" ] && [ "$(blob "$A_HEAD" "$DX")" = "$DX_M_BLOB" ] && [ "$(blob "$C_HEAD" "$DX")" = "$DX_M_BLOB" ] \
  && [ "$(blob "$B_HEAD" "$DX")" = "$DX_B_BLOB" ] && [ "$(blob "$B_HEAD" "$T791")" = "$T791_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T791")" ] \
  || { echo "REFUSING: RD-791's blobs are not dataExport b31a4e0 -> 55dabbd / rd791 e7a2885" >&2; exit 94; }
[ "$(sha16 "$BASE_AB" "$DX")" = "$DX_M_SHA16" ] && [ "$(sha16 "$B_HEAD" "$DX")" = "$DX_B_SHA16" ] || { echo "REFUSING: N's sha256 stamps (a4f2686d… / 46af6f22…) no longer match the blobs (WRONG 3's premise)" >&2; exit 94; }
for T in 'storeStat = fs.lstatSync(full);' "if (e.code === 'ENOENT' || e.code === 'ELOOP') resolves = false;" \
         "logger.warn('dataExport withheld a store that is a symbolic link — the export never follows a link', { file: fname, resolves });"; do
  [ "$(cnt "$B_HEAD" "$DX" "$T")" = "1" ] && [ "$(cnt "$BASE_AB" "$DX" "$T")" = "0" ] || { echo "REFUSING: dataExport.js at b79e02e lacks '$T' exactly once (b4's premise)" >&2; exit 94; }
done
[ "$(cnt "$BASE_AB" "$DX" 'if (!fs.existsSync(full)) continue;')" = "1" ] && [ "$(cnt "$B_HEAD" "$DX" 'if (!fs.existsSync(full)) continue;')" = "0" ] || { echo "REFUSING: M-exists' anchor is not 1 -> 0 (b6's premise)" >&2; exit 94; }
[ "$(g show "${B_HEAD}:${T791}" 2>/dev/null | grep -cE '^[[:space:]]+test\(')" = "6" ] || { echo "REFUSING: rd791 is not six test() cells" >&2; exit 94; }
for T in "test('L1 " "test('L2 " "test('L3 " "test('L4 " "test('L5 " "test('C1 "; do
  [ "$(cnt "$B_HEAD" "$T791" "$T")" = "1" ] || { echo "REFUSING: rd791 lacks the cell '$T' exactly once" >&2; exit 94; }
done

# 95 — RD-756's premises at source, and RD-603's (not a member) shape.
[ "$(blob "$RD603" "$T603")" = "$T603_P_BLOB" ] && [ "$(blob "$C_HEAD" "$T603")" = "$T603_C_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$T603")" ] \
  && [ "$(blob "$RD603" "$HP")" = "$HP_BLOB" ] && [ "$(blob "$C_HEAD" "$HP")" = "$HP_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$HP")" ] \
  && [ "$(blob "$RD603" "$SV")" = "$SV_C_BLOB" ] && [ "$(blob "$C_HEAD" "$SV")" = "$SV_C_BLOB" ] && [ "$(blob "$BASE_C" "$SV")" = "$SV_Z_BLOB" ] \
  || { echo "REFUSING: RD-603/RD-756 blobs are not rd603 ead177e -> 2db462e / healthProjection e9e863c / server entry point 0d7e387 -> 2b907e8" >&2; exit 95; }
TD="$(diff <(titles "$RD603" "$T603") <(titles "$C_HEAD" "$T603") 2>/dev/null | grep -E '^[<>]')"
[ "$(printf '%s\n' "$TD" | grep -c '^>')" = "1" ] && [ "$(printf '%s\n' "$TD" | grep -c '^<')" = "0" ] && printf '%s\n' "$TD" | grep -qF "test.each(NOT_ADMIN_USERS)('P9 " \
  || { echo "REFUSING: RD-756's title diff is not exactly +P9 (c4's premise)" >&2; exit 95; }
[ "$(cnt "$C_HEAD" "$HP" "const isAdmin = !!(req && req.user && req.user.role === 'admin');")" = "1" ] || { echo "REFUSING: M1/M2's anchor (isAdmin) is not present once in healthProjection.js (c0's premise)" >&2; exit 95; }
[ "$(cnt "$RD603" "$SV" "const { healthDetailsForCaller } = require('./services/healthProjection');")" = "1" ] && [ "$(cnt "$MAIN_SHA" "$SV" 'function healthDetailsForCaller(full, req) {')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$SV" 'function healthDetailsForCaller(full, req) {')" = "1" ] \
  || { echo "REFUSING: RD-603's move of healthDetailsForCaller (or its presence in M0 / RD-761's server entry point) is not as briefed (y2's premise)" >&2; exit 95; }

# 98 — shared blobs; the TWO locks as briefed; the image inputs.
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD"; do
  [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] && [ "$(blob "$S" "$TSH")" = "$TSH_BLOB" ] \
    && [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] \
    || { echo "REFUSING: lock / package.json / test-server / test-server-helper / Dockerfile / .dockerignore at ${S:0:7} are not e9063d4 / cdb1168 / cff1e54 / f612fb4 / 12aab55 / 3e45ec5" >&2; exit 98; }
done
[ "$(blob "$C_HEAD" "$LOCK")" = "$LOCK_C_BLOB" ] && [ "$(blob "$RD603" "$LOCK")" = "$LOCK_C_BLOB" ] && [ "$(blob "$BASE_C" "$LOCK")" = "$LOCK_C_BLOB" ] && [ "$(blob "$C_HEAD" "$PKG")" = "$PKG_BLOB" ] \
  || { echo "REFUSING: RD-756 / RD-603 / fae2aa1 do not carry lock f74a4e8 and package.json cdb1168 (WRONG 5's premise)" >&2; exit 98; }
for P in "$R465" "$R549"; do
  [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$A_HEAD" "$P")" ] && [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$B_HEAD" "$P")" ] || { echo "REFUSING: $P differs between M0 and RD-761/RD-791" >&2; exit 98; }
done
[ "$(blob "$C_HEAD" "$R465")" != "$(blob "$MAIN_SHA" "$R465")" ] || echo "NOTE: rd465 at RD-756 now equals M0's — WRONG 6 (pre-RD-733 at C's head) may be stale" >&2

# 23 — EXPECTED OVERLAPS: A and B share only the counts file; A and C's stack share exactly the server entry point; B and C nothing; main since 2f0ae4a meets A only at the server entry point.
dn() { g diff --name-only "$1" "$2" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
OV_AB="$(comm -12 <(dn "$BASE_AB" "$A_HEAD") <(dn "$BASE_AB" "$B_HEAD"))"
[ -z "$OV_AB" ] || { echo "REFUSING: RD-761 and RD-791 share a path beyond the counts file: $OV_AB" >&2; exit 23; }
OV_AC="$(comm -12 <(dn "$BASE_AB" "$A_HEAD") <(dn "$BASE_C" "$C_HEAD"))"
[ "$OV_AC" = "$SV" ] || { echo "REFUSING: RD-761 and RD-756's stack share '$OV_AC', not exactly the server entry point" >&2; exit 23; }
OV_BC="$(comm -12 <(dn "$BASE_AB" "$B_HEAD") <(dn "$BASE_C" "$C_HEAD"))"
[ -z "$OV_BC" ] || { echo "REFUSING: RD-791 and RD-756's stack share a path beyond the counts file: $OV_BC" >&2; exit 23; }
OV_MA="$(comm -12 <(dn "$BASE_AB" "$MAIN_SHA") <(dn "$BASE_AB" "$A_HEAD"))"
[ "$OV_MA" = "$SV" ] || { echo "REFUSING: main since 2f0ae4a and RD-761 share '$OV_MA', not exactly the server entry point" >&2; exit 23; }
OV_MB="$(comm -12 <(dn "$BASE_AB" "$MAIN_SHA") <(dn "$BASE_AB" "$B_HEAD"))"
[ -z "$OV_MB" ] || { echo "REFUSING: main since 2f0ae4a changed a path RD-791 changes: $OV_MB — a COMBINED blob the brief does not predict" >&2; exit 23; }

# 35 — counts at every pinned sha; __tests__ census.
for PAIR in "$BASE_C 4230 255" "$BASE_AB 4263 260" "$RD603 4254 256" "$MAIN_SHA 4279 262" "$A_HEAD 4336 262" "$B_HEAD 4269 261" "$C_HEAD 4260 256"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
CENSUS="$(for S in "$BASE_C" "$BASE_AB" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do printf '%s ' "$(ntests "$S")"; done)"
[ "$CENSUS" = "298 303 307 306 304 299 " ] || { echo "REFUSING: the __tests__ census (fae2aa1 2f0ae4a M0 A B C) is '$CENSUS', not '298 303 307 306 304 299'" >&2; exit 35; }

# 70 — the locks on origin main; the npm cache, the sqlite3 prebuild, Chrome, and the carried rulings (NOTEs where the gate decides, REFUSALs where a ruling is missing).
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not e9063d4 (RD-816 landed?) — another lock is in play; prove node_modules before any run (H-31)" >&2
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in axios/-/axios-1.20.0.tgz http-cache-semantics/-/http-cache-semantics-4.3.0.tgz sqlite3/-/sqlite3-5.1.7.tgz axios/-/axios-1.18.0.tgz http-cache-semantics/-/http-cache-semantics-4.2.0.tgz playwright/-/playwright-1.62.1.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(shasum -a 256 "$PREBUILD" 2>/dev/null | cut -d' ' -f1)"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -d "$CHROME_APP" ] || echo "NOTE: $CHROME_APP is absent — a9 (the browser leg) will be NOT RUN, named (ruling o)" >&2
[ "$(g show "${MAIN_SHA}:${LOCK}" 2>/dev/null | grep -A1 '"node_modules/playwright": {' | grep -cF '"version": "1.62.1"')" = "1" ] || echo "NOTE: M0's lock does not pin playwright 1.62.1 — ruling (o)'s driver version differs; the gate names what it finds" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$REFILE_ANS" ] && grep -qF 'file the replacement under the SAME tag with --after YOUR OWN still-waiting ticket, confirm it is queued, and only then withdraw the old ticket' "$REFILE_ANS" \
  || { echo "REFUSING: Tuesday's first-in-line re-file ruling (ruling i) is not at $REFILE_ANS as quoted" >&2; exit 70; }
[ -s "$BROWSER_ANS" ] && grep -qF 'Playwright 1.62.1 from YOUR tree' "$BROWSER_ANS" && grep -qF "headless (channel 'chrome'), no download" "$BROWSER_ANS" \
  || { echo "REFUSING: Tuesday's browser-driver ruling (ruling o) is not at $BROWSER_ANS as quoted" >&2; exit 70; }

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean.
MT_PAIRS=0
for PAIR in "$M_ORIGIN $A_HEAD" "$M_ORIGIN $B_HEAD" "$M_ORIGIN $C_HEAD" "$M_ORIGIN $RD603" "$A_HEAD $B_HEAD" "$A_HEAD $C_HEAD" "$B_HEAD $C_HEAD"; do
  X="${PAIR% *}"; Y="${PAIR#* }"
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done

# 31 — READYs, rulings, builder evidence, prior reports, gate 16's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$PBRIEF_A" "$CLAR" "$UNBELT15_ANS" "$BRIEF14" "$BRIEF16" "$BRIEF17" "$B16_REPORT" "$B12_REPORT" "$B13_REPORT" "$G4_REPORT" "$C133" \
         "$EV_R/hold-04.log" "$EV_R/hold-05-full.txt" "$EV_R/hold-05-jest.json" "$EV_R/screens/branch-141d7ea-custom-offlist.png" "$EV_R/screens/main-2f0ae4a-custom-offlist.png" \
         "$EV_N/rd791-hold.out" "$EV_N/rd791-hold.sh" "$EV_N/set-rd791.lst" "$EV_M/rd756-hold.log" "$EV_M/rd756-hold.sh" \
         "$NX/session-tools/nexusai-lock.sh" \
         "$B16_INST/HOLD16.sh" "$B16_INST/qa-holdlib16.sh" "$B16_INST/qa-floorlib16.sh" "$B16_INST/qa-floorcount.py" "$B16_INST/qa-to.sh" "$B16_INST/qa-jestwrap.sh" "$B16_INST/qa-jsum.js" \
         "$B16_INST/qa-runj16.sh" "$B16_INST/qa-mut16.py" "$B16_INST/qa-mutlib16.sh" "$B16_INST/qa-merge16.sh" "$B16_INST/qa-pin16.sh" "$B16_INST/qa-build16.sh" "$B16_INST/qa-file16b.sh" \
         "$B16_INST/qa-wait16.py" "$B16_INST/qa-verify16.sh" "$B16_INST/qa-h1-selftest16.sh" "$B16_INST/qa-h1-scan.py" "$B16_INST/qa-mail.py" "$B16_INST/qa-mailread.py" "$B16_INST/qa-lockcheck.py" \
         "$B16_INST/qa-ssprint.sh" "$B16_INST/qa-netbelt.sb" "$B16_INST/qa-netbelt-nodns.sb" "$B16_INST/qa-netbelt-ctl.js" "$B16_INST/qa-blobcensus16.py" "$B16_INST/qa-c57-id-superset.sh" \
         "$B16_INST/qa-c57ctl16.py" "$B16_INST/qa-c68census.py" "$B16_INST/qa-cov-setup.js" "$B16_INST/qa-plant16.js" "$B16_INST/qa-endacct16.sh" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "${C_HEAD:0:7}" "$READY_C" && grep -qF "${RD603:0:7}" "$READY_C" \
  && grep -qF 'PRIOR WORK' "$READY_B" && grep -qF 'PRIOR WORK' "$READY_C" && grep -qF 'PRIOR WORK (C-49)' "$PBRIEF_A" \
  || { echo "REFUSING: a READY does not name its head, or a PRIOR WORK section is missing (RD-761's is in its project brief)" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4269/4269 tests passed across 261 suites (jest exit 0)' "$EV_N/rd791-hold.out" && grep -qF 'expectation UPDATED — tests=4269 suites=261' "$EV_N/rd791-hold.out" \
  && grep -qF '=== done 2026-10-05T21:36:42Z' "$EV_N/rd791-hold.out" && grep -qF 'main sha a4f2686dd990e33d' "$EV_N/rd791-hold.out" && grep -qF 'restore X 46af6f228bf6d13f' "$EV_N/rd791-hold.out" \
  && grep -qF 'Tests:       89 passed, 89 total' "$EV_N/rd791-hold.out" && ! grep -qF '=== HEAD ' "$EV_N/rd791-hold.out" \
  && grep -qF 'VERDICT: PASS — 4260/4260 tests passed across 256 suites (jest exit 0)' "$EV_M/rd756-hold.log" && grep -qF 'expectation UPDATED — tests=4260 suites=256' "$EV_M/rd756-hold.log" \
  && grep -qF 'Tests:       3 failed, 24 skipped, 3 passed, 30 total' "$EV_M/rd756-hold.log" && grep -qF 'Tests:       6 failed, 24 skipped, 30 total' "$EV_M/rd756-hold.log" \
  && grep -qF 'restored e9e863c33de88bd6ee03a40371915b1fa2aadf5e' "$EV_M/rd756-hold.log" \
  && grep -qF 'start branch=3b547e3' "$EV_R/hold-04.log" && grep -qF 'rd761pass' "$EV_R/hold-05-full.txt" \
  || { echo "REFUSING: a builder log no longer carries the line the brief quotes (WRONG 2-3's premise)" >&2; exit 31; }
grep -qF 'F-A7' "$G4_REPORT" && grep -qF 'a store-as-link export hands out the link text and a bogus manifest size' "$G4_REPORT" \
  && grep -qF 'L-B2' "$B13_REPORT" && grep -qF '3529d5313a24807d555b1bcb33fb85f204880366' "$B13_REPORT" \
  || { echo "REFUSING: the gate-4 / gate-13 reports no longer carry F-A7 / RD-603's head and L-B2 as the brief quotes" >&2; exit 31; }
grep -qF 'GO WITH FINDINGS' "$B16_REPORT" && grep -qF 'update-notifier' "$B16_REPORT" || { echo "REFUSING: gate 16's report does not read as delivered with its S-1 notifier lesson" >&2; exit 31; }
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-53572\}' "$B16_INST/qa-floorlib16.sh" || echo "NOTE: gate 16's qa-floorlib16.sh ROOT default is no longer 53572 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF17" || grep -q '^Self-check note: Tuesday' "$BRIEF17" || echo "NOTE: gate 17's brief does not read as stamped by Tuesday — the brief calls it the stamped template" >&2

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
for P in "$G4_REPORT" "$B13_REPORT" "$B16_REPORT" "$B12_REPORT" "$BRIEF14" "$BRIEF16" "$BRIEF17" "$READY_A" "$READY_B" "$READY_C" "$PBRIEF_A" "$B16_INST/"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in '**RD-761 is TIER 1' '**RD-791 is TIER 1' '**RD-756 is TIER 2 (test-only).**' 'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION' \
         'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'THE BROWSER DRIVER' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'AT A WAIT DEADLINE WHILE FIRST IN LINE' 'THE CROSSES' 'RD-603 is NOT re-verdicted'; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-761 (TIER 1, security control' 'RD-791 (TIER 1, privacy' 'RD-756 (TIER 2, test-only' 'one verdict per ticket' 'THE CROSSES' 'manifest evaluation, NO image built' 'UNBELTED' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'AT A WAIT DEADLINE WHILE FIRST IN LINE' 'RD-603 is NOT re-verdicted' 'Playwright 1.62.1' 'channel chrome'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$MAIN_SHA" "$BASE_AB" "$BASE_C" "$RD603"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$LP_A_BLOB" "$AL_M_BLOB" "$AL_A_BLOB" "$SV_Z_BLOB" "$SV_M_BLOB" "$SV_A_BLOB" "$SV_C_BLOB" "$DX_M_BLOB" "$DX_B_BLOB" "$T603_P_BLOB" "$T603_C_BLOB" "$HP_BLOB" \
         "$LOCK_BLOB" "$LOCK_C_BLOB" "$PKG_BLOB" "$RD671" "$RD640"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
for S in "$DX_M_SHA16" "$DX_B_SHA16"; do grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name the stamp $S" >&2; exit 14; }; done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 18' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 18 has no priority member" >&2; exit 15; fi
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
WORDS="RD-761 RD-791 RD-756 RD-603 RD-816 RD-671 RD-618 C-49 C-57 C-68 C-76 C-89 C-97 C-98 C-102 C-104 C-112 C-115 C-125 C-133 C-139 C-141 ADDENDUM%5 C-174 C-178 C-185 C-186 C-190 C-192 C-203
RED-AT-PARENT RED-UNDER-MUTANT a0 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 b0 b2 b3 b4 b5 b6 b7 b8 c0 c2 c3 y1 y2 y3 y7 MT1 MT2 MT-603 MTF M0 F-A7 L-B2 P9 M1 M2
M-hostlog M-breakerFirst M-gateOne M-guidAnchor M-allowCase M-redirect3 M-follow M-silent-dangling M-exists M-noWarn M-redacted M-linkText M-statFollow
SINK FALLBACK maxRedirects GUID open%window OUTSIDE%DATA_DIR ELOOP-BY-LENGTH ENOTDIR EACCES redacted link%text dangling 4388/266 4358/265 4382/266 4285/263 4279/262 4336/262 4269/261 4260/256
e9063d4 f74a4e8 L-A1 L-A8 L-B1 L-B4 L-C1 L-C4 L-Y1 H-1 H-2 H-3 H-9 H-15 H-16 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 SCRATCH%object%dir git%clone%--shared REGENERATION intercept%preload ms-playwright
id-superset pull%request missing%0 new%ids%109 STOP JOINS ADDENDUM%SLOT POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b18- qa-b14- qa-b15- qa-b17- MERGES%GO%FIRST
QUEUE,%NEVER%TAKE%OVER --after UNCHANGED%tag DEADLINE HEARTBEAT PEER%gates 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center gate%4 gate%13 gate%16
npm%install --offline ENOTCACHED HOLD16.sh qa-floorlib16.sh qa-file16b.sh qa-verify16.sh Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> OBS-1 err.cause GHSA-jqcg-44mw-7w3h proxy-addr"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Targets' '^## 2. Why these tiers' '^## 2a. LEGITIMATE SHAPES' \
         '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 5b. TARGET C' '^## 6. THE CROSSES' '^## 7. THE MERGED TREE' '^## 8. CI' \
         '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## ADDENDUM SLOT' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^### TARGET C' \
         '^### File overlap' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
# the WRONG list sits ABOVE the rulings (the commission's order)
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-A7 L-A8 L-B1 L-B2 L-B3 L-B4 L-C1 L-C2 L-C3 L-C4 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a1 a2 a3 a4 a5 a6 a7 a8 a9 a10 a11 a12 a13 a14 b0 b1 b2 b3 b4 b5 b6 b7 b8 c0 c1 c2 c3 c4 c5 c6 y1 y2 y3 y4 y5 y6 y7 y8; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
for R in s0 s1 s2 s3 s4 s5 s6; do
  grep -qF "**$R " "$BRIEF" || { echo "REFUSING: brief lacks the SLOT row $R" >&2; exit 19; }
done
# every builder's stated scope / limits / interpretation lines carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|A LOCAL run of the branch, not the demo (RD-76).
A|The wizard was NOT clicked through step by step; please drive it.
A|The wizard still OFFERS "Azure China" and a regional Custom placeholder, both now refused. That is RD-792's call (Kam's); static/ was not touched.
A|The RD-437-state residual, as C-178 ruled.
A|RD-793 (other mutators) and RD-797 (the breaker hides other reasons).
A|full verify PASS 4336/262 at 3b547e3; at 141d7ea only the azureLogAnalytics.js requirers re-run (6 files by grep, 9 in the run set, 179/179), by Tuesday's ruling.
B|Drivable as plain jest on a temp DATA_DIR via streamExport; no server, no auth, no browser leg.
B|Not changed, said plainly: a NON-ENOENT lstat error on a store name is still a skip, as existsSync's false was before (not widened here); and links INSIDE feedback-attachments (_filesUnder, gate-4 F-A3 (v)) are unchanged: they are left out of the export, and that cell is NOT PROVEN (RD-640's READY).
B|erasure unchanged.
C|STACKED on RD-603's gated head 3529d53 (RD-603's head does not move; RD-756 merges after RD-603).
C|PRIOR WORK: nothing replaced or removed. The behaviour P9 asserts was already correct (gate 13 b9, plain node). This is coverage only.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
The sink sends the constant and resolves it BEFORE `getAccessToken()`, so a refused endpoint mints no token and sends nothing.
The open window is unchanged by construction (C-01, C-41, C-178)
refused at use with `LAW_ENDPOINT_NOT_ALLOWED`. The log carries the HOST only and says where to fix it. Nothing is ever migrated or rewritten.
GUID-checked on all four writers when present, and at the sink in `getTokenViaServicePrincipal`.
The shape `mustHaveSession && role !== 'admin'` was REJECTED
whether the constant base URL closes #23/#24/#26, and whether the GUID guard closes #25. The PR's CodeQL run measures both.
The export NEVER follows a store that is a SYMLINK, whether it points at a file or a directory (`feedback-attachments` included).
A DANGLING store link is NAMED (withheld: dangling link), never skipped silently.
Erasure is UNCHANGED (this entry's rule: removing too much is the safe direction).
close ONLY the Key Vault identity; every other open-window surface stays as it is
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
When a fix reddens an older test, the FIXTURE changes, never the policy
A cell asserts the PROPERTY THAT MUST HOLD AFTER THE FIX, never the defect that exists before it
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
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b18-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
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
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4388/266' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'e9063d4' 'f74a4e8' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' 'sqlite3 binding: cached prebuild, offline' 'manifest evaluation' 'NO image built' 'shippedFiles' \
         'lawEndpointPolicy' 'getAccessToken' 'FALLBACK' 'maxRedirects: 0' 'LAW_ENDPOINT_NOT_ALLOWED' 'LAW_TENANT_ID_INVALID' 'requireAdminFor' 'endpointHostForLog' 'intercept preload' \
         'streamExport' 'isSymbolicLink' 'withheld' 'redacted: true' 'link text' 'ELOOP' 'ENOTDIR' 'EACCES' 'OUTSIDE DATA_DIR' 'healthDetailsForCaller' 'P9' 'C-97' 'C-98' 'C-133' 'C-178' \
         'F-A7' 'L-B2' 'NOT PROVEN' 'Playwright 1.62.1' "channel: 'chrome'" 'ms-playwright' 'GHSA-jqcg-44mw-7w3h' 'proxy-addr' \
         '8e79499' 'ANY rd465 O-1 failure' 'ADDENDUM SLOT' 'RD-816 SLOT' 'WRONG 4' 'WRONG 5' 'WRONG 6' 'WRONG 9' 'WRONG 15' 'OBS-1' 'S-1' 'S-6' 'qa-floorlib16.sh' 'HOLD16.sh' 'qa-file16b.sh' \
         'ADDENDUM 5' 'datasecau/Reporting_Dashboard_Au' 'IS PART OF H-31' 'Tuesday rules'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the RD-816 ADDENDUM SLOT: EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head, every premise re-checked.
S_JOINS="$(grep -E '^ADDENDUM RD-816 JOINS @ [0-9a-f]{40} ON [A-Za-z0-9._/-]+ TIER [12] \| READY /' "$BRIEF" 2>/dev/null)"
S_EMPTY="$(grep -c '^RD-816 SLOT: EMPTY$' "$BRIEF" 2>/dev/null)"
S_STATE=''
SLOT_DESC=''
S_NOW=''
if [ -n "$S_JOINS" ]; then
  [ "$(printf '%s\n' "$S_JOINS" | grep -c .)" = "1" ] && [ "$S_EMPTY" = "0" ] || { echo "REFUSING: the RD-816 ADDENDUM SLOT has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  S_SHA="$(printf '%s\n' "$S_JOINS" | sed -E 's/^ADDENDUM RD-816 JOINS @ ([0-9a-f]{40}) .*/\1/')"
  S_BRANCH="$(printf '%s\n' "$S_JOINS" | sed -E 's/^.* ON ([A-Za-z0-9._/-]+) TIER .*/\1/')"
  S_TIER="$(printf '%s\n' "$S_JOINS" | sed -E 's/^.* TIER ([12]) .*/\1/')"
  S_READY="$(printf '%s\n' "$S_JOINS" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  case "$S_BRANCH" in *"$S_BRANCH_HINT"*) ;; *) echo "REFUSING: the SLOT's branch '$S_BRANCH' does not name $S_BRANCH_HINT (89)" >&2; exit 89 ;; esac
  lsr "refs/heads/$S_BRANCH" || { echo "REFUSING: ls-remote of the SLOT's branch failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN (C-192) (89)" >&2; exit 89; }
  S_NOW="$(printf '%s\n' "$LSR_OUT" | awk -v r="refs/heads/$S_BRANCH" '$2==r{print $1}')"
  [ "$S_NOW" = "$S_SHA" ] || { echo "REFUSING: the RD-816 ADDENDUM names $S_SHA but origin $S_BRANCH is '${S_NOW:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$S_SHA" 2>&1)" = "commit" ] || { echo "REFUSING: RD-816 $S_SHA is not in the object store (89)" >&2; exit 89; }
  [ -s "$S_READY" ] && grep -qF "${S_SHA:0:7}" "$S_READY" || { echo "REFUSING: RD-816's READY '$S_READY' is absent or does not name ${S_SHA:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$S_SHA" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: RD-816 ${S_SHA:0:7} is already on main (89)" >&2; exit 89; fi
  S_BASE="$(g merge-base "$S_SHA" "$M_ORIGIN")"
  [ -z "$(g diff --name-only "$S_BASE" "$S_SHA" -- "$PKG" 2>/dev/null)" ] || { echo "REFUSING: RD-816 changes package.json — Tuesday ruled lockfile-only (89)" >&2; exit 89; }
  S_RES="$(g diff "$S_BASE" "$S_SHA" -- "$LOCK" 2>/dev/null | grep -E '^[-+][[:space:]]+"resolved"' | sed -E 's/.*registry\.npmjs\.org\///; s/",?$//' | sort -u | tr '\n' ' ')"
  [ "$S_RES" = "proxy-addr/-/proxy-addr-2.0.7.tgz proxy-addr/-/proxy-addr-2.0.8.tgz " ] || { echo "REFUSING: RD-816's lock delta moves '$S_RES', not exactly proxy-addr 2.0.7 -> 2.0.8 (anything else moving = STOP, Tuesday 13:14) (89)" >&2; exit 89; }
  [ -z "$(g diff --name-only "$S_BASE" "$S_SHA" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" ] || { echo "REFUSING: RD-816 touches a product path — commissioned lockfile-only + cells (89)" >&2; exit 89; }
  for X in "$M_ORIGIN" "$A_HEAD" "$B_HEAD" "$C_HEAD"; do
    RC="$(conflicts "$X" "$S_SHA" | tr '\n' ' ' | sed 's/ $//')"
    [ -z "$RC" ] || [ "$RC" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x RD-816 conflicts beyond the counts file: '$RC' (89)" >&2; exit 89; }
    MT_PAIRS=$((MT_PAIRS + 1))
  done
  S_STATE="RD-816 JOINS this gate per the brief's ADDENDUM SLOT, at $S_SHA (origin $S_BRANCH, re-pinned by the launcher), TIER $S_TIER as Tuesday wrote it, READY $S_READY — gate it by the brief's ADDENDUM SLOT rows (s0-s6) and Tuesday's T6 on the audit; it brings a THIRD lock; merge it LAST (after MTF) unless Tuesday's JOINS stamp says otherwise."
  SLOT_DESC="JOINS @ ${S_SHA:0:7} ($S_BRANCH, tier $S_TIER)"
else
  [ "$S_EMPTY" = "1" ] || { echo "REFUSING: the RD-816 ADDENDUM SLOT is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
  S_STATE="RD-816 is NOT a member of this gate (the brief's ADDENDUM SLOT is EMPTY): do not gate it; say so in the report."
  SLOT_DESC="EMPTY"
fi

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §9 clause 1)" >&2
  for PT in qa-b14- qa-b15- qa-b17-; do
    BQ="$(grep -l "$PT" "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
    [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate ($PT) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
  done
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38R — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
# ps, not pgrep: macOS pgrep hides the caller's own ancestors, so Tuesday's own claude would vanish when --check runs from her shell.
# The builder panes are CANDIDATES (M/N/O/P/R): each LIVE one must carry exactly one claude; 'tuesday' is REQUIRED; at least three builder seats must be live.
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
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R tuesday; do   # the coordinator pane is named 'tuesday' on this seat
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
for PEER in 'QA/NexusAI-batch14' 'QA/NexusAI-batch15' 'QA/NexusAI-batch16' 'QA/NexusAI-batch17'; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
  else
    echo "NOTE: no live claude under a pane named $PEER — that peer gate finished or its pane is gone" >&2
  fi
done

# 86 — no live gate-18 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 18 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 98 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}" >&2
  echo "  member pins (origin, re-read now): RD-761 $A_HEAD · RD-791 $B_HEAD · RD-756 $C_HEAD (on RD-603 $RD603) · SLOT RD-816: $SLOT_DESC" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 3 member branches + RD-603 at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192)"
  echo "  main ${M_ORIGIN:0:7} (8e79499 or a descendant; no member-only path moved) (18b)"
  echo "  merge-bases (7); chains (8); deltas + no package change + product paths (22); premises (93 94 95 98)"
  echo "  overlaps (23); counts + census (35); locks + npm cache + sqlite3 prebuild + Chrome + the carried rulings (70); $MT_PAIRS three-argument merge-trees counts-only or clean (80, 89); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); RD-816 SLOT $SLOT_DESC (89); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$RD603_BRANCH = $RD603; refs/heads/main = $M_ORIGIN (8e79499 or a descendant; no member-only path moved since 8e79499). $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main, RD-603 and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
THE ADDENDUM SLOT: $S_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
