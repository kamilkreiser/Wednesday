## BLUF
Gate 9 (tier 1, round 1 of 2), Seat R 6th:
- **#1797 (KS-1219): GO WITH NOTES.** Merge slot **106**. At your prep, add the missing null/0/false cell (test-only).
- **#1799 (KS-1467): GO WITH NOTES, with one Medium Wednesday rules as a ROUND 2 fix before merge.** Merge slot **107**.
Do not prep either yet. Wednesday mails each turn.

## #1799 round 2 (round 2 of 2 under the cap): conform to the PUBLISHED 422 contract; do not change the contract
- **The finding (gate 9, 1799-1):** the published 422 schema says `details` is a ZodIssue array. The three weak-password sites now send `details: {feedback:[...]}`, an object. KS-1467 itself said to check the published 422 shape first.
- **Ruling:** shape the weak-password `details` as a ZodIssue-compatible array (for example `[{ path: ['password'], message: <one feedback line>, code: 'custom' }]`, one entry per feedback line). Then the published contract stays true and no client sees a new shape. Do NOT widen the OpenAPI schema. Keep N1. Add a cell that asserts the 422 body validates against the published schema.
- **Add a ROUTE-LEVEL echo cell.** The gate found that a password echo added at a route site survives your cells, and its own route probe catches it. Pin that the 422 body through the real route never contains the submitted password.
- Re-run your 35 plus the new cells. Mail the new head for a delta gate.

## #1797 at prep
- Add a cell for the scope values null / 0 / false (302 -> 400; at base, approve minted a code with the full allow-list for these). The gate measured it on the wire; the PR has no cell.
- File ONE follow-up (search first; Low; board account; related to KS-1219): repeated `state` or `code_challenge` parameters still answer 500, the same class as the scope fix. Note in it that scope is neither deduplicated nor bounded (pre-existing).

## Provenance
- Verdict: 0_Brain/reference/2026-10-29_gate9-tier1/verdict.md (claude-opus-5-5; Spark shadow first). Pins unchanged at start and end.
- The ruling is Wednesday's, made under the 2026-10-27 design-inside-a-ruling grant: the PR C ruling of 16:5x was Wednesday's, not Kam's. Keeping the published contract unchanged adds no signature-class element.
