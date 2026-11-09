PR 2128: GO WITH NOTES

# Gate 290, tier 1 (Opus), round 2 of 2: PR 2128 (KS-1208 only), Seat G 31st

| PR | head | verdict |
|---|---|---|
| 2128 | c7e84537d2aeb6b1c11aeaebdff203a7aa6ff181 | GO WITH NOTES |

**Read first: one question is unanswered.** I could not read Linear (the KS-619 attachment and state) or the live PR title and body. Both need a credential: the Linear key is in the project's real .env, and gh uses the project's gh config. The commission forbids me to open either. So I answered that part from the seat's own evidence only, and I mark it NOT TESTED. Another seat with read access has to close it.

**CAP.** No finding is NO GO-class. Nothing is held back as residue.

## BLUF
- The split is clean. Between round 1 and the head, the only code change in auth.ts is the removal of `if (!decoded.tenantId && !isPlatformRole(decoded.role)) return 'tenantId';`. Every other changed line is a comment.
- auth.test.ts is byte-identical to develop's.
- Net change against develop: 4 files, +311/-0.
- The KS-1208 guard is unchanged.
- I reproduced all of the seat's figures:
  - 8 of 19 red on develop, 3 red (T1-T3) against round 1's code, 19 of 19 at the head.
  - M1, M2 and MT each red on exactly the cells the seat declared.
  - Whole suite 1,899 of 1,899. tsc and eslint identical to develop.
- My own login-shaped cells agree with T1-T3.
- One new Low: the test file does not pin 3 of the 7 header claims (G290-1).

