#!/bin/bash
# launch_qa_secuura_ks1211_1027.sh — cross-project QA agent, ONE TIER 2 ROUND 1 gate over Secuura/Blockchain PR #1027
# (KS-1211, Seat B, PR-3a of the regroup: GHSA-2883-xcg3-v3hh js-yaml HIGH + GHSA-w5vr-8v7q-w6rv baseline-browser-mapping)
# @ d7fc6cc5582b918c0773ec6f25f86407de6f86ab — TWO commits: b51ed77e1 (the change, on efaaa6034) and d7fc6cc55 (a merge of develop
# 19f1e5475 = #1025). TEN files, no manifest: js-yaml 3.15.1 -> 3.15.2 in services/governance, originate, referral, vc-issuer and the
# Blockchain/Dev root lock; baseline-browser-mapping -> 2.11.24 in frontend/admin, issuer, outlook-addin, verifier, services/governance,
# originate, referral and the root lock; the two rows removed from Blockchain/Dev/scripts/audit/audit-baseline.json (34 -> 32).
#
# THE SHAPE, as read 20:05-20:09 AEST 2026-09-17 (git ls-remote + the compare API): head parents b51ed77e1 + 19f1e5475; origin develop
# 19f1e5475. compare develop...head = merge_base 19f1e5475, status ahead, ahead 2, behind 0, files 10. The compare is asserted as
# merge_base + ahead + files (exit 10); `behind` is deliberately NOT asserted, so a develop that moves on does not trip this guard — the
# develop arm judges the move by CONTENT.
#
# The develop pin is judged by CONTENT, not bare: (a) TWENTY-FIVE files by blob at the CURRENT develop — audit-baseline.json (base
# e6f2184d2 / own 017f52bb5), the nine touched locks (base / own blob each; an own blob -> exit 19 LANDED), their nine package.json,
# and scripts/audit/ audit-locks.mjs, audit-gate.mjs, lock-discovery.mjs, baseline-contract.mjs, package.json, package-lock.json — any
# blob nobody pinned -> exit 18; (b) if develop moved past 19f1e5475, the compare pinned...develop REFUSES (exit 18) only when the delta
# touches a GUARDED path — anything under Blockchain/Dev/scripts/audit/, any of the nine touched locks or their package.json — or cannot
# be judged; anything else proceeds and the gate re-derives every count on the merged tree. TEN open Dependabot PRs (#945-#949, #649, 
# #639, #635, #575, #572) touch the root lock, so one of them landing first REFUSES here by design: re-pin deliberately.
# DEV_CONTENT_ALLOWED is empty.
#
# exit 21: the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it in a cockpit
# pane, never inside a Bash tool. `--check` still runs headless (it launches nothing).
#
# Adapted from launch_qa_secuura_ks1211_1021.sh by gen_launcher_1027.py (asserted substitutions + residual guard + output
# controls + bash -n): same guards and exit codes, re-pointed at #1027. Exit codes 2..21 (19 = LANDED).
# Written by the generator because it contains a legitimate directory change.
#
# Usage: launch_qa_secuura_ks1211_1027.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA1027_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1027-ks1211-jsyaml-bbm-tier2.md}"
PROMPT_FILE="${QA1027_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1027-ks1211-jsyaml-bbm-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1211-bump-jsyaml-bbm'
HEAD_SHA="${QA1027_HEAD:-d7fc6cc5582b918c0773ec6f25f86407de6f86ab}"
MERGE_BASE='19f1e54750ce2b65312a687add2db4f5628edb7d'   # the merge-base of the head with develop = the develop the seat merged in (#1025, KS-528)
DEVELOP_SHA='19f1e54750ce2b65312a687add2db4f5628edb7d'   # develop at draft time = the merge-base itself, #1025 squash (ls-remote 20:05:22 and 20:07:07 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1027-ks1211-jsyaml-bbm-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# The head, pinned at its branch on origin (one ls-remote at run time).
LSR="$(git -C "$REPO" ls-remote origin "$BRANCH")"
if ! printf '%s\n' "$LSR" | grep -q "^${HEAD_SHA}[[:space:]]${BRANCH}\$"; then
  echo "REFUSING: #1027 — $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  printf '%s\n' "$LSR" >&2
  exit 6
fi

# The compare (GitHub compare API), asserted whole (merge_base + ahead + files; NOT behind — see the header):
# develop...#1027 = 19f1e5475 ahead 2 files 10 (behind 0 at draft time — deliberately not asserted).
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
[ "$COMPARE" = "$MERGE_BASE ahead=2 files=10" ] || { echo "REFUSING: #1027 develop...head reads '$COMPARE', brief pins '$MERGE_BASE ahead=2 files=10'" >&2; exit 10; }

