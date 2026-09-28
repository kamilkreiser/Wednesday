#1330 KS-1352: a revoked credential fails verify, by either revoke route
head 699acfb804729f80da8aa4f4034f3cd58d99f40e

## BLUF
`POST /api/credentials/verify` wired **no resolver of any kind**, so `checkStatus()` could reach
neither revocation authority: it returned `{ valid: errors.length === 0 }` over an empty error list
— VALID — and **nothing anywhere read `credentialStatus.revoked`**. A credential revoked through
**either** route answered `verified: true`, `checks.status: true`, `status: 'active'`.

Both authorities are now consulted, each **keyed by credential id**. `POST /api/presentations/verify`
had the same defect (it called the same shared verifier with **no config at all**) and is fixed by the
same wiring. Kam ruled option **a** on this ticket: "Fix verify properly: a revoked credential fails".

**Not deployed anywhere.** Base `develop` `0d156d12cc0f`.

## What changed
- **`packages/shared/src/vc/verifier.ts`** — two new `VCVerifierConfig` fields,
  `storedRecordResolver` and `statusListRevocationResolver`, both keyed by **credential id**;
  `checkStatus()` gains one arm per authority; and the `if (!credential.credentialStatus) return
  { valid: true, errors: [] }` early return no longer **discards** those arms — it now returns
  `errors.length === 0`.
- **`verify()`** runs the status check when either resolver is wired, even if the **submitted**
  document carries no `credentialStatus`. The caller supplies that document, so treating its absence
  as "nothing to check" would let a revoked credential verify **by omission**.
- **`services/vc-issuer/src/services/revocationResolvers.ts`** (new) — builds the resolver pair in
  one place, because **two** routes had the defect.
- **`services/vc-issuer/src/routes/status.ts`** — exports `statusListRevocation(credentialId)`, the
  narrowest accessor over the module-local `statusListManagers`: no manager escapes, no mutation.
- **`credentials.ts`** and **`presentations.ts`** — wire it. On presentations only the revocation
  resolvers are added; the verifier's other defaults are untouched.

### Why credential id, not `statusListIndex`
The issue route allocates `credentialStatus.statusListIndex` from its **own module counter**
(`credentials.ts:118`), a different sequence from the status manager's `allocateIndex()`. An index
from one is not a valid key into the other, so resolving revocation by index can test an unrelated
bit. `StatusListManager` already exposes `isRevoked(credentialId)` and `getEntry(credentialId)`, and
`getEntry` is what distinguishes "not in this list" from "in this list, not revoked".

### The two arms are separate config fields on purpose
The rule is an **OR of two conditions**, so each disjunct must be independently removable — which is
what lets one tamper arm target one disjunct. See the arms table.

## An id with NO stored record still verifies — deliberately
The stored-record arm **abstains** when the repository has no record. That is the boundary of the
ruling on this ticket, which is about **revoked** credentials, not unknown ones. Failing closed was
measured and rejected: `credentialRepo.loadFromDb()` returns silently when the database is
unavailable (`credentialRepo.ts:212`) and the memory store then starts empty, so a fail-closed rule
would refuse **every** credential on a process with no database. Cell **C2** pins the abstention, so
it cannot be changed by accident. The policy question is filed as **KS 1368** (Backlog).

## Test Evidence

**Touched:** `packages/shared/src/vc/verifier.ts` · `services/vc-issuer/src/routes/{credentials,presentations,status}.ts` ·
`services/vc-issuer/src/services/revocationResolvers.ts` (new) ·
`services/vc-issuer/src/__tests__/ks1352-revoked-credential-fails-verify.test.ts` (new) · `BACKLOG.md`

**RAN — red first, then green, on this worktree at base `0d156d12`:**
| run | result |
|---|---|
| vc-issuer **baseline** (my file excluded) | **15 files / 140 tests, 0 failed** |
| new cells at the **UNTOUCHED tip** | **3 failed / 3 passed (6)** — R1, R2, R3 red **by `AssertionError`**; F0, C1, C2 green |
| new cells **after the fix** | **6 passed (6)** |
| vc-issuer **full, after** | **16 files / 146 tests, 0 failed** (+1 file / +6 tests = exactly my cells) |
| `packages/shared` full, after | **48 files / 945 tests, 1 failed** — see the pre-existing red below |
| `tsc` packages/shared | rc 0, **0 errors** |
| `tsc` vc-issuer (build program) | rc 0, **0 errors** |
| `tsc` vc-issuer **including `src/__tests__`** (temp config inside the package, `exclude: []`) | rc 0, **0 errors**, and a `--listFilesOnly` census proves my cell (1) and resolver (1) are in that program, bogus-name control 0 |
| `eslint src` vc-issuer — **run by hand** (the harness has no LINT leg) | rc 0, **0 problems**; a planted `no-control-regex` **error** in my own new file gives rc 1, restored by sha256, clean re-run rc 0 |
| `eslint src` packages/shared — **run by hand** | rc 1, **exactly 1 error**: the known pre-existing `no-control-regex` at `src/middleware/index.ts:539`; 35 warnings; **0 errors in any file I touched** |

