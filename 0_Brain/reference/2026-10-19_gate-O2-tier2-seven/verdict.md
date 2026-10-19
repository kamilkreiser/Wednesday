#1591 GO a992894cdbf74e7eaf7b93cb280520d77c442948 (KS-1620 i1; one product hunk info.ts:134, 4 cells; mutants killed; NOTE: ticket body not readable by this gate, so the no-ellipsis comparison is unconfirmed)
#1592 GO ac758817103cfb1208a27fc0f508250512556b03 (KS-1621 1/2; test only, product byte-unchanged; F5 red under the ?? to || tamper)
#1593 GO 587fe9dbf0a77bc54e19b3227ec9394280ce4376 (KS-1621 2/2; test only, product byte-unchanged; D4 red under two tampers)
#1594 GO 2cda8fe5243f0308c85f44f9d6261125db9583db (KS-1627 2/2; test only, product byte-unchanged; R3 red under the always-refuse tamper)
#1595 GO 46795487b69cafbc96012f9e9b792551b19d5ff5 (KS-1526; one product hunk logger.ts:32-33; mutants killed; NOTE: author's api-gateway figure not reproducible, see below)
#1600 GO 6499cce63ab90bd28c566c13a0f722947136029d (KS-1544; one product hunk index.ts:558; mutants killed; NOTES on random-uuid tie-break, text-only pin, no plan check)
#1601 GO c08b786603c3a30fcc1a985e0effdab9041c9923 (KS-1525; test only, product byte-unchanged; G1 and G10 each red under their tamper; G7/G8 omission confirmed by calling the real function)
sha256/16: acac7c86cb6e54d2

# GATE O2 verdict: seven tier-2 PRs, round 1 of 2 (2026-10-19, Sonnet)

All seven heads equal the brief's (fetched with `git fetch refs/pull/*/head` into my own shared clone; origin/develop = 78cb3c3939e319332e387ffecb075a169edd4a39, tree 1ca89b2b5b7280ced0760012b09338dec94766aa, re-read at fetch). No P1/P2 finding. Every verdict is GO; the NOTES below are non-blocking.

Merge-prediction base. #1591-#1595 branch from 83ed01af70fd, #1600/#1601 from 78cb3c3939e3. Each was merged onto the LIVE develop with `git merge-tree --write-tree` (no conflict, rc 0 each). All seven were then chained onto develop in numeric order, and the five tier-1 PRs from gate O1 on top of that.

