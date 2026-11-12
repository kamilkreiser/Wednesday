# Gate 340, TIER 2 (Sonnet; routing v1.0: tier-2 gates run on Sonnet: log-meta hygiene in services/auth, no auth decision). Seat R 112th's KS-2174 part 1 = PR 2216. Commissioned 2026-11-12 ~21:2x AEDT by the 20:2x Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate339-tier2-pr2215/commission.md` and gate 336's (`2026-11-12_gate336-tier2-pr2213/commission.md`, the log-hygiene precedent). Read both, and gate 333's verdict.md for the tier-2 output shape and Constraints.

Pins (Wednesday's git ls-remote at 21:20:36 AEDT; RE-READ at start and end): develop 13e62febfba85b867831a42a95cb8bcb558084d2; refs/pull/2216/head b12dd042761ddd67d86716bc7142d3ebd05e89b7 (ONE commit, parent eab5ac6bff8d; develop has since moved by PR 2213's squash, governance-only, which the seat says touches none of its paths); PR 2201 head 50c32501e60c (owns routes/users.ts:678, the ninth site; not this PR).

READY (read whole; reproduce, do not trust): `ready_r112_ks2174_mail.txt` in THIS folder.

What the row claims (unverified by Wednesday): routes/auth.ts:291 logs `maskEmail(user.email)` (url unchanged); repositories/userRepo.ts 1753, 1796, 1842, 1865, 1867 log `userId: account.id` instead of `email: account.email`; two new cell files (seeder 6 cells, route 3 cells), 7 RED at develop's product, 9/9 green with the change; whole auth suite 1,859/1,859; planted controls; a fragment pair. Deliberately NOT in this PR (Wednesday's STAMP 2, KS-2174 part 2): userRepo.ts 1764 and 1773 and any ks949 edit.

Questions:
1. Scope: exactly 6 files; the diff changes ONLY logger meta (and comments) in the two product files — no auth decision, token, credential, DB write, export or response change. Grep every hunk.
2. Correctness: do the six named sites now carry no raw address in ANY meta value (including nested objects and the `error` value at 1753/1867 — can an error message itself carry the address)? Is `maskEmail` the file's own helper and does it really mask (read its body)? Is `account.id` defined at every seeder site?
3. Tests: reproduce red-first (product reverted -> the 7 cells red) and green; are the cells able to fail independently (planted control); does the route cell genuinely reach line 291's branch (`!emailSent && NODE_ENV !== 'production'`)? Whole services/auth suite at head via `npm --prefix` (G339-2215-4), load1 < 8; state Node.
4. Census: no open PR on the 6 paths (a positive control); confirm PR 2216 merges cleanly onto develop 13e62febfba8 (merge-tree in your clone) and that the develop move touches none of its paths.
5. Completeness claim: the seat says the only unmasked sites left are 1764, 1773 (part 2) and routes/users.ts:678 (PR 2201's). Re-run a scan of services/auth/src at head for raw email in logger meta, with the known sites as a positive control; state the frame (logger calls only; errorHandler/request logs NOT examined).
6. Body: tier-2 statement first, Refs KS-2174 only, no close word; part-2 carve-out stated; fragment pair present.

OUTPUT: `verdict.md` here. First line: 'PR 2216: GO / GO WITH NOTES / NO GO (at head b12dd042761d; tier 2; round 1)'. Findings G340-2216-N graded. NOT TESTED section. Constraints exactly gate 333's (read-only on the project; clone into scratch/ here; no push, comment, ticket write, merge or mail; never `cd`).
