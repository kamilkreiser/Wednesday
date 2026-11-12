# Gate 338, TIER 1 (Opus; routing v1.0 tier-1 row: SECURITY DESIGN — an authorization/IDOR fix on the kyc routes). Seat A 29th's KS-2166 = PR 2214. Commissioned 2026-11-12 by the 18:23 Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate334-tier1-pr2211/commission.md` (read it and gate 334's verdict for the output shape, controls, mutant discipline and Constraints).

Pins (Wednesday's ls-remote just before this commission; RE-READ at start and end): develop fa2d60ca8ceec35299bf934c9c8d2bf74a330c8d; refs/pull/2214/head eb7315988de5c63cd6f9a1d96a89cb131b2643be (two commits on fa2d60ca8cee: the fix fe1587f57b99, then the ks1931 principal repair).

READY (read whole; reproduce, do not trust): `ready_a29_ks2166_mail.txt` in THIS folder. The design ruled by Wednesday (A 29th's plan ANSWER, briefs_staged/2026-11-12_A29_answer_plan.md): owner check on all four kyc routes (GET /api/kyc/:id after lookup, GET /user/:userId, DELETE /user/:userId/data, POST /initiate on the BODY userId); platform roles (isPlatformRole: SYSTEM_ADMIN, SUPER_ADMIN) admitted on the two READ routes only; DELETE and INITIATE owner-only; 403 FORBIDDEN "Forbidden"; ASCII-only fold of the ids; req.user.userId the only identity.

Questions:
1. Correctness, adversarially: for each route, try to reach another user's data as a non-owner: role spellings (ADMIN, ORG_ADMIN, ISSUER_ADMIN, connector, array roles, lowercase system_admin), id case variants, Unicode lookalikes (Kelvin sign, fullwidth), %2F, trailing slash, missing/empty/non-string userId claim, an RS256 token without userId, a REFRESH token used as a bearer (A 29th flagged verifyJwtRs256 checks signature + alg only: measure whether kyc's authenticate() admits a refresh token; if yes, grade it and say whether it is in scope). Say which reach the handler and what they get.
2. Order: zero DB statements on a refused list/DELETE/initiate; a refused initiate writes neither verification nor consent rows; the DELETE check precedes any delete (mutant M11 class).
3. Reproduce A 29th's figures: red-first 61/83 at develop's index.ts, 83/83 at head, whole kyc suite 177/177, 18/18 mutants killed; add your own mutants (exception widened to DELETE; isPlatformOrOrgAdminRole swap; fold to toLowerCase; compare on the claim's sub).
4. The ks1931 repair: did it change any assertion (count `expect(`)? Do ks1931 R1/R2 now fail when 2211's fix is reverted (non-vacuous)?
5. Behaviour change for callers: a non-subject non-platform caller now gets 403 where it got 200/201. Enumerate in-repo callers (frontends, services, connectors) with a control; say whether any legitimate flow breaks.
6. PR body: tier-1 statement, the 403-after-lookup existence-oracle trade-off named, Refs only, the candidates (refresh-token bearer, upper-case initiate id) listed as not-in-scope.

OUTPUT: `verdict.md` here. First line: 'PR 2214: GO / GO WITH NOTES / NO GO (at head eb7315988de5; tier 1; round 1)'. Findings G338-2214-N graded. NOT TESTED. Constraints exactly gate 334's (read-only on the project; clone into scratch/ here; no push, comment, ticket write, merge or mail; never `cd`).
