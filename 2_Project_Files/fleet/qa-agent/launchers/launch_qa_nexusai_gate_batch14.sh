#!/bin/bash
# launch_qa_nexusai_gate_batch14.sh — cross-project QA agent, ONE batched gate on Datasec/NexusAI ("batch 14"), FIVE members, one verdict per ticket,
# ONE report (2026-10-05). A FRESH gate (not a resume): M0 is origin main as the gate reads it at its own start.
#   A — RD-736 (TIER 2, test helper) rd-736-either-reading-carrier-s87o @ 61e20ad: eefc610 on fae2aa1, merged forward with 55333df (9b26b36), counts. 4242/256.
#   B — RD-737 (TIER 1, image content, test code) rd-737-key-rule-guard-s87o @ 88f3d11: e447230 on 55333df, counts. 4256/256.
#   C — RD-708 (TIER 2, test code) rd-708-stale-reviewed-entry-s87o @ ed539e4: 01aa919 on 55333df, counts. 4234/255. PRIOR WORK in an ADDENDUM in its READY.
#   D — RD-690 (TIER 1, shipped comments + test) rd-690-workspace-prefix-comments-s87o @ b05b6ff: ONE commit on 55333df, counts unchanged 4231/255.
#   E — RD-675 (TIER 2, test code) rd-675-ban-wide-windows-scripts-s87o @ 12de511: ce89bb2 on 5fd2398, counts. 4238/255.
#   All five are NexusAI-O (S87O). C and D both edit rd385's RD-425 describe in separate hunks (clean merge; COMBINED blob 9d3329e predicted).
#   OPTIONAL — RD-430 (NexusAI-P) joins ONLY by the brief's ADDENDUM SLOT line "ADDENDUM RD-430 JOINS @ <sha> | READY <path>" (guard 89).
#   Main at drafting 3b6c9ec (RD-692; before it RD-741 5fd2398, RD-707 55333df). RD-733 (M) may land before launch: a NOTE, the gate re-bases on its own M0.
#   Predicted MT1 (M0 + A + B + C + D + E) 4282/258 at M0 = 3b6c9ec.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch14' "bash '/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch14.sh'"
#   (i.e. /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's batch 14 commission (2026-10-05 ~06:1x AEDT); READY mails copied in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION. Starts on Opus 5.5.
# This gate is FINDINGS-ONLY: it NEVER merges (outside its own scratch clones), NEVER pushes, NEVER opens/comments/approves a PR (C-190 is the merge
# authors' route); no fix, no deploy, nothing to Partner Center/demo/prod, no az, no docker, NO npm registry (node_modules offline only, H-31).
#
# PATTERN: launch_qa_nexusai_gate_batch13.sh (prompt EMBEDDED, --check mode, pin guards, THE MODEL RULE, floor, H-rules, the LIVE negative-control seat
# derivation 38R, route-line and stamp guards last, the RD-430 ADDENDUM slot). CHANGES versus gate 13's launcher, each deliberate:
#   - members/bases/chains/deltas/premises re-written for RD-736, RD-737, RD-708, RD-690, RD-675 (guards 6 7 8 22 93-97 23 35 70 80 31).
#   - 22b (new): NO member delta may touch package-lock.json or package.json (ruling m: the registry exception does NOT carry).
#   - 23: the expected overlap set is the counts file PLUS C x D on rd385 (the commission's coupling); anything else refuses.
#   - 80: three-argument merge-trees must be counts-only OR clean; C x D must be clean (it is the COMBINED rd385).
#   - 18b: main must be 3b6c9ec or a descendant; main moving a member path or .dockerignore REFUSES; the lock, Dockerfile, ICE, the review
#     fixture, rd465/rd549 moving is a NOTE; RD-733 / RD-430 landing a NOTE.
#   - 38R: gate 12's AND gate 13's claudes are added as negative controls if live (a NOTE for each absent one).
#   - 86: REFUSES if a pane named QA/NexusAI-batch14 already runs a claude.
#   - no EARLY verdict (no priority member); no registry exception (m); no browser leg.
#
# Identity: exports NexusAI's OWN az/gh dirs (az unused, gh READ-ONLY for §10); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree) plus the
# three-argument merge-tree (stdout only); python over `git show` output; grep, ls, shasum, ps, tmux, test -e. It writes nothing anywhere and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch14.sh [--check]
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
BRIEF="$BRIEFS/2026-10-05_nexusai-gate-batch14.md"
BRIEF13="$BRIEFS/2026-10-04_nexusai-gate-batch13.md"
READY_A="$BRIEFS/2026-10-05_nexusai-rd736-READY-mail.txt"
READY_B="$BRIEFS/2026-10-05_nexusai-rd737-READY-mail.txt"
READY_C="$BRIEFS/2026-10-05_nexusai-rd708-READY-mail.txt"
READY_D="$BRIEFS/2026-10-05_nexusai-rd690-READY-mail.txt"
READY_E="$BRIEFS/2026-10-05_nexusai-rd675-READY-mail.txt"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EV_O="$NX/session-tools/s87o"
LOCKQ="$NX/session-tools/locks/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
C133="$NX/session-tools/s78g/c133-accounting.py"
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'
RPTS="$QA_DIR/projects/nexusai/reports"
B13_DIR="$RPTS/2026-10-04-gate-batch13"
B13_INST="$B13_DIR/evidence/inst"
B12_REPORT="$RPTS/2026-09-30-gate-batch12/report.md"
PREV_B10="$RPTS/2026-09-29-gate-batch10/report.md"
PREV_B4="$RPTS/2026-09-27-gate-batch4/report.md"
PREV_FLOORLIB="$B13_INST/qa-floorlib13.sh"
G7R1_FLOOR="$RPTS/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
REPORT="$RPTS/2026-10-05-gate-batch14/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch14'
ROUTE_NAME12='QA/NexusAI-batch12'
ROUTE_NAME13='QA/NexusAI-batch13'
NPM_CACHE="${HOME}/.npm/_cacache"

MAIN_SHA='3b6c9ec52cc6def9a47b3baff8b293fa27359e99'      # origin main at drafting (06:15:29 AEDT; RD-692)
M707='55333df5ca3b86d26f39be2c45145b5132bd648e'          # RD-707's main — A, B, C, D's base
M741='5fd239853f1d1e6a0a36fa8df349d05a1cb4b9f8'          # RD-741's main — E's base
M630='630bb249c7740fee57a371378371afcfff33c454'          # gate 13's M0 (ancestor check only)
FAE='fae2aa12cd6d27c6a46e690ce57c15052f164472'           # A's first commit's parent
A_BRANCH='rd-736-either-reading-carrier-s87o'
A_HEAD="${QA_A_HEAD_OVERRIDE:-61e20ad841f245a4b19f1ec8c2d56dfea2bd65fe}"
A_FIX='eefc6107cc9b1eddce9d0934850d86d2f5ce413d'          # fix + cells, on fae2aa1
A_MRG='9b26b36f0af43e87eb2f22104706ea7b5c96da7f'          # merge of main 55333df
B_BRANCH='rd-737-key-rule-guard-s87o'
B_HEAD="${QA_B_HEAD_OVERRIDE:-88f3d11179d2b5ea46ce95da65d19d94b951e136}"
B_FIX='e447230abdbcd6e4c7c596ae0c3253f0424dd0e8'
C_BRANCH='rd-708-stale-reviewed-entry-s87o'
C_HEAD="${QA_C_HEAD_OVERRIDE:-ed539e415bb310f824a1428173a6e4737e2b3297}"
C_FIX='01aa9192037367a704f296a3fcda98e4917a2ce5'
D_BRANCH='rd-690-workspace-prefix-comments-s87o'
D_HEAD="${QA_D_HEAD_OVERRIDE:-b05b6ffe15ca6bd6a1577795dbba504da9cb5127}"
E_BRANCH='rd-675-ban-wide-windows-scripts-s87o'
E_HEAD="${QA_E_HEAD_OVERRIDE:-12de5116a66664f07e15064939e318bbe35ee915}"
E_FIX='ce89bb2d32620a3bff90aeadb39d11328f1d0424'
P430_BRANCH='rd-430-remove-response-form-s84p'
P430_SHA='379b8b57b823268e372000229a613739688e443c'       # NOT a member unless the ADDENDUM SLOT says JOINS (89)
M733_BRANCH='rd-733-user-access-stale-entra-check-s86m'
M733_SHA='ed4c1bfd5a195f163b8f76e84b467157f8b97813'       # not on main; both C-185 O-1 cells leave the set when it lands — a NOTE

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
IM='__tests__/helpers/image-manifest.js'
R736='__tests__/rd736-ambiguous-run-either-reading.test.js'
R418='__tests__/rd418-dockerignore-round3.test.js'
R737='__tests__/rd737-key-suffix-rule-guard.test.js'
R385='__tests__/rd385-shipped-root-markdown-identifiers.test.js'
LAW='backend/azureLogAnalytics.js'
R429='__tests__/rd429-nul-byte-does-not-hide-a-file.test.js'
DIG='.dockerignore'
DKF='Dockerfile'
ICE='__tests__/image-content-exposure.test.js'
REVIEW='__tests__/fixtures/image-carrier-review.json'
TS='__tests__/helpers/test-server.js'
R465='__tests__/rd465-first-run-open-window.test.js'
R549='__tests__/rd549-ai-config-inert-until-confirmed.test.js'

