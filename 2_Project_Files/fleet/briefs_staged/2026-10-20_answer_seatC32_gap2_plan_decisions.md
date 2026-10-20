## BLUF
Your gap 2 PLAN is accepted on all three decisions, with one condition on timing. Start the build only AFTER #1654 is merged to develop (I mail you when it is). The demo and kintsugi counts are a prerequisite for MERGING your gap-2 PR, not for building and red-proving it; I commission the counts, not you.

## Answers to your three decisions
1. **Admin predicate: YES.** Use `isPlatformRole` for the owner-less arm only, leave the owned arm's `isAdmin` untouched, and file the `documents.ts:1076` literal-set inconsistency as its own ticket with the facts (the same SUPER_ADMIN omission as your N2). Name the exported predicate, never a copied literal set.
2. **Recipients: EXCLUDED from the owner-less arm.** Wednesday's reading of Kam's option (b) words ("only the connector that created a record, plus platform administrators ... no person in the tenant can") is that a recipient is a person and is not admitted. This is a reading of his words, not a ruling he gave on recipients, so state it in the PR body's Known residue as "Wednesday's reading, Kam can correct" and say what a recipient of an owner-less record loses.
3. **Empty caller id never matches: YES.** Pin it with a cell like R13, plus a cell for an empty `owner.id` with an empty caller id, as you proposed.
Your other plan points stand: files are `routes/documents.ts` (the owner-less arm) and one new test file; NOT `documentRepo.ts`; the creating-connector check names the exported `CONNECTOR_CREATE_ACTION` constant, never the string `'create'`; the mutants you list, including the literal-set one.

## The counts
- Why not you: your HOLDS forbid the box, and that stands. No seat now live has box rights either (D 26th's mails say no box, no az, no Docker).
- Wednesday's plan, to be confirmed by the seat that takes it: one read-only SELECT per box (demo, kintsugi) in the form you quoted, with the documents total as the in-statement control, run by a deploy-capable seat under the October grant. Wednesday commissions it after #1654 and the gate load clear; I will tell you when the numbers exist. The gap-2 PR does not get a GO until they are read.
- Until then, build and red-prove over the router from your own fixtures once #1654 has landed, as you said.

## Provenance
- Your QUESTION `gap 2 PLAN (option b)`, read whole at 15:1x; Kam's ruling on card `secuura-ks1695-ownerless-records-who-reads-1020` (b, recorded 15:02). I did not re-read `documents.ts:1076/:1124/:1130` or `tokenCrypto`/`provenance.ts`; those lines are your reads, not Wednesday's.
- #1654 state: gate CN1 (Opus, tier 1, last round) is running on head c52ab20328fa; a third NO GO would go to Kam.

## Meanwhile
Idle on gap 2 until my "1654 merged" mail. If you want something else in the gap, send a STATUS naming it; otherwise wrap your pane after #1667's KS-1695 comment is up.
