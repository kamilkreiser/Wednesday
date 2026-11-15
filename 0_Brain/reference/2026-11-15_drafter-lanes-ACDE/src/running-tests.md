# Running Tests

Comprehensive guide to running Schemathesis test sweeps, test strategies, authentication, and troubleshooting.

---

> **A LOCAL run must name its slot (KS-1016, 2026-09-11; KS-1386, 2026-09-29).** Every harness — Schemathesis, k6,
> Playwright, Akto and the shared provisioning step — refuses to start against a **local** target
> (`localhost`, `127.0.0.1`, `[::1]`, `host.docker.internal`) when neither `SECUURA_STACK_SLOT` nor
> the platform-s alias `STACK_SLOT` is set, and prints the command to run instead. There is no
> default URL either (KS-1386): with no slot and no `SECUURA_BASE_URL`/`API_BASE_URL` the run is
> refused, CI included.
>
> ```text
> No stack slot named. Every LOCAL system-test run must say which Docker stack it targets
> (target: …). Name the slot and run again, for example:
>   SECUURA_STACK_SLOT=<n> python3 scripts/run.py pr
>   or: systemTest/run-in-slot.sh <n> python3 scripts/run.py pr
> ```
>
> **Local only.** A remote target (demo, a tunnel) carries no slot and is left alone, and CI is
> exempt because its isolated per-suite stacks are local by construction and deliberately unslotted
> (GitHub Actions sets `CI=true`; the exemption is a convention, not a lock). Before this rule an
> unset slot meant slot 1 silently — another ticket's stack on a shared machine.

## Test Commands

### Command reference

The complete `python3 scripts/run.py <command>` set — all run from `systemTest/schemathesis/`.
The runner + `config/schemathesis_tests.yaml` are the source of truth (`python3 scripts/run.py -h`).

The tables below list command names only. Every command that reaches a stack is run with the slot
named — `SECUURA_STACK_SLOT=1 python3 scripts/run.py <command>` — and that is every command here
except `update-deps`, `quality:static` and `report` (`setup`/`install` log in to mint the API token,
and `quality` can reach a stack through its integration leg, so both are refused without a slot).
Replace `1` with your stack slot; a local run that names no slot is refused (KS-1386).

**Setup & maintenance**

| Command                   | What it does                                                                 |
| ------------------------- | ---------------------------------------------------------------------------- |
| `setup` (alias `install`) | One-shot first-time: venv + deps + `.env` files + API token (needs Docker)   |
| `update-deps`             | Upgrade venv deps to the latest allowed by `pyproject.toml`, report outdated |

**Quality gate**

| Command          | What it does                                                                                                                                |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `quality`        | Full gate — format + lint + type-check + unit tests + coverage gate + integration (when token + platform) + pip-audit. Run on every change. |
| `quality:static` | Same gate **minus** the pytest suites (static checks + pip-audit only) — the PR CI path                                                     |

**Reporting**

| Command                    | What it does                                                      |
| -------------------------- | ----------------------------------------------------------------- |
| `report`                   | Regenerate the HTML report from existing output files (no re-run) |
| `report --input-dir <dir>` | Regenerate from a named run directory                             |

**Test profiles** (property sweeps — each also writes the HTML report)

| Command               | Scope                                                                                                                                                                                                                                                                                                            |
| --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pre-merge`           | PR/pre-merge gate — 6 examples/op, ~6.5 min (the CI pre-merge tier)                                                                                                                                                                                                                                              |
| `full` (alias `test`) | On-demand — 25 examples/op; also runs the IDOR suite. **~11.8 min of sweep, ~17.4 min wall-clock for the whole command** (KS-1408, this Mac, 2026-10-05); 19.6 min at 4.29.3 and 20.9 / 20.3 min at 4.29.4 on 2026-10-07 (KS-1439, slot 4, other sessions' stacks up, so not like-for-like) — see the note below |
| `nightly`             | Scheduled soak — 1100 examples/op, ~4 hrs                                                                                                                                                                                                                                                                        |
| `test-fast`           | Quick validation — 6 examples/op, ~1–2 min, minimal checks                                                                                                                                                                                                                                                       |
| `pr`                  | PR-profile sweep — 5 examples/op, ~1 min (moved off the PR gate to pre-merge)                                                                                                                                                                                                                                    |
| `local-debug`         | Quick debugging — 4 examples/op, ~2–3 min (swap `--mode` as needed)                                                                                                                                                                                                                                              |
| `auth-rate-limited`   | Rate-limited auth-only sweep — 2 examples/op (KS-270)                                                                                                                                                                                                                                                            |

**Anchoring-integrity Integration mode** (co-located suite, KS-489-D / KS-492 — not a separate project)

| Command       | What it does                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `integration` | Live orchestrated anchoring-integrity tests — `tests/integration/` only (anchor fabrication / mock-TSA fail-closed + anchor-verify-vs-chain). Flips stack env / stops services, so it runs isolated from the property sweep (needs Docker + the stack), then regenerates the report with the anchoring tabs. **The report opens on Overview, which is a sweep tab and is empty for this command — this run's results are in the three `Anchoring …` tabs.** Until KS-519 the command produced no report at all (the generator required sweep artefacts it never writes), and then briefly produced one whose landing tab claimed "✓ All checks passed" over zero executed cases. |

The offline anchoring **unit** tests run inside `quality` (coverage-gated). The suite **also runs
inside `pre-merge` / `full` / `nightly`** as its own isolated pytest invocation (before the sweep),
gating that profile's exit code; the profile report then folds in the anchoring tabs. A normal sweep
with no anchoring `results.json` renders a byte-for-byte unchanged report.

**KS-608 — status agreement (`tests/integration/test_anchor_status_agreement.py`).** Two invariants
over anchors this persona can reach:

- `anchor_status_verify_vs_anchor_read` — for each document, verify is called once and the anchor it
  names (`blockchain.anchorId`) is read once from `GET /api/anchors/{id}`; the two must not make
  opposing terminal claims (confirmed vs failed). Scoped to the anchor id, not the document, on
  Kamil's KS-607 answer. Runs in both anchoring modes. **Not read-only:** it creates one document so
  it always has a subject, and verify itself can write a healed blob back (KS-584
  `persistHealedAnchor`). Only pairs where both sides are terminal are judged; the rest (in flight,
  no anchor named, non-anchor id, anchor 404) are counted and reported, and zero judged pairs fails.
- `anchor_status_chain_evidence_not_failed` — an anchor with a real 64-hex hash and a block number
  must not read `failed` (Kamil, KS-607). Read-only (lists and reads anchors, creates nothing). Needs
  real anchoring, so it is **OUT OF SCOPE (mode)** on a local, mock-anchoring stack (KS-535) and is
  exercised against demo.

Neither decides which endpoint is authoritative; that is KS-607.

**Test categories** (from `config/schemathesis_tests.yaml`)

| Command                 | Covers                                            |
| ----------------------- | ------------------------------------------------- |
| `contract_schema`       | Schema validation, status codes, headers          |
| `data_generation`       | Happy path, fuzzing, negative testing, boundaries |
| `stateful_workflows`    | POST→GET→DELETE chains, operation linking         |
| `security_auth`         | Auth scenarios, IDOR, RBAC                        |
| `reliability_stability` | Server-error detection, input handling, timeouts  |

**CLI overrides** (apply to profiles & categories): `--workers=N`, `--mode <mode>` (for `local-debug`),
`--input-dir <dir>` (for `report`), `--seed <int>` (fix the seed), and the reproducibility-set flags
`--repeat N`, `--no-isolate`, `--compare <set>` (KS-1680, below).

**Direct pytest** (bypass the runner, for the offline/integration suites):

```bash
python3 -m pytest tests/unit/ -q     # offline unit suite (no platform/token)
SECUURA_STACK_SLOT=1 python3 -m pytest tests/ -q          # full live integration suite (needs platform + creds)
```

The prose below expands on the most-used commands.

### Full & Quick Sweeps

```bash
# Full sweep (alias: `test`) — all 4 phases, 25 examples/operation, 12 workers.
# ~17.4 min wall-clock end to end on this Mac (KS-1408, 2026-10-05, Schemathesis 4.29.3, slot 4); the
# ~11.8 min figure is the sweep phase alone and excludes the four pytest suites `full` runs first.
# (At 4.28.0 the same stack took 23.1 min / 17.3 min sweep — 4.29 generates ~31% fewer cases.)
# KS-1439, 2026-10-07, slot 4, seed 1439, other sessions' stacks up: 19.6 min at 4.29.3; 20.9 and 20.3 min at 4.29.4.
# KS-1455, 2026-10-09, slot 4, seed 1455, 4.30.0: 19.7 min wall (sweep 12.0 min), 17,497 cases, 100 unique failures, 0 errored.
# KS-1476, 2026-10-12, slot 3, seed 1476: 4.30.0 20.1 min (17,839 cases, 104 unique); 4.30.1 19.8 min (sweep 12.1, 17,439, 95);
#   4.30.1 + hypothesis 6.169.0 on develop aa9ca9de9 20.1 min (sweep 12.0, 17,523, 101). `pr` 1.7 min, 2,219 cases, 9 unique.
# KS-1478, 2026-10-14, slot 1, NO fixed seed: 4.31.0 + hypothesis 6.169.1 on develop 3c0a52221 — full 21.2 min (sweep 12.3,
#   17,636 cases, 100 unique); pre-merge 15.2 min (11,351, 90); `pr` 1.8 min, 2,253 cases, 9 unique. Not comparable to the seeded rows.
# KS-1615, 2026-10-15, slot 1 of the Mac, NO fixed seed, Schemathesis 4.31.1, Node 24.22.0 LTS, Python 3.14.8, develop 0bb4f17ca + branch: `pr` (cold) engine 92 s, wrapper 126 s, 8 unique failures;
#   pre-merge engine 470 s, wrapper 15 m 58 s, 93 unique; full engine 725 s (12.1 min), wrapper 20.1 min, 94 unique.
#   Sequencing caveat: a first `pr` run straight after the Akto security scan took 433 s engine / 14 m 34 s with 15 read timeouts and one event_loop_lag 503 —
#   load from running back-to-back, not the tool. Run one suite at a time and let the stack settle.
# Name the SAME SECUURA_TICKET for `setup` and the sweep: a mismatch skipped the IDOR + integration suites on the first run.
# Runs the TestGdprOwnershipGuard IDOR regression (KS-258) FIRST, then the sweep, and
# surfaces the IDOR results in the GDPR IDOR tab of the HTML report.
SECUURA_STACK_SLOT=1 python3 scripts/run.py full

