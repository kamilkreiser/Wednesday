#!/bin/bash
# launch_qa_secuura_ks1123_1002_ks1165_1003.sh — cross-project QA agent, TIER 2 (through code) gate ROUND 1 on TWO
# test-only Secuura PRs in ONE pass, one verdict per PR (both Seat A, both services/api-gateway, no shared file):
#   PR #1002 (KS-1123) @ a376756ab, branch feature/ks-1123-ornith-verify-status-pins — two new test files (F3, F2) plus
#            comment-only edits in routes/verification.ts; one commit on develop 80686962; "Part of KS-1123";
#   PR #1003 (KS-1165) @ c5488a689, branch feature/ks-1165-f1-real-app-mount-cell — a real-app CSRF mount-order test
#            file plus a header fix in the merged composed ks1165 test; one commit on develop 5b4f38a48; "Closes KS-1165".
#
# THE SHAPE, as read 22:36-22:51 AEST 2026-09-16 (git + the compare API agree): the PRs have DIFFERENT bases. Each head's
# parent is its merge-base with develop (80686962 and 5b4f38a48). Develop is 5b4f38a48 (#1001 merged). The compare
# develop...head is asserted PER PR as merge_base + ahead + files (exits 13/10); `behind` is deliberately NOT asserted,
# so develop moving on does not trip it. A landed PR reads ahead=0 and refuses there.
#
# exit 18 (the develop arm): develop MAY move — the brief tells the gate to merge the then-current develop onto each
# head in its clone and re-derive — but a move that touches either PR's files, the files their tampers anchor in
# (routes/verification.ts, src/index.ts, middleware/csrf.ts, middleware/contentType.ts), the api-gateway
# vitest/tsconfig/package files or the Dev lockfile refuses, as does an unjudgeable move.
#
# Adapted from launch_qa_secuura_ks1130_999_ks960_1000.sh by gen_launcher_1002_1003.py (asserted substitutions, residual
# guard, positive controls, heredoc check, bash -n): the same guards and exit codes — exit 6 per head, exits 13/10 per
# PR, exit 20 (brief or prompt does not name a pinned head SHA), exit 21 (the LAUNCH path refuses a non-TTY stdin),
# exit 12 (the prompt must name wednesday-agent@agentmail.to) — plus exit 18 above.
#
# Written by the generator because it contains a legitimate `cd`.
#
# Usage: launch_qa_secuura_ks1123_1002_ks1165_1003.sh [--check]
# Exit: 0 launched (or guards passed under --check) · 2..18, 20, 21 a guard refused
set -u

QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'
WED='/Volumes/DevMASTER/WEDNESDAY'
BRIEF="${QA10021003_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.md}"
PROMPT_FILE="${QA10021003_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.prompt.txt}"
REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'
SECUURA_ENV='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env'
BRANCH='refs/heads/feature/ks-1123-ornith-verify-status-pins'
HEAD_SHA="${QA1002_HEAD:-a376756aba1e1ae32c49ed47ba057fd80c7ed136}"
MERGE_BASE='80686962828197acf305e4010a2ed5b401285743'        # #1002: the head's parent = its merge-base with develop
BRANCH_1003='refs/heads/feature/ks-1165-f1-real-app-mount-cell'
HEAD_1003="${QA1003_HEAD:-c5488a6891e6ac6fe950c101196d8c33ab8e173f}"
MERGE_BASE_1003='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'   # #1003: the head's parent = its merge-base with develop
DEVELOP_SHA='5b4f38a48aeb40c2295895aaa5cd08e273aa7a08'       # develop at draft time, #1001 merged (read 22:36:56, 22:49:03, 22:51:05 AEST)
REAL_BRIEF="$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-16_secuura-1002-1003-ks1123-ks1165-tier2.md"

[ -d "$QA_DIR" ]         || { echo "QA project missing: $QA_DIR" >&2; exit 2; }
[ -s "$BRIEF" ]          || { echo "brief missing or empty: $BRIEF" >&2; exit 3; }
[ -s "$PROMPT_FILE" ]    || { echo "prompt file missing or empty: $PROMPT_FILE" >&2; exit 4; }
[ -d "$REPO" ]           || { echo "repo under test missing: $REPO" >&2; exit 5; }

