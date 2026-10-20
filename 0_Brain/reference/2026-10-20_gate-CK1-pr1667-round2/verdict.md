VERDICT: GO WITH NOTE at head c502c6434cf2... (tier 1, round 2 of 2; landing tree 52968b7b9e65 on develop 561a6c5b5282; 0 blockers, 5 notes)

## BLUF
- **Round 2 does what Wednesday ruled.** The admit rule on all three GETs is now `isPlatformRole(role) || (userId !== '' && userId === issuer.id) || (userId !== '' && userId === holder.id)`.
  - The refusal is still the one `certificationNotFound` body, byte-identical to unknown-id.
  - The check still runs before the expiry write, the share lookup and the charge event.
  - SYSTEM_ADMIN, system_admin, SUPER_ADMIN and super_admin get 200 on a non-party's certification on all three routes. ORG_ADMIN gets 404. `platform_admin` gets 404 (R18).
- **The round-1 regression is closed. The two test gaps are closed.** M8 is killed by R16 and M9 by R17. I built 8 mutants and all 8 were killed.
- **The suite at the landing is 136 files / 1613 tests / 0 failed.** That is +37 by name over develop and 0 vanished. Develop moved during the gate (21e2ffd → 561a6c5). The move only touches a vc-issuer test file, and originate's tree in the two landings is identical (`a1e49300f64e`).
- **KS 1591 (dotless-i, long-s, array role):** these ARE admitted on this read path. I measured it through the real router: 200 on all three routes. It is **not reachable from any token minter in the repo** (source-read, inferred). I judge that round 2 does not trade a real regression for a spoofable admit. Keep `isPlatformRole` and fix KS 1591 inside it.
- **Notes, not blockers:**
  - (N1) The claim's arm table is off by one.
  - (N2) R18's "gateway-only" premise is wrong. Auth mints `platform_admin` verbatim, while no auth path mints upper-case `SUPER_ADMIN`.
  - (N3) An exact HOLDER compare is still unpinned.
  - (N4) The function docstring still says "the rule the LIST route already applies".
  - (N5) KS 1591 is measured on the handler but its reachability is inferred.

## Findings

**Q1 Delta vs round 1, read whole.**
- `git diff d7c2e296c909..c502c6434cf2`: product change is `certifications.ts` +8/-2:
  - one new import, `import { isPlatformRole } from '@secuura/shared'`;
  - the literal role set replaced by `if (isPlatformRole(authUser?.role as string | undefined)) return true;` with a comment.
- The test file is +98 (C10×4, C11, R18, R15, R16, R16b, R17×4, R17-control, plus a MIXED_CERT fixture).
- The third file in the range, m365 `ks1677-…pkce…test.ts`, comes from develop's merge, not the author.
- Three-dot vs live develop: 2 files, +503/-3 (`certifications.ts` +72/-3, the test file +434). No lockfile, `package.json` or `packages/shared` change: their blobs are identical across 7e3b9362e08b, develop and the head.
- Admit rule (`certifications.ts:155-166`):
  - `isPlatformRole` first.
  - Then `userId` is `req.user.userId` if it is a string, else `''`. `''` → false.
  - Then the exact `===` against `issuer?.id`, then `holder?.id`. That equals the brief's rule.
- `isPlatformRole` is at `packages/shared/src/security/keyRevokePolicy.ts:140`, body `PLATFORM_ROLES.has(String(role || '').toUpperCase())`, `PLATFORM_ROLES` at `:60`, exported `index.ts:229`. All as claimed.
- **Refusal and unknown-id:** both go through `certificationNotFound` on all three routes (`:1019/:1025`, `:1479/:1485`, `:1566/:1572`). Body: `{"success":false,"error":{"code":"NOT_FOUND","message":"Certification not found"}}`. K4 asserts this literally on lineage and evidence-bundle; R4 asserts it on `/:id`.
- **Ordering:**
  - `/:id`: the check at `:1024` comes before the expiry `saveCertification`.
  - Lineage: `:1484` comes before `getSharesByCertification`.
  - Evidence-bundle: `:1571` comes before the share, lineage and charge reads and `createChargeEvent('evidence_export')`.
  - Measured by K3: a refused reader gives 0/0/0/0/0 calls to save, shares, lineage events, charge read and charge write. The issuer control hits save, shares ×2 and charge write ×1.
- `callerMayReadCertification(` has exactly 3 call sites (`:1024 :1484 :1571`). Control: the same grep finds the definition at `:155`.

**Q2 KS 1591 reachability.**
- **Where `req.user.role` comes from (source-read):**
  - `certificationsRouter.use(authenticate())` (`certifications.ts:66`).
  - `authenticate` (`middleware/auth.ts`) RS256-verifies the bearer and `setUser(req, decoded)` puts the decoded claim on `req.user` verbatim. There is no normalisation and no header fallback on this router.
  - Mounted once, at `originate/src/index.ts:258`.