LOCK_OLD_BLOB='f74a4e8679491d6c1a496c96b405b15673dbc0fb'   # 55333df, A, B, C, D (pre-RD-741)
LOCK_M_BLOB='e9063d44757007324b8c55fa58c03c03dfe552ae'     # 5fd2398, M0, E
PKG_BLOB='cdb1168783a92179afe20be67b37976203b904f8'        # every sha here
IM_M_BLOB='23bfa4fcf4976b139e101162fa4699497c4dc146'
IM_A_BLOB='2040ca2ec3a712561011829ce7672fb18861c5c5'
R736_BLOB='6978d32eeb0feccd108bf40e2dfd4164dc9bc4bd'
R418_M_BLOB='b72f8c9a34c98ee47dab6b6463489ed55b48bbc2'
R418_B_BLOB='2f0d1a4aa3d3534018efb808fa03d1b0de815cea'
R737_BLOB='25c9986243b03172385f67c0dc0b0ea4283c8cab'
R385_M_BLOB='d1b26f30e1816c231b1654ca00ba314d468cb217'
R385_C_BLOB='401e31d26295e242dcb6006682ff9dfef0830068'
R385_D_BLOB='58181897b101dfc8bbeec3e0f6156b0da912fbe0'
R385_CD_BLOB='9d3329ee132f22fde8419c28a5f2daa9a5d7619a'    # COMBINED prediction (merge-file + hash-object, no -w) — the gate measures it
LAW_M_BLOB='036c34f7cf32e51451fdab4ca283f95ad9711e82'
LAW_D_BLOB='ffdc003c78036257a4da6a4ea7f48025e8d7ae4c'
R429_M_BLOB='7544939b12e010653e4253d45a8f362d850d086d'
R429_E_BLOB='d38e28f49ac1adc0148ef3c551a1312dd0f7a992'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'        # 55333df, M0, every head
DKF_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
ICE_BLOB='7e3262b001088991f7b3660c0a2949139f80510a'
REVIEW_BLOB='7ec591046399b1b9ecc9191817998bee0559e32a'
TS_BLOB='cff1e54099bb3aa88f11d16f22599f32006f4095'         # RD-591 NOT on main (H-23)

A_EXPECTED_FILES="$IM
$R736
$COUNTS_FILE"
B_EXPECTED_FILES="$R418
$R737
$COUNTS_FILE"
C_EXPECTED_FILES="$R385
$COUNTS_FILE"
D_EXPECTED_FILES="$R385
$LAW"
E_EXPECTED_FILES="$R429
$COUNTS_FILE"
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 14'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch14] ANSWER'
NOTTESTED_LINE="Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Docker image build or image diff (the tier-1 image legs are manifest evaluations), the demo (behind RD-76 SSO), any deployed environment, any browser, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
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

You are the fleet QA/testing agent running ONE batched gate on Datasec/NexusAI, "batch 14", with FIVE members, one verdict per ticket and ONE report. It is a FRESH gate. All five are NexusAI-O's and all five are test code except two shipped comment lines. The members: RD-736 (TIER 2, test helper: the image-content gates' shared reader, helpers/image-manifest.js, now gives the gates BOTH readings of an ambiguous wide run, keepLE; batch-10 B-F1 + B-F2); RD-737 (TIER 1, image content, test code: every RD-707 .dockerignore rule gets a plant it alone excludes, and the broad key-suffix rules are guarded over tracked files; .dockerignore itself unchanged; batch-10 C-F1 + C-N1); RD-708 (TIER 2, test code: a REVIEWED identifier entry in rd385 that no longer matches a live finding is reported stale; batch-4 B-F1; its PRIOR WORK came as an ADDENDUM in the same READY file); RD-690 (TIER 1, shipped comments: two comments in backend/azureLogAnalytics.js lose their workspace-ID prefixes, the C-17 class, and rd385's REVIEWED entry for them goes); RD-675 (TIER 2, test code: rd429 bans a tracked UTF-16 .bat, .cmd or .htm, Tuesday's ruling (a)). Each ticket gets its own verdict — GO, GO WITH FINDINGS or NO GO — about its branch head AND about the merged tree. A finding on one ticket never becomes another's verdict. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, and NEVER open, comment on, approve or merge a pull request; no fixes, no deploys, nothing to Partner Center, the demo or production, no az, no docker, no image build, no npm registry.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-05_nexusai-gate-batch14.md
It opens with TUESDAY'S RULINGS (a) to (m) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, then the five READY mails it names (read each WHOLE; RD-708's PRIOR WORK is its ADDENDUM, appended in the same file), then gate 13's brief (the base of your instrument rules H-1 to H-33; gate 13 is STILL RUNNING: read only, never its trees, never its report dir), gate 12's report's RESUME METHOD NOTE (gate 12 may also still be running: read only), then the batch 10 and batch 4 reports it names (the findings these members answer). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES tables (section 2a) are required measurements, row by row, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows, including the planted ones (D's workspace-prefix census, C's planted stale entries, B's planted key files, E's planted UTF-16 scripts) — every one is an authorised, findings-only measurement in your own trees. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running jest step finish and let the hold exit so you never sit holding the jest lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGETS. RD-736: rd-736-either-reading-carrier-s87o at 61e20ad841f245a4b19f1ec8c2d56dfea2bd65fe (eefc6107cc9b1eddce9d0934850d86d2f5ce413d on fae2aa12cd6d27c6a46e690ce57c15052f164472, merged forward with main 55333df5ca3b86d26f39be2c45145b5132bd648e as 9b26b36f0af43e87eb2f22104706ea7b5c96da7f, then counts). RD-737: rd-737-key-rule-guard-s87o at 88f3d11179d2b5ea46ce95da65d19d94b951e136 (e447230abdbcd6e4c7c596ae0c3253f0424dd0e8 on 55333df, then counts). RD-708: rd-708-stale-reviewed-entry-s87o at ed539e415bb310f824a1428173a6e4737e2b3297 (01aa9192037367a704f296a3fcda98e4917a2ce5 on 55333df, then counts). RD-690: rd-690-workspace-prefix-comments-s87o at b05b6ffe15ca6bd6a1577795dbba504da9cb5127 (ONE commit on 55333df; counts unchanged). RD-675: rd-675-ban-wide-windows-scripts-s87o at 12de5116a66664f07e15064939e318bbe35ee915 (ce89bb2d32620a3bff90aeadb39d11328f1d0424 on 5fd239853f1d1e6a0a36fa8df349d05a1cb4b9f8, then counts). The deltas share NO path but the counts file, EXCEPT RD-708 and RD-690, which edit rd385's RD-425 describe in separate hunks: a clean merge with a COMBINED rd385 blob (predicted 9d3329e). They share SEMANTIC surfaces: RD-736's image-manifest helper sits under every other member's cells (rd737, rd418, rd385, rd429 require it); RD-708's stale guard reads the REVIEWED list RD-690 edits and the shipped file RD-690 changes — C-68 re-runs rd385 BY NAME on the merged tree, and y2's control proves the coupling in both directions. RD-430 (NexusAI-P) is NOT a member unless the brief's ADDENDUM SLOT says it JOINS (the launcher tells you below). A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

MAIN MAY MOVE BEFORE AND DURING YOUR GATE (ruling b). Take M0 = origin main AT YOUR OWN START by git ls-remote, say so, and RE-BASE EVERY PREDICTION on it: counts (MTa = M0 + RD-736 4247/257; MTb = + RD-737 4272/258; MTc = + RD-708 4275/258; MTd = + RD-690 4275/258; MT1 = + RD-675 4282/258, predicted at M0 = 3b6c9ec52cc6def9a47b3baff8b293fa27359e99), the tests census (301 at MT1), new ids 46, missing 0. Four members are cut from 55333df and carry the pre-RD-741 lock (stale-parent); RD-675 is cut from 5fd2398. Members are merged forward onto M0 in YOUR OWN trees, never in a builder's worktree. Never re-base mid-gate; at your END measure each member onto the main you find by merge-tree. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value.

C-190: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included). No PR exists for any member branch at drafting: CodeQL is NOT RUN and the CI Build is NOT RUN at any member head — say so; re-read with gh READ ONLY. npm-audit runs on every branch push: the four heads carrying the old lock fail it because of that lock, not the member — say so READ ONLY. C-185 with its ADDENDA on M0: the known-failing set is {rd465 O-1 "Turn on Authentication Control: success removes the banner" AND its sibling O-1 'Step 3 "Enforce Authentication": success removes the banner', each only with the checkEntraStatus TypeError; rd549 O4 only when envReached alone differs}; both O-1 cells leave the set when RD-733 merges. A local failure of any of these is named, never waved.

