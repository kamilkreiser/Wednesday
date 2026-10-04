#!/bin/bash
# launch_qa_nexusai_gate_batch13.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 13"), FOUR members, one verdict per ticket,
# ONE report (2026-10-04). A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-741 (TIER 2, PRIORITY, lockfile only) rd-741-npm-audit-advisories-s86m @ 5db3f72, ONE commit on 630bb24 (= main at drafting). 4230/255. NexusAI-M.
#   B — RD-603 (+RD-601) (TIER 2) rd-603-health-projection-s86m @ 3529d53, four linear commits on fae2aa1 (NOT on main 630bb24). 4254/256. NexusAI-M.
#   C — RD-614 (TIER 2 + BROWSER LEG) rd-614-degraded-banner-title-s86n @ a71d078, two commits on ca7de45. 4232/256. NexusAI-N.
#   D — RD-629 (TIER 2, test harness only) rd-629-boot-loops-stop-child-s86n @ f7e2eff, two commits on ca7de45. 4234/256. NexusAI-N.
#   OPTIONAL — RD-430 (NexusAI-P) joins ONLY by the brief's ADDENDUM SLOT line "ADDENDUM RD-430 JOINS @ <sha> | READY <path>" (guard 89).
#   Main at drafting 630bb24 (RD-723; before it RD-732 fae2aa1). RD-707 (O) may land before launch: a NOTE, the gate re-bases on its own M0.
#   Predicted MT1 (M0 + A + B + C + D) 4260/258 at M0 = 630bb24.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch13' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch13.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's batch 13 commission (2026-10-04 ~22:1x AEDT); READY mails copied in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION. Starts on Opus 5.5.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker. The npm registry ONLY under the brief's exception (m)/H-31.
#
# PATTERN: launch_qa_nexusai_gate_batch12.sh (prompt EMBEDDED, --check mode, pin guards, THE MODEL RULE, floor §10, H-rules) + the LIVE negative-control
# seat derivation of resume_qa_nexusai_gate_batch12.sh (38R). CHANGES versus gate 12's fresh launcher, each deliberate:
#   - members/bases/chains/deltas/premises re-written for RD-741, RD-603, RD-614, RD-629 (guards 6 7 8 22 93 94 95 96 23 35 70 80 31).
#   - 18b: main must be 630bb24 or a descendant; main moving a member path REFUSES (incl. package-lock.json: RD-741 is lockfile-only);
#     the server entry point, rd518, rd441, rd638 or the rd525 helper moving is a NOTE; RD-707 / RD-733 landing a NOTE.
#   - 38R (from the resume launcher): NEG_SEATS DERIVED live from the cockpit panes Datasec/NexusAI-M/-N/-O/-P + 'wednesday' (claude descendant,
#     depth <= 5, by ps — not pgrep); REFUSES if any is missing/ambiguous. Gate 12's own claude (pane QA/NexusAI-batch12) is added as a 6th if live (NOTE if not).
#   - 86 (new): REFUSES if a pane named QA/NexusAI-batch13 already runs a claude (two sessions, one report).
#   - 89 (new): the RD-430 ADDENDUM SLOT — EMPTY (not a member) or one JOINS line, re-pinned by ls-remote.
#   - 32/40 reordered: both are checked LAST; every missing item is printed; the route line's absence exits 40 (named), else a stamp placeholder exits 32.
#   - exec: --model claude-opus-5-5 (gate 12's fresh launcher had no --model; its resume launcher did).
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §9); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python over `git show` output; grep, ls, shasum, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch13.sh [--check]
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
BRIEF="$BRIEFS/2026-10-04_nexusai-gate-batch13.md"
BRIEF12="$BRIEFS/2026-09-30_nexusai-gate-batch12.md"
READY_A="$BRIEFS/2026-10-04_nexusai-rd741-READY-mail.txt"
READY_B="$BRIEFS/2026-10-04_nexusai-rd603-READY-mail.txt"
READY_C="$BRIEFS/2026-09-30_nexusai-rd614-READY-mail.txt"
READY_D="$BRIEFS/2026-09-30_nexusai-rd629-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_M="$NX/session-tools/s86m"
EV_N="$NX/session-tools/s86n"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B12_DIR="$RPTS/2026-09-30-gate-batch12"
B12_EV="$B12_DIR/evidence"
B12_REPORT="$B12_DIR/report.md"
B10_EV="$RPTS/2026-09-29-gate-batch10/evidence"
PREV_B10="$RPTS/2026-09-29-gate-batch10/report.md"
PREV_FLOORLIB="$B12_EV/qa-floorlib12.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-04-gate-batch13/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch13'
ROUTE_NAME12='QA/NexusAI-batch12'

MAIN_SHA='630bb249c7740fee57a371378371afcfff33c454'      # origin main at drafting (22:19:40 AEDT; = rd-723 branch = refs/pull/40/head)
FAE='fae2aa12cd6d27c6a46e690ce57c15052f164472'           # RD-732's main — RD-603's base
CA7='ca7de453bea6e2c43657fc57104df8250959e72f'           # RD-197's main — RD-614 / RD-629's base
A_BRANCH='rd-741-npm-audit-advisories-s86m'
A_HEAD="${QA_A_HEAD_OVERRIDE:-5db3f7238f0eefaf10310a37d70ec5c41a6baaa5}"
B_BRANCH='rd-603-health-projection-s86m'
B_HEAD="${QA_B_HEAD_OVERRIDE:-3529d5313a24807d555b1bcb33fb85f204880366}"
B_MOVE='eb90f9243279f2c07a2de98eece5698ee6422555'         # the MOVE + P1-P7
B_DOC='ff5738f7a783303348c72202c260a0604369a015'          # RD-601 comment
B_FC='7983c9d28990cb9b9fa9eaa1f4626566e8c6e14c'           # FAIL CLOSED (P8/P8b)
C_BRANCH='rd-614-degraded-banner-title-s86n'
C_HEAD="${QA_C_HEAD_OVERRIDE:-a71d0786af2c68f0a44e226f7e3d99d4a428fa15}"
C_MID='f515f6ef137cb2956ae68fd008d07b651e420fe7'
D_BRANCH='rd-629-boot-loops-stop-child-s86n'
D_HEAD="${QA_D_HEAD_OVERRIDE:-f7e2eff3f1257b780f437e12133854027e6feb21}"
D_MID='275806ad4c5b011a404d0e91deeb41a6ee684623'
P430_BRANCH='rd-430-remove-response-form-s84p'
P430_SHA='379b8b57b823268e372000229a613739688e443c'       # NOT a member unless the ADDENDUM SLOT says JOINS (89)
O707_BRANCH='rd-707-key-backup-copies-s86o'
O707_SHA='e224ab936afdab64b877f0a1c6540bc5ce2b1591'       # may land before launch — a NOTE
M733_BRANCH='rd-733-user-access-stale-entra-check-s86m'
M733_SHA='ed4c1bfd5a195f163b8f76e84b467157f8b97813'       # not on main; C-185's O-1 leaves the set when it lands — a NOTE
NEAR_413='f70594a2418bb26a5ec2d98d68e8e4ed620cd575'; NEAR_413_BR='rd-413-truthful-mail-secret-storage-s84m'
NEAR_657='5584ea45617477338c2b5a01a0011cc92158a7f0'; NEAR_657_BR='rd-657-health-version-from-package-s86m'
NEAR_W3='fb6e67df24fd78b652b42b299a410905f881ce75';  NEAR_W3_BR='wip/s65-rd518-3'
NEAR_W4='80708a7434ef4eeea3801180600c28967597d054';  NEAR_W4_BR='wip/s65-rd518-4'
DEP39='f5004fac5300e4b4ff68c285440e9e8942e5e18d'          # Dependabot PR #39 head (row a9, READ ONLY)

