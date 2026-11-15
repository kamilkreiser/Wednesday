"""Governance calls that build a capped slot on a live stack, for the KS-1762 live cap suite.

KS-1719's fix (PR #1687) frees the cap's ``active`` AND ``queued`` proposals, oldest first and only the
super-admin's own. It was proven live on one shape only — 20 ``active`` proposals from one proposer — so
this module builds the shapes that were not: a cap held partly by ``queued`` proposals, from two proposers.

How a proposal reaches ``queued`` without waiting out a voting period (``governanceService.ts`` on develop):

* ``submitProposal`` snapshots ``totalVotePower`` as the sum of every DRep's ``vote_power`` (L552-590).
* ``castVote`` finalises early once the remaining votes cannot change the outcome (L704-717), and
  ``finalizeProposal`` moves a passed proposal to ``queued`` (L724-760).
* So one DRep holding more than half the snapshotted power, voting ``for``, queues the proposal at once.

The voter is made that DRep through ``POST /governance/participants/register``: governance auto-registers a
proposer as a participant whose id AND wallet address are its user id (``createProposal`` L470-487), and
``registerParticipant`` updates the row it finds by wallet address, keeping that id (L380-416). The caller
records the participant first and restores it afterwards, so the slot's vote power is left as it was.

These helpers touch ``httpx``, so they live beside the suite, not in the transport-free ``tests/support``.
Ticket reference is the plain id ``KS-1762`` only - never a URL (systemTest rule).
"""

from typing import Any

import httpx

from tests.precondition_probes import _decode_body

# KS-1762: CreateProposalSchema needs a title >= 10 and a description >= 50 characters.
_PROPOSAL_DESCRIPTION: str = (
    "KS-1762 live cap proof: a proposal created only to fill the governance cap with a known mix "
    "of active and queued rows, cancelled again on teardown."
)

# KS-1762: RegisterParticipantSchema caps stakedAmount at 1e12. The largest stake gives the voter the
# largest vote power the platform allows, so it outweighs every other DRep on a slot not fuzzed to the cap.
_DREP_STAKE: int = 10**12


def _data(response: httpx.Response) -> Any:
    """Return the ``data`` member of a governance envelope, or the body itself when there is none.

    Args:
        response: A governance response.

    Returns:
        The decoded payload.
    """
    body = _decode_body(response)
    return body.get("data", body) if isinstance(body, dict) else body


def _expect(response: httpx.Response, action: str) -> Any:
    """Return the payload of a 2xx response, or fail with the status and body when it is anything else.

    Building the cap is the test's precondition, so a refusal here is reported as what it is, loudly,
    rather than leaving a half-built slot to be read as a finding about the helper.

    Args:
        response: The response to check.
        action: What was being done, for the failure message.

    Returns:
        The decoded payload.

    Raises:
        AssertionError: When the response is not 2xx.
    """
    assert response.is_success, f"KS-1762 setup: {action} returned HTTP {response.status_code}: {response.text[:200]}"
    return _data(response)


def user_id(client: httpx.Client) -> str:
    """Return the id of the user behind ``client`` (``GET /users/me``), which governance stores as ``proposerId``.

    Args:
        client: An authenticated client.

    Returns:
        The user id.
    """
    data = _expect(client.get("/users/me"), "GET /users/me")
    assert isinstance(data, dict), f"KS-1762 setup: /users/me answered no object: {data!r}"
    assert isinstance(data.get("id"), str), f"KS-1762 setup: /users/me carried no id: {data!r}"
    return data["id"]


def config_value(client: httpx.Client, key: str) -> int:
    """Return one positive integer from the platform's governance config (``GET /governance/config``).

    Read live so no test types the platform's numbers (``maxActiveProposals``, ``minProposalStake``).

    Args:
        client: An authenticated client.
        key: The config key.

    Returns:
        The value.
    """
    data = _expect(client.get("/governance/config"), "GET /governance/config")
    value = data.get(key) if isinstance(data, dict) else None
    assert isinstance(value, int), f"KS-1762 setup: /governance/config carried no integer {key}: {data!r}"
    assert value > 0, f"KS-1762 setup: /governance/config carried a non-positive {key}: {data!r}"
    return value


def cap_size(client: httpx.Client) -> int:
    """Return the platform's ``maxActiveProposals``, the cap these tests fill.

    Args:
        client: An authenticated client.

    Returns:
        The cap.
    """
    return config_value(client, "maxActiveProposals")


def other_dreps(client: httpx.Client, own_id: str) -> list[dict[str, Any]]:
    """List every DRep on the slot except ``own_id`` (``GET /governance/participants?isDRep=true``).

    ``queue`` needs the voter to hold more than half the DRep vote power. A sweep fuzzes
    ``POST /governance/participants/register`` with stakes up to the schema's 1e12, so a slot that has
    hosted one can hold DReps the voter cannot outweigh.

    Args:
        client: An authenticated client.
        own_id: The voter's participant id, left out of the list.

    Returns:
        The other DReps' rows.
    """
    data = _expect(client.get("/governance/participants", params={"isDRep": "true"}), "listing DReps")
    assert isinstance(data, list), f"KS-1762 setup: the DRep listing held no list: {data!r}"
    return [row for row in data if isinstance(row, dict) and row.get("id") != own_id]


