"""Pure helpers for the demo-seed gate suite (KS-502 §2 / KS-487 B-3).

WHY THIS EXISTS (KS-502). ``tests/test_seed_demo_gate.py`` was a ``skip`` written against the
pre-fix design, which would have gated ``POST /api/admin/seed-demo-users`` on ``NODE_ENV``. The
platform fix (KS-487 B-3, ``dc4fed788``) gates it on two explicit flags instead, which the
integration compose override CAN flip, so the gate is now testable on a local slot.

Platform facts these helpers encode (``services/originate``):

* ``utils/demoSeedGate.ts`` ``isDemoSeedEnabled`` — true only when ``ALLOW_DEFAULT_SEED_PASSWORDS``
  and ``ENABLE_DEMO_SEED`` are both the literal string ``'true'``.
* ``routes/adminConfig.ts`` — refused: ``403 {success: false, error: {code: 'DEMO_SEED_DISABLED'}}``;
  allowed: ``200 {success: true, seededUsers, created, alreadyPresent, failed}`` where an account that
  already exists is counted in ``alreadyPresent`` and left untouched (``ON CONFLICT (email) DO
  NOTHING``; before KS-487 B-3 it was ``DO UPDATE``, which reset the password and role).

Pure: no I/O, no httpx, no pytest. Covered by ``tests/unit/support/test_demo_seed_gate.py``.
"""

from dataclasses import dataclass
from typing import Any

# Relative to the /api-suffixed base URL; reached through the gateway's /api/admin proxy.
SEED_DEMO_PATH = "/admin/seed-demo-users"

# demoSeedGate.ts `DEMO_SEED_FLAGS`, in the same order.
DEMO_SEED_FLAGS: tuple[str, str] = ("ALLOW_DEFAULT_SEED_PASSWORDS", "ENABLE_DEMO_SEED")


@dataclass(frozen=True)
class SeedCounts:
    """The per-run account counts the seed endpoint reports.

    Attributes:
        created: Accounts inserted by this call.
        already_present: Accounts that existed and were left as they were.
        failed: Accounts whose insert raised.
    """

    created: int
    already_present: int
    failed: int

    @property
    def total(self) -> int:
        """Every account the handler attempted.

        Returns:
            ``created + already_present + failed``.
        """
        return self.created + self.already_present + self.failed


def seed_flag_env(*, allow_default_seed_passwords: bool, enable_demo_seed: bool) -> dict[str, str]:
    """Build the compose-override values for one gate leg.

    Both keys are ALWAYS set. KS-502: the slot-4 stack runs with ``ALLOW_DEFAULT_SEED_PASSWORDS=true``
    in its own env, so a key left out would inherit that value and a "both off" leg would silently be
    a "one on" leg.

    Args:
        allow_default_seed_passwords: Value for ``ALLOW_DEFAULT_SEED_PASSWORDS``.
        enable_demo_seed: Value for ``ENABLE_DEMO_SEED``.

    Returns:
        ``{flag: 'true' | 'false'}`` for both flags.
    """
    values = (allow_default_seed_passwords, enable_demo_seed)
    return {flag: "true" if on else "false" for flag, on in zip(DEMO_SEED_FLAGS, values, strict=True)}


def is_demo_seed_refusal(status: int, body: object) -> bool:
    """True only for originate's own gate refusal.

    A 403 from ``requireRole`` (wrong persona) has a different code and must not read as the gate
    holding — that would turn a broken precondition into a pass.

    Args:
        status: HTTP status.
        body: Parsed JSON body.

    Returns:
        True for ``403`` with ``error.code == 'DEMO_SEED_DISABLED'``.
    """
    error = body.get("error") if isinstance(body, dict) else None
    return status == 403 and isinstance(error, dict) and error.get("code") == "DEMO_SEED_DISABLED"


def _strict_int(value: Any) -> int | None:
    """Return ``value`` when it is a real int (``bool`` excluded), else None.

    Args:
        value: A JSON scalar.

    Returns:
        The int, or None.
    """
    return value if isinstance(value, int) and not isinstance(value, bool) else None


def parse_seed_counts(status: int, body: object) -> SeedCounts | None:
    """Parse a successful seed response into counts, strictly.

    Args:
        status: HTTP status.
        body: Parsed JSON body.

    Returns:
        :class:`SeedCounts` for a ``200 {success: true}`` body carrying all three integer counts;
        None for anything else — a missing count is never read as zero.
    """
    if status != 200 or not isinstance(body, dict) or body.get("success") is not True:
        return None
    created = _strict_int(body.get("created"))
    present = _strict_int(body.get("alreadyPresent"))
    failed = _strict_int(body.get("failed"))
    if created is None or present is None or failed is None:
        return None
    return SeedCounts(created=created, already_present=present, failed=failed)


def rerun_overwrote_nothing(first: SeedCounts, second: SeedCounts) -> bool:
    """True when a second seed run created nothing and found every account from the first.

    ``$executeRaw`` returns the affected row count: ``DO NOTHING`` gives 0 for an existing email, the
    pre-KS-487 ``DO UPDATE`` gave 1 — so an overwriting platform reports ``created > 0`` on the re-run.

    Args:
        first: Counts from the first call.
        second: Counts from the immediately following call.

    Returns:
        True when the re-run attempted the same non-zero number of accounts, created none, and
        counted every previously created or present account as already present.
    """
    return (
        first.total > 0
        and second.total == first.total
        and second.created == 0
        and second.already_present == first.created + first.already_present
    )
