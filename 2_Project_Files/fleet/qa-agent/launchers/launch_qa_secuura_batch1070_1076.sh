#!/bin/bash
# launch_qa_secuura_batch1070_1076.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over SEVEN file-disjoint Secuura/Blockchain PRs
#   #1070 KS-1276 @ 59af03cba  docs/VOCABULARY.md: the PII caveat opens "payload is encrypted at rest" — the gate GRADES it MEETS or PARTIAL — TIER 2 (docs)
#   #1071 KS-1269 @ dc0bf9315  vc-issuer status.ts: /revoke and /unrevoke refuse a present non-integer index (400) + 2 new suites  — TIER 1 (runtime)
#   #1072 KS-1206 @ cb8c0b186  ks1206 jest test: N61-1, rateLimit null / 0 / 1.5 / "100" refused, lower bound 1 mints            — TIER 2 (test-only)
#   #1073 KS-864  @ 085205d44  ks864d vitest test: N64-1, an EMPTY NODE_ENV is reported as development                           — TIER 2 (test-only)
#   #1074 KS-1230 @ 6be54e11b  ks1230 vitest test: N69-1, a null allow-list on the SECOND integration is stored as null           — TIER 2 (test-only)
#   #1075 KS-739  @ 3ec034083  ks739 jest test: N66-1, a non-JSON 401 / 429 lookup answers that 4xx (archived ticket, NO Refs)     — TIER 2 (test-only)
#   #1076 KS-1238 @ aff1568f3  ks1215 test +1 cell (F1i) and NEW ks1238 test (F1ii): AUTH surface, test files only, 0 product bytes  — TIER 2 (test-only)
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too; PR #1070 is KS-1276 and PR #1071 is KS-1269 (exit 32).
# Batched under Kam's 09:22 rule. SEVEN verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 14:33:37 AEST 2026-09-19 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop 51dbedd39; compare develop...head = merge_base 51dbedd39, ahead 1, files 1/3/1/1/1/1/2 (asserted per PR, exit 10).
# Pairwise file-disjoint (10 files, 3 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL SEVEN = tree bc4d0ed7f, re-derived by
# the generator by pure tree hashing (no git write) AND by the drafter in a --shared scratch clone (merge-tree chains, forward and reverse), equal to
# the builder's prediction and to its local octopus commit 29bc11a08's tree. All seven are byte-identical to their CANONICAL local-model patches,
# re-applied by the generator in a plain scratch dir (#1071's four sections with --directory=Blockchain/Dev, in both run orders; the rest strict).
#
# The develop pin is judged by CONTENT — THIRTY-FIVE paths by blob at the CURRENT develop: the 10 PR files (seven at develop blobs, three new files
# ABSENT; any PR's head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: the lifecycle repo + payload codec (KS-1276's
# premise), proxy.ts / auth.ts / platform.ts (the auth tampers and F-1 (iii)), adminConfig.ts, system-status.ts, admin.ts, documents.ts, the
# vc-issuer OpenAPI source, the vc-issuer / originate / api-gateway configs, the Dev package.json + lock, eslint.config.mjs, the two systemTest reads
# (test_by_design_permissive.py, schemathesis-baseline.json) and BACKLOG.md.
# GUARDED: vc-issuer / api-gateway / originate src/ + config, packages/shared src/, docs/VOCABULARY.md, systemTest/schemathesis/, the Dev
# package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md, the seat's READY mail (04:30:27Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the seven heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all seven heads.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and SEVEN verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1061-#1069 batch) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'Legs 3/4/8 need a stack', 'mergeable_state: unstable' and 'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-4th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (status.ts:300, :231, merge-msg-1071.txt, 2026-08-27T15:22:07Z, platform.ts:254,
#          BEARERONLY, COMPLETENESS), and the prompt must ask the gate to MEASURE, not conclude, and to grade KS-1276 MEETS or PARTIAL.
# exit 31: the prompt must name the all-seven tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row.
# exit 32: the READY mail AND the prompt must BOTH name the namespace trap: PR #1070 is KS-1276, PR #1071 is KS-1269.
# QAB1070_CUR_DEV (test override, --check only): stands in for origin develop. QAB1070_HEAD_1076 (test override): stands in for #1076's pinned head.
# QAB1070_STATUSTS_FILE (test fixture, --check only): a local file stands in for develop services/vc-issuer/src/routes/status.ts (its git blob).
# A launch with any QAB1070_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-19_gate1070to1076/gen_launcher_batch1070_1076.py from launch_qa_secuura_batch1061_1069.sh (asserted block
# substitutions + pins re-read + canonical-patch identity + all-seven tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1070_1076.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..32 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1070_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md}"
PROMPT_FILE="${QAB1070_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-19_secuura-batch1070-1076.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (04:30:27Z) and re-read by the drafter (git ls-remote 14:33:37 AEST, branch AND refs/pull/N/head)
# NAMESPACE TRAP: PR #1070 is KS-1276 and PR #1071 is KS-1269 (no PR here is its own-numbered ticket)
PRS=(
  "1070|KS-1276|refs/heads/feature/ks-1276-docsvocabularymd165-166-says-lifecycle-payloads-are-stored|59af03cbab07bfcd151206d732d3aa989ac0256c"
  "1071|KS-1269|refs/heads/feature/ks-1269-post-apistatusidrevoke-accepts-index-object-where-integer-is|dc0bf93159a981d695d4fcdff9329003e1c26d99"
  "1072|KS-1206|refs/heads/feature/ks-1206-originate-admin-api-key-mint-writes-no-connector_id-and-an-n61-1|cb8c0b18616b29eea77ef6efac0e3fac90178671"
  "1073|KS-864|refs/heads/feature/ks-864-dead-estate-pointers-in-runtime-source-outside-n64-1|085205d444f6045c5ccc1c45f741aa252beae764"
  "1074|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n69-1|6be54e11b263f9881c7b410ae17613134c577fb7"
  "1075|KS-739|refs/heads/feature/pin-transfer-custody-nonjson-401-429-lookup-failed|3ec034083716f104eccfc50e2734ab16082e1e72"
  "1076|KS-1238|refs/heads/feature/ks-1238-f-1-pin-bearer-scheme-and-hand-forwarded-routes|${QAB1070_HEAD_1076:-aff1568f387b5073f31dcb99519cafeda7cc66bc}"
)
DEVELOP_SHA='51dbedd39ade43cc511278502b2e1e190de641c7'   # the pin = develop at 14:33:37 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1070-1076-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1061-1069-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-19_gate1070to1076/mail_batch1070_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The seven heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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
# develop...head = 51dbedd39 ahead 1 for all seven PRs; files #1070 1, #1071 3, #1072-#1075 1 each, #1076 2
# (git diff --name-only + rev-list, drafter 14:3x AEST; the launcher reads the compare API).
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
WANT_COMPARE="1070 $MERGE_BASE ahead=1 files=1
1071 $MERGE_BASE ahead=1 files=3
1072 $MERGE_BASE ahead=1 files=1
1073 $MERGE_BASE ahead=1 files=1
1074 $MERGE_BASE ahead=1 files=1
1075 $MERGE_BASE ahead=1 files=1
1076 $MERGE_BASE ahead=1 files=2"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirty-five paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1070_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
ST = "systemTest/schemathesis/"
STATUSTS = V + "src/routes/status.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  D + "docs/VOCABULARY.md":                                                        ({"cc4093b0b992621a651c21ac9a4cb6cee9425515": DV}, {"7b7072b4e1da0532f477d3e7f5ad60752fc76c71": "#1070 own"}),
  STATUSTS:                                                                        ({"c44d69275a28f51dc26e41c66f382208a7962f03": DV}, {"394337283ec19e77a10d1b25b8c5cc2b978fb52e": "#1071 own"}),
  O + "src/__tests__/ks1206-admin-api-key-mint-bounds-rate-limit.test.ts":         ({"02339f9b0e00048b07c521c75d66239878e87158": DV}, {"97e3e28822556e6c85a2e6d5653538a11b952bbc": "#1072 own"}),
  A + "src/__tests__/ks864d-empty-portal-env-var-falls-back.test.ts":              ({"95f5fd995353d24ae1c641c4f78b53aeb1ff1a25": DV}, {"d8129b7ad94fcaf7e32bfdf484c23c3a057f6d49": "#1073 own"}),
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"7fcedac7602a22f202f3ef6257db940d52f98010": DV}, {"d7adefe7b6fad5135d3a934ec58119dd6aa13ea6": "#1074 own"}),
  O + "src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts":           ({"234858bb1f2661bb82d4f7aa40f360d320448dee": DV}, {"fcb46e6aa547fd51d8273b9336bae0dc87ad0dca": "#1075 own"}),
  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"75006b5cf50fb8b42a5e7588a1d622b9168c1b07": DV}, {"7d14580b0a2c0f7967e578345e13f534d0919987": "#1076 own"}),
  O + "src/repositories/lifecycleEventRepo.ts":                                    ({"0aec7a3265ee91eeb430ad02b2445d9d89a9f7f2": DV}, {}),
  O + "src/utils/lifecyclePayloadCodec.ts":                                        ({"ff48ac114a60d450e9d477d748d48562ba50502e": DV}, {}),
  A + "src/routes/proxy.ts":                                                       ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  A + "src/middleware/auth.ts":                                                    ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  A + "src/routes/platform.ts":                                                    ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  O + "src/routes/adminConfig.ts":                                                 ({"62af28d017069d38fa00e7915bfa65226db678c6": DV}, {}),
  A + "src/routes/system-status.ts":                                               ({"e911ce1fdaa4b755e9b7b6428f899cdbd63889cb": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  O + "src/routes/documents.ts":                                                   ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {}),
  V + "src/vc-issuer.openapi.ts":                                                  ({"6ab97ceb863a2d0a3725259670307d165918e9ba": DV}, {}),
  V + "package.json":                                                              ({"27888b6eeb6c20b44af947d14eddb3bccf6293cf": DV}, {}),
  V + "vitest.config.ts":                                                          ({"ddacccfb518d23d24ecfb5ddcf60e8373166d8b5": DV}, {}),
  V + "tsconfig.json":                                                             ({"b3546b85f68847a2cd62ad74f10f5f7347579bc5": DV}, {}),
  O + "package.json":                                                              ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  O + "jest.config.js":                                                            ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                             ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  A + "package.json":                                                              ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                          ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  A + "tsconfig.json":                                                             ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  ST + "tests/test_by_design_permissive.py":                                       ({"c96967cfce7022e625ca92f66c8224f7defbaba5": DV}, {}),
  ST + "config/schemathesis-baseline.json":                                        ({"e94ee422eca3eb80554cf8a4d65f78ed65658f44": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
  A + "src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts":  ({"ABSENT": DV}, {"ee10e191c8497948720ccc3e9df705601c4a67b1": "#1076 own"}),
  V + "src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts":    ({"ABSENT": DV}, {"bb8801cfb463758b3765ad015382906e4191d627": "#1071 own"}),
  V + "src/__tests__/ks1269-status-unrevoke-refuses-a-non-integer-index.test.ts":  ({"ABSENT": DV}, {"18197eb1ef648aef145d04ebdee08afca85cd484": "#1071 own"}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1070_STATUSTS_FILE", "") if f == STATUSTS else ""
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all seven heads: each merged tree = its head tree, a fast-forward: #1070 2c1ffc1b0, #1071 0ff438faa, #1072 48eb67154, #1073 35d782a03, #1074 7a67ef6a3, #1075 0eb2d8cec, #1076 8e11427ef; all seven together bc4d0ed7fccc3bb9f594bd18565c9a5e47ab9db4, drafter tree-hash and scratch-clone merges = builder prediction; git ls-remote)"); sys.exit(0)
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
           V + "vitest.config.ts",
           V + "tsconfig.json",
           D + "packages/shared/src/",
           D + "docs/VOCABULARY.md",
           ST,
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
tail = "the gate merges the then-current develop onto EACH of the seven heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all seven bc4d0ed7f) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (vc-issuer, api-gateway and originate src/ + config, packages/shared src/, docs/VOCABULARY.md, systemTest/schemathesis/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1070 KS-1276: TIER 2' "$PROMPT_FILE" && grep -qF '#1071 KS-1269: TIER 1' "$PROMPT_FILE" && grep -qF '#1072 KS-1206: TIER 2' "$PROMPT_FILE" && grep -qF '#1073 KS-864: TIER 2' "$PROMPT_FILE" && grep -qF '#1074 KS-1230: TIER 2' "$PROMPT_FILE" && grep -qF '#1075 KS-739: TIER 2' "$PROMPT_FILE" && grep -qF '#1076 KS-1238: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1071 T1, #1070 and #1072-#1076 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1070-#1076 (seven PRs; tier 1 = #1071 KS-1269)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'SEVEN lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and SEVEN verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'Legs 3/4/8 need a stack' "$PROMPT_FILE" && grep -qF 'mergeable_state: unstable' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$PROMPT_FILE" \
  && grep -qF 'Legs 3/4/8 need a stack' "$BRIEF" && grep -qF 'mergeable_state: unstable' "$BRIEF" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: Legs 3/4/8 need a stack / mergeable_state: unstable / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-19_seatB-4th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-19_seatB-4th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF 'status.ts:300' "$PROMPT_FILE" && grep -qF ':231' "$PROMPT_FILE" && grep -qF 'merge-msg-1071.txt' "$PROMPT_FILE" && grep -qF '2026-08-27T15:22:07Z' "$PROMPT_FILE" && grep -qF 'platform.ts:254' "$PROMPT_FILE" && grep -qF 'BEARERONLY' "$PROMPT_FILE" && grep -qF 'COMPLETENESS' "$PROMPT_FILE" \
  && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'MEETS or PARTIAL' "$PROMPT_FILE" \
  && grep -qF 'status.ts:300' "$BRIEF" && grep -qF ':231' "$BRIEF" && grep -qF 'merge-msg-1071.txt' "$BRIEF" && grep -qF '2026-08-27T15:22:07Z' "$BRIEF" && grep -qF 'platform.ts:254' "$BRIEF" && grep -qF 'BEARERONLY' "$BRIEF" && grep -qF 'COMPLETENESS' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items 2-10, or the prompt does not say MEASURE, not conclude and grade KS-1276 MEETS or PARTIAL" >&2; exit 30; }
grep -qF 'bc4d0ed7fccc3bb9f594bd18565c9a5e47ab9db4' "$PROMPT_FILE" && grep -qF '29bc11a08' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-seven tree in full, the octopus commit, or the NOT-PINNED list with a proposed cell per row" >&2; exit 31; }
grep -qF 'PR #1070 is KS-1276' "$PROMPT_FILE" && grep -qF 'PR #1071 is KS-1269' "$PROMPT_FILE" && grep -qF '| #1070 | KS-1276 |' "$BRIEF" && grep -qF '| #1071 | KS-1269' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH name the namespace trap: PR #1070 is KS-1276 / PR #1071 is KS-1269" >&2; exit 32; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  seven heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1071 T1, #1070 and #1072-#1076 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all seven heads"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, SEVEN verdict lines"
  echo "  prompt names the report directory, the #1061-#1069 batch PRIOR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: Legs 3/4/8 need a stack / mergeable_state: unstable / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-19_seatB-4th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items 2-10; the prompt says MEASURE, not conclude, and grades KS-1276 MEETS or PARTIAL"
  echo "  prompt names the all-seven tree, the octopus commit and the NOT-PINNED list with a proposed cell per row"
  echo "  READY mail and prompt BOTH name the namespace trap: PR #1070 is KS-1276, PR #1071 is KS-1269"
  [ -n "${QAB1070_CUR_DEV:-}" ] && echo "  (develop read from the QAB1070_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1070_STATUSTS_FILE:-}" ] && echo "  (develop services/vc-issuer/src/routes/status.ts read from the QAB1070_STATUSTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1070_BRIEF:-}${QAB1070_PROMPT:-}${QAB1070_HEAD_1076:-}${QAB1070_CUR_DEV:-}${QAB1070_STATUSTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