# TWO heads, each pinned at its own branch on origin; a moved head names its PR (exit 6).
for pair in "1002|$HEAD_SHA|$BRANCH" "1003|$HEAD_1003|$BRANCH_1003"; do
  PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; PR_BRANCH="${REST#*|}"
  if ! git -C "$REPO" ls-remote origin "$PR_BRANCH" | grep -q "^${PR_HEAD}[[:space:]]"; then
    echo "REFUSING: #$PR_N head $PR_HEAD is not at $PR_BRANCH on origin — the head moved; the brief is about a different SHA" >&2
    git -C "$REPO" ls-remote origin "$PR_BRANCH" >&2
    exit 6
  fi
done

# The compare develop...head, read PER PR from the GitHub compare API and asserted as merge_base + ahead + files
# (NOT behind; see the header). The two PRs have DIFFERENT bases. exit 13 unreadable, exit 10 changed.
COMPARES=""
for pair in "1002|$HEAD_SHA|$MERGE_BASE|3" "1003|$HEAD_1003|$MERGE_BASE_1003|2"; do
PR_N="${pair%%|*}"; REST="${pair#*|}"; PR_HEAD="${REST%%|*}"; REST="${REST#*|}"; PR_MB="${REST%%|*}"; PR_FILES="${REST#*|}"
COMPARE="$(
  set -a; . "$SECUURA_ENV"; set +a
  HEAD_SHA="$PR_HEAD" python3 - <<'PY'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/develop..." + os.environ["HEAD_SHA"]
r = urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60)
c = json.load(r)
print("%s ahead=%d files=%d" % (c["merge_base_commit"]["sha"], c["ahead_by"], len(c.get("files") or [])))
PY
)"
[ -n "$COMPARE" ] || { echo "REFUSING: could not read the compare develop...#$PR_N from the GitHub compare API" >&2; exit 13; }
[ "$COMPARE" = "$PR_MB ahead=1 files=$PR_FILES" ] || { echo "REFUSING: #$PR_N develop...head reads '$COMPARE', brief pins '$PR_MB ahead=1 files=$PR_FILES'" >&2; exit 10; }
COMPARES="$COMPARES #$PR_N $COMPARE;"
done

# The develop arm (exit 18). Develop MAY move; a move touching a GUARDED path, or one that cannot be judged, refuses.
CUR_DEV="$(git -C "$REPO" ls-remote origin refs/heads/develop | cut -f1)"
[ -n "$CUR_DEV" ] || { echo "REFUSING: could not read origin develop (git ls-remote)" >&2; exit 18; }
if [ "$CUR_DEV" = "$DEVELOP_SHA" ]; then
  DEV_NOTE="origin develop still $DEVELOP_SHA (the draft reading: #1001 merged; #1003 sits on it, #1002 is one merge behind and file-disjoint)"
else
  DEV_JUDGEMENT="$(
    set -a; . "$SECUURA_ENV"; set +a
    DEVELOP_SHA="$DEVELOP_SHA" CUR_DEV="$CUR_DEV" python3 - <<'PYJ'
import json, os, urllib.request
t = os.environ.get("GH_TOKEN", "")
u = "https://api.github.com/repos/Secuura/Distributed_Secuura/compare/" + os.environ["DEVELOP_SHA"] + "..." + os.environ["CUR_DEV"]
try:
    c = json.load(urllib.request.urlopen(urllib.request.Request(u, headers={"Authorization": "Bearer " + t, "Accept": "application/vnd.github+json"}), timeout=60))
except Exception as e:
    print("UNJUDGEABLE compare unreadable: " + type(e).__name__)
    raise SystemExit(0)
files = [f["filename"] for f in (c.get("files") or [])]
if c.get("status") != "ahead" or len(files) >= 300:
    print("UNJUDGEABLE status=%s files=%d" % (c.get("status"), len(files)))
    raise SystemExit(0)
A = "Blockchain/Dev/services/api-gateway/"
GUARDED = [A + "src/routes/verification.ts",
           A + "src/index.ts",
           A + "src/middleware/csrf.ts",
           A + "src/middleware/contentType.ts",
           A + "src/__tests__/ks1123-f2-anchor-failed-stale-confidence.test.ts",
           A + "src/__tests__/ks1123-f3-empty-status-is-off-chain.test.ts",
           A + "src/__tests__/ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts",
           A + "src/__tests__/ks1165-real-app-csrf-mount-order.test.ts",
           A + "vitest.config.ts",
           A + "vitest.setup.ts",
           A + "tsconfig.json",
           A + "package.json",
           "Blockchain/Dev/package-lock.json"]
