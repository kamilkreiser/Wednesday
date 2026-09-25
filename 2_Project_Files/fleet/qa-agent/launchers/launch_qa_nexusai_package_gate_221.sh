#!/bin/bash
# launch_qa_nexusai_package_gate_221.sh — cross-project QA agent, TIER 1, THE PACKAGE GATE for the NexusAI 2.2.1
# Marketplace resubmission (C-158: RD-665, the availability test converted from a classic URL ping test to a Standard
# test). Target: branch rd-665-standard-webtest-s83l at the pinned HEAD_SHA (the fix d14a975 on the submitted 2.2.0 source
# c5da4d4, plus the 2.2.1 package commit), the non-draft 2.2.1 zips the builder produced, and the release image — UNCHANGED
# from 2.2.0 — nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda3309…7f66.
# The verdict decides whether Tuesday emails the 2.2.1 zip to Kam as ready to upload.
#
# PATTERN: launch_qa_nexusai_package_gate_220.sh. CHANGES vs 220, each deliberate:
#   - exit 9:  refuses while the HEAD / ZIPDIR / READY_MAIL / KAM_DOC placeholders are unsubstituted anywhere (brief, this
#              file's prompt, this file's variables), and while HEAD is not 40 hex. KAM_DOC is new (220 gate F-1).
#   - exit 18: RE-PIN by ls-remote: rd-665-standard-webtest-s83l must be EXACTLY the pinned head; mkt-release-2.2.0-s81j must
#              still be c5da4d4 (the submitted 2.2.0 source). main moving past 0677388 is a NOTE.
#   - exit 8:  the chain — d14a975's ONLY parent is c5da4d4; the PACKAGE COMMIT (read from the manifest's first line) descends
#              from d14a975 and is the head or an ancestor of it; package..head touches docs/resubmission/ only.
#   - exit 22: c5da4d4..d14a975 = EXACTLY the 3 fix files; d14a975..package = EXACTLY release-policy.json.
#   - exit 35: counts c5da4d4 4121/241, head 4125/242.
#   - exit 41: the template changed ONLY in the webtest resource (comments, Kind ping->standard, Configuration removed,
#              Request + ValidationRules added), containerImage still the release reference, the alert still points at it.
#   - exit 42: the policy changed ONLY by imageTagExceptions gaining exactly "2.2.1" = the same image; "2.2.0" and
#              imagePlaceholder byte-unchanged.
#   - exit 47: the zip dir holds exactly the 2.2.1 trio for the package commit, manifest names version 2.2.1 + the package
#              sha and ends 0 failed; the ZIPPED webtest is standard (scoped no-ping); the ZIPPED containerImage is the
#              release ref; per-entry vs the 2.2.0 zips: ONLY mainTemplate.json may differ; the 2.2.0 zips are unchanged.
#   - dropped from 220: exit 43 (README), exit 44 (rd495 C-133 blobs) — proved by the 2.2.0 gate on files 2.2.1 does not touch;
#              exit 22 now proves they are untouched.
#   - exit 40: the routing line QA/NexusAI-pkg221 exists in fleet/inbox_routing.conf.
#   - exit 46: the prompt and brief carry no instruction to use the customer-test identity (ct-az.sh) except as HELD.
#   - THE PROMPT IS EMBEDDED BELOW (heredoc). Every prompt guard applies to that text. exit 24 carried.
#
# LAUNCH IT IN A TMUX PANE (cockpit.sh add 'QA/NexusAI-pkg221' "bash '<this file>'"), NEVER nohup.
# Identity: exports NexusAI's OWN az/gh dirs (az READ-ONLY per brief §9 — NEVER the customer-test dir), CLAUDE_CONFIG_DIR
# pinned to Tuesday's project-local store.
# --check is READ-ONLY: git read verbs (cat-file, log, merge-base, diff, show, rev-parse, ls-remote), grep, ps, python3
# reading zips and git output. Nothing is written anywhere.
# ABSOLUTE PATHS ON PURPOSE. TRACKED in launchers/. Contains a legitimate `cd` (into the QA project, at exec).
# Usage: launch_qa_nexusai_package_gate_221.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..71 a guard refused
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
PH_KAMDOC='@KAM''_DOC@'
PH_STAMP='@STA''MP@'

QA_DIR='/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN'
TUE='/Volumes/KK_T9_External_HDD/TUESDAY'
BRIEF="$TUE/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-package-gate-221.md"
ROUTING="$TUE/2_Project_Files/fleet/inbox_routing.conf"
NX='/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI'
REPO="$NX/2_Project_Files"
EVID_L="$NX/session-tools/s83l"
EVID_G="$NX/session-tools/s78g"
EVID_CT="$NX/evidence-s83l-customer-test"
CLAR="$NX/1_Project_Definition/CLARIFICATIONS.md"
HANDOVER_L="$NX/HANDOVER-S83L.md"
PRIOR_REPORT="$QA_DIR/projects/nexusai/reports/2026-09-25-pkg-gate-220/report.md"
G7R1_FLOOR="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py"
G7R1_FLOORLIB="$QA_DIR/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorlib.sh"
REPORT="$QA_DIR/projects/nexusai/reports/2026-09-25-pkg-gate-221/report.md"
ID_ROOT="${QA_IDENTITY_ROOT_OVERRIDE:-$NX/4_Credentials}"
ROUTE_NAME='QA/NexusAI-pkg221'

