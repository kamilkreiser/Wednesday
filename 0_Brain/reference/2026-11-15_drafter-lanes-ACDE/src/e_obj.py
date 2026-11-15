"""Two-user read tests for the six GET-by-id routes Schemathesis's ST402 check found leaking (KS-1703).

Found by the object_level_authorization leg (KS-1674), first live run, slot 2, 2026-10-20: a second user
(``ownerPeer``) was served an object that ``owner`` created, on all six routes below, with the same body. This module
reproduces each finding deterministically with an ordinary, readable test, so the evidence does not depend on a
property-based sweep drawing the right ids, and so the fix is proven red -> green by a test and not only by a sweep.

The two users are the generated OWNER actors ``owner`` and ``ownerPeer`` (``fixtures/provision-actors.ts``), in the SAME
tenant. That is what the leg tests, and it is all the local stack can do: no route places a user in a second tenant, so
cross-tenant reads are NOT covered here (KS-1703 acceptance criterion 4 asks for that test once a second tenant can be
provisioned).

Each test asserts the **secure** expectation: the second user is refused (403 or 404; 404 is the convention
``GET /api/security/audit/{id}`` already documents for a foreign id, so existence is not leaked). They are
``xfail(strict=True)`` tied to KS-1703, the repo's mechanism for an open platform defect (see
``test_notification_bola.py``): they are reported as xfailed in every run, and the moment the platform is fixed
they XPASS and fail the run until the marker is removed.

**Which markers mean what.** Transfers, transfer history and delegations are confirmed defects (their own mutating
routes use the caller; this read does not). Analytics exports, governance participants and audit entries are listed in
KS-1703 as awaiting a ruling on whether same-tenant visibility is intended; if it is ruled intended, move that route to
``test_by_design_permissive.py`` instead of deleting it.

**What cannot be masked by the marker.** The object is created, and its owner can read it back (200), in fixtures. A
fixture that fails errors the test; it never turns into an expected failure. Only the peer's read is inside the xfail.
``raises=AssertionError`` keeps the marker honest too: a connection error or any other exception in the peer's read is a
real failure, not an expected one.

systemTest rule: reproduce against the local stack; ``KS-###`` text refs only, no GitHub URLs.
"""

import secrets
import time
from collections.abc import Callable, Generator
from typing import Any

import httpx
import pytest

from src.config import get_token
from src.http_client import make_client
from tests.actor_manifest import get_actor

#: What a correctly guarded GET-by-id answers a user who is not entitled to the object. 404 is the repo's convention
#: (GET /api/security/audit/{id} returns 404 for a foreign id so existence is not leaked); 403 is also a refusal.
REFUSED = (403, 404)

_TICKET = "KS-1703"
_OPEN_DEFECT = f"{_TICKET}: the platform serves this object to a second user. Remove this marker when the fix lands."
_RULING_PENDING = (
    f"{_TICKET} (ruling pending): whether same-tenant visibility is intended is undecided. "
    "If it is ruled shared, move this route to test_by_design_permissive.py; if not, remove this marker when fixed."
)


def _new_document_id() -> str:
    """A ``doc-<ms>-<8 hex>`` external id, the format the transfer service accepts (KS-474)."""
    return f"doc-{int(time.time() * 1000)}-{secrets.token_hex(4)}"


def _client_for(actor_key: str, base_url: str) -> httpx.Client:
    """A logged-in client for one generated actor; a missing actor is a FAILURE, never a skip.

    Args:
        actor_key: ``owner`` or ``ownerPeer``.
        base_url: Gateway base URL, ``/api``-suffixed.

    Returns:
        An authenticated ``httpx.Client``.
    """
    actor = get_actor(actor_key)
    if not actor or not actor.get("email") or not actor.get("password"):
        # Not a skip (measured 2026-10-20: a `quality` run without BOOTSTRAP_ADMIN_PASSWORD moved the manifest
        # aside and all six tests SKIPPED, which reads as a pass). This is a security regression test: when its
        # precondition is missing the run must say so loudly.
        pytest.fail(
            f"generated actor {actor_key!r} is not in this slot's manifest "
            "(fixtures/generated/actors-slot<N>.json). Run systemTest/fixtures/provision-actors.ts for the slot "
            "with BOOTSTRAP_ADMIN_PASSWORD set, or restore the actors.superseded-* file if a run moved it aside."
        )
    # A login failure is an error too: the actor exists, so something is wrong and must be seen.
    return make_client(base_url, bearer=get_token(str(actor["email"]), str(actor["password"]), base_url))


@pytest.fixture(scope="module")
def owner(api_base_url: str) -> Generator[httpx.Client]:
    """The first generated OWNER actor, who creates every object under test."""
    client = _client_for("owner", api_base_url)
    yield client
    client.close()


@pytest.fixture(scope="module")
def peer(api_base_url: str) -> Generator[httpx.Client]:
    """The second generated OWNER actor, in the same tenant, who must not be served the owner's objects."""
    client = _client_for("ownerPeer", api_base_url)
    yield client
    client.close()


def _created_id(response: httpx.Response, expected: tuple[int, ...], pick: Callable[[dict[str, Any]], Any]) -> str:
    """The new object's id from a create response, failing LOUDLY (never as an xfail) on any other outcome."""
    assert response.status_code in expected, (
        f"could not create the object: {response.status_code} {response.text[:300]}"
    )
    return str(pick(response.json()["data"]))


