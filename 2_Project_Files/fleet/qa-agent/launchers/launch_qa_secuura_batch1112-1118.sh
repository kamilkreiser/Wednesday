#!/bin/bash
# launch_qa_secuura_batch1112-1118.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SEVEN file-disjoint TEST-ONLY
# Secuura/Blockchain PRs (Seat B 12th; fifteen local-model patches grouped by FILE into seven PRs across FIVE lanes)
#   #1112 PR A KS-1203 @ 3a28d2a3c  api-gateway VITEST test: NESTEDTYPE-1+WSTRIM-1 (+8, one file, two cells) — TIER 2, pushed FIRST
#   #1113 PR B KS-1283 @ abf8321a9  api-gateway VITEST test: PROVADMIN-1 (+4, the requireOrgProvisioner guard) — TIER 1 (Wednesday's ruling)
#   #1114 PR C KS-1244 + KS-1198 @ 762a70117  api-gateway VITEST test: JOINEDKEY-1 + SKMETA-1 (+24, auth.test.ts) — TIER 1 (authenticateToken)
#   #1115 PR D KS-1275 @ b008489e4  originate JEST test: ORDERTHROUGHSPEC-1 (+6) — TIER 2
#   #1116 PR E KS-1284 + KS-1175 @ 9a485cfe7  anchoring VITEST tests: the anchoring six (+131 over FIVE files, three NEW) — TIER 2
#   #1117 PR G KS-1137 @ b3f94f14a  BASH suite: F2-ESTATEIMAGE-1 (+19, container_trivy_image_filter.test.sh) — TIER 2
#   #1118 PR F KS-1006 + KS-1236 @ f132c9214  the AUTH service VITEST test: WRONGCODE-1 + SUBMITLEVEL-1 (+24) — TIER 1 (the auth service), pushed LAST
# ALL SEVEN are TEST-ONLY (files API + local diff --raw: 11 paths, every one under __tests__/, +216/-0, 8 M + 3 A — generator-asserted by numstat).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the seven heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the seven head trees (= the trees over develop: each head's parent IS develop, a
# fast-forward) and the all-seven tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch.out) AND by pure tree
# hashing in the generator; every BOTH-list token asserted present in the READY capture and the prompt at generation.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets13.py wants exactly ONE equality target PER PR FILE (1/1/1/1/5/1/1) and parses the list non-greedily to the
# FIRST `;` (targets13.py:28) — the #1116 addendum line carries FIVE targets COMMA-separated (exit 25); merge13.py:58-:64 asserts each squash body's
# key set == the PR's OWN Refs set (two keys on #1114, #1116, #1118).
# Batched under Kam 2026-09-18 standing rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All ten tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + seven refs/pull/N/head + seven branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 362e51fe0 (tree 2e981e777, the #1106-#1111 batch landed) — NO develop move under these heads,
# so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 362e51fe0, ahead 1, BEHIND 0, files
# 1/1/1/1/5/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint (11 paths: 8 modified
# tests, 3 NEW tests; overlap 0 over 21 pairs). ALL SEVEN over 362e51fe0 = 6aa9873f974019a92574d6db52e6356734573c8c, identical in every order tried.
#
# The develop pin is judged by CONTENT — FIFTY-TWO paths by blob at the CURRENT develop: the 11 PR paths (8 at develop blobs, 3 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 10 tamper files (enforcement.ts, platform.ts, middleware/auth.ts, originate.openapi.ts,
# anchorReadback.ts, cardanoMetadatum.ts, anchoring index.ts, transaction.ts, users.ts, 04-container-trivy.sh), and what the gate runs or reads:
# the three cover-cell files (ks1215, ks480-connector-auth, ks1284-cardano-metadatum), threadTokenMint.test.ts (the pre-existing red), db.retry
# (LOAD-1), auth.integration.test.ts + the auth / originate index.ts (the :4003 / :4000 listens), the five packages' package.json / config /
# tsconfig / lock, run-shell-suites.sh, preflight.sh, the pre-push hook, the Dev package.json + lock, eslint.config.mjs, the 3 sibling trivy suites.
# GUARDED: api-gateway src/ + config, originate src/ + config, anchoring src/ + config, auth src/ + config, packages/shared src/ + config,
# scripts/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1112to1118/mail_batch1112_ready.md, the seat's SEVEN READY mails (19:53:20Z … 20:29:59Z) + the 19:34:31Z STATUS
# mail + the 18:45:57Z plan-confirmation mail, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2).
# exit 10: the compare per PR (merge_base 362e51fe0, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all seven heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1106-#1111), the ANCHORING REPORT (#1105), the EARLIER REPORT
#          (#1102-#1104) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (FIVE for #1116, comma-separated), the
#          `## MERGE ADDENDUM` heading targets13.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b12-*) and writing in the seat 2026-09-21_seatB-12th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4005 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the seven head trees, the
#          all-seven tree, the eleven head blobs, the 22 plant sha256s the READYs carry, the 27 tamper ids, the suite counts, the three covers'
#          words F1 / F2 / F3 and INSTR-1, the :5432 and :4005 words, the archived and foreign keys, the GO subject), and the prompt must ask the
#          gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-seven tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the seven, which ticket(s) the PR is (PR #1112 is KS-1203. … PR #1118 is KS-1006 + KS-1236.).
# exit 33: the prompt must carry Wednesday SEVENTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1112_CUR_DEV (test override, --check only): stands in for origin develop. QAB1112_HEAD_1118 (test override): stands in for #1118 pinned head.
# QAB1112_BRIEF / QAB1112_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1112_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1112to1118/gen_launcher_1112.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1106.py.
#
# Usage: launch_qa_secuura_batch1112-1118.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1112_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118/mail_batch1112_ready.md}"
PROMPT_FILE="${QAB1112_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1112-1118.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1112|KS-1203|refs/heads/feature/ks-1203-a-connector-restricted-by-alloweddocumenttypes-can-still-nestedtype-wstrim-1|3a28d2a3c4d030cb73b7775bb19c5844ce190e56|1"
  "1113|KS-1283|refs/heads/feature/ks-1283-platformts-a-widened-super_roles-would-admit-a-tenant-admin-provadmin-1|abf8321a9ca426a1d623a54a41453824dce34def|1"
  "1114|KS-1244|refs/heads/feature/ks-1244-a-duplicated-x-api-key-header-defeats-key-authentication-via-joinedkey-skmeta-1|762a70117c6cf40545f8a4ac5f24708e7fcd91fe|1"
  "1115|KS-1275|refs/heads/feature/ks-1275-published-post-lifecycle-events-description-still-enumerates-orderthroughspec-1|b008489e4fbc72bb8b68cb3bb925557978399780|1"
  "1116|KS-1284|refs/heads/feature/ks-1284-cardanotransactionts-add_json_metadatum_with_schema-throws-anchoring-pins-1|9a485cfe77406f47103ed6ab65c14ec01144cb68|5"
  "1117|KS-1137|refs/heads/feature/ks-1137-trivy-estate-image-1|b3f94f14a0cf3e0236284481b85781417fd233f3|1"
  "1118|KS-1006|refs/heads/feature/ks-1006-post-apiusersmemfadisable-skips-code-verification-when-wrongcode-submitlevel-1|${QAB1112_HEAD_1118:-f132c92147b5005c36e405d0116faa541d978a67}|1"
)
DEVELOP_SHA='362e51fe0db7e73d5557924902763fe3f10fd8c7'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='362e51fe0db7e73d5557924902763fe3f10fd8c7'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='6aa9873f974019a92574d6db52e6356734573c8c'     # all seven over the pin 362e51fe0 (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
ANCHOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1112to1118/mail_batch1112_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The seven heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
HEADS_NOTE=""
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h _f <<< "$_pr"
  _lsr="$(git -C "$REPO" ls-remote origin "$_br" "refs/pull/$_n/head")"
  if ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]${_br}\$" || ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]refs/pull/${_n}/head\$"; then
    echo "REFUSING: #$_n $_t — $_h is not at $_br AND refs/pull/$_n/head on origin — that head moved; a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_lsr" >&2
    exit 6
  fi
  HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"
