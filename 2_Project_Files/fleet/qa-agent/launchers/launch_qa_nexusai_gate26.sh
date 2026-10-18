#!/bin/bash
# launch_qa_nexusai_gate26.sh — cross-project QA agent, ONE gate on Datasec/NexusAI (gate 26): a TIER-1 RE-GATE AS MERGED of C-170 / RD-460
# (the released 2.2.1 package files into main) on today's main — one merged tree, one verdict, a SHIPPED-TEXT answer, ONE report
# (drafted 2026-10-18 from ~13:55 AEDT by a read-only drafting agent for Tuesday; the drafter ran only bash -n and --check).
# A FRESH gate on the Mac mini, /Volumes/Laptop-DEV; the T9 is UNMOUNTED, so the lock base is the Laptop-DEV locks-laptop-1017.
#   C-170 / RD-460 rd-460-pkg-into-main-s84m @ be0fe37 (gate 5b GO WITH FINDINGS) AS MERGED onto main c7ca0ed   -> M170 tree 0f4602e
#   The seat's merge commit 88153c0 is a detached worktree HEAD: the gate REBUILDS the tree in its own store.
#
# LAUNCHED ONLY VIA: cockpit.sh add 'QA/NexusAI-gate26' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate26.sh'"
#   (i.e. /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh). A tmux pane, NEVER nohup, never run it bare from a seat's shell.
#
# AUTHORITY: Tuesday's gate-26 drafting commission (2026-10-18) and her ANSWER-7 to S101O ("Tuesday commissions ONE tier-1 re-gate for it").
# THE MODEL RULE: Kam, live board 2026-09-30 09:07, card nexusai-gate11-opus55-safeguard-model-switch, option (b), PER SESSION.
# Carried rulings (sqlite3 cached prebuild; full verifies UNBELTED; npm_config_update_notifier=false; ruling (b) + EXTENSION; C-190 + ADDENDUM;
# C-209; C-141 ADDENDA 6/7; the by-hand gate yield RETIRED; C-216 (C-170's three rulings); the load-8 rule; the Laptop-DEV lock base).
# FINDINGS-ONLY: never merges (outside its own store), never pushes, never opens/comments/approves/updates a PR, never dismisses an alert, never
# swaps or edits the lock tool, the C-57 runner, the C-133 tool or the package build; no fix, no deploy, no az, no docker, no demo, no human.
#
# PATTERN: launch_qa_nexusai_gate25.sh (prompt EMBEDDED, --check mode, PIN-table parser, pin guards with the C-192 retry, THE MODEL RULE,
# the LIVE negative-control seat derivation 38R, stamp + route guards last). CHANGES, each deliberate:
#   - 40: ONE head (RD460) and ONE merged tree (M170) in the brief's tables.
#   - 22: the 34 gated paths; both-sides = the counts file only; main's 121.
#   - 93: the BUILD's inputs unchanged by main; the image guards' inputs changed by main; the build's two registry requests; arm-ttk.yml;
#         deploy-demo's paths-ignore; the shipped-text provenance chain (0677388, the clean-tree rule).
#   - 95 (new): the 2.2.1 reference dir pinned by sha256.
#   - no server, no socket ledger, no docker, no az; the READY is read from briefs/ (the drafter saved it there).
#   - READY path overridable by QA_READY_OVERRIDE_170 (drafter's --check only; the launch refuses with it set).
#
# Identity: exports NexusAI's OWN az/gh dirs (az is NOT used; gh READ-ONLY); CLAUDE_CONFIG_DIR pinned to Tuesday's store.
# --check is READ-ONLY in NexusAI: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote, rev-list, ls-tree); shasum / bash -n /
# grep over session-tools files; python over `git show` output; ls, ps, tmux list-panes, test -e. Writes nothing.
# ABSOLUTE PATHS ON PURPOSE. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_gate26.sh [--check]
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
TBRIEFS="$TUE/2_Project_Files/tuesday/briefs"
BRIEF="$BRIEFS/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md"
BRIEF22="$BRIEFS/2026-10-13_nexusai-gate-batch22.md"
BRIEF23="$BRIEFS/2026-10-16_nexusai-gate-batch23.md"
BRIEF24="$BRIEFS/2026-10-17_nexusai-gate24-rd848.md"
BRIEF25="$BRIEFS/2026-10-18_nexusai-gate25-rd761-rd794-merged.md"
BRIEF5B="$BRIEFS/2026-09-27_nexusai-gate-batch5b-c170pkg-rd696-rd594.md"
V5B="$STAGED/2026-09-28_nexusai_M_batch5b_verdict.md"
ADD25="$TBRIEFS/2026-10-18_gate25_ADDENDUM-1_ref-order.md"
READY_170="${QA_READY_OVERRIDE_170:-$BRIEFS/2026-10-18_nexusai-c170-merged-READY-mail.txt}"
READY_SHA='0e479fd5db4d87401cf7030edd1085bd6d7f3b4482fee3c14c6846e3be9c9ea3'
ANS1="$TBRIEFS/2026-10-18_S101O_ANSWER-1_plan-confirmation.md"
ANS7="$TBRIEFS/2026-10-18_S101O_ANSWER-7_c170-ready-three-rulings.md"
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
S101="$ST/s101"
REF_DIR="$ST/s84m/pkg-build-final-be0fe37"
S81J="$ST/s81j"
S78G_ACC="$ST/s78g/c57-accounting.txt"
LOCKTOOL="$ST/nexusai-lock.sh"
C57TOOL="$ST/c57-id-superset.sh"
C133TOOL="$ST/s78g/c133-accounting.py"
LOCK_SHA_INST='3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792'   # RD-821 round 3, INSTALLED — PINNED
C57_SHA='1ae84a1083348be3acbd421e595af262f74260bf92c1eb822757fc7363125581'         # RD-837 r2 — PINNED
C133_SHA='6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f'        # RD-658 — PINNED
T9_VOL='/Volumes/KK_T9_External_HDD'
LOCK_BASE_LAPTOP="$ST/locks-laptop-1017"
LOCKQ_J="$LOCK_BASE_LAPTOP/queue-jest"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
RPTS="$QA_DIR/projects/nexusai/reports"
B24_DIR="$RPTS/2026-10-17-gate24-rd848"
B24_REPORT="$B24_DIR/report.md"
B24_INST="$B24_DIR/evidence/inst"
REPORT="$RPTS/2026-10-18-gate26-c170-be0fe37-merged/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-gate26'
PEER_GATE='QA/NexusAI-gate25'
NPM_CACHE="${HOME}/.npm/_cacache"
PREBUILD="${HOME}/.npm/_prebuilds/0068db-sqlite3-v5.1.7-napi-v6-darwin-arm64.tar.gz"
PREBUILD_SHA='84a34404b12ff212adbca70eff76c2e4dd83b91245eed0b4569438f928567afc'

# ---- the pins (cross-checked against the brief's two tables, guard 40)
MAIN_SHA='c7ca0ed7113750b268028f12e8659bf1e3d34282'      # origin main at drafting (13:55:49 AEDT) = PR #90 (RD-828 s2)
B460='rd-460-pkg-into-main-s84m'
H460='be0fe3704023d8f092da0be27f79b82fbc029085'
MB460='1904765007e9447ac6c980f9840c0689a02abe6c'
N460=1
SM170='88153c09155feb1eaf29ea2c0f18c5039cc64c9b'; T170='0f4602e01faecebf9cffb207da40144702445919'; CB170='fc7937bca42ab0f1151ee2154210a28fc0cd5b8d'
IMG_SRC='0677388ab031ffaf569a52f6c0301af48f44aece'          # BUILD_COMMIT_SHA of the 2.2.0 image (= the 2.2.1 image)
REL221='3f79e9c'                                           # the 2.2.1 package commit (arm-ttk.yml as released)
IMG_DIGEST='sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66'

COUNTS_FILE='scripts/verify-expected-counts.json'
PKG='package.json'; PKG_BLOB='384805d9e286718bb34ffd05be01c62c00806cf5'; PKG_BASE='cdb1168'
LOCK='package-lock.json'; LOCK_BLOB='19477a9329f17e529c208d91d172b95b47fc1bb5'; LOCK_BASE='9064763'
DEPLOY_WF='.github/workflows/deploy-demo.yml'; DEPLOY_BLOB='953b2a2f84e8710bea857ec87c6f00faa50fa56b'
ARMTTK='.github/workflows/arm-ttk.yml'; ARMTTK_BLOB='80b95b83e80e447b2d6c13f9e665e6e8dd56e0e7'
BUILD_SH='scripts/marketplace-package-build.sh'
MT='azure-marketplace/combined/mainTemplate.json'; CUI='azure-marketplace/plans/managed-ai/createUiDefinition.json'; VD='azure-marketplace/combined/viewDefinition.json'
POL='azure-marketplace/release-policy.json'; LST='azure-marketplace/listing-assets.txt'
GATED_460='.github/workflows/arm-ttk.yml DEPLOYMENT_GUIDE.md README.md __tests__/dev-scripts-template-parameters.test.js __tests__/helpers/shipped-plan-build.js __tests__/listing-folds-rd465-rd454.test.js __tests__/marketplace-keyvault-durability.test.js __tests__/marketplace-package-build.test.js __tests__/marketplace-setup-checks.test.js __tests__/marketplace-single-build-path.test.js __tests__/marketplace-template-log-analytics-enabled.test.js __tests__/rd461-self-contained-and-template-toolkit.test.js __tests__/rd471-wizard-image-element-types.test.js __tests__/rd472-image-bearing-resources.test.js __tests__/rd503-r2-doc-claims-against-product.test.js __tests__/rd630-armttk-ci-workflow.test.js azure-marketplace/combined/README.md azure-marketplace/combined/mainTemplate.json azure-marketplace/listing-assets.txt azure-marketplace/plans/README.md azure-marketplace/plans/managed-ai/createUiDefinition.json azure-marketplace/release-policy.json azure-marketplace/submission-readiness-checklist.md docs/HOSTING_AND_COST_ANALYSIS.md docs/MARKETPLACE_TEST_PROCEDURE.md docs/REFERENCE_ARCHITECTURE.md docs/marketing/MARKETPLACE_LISTING_CONTENT.md scripts/arm-ttk-check.sh scripts/build-plan-packages.sh scripts/deploy-dev.sh scripts/marketplace-package-build.sh scripts/provision-customer.sh scripts/validate-marketplace-template.sh scripts/verify-expected-counts.json'
NEG_SEATS=''   # 38R: DERIVED at launch from the live cockpit panes — never stamped by hand

SUBJECT='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 26'
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
STATUS_SUBJ='[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch'
PARK_LINE='PARKED: flagged — awaiting the Opus 4.8 switch'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-gate26] ANSWER'
NOTTESTED_LINE="Not tested by this gate: CodeQL and the CI Build on the merged tree (no pull request carries one; Tuesday reads them at landing), CodeQL (actions) on arm-ttk.yml (never analysed), arm-ttk itself (no pwsh on this machine), the full jest suite on Node 24 (every run used this machine's Node 26.8.1), npm audit against the merged tree (the lockfile is byte-identical to main's), any image built from the merged tree, the released image beyond the one layer read for the shipped guides (if ruled), a deployment of the package to Azure, Partner Center, the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), the gate 5b report and its section 9.9 table (on the unmounted T9), the zip-container digests (entries carry the extract time, C-216), the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows."
SAFE_PRINTER='if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi'

g() { git --no-optional-locks -C "$REPO" "$@"; }
counts_blob() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
counts_at() { counts_blob "$(g rev-parse --verify -q "${1}:${COUNTS_FILE}" 2>/dev/null)"; }
blob() { g rev-parse --verify -q "${1}:${2}" 2>/dev/null; }
b7() { blob "$1" "$2" | cut -c1-7; }
cntF() { g show "${1}:${2}" 2>/dev/null | grep -cF -- "$3"; }
lineat() { g show "${1}:${2}" 2>/dev/null | sed -n "${3}p"; }
ntests() { g ls-tree -r -z --name-only "$1" -- __tests__ 2>/dev/null | tr '\0' '\n' | grep -c .; }
fsha() { shasum -a 256 "$1" 2>/dev/null | cut -d' ' -f1; }
lockver() { g cat-file -p "$1" 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)["packages"].get("node_modules/"+sys.argv[1],{}).get("version",""))' "$2" 2>/dev/null; }
both_sides() { comm -12 <(g diff --name-only "$1" "$2" 2>/dev/null | sort) <(g diff --name-only "$1" "$3" 2>/dev/null | sort) | tr '\n' ' ' | sed 's/ $//'; }
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

