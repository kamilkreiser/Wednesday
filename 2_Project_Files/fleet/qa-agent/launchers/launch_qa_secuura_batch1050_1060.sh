#!/bin/bash
# launch_qa_secuura_batch1050_1060.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over ELEVEN file-disjoint Secuura/Blockchain PRs
#   #1050 KS-1261 @ 6f6c6ed30  preflight.sh: FAILED_LEGS / fail_total initialised (the pre-push gate everyone runs) + new suite  — TIER 2 (runtime)
#   #1051 KS-1136 @ 58e2fb66b  Testing/jobs/04-container-trivy.sh: a failed per-image scan is scan-failed and exits 1 + suite  — TIER 2 (runtime)
#   #1052 KS-1267 @ cd791b821  ks1228 jest test: Q1, /version row after saveDocument                                         — TIER 2 (test-only)
#   #1053 KS-1258 @ baf651460  ks1258 vitest test: N44-1, no start command in any shape                                      — TIER 2 (test-only)
#   #1054 KS-1230 @ 1ea5c7b7e  ks1230 vitest test: N45-5, a null allow-list stores 200                                       — TIER 2 (test-only)
#   #1055 KS-1202 @ 31d55923d  ks1202 jest test: N-B, legacy matching shape + case-exact documentType                         — TIER 2 (test-only)
#   #1056 KS-1153 @ 7eb4dbad5  run_code_guards.test.sh: R-918-A, the advisory-skip arm (applied --recount)                   — TIER 2 (test-only)
#   #1057 KS-1209 @ b3b90db4d  preflight_verdict_names_real_failures.test.sh: N41-3, a real leg-1 failure is named           — TIER 2 (test-only)
#   #1058 KS-1134 @ 2e212047d  orchestrate_jobs.test.sh: zero Stage-1 jobs reach the JOIN                                    — TIER 2 (test-only)
#   #1059 KS-1172+KS-1173 @ f22ec785e  note / certified / verified in the anchored lifecycle vocabulary + yaml (3 commits)     — TIER 1 (sets the floor)
#   #1060 KS-1264 @ 3743e57ea  documents.ts /revoke: record the provenance row only after updateDocument                     — TIER 1
# Batched under Kam's 09:22 rule. ELEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 07:59:10 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: ten PRs are ONE commit
# whose parent IS develop 59412d057; #1059 is THREE (8a1bdf1df verbatim / 1a3e27ee5 titles / f22ec785e yaml); compare develop...head = merge_base
# 59412d057, ahead 1 (x10) / 3, files 2/2/1/1/1/1/1/1/1/6/2 (asserted per PR, exit 10). Pairwise file-disjoint (19 files). Each PR over develop is a
# fast-forward (merged tree = head tree). ALL ELEVEN = tree cb7860d61, re-derived by the generator by pure tree hashing (no git write), equal to the
# builder's prediction and to its local predict commit 23c379dcd's tree. All eleven are byte-identical to their CANONICAL local-model patches
# (#1059 at 8a1bdf1df), re-applied by the generator in a plain scratch dir; #1056's --recount controlled (a strict apply gives another blob).
#
# The develop pin is judged by CONTENT — FORTY-FIVE paths by blob at the CURRENT develop: the nineteen PR files (sixteen at develop blobs, three new
# files ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the pre-push hook, run-shell-suites.sh,
# run-code-guards.sh, jobs/09 + ci/orchestrate.sh + ci/aggregate.ts, generate-openapi.ts, both openapi sources, certifications.ts, provenance.ts,
# system-status.ts, admin.ts, the originate / anchoring / api-gateway configs, the Dev package.json + lock, eslint.config.mjs and BACKLOG.md.
# GUARDED: scripts/, Testing/jobs/ + ci/, docs/, api-gateway / originate / anchoring src/ + config, the Dev package.json + lock, eslint.config.mjs,
# .githooks/, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md, the seat's READY mail (21:56:17Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the eleven heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all eleven heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and ELEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1042-#1045 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 were skipped', 'login_stub' and 'threadTokenMint'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-2nd history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's G1 / G2 / G3 (documents.ts:2327, :2051, 09-aggregate-report), and the prompt must
#          ask the gate to MEASURE, not conclude.
# exit 31: the prompt must name the all-eleven tree in full, the predict commit, the NOT-PINNED list, and pin preflight's GATEWAY_URL to loopback.
# QAB1050_CUR_DEV (test override, --check only): stands in for origin develop. QAB1050_HEAD_1060 (test override): stands in for #1060's pinned head.
# QAB1050_DOCS_FILE (test fixture, --check only): a local file stands in for develop services/originate/src/routes/documents.ts (its git blob).
# A launch with any QAB1050_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1050to1060/gen_launcher_batch1050_1060.py from launch_qa_secuura_batch1042_1045.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-eleven tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1050_1060.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..31 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1050_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md}"
PROMPT_FILE="${QAB1050_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-19_secuura-batch1050-1060.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (21:56:17Z) and re-read by the drafter (git ls-remote 07:59:10 AEST, branch AND refs/pull/N/head)
PRS=(
  "1050|KS-1261|refs/heads/feature/ks-1261-preflight-failed_legs-fail_total-are-never-initialised-so-an|6f6c6ed306f35aea0ca4f1e51fb785d8b1cf77b8"
  "1051|KS-1136|refs/heads/feature/ks-1136-audit-jobs-a-per-image-trivy-failure-reads-as-a-clean-image|58e2fb66bd5ed5138f700cd58433e82e25ba9b82"
  "1052|KS-1267|refs/heads/feature/ks-1267-ks-1228-two-row-placements-are-unpinned-versions-row-after|cd791b8214999427b645364e666ca215dc4e7c39"
  "1053|KS-1258|refs/heads/feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n44-1|baf651460a46dff3c5bd52e19ab3f64e681ab6df"
  "1054|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n45-5|1ea5c7b7eb955d146d935447572e28d8f48a12cf"
  "1055|KS-1202|refs/heads/feature/ks-1202-the-served-document-type-comes-from-datadocumenttype-which-n-b|31d55923d35669959413aba8e533661282608e18"
  "1056|KS-1153|refs/heads/feature/ks-1153-l7-gate-records-918924925-run-code-guardssh-check-unreached|7eb4dbad51958c0c814a77e3263b54a84b1d0edc"
  "1057|KS-1209|refs/heads/feature/ks-1209-preflights-closing-verdict-says-a-run-failed-on-the-n41-3|b3b90db4d19818ed580cbc98a199a5f145e7f064"
  "1058|KS-1134|refs/heads/feature/ks-1134-orchestrate_jobs-cell-1415-cannot-tell-the-ks-922-fix-from-a|2e212047d66d15ca8551e8fdd9d4ea772d5ab085"
  "1059|KS-1172+KS-1173|refs/heads/feature/ks-1172-add-note-and-verified-to-the-lifecycle-vocabulary|f22ec785ea0dcc620e0e4bf53987a0da7a03e104"
  "1060|KS-1264|refs/heads/feature/ks-1264-revoke-records-its-action_provenance-row-before|${QAB1050_HEAD_1060:-3743e57eac6050056df87cbfc8724ae642d1ff6c}"
)
DEVELOP_SHA='59412d0575dff3243f5f0ccd1e50608ddb920d6c'   # the pin = develop at 07:59:10 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-batch1042-1045-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1050to1060/mail_batch1050_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The eleven heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
HEADS_NOTE=""
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  _lsr="$(git -C "$REPO" ls-remote origin "$_br" "refs/pull/$_n/head")"
  if ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]${_br}\$" || ! printf '%s\n' "$_lsr" | grep -q "^${_h}[[:space:]]refs/pull/${_n}/head\$"; then
    echo "REFUSING: #$_n $_t — $_h is not at $_br AND refs/pull/$_n/head on origin — that head moved; a verdict is valid ONLY at its head" >&2
    printf '%s\n' "$_lsr" >&2
    exit 6
  fi
  HEADS_NOTE="$HEADS_NOTE #$_n@${_h:0:9}"
