# Gate verdict: Secuura Platform K PR #1543 (KS-759, two deleted type casts in originate)
Report sha256/16: bb6259a0504dd87a
Gate: independent QA, SONNET tier 2, findings only. Date 2026-10-13.

**Head under test:** `502b164e4f863df4a685315ffa600b2e910ab958`, tree `009d57d2f5e61fce05be01bdbd6b7ecabc25d3b8` (asserted equal to `refs/pull/1543/head` fetched by me), one commit on develop `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e` (`git rev-list --count a7cffc8..pr1543` = 1; parent asserted).
Live develop tip asserted: `29bb45342e6a65c047ed902aafeae6525529f150`.
All raw outputs: `evidence/` beside this file. Work done in a `git clone --shared` in my scratchpad (push URLs set to DISABLED), no git write verb in the project folder, nothing written under `!CODING`.

## VERDICT: GO WITH NOTE
0 Major, 2 Minor. The change is what it says: two files, +4/-6, types only, value-equivalent, and the compiler now checks the four reads. The notes are about what the evidence does and does not cover, not about the diff.

Tier check (brief asked for this FIRST): the diff touches exactly two files and changes no runtime value. No tier raise needed.

## 1. Diff, whole (FOUND / TESTED / HOW)
- `git diff a7cffc8...pr1543` : `--stat` = 2 files, 4 insertions, 6 deletions (evidence/diff-stat.txt, diff.txt). Files: `Blockchain/Dev/services/originate/src/routes/gdpr.ts`, `.../platformOrganizations.ts`. Instrument: git itself; control = the same command on the 29bb4534 range printed 10 other files (evidence/develop-moved-stat.txt), so the stat does list extra files when they exist.
- Both functions read before and after. Before: `claims = user as unknown as {tenantId?, organizationId?} | undefined`, reads `claims?.tenantId`, then after `if (!user || !tenantId) return null`, `claims?.organizationId`. After: `user?.tenantId`, then `user.organizationId`.
- **Can `user.organizationId` and `claims?.organizationId` differ?** No, for any input. `claims` is the identical object reference as `user` (a cast emits no code). At the read, the guard has already returned for `user` undefined/null/falsy, so `claims?.x` and `user.x` both evaluate `user.x` on a truthy object. `JwtPayload` (`services/originate/src/middleware/auth.ts:15`) declares `organizationId?: string` and `tenantId?: string`, the same `string | undefined` the cast declared, so the static type is unchanged too. Cases: null user -> returns null before either read; user without the field -> undefined both; connector principal (`userId: connector:<id>`, role connector, claims from the verified JWT) -> same value both; platform role -> cannot reach it: all four call sites are behind `requireRole(...CONNECTOR_ROLES)` (gdpr.ts 521/552 via `gdprRouter.post('/erasures', requireRole(...)` and its sibling; platformOrganizations.ts:93 and :151).
- **Is `user` provably non-null at `user.organizationId`?** Yes. The only path to the `return {...}` is past `if (!user || !tenantId) return null;` with no assignment to `user` between (const). I also proved it by machine, not by reading: mutant `nullpath` (`user?.tenantId` -> `user.tenantId`) and `orgearly` (read `user.organizationId` BEFORE the guard) both give `tsc` rc 2 with `TS18048: 'user' is possibly 'undefined'` at gdpr.ts(472,20) and platformOrganizations.ts(54,20) (evidence/mut-nullpath-both-tsc.txt, mut-orgearly-both-tsc.txt); the as-committed read at the end does not error (tsc rc 0), so narrowing is doing the work.