BRANCH='rd-665-standard-webtest-s83l'
BRANCH_220='mkt-release-2.2.0-s81j'
HEAD_SHA="${QA_HEAD_SHA_OVERRIDE:-@HEAD@}"
ZIPDIR='@ZIPDIR@'
READY_MAIL='@READY_MAIL@'
KAM_DOC='@KAM_DOC@'
VERSION='2.2.1'
FIX_SHA='d14a975e6a325b0b246fbb85287b7831f22e5f33'       # RD-665 fix, ONLY parent = BASE_220
BASE_220='c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47'      # the submitted 2.2.0 source (the 2.2.0 gate's head)
PKG_220='3464dd80854c108063facfb0355ce1a4eed5fff8'       # the 2.2.0 package commit (the 2.2.0 zips' source)
IMG_SHA='0677388ab031ffaf569a52f6c0301af48f44aece'       # the image commit (C-149, C-72), unchanged
ZIPDIR_220="$NX/marketplace-submission-2026-09-25-2.2.0"
ZIP220_PLAN='NexusAI_plan-managed-ai_2.2.0_3464dd8.zip'
ZIP220_LIST='NexusAI_listing-assets_2.2.0_3464dd8.zip'
ZIP220_PLAN_SHA='18155587c6cb0141b35d082b25fcccae9f3b8683189208dac3cf701790eef21c'
ZIP220_LIST_SHA='c333f95c328c1a0dceb19b9a47ec16721d05742b597d6659446c25159da7ecbe'

RELEASE_DIGEST='sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66'
RELEASE_REF="nexusaireleaseacr.azurecr.io/nexusai@$RELEASE_DIGEST"
HEALTH_BUILD='b6f4bfddadcd4055'

COUNTS_FILE='scripts/verify-expected-counts.json'
TEMPLATE='azure-marketplace/combined/mainTemplate.json'
POLICY='azure-marketplace/release-policy.json'
RD665_TEST='__tests__/rd665-standard-availability-test.test.js'
FIX_FILES="$RD665_TEST
$TEMPLATE
$COUNTS_FILE"
BASE_COUNTS='4121 241'
EXP_COUNTS="${QA_EXP_COUNTS_OVERRIDE:-4125 242}"

NEG_SEATS='29171 60235'   # NexusAI seat claude (%8), Tuesday claude (%0), read 2026-09-25 ~18:30 AEST

SUBJECT_STEM='[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.1: '
QUESTION_SUBJ='[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>'
ANSWER_PREFIX='[Tuesday -> QA/NexusAI-pkg221] ANSWER'
NOTTESTED_LINE="Real Azure: not deployed through Partner Center; the 2.2.1 template was not deployed, validated or what-if'd against real Azure by this gate (the builder's create-time proof in 73e9b141 is RELAYED, not re-tested); the Key Vault success path is observed at log level only (C-124 update), its admin-health fields never measured; the jest suites are not network-sandboxed (C-58)."

g() { git --no-optional-locks -C "$REPO" "$@"; }
sorted() { printf '%s\n' "$1" | sed '/^$/d' | sort; }
counts_at() { g show "$1:$COUNTS_FILE" 2>/dev/null | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["tests"], d["suites"])' 2>/dev/null; }

# ---------------------------------------------------------------- THE PROMPT (embedded; guarded below like a prompt file)
PROMPT=''
read -r -d '' PROMPT <<'PROMPT_EOF' || true
ultrathink

You are the fleet QA/testing agent running ONE gate, TIER 1: THE PACKAGE GATE for the Datasec/NexusAI 2.2.1 Azure Marketplace resubmission (C-158, RD-665). One target, one verdict: GO, GO WITH FINDINGS or NO GO FOR UPLOAD. Your verdict decides whether Tuesday emails the 2.2.1 zip to Kam as ready for him to upload to Partner Center himself, replacing the live 2.2.0 plan package. Nothing checks the zip after you.

READ YOUR COMMISSION FIRST, whole: /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-25_nexusai-package-gate-221.md
Then the charter it names, then the 2.2.0 package gate's report it names as PRIOR ROUND (your baseline). Every builder statement is a CLAIM, never evidence.

THE TARGET. Branch rd-665-standard-webtest-s83l at @HEAD@. The RD-665 fix is d14a975e6a325b0b246fbb85287b7831f22e5f33, whose ONLY parent is c5da4d4d77b76a474b1842cfed9e6fe82fe1cd47 (the submitted 2.2.0 source, gated GO WITH FINDINGS); the 2.2.1 package commit follows it and only adds imageTagExceptions["2.2.1"]. The builder's non-draft zips and manifest are in @ZIPDIR@ (copy before unzipping; never write there); the 2.2.0 zips are in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/marketplace-submission-2026-09-25-2.2.0 (same rule). The release image is UNCHANGED: nexusaireleaseacr.azurecr.io/nexusai@sha256:fdda33098c36a484b50a9a761660bb69bc53f5ed238ffceeb1bd038c8eb77f66 (tag 2.2.0, from 0677388ab031ffaf569a52f6c0301af48f44aece; health build b6f4bfddadcd4055). The builder's READY is @READY_MAIL@. The handover doc that goes to Kam with the zip is @KAM_DOC@.

THE DELTA FROM c5da4d4 IS EXACTLY FOUR FILES: the template's ONE Microsoft.Insights/webtests resource (Kind ping -> standard, the classic WebTest XML Configuration removed, Request + ValidationRules added, same resource name so the availability metric alert is unchanged), the new RD-665 test file, the counts file (4121/241 -> 4125/242), and release-policy.json (imageTagExceptions gains exactly "2.2.1" with the SAME image). Prove it by parsing, and prove everything else is byte-identical, so the 2.2.0 gate's proofs still cover it.

(a) THE RD-665 FIX IN THE PACKAGED TEMPLATE, read from your copy of the builder's plan zip: one webtest, Kind standard, no Configuration, no <WebTest anywhere, Request GET to /api/health on the ingress fqdn, ValidationRules status 200, same frequency, timeout, retries and three locations as the ping test. THE NO-PING CHECK IS SCOPED, NOT A TEXT SEARCH: the file legitimately contains the substring "ping" (the conversion comment, the Azure OpenAI check's 1-token prompt, identifiers like kvWrappingKeyName) — the binding check is that no key or value under any webtest resource's properties contains "ping", no "Kind": "ping" anywhere, no <WebTest anywhere; classify every remaining hit by JSON path. Control: put the c5da4d4 ping block back into a COPY and the RD-665 suite must redden.

