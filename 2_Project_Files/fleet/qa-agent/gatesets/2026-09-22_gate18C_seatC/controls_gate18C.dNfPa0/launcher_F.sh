#!/bin/bash
# launch_qa_secuura_batch1167-1175.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate over SIX Secuura/Blockchain PRs (Seat C 18th):
# TIER 1 on FOUR (#1167 #1171 #1173 #1175 — KS-947 the MFA-limiter auth-surface pin + the THREE code_patch PRs with PRODUCT bytes on api-gateway), TIER 2 on
# the two test-only pins; seven local-model R16 ROUND-2 READYs (three run patches strict + four code_patch runs applied per SECTION file, the ONE
# .opts accommodation on KS-1231 Part B section 1) grouped by TICKET = by FILE into six PRs on ONE lane — api-gateway vitest — TEN paths, the ONE
# same-file PAIR health.ts (#1171 Part B + #1173: the merging seat passes --pair-blob on #1173 after #1171), ZERO overlap with Seat B 18th's nine.
#   #1167 PR 1 KS-947 F3F4b @ 4f2b87547  TEST-ONLY ks733-users-mfa-rate-limit-mount.test.ts +66/-0 — TIER 1
#   #1168 PR 2 KS-1123 F3b-CAST @ e17efafa7  TEST-ONLY ks1123-api-gateway-verify-an-empty-string.test.ts +215/-0 — TIER 2
#   #1169 PR 3 KS-1192 NOQUOTE @ 9088a3509  TEST-ONLY ks1192-real-app-production-erasure-door.test.ts +144/-0 — TIER 2
#   #1171 PR 4 KS-1231 PARTA PARTB @ f17ec0af4  CODE_PATCH (product: verification.ts + health.ts) ks1231-a-connector-allow-list-fails-open.test.ts + verification.ts + ks1231-info-reader-malformed-container-refused.test.ts + health.ts +348/-6 — TIER 1
#   #1173 PR 5 KS-1246 SERVICESBODY @ 611c9d504  CODE_PATCH (product: health.ts) ks1246-f-2-health-services-still-reads.test.ts + health.ts +138/-1 — TIER 1
#   #1175 PR 6 KS-1257 SETTINGSDEFAULTS (THREEHUNKS) @ be3fb14b6  CODE_PATCH (product: admin.ts) ks1230-settings-write-validates-allowed-document-types.test.ts + admin.ts +97/-8 — TIER 1
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the head trees (= the trees over the heads' parent 8c2f7b3fd: each head's parent IS that
# commit) by pure tree hashing; the all-6 tree over the parent (52853c8bf6c4…) by REAL applies of the 11 canonicals in three orders AND real
# 3-way merges of the heads in four orders in a --shared scratch clone under a cwd guard (predict_batch_scratch_*.out) AND by tree hashing with
# health.ts at the PAIR blob; every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets18.py wants exactly ONE equality target PER PR FILE (1/1/1/4/2/2 = ELEVEN over TEN paths) and parses the
# list non-greedily to the FIRST `;` — three multi-file lines this round (#1171 four, #1173 two, #1175 two: the COMMA-separated MG-2 form is
# EXERCISED); #1173's health.ts target is the ALONE blob bca1d9500aa3 by construction and is REWRITTEN to the PAIR blob ae6017a84cf7… at merge
# time (--pair-blob, the 2026-09-21 21:02 ruling); merge18b.py asserts each squash body's key set == the PR's OWN Refs set (one key each).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All six tickets stay where they are (In Progress; bot-walked).
#
# THE SHAPE, re-read live by the generator: each head is ONE commit whose parent IS 8c2f7b3fd (tree 04b05e093ad8 — the #1036 KS-763 squash the
# seat itself wrote FIRST on Wednesday's separate GO, over 3916eacd1). ORIGIN DEVELOP: the pin is 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 (tree 04b05e093ad8) — UNMOVED since
# the raise at generation (behind 0); the compare per PR reads develop...head = merge_base 8c2f7b3fd, ahead 1, BEHIND 0, files
# 1/1/1/4/2/2 (exit 10 — a develop move changes `behind` and REFUSES: re-pin deliberately — Seat B 18th's GO may land its seven merges first).
# ALL SIX over the parent = 52853c8bf6c4ff43585cdade61c637ff8cbaa5d0; ALL SIX over the current develop = 52853c8bf6c4ff43585cdade61c637ff8cbaa5d0 (the END STATE if every merge
# lands on 8c2f7b3fd).
#
# The develop pin is judged by CONTENT — the 10 target paths at the CURRENT develop (five NEW files judged ABSENT — any present blob -> exit 19
# LANDED if it is the head blob, exit 18 otherwise; the five MODIFIED files by blob — health.ts LANDED on EITHER alone blob OR the PAIR blob) plus
# 32 unchanged-read paths (index.ts — this round's other tamper file; the 16th's seven other tamper files; the 15th's five; the hook,
# preflight.sh, run-shell-suites.sh, fix-libsodium-symlink.js, audit-baseline.json (#1036's), proxy.ts, the ks1072 / ks815 / ks1123-f2 /
# ks1123-f3 test files the census and the covers name, api-gateway's package.json / vitest.config.ts / tsconfig.json / lock, packages/shared's
# package.json / config, the Dev package.json + lock, eslint.config.mjs). GUARDED on a move: api-gateway src + config, packages/shared src +
# config, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs (originate / anchoring / auth — Seat B 18th's lanes — are NOT
# guarded: a Seat B merge is a disjoint move by the partition, still refused at exit 10 by `behind`).
#
# SOURCE = gatesets/2026-09-22_gate18C_seatC/mail_gate18C_ready.md, the seat's six READY mails (23:37:46Z … 00:32:55Z; PR 4's carries BOTH KS-1231
# READY rows) + its 22:55:59Z, 23:26:38Z and 00:42:07Z STATUS mails + its two QUESTION mails, each captured verbatim by message id from
# wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry TIER 1 on FOUR of the six AND each PR own tier line (#1167 T1, #1168 T2, #1169 T2, #1171 T1, #1173 T1, #1175 T1).
# exit 10: the compare per PR (merge_base 8c2f7b3fd, ahead 1, behind 0, files 1/1/1/4/2/2) — develop moving refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name every pinned head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1148-#1166), the EARLIER REPORT (#1147-#1161), the OLDER REPORT
#          (#1036 KS-763) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE, the `## MERGE ADDENDUM` heading targets18.py
#          parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-c18-*, s-b18-*) and writing in the seat 2026-09-22_seatC-18th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 / :4005 / :6000 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the parent and its tree, the head trees, the all-6
#          tree, the pair / trio trees, the eleven head blobs + the PAIR blob, the eleven canonical sha16s, the five develop blobs, the suite
#          counts, the red/green words, the lock words, the attributions, the archived / content keys, the GO string), and the prompt must ask the
#          gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-6 tree in full, the parent and the current develop in full, the NOT-PINNED section and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH PR, which ticket the PR is (PR #1167 is KS-947. … ).
# exit 33: the prompt must carry Wednesday SIX-PR BY-NAME items (twelve), each by its own keywords (the ladder below), and the standard closing.
# exit 34: a PARTIAL prompt (any `PENDING-PR-` token) refuses — --check and launch alike; inherited, never expected this round.
# exit 35: the prompt must carry the PAIR: `--pair-blob`, the pair blob ae6017a84cf7aff42e17e1fe06ed66032e513d8c in full, and `alone blob`.
# QAB1167_CUR_DEV (test override, --check only): stands in for origin develop. QAB1167_HEAD_1175 (test override): stands in for #1175 pinned head.
# QAB1167_BRIEF / QAB1167_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1167_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-22_gate18C_seatC/gen_launcher_gate18C.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_gate16C.py / gen_launcher_gate15.py.
#
# Usage: launch_qa_secuura_batch1167-1175.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..35 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1167_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18C_seatC/mail_gate18C_ready.md}"
PROMPT_FILE="${QAB1167_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-22_secuura-batch1167-1175.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1167|KS-947|refs/heads/feature/ks-947-gate-blindness-f3f4-the-parity-cell-misses-skip-and-r16-f3f4b-1|4f2b87547d8060646763a5f15ef4a165a1e436bd|1"
  "1168|KS-1123|refs/heads/feature/ks-1123-api-gateway-verify-an-empty-string-0-false-anchor-status-is-r16-f3b-cast-1|e17efafa7eac15108cd51bf27eca04902c149603|1"
  "1169|KS-1192|refs/heads/feature/ks-1192-ks871-real-app-canonical-audit-rows-production-cell-does-not-r16-noquote-1|9088a3509730c1663ecae3b380e18d17561f9f77|1"
  "1171|KS-1231|refs/heads/feature/ks-1231-a-connector-allow-list-fails-open-when-platform-settings-r16-parta-partb-1|f17ec0af49d9b3d97e5671176adc70dc3212b7f4|4"
  "1173|KS-1246|refs/heads/feature/ks-1246-f-2-healthservices-still-reads-responseok-only-a-degraded-r16-servicesbody-1|611c9d504463eacd12c37e0be8af11ba67e65c82|2"
  "1175|KS-1257|refs/heads/feature/ks-1257-after-platform-settings-has-expired-a-partial-admin-write-r16-settingsdefaults-1|${QAB1167_HEAD_1175:-be3fb14b6eef1b32cf510a3603287a1ce0e925f7}|2"
)
DEVELOP_SHA='8c2f7b3fd4fde915b2a24542bc32259b24e092a0'   # the pin = origin develop at generation (= the heads' parent; a move refuses at exit 10 / 18)
MERGE_BASE='8c2f7b3fd4fde915b2a24542bc32259b24e092a0'    # every head's parent = the merge-base with the current develop (the #1036 squash)
ALL_OVER_DEV='52853c8bf6c4ff43585cdade61c637ff8cbaa5d0'     # all six over the CURRENT develop (real applies + 3-way merges; generator tree-hash) — the END STATE
ALL_OVER_PARENT='52853c8bf6c4ff43585cdade61c637ff8cbaa5d0'   # all six over the parent 8c2f7b3fd (the seat's measure18b; three + four orders)
PAIR_BLOB='ae6017a84cf7aff42e17e1fe06ed66032e513d8c'   # health.ts with BOTH hunks — #1173's --pair-blob target after #1171
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1167-1175-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1148-1166-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-batch1147-1161-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-22-ks763-1036-4b251997a-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-22_gate18C_seatC/mail_gate18C_ready.md"

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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 8c2f7b3fd, ahead 1, behind 0,
# files 1/1/1/4/2/2 (generator, rev-list --left-right; the launcher reads the compare API). A develop move -> exit 10.
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
WANT_COMPARE="1167 $MERGE_BASE ahead=1 behind=0 files=1
1168 $MERGE_BASE ahead=1 behind=1 files=1
1169 $MERGE_BASE ahead=1 behind=0 files=1
1171 $MERGE_BASE ahead=1 behind=0 files=4
1173 $MERGE_BASE ahead=1 behind=0 files=2
1175 $MERGE_BASE ahead=1 behind=0 files=2"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB (or ABSENT) at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1167_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
SC = D + "scripts/"
DV = "develop"
# file -> (develop-OK blobs {blob or ABSENT: label}, LANDED blobs {blob: label})
JUDGED = {
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts":                          ({"f98e22a735613d46e5e006dc7862dcdb5e6b1328": DV}, {"9f50c828743a09459596c1e7aadd2ef0a191e5e4": "#1167 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-api-gateway-verify-an-empty-string.test.ts":                 ({"ABSENT": DV}, {"94f08cee8859b4e726b6f2c9f07c5f9405f05582": "#1168 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1192-real-app-production-erasure-door.test.ts":                   ({"ABSENT": DV}, {"c0fea7ac4cd94e10e66bce1200946c44d030742f": "#1169 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-a-connector-allow-list-fails-open.test.ts":                  ({"ABSENT": DV}, {"ff079c3c257bde0161ebc43f610abdea92f70170": "#1171 own"}),
  "Blockchain/Dev/services/api-gateway/src/routes/verification.ts":                                                      ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {"bd8165896d173a133859b7a6aa86b94a615d2dbc": "#1171 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1231-info-reader-malformed-container-refused.test.ts":            ({"ABSENT": DV}, {"f6592e6d753eb516c4e7917469169dab9936eecb": "#1171 own"}),
  "Blockchain/Dev/services/api-gateway/src/services/health.ts":                                                          ({"7bedc074583d816d997bd6d679043db010804aed": DV}, {"772a70e4c19350ea9e67176696b747194f579e19": "#1171 own", "bca1d9500aa35af6755fba9ae95b6fe7d2aa5f86": "#1173 own", "ae6017a84cf7aff42e17e1fe06ed66032e513d8c": "the PAIR (#1171 + #1173)"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1246-f-2-health-services-still-reads.test.ts":                    ({"ABSENT": DV}, {"84de41765db423554696f1a12c801ef6103c2c22": "#1173 own"}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts":    ({"893879a1995031a13d4a1969d24f3aa0c60e5d21": DV}, {"966e055f901cbe9932656dde526843ef5115f058": "#1175 own"}),
  "Blockchain/Dev/services/api-gateway/src/routes/admin.ts":                                                             ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {"2e558148f061660ff90744164eaa6e7c2dea9506": "#1175 own"}),
  "Blockchain/Dev/services/api-gateway/src/index.ts":                                                                    ({"4e7fc1174d5453f9d6f71e3a69f166fc6a08db49": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/system-status.ts":                                                     ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
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
  "Blockchain/Dev/scripts/audit/audit-baseline.json":                                                                    ({"648e8ee7bbf22b5737597e3dd61ee92922628e58": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts":                                                             ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts":             ({"d9c98320ea64638c3ab5ef2f35c102aba6d1207a": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks815-verification-router-guards-its-own-body.test.ts":             ({"83c3771c75e3d141a576eb21f787b7b816355931": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts":                  ({"afaa781d438bb350b7a33446fb41b528e3363077": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts":                       ({"8c413fba6dd2687f7f0a70f5460aa3560e13d45b": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"4a4a58de3c79b2f33f335a0fbf845781a2fde127": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package.json":                                                                    ({"3f7dfd358c9e2a8506a8f6bc77b8984617a549ab": DV}, {}),
  "Blockchain/Dev/services/api-gateway/vitest.config.ts":                                                                ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  "Blockchain/Dev/services/api-gateway/tsconfig.json":                                                                   ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  "Blockchain/Dev/services/api-gateway/package-lock.json":                                                               ({"cd2851509155ec1f45290b63e0f0b35675be4cdf": DV}, {}),
  "Blockchain/Dev/package.json":                                                                                         ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                                                    ({"54ba290e54f77725d4f757e974d51eeb3564400f": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                                                    ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob or the PAIR blob, exit 19).
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
    print("OK " + state + " | origin develop still " + pinned + " (the pin = the heads parent; behind 0; all six together " + all_over_dev + " over it, three + four orders, generator tree-hash + scratch-clone applies; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [SH + "src/", SH + "package.json", SH + "vitest.config.ts", SH + "tsconfig.json",
           AG + "src/", AG + "package.json", AG + "vitest.config.ts", AG + "tsconfig.json", AG + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH head in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-6 tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (predict_batch_scratch_gate18C.py + gen_launcher_gate18C.py + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 1 on FOUR' "$PROMPT_FILE" && grep -qF '#1167 KS-947: TIER 1' "$PROMPT_FILE" && grep -qF '#1168 KS-1123: TIER 2' "$PROMPT_FILE" && grep -qF '#1169 KS-1192: TIER 2' "$PROMPT_FILE" && grep -qF '#1171 KS-1231: TIER 1' "$PROMPT_FILE" && grep -qF '#1173 KS-1246: TIER 1' "$PROMPT_FILE" && grep -qF '#1175 KS-1257: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry TIER 1 on FOUR of the six and each PR own tier line (#1167 T1, #1168 T2, #1169 T2, #1171 T1, #1173 T1, #1175 T1)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1167-#1175 (six PRs; tier 1 = #1167, #1171, #1173, #1175: Seat C 18th — KS-947 auth-surface pin + three code_patch product PRs; tier 2 = #1168, #1169)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SIX lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SIX verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qF -- '--pair-blob' "$PROMPT_FILE" && grep -qF "$PAIR_BLOB" "$PROMPT_FILE" && grep -qF 'alone blob' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the PAIR (--pair-blob, the pair blob $PAIR_BLOB in full, 'alone blob')" >&2; exit 35; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-c18-batch' "$PROMPT_FILE" && grep -qF 's-b18-' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-22_seatC-18th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-c18-*, s-b18-*) and writing in the seat 2026-09-22_seatC-18th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:6000 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          52853c8bf6c4 \
          8c2f7b3fd4fde915b2a24542bc32259b24e092a0 \
          8c2f7b3fd \
          04b05e093ad8 \
          3916eacd1 \
          4b251997a \
          c28f7a2f538c \
          a3becc4c37a9 \
          1b956c660f7c \
          'GO: merge #1167, #1168, #1169, #1171, #1173, #1175 batch' \
          fe51775add78 \
          13f5b691b1eb \
          b95f18d1247d \
          b60cb5694d73 \
          454c69ef63d9 \
          9cd0a3201aef \
          9f50c828743a \
          94f08cee8859 \
          c0fea7ac4cd9 \
          ff079c3c257b \
          bd8165896d17 \
          f6592e6d753e \
          772a70e4c193 \
          84de41765db4 \
          bca1d9500aa3 \
          966e055f901c \
          2e558148f061 \
          2539ed9b890df8a0 \
          6c3c562aca1c382d \
          8209b9bad1b67b4e \
          0033bb21c8c7a633 \
          0a768897c42fe375 \
          a51a7077f24bc4ad \
          d037aa38240fe479 \
          2daa85b8c046e74b \
          819988738b3714e0 \
          8ab9c06cd8e179d5 \
          ab13126212432b83 \
          ae6017a84cf7aff42e17e1fe06ed66032e513d8c \
          ae6017a84cf7 \
          f98e22a73561 \
          f888e8cd0bd1 \
          7bedc074583d \
          893879a19950 \
          20c8a088f5dc \
          710/710 \
          716/716 \
          714/714 \
          717/717 \
          715/715 \
          742/742 \
          '1008 insertions' \
          '15 deletions' \
          --pair-blob \
          'PAIR blob' \
          'alone blob' \
          RED-FIRST \
          GREEN-AFTER \
          A4 \
          A5 \
          code_patch \
          'PRODUCT BYTES' \
          '--recount --ignore-whitespace' \
          strict \
          section_1.diff \
          section_2.diff \
          'DEVELOP COVER' \
          cover-aware \
          PARITY \
          anchor-ambiguity \
          suggested_test_file \
          no-useless-assignment \
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
          typecheck18 \
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
          push-lock-18 \
          lock18.sh \
          push18.sh \
          series18.py \
          ATTRIBUTED \
          attrib18.json \
          attachmentsForURL \
          contributes \
          'linear[bot]' \
          measure18b \
          measure18.py \
          MG-10 \
          lockproof18 \
          a4titles \
          s2path \
          loadintermittent \
          batch_tampers18 \
          settingsdefaults \
          threehunks \
          ks-733 \
          ks871 \
          ks-1 \
          kksecura \
          'Seat B 18th' \
          merge18b.py \
          targets18.py \
          dry18.sh \
          go18.sh \
          postmerge18.py \
          --ruling \
          'cwd guard' \
          audit-baseline.json \
          KS-763 \
          KS-775 \
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
          KS-1230 \
          KS-1072 \
          KS-999 \
          KS-871 \
          KS-1227 \
          KS-1213 \
          KS-1073 \
          KS-1050 \
          KS-1204 \
          KS-1183 \
          KS-1018 \
          KS-1285 \
          KS-1031 \
          KS-1175 \
          KS-1250 \
          KS-1273 \
          KS-958 \
          KS-1185 \
          KS-1280 \
          KS-730 \
          KS-692 \
          KS-1118 \
          KS-1158 \
          KS-1265 \
          KS-1171 \
          KS-811 \
          KS-1188 \
          KS-1181 \
          'Refs KS-947' \
          'Refs KS-1123' \
          'Refs KS-1192' \
          'Refs KS-1231' \
          'Refs KS-1246' \
          'Refs KS-1257'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$ALL_OVER_PARENT" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF "$MERGE_BASE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-6 tree, the parent and the current develop in full, the NOT-PINNED section, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1167 is KS-947.' "$PROMPT_FILE" && grep -F '#1167' "$BRIEF" | grep -qF 'KS-947' && grep -qF 'PR #1168 is KS-1123.' "$PROMPT_FILE" && grep -F '#1168' "$BRIEF" | grep -qF 'KS-1123' && grep -qF 'PR #1169 is KS-1192.' "$PROMPT_FILE" && grep -F '#1169' "$BRIEF" | grep -qF 'KS-1192' && grep -qF 'PR #1171 is KS-1231.' "$PROMPT_FILE" && grep -F '#1171' "$BRIEF" | grep -qF 'KS-1231' && grep -qF 'PR #1173 is KS-1246.' "$PROMPT_FILE" && grep -F '#1173' "$BRIEF" | grep -qF 'KS-1246' && grep -qF 'PR #1175 is KS-1257.' "$PROMPT_FILE" && grep -F '#1175' "$BRIEF" | grep -qF 'KS-1257' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (PR #1167 is KS-947. … )" >&2; exit 32; }
grep -qF -- 'TIER AND ROUND' "$PROMPT_FILE" && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'outside __tests__` == the declared PRODUCT set' "$PROMPT_FILE" && grep -qF -- 'files API union 10' "$PROMPT_FILE" && grep -qF -- 'Any product byte OUTSIDE the declared set' "$PROMPT_FILE" && grep -qF -- 'STATE WHICH by the files API' "$PROMPT_FILE" && grep -qF -- 'a declared product byte the test does not prove red-first' "$PROMPT_FILE" && grep -qF -- 'TEST-FILE-ONLY / PRODUCT-AS-DECLARED:' "$PROMPT_FILE" && grep -qF -- 'the test file(s) exactly on' "$PROMPT_FILE" && grep -qF -- 'the declared product file(s) + test file(s) EXACTLY' "$PROMPT_FILE" && grep -qF -- 'name-status A ×5 / M ×6' "$PROMPT_FILE" && grep -qF -- 'nothing else moved on any PR' "$PROMPT_FILE" && grep -qF -- 'THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'TEN' "$PROMPT_FILE" && grep -qF -- 'exactly ONE PR pair overlapping' "$PROMPT_FILE" && grep -qF -- 'ZERO overlap with Seat B 18th' "$PROMPT_FILE" && grep -qF -- 'at least forward, exact reverse and one shuffle' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'state the SET you read and' "$PROMPT_FILE" && grep -qF -- 'the health.ts PAIR (#1171 + #1173) by real merges in BOTH' "$PROMPT_FILE" && grep -qF -- 'say which hunk each alone blob lacks' "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY, STRICT' "$PROMPT_FILE" && grep -qF -- 'the EIGHT section files' "$PROMPT_FILE" && grep -qF -- 'applied THREE ways' "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'The section `.opts` files are TWO lines' "$PROMPT_FILE" && grep -qF -- 'THE CELLS — two protocols' "$PROMPT_FILE" && grep -qF -- 'every declared cell + control' "$PROMPT_FILE" && grep -qF -- 'per-tamper' "$PROMPT_FILE" && grep -qF -- 'reds EXACTLY the declared set' "$PROMPT_FILE" && grep -qF -- 'tamper files restored by bytes' "$PROMPT_FILE" && grep -qF -- 'THE ANCHOR-AMBIGUITY ROWS' "$PROMPT_FILE" && grep -qF -- 'THE RED/GREEN PROTOCOL' "$PROMPT_FILE" && grep -qF -- 'head-minus-product' "$PROMPT_FILE" && grep -qF -- 'assert BOTH blobs after each step' "$PROMPT_FILE" && grep -qF -- 'MODIFY-IN-PLACE test' "$PROMPT_FILE" && grep -qF -- 'SECOND PIN' "$PROMPT_FILE" && grep -qF -- 'PER-FILE TYPECHECK DELTA 0' "$PROMPT_FILE" && grep -qF -- 'planted TS2322 control CAUGHT' "$PROMPT_FILE" && grep -qF -- 'a zero that needs its control' "$PROMPT_FILE" && grep -qF -- 'DELTA 0 with a PRE-EXISTING error' "$PROMPT_FILE" && grep -qF -- 'AND the THREE product files' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE v2 + the (b) ruling' "$PROMPT_FILE" && grep -qF -- 'against the ALLOW set' "$PROMPT_FILE" && grep -qF -- 'count BARE' "$PROMPT_FILE" && grep -qF -- 'census from the PRELOAD run' "$PROMPT_FILE" && grep -qF -- '`lsof -nP -iTCP:<port> -sTCP:LISTEN` before / after every run' "$PROMPT_FILE" && grep -qF -- 'login_stub cleared by PID' "$PROMPT_FILE" && grep -qF -- 'a FOURTH row would be a STOP' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'Backlog -> In Progress walks recorded' "$PROMPT_FILE" && grep -qF -- 'KS-1246 and KS-1257' "$PROMPT_FILE" && grep -qF -- 'assigned to the board login at item 0' "$PROMPT_FILE" && grep -qF -- 'EXCISION' "$PROMPT_FILE" && grep -qF -- 'RUN the scanner' "$PROMPT_FILE" && grep -qF -- 'no archived key in any branch' "$PROMPT_FILE" && grep -qF -- 'Recommend nothing' "$PROMPT_FILE" && grep -qF -- 'PR #1171 is KS-1231 (KS-1171 is Seat B' "$PROMPT_FILE" && grep -qF -- 'PR #1173 is KS-1246 (KS-1173 is a foreign' "$PROMPT_FILE" && grep -qF -- 'THE TWO-SEAT ARTEFACTS' "$PROMPT_FILE" && grep -qF -- 'INSIDE the push-window lock' "$PROMPT_FILE" && grep -qF -- 'grade present / absent + MONOTONIC' "$PROMPT_FILE" && grep -qF -- 'TWENTY-FIVE windows' "$PROMPT_FILE" && grep -qF -- 'the lock POLLS' "$PROMPT_FILE" && grep -qF -- 'THE MID-TAKE ARM (MG-10' "$PROMPT_FILE" && grep -qF -- 'attributions the seat made for Seat B' "$PROMPT_FILE" && grep -qF -- 'four-condition' "$PROMPT_FILE" && grep -qF -- 'ONLY tolerated state change' "$PROMPT_FILE" && grep -qF -- 'THE PROCESS-NAMESPACE RULE' "$PROMPT_FILE" && grep -qF -- 'THE COUNT-OBJECTS ACCOUNT' "$PROMPT_FILE" && grep -qF -- "THE SEAT'S OWN FINDINGS / SLIPS" "$PROMPT_FILE" && grep -qF -- 'CONFIRMED / REFUTED' "$PROMPT_FILE" && grep -qF -- 'the SECOND PINS' "$PROMPT_FILE" && grep -qF -- 'S1 the merge-tree in the shared checkout' "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST timeout under load 17' "$PROMPT_FILE" && grep -qF -- 're-run standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM — SIX lines VERBATIM' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER' "$PROMPT_FILE" && grep -qF -- 'ELEVEN targets over TEN paths' "$PROMPT_FILE" && grep -qF -- 'alone-tree reading' "$PROMPT_FILE" && grep -qF -- 'stays In Progress' "$PROMPT_FILE" && grep -qF -- 'SHIPS-WITH text ≤ 3 sentences each and KEY-FREE' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED rows NAMED' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED for its own' "$PROMPT_FILE" && grep -qF -- 'READ THE WHOLE TEST FILE before proposing a cell' "$PROMPT_FILE" && grep -qF -- 'sha256 + byte count IN the mail' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED written FIRST' "$PROMPT_FILE" && grep -qF -- 'the CONTEXT RULE: at ctx 80 write report.md' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4005 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:6000 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" && grep -qF -- 'NAMESPACE GUARD' "$PROMPT_FILE" && grep -qF -- 'SIX lines, one per PR' "$PROMPT_FILE" && grep -qF -- 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 (the KEY-SET rule' "$PROMPT_FILE" && grep -qF -- 'node_modules per ENTRY' "$PROMPT_FILE" && grep -qF -- 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF -- 'no memory maintenance' "$PROMPT_FILE" && grep -qF -- 'NEVER print a credential value' "$PROMPT_FILE" && grep -qF -- 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" && grep -qF -- 'NEVER touch the push-window lock directory' "$PROMPT_FILE" && grep -qF -- 'by ANCESTRY' "$PROMPT_FILE" && grep -qF -- 'never by a basename' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST' "$PROMPT_FILE" && grep -qF -- 'first act asserts' "$PROMPT_FILE" && grep -qF -- 'the END STATE is yours to name' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday twelve by-name items (tier/round; product-as-declared; the trees, the pair and the zero overlap; canonical identity strict; the cells with the red/green protocol; the per-file typecheck; the census rule; Linear hygiene; the two-seat artefacts; the seat findings/slips; the intermittents; the addendum) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present; the prompt is not PARTIAL"
  echo "  prompt carries TIER 1 on FOUR and each PR tier (#1167 T1, #1168 T2, #1169 T2, #1171 T1, #1173 T1, #1175 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name every pinned head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1148-#1166 PRIOR REPORT, the #1147-#1161 EARLIER REPORT, the #1036 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE, the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt carries the PAIR (--pair-blob, the pair blob in full, the alone blob)"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-c18-*, s-b18-*) and the seat 2026-09-22_seatC-18th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 / :4005 / :6000 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (192 tokens); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-6 tree, the parent and the current develop in full, the NOT-PINNED section and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each PR is"
  echo "  prompt carries Wednesday twelve by-name items and the standard closing (128 keywords)"
  [ -n "${QAB1167_CUR_DEV:-}" ] && echo "  (develop read from the QAB1167_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1167_BRIEF:-}${QAB1167_PROMPT:-}${QAB1167_HEAD_1175:-}${QAB1167_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
