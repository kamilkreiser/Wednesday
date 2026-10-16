#!/bin/bash
# launch_qa_nexusai_gate_batch23.sh — cross-project QA agent, ONE gate on Datasec/NexusAI ("batch 23"), ONE member, one verdict, ONE report
# (drafted 2026-10-16 ~12:10–~12:30 AEDT by a read-only drafting agent for Tuesday; the drafter ran only bash -n and --check).
# A FRESH gate (not a resume) on a NEW MACHINE (Mac mini, /Volumes/Laptop-DEV; the T9 is ALSO mounted). TIER 1.
#   A — RD-846 (TIER 1; the shipped build / image) rd-846-acr-build-s99o @ 3a45914: ONE commit on main 3907c57, Dockerfile ONLY (+8/-2):
#       the production stage stops re-copying package.json + package-lock.json (an EMPTY layer under a naive-diff builder; ACR failed the next COPY).
#   No other member, no slots. The base IS origin main 3907c57 (counts 4506/283; lock 19477a9).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-batch23' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate_batch23.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-23 drafting commission (2026-10-16). READY copied into briefs/ at stamp. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED). The installed jest/docker-lock tool is RD-821 r3 (sha256 3c33f5ae…), default base on the T9 (RD-847).
# FINDINGS-ONLY: never merges (outside its own clones), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never swaps
# the lock tool; no fix, no deploy, nothing to Partner Center/demo/prod/any human. DOCKER: own qa-b23-* daemons/containers only (H-35), Docker Hub +
# the image's own npm ci inside builds only (T2). AZURE: only Tuesday's T1 (a) — at most ONE `az acr build` to nexusai:gate23-3a45914 in nexusaidevacrfa39.
#
# PATTERN: launch_qa_nexusai_gate_batch22.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules,
# the LIVE negative-control seat derivation 38R, route-line and stamp guards last). CHANGES, each deliberate:
#   - ONE member on main itself (no merge-base stack, no member pairs, no merge-tree guard 80, no ADDENDUM SLOTS guard 89, no browser, no RD-640 instruments).
#   - EVERY PATH re-based from /Volumes/KK_T9_External_HDD to /Volumes/Laptop-DEV (TUESDAY, the NexusAI project, Testing Agent MAIN, the cockpit,
#     the AgentMail .env) EXCEPT three that exist ONLY on the T9 and are READ there: the LIVE lock base (the tool's own default, RD-847), gate 22's
#     instruments/report (this drive's Testing Agent MAIN stops at 2026-09-16), gate 20's answer-starvation.txt.
#   - 90: the installed tool pinned at 3c33f5ae…, its default base must name the T9 AND the T9 base must be present; both queue kinds read;
#         NEXUSAI_LOCK_BASE is UNSET before exec (a NOTE if it was set).
#   - 22/93: the delta is Dockerfile only and its ONLY non-comment change is the one removed production-stage COPY; line pins; the health formula
#         computed here from the head sha (printf %s | shasum) and required in the brief.
#   - 70D: the docker daemon must answer; azure-cli 2.90.0's own packer present; docker:27-dind / builder containers / NexusAI's az profile NOTEd.
#   - 38R: the coordinator + at least ONE Datasec/NexusAI-* builder seat (the floor is O alone today); fleet-monitor added as a negative control if a claude runs under it.
#   - MODEL: read from Tuesday's 0_Brain/dashboard/data/models_latest.json (levels.opus.model_id) and REFUSED unless it is the brief's claude-opus-5-5.
#   - READY path overridable by QA_READY_OVERRIDE (the drafter's --check only; Tuesday copies the READY into briefs/ at stamp).
#
# Identity: exports NexusAI's OWN az/gh dirs (az only under T1; gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, grep, rev-list, ls-tree);
# shasum / bash -n over session-tools files; python/grep over `git show` output; docker version/info/images/ps (read); ls, ps, tmux list-panes, test -e.
# It writes nothing and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate_batch23.sh [--check]
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

QA_DIR='/Volumes/Laptop-DEV/!CODING/Testing Agent MAIN'
TUE='/Volumes/Laptop-DEV/TUESDAY'
BRIEFS="$TUE/2_Project_Files/fleet/qa-agent/briefs"
STAGED="$TUE/2_Project_Files/fleet/briefs_staged"
BRIEF="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
READY_A="${QA_READY_OVERRIDE:-$BRIEFS/2026-10-16_nexusai-rd846-READY-mail.txt}"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
SUCC_S99O="$STAGED/2026-10-16_nexusai_O_successor_S99O.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
S99="$ST/s99o"
LOCKTOOL="$ST/nexusai-lock.sh"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED (identical on the T9 copy) — PINNED
T9_NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
LOCK_BASE_T9="$T9_NX/session-tools/locks"                     # the LIVE base: the installed tool's own default (RD-847)
LOCKQ_J="$LOCK_BASE_T9/queue-jest"
LOCKQ_D="$LOCK_BASE_T9/queue-docker"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
HANDOVER="$NX/HANDOVER-S96O.md"
RPTS="$QA_DIR/projects/nexusai/reports"
T9_RPTS='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports'
B22_DIR="$T9_RPTS/2026-10-13-gate-batch22"
B22_REPORT="$B22_DIR/report.md"
B22_INST="$B22_DIR/evidence/inst"
B20_STARVE="$T9_RPTS/2026-10-08-gate-batch20/evidence/answer-starvation.txt"
PREV_FLOORLIB="$B22_INST/qa-floorlib22.sh"
REPORT="$RPTS/2026-10-16-gate-batch23/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-batch23'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
AZPY='/opt/homebrew/Cellar/azure-cli/2.90.0/libexec/bin/python'
AZ_PACKER_GLOB='/opt/homebrew/Cellar/azure-cli/2.90.0/libexec/lib/python3*/site-packages/azure/cli/command_modules/acr/_archive_utils.py'
DIND_DIGEST='sha256:aa3df78ecf320f5fafdce71c659f1629e96e9de0968305fe1de670e0ca9176ce'
NODE_ALPINE_DIGEST='sha256:44fce696f38ba8c987c4db89954051000bbd05ffd8d8659ba15ed4a8602e937f'
AZ_TENANT='d500ebad-cf53-4f2a-a501-f831289e67fc'
AZ_SUB='0c57ab37-349c-47ae-a10f-e284a380bbb9'
ACR_TAG='nexusai:gate23-3a45914'

