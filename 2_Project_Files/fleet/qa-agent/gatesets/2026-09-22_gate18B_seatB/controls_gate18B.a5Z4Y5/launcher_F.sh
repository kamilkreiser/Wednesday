#!/bin/bash
# launch_qa_secuura_batch1170-1179.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate over SEVEN Secuura/Blockchain PRs (Seat B
# 18th; eight local-model READY rows applied STRICT and grouped by TICKET = by FILE into seven PRs across FOUR lanes — originate jest,
# anchoring `vitest run`, auth vitest, packages/shared `vitest run` — NINE paths, ZERO overlap, ONE product change (documents.ts +8/-0 on
# #1174); TIER 1 on #1174 (product bytes, the code_patch RED/GREEN protocol) + #1177 / #1178 (auth-surface pins); TIER 2 on the rest)
#   #1170 PR 1 KS-1118 F3b @ 3e9f7d7b7  COMMENT ks1103-verify-hash-field.test.ts +7/-2 — TIER 2
#   #1172 PR 2 KS-1158 R5b @ d74b04678  COMMENT ks1058-anchor-failed-preserves-thread-token.test.ts +1/-1 — TIER 2
#   #1174 PR 3 KS-1265 EARLYGUARD @ e1dea649c  CODE_PATCH ks549-documents-create-issuer-name-persist.test.ts + documents.ts +12/-7 — TIER 1
#   #1176 PR 4 KS-1171 8J-TSFIX GUARD3S-TSFIX @ 8ced0d50b  TEST_ONLY ks1171-8j-confirmed-wins-over-polled-zero.test.ts + ks1171-guard-3-s-re-poll-reads.test.ts +234/-0 — TIER 2
#   #1177 PR 5 KS-811 F7SETPIN @ 13030ac59  TEST_ONLY ks811-social-callback-403-code-set-agrees.test.ts +111/-0 — TIER 1
#   #1178 PR 6 KS-1188 MFASIBLINGS @ e48b90e74  TEST_ONLY ks1188-mfa-sibling-sites-503.test.ts +147/-0 — TIER 1
#   #1179 PR 7 KS-1181 F3w @ e62555dd0  COMMENT ks727-errorhandler-class-guard.test.ts +1/-1 — TIER 2
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 3916eacd1: each head's parent IS that
# commit) by pure tree hashing; the all-7 tree over the parent (a36532029483…) by REAL strict applies in three orders AND real 3-way merges of
# the heads in four orders in a --shared scratch clone under a cwd guard (predict_batch_scratch_*.out) AND by tree hashing; the all-7 tree over
# the CURRENT develop 8c2f7b3fd (the END_TREE) the same three ways; every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets18.py wants exactly ONE equality target PER PR FILE (1/1/2/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` — the TWO-file lines (#1174: documents.ts + its test; #1176: two anchoring files) carry TWO targets COMMA-separated (the
# COMMA-separated form is EXERCISED); merge18.py asserts each squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All seven tickets stay where they are (In Progress; three bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 3916eacd1 (tree 4b573853be61, the seat's item-0 tip);
# ORIGIN DEVELOP: the pin is 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 (tree 04b05e093ad8) — ONE squash AHEAD of the parent (the #1036 KS-763 lock family, 50 manifest paths,
# ∩ the 9 targets + 4 tamper files = ∅ — MEASURED; behind 1 at generation); the compare per PR reads develop...head = merge_base
# 3916eacd1, ahead 1, BEHIND 1, files 1/1/2/2/1/1/1 (exit 10 — a FURTHER develop move (Seat C 18th's six merges) changes `behind` and
# REFUSES: re-pin deliberately). ALL SEVEN over the parent = a36532029483c3f8a4ca0cd33ec1219076ef9219; ALL SEVEN over the current develop =
# 76a88d9ddfa4f50098aa639a1056c5c9387aeb18 (the END STATE if every merge lands on 8c2f7b3fd — the END_TREE the GO carries).
#
# The develop pin is judged by CONTENT — the 9 target paths at the CURRENT develop (four NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the five MODIFY targets by blob, exit 19 if at a head blob) plus 29 unchanged-read
# paths (this round's 4 tamper files, the hook, preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts, proxy.ts,
# documentRepo.ts, the ks795 / threadTokenMint / ks1004 / ks1188-mfa-status / ks949 / ks1181 test files, the lanes' unmoved package.json /
# config / tsconfig, eslint.config.mjs) plus 8 MOVED manifests judged at develop's post-#1036 blobs (shared + auth package.json, the four
# lanes' package-lock.json, the Dev root lock, audit-baseline.json). GUARDED on a further move: shared / originate / security /
# anchoring / auth src + config, packages/shared, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs (api-gateway — Seat C's
# lane — is NOT guarded: a Seat C merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate18B_seatB/mail_gate18B_ready.md, the seat's seven READY mails (00:02:34Z … 01:05:17Z) + its 23:47:45Z and
# 01:08:36Z STATUS mails (the HOLD) + its two QUESTION mails, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (#1170 T2, #1172 T2, #1174 T1, #1176 T2, #1177 T1, #1178 T1, #1179 T2).
# exit 10: the compare per PR (merge_base 3916eacd1, ahead 1, behind 1, files per PR) — a further develop move refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1147-#1161), the EARLIER REPORT (#1148-#1166), the OLDER REPORT
#          (the #1036 gate) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets18.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b18-*, s-c18-*) and writing in the seat 2026-09-22_seatB-18th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the all-7
#          tree, the octopus, the nine head blobs, the eight canonical sha16s, the suite counts, the A4 / A5 protocol, the lock words, the
#          attributions, the archived / content keys, the GO string), and the prompt must ask the gate to MEASURE, not conclude, and to RULE
#          WHETHER IT BLOCKS.
# exit 31: the prompt must name the END_TREE and the parent-based tree in full, the parent and the current develop in full, the NOT-PINNED
#          section and a loopback GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #1170 is KS-1118. … ).
# exit 33: the prompt must carry Wednesday TWELVE BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# QAB1170_CUR_DEV (test override, --check only): stands in for origin develop. QAB1170_HEAD_1179 (test override): stands in for #1179 pinned head.
# QAB1170_BRIEF / QAB1170_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1170_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate18B_seatB/gen_launcher_gate18B.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate16B.py.
#
# Usage: launch_qa_secuura_batch1170-1179.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1170_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB/mail_gate18B_ready.md}"
PROMPT_FILE="${QAB1170_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1170-1179.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1170|KS-1118|refs/heads/feature/ks-1118-post-apiverificationverify-the-documenthash-over-hash-r18-f3b-1|3e9f7d7b707da88e666ff94c769658f2ba3894b8|1"
  "1172|KS-1158|refs/heads/feature/ks-1158-l3a-gate-records-912-r2-937-the-placeholder-hash-anchoredat-r18-r5b-1|d74b04678574f5cb7828a82f84577882a3496a66|1"
  "1174|KS-1265|refs/heads/feature/ks-1265-post-apidocuments-saves-the-document-and-its-provenance-row-r16-earlyguard-1|e1dea649c7e338ba70a67acd8ce2957edd8058c9|2"
  "1176|KS-1171|refs/heads/feature/ks-1171-guard-3s-re-poll-reads-a-mixed-window-as-absent-one-early-r16-8j-tsfix-guard3s-tsfix-1|8ced0d50bb457d04b186b58a504e69b28052afb5|2"
  "1177|KS-811|refs/heads/feature/ks-811-nothing-asserts-815s-403-code-set-against-what-the-route-r16-f7setpin-1|13030ac59743c0df869bcf56ae10311445ae94d7|1"
  "1178|KS-1188|refs/heads/feature/ks-1188-1013-gate-findings-the-getuserbyid-route-level-503-r16-mfasiblings-1|e48b90e747def96b708f02890d2aa66ce10e52c0|1"
  "1179|KS-1181|refs/heads/feature/ks-1181-error-handler-guard-corpus-1-canary-cells-cannot-r18-f3w-1|${QAB1170_HEAD_1179:-e62555dd00eb2cdfa8d73c0f9329f4ac467ffa0c}|1"
)
DEVELOP_SHA='8c2f7b3fd4fde915b2a24542bc32259b24e092a0'   # the pin = origin develop at generation (ONE squash ahead of the heads' parent; a further move refuses at exit 10 / 18)
MERGE_BASE='3916eacd12af23bfd464440b4c770f7da0f2dd96'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='76a88d9ddfa4f50098aa639a1056c5c9387aeb18'     # all seven over the CURRENT develop (real 3-way merges four orders + strict applies three orders; generator tree-hash) — the END_TREE
ALL_OVER_PARENT='a36532029483c3f8a4ca0cd33ec1219076ef9219'   # all seven over the parent 3916eacd1 (the seat's item 0 + octopus 5185c65cf; three + four orders)
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1170-1179-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1147-1161-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1148-1166-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-ks763-1036-4b251997a-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18B_seatB/mail_gate18B_ready.md"

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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 3916eacd1, ahead 1, behind 1,
# files per PR (generator, rev-list --left-right; the launcher reads the compare API). A further develop move -> exit 10.
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
WANT_COMPARE="1170 $MERGE_BASE ahead=1 behind=1 files=1
1172 $MERGE_BASE ahead=1 behind=2 files=1
1174 $MERGE_BASE ahead=1 behind=1 files=2
1176 $MERGE_BASE ahead=1 behind=1 files=2
1177 $MERGE_BASE ahead=1 behind=1 files=1
1178 $MERGE_BASE ahead=1 behind=1 files=1
1179 $MERGE_BASE ahead=1 behind=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB (or ABSENT) at the CURRENT develop (no region judgement), then — if
# develop moved further — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1170_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
AU = D + "services/auth/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
JUDGED = {
  "Blockchain/Dev/services/originate/src/__tests__/ks1103-verify-hash-field.test.ts":                                    ({"ac76fc1da6861c9c8e3a76c17035c3c5c7791346": DV}, {"58eefc2aecd2fa274be2f2d916d5a6f7ab68aa2f": "#1170 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1058-anchor-failed-preserves-thread-token.test.ts":                 ({"1c78b4a618d1ae5ffaab03ccb40bb27df0d22e70": DV}, {"0a9573c19f3c89c5973ca4fec6efb4110ba4231e": "#1172 own"}),
  "Blockchain/Dev/services/originate/src/__tests__/ks549-documents-create-issuer-name-persist.test.ts":                  ({"62c767fccf5525ed67316500803b1163eeb547b9": DV}, {"d32b112102fdf39a9d82cbb3b6a0f1ea6236a304": "#1174 own"}),
  "Blockchain/Dev/services/originate/src/routes/documents.ts":                                                           ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {"1089377e11466bd847cb13420f8129aa7737a1ef": "#1174 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts":                   ({"ABSENT": DV}, {"c0c345bd0aae0d01c825cac91819db2870e53b9f": "#1176 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts":                              ({"ABSENT": DV}, {"a7d2c4bb37996e452bfd62b5952b191cc73c5946": "#1176 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks811-social-callback-403-code-set-agrees.test.ts":                        ({"ABSENT": DV}, {"b6fbff22e99ca13930608f87ea70829e3c5f07f8": "#1177 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-sibling-sites-503.test.ts":                                     ({"ABSENT": DV}, {"3e9b78aeaf5b5c7e28e88577e0d0ddab5cd739fd": "#1178 own"}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts":                                 ({"5127297156ed9b970ad17e804b3e3211894b6f8c": DV}, {"35eb27404fd615886d3f03ba7e691be97051f1ee": "#1179 own"}),
  "Blockchain/Dev/services/anchoring/src/anchorSubmission.ts":                                                           ({"d3ad106d8e5764a526456b3218e1e8d9ad1a38ba": DV}, {}),
  "Blockchain/Dev/services/auth/src/auth.openapi.ts":                                                                    ({"2c356c3c7877add99f5e1a3c437d04ac8be3dc76": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/auth.ts":                                                                     ({"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/mfa.ts":                                                                      ({"87d3ee1079fe90010f45955dbaf4307ae595b205": DV}, {}),
  ".githooks/pre-push":                                                                                                  ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                                       ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                          ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/fix-libsodium-symlink.js":                                                                     ({"526e024c2c107bb46ec9328c7de6687d4b8b7367": DV}, {}),
  "Blockchain/Dev/services/auth/src/services/jwt.ts":                                                                    ({"26562a22470af688ae733000792a2b0321650145": DV}, {}),
  "Blockchain/Dev/services/originate/src/services/provenance.ts":                                                        ({"483aa9eb331d2caa5af285e20d9668a9dbcd92a6": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts":                                                             ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  "Blockchain/Dev/services/originate/src/repositories/documentRepo.ts":                                                  ({"6e059d36c50a82016faca14111c28ec35bc4f237": DV}, {}),
  "Blockchain/Dev/services/auth/src/__tests__/ks795-social-link-verified-email.test.ts":                                 ({"a1c65ccd4c09da2861ef495c5ca6633e0989b9bb": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/threadTokenMint.test.ts":                                             ({"b88b3a43ec5dcb8651b91d5df90e9dec42a1795f": DV}, {}),
  "Blockchain/Dev/services/originate/src/__tests__/ks1004-anchor-failed-lockout.test.ts":                                ({"4684fb3ad2fa925ff654cf274aad6849b914d0d5": DV}, {}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts":                                      ({"5213553cca6ad057bee0e7d2fc5888f15ebd07eb": DV}, {}),
  "Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts":                               ({"4f03e6f4f132bc7a8f3c3577684f6eef3bf8ce03": DV}, {}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks1181-ks-727-error-handler-guard-corpus.test.ts":                       ({"cab04d1ae61d31c18bbdf856567b92935b84cfca": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/services/originate/package.json":                                                                      ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  "Blockchain/Dev/services/originate/tsconfig.json":                                                                     ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  "Blockchain/Dev/services/originate/jest.config.js":                                                                    ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  "Blockchain/Dev/services/anchoring/package.json":                                                                      ({"a7eed73550b40aa2d968872817fa22e933373831": DV}, {}),
  "Blockchain/Dev/services/anchoring/vitest.config.ts":                                                                  ({"2e1d21f130f8aa80a1c71987f920181dafaf6b90": DV}, {}),
  "Blockchain/Dev/services/anchoring/tsconfig.json":                                                                     ({"f593300cac7c9c3073f15a1287323cf5b9dd478d": DV}, {}),
  "Blockchain/Dev/services/auth/vitest.config.ts":                                                                       ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": DV}, {}),
  "Blockchain/Dev/services/auth/tsconfig.json":                                                                          ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                                                    ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"4a4a58de3c79b2f33f335a0fbf845781a2fde127": DV}, {}),
  "Blockchain/Dev/packages/shared/package-lock.json":                                                                    ({"77b5dba5ac05a23c28927f5742929d0f18227902": DV}, {}),
  "Blockchain/Dev/services/auth/package.json":                                                                           ({"66edc57735a8d43c0e682118da4a212d29d287f5": DV}, {}),
  "Blockchain/Dev/services/auth/package-lock.json":                                                                      ({"a9f32ff8814343219ff65677dd2cba00e6787d27": DV}, {}),
  "Blockchain/Dev/services/anchoring/package-lock.json":                                                                 ({"d77ac9080f591c30a840b4abdd21f3019a308d2a": DV}, {}),
  "Blockchain/Dev/services/originate/package-lock.json":                                                                 ({"c1033c41a6e9fb2938542e01beab0fc17028431f": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                                                    ({"54ba290e54f77725d4f757e974d51eeb3564400f": DV}, {}),
  "Blockchain/Dev/scripts/audit/audit-baseline.json":                                                                    ({"648e8ee7bbf22b5737597e3dd61ee92922628e58": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent + the #1036 squash; behind 1; all seven together " + all_over_dev + " over it, four + three orders, generator tree-hash + scratch-clone merges; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "package-lock.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           OR + "src/", OR + "package.json", OR + "jest.config.js", OR + "tsconfig.json", OR + "package-lock.json",
           SE + "src/", SE + "package.json", SE + "vitest.config.ts", SE + "tsconfig.json", SE + "package-lock.json",
           AN + "src/", AN + "package.json", AN + "vitest.config.ts", AN + "tsconfig.json", AN + "package-lock.json",
           AU + "src/", AU + "package.json", AU + "vitest.config.ts", AU + "tsconfig.json", AU + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the seven-PR tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate18B.py + fill_prompt_gate18B.py + gen_launcher_gate18B.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 2 floor' "$PROMPT_FILE" && grep -qF '#1170 KS-1118: TIER 2' "$PROMPT_FILE" && grep -qF '#1172 KS-1158: TIER 2' "$PROMPT_FILE" && grep -qF '#1174 KS-1265: TIER 1' "$PROMPT_FILE" && grep -qF '#1176 KS-1171: TIER 2' "$PROMPT_FILE" && grep -qF '#1177 KS-811: TIER 1' "$PROMPT_FILE" && grep -qF '#1178 KS-1188: TIER 1' "$PROMPT_FILE" && grep -qF '#1179 KS-1181: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 2 floor and each PR own tier line (#1170 T2, #1172 T2, #1174 T1, #1176 T2, #1177 T1, #1178 T1, #1179 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1170-#1179 (seven PRs; tier 1 = #1174, #1177, #1178: Seat B 18th, one product change)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SEVEN verdict lines one per PR" >&2; exit 23; }
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
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b18-batch' "$PROMPT_FILE" && grep -qF 's-c18-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatB-18th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b18-*, s-c18-*) and writing in the seat 2026-09-22_seatB-18th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          a36532029483 \
          5185c65cf \
          3916eacd1 \
          8c2f7b3fd \
          4b573853be61 \
          'GO: merge #1170, #1172, #1174, #1176, #1177, #1178, #1179 batch' \
          .push-lock-18 \
          s-b18-batch \
          93d471282177 \
          25f2d6767be9 \
          d8a095b55198 \
          96b4b7c9a42b \
          b7fd625c7c73 \
          d081ff92369d \
          560e6992e4da \
          58eefc2aecd2 \
          0a9573c19f3c \
          d32b112102fd \
          1089377e1146 \
          c0c345bd0aae \
          a7d2c4bb3799 \
          b6fbff22e99c \
          3e9b78aeaf5b \
          35eb27404fd6 \
          d0b78a1ab0fa2bcc \
          1fb99c3994dc07e9 \
          375f588f53cfea3e \
          0dc85536c0fe8565 \
          b1d9f5127e3b210f \
          03a43332e63fbc36 \
          153d942ec3df0ece \
          00c50c7ad6828df2 \
          d628409f8774aaf2 \
          d955f73e1c5d70c3 \
          835/835 \
          334/335 \
          828/828 \
          917/917 \
          824/824 \
          822/822 \
          818/818 \
          14/14 \
          6/6 \
          103/103 \
          +513/ \
          329 \
          '71 files' \
          '74 files' \
          '46 files' \
          '22 files' \
          threadTokenMint \
          TS1378 \
          strict \
          A4 \
          A5 \
          '1 failed / 4 run' \
          4/4 \
          section_1 \
          section_2 \
          +8/-0 \
          documents.ts \
          E-01 \
          issuerName \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          '45 passed, 0 failed (of 45)' \
          PROTOCOL-CLEAN \
          TEST-FILE-ONLY \
          COMMENT-ONLY \
          CODE_PATCH \
          typecheck \
          TS2322 \
          'STOP-class 0' \
          netlog \
          :5432 \
          anchoring:4005 \
          203.0.113.7:443 \
          ks914-pinned-address \
          'LANE COUNTS' \
          bare \
          preload \
          started_utc \
          'lock released' \
          attachmentsForURL \
          contributes \
          'linear[bot]' \
          ks795 \
          'nothing matched by identity' \
          SPECRENAME \
          ROUTECOLLAPSE \
          F1C \
          F1D \
          8J \
          :260 \
          :2097 \
          :1081 \
          :166 \
          :396 \
          anchors18.json \
          whole-line \
          ks-999 \
          ks-727 \
          Q6 \
          'Seat C 18th' \
          QUARANTINE \
          covermisread \
          go18.sh \
          targets18.py \
          merge18.py \
          dry18.sh \
          END_TREE \
          BASE_GO \
          KS-947 \
          '#1167' \
          KS-1123 \
          '#1168' \
          KS-1192 \
          '#1169' \
          KS-1231 \
          '#1171' \
          KS-1246 \
          '#1173' \
          KS-1257 \
          '#1175' \
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
          KS-549 \
          KS-733 \
          KS-815 \
          KS-1013 \
          KS-1058 \
          KS-1103 \
          KS-999 \
          KS-1230 \
          KS-871 \
          KS-763 \
          KS-775 \
          KS-1285 \
          KS-1227 \
          'Refs KS-1118' \
          'Refs KS-1158' \
          'Refs KS-1265' \
          'Refs KS-1171' \
          'Refs KS-811' \
          'Refs KS-1188' \
          'Refs KS-1181'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the END_TREE and the parent-based tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1170 is KS-1118.' "$PROMPT_FILE" && grep -F '#1170' "$BRIEF" | grep -qF 'KS-1118' && grep -qF 'PR #1172 is KS-1158.' "$PROMPT_FILE" && grep -F '#1172' "$BRIEF" | grep -qF 'KS-1158' && grep -qF 'PR #1174 is KS-1265.' "$PROMPT_FILE" && grep -F '#1174' "$BRIEF" | grep -qF 'KS-1265' && grep -qF 'PR #1176 is KS-1171.' "$PROMPT_FILE" && grep -F '#1176' "$BRIEF" | grep -qF 'KS-1171' && grep -qF 'PR #1177 is KS-811.' "$PROMPT_FILE" && grep -F '#1177' "$BRIEF" | grep -qF 'KS-811' && grep -qF 'PR #1178 is KS-1188.' "$PROMPT_FILE" && grep -F '#1178' "$BRIEF" | grep -qF 'KS-1188' && grep -qF 'PR #1179 is KS-1181.' "$PROMPT_FILE" && grep -F '#1179' "$BRIEF" | grep -qF 'KS-1181' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1170 is KS-1118. … )" >&2; exit 32; }
grep -qF -- 'TIER AND ROUND' "$PROMPT_FILE" && grep -qF -- 'Round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'outside __tests__: []' "$PROMPT_FILE" && grep -qF -- 'files API union 9' "$PROMPT_FILE" && grep -qF -- 'Any product byte anywhere else' "$PROMPT_FILE" && grep -qF -- 'STATE WHICH by the files' "$PROMPT_FILE" && grep -qF -- 'the FULL weight incl. the code_patch RED/GREEN' "$PROMPT_FILE" && grep -qF -- 'TEST-FILE-ONLY / COMMENT-ONLY exactly as declared' "$PROMPT_FILE" && grep -qF -- 'THE COMMENT-ONLY PROOF' "$PROMPT_FILE" && grep -qF -- 'name-status M / M / M+M / A+A / A / A /' "$PROMPT_FILE" && grep -qF -- 're-measure, do not copy' "$PROMPT_FILE" && grep -qF -- 'THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'SEVEN' "$PROMPT_FILE" && grep -qF -- 'ZERO overlap' "$PROMPT_FILE" && grep -qF -- 'at least forward, exact reverse and one shuffle' "$PROMPT_FILE" && grep -qF -- 'read-tree back to' "$PROMPT_FILE" && grep -qF -- 'state the SET you read and WHEN' "$PROMPT_FILE" && grep -qF -- 'the #1036 move ∩ the 9 PR paths = ∅ AND ∩ the 4 tamper files = ∅' "$PROMPT_FILE" && grep -qF -- 'THE END_TREE the GO' "$PROMPT_FILE" && grep -qF -- 'EXACTLY the 50 paths' "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY, STRICT' "$PROMPT_FILE" && grep -qF -- '`--recount` a NO-OP on every one' "$PROMPT_FILE" && grep -qF -- 'cat(section_1.diff, section_2.diff) == patch.diff' "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'No `--recount`' "$PROMPT_FILE" && grep -qF -- 'THE CELLS: test_only rows' "$PROMPT_FILE" && grep -qF -- 'every declared cell + control present BY TITLE' "$PROMPT_FILE" && grep -qF -- 'reds EXACTLY the declared set' "$PROMPT_FILE" && grep -qF -- 'tamper files restored by bytes' "$PROMPT_FILE" && grep -qF -- 'the RED/GREEN protocol:' "$PROMPT_FILE" && grep -qF -- 'head-minus-product' "$PROMPT_FILE" && grep -qF -- 'A4 red set (1/4' "$PROMPT_FILE" && grep -qF -- 'A5 4/4 green' "$PROMPT_FILE" && grep -qF -- 'BOTH stated' "$PROMPT_FILE" && grep -qF -- 'the NEW baseline over the' "$PROMPT_FILE" && grep -qF -- 'PER-FILE TYPECHECK DELTA 0' "$PROMPT_FILE" && grep -qF -- 'planted' "$PROMPT_FILE" && grep -qF -- 'TS2322 control CAUGHT' "$PROMPT_FILE" && grep -qF -- 'a zero that needs its control' "$PROMPT_FILE" && grep -qF -- 'TS1378' "$PROMPT_FILE" && grep -qF -- 'AND on `documents.ts`' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE v2 on the FOUR lanes' "$PROMPT_FILE" && grep -qF -- 'zero :5432' "$PROMPT_FILE" && grep -qF -- 'unestablished EXTERNAL attempts REPORTED by NAME' "$PROMPT_FILE" && grep -qF -- '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before' "$PROMPT_FILE" && grep -qF -- 'login_stub cleared by' "$PROMPT_FILE" && grep -qF -- 'census STOP-class 0' "$PROMPT_FILE" && grep -qF -- 're-measured on' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'Backlog -> In Progress walks' "$PROMPT_FILE" && grep -qF -- 'the ONE tolerated state change' "$PROMPT_FILE" && grep -qF -- 'no archived key in any branch' "$PROMPT_FILE" && grep -qF -- 'Recommend nothing' "$PROMPT_FILE" && grep -qF -- 'hyphenated-key scanner' "$PROMPT_FILE" && grep -qF -- 'KS-1171 is PR 4' "$PROMPT_FILE" && grep -qF -- 'no em-dash' "$PROMPT_FILE" && grep -qF -- 'THE TWO-SEAT ARTEFACTS' "$PROMPT_FILE" && grep -qF -- 'every push INSIDE the push-window lock' "$PROMPT_FILE" && grep -qF -- 'grade present / absent + MONOTONIC' "$PROMPT_FILE" && grep -qF -- 'ATTRIBUTION BY NAME of Seat C 18th' "$PROMPT_FILE" && grep -qF -- 'four conditions' "$PROMPT_FILE" && grep -qF -- 'the ONLY tolerated state change' "$PROMPT_FILE" && grep -qF -- 'THE PROCESS-NAMESPACE RULE' "$PROMPT_FILE" && grep -qF -- 'measure18.py has NO cwd guard' "$PROMPT_FILE" && grep -qF -- 'count-objects before / after' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S OWN FINDINGS / SLIPS" "$PROMPT_FILE" && grep -qF -- 'CONFIRMED / REFUTED' "$PROMPT_FILE" && grep -qF -- 'F9 the two cover-pass misreads' "$PROMPT_FILE" && grep -qF -- 'S6 the ks811 cover title' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- 'KNOWN intermittent, NAMED' "$PROMPT_FILE" && grep -qF -- 'PRELOAD TIMING ARTEFACT' "$PROMPT_FILE" && grep -qF -- 're-run standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM — SEVEN lines VERBATIM' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER' "$PROMPT_FILE" && grep -qF -- 'MERGED-tree reading' "$PROMPT_FILE" && grep -qF -- 'stays In Progress' "$PROMPT_FILE" && grep -qF -- 'SHIPS-WITH text ≤ 3 sentences each and KEY-FREE' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED rows NAMED' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED for its own file' "$PROMPT_FILE" && grep -qF -- 'READ THE WHOLE TEST FILE before proposing a cell' "$PROMPT_FILE" && grep -qF -- 'sha256 + byte count IN the mail' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED written FIRST' "$PROMPT_FILE" && grep -qF -- 'THE CONTEXT RULE' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" && grep -qF -- 'NAMESPACE GUARD' "$PROMPT_FILE" && grep -qF -- 'SEVEN lines, one per PR' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'node_modules per ENTRY' "$PROMPT_FILE" && grep -qF -- 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF -- 'no memory maintenance' "$PROMPT_FILE" && grep -qF -- 'NEVER print a credential value' "$PROMPT_FILE" && grep -qF -- 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" && grep -qF -- 'NEVER touch the' "$PROMPT_FILE" && grep -qF -- 'by ANCESTRY' "$PROMPT_FILE" && grep -qF -- 'never by a basename' "$PROMPT_FILE" && grep -qF -- 'BASE_GO = ' "$PROMPT_FILE" && grep -qF -- 'END_TREE = ' "$PROMPT_FILE" && grep -qF -- 'at ctx 80 write report.md' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; test-file-only / comment-only; the trees over both bases and the #1036 intersection; canonical identity strict; the cells with the red/green protocol; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries the TIER 2 floor and each PR tier (#1170 T2, #1172 T2, #1174 T1, #1176 T2, #1177 T1, #1178 T1, #1179 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1147-#1161 PRIOR REPORT, the #1148-#1166 EARLIER REPORT, the #1036 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b18-*, s-c18-*) and the seat 2026-09-22_seatB-18th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (174 tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the END_TREE and the parent-based tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (122 keywords)"
  [ -n "${QAB1170_CUR_DEV:-}" ] && echo "  (develop read from the QAB1170_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1170_BRIEF:-}${QAB1170_PROMPT:-}${QAB1170_HEAD_1179:-}${QAB1170_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
