VERDICT: GO WITH NOTE at head c2a409ed8d0baa29a9a6bedb92dd3f8a4b9bf323 (tier 1, round 1 of 2; landing tree 3ea28cd71fa5b1579701e754d7e04fabfc6dd0cf on develop 4abff9b1a4765982ea504784c9df69a8ddd52210; 0 blockers, 4 notes)

## BLUF

Kam's ruling (a) is built as Wednesday read it, and it fails closed. Over real HTTP, with the real routers and the real errorHandler, in all 3 DB modes (db / every query throws / DB unavailable):
- An ORG_ADMIN and a SYSTEM_ADMIN of the row's tenant read every owner-less row of that tenant. I tested 6 such rows: rows in the table, rows created by POST, memory-only rows, and rows after a boot load.
- 34 near-miss principals are refused on all 6 rows, in all 3 modes. Each refusal matches the unknown-id response in status, body bytes and headers.
- A pre-054 row (tenant unknown) is refused to everyone.

The row's tenant comes only from `created_by_tenant_id`, or from the memory owner map, which is stamped from the creator's signed token. It never comes from the reader. A body, header or query that tries to supply it is ignored.

BH1's own 16-caller probe, re-run unchanged (sha256 8e188a7d…), is 64/64 at the landing. All three of BH1 NOTE 1's survivors now red the author's own cells, and each on a cell about it: BM1 on X1/X2, BM2 on Q1, BM4 on W1/W2. 12 of my 13 mutants are red in the author's 118 cells. The other 2 of my own (role set widened, tenant prefix) are green there and red only in my probe (NOTE 2).

The suite at the real landing is 278/278. 0 develop cells vanished other than the 18 N1-N6 retitles, whose bodies are unchanged. tsc, lint and the ratchet are rc 0, and each one's positive control fails. **Develop has moved** since the claim (NOTE 1), so the landing tree is 3ea28cd7…, not eadbaa1…

## Findings

### Blockers
None.