# Pre-merge gate — the faster cut of full: identical checks + 4 phases + IDOR suite,
# 6 examples/operation (~6 min). This is what the pre-merge CI tier runs.
SECUURA_STACK_SLOT=1 python3 scripts/run.py pre-merge

# PR gate — read-only checks, 5 examples (~1 min).
SECUURA_STACK_SLOT=1 python3 scripts/run.py pr

# Fast sweep — 6 examples, 12 workers (~1-2 min). Does NOT run the IDOR suite
# (only pre-merge, full, nightly, and test do).
SECUURA_STACK_SLOT=1 python3 scripts/run.py test-fast

# Overnight soak — 1100 examples (~4 hrs); same checks/phases as full.
SECUURA_STACK_SLOT=1 python3 scripts/run.py nightly

# Auth-only, low-frequency fuzz of /api/auth/* — 2 examples (~2 min; KS-270).
SECUURA_STACK_SLOT=1 python3 scripts/run.py auth-rate-limited
```

### Targeted Sweeps by Category

Category names come from `schemathesis_tests.yaml` (see `python3 scripts/run.py -h`):

```bash
# Happy path, property-based fuzzing, negative testing, boundaries
SECUURA_STACK_SLOT=1 python3 scripts/run.py data_generation

# Auth scenarios, IDOR, RBAC — includes the TestGdprOwnershipGuard IDOR regression
# for KS-228. Requires two seed users (issuer@secuura.com, verifier@secuura.com);
# tokens resolve automatically, or pre-generate with `SECUURA_STACK_SLOT=1 python3 scripts/setup.py --idor-tokens` (KS-258).
SECUURA_STACK_SLOT=1 python3 scripts/run.py security_auth

# Schema validation, status codes, headers
SECUURA_STACK_SLOT=1 python3 scripts/run.py contract_schema

# Stateful workflows — POST→GET→DELETE chains, operation linking, idempotency
# (idempotency is coverage: PARTIAL — see "Coverage Levels" below)
SECUURA_STACK_SLOT=1 python3 scripts/run.py stateful_workflows

# Error handling, input rejection, timeout/hang detection
SECUURA_STACK_SLOT=1 python3 scripts/run.py reliability_stability
```

### The Test Suites (pytest)

Two suites run **offline** — no platform, no token — so together they are the fastest check that
a checkout is healthy. The integration suite drives the live API and needs the platform + a token.

- `tests/unit/` — unit tests of Python modules, grouped by subject: `report/`, `runner/`,
  `api_config/`, `checks/`.
- `tests/functional/config/` — contract tests of _this repo's configuration_
  (`config/schemathesis_tests.yaml`, `schemathesis.toml`) against the installed Schemathesis.
  They import `schemathesis` only as the source of truth for its check/phase/warning registries;
  the subject under test is our YAML/TOML, not the library — which is why they are functional
  tests of configuration rather than unit tests of a module.

```bash
# Both offline suites — the coverage gate spans them (~516 tests, a few seconds)
python3 -m pytest tests/unit/ tests/functional/ -q

# Full integration suite — live API journeys (needs docker compose up + a token)
SECUURA_STACK_SLOT=1 python3 -m pytest tests/ -q

# KS-478 state-machine / precondition suite alone (§11 — live; also runs standalone inside
# pre-merge/full/nightly with its own Preconditions report tab)
SECUURA_STACK_SLOT=1 python3 -m pytest tests/test_state_machine_preconditions.py -q

# KS-1762 live governance-cap proof — OPT-IN and DESTRUCTIVE: fills the slot's governance cap with a
# mix of active and queued proposals from two proposers, then cancels them. Never part of a profile,
# a sweep or the quality gate. Run it alone, through run.py, on a slot of your own with no active or
# queued proposals and no DRep but the super-admin (one no sweep has run on, or after --fresh-db), with
# BOOTSTRAP_ADMIN_PASSWORD (the slot's ADMIN_USER_PASSWORD) exported. run.py provisions the generated
# actors first, writes the suite's JUnit into the run directory and renders the HTML report with a
# Governance cap tab (console = JUnit = HTML report). Exit 0 only when every test ran and passed.
systemTest/run-in-slot.sh 1 python3 scripts/run.py governance-cap
# A bare pytest still works but bypasses provisioning and the report: after a --fresh-db the generated
# actor manifest names users that no longer exist, so every test 401s at login (measured KS-1762).

