PR 2232: GO WITH NOTES (at head 84eea21e360af4ed04fbad0125ef5a0efadcad46; tier 1)

Gate 354 (tier 1, Opus), RE-COMMISSION, 2026-11-15 17:31 to 17:42 AEDT. The first gate agent died at 17:31 AEDT before it wrote a verdict. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Reuse of the dead agent's work.**
- **Its clone.** I reused `scratch/clone` only after this check: re-fetched, `origin/develop` = ce35818d50ae and `origin/pr2232` = 84eea21e360a, equal to my `gh api` pin. Push URL `DISABLED`; alternates are read-only to the Blockchain object store.
- **What it left behind.** `wt-head` was NOT clean. It held a live plant (`async_payment_failed` renamed `_x` in `webhooks.ts`) and its probe file inside the tree. I restored `webhooks.ts` with `git checkout HEAD --` (blob read back 8e641e04c1cf = the head's blob). I moved the probe file out to `scratch/probe/orphan-from-dead-agent.test.ts`. Both worktrees were then at porcelain 0.
- **Its installs and logs.** I did NOT trust its `npm ci` or shared builds. I re-ran both in both trees (`scratch/r-setup.sh`, rc 0 ×4).
- **What this verdict cites.** Every figure comes from my own `r-*` outputs. The old `out-*` logs are not cited.
- **Probe file.** I read the dead agent's probe cells (`scratch/probe/cells.ts.part`) whole, adopted them as my instrument, and added G12 (`scratch/probe/r-cells.ts.part`). I re-ran all of them myself.

**Pins.**
- `gh api` at 17:33:05 (`scratch/pin2.out`) and again at 17:41:35 AEDT (`scratch/pin3.out`):
  - develop ce35818d50aebe7f41fc41f677ee03079c36d7ad
  - PR 2232 head 84eea21e360af4ed04fbad0125ef5a0efadcad46 (open, not merged)
- Neither moved during the gate. `git ls-remote` with the deploy key at 17:33 (`scratch/r-fetch.log` run) agreed. A second `ls-remote` without the key at 17:41 was refused (publickey): that was my invocation, and `gh api` is the pin of record.
- The PR is ONE commit on 4e4347818772. develop has moved one commit since then (ce35818d50ae, KS-2144: one shared test file only).
- **Merge-tree on the develop I read** (`scratch/r-mt.sh` → `scratch/r-mt.txt`): `merge-tree --write-tree` gives tree bbe3de71ea6b in both orders, rc 0. In the merge:
  - the billing tree is d489f92d61b8, identical to the head's;
  - `webhooks.ts` is 8e641e04c1cf, identical to the head's (develop's is c7413974423e, identical at 4e4347818772);
  - the merge differs from the head by 1 path (the KS-2144 shared test) and from develop by exactly the PR's 4 paths;
  - `package-lock.json` is identical at develop and head (e0f4edae4cce).
- So the billing service measured at the head IS the billing service of the merge.

## FOUND

**G354-2232-1 (Low; test gap, not a product defect).**
- **The gap.** No PR cell sends `checkout.session.async_payment_succeeded` with a NON-paid `payment_status`.
- **Measured.** My plant `check_completed_only` makes the paid check apply to `checkout.session.completed` only, so an async success credits whatever its status. It survives all 18 PR cells and all 16 ks1933 cells. Only my G1 kills it (`scratch/r-plant-check_completed_only.json`).
- **The code is right at source.** Both session events share one handler, and the check sits on the session, not the event type (`webhooks.ts:378-379`, `:513`).
- **Action for the builder or board:** a cell "async_payment_succeeded with payment_status unpaid: 0 grants, 0 claims".

**G354-2232-2 (Info; pre-existing KS-1933 key residual, now also reachable through the new event).**
- **What it is.** `checkoutPaymentKey` (`creditGrants.ts`, not in the diff) falls back to `cs:<session id>` when a session carries no `payment_intent`. `payment_intent.succeeded` keys `pi:<id>`.
- **Measured.** My OBSERVE cell G9: an `async_payment_succeeded` session with `payment_intent: null`, followed by `payment_intent.succeeded` for the same purchase, gives **2 grants** at the head ("expected 2 to be 1"). This is the head baseline's only failure (`scratch/r-plant-none.json`).
- **Not new to this PR.** It is the same fallback that `checkout.session.completed` 'paid' already had before this PR (read at source).
- **Reachability: UNMEASURED.** Billing creates `mode: 'payment'` sessions only (`stripeService.ts:307`, `:362`), and for those Stripe sets `payment_intent`. No real Stripe was called.
- **Grade:** latent. It belongs to KS-1933's residual list, not to this PR.

