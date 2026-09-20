#!/bin/bash
# launch_qa_secuura_batch1106-1111.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SIX file-disjoint Secuura/Blockchain PRs
#   #1106 KS-1232 @ 2abc82d11  api-gateway VITEST test: INFOEMPTY-1, connector/info answers [] for a stored "", 0 or false — TIER 2 (test-only), pushed FIRST
#   #1107 KS-753  @ 7e7da2f88  timestamping VITEST test: MOCKVERIFIED-1, the mock TSA fallback is reported verified: true TODAY (decides nothing) — TIER 2
#   #1108 KS-1234 @ 4904c081c  api-gateway CODE PATCH: V1-ALIAS-BODYPARSE, ONE product line (index.ts:413 shouldParseBody judges the /api/v1 alias by its
#         rewritten path — a middleware-skip WIDENING on every /api/v1/<proxyPath> alias) + ONE new red-first test (94 lines) — TIER 1 (Wednesday's ruling)
#   #1109 KS-1279 @ f592268af  BASH PATCH: RATIO-ENVFAIL, ONE script line + ONE comment in scripts/preflight/preflight.sh (:704-:705, the :711 twin
#         unchanged) + ONE new bash test (83 lines) — TIER 2
#   #1110 KS-880  @ a2a7d7845  security VITEST test: DEADCONV-1, the dead converters.ts rowToApiKey maps neither tenantId nor connectorId — TIER 1 (security)
#   #1111 KS-1223 @ 3d1ea289a  api-gateway VITEST test: WALLET-1, x-wallet-address is OUTSIDE the trust-header strip — TIER 1 (the strip), pushed LAST
# #1106, #1107, #1110, #1111 are TEST-ONLY (files API + local diff-tree: 0 product bytes, 0 deleted lines); #1108 is exactly `1 1` on index.ts + `94 0`
# on the new test; #1109 exactly `2 1` on preflight.sh + `83 0` on the new test (generator-asserted by numstat).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the six heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR trees and blobs by diff --raw; the per-PR trees over develop and the two all-six trees by REAL 3-way merges in a
# --shared scratch clone in SIX orders each (predict_batch_scratch.out) AND by pure tree hashing in the generator; every BOTH-list token asserted
# present in the READY capture and the prompt at generation.
# MG-1 / MG-2 THIS ROUND: targets12.py wants exactly ONE equality target PER PR FILE (1/1/2/2/1/1) and parses the list non-greedily to the FIRST `;`
# (targets12.py:26) — the #1108 and #1109 addendum lines carry TWO targets COMMA-separated (exit 25).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All six tickets stay where they are (bot-walked In Progress).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + six refs/pull/N/head + six branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS 778e6cfe2 (tree d0c8bfd09, the #1102-#1104 batch tree, landed); origin develop = cbae988db (tree 1f2bc512a)
# = 778e6cfe2 + ONE squash (#1105, KS-1175 + KS-1284, anchoring only, 12 paths DISJOINT from the eight and from the four tamper files). So each PR
# over 778e6cfe2 is a fast-forward (merged tree = head tree) and over cbae988db a clean 3-way merge; compare develop...head = merge_base 778e6cfe2,
# ahead 1, BEHIND 1, files 1/1/2/2/1/1 (exit 10 — a second squash on develop changes `behind` and REFUSES: re-pin deliberately).
# Pairwise file-disjoint (8 paths: 4 modified tests, 1 product file, 1 script, 2 NEW tests; overlap 0 over 15 pairs). ALL SIX over 778e6cfe2 =
# a785e7cb93b46ac4253a13932aab0f10206cdc61 and over cbae988db = 2e981e7779dc9bcabecd099c6e93da21345a8ed0, identical in every order tried.
#
# The develop pin is judged by CONTENT — FORTY-EIGHT paths by blob at the CURRENT develop: the 8 PR paths (6 at develop blobs, 2 ABSENT; any at its
# head blob -> exit 19 LANDED, naming the PR), the 4 tamper files (health.ts, timestamping index.ts, converters.ts, trustHeaders.ts), and what the
# gate runs or reads: verification.ts + referrals.ts (the x-wallet-address readers), db.retry.test.ts (LOAD-1), security index.ts + the ks869 test
# (the LIVE rowToApiKey), the ks781 shared test, the four services' package.json / vitest.config.ts / tsconfig.json (+ api-gateway vitest.setup.ts),
# run-shell-suites.sh, the pre-push hook, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md, the spec yaml, the two MCP relay files, the
# 8 sibling bash suites.
# GUARDED: api-gateway src/ + config, timestamping src/ + config, security src/ + config, packages/shared src/ + config, referral src/routes/,
# mcp-server src/, scripts/, .githooks/, docs/openapi/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-21_gate1106to1111/mail_batch1106_ready.md, the seat's SIX READY mails (15:36:16Z … 16:09:59Z) + the 15:28:28Z STATUS
# mail, each captured verbatim by message id from wednesday-agent@ and combined in PR order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2).
# exit 10: the compare per PR (merge_base 778e6cfe2, ahead 1, behind 1, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all six heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1102-#1104), the DEVELOP-MOVE REPORT (#1105), the EARLIER REPORT
#          (#1100-#1101) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (two for #1108 and #1109, comma-separated), the
#          `## MERGE ADDENDUM` heading targets12.py parses from report.md, and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b11-*) and writing in the seat 2026-09-21_seatB-11th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4006 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, both develops and their trees, the six head trees, the
#          six per-PR trees over develop, the two all-six trees, the eight head blobs, the eight plant sha256s, the eight tamper ids, the suite
#          counts, INT-1 / LINT-1 / F2 words, the :4006 and :5432 words, the numstats, the reanchor, the archived and foreign keys), and the prompt
#          must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name BOTH all-six trees in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the six, which ticket the PR is (PR #1106 is KS-1232. … PR #1111 is KS-1223.).
# exit 33: the prompt must carry Wednesday SIXTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1106_CUR_DEV (test override, --check only): stands in for origin develop. QAB1106_HEAD_1111 (test override): stands in for #1111 pinned head.
# QAB1106_BRIEF / QAB1106_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1106_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1106to1111/gen_launcher_1106.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1105.py x launch_qa_secuura_batch1102_1104.sh.
#
# Usage: launch_qa_secuura_batch1106-1111.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1106_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1106to1111/mail_batch1106_ready.md}"
PROMPT_FILE="${QAB1106_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1106-1111.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1106|KS-1232|refs/heads/feature/ks-1232-get-apiconnectorinfo-tells-a-connector-all-types-permitted-infoempty-1|2abc82d11014f00567b75a6b8fab5ec5e78f9df2|1"
  "1107|KS-753|refs/heads/feature/ks-753-timestamping-fail-closed-a-mock-tsa-fallback-must-not-report-mockverified-1|7e7da2f88f9ef8dcf571a5720bb7bffcd700aa30|1"
  "1108|KS-1234|refs/heads/feature/ks-1234-post-apiv1documents-with-applicationjson-never-answers-and-v1-alias-bodyparse-1|4904c081c4f9be776acef78349bc10384f10de35|2"
  "1109|KS-1279|refs/heads/feature/ks-1279-preflights-legs-ran-ratio-counts-leg-1-as-run-on-a-no-ratio-envfail-1|f592268af36b282029e50ff2fa1ebe2614304b81|2"
  "1110|KS-880|refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-deadconv-1|a2a7d7845e75dac2df5c6ad0c4109d5f63394d4c|1"
  "1111|KS-1223|refs/heads/feature/ks-1223-a-client-x-wallet-address-is-forwarded-past-the-gateway-wallet-1|${QAB1106_HEAD_1111:-3d1ea289a0c367af5cd0d060322e46fc900a1c76}|1"
)
DEVELOP_SHA='cbae988dbe90ebe556459ada2cb437eaf80e2402'   # the pin = origin develop at generation (778e6cfe2 + the #1105 squash)
MERGE_BASE='778e6cfe2b6061d60ffcf3a57a951c84dc152b67'   # every head's parent = merge-base = the develop the seat built on
ALL_OVER_BASE='a785e7cb93b46ac4253a13932aab0f10206cdc61'   # all six over 778e6cfe2 (the seat's batch tree; fast-forward chain)
ALL_OVER_DEV='2e981e7779dc9bcabecd099c6e93da21345a8ed0'     # all six over the pin cbae988db (real 3-way, six orders; generator tree-hash) — the tree that matters for the merge
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
DEVMOVE_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1106to1111/mail_batch1106_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The six heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 778e6cfe2, ahead 1, behind 1 (the one
# #1105 squash), files 1/1/2/2/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
WANT_COMPARE="1106 $MERGE_BASE ahead=1 behind=1 files=1
1107 $MERGE_BASE ahead=1 behind=1 files=1
1108 $MERGE_BASE ahead=1 behind=1 files=2
1109 $MERGE_BASE ahead=1 behind=1 files=2
1110 $MERGE_BASE ahead=1 behind=1 files=1
1111 $MERGE_BASE ahead=1 behind=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1106_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
T = D + "services/timestamping/"
S = D + "services/security/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the two NEW tests)
JUDGED = {
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks480-connector-auth.test.ts":          ({"eca492723115531d8daa52d1d8b52b1b9b99970a": DV}, {"16e88d9b7e00d816e6a93bfb4359e6bdc43fcb43": "#1106 own"}),
  "Blockchain/Dev/services/timestamping/src/__tests__/ks740-bounded-fanout.test.ts":         ({"a36eaa20ef8e96504a1844ba2eb16e3098f5ad0f": DV}, {"6fdf0e80a46ce75c0e0f4c5540aea443779d944c": "#1107 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1234-v1-documents-json-create-never-answers.test.ts": ({"ABSENT": DV}, {"3f85887f7268a9a19fd61d73e6178bf7f6c892dc": "#1108 own"}),
  "Blockchain/Dev/services/api-gateway/src/index.ts":                                        ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {"4e7fc1174d5453f9d6f71e3a69f166fc6a08db49": "#1108 own"}),
  "Blockchain/Dev/scripts/__tests__/preflight_ratio_excludes_leg1_no_install.test.sh":       ({"ABSENT": DV}, {"42f43cd4393f57ece8d24ad122b5c02a438ebf17": "#1109 own"}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                           ({"712f895362e2c8d1ead6fd09ac257d7bce212948": DV}, {"fe29676b7073d4b6b9a71d492de962777cf5bdf8": "#1109 own"}),
  "Blockchain/Dev/services/security/src/__tests__/row-converters.test.ts":                   ({"17930b12b97344d23f7833dcc6de5705dde48be2": DV}, {"bde8ae21f66cdf34ae2342222cbfc6c281bec3fc": "#1110 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1041-vouch-header-strip.test.ts":     ({"a3e1631f4046288339898170bdaa1f2faff347d5": DV}, {"c92a7f85516b6b185e13ec14eec868d27f070244": "#1111 own"}),
  "Blockchain/Dev/services/api-gateway/src/services/health.ts":                              ({"7bedc074583d816d997bd6d679043db010804aed": DV}, {}),
  "Blockchain/Dev/services/timestamping/src/index.ts":                                       ({"1d2f109f644d01915f720e1894741794c91f4338": DV}, {}),
  "Blockchain/Dev/services/security/src/converters.ts":                                      ({"04b9952eb7e4695c687f35791707b5866f26e55a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts":                           ({"15626e80f6caea4866abd1bb9ad171c79e12e788": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/verification.ts":                          ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  "Blockchain/Dev/services/referral/src/routes/referrals.ts":                                ({"e97b7f0bc5506118043adb8537a15cc0879d9c5d": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/db.retry.test.ts":                      ({"5933da41ed3dcf37f415000c4da4a717ea8d7eba": DV}, {}),
  "Blockchain/Dev/services/security/src/index.ts":                                           ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  "Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts":     ({"7a3fc7e16d0c93a2c70edbda853d6acf4faee259": DV}, {}),
  "Blockchain/Dev/packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts":       ({"bc4815c4ec9cae2f065e29dec6b938cdf49f2d23": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                        ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                    ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.setup.ts":                                     ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                       ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/timestamping/package.json":                                       ({"450cb6dc189a8552eb0923a44a4a7b29d4b1eb69": DV}, {}),
  "Blockchain/Dev/services/timestamping/vitest.config.ts":                                   ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/timestamping/tsconfig.json":                                      ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/services/security/package.json":                                           ({"a2f2e03ff75b5aba19a9aac97a827cb7a6c50aba": DV}, {}),
  "Blockchain/Dev/services/security/vitest.config.ts":                                       ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/security/tsconfig.json":                                          ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                             ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                         ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                            ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                              ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  ".githooks/pre-push":                                                                      ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/package.json":                                                             ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                        ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                        ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                              ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
  "Blockchain/Dev/services/mcp-server/src/tools/info.ts":                                    ({"c0f2268ca0aceeec2d89639bbead5bbc549fe859": DV}, {}),
  "Blockchain/Dev/services/mcp-server/src/http-server.ts":                                   ({"fce4a31793b3765de96fc387a2f306da5db15744": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/check_slot_credentials.test.sh":                         ({"5ea337e2c7b92bcc92bb99cea4d229fb354d0358": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/no_tracked_credentials_root.test.sh":                    ({"b4e622e3a7c605ff050cec14e40d9f1fccd030cc": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh":                             ({"affdf027bff11e3690d374e902e3e93274788c62": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/pre_push_hook_current_develop.test.sh":                  ({"60ae41616a9f54594509e08917cd83eaf25dbc1d": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh":                                 ({"5ad0541313589635c6c100677cf14fb02d00be78": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh":          ({"8bab19ddaa78617b3eea67d09fff072a97036823": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/preflight_state_is_initialised.test.sh":                 ({"ee31ee5f5bc3f0e4939df9587e346296b8ea494c": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/preflight_verdict_names_real_failures.test.sh":          ({"fb762f6389a0700afcab456fc275062cace05520": DV}, {}),
  "Blockchain/Dev/docs/openapi/secuura-api.yaml":                                            ({"1871025e2c1196aeb6ff33e9bc74b916d3eb9e9e": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (778e6cfe2 + the #1105 squash; every head merges clean over it; all six together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/", A + "package.json", A + "vitest.config.ts", A + "vitest.setup.ts", A + "tsconfig.json",
           T + "src/", T + "package.json", T + "vitest.config.ts", T + "tsconfig.json",
           S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json",
           P + "src/", P + "package.json", P + "vitest.config.ts", P + "tsconfig.json",
           D + "services/referral/src/routes/", D + "services/mcp-server/src/",
           D + "scripts/", ".githooks/", D + "docs/openapi/",
           D + "package.json", D + "package-lock.json", D + "eslint.config.mjs", "BACKLOG.md"]
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
tail = "the gate merges the then-current develop onto EACH of the six heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-six tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1106.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1106 KS-1232: TIER 2' "$PROMPT_FILE" && grep -qF '#1107 KS-753: TIER 2' "$PROMPT_FILE" && grep -qF '#1108 KS-1234: TIER 1' "$PROMPT_FILE" && grep -qF '#1109 KS-1279: TIER 2' "$PROMPT_FILE" && grep -qF '#1110 KS-880: TIER 1' "$PROMPT_FILE" && grep -qF '#1111 KS-1223: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1106-#1111 (six PRs; tier 1 = #1108, #1110, #1111)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SIX lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SIX verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$DEVMOVE_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the DEVELOP-MOVE REPORT $DEVMOVE_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1108 TWO, #1109' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1108 TWO, #1109 TWO, comma-separated), the ## MERGE ADDENDUM heading and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b11-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-11th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b11-*) and writing in the seat 2026-09-21_seatB-11th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4006 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4006 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          a785e7cb93b46ac4253a13932aab0f10206cdc61 \
          2e981e7779dc \
          cbae988dbe90ebe556459ada2cb437eaf80e2402 \
          778e6cfe2b6061d60ffcf3a57a951c84dc152b67 \
          d0c8bfd095b6 \
          1f2bc512aee2 \
          50eb9b8683ec332b1d7caa4ee2b73552da6c6765 \
          ceb6bdc7e2f101919ff81750ec6594f906680006 \
          83bd05b8033f2a8d15bf5af72b67d4afcd9004ff \
          a33bde818f2e790fd81610fa3abe9fe2f2a1c705 \
          04659f893122a9b5c1edd5b98160eee90ef881db \
          4a0792982a1bd8451b834d02cbe3013ee8fd2987 \
          4de60c4def27 \
          f6e218ea6fab \
          3d91c935f41f \
          44ba2d430d33 \
          42641a11669e \
          1d877179f20c \
          16e88d9b7e00d816e6a93bfb4359e6bdc43fcb43 \
          6fdf0e80a46ce75c0e0f4c5540aea443779d944c \
          3f85887f7268a9a19fd61d73e6178bf7f6c892dc \
          4e7fc1174d5453f9d6f71e3a69f166fc6a08db49 \
          42f43cd4393f57ece8d24ad122b5c02a438ebf17 \
          fe29676b7073d4b6b9a71d492de962777cf5bdf8 \
          bde8ae21f66cdf34ae2342222cbfc6c281bec3fc \
          c92a7f85516b6b185e13ec14eec868d27f070244 \
          ffc1ee73959b \
          518f4001c9db \
          987e9d341057 \
          9811ba5fe34f \
          734ef5eda655 \
          178c3b24f478 \
          793e0a42939a \
          6e9106afb9a5 \
          NULLISHRAW \
          NOTALIST \
          VERIFIEDEQEIDAS \
          VERIFIEDNOTMOCK \
          TENANTMAPPED \
          CONNECTORMAPPED \
          WALLETINPATTERN \
          BAGDELETESWALLET \
          678 \
          679 \
          681 \
          683 \
          42 \
          43 \
          213 \
          214 \
          907/907 \
          231/231 \
          :4006 \
          INT-1 \
          LINT-1 \
          no-useless-assignment \
          preflight_deps \
          'leg 14' \
          :5432 \
          'STOP-class 0' \
          127.0.0.1:1 \
          anchoring:4005 \
          localhost:6000 \
          203.0.113.7:443 \
          shouldParseBody \
          referrals.ts:55 \
          :711 \
          :704 \
          :705 \
          REANCHOR \
          'patch failed' \
          '86 2' \
          '`1 1`' \
          '94 0' \
          '`2 1`' \
          '83 0' \
          MG-2 \
          MG-1 \
          1/1/2/2/1/1 \
          section_1 \
          section_2 \
          converters.ts \
          rowToApiKey \
          x-wallet-address \
          'verified: true' \
          'stubs=4' \
          'skips are not a pass' \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          login_stub \
          mergeable_state \
          'linear[bot]' \
          attachmentsForURL \
          contributes \
          'Deviation from verbatim: NONE' \
          'bash -n' \
          /bin/bash \
          shellcheck \
          tools/info.ts:144 \
          http-server.ts:258 \
          KS-1062 \
          KS-1238 \
          KS-1282 \
          KS-501 \
          KS-480 \
          KS-740 \
          KS-1041 \
          KS-523 \
          KS-1046 \
          KS-781 \
          KS-1260 \
          KS-1209 \
          KS-953 \
          KS-741 \
          '#995' \
          TS2322 \
          CAUGHT; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF "$ALL_OVER_BASE" "$PROMPT_FILE" && grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name both all-six trees and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1106 is KS-1232.' "$PROMPT_FILE" && grep -F '#1106' "$BRIEF" | grep -qF 'KS-1232' && grep -qF 'PR #1107 is KS-753.' "$PROMPT_FILE" && grep -F '#1107' "$BRIEF" | grep -qF 'KS-753' && grep -qF 'PR #1108 is KS-1234.' "$PROMPT_FILE" && grep -F '#1108' "$BRIEF" | grep -qF 'KS-1234' && grep -qF 'PR #1109 is KS-1279.' "$PROMPT_FILE" && grep -F '#1109' "$BRIEF" | grep -qF 'KS-1279' && grep -qF 'PR #1110 is KS-880.' "$PROMPT_FILE" && grep -F '#1110' "$BRIEF" | grep -qF 'KS-880' && grep -qF 'PR #1111 is KS-1223.' "$PROMPT_FILE" && grep -F '#1111' "$BRIEF" | grep -qF 'KS-1223' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1106 is KS-1232. … PR #1111 is KS-1223.)" >&2; exit 32; }
grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes on #1106, #1107, #1110 and' "$PROMPT_FILE" && grep -qF -- 'ONE product line on #1108' "$PROMPT_FILE" && grep -qF -- 'ONE script edit on #1109' "$PROMPT_FILE" && grep -qF -- 'DISJOINTNESS AND THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'at least forward and exact reverse' "$PROMPT_FILE" && grep -qF -- 'read-tree back to each develop' "$PROMPT_FILE" && grep -qF -- 'security develop baseline 213' "$PROMPT_FILE" && grep -qF -- 'THE THREE SKIPPED LEGS' "$PROMPT_FILE" && grep -qF -- 'legs 3 4 8' "$PROMPT_FILE" && grep -qF -- 'skip_stack' "$PROMPT_FILE" && grep -qF -- 'would have EXERCISED these changes' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST PER TEST-ONLY PR' "$PROMPT_FILE" && grep -qF -- 'DEVELOP COVER measured' "$PROMPT_FILE" && grep -qF -- 'both tampers of a PR red' "$PROMPT_FILE" && grep -qF -- 'NOT routes/' "$PROMPT_FILE" && grep -qF -- 'FOUR lines :516 / :573 / :603 / :612' "$PROMPT_FILE" && grep -qF -- 'THE FULL WEIGHT' "$PROMPT_FILE" && grep -qF -- 'ZERO bare `+` lines in the index.ts hunk' "$PROMPT_FILE" && grep -qF -- 'a 3 s timeout red' "$PROMPT_FILE" && grep -qF -- 'VALUE TABLE of `shouldParseBody(req)`' "$PROMPT_FILE" && grep -qF -- 'the four middlewares it now skips' "$PROMPT_FILE" && grep -qF -- ':561 runs AFTER :416-:459' "$PROMPT_FILE" && grep -qF -- 'THE TEST PINS THE ALIAS ONLY' "$PROMPT_FILE" && grep -qF -- 'ALIASWIDENINGOTHERROUTES' "$PROMPT_FILE" && grep -qF -- 'SECURITYMIDDLEWARESKIPUNPINNED' "$PROMPT_FILE" && grep -qF -- '231/231' "$PROMPT_FILE" && grep -qF -- "develop's own" "$PROMPT_FILE" && grep -qF -- 'The 307: out of scope' "$PROMPT_FILE" && grep -qF -- 'pins EXACTLY the strip and nothing else' "$PROMPT_FILE" && grep -qF -- 'verification.ts:1296' "$PROMPT_FILE" && grep -qF -- 'referrals.ts:55' "$PROMPT_FILE" && grep -qF -- 'WALLETFORWARDUNPINNED' "$PROMPT_FILE" && grep -qF -- 'REFERRALFALLBACKUNPINNED' "$PROMPT_FILE" && grep -qF -- 'NOT pinned BY DESIGN' "$PROMPT_FILE" && grep -qF -- 'PROVE THE COPY IS DEAD' "$PROMPT_FILE" && grep -qF -- 'security/src/index.ts:418' "$PROMPT_FILE" && grep -qF -- 'LIVETENANTDEFAULT' "$PROMPT_FILE" && grep -qF -- 'fix-robust' "$PROMPT_FILE" && grep -qF -- 'MODULE ABSENCE' "$PROMPT_FILE" && grep -qF -- 'DECIDES NOTHING on the 503-vs-verified:false question' "$PROMPT_FILE" && grep -qF -- 'FIX-ROBUST in that sense' "$PROMPT_FILE" && grep -qF -- '201 -> 503' "$PROMPT_FILE" && grep -qF -- "vi.doMock('../db')" "$PROMPT_FILE" && grep -qF -- 'MCPINFORAWECHO' "$PROMPT_FILE" && grep -qF -- 'HTTPSERVERINFOEMPTY' "$PROMPT_FILE" && grep -qF -- 'stale collision flag' "$PROMPT_FILE" && grep -qF -- 'two-section strict apply' "$PROMPT_FILE" && grep -qF -- 'corrupt patch.diff rc 1 reproduced' "$PROMPT_FILE" && grep -qF -- 'reanchor disclosure' "$PROMPT_FILE" && grep -qF -- 'twin byte-unchanged at :712' "$PROMPT_FILE" && grep -qF -- '2 FAIL / 4 ok' "$PROMPT_FILE" && grep -qF -- '6 ok / 0 FAIL' "$PROMPT_FILE" && grep -qF -- 'INT-1: re-run preflight_deps' "$PROMPT_FILE" && grep -qF -- 'env_fail=1 now subtracts one' "$PROMPT_FILE" && grep -qF -- 'ENVFAILONLYSUBTRACTSONE' "$PROMPT_FILE" && grep -qF -- 'PRE-EXISTING, CLOSED by the EARLIER REPORT' "$PROMPT_FILE" && grep -qF -- 're-run that suite SERIAL' "$PROMPT_FILE" && grep -qF -- 'report the ratio' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'THE CONNECTION CENSUS' "$PROMPT_FILE" && grep -qF -- 'CENSUS RULE v2' "$PROMPT_FILE" && grep -qF -- 'the baseline leg REPORTS only' "$PROMPT_FILE" && grep -qF -- 'a real Postgres listens on 127.0.0.1:5432' "$PROMPT_FILE" && grep -qF -- 'THE :4006 LISTENER' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'KS-1106' "$PROMPT_FILE" && grep -qF -- 'KS-1111' "$PROMPT_FILE" && grep -qF -- 'Completes KS-1234' "$PROMPT_FILE" && grep -qF -- 'recommend nothing' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'proposed cell' "$PROMPT_FILE" && grep -qF -- "local model's next round" "$PROMPT_FILE" && grep -qF -- 'ONE MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- '#1108 TWO, #1109' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- 'targets12.py:26' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'targets12.py reads report.md' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S SLIPS S1 / S2 / S3 / S4 / S5 / S6" "$PROMPT_FILE" && grep -qF -- 'none reached a pushed byte' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday sixteen by-name items (tier/round/product bytes; the trees over both develops; the three skipped legs; red-first per test-only PR with the develop cover; #1108 the widening value table + the test pins the alias only; #1111 the strip and its two readers; #1110 the copy is dead + the live default; #1107 decides nothing + fix-robust; #1106 the MCP relays; #1109 two sections + the reanchor + INT-1 + env_fail; db.retry serial ratio + ruling; census v2 + :4006; link hygiene incl. KS-1106..KS-1111; NOT-PINNED format; addendum per PR comma-separated under ## MERGE ADDENDUM; the seat slips) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  six heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1108 T1, #1110 T1, #1111 T1, #1106 T2, #1107 T2, #1109 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all six heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1102-#1104 PRIOR REPORT, the #1105 DEVELOP-MOVE REPORT, the #1100-#1101 EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1108 TWO, #1109 TWO, comma-separated), the ## MERGE ADDENDUM heading and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b11-*) and the seat 2026-09-21_seatB-11th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4006 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (119 tokens: both develops + trees, six head trees, six per-PR trees over develop, both all-six trees, eight head blobs, eight plant shas, eight tamper ids, counts, INT-1/LINT-1, :4006/:5432, numstats, reanchor, archived + foreign keys); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names both all-six trees and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each of the six PRs is"
  echo "  prompt carries Wednesday sixteen by-name items and the standard closing (95 keywords)"
  [ -n "${QAB1106_CUR_DEV:-}" ] && echo "  (develop read from the QAB1106_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1106_BRIEF:-}${QAB1106_PROMPT:-}${QAB1106_HEAD_1111:-}${QAB1106_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