# A single file or test
python3 -m pytest tests/unit/report/test_panels_core.py -q
python3 -m pytest tests/unit/report/test_parsing_openapi.py -k Coverage -q
```

**Coded-regression suites (KS-492 / Review G).** Alongside the GDPR IDOR suite, the KS-478
`tests/test_state_machine_preconditions.py` suite drives the ten KS-466 §11 state-machine /
precondition operations to their unmet precondition and asserts each refusal is a clean,
enveloped business 4xx (never a raw 5xx / silent 2xx). Like IDOR it runs **standalone** before the
sweep (`run_pytest_preconditions` in `scripts/runner/pytest_suites.py` → `pytest-preconditions-output.xml`), **gates the profile exit
code**, and surfaces in a dedicated **Preconditions** report tab. A vector the target cannot satisfy
(unconfigured provider 503, unseeded/collided auth) **skips — and a skip is NOT a pass** (KS-478
red→green rule): any skip drops the suite to **INCOMPLETE** (amber `pill-s`) and **fails the gate**,
because an un-exercised op cannot verify its refusal. The console/report show `N of 10 ops
exercised`. Close a skip by provisioning the persona/provider so the op runs, or promote a genuinely
unprovisionable vector to an explicit `pytest.xfail(reason=…)` — never leave it a bare skip.

**`OUT OF SCOPE` — the one outcome that is neither (KS-519).** A fifth badge sits alongside PASS /
FAIL / SKIP / KNOWN FAILURE, for a scenario the _target_ cannot contain rather than one the harness
failed to provision: the anchoring suite's `test_revoked_document_does_not_verify` needs a real
on-chain anchor, and local anchoring is mock **by design** since KS-535. It is excluded from the
gate and printed with its reason, because failing on it would red the local suite on every run —
and a permanently-red gate is not consulted, which loses the same signal a silent pass would.
Recognised only by the `OUT_OF_SCOPE_SKIP_PREFIX` constant, so an ordinary `pytest.skip("…")` still
reds; and a run that exercised **nothing** fails regardless, so the exclusion can never empty a
suite quietly. Full rules in `known-issues-and-baseline.md`.

**The combined run banner covers every gate (KS-571, reversing KS-684).** `Combined Test Results` lists the
sweep, IDOR, the three gated suites, authenticated coverage and each post-run gate (run validity, NDJSON
completeness, reconciliation, console vs verdict (KS-1439), baseline — `NOT EVALUATED` only when the run is invalid or its
NDJSON incomplete, KS-752), and
`OVERALL` is the AND of all of them. When the gated trio could not run at all (no credentials, platform not
answering) its rows read `SKIPPED` with the reason **and still count toward `OVERALL`**, as they count toward
the exit code — KS-684 had excluded them, which printed `OVERALL: PASSED` over an exit code of 1.
(`scripts/runner/suite_gates.py::log_combined_status`.)

**Console vs verdict (KS-1439).** From Schemathesis 4.29.4 an errored case (a network error, a crashed check) is
counted as `errored`, not `skipped`, and the console prints it as its own clause
(`17592 generated, 115 found 121 unique failures, 1 errored, 431 skipped`). The gate holds the console's four counts
(generated, unique failures, errored, skipped) equal to `schemathesis-output.json`'s `test_cases`
(`generated`, `unique_failures`, `errored`, `without_checks`) — the JSON is what the report's Verdict section renders,
so this is the leg that keeps console = Schemathesis results = HTML report true for those counts. A verdict with no
`test_cases.errored` (a pre-4.29.4 writer) is a failure, not a pass. **It, reconciliation and the triaged baseline now run on every valid run, a failed sweep
included (KS-752)**; before, they read `NOT EVALUATED` once the sweep failed. To re-run it by hand against
a run directory:

```bash
cd systemTest/schemathesis
PYTHONPATH=. venv/bin/python3 - <<'EOF'
from pathlib import Path
from scripts.runner.report_reconciliation import check_console_matches_verdict, parse_console_totals
run = Path("output/reports/<run-directory>")
print(check_console_matches_verdict(parse_console_totals(run / "schemathesis-console.txt"), run / "schemathesis-output.json"))
EOF
```

### Code Quality (the comprehensive gate — run on EVERY change)

```bash
# THE gate. Run after any change, before every commit. Must end with "All quality checks passed!"
SECUURA_STACK_SLOT=1 python3 scripts/run.py quality
```

`quality` is a single comprehensive command that:

- auto-fixes formatting, import order and lint (all **Ruff**: `ruff format` then `ruff check --fix`; black and isort were removed 2026-07-24) across **`src/`, `tests/`, `scripts/`, and `config/`** (the live hook modules — KS-425),
- type-checks with **MyPy** (production code, the runner, and the `config/` hooks),
- runs the **offline unit suite with the coverage gate** (`pytest tests/unit/ tests/functional/`, fails below **90%**), and
- runs the **integration suite** (`pytest tests/`) **only** when `API_TOKEN` (or
  `API_EMAIL`/`API_PASSWORD`) is set and the platform is reachable — otherwise it is
  **skipped, not failed**, so the gate stays runnable offline.

`quality` auto-fixes formatting and lint; for a granular/direct run, call the venv tools yourself:

```bash
venv/bin/ruff format src tests scripts config          # Format
venv/bin/ruff check src tests scripts config --fix     # Import order + lint, incl. the S security rules (auto-fix)
venv/bin/mypy src/html_report             # Type-check the report code
```

### Help & Information

```bash
# List all available commands
python3 scripts/run.py -h
```

---

## Schemathesis Version Compatibility Tests (checks & phases)

`config/schemathesis_tests.yaml` declares Schemathesis `--checks` and `--phases` values by
name, and `schemathesis.toml` declares a `[warnings] fail-on` list (KS-226) — all three are
just strings until the CLI parses them, so a Schemathesis upgrade that renames or removes one
would otherwise only surface as a `--checks: invalid choice` failure the next time a sweep
runs, and a newly-added check/phase could go unused indefinitely with nobody noticing.

Two offline **functional** modules — they test the config files, not Schemathesis — guard against
both failure modes automatically, on every run of
`pytest tests/unit/ tests/functional/` / `python3 scripts/run.py quality` — no manual `--help` diff or changelog
read is required day-to-day:

- **`tests/functional/config/test_schemathesis_checks_compatibility.py`** — validates every check name in
  `config/schemathesis_tests.yaml` (`harness.default_checks`, every profile's `checks` list,
  every `test_categories` entry's `flags.checks`) against `schemathesis.checks.CHECKS`, the
  installed package's own check registry. Also validates `schemathesis.toml`'s
  `[warnings] fail-on` list against `schemathesis.core.warnings.SchemathesisWarning`.
- **`tests/functional/config/test_schemathesis_phases_compatibility.py`** — same idea for `flags.phases`
  values, validated against `schemathesis.config._phases.PhasesConfig`'s dataclass fields.

Each module asserts **both directions**:

1. Every check/phase/warning referenced in the config is one the installed Schemathesis
   version actually recognises (catches a rename or removal in a version bump).
2. Every check/phase/warning the installed version supports is referenced _somewhere_ in the
   config (catches a newly-added one that hasn't been triaged into a profile yet).

If a Schemathesis upgrade trips test (2), decide whether to adopt the new check/phase (wire it
into the relevant profile(s) in `config/schemathesis_tests.yaml`) or leave it out deliberately
and adjust the test with a documented reason. See `CLAUDE.md` → Schemathesis for the full
version-bump workflow these tests are part of.

> **Custom checks are not listed in the yaml.** Our own checks — `integration_5xx_guard` (KS-268),
> `public_operation_auth_conformance` (KS-425), `control_byte_acceptance_guard` (KS-472,
> hard gate — it raises on an accepted control byte, and stays red until the platform's shared-base
> rejection lands), `by_design_input_tolerance_guard` (KS-662) and `by_design_501_guard` (KS-686 —
> tolerates only the ruled 501 `NOT_IMPLEMENTED` envelope on `POST /api/wallets/verify` until KS-627
> lands; `tests/test_wallet_verify_stub.py` is its expiry tripwire), all in `config/checks.py` — self-register via the `@schemathesis.check` decorator
> when the hooks load, and gate per-operation in the check body rather than via `--checks` selection.
> Test (2) deliberately filters them out by `__module__`, so adding a custom check needs **no**
> `config/schemathesis_tests.yaml` entry. See the per-tool audit in
> [how-to-test-secuura.md](../../docs/how-to-test-secuura.md) → Spec Consumption by Tool.

> **KS-492 (Review G) security regressions.** Integration tests in `tests/` verify Platform-K
> security findings so posture can't silently regress; they run in the pre-merge/nightly integration
> suite alongside `TestGdprOwnershipGuard`. Unfixed platform findings are marked as a **Known Failure**
> (recorded as a pytest `xfail(strict=True)`) / `skip` so they document the vuln without red-ing the
> gate and auto-flip when the fix lands (a Known Failure that passes becomes an **Unexpected Pass** — a
> pytest `xpass` — the signal to flip the marker to a hard assertion):
> `test_notification_bola.py` (KS-486-A, Known Failure), `test_webhook_ssrf.py` (KS-487-B — a passing
> literal/scheme guard + a DNS-rebind Known Failure + a send-time/m365 `skip`),
> `test_wallet_verify_stub.py` (KS-488-C, Known Failure), `test_kyc_callback_auth.py`
> (KS-488-C, passing api-key guard), `test_m365_callback_redirect.py` (KS-1641 — the public m365
> OAuth callback's redirect target and reflected `error_description`; seven of its ten cells are
> **hard failures, not Known Failures**, by Peter's ruling of 2026-10-26, and stay red until the
> platform fix lands (one is the nginx edge answering 502 to a long astral description); three
> controls pass — see
> [known-issues-and-baseline.md](known-issues-and-baseline.md) → *KS-1641*). KS-502 (2026-10-06) replaced the two remaining environment skips
> with orchestrated tests in `tests/integration/` (run by `run.py integration`, not here):
> `test_seed_demo_gate.py` (KS-487 B-3 — originate recreated per flag pair; both-off / allow-only /
> enable-only → 403 `DEMO_SEED_DISABLED`, both-on → 200 and a re-run overwrites nothing) and
> `test_billing_webhook_idempotency.py` (KS-488 C-4 — billing recreated with a test-generated
> `STRIPE_WEBHOOK_SECRET`; signed first delivery processed, redelivery acknowledged as duplicate with
> the `webhook_events` row unchanged, and with billing's `DATABASE_URL` unresolvable every delivery
> refused 503).

---

## The Schemathesis CLI parameter surface (KS-544)

Every applicable `schemathesis run` option is **declared configuration**, not a value defaulted by
omission. Before KS-544 the runner passed roughly 20 of the ~45 available options and left the rest
unset, with no record of whether each had been considered and rejected or simply never noticed.

**Where each thing lives:**

| Concern                                                | Location                                                                      |
| ------------------------------------------------------ | ----------------------------------------------------------------------------- |
| Defaults + the reason for each                         | `config/schemathesis_tests.yaml` → `harness.execution` / `harness.generation` |
| Flags deliberately **not** adopted, with a reason each | `config/schemathesis_tests.yaml` → `harness.deliberately_unused_flags`        |
| Per-profile overrides                                  | each profile's `flags:` block                                                 |
| Resolution (harness default → profile override)        | `scripts/runner/run_options.py`                                               |
| Emission into the argv                                 | `scripts/runner/args_builder.py`                                              |

A flag missing from the generated command line is therefore either listed under
`deliberately_unused_flags` with a reason, or it is a bug — `tests/unit/runner/test_args_builder.py`
asserts both directions against the real yaml, so a config-only regression fails the offline gate.

### Tests always continue on failure

`--continue-on-failure` is emitted on **every** run and is deliberately **not** a yaml key: it is
the `CONTINUE_ON_FAILURE` constant in `run_options.py`, so no profile can switch it off. Without it
a scenario stops at its first failing case, so every later case in that scenario never executes —
and in the HTML report those cells are blank, which reads as "passed" rather than "never ran". A
truncated run is not a result. `--max-failures` is supported by the emitter but never set, for the
same reason. See `systemTest/CLAUDE.md` → MUST #12, which applies this to all four suites.

### What the sweep's exit code means (KS-1408)

Schemathesis 4.29.0 changed its exit codes. The runner classifies the code once
(`src/sweep_outcome.py`) and the console `Status:` line, `schemathesis-results.json`
(`summary.status`, `summary.schemathesis_exit_code`, `summary.status_meaning`) and the HTML
report's Verdict section (**Outcome** row) all render that one classification:

| Exit  | Outcome         | Meaning                                                                                              |
| ----- | --------------- | ---------------------------------------------------------------------------------------------------- |
| 0     | **PASSED**      | No failures.                                                                                         |
| 1     | **FAILED**      | Failures found — triage them in the report.                                                          |
| 2     | **INVALID**     | Nothing was tested, or a schema / configuration / internal error stopped the run. Nothing to triage. |
| 124   | **TIMED OUT**   | The harness's own wall-clock limit stopped the sweep; the counts describe a partial run.             |
| 130   | **INTERRUPTED** | Ctrl+C; the counts describe a partial run.                                                           |
| other | **UNKNOWN**     | Not a code this harness recognises — treat the run as unverified.                                    |

Measured 2026-10-05, 4.28.0 → 4.29.3, on a throwaway local spec: nothing tested **0 → 2**, Ctrl+C
**0 → 130**, missing schema 2 → 2. Before KS-1408 every non-zero code was recorded as `failed` and
logged _"Some tests failed"_, and at 4.28.0 a sweep that tested nothing (or was interrupted) exited
0 and read as passed. Only **PASSED** makes the sweep green; the gate's verdict is otherwise
unchanged.

### Reproducibility: the seed, and `--repeat N` (KS-1680)

**One run is one draw.** Each run draws a fresh random seed unless one is fixed, and a failure appears only
when the seed draws the case that reaches it — or, sometimes, only when another operation in the same sweep
has created the data it fails on. Three `pr` runs on one unchanged build found **11, 9 and 8** unique
failures (KS-1680, 2026-10-19). So a single run cannot tell a fix from a lucky draw.

**Every run says which seed it ran and how it was chosen**, in the same words on all three surfaces:

| Surface                       | Where                                                         | Example                            |
| ----------------------------- | ------------------------------------------------------------- | ---------------------------------- |
| Console                       | `Seed: …` line, just before the sweep starts                  | `Seed: 3542270494 (random)`        |
| `schemathesis-results.json`   | `summary.seed`, `summary.seed_source`, `summary.seed_label`   | `"seed_source": "random"`          |
| HTML report                   | Overview → Execution Details → Seed                           | `1607 (fixed via --seed)`          |

`seed_source` is `random`, `profile` (an integer `seed:` in the profile), `cli` (`--seed`) or `repeat` (a
member of a set). A report regenerated from a run directory written before KS-1680 says
`(source not recorded)` rather than guessing.

**To know whether a failure is real, run a set:**

```bash
SECUURA_STACK_SLOT=1 python3 scripts/run.py pr --repeat 3              # 3 runs, 3 random seeds
SECUURA_STACK_SLOT=1 python3 scripts/run.py pr --repeat 3 --seed 1680  # seeds 1680, 1681, 1682 — the set is re-runnable
SECUURA_STACK_SLOT=1 python3 scripts/run.py pr --repeat 3 --compare output/repeats/<earlier set>
```

- **N is 2–10.** Every member is a complete normal run of the tier — its own run folder under
  `output/reports/<tier>-…-r<i>of<N>-…`, its coded suites, its post-run gates and its own HTML report — so a
  set takes N times as long as one run (`full --repeat 3` ≈ an hour on this Mac).
- **Isolation recheck** (on by default; `--no-isolate` skips it): each operation that failed in any member is
  swept again **alone** (`--include-name`) on the same seeds: one sweep per operation per seed, one at a
  time, and the console says how many before it starts. Each is short, but there are many on a big tier
  (`full` with ~90 failing operations × 3 seeds ≈ 270 sweeps) — use `--no-isolate` when only the k/N
  counts are needed. A member whose sweep tested nothing is marked unreadable, never counted as clean.
- **Output:** `output/repeats/<tier>-…/repeat-summary.json` and `repeat-report.html`, plus the same table on
  the console. All three are built from one document, so they agree.

How to read a pair:

| Column      | Value                                       | Meaning                                                                                                         |
| ----------- | ------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| Failed in   | `3/3`                                       | **Deterministic** — every seed reached it. Real, and reproducible on demand.                                    |
| Failed in   | `1/3`                                       | **Seed-dependent** — only some draws reach it. Still a real failure; absence in one run proves nothing.        |
| Isolation   | reproduces alone                            | It fails with no other operation in the sweep.                                                                  |
| Isolation   | needs other operations' data (inferred)     | Failed in the full sweep, never alone on the same seeds: another operation probably creates what it fails on.   |
|             |                                             | For a check that inspects the response (schema, content type, headers) it also means: alone, the operation     |
|             |                                             | never got the status it failed on (e.g. only 404s where it failed on a 200).                                    |
| Isolation   | does not reproduce alone (…reached, passed) | Response-inspecting checks only: alone, the operation got the status it failed on and the check passed there.  |
| Isolation   | inconclusive (operation not tested alone)   | The isolated sweep did not test the operation (or could not be read). **Not** a pass.                           |
| Isolation   | not isolatable (stateful chain)             | `Stateful tests` is a chain of operations; there is no single name to run alone.                                |

**The baseline gate over a set** keeps the single-run rules and reads the counts: an untriaged pair seen in any
run still **fails** (`NEW (not triaged): <pair>  1/3 seed-dependent`); a baselined pair absent from every run
is reported at `0/N` and never removed (KS-565). The single-run gate now runs on a failed sweep too (KS-752,
2026-10-30); before, only the set's gate did. A single run's `NEW` lines say they were seen in 1 of 1 run.

**`--compare`** reads an earlier set's folder (or its `repeat-summary.json`): a pair is **new** only at
0/N → N/N, and anything that moved otherwise (`3/3 → 1/3`, `0/3 → 1/3`) is **inconclusive**. N/N → 0/N
needs evidence before it is called **fixed**, and what counts as evidence depends on the check:

| Check                                                                                   | N/N → 0/N reads                                                                                         |
| --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `response_schema_conformance`, `content_type_conformance`, `response_headers_conformance` | **fixed** if the later set got the status it failed on (and the check passed there), else **not reached** |
| every other check (`not_a_server_error`, `status_code_conformance`, `positive_data_acceptance`, the custom guards) | **gone (not proven fixed)** — the status IS the defect, so once fixed it is never seen again        |

Measured on the KS-1680 proving run, platform unchanged: `POST /api/oauth/apps/{id}/rotate-secret` failed the
schema check on its 200s in 3/3 runs, then got only 400 and 404 in 3/3 later runs. Counting alone called that
fixed; it now reads **not reached**. An earlier set written before statuses were recorded can never support
**fixed**. The single-run Delta tab says the same thing in its caption, and compares only with an
earlier run **of the same profile** — the first `pre-merge` after a `pr` set used to be diffed against a `pr`
member (69 bogus "regressions", KS-1680); it now says there is no earlier run of the profile.

**Exit code:** 0 only when every member exited 0, every member's NDJSON was read, and the set's baseline
verdict is OK.

### Two behaviours worth knowing

- **No health check is suppressed at all (KS-544).** `--suppress-health-check` is not passed.
  Suppression is **root-only** in Schemathesis's config schema, so a single entry silences the check
  for every operation (318 when KS-544 was written; 344 counted from the spec on 2026-10-06) — the blanket-masking pattern KS-156 argued against. Both former entries
  were removed: `too_slow` (a strategy-build timing signal we do not act on) and `filter_too_much`
  (budget-sensitive per KS-500 — trips at `max_examples` 6–15, clears at ≥25, so it reports "this
  profile's budget is too low for this schema", not "this endpoint is broken"). The one endpoint
  that needed relief, `POST /api/timestamps/batch`, now carries a per-operation
  `generation.max-examples = 50` in `schemathesis.toml` instead — the right scope. (KS-500's ≥25
  clearance floor did **not** hold when KS-544 re-measured it: 25 and 30 both tripped, and the check
  proved flaky run-to-run, so the budget is 50 and the trip is reduced rather than eliminated.)
  Worth knowing: the previous mechanism (a Hypothesis profile registered in the sweep subprocess)
  **never took effect anyway** — Schemathesis builds its own `hypothesis.settings(...)` per operation
  and passes `suppress_health_check` explicitly, overriding it. Verified on 4.24.3: the effective
  list was `[]`.
- **`max_redirects` is intentionally left unset.** It caps how many redirects are _followed_, not
  whether they are — so `0` makes requests raise `TooManyRedirects` on the first hop, turning any
  redirect into a global engine error rather than a check result. Redirects are always followed, so
  a 3xx operation's checks see the redirect target's response. The one unfuzzable case
  (`/api/m365/callback`) is handled by `harness.excluded_paths`; the remaining gap is tracked in
  KS-548.

### Verifying the surface after a version bump

Step 4 of the bump ritual is a `schemathesis run --help` diff against `build_schemathesis_args()`.
The run's _effective_ flags are also visible in the generated report — the **Run Settings** section
on the Overview tab is derived from the captured argv (`command-metadata.json`), not from the yaml,
so an override or a resolution bug shows up there instead of hiding behind what the config intended.

---

## Authentication & Token Resolution

### Tiered Token Resolution

`src/config.py` resolves the API token using a 3-tier system (first match wins):

| Tier | Mechanism                                                          | When Used                               |
| ---- | ------------------------------------------------------------------ | --------------------------------------- |
| 1    | `API_TOKEN` env var                                                | Always checked first — highest priority |
| 2    | Azure Key Vault (`AZURE_KEY_VAULT_NAME` + `ENVIRONMENT=dev\|demo`) | CI / cloud deployments                  |
| 3    | Auto-login via `API_EMAIL` + `API_PASSWORD`                        | Local fallback                          |

### Minimal .env for Local Development

Choose **one** of these options:

**Option A — Token directly (fastest):**

```bash
API_TOKEN=eyJhbGci...
```

**Option B — Auto-login (requires Docker + running services):**

```bash
API_EMAIL=issuer@secuura.com
API_PASSWORD=issuer123
```

`API_BASE_URL` is deliberately absent: since KS-1016 the suite derives the gateway from
`SECUURA_STACK_SLOT`, so setting it here would pin the run to one stack. Set the slot instead
(`SECUURA_STACK_SLOT=1 python3 scripts/run.py pr`), and set `API_BASE_URL` only for a remote target such as demo.
With neither a slot nor a URL the run is refused — there is no default gateway (KS-1386).

⚠️ `API_BASE_URL` must be the **host only** — no trailing `/api` (spec paths carry `/api` already).

### Persona Authentication (Full Authenticated Coverage)

Persona auth is **on by default** for every sweep: the `PersonaAuth` provider in `config/persona_auth.py`
(registered when `config/hooks.py` is loaded) injects a real Bearer token for **5 personas**, so authed endpoints are actually exercised. Set
`ENABLE_HOOKS=0` to opt out — then every `bearerAuth` endpoint receives no token and returns 401,
and only public routes are meaningfully tested. Loading the hooks also arms the request-side guards
that keep the sweep from disarming itself: a disposable _session_ for `logout`/`refresh`
(`disposable_session.py`, KS-517) and a disposable _identity_ at the two account-lockout doors
(`principal_shield.py`, KS-575 — a body `email` naming a persona is rewritten to a `.invalid` sibling
on `POST /api/auth/login` / `POST /api/oauth/authorize`, so five fuzzed passwords can no longer lock the
persona out for 15 minutes mid-run). The 5 personas:

| Persona       | Email                  | Role         | Use Case                                      |
| ------------- | ---------------------- | ------------ | --------------------------------------------- |
| `super_admin` | `admin@secuura.com`    | SYSTEM_ADMIN | System admin operations, cross-tenant queries |
| `issuer`      | `issuer@secuura.com`   | ISSUER_ADMIN | Document creation, anchoring                  |
| `verifier`    | `verifier@secuura.com` | VERIFIER     | Verification workflows                        |
| `rh`          | `holder@secuura.com`   | OWNER        | Document owner / holder (rights-holder) views |
| `certifier`   | `issuer@secuura.com`   | ISSUER_ADMIN | Certification / signing operations            |

**How it works:**

1. `PersonaAuth.auth(request)` intercepts every request
2. Resolves the request's required auth scope from the OpenAPI spec
3. Injects a real Bearer token for the appropriate persona
4. Lets the request proceed with authentication

**Run with persona auth:**

```bash
SECUURA_STACK_SLOT=1 python3 scripts/run.py test
```

**Override default persona:**

```bash
SECUURA_STACK_SLOT=1 ENABLE_HOOKS=1 SECUURA_DEFAULT_PERSONA=issuer python3 scripts/run.py test
```

---

## Test Strategies

### Scenario Categories

Schemathesis divides test execution into **11 scenarios**, grouped by testing strategy:

#### Phase 1: Examples (Baseline Happy Path)

- **Scenario 1:** Declared examples from OpenAPI spec
- **Scenario 2:** Generated examples (happy-path inputs)

#### Phase 2: Fuzzing (Property-Based Input Mutation)

- **Scenario 3:** Fuzz parameters (query, path, header)
- **Scenario 4:** Fuzz request bodies
- **Scenario 5:** Fuzz boundary values (empty strings, max-length, null)

#### Phase 3: Stateful Testing (Request Chains)

- **Scenario 6:** Generate request chains from OpenAPI links (create → read → delete)
- **Scenario 7:** Positive workflow (happy path chains)
- **Scenario 8:** Negative workflow (chains with error injection)

#### Phase 4: Security & Auth

- **Scenario 9:** Authentication enforcement (missing/invalid tokens)
- **Scenario 10:** Permission enforcement (endpoint-level RBAC)

#### Phase 5: Performance

- **Scenario 11:** Latency and throughput baselines

### Choosing a Strategy

| Goal                                         | Command                 | Duration | Coverage                                                                                                                         |
| -------------------------------------------- | ----------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------- |
| Quick dev feedback                           | `test-fast`             | ~2-3 min | 6 examples/operation                                                                                                             |
| Pre-merge gate (full contract compliance)    | `pre-merge`             | ~6 min   | all endpoints, generates the report; the CI **pre-merge** tier (`pre-merge-platform-suites.yml`) runs this, NOT the fast PR gate |
| Nightly / deep                               | `full`                  | ~25 min+ | 25 examples (`--max-examples=500` for deep) + extra checks                                                                       |
| Schema / status / headers                    | `contract_schema`       | targeted | schema validation, status codes, headers                                                                                         |
| Data generation (fuzz, negative, boundaries) | `data_generation`       | targeted | happy path, fuzzing, negative, boundaries                                                                                        |
| Auth / IDOR / RBAC                           | `security_auth`         | targeted | auth scenarios + the GDPR IDOR regression                                                                                        |
| Stateful workflows                           | `stateful_workflows`    | targeted | POST→GET→DELETE chains, operation linking, idempotency (PARTIAL)                                                                 |
| Error handling & stability                   | `reliability_stability` | targeted | server error detection, input rejection, timeout/hang detection (PARTIAL)                                                        |

### Coverage Levels

Every test entry under `test_categories` in `config/schemathesis_tests.yaml` carries a
`coverage` field stating how completely it validates its own stated `purpose`:

| Level       | Meaning                                                                                                                                                                                                                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `PRIMARY`   | Fully automated today — the listed `flags`/`checks` actually enforce the purpose, and a real violation fails the sweep. Most entries are this.                                                                                                                                                         |
| `PARTIAL`   | Runs today (rides an existing phase or check) but only partially validates the purpose — the gap is spelled out in that entry's `notes`. Not a bug to "fix" silently; a `PARTIAL` entry is either accepted as-is or needs new Schemathesis-side capability (a custom hook, a different tool) to close. |
| `AUTOMATIC` | Runs as a built-in Schemathesis phase (currently only `api_probing`) with no dedicated `flags` to configure — Schemathesis decides when and how it runs.                                                                                                                                               |

**The two entries currently marked `PARTIAL`, and why:**

- **`stateful_workflows.idempotency`** ("Idempotency Testing") — declares
  `flags.phases: "stateful"`, the same phase `stateful_workflows` and `operation_linking` use,
  but that phase only _generates and executes_ the request chain; Schemathesis has no built-in
  check that repeats a request and compares the two responses. Verifying "safe to retry, same
  result on repeat" needs a **custom hook** (see the entry's `notes` and its
  [hooks reference](https://schemathesis.readthedocs.io/en/stable/reference/hooks/)), which does
  not exist yet — so today this entry exercises the chain but asserts nothing about idempotency.
- **`reliability_stability.timeout_stability`** ("Timeout & Stability") — declares
  `flags.request_timeout: 5`, which only catches a **hard hang** (no response inside 5s). It says
  nothing about latency, p95/p99, or behaviour under sustained load — that is explicitly out of
  scope for Schemathesis and owned by the k6 performance suite (`systemTest/performance/`) per
  the entry's `notes` ("NOT a performance tool — validates stability only"). This entry is a
  stability floor, not a performance measurement, hence `PARTIAL` rather than `PRIMARY`.

When adding a new `test_categories` entry, default to `PRIMARY` — only use `PARTIAL` when the
configured `flags`/`checks` demonstrably don't fully cover the stated `purpose`, and always add a
`notes` entry explaining the gap (mirroring the two examples above) so the next reader doesn't
have to reverse-engineer it from the yaml alone.

---

## Pre-Commit Workflow

Before committing any changes:

```bash
# 1. Run the quality gate — it AUTO-FIXES formatting and must end with "All quality checks passed!"
#    (linters + mypy over src/tests/scripts/config, offline unit suite + 90% coverage, integration when creds present)
SECUURA_STACK_SLOT=1 python3 scripts/run.py quality