done

# The compare (GitHub compare API) per PR, asserted whole (merge_base + ahead + files; NOT behind — develop is expected to move):
# develop...head = 59412d057 ahead 1 for ten PRs, ahead 3 for #1059; files #1050 2, #1051 2, #1052-#1058 1 each, #1059 6, #1060 2
# (git diff --name-only + rev-list, drafter 07:5x AEST; the launcher reads the compare API).
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  PRS_FLAT="${PRS[*]}" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
for pr in os.environ["PRS_FLAT"].split():
    n, tk, br, h = pr.split("|")
    r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + h, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
    c = json.load(r)
    print("%s %s ahead=%d files=%d" % (n, c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compares develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="1050 $MERGE_BASE ahead=1 files=2
1051 $MERGE_BASE ahead=1 files=2
1052 $MERGE_BASE ahead=1 files=1
1053 $MERGE_BASE ahead=1 files=1
1054 $MERGE_BASE ahead=1 files=1
1055 $MERGE_BASE ahead=1 files=1
1056 $MERGE_BASE ahead=1 files=1
1057 $MERGE_BASE ahead=1 files=1
1058 $MERGE_BASE ahead=1 files=1
1059 $MERGE_BASE ahead=3 files=6
1060 $MERGE_BASE ahead=1 files=2"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): forty-five paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1050_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import hashlib, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
def raw(path, ref):
    return urllib.request.urlopen(urllib.request.Request(api + "/contents/" + path + "?ref=" + ref, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github.raw"}), timeout=60).read().decode("utf-8")
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
A = D + "services/api-gateway/"
O = D + "services/originate/"
N = D + "services/anchoring/"
T = "Blockchain/Testing/"
DOCSTS = O + "src/routes/documents.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  D + "scripts/preflight/preflight.sh":                                            ({"f24fa96316b64f1b06b6a78835f4385fcd753e7b": DV}, {"539493d9d94942189e85953512d6f3981bd9c5d4": "#1050 own"}),
  T + "jobs/04-container-trivy.sh":                                                ({"4312a79f5292ed3a4cab07e0486dd2fd1dbe4763": DV}, {"88444463f9d42a3ee4ad8f8b5ca24123ae678fb6": "#1051 own"}),
  O + "src/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts":   ({"0b9be16318b97d1a214afcfdd5a1c0483c27904e": DV}, {"ae43c82f8c299e6278f3473a07ff0c606ed083cb": "#1052 own"}),
  A + "src/__tests__/ks1258-degraded-optional-service-advice.test.ts":             ({"9143365cb4571906f6d0c2df13db430645447c72": DV}, {"fe456997603256f1036499a8a8f33949f43631bf": "#1053 own"}),
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"dd5ce85644dde844833989ad482288bf855e3d23": DV}, {"26af52344bcdbc5de5ba592e97fabc2608718738": "#1054 own"}),
  O + "src/__tests__/ks1202-a-mismatched-data-documenttype-is-refused.test.ts":    ({"ada07f0536ad003754cb2a08f514fc04f8996b27": DV}, {"16ac8db994ad85ea3fbdf22adc7348c70f3d635d": "#1055 own"}),
  D + "scripts/__tests__/run_code_guards.test.sh":                                 ({"55a376f769e078ceeeadc25d026364c0e06961b1": DV}, {"c5125fe3c9cc34e07f254990bb40ffbdcb035028": "#1056 own"}),
  D + "scripts/__tests__/preflight_verdict_names_real_failures.test.sh":           ({"a3d5efe68e350710e2bde8b01c21b298dcca446f": DV}, {"fb762f6389a0700afcab456fc275062cace05520": "#1057 own"}),
  D + "scripts/__tests__/orchestrate_jobs.test.sh":                                ({"a9abe5bcefd0969e79f07ba186f3f6647f88fadc": DV}, {"4653bc8a1d4abd080db26ce03c33434beac16896": "#1058 own"}),
  D + "docs/VOCABULARY.md":                                                        ({"482544b9dc7dda652b5e7ac0452c35c8c035359f": DV}, {"cc4093b0b992621a651c21ac9a4cb6cee9425515": "#1059 own"}),
  D + "docs/openapi/secuura-api.yaml":                                             ({"16ac8aa78463849864fa6285e20c9946c027fb7b": DV}, {"a34b59363b81dc3f69cc11a238ff9369deefa9d9": "#1059 own"}),
  N + "src/__tests__/anchorSchema.test.ts":                                        ({"ff85c737628b8fc20e3b1faad6adfcc92c8dfd06": DV}, {"c1a3e865a101f865f045ef3dfa8252b266ad04d3": "#1059 own"}),
  N + "src/anchorSchema.ts":                                                       ({"67ae9d907f4e8a0ad405067af82c6b7308075f1b": DV}, {"8341c8221b5008b5f6a0a6a6d7887198f71b02f5": "#1059 own"}),
  O + "src/__tests__/lifecycleEventRepo.test.ts":                                  ({"4e53a82966d82da0b29eddd49eb101575c387347": DV}, {"994abf9ffd17a59acdcabedff4b2db8e5e1423fb": "#1059 own"}),
  O + "src/lifecycleActions.ts":                                                   ({"4ac5ad58a22b565d267512b734b09b9bf1b1d844": DV}, {"aa1c8434d5a55ad035e1ee62755ace7379af69fb": "#1059 own"}),
  DOCSTS:                                                                          ({"b5e76dc61ae5d4da8667b466b0a1dcf79d5a0498": DV}, {"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": "#1060 own"}),
  ".githooks/pre-push":                                                            ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  D + "scripts/run-shell-suites.sh":                                               ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  D + "scripts/run-code-guards.sh":                                                ({"2f06e19d3d33d649d7229e44ade8a35c0df3a0db": DV}, {}),
  T + "jobs/09-aggregate-report.sh":                                               ({"739ebab8c64e5f9195bc2280e38b4cc5fea0e023": DV}, {}),
  T + "ci/orchestrate.sh":                                                         ({"65247243f7585951ada3e5dfa8a9af88189ee5b1": DV}, {}),
  T + "ci/aggregate.ts":                                                           ({"b841f02572247da7a1d0a29f69f9c3231636991c": DV}, {}),
  D + "scripts/generate-openapi.ts":                                               ({"e84acdc9e1be073751fcd6a8bb95504e23688019": DV}, {}),
  O + "src/originate.openapi.ts":                                                  ({"2d1b48a0c7ea93521d553cc28ccb53b4fe3fd19c": DV}, {}),
  N + "src/anchoring.openapi.ts":                                                  ({"29c089bb0abcd65d42fe8fca2d6beaff0368fa98": DV}, {}),
  O + "src/routes/certifications.ts":                                              ({"02dcbe6294b497eab093f11a8fc6c9e275be91c5": DV}, {}),
  O + "src/services/provenance.ts":                                                ({"483aa9eb331d2caa5af285e20d9668a9dbcd92a6": DV}, {}),
  A + "src/routes/system-status.ts":                                               ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  O + "package.json":                                                              ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  O + "jest.config.js":                                                            ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                             ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  N + "package.json":                                                              ({"a7eed73550b40aa2d968872817fa22e933373831": DV}, {}),
  N + "package-lock.json":                                                         ({"7ef3f65a35b48bec2591df4b2859bab9aa237334": DV}, {}),
  N + "vitest.config.ts":                                                          ({"2e1d21f130f8aa80a1c71987f920181dafaf6b90": DV}, {}),
  N + "tsconfig.json":                                                             ({"f593300cac7c9c3073f15a1287323cf5b9dd478d": DV}, {}),
  A + "package.json":                                                              ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                          ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
  D + "scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh":             ({"ABSENT": DV}, {"819ca90240aae6310758d0c5ea2733c3eec3f1b3": "#1051 own"}),
  D + "scripts/__tests__/preflight_state_is_initialised.test.sh":                  ({"ABSENT": DV}, {"ee31ee5f5bc3f0e4939df9587e346296b8ea494c": "#1050 own"}),
  O + "src/__tests__/ks1264-revoke-records-its-action-provenance-row.test.ts":     ({"ABSENT": DV}, {"2043effc18923455dba72d6db8238a65ca815efa": "#1060 own"}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1050_DOCS_FILE", "") if f == DOCSTS else ""
    try:
        if fixture:
            data = open(fixture, "rb").read()
            blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        else:
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all eleven heads: each merged tree = its head tree, a fast-forward: #1050 a84e8df57, #1051 137cc4ff4, #1052 454a870ee, #1053 5902a257a, #1054 544f6dd76, #1055 08b3b219b, #1056 d9a1c04a2, #1057 72fcf4a47, #1058 7fabec16e, #1059 93c05c640, #1060 841f00564; all eleven together cb7860d61b27cc41aa5865d850f2424884d1b8e0, drafter tree-hash = builder prediction; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A + "src/",
           A + "package.json",
           A + "vitest.config.ts",
           O + "src/",
           O + "package.json",
           O + "jest.config.js",
           O + "tsconfig.json",
           N + "src/",
           N + "package.json",
           N + "package-lock.json",
           N + "vitest.config.ts",
           N + "tsconfig.json",
           D + "scripts/",
           D + "docs/",
           T + "jobs/",
           T + "ci/",
           D + "package.json",
           D + "package-lock.json",
           D + "eslint.config.mjs",
           ".githooks/",
           "BACKLOG.md"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this batch; any GUARDED move refuses: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h]) or h in content_cleared)
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto EACH of the eleven heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all eleven cb7860d61) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway, originate and anchoring src/ + config, scripts/, docs/, Testing jobs/ + ci/, the Dev package.json + lock, eslint.config.mjs, .githooks/, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1050 KS-1261: TIER 2' "$PROMPT_FILE" && grep -qF '#1051 KS-1136: TIER 2' "$PROMPT_FILE" && grep -qF '#1052 KS-1267: TIER 2' "$PROMPT_FILE" && grep -qF '#1053 KS-1258: TIER 2' "$PROMPT_FILE" && grep -qF '#1054 KS-1230: TIER 2' "$PROMPT_FILE" && grep -qF '#1055 KS-1202: TIER 2' "$PROMPT_FILE" && grep -qF '#1056 KS-1153: TIER 2' "$PROMPT_FILE" && grep -qF '#1057 KS-1209: TIER 2' "$PROMPT_FILE" && grep -qF '#1058 KS-1134: TIER 2' "$PROMPT_FILE" && grep -qF '#1059 KS-1172+KS-1173: TIER 1' "$PROMPT_FILE" && grep -qF '#1060 KS-1264: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1050-#1058 T2, #1059 T1, #1060 T1)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat's READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "${_h:0:9}" "$BRIEF" \
    || { echo "REFUSING: the READY mail or the prompt does not name #$_n's head $_h — a gate about another SHA is another gate" >&2; exit 20; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1050-#1060 (eleven PRs; tier 1 = #1059 KS-1172+KS-1173, #1060 KS-1264)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'ELEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and ELEVEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 were skipped' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'threadTokenMint' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 were skipped' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'threadTokenMint' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 were skipped / login_stub / threadTokenMint" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-2nd/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-2nd history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'documents.ts:2327' "$PROMPT_FILE" && grep -qF ':2051' "$PROMPT_FILE" && grep -qF '09-aggregate-report' "$PROMPT_FILE" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" \
  && grep -qF 'documents.ts:2327' "$BRIEF" && grep -qF ':2051' "$BRIEF" && grep -qF '09-aggregate-report' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry G1 / G2 / G3, or the prompt does not say MEASURE, not conclude" >&2; exit 30; }
grep -qF 'cb7860d61b27cc41aa5865d850f2424884d1b8e0' "$PROMPT_FILE" && grep -qF '23c379dcd' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-eleven tree in full, the predict commit, the NOT-PINNED list, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  eleven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1050-#1058 T2, #1059 T1, #1060 T1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all eleven heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, ELEVEN verdict lines"
  echo "  prompt names the report directory, the #1042-#1045 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 were skipped / login_stub / threadTokenMint"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-2nd history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry G1 / G2 / G3; the prompt says MEASURE, not conclude"
  echo "  prompt names the all-eleven tree, the predict commit, the NOT-PINNED list and a loopback GATEWAY_URL for preflight"
  [ -n "${QAB1050_CUR_DEV:-}" ] && echo "  (develop read from the QAB1050_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1050_DOCS_FILE:-}" ] && echo "  (develop services/originate/src/routes/documents.ts read from the QAB1050_DOCS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1050_BRIEF:-}${QAB1050_PROMPT:-}${QAB1050_HEAD_1060:-}${QAB1050_CUR_DEV:-}${QAB1050_DOCS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