You are the fleet QA/testing agent running ONE gate on Datasec/NexusAI, gate 26: a TIER-1 RE-GATE AS MERGED of C-170 / RD-460 on today's main, with one merged tree, one verdict, a SHIPPED-TEXT answer for Tuesday and ONE report. It is a FRESH gate on Kam's Mac mini, working volume /Volumes/Laptop-DEV; the T9 drive is UNMOUNTED, so the project's jest lock lives on this drive's locks-laptop-1017 base. The head: rd-460-pkg-into-main-s84m at be0fe3704023d8f092da0be27f79b82fbc029085, ONE commit over base 1904765 that COPIES the released 2.2.1 Marketplace package files, and what main needs to build and check them, onto main (C-170 option (b)); gate 5b GO WITH FINDINGS on that head on 2026-09-28. Main has moved 304 commits since, so Tuesday ruled a re-gate AS IT WOULD LAND: M170 = be0fe37 merged with main c7ca0ed7113750b268028f12e8659bf1e3d34282 (pinned tree 0f4602e01faecebf9cffb207da40144702445919, the seat's local commit 88153c0, counts conflict only). The builder's merge commit exists only as a detached worktree HEAD in the project's object store: you REBUILD the merged tree yourself in your own store and PROVE its id; never trust the seat's trees, logs or tables as the proof. FINDINGS-ONLY: you NEVER merge anything the fleet can see, NEVER push, NEVER open, comment on, approve or merge a pull request, never dismiss an alert, and NEVER swap, copy over or edit the installed lock tool, the C-57 runner, the C-133 tool or the package build script; no fixes, no deploys, no az, no docker, no production, no HTTP to any production or demo host, nothing to Partner Center, the demo or any human, no browser, no host npm registry, and no zip ever leaves your dirs (C-23). One client only: Datasec/NexusAI.

READ YOUR COMMISSION FIRST, whole: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md
It opens with the PIN-HEADS and MERGE-PINS tables, the TIER argument and the drafter's WRONG OR UNVERIFIED list (each item MEASURED or READ-ONLY-INFERRED), then TUESDAY'S RULINGS (T1 to T9 as Tuesday stamped them, the commission's properties, the carried rulings) and THE MODEL RULE: apply them, do not re-rule them. Then the charter it names; the READY mail it names, read WHOLE; Tuesday's ANSWER-7 to the builder and C-216 (her three rulings, at source); the clarifications it names at source (C-216, C-170, C-138, C-57, C-133 and C-190 first); Tuesday's batch 5b verdict and the gate 5b kit; gate 25's ADDENDUM-1 (the ref order); gates 22, 23, 24 and 25's section 3a (the H-rules, carried by reference); and gate 24's report on THIS drive (the structural template and the instrument source). The gate 5b report and its section 9.9 table are on the unmounted T9: NOT READ, named; T2 rules the substitute. Every builder statement is a CLAIM — RELAYED, never evidence. The brief's section 2a rows r0 to r10 (with r5b), section 2b (how the package build works, so the build row can fail on the right thing) and section 2c (the per-id accounting of all 24 ids) are required measurement.

THE MODEL RULE (Kam, live board 2026-09-30 09:07, card (b)): QA gates may switch to Opus 4.8 when flagged by Opus 5.5's safeguards, PER SESSION. You start on Opus 5.5. You run the FULL rows. If one of your responses is stopped by the safeguards: that step is NOT RUN (never re-worded to slip past); write ONE line to evidence/classifier-stops.txt; let any running step finish and let the hold exit so you never sit holding a lock (H-28); mail tuesday-agent@agentmail.to with the subject exactly "[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch"; then end your turn with the line "PARKED: flagged — awaiting the Opus 4.8 switch" and wait. Tuesday switches THIS pane's model and taps you by mail. You never answer the model dialog yourself, and nobody ever chooses "Switch automatically". After the switch, resume at the stopped row. The report states which rows ran on which model, with the switch time, and quotes classifier-stops.txt whole.

THE PROPERTIES (brief sections 2a to 2c). (1) THE TREE ROW r1: in your own --mirror store (T6: only a mirror carries the head, which the NexusAI repo names only under refs/remotes/t9-drive-2026-10-15, and removing origin from a mirror drops every refs/remotes ref, so create your g26 refs FIRST, then remove origin, then prove each), git merge-tree --write-tree of c7ca0ed and be0fe37 must conflict in scripts/verify-expected-counts.json ONLY; your raw merge tree must differ from the pin in that path only (its id depends on how you spell the arguments, so it is never a pin); with the seat's counts blob substituted, write-tree must equal the pin; your own full verify passing on that tree is the counts file's assertion; positive control first (your method on c7ca0ed's own merge) and a negative control (another counts blob gives another id). (2) THE INTERACTION ROW r2: does anything main changed since 1904765 (121 files) touch what the package build or the image guards READ — by INPUT, not by file name. Read the build script at the merged tree and list every input and tool; read each of set A's image guards and list every file it reads, through its helpers; the drafter measured that main changed none of the build's inputs but DID change the Dockerfile, .dockerignore and the guards that judge the head's new README.md and DEPLOYMENT_GUIDE.md, so the plants of T8 must turn those guards red on the merged tree. (3) THE GUARD ROW r3: set A's ten image guards BY NAME on the merged tree (image-content-exposure, rd418-dockerignore-round3, rd385-shipped-root-markdown-identifiers, rd698-mixed-encoding-file, rd699-decode-branches-behaviour, rd403-first-run-no-publisher-identifiers, rd477-customer-leftovers, marketplace-package-build, marketplace-single-build-path, rd630-armttk-ci-workflow) plus the head's other suites, with red proofs. (4) THE BUILD ROW r4: C-170's acceptance — run scripts/marketplace-package-build.sh 2.2.1 from a git archive extraction of YOUR merged commit (rc 0, "MANIFEST COMPLETE: 32 checks, 0 failed") and the same script against c7ca0ed (it refuses, 15 FAILs, no zip), each into a fresh empty out-dir, with a curl shim on PATH recording every request; compare the merged build to the 2.2.1 reference MANIFEST and zips by C-216's rule (every [PASS] check line, the three blob sha256s, the image line, both zip byte counts and every zip ENTRY byte-identical; the zip-container digests are the named limit). The build makes TWO anonymous requests to nexusaireleaseacr.azurecr.io (the token GET and the manifest GET), not one; they are allowed and recorded, nothing else is; never set MKT_ANON_PULL_PROBE for the acceptance run (a stub would forge the HTTP 200 line). (5) THE SUITE ROW r5: the full verify on the merged tree, names as SETS vs main; r5b — C-57 through a byte-identical COPY of the installed runner with C57_ROOT pointing at your own shim (T1), C-133 through a copy of the installed tool, every one of the 24 ids classified per section 2c under C-216: the 5 main-side (B blob = base, merged = main's byte for byte, new titles PRESENT and PASSED, the image-content-exposure 2 -> 4 rewrite named) and the 19 head-side (A blob = base, merged = the head's, paired as T2 rules); anything else is a STOP. (6) THE SHIPPED-TEXT ROW r6, for Tuesday: are README.md and DEPLOYMENT_GUIDE.md at be0fe37 byte-equal to what the released 2.2.1 image ships? The drafter's read-only chain says the image was built from main-line commit 0677388, which carries main's text, so probably NOT; T4 rules whether you read the image's markdown layer anonymously by curl (no docker, no az) or re-measure the chain only. Not equal is not your finding: it is Tuesday's word-pack trigger. (7) THE WORKFLOW ROW r7: arm-ttk.yml read for Tuesday's landing checklist (permissions, expressions, pins, triggers, required or not; CodeQL has never analysed it; arm-ttk itself NOT RUN, no pwsh). (8) THE DEPLOY ROW r8: deploy-demo must SKIP on landing — this merge changes paths its paths-ignore does not cover, so the push STARTS it, and only the two if: conditions on vars.CI_DEPLOY_ENABLED keep it from deploying; read the variables (T3) and the last Deploy demo runs. (9) THE AUDIT ROW r9: the merged tree carries main's lockfile 19477a9 and package.json 384805d, proxy-addr 2.0.8. (10) THE SECRETS ROW r10: gitleaks 8.30.1 over the gated range, your merge, an archive extraction of the merged tree and the build's out-dir, after a planted throwaway string is found first; never print a value. Plus r0 scope and pins.

MAIN MUST NOT MOVE (ruling b): the launcher verified origin main = c7ca0ed exactly; take M0 by git ls-remote at YOUR start and say so. If main moves mid-gate (gate 25's members are the likeliest movers), the merged tree is stale: name what landed, finish nothing that would read as a verdict on the new main, and mail a QUESTION (C-68). GitHub SSH intermittently denies auth (C-192): retry every ls-remote up to 5 times about 10 s apart; a FAILED ls-remote is UNKNOWN, never a value. Re-hash the lock tool, the C-57 runner and the C-133 tool at start, mid and end.

C-190 + its ADDENDUM — BOTH thresholds block: every merge to main goes through a pull request that adds no new high-or-higher CodeQL alert in changed code (test code included), AND any new alert whose RULE severity is error blocks whatever its security severity. Alerts are fixed in code, never dismissed. C-209: a PR's CodeQL run cannot show a pre-existing main alert as fixed. No PR carries the merged tree or be0fe37: CodeQL is NOT RUN on any merged tree, CodeQL (actions) has never seen arm-ttk.yml, and the CI Build is NOT RUN — say so, and state (never resolve) the seat's note that lands are deploy-key pushes. C-185 (ruling h): read its known set at source; any other failure is by NAME; no re-run is a clearance.

THE LOCK (C-63). The installed tool is session-tools/nexusai-lock.sh in the NexusAI project on this drive, sha256 3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792. While the T9 is unmounted the base is NEXUSAI_LOCK_BASE=/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/session-tools/locks-laptop-1017, which the launcher has EXPORTED into your environment: keep it on every jest step, quote the c57 runner's resolved LOCK_BASE= and ROOT= line, and never touch this drive's stale session-tools/locks (a 2026-09-22 holder lives there). If the T9 mounts mid-gate, finish the running hold, file nothing more, and mail a QUESTION. EVERY jest run goes in the jest lock, each hold tagged qa-g26- (no tag of yours contains the word "merge": C-141 ADDENDUM 7), ONE hold at a time. MERGES GO FIRST and RULING (i)'s BY-HAND GATE YIELD IS RETIRED: if a ticket is queued ahead of you, wait behind it (FIFO) — the builder S101O and the peer gate QA/NexusAI-gate25 are live and file jest holds on the same base. AT A WAIT DEADLINE: --replace on your own still-waiting ticket BEFORE its deadline fires (C-141: a SAME-PLACE handover), confirmed from the queue listing (the old ticket to released/ as ticket-left-*, your place unchanged); a duplicate-tag refusal takes a -r<N> suffix. Read queue-jest at start, around every hold and at end; any qa-g26- entry that is not your current hold is a STOP. Read your inbox before filing every new hold. THE LOAD RULE: file a hold and start any full jest only below a 1-minute load of 8 (8 cores; Tuesday's ANSWER-1 to S101O).

NODE_MODULES WITHOUT THE HOST REGISTRY (ruling m, H-31): offline npm ci --offline --ignore-scripts --no-audit --no-fund with --cache pointing at an APFS clone of the local npm cache on the same volume; EVERY npm invocation carries npm_config_update_notifier=false (prove the cache copy's _update-notifier-last-checked marker absent or unchanged); an ENOTCACHED is NOT RUN, named, with a QUESTION — never go online from the host, never npm install. sqlite3's binding from the cached prebuild (an APFS clone of ~/.npm/_prebuilds), inside the strict belt, IS PART OF H-31, with its three conditions (the tarball's and the unpacked node_sqlite3.node's sha256; CI builds its own Linux binding; every row that needs it names "sqlite3 binding: cached prebuild, offline"). proxy-addr must resolve 2.0.8 from the merged tree's own path (RD-827, C-205). The C-57 runner does its own offline npm ci per worktree: that is its method, recorded, and its B-side install of be0fe37 uses base's lockfile — never read as the merged tree's.

FULL VERIFIES (r5) through the jest lock, UNBELTED by Tuesday's 2026-10-05 answer to gate 14 (ruling n), with its four conditions. SESSION_SECRET UNSET, npm_config_update_notifier=false npm run verify -- --maxWorkers=2 --forceExit (prove the flag reached jest), Node v26.8.1 as T5 rules. RULING (b) and its EXTENSION (ruling o): if the verify stays lock-starved about 2 h after filing, deliver it NAMED NOT RUN — never "skipped" — with the brief's coverage sentence in NOT TESTED. The TREE, INTERACTION, GUARD and BUILD rows are NOT covered by that extension: they run, and a TIER-1 verdict whose tree, interaction, guard or build row did not run is PROVISIONAL and releases nothing. A plant or mutant counts only if it LANDED (the exact mutated text present, the original absent) and parses; a red from a plant that never landed is a VOID arm, a planted control that does not fire makes its row VOID (never a pass), and an edit whose anchor is absent fails loudly and nothing downstream runs on that tree.

THE INSTRUMENT RULES H-1 TO H-35 (brief section 3a; gates 22, 23, 24 and 25's section 3a read WHOLE). H-1: the ONLY SESSION_SECRET printer is the one the brief quotes; self-test it and gate 24's scan. H-3: a LANDING CONTROL for every plant and mutant. H-4: the HEARTBEAT is a separate child of the hold wrapper, aborted if absent 90 s after the grant, max gap reported. H-6: every path with a space quoted; every host jest run but the full verify, and every driver, under your copy of the belt with its landing control; the merged package build is the ONE unbelted networked step. H-9: byte plants by Buffer, checked with xxd. H-11/H-18: /bin/bash explicitly, "${sha}:${path}" quoted (zsh eats :s and :a). H-17: censuses by pgrep, never ps. H-20: a per-step hard DEADLINE on every jest run (with --forceExit), the runner invocation, every npm ci, every package build and every registry request (qa-to.sh). H-21: every file you mutate is restored by a trap on EXIT (also INT and TERM) installed BEFORE the first mutation. H-22: never nest sandbox-exec (it exits 71). H-24: jest array options after the paths, lists built in bash. H-26: C-192 retries. H-27: THE MODEL RULE. H-28: ONE focused hold at a time, at most about 40 minutes planned (T1's runner hold excepted), rows GROUPED, a hold that would overrun SPLIT, every part file bash -n checked before filing; you stay in the FOREGROUND — a hold that must outlive one tool call runs as a TRACKED child of your session (never nohup) with its timeout at the 2-hour maximum; each hold carries a wait deadline and you --replace before it fires. H-29: other gates' and the builder's evidence is method only. H-31: offline host node_modules. H-32: no server is booted; no HTTP to any production or demo host. H-33: never rm — quarantine (T1's and T7's disclosed tool exceptions only); every child reaped by pid. H-34: the Laptop-DEV lock base. H-35: NO docker object and NO az command, not even az version; the image is read by curl only, if T4 rules it.

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT (fresh mktemp dirs under projects/nexusai/qa-trees/gate26.* in /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN): ONE --mirror clone of the NexusAI repo on THIS drive as your store (T6), your refs g26/* in it made BEFORE origin is removed, your merge commit in it, every work tree a clone of that store, status-checked before use, EXCLUSIVE to one purpose. NEVER work in the NexusAI root checkout or any worktrees/ folder (LIVE, the builder's: read the seat's merge commit BY SHA only). In the NexusAI repo use ONLY read verbs (show, diff, log with an explicit rev, ls-tree, cat-file, grep, ls-remote, rev-parse, merge-base, rev-list, count-objects, for-each-ref); NEVER fetch, pull, push, checkout, worktree, commit, stash, gc, merge, merge-tree --write-tree or hash-object -w there. Copy instruments BY NAME from gate 24's evidence/inst on THIS drive (never the whole directory), re-point every gate-24 path in your copies to gate 26 — INCLUDING the lock base line, which gate 24's copies UNSET for the T9 and yours set to the Laptop-DEV base (quote that diff) — and correct the floor library's ROOT and NEG defaults from the live list below; never write into another gate's dirs on either drive (gate 25's report and qa-trees are LIVE). Never write into the builders' session-tools (S101O is live in s101/: hash it at start and end) or the 2.2.1 reference dir session-tools/s84m/pkg-build-final-be0fe37; never run the seat's scripts in place. Findings-only: never push, no commits outside your store, no tickets, no PRs, no edits in NexusAI. No Microsoft login host, no CDN, no demo, no Partner Center, no workflow dispatch, no repo variable written. No mail to any human, no zip attached to any mail. Never rm: quarantine.

FLOOR DISCIPLINE — section 9 of the brief exactly. Do ALL lock-free work first (pins, hashes, reads, r0, r1's rebuild and its controls, r2's reading halves, r4's two builds, r6 to r10, the offline npm ci, the belt self-tests); then file your holds one at a time through your COPY of gate 24's qa-file24.sh re-pointed to qa-g26 tags and the jest kind. QUEUE, NEVER TAKE OVER: never signal, move or edit another seat's or gate's process, lock, ticket or worktree. Count foreign servers the C-125 way anchored on YOUR OWN claude pid, with the negative-control seats the launcher derived (listed at the end of this prompt) classifying foreign in the same run; re-derive them at every hold's start; a hold with no live negative control aborts. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every step has a per-step DEADLINE, every child is killed in a finally by pid from your own ancestry (C-174, never by pattern), a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

RE-PIN at start, mid and end: main and the branch rd-460-pkg-into-main-s84m, plus the three tools' sha256 — three timestamped readings with the branch name and attempt count beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. Call main at your start M0 and say so. Count the NexusAI .git/objects files and their newest mtime at start and end and account for any delta.

QUESTIONS: your routing name is QA/NexusAI-gate26. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting (the one exception is a safeguards stop, which PARKS you under THE MODEL RULE); Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-gate26] ANSWER". Approval-class items (anything Azure beyond the anonymous registry reads ruled here, the demo, Partner Center, money, a human, the live lock tool) are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your ONE report to: /Volumes/Laptop-DEV/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-10-18-gate26-c170-be0fe37-merged/report.md
Write its VERDICT and FINDINGS table early and keep it current. Findings are G26-<n>, notes N26-<n>, each naming its instrument and evidence class.

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with the subject exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 26
Lead the body with the THREE lines in the form the brief's section 11 gives — C-170 AS MERGED (with its TREE, INTERACTION, GUARDS, BUILD, VERIFY, C-57, C-133, C-216(1), ARM-TTK, AUDIT, DEPLOY-DEMO and GITLEAKS clauses), SHIPPED TEXT, and LANDING CHECKLIST — then one line naming M0 and END main, the C-102 sweep, which rows ran on Opus 4.8 (or none), which holds ran and which are NAMED NOT RUN under ruling (b) extended, and "CodeQL NOT RUN on any merged tree (no PR carries one)". The report's last three lines are those same three lines. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/Laptop-DEV/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key, a token, a signed URL, a session value or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice — the only turn you end while waiting is the PARKED line of THE MODEL RULE.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section carrying the builder's stated limits, every declared limit L-B1 to L-B8 and L-Y1 discharged with a measurement or left standing and named (C-112), Prior work checked (C-49), every finding naming its instrument, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. Severity is yours; priority is Tuesday's. The tester never fixes. C-216, C-170, C-138, C-23, C-57, C-133, C-190 with its ADDENDUM, C-209, C-185 with its ADDENDA, C-192, C-205, C-141 with ADDENDA 6 and 7, C-63, C-40, C-68, C-76, C-102, C-112 and C-174 are the clarifications this gate leans on; C-49, C-89, C-115, C-125, C-130, C-131, C-151 and C-203 are carried. That section must carry this line verbatim:
Not tested by this gate: CodeQL and the CI Build on the merged tree (no pull request carries one; Tuesday reads them at landing), CodeQL (actions) on arm-ttk.yml (never analysed), arm-ttk itself (no pwsh on this machine), the full jest suite on Node 24 (every run used this machine's Node 26.8.1), npm audit against the merged tree (the lockfile is byte-identical to main's), any image built from the merged tree, the released image beyond the one layer read for the shipped guides (if ruled), a deployment of the package to Azure, Partner Center, the demo (behind RD-76 SSO) and any deployed revision, a deploy-demo run itself (its skip is read from the workflow condition and the variables), the gate 5b report and its section 9.9 table (on the unmounted T9), the zip-container digests (entries carry the extract time, C-216), the host npm registry (node_modules from an offline cache copy with install scripts skipped and the update notifier off; sqlite3's binding from its cached prebuild), and Windows.
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# MODEL — read from Tuesday's models_latest.json (opus level), never typed from memory; REFUSE unless it is the brief's pin.
MODEL="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["levels"]["opus"]["model_id"])' "$MODELS_JSON" 2>/dev/null)"
[ "$MODEL" = "$MODEL_PIN" ] || { echo "REFUSING: $MODELS_JSON levels.opus.model_id is '${MODEL:-unreadable}', not $MODEL_PIN as the brief states — re-brief" >&2; exit 9; }

# 40 — parse BOTH pin tables from the brief (the ONLY source of heads and trees) and cross-check them against this launcher's pins.
parse_block() { python3 - "$BRIEF" "$1" <<'PY'
import sys, re
s = open(sys.argv[1], encoding='utf-8').read(); name = sys.argv[2]
m = re.search(r'<!-- %s:BEGIN -->(.*?)<!-- %s:END -->' % (name, name), s, re.S)
if not m:
    print('NO-BLOCK'); sys.exit(0)
for line in m.group(1).splitlines():
    line = line.strip()
    if not line.startswith('|') or line.startswith('| id ') or set(line) <= set('|-: '):
        continue
    print('\t'.join(c.strip().strip('`') for c in line.strip('|').split('|')))
PY
}
PIN="$(parse_block PIN-HEADS)"; MPIN="$(parse_block MERGE-PINS)"
[ "$PIN" != "NO-BLOCK" ] && [ -n "$PIN" ] || { echo "REFUSING: the brief has no PIN-HEADS block — the heads have nowhere to come from" >&2; exit 40; }
[ "$MPIN" != "NO-BLOCK" ] && [ -n "$MPIN" ] || { echo "REFUSING: the brief has no MERGE-PINS block — the merged tree has nowhere to come from" >&2; exit 40; }
prow() { printf '%s\n' "$1" | awk -F'\t' -v id="$2" '$1==id'; }
pfld() { prow "$1" "$2" | awk -F'\t' -v n="$3" '{print $n}'; }
is40()  { printf '%s' "$1" | grep -Eq '^[0-9a-f]{40}$'; }
[ "$(printf '%s\n' "$PIN" | wc -l | tr -d ' ')" = "2" ] || { echo "REFUSING: PIN-HEADS must carry exactly two rows (MAIN RD460)" >&2; exit 40; }
[ "$(printf '%s\n' "$MPIN" | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: MERGE-PINS must carry exactly one row (M170)" >&2; exit 40; }
for ID in MAIN RD460; do
  R="$(prow "$PIN" "$ID")"
  [ "$(printf '%s\n' "$R" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || { echo "REFUSING: PIN-HEADS must carry exactly one row '$ID'" >&2; exit 40; }
  [ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "7" ] || { echo "REFUSING: PIN-HEADS row $ID does not have 7 cells: $R" >&2; exit 40; }
  printf '%s' "$R" | grep -q '@' && { echo "REFUSING: PIN-HEADS row $ID still carries a placeholder" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 7)" = "IN" ] || { echo "REFUSING: PIN-HEADS row $ID status is not IN" >&2; exit 40; }
  [ "$(pfld "$PIN" "$ID" 2)" = "nexusai" ] || { echo "REFUSING: PIN-HEADS row $ID repo must be nexusai" >&2; exit 40; }
  is40 "$(pfld "$PIN" "$ID" 4)" || { echo "REFUSING: PIN-HEADS row $ID head is not a 40-hex sha" >&2; exit 40; }
done
[ "$(pfld "$PIN" MAIN 3)" = "main" ] && [ "$(pfld "$PIN" MAIN 4)" = "$MAIN_SHA" ] || { echo "REFUSING: PIN-HEADS MAIN is not main @ c7ca0ed — this launcher's guards are pinned to it; re-brief" >&2; exit 40; }
[ "$(pfld "$PIN" RD460 3)" = "$B460" ] && [ "$(pfld "$PIN" RD460 4)" = "$H460" ] && [ "$(pfld "$PIN" RD460 5)" = "$MB460" ] && [ "$(pfld "$PIN" RD460 6)" = "$N460" ] \
  || { echo "REFUSING: PIN-HEADS RD460 is not $B460 @ be0fe37, base 1904765, $N460 commit" >&2; exit 40; }
R="$(prow "$MPIN" M170)"
[ "$(printf '%s\n' "$R" | awk -F'\t' '{print NF}')" = "8" ] || { echo "REFUSING: MERGE-PINS row M170 does not have 8 cells: $R" >&2; exit 40; }
printf '%s' "$R" | grep -q '@' && { echo "REFUSING: MERGE-PINS row M170 still carries a placeholder" >&2; exit 40; }
[ "$R" = "$(printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' M170 "$H460" "$MAIN_SHA" "$SM170" "$T170" "$CB170" 4706 294)" ] || { echo "REFUSING: MERGE-PINS row M170 is not as this launcher pins it: '$R'" >&2; exit 40; }

# 6 — every sha the guards use is a commit in the local object store (this launcher never fetches).
for S in "$MAIN_SHA" "$H460" "$MB460" "$IMG_SRC" "$REL221"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T') — this launcher never fetches" >&2; exit 6; }
done

# 7 / 8 — the chain: merge base, one linear commit, head not on main; the image source is an ancestor of the base and of main.
[ "$(g merge-base "$H460" "$MAIN_SHA" 2>/dev/null)" = "$MB460" ] || { echo "REFUSING: merge-base(be0fe37, c7ca0ed) is not 1904765" >&2; exit 7; }
if g merge-base --is-ancestor "$H460" "$MAIN_SHA" 2>/dev/null; then echo "REFUSING: be0fe37 is ALREADY on main c7ca0ed — re-brief" >&2; exit 7; fi
[ "$(g rev-list --count "${MB460}..${H460}" 2>/dev/null)" = "$N460" ] && [ -z "$(g rev-list --merges "${MB460}..${H460}" 2>/dev/null)" ] \
  || { echo "REFUSING: RD-460 is not ONE linear commit over 1904765" >&2; exit 8; }
[ "$(g rev-list --count "${H460}..${MAIN_SHA}" 2>/dev/null)" = "304" ] || echo "NOTE: main is $(g rev-list --count "${H460}..${MAIN_SHA}" 2>/dev/null) commits past be0fe37, not 304 as briefed" >&2
g merge-base --is-ancestor "$IMG_SRC" "$MB460" 2>/dev/null || { echo "REFUSING: the image source 0677388 is not an ancestor of the base 1904765 (WRONG 7's premise)" >&2; exit 8; }

# 18T — the T9 MOUNTED refuses: two lock bases would split the FIFO (ruling q); Tuesday decides the base first.
[ ! -d "$T9_VOL" ] || { echo "REFUSING: $T9_VOL is MOUNTED — the brief's lock base (locks-laptop-1017) assumes it is not; Tuesday decides the base, then re-brief" >&2; exit 18; }

# 18 — RE-PIN NOW by ls-remote (C-192 retries): main EXACTLY c7ca0ed; the branch exactly its pin; no PR carries the head (NOTE).
lsr refs/heads/main "refs/heads/$B460" || { echo "REFUSING: git ls-remote origin failed after $LSR_ATTEMPTS attempt(s) — UNKNOWN, not a value (C-192); relaunch later" >&2; exit 18; }
LSR_ALL="$LSR_OUT"
ref_now() { printf '%s\n' "$LSR_ALL" | awk -v r="$1" '$2==r{print $1}'; }
M_ORIGIN="$(ref_now refs/heads/main)"
[ "$M_ORIGIN" = "$MAIN_SHA" ] || { echo "REFUSING: origin main is '${M_ORIGIN:-unreadable}', not c7ca0ed — the merged tree of this gate is ON c7ca0ed; re-brief" >&2; exit 18; }
[ "$(ref_now "refs/heads/$B460")" = "$H460" ] || { echo "REFUSING: origin $B460 is '$(ref_now "refs/heads/$B460")', not be0fe37 — moved (a landing push?); re-brief" >&2; exit 18; }
PRREF="$(g ls-remote origin 'refs/pull/*/head' 2>/dev/null | awk -v h="$H460" '$1==h{print $2}' | tr '\n' ' ')"
[ -z "$PRREF" ] || echo "NOTE: a PR ref now carries be0fe37 (${PRREF}) — the brief says it has no PR; the gate reads it (§8)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 90 — the INSTALLED lock tool PINNED; it honours NEXUSAI_LOCK_BASE; the Laptop-DEV base is present with queue-jest; no qa-g26 ticket.
INST_NOW="$(fsha "$LOCKTOOL")"
[ "$INST_NOW" = "$LOCK_SHA_INST" ] || { echo "REFUSING: the INSTALLED lock tool's sha256 is '${INST_NOW:-absent}', not 3c33f5ae… — find out who changed it; re-brief" >&2; exit 90; }
grep -qF 'BASE="${NEXUSAI_LOCK_BASE:-' "$LOCKTOOL" || { echo "REFUSING: the installed tool no longer honours NEXUSAI_LOCK_BASE — ruling q's premise" >&2; exit 90; }
bash -n "$LOCKTOOL" 2>/dev/null || { echo "REFUSING: $LOCKTOOL does not parse (bash -n)" >&2; exit 90; }
grep -qF -- '--replace' "$LOCKTOOL" && grep -qF 'jest|docker) ;;' "$LOCKTOOL" || { echo "REFUSING: $LOCKTOOL lacks --replace or the jest kind" >&2; exit 90; }
[ -d "$LOCK_BASE_LAPTOP" ] && [ -d "$LOCKQ_J" ] || { echo "REFUSING: the Laptop-DEV lock base $LOCK_BASE_LAPTOP (queue-jest) is not present (ruling q)" >&2; exit 90; }
BQ="$(grep -l '^tag=qa-g26' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${BQ:-0}" = "0" ] || { echo "REFUSING: $BQ qa-g26* ticket(s) already in $LOCKQ_J — a live or stale gate-26 ticket; read before launch" >&2; exit 90; }
MQ="$(grep -lE '^tag=.*(^|[-_=])merge([0-9]+[a-z]?)?([-_]|$)' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${MQ:-0}" = "0" ] || echo "NOTE: $MQ merge-tagged ticket(s) in $LOCKQ_J now — the gate files behind them (brief §9)" >&2
G25Q="$(grep -l '^tag=qa-g25' "$LOCKQ_J"/* 2>/dev/null | wc -l | tr -d ' ')"
[ "${G25Q:-0}" = "0" ] || echo "NOTE: $G25Q qa-g25 ticket(s) queued — the peer gate 25 is ahead in FIFO; gate 26 waits behind it, never touches it" >&2
HOLDER="$(sed -n 's/^tag=//p' "$LOCK_BASE_LAPTOP/nexusai-jest.lock/owner" 2>/dev/null | head -1)"
case "$HOLDER" in
  qa-g26*) echo "REFUSING: the Laptop-DEV jest lock is HELD by '$HOLDER' — a gate-26 holder already exists" >&2; exit 90 ;;
  '') ;;
  *) echo "NOTE: the Laptop-DEV jest lock is held now by '$HOLDER' (FIFO; the gate waits behind it)" >&2 ;;
esac
LB_WAS="${NEXUSAI_LOCK_BASE:-}"
[ -z "$LB_WAS" ] || [ "$LB_WAS" = "$LOCK_BASE_LAPTOP" ] || echo "NOTE: NEXUSAI_LOCK_BASE was '$LB_WAS' in the launcher's environment — REPLACED by the Laptop-DEV base before exec (ruling q)" >&2

# 91 — the C-57 runner and the C-133 tool PINNED, and the runner's ROOT / LOCK_BASE / rm premises that T1 rests on.
C57_NOW="$(fsha "$C57TOOL")"; C133_NOW="$(fsha "$C133TOOL")"
[ "$C57_NOW" = "$C57_SHA" ] || { echo "REFUSING: c57-id-superset.sh sha256 is '${C57_NOW:-absent}', not 1ae84a10…5581 — re-brief" >&2; exit 91; }
[ "$C133_NOW" = "$C133_SHA" ] || { echo "REFUSING: c133-accounting.py sha256 is '${C133_NOW:-absent}', not 6f938bfc…f972f — re-brief" >&2; exit 91; }
grep -qF 'if [ -n "${C57_ROOT:-}" ]; then ROOT="$C57_ROOT"' "$C57TOOL" && grep -qF 'LOCK_BASE="${NEXUSAI_LOCK_BASE:-' "$C57TOOL" \
  && grep -qF 'rm -rf "$wt"' "$C57TOOL" && grep -qF 'worktree remove --force "$wt"' "$C57TOOL" && grep -qF 'OUT="$ROOT/session-tools/c57-$TAG"' "$C57TOOL" \
  || { echo "REFUSING: the C-57 runner's C57_ROOT / LOCK_BASE / rm / worktree / OUT lines are not as T1 describes" >&2; exit 91; }
grep -qF 'usage: c133-accounting.py <c57-out-dir> <base> <A=main> <B=branch> <merged-tree-or-commit> <repo-dir>' "$C133TOOL" || { echo "REFUSING: c133-accounting.py's usage line moved" >&2; exit 91; }

# 22 — the gated file set, the both-sides set, main's count.
[ "$(g diff --name-only "$MB460" "$H460" 2>/dev/null | sort | tr '\n' ' ' | sed 's/ $//')" = "$(printf '%s\n' $GATED_460 | sort | tr '\n' ' ' | sed 's/ $//')" ] \
  || { echo "REFUSING: RD-460's gated files (1904765..be0fe37) are not the briefed 34" >&2; exit 22; }
[ "$(both_sides "$MB460" "$H460" "$MAIN_SHA")" = "$COUNTS_FILE" ] || { echo "REFUSING: the both-sides set is not the counts file alone (got '$(both_sides "$MB460" "$H460" "$MAIN_SHA")')" >&2; exit 22; }
[ "$(g diff --name-only "$MB460" "$MAIN_SHA" 2>/dev/null | grep -c .)" = "121" ] || { echo "REFUSING: main's changed-file count since 1904765 is not 121" >&2; exit 22; }

# 93 — the premises at source (WRONG 3, 6, 7, 8, 9, 12): build inputs, guard inputs, the probe, arm-ttk, deploy-demo, counts, census, locks.
for P in "$MT" "$CUI" "$POL" "$BUILD_SH"; do
  [ "$(b7 "$MB460" "$P")" = "$(b7 "$MAIN_SHA" "$P")" ] && [ "$(b7 "$MB460" "$P")" != "$(b7 "$H460" "$P")" ] \
    || { echo "REFUSING: build input $P is not (base = main) != head — main changed a build input, or the head no longer does (WRONG 6a)" >&2; exit 93; }
done
[ "$(b7 "$H460" "$MT")" = "93ecbca" ] && [ "$(b7 "$H460" "$CUI")" = "6d87b9d" ] && [ "$(b7 "$H460" "$POL")" = "241f983" ] && [ "$(b7 "$H460" "$BUILD_SH")" = "40ec7de" ] \
  && [ "$(b7 "$H460" "$LST")" = "be050c1" ] && [ -z "$(blob "$MAIN_SHA" "$LST")" ] && [ "$(b7 "$MB460" "$VD")" = "c8d5fd5" ] && [ "$(b7 "$MAIN_SHA" "$VD")" = "c8d5fd5" ] && [ "$(b7 "$H460" "$VD")" = "c8d5fd5" ] \
  || { echo "REFUSING: the package input blobs at be0fe37 are not 93ecbca / 6d87b9d / 241f983 / 40ec7de / be050c1 (viewDefinition c8d5fd5 everywhere)" >&2; exit 93; }
NMEDIA=0
while IFS= read -r p; do
  case "$p" in ''|'#'*) continue ;; esac
  NMEDIA=$((NMEDIA + 1))
  [ -n "$(blob "$MB460" "$p")" ] && [ "$(blob "$MB460" "$p")" = "$(blob "$MAIN_SHA" "$p")" ] && [ "$(blob "$MB460" "$p")" = "$(blob "$H460" "$p")" ] \
    || { echo "REFUSING: listed media $p is not the same blob at base, main and head" >&2; exit 93; }
