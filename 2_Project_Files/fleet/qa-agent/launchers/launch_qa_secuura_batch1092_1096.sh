#!/bin/bash
# launch_qa_secuura_batch1092_1096.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over FIVE file-disjoint Secuura/Blockchain PRs
#   #1092 KS-1230 @ d1c35a0c3  ks1230 vitest test: N86-1, a null allow-list FIRST of three, and three null, stored as null (admin.ts:1132)  — TIER 2 (test-only)
#   #1093 KS-1062 @ b6c29f87b  ks1062 vitest test: N88-1, every tenant skipped is counted skipped (archived ticket, NO Refs, NO key)          — TIER 2 (test-only)
#   #1094 KS-739  @ 655b83efd  ks739 jest test: N89-1, a non-JSON 422 -> 400; non-JSON 502 / 504 -> 502 (archived ticket, NO Refs, NO key)  — TIER 2 (test-only)
#   #1095 KS-1238 @ b62df6645  ks1238 vitest test: N90-1 (verify, document found, :597-:598) + N83-2 (document create, :1297)             — TIER 1 (AUTH, test-only)
#   #1096 KS-1238 + KS-1282 @ 789e6b984  ks1215 vitest test: N91-1 (:254 super-admin) + N83-6 (register LIVE+REFUSED) + N91-2 (GET :222) — TIER 1 (AUTH, test-only)
# ALL FIVE ARE TEST-ONLY: every changed path is under a src/__tests__/ directory (generator: local objects AND the PR files API; 0 product bytes,
# 0 deleted lines; #1095 and #1096 asserted by name).
# #1095's and #1096's verdicts carry the same ruling, KS-1238 COMPLETE or NOT-COMPLETE, measured against the ticket's own ask and its F-1 source; a
# COMPLETE ruling moves KS-1238 to Done + archived after the last merge (the seat's D10). KS-1282's completeness is Kam's call, not the gate's.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too (KS-1092..KS-1096 exist), two PRs share KS-1238 and #1096 also carries KS-1282; the
# READY mail AND the prompt must BOTH state which ticket(s) each of the five PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. FIVE verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 01:17:23 AEST 2026-09-20 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop 4273adfac; compare develop...head = merge_base 4273adfac, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (5 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL FIVE = tree 458cff717,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in --shared scratch clones (merge-tree chains in THREE orders:
# forward, reverse, shuffled with the tier-1 heads first; and a scratch-index composition), equal to the builder's prediction and to its local
# octopus commit 4a1fa96a5's tree. All five are byte-identical to their CANONICAL local-model patch.diff, re-applied strict by the generator in a
# plain scratch dir (#1095 = two runs in BOTH orders, #1096 = three runs in ALL SIX orders; each run alone differs and = the READY's single blob; the
# KS-1238 pair alone = 7007f002aa53), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — TWENTY-SIX paths by blob at the CURRENT develop: the 5 PR files (all at develop blobs; any PR's head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: verification.ts (:151 / :189 / :289 / :517 / :521 / :526 / :597-:598 / :1297),
# platform.ts (:222 / :239 / :254 / :491 and the other 11 guards), admin.ts, startup-migrations.ts, proxy.ts, auth.ts, index.ts, originate
# documents.ts, preflight.sh, run-shell-suites.sh, the pre-push hook, the api-gateway / originate configs, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway / originate src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-20_gate1092to1096/mail_batch1092_ready.md, the seat's READY mail (15:15:35Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the five heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all five heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and FIVE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1084-#1091 batch), the EARLIER REPORT (the #1077-#1083 batch), the
#          KS-1238 F-1 source report and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state' and
#          'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-7th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (ruleset 18499832, the order-independence blobs 156f7082 / 6adc2820 /
#          7007f002aa53, the eleven plant sha256s, the five tier-1 tamper ids, the platform.ts / verification.ts sha256s, the 13 guard lines), and the
#          prompt must ask the gate to MEASURE, not conclude, and to rule KS-1238 COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-five tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the five, which ticket(s) the PR is (PR #1092 is KS-1230 ... PR #1096 is
#          KS-1238 + KS-1282).
# exit 33: the prompt must carry Wednesday's BY-NAME items: KS-1238's comment 60c1e1f7 and the facts text, the ruling against the ask and F-1, the
#          other twelve requireSuperAdmin guards and KS-1282's completeness as Kam's call, ZERO product bytes in all five, the combined runs over the
#          WHOLE api-gateway suite, the two SHARED-LINE TAMPER PAIRS, the /unrevoke rule (must not recommend pinning either; N84-1), and the PRIOR
#          REPORT's row format.
# QAB1092_CUR_DEV (test override, --check only): stands in for origin develop. QAB1092_HEAD_1096 (test override): stands in for #1096's pinned head.
# QAB1092_VERIFTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/verification.ts (its git blob).
# A launch with any QAB1092_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1092to1096/gen_launcher_batch1092_1096.py from launch_qa_secuura_batch1084_1091.sh (asserted block
# substitutions + pins re-read + canonical-patch identity in every order + all-five tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1092_1096.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1092_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1092to1096/mail_batch1092_ready.md}"
PROMPT_FILE="${QAB1092_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_secuura-batch1092-1096.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (15:15:35Z) and re-read by the drafter (git ls-remote 01:17:23 AEST, branch AND refs/pull/N/head)
# NAMESPACE TRAP: no PR here is its own-numbered ticket; #1095 and #1096 share KS-1238 and #1096 also carries KS-1282; the ticket column is the truth (exit 32)
PRS=(
  "1092|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n86-1|d1c35a0c3b29383411c5f697f535293a99482de6"
  "1093|KS-1062|refs/heads/feature/pin-startup-migrations-all-tenants-skipped-summary-complete|b6c29f87b8c2d3956ac1b89bfe338940e109a805"
  "1094|KS-739|refs/heads/feature/pin-transfer-custody-nonjson-422-502-504-lookup|655b83efd6f4948b5e973afdbcd21456dc7f1661"
  "1095|KS-1238|refs/heads/feature/ks-1238-n90-1-n83-2-pin-verify-found-and-create-send-no-bearer|b62df66454c2f4a73c77a2168fabf7e16b3290d2"
  "1096|KS-1238+KS-1282|refs/heads/feature/ks-1238-n91-1-n83-6-n91-2-pin-platform-bearers-and-tenants-get-guard|${QAB1092_HEAD_1096:-789e6b984c1540785c8249cb2b269e5ab63c6909}"
)
DEVELOP_SHA='4273adfac57ab1a65b4a9983c566cc115faefc01'   # the pin = develop at 01:17:23 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1092-1096-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1084-1091-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1077-1083-tier1-r1/'
F1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1092to1096/mail_batch1092_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The five heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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
# develop...head = 4273adfac ahead 1 for all five PRs; files 1 each
# (git diff --name-only + rev-list, drafter 01:1x AEST; the launcher reads the compare API).
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
WANT_COMPARE="1092 $MERGE_BASE ahead=1 files=1
1093 $MERGE_BASE ahead=1 files=1
1094 $MERGE_BASE ahead=1 files=1
1095 $MERGE_BASE ahead=1 files=1
1096 $MERGE_BASE ahead=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twenty-six paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1092_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
VERIFTS = A + "src/routes/verification.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"6c048ec6a48116e296a23dc10a22a51a1c32da75": DV}, {"195a1453565d83f88072a293b26385c7f9772331": "#1092 own"}),
  A + "src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts": ({"cebfc0d469bcb80bf7676dc90934cd81186af4f5": DV}, {"c363585f6404a9b53863d76fca0afc789c46e329": "#1093 own"}),
  O + "src/__tests__/ks739-transfer-custody-lookup-4xx-mapping.test.ts":           ({"fc2a0f89e38ba9f931ed80aa3d084b2e4d0b700b": DV}, {"abe4453bb76c2651a11b22ed4419619533c3b2e5": "#1094 own"}),
  A + "src/__tests__/ks1238-hand-forwarded-routes-send-no-caller-bearer.test.ts":  ({"0a37c1d56be845f0d7658d9691a8978eb357d662": DV}, {"156f708272707fe2c13f9e5cfac9c2035bb42f9d": "#1095 own"}),
  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"e2a4b12be53be4af7a16ec6a47a9b4c189c4ad99": DV}, {"6adc2820514ee191df201c1cbfea2062c9b12f14": "#1096 own"}),
  VERIFTS:                                                                         ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  A + "src/routes/platform.ts":                                                    ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  A + "src/startup-migrations.ts":                                                 ({"ed3e521426e75910c5bf2cf07e7251f2fd8ef538": DV}, {}),
  A + "src/routes/proxy.ts":                                                       ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  A + "src/middleware/auth.ts":                                                    ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  A + "src/index.ts":                                                              ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {}),
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
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1092_VERIFTS_FILE", "") if f == VERIFTS else ""
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all five heads: each merged tree = its head tree, a fast-forward: #1092 d041e0287, #1093 fdd54f5b9, #1094 9acede956, #1095 a2880e5ea, #1096 019bd34ca; all five together 458cff7174a2c9090a14c9d5ed71e3a17c3792e4, drafter tree-hash, three-order scratch-clone merges and scratch-index composition = builder prediction; git ls-remote)"); sys.exit(0)
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
tail = "the gate merges the then-current develop onto EACH of the five heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all five 458cff717) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway and originate src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1092 KS-1230: TIER 2' "$PROMPT_FILE" && grep -qF '#1093 KS-1062: TIER 2' "$PROMPT_FILE" && grep -qF '#1094 KS-739: TIER 2' "$PROMPT_FILE" && grep -qF '#1095 KS-1238: TIER 1' "$PROMPT_FILE" && grep -qF '#1096 KS-1238 + KS-1282: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1095 + #1096 T1, #1092-#1094 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1092-#1096 (five PRs; tier 1 = #1095 + #1096 KS-1238)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'FIVE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and FIVE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$F1_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the F-1 source $F1_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'PREFLIGHT INCOMPLETE' "$PROMPT_FILE" && grep -qF 'PREFLIGHT INCOMPLETE' "$BRIEF" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state' "$PROMPT_FILE" && grep -qF 'mergeable_state' "$BRIEF" && grep -qF 'zero product bytes' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-7th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-7th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF -- '18499832' "$PROMPT_FILE" && grep -qF -- '18499832' "$BRIEF" && grep -qF -- '156f708272707fe2c13f9e5cfac9c2035bb42f9d' "$PROMPT_FILE" && grep -qF -- '156f708272707fe2c13f9e5cfac9c2035bb42f9d' "$BRIEF" && grep -qF -- '6adc2820514ee191df201c1cbfea2062c9b12f14' "$PROMPT_FILE" && grep -qF -- '6adc2820514ee191df201c1cbfea2062c9b12f14' "$BRIEF" && grep -qF -- '7007f002aa53' "$PROMPT_FILE" && grep -qF -- '7007f002aa53' "$BRIEF" && grep -qF -- '928cd340d396' "$PROMPT_FILE" && grep -qF -- '928cd340d396' "$BRIEF" && grep -qF -- '166ac35794bd' "$PROMPT_FILE" && grep -qF -- '166ac35794bd' "$BRIEF" && grep -qF -- '37872084b6f9' "$PROMPT_FILE" && grep -qF -- '37872084b6f9' "$BRIEF" && grep -qF -- 'f645833929d6' "$PROMPT_FILE" && grep -qF -- 'f645833929d6' "$BRIEF" && grep -qF -- '2265f3417115' "$PROMPT_FILE" && grep -qF -- '2265f3417115' "$BRIEF" && grep -qF -- '5cab73f735fe' "$PROMPT_FILE" && grep -qF -- '5cab73f735fe' "$BRIEF" && grep -qF -- '33f70ca97352' "$PROMPT_FILE" && grep -qF -- '33f70ca97352' "$BRIEF" && grep -qF -- 'd5188b1d3fb6' "$PROMPT_FILE" && grep -qF -- 'd5188b1d3fb6' "$BRIEF" && grep -qF -- '8dd8cfd7bca2' "$PROMPT_FILE" && grep -qF -- '8dd8cfd7bca2' "$BRIEF" && grep -qF -- '23b787888893' "$PROMPT_FILE" && grep -qF -- '23b787888893' "$BRIEF" && grep -qF -- 'ecda4905a89e' "$PROMPT_FILE" && grep -qF -- 'ecda4905a89e' "$BRIEF" && grep -qF -- 'RAW598' "$PROMPT_FILE" && grep -qF -- 'RAW598' "$BRIEF" && grep -qF -- 'RAW1297' "$PROMPT_FILE" && grep -qF -- 'RAW1297' "$BRIEF" && grep -qF -- 'REFRESHNOAUTH' "$PROMPT_FILE" && grep -qF -- 'REFRESHNOAUTH' "$BRIEF" && grep -qF -- 'IV_REGLIVEONLY' "$PROMPT_FILE" && grep -qF -- 'IV_REGLIVEONLY' "$BRIEF" && grep -qF -- 'TENANTSGETUNGUARDED' "$PROMPT_FILE" && grep -qF -- 'TENANTSGETUNGUARDED' "$BRIEF" && grep -qF -- '7d04a92ca724' "$PROMPT_FILE" && grep -qF -- '7d04a92ca724' "$BRIEF" && grep -qF -- '43d29242eda1' "$PROMPT_FILE" && grep -qF -- '43d29242eda1' "$BRIEF" && grep -qF -- '222, 239, 284, 301, 320, 339, 362, 767, 782, 792, 806, 832, 859' "$PROMPT_FILE" && grep -qF -- '222, 239, 284, 301, 320, 339, 362, 767, 782, 792, 806, 832, 859' "$BRIEF" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF '458cff7174a2c9090a14c9d5ed71e3a17c3792e4' "$PROMPT_FILE" && grep -qF '4a1fa96a5fe9240e3f5f26b07b3382fd1eccc92b' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-five tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1092 is KS-1230.' "$PROMPT_FILE" && grep -F '| #1092 | ' "$BRIEF" | grep -qF 'KS-1230' && grep -qF 'PR #1093 is KS-1062.' "$PROMPT_FILE" && grep -F '| #1093 | ' "$BRIEF" | grep -qF 'KS-1062' && grep -qF 'PR #1094 is KS-739.' "$PROMPT_FILE" && grep -F '| #1094 | ' "$BRIEF" | grep -qF 'KS-739' && grep -qF 'PR #1095 is KS-1238.' "$PROMPT_FILE" && grep -F '| #1095 | ' "$BRIEF" | grep -qF 'KS-1238' && grep -qF 'PR #1096 is KS-1238 + KS-1282.' "$PROMPT_FILE" && grep -F '| #1096 | ' "$BRIEF" | grep -qF 'KS-1238' && grep -F '| #1096 | ' "$BRIEF" | grep -qF 'KS-1282' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket(s) each PR is (PR #1092 is KS-1230 ... PR #1096 is KS-1238 + KS-1282) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
grep -qF -- '60c1e1f7' "$PROMPT_FILE" && grep -qF -- 'KS-1238 COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" && grep -qF -- 'FACTS-COMMENT TEXT' "$PROMPT_FILE" && grep -qF -- 'ITS F-1 SOURCE' "$PROMPT_FILE" && grep -qF -- '239, 284, 301, 320, 339, 362, 767, 782, 792, 806, 832, 859' "$PROMPT_FILE" && grep -qF -- 'completeness is Kam' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes in all five' "$PROMPT_FILE" && grep -qF -- 'WHOLE api-gateway suite' "$PROMPT_FILE" && grep -qF -- 'SHARED-LINE TAMPER PAIRS' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'N84-1' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday's by-name items (KS-1238 comment 60c1e1f7 and the facts text, the ruling against the ask and F-1, the other twelve guards and KS-1282 as Kam's call, ZERO product bytes in all five, the whole-suite combined runs, the shared-line pairs, the /unrevoke rule, the PRIOR REPORT's row format)" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  five heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1095 + #1096 T1, #1092-#1094 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all five heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, FIVE verdict lines"
  echo "  prompt names the report directory, the #1084-#1091 batch PRIOR REPORT, the EARLIER REPORT, the F-1 source and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-20_seatB-7th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-five tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket(s) each of the five PRs is (namespace trap; #1095 and #1096 both KS-1238, #1096 also KS-1282)"
  echo "  prompt carries Wednesday's by-name items: 60c1e1f7 + facts text, ask + F-1, the other twelve guards, KS-1282 = Kam's call, zero product bytes x5, whole-suite combined runs, shared-line pairs, no /unrevoke pin, the row format"
  [ -n "${QAB1092_CUR_DEV:-}" ] && echo "  (develop read from the QAB1092_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1092_VERIFTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/verification.ts read from the QAB1092_VERIFTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1092_BRIEF:-}${QAB1092_PROMPT:-}${QAB1092_HEAD_1096:-}${QAB1092_CUR_DEV:-}${QAB1092_VERIFTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
