#!/bin/bash
# launch_qa_secuura_ks885_886_978.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on
# Secuura PR #978 (KS-885 / KS-886) @ 13b767a7f: packages/shared `ks879-no-raw-control-bytes-repo-wide.test.ts`
# — the E1 control asserts on the six-character escape ITSELF (charCodeAt(3) === 0, length 7) and a new E2 cell
# pins the ks474 transfer fixture's two escape sites read-only (KS-885); the walk is rooted at Blockchain/Dev
# instead of services/ + packages/ (1,284 files / 12,758,153 bytes / 0 raw control bytes at head), with a shared
# offendersUnder(root), F1 named-file pins, an F2 planted-NUL regression and raised floors (KS-886). Test-file only,
# +128 -24; the ks474 fixture does NOT move (blob b8dea87ec at develop AND head). Round 1 on this PR; both tickets
# were F1/F2 of the #856 tier-2 gate.
#
# #978's parent is 0f69129b3 (= the GitHub compare merge-base, exit 10). origin develop MOVED TWICE while this set
# was being built, then a THIRD time during its red-proof — 0f69129b3 -> 506cd3a33 at 16:56:51 AEST 2026-09-13
# (#969's squash, KS-1069: 3 files under services/api-gateway/) -> fa55e58c9 at 17:08:33 (#970's squash, KS-963 r2:
# 2 files under services/auth/) -> 50b729d69 at 17:21:55 (#971's squash, KS-922/941: two .sh files, none walked) —
# each disjoint by name from the ks879 test, the ks474 fixture and the three F1-named files; the first two each
# add ONE walked .ts, so the docblock's census (1,284 / 12,758,153) is stale on arrival by +2 files / +33,208
# bytes on the merged tree (1,286 / 12,791,361); the brief says so. A squash lands every ~12 minutes, so
# the develop pin below is DISJOINTNESS-CHECKED rather than bare: DEVELOP_SHA is the develop the brief's census
# and ratio were written against; if origin develop has moved past it, the GitHub compare of that delta is read
# and the launcher REFUSES (exit 18) only when the delta touches one of the guard's five files or anything under
# packages/shared/ (that changes the brief's expectations — #975, the sibling ks781 test, would), or when the
# delta cannot be judged (unreadable, >250 files); otherwise it proceeds and prints the move, its file count and
# the walked-set delta, which the gate re-states itself (brief items 2 and 7). A refusal means: confirm the new
# delta, re-state the census, re-pin DEVELOP_SHA here AND in the brief's TARGET section and the prompt — a
# different brief, a deliberate edit. If #975 is in the delta, the expected full-package count becomes 790/790.
#
# Adapted from launch_qa_secuura_ks1069_969.sh by gen_launcher_978.py (asserted substitutions, ONE asserted
# insertion — the disjointness-checked develop pin replacing the bare one — residual guard): same guards and exit
# codes, re-pointed at #978.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks885_886_978.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA978_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-978-ks885-886-tier2.md}"
PROMPT_FILE="${QA978_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-978-ks885-886-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-885-ks-886-control-byte-guard-escape-and-roots'
HEAD_SHA="${QA978_HEAD:-13b767a7fcf64cee2403c1b810d698243998fb5b}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='50b729d69c58474624508ed79d05c520dab22cc6'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-978-ks885-886-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

if ! git -C "$REPO" ls-remote origin "$BRANCH" | grep -q "^${HEAD_SHA}[[:space:]]"; then
  echo "REFUSING: $HEAD_SHA is not at $BRANCH on origin — the head moved; the brief is about a different SHA" >&2
  git -C "$REPO" ls-remote origin "$BRANCH" >&2
  exit 6
fi

ACTUAL_MB="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$HEAD_SHA" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}))
print(json.load(r)["merge_base_commit"]["sha"])
PY
)"
[ -n "$ACTUAL_MB" ] || { echo "REFUSING: could not read the merge-base from the GitHub compare API" >&2; exit 13; }
[ "$ACTUAL_MB" = "$MERGE_BASE" ] || { echo "REFUSING: merge-base is now '$ACTUAL_MB', brief says '$MERGE_BASE'" >&2; exit 10; }

# The develop pin, disjointness-checked (see the header). GUARDED = the files whose movement changes this brief.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (the develop the brief's census and ratio were written against; git ls-remote)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, sys, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__); sys.exit(0)
files = c.get("files") or []
if c.get("status") != "ahead" or len(files) > 250:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files))); sys.exit(0)
GUARDED = ["Blockchain/Dev/packages/shared/",
           "Blockchain/Dev/services/transfer/src/__tests__/ks474-delegation-document-id.test.ts",
           "Blockchain/Dev/tests/admin-crud-test-robust.spec.ts",
           "Blockchain/Dev/frontend/verifier/src/App.tsx",
           "Blockchain/Dev/scripts/check-port-crossover.mjs"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
EXTS = (".ts", ".tsx", ".js", ".mjs", ".cjs"); SKIP = {"node_modules", "dist", "build", "coverage", ".turbo"}
def walked(p):
    return p.startswith("Blockchain/Dev/") and p.endswith(EXTS) and not (set(p.split("/")[:-1]) & SKIP)
added = sum(1 for f in files if f["status"] == "added" and walked(f["filename"]))
removed = sum(1 for f in files if f["status"] == "removed" and walked(f["filename"]))
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d walked+%d/-%d" % (c["ahead_by"], len(files), added, removed))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's five files and packages/shared/; the brief's census is stale by the walked-set delta and the gate re-states it (brief items 2 and 7)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, re-state the census, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  exit 0
fi

[ -z "${QA978_BRIEF:-}${QA978_PROMPT:-}${QA978_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