## Merge-prediction table (live develop 78cb3c393, tree 1ca89b2b5b72)
| merge | tree id | conflicts |
|---|---|---|
| develop + #1591 | c44ff0dfda170667c8c1f7ee03a3386c9b91546c | none |
| develop + #1592 | 1dbb172033c8d1f43ef4ab385b07aac75ed3d559 | none |
| develop + #1593 | 38baa8c47b2cd6312279723f5914806efafc9e32 | none |
| develop + #1594 | 2e3f77bf2830de89baf85aa5769dc512d48c5ce6 | none |
| develop + #1595 | 4a15f7530fb9d6171145e8f616288023699eedb2 | none |
| develop + #1600 | a0a5c286132e99614ebf7c068832f6fd7bbc51fd | none |
| develop + #1601 | 5c881d3a501b40bd46b2b58b5ef1447b2cde1dd0 | none |
| ALL SEVEN chained (commit 4070e7a93ac0350a8e723908ee50fdcb3e63066f) | 0ca7bc0e8363d5e950df8c12f648474d00424f7e | none (the chain's first step equals the single #1591 tree, a control) |
| ALL SEVEN + O1's #1597 #1590 #1596 #1598 #1599 | 4a7cd99d9fce975bf9de409c213c2e268103aa95 | none |

File-disjointness: pairwise among the seven, 0 shared paths (control: injecting a duplicate path made the same awk report it). Against the O1 five, 0 shared paths. No literal collision. Same-service neighbours (not collisions): #1598 middleware/auth.ts and #1593/#1594/#1595 are all api-gateway; #1596/#1597 and #1592 are all originate. Their suites were run together on the 12-PR tree (below) and are green.

## #1591  a992894cdbf74e7eaf7b93cb280520d77c442948
FOUND: 2 files: new test ks1620-get-info-bounds-the-relayed-gateway-text.test.ts (4 cells) and mcp-server/src/tools/info.ts, one hunk (`refusalText.slice(0, 200)`, info.ts:134 plus a comment line). Nothing else.
TESTED: Red-first (develop product + the PR's test): B1 and B2 fail by AssertionError (note equality), B3 and B4 pass. Mutants on the predicted tree: slice(0,199) killed by B1,B2,B3; slice(0,201) killed by B1,B2; no slice killed by B1,B2. A fourth mutant (slicing only the string branch while the outer slice stays) passes all four cells, but it is an EQUIVALENT mutant (the outer slice still bounds both), not a gap. mcp-server on the predicted tree 15/15 (develop 11/11, so +4).
HOW: `vitest run --root services/mcp-server` on the all-seven tree; mutation by an exact-one-match replace script.
Ticket question (brief item 6): I could NOT read the KS-1620 ticket (no Linear read in this gate). The only text I could see is the author's own SCREEN_7 line 49: "the bound of 200 and the absence of an ellipsis marker are my choices ... Confirm against the ticket body". So "differs from the ticket's example, not from the ticket" is UNCONFIRMED by me.

## #1592  ac758817103cfb1208a27fc0f508250512556b03
FOUND: 1 file, 5 added lines in originate ks1333-sync-writers-persist-null-not-zero.test.ts (cell F5). Product files byte-unchanged (diff stat lists the test file only).
TESTED: The named product line is anchorStateSync.ts `blockHeight: prior?.blockHeight ?? null` (line number about 190). Tamper `?? null` to `|| null` on the predicted tree: F5 fails by assertion; F1-F4 and the other 14 cells stay green. Untampered, originate on the predicted tree 1443/1443 (develop 1442, so +1).
HOW: jest (originate uses jest, not vitest) with `--rootDir`.

## #1593  587fe9dbf0a77bc54e19b3227ec9394280ce4376
FOUND: 1 file, 12 added lines in api-gateway ks1543-document-types-catch-logs-the-error.test.ts (cell D4). Product files byte-unchanged.
TESTED: Tamper A, constructor name replaced by the literal 'object' in routes/verification.ts:1082: D4 fails (and the older D1). Tamper B, `Object.keys(err)` to `Object.values(err)` (leaks SECRET-VALUE-ks1621): D4 fails (and D1). 8 other cells pass in each run. D4 is therefore not the unique killer of either tamper, but it is a killer and its secret-leak assertion is live.
HOW: single file via vitest verbose, tamper on the all-seven tree.

## #1594  2cda8fe5243f0308c85f44f9d6261125db9583db
FOUND: 1 file, +24/-1 in api-gateway ks1627-info-reader-real-redis-fallback-refuses.test.ts (a vi.mock of ioredis plus cell R3). Product unchanged.
TESTED: The route under test is services/health.ts (createHealthRoutes, line 53), NOT verification.ts; my first tamper (verification.ts) did not bite, which is how I found out. Tamper `isRedisAvailable?.() === false` to `true` (always refuse): only R3 fails (R1, R2, C1, C2 stay green). Opposite tamper to `false` (never refuse): R1 and R2 fail, R3 stays green. So R3 pins exactly the Redis-mode 200 and nothing else.
HOW: single file via vitest verbose.

## #1595  46795487b69cafbc96012f9e9b792551b19d5ff5
FOUND: 2 files: new test ks1526-production-file-logs-carry-the-entry.test.ts (4 cells) and api-gateway/src/utils/logger.ts, one hunk (`format: combine(json())` on both File transports, lines 32-33).
TESTED: Red-first on develop product: L1 and L2 fail by assertion (the files hold `undefined`), L3 and L4 controls pass. Mutants: drop format from error.log only, killed by L1; drop it from combined.log only, killed by L2; json() replaced by simple(), killed by L2 (L1 not hit because that mutant touched combined only). Suite on the predicted tree 1112/1112 (develop 1106, so +6 over the three api-gateway PRs: 1+1+4).
HOW: as above. The cells chdir into os.tmpdir() mkdtemp folders (see NOT tested).

## #1600  6499cce63ab90bd28c566c13a0f722947136029d
FOUND: 2 files: new test ks1544-audit-log-is-paged-in-a-total-order.test.ts (4 cells) and tenant-provisioning/src/index.ts:558 (one hunk, `ORDER BY created_at DESC, id DESC`). Base is 78cb3c3939e3, so already the live develop.
TESTED: Red-first on develop product: O1 fails by assertion (`contain 'ORDER BY created_at DESC, id DESC'`), O2-O4 pass. Mutants: `id ASC` killed by O1; `id DESC, created_at DESC` killed by O1 and O4; `created_at ASC` killed by O1 and O4. tenant-provisioning on the predicted tree 21/21 (develop 17/17, so +4).
HOW: as above (pg replaced by a recorder, so the cells see the SQL string, not rows).
Brief item 4 questions (NOTES, not NO GO):
1. Tie-break `id`: confirmed `id UUID PRIMARY KEY DEFAULT gen_random_uuid()` (migrations/003_platform_tenancy.sql:50), so ties are ordered by a random value: paging is deterministic (no repeat or skip between windows), NOT chronological. The one consumer is api-gateway routes/platform.ts (~lines 405-430): it reads the platform half in sequential windows by limit/offset (KS-1512), collects, then re-sorts the merged list in memory with `created_at` only (platform.ts ~line 495, stable sort). The consumer needs only a stable total order across windows, which this gives it; it does not need chronology within a timestamp. Residual: rows with the same created_at show in random-uuid order, identical on every request.
2. Same defect class outside the PR's scope: the gateway's own audit_logs query (platform.ts ~451) is `ORDER BY created_at DESC LIMIT $1` with no tie-break, but it always reads from row 0 and slices after the merge, so a tie can still reorder across requests (a page boundary can repeat or skip a tied row). Out of scope, mention to author.
3. Does a test that pins the ORDER BY text satisfy a ticket whose own test spec asks for the two-window behaviour? I could not read the ticket. As built, O1 pins TEXT only; no cell runs two windows (the `pg` double returns fixed rows, so nothing proves the windows do not overlap or skip). The code claim (ORDER BY ends in the PK) is exactly what the PR states, so the PR does not claim more than it does, and the hunk is correct; but if the ticket's test spec requires the two-window behaviour, this is the text-pin substitute, not that test. NOTE.
4. Query plan: not done (no database). Migrations hold no index on platform_audit_log (grep found none; control: the same grep finds other tables' indexes). The sort is a scan-and-sort with or without the extra key, so adding `id` should not change the plan class; unmeasured.

## #1601  c08b786603c3a30fcc1a985e0effdab9041c9923
FOUND: 1 file, +12 in security row-converters.test.ts (three cells: RED G1, CONTROL G1 null, CONTROL G10). Product unchanged.
TESTED: Tamper `Boolean(r.is_active)` to `r.is_active !== false` (converters.ts:171): RED G1 and the null control fail. Tamper to `=== true`: CONTROL G10 ("t" reads active) fails. Untampered security suite on the predicted tree 346/346 (develop 343, so +3).
G7/G8 (brief item 5): called the real rowToApiKey with ids '' / 'k1' / undefined / null: id '' comes back '' (not refused), undefined comes back absent, null comes back null; connector_id '' comes back ''. Confirms R's measurement that the function returns '' for empty-string ids, so G7/G8 as refusals would be wrong tests. The same probe shows is_active "f" and "false" (text) read ACTIVE (Boolean of a non-empty string); the test's comment names only "t". Real pg returns booleans for a bool column, so this is theoretical; not in this PR's scope.
HOW: probe file written then removed inside my clone.

## Author figures vs measured on the PREDICTED tree (all seven chained)
| suite | author | measured predicted | develop alone | delta |
|---|---|---|---|---|
| mcp-server | 15/15 | 15/15 | 11 | +4 ok |
| tenant-provisioning | 21/21 | 21/21 | 17 | +4 ok |
| security | 346/346 | 346/346 | 343 | +3 ok |
| originate (jest) | 1406/1406 | 1443/1443 | 1442 | +1 ok; absolute differs because develop moved (R's own later mail says 1442 base) |
| api-gateway | 1196 / 1199 | 1112/1112 (113 files) | 1106 (112 files) | +6 ok; the ABSOLUTE 1196/1199 does NOT reproduce in my environment (about 90 tests fewer), cause not found |
12-PR tree: api-gateway 1117/1117, originate 1462/1462 (no cross-PR failures).

## NOT tested
- Ticket bodies (KS-1620, KS-1544, KS-1525, KS-1621/1627): no Linear read; items 4's spec question, and 6, rest on the code and the author's own notes.
- No query plan, no real Postgres/Redis: #1600 and #1594 use doubles.
- The api-gateway absolute test count gap (1196 vs 1106) is unexplained; I did not bisect which test files the author's run included.
- Branch-level hygiene (commit trailers, PR bodies, CI) not read.
- #1595's cells create temp folders under the OS temp dir (`ks1526-*`, outside my scratch folder) and do not remove them; one real `logs/` write per cell, no project paths touched. Hygiene NOTE only.
- tsc and eslint not run on the seven.

## Severities
- NOTE (low), platform.ts ~451: audit_logs query has no tie-break (pre-existing, adjacent to #1600), same class as KS-1544.
- NOTE (low), ks1544-audit-log-is-paged-in-a-total-order.test.ts O1: text pin, no two-window cell.
- NOTE (info), converters.ts:171: text "f"/"false" read active; pre-existing.
- NOTE (info), #1595 temp dirs not cleaned.
- NOTE (info), api-gateway absolute figure unreproduced.

MODEL: claude-sonnet-5-5 (routing receipt: "tier-2 gate row (batched seven, round 1 of 2) -- P1-P4 no -- gauge 24%")
WALL-CLOCK: 13 min 18 s (11:41 to 11:54 AEDT, 2026-10-19)
