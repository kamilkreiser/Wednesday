#!/bin/bash
# launch_qa_secuura_ks924_901_980_r2.sh — cross-project QA agent, TIER 2 (through code: a structural guard's own
# suite in packages/shared; no running system, no rendered surface) DELTA gate, ROUND 2, on Secuura PR #980
# (KS-924 / KS-901) @ 103c235b4 — TWO commits on origin develop's M9 50b729d69: the r1 head 9c620f890 (gated GO
# WITH FINDINGS 2026-09-13 19:58 AEST onto M11 a2257e502, 794/794; 1 Polish GF-1; Records R-1..R-4, R-3 -> KS-1142)
# and the r2 commit 103c235b4 (parent 9c620f890, tree 068aa3d0f, +1 -1, ONE file, ONE line: entrypoint-corpus.test.ts
# :235 — the P3 census plant's STRING `app.listen(0);` -> `app.listen(0, '127.0.0.1');`, +13 chars, 443 lines, blob
# e232b0289 -> d81265b7f, sha256 86b7f7b23b2ac591... -> 020634da9cec74ec...). PR files API: 1 file +130 -14 vs M9.
#
# Why a round 2: the merge seat s209 HELD 9c620f890 — on the MERGED tree the ks860 test-listener loopback guard
# (ks860-test-listeners-bind-loopback.test.ts, widened by #976 = M13 3370ef661 to walk packages/ too; its comment mask
# preserves string contents by design) read that plant string as a host-less listener: packages/shared 805/806 on
# M14, 812/813 on M15, the file green alone (the guard at #980's own tree is still the pre-#976 blob d8842e577).
# No gate could see it: round 1 gated onto M11, M13 came after. Wednesday ruled shape A (the guard's own accepted
# spelling, its :517 control); s210 pushed it as a fast-forward; the delta gate re-reads it.
#
# Round 2 re-gates: (1) the delta is EXACTLY the one line, by blob and by diff; (2) on the MERGED tree (3-way onto
# the live develop) the full packages/shared green with the loopback guard's red cell GREEN (813/813 on M15 — the
# number moves with develop, the gate states its instrument) and RED-FIRST with round 1's bytes swapped in (the red
# cell names :235); (3) the P3 census still names the plant (KS-901's absence tamper T-P3 still reds P1 P2 P3, T6
# reds P3; cells-run quoted); (4) round 1's findings unchanged (GF-1 rides the next touch; R-3 -> KS-1142 exists);
# (5) delivered-vs-commissioned against the s210 brief + Wednesday's ANSWER (shape A; Q1 the M15 export; Q-GF1 NOT
# taken); (6) findings-only; board search by symbol before filing (Wednesday's); a NOT-TESTED list.
#
# Merge-base = the PR's parent M9 50b729d69 (GitHub compare develop...head: diverged, ahead 2 / behind 6, 1 file —
# exit 10 if it changes). origin develop = M15 1c38077ba (#981's squash "KS-828 KS-900 ...", 10:20:41Z; read 20:53
# AEST 2026-09-13); M9..M15 = 6 squashes / 16 files: under packages/shared/ exactly THREE modified tests (ks781,
# ks860 — the loopback guard, ks879), NOT #980's file (blob 472c07dbe at M9 AND M15) and NOT the module (a7abd31ef
# everywhere); the walk the corpus reads (services/ + connectors/) is 380 files / 27 packages / census [] at M15
# (bytes 4,764,340). The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M15,
# the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the delta touches a GUARDED
# path — #980's file, the ks860 guard file, or anything under Blockchain/Dev/packages/shared/ (the 813 ratio moves)
# — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file
# count, which the gate re-states (brief items 1 and 2). A refusal means: confirm the new delta, then re-pin
# DEVELOP_SHA here AND in the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #977 round-2 launcher by gen_launcher_980r2.py (asserted substitutions, residual guard): same
# guards and exit codes 2..20, re-pointed at #980 round 2 (exit 19 = the round-1 report named AND on disk; exit 20 =
# the full head SHA in both brief and prompt).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks924_901_980_r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..20 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA980R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.md}"
PROMPT_FILE="${QA980R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-924-ks-901-entrypoint-corpus-presence-set-and-three-shapes'
HEAD_SHA="${QA980R2_HEAD:-103c235b4d2be54cc1ade65ed660f397cf03e997}"
MERGE_BASE='50b729d69c58474624508ed79d05c520dab22cc6'
DEVELOP_SHA='1c38077ba2aea5f4c4371c1b68796026dc577764'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-980-ks924-901-tier2-r2.md"

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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M15, the develop this brief's 813/813 was written against; git ls-remote)"
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
GUARDED = ["Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",
           "Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",
           "Blockchain/Dev/packages/shared/"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's three paths (#980's file, the ks860 loopback guard file, the packages/shared/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the ratio (brief items 1 and 2)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
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

R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks924-901-980-9c620f890-tier2-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 2"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name the head SHA $HEAD_SHA"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief names the round-1 report and it is present on disk"
  exit 0
fi

[ -z "${QA980R2_BRIEF:-}${QA980R2_PROMPT:-}${QA980R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