(b) THE VERSION: 2.2.1 in both zip names, the manifest name, the manifest's first line with the full package commit sha, its tag-exception line, and the policy key. No shipped file carries a version (contentVersion 1.3.0.0 unchanged) — confirm. POSITIVE CONTROL FIRST: the clean files green. Then your own arms through the REAL build script: V1 the "2.2.1" key removed (predict exit 1), V2 the "2.2.1" image one hex off (predict exit 1), V3 version 2.2.0 on the shipped files (predict exit 0). Every package jest cell builds version '2.2.0', so run V2 through the named package suites too: if nothing reddens, that is a finding. A RED ARM COUNTS ONLY IF THE MUTANT STILL PARSES: node --check every mutated .js, JSON.parse every mutated .json, quote the exit code; a red from a mutant that does not parse is a VOID arm.

(c) THE IMAGE IS UNCHANGED AND STILL ANONYMOUSLY PULLABLE: the zipped containerImage equals the 2.2.0 zip's and the release reference character for character. Re-verify anonymous pull YOURSELF through the registry API with no credentials: anonymous token, GET the manifest by digest, its bytes' sha256 must equal the digest; GET the config blob and one layer by digest and hash them; read the labels. Negative controls in the same window: no token is 401; the dev registry refuses an anonymous token. NEVER docker rmi the release image. If you docker pull, use a fresh DOCKER_CONFIG holding {} with DOCKER_HOST pinned, and read the exit code. At most ONE GET /api/health to the demo host in the brief; build must be b6f4bfddadcd4055; version "2.0.1" is RD-657, NOT a failure.

(d) THE 2.2.1 ZIPS AGAINST THE 2.2.0 ZIPS, PER ENTRY: identical entry names; the ONLY entry allowed to differ is mainTemplate.json, and inside it ONLY the webtest resource. createUiDefinition.json, viewDefinition.json and all listing entries byte-identical to 2.2.0's. Version fields, release-policy.json and the handover doc are not zip entries; one appearing inside a zip is a finding. Any other difference is a finding. Whole-file zip shas will differ (entry timestamps) — not a finding on its own. Hash the 2.2.0 zips at start and end: they are what is live.

REBUILD THE PACKAGE YOURSELF with scripts/marketplace-package-build.sh (non-draft, version 2.2.1, a NEW empty out-dir in your own project, with the cwd inside your own git archive extract of the package commit, because the listing-list argument is a filesystem path — 2.2.0 gate F-6). PREDICT FIRST: listing zip whole-file sha should match; plan zip probably not (cp without -p). The binding comparison is PER ENTRY against git show at the package commit. Both manifests must end "MANIFEST COMPLETE: <N> checks, 0 failed"; explain every differing line. No DRAFT- or FAILED- file.

ARM-TTK: S78G's runner (session-tools/s78g/armttk.sh) on the package commit with tag pkg221, quote N/M (builder: 49/49), BOTH controls (hideconf, hardloc) must fire; TMPDIR inside your own project. Then the three files unpacked from the builder's plan zip. Say whether any arm-ttk test inspects webtests at all.

(e) THE CREATE-TIME PROOF IS RELAYED, NOT RE-TESTED. Read evidence-s83l-customer-test/RD665-webtest-readback.json, RD665-alert-readback.json and RD665-availability-results.json and say what they show and what they do not: the read-back says Enabled true, so "then disabled" has no artefact; there is no deployment-operation record and no record of which template blob was deployed. You do NOT use Azure in the customer-test tenant: never run session-tools/s83l/ct-az.sh, never use 4_Credentials/.azure-customer-test, never contact any nxcusttest host, no what-if. That is HELD unless the brief's section 9 carries a signed line from Tuesday granting it.

GITLEAKS: run gitleaks over the unpacked 2.2.1 zips, the manifest and the handover doc (copies in your own dir), with the repo's config at the head AND the default rules. POSITIVE CONTROL FIRST: a planted canary the ruleset TARGETS must fire in the same run. THE HANDOVER DOC: check every value against your measurements (version 2.2.1, the package commit, zip names and sha256s, counts 4125/242, arm-ttk, the unchanged digest, why 2.2.1 replaces 2.2.0); a 2.2.0 value presented as 2.2.1's, an unfilled value, or a disagreement is a finding, because it goes to Kam in the same email.

FULL VERIFY at the head under the jest lock, SESSION_SECRET UNSET (env -u SESSION_SECRET; print SET or UNSET as the hold's first line, the NAME only), npm run verify -- --maxWorkers=2 on a tree you built. Predicted 4125/242 — confirm or contradict. Account for every test id at c5da4d4 and at the head: the only change allowed is the four new RD-665 ids; a missing id is a Major. C-89 on your own copy.

KNOWN RESIDUALS — LIST, DO NOT FAIL: RD-657 (health says 2.0.1); the stale comment at the build script's lines 37-38; C-124 as UPDATED (Key Vault success observed at log level only on the 2.2.0 customer test; admin-health fields never measured); C-20 (this gate does not deploy or validate against real Azure); the 2.2.0 gate's F-3 (no cell catches a consistent wrong digest).

TREES AND WRITES. Build every tree INSIDE YOUR OWN PROJECT from the object store (git archive into a fresh mktemp dir under projects/nexusai/qa-trees/pkg221.*). Each tree is EXCLUSIVE to this gate and to one purpose. In the NexusAI repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep, merge-base, archive); never fetch, pull, push, checkout, worktree, commit, stash, gc, clean or merge-tree --write-tree, and never work in its 2_Project_Files checkout or the builder's worktrees (C-28). Count the repo's object files before and after and account for any delta by mtime. Findings-only: no commits, no tickets, no edits in NexusAI, no replacement zip, never merge the branch anywhere. No push, no registry change, no demo change, no Partner Center (C-23: Kam uploads himself), no mail to any human. Never rm: quarantine. Prior-work check: before calling anything missing, wrong or new, search what was built before and why, and cite it.

