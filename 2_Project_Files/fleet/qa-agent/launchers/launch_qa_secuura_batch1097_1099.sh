#!/bin/bash
# launch_qa_secuura_batch1097_1099.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over THREE file-disjoint Secuura/Blockchain PRs
#   #1097 KS-1230 @ f53642179  ks1230 vitest test: N92-1, a null allow-list FIRST of two (mixed) and FIRST of four, stored as null (admin.ts:1132) — TIER 2 (test-only)
#   #1098 KS-1062 @ efce14bed  ks1062 vitest test: N93-1, one tenant skipped counted; every tenant failed = INCOMPLETE (archived ticket, NO Refs, NO key) — TIER 2
#   #1099 KS-1238 + KS-1282 @ b68aaf9b4  ks1215 vitest test: N95-1 (the admin-shadow 401, admin.ts :1366 / :1428) + N96-1a + N96-1b (eleven
#         requireSuperAdmin guards, platform.ts) — TIER 1 (AUTH, test-only)
# ALL THREE ARE TEST-ONLY: every changed path is under api-gateway src/__tests__/ (generator: local objects AND the PR files API; 0 product bytes,
# 0 deleted lines; #1099 asserted by name).
# #1099's verdict carries the ruling KS-1238 COMPLETE or NOT-COMPLETE, by name, against the ticket's own ask, its F-1 source and the prior gate's
# comment 77f4ec90; a COMPLETE ruling moves KS-1238 to Done + archived after the last merge (the seat's D11). KS-1282's completeness is Kam's call.
# NAMESPACE TRAP: the PR numbers are other tickets' numbers too (KS-1097..KS-1099 exist) and #1099 carries two tickets; the READY mail AND the prompt
# must BOTH state which ticket(s) each of the three PRs is, or the launch refuses (exit 32).
# Batched under Kam's 09:22 rule. THREE verdicts, one per head; one PR failing does not block the others. Merge authority for each: WEDNESDAY'S signed GO
# naming its head, under Kam's TESTED grant (exit 26).
#
# THE SHAPE, re-read live 04:41:46 AEST 2026-09-20 (git ls-remote develop + refs/pull/N/head + branch) and again by the generator: each PR is ONE commit
# whose parent IS develop c87458bdd; compare develop...head = merge_base c87458bdd, ahead 1, files 1 each (asserted per PR, exit 10).
# Pairwise file-disjoint (3 files, all modified, 0 new). Each PR over develop is a fast-forward (merged tree = head tree). ALL THREE = tree 706de8305,
# re-derived by the generator by pure tree hashing (no git write) AND by the drafter in --shared scratch clones (merge-tree chains in THREE orders:
# forward, reverse, tier-1-first; and a scratch-index composition), equal to the builder's prediction and to its local octopus commit f893a92cf's
# tree. All three are byte-identical to their CANONICAL local-model patch.diff, re-applied strict by the generator in a plain scratch dir (#1099 =
# three runs in ALL SIX orders; every proper subset in every order = the READY's item-0 blob), each reverse-applied control refusing.
#
# The develop pin is judged by CONTENT — TWENTY-ONE paths by blob at the CURRENT develop: the 3 PR files (all at develop blobs; any PR's head blob
# -> exit 19 LANDED, naming the PR), and what the gate runs or reads: platform.ts (the 13 requireSuperAdmin guards, SUPER_ROLES, the pg.Pool
# routes), admin.ts (:1132, :1366, :1428), startup-migrations.ts, proxy.ts (:472 / :504), verification.ts, auth.ts, index.ts (the mount order),
# preflight.sh, run-shell-suites.sh, the pre-push hook, the api-gateway configs incl. vitest.setup.ts, the Dev package.json + lock,
# eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md, the seat's READY mail (18:38:22Z) captured verbatim by message id from wednesday-agent@.
#
# exit 6:  any of the three heads is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR's own tier line.
# exit 20: the READY mail AND the prompt must name all three heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and THREE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1092-#1096 batch), the EARLIER REPORT (the #1084-#1091 batch), the
#          KS-1238 F-1 source report and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR's merge authority, with no Kam's-tap and no "not ... alone" condition.
# exit 27: the READY mail AND the prompt must BOTH carry the seat's own words: 'PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state' and
#          'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-8th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY mail AND the prompt must BOTH carry the seat's items (ruleset 18499832, the order-independence blobs, the 17 plant sha256s, the
#          tamper ids, the develop sha256s, the census words), and the prompt must ask the gate to MEASURE, not conclude, and to rule KS-1238
#          COMPLETE or NOT-COMPLETE.
# exit 31: the prompt must name the all-three tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, and a loopback
#          GATEWAY_URL for any preflight run.
# exit 32: the READY mail AND the prompt must BOTH name, for EACH of the three, which ticket(s) the PR is (PR #1097 is KS-1230 ... PR #1099 is
#          KS-1238 + KS-1282).
# exit 33: the prompt must carry Wednesday's ELEVEN BY-NAME items: tier + round 1 of 2 + ZERO product bytes on #1099; ALL SIX orders; the WHOLE
#          api-gateway suite combined runs + the SHARED-LINE TAMPER PAIR; KS-1238 COMPLETE or NOT-COMPLETE BY NAME with comment 77f4ec90, its
#          one-cell-per-path sentence and the FACTS-COMMENT TEXT; the eleven guard lines + KS-1282 completeness as Kam's call; NOTHING ABOUT O-1 +
#          no /unrevoke pin; the real Postgres on 127.0.0.1:5432; attachmentsForURL + includeArchived; the NOT-PINNED row format; the MERGE ADDENDUM.
# QAB1097_CUR_DEV (test override, --check only): stands in for origin develop. QAB1097_HEAD_1099 (test override): stands in for #1099's pinned head.
# QAB1097_PLATFORMTS_FILE (test fixture, --check only): a local file stands in for develop services/api-gateway/src/routes/platform.ts (its git blob).
# A launch with any QAB1097_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-20_gate1097to1099/gen_launcher_batch1097_1099.py from launch_qa_secuura_batch1092_1096.sh (asserted block
# substitutions + pins re-read + canonical-patch identity in every order + all-three tree re-derived + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_batch1097_1099.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1097_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md}"
PROMPT_FILE="${QAB1097_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_secuura-batch1097-1099.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head — pinned from the seat READY (18:38:22Z) and re-read by the drafter (git ls-remote 04:41:46 AEST, branch AND refs/pull/N/head)
# NAMESPACE TRAP: no PR here is its own-numbered ticket; #1098 is archived KS-1062 (no Refs); #1099 carries KS-1238 AND KS-1282; the ticket column is the truth (exit 32)
PRS=(
  "1097|KS-1230|refs/heads/feature/ks-1230-put-apiadminsettings-stores-a-connectors-n92-1|f5364217952c1cb4d3755fbf8604b3edde124c42"
  "1098|KS-1062|refs/heads/feature/pin-startup-migrations-one-skipped-counted-and-all-failed-incomplete|efce14bed4a8adda15bca124fa60ae7d894fa6a6"
  "1099|KS-1238+KS-1282|refs/heads/feature/ks-1238-n95-1-n96-1-pin-admin-shadow-401-and-superadmin-guards|${QAB1097_HEAD_1099:-b68aaf9b4581e67369be33d8ebcf4d61886c039b}"
)
DEVELOP_SHA='c87458bdd8a9dd5ae3a082612e467cda5539aebc'   # the pin = develop at 04:41:46 AEST; every head's merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1097-1099-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1092-1096-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-19-batch1084-1091-tier1-r1/'
F1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1215-1034-e4624218b-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1097to1099/mail_batch1097_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The three heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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
# develop...head = c87458bdd ahead 1 for all three PRs; files 1 each
# (git diff --name-only + rev-list, drafter 04:4x AEST; the launcher reads the compare API).
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
WANT_COMPARE="1097 $MERGE_BASE ahead=1 files=1
1098 $MERGE_BASE ahead=1 files=1
1099 $MERGE_BASE ahead=1 files=1"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twenty-one paths by PATH BLOB at the CURRENT develop (no region judgement), then — if
# develop moved — the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1097_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
PLATFORMTS = A + "src/routes/platform.ts"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  A + "src/__tests__/ks1230-settings-write-validates-allowed-document-types.test.ts": ({"195a1453565d83f88072a293b26385c7f9772331": DV}, {"026197fbaeff433b2b92d9fad9d9527a2e7ac212": "#1097 own"}),
  A + "src/__tests__/ks1062-startup-migrations-tenant-summary-first-error.test.ts": ({"c363585f6404a9b53863d76fca0afc789c46e329": DV}, {"0ec64a16e77169129d01cb95cd1f008b050a5dcc": "#1098 own"}),
  A + "src/__tests__/ks1215-the-connector-branch-never-carries-the-callers-bearer.test.ts": ({"6adc2820514ee191df201c1cbfea2062c9b12f14": DV}, {"fe235c8aa1d85d28d73a4853890c840bd59e0a7a": "#1099 own"}),
  PLATFORMTS:                                                                      ({"b80a8cd8d4e1af5a944817227f5ee6612c793954": DV}, {}),
  A + "src/routes/admin.ts":                                                       ({"20c8a088f5dc34fc1563b3907e7c816e1b9fa3d3": DV}, {}),
  A + "src/startup-migrations.ts":                                                 ({"ed3e521426e75910c5bf2cf07e7251f2fd8ef538": DV}, {}),
  A + "src/routes/proxy.ts":                                                       ({"795ae7ca3bdc76be3e563e87fc34a8cc221e5632": DV}, {}),
  A + "src/routes/verification.ts":                                                ({"f888e8cd0bd10c98a508542d75902ab122595157": DV}, {}),
  A + "src/middleware/auth.ts":                                                    ({"bf09d315a64443b7f02bc27a74366b7a7f1dae81": DV}, {}),
  A + "src/index.ts":                                                              ({"db127dbfa5dd899b0a8e0d844690890d91e27f10": DV}, {}),
  A + "package.json":                                                              ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                          ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  A + "vitest.setup.ts":                                                           ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  A + "tsconfig.json":                                                             ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  D + "scripts/preflight/preflight.sh":                                            ({"712f895362e2c8d1ead6fd09ac257d7bce212948": DV}, {}),
  D + "scripts/run-shell-suites.sh":                                               ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  ".githooks/pre-push":                                                            ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  D + "package.json":                                                              ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                         ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                         ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                                    ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
}
# No REGION judgement: every path is judged by exact blob (a develop move of any judged path refuses, exit 18; any PR head blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QAB1097_PLATFORMTS_FILE", "") if f == PLATFORMTS else ""
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all three heads: each merged tree = its head tree, a fast-forward: #1097 dff1aafa3, #1098 9da0c747c, #1099 c65575ff9; all three together 706de83052728ddfe4c581e378f708fec2338b80, drafter tree-hash, three-order scratch-clone merges and scratch-index composition = builder prediction; git ls-remote)"); sys.exit(0)
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
           A + "vitest.setup.ts",
           A + "tsconfig.json",
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
tail = "the gate merges the then-current develop onto EACH of the three heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all three 706de8305) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway src/ + config, packages/shared src/, scripts/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1097 KS-1230: TIER 2' "$PROMPT_FILE" && grep -qF '#1098 KS-1062: TIER 2' "$PROMPT_FILE" && grep -qF '#1099 KS-1238 + KS-1282: TIER 1' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR's own tier line (#1099 T1, #1097 + #1098 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1097-#1099 (three PRs; tier 1 = #1099 KS-1238 + KS-1282)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'THREE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and THREE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" && grep -qF "$F1_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT, the F-1 source $F1_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam's-tap / not-alone condition" >&2; exit 26; }
grep -qF 'PREFLIGHT INCOMPLETE' "$PROMPT_FILE" && grep -qF 'PREFLIGHT INCOMPLETE' "$BRIEF" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state' "$PROMPT_FILE" && grep -qF 'mergeable_state' "$BRIEF" && grep -qF 'zero product bytes' "$PROMPT_FILE" && grep -qF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's words: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-8th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat's 2026-09-20_seatB-8th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
grep -qF -- '18499832' "$PROMPT_FILE" && grep -qF -- '18499832' "$BRIEF" && grep -qF -- 'fe235c8aa1d85d28d73a4853890c840bd59e0a7a' "$PROMPT_FILE" && grep -qF -- 'fe235c8aa1d85d28d73a4853890c840bd59e0a7a' "$BRIEF" && grep -qF -- 'f9bff1b332af' "$PROMPT_FILE" && grep -qF -- 'f9bff1b332af' "$BRIEF" && grep -qF -- '63d5c6876d82' "$PROMPT_FILE" && grep -qF -- '63d5c6876d82' "$BRIEF" && grep -qF -- '7c56fdbdcfde' "$PROMPT_FILE" && grep -qF -- '7c56fdbdcfde' "$BRIEF" && grep -qF -- '86d7faeae0e3' "$PROMPT_FILE" && grep -qF -- '86d7faeae0e3' "$BRIEF" && grep -qF -- 'f47c8eadf237' "$PROMPT_FILE" && grep -qF -- 'f47c8eadf237' "$BRIEF" && grep -qF -- '6292bafe5906' "$PROMPT_FILE" && grep -qF -- '6292bafe5906' "$BRIEF" && grep -qF -- '6ca6003490e2' "$PROMPT_FILE" && grep -qF -- '6ca6003490e2' "$BRIEF" && grep -qF -- '7cbea3850ecc' "$PROMPT_FILE" && grep -qF -- '7cbea3850ecc' "$BRIEF" && grep -qF -- 'caa3971a4e3a' "$PROMPT_FILE" && grep -qF -- 'caa3971a4e3a' "$BRIEF" && grep -qF -- 'c423a8f77ccc' "$PROMPT_FILE" && grep -qF -- 'c423a8f77ccc' "$BRIEF" && grep -qF -- '41234d5f1db7' "$PROMPT_FILE" && grep -qF -- '41234d5f1db7' "$BRIEF" && grep -qF -- '1a8800d9728e' "$PROMPT_FILE" && grep -qF -- '1a8800d9728e' "$BRIEF" && grep -qF -- 'dec8abd6c60f' "$PROMPT_FILE" && grep -qF -- 'dec8abd6c60f' "$BRIEF" && grep -qF -- 'e091c63c14b6' "$PROMPT_FILE" && grep -qF -- 'e091c63c14b6' "$BRIEF" && grep -qF -- '465234ebec8f' "$PROMPT_FILE" && grep -qF -- '465234ebec8f' "$BRIEF" && grep -qF -- 'b31f6c613735' "$PROMPT_FILE" && grep -qF -- 'b31f6c613735' "$BRIEF" && grep -qF -- 'f1c507f33c70' "$PROMPT_FILE" && grep -qF -- 'f1c507f33c70' "$BRIEF" && grep -qF -- 'b040c368c317' "$PROMPT_FILE" && grep -qF -- 'b040c368c317' "$BRIEF" && grep -qF -- '75cd534254e4' "$PROMPT_FILE" && grep -qF -- '75cd534254e4' "$BRIEF" && grep -qF -- 'b9010e9ee952' "$PROMPT_FILE" && grep -qF -- 'b9010e9ee952' "$BRIEF" && grep -qF -- '4d76f733a198' "$PROMPT_FILE" && grep -qF -- '4d76f733a198' "$BRIEF" && grep -qF -- 'ad7aa5682a33' "$PROMPT_FILE" && grep -qF -- 'ad7aa5682a33' "$BRIEF" && grep -qF -- '8d871fb0274e' "$PROMPT_FILE" && grep -qF -- '8d871fb0274e' "$BRIEF" && grep -qF -- 'FIRSTOF2NULLMIXED' "$PROMPT_FILE" && grep -qF -- 'FIRSTOF2NULLMIXED' "$BRIEF" && grep -qF -- 'FIRSTOF4NULL' "$PROMPT_FILE" && grep -qF -- 'FIRSTOF4NULL' "$BRIEF" && grep -qF -- 'ONESKIPPED' "$PROMPT_FILE" && grep -qF -- 'ONESKIPPED' "$BRIEF" && grep -qF -- 'ALLFAILED' "$PROMPT_FILE" && grep -qF -- 'ALLFAILED' "$BRIEF" && grep -qF -- 'ADMINSHADOW1366' "$PROMPT_FILE" && grep -qF -- 'ADMINSHADOW1366' "$BRIEF" && grep -qF -- 'ADMINSHADOW1428' "$PROMPT_FILE" && grep -qF -- 'ADMINSHADOW1428' "$BRIEF" && grep -qF -- '7d04a92ca724' "$PROMPT_FILE" && grep -qF -- '7d04a92ca724' "$BRIEF" && grep -qF -- '6a733afc58fd' "$PROMPT_FILE" && grep -qF -- '6a733afc58fd' "$BRIEF" && grep -qF -- '623a99b9531e' "$PROMPT_FILE" && grep -qF -- '623a99b9531e' "$BRIEF" && grep -qF -- 'STOP-class 0' "$PROMPT_FILE" && grep -qF -- 'STOP-class 0' "$BRIEF" && grep -qF -- '76 runs' "$PROMPT_FILE" && grep -qF -- '76 runs' "$BRIEF" && grep -qF -- '127.0.0.1:1' "$PROMPT_FILE" && grep -qF -- '127.0.0.1:1' "$BRIEF" && grep -qF -- ':5432' "$PROMPT_FILE" && grep -qF -- ':5432' "$BRIEF" && grep -qF -- '667' "$PROMPT_FILE" && grep -qF -- '667' "$BRIEF" && grep -qF -- '671' "$PROMPT_FILE" && grep -qF -- '671' "$BRIEF" && grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'COMPLETE or NOT-COMPLETE' "$PROMPT_FILE" \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH carry the seat's items, or the prompt does not say MEASURE, not conclude and rule KS-1238 COMPLETE or NOT-COMPLETE" >&2; exit 30; }
grep -qF '706de83052728ddfe4c581e378f708fec2338b80' "$PROMPT_FILE" && grep -qF 'f893a92cf105a4faaacb7c48b647efe3e8fedbec' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the all-three tree in full, the octopus commit, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1097 is KS-1230.' "$PROMPT_FILE" && grep -F '| #1097 | ' "$BRIEF" | grep -qF 'KS-1230' && grep -qF 'PR #1098 is KS-1062.' "$PROMPT_FILE" && grep -F '| #1098 | ' "$BRIEF" | grep -qF 'KS-1062' && grep -qF 'PR #1099 is KS-1238 + KS-1282.' "$PROMPT_FILE" && grep -F '| #1099 | ' "$BRIEF" | grep -qF 'KS-1238' && grep -F '| #1099 | ' "$BRIEF" | grep -qF 'KS-1282' \
  || { echo "REFUSING: the READY mail and the prompt do not BOTH state which ticket(s) each PR is (PR #1097 is KS-1230, PR #1098 is KS-1062, PR #1099 is KS-1238 + KS-1282) — the PR numbers are other tickets' numbers too" >&2; exit 32; }