- **Who mints the role claim (source-read):** only `services/auth/src/services/jwt.ts`.
  - **Users:** `role: user.role`, where `user.role` comes from `mapDbRole` (`userRepo.ts:257-275`). That is a dictionary lookup onto the `UserRole` union (`types/index.ts:8`: OWNER, ISSUER_ADMIN, ISSUER_APPROVER, VERIFIER, ORG_ADMIN, SYSTEM_ADMIN), with unknown → `'OWNER'`. Role writes from the API go through `normalizeAssignableRole` (`routes/users.ts:217`), an allow-list (KS-486).
  - **Platform admins:** `routes/auth.ts:451-453` mints `role: platformAdmin.role` verbatim from `platform_admins.role`, which is `CHECK (role IN ('super_admin','platform_admin','platform_viewer'))` (`docker/init-platform/01-platform-schema.sql:80`). The only seed is `'super_admin'` (`deployment/azure/migrate/run-platform.sh:144-147`).
  - **Connectors:** `role: 'connector'` (`jwt.ts:291`).
  - `TokenRotationService.jwt.sign` (`packages/shared/src/security/token-rotation.ts:151`) has no service caller (case-insensitive grep over `services/`, non-test: 0 files; control: 2 files in `packages/shared/src`).
  - So no minter can emit a dotless-i, long-s or array role. That needs the auth signing key, or a hand-edited `platform_admins` row that the CHECK would refuse. **Inferred, not run.** I found no other minter but did not prove there is none.
- **Measured on the real router (K1):** `super_admın` (U+0131), `ſuper_admin` (U+017F), `['SUPER_ADMIN']` and `['system_admin']` as a non-party reader each get **200 on all three routes**. Control: the same reader with ORG_ADMIN gets 404/404/404. Round 1's literal set refuses all four: K1 is red on the round-1 arm.
- **Judgement:** the admit is real on the handler but unreachable from any in-repo minter, so it is not a spoofable admit in practice. Ranking:
  1. Keep `isPlatformRole`. There is one definition, and the KS 1591 fix belongs inside it (exact match on a string, no `toUpperCase` folding of non-ASCII), which then fixes every caller at once.
  2. originate's own `hasAnyRole(user, ['SYSTEM_ADMIN'])` (`middleware/auth.ts:168`). It is exact (`super_admin`/`SUPER_ADMIN` alias to SYSTEM_ADMIN), refuses the three KS 1591 forms, and drops lowercase `system_admin`, which no minter emits. A sound fallback if KS 1591 is not fixed soon.
  3. A hand-written exact set (the two upper-case spellings plus lowercase variants). This is the second-copy drift that `keyRevokePolicy.ts` exists to prevent, and it is how round 1 missed SUPER_ADMIN.
  - ORG_ADMIN is not admitted (M4 killed).

**Q3 Regression closed; three-arm table.** All runs are the author's 37 cells plus my 7, real router, `npm test` with cwd = originate.

| arm | route blob (sha256) | author's file | mine |
|---|---|---|---|
| develop (no check) | `6abd05c5ea2f25f1` | **22 failed / 15 passed** | 6 red / 1 green (K0, control) |
| round 1 literal set | `b0ea5cc5f1f90195` | **3 failed / 34 passed**: C10[SUPER_ADMIN], C11, R18 | K1, K2 red |
| this head | `cd23193dd298622c` | **37 / 37** | 7 / 7 |

- Every failure is by `expect(` assertion. There are 0 suite exec errors.
- Restored to `cd23193dd298622c`, sha-asserted; `git checkout` back to the head.
- See N1 for the gap against the claim.
- K2 (all three routes, non-party reader):
  - 200: `system_admin`, `SYSTEM_ADMIN`, `super_admin`, `SUPER_ADMIN`, `System_Admin`.
  - 404: `ORG_ADMIN`, `platform_admin`, `platform_viewer`, `' SUPER_ADMIN'`, `'SUPER_ADMIN\0'`, `admin`, `''`.

**Q4 The two new gaps and mutants.** Each mutant compiled first (`tsc --noEmit -p originate` rc 0). The anchor count was 1 each time. Failures were parsed from `jest --json`, all by assertion, with 0 suites failing to run. Restore was sha-asserted every time; final restore True.
- **M8** (lineage check after `getSharesByCertification`) → **R16**, K3.
- **M9** (case-insensitive issuer compare) → **R17[upper-cased]** only.
- Author's others, re-run:
  - M1 (drop holder arm) → C2, K5.
  - M2 (drop `''` guard) → R13, K6.
  - M3 (check after expiry write) → R6, K3.
  - M4 (`|| role === 'ORG_ADMIN'`) → R14, R15, K1, K2, K3.