### Notes
- **NOTE 1: develop moved, so the landing tree changed.** Live develop is 4abff9b1a476 (#1647, KS-1677, merged after the claim). The brief's develop was c66b834ed451. `merge-tree --write-tree` on live develop gives **3ea28cd71fa5…**, rc 0, clean. The author's eadbaa1bbc60… reproduces exactly on the OLD develop c66b834e (control). The landing differs from live develop in exactly the 2 PR files. #1647 touches no vc-issuer file, but it does touch `packages/shared/src/crypto/encryptedField.ts`. So everything below was run at the real landing 3ea28cd7: shared rebuilt, then suite, tsc, lint and ratchet. Any GO recipe must name the new landing tree.
- **NOTE 2: the author's cells cannot see two predicate regressions.** Each mutant type-checks alone (tsc rc 0). Each is green in all 118 KS-1116 cells and in ks1020, and red in my probe:
  - JM8: the role set is widened to `TENANT_ADMIN` / `SUPER_ADMIN`. The brief names TENANT_ADMIN as must-refuse, but the author's ruling-(a) refusal list has OWNER and lower-case `org_admin`, and no TENANT_ADMIN or SUPER_ADMIN row.
  - JM11: the tenant is matched as a prefix (`rowTenantId.startsWith(claim)`).

  The product code is correct on both. These are regression-guard gaps, not defects. Suggested additions: TENANT_ADMIN and SUPER_ADMIN of the row's tenant -> 404, and an admin whose tenant is a strict prefix of the row's tenant -> 404.
- **NOTE 3: no auth-minted token can create a row that ruling (a) admits.** The (a) branch needs a row with no userId but a known tenant. `services/auth/src/services/jwt.ts` signs `userId` in every payload it mints: :194 access, :220 refresh, :289 connector (`connector:${…}`). So such a row arises only from a token minted elsewhere, or from an empty `user.id`. The author measured that (a) reaches 0 of the existing rows. On top of that, it reaches practically no future row through auth. Wednesday should tell Kam this per the brief's "if his option ends up reaching no row" line. I checked only auth's jwt.ts; I did not survey other minters.
- **NOTE 4: one of my mutants is equivalent (disclosure).** BM4c applies `String()` coercion to the userId only. It is green everywhere, and that is correct, because no input can expose it: `mayRead` returns false on `claim(user?.userId) === null` before it reaches the compare, so `String()` only ever sees a string. It is not a gap. BH1's BM4 shape, and the tenant-only BM4b, both red W1/W2.

On the author's two open choices: case-sensitive roles, and no SUPER_ADMIN. Both are stricter than the ruling's words and fail closed. I found nothing against either, so they are left for Wednesday or Kam to rule on.

## FOUND / TESTED / HOW

| Q | Result | How |
|---|---|---|
| Heads | head c2a409ed8d0b (branch = refs/pull/1649/head), unmoved at 21:47Z and 21:56Z. Develop 4abff9b1, unmoved across the gate. head^{tree} = eadbaa1b. | `ls-remote` via the cache clone. `git clone --shared` into my scratch. Fetched the BRANCH ref with the cache's own deploy-key sshCommand. |
| 1 Predicate | **ADMITTED (200, correct id):** ORG_ADMIN T1 and SYSTEM_ADMIN T1, on 6 owner-less T1 rows × 3 modes. **REFUSED (404 = unknown id in status, body and headers), 34 principals × 6 rows × 3 modes:** admins of T2; admins with no tenant / null / '' / 1 / [T1] / {toString} / {tenantId} / upper-case / padded / prefix tenant; OWNER, TENANT_ADMIN, SUPER_ADMIN, ADMIN, ISSUER, VERIFIER, USER of T1; role `org_admin` / `system_admin` / padded / ['ORG_ADMIN'] / {toString} / '' / absent / `roles` array only; admin with no userId / '' / number; no principal. **Tenant unknown:** pre-054 presentation and credential refused to T1 admins and to tenant-less admins; a T2 owner-less row refused to T1 admins (U ×3). **Caller-supplied tenant:** a T2 admin sending `x-tenant-id: T1`, `x-organization-id: T1` and `?tenantId=T1&created_by_tenant_id=T1` -> 404 on all 6 rows (H ×3). On a POST by a T1 token with no userId and a body smuggling T2, both table rows carry `[null, T1]` (S0). **POSITIVE CONTROLS:** A ×3 and U2 ×3 (a T2 admin reads the T2 row) are green at the landing, so every refusal is about the principal and not about a missing row. On DEVELOP (option C) product, the same probe is red on exactly A ×3 and U2 ×3 ("expected 404 to be 200"), and every refusal stays green. | `src/__tests__/bj1-probe.test.ts` in my clone, 116 cells, built on BH1's harness (express `listen(0)`, a fake SQL table that projects only the SELECTed columns). Develop arm in a worktree of my clone. |
| How the row's tenant is decided | `mayRead` -> `ownerlessRowReadable(req, owner?.tenantId ?? null)`. `owner` comes from `ownerFromRow` (the DB column, or the boot load), or from the memory Map stamped by `ownerOf(req)` at create. A Map miss gives OWNERLESS, which means null. The reader's request is used only for its own role and tenant claims. `req.user` is the verified JWT payload only (shared `authenticate()` :110/:121), and no vc-issuer middleware rewrites it (0 hits for `req.user =` in vc-issuer src). | read: ownership.ts, credentialRepo.ts, routes/presentations.ts, routes/credentials.ts, shared middleware/index.ts |
| 2 Owned path | BH1's probe, copied byte-for-byte (sha256 8e188a7d… = BH1's file), at the landing: **64/64**. That covers 16 foreign callers × 3 modes × 3 rows -> 404 identical to unknown, Alice reads (A0 ×3), X1 body-smuggle, R1 owner never transfers, V1 tokenless verify true then revoked false, and Q1. Q1: after revoke with the DB down, Alice is 404, which is KS-1684 and unchanged. JM12 (a tenant admin also reads OWNED rows of their tenant) is red in BH1's probe (6) and in the author's C1 D1 E1 M1 P1. | `bj1-bh1copy.test.ts` |
| 3 NOTE 1 survivors | BM1 (owner read from the body): red on **X1, X2** only. BM2 (Map miss accepted, `?? OWNERLESS` dropped): red on **Q1** only. BM4 (BH1's String shape) and BM4b (tenant only): red on **W1 ×2, W2 ×2** only. BM4c (userId only): equivalent, NOTE 4. All tsc rc 0. | `mutants_bh1.py`, run over the author's file + ks1020 |
| 4 My mutants | Each tsc rc 0 alone; the type-error **CONTROL** JM0 gives tsc rc 2. Author cells that red on each: JM1 role only: A2 A3 A5 A6 A7 A9 N1-N6. JM2b tenant only: A2 A5 A7 A9. JM3 role OR tenant: A2 A3 A5 A6 A7 A9 N1-N6. JM4 fall open when the tenant is unknown: A3 N1-N6. JM5 loose `==` on the raw claim: A2 A5 A7 A9. JM6 unknown tenant borrowed from the caller: N1-N6. JM7 no-userId guard moved after the branch: A2 A5 A7 A9. JM9 case-fold + trim: A2 A5 A7 A9. JM10 null matches null: A3. JM12: C1 D1 E1 M1 P1. **JM8 widened role set: 0 author cells. JM11 prefix tenant: 0 author cells** (NOTE 2). All 13 are red in my probe or BH1's. Restored from an in-memory snapshot; ownership.ts sha256 895064d3… = head's blob; clone `git status` empty. | `mutants.py`, `mutants_jm2.py` (JM2 re-cut: the first cut failed tsc on an unused const and was discarded) |
| 5 Landing | merge-tree on live develop = **3ea28cd7**, rc 0. On the old develop c66b834e = eadbaa1b (the author's tree, control). Landing vs develop: exactly the 2 PR files. Suite at the landing: **278/278, 18 files**, of which 118 are in the KS-1116 file. Develop: 233/233. Missing by full name: 18, all of them N1-N6 "interim option C" titles. The diff's removed lines are those titles and the old header comment only; 0 removed `expect(`. Added: 63 (18 retitles + 45 new), all in the KS-1116 file. 0 develop cells failing at the landing. tsc `--noEmit` rc 0. eslint rc 0 (**CONTROL:** no-debugger and no-var give rc 1). `check.cjs services/vc-issuer` rc 0, 18 test files, 0 errors (**CONTROL:** an injected test TS2322 gives rc 1, "1 new"). Public tokenless verify: BH1 V1 green at the landing; the PR touches no verify or revocation file. | vitest JSON reporters on both arms; probe and control files parked (mv) before tsc, lint and ratchet |

## NOT RUN
- No live HTTP against the real gateway or deployed service. The real `jwtAuthenticate` was not in the chain: a stand-in attaches a verified payload, as in BH1. The PR does not change it.
- No Docker, no box, no Schemathesis, Akto, Playwright or k6. No real-PostgreSQL run this round: the PR adds no SQL and no migration, and BH1 covered 054 on PG 18.3.
- The live PR body, KS-1684/1685/1686 and the Kam card were not read (no GitHub or Linear access used).
- The token minter survey covers auth `jwt.ts` only (NOTE 3).
- The author's red-proof logs and tools were not re-run; my own mutants stand in for them.

## Wall-clock
21:47Z to 22:00Z 2026-10-19 (08:47 to 09:00 AEDT 2026-10-20). Artefacts: /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/19de126d-c0be-44ad-bebc-29a8293479e1/scratchpad/gate_bj1/ (parked/bj1-probe.test.ts.parked, land_suite.json, dev_suite.json, bj1_dev.json, mutants.log, mutants_jm2.log, mutants_bh1.log, mutants_summary_run1.json, lint/ratchet/tsc logs). BH1's scratch was read only.
86d54842f7e907cbcdc26e94729be4cb30a66770c460bf5f88e4ed2f31ab43aa