FLOOR DISCIPLINE — section 8 of the brief exactly. QUEUE, NEVER TAKE OVER. Every jest run goes through session-tools/nexusai-lock.sh with a tag starting qa-pkg221- (C-141), the lock held once per multi-run measurement as a tracked child of your seat; docker legs through the docker lock. Count foreign servers the RD-606 way anchored on YOUR OWN claude pid, with the brief's negative-control seats classifying foreign in the same run. A zero is reportable only beside a control that fired in the same window. DEADLINE AND HEARTBEAT: every probe and network request has a per-step DEADLINE and a client timeout, every server is killed in a finally, a HEARTBEAT line at least every 2 minutes during a hold, and a step with no heartbeat for 5 minutes is aborted and reported.

NETWORK: only nexusaireleaseacr.azurecr.io, one anonymous token request to the dev registry as the negative control, and at most one GET /api/health to the demo. Everything else on 127.0.0.1. This is authorised defensive QA of Datasec's own release artefacts; if a response is cut off by a safety check, record it and continue with the next item.

RE-PIN at start, mid and end: the head on rd-665-standard-webtest-s83l, c5da4d4 on mkt-release-2.2.0-s81j, and main — three timestamped readings with the branch name beside each sha. A head that disagrees with the brief is a FINDING and a reason to stop, never a typo to fix.

QUESTIONS: your routing name is QA/NexusAI-pkg221. If you must ask, mail tuesday-agent@agentmail.to with subject "[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>" and PROCEED ON THE SAFEST READING without waiting; Tuesday's answer arrives in tuesday-agent@agentmail.to with a subject beginning "[Tuesday -> QA/NexusAI-pkg221] ANSWER". Approval-class items are NOT RUN and named, never done on a safe reading. Record every question, reading and answer in the report.

Write your report to: /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-25-pkg-gate-221/report.md

MAIL YOUR VERDICT to tuesday-agent@agentmail.to with a subject beginning exactly:
[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — package gate 2.2.1: <GO | GO WITH FINDINGS | NO GO FOR UPLOAD> @ <the first 7 characters of the pinned head> Lead the body with one sentence: is the zip ready for Tuesday to email to Kam, and if not, what stops it. Never wednesday-agent@. You have no inbox that wakes you, so a verdict you do not mail is lost.

The AgentMail key is AGENTMAIL_API_KEY in /Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env. It is an absolute path because the QA project has no 4_Credentials directory of its own. Never put the key or any secret in a mail or the report.

Run long commands in the FOREGROUND. Never end a turn waiting on a background notice.

Rule 2 stands: what you did NOT test is first-class output — a NOT TESTED section, and every action recommendation labelled MEASURED AT RUNTIME, PROBED or READ ONLY. That section must carry this line verbatim:
Real Azure: not deployed through Partner Center; the 2.2.1 template was not deployed, validated or what-if'd against real Azure by this gate (the builder's create-time proof in 73e9b141 is RELAYED, not re-tested); the Key Vault success path is observed at log level only (C-124 update), its admin-health fields never measured; the jest suites are not network-sandboxed (C-58).
PROMPT_EOF

# ---------------------------------------------------------------- GUARDS
[ -d "$QA_DIR" ]  || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]   || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -n "$PROMPT" ]  || { echo "embedded prompt is empty" >&2; exit 4; }
[ -d "$REPO/.git" ] || [ -f "$REPO/.git" ] || { echo "repo under test missing: $REPO" >&2; exit 5; }

# 9 — nothing unsubstituted. The head must be a full 40-hex sha.
for PH in "$PH_HEAD" "$PH_ZIP" "$PH_READY" "$PH_KAMDOC"; do
  if grep -qF "$PH" "$BRIEF"; then echo "REFUSING: the brief still carries $PH — fill it at READY" >&2; exit 9; fi
  case "$PROMPT" in *"$PH"*) echo "REFUSING: the embedded prompt still carries $PH — sed this launcher at READY" >&2; exit 9 ;; esac
done
[ "$HEAD_SHA" != "$PH_HEAD" ] || { echo "REFUSING: HEAD_SHA is still the placeholder" >&2; exit 9; }
[ "$ZIPDIR" != "$PH_ZIP" ] && [ "$READY_MAIL" != "$PH_READY" ] && [ "$KAM_DOC" != "$PH_KAMDOC" ] || {
  echo "REFUSING: ZIPDIR, READY_MAIL or KAM_DOC is still a placeholder" >&2; exit 9; }
