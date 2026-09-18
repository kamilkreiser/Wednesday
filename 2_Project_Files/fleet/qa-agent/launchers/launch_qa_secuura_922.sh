#!/bin/bash
# launch_qa_secuura_922.sh — cross-project QA agent, ONE TIER 2 (through code) ROUND 1 gate over Secuura/Blockchain PR #922 (KS-679, Seat A)
# @ 8664826e53cc47d4dd69c784926c9c14af444cec — the published example Anchor.id becomes the shape anchoring actually mints (anchor_<uuid>, was anc_…, which
# E8 CERTIFIED because it sat in the fixture set), and the spec-example secret detector E7 is WIDENED: BENIGN_SHAPES gains /^[a-z]+_<exact uuid>$/i.
# Five files, four commits: 2b5075e9f (the change) -> a7d9e2943 (develop 852e1fff7 in) -> e60a24c50 (the seven-case E7 control) -> 8664826e5 (develop
# f6669623c in, this morning). Head tree 92224cca7. anchoring.openapi.ts is +3 COMMENT lines.
# TIER 2, drafter-ruled: no route, schema, status code, handler or mint path moves; the risk is a guard being loosened, measured through code. A GO is a
# gate verdict: #922 merges on WEDNESDAY'S signed GO naming the head (the TESTED grant) and on nothing else (exit 26 guards it).
#
# THE SHAPE, re-read live 10:37:46-10:45:15 AEST 2026-09-18 (git ls-remote + the GitHub PR and compare APIs agree): the head is 8664826e5 on origin, as
# relayed. #922 is ALREADY ONE DEVELOP-MOVE BEHIND: develop a105cd32b = #1034 (KS-1215), three files, all services/api-gateway. compare develop...head =
# merge_base f6669623c, status diverged, ahead 4, files 5, behind 1 (ahead and files asserted, exit 10; behind NOT asserted). MEASURED: 0 shared files,
# and the read-only merge-tree of 8664826e5 against a105cd32b is CLEAN — merged tree 5c56e26fee8cffc3497eae5cc6433a81914d3931, 0 conflicted paths.
# The seat's survival control is RE-DERIVED by the generator: e60a24c50..8664826e5 = develop 852e1fff7..f6669623c by name (234 = 234) AND by patch-id,
# and KS-679's own delta is patch-id-equal before and after the merge.
# THE LOCAL BRANCH REF IS STALE (refs/heads/kamilkreiser/ks-679-anchor-id-format-false = 2b5075e9f in the checkout): the head is pinned from ORIGIN only.
#
# The develop pin is judged by CONTENT — PATH BLOBS — never by develop's SHA: (a) EIGHTEEN files by blob at the CURRENT develop: the PR five
# (secuura-api.yaml 122d3a2f8, the ks256 test adbe91dfb, fixtures.ts ca5d5eae1, contract.mjs 43a9c5dea, anchoring.openapi.ts 49b8b38da; at a #922 blob ->
# exit 19 LANDED) and what the gate runs: the spec-example guard (check-spec-examples.mjs, rules-example / rules-global / allowlist / collect .mjs, the
# allowlist json), scripts/generate-openapi.ts, packages/shared package.json / vitest.config.ts / tsconfig.json, anchoring index.ts (the mint sites),
# the Dev package.json (check:openapi) and eslint.config.mjs — any blob nobody pinned -> exit 18; (b) if develop moves past a105cd32b, the compare
# pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path — packages/shared/src/ and its package.json / vitest.config.ts /
# tsconfig.json, scripts/spec-examples/, scripts/generate-openapi.ts, docs/openapi/, services/anchoring/src/, the Dev package.json, eslint.config.mjs.
# NOTE: #1036 (KS-763, READY, ungated) rewrites packages/shared/package.json — if it lands first this REFUSES by design: re-pin deliberately.
# Lockfiles are not guarded: the gate names the vitest version it ran. DEV_CONTENT_ALLOWED is EMPTY.
#
# NO SEAT READY MAIL at this head. BRIEF = gatesets/2026-09-18_gate922/pr922_snapshot.md, the PR body + comments captured verbatim from the GitHub API
# (00:45:15Z). Its Test Evidence and PREFLIGHT line are from the 2026-09-14 push at e60a24c50, not this head — the prompt says so.
#
# exit 7:  the prompt must name TIER 2 and must NOT carry a 'TIER 1 ROUND' / 'TIER 1 GATE' line (the seat stated no tier; the drafter ruled it).
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact #922 verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# exit 24: the prompt must name the REPORT DIRECTORY, the PRIOR REPORT (#1027, the tier 2 method bar) and NOT-TESTED.written-first.md.
# exit 25: the prompt must carry the MERGE ADDENDUM and require the per-finding CLOSED / STILL OPEN / NEW disposition.
# exit 26: the prompt must name WEDNESDAY'S signed GO as #922's merge authority and carry no copied Kam's-tap merge condition.
# exit 27: the PR snapshot AND the prompt must BOTH carry the seat's own words for what must not pass as green: '12/15 legs ran, 3 SKIPPED' (the
#          incomplete preflight), 'Closes KS-679' (a closing phrase) and 'External consumers' (unmeasured).
# exit 28: the prompt must forbid entering BOTH worktrees that hold this branch: 5_Project_History/quarantine/2026-09-15-s233/worktree-ks679 and
#          worktrees/s-a9-ks679 (seat A's, detached at the head).
# QA922_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# QA922_CONTRACT_FILE (test fixture, --check only): a local file stands in for develop scripts/spec-examples/check/contract.mjs (its git blob).
# A launch with any QA922_* override or fixture set refuses (exit 16).
#
# Generated by gatesets/2026-09-18_gate922/gen_launcher_922.py from launch_qa_secuura_ks1101_1037.sh (asserted block substitutions + pins re-read from the
# repo + a re-derived merged tree + a re-derived survival control + residual guard + output controls + bash -n).
#
# Usage: launch_qa_secuura_922.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..28 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA922_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate922/pr922_snapshot.md}"
PROMPT_FILE="${QA922_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-18_secuura-922-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/kamilkreiser/ks-679-anchor-id-format-false'   # read on ORIGIN only: the checkout's local ref of this name is stale at 2b5075e9f
HEAD_SHA="${QA922_HEAD:-8664826e53cc47d4dd69c784926c9c14af444cec}"
MERGE_BASE='f6669623ccae5ab445be6e0e73fb4f19ae2c89d1'   # the merge-base of the head with develop = the head second parent (develop when the seat merged it in, NOT develop now)
DEVELOP_SHA='a105cd32b1ed9c6927ae6e797f8259224d8480c6'   # the pin = develop RE-READ at drafting, after #1034 landed (NOT the merge-base f6669623c; moves judged by PATH BLOB and GUARDED paths: git ls-remote 10:37:46 AEST 2026-09-18)
REPORT_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks679-922-8664826e5-tier2-r1/'
PRIOR_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1211-1027-d7fc6cc55-tier2-r1/'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/gatesets/2026-09-18_gate922/pr922_snapshot.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #922 — $HEAD_SHA is not at $BRANCH on origin — the head moved; a verdict is valid ONLY at its head" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#922 = f6669623c ahead 4 files 5 (behind 1: develop moved to a105cd32b after the seat merged; behind deliberately NOT asserted). Compare API 00:37:52Z 2026-09-18.
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/"
r = urllib.request.urlopen(urllib.request.Request(api + "develop..." + os.environ["HEAD_SHA"], headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...head from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$MERGE_BASE ahead=4 files=5" ] || { echo "REFUSING: #922 develop...head reads '$COMPARE', the gateset pins '$MERGE_BASE ahead=4 files=5'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): eighteen files by PATH BLOB at the CURRENT develop (no region judgement), then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA922_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
A = D + "packages/shared/"
X = D + "scripts/spec-examples/"
CONTRACT = X + "check/contract.mjs"
DV = "develop"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  D + "docs/openapi/secuura-api.yaml":                               ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": DV}, {"16ac8aa78463849864fa6285e20c9946c027fb7b": "#922 own"}),
  A + "src/__tests__/ks256-spec-example-contract.test.ts":           ({"adbe91dfb0f10752057cceec647b727edb186621": DV}, {"72533d3b01a4941578b1f777f0def3f9ec9ea6f0": "#922 own"}),
  A + "src/openapi/examples/fixtures.ts":                            ({"ca5d5eae163f492c6703e0017610ea7ece7b9583": DV}, {"b54d26929c564d9cd4e2e2f27da12df6d6d85325": "#922 own"}),
  CONTRACT:                                                          ({"43a9c5dea27fc67bf0efc96489a1889833e2cbfd": DV}, {"db726db299f738e2bf6790b3612d917b4d1eb9fc": "#922 own"}),
  D + "services/anchoring/src/anchoring.openapi.ts":                 ({"49b8b38da7764e071711ded751fa006ae21e808d": DV}, {"29c089bb0abcd65d42fe8fca2d6beaff0368fa98": "#922 own"}),
  X + "check-spec-examples.mjs":                                     ({"e9c14a4dedf103850dc1c93fb1c5c67b8489b2a3": DV}, {}),
  X + "check/rules-example.mjs":                                     ({"5d1e7ecaef021de85a12121af94871d86547dfcf": DV}, {}),
  X + "check/rules-global.mjs":                                      ({"f1b447b6d913b8700a47a2a1fff86e5fa18195e1": DV}, {}),
  X + "check/allowlist.mjs":                                         ({"a712f3c61d7ce570c709002ca0e217c8078af8c3": DV}, {}),
  X + "check/collect.mjs":                                           ({"a2da5a4dab146a70818a244033a4032fbd6ec3a6": DV}, {}),
  X + "spec-example-allowlist.json":                                 ({"32bacbc4aa2c8764cc387c4d86919c2f1b08c223": DV}, {}),
  D + "scripts/generate-openapi.ts":                                 ({"e84acdc9e1be073751fcd6a8bb95504e23688019": DV}, {}),
  A + "package.json":                                                ({"3957692311221fbe87c4ab19447de8cec44aa19a": DV}, {}),
  A + "vitest.config.ts":                                            ({"2a226c0068faa65538cda8d43d03bb9bee2944f1": DV}, {}),
  A + "tsconfig.json":                                               ({"1fd016cc28803cc8f36cc84db4628941a2af9c50": DV}, {}),
  D + "services/anchoring/src/index.ts":                             ({"da4abd43292186da45c1533017fe042fa512bd43": DV}, {}),
  D + "package.json":                                                ({"773443a9faa0a2eb7caf01c313b880fbe3251922": DV}, {}),
  D + "eslint.config.mjs":                                           ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": DV}, {}),
}
# No REGION judgement: every file is judged by exact blob (a develop move of any judged file refuses, exit 18; a #922 blob, exit 19).
content_cleared = set()
state = []
for f, (ok, landed) in JUDGED.items():
    fixture = os.environ.get("QA922_CONTRACT_FILE", "") if f == CONTRACT else ""
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #922 has landed; this gateset is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (#1034 KS-1215, services/api-gateway only, 0 #922 files, NOT an ancestor of the head: merged tree 8664826e5 x a105cd32b = 5c56e26fee8cffc3497eae5cc6433a81914d3931, 0 conflicts, drafter merge-tree 00:38:43Z; git ls-remote)"); sys.exit(0)
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
           X,
           D + "scripts/generate-openapi.ts",
           D + "docs/openapi/",
           D + "services/anchoring/src/",
           D + "package.json",
           D + "eslint.config.mjs"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: EMPTY. No lockfile is guarded: the gate names the vitest version it ran against develops lock. Re-pin deliberately.
# A pending PR that rewrites packages/shared/package.json would refuse here if it lands first. That is by design: re-pin deliberately.
DEV_CONTENT_ALLOWED = {}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if (h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") in DEV_CONTENT_ALLOWED[h]) or h in content_cleared)
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto 8664826e5 in its own clone, asserts the merged packages/shared/src, scripts/spec-examples, docs/openapi and services/anchoring/src subtrees equal the head, or re-runs the E7 census, the guard verdict diff, the tamper table and the suites on the MERGED tree; names the merged-tree OID, drafter a105cd32b -> 5c56e26fe (prompt L0 and items 1-3, 5, 6)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — GUARDED hits %d — disjoint from the GUARDED list (packages/shared/src/ + its package.json / vitest.config.ts / tsconfig.json, scripts/spec-examples/, scripts/generate-openapi.ts, docs/openapi/, services/anchoring/src/, the Dev package.json, eslint.config.mjs); %s" % (pinned, cur, c["ahead_by"], len(files), len(hits), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 2' "$PROMPT_FILE" && ! grep -qE 'TIER 1 (ROUND|GATE)' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name TIER 2, or still carries a TIER 1 ROUND / GATE line — the drafter ruled tier 2; the seat stated none" >&2; exit 7; }
grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: prompt does not name ROUND 1 — this gate has no seat READY mail; its source is the PR snapshot, which carries no round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the PR snapshot path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: the PR snapshot or the prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA -> Wednesday] TIER 2 GATE #922 (KS-679) 8664826e5' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact #922 verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }
grep -qF "$REPORT_DIR" "$PROMPT_FILE" && grep -qF 'NOT-TESTED.written-first.md' "$PROMPT_FILE" && grep -qF "$PRIOR_REPORT" "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not name the report directory $REPORT_DIR, the PRIOR REPORT $PRIOR_REPORT (#1027, the tier 2 method bar) and NOT-TESTED.written-first.md — the QA agent has no inbox" >&2; exit 24; }
grep -qF 'MERGE ADDENDUM' "$PROMPT_FILE" && grep -qF 'CLOSED / STILL OPEN / NEW' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the MERGE ADDENDUM and the per-finding CLOSED / STILL OPEN / NEW disposition" >&2; exit 25; }
grep -qiF "WEDNESDAY'S signed GO" "$PROMPT_FILE" && ! grep -qiE "waits for Kam.s tap|on Kam.s tap only" "$PROMPT_FILE" "$BRIEF" \
  || { echo "REFUSING: prompt does not name WEDNESDAY'S signed GO as the #922 merge authority, or a copied Kam's-tap merge condition survives" >&2; exit 26; }
