KS-1351 vc-issuer: VCCredentialStatus declares no revocation fields, so four credentialRepo cells are TS2339 — plus the prefer-const left by KS-1121's deletion
state In Progress

**One test pass's residue from #1313 (KS-1121), both measured there and neither fixed in it.**

**Searched the board first, literally, over all 1340 Secuura-PK issues including archived** (`searchIssues` is fuzzy, so this was a literal substring match over every page): `VCCredentialStatus` — **0 open hits**; `prefer-const` — **0 hits**; `credentialRepo` — 6 hits, none about either item (KS-1295 store fallback, KS-1281 table permissions, KS-1204 allowedDocumentTypes, KS-1121 itself, KS-1116 ownership, KS-149 archived tooling); `vc-issuer/src/repositories` — 2 hits (KS-1281, KS-1121). Positive control: `credentialRepo` returned 6, so the scan can see.

## Item 1 — `VCCredentialStatus` has no `revoked` / `revocationReason` / `revokedAt`, and four cells read them

`packages/shared/src/vc/types.ts` declares `VCCredentialStatus` as `id`, `type`, `statusPurpose?`, `statusListIndex?`, `statusListCredential?`. Nothing else. But `services/vc-issuer/src/__tests__/credentialRepo.test.ts` reads `credentialStatus?.revoked`, `?.revocationReason` and `?.revokedAt`, and `tsc --noEmit` over a program that includes the test files reports **TS2339 at four sites** after #1313 (three before it):

```
src/__tests__/credentialRepo.test.ts(72,63):  error TS2339: Property 'revoked' does not exist on type 'VCCredentialStatus'.
src/__tests__/credentialRepo.test.ts(142,39): error TS2339: Property 'revoked' does not exist on type 'VCCredentialStatus'.
src/__tests__/credentialRepo.test.ts(143,39): error TS2339: Property 'revocationReason' does not exist on type 'VCCredentialStatus'.
src/__tests__/credentialRepo.test.ts(144,39): error TS2339: Property 'revokedAt' does not exist on type 'VCCredentialStatus'.
```

Three of the four pre-date #1313 (they sit at 118-120 at its base and shift to 142-144); the fourth, at `72:63`, is added by its new revoke cell. **The runtime path sets these fields** — `revoke()` writes them — so either the type is missing three fields it should declare, or the repository is writing fields the contract does not have. That is the decision this ticket asks for; it is not obviously a one-line type edit.

**Observation, not a conclusion:** line 32 of the same file writes `revoked: false` INSIDE a `credentialStatus` object literal at every tree and does **not** error, so the gap is reachable on a read and not on that construction. Worth one minute from whoever picks this up; it may say something about how the fixture is typed.

Note the package tsconfig excludes `src/__tests__`, so the package's own `tsc` never sees any of this. It is only visible through a program built with `exclude: []`.

## Item 2 — the same pass's cleanup: a `prefer-const` warning created by the ruled deletion

`services/vc-issuer/src/repositories/credentialRepo.ts:95:11` — `warning  'result' is never reassigned. Use 'const' instead  prefer-const`.

Before #1313, `let result` was assigned twice: the exact lookup, then the `LIKE '%id%'` fallback. The owner's 2026-09-16 ruling deletes the fallback, so `result` is now assigned once. `npm run lint` in vc-issuer: **0 problems at #1313's base, 1 warning at its head**; rc 0 either way, because it is a warning.

## Why this is one ticket and not two

Both are residue of the same test pass (#1313) in the same package, and both are cleanup rather than behaviour. Split them if whoever picks it up finds the type question is a shared-package decision — it may be.

## Definition of done

* `VCCredentialStatus` and the repository agree about the revocation fields, decided rather than patched, and the four TS2339 sites go to zero over an `exclude: []` program.
* `credentialRepo.ts:95` is `const`, and vc-issuer lint is back to 0 problems.
* A note on whether the package tsconfig should stop excluding `src/__tests__` — this class is invisible until it does not.

Refs KS-1121
