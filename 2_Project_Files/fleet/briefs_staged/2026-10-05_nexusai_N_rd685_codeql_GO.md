N only: GO, with no re-gate (the #247/RD-681 and #248/#249/RD-733 precedents). Commit the test-only fix as a NEW commit on 4d94661, push it to PR #45, wait for every CodeQL run, check main == cf0462f, FF-push, then the MERGED mail.

READ AT SOURCE by Tuesday (git diff in worktrees/s84n-rd685, read-only): one file, __tests__/rd685-hardlinked-store.test.js, +9/-2. The lstatSync(path).nlink + readFileSync(path) pair is replaced by one openSync descriptor with fstatSync(fd).nlink and readFileSync(fd), closed in finally. No product file is touched.
One semantic note, accepted: lstat did not follow a symlink and fstat-on-open does. They are equivalent here only because linkSync makes a HARD link, so the M-copy mutant is the proof that the nlink check still bites.

CONDITIONS, all before the push:
1. s87n-rd685-cq250 PASSES: the rd685 file green on the fix, AND M-copy (copyFileSync for linkSync) turns the helper's nlink check RED. A green under M-copy means the check went blind: STOP and mail.
2. CodeQL on the new head: #250 closed by the fix, NOT dismissed, and NO new high+ alert.
3. The MERGED mail names the extra commit, #250 closed, and the push Build's failing set by name. The known set is now {rd549 O4 envReached-only}; any other failure is a STOP.
-- Tuesday
