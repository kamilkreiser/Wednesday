#!/bin/bash
# launch_qa_secuura_batch1102_1104.sh — cross-project QA agent, ONE BATCHED ROUND 1 gate at the TIER 1 floor over THREE file-disjoint Secuura/Blockchain PRs
#   #1102 KS-1275 @ f5a599b07  originate JEST test: ORDER-1, LIFECYCLE_EVENT_ACTIONS declared in ONE order — TIER 2 (test-only), pushed FIRST
#   #1103 KS-1203 @ 47593b77b  api-gateway VITEST test: UNTYPED-1, an untyped body admits with an EMPTY docType and never consults the catalogue
#         (enforcement.ts:96 enforceDocumentTypeRules, :100 the spellings, :116 the untyped return) — TIER 1 (ALLOW-LIST ENFORCEMENT surface, test-only)
#   #1104 KS-1272 @ 9b668edba  api-gateway CODE PATCH: UUID-DEDUP-1, ONE product line (startup-migrations.ts:1077 COALESCE -> IS NOT DISTINCT FROM,
#         the :473 CORE_MIGRATIONS twin UNCHANGED) + ONE new test file (85 lines) — TIER 2 (a migration statement), pushed LAST
# #1102 and #1103 are TEST-ONLY (files API + local diff-tree: 0 product bytes, 0 deleted lines); #1104 is exactly `1 1` on the product file + `85 0`
# on the new test (deletions total 1).
# EVERY VALUE HERE IS THE SEAT MEASUREMENT RE-DERIVED BY THE DRAFTER, never adopted: the three heads by ls-remote (branch AND refs/pull/N/head) and
# local object reads; the per-PR trees and blobs by diff-tree; the batch tree by chained merge-tree in a --shared scratch clone in ALL SIX orders
# (predict_batch_scratch.out); the three canonical patches re-applied in a plain scratch dir (PR1 strict, PR2 strict rc 128 then --recount, PR3
# strict) each hashing to the head blob (measure_patches.out); the 85-vs-86-line checker variant diffed (one unused `const summary` declaration).
# MG-1 THIS ROUND: merge11.py wants exactly ONE equality target PER PR FILE (1 / 1 / 2) — the #1104 addendum line carries TWO (exit 25).
# Batched under Kam 2026-09-18 standing rule. THREE verdicts, one per head; one PR failing does not block the others. Merge authority for each:
# WEDNESDAY'S signed GO naming its head, under Kam TESTED grant (exit 26).
#
# THE SHAPE, re-read live 2026-09-20T13:06Z and 13:10Z (git ls-remote develop + refs/pull/N/head + branch): each PR is ONE commit whose parent IS
# develop dc061f2bb; compare develop...head = merge_base dc061f2bb, ahead 1, files 1 / 1 / 2 (asserted per PR, exit 10).
# Pairwise file-disjoint (4 paths, 3 modified + 1 new, overlap 0). Each PR over develop is a fast-forward (merged tree = head tree). ALL THREE =
# tree d0c8bfd095b65861efc1a4e8524017235b42e382 in all six orders; PR1+PR2 = d2387eabdba1 in both orders.
#
# The develop pin is judged by CONTENT — paths by blob at the CURRENT develop: the 4 PR paths (the 3 develop-side blobs; the new test ABSENT at
# develop; any PR head blob -> exit 19 LANDED, naming the PR), and what the gate runs or reads: enforcement.ts (the #1103 tamper file),
# enforcement.test.ts (the :148 develop cover), lifecycleActions.ts (the #1102 tamper file), db.retry.test.ts (the LOAD-1 file), the platform
# schema SQL (the semantic note), the api-gateway and originate configs, preflight.sh, run-shell-suites.sh, the pre-push hook, the Dev package.json
# + lock, eslint.config.mjs, BACKLOG.md.
# GUARDED: api-gateway src/ + config, originate src/ + config, packages/shared src/, scripts/, .githooks/, docker/init-platform/, the Dev
# package.json + lock, eslint.config.mjs, BACKLOG.md.
#
# SOURCE = gatesets/2026-09-20_gate1102to1104/mail_batch1102_ready.md, the seat's THREE READY mails (12:56:33Z, 13:02:49Z, 13:09:38Z) + the
# 12:46:17Z STATUS mail, each captured verbatim by message id from wednesday-agent@ and combined in PR order.
#
# exit 6:  any head is not at its branch AND at refs/pull/N/head on origin (the refusal names the PR).
# exit 7:  the prompt must carry the TIER 1 floor AND each PR own tier line.
# exit 20: the READY capture AND the prompt must name all three heads in full.
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY.
# exit 23: the prompt must carry the exact batch verdict subject prefix, coagent@ as sender, wednesday-agent@ as recipient, and THREE verdict lines.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (the #1100-#1101 batch), the EARLIER REPORT (the #1097-#1099 batch) and
#          NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM per PR with ONE equality target PER PR FILE (two for #1104) and the CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as each PR merge authority, with no Kam-tap and no "not ... alone" condition.
# exit 27: the READY capture AND the prompt must BOTH carry the seat own words: 'PREFLIGHT INCOMPLETE', 'login_stub', 'mergeable_state' and
#          'zero product bytes'.
# exit 28: the prompt must forbid entering any seat worktree and writing in the seat 2026-09-20_seatB-10th history.
# exit 29: the prompt must require every listener the gate starts ENDED BY PID, with a census (KS-1201).
# exit 30: the READY capture AND the prompt must BOTH carry the seat items (ruleset 18499832, the per-PR and batch trees, the head blobs, the four
#          plant sha256s, the tamper ids, the develop byte counts, the :116/:136 twin, the :148 develop cover, the 85/86-line finding, the :473/:1077
#          twin, the suite counts, the census words), and the prompt must ask the gate to MEASURE, not conclude, and to RULE WHETHER IT BLOCKS.
# exit 31: the prompt must name the batch tree in full, the NOT-PINNED list with a proposed cell per row, and a loopback GATEWAY_URL for any
#          preflight run.
# exit 32: the READY capture AND the prompt must BOTH name, for EACH of the three, which ticket the PR is (#1102 KS-1275, #1103 KS-1203, #1104 KS-1272).
# exit 33: the prompt must carry Wednesday BY-NAME items: tier + round 1 of 2 + ONE product line on #1104; ALL SIX MERGE ORDERS; the :116-not-:136
#          proof; the develop cover at enforcement.test.ts:148 as pre-existing coverage, NOT a regression; the 85-line head, not the checker's
#          86-line variant; the 5-space twin at :473; IS NOT DISTINCT FROM vs COALESCE with uuid NOT NULL; db.retry re-run serial + ratio, RULE
#          WHETHER IT BLOCKS; the real Postgres on 127.0.0.1:5432; census rule v2 + originate REPORTS only; attachmentsForURL + includeArchived; the
#          NOT-PINNED row format; ONE MERGE ADDENDUM line PER PR; NOTHING ABOUT O-1.
# QAB1102_CUR_DEV (test override, --check only): stands in for origin develop. QAB1102_HEAD_1104 (test override): stands in for #1104 pinned head.
# A launch with any QAB1102_* override set refuses (exit 16).
#
# Drafted by hand from launch_qa_secuura_batch1100_1101.sh (block substitutions + pins re-read + canonical-patch identity + batch tree re-derived +
# bash -n); the measurements are in gatesets/2026-09-20_gate1102to1104/.
#
# Usage: launch_qa_secuura_batch1102_1104.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..33 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QAB1102_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1102to1104/mail_batch1102_ready.md}"
PROMPT_FILE="${QAB1102_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-20_secuura-batch1102-1104.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
# n|ticket|branch|head|files — pinned from the seat READYs and re-read by the drafter (git ls-remote 13:06Z + 13:10Z, branch AND refs/pull/N/head)
PRS=(
  "1102|KS-1275|refs/heads/feature/ks-1275-published-post-lifecycle-events-description-still-enumerates-order-1|f5a599b077667a1fdda602744092d866df03c3fa|1"
  "1103|KS-1203|refs/heads/feature/ks-1203-a-connector-restricted-by-alloweddocumenttypes-can-still-untyped-1|47593b77b80a295b4113da8acf850b5c8b03fd7e|1"
  "1104|KS-1272|refs/heads/feature/ks-1272-api-gateway-boot-the-platform-db-de-dup-delete-fails-22p02-uuid-dedup-1|${QAB1102_HEAD_1104:-9b668edba63e1328ab113058b47953a11d2a3ed6}|2"
)
DEVELOP_SHA='dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa'   # the pin = develop at 13:06Z / 13:10Z; all three heads merge-base
MERGE_BASE="$DEVELOP_SHA"    # every PR sits on the pin itself — the compare is asserted against it
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1102-1104-tier1-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1100-1101-tier1-r1/'
EARLIER_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-20-batch1097-1099-tier1-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-20_gate1102to1104/mail_batch1102_ready.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The three heads, each pinned at its branch AND at refs/pull/N/head on origin (one ls-remote per PR). One moved head refuses the launch: re-pin that PR.
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

