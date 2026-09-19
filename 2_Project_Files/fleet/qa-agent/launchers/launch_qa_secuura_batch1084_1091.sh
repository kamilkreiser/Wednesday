#!/bin/bash
# launch_qa_secuura_batch1084_1091.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over EIGHT file-disjoint Secuura/Blockchain PRs
#   #1084 KS-1269 @ 946cdfd78  vc-issuer ks1269 vitest test: N71-1 (index null refused, /revoke + /unrevoke) + N71-2 (/revoke guard order)  — TIER 2 (test-only)
#   #1085 KS-1258 @ c3d9ca2e2  ks1248 vitest test: N77-1, the :576 degraded REQUIRED advice is EXACTLY the comment + one curl (allow-list)  — TIER 2 (test-only)
#   #1086 KS-1230 @ b0bcf733f  ks1230 vitest test: N80-1, nulls at 2 and 3 of four, and null LAST of three, stored as null            — TIER 2 (test-only)
#   #1087 KS-1206 @ d4658c021  ks1206 jest test: N81-1, rateLimit Infinity / " 100" / -0 refused 400 before the INSERT                   — TIER 2 (test-only)
#   #1088 KS-1062 @ 734a8f0bd  ks1062 vitest test: N79-2, two skipped counted; skipped-first keeps the loop (archived, NO Refs, NO key)   — TIER 2 (test-only)
#   #1089 KS-739  @ a64390edf  ks739 jest test: N82-1, a non-JSON 400 / 503 lookup maps to 400 / 502 (archived ticket, NO Refs, NO key)  — TIER 2 (test-only)
#   #1090 KS-1238 @ bd45f3b4f  ks1238 vitest test: N83-3, the recorder also sees /api/anchors/ — pins verification.ts:521 (RAW521)      — TIER 1 (AUTH, test-only)
#   #1091 KS-1238 @ dad4786c8  ks1215 vitest test: N83-5, a connector key is refused 403 on POST /api/platform/tenants (platform.ts:239)  — TIER 1 (AUTH, test-only)
# ALL EIGHT ARE TEST-ONLY: every changed path is under a src/__tests__/ directory (generator: local objects AND the PR files API; 0 product bytes;
# ZERO product bytes in #1090 and #1091 asserted by name).
# #1090's and #1091's verdicts carry the same ruling, KS-1238 COMPLETE or NOT-COMPLETE; KS-1238 stays in Backlog regardless (this batch never moves
# it to Done) and the gate gives its corrected facts-comment text.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too, and two PRs share KS-1238; the READY mail AND the prompt must BOTH state which ticket
# each of the eight PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. EIGHT verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 21:55:59 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop ba1210afc; compare develop...head = merge_base ba1210afc, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (8 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL EIGHT = tree f76901ed9,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains in THREE orders:
# forward, reverse, shuffled with the tier-1 heads first), equal to the builder's prediction and to its local octopus commit 1f11437af's tree. All
# eight are byte-identical to their CANONICAL local-model patch.diff, re-applied strict by the generator in a plain scratch dir (#1084 = two runs, in
# BOTH orders; each run alone differs), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — THIRTY-SIX paths by blob at the CURRENT develop: the 8 PR files (all at develop blobs; any PR's head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: verification.ts (RAW521 / :598 / :1297), platform.ts (:239 / :222 / :254),
# system-status.ts, startup-migrations.ts, admin.ts, proxy.ts, auth.ts, index.ts, vc-issuer status.ts, adminConfig.ts, documents.ts, preflight.sh,
# run-shell-suites.sh, the pre-push hook, the api-gateway / originate / vc-issuer configs, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway / originate / vc-issuer src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md, the seat's READY mail (11:53:21Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the eight heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all eight heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and EIGHT verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1077-#1083 batch), the EARLIER REPORT (the #1070-#1076 batch) and
#          NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'The 3 skipped legs need a stack', 'login_stub',
#          'mergeable_state: unstable' and 'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-6th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (ruleset 18499832, the order-independence tree e9fc521fb, the six plant
#          sha256s of the line-pinned anchors, RAW521 and its sha 2c7f6a3dbdef, TENANTSORGPROV / TENANTSUNGUARDED, --listFilesOnly, the N71 blobs
#          bb8801cfb463 / 394337283ec1, db.retry.test.ts), and the prompt must ask the gate to MEASURE, not conclude, and to rule KS-1238
#          COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-eight tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the eight, which ticket the PR is (PR #1084 is KS-1269 ... PR #1091 is KS-1238).
# exit 33: the prompt must carry Wednesday's BY-NAME items: KS-1238's comment 18580369, ZERO product bytes in #1090 and #1091, the NON-RULED
#          /unrevoke -1 rule (the gate must not recommend pinning -1 either way), the tsc --listFilesOnly finding, and the PRIOR REPORT's row format.
# QAB1084_CUR_DEV (test override, --check only): stands in for origin develop. QAB1084_HEAD_1091 (test override): stands in for #1091's pinned head.
# QAB1084_VERIFTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/verification.ts (its git blob).
# A launch with any QAB1084_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1084to1091/gen_launcher_batch1084_1091.py from launch_qa_secuura_batch1077_1083.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-eight tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1084_1091.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1084_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md}"
PROMPT_FILE="${QAB1084_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-19_secuura-batch1084-1091.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (11:53:21Z) and re-read by the drafter (git ls-remote 21:55:59 AEST, branch AND refs/pull/N/head)
# NAMESPACE TRAP: no PR here is its own-numbered ticket, and #1090 and #1091 share KS-1238; the ticket column is the truth (exit 32)
PRS=(
  "1084|KS-1269|refs/heads/feature/ks-1269-post-apistatusidrevoke-accepts-index-object-where-integer-is-n71|946cdfd7801e0994d7f5e8847397aaf1c0d13677"
  "1085|KS-1258|refs/heads/feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n77-1|c3d9ca2e2ccd6402eeb8456a1b577b0609df019b"
  "1086|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n80-1|b0bcf733f316083fe661facab6a11d024600c497"
  "1087|KS-1206|refs/heads/feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an-n81-1|d4658c0211a214f476bcf79470957e0f50317275"
  "1088|KS-1062|refs/heads/feature/pin-startup-migrations-skipped-tenants-counted-loop-continues|734a8f0bd1b1cd420c09ee35a2e736b2a6fb832e"
  "1089|KS-739|refs/heads/feature/pin-transfer-custody-nonjson-400-503-lookup|a64390edf791e5c52a841cdb63397a33893af2f9"
  "1090|KS-1238|refs/heads/feature/ks-1238-n83-3-pin-anchor-store-forward-sends-no-caller-bearer|bd45f3b4f02789a55f9d6f81d061ae4dd21f02d0"
  "1091|KS-1238|refs/heads/feature/ks-1238-n83-5-pin-platform-tenants-refuses-a-connector-key|${QAB1084_HEAD_1091:-dad4786c8e3e0616cc8785c901997b4fbe1f7287}"
)
DEVELOP_SHA='ba1210afcab7ddf127cccb270b1c341360261cee'   # the pin = develop at 21:55:59 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1084-1091-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1077-1083-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1084to1091/mail_batch1084_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The eight heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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
# develop...head = ba1210afc ahead 1 for all eight PRs; files 1 each
# (git diff --name-only + rev-list, drafter 21:5x AEST; the launcher reads the compare API).
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
WANT_COMPARE="1084 $MERGE_BASE ahead=1 files=1
1085 $MERGE_BASE ahead=1 files=1
1086 $MERGE_BASE ahead=1 files=1
1087 $MERGE_BASE ahead=1 files=1
1088 $MERGE_BASE ahead=1 files=1
1089 $MERGE_BASE ahead=1 files=1
1090 $MERGE_BASE ahead=1 files=1
1091 $MERGE_BASE ahead=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirty-six paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1084_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
V = D + "services/vc-issuer/"
VERIFTS = A + "src/routes/verification.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  V + "src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts":    ({"bb8801cfb463758b3765ad015382906e4191d627": DV}, {"2741189ec51271c4b206ae680bea75acb79638f1": "#1084 own"}),
  A + "src/__tests__/ks1248-n-1-system-status-troubleshooting-marks.test.ts":      ({"57b5fdc453bf1feb6a6af6c5a11dba2d477d08c5": DV}, {"ee9cecf62228810bbd4b3281f8fc6d68dddca7f4": "#1085 own"}),
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"069ad80eb125b52d94b475b9d8319c260016ef9f": DV}, {"6c048ec6a48116e296a23dc10a22a51a1c32da75": "#1086 own"}),
  O + "src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts":         ({"67edac0af3d9c491fcc5f0efc8e5eba225018005": DV}, {"d5154cb7b2fea379952d351e03895d47415f6c0b": "#1087 own"}),
  A + "src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts": ({"c7046d12d2fa1229911e25cf8fdcb2f8a1d53773": DV}, {"cebfc0d469bcb80bf7676dc90934cd81186af4f5": "#1088 own"}),
  O + "src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts":           ({"42e4af4860a54d0d87a5d2ec3f743606dc0c4b73": DV}, {"fc2a0f89e38ba9f931ed80aa3d084b2e4d0b700b": "#1089 own"}),
  A + "src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts":  ({"e3384324c6051ef70d6a16e3c15e08038f53a9d5": DV}, {"0a37c1d56be845f0d7658d9691a8978eb357d662": "#1090 own"}),
  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"7d14580b0a2c0f7967e578345e13f534d0919987": DV}, {"e2a4b12be53be4af7a16ec6a47a9b4c189c4ad99": "#1091 own"}),
  VERIFTS:                                                                         ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  A + "src/routes/platform.ts":                                                    ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  A + "src/routes/system-status.ts":                                               ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
  A + "src/startup-migrations.ts":                                                 ({"ed3e521426e75910c5bf2cf07e7251f2fd8ef538": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  A + "src/routes/proxy.ts":                                                       ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  A + "src/middleware/auth.ts":                                                    ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  A + "src/index.ts":                                                              ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {}),
  V + "src/routes/status.ts":                                                      ({"394337283ec19e77a10d1b25b8c5cc2b978fb52e": DV}, {}),
  O + "src/routes/adminConfig.ts":                                                 ({"62af28d017069d38fa00e7915bfa65226db678c6": DV}, {}),
  O + "src/routes/documents.ts":                                                   ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {}),
  D + "scripts/preflight/preflight.sh":                                            ({"712f895362e2c8d1ead6fd09ac257d7bce212948": DV}, {}),
  D + "scripts/run-shell-suites.sh":                                               ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  ".githooks/pre-push":                                                            ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  A + "package.json":                                                              ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                          ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  A + "tsconfig.json":                                                             ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  O + "package.json":                                                              ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  O + "jest.config.js":                                                            ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                             ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  V + "package.json":                                                              ({"27888b6eeb6c20b44af947d14eddb3bccf6293cf": DV}, {}),
  V + "package-lock.json":                                                         ({"b0b66b5018e556731056875d4c1720945e3478e7": DV}, {}),
  V + "vitest.config.ts":                                                          ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  V + "tsconfig.json":                                                             ({"b3546b85f68847a2cd62ad74f10f5f7347579bc5": DV}, {}),
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1084_VERIFTS_FILE", "") if f == VERIFTS else ""
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all eight heads: each merged tree = its head tree, a fast-forward: #1084 e9fc521fb, #1085 b904e7243, #1086 8f3df5a64, #1087 6c3dfead8, #1088 56a40abab, #1089 bab87a37e, #1090 95ecc81a8, #1091 4a4802bb7; all eight together f76901ed9cfae15ce6580ff24ebcbbea22bd36fb, drafter tree-hash and three-order scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)
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
           A + "tsconfig.json",
           O + "src/",
           O + "package.json",
           O + "jest.config.js",
           O + "tsconfig.json",
           V + "src/",
           V + "package.json",
           V + "package-lock.json",
           V + "vitest.config.ts",
           V + "tsconfig.json",
           D + "packages/shared/src/",
           D + "scripts/",
           ".githooks/",
           D + "package.json",
           D + "package-lock.json",
           D + "eslint.config.mjs",
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
tail = "the gate merges the then-current develop onto EACH of the eight heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all eight f76901ed9) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway, originate and vc-issuer src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1084 KS-1269: TIER 2' "$PROMPT_FILE" && grep -qF '#1085 KS-1258: TIER 2' "$PROMPT_FILE" && grep -qF '#1086 KS-1230: TIER 2' "$PROMPT_FILE" && grep -qF '#1087 KS-1206: TIER 2' "$PROMPT_FILE" && grep -qF '#1088 KS-1062: TIER 2' "$PROMPT_FILE" && grep -qF '#1089 KS-739: TIER 2' "$PROMPT_FILE" && grep -qF '#1090 KS-1238: TIER 1' "$PROMPT_FILE" && grep -qF '#1091 KS-1238: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1090 + #1091 T1, #1084-#1089 T2)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the seat's READY mail capture path" >&2; exit 9; }
for _pr in "${PRS[@]}"; do
  IFS='|' read -r _n _t _br _h <<< "$_pr"
  grep -qF "$_h" "$PROMPT_FILE" && grep -qF "$_h" "$BRIEF" \
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
grep -qF '[QA -> Wednesday] BATCH GATE #1084-#1091 (eight PRs; tier 1 = #1090 + #1091 KS-1238)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'EIGHT lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and EIGHT verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'The 3 skipped legs need a stack' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$PROMPT_FILE" \
  && grep -qF 'The 3 skipped legs need a stack' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: The 3 skipped legs need a stack / login_stub / mergeable_state: unstable / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-6th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-6th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF -- '18499832' "$PROMPT_FILE" && grep -qF -- '18499832' "$BRIEF" && grep -qF -- 'e9fc521fbfb72dab46b751ee215e76268efffab7' "$PROMPT_FILE" && grep -qF -- 'e9fc521fbfb72dab46b751ee215e76268efffab7' "$BRIEF" && grep -qF -- 'fa9573ff4f16' "$PROMPT_FILE" && grep -qF -- 'fa9573ff4f16' "$BRIEF" && grep -qF -- 'ab8cf42a9e96' "$PROMPT_FILE" && grep -qF -- 'ab8cf42a9e96' "$BRIEF" && grep -qF -- '95c52eeb088d' "$PROMPT_FILE" && grep -qF -- '95c52eeb088d' "$BRIEF" && grep -qF -- 'aa66a0aa4555' "$PROMPT_FILE" && grep -qF -- 'aa66a0aa4555' "$BRIEF" && grep -qF -- 'c3a3e6140e5d' "$PROMPT_FILE" && grep -qF -- 'c3a3e6140e5d' "$BRIEF" && grep -qF -- '1db9dd398a46' "$PROMPT_FILE" && grep -qF -- '1db9dd398a46' "$BRIEF" && grep -qF -- '2c7f6a3dbdef' "$PROMPT_FILE" && grep -qF -- '2c7f6a3dbdef' "$BRIEF" && grep -qF -- 'RAW521' "$PROMPT_FILE" && grep -qF -- 'RAW521' "$BRIEF" && grep -qF -- 'TENANTSORGPROV' "$PROMPT_FILE" && grep -qF -- 'TENANTSORGPROV' "$BRIEF" && grep -qF -- 'TENANTSUNGUARDED' "$PROMPT_FILE" && grep -qF -- 'TENANTSUNGUARDED' "$BRIEF" && grep -qF -- '--listFilesOnly' "$PROMPT_FILE" && grep -qF -- '--listFilesOnly' "$BRIEF" && grep -qF -- 'bb8801cfb463' "$PROMPT_FILE" && grep -qF -- 'bb8801cfb463' "$BRIEF" && grep -qF -- '394337283ec1' "$PROMPT_FILE" && grep -qF -- '394337283ec1' "$BRIEF" && grep -qF -- 'db.retry.test.ts' "$PROMPT_FILE" && grep -qF -- 'db.retry.test.ts' "$BRIEF" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items 1-10, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF 'f76901ed9cfae15ce6580ff24ebcbbea22bd36fb' "$PROMPT_FILE" && grep -qF '1f11437afc21cad6a77fbf75030444fd845e17c4' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-eight tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1084 is KS-1269.' "$PROMPT_FILE" && grep -qF '| #1084 | KS-1269' "$BRIEF" && grep -qF 'PR #1085 is KS-1258.' "$PROMPT_FILE" && grep -qF '| #1085 | KS-1258' "$BRIEF" && grep -qF 'PR #1086 is KS-1230.' "$PROMPT_FILE" && grep -qF '| #1086 | KS-1230' "$BRIEF" && grep -qF 'PR #1087 is KS-1206.' "$PROMPT_FILE" && grep -qF '| #1087 | KS-1206' "$BRIEF" && grep -qF 'PR #1088 is KS-1062.' "$PROMPT_FILE" && grep -qF '| #1088 | KS-1062' "$BRIEF" && grep -qF 'PR #1089 is KS-739.' "$PROMPT_FILE" && grep -qF '| #1089 | KS-739' "$BRIEF" && grep -qF 'PR #1090 is KS-1238.' "$PROMPT_FILE" && grep -qF '| #1090 | KS-1238' "$BRIEF" && grep -qF 'PR #1091 is KS-1238.' "$PROMPT_FILE" && grep -qF '| #1091 | KS-1238' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket each PR is (PR #1084 is KS-1269 ... PR #1090 and PR #1091 are KS-1238) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