def _owner_can_read(owner: httpx.Client, path: str) -> None:
    """Control: the creating user reads their own object (200). Without it a 404 for the peer proves nothing."""
    response = owner.get(path)
    assert response.status_code == 200, f"the owner cannot read their own object at {path}: {response.status_code}"


@pytest.fixture(scope="module")
def transfer_id(owner: httpx.Client) -> str:
    """A transfer the owner initiated. Both parties are throwaway uuids, so neither peer is a party to it."""
    body = {
        "documentId": _new_document_id(),
        "transferType": "simple",
        "currentOwnerId": "00000000-0000-4000-8000-000000000a01",
        "newOwnerId": "00000000-0000-4000-8000-000000000a02",
        "documentHash": secrets.token_hex(32),
        "documentTitle": "KS-1703 read test",
        "documentType": "contract",
    }
    created = _created_id(owner.post("/transfers", json=body), (201,), lambda d: d["id"])
    _owner_can_read(owner, f"/transfers/{created}")
    return created


@pytest.fixture(scope="module")
def delegation_id(owner: httpx.Client) -> str:
    """A delegation the owner granted to a throwaway delegate."""
    body = {"delegateId": "00000000-0000-4000-8000-000000000b01", "delegationType": ["full"]}
    created = _created_id(owner.post("/delegations", json=body), (201,), lambda d: d["delegation"]["id"])
    _owner_can_read(owner, f"/delegations/{created}")
    return created


@pytest.fixture(scope="module")
def export_id(owner: httpx.Client) -> str:
    """An analytics export the owner requested (the body shape the leg's sweep got a 202 for)."""
    body = {"format": "csv", "period": "all", "type": ""}
    created = _created_id(owner.post("/analytics/exports", json=body), (202,), lambda d: d["id"])
    _owner_can_read(owner, f"/analytics/exports/{created}")
    return created


@pytest.fixture(scope="module")
def participant_id(owner: httpx.Client) -> str:
    """A governance participant the owner registered with a unique wallet address."""
    body = {"walletAddress": f"addr_test1ks1703{secrets.token_hex(8)}", "stakedAmount": 0}
    created = _created_id(owner.post("/governance/participants/register", json=body), (201,), lambda d: d["id"])
    _owner_can_read(owner, f"/governance/participants/{created}")
    return created


@pytest.fixture(scope="module")
def audit_id(owner: httpx.Client) -> str:
    """An audit entry the owner wrote about themselves."""
    me = owner.get("/users/me")
    assert me.status_code == 200, f"cannot resolve the owner's identity: {me.status_code}"
    body = {"action": "read", "resourceType": "ks1703-read-test", "userId": str(me.json()["data"]["id"])}
    created = _created_id(owner.post("/security/audit", json=body), (201,), lambda d: d["id"])
    _owner_can_read(owner, f"/security/audit/{created}")
    return created


def _assert_peer_refused(peer: httpx.Client, path: str) -> None:
    """The finding: the second user must be refused, and is not."""
    response = peer.get(path)
    assert response.status_code in REFUSED, (
        f"{_TICKET}: a second same-tenant OWNER read {path} and got {response.status_code} "
        f"(expected {REFUSED}); body: {response.text[:200]}"
    )


class TestSecondUserCannotReadAnotherUsersObject:
    """The six routes ST402 found; each created by ``owner``, read by ``ownerPeer`` (KS-1703)."""

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_OPEN_DEFECT)
    def test_transfer_by_id(self, peer: httpx.Client, transfer_id: str) -> None:
        # Arrange: the owner's transfer (fixture). Act + Assert: the second user is refused.
        _assert_peer_refused(peer, f"/transfers/{transfer_id}")

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_OPEN_DEFECT)
    def test_transfer_history(self, peer: httpx.Client, transfer_id: str) -> None:
        # The history carries statusHistory, approvals and rejections.
        _assert_peer_refused(peer, f"/transfers/{transfer_id}/history")

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_OPEN_DEFECT)
    def test_delegation_by_id(self, peer: httpx.Client, delegation_id: str) -> None:
        # The list route of the same service already scopes by the authenticated caller; this read does not.
        _assert_peer_refused(peer, f"/delegations/{delegation_id}")

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_RULING_PENDING)
    def test_analytics_export_by_id(self, peer: httpx.Client, export_id: str) -> None:
        # The export type has no owner or tenant field, so entitlement needs a model decision first.
        _assert_peer_refused(peer, f"/analytics/exports/{export_id}")

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_RULING_PENDING)
    def test_governance_participant_by_id(self, peer: httpx.Client, participant_id: str) -> None:
        # A participant may be public by design (it is looked up by wallet address as well as id).
        _assert_peer_refused(peer, f"/governance/participants/{participant_id}")

    @pytest.mark.xfail(strict=True, raises=AssertionError, reason=_RULING_PENDING)
    def test_security_audit_entry_by_id(self, peer: httpx.Client, audit_id: str) -> None:
        # Tenant-scoped today (a foreign tenant gets 404). Whether one OWNER may read another's is the ruling.
        _assert_peer_refused(peer, f"/security/audit/{audit_id}")
