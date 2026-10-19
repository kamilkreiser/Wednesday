VERDICT: GO WITH NOTE at head 24a07c497812... (tier 2 delta, round 2 of 2; landing tree 610c3c69c969f8e1571761e502ea9d0ed0e878b4 on develop adb0dfd58fc582f24ab2a7db021a2027544f566c; 0 blockers, 3 notes)

# GATE AL1: PR #1624 (KS-1662) DELTA, Sonnet, tier 2, round 2 of 2

Gated 2026-10-19. Own clone `scratchpad/al1/repo` (APFS copy of aj1's, fetched, detached), scratch PostgreSQL 15 on 127.0.0.1:55451 (TCP only; the migrated aj1 data dir, same migrations). Nothing written under `!CODING`, no GitHub/Linear writes, no push.

## Heads (ls-remote at start and again before this verdict)
- #1624 head `24a07c497812e5dc6b8e88a654b38b492c2e2980`: unchanged. develop MOVED: `a0da739b...` -> `adb0dfd58fc582f24ab2a7db021a2027544f566c` (#1623, KS-1633; 8 files: certifications.ts, certificationRepo.ts, db.ts and 5 tests).
- `merge-tree --write-tree adb0dfd58 24a07c497`: rc 0, tree **610c3c69c969f8e1571761e502ea9d0ed0e878b4** = the author's re-predicted tree (checked out as a commit: `HEAD^{tree}` equals it). The READY's 6deb4a04f454 is the tree on the OLD develop (reproduced, rc 0), stale now.
- Three-dot on the new develop: exactly 3 files (documents.ts, ks1402-invited-stub-holder test, ks1662 test), +440/-20. File overlap with #1623: 0 (control: the PR list intersected with itself = 3, so the comm instrument discriminates).

## Q1 B1 CLOSED
Located by content at the head: exactly four `AND (tenant_id IS NULL OR tenant_id = ${tenantId}::uuid)` lines, all inside `FROM users` reads: :1609 (resolveByHash), :1715 (id re-read), :1944 (email local read), :2050 (id-path existence). The planter asserts the predicate is on the target line, plants `AND true`, tsc rc 0 each, restored after each (0 modified).

| Mutant | ks1662 (owner), BOTH modes | ks1402-invited-stub-holder (secuura_app), both modes |
|---|---|---|
| :1609 resolveByHash | 1 failed / 5 passed: MINT hash re-resolve | 16/16 |
| :1715 id re-read | 1 failed / 5 passed: MINT id re-read | 16/16 |
| :1944 email local read | 2 failed / 4 passed: EMAIL PATH + MINT hash re-resolve (as the author said) | 16/16 |
| :2050 id path | 1 failed / 5 passed: ID PATH | 16/16 |

Unmutated ks1662 6/6 both modes. Each predicate reds its named cell; the ks1402 suite stays green under all four (it cannot see them, as in round 1).

## Q2 comment-only: HOLDS
documents.ts three-dot on the new develop: 72 +/- lines, 72 match `^[+-]\s*//`, 0 non-comment (control: a planted `+  const x = 1;` gives 1). Independent: TypeScript transpile with removeComments is byte-identical for develop and head (`c1744061d948` both); with comments kept they differ (`ce3e33b9bebf` vs `b54b5733234f`). Round1->round2 documents.ts delta also 0 non-comment lines.

## Q3 are the new comments TRUE
- deploy.sh:679-702 admin fallback: TRUE. The file is `deployment/azure/deploy.sh`; the secret read is `az keyvault secret show ... 2>/dev/null || echo ""` (so the `|| echo ""` is real) and the `if [ -n "$APP_DB_PASSWORD" ] ... else DATABASE_URL="$ADMIN_DATABASE_URL"` fallback quotes match. services.bicep :50-54 and :265-268 say what the comment says.
- RLS_ROLE_CUTOVER.md: exists at `deployment/azure/RLS_ROLE_CUTOVER.md` (cited as a bare filename, fine), Stage 2 dev and Stage 3 demo/prod marked DONE 2026-05-22. docker-compose.yml:581 exact.
- platform_admin branch unreachable from this route: CONCLUSION HOLDS (documents.ts has no import of or call into anything that enters platform scope; `platformScope` is set only by `runWithPlatformScope` at tenant-guc.ts:103; `tenantGucContext` sets only `{ tenantId }` at :114-131; tenant-guc.ts:102 is the function line). **But the supporting statement "originate's only call sites are in routes/adminConfig.ts" is FALSE: see N1.**
- Two-halves tripwire statement: TRUE as stated (mint half = ks843 F-2; admission half UNCOVERED). The KS-1653 note itself is not verifiable from here (no Linear).

## Q4 AJ1 notes
- ks1402 test :284 now cites `userRepo.ts:771`: real line 771 is `id: uuidv4(),` (read). :732 is `return user;` (read), :692-698 the upsert. Closed.
- RACE comment: "`toHaveLength(1)` can only ever catch ZERO rows" is TRUE (unique conflict key on email_lookup_hash, as I measured in round 1); the phantom-id read is the load-bearing line. Closed.
- "17 rows": gone from documents.ts, ks1662 and ks1402 (grep -i, control: the same grep hits other numbers elsewhere). Closed.

## Q5 delta discipline (24ab138d -> 24a07c497, one commit, 3 files +111/-26)
documents.ts: comment-only (replacement of the over-claim with the which-role block, the platform_admin paragraph, the two-halves tripwire). ks1402 test: the :768->:771 citation and the RACE comment rewrite (no code). ks1662 test: header corrections; `PHANTOM` const and `stubMode` ('notFound'|'foreignId'|'phantom', reset in the per-test cleanup); two stub branches; two new cells (MINT id re-read, MINT hash re-resolve). Every hunk accounted for; no production code touched.

## Q6 landing (tree 610c3c69c969, commit made in scratch from merge-tree)
- originate unit suite: **126 suites, 1510/1510**, rc 0 (grew from 125/1504 because #1623 added tests).
- ks1662 **6/6** MT=false and MT=true; ks1402-invited-stub-holder **16/16** both; sibling ks1402-transfer-custody-connector-actor **6/6** both.
- type-check including test files (`tsc --noEmit`, tsconfig `src/**/*`): rc 0; control: a planted `const __ctl: number = "x"` in ks1662 gives rc 2.
- **db.ts (#1623 `withTenant` optional `opts.pool`) does NOT affect either suite**, measured: omitted pool = `tenantManager.getDefaultPool()` exactly as before; the only caller passing a pool is certificationRepo.ts:161 (`pool ? { pool } : undefined`); documents.ts's two `withTenant` calls (:2087, :2525) and the three test call sites (ks1662 :259/:266, ks1402 :376) pass two args. All six suite runs above are on the post-#1623 tree and green.

## BLOCKERS
None.

## NOTES
- **N1. False enumeration in two new comments.** `documents.ts:1919-1920` and the ks1662 header (`... only runWithPlatformScope call sites are in routes/adminConfig.ts`) say originate's only call sites are in adminConfig.ts. Measured: `services/gdprService.ts` also calls it (:419, :542, :933, :1332, :1512) besides adminConfig.ts (~20 sites); the control shows the grep sees the gateway's sites too. The conclusion (unreachable from the documents route) is unaffected: documents.ts has no import of gdprService or adminConfig (the other gdprService hits in orgId.ts/provenance.ts are comments), and the scope is an AsyncLocalStorage run bounded to the wrapped call. A comment-only fix ("adminConfig.ts and gdprService.ts, neither reachable from this route"); not worth a round at tier 2, but it is a statement labelled "measured" that is wrong as written.
- **N2. Migration citation reads wrongly.** `documents.ts:1921` "Migration 039_rls_fail_closed.sql:156-157 is what changed it" now follows the platform_admin paragraph; lines 156-157 are the `users_auth_lookup` DROP/CREATE POLICY (the FORCE RLS and fail-closed `tenant_isolation` are at :111-117). Same line cited in ks1662 header :27 ("created by"). The sentence was carried from round 1; it now sits where it implies 039 introduced the platform_admin branch. Also the ks1662 header still says "So RLS is the enforcement in the deployed shape, and the predicate is the belt-and-braces" a few lines above its own corrected "owner connection IS reachable" paragraph: true for cut-over environments only, consistent with the corrected block but unqualified.
- **N3. Unverifiable here:** KS-1653 (admission half "noted") and KS-1665 exist/read back as the author states; which role demo and kintsugi actually run as is unmeasured (the author says so). The PR body was not read (no GitHub).

## NOT RUN
- Auth's unit and integration suites, api-gateway ks843 (round 1 measured those under the mutants; nothing in this delta touches them).
- The full originate integration suite (5 pre-existing failing suites in the author's account) and ESLint.
- The mutants under the post-#1623 landing tree (run on the PR head; the landing tree's 3 suites were run unmutated, both modes).
- Any deployed environment; PR body; Linear.

## Harness
Scratch PG reused the aj1 data dir (migrations 050-052 applied; the #1623 diff adds no migration), `secuura_app` password reset for this port. Untracked `tsconfig.ai1tests.json`/`tsconfig.aj1tests.json` in the clone are scratch artefacts, not part of the PR.
sha256: 5c3b2361cae1627543c22545d1da9bb5ef7e765e3b217b5aa6601f9a82247557