COUNTS_FILE='scripts/verify-expected-counts.json'
SRV='backend/server.js'
HP='backend/services/healthProjection.js'
PKG='package.json'
LOCK='package-lock.json'
IDX='static/js/index.js'
R603='__tests__/rd603-health-projection.test.js'
R518A='__tests__/rd518-keyvault-identity-and-loud-fallback.test.js'
R518B='__tests__/rd518-r3-health-detail-decision.test.js'
R614='__tests__/rd614-degraded-banner-title.test.js'
R441='__tests__/rd441-persistence-alarm-reaches-dashboard.test.js'
R436='__tests__/rd436-group-gate-callback.test.js'
R452='__tests__/rd452-group-config-strict-callback.test.js'
R629='__tests__/rd629-rd525-bootOn-stops-child.test.js'
R638='__tests__/rd638-export-always-ends.test.js'
H525='__tests__/helpers/rd525-live-store.js'
STOPC='__tests__/helpers/stop-child.js'
P629F='__tests__/helpers/rd629-boot-failure.js'
P629C='__tests__/helpers/rd629-csrf-not-json-preload.js'
P629N='__tests__/helpers/rd629-never-listens-preload.js'
H395='__tests__/helpers/rd395-server-harness.js'
TS='__tests__/helpers/test-server.js'
ICE='__tests__/image-content-exposure.test.js'
AUDIT_YML='.github/workflows/npm-audit.yml'
C68_741="$EV_M/rd741-c68-set.txt"

LOCK_CA7_BLOB='906476350431e2ecb3c21070a25c64b1702c1aa8'   # ca7de45, C, D
LOCK_M_BLOB='f74a4e8679491d6c1a496c96b405b15673dbc0fb'     # fae2aa1, 630bb24, B
LOCK_A_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'     # RD-741
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'        # every sha here
SRV_M_BLOB='0d7e387558f06dba0e94a8bbf8f53382fd7ef5d2'      # ca7de45, fae2aa1, 630bb24, A, C, D
SRV_B_BLOB='2b907e82ce4186ab6b52c5ff22655521c71070db'      # eb90f92 .. 3529d53
HP_MOVE_BLOB='c32c3e8d0650f1f1ab2bed526aca459a86d207b0'
HP_B_BLOB='e9e863c33de88bd6ee03a40371915b1fa2aadf5e'
R603_MOVE_BLOB='73227f555f54e9ec32aceecc1cda503caa1eaa1e'
R603_B_BLOB='ead177eddbe8aa754ddb84ba32a6dd69e4177561'
R518A_BLOB='9fabe8ecbf5bf656a7c9c1aa5e2291473ab1ec2c'
R518B_BLOB='0bf596acb622e9a25bace1a56e40ea160f54a222'
IDX_M_BLOB='ae59c25d70df6c4d4053eef950cd3b495a1e6554'
IDX_C_BLOB='4acb49882cb655f3bf839a37f7eaef3e524a8410'
R614_BLOB='93d83623a4d89c67b96177c3d0ee17ac1af57a23'
R525_M_BLOB='d90a49879e5dcaa874d2e4996ed8993c2765435b'
R525_D_BLOB='33497a38b2b763aa563abaea4220d697d73f49c9'
R436_M_BLOB='546c0bb09bc55d50de26bf64fc990bac9dcc1984'
R436_D_BLOB='088e583c2459028a84b190b1186118c5de7a8a70'
R441_M_BLOB='9790565df51088d284385ec38cfbbbeae236603a'
R441_D_BLOB='87255d1faffb1f353cc4360a6d2fc4d778612fa2'
R452_M_BLOB='67c5d5067e817f4faa10eb202c7c5a3f040bc6eb'
R452_D_BLOB='ef2d81c76f46bdbe5dcd77012e92a0cf3b2ecfa5'
R629_BLOB='e5a911372dae5b12d0853574ee2b05191ed0e759'
STOPC_BLOB='e31096090b6b4bf6bafc4d718d522483297c2db2'
R638_M_BLOB='fc121f5d295997d5ec15e29a1c92063172197845'     # 630bb24, A (RD-723)
R638_O_BLOB='e7789e5731151ca84c1ac6d55cafc440cd3474ce'     # ca7de45, B, C, D (stale-parent)
H395_BLOB='2453a3fa7840de9d71267169b02ecea4a37015b6'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'         # RD-591 NOT on main (H-23 re-based)
ICE_BLOB='7e3262b001088991f7b3660c0a2949139f80510a'

A_EXPECTED_FILES="$LOCK"
B_EXPECTED_FILES="$R603
$SRV
$HP
$COUNTS_FILE"
C_EXPECTED_FILES="$R614
$COUNTS_FILE
$IDX"
D_EXPECTED_FILES="$H525
$P629F
$P629C
$P629N
$STOPC
$R436
$R441
$R452
$R629
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 13'
EARLY_SUBJ='[QA/Datasec-NexusAI -> Tuesday] EARLY VERDICT — batch 13 RD-741'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch13] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, the demo (behind RD-76 SSO), any deployed environment, a Docker image build, any browser but the gate's own driver against a local run, multi-replica deployments, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry beyond \`npm ci\` and \`npm audit\` in two of the gate's own trees, and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
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

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 13", with FOUR members, one verdict per ticket and ONE report. It is a FRESH gate. The members: RD-741 (TIER 2, the PRIORITY member, gated FIRST: a lockfile-only security fix moving axios 1.18.0 -> 1.20.0, http-cache-semantics 4.2.0 -> 4.3.0 and three brace-expansion entries to patched versions, package.json byte-identical); RD-603 with RD-601 (TIER 2, through-code: the admin-health projection healthDetailsForCaller moved byte-for-byte out of the server entry point into backend/services/healthProjection.js, its docstring corrected by RD-601, and a non-admin now served keyVaultEncryption null when the stored value is not a plain object — fail closed); RD-614 (TIER 2 plus a BROWSER LEG: the dashboard's DEGRADED banner title becomes "Service degraded — some features may not work.", C-193); RD-629 (TIER 2, test harness only: four test boot helpers stop their server child before they throw). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-04_nexusai-gate-batch13.md
It opens with TUESDAY'S RULINGS (a) to (n) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the four READY mails it names (read each WHOLE), then gate 12's brief (the base of your instrument rules H-1 to H-30) and gate 12's report's WRAP / COLD-RESUME HANDOVER and RESUME METHOD NOTE (gate 12 is STILL RUNNING: read only, never its trees, never its report dir), then the batch 10 report it names (its self-corrections are folded into H-22 to H-26 — a nested sandbox-exec exits 71; /bin/ps is setuid and EPERMs inside the sandbox, so use pgrep; --setupFilesAfterEnv is an array option, so test paths go first; quote every path with a space; zsh eats a bare ===== line; a bare END is not END ok). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the attack-style ones (b2's role-bypass mutants, b4's anonymous admin-health reads) — every one is an authorised, findings-only measurement against your own loopback servers from your own trees. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-741: rd-741-npm-audit-advisories-s86m at 5db3f7238f0eefaf10310a37d70ec5c41a6baaa5, one commit whose parent is main at drafting 630bb249c7740fee57a371378371afcfff33c454. RD-603: rd-603-health-projection-s86m at 3529d5313a24807d555b1bcb33fb85f204880366, four linear commits (the move eb90f9243279f2c07a2de98eece5698ee6422555, RD-601's comment ff5738f7a783303348c72202c260a0604369a015, fail closed 7983c9d28990cb9b9fa9eaa1f4626566e8c6e14c, counts) on fae2aa12cd6d27c6a46e690ce57c15052f164472 — NOT on main. RD-614: rd-614-degraded-banner-title-s86n at a71d0786af2c68f0a44e226f7e3d99d4a428fa15; RD-629: rd-629-boot-loops-stop-child-s86n at f7e2eff3f1257b780f437e12133854027e6feb21 — each two commits on ca7de453bea6e2c43657fc57104df8250959e72f. The deltas share NO path but the counts file. They share SEMANTIC surfaces: RD-741's node_modules sits under every merged-tree run; rd441 is RD-614's C-68 cell AND is modified by RD-629; RD-629's rd525 live-store helper sits under main's RD-723 rd638 (C-68). RD-430 (NexusAI-P) is NOT a member unless the brief's ADDENDUM SLOT says it JOINS (the launcher tells you below). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MTa = M0 + RD-741 4230/255; MTb = + RD-603 4254/256; MTc = + RD-614 4256/257; MT1 = + RD-629 4260/258, predicted at M0 = 630bb24; +1 test if RD-707 landed), the tests census (305 at MT1), new ids 30, missing 0. Members cut from ca7de45 and fae2aa1 are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included). No PR exists for any member branch at drafting: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY. npm-audit DOES run on every branch push: READ its runs (RD-741's head success, main's failure) as CLAIMS beside your own measurement. C-185 with its ADDENDA on M0: the known-failing set is {rd465 O-1 only with the checkEntraStatus TypeError, rd549 O4 only when envReached alone differs}; rd638 E2 LEFT the set when RD-723 merged — a red E2 is reported, never waved.