grep -qF -- '18580369' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes in #1090 and #1091' "$PROMPT_FILE" && grep -qF -- 'NON-RULED' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning -1 either way' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'CORRECTED FACTS-COMMENT TEXT' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday's by-name items (KS-1238 comment 18580369 and the corrected facts text, ZERO product bytes in #1090 and #1091, the NON-RULED /unrevoke -1 rule, the PRIOR REPORT's row format)" >&2; exit 33; }
grep -qF -- '--listFilesOnly' "$PROMPT_FILE" && grep -qF -- '--listFilesOnly' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the tsc --listFilesOnly finding (by-name item 5)" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  eight heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1090 + #1091 T1, #1084-#1089 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all eight heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, EIGHT verdict lines"
  echo "  prompt names the report directory, the #1077-#1083 batch PRIOR REPORT, the EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: The 3 skipped legs need a stack / login_stub / mergeable_state: unstable / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-6th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-eight tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket each of the eight PRs is (namespace trap; #1090 and #1091 both KS-1238)"
  echo "  prompt carries Wednesday's by-name items: 18580369 + corrected facts text, ZERO product bytes in #1090 and #1091, NON-RULED -1, --listFilesOnly, the row format"
  [ -n "${QAB1084_CUR_DEV:-}" ] && echo "  (develop read from the QAB1084_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1084_VERIFTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/verification.ts read from the QAB1084_VERIFTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1084_BRIEF:-}${QAB1084_PROMPT:-}${QAB1084_HEAD_1091:-}${QAB1084_CUR_DEV:-}${QAB1084_VERIFTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
