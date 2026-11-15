# Known Issues and Documented Drift

Catalogues known failures, documented spec-vs-runtime drift, and explicit exclusions for
Schemathesis test sweeps. (Point-in-time baseline metrics are not kept here — read the
failure counts from the latest run report under `output/reports/`.)

---

## Overview

This document tracks:

- **DRIFT-\*:** Documented spec-vs-runtime divergence (spec is wrong or runtime is loose)
- **EXCLUDE-\*:** Known production/security bugs we explicitly tell Schemathesis to skip

When you discover a new expected failure during a baseline re-run:

1. Add it here with a stable identifier (e.g., `DRIFT-AUTH-...` or `EXCLUDE-...`)
2. If drift: link the underlying `.openapi.ts` and/or handler that needs fixing
3. If exclusion: add the operation to `schemathesis.toml`'s `[exclude]` section (Phase 2)

---

## Report Interpretation — NDJSON vs. VCR Check Counts

### Coverage Phase Crash Inflates VCR-Based Check Counts

**Symptom:** The "Error Patterns" or "Checks" tab of the HTML report shows a check (e.g., `status_code_conformance`) as failing 20+ times when NDJSON analysis of the same run shows 0 failures.

**Root cause:** When a phase (e.g., Coverage) finishes with `status: error`, every VCR cassette interaction recorded during that phase has all of its check fields written as `value: False`. This reflects the phase-level crash, not the individual check outcomes. A single crashed Coverage phase can inflate `status_code_conformance` failures by ~21 (one per recorded interaction in that phase).

**Authoritative source:** The NDJSON event stream (`schemathesis-output.ndjson`) records check outcomes from `ScenarioFinished.recorder.checks` at the individual check level. These are unaffected by phase crashes. **Always use NDJSON for check result totals.**

**Report fix (implemented):** As of 2026-06-11, the HTML report's Checks tab, Check Matrix tab, Run Health card, and Error Patterns tab all source check data from NDJSON, not VCR. A phase error banner is shown on the Failures and Error Patterns tabs when any phase ended with `status: error`.

### `filter_too_much` health check suppressed (KS-500)

**Symptom (historical):** `POST /api/timestamps/batch` reported an **error** ("Failed Health Check: 1")
every sweep — Hypothesis's `filter_too_much` — leaving the operation effectively unexercised.

**Root cause:** schemathesis's positive generation of that operation's array-of-objects body inherently
filters a large fraction of draws, and the health check is **budget-sensitive** — it trips at the low
`max_examples` the sweeps use (test-fast=6, pre-merge=6) and clears at ~≥25. The `^[a-f0-9]{64}$` hash is
**not** the cause (`from_regex` generates it fine).

**Intended fix (KS-500):** suppress `HealthCheck.filter_too_much` for the sweep alongside the
long-standing `too_slow` — both are aborts driven by schema _complexity_, not a real defect, so
suppressing lets complex-schema operations run their cases to completion instead of erroring. A
genuinely un-generable operation still surfaces via the `missing_test_data` warning + a low case
count, not a hard error.

**⚠ The KS-500 mechanism never actually took effect (found in KS-544, 2026-07-31).** The suppression
was applied by registering a Hypothesis profile in the sweep subprocess
(`build_hypothesis_setup()` in `scripts/runner/invocation.py`, spliced into a `python3 -c`
bootstrap). Schemathesis does not read that profile: it builds its own `hypothesis.settings(...)`
**per operation** and passes `suppress_health_check` **explicitly**, which overrides anything an
externally registered profile set. Verified against the installed 4.24.3 — with no CLI flag the
effective suppression list is `[]`. So from KS-500 until KS-544, **neither** `filter_too_much`
**nor** `too_slow` was actually suppressed.

**Resolution (KS-544, 2026-07-31): the suppression was REMOVED, not repaired.** Once the mechanism
was made to work it became clear it should not exist: `--suppress-health-check` is **root-only** in
Schemathesis's config schema, so suppressing `filter_too_much` silences it for all 318 operations to
accommodate one. That is the blanket-masking pattern KS-156 argued against. And the check is not
reporting a defect here — this entry's own root-cause analysis shows it is **budget-sensitive**, so
it means "this profile's budget is too low for this schema".

The endpoint is now handled at the right scope, in `schemathesis.toml`:

```toml
[[operations]]
include-name = "POST /api/timestamps/batch"
generation.max-examples = 50
```

**KS-500's ≥25 clearance floor did not survive re-measurement under KS-544.** Both 25 and 30 were
observed to trip on live `full` sweeps, and the check is _flaky_: the same configuration cleared one
batch of runs and then tripped twice back-to-back in another. 50 clears it in most runs but **does
not eliminate it** — the residual trips are tracked under KS-611 rather than tuned away, and are
still live (an `error` at 37.4s on run `full-2026-08-10T15-43-09Z`). Pinned by
`tests/unit/runner/test_args_builder.py`
(`_MEASURED_MINIMUM_BUDGET = 50`), which fails if the budget drops below 50 or if any profile
re-introduces `--suppress-health-check`.

**⚠ STATUS 2026-09-01 (KS-611): the generator this entry analyses NO LONGER EXISTS, and the
residual no longer reproduces offline.** Schemathesis 4.25.0 dropped `hypothesis-jsonschema`
entirely (`jsonschema-rs` 0.51.0 in its place). Re-measured on 4.25.2 by driving Schemathesis's own
generator via `op.as_strategy()` against the real `TimestampBatchRequest` body:

    budgets 6 / 25 / 30 / 50 / 70 / 90 / 100, 20 seeds each  ->  0 trips
    positive AND negative mode, budgets 25 / 50, 20 seeds    ->  0 trips
    440 runs total                                           ->  0 trips

Controls, because an all-zero table is also what a broken harness produces: detection verified
against three filters hypothesis cannot rewrite (the first control was itself faulty — hypothesis
rewrites `x == const` into `just(const)`, so nothing was ever filtered); generation verified real
(50 cases, 46–47 unique bodies, `hashes` arrays of 1–8); and the same `as_strategy()` path verified
able to trip the check 10/10 on a pathological schema (`format: uuid` + `pattern: ^aaaa`).

- **The "budget-sensitive" root cause above is RETIRED, not merely unconfirmed.** It was a property
  of `hypothesis-jsonschema`'s `from_object_schema`. The ≥≈25 floor, the cliff at ~90 and the
  `small_example_cap` mechanism all describe a dependency that is no longer installed.
- **The positive-format-strategy lead is CLOSED as measured-and-rejected**, not untried: the hash
  was never what was being filtered, so generating it directly cannot help.
- **⚠ Offline no longer models live.** The operation still tripped on a live sweep at 4.25.2 (run 1
  09:27Z carried the abort, run 2 10:44Z did not) while reproducing 0/440 offline. Whatever drives
  it sits above `as_strategy()` — phases, hooks, the alphabet, auth, stateful context. **There is
  currently no known mechanism**, and it cannot be pinned offline, which is why KS-611 carries it as
  an accepted residual rather than a fix.

**The previously-recorded green was misattributed.** This entry used to state that after the KS-500
change a `test-fast` run reported `errors=0` with `POST /api/timestamps/batch` passing. That cannot
have been caused by the suppression, since the suppression was inert — it was either a run where the
filter ratio happened to stay under the threshold (the check is budget-sensitive and the draw is
random), or the operation was already clearing at that budget. Recorded here because the same
misattribution happened twice on this ticket (the earlier `format`+strategy attempt was also declared
verified and later found to be a no-op), which is what the "prove a mitigation actually takes effect"
rule in systemTest/CLAUDE.md now exists to prevent.

**Current status (full sweep 2026-07-31, `full-2026-07-31T12-49-34Z`):** with no suppression and the
per-operation budget of 50 in place, `POST /api/timestamps/batch` no longer reports a health-check
error. It now fails differently and genuinely: a **`Response time limit exceeded`** plus a
**`Network Error — read timed out after 10.0s`**. The platform cannot serve a **spec-legal**
`maxItems: 100` batch inside the transport timeout — the generator drew the documented boundary. That
is a platform finding, deliberately left failing rather than tuned away.

---

## §11 State-machine / Precondition Refusals — verified correct (KS-478, KS-466 §11)

**Symptom:** A `pre-merge` sweep reports ten operations as `API rejected schema-compliant request`:
`POST /api/governance/proposals/{id}/{submit,cancel,execute,vote}`, `POST /api/transfers/{id}/reject`,
`POST /api/governance/delegate`, `POST /api/referrals/apply`, `POST /api/stake/unstake`,
`POST /api/m365/documents/sync`, `POST /api/m365/sites`.

