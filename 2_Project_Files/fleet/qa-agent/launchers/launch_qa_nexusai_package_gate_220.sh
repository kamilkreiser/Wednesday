#!/bin/bash
# launch_qa_nexusai_package_gate_220.sh — cross-project QA agent, TIER 1, THE ONE PACKAGE GATE for the NexusAI 2.2.0
# Marketplace resubmission (HANDOVER-S78G §★): branch mkt-release-2.2.0-s81j at the pinned HEAD_SHA (ONE step-4 commit on the forward
# merge 6f4945b = df70a96 + main 0677388), the non-draft zips NexusAI-J (S81J) built from it, and the release image
# nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda3309…7f66 (tag 2.2.0, from 0677388, ACR run cr1).
# The verdict decides whether Tuesday emails the zip to Kam as ready to upload.
#
# PATTERN: launch_qa_nexusai_mktpkg_7aa5aaf.sh (the last package gate) + launch_qa_nexusai_gate8.sh (current conventions:
# --check, placeholder comparands BUILT BY CONCATENATION, ls-remote re-pin, SELF-CHECK stamped by the coordinator LAST,
# no --model flag). CHANGES, each deliberate:
#   - exit 9:  refuses while the HEAD / ZIPDIR / READY_MAIL placeholders are unsubstituted anywhere (brief, this file's
#              prompt), and while HEAD is not 40 hex.
#   - exit 18: RE-PIN at launch by `git ls-remote origin`: the branch must be EXACTLY the pinned head, and
#              mkt-release-gate-s78g must still be df70a96. main moving past 0677388 is a NOTE (C-149 pins the image commit).
#   - exit 8:  the chain — head's ONLY parent is 6f4945b; 6f4945b = merge(df70a96, 0677388), tree 9ec70f87.
#   - exit 22: the step-4 delta is EXACTLY the six files (five content + counts), as the builder's commit guard enforces.
#   - exit 41/42/43: the digest is set in the template (only containerImage changed), the policy (only imageTagExceptions
#              changed, one key "2.2.0", imagePlaceholder kept) and the README.
#   - exit 44: C-133 blob premise for rd495 CTRL-1 (base/B 76bbbf3, A/merged 9ffe71a).
#   - exit 45: the health build formula sha256(0677388)[:16] = b6f4bfddadcd4055.
#   - exit 47: the builder's zip dir holds exactly the non-draft trio for this head, manifest complete with 0 failed,
#              and the ZIPPED template carries the release reference.
#   - exit 40: the routing line QA/NexusAI-pkg220 exists in fleet/inbox_routing.conf (answers route there).
#   - THE PROMPT IS EMBEDDED BELOW (heredoc), not a .prompt.txt: the commission allowed two files only. Every prompt guard
#     applies to that text. exit 24 carried: the prompt must not carry the server entry point's literal path.
#   - docker and gitleaks are NOTES, not refusals: the registry-API pull needs neither; the optional smoke boot needs docker.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-pkg220' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az READ-ONLY per brief §9, gh optional and READ-ONLY); CLAUDE_CONFIG_DIR pinned
# to Tuesday's project-local store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, rev-list, ls-remote), grep, ps,
# python3 reading zips and git output. Nothing is written anywhere.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_package_gate_220.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..47 a guard refused
set -u
CHECK=0
for a in "$@"; do
  case "$a" in
    --check) CHECK=1 ;;
    *) echo "unknown argument: $a" >&2; exit 2 ;;
  esac
done

# Placeholder comparands, BUILT BY CONCATENATION so a sed of the placeholder text cannot reach them.
PH_HEAD='@HE''AD@'
PH_ZIP='@ZIP''DIR@'
PH_READY='@READY''_MAIL@'
PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-package-gate-220.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EVID_J="$NX/session-tools/s81j"
EVID_G="$NX/session-tools/s78g"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
HANDOVER_G="$NX/HANDOVER-S78G.md"
KAM_DOC="$EVID_J/doc/handover.md"
PRIOR_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-12-mktpkg-7aa5aaf-tier1r4/report.md"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
G7R1_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorlib.sh"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-25-pkg-gate-220/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-pkg220'