## 2. The four-error reading, reproduced on the committed tree
Instrument: `node_modules/.bin/tsc --noEmit -p services/originate/tsconfig.json` (TypeScript from the project's own node_modules, copied; `packages/shared` rebuilt at head first). The experiment deletes `tenantId?` and `organizationId?` lines from `interface JwtPayload` (script `delfields.py`, diff shown to be 2 deleted lines in auth.ts only).
| tree | JwtPayload fields | tsc rc | errors | evidence |
|---|---|---|---|---|
| develop a7cffc8 | present | 0 | 0 | tsc-develop-normal.txt |
| develop a7cffc8 | both deleted (POSITIVE CONTROL: the casts hide the reads) | **0** | 0 | tsc-develop-fields-deleted.txt |
| head 502b164 | present | 0 | 0 | tsc-head-normal.txt |
| head 502b164 | both deleted | **2** | **exactly 4 TS2339**: gdpr.ts(472,26) tenantId, gdpr.ts(477,26) organizationId, platformOrganizations.ts(54,26) tenantId, platformOrganizations.ts(56,104) organizationId | tsc-head-fields-deleted.txt |
Author's reading CONFIRMED, positions identical to the brief. (First attempt of my own script deleted only one field because it cut at the first `}` inside the doc comment; I caught it from the 2-error output, fixed it, and the table is from the fixed run.)
- eslint: `eslint services/originate/src/routes/gdpr.ts .../platformOrganizations.ts` run from `Blockchain/Dev` (env -C, so the flat config's base path applies) rc 0, 0 problems (eslint-head.txt). CONTROL that it can fail: appended `const unusedControl: any = 1; debugger;` to gdpr.ts -> rc 1, "error Unexpected 'debugger' statement" (eslint-control.txt). My FIRST eslint run printed "File ignored because outside of base path" with rc 0 and was a false green; discarded, the rerun above is the evidence.
- `git grep -n "as unknown as { tenantId"` : head = 0 hits (evidence/grep-head-cast.txt); CONTROL on develop a7cffc8 = 2 hits, gdpr.ts:472 and platformOrganizations.ts:54 (grep-develop-cast-control.txt).

## 3. Census of other cast/any reads of tenantId/organizationId off the user
Instrument: `git grep -E` over `Blockchain/Dev/*.ts|*.js|*.tsx|*.mjs|*.cjs` at head (grep-head-broad.txt, grep-head-shape-casts.txt). Author's "these were the only two" is TRUE for the exact shape `user as unknown as { tenantId?; organizationId? }`, and that is all it is true for. The frame misses the same hiding mechanism in other spellings:
- `(req as any).user?.tenantId|organizationId` in NON-test source: 27 lines (originate 11: adminConfig.ts:947,1069,1070, certifications.ts:378,523, documents.ts:100,119,391,507,743,1019; security 11: index.ts 765,819,870,1093,1150,1151,1183,1192,1434,1435 plus the 1633/1747 messages; tokenisation/src/index.ts 4 lines (63,66,95,98); packages/shared/src/security/audit-logger.ts:214).
- Typed local re-casts of the same payload: security/src/index.ts:1179,1352,1415; anchoring/src/index.ts:474; api-gateway/src/routes/platform.ts:530; auth/src/routes/issuerCerts.ts:119; auth/src/routes/oauth.ts:102.
- Tests are included in the grep (several `(req as any).user = {...}` fixtures); they are fixtures, not reads, and I excluded them from the 27.
Consequence: deleting a field from originate's JwtPayload still compiles for the 11 originate `any` reads. The PR is correct about what it fixed; "casts hid the reads" remains true elsewhere. I did NOT classify which of those 27 should become typed reads. (Minor 2.)
- Also true to note: `originate/src/index.ts`, `adminConfig.ts` etc. read `(req as any).tenantId` (a property of req, not of the JWT payload); those are a different pattern and out of this PR's frame.

## 4. Suites
Environment: scratch PostgreSQL 15.14 (Homebrew binaries, own data dir in my scratchpad, port 55491 checked free with lsof; 55418 and 55436 never touched, and verified still listening and untouched at the end). Schema = `docker/init/*.sql` + `docker/init-platform/*.sql` + `scripts/run-migrations.sh` (applied=51 failed=0, evidence/migrations.log), `secuura_app` created by the project's own `01-create-app-role.sh`; `secuura_app` verified `rolsuper=f rolbypassrls=f`, and the suites' own SETUP cell asserts the product connected as that role. Prisma client generated with the project's `npm run generate`. Harness deviations (mine, disclosed): migration 003_platform_tenancy.sql also applied to the main DB (it routes by filename to the platform DB only, but the tests insert `tenants` into the main DB); `GRANT ALL ON ALL TABLES/SEQUENCES TO secuura_app` (broader than the real role's grants; RLS still binds it); for MT=true the platform URL points at the same database as main (the tenant manager reads `tenants` from the platform URL and the tests seed the main one).
| run | head 502b164 | develop a7cffc8 | evidence |
|---|---|---|---|
| originate unit (jest, `--silent`) | 105 suites / 1321 passed, rc 0 | 105 / 1321, rc 0 | jest-originate-head.txt, -develop.txt |
| gdpr unit cells (`jest gdpr`) | 7 files / 87, rc 0 | 7 / 87, rc 0 | jest-gdpr-head.txt, -develop.txt |
| ks695 erase-connector integration, MULTI_TENANCY_ENABLED=false, product as secuura_app | 3 files, 48/48 | 48/48 | jest-int-head-MTfalse.txt, jest-int-develop-MTfalse.txt |
| same, MULTI_TENANCY_ENABLED=true | 48/48; per file via jest json: erase-connector.integration 15/15, fallback-principal 8/8, selector-bounds 25/25 | 48/48 | jest-int-head-MTtrue.txt/.json, jest-int-develop-MTtrue.txt |
Author's numbers match mine (105/1321, 7/87, 15+8+25, both modes, same as develop). Merged tree (head's two files onto live 29bb4534): originate tsc rc 0, unit 105/1321 rc 0 (tsc-merged-tree.txt, jest-originate-merged.txt).
Controls that each harness can fail: the mutants in section 5 turn unit red (36, 51, 3 failures), integration red (21, 28, 48 failures in both modes) and tsc red (2 errors). My first MT=true integration attempts failed 48/48 on "tenant configs did not load" (my harness setup), which also shows the KS-1311 guard refuses a mislabeled mode; the run above is after the fix.
`check:openapi` and preflight were NOT run (see section 7).

