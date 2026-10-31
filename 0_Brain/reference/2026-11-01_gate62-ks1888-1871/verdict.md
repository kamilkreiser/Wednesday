## QA GATE 62, TIER 1, ROUND 1: KS-1888 #1871

**BLUF: GO WITH NOTES.** At `aa64f183` every billing route that takes a customer, invoice or payment-method id runs one check, `mayActOnCustomer` (owner = the Stripe customer's stored `metadata.userId`, plus `metadata.tenantId` where one is recorded, or the shared `isPlatformRole`). The check runs before any Stripe write, any listing and any log line. POST /customers takes the owner from the token. All 12 routes plus POST /customers are guarded. Nothing in `services/billing` that touches a customer is unguarded, apart from the two checkout routes (KS-1897, stated out of scope), POST /admin/credits (platform-admin only since KS-1850) and the two webhooks (Stripe signature; replay needs `requireRole('SYSTEM_ADMIN','SUPER_ADMIN')`). I ran 10 refused principals on each of the 12 routes. For every one, the refusal matched an unknown id byte for byte: **status, body and every response header except Date** (120 cells), with no effect call, the store unchanged and nothing logged. I wrote 18 mutants of my own. **17 were killed by the PR's own tests and 1 survived** (G62-F3, a test gap that costs availability and leaks nothing). The head merges cleanly onto develop `1ae193f7`, and the billing suite is 324/324 on the merged tree. Nothing blocks the merge. There is one minor side channel (G62-F1: two of the 12 routes make one extra Stripe round trip on a refusal, so latency, not bytes, separates "exists but foreign" from "unknown"). The stated limit is also understated (G62-F2).

- PR https://github.com/Secuura/Distributed_Secuura/pull/1871 · ticket KS-1888 (https://linear.app/secuura/issue/KS-1888) · author Seat E 22nd · commissioned by Wednesday, Sun 1 Nov 2026
- **Head at START** (2026-10-31T13:50:48Z UTC = 1 Nov 00:50 AEDT, `git ls-remote`): `refs/pull/1871/head` = `aa64f183eda0f45ab070379a61b36ee1eefac603`, develop = `1ae193f79a124cadfa7c2a3ce72fe1ae76305af0` (`evidence/lsremote_start.txt`)
- **Head at END** (2026-10-31T14:07:26Z): `refs/pull/1871/head` = `aa64f183eda0f45ab070379a61b36ee1eefac603`, develop = `1ae193f79a12…`. **Unchanged** (`evidence/lsremote_end.txt`)
- Clone: `0_Brain/reference/2026-11-01_gate62-ks1888-1871/repo` (blob:none, fetched over the Blockchain deploy key, push URL set to `DISABLED_READ_ONLY`). `rev-parse --show-toplevel` equalled the clone directory before any fetch (`ASSERT_OK`). It was left at the head with **0** porcelain lines after the base swap and all mutants were restored (sha256 verified after each one). Nothing was pushed, commented on or written to GitHub or Linear. No Stripe call of any kind was made: every route cell uses the PR's in-memory fake.
- Host: Apple Silicon Mac, **Node v26.8.1, which is not LTS. Node 24 LTS is UNMEASURED.** vitest 4.1.12. Load was 7 to 13 throughout. All suites ran with `nice -n 10` and `--maxWorkers=2`.
- Path note: the brief named `2_Project_Files/fleet/spark_gate.sh`, which does not exist. The script is at `2_Project_Files/local-model/gate/spark_gate.sh`.

## VERDICT: GO WITH NOTES

## Findings

**G62-F1 · minor (side channel, follow-up).** On `GET /invoices/:id` and `DELETE /payment-methods/:id` a refusal makes **two** Stripe round trips, while an unknown id makes **one**. Measured by counting lookup calls in the harness (`evidence/gate62_probe_callcount.log`):
- invoice: refused `getInvoice 1 + getCustomer 1`, unknown `getInvoice 1`
- payment method: refused `getPaymentMethod 1 + findCustomer 1`, unknown `getPaymentMethod 1`

On the other 10 routes the counts are equal. The bytes are identical, so this is not an oracle in the response itself. But one Stripe RTT, typically 100 ms or more, is visible to a caller, so a caller can tell "this in_/pm_ id exists and belongs to someone else" from "no such id". Exploitability is low: Stripe ids are high-entropy and the channel reveals existence only, never content. The PR's claim "byte-identical to an unknown id" is **true as worded**. The fragments do not claim timing parity. Fix if wanted: accept and document it, or do a fixed dummy lookup on the unknown branch.

**G62-F2 · minor (limit wording, fix-before-merge only if cheap; before deploy for the data question).** The stated limit, "a customer created before this change carries whatever userId **its creator** posted", understates the risk. At develop `df99b047`, `PUT /customers/:id` (`billing.ts:309-318`) had no owner check and accepted any `metadata` record. So **any authenticated caller could overwrite `metadata.userId` / `metadata.tenantId` on any customer**, not only its creator. A pre-existing customer therefore carries whatever userId the **last writer** set. Since this PR (D3 + D1) nobody but a platform admin can change it again, so the exposure is frozen at whatever happened before deploy. Suggested rewording: "carries whatever userId was last written to it before this change, by its creator or by any caller through the old PUT". Before deploy, Kam may want the unmeasured count the fragments name (customers whose `metadata.userId` is not their real owner). That is a Stripe-side audit, which this gate did not do and must not do.

**G62-F3 · minor (test gap, follow-up).** My mutant M18 **survived** all 211 PR cells. It changes `GET /customers/by-email` back to Stripe's first match (`findCustomerByEmail`) and checks only that match. The PR's duplicate-email cell P7 covers POST /customers only. The effect of the regression is availability, not a leak: if another user created a customer with the owner's email first, the owner would get 404 on their own lookup. Fix: add a by-email twin of P7.

**G62-F4 · file-only (scope of the "outage stays 503" claim).** The five GET routes that look up the owner through `getCustomer`, which swallows **every** error, still answer **404 on a Stripe outage**: `GET /customers/:id`, `/credits`, `/purchases`, `/invoices`, `GET /invoices/:id`. That was already true for `:id` and `:customerId/*`. The PR's 503 claim is scoped to the `findCustomer` / `getPaymentMethod` routes (cells X1×5 and X2), and my M15/M16 confirm those. So no claim is false, but "the owner lookup must not turn a provider outage into a 404" (test header) holds only for those 6 routes.

**G62-F5 · file-only ("nothing is logged").** Measured: the billing logger (all four levels mocked) records nothing on a refusal in 120 of my cells. M12 (log caller and id before the check) was killed by the PR's own cells. The one line that can carry the id is the request logger in `index.ts:57-62`, `logger.debug('Request', {method, path})`. It is identical for an unknown id and is emitted only when `LOG_LEVEL=debug` (the default is `info`, `utils/logger.ts:19`). The harness mounts the router without `index.ts`, so this is from reading the code, not a measurement. Unlike gate 59, no error-level line is written: no refusal path throws.

**G62-F6 · file-only.** `POST /customers/:customerId/default-payment-method` checks the customer but not that the body's `paymentMethodId` belongs to it. Setting another customer's pm relies on Stripe refusing an unattached pm. This is unmeasured against real Stripe and predates this PR.

**G62-F7 · file-only (operational).** Customers without `metadata.userId`, for example ones created in the Stripe dashboard or by Checkout, are now platform-admin only (D1, cells R4/A4). Their human owners lose self-service on these routes. This is by design, and how many exist is unmeasured.

**G62-F8 · file-only (edge).** `listCustomersByEmail` uses `limit: 100` with no paging. With more than 100 customers on one email, the caller's own customer can be missed: POST then creates a duplicate and by-email returns 404. It fails closed.

## Q1. Coverage: every route that reads or writes a customer, invoice, subscription or payment method
**FOUND:** the registrations, from `grep` of `router.(get|post|put|patch|delete)` in `services/billing/src/routes/*.ts` and `app.*` in `index.ts` at the head:

| Route | Touches | Guard at head |
|---|---|---|
| POST /customers | customer create / existing by email | token owner; body userId ≠ caller → 403 unless platform admin; existing returned only if `mayActOnCustomer` |
| GET /customers/by-email | customer | `mayActOnCustomer` on every match (D4 moved above `:id`) |
| GET /customers/:id | customer | `mayActOnCustomer` |
| GET /customers/:id/credits | balance | `mayActOnCustomer` (unknown now 404, was 0) |
| PUT /customers/:id | customer write | reserved keys 400, then `mayActOnCustomer(findCustomer)` |
| GET /customers/:customerId/purchases | payment intents | `mayActOnCustomer` |
| GET /customers/:customerId/invoices | invoices | `mayActOnCustomer` |
| POST /customers/:customerId/setup-intent | Stripe write | `mayActOnCustomer(findCustomer)` |
| GET /customers/:customerId/payment-methods | pms | `mayActOnCustomer(findCustomer)` |
| POST /customers/:customerId/default-payment-method | customer write | `mayActOnCustomer(findCustomer)` (G62-F6) |
| DELETE /payment-methods/:id | pm detach | `mayActOnAttachedTo(pm.customer)` |
| GET /invoices/:id | invoice | `mayActOnAttachedTo(invoice.customer)` |
| POST /credits/use | balance spend | `mayActOnCustomer(findCustomer)` |
| POST /admin/credits | balance add | `isPlatformRole` (KS-1850, unchanged) |
| POST /checkout/bundle, /checkout/custom | checkout with `req.user.stripeCustomerId` | **out of scope, KS-1897** (stated) |
| POST /webhooks/stripe | credits via event | Stripe signature |
| POST /webhooks/replay | replay | `authenticate()` + `requireRole('SYSTEM_ADMIN','SUPER_ADMIN')` |
| GET /bundles, /bundles/:id, /config, /pricing, /health, / | no customer | n/a |

**No subscription routes exist** in this service. **No customer-touching route is unguarded** apart from the KS-1897 checkout pair.
**TESTED:** each of the 12 id routes has PR cells A1–A4, R1–R7 and U1, plus my 10 refused principals. M1, M2 and M3 drop the check on one route each and are killed by the PR's cells (7, 7 and 8 cells).

## Q2. Equivalence: byte-identical, and the check before any effect
**FOUND: yes for bytes and headers. Yes for ordering.** Every refusal uses the route's own unknown-id 404 literal (`sendNotFound` or the existing inline 404). The check sits before the first Stripe write or listing on every route, and no logger call precedes it.
**TESTED (`evidence/gate62_probe_head.log`, `gate62-probe.test.ts`):** 120 cells (12 routes × 10 principals). `sendFull` compares status, body and **all response headers except `date`/`connection`/`keep-alive`** between refused and unknown. A control cell confirms the compared header set includes `content-type`, `content-length`, `etag` and `x-powered-by`, and 12 owner-vs-unknown controls confirm the instrument tells the two apart. Each cell also asserts 0 effect calls, an unchanged store snapshot and an unchanged log, and all **144/144 pass**. Mutants: M6 (setup-intent write before the check) was killed. M8 (different 404 message on invoices) was killed. M12 (log before the check) was killed. The one asymmetry found is the round-trip count (G62-F1).

## Q3. Who counts
**FOUND:** the owner comes from the **stored Stripe object** (`customer.metadata.userId`/`tenantId`, from `getCustomer`/`findCustomer` by the path or body id; for an invoice or pm, from its stored `customer` field). It is never taken from request input. Platform admin = shared `isPlatformRole` (`packages/shared/src/security/keyRevokePolicy.ts:140`: SYSTEM_ADMIN / SUPER_ADMIN, ASCII fold only, non-string refused). The owner can no longer change the owner fields (D3: `userId`, `tenantId` and `certificationCredits` give 400 for everyone).
**TESTED:** refused on all 12 routes, byte-identical to unknown: ORG_ADMIN of the owner's tenant, anonymous, a `CONNECTOR`-role token with a userId, a `SERVICE` token with no userId, an array role `['SYSTEM_ADMIN']`, role `ADMIN`, `SYSTEM_ADMıN` (dotless i), the owner's userId with no tenant claim on a tenant-stamped customer, and the owner's userId in upper case. POST /customers: ORG_ADMIN, connector, service, array role, anonymous and a plain OWNER posting `userId: u-alice` all get **403 with no Stripe call** (6 cells). Anonymous with `userId: ''` gets 403. A body `metadata.userId`/`tenantId` on create is stripped, and the owner is the caller. An ORG_ADMIN posting the owner's email gets a new customer, never the owner's. PUT with `userId: ''` or `tenantId: ''` gives 400 with nothing written. Mutants: M4 (body userId trusted) killed; M5 (admin check inverted) killed; M9 (ORG_ADMIN same-tenant bypass) killed; M14 (pm owner from the request query) killed; M17 (no-userId guard removed, String-coerced compare) killed.

## Q4. Mutants
`scripts/mutants.py`. Each mutant is applied by a unique anchor (count asserted = 1), the suite is run, the file is restored, and sha256 is verified after every mutant (`restored: true`). The control (unmutated) run is 355/355 over the 3 files (`evidence/mutant_control.log`). I ran each mutant twice: against the PR's two test files only (`own_mutants_pr_tests_only.json`) and with my probe added (`own_mutants.json`).

| # | Mutant | PR tests only | + gate probe |
|---|---|---|---|
| M1 | check dropped on GET /customers/:id | killed, 7 | killed, 17 |
| M2 | check dropped on POST /credits/use | killed, 7 | killed, 17 |
| M3 | check dropped on DELETE /payment-methods/:id | killed, 8 | killed, 18 |
| M4 | POST /customers trusts body userId | killed, 3 | killed, 9 |
| M5 | platform-admin check inverted | killed, 127 | killed, 248 |
| M6 | setup-intent Stripe write before the check | killed, 8 | killed, 18 |
| M7 | tenant conjunct dropped | killed, 12 | killed, 24 |
| M8 | invoice refusal gets a different 404 message | killed, 8 | killed, 18 |
| M9 | ORG_ADMIN same-tenant bypass | killed, 12 | killed, 25 |
| M10 | POST existing-by-email unfiltered | killed, 2 | killed, 3 |
| M11 | PUT reserved-key refine removed | killed, 4 | killed, 6 |
| M12 | log caller+id before the check | killed, 7 | killed, 17 |
| M13 | invoice/pm with no customer admitted | killed, 2 | killed, 2 |
| M14 | pm owner from request query | killed, 2 | killed, 3 |
| M15 | credits/use lookup swallows outage | killed, 2 | killed, 2 |
| M16 | `isMissingResource` always true | killed, 8 | killed, 8 |
| M17 | no-userId guard removed / coerced compare | killed, 12 | killed, 12 |
| M18 | by-email first match then check | **SURVIVED** (211/211) | **SURVIVED** (355/355) |

**17/18 killed. M18 survived → G62-F3.** I did not re-run E's own 26 mutants (I don't have them); E's "26 of 26" is UNVERIFIED as stated.

