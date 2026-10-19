#!/bin/bash
# Arms for the 2026-10-20 widening of pretooluse_no_cd.sh's git write-verb clause
# (--git-dir / --work-tree / GIT_DIR= now name the target exactly as -C does; gate AU1 N1).
# Usage: no_cd_gitdir_arms.sh [hook-path]   (default: the live hook beside ../hooks/)
set -u
SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK="${1:-$SELF_DIR/../hooks/pretooluse_no_cd.sh}"
P=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files
PASS=0; FAIL=0
arm() { # name want_rc command
  local name="$1" want="$2" cmd="$3"
  local json; json=$(python3 -c 'import json,sys; print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$cmd")
  printf '%s' "$json" | bash "$HOOK" > /dev/null 2>"$TMPDIR/arm.err"; local rc=$?
  if [ "$rc" = "$want" ]; then PASS=$((PASS+1)); echo "PASS $name (rc $rc)"; else FAIL=$((FAIL+1)); echo "FAIL $name (rc $rc, want $want)"; sed 's/^/    /' "$TMPDIR/arm.err" | head -3; fi
}
# FIRE: a write verb aimed at another project, in every form
arm "git -C <project> fetch (the original clause)" 2 "git -C $P fetch origin"
arm "git --git-dir=<project>/.git fetch"          2 "git --git-dir=$P/.git fetch origin"
arm "git --git-dir <project>/.git commit"         2 "git --git-dir $P/.git commit -m x"
arm "git --work-tree=<project> checkout"          2 "git --work-tree=$P checkout develop"
arm "GIT_DIR=<project>/.git git fetch"            2 "GIT_DIR=$P/.git git fetch origin"
arm "git --git-dir=\$VAR fetch (unresolvable: fail closed)" 2 'git --git-dir=$X/.git fetch origin'
# QUIET: allowed targets and reads
arm "git -C /private/tmp scratch fetch"           0 "git -C /private/tmp/wed_x fetch origin"
arm "git --git-dir=/private/tmp/.git fetch"       0 "git --git-dir=/private/tmp/wed_x/.git fetch origin"
arm "git -C <own tree> commit"                    0 "git -C /Volumes/DevMASTER/WEDNESDAY commit -m x"
arm "bare git log"                                0 "git log --oneline -3"
arm "bare git status"                             0 "git status --short"
arm "git -C <project> log (a read)"               0 "git -C $P log -1"
arm "git --git-dir=<project>/.git ls-remote (a read)" 0 "git --git-dir=$P/.git ls-remote origin"
arm "heredoc prose naming the bypass"             0 "cat > /private/tmp/x.md <<'EOF'
git --git-dir=$P/.git fetch origin
EOF"
echo "ARMS: $PASS pass, $FAIL fail"
[ "$FAIL" = 0 ]
