#!/bin/bash
# launch_qa_secuura_batch1119-1128.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over TEN file-disjoint
# Secuura/Blockchain PRs (Seat B 13th; fourteen local-model patches grouped by FILE SET into ten PRs across SEVEN lanes)
#   #1119 PR B KS-753 @ e9e20196f  timestamping VITEST test: VERIFIEDPERSISTED-1 (+32, one file) — TIER 2, pushed FIRST
#   #1120 PR E KS-1232 @ 2a66cd17e  mcp-server VITEST tests: MCPINFORAWECHO-1 + HTTPSERVERINFOEMPTY-1 (+87, two NEW files) — TIER 2 (a NEW lane)
#   #1121 PR G KS-957 + KS-930 @ 939de1ba5  BASH suite: F4-TOOLINGTOKENS-1 (+74, one NEW suite) — TIER 2
#   #1122 PR F KS-1273 @ 9aa5442ae  bash_patch: the round's ONE PRODUCT HUNK on Blockchain/Testing/jobs/04-container-trivy.sh (-1/+2) + one NEW suite (+114) — TIER 2 (a CI job)
#   #1123 PR H KS-1275 @ c346999ad  originate JEST test: DESCRIPTIONVERBLIST-1 (+9) — TIER 2
#   #1124 PR A KS-880 @ bd907c553  security VITEST test: LIVETENANTDEFAULT-1 (+9) — TIER 1 (rowToApiKey, a tenant-isolation surface)
#   #1125 PR D KS-1223 @ c50c0a8d4  api-gateway + referral VITEST tests: WALLETFORWARD-1 + REFERRALFALLBACK-1 (+124, two NEW files, TWO lanes) — TIER 1
#   #1126 PR I KS-1283 @ b23ad259a  api-gateway VITEST test: PROVMOUNT-SUPERADMINROUTES-1 (+26) — TIER 1 (routes/platform.ts)
#   #1127 PR J KS-1244 @ f0cc0aadc  api-gateway VITEST test: REFUSALMESSAGE-1 (+13) — TIER 1 (middleware/auth.ts)
#   #1128 PR C KS-1234 @ e35b5ddc2  api-gateway VITEST test: the KS-1234 trio (+18, one file, three READYs) — TIER 1 (the sanitizer mount), pushed LAST
# NINE are TEST-ONLY and #1122 carries EXACTLY ONE product path (files API + local diff --raw: 13 paths, 12 under __tests__/ + the job, +508/-1,
# 7 M + 6 A — generator-asserted by numstat; the job is mode 100755).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the ten heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the ten head trees (= the trees over develop: each head's parent IS develop, a fast-forward)
# and the all-ten tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch.out) AND by pure tree hashing in the
# generator; every BOTH-list token asserted present in the READY capture and the prompt at generation.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets14.py wants exactly ONE equality target PER PR FILE (1/2/1/2/1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` (targets14.py:28) — the #1120, #1122 and #1125 addendum lines carry TWO targets COMMA-separated (exit 25); merge14.py:54-:64
# asserts each squash body's key set == the PR's OWN Refs set (two keys on #1121 only).
# Batched under Kam 2026-09-18 standing rule. TEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All eleven tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + ten refs/pull/N/head + ten branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 7be81d5c9 (tree 6aa9873f974, the #1112-#1118 batch landed) — NO develop move under these
# heads, so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 7be81d5c9, ahead 1, BEHIND 0,
# files 1/2/1/2/1/1/2/1/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint (13 paths:
# 6 modified tests + the job, 6 NEW tests; overlap 0 over 45 pairs). ALL TEN over 7be81d5c9 = 23d60cace7c37bc329ccc425e58659e950089a4d, identical
# in every order tried.
#
# The develop pin is judged by CONTENT — SIXTY-TWO paths by blob at the CURRENT develop: the 13 PR paths (7 at develop blobs, 6 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 11 tamper files (security index.ts, timestamping index.ts, api-gateway index.ts,
# verification.ts, platform.ts, middleware/auth.ts, originate.openapi.ts, referrals.ts, info.ts, http-server.ts, check-shared-relink.sh), and
# what the gate runs or reads: the five bash siblings + manifest_quarantine, the ks480 cover-cell file, db.retry (LOAD-1), the ks1207 control file,
# the six services' package.json / config / tsconfig / lock, the originate + referral index.ts, packages/shared's, run-shell-suites.sh,
# preflight.sh, fix-libsodium-symlink.js, the pre-push hook, the Dev package.json + lock, eslint.config.mjs.
# GUARDED: every service's src/ + config (security, timestamping, api-gateway, referral, mcp-server, originate, anchoring, auth), packages/shared,
# scripts/, systemTest/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1119to1128/mail_batch1119_ready.md, the seat's TEN READY mails (01:01:31Z … 02:22:31Z) + the 00:58:10Z STATUS
# mail + the 00:13:13Z plan-confirmation mail + the 00:39:34Z PR C and 01:44:22Z PR D QUESTION mails, each captured verbatim by message id from
# wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2).
# exit 10: the compare per PR (merge_base 7be81d5c9, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all ten heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1112-#1118), the EARLIER REPORT (#1106-#1111), the OLDER REPORT
#          (#1102-#1104) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for #1120, #1122, #1125, comma-separated),
#          the `## MERGE ADDENDUM` heading targets14.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b13-*) and writing in the seat 2026-09-21_seatB-13th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4005 / :4006 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the ten head trees, the
#          all-ten tree, the thirteen head blobs, the 20 plant sha256s the READYs carry, the 20 tamper ids, the suite counts, the allowance's
#          words, LINT-1 / LINT-2 / INSTR-1, the leg-14 words, the :5432 and :4005 words, the archived and foreign keys, the GO subject), and
#          the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-ten tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the ten, which ticket(s) the PR is (PR #1119 is KS-753. … PR #1128 is KS-1234.).
# exit 33: the prompt must carry Wednesday EIGHTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1119_CUR_DEV (test override, --check only): stands in for origin develop. QAB1119_HEAD_1128 (test override): stands in for #1128 pinned head.
# QAB1119_BRIEF / QAB1119_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1119_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1119to1128/gen_launcher_1119.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1112.py.
#
# Usage: launch_qa_secuura_batch1119-1128.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1119_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128/mail_batch1119_ready.md}"
PROMPT_FILE="${QAB1119_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1119-1128.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1119|KS-753|refs/heads/feature/ks-753-timestamping-fail-closed-a-mock-tsa-fallback-must-not-report-verifiedpersisted-1|e9e20196f2a91ca57ec6bc6d24087843e2611a08|1"
  "1120|KS-1232|refs/heads/feature/ks-1232-get-apiconnectorinfo-tells-a-connector-all-types-permitted-mcp-info-doctypes-1|2a66cd17ec3bd5d91e2fc72c7e3f9102ce1eb839|2"
  "1121|KS-957|refs/heads/feature/ks-957-round-2-gate-residue-the-guard-and-its-suite-write-f4-toolingtokens-1|939de1ba519629cacd22031cbc42dbbb765b4040|1"
  "1122|KS-1273|refs/heads/feature/ks-1273-job-04-a-trivy_exit_code-or-trivyyaml-exit-code-in-the-exitcodeenv-1|9aa5442aeef4d07a3d39e3c3e73e65ef9a42a350|2"
  "1123|KS-1275|refs/heads/feature/ks-1275-published-post-lifecycle-events-description-still-enumerates-descriptionverblist-1|c346999ad3956c02e56fca61f9ad30396ceee2ff|1"
  "1124|KS-880|refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-livetenantdefault-1|bd907c5538286ee9333e2182d7b388c1007b7163|1"
  "1125|KS-1223|refs/heads/feature/ks-1223-a-client-x-wallet-address-is-forwarded-past-the-gateway-walletforward-referralfallback-1|c50c0a8d402cb6fc585b889c528802fba74c0e40|2"
  "1126|KS-1283|refs/heads/feature/ks-1283-platformts-a-widened-super_roles-would-admit-a-tenant-admin-provmount-superadminroutes-1|b23ad259a880ecb207b2ab3cf7e9a1b0b8368dad|1"
  "1127|KS-1244|refs/heads/feature/ks-1244-a-duplicated-x-api-key-header-defeats-key-authentication-via-refusalmessage-1|f0cc0aadc1a7856f76cbb69e925e23b94dd05a40|1"
  "1128|KS-1234|refs/heads/feature/ks-1234-post-apiv1documents-with-applicationjson-never-answers-and-alias-trio-1|${QAB1119_HEAD_1128:-e35b5ddc27dffca5ad1a7cea17b4433484d460ac}|1"
)
DEVELOP_SHA='7be81d5c9b109959b559e03652fb092c12de58e8'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='7be81d5c9b109959b559e03652fb092c12de58e8'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='23d60cace7c37bc329ccc425e58659e950089a4d'     # all ten over the pin 7be81d5c9 (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1119to1128/mail_batch1119_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The ten heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 7be81d5c9, ahead 1, behind 0 (no develop
# move), files 1/2/1/2/1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
WANT_COMPARE="1119 $MERGE_BASE ahead=1 behind=0 files=1
1120 $MERGE_BASE ahead=1 behind=0 files=2
1121 $MERGE_BASE ahead=1 behind=0 files=1
1122 $MERGE_BASE ahead=1 behind=0 files=2
1123 $MERGE_BASE ahead=1 behind=0 files=1
1124 $MERGE_BASE ahead=1 behind=0 files=1
1125 $MERGE_BASE ahead=1 behind=0 files=2
1126 $MERGE_BASE ahead=1 behind=0 files=1
1127 $MERGE_BASE ahead=1 behind=0 files=1
1128 $MERGE_BASE ahead=1 behind=0 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1119_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
S = D + "services/security/"
T = D + "services/timestamping/"
R = D + "services/referral/"
M = D + "services/mcp-server/"
SC = D + "scripts/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the six NEW tests)
JUDGED = {
  "Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts":                                     ({"6fdf0e80a46ce75c0e0f4c5540aea443779d944c": DV}, {"d732631dc0c2adfa1cbf3345074f7c39ba41c2f5": "#1119 own"}),
  "Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-connector-info-relay.test.ts":                                ({"ABSENT": DV}, {"e93bfae369f0ba940739c2a22ad25f9718ebda0a": "#1120 own"}),
  "Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-generate-package-doctypes-default.test.ts":                   ({"ABSENT": DV}, {"59bc927624043f1b5c3bccd03dc98cfec00ef400": "#1120 own"}),
  "Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh":                                         ({"ABSENT": DV}, {"fdb125ca3e6ae4516836c4c12ac88e5b34b2ca46": "#1121 own"}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh":                               ({"ABSENT": DV}, {"d119e64ba755e41e41d719d03ded24f79f297e04": "#1122 own"}),
  "Blockchain/Testing/jobs/04-container-trivy.sh":                                                                       ({"88444463f9d42a3ee4ad8f8b5ca24123ae678fb6": DV}, {"6dfc5731e56ede5e5a6f420cccd92874b7566a87": "#1122 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks978-published-contract-organizationuuid.test.ts":                   ({"27366baf325148d402822609f8ebe4d3c822724d": DV}, {"530fa32f8d886e70375e967304cf8881edf0e950": "#1123 own"}),
  "Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts":                                 ({"7a3fc7e16d0c93a2c70edbda853d6acf4faee259": DV}, {"f452db039b9dceb34bebd5046525de1e42b1879e": "#1124 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1223-wallet-forwarded-to-originate.test.ts":                      ({"ABSENT": DV}, {"82a92ea52407fba3cdeb755efab488854b3e5758": "#1125 own"}),
  "Blockchain/Dev/services/referral/src/__tests__/ks1223-wallet-header-fallback.test.ts":                                ({"ABSENT": DV}, {"daf9f5c1a6bb586065fcf44559073c25624dcf48": "#1125 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"50298953359ead9f947ac9f20f455a529dd2543a": DV}, {"94d0813cc861333a2dc60457d7fac8af9ec6fd17": "#1126 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/auth.test.ts":                                                      ({"6d837e0aeeb8fdc7434033ae5d91fd018cfc5b66": DV}, {"41f85fcb250ea6cd1b1e6bc33117dab2e7ee93ae": "#1127 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts":             ({"3f85887f7268a9a19fd61d73e6178bf7f6c892dc": DV}, {"e5cc79c5e29b0b657240feb2b8afc2b1d6073ba8": "#1128 own"}),
  "Blockchain/Dev/services/security/src/index.ts":                                                                       ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  "Blockchain/Dev/services/timestamping/src/index.ts":                                                                   ({"1d2f109f644d01915f720e1894741794c91f4338": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/index.ts":                                                                    ({"4e7fc1174d5453f9d6f71e3a69f166fc6a08db49": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/verification.ts":                                                      ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/platform.ts":                                                          ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/middleware/auth.ts":                                                          ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  "Blockchain/Dev/services/originate/src/originate.openapi.ts":                                                          ({"2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c": DV}, {}),
  "Blockchain/Dev/services/referral/src/routes/referrals.ts":                                                            ({"e97b7f0bc5506118043adb8537a15cc0879d9c5d": DV}, {}),
  "Blockchain/Dev/services/mcp-server/src/tools/info.ts":                                                                ({"c0f2268ca0aceeec2d89639bbead5bbc549fe859": DV}, {}),
  "Blockchain/Dev/services/mcp-server/src/http-server.ts":                                                               ({"fce4a31793b3765de96fc387a2f306da5db15744": DV}, {}),
  "Blockchain/Dev/scripts/check-shared-relink.sh":                                                                       ({"d41c79538503d6d31e2037b3f49e025ed38f2870": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh":                                               ({"35bbb4519950f77188ad30f3f1d46683ac63ddf5": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh":                                        ({"819ca90240aae6310758d0c5ea2733c3eec3f1b3": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh":                                                        ({"867ce728ab4aab4022befddc9cf5fa5e6df439ba": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/aggregate_report_trivy_artefact.test.sh":                                            ({"fb667d93f089bb586257c970b72bb50b3f5872a4": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh":                                                           ({"4653bc8a1d4abd080db26ce03c33434beac16896": DV}, {}),
  "systemTest/__tests__/manifest_quarantine.test.sh":                                                                    ({"2ae67f244ddd6e38b4a2b72255d101216cf30314": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts":                                ({"92966f9c1f6291e8190b139d117ce39148fc6752": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/db.retry.test.ts":                                                  ({"5933da41ed3dcf37f415000c4da4a717ea8d7eba": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts": ({"f56bd48b9e9213d5afb85df6c94a5eada3c5aa22": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.setup.ts":                                                                 ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                                                    ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                                                ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                                                   ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package-lock.json":                                                               ({"5ec55d86d83f93e70dc03676293331fd3bc250e5": DV}, {}),
  "Blockchain/Dev/services/originate/package.json":                                                                      ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  "Blockchain/Dev/services/originate/jest.config.js":                                                                    ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  "Blockchain/Dev/services/originate/tsconfig.json":                                                                     ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  "Blockchain/Dev/services/originate/package-lock.json":                                                                 ({"4c1800aee48392e6ca2efa80526b1b2627cec34d": DV}, {}),
  "Blockchain/Dev/services/originate/src/index.ts":                                                                      ({"44d4e4f341f5d314f5b95405b209a9450cde1d3e": DV}, {}),
  "Blockchain/Dev/services/security/package.json":                                                                       ({"a2f2e03ff75b5aba19a9aac97a827cb7a6c50aba": DV}, {}),
  "Blockchain/Dev/services/security/vitest.config.ts":                                                                   ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/security/tsconfig.json":                                                                      ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/services/security/package-lock.json":                                                                  ({"2675691235597a521c8952a5058df29203b4eb8c": DV}, {}),
  "Blockchain/Dev/services/timestamping/package.json":                                                                   ({"450cb6dc189a8552eb0923a44a4a7b29d4b1eb69": DV}, {}),
  "Blockchain/Dev/services/timestamping/vitest.config.ts":                                                               ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/timestamping/tsconfig.json":                                                                  ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/services/timestamping/package-lock.json":                                                              ({"c2f5b451133aef7cb8f00d5e19aba929075d7113": DV}, {}),
  "Blockchain/Dev/services/referral/package.json":                                                                       ({"1bc18b51f0ee6100b70ea65ee2610b9bf0220d7f": DV}, {}),
  "Blockchain/Dev/services/referral/vitest.config.ts":                                                                   ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/referral/tsconfig.json":                                                                      ({"9f2e458392759cbbd831bb9b7689233b46dd950c": DV}, {}),
  "Blockchain/Dev/services/referral/package-lock.json":                                                                  ({"c7bd745800eae211d7fe21d978cd8b316b9f6ba5": DV}, {}),
  "Blockchain/Dev/services/referral/src/index.ts":                                                                       ({"a2e766d5c537d9edbdb1446bce70d9541acd77ce": DV}, {}),
  "Blockchain/Dev/services/mcp-server/package.json":                                                                     ({"940a2e70b03e2aa10ef69beafc98c1170366db26": DV}, {}),
  "Blockchain/Dev/services/mcp-server/vitest.config.ts":                                                                 ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/mcp-server/tsconfig.json":                                                                    ({"c27dc52d7e1c25a6abd3407d4f724f6b9a8d1d8a": DV}, {}),
  "Blockchain/Dev/services/mcp-server/package-lock.json":                                                                ({"780b4cbcb86ad9edc285f2efc66cf708a97f092d": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                          ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                                       ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  "Blockchain/Dev/scripts/fix-libsodium-symlink.js":                                                                     ({"526e024c2c107bb46ec9328c7de6687d4b8b7367": DV}, {}),
  ".githooks/pre-push":                                                                                                  ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/package.json":                                                                                         ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                                                    ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                                                    ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all ten together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json", A + "package-lock.json",
           O + "src/", O + "package.json", O + "jest.config.js", O + "tsconfig.json", O + "package-lock.json",
           S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json", S + "package-lock.json",
           T + "src/", T + "package.json", T + "vitest.config.ts", T + "tsconfig.json", T + "package-lock.json",
           R + "src/", R + "package.json", R + "vitest.config.ts", R + "tsconfig.json", R + "package-lock.json",
           M + "src/", M + "package.json", M + "vitest.config.ts", M + "tsconfig.json", M + "package-lock.json",
           D + "services/anchoring/src/", D + "services/anchoring/package.json", D + "services/auth/src/", D + "services/auth/package.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           SC, "systemTest/", ".githooks/", "Blockchain/Testing/jobs/",
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
tail = "the gate merges the then-current develop onto EACH of the ten heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-ten tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1119.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1119 KS-753: TIER 2' "$PROMPT_FILE" && grep -qF '#1120 KS-1232: TIER 2' "$PROMPT_FILE" && grep -qF '#1121 KS-957: TIER 2' "$PROMPT_FILE" && grep -qF '#1122 KS-1273: TIER 2' "$PROMPT_FILE" && grep -qF '#1123 KS-1275: TIER 2' "$PROMPT_FILE" && grep -qF '#1124 KS-880: TIER 1' "$PROMPT_FILE" && grep -qF '#1125 KS-1223: TIER 1' "$PROMPT_FILE" && grep -qF '#1126 KS-1283: TIER 1' "$PROMPT_FILE" && grep -qF '#1127 KS-1244: TIER 1' "$PROMPT_FILE" && grep -qF '#1128 KS-1234: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1119-#1128 (ten PRs; tier 1 = #1124, #1125, #1126, #1127, #1128)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1120 TWO' "$PROMPT_FILE" && grep -qF '#1122 TWO' "$PROMPT_FILE" && grep -qF '#1125 TWO' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1120 TWO, #1122 TWO, #1125 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b13-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-13th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b13-*) and writing in the seat 2026-09-21_seatB-13th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4006 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4005 / :4006 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          23d60cace7c37bc329ccc425e58659e950089a4d \
          6aa9873f9740 \
          7be81d5c9b109959b559e03652fb092c12de58e8 \
          855c77ac4db8 \
          84ef030470037ea14749365c6dbaf7895afc8624 \
          c35d59b310b6b9d456a4f6b7b1eb8b26859b179d \
          e8b4659fab666a47c2e42c6fe1ec68d0945eb4dc \
          c11e01c5e18b91705ebefec6e160b2c235f1daf6 \
          743126250635ef59c2421471712d90f3a4636449 \
          85ddc802fe50371f051132a88c5141e9b133a0f0 \
          192f34492e33c1b0e00b5fda33531b9cf2234afb \
          b058d498b3b6b86d8eb88df7b03e48d5426dab13 \
          4b32a4d50b3758b2597f2a76e2aa84287a13aae8 \
          bf45a0ddb07a6154b394a70fcb583b44fe5c988f \
          127d9d55be7796ca36449faa123be949f72dee50 \
          d732631dc0c2adfa1cbf3345074f7c39ba41c2f5 \
          e93bfae369f0ba940739c2a22ad25f9718ebda0a \
          59bc927624043f1b5c3bccd03dc98cfec00ef400 \
          fdb125ca3e6ae4516836c4c12ac88e5b34b2ca46 \
          6dfc5731e56e \
          d119e64ba755 \
          530fa32f8d886e70375e967304cf8881edf0e950 \
          f452db039b9dceb34bebd5046525de1e42b1879e \
          82a92ea52407fba3cdeb755efab488854b3e5758 \
          daf9f5c1a6bb586065fcf44559073c25624dcf48 \
          94d0813cc861333a2dc60457d7fac8af9ec6fd17 \
          41f85fcb250ea6cd1b1e6bc33117dab2e7ee93ae \
          e5cc79c5e29b0b657240feb2b8afc2b1d6073ba8 \
          4a90382b7882 \
          7962b0e379ef \
          9fa2a9e41619 \
          79d25bd522ff \
          c944a3e24782 \
          d0333a7bb4ad \
          947a3ec410ef \
          8de000e899a9 \
          46784fc8ed79 \
          ffc3162048bc \
          75b4a70d1503 \
          53f09e6638f7 \
          4aa0c1b41466 \
          430f435447c5 \
          0acfe0d608fd \
          c135806c7c00 \
          3ac42d3bd247 \
          0c06f16a4a40 \
          b8aa0b14a95f \
          d8b2e2654543 \
          VERIFIEDFALSE \
          VERIFIEDATDROPPED \
          RELAYDROPPED \
          RELAYWRONGFIELD \
          RAWDOCTYPES \
          TOOLINGTOKENSGONE \
          NPMGONE \
          YARNGONE \
          VERBLISTSTALE \
          VERBWITHOUTROUTE \
          LIVETENANTRAW \
          WALLETNOTFORWARDED \
          HEADERFALLBACKREMOVED \
          PROVMOUNTUNGUARDED \
          WIDENROLES \
          REFUSALMESSAGECHANGED \
          ALIASNARROWED \
          SANITIZEEVERYWHERE \
          PARSERONNFTALIAS \
          NFTPARSERUNMOUNTED \
          215 \
          44/44 \
          692 \
          690 \
          689 \
          697/697 \
          28/28 \
          5/5 \
          809/809 \
          907/907 \
          '6 ok / 0 FAIL' \
          '5 ok / 0 FAIL' \
          '3 ok / 2 FAIL' \
          '3 ok / 0 FAIL' \
          '106 passed, 0 failed' \
          '41 passed, 0 failed (of 41)' \
          '42 passed, 0 failed (of 42)' \
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
          no-useless-assignment \
          LINT-1 \
          LINT-2 \
          manifest_quarantine \
          KS-1135 \
          'reports nothing moved' \
          drive.ts \
          SIBLING_ALLOW \
          prc_rows \
          quarantine-prc-run1 \
          PROTOCOL-DIFF \
          PROTOCOL-CLEAN \
          'GO: merge #1119-#1128 batch' \
          'Deviation from verbatim: NONE' \
          'linear[bot]' \
          attachmentsForURL \
          contributes \
          'Refs KS-930' \
          ks-930 \
          KS-887 \
          KS-958 \
          KS-794 \
          KS-1133 \
          :5432 \
          anchoring:4005 \
          localhost:6000 \
          203.0.113.7:443 \
          unattributed \
          x-wallet-address \
          rowToApiKey \
          requireOrgProvisioner \
          requireSuperAdmin \
          sanitizeInput \
          shouldParseBody \
          allowedDocumentTypes \
          LIFECYCLE_EVENT_ACTIONS \
          TRIVY_EXIT_CODE \
          '--exit-code 0' \
          TRIVY_JOB_SH \
          shellcheck \
          jq \
          /bin/bash \
          'bash -n' \
          KS-1136 \
          fullName \
          RED-FIRST \
          GREEN-AFTER \
          section_1 \
          section_2 \
          'tolower(L)' \
          'T9 gap' \
          'em dash' \
          127.0.0.1:1 \
          KS-501 \
          KS-480 \
          KS-978 \
          KS-721 \
          KS-522 \
          KS-726 \
          KS-535 \
          KS-867 \
          KS-878 \
          KS-914 \
          KS-1238 \
          KS-1282 \
          KS-1062 \
          KS-869 \
          KS-740 \
          KS-444 \
          KS-921 \
          KS-490 \
          KS-1072 \
          KS-815 \
          KS-1215 \
          KS-1203 \
          KS-1198 \
          KS-1284 \
          KS-1175 \
          KS-1006 \
          KS-1236 \
          KS-570 \
          KS-719 \
          KS-1194 \
          KS-1279 \
          KS-1272 \
          KS-741 \
          KS-1260 \
          KS-1209 \
          KS-953 \
          'Nothing failed' \
          'pairwise overlaps NONE' \
          '<= 92 chars' \
          'six orders' \
          'both ways' \
          4ef6430c3d68e2bb \
          0720a4bfa4a4 \
          7431262506 \
          ALIASUPLOAD-1 \
          ALIASOTHERROUTES-1 \
          SECURITYMIDDLEWARESKIP-1 \
          VERIFIEDPERSISTED-1 \
          MCPINFORAWECHO-1 \
          HTTPSERVERINFOEMPTY-1 \
          F4-TOOLINGTOKENS-1 \
          EXITCODEENV-1 \
          DESCRIPTIONVERBLIST-1 \
          LIVETENANTDEFAULT-1 \
          WALLETFORWARD-1 \
          REFERRALFALLBACK-1 \
          PROVMOUNT-SUPERADMINROUTES-1 \
          REFUSALMESSAGE-1; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-ten tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1119 is KS-753.' "$PROMPT_FILE" && grep -F '#1119' "$BRIEF" | grep -qF 'KS-753' && grep -qF 'PR #1120 is KS-1232.' "$PROMPT_FILE" && grep -F '#1120' "$BRIEF" | grep -qF 'KS-1232' && grep -qF 'PR #1121 is KS-957 + KS-930.' "$PROMPT_FILE" && grep -F '#1121' "$BRIEF" | grep -qF 'KS-957' && grep -qF 'PR #1122 is KS-1273.' "$PROMPT_FILE" && grep -F '#1122' "$BRIEF" | grep -qF 'KS-1273' && grep -qF 'PR #1123 is KS-1275.' "$PROMPT_FILE" && grep -F '#1123' "$BRIEF" | grep -qF 'KS-1275' && grep -qF 'PR #1124 is KS-880.' "$PROMPT_FILE" && grep -F '#1124' "$BRIEF" | grep -qF 'KS-880' && grep -qF 'PR #1125 is KS-1223.' "$PROMPT_FILE" && grep -F '#1125' "$BRIEF" | grep -qF 'KS-1223' && grep -qF 'PR #1126 is KS-1283.' "$PROMPT_FILE" && grep -F '#1126' "$BRIEF" | grep -qF 'KS-1283' && grep -qF 'PR #1127 is KS-1244.' "$PROMPT_FILE" && grep -F '#1127' "$BRIEF" | grep -qF 'KS-1244' && grep -qF 'PR #1128 is KS-1234.' "$PROMPT_FILE" && grep -F '#1128' "$BRIEF" | grep -qF 'KS-1234' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1119 is KS-753. … PR #1128 is KS-1234.)" >&2; exit 32; }
grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes on' "$PROMPT_FILE" && grep -qF -- 'EXACTLY ONE product path on #1122' "$PROMPT_FILE" && grep -qF -- 'files API union 13' "$PROMPT_FILE" && grep -qF -- 'DISJOINTNESS AND THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'at least forward and exact reverse' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'fast-forward = its head tree' "$PROMPT_FILE" && grep -qF -- 'every count from the RUNNER' "$PROMPT_FILE" && grep -qF -- 'THE THREE SKIPPED LEGS AND THE LEG-14 RED' "$PROMPT_FILE" && grep -qF -- 'legs 3, 4, 8' "$PROMPT_FILE" && grep -qF -- 'skip_stack' "$PROMPT_FILE" && grep -qF -- 'GRADE the manifest_quarantine red' "$PROMPT_FILE" && grep -qF -- 'one class with INT-1' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST PER PR UNDER THE COVER RULE' "$PROMPT_FILE" && grep -qF -- 'DEVELOP COVER measured FIRST' "$PROMPT_FILE" && grep -qF -- 'reds == declared ∪ measured cover' "$PROMPT_FILE" && grep -qF -- 'ONE named sibling allowance on #1128' "$PROMPT_FILE" && grep -qF -- '20/20 by exact-line AND raw-substring' "$PROMPT_FILE" && grep -qF -- 'TWO-line block' "$PROMPT_FILE" && grep -qF -- 'THE NAMED SIBLING ALLOWANCE' "$PROMPT_FILE" && grep -qF -- 'expect EXACTLY those two cells red' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST / GREEN-AFTER' "$PROMPT_FILE" && grep -qF -- 'THE ROW MAPPER' "$PROMPT_FILE" && grep -qF -- 'OTHERMAPPERDEFAULT' "$PROMPT_FILE" && grep -qF -- 'KS-887 stays OUT' "$PROMPT_FILE" && grep -qF -- 'THE WALLET HEADER, TWO LANES' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_VOUCH_SECRET' "$PROMPT_FILE" && grep -qF -- 'LINT-1 (LEAD)' "$PROMPT_FILE" && grep -qF -- 'THE MOUNTS' "$PROMPT_FILE" && grep -qF -- 'THIRTEENTHMOUNT' "$PROMPT_FILE" && grep -qF -- 'TWELVE method/path pairs' "$PROMPT_FILE" && grep -qF -- 'tenantAdminJwt()' "$PROMPT_FILE" && grep -qF -- 'THE 401 BODY' "$PROMPT_FILE" && grep -qF -- 'INSTR-1 recurs by construction' "$PROMPT_FILE" && grep -qF -- 'two drives, one cell' "$PROMPT_FILE" && grep -qF -- 'THE ALIAS TRIO AND THE ALLOWANCE' "$PROMPT_FILE" && grep -qF -- 'NOT the CONTROL' "$PROMPT_FILE" && grep -qF -- 'vi.doMock' "$PROMPT_FILE" && grep -qF -- 'makes NO connection at all' "$PROMPT_FILE" && grep -qF -- 'a NEW lane' "$PROMPT_FILE" && grep -qF -- 'MCP_HTTP_PORT=0' "$PROMPT_FILE" && grep -qF -- ':7890 never taken' "$PROMPT_FILE" && grep -qF -- 'CONTROL install verb' "$PROMPT_FILE" && grep -qF -- 'TALLY line' "$PROMPT_FILE" && grep -qF -- 'ONLY product byte of the round graded on its own' "$PROMPT_FILE" && grep -qF -- 'which trivy' "$PROMPT_FILE" && grep -qF -- 'TRIVYYAMLEXITCODE' "$PROMPT_FILE" && grep -qF -- 'completeness detector fires' "$PROMPT_FILE" && grep -qF -- 'REGISTERED schema' "$PROMPT_FILE" && grep -qF -- 'em dash planted as UTF-8' "$PROMPT_FILE" && grep -qF -- 'F3 (LEAD' "$PROMPT_FILE" && grep -qF -- 'testMatch' "$PROMPT_FILE" && grep -qF -- 'THE db.retry INTERMITTENT, LOAD-2 AND THE LEG-14 RED' "$PROMPT_FILE" && grep -qF -- 're-run that suite SERIAL' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'filed by nobody here' "$PROMPT_FILE" && grep -qF -- 'THE CONNECTION CENSUS' "$PROMPT_FILE" && grep -qF -- 'four FIRST sets' "$PROMPT_FILE" && grep -qF -- 'multiplicity scales with' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'KS-1119' "$PROMPT_FILE" && grep -qF -- 'KS-1128' "$PROMPT_FILE" && grep -qF -- 'Completes KS-1244' "$PROMPT_FILE" && grep -qF -- 'recommend' "$PROMPT_FILE" && grep -qF -- 'archived-but-labelled-live' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'proposed cell' "$PROMPT_FILE" && grep -qF -- "local model's next round" "$PROMPT_FILE" && grep -qF -- 'BY DESIGN' "$PROMPT_FILE" && grep -qF -- 'THIRTEEN prior rows CLOSE here' "$PROMPT_FILE" && grep -qF -- 'ONE MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- '#1120 TWO' "$PROMPT_FILE" && grep -qF -- '#1122 TWO' "$PROMPT_FILE" && grep -qF -- '#1125 TWO' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'merge14.py:58' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4006 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday eighteen by-name items (tier/round/product bytes; the trees and disjointness; the skipped legs + the leg-14 red; red-first under the cover rule with the allowance and the covers; #1124 the row mapper; #1125 the wallet header; #1126 the mounts; #1127 the 401 body; #1128 the alias trio; #1119; #1120; #1121+#1122 bash; #1123 jest; the intermittents; census; link hygiene incl. KS-1119..KS-1128; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3 + the line-number discipline) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  ten heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1124 T1, #1125 T1, #1126 T1, #1127 T1, #1128 T1, #1119 T2, #1120 T2, #1121 T2, #1122 T2, #1123 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all ten heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TEN verdict lines"
  echo "  prompt names the report directory, the #1112-#1118 PRIOR REPORT, the #1106-#1111 EARLIER REPORT, the #1102-#1104 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1120 TWO, #1122 TWO, #1125 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b13-*) and the seat 2026-09-21_seatB-13th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4005 / :4006 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (208 tokens: develop + tree, ten head trees, the all-ten tree, thirteen head blobs, 20 plant shas, 20 tamper ids, counts, the allowance, LINT-1/LINT-2/INSTR-1, the leg-14 words, :5432/:4005, archived + foreign keys, the GO subject); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the all-ten tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the ten PRs is"
  echo "  prompt carries Wednesday eighteen by-name items and the standard closing (98 keywords)"
  [ -n "${QAB1119_CUR_DEV:-}" ] && echo "  (develop read from the QAB1119_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1119_BRIEF:-}${QAB1119_PROMPT:-}${QAB1119_HEAD_1128:-}${QAB1119_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