MAIN_SHA='3907c5789a7d87302c0cdd20f4250e2f391971e4'      # origin main at drafting (11:53 AEDT; RD-840+841's counts commit) = RD-846's parent
A_BRANCH='rd-846-acr-build-s99o'
A_HEAD="${QA_A_HEAD_OVERRIDE:-3a459146919eb56b169381193e0b6b7b4e039bdd}"
BUILD_HEAD='ca8aa27c7277da5f'                              # sha256("3a45914…" 40 bytes, no newline)[:16] — buildIdentity.js
BUILD_BASE='dbce3e7f0dfd1346'                              # the same for 3907c57 (= HANDOVER-S96O §1)

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
DKF='Dockerfile'
DIG='.dockerignore'
BID='backend/services/buildIdentity.js'
BPF='backend/bootPreflight.js'
DKF_M_BLOB='12aab559a9a48dad8228d7faad5e4f8f9fab7c1e'
DKF_A_BLOB='4e5638e0b01488ba1e6c1d7e766b6ccc2b4a84fd'
PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
TESTS_TREE='41274706aa325a15739a6c2a399b411c7b20611a'
BID_BLOB='5cb8b9a43596e7bbd41bc3bc6ed983267fd757a5'
REMOVED_LINE='COPY --from=build /app/package.json /app/package-lock.json ./'
PAIR_LINE='COPY package.json package-lock.json ./'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 23'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-batch23] ANSWER'
NOTTESTED_LINE="Not tested by this gate: ACR's own build daemon beyond the one candidate run T1 permits (its layer-diff mode is modelled by a local vfs dind daemon), CodeQL and the CI Build at the head (no pull request), the full jest suite on Node 24 (the verify ran on this machine's Node 26.8.1), the image on Azure Container Apps or any deployed revision, the demo (behind RD-76 SSO), the release registry and the 2.2.x package, BuildKit as ACR does not use it, linux/amd64 emulation beyond the daemon's native platform, Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild; the image's own npm ci contacted the registry inside the build only), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_at() { g show "${1}:${COUNTS_FILE}" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
cnt() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
cntx() { g show "${1}:${2}" 2>/dev/null | grep -cxF -- "$3"; }
lineat() { g show "${1}:${2}" 2>/dev/null | sed -n "${3}p"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
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

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, "batch 23", with ONE member, one verdict and ONE report. It is a FRESH gate, TIER 1, on a NEW MACHINE: Kam's Mac mini, working volume /Volumes/Laptop-DEV, with the T9 drive /Volumes/KK_T9_External_HDD also mounted. The member: RD-846 (TIER 1, the shipped build, NexusAI-O / S99O): the image's production stage stops re-copying package.json and package-lock.json from the build stage. That line made a layer identical to what the production stage already inherits from base, so under a naive layer diff it was EMPTY, and ACR's classic builder then failed the NEXT copy with "failed to get layer ...: layer does not exist" (ACR runs cr4m, cr4n, cr4p at main 3907c57). The fix is one commit, Dockerfile only. RD-846 blocks the owed demo deploy and every release image. Your verdict — GO, GO WITH FINDINGS or NO GO — rests on six properties, and you prove each INDEPENDENTLY: never trust the builder's logs as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, nothing to Partner Center, the demo, production or any human, no browser, no host npm registry. Docker: only your own qa-b23 daemons, containers, volumes and tags (H-35). Azure: only what Tuesday ruled under T1 — at most ONE az acr build of the head to a NEW tag, and only if YOU decide it is needed.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_nexusai-gate-batch23.md
It opens with the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1-T6 as Tuesday stamped them, the commission's rulings, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, the READY mail it names (read it WHOLE), the clarifications it names at source (C-63, C-72 and C-190 first), gate 22's brief section 3a (the H-rules, carried by reference) and gate 22's report on the T9 (the structural template and the instrument source). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's LEGITIMATE SHAPES table (section 2a, rows r0 to r9) is required measurement, row by row, base and head in the same window, each with a control that can fail.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGET. RD-846: rd-846-acr-build-s99o at 3a459146919eb56b169381193e0b6b7b4e039bdd, ONE commit whose only parent is origin main 3907c5789a7d87302c0cdd20f4250e2f391971e4; Dockerfile only, +8/-2, blob 12aab55 -> 4e5638e; the only non-comment change is the removed production-stage line COPY --from=build /app/package.json /app/package-lock.json ./. The __tests__ tree, package.json (384805d), the lock (19477a9, proxy-addr 2.0.8) and .dockerignore are identical at base and head; counts 4506/283 at both. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

THE SIX PROPERTIES (brief section 2a). (1) THE DEFECT ROW r1: on your OWN docker:27-dind daemon with the vfs storage driver (the naive diff), with an overlay2 daemon as the control, the build context packed by azure-cli 2.90.0's own source packer over a fresh checkout of your clone (the ACR-equivalent shape) AND over a git archive extraction (the builder's shape; the brief's WRONG 1: ACR's context was 78.04MB, the builder's local one 68.06MB — diff them by member), classic builder, no cache: the base 3907c57 FAILS at COPY --from=build /app/docs/ with "layer does not exist", the head 3a45914 PASSES, and the head with the removed line re-added (M-readd) FAILS again — C-76's red proof of the cause. Then THE ACR DECISION r9: you decide whether one more ACR build of the head is needed and SAY so with the reason (the builder's ACR run cr4q is RELAYED, never your proof); if Tuesday's T1 is (a) and you decide yes, at most ONE run, tag nexusai:gate23-3a45914 in nexusaidevacrfa39, under T1's conditions exactly (az account show must read tenant d500ebad and subscription 0c57ab37 first). (2) THE CONTENT ROW r2: base and head images built on one daemon in one window from the same context shape and the same node:24-alpine digest; /app listed per file (path, owner, mode, full sha256, symlink target) plus a node_modules digest; the diff must be EMPTY, package.json and package-lock.json byte-identical to git's blobs, the config different only in build-arg values — with a planted-difference control that proves the comparison can fail (a planted listing AND a real one-byte image plant), and the image-manifest helper's derived set compared with the real /app. (3) THE BOOT ROW r3: run the head image with --network none, the T3 throwaway secret by env file only, and read /api/health from inside the container: build must be ca8aa27c7277da5f (sha256 of the 40-hex commit, first 16 hex, exactly as HANDOVER-S96O section 1 applies it), the base dbce3e7f0dfd1346, an image built without the arg "unknown"; say if the formula cannot be applied and why. (4) r4: npm run verify at the head through the project's jest lock: 4506/4506, 283 suites, no lost test names vs base (r5 supplies the base names of every image reader). (5) r0: the diff is Dockerfile only and the removed line is exactly that production-stage copy, nothing else. (6) r6: the builder's flagged items, each ruled GO or NOTES — the build stage's own pair copy (head line 74, the READY's ":73") with a census of every COPY's layer size on vfs, the missing red-first jest cell (a proposed static guard is a NOTE, not a blocker; you may PROBE one as a scratch script, never committed), and Node 26 locally vs Node 24 in CI. Plus r5 (the image-reading cells at head and base, TIER-1 cell row, with M-readd and M-dupBase), r7 (main moved, C-68), r8 (prior work, C-49, and CI read only).

MAIN MAY MOVE (ruling b): take M0 = origin main AT YOUR OWN START by git ls-remote, say so; it must be 3907c57 or a descendant. If it moved, name what landed and which rows it invalidates; a move touching the Dockerfile, .dockerignore, the package pair or an image reader means your image legs measure the head, not the merged tree — say so. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the installed lock tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. No PR exists for the head: CodeQL is NOT RUN and the CI Build is NOT RUN — say so; re-check with gh READ ONLY (repo datasecau/Reporting_Dashboard_Au). C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCKS (C-63: the jest AND docker lock). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, RD-821 round 3, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. Its DEFAULT BASE is the T9's session-tools/locks (RD-847): call it with NEXUSAI_LOCK_BASE UNSET so you serialise with the builder seats; this drive's own session-tools/locks is STALE and is never read as live or touched. EVERY docker build and container run goes in the docker lock, every jest run in the jest lock, each hold tagged qa-b23- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time across both kinds. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: you never stop your own waiter to re-file behind a merge that filed after you; if a ticket is queued ahead of you, wait behind it (FIFO). AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read the T9 queue-jest and queue-docker at start, around every hold and at end; any qa-b23- entry that is not your current hold is a STOP.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): ONE offline npm ci --offline --ignore-scripts --no-audit --no-fund in your own jest tree with --cache pointing at an APFS clone of the local npm cache; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots the host server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from your tree's own path (RD-827, C-205). The IMAGE builds are different (T2): their pulls from Docker Hub and the image's own npm ci inside the build are the one named network exception; record every digest, and base and head of one comparison must resolve the same node:24-alpine digest.

FULL VERIFY (r4) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions (the test-server-helper control pair belted red and unbelted green; belted runs kept; "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; other failures on their merits). SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), Node v26.8.1 as T5 rules. RULING (b) and its EXTENSION (ruling o): if r4 stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The TIER-1 cell row r5 is NOT covered by that extension: it runs, and a TIER-1 verdict whose cell rows did not run is PROVISIONAL and releases nothing. A mutant arm counts only if the mutant LANDED (the exact mutated text present, the original absent) and parses; a red from a mutant that never landed is a VOID arm.

THE INSTRUMENT RULES H-1 TO H-35 (brief section 3a; gate 22's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it; scan every hold's and every container's logs for the T3 throwaway (docker inspect output included, scanned, never quoted whole). H-3: a LANDING CONTROL for every plant, mutant and daemon driver. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted. H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every docker build, every dind start, every container boot and every context pack (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned, rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only. H-31: offline host node_modules. H-32: this gate BUILDS and RUNS images — every caption "local image of <sha> built by the gate on <daemon/driver> — NOT the demo, NOT a release image". H-33: never rm — quarantine; every child reaped by pid. H-34: the live T9 lock bases. H-35: DOCKER DISCIPLINE — only qa-b23 objects; never touch the builder's rd846-dind, rd846-dind-vfs or any other foreign container, image or volume; never prune; no docker push, no docker login; your dind daemons get no host bind mount; your containers are stopped and LEFT, listed by id.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/batch23.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN), each by git clone --shared --no-checkout of the NexusAI repo on THIS drive, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout (stale, cd2b543) or any worktrees/ folder (their .git links point at the T9). In the NexusAI repo use ONLY read verbs (show, diff, log, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge. Copy instruments BY COPY from gate 22's evidence/inst on the T9 (re-point every hard-coded T9 path in your copies to this drive EXCEPT the lock base; correct qa-floorlib22.sh's stale ROOT and NEG defaults from the live list below); never write into another gate's dirs on either drive. Never write into the builders' session-tools (copy, then hash at start and end); never run dind-build.sh, vfs-matrix.sh or own-install.sh in place. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, no swap of the lock tool. No Microsoft, Log Analytics or login host, no CDN, no demo, no Partner Center, no ARM deployment, no release registry. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, the context packs and their member lists, r7, r8, the offline npm ci, the static-guard probe); then file your holds one at a time, through your COPY of gate 22's qa-file22.sh re-pointed to qa-b23 tags. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock, ticket, container or image. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; record the foreign count and the foreign running-container set beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: main and rd-846-acr-build-s99o, plus the installed lock tool's sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so; never re-base mid-gate.

QUESTIONS: your routing name is QA/NexusAI-batch23. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-batch23] ANSWER". Approval-class items (Azure beyond T1, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-16-gate-batch23/report.md
Write its VERDICT and FINDINGS table early and keep it current.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 23
Lead the body with the one RD-846 line in the form the brief's section 11 gives (DEFECT, ACR, CONTENT, BOOT, VERIFY, SCOPE, FLAGGED), then one line naming M0 and END main, the C-102 sweep, which rows ran on Opus 4.8 (or none), which holds ran and which are NAMED NOT RUN under ruling (b) extended, the docker objects you left by id, and "CodeQL NOT RUN (no PR) for RD-846". Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-A1 to L-A6 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-63, C-72, C-57, C-68, C-190 with its ADDENDUM, C-209, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-40, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125 and C-133 are carried. That section must carry this line verbatim:
Not tested by this gate: ACR's own build daemon beyond the one candidate run T1 permits (its layer-diff mode is modelled by a local vfs dind daemon), CodeQL and the CI Build at the head (no pull request), the full jest suite on Node 24 (the verify ran on this machine's Node 26.8.1), the image on Azure Container Apps or any deployed revision, the demo (behind RD-76 SSO), the release registry and the 2.2.x package, BuildKit as ACR does not use it, linux/amd64 emulation beyond the daemon's native platform, Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild; the image's own npm ci contacted the registry inside the build only), and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }
[[ "$A_HEAD" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: head '$A_HEAD' is not a full 40-hex sha" >&2; exit 9; }

# MODEL — read from Tuesday's models_latest.json (opus level), never typed from memory; REFUSE unless it is the brief's pin.
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ "$MODEL" = "$MODEL_PIN" ] || { echo "REFUSING: $MODELS_JSON levels.opus.model_id is '${MODEL:-unreadable}', not $MODEL_PIN as the brief states — re-brief" >&2; exit 9; }

# 6 — both pinned shas are commits in the object store (this launcher never fetches).
for S in "$MAIN_SHA" "$A_HEAD"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — the head is ONE commit whose only parent is main 3907c57.
[ "$(g rev-parse "${A_HEAD}^" 2>/dev/null)" = "$MAIN_SHA" ] && [ -z "$(g rev-parse -q --verify "${A_HEAD}^2" 2>/dev/null)" ] \
  && [ "$(g rev-list --count "${MAIN_SHA}..${A_HEAD}" 2>/dev/null)" = "1" ] \
  || { echo "REFUSING: RD-846 is not ONE non-merge commit on 3907c57" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the branch exactly the pin (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
printf '%s\n' "$LSR_ALL" | grep -q "^${A_HEAD}[[:space:]]refs/heads/${A_BRANCH}\$" || {
  echo "REFUSING: origin refs/heads/$A_BRANCH is not $A_HEAD — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY move (ruling b): 3907c57 or a descendant IN THE OBJECT STORE; the head already on it REFUSES; a Dockerfile / .dockerignore / package move REFUSES.
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 3907c57 — main was rewritten; re-brief" >&2; exit 18; }
if g merge-base --is-ancestor "$A_HEAD" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: 3a45914 is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(printf '%s\n' "$MOVED" | grep -xF -e "$DKF" -e "$DIG" -e "$PKG" -e "$LOCK" | tr '\n' ' ')"
[ -z "$HIT" ] || { echo "REFUSING: main moved 3907c57..${M_ORIGIN:0:7} and touched ${HIT}— the base of r1/r2 is no longer main; re-brief" >&2; exit 18; }
HITT="$(printf '%s\n' "$MOVED" | grep -E '^(__tests__/|backend/services/buildIdentity\.js$|backend/bootPreflight\.js$)' | tr '\n' ' ')"
[ -z "$HITT" ] || echo "NOTE: main's movement touches ${HITT}— r4/r5 and the C-102 sweep run on the head's tree; the gate names it (r7, C-68)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 3907c57) — the gate re-pins M0 itself (r7)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED jest/docker-lock tool PINNED by sha256 (REFUSE if moved); its default base names the T9 and the T9 base is present; both kinds; --replace.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks}"' "$LOCKTOOL" || { echo "REFUSING: the installed tool's default lock base no longer names the T9 base (WRONG 9 / H-34's premise)" >&2; exit 90; }
[ -d "$LOCK_BASE_T9" ] && [ -d "$LOCKQ_J" ] && [ -d "$LOCKQ_D" ] || { echo "REFUSING: the LIVE lock base $LOCK_BASE_T9 (queue-jest, queue-docker) is not present — is the T9 mounted?" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the docker kind" >&2; exit 90; }
LB_WAS=''; [ -z "${NEXUSAI_LOCK_BASE+x}" ] || { LB_WAS="$NEXUSAI_LOCK_BASE"; echo "NOTE: NEXUSAI_LOCK_BASE was set in the launcher's environment ('$LB_WAS') — UNSET before exec (H-34)" >&2; }

# 22 — the delta is EXACTLY the Dockerfile; numstat; ONE non-comment change = the removed production-stage COPY; no package change.
[ "$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null)" = "$DKF" ] || { echo "REFUSING: RD-846's delta is not the Dockerfile alone" >&2; exit 22; }
[ "$(g diff --numstat "$MAIN_SHA" "$A_HEAD" -- "$DKF" 2>/dev/null | cut -f1,2 | tr '\t' ' ')" = "8 2" ] || { echo "REFUSING: Dockerfile numstat is not +8/-2" >&2; exit 22; }
NCL="$(g diff "$MAIN_SHA" "$A_HEAD" -- "$DKF" 2>/dev/null | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-][[:space:]]*(#|$)')"
[ "$NCL" = "-$REMOVED_LINE" ] || { echo "REFUSING: the non-comment changed lines are not exactly '-$REMOVED_LINE'. Got:" >&2; printf '%s\n' "$NCL" >&2; exit 22; }

# 93 — the premises at source (WRONG 4, 5, 6).
[ "$(blob "$MAIN_SHA" "$DKF")" = "$DKF_M_BLOB" ] && [ "$(blob "$A_HEAD" "$DKF")" = "$DKF_A_BLOB" ] || { echo "REFUSING: Dockerfile blobs are not 12aab55 -> 4e5638e" >&2; exit 93; }
[ "$(cntx "$MAIN_SHA" "$DKF" "$REMOVED_LINE")" = "1" ] && [ "$(cntx "$A_HEAD" "$DKF" "$REMOVED_LINE")" = "0" ] \
  && [ "$(lineat "$A_HEAD" "$DKF" 74)" = "$PAIR_LINE" ] && [ "$(lineat "$A_HEAD" "$DKF" 23)" = "$PAIR_LINE" ] \
  && [ "$(lineat "$MAIN_SHA" "$DKF" 73)" = "$PAIR_LINE" ] && [ "$(lineat "$MAIN_SHA" "$DKF" 22)" = "$PAIR_LINE" ] \
  && [ "$(cntx "$A_HEAD" "$DKF" "$PAIR_LINE")" = "2" ] \
  || { echo "REFUSING: the pair lines are not as briefed (base 22/73 + production COPY; head 23/74, production COPY gone — WRONG 4)" >&2; exit 93; }
[ "$(cntx "$A_HEAD" "$DKF" 'FROM node:24-alpine AS base')" = "1" ] && [ "$(cntx "$A_HEAD" "$DKF" 'FROM base AS production')" = "1" ] \
  && [ "$(cntx "$A_HEAD" "$DKF" 'ARG BUILD_COMMIT_SHA=')" = "1" ] && [ "$(cntx "$A_HEAD" "$DKF" 'COPY --from=build /app/docs/ ./docs/')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$DKF" 'RUN npm ci --omit=dev && npm cache clean --force')" = "1" ] \
  || { echo "REFUSING: the Dockerfile's FROM / ARG / docs COPY / npm ci lines are not as briefed (r1/r3, T2's premise)" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$BID")" = "$BID_BLOB" ] && [ "$(blob "$A_HEAD" "$BID")" = "$BID_BLOB" ] \
  && [ "$(cnt "$A_HEAD" "$BID" "return crypto.createHash('sha256').update(raw, 'utf8').digest('hex').slice(0, 16);")" = "1" ] \
  || { echo "REFUSING: buildIdentity.js is not the briefed formula (5cb8b9a, sha256 first 16) — r3's premise" >&2; exit 93; }
[ "$(printf %s "$A_HEAD" | shasum -a 256 | cut -c1-16)" = "$BUILD_HEAD" ] && [ "$(printf %s "$MAIN_SHA" | shasum -a 256 | cut -c1-16)" = "$BUILD_BASE" ] \
  || { echo "REFUSING: the health digests computed now are not ca8aa27c7277da5f / dbce3e7f0dfd1346" >&2; exit 93; }
grep -qF "$BUILD_BASE" "$HANDOVER" || { echo "REFUSING: HANDOVER-S96O no longer carries the expected 3907c57 build $BUILD_BASE (r3's formula check)" >&2; exit 93; }
[ "$(cnt "$A_HEAD" "$BPF" 'const SESSION_SECRET_MIN_LENGTH = 32;')" = "1" ] || echo "NOTE: bootPreflight's SESSION_SECRET minimum moved — T3's premise may be stale" >&2

# 98 — shared blobs; counts; census; lock versions.
for S in "$MAIN_SHA" "$A_HEAD"; do
  [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] && [ "$(blob "$S" __tests__)" = "$TESTS_TREE" ] \
    || { echo "REFUSING: package.json / lock / .dockerignore / __tests__ at ${S:0:7} are not 384805d / 19477a9 / 3e45ec5 / 4127470" >&2; exit 98; }
  [ "$(counts_at "$S")" = "4506 283" ] || { echo "REFUSING: $COUNTS_FILE at ${S:0:7} reads '$(counts_at "$S")', not '4506 283'" >&2; exit 98; }
  [ "$(ntests "$S")" = "336" ] || { echo "REFUSING: the __tests__ census at ${S:0:7} is not 336" >&2; exit 98; }
done
[ "$(lockver "$LOCK_BLOB" proxy-addr)" = "2.0.8" ] || { echo "REFUSING: proxy-addr in 19477a9 is not 2.0.8 (RD-827)" >&2; exit 98; }

# 70 — the npm cache, the sqlite3 prebuild, the carried rulings (REFUSALs where a ruling is missing).
if [ -d "$NPM_CACHE/index-v5" ]; then
  for T in proxy-addr/-/proxy-addr-2.0.8.tgz sqlite3/-/sqlite3-5.1.7.tgz; do
    grep -r -l -F -m1 -- "$T" "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no '$T' — the offline npm ci (H-31) may ENOTCACHE" >&2
  done
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" && grep -qF 'merge hold full verify + PR Build are the gate' "$RULING_B" \
  || { echo "REFUSING: Tuesday's ruling (b) is not at $RULING_B as quoted" >&2; exit 70; }
[ -s "$B20_STARVE" ] && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$B20_STARVE" || { echo "REFUSING: ruling (o)'s EXTENSION is not at $B20_STARVE (T9) as quoted" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" \
  || { echo "REFUSING: the RETIREMENT of ruling (i)'s yield is not in gate 19's RELEASE as quoted" >&2; exit 70; }
[ -s "$SUCC_S99O" ] && grep -qF 'All 222 folders under `worktrees/` hold `.git` links to the T9 path' "$SUCC_S99O" \
  || { echo "REFUSING: Tuesday's successor brief to S99O (WRONG 12's source) is not at $SUCC_S99O as quoted" >&2; exit 70; }

# 70D — docker and the packer (the image legs r1-r3 are the gate's core; REFUSE if the daemon or the packer is absent); the rest NOTEd.
command -v docker >/dev/null 2>&1 || { echo "REFUSING: docker CLI not found — r1-r3 cannot run" >&2; exit 70; }
DSV="$(docker version --format '{{.Server.Version}}' 2>/dev/null)"
[ -n "$DSV" ] || { echo "REFUSING: the docker daemon does not answer (docker version) — start Docker Desktop before launch; r1-r3 cannot run" >&2; exit 70; }
[ "$DSV" = "29.7.2" ] || echo "NOTE: docker server is $DSV, not 29.7.2 as measured at drafting — the gate records it" >&2
[ -x "$AZPY" ] || { echo "REFUSING: azure-cli 2.90.0's python ($AZPY) is absent — r1's ACR-equivalent packer is missing" >&2; exit 70; }
# shellcheck disable=SC2086
AZPK="$(ls -d $AZ_PACKER_GLOB 2>/dev/null | head -1)"
[ -n "$AZPK" ] && grep -qF 'def _pack_source_code' "$AZPK" || { echo "REFUSING: azure-cli's _archive_utils._pack_source_code is not at $AZ_PACKER_GLOB" >&2; exit 70; }
docker images --digests --format '{{.Repository}}:{{.Tag}} {{.Digest}}' 2>/dev/null | grep -qxF "docker:27-dind $DIND_DIGEST" \
  || echo "NOTE: docker:27-dind is not cached at $DIND_DIGEST — the gate's first dind start pulls it (T2) and records the digest" >&2
FOREIGN_CTR="$(docker ps -a --format '{{.Names}}' 2>/dev/null | grep -E '^rd846-' | tr '\n' ' ')"
[ -z "$FOREIGN_CTR" ] || echo "NOTE: builder-owned containers present: ${FOREIGN_CTR}— never started, stopped, removed or reused (H-35)" >&2
QA_CTR="$(docker ps -a --format '{{.Names}}' 2>/dev/null | grep -E '^qa-b23-' | tr '\n' ' ')"
[ -z "$QA_CTR" ] || { echo "REFUSING: qa-b23-* containers already exist (${QA_CTR}) — a previous gate-23 session left them; read before launch" >&2; exit 70; }
AZP="$(python3 -c 'import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8-sig"))
s=[x for x in d.get("subscriptions",[]) if x.get("isDefault")]
print((s[0].get("tenantId","")+" "+s[0].get("id","")+" "+(s[0].get("user") or {}).get("type","")) if s else "")' "$ID_ROOT/.azure/azureProfile.json" 2>/dev/null)"
[ "$AZP" = "$AZ_TENANT $AZ_SUB servicePrincipal" ] || echo "NOTE: NexusAI's az profile default is '${AZP:-unreadable}', not tenant d500ebad / sub 0c57ab37 / servicePrincipal — T1's run would be NOT RUN at its own account check" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T5) — the gate records it" >&2

# 31 — READY, builder evidence, gate 22's instruments (T9), standing references.
for f in "$READY_A" "$CLAR" "$HANDOVER" "$BRIEF22" "$B22_REPORT" "$CHARTER" \
         "$S99/dind-build.sh" "$S99/vfs-matrix.sh" "$S99/vfs-matrix.out" "$S99/dind-vfs-3907c57.log" "$S99/dind-acrctx-3907c57.log" "$S99/dind-classic-3907c57.log" \
         "$S99/local-classic-3907c57.log" "$S99/acr-retry-3907c57.log" "$S99/acr-cand-3a45914.log" "$S99/manifest-acrctx-3907c57.txt" "$S99/manifest-acrctx-3a45914.txt" \
         "$S99/own-install.sh" "$S99/own-install-rd846.out" "$S99/verify-rd846.log" "$S99/mail-03-repro.txt" \
         "$B22_INST/HOLD22.sh" "$B22_INST/env22.sh" "$B22_INST/qa-file22.sh" "$B22_INST/qa-floorlib22.sh" "$B22_INST/qa-floorcount.py" "$B22_INST/qa-to.sh" \
         "$B22_INST/qa-jestwrap.sh" "$B22_INST/qa-jsum.js" "$B22_INST/qa-npm22.sh" "$B22_INST/qa-pin22.sh" "$B22_INST/qa-netbelt.sb" "$B22_INST/qa-netbelt-nodns.sb" \
         "$B22_INST/qa-netbelt-ctl.js" "$B22_INST/qa-h1-scan.py" "$B22_INST/qa-mail.py" "$B22_INST/qa-mailread.py" "$B22_INST/qa-lockcheck.py" "$B22_INST/qa-mut22.py" \
         "$B22_INST/qa-mutlib22.sh" "$B22_INST/g21/qa-verify21.sh" "$B22_INST/g21/qa-h1-selftest21.sh"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "$A_HEAD" "$READY_A" && grep -qF 'READY FOR GATE' "$READY_A" && grep -qF 'PRIOR WORK' "$READY_A" && grep -qF 'NOT TESTED' "$READY_A" \
  || { echo "REFUSING: the READY does not name the head, READY FOR GATE, PRIOR WORK and NOT TESTED" >&2; exit 31; }
grep -qF 'Sending build context to Docker daemon  78.04MB' "$S99/acr-cand-3a45914.log" && grep -qF 'Sending build context to Docker daemon  68.06MB' "$S99/dind-vfs-3907c57.log" \
  && grep -qF 'layer does not exist' "$S99/dind-vfs-3907c57.log" && grep -qF "8de8e5c~1 7c47ec4 rc=125 last=''" "$S99/vfs-matrix.out" \
  && grep -qF 'node:node 644 2614fdb976d0efce ./CHANGELOG.md' "$S99/manifest-acrctx-3907c57.txt" && [ "$(head -1 "$S99/verify-rd846.log")" = "v26.8.1" ] \
  && grep -qF 'VERDICT: PASS — 4506/4506 tests passed across 283 suites (jest exit 0)' "$S99/verify-rd846.log" \
  || { echo "REFUSING: a builder log no longer carries the line the brief quotes (WRONG 1/2/3/11)" >&2; exit 31; }
[ "$(fsha "$S99/manifest-acrctx-3907c57.txt")" = "dc9678e7226df9e329bc163960880150f39d7f69b6ab8c3196c9b504beb58cc2" ] && [ "$(fsha "$S99/manifest-acrctx-3a45914.txt")" = "dc9678e7226df9e329bc163960880150f39d7f69b6ab8c3196c9b504beb58cc2" ] \
  || echo "NOTE: the builder's manifests changed since drafting (WRONG 2) — RELAYED only" >&2
grep -qF 'STATUS: COMPLETE' "$B22_REPORT" || { echo "REFUSING: gate 22's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
grep -qE '^ROOT=\$\{ROOT:-85673\}' "$B22_INST/qa-floorlib22.sh" || echo "NOTE: gate 22's qa-floorlib22.sh ROOT default is no longer 85673 — the brief's 'STALE defaults' line names the old value" >&2
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | 20' "$BRIEF22" || echo "NOTE: gate 22's brief does not read as stamped — the H-rule reference may be stale" >&2
grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF22" || { echo "REFUSING: gate 22's brief has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }

# 39 — the floor instrument is named in the brief.
grep -qF 'qa-floorlib22.sh' "$BRIEF" && grep -qF "$B22_INST/" "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument / gate 22's instrument dir" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-16_nexusai-rd846-READY-mail.txt" "2026-10-13_nexusai-gate-batch22.md" "2026-10-16_nexusai_O_successor_S99O.md" "2026-10-05_qa_b14_belt_ANSWER.md" \
         "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "answer-starvation.txt" "qa-file22.sh" "HOLD22.sh" "env22.sh" "acr-cand-3a45914.log" "vfs-matrix.out" \
         "manifest-acrctx-3907c57.txt" "HANDOVER-S96O" "models_latest.json" "QA_AGENT_CHARTER.md"; do
  grep -qF "$P" "$BRIEF" || { echo "REFUSING: brief must name $P" >&2; exit 10; }
done

# 11 — identity: NexusAI's OWN dirs.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
[ -d "$CLAUDE_CONFIG_DIR" ] || { echo "REFUSING: Tuesday's claude store $CLAUDE_CONFIG_DIR is absent" >&2; exit 11; }

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
for T in 'RD-846 is TIER 1' 'THIS IS A TIER-1 GATE' 'No other member, no slots' 'NO HOST NPM REGISTRY' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-b23-' 'RETIRED' 'H-34' 'H-35' 'C-63' 'C-72' \
         'THE DEFECT ROW' 'THE CONTENT ROW' 'THE BOOT ROW' 'THE ACR DECISION' 'PLANTED-DIFFERENCE CONTROLS' 'M-readd' 'NOT a blocker'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-846 (TIER 1' 'TIER 1' 'six properties' 'THE DEFECT ROW' 'THE CONTENT ROW' 'THE BOOT ROW' 'THE ACR DECISION' 'vfs' 'overlay2' 'M-readd' 'planted-difference control' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-b23-' 'RETIRED' 'NEXUSAI_LOCK_BASE UNSET' \
         'docker lock' 'nexusai:gate23-3a45914' 'a NOTE, not a blocker' 'ca8aa27c7277da5f' 'dbce3e7f0dfd1346' "never trust the builder's logs"; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$MAIN_SHA" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$DKF_M_BLOB" "$DKF_A_BLOB" "$PKG_BLOB" "$LOCK_BLOB" "$DIG_BLOB" "$TESTS_TREE" "$PREBUILD_SHA" "$DIND_DIGEST" "$NODE_ALPINE_DIGEST" "$AZ_TENANT" "$AZ_SUB" "$BUILD_HEAD" "$BUILD_BASE" "$ACR_TAG"; do
  grep -qF -- "$S" "$BRIEF" || grep -qF -- "${S:0:7}" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_0-9]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
grep -qF "$SUBJECT" "$BRIEF" || { echo "REFUSING: brief must carry the subject exactly: $SUBJECT" >&2; exit 15; }
case "$PROMPT" in *"$SUBJECT"*) ;; *) echo "REFUSING: prompt must carry the subject exactly: $SUBJECT" >&2; exit 15 ;; esac
case "$PROMPT" in *"/Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
[ -s "$TUE/4_Credentials/.env" ] || { echo "REFUSING: the AgentMail key file $TUE/4_Credentials/.env is absent" >&2; exit 20; }
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD/TUESDAY'; then echo "REFUSING: the prompt names the T9 TUESDAY tree — this machine's Tuesday is /Volumes/Laptop-DEV/TUESDAY" >&2; exit 15; fi
[ "$(grep -oE 'qa-b23-[A-Za-z0-9_-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-b23- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-b23-[A-Za-z0-9_-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-b23- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED; then both live queues as the launch finds them (read-only ls/grep).
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac
for Q in "$LOCKQ_J" "$LOCKQ_D"; do
  MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$Q"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in $Q now — the gate files behind them (brief §9)" >&2
  BQ="$(grep -l '^tag=qa-b23' "$Q"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-b23* ticket(s) already in $Q — a live or stale gate-23 ticket; read before launch" >&2; exit 41; }
