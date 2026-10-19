VERDICT: NO GO at head dbb00e65dfb04abf6886237a76aaf3b2860ac3cb (tier 1, round 1 of 2; landing tree d56b9b8514d5a34fd5ffc3a8d9d26ed621107e48 on develop 6ec1b7badb9b9fc1cd8d8cfe63b6cd61b8ce7b63; 2 blockers, 9 notes)

# GATE AF1: PR #1620 (KS-1402 invited-stub holder), Opus, tier 1, round 1 of 2

Gated 2026-10-19 08:56Z to 09:08Z. Everything was run in my own clone at
`scratchpad/af1/repo`. I made no writes under `!CODING`, no GitHub or Linear writes, used no Docker and ran no `rm`.
Logs are in `scratchpad/af1/logs/`. Scratch PostgreSQL 15 ran on 127.0.0.1:55411, TCP only.

## Heads (re-read at start, 08:56Z, and again before the verdict, 09:08Z, with `git ls-remote origin`)
- #1620 head `dbb00e65dfb04abf6886237a76aaf3b2860ac3cb`: unchanged both times.
- develop **moved** after the brief was written: `66faac9aebc3` became **`6ec1b7badb9b`** (one commit, KS-1642: a probe on the 409 mapping helpers, 3 files, none of them the PR's). It was unchanged between my two reads.
- `merge-tree --write-tree` on LIVE develop 6ec1b7ba: rc 0, no conflicts, tree **`d56b9b8514d5`**.
- `merge-tree --write-tree` on the author's base 66faac9a: rc 0, tree `30f298e098bd19d7e179f99ead09a3e337a8e65c`. This reproduces the author's prediction exactly, but it is no longer the landing tree.
- Overlap: 12 files landed since merge-base 80868551. They intersect the PR's 6 files in 0. Control: the landed set intersected with itself gives 12.
- Three-dot list: exactly 6 files, the five tests plus `routes/documents.ts`, +706/-36. This matches the brief.

## BLOCKERS

**B1. The race arm handles a failure that auth never produces. The real same-tenant race gives a wrong 404 and a false tenant-breach log.**

Instrument 1, code reading:
- auth `createInvitedStub` (userRepo.ts:753-793) reads the email and then calls `createUser`.
- `createUser` (userRepo.ts ~668-700) inserts with `ON CONFLICT (email_lookup_hash) ... DO UPDATE`.
- No UNIQUE index exists on `email`. Measured on the scratch schema: the only unique indexes on `users` are the pkey, `email_lookup_hash`, and the social ids.

Instrument 2, a SQL emulation on the real migrated schema, run as `secuura_app` (no BYPASSRLS) with the tenant GUC set (log: `logs/race.log`):
- **Same tenant:** the losing INSERT with its own fresh uuid returns `INSERT 0 1`. There is **no error**, one row remains with the winner's id, and the loser's id exists 0 times. Control: the winner's id exists once.
- **Cross tenant:** the loser fails with an RLS USING violation, so auth answers 500, and that case is handled correctly (fallback read, then 502).

What this means at runtime:
- In the same-tenant race, auth answers **201 with a userId that does not exist**.
- originate's re-read then finds 0 rows, so it answers **404 RECIPIENT_NOT_FOUND** and logs `users/stub returned a holder outside this tenant — refusing`. That is a false security alarm.
- The `raced` fallback is never reached in that case.
- The RACE cell's stub (`raceThenFail`: insert the row, then answer 500) models an auth behaviour that the code and the schema do not have, so the cell proves nothing about the real race.
- The outcome fails safe: no custody row is written and none is mis-pointed. But both the PR comment at the fallback ("the loser hits the global `email` UNIQUE constraint, which surfaces here as a non-2xx") and the cell assert the opposite of what auth does.

Round-2 shape (findings only, not a fix):
- When the re-read misses, run the hash-keyed tenant-bound read before answering 404, and log the two causes distinctly.
- Re-model RACE as "201 with a phantom id".

**B2. The tenant re-read on the 200 (`alreadyExisted`) branch is pinned by no cell. My one-branch mutant survives in both modes.**

Instrument: mutant A1 inserts `if (stubRes.status === 200) return holderId;` just before the re-read. tsc rc 0. The new suite stays **12/12 in both MT=false and MT=true**.

Why that branch matters most:
- Every cell that reaches the stub gets a 201. IDEMPOTENT's second call resolves locally and never reaches the stub.
- auth returns an existing user from ANOTHER tenant as 200 exactly when its own compare is skipped: `if (callerTenantId && existing.tenantId && existing.tenantId !== callerTenantId)` (userRepo.ts createInvitedStub). That is a caller credential with no tenant, or a NULL-tenant row, which is the KS-1406 class the PR's own comments name.
- So the branch where the re-read is the only tenant authority is the one branch the TENANT PROOF does not cover.
- The code itself is correct today. The tier-1 condition "tenant boundary proved" is not met.

Round-2 shape: a TENANT PROOF variant whose stub answers 200 `alreadyExisted:true` with a foreign-tenant id. Mutant A1 must kill it.

## NOTES

- **N1. The mint runs before the document-existence check.** Cell C10 pins that order: `mockGetDocument` is never called. So a transfer naming a missing or foreign document, or one that later fails in the transaction (500), still leaves a new auth user row holding PII, then answers 404 NOT_FOUND or 500. This is not an escalation: the same principal can call `/stub` directly with `certifications:write`. It is still a write on a failing request. Consider moving the mint after `getDocument`; that would not change the answer order for unknown emails.
- **N2. Cross-tenant existence is now distinguishable on this route.** An email that is unknown everywhere gives 201 (stub minted). An email that exists in another tenant gives 404. Before this PR both gave 404. This follows from the ruling and from the `/stub` / certifications/issue precedent, and the same oracle already exists there. The author's divergence table states the change for Kintsugi but does not call it a disclosure.
- **N3. The SCOPE ADMISSION and withdrawal CONTROL cells test hard-coded copies.** `S_SCOPES` and `STUB_ADMITS` in the test file are literals, so editing `api-gateway routes/platform.ts` or auth's `hasUsersStubScope` does not red either cell. The real tripwires already exist elsewhere:
  - api-gateway `ks843-erasure-scope-gate.test.ts` "F-2", an exact-equality source read of `S_CONNECTOR_SCOPES` that includes `certifications:write`;
  - auth `ks564-connector-stub-auth.test.ts`.

  Wednesday's condition is met in form. But the documents.ts comment claiming the new cell reds on withdrawal is inaccurate. Confirmed by reading: `S_CONNECTOR_SCOPES` carries `certifications:write` at platform.ts:**591-595** (the brief's :513-523 is stale), and `hasUsersStubScope` is at users.ts:247-258.
