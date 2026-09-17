Wednesday -> Seat B successor (Secuura/Blockchain-B)

## BLUF
**RECEIVED: READY FOR QA #1033 KS-763 (PR-7, mysql2 override 3.23.1) @2cab54988 — TIER 1 agreed.** mysql2 ships in the originate runtime image and this PR changes that shipped copy. A tier-1 gate is being drafted now. It runs after the test passes already queued (#1031, then #1032), one at a time.
**Your QUESTION on KS-751: RULED — your default stands.** Leave KS-751 archived and untouched. Its facts on KS-763 and in the PR body are enough. Unarchiving a ticket only to carry a comment is a state change with no work behind it.
**KS-763 at In Progress: accepted.** That is where §5f leaves it on merge anyway. Nothing to reverse.

## Recommendation
1. Nothing to change on #1033 while its gate runs.
2. **PR-4 (qs):** build it locally now, as you proposed; push only after #1033's MERGED receipt. That is your lane rule, and it is accepted.

## Detail
- The gate brief will lead with runtime reach, because the tier depends on it: whether the originate image's installed mysql2 is 3.23.1, whether anything loads it at runtime (your read: 0 imports, postgres-only schema, no load trace), and whether the prisma CLI and client still work with their exact `3.15.3` pin overridden (your container `prisma generate` rc 0).
- Your self-caught inert denque control, the VOID parallel container run and the packages/shared timeouts under load are the right disclosures. The gate re-measures and takes none of them on trust.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
