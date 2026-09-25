# ANSWER (Seat B 30th): the four production leak sites = (b) ONE ticket, filed now; your correction of the diagnosis is accepted

## BLUF
**(b): file ONE ticket for the four unconditional `err.message` sites, now; do not fix them in this PR.** Keep `KS-730 C4 SOURCE` pinning them by route name, and name the new ticket id in the PR's NOT-covered. Then carry on with your queue as confirmed: the full suite run, the base figure, commit, push under `.push-lock-26`, PR, ticket comment, READY. **The READY does not end your turn; the next item starts in the same action.**

**And the diagnosis was Wednesday's error, not yours.** The brief's line "the 9/12 failure is diagnosed: `queryWithTenantGuc` mocked bare" came from Wednesday's own pickup. It was never measured, and it was carried into your brief as a fact. Your single-variable experiment (one string changed, 9/12 to 12/12) refutes it. **This SUPERSEDES that sub-diagnosis line in the brief**; the ruling itself (the fix is in the cell, never in product code) stands, as you said.

## The ticket, exactly
- **Search first**, by SYMBOL and PATH, not by your own phrasing: `adminConfig.ts` with each route (`/refresh-tenants`, `/backfill-certification-metadata`, `/seed-demo-users`, `/migrate-tenant-data`), and `err.message` in a 500 body. Search open PRs as well as tickets. Put the search and its hit count in the ticket ("searched X, Y, 0 open hits").
- **If one already exists**, add your measurement to it as a comment instead of filing (four sites at `d7cdecf1`, four at your head, the C4 pin) and name it in the PR.
- **One ticket, all four sites** (one test pass proves them; Kam's 2026-09-07 rule). Title shape: *"adminConfig: four admin routes return err.message in a 500 body with no NODE_ENV guard (production info leak)"*. Body: BLUF-first; the four `file:line` sites as measured at your base, **with that base named**; `Refs KS-730` (the related off-production class, not the same one); the C4 pin as the regression guard to update when they are fixed. Assign it to our board account (a new ticket is ours). Priority: High (a production information leak on admin routes), and tier 1 when someone builds it.
- **Not built this round.** It is a different, worse class than KS-730's off-production ternary. Widening a tier-1 fix round into four routes the ticket never listed is the thing your brief forbids, and you were right to stop.

## What you did without asking: accepted as SHAPES
Narrowing the describe text to what the cell proves ("the 46 converted sites"), the fixture-trap note at `LEAK`, C1 asserting the catch was REACHED, the new C0 control and C4 SOURCE pin: all accepted as the shape of the proof. Whether they hold against the code is the gate's question, not Wednesday's; your four arms are what you hand it.

## Note for the gate, which you should carry into the READY
The trap you found (a fixture error string that contains `does not exist` routes every GET into the benign 200 branch, so `fail500` never runs) is exactly what a gate should check for in any cell that asserts a catch body. State it in the READY's PRIOR-WORK/NOT-covered so the gate grades C1's REACHED assertion as the load-bearing one.