- **N4. A reserved wallet email (`*@wallet.local`) not present locally now gives 502 BAD_GATEWAY.** auth's stub schema refuses it with 400, and originate maps any non-ok answer to the fallback and then 502. It was 404 before. A client error is presented as a gateway error.
- **N5. A non-UUID `userId` from upstream gives a 500, not a 502.** It reaches `${holderId}::uuid` in the re-read, throws 22P02, and lands in the outer catch, so it answers 500 INTERNAL_ERROR. It fails closed and writes nothing.
- **N6. The 20 re-pinned unit cells depend on nothing listening at the auth URL.** Their harnesses pass non-`/lookup` URLs to `realFetch`, so the expected 502 relies on ECONNREFUSED at `AUTH_SERVICE_URL` (default localhost:6003). It held here (no listener on 6003, checked with lsof). It is environment-dependent.
- **N7. Landing-tree numbers differ from the claim only because develop moved.**
  - originate unit on landing d56b9b85: **124/124 suites, 1495/1495**, rc 0. That equals live develop 6ec1b7ba (1495/1495, 124 suites).
  - At the PR head alone I reproduced the author's **1481/1481 in 122 suites**. The +14 tests and +2 suites belong to KS-1642.
- **N8. The re-pinned cell count is 20, not the brief's "19 (ks739 x13, ks1402 x5, ks697 x1) + KINTSUGI".** The split is ks739 14 (13 `it.each` rows plus R-KS74), ks1402-resolves 4 (C2, C2b, C5, C10), connector-actor 1 (KINTSUGI) and ks697 1. This is an accounting difference only (see Q3).
- **N9. The disclosed KINTSUGI line is verified as an addition (Wednesday addendum).** `ks1402-transfer-custody-connector-actor.integration.test.ts:320` `expect(r.json?.error?.code).not.toBe('RECIPIENT_NOT_FOUND')` is the only changed non-status line, and it is added. It is redundant with the next line's `toEqual({status:502, code:'BAD_GATEWAY'})`, but it is harmless and authorised.

