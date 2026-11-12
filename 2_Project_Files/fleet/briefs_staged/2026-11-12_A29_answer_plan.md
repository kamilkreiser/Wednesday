Seat A 29th

ANSWER to your plan confirmation (07:35:51Z). Your plan is CONFIRMED as written, with the rulings below. Start the build.

RULINGS (Wednesday; security-design row, your measurements read in your mail, not re-derived by Wednesday):
1. D1 identity: req.user.userId as a string, nothing else; a token without userId is refused; `sub` and x-user-* rejected. As proposed.
2. D2 owner rule: ONE helper callerMayActOn(req, subjectId, platformMayRead) beside foldedUserId; subject per route as you listed (path :userId on list and DELETE, the BODY userId on initiate with a mismatch refused and the contract unchanged, verification.userId after the lookup on GET /:id). The ASCII-only fold (A-Z lowered, nothing else) is APPROVED, for your stated reason (a strict compare fails closed on a real owner; toLowerCase widens the admit side, U+212A).
3. D3 exception: isPlatformRole (SYSTEM_ADMIN, SUPER_ADMIN) admitted on the two READ routes only; DELETE and INITIATE are OWNER-ONLY. No admin exception on DELETE, so no Kam card. NOT isPlatformOrOrgAdminRole (the tables carry no tenant/org column).
4. D4 shape and order: 403 { success:false, error:{ code:'FORBIDDEN', message:'Forbidden' } } on all four, in the orders you gave. GET /:id answers 403 after the lookup (not 404): the spec declares 403 there, the review precedent answers 403, and the id is a service-minted v4 UUID. Name the existence-oracle trade-off in one line of the PR body.
5. D5: kycRateLimit stays first on INITIATE, unchanged. D6: no try/catch added; KS-2185 untouched.
6. PR 2211 SEQUENCING: as proposed. 2211 is first in the next merge seat's queue. Measure at READY on a real merge-tree with your overlap control. If 2211 has merged, your PR carries the ks1931 principal repair (its 4 cells named). If not, the repair is 2211's merge-time follow-up with the exact lines in your READY. Never edit 2211's files while it is unmerged.
7. Existing-cell repairs (ks849, ks1868): as proposed. Every repaired cell is named, and the counted `expect(` diff reads 0.
8. Your throwaway BEFORE cells (copied in for one run, moved out, porcelain 0) are ACCEPTED under HOLDS 1: a measurement that leaves the tree clean is not an edit.
9. OUTSIDE CONSUMERS: UNKNOWN to Wednesday. Wednesday holds no inventory of out-of-repo clients, and your in-repo census (25 hits, no service or frontend caller, control 1) is the only evidence. State the 200 -> 403 behaviour change for a non-subject caller plainly in the PR body and the READY, so the gate and the next Kintsugi deploy notice carry it.
10. CANDIDATE FILINGS, NOT yours to file: (a) the shared verifyJwtRs256 may accept a REFRESH token as a bearer (UNMEASURED, your point 21); (b) initiate stores an upper-case body userId verbatim, so the owner's lower-case list never shows those rows (your point 8). List both in your READY under candidates; Wednesday routes them to the board seat.
11. Gate: G1 tier 1 Opus after your READY, as stamped. Your meter rules (stop-starting 55, wrap 60) stand.

Grant: Kam 2026-11-12 15:01:00 "please archive anything that is ready and continue with Secuura tickets.  Try to clear the board ASAP"; card secuura-wednesday-go-counts-as-kams-word-1030 = a. Not a signature class: a code change on a branch, gated before any merge; nothing deploys.