# 2. Commit
git add .
git commit -m "..."
```

**Quality gate must pass with zero errors** before every commit.

---

## Pre-PR Workflow

Before raising a pull request:

```bash
# 1. Quality gate (mandatory)
SECUURA_STACK_SLOT=1 python3 scripts/run.py quality

# 2. Full authenticated sweep (recommended)
SECUURA_STACK_SLOT=1 python3 scripts/run.py test

# 3. At minimum: fast sweep
SECUURA_STACK_SLOT=1 python3 scripts/run.py test-fast
```

All tests must pass; see [Troubleshooting](#troubleshooting) if failures occur.

**For a platform PR, the tier is `pr` (or `pre-merge`), and a failure count is not attribution.**
Enumerate every failure from the run's NDJSON, name its operation and the ticket that owns it, and
only then compare with the `develop` baseline — "same count as develop" is evidence only once they
are the _same_ failures. The standing floor at the PR tier is the KS-693 `ENTRA_*`-unconfigured 503
class; anything outside it is yours until proven otherwise. See
**[`systemTest/CLAUDE.md` → The four-suite final check before review](../../CLAUDE.md#the-four-suite-final-check-before-review-ks-685)**
and [known-issues-and-baseline.md](known-issues-and-baseline.md).

---

## Performance Tuning

### Wall-Clock Timeout

```bash
# Default is 1800 seconds (30 minutes)
# Override for faster iteration:
SECUURA_STACK_SLOT=1 SECUURA_SWEEP_TIMEOUT=300 python3 scripts/run.py test-fast
```

### Request Timeout

```bash
# Default is 10 seconds per request
# Increase for slow backends:
SECUURA_STACK_SLOT=1 SECUURA_REQUEST_TIMEOUT=30 python3 scripts/run.py test
```

### Worker Count

Sweeps run with **12 workers** by default (the `--workers` CLI default, tuned for Mac M2).
Override per run with `--workers N`:

```bash
SECUURA_STACK_SLOT=1 python3 scripts/run.py full --workers 8
```

Profile-level defaults live in `config/schemathesis_tests.yaml`
(`harness.workers_default` / `harness.workers_cli_default`).

---

## Output & Reports

### Test Output Location

All test outputs are written to `output/reports/`:

Each sweep writes to its own per-run directory, `output/reports/<profile>-<timestamp>/`, with a
`latest` symlink pointing at the most recent one:

```
output/reports/<run>/
├── schemathesis-output.har                # HTTP Archive (timing data)
├── schemathesis-output.yaml               # VCR cassette (all interactions)
├── schemathesis-output.ndjson             # NDJSON events (authoritative check counts)
├── schemathesis-output.xml                # JUnit XML — root totals AND per-operation detail
├── schemathesis-allure/                   # Allure test results
├── schemathesis-native-html/index.html    # Schemathesis's own HTML report (4.31+, KS-1615) — linked from the Overview; the report below stays canonical
├── schemathesis-crashes/                  # Replayable crash files (ST 4.22+) → Reproduce tab
├── schemathesis-console.txt               # Tee'd stdout — the WARNINGS block lives only here
├── schemathesis-metrics.jsonl             # Per-call metrics from config/hooks.py → auth coverage
├── schemathesis-results.json              # Run summary + config block
├── command-metadata.json                  # The exact argv → Overview's Run Settings section
├── pytest-idor-output.xml                 # TestGdprOwnershipGuard JUnit XML (pre-merge/full only)
└── report-<timestamp>.html                # Interactive HTML report (+ a report.html shortcut)
```

One artefact lives **outside** the per-run directory, deliberately:

```
output/.hypothesis-db/                     # Hypothesis example database (--generation-database)
```

It persists **across** runs so an input that once failed an operation is replayed on every later
sweep — real regression catching rather than re-discovery by chance. Putting it inside
`output/reports/<run>/` would recreate it empty each sweep and make it pointless. It is gitignored
along with the rest of `output/`; delete the directory to reset the replay corpus.

### Regenerating the Report

To regenerate the HTML report from existing output files without re-running tests:

```bash
# From the default output directory (output/reports/)
python3 scripts/run.py report

