"""Billing webhook idempotency regression (KS-492 / Review G, finding KS-488-C).

Finding (KS-488, work-stream C): ``services/billing/src/routes/webhooks.ts:34`` — ``isEventProcessed``
returns ``false`` when the DB is unavailable (fail-**open**), so a redelivered Stripe event
re-adds credits during a DB blip; ``recordEvent`` also silently no-ops without a DB.

Why this is a documented **skip**, not a live assertion: the billing webhook first verifies the
raw-body ``stripe-signature`` via ``constructWebhookEvent`` and answers 400 on any missing/invalid
signature (``webhooks.ts:95-110``) — so reaching the idempotency logic at all needs a **genuine
Stripe-signed event**, i.e. the webhook signing secret and a correctly-constructed payload, which
the schemathesis harness does not hold. Worse, the specific defect (fail-open) only manifests when
the **DB is unavailable**, which a black-box API test cannot induce on the shared local stack.
Exercising this needs a billing-service test harness that can sign events and control DB
availability (the ``systemTest/integration`` harness KS-492 anticipates) — **tracked as KS-502**,
not schemathesis.

This test records the expected contract so the gap is tracked; un-skip it in a harness that can
sign Stripe events and simulate DB-unavailability (KS-502).

systemTest rule: reproduce against the local stack; ``KS-###`` text refs only, no GitHub URLs.
"""

import pytest

# The gateway route for Stripe webhooks (no bearer — Stripe-signed, raw body): /webhooks/stripe.
STRIPE_WEBHOOK_PATH = "/webhooks/stripe"


class TestBillingIdempotency:
    """A redelivered Stripe event must not double-credit, even on a DB blip (KS-488-C)."""

    @pytest.mark.skip(
        reason="KS-488-C: the webhook rejects any unsigned/invalidly-signed body with 400 before "
        "the idempotency logic, so reaching it needs the Stripe signing secret + a constructed "
        "signed event the harness does not hold; and the fail-open defect only manifests with the "
        "DB unavailable, which a black-box API test cannot induce. Needs a billing harness that can "
        "sign events and control DB availability (the systemTest/integration harness KS-492 anticipates; KS-502)."
    )
    def test_redelivered_event_does_not_double_credit(self) -> None:
        """A duplicate Stripe event is processed once (no double credit), even during a DB blip."""
        # KS-502 fail-on-unskip guard. This body is deliberately a hard failure, NOT empty: an empty
        # body PASSES the moment the skip marker above is removed, reporting green "coverage" for a
        # security vector that was never exercised — strictly worse masking than the skip itself.
        # Implement the assertions (sign a Stripe event with the webhook secret, deliver it twice,
        # assert credits applied once) BEFORE removing the skip.
        pytest.fail(
            "KS-502/KS-488-C: billing webhook idempotency is NOT implemented. Removing the skip "
            "marker does not create coverage — implement the signed-event replay assertions first."
        )
