VERDICT: GO at head e9630de51c22... (tier 2, round 1 of 2; landing tree b8df98cfb692eaa02819b4c3fb441e761fbf508d on develop 513371a34be58af9e740b82ea26795155c7bd0b4; 0 blockers, 2 notes)

## BLUF
GO. Every clause I mutated reds exactly its intended cell and nothing else; every mutant compiled (tsc rc 0 before counting); the controls stay green under the clause mutants and go red when the heal or the persist is disabled, so none is vacuous. The v2 companion row is load-bearing for the settled/failed cells and for G1/G2. Landing tree equals Wednesday's figure, the diff against develop is test files only, and the full originate suite at the landing is 133 files, 1,555/1,555. KS-1676 stays `Refs` (the `!chain` row is unpinned, as disclosed).

## Findings (notes, not blockers)
1. NOTE - the v2 companion is NOT load-bearing for every v2 cell. In the simulated/malformed file the target is itself a stale-pending row in G3 and C1, so a fetch happens without the companion: G3 still kills its mutant, and C1 stays green, with the companion removed. It is load-bearing for G1 (stored simulated) and G2 (stored malformed txHash), and for all of S1-S4 and C1 in the settled/failed file. The header comment of the simulated file says every cell lists the companion, which is true, but only two of its four cells need it. Cosmetic.
2. NOTE - the `expect(r.fetchCalls).toBe(1)` line in the v2 cells is the canary that makes a dropped companion visible: with the companion removed and that line kept, S1-S4 and G1/G2 go red at the untouched tip for the wrong reason (fetch=0). Good design; I mention it so nobody removes the line as redundant (with it removed AND the companion removed, G1 and S1/S4 go silently green under their tamper, see Q2).
3. Not a finding: author's A4 wording point (a test-only READY's "fails at the untouched tip" template string) is outside this gate; the files pass at the tip as the author says (19/19).

## FOUND / TESTED / HOW

Heads re-read at start and at the end by ls-remote on the project and by rev-parse in the cache: #1644 = e9630de51c2266627bef25742c1e95826a67ae75, develop = 513371a34be58af9e740b82ea26795155c7bd0b4. Three-dot diff = 4 new files under Blockchain/Dev/services/originate/src/__tests__/, +595; `git diff --stat develop HEAD` excluding that directory is empty after the merge (zero product bytes).

Setup: clone --shared of the cache into the gate scratchpad, detached at the head, node_modules cp -R -P'd from the project into the clone (symlinks relative, so @secuura/shared resolves inside the clone), packages/shared built with tsc (rc 0). Baseline: originate `tsc --noEmit` rc 0; the 4 files at the tip, 19/19 pass.