**Root cause — not a defect.** Each answers a _legitimate_ business-rule refusal ("Only draft proposals
can be submitted", "Proposal is not open for voting", "Invalid referral code", "Invalid or disconnected
connection", …). The fuzzer cannot chain create → submit → vote to reach the state where the call would
be valid, so it only ever observes the refusal and flags a false positive.

**Neither DRIFT nor EXCLUDE.** These are not excluded (silencing them would pre-empt the contract-side
fix) and are not spec drift. The **preferred resolution is KS-188** — declare OpenAPI `links` +
`operationId` so the fuzzer establishes the preconditions itself and most of §11 stops being reported;
the fallback (KS-478 option b) is to publish the genuinely undeclared 409/422 responses. Both are
platform/spec-side and out of scope for systemTest.

**systemTest verification leg (KS-492 / Review G):** `tests/test_state_machine_preconditions.py` drives
each op to its unmet precondition and pins the refusal to a **clean, enveloped business 4xx** — never a
raw 5xx (the KS-451/KS-431 mode) and never a silent 2xx. This records §11 as working-as-intended, so a
sweep report on these ops is a provable false positive, and it auto-flags the day a refusal degrades.
Runs standalone with a dedicated **Preconditions** report tab (see `schemathesis-report-requirements.md`).

**A skip is NOT a pass (KS-478 red→green rule).** An op that could not be driven here (a 503 provider
or an unseeded/collided persona → 401) **skips**, and a skip is a _coverage hole_, not a pass: any skip
drops the suite to **INCOMPLETE** (amber `pill-s`) and fails the gate, and the console/report show
`N of 10 ops exercised`. A regression guard that skips is not guarding, so a skipped op verifies
nothing. Close it by provisioning the persona/provider, or promote a genuinely unprovisionable vector
to an explicit `pytest.xfail(reason=…)`.

**The one boundary of that rule — OUT OF SCOPE (KS-519).** A vector this environment _could_ have
driven and did not is a coverage hole. A vector the environment **cannot contain** is not, and
failing the gate on it produces the same desensitisation by the opposite route: a gate that is red on
every run stops being read. The anchoring suite's `test_revoked_document_does_not_verify` is the
worked example — it asserts on a real on-chain anchor, and local anchoring is mock **by design**
since KS-535, so it had failed every local run 13 times without once executing. It is now excluded
by `require_real_anchoring` (`tests/integration/fixtures/anchoring_mode.py`) and reported as
`OUT OF SCOPE` with its reason, rather than as a skip.

Three properties keep the exclusion honest, and none is optional:

- It is recognised **only** by the `OUT_OF_SCOPE_SKIP_PREFIX` constant (`src/constants.py`, one
  definition shared by the fixture that emits it and the gate that reads it) — never by "a reason was
  given", so an ordinary `pytest.skip("…")` still reds.
- A run in which **nothing** was exercised fails with `NOTHING EXERCISED`, so pointing the suite at a
  target where every scenario opts out cannot report clean (MUST #13 rule 6 applied to the exclusion
  itself).
- The gate's success line names the exclusion (`… passed, 1 out of scope (mode) …`) instead of
  claiming a clean sweep.

It is deliberately **not** an `xfail`: an xfail asserts a documented _open platform defect_ and is
`strict=True`, so it would flip to a hard failure the moment someone ran the suite against demo and
the test passed — announcing a platform fix that never happened. An environment fact must not borrow
the vocabulary of a defect. The dominant skip cause is a 401 on the governance/stake
creates (a single-session collision or role-auth gap, cf. the KS-507 single-session note) — a harness
provisioning gap to fix, not an environment fact. `POST /api/stake/unstake` is also the KS-515
regression guard (business-over-limit refusal must stay green through Kamil's `positive_data_acceptance`
fix).

---

## Known Drift — Documented Spec-vs-Runtime Divergence

### DRIFT-METHOD-405 — undeclared methods: the old 502 is fixed; they now answer 405 + `Allow` before auth (KS-1358)

_The Symptom / Count / Fix path below are the ORIGINAL entry, kept as history — the 502 no longer occurs.
Current state is the 2026-09-28 status that follows them._

**Symptom (original):** Schemathesis sends `TRACE`, `OPTIONS`, etc. to routes whose spec only declares (e.g.) `GET`. Gateway proxies the method upstream, which rejects it, and returns **502 Bad Gateway** instead of the documented **405 Method Not Allowed**.

**Count:** 31 unsupported-method failures + 5 server-error failures (overlapping).

**Where:** `services/api-gateway/src/index.ts` (proxy middleware).

**Fix path:** Add an HTTP-method allowlist middleware that rejects unsupported methods at the edge with 405 + `Allow:` header before any upstream proxy call.

**Status 2026-09-28 (KS-1353): the 502 is gone — and the fix path above is what landed, which now disagrees
with KS-406.** Measured on slot 3 (`d9ce1403d`), with **no credentials at all**:

```
DELETE /api/analytics/overview   (undeclared method)  →  405 Method Not Allowed   Allow: GET
GET    /api/analytics/overview   (declared — control) →  401
TRACE  /api/auth/logout                                →  405 Not Allowed         Allow: GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS
```

Across a full sweep's undeclared-method probes: **405 ×1,760**, 204 ×307 (OPTIONS), 404 ×29, and **401 ×2**.

So the method check now runs **before** authentication, and the route-specific `Allow` header tells an
anonymous caller which methods each operation supports. The declared-method control still answers 401, so
authentication itself is intact; only the ordering changed. That is the reverse of the posture KS-406 ruled
on 2026-07-08 — _"That posture is INTENDED — it avoids revealing the method surface to unauthenticated
callers"_ (`schemathesis.toml`, `[phases.coverage]`). Which record stands is the platform owner's call: this
entry's own fix path asked for exactly the 405 + `Allow` now in place, and method enumeration is low severity
on its own. **Raised as KS-1358** (2026-09-28, Security Review — Platform K), phrased as a question. The source
is `api-gateway/src/specRouteMap.ts` — spec-aware method filtering, i.e. KS-406's option (b), but running
_before_ authentication — and it now answers 405 on the very route KS-406 cited as its evidence of 401
(`/api/referrals/0`). **Not decided here.** The harness keeps KS-406's suppression until it is re-ruled.

The `TRACE` row answers with nginx's own reason phrase (`Not Allowed`) and a global `Allow` list, so that one
is refused at the edge before the api-gateway sees it; the route-specific disclosure is the api-gateway's.

---

### DRIFT-MISSING-RESPONSE-STATUSES — Undocumented status codes (429 / 502 / 503)

**Symptom:** Routes return `429`, `502`, or `503` at runtime but those statuses aren't declared in the route's `.openapi.ts` `responses` block.

**Count:** 48 "undocumented status code" failures.

**Where:** Every `.openapi.ts` whose route can return a documented status not in `commonErrorResponses[400/401/403/404/409/422/500]`.

**Fix path:** Phase 1 KS-2 `commonErrorResponses` already includes 429, 502, 503 — they just weren't applied to most routes. Audit all 23 service `.openapi.ts` files: add `429: commonErrorResponses[429]` to any rate-limited route, and `502 / 503` where applicable.

---

### DRIFT-ERROR-SHAPE — Handlers bypass formatErrorResponse(), return string errors

**Symptom:** Schemathesis hits a 4xx and the body is `{"error": "Forbidden"}` (string) but spec says `error: {code, message, details?}` (object). Sometimes missing `success: false`.

**Count:** 32 "response violates schema" failures.

**Where:** Route handlers using raw `res.status(403).json({ error: 'Forbidden' })` instead of `res.status(err.statusCode).json(formatErrorResponse(err))`.

**Fix path:** Find handlers that don't use the shared error middleware. `git grep "res.status.*\\.json(.*error: " services/` is a starting point. Convert each to throw `AppError` so the express errorHandler shapes it correctly.

---

### DRIFT-MISSING-HEADER-NOT-REJECTED — Required headers not enforced

**Symptom:** Spec marks a header `required: true` (CSRF token, tenant scope, etc.) but runtime accepts requests without it.

**Count:** 54 "missing header not rejected" failures.

**Where:** Middleware-wide. Decision needed per route family: enforce or relax.

**Fix path:** Audit in two passes:

1. Mass-grep `required: true` in `.openapi.ts` parameter declarations
2. For each, decide: enforce middleware-side, or relax spec-side. Document the decision in the route's `.openapi.ts` description.

---

### DRIFT-POSITIVE-DATA-ACCEPTANCE — `positive_data_acceptance` (KS-255, partial)

**Symptom:** Schemathesis generates schema-compliant request bodies, but the API rejects them with 422 (weak password) or 429 (rate limiting). The `positive_data_acceptance` check records these as failures because the API rejected a schema-valid input.

**Count (2026-06-11 full run, NDJSON-verified):** 19 failures across all 12 target endpoints.

**Root causes:**

- `POST /api/auth/register`, `POST /api/auth/change-password` — `00000000` / `000000000` generated as password; server correctly rejects weak passwords with 422. The OpenAPI spec does not declare `minLength` for password fields, so Schemathesis considers the short value schema-compliant.
- Rate-limited endpoints — 429 responses when the fuzzer hits the same route many times in quick succession.

**Fix path:**

- Declare `minLength` (and optionally a `pattern`) for all password fields in the OpenAPI spec so Schemathesis generates only values that would pass validation.
- Declare `429` in `responses` for rate-limited routes (overlaps with DRIFT-MISSING-RESPONSE-STATUSES).
- Track under KS-255.

**Note:** `status_code_conformance` was ✅ 0 failures in the same run — that part of KS-255 is resolved.

**v4.21.7 note (KS-275):** v4.21.7 fixes a false positive in the `positive_data_acceptance` check for array parameters that use percent-encoded separators (`%2C` for `,`, `%7C` for `|`). If the `positive_data_acceptance` failure count drops below 19 after upgrading to v4.21.7, this is the cause — not a regression. The remaining failures (weak password 422 + rate limiting 429) are genuine known issues tracked under KS-591 — the live owner of the `positive_data_acceptance` recurrence. (KS-255 first recorded them and is Done + archived; see `src/html_report/failure_tickets.py`, which maps this check to KS-591 for the same reason.)

**KS-283 update (2026-06-17):** two _additional_ `positive_data_acceptance` triggers on the auth endpoints were diagnosed and fixed:

- **Empty / absent body** on `POST /api/auth/{register,login,forgot-password}` — the spec's `requestBody` was not `required`, so Schemathesis generated empty-body "positive" cases the runtime correctly 400s. Fixed by marking the three request bodies `required: true` (`services/auth/src/auth.openapi.ts`). The **Coverage phase is now green** for all three (local run 2026-06-17, seeds `1615736067` + `424242`).
- **`mfaCode` astral chars** on `POST /api/auth/login` — runtime `z.string().length(6)` counts UTF-16 code units while the spec's `minLength/maxLength: 6` counts code points, so a 6-code-point astral string was >6 code units → 400. Fixed by aligning both the runtime (`auth.ts loginSchema`) and the spec to `pattern: ^[0-9]{6}$` (the real TOTP shape; digit-only, so the two counts agree).

**KS-285 update (2026-06-17) — RESOLVED:** the residual flagged by KS-283 — a _flaky, fuzzing-phase_ `positive_data_acceptance` failure on `register/login/forgot-password` when Schemathesis generates an email valid per JSON-Schema `format: email` but rejected by the stricter runtime Zod `.email()` (e.g. `k-{c@ge.w0.tl`, `GH7Zah%W|T@…`) — is fixed by a **custom `email` format strategy** in `config/formats.py` (was `config/hooks.py` before that module was split): `schemathesis.openapi.format("email", st.from_regex(<validator-clean pattern>))`. This overrides only the _positive_ generator, so the schema's notion of validity is unchanged and `negative_data_rejection` still mutates the field freely — deliberately NOT a spec `pattern`/runtime change, which is the #240/#248 trap (those regressed `negative_data_rejection`, reverted; see `schemathesis.toml` lines 16-21). Verified local 2026-06-17: the auth+oauth ops pass all three checks across seeds `1615736067` (the previously-failing one), `424242`, `99887766` — 291/291, every phase green. The strategy applies whenever the hooks load (persona auth is on by default for sweeps; `ENABLE_HOOKS=0` opts out).

**KS-356 update (2026-06-30) — residual of KS-285; resolved via expected-statuses:** the KS-285 custom `email` format strategy reduces but does not _eliminate_ the format:email-vs-Zod-`.email()` mismatch on the auth endpoints. It is a _hypothesis_ strategy — hook-load- and version-dependent — and KS-356 recurred on a 4.21.10 `full` run (`%@r.lr` on `POST /api/auth/login`) despite it. Spec-pattern tightening remains the #240/#248 trap (regresses `negative_data_rejection`), so the durable, phase-agnostic fix follows the repo's blessed mechanism — a per-operation `positive_data_acceptance.expected-statuses` entry adding `400` for `POST /api/auth/login` in `schemathesis.toml`, alongside the existing register/reset-password/oauth/wallet exceptions.

_Verified 2026-06-30 against a live local auth stack on schemathesis **4.21.10** (correcting an earlier coverage-phase hypothesis):_

- The **fuzzing phase**, when the KS-285 strategy is _not_ constraining generation (hooks off), emits format:email-valid-but-Zod-invalid emails as **positive** cases — VCR captured `~rD@…`, `DSmJmbH_&%@…`, `wY{|…=…@…`. With hooks on, the strategy eliminates them (all emails Zod-clean). So `%@r.lr` is **fuzzing-phase** output, _not_ coverage-phase.
- The **coverage phase** does ignore custom format strategies (`cover_schema_iter` on `{type:string,format:email}` yields the same value with/without the strategy), but that value is `0@a.com` — Zod-**valid** — so the coverage phase is **not** the source of the 400.
- The runtime correctly 400s a Zod-invalid email (live `curl … %@r.lr` → `400 VALIDATION_ERROR: email: Invalid email`).
- schemathesis resolves login's `positive_data_acceptance.expected-statuses` to include `400` (scoped to login; control endpoint unchanged) → the check passes on that 400.
- _Caveat — not a fully organic end-to-end repro:_ login is heavily rate-limited (per-IP login limit + F-06 account lockout), so a local burst returns **429** (an accepted status) before the 400 surfaces, masking the failure. The fix is therefore verified at every mechanistic link rather than by one organic before/after run.

**KS-362 update (2026-07-01) — RESOLVED for register + forgot-password:** the two sibling endpoints flagged on `full` runs (2026-06-30, base `http://localhost:6882`) — non-deterministically, since property-based fuzzing varies the payload per seed (register failed at 13:30, passed at 13:47; forgot-password failed both). Same blessed mechanism as KS-356: a per-operation `positive_data_acceptance.expected-statuses` entry adding `400`, scoped to each endpoint in `schemathesis.toml`. Register keeps `422` (weak-password ValidationError); forgot-password has no `422` (email-only, no password-strength check). The trigger here is broader than the KS-356 email mismatch — Schemathesis injects extra unknown body properties and the runtime correctly rejects them with `400 VALIDATION_ERROR` (additionalProperties). The same email:format-vs-Zod-`.email()` mismatch also applies (same `email: z.string().trim().email()`). Spec-tightening (`additionalProperties: false` / `pattern`) stays off — the #240/#248 trap that regresses `negative_data_rejection`. `negative_data_rejection` on both endpoints is unchanged (no spec change).

---

### DRIFT-NEGATIVE-DATA-REJECTION — `negative_data_rejection` (KS-266)

**Symptom:** Schemathesis sends schema-violating request bodies (missing required fields, wrong types) but the API returns 2xx instead of 4xx, indicating the input passed validation when it should have been rejected.

**Count (2026-06-11 full run, NDJSON-verified):** 2 failures.

**Affected endpoints:**

- `POST /api/auth/register` — accepts a body with no `password` field; should return 422.
- `POST /api/auth/forgot-password` — similar schema-bypassing case.

**Fix path:** Add Zod `.parse()` validation at the handler entry point for both endpoints (not `safeParse()`, so the Zod error propagates to the shared error middleware as a typed 422).

**KS-518 update (2026-07-31, re-measured on 4.24.3):** this class now stands at **10 operations**,
tracked as KS-518 (In Progress). Kamil has closed two of them — `POST /api/transfers/{id}/approve`
(PR #605: zod's non-strict object silently _dropped_ the undeclared `reason` key, so `reason: {}` was
accepted-and-ignored; it now 400s) and `POST /api/notifications` (PR #604). The count held at 10
because membership rotated, not because nothing was fixed.

**One member of this class is BY DESIGN and must not be "fixed" — `GET /api/platform/audit-log`
accepting an unknown query parameter** (Kamil, KS-518, 2026-07-29):

> _"rejecting unknown query params is NOT standard REST practice and a platform-wide flip would fight
> the positive generator (the KS-472 lesson) — recommend registering this one (and the class) as
> **by-design tolerated** rather than 'fixing' it."_

Recorded here so it is a decision rather than an open finding someone re-files each sweep. The
reasoning is the same trap as #240/#248 above: tightening the contract to satisfy a negative check
regresses the positive generator, which costs real coverage and reports nothing when it does.

**KS-662 update (2026-08-17) — this section previously ended with the line:**

> _"Note this is a **platform** by-design call — it does **not** license suppressing_
> `negative_data_rejection` _in the harness, which stays armed for the other nine."_

**That line is superseded, and the distinction it drew is preserved rather than dropped.** It was
written when the only available harness lever was a per-operation `expected-statuses` exception,
which is all-or-nothing — so "suppress in the harness" could only have meant excusing the whole
endpoint, and refusing it was right. KS-662 adds a lever that did not exist then, so the harness now
records the ruling **without** the masking the line was protecting against.

✅ **RULED by Kam, 2026-08-25 — Option A, the property reading** (relayed by Wednesday; recorded in
full on KS-662, comment `16aa42bd`). This block is no longer proposed. Prior state: it read _"Pending
Kamil's agreement — treat this block as proposed until he confirms"_, which was written on 2026-08-17
before the ruling existed and was stale from 2026-08-25.

> _"the four-vs-ten reconciliation is settled, and you are unblocked … That is exactly what PR #722
> already implements, so the ruling costs zero build change — nothing on the branch moves."_

**KS-518's closure is honoured on its PROPERTY, not on its COUNT of ten.** Its basis sentence — _"the
10 flagged operations are status-list service reads"_ — is right about the property and wrong about
the count: only **three** of the ten are the status-list service. The ruling stands; one clause of its
basis is corrected.

⚠️ **Two precisions that must not be lost, both from the same ruling:**

1. **The tolerated set is three status-list operations + `audit-log` — not "four status-list
   operations".** `audit-log` rides on a **separate** authority (Kam's 2026-07-29 unknown-query-param
   rule), which survives whichever way the status trio is ruled. A future change to one must not
   silently move the other.
2. **`POST /api/status/{id}/allocate` is a fourth status-list operation with NO violation** in
   KS-518's table (a dash, with the KS-472 note). It is deliberately not tolerated and never needed to
   be. Two different "fours" are in circulation and are easy to merge by accident.

**Standing instruction if the tool stops producing a tolerated case** (e.g. Schemathesis 4.25.x's
`format: float` bound fixes dissolving the `check/{index}` float case): the entry is **DELETED, not
kept** — the tripwire test in `tests/test_by_design_permissive.py` is the signal, and per the
2026-08-05 correction absence from one run is not evidence, so it wants a targeted re-probe.

What actually ships, in two halves that are useless apart:

1. **`schemathesis.toml`** — `negative_data_rejection` accepts `2xx` on **four** operations only:
   `GET /api/platform/audit-log`, `GET /api/status/{id}/check/{index}`,
   `POST /api/status/{id}/revoke`, `POST /api/status/{id}/unrevoke`. Each entry carries its ruling
   verbatim with the ticket.
2. **`by_design_input_tolerance_guard`** (`config/checks.py`) — on a 2xx to those operations it
   classifies which violation was sent: the ruled one passes, **anything else fails, naming what was
   accepted**. So the endpoint keeps its coverage; only the decision is excused.

Three things keep that honest, because half of it cannot fail on its own:

- **The toml half can never fail** — `400` was already an expected status, so adding `2xx` makes the
  blanket check pass whether the platform accepts _or_ rejects. That is a check that cannot fail
  (MUST #13 rule 6), which is precisely why it does not ship alone.
- **`TestLockstepWithSchemathesisToml`** (`tests/unit/checks/test_by_design_input_tolerance_guard.py`)
  fails the offline gate on drift in either direction. The dangerous one is silent: excused in the
  toml, absent from the guard, so every violation on that endpoint is tolerated and the run looks
  clean.
- **`tests/test_by_design_permissive.py`** pins all four tolerated behaviours live. Neither the toml
  nor the guard can notice the exception outliving the decision — the guard passes a 4xx, since a
  rejection is the desired outcome. If go-live hardening lands (the KS-545 gated-hardening pattern
  KS-518's closure anticipates), those tests go **RED**, and that is the signal to delete the
  exception rather than update the assertion.

**Scope — deliberately four, not ten.** Kamil's closing note said _"the 10 flagged operations are
status-list service reads"_, but only three are; the audit-log tolerance rests on his separate
2026-07-29 ruling. The other six have no stated ruling, so `negative_data_rejection` stays fully
armed on `POST /api/presentations/verify`, `POST /api/wallets/verify`,
`PATCH /api/security/events/{id}/resolve`, `POST /api/analytics/exports`,
`POST /api/gdpr/erasure/{userId}` and `GET /api/users/admin/list` — three of which also violate their
response schema (see the block below). This applies the ruling to what it actually names.

### The by-design 501 on `POST /api/wallets/verify` (KS-686)

The same two-halves shape, applied to `not_a_server_error`. The operation fails closed with a
documented **501 NOT_IMPLEMENTED** since KS-488 C-2 (it used to answer `verified:true` for any input);
`not_a_server_error` ignores the declared status list and reported that correct posture as a defect on
every sweep — 29 × 501 in one pre-merge run (2026-08-25), inflating KS-593's raw-5xx register by an
operation that carries no unhandled exception.

The ruling, verbatim: _"Tolerate the 501 until KS-627 lands (guard + tripwire, land it on the KS-684
branch)"_ — Kam, 2026-08-26 10:44:51 AEST, on KS-686.

1. **`schemathesis.toml`** — `checks.not_a_server_error.expected-statuses = ["2xx", "3xx", "4xx", "501"]`
   on that one operation, ruling quoted beside it. (Until KS-1170 this was `enabled = false`; Schemathesis
   4.26.1 made the profiles' explicit `--checks` list override a per-operation disable, so from the 4.27.1
   bump the line was dead and the 501 redded every sweep again. The tolerance names the ONE status and
   survives the list — the built-in check still fails a raw 500/502/503 here.)
2. **`by_design_501_guard`** (`config/checks.py`, set in `config/check_predicates.py::_BY_DESIGN_501_OPS`)
   — passes a `< 500` and the declared `{"success": false, "error": {"code": "NOT_IMPLEMENTED"}}`
   envelope; **fails a raw 500, a 502/503/504, and a 501 with any other body.**

Kept honest by:

- **`TestLockstepWithSchemathesisToml`** (`tests/unit/checks/test_by_design_501_guard.py`) — the toml
  entry ⇔ the frozenset, and every operation tolerating a 5xx on `not_a_server_error` owned by exactly one guard
  (the KS-268/KS-544 503 set XOR this 501 set, never both, never neither).
- **`tests/test_wallet_verify_stub.py`** — the live tripwire. The guard passes a `< 500` on purpose and so
  cannot notice the exception outliving the ruling; this test asserts the 501 posture and the
  never-`verified:true` invariant separately, and goes **RED naming KS-627** the moment the 501 ends.
  That red means delete both halves (and KS-627's own `positive_data_acceptance` exception), then
  replace the test with real CIP-8/COSE negative vectors — never loosen it to accept what replaced the 501.

**KS-593's count is inflated by this operation until the guard has run live** — re-check it on the
next sweep and note the correction there.

**One observation raised, not settled (KS-662).** `GET /api/status/{id}/check/{index}` does not
merely accept the non-integer `index` — it silently coerces it. `2.5890419884777833e-42` was answered
as `{"index": 2, "isRevoked": true}`: a revocation-status answer about a _different_ credential index
than the caller asked for. Whether that sits inside "permissive input handling" or is a separate
correctness defect is unadjudicated; it is recorded on KS-662 and asserted in neither direction.

**A SECOND member of this class is BY DESIGN as of 2026-08-26 — `GET /api/users/admin/list`,
SCOPED TO THE CHECK AND NOT TO THE OPERATION** (Kam, KS-592, 2026-08-26, relayed by Wednesday):

> _"Whole operation tolerated under the 2026-07-29 rule; the null union is intended"_ (10:45:25 AEST)

> **SUPERSEDED THE SAME DAY, by Kam, 17:11:38 AEST:** _"check — Tolerate the CHECK
> (unknown-query-param class) …"_

**The second ruling is the operative one.** The tolerated thing is the `negative_data_rejection`
CHECK on this operation under the 2026-07-29 unknown-query-param class — **not the operation**. The
distinction is not pedantic: a whole-operation exclusion would also have swallowed the two `offset=-1`
**HTTP 500**s documented below, and a ruling can settle a 200-where-a-400-was-wanted but cannot make
an unhandled 500 correct. Those rows stay **LIVE** and able to fail red.

This answers three questions raised on KS-592 (2026-08-25): (1) the 2026-07-29 unknown-query-param
rule is **platform-wide** — "the class" — so it reaches this operation on the same footing as
`audit-log`; (2) the spec's `[integer, "null"]` union for `offset` is the **intended** contract, so
`offset=null` is conformant rather than a separate violation; (3) no spec narrowing ever happened, so
that question is moot. **KS-592's fix set drops from six operations to five** — for the
`negative_data_rejection` check only. This operation remains in scope for every other check.

The union reading was confirmed against the failure artefact before the ruling arrived, not merely
argued: in the 2026-08-18 pre-merge run `limit=1&offset=null&search=&role=` returns **200 and passes
every check**, so the absent bare-`offset=null` failure is a real pass rather than a gap in the corpus.

⚠ **Two rows on this operation are NOT `negative_data_rejection` and are NOT reached by the ruling's
stated basis.** The same artefact shows `offset=-1` (and `limit=1&offset=-1&search=&role=`) returning
**HTTP 500**, failing `not_a_server_error`. That is the DRIFT-FUZZ-5XX class below, whose KS-544 update
(2026-08-04) already documents this exact defect with its root cause — `parseInt(req.query.offset as
string) || 0` at `services/auth/src/routes/users.ts:344` and `:398`, where `-1` is truthy and Postgres
rejects it — and records that the negative-offset pattern is **six sites across four services**, of
which the sweep reaches only these two.

**So the tolerance is NOT implemented as a blanket per-operation exclusion — and that is now ruled,
not merely recommended.** A ruling can settle a 200-where-a-400-was-wanted; it cannot make an
unhandled 500 correct, and the first ruling's two stated reasons (unknown query params, the intended
null union) reach neither of those rows. The exception is therefore scoped to the **ruled check**,
exactly as the audit-log entry above already requires and as the by-design-503 and KS-686 guards do —
exclude the ruled shape, keep everything else able to fail red.

Raised back to Kam through Wednesday on 2026-08-26 and **answered the same day** (17:11:38 AEST,
above): tolerate the check, not the operation. **The two `offset=-1` 500s remain in scope** and are
already tracked — root-caused on KS-565 §2 (`parseInt(req.query.offset as string) || 0` at
`services/auth/src/routes/users.ts:344` and `:398`, where `-1` is truthy and Postgres rejects it),
carried on KS-593 as part of the live `not_a_server_error` recurrence, and noted on KS-544's
2026-08-04 update. **No new ticket is needed for them**; they are not orphaned by this exception.

Artefact caveat, stated because it changes what the numbers mean: the measurements above are from the
2026-08-18 pre-merge run on **Schemathesis v4.24.3**, i.e. before 4.25.0 replaced the generation engine
(`hypothesis-jsonschema` dropped entirely). They describe the old generator; a current-generator
re-measurement needs a live 4.25.2 stack.

**IMPLEMENTED IN THE HARNESS — KS-1447 (2026-10-15), scoped to Kam's stated class only.** Until this
change nothing implemented the ruling: only the `negative_data_rejection::GET /api/users/admin/list`
baseline entry (ticket KS-1015) kept the pair quiet. The operation now joins the KS-662 two-halves set:

- `schemathesis.toml`: `2xx` added to `checks.negative_data_rejection.expected-statuses` for this
  operation only. No other check is configured, so `not_a_server_error` still fails the `offset=-1` 500s.
- `config/check_predicates.py`: the operation is in `_BY_DESIGN_TOLERANT_OPS` with a **strict** classifier,
  `config/unknown_query_tolerance.py`. It tolerates a request only when an undeclared query key is its
  ONLY violation: every declared value must be valid (wire strings such as `"1"` are read as the server
  reads them), and nothing other than the query may be negative. Audit-log's classifier was not reused,
  because it answers True whenever any undeclared key is present.
- `tests/unit/checks/test_unknown_query_tolerance.py` and
  `tests/functional/config/test_admin_list_unknown_query_tolerance.py` (real CLI against a stub): red on
  develop `0543ff1e6`, green after. A live tripwire is in `tests/test_by_design_permissive.py`.

**Narrowed on Peter's instruction (2026-10-15): "The tolerance should not be wider than Kam
mentioned."** The first cut on this branch tolerated the whole check, which also hid the declared
`limit`/`offset` violations.

**Measured live, slot 2 of the Mac, develop `0543ff1e6`, Schemathesis 4.31.1, `pre-merge`, 347 operations,
`STACK_PREFIX=secuura-s2` exported (KS-1616 workaround — no longer needed once KS-1616 lands):**

| pair | before (develop, `pre-merge-2026-10-15T12-52-22Z-slot2`) | after (KS-1447, `pre-merge-2026-10-15T13-25-37Z-slot2`) |
| -- | -- | -- |
| `negative_data_rejection::GET /api/users/admin/list` | 10 | **0** |
| `by_design_input_tolerance_guard::GET /api/users/admin/list` | not guarded | **21**: declared `limit`/`offset` violations; none carries an undeclared key |
| `not_a_server_error::GET /api/users/admin/list` (the `offset=-1` 500s) | 2 | **2**: still live, as ruled |

The `negative_data_rejection` baseline entry is retired. The 21 real violations are baselined under
`by_design_input_tolerance_guard::GET /api/users/admin/list` (ticket KS-1015), the same arrangement as
audit-log's KS-1359 entry. The `not_a_server_error` entry (KS-593) stays. On the after run the
triaged-baseline gate reads 85 observed pairs, 0 unlisted, 0 expired.

**Also unresolved in this class (untracked as of 2026-08-04):** `POST /api/presentations/verify`,
`POST /api/wallets/verify` and `PATCH /api/security/events/{id}/resolve` **additionally** violate
their declared _response_ schema in the same run — likely one root cause (nothing validated, so
nothing shaped correctly) rather than two independent defects. Worth confirming before treating them
as separate work.

---

### DRIFT-FUZZ-5XX — Fuzzed input crashes the server

**Symptom:** Schemathesis sends a payload that should be 422, server returns 500.

**Count:** 5 "server error" failures.

**Where:** Route handlers not validating input via Zod before reaching business logic.

**Fix path:** Add `parse()` (not `safeParse()`) at handler entry — Zod throws → middleware turns into typed 422.

**KS-283 update (2026-06-17):** one of these — `GET /api/oauth/authorize` returning 500 on a NUL-byte / non-UTF-8 `client_id` — is fixed. The malformed value reached `getAppByClientId()` and Postgres threw `22021` (invalid byte sequence for encoding UTF8), surfacing as a 500. Now rejected with 400 _before_ the DB lookup (charset guard on `client_id`) plus a catch-level `22021`/`22P05` → 400 mapping (`services/auth/src/routes/oauth.ts`). `not_a_server_error` green on `/api/oauth/authorize` (local run 2026-06-17).

**KS-544 update (2026-08-04) — two members of this class are still live and UNFILED.** Both were
re-verified by reading the current `develop`-merged source, not inferred from an old sweep. They are
recorded here with `file:line` so the finding survives without a ticket; both are backend-owned.

| Operation                      | Site                                                   | Mechanism                                                                                                                                                                                                                                          |
| ------------------------------ | ------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `POST /api/users/admin/create` | `services/auth/src/routes/auth.ts:177`                 | `data.email.toLowerCase()` runs with no type guard, so a non-string `email` (e.g. `{}`) raises `TypeError` → 500 instead of a typed 400/422.                                                                                                       |
| `GET /api/users/admin/list`    | `services/auth/src/routes/users.ts:344` **and `:398`** | `parseInt(req.query.offset as string) \|\| 0` — `-1` is truthy, so it passes the guard unchanged and Postgres rejects it (`OFFSET must not be negative`) → 500. The `\|\| 0` fallback only catches `NaN`, never a valid-but-out-of-range negative. |

**The negative-offset pattern is SIX sites across four services, not the two the sweep surfaced**
(grepped on 2026-08-04; the sweep only reached the two `users.ts` handlers because the others need
different preconditions):

| Site                                                | Reaches                                                                               |
| --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `auth/src/routes/users.ts:344`, `:398`              | `userRepo.listUsers({ offset })`                                                      |
| `originate/src/routes/adminConfig.ts:1006`, `:1166` | raw `LIMIT ${limit} OFFSET ${offset}` (×4 queries)                                    |
| `tenant-provisioning/src/index.ts:556`              | `SELECT … LIMIT $1 OFFSET $2`                                                         |
| `api-gateway/src/routes/platform.ts:374`            | capped by `Math.min(…, MAX_AUDIT_OFFSET)` — upper bound only, still no negative guard |

**Not an injection risk** — the raw-SQL cases use Prisma's `$queryRaw` _tagged template_, so the
values are parameterised, and `parseInt(…) || 0` always yields a number regardless. The defect is
purely the unvalidated negative reaching Postgres as a 500. A fix touching only `users.ts:344` leaves
five siblings exposed. Standard fix path for this section: validate at handler entry with
`.int().min(0)` on `offset` so it surfaces as a typed 4xx.

### The "four missing by-design 503s" claim was OVERSTATED — only one holds (checked 2026-08-04)

A working note on KS-544 flagged four operations as by-design 503s missing from
`_UNCONFIGURED_503_OPS` in `config/checks.py`. **Do not add them as a block.** Checked against source:

| Operation                           | By-design 503 evidenced?                                                                                                                                                                                                 |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `POST /api/timestamps`              | **Yes** — `timestamping/src/index.ts:268` returns `503 QUALIFIED_TSA_UNAVAILABLE`; the KS-523 comment at `:160` states the request is _"REFUSED (503) rather than silently falling back to a mock/non-qualified token"_. |
| `POST /api/presentations`           | **No** — served by `vc-issuer`, whose only 503 is the generic `errorHandler` status map. No unconfigured-provider path found.                                                                                            |
| `POST /api/billing/checkout/custom` | **No** — the KS-431 provider classifier (`billing/src/routes/billing.ts:57`, _"Billing provider not configured"_ → 503) exists, but neither handler was found calling it.                                                |
| `POST /api/billing/credits/use`     | **No** — same.                                                                                                                                                                                                           |

**The spec is not evidence here.** All four declare `503`, but so do **306 of 318** operations (96%) —
it is boilerplate in the generated error-response set, so a 503 declaration says nothing about whether
an operation 503s _by design when its provider is unconfigured_. Adding the three unevidenced ops
would swap `not_a_server_error` for `integration_5xx_guard` on operations that may be failing
genuinely — masking three real findings to silence one true positive. Add `POST /api/timestamps`
alone, and only after a live run confirms the guard fires; leave the other three failing and reported.

---

## Known Exclusions — Bugs We Explicitly Skip

### EXCLUDE-DOCUMENTS-CROSSTENANT-001 — BUG-ISOLATION-001

**Why excluded:** Schema-level cross-tenant document leak (P0 critical in `Blockchain/Dev/BACKLOG.md`). Scoped to a separate PR (multi-day work: schema migration, RLS policy, ~15 call-site changes).

**Operation:** `GET /api/documents/{id}` with `X-Tenant-Override` header.

**Wire-up:** `schemathesis.toml` doesn't yet have per-operation exclusion syntax (Phase 2). Until then, exclude via CLI: `--exclude-path "/api/documents/*"` for security-focused sweeps, or accept the 200-instead-of-404 as an expected baseline failure.

**Remove when:** BUG-ISOLATION-001 fix ships.

---

### RESOLVED-USERADMIN-CROSSORG-KS467 — user-admin cross-org IDOR (fixed + guard active)

**Status: fixed (KS-467, 2026-07-15).** The Secuura-PK mirror of PS-198. The user-admin surface in
`Blockchain/Dev/services/auth/src/routes/users.ts` previously gated on **role only**, so a
tenant-scoped admin (`ISSUER_ADMIN` / `ORG_ADMIN`) saw **every tenant's** users via
`GET /api/users/admin/list`. The fix scopes the list/organizations endpoints to the caller's own
tenant for tenant-scoped admins (platform admins keep the cross-tenant view), adds an app-layer
ownership re-check on `PATCH /admin/:id` and the verification review (platform-scope read +
`target.tenantId == caller` compare, mirroring the `/lookup` template), and applies a
platform-role assignment ceiling. Verified live against the local multi-tenant seed: a
`default`-tenant issuer sees only its tenant, an `apex` org-admin sees only apex, cross-tenant
PATCH/review return 404, and a platform admin retains cross-tenant management.

**Operation:** `GET /api/users/admin/list` (+ `/admin/organizations`, `PATCH /admin/:id`,
`POST /users/verification/:requestId/review`).

**Wire-up:** The regression lives in `tests/test_user_admin_isolation.py`
(`TestUserAdminOwnershipGuard`) and is now **active** (module skip removed, both disclosure
assertions hard/blocking — the Known Failure markers (recorded as a pytest `xfail`) were dropped
once they became Unexpected Passes — a pytest `xpass` — against the fixed stack). Its pure
disclosure predicate is additionally unit-tested offline in
`tests/unit/support/test_user_admin_isolation.py` (via `tests/support/user_admin_isolation.py`).

---

### EXCLUDE-RH-CROSSTENANT-002 — BUG-ISOLATION-002 bandaid

**Why excluded:** Super-admin RH list endpoint requires `?organizationId=<uuid>` query parameter as a defensive bandaid; without it returns `400 TENANT_SCOPE_REQUIRED`.

**Operation:** Any RH list endpoint when `super_admin` token used without `organizationId`.

**Wire-up:** Mark `organizationId` as `required: true` in `.openapi.ts` (changes the spec), or accept the 400 as documented behaviour (extend `commonErrorResponses[400]` description).

**Remove when:** Schema-level fix ships.

---

### EXCLUDE-503-BY-DESIGN-001 — Integration endpoints that 503 when unconfigured (KS-268)

**Why excluded:** Three integration routes return a declared `503 SERVICE_UNAVAILABLE` — with a human-readable setup message — whenever the backing provider is not configured. Local and dev environments have no M365 licence or billing provider, so these endpoints will always 503 in those environments. Enabling `not_a_server_error` for them would permanently red every local run without indicating a real failure.

**Affected operations:**

| Operation                                                 | 503 message                       |
| --------------------------------------------------------- | --------------------------------- |
| `GET /api/billing/customers/{customerId}/payment-methods` | "Billing provider not configured" |
| `GET /api/onedrive/files`                                 | "M365 integration not configured" |
| `GET /api/teams/webhook-config`                           | "M365 integration not configured" |

**Wire-up:** `schemathesis.toml` — per-operation `checks.not_a_server_error.expected-statuses = ["2xx", "3xx", "4xx", "503"]` for each route (the whole `_UNCONFIGURED_503_OPS` set — 14 operations since KS-544). Added in KS-255 round 3 as `enabled = false`; **re-expressed under KS-1170 (2026-09-15)** because Schemathesis 4.26.1 made the profiles' explicit `--checks` list override a per-operation disable, which left every one of these lines dead from the 4.27.1 bump and the declared 503s redding 14 pairs per sweep. Per-operation `expected-statuses` is merged operation-first and survives the list; it also tolerates only the declared 503, so a 500/502/504 still fails the built-in check here.

**Residual risk:** none for a genuine `500` — it fails **both** `not_a_server_error` (500 is not tolerated) and `integration_5xx_guard`. A 503 with a body other than the declared envelope fails the guard. The one dependency is that the guard is actually selected; since KS-1170 that is pinned offline (`harness.custom_checks` ⇔ the registry, every profile's argv, and the live-CLI functional guard).

**Removal plan (KS-268):** Either:

1. Seed a local/dev test configuration for the M365 and billing integrations so the endpoints exercise their real code paths and return 200; or
2. Teach the harness to distinguish the declared "unconfigured" 503 envelope (known body shape + setup message) from a real 5xx — then gate only on the latter.

Once either approach lands, remove the three `[[operations]]` blocks from `schemathesis.toml` and re-enable `not_a_server_error` for these routes. The Linear ticket [KS-268](https://linear.app/secuura/issue/KS-268) tracks the full acceptance criteria.

---

### EXCLUDE-503-BY-DESIGN-002 — eight MORE unconfigured-503 ops, NOT tolerated on `develop` (KS-693)

**Status: an open floor, not an exclusion yet.** Recorded here because a sweep on `develop` _will_ show
these and they are not a regression. The tolerance lives on PR #809
(`feature/ks-693-tolerate-m365-unconfigured-503`), which is **still open** — so until it merges these eight
operations fail `not_a_server_error` on every local run.

**Symptom:** eight operations answer a declared `503` / `SERVICE_UNAVAILABLE` ("M365 integration not
configured") whenever `ENTRA_*` is absent — which every local stack and every fresh clone is, by design.

**Count:** 8 operations. Measured by Kamil on 2026-09-04 (KS-693 comment; run `pr-2026-09-04T03-09-51Z`,
1,755 cases): tolerating them takes the server-error floor **9 → 1**.

**Where:** `POST /api/m365/connections/init`, `…/connections/complete`, `…/connections/{id}/refresh`,
`…/documents/sync`, `…/outlook/exchange-token`, `POST /api/m365/sites`,
`POST /api/onedrive/files/{id}/sync`, `POST /api/teams/webhook-config`.

**The surviving 1 is a different ticket:** `POST /api/wallets/verify` (`501`, a deliberate fail-closed
decision) — registered above under _The by-design 501 on `POST /api/wallets/verify` (KS-686)_.

**Controls that make 9 → 1 a measurement and not a silent zero** (Kamil, same comment): the eight were
_exercised_, not skipped — NDJSON mentions `m365/connections/init` 3, `m365/sites` 9, `onedrive/files` 5,
`teams/webhook-config` 7; **102 × `503`** responses were recorded across the run; and **no crash file
mentions m365 / onedrive / teams**.

> **⚠ Declaring a 5xx in the spec does NOT stop `not_a_server_error` firing.** Kamil's load-bearing
> correction on KS-693 (2026-08-27), measured against the spec: `POST /api/m365/connections/init` already
> declares `503` and `POST /api/wallets/verify` already declares `501` — **both are still flagged.** The
> built-in check fires on the **5xx class** regardless of what the spec declares; declaration only ever
> satisfies `status_code_conformance`. Any remedy that keeps the response inside 5xx therefore leaves these
> operations red, which is what eliminated the `501` option on evidence rather than on taste.

**Fix path:** KS-693 carries one open ruling for Peter — answer `400`/`422` with the `SERVICE_UNAVAILABLE`
detail preserved (Kamil's recommendation), or mount the routes conditionally so they 404 when unconfigured
(cleanest in the abstract, worst for the KS-663 spec-as-consumed-contract work). PR #809 is labelled interim
and pre-empts neither.

---

### DRIFT-KEYS-ORGID — `organizationId` declared required + `uuid`; the `200` body fails its schema (KS-747)

**Status: measured (KS-1353, 2026-09-28) — see _Measured_ below.** The prediction this entry originally
recorded is settled; its format-enforcement half (U-1) is still unverified. KS-747 merged as `f28cd1fbc` (PR #1318, 2026-09-28) and
declares `organizationId` a **required, `uuid`-format** query parameter on `GET /api/security/keys`, which
the handler already required at runtime. Kamil's merge comment says so plainly: _"**NOT TESTED:** the served
spec … and the Schemathesis `pr` tier — no local stack, and the ticket itself calls the Schemathesis outcome
a prediction."_

**Where:** `services/security/src/security.openapi.ts` → regenerated into `docs/openapi/secuura-api.yaml`
(+7 lines, through the repo's own `generate-openapi`; never hand-edited).

**Why a sweep cares:** a newly-required parameter changes what Schemathesis generates for that operation, so
any movement on `GET /api/security/keys` belongs to KS-747 and **must not be attributed to a Schemathesis
version bump**.

**Candidate follow-up (Kamil's U-1, not filed):** `organizationId` is now _declared_ required and
`uuid`-format, but the handler does not _enforce_ the format. Declaration and enforcement are separate, and
only the declaration moved.

**Measured — the prediction settled (KS-1353, 2026-09-28, slot 3, head `d9ce1403d`, seed 1353).** Three
`full` sweeps on one head, so the numbers describe the spec change and not a version:

Counts are every `GET /api/security/keys` call in the run's NDJSON — the operation's own tests **plus** the
calls stateful chains make to it — split as _own + stateful_:

| sweep                     | calls   | 200s reached | `response_schema_conformance` | `negative_data_rejection` |
| ------------------------- | ------- | ------------ | ----------------------------- | ------------------------- |
| 1 — Schemathesis 4.27.5   | 96 + 6  | 33           | 31 + 1 = **32**               | 5                         |
| 2 — 4.28.0                | 96 + 15 | 36           | 31 + 1 = **32**               | 5 + 1 = 6                 |
| 3 — 4.28.0 + deps refresh | 96 + 17 | 36           | 31 + 1 = **32**               | 5                         |
| 4 — toml loaded           | 96 + 15 | 36           | 31 + 1 = **32**               | 5                         |

On the operation's own tests **every `200` it returned (31 of 31) fails the schema** —
_`"keys" is a required property`_. The `+1` is the same failure reached inside a stateful chain, which the
baseline gate files under the `Stateful tests` label, not under this operation.

- **KS-747 did what it set out to do:** the suite now reaches the `200` branch it could never reach.
- **That `200` body does not match its declared response schema** — 31 of 31 own-test `200`s (+1 stateful) in every sweep, so stable and
  reproducible rather than a draw. A separate spec-vs-runtime defect, visible only now that the branch is reached.
- **The steady `negative_data_rejection` count is consistent with U-1** — a declared-but-unenforced `uuid`
  format accepts values the declaration says to refuse. Consistent with, not proven by: confirming it needs a
  targeted probe with a non-uuid `organizationId`.

---

### DRIFT-OAUTH-ROTATE-SECRET-ID — the `rotate-secret` success response omits `id` (KS-1357)

**Status: tracked as KS-1357** (raised 2026-09-28, assigned to the platform owner, related to the KS-565
register). Reached in one of KS-1353's four sweeps (the third). Recorded here so the next sweep reads it as known rather than new.

**Symptom:** `POST /api/oauth/apps/{id}/rotate-secret` answers `200` with a body that fails
`response_schema_conformance` — _`"id" is a required property`_. The declared schema requires `id`,
`clientId`, `clientSecret`, `name`, `redirectUris`, `scopes` and `createdAt`.

**Count, and why it is rarely seen** (cases exclude the undeclared-method probes sweeps 1–3 sent):

| sweep                          | cases | statuses                  | failing                                                              |
| ------------------------------ | ----- | ------------------------- | -------------------------------------------------------------------- |
| 1 — 4.27.5                     | 27    | 401×5, 400×22             | `positive_data_acceptance` ×22                                       |
| 2 — 4.28.0                     | 27    | 401×5, 400×22             | `positive_data_acceptance` ×22                                       |
| 3 — 4.28.0 + deps              | 49    | 401×31, 400×7, **200×11** | `positive_data_acceptance` ×7, **`response_schema_conformance` ×11** |
| 4 — 4.28.0 + deps, toml loaded | 27    | 401×20, 400×5, 404×2      | `positive_data_acceptance` ×5; **no `200` reached**                  |

Only sweep 3 reached the `200` branch — 11 times, fuzzing phase — and **every one** of those responses violates
the schema. This is **reach onto a pre-existing defect**, not a regression.

**Attribution — settled by sweep 4: it is the draw, not a version.** Sweep 3 was first explained by two
candidates: the dependency refresh (hypothesis 6.168.0 → 6.168.3) or a database earlier sweeps had populated.
Sweep 4 ran on the **same dependencies** as sweep 3, on a still-more-populated database, and drew no valid,
caller-owned app id at all — so reaching the branch depends on which ids a sweep happens to draw. A
deterministic pin (create → rotate → validate the `200`) is the reliable regression check, suggested on KS-1357.

**⚠ Handle the body with care.** Per its own schema `clientSecret` is a **plaintext** secret returned only at
creation and on rotate. Quote the failure message, never the response body.

**Fix path:** the handler's success body should carry the declared fields (or the schema should state the real
shape) — Kamil's call as platform owner. Adding the missing `id` is the likely direction.

---

### DRIFT-AUDITLOG-QUERY-TOLERANCE — `GET /api/platform/audit-log` accepts more than its ruling allows (KS-1359)

**Status: tracked as KS-1359** (raised 2026-09-28, platform owner). The KS-518 / KS-662 ruling tolerates
exactly one violation here — an **unknown** query key (`config/check_predicates.py:355`).

**Symptom:** `by_design_input_tolerance_guard` fails ×30 per sweep, **every one an HTTP 200**: wrong-typed
`offset` / `limit` (20 coverage + 3 fuzzing cases) and values outside their declared minimum / maximum
(7). Smallest repro: `GET /api/platform/audit-log?offset=-1` as the SYSTEM_ADMIN persona → 200.

**Count:** 30 / 30 / 30 / 30 across KS-1353's four sweeps — stable, not a draw. The guard lives in
`check_predicates.py` (hook-loaded), so it ran in every sweep; only `negative_data_rejection` moved
(32 → 0) once sweep 4 loaded the toml exception for the ruled shape — that drop is the ruling being
applied, not a fix.

**Fix path:** validate the query's types and bounds, or widen the ruling deliberately on its ticket.
Never by relaxing the guard.

---

### DRIFT-WALLET-SESSION-DELETE-SUCCESS — the `DELETE /api/wallets/session/{sessionId}` 200 omits `success` (KS-1360)

**Status: tracked as KS-1360** (raised 2026-09-28, platform owner).

**Symptom:** `response_schema_conformance` — _`"success" is a required property`_. The body is
`{"message": "Session disconnected"}`; the declared 200 schema requires boolean `success`.

**Count:** 1 per sweep in all four KS-1353 sweeps — **1 of 1** successful responses every time, so
deterministic. The count is small only because a live session id is rarely drawn (most draws 404).

**Fix path:** add `success: true` to the handler's success body, or correct the published schema.

---

### DRIFT-REQUESTBODY-NOT-REQUIRED — 85 of 145 request bodies are not marked `required: true` (KS-1364)

**Status: tracked as KS-1364** (raised 2026-09-28, platform owner).

**Symptom:** OpenAPI's default is `required: false`, so Schemathesis correctly sends a positive case
with **no body at all**; where the handler needs one it answers 400 and `positive_data_acceptance`
records a failure the contract invited. Example: `POST /api/billing/checkout/custom` → 400
_"quantity: Required"_, in all four sweeps.

**Count (sweep 4):** 85 operations with a non-required body; 40 were sent a no-body case (237 cases);
**17 operations / 35 cases** failed. 15 of those 17 pairs sit in `schemathesis-baseline.json` citing
KS-255, which is Done and archived — so until KS-1364 lands they have no live owner. The other 23
operations accepted the missing body, so the fix is **not** "mark all 85 required".

**Fix path:** mark `requestBody.required: true` where the handler's Zod schema rejects an absent body —
at the generator (`*.openapi.ts` → `npm run generate-openapi`), never by hand-editing the YAML.

---

### HARNESS-BASELINE-LAG — the baseline file lags the Linear registers (KS-1361)

**Status: tracked as KS-1361** (raised 2026-09-28, systemTest owner — no platform change).

**Symptom:** run by hand on sweep 4 (the first KS-1353 sweep with the toml loaded), the baseline gate
finds **90 failing pairs: 53 baselined, 37 untriaged** — all 37 carried on a live Linear ticket, none in
`config/schemathesis-baseline.json`. In the other direction, **44 of the file's 97 entries did not fail**
in sweep 4 (fixed, or not drawn — one sweep cannot tell).

**Why nobody saw it:** KS-752 — `run.py` skips the baseline gate whenever the sweep fails, i.e. on every
real sweep; and before KS-1353's `cwd=` fix, sweeps often ran without the toml (96–99 untriaged in
sweeps 1–3).

**Fix path:** add each tracked pair with reason + ticket + `expires`; retire an unseen entry only after a
second toml-loaded sweep and its ticket's status agree; re-run the gate by hand to **0 untriaged**.

**Reconciled 2026-10-07 (KS-1361), Schemathesis 4.29.4, slot 1.** Three runs: `full` seed 1361 and
`pre-merge` seed 1361 on platform `eef784a32`, `full` seed 1362 on platform `2c27ddfee` (harness
`652cf5f6e`). Before the edit the hand gate read 19 / 11 / 19 unlisted pairs; after it, **0 unlisted,
0 expired, 0 malformed on all three** (165 entries, from 135). 31 entries added (23 of them KS-1414 tool
false positives, see TOOL-FP-POOL-DRAW-NEGATIVE), 9 re-pointed off closed tickets (KS-592 x8 to KS-1015,
KS-686 to KS-627), 43 reworded (the false "owner notified in the merge message" line, and the callback
entry's owner confirmed as KS-1015), 1 retired (`integration_5xx_guard::POST /api/timestamps`, fixed
harness-side per KS-565 and 0 in all three runs). 32 other entries were unseen in all three runs and are
**kept**: no owner says they are fixed. Every entry now expires 2026-12-31 and points at its owner's words
in `config/baseline_kamil.py`, enforced by `tests/unit/runner/test_baseline_kamil_traceability.py`.
The runner still skips this gate on a failing sweep (KS-752), so it was evaluated by hand.

---

### HARNESS-SEED-AND-COMPOSITION — one run is one draw (KS-1680)

**Status: tooling shipped under KS-1680** (`run.py <tier> --repeat N`, systemTest owner — no platform change).

**Symptom:** on one unchanged build (slot 2, platform `c00641f7a`), three `pr` runs found **11, 9 and 8**
unique failures — seeds 4016701351, 3542270494 and 2780863245. Two dropouts were traced to the draw:
`GET /api/admin/audit/export` (run 1's only 200 was `format=json` and broke the schema; run 2's only 200 was
`format=csv`) and `POST /api/referrals/apply` (run 1 reached the success path and got an undeclared 201; run 2
drew only 400s).

**Targeted recheck (2026-10-19, `full` argv restricted to 13 failing operations, seeds 1/2/3):**

| Class                                   | Pairs                                                                                                                                                                                                                                                                                                                             |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Deterministic (3/3)                     | `GET /api/admin/audit/export` ST108 and ST202 · `GET /api/security/audit/{id}` ST108 · `GET /api/security/keys` ST108 and ST201 · `PATCH /api/platform/tenants/{id}/status` ST202 · `POST /api/referrals/apply` ST202 · `POST /api/security/audit` ST202 · `PUT /api/security/keys/admin-scopes/{userId}` ST202 · Stateful tests (`POST /api/m365/connections/complete`) ST202 |
| Seed-dependent (2/3)                    | `POST /api/billing/credits/use` ST202                                                                                                                                                                                                                                                                                             |
| Seen in full sweeps, never in isolation | `GET /api/did/{did}` ST108 · `PATCH /api/did/{did}` ST103 · `GET /api/kyc/microsoft/user/{userId}/sessions` ST108 · `POST /api/m365/connections/complete` (stateless) ST108 · `POST /api/timestamps/verify` ST202 (pre-merge) — inferred dependence on another operation's data, producer not traced                              |

**How to read a run now:** see `running-tests.md` → *Reproducibility: the seed, and `--repeat N`*. Every report
states its seed and whether it was fixed; `--repeat N` turns "absence in one run is not evidence" (KS-565) from a
reading rule into a count; `--compare` will not call a pair fixed unless it went N/N → 0/N on a response-inspecting check and the later set
reached the status it failed on (else *not reached*, or *gone (not proven fixed)* for a check that fails on its status).

---

### HARNESS-SANITIZER-KEY-COLLISION — the positive sanitizer sent a control-byte key (FIXED, KS-1680)

**Status: fixed in KS-1680** (systemTest owner — no platform change; noted on KS-591 and KS-1015).

**Symptom:** `pre-merge-2026-10-23T13-01-26Z-slot1` (slot 1, seed 2796048272) reported `positive_data_acceptance`
on `POST /api/did`: a "schema-valid" request answered **400** `VALIDATION_ERROR` *"Must not contain control byte
U+0012"*. The request as sent (read from the run's NDJSON) carried, under `services[4]`, both a key `"\x12"` and a
key `"_"`.

**Cause:** `config/positive_sanitizer.py` (KS-472) replaces each disallowed control byte in positive-mode bodies
with `_`. For an object key whose cleaned name already existed in the same object, it kept the **dirty** key so as
not to merge two properties — so the control byte was sent, and the platform's correct KS-472 refusal read as a
contract failure. It needs a draw that generates both keys, so it appears and disappears with the seed.

**Fix:** a colliding key now gets another clean, unused name (`_` appended until free): no property is merged and
no control byte is sent in positive mode. `tests/unit/hooks/test_positive_sanitizer.py` —
`test_key_collision_picks_another_clean_key` (the measured `{"\x12", "_"}` shape) and
`test_key_collision_with_several_dirty_keys_stays_distinct` — fail on the old rule and pass on the new one; the
former `test_key_collision_keeps_original` pinned the defect and was replaced.

**So it cannot come back:** `tests/unit/hooks/test_positive_sanitizer_properties.py` states the RULE and lets Hypothesis
hunt for counterexamples on generated bodies — no control byte survives anywhere; nothing is lost or merged; clean
input is unchanged; negative cases go out raw. Three of the four fail on the old rule. Hypothesis also found a second
defect in it: two different dirty keys that clean to the same name (`"\x12"` and `"\x01"`, with no `"_"` present)
were MERGED into one property, silently dropping a value. Both are fixed.

**Live red→green on the same input:** the failing run's operation and seed re-run alone on the fixed harness
(`POST /api/did`, pre-merge profile, seed 2796048272): the same draw came up (same distinctive `services[4]` key),
the control-byte key went out as `"__"`, and the platform answered **201** instead of 400 (64 generated, 64 passed).

**Scope, stated so it is not mistaken for coverage:** the sanitizer cleans request BODIES only. Every 2026-10-23 run
sent 3–6 positive requests with a control byte in the QUERY string; none was refused because of it (the KS-472 rule
covers JSON bodies), so none is a false failure today. If the platform ever starts refusing control bytes in query
strings, those would read as `positive_data_acceptance` failures and the sanitizer would need to cover query too.

---

### TOOL-FP-POOL-DRAW-NEGATIVE — 4.29.x reports `negative_data_rejection` on VALID requests (KS-1414)

**Not a platform defect — do not triage or baseline these as one.** From Schemathesis 4.29.x a
negative case can mutate only the request body and then have a pool-drawn value (captured from an
earlier response) overwrite that mutation, so the request actually sent is **valid** under the
published schema. The platform correctly accepts it; the check still reports _"Invalid data should
have been rejected"_. The case's phase description reads _"Positive test case"_ — the tell.

Measured on slot 4, `develop` `46c3e20cf`, seed 1408 (KS-1408, 2026-10-05), classifying each failing
case by `meta.components` (only `body` negative) + validating the sent body against the spec:

| Run           | `negative_data_rejection` failures | false positives | operations                        |
| ------------- | ---------------------------------- | --------------- | --------------------------------- |
| 4.28.0        | 209                                | 2               | 1 (`POST /api/analytics/exports`) |
| 4.29.3        | 251                                | 55              | 12                                |
| 4.29.3 re-run | 253                                | 61              | 12                                |

KS-1439 (2026-10-07, slot 4, `develop` `147ae4420`, seed 1439 — a different seed and stack state, so not a continuation of the rows above):

| Run           | `negative_data_rejection` failures | false positives (of which body pool draw) | operations |
| ------------- | ---------------------------------- | ----------------------------------------- | ---------- |
| 4.29.3        | 242                                | 39 (24)                                   | 11         |
| 4.29.4        | 222                                | 25 (6)                                    | 8          |
| 4.29.4 repeat | 232                                | 35 (26)                                   | 11         |

**The class is not fixed or reduced by 4.29.4.** The two 4.29.4 runs differ by 10 false positives and by 20 body-draw ones, so the first run's 25 (6)
was the low end of the same-version spread, not a result of the bump. None of 4.29.4's eight `negative_data_rejection` fixes describes the pool-draw mechanism.

**KS-1455 (2026-10-09, slot 4, Schemathesis 4.30.0): measured 0 on two seeds.**

| Run | `negative_data_rejection` failures | false positives (of which body pool draw) | operations |
| --- | --- | --- | --- |
| 4.30.0, seed 1455 | 191 | 0 (0) | 11 |
| 4.30.0, seed 20261009 | 193 | 0 (0) | 11 |

All 23 baseline entries owned by KS-1414 were unseen in both runs. Against 25-39 per sweep on 4.29.x that is a real change, but the
CAUSE is not established: 4.30.0's changelog fixes two neighbouring `negative_data_rejection` false positives (a `before_call` hook
editing another part; a `body.*` override restoring the mutated field) and neither describes the pool-draw mechanism. **The 23 entries
are deliberately NOT removed** - two seeds on one stack is a measurement, not a ruling; remove them per route once a later sweep confirms.

**KS-1476 (2026-10-12, slot 3, seed 1476): still 0 at 4.30.1.** 4.30.1's changelog does name the mechanism this time ("pooled values
were paired with the wrong parent when names differ, such as `id` and `project_id`").

| Run | `negative_data_rejection` failures | false positives (of which body pool draw) |
| --- | --- | --- |
| 4.30.0, develop `524db0ce6` | 189 | 0 (0) |
| 4.30.1, develop `524db0ce6` | 195 | 0 (0) |
| 4.30.1 + hypothesis 6.169.0, develop `aa9ca9de9` | 196 | 0 (0) |

Five sweeps across two versions now read 0. The 23 entries are still kept, because removal is per route and is Peter's call (see the
debt-entry rule); this is the evidence to make it with.
**Closed on the harness side (KS-1414, 2026-10-07).** The classifier used to cover `negative_data_rejection` only, and a path-negative case counted only when EVERY
path value was drawn, so `by_design_input_tolerance_guard` on `GET /api/status/{id}/check/{index}` with `id="0"` (drawn) and `index=127` — both valid under the
published spec (`id` a plain string, `index` an integer `minimum: 0`) — was flagged by the custom guard and never counted. Reading all 12 guard failures on the three
KS-1439 sweeps (slot 4, seed 1439; 2 + 5 + 5): **6 were valid as sent** (`check/{index}`, `revoke`, `unrevoke`, once each in two runs; the `revoke`/`unrevoke` bodies were
drawn over and validate under `StatusListEntryRevokeRequest`) and **6 were genuine** (`GET /api/platform/audit-log` with `limit=201`, maximum 200 — KS-1359, Kamil). The
guard now passes a request valid as sent, and the classifier counts the guard's failures and passes, with one rule shared by both
(`config/valid_as_sent.py`, `parsing/path_parameter_schemas.py`). The `audit-log` failures stay failures.

Most frequent: `POST /api/governance/participants/register` (12/12), `POST /api/security/events`
(8/8), `POST /api/security/rate-limit/reset` (6/6), `POST /api/transfers` (5/5). Kept **visible** —
no harness filter, no baseline masking (truthful-gate rule). Re-check on every upstream release; the
full method and operation list are on KS-1414.

**Baselined under KS-1414, narrowly (KS-1361, Peter's decision 2026-10-07).** A pair is baselined as
`ticket: KS-1414` only when **every** failing case of that pair, in **every** KS-1361 run, was counted by the
classifier as valid as sent: 23 pairs. Prior behaviour: no KS-1414 entry existed, so each sweep reported
these as NEW and the hand gate could never reach 0. They stay **visible**: the console, `results.json` and
the HTML report still count them, and a pair that also has a genuine failing case is not covered (e.g.
`PATCH /api/did/{did}` stays under KS-1015 because sweep 1 had 5 genuine cases). Each expires 2026-12-31.

### HARNESS-SUPER-ADMIN-PERSONA — five "cross-tenant disclosure" failures that were a mis-provisioned persona (FIXED, KS-1353)

**Status: fixed in systemTest on 2026-09-28.** Recorded because the failure messages named real security
tickets (KS-467, KS-513) and read as platform regressions. They were not.

**Symptom:** under the gate (`systemTest/run-in-slot.sh`), five live-integration tests failed with messages
such as _"KS-467 cross-tenant disclosure: the tenant-scoped ISSUER_ADMIN sees 15 users vs the super-admin's 15"_
and _"KS-513 cross-tenant api-key disclosure …"_ — plus the audit-log tripwire answered _"Super-admin access
required"_ to its "SYSTEM_ADMIN" client.

**Cause:** the tests' super-admin came from `TEST_CREDENTIALS["admin"]`, which `tests/conftest.py` itself says is
an `orgAdmin` **stand-in** whenever the generated-actor manifest exists. Measured: in a plain shell it resolved to
`admin@secuura.com` (SYSTEM_ADMIN); through the slot runner, to `ks256-orgadmin-local@secuura-test.invalid`
(**ORG_ADMIN**). The platform then did exactly what it should to an ORG_ADMIN — scoped its user list to one
tenant, ignored its `X-Tenant-Override`, refused the platform audit log. Nothing leaked; and while the persona was
wrong, **none of those tests was testing isolation at all.** KS-969 tracks the wider actor-path gap.

**Fix:** `tests/support/platform_admin.py` resolves a genuine platform admin (explicit `TEST_ADMIN_*`, else the
bootstrap SYSTEM_ADMIN via `BOOTSTRAP_ADMIN_PASSWORD`, never the stand-in) and **verifies the role from the issued
token**, failing as a named precondition otherwise. Same five modules, same invocation: `HEAD` 5 failed / 22 passed
/ 2 errors → **29 passed**, none skipped. With a real super-admin the platform's isolation holds.

**The two errors in the same run** were not this: KS-692 (2026-09-28) ruled `ISSUER_ADMIN` out of status-list
writes, so the by-design tripwires now allocate/revoke/unrevoke as a platform admin.

---

## COVERAGE-CSRF — write paths were invisible to the sweep until 2026-07-11 (KS-428, RESOLVED)

**Resolved 2026-07-11** — the gateway's CSRF guard (`services/api-gateway/src/middleware/csrf.ts`)
was inverted: it skipped CSRF when there was _no_ `Authorization` header and enforced it when
there _was_ one. CSRF defends against ambient authority (cookies the browser attaches
automatically); a bearer token is never auto-attached, so bearer requests are the ones that
need no check. The KS-428 fix applies exactly that rule: header-credentialled requests
(Bearer / `x-api-key`) and cookie-less requests skip CSRF; only cookie-bearing requests with
no header credential get origin + double-submit validation.

Why this entry stays in the document: **every sweep recorded before 2026-07-11 covered read
paths only.** Each mutating request carried a bearer token and was rejected with
`403 CSRF_TOKEN_MISSING` before reaching a handler — measured on one `full` run's HAR: 7,135
such 403s (POST 6,086 · PATCH 563 · DELETE 389 · PUT 97, i.e. all of them) against 76 `200`s
out of 13,004 requests. `403` is an accepted status for `positive_data_acceptance`, so those
runs reported `315 operations · 0 failed` while never exercising a create, update, or delete.
Do not treat a pre-2026-07-11 green as evidence about write behaviour, and expect the first
post-fix sweeps to surface findings on write paths that had never been exercised before —
those are new _visibility_, not new _regressions_.

The first post-fix sweep (2026-07-11) confirmed the prediction and its findings are tracked:
**KS-430** (request-schema contract drift on 60 write operations — the KS-423 class at scale,
plus 3 errored ops, 8 environment-expected M365 503s, and the stateful-phase repeats) and
**KS-431** (16 write operations returning raw `500 INTERNAL_ERROR` — the KS-421 class).
Until those two land, a sweep that fails **only** on operations listed in KS-430/KS-431 is
reporting the known-open backlog, not a regression introduced by the change under test —
read the failure list against those tickets before treating a red as blocking.

---

## COVERAGE-LOGOUT — the sweep revokes its own session (handled, worth knowing)

The spec exposes `POST /api/auth/logout`, so the sweep fuzzes it with the very bearer token
the persona-auth hook is using — 29 times in one observed run, the first within the opening
dozen requests. Each call revokes the session server-side while the JWT remains unexpired by
its own `exp` claim.

The `after_call` hook therefore cannot decide "is this token dead?" from `exp` alone. It
reads the 401 body: `SESSION_INVALIDATED` / `TOKEN_EXPIRED` / `TOKEN_REVOKED` mean re-login;
any other code (a scope or tenant refusal on a still-valid token) means keep the token, so
the login endpoint is not stormed. See `_REVOKED_TOKEN_ERROR_CODES` in `config/hooks.py`.

This is _not_ a platform bug — logging out when asked to log out is correct. It is a property
of fuzzing an API that can revoke its own credentials, and the harness must expect it.

## COVERAGE-LOCKOUT — the sweep could lock its own principal (handled, KS-575)

The sibling of the above one level out: the same fuzzing that revokes its own _session_ can also
lock its own _credential_. The F-06 account lockout (`services/auth/src/services/accountLockout.ts`)
counts consecutive failed logins per `(email, source /24)` and locks the account for 15 minutes at 5.
Schemathesis 4.x reuses values from earlier responses, and the persona's own address comes back from
`GET /api/users/me` and the admin listings — so the fuzzing phase fed `admin@secuura.com` plus wrong
passwords into `POST /api/auth/login`: **three consecutive 401s** in `pre-merge-2026-09-14T12-56-17Z-slot3`
(HAR #10937–10941), from the one `/24` every harness request shares. Five in a row before a hook login
resets the counter locks `super_admin` for 15 minutes — the intermittent ~50 % self-lockout KS-575
measured on 2026-08-25, which read as a stale token or a broken seed because the platform answers a
locked account and a wrong password with the same 401 (F-11). The ticket's original mechanism
(`change-password`) was wrong: that route never touches the lockout.

Handled by `config/principal_shield.py`: on the two lockout doors only (`POST /api/auth/login`,
`POST /api/oauth/authorize`) a body `email` naming a harness principal is rewritten to
`ks575-shield+<local>@secuura-test.invalid` — same request, same door, same fuzzed password, same
401; only the account charged changes. Nothing is excluded: the same run also locked the spec's inline
example `demo.issuer@example.com` (5 × 401 at #656–660), which is the control working on an account
nobody owns. `fixtures.login` now names both causes on a persona 401 and the auth-log line
(`blocked by account lockout`) that separates them. `tests/test_account_lockout_shield.py` pins the
control live on a throwaway account (5 bad logins → correct password refused) and the diagnosis.
Raising `LOGIN_LOCKOUT_THRESHOLD` locally was rejected — masking a pen-test control by configuration.

---

## How to Extend This Document

When a baseline run surfaces an expected failure:

1. Add a section with a stable `DRIFT-…` or `EXCLUDE-…` identifier
2. Include: Symptom + Count + Where + Fix-path / Wire-up
3. Cross-link to BACKLOG.md or Linear issue if tracked elsewhere

Schemathesis re-runs that surface a new pattern not listed here = regression signal.

---

## Next Steps

- [Running Tests](running-tests.md) — How to run your own baseline
- [Contributing Guide](contributing.md) — Adding tests and fixing drifts
- [Getting Started](getting-started.md) — Environment setup

---

**Last Updated:** 2026-09-28

## KS-1607: Schemathesis 4.31.1 → 4.32.1, measured before and after (2026-10-19)

**Host and setup:** this Mac (arm64), Docker Desktop 8 CPUs / 31.3 GiB, platform-k slot 2, platform at `c00641f7a`. `full` tier, **fixed seed 1607** for
both, the second started 60 min after the first (the `/auth/register` limit). Console, verdict and WFC were reconciled by hand because the gates read
NOT EVALUATED once a sweep fails (KS-752).

| | 4.31.1 (before) | 4.32.1 (after) |
|---|---|---|
| Started / wall clock | 15:21Z / 1,232 s | 16:21Z / 1,234 s |
| Test cases | 17,845 generated, 95 found | 17,921 generated, 92 found |
| Unique failures | **101** | **98** |
| Skipped / errored | 441 / 0 | 435 / 0 |
| Operations tested | 345 of 347 | 345 of 347 |
| Failing (check, operation) pairs | 91 | 86 (83 in common) |
| Console = verdict | agree | agree |
| WFC | entries 98 = distinct 90 + 8 repeats; totalNumber 90 (= distinct); verdict predicts 99 entries (informational gap of 1) | entries 96 = distinct 88 + 8 repeats; totalNumber 88 (= distinct); verdict predicts 96 entries |
| Warnings | missing_auth 19, base_url_mismatch 72, missing_test_data 55, validation_mismatch 14, rate_limited 7 | 19, 67, 46, 10, 5 |

**Reading it, with the caveats the earlier bumps taught (KS-565, KS-1439):**
- **101 → 98 unique failures and 91 → 86 pairs are inside the same-version spread** (4.29.4 ran 113 vs 121 on one build, KS-1439). The 8 pairs only in
  the before run and the 3 only in the after run are **not evidence of a fix or a regression**; the generated cases differ between versions even on one seed.
- Pairs only in the **before** run: `positive_data_acceptance` on `DELETE /api/platform/tenants/{id}`, `POST /api/oauth/apps`, `POST /api/platform/tenants`,
  `POST /api/security/keys`, `PUT /api/security/keys/admin-scopes/{userId}`; `response_schema_conformance` on `GET /api/kyc/microsoft/session/{sessionId}`,
  `POST /api/oauth/apps/{id}/rotate-secret`, `POST /api/verification/verify`.
- Pairs only in the **after** run: `positive_data_acceptance` on `PATCH /api/platform/tenants/{id}/status`, `POST /api/billing/credits/use`;
  `status_code_conformance` on the pseudo-operation `Stateful tests` (observed, cause not established: `UndefinedStatusCode` rose from 3 to 4
  operations in the same run, which fits a stateful-phase failure but was not traced to a case).
- **Failure codes appear in the verdict** (`ST101` server error, `ST103` undocumented status, `ST108` response violates schema, `ST201`/`ST202` accepted
  negative / rejected positive data, `ST901` custom checks). Failure **titles** were renamed (`API rejected schema-compliant request` → `Schema-valid request
  rejected`); no harness parser keys on a title.
- `schemathesis-failures-pytest.py` held **92** tests = the 92 failing cases found, and the report links it.
- **Stateful numbers:** neither console prints a scenario count. The after run's NDJSON-completeness gate reads "345 operations across 1145 scenarios";
  the before run's figure was not extracted, so no stateful coverage movement is claimed (KS-1442 and KS-188 stay as they were).
- **New finding, recorded not fixed:** the KS-1408 WFC total rule reads 89 expected vs 90 reported when the stateful phase records a failure (the verdict
  files it under `Stateful tests`, WFC under the real endpoint) — appended to KS-1674 with the 24-vs-23 listing finding.

## KS-1641: the m365 OAuth callback — seven hard reds by design (2026-10-26)

`tests/test_m365_callback_redirect.py` drives the public `GET /api/m365/callback` (spec `security: []`) through the gateway with an
anonymous client, redirects not followed, on the three branches a local run can reach: no parameters (`missing_code_or_state`), a
provider `error=access_denied`, and a `code` with an unknown `state` (`invalid_state`).

| Cell | Asserts | Measured on develop `8661f5d41`, slot 1, 2026-10-26 |
|---|---|---|
| `test_ks1641_redirect_targets_a_declared_admin_route` ×3 | the `Location` path, under the `/admin` basename, is a route the admin app declares (the list in KS-1641) | **red** ×3 — all three go to `/admin/integrations`, matched as `/integrations`, which is not declared (finding 1) |
| `test_ks1641_error_description_never_reaches_the_redirect` ×3 | a 5,000-character, a phishing-prose and an emoji-at-the-200th-code-unit `error_description` never appear in the `Location` | **red** ×3 — #1622 caps the text at 200 code points but still reflects it (finding 2) |
| `test_ks1641_oversized_description_keeps_the_redirect_bounded_and_the_service_up` ×4 | the same inputs plus 400 astral code points still get a 302 with a `Location` of at most 2,500 characters, and the service answers the next callback | pass ×3; **red** ×1 on `[400-astral-code-points]` — the nginx edge answers **502** (below) |

**The edge 502 (found by this file, 2026-10-26).** With 400 astral code points (capped to 200 by #1622) m365 answers 302 and api-gateway
passes the 302 on, but `secuura-nginx-gateway` logs `upstream sent too big header while reading response header from upstream` and the
caller gets `502 BAD_GATEWAY`. The `Location` is about 2,460 characters; with the gateway's other response headers the total exceeds the
edge's response-header buffer (no `proxy_buffer_size` is set, so nginx's default applies — assumed one 4 KB page, not verified). 150 astral
code points still pass (302, `Location` 1,860, headers ~3,676 bytes). Nothing crashes: m365 kept `RestartCount` 0 and the next callback got
302. It is a consequence of finding 2 (a bounded but still large reflection) and disappears if only a short code goes on the URL. Proposed as
its own platform-k ticket, related to KS-1641; until raised, a red here matches KS-1641.

**Decision (Peter, 2026-10-26): the seven defect reds are hard failures, not `xfail(strict=True)` Known Failures** — "do not mask failures, we
need to be honest", and for the edge 502: "Keep it honest". They are red on every run until the platform fix (owned outside systemTest)
lands; a red on these seven is expected. Any other failure in this file is new and must be triaged. Each cell first asserts it reached the
intended branch, so a red is the defect and not a different response.

**Not covered:** the success redirect and the token-exchange-failure redirect. Both need a state from `POST /api/m365/connections/init`, its
browser-binding cookie and a real Microsoft code exchange, which no local run can produce. The route list is the ticket's; if the fix adds a
route instead of repointing the redirects, update `ADMIN_DECLARED_ROUTES` from the ticket or the fix's PR, not from the router source.

## KS-1674: the object_level_authorization leg — first live findings (2026-10-20)

First live run of the leg (slot 2, run `full-ks-1674-2026-10-20T10-52-16Z-slot2`, branch `8a203488b`, Schemathesis 4.32.1, seed 1674):
259 peer replays between `owner` and `ownerPeer` (two OWNER users in ONE tenant), **6 ST402 violations**, equal in the leg's NDJSON and its
JSON verdict. Filed as **KS-1703** (assigned to Kamil; found under KS-1674, part of Review A, KS-486).

| Route | Case id | What the code does |
|---|---|---|
| `GET /api/transfers/{id}` | `1U6qU1` | `SELECT * FROM svc_transfers WHERE id = $1`; no caller, no tenant (`transfer/src/index.ts:247-251, 649-661`). Its list `GET /api/transfers` is ALSO unscoped: it returns every transfer unless the caller supplies their own `?ownerId=` (`:602-643`) |
| `GET /api/transfers/{id}/history` | `9JG2nb` | same lookup (`:904-922`) |
| `GET /api/delegations/{id}` | `7mMh5M` | never reads `req.user` (`transfer/src/routes/delegations.ts:139-143`); the list route filters on `delegatorId`/`delegateId` |
| `GET /api/analytics/exports/{id}` | `rVMsIL` | in-memory map, the type has no owner or tenant field (`analytics/src/routes/analytics.ts:334-338`) |
| `GET /api/governance/participants/{id}` | `eiqPHs` | lookup by id or wallet address, no tenant field; gateway mount has optional auth |
| `GET /api/security/audit/{id}` | `grR2ha` | tenant-scoped only (`security/src/index.ts:898-910`) |

**Not measured:** cross-tenant exposure (the local stack cannot place a user in a second tenant; five of the six handlers have no tenant
filter, so it is likely). **Open ruling:** whether same-tenant OWNER users may read each other's analytics exports, governance participants
and audit entries. Transfers and delegations look like defects: the mutating routes of both services use the authenticated caller, and the delegation list is scoped to it. (An earlier version of this section said the transfer LIST was scoped to the owner too; it is not, which is a second exposure in KS-1703.)

Until the routes are fixed or the six `object_level_authorization::<operation>` pairs are triaged in `config/schemathesis-baseline.json`
(a ticket and an owner each), every `pre-merge`/`full`/`nightly` run FAILS on the leg — by design, not a harness fault.

**Decision (Peter, 2026-10-20): the six pairs are NOT baselined.** They are real product findings, so the leg's gate stays red until KS-1703
is fixed or ruled on, rather than being turned green by triage entries. A red leg on these six pairs is therefore expected; any OTHER leg
failure, or a seventh pair, is new and must be triaged.

Same run, **classified afterwards by a control run** (develop's own harness, `32964477f`, same slot, seed 1674; see below): 5 main-sweep pairs not in the baseline — `positive_data_acceptance` on `GET /api/admin/audit/export` (x10),
`POST /api/security/keys` (x3), `POST /api/timestamps/verify` (x2), `PUT /api/security/keys/admin-scopes/{userId}` (x7), and
`response_schema_conformance` on `GET /api/admin/audit/export` (x1); and 2 live integration failures —
`test_cross_tenant_isolation` (BUG-ISOLATION-001, above) and `test_api_key_cross_tenant_isolation` (KS-513).
The report-reconciliation and console-vs-verdict gates, skipped by the run (KS-752), agree when run by hand: 102 unique failures, 17,485 cases.

**Control run (2026-10-20): none of these is caused by KS-1674.**
- The two integration failures fail identically from develop's harness: **pre-existing product defects**, filed as **KS-1704** (Kamil; the
  tickets they guard, KS-4 and KS-513, are Done). Not the KS-1054 fresh-database window: `039` and its `038a` fix applied on boot 1.
- `GET /api/admin/audit/export` x10 (`from`/`to` required) and x1 (no `entries` key) fail identically on develop: spec drift already owned by
  **KS-1645** (its table rows 1 and 4).
- `PUT /api/security/keys/admin-scopes/{userId}` (7 vs 5 on develop), `POST /api/security/keys` (3 vs 3) and `POST /api/timestamps/verify`
  (2 vs 0, sampling): every case sent no body, which the spec does not mark required — the KS-1364 class, plus a `POST /api/security/keys`
  schema with no properties. Filed as **KS-1705** (Kamil).
- Control-run caveat: that worktree bootstrapped its own `Blockchain/Dev/.env`, and its anchoring tests recreated slot 2's originate from it
  (unhealthy), so the control's anchoring results (9 of 28 failed) are invalid. None of the routes above is served by originate.
  **Do not let a control worktree bootstrap its own platform `.env` while it drives another worktree's stack.**

**Reproduced without the sweep.** `tests/test_get_by_id_object_authorization.py` creates each object as `owner` (the owner reads it back, 200, in a
fixture) and reads it as `ownerPeer`. With the `xfail` markers disabled (`--runxfail`) all six FAIL with `assert 200 in (403, 404)`: the second
user got HTTP 200 on every route (slot 2, 2026-10-20). Normally the six report as xfailed against KS-1703 (strict, `raises=AssertionError`),
so the run is not red for them but they flip the moment a route is fixed. Transfers use throwaway party ids, so neither peer is a party to the
transfer they could read. Three are marked as confirmed defects; analytics, governance and audit are marked "ruling pending".

**Operator trap found while doing this.** Running `quality` with a live named slot exported (`SECUURA_STACK_SLOT=2` and the stack up) makes its
pre-suite step try to re-provision; without `BOOTSTRAP_ADMIN_PASSWORD` it cannot verify the actors and moves `fixtures/generated/actors-slot<N>.json`
aside as `actors.superseded-…` (the harness's protective behaviour), after which every test that needs the generated actors has no credentials.
Restore by renaming the superseded file back. To run `quality` offline, name a slot whose stack is down.