[[ "$HEAD_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: HEAD_SHA '$HEAD_SHA' is not a full 40-hex sha" >&2; exit 9; }
HEAD7="${HEAD_SHA:0:7}"

# 47a — the package commit is read from the builder's manifest (it names the zips), so the zip dir must be sane first.
[ -d "$ZIPDIR" ] || { echo "REFUSING: builder zip dir missing: $ZIPDIR" >&2; exit 47; }
MANIFESTS="$(ls "$ZIPDIR"/MANIFEST-"$VERSION"_*.txt 2>/dev/null)"
[ "$(printf '%s\n' "$MANIFESTS" | sed '/^$/d' | wc -l | tr -d ' ')" = "1" ] || {
  echo "REFUSING: $ZIPDIR must hold exactly one MANIFEST-${VERSION}_*.txt; found: ${MANIFESTS:-<none>}" >&2; exit 47; }
PKGC_SHA="$(head -1 "$MANIFESTS" | sed -n "s/^NexusAI Marketplace upload package — version $VERSION, commit \([0-9a-f]\{40\}\)\$/\1/p")"
[[ "$PKGC_SHA" =~ ^[0-9a-f]{40}$ ]] || { echo "REFUSING: the manifest's first line does not read 'version $VERSION, commit <40-hex>' (non-draft): $(head -1 "$MANIFESTS")" >&2; exit 47; }
PKGC7="${PKGC_SHA:0:7}"

# 6 — every pinned sha is a commit in the object store (this launcher never fetches).
for S in "$HEAD_SHA" "$PKGC_SHA" "$FIX_SHA" "$BASE_220" "$PKG_220" "$IMG_SHA"; do
  T="$(g cat-file -t "$S" 2>&1)"
  [ "$T" = "commit" ] || { echo "REFUSING: $S is not a commit in $REPO (got '$T')" >&2; exit 6; }
done

# 8 — the chain.
[ "$(g log -1 --format='%P' "$FIX_SHA" 2>/dev/null)" = "$BASE_220" ] || { echo "REFUSING: d14a975's parent list is not exactly c5da4d4" >&2; exit 8; }
g merge-base --is-ancestor "$FIX_SHA" "$PKGC_SHA" 2>/dev/null && [ "$PKGC_SHA" != "$FIX_SHA" ] || {
  echo "REFUSING: the package commit $PKGC7 does not strictly descend from d14a975" >&2; exit 8; }
g merge-base --is-ancestor "$PKGC_SHA" "$HEAD_SHA" 2>/dev/null || { echo "REFUSING: $HEAD7 does not descend from the package commit $PKGC7" >&2; exit 8; }
_DOCD="$(g diff --name-only "$PKGC_SHA" "$HEAD_SHA" 2>/dev/null | grep -v '^docs/resubmission/')"
[ -z "$_DOCD" ] || { echo "REFUSING: $PKGC7..$HEAD7 touches more than docs/resubmission/: $_DOCD" >&2; exit 8; }
[ "$(g diff --name-only "$PKG_220" "$BASE_220" 2>/dev/null)" = "docs/resubmission/2026-09-22_resubmission-handover-for-kam.md" ] || {
  echo "REFUSING: 3464dd8..c5da4d4 is no longer only the 2.2.0 handover doc — the 2.2.0 baseline moved" >&2; exit 8; }

# 18 — RE-PIN NOW by ls-remote. The branch must be at origin (C-113) and exactly the pinned head.
L="$(g ls-remote origin "refs/heads/$BRANCH" 2>&1)"
printf '%s\n' "$L" | grep -q "^${HEAD_SHA}[[:space:]]refs/heads/${BRANCH}\$" || {
  echo "REFUSING: origin refs/heads/$BRANCH is not $HEAD_SHA — not pushed, or moved; re-brief. ls-remote said:" >&2; printf '%s\n' "${L:-<nothing>}" >&2; exit 18; }
L2="$(g ls-remote origin "refs/heads/$BRANCH_220" 2>&1)"
printf '%s\n' "$L2" | grep -q "^${BASE_220}[[:space:]]refs/heads/${BRANCH_220}\$" || {
  echo "REFUSING: origin $BRANCH_220 is not c5da4d4 — the submitted 2.2.0 source moved; re-brief" >&2; printf '%s\n' "$L2" >&2; exit 18; }
M_ORIGIN="$(g ls-remote origin refs/heads/main 2>/dev/null | awk '{print $1}')"
[ "$M_ORIGIN" = "$IMG_SHA" ] || echo "NOTE: origin main is now ${M_ORIGIN:-unreadable}, not 0677388 — not a refusal (C-149 pins the image commit); the gate reports what moved (brief Q0)" >&2
PIN_TS="$(date '+%Y-%m-%d %H:%M:%S %Z')"

# 22 — the deltas are EXACTLY the commissioned files.
GOT="$(g diff --name-only "$BASE_220" "$FIX_SHA" 2>/dev/null | sort)"
[ "$GOT" = "$(sorted "$FIX_FILES")" ] || { echo "REFUSING: c5da4d4..d14a975 is not exactly the three fix files. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }
GOT="$(g diff --name-only "$FIX_SHA" "$PKGC_SHA" 2>/dev/null)"
[ "$GOT" = "$POLICY" ] || { echo "REFUSING: d14a975..$PKGC7 is not exactly $POLICY. Got:" >&2; printf '%s\n' "$GOT" >&2; exit 22; }

# 35 — counts.
CT="$(counts_at "$BASE_220")"; [ "$CT" = "$BASE_COUNTS" ] || { echo "REFUSING: counts at c5da4d4 read '${CT:-unreadable}', not '$BASE_COUNTS'" >&2; exit 35; }
CT="$(counts_at "$HEAD_SHA")"; [ "$CT" = "$EXP_COUNTS" ] || {
  echo "REFUSING: counts at $HEAD7 read '${CT:-unreadable}', not '$EXP_COUNTS' — confirm against the READY and set EXP_COUNTS (and the brief)" >&2; exit 35; }

# 41 / 42 — the template and the policy changed ONLY where RD-665 and the 2.2.1 package say.
python3 - "$REPO" "$BASE_220" "$PKGC_SHA" "$TEMPLATE" "$POLICY" "$RELEASE_REF" "$VERSION" <<'PY'
import json, subprocess, sys, copy
repo, base, pkg, tpath, ppath, ref, ver = sys.argv[1:8]
def show(sha, p):
    return json.loads(subprocess.run(["git", "--no-optional-locks", "-C", repo, "show", f"{sha}:{p}"],
                                     check=True, capture_output=True).stdout)
def die(code, msg): print("REFUSING: " + msg, file=sys.stderr); sys.exit(code)
tb, tp = show(base, tpath), show(pkg, tpath)
for name, t in (("c5da4d4", tb), ("package", tp)):
    if t["variables"].get("containerImage") != ref: die(41, f"containerImage at {name} is not the release reference")
wb = [i for i, r in enumerate(tb["resources"]) if r.get("type") == "Microsoft.Insights/webtests"]
wp = [i for i, r in enumerate(tp["resources"]) if r.get("type") == "Microsoft.Insights/webtests"]
if len(wb) != 1 or wb != wp: die(41, f"expected ONE webtest at the same index in both templates: {wb} vs {wp}")
i = wb[0]; ob, op = tb["resources"][i], tp["resources"][i]
if ob["properties"].get("Kind") != "ping": die(41, "the webtest at c5da4d4 is not the ping test the commission describes")
pr = op["properties"]
if pr.get("Kind") != "standard": die(41, f"webtest Kind at the package commit is {pr.get('Kind')!r}, not 'standard'")
if "Configuration" in pr: die(41, "the Standard webtest still carries Configuration")
rq, vr = pr.get("Request") or {}, pr.get("ValidationRules") or {}
if rq.get("HttpVerb") != "GET" or "/api/health" not in str(rq.get("RequestUrl", "")): die(41, f"Request is not GET /api/health: {rq!r}")
if vr.get("ExpectedHttpStatusCode") != 200: die(41, f"ValidationRules.ExpectedHttpStatusCode is not 200: {vr!r}")
if "ping" in json.dumps(pr).lower(): die(41, "the word 'ping' appears inside the webtest's properties")
if op["name"] != ob["name"]: die(41, "the webtest resource name changed — the alert would lose it")
# everything outside the allowed keys is identical
a, b = copy.deepcopy(tb), copy.deepcopy(tp)
for t in (a, b):
    w = t["resources"][i]; w.pop("comments", None)
    for k in ("Kind", "Configuration", "Request", "ValidationRules"): w["properties"].pop(k, None)
if a != b: die(41, "the template changed outside the webtest's comments/Kind/Configuration/Request/ValidationRules")
wid = f"[resourceId('Microsoft.Insights/webtests', concat(parameters('siteName'), '-availability-test'))]"
if op["name"] != "[concat(parameters('siteName'), '-availability-test')]" or wid not in json.dumps(tp): die(41, "no resource references the webtest by its id")
# policy
pb, pp = show(base, ppath), show(pkg, ppath)
if pb.get("imagePlaceholder") != pp.get("imagePlaceholder") or not pp.get("imagePlaceholder"): die(42, "imagePlaceholder changed or vanished")
eb, ep = pb.get("imageTagExceptions") or {}, pp.get("imageTagExceptions") or {}
if sorted(ep) != sorted(list(eb) + [ver]) or ver in eb: die(42, f"imageTagExceptions keys went {sorted(eb)} -> {sorted(ep)}, not +['{ver}'] exactly")
if ep["2.2.0"] != eb.get("2.2.0"): die(42, "the '2.2.0' exception entry changed")
if not isinstance(ep[ver], dict) or ep[ver].get("image") != ref or ep["2.2.0"].get("image") != ref: die(42, f"the '{ver}' exception image is not exactly the release reference (== 2.2.0's)")
x, y = {k: v for k, v in pb.items() if k != "imageTagExceptions"}, {k: v for k, v in pp.items() if k != "imageTagExceptions"}
if x != y: die(42, "release-policy changed outside imageTagExceptions")
PY
RC=$?; [ "$RC" = 0 ] || exit "$RC"
g show "$HEAD_SHA:scripts/marketplace-package-build.sh" 2>/dev/null | sed -n '37,38p' | grep -qi 'every build fails today' \
  || echo "NOTE: the known stale comment is no longer at marketplace-package-build.sh:37-38 — re-read the brief's residual line" >&2

# 45 — the health build formula (image unchanged).
HB="$(python3 -c 'import hashlib,sys; print(hashlib.sha256(sys.argv[1].encode()).hexdigest()[:16])' "$IMG_SHA")"
[ "$HB" = "$HEALTH_BUILD" ] || { echo "REFUSING: sha256(0677388)[:16] is $HB, not $HEALTH_BUILD" >&2; exit 45; }

# 47 — the builder's 2.2.1 trio, the zipped fix, and the per-entry diff against the (unchanged) 2.2.0 zips.
python3 - "$ZIPDIR" "$PKGC7" "$RELEASE_REF" "$VERSION" "$ZIPDIR_220" "$ZIP220_PLAN" "$ZIP220_LIST" "$ZIP220_PLAN_SHA" "$ZIP220_LIST_SHA" "$REPO" "$PKGC_SHA" "$TEMPLATE" <<'PY'
import hashlib, json, os, re, subprocess, sys, zipfile, copy
d, h7, ref, ver, d0, p0, l0, p0sha, l0sha, repo, pkg, tpath = sys.argv[1:13]
def die(msg): print("REFUSING: " + msg, file=sys.stderr); sys.exit(47)
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
want = {f"NexusAI_plan-managed-ai_{ver}_{h7}.zip", f"NexusAI_listing-assets_{ver}_{h7}.zip", f"MANIFEST-{ver}_{h7}.txt"}
names = set()
for root, dirs, files in os.walk(d):
    for f in files: names.add(os.path.relpath(os.path.join(root, f), d))
if want - names: die(f"{d} lacks {sorted(want - names)}")
bad = sorted(n for n in names if re.search(r"(^|/)(DRAFT-|FAILED-)", n) or (n.lower().endswith(".zip") and n not in want))
if bad: die(f"{d} also holds {bad} — a draft, failed or foreign zip beside the package")
lines = [l for l in open(os.path.join(d, f"MANIFEST-{ver}_{h7}.txt"), encoding="utf-8").read().splitlines() if l.strip()]
if not re.fullmatch(r"MANIFEST COMPLETE: \d+ checks, 0 failed", lines[-1].strip()): die(f"manifest last line is {lines[-1]!r}")
if not any(f"differs from version {ver} under a committed exception" in l for l in lines): die(f"manifest has no tag-exception PASS line for version {ver}")
# the 2.2.0 zips are what is live: unchanged on disk
if sha(os.path.join(d0, p0)) != p0sha or sha(os.path.join(d0, l0)) != l0sha: die("the 2.2.0 zips on disk no longer hash to the recorded values")
zp, zl = zipfile.ZipFile(os.path.join(d, f"NexusAI_plan-managed-ai_{ver}_{h7}.zip")), zipfile.ZipFile(os.path.join(d, f"NexusAI_listing-assets_{ver}_{h7}.zip"))
zp0, zl0 = zipfile.ZipFile(os.path.join(d0, p0)), zipfile.ZipFile(os.path.join(d0, l0))
if sorted(zp.namelist()) != ["createUiDefinition.json", "mainTemplate.json", "viewDefinition.json"]: die(f"plan zip entries are {sorted(zp.namelist())}")
if sorted(zp.namelist()) != sorted(zp0.namelist()) or sorted(zl.namelist()) != sorted(zl0.namelist()): die("entry-name sets differ from the 2.2.0 zips")
for z, z0 in ((zp, zp0), (zl, zl0)):
    for n in z.namelist():
        if n != "mainTemplate.json" and z.read(n) != z0.read(n): die(f"entry {n} differs from 2.2.0 — only mainTemplate.json may")
raw = zp.read("mainTemplate.json")
if raw != subprocess.run(["git", "--no-optional-locks", "-C", repo, "show", f"{pkg}:{tpath}"], check=True, capture_output=True).stdout:
    die("the zipped mainTemplate.json is not byte-identical to the package commit's template")
t, t0 = json.loads(raw), json.loads(zp0.read("mainTemplate.json"))
if t["variables"].get("containerImage") != ref or t0["variables"].get("containerImage") != ref: die("the zipped containerImage is not the release reference in both versions")
if b"<WebTest" in raw or re.search(rb'"Kind"\s*:\s*"ping"', raw): die("the zipped template still carries a classic ping test")
ws = [r for r in t["resources"] if r.get("type") == "Microsoft.Insights/webtests"]
if len(ws) != 1 or ws[0]["properties"].get("Kind") != "standard" or "ping" in json.dumps(ws[0]["properties"]).lower(): die("the zipped webtest is not a single Standard test free of 'ping'")
a, b = copy.deepcopy(t0), copy.deepcopy(t)
for x in (a, b):
    for r in x["resources"]:
        if r.get("type") == "Microsoft.Insights/webtests":
            r.pop("comments", None)
            for k in ("Kind", "Configuration", "Request", "ValidationRules"): r["properties"].pop(k, None)
if a != b: die("the zipped template differs from 2.2.0's outside the webtest")
PY
RC=$?; [ "$RC" = 0 ] || exit "$RC"

# 31 — builder evidence, standing references and tools on disk.
for f in "$READY_MAIL" "$KAM_DOC" "$HANDOVER_L" "$CLAR" "$PRIOR_REPORT" \
         "$EVID_CT/RD665-webtest-readback.json" "$EVID_CT/RD665-alert-readback.json" "$EVID_CT/RD665-availability-results.json" \
         "$EVID_CT/T4-restart-log.json" "$EVID_L/ct-az.sh" \
         "$EVID_G/armttk.sh" "$NX/session-tools/nexusai-lock.sh" \
         "$NX/session-tools/pwsh-v7.6.6.bYFB/pwsh" "$NX/session-tools/arm-ttk-20260213.TjXW/arm-ttk/arm-ttk/arm-ttk.psd1" \
         "$G7R1_FLOOR" "$G7R1_FLOORLIB"; do
  [ -s "$f" ] || { echo "REFUSING: evidence or tool absent: $f" >&2; exit 31; }
done
grep -qF "$HEAD_SHA" "$READY_MAIL" || grep -qF "$HEAD7" "$READY_MAIL" || { echo "REFUSING: the READY at $READY_MAIL does not name $HEAD7" >&2; exit 31; }
[ -s "$EVID_L/armttk-$PKGC7.txt" ] || echo "NOTE: no builder arm-ttk result at $EVID_L/armttk-$PKGC7.txt — the 49/49 claim is READY-only" >&2

# 40 — the answer route exists.
grep -q "^${ROUTE_NAME}|tuesday-agent@agentmail.to|" "$ROUTING" || {
  echo "REFUSING: no '${ROUTE_NAME}|tuesday-agent@agentmail.to|…' line in $ROUTING — answers to the gate would have no route" >&2; exit 40; }

# 10 / 17 — report path named in both; no stale report.
grep -qF "$REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the report path $REPORT" >&2; exit 10; }
case "$PROMPT" in *"$REPORT"*) ;; *) echo "REFUSING: prompt does not name the report path" >&2; exit 10 ;; esac
[ ! -e "$REPORT" ] || { echo "REFUSING: $REPORT already exists — a stale report would read as this gate's" >&2; exit 17; }
grep -qF "$PRIOR_REPORT" "$BRIEF" || { echo "REFUSING: brief must name the 2.2.0 package gate's report" >&2; exit 10; }