done < <(g show "${H460}:${LST}" 2>/dev/null)
[ "$NMEDIA" = "7" ] || { echo "REFUSING: listing-assets.txt at be0fe37 does not list 7 media files (got $NMEDIA)" >&2; exit 93; }
[ "$(b7 "$MB460" Dockerfile)" = "92022ec" ] && [ "$(b7 "$MAIN_SHA" Dockerfile)" = "f0367f1" ] && [ "$(b7 "$H460" Dockerfile)" = "92022ec" ] \
  && [ "$(b7 "$MB460" .dockerignore)" = "881f0f8" ] && [ "$(b7 "$MAIN_SHA" .dockerignore)" = "3e45ec5" ] && [ "$(b7 "$H460" .dockerignore)" = "881f0f8" ] \
  || { echo "REFUSING: Dockerfile / .dockerignore are not 92022ec->f0367f1 / 881f0f8->3e45ec5 on main only (WRONG 6b)" >&2; exit 93; }
[ "$(b7 "$MB460" README.md)" = "f129ff3" ] && [ "$(b7 "$MAIN_SHA" README.md)" = "f129ff3" ] && [ "$(b7 "$H460" README.md)" = "e23999f" ] && [ "$(b7 "$IMG_SRC" README.md)" = "f129ff3" ] \
  && [ "$(b7 "$MB460" DEPLOYMENT_GUIDE.md)" = "01c7c46" ] && [ "$(b7 "$MAIN_SHA" DEPLOYMENT_GUIDE.md)" = "01c7c46" ] && [ "$(b7 "$H460" DEPLOYMENT_GUIDE.md)" = "3753a82" ] && [ "$(b7 "$IMG_SRC" DEPLOYMENT_GUIDE.md)" = "01c7c46" ] \
  || { echo "REFUSING: README.md / DEPLOYMENT_GUIDE.md blobs at base/main/head/0677388 are not as WRONG 7 states" >&2; exit 93; }
