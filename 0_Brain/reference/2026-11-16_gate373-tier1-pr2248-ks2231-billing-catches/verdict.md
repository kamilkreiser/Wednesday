PR 2248: GO WITH NOTES (at head 2189fe3e5d149aef0735c8e8b5337e81646987fb; tier 1)
Head unmoved: gh api read 2189fe3e5d14 at 10:11:09 (before the first measurement) and again at 10:23:19 AEDT (before this verdict). Develop 9ddba202bb15c8eb45a692f77291d6a52adb5aec at both reads.

Gate 373, re-commission (the first gate-373 agent died with its coordinator seat at ~10:08). Nothing from that agent was trusted. Its clone in scratch/repo was re-verified (`rev-parse HEAD` = 2189fe3e, origin = Secuura/Distributed_Secuura, tracked tree clean). Its one untracked file (g373-postwrite.test.ts) and all of its notes and outputs were moved, unread, into scratch/_prev_attempt/. Everything below was re-measured. Findings only: nothing was fixed, posted, mailed, pushed or written to Linear or GitHub.

## Money (the item that would go to Kam): NO CHANGE beyond the status code
Measured with the real StripeService over a stateful stubbed Stripe client (credit lock passed through), POST /admin/credits run against develop bytes and against head bytes. Ten scenarios (scratch/g373_measure.test.ts, outputs scratch/out/D_measure.json and H_measure.json):

| scenario | develop | head | customers.update calls | stored balance (dev = head) |
|---|---|---|---|---|
| PW0 first read: connection error (before the write) | 500 | 503 unreachable | 0 | 3 (untouched) |
| PW1 verify read: connection error (after the write) | 500 | 503 unreachable | 1 | 8 (credited) |
| PW2 verify read: "No such customer" 404 | 500 | **404 "Customer not found"** | 1 | 8 (credited) |
| PW3 verify read: 429 | 500 | 503 unavailable | 1 | 8 |
| PW4 verify read: provider 5xx, StripeAPIError | 500 | 500 | 1 | 8 |
| PW5 update applied at the provider, then a connection error | 500 | 503 unreachable | 1 | 8 |
| PW6 update connection error, not applied | 500 | 503 unreachable | 1 | 3 |
| PW7 the PW1 failure, then an identical retry | 500, then 200 | 503, then 200 | 2 | **13 on BOTH** |
| PW8 deleted customer (plain Error) | 500 | 500 | 0 | 3 |

In every scenario the credits written per request are byte-for-byte the same on develop and head. A retry after a post-write failure double-credits on develop too (13 = 3+5+5): POST /admin/credits has no idempotency key, and that problem predates this PR. The PR changes only the status code, and that change can make a client more likely to retry. No in-repo caller of /admin/credits exists (git grep over ts/tsx/js outside billing: 0 hits; the openapi entries are the positive control). The gateway proxies with http-proxy-middleware and has no retry path (grep: the only gateway "retry" code is its DB probe and the brute-force config). So the PR does not change money behaviour. The double-credit risk stays a candidate filing, as Wednesday ruled (plan item c).

## Findings
- **N1 (MEDIUM, non-blocking; accepted design per plan item c; candidate filing):** the classifier cannot tell pre-write from post-write. It receives only the error object (P1 and PW0 vs PW1 give byte-identical answers). Two points go beyond what the PR and READY say:
  - (a) A "No such customer" in the verify read now answers **404 "Customer not found" after the credits were added** (PW2). That tells the caller nothing happened when something did. The cheat fragment says "503 (or 404)"; the PR body names only the 503.
  - (b) The post-write window is not only the verify read. A `customers.update` that the provider applies but whose response is lost (timeout or connection error, PW5) also answers 503 now, and 500 before. The builder's option m12 (classify only "not configured" on R7) would keep both at 500. It also keeps the pre-write PW0/PW6 at 500, which are retry-safe.
- **N2 (LOW, test gap):** nothing pins "classifier after logger.error". My 7 mutants that move each route's classifier above its logger.error line ALL SURVIVE (49/49 green). By reading, the product order is correct on all seven. If the order were swapped, classified errors would stop being logged.
- **N3 (LOW, verified equivalents):**
  - m10, the R7 classifier before the lock branch, survives. EQUIVALENT: CreditLockUnavailableError's message ("Credit balance unavailable: the database that serialises it is down") and its code 'CREDIT_LOCK_UNAVAILABLE' match no classifier pattern, and it has no type or statusCode.
  - m11, R6 with 'Customer not found', survives. EQUIVALENT in production: R6's catch is reachable only through getStripeService(), and its constructor does no network call (loadStripeConfig, new Stripe, loadStripeProductIds), so no 4xx or "No such" error can reach it.
  - The same holds for my text swaps on R1 and R2 (both survive). My R3-before-Zod and R7-before-Zod mutants also survive and are equivalent, because a ZodError matches no classifier pattern.
  - The builder's claims for m10 and m11 are VERIFIED.
- **N4 (COSMETIC, PR body):**
  - The "Measurement" heading names develop dee28f4be27b, but the suites ran at 7398976ba14a. The next line explains this.
  - A stray backtick and an unclosed parenthesis follow `restore_local_secrets.test.sh`.
  - The 404 variant (N1a) is not named.