# 11 — identity: NexusAI's OWN dirs, never the customer-test one.
[ -d "$ID_ROOT/.azure" ] && [ -d "$ID_ROOT/.gh-config" ] || {
  echo "REFUSING: NexusAI identity dirs missing under $ID_ROOT (.azure / .gh-config) — would inherit the caller's" >&2; exit 11; }
export AZURE_CONFIG_DIR="$ID_ROOT/.azure"
export GH_CONFIG_DIR="$ID_ROOT/.gh-config"
export CLAUDE_CONFIG_DIR="$TUE/4_Credentials/.claude"
case "$AZURE_CONFIG_DIR" in *customer-test*) echo "REFUSING: AZURE_CONFIG_DIR points at the customer-test identity" >&2; exit 11 ;; esac

# 12 / 13 / 14 / 15 / 20 — tier, directive, brief path, pins, verdict route, key path, question route.
grep -q 'TIER 1' "$BRIEF" || { echo "REFUSING: brief does not declare TIER 1" >&2; exit 12; }
case "$PROMPT" in *"TIER 1"*) ;; *) echo "REFUSING: prompt does not declare TIER 1" >&2; exit 12 ;; esac
[ "$(printf '%s\n' "$PROMPT" | head -1)" = "ultrathink" ] || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 13; }
case "$PROMPT" in *"$BRIEF"*) ;; *) echo "REFUSING: prompt must name the brief path" >&2; exit 14 ;; esac
for S in "$HEAD_SHA" "$FIX_SHA" "$BASE_220" "$IMG_SHA" "$RELEASE_DIGEST" "$HEALTH_BUILD" "$ZIPDIR" "$READY_MAIL" "$KAM_DOC"; do
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
WORDS="C-158 C-58 C-124 C-20 C-23 C-28 C-89 C-141 RD-665 RD-657 37-38 F-3 F-6 V1 V2 V3 standard ValidationRules
SCOPED <WebTest RELAYED ct-az.sh customer-test PER%ENTRY POSITIVE%CONTROL%FIRST node%--check VOID SESSION_SECRET%UNSET
arm-ttk hideconf hardloc gitleaks canary DOCKER_CONFIG cp%without%-p MANIFEST%COMPLETE EXCLUSIVE qa-pkg221- QUEUE,%NEVER%TAKE%OVER
DEADLINE HEARTBEAT 2%minutes 5%minutes finally NOT%TESTED MEASURED%AT%RUNTIME READ%ONLY PROBED 4125/242 docker%rmi FOREGROUND
never%merge Prior-work%check"
for w in $WORDS; do
  w="${w//%/ }"
  case "$PROMPT" in *"$w"*) ;; *) echo "REFUSING: prompt must carry '$w'" >&2; exit 19 ;; esac
