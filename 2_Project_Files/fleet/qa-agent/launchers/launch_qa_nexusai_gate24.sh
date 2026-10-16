#!/bin/bash
# launch_qa_nexusai_gate24.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 24), ONE member, one verdict, ONE report
# (drafted 2026-10-17 from ~07:38 AEDT by a read-only drafting agent for Tuesday; the drafter ran only bash -n and --check).
# A FRESH gate (not a resume) on the Mac mini, /Volumes/Laptop-DEV; the T9 is ALSO mounted and carries the LIVE lock base (RD-847). TIER 1.
#   A — RD-848 (TIER 1; the shipped build / image) rd-848-dockerfile-build-stage-s100o @ 065a0d8: FOUR commits on main 17fc6c5:
#       the build stage stops re-copying package.json + package-lock.json (gate 23 F-846-1), a per-stage redundant-COPY jest guard
#       (__tests__/helpers/dockerfile-stages.js + rd848-no-redundant-copy.test.js, 19 cells), counts 4506/283 -> 4525/284.
#   No other member, no slots. The base IS origin main 17fc6c5 (RD-846's merge, PR #86).
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate24' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate24.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-24 drafting commission (2026-10-17). READY already in briefs/. THE MODEL RULE: Kam, live board 2026-09-30 09:07,
# card nexusai-gate11-opus55-safeguard-model-switch, option (b) — QA gates may switch to Opus 4.8 when flagged, PER SESSION.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED). The installed jest/docker-lock tool is RD-821 r3 (sha256 3c33f5ae…), default base on the T9 (RD-847).
# FINDINGS-ONLY: never merges (outside its own clones), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never swaps
# the lock tool; no fix, no deploy, no production, no HTTP to a production or demo host, nothing to Partner Center/demo/any human.
# DOCKER: own qa-g24-* daemons/containers only (H-35; gate 23's qa-b23-* and the builder's rd846-* are FOREIGN). Docker Hub + the image's own npm ci
# inside builds only (T2). AZURE: only Tuesday's T1 (a) — at most ONE `az acr build` to nexusai:gate24-065a0d8 and ONE `az acr run` (read-only lister).
#
# PATTERN: launch_qa_nexusai_gate_batch23.sh (prompt EMBEDDED, --check mode, pin guards with the C-192 retry, THE MODEL RULE, floor, H-rules,
# the LIVE negative-control seat derivation 38R, route-line and stamp guards last). CHANGES, each deliberate:
#   - 7/8: the member is FOUR linear commits on main (no merge commit in the range), not one.
#   - 22: the delta is EXACTLY four files; the Dockerfile's ONLY non-comment change is the removed BUILD-stage pair COPY.
#   - 93: base :23/:74 and head :23/:69 line pins; the health formula computed here for 065a0d8 / 17fc6c5.
#   - 98: counts 4506/283 at base and 4525/284 at head; __tests__ census 336 -> 338.
#   - 31: the instrument source is gate 23's evidence/inst on THIS drive (gate 23 DELIVERED); gate 22's and gate 20's T9 files still read for rulings.
#   - 19: T-slots T1..T7 (T6 = the clone mode, gate 23 §14 item 9).
#   - READY path overridable by QA_READY_OVERRIDE (drafter's --check only).
#
# Identity: exports NexusAI's OWN az/gh dirs (az only under T1; gh READ-ONLY for §8); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list, ls-tree);
# shasum / bash -n over session-tools files; python/grep over `git show` output; docker version/images/ps (read); ls, ps, tmux list-panes, test -e.
# It writes nothing and starts no claude.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate24.sh [--check]
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
BRIEF="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
READY_A="${QA_READY_OVERRIDE:-$BRIEFS/2026-10-17_nexusai-rd848-READY-mail.txt}"
PLAN_ANS="$BRIEFS/2026-10-17_nexusai-rd848-plan-ANSWER.txt"
CHARTER="$TUE/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md"
MODELS_JSON="$TUE/0_Brain/dashboard/data/models_latest.json"
MODEL_PIN='claude-opus-5-5'
BELT_ANS="$STAGED/2026-10-05_qa_b14_belt_ANSWER.md"
SQLITE_RULING="$STAGED/2026-10-05_qa_b14_sqlite3_ANSWER.md"
NOTIFIER_ANS="$STAGED/2026-10-05_qa_gate16_notifier_ANSWER.md"
RULING_B="$STAGED/2026-10-06_nexusai_g18_ruling_b_deliver_now.md"
G19_RELEASE="$STAGED/2026-10-12_nexusai_gate19_RELEASE.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
ST="$NX/session-tools"
S100="$ST/s100o"
LOCKTOOL="$ST/nexusai-lock.sh"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED — PINNED
T9_NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
LOCK_BASE_T9="$T9_NX/session-tools/locks"                     # the LIVE base: the installed tool's own default (RD-847)
LOCKQ_J="$LOCK_BASE_T9/queue-jest"
LOCKQ_D="$LOCK_BASE_T9/queue-docker"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
T9_RPTS='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports'
B20_STARVE="$T9_RPTS/2026-10-08-gate-batch20/evidence/answer-starvation.txt"
B23_DIR="$RPTS/2026-10-16-gate-batch23"
B23_REPORT="$B23_DIR/report.md"
B23_INST="$B23_DIR/evidence/inst"
REPORT="$RPTS/2026-10-17-gate24-rd848/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate24'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'
AZPY='/opt/homebrew/Cellar/azure-cli/2.90.0/libexec/bin/python'
AZ_PACKER_GLOB='/opt/homebrew/Cellar/azure-cli/2.90.0/libexec/lib/python3*/site-packages/azure/cli/command_modules/acr/_archive_utils.py'
DIND_DIGEST='sha256:aa3df78ecf320f5fafdce71c659f1629e96e9de0968305fe1de670e0ca9176ce'
AZ_TENANT='d500ebad-cf53-4f2a-a501-f831289e67fc'
AZ_SUB='0c57ab37-349c-47ae-a10f-e284a380bbb9'
ACR_TAG='nexusai:gate24-065a0d8'
DEMO_DIGEST='sha256:c12c43e538f1274c1a7ba180f2cdfd595be63ec16eee0e45c690903734e08e4f'
CAND_DIGEST='sha256:a173b79574d5fb2fd4fc356c68b0fa47dd8101770c20e2b075a1844122ccc508'

