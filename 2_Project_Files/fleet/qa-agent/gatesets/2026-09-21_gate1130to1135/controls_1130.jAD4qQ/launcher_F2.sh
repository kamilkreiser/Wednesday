#!/bin/bash
# launch_qa_secuura_batch1130-1135.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SIX Secuura/Blockchain PRs
# (Seat B 14th; seven local-model patches grouped by FILE SET into six PRs across THREE lanes — five file-disjoint plus ONE same-file pair)
#   #1130 PR 1 KS-1273 @ 7c3cc821f  scripts BASH suite (MODIFY): TRIVYYAMLEXITCODE-1 (+8/-1, the suite's own trivy stub + one cell) — TIER 2, pushed FIRST
#   #1131 PR 2 KS-1135 @ d897f5318  systemTest BASH suite (MODIFY): MANIFESTQUARANTINESTDERR-1 (+1/-1, cleanup() diagnostic, NO cell) — TIER 2
#   #1132 PR 6 KS-958 @ 39bbf29a5  bash_patch: the round's ONLY PRODUCT bytes on Blockchain/Dev/scripts/check-shared-relink.sh (-2/+2, a PUSH GUARD) + one NEW suite (+84) — TIER 1 (pushed THIRD)
#   #1133 PR 3 KS-880 @ 0fd2a7f0d  security VITEST test: OTHERMAPPERDEFAULT-1 (+8, rowToAuditLog) — TIER 1
#   #1134 PR 5 KS-887 @ d7439346d  security VITEST test: KS-887 modify-in-place of PR 3's OWN file (+5/-1, the WRITE-half cell) — TIER 1 (after PR 3, same file)
#   #1135 PR 4 KS-1236 + KS-1006 @ 1c7c01afe  auth VITEST test: ALREADYPENDING-1 + MFANOTENABLED-1 (+32, one file, two READYs, two tickets) — TIER 1, pushed LAST
# FIVE are TEST-ONLY and #1132 carries EXACTLY the two paths (files API + local diff --raw: 6 paths, 5 under __tests__/ + the guard, +140/-5,
# 5 M + 1 A — generator-asserted by numstat; the guard and the manifest suite are mode 100755).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the six heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR blobs by diff --raw; the six head trees (= the trees over develop: each head's parent IS develop, a fast-forward)
# and the all-six tree by REAL 3-way merges in a --shared scratch clone in SIX orders (predict_batch_scratch_*.out) AND by pure tree hashing in the
# generator (the PAIR blob dcd3efaaf45a on the shared ks869 file); every BOTH-list token asserted present in the READY capture and the prompt.
# MG-1 / MG-2 / MG-3 THIS ROUND: targets15.py wants exactly ONE equality target PER PR FILE (1/1/2/1/1/1) and parses the list non-greedily
# to the FIRST `;` (targets15.py:28) — the #1132 addendum line carries TWO targets COMMA-separated (exit 25); merge15.py:54-:65
# asserts each squash body's key set == the PR's OWN Refs set (two keys on #1135 only).
# Batched under Kam 2026-09-18 standing rule. SIX verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming each head, under Kam TESTED grant (exit 26). All seven tickets stay where they are (In Progress; bot-walked or already).
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + six refs/pull/N/head + six branches; rev-list --parents; diff --raw): each
# head is ONE commit whose parent IS origin develop 9f0265eb0 (tree 23d60cace7c3, the #1119-#1128 batch landed) — NO develop move under these
# heads, so each PR over develop is a fast-forward (merged tree = head tree); compare develop...head = merge_base 9f0265eb0, ahead 1, BEHIND 0,
# files 1/1/2/1/1/1 (exit 10 — a squash on develop changes `behind` and REFUSES: re-pin deliberately). Pairwise file-disjoint EXCEPT the PR 3 / PR 5
# pair on ks869-connector-id-persisted.test.ts (disjoint hunks; both orders one blob dcd3efaaf45a). ALL SIX over 9f0265eb0 =
# 60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b, identical in every order tried; the PAIR alone 9e5dec6aef2070de26d1450c961f531572ee8f57.
#
# The develop pin is judged by CONTENT — THIRTY-THREE paths by blob at the CURRENT develop: the 6 PR paths (5 at develop blobs, 1 ABSENT; any at
# a head blob or at the PAIR blob -> exit 19 LANDED, naming the PR), the 4 other tamper files (the trivy job, manifest.ts, security index.ts,
# users.ts), and what the gate runs or reads: the six bash siblings, run-shell-suites.sh, preflight.sh, run-code-guards.sh, fix-libsodium-symlink.js,
# the pre-push hook, security's and auth's package.json / config / tsconfig / lock, auth index.ts, packages/shared's, the Dev package.json + lock,
# eslint.config.mjs.
# GUARDED: security/ + auth/ src + config, packages/shared, scripts/, systemTest/, .githooks/, Blockchain/Testing/jobs/, the Dev package.json + lock,
# eslint.config.mjs.
#
# SOURCE = gatesets/2026-09-21_gate1130to1135/mail_batch1130_ready.md, the seat's SIX READY mails (08:56:14Z … ) + the 09:24:08Z CORRECTION to
# READY 5 + the 08:33:52Z STATUS mail + the 08:00:58Z plan-confirmation mail + the 08:43:18Z PR 1 leg-14 QUESTION mail, each captured verbatim by
# message id from wednesday-agent@ and combined in PR push order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line (#1130 T2, #1131 T2, #1132 T1, #1133 T1, #1134 T1, #1135 T1).
# exit 10: the compare per PR (merge_base 9f0265eb0, ahead 1, behind 0, files) — develop moving off the pin refuses here.
# exit 18/19: the develop pin judged by content (above).
# exit 20: the READY capture AND the prompt must name all six heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SIX verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1119-#1128), the EARLIER REPORT (#1112-#1118), the OLDER REPORT
#          (#1106-#1111) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (TWO for #1132, comma-separated),
#          the `## MERGE ADDENDUM` heading targets15.py parses from report.md, the MG-3 key-set rule and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', '12/15', 'SKIPPED', 'login_stub',
#          'mergeable_state', 'skips are not a pass'.
# exit 28: the prompt must forbid entering any seat worktree (s-b14-*) and writing in the seat 2026-09-21_seatB-14th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201), and the :4003 / :4004 discipline.
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, develop and its tree, the six head trees, the
#          all-six tree, the pair tree + blob, the seven head blobs, the 8 plant sha256s, the 8 tamper ids, the suite counts, the S6 words, the
#          --recount / golden words, the NO PREFLIGHT VERDICT words, the :5432 words, the archived and foreign keys, the GO subject, the
#          CORRECTION), and the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the all-six tree in full, develop in full, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the six, which ticket(s) the PR is (PR #1130 is KS-1273. … PR #1135 is KS-1236 + KS-1006.).
# exit 33: the prompt must carry Wednesday SEVENTEEN BY-NAME items, each by its own keywords (the ladder below), and the standard closing.
# QAB1130_CUR_DEV (test override, --check only): stands in for origin develop. QAB1130_HEAD_1135 (test override): stands in for #1135 pinned head.
# QAB1130_BRIEF / QAB1130_PROMPT (test overrides): stand in for the READY capture / the prompt. A launch with any QAB1130_* override set refuses (exit 16).
#
# Generated by gatesets/2026-09-21_gate1130to1135/gen_launcher_1130.py (pins re-read from origin + local objects + tree hashing + BOTH-list +
# by-name ladder + output controls + heredoc parity + bash -n) in the shape of gen_launcher_1119.py.
#
# Usage: launch_qa_secuura_batch1130-1135.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1130_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/mail_batch1130_ready.md}"
PROMPT_FILE="${QAB1130_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-21_secuura-batch1130-1135.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket(s)|branch|head|files — pinned from the seat READYs and re-read by the generator (git ls-remote, branch AND refs/pull/N/head; local objects)
PRS=(
  "1130|KS-1273|refs/heads/feature/ks-1273-job-04-a-trivy_exit_code-or-trivyyaml-exit-code-in-the-trivyyamlexitcode-1|7c3cc821f2fdd63d96e30689cc9477472a843ce0|1"
  "1131|KS-1135|refs/heads/feature/ks-1135-run-shell-suitessh-fails-6-of-25-suites-under-a-long-tmpdir-manifestquarantinestderr-1|d897f531876b33c9b4f2e118e3aea08b23e5344d|1"
  "1132|KS-958|refs/heads/feature/ks-958-the-re-link-guard-matches-the-js-runtime-name-case-1|39bbf29a564fcc6b68ffe50607e29df251b8b180|2"
  "1133|KS-880|refs/heads/feature/ks-880-quarantine-or-reconcile-the-dead-converters-copy-a-second-othermapperdefault-1|0fd2a7f0d3990329567e2ae6532babab0f0d250a|1"
  "1134|KS-887|refs/heads/feature/ks-887-test-defect-mine-the-write-half-column-list-pin-can-modifyinplace-1|d7439346d1c489162584c64937ea91d66cb28984|1"
  "1135|KS-1236+KS-1006|refs/heads/feature/ks-1236-approving-a-stale-pending-verification-request-after-the-alreadypending-mfanotenabled-1|${QAB1130_HEAD_1135:-1c7c01afe589f1ba07e70106dc1cf019dba14a00}|1"
)
DEVELOP_SHA='9f0265eb06ecf24d4de18149ce862ad2330a61ee'   # the pin = origin develop at generation = every head's parent (no develop move this round)
MERGE_BASE='9f0265eb06ecf24d4de18149ce862ad2330a61ee'    # every head's parent = merge-base = develop itself
ALL_OVER_DEV='60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b'     # all six over the pin 9f0265eb0 (real 3-way, six orders; generator tree-hash with the pair blob) — the tree that matters for the merge
PAIR_TREE='9e5dec6aef2070de26d1450c961f531572ee8f57'      # PR 3 + PR 5 both orders over the pin
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1130-1135-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1112-1118-tier1-r1/'
OLDER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1106-1111-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-21_gate1130to1135/mail_batch1130_ready.md"

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