[ "$(cntF "$MAIN_SHA" Dockerfile 'COPY --from=build /app/PRIVACY.md /app/TERMS_OF_SERVICE.md /app/README.md /app/CHANGELOG.md /app/DEPLOYMENT_GUIDE.md ./')" = "1" ] \
  || { echo "REFUSING: main's Dockerfile no longer copies README.md and DEPLOYMENT_GUIDE.md into the production stage (WRONG 6b, r2 M-c's anchor)" >&2; exit 93; }
for f in image-content-exposure rd385-shipped-root-markdown-identifiers; do
  [ "$(blob "$MB460" "__tests__/${f}.test.js")" != "$(blob "$MAIN_SHA" "__tests__/${f}.test.js")" ] && [ "$(blob "$MB460" "__tests__/${f}.test.js")" = "$(blob "$H460" "__tests__/${f}.test.js")" ] \
    || { echo "REFUSING: guard $f is not main-changed and head-unchanged (WRONG 6b)" >&2; exit 93; }
done
[ -z "$(blob "$MB460" __tests__/rd418-dockerignore-round3.test.js)" ] && [ -n "$(blob "$MAIN_SHA" __tests__/rd418-dockerignore-round3.test.js)" ] && [ -n "$(blob "$MAIN_SHA" __tests__/helpers/dockerfile-stages.js)" ] \
  || { echo "REFUSING: rd418-dockerignore-round3 / helpers/dockerfile-stages.js are not main-added (WRONG 6b)" >&2; exit 93; }