**Red-first:** base product files (`billing.ts`, `stripeService.ts` from `df99b047`) under the head's two test files give **120 failed / 91 passed** (`evidence/ks1888_base_product.log`). The failures are product reasons: `expected {status:200} to deeply equal {status:404}`, `no Stripe write or listing for a refused caller: expected 1 to be +0`, `expected 201 to be 403`, `expected 200 to be 400/503`, and `service.findCustomer/getPaymentMethod/listCustomersByEmail is not a function` in the lookups file. This matches E's "102 of 192 route + 18 of 19 lookup" (120 red, 91 green). Spark's runner got the same 91/120 independently.

## Q5. Merge
**FOUND:** develop moved 11 commits from `df99b047` to `1ae193f7`, touching 66 files. **0 overlap** with the PR's 8 files. The control: the same `grep -x -F -f` matches a known line (1), and the develop file list has 37 `services/` lines, but none under `services/billing`, `packages/shared` or the root `package*.json`. `git merge-tree --write-tree 1ae193f7 aa64f183` gave tree `fc1246c6…`, **rc 0, clean** (`evidence/merge_tree.txt`). The merged tree differs from develop in **exactly the PR's 8 files** (`git diff --name-only 1ae193f7 fc1246c6`). The diff stat from head to merged tree for billing, packages and the root package files is empty.
**TESTED:** I made a local merge commit `0db6de29` (never pushed) and a worktree at `tmp/merged` using the clone's installed `node_modules`, then ran the full billing suite there: **13 files, 324/324, rc 0** (`evidence/vitest_merged_full.log`). At the head: also **324/324, rc 0** (`evidence/vitest_head_full.log`). `tsc --noEmit -p services/billing/tsconfig.json`: rc 0. `npm run lint` (eslint src + the 2 product files): rc 0, 0 errors, 3 warnings, all on unchanged lines (`stripeService.ts:154`, `:540`, unused `error`). No planted-error control was run for eslint this time.