# From a specific named run directory
python3 scripts/run.py report --input-dir output/pre-merge3-reports
# KS-1680: the Delta tab of a regenerated report compares only with an earlier run of the same profile and slot,
# read from the folder NAME (<profile>[-<ticket>]-<UTC run id>[-slotN]). A hand-named folder such as the one above
# carries no profile or run id, so its Delta tab says there is no earlier run to compare with.
```

Requires `schemathesis-output.ndjson`, `schemathesis-output.yaml`, and `schemathesis-output.xml` in the target directory. Writes a timestamped `report-*.html` and a `report.html` shortcut into the same directory.

### Curl commands in the HTML report

Every failure card in the HTML report includes a **Reproduce with curl** command. The command includes `-i` so that running it directly in a terminal shows the full response — status line, headers, and body:

```bash
curl -i -X POST 'http://localhost:6882/api/auth/register' \
  -H 'Content-Type: application/json' \
  -d '{"email": "test@example.com"}'
```

### JUnit Operations tab — Schemathesis's own per-operation verdict (KS-544)

`schemathesis-output.xml` carries one `<testcase>` per tested API **operation**, each with its
outcome, wall-clock duration, and — where applicable — the violated check or the skip reason. Until
KS-544 only the root `<testsuites>` totals reached the report (as the console cross-check); the
per-operation detail was parsed and then discarded. The **JUnit Operations** tab renders it: rows
ordered errors → failures → skips → passes, slowest first within each, with the full failure or
skip text on expand.

> **These counts are operation-level and will not match the Overview tiles.** The Overview counts
> individual HTTP **interactions**; JUnit counts **operations**. Both are correct and they measure
> different things — the panel states this on its face, because presenting two incomparable numbers
> without the caveat is exactly what produced the "Failed 5,279 vs 224 unique failures" alarm. Read
> this tab for _which operations are unhealthy_, and Overview for _request volume_.

It is also the only per-operation record of **why** an operation was skipped, which makes it the
fastest way to see what a `method_not_allowed` skip actually hit.

**Proving the `method_not_allowed` gate end to end (KS-1607).** The gate is tested through the public CLI, not the private
`WarningCollector`: one real stub sweep exits **1** under the shipped `fail-on` and **0** with `method_not_allowed` stripped from it.

```bash
cd systemTest/schemathesis && venv/bin/python3 -m pytest -q --no-cov tests/functional/config/test_method_not_allowed_gate_end_to_end.py
```

**Reconciling WFC's counts by hand (KS-1607).** The Overview's WFC section shows the result; to check a run directory directly:

```bash
cd systemTest/schemathesis && venv/bin/python3 -c "import sys; from pathlib import Path; from src.html_report.parsing.wfc import parse_wfc_report; from src.html_report.parsing.verdict import parse_verdict_json; from src.html_report.parsing.wfc_reconcile import reconcile_wfc_with_verdict, reconcile_wfc_entries; d=Path(sys.argv[1]); w=parse_wfc_report(d/'schemathesis-output.wfc.json'); print(reconcile_wfc_entries(w.found_fault_entries, w.distinct_found_faults, w.total_faults, reconcile_wfc_with_verdict(parse_verdict_json(d/'schemathesis-output.json'))))" <run-dir>
```

`total_agrees` must be `True`: it is the only hard rule (distinct (code, context) pairs = `totalNumber`). `entries_agree` is
informational (Peter's ruling, KS-1607): `False` means the verdict counts a different number of unique failures than WFC lists — explained in
the report, not a reconciliation failure (the 4.31.1 `full` run, seed 1607, read 24 vs 23). The KS-1478 pre-merge run reads 89 entries, 81 distinct, totalNumber 81, 89 expected.

---

### Reproducing failures with `schemathesis replay` (Schemathesis 4.22+)

From Schemathesis 4.22, every failing case is recorded to disk as a **crash file** — no
flag needed — under `.schemathesis/<project>/cache/crashes/`. A later `schemathesis replay`
re-sends those exact requests and reports which now pass, so you can confirm a fix without
re-running a whole sweep and hoping the same inputs come up again.

**From 4.28.0 (KS-1353), a crash that passes on replay is retried up to three times**, and one that
passes only sometimes is reported as **`FLAKY`** rather than fixed. That distinction matters here: a
single green replay used to read as "fixed", and an intermittent pass is the one result that most
deserves not to be read that way. We do not drive `replay` from the runner — the crash-file cache is
deliberately unused (`scripts/runner/run_options.py`, measured to trip `filter_too_much`) — so this is
a change to the manual reproduction path only.

> Always write the full `schemathesis` binary name. The CLI also answers to the two-letter
> alias, but it is ambiguous in a copy-paste context, so it must never appear in our docs or
> in the rendered report (enforced by a unit test).

The runner stages each run's crash files next to the other report artefacts (in
`schemathesis-crashes/`) and the HTML report's **Reproduce** tab (right after Failures) lists
them: one card per recorded failure with the violated check(s), the reproduce `curl`, the
`schemathesis replay <case-id>` command, and — for stateful failures — the recorded request
chain. A clean run records nothing, and the tab shows an informational notice (the healthy
result).

**The two commands are not equally durable, and the card orders them accordingly:**

| Command                         | Needs the original crash files?  | Use when                                                               |
| ------------------------------- | -------------------------------- | ---------------------------------------------------------------------- |
| the embedded `curl`             | **No** — it is self-contained    | Reading the report later, on any machine, with no Schemathesis install |
| `schemathesis replay <case-id>` | **Yes** — reads `.schemathesis/` | You still have the run that produced the report                        |

That asymmetry is why the report embeds the full `curl` in every crash card: the HTML alone
must be enough to reproduce a failure years from now. Note the `curl` shows
`Authorization: [Filtered]` — credentials are redacted by design, so substitute a valid one
before sending, or the request answers `401`.

```bash
# Re-check every recorded failure after a fix
venv/bin/schemathesis replay