## Pins
- Start, 07:55:20Z: develop f98afb113c2d, PR head c7e84537d2ae (refs/pull and the branch agree). Both match the commission.
- End, 08:06:28Z: develop f98afb113c2d, PR head c7e84537d2ae. **Neither moved.**
- READY read: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatG-31st/mail/out_08_ready_2128_r2.txt`. It is the newest READY in that folder; out_09 is a wrap.

## Findings

**G290-1 (LOW). The new test file does not pin the guard on organizationId, tenantId or tenantSlug.**
- FOUND: the file covers userId and role (C1-C3, C6), email (C4) and verificationLevel (C5). No cell sends an illegal organizationId, tenantId or tenantSlug.
- TESTED: three survivor mutants, each taking one claim out of `OPTIONAL_HEADER_CLAIMS` (head auth.ts:362). Each stayed 19 of 19 green on the seat's file.
- My own cells kill all three on the same harness:
  - X6, a CR-LF tenantSlug: red only under S_tenantSlug.
  - X7, U+0142 in organizationId: red only under S_organizationId.
  - X8, a CR-LF tenantId: red only under S_tenantId.
  - On develop, X6-X8 answer **500**. At the head they answer 401 with 0 upstream hits.
- So the code is right, but three of the seven claims the PR body says are guarded are unpinned. It was the same in round 1, where only my gate cell X8 covered tenantSlug.

**G290-2 (INFO). T1-T3 are close to the real login token, not exact copies of it.**
- At develop, the platform-admin login (services/auth/src/routes/auth.ts:394-409 and :470-473) mints `{ ...syntheticUser, role: platformAdmin.role }`. syntheticUser carries `tenantId: undefined`, `tenantSlug: undefined` and `verificationLevel: 'ENHANCED'`, and has no organizationId.
- generateAccessToken (services/auth/src/services/jwt.ts:187-210) then adds `sessionId` and `type: 'access'`. Its scopes come out empty, because getDefaultScopesForRole returns [] except for OWNER (packages/shared/src/security/scopes.ts:287-294).
- T1-T3 leave out sessionId and type. The guard reads neither, so this is immaterial.
- My X1-X4 tokens carry sessionId and `type: 'access'` and use a uuid userId:
  - X1: platform_admin, required mount.
  - X2: platform_viewer, optional mount.
  - X3: admin, optional mount.
  - X4: platform_admin with x-tenant-override.
- Result: [200, 1, default tenant] at the head and on develop, and [401, 0] against round 1's code. Same as T1-T3.
- X4 also shows that a platform_admin's x-tenant-override is ignored, as on develop. isPlatformRole is false for that role, which is existing behaviour.

**G290-3 (INFO). A KS-619 name is left in a test constant.**
- `DEFAULT_TENANT = 't-default-ks619'` (new test file, line 35) is cosmetic.
- Every other KS-619 mention in the added lines explains the split on purpose: the file header, the T describe line, the unforwardableClaim doc comment and both fragments.
- None of them is code or a cell.

**G290-4 (INFO). The seat's suite line says "files 505".**
- vitest reports **169** test files (1,899 tests). The test count matches; the file count in the READY does not.

## Questions answered

1. **The split.**
   - What was removed: the tenant clause in unforwardableClaim, the KS-619 lines in its comments, and the C11-C15 cells (replaced by T1-T7). The fragments are rewritten to KS-1208 only.
   - Develop's `if (!decoded.tenantId) decoded.tenantId = DEFAULT_TENANT_ID;` is untouched. It is now head auth.ts:752 and appears in the develop diff only as a context line.
   - auth.test.ts at the head has blob 8bed53e2, the same as develop's. A diff against develop prints 0 bytes. The planted control, the same diff at round 1's head aff0f43e, prints 1,562 bytes.
   - `git diff --stat origin/develop...c7e84537` gives 4 files changed, 311 insertions (+). That is true.
   - PR title and body: I checked only the seat's draft and its prcheck output (19/19, KS keys ['KS-1208'] only), not the live text (see NOT TESTED).

2. **The guard is unchanged.**
   - In `git diff aff0f43e4079 c7e84537d2ae -- auth.ts` with comment lines filtered out, the only line left is the removed tenant clause.
   - The checks at the head:
     - userId and role: `value === '' || !isForwardableHeaderValue(value)` (:385).
     - Every copied header claim goes through `validateHeaderValue` (:368-372, :387-390). The header writes at :754-772 are the same 7 claims.
     - The refusal body (:408) is the same literal as the catch at :779.
     - The log names `claim` and no value (:400-407). C4 checks this.

3. **The no-lockout cells.**
   - The minting code is quoted under G290-2: role = `platformAdmin.role` (auth.ts:471), tenantId and tenantSlug undefined (:408-409), verificationLevel 'ENHANCED' (:404), no organizationId.
   - The T shapes match on every claim the guard reads.
   - At the head T1-T3 are served. Against round 1's auth.ts they fail with `expected [401, 0, null] to deeply equal [200, 1, 't-default-ks619']`.
   - The seat's MT reddens exactly T1, T2 and T3.
   - **My mutant G1** (a refused token on an optional mount calls next() instead): reddens **C9 only**.
   - Re-runs:
     - Develop's auth.ts: 8 of 19 red, exactly C1-C6, C9 and C10.
     - Head: 19 of 19.
     - M1: C1, C2, C3, C9, C10.
     - M2: C4, C5, C6.
   - Every plant was restored, and sha256 d203241ab30e equals the head.

4. **Round 1's findings.**
   - **G285-1: MOOT.** The tenant refusal is gone; the line above is the only code change. T1-T3 and X1-X4 are served at the head and 401 at round 1. X10, an ordinary ISSUER with no tenant, is also served in the default tenant at the head and 401 at round 1.
   - **G285-2: STILL OPEN (Low), unchanged.** X9, `organizationId: 123`, gives [401, 0] at the head and [200, 1] on develop. The PR body names it as a follow-up.
   - **G285-3: STILL OPEN, static, unchanged.** admin.ts requireAdmin still verifies the JWT itself at admin.ts:647, with no claim guard. It is mounted at index.ts:932, and only `/api/admin/audit` (:845) runs authenticateToken.
     - Its KS-619 half is now moot, because the gateway refuses no tenantless token anywhere.
     - What is left: it does not run the KS-1208 guard. It copies no claim onto a header, so it has no 500 path.
     - A board-seat follow-up is right, and it is low urgency. It fits beside KS-2152 (the login marker), because that ticket will need the same exception at this door.
   - **G285-4: STILL OPEN (Info).** The cells still run on a bare express app plus a real proxy, not index.ts with stripTrustHeaders. The seat lists it under NOT run.
   - **G285-5: STILL OPEN (Info).** The override line is develop :697 and head **:766** (it was :769 in round 1). PR 2125's head is unchanged at f9e9da889d42, and it names the expression (`tenantOverride && isPlatformRole(decoded.role)`, which follows `verifyRs256(token)`), not a line number. Both still exist at the head (:712, :766), so 2125's text stays true.

5. **Suite, tsc and eslint at the head (Node v26.8.1, vitest 4.1.12).**
   - api-gateway suite: **1,899 of 1,899**, 169 files, 0 failed.
   - Develop's auth.test.ts runs inside it: 19 of 19 in the targeted run too.
   - `tsc -p tsconfig.test.json --noEmit`: 25 errors at the head and 25 with develop's auth.ts and without the new file. The sorted lists are identical.
   - eslint src: 0 errors and 30 warnings on both trees, identical per file. Planted control (a `debugger` statement on stdin): rc 1, 1 error.
   - docs-fragments.mjs check: OK, rc 0. One cheat ADVISORY line is also in the seat's own docs_check_r2.out, so it is not new.

6. **Merge tree and overlap.**
   - `git merge-tree --write-tree origin/develop(f98afb11) c7e84537`: rc 0, tree 6fbf64bc.
   - Overlap: 58 `refs/pull/*/merge` refs (each read as merge^1..merge), matched on auth.ts, auth.test.ts, ks1208 or the KS-1208 fragments. Hits: PR 2128 only. Planted control (rateLimitEnforce.ts): PR 2064 found.
   - **KS-619 attachment and state: NOT TESTED** (see the top). The seat says 267ec431 was present after the body edit, gone on its next call, and that it made no delete; HANDOVER.md:12 says KS-619 is In Progress with 2128 not attached. I did not verify any of this, and I infer nothing about who removed it.

## NOT TESTED
- Linear: KS-619's attachments and state, and KS-2152's existence. The live PR title and body, and the edited KS-619 comment 03d2903b. All need credentials I am barred from.
- The real index.ts app with the edge strip (G285-4), and G285-3 at runtime.
- Node 24, the platform suites, a stack, the edge. No box, kintsugi or demo.
- Open PRs with no merge ref.
- Any live count of platform_admins.role. The split makes it irrelevant to this PR.

## Conduct
- I wrote only to /private/tmp/g290 and this file.
- Clone: /private/tmp/g290/repo, blob-filtered, with `--reference-if-able` /private/tmp/g285/repo. It uses the deploy key named in the Blockchain checkout's core.sshCommand, set in my clone's config only.
- In the !CODING checkout I used ls-remote only, plus plain file reads of the seat folder and one package.json.
- I did not run `npm ci`. node_modules and packages/shared/dist were APFS-cloned (`cp -c`) from g285. The lockfile and packages/ are unchanged between g285's base and develop f98afb11 (diff --stat empty).
- My extra cell file was moved, not deleted, to /private/tmp/g290/_quarantine_2026-11-09/g290-gate-extra.test.ts. The clone's `git status --short` is empty at the end. No rm.
- No .env, gh config or credential file was opened. Nothing pushed, posted or mailed.
- Hook refusals (my errors, re-issued): an unquoted `=====`, `$G` word-splitting, and one `cd`.
- Load: other processes drove load1 to 14-20 at about 19:00 AEDT. I paused with a wait loop until load1 was under 6, then ran with nice and at most 2 workers. At the end it was 5.9.
- df /Volumes/DevMASTER: 99 GiB free at the start and 99 GiB at the end. /private/tmp/g290 is 1.8 GB and is left in place, because of the no-rm rule.