RD-741 FIRST (ruling a). Rows a0-a10: a0 POSITIVE CONTROL FIRST — in YOUR OWN M0 control tree, npm ci --no-audit --no-fund then CI's command npm audit --omit=dev --audit-level=moderate --json AND the bare npm audit --omit=dev, both NON-ZERO; a1 the same in YOUR head tree, both exit 0, then the full audit (the dev-only residue GHSA-vfj7-8cjw-p6xm is RD-742's); a2 npm ci from the head lock and each of the 5 changed lock entries read back from node_modules and the lock; a3 the lock diff is exactly five entries (a planted sixth caught); a4 npm ls; a5 the advisory ranges; a6 the 36-file C-68 set BY NAME (8 of them mock axios); a7 real axios 1.20.0 on the wire once; a8 the app boots; a9 Dependabot PR #39 read only; a10 the CI runs read only. THE NPM REGISTRY EXCEPTION (ruling m, H-31): registry.npmjs.org ONLY for npm ci and npm audit in those two trees of yours, each with its own npm cache under your mktemp dir — never npm install, npm update, npm audit fix or a downloading npx. RD-741's first hold is its own (its 36-file set and its full verify). Unless Tuesday struck ruling (n) at stamp, mail RD-741's verdict line alone as soon as its rows are complete, subject exactly "[QA/Datasec-NexusAI -> Tuesday] EARLY VERDICT — batch 13 RD-741", then carry on.

RD-603 (TIER 2): b0 THE BYTE-IDENTICAL MOVE measured with your own extractor and a positive control (the 48-line docstring and function, old in the server entry point at fae2aa1 vs new in healthProjection.js at the move commit: the drafter read exactly one changed line, the require path); b1 RED-AT-PARENT — the head's cells against the move commit's module: P8 red for string, array, number, boolean and Map, P8-null green, and P8b (the ADMIN control) GREEN — the commission's "P8/P8b red at the move" is corrected in the brief's WRONG 3; b2 the builder's mutants M1-M4 re-derived plus your own; b3 rd518 R9/R9b/R10 unchanged and green; b4 the route through a real local boot; b5 the merge-tree census claim re-derived on HUNKS for the four near-region branches the READY lists; b6-b9 prior work, RD-601 comment-only, reachability, the role-less user. RD-614 (TIER 2 + BROWSER LEG): c0 RED-AT-PARENT, c1, c2 mutants, c3 THE BROWSER LEG — a LOCAL RUN of a71d078 in open mode, DEGRADED reached for real through an unwritable storage volume under your own mktemp dir, read in the QA project's browser driver on 127.0.0.1 only, title and message from the DOM, screenshot, console, network, the overlay named; every caption and the verdict clause say "local run of <sha>, open mode — NOT the demo"; never a claim that the demo was tested; if the browser driver is unavailable the leg is NOT RUN, never a jsdom render called a browser (H-32); c4 stubbed only if c3 cannot reach DEGRADED; c5 the browser leg on MT1; c6-c8. RD-629 (TIER 2): d0 RED-AT-PARENT = M-nostop with NO title filter — L1-L4 red, each live child SEEN alive then reaped BY ITS PROVEN PID (H-33); d1-d8 including the SIGKILL path, grandchildren, the named limit and the re-count. Cross cells y1-y4 on MT1.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class.

