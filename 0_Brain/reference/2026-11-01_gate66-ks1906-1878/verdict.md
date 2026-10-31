## QA GATE 66, TIER 1, ROUND 1: KS-1906 #1878 (owner-less credentials, option (A))
(Opus, Sun 1 Nov 2026, commissioned by Wednesday. Findings only: nothing was fixed, pushed, commented, approved or merged, and nothing was written to GitHub or Linear. Client scope: Secuura only. Evidence is in `evidence/`, scripts in `scripts/`.)

> **MERGE HOLD, independent of this verdict: #1878 must NOT merge before Kam rules card `secuura-ks1906-ownerless-credentials-connectors-1101`.** It builds option (A), the card's default: no connector is admitted. A GO here is a statement about head `2cad07f76492` under option (A) only. If Kam rules for connectors, the head changes and this verdict expires with it.

**BLUF: GO WITH NOTES** (for option (A), subject to the hold above). For credentials with no owner, the authorisation rule is exactly what the scope sentence says. I measured it through the real routes on **real Postgres 15** with an oracle I wrote myself, not taken from the PR: 21 principals × 9 row shapes × {by id, by hash, list, revoke}, on both schema sources. The results:
- Admitted: `isPlatformRole` (SYSTEM_ADMIN / SUPER_ADMIN, ASCII fold), and only for a row of the caller's own tenant.
- Refused: ORG_ADMIN, connector, anonymous, a different tenant, a caller with no tenant, and a row with no tenant.
- The SQL filter and the JS backstop never disagreed.

All 7 credential call sites that used `mayRead` now use `mayReadCredential`, and presentations correctly keep `mayRead`. The census is repo-wide and nothing outside vc-issuer imports the module. The author's red-first figures reproduce exactly: 24/224 and 11 existing cells. 6 reconstructed author mutants and 9 of my own were all killed (3 of mine only by my real-PG probe). Merge is clean on the brief's develop and on develop as it is now.

Nothing blocks the merge. One MINOR is for Kam, because it is a consequence of the ruling as built:
- **G66-F1 (MINOR, for Kam).** The people who actually log in as platform administrators (the `platform_admins` table) get a token with **no tenant**. So they can never read or revoke an owner-less credential.
- No code path signs an upper-case `SUPER_ADMIN` that carries a tenant. The effective audience is therefore **a users-table SYSTEM_ADMIN of the row's tenant**, and nobody else.
- ORG_ADMIN lost access, so a tenant with no SYSTEM_ADMIN has nobody who can revoke its owner-less credentials through the API.