hits = sorted(f for f in files if f in GUARDED)
if hits:
    print("GUARDED " + " ".join(hits))
    raise SystemExit(0)
print("OK origin develop MOVED %s -> %s: commits=%d files=%d, none on the GUARDED list; the gate merges the then-current develop onto each head in its clone and re-derives, brief D1 and item 4" % (os.environ["DEVELOP_SHA"][:9], os.environ["CUR_DEV"][:9], c["ahead_by"], len(files)))
PYJ
  )"
  case "$DEV_JUDGEMENT" in
    OK*) DEV_NOTE="${DEV_JUDGEMENT#OK }" ;;
    *) echo "REFUSING: origin develop is at $CUR_DEV (pinned $DEVELOP_SHA) and the move is not provably clear of #1002/#1003: ${DEV_JUDGEMENT:-no judgement} — confirm the delta, then re-pin deliberately (launcher DEVELOP_SHA + brief D1 + prompt)" >&2
       exit 18 ;;
  esac
fi

grep -q 'TIER 2' "$BRIEF" && grep -q 'TIER 2' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the tier" >&2; exit 7; }
grep -q 'ROUND 1' "$BRIEF" && grep -q 'ROUND 1' "$PROMPT_FILE" || { echo "REFUSING: brief and prompt disagree about the round" >&2; exit 15; }
head -1 "$PROMPT_FILE" | grep -q 'ultrathink' || { echo "REFUSING: prompt does not open with the thinking directive" >&2; exit 8; }
grep -qF "$REAL_BRIEF" "$PROMPT_FILE" || { echo "REFUSING: prompt does not name the brief path" >&2; exit 9; }
for sha in "$HEAD_SHA" "$HEAD_1003"; do
  grep -qF "$sha" "$PROMPT_FILE" && grep -qF "$sha" "$BRIEF" \
    || { echo "REFUSING: brief or prompt does not name the head SHA $sha — a gate about another SHA is another gate" >&2; exit 20; }
done
grep -qi 'MAIL YOUR VERDICT' "$PROMPT_FILE" && grep -qF 'wednesday-agent@agentmail.to' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not tell the agent to MAIL its verdict to wednesday-agent@agentmail.to" >&2; exit 12; }
grep -qi 'NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid pushing / running the hook in the real checkout" >&2; exit 11; }
grep -qi 'no memory maintenance' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid memory maintenance inside the gate session" >&2; exit 14; }
grep -qi 'NEVER print a credential value' "$PROMPT_FILE" \
  || { echo "REFUSING: prompt does not forbid printing a credential value" >&2; exit 17; }

if [ "${1:-}" = "--check" ]; then
  echo "all guards pass:"
  echo "  #1002 head $HEAD_SHA present at $BRANCH on origin"
  echo "  #1003 head $HEAD_1003 present at $BRANCH_1003 on origin"
  echo "  compare develop...head (GitHub API, per PR):$COMPARES"
  echo "  $DEV_NOTE"
  echo "  brief, prompt, QA project and repo all present"
  echo "  brief and prompt agree on TIER 2 and ROUND 1"
  echo "  prompt opens with the thinking directive and names the brief"
  echo "  brief and prompt both name both head SHAs"
  echo "  prompt tells the agent to MAIL its verdict to wednesday-agent@agentmail.to"
  echo "  prompt forbids pushing / the real hook / preflight in the Secuura checkout"
  echo "  prompt forbids memory maintenance inside the gate session"
  echo "  prompt forbids printing a credential value"
  echo "  a launch (not --check) will refuse unless stdin is a TTY (exit 21)"
  exit 0
fi

[ -t 0 ] || { echo "REFUSING: stdin is not a TTY — this launcher execs an interactive agent; run it in a cockpit pane, never inside a Bash tool" >&2; exit 21; }
[ -z "${QA10021003_BRIEF:-}${QA10021003_PROMPT:-}${QA1002_HEAD:-}${QA1003_HEAD:-}" ] || { echo "REFUSING: a launch with test overrides set" >&2; exit 16; }
echo "$DEV_NOTE" >&2
cd "$QA_DIR" || { echo "cannot enter $QA_DIR" >&2; exit 16; }
exec claude --dangerously-skip-permissions --model opus "$(cat "$PROMPT_FILE")"
