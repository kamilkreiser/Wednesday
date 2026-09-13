#!/bin/bash
# launch_qa_secuura_ks991_903_r2.sh — cross-project QA agent, TIER 2 (through code: a shell test file for the pre-push hook's
# base resolution — no service, route, spec, schema or UI) DELTA gate, ROUND 2, on Secuura PR #903 (KS-991) @ a4f71cde6 —
# FOUR commits, all on origin develop's M18 8861e6216 by merge: the two reviewed commits d4a596f35 + a70f92d7c (the KS-991 guard in
# .githooks/pre-push and the env_fail arm in preflight.sh; base 986c592d5 then), the merge commit 48553f272 (develop 8861e6216
# merged IN, --no-ff, clean, tree 2e6d92d16 = s213's merge-tree prediction) and the round-2 fix commit a4f71cde6 (parent 48553f272,
# tree 5d4023647, +123 -1, ONE file, ONE hunk @@ -504,11 +504,133 @@: CASE 10 + CASE 11 in
# Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh, blob d95af6514 -> affdf027b, 524 -> 646 lines, sha256
# 48ada0c361efcc3c -> 6dabbb516e92e5cf). PR files API vs develop: 3 files +186 -2 (hook +39 -1, test +123 -1, preflight.sh +24 -0).
#
# Why a round 2: round 1 was PETER's review (PR comment 5585854866, 2026-09-08 13:25Z — "Not approving yet — solely on the missing
# regression case"): the KS-991 change edits the block pre_push_hook_base.test.sh guards and added no case, so the property lived
# only in the PR description. His ONE ask: two committed cases (his "CASE 7/8" against the 6-case file at 986c592d5). s214 delivered
# them as CASE 10 (stale strict-ancestor local develop + docs-only branch -> SKIPS and says KS-991) and CASE 11 (same stale develop +
# a real Blockchain/Dev change -> still RUNS), red-first against develop's hook f0748ed56 (26/2) and the merge base's aae2743ac
# (23/5), green at the head's 1b22d4e14 (28/0) — Wednesday's drafter re-derived all six rows + three gate-designed tampers EXACT
# on git-show copies (gate903r2/guards_sim.out).
#
# Round 2 re-gates: (1) the delta is EXACTLY the fix commit (one file, one hunk) on a CLEAN develop merge — hook + preflight.sh
# blob-identical between 48553f272 and a4f71cde6; the merge vs develop = the reviewed delta (39/1 + 24/0); (2) the RED-FIRST pair
# re-derived in the gate's own clone: develop's hook blob -> 26/2 (CASE 10's two behaviour cells), the head's -> 28/0, the merge
# base's -> 23/5; (3) the tamper table with the suite running (T1 revert / T2 unconditional / T3 token, + Tg-A direction-inverted
# 25/3, Tg-B `!=` dropped 28/0 — the suite is BLIND to that clause, a Record — and Tg-E ancestor:=true 27/1); (4) Peter's five
# notes answered as the ticket comment e1e526bc says; (5) CI at the head ATTRIBUTED, never graded (step 11's two reds are develop's
# own — KS-1138 + KS-1148; step 7's npm-audit red is KS-1075/KS-1077's; the `pr` workflow's Playwright red is develop's own too);
# (6) delivered-vs-commissioned against the s214 brief ITEM 1 (overlaying s213 §2) and Peter's ask; findings-only; NOT-TESTED.
#
# Merge-base = origin develop M18 8861e6216 (develop was merged INTO the branch, so GitHub compare develop...head: ahead 4 /
# behind 0 — exit 10 if it changes). origin develop = M18 8861e6216 (12:00:26Z 2026-09-13; read 07:56 and 08:03 AEST 2026-09-14).
# The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past M18, the GitHub compare of that delta is
# read and the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — the three PR files, deps-present.sh,
# run-shell-suites.sh, or anything under Blockchain/Dev/scripts/__tests__/ (the 29-suite leg-14 count moves) — or cannot be judged
# (unreadable, not ahead, >250 files); otherwise it proceeds printing the move and its file count, which the gate re-states (brief
# items 1 and 6). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA here AND in the brief's TARGET section AND the
# prompt — a different brief, a deliberate edit. #918 and #925 both touch preflight.sh: either merging first fires exit 18.
#
# NEW in this launcher (exit 21): the LAUNCH path refuses when stdin is not a TTY. This launcher execs an interactive agent; run it
# in a cockpit pane, never inside a Bash tool — a gate launched there runs headless, invisible to Kam, and dies with the caller's
# shell (2026-09-13 ledger). `--check` still runs headless (it launches nothing).
#
# Adapted from the #980 round-2 launcher by gen_launcher_903r2.py (asserted substitutions, residual guard): the same guard family
# and exit codes 2..21 (exit 19 = the round-1 record named AND on disk — here Peter's saved review, not a QA report; exit 20 = the
# full head SHA in both brief and prompt; exit 21 = stdin not a TTY on the launch path).
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks991_903_r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA903R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md}"
PROMPT_FILE="${QA903R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/kamilkreiser/ks-991-stale-local-develop'
HEAD_SHA="${QA903R2_HEAD:-a4f71cde660c1442d98317e26d93845340b20098}"
MERGE_BASE='8861e62161466c40f08d2b10a30edeb203123993'
DEVELOP_SHA='8861e62161466c40f08d2b10a30edeb203123993'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md"

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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M18, the develop merged INTO the branch and the one this brief's 28/0 was written against; git ls-remote)"
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
GUARDED = [".githooks/pre-push",
           "Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh",
           "Blockchain/Dev/scripts/preflight/preflight.sh",
           "Blockchain/Dev/scripts/preflight/deps-present.sh",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           "Blockchain/Dev/scripts/__tests__/"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's six paths (#903's three files, deps-present.sh, run-shell-suites.sh, the scripts/__tests__/ prefix); the gate merges the then-current develop, re-states the delta by name and re-derives the leg-14 count (brief items 1 and 6)" ;;
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

R1_REPORT='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 record path (Peter's review; a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 record named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }

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
  echo "  brief names the round-1 record (Peter's review) and it is present on disk"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool (a headless gate is invisible and dies with the caller's shell)" >&2; exit 21; }
[ -z "${QA903R2_BRIEF:-}${QA903R2_PROMPT:-}${QA903R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