grep -qF -- 'round 1 of 2' "$PROMPT_FILE" && grep -qF -- 'ZERO product bytes on #1099' "$PROMPT_FILE" && grep -qF -- 'ALL SIX orders' "$PROMPT_FILE" && grep -qF -- 'WHOLE api-gateway suite' "$PROMPT_FILE" && grep -qF -- 'SHARED-LINE TAMPER PAIR' "$PROMPT_FILE" && grep -qF -- 'KS-1238 COMPLETE or NOT-COMPLETE, BY NAME' "$PROMPT_FILE" && grep -qF -- '77f4ec90' "$PROMPT_FILE" && grep -qF -- 'One cell per path pinning that a connector key alone gets 401 there closes it' "$PROMPT_FILE" && grep -qF -- 'FACTS-COMMENT TEXT' "$PROMPT_FILE" && grep -qF -- ':284 :301 :320 :339 :362 :767 :782 :792 :806 :832 :859' "$PROMPT_FILE" && grep -qF -- 'completeness is Kam' "$PROMPT_FILE" && grep -qF -- 'NOTHING ABOUT O-1' "$PROMPT_FILE" && grep -qF -- 'must not recommend pinning either' "$PROMPT_FILE" && grep -qF -- 'a real Postgres listens on 127.0.0.1:5432' "$PROMPT_FILE" && grep -qF -- 'attachmentsForURL' "$PROMPT_FILE" && grep -qF -- 'includeArchived' "$PROMPT_FILE" && grep -qF -- 'SAME ROW FORMAT as the PRIOR REPORT' "$PROMPT_FILE" && grep -qF -- 'ONE MERGE ADDENDUM line PER PR' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not carry Wednesday's eleven by-name items (tier + round 1 of 2 + zero product bytes on #1099, all six orders, whole-suite combined runs + the shared-line pair, KS-1238 by name with 77f4ec90 + its one-cell-per-path sentence + facts text, the eleven guards + KS-1282 as Kam's call, nothing about O-1 + no /unrevoke pin, the real Postgres on :5432, attachmentsForURL + includeArchived, the NOT-PINNED row format, the merge addendum)" >&2; exit 33; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  three heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY mail, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR's tier (#1099 T1, #1097 + #1098 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY mail and prompt both name all three heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, THREE verdict lines"
  echo "  prompt names the report directory, the #1092-#1096 batch PRIOR REPORT, the EARLIER REPORT, the F-1 source and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam's-tap or not-alone condition"
  echo "  READY mail and prompt BOTH carry: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat's 2026-09-20_seatB-8th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY mail and prompt BOTH carry the seat's items; the prompt says MEASURE, not conclude, and rules KS-1238 COMPLETE or NOT-COMPLETE"
  echo "  prompt names the all-three tree, the octopus commit, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY mail and prompt BOTH state which ticket(s) each of the three PRs is (namespace trap; #1098 archived KS-1062, #1099 KS-1238 + KS-1282)"
  echo "  prompt carries Wednesday's eleven by-name items: tier/round/zero bytes, six orders, whole-suite runs + shared-line pair, KS-1238 by name (77f4ec90), eleven guards + Kam's call, nothing about O-1, Postgres :5432 isolation, link hygiene, NOT-PINNED, addendum"
  [ -n "${QAB1097_CUR_DEV:-}" ] && echo "  (develop read from the QAB1097_CUR_DEV test override, not ls-remote)"
  [ -n "${QAB1097_PLATFORMTS_FILE:-}" ] && echo "  (develop services/api-gateway/src/routes/platform.ts read from the QAB1097_PLATFORMTS_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1097_BRIEF:-}${QAB1097_PROMPT:-}${QAB1097_HEAD_1099:-}${QAB1097_CUR_DEV:-}${QAB1097_PLATFORMTS_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
