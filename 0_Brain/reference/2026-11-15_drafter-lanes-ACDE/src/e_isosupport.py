"""Pure logic for the dedicated isolation tenants the cross-tenant tests use (KS-1042).

**Why dedicated tenants.** The cross-tenant vectors need two live tenants. They used to name seeded
ones (Oxford University, BUPA Health UK) — first by UUIDs copied from the gateway's seed code, then by
name. Neither survives a sweep: measured on slot 1 on 2026-10-21 after three pre-merge runs, the
Schemathesis fuzzer (which exercises ``PATCH`` / ``DELETE /api/platform/tenants/{id}`` as a platform
admin) had DELETED Oxford, renamed BUPA to a fuzzed string, and ARCHIVED Greenfield.

So the tests own their tenants: each is found by a fixed slug and created through the spec's
``POST /api/platform/tenants`` when missing, or re-activated through ``PATCH …/status`` when a sweep
has suspended or archived it. Slugs are fixed (not random per run) because every created tenant also
provisions a per-tenant database; a fixed slug means one per stack, not one per run.

Kept transport-free per the ``tests/support`` contract — the HTTP side is in
``tests/isolation_tenant_fixtures.py``.
"""

from collections.abc import Mapping
from typing import Any

#: The two dedicated tenants: ``(slug, display name)``. Plain words — the spec says the slug is checked
#: against ``TENANT_SLUG_BLOCKLIST`` ("test/cruft patterns are refused at validation").
TENANT_A: tuple[str, str] = ("isolation-tenant-a", "Isolation Tenant A")
TENANT_B: tuple[str, str] = ("isolation-tenant-b", "Isolation Tenant B")


def tenant_with_slug(body: Any, slug: str) -> Mapping[str, Any] | None:
    """Return the row of the tenant whose slug is ``slug`` in a ``GET /api/platform/tenants`` body.

    The spec's 200 schema is ``{success, tenants: [{id, name, slug, status, …}], total}``.

    Args:
        body: The parsed JSON body.
        slug: The exact slug.

    Returns:
        The row, or None when no row has that slug, more than one does, or the body is not that shape.
    """
    rows = body.get("tenants") if isinstance(body, Mapping) else None
    if not isinstance(rows, list):
        return None
    matches = [row for row in rows if isinstance(row, Mapping) and row.get("slug") == slug]
    if len(matches) != 1 or not isinstance(matches[0].get("id"), str):
        return None
    return matches[0]


def needs_reactivation(row: Mapping[str, Any]) -> bool:
    """Whether a found tenant must be set back to ``active`` before a test may rely on it.

    Args:
        row: A tenant row.

    Returns:
        True for any status other than ``active`` (the spec's enum is active / suspended / archived).
    """
    return row.get("status") != "active"


def created_tenant_id(body: Any) -> str | None:
    """Return the new tenant's id from a ``POST /api/platform/tenants`` 201 body, or None.

    Args:
        body: The parsed JSON body (``{success, tenant: {id, …}, …}``).

    Returns:
        ``tenant.id`` when present as a string.
    """
    tenant = body.get("tenant") if isinstance(body, Mapping) else None
    tenant_id = tenant.get("id") if isinstance(tenant, Mapping) else None
    return tenant_id if isinstance(tenant_id, str) else None
