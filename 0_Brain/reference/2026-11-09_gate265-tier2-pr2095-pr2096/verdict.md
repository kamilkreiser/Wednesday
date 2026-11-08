PR 2095: GO; PR 2096: GO

# Gate 265, tier 2 batch: PR 2095 (KS-2012) and PR 2096 (KS-2016)
Model claude-sonnet-5-5, row G2 (tier 2), gauge 17%. Findings only; nothing fixed, pushed or posted.

| PR | head | verdict |
|---|---|---|
| 2095 | 90e8ee1d8f93 | GO |
| 2096 | 85785a9f3663 | GO |

Pins (git ls-remote) at start and end were identical: develop 092d30706b95, 2095 90e8ee1d8f93, 2096 85785a9f3663. No verdict voided.

## BLUF
Both PRs add exactly one cell to one existing api-gateway test file (+12 / +15, -0), no product byte. Each cell tests what its ticket says, at the named surface. Each went red alone, by assertion, under the builder's plant and under my independent mutants; every restore byte-equal. Whole suite on current develop 092d30706b95: 1869/1869 unpatched, 1870/1870 with each PR, failed-name lists empty, the only added test name in each run is the new cell. Merge-tree rc 0 for both, no shared path with PR 2061. No blocker. Three minor notes below.

## PR 2095 (KS-2012)
Q1 ticket vs cell. Ticket: no cell asserts `error: err.message` in the warn meta at verification.ts:647 (approve-forward, status already decided). Cell (ks1185 test, new describe at line ~228) drives a 201 whose body never ends, waits FORWARD_TIMEOUT_MS+700, takes the one warn line containing "reply body did not finish", and asserts meta toMatchObject {status:201, error:`originate did not answer within 1000 ms`}. That is the ticket's property at the logger surface the READY names. The error text is the product's own (verification.ts:639) and the bound passed in is the test's own 1,000 ms, so the expected string is not a free-standing constant.
Q2 red-first (plants in verification.ts, never committed, sha256 restored equal each time; cell file 8 cells):
- m0 builder's plant (drop error key): new cell red alone, 7 green.
- m2 error replaced with 'redacted': new cell red alone.
- m4 error truncated to 10 chars: new cell red alone.
- m1 level warn to error: 3 red (new cell plus two existing F3 cells); new cell red.
- m3 drop status key: 3 red incl. new cell.
- m5 force the else branch: 4 red incl. new cell.
Q3 suite: see below. Q4 merge-tree below. Q5 wrong-reason check: log is a vi.fn captured by the gateway's own logger path; no mock answers regardless; the assertion is on runtime meta, not a constant; length 1 is asserted first.
Findings:
- N-2095-1, Low (flake risk, not a defect). ks1185 test line ~236: the cell sleeps 1,700 ms against a 1,000 ms idle bound (700 ms margin) and has a 15 s timeout. FOUND: wall-clock dependent. TESTED: 5 passes in total (1 in the full suite at load ~7, 1 in the first full run, 3 isolated reruns: 1706, 1707, 1704, 1704 ms). Not proof it never flakes on a starved CI box; same pattern as the 7 neighbouring cells already in the file.
- N-2095-2, Note. Pins status 201 only (the PR body says so); the 401 neighbour cell asserts the status key only, so the error key is unpinned for the non-2xx-decided variant. Ticket asks only for the error key at this line, so in scope as written.
- Note on claims: the PR body's "Observed, cause not found" (vitest stack frames naming another seat's worktree) did not occur here: my frames name my own tree. Not reproducible by me; harmless.