def counted(client: httpx.Client, *, status: str = "active,queued") -> list[dict[str, Any]]:
    """List the proposals in ``status`` (by default the two the cap counts), across every proposer.

    Args:
        client: An authenticated client.
        status: The list route's comma-separated status filter.

    Returns:
        The proposal rows.
    """
    data = _expect(client.get("/governance/proposals", params={"status": status}), f"listing {status} proposals")
    assert isinstance(data, list), f"KS-1762 setup: the proposal listing held no list: {data!r}"
    return data


def create_draft(client: httpx.Client, label: str) -> str:
    """Create a ``general`` draft proposal as the user behind ``client`` and return its id.

    Args:
        client: The proposer's client.
        label: Distinguishes the proposal's title in the database.

    Returns:
        The new proposal's id.
    """
    payload = {"title": f"KS-1762 cap fill {label}", "description": _PROPOSAL_DESCRIPTION, "category": "general"}
    data = _expect(client.post("/governance/proposals", json=payload), f"creating proposal {label}")
    return str(data["id"])


def submit(client: httpx.Client, proposal_id: str) -> None:
    """Submit a draft, which makes it ``active`` and snapshots the DRep vote power.

    Args:
        client: The proposer's client (submit is proposer-only).
        proposal_id: The draft's id.
    """
    _expect(client.post(f"/governance/proposals/{proposal_id}/submit"), f"submitting {proposal_id}")


def vote_for(client: httpx.Client, proposal_id: str) -> None:
    """Vote ``for`` a proposal as the user behind ``client``, who must be a DRep.

    Args:
        client: The voter's client.
        proposal_id: The active proposal's id.
    """
    _expect(client.post(f"/governance/proposals/{proposal_id}/vote", json={"vote": "for"}), f"voting on {proposal_id}")


def status_of(client: httpx.Client, proposal_id: str) -> str:
    """Return a proposal's current status.

    Args:
        client: An authenticated client.
        proposal_id: The proposal's id.

    Returns:
        The status string.
    """
    data = _expect(client.get(f"/governance/proposals/{proposal_id}"), f"reading {proposal_id}")
    return str(data["status"])


def cancel(client: httpx.Client, proposal_id: str) -> int:
    """Cancel a proposal as the user behind ``client``, best effort, and return the status code.

    A proposal that is already cancelled answers 409, which still means the slot is free.

    Args:
        client: The proposer's client.
        proposal_id: The proposal's id.

    Returns:
        The HTTP status of the cancel.
    """
    return client.post(f"/governance/proposals/{proposal_id}/cancel").status_code


def participant(client: httpx.Client, participant_id: str) -> dict[str, Any] | None:
    """Return a governance participant by id, or ``None`` when there is none.

    Args:
        client: An authenticated client.
        participant_id: The participant's id (a proposer's user id).

    Returns:
        The participant row, or ``None``.
    """
    response = client.get(f"/governance/participants/{participant_id}")
    if response.status_code == 404:
        return None
    data = _expect(response, f"reading participant {participant_id}")
    return data if isinstance(data, dict) else None


def register(client: httpx.Client, wallet_address: str, *, staked_amount: int, is_drep: bool) -> None:
    """Register or update the participant whose wallet address is ``wallet_address``.

    Args:
        client: An authenticated client.
        wallet_address: The participant's wallet address (a proposer's user id).
        staked_amount: The stake to record.
        is_drep: Whether the participant may vote.
    """
    body = {"walletAddress": wallet_address, "stakedAmount": staked_amount, "isDRep": is_drep}
    _expect(client.post("/governance/participants/register", json=body), f"registering participant {wallet_address}")


def make_dominant_drep(client: httpx.Client, wallet_address: str) -> None:
    """Make the participant the DRep holding the most vote power the platform allows.

    Args:
        client: An authenticated client.
        wallet_address: The participant's wallet address (its user id).
    """
    register(client, wallet_address, staked_amount=_DREP_STAKE, is_drep=True)


def queue(proposer: httpx.Client, voter: httpx.Client, proposal_id: str) -> None:
    """Drive a draft to ``queued``: submit it, then vote it through as the dominant DRep.

    Args:
        proposer: The proposer's client.
        voter: The dominant DRep's client.
        proposal_id: The draft's id.

    Raises:
        AssertionError: When the vote did not finalise the proposal into ``queued``.
    """
    submit(proposer, proposal_id)
    vote_for(voter, proposal_id)
    reached = status_of(voter, proposal_id)
    assert reached == "queued", (
        f"KS-1762 setup: the vote left {proposal_id} {reached!r}, not 'queued' - the voter does not hold "
        "more than half the vote power snapshotted at submit (another DRep on this slot outweighs it)"
    )
