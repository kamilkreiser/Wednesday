# QA gate: Secuura Platform K PR #1511 (KS-880, one home for the security row mappers), head c6567a74

- **Head:** `c6567a74493f268e1ed91b3587421107cf2138c0`, two commits on base: `e043b7fa0` (KS-880) and `c6567a744` (merge develop). `git merge-base --is-ancestor f6f2a539 c6567a74` gives rc 0.
- **Base:** develop `f6f2a539f4a027a0bc60d7bf4b839a352f2b7032` (V's #1506 squash).
- **Real tip:** `git ls-remote origin refs/heads/develop` returned **`f6f2a539…`** at 01:44:08 AEDT and again at 01:55:53 AEDT. Develop has not moved. `refs/pull/1511/head` is `c6567a74…`, the head named above.
- **Merged tree:** merging the real tip into the head gave "Already up to date." (rc 0). The merged tree `879867e674b4` is the head tree `879867e674b4`. So every head run below is also a merged-tip run. There were no conflicts.
- **Bundle:** sha256/16 is `3bb2cf616c844d2b`, which matches the builder. `git bundle verify` rc 0, requiring `f6f2a539`. Its `HEAD` is `c6567a74…`, which matches.
- **Diff stat, f6f2a539..c6567a74:** 4 files, **+246/-155**, all under `services/security`: `converters.ts`, `index.ts`, `__tests__/ks880-one-mapper-home.test.ts` (new) and `__tests__/row-converters.test.ts`. No non-security file is touched.
- **How I got the tree:**
  - I cloned with `--no-hardlinks` from my own earlier scratch clone into `scratchpad/g1511/repo`.
  - I fetched develop (read-only, using the project's deploy-key `sshCommand` as an env var) and the bundle into that scratch clone. I made worktrees `head`, `base` and `merged`.
  - Nothing was written under `!CODING`. I ran no fetch, checkout or worktree inside it. The builder's `tools/mutants880.py` was **copied out** (sha256/16 `a703d93985992b9a`) and retargeted to my worktree.
  - **node_modules is symlinked** from the project install (root, `services/security`, `auth`, `api-gateway`, `packages/shared`, `services/shared`). The `@secuura/*` links are recreated relative, so they point into my tree. I built `packages/shared` with `tsc` in both head and base (rc 0).
- **Database:** none. The security suite needs no Postgres. No real database, Kintsugi, demo or box was touched.
- **Gate:** independent Opus, Tier OPUS (API-key row mappers are a security surface), 2026-10-13.

## VERDICT: NO GO

**The production claim holds. All five mappers are behaviour-identical, base index.ts against head. A 112-row differential gives 0 differences and byte-identical output, from the TS source and from the compiled `dist/` the container runs. The four re-exports are `===` under vitest, tsx and tsc CommonJS.**
**But the PR turns the `packages/shared` suite red: 948/949, against 949/949 on base. It moved the KS-33 comment containing the word `svc_api_keys` into `converters.ts`, which also reads `is_active`, and that trips the KS-764 revoke-call-site guard. The fix is a one-line change, which the builder chooses: allowlist the file with a reason, or reword the comment. Then re-gate.**

## By my runs

Raw output is in `scratchpad/g1511/out/`.

### 1. Suites

- **services/security, full suite, head (== merged):**
  - **29 files / 311 tests, 0 failed, rc 0.** This holds on five sequential repeats (`rep_head_1..5`).
  - Base f6f2a539 gives **28 / 292**, rc 0, on five repeats. The builder's "base 28/291" predates #1508's pin cell, which is consistent with his "310 → 311". The delta is +19 tests, all from the two KS-880 files.
- **The first head run** showed `1 failed | 310 passed`. To check whether that was the PR, I ran three head and three base suites concurrently. **All six** failed the same cell: `ks578-ks643-revoke-authorization > REFUSES a tenant-scoped ORG_ADMIN revoking another tenant's key`, with `Test timed out in 5000ms` (7.8–9.0 s). That failure is base too, so it is a **pre-existing load flake, not this PR**. Run alone, that file gives 11/11.
- **The two touched test files on head:** **33 cells, 33 passed.** The builder says 30. `grep -c "it("` gives 20 + 10 = 30 declarations; an `it.each` over the four SAME_FUNCTION names expands them to 33 runtime cells.
- **Red first:** I put head's two test files against the unmodified base source.
  - Result: **10 red / 23 green**. The builder said 8 / 22.
  - The extra two red cells are `row-converters.test.ts:201` ("green before and after the move") and the tenantId default-tenant cell. Note N2.
  - Base was restored with `git checkout`, and `git status` is clean.
- **KS-869 test** (`ks869-connector-id-persisted`, which reads `index.ts` for the `INSERT INTO svc_api_keys`): **8/8 green** on head. The two WRITE-half cells pass, because the INSERT did not move.
- **packages/shared, full suite:**
  - **Base: 49 files / 949 passed, rc 0.**
  - **Head: 1 failed | 948 passed, rc 1.** The failure is `ks764-key-revoke-call-site-guard > no file mentions svc_api_keys + is_active except the call sites and a NAMED allowlist`. The received list adds **`services/security/src/converters.ts`** (Major M1).
- **api-gateway tests that name the security service** (ks1090, ks1230, notifications): 3 files / 33 passed.

### 2. Static guards

- **tsc:**
  - `tsc -p tsconfig.json` in services/security gives rc 0 (emit) and rc 0 (`--noEmit`), on head and on base.
  - The two test files under strict `tsc --noEmit` give rc 0. They are not covered by any ratchet. The planted type-error control gives rc 2 (TS2322).
- **eslint** on the four files: rc 0, empty output. **Control:** a copy of converters.ts in the same directory, plus `debugger;`, gives rc 1 (`no-debugger`).
- **`npm run check:test-types`:** rc 0.
  - auth: examined 144 files (93 tests), 42 errors, 42 in the baseline, 0 new, 0 stale.
  - api-gateway: examined 149 files (114 tests), 35 errors, 35 in the baseline, 0 new, 0 stale.
  - security is **not under the ratchet**: `check.cjs services/security` gives rc 2, "no tsconfig.test.json".
- **`npm run check:openapi`:** rc 0, "413 example blocks … OK".

### 3. Mutants

**29 mutants, each applied alone, each with the full security suite and also my differential harness. Both files were restored byte-identical by sha256 every time** (`restored=True` × 29). The sha256/16 before and after were the same: converters `aae746bdcaa5ffa3`, index `60e68e91c5f0600c`. `git status` was clean.

| Mutant | Suite | My harness vs base |
|---|---|---|
| **Builder's 19, all run** | | |
| K1 apiKey drops tenantId | RED 7 | 40 diffs |
| K2 apiKey drops connectorId | RED 3 | 40 |
| K3 apiKey loses default-tenant fallback | RED 2 | 5 |
| K4 organizationId not null for an absent column | RED 1 | 2 |
| K5 scopes unparsed | RED 5 | 38 |
| K6 audit loses fallback | RED 2 | 4 |
| K7 audit ignores the decryptor | RED 1 | 1 |
| K8 audit uses the wrong audit id | RED 1 | 1 |
| K9 event drops resolvedBy | RED 1 | 15 |
| K10 event details unparsed | RED 1 | 14 |
| K11 converters gains a value import | RED 1 | same (structural) |
| K12 parseJson throws | RED 1 | 3 |
| I1 a copy of rowToApiKey that agrees | RED 2 | same (identity cell kills it) |
| I2 identity decryptor | RED 3 | 8 |
| I3 null decryptor | RED 2 | 4 |
| I4 leftover column read | RED 1 | same |
| I5 re-declared interface | RED 1 | same |
| I6 re-export dropped | RED 6 | 40 |
| I7 stale event copy | RED 1 | same |
| **The gate's own 10** | | |
| G1 isActive defaults TRUE when the column is absent | **SURVIVED** (311/311) | 2 diffs |
| G2 tenantId fallback reads organization_id | RED 7 | 39 |
| G3 parseJsonArray keeps the raw string on a parse error | RED 1 | 2 |
| G4 audit wrapper binds tenant_id as AAD, not the row id | RED 2 | 1 |
| G5 audit wrapper hard-codes the test's id `audit_880` | RED 1 (the different-id cell) | 1 |
| G6 the parseJson re-export replaced by an exact copy | RED 2 (identity) | same |
| G7 connectorId `??` → `\|\|` | **SURVIVED** | 1 |
| G8 organizationId `??` → `\|\|` | **SURVIVED** | 2 |
| G9 a failed decrypt answers null, not `{}` | RED 1 | 19 |
| G10 isActive `=== true` (string `'t'` no longer active) | **SURVIVED** | 3 |

- The builder's 19 reproduce his table: 19/19 killed.
- 4 of my 10 survive the suite. Every survivor is caught by the differential harness (Minor m1).

### 4. Identity and the audit wrapper

- **vitest:** the four IDENTITY cells are green on head and red on base (red-first above).
- **tsc CommonJS** (the project's own tsconfig: module commonjs, ES2022; the Dockerfile runs `npm run build` = `tsc`, then `node dist/index.js`):
  - `dist/index.js:40-43` compiles each re-export to `Object.defineProperty(exports, "<name>", { enumerable: true, get: … converters_1.<name> })`.
  - Loading `dist/index.js` with `SECURITY_DISABLE_BOOT=1`: `parseJson`, `parseJsonArray`, `rowToSecurityEvent` and `rowToApiKey` each give `index===converters: true`, as a getter. `rowToAuditLog` gives `false`, as a value, which is by design.
  - Base gives `false` for all five, as values (the positive control).
- **tsx** (the `dev` script): the same four are `true` and `rowToAuditLog` is `false`.
- **The wrapper:**
  - `index.rowToAuditLog.length` is 1 (`converters.rowToAuditLog.length` is 2).
  - `index.rowToAuditLog(row, () => ({injected:true}))` returns `details {"p":1}`. The extra argument is ignored, so an outside caller cannot swap the decryptor through the export.
  - But see Note N1: **mutating the converters CommonJS export object** does reach it.
- **Keyring is not loaded by converters:** I loaded `dist/converters.js` alone with `PII_ENCRYPTION_KEY` unset.
  - `require.cache` then holds only `["tools/cjs.cjs","dist/converters.js"]`.
  - `grep -c 'require(' dist/converters.js` is **0**. The control, `dist/index.js`, has 19.
  - `rowToApiKey({}).tenantId` gives the default tenant.
  - So there is no circular import and no import-side effect is possible from converters.

## Equivalence table

The harness (`tools/gate1511-diff.test.ts`) feeds hand-made rows to each mapper exported from `../index`. The rows cover:

- **Key mapper:** nulls, absent columns and `{}`; `''` and `0`; scopes as a JSON string, an array, `[]`, `'[]'`, null, absent, `'[broken'`, `'{"a":1}'`, `'"str"'`, an object, `''` and a number; `is_active` as `'t'`, `'f'`, 1, 0, false, null and absent.
- **Timestamps:** Date versus string, invalid strings and absent values.
- **Event mapper:** details as `'[bad'`, an object, null, `''`, `'[1,2]'` and `'null'`.
- **Audit mapper:**
  - details as **real v1 ciphertext bound to its own id**, the same ciphertext under a different id, ciphertext bound to another id, `'v1:garbage:zz'`, `'v9:aaaa'`, plaintext JSON, an object, `'[bad'`, `''` and `42`;
  - tenant_id as null, `''` or absent;
  - id null with ciphertext.
- **parseJson / parseJsonArray:** 17 raw values each.

The serialisation is tagged. It distinguishes undefined from absent, records Date values, NaN, **key order**, reference identity (`sameRef`) and throws.

| Mapper | Rows | base index.ts vs head (TS source) | base dist vs head dist (compiled) | Control: base index vs base DEAD converters |
|---|---|---|---|---|
| rowToApiKey | 40 | **0 diffs** | **0** | **40 diffs** (no tenantId, no connectorId, organizationId undefined) |
| rowToSecurityEvent | 15 | **0** | **0** | 0 (the dead copy agreed) |
| rowToAuditLog | 23 | **0** | **0** | 23 (called with no decryptor: throws) |
| parseJson | 17 | **0** | **0** | 0 |
| parseJsonArray | 17 | **0** | **0** | 0 |

- **Whole-file results:**
  - `cmp diff_base.json diff_head.json` is BYTE-IDENTICAL (sha256/16 `dd64b678581d2dd4` for both).
  - `cmp dist_base.json dist_head.json` is BYTE-IDENTICAL.
  - The compiled output equals the source output.
  - The `dist/` file lists are identical (10 `.js`).
- **The harness's audit cells are live:** row 2 decrypts to `{"secret":"s1","n":2}`, and the same ciphertext on `aud_X` gives `{}`.
- **Throws:** 0 rows throw on base for any mapper. A failed decrypt returns the same shape (`details: {}`), and `decryptDetails` (unchanged in index.ts, outside the diff hunks) does the logging, exactly as before.
- **Comment-stripped source:** I also compared the bodies, base index.ts against head converters.ts. All five are IDENTICAL. **Control:** base index.ts against base converters.ts gives rowToApiKey DIFF and the other four identical.
- **Callers.** `git grep` at c6567a74 for `rowToApiKey|rowToAuditLog|rowToSecurityEvent|parseJsonArray|parseJson\b` across `Blockchain/` finds:
  - **Production:** only `services/security/src/index.ts`.
    - `:341` is `dbGetApiKey`, the revoke path: `lookupKeyForRevoke(id)` → `rowToApiKey(row)` → `decideKeyRevoke`.
    - `:379` is loadFromDb audit logs, `:386` events, `:392` keys.
    - `:1287` and `:1310` are the validate path.
  - In `dist/index.js` these are `(0, converters_1.rowToApiKey)(…)` at lines 314, 344, 349, 1175 and 1199, and the audit wrapper at 321.
  - **Tests:** ks869, ks880 and row-converters, plus 16 files importing `../index` (the control count).
  - The other matches are unrelated `parseJsonb` helpers in prism and kyc, and a SQL comment in migration 018.
- **Importers of `converters`:**
  - **At base:** exactly one, `__tests__/row-converters.test.ts:13`. The dead copy had **no production importer**.
  - **At head:** `index.ts:50` and the two test files. The only other `from '../converters'` in the repo is prism's own module (the positive control that the pattern matches).
  - Outside services/security, nothing imports the security service. The only hit is a comment in `packages/shared/src/index.ts:223`.
- **So nothing relied on the dead copy's missing tenantId/connectorId.** Every production api-key lookup already went through the live index.ts copy, which already returned both fields. **No authorisation input changes** (`decideKeyRevoke` and `decideTenantAccess` see the same object, field-for-field and in the same key order).

## Findings

### Major

**M1. The PR turns the packages/shared suite red (KS-764 drift guard).**
- **Where:**
  - The trigger is `services/security/src/converters.ts:55`: `// KS-33: organization_id is now NULL-able in svc_api_keys. …`. That comment moved from index.ts into a file that also reads `r.is_active` (`:164`).
  - The guard is `packages/shared/src/__tests__/ks764-key-revoke-call-site-guard.test.ts:388`. Its allowlist is `NON_REVOKE_MENTIONS` at `:178`.
- **The guard's own output:** "expected [ …(5) ] to deeply equal [ …(4) ]". The diff adds `"services/security/src/converters.ts"`.
- **Shared suite:** base 949/949 rc 0, head 948/949 rc 1. Reproduced three times, and the check is deterministic (a text scan).
- **Cause proven by a single edit:** I rewrote only that comment's `svc_api_keys` to "the keys table" (0 occurrences left), and the guard went to **15/15**. Then I restored converters.ts to sha256/16 `aae746bdcaa5ffa3`, the same as before.
- **Why the builder missed it:** his evidence lists the security suite, tsc, eslint and check:test-types. The `packages/shared` suite is not among them.
- **Decision for the builder, per the guard's message:** converters.ts does not revoke. Adding it to `NON_REVOKE_MENTIONS` with a reason ("row mapper: reads is_active, writes nothing") is the honest fix. Rewording the comment would also pass, but it hides a real mention from the sweep.

### Minor

**m1. Four equivalence-boundary mutants survive the whole suite.**
- All four are caught by my differential harness, so the head is proven equivalent by my runs. They are listed because the suite would not catch a future drift:
  - **G1:** `is_active` absent gives `isActive: true`.
  - **G10:** `is_active === true`, so a `'t'` string is no longer active.
  - **G7:** connectorId `''` stays `''` versus becoming undefined.
  - **G8:** organizationId `''` stays `''` versus becoming null.
- **Where:** `converters.ts:164`, `:170` and `:152`.
- G1 is the security-relevant one: a mapper that defaults a key to active passes 311/311.
- These gaps predate the PR (the same cells were unpinned at base). They are not a reason to hold this PR beyond M1, but they belong in a follow-up ticket, ideally a cell for `isActive` on an absent or NULL column.

### Note

**N1. The CommonJS live binding is a new patch point.**
- index.ts now calls the mappers through `converters_1.<name>` (`dist/index.js:314,321,344,349,1175,1199`).
- I ran `require('dist/converters.js').rowToAuditLog = () => ({hijacked:true})`. After that, `index.rowToAuditLog(row)` returns the hijacked object. Base gave `false`, because the copies were module-local.
- This needs in-process code execution, which could already patch `@secuura/shared`. So it is not an attack surface. It does mean that a `vi.spyOn(converters, …)` in a test now affects index.ts too.

**N2. Red-first count and labels differ from the PR's.**
- I measured **10 red / 23 green of 33 runtime cells**. The builder says 8 / 22 of 30.
- `row-converters.test.ts:201` is labelled "(green before and after the move …)", but it is **RED on base**, because that file imports the dead converters copy, which returns `undefined` for an absent `organization_id`. The label is true of the old index.ts copy, not of the module the cell exercises.
- The tenantId default-tenant cell is also red on base, and the builder did not count it.
- These are documentation inaccuracies only.

**N3. Pre-existing load flake, not this PR.**
- `ks578-ks643-revoke-authorization.test.ts`, the cell "REFUSES a tenant-scoped ORG_ADMIN revoking another tenant's key", times out at 5 s under parallel load. It did so in 6/6 concurrent runs (3 head, 3 base).
- Its first cell pays the cold `import('../index')` inside the test timeout.

**N4. Pre-existing quirks, kept identical by the PR.**
- `parseJsonArray('{"a":1}')` returns an object, not an array.
- `parseJson('null')` returns `null`.
- Neither is in scope.

**N5. security is not under the test-types ratchet** (no `tsconfig.test.json`), and its tsconfig excludes `__tests__`. I typechecked the two touched test files directly: strict rc 0, with a planted-error control giving rc 2.

## Not measured

- The 16-leg preflight hook. I did not run it; the builder cites his own run.
- The four platform suites and the other 26 services' full suites. I ran only the 3 api-gateway files that name security, and the full `packages/shared` suite.
- A Docker image build and a container boot. I built `dist/` with the project tsconfig and loaded it with node, which is unmeasured inside the alpine image.
- A live or deployed security service, and any real database. `loadFromDb`, validate and revoke were exercised through their mapper functions only, not against Postgres.
- vitest identity under coverage instrumentation (`test:coverage`).