## Answers by question

**Q1. Tenant boundary.**
- (a) Code reading of `mintInvitedStubHolder` and the handler: the upstream id reaches the handler ONLY after the re-read through `(tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)`, which is the same predicate as the resolution read and the id path. The race branch returns an id from originate's own tenant-bound, hash-keyed read, not the upstream id.
  - Logs: the refusal log carries `tenantId` only.
  - Event, custody row, owner flip and `logger.info`: these use `resolvedHolderId` only after it is confirmed.
  - No path uses the returned id unconfirmed.
- (b) TENANT PROOF passes in both modes. Mutant M1 (re-read replaced by a constant row) kills exactly TENANT PROOF in both modes (11 pass). My one-branch mutant A1 **survives**: see B2.
- (c) auth `/stub` (users.ts:364-433, read only) takes `callerTenantId = req.user?.tenantId` from the verified token. `createInvitedStub` pins the new row's `tenant_id` to it, and `EMAIL_RESERVED_ELSEWHERE` gives 404 `USER_NOT_FOUND`. Caveats: the compare is skipped when the caller tenant or the existing row's tenant is empty (the B2 branch), and `createUser` defaults an empty tenant to `DEFAULT_TENANT_ID`. **I did not build or run auth.** This is code reading only.

**Q2. PII.** I read the stub row through `createInvitedStub` and `createUser`. It holds:
- a new uuid;
- `email`, encrypted with `encryptPiiCol(normEmail,'email',id)`;
- `email_lookup_hash`, an HMAC;
- `role` user, `status` invited, `email_verified` false, `mfa_enabled` false, `verification_level` basic, `auth_method` email;
- `tenant_id` from the caller (or `DEFAULT_TENANT_ID` when empty);
- `metadata` `{}` and timestamps;
- names, password, wallet and org all NULL.

originate sends `normalisedEmail` only in the `/stub` request body. The new logger lines carry `{error message, timedOut}`, `{status}` and `{tenantId}`. The event payload is unchanged (ids only), and every error body is a fixed string. **There is no new email echo.** auth's 201/200 body echoes `email`, and originate discards it, reading only `data.userId`. This is code reading. Like the author, I wrote no column-asserting cell.

**Q3. The re-pinned cells (each file diffed against develop with `git diff -U0` and filtered of `//` comment lines).**
- **Every changed non-comment line is one of three kinds:**
  - an `it(`/`describe(`/`])(` title;
  - a status/code `expect` (`toBe(404)` to `toBe(502)`, `RECIPIENT_NOT_FOUND` to `BAD_GATEWAY`);
  - an `error:{code,message}` literal inside an existing payload `toEqual`.
- The single exception is N9's added line.
- **No `lookupCalls`, `custodyInsertCount`, `custodyInserts`, `ownerFlips`, `anchorCalls`, `custodyRows`, `ownerOf` or `mockGetDocument` line changed.**
- `expect(` counts, develop/branch: ks739 15/15, ks1402-resolves 38/38, ks697 32/32, connector-actor 22/23. These match the author's figures.
- Removed `expect` lines: 13. Added: 14. Each removal has a same-cell replacement.
- `])(`: one line removed and one added (the ks739 `it.each` title). That is the "two" lines, and they are titles.

**Q4. Admission by `certifications:write`.**
- (a) Confirmed at api-gateway platform.ts:591-595 (see N3 for the line drift).
- (b) The SCOPE ADMISSION cell exists and passes in both modes, but against copies (N3). The source-level pins are ks843 F-2 and auth ks564.
- (c) **KS-1653: NOT verified against the PR body.** `gh` has no authenticated session in the Secuura gh-config here, so I did not read the PR body. The only evidence is the author's READY mail ("KS-1653 / KS-1654 / KS-1655 filed").

