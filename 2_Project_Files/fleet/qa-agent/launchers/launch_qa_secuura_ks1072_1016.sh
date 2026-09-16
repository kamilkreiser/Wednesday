#!/bin/bash
# launch_qa_secuura_ks1072_1016.sh — cross-project QA agent, ONE TIER 1 ROUND 1 gate over Secuura/Blockchain PR #1016
# (KS-1072, Seat A) @ a226d94fe8c6fbfecb81de415feb645302cdd166 — ONE commit on 523f283c6 (#1011 squash), 2 files, both services/api-gateway:
# src/routes/verification.ts +7 -2 (makeFetchDocFromAnchorStore: equal blockNumbers break on the most recent confirmedAt)
# and the NEW src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts (+177, 5 cells).
# TIER 1: the selected anchor sets a TIER-2 VERIFY VERDICT on the public verification path (POST /api/documents/:id/verify).
#
# THE SHAPE, as read 06:42-06:58 AEST 2026-09-17 (git ls-remote + the compare API agree): the PR parent = merge-base = develop 523f283c6,
# so compare develop...head = merge_base 523f283c6, ahead 1, behind 0, files 2, and the merged tree IS the head tree until develop moves.
# The compare is asserted as merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted — the develop arm judges every move
# by CONTENT (#1014 and #1015 are gating and may land during the run).
#
# The develop pin is judged by CONTENT, not bare: (a) TWELVE files by blob at the CURRENT develop — verification.ts (base 04b3d980f;
# the PR own a7a6d4605 -> exit 19 LANDED), the ks1072 test (ABSENT at base; the PR own 4ad1cdcd1 -> exit 19 LANDED), api-gateway src/index.ts
# (the mounts + the v1 rewrite), services/enforcement.ts (533cd309c base OR 3e314ba11 = #1014 own — both clear), api-gateway package.json /
# vitest.config.ts / vitest.setup.ts / tsconfig.json, anchoring src/index.ts (the anchor-list producer), Dev eslint.config.mjs, the Dev lockfile
# and docs/openapi/secuura-api.yaml — any blob nobody pinned -> exit 18;
# (b) if develop moved past 523f283c6, the compare pinned...develop REFUSES (exit 18) when the delta touches a GUARDED path —
# services/api-gateway/src/ and its config files, services/anchoring/src/, packages/shared/src/, migrations/, docker/init/, docs/openapi/,
# eslint.config.mjs, the Dev lockfile — unless the file blob is EXACTLY #1014 own (enforcement.ts 3e314ba11, ks1176 test 5820520ae), or cannot
# be judged. #1015 (services/auth) is outside the GUARDED list. #995 touches anchoring src/index.ts: if it lands, re-pin deliberately.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool — and never run it without --check to "prove" this guard. `--check` runs headless (it launches nothing).
# exit 22: the prompt must require node_modules farmed PER ENTRY (the #1009 gate R-6: a wholesale link can write through to the checkout .vite).
# exit 23: the prompt must carry the exact verdict subject and name coagent@ as the sender and wednesday-agent@ as the recipient.
# QA1016_CUR_DEV (test override, --check only): stands in for origin develop so the LANDED / GUARDED refusals can be proven.
# A launch with any QA1016_* override set refuses (exit 16).
#
# Hand-derived by the #1016 drafter from launch_qa_secuura_ks1176_1014.sh by one inline asserting Python edit (header, pins, JUDGED / GUARDED /
# DEV_CONTENT_ALLOWED blocks replaced whole; other lines substituted with asserted counts; a residual guard for 1014 / 1176 / 616c766a5 /
# e0f41a8fa / 8589933267 outside named #1014 mentions): same guards and exit codes, re-pointed at #1016. Exit codes 2..23 (19 = LANDED).
#
# Usage: launch_qa_secuura_ks1072_1016.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..23 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1016_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1.md}"
PROMPT_FILE="${QA1016_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1072-ornith-latest-anchor-confirmedat-tiebreak'
HEAD_SHA="${QA1016_HEAD:-a226d94fe8c6fbfecb81de415feb645302cdd166}"
MERGE_BASE='523f283c6cd2550263ec9869dc5ee722be40df4e'   # the merge-base of the head with develop = the PR parent 523f283c6 (#1011's squash)
DEVELOP_SHA='523f283c6cd2550263ec9869dc5ee722be40df4e'   # develop at draft time = the PR parent itself, an ANCESTOR of the head (git ls-remote 06:42:47 and 06:55:00, branches API 06:52 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1016 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1016 = 523f283c6 ahead 1 files 2 (behind 0 at draft time; behind deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=1 files=2" ] || { echo "REFUSING: #1016 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=1 files=2'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twelve files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="${QA1016_CUR_DEV:-$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)}"
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
G = D + "services/api-gateway/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label}); ABSENT = the contents API answers 404 at develop
JUDGED = {
  G + "src/routes/verification.ts":                                    ({"04b3d980f657b13717060e9547d92970100b2557": "base"}, {"a7a6d46057a18b3460e7d08bbec5df12ab763a81": "#1016 own"}),
  G + "src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts": ({"ABSENT": "base"}, {"4ad1cdcd1e45044efdbb0b8e4e6eaf358453d780": "#1016 own"}),
  G + "src/index.ts":                                                  ({"6f38c819e48162e3179aaf557085766f91beecc1": "base"}, {}),
  G + "src/services/enforcement.ts":                                   ({"533cd309c56b8167ebe00b620744259b3cc186cc": "base", "3e314ba116f85df0a8a37549272f8078c4c95ccd": "#1014 squash"}, {}),
  G + "package.json":                                                  ({"841d8c6adcd71e885c01e65c22da9418daff276a": "base"}, {}),
  G + "vitest.config.ts":                                              ({"5888e0b320d934f6f434e0e5ca3c74a995cecc02": "base"}, {}),
  G + "vitest.setup.ts":                                               ({"22c1107683b8192df3bfd3e929aa94aff3dc7d45": "base"}, {}),
  G + "tsconfig.json":                                                 ({"c981e6a92fdd2417fa35070eb979c5f1c77ffbcd": "base"}, {}),
  D + "services/anchoring/src/index.ts":                               ({"da4abd43292186da45c1533017fe042fa512bd43": "base"}, {}),
  D + "eslint.config.mjs":                                             ({"8c5374c6022eb0a3f449f41a570db61294aa63f1": "base"}, {}),
  D + "package-lock.json":                                             ({"17d2061b397595677ae789683b0ca1d4b8398bec": "base"}, {}),
  D + "docs/openapi/secuura-api.yaml":                                 ({"122d3a2f84cf77bf2b7e2dc51489a0d5f823db1f": "base"}, {}),
}
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
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1016 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (= the PR parent, an ANCESTOR of the head: the merged tree IS the head tree eecd5f08729f6b6199a8fb86e86c9a28639bef58; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [G + "src/",
           G + "package.json",
           G + "vitest.config.ts",
           G + "vitest.setup.ts",
           G + "tsconfig.json",
           D + "services/anchoring/src/",
           D + "packages/shared/src/",
           D + "migrations/",
           D + "docker/init/",
           D + "docs/openapi/",
           D + "eslint.config.mjs",
           D + "package-lock.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. For this gate: #1014 own two blobs (KS-1176, gating at draft time) — enforcement.ts is injected into the verify router as
# meetsVerificationLevel, which every verify cell mocks, and the ks1176 test only moves the api-gateway denominator (+1 file / +13 cells).
# Any OTHER blob of those files, and every other guarded hit, falls through to exit 18.
DEV_CONTENT_ALLOWED = {
  G + "src/services/enforcement.ts": "3e314ba116f85df0a8a37549272f8078c4c95ccd",
  G + "src/__tests__/ks1176-connector-key-level-ranks-as-none.test.ts": "5820520ae769aa5d118de2c1c5db4d1204d762e6",
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto a226d94fe in its own clone, rebuilds the shared dist there, runs the api-gateway suite and the verdict-flip rows on the MERGED tree beside the base and head trees, names the merged-tree OID and re-derives every count, above all the api-gateway denominator (brief items 1, 8, 9)"
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (services/api-gateway/src/ + its config files, services/anchoring/src/, packages/shared/src/, migrations/, docker/init/, docs/openapi/, eslint.config.mjs, the Dev lockfile) or cleared at #1014 own blobs; %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round (ROUND 1)" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qF "$HEAD_SHA" "$PROMPT_FILE" && grep -qF "$HEAD_SHA" "$BRIEF" \
  || { echo "REFUSING: brief or prompt does not name the head SHA $HEAD_SHA — a gate about another SHA is another gate" >&2; exit 20; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }
grep -qi 'node_modules per ENTRY' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not require node_modules farmed per ENTRY (a wholesale link can write through to the checkout .vite cache)" >&2; exit 22; }
grep -qF '[QA -> Wednesday] TIER 1 GATE #1016 (KS-1072) a226d94fe' "$PROMPT_FILE" && grep -qF 'coagent@agentmail.to' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not carry the exact verdict subject, the coagent@ sender and the wednesday-agent@ recipient" >&2; exit 23; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1016 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1016 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  prompt requires node_modules farmed per ENTRY"
  echo "  prompt carries the exact verdict subject, coagent@ sender, wednesday-agent@ recipient"
  [ -n "${QA1016_CUR_DEV:-}" ] && echo "  (develop read from the QA1016_CUR_DEV test override, not ls-remote)"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1016_BRIEF:-}${QA1016_PROMPT:-}${QA1016_HEAD:-}${QA1016_CUR_DEV:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
