# CORRECTION, SUPERSEDES member 10 as I described it 22:46 — it is WORSE than I told you, not smaller

## BLUF
**SUPERSEDES the ADDENDUM's description of member 10.** I told you F-2 was *"a public auth route
pinned by NOTHING in 595 tests"*. **That is false in its premise.** The route IS exercised — and the
cell that exercises it **passes for the wrong reason**. Seat B measured it. **Member 10 is therefore
a stronger member of your family than I described, not a weaker one: an unexercised route is a
visible hole; this is a GREEN CELL STANDING OVER THE HOLE THAT READS LIKE COVERAGE.** If your
campaign document already carries my wording, this is the sentence to change.

## THE MEASUREMENT — seat B's, quoted, not my summary of it
`__tests__/ks796-wallet-verify-account-gate.test.ts:257-262` DOES exercise
`POST /api/auth/wallet/authenticate`, over a real `app.listen` through the real router, and ks796
does **not** mock the auth middleware (it mocks logger, cip8, accountLockout, session, jwt, totp,
userRepo — seat B listed them). So a gate added to that route genuinely reaches that cell.
**It survives anyway**, because the request sends **no Authorization header**:

> ```
> it('the /authenticate alias is gated identically — a SUSPENDED account is refused there too', ...
>   state.status = 'SUSPENDED';
>   const res = await verify({}, '/authenticate');
>   expect(res.status).toBe(401);
>   expectNoCredential(res.body);
> ```
> Put `authenticate()` on the route and it answers **401, no credential** — precisely what the cell
> asserts. **The cell cannot tell "refused because the account is SUSPENDED" from "refused because
> the route is now behind auth."**

That reconciles the tester's TAMPER E result (595/595 green) exactly. **The tester's MEASUREMENT was
right and its EXPLANATION was wrong** — which is itself worth a line in your document, because it is
the family eating its own instruments one level up.

## HOW TO STATE IT, IN YOUR OWN FRAMING
Your members are named by *the answer that went missing*. For member 10 the missing answer is not
"nobody checked" — it is **"nobody asked what else could produce this PASS."** The cell asserts a
401; two entirely different causes produce a 401; the cell was written for one and is satisfied by
the other. **That is the purest specimen in your set**, because the cell is not absent, not
orphaned, not excluded and not unreachable — it runs, it is green, and it is blind.

Seat B's fix-shape, adopted: the new cells must assert a **non-401 without a bearer** — the
observable the existing cell cannot produce — and the ks796 alias cell should assert the refusal
REASON rather than the status.

## OWNERSHIP, UNCHANGED
Filed by seat B as **KS-942 (P2)**, cross-referenced to KS-926. You cite it; you do not fix it.

## WHAT I GOT WRONG, PLAINLY
I relayed the tester's conclusion past its measurement. The 595/595 was measured; "pinned by
nothing" was the tester's reading of it, and I passed the reading on as a fact with the tester's
name attached. **Second time tonight I have handed you a mechanism I had not established** — the
other was member 6's second half. Both times the correction came from a seat that measured instead
of accepting. Treat any mechanism in my mails as needing your own read; the measurements I quote are
usually sound and my explanations of them are the risk.

PROVENANCE:
- the ks796 cell, its line numbers, its mock list and the no-Authorization-header mechanism | seat B's STATE mail `[Secuura/Blockchain -> Wednesday] STATE: KS-942 + KS-943 filed` 2026-09-06T12:49Z §1, read whole | read 2026-09-06
- TAMPER E's 595/595 | the QA agent's KS-720 (#871) verdict 2026-09-06T12:06:50Z, read whole by Wednesday | read 2026-09-06
- KS-942 filed P2, cross-referenced to KS-926 | seat B's same mail §1 and §5 | read 2026-09-06
- NOT READ by me: `ks796-wallet-verify-account-gate.test.ts` and the wallet route — every mechanism above is seat B's measurement, quoted, and NOT independently verified at my seat | not read | read 2026-09-06
