#!/bin/bash
# launch_qa_secuura_1105.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over ONE Secuura/Blockchain PRODUCT PR
#   #1105 KS-1175 (+ KS-1284 codec, Refs KS-721) @ e02d3ecb5 — the KS-1175 REAL FIX: the flat-anchor schema accepts a top-level `identity` block
#   (seven non-PII fields + identityCommitment), the KS-1284 Cardano metadatum codec at the ONE tx-build attach point and its inverse at the
#   verify-by-hash chain read, two read-backs (GET /api/anchors/verify/:hash metadata.identity; GET /api/anchors/:id identityCommitment + identity),
#   the regenerated OpenAPI yaml (ONE FlatAnchorRequest hunk) and VOCABULARY.md §2. Raised by Seat A 15th, READY 2026-09-20T13:55:07Z.
# TIER 1: it changes the schema of what goes on the immutable Cardano record. Round 1 of 2 (Kam 2026-09-05 cap). ONE verdict.
# 12 files +1084/-64, ALL under Blockchain/Dev/services/anchoring/** except docs/openapi/secuura-api.yaml and docs/VOCABULARY.md (generator: local
# objects AND the PR files API, gh_pr_reads.out); 5 ADDED (absent at develop), 7 MODIFIED, 0 deleted; no migration / config / dependency (CSL 15.0.3
# pinned in both lockfiles at both trees, generator-read).
# EVERY VALUE HERE IS THE BUILDER'S MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the head, its parent, its tree, the 12 blob pairs, the
# unchanged-read blobs, the CSL pin, the one yaml hunk — all re-read from origin + local objects by gen_launcher_1105.py at generation.
# NAMESPACE TRAP: KS-1105 is a real, unrelated ticket (Backlog, 0 attachments at 14:03Z); PR #1105 is KS-1175. The READY mail AND the prompt must
# BOTH state it, or the launch refuses (exit 32).
# MERGE AUTHORITY: WEDNESDAY'S signed GO naming e02d3ecb5 (exit 26). THE DEPLOY AND THE ANCHOR ARE KAM'S — the gate rules nothing about either.
#
# THE SHAPE, re-read live by the generator (git ls-remote develop + refs/pull/1105/head + the branch; rev-list --parents; diff --raw): the head is
# ONE commit whose parent IS develop dc061f2bb (tree 1ccb80e0d = the #1100-#1101 batch gate's both-PRs tree, landed); head tree 8f066a817. Over the
# pin the merge is a fast-forward: merged tree = head tree. compare develop...head = merge_base dc061f2bb, ahead 1, files 12 (exit 10).
#
# The develop pin is judged by CONTENT — THIRTY-FIVE paths by blob at the CURRENT develop: the 12 PR paths (7 at develop blobs, 5 ABSENT; any at its
# head blob -> exit 19 LANDED), and what the gate runs or reads: anchoring package.json + lock + tsconfig + vitest.config, verifyAnchorStatus.ts,
# the control test files (ks480, ks566, threadTokenMint, db.retry), cardano/provider.ts + wallet.ts, the Dev package.json + lock, eslint.config.mjs,
# BACKLOG.md, the pre-push hook, generate-openapi.ts, check-spec-examples.mjs, preflight.sh, originate documents.ts + anchors.ts (the SEVEN-endpoint
# count), api-gateway proxy.ts + verification.ts (NOT DONE 2).
# GUARDED: services/anchoring/, docs/openapi/, docs/VOCABULARY.md, scripts/, packages/shared src/, .githooks/, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md, the two originate route files, the two api-gateway route files.
#
# SOURCE = gatesets/2026-09-20_gate1105_READY_seatA15.txt (the READY, 13:55:07Z) + gatesets/2026-09-20_gate1105_STATUS2_seatA15.txt (STATUS 2,
# 13:51:06Z), both captured verbatim by Wednesday from wednesday-agent@ and re-listed by message id by the drafter (list_ready_mail.out).
#
# exit 6:  the head is not at its branch AND at refs/pull/1105/head on origin.
# exit 7:  the prompt must carry 'TIER 1' AND the PR's own tier line '#1105 KS-1175: TIER 1'.
# exit 20: the READY mail AND the prompt must name the head in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and the three verdict words.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1100-#1101 batch, whose both-PRs tree IS this develop), the EXEMPLAR
#          REPORT (the ks1215 #1034 single-PR product gate) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO naming e02d3ecb5 as the merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the builder's own words: 'PREFLIGHT', '12/15', 'login_stub', 'SKIPPED', 'threadTokenMint'.
# exit 28: the prompt must forbid entering any seat worktree (s-a15-ks1175) and writing in the builder's 2026-09-20_seatA-15th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the builder's items (the counts 318/319, 242, 293, 247/46; T1-T6 and T3b's '0 red'; the
#          facts comment id and 4999/4999; CSL 15.0.3; develop in full; :6882 and :5432; BACKLOG.md:155; the +65 hunk and 405 blocks; the two
#          originate line ranges; transaction.ts:107; SEVEN; R8/R9 by MODULE ABSENCE; superRefine; NOT DONE), and the prompt must ask the gate to
#          MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the head tree in full, the NOT-PINNED list with a proposed cell per row, and a loopback GATEWAY_URL for any
#          preflight run.
# exit 32: the READY mail AND the prompt must BOTH state that PR #1105 is KS-1175 (KS-1105 is another ticket).
# exit 33: the prompt must carry Wednesday's FIFTEEN BY-NAME items, each by its own keywords (see the ladder below): head/base re-read by two
#          instruments; red-first as TWO kinds of red; the six tampers with T3b's 0 red as a finding; the codec's four (no-op, UTF-8 bytes straddling
#          64, booleans as strings, floats/null upstream); the verify-by-hash order with the reorder control; DECIDE 2; whitelist/strip; the two
#          read-backs with the byte-for-byte diff; the spec (check:openapi, one hunk, 405, masked); nothing outside the allowed paths / no
#          dependency change; SEVEN-not-six; the 3 SKIPPED legs NOT RUN; the six NOT DONE with the facts comment by id by length only; NOT-PINNED
#          as the local model's feed; the standard closing (DKIM, NOT-TESTED first, census, the verdict words, Majors/Minors, slips by name).
# QAB1105_CUR_DEV (test override, --check only): stands in for origin develop. QAB1105_HEAD (test override): stands in for the pinned head.
# QAB1105_INDEXTS_FILE (test fixture, --check only): a local file stands in for develop services/anchoring/src/index.ts (its git blob).
# A launch with any QAB1105_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1105/gen_launcher_1105.py in the shape of launch_qa_secuura_batch1100_1101.sh (pins re-read from origin +
# local objects + output controls + heredoc parity + bash -n).
#
# Usage: launch_qa_secuura_1105.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1105_BRIEF:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1105_READY_seatA15.txt}"
STATUS2="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1105_STATUS2_seatA15.txt"
PROMPT_FILE="${QAB1105_PROMPT:-/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_secuura-1105.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the builder's READY (13:55:07Z) and re-read by the drafter (git ls-remote 13:59:46Z and 14:13:57Z, branch AND
# refs/pull/1105/head; the pulls API 14:03:26Z). NAMESPACE TRAP: KS-1105 is another ticket; the ticket column is the truth (exit 32)
PRS=(
  "1105|KS-1175|refs/heads/feature/ks-1175-anchor-originate-lifecycle-event-schemas-accept-and-anchor|${QAB1105_HEAD:-e02d3ecb51a457b0eb490db1854f28c6b1af69ad}"
)
DEVELOP_SHA='dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa'   # the pin = develop at 13:59:46Z and 14:13:57Z; the head's parent and merge-base
MERGE_BASE="$DEVELOP_SHA"    # the head sits on the pin itself — the compare is asserted against it
HEAD_TREE='8f066a81784c89ae3531938a006c7ae69bdb4ba1'     # over the pin the merge is a fast-forward: merged tree = head tree
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-pr1105-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
EXEMPLAR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
REAL_BRIEF="/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1105_READY_seatA15.txt"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief (READY capture) missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$STATUS2" ]        || { echo "STATUS 2 capture missing or empty: $STATUS2" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch AND at refs/pull/1105/head on origin (one ls-remote). A moved head refuses the launch: re-pin.
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

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — develop is expected to move):
# develop...head = dc061f2bb ahead 1 files 12 (git rev-list + diff --raw, drafter 13:59Z; the launcher reads the compare API).
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
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="1105 $MERGE_BASE ahead=1 files=12"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compare read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): thirty-five paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1105_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" HEAD_TREE="$HEAD_TREE" python3 - <<'PYJ'
import hashlib, json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]; head_tree = os.environ["HEAD_TREE"]
D = "Blockchain/Dev/"
A = D + "services/anchoring/"
INDEXTS = A + "src/index.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  "Blockchain/Dev/docs/VOCABULARY.md":                                                 ({"7b7072b4e1da0532f477d3e7f5ad60752fc76c71": DV}, {"75633ef85930dda5afb4ce6cad07f6e225a5d014": "#1105 own"}),
  "Blockchain/Dev/docs/openapi/secuura-api.yaml":                                      ({"a34b59363b81dc3f69cc11a238ff9369deefa9d9": DV}, {"1871025e2c1196aeb6ff33e9bc74b916d3eb9e9e": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/anchorSchema.test.ts":              ({"c1a3e865a101f865f045ef3dfa8252b266ad04d3": DV}, {"570d2168350452e0e500e2ad2feed27713b54983": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts":    ({"ABSENT": DV}, {"05793d9254002f951e46d882510ec39e3d38dd37": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts": ({"ABSENT": DV}, {"c3f430d783ba0d8594d962ceef13ad27325f402b": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks1284-cardano-metadatum.test.ts":  ({"ABSENT": DV}, {"33cf6608e6a472293b7116a81a304dad446071a1": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/anchorReadback.ts":                           ({"ABSENT": DV}, {"f49ffb6afaafabefe4dfbe8d897623bb2e5b3fc7": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/anchorSchema.ts":                             ({"8341c8221b5008b5f6a0a6a6d7887198f71b02f5": DV}, {"af95458d00b776f7427f367d0ca834ef33430aa7": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/anchoring.openapi.ts":                        ({"29c089bb0abcd65d42fe8fca2d6beaff0368fa98": DV}, {"5d0a1b9eb19b116abc0c9739a714439adad7bc35": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/cardano/cardanoMetadatum.ts":                 ({"ABSENT": DV}, {"aaaec6c63655340bb864dc3aaa395a5707c9a6fb": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/cardano/transaction.ts":                      ({"3a86936bef0b657bd0375b7d1838c3ee22f15bce": DV}, {"e047630ea0048b7d9e5d29793558a59eb5e437e4": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/src/index.ts":                                    ({"da4abd43292186da45c1533017fe042fa512bd43": DV}, {"b6386f402a4bc1572574c14e4925a96fd7811a39": "#1105 own"}),
  "Blockchain/Dev/services/anchoring/package.json":                                    ({"a7eed73550b40aa2d968872817fa22e933373831": DV}, {}),
  "Blockchain/Dev/services/anchoring/package-lock.json":                               ({"7ef3f65a35b48bec2591df4b2859bab9aa237334": DV}, {}),
  "Blockchain/Dev/services/anchoring/tsconfig.json":                                   ({"f593300cac7c9c3073f15a1287323cf5b9dd478d": DV}, {}),
  "Blockchain/Dev/services/anchoring/vitest.config.ts":                                ({"2e1d21f130f8aa80a1c71987f920181dafaf6b90": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/verifyAnchorStatus.ts":                       ({"b8b73078e456916c9d3d47c350046758975a1208": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks480-provenance-exclusion.test.ts": ({"a87ee027668cd0f56fe2886ceb116a12920eb61f": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/ks566-connector-attribution.test.ts": ({"b7c1013b8836bc4e3ef247a82d088f2c0d149294": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/threadTokenMint.test.ts":           ({"b88b3a43ec5dcb8651b91d5df90e9dec42a1795f": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/__tests__/db.retry.test.ts":                  ({"0367a32466a4a555186385fd6798548f04a8d923": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/cardano/provider.ts":                         ({"9232d4d0a8a5950a1096cfa473da6705751da77e": DV}, {}),
  "Blockchain/Dev/services/anchoring/src/cardano/wallet.ts":                           ({"f2160e51817c4a752a1dbb77eb6207f3f56bb65a": DV}, {}),
  "Blockchain/Dev/package.json":                                                       ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  "Blockchain/Dev/package-lock.json":                                                  ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  "Blockchain/Dev/eslint.config.mjs":                                                  ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                        ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
  ".githooks/pre-push":                                                                ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  "Blockchain/Dev/scripts/generate-openapi.ts":                                        ({"e84acdc9e1be073751fcd6a8bb95504e23688019": DV}, {}),
  "Blockchain/Dev/scripts/spec-examples/check-spec-examples.mjs":                      ({"e9c14a4dedf103850dc1c93fb1c5c67b8489b2a3": DV}, {}),
  "Blockchain/Dev/scripts/preflight/preflight.sh":                                     ({"712f895362e2c8d1ead6fd09ac257d7bce212948": DV}, {}),
  "Blockchain/Dev/services/originate/src/routes/documents.ts":                         ({"3f837fc6e656d5a10f9cc349b1cb2a876a2be09b": DV}, {}),
  "Blockchain/Dev/services/originate/src/routes/anchors.ts":                           ({"d30620bffae3931c242104501299564d785ed8fb": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/proxy.ts":                           ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  "Blockchain/Dev/services/api-gateway/src/routes/verification.ts":                    ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; the PR head blob, exit 19).
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1105_INDEXTS_FILE", "") if f == INDEXTS else ""
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — that PR has landed; this gateset is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (the parent and merge-base of the head: the merged tree = the head tree " + head_tree + ", a fast-forward; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [A,
           D + "docs/openapi/",
           D + "docs/VOCABULARY.md",
           D + "scripts/",
           D + "packages/shared/src/",
           ".githooks/",
           D + "package.json",
           D + "package-lock.json",
           D + "eslint.config.mjs",
           "BACKLOG.md",
           D + "services/originate/src/routes/documents.ts",
           D + "services/originate/src/routes/anchors.ts",
           D + "services/api-gateway/src/routes/proxy.ts",
           D + "services/api-gateway/src/routes/verification.ts"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. Nothing is pre-cleared for this gate; any GUARDED move refuses: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto the head in its own clone, names the merged-tree OID (drafter over the pin: = the head tree) and re-runs every item and suite on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (services/anchoring/, docs/openapi/, VOCABULARY.md, scripts/, packages/shared src/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md, the two originate and two api-gateway route files); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + prompt)" >&2
     exit 18 ;;
esac
grep -qF 'TIER 1' "$PROMPT_FILE" && grep -qF '#1105 KS-1175: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry TIER 1 and the PR's own tier line (#1105 KS-1175: TIER 1)" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" && grep -qF "$STATUS2" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the READY and STATUS 2 capture paths" >&2; exit 9; }
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
grep -qF '[QA/Secuura-1105 -> Wednesday] TIER 1 GATE #1105 (KS-1175 + KS-1284) @ e02d3ecb5' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'GO, GO WITH FINDINGS, or NO GO' "$PROMPT_FILE" && grep -qF 'Majors <n> / Minors <m>' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, coagent@ / wednesday-agent@, the three verdict words and Majors / Minors" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EXEMPLAR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EXEMPLAR REPORT $EXEMPLAR_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'ONE MERGE ADDENDUM line' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry ONE MERGE ADDENDUM line and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming e02d3ecb5" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming e02d3ecb5 as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
grep -qF 'PREFLIGHT' "$PROMPT_FILE" && grep -qF -- '12/15' "$PROMPT_FILE" && grep -qF -- '12/15' "$BRIEF" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'SKIPPED' "$PROMPT_FILE" && grep -qF 'SKIPPED' "$BRIEF" && grep -qF 'threadTokenMint' "$PROMPT_FILE" && grep -qF 'threadTokenMint' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the builder's words: PREFLIGHT / 12/15 / login_stub / SKIPPED / threadTokenMint" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF 's-a15-ks1175' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatA-15th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree (s-a15-ks1175) and writing in the builder's 2026-09-20_seatA-15th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF -- '318 / 319' "$PROMPT_FILE" && grep -qF -- '318 / 319' "$BRIEF" && grep -qF -- '242' "$PROMPT_FILE" && grep -qF -- '242' "$BRIEF" && grep -qF -- '293' "$PROMPT_FILE" && grep -qF -- '293' "$BRIEF" && grep -qF -- '247 / 46' "$PROMPT_FILE" && grep -qF -- '247 / 46' "$BRIEF" && grep -qF -- 'T1' "$PROMPT_FILE" && grep -qF -- 'T1' "$BRIEF" && grep -qF -- 'T2a' "$PROMPT_FILE" && grep -qF -- 'T2a' "$BRIEF" && grep -qF -- 'T2b' "$PROMPT_FILE" && grep -qF -- 'T2b' "$BRIEF" && grep -qF -- 'T3a' "$PROMPT_FILE" && grep -qF -- 'T3a' "$BRIEF" && grep -qF -- 'T3b' "$PROMPT_FILE" && grep -qF -- 'T3b' "$BRIEF" && grep -qF -- 'T3c' "$PROMPT_FILE" && grep -qF -- 'T3c' "$BRIEF" && grep -qF -- 'T4' "$PROMPT_FILE" && grep -qF -- 'T4' "$BRIEF" && grep -qF -- 'T5' "$PROMPT_FILE" && grep -qF -- 'T5' "$BRIEF" && grep -qF -- 'T6' "$PROMPT_FILE" && grep -qF -- 'T6' "$BRIEF" && grep -qF -- '0 red' "$PROMPT_FILE" && grep -qF -- '0 red' "$BRIEF" && grep -qF -- '21af3285-0a40-490c-bfff-bc3466b6066b' "$PROMPT_FILE" && grep -qF -- '21af3285-0a40-490c-bfff-bc3466b6066b' "$BRIEF" && grep -qF -- '4999/4999' "$PROMPT_FILE" && grep -qF -- '4999/4999' "$BRIEF" && grep -qF -- 'CSL 15.0.3' "$PROMPT_FILE" && grep -qF -- 'CSL 15.0.3' "$BRIEF" && grep -qF -- 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa' "$PROMPT_FILE" && grep -qF -- 'dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa' "$BRIEF" && grep -qF -- ':6882' "$PROMPT_FILE" && grep -qF -- ':6882' "$BRIEF" && grep -qF -- ':5432' "$PROMPT_FILE" && grep -qF -- ':5432' "$BRIEF" && grep -qF -- 'BACKLOG.md:155' "$PROMPT_FILE" && grep -qF -- 'BACKLOG.md:155' "$BRIEF" && grep -qF -- '+65' "$PROMPT_FILE" && grep -qF -- '+65' "$BRIEF" && grep -qF -- '405' "$PROMPT_FILE" && grep -qF -- '405' "$BRIEF" && grep -qF -- 'documents.ts:1263-1285' "$PROMPT_FILE" && grep -qF -- 'documents.ts:1263-1285' "$BRIEF" && grep -qF -- 'anchors.ts:282-297' "$PROMPT_FILE" && grep -qF -- 'anchors.ts:282-297' "$BRIEF" && grep -qF -- 'transaction.ts:107' "$PROMPT_FILE" && grep -qF -- 'transaction.ts:107' "$BRIEF" && grep -qF -- 'SEVEN' "$PROMPT_FILE" && grep -qF -- 'SEVEN' "$BRIEF" && grep -qF -- 'login_stub' "$PROMPT_FILE" && grep -qF -- 'login_stub' "$BRIEF" && grep -qF -- '12/15' "$PROMPT_FILE" && grep -qF -- '12/15' "$BRIEF" && grep -qF -- 'SKIPPED' "$PROMPT_FILE" && grep -qF -- 'SKIPPED' "$BRIEF" && grep -qF -- 'threadTokenMint' "$PROMPT_FILE" && grep -qF -- 'threadTokenMint' "$BRIEF" && grep -qF -- 'R8' "$PROMPT_FILE" && grep -qF -- 'R8' "$BRIEF" && grep -qF -- 'R9' "$PROMPT_FILE" && grep -qF -- 'R9' "$BRIEF" && grep -qF -- 'MODULE ABSENCE' "$PROMPT_FILE" && grep -qF -- 'MODULE ABSENCE' "$BRIEF" && grep -qF -- 'superRefine' "$PROMPT_FILE" && grep -qF -- 'superRefine' "$BRIEF" && grep -qF -- 'NOT DONE' "$PROMPT_FILE" && grep -qF -- 'NOT DONE' "$BRIEF" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the builder's items, or the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS" >&2; exit 30; }
grep -qF "$HEAD_TREE" "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the head tree in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1105 is KS-1175.' "$PROMPT_FILE" && grep -qF 'KS-1105' "$PROMPT_FILE" && grep -F 'PR #1105' "$BRIEF" | grep -qF 'KS-1175' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state that PR #1105 is KS-1175 (KS-1105 is another ticket) — the PR number is another ticket's number too" >&2; exit 32; }
grep -qF -- 'parent of e02d3ecb5 is dc061f2bb' "$PROMPT_FILE" && grep -qF -- 'two instruments' "$PROMPT_FILE" && grep -qF -- 'red by ASSERTION' "$PROMPT_FILE" && grep -qF -- 'red by MODULE ABSENCE' "$PROMPT_FILE" && grep -qF -- 'TWO DIFFERENT KINDS OF RED' "$PROMPT_FILE" && grep -qF -- 'BACKLOG.md:155' "$PROMPT_FILE" && grep -qF -- 'threadTokenMint' "$PROMPT_FILE" && grep -qF -- 'tampers/tampers.json' "$PROMPT_FILE" && grep -qF -- 'T3b' "$PROMPT_FILE" && grep -qF -- '0 red' "$PROMPT_FILE" && grep -qF -- 'FINDING to re-measure and grade' "$PROMPT_FILE" && grep -qF -- 'WHOLE anchoring suite' "$PROMPT_FILE" && grep -qF -- 'BYTE-IDENTICAL NO-OP' "$PROMPT_FILE" && grep -qF -- 'UTF-8 BYTES ON CODE-POINT BOUNDARIES' "$PROMPT_FILE" && grep -qF -- 'STRADDLING byte 64' "$PROMPT_FILE" && grep -qF -- '"true"/"false"' "$PROMPT_FILE" && grep -qF -- 'FLOATS / NULL are rejected UPSTREAM' "$PROMPT_FILE" && grep -qF -- 'VERIFY-BY-HASH ORDER' "$PROMPT_FILE" && grep -qF -- 'REORDERED copy' "$PROMPT_FILE" && grep -qF -- 'prove the check can fail' "$PROMPT_FILE" && grep -qF -- 'DECIDE 2 superRefine' "$PROMPT_FILE" && grep -qF -- 'MEASURE the anchored key set' "$PROMPT_FILE" && grep -qF -- 'WHITELIST / STRIP' "$PROMPT_FILE" && grep -qF -- 'smuggled' "$PROMPT_FILE" && grep -qF -- 'ks566 ×6' "$PROMPT_FILE" && grep -qF -- '!== undefined' "$PROMPT_FILE" && grep -qF -- 'GET /api/anchors/verify/:hash' "$PROMPT_FILE" && grep -qF -- 'GET /api/anchors/:id' "$PROMPT_FILE" && grep -qF -- 'buildVerifyResponse' "$PROMPT_FILE" && grep -qF -- 'byte-for-byte' "$PROMPT_FILE" && grep -qF -- 'DIFF IT' "$PROMPT_FILE" && grep -qF -- 'check:openapi' "$PROMPT_FILE" && grep -qF -- 'check:spec-examples' "$PROMPT_FILE" && grep -qF -- 'ONE FlatAnchorRequest hunk' "$PROMPT_FILE" && grep -qF -- 'MASKED' "$PROMPT_FILE" && grep -qF -- '405' "$PROMPT_FILE" && grep -qF -- 'FILES API' "$PROMPT_FILE" && grep -qF -- 'CSL 15.0.3' "$PROMPT_FILE" && grep -qF -- 'no migration' "$PROMPT_FILE" && grep -qF -- 'no dependency change' "$PROMPT_FILE" && grep -qF -- 'SEVEN-not-six' "$PROMPT_FILE" && grep -qF -- 'documents.ts:1263-1285' "$PROMPT_FILE" && grep -qF -- 'anchors.ts:282-297' "$PROMPT_FILE" && grep -qF -- '3 SKIPPED' "$PROMPT_FILE" && grep -qF -- 'NOT RUN, never as passes' "$PROMPT_FILE" && grep -qF -- ':6882' "$PROMPT_FILE" && grep -qF -- 'NOT DONE ITEMS (six)' "$PROMPT_FILE" && grep -qF -- '21af3285-0a40-490c-bfff-bc3466b6066b' "$PROMPT_FILE" && grep -qF -- '4999' "$PROMPT_FILE" && grep -qF -- 'BY LENGTH ONLY' "$PROMPT_FILE" && grep -qF -- 'NOT-PINNED' "$PROMPT_FILE" && grep -qF -- 'one-line tamper' "$PROMPT_FILE" && grep -qF -- "local model's next feed" "$PROMPT_FILE" && grep -qF -- 'proposed cell' "$PROMPT_FILE" && grep -qF -- 'DKIM-VERIFY' "$PROMPT_FILE" && grep -qF -- 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF -- 'census' "$PROMPT_FILE" && grep -qF -- 'GO / GO WITH FINDINGS / NO GO' "$PROMPT_FILE" && grep -qF -- 'Majors/Minors' "$PROMPT_FILE" && grep -qF -- 'prediction slips named BY NAME' "$PROMPT_FILE" && grep -qF -- 'round 1 of 2' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday's fifteen by-name items (head/base by two instruments; red-first as TWO kinds of red; the six tampers with T3b's 0 red as a finding; the codec's four; the verify-by-hash order with the reorder control; DECIDE 2; whitelist/strip; the two read-backs with the byte-for-byte diff; the spec; nothing outside the allowed paths; SEVEN-not-six; the 3 SKIPPED legs NOT RUN; the six NOT DONE with the facts comment by length only; NOT-PINNED as the local model's feed; the standard closing) or round 1 of 2" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  the head on origin (branch AND refs/pull/1105/head):$HEADS_NOTE"
  echo "  compare (GitHub API), develop...head:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY + STATUS 2 captures, prompt, QA project and repo all present"
  echo "  prompt carries TIER 1 and the PR tier line (#1105 KS-1175: TIER 1); names ROUND 1"
  echo "  prompt opens with the thinking directive and names both mail captures"
  echo "  READY mail and prompt both name the head in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient, the three verdict words, Majors / Minors"
  echo "  prompt names the report directory, the #1100-#1101 PRIOR REPORT, the ks1215 EXEMPLAR REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries ONE MERGE ADDENDUM line and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming e02d3ecb5; no Kam-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT / 12/15 / login_stub / SKIPPED / threadTokenMint"
  echo "  prompt forbids any seat worktree (s-a15-ks1175) and the builder's 2026-09-20_seatA-15th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the builder's items; the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS"
  echo "  prompt names the head tree, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state that PR #1105 is KS-1175 (namespace trap; KS-1105 is another ticket)"
  echo "  prompt carries Wednesday's fifteen by-name items and round 1 of 2"
  [ -n "${QAB1105_CUR_DEV:-}" ] && echo "  (develop read from the QAB1105_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1105_INDEXTS_FILE:-}" ] && echo "  (develop services/anchoring/src/index.ts read from the QAB1105_INDEXTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1105_BRIEF:-}${QAB1105_PROMPT:-}${QAB1105_HEAD:-}${QAB1105_CUR_DEV:-}${QAB1105_INDEXTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
