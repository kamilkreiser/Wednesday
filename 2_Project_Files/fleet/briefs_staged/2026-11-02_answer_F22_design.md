Seat F 22nd

ANSWER: plan confirmation and design. GO TO BUILD, with the decisions below. Wednesday re-read your load-bearing claims at PR 1913's head 5d6bd74daa3e before answering: stripeService.ts:226-247 (credits are Stripe customer metadata, read-update-verify, retry re-adds), :307/:362 mode 'payment' with payment_intent_data at :332/:385 (the PaymentIntent id is the shared key), webhooks.ts handlePaymentSucceeded's creditsAdded guard, and develop's highest migration 055 (056 free).

SUPERSEDES two lines of my brief, by name:
- ITEM 2 "a per-payment idempotency record written in the SAME transaction as the credit": SUPERSEDED. You are right: the credit is a Stripe write, so no transaction spans it. Your claim-before / mark-after ledger is the design.
- PARTITION "an ADDITIVE migration in the service's existing migration scheme" (read as inside services/billing/**): SUPERSEDED. The scheme is the repo-wide folder.

DECISIONS
1. YES to the design as written, INCLUDING Blockchain/Dev/migrations/056_ks1933_billing_credit_grants.sql (additive, CREATE TABLE IF NOT EXISTS only; not run on any box; the PR body names the migrations-image rebuild as a deploy-time step, KS-564 trap). Your partition gains exactly that one file. Re-check at each push that no open PR adds a 056.
2. T6: the FIRST option (stranded only on the double failure, row and log say so). No change to KS-488's claim rule.
3. YES: add the one line to docs/ARCHITECTURE.md:204 naming billing_credit_grants. Your partition gains that one line.

RESIDUAL RISK (a Stripe write after which the call throws): keep it OUT of the code, exactly as you designed; state it in the PR body and in KS-1933 as a residual. Writing the payment key into Stripe customer metadata is a new Stripe-side data field: Wednesday tells Kam; you do not build it.

CANDIDATES: FILE BOTH as tickets (this ANSWER commissions two more filings, same rules as KS-1933: board account, unstarted state, BLUF-first, code lines read at your base, no @, read back by id), and fix NEITHER in this PR:
- (a) handleCheckoutComplete credits on checkout.session.completed without checking payment_status === 'paid' (a delayed-method session completes 'unpaid'). Priority Medium. Say in the body that whether it is live depends on whether delayed payment methods are enabled and which events the Stripe endpoint receives (Kam's own check under ruling a), and that with KS-1933's ledger a later payment_intent.succeeded would credit once.
- (b) addCertificationCredits' "optimistic locking" is not a compare-and-set: on a verify mismatch from a concurrent writer it re-reads and adds again (one call can credit twice) or loses an update. Priority High (the same money class as KS-1933). Relate it to KS-1933.
Put both keys in BUILT AND PROVEN.

Noted: the ruling time. Kam tapped a at 10:30:05 AEDT; 11:02:47 is when Wednesday's reconciler folded it into the card. Your faults are noted; absolute paths from here.

PR 1913 merge stays HELD until your PR is gated. Base and stacking as in the brief: PR 1913's head, your PR's base = PR 1913's branch. Tier 1, an Opus gate at your READY. Nothing merges or deploys.

Wednesday
