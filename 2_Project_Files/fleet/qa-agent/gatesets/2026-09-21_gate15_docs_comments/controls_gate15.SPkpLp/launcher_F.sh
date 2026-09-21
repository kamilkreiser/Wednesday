#!/bin/bash
# launch_qa_secuura_batch1136-1146.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 2 floor over TEN Secuura/Blockchain PRs
# (Seat B 15th; fourteen local-model DOC / COMMENT patches grouped by FILE into ten PRs across FIVE lanes — docs, packages/shared vitest,
# originate jest, vc-issuer vitest, api-gateway vitest — ELEVEN paths, ZERO overlap, ZERO product bytes)
#   #1136 PR 1 KS-1035 + KS-1036 D + item3 @ 6f5c31c45  DOCS-ONLY DEV-PROCESS.md +12/-0 — TIER 2
#   #1137 PR 2 KS-1037 + KS-1049 R15 + A @ 08f931532  DOCS-ONLY CONTRIBUTING.md +10/-0 — TIER 2
#   #1139 PR 3 KS-1045 A + B @ 9b2cf251c  DOCS-ONLY KINTSUGI-DEV-SERVER-PLAN.md +3/-3 — TIER 2
#   #1140 PR 4 KS-1097 Da @ 21c87abe3  DOCS-ONLY CLAUDE.md +1/-1 — TIER 2
#   #1141 PR 5 KS-890 R15 @ e4ae24b7f  DOCS-ONLY DEPLOYMENT-ARCHITECTURE.md +8/-0 — TIER 2
#   #1142 PR 6 KS-1140 GF2GF4 @ 51d47ea44  TEST-FILE-COMMENT-ONLY ks879-no-raw-control-bytes-repo-wide.test.ts +2/-2 — TIER 2
#   #1143 PR 7 KS-1152 R1c + R1d @ 7cb87fedb  TEST-FILE-COMMENT-ONLY ks764-key-revoke-call-site-guard.test.ts + ks764-admin-api-keys-revoke-route-contract.test.ts +5/-3 — TIER 2
#   #1144 PR 8 KS-979 R15 @ 5c1f70149  TEST-FILE-COMMENT-ONLY ks597-issuer-org-bind.test.ts +6/-2 — TIER 2
#   #1145 PR 9 KS-1120 F3 @ 6cba33e52  TEST-FILE-COMMENT-ONLY ks1020-presentation-lookup-exact-or-404.test.ts +5/-3 — TIER 2
#   #1146 PR 10 KS-1156 A3 @ abb48650b  TEST-FILE-COMMENT-ONLY ks835-oauth-token-scope-gate.test.ts +1/-1 — TIER 2
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 581ed7fa1: each head's parent IS that
# commit) by pure tree hashing; the all-ten tree over the parent (a93fe063d28a…) and over the CURRENT develop by REAL applies + 3-way merges in a
# --shared scratch clone (predict_batch_scratch_*.out) AND by tree hashing; every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets16.py wants exactly ONE equality target PER PR FILE (1/1/1/1/1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` — the two-file PR 7 addendum line carries TWO targets COMMA-separated (exit 25); merge16.py asserts each squash body's key set ==
# the PR's OWN Refs set (two keys on #1136 and #1137 only).
# Batched under Kam 2026-09-18 standing rule. TEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All twelve tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 581ed7fa1 (tree 60bd96e7078c, Seat B 14th's final state).
# ORIGIN DEVELOP HAS MOVED SINCE (PR #1138 KS-1285, a MERGE commit at 12:44:19Z, 3 commits / 7 files under systemTest/ + Projects Documents/, none
# of this round's 11 paths, none of the paths the gate reads): the pin is the CURRENT develop b192ffd4a61d1b01bb9485a0f5260ca9fd69cf05 (tree 30c3e9342d64); the compare per PR reads
# develop...head = merge_base 581ed7fa1, ahead 1, BEHIND 3, files 1/1/1/1/1/1/2/1/1/1 (exit 10 — a FURTHER develop move changes `behind` and
# REFUSES: re-pin deliberately). ALL TEN over the parent = a93fe063d28ae66d4a90e1926b78364a7a578ff4; ALL TEN over the current develop = 87b4aa12d2ebae335f11790ceed9158f7d5614ec
# (the END STATE if every merge lands on b192ffd4a).
#
# The develop pin is judged by CONTENT — the 11 target paths by blob at the CURRENT develop (any at a head blob -> exit 19 LANDED, naming the PR;
# any other blob -> exit 18 GUARDED) plus 30 unchanged-read paths (the 14th's five tamper files, the hook, preflight.sh, run-shell-suites.sh,
# fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the four lanes' package.json / config / tsconfig / lock, the Dev package.json + lock,
# eslint.config.mjs). GUARDED on a further move: shared / originate / vc-issuer / api-gateway src + config, packages/shared, scripts/, .githooks/,
# docs/, deployment/, CONTRIBUTING.md, CLAUDE.md, the Dev package.json + lock, eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate15_docs_comments/mail_gate15_ready.md, the seat's READY mails (12:34:14Z …) + the 12:30:09Z STATUS mail + the
# 12:02:12Z plan-confirmation QUESTION, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (#1136 T2, #1137 T2, #1139 T2, #1140 T2, #1141 T2, #1142 T2, #1143 T2, #1144 T2, #1145 T2, #1146 T2).
# exit 10: the compare per PR (merge_base 581ed7fa1, ahead 1, behind 3, files) — develop moving AGAIN refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1130-#1135), the EARLIER REPORT (#1119-#1128), the OLDER REPORT
#          (#1112-#1118) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for PR 7, comma-separated),
#          the `## MERGE ADDENDUM` heading targets16.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b15-*) and writing in the seat 2026-09-21_seatB-15th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the all-ten
#          tree, the eleven head blobs, the 14 canonical sha16s, the suite counts, the --recount rcs, the VM read words, the stale-claim words, the
#          archived / content keys, the branch-name findings, the develop move), and the prompt must ask the gate to MEASURE, not conclude, and to
#          RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-ten trees in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket(s) the PR is (PR #1136 is KS-1035 + KS-1036. … ).
# exit 33: the prompt must carry Wednesday THIRTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; a record, never a gate.
# QAB1136_CUR_DEV (test override, --check only): stands in for origin develop. QAB1136_HEAD_1146 (test override): stands in for #1146 pinned head.
# QAB1136_BRIEF / QAB1136_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1136_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate15_docs_comments/gen_launcher_gate15.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1130.py.
#
# Usage: launch_qa_secuura_batch1136-1146.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1136_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments/mail_gate15_ready.md}"
PROMPT_FILE="${QAB1136_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1136-1146.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket(s)|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1136|KS-1035+KS-1036|refs/heads/feature/ks-1035-the-merge-gate-cannot-see-a-withdrawn-approval-813-reads-r15-d-item3-1|6f5c31c455df5f75d2cc4db93dd5bdfb85cb0dfb|1"
  "1137|KS-1037+KS-1049|refs/heads/feature/ks-1037-the-no-force-push-rule-exists-only-in-githookspre-push-and-r15-a-1|08f931532e4f5effeea6144be63b3755267ad351|1"
  "1139|KS-1045|refs/heads/feature/ks-1045-kintsugi-dev-server-planmd-still-says-the-vm-has-not-been-r15-a-b-1|9b2cf251cc4228b47b75e3c6f53b5ac46cbbaa67|1"
  "1140|KS-1097|refs/heads/feature/ks-1097-merge-rule-docs-after-957-the-v4-footer-and-two-gate-r15-da-1|21c87abe391be6afc001e35ded57807b88e7c91d|1"
  "1141|KS-890|refs/heads/feature/ks-890-runbook-a-code-first-deploy-leg-must-use-docker-compose-up-d-r15-1|e4ae24b7fd5c96258bf2729cc72d2d9682dc1ca3|1"
  "1142|KS-1140|refs/heads/feature/ks-1140-ks879-guard-the-cell-walks-the-tree-on-its-own-r15-gf2gf4-1|51d47ea44ec7d644d1181e0e722ce0fa3b19cd2e|1"
  "1143|KS-1152|refs/heads/feature/ks-1152-l5-gate-records-799880985-jwtts-citation-x5-security-log-r15-r1c-r1d-1|7cb87fedb30e12a0983d426de9e9549f968148a1|2"
  "1144|KS-979|refs/heads/feature/ks-979-own-bind-test-file-repeats-two-claims-that-were-r15-1|5c1f701491632917e90b0806adfef0b656c76267|1"
  "1145|KS-1120|refs/heads/feature/ks-1120-get-apipresentationsid-exact-or-404-the-memory-path-prefix-r15-f3-1|6cba33e52290f3903a2671f51277b01851e7b42e|1"
  "1146|KS-1156|refs/heads/feature/ks-1156-auth4-gate-records-983-r2-984-r2-986-987-h-limiter-r15-a3-1|${QAB1136_HEAD_1146:-abb48650be67d27b3d5e405db71d5c7a6ffff177}|1"
)
DEVELOP_SHA='b192ffd4a61d1b01bb9485a0f5260ca9fd69cf05'   # the pin = origin develop at generation (MOVED off the heads' parent by #1138; a FURTHER move refuses at exit 10 / 18)
MERGE_BASE='581ed7fa124b85c7c2da89ac05d52f99c2502911'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='87b4aa12d2ebae335f11790ceed9158f7d5614ec'     # all ten over the CURRENT develop (real 3-way + canonical apply, three orders; generator tree-hash) — the END STATE
ALL_OVER_PARENT='a93fe063d28ae66d4a90e1926b78364a7a578ff4'   # all ten over the parent 581ed7fa1 (the seat's octopus; three orders)
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1136-1146-tier2-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate15_docs_comments/mail_gate15_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
grep -qF 'PENDING-PR-' "$PROMPT_FILE" && { echo "REFUSING: the prompt is PARTIAL (a PENDING-PR- token) — re-fill once every READY is captured (README.md section 8); a partial gate is not a gate" >&2; exit 34; }

