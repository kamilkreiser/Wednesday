GO WITH NOTES — HOLD-FOR-KAM (3 of 43 real-PG cells present a certification base did not: 2 are the original holder's own certification, 1 is a latecomer's under the D4 registry-time residual where base's unordered pick happened to land on the original; G188-F7)
# QA Gate 188 (Tier 1, round 2): PR 2000 / KS-1561 verify presents the ORIGINAL registrant's certification (G188-F1 delta)

## Subject
- Repo Secuura/Distributed_Secuura, PR 2000. Round-2 head `f702d4da4b69478e82d3d79ea4e8746fae47f2eb` (parent = round-1 head `d03b03046d76`, one commit, fast-forward).
- **Start** (12:36:04Z, ls-remote on the read-only checkout): head `f702d4da4b69478e82d3d79ea4e8746fae47f2eb`, develop `536642104002f506f61e2e9b6c98a32bf19c3b10`.
- **End** (12:48:13Z): head `f702d4da4b69` **unchanged**, develop `536642104002` **unchanged**.
- Merge-base of head with develop: `d92b849ece732cd04e283bfcb0ee9e8bd6989631` (the branch base; base = develop as the PR started from it).
- **Merge tree, for the merge seat:** `git merge-tree --write-tree 536642104002 f702d4da4b69` in my clone: **rc 0, tree `6eb2b84777ccc1840ac14d8f075af9405c64bcef`**. It differs from develop in exactly the PR's 7 files; its two route files are byte-equal to the head's.
- Host: Node v26.8.1, TypeScript 5.9.3, jest 29.7.0 / ts-jest 29.4.14, pg 8.23.0, PostgreSQL 15.19 (Homebrew keg), my own cluster (data dir `tmp_r2/pgdata`, TCP 127.0.0.1:55488 only, unix sockets off: the workdir path is too long for a socket). Not run on: Node 24, kintsugi or demo, a deployed stack, Docker.
- Dependencies: round 1's install in my `clone --shared` (lock unchanged between d03b and f702: the commit touches 5 files, none a lock). `@secuura/shared` mapped read-only to the shared checkout's build, as in round 1 (disclosed there).

**Method.** I fetched the PR ref into my round-1 clone and checked the head out there. Each version (base d92b849e, round-1 d03b0304, round-2 f702d4da) was driven by writing that version's two route blobs into my clone (`git show`, never a checkout of the shared repo), running, then restoring the head blobs with `git checkout f702 -- <files>` and checking sha256 (`aadbf21f6e8e33aa` / `9219e8b9703ef429` after every run). The real-PG harness (`harness_r2/g188r2-pg15.harness.test.ts`) started from a COPY of Seat F 30th's pgcell template (its DB seam and seed shape). I re-pointed it at my clone and my cluster, and added my own cells: the 22/23-row trigger edge with per-request query counts, 24/25 tied originals, an owner-sensitive tie cut, and two registry cells built to look for a head-more-permissive-than-base outcome (CAP-LATE-LOWID, CAP-ORIGCERT). It drives the real `verificationRouter` / `verificationV2Router` over HTTP; the routes' own SQL runs on PG15 (schema `docker/init/01-schema.sql` + platform schema at f702, plus the two ALTERs both earlier harnesses used). Direction was counted by `harness_r2/table.py` from the per-cell records, with a swapped control. EXPLAIN ran on a separate DB loaded with `migrations/001_initial-schema.sql` at f702, seeded with 310,030 rows. Mutants: `harness_r2/mutants_r2.py`, against the committed bytes, each run against both the seat's 30-cell mock file and my PG harness.

## Findings

### G188-F1 — (round 1 MAJOR) — FIXED, measured on real PostgreSQL 15
- **FOUND:** the original is now found over the full same-hash set. At 22, 23, 24 and 25 later certified copies, round 2 presents B (the uncertified original), not certified, with no certification, on all 5 paths. The 5 paths are /verify, verify-file, cross-tenant, v2 local and v2 cross; v2 count is 1.
- **TESTED:** `runs_r2/pg_table.txt`, 20 real-PG cells × 3 versions. Base presents the latecomer at every n. Round 1 presents B at 22 and 23 and the latecomer (gcert-a-24, gcert-a-25) at 24 and 25. Round 2 presents B at all four. That is exactly the table the commission expected (plus my n=22 row). My round-1 mock cell N-TRUNC is now green at f702, and N-TRUNC-23 is still green.
- **HOW:** `bash harness_r2/run_pg.sh <base|r1|r2> pg_<v> [r2]`; records in `runs_r2/pg_{base,r1,r2}.jsonl`. Every r2 assertion passed (20/20, EXPECT=r2).

### G188-F5 — MINOR: for a hash with a few hundred rows or more, the new MIN(created_at) subquery walks the whole `documents` table through `idx_documents_created`, not `idx_documents_content_hash`
- **FOUND:**
  - On a migrated database (migration 001: `idx_documents_content_hash` and `idx_documents_created (created_at DESC)`), PostgreSQL 15 plans `SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = $1 OR … $2 OR … $3` two ways, depending on how many rows it estimates for the hash:
    - **Small groups** (24 and 100 rows): a BitmapOr on `idx_documents_content_hash`. 10-13 buffers, about 0.03 ms.
    - **From 300 rows up** (300, 576, 1,000, 2,000, 5,000; 310,030-row table): `Index Scan Backward using idx_documents_created … Filter: content_hash …`. It walks created_at from the oldest row until it meets the hash.
  - When the hash's rows are the newest in the table (a recently registered file), that walk reads **every row: Rows Removed by Filter 310,027, 18,899 buffers, about 31 ms**. For comparison, the unchanged row-set read on the same hash costs 136 buffers and about 1 ms.
  - With the hash's first row in the middle of the table, the walk was 133,237 rows (3,932 buffers, 13.6 ms).
  - The outer read (`created_at = $1`) is cheap in every plan.
  - So the extra read is cheap in the common case: it only fires when a read returns 24 rows. But for exactly the large groups it exists for (the code's own comment names a 576-row group), it costs a walk of the whole table on an unauthenticated verify path. The cost scales linearly with the size of the tenant's `documents` table.
  - Seat F 30th's EXPLAIN, on a 25-row table, could not show this.
- **TESTED:**
  - Custom plans, both with literal values and with a `$1..$3` prepared statement. The pg driver sends unnamed statements, which are custom-planned.
  - Generic plan forced: it chose the bitmap (`runs_r2/explain.txt` B2).
  - Grading: MINOR at the measured scale (31 ms at 310k rows). It would be MAJOR if a tenant's documents table holds millions of rows. That table size is **not measured**, nor how often groups of 300+ rows occur.
  - Not FIX-BEFORE-MERGE on my reading: correctness is unaffected.
- **HOW:**
  - `psql -f harness_r2/explain.sql`, then `explain2.sql`, then `explain3.sql` (a probe that flips at between 100 and 300 rows), on DB g_mig. Outputs: `runs_r2/explain{,2,3}.txt`.
  - Control: the same file shows the unchanged row-set read using `idx_documents_content_hash` on the same hash (section G), so the instrument distinguishes the two plans.
  - A fix shape (not tested): read the MIN from the content_hash rows only. Options are `ORDER BY created_at, id LIMIT 1` over a `(content_hash, created_at)` index, or a MATERIALIZED CTE over the hash's rows, or defeating the created_at index (`MIN(e.created_at + interval '0')`).

### G188-F6 — MINOR: ranking v2's 8 tenants by registry MIN(created_at) trades one residual for another; the seat's CAP-LATE cell does not show the trade
- **FOUND:**
  - Cell CAP-LATE-LOWID: 9 tenants hold the bytes. B, the uncertified original, sits in the LOWEST tenant_id, but its registry row was written late (after every other tenant's).
  - v2-cross:
    - Round 1 (ORDER BY tenant_id) listed **B only, count 1**.
    - Round 2 drops B's tenant and lists **8 latecomer certifications** (gcert-a-2..a-9).
    - Base listed 7 latecomer certifications.
  - So on this cell round 2 is MORE permissive than round 1, but not more permissive than base.
  - The seat's CAP-LATE cell puts B in the 9th tenant by id, where all three versions agree (8 latecomer certs). It therefore reads as "no worse than before", and the CAP-LATE-LOWID shape does not appear.
  - The PR body's residual sentence does cover this case in words ("a tenant whose registry row was written late ranks late"). Wednesday ruled (b) knowing the residual.
  - Neither ordering dominates the other:
    - tenant_id order loses CAP-9 and CAP-10.
    - registry-time order loses CAP-LATE and CAP-LATE-LOWID.
- **TESTED:** real PG, all three versions (`runs_r2/pg_table.txt`). I did not measure how often a registry row is written late in real data.
- **HOW:** `harness_r2/g188r2-pg15.harness.test.ts`, describe "v2 tenant cap". Not FIX-BEFORE-MERGE: it is inside ruling (b), so it is for Wednesday's awareness.

### G188-F7 — MINOR (states the HOLD-FOR-KAM condition): base vs round 2, 3 of 43 real-PG cells present a certification base did not
- **FOUND:**
  - Predicate: v1 `checks.isCertified === true` or a certification object; v2 any match certified or carrying a certification. Count: head presents one where base presented none.
  - **(a) CAP-ORIGCERT, v2-cross** (round-2 change). B registered first in the 9th tenant by id and certified its OWN row; 8 later uncertified rows sit in tenants 1-8.
    - Base and round 1 enumerate tenants 1-8 and show no certification.
    - Round 2 ranks B's tenant first and presents B's own certification (`gcert-b-own`), next to the 7 other rows.
    - This is the original holder's certification, which Kam's ruling (a) says to show. Base hid it because of the cap.
  - **(b) CAP-ORIGCERT, v1 cross-tenant** (round-1 D4, unchanged in round 2). Same data: D4's `ORDER BY created_at ASC, id` picks B's tenant and presents `gcert-b-own`. Base's `LIMIT 1` with no ORDER BY returned tenant 1's uncertified later row.
  - **(c) CAP-LATE-LOWID, v1 cross-tenant** (round-1 D4, unchanged in round 2).
    - Base's unordered `LIMIT 1` returned B's registry row, inserted first in heap order, and presented B uncertified.
    - D4 picks the earliest registry `created_at`. Because B's registry row was written late, that is tenant 2, and the head presents a **latecomer's** certification (`gcert-a-2`).
    - Base's answer here comes from heap order, not from a rule, and the head's is D4's stated residual.
    - It is still a cell where a latecomer certification appears on head and did not on base.
  - Round 1's direction count (0 of 48) did not include any registry-order cell. Rows (b) and (c) belong to round 1's D4 and are newly measured here.
- **TESTED:** all 43 records of `runs_r2/pg_{base,r2}.jsonl`.
  - Swapped control: base presents a certification where round 2 does not in **33 of 43**.
  - Round 2 vs round 1: 2 of 43 (CAP-ORIGCERT v2-cross, which is (a), and CAP-LATE-LOWID v2-cross, which is G188-F6). Round 1 vs round 2: 18 of 43.
  - Both present a certification but a different one: 4 (OLDCERT ×3, where the head shows the original's `gcert-b-old`; CAP-LATE-LOWID v2).
- **HOW:** `python3 -I harness_r2/table.py runs_r2 [swap]`, writing `runs_r2/pg_table.txt` and `runs_r2/pg_direction_swapped.txt`. No signature class is touched (no production, money, message to a human, or irreversible action). The HOLD-FOR-KAM line is written only because the count is above 0, as the commission's Q5 requires. Wednesday rules.

### G188-F8 — INFO: one of my mutants survives (G4: merged originals placed FIRST instead of last); no cell pins which eligible certification wins when a cut-off original and later eligible copies are both certified
- **FOUND:** `selectVerifiableRow` returns `certified[0]` in list order. With originals appended last (head), the most recently certified *eligible* row wins. With them first, a cut-off certified original would win. Neither breaks D1-D4. The mutant is not strictly equivalent, but no cell (mock or PG) has same-owner later certified copies plus a certified original outside the fetched 24.
- **TESTED / HOW:** `runs_r2/mutants_r2.json`: G4 gives 0/30 mock and 0/20 PG red; the file was restored with sha256 equal.

### Carried from round 1
- **G188-F2 MINOR (unchanged, filing candidate):** v1's tenant-local scope vs v2's cross-tenant scope. My round-1 cell N-SPLIT is still red at f702 (v1 `gate188-a0`, v2 `gate188-b0`). The seat states it did not change this.
- **G188-F3 INFO: RESOLVED.** The new file's mock (`answer()`, lines ~111-136) applies `ORDER BY certified_at DESC NULLS LAST`, the LIMIT bound from the template values, and MIN/MAX plus `ORDER BY id` direction for the originals read, and returns fresh objects per statement. M0 behaves as claimed: on the round-1 head its 3 cells are green, with B in the fetched set at 23 and absent at 24 and 25.
- **G188-F4 INFO (pre-existing, unchanged):** the by-id paths are untouched by this commit (no hunk).

## What passed (measured)
- **Q1 scope:**
  - `git diff --name-only d03b0304 f702d4da` lists exactly the 5 files in the READY. Against the base, 7 files.
  - verification.ts lines 1-480 (certificationEligibility, selectVerifiableRow, siblingCertification, scopeTenantFields) are **byte-equal** between r1 and r2. Control: base vs r2 over the same range differs.
  - The round-1 test files `ks1561-verify-original-registrant-certifier.test.ts` and `ks584-p3-verify-list.test.ts` (the :195/:213 edits) are unchanged between r1 and r2.
  - Touched hunks, verification.ts:
    - the new block after `VERIFY_ROWSET_LIMIT` (ORIGINAL_ROWS_LIMIT, rowSetMayBeCut, withOriginalRows, ORIGINAL_ROWS_POOL_SQL, readOriginalRows, readOriginalRowsNarrow);
    - the crossTenantLookup merge (+7);
    - verify-file (+1);
    - /verify (+1);
    - chain-first (1 line replaced by 5).
  - Touched hunks, verificationV2.ts:
    - the imports;
    - the localRowsByHash wrap;
    - the registry SQL (DISTINCT/ORDER BY tenant_id becomes GROUP BY plus ORDER BY MIN(created_at), tenant_id);
    - the per-tenant merge.
  - v2's `presentable` filter and rule (A) are untouched.
  - All 6 row-set reads (`LIMIT ${VERIFY_ROWSET_LIMIT}`: v1 at :682, :790, :1251, :1318; v2 at :301, :344) are followed by `rowSetMayBeCut`. Counted from `tmp_r2/v_r2.ts` and `v2_r2.ts`.
- **Q2 F1 on PG15:** see G188-F1. 5 paths × n ∈ {23, 24, 25} at all three versions match the expected table exactly, plus n = 22.
- **Q3 bounds and edges (real PG, per-request statement counts):**
  - **Trigger:**
    - B + 22 copies (23 rows): **0 originals reads** on all 5 paths.
    - B + 23 copies (24 rows, B inside): **1 read on each path**, and B is listed once (merged by id).
    - Control: mutant G1 (dedupe dropped) turns that cell red (v2 count 2).
    - Base and r1 issue 0 reads everywhere.
  - **TIE24** (24 tied uncertified originals + 24 later certified copies): /verify presents no certification; v2 lists the 24 originals; no warning.
  - **TIE25:** the same, plus **the warning naming KS-1561**; v2 lists 24 and leaves out `g-tie-25` (the first 24 by id are kept).
  - **TIE25-OWNER-LAST** (the 25th original by id belongs to A): head presents **no** certification. A full set would make A's copies eligible, so the cut **narrows** as the PR states.
  - **TIE25-OWNER-FIRST** (the 1st original belongs to A): head presents A's certification (same owner as an original, the P side).
  - **OLDCERT** (B certified before every later copy, 25 copies): `gcert-b-old` on /verify, verify-file and v2. Base and r1 show `gcert-a-25`.
  - **INSIDE** (3 copies): B, 0 originals reads.
- **Q4 v2 cap on PG:**

  | Cell | Base | Round 1 | Round 2 |
  |---|---|---|---|
  | CAP-8 | 7 latecomer certs | B only | B only |
  | CAP-9 | 8 latecomer certs | 8 latecomer certs | B only |
  | CAP-10 | 8 latecomer certs | 8 latecomer certs | B only |
  | CAP-LATE | 8 latecomer certs | 8 latecomer certs | 8 latecomer certs (the stated residual; no worse than base or r1) |
  | CAP-LATE-LOWID | 7 latecomer certs | B only | 8 latecomer certs |

  - CAP-LATE-LOWID: worse than r1 and not worse than base (G188-F6).
  - Ranking by MIN(created_at) presents a certification base did not in 1 v2 cell, CAP-ORIGCERT, and that certification is the original's own (G188-F7a).
- **Q5 direction:** 3 of 43 (G188-F7). Swapped control 33 of 43.
- **Q6 cost:** see G188-F5. The row-set read (unchanged) uses `idx_documents_content_hash` at 5,000 rows. The originals read uses it only for small groups.
- **Q7 mocks and red-first:** the new file at f702 passes **30/30**. With the r1 route blobs overlaid, it gives **18 failed, 12 passed**. All 18 fail by assertion: 0 `error TS`, 0 module errors in `runs_r2/mock_new_r1.txt`. That reproduces the seat's 18/12, and the same 12 cells are green (M0 ×3, the five 23-copy cells, the under-limit P cell, N-SPLIT, CAP-8, the residual).
- **Q8 mutants** (committed bytes; each anchor count asserted; 0 TS errors; every file restored sha256-equal). Counted from `runs_r2/mutants_r2.json`: **9 valid, 8 killed, 1 survived (G4, G188-F8)**.

  | Mutant | Change | Mock red (of 30) | PG red (of 20) |
  |---|---|---|---|
  | M1 | trigger off | 16 | 8 |
  | M3 | threshold 25 | 16 | 8 |
  | M5 | tie bound 1 | 2 | 2 |
  | M6 | MIN to MAX in all three originals reads | 15 | 8 |
  | M11 | tenant rank back to tenant_id | 2 | 2 |
  | G1 | id dedupe dropped | 3 | 2 |
  | G2 | tie cut dropped | 1 | 1 |
  | G3 | crossTenantLookup not wired | 2 | 2 |
  | G4 | merged originals first | 0 | 0 (survivor) |

  - M1 and M3 have the same effect: a read never returns more than 24 rows.
  - My M6 is wider than the seat's (all three reads, not the caller read only), so its 15 differs from the seat's 10.
- **Neighbours at f702:** the following suites pass: the seat's new file; ks1561-verify-original-registrant-certifier; ks584-p3-verify-list; ks584-verify-row-selection; ks584-p3-auth-error-classification; ks1557-trusted-certification-evidence; the two ks1628-successor suites. My round-1 matrix gives 12/13: N-TRUNC is now green, and the one red is N-SPLIT (F2).
  - `tsc --noEmit` with the gate tsconfig: 9 errors, the same count as round 1 and all from the stale shared build. **0 are in routes/verification\*.ts.** Control: the same output lists 9 errors in other files, so the instrument fires.
- **Q9 title/body:**
  - The title "Refs KS-1561: verify shows a certification only for the holder of the original registration" is **91 chars**, at most 92, and starts with "Refs KS-1561:". Source: the round-1 commit subject plus Seat F 30th's read-back record (`pr/patch_real.out`: "title unchanged", "readback_equal: true").
  - The body's round-2 section in the seat's sent body (`patch_real.json.newbody`, :131-:139) states the bound ("at most 24 rows tied … 25 are asked for … logs a warning") and the residual ("a tenant whose registry row was written late …").
  - **Read via the GitHub API: UNMEASURED.** The repo is private, the anonymous API returns 404, and I did not borrow any `gh` identity (hard rule 5).
- **Q10 merge:** rc 0, tree `6eb2b847` on develop `536642104002`, the same at the end.

## NOT tested
- Node 24, kintsugi or demo, the live verify after deploy, real Platform S traffic, and the four platform suites.
- The whole originate suite in a valid environment. In my harness it gives 73 suites failing to load: stale `@secuura/shared` build (`signEmitterHop`, `zod3-compat`, `documents/default-type`), the real-app KS-1032/1041 suites, and the KS-1612 migration-text suite. None is in the PR's files. The seat reports 2451/2451 on its install; I did not reproduce that. Lint not run.
- The chain-first branch on real PG. It is covered only by the seat's mock cell and by reading its code (it uses `readOriginalRowsNarrow`; mutant coverage comes through the shared trigger).
- Production `documents` table size per tenant, and how often hashes have 24+ or 300+ rows (decides G188-F5's real cost).
- Whether a registry row is written late in practice (decides how often G188-F6 and G188-F7(c) occur). Base's `LIMIT 1` pick in G188-F7(c) depends on heap order and is not deterministic in general.
- EXPLAIN of the v2 registry `GROUP BY … ORDER BY MIN(created_at)` on a large registry. RLS or pool-mode plans, where `documents` is shared across tenants and the backward walk in G188-F5 would cross every tenant's rows (read, not measured).
- Reachability of 24 certified copies, or of 9+ tenants per hash, through the real register and certify APIs.
- PR body and title on GitHub itself (see Q9).

## Plain answer for Kam
- The fix works. Someone who registers your file later and certifies 24 or more copies of it can no longer make verify say "certified by them". I checked that on a real database for every way of verifying.
- Compared with today's develop, it shows a certification in only 3 of the 43 cases I ran. Two of those are the original registrant's own certification, which the old code hid by accident. One is a latecomer's certification in a rare setup where the original's registry entry was written late (a known, stated limit). That is why I am flagging it for you instead of a plain merge.
- One cost note: for files registered hundreds of times, the new "find the original" step reads through the whole documents table on each verify. That is about 30 milliseconds on a 300,000-row table, and more on bigger ones. It is a cheap fix to make later, not a correctness problem.
- The tenant-ordering change helps in some cases and hurts in a rarer one. Neither ordering is perfect, and this is the one Wednesday chose.