BRANCH='mkt-release-2.2.0-s81j'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47}"
ZIPDIR='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0'
READY_MAIL='/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-pkg220-READY-mail.txt'
MERGE_SHA='6f4945bf825dbe1928ef781613c94b5ee7cfdf8b'     # step 3: the forward merge, the head's ONLY parent
MERGE_TREE='9ec70f87b3976bdf7ec2154465b3d85652afd843'    # the tree the builder's C-57 controls ran on
PKG_SHA='df70a96145c5887a762b86f081436bd8befdf329'       # mkt-release-gate-s78g (first parent of the merge)
IMG_SHA='0677388ab031ffaf569a52f6c0301af48f44aece'       # main at drafting = the image commit (C-149, C-72)
BASE_SHA='c0788b1017a20ea5d2d0b9c0e5837ee233830696'      # merge-base(df70a96, 0677388)
RD497_SHA='5366193'                                      # A-side commit that re-anchored rd495 CTRL-1
S78G_MERGE='5b6a24f'                                     # B-side pass-through merge the C-133 script counted

RELEASE_DIGEST='sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66'
RELEASE_REF="nexusaireleaseacr.azurecr.io/nexusai@$RELEASE_DIGEST"
PLACEHOLDER='nexusaireleaseacr.azurecr.io/nexusai@sha256:RD-460-DIGEST-NOT-SET'
HEALTH_BUILD='b6f4bfddadcd4055'
DEMO_REV='nexusaidev-app--s81j-220-fdda330'

COUNTS_FILE='scripts/verify-expected-counts.json'
TEMPLATE='azure-marketplace/combined/mainTemplate.json'
POLICY='azure-marketplace/release-policy.json'
README='azure-marketplace/plans/README.md'
RD495='__tests__/rd495-admin-routes-behind-the-gate.test.js'
STEP4_FILES="__tests__/marketplace-package-build.test.js
__tests__/marketplace-single-build-path.test.js
$TEMPLATE
$README
$POLICY
$COUNTS_FILE"
MERGE_COUNTS='4120 241'
EXP_COUNTS="${QA_EXP_COUNTS_OVERRIDE:-4121 241}"    # PREDICTED (step4-hold-run2.log: 4121 after the c1/c2 split). Confirm at READY.
RD495_BLOB_BASE='76bbbf3c4ec1aa1cee6269d4ac2331b75d4c5ad0'
RD495_BLOB_A='9ffe71a215c55eb15a641e93b7114922675f29b0'

NEG_SEATS='11382 2679'   # NexusAI-J claude (%2), Tuesday claude (%0), read 2026-09-25 11:40 AEST

SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.0: '
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-pkg220] ANSWER'
NOTTESTED_LINE='Real Azure: not deployed through Partner Center, not validated against real Azure (C-20), and the Key Vault success path never executed (C-124); the jest suites are not network-sandboxed (C-58).'

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }
blob() { g rev-parse "$1:$2" 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate, TIER 1: THE ONE PACKAGE GATE for the Datasec/NexusAI 2.2.0 Azure Marketplace resubmission. One target, one verdict: GO, GO WITH FINDINGS or NO GO FOR UPLOAD. Your verdict decides whether Tuesday emails the zip to Kam as ready for him to upload to Partner Center. Kam is away and cannot reach this machine; nothing checks the zip after you.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-package-gate-220.md
Then the charter it names. Every builder statement in it is a CLAIM, never evidence.

THE TARGET. Branch mkt-release-2.2.0-s81j at c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 — ONE step-4 commit whose only parent is the forward merge 6f4945bf825dbe1928ef781613c94b5ee7cfdf8b (parents df70a96145c5887a762b86f081436bd8befdf329, the package line, and 0677388ab031ffaf569a52f6c0301af48f44aece, main and the image commit; merge base c0788b1017a20ea5d2d0b9c0e5837ee233830696). The builder's non-draft zips and manifest are in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0 (copy before unzipping; never write there). The release image is nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66 (tag 2.2.0, built from 0677388 by ACR run cr1; the source label is empty by ruling). The builder's READY is /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-pkg220-READY-mail.txt.

STEP 4 CHANGED EXACTLY SIX FILES (five content files plus the counts file): the template's containerImage variable, the plans README's image sentence (lines 40-42), release-policy.json (imageTagExceptions["2.2.0"] only; imagePlaceholder KEPT as the refusal rule), the package-build test file (sites a, b, c1/c2, d), the single-build-path test file (the RD-506 cells via placeholderBack on a COPY), and the counts file. Prove every re-anchor is strictly stronger and nothing was deleted, and that the refusal-on-placeholder property is still proven ON THE REAL FILES. Then run the both-files-wrong arm (template AND exception set to one well-formed wrong digest) and say what, if anything, reddens.

POSITIVE CONTROL FIRST: the clean files green at the head. Then re-run the builder's FOUR red-proof arms INDEPENDENTLY with mutants you build yourself — R1 and R2 on the package-build file (predicted exactly 7 red each) and Q1 and Q2 on the single-build-path file (predicted exactly the 2 RD-506 rows each) — plus the drafter's arm (exception keyed "2.2.1"). A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES: run node --check on every mutated .js and JSON.parse on every mutated .json, quote the exit code; a red from a mutant that does not parse is a VOID arm.

C-133 BY BLOB, NOT BY COMMIT LIST: re-derive all 21 missing ids of the 6f4945b merge on blob ids. The ruled one is rd495 CTRL-1: base c0788b1 76bbbf3, A 0677388 9ffe71a, B df70a96 76bbbf3, merged 9ffe71a; read the A-side re-anchor (RD-497) and say whether it is strictly stronger. Re-check the rd503-r2 id too. C-112 on all 283 merged test files. And discharge C-133's standing duty: confirm class (a) of the 23-id table of the earlier release-gate merge against RD-460's commits.

C-58 ITEM 1. (a) Re-verify anonymous pull YOURSELF through the registry API with no credentials: anonymous token, GET the manifest by digest, the sha256 of the bytes must equal the digest; GET the config blob and one layer by digest and hash them; read the labels (revision 0677388, version 2.2.0, source empty). Negative controls in the same window: no token is 401; the dev registry refuses an anonymous token. NEVER docker rmi the release image (shared store, builder's evidence). If you docker pull, use a fresh DOCKER_CONFIG holding {} with DOCKER_HOST pinned, and read the pull's exit code. Optional local smoke boot under the docker lock: health build must be b6f4bfddadcd4055 = sha256(0677388)[:16]; version "2.0.1" is known residual RD-657, NOT a failure. (b) Read the demo back READ-ONLY: at most three GET /api/health to the demo host named in the brief, build must be b6f4bfddadcd4055; the sole active revision must be nexusaidev-app--s81j-220-fdda330 running the release digest with no registry credential added — read with READ-ONLY az only if the brief's section 9 clause stands, otherwise mark that half READ ONLY. C-72: the image came from MAIN.

REBUILD THE PACKAGE YOURSELF from the pinned head with scripts/marketplace-package-build.sh (non-draft, version 2.2.0, a NEW empty out-dir in your own project, listing list azure-marketplace/listing-assets.txt) and compare with the builder's zip. PREDICT FIRST: the listing zip's whole-file sha256 should match; the plan zip's probably will NOT, because the plan files are staged with cp without -p, so entry timestamps are the build time. The binding comparison is PER ENTRY: every entry of both zips must hash equal to git show of its source at the head. Both manifests must end "MANIFEST COMPLETE: <N> checks, 0 failed"; explain every differing manifest line. The digest in the ZIPPED template must equal the release reference exactly. No DRAFT- or FAILED- file.

ARM-TTK: S78G's arm-ttk runner (session-tools/s78g/armttk.sh) on the head, quote N/M (df70a96 was 49/49), with BOTH controls (hideconf, hardloc) firing; set TMPDIR inside your own project first. Then the same on the three files unpacked from the builder's plan zip.

GITLEAKS: run gitleaks over the unpacked contents of both zips, the manifest and the handover document for Kam (copies in your own dir), with the repo's config at the head AND the default rules. POSITIVE CONTROL FIRST: a planted canary the ruleset TARGETS must fire in the same run. Check the handover document's filled values against your measurements; any unfilled value or disagreement is a finding, because it goes to Kam in the same email.

FULL VERIFY at the head under the jest lock, SESSION_SECRET UNSET (env -u SESSION_SECRET; print SET or UNSET as the hold's first line, the NAME only), npm run verify -- --maxWorkers=2 on a tree you built. Predicted 4121/241 — confirm or contradict. A clean merge-tree does not prove the checks agree (C-131); the full verify is the evidence. C-89 on your own copy.

KNOWN RESIDUALS — LIST, DO NOT FAIL: RD-657 (health says 2.0.1); the stale comment at the build script's lines 37-38 ("every build fails today"); C-124 (the Key Vault success path never executed by anyone); C-20 (the template never validated against real Azure; the validate script is an az write and is NOT RUN).

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/pkg220.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean or merge-tree --write-tree, and never work in its 2_Project_Files checkout or the builder's worktrees (C-28). Count the repo's object files before and after and account for any delta by mtime. Findings-only: no commits, no tickets, no edits in NexusAI, no replacement zip. No push, no registry change, no demo change, no Partner Center, no mail to any human. Never rm: quarantine.

FLOOR DISCIPLINE — section 8 of the brief exactly. QUEUE, NEVER TAKE OVER. Every jest run goes through session-tools/nexusai-lock.sh with a tag starting qa-pkg220- (C-141), the lock held once per multi-run measurement as a tracked child of your seat; docker legs through the docker lock. Count foreign servers the RD-606 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe and network request has a per-step DEADLINE and a client timeout, every server is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

NETWORK: only nexusaireleaseacr.azurecr.io, one anonymous token request to the dev registry as the negative control, and at most three GET /api/health to the demo. Everything else on 127.0.0.1. This is authorised defensive QA of Datasec's own release artefacts; if a response is cut off by a safety check, record it and continue with the next item.

RE-PIN at start, mid and end: the head on mkt-release-2.2.0-s81j, df70a96 on mkt-release-gate-s78g, and main — three timestamped readings with the branch name beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix. If main has moved past 0677388 that is not a refusal (C-149 pins the image commit) but report what moved.

QUESTIONS: your routing name is QA/NexusAI-pkg220. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-pkg220] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-220/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.0: <GO | GO WITH FINDINGS | NO GO FOR UPLOAD> @ <the first 7 characters of the pinned head> Lead the body with one sentence: is the zip ready for Tuesday to email to Kam, and if not, what stops it. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. That section must carry this line verbatim:
Real Azure: not deployed through Partner Center, not validated against real Azure (C-20), and the Key Vault success path never executed (C-124); the jest suites are not network-sandboxed (C-58).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 9 — nothing unsubstituted. The head must be a full 40-hex sha.
for PH in "$PH_HEAD" "$PH_ZIP" "$PH_READY"; do
  if grep -qF "$PH" "$BRIEF"; then echo "REFUSING: the brief still carries $PH — fill it at READY" >&2; exit 9; fi
  case "$PROMPT" in *"$PH"*) echo "REFUSING: the embedded prompt still carries $PH — sed this launcher at READY" >&2; exit 9 ;; esac
done
[ "$HEAD_SHA" != "$PH_HEAD" ] || { echo "REFUSING: HEAD_SHA is still the placeholder" >&2; exit 9; }
[ "$ZIPDIR" != "$PH_ZIP" ] && [ "$READY_MAIL" != "$PH_READY" ] || { echo "REFUSING: ZIPDIR or READY_MAIL is still a placeholder" >&2; exit 9; }
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: HEAD_SHA '$HEAD_SHA' is not a full 40-hex sha" >&2; exit 9; }
HEAD7="${HEAD_SHA:0:7}"

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$HEAD_SHA" "$MERGE_SHA" "$PKG_SHA" "$IMG_SHA" "$BASE_SHA" "$RD497_SHA" "$S78G_MERGE"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# 7 — the forward merge's base.
[ "$(g merge-base "$PKG_SHA" "$IMG_SHA" 2>/dev/null)" = "$BASE_SHA" ] || { echo "REFUSING: merge-base(df70a96, 0677388) is not c0788b1" >&2; exit 7; }

# 8 — the chain: head's ONLY parent is the merge; the merge's parents and tree are the commissioned ones.
# ADDENDUM AT READY (Tuesday): the head is the PACKAGE commit 3464dd8 (only parent = the merge) plus three doc-only
# commits. Assert both halves: 3464dd8's only parent is 6f4945b, the head descends linearly from 3464dd8, and
# 3464dd8..head touches ONLY the handover doc.
PKGC_SHA=3464dd80854c108063facfb0355ce1a4eed5fff8
[ "$(g log -1 --format='%P' "$PKGC_SHA" 2>/dev/null)" = "$MERGE_SHA" ] || {
  echo "REFUSING: 3464dd8's parent list is '$(g log -1 --format='%P' "$PKGC_SHA" 2>/dev/null)', not exactly 6f4945b" >&2; exit 8; }
# 28e1949 is a MERGE (the fold of resubmission-handover-s78g @ dfbd55b), so "linear" is not asserted; the binding
# property is the TREE difference below (only the handover doc), plus ancestry.
g merge-base --is-ancestor "$PKGC_SHA" "$HEAD_SHA" 2>/dev/null || {
  echo "REFUSING: $HEAD7 does not descend from 3464dd8" >&2; exit 8; }
_DOCD="$(g diff --name-only "$PKGC_SHA" "$HEAD_SHA" 2>/dev/null)"
[ "$_DOCD" = "docs/resubmission/2026-09-22_resubmission-handover-for-kam.md" ] || {
  echo "REFUSING: 3464dd8..$HEAD7 touches more than the handover doc: $_DOCD" >&2; exit 8; }
[ "$(g log -1 --format='%P' "$MERGE_SHA" 2>/dev/null)" = "$PKG_SHA $IMG_SHA" ] || { echo "REFUSING: 6f4945b's parents are not df70a96 + 0677388 in that order" >&2; exit 8; }
[ "$(g log -1 --format='%T' "$MERGE_SHA" 2>/dev/null)" = "$MERGE_TREE" ] || { echo "REFUSING: 6f4945b's tree is not 9ec70f87 (the tree the C-57 controls ran on)" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote. The branch must be at origin (C-113) and exactly the pinned head.
L="$(g ls-remote origin "refs/heads/$BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: origin refs/heads/$BRANCH is not $HEAD_SHA — not pushed, or moved; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
L2="$(g ls-remote origin refs/heads/mkt-release-gate-s78g 2>&1)"
printf '%s\n' "$L2" | grep -q "^${PKG_SHA}[[:space:]]refs/heads/mkt-release-gate-s78g\$" || {
  echo "REFUSING: origin mkt-release-gate-s78g is not df70a96 — the package line moved; re-brief" >&2; printf '%s\n' "$L2" >&2; exit 18; }
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$IMG_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not 0677388 — not a refusal (C-149 pins the image commit); the gate reports what moved (brief Q0)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — the step-4 delta is EXACTLY the six files.
GOT="$(g diff --name-only "$MERGE_SHA" "$PKGC_SHA" 2>/dev/null | sort)"   # ADDENDUM: the package commit, not the doc-carrying head
[ "$GOT" = "$(sorted "$STEP4_FILES")" ] || { echo "REFUSING: 6f4945b..$HEAD7 is not exactly the six step-4 files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts at the merge and at the head.
CT="$(counts_at "$MERGE_SHA")"; [ "$CT" = "$MERGE_COUNTS" ] || { echo "REFUSING: counts at 6f4945b read '${CT:-unreadable}', not '$MERGE_COUNTS'" >&2; exit 35; }
CT="$(counts_at "$HEAD_SHA")"; [ "$CT" = "$EXP_COUNTS" ] || {
  echo "REFUSING: counts at $HEAD7 read '${CT:-unreadable}', not the predicted '$EXP_COUNTS' — confirm against the READY and set EXP_COUNTS (and the brief) before launch" >&2; exit 35; }

# 41 / 42 — the template and the policy changed ONLY where step 4 says, to exactly the release reference.
python3 - "$REPO" "$MERGE_SHA" "$HEAD_SHA" "$TEMPLATE" "$POLICY" "$RELEASE_REF" "$PLACEHOLDER" <<'PY'
import json, subprocess, sys
repo, base, head, tpath, ppath, ref, ph = sys.argv[1:8]
def show(sha, p):
    return json.loads(subprocess.run(["git", "--no-optional-locks", "-C", repo, "show", f"{sha}:{p}"],
                                     check=True, capture_output=True).stdout)
tb, th = show(base, tpath), show(head, tpath)
if tb["variables"].get("containerImage") != ph:
    print("REFUSING: the template at 6f4945b does not hold the placeholder", file=sys.stderr); sys.exit(41)
if th["variables"].get("containerImage") != ref:
    print(f"REFUSING: the template's containerImage at the head is {th['variables'].get('containerImage')!r}, not the release reference", file=sys.stderr); sys.exit(41)
th2 = json.loads(json.dumps(th)); th2["variables"]["containerImage"] = ph
if th2 != tb:
    print("REFUSING: the template changed somewhere other than variables.containerImage", file=sys.stderr); sys.exit(41)
pb, phd = show(base, ppath), show(head, ppath)
if phd.get("imagePlaceholder") != ph or pb.get("imagePlaceholder") != ph:
    print("REFUSING: release-policy imagePlaceholder is not kept as the refusal rule", file=sys.stderr); sys.exit(42)
ex = phd.get("imageTagExceptions")
if not isinstance(ex, dict) or list(ex) != ["2.2.0"] or not isinstance(ex["2.2.0"], dict) or ex["2.2.0"].get("image") != ref:
    print(f"REFUSING: imageTagExceptions is not exactly {{'2.2.0': {{image: <release ref>}}}}: {ex!r}", file=sys.stderr); sys.exit(42)
a = {k: v for k, v in pb.items() if k != "imageTagExceptions"}
b = {k: v for k, v in phd.items() if k != "imageTagExceptions"}
if a != b:
    print("REFUSING: release-policy changed outside imageTagExceptions", file=sys.stderr); sys.exit(42)
if pb.get("imageTagExceptions") != {}:
    print("REFUSING: imageTagExceptions at 6f4945b was not {}", file=sys.stderr); sys.exit(42)
PY
RC=$?; [ "$RC" = 0 ] || exit "$RC"

# 43 — the README names the release reference at the head.
g show "$HEAD_SHA:$README" 2>/dev/null | grep -qF "$RELEASE_REF" || { echo "REFUSING: $README at $HEAD7 does not name the release reference" >&2; exit 43; }
g show "$HEAD_SHA:scripts/marketplace-package-build.sh" 2>/dev/null | sed -n '37,38p' | grep -qi 'every build fails today' \
  || echo "NOTE: the known stale comment is no longer at marketplace-package-build.sh:37-38 — re-read the brief's residual line" >&2

# 44 — C-133's blob premise for rd495 CTRL-1.
[ "$(blob "$BASE_SHA" "$RD495")" = "$RD495_BLOB_BASE" ] && [ "$(blob "$PKG_SHA" "$RD495")" = "$RD495_BLOB_BASE" ] \
  && [ "$(blob "$IMG_SHA" "$RD495")" = "$RD495_BLOB_A" ] && [ "$(blob "$MERGE_SHA" "$RD495")" = "$RD495_BLOB_A" ] \
  && [ "$(blob "$HEAD_SHA" "$RD495")" = "$RD495_BLOB_A" ] || {
  echo "REFUSING: the rd495 blobs are not base/B 76bbbf3, A/merged/head 9ffe71a — the C-133 premise is gone" >&2; exit 44; }

# 45 — the health build formula.
HB="$(python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest()[:16])' "$IMG_SHA")"
[ "$HB" = "$HEALTH_BUILD" ] || { echo "REFUSING: sha256(0677388)[:16] is $HB, not $HEALTH_BUILD" >&2; exit 45; }

# 47 — the builder's zip dir: exactly the non-draft trio for this head, complete with 0 failed, digest in the zipped template.
[ -d "$ZIPDIR" ] || { echo "REFUSING: builder zip dir missing: $ZIPDIR" >&2; exit 47; }
python3 - "$ZIPDIR" "${PKGC_SHA:0:7}" "$RELEASE_REF" <<'PY'   # ADDENDUM: zips are named after the package commit 3464dd8
import json, os, re, sys, zipfile
d, h7, ref = sys.argv[1:4]
want = {f"NexusAI_plan-managed-ai_2.2.0_{h7}.zip", f"NexusAI_listing-assets_2.2.0_{h7}.zip", f"MANIFEST-2.2.0_{h7}.txt"}
names = set()
for root, dirs, files in os.walk(d):
    for f in files:
        names.add(os.path.relpath(os.path.join(root, f), d))
missing = want - names
if missing:
    print(f"REFUSING: {d} lacks {sorted(missing)}", file=sys.stderr); sys.exit(47)
bad = sorted(n for n in names if re.search(r"(^|/)(DRAFT-|FAILED-)", n) or (n.lower().endswith(".zip") and n not in want))
if bad:
    print(f"REFUSING: {d} also holds {bad} — a draft, failed or foreign zip beside the package", file=sys.stderr); sys.exit(47)
lines = [l for l in open(os.path.join(d, f"MANIFEST-2.2.0_{h7}.txt"), encoding="utf-8").read().splitlines() if l.strip()]
if not lines or not re.fullmatch(r"MANIFEST COMPLETE: \d+ checks, 0 failed", lines[-1].strip()):
    print(f"REFUSING: the manifest's last line is {lines[-1] if lines else '<empty>'!r}, not 'MANIFEST COMPLETE: N checks, 0 failed'", file=sys.stderr); sys.exit(47)
with zipfile.ZipFile(os.path.join(d, f"NexusAI_plan-managed-ai_2.2.0_{h7}.zip")) as z:
    if sorted(z.namelist()) != ["createUiDefinition.json", "mainTemplate.json", "viewDefinition.json"]:
        print(f"REFUSING: plan zip entries are {sorted(z.namelist())}", file=sys.stderr); sys.exit(47)
    img = json.loads(z.read("mainTemplate.json"))["variables"].get("containerImage")
if img != ref:
    print(f"REFUSING: the ZIPPED template's containerImage is {img!r}, not the release reference", file=sys.stderr); sys.exit(47)
PY
RC=$?; [ "$RC" = 0 ] || exit "$RC"

# 31 — builder evidence, standing references and tools on disk.
for f in "$READY_MAIL" "$KAM_DOC" "$HANDOVER_G" "$CLAR" "$PRIOR_REPORT" \
         "$EVID_J/acr-build-2.2.0.log" "$EVID_J/anon-pull-smoke.log" "$EVID_J/anon-pull-smoke-run2.log" \
         "$EVID_J/demo-anchor-before.json" "$EVID_J/demo-after-5b.json" "$EVID_J/demo-redeploy-5b.log" \
         "$EVID_J/expect-step4.txt" "$EVID_J/expect-step4b.txt" "$EVID_J/step4-hold-run2.log" "$EVID_J/step4b-hold.log" \
         "$EVID_J/step4b-hold.sh" "$EVID_J/pkgmerge-A-accounting.txt" "$EVID_J/pkgmerge-hold.log" "$EVID_J/pkgmerge-commit-hold.log" \
         "$EVID_J/census-table.md" "$EVID_J/census-raw.txt" "$EVID_J/rd-new-c133.txt" "$EVID_J/rd-new-version.txt" \
         "$EVID_J/mail-09-c133.txt" "$EVID_J/mail-11-step4-stop.txt" "$EVID_J/mail-12-census.txt" \
         "$EVID_G/c57-accounting.txt" "$EVID_G/armttk.sh" "$EVID_G/c133-accounting.py" \
         "$NX/session-tools/c57-id-superset.sh" "$NX/session-tools/nexusai-lock.sh" \
         "$NX/session-tools/pwsh-v7.6.6.bYFB/pwsh" "$NX/session-tools/arm-ttk-20260213.TjXW/arm-ttk/arm-ttk/arm-ttk.psd1" \
         "$G7R1_FLOOR" "$G7R1_FLOORLIB"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "$HEAD_SHA" "$READY_MAIL" || grep -qF "$HEAD7" "$READY_MAIL" || { echo "REFUSING: the READY at $READY_MAIL does not name $HEAD7" >&2; exit 31; }

# 40 — the answer route exists.
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
grep -qF "$PRIOR_REPORT" "$BRIEF" || { echo "REFUSING: brief must name the prior package gate's report" >&2; exit 10; }

# 11 — identity.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, head, verdict route, key path, question route.
grep -q 'TIER 1' "$BRIEF" || { echo "REFUSING: brief does not declare TIER 1" >&2; exit 12; }
case "$PROMPT" in *"TIER 1"*) ;; *) echo "REFUSING: prompt does not declare TIER 1" >&2; exit 12 ;; esac
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$HEAD_SHA" "$MERGE_SHA" "$PKG_SHA" "$IMG_SHA" "$BASE_SHA" "$RELEASE_DIGEST" "$HEALTH_BUILD" "$DEMO_REV" "$ZIPDIR" "$READY_MAIL"; do
  grep -qF -- "$S" "$BRIEF" || { echo "REFUSING: brief must name $S" >&2; exit 14; }
  case "$PROMPT" in *"$S"*) ;; *) echo "REFUSING: prompt must name $S" >&2; exit 14 ;; esac
