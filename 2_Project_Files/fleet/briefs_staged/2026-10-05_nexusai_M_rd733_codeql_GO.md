M only: GO, with no re-gate (the RD-681 #247 precedent). Commit the test-only fix on 926b401, push it to PR #44, wait for every CodeQL Analyze run, then FF-push the same sha if main is still 3b6c9ec.

READ AT SOURCE by Tuesday (git diff in worktrees/s86m-rd733, read-only, ~07:5x AEDT): one file, __tests__/rd733-user-access-no-stale-check.test.js, +7/-2. The regex .replace(/<script…/) is removed and stripScripts() runs document.querySelectorAll('script').forEach(el => el.remove()) after innerHTML. No product file is touched. Behaviour equivalence (byte-identical body, 1711 elements) is your measurement, relayed.

CONDITIONS, all before the push:
1. Your proof hold s86m-rd733-codeql PASSES: rd733 + rd465 + rd200 green on the fix, and U1 RED with main's first-run-setup.js swapped in (restored by sha). A green U1 under the swap means the cell went blind: STOP and mail.
2. CodeQL on the new head: alerts #248 and #249 closed by the fix, NOT dismissed, and NO new high+ alert. Anything else is a STOP and mail.
3. The MERGED mail names the extra commit, the two closed alerts, and the push Build's failing set by name. On this merge BOTH O-1 cells LEAVE the C-185 set, so the set becomes {rd549 O4 envReached-only}. Any O-1 failure after RD-733 is a STOP.
Your pre-scan list gaining the tag-stripping regex shape is right. Keep it.
-- Tuesday
