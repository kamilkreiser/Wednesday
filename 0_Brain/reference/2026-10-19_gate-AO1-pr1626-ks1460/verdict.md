VERDICT: GO WITH NOTE at head cb8e3cfee86e52a79ade3acef586b6c33cd02102 (tier 1, round 1 of 2; landing tree aa6acdbf5d52a9c9490c63aa5feb1e3c1b11cc2e on develop bc3e2e2460fff5e961cd26b70da3ab0050fccbcc; 0 blockers, 5 notes)

model: claude-opus-5-5 -- G1 (tier 1, auth public registration) -- P1-P4 no -- gauge 49%

## BLUF

- The defect is real and the fix closes it. On develop, a claim of an INVITED stub whose activating UPDATE matches 0 rows answers 201 and issues a session, a verification token and a mail (`[1,1,1,1]`), and the row stays INVITED. With the fix it answers 503 SERVICE_UNAVAILABLE and nothing is issued. I measured this twice: with the author's cells, and with my own cells that run the REAL `userRepo`/`updateUserOrThrow` over a db stub that emulates fail-closed RLS.
- A normal claim does not regress, as far as I can measure without Postgres. With no tenant header (the production shape: the gateway strips a client-sent `x-tenant-id` and sets it only from a verified JWT or API key), `updateUser` resolves the stub's own tenant through the pre-auth carve-out, the UPDATE lands and the answer is 201. A matching header also gives 201. **Unmeasured on Postgres.**
- Landing: real `--no-ff` merge tree = merge-tree = predicted `aa6acdbf5d52`. Full auth suite at the landing tree: **1,089/1,089 in 98 files, rc 0**. Ratchet at the landing tree: rc 0, 42 errors, all 42 in the baseline, 0 new. Three-dot diff = 2 files, +146/-2.
- Every cell reds on a named mutant: R1, R2, C1, C2 and C3 (6 mutants). After each mutant the source was restored to blob `fa7b3386a945`.
- The notes cover the 503's "please retry" wording when the tenant mismatch is permanent, a small enumeration delta, what a 503 leaves on the row, the census of the six remaining callers (`:1253` is the closest in severity), and the fact that the PR's cells mock the wrapper itself.

## Findings

No blockers.

**N1 (note): the 503 is permanent when the ambient tenant differs from the stub's tenant, but its message says "Please retry".** `updateUser` uses `currentTenantId()` when one is in scope (`userRepo.ts:881-883`). `tenantGucContext()` is mounted service-wide (`services/auth/src/index.ts:102`). So a caller whose request carries tenant B gets a 0-row UPDATE against stub tenant A every time. That caller is one holding a verified JWT/API key for B, or a direct service hit. My cells G3 and G5 measure 503 on every retry. Before this PR that caller got a 201 and an account that login refuses (INVITED is outside the login allow-list, `auth.ts:492` comment / `enforcePasswordLoginGates`), so the fix is strictly better. But "could not be confirmed. Please retry" will never succeed for that caller. Findings only, no fix proposed here. The unauthenticated production path does not carry a header, so it is not affected: the gateway strips `x-tenant-id` (`api-gateway/src/index.ts:326-333`) and re-sets it only at `middleware/auth.ts:427/518/522`.

**N2 (note): enumeration delta, same condition as N1.** With the fix, an email that has an INVITED stub in tenant A answers 503 under tenant B, and a fresh email answers 201 (G3 vs G6, measured). Before the fix both answered 201. This is a new "an invitation exists in another tenant" signal. It is small next to what `/register` already discloses globally: ACTIVE, SUSPENDED and DEACTIVATED emails already answer 409 "Email already registered" (`auth.ts:195-197`). For the production unauthenticated caller (no header) there is no delta: INVITED → 201, fresh → 201. I reasoned about the timing class but did not measure it. On the 503 arm, the 0-row branch skips the read-back, while the hash work, `getUserByEmail` and the INSERT are the same on both arms, so I see no extra slow-path work on the 503 arm.

**N3 (note): what a 503 leaves behind. This is pre-existing and not changed by the PR.** `createUser`'s `ON CONFLICT ... DO UPDATE` runs under the stub's explicit tenant before the claim (`auth.ts:251`, `userRepo.ts:686-694`). It writes `password_hash` (COALESCE), `display_name`, `tenant_*` and `updated_at`. After a 503 the row therefore stays `status='invited'` but carries the claimant's password hash (G3 printed `leftover password_hash hashed-new` in the emulation). It is not half-activated. Login refuses INVITED. A retry re-enters the claim path through `getUserByEmail` → INVITED, keeps the same user id (G4: retry with a matching scope → 201 with `user.id == STUB_ID`) and creates no second row (the INSERT ON CONFLICTs on `email_lookup_hash`). One consequence: C3's `passwordHash` pin guards a write that `ON CONFLICT` already makes. Mutant K2 (drop `passwordHash`) reds C3 only, and all six of my real-repo cells stay green under it. That is harmless; C3 still pins the update's shape.