- **Mine:**
  - **X3** (revert to round 1's literal set; the first build failed tsc TS6133 on the unused import, so I re-built it with `void isPlatformRole;` and rc 0 before counting) → C10[SUPER_ADMIN], C11, R18, K1, K2.
  - **X4** (case-insensitive HOLDER compare) → **killed only by my K5**. It survives all 37 of the author's cells (N3).
- Total: 8 built, 8 killed.

**Q5 Round 1 still holds.**
- K6 on the head (all three routes):
  - a and a2 get 404.
  - Connector c gets 200 on its holder-less cert and 404 on the human cert. A different connector id gets 404.
  - Tenant b, and the issuer calling from tenant b, get 404.
  - On the bare row, a `userId` of `''`, absent, `['x']` or `0`, and `req.user = null`, all get 404. A SYSTEM_ADMIN with `userId ''` gets 200 (control).
- **Suites by unique `path + fullName`:**
  - 7e3b9362e08b: **135 / 1575**.
  - develop 21e2ffd: 135 / 1576.
  - Landing (`commit-tree` of `ffc4db54b24c`, which equals a real `git merge` of develop into the head): **136 / 1613 / 0 failed / 0 exec errors**.
  - develop → landing: +37, all in the new file, 0 vanished.
  - base → landing: +38 (adds develop's `ks1659…` cell), 0 vanished.
- **The new file type-checked in its own program** (child tsconfig extending originate's, `files: [the test]`; `--listFilesOnly` lists it once): rc 0. Positive control: a copy with `const TENANT: number = '…'` gives rc 2, with TS2322 at line 70.
- ts-jest also type-checks at load. My own first cell file LOADFAILED on TS6133, and I fixed it before counting.
- Originate `tsc --noEmit` at the landing: rc 0.
- **merge-tree:**
  - On develop 21e2ffd: `ffc4db54b24c8efaee75e7758d58d04a817fe48b`, equal to the claim.
  - On LIVE develop 561a6c5 (moved at 03:44Z): **`52968b7b9e65c60173a89855cc01b904b7dd52bf`**. It differs from ffc4db only by `services/vc-issuer/src/__tests__/ks1116-…test.ts`, and the originate subtree is identical (`a1e49300f64e`).
- merge-base is f01ba49da56d. The develop moves 7e3b9362e08b → 561a6c5 touch neither PR file (`git diff` on the two paths is empty; control: 12 other files changed). The auth `routes/auth.ts`/`users.ts` changes on develop have 0 `role` lines (control: 53 inserted lines).

**Q6 Known residue against the code.** I did NOT read the PR body itself (gh is not allowed). I checked the claims as the READY states them.
- **N1 (verify/share/recertify sidestep, KS-1699):** accurate. `POST /:id/verify` (`:1146`), `/:id/share` (`:1216`) and `/:id/recertify` (`:1317`) call `getCertification` with no per-record caller check.
- **The by-id read is more permissive than the list for SUPER_ADMIN:** accurate. The list's `isAdmin` (`:954`) is still `system_admin|SYSTEM_ADMIN|super_admin`. Also true for `System_Admin` and the KS 1591 forms.
- **KS 1536 / KS 1591 references:** consistent with the code. KS 1536's quoted line `PLATFORM_ROLES "<-- no platform_admin"` matches `:60`. I did not read Linear.
- **Stale E2E spec:** unchanged. The three-dot diff does not touch `tests/e2e`, so round 1's N4 stands.
- **Sentences that describe something that is not so:** see N2 (R18's comment) and N4 (the docstring). I found no sentence that describes a guard that does not exist.

## Notes
- **N1 (claim accuracy):** the claim's table reads develop "21 failed / 15 passed" and round 1 "2 failed / 34 passed, exactly C10[SUPER_ADMIN] + C11". Each pair sums to 36, not 37. Measured: **22/15** and **3/34**.
  - The extra cell is R18 in both arms.
  - On develop, R18 is red at `:376` (`platform_admin` gets 200).
  - On round 1, R18 is red at its own SUPER_ADMIN control line `:381` (404 ≠ 200).
  - Every cell's outcome is still right. Only the reported counts are wrong.
- **N2 (R18's premise; source-read):**
  - R18's comment and the brief call `platform_admin` a "GATEWAY-only spelling". In fact auth mints it verbatim for a `platform_admins` row whose role is `platform_admin` (`routes/auth.ts:451-453`; the CHECK permits it). There is no such row in the repo's seed (`super_admin` only).
  - Conversely, no auth path found mints upper-case `SUPER_ADMIN` or lower-case `system_admin`. Users get `SYSTEM_ADMIN` via `mapDbRole`; platform admins get `super_admin`.
  - So the spelling round 2 newly admits is one no in-repo minter emits. The one admin spelling that is refused (`platform_admin`) is mintable, though only for a hand-inserted row.
  - This does not change the verdict: ruling (a) stands and the code matches it. Wednesday may want the premise corrected in the R18 comment or KS 1536.
- **N3 (test gap, measured by X4):** nothing in the 37 pins an exact HOLDER compare. R17 covers only the issuer arm, so a case-insensitive holder compare survives every cell. My K5 kills it. This is low risk (the code uses `===`), but it is a cell worth adding.
- **N4 (doc text, source-read):**
  - The `callerMayReadCertification` docstring (`:141-143`) still says "The rule is the one the LIST route already applies … a refused reader is one the list already hides the row from." That is now false for SUPER_ADMIN, `System_Admin` and the KS 1591 forms. The new inline comment directly below corrects it.
  - The comment's "(:906)" is develop's line numbering; it is `:954` at the head.
  - The test file header repeats "the rule the LIST route already applies".
  - None of this describes a missing guard.
- **N5 (KS 1591 reachability is INFERRED):** the admit of the three forms is measured on the handler. Their unreachability rests on reading `jwt.ts`, `mapDbRole`, `normalizeAssignableRole` and the platform CHECK. I decoded no live token and read no deployed `platform_admins` table.

## FOUND / TESTED / HOW
- **FOUND:**
  - The rule matches the brief exactly on all three GETs. It runs before every side effect, and the refusal equals unknown-id.
  - Landing reproduces (ffc4db on 21e2ffd; 52968b on live 561a6c5).
  - The suite is +37 by name with 0 vanished.
  - The claim's counts are off by one (N1).
  - The R18 premise is inaccurate (N2).
  - The holder compare is unpinned (N3).
- **TESTED:**
  - The author's 37 cells on three arms.
  - My 7 cells (K0-K6) on three arms.
  - 8 mutants: 6 of the author's (M1-M4, M8, M9) and 2 of mine (X3, X4).
  - Three full originate suites by name.
  - A separate test-file tsc with a positive control.
  - merge-tree on both develop heads, plus a real merge.
- **HOW:**
  - `git clone --shared` of the spark cache into `scratchpad/gate_ck1/src`. Fetched `refs/pull/1667/head` and `develop` from GitHub over the Blockchain deploy key (read only).
  - Ran `npm ci --prefix <clone>/Blockchain/Dev --ignore-scripts --workspace=packages/shared --workspace=services/originate --include-workspace-root`, then `npm run build --prefix …/packages/shared` and `npm run generate --prefix …/services/originate`.
  - Ran tests with `npm test --prefix …/services/originate`. The mutant runner (`scratchpad/gate_ck1/tools/mutants.py`, run with `python3 -I`) used subprocess `cwd=<originate>`.
  - No PGlite was needed this round, and nothing from m365 was run.
  - My cell file was copied into `__tests__` for the arm and mutant runs and moved out with `mv` before the full suites. The clone's `git status` was clean afterwards.

## NOT RUN
- No real gateway, real JWT decode, real Postgres, Docker, or the four platform suites.
- No `services/auth` run. Its role-minting reading is source-only.
- No E2E, and no OWNER, `MULTI_TENANCY_ENABLED=true`, share-recipient or `onBehalfOf` reader.
- The PR body and Linear (KS 1536/1591/1699) were not read. No GitHub, Linear or gh writes, and no push.
- Nothing under `!CODING` was written. Its only use was the deploy key path for the fetches.
- I did not re-run the full suite on the 561a6c5 landing. Its originate subtree is identical to the measured landing's.

## Housekeeping
- **Heads:**
  - Start (03:35:15Z): PR `c502c6434cf299d09b47b7b0ca354338f5892410`, develop `21e2ffd20795cabb3758677380ffb4f90da51ab5`.
  - End (03:45:02Z): PR unchanged; develop `561a6c5b528289f4d7ecd19f9c069501e925e9ea` (one vc-issuer test-only commit, KS-1116). I re-derived the landing on it: `52968b7b9e65`.
- `git -C /Volumes/DevMASTER/WEDNESDAY status --short` before writing: no untracked path is outside `0_Brain/`, `5_Project_History/`, `2_Project_Files/local-model/` or `2_Project_Files/fleet/briefs_staged/`. This gate's only write in WEDNESDAY is this `verdict.md`.

## Wall-clock
- 03:34:56Z start → about 03:48Z verdict written (about 13 minutes).
- Arm runs: about 4 s each. Mutant batch: about 40 s. Full suites: about 25 s each.
sha256 (sed '1d;$d' verdict.md | shasum -a 256): d7b463392ac28aab14e11541b22253bdc21ba013be4e729a280cd0fa247a8edc
