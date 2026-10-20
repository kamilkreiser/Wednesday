VERDICT: GO WITH NOTE at head c52ab20328fa... (tier 1, round 3 of 3; landing tree 7cef3f20d1342c3cf7fcbf137063db4709173e76 on develop e84971b3504c; 0 blockers, 7 notes)

## BLUF
B2 is closed. Every branch of 055's CASE now refuses a child whose parent carries no connector `version:*` row in the parent's own tenant, or that has no parent at all. No path remains where `own_minter LIKE 'connector:%'` alone decides. FORGE1 and FORGE2 credit c9 and c1 under the round-2 file (`1edafb8d`), and both are SKIPPED and REPORTED under the head, each with its own named reason. All 6 of the author's mutants I re-made die with exactly the claimed counts (7, 5, 1, 2, 1, 2). Of my 6 mutants, 4 die and 2 survive; both survivors are tenant-scope variants (N2). The 055 cells pass 17/17 with the RLS cell RUN, in both modes. lineage-certify is 19/19 and verify-trusts is 17/17 in both modes, at the claimed landing and again at a later live-develop landing. The unit suite has 0 vanished cells and 0 status changes by name. `documents.ts` and `provenance.ts` are byte-unchanged.

**The main note (N1):** corroboration works per PARENT, not per CHILD. A pre-KS-1508 child that a different actor minted with a planted `versionedById = C1` is still credited to C1, as long as C1 left a `version:*` row on the same parent (my `gx-K50b`, measured). This is the narrow remainder of B1/B2's harm class: the credited connector must genuinely have versioned that parent. It follows from ruling (a) as the author built it. I do not block on it. **kintsugi is UNMEASURED**, and a one-query count (in N1) would size the exposure before 055 runs there.

Heads: at the start, `refs/pull/1654/head` = c52ab20328fa95da6d75cdc62a91b53e3354de77 and develop = f418cddac514, and merge-tree gave 58c4740a5e46, equal to the claim. At the end the head was unchanged, but develop had MOVED twice:
- To 21e0c39149ca: #1667 KS-1695 (certifications.ts) and KS-758 F9 (gdprService.ts). That is 4 files under originate, 0 of them the PR's 6 files. I re-ran the suites on that landing (tree 0598c752): all green.
- Then to **e84971b3504c**: KS-1689, 2 files, both m365-only, 0 under originate or migrations (control: the same matcher counts 2 files in total). merge-tree rc 0, tree 7cef3f20.

## BLOCKERS
None.

## NOTES
- **N1. Corroboration is per parent, not per child (residue of the B1/B2 class).**
  - Clause 3 asks whether *some* `version:*` row on the parent, in the parent's tenant, names this minter. It does not ask whether *this child's* minting request wrote that row.
  - Fixture `gx-K50a`/`gx-K50b`, on PG 15.14:
    - P50 carries one `version:watermark` row naming c1 (c1 versioned it with obo, which produced K50a).
    - K50b is a pre-KS-1508 `/sign-wallet` child, which writes no row. Its minter planted `versionedById = connector:platform-s:c1`.
    - Head result: `gx-K50b create:connector connector:platform-s:c1 ks1557-055-backfill`. The round-2 file gives the same result.
  - c1 then passes `wasCreatedByConnector` on a document it did not mint. That means certify on both paths, the GET read-back and the legacy UPDATE (the reach BN1 measured).
  - The bound: the credited connector really did version that same parent with obo, so this is not a free choice of beneficiary as FORGE1 was.
  - The header overstates it. Line 10 says "CREDITED ONLY WHERE ITS PARENT'S OWN RECORD CONFIRMS THE MINTER". The parent's record confirms that this connector versioned the parent, not that it minted this child.
  - Nothing in the shape tells this case apart from c1 versioning P twice with one obo, so a stricter rule would cost legitimate rows. I am naming it, not prescribing a fix.
  - **Before 055 runs on kintsugi**, count it. For each (parent, minter), compare the number of candidate children with the number of the parent's own-tenant `version:*` rows naming that minter. Any pair where children > rows is where this can occur.
  - Demo: BN1 read the author's figures as 31 children on 31 distinct parents with 31 rows. That would make demo 0, but I did not measure it.
- **N2. The tenant scope is only half pinned.** CROSSTENANT kills the author's "tenant scope" mutant (both subqueries unscoped: 2 red, by assertion). Two variants that are just as fail-open pass **17/17**:
  - **O3** removes `ap.tenant_id = p.tenant_id` from `parent_agrees` only. On my fixture this credits `gx-K52` to c1: the parent's own-tenant row names c2, and a row filed under T2 names c1. It also credits `gx-K30` to c7.
  - **O4** scopes on the CHILD's tenant (`d.tenant_id`) instead of the parent's. This credits `gx-K53`: the parent is in T1 with no own-tenant row, and the child plus a planted row both sit in T2. That is the exact forgery shape the header (lines 133-137) gives as its reason to scope on the parent.

  The code at the head is correct: it skips K52, K53 and K30. Only the cell is missing. A related inert detail: `gx-K31` (child in T2, parent in T1, corroborated in T1) is credited, and its row lands in T2.