## The six questions
1. **Seven routes:** verified. The diff has 7 hunks, +20 -0, each inside one of the seven catches, after logger.error and before the route's own 500. On R3 and R7 the call comes after the ZodError branch, and on R7 also after the CreditLockUnavailableError branch. The arguments are as ruled: R3 uses the 4-argument form, R6 'Invoice not found', the rest 'Customer not found'. Cells at head: 49/49. The K, D and G1 cells give the classifier's status for classified errors and the route's own exact 500 for `Error('boom')`.
2. **Nothing widened:**
   - The 403 on /admin/credits is answered before the try touches the provider. A-G1a (OWNER) and A-G1b (ORG_ADMIN) pass with getStripeService called 0 times.
   - Owner refusals (G3) pass. An owner-bypass control on R6 turns G3-R6 red ("expected 200 to be 404").
   - Success paths: no success-path line is in the diff. A control that changes the R6 success body turns G2-R6 red.
3. **Post-write path:** see Money and N1. The classifier cannot distinguish pre-write from post-write errors. Severity is MEDIUM: the change is status-only and the money effect is unchanged.
4. **Tests are honest:**
   - Red-first at develop bytes (9ddba202 billing.ts, which equals the 7398976 bytes): 24 of 49 red, all 24 AssertionError "expected 500 to be 503/404/400" (7 K, 16 D, P1); 25 green.
   - My own mutants (31, each restored, sha256 997f5ef036da checked after every run):
     - deleting the classifier line, per route: R1 1 red, R2 1, R3 5, R4 5, R5 5, R6 1, R7 6 (incl. P1).
     - classify-everything, per route: 2, 2, 5, 5, 5, 2, 5 red, each including that route's G1.
     - R3 three-argument call (m9): 1 red (the D-R3 "other 400" cell).
     - notFound text swaps: R3 1, R4 2, R7 2 red; R1 and R2 survive (equivalent, N3).
     - ordering mutants: m10 and both before-Zod mutants survive (equivalent); all 7 before-logger mutants survive (N2).
   - The builder's first control (R6 refusal text) re-run: it does NOT fire (49/49), as the builder said, because both sides of G3 share that line. Its replacements fire: success body → G2-R6 red; owner bypass → G3-R6 red.
5. **Nothing else changed:** the PR has 4 files per gh api: billing.ts (modified +20), the new ks2231 test file (+415), and the cheat and flow fragments (+18, +17, new). There is no change to openapi, schema, package or stripeService. One commit, "Refs KS-2231". Develop moved 7398976 → 9ddba202 by 2 files (auth test, KS-1797 cheat fragment); 0 of them under billing, shared or a lockfile.
6. **PR body:**
   - "Gate tier: 1" is present. The double-credit-on-retry candidate filing is named. KS 1888 F4 is measured (25/25 → 404) and out. The limit casts are measured (200, no crash) and out.
   - Closing keyword: 0 hits in the body and the commit message. The planted "Closes KS-1" fires 1.
   - Self-hold sentence: 0 hits. The planted hold sentence fires 1.

## Other checks (each with a control)
- **Merge-tree:** clean both ways on live develop 9ddba202 (rc 0), same tree a56b7b0f651e both ways. A planted same-lines conflict commit on develop is refused rc 1 both ways (CONFLICT in routes/billing.ts). Note: the first build of this control failed on a missing committer identity, not a conflict. It was rebuilt with an explicit identity before any result was read as a pass.
- **Whole billing suite, interleaved:**

  | run | build | result | load1 start→end |
  |---|---|---|---|
  | A1 | develop bytes | 25 files 458/458 | 6.25→7.75 |
  | B1 | head | 26 files 507/507 | 7.75→9.21 at end |
  | A2 | develop bytes | 25 files 458/458 | 7.50→7.54 |
  | B2 | head | 26 files 507/507 | 7.54→7.54 |

  This matches the READY. Every run started at load1 ≤ 8 (the gate script waits). The runner reports failures: the develop cell run showed 24 failed.
- **tsc 5.9.3:**
  - Service source: rc 0, 0 lines.
  - Source plus tests, commonjs: 19 errors (17 TS1378 in 11 existing files, plus TS6196 and TS18046). ESM config: 2 errors (the TS6196 and TS18046 already on develop).
  - The two changed files: 0 errors in either config. Control: ks2219's file is counted 1 in the same filter.
  - Planted type error: rc 2, TS2322.
  - Configs are re-pointed copies of C 41st's, in scratch/.
- **eslint** (flat config at Blockchain/Dev, run through the API with cwd set to Dev): both changed files 0 errors, 0 warnings. A planted `debugger;` in billing.ts gives 1 error (no-debugger), rc 1. Note: the plain CLI run from another cwd ignores the files ("no matching configuration") and gives a false result. That run is discarded.
- **docs-fragments check:** OK, with 2 ADVISORY lines. Removing the KS-2231 pair gives the same 2 ADVISORY lines, identical. A planted unclosed `<div>` in the cheat fragment fails rc 1 ("<div> opened 3, closed 2"). The fragment was restored from the head blob, and git status shows 0 lines.

## Not measured
- A real or test Stripe account (no account was used; doubles only).
- The production provider's error shapes.
- stripe-node's own network retries in production (v14.25.0; the service sets no maxNetworkRetries).
- Any external client of /admin/credits outside this repo.
- Class L and the limit casts were not re-run by me; they are accepted by reading (getCustomer and getInvoice swallow to null).
- The push hook was not re-run.

Artefacts: scratch/ (g.sh, suites.sh, mk_mutants.py, mut/, ctl/, out/, g373_measure.test.ts, mt_control.sh, eslint_run.cjs, tsconfig.*_g373.json). The scratch clone is left clean at head; the measure file is parked outside the tree as scratch/_g373_measure_parked.test.ts.