grep -qF '12/15 legs ran, 3 SKIPPED' "$PROMPT_FILE" && grep -qF 'Closes KS-679' "$PROMPT_FILE" && grep -qiF 'External consumers' "$PROMPT_FILE" \
  && grep -qF '12/15 legs ran, 3 SKIPPED' "$BRIEF" && grep -qF 'Closes KS-679' "$BRIEF" && grep -qiF 'External consumers' "$BRIEF" \
  || { echo "REFUSING: the PR snapshot and the prompt do not BOTH carry the seat's own words for the incomplete preflight (12/15 legs ran, 3 SKIPPED), the closing phrase (Closes KS-679) and the unmeasured External consumers — the gate must not let them pass as green" >&2; exit 27; }
grep -qF 'quarantine/2026-09-15-s233/worktree-ks679' "$PROMPT_FILE" && grep -qF 'worktrees/s-a9-ks679' "$PROMPT_FILE" && grep -qi 'DO NOT ENTER EITHER WORKTREE' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid entering BOTH worktrees that hold this branch (quarantine/2026-09-15-s233/worktree-ks679 and worktrees/s-a9-ks679)" >&2; exit 28; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #922 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#922 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  PR snapshot, prompt, QA project and repo all present"
  echo "  prompt names TIER 2 and carries no TIER 1 ROUND / GATE line; prompt names ROUND 1"
  echo "  prompt opens with the thinking directive and names the PR snapshot"
  echo "  PR snapshot and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact #922 verdict subject, coagent@ sender, wednesday-agent@ recipient"
  echo "  prompt names the report directory, the #1027 PRIOR REPORT (tier 2 method bar) and NOT-TESTED.written-first.md"
  echo "  prompt carries the MERGE ADDENDUM and requires CLOSED / STILL OPEN / NEW per finding"
  echo "  prompt names WEDNESDAY'S signed GO as the merge authority; no copied Kam's-tap merge condition survives"
  echo "  PR snapshot and prompt BOTH carry: 12/15 legs ran, 3 SKIPPED / Closes KS-679 / External consumers"
  echo "  prompt forbids entering both worktrees (the quarantined worktree-ks679 and seat A's s-a9-ks679)"
  [ -n "${QA922_CUR_DEV:-}" ] && echo "  (develop read from the QA922_CUR_DEV test override, not ls-remote)"
  [ -n "${QA922_CONTRACT_FILE:-}" ] && echo "  (develop scripts/spec-examples/check/contract.mjs read from the QA922_CONTRACT_FILE fixture, not the contents API)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA922_BRIEF:-}${QA922_PROMPT:-}${QA922_HEAD:-}${QA922_CUR_DEV:-}${QA922_CONTRACT_FILE:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