done

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 362e51fe0, ahead 1, behind 0 (no develop
# move), files 1/1/1/1/5/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  PRS_FLAT="${PRS[*]}" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
for pr in os.environ["PRS_FLAT"].split():
    n, tk, br, h, nf = pr.split("|")
    r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + h, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
    c = json.load(r)
    print("%s %s ahead=%d behind=%d files=%d" % (n, c["merge_base_commit"]["sha"], c["ahead_by"], c["behind_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compares develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="1112 $MERGE_BASE ahead=1 behind=0 files=1
1113 $MERGE_BASE ahead=1 behind=0 files=1
1114 $MERGE_BASE ahead=1 behind=0 files=1
1115 $MERGE_BASE ahead=1 behind=0 files=1
1116 $MERGE_BASE ahead=1 behind=0 files=5
1117 $MERGE_BASE ahead=1 behind=0 files=1
1118 $MERGE_BASE ahead=1 behind=0 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1112_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" ALL_OVER_DEV="$ALL_OVER_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]; all_over_dev = os.environ["ALL_OVER_DEV"]
D = "Blockchain/Dev/"
A = D + "services/api-gateway/"
O = D + "services/originate/"
N = D + "services/anchoring/"
U = D + "services/auth/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the three NEW tests)
JUDGED = {
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks501-enforcement-non-string-doctype.test.ts":              ({"e05c6bd21f64ad766083c72d0fc070ebeb478b7f": DV}, {"d68c6b2be95bf7c72b31903c27a0f26bbeee0332": "#1112 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts":                        ({"38787a194855ddb6931c81611c096cab8ec49c0d": DV}, {"92966f9c1f6291e8190b139d117ce39148fc6752": "#1113 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts":                                              ({"72348995a66ea324ffe78dc64136f46e64985aad": DV}, {"6d837e0aeeb8fdc7434033ae5d91fd018cfc5b66": "#1114 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts":           ({"22485a7ab3c5022912bf5216e9207875bc530aa4": DV}, {"27366baf325148d402822609f8ebe4d3c822724d": "#1115 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts":                              ({"05793d9254002f951e46d882510ec39e3d38dd37": DV}, {"d3d29533c9eeb962a6c1f7b3d4603b0a43658fd8": "#1116 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts":                             ({"ABSENT": DV}, {"57de9c9e24787dc33e3ec1006eae3f6640848b3f": "#1116 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts":                           ({"c3f430d783ba0d8594d962ceef13ad27325f402b": DV}, {"a6765883d409756eed8f7e73cca1dd05dd121d81": "#1116 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1284-attach-point.test.ts":                                 ({"ABSENT": DV}, {"d42259343d79141948ff3e879f8a7b34187dcb95": "#1116 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1284-chain-read-order.test.ts":                             ({"ABSENT": DV}, {"f461e832c5662bbe5258347654b0aa949008a1d3": "#1116 own"}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh":                                       ({"dec2db8dee6326369ebc16cacb1f8d58287a7562": DV}, {"35bbb4519950f77188ad30f3f1d46683ac63ddf5": "#1117 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts": ({"703c80dca84cde113b585788317f56cb5184f3d3": DV}, {"bfa8b1d3fc3611ad04266d9e520848958f2a4b55": "#1118 own"}),
  "Blockchain/Dev/services/api-gateway/src/services/enforcement.ts":                                             ({"be466fbf444178bbb41293fb1d811957e55e1d2d": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/platform.ts":                                                  ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts":                                                  ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  "Blockchain/Dev/services/originate/src/originate.openapi.ts":                                                  ({"2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/anchorReadback.ts":                                                     ({"f49ffb6afaafabefe4dfbe8d897623bb2e5b3fc7": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts":                                           ({"aaaec6c63655340bb864dc3aaa395a5707c9a6fb": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/index.ts":                                                              ({"b6386f402a4bc1572574c14e4925a96fd7811a39": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/cardano/transaction.ts":                                                ({"e047630ea0048b7d9e5d29793558a59eb5e437e4": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/users.ts":                                                            ({"3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d": DV}, {}),
  "Blockchain/Testing/jobs/04-container-trivy.sh":                                                               ({"88444463f9d42a3ee4ad8f8b5ca24123ae678fb6": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"50298953359ead9f947ac9f20f455a529dd2543a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks480-connector-auth.test.ts":                              ({"16e88d9b7e00d816e6a93bfb4359e6bdc43fcb43": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1284-cardano-metadatum.test.ts":                            ({"33cf6608e6a472293b7116a81a304dad446071a1": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/threadTokenMint.test.ts":                                     ({"b88b3a43ec5dcb8651b91d5df90e9dec42a1795f": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/db.retry.test.ts":                                          ({"5933da41ed3dcf37f415000c4da4a717ea8d7eba": DV}, {}),
  "Blockchain/Dev/services/auth/src/__tests__/auth.integration.test.ts":                                         ({"aa4b88f203d8f652d11c6f0ed9994191c8ffd5e7": DV}, {}),
  "Blockchain/Dev/services/auth/src/index.ts":                                                                   ({"edabbf87182311241662b20ac71d7244e923b5a3": DV}, {}),
  "Blockchain/Dev/services/originate/src/index.ts":                                                              ({"44d4e4f341f5d314f5b95405b209a9450cde1d3e": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                                            ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                                        ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.setup.ts":                                                         ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                                           ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package-lock.json":                                                       ({"5ec55d86d83f93e70dc03676293331fd3bc250e5": DV}, {}),
  "Blockchain/Dev/services/originate/package.json":                                                              ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  "Blockchain/Dev/services/originate/jest.config.js":                                                            ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  "Blockchain/Dev/services/originate/tsconfig.json":                                                             ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  "Blockchain/Dev/services/originate/package-lock.json":                                                         ({"4c1800aee48392e6ca2efa80526b1b2627cec34d": DV}, {}),
  "Blockchain/Dev/services/anchoring/package.json":                                                              ({"a7eed73550b40aa2d968872817fa22e933373831": DV}, {}),
  "Blockchain/Dev/services/anchoring/vitest.config.ts":                                                          ({"2e1d21f130f8aa80a1c71987f920181dafaf6b90": DV}, {}),
  "Blockchain/Dev/services/anchoring/tsconfig.json":                                                             ({"f593300cac7c9c3073f15a1287323cf5b9dd478d": DV}, {}),
  "Blockchain/Dev/services/anchoring/package-lock.json":                                                         ({"7ef3f65a35b48bec2591df4b2859bab9aa237334": DV}, {}),
  "Blockchain/Dev/services/auth/package.json":                                                                   ({"814e88419470b811f26f1593984071bb317608d8": DV}, {}),
  "Blockchain/Dev/services/auth/vitest.config.ts":                                                               ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": DV}, {}),
  "Blockchain/Dev/services/auth/tsconfig.json":                                                                  ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": DV}, {}),
  "Blockchain/Dev/services/auth/package-lock.json":                                                              ({"2d91a356aa8426304dc291e0090dbd6893d53c00": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                 ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                             ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                  ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                               ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  ".githooks/pre-push":                                                                                          ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/package.json":                                                                                 ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                                            ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                                            ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/aggregate_report_trivy_artefact.test.sh":                                    ({"fb667d93f089bb586257c970b72bb50b3f5872a4": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh":                                ({"819ca90240aae6310758d0c5ea2733c3eec3f1b3": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh":                                                   ({"4653bc8a1d4abd080db26ce03c33434beac16896": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except urllib.error.HTTPError as e:
        if e.code != 404:
            print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": HTTP " + str(e.code)); sys.exit(0)
        blob = "ABSENT"
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — that PR has landed; this gateset is stale for it"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all seven together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json", A + "package-lock.json",
           O + "src/", O + "package.json", O + "jest.config.js", O + "tsconfig.json", O + "package-lock.json",
           N + "src/", N + "package.json", N + "vitest.config.ts", N + "tsconfig.json", N + "package-lock.json",
           U + "src/", U + "package.json", U + "vitest.config.ts", U + "tsconfig.json", U + "package-lock.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           D + "scripts/", ".githooks/", "Blockchain/Testing/jobs/",
           D + "package.json", D + "package-lock.json", D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto EACH of the seven heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-seven tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1112.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1112 KS-1203: TIER 2' "$PROMPT_FILE" && grep -qF '#1113 KS-1283: TIER 1' "$PROMPT_FILE" && grep -qF '#1114 KS-1244: TIER 1' "$PROMPT_FILE" && grep -qF '#1115 KS-1275: TIER 2' "$PROMPT_FILE" && grep -qF '#1116 KS-1284: TIER 2' "$PROMPT_FILE" && grep -qF '#1117 KS-1137: TIER 2' "$PROMPT_FILE" && grep -qF '#1118 KS-1006: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h _f <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "$_h" "$BRIEF" \
    || { echo "REFUSING: the READY capture or the prompt does not name #$_n's head $_h — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA -> Wednesday] BATCH GATE #1112-#1118 (seven PRs; tier 1 = #1113, #1114, #1118)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SEVEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$ANCHOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the ANCHORING REPORT $ANCHOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1116 FIVE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1116 FIVE, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b12-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-12th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b12-*) and writing in the seat 2026-09-21_seatB-12th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4005 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          6aa9873f974019a92574d6db52e6356734573c8c \
          2e981e7779dc \
          362e51fe0db7e73d5557924902763fe3f10fd8c7 \
          9c8c7520b2cd \
          7b8734234ed58c55bf1ff427d6cd03fdfdc36e20 \
          5c8e116814348c78207055424af12a43b93ab564 \
          c6a6a7380f1d4554de724f9a38257e0498e3a261 \
          fea63ca447a2d2d54aada84575236780b03fa948 \
          ea9fc7d7cefc2b88d7fec7b694fc1204b07f1777 \
          8de2a19066c964a23b052e0db6395ea3f2bb74ec \
          7e75405911ec06a01839d4bcf86ccd747b4a3802 \
          d68c6b2be95bf7c72b31903c27a0f26bbeee0332 \
          92966f9c1f6291e8190b139d117ce39148fc6752 \
          6d837e0aeeb8fdc7434033ae5d91fd018cfc5b66 \
          27366baf325148d402822609f8ebe4d3c822724d \
          d3d29533c9eeb962a6c1f7b3d4603b0a43658fd8 \
          a6765883d409756eed8f7e73cca1dd05dd121d81 \
          57de9c9e24787dc33e3ec1006eae3f6640848b3f \
          f461e832c5662bbe5258347654b0aa949008a1d3 \
          d42259343d79141948ff3e879f8a7b34187dcb95 \
          35bbb4519950f77188ad30f3f1d46683ac63ddf5 \
          bfa8b1d3fc3611ad04266d9e520848958f2a4b55 \
          82085a23936d \
          63e6537d84de \
          0acfe0d608fd \
          736c76413f61 \
          b3757be6387c \
          df7bde2a7a39 \
          f5c97a3d2437 \
          e26f40eded94 \
          b092b49304f4 \
          eb792dee994c \
          794830fdff2b \
          a31c8d005698 \
          c0920d5a45ac \
          b23a4749fe9a \
          542f8fad18b5 \
          c525238074c4 \
          2186541ed00e \
          b59cb32248c7 \
          ad1a74f801f3 \
          863ad55f9e69 \
          fac3264f37b2 \
          13f6546e693a \
          NESTEDTYPEHONOURED \
          WHITESPACETYPETRIMMED \
          WIDENROLES \
          ADMINBRANCH \
          SPLITFIRST \
          FALLTHROUGH \
          METADROPPED \
          METAWIDENED \
          REQREGREVERSED \
          RESREGREVERSED \
          DOCIDFROMROWONLY \
          CERTIDFROMROWONLY \
          CODECJOINDROPPED \
          NETWORKINVERTED \
          MAINNETPREFIXED \
          EMPTYIDENTITYKEPT \
          GETIDVIEWDROPPED \
          GETIDVIEWWRONGSOURCE \
          CHAINREADNODECODE \
          HASHCOMPARERAW \
          ATTACHPOINTRAW \
          TRAILINGDIGITONLY \
          KS867REVERTED \
          VERIFYINVERTED \
          PRESENCEINVERTED \
          EQUALADMITTED \
          GUARDNEVERFIRES \
          683 \
          685 \
          684 \
          688 \
          807 \
          808 \
          328/329 \
          779 \
          782 \
          907/907 \
          '5 ok / 0 FAIL' \
          '4 ok / 0 FAIL' \
          '18 ok' \
          '41 passed, 0 failed (of 41)' \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          INSTR-1 \
          TS2339 \
          TS2322 \
          req.user \
          threadTokenMint \
          'per-seed policyId' \
          ks1215 \
          KS-1232 \
          'bools not allowed in metadata' \
          TRIVY_JOB_SH \
          shellcheck \
          jq \
          /bin/bash \
          'bash -n' \
          'Deviation from verbatim: NONE' \
          'linear[bot]' \
          attachmentsForURL \
          contributes \
          'GO: merge #1112-#1118 batch' \
          ks-878867 \
          KS-480 \
          KS-721 \
          :5432 \
          '"port":5432,' \
          anchoring:4005 \
          localhost:6000 \
          203.0.113.7:443 \
          unattributed \
          x-api-key \
          connectorMeta \
          SUPER_ROLES \
          requireOrgProvisioner \
          verifyTOTP \
          LIFECYCLE_EVENT_ACTIONS \
          anchorIdentityView \
          buildAnchorTransaction \
          handleAnchorVerifyByHash \
          dev-auth2 \
          'Refs KS-1244' \
          'Refs KS-1198' \
          'Refs KS-1284' \
          'Refs KS-1175' \
          'Refs KS-1006' \
          'Refs KS-1236' \
          F1 \
          F2 \
          F3 \
          S1 \
          S2 \
          S3 \
          S4 \
          S5 \
          'CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction' \
          KS-501 \
          KS-978 \
          KS-522 \
          KS-726 \
          KS-535 \
          KS-867 \
          KS-878 \
          KS-914 \
          KS-1238 \
          KS-1282 \
          KS-1062 \
          KS-1194 \
          KS-1136 \
          KS-753 \
          KS-1205 \
          KS-1171 \
          KS-1172 \
          KS-1133 \
          KS-794 \
          KS-1215 \
          KS-1273 \
          KS-1274 \
          KS-932 \
          KS-741 \
          KS-1260 \
          KS-1209 \
          KS-953 \
          '#995' \
          cardano-serialization-lib \
          '<= 92 chars' \
          'Nothing failed' \
          quarantine \
          'both orders' \
          'pairwise overlaps NONE'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-seven tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1112 is KS-1203.' "$PROMPT_FILE" && grep -F '#1112' "$BRIEF" | grep -qF 'KS-1203' && grep -qF 'PR #1113 is KS-1283.' "$PROMPT_FILE" && grep -F '#1113' "$BRIEF" | grep -qF 'KS-1283' && grep -qF 'PR #1114 is KS-1244 + KS-1198.' "$PROMPT_FILE" && grep -F '#1114' "$BRIEF" | grep -qF 'KS-1244' && grep -qF 'PR #1115 is KS-1275.' "$PROMPT_FILE" && grep -F '#1115' "$BRIEF" | grep -qF 'KS-1275' && grep -qF 'PR #1116 is KS-1284 + KS-1175.' "$PROMPT_FILE" && grep -F '#1116' "$BRIEF" | grep -qF 'KS-1284' && grep -qF 'PR #1117 is KS-1137.' "$PROMPT_FILE" && grep -F '#1117' "$BRIEF" | grep -qF 'KS-1137' && grep -qF 'PR #1118 is KS-1006 + KS-1236.' "$PROMPT_FILE" && grep -F '#1118' "$BRIEF" | grep -qF 'KS-1006' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1112 is KS-1203. … PR #1118 is KS-1006 + KS-1236.)" >&2; exit 32; }
grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes on ALL SEVEN' "$PROMPT_FILE" && grep -qF -- '0 files outside `__tests__/`' "$PROMPT_FILE" && grep -qF -- 'files API union 11' "$PROMPT_FILE" && grep -qF -- 'DISJOINTNESS AND THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'at least forward and exact reverse' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'fast-forward = its head tree' "$PROMPT_FILE" && grep -qF -- 'auth develop baseline 779' "$PROMPT_FILE" && grep -qF -- 'THE THREE SKIPPED LEGS' "$PROMPT_FILE" && grep -qF -- 'legs 3, 4, 8' "$PROMPT_FILE" && grep -qF -- 'skip_stack' "$PROMPT_FILE" && grep -qF -- 'would have EXERCISED these changes' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST PER PR UNDER THE COVER RULE' "$PROMPT_FILE" && grep -qF -- 'DEVELOP COVER measured FIRST' "$PROMPT_FILE" && grep -qF -- 'reds == declared ∪ measured cover' "$PROMPT_FILE" && grep -qF -- 'ONE named sibling allowance' "$PROMPT_FILE" && grep -qF -- 'LEAD F1' "$PROMPT_FILE" && grep -qF -- 'LEAD F2' "$PROMPT_FILE" && grep -qF -- 'LEAD F3' "$PROMPT_FILE" && grep -qF -- 'GRADE F1' "$PROMPT_FILE" && grep -qF -- 'GRADE F2' "$PROMPT_FILE" && grep -qF -- 'GRADE F3' "$PROMPT_FILE" && grep -qF -- 'NEW = N - 1' "$PROMPT_FILE" && grep -qF -- '27/27 by exact-line count' "$PROMPT_FILE" && grep -qF -- 'THE GUARD AND ITS MOUNT' "$PROMPT_FILE" && grep -qF -- 'PROVMOUNTUNPINNED' "$PROMPT_FILE" && grep -qF -- 'SUPERADMINROUTESWIDEN' "$PROMPT_FILE" && grep -qF -- 'fake req/res' "$PROMPT_FILE" && grep -qF -- ':489 -> :91 -> :97' "$PROMPT_FILE" && grep -qF -- 'THE API-KEY PATH' "$PROMPT_FILE" && grep -qF -- 'OPTIONALMOUNTJOINEDKEY' "$PROMPT_FILE" && grep -qF -- 'INSTR-1 reproduced' "$PROMPT_FILE" && grep -qF -- 'Request augmentation' "$PROMPT_FILE" && grep -qF -- 'in either order' "$PROMPT_FILE" && grep -qF -- 'THE TWO ROUTES' "$PROMPT_FILE" && grep -qF -- 'FALSYMFASECRETDOOR' "$PROMPT_FILE" && grep -qF -- 'STALEAPPROVALPATH' "$PROMPT_FILE" && grep -qF -- 'before any store read' "$PROMPT_FILE" && grep -qF -- ':4003 discipline' "$PROMPT_FILE" && grep -qF -- 'THE RATIO, THE COVERS, THE THREE NEW FILES' "$PROMPT_FILE" && grep -qF -- 'a second red is a finding' "$PROMPT_FILE" && grep -qF -- 'GETIDROUTEBOOTLESS' "$PROMPT_FILE" && grep -qF -- 'source guard reds on text, not behaviour' "$PROMPT_FILE" && grep -qF -- 'prove CSL resolved in' "$PROMPT_FILE" && grep -qF -- 'offset-4 apply after NESTEDTYPE' "$PROMPT_FILE" && grep -qF -- 'EARLIER rows it CLOSES' "$PROMPT_FILE" && grep -qF -- 'reads the REGISTERED schemas' "$PROMPT_FILE" && grep -qF -- 'DESCRIPTIONVERBLIST' "$PROMPT_FILE" && grep -qF -- 'jest `fullName`' "$PROMPT_FILE" && grep -qF -- 'TRIVY_JOB_SH copies' "$PROMPT_FILE" && grep -qF -- 'NONLATESTTAGEXCLUDED' "$PROMPT_FILE" && grep -qF -- 'jq absent rc 2' "$PROMPT_FILE" && grep -qF -- 'THE db.retry INTERMITTENT AND LOAD-2' "$PROMPT_FILE" && grep -qF -- 're-run that suite SERIAL' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- "deterministic, develop's own" "$PROMPT_FILE" && grep -qF -- 'THE CONNECTION CENSUS' "$PROMPT_FILE" && grep -qF -- 'CENSUS RULE v2' "$PROMPT_FILE" && grep -qF -- 'the baseline leg REPORTS only' "$PROMPT_FILE" && grep -qF -- 'a real Postgres listens on 127.0.0.1:5432' "$PROMPT_FILE" && grep -qF -- 'identical A/B totals' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'KS-1112' "$PROMPT_FILE" && grep -qF -- 'KS-1118' "$PROMPT_FILE" && grep -qF -- 'Completes KS-1244' "$PROMPT_FILE" && grep -qF -- 'recommend nothing' "$PROMPT_FILE" && grep -qF -- 'the seat elided' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'proposed cell' "$PROMPT_FILE" && grep -qF -- "local model's next round" "$PROMPT_FILE" && grep -qF -- 'BY DESIGN' "$PROMPT_FILE" && grep -qF -- 'ONE MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- '#1116 FIVE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- 'targets13.py:28' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'targets13.py reads' "$PROMPT_FILE" && grep -qF -- 'MG-3 KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'merge13.py:58' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S SLIPS S1 / S2 / S3 / S4 / S5" "$PROMPT_FILE" && grep -qF -- 'none reached a pushed byte' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday seventeen by-name items (tier/round/product bytes; the trees and disjointness; the three skipped legs; red-first under the cover rule with F1 / F2 / F3 graded; #1113 the guard and its mount; #1114 the api-key path + INSTR-1; #1118 the two routes; #1116 the ratio, covers and three new files; #1112; #1115 jest; #1117 bash; db.retry + LOAD-2; census v2 + :4003/:4005; link hygiene incl. KS-1112..KS-1118; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3; the seat slips + the line-number discipline) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  seven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1113 T1, #1114 T1, #1118 T1, #1112 T2, #1115 T2, #1116 T2, #1117 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all seven heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1106-#1111 PRIOR REPORT, the #1105 ANCHORING REPORT, the #1102-#1104 EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1116 FIVE, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b12-*) and the seat 2026-09-21_seatB-12th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4005 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (180 tokens: develop + tree, seven head trees, the all-seven tree, eleven head blobs, 22 plant shas, 27 tamper ids, counts, F1/F2/F3/INSTR-1, :5432/:4005, archived + foreign keys, the GO subject); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the all-seven tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the seven PRs is"
  echo "  prompt carries Wednesday seventeen by-name items and the standard closing (100 keywords)"
  [ -n "${QAB1112_CUR_DEV:-}" ] && echo "  (develop read from the QAB1112_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1112_BRIEF:-}${QAB1112_PROMPT:-}${QAB1112_HEAD_1118:-}${QAB1112_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