BS="$(g show "${H460}:${BUILD_SH}" 2>/dev/null)"
printf '%s\n' "$BS" | grep -qF '/oauth2/token?service=${reg}&scope=repository:${repo}:pull' && printf '%s\n' "$BS" | grep -qF '"https://${reg}/v2/${repo}/manifests/${ref}"' \
  && printf '%s\n' "$BS" | grep -qF 'MKT_ANON_PULL_PROBE' && printf '%s\n' "$BS" | grep -qF "trap 'rm -rf \"\$WORK\"' EXIT" && printf '%s\n' "$BS" | grep -qF 'git -C "$REPO" archive "$SHA"' \
  || { echo "REFUSING: the package build no longer reads as §2b / WRONG 3 describe (two curl requests, MKT_ANON_PULL_PROBE, its own rm trap, git archive)" >&2; exit 93; }
[ "$(printf '%s\n' "$BS" | grep -c 'curl -s -m')" = "2" ] || { echo "REFUSING: the package build does not carry exactly two curl calls (WRONG 3)" >&2; exit 93; }
g show "${MAIN_SHA}:scripts/build-commit-sha.sh" 2>/dev/null | grep -qF 'So a clean tree prints `git rev-parse HEAD`; anything else prints nothing' \
  || { echo "REFUSING: build-commit-sha.sh no longer states the clean-tree rule (WRONG 7 (iii))" >&2; exit 93; }
[ "$(blob "$H460" "$ARMTTK")" = "$ARMTTK_BLOB" ] && [ "$(blob "$REL221" "$ARMTTK")" = "$ARMTTK_BLOB" ] && [ -z "$(blob "$MAIN_SHA" "$ARMTTK")" ] && [ -z "$(blob "$MB460" "$ARMTTK")" ] \
  || { echo "REFUSING: arm-ttk.yml is not 80b95b8 at be0fe37 and 3f79e9c, absent at base and main (WRONG 8)" >&2; exit 93; }
AT="$(g show "${H460}:${ARMTTK}" 2>/dev/null)"
printf '%s\n' "$AT" | grep -qF 'contents: read' && [ "$(printf '%s\n' "$AT" | grep -c '\${{')" = "1" ] && [ "$(printf '%s\n' "$AT" | grep -c 'sha256sum -c')" = "2" ] && printf '%s\n' "$AT" | grep -qF 'uses: actions/checkout@v4' \
  || { echo "REFUSING: arm-ttk.yml no longer reads as WRONG 8 (contents: read, one expression, two sha256 checks, checkout@v4)" >&2; exit 93; }