THE MERGED TREE — part of every verdict (brief section 8). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff RD-741 (MTa), RD-603 (MTb), RD-614 (MTc), RD-629 (MT1). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only; no COMBINED blob is predicted (name any). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1 on RD-741's npm-ci'd modules: predicted 4260/258, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0; any missing id is a STOP. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only, each on node_modules PROVEN for its own lock (three locks are in play: RD-741's for the head and every merged tree, main's for RD-603, ca7de45's for RD-614 and RD-629). Predicted 5db3f72 4230/255, 3529d53 4254/256, a71d078 4232/256, f7e2eff 4234/256, MT1 4260/258. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker. H-3: a LANDING CONTROL for every preload, plant, pid file, unwritable volume or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-15: preloads with -r in argv; no exception this batch. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (amended from gate 12's wrap): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and today's lock waits ran 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly if not granted. H-29: gate 12 is live; its evidence is method only. H-31: the registry exception. H-32: the browser leg. H-33: deliberate leaks reaped by proven pid. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch13.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gate 12's and gate 11's trees and report dirs are not yours — read their evidence only, copy instruments BY COPY (gate 12's HOLD12.sh hard-codes its own evidence dir: re-point your copy). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, serve or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry outside H-31. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 10 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gate 12 (QA/NexusAI-batch12, tags qa-b12-, a PEER gate: FIFO, never touched) and the four builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the npm ci and audit rows, plain-node rows, the browser leg); then file your holds tagged qa-b13-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4); once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run (correct the stale ROOT and NEG defaults of gate 12's copied qa-floorlib12.sh first); record the foreign count beside every result; count every child you start (RD-629's deliberate leaks, the browser leg's server, stand-ins) and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe, boot, request, npm call, browser step and jest run has a per-step DEADLINE and a client timeout, every server and child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the four member branches, RD-430's, RD-707's, RD-733's, the four near-region branches and main — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be 630bb24 or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch13. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch13] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-04-gate-batch13/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 13
Lead the body with one line per ticket, in the forms the brief's section 12 gives (RD-741 @ 5db3f72 with the audit rc at head and M0, lock entries moved, the read-back, the 36-file set and the boot; RD-603 @ 3529d53 with the move, P8 at the move, P8b, rd518 and new conflict regions; RD-614 @ a71d078 with the browser leg as a local run, NOT the demo; RD-629 @ f7e2eff with M-nostop reds and children left), then one line naming M0, your recommended merge order, the merged counts you measured, the C-57 result, which rows ran on Opus 4.8 (or none), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR)". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's NOT TESTED list and named limits as the brief quotes them, every declared limit L-A1 to L-A6, L-B1 to L-B5, L-C1 to L-C4 and L-D1 to L-D3 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-185 with its ADDENDA, C-190, C-192 and C-193 are the clarifications this batch leans on; C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, the demo (behind RD-76 SSO), any deployed environment, a Docker image build, any browser but the gate's own driver against a local run, multi-replica deployments, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry beyond `npm ci` and `npm audit` in two of the gate's own trees, and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do
  [[ "$S" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$S' is not a full 40-hex sha" >&2; exit 9; }
done

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$FAE" "$CA7" "$A_HEAD" "$B_HEAD" "$B_MOVE" "$B_DOC" "$B_FC" "$C_HEAD" "$C_MID" "$D_HEAD" "$D_MID" "$P430_SHA" "$O707_SHA" "$M733_SHA" \
         "$NEAR_413" "$NEAR_657" "$NEAR_W3" "$NEAR_W4" "$DEP39"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: each member's own base with main; the bases are on main.
for S in "$FAE" "$CA7"; do
  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not an ancestor of 630bb24 — re-brief" >&2; exit 7; }
done
for PAIR in "$A_HEAD $MAIN_SHA" "$B_HEAD $FAE" "$C_HEAD $CA7" "$D_HEAD $CA7"; do
  H="${PAIR% *}"; W="${PAIR#* }"
  [ "$(g merge-base "$H" "$MAIN_SHA" 2>/dev/null)" = "$W" ] || { echo "REFUSING: merge-base(${H:0:7}, 630bb24) is not ${W:0:7} — re-brief" >&2; exit 7; }
done

# 8 — chains exact (linear, one parent each).
[ "$(g log --format='%H %P' "${MAIN_SHA}..${A_HEAD}" 2>/dev/null)" = "$A_HEAD $MAIN_SHA" ] || { echo "REFUSING: 630bb24..RD-741 is not exactly one commit 5db3f72 on 630bb24" >&2; exit 8; }
[ "$(g log --format='%H %P' "${FAE}..${B_HEAD}" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$B_HEAD $B_FC $B_FC $B_DOC $B_DOC $B_MOVE $B_MOVE $FAE" ] \
  || { echo "REFUSING: fae2aa1..RD-603 is not exactly eb90f92 -> ff5738f -> 7983c9d -> 3529d53" >&2; exit 8; }
for TRIPLE in "$C_HEAD $C_MID $CA7" "$D_HEAD $D_MID $CA7"; do
  set -f; set -- $TRIPLE; set +f
  [ "$(g log --format='%H %P' "${3}..${1}" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$1 $2 $2 $3" ] || { echo "REFUSING: ${3:0:7}..${1:0:7} is not exactly two linear commits ${2:0:7} -> ${1:0:7}" >&2; exit 8; }
done

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the four ticket branches exactly the pins (REFUSE); RD-430 / RD-707 / RD-733 / near-region a NOTE.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "refs/heads/$D_BRANCH" "refs/heads/$P430_BRANCH" "refs/heads/$O707_BRANCH" \
    "refs/heads/$M733_BRANCH" "refs/heads/$NEAR_413_BR" "refs/heads/$NEAR_657_BR" "refs/heads/$NEAR_W3_BR" "refs/heads/$NEAR_W4_BR" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
P430_NOW="$(ref_now "$P430_BRANCH")"; O707_NOW="$(ref_now "$O707_BRANCH")"; M733_NOW="$(ref_now "$M733_BRANCH")"
[ "$P430_NOW" = "$P430_SHA" ] || echo "NOTE: origin $P430_BRANCH is '${P430_NOW:-absent}', not 379b8b5 — the RD-430 ADDENDUM (if any) must name the current head (89)" >&2
[ "$O707_NOW" = "$O707_SHA" ] || echo "NOTE: origin $O707_BRANCH is '${O707_NOW:-absent}', not e224ab9 — RD-707 moved or landed; the gate re-bases on its M0" >&2
[ "$M733_NOW" = "$M733_SHA" ] || echo "NOTE: origin $M733_BRANCH is '${M733_NOW:-absent}', not ed4c1bf — re-read C-185's O-1 condition on M0" >&2
for PAIR in "$NEAR_413_BR $NEAR_413" "$NEAR_657_BR $NEAR_657" "$NEAR_W3_BR $NEAR_W3" "$NEAR_W4_BR $NEAR_W4"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"; NOW="$(ref_now "$BR")"
  [ "$NOW" = "$H" ] || echo "NOTE: near-region branch $BR is '${NOW:-absent}', not ${H:0:7} — row b5 measures what it finds and names the move" >&2
done
# 18b — main MAY move (ruling b). It must be 630bb24 or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 630bb24 — main was rewritten; re-brief" >&2; exit 18; }
if [ "$M_ORIGIN" != "$MAIN_SHA" ]; then
  for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do
    if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
  done
fi
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$LOCK" "$PKG" "$HP" "$IDX" "$R603" "$R614" "$R629" "$R436" "$R441" "$R452" "$H525" "$STOPC" "$P629F" "$P629C" "$P629N" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 630bb24..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief (RD-741 is lockfile-only: a moved lock re-bases its whole audit)" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$SRV" "$R518A" "$R518B" "$R638" "$H395" "$TS" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the C-68 sets run on M0's blobs (brief ruling b)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 630bb24) — the gate re-pins M0 itself and re-bases every prediction" >&2
ON_MAIN=''
g merge-base --is-ancestor "$O707_SHA" "$M_ORIGIN" 2>/dev/null && ON_MAIN="$ON_MAIN RD-707(e224ab9)"
g merge-base --is-ancestor "$M733_SHA" "$M_ORIGIN" 2>/dev/null && ON_MAIN="$ON_MAIN RD-733(ed4c1bf)"
g merge-base --is-ancestor "$P430_SHA" "$M_ORIGIN" 2>/dev/null && ON_MAIN="$ON_MAIN RD-430(379b8b5)"
[ -z "$ON_MAIN" ] || echo "NOTE: origin main carries:$ON_MAIN — the gate re-bases counts, census and C-68 populations on M0" >&2
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? gate 12's H-23 applies (brief H-23 re-based)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$MAIN_SHA" "$A_HEAD" "$A_EXPECTED_FILES" "RD-741 (630bb24..5db3f72)"
chk_delta "$FAE" "$B_HEAD" "$B_EXPECTED_FILES" "RD-603 (fae2aa1..3529d53)"
chk_delta "$CA7" "$C_HEAD" "$C_EXPECTED_FILES" "RD-614 (ca7de45..a71d078)"
chk_delta "$CA7" "$D_HEAD" "$D_EXPECTED_FILES" "RD-629 (ca7de45..f7e2eff)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$MAIN_SHA" "$A_HEAD" "$LOCK")" = "16 16" ] || { echo "REFUSING: RD-741's lock numstat is not +16/-16" >&2; exit 22; }
[ "$(ns "$FAE" "$B_HEAD" "$SRV")" = "1 48" ] && [ "$(ns "$FAE" "$B_HEAD" "$HP")" = "73 0" ] && [ "$(ns "$FAE" "$B_HEAD" "$R603")" = "149 0" ] \
  || { echo "REFUSING: RD-603's numstats are not server +1/-48, healthProjection +73, rd603 +149" >&2; exit 22; }
[ "$(ns "$CA7" "$C_HEAD" "$IDX")" = "5 1" ] && [ "$(ns "$CA7" "$C_HEAD" "$R614")" = "77 0" ] || { echo "REFUSING: RD-614's numstats are not index.js +5/-1, rd614 +77" >&2; exit 22; }
[ "$(ns "$CA7" "$D_HEAD" "$H525")" = "6 4" ] && [ "$(ns "$CA7" "$D_HEAD" "$STOPC")" = "58 0" ] && [ "$(ns "$CA7" "$D_HEAD" "$R436")" = "64 39" ] && [ "$(ns "$CA7" "$D_HEAD" "$R441")" = "25 5" ] \
  && [ "$(ns "$CA7" "$D_HEAD" "$R452")" = "74 49" ] && [ "$(ns "$CA7" "$D_HEAD" "$R629")" = "37 0" ] || { echo "REFUSING: RD-629's numstats are not as briefed" >&2; exit 22; }
[ -z "$(g diff --name-only "$CA7" "$D_HEAD" -- backend static docs Dockerfile .dockerignore package.json package-lock.json .github 2>/dev/null)" ] || { echo "REFUSING: RD-629 touches a product/package path — commissioned as test harness only" >&2; exit 22; }
[ -z "$(g diff --name-only "$CA7" "$C_HEAD" -- backend docs Dockerfile .dockerignore package.json package-lock.json .github 2>/dev/null)" ] || { echo "REFUSING: RD-614 touches a path beyond static/ and its cell" >&2; exit 22; }

# 93 — RD-741's premises at source: package.json byte-identical; the lock moves EXACTLY five packages entries with the briefed versions; CI's audit command.
[ "$(blob "$MAIN_SHA" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$A_HEAD" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: package.json is not cdb1168 at 630bb24 and 5db3f72" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$LOCK")" = "$LOCK_M_BLOB" ] && [ "$(blob "$A_HEAD" "$LOCK")" = "$LOCK_A_BLOB" ] || { echo "REFUSING: package-lock is not f74a4e8 -> e9063d4" >&2; exit 93; }
LOCKCMP="$(python3 - "$REPO" "$MAIN_SHA" "$A_HEAD" <<'PYEOF'
import json, subprocess, sys
repo, a, b = sys.argv[1:4]
def load(s):
    return json.loads(subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:package-lock.json'],capture_output=True,check=True).stdout)["packages"]
pa, pb = load(a), load(b)
keys = sorted(set(pa) | set(pb))
changed = [k for k in keys if pa.get(k) != pb.get(k)]
out = []
for k in changed:
    out.append(f"{k}={pa.get(k,{}).get('version')}->{pb.get(k,{}).get('version')}")
print(";".join(out))
PYEOF
)"
WANT_LOCK='node_modules/archiver-utils/node_modules/brace-expansion=2.1.4->2.1.7;node_modules/axios=1.18.0->1.20.0;node_modules/brace-expansion=1.1.18->1.1.21;node_modules/http-cache-semantics=4.2.0->4.3.0;node_modules/readdir-glob/node_modules/brace-expansion=2.1.4->2.1.7'
[ "$LOCKCMP" = "$WANT_LOCK" ] || { echo "REFUSING: RD-741's lock does not move exactly the five briefed entries. Got: '$LOCKCMP'" >&2; exit 93; }
[ "$(cnt "$MAIN_SHA" "$AUDIT_YML" 'npm audit --omit=dev --audit-level=moderate --json > audit.json')" = "1" ] && [ "$(cnt "$MAIN_SHA" "$AUDIT_YML" "branches: ['**']")" -ge 1 ] \
  || { echo "REFUSING: CI's npm-audit command / every-branch trigger is not as briefed (WRONG 2's premise)" >&2; exit 93; }
[ "$(grep -c . "$C68_741" 2>/dev/null)" = "36" ] || { echo "REFUSING: $C68_741 is not the 36-file C-68 set" >&2; exit 93; }
while IFS= read -r F; do
  [ -n "$F" ] || continue
  g cat-file -e "${A_HEAD}:${F}" 2>/dev/null || { echo "REFUSING: C-68 set path $F is not in 5db3f72" >&2; exit 93; }
done < "$C68_741"

# 94 — RD-603's premises at source: the byte-identical move (one changed line, the require path); the wiring; fail-closed; rd518 unchanged.
MOVECMP="$(python3 - "$REPO" "$FAE" "$B_MOVE" <<'PYEOF'
import subprocess, sys, difflib
repo, old, new = sys.argv[1:4]
def show(s, p):
    return subprocess.run(['git','--no-optional-locks','-C',repo,'show',f'{s}:{p}'],capture_output=True,check=True).stdout.decode().split('\n')
def block(lines):
    i = next(n for n, l in enumerate(lines) if l.startswith('function healthDetailsForCaller('))
    s = i
    while not lines[s].startswith('/**'): s -= 1
    e = i
    while lines[e] != '}': e += 1
    return lines[s:e+1]
a = block(show(old, 'backend/server.js')); b = block(show(new, 'backend/services/healthProjection.js'))
d = [l for l in difflib.unified_diff(a, b, lineterm='', n=0) if l[:1] in '+-' and not l.startswith(('+++','---'))]
print(len(a), len(b), len(d), '|'.join(x[0] + x[1:].strip() for x in d))
PYEOF
)"
[ "$MOVECMP" = "48 48 2 -keyVaultEncryption: require('./encryptionService').publicKeyVaultState(full.keyVaultEncryption),|+keyVaultEncryption: require('../encryptionService').publicKeyVaultState(full.keyVaultEncryption)," ] \
  || { echo "REFUSING: the RD-603 move is not 48 lines with exactly the require path changed (b0's premise). Got: '$MOVECMP'" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$SRV" "const { healthDetailsForCaller } = require('./services/healthProjection');")" = "1" ] && [ "$(g show "${B_HEAD}:${SRV}" 2>/dev/null | grep -cE 'function[[:space:]]+healthDetailsForCaller[[:space:]]*\(')" = "0" ] \
  && [ "$(cnt "$B_HEAD" "$SRV" 'healthDetailsForCaller(full, req)')" -ge 1 ] && [ "$(cnt "$FAE" "$SRV" 'function healthDetailsForCaller(full, req) {')" = "1" ] \
  || { echo "REFUSING: the server entry point's wiring is not as briefed (one require, no local copy, the route call kept)" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$HP" 'function isPlainObject(v) {')" = "1" ] && [ "$(cnt "$B_HEAD" "$HP" 'return proto === Object.prototype || proto === null;')" = "1" ] && [ "$(cnt "$B_MOVE" "$HP" 'isPlainObject')" = "0" ] \
  || { echo "REFUSING: fail-closed isPlainObject is not new at 7983c9d as briefed" >&2; exit 94; }