# Re-check just one case (the id is on its Reproduce card and in the run's output)
venv/bin/schemathesis replay 17489A

# Replay against a different environment (e.g. confirm a fix reached staging)
venv/bin/schemathesis replay --url https://staging.example.com
```

Fixed cases are removed from the crashes directory automatically (pass `--keep` to retain
them); cases that still fail are kept. Add `.schemathesis/` to your ignore list — it is
per-project cache, not something to commit.

---

## GDPR IDOR Regression Tests (KS-258)

`pre-merge` and `full` automatically run `TestGdprOwnershipGuard` after the Schemathesis sweep to verify the KS-228 ownership-guard fix is still in place.

### What runs

Six pytest tests in `tests/test_auth_security.py::TestGdprOwnershipGuard` that confirm:

- An issuer cannot read another issuer's orders or documents (403 expected)
- A verifier cannot access documents belonging to a different tenant (403 expected)
- Cross-tenant mutations (update, delete) are rejected (403 expected)

### How to trigger

```bash
# Runs TestGdprOwnershipGuard FIRST (before the sweep, so the sweep's auth probes can't trip the
# login limiter and block the IDOR fixtures' login), then the Schemathesis sweep, then the HTML report
SECUURA_STACK_SLOT=1 python3 scripts/run.py pre-merge