**Q5. Race and failure arms.**
- Race: B1.
- TIMEOUT: the route's own 5 s `AbortSignal.timeout` fires (the cell took 5011-5017 ms), the answer is 503, and there is no custody row and no owner flip. Mutant M4 (swap 503/502) kills exactly TIMEOUT.
- BAD GATEWAY (upstream 500, no row): 502, nothing written.
- The 502 from an ECONNREFUSED catch is pinned by the re-pinned unit cells, by message.
- Both arms answer before `withTenant`.
- Repeat transfer: IDEMPOTENT passes. There is one stub call and one user row, and the second transfer resolves locally.

**Q6. Red-first, mutants, landing.**
- New suite on landing: **12/12 with MT=true and 12/12 with MT=false**.
- Sibling connector-actor: 6/6 in both modes.
- Red-first: with documents.ts reverted to develop's version on the landing tree, the suite is **9 red / 3 green in both modes**. The green cells are SETUP, the CONTROL cross-tenant 404 and the CONTROL unknown id. documents.ts was restored byte-identically (sha256 `-c` OK after every revert and mutant).
- Mutants, each run in both modes:

| Mutant | tsc | Result |
|---|---|---|
| M1 (delete the re-read) | rc 0 | kills TENANT PROOF only |
| M3' (`raced.length > 0` to `> 1`) | rc 0 | kills RACE only |
| M4 (swap 503/502) | rc 0 | kills TIMEOUT only |
| A1, mine (skip the re-read on 200 only) | rc 0 | **survives** (B2) |
| A2c, mine (drop Authorization forwarding in the `/stub` call) | rc 0 | kills 8 cells: MINT, MINT TENANT, IDEMPOTENT, TENANT PROOF, TIMEOUT, RACE, CONTROL cross-tenant, SCOPE ADMISSION |

  Discarded, not counted: A2 and A2b. The perl substitution hit the first `Authorization: authHeader` (documents.ts:1360, a different route), not the mint call. A2 failed tsc with TS6133, which serves as the prod-config tsc positive control.
- originate unit on landing: 1495/1495 (N7).
- tsc: rc 0 on the originate prod config. With tests included (143 `__tests__` files listed, through a scratch tsconfig that extends originate's and adds jest/node types), also rc 0. Positive control: a planted `const x: number = "..."` in the new test file gave rc 2, then I restored the file.
- Scratch PG: `docker/init/*` run in order, with `00-init-platform-db.sh` emulated as in prior gates, then the project's `run-migrations.sh` (copy with the cwd glob made absolute): **applied=54 failed=0**, including 052.
- **Harness deviations, stated:**
  - Following the sibling suite's documented single-DB layout, I also loaded `init-platform/01-platform-schema.sql` into `secuura` and pointed `TEST_PLATFORM_DATABASE_URL` at `secuura`.
  - I granted `secuura_app` SELECT/INSERT/UPDATE/DELETE on all public tables.
  - The first run, without the tenants table, failed 12/12 and 6/6. That doubles as a positive control that the runner reports reds.

## NOT RUN
- auth service: not built or run. `/stub`, `createInvitedStub` and `createUser` were code-read only, plus the SQL emulation of the INSERT in B1. There was no live concurrent race against a running auth.
- The author's mutant **M2**: not identified (it is not named in the READY mail, and I could not read the PR body), so not run.
- The PR body on GitHub (no authenticated `gh` here). So the KS-1653 check rests on the READY mail only.
- Linear (as the brief instructs).
- eslint: it reported "File ignored because outside of base path" from the scratch path, which is inconclusive. Treat it as not run.
- The 5 pre-existing failing originate integration suites the author names (ks1119, ks695, ks1508, ks1538, ks1557): not run, on develop or on the landing tree.
- The full originate integration suite: not run. Only the new suite and the connector-actor sibling were run, in both modes.
- The api-gateway ks843 F-2 and auth ks564 suites: read, not run.
- Any deployed environment: not touched.

sha256: 180edacbf4289a3f9a1ca9b043f563f220699c12eaad09e3cbe4a2efb25d321a