### Q1 Clause coverage (15 mutants, I planted them myself; line asserted to occur once before editing; tsc --noEmit rc 0 on EVERY mutant before counting; restored by git checkout with sha256 equality each time)
Each mutant ran against all four files; "red" = the only failing cell of 19.
| Mutant (one clause weakened) | tsc | Only cell red |
|---|---|---|
| v1 verification.ts:435 drop `anchored === true` | 0 | v1 settled/failed S4 |
| v1 :435 drop `status === 'confirmed'` | 0 | v1 settled/failed S3 |
| v1 :436 drop `status === 'failed'` | 0 | v1 settled/failed S1 |
| v1 :436 drop `status === 'anchor_failed'` | 0 | v1 settled/failed S2 |
| v1 :432 stored `simulated === true` -> false | 0 | v1 simulated/malformed G1 |
| v1 :434 drop stored txHash regex | 0 | v1 simulated/malformed G2 |
| v1 :455 drop `chain?.verified !== true` | 0 | v1 simulated/malformed G3 |
| v1 :455 drop incoming txHash regex | 0 | v1 simulated/malformed G4 |
| v2 verificationV2.ts:133 drop `anchored === true` | 0 | v2 settled/failed S4 |
| v2 :133 drop `status === 'confirmed'` | 0 | v2 settled/failed S3 |
| v2 :134 drop `status === 'failed'` | 0 | v2 settled/failed S1 |
| v2 :134 drop `status === 'anchor_failed'` | 0 | v2 settled/failed S2 |
| v2 :130 drop stored `simulated === true` | 0 | v2 simulated/malformed G1 |
| v2 :132 drop stored txHash regex | 0 | v2 simulated/malformed G2 |
| v2 :137 drop incoming txHash regex | 0 | v2 simulated/malformed G3 |
All 15: 18 pass / 1 fail, jest rc 1, the control (C1) green and no other file red. Settled/failed and stored/incoming pairs on both v1 and v2 covered, the stored-simulated and tx-shape clauses covered. One extra mutant I tried (an `|| true` on persistHealedAnchor's first guard) did NOT compile (tsc rc 2) and is not counted.

### Q2 v2 companion
Edited the test in the clone to list only the target row (the companion kept referenced so ts-jest noUnusedLocals does not fail the suite; my first attempt did exactly that and ran 0 tests, a positive-control catch), then restored.
- Settled/failed file, companion dropped, `fetchCalls` assertion KEPT: S1-S4 and C1 all red at the untouched tip (fetch 0).
- Same, `fetchCalls` assertion also removed: tip = S1-S4 green, C1 RED. With the mutant (drop `failed`, or drop `anchored`) the result is IDENTICAL (4 pass, only C1 red): the tamper no longer reds S1/S4. Companion proven load-bearing, control goes red.
- Simulated/malformed file, companion dropped, `fetchCalls` kept: G1 and G2 red at the tip. Both asserts removed: tip 4/4 green and the stored-simulated mutant leaves 4/4 green (G1 no longer kills it): load-bearing for G1. G3's mutant still reds G3 and C1 stays green: not load-bearing there (Note 1).

### Q3 Non-vacuity of the controls
Disabled the heal (status 'confirmed' -> 'pending' at v1 :471, then v2 :146; both tsc rc 0): exactly the C1 of the two files of that version red (17/2). Disabled persistence (v1 :499 `if (!row?._tenantId) return;`, tsc rc 0, shared by v2): all four C1 cells red (15/4). Each control asserts fetch count and persist (v1) or persisted ids plus the healed status/txHash (v2), so each proves the heal path ran and persisted.

### Q4 Landing
Merged the head into develop 513371a3 in the clone: tree b8df98cfb692eaa02819b4c3fb441e761fbf508d, equal to Wednesday's and the author's figure. Full originate suite at the landing: 133 suites, 1,555 tests, 1,555 passed, 0 failed, 0 pending, rc 0 (matches the author's 1,555 / 133). Each new file type-checked separately in its own program (typeRoots, types jest+node, extends the originate tsconfig): all four rc 0; controls: the file is in the program, @types/jest is in the program, and a planted TS2322 in the v1 settled file gave rc 2 and restored byte-identically (sha256).

## NOT RUN
- v2 `!chain` null guard (unpinned, author-disclosed, no compile-safe one-line mutant; Undecided row).
- v1 and v2 incoming `chain.simulated` guards (KS-1661's; not one of the KS-1676 rows I tested), v2 sameTx/sameDoc attribution, and any other non-KS-1676 branch.
- I did not read the ticket's 15-row table (only the brief and the author's claim), so I mapped clauses to guard conditions myself (15 distinct guard operands) rather than by the ticket's row ids A1..B5; the author's 15-mutant table was not independently diffed.
- Baseline 1,536 / 129 files on the untouched develop (only the landing was run).
- No integration suite, no Docker, no Postgres, no real chain/fetch, no preflight legs, no CI; unit suite mocks db/auth/fetch by design.
- Author's PR body, ticket comment, patch identity, census of 23 open PRs: not re-verified.
- No GitHub/Linear reads or writes.

## Wall-clock
Started 2026-10-19T18:09:30Z, verdict written about 18:18Z by the machine clock (about 9 minutes).

c357c27d397fca41b8b3be04f7dbc8e16b466e63cc997b474aed807f45472dda