**G354-2232-3 (Info; three unpinned bookkeeping lines).**
- **The lines.** The `async_payment_failed` case sets `result.customerId`, `amount` and `currency` (`webhooks.ts:394-396`). These are the audit columns `finaliseEvent` writes to `webhook_events`.
- **Measured.** My plant `failed_no_result` drops all three and survives every cell. The harness's `db` model ignores the finalise parameters.
- No money effect. Recorded so the next harness can pin it.

**G354-2232-4 (Info; a figure in the READY differs from mine, same conclusion).**
- **The difference.** The seat's "paid check moved after `grantCreditsOnce`" fails 8 cells. My `check_after_grant` plant fails **7 PR cells**: C1, C7, C9, C3, C4c, C5 and C6. It also fails G1, G4, G7, G8 and G10.
- **Why.** In my placement C1b stays green, because the not-paid log line still fires after the grant. The seat's plant evidently sat elsewhere.
- Either way the mutant is killed, by many cells.

**G354-2232-5 (Info; the flow fragment is slightly wider than the code).**
- **The sentence.** The flow fragment says that without the async subscriptions "a delayed purchase is still credited once by `payment_intent.succeeded`".
- **When that holds.** Only for a session with a customer. Today's two checkout routes never set one (KS-1897), so in practice neither path credits such a purchase. The PR body's "Interaction with KS-1897" section says this correctly; the fragment omits it.

**G354-2232-6 (Info; tool coverage).** `npm run check:test-types` covers auth, api-gateway, vc-issuer, security and m365-integration only. "billing" appears 0 times in the root `package.json` script; the control "services/auth" appears 3 times. So the READY's "check:test-types rc 0" says nothing about billing's tests. My own tests-in-program tsc (below) covers that.

**G354-2232-7 (routing note for KS-1897; Kam's 17:09 ruling (b), "credit email-only checkouts by matching the email").** PR 2232 does NOT conflict with that ruling, and does not make it harder. What the KS-1897 builder must know:
- **(a) No new early return.** The hard early return on a missing customer (`if (!customerId) { logger.error('No customer ID in checkout session'); return 0; }`, `webhooks.ts:503-506`) is PRE-EXISTING and unchanged by this PR; the diff adds no new customer return. Because this PR routes `async_payment_succeeded` into the same `handleCheckoutComplete`, one email-match at that return covers both session events.
- **(b) Order.** Today the customer check runs BEFORE the paid check. My G12 proves it: an email-only unpaid session logs "No customer ID" and never reaches the not-paid line.
  - An email-match will be a Stripe lookup. It should go AFTER the paid check, so that an unpaid session costs no lookup and still claims no grant row.
  - Swapping the two checks is grant-neutral. My `check_before_customer` plant reddened NO PR cell and no ks1933 cell, only my order-observing G12. So KS-1897 can reorder freely, with no PR cell in the way.
- **(c) Cell C2d.** C2d ("a paid session with no customer: 0 grants") uses a fixture with neither `customer` nor `customer_email`. It should stay true under email-match. It also asserts the exact "No customer ID in checkout session" error line: if KS-1897 changes that message, C2d must be updated deliberately. That is not a regression.
- **(d) The backup cannot credit an email-only purchase.** `payment_intent.succeeded` needs `paymentIntent.customer` (`webhooks.ts:569`). So under ruling (b), an email-only DELAYED purchase can be credited ONLY through `checkout.session.async_payment_succeeded`, the case this PR adds.
  - That makes the live endpoint's subscription to that event (Kam's operational check, in the PR body) load-bearing for KS-1897.
  - There is no double-credit risk: a session credited under its `pi:` key blocks a later PI event; and a PI event with no customer credits nothing.
- **(e) The grant row.** It stores `customer_id` as passed. The email-matched id must be resolved before `grantCreditsOnce`, never after.

## TESTED

**Q1. 'paid' only, and the skip comes BEFORE `grantCreditsOnce`.**
- **At source** (`webhooks.ts` at the head):
  1. the customer return (`:503`);
  2. `if (session.payment_status !== 'paid') { log; return 0; }` (`:513-516`);
  3. then `grantCreditsOnce` (`:522`).

  The comparison is strict. G8: "PAID" and " paid" give 0 grants.
