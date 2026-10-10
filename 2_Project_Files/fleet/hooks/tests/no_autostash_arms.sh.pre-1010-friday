#!/bin/bash
# Arms for pretooluse_no_autostash.sh: expected rc per command (2 = refused, 0 = passed).
H="$(cd "$(dirname "$0")/.." && pwd)/pretooluse_no_autostash.sh"; P=0; F=0
arm() { local want=$1 cmd=$2; got=$(python3 -c 'import json,sys;print(json.dumps({"tool_input":{"command":sys.argv[1]}}))' "$cmd" | bash "$H" 2>/dev/null; echo $?)
  if [ "$got" = "$want" ]; then P=$((P+1)); echo "PASS want $want  $cmd" | head -1; else F=$((F+1)); echo "FAIL want $want got $got  $cmd" | head -1; fi; }
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
got=$(printf 'not json' | bash "$H" 2>/dev/null; echo $?); [ "$got" = 0 ] && { P=$((P+1)); echo "PASS fail-open on bad input"; } || { F=$((F+1)); echo "FAIL fail-open got $got"; }
echo "== $P pass, $F fail"; [ "$F" = 0 ]
