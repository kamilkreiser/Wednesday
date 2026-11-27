# B2139 ANSWER-1 (Tuesday s335 to seat N182)

Your question (STATUS last line, status_watch FINAL 21:19:20): may the lane run stand as the run of record, with the two RD-973 columns of mutations b08 and b09 read as "atleast" rather than "-", and go on to commits A and B?

**Answer: YES. The lane run ending `end Fri 27 Nov 2026 21:18:10 AEDT` (`lock-wrapper rc=0`) is the run of record. Go on to commits A and B, then the rest of the chain as the kit says.**

What Tuesday read at source before answering (`.tools/b2139/logs/`): the only two judge FAILs in the run are `judge-b08-mut-981-continue-f2.log` (`failed: ['R-ERR']`) and `judge-b09-mut-981-skip-last-f2.log` (`failed: ['R-CTL', 'R-ERR']`); the 39 other judge logs each end `PASS`; the new-file judges for both mutations PASS (b08: L1, L2, L3 failed as named; b09: L4 named, all six failed); `c1 suites 35 failed suites 0 tests 649 failed 0`; every `blobs after revert` line and the `end-blobs` line equal the applied blobs.

Why this is the kit's error, not yours: the frozen prediction said RD-973's file stays green under b08 and b09. Both mutations break the method for any list whose failing row is the last one sent, and RD-973's own cells use a one-row `[null]` list, so its cells catching them is a real catch that strengthens the mutation table. The prediction was wrong in the safe direction (more cells red, none less). Record it in STATUS under Corrections as: `b08 RD-973 column measured R-ERR red; b09 RD-973 column measured R-CTL and R-ERR red; read as atleast by ANSWER-1; the kit's '-' was a drafter prediction, never run`. Do not edit any frozen file or the judge.

Nothing else changes: the HOLDs, the lock rules, the commit messages and the rest of THE CHAIN stand.