**N4 (note): census of the six remaining discarding callers, and their severity. Findings only.** At the landing tree there are exactly six bare `await userRepo.updateUser(` statements in `routes/auth.ts`, at `:541, :589, :1249, :1253, :1323, :1327`. That is the author's list, byte-exact. Positive control: develop has 7 (the same six plus `:257`). A case-insensitive `updateuser` grep finds no other call form, and `userRepo` is imported once, as a namespace (`:48`).
- `:1253` (social-login callback, verificationLevel → SOCIAL) is the **closest in severity**. `user.verificationLevel = 'SOCIAL'` is set in memory (`:1254`) and the token pair is then minted over the unconfirmed write. `verificationLevel` is a JWT claim (`services/jwt.ts:198, :224`). It is a token claim over an unconfirmed write, not an activation. The claim is also arguably true for this login event, so it is lower severity than `:257`.
- `:1249` / `:1323` (social-id link): `updateUser`'s fieldMap has no social-id columns, so ZERO statements are issued and `updateUser` returns the non-null read-back. **`updateUserOrThrow` would not catch these.** The code comments at `:1235` and `:1299` document this. `/social/link` answers `linked: true` over nothing (BACKLOG).
- `:1327` (`/social/link` verificationLevel): no token is minted there; the user gets a false "linked" answer.
- `:541` (UPGRADE-ON-VERIFY rehash) sits inside a try/catch, non-fatal by design. The old hash is still valid, so no credential is lost.
- `:589` (`lastLoginAt`): the session is issued over an unconfirmed timestamp write. That is not a credential or activation.
- None of the six issues a credential or session over an unconfirmed *activation or credential* write in the way `:257` did. `:1253` is the nearest.

**N5 (note): what the PR's cells mock, and why R1 is not vacuous.** The PR's test mounts the REAL `authRoutes` and the real `errorHandler`. It mocks `../repositories/userRepo` whole, *including `updateUserOrThrow`, which it re-implements* (throws `ServiceUnavailableError` when `updateResult` is null). It also mocks `services/password` (hashPassword only), `services/jwt` (generateTokenPair only), `services/session`, `services/email`, `../events`, `../db` and both loggers. The cells therefore pin that the route CALLS the wrapper and lets its throw reach a 503. They do not pin the wrapper itself. R1 is not vacuous: C1, under the same mock with a non-null result, answers 201, and K3 (back to `updateUser`) reds R1. My G3 measures the real wrapper's 503 and its error shape. The sibling routes `/reset-password` (`auth.ts:848`, 'Password reset') and `/verify-email` (`:892`, 'Email verification') use the same wrapper, the same `ServiceUnavailableError` → 503, and the same `{success:false,error:{code:'SERVICE_UNAVAILABLE',message:'<operation> could not be confirmed. Please retry — if you already succeeded, you may not need to.'}}` shape. The shape was read at `userRepo.ts:960-976` and `errorHandler.ts:77-81`, and measured for this route in G3.

## What was tested and how

All work ran in `/private/tmp/wed_gate_ao1/`. The clone was made with `git clone --shared` from Wednesday's cache clone, then the PR head and develop were fetched over the cache clone's SSH command, set repo-local in my clone. npm, vitest and node were pointed into the clone with `--prefix` or absolute paths, never with the WEDNESDAY tree as cwd.

