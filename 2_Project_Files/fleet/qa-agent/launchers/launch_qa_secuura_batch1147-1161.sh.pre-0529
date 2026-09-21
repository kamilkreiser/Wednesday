#!/bin/bash
# launch_qa_secuura_batch1147-1161.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 2 floor (TIER 1 on #1161) over EIGHT
# Secuura/Blockchain PRs (Seat B 16th; twelve local-model R15 TEST-ONLY patches applied --recount and grouped by TICKET = by FILE into eight PRs
# across THREE lanes — originate jest, packages/shared vitest, security vitest — EIGHT paths, ZERO overlap, ZERO product bytes; the seat's PR 8
# KS-1171 HELD un-pushed, NOT here)
#   #1147 PR 1 KS-928 DEMOSEEDGATE @ e456ffb5e  TEST-ONLY ks928-the-demo-seed-gate-s-predicate.test.ts +107/-0 — TIER 2
#   #1149 PR 2 KS-1118 F2 @ 75f5b924e  TEST-ONLY ks1118-verify-documenthash-over-hash.test.ts +150/-0 — TIER 2
#   #1151 PR 3 KS-1133 B @ 10c689dcf  TEST-ONLY ks1133-v2-verify-hash-read-first.test.ts +109/-0 — TIER 2
#   #1153 PR 4 KS-1158 R3 @ be21a0ae4  TEST-ONLY ks1158-r3-network-carry-second-pin.test.ts +96/-0 — TIER 2
#   #1155 PR 5 KS-1229 AFTERVERIFY SIGNCERT SIGNWALLET UNTYPEDSRCb VERSIONTRIM @ b455e4594  TEST-ONLY ks1213-a-derived-writer-relabel-is-refused.test.ts +84/-1 — TIER 2
#   #1157 PR 6 KS-1179 F1 @ 8b0713d8f  TEST-ONLY ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts +98/-0 — TIER 2
#   #1159 PR 7 KS-1181 F3 @ c6af5ca67  TEST-ONLY ks1181-ks-727-error-handler-guard-corpus.test.ts +75/-0 — TIER 2
#   #1161 PR 9 KS-975 ITEM1 @ 7f426f170  TEST-ONLY ks975-malformed-sub-is-refused.test.ts +36/-0 — TIER 1
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 64ab10513: each head's parent IS that
# commit) by pure tree hashing; the eight-PR tree over the parent (c54c1ae73ba3…) by REAL --recount applies in three orders AND real 3-way merges of
# the heads in four orders in a --shared scratch clone (predict_batch_scratch_*.out) AND by tree hashing; every BOTH-list token asserted present in
# the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets17.py (re-keyed to EIGHT) wants exactly ONE equality target PER PR FILE (1/1/1/1/1/1/1/1) and parses the
# list non-greedily to the FIRST `;` — no two-file line this round (the COMMA-separated form is inherited, not exercised); merge17.py asserts each
# squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. EIGHT verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All eight tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 64ab10513 (tree 87b4aa12d2eb, Seat B 15th's final state +
# Peter's #1138). ORIGIN DEVELOP: the pin is 64ab105132eada0621622acf4d6053bc59926780 (tree 87b4aa12d2eb) — UNMOVED since the raise at generation (behind 0); the
# compare per PR reads develop...head = merge_base 64ab10513, ahead 1, BEHIND 0, files 1 ×8 (exit 10 — a develop move changes `behind`
# and REFUSES: re-pin deliberately — Seat C 16th's GO may land its merges first). ALL EIGHT over the parent = c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d;
# ALL EIGHT over the current develop = c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d (the END STATE if every merge lands on 64ab10513).
#
# The develop pin is judged by CONTENT — the 8 target paths at the CURRENT develop (seven NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the ks1213 file by blob) plus 41 unchanged-read paths (this round's 9 tamper files, the
# 15th's five, the hook, preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts, the ks1004 cover test, the
# threadTokenMint test, the four lanes' package.json / config / tsconfig / lock, the Dev package.json + lock, eslint.config.mjs). GUARDED on a move:
# shared / originate / security / anchoring src + config, packages/shared, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs
# (api-gateway / auth — Seat C's lanes — are NOT guarded: a Seat C merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate16B_seatB/mail_gate16B_ready.md, the seat's eight READY mails (17:01:06Z … 18:31:47Z) + its 16:54:31Z and
# 18:33:17Z STATUS mails + its QUESTION / ACK mails, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (#1147 T2, #1149 T2, #1151 T2, #1153 T2, #1155 T2, #1157 T2, #1159 T2, #1161 T1).
# exit 10: the compare per PR (merge_base 64ab10513, ahead 1, behind 0, files 1) — develop moving refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and EIGHT verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1136-#1146), the EARLIER REPORT (#1130-#1135), the OLDER REPORT
#          (#1119-#1128) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets17.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b16-*, s-c16-*) and writing in the seat 2026-09-22_seatB-16th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the eight-PR
#          tree, the held octopus, the eight head blobs, the twelve canonical sha16s, the four STRICT blobs, the suite counts, the --recount rcs,
#          the lock words, the attributions, the archived / content keys, the GO string), and the prompt must ask the gate to MEASURE, not
#          conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the eight-PR tree in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #1147 is KS-928. … ).
# exit 33: the prompt must carry Wednesday TWELVE BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# QAB1147_CUR_DEV (test override, --check only): stands in for origin develop. QAB1147_HEAD_1161 (test override): stands in for #1161 pinned head.
# QAB1147_BRIEF / QAB1147_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1147_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate16B_seatB/gen_launcher_gate16B.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate15.py.
#
# Usage: launch_qa_secuura_batch1147-1161.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1147_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB/mail_gate16B_ready.md}"
PROMPT_FILE="${QAB1147_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1147-1161.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1147|KS-928|refs/heads/feature/ks-928-the-demo-seed-gates-predicate-is-tested-but-its-call-site-is-r15-demoseedgate-1|e456ffb5e9e1e1525f155864452c0aa2cad8752b|1"
  "1149|KS-1118|refs/heads/feature/ks-1118-post-apiverificationverify-the-documenthash-over-hash-r15-f2-1|75f5b924ea28b3a9a68e8d02af8f95f16c28c99d|1"
  "1151|KS-1133|refs/heads/feature/ks-1133-verify-hash-precedence-v1-hash-last-v2-hash-first-document-r15-b-1|10c689dcfb1722c993046a115be82b951db0596f|1"
  "1153|KS-1158|refs/heads/feature/ks-1158-l3a-gate-records-912-r2-937-the-placeholder-hash-anchoredat-r15-r3-1|be21a0ae404c04a966379773a18ce5b5674f8e4b|1"
  "1155|KS-1229|refs/heads/feature/ks-1229-ks1213-cells-ten-tampers-stay-green-a-refused-issue-can-mint-r15-afterverify-signcert-signwallet-untypedsrcb-versiontrim-1|b455e4594865cfd63aea486139d6afae182eb3c6|1"
  "1157|KS-1179|refs/heads/feature/ks-1179-safeoutboundrequest-tests-no-cell-pins-dns-layer-r15-f1-1|8b0713d8ff33c1e4e7690ec6b6b8bb1cda0d138f|1"
  "1159|KS-1181|refs/heads/feature/ks-1181-error-handler-guard-corpus-1-canary-cells-cannot-r15-f3-1|c6af5ca678c4a1ae3aba6bc4cd7a98f796247929|1"
  "1161|KS-975|refs/heads/feature/ks-975-ratelimitscope-tri-state-a-malformed-sub-silently-became-a-r15-item1-1|${QAB1147_HEAD_1161:-7f426f1706bd40a5dd800502d5af9a1968611718}|1"
)
DEVELOP_SHA='64ab105132eada0621622acf4d6053bc59926780'   # the pin = origin develop at generation (= the heads' parent; a move refuses at exit 10 / 18)
MERGE_BASE='64ab105132eada0621622acf4d6053bc59926780'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d'     # all eight over the CURRENT develop (real applies + 3-way merges; generator tree-hash) — the END STATE
ALL_OVER_PARENT='c54c1ae73ba32d9bdd7ed3258a9c19e59ad5cb1d'   # all eight over the parent 64ab10513 (the seat's batch8.py; three + four orders)
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1147-1161-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1136-1146-tier2-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16B_seatB/mail_gate16B_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }
grep -qF 'PENDING-PR-' "$PROMPT_FILE" && { echo "REFUSING: the prompt is PARTIAL (a PENDING-PR- token) — a partial gate is not a gate" >&2; exit 34; }

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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 64ab10513, ahead 1, behind 0,
# files 1 ×8 (generator, rev-list --left-right; the launcher reads the compare API). A develop move -> exit 10.
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
WANT_COMPARE="1147 $MERGE_BASE ahead=1 behind=0 files=1
1149 $MERGE_BASE ahead=1 behind=0 files=1
1151 $MERGE_BASE ahead=1 behind=0 files=1
1153 $MERGE_BASE ahead=1 behind=0 files=1
1155 $MERGE_BASE ahead=1 behind=0 files=1
1157 $MERGE_BASE ahead=1 behind=0 files=1
1159 $MERGE_BASE ahead=1 behind=0 files=1
1161 $MERGE_BASE ahead=1 behind=0 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB (or ABSENT) at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1147_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
SE = D + "services/security/"
AN = D + "services/anchoring/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
JUDGED = {
  "Blockchain/Dev/services/originate/src/__tests__/ks928-the-demo-seed-gate-s-predicate.test.ts":                        ({"ABSENT": DV}, {"a215e136e805694fb21807cb1684a6f0f07135fb": "#1147 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1118-verify-documenthash-over-hash.test.ts":                        ({"ABSENT": DV}, {"01ab706fe9a6b15eb1c5b2f63757b444d15a3969": "#1149 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1133-v2-verify-hash-read-first.test.ts":                            ({"ABSENT": DV}, {"f343c69cd71087c2782dd389021bf77854382c6c": "#1151 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1158-r3-network-carry-second-pin.test.ts":                          ({"ABSENT": DV}, {"0d1db7f6cad9846cccd12e52c66a55a9fe03eb72": "#1153 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts":                  ({"8082826898c21c20822001ecaadbe998a818c144": DV}, {"bbfcd0f98923ca986a5779d937a75398badc03d1": "#1155 own"}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts":              ({"ABSENT": DV}, {"1dd3a0024fa43701664ef80247f71e2a555ab6a4": "#1157 own"}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts":                       ({"ABSENT": DV}, {"cab04d1ae61d31c18bbdf856567b92935b84cfca": "#1159 own"}),
  "Blockchain/Dev/services/security/src/__tests__/ks975-malformed-sub-is-refused.test.ts":                               ({"ABSENT": DV}, {"60015bd01b6ab9da09e223214322b38997dd94a3": "#1161 own"}),
  "Blockchain/Dev/services/originate/src/routes/adminConfig.ts":                                                         ({"62af28d017069d38fa00e7915bfa65226db678c6": DV}, {}),
  "Blockchain/Dev/services/originate/src/routes/verification.ts":                                                        ({"7e122e960a98ea96dd8001deb3d7a85b69be538f": DV}, {}),
  "Blockchain/Dev/services/originate/src/routes/verificationV2.ts":                                                      ({"dfa26c0572d6a3888d7b07bc6172b4b7ef4852e0": DV}, {}),
  "Blockchain/Dev/services/originate/src/services/anchorStateSync.ts":                                                   ({"d8e988f7a479275d967cab6bfd30bca79d3e3f4a": DV}, {}),
  "Blockchain/Dev/services/originate/src/routes/documents.ts":                                                           ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {}),
  "Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts":                                                           ({"efd880010d5f31c5ea17d6229ef3f86f15321ea2": DV}, {}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts":                                 ({"5127297156ed9b970ad17e804b3e3211894b6f8c": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/anchorSubmission.ts":                                                           ({"d3ad106d8e5764a526456b3218e1e8d9ad1a38ba": DV}, {}),
  "Blockchain/Dev/services/security/src/rateLimitScope.ts":                                                              ({"cb51abd021bce9aeb702f83e9e8bfd2401d110f2": DV}, {}),
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
  "Blockchain/Dev/services/originate/src/__tests__/ks1004-anchor-failed-lockout.test.ts":                                ({"4684fb3ad2fa925ff654cf274aad6849b914d0d5": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/threadTokenMint.test.ts":                                             ({"b88b3a43ec5dcb8651b91d5df90e9dec42a1795f": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/services/originate/package.json":                                                                      ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  "Blockchain/Dev/services/originate/tsconfig.json":                                                                     ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  "Blockchain/Dev/services/originate/jest.config.js":                                                                    ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  "Blockchain/Dev/services/originate/package-lock.json":                                                                 ({"4c1800aee48392e6ca2efa80526b1b2627cec34d": DV}, {}),
  "Blockchain/Dev/services/security/package.json":                                                                       ({"a2f2e03ff75b5aba19a9aac97a827cb7a6c50aba": DV}, {}),
  "Blockchain/Dev/services/security/vitest.config.ts":                                                                   ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/security/tsconfig.json":                                                                      ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/services/security/package-lock.json":                                                                  ({"2675691235597a521c8952a5058df29203b4eb8c": DV}, {}),
  "Blockchain/Dev/services/anchoring/package.json":                                                                      ({"a7eed73550b40aa2d968872817fa22e933373831": DV}, {}),
  "Blockchain/Dev/services/anchoring/vitest.config.ts":                                                                  ({"2e1d21f130f8aa80a1c71987f920181dafaf6b90": DV}, {}),
  "Blockchain/Dev/services/anchoring/tsconfig.json":                                                                     ({"f593300cac7c9c3073f15a1287323cf5b9dd478d": DV}, {}),
  "Blockchain/Dev/services/anchoring/package-lock.json":                                                                 ({"7ef3f65a35b48bec2591df4b2859bab9aa237334": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent; behind 0; all eight together " + all_over_dev + " over it, three + four orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           OR + "src/", OR + "package.json", OR + "jest.config.js", OR + "tsconfig.json", OR + "package-lock.json",
           SE + "src/", SE + "package.json", SE + "vitest.config.ts", SE + "tsconfig.json", SE + "package-lock.json",
           AN + "src/", AN + "package.json", AN + "vitest.config.ts", AN + "tsconfig.json", AN + "package-lock.json",
           SC, ".githooks/", D + "package.json", D + "package-lock.json", D + "eslint.config.mjs"]
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the eight-PR tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate16B.py + gen_launcher_gate16B.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 2 floor' "$PROMPT_FILE" && grep -qF '#1147 KS-928: TIER 2' "$PROMPT_FILE" && grep -qF '#1149 KS-1118: TIER 2' "$PROMPT_FILE" && grep -qF '#1151 KS-1133: TIER 2' "$PROMPT_FILE" && grep -qF '#1153 KS-1158: TIER 2' "$PROMPT_FILE" && grep -qF '#1155 KS-1229: TIER 2' "$PROMPT_FILE" && grep -qF '#1157 KS-1179: TIER 2' "$PROMPT_FILE" && grep -qF '#1159 KS-1181: TIER 2' "$PROMPT_FILE" && grep -qF '#1161 KS-975: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 2 floor and each PR own tier line (#1147 T2, #1149 T2, #1151 T2, #1153 T2, #1155 T2, #1157 T2, #1159 T2, #1161 T1)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1147-#1161 (eight PRs; tier 2 floor, tier 1 = #1161: Seat B 16th test-only pins)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'EIGHT lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and EIGHT verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b16-batch' "$PROMPT_FILE" && grep -qF 's-c16-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatB-16th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b16-*, s-c16-*) and writing in the seat 2026-09-22_seatB-16th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          c54c1ae73ba3 \
          649ccf34c6d1 \
          2ede08b37 \
          64ab105132eada0621622acf4d6053bc59926780 \
          64ab10513 \
          87b4aa12d2eb \
          685d5f264 \
          s-b16-ks1171 \
          'GO: merge #1147, #1149, #1151, #1153, #1155, #1157, #1159, #1161 batch' \
          075e5670c8b1 \
          a7f9258d941f \
          7256a271adf3 \
          8138fe9bb3a8 \
          4c105c64e6dd \
          080b50fb0332 \
          4e6cf2cbda1e \
          c5dd18b13d84 \
          a215e136e805 \
          01ab706fe9a6 \
          f343c69cd710 \
          0d1db7f6cad9 \
          bbfcd0f98923 \
          1dd3a0024fa4 \
          cab04d1ae61d \
          60015bd01b6a \
          98a5fa3032f0e5a3 \
          3920a191b5d5f3b8 \
          7d469d279b885243 \
          1d4557e8f2b7578e \
          cd40d58da5117a33 \
          7ec8970968618911 \
          74044d4cda9afd95 \
          264bf565852a205a \
          6a643d4cea7901ba \
          99f11c834aa60bd9 \
          6d42ce5422418cf0 \
          cb1568354a105511 \
          e76b3e90db28 \
          e9dc6e3899f0 \
          6250385ee49e \
          1fcffe443b5c \
          8082826898c2 \
          c771e61f4cbe \
          51d28696e81e \
          a7ac2c174cad \
          d57c47dac730 \
          809 \
          907 \
          216 \
          813/813 \
          812/812 \
          814/814 \
          819/819 \
          914/914 \
          910/910 \
          220/220 \
          835 \
          917 \
          328/329 \
          threadTokenMint \
          'corrupt patch at line 100' \
          --recount \
          TRUNCATION \
          RECOUNT \
          strict \
          '+755/' \
          c54c1ae73ba3 \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          '44 passed, 0 failed (of 44)' \
          PROTOCOL-CLEAN \
          TEST-FILE-ONLY \
          typecheck17 \
          TS2322 \
          'STOP-class 0' \
          netlog.cjs \
          :5432 \
          anchoring:4005 \
          203.0.113.7:443 \
          fast.example:443 \
          ks914-pinned-address \
          started_utc \
          'lock released' \
          attachmentsForURL \
          contributes \
          'linear[bot]' \
          ks1004-anchor-failed-lockout \
          'CARRIED FORWARD' \
          'declared ∪ the measured cover' \
          'EXACTLY ITS DECLARED CELLS' \
          anchors17.json \
          cover-aware \
          ks-727 \
          ks1213 \
          '138 chars' \
          'Q6(b)' \
          KS-1180 \
          '#1150' \
          KS-1185 \
          '#1152' \
          kksecura \
          Blockchain-C \
          'Seat C 16th' \
          57702 \
          16053 \
          S7 \
          S8 \
          ready_send17.sh \
          batch8.py \
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
          KS-1270 \
          KS-1213 \
          KS-1073 \
          KS-1050 \
          KS-1204 \
          KS-1072 \
          KS-1183 \
          KS-999 \
          KS-1018 \
          KS-1285 \
          KS-1123 \
          KS-1171 \
          'Refs KS-928' \
          'Refs KS-1118' \
          'Refs KS-1133' \
          'Refs KS-1158' \
          'Refs KS-1229' \
          'Refs KS-1179' \
          'Refs KS-1181' \
          'Refs KS-975'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the eight-PR tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1147 is KS-928.' "$PROMPT_FILE" && grep -F '#1147' "$BRIEF" | grep -qF 'KS-928' && grep -qF 'PR #1149 is KS-1118.' "$PROMPT_FILE" && grep -F '#1149' "$BRIEF" | grep -qF 'KS-1118' && grep -qF 'PR #1151 is KS-1133.' "$PROMPT_FILE" && grep -F '#1151' "$BRIEF" | grep -qF 'KS-1133' && grep -qF 'PR #1153 is KS-1158.' "$PROMPT_FILE" && grep -F '#1153' "$BRIEF" | grep -qF 'KS-1158' && grep -qF 'PR #1155 is KS-1229.' "$PROMPT_FILE" && grep -F '#1155' "$BRIEF" | grep -qF 'KS-1229' && grep -qF 'PR #1157 is KS-1179.' "$PROMPT_FILE" && grep -F '#1157' "$BRIEF" | grep -qF 'KS-1179' && grep -qF 'PR #1159 is KS-1181.' "$PROMPT_FILE" && grep -F '#1159' "$BRIEF" | grep -qF 'KS-1181' && grep -qF 'PR #1161 is KS-975.' "$PROMPT_FILE" && grep -F '#1161' "$BRIEF" | grep -qF 'KS-975' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1147 is KS-928. … )" >&2; exit 32; }
grep -qF -- 'TIER AND ROUND' "$PROMPT_FILE" && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'outside __tests__: []' "$PROMPT_FILE" && grep -qF -- 'files API union 8' "$PROMPT_FILE" && grep -qF -- 'Any product byte' "$PROMPT_FILE" && grep -qF -- 'STATE WHICH by the files API' "$PROMPT_FILE" && grep -qF -- 'TEST-FILE-ONLY:' "$PROMPT_FILE" && grep -qF -- 'the test file exactly' "$PROMPT_FILE" && grep -qF -- 'the RECOUNT column' "$PROMPT_FILE" && grep -qF -- 'name-status A ×7 / M ×1' "$PROMPT_FILE" && grep -qF -- 'THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'EIGHT' "$PROMPT_FILE" && grep -qF -- 'ZERO overlap' "$PROMPT_FILE" && grep -qF -- 'at least forward, exact reverse and one shuffle' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'state the SET you read and WHEN' "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY with the `--recount` class' "$PROMPT_FILE" && grep -qF -- '`--recount` is MANDATORY on every apply this round' "$PROMPT_FILE" && grep -qF -- 'per stage for #1155' "$PROMPT_FILE" && grep -qF -- "Name each READY's strict / recount" "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'THE CELLS: green at head' "$PROMPT_FILE" && grep -qF -- 'every declared cell + control' "$PROMPT_FILE" && grep -qF -- 'per-tamper' "$PROMPT_FILE" && grep -qF -- 'reds EXACTLY the declared set' "$PROMPT_FILE" && grep -qF -- 'tamper files restored by bytes' "$PROMPT_FILE" && grep -qF -- 'admitted by NAME' "$PROMPT_FILE" && grep -qF -- 'PER-FILE TYPECHECK DELTA 0' "$PROMPT_FILE" && grep -qF -- 'planted TS2322 control CAUGHT' "$PROMPT_FILE" && grep -qF -- 'a zero that needs its control' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE v2: loopback only, zero :5432' "$PROMPT_FILE" && grep -qF -- 'unestablished EXTERNAL attempts REPORTED' "$PROMPT_FILE" && grep -qF -- '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run' "$PROMPT_FILE" && grep -qF -- 'login_stub cleared by PID' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'Backlog -> In Progress walks recorded' "$PROMPT_FILE" && grep -qF -- 'KS-975 assigned to the board login at item 0' "$PROMPT_FILE" && grep -qF -- 'no archived key in any branch' "$PROMPT_FILE" && grep -qF -- 'Recommend nothing' "$PROMPT_FILE" && grep -qF -- "PR #1158 is Seat C's KS-855" "$PROMPT_FILE" && grep -qF -- 'THE TWO-SEAT ARTEFACTS' "$PROMPT_FILE" && grep -qF -- 'every push INSIDE the push-window lock' "$PROMPT_FILE" && grep -qF -- 'grade present / absent + MONOTONIC' "$PROMPT_FILE" && grep -qF -- "attributions the seat made for Seat C's PRs BY NAME" "$PROMPT_FILE" && grep -qF -- 'four-condition rule' "$PROMPT_FILE" && grep -qF -- 'ONLY tolerated state change' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S OWN FINDINGS / SLIPS" "$PROMPT_FILE" && grep -qF -- 'CONFIRMED / REFUTED' "$PROMPT_FILE" && grep -qF -- 'S7 the eight-PR body paragraph' "$PROMPT_FILE" && grep -qF -- 'S6 the sender WRAPPER killed by Seat C' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- '5 s timeouts' "$PROMPT_FILE" && grep -qF -- 're-run standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM — EIGHT lines VERBATIM' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER' "$PROMPT_FILE" && grep -qF -- 'alone-tree reading' "$PROMPT_FILE" && grep -qF -- 'stays In Progress' "$PROMPT_FILE" && grep -qF -- 'SHIPS-WITH text ≤ 3 sentences' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED rows NAMED' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED for its own file' "$PROMPT_FILE" && grep -qF -- 'sha256 + byte count IN the mail' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED written FIRST' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" && grep -qF -- 'NAMESPACE GUARD' "$PROMPT_FILE" && grep -qF -- 'EIGHT lines, one per PR' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'node_modules per ENTRY' "$PROMPT_FILE" && grep -qF -- 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF -- 'no memory maintenance' "$PROMPT_FILE" && grep -qF -- 'NEVER print a credential value' "$PROMPT_FILE" && grep -qF -- 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" && grep -qF -- 'NEVER touch the push-window lock directory' "$PROMPT_FILE" && grep -qF -- 'by ANCESTRY' "$PROMPT_FILE" && grep -qF -- 'never by a basename' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; test-file-only; the trees and the zero overlap; canonical identity with the recount class; the cells; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries the TIER 2 floor and each PR tier (#1147 T2, #1149 T2, #1151 T2, #1153 T2, #1155 T2, #1157 T2, #1159 T2, #1161 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, EIGHT verdict lines"
  echo "  prompt names the report directory, the #1136-#1146 PRIOR REPORT, the #1130-#1135 EARLIER REPORT, the #1119-#1128 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b16-*, s-c16-*) and the seat 2026-09-22_seatB-16th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (158 tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the eight-PR tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (97 keywords)"
  [ -n "${QAB1147_CUR_DEV:-}" ] && echo "  (develop read from the QAB1147_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1147_BRIEF:-}${QAB1147_PROMPT:-}${QAB1147_HEAD_1161:-}${QAB1147_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