The red is **by assertion**, not by error: received `{verified: true, statusCheck: true, docStatus:
'active', saysRevoked: false}` against expected `{false, false, 'revoked', true}`. 0 unhandled.

**⚠ My first red run was INVALID and is reported rather than buried.** All five cells failed 503
`VC_SIGNING_KEY environment variable is required` inside my `issue()` helper — **including both
controls**, which is the tell that a run measured the harness, not the product. Fixed with a
per-run Ed25519 PKCS8 key in `beforeAll`, plus cell **F0**, which asserts issuance works and the
proof is `Ed25519Signature2020`, so a future fixture break can never again read as a product red.

### Tamper arms — one per disjunct. Predictions were the brief's; these are measurements.
Each anchor asserted to occur **exactly once**, each tamper proven non-inert by byte comparison,
each restored with sha256 proved equal, and the untampered run proved all-green first.

| arm | tamper | predicted | **measured** |
|---|---|---|---|
| a | stored-record arm never reports revoked | R1, R2 red | **passed=4 failed=2 — RED R1, R2; green F0, R3, C1, C2** |
| b | status-list arm never reports revoked | R3 red | **passed=5 failed=1 — RED R3; green F0, R1, R2, C1, C2** |
| c | both arms removed | R1–R3 red | **passed=3 failed=3 — RED R1, R2, R3; green F0, C1, C2** |

Each arm reds **exactly** the cells its disjunct carries, and **no arm reds a control**. After all
three, restored: 6 passed, sha256 equal to pristine.

**NOT RUN:**
- **No live stack, no Postgres.** `credentialRepo` used its in-memory fallback throughout, so the
  **DB** revoke path (`credentialRepo.ts:249-262`) is not exercised against a real database, and
  neither is the swallowed-DB-write path. **§5f live sweep owed.**
- The four platform suites (Schemathesis · Akto · Playwright · Performance/k6) — **not run**.
- **`check:openapi` not run**, and I am not claiming what the spec says about the verify response.
  This change alters a **response body's truth**, not its shape: `verified`, `checks.status` and
  `credential.status` are already declared fields and no field is added or removed.
- Whether any **other open PR** touches these files — not measured.
- **`/api/verification/*`** (proxied to `originate`) and **`/api/batch/verify`** (the gateway's own):
  both are document-hash verification and **whether either consults credential revocation is
  unread**. Named as a follow-up, deliberately not changed here.

**Migrations + config:** **none.** No migration, no env var, no config default. `packages/shared` is
consumed as its **built `dist/`**, so `npm run build -w packages/shared` is required after this
change — measured: `storedRecordResolver` appears **0** times in `dist/vc/verifier.d.ts` before the
build and **1** after.

**⚠ PREFLIGHT INCOMPLETE — see the ratio in the push gate section below.** Stated as a ratio, not
implied away.

## A RED on `develop` that is NOT from this change
`packages/shared` is **1 failed / 945** at base. The failing cell is KS 764's revoke call-site guard,
and **PR #1327** broke it: the guard's regex for `services/security/src/index.ts` is
`/isActive\s*=\s*false;[\s\S]{0,80}dbSaveApiKey\(/` and the nearest pair is now **1445 characters**
apart, reaching a function *declaration* rather than a call. Bisected: matches at `63db8a383`, does
**not** match at `ea816de19f86` (#1327) or `0d156d12c`.

**Proven independent of this work, twice:** identical `1 failed | 944 passed (945)` with and without
my new resolver file, and identical again with **every file I touched reverted** to its pristine
`0d156d12` content — restore verified 6/6 by sha256, and the pristine/patched `dist` counts went
0 → 1 either way, so the rebuild swap was real in both directions. Filed in `BACKLOG.md`; not fixed
here, because the fix is a decision about #1327's revoke shape.

Refs KS-1352

