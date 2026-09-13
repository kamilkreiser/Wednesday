#!/bin/bash
# launch_qa_secuura_ks950_962_973_r2.sh — cross-project QA agent, TIER 1 (through code; a boot-path
# statement that WRITES the users table on api-gateway — PII/data integrity; no rendered surface, so the
# real-browser half of tier 1 does not apply) gate ROUND 2 OF 2 under the two-NO-GO cap on Secuura
# KS-950 / KS-962, PR #973 @ ca2a9109c — TWO commits on origin develop's M6 0f69129b3: the r1 head
# dfed981d0 (gated NO GO 2026-09-13 17:17 AEST on F-973-1 Major + F-973-2 Minor) and the r2 commit
# ca2a9109c (parent dfed981d0, tree a0f47e818, +59 -19, TEST FILES ONLY: the auth seed-site test
# ks949-platform-admin-seed-identity.test.ts +24 -7 blob 30ddc1c70 -> 67316e5da, and the suite
# ks949_main_seed_idempotence.test.sh +35 -12 blob 76a40a0ed -> 89c89fef8 mode 100755). The product file
# startup-migrations.ts is BYTE-IDENTICAL to r1 (blob ed3e52142, sha256 623a99b9531e7c2c...) — verified
# through the GitHub contents API at both heads. PR files API: 3 files +490 -38.
#
# Round 2 re-gates: (1) F-973-1 CLOSED at the new head by RUNNING — the auth test's enumeration cell pins the
# gateway's REMOVAL (:343-344 toBe(false)) and the identity cell names ONE site + pins the inverse on the
# gateway (:376, :381-382 .not.toContain); red-first against M6's product file must red EXACTLY those two
# with 28/30 run; (2) F-973-2 CLOSED — cell ID3 (:308-318, TOTAL_CELLS 27) pins the ruled IS DISTINCT FROM
# guard; Tg (guard line :1043 deleted) must red EXACTLY {ID3} with 27 cells run; (3) no NEW defect from the
# r2 diff (its own red-proof); (4) the r1 legs the r2 change could affect re-run; F-973-3 / F4 stand on
# KS-962 by ruling (comments 97fb9b93 / d863f815, KS-950 692689aa, KS-1125 f18bbf67 — exist, 0 mentions);
# (5) delivered-vs-commissioned against the s207 brief + Wednesday's ANSWER (P7 NOT taken by ruling; Q-A taken).
#
# Merge-base = the PR's parent M6 0f69129b3 (GitHub compare develop...head: diverged, ahead 2 / behind 4,
# 3 files — exit 10 if it changes). origin develop = M10 e91eb5bda (#972's squash, 17:37:11 AEST; read
# 19:14 AEST 2026-09-13); M6..M10 = 4 squashes, 15 files, NONE of #973's three (control: userRepo.ts IS in
# that delta — the brief's auth counts are stated at the head-on-M6 tree, the merged-tree count is the
# gate's own measurement). The develop pin below is DISJOINTNESS-CHECKED, not bare: if origin develop has
# moved past M10, the GitHub compare of that delta is read and the launcher REFUSES (exit 18) only when the
# delta touches a GUARDED path — #973's three files, auth's userRepo.ts (the twelve triples and the real
# seeder the suite imports), migrations/ and docker/init/ (the deployed shape the suite builds), the
# tenant-guc, run-shell-suites.sh, api-gateway's index.ts — or cannot be judged (unreadable, not ahead,
# >250 files); otherwise it proceeds printing the move and its file count, which the gate re-states (brief
# items 1 and 7). A refusal means: confirm the new delta, then re-pin DEVELOP_SHA here AND in the brief's
# TARGET section AND the prompt — a different brief, a deliberate edit.
#
# Adapted from the #978 tier-2 launcher by gen_launcher_973r2.py (asserted substitutions, two asserted
# insertions — the exit-19 round-1-report-path guard and its --check line — residual guard): same guards
# and exit codes, re-pointed at #973 round 2.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks950_962_973_r2.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..19 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA973R2_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1-r2.md}"
PROMPT_FILE="${QA973R2_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1-r2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-950-the-boot-seed-dies-permanently-at-boot-2-migration-030-drops'
HEAD_SHA="${QA973R2_HEAD:-ca2a9109cebf7ed73f916367b7c78b76d137e35c}"
MERGE_BASE='0f69129b3156d3adaf0af534a6527b9c3a8d3519'
DEVELOP_SHA='e91eb5bdaf68461e43a6055ed39137bd60a36749'
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-13_secuura-973-ks950-ks962-tier1-r2.md"

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
  DEV_NOTE="origin develop still $DEVELOP_SHA (M10, the develop this brief was written against; git ls-remote)"
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
GUARDED = ["Blockchain/Dev/services/api-gateway/src/startup-migrations.ts",
           "Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh",
           "Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts",
           "Blockchain/Dev/services/auth/src/repositories/userRepo.ts",
           "Blockchain/Dev/migrations/",
           "Blockchain/Dev/docker/init/",
           "Blockchain/Dev/packages/shared/src/db/tenant-guc.ts",
           "Blockchain/Dev/scripts/run-shell-suites.sh",
           "Blockchain/Dev/services/api-gateway/src/index.ts"]
hits = sorted({f["filename"] for f in files for g in GUARDED if f["filename"] == g or (g.endswith("/") and f["filename"].startswith(g))})
if hits:
    print("GUARDED " + " ".join(hits)); sys.exit(0)
print("DISJOINT commits=%d files=%d" % (c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    DISJOINT*) DEV_NOTE="origin develop MOVED $DEVELOP_SHA -> $CUR_DEV: ${DEV_JUDGEMENT#DISJOINT } — disjoint from the guard's nine paths (#973's three files, userRepo.ts, migrations/, docker/init/, tenant-guc.ts, run-shell-suites.sh, index.ts); the gate merges the then-current develop and re-states the delta by name (brief items 1 and 7)" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV, not the pinned $DEVELOP_SHA, and the delta is not provably disjoint: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief TARGET + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 1' "$BRIEF" && grep -q 'TIER 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 2' "$BRIEF" && grep -q 'ROUND 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

R1_REPORT='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-13-ks950-962-973-dfed981d0-tier1-r1/report.md'
grep -qF "$R1_REPORT" "$BRIEF" || { echo "REFUSING: brief does not name the round-1 report path (a gate cannot ask)" >&2; exit 19; }
[ -s "$R1_REPORT" ] || { echo "REFUSING: the round-1 report named by the brief is missing or empty: $R1_REPORT" >&2; exit 19; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  head $HEAD_SHA present at $BRANCH on origin"
  echo "  merge-base still $MERGE_BASE (GitHub compare API)"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 1 and ROUND 2"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  prompt tells the agent to MAIL its verdict"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  brief names the round-1 report and it is present on disk"
  exit 0
fi

[ -z "${QA973R2_BRIEF:-}${QA973R2_PROMPT:-}${QA973R2_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