- **N3. REPORT is not hermetic.** I planted one foreign, uncreditable, version-minted document in a third tenant and committed it. REPORT then fails, **by assertion** (`+ "cn1-foreign-1"`); the other 16 cells pass.
  - The cause: 055 is global, and REPORT compares every printed id against a set scoped to T.
  - The file header ("One tenant of this run's own, so the cells cannot read another seat's rows") is therefore false for REPORT.
  - By the same mechanism (code read, not measured), on a shared integration DB the FORWARD and RLS runs insert `create:connector` rows on other tenants' candidates. `afterAll` deletes only T and T2, so those rows stay.

  Both are test-harness issues, not migration defects.
- **N4. NOPARENTROW's inversion is the right reading, and it has a real cost.**
  - It matches Kam's ruling. In Wednesday's daily note at 14:03, card `…round3-1020` = a, "round 3 corroboration-required". The commit and the header say the same.
  - On my 22-candidate fixture, round 2 credits 16 and round 3 credits 8. Dropped:
    - FORGE1 K25, FORGE2 K26, cross-tenant K30, K52 and K53, and `connector:` K29a: all correctly dropped.
    - K27: the parent's row has a NULL `connector_id`.
    - **K11, the one legitimate shape: a connector that versioned without obo before the fix.**
  - Also uncredited unless a coincidental row exists (N1): a connector-minted `/sign-cert` or `/sign-wallet` child, because those routes never write a row. The forward fix does not credit them either (BN1 N5).
  - **Consequence:** those historical documents keep today's state for their minting connector: certify is 403 on both paths, the GET read-back is 404, and the legacy UPDATE is refused. This is Stuart's regression, left in place for those rows.
  - The header (lines 59-64) states it, and it is the recoverable direction.
  - Demo cost is 0 by the author's figure ("0 have a parent with no row"). I did not measure it. On kintsugi it is unknown.
- **N5. The test-file header still has the round-2 cite drift.** Lines 13-14 give `/:id/sign-cert` (`:2891`) and `/:id/sign-wallet` (`:3159`); at the head those are `:2905` and `:3173`. Line 18 still states "server-set on all three minting routes since KS-1508" as the premise, and only the next paragraph corrects it. The migration header's cites I checked are right (`:124`, `:158`, `:2347`, `:2905`, `:3092`, `:3173`, `:3287`, `:617-618`).
- **N6. The carried residue is accurate, with one stale line.**
  - N4 (the guard checks the setting, not visibility): the code at lines 119-123 is unchanged. I did not re-run BU1's fourth arm.
  - N5 / KS-1685: `gx-K28` (`connector:api-key`, corroborated) is credited, as disclosed.
  - N7:
    - Timezone: re-measured. With the DB timezone set to Australia/Sydney, verify-trusts MT=false has **3 reds** at the landing AND at develop f418cdd, identical by cell, each `certifiedAt` off by 11h (`Expected "…10-19T17:19…" / Received "…10-20T04:19…"`). The 055 file is 17/17 under Sydney time, since 055 reads no timestamps.
    - `versionedById = 'connector:'` is "credited but inert": that is now stale. Under round 3 it would need a parent row whose `connector_id` is `'connector:'`, which nothing writes. `gx-K29a` is skipped.