THE ROWS (brief section 2a), POSITIVE CONTROL FIRST in every target. RD-736: a0 RED-AT-PARENT first (the head's rd736 against main's helper 23bfa4f: exactly the 5 B-F1 cells red), a1-a8 including the mutants M-noLE, M-latin, M-display plus your own, the batch-10 r5b planted carriers on planted BYTES, the tracked differential at M0 AND MT1, and C-194's review fingerprints unchanged. RD-737 (TIER 1): b0 THE IMAGE LEG as a MANIFEST EVALUATION (the gates' own shippedFiles over git ls-files with the real .dockerignore at M0, head and MT1 — said as "manifest evaluation, NO image built"; a docker build is NOT RUN); b1 RED-AT-PARENT = drop each of the 20 RD-707 rules with main's rd418 (exactly 12 stay green) and with the head's (0); b2 each plant excluded by exactly ONE rule; b4 the C-N1 guard on a REAL tracked api.key.js committed in YOUR clone; b5-b8. RD-708: c0 RED-AT-PARENT = M-stale (silent on main's rd385, 3 red on the head's), c1-c8 including a count going down, the RD-689 forecast (its 5 entries) and the ADDENDUM's prior work claim by claim. RD-690 (TIER 1): d0 RED-AT-PARENT = M-back (exactly the RD-690 group, 3 red); d1 comments only by the comment-aware compare; d2 the workspace prefixes gone from EVERY shipped file at head and MT1 (2 at M0 as the positive control) — derived and compared IN MEMORY ONLY, never printed, written or mailed; d3 THE IMAGE LEG as a manifest evaluation (exactly one shipped file's blob changes); d4-d8. RD-675: e0 RED-AT-PARENT = M-oldlist (exactly the 3 planted UTF-16 cells), e2 the tracked census 0, e3 THE BAN ON A TRACKED FILE (a UTF-16LE .bat, .CMD, .HTM committed in YOUR clone reddens the head's tracked cell and not the base's), e4-e7. Cross cells y1-y5 on MT1.

PRIOR WORK: verify each READY's PRIOR WORK section claim by claim (C-49) — VERIFIED, FALSE or UNVERIFIED with its evidence class. RD-708's is its ADDENDUM.

THE MERGED TREE — part of every verdict (brief section 9). In YOUR OWN scratch clone (git clone --shared --no-checkout into your own project dir; origin removed; local user config; gc.auto 0; hooks off; merges and commits in the clone ONLY): M0, then merge --no-ff RD-736 (MTa), RD-737 (MTb), RD-708 (MTc), RD-690 (MTd), RD-675 (MT1). Re-measure every pair by merge-tree --write-tree in a SCRATCH object dir first (GIT_OBJECT_DIRECTORY your own, NexusAI's objects only as GIT_ALTERNATE_OBJECT_DIRECTORIES) — the drafter's READ-ONLY three-argument merge-trees: every pair conflicted on the counts file only or was clean; the one COMBINED blob is rd385 (RD-708 with RD-690). Predict each merge before it; anything other than the counts file conflicting STOPS (C-57). C-104: resolve and stage before any census or run. Counts by REGENERATION once on MT1 on node_modules proven for M0's lock: predicted 4282/258, re-based on YOUR M0; the measurement decides. A second clone in reverse order, root trees identical apart from the counts file. The id-superset control LIKE WITH LIKE, all K1, both controls (a planted missing id STOPS; a superset passes): predicted missing 0; any missing id is a STOP. C-68 unions by name, in holds per H-28. C-89 on your clone. Count the NexusAI object files before and after and account for any delta by full-date mtime. Nothing leaves your clone; never push.

NODE_MODULES WITHOUT THE REGISTRY (ruling m, H-31). No member changes the lock or package.json, so there is NO npm registry exception in this gate. Two locks are in play (the pre-RD-741 lock for RD-736, RD-737, RD-708 and RD-690; M0's for RD-675 and every merged tree). For each lock ONCE: npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache under your own mktemp dir, in your own tree, under a deadline; an ENOTCACHED is NOT RUN for that lock (name it, mail a QUESTION) — never go online, never npm install. Every other tree clones node_modules from one of your two proven trees; never from gate 12's or gate 13's trees.

FULL VERIFY of each head and of MT1 through the lock, SESSION_SECRET UNSET, npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest or say it did not), K1 trees only, each on node_modules PROVEN for its own lock. Predicted 61e20ad 4242/256, 88f3d11 4256/256, ed539e4 4234/255, b05b6ff 4231/255, 12de511 4238/255, MT1 4282/258. Every builder verify ran on its pre-counts commit with --update-counts; yours decides. Every failure by NAME. Re-run-until-green is not an acceptance gate. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES AND LANDED: node --check every mutated JS file and quote the exit code, assert each anchor matched once and the exact mutated text is present; a red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-33 (brief section 3a). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it with a throwaway, scan every hold's logs for it, and let the scan's control plant a DIFFERENT marker; the same in-process scan covers RD-690's workspace prefixes. H-3: a LANDING CONTROL for every plant, planted tracked file, read override or mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap per hold reported (at most 120 s). H-9: byte plants by Buffer, checked with xxd. H-15: preloads with -r in argv; no exception this batch. H-20: EVERY jest invocation carries --forceExit AND a per-step hard deadline (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation, hash-compared to its pinned blob after every hold. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the test paths. H-25: the comment-aware compare with its IGNORED control. H-26: C-192 retries. H-27: THE MODEL RULE. H-28 (gate 12's wrap, gate 13's stamped reading): ONE focused hold at a time, at most about 40 minutes of planned jest, every part file written and bash -n checked before the hold is filed; you stay in the FOREGROUND for the whole hold — a hold that must outlive one foreground tool call runs as a TRACKED child of your session (never nohup) with its own timeout at the 2-hour maximum while you poll its output, because backgrounded commands die at 2 h and lock waits have run 5600 to 8995 s; each hold carries a wait deadline and re-files cleanly under the SAME tag if not granted. H-29: gates 12 and 13 are live; their evidence is method only. H-31: offline node_modules. H-32: the tier-1 image legs are manifest evaluations, NO image built. H-33: plants and scratch dirs counted and quarantined, never rm. The rest as the brief states them.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch14.*), status-checked before use. Each tree is EXCLUSIVE to this gate and to one purpose; gate 12's and gate 13's trees and report dirs are not yours — read their evidence only, copy instruments BY COPY from gate 13's evidence/inst (its HOLD13.sh hard-codes its own evidence dir and its qa-floorlib13.sh carries stale ROOT and NEG defaults: re-point and correct your copies). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list; count-objects for the object accounting); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, and merge-tree --write-tree ONLY with your own scratch object directory; never work in its 2_Project_Files checkout or any builder worktree. Never write into the builders' session-tools: copy, then hash at start and end; never run their hold, red or mutate scripts. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI. No Azure (no az at all), no demo, no docker, no image build, no Partner Center, no ARM deployment, no npm registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 11 of the brief exactly. MERGES GO FIRST: the jest lock (session-tools/nexusai-lock.sh, queue session-tools/locks/queue-jest) is shared with gate 12 (QA/NexusAI-batch12, tags qa-b12-) and gate 13 (QA/NexusAI-batch13, tags qa-b13-) — each a PEER gate: FIFO, never touched — and the four builder seats; merges go one at a time in the C-186 ADDENDUM's turns. Do ALL lock-free work first (pins, reads, merge-trees in scratch objects, the offline npm ci, plain-node rows, census greps); then file your holds tagged qa-b14-, one at a time; if a MERGE ticket (a tag containing "merge") is queued ahead of you, wait behind it; if one files behind you BEFORE your hold is granted, re-file your ticket behind it (stop your OWN unstarted waiter by pid from your own ancestry, then re-queue with --after that merge ticket's tag, C-141 ADDENDUM 4) under your UNCHANGED tag (C-141 ADDENDUM 5: builders yield once per gate TAG); once granted, carry on. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock or ticket. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count beside every result; count every child you start and prove none left; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every npm call, node driver and jest run has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: the five member branches, RD-430's, RD-733's and main — three timestamped readings with the branch name and attempt count beside each sha. A TICKET head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Main MAY move: call main at your start M0 and say so; it must be 3b6c9ec or a descendant; if main moves again, your verdict names M0 and says what moved (C-68); never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch14. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch14] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch14/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 14
Lead the body with one line per ticket, in the forms the brief's section 13 gives (RD-736 @ 61e20ad with B-F1 red at base, planted carriers flagged, the tracked differential and the fingerprints; RD-737 @ 88f3d11 with the image leg as a manifest evaluation, NO image built, the unplanted rules at main and head, plants with more than one excluding rule, and the tracked api.key.js; RD-708 @ ed539e4 with M-stale at main and head, live entries called stale and the coupling control; RD-690 @ b05b6ff with prefixes in shipped files at head and MT1 as counts only, code tokens changed and the image leg as a manifest evaluation; RD-675 @ 12de511 with M-oldlist reds, the tracked ban and today's tracked count), then one line naming M0, your recommended merge order, the merged counts you measured, the C-57 result, the rd385 combined blob, which rows ran on Opus 4.8 (or none), and "CodeQL NOT RUN (no PR); Build NOT RUN (no PR)". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a workspace prefix or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying every builder's stated limits as the brief quotes them, every declared limit L-A1 to L-A4, L-B1 to L-B5, L-C1 to L-C4, L-D1 to L-D4, L-E1 to L-E4 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked for each ticket (C-49), and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. C-17, C-167, C-185 with its ADDENDA, C-190, C-192 and C-194 are the clarifications this batch leans on; C-49, C-57, C-68, C-89, C-102, C-104, C-112, C-115, C-125, C-141 with ADDENDUM 5, C-173, C-174 and C-186 are carried. That section must carry this line verbatim:
Not tested by this gate: Linux or CI Build at any branch head (no PR exists, so no CI Build ran there), CodeQL at any head without a PR, a real Docker image build or image diff (the tier-1 image legs are manifest evaluations), the demo (behind RD-76 SSO), any deployed environment, any browser, a real Key Vault, a real Entra tenant, real Azure, Partner Center, docker, the npm registry (node_modules from an offline cache copy with install scripts skipped), and Windows.
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
for S in "$MAIN_SHA" "$M707" "$M741" "$M630" "$FAE" "$A_HEAD" "$A_FIX" "$A_MRG" "$B_HEAD" "$B_FIX" "$C_HEAD" "$C_FIX" "$D_HEAD" "$E_HEAD" "$E_FIX" "$P430_SHA" "$M733_SHA"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 — merge-bases: each member's own base with main; the bases are on main.
for S in "$M630" "$M707" "$M741" "$FAE"; do
  g merge-base --is-ancestor "$S" "$MAIN_SHA" 2>/dev/null || { echo "REFUSING: ${S:0:7} is not an ancestor of 3b6c9ec — re-brief" >&2; exit 7; }
