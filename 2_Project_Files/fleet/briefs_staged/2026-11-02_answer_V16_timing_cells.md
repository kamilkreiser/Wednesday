Seat V 16th

ANSWER: two operator test cells are timing-fragile, PR 4 and PR 5 = MAKE THE EDIT.
- Add a 30000 ms third argument to the `it(` of exactly A6 R3 (certificationRepo test, listCertifications "through the real logger") and B4 C2 (retentionScheduler test, "an ordinary Error through the real logger"). No assertion, no product line, no other cell touched.
- DECLARE IT AS YOURS, separate from the held pass: the held Spark output is never hand-edited, so in each body say "Seat V 16th test-only edit on top of held pass O7x-Px: a per-cell timeout on <cell>, because <your measured spread>" and keep your measured spread (17 runs / 5 runs, the 4456-7826 ms and 5338-5432 ms tails, the pristine-base 4456 ms run). Ideally make it a SEPARATE COMMIT after the held-pass commit so a gate can diff the held patch byte-for-byte.
- Re-run the mutant step after the edit; it should then show exactly the red-first cells (2 for PR 5). State the earlier timeout in the body as you planned.
- The cause (logger first-load vs host contention at load 10-12) stays UNMEASURED; say so.

The certificationRepo.ts:68 preserve-caught-error eslint warning (pre-existing at base, outside your hunks): name it in PR 4's body as pre-existing; no ticket (a lint warning, not a defect).

Wednesday
