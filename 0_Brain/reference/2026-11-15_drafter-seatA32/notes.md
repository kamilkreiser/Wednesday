# Drafter notes, Seat A 32nd KS-1897 build brief (2026-11-15 ~18:40 AEDT)

- Read whole: commission, A31 template brief, Wednesday's mail to A31, A31 HANDOVER (17 KB), gate 361 verdict.
- Base: develop 9bb6c98b2c47228e2c217cff30f252e1f2148177, read by `gh api .../branches/develop` and `git ls-remote origin refs/heads/develop` (read verb) at 18:35 and 18:38; equal.
- Sources read at that sha via gh api raw contents (saved in session scratchpad): webhooks.ts, billing.ts, stripeService.ts, creditGrants.ts, ks1934 test, ks1364/ks445/ks1888 tests (grep only).
- Facts that differ from A31's plan (it was read at ce35818d50ae): develop now has PR 2232 (paid check at 513, no-customer return at 503, async_payment_succeeded routed). Line numbers updated. No creditLock.ts on develop.
- Added from my own reading: (1) builders spread params.metadata LAST, so route metadata must be exactly userId/tenantId (cell M11); (2) dispatcher sets webhook_events customer_id from session.customer, so a matched credit shows customer null with credits_added > 0 (reconciliation list must filter on credits_added = 0); (3) ks1934's stripe double has no listCustomersByEmail, C2d fixture has neither customer nor email, so keeping the 2232 line for "neither" leaves that file untouched; (4) the 2235 import insertion at billing.ts 25-26 would conflict with an import added to billing.ts's top block, so the helper import goes in webhooks.ts only.
- 2235 overlap verdict: NO textual overlap with the designed write set; build on develop now; rebase/re-cut only if 2235 merges first. Measured by hunk ranges and blob shas, not merge-tree.
- Open PRs touching services/billing: 2235, 649, 575 (88 open scanned, control 2235 = 5 files).
- Ordinals: A32nd 0, A31st 1. Routing row present. Model claude-opus-5-5.
- Writes: only the brief and this file. No !CODING writes. gh read-only (GET). No secret printed.

UNMEASURED: merge-tree of KS-1897 against PR 2235 (no tree built, hunk-range reading only); the billing suite on develop or any tree; Stripe customers.list email case semantics and SDK typings; token field names userId/tenantId on /billing (only A31's read of JwtPayload relied on); push queue, lock, cockpit floor; whether the brief's own cell design compiles against the ks1934 harness.