done
for PAIR in "$A_HEAD $M707" "$B_HEAD $M707" "$C_HEAD $M707" "$D_HEAD $M707" "$E_HEAD $M741"; do
  H="${PAIR% *}"; W="${PAIR#* }"
  [ "$(g merge-base "$H" "$MAIN_SHA" 2>/dev/null)" = "$W" ] || { echo "REFUSING: merge-base(${H:0:7}, 3b6c9ec) is not ${W:0:7} — re-brief" >&2; exit 7; }
done

# 8 — chains exact.
[ "$(g log --format='%H %P' "${M707}..${A_HEAD}" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$A_HEAD $A_MRG $A_MRG $A_FIX $M707 $A_FIX $FAE" ] \
  || { echo "REFUSING: 55333df..RD-736 is not exactly eefc610 (on fae2aa1) -> 9b26b36 (merge 55333df) -> 61e20ad" >&2; exit 8; }
for TRIPLE in "$B_HEAD $B_FIX $M707" "$C_HEAD $C_FIX $M707" "$E_HEAD $E_FIX $M741"; do
  set -f; set -- $TRIPLE; set +f
  [ "$(g log --format='%H %P' "${3}..${1}" 2>/dev/null | tr '\n' ' ' | sed 's/ $//')" = "$1 $2 $2 $3" ] || { echo "REFUSING: ${3:0:7}..${1:0:7} is not exactly two linear commits ${2:0:7} -> ${1:0:7}" >&2; exit 8; }
