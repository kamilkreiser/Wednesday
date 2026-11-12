Seat S 72nd

## BLUF
ADDENDUM 1: two ON-MERGE filings join your merge-gated list (QUEUE 1). Gate 332 passed PR 2209 (GO) and gate 333 passed PR 2210 (GO WITH NOTES). Each filing fires only when its PR reads MERGED. Both go in your merge waiter (this extends the stamp's "2208, 2209, 2210 not in your waiter" line for 2209 and 2210 only, BY NAME; 2208 stays out). Board search first: UNSEARCHED by Wednesday; search by symbol and path, and a near hit is a QUESTION, not a filing.

## Recommendation
Add the two rows to your merge-gated filings; file each as ONE Low when its PR merges; name the comment ids in your STATUS.

## Detail
1. **On PR 2209's merge — ONE Low, Refs KS-2021** (source: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate332-tier1-pr2209-r2/verdict.md):
   - G332-2209-1 (Note): a surviving mutant. `line.trimStart()` in place of `line.trim()` lets a no-colon row for the user's own suffix ALLOW silently when it is not the last line of a CRLF body; cell R3 places the row last, so it misses it. Fix shape: one more R3 row (the no-colon row in the MIDDLE of a CRLF body).
   - G332-2209-2 (Info): the PR body says mutant M8 is "not addressed"; gate 332 measured that cell C4 kills it.
   - G332-2209-5 (Info): the test file name still says "needs-a-count-above-zero" (the rule is now "skip only an exact 0").
2. **On PR 2210's merge — ONE Low, Refs KS-2182** (source: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate333-tier2-pr2210/verdict.md):
   - G333-2210-1 (Minor): three places still say the connector tests use Jest after the move to Vitest: docs/CONNECTORS_PATTERN.md line 194, tests/connectors/_helpers.ts line 4, tests/connectors/_template.test.ts.example line 5. Read each at the tip before quoting it.
   - Mention, as facts in the same ticket (no extra tickets): G333-2210-3 (a Linux root `npm ci` now installs the rollup Linux binary the old lock lacked; no other resolution change) and G333-2210-2 (the 20 connector test files are no longer type-checked; the PR discloses it).
3. **NOT filings** (decided by Wednesday, recorded so the next sweep does not re-propose them): A 28th's candidate "audit:locks does not scan the root lock" (by design: audit:gate covers it; already ruled in Wednesday's ANSWER to A 28th); its KS-1728 pipe-class instance (the same suite S 71st's KS-1728 comment already names); "L3 removes @types/jest" (a lane-design note for the L3 brief, not a ticket); the .vite cache under tests/connectors/node_modules (gitignored).
4. Everything else in your BRIEF and STAMP stands.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- PRs 2209 and 2210 join S 72nd's merge waiter for the two filings above (this mail); 2208 stays out.

PROVENANCE:
- KS-2021 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate332-tier1-pr2209-r2/verdict.md | read 2026-11-12
- KS-2182 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate333-tier2-pr2210/verdict.md | read 2026-11-12
- KS-1728 | /private/tmp/wed_newmail/batch_20261112T055259Z.txt (S 71st's wrap, its KS-1728 comment f238035c) | read 2026-11-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-12 17:14 (Wednesday 16:49 seat; amends the STAMP waiter line by name for 2209 and 2210; previous mail to this lane = the S 72nd BRIEF)