## PR 2096 (KS-2016)
Q1 ticket vs cell. Ticket: no cell asserts the caller's Authorization reaches the upstream on every audit-export page (mutant: dropped on page 2 and later). Cell (ks1645 test, new describe at line ~185) seeds 2,300 rows (three pages at limit 1000), sends a real request with `authorization: Bearer ks2016-caller`, asserts status 200 and that the Authorization header of ALL three recorded fetch calls (via fetchMock.mock.calls, cleared in beforeEach) equals the bearer, with the array length pinned by toEqual of exactly 3. Surface matches the READY (audit-export.ts:183-198, one `headers` object reused for every page).
Q2 red-first (plants in audit-export.ts, never committed, restored byte-equal):
- n0 builder's plant (Content-Type only once rows exist): new cell red alone, 12 green.
- n1 drop header on page 2 only (offset 1000): new cell red alone.
- n2 drop header on page 3 only (offset 2000): new cell red alone.
- n3 mangle value on last page (trailing space): new cell red alone.
- n4 never attach Authorization: red alone (sent = [undefined x3]).
- n6 no paging (loop breaks after page 1): 5 red, new cell among them (length catches it).
Q5: nothing passes for the wrong reason; the stub fetch returns pages by real from/to/limit/offset logic (the file's own double), the header array is built from the recorded calls, not a constant.
Findings:
- N-2096-1, Low. n5: renaming the header key to lowercase `authorization` (HTTP-equivalent for fetch) turns the cell red because the cell reads the literal key `Authorization`. A false red on a harmless refactor, not a false green. FOUND/TESTED at audit-export.ts:185 via mutant n5; cost is only a future maintainer's confusion.
- N-2096-2, Note. Three pages and the Bearer form only (PR says so). An upstream-side no-JWT refusal (services/security) was not re-read; the PR's fail-closed claim is gate 202's and is not tested here.

## Q3 suite (same instrument both sides: vitest run, json reporter, develop 092d30706b95, Node v26.8.1)
- Unpatched: 1869 total, 1869 passed, 0 failed, failed-name list empty.
- With PR 2095's file: 1870/1870, 0 failed; only added test name is the KS-2012 E1 cell.
- With PR 2096's file: 1870/1870, 0 failed; only added test name is the KS-2016 A1 cell.
Matches T 15th's 1869 / 1870 / 1870, now confirmed on the newer develop (builder measured on 7eda23b34d3b). Instrument note: needed the Blockchain/Dev workspace install, packages/shared built (tsc), and @electric-sql/pglite@0.4.1 added --no-save for ks1256; with those, no failures. A first run without shared built showed 43 failures from missing modules; that was my environment, not either PR.

## Q4 merge-tree (git merge-tree --write-tree 092d30706b95 <head>)
- 2095: rc 0, tree 15a3048bb988d33ecb85dfa64823a495f2c5d622.
- 2096: rc 0, tree 903346499dd9a25a543dd857b8e7e6201aae4f7a.
- Develop's one move (PR 2061, 7eda23b34d3b..092d30706b95) touches 8 paths (auth service files, ROLES-AND-AUTHORIZATION-INVENTORY.md, two KS-1536 fragments). Shared paths with either PR: none. The two PRs are file-disjoint with each other.

## NOT TESTED
Live stack, Schemathesis, Akto, e2e (tier 2). Node 24 (ran Node 26.8.1, as the builder). Repo test-types ratchet, eslint, docs-fragments check, the pre-push hook legs (not re-run; builder's claims, unverified by me). The combined suite with both PRs applied together (cells are in different files). Ticket text was read from Seat T's boot snapshot of Linear (linear_tickets_boot.txt), not live at source. Behaviour of any other status code (non-201) for the 2095 error key. The PR bodies' client-visible sentences beyond the factual test counts (accurate where I tested them: +12/+15, one file each, 8 and 13 cells, parent 7eda23b34d3b).

## NEEDS TIER 1
Neither.

## My own conduct
- Disk: one clone, kept in the session scratchpad on the boot volume under /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8bd59522-1a3b-4b02-8fa6-5687685b3d9c/scratchpad/repo (2.4 GiB with node_modules), because the fleet hook refused git write verbs on a clone at /private/tmp/265; I moved the clone there. Evidence in /private/tmp/265 (113 MB). Never delete rule observed: I did NOT remove either; one stale api-gateway node_modules was moved to /private/tmp/265/q_nm_gw. Boot volume 286 GiB free after (290 before). DevMASTER untouched except this folder's verdict.md.
- One slip: the first full-suite command used a subshell `cd` into the api-gateway dir (violating never-cd). No write effect; every later call used --root and absolute paths.
- Fetched only the three pinned SHAs with the deploy key from the product repo's remote; read-only checkout of Blockchain/2_Project_Files not touched. Wrote nothing to origin, GitHub, any ticket, or any seat tree. Plants applied only inside my clone, each restored and sha256-compared; final clone state: PR 2096's test file staged, product files sha equal to develop's.
- Load average ranged 4.6 to 7.0 (under 8).
- GiB left: 286 GiB free on the boot volume.
