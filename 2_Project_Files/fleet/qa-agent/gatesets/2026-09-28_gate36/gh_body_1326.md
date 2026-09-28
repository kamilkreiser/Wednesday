#1326 KS-1351 item 1: declare the revocation fields on a Secuura status extension
head 3f569dfc701c757253aa71ed8b91b81ce9c84c93

## What this is

**Item 1 of this ticket, and only item 1** (plus its item 2, the one-word `const`). `Refs KS-1351`.
**Types only. No runtime change** — this declares what the code already writes and already reads.

Decided by Wednesday under the 2026-08-07 autonomy grant (items 3–4), so this is reported as a
decision taken, not a question raised.

## The decision: a Secuura extension, not a widened W3C base

`credentialRepo.revoke()` writes `revoked`, `revokedAt` and `revocationReason` into
`credentialStatus`, and the issuer portal reads `credentialStatus?.revoked` to render a
credential's revoked state (`frontend/issuer/src/components/CredentialCard.tsx:119`,
`CredentialDetailModal.tsx:84`). The three fields were undeclared, so four cells that read them
were `TS2339`.

The ticket framed this as "declare the fields, or stop writing them". **"Stop writing them" was
never really open**: it would break the issuer portal's revoked display and change a served
response — `GET /api/credentials/:id` returns the stored credential as is.

So: declare. But **on a new `SecuuraCredentialStatus extends VCCredentialStatus`**, with
`SecuuraCredential` narrowed to it, rather than widening the base. `VCCredentialStatus` is the
W3C-shaped status object; these three fields are ours. The base stays a faithful W3C shape and
Secuura credentials declare what they actually carry.

**It is a narrowing, not a widening** — every `SecuuraCredentialStatus` is a valid
`VCCredentialStatus`, and all three new fields are optional, so nothing that built a status
object before stops compiling.

## Test evidence

**Touched:** `packages/shared/src/vc/types.ts` (+25/−0) ·
`services/vc-issuer/src/repositories/credentialRepo.ts` (+1/−1, `let` → `const`).

**The measurement this ticket asks for: `TS2339` 4 → 0.**

The package tsconfig excludes the tests, so a bare `tsc -p` cannot see any of this — measured:
**0** copies of `credentialRepo.test.ts` in that program. Through a temp config inside the package
(`exclude` narrowed to `node_modules`/`dist`): census test file **1**, `credentialRepo.ts` **1**,
shared `vc/types` **1**, bogus-name control **0**, 428 files.

| | rc | total errors | TS2339 |
|---|---|---|---|
| base | 2 | 4 | **4** |
| with this change | 0 | 0 | **0** |

The four at base are exactly the sites the ticket names — `credentialRepo.test.ts` 72:63, 142:39,
143:39, 144:39 — and they are the *only* errors in that program. Control: a planted
`const x: number = "not-a-number"` takes the run to 5 errors, so the check can still fail.

⚠ **A trap worth recording, because it made my first run read as "the change does nothing".**
`vc-issuer` resolves `@secuura/shared` to the package's **built `dist/`**, not its source. After
editing `packages/shared/src/vc/types.ts` the count was still 4/4, naming `VCCredentialStatus`.
Measured, not guessed: `dist/vc/types.d.ts` held **0** occurrences of the new interface before
`npm run build -w packages/shared` and **2** after, and only then did `tsc` go to 0. **A types-only
change in `packages/shared/src` is invisible to every consumer until that package is rebuilt.**

**eslint, run by hand** (no LINT leg in the harness) — this is item 2, and it is a measured delta:

| | rc | result |
|---|---|---|
| base | 0 | `✖ 1 problem (0 errors, 1 warning)` — the `prefer-const` at `credentialRepo.ts:95` |
| with this change | 0 | **0 problems, 0 `prefer-const` occurrences** |

**Nothing else moved.** `packages/shared` own `tsc`: rc 0, 0 errors. Issuer frontend `tsc`
(the consumer that reads the field): **rc 0, 0 errors** — the narrowing does not break the portal.
vc-issuer suite: **15 files / 140 tests passed, identical at base and with the change** — which is
the right result for a types-only change. A moved cell count here would have meant I had done
something the ticket did not ask for.

**NOT run:** no live stack. Playwright, k6, Schemathesis and Akto were not run. `check:openapi`
not run and not affected — the spec publishes `credentialStatus` as an open record
(`z.record(z.string(), z.unknown())`), so this declaration narrows no published contract.

**Migrations + config:** none.

## NOT COVERED

* **The ticket's own third bullet is not done here:** whether the package tsconfig should stop
  excluding `src/__tests__`. This class of error stays invisible to the package's own `tsc` until
  it does. Left as the ticket left it — it is a harness decision, not a types one.
* This changes no runtime behaviour, so there is nothing for a live sweep to observe. It is `Refs`
  because the tsconfig question above is still open on the ticket.
* 14 files reference `credentialStatus` (positive control: `SecuuraCredential` returns 16 files;
  negative control: 0). The two that read the revocation fields are the frontend components above,
  and they declare their own local type with `revoked?: boolean`, so they were never broken and are
  not changed.

## Push gate — quoted from THIS push's raw log

Head `3f569dfc701c757253aa71ed8b91b81ce9c84c93`, push rc **0**, `.rc` file **0**.

* `pre_push_hook_base.test.sh` **28 / 0** · fixture guard **6 / 0** · `run_shell_suites.test.sh` **49 / 0**
* shell suites **60 passed, 0 failed, 0 skipped (of 60)** · `^FIXTURE BUILD FAILED` **0**
  · **13 code guards passed** · zero `FAIL` / `not ok` lines
* **`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`** The three skipped are
  the stack-dependent legs; no local stack was up. Nothing failed, but 12/15 is not a pass.
* Orphaned `login_stub` listeners from my worktree: **0**.

## Gate

Author-tested per the 2026-08-25 merge flow. Not merged without a signed GO.

