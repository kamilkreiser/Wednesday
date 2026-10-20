VERDICT: NO GO at head cbf31d40d652... (tier 1, round 2 of 2; landing tree 6256a8e09659efe65dbd7fc6f15dd5e1eef9fc53 on develop 610570e5a757; 1 blocker, 7 notes)

## BLUF
Round 2 closes B1 as BN1 built it. On real PG 15 the K8b/K9b/no-row/no-minter fixtures each go to their own minter or are skipped with a reason. The author's round-1-rule mutant reds exactly the 5 claimed cells, by assertion. The code fix is byte-unchanged from round 1. At the landing, lineage-certify is 19/19 and verify-trusts is **17/17** in both modes, the unit suite is 134/134 files and 1,568/1,568 tests, and `tsc` is rc 0.

**The blocker:** when a child's parent carries no connector `version:*` row, 055 trusts `metadata.versionedById` with nothing to check it against. The header's premise ("server-set on all three minting routes since KS-1508") does not hold for the rows this backfill exists for. Before KS-1508 (b2085e99f, merged 2026-10-13), **every** route let the caller choose that key:
- On `/version`, `/sign-cert` and `/sign-wallet`, `...metadata` was spread AFTER `versionedById: user.id`.
- `POST /` stored `data.versionedById` as sent.
- `/certifications/issue` spread it into the derived row.

So a pre-KS-1508 row can still credit a connector that did not mint the document. That is B1's harm: certify on both paths, the GET read-back and the legacy-certify UPDATE. I measured two shapes, and one of them is ordinary traffic.

Demo exposure is zero by the author's own figures: all 31 candidates are corroborated by a server-written parent row. **kintsugi is UNMEASURED.** Requiring corroboration would have cost 0 of the 31 on demo. Kam may reasonably accept this as residue, with a kintsugi count before 055 runs there. That is his call, not a gate pass.