MAIN_SHA='17fc6c5157d5446cc015e97555fdc1ffcdc986ee'      # origin main at drafting (07:38:45 AEDT) = RD-846's merge (PR #86)
A_BRANCH='rd-848-dockerfile-build-stage-s100o'
A_HEAD="${QA_A_HEAD_OVERRIDE:-065a0d8f0f871ecd77636231014511edf167cc8b}"
A_NCOMMITS=4
BUILD_HEAD='15f6e1debe3ac6c5'                              # sha256("065a0d8…" 40 bytes, no newline)[:16] — buildIdentity.js
BUILD_BASE='def3ac7e654fdacd'                              # the same for 17fc6c5

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'
LOCK='package-lock.json'
DKF='Dockerfile'
DIG='.dockerignore'
BID='backend/services/buildIdentity.js'
HELPER='__tests__/helpers/dockerfile-stages.js'
TESTF='__tests__/rd848-no-redundant-copy.test.js'
IMF='__tests__/helpers/image-manifest.js'
DKF_M_BLOB='4e5638e0b01488ba1e6c1d7e766b6ccc2b4a84fd'
DKF_A_BLOB='f0367f12af2a13836245b1a21796325439c7069e'
PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'
LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'
DIG_BLOB='3e45ec511803b02014fc376245656cf830c90df4'
IMF_BLOB='2040ca2ec3a712561011829ce7672fb18861c5c5'
TESTS_TREE_M='41274706aa325a15739a6c2a399b411c7b20611a'
TESTS_TREE_A='b566eb6726ecffcf12b70418f2336b57b5a55703'
BID_BLOB='5cb8b9a43596e7bbd41bc3bc6ed983267fd757a5'
REMOVED_LINE='COPY package.json package-lock.json ./'
SH_LINE='COPY *.sh ./'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 24'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate24] ANSWER'
NOTTESTED_LINE="Not tested by this gate: ACR's own build daemon beyond the ACR legs T1 permits (its layer-diff mode is modelled by a local vfs dind daemon), CodeQL and the CI Build at the head (no pull request), the full jest suite on Node 24 (the verify ran on this machine's Node 26.8.1), the image on Azure Container Apps or any deployed revision, the demo (behind RD-76 SSO) and whether a merge to main auto-deploys it (deploy-demo.yml's CI_DEPLOY_ENABLED was not read), the release registry and the 2.2.x package, BuildKit as ACR does not use it, linux/amd64 emulation beyond the daemon's native platform, Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild; the image's own npm ci contacted the registry inside the build only), and Windows."
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 24, with ONE member, one verdict and ONE report. It is a FRESH gate, TIER 1, round 1 of 2, on Kam's Mac mini, working volume /Volumes/Laptop-DEV, with the T9 drive /Volumes/KK_T9_External_HDD also mounted (it carries the LIVE lock base). The member: RD-848 (TIER 1, the shipped build, NexusAI-O / S100O): the image's BUILD stage stops re-copying package.json and package-lock.json, which it already inherits from base via deps — gate 23's finding F-846-1: that copy recorded NO layer on a naive-diff daemon and survived only because a RUN followed it; one inserted COPY after it re-armed RD-846's ACR failure ("failed to get layer ...: layer does not exist"). The ticket also adds a per-stage jest guard (a new helper and a new 19-cell test) and regenerates the counts to 4525/284. Your verdict — GO, GO WITH FINDINGS or NO GO — rests on six properties, and you prove each INDEPENDENTLY: never trust the builder's logs as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool; no fixes, no deploys, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no browser, no host npm registry. Docker: only your own qa-g24 daemons, containers, volumes and tags (H-35). Azure: only what Tuesday ruled under T1. One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_nexusai-gate24-rd848.md
It opens with the TIER argument and the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1-T7 as Tuesday stamped them, the commission's properties, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names, the READY mail it names (read it WHOLE), the clarifications it names at source (C-63, C-72 and C-190 first), gate 22's and gate 23's brief section 3a (the H-rules, carried by reference) and gate 23's report on THIS drive (the structural template, the origin of F-846-1, F-846-2 and N-846-1, and the instrument source). Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a table (rows r0 to r9) and section 2b (the guard as a CHECKER: its legitimate shapes and the READY's ten claims C1 to C10, each a check that CAN FAIL with a positive and a negative control) are required measurement, base and head in the same window.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE TARGET. RD-848: rd-848-dockerfile-build-stage-s100o at 065a0d8f0f871ecd77636231014511edf167cc8b, FOUR linear commits on origin main 17fc6c5157d5446cc015e97555fdc1ffcdc986ee (9f20773 the red-first guard, b2fc9bf the Dockerfile fix, 6e0e437 the helper's CodeQL pre-scan rewrite, 065a0d8 the counts). Four files: Dockerfile (blob 4e5638e -> f0367f1, +13/-8, whose only non-comment change is the removed build-stage line COPY package.json package-lock.json ./ at base line 74), the new helper __tests__/helpers/dockerfile-stages.js, the new test __tests__/rd848-no-redundant-copy.test.js, and scripts/verify-expected-counts.json (4506/283 -> 4525/284). package.json (384805d), the lock (19477a9, proxy-addr 2.0.8), .dockerignore, image-manifest.js, the backend and .github are identical at base and head. The builder's ACR candidate cr4s was built from b2fc9bf, NOT from the head: build 065a0d8 yourself. A Tuesday ADDENDUM mailed from tuesday-agent@ during the gate supersedes the closing lines.