done
if printf '%s\n' "$PROMPT" | LC_ALL=C grep -q '@[A-Z_]*@'; then echo "REFUSING: the prompt carries a placeholder" >&2; exit 14; fi
case "$PROMPT" in *"MAIL YOUR VERDICT"*"tuesday-agent@agentmail.to"*) ;; *) echo "REFUSING: prompt must say MAIL YOUR VERDICT to tuesday-agent@agentmail.to" >&2; exit 15 ;; esac
case "$PROMPT" in *"$SUBJECT_STEM"*) ;; *) echo "REFUSING: prompt must carry the verdict subject stem" >&2; exit 15 ;; esac
grep -qF "$SUBJECT_STEM" "$BRIEF" || { echo "REFUSING: brief must carry the verdict subject stem" >&2; exit 15; }
case "$PROMPT" in *"/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env"*) ;; *) echo "REFUSING: prompt must name the AgentMail key by ABSOLUTE path" >&2; exit 20 ;; esac
for T in "$QUESTION_SUBJ" "$ANSWER_PREFIX" "$ROUTE_NAME"; do
  grep -qF -- "$T" "$BRIEF" || { echo "REFUSING: brief lacks the question route: $T" >&2; exit 20; }
  case "$PROMPT" in *"$T"*) ;; *) echo "REFUSING: prompt lacks the question route: $T" >&2; exit 20 ;; esac