Heads re-read at the end: refs/pull/1654/head = cbf31d40d652875d3ec99d43f6309dd7b75f1dd7 (unchanged). develop MOVED from f4259b8ed387 to **610570e5a757** (#KS-1407, KS-1157). That move touches 12 files, all under `services/auth`, and 0 of them are under originate/ or migrations/. The control is the same matcher counting 12 files in total; `jwt.ts` is not among them. merge-tree on live develop is clean (rc 0), tree 6256a8e0. My runs used the landing on f4259b8 (merge commit 8e577a9a, tree 3ffc5bf0).

## BLOCKER
**B2: 055 trusts a field that callers could forge, whenever there is no parent row to check it against (fail-OPEN, same harm class as B1).**
File: `migrations/055_ks1557_backfill_connector_create_for_versioned_documents.sql`, in the eligibility CASE. Clause 3 applies only `WHEN parent_rows > 0`. With no connector `version:*` row on the parent, or no parent at all (it is a `LEFT JOIN`), `own_minter LIKE 'connector:%'` alone decides.

Measured on PG 15.14, superuser run:
- **FORGE1 (`gx-K25`).** A pre-KS-1508 `/version` sent without obo, with planted `metadata.versionedById='connector:platform-s:c9'`. The parent has no row. Result: `create:connector connector:platform-s:c9 ks1557-055-backfill`. Credited to c9, which minted nothing.
- **FORGE2 (`gx-K26`), the benign path.** A pre-KS-1508 `POST /` that round-trips a K version's data. KS-1508's own comment calls this a real caller pattern ("a caller that round-trips a K document's data into a create"). The new document carries `versionAction` plus the ORIGINAL minter's `versionedById=c1`, and has no `parent_document_id`.
  - A human creator writes no creation row.
  - Neither does a no-obo connector creator: on develop, `POST /` writes `create` only with obo, and `create:connector` arrives with this PR.
  - 055 credits **c1** on a document c1 never created: `create:connector connector:platform-s:c1`.
  - `GET` exposes metadata in `data` (`documentRepo.ts:183-189` spreads `meta`), so the round-trip carries both keys.
- **Consequence.** `wasCreatedByConnector` (`provenance.ts:321-334`) matches `connector_id` exactly, with no other predicate. The credited connector therefore passes:
  - certify on both paths (`certifications.ts:128`);
  - the `isCreatingConnector` GET read-back (`documents.ts:1138`);
  - the legacy-certify `UPDATE`.

  BN1 measured that reach for a credited row.
- **The repo already says these rows cannot be trusted.** KS-1508's own commit: "derivative rows planted before this fix cannot be told apart by shape."
- **Population.**
  - Demo: the author reports 31 candidates, all with a parent row, 0 parents with no row, and 31 inserted. Each of the 31 therefore had `parent_agrees` true, i.e. corroborated by `recordOnBehalfOf`'s server-set `connector_id = req.user.userId` (`documents.ts:122-133`). So demo exposure is 0, which I inferred and did not measure myself.
  - kintsugi: unmeasured, and 055 runs wherever migrations run.
- Not prescribing a fix. As an observation only: skipping and reporting the uncorroborated branch would have changed 0 rows on demo.

## NOTES
- **N1 (Q3): the report is not pinned.** The report and the insert do read one temp table, and `eligible = (skip_reason IS NULL)` is never NULL, so the two sets partition the candidates. But no cell asserts the report:
  - My mutant MR2 (report loop `WHERE NOT eligible` changed to `WHERE eligible`) printed "skipped 12 of 18" against 12 inserted, and still passed **12/12** green.
  - The insert-side mutant MR3 (`OR skip_reason LIKE '%DIFFERENT%'`) IS killed: B1a red by assertion, `Received: "connector:platform-s:c2-…"`.

  The report has no deploy-visible reader anyway (BN1 N2, still true).
- **N2: the connector-principal clause (BN1 N4) is not isolated by any cell.**
  - MR5 deletes the `NOT LIKE 'connector:%'` branch and passes 12/12.
  - The reason: B1b's human child sits under `pPlain`, whose row names C1, so the cross-check alone skips it.
  - A human minter under a parent with no row would be credited under MR5.
  - The current code is correct (my `gx-K9b`, `gx-K29b/c` are skipped). The claim "cell B1b proves a human minter gets nothing" is true of the code, but that cell does not test it.
- **N3: the `LEFT JOIN` widens scope without a cell, and the header overstates it.**
  - MR6 (LEFT changed to INNER) passes 12/12.
  - The LEFT JOIN is what admits parentless documents, which is FORGE2's vector.
  - The header says children whose parent has no row are "SKIPPED and REPORTED". In fact they are INSERTED (`gx-K11`, `gx-K26`; the author's own NOPARENTROW cell asserts the credit), with no per-id NOTICE.
- **N4 (Q4, N2 measured): the guard checks the setting, not whether the rows became visible.** Runs as `secuura_app` (NOSUPERUSER, NOBYPASSRLS):

  | Arm | Result | rc |
  |---|---|---|
  | shipped file | 12 inserted | 0 |
  | `set_config` line removed | raises `REFUSING TO RUN … reads (unset)`, 0 rows | 3 |
  | set line and guard both removed (BN1's hazard) | "inserted 0 … skipped 0 of 0" | 0 |
  | shipped file, on a copy whose policies lack the `tenant_scope_bypass` arm | inserted 0 (superuser control on the same copy: 12) | 0 |

  - With the rc 3 arm, nothing is recorded: `run-migrations.sh:128-129` records only on success.
  - A `set_config` can never fail to take, so with the shipped file the RAISE fires only if someone edits the line out. The fourth arm shows the guard does not check that rows became visible: the GUC took and the rows stayed hidden. That failure needs a different policy from 039's, so it is residue.
- **N5 (Q6): the named decision on the bucket is acceptable as a NOTE.**
  - Crediting `connector:api-key` gives every holder of a connector-id-less key in the tenant certify (both paths), the GET read-back and the legacy UPDATE on those children. That is across organisations: the principal string is identical (`jwt.ts:289`, `auth.ts:392`), and `wasCreatedByConnector` has no org predicate.
  - Against BN1 N1's baseline (the minter gains certify and read on its minted child, and no reach into the original), this grants the bucket exactly what the forward writer (`documents.ts:2365`) grants it for every new bucket-minted version. It grants no reach into the parent.
  - It is the known KS-1685 defect extended to 6 existing rows on demo (the author's count, which I did not measure). It is not a new party class.
  - Keep KS-1685 linked. I would not block on it.
- **N6:** `parent_agrees` and `parent_rows` join provenance by `document_id` only, not by tenant. In `gx-K30`, an agreeing row in tenant T2 satisfied the cross-check for a T1 child. Today this is inert, because the credit comes from the child's own record anyway, but it weakens the cross-check if one is added.
- **N7: residue.**
  - The header's line cites have drifted. It gives `:2339/:3077/:3272` for `versionedById`; the actual lines are 2347/3092/3287. It gives `:2891/:3159` for sign-cert/sign-wallet; the actual lines are 2905/3173.
  - `versionedById='connector:'` is credited (`gx-K29a`). That is inert, because no key mints that principal (`|| 'api-key'`).
  - `ks1557-verify-trusts` is timezone-sensitive: with the DB `timezone=Australia/Sydney`, MT=false shows 3 reds (certifiedAt off by 11h), **identically at develop f4259b8**. It is 17/17 with the DB in UTC. This is pre-existing, not this PR.

## FOUND / TESTED / HOW
- **Byte-unchanged claim: VERIFIED.**
  - `db9bca740df0` is an ancestor of the head (rc 0).
  - `diff --stat db9bca740df0 cbf31d40` lists only 055 and the new test file.
  - The blobs are equal at both commits: documents.ts d3e7e2a2, provenance.ts 2cbc4aa0, ks1228 246e3bac, lineage-certify 7ff08743.
  - The two src blobs are also unchanged at the landing.
- **Q1 (PG 15.14, my instance 127.0.0.1:55480; DB migrated 001..054 + 003_platform_tenancy as superuser `secuura`).** Fixture: 21 K documents and 14 rows, counted before the run.

  | Fixture | Result |
  |---|---|
  | K8a | c1 |
  | **K8b** (minter c2, parent row c1) | SKIPPED "DIFFERENT connector" |
  | K9a | c1 |
  | **K9b** (human uuid, sign-wallet) | SKIPPED "not a connector principal" |
  | K11 (no parent row) | own c1 |
  | K12 (no minter) | SKIPPED "absent" |

  Break attempts:
  - K21 (minter c3, parent names only c1): SKIPPED.
  - K23 (two `version:*` rows on the parent, both c1): ONE insert.
  - K24 (parent rows c1 and c2, child c2): c2.
  - K27 (parent row with NULL connector): own c5. So clause 3 is skipped there too.
  - K31 (child in T2, parent in T1): row lands in T2.
  - K40/K41 (pre-existing `create:connector` / `create`) and K42 (no versionAction): untouched.
  - FORGE1 and FORGE2: see B2.

  Totals: inserted 12, skipped 6 of 18. Idempotent: run 2 inserted 0 and the total stayed 26. Reverse `DELETE` removed exactly 12, total 26 to 14, and K40/K41 survived.

  Human principal ids: human JWTs carry `users.id` (uuid). Only `generateConnectorToken` and the gateway's API-key branch mint `connector:` (`jwt.ts:289`, `api-gateway auth.ts:392`). I found no route that lets a human principal carry that prefix. The only `connector:` strings a human can place are planted *values*, which is B2.
- **Q2:** the three routes at the landing set `versionedById: user.id` AFTER `...metadata` (`documents.ts:2347`, `:3092`, `:3287`). `POST /` drops it (`:617-618`), and `/certifications/issue` drops it (`certifications.ts:647`).
  - Today: a client cannot store it.
  - Before b2085e99f: a client could, on all five routes (the diff was read).
  - Rows with no `versionedById` are skipped (K12).
  - Rows with a planted value: see B2.
- **Q5:** I re-made the author's round-1-rule mutant (MR1: `own_minter` := the parent's single distinct connector; clauses 2 and 3 removed). Result: **5 failed / 7 passed**, red on exactly B1a, B1b, NOPARENTROW, NOMINTER and MULTI. All five are assertion failures (`Received: "connector:platform-s:c1-74aa9d8e"` / `Received: null`, `expect(` present).
  - My own mutants: MR3 and MR4 (clause 3 removed) are killed on B1a by assertion. MR2, MR5 and MR6 survive (N1-N3).
  - Every mutant was first run through psql at rc 0, as the SQL analogue of `tsc` rc 0; the test file was unmodified throughout.
  - After every arm the file was restored with `git checkout landing --`, asserted by blob `1edafb8d`, and the index was clean.
- **Q7:**
  - Committed `ks1557-055-backfill`: 12/12 in both modes.
  - `ks1557-lineage-certify`: **19/19** in both modes.
  - `ks1557-verify-trusts`: **17/17** in both modes (the landing blob e950ef32 equals develop's).
  - Unit suite: develop f4259b8 gives 134 files / 1,568 cells; the landing gives 134 / 1,568, all passed. By cell NAME the only difference is the renamed ks1228 control (1 out, 1 in), with 0 status changes.
  - `tsc --noEmit -p originate`: rc 0, 0 `error TS`.
  - The new test file, type-checked in its own program (jest+node types): rc 0. Positive control: the same program plus an injected bad file gives exactly 1 `TS2322`, in that file.
- **HOW:**
  - Scratch clone `--shared` of the spark cache at `<scratch>/gate_bu1/src`, with a repo-local `core.sshCommand` (Secuura deploy key, read in place). I fetched develop and the PR ref only, read-only, and ran git write verbs from scripts with literal paths.
  - Then `npm ci --ignore-scripts`, the `packages/shared` build, and `npm run generate` in originate. Without the generate step, MT=false lineage-certify failed 19/19 at a load error; I discarded that run.
  - The integration DB also needed a platform DB for MT=true (from `docker/init-platform`) and the DB timezone set to UTC (N7).
  - No Docker; no box was touched.
  - Fixture, mutants and scripts live in `<scratch>/gate_bu1/{tools,mut,bin}` and were never committed. Postgres was stopped at the end.

## NOT RUN
- An HTTP-level certify or GET on a B2-credited row: I cite `wasCreatedByConnector` and BN1's measurement of that reach instead.
- The author's demo figures (31 / 6 bucket / 0 uncorroborated): not re-measured, since the boxes are not mine. kintsugi: unmeasured.
- Not run: eslint; the `migrations` image build; the gateway `startup-migrations` runner (055 was applied via psql only); the four platform suites; Schemathesis, Akto, Playwright, k6.
- The PR body was not read (no `gh` use).
- I ran no suites on the live-develop landing tree 6256a8e0. Its delta from my tested landing is auth-only (0 originate or migration files).

## Untracked paths in /Volumes/DevMASTER/WEDNESDAY
`git status --short` at the end: none untracked outside the allowed folders (only ` M 0_Brain/daily/2026-10-20.md` and ` M 0_Brain/dashboard/data/usage_wednesday.json`, neither of them mine).

## Wall-clock
11:31 to 11:56 AEDT 2026-10-20 (about 25 min).

sha256 (method: `sed '1d;$d' verdict.md | shasum -a 256`): 1bdaddf25b080bef2f7b339c05295ff085fd91218102fbf806d15fb8ed7befbf