## 5. Mutants (applied to the head in the scratch tree, restored after each)
| mutant | tsc | unit (1321) | integration x2 modes (48) | seen by |
|---|---|---|---|---|
| swap fields in BOTH files (`tenantId = user?.organizationId`, `organizationId: user.tenantId`) | rc 0 (same type, not a type error) | 36 FAIL (ks695-ask3-erase-connector-erasure, -refusals) | 21 FAIL both modes | runtime cells, not tsc |
| same swap in gdpr.ts ONLY | 0 | **0 fail** | **0 fail** | **NOTHING: SURVIVES** |
| same swap in platformOrganizations.ts ONLY | 0 | 36 FAIL | 21 FAIL both | unit + integration |
| `organizationId: undefined` in gdpr.ts ONLY | 0 | **0 fail** | **0 fail** | **NOTHING: SURVIVES** |
| `organizationId: undefined` in platformOrganizations.ts ONLY | 0 | 51 FAIL | 28 FAIL both | unit + integration |
| `user?.tenantId` -> `user.tenantId` (null path), both files | **rc 2, 2x TS18048** | ts-jest compile failures in every suite importing the routes | 48 FAIL | tsc first, then every suite |
| `user.organizationId` read BEFORE the guard, both files | **rc 2, 2x TS18048** | same | 48 FAIL | tsc first |
| gdpr.ts connectorContext made always return null (`... \|\| Date.now() > 0`) | 0 | **0 fail (105/1321 green)** | 0 fail | **NOTHING: SURVIVES** |
Raw: evidence/mutants-summary.txt, mut-*-diff/tsc/unit.txt, jest-int-m-*.txt. A first batch of mutant runs was invalidated by my runner (zsh did not word-split a loop variable); those files are quarantined under evidence/_invalid_runner_bug/ and NOT used. Everything in the table is from the clean rerun, except `swap both`, which ran correctly the first time.