- **N7. A naming matter, pre-existing since round 1 and inert.** The reverse marker sits in `action_provenance.external_ref`, which `gdprService.executeErasureByExternalRef` treats as a Platform-S subject reference (lines 1457, 1511; develop's KS-758 F9 now writes a `data_deletion_log` row there). An erasure request for the literal ref `ks1557-055-backfill` would match 055's rows in that tenant, blank columns that are already NULL, and log an "erasure". The reverse DELETE stays exact: no other writer puts `create:connector` together with that ref.

## Answers by question
- **Q1.** The CASE at the head (lines 159-165) has six outcomes, in order:
  1. minter absent;
  2. not a connector principal;
  3. **`parent_ext IS NULL`** (new);
  4. **`parent_rows = 0`** (new; own-tenant, `connector_id IS NOT NULL`);
  5. `NOT parent_agrees`, now unguarded;
  6. otherwise eligible.

  So a credit requires `parent_agrees`, and `parent_agrees` requires an own-tenant parent row equal to the minter. Branch 4 is defended twice: my O5 deletes it and nothing is credited, because branch 5 catches the child, so only REPORT's reason text reds. The fail-open forms are killed: O1 (`parent_rows = 0 THEN NULL`) reds NOPARENTROW, FORGE1, CROSSTENANT and REPORT; O1b (`parent_ext IS NULL THEN NULL`) reds FORGE2 and REPORT.

  BU1's own fixture plus my additions, run twice per file inside BEGIN/ROLLBACK:

  | Fixture | Round 2 (`1edafb8d`) | Head |
  |---|---|---|
  | FORGE1 `gx-K25` | `create:connector …c9` | SKIPPED, "parent carries no connector version row" |
  | FORGE2 `gx-K26` | `…c1` | SKIPPED, "has no parent document at all" |
  - Head totals: inserted 8, skipped 13 of 21 (14 of 22 with K53). Run 2 inserted 0.
- **Q2.** See N4. Credited at the head: K8a, K9a, K23, K24, K28, K31, K50a, K50b. Credited in round 2 and not at the head: K11, K25, K26, K27, K29a, K30, K52, K53.
- **Q3.**
  - **HUMANOBO** asserts the human-on-behalf-of case. The parent row names that same uuid, and its own control asserts the row exists. Only the connector-principal clause can stop that child: MR5 reds HUMANOBO, with `Received: "<uuid>"`, plus REPORT.
  - **CROSSTENANT** proves that a row filed under T2 does not corroborate. The "tenant scope" mutant reds exactly 2, CROSSTENANT and REPORT. It does not pin the half-scoped variants (N2).
  - **REPORT** asserts that the printed SKIPPED ids equal the not-credited set read back from the DB. It also checks that set by name (8 ids) and each id's reason, plus `size > 0`. An empty report fails both (a) and (b), and MR2 and my O2 (the report drops NOMINTER) each red REPORT alone. Hermeticity gap: N3.
- **Q4.**
  - Idempotent: a second run inserts 0, both in the cell and in my fixture.
  - Reverse: the DELETE on my fixture removed exactly 8, total 26 back to 18, and the pre-existing K40/K41 survived.
  - RLS: the cell RAN as `secuura_app` (it asserts `rolsuper=false, rolbypassrls=false`). My fixture under `SET ROLE secuura_app` also gave 8 inserted, then 0 on the second run.
  - No candidates (the real DB, committed run): "0 candidate … inserted 0" as secuura and as secuura_app, rc 0. `action_provenance` stayed at 0 before and after, and no temp table was left behind. The positive control is the same file against the fixture: 22 candidates.
  - Candidates but ZERO `version:*` rows anywhere: "inserted 0, skipped 22 of 22", rc 0.
  - Timezone: N6.
- **Q5.**
  - 055 file: 17/17 in both modes, at both landings, RLS cell run. Superuser-only run (no app DSN): 16 passed, 1 skipped (RLS).
  - lineage-certify: 19/19 in both modes. verify-trusts: 17/17 in both modes.
  - Unit suite: live landing 58c4740a = **135 files / 1,577**; develop f418cdd = 135 / 1,577.
    - By cell name, the only difference is the renamed ks1228 control (1 out, 1 in), with 0 status changes.
    - Against BU1's landing JSON: 0 vanished and 9 added. Those are 8 from `ks1659-a-connector-certifying-with-no-holder.test.ts` and 1, `ks1679 … R6`, which arrived in f418cdd. That R6 is absent at f01ba49 and present at f418cdd, by `git grep`.
    - So the author's 135 / 1,576 at f01ba49 re-derives as 1,568 + 8. Removing ks1659 at f418cdd gives 134 / 1,569, which is BU1's 1,568 + R6.
    - Later landing 0598c752: 136 / 1,625. The extra 48 are 37 from the new ks1695 file and 11 new ks695 cells. 0 vanished, 0 status changes.
  - The blobs `d3e7e2a2` (`documents.ts`) and `2cbc4aa0` (`provenance.ts`) are equal at db9bca7, cbf31d4 and the head. Control: develop's blobs read as changed (6c2386b3 / 483aa9eb).
  - The test file type-checks in its own program: rc 0 with 0 `error TS`. Control: an injected bad file gives rc 2 and exactly 1 TS2322, in that file. `tsc --noEmit -p originate`: rc 0.
- **Q6.**
  - Author's mutants, re-made: round-1 rule **7** · round-2 rule **5** · MR2 **1** · MR5 **2** · MR6 **1** · tenant scope **2**. All match the claim. I did not re-make conjuncts A/C/D.
  - Mine: O1 4 · O1b 2 · O2 (REPORT) 1 · O5 1 (reason text only) · **O3 0 and O4 0, both survived** (N2).
  - Each mutant first ran through psql at rc 0 inside BEGIN/ROLLBACK. Each red was by assertion (`Received:` / `expect(` present). After each arm the file was restored with `git checkout`, asserted by sha256 `a4d838106ffe00b6…`, and `git status` was clean.
- **Q7.** `gh` is not logged in for this seat ("You are not logged into any GitHub hosts"), so I did NOT read the live PR body. I checked the corrected cites quoted in the claim against the head, and each points at what it claims:
  - `documents.ts:2358` = the `version:${action}` row;
  - `:776` = the create-path `recordConnectorProvenance`;
  - `:1163` = `getCreationProvenance` on GET;
  - `provenance.ts:272` = the literal `action = 'create'`;
  - `:287` = `pseudonymised`.

  The old cites point at unrelated lines, as the author says. I found no sentence in the 055 header describing a guard that does not exist. Line 10's wording overstates (N1), and the test header is stale (N5).
- **Q8.** I measured nothing on demo or kintsugi: no `az`, no ssh, no SELECT. The 31 / 6 / 0 figures are Seat C 31st's, quoted by the author, and I did not re-measure them. kintsugi is UNMEASURED, so the counts behind N1 and N4 there are unknown.

## FOUND / TESTED / HOW
- **FOUND:** B2 closed. N1, the per-parent corroboration residue, measured. N2, two surviving tenant-scope mutants, measured. N3, REPORT not hermetic, measured. N4-N7 as above.
- **TESTED:**
  - My own PG 15.14 on 127.0.0.1:55491. I ran initdb in my scratchpad (TCP only, DB timezone UTC) and stopped the server at the end.
  - Tenant DB `cn1_it`: docker/init plus migrations 001..054 plus `003_platform_tenancy`. Platform DB `cn1_platform` from `docker/init-platform/01-platform-schema.sql`, for MT=true.
  - The integration file was run with jest's integration config and an explicit `--rootDir`:
    - superuser run: `TEST_DATABASE_URL=postgresql://secuura:…@127.0.0.1:55491/cn1_it`, `MULTI_TENANCY_ENABLED=false|true`;
    - RLS run: the same, plus `TEST_APP_DATABASE_URL=postgresql://secuura_app:…/cn1_it` (NOSUPERUSER NOBYPASSRLS, asserted by the cell);
    - a superuser-only run with the app DSN unset.
  - The Sydney timezone runs used `ALTER DATABASE cn1_it SET timezone`, reset to UTC afterwards (read back).
  - My fixture was BU1's `fixture.sql` (copied, read in place) plus K50a/b, K52 and K53. It always ran inside BEGIN … ROLLBACK, except the N3 plant, which I deleted afterwards (read back: 0 tenants left).
- **HOW:**
  - `git clone --shared` of the spark cache into `<scratchpad>/gate_cn1/src`. Origin was repointed with a repo-local `core.sshCommand` (Secuura deploy key, read in place). I fetched develop and `refs/pull/1654/head` only. Every git write verb ran from a script with literal paths; there was no `cd`.
  - Then `npm --prefix <clone>/Blockchain/Dev ci --ignore-scripts`, the `packages/shared` build, and `npm run generate --workspace=services/originate`, all rc 0.
  - Every npm, jest, tsc and psql command named its directory inside the clone or the scratchpad.
  - Mutants and the fixture live in `<scratchpad>/gate_cn1/{mut,tools}`; none was ever committed.

## NOT RUN
- An HTTP-level certify or GET on a K50b-credited row. I cite `wasCreatedByConnector` and BN1's measurement instead.
- Anything on demo or kintsugi.
- The live PR body (`gh` not logged in).
- The author's conjunct A/C/D mutants.
- BU1's fourth RLS arm (policies without the bypass arm).
- eslint, the `migrations` image, the gateway `startup-migrations` runner (055 was applied via psql and jest only), concurrency, and Schemathesis, Akto, Playwright and k6.
- No suites on the final landing 7cef3f20. Its delta from my tested 0598c752 is 2 m365 files.

## Untracked paths in /Volumes/DevMASTER/WEDNESDAY
`git status --short` before writing this file: every untracked path sits under 0_Brain/, 2_Project_Files/fleet/briefs_staged/ or 2_Project_Files/local-model/. There are none outside them, and none are mine. Apart from those, the only new file is this verdict.md.

## Wall-clock
15:06 to 15:31 AEDT 2026-10-20 (about 25 min).

sha256 (method: `sed '1d;$d' verdict.md | shasum -a 256`): 6e710543e8e85c365afc9ccff504bce035368fba502a6cdacd12d5f425a188f5
