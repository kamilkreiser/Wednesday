#!/bin/bash
# safe_push_silent_pull_arms.sh — red-proof for the 2026-09-17 safe_push fix (rc 24).
# THE DEFECT: a pull that is neither a success nor a conflict (e.g. an orphaned
# .git/rebase-merge/ holding only an autostash, the 00:44 case) broke out of the pull
# loop SILENTLY; the only output was "WARNING HEAD != origin", rc 3.
# Usage: safe_push_silent_pull_arms.sh <candidate safe_push.sh> [<old safe_push.sh>]
#   Each arm builds a throwaway repo pair under a mktemp dir in $ARMS_SCRATCH (default
#   $TMPDIR) — nothing is deleted (never-delete rule); the dirs stay for inspection.
# Arms:
#   ARM1 defect  : planted rebase-merge/autostash → candidate rc 24 + "PULL FAILED" + git's own "rebase-merge" text
#   ARM1-OLD     : the same plant against the OLD script → rc != 24 and no "PULL FAILED" (proves ARM1 discriminates)
#   ARM2 control : clean tree, local commit → rc 0, "HEAD == origin"
#   ARM3 control : origin ahead (a second clone pushed) → rc 0, rebased, "HEAD == origin"
#   ARM4 control : nothing new on either side → rc 0 (no false 24 on an up-to-date pull)
set -u
CAND="${1:?candidate safe_push.sh}"; OLD="${2:-}"
SRC_TOOLS="$(cd -P "$(dirname "$CAND")" && pwd)"
BASE="$(mktemp -d "${ARMS_SCRATCH:-${TMPDIR:-/tmp}}/sp_arms.XXXXXX")"
PASS=0; FAIL=0
ok()  { echo "PASS $*"; PASS=$((PASS+1)); }
bad() { echo "FAIL $*"; FAIL=$((FAIL+1)); }

mkpair() {  # $1 = arm dir, $2 = safe_push to install → prints nothing; builds $1/origin.git + $1/repo
  local d="$1" sp="$2"
  mkdir -p "$d"
  git init -q --bare -b main "$d/origin.git"
  git init -q -b main "$d/repo"
  git -C "$d/repo" config user.email arms@example.invalid
  git -C "$d/repo" config user.name arms
  mkdir -p "$d/repo/2_Project_Files/tools" "$d/repo/0_Brain/dashboard/data"
  cp "$sp" "$d/repo/2_Project_Files/tools/safe_push.sh"
  for h in union_chat_log.py union_decisions.py union_scoreboard.py; do cp "$SRC_TOOLS/$h" "$d/repo/2_Project_Files/tools/$h"; done
  echo seed > "$d/repo/seed.txt"
  git -C "$d/repo" add -A
  git -C "$d/repo" commit -q -m seed
  git -C "$d/repo" remote add origin "$d/origin.git"
  git -C "$d/repo" push -q -u origin main
}
run_sp() {  # $1 = arm dir, $2 = msg, $3 = path → sets RC, OUTF
  OUTF="$1/sp.out"
  SAFE_PUSH_SCRATCH="$1/scratch" bash "$1/repo/2_Project_Files/tools/safe_push.sh" "$2" "$3" > "$OUTF" 2>&1
  RC=$?
}

# ARM1 — the defect, candidate
A="$BASE/arm1"; mkpair "$A" "$CAND"
echo change1 > "$A/repo/a1.txt"
mkdir -p "$A/repo/.git/rebase-merge"; echo deadbeef > "$A/repo/.git/rebase-merge/autostash"
run_sp "$A" "arm1" a1.txt
if [ "$RC" -eq 24 ] && grep -q 'PULL FAILED' "$OUTF" && grep -qi 'rebase-merge' "$OUTF"; then ok "ARM1 defect → rc 24 with git's text"; else bad "ARM1 rc=$RC"; sed 's/^/    /' "$OUTF"; fi

# ARM1-OLD — the same plant against the old script must NOT produce the new behaviour
if [ -n "$OLD" ]; then
  A="$BASE/arm1old"; mkpair "$A" "$OLD"
  echo change1 > "$A/repo/a1.txt"
  mkdir -p "$A/repo/.git/rebase-merge"; echo deadbeef > "$A/repo/.git/rebase-merge/autostash"
  run_sp "$A" "arm1old" a1.txt
  if [ "$RC" -ne 24 ] && ! grep -q 'PULL FAILED' "$OUTF"; then ok "ARM1-OLD old script stays silent (rc=$RC) — the arm discriminates"; else bad "ARM1-OLD rc=$RC"; sed 's/^/    /' "$OUTF"; fi
fi

# ARM2 — clean control
A="$BASE/arm2"; mkpair "$A" "$CAND"
echo change2 > "$A/repo/a2.txt"
run_sp "$A" "arm2" a2.txt
if [ "$RC" -eq 0 ] && grep -q 'HEAD == origin' "$OUTF"; then ok "ARM2 clean → rc 0"; else bad "ARM2 rc=$RC"; sed 's/^/    /' "$OUTF"; fi

# ARM3 — origin ahead control
A="$BASE/arm3"; mkpair "$A" "$CAND"
git clone -q "$A/origin.git" "$A/other"
git -C "$A/other" config user.email arms@example.invalid; git -C "$A/other" config user.name arms
echo theirs > "$A/other/b3.txt"; git -C "$A/other" add b3.txt; git -C "$A/other" commit -q -m theirs; git -C "$A/other" push -q origin main
echo ours > "$A/repo/a3.txt"
run_sp "$A" "arm3" a3.txt
if [ "$RC" -eq 0 ] && grep -q 'HEAD == origin' "$OUTF" && [ -f "$A/repo/b3.txt" ]; then ok "ARM3 origin ahead → rebased, rc 0"; else bad "ARM3 rc=$RC"; sed 's/^/    /' "$OUTF"; fi

# ARM4 — nothing new anywhere control (no false 24)
A="$BASE/arm4"; mkpair "$A" "$CAND"
run_sp "$A" "arm4" seed.txt
if [ "$RC" -eq 0 ] && ! grep -q 'PULL FAILED' "$OUTF"; then ok "ARM4 up to date → rc 0, no false 24"; else bad "ARM4 rc=$RC"; sed 's/^/    /' "$OUTF"; fi

echo "arms: $PASS pass, $FAIL fail (dirs under $BASE)"
[ "$FAIL" -eq 0 ]