# The heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 581ed7fa1, ahead 1, behind 3 (the
# #1138 move), files 1/1/1/1/1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A FURTHER develop move -> exit 10.
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
WANT_COMPARE="1136 $MERGE_BASE ahead=1 behind=3 files=1
1137 $MERGE_BASE ahead=1 behind=4 files=1
1139 $MERGE_BASE ahead=1 behind=3 files=1
1140 $MERGE_BASE ahead=1 behind=3 files=1
1141 $MERGE_BASE ahead=1 behind=3 files=1
1142 $MERGE_BASE ahead=1 behind=3 files=1
1143 $MERGE_BASE ahead=1 behind=3 files=2
1144 $MERGE_BASE ahead=1 behind=3 files=1
1145 $MERGE_BASE ahead=1 behind=3 files=1
1146 $MERGE_BASE ahead=1 behind=3 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved
# further — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1136_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
SH = D + "packages/shared/"
OR = D + "services/originate/"
VC = D + "services/vc-issuer/"
AG = D + "services/api-gateway/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})
JUDGED = {
  "Blockchain/Dev/docs/DEV-PROCESS.md":                                                                                  ({"c9cd41d588a2974c589a5c05472755192363cdd1": DV}, {"ab9a70f13e3c18b270117297d5e5dad5f0be38c1": "#1136 own"}),
  "Blockchain/Dev/CONTRIBUTING.md":                                                                                      ({"953067eb7aa753f34c40a07f56bdbbf1754fcd96": DV}, {"b3cc10a400898d6ea2211f870984f810897f1dc5": "#1137 own"}),
  "Blockchain/Dev/deployment/KINTSUGI-DEV-SERVER-PLAN.md":                                                               ({"bbd5bbf787781137054cd076d2da78c55b123140": DV}, {"5ba84caf2e309357d877c91d6ba2d9bdfbd070b0": "#1139 own"}),
  "CLAUDE.md":                                                                                                           ({"dd782eab7435f328649d8e8e343bace342bce865": DV}, {"ef2f8fc2e4cb614c72cf64b2b32bc60509a4a3ea": "#1140 own"}),
  "Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md":                                                                ({"daabe1087bb99ad3db28324ba6a9f3ecf074c0fe": DV}, {"622c0e50527846e559625e376303a4b03db1ca3f": "#1141 own"}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks879-no-raw-control-bytes-repo-wide.test.ts":                           ({"7f0ac617f67565ffc044d082427b6f6a223381d6": DV}, {"9ce9e852ae447d71c2d41c8d19860225dfef51fc": "#1142 own"}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts":                               ({"ab8e46d795d268822924a57e2630403be1963497": DV}, {"6a51358e36197702bbf5214e7c135fd912d4f353": "#1143 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts":                  ({"eb7782db881608cc4f8b9c4c4da53b170bdaea8c": DV}, {"57de2c6753e451aa4423f86bb5a873876547d212": "#1143 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks597-issuer-org-bind.test.ts":                                       ({"9bb899a106776ba1cf3b256130ce476e6713b2b1": DV}, {"bed97468d49931d2d4daedb1ea4824ae4f48ff27": "#1144 own"}),
  "Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts":                     ({"eb0e5305c8150ba6cde1034c05be79f641607962": DV}, {"b7949520cf038cce186e2ea00d9e8390f0622077": "#1145 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks835-oauth-token-scope-gate.test.ts":                              ({"548e1ec1217ef627aeea06da43a9a8c284161b86": DV}, {"595bed15d85962f3dfb630945cdb7715243ad08f": "#1146 own"}),
  "Blockchain/Testing/jobs/04-container-trivy.sh":                                                                       ({"6dfc5731e56ede5e5a6f420cccd92874b7566a87": DV}, {}),
  "systemTest/fixtures/manifest.ts":                                                                                     ({"a6bfe3e7662791866e16c04331ba8fdc473a535a": DV}, {}),
  "Blockchain/Dev/services/security/src/index.ts":                                                                       ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/users.ts":                                                                    ({"3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d": DV}, {}),
  "Blockchain/Dev/scripts/check-shared-relink.sh":                                                                       ({"4e0704b6c7b9f4db2ceebf0530015e3b2f469662": DV}, {}),
  ".githooks/pre-push":                                                                                                  ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                                       ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                          ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/fix-libsodium-symlink.js":                                                                     ({"526e024c2c107bb46ec9328c7de6687d4b8b7367": DV}, {}),
  "Blockchain/Dev/services/auth/src/services/jwt.ts":                                                                    ({"26562a22470af688ae733000792a2b0321650145": DV}, {}),
  "Blockchain/Dev/services/originate/src/services/provenance.ts":                                                        ({"483aa9eb331d2caa5af285e20d9668a9dbcd92a6": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts":                                                             ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/services/originate/package.json":                                                                      ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  "Blockchain/Dev/services/originate/tsconfig.json":                                                                     ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  "Blockchain/Dev/services/originate/jest.config.js":                                                                    ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  "Blockchain/Dev/services/originate/package-lock.json":                                                                 ({"4c1800aee48392e6ca2efa80526b1b2627cec34d": DV}, {}),
  "Blockchain/Dev/services/vc-issuer/package.json":                                                                      ({"27888b6eeb6c20b44af947d14eddb3bccf6293cf": DV}, {}),
  "Blockchain/Dev/services/vc-issuer/vitest.config.ts":                                                                  ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/vc-issuer/tsconfig.json":                                                                     ({"b3546b85f68847a2cd62ad74f10f5f7347579bc5": DV}, {}),
  "Blockchain/Dev/services/vc-issuer/package-lock.json":                                                                 ({"b0b66b5018e556731056875d4c1720945e3478e7": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                                                    ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                                                ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                                                   ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package-lock.json":                                                               ({"5ec55d86d83f93e70dc03676293331fd3bc250e5": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the post-#1138 tip; every head parent is 581ed7fa1, behind 3; all ten together " + all_over_dev + " over it, three orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           OR + "src/", OR + "package.json", OR + "jest.config.js", OR + "tsconfig.json", OR + "package-lock.json",
           VC + "src/", VC + "package.json", VC + "vitest.config.ts", VC + "tsconfig.json", VC + "package-lock.json",
           AG + "src/", AG + "package.json", AG + "vitest.config.ts", AG + "tsconfig.json", AG + "package-lock.json",
           SC, ".githooks/", D + "docs/", D + "deployment/", D + "CONTRIBUTING.md", "CLAUDE.md",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-ten tree"
print("OK " + state + " | origin develop MOVED AGAIN %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_gate15.py + predict_batch_scratch_gate15.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 2 floor' "$PROMPT_FILE" && grep -qF '#1136 KS-1035 + KS-1036: TIER 2' "$PROMPT_FILE" && grep -qF '#1137 KS-1037 + KS-1049: TIER 2' "$PROMPT_FILE" && grep -qF '#1139 KS-1045: TIER 2' "$PROMPT_FILE" && grep -qF '#1140 KS-1097: TIER 2' "$PROMPT_FILE" && grep -qF '#1141 KS-890: TIER 2' "$PROMPT_FILE" && grep -qF '#1142 KS-1140: TIER 2' "$PROMPT_FILE" && grep -qF '#1143 KS-1152: TIER 2' "$PROMPT_FILE" && grep -qF '#1144 KS-979: TIER 2' "$PROMPT_FILE" && grep -qF '#1145 KS-1120: TIER 2' "$PROMPT_FILE" && grep -qF '#1146 KS-1156: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 2 floor and each PR own tier line (#1136 T2, #1137 T2, #1139 T2, #1140 T2, #1141 T2, #1142 T2, #1143 T2, #1144 T2, #1145 T2, #1146 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1136-#1146 (ten PRs; tier 2 floor: five docs + five test-file comments)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'TWO comma-separated = MG-2' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (PR 7 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b15-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-15th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b15-*) and writing in the seat 2026-09-21_seatB-15th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          a93fe063d28ae66d4a90e1926b78364a7a578ff4 \
          60bd96e7078c \
          581ed7fa124b85c7c2da89ac05d52f99c2502911 \
          a39d35b05 \
          b192ffd4a \
          4cd290a2c80e \
          0edbb8341e60 \
          d1ba6f8882fd \
          4f0a8c67f95f \
          374c0328a8c5 \
          99a9adaf3151 \
          6e95645e29fb \
          366ec698c266 \
          07d01c8ae4f5 \
          9fdeab78e610 \
          ab9a70f13e3c \
          b3cc10a40089 \
          5ba84caf2e30 \
          ef2f8fc2e4cb \
          622c0e505278 \
          9ce9e852ae44 \
          6a51358e3619 \
          57de2c6753e4 \
          bed97468d499 \
          b7949520cf03 \
          595bed15d859 \
          849507a10f99b9ab \
          8a49e7c68318cb58 \
          b9ed6eb6bac788a7 \
          d5a07523e6a450f7 \
          2497bea61ff7789f \
          66aa75dfcf5ea1f3 \
          d41e4136c612bac5 \
          3b8d82cf560c2605 \
          42486061ffa4448e \
          31ae771c8a5f8fe5 \
          7ddcf0309e15ba55 \
          1c0121de5b00ce95 \
          ee3c484b2aff8ff0 \
          8d60c7b67227561c \
          907/907 \
          809/809 \
          123/123 \
          697/697 \
          'corrupt patch at line 16' \
          'corrupt patch at line 19' \
          'corrupt patch at line 10' \
          DEV-PROCESS.md:224 \
          --recount \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          '44 passed, 0 failed (of 44)' \
          PROTOCOL-CLEAN \
          DOCS-ONLY \
          'const x = 1;' \
          IDENTICAL \
          tsc \
          eslint \
          TS2322 \
          typecheck16 \
          'STOP-class 0' \
          netlog.cjs \
          :5432 \
          'az vm show' \
          SECUURA-DEMO-RG \
          secuura02-kintsugi-vm \
          ResourceNotFound \
          Enabled \
          'step 6' \
          :303 \
          'seven times' \
          generateAccessToken \
          provenance.ts:109 \
          F1 \
          F2 \
          F4 \
          F5 \
          F8 \
          S1 \
          'linear[bot]' \
          attachmentsForURL \
          contributes \
          'Refs KS-1035' \
          'Refs KS-1036' \
          'Refs KS-1037' \
          'Refs KS-1049' \
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
          KS-971 \
          KS-1078 \
          KS-921 \
          KS-490 \
          KS-597 \
          KS-727 \
          KS-764 \
          KS-879 \
          KS-1020 \
          KS-835 \
          KS-869 \
          KS-601 \
          KS-973 \
          KS-1118 \
          KS-1158 \
          KS-1181 \
          x5 \
          ks879 \
          'Deviation from verbatim' \
          '<= 92 chars' \
          '#920' \
          '#887' \
          b192ffd4a \
          MOVED \
          Live-but-foreign \
          'GO: merge #1136, #1137, #1139, #1140, #1141, #1142, #1143, #1144, #1145, #1146 batch'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-ten trees, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1136 is KS-1035 + KS-1036.' "$PROMPT_FILE" && grep -F '#1136' "$BRIEF" | grep -qF 'KS-1035' && grep -qF 'PR #1137 is KS-1037 + KS-1049.' "$PROMPT_FILE" && grep -F '#1137' "$BRIEF" | grep -qF 'KS-1037' && grep -qF 'PR #1139 is KS-1045.' "$PROMPT_FILE" && grep -F '#1139' "$BRIEF" | grep -qF 'KS-1045' && grep -qF 'PR #1140 is KS-1097.' "$PROMPT_FILE" && grep -F '#1140' "$BRIEF" | grep -qF 'KS-1097' && grep -qF 'PR #1141 is KS-890.' "$PROMPT_FILE" && grep -F '#1141' "$BRIEF" | grep -qF 'KS-890' && grep -qF 'PR #1142 is KS-1140.' "$PROMPT_FILE" && grep -F '#1142' "$BRIEF" | grep -qF 'KS-1140' && grep -qF 'PR #1143 is KS-1152.' "$PROMPT_FILE" && grep -F '#1143' "$BRIEF" | grep -qF 'KS-1152' && grep -qF 'PR #1144 is KS-979.' "$PROMPT_FILE" && grep -F '#1144' "$BRIEF" | grep -qF 'KS-979' && grep -qF 'PR #1145 is KS-1120.' "$PROMPT_FILE" && grep -F '#1145' "$BRIEF" | grep -qF 'KS-1120' && grep -qF 'PR #1146 is KS-1156.' "$PROMPT_FILE" && grep -F '#1146' "$BRIEF" | grep -qF 'KS-1156' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1136 is KS-1035 + KS-1036. … )" >&2; exit 32; }
grep -qF -- 'TIER AND ROUND' "$PROMPT_FILE" && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'outside __tests__ and *.md: []' "$PROMPT_FILE" && grep -qF -- 'files API union 11' "$PROMPT_FILE" && grep -qF -- 'Any product byte anywhere = a NO GO' "$PROMPT_FILE" && grep -qF -- 'THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'ELEVEN' "$PROMPT_FILE" && grep -qF -- 'ZERO overlap' "$PROMPT_FILE" && grep -qF -- 'at least forward, exact reverse and one shuffle' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'every count from the RUNNER' "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY' "$PROMPT_FILE" && grep -qF -- 'RE-EXTRACTED by you' "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'THREE by `--recount`' "$PROMPT_FILE" && grep -qF -- 'COMMENT-ONLY PROOF' "$PROMPT_FILE" && grep -qF -- 'PLANTED `const x = 1;` control' "$PROMPT_FILE" && grep -qF -- 'IDENTICAL by TITLE' "$PROMPT_FILE" && grep -qF -- 'eslint 0/0 on the six files with a firing control' "$PROMPT_FILE" && grep -qF -- 'DOCS-ONLY PROOF' "$PROMPT_FILE" && grep -qF -- 'exactly the one `.md`' "$PROMPT_FILE" && grep -qF -- "GRADE THE SEAT'S STATEMENT" "$PROMPT_FILE" && grep -qF -- 'THE STALE-CLAIM FINDINGS' "$PROMPT_FILE" && grep -qF -- 'Minor SHIPS-WITH' "$PROMPT_FILE" && grep -qF -- 'dangling' "$PROMPT_FILE" && grep -qF -- 'who inherited it' "$PROMPT_FILE" && grep -qF -- "KS-1045-A's DONE row" "$PROMPT_FILE" && grep -qF -- 'PROVENANCE' "$PROMPT_FILE" && grep -qF -- 'present / absent' "$PROMPT_FILE" && grep -qF -- 'does NOT run `az`' "$PROMPT_FILE" && grep -qF -- 'BRANCH NAMES' "$PROMPT_FILE" && grep -qF -- '`ks-597s-` ABSENT' "$PROMPT_FILE" && grep -qF -- 'no non-ASCII byte in ANY of the ten branch names' "$PROMPT_FILE" && grep -qF -- 'ONE `Refs` on a' "$PROMPT_FILE" && grep -qF -- 'ASCII and <= 92 chars' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'KS-1136' "$PROMPT_FILE" && grep -qF -- 'KS-1147' "$PROMPT_FILE" && grep -qF -- 'EXCEPT KS-1140 for pull/' "$PROMPT_FILE" && grep -qF -- 'Recommend nothing' "$PROMPT_FILE" && grep -qF -- 'PR #1036 is OPEN and is KS-763' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE (v2)' "$PROMPT_FILE" && grep -qF -- 'ALLOW set' "$PROMPT_FILE" && grep -qF -- '"port":5432,' "$PROMPT_FILE" && grep -qF -- 'login_stub cleared by PID' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- '5 s timeouts' "$PROMPT_FILE" && grep -qF -- 're-run standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM — TEN lines VERBATIM' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER' "$PROMPT_FILE" && grep -qF -- 'TWO comma-separated = MG-2' "$PROMPT_FILE" && grep -qF -- 'alone-tree reading' "$PROMPT_FILE" && grep -qF -- 'stays In Progress' "$PROMPT_FILE" && grep -qF -- 'SHIPS-WITH text ≤ 3 sentences' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED rows: NONE EXPECTED' "$PROMPT_FILE" && grep -qF -- 'sha256 + byte count IN the mail' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S SLIPS S1-S4 + F8 as measured" "$PROMPT_FILE" && grep -qF -- 'CONFIRMED / REFUTED' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME' "$PROMPT_FILE" && grep -qF -- 'WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" && grep -qF -- 'NAMESPACE GUARD' "$PROMPT_FILE" && grep -qF -- 'TEN lines, one per PR' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'node_modules per ENTRY' "$PROMPT_FILE" && grep -qF -- 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF -- 'no memory maintenance' "$PROMPT_FILE" && grep -qF -- 'NEVER print a credential value' "$PROMPT_FILE" && grep -qF -- 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday thirteen by-name items (tier/round; the trees and the zero overlap; canonical identity; the comment-only proof; the docs-only proof; the stale-claim findings; the VM provenance; branch names; Linear hygiene; the census rule; the intermittents; the addendum; the seat slips + F8 + the line-number discipline) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries the TIER 2 floor and each PR tier (#1136 T2, #1137 T2, #1139 T2, #1140 T2, #1141 T2, #1142 T2, #1143 T2, #1144 T2, #1145 T2, #1146 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TEN verdict lines"
  echo "  prompt names the report directory, the #1130-#1135 PRIOR REPORT, the #1119-#1128 EARLIER REPORT, the #1112-#1118 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (PR 7 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b15-*) and the seat 2026-09-21_seatB-15th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (131 tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-ten trees, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each PR is"
  echo "  prompt carries Wednesday thirteen by-name items and the standard closing (91 keywords)"
  [ -n "${QAB1136_CUR_DEV:-}" ] && echo "  (develop read from the QAB1136_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1136_BRIEF:-}${QAB1136_PROMPT:-}${QAB1136_HEAD_1146:-}${QAB1136_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