[ "$(blob "$B_MOVE" "$HP")" = "$HP_MOVE_BLOB" ] && [ "$(blob "$B_FC" "$HP")" = "$HP_B_BLOB" ] && [ "$(blob "$B_HEAD" "$HP")" = "$HP_B_BLOB" ] \
  && [ "$(blob "$B_MOVE" "$R603")" = "$R603_MOVE_BLOB" ] && [ "$(blob "$B_HEAD" "$R603")" = "$R603_B_BLOB" ] && [ "$(blob "$B_HEAD" "$SRV")" = "$SRV_B_BLOB" ] && [ "$(blob "$B_MOVE" "$SRV")" = "$SRV_B_BLOB" ] \
  || { echo "REFUSING: RD-603's blobs are not c32c3e8->e9e863c / 73227f5->ead177e / server 2b907e8" >&2; exit 94; }
[ "$(cnt "$B_HEAD" "$R603" "test.each(NOT_PLAIN)('P8 — ")" = "1" ] && [ "$(cnt "$B_HEAD" "$R603" "test.each(NOT_PLAIN)('P8b — CONTROL: ")" = "1" ] && [ "$(cnt "$B_MOVE" "$R603" "P8")" = "0" ] \
  || { echo "REFUSING: rd603's P8 / P8b are not new at 7983c9d (WRONG 3's premise)" >&2; exit 94; }
[ "$(g diff -U0 "$B_MOVE" "$B_DOC" 2>/dev/null | grep -E '^[-+][^-+]' | grep -cvE '^[-+][[:space:]]*\*')" = "0" ] || { echo "REFUSING: RD-601 (ff5738f) changes a non-comment line" >&2; exit 94; }
for S in "$FAE" "$MAIN_SHA" "$B_HEAD"; do
  [ "$(blob "$S" "$R518A")" = "$R518A_BLOB" ] && [ "$(blob "$S" "$R518B")" = "$R518B_BLOB" ] || { echo "REFUSING: rd518 files are not 9fabe8e / 0bf596a at ${S:0:7} (b3's premise)" >&2; exit 94; }
done
[ "$(cnt "$B_HEAD" "$R518A" "test('R9 — THE F-02 CELL")" = "1" ] && [ "$(cnt "$B_HEAD" "$R518A" "test('R9b — CONTROL")" = "1" ] || { echo "REFUSING: rd518 R9 / R9b titles are not present" >&2; exit 94; }
[ "$(cnt "$B_HEAD" 'backend/encryptionService.js' 'function publicKeyVaultState(state) {')" = "1" ] && [ "$(cnt "$B_HEAD" 'backend/encryptionService.js' "if (!state || typeof state !== 'object') return state;")" = "1" ] \
  || { echo "REFUSING: publicKeyVaultState is not as the brief reads it (READ (ii))" >&2; exit 94; }

# 95 — RD-614's premises at source.
[ "$(cnt "$CA7" "$IDX" "'Service degraded — data source unreachable.'")" = "1" ] && [ "$(cnt "$MAIN_SHA" "$IDX" "'Service degraded — data source unreachable.'")" = "1" ] \
  && [ "$(cnt "$C_HEAD" "$IDX" "'Service degraded — some features may not work.'")" = "1" ] && [ "$(cnt "$C_HEAD" "$IDX" "'Service degraded — data source unreachable.'")" = "0" ] \
  || { echo "REFUSING: the DEGRADED title is not old (ca7de45, 630bb24) -> new (a71d078) as briefed" >&2; exit 95; }
[ "$(blob "$CA7" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$IDX")" = "$IDX_M_BLOB" ] && [ "$(blob "$C_HEAD" "$IDX")" = "$IDX_C_BLOB" ] && [ "$(blob "$C_HEAD" "$R614")" = "$R614_BLOB" ] \
  || { echo "REFUSING: RD-614's blobs are not index ae59c25 -> 4acb498 / rd614 93d8362" >&2; exit 95; }
[ "$(cnt "$C_HEAD" "$R614" "test('T1 — a STORAGE fault")" = "1" ] && [ "$(cnt "$C_HEAD" "$R614" "test('T2 — every reason shape")" = "1" ] \
  && [ "$(cnt "$MAIN_SHA" "$R441" "test('B2 - DEGRADED shows the public degradedReason'")" = "1" ] || { echo "REFUSING: rd614 T1/T2 or rd441 B2 are not as briefed" >&2; exit 95; }
[ "$(g show "${MAIN_SHA}:${R441}" 2>/dev/null | grep -cE '^[[:space:]]*test\(')" = "19" ] || { echo "REFUSING: rd441 does not carry 19 cells at 630bb24 (c1's premise)" >&2; exit 95; }

# 96 — RD-629's premises at source.
[ "$(cnt "$D_HEAD" "$STOPC" 'module.exports = { stopChild, stopChildThenThrow, stopChildOnThrow, exited };')" = "1" ] && [ "$(blob "$D_HEAD" "$STOPC")" = "$STOPC_BLOB" ] \
  || { echo "REFUSING: stop-child.js does not export the briefed four (or its blob is not e310960)" >&2; exit 96; }
[ "$(cnt "$D_HEAD" "$R441" "test('L1 — ")" = "1" ] && [ "$(cnt "$D_HEAD" "$R629" "test('L2 — ")" = "1" ] && [ "$(cnt "$D_HEAD" "$R452" "test('L3 — ")" = "1" ] && [ "$(cnt "$D_HEAD" "$R436" "test('L4 — ")" = "1" ] \
  || { echo "REFUSING: L1-L4 are not present once each in the briefed files" >&2; exit 96; }
for F in "$R441" "$H525" "$R452" "$R436"; do
  [ "$(cnt "$D_HEAD" "$F" 'spawn(process.execPath, [')" -ge 1 ] || [ "$(cnt "$D_HEAD" "$F" 'spawn(process.execPath, preload ?')" -ge 1 ] || { echo "REFUSING: $F does not spawn process.execPath directly (d4's premise)" >&2; exit 96; }
done
[ "$(blob "$CA7" "$H525")" = "$R525_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$H525")" = "$R525_M_BLOB" ] && [ "$(blob "$D_HEAD" "$H525")" = "$R525_D_BLOB" ] \
  && [ "$(blob "$CA7" "$R436")" = "$R436_M_BLOB" ] && [ "$(blob "$D_HEAD" "$R436")" = "$R436_D_BLOB" ] && [ "$(blob "$CA7" "$R441")" = "$R441_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R441")" = "$R441_M_BLOB" ] && [ "$(blob "$D_HEAD" "$R441")" = "$R441_D_BLOB" ] \
  && [ "$(blob "$CA7" "$R452")" = "$R452_M_BLOB" ] && [ "$(blob "$D_HEAD" "$R452")" = "$R452_D_BLOB" ] && [ "$(blob "$D_HEAD" "$R629")" = "$R629_BLOB" ] \
  || { echo "REFUSING: RD-629's blobs are not as briefed" >&2; exit 96; }
[ "$(blob "$MAIN_SHA" "$R638")" = "$R638_M_BLOB" ] && [ "$(blob "$CA7" "$R638")" = "$R638_O_BLOB" ] && [ "$(blob "$D_HEAD" "$R638")" = "$R638_O_BLOB" ] && [ "$(blob "$B_HEAD" "$R638")" = "$R638_O_BLOB" ] \
  && g grep -q -E "require\([^)]*rd525-live-store['\"]" "$MAIN_SHA" -- "$R638" 2>/dev/null || { echo "REFUSING: rd638 is not fc121f5 on main (e7789e5 at the cut-from-old members) requiring the rd525 helper (y2's premise)" >&2; exit 96; }
for S in "$CA7" "$MAIN_SHA" "$D_HEAD"; do
  [ "$(blob "$S" "$H395")" = "$H395_BLOB" ] || { echo "REFUSING: rd395-server-harness at ${S:0:7} is not 2453a3f (d7's premise: RD-619's failBoot kept)" >&2; exit 96; }
done
for S in "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do
  [ "$(blob "$S" "$ICE")" = "$ICE_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] || { echo "REFUSING: image-content-exposure / test-server at ${S:0:7} are not 7e3262b / cff1e54 (rulings e and H-23)" >&2; exit 96; }
done

# 23 — EXPECTED OVERLAPS by each member's own delta: the counts file only.
declare_delta() { g diff --name-only "$1" "$2" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
OV_BAD=''
LIST="A:$MAIN_SHA:$A_HEAD B:$FAE:$B_HEAD C:$CA7:$C_HEAD D:$CA7:$D_HEAD"
for I in $LIST; do for J in $LIST; do
  [ "${I%%:*}" \< "${J%%:*}" ] || continue
  IB="${I#*:}"; JB="${J#*:}"
  SH="$(comm -12 <(declare_delta "${IB%%:*}" "${IB#*:}") <(declare_delta "${JB%%:*}" "${JB#*:}") | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$SH" ] || OV_BAD="$OV_BAD ${I%%:*}${J%%:*}='$SH'"
done; done
[ -z "$OV_BAD" ] || { echo "REFUSING: path overlaps are not as briefed (none but the counts file):$OV_BAD" >&2; exit 23; }

# 35 — counts at every pinned sha; __tests__ census at the heads.
for PAIR in "$CA7 4230 255" "$FAE 4230 255" "$MAIN_SHA 4230 255" "$A_HEAD 4230 255" "$B_MOVE 4230 255" "$B_FC 4230 255" "$B_HEAD 4254 256" \
            "$C_MID 4230 255" "$C_HEAD 4232 256" "$D_MID 4230 255" "$D_HEAD 4234 256"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
[ "$(ntests "$MAIN_SHA")" = "298" ] && [ "$(ntests "$A_HEAD")" = "298" ] && [ "$(ntests "$B_HEAD")" = "299" ] && [ "$(ntests "$C_HEAD")" = "299" ] && [ "$(ntests "$D_HEAD")" = "303" ] \
  || { echo "REFUSING: the __tests__ census is not 298 / 298 / 299 / 299 / 303 (M0, A, B, C, D)" >&2; exit 35; }

# 70 — package-lock: three blobs in play, exactly where the brief says.
for S in "$CA7" "$C_HEAD" "$D_HEAD"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_CA7_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not 9064763" >&2; exit 70; }; done
for S in "$FAE" "$MAIN_SHA" "$B_HEAD"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_M_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not f74a4e8" >&2; exit 70; }; done
for S in "$CA7" "$FAE" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: package.json at ${S:0:7} is not cdb1168" >&2; exit 70; }; done
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_M_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not f74a4e8 — 18b would have refused unless only its blob id read differently; prove node_modules before any run" >&2
[ "$(blob "$MAIN_SHA" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$FAE" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$A_HEAD" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$C_HEAD" "$SRV")" = "$SRV_M_BLOB" ] && [ "$(blob "$D_HEAD" "$SRV")" = "$SRV_M_BLOB" ] \
  || { echo "REFUSING: the server entry point is not 0d7e387 at ca7de45/fae2aa1/630bb24/A/C/D" >&2; exit 70; }

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair's conflict markers in the counts file ONLY.
HEADS="$A_HEAD $B_HEAD $C_HEAD $D_HEAD"
MT_PAIRS=0
for X in $M_ORIGIN $HEADS; do for Y in $HEADS; do
  [ "$X" \< "$Y" ] || [ "$X" = "$M_ORIGIN" ] || continue
  [ "$X" = "$Y" ] && continue
  if g merge-base --is-ancestor "$Y" "$X" 2>/dev/null || g merge-base --is-ancestor "$X" "$Y" 2>/dev/null; then continue; fi   # contained (RD-741 on M0)
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done; done

# 31 — builder evidence, prior reports, gate 12's evidence, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$CLAR" "$PREV_B10" "$BRIEF12" "$B12_REPORT" "$C133" "$C68_741" \
         "$EV_M/rd741-hold.log" "$EV_M/rd741-hold.sh" "$EV_M/rd741-serve.sh" "$EV_M/rd603-hold.log" "$EV_M/rd603-hold.sh" "$EV_M/rd603-census.txt" "$EV_M/rd603-new-conflicts.txt" \
         "$EV_N/rd614/r1-hold.out" "$EV_N/rd614/verify-hold.out" "$EV_N/rd614/rd614-degraded-banner-before.png" "$EV_N/rd614/rd614-degraded-banner-after.png" \
         "$EV_N/rd629/r1-hold.out" "$EV_N/rd629/r2-hold.out" "$EV_N/rd629/verify-hold.out" \
         "$NX/session-tools/nexusai-lock.sh" \
         "$B12_EV/qa-floorlib12.sh" "$B12_EV/qa-floorcount.py" "$B12_EV/qa-holdlib12.sh" "$B12_EV/HOLD12.sh" "$B12_EV/qa-to.sh" "$B12_EV/qa-jestwrap.sh" "$B12_EV/qa-jsum.js" \
         "$B12_EV/qa-runj12.sh" "$B12_EV/qa-mut12.py" "$B12_EV/qa-mutlib12.sh" "$B12_EV/qa-merge12.sh" "$B12_EV/qa-verify12.sh" "$B12_EV/qa-pin12.sh" "$B12_EV/qa-h1-selftest12.sh" \
         "$B12_EV/qa-h1-scan.py" "$B12_EV/qa-mail.py" "$B12_EV/qa-mailread.py" "$B12_EV/qa-lockcheck.py" "$B12_EV/qa-ssprint.sh" "$B12_EV/qa-netbelt.sb" "$B12_EV/qa-netbelt-nodns.sb" \
         "$B12_EV/qa-netbelt-ctl.js" "$B12_EV/qa-blobcensus12.py" \
         "$B10_EV/qa-c57-id-superset.sh" "$B10_EV/qa-c68census.py" "$B10_EV/qa-cov-setup.js" "$B10_EV/qa-srvlib.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "${C_HEAD:0:12}" "$READY_C" && grep -qF "${D_HEAD:0:12}" "$READY_D" \
  || { echo "REFUSING: a READY (RD-741/603/614/629) does not name its head" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4230/4230 tests passed across 255 suites (jest exit 0)' "$EV_M/rd741-hold.log" && grep -qF 'Tests:       720 passed, 720 total' "$EV_M/rd741-hold.log" \
  && grep -qF 'installed axios 1.20.0' "$EV_M/rd741-hold.log" && [ "$(grep -c 'installed brace-expansion' "$EV_M/rd741-hold.log")" = "0" ] \
  && grep -qF 'VERDICT: PASS — 4254/4254 tests passed across 256 suites (jest exit 0)' "$EV_M/rd603-hold.log" && grep -qF 'Tests:       5 failed, 19 passed, 24 total' "$EV_M/rd603-hold.log" \
  && grep -qF 'HEAD_EXPECT=7983c9d' "$EV_M/rd603-hold.sh" \
  || { echo "REFUSING: a builder log no longer carries the result line the brief quotes (or now prints brace-expansion: WRONG 4 changed)" >&2; exit 31; }
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" && grep -qF 'File **one focused hold at a time** (≤~40 min of jest)' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE the brief quotes (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-26600\}' "$B12_EV/qa-floorlib12.sh" || echo "NOTE: gate 12's qa-floorlib12.sh ROOT default is no longer 26600 — the brief's 'STALE defaults' line names the old value" >&2

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
for P in "$PREV_B10" "$BRIEF12" "$B12_REPORT" "$READY_A" "$READY_B" "$READY_C" "$READY_D"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-741, RD-603, RD-614 and RD-629 are each TIER 2 (through-code)' 'RD-614 adds a BROWSER LEG' 'RD-741 is the PRIORITY member: gate it first' 'One verdict PER ticket' 'TIER 2 AT THROUGH-CODE WEIGHT' 'never a claim that the demo was tested'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-741 (TIER 2, the PRIORITY member, gated FIRST' 'RD-603 with RD-601 (TIER 2, through-code' 'RD-614 (TIER 2 plus a BROWSER LEG' 'RD-629 (TIER 2, test harness only' 'one verdict per ticket' 'never a claim that the demo was tested'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$MAIN_SHA" "$FAE" "$CA7" "$B_MOVE" "$B_DOC" "$B_FC"; do
  grep -qF -- "$S" "$BRIEF" || grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$LOCK_CA7_BLOB" "$LOCK_M_BLOB" "$LOCK_A_BLOB" "$PKG_BLOB" "$SRV_M_BLOB" "$SRV_B_BLOB" "$HP_MOVE_BLOB" "$HP_B_BLOB" "$R603_MOVE_BLOB" "$R603_B_BLOB" "$IDX_M_BLOB" "$IDX_C_BLOB" \
         "$R525_M_BLOB" "$R525_D_BLOB" "$R436_M_BLOB" "$R436_D_BLOB" "$R441_M_BLOB" "$R441_D_BLOB" "$R452_M_BLOB" "$R452_D_BLOB" "$R638_M_BLOB" "$R638_O_BLOB" "$H395_BLOB" "$TS_BLOB" "$ICE_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
for T in "$SUBJECT" "$EARLY_SUBJ"; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $T" >&2; exit 15; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $T" >&2; exit 15 ;; esac
done
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
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-31' "$BRIEF" && grep -qF 'H-32' "$BRIEF" && grep -qF 'H-33' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-31..H-33" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; READY lines verbatim; clarification quotes.
WORDS="RD-741 RD-603 RD-601 RD-614 RD-629 RD-430 RD-707 RD-723 RD-742 C-49 C-57 C-68 C-89 C-102 C-104 C-112 C-115 C-125 C-141 ADDENDUM C-174 C-185 C-186 C-190 C-192 C-193
RED-AT-PARENT a0 a1 a2 a3 a6 a7 a10 b0 b1 b2 b3 b4 b5 c0 c3 c4 c5 d0 y1 y4 MTa MTb MTc MT1 M0 P8 P8b R9/R9b M-nostop L1-L4 GHSA-vfj7-8cjw-p6xm
L-A1 L-A6 L-B1 L-B5 L-C1 L-C4 L-D1 L-D3 H-1 H-15 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
npm%ci%--no-audit%--no-fund npm%audit%--omit=dev%--audit-level=moderate%--json registry.npmjs.org npm%cache 36-file BYTE-IDENTICAL%MOVE near-region BROWSER%LEG open%mode NOT%the%demo unwritable%storage%volume 127.0.0.1
setuid pgrep exits%71 END%ok ===== 4260/258 4230/255 4254/256 4232/256 4234/256 4256/257 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request missing%0
POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b13- qa-b12- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --after DEADLINE HEARTBEAT PEER%gate PROVEN%PID
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child
Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center batch%10 gate%12 COMBINED npm%install HOLD12.sh"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' '^## 8. THE MERGED TREE' '^## 9. CI' '^## 10. Floor discipline' \
         '^## 11. HELD' '^## 12. Output' '^## ADDENDUM SLOT' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^### TARGET C' '^### TARGET D' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-B1 L-B2 L-B3 L-B4 L-B5 L-C1 L-C2 L-C3 L-C4 L-D1 L-D2 L-D3; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a10 b0 b9 c0 c8 d0 d8 y1 y4; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
# every builder's NOT TESTED list and named limits carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; D) F="$READY_D" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|Not covered: no deploy, no demo, no image build, no Partner Center.
A|LIMIT: 8 of the 36 jest.mock('axios'), so they do not exercise real axios 1.20.0; the other 28 load the real modules.
B|The fail-closed branch is not reachable through the product (no producer yields a non-object), so it is proved by the direct cells only.
B|RD-600 stays separate (not touched).
B|P8 red for string, array, number, boolean and Map (5/24 failed). P8-null is green there too
C|a local run of this commit (npm start with a fresh DATA_DIR serves every page in open mode; no auth shim). This is the same commit, NOT the demo image; the demo sits behind RD-76 SSO.
C|for example with an unwritable storage volume (storageStatus 'unwritable' gives the storage reason).
C|in both, the banner is under a dimming overlay that the stubbed page never clears (the dashboard's data calls got {} stubs).
D|NAMED LIMITS / NOT DONE: 11 files kill with SIGTERM only and never confirm the exit (listed on RD-629). That is weaker than failBoot, but it is not this leak unless a child ignores SIGTERM. Not changed; ticket it if you want it closed. Also not done: routing these boots through rd395's bootServer (their env sets differ).
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
a FAILED ls-remote is UNKNOWN, never a value.
absence of a port clash is NOT evidence of a quiet floor.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
O-1 counts as known ONLY while its failure is
counts as known ONLY when the received object differs from the expected in `envReached` alone
When it merges, the known set returns to {}.
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
condition (2) is decided on BLOBS, and commit lists are evidence only
No re-run is used as a clearance
THE TURN PASSES
The DEGRADED service banner's title is cause-neutral
a browser render for the testing agent at READY.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b13-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
         'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' 'C-104' 'Main may move' '--after' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' \
         'session-tools/locks/queue-jest/' 'carry on' 'never idles holding the jest lock' 'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' 'PEER gate'; do
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
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4260/258' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'npm audit --omit=dev --audit-level=moderate --json' 'npm ci --no-audit --no-fund' 'exception (m)' 'GHSA-vfj7-8cjw-p6xm' 'RD-742' 'devOptional' '36-file' 'jest.mock' \
         'BYTE-IDENTICAL MOVE' '46c46' 'P8b' 'WRONG 3' 'near-region' 'fb6e67d' '80708a7' 'f70594a' '5584ea4' 'BROWSER LEG' 'Claude-in-Chrome' 'NOT the demo' 'unwritable' 'overlay' \
         'M-nostop' 'NO `-t` title filter' 'PROVEN PID' 'rd638' 'E2 LEFT the set' '37198193233' '37191653227' 'Never `npm install`' 'qa-floorlib12.sh' 'HOLD12.sh' 'EARLY VERDICT' 'ADDENDUM SLOT' 'RD-430 SLOT'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this batch's premise '$w'" >&2; exit 81; }
done

# 89 — the RD-430 ADDENDUM SLOT: EMPTY (not a member) or exactly one JOINS line, re-pinned by ls-remote, its READY on disk naming the head.
R430_JOINS="$(grep -E '^ADDENDUM RD-430 JOINS @ [0-9a-f]{40} \| READY /' "$BRIEF" 2>/dev/null)"
R430_EMPTY="$(grep -c '^RD-430 SLOT: EMPTY$' "$BRIEF" 2>/dev/null)"
R430_STATE=''
if [ -n "$R430_JOINS" ]; then
  [ "$(printf '%s\n' "$R430_JOINS" | grep -c .)" = "1" ] && [ "$R430_EMPTY" = "0" ] || { echo "REFUSING: the RD-430 ADDENDUM SLOT has more than one JOINS line, or JOINS and EMPTY both (89)" >&2; exit 89; }
  R430_SHA="$(printf '%s\n' "$R430_JOINS" | sed -E 's/^ADDENDUM RD-430 JOINS @ ([0-9a-f]{40}) .*/\1/')"
  R430_READY="$(printf '%s\n' "$R430_JOINS" | sed -E 's/^.* \| READY (\/.*)$/\1/')"
  [ "$P430_NOW" = "$R430_SHA" ] || { echo "REFUSING: the RD-430 ADDENDUM names $R430_SHA but origin $P430_BRANCH is '${P430_NOW:-absent}' (89)" >&2; exit 89; }
  [ "$(g cat-file -t "$R430_SHA" 2>&1)" = "commit" ] || { echo "REFUSING: RD-430 $R430_SHA is not in the object store (89)" >&2; exit 89; }
  [ -s "$R430_READY" ] && grep -qF "${R430_SHA:0:7}" "$R430_READY" || { echo "REFUSING: RD-430's READY '$R430_READY' is absent or does not name ${R430_SHA:0:7} (89)" >&2; exit 89; }
  if g merge-base --is-ancestor "$R430_SHA" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: RD-430 ${R430_SHA:0:7} is already on main (89)" >&2; exit 89; fi
  RC430="$(conflicts "$M_ORIGIN" "$R430_SHA" | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$RC430" ] || [ "$RC430" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree main x RD-430 conflicts beyond the counts file: '$RC430' (89)" >&2; exit 89; }
  R430_STATE="RD-430 JOINS this gate per the brief's ADDENDUM SLOT, at $R430_SHA (origin $P430_BRANCH, re-pinned by the launcher), READY $R430_READY — gate it as the ADDENDUM paragraph says, merge it LAST (step e)."
else
  [ "$R430_EMPTY" = "1" ] || { echo "REFUSING: the RD-430 ADDENDUM SLOT is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
  R430_STATE="RD-430 is NOT a member of this gate (the brief's ADDENDUM SLOT is EMPTY): do not gate it; say so in the report."
fi

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §10 clause 1)" >&2
  BQ="$(grep -l 'qa-b12-' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ gate-12 (qa-b12-) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
else
  echo "NOTE: jest queue dir $LOCKQ not found — the gate reads the lock tool's own layout at start" >&2
fi

# 38R (from resume_qa_nexusai_gate_batch12.sh) — the negative-control seats are DERIVED now from the live cockpit panes: the claude descendant of each pane pid.
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
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P wednesday; do
  PP="$(pane_pid_of "$NAME")"
  [ "$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named '$NAME', found: '${PP:-none}' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
done
NEG_SEATS="${NEG_SEATS# }"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "5" ] || { echo "REFUSING: the five derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
# gate 12's own claude, if its pane is live: a sixth negative control (a NOTE when absent — gate 12 may have finished).
G12P="$(pane_pid_of "$ROUTE_NAME12")"
G12C=''
[ -n "$G12P" ] && [ "$(printf '%s\n' "$G12P" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && G12C="$(claude_under "$G12P")"
if [ -n "$G12C" ] && [ "$(printf '%s\n' "$G12C" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
  NEG_SEATS="$NEG_SEATS $G12C"; NEG_DESC="$NEG_DESC \`$G12C\` ($ROUTE_NAME12, the live peer gate);"
else
  echo "NOTE: no live claude under a pane named $ROUTE_NAME12 — gate 12 finished or its pane is gone; five negative controls" >&2
fi

# 86 (new) — no live gate-13 session already exists: a pane named QA/NexusAI-batch13 with a claude under it REFUSES (two sessions, one report).
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 13 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
# Both are checked and every missing item printed, so --check shows them all; the route's absence exits 40, else a stamp placeholder exits 32.
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 93 94 95 96 23 35 70 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}; on main:${ON_MAIN:- none}" >&2
  echo "  member pins (origin, re-read now): RD-741 $A_HEAD · RD-603 $B_HEAD · RD-614 $C_HEAD · RD-629 $D_HEAD" >&2
  echo "  NEG seats (38R, derived live):$NEG_DESC" >&2
  echo "  RD-430: ${R430_STATE}" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): a stamp placeholder remains in the brief (the SELF-CHECK line / Self-check note) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: 4 member branches at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192): RD-741 ${A_HEAD:0:7} RD-603 ${B_HEAD:0:7} RD-614 ${C_HEAD:0:7} RD-629 ${D_HEAD:0:7}"
  echo "  main ${M_ORIGIN:0:7} (630bb24 or a descendant; no member path moved) (18b); on main:${ON_MAIN:- none}; RD-430 ${P430_NOW:0:7} RD-707 ${O707_NOW:0:7} RD-733 ${M733_NOW:0:7}"
  echo "  merge-bases (7); chains (8); deltas (22); premises RD-741 (93) RD-603 (94) RD-614 (95) RD-629 (96)"
  echo "  overlaps (23); counts + census (35); locks (70); $MT_PAIRS three-argument merge-trees counts-only (80); evidence (31); C-133 script (83)"
  echo "  H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); MODEL RULE (82); RD-430 slot (89); queue (41); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live):$NEG_DESC"
  echo "  RD-430: $R430_STATE"
  echo "  model: claude-opus-5-5 at exec"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$P430_BRANCH = ${P430_NOW:-absent}; refs/heads/$O707_BRANCH = ${O707_NOW:-absent}; refs/heads/$M733_BRANCH = ${M733_NOW:-absent}; refs/heads/main = $M_ORIGIN (630bb24 or a descendant; no member path moved since 630bb24; already on it:${ON_MAIN:- none}). $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only across main and every member pair. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
$R430_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