done
for H in '^## PRIOR ROUND' '^## 2a. LEGITIMATE SHAPES' '^## 5. KNOWN RESIDUALS' '^## WRONG AT SOURCE' '^## PROVENANCE' '^## FILL AT READY'; do
  grep -q "$H" "$BRIEF" || { echo "REFUSING: brief lacks section '$H'" >&2; exit 19; }
done
for w in 'RD-657' '37-38' 'C-124' 'C-20' 'C-158' 'SCOPED' 'RELAYED' 'NOT RE-TESTED' 'Prior-work check' 'Never merge' "$ZIP220_PLAN_SHA" "$ZIP220_LIST_SHA"; do
  grep -qiF "$w" "$BRIEF" || { echo "REFUSING: brief must carry '$w'" >&2; exit 19; }
done

# 24 — the prompt must DESCRIBE the server entry point, never carry its literal path (RD-591 c.37901).
if printf '%s\n' "$PROMPT" | grep -qi 'backend/server\.js'; then
  echo "REFUSING: the prompt contains the server entry point's literal path (RD-591 c.37901). Describe it; do not name it." >&2; exit 24; fi

# 46 — the customer-test identity appears only as HELD / never-use in both texts.
case "$PROMPT" in *"never run session-tools/s83l/ct-az.sh"*) ;; *) echo "REFUSING: prompt must forbid ct-az.sh explicitly" >&2; exit 46 ;; esac
grep -qF 'any use of `session-tools/s83l/ct-az.sh` or' "$BRIEF" || { echo "REFUSING: brief §9 must hold ct-az.sh / the customer-test identity" >&2; exit 46; }