# The develop pin, judged by CONTENT (see the header): twenty-five files by blob at the CURRENT develop, then — if develop
# moved — the pinned...develop delta against the GUARDED list with the DEV_CONTENT_ALLOWED blobs cleared.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
DEV_JUDGEMENT="$(
  set -a; . "$SECUURA_ENV"; set +a
  DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
api = "https://api.github.com/repos/Secuura/Distributed_Secuura"
def get(p):
    return json.load(urllib.request.urlopen(urllib.request.Request(api + p, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
cur = os.environ["CUR_DEV"]; pinned = os.environ["DEVELOP_SHA"]
D = "Blockchain/Dev/"
# file -> (develop-OK blobs {blob: label}, LANDED blobs {blob: label})
JUDGED = {
  D + "scripts/audit/audit-baseline.json": ({"e6f2184d2dde6de00fb79618de3621659998e307": "base"}, {"017f52bb5a358e8cae1d25a729c8642d3ed45bc5": "#1027 own"}),
  D + "frontend/admin/package-lock.json": ({"e2a3e7b574cd0d828e810d206e18f5f862b08c3b": "base"}, {"3d9acadaf808610c57de3781657c94a598001f32": "#1027 own"}),
  D + "frontend/admin/package.json": ({"a7fd91ccf3a553d7a2d619caf9cfd4de7ea9d7ac": "base"}, {}),
  D + "frontend/issuer/package-lock.json": ({"8ebf271f14e7dd997c974ec95698357922d7f11b": "base"}, {"b0c47af7144f9228450dc5a82225f742db50b662": "#1027 own"}),
  D + "frontend/issuer/package.json": ({"9d229cab1ec88eb5312693d4860b50b66b80383d": "base"}, {}),
  D + "frontend/outlook-addin/package-lock.json": ({"25ddd7127d618373a5da58cf45284532380b5e19": "base"}, {"c71cfe57a3e4a6f2c4c641ac395c10e99be9c8ba": "#1027 own"}),
  D + "frontend/outlook-addin/package.json": ({"482d51f881b68d462f88df48bd4137d4dc6b5265": "base"}, {}),
  D + "frontend/verifier/package-lock.json": ({"39494d91d2ba6aadda5c3b541b2fb1364f65d7c8": "base"}, {"0a13fe2b72adc794ce9bc645a1680fdbbd570d9d": "#1027 own"}),
  D + "frontend/verifier/package.json": ({"76ef5149dbedb8a5179d5ea7145058a4ed74dc2e": "base"}, {}),
  D + "services/governance/package-lock.json": ({"0f173b26a5c2184201b7a0403425095ad7d499d6": "base"}, {"5fae8f62ca58252800146606ea47877ad9a9a3a6": "#1027 own"}),
  D + "services/governance/package.json": ({"e0644b07509ee7dfbd0b8d267e4246dd3a1e2f65": "base"}, {}),
  D + "services/originate/package-lock.json": ({"d91d746efb2b7fcd6d3168838925f40d7282ea32": "base"}, {"040908e22c620b245d7d1c1c0f512409ef94f043": "#1027 own"}),
  D + "services/originate/package.json": ({"749912c592e8630fff348cc60e1bf49677c18ab1": "base"}, {}),
  D + "services/referral/package-lock.json": ({"009788ecca8eb2ee23629409adf4ceaa7426d602": "base"}, {"725d5d2c21f00e574b2f3986383ca398e322b2aa": "#1027 own"}),
  D + "services/referral/package.json": ({"6482d21714eaa92df7a5fc7e8347912eb446c214": "base"}, {}),
  D + "services/vc-issuer/package-lock.json": ({"d0e7d22d683bf2ea415cd00e367f33df5ab16009": "base"}, {"05dff4ebb509fdf2c5605f0e4caa2e16a15bb0b5": "#1027 own"}),
  D + "services/vc-issuer/package.json": ({"98b44b6c9bc95409a834339dda8b14c0f1e51c77": "base"}, {}),
  D + "package-lock.json": ({"99db3e7c2434f65eb64ab0d8db5775e11eefd6bd": "base"}, {"4831bf2074779139926fbfda3f872c404eba177f": "#1027 own"}),
  D + "package.json": ({"769b7adbda124bb200dd9827d2e4fbc5883e6124": "base"}, {}),
  D + "scripts/audit/audit-locks.mjs": ({"aff23b0420ced863884787443a35f28cf727bd09": "base"}, {}),
  D + "scripts/audit/audit-gate.mjs": ({"8e236ee70ce1a4634552596fb86fcffce234f221": "base"}, {}),
  D + "scripts/audit/lock-discovery.mjs": ({"3dd903b527f26c758cc1da84b10cc0a0db3b1d46": "base"}, {}),
  D + "scripts/audit/baseline-contract.mjs": ({"2504d9a28dc017fcaabfc88248bf1c64431eb38a": "base"}, {}),
  D + "scripts/audit/package.json": ({"d5977b6a13638558ef57e8c294809d7ada8be6cd": "base"}, {}),
  D + "scripts/audit/package-lock.json": ({"ffb2b110a2d69c2c9a10e6caf5666c5fa08ec62c": "base"}, {}),
}
state = []
for f, (ok, landed) in JUDGED.items():
    try:
        blob = get("/contents/" + f + "?ref=" + cur)["sha"]
    except Exception as e:
        print("UNJUDGEABLE develop blob unreadable for " + f.split("/")[-1] + ": " + type(e).__name__); sys.exit(0)
    short = f.replace(D, "")
    if blob in landed:
        print("LANDED develop " + short + " blob " + blob[:9] + " = " + landed[blob] + " — #1027 has landed; this brief is stale"); sys.exit(0)
    if blob not in ok:
        print("GUARDED develop " + short + " blob " + blob[:9] + " — a version nobody pinned"); sys.exit(0)
    state.append(f.split("/")[-1] + " " + blob[:9] + " = " + ok[blob])
state = "; ".join(state)
if cur == pinned:
    print("OK " + state + " | origin develop still " + pinned + " (#1025 squash = the merge-base; git ls-remote)"); sys.exit(0)
try:
    c = get("/compare/" + pinned + "..." + cur)
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = [D + "scripts/audit/",
           D + "frontend/admin/package-lock.json",
           D + "frontend/admin/package.json",
           D + "frontend/issuer/package-lock.json",
           D + "frontend/issuer/package.json",
           D + "frontend/outlook-addin/package-lock.json",
           D + "frontend/outlook-addin/package.json",
           D + "frontend/verifier/package-lock.json",
           D + "frontend/verifier/package.json",
           D + "services/governance/package-lock.json",
           D + "services/governance/package.json",
           D + "services/originate/package-lock.json",
           D + "services/originate/package.json",
           D + "services/referral/package-lock.json",
           D + "services/referral/package.json",
           D + "services/vc-issuer/package-lock.json",
           D + "services/vc-issuer/package.json",
           D + "package-lock.json",
           D + "package.json"]
# STYLE NOTE (912r2 launcher, measured): bash scans quote/paren state THROUGH this heredoc because it sits inside a
# command substitution — keep apostrophes and parentheses EVEN (this block uses none of the former), or the outer $( ) breaks.
# CONTENT-JUDGED allowlist: a hit under a GUARDED path clears ONLY if the per-file blob sha in the compare is EXACTLY one
# pinned here. EMPTY for this gate: at draft time 20:08 AEST ten open Dependabot PRs share the root lock with #1027 (PR files API, 20 open PRs),
# so every guarded hit falls through to GUARDED and exit 18 — re-pin deliberately.
DEV_CONTENT_ALLOWED = {
}
hits = sorted({x["filename"] for x in files for g in GUARDED if x["filename"] == g or (g.endswith("/") and x["filename"].startswith(g))})
by_name = {x["filename"]: x for x in files}
cleared = sorted(h for h in hits if h in DEV_CONTENT_ALLOWED and by_name.get(h, {}).get("sha") == DEV_CONTENT_ALLOWED[h])
remaining = sorted(h for h in hits if h not in cleared)
if remaining:
    print("GUARDED " + " ".join(remaining)); sys.exit(0)
tail = "the gate merges the then-current develop onto d7fc6cc55 in its own clone, re-runs the lock parse and both audit gates on the MERGED tree beside the develop and head trees, and names the delta (brief item 5)"
if cleared:
    print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d, cleared BY BLOB under guarded paths: %s — %s" % (pinned, cur, c["ahead_by"], len(files), ",".join(x.split("/")[-1] for x in cleared), tail)); sys.exit(0)
print("OK " + state + " | origin develop MOVED %s -> %s: commits=%d files=%d — disjoint from the GUARDED list (Blockchain/Dev/scripts/audit/, the nine touched package-lock.json and their package.json); %s" % (pinned, cur, c["ahead_by"], len(files), tail)); sys.exit(0)
PYJ
)"
case "$DEV_JUDGEMENT" in
  OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
  LANDED*) echo "REFUSING: ${DEV_JUDGEMENT#LANDED } (develop $CUR_DEV) — re-pin deliberately: a different brief" >&2; exit 19 ;;
  *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA / JUDGED blobs / DEV_CONTENT_ALLOWED + brief TARGET + prompt)" >&2
     exit 18 ;;
esac
grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
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

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head on origin: #1027 $HEAD_SHA at $BRANCH"
  echo "  compare (GitHub API): develop...#1027 = $COMPARE"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA1027_BRIEF:-}${QA1027_PROMPT:-}${QA1027_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