## Q6. Node
Node **v26.8.1** (a Current release, not LTS). **Node 24 LTS is UNMEASURED.** E's fragment also says it was not measured on LTS.

## COUNTS
- Findings: 0 blocker · 0 major · 3 minor (F1 timing, F2 limit wording, F3 test gap) · 5 file-only (F4–F8)
- PR cells: 211/211 at the head; 120 red / 91 green at base product
- Gate cells: 144 probe + 12 call-count (10 equal, 2 unequal → F1)
- Own mutants: 18, killed 17, survived 1
- Billing suite: 324/324 at the head, 324/324 on the merged tree

## SPARK SHADOW AND CALIBRATION
- `spark_gate.sh` (non-pytest mode, the two ks1888 files, `--node-modules` = the clone's root `node_modules`, `--work` = `…/scratchpad/gate62_spark`, `--out` = `evidence/spark/facts`): **rc 0 in 16 s**. It reported head 211/0, base product 91/120, diff 8 files +845/-44, merge-base `df99b047`, base tip `1ae193f7`. All five match my figures. **The gate 60 npm-workspace hoisting break did not reproduce** with the root `node_modules`.
- `spark_review.py` (`--ticket KS-1888`, `--pr-body-file evidence/commit_message.txt`, because the PR body could not be read: see UNMEASURED): **rc 4, "SCHEMA FAILURE x2"**. Both attempts ended in `repetition_abort`: attempt 1 at 84.1 s ("claim repeated 3x: 'the fix does not actually close the idor for a customer whose metadata.userid is'") and attempt 2 at 19.6 s ("claim repeated 5x"). The JSON could not be parsed. It produced **no Spark verdict** (`evidence/spark/review/`). The prompt was 58.4K tokens (touched files 124,644 chars).

**Calibration** (taken from the raw draft in `raw_attempt1.txt`, because no valid review exists)

| Spark draft finding | Severity (Spark) | Mine | Call |
|---|---|---|---|
| The owner can re-own a customer by `PUT metadata.userId` | Major | D3 refuses `userId`/`tenantId`/`certificationCredits` with 400 for everyone. PR cells M1×3 and my empty-value cells test it, and my M11 was killed | **Spark false positive.** But it was close to G62-F2, the **pre-change** PUT rewrite that Spark did not frame as pre-change |
| An absent or wrong `metadata.userId` "falls back to trusting" | Major (repeated, looped) | An absent owner is platform-admin only (R4/A4, M13 killed). A wrong pre-existing one is the stated limit | **Partly false.** "Absent" is wrong; "wrong" is the stated limit |
| — | — | G62-F1 timing asymmetry (measured) | Spark missed |
| — | — | G62-F3 by-email duplicate gap (M18 survived) | Spark missed |
| — | — | G62-F4–F8 | Spark missed |

| | Verdict |
|---|---|
| Spark | **none** (rc 4, schema failure ×2, repetition loop) |
| Gate 62 | **GO WITH NOTES** |

## UNMEASURED
- **The PR description and its Test Evidence block on GitHub.** `gh pr view` with the Blockchain project's `GH_CONFIG_DIR` returned rc 4, "gh auth login" (`evidence/pr_view.err`). I did not authenticate. The claims I checked come from the commit message and the two docs fragments in the diff, which carry D1–D4, the limit, the KS-1897 out-of-scope note, 324/324, 102+18 red-first, 26/26 mutants and Node v26.8.1. Whether the GitHub body carries the same text is unverified.
- Node 24 LTS. A running stack, the real `index.ts` middleware chain (`jwtAuthenticate`, request logger) and real or test Stripe. The four platform suites (Schemathesis, Akto, Playwright, k6).
- Wall-clock timing of G62-F1 (I counted calls instead of timing them).
- How many existing Stripe customers carry a wrong `metadata.userId` (G62-F2). Stripe's behaviour for G62-F6.
- E's own 26 mutants. A planted-error control for eslint.

## HOW
- Clone: `git clone --filter=blob:none --no-checkout` over the deploy key, then the toplevel assertion, `fetch refs/pull/1871/head`, detached checkout of `aa64f183`, `npm ci --ignore-scripts` at `Blockchain/Dev` (1795 packages, rc 0) and `npm run build` in `packages/shared` (rc 0).
- Suites: `nice -n 10 node_modules/.bin/vitest run --root services/billing --maxWorkers=2`, with TMPDIR set to the gate `tmp/`.
- Probe: `scripts/gate62-probe.test.ts` = the PR test's harness (lines 1–216, verbatim) plus my cells. It was copied into `src/__tests__/` for runs and is now parked at `tmp/gate62-probe.test.ts.parked`, so the clone tree is clean. There is a copy in `evidence/`.
- Mutants: `scripts/mutants.py` (`PR_ONLY=1` for the PR-tests-only pass).
- Merge: `merge-tree --write-tree`, then `commit-tree` (local only), then `worktree add tmp/merged` with `node_modules` symlinked to the clone's.
- Processes: I started none in the background apart from `spark_review.py` (it exited on its own) and two `grep`/`git grep` jobs that I stopped by their task id. I killed nothing by name.
