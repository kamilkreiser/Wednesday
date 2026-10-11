"""Environment-gating regression for POST /api/admin/seed-demo-users (KS-492 / Review G, KS-487-B).

Finding (KS-487, work-stream B): ``POST /api/admin/seed-demo-users``
(``services/originate/src/routes/adminConfig.ts:1766``) seeds ``ORG_ADMIN``/``OWNER`` accounts
with a hardcoded ``admin123`` bcrypt hash. The router requires ``ORG_ADMIN`` but has **no**
``NODE_ENV``/``ENABLE_DEMO_SEED`` gate, so any org-admin could mint known-password accounts in
production. The fix is to gate the endpoint to non-prod.

Why this is a documented **skip**, not a live assertion: the vulnerability is *prod-only gating
behaviour*, and the local stack runs as non-prod. Post-fix, the endpoint must still work in
non-prod (where the harness runs) and refuse only in a production-like config — so a local call
cannot distinguish fixed from unfixed (it succeeds either way), and the endpoint is not in the
published OpenAPI spec, so the Schemathesis sweep never reaches it. Exercising the real contract
needs the service booted with ``NODE_ENV=production`` (and ``ENABLE_DEMO_SEED`` unset), which a
test cannot impose on the shared local stack. This test records the expected post-fix contract so
the gap is tracked; un-skip it in an environment that can set the service's ``NODE_ENV``.

systemTest rule: reproduce against the local stack; ``KS-###`` text refs only, no GitHub URLs.
"""

import pytest

# The endpoint under review (originate adminConfigRouter mounted at /api/admin).
SEED_DEMO_PATH = "/admin/seed-demo-users"


class TestSeedDemoUsersGate:
    """POST /api/admin/seed-demo-users must be refused in a production-like config (KS-487-B)."""

    @pytest.mark.skip(
        reason="KS-487-B: the gate is prod-only behaviour and the local stack is non-prod, so a "
        "local call cannot distinguish fixed from unfixed (the endpoint succeeds in non-prod "
        "either way) and it is absent from the OpenAPI spec (the sweep never reaches it). "
        "Needs the originate service booted with NODE_ENV=production / ENABLE_DEMO_SEED unset. "
        "Un-skip when a prod-like environment is available (tracked: KS-502)."
    )
    def test_seed_demo_users_refused_outside_non_prod(self) -> None:
        """In a production-like config the endpoint must refuse (not mint admin123 accounts)."""
        # KS-502 fail-on-unskip guard — see the note in test_billing_idempotency.py. An empty body
        # would pass vacuously the instant the skip marker is removed, claiming security coverage
        # that does not exist. Implement the prod-like assertion (boot originate with
        # NODE_ENV=production via the KS-489-D ComposeController, POST the endpoint, assert refusal)
        # BEFORE removing the skip.
        pytest.fail(
            "KS-502/KS-487-B: the seed-demo-users prod gate is NOT implemented. Removing the skip "
            "marker does not create coverage — implement the NODE_ENV=production assertion first."
        )
