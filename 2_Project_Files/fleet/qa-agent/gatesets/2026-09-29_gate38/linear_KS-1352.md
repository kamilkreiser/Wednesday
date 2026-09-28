KS-1352 Security: a revoked credential still verifies as valid by EITHER route — POST /credentials/verify wires no statusListResolver, so checkStatus reports status:true and can never fail
state In Progress

**A credential revoked through EITHER route still verifies as valid, and the verify response affirmatively reports** `checks.status: true`**. Measured at runtime, both arms, on a local stack at develop** `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`**.**

Revocation is currently unenforceable at `POST /api/credentials/verify`. This is not "the credentials route forgets to update the status list" — it is that the verify route wires no `statusListResolver`, so `VerifiableCredentialVerifier.checkStatus()` cannot return anything but valid, whichever route did the revoking.

## What was measured

Local stack from a worktree at `d9ce1403`, services `vc-issuer` + `pgbouncer` + `postgres` + `redis` (all healthy, `migrations` completed). Requests issued from inside the `vc-issuer` container against `http://localhost:4014`. `POST /credentials/verify` is a `publicOps` exemption, so the verify arms carry no bearer.

### ARM 1 — revoke through `POST /api/credentials/:id/revoke`

| step | request | result |
| -- | -- | -- |
| issue | `POST /api/credentials` | `201`, id `https://secuura.io/credentials/2b8015ca-…`, `statusListIndex "4"` |
| baseline verify | `POST /api/credentials/verify` | `200` · `verified: true` · `checks {signature:true,status:true,expiration:true,issuerDID:true,blockchain:true}` |
| revoke | `POST /api/credentials/<urlencoded id>/revoke` `{"reason":"…"}` | `200` `{"success":true,"message":"Credential revoked successfully","revokedAt":"2026-09-28T07:03:11.724Z"}` |
| re-read | `GET /api/credentials/<urlencoded id>` | `200`, `credentialStatus` now carries `"revoked": true, "revokedAt": "…", "revocationReason": "…"` — **the revocation IS persisted** |
| verify as-issued doc | `POST /api/credentials/verify` | `200` · `verified: true` · `errors: []` |
| verify the RE-READ doc | `POST /api/credentials/verify` | `200` · `verified: true` · `checks.status: true` · `errors: []` |

The last row is the sharp one: a document whose own `credentialStatus` reads `"revoked": true` is submitted to verify, and verify answers `verified: true` **with** `checks.status: true` — an affirmative claim that the status was checked and passed.

### ARM 2 — positive control, revoke through the STATUS route

| step | request | result |
| -- | -- | -- |
| issue | `POST /api/credentials` | `201`, id `…/65f34225-…`, `statusListIndex "5"` |
| baseline verify |  | `200` · `verified: true` |
| allocate | `POST /api/status/default/allocate` | `200`, `index: 1` |
| revoke | `POST /api/status/default/revoke` | `200` `{"revoked":true,"revokedAt":"2026-09-28T07:03:11.740Z"}` |
| confirm recorded | `GET /api/status/default/revoked` | `200` `{"revokedIndexes":[0,1],"totalRevoked":2}` — **genuinely recorded in the status list** |
| verify | `POST /api/credentials/verify` | `200` · `verified: true` · `errors: []` |

**The positive control does NOT discriminate — and that is the finding.** The control was built to show that a "correct" revocation reaches verify. It does not. Revocation reaches verify by **neither** route, so the defect is broader than the credentials route: it is the verify route's missing resolver.

## Why, in code (read at `d9ce1403`, all paths under `Blockchain/Dev/`)

* `packages/shared/src/vc/verifier.ts:435` — `checkStatus()` consults revocation **only** inside `if (this.config.statusListResolver) { … }`. It is the only branch that can push an error.
* `packages/shared/src/vc/verifier.ts:449` — with no resolver the method falls through to `return { valid: errors.length === 0, errors }` with `errors` empty, i.e. **valid**.
* `services/vc-issuer/src/routes/credentials.ts:338-342` — `POST /verify` calls `verifyCredential(credential, { checkStatus: true, checkExpiration: true, checkBlockchain: false })`. `checkStatus: true` is passed; **no** `statusListResolver` **is**.
* `git grep statusListResolver` over the whole tree returns **3 hits, all inside** `verifier.ts` **itself** (`:24` the optional declaration, `:435` the guard, `:437` the call). Nothing anywhere supplies one.
* `services/vc-issuer/src/routes/credentials.ts:284-309` — the credentials-route revoke calls only `credentialRepo.revoke(id, reason)`; it never touches the status list. That part of the original read is correct, but it is not what makes verify wrong.
* `services/vc-issuer/src/repositories/credentialRepo.ts:232-265` — `revoke()` writes `revoked` / `revokedAt` / `revocationReason` onto `credentialStatus`. Nothing reads them at verify. (Those three fields are also undeclared on the type — that is KS 1351, a different ticket.)

`checkStatus: true` therefore reads as a request for a check that structurally cannot fail.

## Board search before filing

Literal substring over title + description, `includeArchived: true`, team Secuura-PK: `statusListResolver` **0**, `checkStatus` **0**, `StatusList2021` **0**, `revoked credential still verifies` **0**, `statusListCredential` **1** (KS 1351, the type declaration + prefer-const ticket — it does not mention verify). Positive control `credentialRepo` returned **7** including one archived, so the scan can see; negative control `zzzq-b38-none` returned **0**. `searchIssues` was not used for the verdict: it is fuzzy and returned 20 unrelated rows for an exact worktree name.

## NOT TESTED / NOT DONE

* **No fix built.** Measurement only, per the brief. No PR, no product change.
* The api-gateway verify path (`POST /api/verification/verify`, `/api/v2/…`) was **not** measured — only vc-issuer's own `POST /api/credentials/verify`.
* Whether the demo or any deployed environment supplies a `statusListResolver` by another route was **not** checked; the grep above is over the repo at `d9ce1403` only.
* Presentation verification (`POST /api/presentations/verify`) was not measured, though it is the same `publicOps` class and likely shares the verifier config.
* Issuance required an ephemeral `VC_SIGNING_KEY` (Ed25519 PKCS8 hex) supplied through a local compose override for the measurement; it was never committed and the credential contents are throwaway.
* No assertion is made about what the *right* behaviour is (resolve the status list at verify, read `credentialStatus.revoked` directly, or refuse when `checkStatus: true` and no resolver is configured). That is a design call.

## Definition of done

* A credential revoked through `POST /api/credentials/:id/revoke` verifies as **not** valid, or `POST /api/credentials/verify` refuses to claim `checks.status: true` when it has no way to check status.
* The same holds for a credential revoked through `POST /api/status/:id/revoke`.
* A cell that fails before the fix and passes after, driving the real routes end to end rather than the verifier in isolation.

Found by runtime measurement, not code reading; the code read alone predicted only the ARM 1 half.