done
[ "$(g log --format='%H %P' "${M707}..${D_HEAD}" 2>/dev/null)" = "$D_HEAD $M707" ] || { echo "REFUSING: 55333df..RD-690 is not exactly one commit b05b6ff on 55333df" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the five ticket branches exactly the pins (REFUSE); RD-430 / RD-733 a NOTE.
lsr refs/heads/main "refs/heads/$A_BRANCH" "refs/heads/$B_BRANCH" "refs/heads/$C_BRANCH" "refs/heads/$D_BRANCH" "refs/heads/$E_BRANCH" "refs/heads/$P430_BRANCH" "refs/heads/$M733_BRANCH" || {
  echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
for PAIR in "$A_BRANCH $A_HEAD" "$B_BRANCH $B_HEAD" "$C_BRANCH $C_HEAD" "$D_BRANCH $D_HEAD" "$E_BRANCH $E_HEAD"; do
  BR="${PAIR%% *}"; H="${PAIR#* }"
  printf '%s\n' "$LSR_ALL" | grep -q "^${H}[[:space:]]refs/heads/${BR}\$" || {
    echo "REFUSING: origin refs/heads/$BR is not $H — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
done
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
P430_NOW="$(ref_now "$P430_BRANCH")"; M733_NOW="$(ref_now "$M733_BRANCH")"
[ "$P430_NOW" = "$P430_SHA" ] || echo "NOTE: origin $P430_BRANCH is '${P430_NOW:-absent}', not 379b8b5 — the RD-430 ADDENDUM (if any) must name the current head (89)" >&2
[ "$M733_NOW" = "$M733_SHA" ] || echo "NOTE: origin $M733_BRANCH is '${M733_NOW:-absent}', not ed4c1bf — RD-733 moved or landed; re-read C-185's O-1 condition on M0" >&2
# 18b — main MAY move (ruling b). It must be 3b6c9ec or a descendant IN THE OBJECT STORE; a member already on it REFUSES; a member path moved REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 3b6c9ec — main was rewritten; re-brief" >&2; exit 18; }
if [ "$M_ORIGIN" != "$MAIN_SHA" ]; then
  for H in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
    if g merge-base --is-ancestor "$H" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: ${H:0:7} is already an ancestor of origin main ${M_ORIGIN:0:7} — a member merged before its gate; re-brief" >&2; exit 18; fi
  done
fi
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(comm -12 <(printf '%s\n' "$IM" "$R736" "$R418" "$R737" "$R385" "$LAW" "$R429" "$DIG" "$PKG" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d'))"
[ -z "$HIT" ] || { echo "REFUSING: main moved 3b6c9ec..${M_ORIGIN:0:7} and touched a member path: $HIT — re-brief (.dockerignore is RD-737's and RD-690's tier-1 premise)" >&2; exit 18; }
HITB="$(comm -12 <(printf '%s\n' "$LOCK" "$DKF" "$ICE" "$REVIEW" "$TS" "$R465" "$R549" | sort -u) <(printf '%s\n' "$MOVED" | sed '/^$/d') | tr '\n' ' ')"
[ -z "$HITB" ] || echo "NOTE: main's movement touches ${HITB}— the C-68 sets and node_modules proofs run on M0's blobs (brief ruling b)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 3b6c9ec) — the gate re-pins M0 itself and re-bases every prediction" >&2
ON_MAIN=''
g merge-base --is-ancestor "$M733_SHA" "$M_ORIGIN" 2>/dev/null && ON_MAIN="$ON_MAIN RD-733(ed4c1bf)"
g merge-base --is-ancestor "$P430_SHA" "$M_ORIGIN" 2>/dev/null && ON_MAIN="$ON_MAIN RD-430(379b8b5)"
[ -z "$ON_MAIN" ] || echo "NOTE: origin main carries:$ON_MAIN — the gate re-bases counts, census, C-185's set and C-68 populations on M0" >&2
[ "$(blob "$M_ORIGIN" "$TS")" = "$TS_BLOB" ] || echo "NOTE: origin main ${M_ORIGIN:0:7}'s test-server is not cff1e54 — RD-591 landed? H-23 applies whole" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — each delta is EXACTLY the commissioned file set; numstats as briefed.
chk_delta() { local from="$1" to="$2" want="$3" label="$4" got
  got="$(g diff --name-only "$from" "$to" 2>/dev/null | sort)"
  [ "$got" = "$(sorted "$want")" ] || { echo "REFUSING: $label delta is not the commissioned set. Got:" >&2; printf '%s\n' "$got" >&2; exit 22; }; }
chk_delta "$M707" "$A_HEAD" "$A_EXPECTED_FILES" "RD-736 (55333df..61e20ad)"
chk_delta "$M707" "$B_HEAD" "$B_EXPECTED_FILES" "RD-737 (55333df..88f3d11)"
chk_delta "$M707" "$C_HEAD" "$C_EXPECTED_FILES" "RD-708 (55333df..ed539e4)"
chk_delta "$M707" "$D_HEAD" "$D_EXPECTED_FILES" "RD-690 (55333df..b05b6ff)"
chk_delta "$M741" "$E_HEAD" "$E_EXPECTED_FILES" "RD-675 (5fd2398..12de511)"
ns() { g diff --numstat "$1" "$2" -- "$3" 2>/dev/null | cut -f1,2 | tr '\t' ' '; }
[ "$(ns "$M707" "$A_HEAD" "$IM")" = "27 7" ] && [ "$(ns "$M707" "$A_HEAD" "$R736")" = "74 0" ] || { echo "REFUSING: RD-736's numstats are not image-manifest +27/-7, rd736 +74" >&2; exit 22; }
[ "$(ns "$M707" "$B_HEAD" "$R418")" = "7 0" ] && [ "$(ns "$M707" "$B_HEAD" "$R737")" = "108 0" ] || { echo "REFUSING: RD-737's numstats are not rd418 +7, rd737 +108" >&2; exit 22; }
[ "$(ns "$M707" "$C_HEAD" "$R385")" = "27 0" ] || { echo "REFUSING: RD-708's numstat is not rd385 +27/-0" >&2; exit 22; }
[ "$(ns "$M707" "$D_HEAD" "$R385")" = "3 3" ] && [ "$(ns "$M707" "$D_HEAD" "$LAW")" = "2 2" ] || { echo "REFUSING: RD-690's numstats are not rd385 +3/-3, azureLogAnalytics +2/-2" >&2; exit 22; }
[ "$(ns "$M741" "$E_HEAD" "$R429")" = "29 3" ] || { echo "REFUSING: RD-675's numstat is not rd429 +29/-3" >&2; exit 22; }
# 22b — ruling (m): no member touches the lock or package.json (the registry exception does NOT carry).
for PAIR in "$M707 $A_HEAD" "$M707 $B_HEAD" "$M707 $C_HEAD" "$M707 $D_HEAD" "$M741 $E_HEAD"; do
  [ -z "$(g diff --name-only "${PAIR% *}" "${PAIR#* }" -- "$LOCK" "$PKG" 2>/dev/null)" ] || { echo "REFUSING: ${PAIR#* } changes package-lock.json/package.json — ruling (m) assumed no member does; re-brief" >&2; exit 22; }
done
for PAIR in "$M707 $A_HEAD" "$M707 $B_HEAD" "$M707 $C_HEAD" "$M741 $E_HEAD"; do
  [ -z "$(g diff --name-only "${PAIR% *}" "${PAIR#* }" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" ] || { echo "REFUSING: ${PAIR#* } touches a product/image path — commissioned as test code only" >&2; exit 22; }
done
[ "$(g diff --name-only "$M707" "$D_HEAD" -- backend static docs Dockerfile .dockerignore .github 2>/dev/null)" = "$LAW" ] || { echo "REFUSING: RD-690 touches a product path beyond $LAW" >&2; exit 22; }

# 93 — RD-736's premises at source.
[ "$(blob "$M707" "$IM")" = "$IM_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$IM")" = "$IM_M_BLOB" ] && [ "$(blob "$FAE" "$IM")" = "$IM_M_BLOB" ] && [ "$(blob "$A_HEAD" "$IM")" = "$IM_A_BLOB" ] && [ "$(blob "$A_FIX" "$IM")" = "$IM_A_BLOB" ] \
  && [ "$(blob "$A_HEAD" "$R736")" = "$R736_BLOB" ] || { echo "REFUSING: RD-736's blobs are not image-manifest 23bfa4f -> 2040ca2 / rd736 6978d32" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$IM" 'function unwidenRuns(text, { keepLE = false } = {}) {')" = "1" ] && [ "$(cnt "$MAIN_SHA" "$IM" 'keepLE')" = "0" ] \
  && [ "$(cnt "$A_HEAD" "$IM" 'function scannableText(relPath, content, opts) {')" = "1" ] && [ "$(cnt "$A_HEAD" "$IM" "add(scannableText(relPath, content, { keepLE: true }));")" = "1" ] \
  || { echo "REFUSING: RD-736's keepLE / scannableText / scanReadings shape is not as briefed" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$R736" "describe('RD-736 B-F1")" = "1" ] && [ "$(cnt "$A_HEAD" "$R736" "describe('RD-736 B-F2")" = "1" ] && [ "$(cnt "$A_HEAD" "$R736" "test('CONTROL: ")" = "4" ] \
  || { echo "REFUSING: rd736's B-F1 / B-F2 describes or its 4 CONTROLS are not as briefed" >&2; exit 93; }
[ "$(g grep -l -E "require\([^)]*image-manifest" "$MAIN_SHA" -- __tests__ 2>/dev/null | grep -c .)" = "12" ] && [ "$(g grep -l -E "require\([^)]*image-manifest" "$A_HEAD" -- __tests__ 2>/dev/null | grep -c .)" = "13" ] \
  || { echo "REFUSING: the image-manifest requirer count is not 12 at M0 / 13 at RD-736's head (a7's premise)" >&2; exit 93; }

# 94 — RD-737's premises at source.
for S in "$M707" "$MAIN_SHA" "$B_HEAD" "$A_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] || { echo "REFUSING: .dockerignore at ${S:0:7} is not 3e45ec5 (the tier-1 image legs' premise)" >&2; exit 94; }
  [ "$(blob "$S" "$DKF")" = "$DKF_BLOB" ] || { echo "REFUSING: Dockerfile at ${S:0:7} is not 12aab55" >&2; exit 94; }
done
[ "$(blob "$M707" "$R418")" = "$R418_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R418")" = "$R418_M_BLOB" ] && [ "$(blob "$B_HEAD" "$R418")" = "$R418_B_BLOB" ] && [ "$(blob "$B_HEAD" "$R737")" = "$R737_BLOB" ] \
  || { echo "REFUSING: RD-737's blobs are not rd418 b72f8c9 -> 2f0d1a4 / rd737 25c9986" >&2; exit 94; }
[ "$(diff <(titles "$M707" "$R418") <(titles "$B_HEAD" "$R418") >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: rd418's title set changed at RD-737 (commissioned: list entries only)" >&2; exit 94; }
[ "$(g show "${B_HEAD}:${R737}" 2>/dev/null | grep -cE "^[[:space:]]+'\*\*/\*\.[^']*': 'backend/[^']*',$")" = "20" ] || { echo "REFUSING: rd737's RD707_PLANTS map is not 20 entries" >&2; exit 94; }
DIG_ADDED="$(g diff "$FAE" "$M707" -- "$DIG" 2>/dev/null | grep -E '^\+[^+#]' | grep -c .)"
[ "$DIG_ADDED" = "20" ] || { echo "REFUSING: RD-707 did not add exactly 20 .dockerignore rule lines fae2aa1..55333df (got $DIG_ADDED; WRONG 5's premise)" >&2; exit 94; }
while IFS= read -r RULE; do
  [ -n "$RULE" ] || continue
  g show "${MAIN_SHA}:${DIG}" 2>/dev/null | grep -qxF -- "$RULE" || { echo "REFUSING: RD-707 rule '$RULE' is not in M0's .dockerignore" >&2; exit 94; }
done < <(g show "${B_HEAD}:${R737}" 2>/dev/null | sed -nE "s/^[[:space:]]+'(\*\*\/\*\.[^']*)': 'backend\/[^']*',$/\1/p")
[ "$(cnt "$B_HEAD" "$R737" "test('census: exactly the 16 key-suffix rules")" = "1" ] && [ "$(cnt "$B_HEAD" "$R737" "test('no TRACKED file is excluded only by a key-suffix rule")" = "1" ] \
  || { echo "REFUSING: rd737's C-N1 census / guard titles are not as briefed" >&2; exit 94; }

# 95 — RD-708's premises at source.
[ "$(blob "$M707" "$R385")" = "$R385_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R385")" = "$R385_M_BLOB" ] && [ "$(blob "$C_HEAD" "$R385")" = "$R385_C_BLOB" ] && [ "$(blob "$C_FIX" "$R385")" = "$R385_C_BLOB" ] \
  || { echo "REFUSING: rd385 is not d1b26f3 (55333df, M0) -> 401e31d (RD-708)" >&2; exit 95; }
[ "$(cnt "$MAIN_SHA" "$R385" 'staleReviewed')" = "0" ] && [ "$(cnt "$C_HEAD" "$R385" 'const staleReviewed = (files, readFile = read) => {')" = "1" ] \
  && [ "$(cnt "$C_HEAD" "$R385" "test('STALE GUARD: every REVIEWED entry still matches a live finding")" = "1" ] && [ "$(cnt "$C_HEAD" "$R385" "test('ARM (RD-708) — ")" = "2" ] \
  || { echo "REFUSING: RD-708's staleReviewed / STALE GUARD / two ARMs are not new at ed539e4 as briefed" >&2; exit 95; }
[ "$(diff <(titles "$M707" "$R385") <(titles "$C_HEAD" "$R385" | grep -vF 'RD-708') >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: RD-708 changes an existing rd385 title" >&2; exit 95; }
grep -qF 'PRIOR WORK (C-49)' "$READY_C" && grep -qF "ADDENDUM: RD-708 READY" "$READY_C" || { echo "REFUSING: RD-708's READY file does not carry its PRIOR WORK ADDENDUM" >&2; exit 95; }

# 96 — RD-690's premises at source (the prefix VALUES are never read or printed by this launcher).
[ "$(blob "$M707" "$LAW")" = "$LAW_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$LAW")" = "$LAW_M_BLOB" ] && [ "$(blob "$D_HEAD" "$LAW")" = "$LAW_D_BLOB" ] && [ "$(blob "$D_HEAD" "$R385")" = "$R385_D_BLOB" ] \
  || { echo "REFUSING: RD-690's blobs are not azureLogAnalytics 036c34f -> ffdc003 / rd385 d1b26f3 -> 5818189" >&2; exit 96; }
LAWDIFF="$(g diff -U0 "$M707" "$D_HEAD" -- "$LAW" 2>/dev/null | grep -E '^[-+][^-+]')"
[ "$(printf '%s\n' "$LAWDIFF" | grep -c .)" = "4" ] && [ "$(printf '%s\n' "$LAWDIFF" | grep -cvE '^[-+][[:space:]]*(//|\*)')" = "0" ] \
  || { echo "REFUSING: RD-690's azureLogAnalytics change is not exactly 2 comment lines out / 2 in (d1's premise)" >&2; exit 96; }
[ "$(cnt "$MAIN_SHA" "$R385" "ticket: 'RD-690'")" = "1" ] && [ "$(cnt "$D_HEAD" "$R385" "ticket: 'RD-690'")" = "0" ] \
  && [ "$(cnt "$D_HEAD" "$R385" ".map(r => r.ticket)).toEqual([]);")" = "1" ] && [ "$(cnt "$MAIN_SHA" "$R385" ".map(r => r.ticket)).toEqual(['RD-690']);")" = "1" ] \
  || { echo "REFUSING: RD-690's REVIEWED entry removal / CONTROL [] are not as briefed" >&2; exit 96; }
[ "$(diff <(titles "$M707" "$R385") <(titles "$D_HEAD" "$R385") >/dev/null 2>&1; echo $?)" = "0" ] || { echo "REFUSING: RD-690 changes an rd385 title" >&2; exit 96; }

# 97 — RD-675's premises at source.
[ "$(blob "$M741" "$R429")" = "$R429_M_BLOB" ] && [ "$(blob "$MAIN_SHA" "$R429")" = "$R429_M_BLOB" ] && [ "$(blob "$E_HEAD" "$R429")" = "$R429_E_BLOB" ] \
  || { echo "REFUSING: rd429 is not 7544939 (5fd2398, M0) -> d38e28f (RD-675)" >&2; exit 97; }
[ "$(cnt "$E_HEAD" "$R429" "'.bat', '.cmd', '.htm',")" = "1" ] && [ "$(cnt "$MAIN_SHA" "$R429" "'.bat'")" = "0" ] \
  && [ "$(cnt "$E_HEAD" "$R429" 'const refusesNul = (rel, bytes) =>')" = "1" ] && [ "$(cnt "$E_HEAD" "$R429" "describe('RD-675 — ")" = "1" ] \
  || { echo "REFUSING: RD-675's TEXT_EXTENSIONS / refusesNul / describe are not as briefed" >&2; exit 97; }
TRK_BAN="$(g ls-tree -r -z --name-only "$MAIN_SHA" 2>/dev/null | tr '\0' '\n' | grep -ciE '\.(bat|cmd|htm)$')"
TRK_PS1="$(g ls-tree -r -z --name-only "$MAIN_SHA" 2>/dev/null | tr '\0' '\n' | grep -ciE '\.ps1$')"
[ "$TRK_BAN" = "0" ] && [ "$TRK_PS1" = "6" ] || { echo "REFUSING: tracked .bat/.cmd/.htm at M0 is '$TRK_BAN' (not 0) or the .ps1 control is '$TRK_PS1' (not 6) — e2's premise" >&2; exit 97; }

# 98 — shared blobs: ICE, the review fixture and test-server identical everywhere (rulings e, a6, H-23).
for S in "$M707" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do
  [ "$(blob "$S" "$ICE")" = "$ICE_BLOB" ] && [ "$(blob "$S" "$REVIEW")" = "$REVIEW_BLOB" ] && [ "$(blob "$S" "$TS")" = "$TS_BLOB" ] \
    || { echo "REFUSING: image-content-exposure / image-carrier-review / test-server at ${S:0:7} are not 7e3262b / 7ec5910 / cff1e54" >&2; exit 98; }
done

# 23 — EXPECTED OVERLAPS by each member's own delta: the counts file only, plus C x D on rd385 (the commission's coupling).
declare_delta() { g diff --name-only "$1" "$2" 2>/dev/null | grep -vxF "$COUNTS_FILE" | sort; }
OV=''
LIST="A:$M707:$A_HEAD B:$M707:$B_HEAD C:$M707:$C_HEAD D:$M707:$D_HEAD E:$M741:$E_HEAD"
for I in $LIST; do for J in $LIST; do
  [ "${I%%:*}" \< "${J%%:*}" ] || continue
  IB="${I#*:}"; JB="${J#*:}"
  SH="$(comm -12 <(declare_delta "${IB%%:*}" "${IB#*:}") <(declare_delta "${JB%%:*}" "${JB#*:}") | tr '\n' ' ' | sed 's/ $//')"
  [ -z "$SH" ] || OV="$OV ${I%%:*}${J%%:*}='$SH'"
done; done
[ "$OV" = " CD='$R385'" ] || { echo "REFUSING: path overlaps are not as briefed (counts file + C x D on rd385 only):${OV:- none}" >&2; exit 23; }

# 35 — counts at every pinned sha; __tests__ census at M0 and the heads.
for PAIR in "$FAE 4230 255" "$M707 4231 255" "$M741 4231 255" "$MAIN_SHA 4236 256" "$A_FIX 4230 255" "$A_MRG 4231 255" "$A_HEAD 4242 256" \
            "$B_FIX 4231 255" "$B_HEAD 4256 256" "$C_FIX 4231 255" "$C_HEAD 4234 255" "$D_HEAD 4231 255" "$E_FIX 4231 255" "$E_HEAD 4238 255"; do
  S="${PAIR%% *}"; WANT="${PAIR#* }"
  CT="$(counts_at "$S")"
  [ "$CT" = "$WANT" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '${CT:-unreadable}', not '$WANT'" >&2; exit 35; }
done
[ "$(ntests "$MAIN_SHA")" = "299" ] && [ "$(ntests "$A_HEAD")" = "299" ] && [ "$(ntests "$B_HEAD")" = "299" ] && [ "$(ntests "$C_HEAD")" = "298" ] && [ "$(ntests "$D_HEAD")" = "298" ] && [ "$(ntests "$E_HEAD")" = "298" ] \
  || { echo "REFUSING: the __tests__ census is not 299 / 299 / 299 / 298 / 298 / 298 (M0, A, B, C, D, E)" >&2; exit 35; }

# 70 — package-lock: two blobs in play, exactly where the brief says; package.json identical.
for S in "$M707" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_OLD_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not f74a4e8" >&2; exit 70; }; done
for S in "$M741" "$MAIN_SHA" "$E_HEAD"; do [ "$(blob "$S" "$LOCK")" = "$LOCK_M_BLOB" ] || { echo "REFUSING: package-lock at ${S:0:7} is not e9063d4" >&2; exit 70; }; done
for S in "$M707" "$M741" "$MAIN_SHA" "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD"; do [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] || { echo "REFUSING: package.json at ${S:0:7} is not cdb1168" >&2; exit 70; }; done
[ "$(blob "$M_ORIGIN" "$LOCK")" = "$LOCK_M_BLOB" ] || echo "NOTE: package-lock on origin main ${M_ORIGIN:0:7} is not e9063d4 — a third lock is in play; prove node_modules before any run (H-31)" >&2
# 70b — H-31's premise: the local npm cache holds the tarballs the two locks need (a NOTE only — the gate decides and names an ENOTCACHED).
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in axios/-/axios-1.20.0.tgz axios/-/axios-1.18.0.tgz http-cache-semantics/-/http-cache-semantics-4.3.0.tgz brace-expansion/-/brace-expansion-2.1.7.tgz brace-expansion/-/brace-expansion-1.1.21.tgz ip-address/-/ip-address-10.7.2.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE for its lock" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi

# 80 — the merge premise by the READ-ONLY three-argument merge-tree (no objects written anywhere): each pair counts-only or clean; C x D clean.
HEADS="$A_HEAD $B_HEAD $C_HEAD $D_HEAD $E_HEAD"
MT_PAIRS=0
for X in $M_ORIGIN $HEADS; do for Y in $HEADS; do
  [ "$X" \< "$Y" ] || [ "$X" = "$M_ORIGIN" ] || continue
  [ "$X" = "$Y" ] && continue
  if g merge-base --is-ancestor "$Y" "$X" 2>/dev/null || g merge-base --is-ancestor "$X" "$Y" 2>/dev/null; then continue; fi
  CONF="$(conflicts "$X" "$Y" | tr '\n' ' ' | sed 's/ $//')"
  MT_PAIRS=$((MT_PAIRS + 1))
  [ -z "$CONF" ] || [ "$CONF" = "$COUNTS_FILE" ] || { echo "REFUSING: merge-tree ${X:0:7} x ${Y:0:7} carries conflict markers in '${CONF}' — not counts-only (80)" >&2; exit 80; }
done; done
[ -z "$(conflicts "$C_HEAD" "$D_HEAD")" ] || { echo "REFUSING: RD-708 x RD-690 is not a clean merge (the COMBINED rd385 premise)" >&2; exit 80; }

# 31 — builder evidence, prior reports, gate 13's instruments, standing references and tools on disk.
for f in "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$CLAR" "$PREV_B10" "$PREV_B4" "$BRIEF13" "$B12_REPORT" "$C133" \
         "$EV_O/rd736-red.log" "$EV_O/rd736-green.log" "$EV_O/rd736-tracked-diff.js" "$EV_O/rd737-hold.log" "$EV_O/rd708-hold.log" "$EV_O/rd690-hold.log" "$EV_O/rd675-hold.log" \
         "$EV_O/rd736-green-hold.sh" "$EV_O/rd737-hold.sh" "$EV_O/rd708-hold.sh" "$EV_O/rd690-hold.sh" "$EV_O/rd675-hold.sh" \
         "$NX/session-tools/s86o/rd737-cn1-measure.txt" "$NX/session-tools/s84o/rd418-build.sh" "$NX/session-tools/nexusai-lock.sh" \
         "$B13_INST/HOLD13.sh" "$B13_INST/qa-holdlib13.sh" "$B13_INST/qa-floorlib13.sh" "$B13_INST/qa-floorcount.py" "$B13_INST/qa-to.sh" "$B13_INST/qa-jestwrap.sh" "$B13_INST/qa-jsum.js" \
         "$B13_INST/qa-runj13.sh" "$B13_INST/qa-mut13.py" "$B13_INST/qa-mutlib13.sh" "$B13_INST/qa-merge13.sh" "$B13_INST/qa-mt13.sh" "$B13_INST/qa-pin13.sh" "$B13_INST/qa-build13.sh" \
         "$B13_INST/qa-h1-selftest13.sh" "$B13_INST/qa-h1-scan.py" "$B13_INST/qa-mail.py" "$B13_INST/qa-mailread.py" "$B13_INST/qa-lockcheck.py" "$B13_INST/qa-ssprint.sh" \
         "$B13_INST/qa-netbelt.sb" "$B13_INST/qa-netbelt-nodns.sb" "$B13_INST/qa-netbelt-ctl.js" "$B13_INST/qa-blobcensus13.py" "$B13_INST/qa-titles13.py" "$B13_INST/qa-lost13.py" \
         "$B13_INST/qa-c57-id-superset.sh" "$B13_INST/qa-c68census.py" "$B13_INST/qa-cov-setup.js" "$B13_INST/qa-b7tok.js" \
         "$G7R1_FLOOR" "$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "${A_HEAD:0:7}" "$READY_A" && grep -qF "${B_HEAD:0:7}" "$READY_B" && grep -qF "${C_HEAD:0:7}" "$READY_C" && grep -qF "${D_HEAD:0:7}" "$READY_D" && grep -qF "${E_HEAD:0:7}" "$READY_E" \
  || { echo "REFUSING: a READY (RD-736/737/708/690/675) does not name its head" >&2; exit 31; }
grep -qF 'VERDICT: PASS — 4242/4242 tests passed across 256 suites (jest exit 0)' "$EV_O/rd736-green.log" && grep -qF 'Tests:       5 failed, 6 passed, 11 total' "$EV_O/rd736-red.log" \
  && grep -qF 'VERDICT: PASS — 4256/4256 tests passed across 256 suites (jest exit 0)' "$EV_O/rd737-hold.log" && grep -qF 'Tests:       414 passed, 414 total' "$EV_O/rd737-hold.log" \
  && grep -qF 'VERDICT: PASS — 4234/4234 tests passed across 255 suites (jest exit 0)' "$EV_O/rd708-hold.log" && grep -qF 'Tests:       3 failed, 51 passed, 54 total' "$EV_O/rd708-hold.log" \
  && grep -qF 'VERDICT: PASS — 4231/4231 tests passed across 255 suites (jest exit 0)' "$EV_O/rd690-hold.log" && grep -qF 'Tests:       3 failed, 48 passed, 51 total' "$EV_O/rd690-hold.log" \
  && grep -qF 'VERDICT: PASS — 4238/4238 tests passed across 255 suites (jest exit 0)' "$EV_O/rd675-hold.log" && grep -qF 'Tests:       3 failed, 22 passed, 25 total' "$EV_O/rd675-hold.log" \
  && grep -qF '=== HEAD 9b26b36' "$EV_O/rd736-green.log" && grep -qF '=== HEAD e447230' "$EV_O/rd737-hold.log" && grep -qF '=== HEAD 01aa919' "$EV_O/rd708-hold.log" \
  && grep -qF '=== HEAD b05b6ff' "$EV_O/rd690-hold.log" && grep -qF '=== HEAD ce89bb2' "$EV_O/rd675-hold.log" \
  || { echo "REFUSING: a builder log no longer carries the result or HEAD line the brief quotes (WRONG 6's premise)" >&2; exit 31; }
grep -qF 'RESUME METHOD NOTE' "$B12_REPORT" && grep -qF 'File **one focused hold at a time** (≤~40 min of jest)' "$B12_REPORT" || { echo "REFUSING: gate 12's report no longer carries the RESUME METHOD NOTE the brief quotes (ruling j)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-32659\}' "$B13_INST/qa-floorlib13.sh" || echo "NOTE: gate 13's qa-floorlib13.sh ROOT default is no longer 32659 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | Tuesday' "$BRIEF13" || echo "NOTE: gate 13's brief does not read as stamped by Tuesday — the brief calls it the stamped base" >&2

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
for P in "$PREV_B10" "$PREV_B4" "$BRIEF13" "$B12_REPORT" "$READY_A" "$READY_B" "$READY_C" "$READY_D" "$READY_E" "$B13_INST/"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tiers, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-736, RD-708 and RD-675 are TIER 2 (through-code). RD-737 and RD-690 are TIER 1' 'No member has a browser leg' 'NO docker, NO image build' 'One verdict PER ticket' 'No priority member' 'NO NPM REGISTRY EXCEPTION'; do
  grep -qF "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-736 (TIER 2, test helper' 'RD-737 (TIER 1, image content, test code' 'RD-708 (TIER 2, test code' 'RD-690 (TIER 1, shipped comments' 'RD-675 (TIER 2, test code' 'one verdict per ticket' 'manifest evaluation, NO image built'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$B_HEAD" "$C_HEAD" "$D_HEAD" "$E_HEAD" "$MAIN_SHA" "$M707" "$M741" "$FAE" "$A_FIX" "$A_MRG" "$B_FIX" "$C_FIX" "$E_FIX"; do
  grep -qF -- "$S" "$BRIEF" || grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$LOCK_OLD_BLOB" "$LOCK_M_BLOB" "$PKG_BLOB" "$IM_M_BLOB" "$IM_A_BLOB" "$R736_BLOB" "$R418_M_BLOB" "$R418_B_BLOB" "$R737_BLOB" "$R385_M_BLOB" "$R385_C_BLOB" "$R385_D_BLOB" "$R385_CD_BLOB" \
         "$LAW_M_BLOB" "$LAW_D_BLOB" "$R429_M_BLOB" "$R429_E_BLOB" "$DIG_BLOB" "$DKF_BLOB" "$ICE_BLOB" "$REVIEW_BLOB" "$TS_BLOB"; do
  grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name ${S:0:7}" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
if grep -qF 'EARLY VERDICT — batch 14' "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF 'EARLY VERDICT'; then echo "REFUSING: an EARLY VERDICT route is carried — batch 14 has no priority member" >&2; exit 15; fi
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
WORDS="RD-736 RD-737 RD-708 RD-690 RD-675 RD-430 RD-733 RD-707 RD-741 RD-689 C-17 C-49 C-57 C-68 C-89 C-102 C-104 C-112 C-115 C-125 C-141 ADDENDUM%5 C-167 C-173 C-174 C-185 C-186 C-190 C-192 C-194
RED-AT-PARENT a0 b0 b1 b2 b4 c0 d0 d1 d2 d3 e0 e2 e3 y1 y2 MTa MTb MTc MTd MT1 M0 B-F1 B-F2 C-F1 C-N1 M-noLE M-latin M-display M-stale M-back M-oldlist keepLE
L-A1 L-A4 L-B1 L-B5 L-C1 L-C4 L-D1 L-D4 L-E1 L-E4 L-Y1 H-1 H-3 H-9 H-15 H-20 H-21 H-22 H-24 H-25 H-26 H-27 H-28 H-29 H-31 H-32 H-33 --forceExit trap%on%EXIT deadline LANDING%CONTROL
4282/258 4247/257 4272/258 4275/258 4242/256 4256/256 4234/255 4231/255 4238/255 9d3329e COMBINED rd385 image-manifest manifest%evaluation NO%image%built IN%MEMORY%ONLY tracked%api.key.js
exits%71 SCRATCH%object%dir reverse%order git%clone%--shared REGENERATION id-superset pull%request missing%0 new%ids%46 stale-parent
POSITIVE%CONTROL%FIRST node%--check VOID EXCLUSIVE qa-b14- qa-b13- qa-b12- MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER --after UNCHANGED%tag DEADLINE HEARTBEAT PEER%gate
2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child
Prior%work PRIOR%WORK FOREGROUND never%push NEVER%merge Partner%Center batch%10 batch%4 gate%12 gate%13 npm%install --offline ENOTCACHED HOLD13.sh qa-floorlib13.sh Never%rm"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 3a. INSTRUMENT RULES' \
         '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 4. TARGET A' '^## 5. TARGET B' '^## 6. TARGET C' '^## 7. TARGET D' '^## 8. TARGET E' '^## 9. THE MERGED TREE' '^## 10. CI' '^## 11. Floor discipline' \
         '^## 12. HELD' '^## 13. Output' '^## ADDENDUM SLOT' '^## WRONG OR UNVERIFIED' '^## PROVENANCE' '^### MERGE ORDER' '^### TARGET A' '^### TARGET B' '^### TARGET C' '^### TARGET D' '^### TARGET E' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for L in L-A1 L-A2 L-A3 L-A4 L-B1 L-B2 L-B3 L-B4 L-B5 L-C1 L-C2 L-C3 L-C4 L-D1 L-D2 L-D3 L-D4 L-E1 L-E2 L-E3 L-E4 L-Y1; do
  grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }
done
for R in a0 a8 b0 b8 c0 c8 d0 d8 e0 e7 y1 y5; do
  grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }
done
# every builder's stated limits / coupling lines carried verbatim (each line checked in the READY AND the brief).
while IFS= read -r PAIR; do
  [ -n "$PAIR" ] || continue
  case "${PAIR%%|*}" in A) F="$READY_A" ;; B) F="$READY_B" ;; C) F="$READY_C" ;; D) F="$READY_D" ;; E) F="$READY_E" ;; *) echo "REFUSING: bad verbatim-table row" >&2; exit 19 ;; esac
  T="${PAIR#*|}"
  grep -qF -- "$T" "$F" || { echo "REFUSING: '$T' is no longer in $F — the READY changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
A|Display text is NOT changed, so r5's 28 readability regressions (BOUNDARY/TRAIL) remain as ruled under (a). This fixes the gates' VERDICT, not the reading.
A|RD-703's endianness-switch-inside-one-run residue is unchanged.
B|The guard covers TRACKED files only (an untracked api.key.js in a build context is still excluded, the safe direction).
B|A key backup with a suffix outside the allow-list that is ALSO a tracked file would fail the guard. That is intended, and loud.
B|The plants mirror shapes; this does not add them to the real-build plant script (session-tools/s84o/rd418-build.sh). That is the gate's leg.
C|SCOPE NOTE: the ticket's fix shape named only "file stops shipping".
C|once this lands, RD-689 (lane 1, the VM-address comments in server.js and healthSweeperScheduler.js) must delete its 5 REVIEWED entries in the same change, or the stale guard goes red.
D|Image leg: the image's file SET is unchanged; one shipped file's bytes change (2 comment lines). A real-image diff should show exactly that.
D|With RD-708's stale guard on main, this entry removal is REQUIRED, not optional.
E|No reason is recorded for .ps1 specifically.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
Shipped documents carry no internal identifiers or named individuals.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
a FAILED ls-remote is UNKNOWN, never a value.
absence of a port clash is NOT evidence of a quiet floor.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
O-1 counts as known ONLY while its failure is
counts as known ONLY when the received object differs from the expected in `envReached` alone
Both O-1 cells LEAVE the set when RD-733 merges.
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
condition (2) is decided on BLOBS, and commit lists are evidence only
No re-run is used as a clearance
THE TURN PASSES
Addendum 2's "once PER WAITING GATE TICKET" means once per gate TAG.
content-keyed reviewed list that never stores a value
deferred to the next lane-3 round, behind the frozen lane-3 branches.
That is a false reopen, never a false pass
RD-736 extends the same shape, in the same direction
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b14-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' \
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
for w in 'RED-AT-PARENT' 'missing 0' 'C-190' 'NEVER opens, comments on, approves or merges a PR' '4282/258' 'RE-BASE EVERY PREDICTION' 'H-20' 'H-21' 'H-22' 'H-23' 'H-24' 'H-25' 'H-26' \
         'NEVER merges and never pushes' 'CodeQL is NOT RUN at any member head' 'THREE-ARGUMENT' 'Blocker' 'setuid' 'pgrep' '`END ok`' 'exits 71' 'ARRAY option' '=====' 'UNKNOWN, never a value' \
         'COMBINED' '9d3329e' 'stale-parent' 'f74a4e8' 'e9063d4' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' 'manifest evaluation' 'NO image built' 'shippedFiles' \
         'keepLE' 'M-noLE' 'M-latin' 'M-display' 'r5b' 'C-194' 'drop-one' 'exactly ONE rule' 'api.key.js' 'M-stale' 'M-noop' 'RD-689' 'M-back' 'IN MEMORY' 'never printed' 'comment-aware' \
         'M-oldlist' 'TRACKED' 'UTF-16LE' 'rmSync' 'C-173' 'ADDENDUM 5' 'qa-floorlib13.sh' 'HOLD13.sh' 'ADDENDUM SLOT' 'RD-430 SLOT' '37223845397' 'WRONG 1' 'WRONG 3'; do
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
  R430_STATE="RD-430 JOINS this gate per the brief's ADDENDUM SLOT, at $R430_SHA (origin $P430_BRANCH, re-pinned by the launcher), READY $R430_READY — gate it as the ADDENDUM paragraph says, merge it LAST (step f)."
else
  [ "$R430_EMPTY" = "1" ] || { echo "REFUSING: the RD-430 ADDENDUM SLOT is neither EMPTY nor one well-formed JOINS line (89)" >&2; exit 89; }
  R430_STATE="RD-430 is NOT a member of this gate (the brief's ADDENDUM SLOT is EMPTY): do not gate it; say so in the report."
fi

# 41 — the jest queue as the launch finds it (MERGES GO FIRST): a NOTE for every merge-tagged / peer-gate ticket (read-only ls/grep).
if [ -d "$LOCKQ" ]; then
  MQ="$(grep -l -i 'merge' "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in the jest queue now — the gate files behind them (brief §11 clause 1)" >&2
  for TAG in qa-b12- qa-b13-; do
    BQ="$(grep -l "$TAG" "$LOCKQ"/* 2>/dev/null | wc -l | tr -d ' ')"
    [ "${BQ:-0}" = "0" ] || echo "NOTE: $BQ peer-gate ($TAG) ticket(s) in the jest queue now — a PEER gate: FIFO, never touched" >&2
  done
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
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P wednesday; do
  PP="$(pane_pid_of "$NAME")"
  [ "$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: expected exactly one tmux pane named '$NAME', found: '${PP:-none}' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
done
NEG_SEATS="${NEG_SEATS# }"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "5" ] || { echo "REFUSING: the five derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }
# the peer gates' own claudes, if their panes are live: extra negative controls (a NOTE when absent — a peer may have finished).
for PEER in "$ROUTE_NAME12" "$ROUTE_NAME13"; do
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER, a live peer gate);"
  else
    echo "NOTE: no live claude under a pane named $PEER — that peer gate finished or its pane is gone" >&2
  fi
done

# 86 — no live gate-14 session already exists: a pane named QA/NexusAI-batch14 with a claude under it REFUSES (two sessions, one report).
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 14 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note, no placeholder) and the answer route (Tuesday adds it, never this launcher).
# Both are checked and every missing item printed, so --check shows them all; the route's absence exits 40, else a stamp placeholder exits 32.
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ]; then
  echo "guards pass (9 6 7 8 18 18b 22 22b 93 94 95 96 97 98 23 35 70 70b 80 31 83 39 10 17 11 12 13 14 15 20 82 19 24 53 71 76 77 78 79 81 89 41 38R 86); stamp and/or route NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); three-argument merge-trees checked: $MT_PAIRS; origin main ${M_ORIGIN:0:7}; on main:${ON_MAIN:- none}" >&2
  echo "  member pins (origin, re-read now): RD-736 $A_HEAD · RD-737 $B_HEAD · RD-708 $C_HEAD · RD-690 $D_HEAD · RD-675 $E_HEAD" >&2
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
  echo "  origin: 5 member branches at their pins at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192): RD-736 ${A_HEAD:0:7} RD-737 ${B_HEAD:0:7} RD-708 ${C_HEAD:0:7} RD-690 ${D_HEAD:0:7} RD-675 ${E_HEAD:0:7}"
  echo "  main ${M_ORIGIN:0:7} (3b6c9ec or a descendant; no member path moved) (18b); on main:${ON_MAIN:- none}; RD-430 ${P430_NOW:0:7} RD-733 ${M733_NOW:0:7}"
  echo "  merge-bases (7); chains (8); deltas + no lock change (22, 22b); premises RD-736 (93) RD-737 (94) RD-708 (95) RD-690 (96) RD-675 (97) shared (98)"
  echo "  overlaps (23); counts + census (35); locks + npm cache (70, 70b); $MT_PAIRS three-argument merge-trees counts-only or clean (80); evidence (31); C-133 script (83)"
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

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/$B_BRANCH = $B_HEAD; refs/heads/$C_BRANCH = $C_HEAD; refs/heads/$D_BRANCH = $D_HEAD; refs/heads/$E_BRANCH = $E_HEAD; refs/heads/$P430_BRANCH = ${P430_NOW:-absent}; refs/heads/$M733_BRANCH = ${M733_NOW:-absent}; refs/heads/main = $M_ORIGIN (3b6c9ec or a descendant; no member path moved since 3b6c9ec; already on it:${ON_MAIN:- none}). $MT_PAIRS three-argument merge-trees (read-only, no objects written) were counts-only or clean across main and every member pair; RD-708 x RD-690 is clean (the COMBINED rd385). These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
$R430_STATE
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS:$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model claude-opus-5-5 "$PROMPT"
