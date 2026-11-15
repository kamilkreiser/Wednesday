"""Functional tests pinning the KS-406 auth-first-401 posture in schemathesis.toml.

The platform answers an HTTP method an endpoint does not declare with 401 (auth runs
before routing) rather than RFC 9110's 405 + Allow — a deliberate decision (KS-406,
Kam 2026-07-08) so the method surface is not revealed to unauthenticated callers.
schemathesis.toml expresses that by setting ``[phases.coverage] unexpected-methods = []``,
which stops the coverage phase generating undeclared-method probes (they failed
``unsupported_method`` on every authenticated route by design — 228 findings, 100% of
the 2026-07-07 sweep's failures). These tests make removing or mistyping that key a
red test rather than a silent 228-failure regression on the next sweep.
"""

from schemathesis.config import SchemathesisConfig
from schemathesis.config._projects import ProjectConfig

from scripts.runner.config import PROJECT_ROOT

SCHEMATHESIS_TOML_PATH = PROJECT_ROOT / "schemathesis.toml"


def _load_project_config() -> ProjectConfig:
    """Parse schemathesis.toml the same way the CLI does at startup.

    Returns:
        The default ProjectConfig resolved from this repo's schemathesis.toml,
        carrying the [phases.coverage] configuration under test.
    """
    return SchemathesisConfig.from_path(SCHEMATHESIS_TOML_PATH).projects.get_default()


def test_unexpected_method_probes_are_disabled() -> None:
    """Verify the parsed config generates NO undeclared-method coverage probes (KS-406)."""
    # Parse with the real CLI config loader — a typo'd section/key would silently fall
    # back to the default probe set, so assert on the *parsed* value, not the raw text.
    coverage = _load_project_config().phases.coverage
    assert coverage.unexpected_methods == set(), (
        "schemathesis.toml must set [phases.coverage] unexpected-methods = [] — "
        "auth-first 401 on undeclared methods is the intended posture (KS-406); "
        "restoring the probes re-fails `unsupported_method` on every authenticated route."
    )


def test_coverage_phase_itself_stays_enabled() -> None:
    """Verify disabling the probes did not disable the whole coverage phase."""
    # The posture decision removes ONE scenario family; the rest of the coverage
    # phase (boundary values, duplicate params, missing headers) must keep running.
    assert _load_project_config().phases.coverage.enabled is True