for S in "$MAIN_SHA" "$H460" "$MB460"; do
  [ "$(blob "$S" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] || { echo "REFUSING: $DEPLOY_WF at ${S:0:7} is not 953b2a2 (r8's premise)" >&2; exit 93; }
done
[ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" "vars.CI_DEPLOY_ENABLED == 'true'")" = "2" ] && [ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" 'branches: [main]')" = "1" ] && [ "$(cntF "$MAIN_SHA" "$DEPLOY_WF" 'paths-ignore:')" = "1" ] \
  || { echo "REFUSING: deploy-demo.yml no longer gates BOTH jobs on vars.CI_DEPLOY_ENABLED == 'true' on push to main with one paths-ignore" >&2; exit 93; }
[ "$(counts_at "$MB460")" = "4133 247" ] && [ "$(counts_at "$H460")" = "4280 254" ] && [ "$(counts_at "$MAIN_SHA")" = "4559 287" ] \
  || { echo "REFUSING: counts are not 4133/247 (base), 4280/254 (be0fe37), 4559/287 (main)" >&2; exit 93; }
[ "$(ntests "$MB460")" = "289" ] && [ "$(ntests "$H460")" = "297" ] && [ "$(ntests "$MAIN_SHA")" = "341" ] || { echo "REFUSING: the __tests__ census is not 289 / 297 / 341" >&2; exit 93; }
[ "$(blob "$MAIN_SHA" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$MAIN_SHA" "$PKG")" = "$PKG_BLOB" ] && [ "$(b7 "$H460" "$LOCK")" = "$LOCK_BASE" ] && [ "$(b7 "$H460" "$PKG")" = "$PKG_BASE" ] \
  && [ "$(lockver "$LOCK_BLOB" proxy-addr)" = "2.0.8" ] \
  || { echo "REFUSING: lockfile / package.json are not 19477a9 + 384805d (main, proxy-addr 2.0.8) and 9064763 + cdb1168 (be0fe37)" >&2; exit 93; }
for f in jsdom-instrument-limits rd327-build-digest-on-public-health image-content-exposure; do
  P="__tests__/${f}.test.js"
  [ "$(blob "$H460" "$P")" = "$(blob "$MB460" "$P")" ] && [ "$(blob "$MAIN_SHA" "$P")" != "$(blob "$MB460" "$P")" ] || { echo "REFUSING: A-side file $f is not head = base != main (C-216(1))" >&2; exit 93; }
done
for f in marketplace-package-build rd461-self-contained-and-template-toolkit rd503-r2-doc-claims-against-product; do
  P="__tests__/${f}.test.js"
  [ "$(blob "$MAIN_SHA" "$P")" = "$(blob "$MB460" "$P")" ] && [ "$(blob "$H460" "$P")" != "$(blob "$MB460" "$P")" ] || { echo "REFUSING: B-side file $f is not main = base != head (C-216(1))" >&2; exit 93; }
done

# 94 — the seat's merged object, read BY SHA (a detached worktree HEAD: if gone, a NOTE — the gate rebuilds and compares to the pin).
if [ "$(g cat-file -t "$SM170" 2>/dev/null)" = "commit" ]; then
  [ "$(g log -1 --format='%P' "$SM170" 2>/dev/null)" = "$H460 $MAIN_SHA" ] || { echo "REFUSING: 88153c0's parents are not be0fe37 + c7ca0ed" >&2; exit 94; }
  [ "$(g rev-parse "${SM170}^{tree}")" = "$T170" ] || { echo "REFUSING: 88153c0's tree is not 0f4602e" >&2; exit 94; }
  [ "$(blob "$SM170" "$COUNTS_FILE")" = "$CB170" ] && [ "$(counts_blob "$CB170")" = "4706 294" ] || { echo "REFUSING: the seat's counts blob is not fc7937b 4706/294" >&2; exit 94; }
  [ "$(blob "$SM170" "$LOCK")" = "$LOCK_BLOB" ] && [ "$(blob "$SM170" "$PKG")" = "$PKG_BLOB" ] && [ "$(blob "$SM170" "$DEPLOY_WF")" = "$DEPLOY_BLOB" ] && [ "$(blob "$SM170" "$ARMTTK")" = "$ARMTTK_BLOB" ] \
    || { echo "REFUSING: 88153c0 does not carry main's lockfile / package.json / deploy-demo.yml and the head's arm-ttk.yml" >&2; exit 94; }
  [ "$(diff <(g ls-tree "$MAIN_SHA" .github/workflows/ 2>/dev/null) <(g ls-tree "$SM170" .github/workflows/ 2>/dev/null) | grep -c '^[<>]')" = "1" ] \
    || { echo "REFUSING: 88153c0's workflows differ from main's by more than the added arm-ttk.yml" >&2; exit 94; }
  [ "$(ntests "$SM170")" = "349" ] || { echo "REFUSING: 88153c0's __tests__ census is not 349" >&2; exit 94; }
  NOTSIDE="$( { g diff --name-only "$MB460" "$H460"; g diff --name-only "$MB460" "$MAIN_SHA"; } 2>/dev/null | sort -u | while IFS= read -r p; do
      [ "$p" = "$COUNTS_FILE" ] && continue
      m="$(blob "$SM170" "$p")"; h="$(blob "$H460" "$p")"; a="$(blob "$MAIN_SHA" "$p")"; b="$(blob "$MB460" "$p")"
      if [ "$h" != "$b" ]; then [ "$m" = "$h" ] || echo "$p"; else [ "$m" = "$a" ] || echo "$p"; fi; done)"
  [ -z "$NOTSIDE" ] || { echo "REFUSING: 88153c0 carries a blob that is neither the changing side's: $NOTSIDE" >&2; exit 94; }
  SEAT_NOTE="seat merge object present: parents, tree, counts, lock, workflows, census and every side's blob as pinned"
else
  SEAT_NOTE="seat merge object NOT in the store (worktree removed?) — the gate rebuilds and compares to the MERGE-PINS"
  echo "NOTE: $SEAT_NOTE" >&2
fi

# 95 — the 2.2.1 reference dir pinned (r4 compares to it; nobody writes to it).
[ "$(fsha "$REF_DIR/MANIFEST-2.2.1_be0fe37.txt")" = 'fc53d1d58b7ef41af5b4309659efc46f247868fa5e8d6467dd854c3d7fe310df' ] \
  && [ "$(fsha "$REF_DIR/NexusAI_plan-managed-ai_2.2.1_be0fe37.zip")" = '621b94b571efdd0b48875ef404d768ef109104f9daf76bc4132af287056294c0' ] \
  && [ "$(fsha "$REF_DIR/NexusAI_listing-assets_2.2.1_be0fe37.zip")" = '0c6f40f0bb01df0252c4eec8d005a6bc38dfd280f65dbd55bb14802d4c3b3ad9' ] \
  || { echo "REFUSING: the 2.2.1 reference ($REF_DIR) MANIFEST / zips are not the pinned sha256s — someone changed the reference" >&2; exit 95; }
tail -1 "$REF_DIR/MANIFEST-2.2.1_be0fe37.txt" | grep -qxF 'MANIFEST COMPLETE: 32 checks, 0 failed' && grep -qF "nexusaireleaseacr.azurecr.io/nexusai@$IMG_DIGEST" "$REF_DIR/MANIFEST-2.2.1_be0fe37.txt" \
  || { echo "REFUSING: the reference MANIFEST does not end 32/0 or does not name the 2.2.1 image digest" >&2; exit 95; }
grep -qF "2.2.0: digest: $IMG_DIGEST" "$S81J/acr-build-2.2.0.log" && grep -qF "BUILD_COMMIT_SHA=$IMG_SRC" "$S81J/mail-04-digest.txt" \
  || { echo "REFUSING: the 2.2.0 build log / digest mail no longer carry WRONG 7's digest and BUILD_COMMIT_SHA" >&2; exit 95; }

# 70 — the carried rulings and Tuesday's answers (REFUSALs where a ruling is missing).
[ -s "$SQLITE_RULING" ] && grep -qF 'The offline unpack of sqlite3' "$SQLITE_RULING" || { echo "REFUSING: Tuesday's sqlite3 prebuild ruling (ruling m) is not at $SQLITE_RULING" >&2; exit 70; }
[ -s "$BELT_ANS" ] && grep -qF 'run UNBELTED. Every other jest run stays belted: cells, mutants, C-68 unions, drivers and servers.' "$BELT_ANS" \
  || { echo "REFUSING: Tuesday's belt answer (ruling n) is not at $BELT_ANS as quoted" >&2; exit 70; }
[ -s "$NOTIFIER_ANS" ] && grep -qF 'Every later npm invocation in this gate carries npm_config_update_notifier=false' "$NOTIFIER_ANS" \
  || { echo "REFUSING: Tuesday's notifier answer (ruling m) is not at $NOTIFIER_ANS as quoted" >&2; exit 70; }
[ -s "$RULING_B" ] && grep -qF 'Deliver the verdict NOW.' "$RULING_B" || { echo "REFUSING: Tuesday's ruling (b) is not at $RULING_B as quoted" >&2; exit 70; }
grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF24" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF25" && grep -qF 'NOT RUN, named, under ruling (o) EXTENDED' "$BRIEF" \
  || { echo "REFUSING: ruling (o)'s EXTENSION words are not carried in gates 24/25's briefs and this brief" >&2; exit 70; }
[ -s "$G19_RELEASE" ] && grep -qF 'the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on.' "$G19_RELEASE" \
  || { echo "REFUSING: gate 19's RELEASE no longer carries the yield retirement" >&2; exit 70; }
[ -s "$ANS1" ] && grep -qF 'load1 below 8 before every heavy run' "$ANS1" && grep -qF 'lock base locks-laptop-1017' "$ANS1" \
  || { echo "REFUSING: Tuesday's ANSWER-1 (load 8, lock base) is not at $ANS1 as quoted" >&2; exit 70; }
[ -s "$ANS7" ] && grep -qF 'Tuesday commissions ONE tier-1 re-gate for it ("gate 26", be0fe37 as merged on c7ca0ed) now; it runs after gate 25 frees the jest lock.' "$ANS7" \
  && grep -qF 'The gate re-measures every one of the 24 per id; a failed condition there is a STOP.' "$ANS7" \
  && grep -qF 'whether README.md and DEPLOYMENT_GUIDE.md as be0fe37 carries them equal what the released 2.2.1 image ships' "$ANS7" \
  || { echo "REFUSING: Tuesday's ANSWER-7 is not at $ANS7 as quoted" >&2; exit 70; }
[ -s "$V5B" ] && grep -qF 'The 13 renames are accounted under C-133 on the gate' "$V5B" && grep -qF 'after C-170, the next image built from main carries the release-line README.md and DEPLOYMENT_GUIDE.md' "$V5B" \
  || { echo "REFUSING: Tuesday's batch 5b verdict no longer carries ruling 1 and A-N1 as quoted" >&2; exit 70; }
[ -s "$ADD25" ] && grep -qF 'BEFORE you run `git remote remove origin`' "$ADD25" || { echo "REFUSING: gate 25's ADDENDUM-1 (the ref order) is not at $ADD25" >&2; exit 70; }

# 70N — machine-local premises, NOTEd (the gate records what it finds).
if [ -d "$NPM_CACHE/index-v5" ]; then
  grep -r -l -F -m1 -- 'proxy-addr/-/proxy-addr-2.0.8.tgz' "$NPM_CACHE/index-v5" >/dev/null 2>&1 || echo "NOTE: the local npm cache index has no proxy-addr 2.0.8 — the offline npm ci (H-31) may ENOTCACHE" >&2
else
  echo "NOTE: no local npm cache at $NPM_CACHE — H-31's offline install has no source; the gate will mail a QUESTION" >&2
fi
PB_NOW="$(fsha "$PREBUILD")"
[ "$PB_NOW" = "$PREBUILD_SHA" ] || echo "NOTE: the cached sqlite3 prebuild is '${PB_NOW:-absent}', not 84a34404…7afc — ruling (m)'s condition 1 records what the gate finds" >&2
NODEV="$(node -v 2>/dev/null)"
[ "$NODEV" = "v26.8.1" ] || echo "NOTE: host node is '${NODEV:-absent}', not v26.8.1 as briefed (T5) — the gate records it" >&2
GLV="$(gitleaks version 2>/dev/null)"
[ "$GLV" = "8.30.1" ] || echo "NOTE: gitleaks is '${GLV:-absent}', not 8.30.1 — r10 records it (CI pins 8.30.1)" >&2
for t in zip unzip zipinfo curl python3; do command -v "$t" >/dev/null 2>&1 || echo "NOTE: '$t' not on PATH — the package build (r4) needs it" >&2; done
command -v pwsh >/dev/null 2>&1 && echo "NOTE: pwsh IS on PATH now — the brief says arm-ttk is NOT RUN for want of it (L-B3); the gate may say so" >&2
LOAD1="$(sysctl -n vm.loadavg 2>/dev/null | awk '{print $2}')"
awk -v l="${LOAD1:-99}" 'BEGIN{exit !(l < 8)}' || echo "NOTE: 1-minute load is ${LOAD1:-unknown} (not below 8) — the gate waits in the queue, never in a hold (ruling p)" >&2

# 31 — the READY, the reference, builder evidence, gate 24's instruments (THIS drive), standing references.
for f in "$READY_170" "$CLAR" "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25" "$BRIEF5B" "$V5B" "$B24_REPORT" "$CHARTER" "$S78G_ACC" \
         "$S101/c57-be0fe37.out" "$S101/c133-be0fe37.out" "$S101/be0fe37-guards.out" "$S101/be0fe37-guards.json" "$S101/verify-merge-be0fe37.log" "$S101/mt-be0fe37.txt" \
         "$S101/shipped-text-be0fe37.txt" "$S101/pkg-build-merged.log" "$S101/pkg-build-control.log" "$S81J/acr-build-2.2.0.log" "$S81J/mail-04-digest.txt" \
         "$B24_INST/env24.sh" "$B24_INST/HOLD24.sh" "$B24_INST/qa-file24.sh" "$B24_INST/qa-file24r.sh" "$B24_INST/qa-floorlib24.sh" "$B24_INST/qa-floorcount.py" "$B24_INST/qa-to.sh" \
         "$B24_INST/qa-pin24.sh" "$B24_INST/qa-qlist24.sh" "$B24_INST/qa-mut24.py" "$B24_INST/qa-npm24.sh" "$B24_INST/qa-runj24.sh" "$B24_INST/qa-verify24.sh" \
         "$B24_INST/qa-holdlib24.sh" "$B24_INST/qa-h1-selftest24.sh" "$B24_INST/qa-h1-scan.py" "$B24_INST/qa-mail24.py" "$B24_INST/qa-mailread24.py" "$B24_INST/qa-jestwrap.sh" \
         "$B24_INST/qa-jsum.js" "$B24_INST/qa-lockcheck.py" "$B24_INST/qa-names23.py" "$B24_INST/qa-ssprint.sh" "$B24_INST/qa-netbelt.sb" "$B24_INST/qa-netbelt-nodns.sb" "$B24_INST/qa-netbelt-ctl.js"; do
  [ -s "$f" ] || { echo "REFUSING: evidence, brief or tool absent: $f" >&2; exit 31; }
done
[ -n "${QA_READY_OVERRIDE_170:-}" ] || [ "$(fsha "$READY_170")" = "$READY_SHA" ] || { echo "REFUSING: the READY in briefs/ is not the drafter's saved body (sha256 0e479fd5…) — re-read it from the inbox" >&2; exit 31; }
grep -qF "${H460:0:7}" "$READY_170" && grep -qF 'READY FOR GATE' "$READY_170" && grep -qF 'PRIOR WORK' "$READY_170" && grep -qF 'NOT TESTED' "$READY_170" && grep -qF "$T170" "$READY_170" && grep -qF "$SM170" "$READY_170" \
  || { echo "REFUSING: the READY does not name be0fe37, 88153c0, tree 0f4602e, READY FOR GATE, PRIOR WORK and NOT TESTED" >&2; exit 31; }
grep -qF 'VERDICT: accounted 24, still missing 0, absent files 0' "$S101/c133-be0fe37.out" && grep -qF 'VERDICT: STOP — the merged set is NOT a superset. Do not merge. (C-57 step 3)' "$S101/c57-be0fe37.out" \
  || { echo "REFUSING: the builder's C-57 / C-133 outputs no longer carry the lines the brief relays" >&2; exit 31; }
grep -qF 'MANIFEST COMPLETE: 42 checks, 15 failed' "$S101/pkg-build-control.log" && grep -qF 'MANIFEST COMPLETE: 32 checks, 0 failed' "$S101/pkg-build-merged.log" \
  || { echo "REFUSING: the builder's build logs no longer carry 42/15 (control) and 32/0 (merged)" >&2; exit 31; }
grep -qF 'removed/rewritten by PACKAGE side 9eee3ff,c7f62f2' "$S78G_ACC" || { echo "REFUSING: s78g/c57-accounting.txt no longer marks the six retired ids (T2's source)" >&2; exit 31; }
grep -qF 'STATUS: COMPLETE' "$B24_REPORT" || { echo "REFUSING: gate 24's report does not read as delivered (the instrument source must be a DELIVERED gate)" >&2; exit 31; }
[ ! -e "$B24_INST/.throwaway-ss" ] || echo "NOTE: gate 24's inst/ holds a .throwaway-ss — copy instruments BY NAME, never the directory" >&2
for B in "$BRIEF22" "$BRIEF23" "$BRIEF24" "$BRIEF25"; do grep -qF '## 3a. INSTRUMENT RULES' "$B" || { echo "REFUSING: $B has no section 3a — the H-rules carried by reference are missing" >&2; exit 31; }; done

# 39 — the floor instrument is named in the brief.
grep -qF 'qa-floorlib24.sh' "$BRIEF" && grep -qF '2026-10-17-gate24-rd848' "$BRIEF" || { echo "REFUSING: brief does not name the floor instrument / gate 24's instrument dir" >&2; exit 39; }

# 10 / 17 — report path named in both; no stale report; brief names every source it cites.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
for P in "2026-10-18_nexusai-c170-merged-READY-mail.txt" "2026-10-18_S101O_ANSWER-7_c170-ready-three-rulings.md" "2026-10-13_nexusai-gate-batch22.md" \
         "2026-10-16_nexusai-gate-batch23.md" "2026-10-17_nexusai-gate24-rd848.md" "2026-10-18_nexusai-gate25-rd761-rd794-merged.md" "2026-09-27_nexusai-gate-batch5b-c170pkg-rd696-rd594.md" \
         "2026-09-28_nexusai_M_batch5b_verdict.md" "2026-10-05_qa_b14_belt_ANSWER.md" "2026-10-06_nexusai_g18_ruling_b_deliver_now.md" "qa-file24.sh" "qa-file24r.sh" \
         "s78g/c57-accounting.txt" "pkg-build-final-be0fe37" "acr-build-2.2.0.log" "mail-04-digest.txt" "build-commit-sha.sh" "models_latest.json" "QA_AGENT_CHARTER.md" \
         ".throwaway-ss" "locks-laptop-1017" "ADDENDUM-1"; do
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
for T in 'THIS IS A TIER-1 GATE' 'RE-GATE AS MERGED' 'NO GO' 'NO HOST NPM REGISTRY' 'IS PART OF H-31' 'FULL VERIFIES UNBELTED' 'EXTENSION' \
         'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'NAMED NOT RUN' '--replace' 'qa-g26-' 'RETIRED' 'H-34' 'H-35' 'C-63' 'C-216' \
         'THE TREE ROW' 'THE INTERACTION ROW' 'THE GUARD ROW' 'THE BUILD ROW' 'THE SUITE ROW' 'THE SHIPPED-TEXT ROW' 'THE WORKFLOW ROW' 'THE DEPLOY ROW' 'THE AUDIT ROW' 'THE SECRETS ROW' \
         'M170' 'DISARMED' 'can fail' 'positive control' 'negative control' 'G26-<n>' 'NOT TESTED' 'PRIOR WORK' 'never dismisses an alert' 'No HTTP to any production or demo host' \
         'word pack' 'curl shim' 'MKT_ANON_PULL_PROBE' 'paths-ignore'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not declare '$T'" >&2; exit 12; }
done
for T in 'TIER-1 RE-GATE AS MERGED' 'THE PROPERTIES' 'THE TREE ROW' 'THE INTERACTION ROW' 'THE GUARD ROW' 'THE BUILD ROW' 'THE SUITE ROW' 'THE SHIPPED-TEXT ROW' 'THE WORKFLOW ROW' \
         'THE DEPLOY ROW' 'THE AUDIT ROW' 'THE SECRETS ROW' 'M170' 'REBUILD' 'C-216' 'by INPUT' 'TWO anonymous requests' 'MKT_ANON_PULL_PROBE' 'paths-ignore' 'as SETS' \
         'UNBELTED' 'npm_config_update_notifier=false' 'BOTH thresholds block' 'RULING (b)' 'EXTENSION' 'NAMED NOT RUN' '--replace' 'qa-g26-' 'RETIRED' 'locks-laptop-1017' \
         'jest lock' 'T1' 'T2' 'T4' 'T6' 'T8' "never trust the seat's trees" 'no HTTP to any production or demo host' 'One client only' 'NO docker object and NO az' 'C-23'; do
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt does not declare '$T'" >&2; exit 12 ;; esac
done
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$H460" "$MAIN_SHA" "$LOCK_SHA_INST" "$T170"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
for S in "$MB460" "$SM170" "$CB170" "$C57_SHA" "$C133_SHA" "$PKG_BLOB" "$LOCK_BLOB" "$DEPLOY_BLOB" "$ARMTTK_BLOB" "$PREBUILD_SHA" "$IMG_SRC" "${IMG_DIGEST#sha256:}" "$READY_SHA"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S in full" >&2; exit 14; }
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
if printf '%s\n' "$PROMPT" | grep -qF 'KK_T9_External_HDD'; then echo "REFUSING: the prompt names a T9 path — every path of this gate is on /Volumes/Laptop-DEV" >&2; exit 15; fi
if grep -qF 'KK_T9_External_HDD/TUESDAY' "$BRIEF"; then echo "REFUSING: the brief names the T9 TUESDAY tree" >&2; exit 15; fi
[ "$(grep -oE 'qa-g26-[A-Za-z0-9_<>-]*merge[A-Za-z0-9_-]*' "$BRIEF" | grep -c .)" = "0" ] || { echo "REFUSING: the brief suggests a qa-g26- tag containing 'merge' (C-141 ADDENDUM 7)" >&2; exit 15; }
[ "$(printf '%s\n' "$PROMPT" | grep -oE 'qa-g26-[A-Za-z0-9_<>-]*merge' | grep -c .)" = "0" ] || { echo "REFUSING: the prompt suggests a qa-g26- tag containing 'merge'" >&2; exit 15; }

# 41 — RULING (i)'s by-hand yield is RETIRED.
for T in 'stop YOUR OWN unstarted waiter' 'stop your OWN unstarted waiter' 'then re-queue with --after that merge' 'self-apply ONE yield per gate TAG'; do
  if grep -qF -- "$T" "$BRIEF" || printf '%s\n' "$PROMPT" | grep -qF -- "$T"; then echo "REFUSING: '$T' instructs the RETIRED by-hand yield" >&2; exit 41; fi
done
grep -qF 'is RETIRED from gate 21 on.' "$BRIEF" || { echo "REFUSING: the brief does not quote the retirement of ruling (i)'s yield" >&2; exit 41; }
case "$PROMPT" in *"BY-HAND GATE YIELD IS RETIRED"*) ;; *) echo "REFUSING: the prompt does not say the by-hand gate yield is RETIRED" >&2; exit 41 ;; esac

