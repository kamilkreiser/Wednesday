GO WITH NOTE — PR #1576 (KS-1114 follow-up) at head 252e53d633d7fda0becd0eefc2ad65525e9e8544
The product line is correct and every mutant is killed; the brief's NULL premise is wrong, but behaviour did not change (NULL was hidden before and is hidden now, and no writer can store NULL); tabs, newlines, CR and NBSP are not trimmed (the narrowing, recorded).
53448c83acdb1797

Gate F1, tier 1 FULL, round 1 of 2. Client: Secuura. Findings only. Nothing was pushed, commented or merged. The project checkout was only read.
Work was done in my own clone (git clone --shared of 2_Project_Files, fetched with that checkout's core.sshCommand) under the session scratchpad, on my OWN PostgreSQL 15.14 (Homebrew) cluster on port 56152, which I checked was free first. I never used 55473 or 55418. The cluster is now stopped. Raw evidence and every script are in `evidence.tgz` next to this file (ev/ and scripts/).

Refs re-read by ls-remote at 23:14 AEDT: develop = 1f73d7ac8cc17add318601c6c572bcace3d5a596 (matches the brief). pull/1576/head = 252e53d633d7… (matches). PR base = 9251ae54d (merge-base with develop).

## FOUND

| # | Sev | Where | Finding |
|---|---|---|---|
| N1 | NOTE (brief premise) | verification.ts:1466 at 833984fc9 / develop; :1467 at head | **The previous predicate was NOT NULL-safe.** At 833984fc9 (and at 9251ae54d and live develop) it reads `AND d.status NOT IN ('draft', 'revoked')`. On a real PG, `NULL NOT IN (...)` evaluates to NULL, so a NULL-status row is dropped. **Measured through the real route: a NULL-status title hit answers the not-found body BEFORE (833984fc9) and AFTER (head), as superuser and as secuura_app, in the default tenant and in a vouched tenant B.** So behaviour is unchanged: NULL fails closed (hidden) both times. **NULL is also unwritable.** `documents.status VARCHAR(20) NOT NULL DEFAULT 'draft'` comes from migrations/001_initial-schema.sql:104. None of the 51 migrations alters `documents.status`, drops its NOT NULL or adds a CHECK. information_schema on the migrated DB says is_nullable=NO, and a NULL insert is refused with not_null_violation. The writers (documentRepo.ts:619/:648 CASE → `${updated.status}` or the existing status; certificationRepo.ts:199; certifications.ts:606 `'certified'`; adminConfig.ts:1927) write only fixed lower-case values or the existing status. Any NULL would hit the constraint. The code comment at :1460 ("documents.status is NOT NULL (migration 001), so NOT IN cannot silently drop a NULL row") is accurate. |
| N2 | NOTE (narrowing, as stated) | verification.ts:1467 | `btrim()` with no second argument trims ASCII spaces only. These variants stay **HITs**: `"\tdeleted"`, `"revoked\t"`, `"\ndraft"`, `"expired\n"`, `"revoked\r"`, `"deleted<NBSP>"` and `" \trevoked\t "`. They were HITs at 833984fc9 too, so nothing regresses. PG confirms it directly: `btrim(E'\tdeleted')` keeps the tab, and NBSP is kept. No writer stores such values (see N1). This is recorded, not a defect. |
| N3 | INFO (comment) | verification.ts:1445 | The summary line still reads "Absent, another tenant's, draft, revoked and the sentinel all answer ONE not-found body". It does not mention deleted or expired, although :1440-1441 does. This is cosmetic. |
| N4 | INFO (not this PR) | ks1557-verify-trusts-certification-evidence.integration.test.ts:241 | Run as secuura_app with MULTI_TENANCY_ENABLED=true, the cell "a caller in ANOTHER tenant reads the registry path (crossTenantLookup in pool mode)" fails (`isCertified` undefined) in my environment. **The same cell fails identically on live develop 1f73d7ac**, so #1576 did not cause it. It is a hash-strategy path, not the title lookup. With MT=false, ks1119 + ks1557 as secuura_app pass 35/35, and as superuser ks1557 passes 17/17. The author's "ks1557 green as secuura_app" holds only for the MT mode they did not state. |
| N5 | INFO (pre-existing) | migrations/001 indexes | `documents` has no index on `title`, so the title lookup is a Parallel Seq Scan before and after the change (see step 7). This is not introduced here. |

No BLOCKER, no MAJOR, no MINOR.

## TESTED / HOW

1. **Diff by hunk at the head** (`git diff 9251ae54d 252e53d63`): 3 files, +178/-8, and nothing else.
   - `Blockchain/Dev/services/originate/src/routes/verification.ts`: two hunks. One is the comment at :1440-1441. The other is the predicate at :1467, `AND lower(btrim(d.status)) NOT IN ('draft', 'revoked', 'deleted', 'expired')`.
   - `…/__tests__/ks1114-title-lookup-hidden-statuses-case-and-space.test.ts` (new, 169 lines).
   - `…/__tests__/ks1114-anonymous-title-lookup-one-tenant.integration.test.ts`: one hunk, the T11 re-pin at :272-282. `deleted` moves from HIT to MISS, and 'expired' plus the case and space variants are added to MISS.
2. **NULL semantics**: covered in N1. My probe suite `gatef1-probe.integration.test.ts` copies the T11 file's harness verbatim (real verificationRouter, real resolveRequestTenantId, tenantGucContext and per-request Prisma) and adds recording cells. It ran on the 833984fc9 tree and on the head tree, each as superuser and as secuura_app (RLS FORCE on `documents`). For the NULL cell, the suite drops NOT NULL on my DB only, inserts the row and puts NOT NULL back in a finally block. SQL-level: `(NULL NOT IN ('draft','revoked')) IS NULL` = t, and the head form is also t.
3. **Reply shape** (head, both roles): every hit is exactly `200 {"verified":false,"checks":{"documentExists":true}}`. Each of the 4 hidden statuses × 8 variants answers byte-identically to the absent-title body: lower, UPPER, Title, aLtErNaTiNg, leading space, trailing space, 3-space padded Title and leading-space UPPER. The absent-title body was measured live in the same run and equals MISS_BODY. At 833984fc9, 30 of those 32 were HITs; only exact `draft` and `revoked` were hidden. The visible set stays HIT: certified, signed, anchored, anchor_failed, pending_signature, CERTIFIED, " signed ", erased, "", " ", revokedx, draft_x, undeleted. The non-space whitespace cells are covered in N2. Table: ev/probe_table.txt.
4. **Tenancy**, both roles, MT=true:
   - a tenant-B title from an anonymous caller is the not-found;
   - the same title from a vouched-B caller is a HIT;
   - a default-tenant title from a vouched-B caller is the not-found;
   - tenant-B `" Deleted "` and `"EXPIRED"` from a vouched-B caller are the not-found (they were HITs at 833984fc9);
   - `absent@B` is byte-identical to `absent`.
   The T11 suite's own T2, T2b and T3 pass in both roles.
5. **Red-first and green at the live tip** (my own PG):
   - tipgreen = merge-tree of develop 1f73d7ac + #1576, committed in my clone as 11f8f638, tree 34356600.
   - tipred = the same tree with verification.ts restored to live develop's bytes and the PR's tests kept.
   - Unit: tipred **4 fail / 3 pass** (the four RED cells: deleted, expired, case, spaces) → tipgreen **7/7**.
   - T11 integration: tipred **16/17** (T11 red) as superuser and as secuura_app → tipgreen **17/17** in both roles. Also 17/17 as secuura_app with MT=false.
   - At the bare head: T11 17/17 in both roles, and unit 7/7.
   - Originate full unit suite: tipgreen **1387/1387** (111 suites) against develop 1380/1380 (110 suites), which is +7 = the new file. `tsc -p services/originate --noEmit`: 0 errors at tipgreen and at develop.
6. **Mutants** on verification.ts:1467, each applied to a copy of the head file (ev/unit_*.json, ev/int_*.json):

| Mutant | Unit cells that fail | T11 integration | Result |
|---|---|---|---|
| M0 revert to develop's line | deleted, expired, case, spaces | T11 | killed |
| M1 drop 'expired' | expired, case, spaces | T11 | killed |
| M1b drop 'deleted' | deleted, case, spaces | T11 | killed |
| M1c drop 'draft' | case, spaces, "control - draft and revoked stay hidden" | T10 + T11 | killed |
| M2 drop lower() | case, spaces | T11 | killed |
| M3 drop btrim() | spaces | T11 | killed |
| M4 comment-only control | none (7/7) | 17/17 | survives, as a control should |
| M5 btrim(lower()) (equivalent) | none (7/7) | 17/17 | survives, as an equivalent mutant should |

7. **EXPLAIN** on my DB, seeded with 200k rows across 2 tenants and an 8-way status mix, after ANALYZE. Before and after, the plan is the same shape: Limit → Gather → Parallel Seq Scan on documents, with every predicate in the Filter. This holds as superuser and as secuura_app under RLS (the policy quals are inlined in the same Filter). The function wrap does not change the plan. No index was usable before either: `idx_documents_status` is not usable for `<> ALL`, and there is no title index. Estimated cost rises 8969 → 9594 (superuser) and 10845 → 11470 (RLS). Measured execution was 12-18 ms either way, with no regression. The seed rows were deleted afterwards (0 left). ev/explain.txt.
8. **Merge prediction** against live develop 1f73d7ac alone. Develop-side changes since 9251ae54d touch only preflight.sh, the ks1547 test, api-gateway platform.ts and the ks1545 test. None overlaps #1576.
   - Pairwise overlap between #1573, #1574, #1575 and #1576: none.
   - #1576 alone: clean, tree 34356600.
   - All 24 orders of the four PRs, merged in sequence with `git merge-tree --write-tree`: every order is clean and every order ends at **tree d753dcc43754b945a7eef45f1a90c610e6aad68c**. **R's prediction d753dcc43754 is confirmed.**
   - Planted conflicting control: a develop-side commit that rewrites the same product line gives merge-tree rc=1 with CONFLICT (content) in verification.ts. The conflict check can fire.

## NOT tested

- Preflight legs (none run by me; the author skipped 3, 4 and 8).
- A live or deployed stack, the gateway's per-IP limiter, and the real gateway vouch path. Vouching is simulated by the T11 harness's own header, as in the suite.
- PostgreSQL 18 (I used PG 15.14 only).
- Production data: I did not survey the statuses actually stored, so whether any tab- or NBSP-padded status exists in a real DB is not measured.
- I did not reproduce the author's MT mode for ks1557.

WALL-CLOCK: 17
