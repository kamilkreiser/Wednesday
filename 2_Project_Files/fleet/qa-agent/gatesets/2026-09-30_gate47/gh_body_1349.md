## Why this change exists

Kam's instruction, verbatim (live board, relayed by Tuesday):

> **16:17:55** "Peter has responded to KS-1374 on WhatsApp. can you please make the change"
> **16:18:57** "his reply was for us to implement the change"

"The change" as shipped in #1347 was: raise the pacing limit on LOCAL stacks only, demo and
production as deployed. **N-1347-11 is where #1347 still fell short of "local only".**

## The finding this closes

**N-1347-11** (gate45 report `:329`, evidence `evidence/probeB_loader.*`, `probeC_hostforms.*`,
`dotenv_order_target.*`, at
`Testing Agent MAIN/projects/secuura/reports/2026-09-29-batch1348-g45/report.md`).

`isLocalScanTarget()` read `SECUURA_API_URL` alone, but the host akto-testing is actually pointed at
is `config.overrideAppUrl || config.secuuraUrl` (`systemTest/akto/src/scan/scanOptions.ts:98`). So a
scan aimed at the demo through `OVERRIDE_APP_URL`, with `SECUURA_API_URL` local or unset, read the
target as LOCAL and paced at **7500/min against a stack that allows 2000** — gate45's measurement.
develop before #1347 paced the same configuration at 1500.

It is reachable by editing the one variable the docs invite you to edit
(`systemTest/akto/.env.example:123`, `configuration.md:424`), and `slot-target.sh:102` keeps a remote
OVERRIDE while resetting SECUURA to the slot's localhost.

**Why it was Minor and not blocking:** reaching it needs a split configuration in which the harness
logs in to the LOCAL stack (`secuuraAuth.ts:70`) and attacks the remote one with local tokens, so
such a scan is already invalid. The documented demo profile sets both variables, and every CI
workflow paces correctly.

## The fix

One product line — the same precedence `scanOptions.ts:98` already uses for the host it attacks:

```ts
const raw = env('OVERRIDE_APP_URL') || env('SECUURA_API_URL');
```

plus the function's docstring and `@example`, updated only where they became false. This is the trap
KS 687 fixed in pre-flight, which probed `host.docker.internal` while the scan attacked something
else: the question "what are we scanning?" now has one answer in this package instead of two.

Every existing contract is kept: both unset → local (the slot default); a malformed URL → NOT local
(paces at 2000, never faster); `AKTO_PLATFORM_REQUESTS_PER_MINUTE` still overrides for any target;
`Math.max(1, …)` stays.

**Measured, not reasoned:** `isLocalScanTarget()` takes no arguments, so no caller can hand it a
`toDockerUrl`-rewritten host, and `toDockerUrl` touches only the `localhost` token
(`scanOptions.ts:96-97`). An operator-set `OVERRIDE_APP_URL=http://host.docker.internal:6882/api`
therefore reads NOT local and paces at 2000 — slower than intended, the safe direction. Pinned as
RED-4 rather than left as an argument.

## Test Evidence

**Touched:** `systemTest/akto/src/setup/aktoRateLimit.ts` (+21/−6),
`systemTest/akto/tests/unit/setup/ks1374-n1347-11-scan-target-override.test.ts` (new, +212).
Two files. No gateway, compose, bicep or env-template line moves.

**Ran** (every count named with the SHA it was measured on):

- Baseline at develop `8c810023f9c9`, measured here and not quoted from the gate: **93 files / 1654
  tests, 0 failed.**
- **Red-first on the final cell text: 4 failed / 5 passed.** The four are RED-1..RED-4 by name; all
  five controls green. 4-and-5 rather than 0-and-0, which would have been a load failure — the cell
  imports only symbols develop exports.
- **Green with the fix: 9/9.** Whole unit suite at `daab8ff3bff5`: **94 files / 1663 tests, 0
  failed** — exactly +1 file and +9 tests over baseline, so nothing else moved.
- **Tamper arm.** Anchor uniqueness proved first (1 occurrence; control: `const raw = ` occurs twice,
  so a looser anchor would have been refused). Reverting the product to its passing pre-fix value
  reddens exactly RED-1..RED-4 and leaves the five controls green. Restored **byte-equal**, sha256
  `5cd96cbac429cf70e3f8e24c` both sides; green again 9/9.
- `npm run lint` **rc 0** (tsc + eslint + stylelint), `prettier --check` rc 0 over src and tests.
  Each rc measured directly, not read off `$?` after a pipe.

**A correction to my own first draft, because the counts moved:** three arms were first labelled
CONTROL — the malformed-URL arm, the `host.docker.internal` arm, and an `isLocalScanTarget()`
assertion inside C5. All three were RED at develop, which makes them red-first arms, not controls; a
control that fails before the fix proves nothing about the fix. Red went 5 → 4 and green 4 → 5, and
C5 now asserts only the pace, which is 3000 on both sides because the override variable returns
first. eslint also found three real errors in the first draft of the cell
(`@typescript-eslint/no-dynamic-delete` on a computed-key `delete`); fixed by matching this package's
own idiom — 64 literal-key deletes across `tests/unit`, and `Reflect.deleteProperty` appears nowhere
— rather than by suppressing the rule.

**NOT run, and why:**

- **The pre-push preflight's 15 legs did not run in-hook.** The hook fast-skips a systemTest-only
  push by design (`.githooks/pre-push:5`, and `[ -z "$changed" ] && exit 0` at `:254`); both changed
  paths are under `systemTest/`, verified, with #1348's non-systemTest paths as the control. What did
  run in-hook is the KS 989 systemTest formatting gate: **1 package checked, 0 skipped, 0 failed.**
- **So the two audit legs were RUN BY HAND against this head instead**, rather than left unclaimed.
  Both on `daab8ff3bff5`, each rc measured directly:
  `npm run audit:gate` **rc 0** — 23 distinct advisories reported, 25 baselined, "no advisories
  outside the triaged baseline"; `npm run audit:locks` **rc 0** — 43 standalone lockfiles, 1612
  packages pinned, 18 advisories matched and all 18 already baselined.
  The gate also emits an advisory-only CLEANUP note: two baseline entries are no longer reported
  (`GHSA-v2v4-37r5-5v8g`, KS 470, and `GHSA-mwp4-54f8-5fhr`, KS 729). That cleanup is owed but is
  **out of scope here** and no baseline row was touched by this PR.
- **No Akto scan was run against any stack.** The behaviour is unit-proven only.
- The other three platform suites (Schemathesis, Playwright, Performance) were not run: this change
  is confined to the Akto harness's own pacing helper and touches no API surface.

**Migrations + config:** none. No migration, no `.env`, no compose, no bicep, no env template.

## NOT COVERED

- A remote stack reached through a localhost port-forward or SSH tunnel still reads as local. Stated,
  not built for; `AKTO_PLATFORM_REQUESTS_PER_MINUTE` is the operator's answer there and still
  outranks every target check.
- **The demo's real `RATE_LIMIT_MAX_REQUESTS` is still unread** — its environment file is not in this
  repository. `services.bicep:681` sets 2000 for `dev` and 100 otherwise.
- `systemTest/akto/.env.example` and `configuration.md` are deliberately unedited. The comment at
  `.env.example:123` is about URL derivation, which this change does not alter.
- A CI stack counts as local by Wednesday's reading, because `internal-audit.yml:94` copies
  `env.example` to `.env`. Kam's word overrides that if he reads it differently.

Refs KS-1374