# 82 — THE MODEL RULE is carried in the brief and the prompt, per session, never "Switch automatically".
for T in "$STATUS_SUBJ" "$PARK_LINE" 'classifier-stops.txt' 'Switch automatically' 'Opus 4.8' 'PER SESSION' 'which rows ran on which model' 'Opus 5.5'; do
  grep -qiF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks THE MODEL RULE fragment '$T'" >&2; exit 82; }
  case "$(printf '%s' "$PROMPT" | tr '[:upper:]' '[:lower:]')" in *"$(printf '%s' "$T" | tr '[:upper:]' '[:lower:]')"*) ;; *) echo "REFUSING: prompt lacks THE MODEL RULE fragment '$T'" >&2; exit 82 ;; esac
done
grep -qF '## THE MODEL RULE' "$BRIEF" && grep -qF 'H-27' "$BRIEF" && grep -qF 'H-28 (AMENDED' "$BRIEF" && grep -qF 'H-32 (LOCAL ONLY' "$BRIEF" && grep -qF 'H-34 (THE LOCK BASE' "$BRIEF" \
  && grep -qF 'H-35 (NO DOCKER, NO AZ' "$BRIEF" \
  || { echo "REFUSING: brief lacks THE MODEL RULE section or H-27/H-28 (amended)/H-32/H-34/H-35" >&2; exit 82; }

# 19 — the words the prompt must carry (% is a space); the brief's sections; limits; rows; READY lines verbatim; clarification quotes.
WORDS="RD-460 C-170 C-216 C-138 C-23 C-57 C-133 C-190 C-209 C-185 C-192 C-205 C-141 C-63 C-40 C-68 C-76 C-102 C-112 C-174 C-49 C-89 C-115 C-125 C-130 C-131 C-151 C-203 ADDENDA%6%and%7
r0 r2 r3 r4 r5 r5b r6 r7 r8 r9 r10 T1 T2 T3 T4 T5 T6 T7 T8 M0 1904765 c7ca0ed 19477a9 384805d 2.0.8 proxy-addr vars.CI_DEPLOY_ENABLED nexusaireleaseacr.azurecr.io 0677388
L-B1 L-B8 L-Y1 H-1 H-3 H-4 H-6 H-9 H-17 H-20 H-21 H-22 H-24 H-26 H-27 H-28 H-29 H-31 H-32 H-33 H-34 H-35 --forceExit trap%on%EXIT DEADLINE LANDING%CONTROL
_prebuilds node_sqlite3.node sqlite3%binding:%cached%prebuild,%offline _update-notifier-last-checked exits%71 --mirror EXCLUSIVE STOP VOID C57_ROOT gitleaks%8.30.1
MERGES%GO%FIRST QUEUE,%NEVER%TAKE%OVER SAME-PLACE%handover HEARTBEAT 2%minutes 5%minutes finally SESSION_SECRET%UNSET NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED
RELAYED CodeQL%is%NOT%RUN UNKNOWN about%40%minutes 2-hour%maximum TRACKED%child Prior%work FOREGROUND never%push NEVER%merge Partner%Center npm%install --offline ENOTCACHED
qa-file24.sh ticket-left-* -r<N> instrument never%fixes GROUPED SPLIT never%dismissed PROVISIONAL qa-g26 G26-<n> N26-<n> 1-minute%load%of%8 S101O QA/NexusAI-gate25
MANIFEST%COMPLETE:%32%checks,%0%failed 15%FAILs zip%ENTRY curl%shim archive%extraction image-content-exposure rd385-shipped-root-markdown-identifiers rd630-armttk-ci-workflow"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## TIER' '^## WRONG OR UNVERIFIED' "^## TUESDAY'S RULINGS" '^## THE MODEL RULE' '^## Charter' '^## THE CLARIFICATIONS THAT BIND THIS GATE' '^## PRIOR ROUND' '^## 1. Target' \
         '^## 2. Tier and severity' '^## 2a. ROWS' '^## 2b. THE BUILD' '^## 2c. THE 24 IDS' '^## 3. THE QUESTIONS' '^## 3a. INSTRUMENT RULES' '^## 3b. THE NEGATIVE-ASSERTION SWEEP' \
         '^## 7. THE MERGED TREE' '^## 8. CI, ALERTS, AUDIT, DEPLOY-DEMO' '^## 9. Floor discipline' '^## 10. HELD' '^## 11. Output' '^## PROVENANCE' '^### How to build your trees' '^## FILL AT STAMP'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
grep -qF '**A RE-GATE AS MERGED, not a fix round**' "$BRIEF" || { echo "REFUSING: the brief's PRIOR ROUND block does not declare the re-gate" >&2; exit 19; }
grep -qF "$B24_REPORT" "$BRIEF" || { echo "REFUSING: the brief does not name gate 24's report path (the instrument source)" >&2; exit 19; }
[ "$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)" -lt "$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)" ] || { echo "REFUSING: the WRONG OR UNVERIFIED section is not above TUESDAY'S RULINGS" >&2; exit 19; }
WSTART="$(grep -n '^## WRONG OR UNVERIFIED' "$BRIEF" | cut -d: -f1)"; WEND="$(grep -n "^## TUESDAY'S RULINGS" "$BRIEF" | cut -d: -f1)"
WUNMARKED="$(sed -n "${WSTART},${WEND}p" "$BRIEF" | grep -E '^[0-9]+\. ' | grep -vE 'MEASURED|READ-ONLY-INFERRED|own actions' | cut -c1-60)"
[ -z "$WUNMARKED" ] || { echo "REFUSING: WRONG items not marked MEASURED / READ-ONLY-INFERRED: $WUNMARKED" >&2; exit 19; }
for L in L-B1 L-B2 L-B3 L-B4 L-B5 L-B6 L-B7 L-B8 L-Y1; do grep -qF "$L" "$BRIEF" || { echo "REFUSING: brief lacks declared limit $L (C-112)" >&2; exit 19; }; done
for R in r0 r1 r2 r3 r4 r5 r5b r6 r7 r8 r9 r10; do grep -qF "| $R |" "$BRIEF" || { echo "REFUSING: brief lacks row $R" >&2; exit 19; }; done
for n in 1 2 3 4 5 6 7 8 9; do
  grep -qE "^- \*\*\(T${n}\) [^*]*:\*\* RULED: " "$BRIEF" || { echo "REFUSING: brief lacks the ruling slot (T$n) as '**(T$n) …:** RULED: …'" >&2; exit 19; }
done
# the READY's lines the brief quotes, verbatim in both.
while IFS= read -r T; do
  [ -n "$T" ] || continue
  grep -qF -- "$T" "$READY_170" || { echo "REFUSING: '$T' is no longer in the READY — the source changed; re-brief" >&2; exit 19; }
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief does not carry the READY line '$T' verbatim" >&2; exit 19; }
done <<'VERBATIM_EOF'
PRIOR WORK: S84M built be0fe37 and its MANIFEST; gate 5b GO WITH FINDINGS (2026-09-28); S86M's P-2 control. This seat ran the merge, verify, guards, C-57/C-133 and the two builds.
VERBATIM_EOF
# the rulings the brief rests on are quoted from source and still say so
while IFS= read -r Q; do
  [ -n "$Q" ] || continue
  grep -qF -- "$Q" "$CLAR" || { echo "REFUSING: CLARIFICATIONS no longer carries '$Q' — the brief's quotes are stale; re-brief" >&2; exit 19; }
  grep -qF -- "$Q" "$BRIEF" || { echo "REFUSING: brief does not quote '$Q'" >&2; exit 19; }
