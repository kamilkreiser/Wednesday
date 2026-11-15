PR 2238: GO WITH NOTES (at head 59f31402e77f8f9baaa9a5194570a49895ddd9c4; tier 1)

# Gate 362, tier 1, PR 2238 (KS-1897), Secuura/Distributed_Secuura. Findings only.

Gate run 2026-11-15 08:20Z to 08:28Z (19:20 to 19:28 AEDT), Opus. Head re-pinned by `gh api .../pulls/2238` at the start AND at 08:27:37Z: `59f31402e77f8f9baaa9a5194570a49895ddd9c4`, open, not merged, one commit on `9bb6c98b2c47`. PR 2235 head `19b6f52483c6` (open, not merged) at both reads.
**develop MOVED during the gate:** `dc42dc89493f` at the start, `918f5e6d312a` (KS-2196, anchoring plus its two fragments, 7 files, none in billing) at 08:27Z. Both measured below.

Read whole first: commission.md, ready_batch.txt (READY 08:17), the stamped brief `2026-11-15_seatA32_ks1897_build.md` (design 1-7, cells M1-M12, residuals 6a-6g), and the ruling in it.

## Answers

**Q1. Does the code do exactly the ruling? YES.**
- **The buyer comes from the token only.** `routes/billing.ts:471-477` `checkoutBuyerMetadata(req.user)` returns `{userId}` or `{userId, tenantId}`, non-empty strings only, or undefined. It is passed at `billing.ts:504` (bundle) and `:551` (custom). The body is parsed by `PurchaseBundleSchema` / `PurchaseCustomSchema` (`billing.ts:174-186`, zod object, unknown keys stripped). No body field reaches `metadata` or `customerId`. `req.user` is set only by `jwtAuthenticate()` (shared `middleware/index.ts:115/126`, RS256-verified), and `index.ts:153` mounts it on `/billing`.
- **Spread order.** The builders put `...params.metadata` last (`stripeService.ts` bundle and custom metadata blocks, unchanged). Because the helper can only emit `userId`/`tenantId`, it cannot override `bundleId`/`certifications`/`type`. Gate cell A1a sends a body with `userId`, `tenantId`, `metadata{certifications:9999}`, `certifications`, `stripeCustomerId` and `customerId`, plus a token carrying extra `certifications`/`bundleId`/`role:SUPER_ADMIN` claims. The builder receives exactly `{userId:U, tenantId:T1}`, `customerId` undefined, and the exact key set (both routes). A1b: a token userId of `42`, `{ $ne: null }`, `''` or null gives no metadata. A1c: a non-string tenantId gives `{userId}` alone.
- **Order:** paid `webhooks.ts:553`, then `certifications > 0` `:559`, then customer-or-match `:563` (`checkoutCustomer`, `:497-527`), then `grantCreditsOnce` `:569`. Unpaid and certs=0 make no lookup and no claim (the PR's M7/M7b, plus my W-sample).
- **Owner filter:** `checkoutBuyer.ts:48-53`. Customer `metadata.userId` must equal the buyer's and be non-empty (`:50`). A recorded non-empty customer tenantId must equal the session's (`:52`). There is NO platform pass, and `recordedBuyer` (`:32-37`) refuses an empty or non-string userId.
- **Exactly one:** `webhooks.ts:520` `owned.length === 1`. Zero (`:521-522`) and several (`:524`) log `sessionId` + `reason` (+ `count`) only and return null before `grantCreditsOnce`, so no grant row is claimed. Neither customer nor email gives PR 2232's exact line (`:511`). No buyer recorded: no lookup at all (`:514-518`).

**Q2. ATTACK: no route found to be credited for another's payment, or to credit another person.** I wrote 17 cells (`scratch/cells/g362-attacks.test.ts`, built on the PR's harness plus ks1934's replay SQL and an RS256 admin token, with a case-insensitive switch on the list double). All 17 pass at head (`out-attacks-head.json`).
- A2/A2b: the squatter's customer under the victim's email, with the squatter's userId (with or without the victim's tenant), is never credited, and no email or customer id is logged.
- A3: the squatter pays his own session prefilled with the victim's email. The victim's customer is not credited, and the squatter is not credited either.
- A4/A4b/A4c: tenant T2 beside T1 credits exactly T1. A recorded tenantId `''` counts as tenant-less, as `mayActOnCustomer` does. A blank buyer gives no lookup.
- A5a: an exact-match list with an upper-case session email: the email goes through verbatim, nothing matches, nothing is credited (fails closed). A5b/A5c: a case- and whitespace-insensitive list returning a squatter is still refused, and the buyer's own customer is credited once.
- A6: a session with customer AND email credits `session.customer` and makes no lookup (pre-existing behaviour; see G362-2).
- A7/A7b: completed then async (the buyer gained a 2nd customer in between), and async then completed: ONE credit, the first customer.
- A8: no match, then the buyer's customer appears, then admin `POST /webhooks/replay`: the first replay gives creditsAdded 5, the second 0, one credit. A8b: a replay of a squatted session credits nobody.

