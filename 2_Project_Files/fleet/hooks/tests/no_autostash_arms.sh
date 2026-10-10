#!/bin/bash
# Arms for pretooluse_no_autostash.sh: expected rc per command (2 = refused, 0 = passed).
# A refusal arm also requires stderr to name the hook. Optional 3rd arg = CLAUDE_PROJECT_DIR for
# that arm (otherwise it is UNSET, so the hook falls back to its own self-located root).
# HOOK_UNDER_TEST=<path> runs the arms against another copy (the red run against the old hook).
H="${HOOK_UNDER_TEST:-$(cd "$(dirname "$0")/.." && pwd)/pretooluse_no_autostash.sh}"; P=0; F=0
ERR=$(mktemp "${TMPDIR:-/tmp}/no_autostash_arm.XXXXXX")
arm() { local want=$1 cmd=$2 pd=${3:-}; local envargs=(-u CLAUDE_PROJECT_DIR)
  [ -n "$pd" ] && envargs+=("CLAUDE_PROJECT_DIR=$pd")
  got=$(python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$cmd" | env "${envargs[@]}" bash "$H" 2>"$ERR"; echo $?)
  local named=yes; [ "$want" = 2 ] && ! grep -q "pretooluse_no_autostash" "$ERR" && named=no
  if [ "$got" = "$want" ] && [ "$named" = yes ]; then P=$((P+1)); echo "PASS want $want  $cmd" | head -1; else F=$((F+1)); echo "FAIL want $want got $got (stderr names hook: $named)  $cmd" | head -1; fi; }
arm 2 'git pull --rebase --autostash'
arm 2 'git -C /Volumes/DevMASTER/WEDNESDAY rebase --autostash origin/main'
arm 2 'git -c rebase.autoStash=true pull --rebase'
arm 2 'git stash push -- 0_Brain/dashboard/data/'
arm 2 'echo hi && git -C $W rebase --autostash origin/main'
arm 2 'git -C "/Volumes/DevMASTER/WEDNESDAY" stash push -m x -- 0_Brain/dashboard/data'
arm 0 'git pull --rebase --no-autostash'
arm 0 'git stash push -- 0_Brain/dashboard/data/news.json'
arm 0 'git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" log --oneline -1'
arm 0 "cat > /tmp/b.md <<'X'
git pull --rebase --autostash
X"
arm 0 'git status --short'
# ── added 2026-10-10 (Friday): $VAR-prefixed git, and -C naming the seat's own root ──
arm 2 'bash -c '\''G="git -C /Volumes/Laptop-DEV/FRIDAY"; $G status --short; $G pull --rebase --autostash 2>&1 | tail -4'\'''
arm 2 'git -C /Volumes/Laptop-DEV/FRIDAY pull --rebase --autostash' /Volumes/Laptop-DEV/FRIDAY
arm 2 'git -C /Volumes/Laptop-DEV/MYSEAT/sub pull --rebase --autostash' /Volumes/Laptop-DEV/MYSEAT
arm 2 'G=git; ${G} pull --autostash'
arm 0 'git -C "/Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/2_Project_Files" pull --rebase --autostash' /Volumes/Laptop-DEV/FRIDAY
arm 0 'bash -c '\''G="git -C /Volumes/Laptop-DEV/FRIDAY"; $G pull --rebase --no-autostash'\'''
arm 0 'G="git -C /Volumes/Laptop-DEV/FRIDAY"; $G status --short'
got=$(printf 'not json' | bash "$H" 2>/dev/null; echo $?); [ "$got" = 0 ] && { P=$((P+1)); echo "PASS fail-open on bad input"; } || { F=$((F+1)); echo "FAIL fail-open got $got"; }
echo "== $P pass, $F fail"; [ "$F" = 0 ]