THE SIX PROPERTIES (brief sections 2a and 2b). (1) THE RE-ARM ROW r1, on your OWN docker:27-dind daemon with the vfs storage driver (the naive diff), an overlay2 daemon as the control, contexts packed by azure-cli 2.90.0's own source packer over fresh checkouts of your clones, classic builder, no cache: P-base (17fc6c5 plus COPY LICENSE ./ right after its line 74) FAILS with "layer does not exist" — the control that proves the daemon sees the shape, and on overlay2 it PASSES; P-head (065a0d8 plus COPY LICENSE ./ right after its line 69, COPY *.sh ./) PASSES; M-readd848 (the head with the removed line restored, then COPY LICENSE ./) FAILS again — C-76's red proof; the plain base ALSO passes (latent), so a head PASS alone discriminates nothing; and your per-step census finds NO no-layer COPY in ANY stage of the head (the base's census finds exactly the line-74 pair). If P-base does not fail, r1 is VOID for the head. Then THE ACR DECISION r9 under T1. (2) THE IMAGE ROW r2: base and head built on one daemon in one window from the same context shape and the same node:24-alpine digest, production images AND --target build images; /app listed per entry (path, type, owner, mode, FULL sha256, symlink target, node_modules per entry) — the production diff must be EMPTY, package.json and package-lock.json byte-identical to git's blobs, the config different only in build-arg values; the head's build stage must still hold the pair (inherited) and must actually run (every build-stage step executed, 47 steps vs 48); three planted-difference controls must fire (a planted listing, a one-byte shipped-file image plant, and a build-stage-only plant that changes the build target's /app by exactly one path and leaves production equal). The READY's "202 entries, diff EMPTY" against main's image is re-measured, never trusted: its lister truncates digests, skips node_modules entries and symlink targets (brief WRONG 4); and remember the empty production diff is near-tautological for a build-stage change (WRONG 1) — the re-arm row is the discriminating evidence. (3) THE BOOT ROW r3: the head image with --network none, the T3 throwaway secret by env file only, /api/health read from inside the container: build must be 15f6e1debe3ac6c5, the base def3ac7e654fdacd, an image built without the arg "unknown". (4) THE SUITE ROW r4: npm run verify at the head through the project's jest lock: 4525/4525, 284 suites; the base 4506/4506, 283 suites; the names compared as SETS — base contained in head, LOST 0, head minus base exactly RD-848's 19 names. (5) r0 SCOPE: four files; the Dockerfile's only non-comment change is that one removed build-stage instruction. (6) THE GUARD ROW r5/r6: the 20 image-reading suites at head and base by name, the READY's ten guard claims each as a check that can fail, your OWN helper mutants (killed or survived — a surviving mutant is a clause guarded by no cell), and the false-negative probe M-chown0 (a byte-identical re-copy spelled with the default owner, --chown=0:0, which the guard's textual flag identity calls new while the real layer is empty) run through the guard AND built on vfs. Plus r7 (main moved, C-68), r8 (prior work, C-49: why the build-stage pair existed, from git log with an EXPLICIT rev — the root checkout's HEAD is a stale cd2b543 — and whether F-846-1, F-846-2 and N-846-1 are fixed), and CodeQL read only.

MAIN MAY MOVE (ruling b): take M0 = origin main AT YOUR OWN START by git ls-remote, say so; it must be 17fc6c5 or a descendant. If it moved, name what landed and which rows it invalidates; a move touching the Dockerfile, .dockerignore, the package pair, the counts file or an image reader means your image legs measure the head, not the merged tree — say so. GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the installed lock tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included — this diff adds 412 lines of it), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. No PR exists for the head: CodeQL is NOT RUN and the CI Build is NOT RUN — say so; re-check with gh READ ONLY (repo datasecau/Reporting_Dashboard_Au); your own pattern pre-scan of the two new files is READ ONLY evidence, never a clearance. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCKS (C-63: the jest AND docker lock). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, RD-821 round 3, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. Its DEFAULT BASE is the T9's session-tools/locks (RD-847): call it with NEXUSAI_LOCK_BASE UNSET so you serialise with the builder seats; this drive's own session-tools/locks is STALE and is never read as live or touched; if the T9 unmounts, stop filing and mail a QUESTION. EVERY docker build and container run goes in the docker lock, every jest run in the jest lock, each hold tagged qa-g24- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time across both kinds. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: you never stop your own waiter to re-file behind a merge that filed after you; if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S100O is on its own merge queue now. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read the T9 queue-jest and queue-docker at start, around every hold and at end; any qa-g24- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. Build images and run a full verify only below a 1-minute load of 40.

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): ONE offline npm ci --offline --ignore-scripts --no-audit --no-fund in your own head jest tree with --cache pointing at an APFS clone of the local npm cache on the same volume; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that boots the host server names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from your tree's own path (RD-827, C-205). The IMAGE builds are different (T2): their pulls from Docker Hub and the image's own npm ci inside the build are the one named network exception; record every digest, and base and head of one comparison must resolve the same node:24-alpine digest.

FULL VERIFIES (r4) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions (the test-server-helper control pair belted red and unbelted green; belted runs kept; "verify UNBELTED by Tuesday's 2026-10-05 answer; matches CI"; other failures on their merits). SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), Node v26.8.1 as T5 rules. RULING (b) and its EXTENSION (ruling o): if a verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The TIER-1 cell row r5 and the image rows r1 and r2 are NOT covered by that extension: they run, and a TIER-1 verdict whose cell or image rows did not run is PROVISIONAL and releases nothing. A mutant arm counts only if the mutant LANDED (the exact mutated text present, the original absent) and parses; a red from a mutant that never landed is a VOID arm, and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-35 (brief section 3a; gate 22's and gate 23's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it; scan every hold's and every container's logs for the T3 throwaway (docker inspect output included, scanned, never quoted whole); never copy gate 23's .throwaway-ss. H-3: a LANDING CONTROL for every plant, probe, mutant and daemon driver, checked in the packed member bytes. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted, every path with a space quoted. H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), every docker build, every dind start, every container boot, every context pack and every az call (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned, rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only; the builder's probe commits in the NexusAI object store (48c7676, 396771f, 317018d) are never built or cited. H-31: offline host node_modules. H-32: this gate BUILDS and RUNS images — every caption "local image of <sha> built by the gate on <daemon/driver> — NOT the demo, NOT a release image". H-33: never rm — quarantine; every child reaped by pid. H-34: the live T9 lock bases. H-35: DOCKER DISCIPLINE — only qa-g24 objects; never touch the builder's rd846-dind, rd846-dind-vfs, gate 23's qa-b23 containers or any other foreign container, image or volume; never prune; no docker push, no docker login; your dind daemons get no host bind mount; your containers are stopped and LEFT, listed by id.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate24.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN), each by the clone mode Tuesday ruled in T6 (default git clone --no-local --no-checkout) of the NexusAI repo on THIS drive, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout (stale, cd2b543) or any worktrees/ folder (their .git links point at the T9). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge. Copy instruments BY NAME from gate 23's evidence/inst on THIS drive (never the whole directory: it holds gate 23's throwaway secret and its quarantine), re-point every gate-23 path in your copies to gate 24 EXCEPT the lock base, correct qa-floorlib23.sh's ROOT and NEG defaults from the live list below; never write into another gate's dirs on either drive. Never write into the builders' session-tools (copy, then hash session-tools/s100o at start and end); never run vfs-matrix.sh, manifest-in-image.sh, rd848-real-trees.js or own-install.sh in place. Findings-only: never push, no commits outside your clones, no tickets, no PRs, no edits in NexusAI, no swap of the lock tool. No Microsoft, Log Analytics or login host, no CDN, no demo, no Partner Center, no ARM deployment, no release registry, no workflow dispatch, no repo variable read or written. No mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, the context packs and their member lists, r7, r8, the offline npm ci, the static guard checks C2, C3 and C10); then file your holds one at a time, through your COPY of gate 23's qa-file23.sh re-pointed to qa-g24 tags. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's process, lock, ticket, container or image. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start (the coordinator's pid changed mid-gate in gate 23); record the foreign count and the foreign running-container set beside every result; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: main and rd-848-dockerfile-build-stage-s100o, plus the installed lock tool's sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so; never re-base mid-gate. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta.

