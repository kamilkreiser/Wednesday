"""Pytest fixtures for the two dedicated isolation tenants (KS-1042).

Why these exist, and why find-or-create by slug: ``tests/support/isolation_tenants.py``. Registered in
``tests/conftest.py`` so any live module can request ``isolation_tenant_a`` / ``isolation_tenant_b``.

A tenant that cannot be found, created or re-activated FAILS the requesting test — never a skip,
because a cross-tenant check with no second tenant has tested nothing (systemTest MUST #13 rule 6).
Nothing here logs a response body: the create answer carries a metering key.
"""

import httpx
import pytest

from tests.support import isolation_tenants as it


def _ensure_tenant(admin: httpx.Client, slug: str, name: str) -> str:
    """Find the tenant with ``slug``, creating or re-activating it as needed, and return its id.

    Args:
        admin: A SYSTEM_ADMIN client (the spec's platform tenant operations are platform-admin only).
        slug: The tenant's fixed slug.
        name: Its display name, used only when creating it.

    Returns:
        The tenant's id, active.
    """
    listed = admin.get("/platform/tenants")
    row = it.tenant_with_slug(listed.json() if listed.status_code == 200 else None, slug)
    if row is None:
        created = admin.post("/platform/tenants", json={"name": name, "slug": slug})
        tenant_id = it.created_tenant_id(created.json()) if created.status_code == 201 else None
        if tenant_id is None:
            pytest.fail(f"KS-1042 precondition: could not create isolation tenant {slug!r} ({created.status_code})")
        return tenant_id
    tenant_id = str(row["id"])
    if it.needs_reactivation(row):
        # A sweep can suspend or archive any tenant; the test needs this one live.
        patched = admin.patch(f"/platform/tenants/{tenant_id}/status", json={"status": "active"})
        if patched.status_code != 200:
            pytest.fail(
                f"KS-1042 precondition: could not re-activate isolation tenant {slug!r} ({patched.status_code})"
            )
    return tenant_id


@pytest.fixture(scope="module")
def isolation_tenant_a(api_client_super_admin: httpx.Client) -> str:
    """Id of dedicated isolation tenant A (found, created or re-activated).

    Args:
        api_client_super_admin: SYSTEM_ADMIN client.

    Returns:
        Tenant A's id.
    """
    return _ensure_tenant(api_client_super_admin, *it.TENANT_A)


@pytest.fixture(scope="module")
def isolation_tenant_b(api_client_super_admin: httpx.Client) -> str:
    """Id of dedicated isolation tenant B (found, created or re-activated).

    Args:
        api_client_super_admin: SYSTEM_ADMIN client.

    Returns:
        Tenant B's id.
    """
    return _ensure_tenant(api_client_super_admin, *it.TENANT_B)