- **No grant row is claimed by an unpaid session.** These cells assert `grantClaims` = 0: C1, C5b, G1, G4, G6, G7 and G12.
- **Mutants that kill it:**
  - `no_check`: 8 PR cells plus 6 of mine;
  - `check_after_grant`: 7 PR cells plus 5 of mine;
  - `truthy_only`: 7 PR cells plus 6 of mine;
  - `unpaid_only`: C7, C9, G7 and G8.

**Q2. The async path and no double credit.**
- **The idempotency key, read at source.** Both session events call `grantCreditsOnce({ paymentKey: checkoutPaymentKey(session) ... })`. `checkoutPaymentKey` returns `pi:<payment_intent id>` (a string or an expanded object), else `cs:<session id>`. `handlePaymentSucceeded` uses `` `pi:${paymentIntent.id}` ``. `CLAIM_GRANT_SQL` is `INSERT ... ON CONFLICT (payment_key) DO UPDATE ... WHERE status = 'failed'`, so a row that is 'granting' or 'granted' blocks every second grant.
- **A delayed payment credits exactly once:**
  - C3, C3b, C4, C4b, C4c and C4d;
  - G2: every event plus an admin replay of each = 1 grant, one row `pi:pi_ks1934_1` 'granted';
  - G2b: reversed order = 1;
  - G3: async, PI and async delivered concurrently = 1;
  - G5: completed 'paid' then async = 1;
  - C6b: replay = 1.
- **A failed one never credits:**
  - C5 and C5b;
  - G4: completed 'unpaid', `async_payment_failed`, `payment_intent.payment_failed`, plus replays of all three = 0 grants, 0 claims.
- **Mutants that kill it:**
  - `async_cs_key` (async success keyed `cs:`): C3b, C4, C4b, G2, G2b, G3 and G5;
  - `failed_credits`: C5, C5b and G4;
  - `no_async_case`: C3, C3b, C4d and C6b;
  - `no_failed_case`: C5 and G10.
- The one residual is G354-2232-2 (no `payment_intent` on the session).

**Q3. `no_payment_required` and a missing customer credit nothing.**
- **The ruling.** As ruled: Q1 = a in Wednesday's 04:40Z plan ANSWER, as quoted by the PR body and the seat's HANDOVER, and the brief's trap (iii) DEFAULT.
- **`no_payment_required`:**
  - C7: 0 grants;
  - G7: with `payment_intent` null and `amount_total` 0, 0 grants and 0 claims;
  - C9: a missing status, 0 grants.
- **A missing customer:**
  - C2d: paid, no customer, 0 grants;
  - G6: no customer on the async success AND on the PI event AND on the async failure: all 200, 0 grants, 0 claims;
  - G12: email-only, 0.
- **Killed by:** `unpaid_only` (C7, C9) and `truthy_only` (C7).
- **Whether a zero-total session can occur at all.** `quantity` has `min(1)` (`billing.ts:182`); bundle and custom prices come from `unit_amount` and there is no coupon or discount in billing (grep: 0 for `allow_promotion_codes`, discounts or coupon; control: `unit_amount` 2). `calculatePricePerCert` itself was NOT read.

**Q4. No real Stripe call anywhere.**
- **The product diff adds no Stripe call.** The only `+` line naming stripe is a type cast (`as Stripe.Checkout.Session`). `addCertificationCredits` is still reached only through `grantCreditsOnce`.
- **The test file.**
  - It has exactly 1 `vi.mock('../services/stripeService')`, which replaces the whole service with an in-memory fake.
  - 0 hits for `new Stripe`, `sk_test`, `sk_live`, `api.stripe.com` and `STRIPE_SECRET`.
  - Its JWT key is generated per run.
- **Runtime.** G11 counts every outbound non-loopback `http`/`https.request` across a full delivery set: **0**. Its positive control G0 (a request to `api.stripe.com`) is counted and refused (passed).

