# Spark operator 55, 2026-11-02: KS-1868 billing webhooks.ts Stripe-webhook path (3 held, 0 skipped)

## BLUF
P1 (:166), P2 (:184), P3 (:215) all PASS 7/7, byte-identical to the golden, on the ORIGINAL brief (no rebrief), control PASS first time each, all three HELD. No site skipped: for each, the after-state equals what an ordinary Error already produces (measured by cells, see below). Tip: develop 03977e89a343ad7362760e4fb0270602fb6da5ce at start (ls-remote 07:04:46 AEDT) and at end (tip_end.out); the round tooling cache was at that sha. Open-PR scan start and end: 19 PRs / 108 files, NO PR lists routes/webhooks.ts (services/billing only as package.json/package-lock.json in 575, 649, 1360); planted control services/billing = 3 entries both times. Lanes beyond open PRs not checked. PR 1906 (replay :316, in the tip) is the ref.
Dry runs: all three returned rc 3 BUSY (round.lock held by operator 54), so no dry run was possible; the golden control (which builds the same input) stood in. See UNMEASURED.

## Held (pasted from ls night | grep O55)
READY_KS-1868-KS-1868-O55-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-STRIPE-WEBHOOK-SIGNATURE-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O55-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-STRIPE-WEBHOOK-CLAIM-CATCH-PASS-7of7_2026-11-02.diff.md
READY_KS-1868-KS-1868-O55-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-STRIPE-WEBHOOK-HANDLER-CATCH-PASS-7of7_2026-11-02.diff.md

## Per pass (hunks are >3 lines apart: 166, 178-184, 213-218; disjoint, apply in any order)
### O55-P1 :166 signature-verification catch (`String(error)`)
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/3 green=3/3 suite=331->334 strict=True`. Model 49.4 s, 17243+1976 tok.
- Fix: inner try around the SAME expression `String(error)` into `reason`, fallback `unreadable thrown value` (PR 1906 pattern). Ordinary Error still logs `Error: <msg>`.
- Callers: the /stripe route handler itself (only route the gateway forwards to billing).
- BEHAVIOUR CHANGE (PR text): runs before the idempotency claim and before any DB write. Hostile throw today: Stripe gets NO response (async rejection unseen by Express 4; request hangs to Stripe's timeout); after: constant 400 `Invalid signature`, what an ordinary verification error already gets. Persisted: nothing, before or after (cell asserts zero db calls). No paid event is processed, retried differently, or marked duplicate by this change. Defence in depth (constructWebhookEvent is Stripe's SDK).
- Tier: 2 (not money-moving: pre-claim, nothing persisted). Raise seat may promote to 1 if it wants the whole file's three PRs reviewed alike.
### O55-P2 :184 claim-failure catch
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=7 product_minus=1 red=2/4 green=4/4 suite=331->335 strict=True`. Model 56.6 s, 17726+2308 tok.
- Fix: same guard (`error instanceof Error ? error.message : String(error)` into `reason`), log uses `error: reason`.
- Callers: the /stripe handler. Reachability note (in the brief and for the PR): claimEvent throws its own ClaimUnavailableError for every DB failure, so a hostile value reaches this catch only if something claimEvent calls outside its try (logger.warn in the !isDbAvailable branch) throws one. The test makes logger.warn throw. Defence in depth.
- BEHAVIOUR CHANGE (PR text): hostile throw today: Stripe gets NO response (timeout, retried); after: constant 503 SERVICE_UNAVAILABLE (retried with backoff), same as an ordinary claim failure. Persisted: no webhook_events row on this path either way (claim not won), no credits (cells assert db and credit calls 0), nothing marked duplicate.
- Tier: 2.
### O55-P3 :215 handler catch, MONEY-ADJACENT
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=6 product_minus=1 red=3/5 green=5/5 suite=331->336 strict=True`. Model 68.5 s, 18642+2909 tok.
- Fix: `let message: string;` + inner try/catch with the constant fallback; every later line (log, `releaseClaim(event.id, message)`, constant 500) untouched.
- Callers: the /stripe handler.
- BEHAVIOUR CHANGE (PR text; this is Seat E 25th's "skips a paid event" site): hostile throw out of handleWebhookEvent, today: (1) Stripe gets no response, (2) webhook_events row stays 'processing' (releaseClaim never reached), (3) Stripe's redelivery loses the claim (the upsert only re-claims status 'failed') and is answered 200 {received:true,duplicate:true} WITHOUT processing, so the paid event is skipped, (4) only admin POST /webhooks/replay recovers it. After: (1) constant 500 (Stripe retries), (2) row set 'failed', (3) redelivery re-claims and is processed. That is exactly the ordinary-Error path; cells C1/C2 (ordinary Error: row 'failed', redelivery 200 {received:true}, one grant) are green at the tip and R1-R3 (hostile) are red at the tip and green after. So the after-state equals the ordinary path and the site is in scope under the brief's rule. Cell R3 pins the money consequence (redelivery processed, one grant, row 'processed'; at the tip it is acknowledged as duplicate).
- Pre-existing, NOT changed, for the raise seat to mention: a value thrown AFTER addCertificationCredits succeeded (later log calls in handleCheckoutComplete) is released and re-processed on redelivery for an ordinary Error today, so a double grant window exists already; the fix extends that same behaviour to hostile values. Whether to close it is a design question for Kam.
- Tier: 1 (money-adjacent), per your default.

## Raise-seat notes
- strict=True on all three: plain git apply works. Tests are new files: ks1868-billing-webhook-stripe-signature-unreadable-throw / -stripe-claim-unreadable-throw / -stripe-handler-unreadable-throw .test.ts under services/billing/src/__tests__ (3 / 4 / 5 cells). Combined suite 331 -> 345 expected if all three applied (UNMEASURED together).
- Red cells at the tip rely on a 2.5 s request deadline (unanswered request), so each red cell takes ~2.5 s; P3 R3 ~2.5 s plus a second request.
- Refs KS-1868; do not close. PR 1906 is the replay-handler sibling already merged.
- Generators and test sources: gen/ (mk55.py, t55_p1..p3.ts.txt, hold55.sh, prscan55.py); briefs night/briefs/ks_1868_o55_p1_*, p2_*, p3_*.

## Round log (done.md row timestamps AEDT)
- 07:11:57 O55-P1 CONTROL-PASS 88 s, golden byte-identical (queued 07:08:41 behind op54)
- 07:12:46 O55-P2 CONTROL-PASS 47 s, byte-identical
- 07:14:23 O55-P3 CONTROL-PASS 97 s, byte-identical
- 07:16:20 O55-P1 model PASS 7/7, round 115 s, model 49.439 s, byte-identical
- 07:18:03 O55-P2 model PASS 7/7, round 102 s, model 56.612 s, byte-identical
- 07:20:37 O55-P3 model PASS 7/7, round 153 s, model 68.544 s, byte-identical
Queue discipline: controls appended together at 07:08:41; each model line appended right after its control row appeared; model rounds ran back to back with the control of the next pass (no idle gap observed beyond other operators' lines). Full rows: done_rows.out. Only appends to queue.md.

## UNMEASURED
Dry runs (BUSY rc 3 for all three, dry_p*.out); whole-suite with all three passes together; real Postgres / real Stripe SDK / the real Express response to Stripe (status codes and Stripe's retry behaviour are read from the route and Stripe's documented non-2xx-retry rule, not run against Stripe); eslint; live lanes beyond open PRs; whether any real path throws an unreadable value here.
