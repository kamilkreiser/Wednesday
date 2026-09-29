<!-- ⚠️ Keep the "Before merging" block and the two acknowledgment checkboxes below —
     they appear on every PR by design and the pr-premerge-ack workflow parses them. -->

> ## ⚠️ Before merging — run the pre-merge suites
> **Do not merge until the pre-merge tests have been run and pass.** The fast PR
> gate is not sufficient on its own. Run each suite's pre-merge tier — locally
> against the stack, or by dispatching **`pre-merge-platform-suites.yml`**
> (Actions → *pre-merge* → *Run workflow*) — confirm it is green, then tick its box.

### Pre-merge acknowledgment (author)

Tick each box **only after** you have run that suite's pre-merge tier and it passed:

- [ ] <!--ack:schemathesis--> **Schemathesis** pre-merge sweep run and **passing** (`python3 scripts/run.py pre-merge`)
- [ ] <!--ack:akto--> **Akto** pre-merge scan run and **passing** (`npm run test:pre-merge`)

### PII review (KS-256 R15/R16)

<!-- KS-256 · KAMIL-REVIEW 2026-07-20. Why he asked for it, verbatim: "put the PII-review sign-off
     as a checkbox in the PR description so it's auditable, not implicit."
     These boxes deliberately carry NO ack marker:
     pr-premerge-ack.yml matches only ack:schemathesis and ack:akto, so this is a human gate, not
     a CI-enforced one. Do NOT write a literal ack comment marker anywhere in this block — an
     inner comment-close would terminate this comment early and render the remainder as visible
     text in every PR. Delete the section only if the PR genuinely cannot touch published data. -->

Tick if this PR changes **anything that reaches a customer-facing artifact** — the published
OpenAPI spec, example values, fixtures, seed data, logs or error messages:

- [ ] **No real personal data ships.** Emails, names, phone numbers, addresses, wallet/stake
      addresses, government or tax IDs, and free text captured from real traffic are placeholdered
      — not merely "looks fake to me".
- [ ] **No credentials ship.** No password, token, API key, secret or private key, including in an
      example that "obviously isn't real".
- [ ] **Reviewed by the person who worked the redaction queue**, not just the author. Name them:
      <!-- @who -->

> Not applicable? Say so explicitly rather than leaving the boxes blank — a blank box reads as
> "not checked", which is the state this section exists to make visible.

---

**PII review: not applicable** — this PR changes systemTest harness code, tests and docs only; nothing reaches the published spec, examples, fixtures, seed data, logs or error messages of the platform.

## Linear

https://linear.app/secuura/issue/KS-1386

## Summary

**No systemTest harness hard-codes or silently defaults a stack slot any more.** Every entry point that touches a stack refuses a LOCAL run that names no slot (CI and remote targets stay exempt, but with no slot and no URL there is no default target anywhere). An exempt run is labelled `unslotted`, never `slot1`. No slot 2–4 value is typed in code, tests, example files or docs — every slot value is derived from the slot-1 base.

Covers all harnesses: api-explorer, fixtures + shell suites, Playwright, Performance, Akto, Schemathesis.

Also on this branch (same ticket, at Peter's direction):
- Akto's offline gate never spawns docker (injected command runner); no script prints part of the API token; api-explorer's golden snapshot is tracked and portable.
- Schemathesis offline suites no longer write into the real `output/reports/` (three tests did; a per-test guard now fails any that do).
- Akto and Performance no-slot refusals name the npm script that was run (`npm run test:pr`, not a fixed example); Performance scripts call `tsx`, not `npx tsx`, so the name survives.
- Docs: every stack-touching example command names its slot (`SECUURA_STACK_SLOT=1 …`); false "defaults to slot 1" statements corrected; the fictional `update-visual-baselines` / visual-testing steps removed, with a guard that every `npm run` in a doc exists.

Split out (not in this PR): KS-1389 (`slot-target.sh` / pre-push / preflight leg 13 — Kamil), KS-1388 (`observability/`).

## Test Evidence

**Touched:** `systemTest/**` (all six harnesses, shell suites, docs) and two `Projects Documents/*.html`. No service, spec, migration or deploy file.

**Ran (local, the Mac, 2026-09-29, at this branch's head):**

| gate | result |
| -- | -- |
| api-explorer `npm run quality` | 130 / 130 |
| Playwright `npm run quality` | 387 / 387 |
| Performance `npm run quality` | 1,353 / 1,353 |
| Akto `npm run quality` | 1,825 / 1,825 (no real docker call) |
| Schemathesis `run.py quality:static` + `pytest tests/unit tests/functional` | green; 2,922 passed |
| `systemTest` typecheck · format gate | 0 errors · 4/4 |
| shell suites (`run-shell-suites.sh`) at `eac2dae2a` | 64 passed, 0 failed, 1 skipped (ks949 — no PostgreSQL on this Mac, documented) |
| slot-literal guard · doc-script guard | 6/6 · 6/6 |
| pre-push preflight | PREFLIGHT PASSED — 15/15 legs ran |
| **mutation check** — 17 deliberate breaks of the risky guards | **17/17 caught** (each suite went red; files restored, SHA-verified) |

**Live, slot 1** (stack built at `8af6ab821` — `develop` does not build, KS-1380):
- Every harness refused an unslotted run; the slot-1 gateway logged **0 requests** during those checks. Akto and Performance refusals name the script run (`npm run test:pr`, `npm run test:load`).
- api-explorer Local/quick-start URLs answer 200; `pre_suite` live 31/31.
- Schemathesis `pr` tier, `SECUURA_STACK_SLOT=1`: 10 failures, all 3,909 requests to slot 1's gateway. A `develop` control with the same seed shows the same 7 new `response_schema_conformance` pairs — none introduced here (recorded on KS-1015).

**NOT run:**
- Schemathesis **pre-merge** sweep and Akto **pre-merge** scan — running next on slot 1; boxes above stay unticked until they pass.
- Playwright / Performance / Akto full suites live (entry-point refusals and targeting only).
- Anything on slots 2–4.

**Migrations / config:** none. `akto/.env.example`, `playwright/.env.example` and the Schemathesis yaml lost their per-slot tables and slot-1 defaults; Performance `package.json` scripts `npx tsx` → `tsx`.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