done
if printf '%s\n' "$PROMPT" | grep -qi 'wednesday-agent@' && ! printf '%s\n' "$PROMPT" | grep -q 'Never wednesday-agent@'; then
  echo "REFUSING: the prompt routes to wednesday-agent@ — Datasec's coordinator is Tuesday" >&2; exit 15; fi

# 19 — the words the prompt must carry (% is a space); and the brief's sections.
WORDS="C-58 C-133 C-131 C-149 C-124 C-20 C-72 C-89 C-141 C-112 C-28 RD-657 RD-506 37-38 placeholderBack R1 R2 Q1 Q2
strictly%stronger POSITIVE%CONTROL%FIRST node%--check VOID SESSION_SECRET%UNSET arm-ttk hideconf hardloc gitleaks canary
DOCKER_CONFIG PER%ENTRY cp%without%-p MANIFEST%COMPLETE EXCLUSIVE qa-pkg220- QUEUE,%NEVER%TAKE%OVER DEADLINE HEARTBEAT
2%minutes 5%minutes finally NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED 4121/241 docker%rmi FOREGROUND"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 5. KNOWN RESIDUALS' '^## WRONG AT SOURCE' '^## PROVENANCE' '^## FILL AT READY'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for w in 'RD-657' '37-38' 'C-124' 'C-20' 'placeholderBack' 'strictly stronger' '23-id table' "$RD495_BLOB_BASE" "$RD495_BLOB_A"; do
  grep -qiF "$w" "$BRIEF" || grep -qF "${w:0:12}" "$BRIEF" || { echo "REFUSING: brief must carry '$w'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 53 / 59 / 60 / 61 / 65 / 71 — standing rules present in the brief (the prompt's are covered by 19).
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-pkg220-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST'; do
  grep -qF "$w" "$BRIEF" || { echo "REFUSING: brief lacks the standing rule '$w'" >&2; exit 53; }
done
grep -qF "$NOTTESTED_LINE" "$BRIEF" || { echo "REFUSING: brief must carry the NOT TESTED line verbatim" >&2; exit 71; }
case "$PROMPT" in *"$NOTTESTED_LINE"*) ;; *) echo "REFUSING: prompt must carry the NOT TESTED line verbatim" >&2; exit 71 ;; esac

