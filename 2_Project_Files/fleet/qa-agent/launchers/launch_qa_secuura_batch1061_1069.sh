#!/bin/bash
# launch_qa_secuura_batch1061_1069.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over NINE file-disjoint Secuura/Blockchain PRs
#   #1061 KS-1206 @ 413cc5e80  adminConfig.ts: POST /api/admin/api-keys refuses rateLimit outside integer 1..10000 (null/0 -> 400) + test — TIER 1 (runtime)
#   #1062 KS-1260 @ b9497c698  preflight.sh: the early FAILED verdict keeps the legs-ran ratio (the pre-push gate) + new suite       — TIER 1 (runtime)
#   #1063 KS-1101 @ cd0a88e41  ks1101 vitest test: N-3, a degraded OPTIONAL service leaves /system/status operational          — TIER 2 (test-only)
#   #1064 KS-864  @ 7fd0f7d1e  NEW ks864d vitest test: R-1 row 17, an EMPTY portal env var falls back                           — TIER 2 (test-only)
#   #1065 KS-991  @ 3b46e2e14  NEW pre_push_hook_current_develop.test.sh: R-1, a CURRENT local develop is not called stale      — TIER 2 (test-only)
#   #1066 KS-739  @ 0c649c09b  ks739 jest test: F1, a non-JSON 403 still answers 403                                           — TIER 2 (test-only)
#   #1067 KS-1062 @ 48a8e12bb  NEW ks1062 vitest test: F-1, the tenant migration summary and the FIRST error                    — TIER 2 (test-only)
#   #1068 KS-1258 @ 9af88d99d  ks1258 vitest test: N53-1, no yarn / node start shape in the degraded optional advice             — TIER 2 (test-only)
#   #1069 KS-1230 @ 34406a29b  ks1230 vitest test: N54-1, a NULL allow-list is stored as null                                   — TIER 2 (test-only)
# NAMESPACE TRAP: PR #1062 is KS-1260 and PR #1067 is KS-1062 (exit 32).
# Batched under Kam's 09:22 rule. NINE verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 11:42:47 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop 3c447abc7; compare develop...head = merge_base 3c447abc7, ahead 1, files 2/2/1/1/1/1/1/1/1 (asserted per PR, exit 10).
# Pairwise file-disjoint (11 files, 5 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL NINE = tree 275cff9ff, re-derived by
# the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains, forward and reverse), equal to
# the builder's prediction and to its local octopus commit 77b7af584's tree. All nine are byte-identical to their CANONICAL local-model patches,
# re-applied by the generator in a plain scratch dir (#1061's sections with --directory=Blockchain/Dev, the rest strict).
#
# The develop pin is judged by CONTENT — THIRTY-SIX paths by blob at the CURRENT develop: the 11 PR files (six at develop blobs, five new files
# ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the pre-push hook, run-shell-suites.sh, the six
# preflight sibling suites, system-status.ts, admin.ts, startup-migrations.ts, documents.ts, the security service index.ts, the two systemTest
# callers of the mint route, the originate / api-gateway configs, the Dev package.json + lock, eslint.config.mjs and BACKLOG.md.
# GUARDED: api-gateway / originate src/ + config, security src/, scripts/, systemTest/schemathesis/, the Dev package.json + lock, eslint.config.mjs,
# .githooks/, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md, the seat's READY mail (01:39:55Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the nine heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all nine heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and NINE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1050-#1060 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 need a stack', 'login_stub' and 'mergeable_state: unstable'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-3rd history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's G-1 / G-2 / G-3 / G-4 (security/src/index.ts:569, Nothing failed, NOJSONCATCH at
#          1695, matches at 576), and the prompt must ask the gate to MEASURE, not conclude, and to execute the FAILED path itself.
# exit 31: the prompt must name the all-nine tree in full, the octopus commit, the NOT-PINNED list, and pin preflight's GATEWAY_URL to loopback.
# exit 32: the READY mail AND the prompt must BOTH name the namespace trap: 'PR #1062 is KS-1260' and 'PR #1067 is KS-1062'.
# QAB1061_CUR_DEV (test override, --check only): stands in for origin develop. QAB1061_HEAD_1069 (test override): stands in for #1069's pinned head.
# QAB1061_ADMINCFG_FILE (test fixture, --check only): a local file stands in for develop services/originate/src/routes/adminConfig.ts (its git blob).
# A launch with any QAB1061_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1061to1069/gen_launcher_batch1061_1069.py from launch_qa_secuura_batch1050_1060.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-nine tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1061_1069.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1061_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md}"
PROMPT_FILE="${QAB1061_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-19_secuura-batch1061-1069.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (01:39:55Z) and re-read by the drafter (git ls-remote 11:42:47 AEST, branch AND refs/pull/N/head)
# NAMESPACE TRAP: PR #1062 is KS-1260 and PR #1067 is KS-1062
PRS=(
  "1061|KS-1206|refs/heads/feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an|413cc5e80c8aab94c9b3058fbe0d49fbcfdaa540"
  "1062|KS-1260|refs/heads/feature/ks-1260-preflight-failure-verdict-keeps-the-ratio|b9497c69837d33d3c56562abfb9f9ac5c0dafa2b"
  "1063|KS-1101|refs/heads/feature/ks-1101-gateway-health-aggregates-read-anchorings-http-status-only-n-3|cd0a88e41ada8ddd927c3dc85f8270b52142f834"
  "1064|KS-864|refs/heads/feature/ks-864-dead-estate-pointers-in-runtime-source-outside-r-1|7fd0f7d1e560d85c789872eac96067b428215ed5"
  "1065|KS-991|refs/heads/feature/pin-pre-push-hook-current-develop-not-stale|3b46e2e14a2783bfe03df8919ca79d2dea21c043"
  "1066|KS-739|refs/heads/feature/pin-transfer-custody-nonjson-403-stays-403|0c649c09bca81ccb41ba791bb2a85ba29476c052"
  "1067|KS-1062|refs/heads/feature/pin-startup-migrations-tenant-summary-first-error|48a8e12bbb6b01d34bea55ab29936b033f8304b3"
  "1068|KS-1258|refs/heads/feature/ks-1258-systemstatus-tells-operators-to-start-the-service-locally-n53-1|9af88d99dbc0203a69cb765c67dee10df900e737"
  "1069|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n54-1|${QAB1061_HEAD_1069:-34406a29babe355a7ea8ecd916062da5b2fa8f85}"
)
DEVELOP_SHA='3c447abc7714e98fbba596aa1045b7bb47a6d215'   # the pin = develop at 11:42:47 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1050-1060-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1061to1069/mail_batch1061_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The nine heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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
# develop...head = 3c447abc7 ahead 1 for all nine PRs; files #1061 2, #1062 2, #1063-#1069 1 each
# (git diff --name-only + rev-list, drafter 11:4x AEST; the launcher reads the compare API).
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
WANT_COMPARE="1061 $MERGE_BASE ahead=1 files=2
1062 $MERGE_BASE ahead=1 files=2
1063 $MERGE_BASE ahead=1 files=1
1064 $MERGE_BASE ahead=1 files=1
1065 $MERGE_BASE ahead=1 files=1
1066 $MERGE_BASE ahead=1 files=1
1067 $MERGE_BASE ahead=1 files=1
1068 $MERGE_BASE ahead=1 files=1
1069 $MERGE_BASE ahead=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirty-six paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1061_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
ST = "systemTest/schemathesis/"
ADMINCFG = O + "src/routes/adminConfig.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  ADMINCFG:                                                                        ({"26cec03de665ef75a8f6e4f2532dfc42a59a25b8": DV}, {"62af28d017069d38fa00e7915bfa65226db678c6": "#1061 own"}),
  D + "scripts/preflight/preflight.sh":                                            ({"539493d9d94942189e85953512d6f3981bd9c5d4": DV}, {"712f895362e2c8d1ead6fd09ac257d7bce212948": "#1062 own"}),
  A + "src/__tests__/ks1101-health-aggregates-surface-degraded.test.ts":           ({"e03f600d51d441ca42aff15d92e8391bcc66e2cb": DV}, {"689a6cdd950c1bf373e974bd0d5c9b62389e5bae": "#1063 own"}),
  O + "src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts":           ({"1b0eb5dd81839dd6e402ff4e6fa87b0b24877885": DV}, {"234858bb1f2661bb82d4f7aa40f360d320448dee": "#1066 own"}),
  A + "src/__tests__/ks1258-degraded-optional-service-advice.test.ts":             ({"fe456997603256f1036499a8a8f33949f43631bf": DV}, {"b8abdea46d68f745724fa7b36b3b852ddb38118b": "#1068 own"}),
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"26af52344bcdbc5de5ba592e97fabc2608718738": DV}, {"7fcedac7602a22f202f3ef6257db940d52f98010": "#1069 own"}),
  ".githooks/pre-push":                                                            ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  D + "scripts/run-shell-suites.sh":                                               ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  D + "scripts/__tests__/preflight_state_is_initialised.test.sh":                  ({"ee31ee5f5bc3f0e4939df9587e346296b8ea494c": DV}, {}),
  D + "scripts/__tests__/preflight_verdict_names_real_failures.test.sh":           ({"fb762f6389a0700afcab456fc275062cace05520": DV}, {}),
  D + "scripts/__tests__/pre_push_hook_base.test.sh":                              ({"affdf027bff11e3690d374e902e3e93274788c62": DV}, {}),
  D + "scripts/__tests__/preflight_deps.test.sh":                                  ({"5ad0541313589635c6c100677cf14fb02d00be78": DV}, {}),
  D + "scripts/__tests__/check_slot_credentials.test.sh":                          ({"5ea337e2c7b92bcc92bb99cea4d229fb354d0358": DV}, {}),
  D + "scripts/__tests__/no_tracked_credentials_root.test.sh":                     ({"b4e622e3a7c605ff050cec14e40d9f1fccd030cc": DV}, {}),
  A + "src/routes/system-status.ts":                                               ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  A + "src/startup-migrations.ts":                                                 ({"ed3e521426e75910c5bf2cf07e7251f2fd8ef538": DV}, {}),
  O + "src/routes/documents.ts":                                                   ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {}),
  D + "services/security/src/index.ts":                                            ({"0903ce4380f219765ac63f5f9399d1bf0b4f230a": DV}, {}),
  ST + "scripts/setup_api_key.py":                                                 ({"8779ff2210d6c2e04aea09e9b66144aa26130309": DV}, {}),
  ST + "tests/test_tenant_isolation_writes.py":                                    ({"0365de3858588226930092aa5eae64444f86ecbe": DV}, {}),
  O + "package.json":                                                              ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  O + "jest.config.js":                                                            ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                             ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  A + "package.json":                                                              ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                          ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  A + "tsconfig.json":                                                             ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
  D + "scripts/__tests__/pre_push_hook_current_develop.test.sh":                   ({"ABSENT": DV}, {"60ae41616a9f54594509e08917cd83eaf25dbc1d": "#1065 own"}),
  D + "scripts/__tests__/preflight_failure_verdict_keeps_ratio.test.sh":           ({"ABSENT": DV}, {"23a19ae6ddb532dc604a681a1e51eece1409e951": "#1062 own"}),
  A + "src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts": ({"ABSENT": DV}, {"a30b777a017febbef378ad0772c4841ae12efa9f": "#1067 own"}),
  A + "src/__tests__/ks864d-empty-portal-env-var-falls-back.test.ts":              ({"ABSENT": DV}, {"95f5fd995353d24ae1c641c4f78b53aeb1ff1a25": "#1064 own"}),
  O + "src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts":         ({"ABSENT": DV}, {"02339f9b0e00048b07c521c75d66239878e87158": "#1061 own"}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1061_ADMINCFG_FILE", "") if f == ADMINCFG else ""
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all nine heads: each merged tree = its head tree, a fast-forward: #1061 40cce41ac, #1062 b8571562e, #1063 9b842f84c, #1064 d03d08e1a, #1065 edfd6317a, #1066 3608b08d1, #1067 2930849c5, #1068 9a10fc667, #1069 ed4f0411a; all nine together 275cff9ffcb1a8204db499506f08db54ee39f4eb, drafter tree-hash and scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)
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
           D + "services/security/src/",
           D + "scripts/",
           ST,
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
tail = "the gate merges the then-current develop onto EACH of the nine heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all nine 275cff9ff) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway and originate src/ + config, security src/, scripts/, systemTest/schemathesis/, the Dev package.json + lock, eslint.config.mjs, .githooks/, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1061 KS-1206: TIER 1' "$PROMPT_FILE" && grep -qF '#1062 KS-1260: TIER 1' "$PROMPT_FILE" && grep -qF '#1063 KS-1101: TIER 2' "$PROMPT_FILE" && grep -qF '#1064 KS-864: TIER 2' "$PROMPT_FILE" && grep -qF '#1065 KS-991: TIER 2' "$PROMPT_FILE" && grep -qF '#1066 KS-739: TIER 2' "$PROMPT_FILE" && grep -qF '#1067 KS-1062: TIER 2' "$PROMPT_FILE" && grep -qF '#1068 KS-1258: TIER 2' "$PROMPT_FILE" && grep -qF '#1069 KS-1230: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1061 T1, #1062 T1, #1063-#1069 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1061-#1069 (nine PRs; tier 1 = #1061 KS-1206, #1062 KS-1260)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'NINE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and NINE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 need a stack' "$PROMPT_FILE" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 need a stack' "$BRIEF" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 need a stack / login_stub / mergeable_state: unstable" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-3rd/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-3rd history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'security/src/index.ts:569' "$PROMPT_FILE" && grep -qF 'Nothing failed' "$PROMPT_FILE" && grep -qF 'NOJSONCATCH' "$PROMPT_FILE" && grep -qF '1695' "$PROMPT_FILE" && grep -qF 'matches at 576' "$PROMPT_FILE" \
  && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qiF 'execute the FAILED path' "$PROMPT_FILE" \
  && grep -qF 'security/src/index.ts:569' "$BRIEF" && grep -qF 'Nothing failed' "$BRIEF" && grep -qF 'NOJSONCATCH' "$BRIEF" && grep -qF '1695' "$BRIEF" && grep -qF 'matches at 576' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry G-1 / G-2 / G-3 / G-4, or the prompt does not say MEASURE, not conclude and execute the FAILED path" >&2; exit 30; }
grep -qF '275cff9ffcb1a8204db499506f08db54ee39f4eb' "$PROMPT_FILE" && grep -qF '77b7af584' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-nine tree in full, the octopus commit, the NOT-PINNED list, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1062 is KS-1260' "$PROMPT_FILE" && grep -qF 'PR #1067 is KS-1062' "$PROMPT_FILE" && grep -qF 'PR #1062 is KS-1260' "$BRIEF" && grep -qF 'PR #1067 is KS-1062' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH name the namespace trap: PR #1062 is KS-1260 / PR #1067 is KS-1062" >&2; exit 32; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  nine heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1061 T1, #1062 T1, #1063-#1069 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all nine heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, NINE verdict lines"
  echo "  prompt names the report directory, the #1050-#1060 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 need a stack / login_stub / mergeable_state: unstable"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-3rd history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry G-1 / G-2 / G-3 / G-4; the prompt says MEASURE, not conclude, and execute the FAILED path"
  echo "  prompt names the all-nine tree, the octopus commit, the NOT-PINNED list and a loopback GATEWAY_URL for preflight"
  echo "  READY mail and prompt BOTH name the namespace trap: PR #1062 is KS-1260, PR #1067 is KS-1062"
  [ -n "${QAB1061_CUR_DEV:-}" ] && echo "  (develop read from the QAB1061_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1061_ADMINCFG_FILE:-}" ] && echo "  (develop services/originate/src/routes/adminConfig.ts read from the QAB1061_ADMINCFG_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1061_BRIEF:-}${QAB1061_PROMPT:-}${QAB1061_HEAD_1069:-}${QAB1061_CUR_DEV:-}${QAB1061_ADMINCFG_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