**Red-proof and suites, reproduced by me** (`scratch/r-runs.sh`; Node v26.8.1, vitest 4.1.12, python3 3.14.10, so outside the 3.9.6 window).
- **The PR's test file on develop's product:** **11 failed / 7 passed**. The 11 are C1, C1b, C7, C9, C3, C3b, C4c, C4d, C5, C6 and C6b, every one an `AssertionError`. The 7 are the controls C2, C2b, C2c, C2d, C4, C4b and C5b. This equals the READY.
- **At the head:** 18/18.
- **Whole billing suite**, interleaved dev → head → dev → head:

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop ce35818d50ae | 20 files, 377/377, rc 0 | 20 files, 377/377, rc 0 |
| head (= the merge's billing tree) | 21 files, 395/395, rc 0 | 21 files, 395/395, rc 0 |

  377 + 18 = 395. Both equal the READY.

**My mutants, per changed line** (`scratch/r-plants.sh`, `scratch/r-plant.py`).
- **Instrument.** The ks1934 file, the ks1933 file and my 13 gate cells: 54 tests in all. `webhooks.ts` was restored after each plant with `git checkout HEAD --`, and `hash-object` read back 8e641e04c1cf every time. Worktree porcelain ended at 0.
- **Baseline at the head:** 1 failure, G9 (OBSERVE, G354-2232-2).

| Plant | Reds beyond baseline |
|---|---|
| `no_check` | 13 |
| `check_after_grant` | 11 |
| `truthy_only` | 12 |
| `unpaid_only` | 4 |
| `check_completed_only` | 1 (G1 only; finding -1) |
| `report_lie` (not-paid branch returns the count) | C6 |
| `log_customer` (customer id in the not-paid log) | C1b, G10 |
| `no_async_case` | 6 |
| `async_cs_key` | 7 |
| `failed_credits` | 4 |
| `no_failed_case` | C5, G10 |
| `check_before_customer` (order swap) | G12 only (grant-neutral, by design) |
| `failed_no_result` | **0, SURVIVED** (finding -3) |

  Every changed product line has at least one killing mutant, except the three audit lines in finding -3.

**Type checks** (`scratch/r-static.sh`, `scratch/tsc-tests/`, `r-tsc-tests-*.norm`).
- **tsc** `--noEmit -p services/billing/tsconfig.json`: rc 0 at both trees. A planted TS2322 in `webhooks.ts` gives rc 2, 1 error, then restored.
- **tsc with the tests in the program** (a scratch config outside the repo): 18 errors at develop and 18 at the head, identical sorted lists, all in older `__tests__` files. 0 are in ks1934 and 0 in `webhooks.ts`.
  - The positive control is that the config does reach `__tests__`: 18 of 18 errors are there.
  - Two earlier attempts of mine failed on type roots (TS2688). That was my config, and it is superseded.

**eslint** (`scratch/tools/r-eslint.mjs`, the ESLint API with `cwd` = the tree's `Blockchain/Dev`, so the root flat config's globs apply; `scratch/r-eslint.txt`):
- **At the head:** `webhooks.ts` and the ks1934 test give 0 errors and 0 warnings. At develop, `webhooks.ts` gives 0 and 0.
- **Planted control:** a `no-fallthrough` switch gives 1 error, rc 1, then restored.
- **A first attempt was the wrong instrument.** It used the CLI with `-c` from the wrong `cwd`: the globs did not match, so it reported a false "Parsing error" on the test file and missed the plant (`scratch/r-eslint-head.log`, `scratch/r-eslint-plant.log`). It is discarded.

**Fragments:** both read; accurate against my measurements, except finding -5.

## HOW
- **The clone.** `scratch/clone`, with read-only alternates to the Blockchain object store. It was fetched with that project's deploy key via a one-shot `GIT_SSH_COMMAND`; push is `DISABLED`.
- **The worktrees.** `wt-dev` at ce35818d50ae and `wt-head` at 84eea21e360a, both sparse on `Blockchain/Dev` and `Projects Documents/fragments`. Each got a fresh `npm ci --ignore-scripts` and a fresh shared build.
- **Probe file.** `gate354-probes.test.ts` = the PR's harness (lines 1-237, verbatim) plus `scratch/probe/r-cells.ts.part`. It was copied in only for runs and moved out after (last copy: `scratch/probe/r-last-run-copy.test.ts`).
- **GitHub reads.** `gh api` GET only, with the Blockchain `GH_CONFIG_DIR`. The PR JSON is in `scratch/pr2232-r.json`.
- **No writes outside this folder.** No `cd`, no `rm`.

## NOT TESTED (UNMEASURED)
- Real Stripe (any call), a real webhook delivery or signature, a real delayed payment method, or whether the live endpoint subscribes to the two async events. All Kam's check, per the PR body.
- A real PostgreSQL and the `billing_credit_grants` constraint itself (only the in-memory model was used); a booted service; two replicas.
- Node 24; Schemathesis, Akto, Playwright, k6; the pre-push preflight.
- The docs-fragments check: it refused, rc 2, because `systemTest/` is outside my sparse tree.
- The text of Wednesday's 04:40Z plan ANSWER (I read it only as quoted, in the PR body and the seat's HANDOVER); KS-1934's Linear state and comment; `calculatePricePerCert`.