QUESTIONS: your routing name is QA/NexusAI-gate24. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate24] ANSWER". Approval-class items (Azure beyond T1, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-17-gate24-rd848/report.md
Write its VERDICT and FINDINGS table early and keep it current. Findings are G24-<n>, notes N24-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 24
Lead the body with the one RD-848 line in the form the brief's section 11 gives (RE-ARM, ACR, IMAGE, BOOT, SUITE, SCOPE, GUARD, CodeQL), then one line naming M0 and END main, the C-102 sweep, which rows ran on Opus 4.8 (or none), which holds ran and which are NAMED NOT RUN under ruling (b) extended, the docker objects you left by id, and "CodeQL NOT RUN (no PR) for RD-848". The report's last line is that same RD-848 line. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-A1 to L-A6 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-63, C-72, C-57, C-68, C-190 with its ADDENDUM, C-209, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-40, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125 and C-133 are carried. That section must carry this line verbatim:
Not tested by this gate: ACR's own build daemon beyond the ACR legs T1 permits (its layer-diff mode is modelled by a local vfs dind daemon), CodeQL and the CI Build at the head (no pull request), the full jest suite on Node 24 (the verify ran on this machine's Node 26.8.1), the image on Azure Container Apps or any deployed revision, the demo (behind RD-76 SSO) and whether a merge to main auto-deploys it (deploy-demo.yml's CI_DEPLOY_ENABLED was not read), the release registry and the 2.2.x package, BuildKit as ACR does not use it, linux/amd64 emulation beyond the daemon's native platform, Partner Center, the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild; the image's own npm ci contacted the registry inside the build only), and Windows.
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

# 7 / 8 — the head is FOUR linear (non-merge) commits on main 17fc6c5.
g merge-base --is-ancestor "$MAIN_SHA" "$A_HEAD" 2>/dev/null \
  && [ "$(g rev-list --count "${MAIN_SHA}..${A_HEAD}" 2>/dev/null)" = "$A_NCOMMITS" ] \
  && [ -z "$(g rev-list --merges "${MAIN_SHA}..${A_HEAD}" 2>/dev/null)" ] \
  || { echo "REFUSING: RD-848 is not $A_NCOMMITS linear non-merge commits on 17fc6c5" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): the branch exactly the pin (REFUSE); main read.
lsr refs/heads/main "refs/heads/$A_BRANCH" || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
printf '%s\n' "$LSR_ALL" | grep -q "^${A_HEAD}[[:space:]]refs/heads/${A_BRANCH}\$" || {
  echo "REFUSING: origin refs/heads/$A_BRANCH is not $A_HEAD — moved or never pushed; re-brief. ls-remote said:" >&2; printf '%s\n' "${LSR_ALL:-<nothing>}" >&2; exit 18; }
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="refs/heads/$1" '$2==r{print $1}'; }
# 18b — main MAY move (ruling b): 17fc6c5 or a descendant IN THE OBJECT STORE; the head already on it REFUSES; a Dockerfile / .dockerignore / package move REFUSES; a counts move is a NOTE (C-57).
M_ORIGIN="$(ref_now main)"
[[ "$M_ORIGIN" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: could not read origin main by ls-remote (got '${M_ORIGIN:-nothing}') — UNKNOWN (C-192)" >&2; exit 18; }
[ "$(g cat-file -t "$M_ORIGIN" 2>&1)" = "commit" ] || { echo "REFUSING: origin main $M_ORIGIN is not in the object store — this launcher never fetches; wait for a seat's fetch or re-brief" >&2; exit 18; }
g merge-base --is-ancestor "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null || { echo "REFUSING: origin main $M_ORIGIN does not descend from 17fc6c5 — main was rewritten; re-brief" >&2; exit 18; }
if g merge-base --is-ancestor "$A_HEAD" "$M_ORIGIN" 2>/dev/null; then echo "REFUSING: 065a0d8 is already an ancestor of origin main ${M_ORIGIN:0:7} — merged before its gate; re-brief" >&2; exit 18; fi
MOVED="$(g diff --name-only "$MAIN_SHA" "$M_ORIGIN" 2>/dev/null | sort -u)"
HIT="$(printf '%s\n' "$MOVED" | grep -xF -e "$DKF" -e "$DIG" -e "$PKG" -e "$LOCK" | tr '\n' ' ')"
[ -z "$HIT" ] || { echo "REFUSING: main moved 17fc6c5..${M_ORIGIN:0:7} and touched ${HIT}— the base of r1/r2 is no longer main; re-brief" >&2; exit 18; }
printf '%s\n' "$MOVED" | grep -qxF "$COUNTS_FILE" && echo "NOTE: main moved 17fc6c5..${M_ORIGIN:0:7} and changed $COUNTS_FILE (S100O's queue-2 merges) — RD-848's merge will need C-57's regeneration; r4's counts are read on the head tree and the move is named (r7)" >&2
HITT="$(printf '%s\n' "$MOVED" | grep -E '^(__tests__/|backend/services/buildIdentity\.js$|backend/bootPreflight\.js$)' | tr '\n' ' ')"
[ -z "$HITT" ] || echo "NOTE: main's movement touches ${HITT}— r4/r5 and the C-102 sweep run on the head's tree; the gate names it (r7, C-68)" >&2
[ "$M_ORIGIN" = "$MAIN_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:0:7} (moved from 17fc6c5) — the gate re-pins M0 itself (r7)" >&2
PRREF="$(g ls-remote origin 'refs/pull/*/head' 2>/dev/null | awk -v h="$A_HEAD" '$1==h{print $2}' | tr '\n' ' ')"
[ -z "$PRREF" ] || echo "NOTE: a PR ref now carries the head (${PRREF}) — CodeQL may have run; the gate reads it (§8), the brief says 'no PR'" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED jest/docker-lock tool PINNED by sha256 (REFUSE if moved); its default base names the T9 and the T9 base is present; both kinds; --replace.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks}"' "$LOCKTOOL" || { echo "REFUSING: the installed tool's default lock base no longer names the T9 base (RD-847 / H-34's premise)" >&2; exit 90; }
[ -d "$LOCK_BASE_T9" ] && [ -d "$LOCKQ_J" ] && [ -d "$LOCKQ_D" ] || { echo "REFUSING: the LIVE lock base $LOCK_BASE_T9 (queue-jest, queue-docker) is not present — is the T9 mounted? (RD-847)" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the docker kind" >&2; exit 90; }
LB_WAS=''; [ -z "${NEXUSAI_LOCK_BASE+x}" ] || { LB_WAS="$NEXUSAI_LOCK_BASE"; echo "NOTE: NEXUSAI_LOCK_BASE was set in the launcher's environment ('$LB_WAS') — UNSET before exec (H-34)" >&2; }

# 22 — the delta is EXACTLY four files; the Dockerfile's ONE non-comment change = the removed build-stage pair COPY.
EXP_FILES="$(printf '%s\n' "$DKF" "$HELPER" "$TESTF" "$COUNTS_FILE" | sort)"
[ "$(g diff --name-only "$MAIN_SHA" "$A_HEAD" 2>/dev/null | sort)" = "$EXP_FILES" ] || { echo "REFUSING: RD-848's delta is not exactly Dockerfile + the helper + the test + the counts file" >&2; exit 22; }
[ "$(g diff --numstat "$MAIN_SHA" "$A_HEAD" -- "$DKF" 2>/dev/null | cut -f1,2 | tr '\t' ' ')" = "13 8" ] || { echo "REFUSING: Dockerfile numstat is not +13/-8" >&2; exit 22; }
NCL="$(g diff "$MAIN_SHA" "$A_HEAD" -- "$DKF" 2>/dev/null | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' | grep -vE '^[+-][[:space:]]*(#|$)')"
[ "$NCL" = "-$REMOVED_LINE" ] || { echo "REFUSING: the Dockerfile's non-comment changed lines are not exactly '-$REMOVED_LINE'. Got:" >&2; printf '%s\n' "$NCL" >&2; exit 22; }

# 93 — the premises at source (blobs, line pins, health formula).
[ "$(blob "$MAIN_SHA" "$DKF")" = "$DKF_M_BLOB" ] && [ "$(blob "$A_HEAD" "$DKF")" = "$DKF_A_BLOB" ] || { echo "REFUSING: Dockerfile blobs are not 4e5638e -> f0367f1" >&2; exit 93; }
[ "$(cntx "$MAIN_SHA" "$DKF" "$REMOVED_LINE")" = "2" ] && [ "$(cntx "$A_HEAD" "$DKF" "$REMOVED_LINE")" = "1" ] \
  && [ "$(lineat "$MAIN_SHA" "$DKF" 23)" = "$REMOVED_LINE" ] && [ "$(lineat "$MAIN_SHA" "$DKF" 74)" = "$REMOVED_LINE" ] \
  && [ "$(lineat "$A_HEAD" "$DKF" 23)" = "$REMOVED_LINE" ] && [ "$(lineat "$A_HEAD" "$DKF" 69)" = "$SH_LINE" ] \
  && [ "$(g show "${A_HEAD}:${DKF}" 2>/dev/null | grep -cE '^COPY ')" = "22" ] && [ "$(g show "${MAIN_SHA}:${DKF}" 2>/dev/null | grep -cE '^COPY ')" = "23" ] \
  || { echo "REFUSING: the pair / line pins are not as briefed (base :23 + :74; head :23 only, :69 = COPY *.sh ./; COPY count 23 -> 22)" >&2; exit 93; }
[ "$(cntx "$A_HEAD" "$DKF" 'FROM node:24-alpine AS base')" = "1" ] && [ "$(cntx "$A_HEAD" "$DKF" 'FROM deps AS build')" = "1" ] \
  && [ "$(cntx "$A_HEAD" "$DKF" 'FROM base AS production')" = "1" ] && [ "$(cntx "$A_HEAD" "$DKF" 'ARG BUILD_COMMIT_SHA=')" = "1" ] \
  && [ "$(cnt "$A_HEAD" "$DKF" 'RUN npm ci --omit=dev && npm cache clean --force')" = "1" ] && [ "$(g show "${A_HEAD}:${DKF}" 2>/dev/null | grep -c -- '--chown')" = "0" ] \
  || { echo "REFUSING: the Dockerfile's FROM / ARG / npm ci lines are not as briefed, or a --chown COPY appeared (r1/r3/r6, T2's premise)" >&2; exit 93; }
g ls-tree "$A_HEAD" -- LICENSE 2>/dev/null | grep -q 'blob' && ! g show "${A_HEAD}:${DIG}" 2>/dev/null | grep -qxF 'LICENSE' \
  || { echo "REFUSING: LICENSE is not a tracked, non-ignored file at the head — r1's re-arm probe has no source" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$BID")" = "$BID_BLOB" ] && [ "$(blob "$A_HEAD" "$BID")" = "$BID_BLOB" ] \
  && [ "$(cnt "$A_HEAD" "$BID" "return crypto.createHash('sha256').update(raw, 'utf8').digest('hex').slice(0, 16);")" = "1" ] \
  || { echo "REFUSING: buildIdentity.js is not the briefed formula (5cb8b9a, sha256 first 16) — r3's premise" >&2; exit 93; }
[ "$(printf %s "$A_HEAD" | shasum -a 256 | cut -c1-16)" = "$BUILD_HEAD" ] && [ "$(printf %s "$MAIN_SHA" | shasum -a 256 | cut -c1-16)" = "$BUILD_BASE" ] \
  || { echo "REFUSING: the health digests computed now are not 15f6e1debe3ac6c5 / def3ac7e654fdacd" >&2; exit 93; }
[ -z "$(g diff --name-only "$MAIN_SHA" "$A_HEAD" -- backend .github 2>/dev/null)" ] || { echo "REFUSING: backend/ or .github/ changed in RD-848 — the brief says identical" >&2; exit 93; }

# 98 — shared blobs; counts; census; lock versions.
for S in "$MAIN_SHA" "$A_HEAD"; do
  [ "$(blob "$S" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$S" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$S" "$DIG")" = "$DIG_BLOB" ] && [ "$(blob "$S" "$IMF")" = "$IMF_BLOB" ] \
    || { echo "REFUSING: package.json / lock / .dockerignore / image-manifest.js at ${S:0:7} are not 384805d / 19477a9 / 3e45ec5 / 2040ca2" >&2; exit 98; }
done
[ "$(blob "$MAIN_SHA" __tests__)" = "$TESTS_TREE_M" ] && [ "$(blob "$A_HEAD" __tests__)" = "$TESTS_TREE_A" ] || { echo "REFUSING: __tests__ trees are not 4127470 -> b566eb6" >&2; exit 98; }
[ "$(counts_at "$MAIN_SHA")" = "4506 283" ] || { echo "REFUSING: $COUNTS_FILE at 17fc6c5 reads '$(counts_at "$MAIN_SHA")', not '4506 283'" >&2; exit 98; }
[ "$(counts_at "$A_HEAD")" = "4525 284" ] || { echo "REFUSING: $COUNTS_FILE at 065a0d8 reads '$(counts_at "$A_HEAD")', not '4525 284'" >&2; exit 98; }
[ "$(ntests "$MAIN_SHA")" = "336" ] && [ "$(ntests "$A_HEAD")" = "338" ] || { echo "REFUSING: the __tests__ census is not 336 -> 338" >&2; exit 98; }
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
[ -s "$PLAN_ANS" ] && grep -qF 'Build and run the full verify only below a load of 40' "$PLAN_ANS" \
  || { echo "REFUSING: Tuesday's plan ANSWER to S100O (the load-40 rule the brief quotes) is not at $PLAN_ANS as quoted" >&2; exit 70; }

# 70D — docker and the packer (the image legs are the gate's core; REFUSE if the daemon or the packer is absent); the rest NOTEd.
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
FOREIGN_CTR="$(docker ps -a --format '{{.Names}}' 2>/dev/null | grep -E '^(rd84[0-9]-|qa-b23-)' | tr '\n' ' ')"
[ -z "$FOREIGN_CTR" ] || echo "NOTE: foreign containers present (builder rd84x-*, gate 23 qa-b23-*): ${FOREIGN_CTR}— never started, stopped, removed or reused (H-35)" >&2
QA_CTR="$(docker ps -a --format '{{.Names}}' 2>/dev/null | grep -E '^qa-g24-' | tr '\n' ' ')"
[ -z "$QA_CTR" ] || { echo "REFUSING: qa-g24-* containers already exist (${QA_CTR}) — a previous gate-24 session left them; read before launch" >&2; exit 70; }
AZP="$(python3 -c 'import json,sys
d=json.load(open(sys.argv[1],encoding="utf-8-sig"))
s=[x for x in d.get("subscriptions",[]) if x.get("isDefault")]
print((s[0].get("tenantId","")+" "+s[0].get("id","")+" "+(s[0].get("user") or {}).get("type","")) if s else "")' "$ID_ROOT/.azure/azureProfile.json" 2>/dev/null)"
[ "$AZP" = "$AZ_TENANT $AZ_SUB servicePrincipal" ] || echo "NOTE: NexusAI's az profile default is '${AZP:-unreadable}', not tenant d500ebad / sub 0c57ab37 / servicePrincipal — T1's legs would be NOT RUN at their own account check" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T5) — the gate records it" >&2

# 31 — READY, builder evidence, gate 23's instruments (THIS drive), standing references.
for f in "$READY_A" "$CLAR" "$BRIEF22" "$BRIEF23" "$B23_REPORT" "$CHARTER" \
         "$S100/vfs-matrix.sh" "$S100/vfs-matrix.out" "$S100/probe-commits.txt" "$S100/manifest-in-image.sh" "$S100/manifest-17fc6c5.txt" "$S100/manifest-b2fc9bf.txt" \
         "$S100/acr-cand-b2fc9bf.log" "$S100/acr-manifest-17fc6c5.log" "$S100/acr-manifest-b2fc9bf.log" "$S100/rd848-red-at-17fc6c5.log" "$S100/rd848-real-trees.js" \
         "$S100/rd848-real-trees.out" "$S100/rd848-mutants.out" "$S100/rd848-dockerfile-readers.out" "$S100/verify-rd848-2.log" "$S100/own-install.sh" "$S100/mail-03-ready-848.txt" \
         "$B23_INST/HOLD23.sh" "$B23_INST/env23.sh" "$B23_INST/qa-file23.sh" "$B23_INST/qa-floorlib23.sh" "$B23_INST/qa-floorcount.py" "$B23_INST/qa-to.sh" \
         "$B23_INST/qa-pin23.sh" "$B23_INST/qa-qlist23.sh" "$B23_INST/qa-k1.sh" "$B23_INST/qa-pack23.sh" "$B23_INST/qa-dock23.sh" "$B23_INST/qa-dock23b.sh" \
         "$B23_INST/qa-census23v3.py" "$B23_INST/qa-mut23.py" "$B23_INST/qa-r0.py" "$B23_INST/qa-r2list.py" "$B23_INST/qa-r2run.sh" "$B23_INST/qa-names23.py" \
         "$B23_INST/qa-npm23.sh" "$B23_INST/qa-runj23.sh" "$B23_INST/qa-verify23.sh" "$B23_INST/qa-holdlib23.sh" "$B23_INST/qa-h1-selftest23.sh" \
         "$B23_INST/qa-mail23.py" "$B23_INST/qa-mailread23.py" "$B23_INST/qa-jestwrap.sh" "$B23_INST/qa-jsum.js" "$B23_INST/qa-lockcheck.py" "$B23_INST/qa-h1-scan.py" \
         "$B23_INST/qa-ssprint.sh" "$B23_INST/qa-netbelt.sb" "$B23_INST/qa-netbelt-nodns.sb" "$B23_INST/qa-netbelt-ctl.js"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "$A_HEAD" "$READY_A" && grep -qF 'READY FOR GATE' "$READY_A" && grep -qF 'PRIOR WORK' "$READY_A" && grep -qF 'NOT TESTED' "$READY_A" \
  || { echo "REFUSING: the READY does not name the head, READY FOR GATE, PRIOR WORK and NOT TESTED" >&2; exit 31; }
grep -qF "48c7676706578c180ec510dcad23b643796ec67b 48c7676 rc=1 last='Step 19/49 : COPY LICENSE ./'" "$S100/vfs-matrix.out" \
  && grep -qF "396771fd782599cba553958e808376e8d4a910d1 396771f rc=0 last='Step 48/48" "$S100/vfs-matrix.out" \
  && grep -qF "$CAND_DIGEST" "$S100/acr-cand-b2fc9bf.log" && grep -qF 'Run ID: cr4s was successful' "$S100/acr-cand-b2fc9bf.log" \
  && grep -qF "$DEMO_DIGEST" "$S100/acr-manifest-17fc6c5.log" && grep -qF 'NM 17771 1c4210cdfd4128c5' "$S100/manifest-17fc6c5.txt" \
  && grep -qF 'VERDICT: PASS — 4525/4525 tests passed across 284 suites (jest exit 0)' "$S100/verify-rd848-2.log" \
  || { echo "REFUSING: a builder log no longer carries the line the brief relays (WRONG 3/4/5, C7)" >&2; exit 31; }
[ "$(fsha "$S100/manifest-17fc6c5.txt")" = "$(fsha "$S100/manifest-b2fc9bf.txt")" ] || echo "NOTE: the builder's two manifests are no longer byte-identical (WRONG 4) — RELAYED only" >&2
grep -qF 'STATUS: COMPLETE' "$B23_REPORT" || { echo "REFUSING: gate 23's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
grep -qF 'F-846-1' "$B23_REPORT" && grep -qF 'N-846-1' "$B23_REPORT" || { echo "REFUSING: gate 23's report no longer carries F-846-1 / N-846-1 (this ticket's origin)" >&2; exit 31; }
grep -q '^SELF-CHECK: re-read end-to-end for contradictions | 20' "$BRIEF23" || echo "NOTE: gate 23's brief does not read as stamped — the H-rule reference may be stale" >&2
grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF22" && grep -qF '## 3a. INSTRUMENT RULES' "$BRIEF23" || { echo "REFUSING: gate 22's or gate 23's brief has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }

# 39 — the floor instrument is named in the brief.
grep -qF 'qa-floorlib23.sh' "$BRIEF" && grep -qF '2026-10-16-gate-batch23/evidence/inst/' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument / gate 23's instrument dir" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-17_nexusai-rd848-READY-mail.txt" "2026-10-17_nexusai-rd848-plan-ANSWER.txt" "2026-10-13_nexusai-gate-batch22.md" "2026-10-16_nexusai-gate-batch23.md" \
         "2026-10-05_qa_b14_belt_ANSWER.md" "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "answer-starvation.txt" "qa-file23.sh" "HOLD23.sh" "env23.sh" \
         "acr-cand-b2fc9bf.log" "vfs-matrix.out" "manifest-in-image.sh" "models_latest.json" "QA_AGENT_CHARTER.md" ".throwaway-ss"; do
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
for T in 'RD-848 is TIER 1' 'THIS IS A TIER-1 GATE' 'No other member, no slots' 'round 1 of 2' 'NO HOST NPM REGISTRY' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-g24-' 'RETIRED' 'H-34' 'H-35' 'C-63' 'C-72' \
         'THE RE-ARM ROW' 'THE IMAGE ROW' 'THE BOOT ROW' 'THE SUITE ROW' 'THE GUARD ROW' 'THE ACR DECISION' 'PLANTED-DIFFERENCE CONTROLS' 'M-readd848' 'M-chown0' \
         'P-base' 'P-head' 'CHECKER' 'can fail' 'positive control' 'negative control' 'G24-<n>' 'NOT TESTED' 'PRIOR WORK' 'never dismisses an alert' 'No HTTP to any production or demo host'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'RD-848 (TIER 1' 'TIER 1' 'round 1 of 2' 'six properties' 'THE RE-ARM ROW' 'THE IMAGE ROW' 'THE BOOT ROW' 'THE SUITE ROW' 'THE GUARD ROW' 'THE ACR DECISION' \
         'vfs' 'overlay2' 'P-base' 'P-head' 'M-readd848' 'M-chown0' 'planted-difference controls' 'as SETS' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-g24-' 'RETIRED' 'NEXUSAI_LOCK_BASE UNSET' \
         'docker lock' 'T1' '15f6e1debe3ac6c5' 'def3ac7e654fdacd' "never trust the builder's logs" 'no HTTP to any production or demo host' 'One client only'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$A_HEAD" "$MAIN_SHA" "$LOCK_SHA_INST"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$DKF_M_BLOB" "$DKF_A_BLOB" "$PKG_BLOB" "$LOCK_BLOB" "$DIG_BLOB" "$TESTS_TREE_M" "$TESTS_TREE_A" "$PREBUILD_SHA" "$AZ_TENANT" "$AZ_SUB" "$BUILD_HEAD" "$BUILD_BASE" \
         "$ACR_TAG" "$DEMO_DIGEST" "$CAND_DIGEST"; do
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
[ "$(grep -oE 'qa-g24-[A-Za-z0-9_-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g24- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g24-[A-Za-z0-9_-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g24- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED; then both live queues as the launch finds them (read-only ls/grep).
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac
for Q in "$LOCKQ_J" "$LOCKQ_D"; do
  MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$Q"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in $Q now — the gate files behind them (brief §9)" >&2
  BQ="$(grep -l '^tag=qa-g24' "$Q"/* 2>/dev/null | wc -l | tr -d ' ')"
  [ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g24* ticket(s) already in $Q — a live or stale gate-24 ticket; read before launch" >&2; exit 41; }
done

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-32 (THE IMAGE LEGS' "$BRIEF" && grep -qF 'H-34 (THE LIVE LOCK BASES' "$BRIEF" && grep -qF 'H-35 (DOCKER DISCIPLINE' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-32/H-34/H-35" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-848 RD-846 RD-847 RD-827 F-846-1 F-846-2 N-846-1 C-63 C-72 C-57 C-68 C-190 C-209 C-185 C-192 C-205 C-141 C-40 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-133 ADDENDA%6%and%7
r0 r1 r2 r3 r4 r5 r6 r7 r8 r9 T1 T2 T3 T5 T6 M0 4525/4525 284%suites 4506/4506 283%suites 19477a9 2.0.8 proxy-addr 17fc6c5 065a0d8 b2fc9bf cr4s cd2b543
docker:27-dind node:24-alpine azure-cli%2.90.0 layer%does%not%exist /api/health --network%none --target%build COPY%LICENSE%./ line%74 line%69 C1 C10
L-A1 L-A6 L-Y1 H-1 H-3 H-4 H-9 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --no-local id STOP VOID EXCLUSIVE
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file23.sh qa-floorlib23.sh .throwaway-ss Never%rm datasecau/Reporting_Dashboard_Au ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g24 rd846-dind qa-b23 G24-<n>"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' \
         '^## 2. Tier and severity' '^## 2a. LEGITIMATE SHAPES' '^## 2b. THE GUARD IS A CHECKER' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' \
         '^## 7. THE MERGED TREE' '^## 8. CI' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qE '^None — \*\*round 1 of 2\.\*\*' "$BRIEF" || { echo "REFUSING: the brief's PRIOR ROUND block does not declare round 1 (template round-N rule)" >&2; exit 19; }
grep -qF "$B23_REPORT" "$BRIEF" || { echo "REFUSING: the brief does not name gate 23's report path (the origin of this ticket's findings)" >&2; exit 19; }
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|disclosed|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-A1 L-A2 L-A3 L-A4 L-A5 L-A6 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r6 r7 r8 r9; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for C in C1 C2 C3 C4 C5 C6 C7 C8 C9 C10; do grep -qF -- "- **$C " "$BRIEF" || { echo "REFUSING: brief lacks guard claim $C (§2b)" >&2; exit 19; }; done
for n in 1 2 3 4 5 6 7; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# the READY's PRIOR WORK line the brief quotes, verbatim in both.
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qF -- "$T" "$READY_A" || { echo "REFUSING: '$T' is no longer in the READY — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
Nothing else read the build-stage pair: grep of __tests__ for package-lock with Dockerfile -> dockerfile-install-and-labels (finds the FIRST pair COPY, still base :23), rd418, rd442 (read shippedFiles, unchanged). All green.
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
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g24-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         'Main may MOVE' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'queue-docker/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' 'ticket-left-*' 'never two live holds' '-r<N>' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'docker push' 'prune' 'STOPPED and LEFT' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac
grep -qF 'The report'"'"'s LAST line is the RD-848 verdict line' "$BRIEF" || { echo "REFUSING: brief must fix the report's last line as the verdict line" >&2; exit 71; }

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed' 'FAILS LOUDLY'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 81 — this gate's own premises are in the brief.
for w in 'C-190' 'NEVER opens, comments on, approves or merges a PR' 'NEVER merges and never pushes' 'CodeQL is NOT RUN at the head' 'Blocker' 'setuid' 'pgrep' '`END ok`' \
         'exits 71' 'ARRAY option' '=====' 'UNKNOWN' '19477a9' 'proxy-addr' 'RD-827' 'RD-847' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' \
         'sqlite3 binding' 'NOT the demo, NOT a release image' 'vfs' 'overlay2' '_pack_source_code' 'layer does not exist' 'deploy-demo.yml' 'CI_DEPLOY_ENABLED' \
         'M-readd848' 'M-chown0' 'M-sameBytes' 'HM-1' 'HM-7' 'dockerfile-stages.js' 'rd848-no-redundant-copy' 'image-manifest.js' 'line 74' 'line 69' 'cd2b543' '48c7676' \
         '15f6e1debe3ac6c5' 'def3ac7e654fdacd' 'buildIdentity.js' '--env-file' '--network none' '--target build' 'nexusai:gate24-065a0d8' 'nexusaidevacrfa39' 'az account show' \
         'servicePrincipal' 'rd848-cand-b2fc9bf' 'nexusaireleaseacr' 'NEXUSAI_LOCK_BASE' 'T9' 'WRONG 1' 'WRONG 4' 'WRONG 6' 'WRONG 9' 'WRONG 11' 'MEASURED' 'READ-ONLY-INFERRED' \
         'qa-floorlib23.sh' 'HOLD23.sh' 'qa-file23.sh' 'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae' 'claude-opus-5-5' \
         'Node v26.8.1' "node-version: '24'" 'load of **40**'; do
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
[ "$NEG_BUILDERS" -ge 1 ] || { echo "REFUSING: no live builder seat among Datasec/NexusAI-M/N/O/P/R — at least ONE negative control is required" >&2; exit 38; }
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

# 86 — no live gate-24 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 24 is live; do not start a second session" >&2; exit 86; fi
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
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7}; RD-848 $A_HEAD; lock tool sha256 ${INST_NOW:0:12}…; docker server $DSV; model $MODEL" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$READY_OK" = "1" ] || echo "REFUSING (31R): the READY was read from QA_READY_OVERRIDE ($READY_A) — launch without the override" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): $NSTAMP stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T7) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin: $A_BRANCH = $A_HEAD at $PIN_TS (18; $LSR_ATTEMPTS ls-remote attempt(s), C-192); main ${M_ORIGIN:0:7} (17fc6c5 or a descendant; no Dockerfile/.dockerignore/package move; head not on it) (18b)"
  echo "  lock tool 3c33f5ae… pinned; default base = T9, present; both queues read, no qa-g24 ticket (90, 41)"
  echo "  delta four files, one Dockerfile non-comment change (22); premises + line pins + health formula (93); blobs + counts + census (98); rulings (70); docker $DSV + az packer (70D)"
  echo "  evidence + gate 23 instruments (31); MODEL RULE (82); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: $MODEL at exec (from models_latest.json)"
  echo "  SUBJECT: $SUBJECT"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/$A_BRANCH = $A_HEAD; refs/heads/main = $M_ORIGIN (17fc6c5 or a descendant; no Dockerfile, .dockerignore or package move since 17fc6c5; the head not on it). The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin; its default base is the T9's $LOCK_BASE_T9 (present) and NEXUSAI_LOCK_BASE is unset in your environment. Docker server $DSV answered. These are the start-of-gate pins; take your own three readings anyway, and re-pin M0 yourself.
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