done <<'CLAR_EOF'
(1) Leftover C-57 ids are ACCOUNTED under C-133's blob rule, not C-215.
The gate re-measures all 24 per id, and a failed condition is a STOP. C-215 stays scoped to RD-761 and RD-794.
It is met by every [PASS] check line, the three blob sha256s, the image line, both zip byte counts, and every zip ENTRY being byte-identical to the reference zips' entries.
The zip-CONTAINER digests are not a reproducibility measure while entries carry the extract time.
(3) C-170 does NOT wait for RD-413.
If they do not, they go to Kam as a word pack.
The main build must reproduce the 2.2.1 MANIFEST sha256s. Tier 1. No deploy, no Partner Center (C-23).
making the job a required status check (a branch-protection setting, not a file)
Kam alone uploads to Partner Center, and only when ready.
A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control.
It normalises runs of digits only, within the same test file.
A missing id is ACCOUNTED, not a STOP, only when BOTH of these hold for its file: (1) the merged blob is byte-identical to one parent's blob; (2) since the merge base, ONLY that parent changed the file, and the other parent's blob equals the base blob.
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
The jest and docker lock (`session-tools/nexusai-lock.sh`) is first-in-first-out, and it takes over an ownerless lock after 30 s.
A check must be able to fail on the thing it claims to be about.
a clean merge-tree and a changed measured surface are not in tension
An explanation of why a fix works is a CLAIM: it gets a red proof, or it is marked UNVERIFIED in the artefact that carries it.
every existing test that relied on a LATER return in that function is a candidate for silent disarmament
A declared limit is where the evidence stops — not a place it is cleared.
NEVER KILL BY PATTERN.
CLAR_EOF

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 71 — standing rules in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-g26-' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST' 'QUEUE, NEVER TAKE OVER' 'LANDING CONTROL' \
         'MAIN MOVES' '--replace' 'never push' 'C-174' '--forceExit' 'trap … EXIT' 'MERGES GO FIRST' 'queue-jest/' 'carry on' 'never idles holding a lock' \
         'ONE focused hold at a time' 'FOREGROUND' '5600' '8995' '10310' '17220' '14.5 h' 'Never two live holds' 'Every finding names its instrument' \
         'NOT TESTED' 'The tester never fixes' 'SPLIT a hold' 'ONE CLIENT ONLY' 'no CodeQL alert dismissed' 'below a 1-minute load of **8**'; do
  grep -qiF -- "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac
grep -qF 'The report'"'"'s LAST three lines are the three verdict lines' "$BRIEF" || { echo "REFUSING: brief must fix the report's last lines as the verdict lines" >&2; exit 71; }

# 76 / 77 / 78 / 79 — H-1's printer and forbidden idioms; H-4; H-9; H-7/H-8.
grep -qF "$SAFE_PRINTER" "$BRIEF" || { echo "REFUSING: brief must carry the safe SESSION_SECRET printer verbatim (H-1)" >&2; exit 76; }
for w in '${SESSION_SECRET-…}' '${SESSION_SECRET+$SESSION_SECRET}' 'printenv' '${envs[*]}' 'docker inspect'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief must name the forbidden idiom $w (H-1)" >&2; exit 76; }
done
for w in 'separate child' 'within 90 s' 'max gap'; do grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the heartbeat fragment '$w' (H-4)" >&2; exit 77; }; done
for w in 'H-9' 'Buffer' 'xxd -l 16' 'JSON.stringify'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the byte-plant fragment '$w' (H-9)" >&2; exit 78; }; done
for w in 'H-7' 'H-8' 'negative control' 'original text is absent once the new text is removed' 'FAILS LOUDLY'; do grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the mutant-landing fragment '$w' (H-7/H-8)" >&2; exit 79; }; done

# 81 — this gate's own premises are in the brief.
for w in 'C-190' 'NEVER opens, comments on, approves or merges a PR' 'NEVER merges anything the fleet can see and never pushes' 'CodeQL is NOT RUN on the merged tree' 'Blocker' 'setuid' 'pgrep' '`END ok`' \
         'exits 71' 'ARRAY option' '=====' 'UNKNOWN' '19477a9' 'proxy-addr' 'RD-827' 'npm ci --offline --ignore-scripts' 'ENOTCACHED' '_cacache' '_prebuilds' '84a34404' \
         'sqlite3' 'merge-tree --write-tree' 'hash-object -w' 'write-tree' 'commit-tree' 'GIT_INDEX_FILE' '_updated' 'detached worktree HEAD' 'argument spelling' \
         'refs/remotes/t9-drive-2026-10-15' 'git remote remove origin' 'oauth2/token' '/manifests/' 'MKT_ANON_PULL_PROBE' 'HTTP 200' 'FAILED-MANIFEST' 'RD-527' 'TMPDIR' \
         'f129ff3' '01c7c46' 'e23999f' '3753a82' 'Dockerfile' '.dockerignore' 'dockerfile-stages.js' 'rd418-dockerignore-round3' 'A-N1' 'build-commit-sha.sh' 'clean' \
         'arm-ttk.yml' 'contents: read' 'actions/checkout@v4' 'sha256sum -c' 'pwsh' 'required_status_checks' 'deploy-key' 'paths-ignore' 'CI_DEPLOY_ENABLED' 'skipped' \
         'gitleaks' '.gitleaks.toml' '.gitleaks-lockfile.toml' 'gitleaks-canary.sh' 'RD-111' 'git archive' 'NEXUSAI_LOCK_BASE' 'locks-laptop-1017' 's78g-regate' 'T9' 'C57_ROOT' \
         'rm -rf' 'worktree remove --force' 'WRONG 1' 'WRONG 2' 'WRONG 3' 'WRONG 4' 'WRONG 6' 'WRONG 7' 'WRONG 8' 'MEASURED' 'READ-ONLY-INFERRED' 'qa-floorlib24.sh' 'qa-file24.sh' \
         'ADDENDUM 7' 'datasecau/Reporting_Dashboard_Au' 'RETIRED' 'wednesday' 'PROVISIONAL' '3c33f5ae' 'claude-opus-5-5' 'Node v26.8.1' 'S101O' 'RD-505' 'RD-506' '§9.9' \
         '2 → 4' 'docs/test-files ships by NO path' 'jsdom-instrument-limits' 'rd327-build-digest-on-public-health' 'marketplace-package-build' 'rd461-self-contained-and-template-toolkit' \
         'rd503-r2-doc-claims-against-product' '5419285' '379b8b5' '5584ea4' '20bf99c' '8de8e5c' '3f7e263' 'QA/NexusAI-gate25' 'gate 25'; do
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
# fleet-monitor and every live 'QA/*' pane other than this gate's own (gate 25 included): a negative control when exactly one claude runs under it.
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
[ -n "$(pane_pid_of "$PEER_GATE" | sed '/^$/d')" ] && echo "NOTE: the peer gate $PEER_GATE is LIVE — gate 26 shares its lock base and queues behind its holds (ANSWER-7)" >&2

# 86 — no live gate-26 session already exists.
for P in $(pane_pid_of "$ROUTE_NAME"); do
  if [ -n "$(claude_under "$P")" ]; then echo "REFUSING: a pane named $ROUTE_NAME (pid $P) already runs a claude — gate 26 is live; do not start a second session" >&2; exit 86; fi
  [ "$CHECK" = "1" ] || echo "NOTE: a pane named $ROUTE_NAME (pid $P) exists with no claude under it — the cockpit's own add decides" >&2
done

# 32 / 40 — LAST: the coordinator's stamp (SELF-CHECK line + note + every 'RULED: @STAMP@' slot, no placeholder), the READY in briefs/ (not an override),
# and the answer route (Tuesday adds it, never this launcher).
STAMP_OK=1
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then STAMP_OK=0; fi
NSTAMP="$(grep -cF "$PH_STAMP" "$BRIEF")"
ROUTE_OK=1
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || ROUTE_OK=0
READY_OK=1
[ -z "${QA_READY_OVERRIDE_170:-}" ] || READY_OK=0
GUARDS='9 MODEL 40 6 7 8 18T 18 90 91 22 93 94 95 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86'
if [ "$STAMP_OK" = "0" ] || [ "$ROUTE_OK" = "0" ] || [ "$READY_OK" = "0" ]; then
  echo "guards pass ($GUARDS); stamp, route and/or READY NOT complete." >&2
  echo "  ls-remote attempts this run: $LSR_ATTEMPTS (C-192); origin main ${M_ORIGIN:0:7}; RD-460 ${H460:0:7}; lock tool ${INST_NOW:0:12}…; c57 ${C57_NOW:0:12}…; c133 ${C133_NOW:0:12}…; model $MODEL" >&2
  echo "  $SEAT_NOTE" >&2
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC" >&2
  [ "$READY_OK" = "1" ] || echo "REFUSING (31R): the READY was read from QA_READY_OVERRIDE_170 — launch without the override" >&2
  [ "$STAMP_OK" = "1" ] || echo "REFUSING (32): $NSTAMP stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T9) — the coordinator re-reads end-to-end and stamps them before launch" >&2
  if [ "$ROUTE_OK" = "0" ]; then
    echo "REFUSING (40): no '${ROUTE_NAME}|tuesday-agent@agentmail.to|no' line in $ROUTING — answers to the gate would have no route; Tuesday adds it at stamp (this launcher never writes it)" >&2; exit 40
  fi
  exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin at $PIN_TS ($LSR_ATTEMPTS ls-remote attempt(s), C-192): main = c7ca0ed exactly; $B460 = ${H460:0:7} (18); T9 unmounted (18T)"
  echo "  lock tool 3c33f5ae… pinned, NEXUSAI_LOCK_BASE honoured, Laptop-DEV base present, no qa-g26 ticket (90); c57 1ae84a10… + c133 6f938bfc… pinned (91)"
  echo "  pin tables (40); chain (7, 8); gated + both-sides sets (22); premises (93); $SEAT_NOTE (94); reference pinned (95); rulings + answers (70); evidence + gate 24 instruments (31)"
  echo "  MODEL RULE (82); H-1 (76); H-4 (77); H-9 (78); H-7/H-8 (79); premises (81); route $ROUTE_NAME (40); report absent (17)"
  echo "  NEG seats (38R, derived live; coordinator pane '$COORD_NAME'):$NEG_DESC"
  echo "  model: $MODEL at exec (from models_latest.json)"
  echo "  SUBJECT: $SUBJECT"
  echo "  NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  echo "  --check started no claude; nothing written."
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only, $LSR_ATTEMPTS attempt(s) under C-192): refs/heads/main = $M_ORIGIN (exactly c7ca0ed); refs/heads/$B460 = $H460. The T9 is unmounted. The installed lock tool $LOCKTOOL sha256 $INST_NOW equals the pin and NEXUSAI_LOCK_BASE=$LOCK_BASE_LAPTOP is exported in your environment. The C-57 runner sha256 $C57_NOW and the C-133 tool sha256 $C133_NOW equal their pins. The 2.2.1 reference MANIFEST and zips equal their pinned sha256s. Seat object: $SEAT_NOTE. These are the start-of-gate pins; take your own three readings anyway.
NEGATIVE-CONTROL SEATS, derived live by the launcher from the cockpit panes at $PIN_TS (the coordinator's pane is named '$COORD_NAME' on this machine):$NEG_DESC Re-read them at the start of every hold."

# rd579-rd639 S-1 belt: the gate session inherits NO SESSION_SECRET. The line prints the NAME and a state only, never a value.
if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET in the launcher's environment (length ${#SESSION_SECRET}) — unsetting before exec"; else echo "SESSION_SECRET UNSET"; fi
unset SESSION_SECRET
# the acceptance build must use the real probe (WRONG 3): never inherit a stub.
unset MKT_ANON_PULL_PROBE
# ruling q / H-34: the gate's lock calls use the Laptop-DEV base while the T9 is unmounted.
export NEXUSAI_LOCK_BASE="$LOCK_BASE_LAPTOP"
# ruling (m): the gate's own npm calls inherit the notifier switch (the gate still passes it explicitly on every call).
export npm_config_update_notifier=false

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model "$MODEL" "$PROMPT"
