# QA GATE 69, TIER 2: KS-1911, PR 1883 (Secuura / Blockchain Platform K)

Findings only. Nothing fixed, pushed, commented or merged; nothing written to GitHub or Linear.

## BLUF
**GO WITH NOTES.** The scope sentence holds: E1 is green at the head, and gate 62's M18 applied byte for byte turns exactly E1 red (1 of 195, none skipped). The fixture forces Bob first, so E1 cannot pass by luck. No product file changed. The billing suite is 327 of 327 on a scratch merge with current develop. The notes are about what the three cells do NOT pin, plus one wording and one stale-comment point. None blocks.

**Conditions:** none required. Recommended, non-blocking: see N1 and N2.

## Heads
- Subject head at start and end: `4b9f13c0efc1f08f3c600f582061ff2d41e5e2c1` (refs/pull/1883/head, ls-remote), one commit on `dd583b4f7495`. Unchanged.
- Develop at commission: `2bc1a0b2b99d`. Develop when I started and at the end: `c4ced0bcb112d883b04bdfc61ac7d5a1105044b9`. It moved 8 commits and 52 files past `dd583b4f7495`, including `packages/shared/src/db/tenant-pool-manager.ts` (KS-1860). It touched nothing under services/billing and no KS-1888/1911 fragment.
- Scratch merge: tree `4497864af4f5`, dangling commit `fa59dd3ac17c` (never pushed).

Host: Darwin 27, Node **v26.8.1** (not an LTS line), vitest 4.1.12, load1 about 8.5 to 9.5 throughout (above the ~8 target; I ran at nice 10, `--maxWorkers=3`, so no timing here is comparable).

## Findings

### N1 (Note, coverage) Nothing pins a non-owner on a shared email, so a leak mutant survives all 195 cells
- Mechanism: the cells use two customers and two callers who each own one. A route that checks only the first match and admits every later one would show Alice her own customer (E1 green) and Bob his own (E2 green). That version also returns Alice's customer to a third user who owns neither.
- Measured: my mutant O3 (`.find((c, i) => i === 0 ? mayActOnCustomer(user, c) : true)`) gives **0 of 195 red**. A probe cell, "Carol (owns neither) gets 404 on dup@a.test", is green on the clean head (196 of 196) and **red under O3** (1 of 196), so the gap is closable with one cell. Probe: `evidence/gate69-probe.test.ts.txt`, run on a copy, not in the PR.
- This is outside the PR's scope sentence (M18 is an availability regression, and the PR says so). It is not a defect in the PR. It is the nearest leak the new describe block sits next to.
- FOUND by reasoning about what E0-E2 do not discriminate. TESTED by mutant plus probe. HOW: `scripts/mut.py`, `evidence/mutants.json`, `evidence/probe_clean.json`, `evidence/probe_O3.json`.

### N2 (Note, docs) Two wording points in the corrected limit sentence
- The product comment `billing.ts` lines ~118-119 still reads "a customer created before KS-1888 carries whatever userId its creator posted". The corrected fragments now say "or by any signed-in caller through the old PUT". The PR rightly leaves the product file alone, but the code comment now disagrees with the docs and wants a follow-up.
- The flow fragment's section .3 says "by anyone through the old PUT", while its section .1 and the cheat fragment say "any signed-in caller". The old route sat behind `app.use('/billing', jwtAuthenticate())`, so "signed-in" is the accurate one. "Anyone" is a small overstatement.

### N3 (Note, harness) spark_gate gave no usable agreement
- Ran FIRST: rc 0, 15 s. Head `4b9f13c0efc1` was the tip, merge-base `dd583b4f7495`, base tip `c4ced0bc`, diff 5 files +82/-2. All of that agrees with the author.
- Targeted run: **head and base both failed 0 passed / 0 failed**. Cause: `Failed to resolve entry for package "@secuura/shared"`. The harness worktree has no `packages/shared/dist`, because shared is not built there. That is a harness setup error, not a product signal. It would fail the same on any billing test.
- So I record **no agreement** on pass counts from Spark. My own runs below replace it. `evidence/spark/facts.json`, `targeted_head.log`.
- Spark's reading of "5 product files" counts the 4 HTML fragments as product files. It is a classifier artefact. The three-dot diff has no product code.

### Zero results, each with a control
- No product file changed: `diff --name-status origin/develop...pr/1883` lists the test file plus 4 fragment HTML files (2 modified, 2 added). Nothing under src/ other than `__tests__`. Control: the same diff lists the test file, so the filter sees `src/`.
- No skipped cells in any run (skipped = 0 in every JSON).

## Evidence

### (2) Cells and mutants
Route file at the head, reporter JSON, every cell counted:

| Run | Cells | Red | Which |
|---|---|---|---|
| head, clean | 195 | 0 | E0, E1, E2 all passed |
| **G62-M18**, extracted from `mutants.py` lines 74-76 by `ast` (not retyped) | 195 | **1** | exactly E1 |
| O1 own: owner check dropped, `[0]` returned | 195 | 8 | R1-R7 and E1 |
| O2 own: owner check inverted | 195 | 15 | A1-A4, R1-R7, E1, E2 |
| O3 own: first match checked, later ones admitted | 195 | **0** | survives (N1) |
| O4 own: last match admitted unchecked | 195 | 7 | R1-R7; E1 and E2 stay green |

- M18 is 1 of 195, exactly E1, and E2 stays green, as the author said. O1 gives 8 red with E1 among them, which matches the author's control mutant. The route file was restored by sha256 after every mutant and `git status` is clean.
- The E0-E2 owner-check mutants O1 and O2 are caught by E1 (and E2 for O2). O4 is caught by the older R cells only, not by E-cells.
- 195 = 192 + 3 as claimed (the file at `dd583b4f7495` has 28 literal `it(` lines plus parameterised cells; I did not recount the 192 by hand, but 195 total is measured).

### (3) E0 and the fixture
- The outer `beforeEach` runs `fake.reset()`, then the new describe's `beforeEach` inserts `cus_dup_bob` then `cus_dup_alice` into a `Map`. The fake's `listCustomersByEmail` filters `[...customers.values()]`, so the order is insertion order: Bob first.
- E0 asserts `findCustomerByEmail` returns `cus_dup_bob` and that the list is exactly `['cus_dup_bob','cus_dup_alice']`. It reads the same mocks the route uses, so if the fixture order flipped E0 goes red and E1 could no longer be read as meaningful. Verdict: sound. Limit: E0 proves the fake's order, not Stripe's real ordering.

### (4) Scratch merge with current develop
- `merge-tree --write-tree origin/develop pr/1883`: clean, rc 0, tree `4497864af4f5`. Its diff against `c4ced0bc` is exactly the 5 files.
- `packages/shared` rebuilt with tsc. The compiled `tenant-pool-manager.js` md5 changed (`161ecd79...` to `81681811...`), so the KS-1860 change was in the run. Whole billing suite: **13 files, 327 passed, 0 failed, 0 suite failures**. `evidence/merge_full.json`.
- `tsc --noEmit -p services/billing`: rc 0, no output.

### (5) Doc sentences against the code
- "old PUT /customers/:id": at `df99b04720b8` the handler took `metadata: z.record(z.string())` and called `updateCustomer(req.params.id, data)` with no ownership check, and `app.use('/billing', jwtAuthenticate())` guards the router. Any signed-in caller could write `metadata.userId`. Confirmed. "Its creator posted": the old POST passed the body to `createCustomer`. Confirmed.
- "listCustomersByEmail(email).find(...mayActOnCustomer...)" matches `billing.ts` at develop. Mutant M18's `findCustomerByEmail` still exists in `stripeService.ts`. Confirmed.
- "Both non-empty strings, exact compare, tenant where recorded": matches `mayActOnCustomer`. "GET /customers/by-email runs at all", moved above `:id`: matches the route comment.
- "211 cells" for gate 62: matches gate 62's Spark facts (head 211/0). "13 files / 327": measured.
- **KS-1909 as an audit ticket: NOT verifiable** (no Linear or GitHub access; the repo mentions it only in the two edited fragments).
- docs-fragments `check` on the scratch merge: prints `OK`, "lint clean, render passes html_docs_check". It also prints two ADVISORY lines (committed page differs from render at flow line 6249 and cheat line 6235). The PR touches neither page, so these look pre-existing, but I did not run `check` on bare develop to prove it.

### (6) merge-tree
Clean onto `c4ced0bc` (the current develop), rc 0. Not run onto `2bc1a0b2` as that was superseded.

## NOT tested
- ESLint: my run used the root config, which does not parse TypeScript ("Parsing error: Unexpected token Meta"). That is my invocation, not a PR finding. The author's "0 errors, 0 warnings" is unchecked.
- tsc with test files in the program (the "same 10 errors as develop" claim).
- The full billing suite at the bare head with its own shared build (I ran it on the merge only).
- docs-fragments `check` on bare develop (advisory baseline).
- Real Stripe ordering; a running stack; the four platform suites; Node 24; KS-1909's existence; the push-hook legs the author lists; the 28-vs-192 cell recount.

## Files
`scripts/run.sh`, `scripts/mut.py`, `evidence/` (JSON per run, `mutants.json`, `spark/`), repo at `repo/`.