# Same run, deeper fuzz — identical checks/phases/IDOR, 25 examples instead of 6
SECUURA_STACK_SLOT=1 python3 scripts/run.py full
```

`pre-merge`, `full`, `nightly`, and `test` (an alias for `full`) all trigger the IDOR regression
suite; the lighter profiles (`pr`, `test-fast`, `local-debug`, `auth-rate-limited`) do not.

### HTML report — GDPR IDOR tab

The generated HTML report contains a **GDPR IDOR** tab (after the Features tab). It shows:

- Overall pass/fail status badge
- Total tests, passed, failed, duration
- Per-test result table with pass/fail/skip badge, duration, and failure detail

When a profile that runs the IDOR suite (`pre-merge`, `full`, `nightly`, or `test`) was not used to
generate the report, the tab shows a "not run" notice.

### Token resolution

`TestGdprOwnershipGuard` resolves tokens automatically — no extra setup required for most runs:

1. `GDPR_IDOR_TEST_ISSUER_TOKEN` env var (pre-generated, fastest)
2. Falls back to live login using `API_EMAIL` / `API_PASSWORD` credentials

To pre-generate tokens (CI / offline environments):

```bash
SECUURA_STACK_SLOT=1 python3 scripts/setup.py --idor-tokens
```

### JUnit XML output

Results are written to `output/reports/pytest-idor-output.xml` alongside the Schemathesis artefacts.

---

## Troubleshooting

| Issue                                                                                                                               | Solution                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `401 Unauthorized` on authed routes                                                                                                 | Persona auth is on by default — check you don't have `ENABLE_HOOKS=0` set                                                                                                                                                                                                                                                                                                                                                                                                            |
| `404` on all requests                                                                                                               | Check `API_BASE_URL` — remove trailing `/api` if present                                                                                                                                                                                                                                                                                                                                                                                                                             |
| Tests timeout after N seconds                                                                                                       | Increase `SECUURA_SWEEP_TIMEOUT` or reduce workers                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| `ConnectionError` or `TimeoutError`                                                                                                 | Run `docker compose ps` in `Blockchain/Dev/` — ensure all services are healthy                                                                                                                                                                                                                                                                                                                                                                                                       |
| Quality gate failing on lint/format                                                                                                 | Re-run `SECUURA_STACK_SLOT=1 python3 scripts/run.py quality` — it auto-fixes formatting; fix any remaining lint/type/test failures it reports                                                                                                                                                                                                                                                                                                                                        |
| `ModuleNotFoundError`                                                                                                               | `SECUURA_STACK_SLOT=1 python3 scripts/run.py install` to reinstall dependencies                                                                                                                                                                                                                                                                                                                                                                                                      |
| `python3: command not found` or wrong version                                                                                       | Install Python **3.14.8 or newer** (KS-571 floor) — see [Getting Started → Python Installation](getting-started.md#python-installation)                                                                                                                                                                                                                                                                                                                                                                       |
| `SyntaxError: invalid syntax` when running tests                                                                                    | The suite requires Python 3.14.8 or newer — check `python3 --version`; an older interpreter is refused up front with the rebuild command                                                                                                                                                                                                                                                                                                                                                                                                                           |
| API token missing                                                                                                                   | `SECUURA_STACK_SLOT=1 python3 scripts/setup.py` (or set `API_EMAIL`/`API_PASSWORD` — sweeps auto-log-in)                                                                                                                                                                                                                                                                                                                                                                             |
| `Permission denied` on scripts                                                                                                      | `chmod +x scripts/*.py`                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| Tests return `502 Bad Gateway`                                                                                                      | Check gateway logs: `docker logs api-gateway`                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `429` on `/api/auth/register`, or a sweep that differs from the last one only in register `429`s                                    | The register limit is **100/hr/ip on local and non-prod stacks** (5/hr only in production — `api-gateway/src/index.ts`). Don't wait a fixed hour: send **one** request and read `RateLimit-Reset` (seconds) from the `429`, then start when it clears — `curl -s -D - -o /dev/null -X POST <gateway>/api/auth/register -H 'Content-Type: application/json' -d '{}' \| grep -i ratelimit`. Don't poll it: every probe spends the same budget (KS-1353)                                |
| The sweep ignores `schemathesis.toml` — undeclared-method probes appear, and the by-design 503 operations fail `not_a_server_error` | Fixed in KS-1353: the sweep now launches from this directory whatever directory `run.py` was started from. On an older checkout, start `run.py` from `systemTest/schemathesis/` — Schemathesis discovers the toml by walking **up** from the working directory, so launching from `systemTest/` never finds it                                                                                                                                                                       |
| `Stack-targeting signals disagree, so this run would address more than one stack`                                                   | The run's `SECUURA_STACK_SLOT` / `STACK_SLOT` / `SECUURA_BASE_URL` / `API_BASE_URL` name different stacks — usually a stale export or an `API_BASE_URL` left in `.env` by a `setup.py` run on another slot. The message lists each disagreement. Target one slot from one source (`systemTest/run-in-slot.sh <n> …`) and unset the stale variable. It refuses rather than picking one, because either choice would run part of the suite against the wrong stack (KS-1373 / KS-1353) |
| Cassette file very large (>1GB)                                                                                                     | Normal for full sweeps; use `test-fast` during development                                                                                                                                                                                                                                                                                                                                                                                                                           |

---

## Environment Variables Reference

| Variable                        | Default                                                               | Description                                                                                                                                                               |
| ------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `API_TOKEN`                     | —                                                                     | JWT Bearer token (Tier 1 priority)                                                                                                                                        |
| `API_BASE_URL`                  | none — derived from the named slot (slot 1 = `http://localhost:6882`) | Host only — no `/api` suffix. Prefer setting `SECUURA_STACK_SLOT`; set this only for a remote target. No slot and no URL → the run is refused (KS-1386)                   |
| `API_EMAIL`                     | —                                                                     | Email for auto-login (Tier 3)                                                                                                                                             |
| `API_PASSWORD`                  | —                                                                     | Password for auto-login (Tier 3)                                                                                                                                          |
| `ENVIRONMENT`                   | `local`                                                               | `local`, `dev`, or `demo`                                                                                                                                                 |
| `AZURE_KEY_VAULT_NAME`          | —                                                                     | Key Vault name (Tier 2 / cloud)                                                                                                                                           |
| `ENABLE_HOOKS`                  | `1` (on)                                                              | Persona auth is injected on every sweep **by default**; set `0` to opt out (authed routes then 401-and-pass). Applies to the `run.py` sweep only, not `pytest`/`quality`. |
| `SECUURA_DEFAULT_PERSONA`       | `super_admin`                                                         | Default persona when hooks enabled (one of `super_admin`, `issuer`, `verifier`, `rh`, `certifier`)                                                                        |
| `SECUURA_SWEEP_TIMEOUT`         | `1800`                                                                | Wall-clock timeout in seconds                                                                                                                                             |
| `SECUURA_REQUEST_TIMEOUT`       | `10`                                                                  | Per-request timeout in seconds                                                                                                                                            |
| `GDPR_IDOR_TEST_ISSUER_TOKEN`   | —                                                                     | Pre-generated ISSUER_ADMIN JWT. **Scope: `TestGdprOwnershipGuard` ONLY (KS-258).** Falls back to live login if absent. Set via `setup.py --idor-tokens`.                  |
| `GDPR_IDOR_TEST_VERIFIER_TOKEN` | —                                                                     | Pre-generated VERIFIER JWT. **Scope: `TestGdprOwnershipGuard` ONLY (KS-258).** Falls back to live login if absent. Set via `setup.py --idor-tokens`.                      |

---

## Next Steps

- [Contributing Guide](contributing.md) — Code standards, pre-commit checklist, adding tests
- [Known Issues & Baseline](known-issues-and-baseline.md) — Documented drifts and exclusions
- [Report Requirements](schemathesis-report-requirements.md) — HTML report specification and requirements

---

**Last Updated:** 2026-07-09

## KS-1607: reading a 4.32 run

The console failure summary now carries the stable code: `❌ ST101 Server error: 1`, then `For more information, run \`st explain ST101\`.`
(`st explain <code>` says what the failure means, how to fix it and how to turn it off). Each run folder also holds
`schemathesis-failures-pytest.py` (every failure as a pytest test); the harness report links it with its count.