done

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-32 (RE-BASED' "$BRIEF" && grep -qF 'H-34 (RE-BASED' "$BRIEF" && grep -qF 'H-35 (NEW' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-32/H-34 (re-based)/H-35 (new)" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-846 RD-847 RD-827 C-63 C-72 C-57 C-68 C-190 C-209 C-185 C-192 C-205 C-141 C-40 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-133 ADDENDA%6%and%7
r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 T1 T2 T3 T5 M0 4506/4506 283%suites 19477a9 2.0.8 proxy-addr 3907c57 3a45914 cr4m cr4q 78.04MB 68.06MB nexusaidevacrfa39 d500ebad 0c57ab37
docker:27-dind node:24-alpine azure-cli%2.90.0 git%archive layer%does%not%exist /api/health HANDOVER-S96O --network%none M-dupBase line%74
L-A1 L-A6 L-Y1 H-1 H-3 H-4 H-9 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 git%clone%--shared id STOP VOID EXCLUSIVE
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file22.sh qa-floorlib22.sh Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL H-35 qa-b23 rd846-dind"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' '^## 2. Tier and severity' \
         '^## 2a. LEGITIMATE SHAPES' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' '^## 7. THE MERGED TREE' '^## 8. CI' '^## 9. Floor discipline' \
         '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qE '^None — \*\*round 1 of 2\.\*\*' "$BRIEF" || { echo "REFUSING: the brief's PRIOR ROUND block does not declare round 1 (template round-N rule)" >&2; exit 19; }
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|disclosed|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r6 r7 r8 r9; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 1 2 3 4 5 6; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# the READY's PRIOR WORK line the brief quotes, verbatim in both.
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qF -- "$T" "$READY_A" || { echo "REFUSING: '$T' is no longer in the READY — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
No earlier branch or fix for this ticket existed (ls-remote on rd-846*: none before mine).
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.
The customer image is built from MAIN at the merged head, NEVER from the package branch.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
a clean merge-tree and a changed measured surface are not in tension
Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included.
`alerts_threshold = errors`, so ANY new alert whose RULE severity is `error` blocks, whatever its security severity.
A PR's CodeQL run CANNOT show a PRE-EXISTING main alert as fixed
counts as known ONLY when the received object differs from the expected in `envReached` alone
No re-run is used as a clearance
a FAILED ls-remote is UNKNOWN, never a value.
A merge hold runs on a node_modules that matches the merged tree's package-lock.json.
is a SAME-PLACE handover.
Gate (`qa-*`) tickets are never moved; the holder is never touched.
TAG CONVENTION — only a merge HOLD's tag contains the word `merge`.
A check must be able to fail on the thing it claims to be about.
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-b23-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         'Main may MOVE' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'queue-docker/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' 'ticket-left-*' 'never two live holds' '-r<N>' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'docker push' 'prune' 'STOPPED and LEFT'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 81 — this gate's own premises are in the brief.
for w in 'C-190' 'NEVER opens, comments on, approves or merges a PR' 'RE-BASE' 'NEVER merges and never pushes' 'CodeQL is NOT RUN at the head' 'Blocker' 'setuid' 'pgrep' '`END ok`' \
         'exits 71' 'ARRAY option' '=====' 'UNKNOWN' '19477a9' 'proxy-addr' 'RD-827' 'RD-847' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' \
         'sqlite3 binding: cached prebuild, offline' 'NOT the demo, NOT a release image' 'vfs' 'overlay2' '_pack_source_code' 'git archive' '78.04MB' '68.06MB' 'layer does not exist' \
         'M-readd' 'M-dupBase' 'image-manifest.js' 'rd418-dockerignore-round3' 'line 74' 'ca8aa27c7277da5f' 'dbce3e7f0dfd1346' 'buildIdentity.js' 'bootPreflight.js' '--env-file' \
         '--network none' 'nexusai:gate23-3a45914' 'nexusaidevacrfa39' 'az account show' 'servicePrincipal' 'rd846-cand-3a45914' 'nexusaireleaseacr' 'NEXUSAI_LOCK_BASE' 'T9' \
         'WRONG 1' 'WRONG 6' 'WRONG 9' 'WRONG 10' 'WRONG 13' 'WRONG 14' 'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib22.sh' 'HOLD22.sh' 'qa-file22.sh' 'ADDENDUM 7' \
         'datasecau/Reporting_Dashboard_Au' 'never dismisses an alert' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae' 'claude-opus-5-5' 'Node v26.8.1' "node-version: '24'"; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks this gate's premise '$w'" >&2; exit 81; }
done

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
COORD_NAME=''
for NAME in tuesday wednesday; do
  if [ -n "$(pane_pid_of "$NAME" | sed '/^$/d')" ]; then
    [ -z "$COORD_NAME" ] || { echo "REFUSING: panes named BOTH 'tuesday' and 'wednesday' are live — the coordinator's negative control is ambiguous" >&2; exit 38; }
    COORD_NAME="$NAME"
  fi
done
[ -n "$COORD_NAME" ] || { echo "REFUSING: no tmux pane named 'tuesday' or 'wednesday' — the coordinator's negative control is required" >&2; exit 38; }
[ "$COORD_NAME" = "tuesday" ] || echo "NOTE: the coordinator's pane is named '$COORD_NAME' on this machine — used as the coordinator's negative control" >&2
for NAME in Datasec/NexusAI-M Datasec/NexusAI-N Datasec/NexusAI-O Datasec/NexusAI-P Datasec/NexusAI-R "$COORD_NAME"; do
  PP="$(pane_pid_of "$NAME")"
  NP="$(printf '%s\n' "$PP" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [ "$NP" = "0" ]; then
    [ "$NAME" = "$COORD_NAME" ] || echo "NOTE: no tmux pane named '$NAME' — not a negative control this launch" >&2; continue
  fi
  [ "$NP" = "1" ] || { echo "REFUSING: more than one tmux pane named '$NAME': '$PP' — cannot derive its negative-control seat" >&2; exit 38; }
  CP="$(claude_under "$PP")"
  [ "$(printf '%s\n' "$CP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: pane '$NAME' (pid $PP) has '${CP:-no}' claude descendant(s), not exactly one — a seat is missing or ambiguous" >&2; exit 38; }
  NEG_SEATS="$NEG_SEATS $CP"; NEG_DESC="$NEG_DESC \`$CP\` ($NAME);"
  [ "$NAME" = "$COORD_NAME" ] || NEG_BUILDERS=$((NEG_BUILDERS + 1))
done
[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-M/N/O/P/R — at least ONE negative control is required (WRONG 13)" >&2; exit 38; }
# fleet-monitor and every live 'QA/*' pane other than this gate's own: a negative control when exactly one claude runs under it.
EXTRA="$(printf '%s\n' "$PANES" | awk '{p=$1; $1=""; sub(/^ /,""); print $0}' | grep -E '^(QA/|fleet-monitor$)' | grep -vxF "$ROUTE_NAME" | sort -u)"
while IFS= read -r PEER; do
  [ -n "$PEER" ] || continue
  GP="$(pane_pid_of "$PEER")"; GC=''
  [ -n "$GP" ] && [ "$(printf '%s\n' "$GP" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] && GC="$(claude_under "$GP")"
  if [ -n "$GC" ] && [ "$(printf '%s\n' "$GC" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ]; then
    NEG_SEATS="$NEG_SEATS $GC"; NEG_DESC="$NEG_DESC \`$GC\` ($PEER);"
    echo "NOTE: $PEER has a live claude — added as a negative control (FIFO, never touched)" >&2
  else
    echo "NOTE: $PEER has no single live claude — not a negative control" >&2
  fi
done <<EOF_PEERS
$EXTRA
EOF_PEERS
NEG_SEATS="${NEG_SEATS# }"
NCOUNT="$(printf '%s\n' $NEG_SEATS | sed '/^$/d' | wc -l | tr -d ' ')"
[ "$(printf '%s\n' $NEG_SEATS | sort -u | wc -l | tr -d ' ')" = "$NCOUNT" ] || { echo "REFUSING: the derived seat pids are not distinct: $NEG_SEATS" >&2; exit 38; }

# 86 — no live gate-23 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 23 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note + every 'RULED: @STAMP@' slot, no placeholder) and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
NSTAMP="$(grep -cF "$PH_STAMP" "$BRIEF")"
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
READY_OK=1
[ -z "${QA_READY_OVERRIDE:-}" ] || READY_OK=0
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$READY_OK" = "0" ]; then
  echo "guards pass (9 MODEL 6 8 18 18b 90 22 93 98 70 70D 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86); stamp, route and/or READY NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7}; RD-846 $A_HEAD; lock tool sha256 ${INST_NOW:0:12}…; docker server $DSV; model $MODEL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$READY_OK" = "1" ] || echo "REFUSING (31R): the READY was read from QA_READY_OVERRIDE ($READY_A) — Tuesday copies it into briefs/ as 2026-10-16_nexusai-rd846-READY-mail.txt and launches without the override" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): $NSTAMP stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T6) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: $A_BRANCH = $A_HEAD at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192); main ${M_ORIGIN:0:7} (3907c57 or a descendant; no Dockerfile/.dockerignore/package move; head not on it) (18b)"
  echo "  lock tool 3c33f5ae… pinned; default base = T9, present; both queues read, no qa-b23 ticket (90, 41)"
  echo "  delta Dockerfile-only, one non-comment change (22); premises + health formula (93); blobs + counts + census (98); rulings (70); docker $DSV + az packer (70D)"
  echo "  evidence + gate 22 instruments (31); MODEL RULE (82); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: $MODEL at exec (from models_latest.json)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/main = $M_ORIGIN (3907c57 or a descendant; no Dockerfile, .dockerignore or package move since 3907c57; the head not on it). The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin; its default base is the T9's $LOCK_BASE_T9 (present) and NEXUSAI_LOCK_BASE is unset in your environment. Docker server $DSV answered. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# H-34: the gate's lock calls use the installed tool's own default base (the T9's).
unset NEXUSAI_LOCK_BASE
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
