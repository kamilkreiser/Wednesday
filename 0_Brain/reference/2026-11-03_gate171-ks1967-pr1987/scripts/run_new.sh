#!/bin/bash
# usage: run_new.sh <label> <accountLockout.ts to use> [extra vitest args]
W=/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987; A=$W/repo/Blockchain/Dev/services/auth
cp "$2" $A/src/services/accountLockout.ts
env -i PATH=/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin HOME=$W/home TMPDIR=$W/tmp bash -c "cd $A && npx vitest run --root $A $3 src/__tests__/ks1967-lockout-fails-closed-while-the-session-store-is-down.test.ts" > $W/logs/new_$1.log 2>&1
echo "new $1 rc=$?"
git -C $W/repo show pr1987:Blockchain/Dev/services/auth/src/services/accountLockout.ts > $A/src/services/accountLockout.ts
sed 's/\x1b\[[0-9;]*m//g' $W/logs/new_$1.log | /usr/bin/grep -E '^ +Tests '
