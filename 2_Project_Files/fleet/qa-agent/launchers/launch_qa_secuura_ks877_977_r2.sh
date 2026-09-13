#!/bin/bash
# launch_qa_secuura_ks877_977_r2.sh — cross-project QA agent, TIER 2 (through code: a build script that
# refuses its own inputs plus the shell suite that pins it; docker a recording stub on a private PATH, no
# daemon, no image, no stack) gate ROUND 2 OF 2 under the two-NO-GO cap on Secuura KS-877 (+ KS-922's two
# comment items), PR #977 @ aede93117 — TWO commits on origin develop's M6 0f69129b3: the r1 head a70585823
# (gated GO WITH FINDINGS 2026-09-13 17:31 AEST — F1 Major: the new suite RED on CI's ubuntu because
# docker-build.sh's `((RUNNING++))` :281 / `((RUNNING--))` :240 return status 1 at value 0 and bash >= 4.1
# `set -e` exits the script on it; pre-existing since ca7c2bf03) and the r2 commit aede93117 (parent a70585823,
# tree e97251c27, +92 -8, the PR's own TWO files: docker-build.sh +11 -2 — :240 / :290 are now the ASSIGNMENTS
# RUNNING=$((RUNNING - 1)) / RUNNING=$((RUNNING + 1)) under a 9-line why-comment :281-289, blob 1b7d59660 ->
# 4511614b9, sha256 90565cd4503efbde..., 316 lines; and docker_build_empty_table.test.sh +81 -6 — CELL 4 the
# STATIC pin on the construct's absence with its positive control inside the cell, CELL 5 the MASK control,
# TOTAL_CELLS=5 with `(of 5 cells)` + INCOMPLETE, O1/O2; blob e37212b89 -> 821828e37, sha256 411ed6bb09f95fb9...,
# 215 lines, mode 100644). PR files API: 2 files +250 -7.
#
# Round 2 re-gates: (1) F1 CLOSED at the new head by READING both lines, by the MECHANISM on bash 3.2 (the only
# bash on the box — `((R++))` at 0 -> status 1, the assignment -> 0) and by CI's per-suite line at the new head
# as the RUNTIME instrument (run 34750512638 / job 103706122580 / step 11; the job log is 401 to the project
# token — round 1 read it through the machine's global gh login, read-only); (2) the suite RUN on 3.2 at head,
# red-first vs the r1 bytes (CELL 4 only) and the base bytes (CELLs 1 + 4), the tamper table with Tn/To on the
# new lines beside round 1's eight, cells-run quoted; (3) CELL 5 red-proofed itself (Tp, Tp2, Tp3); (4) no NEW
# defect from the r2 diff and the static pin's BOUNDARY measured (Tq, Tr); (5) delivered-vs-commissioned against
# the s208 brief + Wednesday's ANSWER (Q-bash NO install; Q-C3 -> KS-1138; Q-home description only + KS-1139;
# Q-cells taken); (6) the cap — round 2 of 2: the verdict names what ships and what is ticketed.
#
# Merge-base = the PR's parent M6 0f69129b3 (GitHub compare develop...head: diverged, ahead 2 / behind 8,
# 2 files — exit 10 if it changes). origin develop = M14 6b62ae446 (the KS-885 KS-886 squash, 10:06:37Z; read 20:08 AEST
# 2026-09-13); M6..M14 = 8 squashes, 22 files, NONE of #977's two (three scripts/__tests__/ suites are in that
# delta — the runner reaches 26 at head, 27 at develop, 28 on the merged tree; docker-build.sh's blob at develop
# is M6's 64a5a4697). The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has moved past
# M14 (the merge seat s209 is merging #980 next — packages/shared/src/__tests__/ only), the GitHub compare of that
# delta is read and the launcher REFUSES (exit 18) only when the delta touches a GUARDED path — #977's two files,
# scripts/run-shell-suites.sh (the consumer), .github/workflows/pr-security-gates.yml (the CI step that is the
# runtime instrument) — or cannot be judged (unreadable, not ahead, >250 files); otherwise it proceeds printing the
# move and its file count, which the gate re-states (brief items 1 and 7). A refusal means: confirm the new delta,
# then re-pin DEVELOP_SHA here AND in the brief's TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #973 round-2 launcher by gen_launcher_977r2.py (asserted substitutions, two asserted
# insertions — round 1's head-SHA-in-both guard at a NEW distinct exit 20 and its --check line — residual
# guard): same guards and exit codes 2..19 plus exit 20, re-pointed at #977 round 2.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks877_977_r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..20 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA977R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2-r2.md}"
PROMPT_FILE="${QA977R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-877-docker-build-empty-table-guard'
HEAD_SHA="${QA977R2_HEAD:-aede931172dde738912cf5d439681e02d30405e2}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='6b62ae446f652182bc014994cd3ecd912e46becd'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-977-ks877-tier2-r2.md"

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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M14, the develop this brief was written against; git ls-remote)"
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
GUARDED = ["Blockchain/Dev/scripts/docker-build.sh",
           "Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           ".github/workflows/pr-security-gates.yml"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's four paths (#977's two files, run-shell-suites.sh, pr-security-gates.yml); the gate merges the then-current develop and re-states the delta by name (brief items 1 and 7)" ;;
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

R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks877-977-a70585823-tier2-r1/report.md'
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

[ -z "${QA977R2_BRIEF:-}${QA977R2_PROMPT:-}${QA977R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