- PR https://github.com/Secuura/Distributed_Secuura/pull/1878 · ticket KS-1906 · author Seat E 22nd · scope: option (A) of card `secuura-ks1906-ownerless-credentials-connectors-1101`
- **Head at START** (2026-10-31T19:10:55Z = 06:10 AEDT, `git ls-remote`): `refs/pull/1878/head` = `2cad07f764922a68a70728978a1edb9b3a322f21`, one commit on `eb9651392f49`. **develop = `dd583b4f7495193e7f846e02b41e2a462e687774`**, already one commit past the brief's `0fab207f` (KS-1579, 5 files, `evidence/lsremote_start.txt`).
- **MID** (Spark runner fetch, ~19:28Z): develop = `9bc1cf3b538b` (`evidence/spark/spark_gate.log`).
- **Head at END** (2026-10-31T19:29:44Z): `refs/pull/1878/head` = `2cad07f764922a68a70728978a1edb9b3a322f21`, **unchanged**. develop = **`9bc1cf3b538bf3e2842e4b6801a611a73d93ba4a`**: 3 more squashes since start (#1879 KS-1858 social adapters, #1881 PR template, #1880 DEVELOPMENT.md). None of them is the PR's files or anything the PR reads (`evidence/lsremote_end.txt`, `evidence/develop_moved_end.txt`).
- Clone: `0_Brain/reference/2026-11-01_gate66-ks1906-1878/repo`, created with `--shared --no-checkout` from gate 65's clone. It has gate 65's `core.sshCommand` (the Blockchain deploy key), is a blob:none promisor, and has push URL `no_push_qa_gate`. `rev-parse --show-toplevel` equalled the clone before every fetch and write. The clone was left detached at the head with `git status --porcelain` empty: every swap and mutant was restored and checked by sha256, and the probe copies were moved to `tmp/_quarantine_2026-11-01/`, not deleted.
- Host: Apple Silicon Mac, **Node v26.8.1 (not LTS; Node 24 UNMEASURED)**, vitest 4.1.12, tsc from the workspace. Postgres 15.19 runs in my own container `gate66-pg` (ID in `evidence/pg_container.id`), bound to 127.0.0.1 only. It is now **stopped, not removed**. No other container was touched.
- `npm ci --ignore-scripts` at `Blockchain/Dev`: rc 0. `packages/shared` build: rc 0. Load1 was 3.5-8.3 during the session. Heavy runs were started below 7 under `nice -n 10`, with at most 2 workers (one for the PG probe).

## VERDICT: GO WITH NOTES (option (A) only; held for Kam's connectors ruling)
Conditions:
- (a) The merge hold above.
- (b) G66-F1 goes to Kam **with** the connectors card. It is the same question, "who is the audience for an owner-less credential?", and his answer may change the tenant binding as well as the connector clause.
- (c) If the head is rebased onto current develop, nothing in this verdict depends on develop's moves. The 3 squashes since start touch no file the PR reads.

## FINDINGS

**G66-F1 · MINOR · for Kam (design consequence, not a code defect) · READ ONLY for the token shapes, MEASURED AT RUNTIME for the predicate on them.** Under option (A) as built, the owner-less audience in practice is a users-table SYSTEM_ADMIN of the row's tenant, nobody else.
- **Mechanism.**
  1. A platform-portal login (`platform_admins` table) mints a token from a synthetic user with `tenantId: undefined` (`services/auth/src/routes/auth.ts:376-390`). Its role is `platformAdmin.role` verbatim (`:453`, and `:477` on the second mint), which is one of `super_admin`, `platform_admin` or `platform_viewer` (`docker/init-platform/01-platform-schema.sql:79-80`).
  2. `ownerlessCredentialReadable` requires `claim(user.tenantId) === rowTenantId` (`ownership.ts:154`). A tenant-less token therefore reads nothing that has no owner.
  3. Users-table roles go through `mapDbRole` (`userRepo.ts:257-274`). It maps `super_admin` to **SYSTEM_ADMIN** and has no `SUPER_ADMIN` key at all, so no users-table token carries upper-case `SUPER_ADMIN`. Every users row has a tenant (`userRepo.ts:685`, RLS fail-closed).
  4. **So the 14 SUPER_ADMIN/super_admin admission cells model a token shape no issuer in the repo produces.** The only reachable admitted principal is a users-table SYSTEM_ADMIN whose `tenant_id` is the row's tenant.
- **Measured** (real PG, `evidence/realpg_head_g66boot.jsonl`, row "SUPER_ADMIN no tenant (platform-admin login shape)", role `super_admin`, no tenant): it gets 404 on all 9 rows by id and by hash, the list is `[]` with total 0, and every revoke gives 404 and leaves the DB row unchanged. `platform_admin` and `platform_viewer` of T1 are also refused, because `isPlatformRole` excludes them, even though the gateway's `SUPER_ADMIN_ROLES` includes `platform_admin` (`api-gateway/src/middleware/auth.ts:591`).
- **Why it matters.** Kam's quoted words are "platform administrators only", with no tenant clause. The tenant binding comes from Wednesday's ANSWER of 16:23:55Z (as the code comment says). Taken together, the ruling's literal audience (the platform-portal administrators) is structurally excluded. ORG_ADMIN lost access too. So in a tenant with no users-table SYSTEM_ADMIN, nobody can revoke an owner-less credential through the API. That is fail-closed, so there is no confidentiality or integrity risk. **Blast radius is probably tiny:** migration 054's header measured 0 pre-054 credentials on demo and on kintsugi, and an owner-less row *with* a tenant needs a creating token that has a tenant but no userId. I did not count such rows on any environment (UNMEASURED).
- **The PR is honest about it.** The fragments say "UNMEASURED whether any platform administrator user carries a tenant". This finding closes that from code: the platform-portal population never does, and the users-table population always does but is never `SUPER_ADMIN`.
- **Fix shape:** none needed for (A). Kam may want to rule the tenant clause for tenant-less platform administrators alongside the connectors card. A docs-only tweak would be: "in practice: a SYSTEM_ADMIN user of the row's tenant; platform-portal admins carry no tenant and read none".

**G66-F2 · MINOR · test strength · MEASURED.** Three of my mutants on the predicate survive all 521 PR cells. My real-PG probe killed each one (`evidence/own_mutants.json`).
- **GM6:** the tenant compare case-folded (`toLowerCase()` on both sides). 0 PR cells red, 12 probe cells red: a SUPER_ADMIN of `G66-TENANT-1` reads `g66-tenant-1`'s owner-less row by id. No PR cell has a tenant that differs from the row's only in case.
- **GM7:** `platform_admin` admitted, which is the gateway's own super-admin set. 0 PR cells, 2 probe cells. No PR cell pins `platform_admin` or `platform_viewer` as refused.
- **GM9:** the role trimmed before `isPlatformRole`. 0 PR cells, 2 probe cells. There is no whitespace-padded role near miss.
- **Realism.** Tenant IDs are stored canonically, and `platform_admin` tokens are tenant-less (G66-F1), so none of the three is reachable through today's issuers. They are cheap near misses that would pin the predicate against a future "normalisation" edit.
- **Regression tests the owner should add to `REFUSED_T1`:** `{...SUPER_ADMIN, tenantId: T1.toUpperCase()}`, `{...SUPER_ADMIN, role: ' SUPER_ADMIN'}`, `{...SUPER_ADMIN, role: 'platform_admin'}`.

**G66-F3 · NOTE · test architecture · MEASURED.** The PR's "database path" never executes SQL. `ownerFilter` + `pgModel` (ks1906 test `:380-414`) is a JS re-implementation of `READABLE_BY_CALLER` driven by the parameters, and it ignores the SQL text.
- My SQL mutants GM4 (the owner-less branch's `= $2` replaced by `$2 IS NOT NULL`) and GM5 (the owner-less branch's `NULLIF` dropped) **are** each killed. The killer is one cell, ks1683 `S1`, which pins the predicate's exact text (`MEASURED_PREDICATE`). No KS-1906 behaviour cell kills them.
- The text pin is adequate as a tripwire, and my real-PG run gives the semantics (below), so this is not a defect. What it means: the claim "the database path: the same audience, in the SQL owner filter" is a claim about a model, and only the text pin ties that model to the SQL.
- GM5 is a real under-serve: on Postgres it drops the `''`-user rows E6 from a platform admin's list while the JS backstop would admit them. GM4 is an over-count: total 2 → 3, and the backstop warns.

**G66-F4 · NOTE · docs accuracy (KS-1851 cheat fragment) · READ ONLY.** The edited sentence still says the revoke "is now bound by `mayRead`". At the head it is `mayReadCredential` (`credentials.ts:305`). It also still says "Anyone else, platform and tenant administrators included, gets the same 404", which now sits beside a parenthetical admitting platform administrators of the row's tenant. That is historically accurate for #1869 and readable with the "superseded" clause, but slightly self-contradictory. Optional reword: "(superseded by KS 1906: credentials use `mayReadCredential`; a platform administrator of its tenant)".

**G66-F5 · NOTE · pre-existing, repo-wide (not this PR's) · READ ONLY.** Which roles count as "platform administrator" differs from place to place:
- `isPlatformRole` (`packages/shared/src/security/keyRevokePolicy.ts:60,140-145`): {SYSTEM_ADMIN, SUPER_ADMIN}, ASCII fold.
- The gateway's `SUPER_ADMIN_ROLES` (`auth.ts:591`): adds `platform_admin`.
- Auth's `PLATFORM_ADMIN_ROLES` (`users.ts:193`) and `OAUTH_PLATFORM_ADMIN_ROLES` (`oauth.ts:1170`): add `admin`.
- `ownership.ts:76-82` (presentations): exact case, with a comment saying "auth signs canonical role names". That premise is false for the platform-portal login, which signs lower-case `super_admin`.

The PR picks the shared predicate, which is the right choice and consistent with KS-1850/1845/1591. The note is that the repo's other lists disagree with it.

## Q1. Call-site census (frame: the whole repo at the head and at `eb965139`, `git grep -w`, excluding `*.test.ts`, `*.md` and `*.html`)
**FOUND: complete.** Base non-test callers of `mayRead`/`ownerlessRowReadable` are 8 (`evidence/census_callers.txt`):
- credentialRepo `:256` (the SQL `$3`), `:298` (by-hash backstop), `:308` (by-hash memory), `:378` (list backstop), `:398` (list memory);
- credentials.ts `:277` (GET /:id) and `:302` (revoke);
- presentations.ts `:412`.

At the head all 7 credential sites call `mayReadCredential`/`ownerlessCredentialReadable`, and presentations `:412` keeps `mayRead`, as ruled. **`ownership` is imported by exactly three files, all in vc-issuer.** No other service or package imports it. The two other hits for the word "ownership" are UI or NFT strings.

Route census of `credentials.ts`: POST /, GET /, GET /:id, POST /:id/revoke, POST /verify, GET /by-hash/:hash. Every route that reads a stored record goes through the rule. The unbound `getById` is used only by `revocationResolvers.ts:55`, the public verify path, which is unbound by contract and documented.
**TESTED:** the reconstructed author mutants "by-id left on `mayRead`" (15 cells red) and "revoke left on `mayRead`" (8 red) were killed. The census itself is READ ONLY.

## Q2. Role matching
**FOUND: consistent with the repo's shared definition.** Head behaviour, MEASURED on real PG and by PR cells:

| role | result |
|---|---|
| SUPER_ADMIN, super_admin, Super_Admin, system_admin, SYSTEM_ADMIN (row's tenant) | admitted |
| ORG_ADMIN | refused |
| connector, `connector:api-key` | refused |
| TENANT_ADMIN, OWNER | refused |
| array roles | refused |
| ſuper_admin (U+017F), super_admın (U+0131) | refused (ASCII fold only) |
| ` SUPER_ADMIN` (leading space) | refused |
| platform_admin, platform_viewer | refused |
| anonymous | refused |

The connector principal is built with literal `role: 'connector'` in both minting sites (`api-gateway/src/middleware/auth.ts:470`, `auth/src/services/jwt.ts:291`), so no connector token can pass `isPlatformRole`.

**SYSTEM_ADMIN re-classification:** this is consistent. `PLATFORM_ROLES = {SYSTEM_ADMIN, SUPER_ADMIN}` is documented as "Roles that may act across tenants" (`keyRevokePolicy.ts:54-60`), and auth itself maps the platform `super_admin` DB role to `SYSTEM_ADMIN` (`userRepo.ts:272`). Its answer is unchanged: SYSTEM_ADMIN T1 is green at base and at head on real PG.

**Case handling:** credentials now fold ASCII while presentations stay exact-case in the same file. Both are deliberate (G66-F5).

## Q3. Tenant binding
**MEASURED AT RUNTIME on real Postgres 15** (`scripts/gate66-realpg.probe.test.ts`; `evidence/realpg_head_{g66boot,g66mig}.jsonl`).
- **Setup:** the real credentials router. `../db` is replaced by a real `pg` Pool connected as a non-superuser `vcapp` role (SELECT/INSERT/UPDATE, plus DELETE for the fixture only). The schema comes from **both** sources the product deploys: `docker/init/03-service-tables.sql` (g66boot), and `migrations/001` + `054` ALTERs (g66mig). I checked that `deployment/azure/migrate/init.sql` has the same 5 columns. The three sources agree (`evidence/pg_schema.log`).
- **Fixture:** 9 rows: O1(null,T1), A2(alice,T1), L3(null,null), O4(null,T2), E5('',''), E6('',T1), E7(null,''), N8(x,null), U9(null,UPPER(T1)).
- **Matrix:** 21 principals. Each cell asserts by-id and by-hash status for all 9 rows, the list ids and `total`, revoke status plus a DB read-back of `credentialStatus.revoked` for all 9 rows, and zero SQL/JS "refuses" warnings.
- **FAIL condition:** any disagreement with the independent `SPEC` oracle in the probe.
- **Result:** 43/43 on both schemas.
  - SUPER_ADMIN of T2 reads only O4.
  - SUPER_ADMIN of `UPPER(T1)` reads only U9. The tenant compare is case-sensitive on both paths.
  - Trailing-space tenant: nothing.
  - Tenant `''`: nothing.
  - **Tenant-less SUPER_ADMIN: nothing owner-less.** That answers the author's UNMEASURED about behaviour. Whether real admins carry a tenant is answered from code in G66-F1.
  - Platform admins of T1 read O1 **and E6** (the `''` user is treated as "no owner" in SQL and in JS alike), with total 2.
- **Control** (base product code swapped in, sha256 restored): **14/43 red on each schema**, exactly the cells the ruling changes: ORG_ADMIN, the platform-admin spellings, and SUPER_ADMIN of T2 or UPPER(T1). SYSTEM_ADMIN T1 is green at base, as expected (`evidence/realpg_summary_base.json`).

## Q4. Red-first, the author's mutants, my mutants
- **Red-first (MEASURED; `scripts/run.py base`, `evidence/red_at_base.txt`):** the three product files were swapped to `eb965139` bytes and restored by sha256. **35 red of 521:**
  - ks1906: **24/224**, exactly the designed set: SUPER_ADMIN and super_admin × M1, M5, M7, V1, D1, D3, D7 (14); ORG_ADMIN × M2, M6, M8, V2, D2, D4, D8 (7); plus D5, M9, P3.
  - ks1116: A7, A8, A9.
  - ks1683: L2, L3, H5, D3, E1, G4.
  - ks1851: V8, V8e.
  - That is **11** existing cells, every name matching the mail. Head: **521/521**. The whole vc-issuer suite at the head is **23 files, 689/689** (`evidence/vitest_vc_full_head.log`), matching the author.
- **The author's 17 mutants:** their script was not found (`/tmp/e22` has no KS-1906 mutant artefact by name), so **their run is UNVERIFIED as stated**. I reconstructed 6 of their named mutants (`scripts/author_mutants.py`, `evidence/author_mutant_sample.json`), all killed:

| reconstructed mutant | cells red (of 521) |
|---|---|
| connector admitted | 17 (author: 15 on the new file) |
| ORG_ADMIN re-admitted | 14 |
| full Unicode fold | 14 |
| tenant compare dropped | 43 |
| by-id left on `mayRead` | 15 |
| revoke left on `mayRead` | 8 |

- **My own 9 (`scripts/mutants.py`, `evidence/own_mutants.json`).** Every edit asserted a unique anchor, that it landed, and an sha256 restore:

| # | mutant | PR cells red | real-PG probe red |
|---|---|---|---|
| GM1 | null-tenant guard dropped (tenant-less admin reads pre-054 rows) | 8 | 6 |
| GM2 | SQL `$3` forced true (backstop hides it, total over-claims) | 26 | 7 |
| GM3 | userId gate dropped in `mayReadCredential` | 5 | 2 |
| GM4 | SQL owner-less branch `= $2` → `$2 IS NOT NULL` | 1 (S1 text pin only) | 8 |
| GM5 | SQL owner-less branch `NULLIF` dropped | 1 (S1 text pin only) | 5 |
| GM6 | JS tenant compare case-folded | **0** | 12 |
| GM7 | `platform_admin` admitted | **0** | 2 |
| GM8 | owned row: tenant ignored | 18 | 0 (my probe has no same-user/other-tenant principal) |
| GM9 | role trimmed | **0** | 2 |

**9/9 killed. 6/9 are killed by the PR's cells.** Two of those six, GM4 and GM5, are killed only by a text pin (G66-F3). The remaining three were killed only by my real-PG probe (G66-F2).

## Q5. The docs, sentence by sentence (READ ONLY against the head)
- **`ROLES-AND-AUTHORIZATION-INVENTORY.md` vc-issuer paragraph:**
  - "bound by the same rule since KS-1851 (#1869, `7a9587ef9`, 2026-10-31)": TRUE. `7a9587ef` is "Refs KS-1851: credential revoke is bound…" and is an ancestor of `eb965139`.
  - "a caller may revoke exactly the credentials they may read": TRUE (the same predicate, `credentials.ts:279`/`:305`).
  - `isPlatformRole`: SYSTEM_ADMIN or SUPER_ADMIN: TRUE (the ASCII fold is not mentioned).
  - "only when the token's tenant equals the row's `created_by_tenant_id`": TRUE (measured).
  - "`vc_credentials_store` has no row-level security": TRUE. `git grep` finds no POLICY or RLS on `vc_*_store` in `migrations/` or `docker/`. Control: the same grep finds `documents` RLS in 011.
  - "No connector is admitted": TRUE.
  - "Presentations keep the tenant-administrator clause": TRUE (`presentations.ts:412`, cells P1/P2).
  - "Not bound: the public verify path's revocation lookup": TRUE (`revocationResolvers.ts:55`).
  - The KS-1807 UNDECIDED line is kept, with a dated code-fact note. That is accurate.
- **KS-1851 fragments (cheat and flow):** the added clauses are true. G66-F4 covers the residual "`mayRead`" and "platform administrators included" wording in the cheat fragment.
- **KS-1906 fragments (new):**
  - "the list's SQL filter, whose text is unchanged; only its third parameter now comes from the new rule": TRUE. The non-comment diff of `credentialRepo.ts` is the import, `readerParams` and the 5 call renames; `READABLE_BY_CALLER` lines 245-249 are byte-unchanged.
  - "ks1683's admitted table gained a SUPER_ADMIN while a connector joined its refused table": TRUE.
  - "V8f, V8g, V9": all present.
  - "migration 054's header measured 0 on demo and 0 on kintsugi": TRUE for credentials (`054:26-27`; demo held 1 *presentation*).
  - Figures 24/224, 11, 689/689: TRUE (re-measured). 17/17: UNVERIFIED (see Q4).
  - "a credential a connector creates is stamped with its userId, so it is owned": TRUE. POST / stores `ownerOf(req)`, and the connector userId is `connector:<id>` (non-empty).
  - The quoted Kam text is the same in all four places.

## Q6. Merge, develop moves, tsc
- **`merge-tree --write-tree`** (`evidence/merge_tree.txt`, `merge_tree_end.txt`):

| develop | rc | tree | differs from develop in |
|---|---|---|---|
| `0fab207f` (brief) | 0 | `1ecd0c17a450…` (= author's figure) | exactly the 12 PR files |
| `dd583b4f` (start) | 0 | `d33935264fcf…` | exactly the 12 PR files |
| `9bc1cf3b` (end) | 0 | `ffb4a5d56dd5…` | 12 files |

- **Develop's moves since `eb965139`:** 42 files to `dd583b4f` (37 to `0fab207f`, as the author says), plus 15 more files to `9bc1cf3b`.
  - **Overlap with the PR's 12 paths: 0.** Control: one known moved file matched itself, 1.
  - The moves touch nothing under `services/vc-issuer`, `packages/shared`, any `package.json` or lock file, `api-gateway/src/middleware/auth.ts`, or auth's token or role code. The auth files moved are the KS-1858 social adapters, which handle provider token answers, not role or tenant claims.
  - The api-gateway file is a KS-1534 test. originate's `connectorOrganisationErasure.ts` is not read by vc-issuer.
- **tsc --noEmit:** `tsconfig.json` rc 0 and `tsconfig.test.json` (with tests) rc 0. **Control:** a planted TS2322 in `ownership.ts` and in the ks1906 test each gave rc 2. Both were restored by sha256.
- eslint and the leg-16 ratchet: not re-run (UNMEASURED by me; the author claims 0 and 0 with a planted control).

## COUNTS
- Findings: 0 blocker · 0 major · 2 minor (F1 for Kam, F2 test near misses) · 3 notes (F3 pgModel/text pin, F4 KS-1851 fragment wording, F5 repo-wide role lists)
- PR cells: 521/521 at the head. 35 red at base product code (24 + 11), exactly as claimed. Whole vc-issuer suite: 23 files, 689/689
- Real-PG probe: 43 cells × 2 schemas, all green at the head. At base, 14 red per schema (control)
- Mutants: 9 own, all killed (6 by PR cells, 2 of them via a text pin only). 6 reconstructed author mutants, all killed. The author's own 17: UNVERIFIED

## SPARK SHADOW AND CALIBRATION
`spark_gate.sh` (non-pytest mode, the 4 test files, `--node-modules` = the clone's root `node_modules`, `--work /private/tmp/gate66_spark_*`, base `develop`, `--out evidence/spark/facts`): **rc 0 in 22 s.** It reported:
- head tip `2cad07f7`, merge-base `eb965139`, base tip `9bc1cf3b`;
- diff 12 files, +760/-50;
- head 4/4 files, 521 passed / 0 failed;
- base product 0/4 files OK, 486 passed / 35 failed.

**Every fact agrees with mine** (the base tip shows develop moved during the session).

**Deviation:** the brief said to run Spark FIRST. I ran it after my own red-first and mutant runs, so my figures were not shadowed by it, but the order differs from the brief. `spark_review.py`, the LLM half, was **not run**: the brief names only the deterministic runner. So there is no Spark verdict to calibrate. The calibration is facts only:

| Spark fact | Mine | Call |
|---|---|---|
| head 521/0 | 521/521 | agree |
| base 486/35 | 35 red (24 + 11) | agree |
| diff 12 files +760/-50 | 12 files +760/-50 | agree |
| merge-base `eb965139` | `eb965139` | agree |
| — (no review) | G66-F1…F5 | not applicable (no Spark review run) |

## NOT TESTED (Rule 2)
- **Kam's ruling itself.** Option (b) (connectors) is not gated. If ruled, it needs a new gate.
- A running stack: gateway → vc-issuer with real RS256 tokens minted by auth. The token shapes in G66-F1 are READ ONLY from auth's code. I did not mint a platform-portal token and send it.
- Any real environment (demo, kintsugi, prod): how many owner-less-with-tenant credentials exist, and which tenants have a users-table SYSTEM_ADMIN.
- The four platform suites (Schemathesis, Akto, Playwright, k6). Node 24 LTS. eslint. The leg-16 ratchet.
- The author's own 17 mutant runs (script not found). I reconstructed 6.
- The in-memory fallback on real PG failure mid-request (DB throws → memory). It is covered only by the PR's memory-path cells, which pass. Pre-existing side effect, not exercised: after a DB revoke, `memoryStore` holds the credential with no `memoryOwners` entry, so a later memory fallback treats it as OWNERLESS with no tenant, which is readable by nobody. That is fail-closed.
- Multi-replica, concurrency, a revoke race (a single UPDATE by id; no transition guard was in scope).
- The PR body on GitHub: not read (I used the READY mail and the commit's fragments). `mergeable_state` and checks: not read.

## HOW
- Clone and fetch as above. `npm ci --ignore-scripts` (`evidence/npm_ci.log`). `npm run build` in `packages/shared` (`evidence/shared_build.log`).
- `scripts/run.py`: vitest JSON-reporter runs of the 4 files (`head`), the base-product swap (`base`), the real-PG probe driver, and a `swapped()` context that asserts the anchor, that the edit landed, and the sha256 restore.
- `scripts/realpg.py head|base`: the probe on both schemas. `scripts/mutants.py`: GM1-GM9, each against the PR cells and the probe (g66boot). `scripts/author_mutants.py`: the 6 reconstructions.
- Probe: `scripts/gate66-realpg.probe.test.ts` was copied into `src/__tests__/` for each run and moved to `tmp/_quarantine_2026-11-01/` afterwards. The schema DDL came from the repo's own files (`scripts/ddl_boot.sql`, `scripts/ddl_mig.sql`).
- Container: `gate66-pg` (postgres:15-alpine, 127.0.0.1:55466, a local throwaway password), **stopped** at the end. gate65-pg and s-w13-pg were not touched.
- No write verb was run under `/Volumes/DevMASTER/!CODING`. The author's `/tmp/e22` was only listed, read-only.
