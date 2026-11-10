GATE B1433b: PROVISIONAL (jest runs pending) @ 725dcf0 on main 849b808

This file is a provisional checkpoint, written at 22:05 AEDT while the jest chain waits in the lock FIFO (queue position 1, behind qa-b1480-gate held since 20:03; load1 21-26, and my chain also waits for load1 < 7). It is NOT a verdict. If no final first line replaces this one, the gate did not finish.

## Measured so far (no jest yet)
| # | Check | Result |
|---|---|---|
| 1 | Ref | ls-remote refs/heads/b1433/nexusai-b-learning-manager-log-lines = 725dcf0ed76572af8773685769e5e5f1414745b2 (control: main printed 849b808c) |
| 2 | Commits | 1 commit, parent 3929b794; head tree d783697e (= builder's claim) |
| 3 | OWNS-B | 2 of 2 (backend/learningManager.js +5 -2; __tests__/rd798-learning-manager-log-lines.test.js +125 new). fnmatch program over the kit block; controls server.js, ticketStore.js, riskAlertScheduler.js, lane-T rd798 test, rd999, counts file all refused |
| 4 | Overlap | open PRs 0 (control closed per_page=3 -> 185,184,183); sibling b1431/b1432/b1433 branches 0 of 0 overlap (control self = 2) |
| 5 | Merge | merge-tree main+head rc 0, tree 220990a9; differs from main only by the 2 head paths, from head only by HISTORY.md (main blob) |
| 6 | Deploy demo | merge WOULD start a run (push to main; backend/ and __tests__/ not in paths-ignore). Jobs gated on vars.CI_DEPLOY_ENABLED; repo variables total_count 0; last 5 push runs skipped -> jobs would read skipped |
| 7 | Alerts | RD-798's 44 (list relayed from B1375 STATUS; membership not re-read in Jira, fenced): 25 fixed 2026-11-08 (162,163,187-207,222,223), 17 fixed earlier (172-186,220,221), 2 open (152,153 learningManager.js:125,153). This branch addresses 152 and 153 only. js/log-injection open on main overall: 2 (these) |
| 8 | Counts order | a 5501/327 counts commit on this branch MERGES CLEAN onto current main but CONFLICTS (scripts/verify-expected-counts.json) once the csp branch (3a5d3444, 5513/327) has landed |
| 9 | Scans | names 0 (controls 9/9), login 0 (control 1), GUID 0, hosts 0, secret-shaped 0, Cf 0 in added lines; non-ASCII only U+2192 (pre-existing arrow); gitleaks branch rc 0 (planted ghp_ control rc 1); CodeQL pre-scan 0 hits; repo Cf scan main = merge (5 files/5 chars) |
| 10 | Probes (node, not jest) | CR/LF, NEL, U+2029, ESC, object toString with LF: main leaks a break on 3 of 6, head 0 of 6; head truncates values over 500 chars (logSafe default) |

Pending: red-first (base blob plant + mutant), verify at main / head / merge / stack (main+csp+head) under qa-b1433b-gate.