# 38 — negative-control seats named in the brief; advisory if one has exited.
for P in $NEG_SEATS; do
  grep -q "\`$P\`" "$BRIEF" || { echo "REFUSING: brief does not name seat pid $P as a negative control" >&2; exit 38; }
  [ "$(ps -o comm= -p "$P" 2>/dev/null | sed 's#.*/##')" = "claude" ] || echo "NOTE: negative-control seat $P is not a running claude now — re-read the seats and update the brief's section 8 before launch" >&2
done

# Advisory — tools the optional legs use.
docker info >/dev/null 2>&1 || echo "NOTE: docker is not responding — the optional smoke boot and a dockerised gitleaks are NOT RUN; the registry-API pull does not need docker" >&2
command -v gitleaks >/dev/null 2>&1 || docker image inspect zricethezav/gitleaks:latest >/dev/null 2>&1 || echo "NOTE: no gitleaks binary or image found — Q10 needs one" >&2

# 32 — the coordinator stamps the self-check. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 6 7 8 18 22 35 41 42 43 44 45 47 31 40 10 17 11 12 13 14 15 20 19 24 53 71 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $BRANCH == $HEAD7 and mkt-release-gate-s78g == df70a96 at $PIN_TS (18); main ${M_ORIGIN:0:7}"
  echo "  chain: $HEAD7 <- 6f4945b = merge(df70a96, 0677388), tree 9ec70f87, base c0788b1 (6 7 8)"
  echo "  step-4 delta = the six files (22); counts 6f4945b $MERGE_COUNTS, head $EXP_COUNTS (35)"
  echo "  digest set in template / policy / README only where ruled; placeholder kept as the refusal rule (41 42 43)"
  echo "  C-133 rd495 blobs (44); health formula $HEALTH_BUILD (45); zip trio complete, 0 failed, zipped digest (47)"
  echo "  evidence + tools (31); route $ROUTE_NAME (40); report absent (17); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$BRANCH = $HEAD_SHA; refs/heads/mkt-release-gate-s78g = $PKG_SHA; refs/heads/main = ${M_ORIGIN:-unreadable}. These are the start-of-gate pins; take your own three readings anyway."

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