**Red-proof.** The as-worded mutant (owner filter AND recorded-buyer check removed: email alone) fails 17 cells against the whole billing suite plus my file (437 tests). 9 of them are the PR's (M2, M2b, M4, M5, M5b, M6, M6b, M6c, M9, equal to the builder's 9) and 8 are mine (A2, A3, A4, A4c, A5b, A5c, A8, A8b). For example, A2 gives `expected [ { customerId: 'cus_x_squat', … } ] to deeply equal []`. At develop `dc42dc89493f` my file is 10 failed / 7 passed. The 7 that pass on develop are "nothing credited" controls, because develop credits no email-only session at all.

**Q3. Suite, counted by the gate (Node v26.8.1, vitest from the lock, `npm ci --ignore-scripts` plus the shared build in a sparse scratch worktree, interleaved):**
| tree | run 1 | run 2 |
|---|---|---|
| develop `dc42dc89493f` | 395 / 21 files, 0 failed | 395 / 21, 0 failed |
| head `59f31402e77f` | 420 / 22, 0 failed | 420 / 22, 0 failed |
| merge develop `dc42dc` + head (local `2c0832fb158c`, tree `c8f3e48d601b` = builder's) | 420 / 22, 0 failed | 420 / 22, 0 failed |
| merge develop `918f5e6d312a` + head (local `d6a2927c4a56`, tree `2ecd2610d2e7`) | 420 / 22, 0 failed | (once) |

The builder's 395/21 and 420/22 are confirmed. merge-tree against `918f5e`, both orders: rc 0, same tree. The billing subtree (`a2004ee3491e`), packages/shared and package-lock are identical in the head tree and both merge trees.

**Mutants.** I drew a random 3 of the builder's 17 non-as-worded mutants (seed 305544): W8, W10 and W9. I re-planted each myself in webhooks.ts, ran it against the whole suite plus my cells, and restored it with sha256 checked (`3d5010e2b5eb…`):
- W8 (PR 2232 line changed): KILLED, 2 cells (M8, ks1934 C2d).
- W9 (lookup fails open): KILLED, 1 cell (M12 `expected 200 to be 500`).
- W10 (session customer ignored): KILLED, 33 cells (ks1868/ks1933/ks1934/ks488/M10/A6).
- As-worded: KILLED, 17 cells.
No survivor. tsc `--noEmit` on billing at head: rc 0. eslint `--max-warnings 0` on the 4 changed TS files: rc 0.

**Q4. ks1934: the file is unchanged** (diff `9bb6c98b2c47..59f31402` on `*ks1934*` is 0 lines). It has **18** cells, and all 18 pass at develop, head, both merges and the 2235 three-way merge. C2d is kept: `webhooks.ts:510-512` keeps the exact line, and mutant W8 turns C2d red.

**Q5. PR body and fragments: honest, with one wrong number** (G362-1). The Test Evidence block names what was NOT run: the four platform suites (Schemathesis, Akto, Playwright, k6), real Stripe, a live webhook, real Postgres, a booted service, Node 24. It gives the push hook's final line, "PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED", and says legs 3, 4 and 8 were SKIPPED (stack not up), "not a pass". It has no closing keyword and no self-hold sentence. It says plainly that the as-worded mutant is a test-only plant. Its 18-mutant list matches the builder's `mut/` evidence (18 files plus summary). Residuals 1-7 = brief 6a-6g.

**Q6. PR 2235 overlap.** merge-tree of 2238 with 2235 `19b6f52483c6`, both orders: rc 0, the same tree `dcee176b9084` (= builder's). Three-way (develop `dc42dc` + 2238, then + 2235, both orders): rc 0, the same tree `fba4659fa68f`. On the local commit `954771ce83b6`, billing ran 443 tests in 24 files, all passing (460 with my 17 attack cells, 25 files, 0 failed); 443 matches the builder.
Semantic interaction: none that changes who is credited. The customer is decided (`webhooks.ts:563`) BEFORE `grantCreditsOnce`. 2235's `withCustomerCreditLock` wraps only `addCertificationCredits` (`stripeService.ts:232/253` in the merged tree), keyed on the already-chosen customer. A `CreditLockUnavailableError` takes the existing failed-claim path (500, redelivery), and the redelivery re-runs the match, which is residual 3. This was measured by merge-tree and the suite only, not by a live lock.

## Findings
- **G362-1 Low.** PR body ("The `ks1934` file is unedited and its 12 cells stay green", Test Evidence, billing-suite bullet) and the READY say **12** cells; the file has **18**, all green (measured: `out-suite-dev1.json`/`head1.json`). The brief's "11 other cells" was also wrong. A claim the measurement does not back; the substance (unedited, all green) holds. Fix the number in the body.
- **G362-2 Info.** `webhooks.ts:505-506`: a session WITH `customer` is credited to that customer with no owner check (cell A6). It is pre-existing and unchanged, and the brief kept it so. Today it is unreachable from a caller: the routes take `customerId` only from `req.user.stripeCustomerId` (`billing.ts:495/541`), which no token minter sets, and A1a proves a body `stripeCustomerId`/`customerId` is stripped. It is worth one line in KS-1897's follow-ups: if anything ever starts setting `stripeCustomerId` on the token, the b-ii owner rule does not cover that path.
- **G362-3 Info.** This is residual 2 restated as an attack. A signed-in caller can create a session (recording himself) prefilled with a victim's email and get the victim to pay it. The caller's own customer is credited. This is inherent to "whoever pays credits the creator", and the PR states it. Nothing more was found.
- **G362-4 Info.** The email goes to `listCustomersByEmail` verbatim (`webhooks.ts:509/519`), with no trim or lower-casing (per the brief). Against exact-match Stripe a case variant credits nothing and fails closed (A5a). Against a case-insensitive Stripe the owner filter still holds (A5b/A5c). Real Stripe semantics are unmeasured.
- **G362-5 Info.** Every gate run, like the builder's, is on Node v26.8.1, which is not the LTS line (the project rule names Node 24). The PR and fragments disclose this.

## Method and artefacts (all under scratch/)
- `repo/` is a blob:none HTTPS clone, push URL `DISABLED`, using the project's gh credential helper per command. `wt/` is a sparse worktree (Blockchain/Dev + Projects Documents); the local refs `g362-merge`, `g362-merge918` and `g362-m3` are never pushed.
- Outputs: `out-suite-{dev,head,merge}{1,2}.json`, `out-suite-merge918.json`, `out-suite-m3.json`, `out-attacks-{head,dev}.json`, `out-mut-*.json`, `out-mutants.json`, `out-tsc-head.log`, `out-eslint.log`, `pr_body.md`.
- Cells and the mutant runner: `cells/g362-attacks.test.ts` (generated by `cells/build.py` from the PR harness + `cells/cells.ts.part`) and `cells/mutants.py`.
- Nothing was written under `!CODING` (the builder's evidence and the CLAUDE.md were read only). There was no Stripe call and no network beyond GitHub reads (the npm registry for `npm ci` excepted).

## NOT TESTED
- `node Blockchain/Dev/scripts/docs-fragments.mjs check` on the fragment pair: REFUSED in my sparse worktree (`systemTest/__tests__/support/html_docs_check.mjs` not checked out; adding it to the sparse set failed rc 128). The fragments were read by eye only.
- Any real Stripe call: `customers.list` email semantics (case, whitespace, the 100 cut-off), real webhook signatures, real Checkout Session payloads.
- A live webhook delivery, a booted billing service, a real PostgreSQL (grant ledger, webhook_events), 2235's advisory lock under a real DB.
- The four platform suites (Schemathesis, Akto, Playwright, k6), and preflight legs 3, 4 and 8.
- Node 24 (LTS). Every run was on v26.8.1.
- `tsc` with the tests in the program, and `check:test-types`. Only `tsc --noEmit -p` on the service ran.
- The builder's other 14 mutants (only W8, W9, W10 and the as-worded one were re-planted), and the builder's planted eslint and docs controls.
- The billing suite on the `918f5e` merge was run once, not interleaved twice (its billing subtree is byte-identical to the twice-run `dc42dc` merge).
- Whether the real auth service signs `tenantId` under that name for every billing caller (read from JwtPayload and the existing code only).