# 53 / 71 — standing rules present in the brief; the NOT TESTED line verbatim in both.
for w in 'DEADLINE' 'HEARTBEAT' '2 minutes' '5 minutes' 'finally' 'qa-pkg221-' 'node --check' 'VOID' 'EXCLUSIVE' 'POSITIVE CONTROL FIRST'; do
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
command -v gitleaks >/dev/null 2>&1 || docker image inspect zricethezav/gitleaks:latest >/dev/null 2>&1 || echo "NOTE: no gitleaks binary or image found — Q9 needs one" >&2

# 32 — the coordinator stamps the self-check. LAST, so --check shows every other guard first.
if grep -qF "$PH_STAMP" "$BRIEF" || ! grep -q '^SELF-CHECK: re-read end-to-end for contradictions | ' "$BRIEF" || ! grep -q '^Self-check note: ' "$BRIEF"; then
  echo "guards pass (9 47a 6 8 18 22 35 41 42 45 47 31 40 10 17 11 12 13 14 15 20 19 24 46 53 71 38); self-check NOT stamped." >&2
  echo "REFUSING: the brief's SELF-CHECK line or Self-check note is unstamped — the coordinator re-reads end-to-end and stamps both before launch" >&2; exit 32
fi

if [ "$CHECK" = "1" ]; then
  echo "all guards pass:"
  echo "  origin $BRANCH == $HEAD7 and $BRANCH_220 == c5da4d4 at $PIN_TS (18); main ${M_ORIGIN:0:7}"
  echo "  chain: c5da4d4 <- d14a975 <- package $PKGC7 <= head $HEAD7, docs-only between (6 8)"
  echo "  deltas: fix = 3 files, package = policy only (22); counts c5da4d4 $BASE_COUNTS, head $EXP_COUNTS (35)"
  echo "  template: webtest ping->standard only, image unchanged; policy: +\"$VERSION\" = same image (41 42)"
  echo "  health formula $HEALTH_BUILD (45); 2.2.1 trio complete, zipped fix, only mainTemplate differs from 2.2.0, 2.2.0 zips unchanged (47)"
  echo "  evidence + tools (31); route $ROUTE_NAME (40); report absent (17); ct-az held (46); seats $NEG_SEATS named (38)"
  echo "  AZURE_CONFIG_DIR=$AZURE_CONFIG_DIR  GH_CONFIG_DIR=$GH_CONFIG_DIR  CLAUDE_CONFIG_DIR=$CLAUDE_CONFIG_DIR"
  exit 0
fi

PROMPT="$PROMPT

VERIFIED BY THE LAUNCHER AT $PIN_TS (git ls-remote origin, read-only): refs/heads/$BRANCH = $HEAD_SHA; refs/heads/$BRANCH_220 = $BASE_220; refs/heads/main = ${M_ORIGIN:-unreadable}. The package commit named by the builder's manifest is $PKGC_SHA. These are the start-of-gate pins; take your own three readings anyway."

cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions "$PROMPT"