# The compare (GitHub compare API) per PR, asserted whole (merge_base + ahead + files; NOT behind — develop is expected to move):
# develop...head = dc061f2bb ahead 1 for all three PRs; files 1 / 1 / 2 (drafter 13:10Z; the launcher reads the compare API).
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
    print("%s %s ahead=%d files=%d" % (n, c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compares develop...head from the GitHub compare API" >&2; exit 13; }
WANT_COMPARE="1102 $MERGE_BASE ahead=1 files=1
1103 $MERGE_BASE ahead=1 files=1
1104 $MERGE_BASE ahead=1 files=2"
[ "$COMPARE" = "$WANT_COMPARE" ] || { echo "REFUSING: develop...head compares read" >&2; printf '%s\n' "$COMPARE" >&2; echo "the gateset pins" >&2; printf '%s\n' "$WANT_COMPARE" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): paths by PATH BLOB at the CURRENT develop (no region judgement), then — if develop moved —
# the pinned...develop delta against the GUARDED list, with NOTHING cleared by content (DEV_CONTENT_ALLOWED is empty).
CUR_DEV="${QAB1102_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request, urllib.error
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
A = D + "services/api-gateway/"
O = D + "services/originate/"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop (OK for the NEW #1104 test)
JUDGED = {
  O + "src/__tests__/lifecycleEventRepo.test.ts":                          ({"994abf9ffd17a59acdcabedff4b2db8e5e1423fb": DV}, {"c4aad21223cc59bf5b8c70dc9e8fa65a875d92a3": "#1102 own"}),
  A + "src/__tests__/ks501-enforcement-non-string-doctype.test.ts":       ({"4f993ee7aefb3abc857436a07cdd5f2b3fa4f80f": DV}, {"e05c6bd21f64ad766083c72d0fc070ebeb478b7f": "#1103 own"}),
  A + "src/startup-migrations.ts":                                         ({"ed3e521426e75910c5bf2cf07e7251f2fd8ef538": DV}, {"cf371028fb564ca0e55d9d9501c3efa1211b5bd0": "#1104 own"}),
  A + "src/__tests__/ks1272-platform-dedup-uuid-tenant-id.test.ts":       ({"ABSENT": DV}, {"2b91446416f826b69dbd5a0ab6f4123c96d06349": "#1104 own"}),
  A + "src/services/enforcement.ts":                                       ({"be466fbf444178bbb41293fb1d811957e55e1d2d": DV}, {}),
  A + "src/__tests__/enforcement.test.ts":                                 ({"79043184542cf64f9fa32583e5b8eba2e01555a2": DV}, {}),
  O + "src/lifecycleActions.ts":                                           ({"aa1c8434d5a55ad035e1ee62755ace7379af69fb": DV}, {}),
  A + "src/__tests__/db.retry.test.ts":                                    ({"5933da41ed3dcf37f415000c4da4a717ea8d7eba": DV}, {}),
  D + "docker/init-platform/01-platform-schema.sql":                       ({"64fb44c68ea55825c4ad2c2c2f199c8c7746ab87": DV}, {}),
  A + "package.json":                                                      ({"841d8c6adcd71e885c01e65c22da9418daff276a": DV}, {}),
  A + "vitest.config.ts":                                                  ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": DV}, {}),
  A + "vitest.setup.ts":                                                   ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": DV}, {}),
  A + "tsconfig.json":                                                     ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": DV}, {}),
  O + "package.json":                                                      ({"d4435238d3ece7f7da42f043f56ca7739a611132": DV}, {}),
  O + "jest.config.js":                                                    ({"735183662feea56d39f664eb6379cae1a2eec957": DV}, {}),
  O + "tsconfig.json":                                                     ({"d1b46ece71ad5b2559ccad3648c23a5231e43b09": DV}, {}),
  D + "scripts/preflight/preflight.sh":                                    ({"712f895362e2c8d1ead6fd09ac257d7bce212948": DV}, {}),
  D + "scripts/run-shell-suites.sh":                                       ({"bf766bb54828cf6abad817f0f21a0c2f674d783f": DV}, {}),
  ".githooks/pre-push":                                                    ({"1b22d4e146487aa25698310b353152a7d09986b5": DV}, {}),
  D + "package.json":                                                      ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "package-lock.json":                                                 ({"646c19f6f7f735ba32bfb20bef8b936835184949": DV}, {}),
  D + "eslint.config.mjs":                                                 ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
  "BACKLOG.md":                                                            ({"59a1928dc56d9921dbdf2e8d36667e2df6af4024": DV}, {}),
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
    print("OK " + state + " | origin develop still " + pinned + " (the merge-base of all three heads: each merged tree = its head tree, a fast-forward: #1102 66cb0c8234ae557beb5f3e063c12e6c35e9a463f, #1103 ce51bd52adf81539c0900791a669c4052f3ce2f4, #1104 35eab598df96eeb5838414d72d986f2208eacc75; all three together d0c8bfd095b65861efc1a4e8524017235b42e382 in all six orders, PR1+PR2 d2387eabdba1be720e0125f64e92667b9ddfa4ae, drafter scratch-clone merge-tree chains; git ls-remote)"); sys.exit(0)
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
           O + "src/",
           O + "package.json",
           O + "jest.config.js",
           O + "tsconfig.json",
           D + "packages/shared/src/",
           D + "scripts/",
           D + "docker/init-platform/",
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
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto EACH of the three heads in its own clones, names each merged-tree OID (drafter over the pin: each = its head tree; all three d0c8bfd095b) and re-runs each PR items and suites on it"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d, cleared by content %d — the rest disjoint from the GUARDED list (api-gateway + originate src/ + config, packages/shared src/, scripts/, docker/init-platform/, .githooks/, the Dev package.json + lock, eslint.config.mjs, BACKLOG.md); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), len(cleared), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'at the TIER 1 floor' "$PROMPT_FILE" && grep -qF '#1103 KS-1203: TIER 1' "$PROMPT_FILE" && grep -qF '#1102 KS-1275: TIER 2' "$PROMPT_FILE" && grep -qF '#1104 KS-1272: TIER 2' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the TIER 1 floor and each PR own tier line (#1103 T1, #1102 T2, #1104 T2)" >&2; exit 7; }
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
grep -qF '[QA -> Wednesday] BATCH GATE #1102-#1104 (three PRs; tier 1 = #1103 KS-1203)' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" && grep -qF 'THREE lines, one per PR' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact batch verdict subject, coagent@ / wednesday-agent@, and THREE verdict lines one per PR" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" && grep -qF "$EARLIER_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT, the EARLIER REPORT $EARLIER_REPORT and NOT-TESTED.written-first.md" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM line PER PR' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" && grep -qF 'ONE equality target PER PR FILE' "$PROMPT_FILE" && grep -qF '#1104 TWO' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1104 TWO) and the CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO naming each head" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only|signed GO alone" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO naming each head as the merge authority, or carries a Kam-tap / not-alone condition" >&2; exit 26; }
grep -qF 'PREFLIGHT INCOMPLETE' "$PROMPT_FILE" && grep -qF 'PREFLIGHT INCOMPLETE' "$BRIEF" && grep -qF 'login_stub' "$PROMPT_FILE" && grep -qF 'login_stub' "$BRIEF" && grep -qF 'mergeable_state' "$PROMPT_FILE" && grep -qF 'mergeable_state' "$BRIEF" && grep -qiF 'zero product bytes' "$PROMPT_FILE" && grep -qiF 'zero product bytes' "$BRIEF" \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat words: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes" >&2; exit 27; }
grep -qF 'Never enter any seat worktree' "$PROMPT_FILE" && grep -qF '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-20_seatB-10th/' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering any seat worktree and writing in the seat 2026-09-20_seatB-10th history" >&2; exit 28; }
grep -qF 'END EVERY LISTENER YOUR RUNS START, BY PID' "$PROMPT_FILE" && grep -qF 'TCP LISTEN census' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require every listener the gate starts ended by pid with a census (KS-1201)" >&2; exit 29; }
# exit 30: every seat item must sit in BOTH the READY capture and the prompt (one loop, the first miss named)
for _w in 18499832 d0c8bfd095b65861efc1a4e8524017235b42e382 66cb0c8234ae557beb5f3e063c12e6c35e9a463f ce51bd52adf81539c0900791a669c4052f3ce2f4 35eab598df96eeb5838414d72d986f2208eacc75 d2387eabdba1 \
          c4aad21223cc59bf5b8c70dc9e8fa65a875d92a3 e05c6bd21f64ad766083c72d0fc070ebeb478b7f cf371028fb564ca0e55d9d9501c3efa1211b5bd0 2b91446416f826b69dbd5a0ab6f4123c96d06349 \
          cd92897c0ec0 4e71783c696b ee05d9c6c99f bc70ed4eef2f SWAPFIRSTTWO SWAPNOTECERT SPELLINGSHONOURED UNTYPEDGETSADEFAULT \
          3423 1fabaf50e7a7 10708 10743 10764 69709f07956e ':116' ':136' 'enforcement.test.ts:148' '85' '86' ':473' ':1077' \
          'IS NOT DISTINCT FROM' 3f7d6d0be92787e47a48e88da5755e0e8e0251344de0f289e0353ad92b659a88 674 675 677 678 806 807 'recount' 'rc 128' \
          'STOP-class 0' ':5432' '127.0.0.1:1' 'anchoring' '4005' 'db.retry' dc061f2bb6dff9180a0724b1d1d5c50b9a0173fa 1ccb80e0d66ab0ff12d5dbb61753b8c0c274e923 \
          '22P02' 'section_2.decl.diff' 'const summary'; do
  grep -qF -- "$_w" "$PROMPT_FILE" && grep -qF -- "$_w" "$BRIEF" \
    || { echo "REFUSING: the READY capture and the prompt do not BOTH carry the seat item '$_w'" >&2; exit 30; }
done
grep -qF 'MEASURE, not conclude' "$PROMPT_FILE" && grep -qF 'RULE WHETHER IT BLOCKS' "$PROMPT_FILE" \
  || { echo "REFUSING: the prompt does not say MEASURE, not conclude and RULE WHETHER IT BLOCKS on the db.retry intermittent" >&2; exit 30; }
grep -qF 'd0c8bfd095b65861efc1a4e8524017235b42e382' "$PROMPT_FILE" && grep -qF 'NOT-PINNED' "$PROMPT_FILE" && grep -qF 'proposed cell' "$PROMPT_FILE" && grep -qF 'GATEWAY_URL=http://127.0.0.1:' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the batch tree in full, the NOT-PINNED list with a proposed cell per row, or a loopback GATEWAY_URL for preflight" >&2; exit 31; }
grep -qF 'PR #1102 is KS-1275.' "$PROMPT_FILE" && grep -F '#1102' "$BRIEF" | grep -qF 'KS-1275' && grep -qF 'PR #1103 is KS-1203.' "$PROMPT_FILE" && grep -F '#1103' "$BRIEF" | grep -qF 'KS-1203' && grep -qF 'PR #1104 is KS-1272.' "$PROMPT_FILE" && grep -F '#1104' "$BRIEF" | grep -qF 'KS-1272' \
  || { echo "REFUSING: the READY capture and the prompt do not BOTH state which ticket each PR is (#1102 KS-1275, #1103 KS-1203, #1104 KS-1272)" >&2; exit 32; }
for _w in 'round 1 of 2' 'ONE product line on #1104' 'ALL SIX MERGE ORDERS' ':116-not-:136' 'PRE-EXISTING COVERAGE, NOT AS A REGRESSION' \
          'THE 85-LINE HEAD vs THE CHECKER' '5-space twin at startup-migrations.ts:473' 'UUID NOT NULL' 're-run that suite' 'report the ratio' 'RULE WHETHER IT BLOCKS' \
          'a real Postgres listens on 127.0.0.1:5432' 'CENSUS RULE v2' 'the baseline leg REPORTS only' 'attachmentsForURL' 'includeArchived' \
          'SAME ROW FORMAT as the PRIOR REPORT' 'ONE MERGE ADDENDUM line PER PR' 'NOTHING ABOUT O-1' 'must not recommend pinning either' 'GRADE THE HEADS'; do
  grep -qF -- "$_w" "$PROMPT_FILE" \
    || { echo "REFUSING: the prompt does not carry Wednesday by-name item '$_w'" >&2; exit 33; }
done

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  three heads on origin (branch AND refs/pull/N/head):$HEADS_NOTE"
  echo "  compares (GitHub API), develop...head per PR:"
  printf '%s\n' "$COMPARE" | sed 's/^/    /'
  echo "  $DEV_NOTE"
  echo "  READY capture, prompt, QA project and repo all present"
  echo "  prompt carries the TIER 1 floor and each PR tier (#1103 T1, #1102 T2, #1104 T2); names ROUND 1"
  echo "  prompt opens with the thinking directive and names the READY mail capture"
  echo "  READY capture and prompt both name all three heads in full"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact batch verdict subject, coagent@ sender, wednesday-agent@ recipient, THREE verdict lines"
  echo "  prompt names the report directory, the #1100-#1101 batch PRIOR REPORT, the #1097-#1099 EARLIER REPORT and NOT-TESTED.written-first.md"
  echo "  prompt carries a MERGE ADDENDUM line PER PR with ONE equality target PER PR FILE (#1104 TWO) and CLOSED / STILL OPEN / NEW"
  echo "  prompt names WEDNESDAY'S signed GO naming each head; no Kam-tap or not-alone condition"
  echo "  READY capture and prompt BOTH carry: PREFLIGHT INCOMPLETE / login_stub / mergeable_state / zero product bytes"
  echo "  prompt forbids any seat worktree and the seat 2026-09-20_seatB-10th history"
  echo "  prompt requires every listener ended by pid with a TCP LISTEN census (KS-1201)"
  echo "  READY capture and prompt BOTH carry the seat items (trees, blobs, plants, twins, the :148 cover, 85/86, :473/:1077, counts, census); the prompt says MEASURE, not conclude, and RULE WHETHER IT BLOCKS on db.retry"
  echo "  prompt names the batch tree, the NOT-PINNED list with a proposed cell per row and a loopback GATEWAY_URL"
  echo "  READY capture and prompt BOTH state which ticket each of the three PRs is"
  echo "  prompt carries Wednesday by-name items: tier/round/one product line, all six orders, :116-not-:136, the :148 cover as pre-existing, 85-line head, :473 twin, IS NOT DISTINCT FROM + uuid NOT NULL, db.retry serial ratio + ruling, Postgres :5432 isolation, census rule v2 + originate REPORTS, link hygiene, NOT-PINNED, addendum per PR, nothing about O-1, grade the heads"
  [ -n "${QAB1102_CUR_DEV:-}" ] && echo "  (develop read from the QAB1102_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QAB1102_BRIEF:-}${QAB1102_PROMPT:-}${QAB1102_HEAD_1104:-}${QAB1102_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
