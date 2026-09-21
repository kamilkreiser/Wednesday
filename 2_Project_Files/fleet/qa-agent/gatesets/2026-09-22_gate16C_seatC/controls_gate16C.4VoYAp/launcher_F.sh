#!/bin/bash
# launch_qa_secuura_batch1148-1166.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 2 floor (TIER 1 on the six auth pins
# #1158 #1160 #1162 #1163 #1164 #1165) over TWELVE Secuura/Blockchain PRs (Seat C 16th; fifteen local-model R15 TEST-ONLY READYs — fourteen run patches applied
# --recount + KS-910's two checker section files applied strict — grouped by TICKET = by FILE into twelve PRs across THREE lanes — api-gateway
# vitest, auth vitest, scripts bash — SIXTEEN paths, ZERO overlap, ZERO product bytes; the seat's PR 2 KS-1123 F3b HELD un-pushed, NOT here)
#   #1148 PR 1 KS-864 F1009b @ c4a96cfe0  TEST-ONLY ks864c-portal-env-vars.test.ts +16/-2 — TIER 2
#   #1150 PR 3 KS-1180 P1P2P4 @ 250a9b9ed  TEST-ONLY ks1073-tier-2-verify-has-no-statusless.test.ts +26/-4 — TIER 2
#   #1152 PR 4 KS-1185 F4 @ 28d1e4df6  TEST-ONLY ks1185-workflow-approve-forward-default-bound.test.ts +108/-0 — TIER 2
#   #1154 PR 5 KS-1199 R15 @ 889b05391  TEST-ONLY ks1199-status-differing-anchor-tie-verdict.test.ts +113/-0 — TIER 2
#   #1156 PR 6 KS-1237 ARRAYLIKE @ 58d293a87  TEST-ONLY ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts +8/-1 — TIER 2
#   #1158 PR 7 KS-855 SCOPETABLE @ ddac6d7d5  TEST-ONLY ks855-the-oauth-available-scopes-list-is.test.ts +82/-0 — TIER 1
#   #1160 PR 8 KS-944 SPECPIN @ ef4713cc6  TEST-ONLY ks944-the-gateway-s-auth-gate-reads.test.ts +57/-0 — TIER 1
#   #1162 PR 9 KS-1156 R15 @ b6b70d787  TEST-ONLY ks1156-auth4-gate-records-983-r2-984.test.ts +111/-0 — TIER 1
#   #1163 PR 10 KS-1188 F1a F1b F2 @ 02f12926f  TEST-ONLY ks1188-mfa-status-503-route.test.ts + ks1188-users-me-503-route.test.ts + ks1188-getuserbyid-failed-log-meta-keys.test.ts +402/-0 — TIER 1
#   #1164 PR 11 KS-1193 F1 F2 @ ba730c6ac  TEST-ONLY ks1193-verification-reads-codeless-pool-timeout.test.ts + ks1193-review-read-query-error-is-not-503.test.ts +270/-0 — TIER 1
#   #1165 PR 12 KS-1217 TESTPINFULLMESSAGE @ 4ecb09cf2  TEST-ONLY ks1050-profile-update-zero-rows-is-not-success.test.ts +2/-1 — TIER 1
#   #1166 PR 13 KS-910 LEGCOMMENT @ a08741f51  TEST-ONLY pre_push_hook_base.test.sh + pre_push_hook_base_leg_comment.test.sh +61/-3 — TIER 2
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 64ab10513: each head's parent IS that
# commit) by pure tree hashing; the twelve-PR tree over the parent (4817a9c2ea23…) by REAL applies in three orders AND real 3-way merges of
# the heads in four orders in a --shared scratch clone (predict_batch_scratch_*.out) AND by tree hashing; every BOTH-list token asserted present in
# the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets17.py wants exactly ONE equality target PER PR FILE (1/1/1/1/1/1/1/1/3/2/1/2 = SIXTEEN) and parses the
# list non-greedily to the FIRST `;` — three multi-file lines this round (#1163 three, #1164 two, #1166 two: the COMMA-separated MG-2 form is
# EXERCISED); merge17.py asserts each squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. TWELVE verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All twelve tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 64ab10513 (tree 87b4aa12d2eb, Seat B 15th's final state +
# Peter's #1138). ORIGIN DEVELOP: the pin is 64ab105132eada0621622acf4d6053bc59926780 (tree 87b4aa12d2eb) — UNMOVED since the raise at generation (behind 0); the
# compare per PR reads develop...head = merge_base 64ab10513, ahead 1, BEHIND 0, files 1/1/1/1/1/1/1/1/3/2/1/2 (exit 10 — a develop move
# changes `behind` and REFUSES: re-pin deliberately — Seat B 16th's GO may land its merges first). ALL TWELVE over the parent = 4817a9c2ea2334b89395c4faa588312cfd609550;
# ALL TWELVE over the current develop = 4817a9c2ea2334b89395c4faa588312cfd609550 (the END STATE if every merge lands on 64ab10513).
#
# The develop pin is judged by CONTENT — the 16 target paths at the CURRENT develop (eleven NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the five MODIFIED files by blob) plus 38 unchanged-read paths (this round's 8 tamper
# files, the 15th's five (users.ts in both), the hook, preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, jwt.ts, provenance.ts,
# proxy.ts, the ks949 / ks1072 / ks815 / ks1123-f2 / ks1123-f3 test files the census and the held PR's cover name, the two lanes' package.json /
# vitest.config.ts / tsconfig.json / lock, packages/shared's package.json / config, the Dev package.json + lock, eslint.config.mjs). GUARDED on a
# move: api-gateway / auth src + config, packages/shared, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs (originate /
# security / anchoring — Seat B's lanes — are NOT guarded: a Seat B merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate16C_seatC/mail_gate16C_ready.md, the seat's twelve READY mails (17:06:23Z … 19:08:40Z) + its 16:46:09Z, 16:51:50Z,
# 16:56:14Z and 19:12:28Z STATUS mails + its two QUESTION mails, each captured verbatim by message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 2 floor AND each PR own tier line (#1148 T2, #1150 T2, #1152 T2, #1154 T2, #1156 T2, #1158 T1, #1160 T1, #1162 T1, #1163 T1, #1164 T1, #1165 T1, #1166 T2).
# exit 10: the compare per PR (merge_base 64ab10513, ahead 1, behind 0, files 1/1/1/1/1/1/1/1/3/2/1/2) — develop moving refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and TWELVE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1136-#1146), the EARLIER REPORT (#1130-#1135), the OLDER REPORT
#          (#1119-#1128) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets17.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-c16-*, s-b16-*) and writing in the seat 2026-09-22_seatC-16th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 / :4005 / :6000 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the twelve-PR
#          tree, the thirteen-PR batch tree, the sixteen head blobs, the fourteen canonical sha16s + the two section sha16s + the fence sha16, the
#          three STRICT blobs, the five develop blobs, the suite counts, the --recount rcs, the lock words, the attributions, the S3 kill, the
#          archived / content keys, the GO string), and the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the twelve-PR tree in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #1148 is KS-864. … ).
# exit 33: the prompt must carry Wednesday TWELVE BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# QAB1148_CUR_DEV (test override, --check only): stands in for origin develop. QAB1148_HEAD_1166 (test override): stands in for #1166 pinned head.
# QAB1148_BRIEF / QAB1148_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1148_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate16C_seatC/gen_launcher_gate16C.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate16B.py / gen_launcher_gate15.py.
#
# Usage: launch_qa_secuura_batch1148-1166.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..34 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1148_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16C_seatC/mail_gate16C_ready.md}"
PROMPT_FILE="${QAB1148_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1148-1166.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1148|KS-864|refs/heads/feature/ks-864-dead-estate-pointers-in-runtime-source-outside-r15-f1009b-1|c4a96cfe012196aa56765b6b26bd63b123980087|1"
  "1150|KS-1180|refs/heads/feature/ks-1180-ks1073-verify-cells-the-tier-guard-is-not-a-tier-witness-the-r15-p1p2p4-1|250a9b9eda021cb2b3d224d68b9e3ca5e9264d2c|1"
  "1152|KS-1185|refs/heads/feature/ks-1185-gate-follow-ups-validate-the-approve-forward-timeout-r15-f4-1|28d1e4df6da993e0363537a5144185d0892e4ca3|1"
  "1154|KS-1199|refs/heads/feature/ks-1199-ks1072-verify-cells-pin-no-verdict-on-a-tie-whose-rows-r15-1|889b0539117b2f31e777f47adde1d8f06a5c5de7|1"
  "1156|KS-1237|refs/heads/feature/ks-1237-ks1204-cells-three-tampers-stay-green-the-array-like-allow-r15-arraylike-1|58d293a87706f58321c8266e4bfeebc2686471d9|1"
  "1158|KS-855|refs/heads/feature/ks-855-the-oauth-available_scopes-list-is-a-second-divergent-scope-r15-scopetable-1|ddac6d7d5fe3362d3e0ff9633628d8367fcc6310|1"
  "1160|KS-944|refs/heads/feature/ks-944-the-gateways-auth-gate-reads-the-specs-security-nothing-pins-r15-specpin-1|ef4713cc66c07b1b013cbd7d7ca0ea2fe5a4f5b2|1"
  "1162|KS-1156|refs/heads/feature/ks-1156-auth4-gate-records-983-r2-984-r2-986-987-h-limiter-r15-r15-1|b6b70d7870222cd746c8a9b98a423ef95a657568|1"
  "1163|KS-1188|refs/heads/feature/ks-1188-1013-gate-findings-the-getuserbyid-route-level-503-r15-f1a-f1b-f2-1|02f12926f248bcc879e1f437d51a306a829b3c8b|3"
  "1164|KS-1193|refs/heads/feature/ks-1193-1015-gate-findings-the-message-form-pool-timeout-the-r15-f1-f2-1|ba730c6ac4fee7c7994531b8e4b9b62fed297830|2"
  "1165|KS-1217|refs/heads/feature/ks-1217-ks1050-c1-pins-only-the-helper-message-prefix-plus-a-3-r15-testpinfullmessage-1|4ecb09cf2c1d623e59bf3ec03db262b1d6108f64|1"
  "1166|KS-910|refs/heads/feature/ks-910-preflight-leg-12-executes-zero-suite-cells-it-is-a-r15-legcomment-1|${QAB1148_HEAD_1166:-a08741f513510f979936ee2a0dcc48d270f21a65}|2"
)
DEVELOP_SHA='64ab105132eada0621622acf4d6053bc59926780'   # the pin = origin develop at generation (= the heads' parent; a move refuses at exit 10 / 18)
MERGE_BASE='64ab105132eada0621622acf4d6053bc59926780'    # every head's parent = the merge-base with the current develop
ALL_OVER_DEV='4817a9c2ea2334b89395c4faa588312cfd609550'     # all twelve over the CURRENT develop (real applies + 3-way merges; generator tree-hash) — the END STATE
ALL_OVER_PARENT='4817a9c2ea2334b89395c4faa588312cfd609550'   # all twelve over the parent 64ab10513 (the seat's measure17b.py; three + four orders)
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1148-1166-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1136-1146-tier2-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate16C_seatC/mail_gate16C_ready.md"

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
# files 1/1/1/1/1/1/1/1/3/2/1/2 (generator, rev-list --left-right; the launcher reads the compare API). A develop move -> exit 10.
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
WANT_COMPARE="1148 $MERGE_BASE ahead=1 behind=0 files=1
1150 $MERGE_BASE ahead=1 behind=1 files=1
1152 $MERGE_BASE ahead=1 behind=0 files=1
1154 $MERGE_BASE ahead=1 behind=0 files=1
1156 $MERGE_BASE ahead=1 behind=0 files=1
1158 $MERGE_BASE ahead=1 behind=0 files=1
1160 $MERGE_BASE ahead=1 behind=0 files=1
1162 $MERGE_BASE ahead=1 behind=0 files=1
1163 $MERGE_BASE ahead=1 behind=0 files=3
1164 $MERGE_BASE ahead=1 behind=0 files=2
1165 $MERGE_BASE ahead=1 behind=0 files=1
1166 $MERGE_BASE ahead=1 behind=0 files=2"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB (or ABSENT) at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1148_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
AG = D + "services/api-gateway/"
AU = D + "services/auth/"
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
JUDGED = {
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks864c-portal-env-vars.test.ts":                                    ({"f886bdadf7065b4a40d7d54b13fa3f70f9cc35cf": DV}, {"1cf9959146c097db35fdb20b0bac8246377194cd": "#1148 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1073-tier-2-verify-has-no-statusless.test.ts":                    ({"26f521ebd2e8aeb6d8884f4245e32235d9c8b1fc": DV}, {"6d28adb1f8ba31780fd35aa3ca4edbff7533ec4d": "#1150 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1185-workflow-approve-forward-default-bound.test.ts":             ({"ABSENT": DV}, {"e231e3eac8cb959876db2694aac8eaeb2a9677b1": "#1152 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1199-status-differing-anchor-tie-verdict.test.ts":                ({"ABSENT": DV}, {"374193ef56832779b8a8c5922412ad93b9d2cc04": "#1154 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1204-a-non-array-allow-list-fails-closed-and-documenttype-wins.test.ts": ({"f1f9840edd15ba8cbb764f675f5c2fdeef228dc7": DV}, {"6683a0c16446b5372ed2728d70e0e7723effd2ca": "#1156 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks855-the-oauth-available-scopes-list-is.test.ts":                         ({"ABSENT": DV}, {"6942187fc7730710b920d95cdb5b8662664e6d8f": "#1158 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks944-the-gateway-s-auth-gate-reads.test.ts":                              ({"ABSENT": DV}, {"5fca556553a626c9b96d49da02ac0ebd1cbfcecd": "#1160 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts":                             ({"ABSENT": DV}, {"56ef7e523469f3a0e63523f8af8fbc3d761b22da": "#1162 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1188-mfa-status-503-route.test.ts":                                      ({"ABSENT": DV}, {"5213553cca6ad057bee0e7d2fc5888f15ebd07eb": "#1163 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1188-users-me-503-route.test.ts":                                        ({"ABSENT": DV}, {"2cd754d9ba5629a46aea8b2b3ebc8491a88ce153": "#1163 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1188-getuserbyid-failed-log-meta-keys.test.ts":                          ({"ABSENT": DV}, {"cb0905a4d4e1ad3f7345d7f67471b9e91c3da791": "#1163 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1193-verification-reads-codeless-pool-timeout.test.ts":                  ({"ABSENT": DV}, {"42213aa17a54759d114e12193ebb498e7d8f9657": "#1164 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1193-review-read-query-error-is-not-503.test.ts":                        ({"ABSENT": DV}, {"862f7ea5cc053afa2b2fcfcfc9c64d68ff7cfc1c": "#1164 own"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1050-profile-update-zero-rows-is-not-success.test.ts":                   ({"ffb3e801ab371bed4a11accd0dbcc64bd8fdc804": DV}, {"80ddfb3f0fa712f42db71ec61908f94855e63732": "#1165 own"}),
  "Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh":                                                         ({"affdf027bff11e3690d374e902e3e93274788c62": DV}, {"e33da9a44e112c64bd887e7b434c9a39b0ecc7eb": "#1166 own"}),
  "Blockchain/Dev/scripts/__tests__/pre_push_hook_base_leg_comment.test.sh":                                             ({"ABSENT": DV}, {"a1598f1163d730e15951f2e3449d6a8ea7d55ceb": "#1166 own"}),
  "Blockchain/Dev/services/api-gateway/src/routes/system-status.ts":                                                     ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/verification.ts":                                                      ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  "Blockchain/Dev/services/auth/src/services/oauth.ts":                                                                  ({"8995edec6a43b7623def6c9d1b002ed0a1b0dc86": DV}, {}),
  "Blockchain/Dev/services/auth/src/auth.openapi.ts":                                                                    ({"2c356c3c7877add99f5e1a3c437d04ac8be3dc76": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/auth.ts":                                                                     ({"18946cd7c5c394d89ecbecf860ab66a96b1e22c7": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/mfa.ts":                                                                      ({"87d3ee1079fe90010f45955dbaf4307ae595b205": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/users.ts":                                                                    ({"3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d": DV}, {}),
  "Blockchain/Dev/services/auth/src/repositories/userRepo.ts":                                                           ({"9060b308e6d6a82c8a79be7387032d2a18c4ac22": DV}, {}),
  "Blockchain/Testing/jobs/04-container-trivy.sh":                                                                       ({"6dfc5731e56ede5e5a6f420cccd92874b7566a87": DV}, {}),
  "systemTest/fixtures/manifest.ts":                                                                                     ({"a6bfe3e7662791866e16c04331ba8fdc473a535a": DV}, {}),
  "Blockchain/Dev/services/security/src/index.ts":                                                                       ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  "Blockchain/Dev/scripts/check-shared-relink.sh":                                                                       ({"4e0704b6c7b9f4db2ceebf0530015e3b2f469662": DV}, {}),
  ".githooks/pre-push":                                                                                                  ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                                       ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                          ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/fix-libsodium-symlink.js":                                                                     ({"526e024c2c107bb46ec9328c7de6687d4b8b7367": DV}, {}),
  "Blockchain/Dev/services/auth/src/services/jwt.ts":                                                                    ({"26562a22470af688ae733000792a2b0321650145": DV}, {}),
  "Blockchain/Dev/services/originate/src/services/provenance.ts":                                                        ({"483aa9eb331d2caa5af285e20d9668a9dbcd92a6": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts":                                                             ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  "Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts":                               ({"4f03e6f4f132bc7a8f3c3577684f6eef3bf8ce03": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts":             ({"d9c98320ea64638c3ab5ef2f35c102aba6d1207a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts":             ({"83c3771c75e3d141a576eb21f787b7b816355931": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts":                  ({"afaa781d438bb350b7a33446fb41b528e3363077": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts":                       ({"8c413fba6dd2687f7f0a70f5460aa3560e13d45b": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                                                    ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                                                ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                                                   ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package-lock.json":                                                               ({"5ec55d86d83f93e70dc03676293331fd3bc250e5": DV}, {}),
  "Blockchain/Dev/services/auth/package.json":                                                                           ({"814e88419470b811f26f1593984071bb317608d8": DV}, {}),
  "Blockchain/Dev/services/auth/vitest.config.ts":                                                                       ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": DV}, {}),
  "Blockchain/Dev/services/auth/tsconfig.json":                                                                          ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": DV}, {}),
  "Blockchain/Dev/services/auth/package-lock.json":                                                                      ({"2d91a356aa8426304dc291e0090dbd6893d53c00": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent; behind 0; all twelve together " + all_over_dev + " over it, three + four orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           AG + "src/", AG + "package.json", AG + "vitest.config.ts", AG + "tsconfig.json", AG + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the twelve-PR tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate16C.py + gen_launcher_gate16C.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 2 floor' "$PROMPT_FILE" && grep -qF '#1148 KS-864: TIER 2' "$PROMPT_FILE" && grep -qF '#1150 KS-1180: TIER 2' "$PROMPT_FILE" && grep -qF '#1152 KS-1185: TIER 2' "$PROMPT_FILE" && grep -qF '#1154 KS-1199: TIER 2' "$PROMPT_FILE" && grep -qF '#1156 KS-1237: TIER 2' "$PROMPT_FILE" && grep -qF '#1158 KS-855: TIER 1' "$PROMPT_FILE" && grep -qF '#1160 KS-944: TIER 1' "$PROMPT_FILE" && grep -qF '#1162 KS-1156: TIER 1' "$PROMPT_FILE" && grep -qF '#1163 KS-1188: TIER 1' "$PROMPT_FILE" && grep -qF '#1164 KS-1193: TIER 1' "$PROMPT_FILE" && grep -qF '#1165 KS-1217: TIER 1' "$PROMPT_FILE" && grep -qF '#1166 KS-910: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 2 floor and each PR own tier line (#1148 T2, #1150 T2, #1152 T2, #1154 T2, #1156 T2, #1158 T1, #1160 T1, #1162 T1, #1163 T1, #1164 T1, #1165 T1, #1166 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1148-#1166 (twelve PRs; tier 2 floor, tier 1 = #1158, #1160, #1162, #1163, #1164, #1165: Seat C 16th test-only pins)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'TWELVE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and TWELVE verdict lines one per PR" >&2; exit 23; }
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
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-c16-batch' "$PROMPT_FILE" && grep -qF 's-b16-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatC-16th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-c16-*, s-b16-*) and writing in the seat 2026-09-22_seatC-16th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:6000 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          4817a9c2ea23 \
          48528fa3c355 \
          64ab105132eada0621622acf4d6053bc59926780 \
          64ab10513 \
          87b4aa12d2eb \
          b8335a32e \
          s-c16-ks1123 \
          HOLD-PR2-NOT-PUSHED-wednesday-answer.txt \
          'GO: merge #1148, #1150, #1152, #1154, #1156, #1158, #1160, #1162, #1163, #1164, #1165, #1166 batch' \
          631a38ab6d4b \
          bb7f9a2ac972 \
          1ffa57af71fb \
          f96a6cad291b \
          6bb07e098ae8 \
          6a1150f85f47 \
          a1541f731c60 \
          8f0a5145c5dd \
          41b33c17d906 \
          3759873dfbd5 \
          395e34b93d13 \
          fa1771ac07e5 \
          1cf9959146c0 \
          6d28adb1f8ba \
          e231e3eac8cb \
          374193ef5683 \
          6683a0c16446 \
          6942187fc773 \
          5fca556553a6 \
          56ef7e523469 \
          5213553cca6a \
          2cd754d9ba56 \
          cb0905a4d4e1 \
          42213aa17a54 \
          862f7ea5cc05 \
          80ddfb3f0fa7 \
          e33da9a44e11 \
          a1598f1163d7 \
          0f274204b12b5514 \
          6a7e9f26a05dd819 \
          f11b7d7af5e08411 \
          43dbab44c004f11d \
          5e5c810330cf04c9 \
          500f8ca4aa5ccc3e \
          25a6cc7721ccf6e2 \
          c6214df3bf4b6178 \
          1da74333f4903fbe \
          81ac27882e17b4e5 \
          10c953d4604b4618 \
          ffd0347dfac13ad8 \
          25df949c29a47684 \
          cdaf4d17e0308c8e \
          9d6dccc83f8020df \
          ebb9a15ecfa32f88 \
          b660b8c4b260f1f5 \
          4f68a823f31f \
          686a707056af \
          610c209861d1 \
          f886bdadf706 \
          26f521ebd2e8 \
          f1f9840edd15 \
          ffb3e801ab37 \
          affdf027bff1 \
          697/697 \
          786/786 \
          701/701 \
          699/699 \
          698/698 \
          790/790 \
          789/789 \
          801/801 \
          793/793 \
          716/716 \
          818/818 \
          '1256 insertions' \
          '+1471/-11' \
          'corrupt patch at line 10' \
          --recount \
          TRUNCATION \
          RECOUNT \
          strict \
          red-first \
          section_1.diff.reanchored \
          section_2.diff \
          'delta -1' \
          TS18046 \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          '44 passed, 0 failed (of 44)' \
          '45 passed, 0 failed (of 45)' \
          PROTOCOL-CLEAN \
          TEST-FILE-ONLY \
          typecheck17 \
          TS2322 \
          'STOP-class 0' \
          netlog.cjs \
          :5432 \
          anchoring:4005 \
          localhost:6000 \
          ks1072-the-latest-anchor-selector-docume \
          ks815-verification-router-guards-its-own \
          'LOCK TAKEN' \
          'LOCK RELEASED' \
          push-lock-16 \
          lock17.sh \
          push17.sh \
          series17.py \
          attributed \
          attrib_verify17.py \
          attachmentsForURL \
          contributes \
          'linear[bot]' \
          measure17b.json \
          F-45 \
          F-COVER-1123 \
          F-FALSECOVER-944 \
          'load intermittent' \
          5002-5266 \
          anchor-ambiguity \
          mfaRoutes.get \
          ks-1183 \
          ks-999 \
          ks-1018 \
          EXCISED \
          kksecura \
          Blockchain-B \
          'Seat B 16th' \
          57702 \
          53817 \
          ready_send17.sh \
          S3 \
          noclobber \
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
          KS-1031 \
          KS-1175 \
          KS-1250 \
          KS-1273 \
          KS-958 \
          KS-1123 \
          KS-1171 \
          'Refs KS-864' \
          'Refs KS-1180' \
          'Refs KS-1185' \
          'Refs KS-1199' \
          'Refs KS-1237' \
          'Refs KS-855' \
          'Refs KS-944' \
          'Refs KS-1156' \
          'Refs KS-1188' \
          'Refs KS-1193' \
          'Refs KS-1217' \
          'Refs KS-910'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the twelve-PR tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1148 is KS-864.' "$PROMPT_FILE" && grep -F '#1148' "$BRIEF" | grep -qF 'KS-864' && grep -qF 'PR #1150 is KS-1180.' "$PROMPT_FILE" && grep -F '#1150' "$BRIEF" | grep -qF 'KS-1180' && grep -qF 'PR #1152 is KS-1185.' "$PROMPT_FILE" && grep -F '#1152' "$BRIEF" | grep -qF 'KS-1185' && grep -qF 'PR #1154 is KS-1199.' "$PROMPT_FILE" && grep -F '#1154' "$BRIEF" | grep -qF 'KS-1199' && grep -qF 'PR #1156 is KS-1237.' "$PROMPT_FILE" && grep -F '#1156' "$BRIEF" | grep -qF 'KS-1237' && grep -qF 'PR #1158 is KS-855.' "$PROMPT_FILE" && grep -F '#1158' "$BRIEF" | grep -qF 'KS-855' && grep -qF 'PR #1160 is KS-944.' "$PROMPT_FILE" && grep -F '#1160' "$BRIEF" | grep -qF 'KS-944' && grep -qF 'PR #1162 is KS-1156.' "$PROMPT_FILE" && grep -F '#1162' "$BRIEF" | grep -qF 'KS-1156' && grep -qF 'PR #1163 is KS-1188.' "$PROMPT_FILE" && grep -F '#1163' "$BRIEF" | grep -qF 'KS-1188' && grep -qF 'PR #1164 is KS-1193.' "$PROMPT_FILE" && grep -F '#1164' "$BRIEF" | grep -qF 'KS-1193' && grep -qF 'PR #1165 is KS-1217.' "$PROMPT_FILE" && grep -F '#1165' "$BRIEF" | grep -qF 'KS-1217' && grep -qF 'PR #1166 is KS-910.' "$PROMPT_FILE" && grep -F '#1166' "$BRIEF" | grep -qF 'KS-910' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1148 is KS-864. … )" >&2; exit 32; }
grep -qF -- 'TIER AND ROUND' "$PROMPT_FILE" && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'outside __tests__: []' "$PROMPT_FILE" && grep -qF -- 'files API union 16' "$PROMPT_FILE" && grep -qF -- 'Any product byte' "$PROMPT_FILE" && grep -qF -- 'STATE WHICH by the files API' "$PROMPT_FILE" && grep -qF -- 'TEST-FILE-ONLY:' "$PROMPT_FILE" && grep -qF -- 'the test file(s) exactly' "$PROMPT_FILE" && grep -qF -- 'the RECOUNT column' "$PROMPT_FILE" && grep -qF -- 'name-status A ×11 / M ×5' "$PROMPT_FILE" && grep -qF -- 'THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'SIXTEEN' "$PROMPT_FILE" && grep -qF -- 'ZERO overlap' "$PROMPT_FILE" && grep -qF -- 'at least forward, exact reverse and one shuffle' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'state the SET you read and WHEN' "$PROMPT_FILE" && grep -qF -- "on exactly KS-1123's one file" "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY with the `--recount` class' "$PROMPT_FILE" && grep -qF -- '`--recount` is MANDATORY on every run-patch' "$PROMPT_FILE" && grep -qF -- 'per stage for #1163' "$PROMPT_FILE" && grep -qF -- "Name each READY's strict / recount" "$PROMPT_FILE" && grep -qF -- 'the SECTION rows' "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'THE CELLS: green at head' "$PROMPT_FILE" && grep -qF -- 'every declared cell + control' "$PROMPT_FILE" && grep -qF -- 'per-tamper' "$PROMPT_FILE" && grep -qF -- 'reds EXACTLY the declared set' "$PROMPT_FILE" && grep -qF -- 'tamper files restored by bytes' "$PROMPT_FILE" && grep -qF -- 'ANCHOR-AMBIGUITY tamper' "$PROMPT_FILE" && grep -qF -- 'plant ONLY :143' "$PROMPT_FILE" && grep -qF -- 'MODIFY-IN-PLACE cell' "$PROMPT_FILE" && grep -qF -- 'PER-FILE TYPECHECK DELTA 0' "$PROMPT_FILE" && grep -qF -- 'planted TS2322 control CAUGHT' "$PROMPT_FILE" && grep -qF -- 'a zero that needs its control' "$PROMPT_FILE" && grep -qF -- 'DELTA -1' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE v2: loopback only, zero :5432' "$PROMPT_FILE" && grep -qF -- 'against the ALLOW set' "$PROMPT_FILE" && grep -qF -- "auth's REPORT set EMPTY" "$PROMPT_FILE" && grep -qF -- '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run' "$PROMPT_FILE" && grep -qF -- 'login_stub cleared by PID' "$PROMPT_FILE" && grep -qF -- 'the bash lane NOT instrumented' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'Backlog -> In Progress walks recorded' "$PROMPT_FILE" && grep -qF -- 'KS-1237 assigned to the board login at item 0' "$PROMPT_FILE" && grep -qF -- 'the three branchName EXCISIONS' "$PROMPT_FILE" && grep -qF -- 'no archived key in any branch' "$PROMPT_FILE" && grep -qF -- 'Recommend nothing' "$PROMPT_FILE" && grep -qF -- "PR #1156 is PR 6's KS-1237" "$PROMPT_FILE" && grep -qF -- "PR #1158 is PR 7's KS-855" "$PROMPT_FILE" && grep -qF -- 'THE TWO-SEAT ARTEFACTS' "$PROMPT_FILE" && grep -qF -- 'every push INSIDE the push-window lock' "$PROMPT_FILE" && grep -qF -- 'grade present / absent + MONOTONIC' "$PROMPT_FILE" && grep -qF -- 'TWENTY windows' "$PROMPT_FILE" && grep -qF -- 'THE SERIES STOP at the ks1199 boundary' "$PROMPT_FILE" && grep -qF -- "attributions the seat made for Seat B's PRs BY NAME" "$PROMPT_FILE" && grep -qF -- 'four-condition rule' "$PROMPT_FILE" && grep -qF -- 'ONLY tolerated state change' "$PROMPT_FILE" && grep -qF -- 'the S3 CROSS-SEAT KILL' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S OWN FINDINGS / SLIPS" "$PROMPT_FILE" && grep -qF -- 'CONFIRMED / REFUTED' "$PROMPT_FILE" && grep -qF -- 'F-FALSECOVER-944 (BY-NAME 5 / 11' "$PROMPT_FILE" && grep -qF -- "F-45 (KS-910's push ran 45 shell suites" "$PROMPT_FILE" && grep -qF -- 'S1 the VAULT daily-note overwrite' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- '5 s timeouts' "$PROMPT_FILE" && grep -qF -- 're-run standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM — TWELVE lines VERBATIM' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER' "$PROMPT_FILE" && grep -qF -- 'SIXTEEN targets' "$PROMPT_FILE" && grep -qF -- 'alone-tree reading' "$PROMPT_FILE" && grep -qF -- 'stays In Progress' "$PROMPT_FILE" && grep -qF -- 'SHIPS-WITH text ≤ 3 sentences' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED rows NAMED' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED for its own file' "$PROMPT_FILE" && grep -qF -- 'sha256 + byte count IN the mail' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED written FIRST' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:6000 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" && grep -qF -- 'NAMESPACE GUARD' "$PROMPT_FILE" && grep -qF -- 'TWELVE lines, one per PR' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'node_modules per ENTRY' "$PROMPT_FILE" && grep -qF -- 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF -- 'no memory maintenance' "$PROMPT_FILE" && grep -qF -- 'NEVER print a credential value' "$PROMPT_FILE" && grep -qF -- 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" && grep -qF -- 'NEVER touch the push-window lock directory' "$PROMPT_FILE" && grep -qF -- 'by ANCESTRY' "$PROMPT_FILE" && grep -qF -- 'never by a basename' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST' "$PROMPT_FILE" && grep -qF -- 'run-shell-suites.sh' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; test-file-only; the trees and the zero overlap; canonical identity with the recount class; the cells; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries the TIER 2 floor and each PR tier (#1148 T2, #1150 T2, #1152 T2, #1154 T2, #1156 T2, #1158 T1, #1160 T1, #1162 T1, #1163 T1, #1164 T1, #1165 T1, #1166 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, TWELVE verdict lines"
  echo "  prompt names the report directory, the #1136-#1146 PRIOR REPORT, the #1130-#1135 EARLIER REPORT, the #1119-#1128 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-c16-*, s-b16-*) and the seat 2026-09-22_seatC-16th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (189 tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the twelve-PR tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (114 keywords)"
  [ -n "${QAB1148_CUR_DEV:-}" ] && echo "  (develop read from the QAB1148_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1148_BRIEF:-}${QAB1148_PROMPT:-}${QAB1148_HEAD_1166:-}${QAB1148_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