# The compare (GitHub compare API) per PR, asserted whole INCLUDING behind: develop...head = merge_base 9f0265eb0, ahead 1, behind 0 (no develop
# move), files 1/1/2/1/1/1 (generator, rev-list --left-right; the launcher reads the compare API). A develop move changes behind -> exit 10.
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
WANT_COMPARE="1130 $MERGE_BASE ahead=1 behind=0 files=1
1131 $MERGE_BASE ahead=1 behind=1 files=1
1132 $MERGE_BASE ahead=1 behind=0 files=2
1133 $MERGE_BASE ahead=1 behind=0 files=1
1134 $MERGE_BASE ahead=1 behind=0 files=1
1135 $MERGE_BASE ahead=1 behind=0 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read (develop moved off the pin, or a head moved)" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1130_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
S = D + "services/security/"
AU = D + "services/auth/"
SC = D + "scripts/"
P = D + "packages/shared/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the one NEW suite)
JUDGED = {
  "Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh":                               ({"d119e64ba755e41e41d719d03ded24f79f297e04": DV}, {"fa63512f6fc234b061c2d7352fabd0124d9b6f89": "#1130 own"}),
  "systemTest/__tests__/manifest_quarantine.test.sh":                                                                    ({"2ae67f244ddd6e38b4a2b72255d101216cf30314": DV}, {"8d21c7e127bb97220df90997bb560bcf29dd89cf": "#1131 own"}),
  "Blockchain/Dev/scripts/__tests__/check_shared_relink_case.test.sh":                                                   ({"ABSENT": DV}, {"9a16088ca5e3c9043cf82ec54f26204e516e62f9": "#1132 own"}),
  "Blockchain/Dev/scripts/check-shared-relink.sh":                                                                       ({"d41c79538503d6d31e2037b3f49e025ed38f2870": DV}, {"4e0704b6c7b9f4db2ceebf0530015e3b2f469662": "#1132 own"}),
  "Blockchain/Dev/services/security/src/__tests__/ks869-connector-id-persisted.test.ts":                                 ({"f452db039b9dceb34bebd5046525de1e42b1879e": DV}, {"789dff0cde0b54d4ecbdf83ead67cd897a5326ee": "#1133 own", "f796e9527537a786ed17ef12bdf433b96d1dda8a": "#1134 own", "dcd3efaaf45a26bb4324b656ef62e79685462600": "#1133 + #1134 (the pair)"}),
  "Blockchain/Dev/services/auth/src/__tests__/ks1194-a-failed-verification-request-save-is-never-acknowledged.test.ts":  ({"bfa8b1d3fc3611ad04266d9e520848958f2a4b55": DV}, {"5273baafd36714a30403b1bdf55cd2318acc587c": "#1135 own"}),
  "Blockchain/Testing/jobs/04-container-trivy.sh":                                                                       ({"6dfc5731e56ede5e5a6f420cccd92874b7566a87": DV}, {}),
  "systemTest/fixtures/manifest.ts":                                                                                     ({"a6bfe3e7662791866e16c04331ba8fdc473a535a": DV}, {}),
  "Blockchain/Dev/services/security/src/index.ts":                                                                       ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  "Blockchain/Dev/services/auth/src/routes/users.ts":                                                                    ({"3bfa47dcde0125d9e23cb8a9fbddf7bd40aa0b2d": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh":                                               ({"35bbb4519950f77188ad30f3f1d46683ac63ddf5": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh":                                        ({"819ca90240aae6310758d0c5ea2733c3eec3f1b3": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh":                                                        ({"867ce728ab4aab4022befddc9cf5fa5e6df439ba": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/check_shared_relink_tooling_tokens.test.sh":                                         ({"fdb125ca3e6ae4516836c4c12ac88e5b34b2ca46": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh":                                                ({"89c89fef831f6c877587eb26920dbb8de8ef750b": DV}, {}),
  "Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh":                                                             ({"5ad0541313589635c6c100677cf14fb02d00be78": DV}, {}),
  "Blockchain/Dev/scripts/run-shell-suites.sh":                                                                          ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                                                       ({"fe29676b7073d4b6b9a71d492de962777cf5bdf8": DV}, {}),
  "Blockchain/Dev/scripts/fix-libsodium-symlink.js":                                                                     ({"526e024c2c107bb46ec9328c7de6687d4b8b7367": DV}, {}),
  "Blockchain/Dev/scripts/run-code-guards.sh":                                                                           ({"2f06e19d3d33d649d7229e44ade8a35c0df3a0db": DV}, {}),
  ".githooks/pre-push":                                                                                                  ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/services/security/package.json":                                                                       ({"a2f2e03ff75b5aba19a9aac97a827cb7a6c50aba": DV}, {}),
  "Blockchain/Dev/services/security/vitest.config.ts":                                                                   ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  "Blockchain/Dev/services/security/tsconfig.json":                                                                      ({"2e8767d5f1e12fe1969b74c8d02d7f1b094e52c7": DV}, {}),
  "Blockchain/Dev/services/security/package-lock.json":                                                                  ({"2675691235597a521c8952a5058df29203b4eb8c": DV}, {}),
  "Blockchain/Dev/services/auth/package.json":                                                                           ({"814e88419470b811f26f1593984071bb317608d8": DV}, {}),
  "Blockchain/Dev/services/auth/vitest.config.ts":                                                                       ({"8bb96293a0f11a14d90e7c7893f32a053277bbdb": DV}, {}),
  "Blockchain/Dev/services/auth/tsconfig.json":                                                                          ({"a7952bdeaf16e933432bb0e7136f484bb7288a40": DV}, {}),
  "Blockchain/Dev/services/auth/package-lock.json":                                                                      ({"2d91a356aa8426304dc291e0090dbd6893d53c00": DV}, {}),
  "Blockchain/Dev/services/auth/src/index.ts":                                                                           ({"edabbf87182311241662b20ac71d7244e923b5a3": DV}, {}),
  "Blockchain/Dev/packages/shared/package.json":                                                                         ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  "Blockchain/Dev/packages/shared/vitest.config.ts":                                                                     ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  "Blockchain/Dev/packages/shared/tsconfig.json":                                                                        ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (every head parent; every head a fast-forward over it; all six together " + all_over_dev + " in six orders, generator tree-hash + scratch-clone 3-way; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [S + "src/", S + "package.json", S + "vitest.config.ts", S + "tsconfig.json", S + "package-lock.json",
           AU + "src/", AU + "package.json", AU + "vitest.config.ts", AU + "tsconfig.json", AU + "package-lock.json",
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
tail = "the gate merges the then-current develop onto EACH of the six heads in its own clones, names each merged-tree OID and re-runs each PR items and suites on it and on the all-six tree"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list; %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (gen_launcher_1130.py DEV / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1130 KS-1273: TIER 2' "$PROMPT_FILE" && grep -qF '#1131 KS-1135: TIER 2' "$PROMPT_FILE" && grep -qF '#1132 KS-958: TIER 1' "$PROMPT_FILE" && grep -qF '#1133 KS-880: TIER 1' "$PROMPT_FILE" && grep -qF '#1134 KS-887: TIER 1' "$PROMPT_FILE" && grep -qF '#1135 KS-1236 + KS-1006: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1130 T2, #1131 T2, #1132 T1, #1133 T1, #1134 T1, #1135 T1)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1130-#1135 (six PRs; tier 1 = #1132, #1133, #1134, #1135)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SIX lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SIX verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$OLDER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the OLDER REPORT $OLDER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1132 TWO' "$PROMPT_FILE" && grep -qF 'COMMA-separated' "$PROMPT_FILE" && grep -qF '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'MG-3 KEY-SET' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1132 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
for _w in 'PREFLIGHT INCOMPLETE' '12/15' 'SKIPPED' 'login_stub' 'mergeable_state' 'skips are not a pass'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass (first miss: $_w)" >&2; exit 27; }
done
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-b14-batch' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-21_seatB-14th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-b14-*) and writing in the seat 2026-09-21_seatB-14th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener ended by pid with a census (KS-1201) and the :4003 / :4004 discipline" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 \
          60bd96e7078c41bbd71b3e0d7e15f815f70b0b1b \
          23d60cace7c3 \
          9f0265eb06ecf24d4de18149ce862ad2330a61ee \
          cecbb9a62653 \
          9e5dec6aef20 \
          dcd3efaaf45a \
          6eeef3623e8a \
          ff4427e75a4dbc62943b23dd6e1e8560ccd13ce0 \
          2088fe31d9ffd6ee8b0693ca3c5d73fbc8d59233 \
          c531a4e6bb680fd91b8b1795552aa8890759fb61 \
          2fba2bc1c6157476a3287de7d6cf061946b3c894 \
          8af100d484836ea87081767b64299c4416e889c6 \
          009a8116db0d18dfb63d3357220a478d09c2b49e \
          fa63512f6fc2 \
          8d21c7e127bb \
          4e0704b6c7b9 \
          9a16088ca5e3 \
          789dff0cde0b \
          f796e9527537 \
          5273baafd367 \
          0720a4bfa4a4 \
          f38ad737419a \
          e461d3795550 \
          cbc37764f051 \
          e2b088f924d6 \
          67e4f8b38833 \
          e417c05bf5d0 \
          c97ddc96b6ab \
          EXITCODEFLAGGONE \
          DRIVERTHROWS \
          AUDITTENANTRAW \
          GUARDTOLOG \
          SAMETARGETONLY \
          MFAOFFIDEMPOTENT \
          LENGTHDROPPED \
          CONNECTORIDDROPPED \
          216/216 \
          786/786 \
          215/215 \
          782/782 \
          '6 ok / 0 FAIL' \
          '5 ok / 0 FAIL' \
          '3 ok / 0 FAIL' \
          '14 ok / 0 FAIL' \
          '3 ok / 2 FAIL' \
          '3 ok / 3 FAIL' \
          '7 ok / 7 FAIL' \
          '2 passed, 4 failed, 0 skipped' \
          '6 passed, 0 failed, 0 skipped' \
          '106 passed, 0 failed' \
          '56 passed, 0 failed' \
          '27 passed, 0 failed (of 27 cells)' \
          '43 passed, 0 failed (of 43)' \
          '44 passed, 0 failed (of 44)' \
          '42 passed, 1 failed (of 43)' \
          'PREFLIGHT INCOMPLETE' \
          12/15 \
          SKIPPED \
          'skips are not a pass' \
          login_stub \
          mergeable_state \
          'stubs=4' \
          'NO PREFLIGHT VERDICT' \
          'ran NO legs' \
          PROTOCOL-DIFF \
          PROTOCOL-CLEAN \
          'packages/shared is not built' \
          ks949_main_seed_idempotence \
          deps15b \
          S6 \
          --recount \
          'corrupt patch at line 7' \
          golden \
          85a7a98230b4 \
          87bb65f6f302 \
          'driver stderr (tail -40 of driver.err' \
          wrapModuleLoad \
          'KS-1135 tamper: the quarantine aborted for a September stamp' \
          'npm_config_offline=true' \
          'tsx v4.23.15' \
          section_1 \
          section_2 \
          'patch failed' \
          'tolower(L)' \
          'expected exit 1, got 0' \
          'NODE_ENV=production' \
          'latent, closed' \
          'push guard' \
          '--directory=Blockchain/Dev' \
          'does not exist in index' \
          'connector_id)' \
          'WRITE half' \
          COALESCE \
          ks-869 \
          'flag > env > config' \
          TRIVY_EXIT_CODE \
          '--exit-code 0' \
          trivy.yaml \
          'CRITICAL=1 HIGH=1' \
          'could not scan' \
          rowToAuditLog \
          rowToApiKey \
          DEFAULT_TENANT \
          TS2322 \
          typecheck15 \
          eslint \
          'linear[bot]' \
          attachmentsForURL \
          contributes \
          'Refs KS-1006' \
          'Refs KS-1236' \
          :5432 \
          127.0.0.1 \
          netlog.cjs \
          'STOP-class 0' \
          jq \
          /bin/bash \
          'bash -n' \
          shellcheck \
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
          KS-869 \
          KS-1194 \
          KS-1136 \
          KS-1137 \
          KS-957 \
          KS-930 \
          KS-969 \
          KS-973 \
          KS-1203 \
          KS-1198 \
          KS-1284 \
          KS-1175 \
          KS-1215 \
          KS-753 \
          KS-1232 \
          KS-1223 \
          KS-1234 \
          KS-1283 \
          KS-1244 \
          KS-1275 \
          KS-1279 \
          KS-1272 \
          KS-741 \
          KS-1260 \
          KS-1209 \
          KS-953 \
          'Nothing failed' \
          '<= 92 chars' \
          'Deviation from verbatim' \
          'GO: merge #1130-#1135 batch' \
          unrendered \
          CORRECTION \
          TRIVYYAMLEXITCODE-1 \
          MANIFESTQUARANTINESTDERR-1 \
          OTHERMAPPERDEFAULT-1 \
          ALREADYPENDING-1 \
          MFANOTENABLED-1 \
          KS-958 \
          KS-887; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the intermittents" >&2; exit 30; }
grep -qF "$ALL_OVER_DEV" "$PROMPT_FILE" && grep -qF "$PAIR_TREE" "$PROMPT_FILE" && grep -qF "$DEVELOP_SHA" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-six tree, the pair tree and develop in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1130 is KS-1273.' "$PROMPT_FILE" && grep -F '#1130' "$BRIEF" | grep -qF 'KS-1273' && grep -qF 'PR #1131 is KS-1135.' "$PROMPT_FILE" && grep -F '#1131' "$BRIEF" | grep -qF 'KS-1135' && grep -qF 'PR #1132 is KS-958.' "$PROMPT_FILE" && grep -F '#1132' "$BRIEF" | grep -qF 'KS-958' && grep -qF 'PR #1133 is KS-880.' "$PROMPT_FILE" && grep -F '#1133' "$BRIEF" | grep -qF 'KS-880' && grep -qF 'PR #1134 is KS-887.' "$PROMPT_FILE" && grep -F '#1134' "$BRIEF" | grep -qF 'KS-887' && grep -qF 'PR #1135 is KS-1236 + KS-1006.' "$PROMPT_FILE" && grep -F '#1135' "$BRIEF" | grep -qF 'KS-1236' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket(s) each PR is (PR #1130 is KS-1273. … PR #1135 is KS-1236 + KS-1006.)" >&2; exit 32; }
grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes on FIVE' "$PROMPT_FILE" && grep -qF -- 'EXACTLY the two paths on #1132' "$PROMPT_FILE" && grep -qF -- 'files API union 6' "$PROMPT_FILE" && grep -qF -- 'DISJOINTNESS AND THE TREES, RE-DERIVED' "$PROMPT_FILE" && grep -qF -- 'at least forward and exact reverse' "$PROMPT_FILE" && grep -qF -- 'read-tree back to develop' "$PROMPT_FILE" && grep -qF -- 'fast-forward = its head tree' "$PROMPT_FILE" && grep -qF -- 'every count from the RUNNER' "$PROMPT_FILE" && grep -qF -- 'the PAIR needs its own proof' "$PROMPT_FILE" && grep -qF -- 'CANONICAL-PATCH IDENTITY' "$PROMPT_FILE" && grep -qF -- 'both roads, both rcs quoted' "$PROMPT_FILE" && grep -qF -- 'the two recheck sections in both orders' "$PROMPT_FILE" && grep -qF -- 'Name any byte that differs' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST PER PR UNDER THE COVER RULE' "$PROMPT_FILE" && grep -qF -- 'DEVELOP COVER measured FIRST' "$PROMPT_FILE" && grep -qF -- 'reds == declared ∪ measured cover' "$PROMPT_FILE" && grep -qF -- '7/7 by exact-line-block AND raw-substring' "$PROMPT_FILE" && grep -qF -- 'TWO-line blocks' "$PROMPT_FILE" && grep -qF -- 'THE TWO-READY FRAME' "$PROMPT_FILE" && grep -qF -- 'RED-FIRST / GREEN-AFTER' "$PROMPT_FILE" && grep -qF -- 'THE PRODUCT BYTES GRADED ON THEIR OWN' "$PROMPT_FILE" && grep -qF -- 'THE PRODUCT BYTES:' "$PROMPT_FILE" && grep -qF -- 'preflight LEG 13' "$PROMPT_FILE" && grep -qF -- 'SHARED_RELINK_STRICT=1' "$PROMPT_FILE" && grep -qF -- 'mode 100644 vs the 15 executable siblings' "$PROMPT_FILE" && grep -qF -- 'completeness detector fires 0/1/0' "$PROMPT_FILE" && grep -qF -- 'THE OTHER MAPPER' "$PROMPT_FILE" && grep -qF -- 'THIRDMAPPERDEFAULT' "$PROMPT_FILE" && grep -qF -- 'rowToAuditLog(` at :374' "$PROMPT_FILE" && grep -qF -- 'THE WRITE-HALF CELL, MODIFY-IN-PLACE' "$PROMPT_FILE" && grep -qF -- 'A2 needed --recount' "$PROMPT_FILE" && grep -qF -- 'SAME-FILE PAIR' "$PROMPT_FILE" && grep -qF -- "Kam's own ticket" "$PROMPT_FILE" && grep -qF -- 'THE AUTH GUARDS' "$PROMPT_FILE" && grep -qF -- 'two drives, one cell' "$PROMPT_FILE" && grep -qF -- 'STALEAPPROVALPATH / FALSYMFASECRETDOOR' "$PROMPT_FILE" && grep -qF -- "auth's FIRST census set" "$PROMPT_FILE" && grep -qF -- "THE STUB'S trivy.yaml ARM" "$PROMPT_FILE" && grep -qF -- 'which trivy' "$PROMPT_FILE" && grep -qF -- 'the `jq` FATAL control' "$PROMPT_FILE" && grep -qF -- 'REALTRIVYCONFIGARM' "$PROMPT_FILE" && grep -qF -- 'THE DIAGNOSTIC AND THE UNGATED PUSH' "$PROMPT_FILE" && grep -qF -- 'NO PREFLIGHT VERDICT on its push' "$PROMPT_FILE" && grep -qF -- 'design or a gap' "$PROMPT_FILE" && grep -qF -- 'SYSTEMTESTPUSHUNGATED' "$PROMPT_FILE" && grep -qF -- 'THE INTERMITTENTS' "$PROMPT_FILE" && grep -qF -- 're-run it standalone 3× serial' "$PROMPT_FILE" && grep -qF -- 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" && grep -qF -- 'one finding, two or three' "$PROMPT_FILE" && grep -qF -- 'THE CONNECTION CENSUS' "$PROMPT_FILE" && grep -qF -- '30 vs 10' "$PROMPT_FILE" && grep -qF -- ':4003 / :4004 / :4005 / :4006' "$PROMPT_FILE" && grep -qF -- 'LINEAR LINK HYGIENE' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'KS-1129' "$PROMPT_FILE" && grep -qF -- 'KS-1137' "$PROMPT_FILE" && grep -qF -- 'Completes KS-1273' "$PROMPT_FILE" && grep -qF -- 'recommend nothing' "$PROMPT_FILE" && grep -qF -- 'PR #887 is OPEN and is KS-961' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'proposed cell' "$PROMPT_FILE" && grep -qF -- "local model's next round" "$PROMPT_FILE" && grep -qF -- 'BY DESIGN' "$PROMPT_FILE" && grep -qF -- 'FOUR prior rows CLOSE here' "$PROMPT_FILE" && grep -qF -- 'ONE MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF -- 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF -- '#1132 TWO' "$PROMPT_FILE" && grep -qF -- 'COMMA-separated' "$PROMPT_FILE" && grep -qF -- '## MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF -- 'MG-3 KEY-SET' "$PROMPT_FILE" && grep -qF -- 'merge15.py:58' "$PROMPT_FILE" && grep -qF -- "THE PAIR'S ADDENDUM" "$PROMPT_FILE" && grep -qF -- 'THE LINE-NUMBER DISCIPLINE' "$PROMPT_FILE" && grep -qF -- 'NAME WHO INHERITED IT' "$PROMPT_FILE" && grep -qF -- '"FOR THE GATE TO MEASURE" ITEMS map onto the above' "$PROMPT_FILE" && grep -qF -- 'the commit subjects <= 92 chars' "$PROMPT_FILE" && grep -qF -- 'THE CENSUS RULE, THE NAMESPACE GUARD AND report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- '"port":5432,' "$PROMPT_FILE" && grep -qF -- 'KS-1135 = PR 2' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors <n> / Minors <m>' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'GRADE THE HEADS' "$PROMPT_FILE" && grep -qF -- 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF -- 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF -- 'WRITE report.md BEFORE THE MAIL' "$PROMPT_FILE" && grep -qF -- 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF -- 'TCP LISTEN census' "$PROMPT_FILE" && grep -qF -- 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4003 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:4004 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'lsof -nP -iTCP:5432 -sTCP:LISTEN' "$PROMPT_FILE" && grep -qF -- 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday seventeen by-name items (tier/round/product bytes; the trees, the pair and disjointness; canonical-patch identity; red-first under the cover rule with the two declared covers and PR 4 frame; #1132 the product bytes; #1133 the other mapper; #1134 the write-half cell; #1135 the auth guards; #1130 the stub; #1131 the diagnostic + the ungated push; the intermittents; census; link hygiene incl. KS-1129..KS-1137; NOT-PINNED format incl. BY DESIGN; addendum per PR comma-separated under ## MERGE ADDENDUM + MG-3 + the pair + the line-number discipline; the seat items; the census/namespace/report.md restatement) or the standard closing" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  six heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR (merge_base + ahead + behind + files):"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1130 T2, #1131 T2, #1132 T1, #1133 T1, #1134 T1, #1135 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all six heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SIX verdict lines"
  echo "  prompt names the report directory, the #1119-#1128 PRIOR REPORT, the #1112-#1118 EARLIER REPORT, the #1106-#1111 OLDER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1132 TWO, comma-separated), the ## MERGE ADDENDUM heading, the MG-3 KEY-SET rule and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / 12/15 / SKIPPED / login_stub / mergeable_state / skips are not a pass"
  echo "  prompt forbids any seat worktree (s-b14-*) and the seat 2026-09-21_seatB-14th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201) and the :4003 / :4004 discipline"
  echo "  READY capture and prompt BOTH carry the seat items (176 tokens: develop + tree, six head trees, the all-six tree, the pair tree + blob, seven head blobs, 8 plant shas, 8 tamper ids, counts, S6, --recount/golden, NO PREFLIGHT VERDICT, :5432, archived + foreign keys, the GO subject, the CORRECTION); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the all-six tree, the pair tree and develop in full, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket(s) each of the six PRs is"
  echo "  prompt carries Wednesday seventeen by-name items and the standard closing (96 keywords)"
  [ -n "${QAB1130_CUR_DEV:-}" ] && echo "  (develop read from the QAB1130_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1130_BRIEF:-}${QAB1130_PROMPT:-}${QAB1130_HEAD_1135:-}${QAB1130_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