## Findings
**Minor 1: gdpr.ts connectorContext has no runtime test at all (pre-existing, not introduced by this PR; it matters because this PR edits it).** No file in `services/originate/src/__tests__` mounts `gdprRouter` `/erasures` (grep for `/erasures` finds none; the always-null mutant survives all 105 unit suites and all 48 integration cells in both modes). The author's cited evidence (7 gdpr files / 87, the three ks695 integration files) exercises `platformOrganizations.ts`'s copy, which is a different function. The gdpr.ts half of the change is therefore protected by `tsc` and by being character-for-character the same expression as the covered half, nothing else. Location: services/originate/src/routes/gdpr.ts:468-479 (callers :521, :552). Minimal fix (a follow-up, not a blocker for a types-only change): one supertest/express cell mounting `gdprRouter` with a connector principal that asserts `tenantId`, `organizationId` and `connectorId` reach the handler and a tenant-less principal gets the refusal.
**Minor 2: the "only two casts" census frame is narrow.** See section 3: 27 non-test `(req as any).user?.tenantId|organizationId` lines (originate 11, security 11, tokenisation 4, shared 1) plus 7 typed re-casts remain, so the "casts hid the reads, deleting the field compiled cleanly" property still holds for them. Not a defect of this PR; the PR body's wording must not be read as "tenantId/organizationId reads off the JWT are now compiler-checked everywhere". Minimal fix: say so in the PR body, or file the sibling census as its own ticket (Wednesday's call).
No Major findings. No runtime value change found; no third file.

## 6. Merge-tree, PR claims, closing keyword, Linear
- `git merge-tree --write-tree gh/develop pr1543` (live tip 29bb4534): rc 0, clean, result tree `8423eb68a6625f5de66fc160243fed260ef6742c` (evidence/merge-tree.txt). CONTROL: a scratch commit on a7cffc8 that edits the very line gdpr.ts:472 merged against the head gives rc 1 with a stage-1/2/3 conflict entry for gdpr.ts (merge-tree-conflict-control.txt), so the instrument can report conflicts.
- Does pull request 1541 touch the two files? No: `git diff --name-only a7cffc8 29bb4534 | grep -c originate` = 0 (10 files: shared policy/security/api-gateway only). Merged tree vs live develop differs in exactly the two files (+4/-6) (`git diff --stat gh/develop 8423eb68`).
- Closing keyword: the commit message says `Refs KS-759` only; no Closes/Fixes/Resolves. The commit's claims match the code: types-only, first cast left, four errors at the stated positions (all reproduced above).
- Linear: I made no Linear or GitHub write of any kind.
- PR BODY: not read. `gh` has no authenticated session here and I did not go looking for credentials. The claims I checked are the ones in the brief and the commit message. (Note the commit trailer says "Co-Authored-By: Claude Opus 5.5" while this brief's attribution is separate; not a finding.)

## 7. NOT tested
- The PR body text on GitHub and its closing-keyword state (unreadable); the PR's required checks and CI state.
- Preflight (13 of 16 legs ran, legs 3, 4, 8 SKIPPED per the author): a skipped leg is not a pass and I did not run any of the 16 legs. `npm run check:openapi` was not run (a types-only change cannot move the spec, but I did not measure it).
- `api-gateway`, `security`, `auth` and the rest of the monorepo's suites on the head; `packages/shared` tests; the other 5 integration files in originate; the front ends.
- A real HTTP request through the live `authenticate()` middleware into either `connectorContext` (the integration cells replace `authenticate` with a header-driven mock and then use the real router/`requireRole`/`withTenant`/RLS).
- The gdpr.ts `/erasures` handlers at runtime at all (no cell exists; Minor 1).
- Production-like tenancy: my MT=true run used one database for both the platform and main roles, with a superuser platform connection, and `secuura_app` with broader grants than production. Only PostgreSQL 15.14 on arm64 macOS and node v24.7.0 were used.
- Whether the 27 other `any` reads are individually safe.
- Anything deployed, anything on the Azure side, and deploy behaviour: I do not recommend deploying; merge only on Wednesday's head-bound GO for `502b164e4f863df4a685315ffa600b2e910ab958`.

## Cleanup
Scratch PostgreSQL stopped (`pg_ctl -m fast stop`, port 55491 no longer listening); no jest/tsc process left. The scratch clone and node_modules copy remain in the scratchpad only.