1. **Heads**, read with `ls-remote` at start and again before writing: #1626 `cb8e3cfee86e52a79ade3acef586b6c33cd02102`, develop `bc3e2e2460fff5e961cd26b70da3ab0050fccbcc`, both unchanged. The two commits are `619106f17` (Spark) and `cb8e3cfee` (C3). The post-image blobs are `fa7b3386a945` (auth.ts) and `833969b2d518` (test), which equal the author's declared ones. The C3 commit touches only the test file.
2. **Landing:** `merge-tree --write-tree gh/develop pr1626` gives `aa6acdbf5d52`. A real `git merge --no-ff` in worktree `land/` gives tree `aa6acdbf5d52`. Positive control: `merge-tree` with `pr1626~1` gives `8bcdcd804a7a`, a different tree. Three-dot diff: 2 files, +146/-2.
3. **Install and build:** a full `npm ci --prefix land/Blockchain/Dev`, then `npm run build --prefix .../packages/shared` (rc 0). The first suite run used a workspace-limited install (`-w packages/shared -w services/auth`). It loaded 97/98 files: `ks1009-wallet-status-reveals-only-existence.test.ts` failed with `Cannot find module 'js-yaml'`, an install artefact (js-yaml is hoisted from another workspace). After the full `npm ci`, all 98 loaded.
4. **Full auth suite at the landing tree:** `npm run test --prefix land/.../services/auth -- run` gave Test Files 98 passed (98), Tests 1089 passed (1089), rc 0.
5. **Ratchet at the landing tree:** `node .../scripts/typecheck-tests/check.cjs .../services/auth` gave rc 0, 149 files, 42 errors, 42 in the baseline, 0 new. **Positive control:** planting `const __ao1PositiveControl: number = 'x';` in the new test gave rc 1 with 2 NEW errors. I restored the file with `git checkout`, re-ran, and got rc 0 / 0 new.
6. **Red-first:** I put the PR's test file into the develop worktree `dev/` and ran it against develop's `auth.ts`. Result: 3 failed | 2 passed (5). R1 `expected 201 to be 503`; R2 `expected [1,1,1,1] to deeply equal [1,0,0,0]`; C3 `expected [] to have a length of 1` (develop calls `updateUser`, not OrThrow). The author reported "2 failed | 2 passed (4)" for the 4 Spark cells; C3 is the fifth. At the landing tree: 5/5.
7. **Gate cells G1-G6** (my own, at `/private/tmp/wed_gate_ao1/zz-gate-ao1-real-repo.test.ts`, moved out of the tree after use): the REAL `userRepo` (real `updateUser` and `updateUserOrThrow`, real lookupHash and PII encryption with a fixed test DEK and a registered test HMAC key), the real router, the real `tenantGucContext()` and the real `errorHandler`. `../db` is a stub that emulates fail-closed RLS (an UPDATE or SELECT on `users` matches only when the effective tenant equals the row's `tenant_id`; the `auth_find_*` carve-outs ignore the tenant). The cells are G1 no header → 201, UPDATE under the stub's tenant A, row active; G2 header A → 201; G3 header B → 503, real message, `[sessions, token INSERTs, mails] = [0,0,0]`, row invited; G4 503 then a no-header retry → 201, same id; G5 three retries under B → 503 each, row invited; G6 fresh email under B → 201. At the landing tree: 6/6. **Positive control at develop:** G3, G4 and G5 red (`expected 201 to be 503`), and G1, G2 and G6 green.
8. **Mutants** were applied to the landing tree's `auth.ts` by script (`/private/tmp/wed_gate_ao1/mut.py`, one-occurrence assert). Each run covered the PR's 5 cells plus G1-G6. After each mutant the file was restored with `git checkout` and `hash-object` read `fa7b3386a945` every time. 0 load or transform errors in any mutant log.

| mutant | PR cells red | G cells red |
| -- | -- | -- |
| K1 drop `status: 'ACTIVE'` | C3 | G1 G2 G4 |
| K2 drop `passwordHash` | C3 | none (ON CONFLICT already writes it, N3) |
| K3 back to `updateUser` | R1 R2 C3 | G3 G4 G5 |
| K4 (mine) a verification token stored before the claim | R2 C1 | G1 G3 |
| K5 (mine) throw after a confirmed claim | C1 C3 | G1 G2 G4 |
| K6 (mine) claim guard → `if (true)` | C2 | G6 |

   Every cell reds on at least one mutant: R1 on K3; R2 on K3 and K4; C1 on K4 and K5; C2 on K6; C3 on K1, K2, K3 and K5. The author's "K1/K2 → C3 only" holds across the five PR cells.
9. **Scope:** both commit messages say `Refs KS-1460`. The close-keyword census over the PR's commit bodies found 0 matches. Positive control: the same regex finds 3 in develop's last 200 commit bodies. I ran the six-caller census at the landing tree and at develop (N4).
10. **Tenant path read:** `userRepo.ts:796-934` (`updateUser`, QA F-1 resolution), `:509` (`getUserByIdPreAuth`, the SECURITY DEFINER carve-out), `db.ts:47-70`, `packages/shared/src/db/tenant-guc.ts`, `migrations/039_rls_fail_closed.sql` (policy and NULL-tenant backfill), `services/auth/src/index.ts:102`, and the gateway strip and set sites listed in N1.

## NOT RUN

- Any Postgres: no live register against a real `users` table under RLS. The RLS behaviour is an emulation in a db stub, so "a normal claim does not 503" is **unmeasured on Postgres**.
- Docker, any deployed environment, the gateway in front of the service.
- The timing class for enumeration (N2) is reasoned, not measured.
- Whether gateway optional-auth decorates the public `/register` with a JWT's tenant, which is the reachability of N1/N2 in production. I read the set sites only.
- The PR body on GitHub (no `gh` read). The close-keyword check covers the commit messages only.
- Other services' suites, the platform suites, the author's preflight legs 3/4/8.
- The open-PR overlap census (taken by the author at `115797747cb6`; not re-taken).

## WEDNESDAY tree after the gate

`git -C /Volumes/DevMASTER/WEDNESDAY status --short`, run before finishing: 10 modified `0_Brain/dashboard/data/*.json` (dashboard data), `?? 0_Brain/reference/2026-10-19_gate-AO1-pr1626-ks1460/verdict.md` (this file), and three paths that are NOT this gate's: `?? 2_Project_Files/local-model/night/briefs/ks_1639_p1/`, `ks_1653_p1/`, `ks_1658_p1/`. Their mtimes are 23:58-00:03 AEDT, during this gate, and the files are golden.diff / KS-*.md / spark.pins, which is the night-run brief shape. This gate never wrote under `2_Project_Files/`. Nothing is at the WEDNESDAY root.
sha256: eecfec588ba2ce64949b5e9991fb697125a9b8f5e5ee71ef92f3c53956f8edcb
