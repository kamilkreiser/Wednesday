# QA GATE 34 - Tier 2 batch, Secuura/Blockchain, findings-only, 2026-10-30

## QA GATE - TIER 2, round 1, #1828: GO
## QA GATE - TIER 2, round 1, #1831: GO WITH NOTES

Clone: .../2026-10-30_gate34-1828-1831/repo (toplevel asserted before fetch). develop = 85cd24d81cb9; merge-base of both PRs = 530f091120d5.
Heads: #1828 = 68c83f8fb0a7349e6e6869aa84c62e732289cac7 (equals refs/pull/1828/head), #1831 = 4eba00d500d7114d2843365cd04cf0632cf5eebb.
npm ci --ignore-scripts rc 0; packages/shared built. Load 14-16 throughout. Nothing written under !CODING, nothing pushed/commented.

## Q1 Zero product bytes - PASS both
- #1828 three-dot diff: ks1533-key-mint-organisation-arm.test.ts (1 comment line, test file), new ks1585-...test.ts, 2 Projects Documents html. No product file.
- #1831: three new ks1836-*.test.ts + the same 2 html. No product file. (html conflict with develop/each other: expected, not a finding.)

## Q2 Re-run + tampers (each anchor count 1, each restored; sha256 equal before/after)
#1828 (4 cells, 4/4 at head):
- T1 revert docstring to "UNDECIDED POLICY, KS-1535": L1 red (`expected ... not to match /UNDECIDED/`), L2 red (`expected ... to match /RULED, KS-1570/`), L3/L4 green = 2/4 red, for the reason the names claim.
- T2 rename the RULED cell title: only L4 red (`expected false to be true`). T3 blank line between docstring and fixture: only L3 red (`expected '' to be '/** `ADMIN`...'`). Controls do bite.
#1831 (13 cells, 13/13 at head; 5/4/4 per file):
- Mf (trim both sides of wallet compare, nftReadGate.ts l.91): W1 + W2 red = 2/5, both `expected ['c1'] to deeply equal []`. Matches claim.
- Ma (drop the foreign-selector disjunct, nft.routes.ts l.244, `if (withheld > 0) {`): L1 red = 1/4, `expected [] to have a length of 1 but got +0`. Matches claim.
- Mb (`if (true) {`): Q1, Q2, Q3 red = 3/4 in the silent file, each `expected [ {level:'warn'...} ] to have a length of +0 but got 1`. Matches claim. (My Mb also reddens L2 and L3 of the foreign-selector file: 5 of 13 overall; the author's 3/4 is the silent file only.)
- Mutant texts are my reconstruction from the commit message line refs (the PR body Test Evidence is not readable from here); the red counts match the author's exactly, which supports the reconstruction.

## Q3 Hermetic / the 30 s
- Both nft ks1836-log files: db, cardano and blockchain-verifier are vi.mock'd; the only network is fetch to an ephemeral 127.0.0.1 express server. No real DB/network. The #1828 test reads a sibling file as text only.
- beforeEach timed alone (`-t L2`, 4 runs, load ~15): whole file 385-504 ms, test+hook ~225-290 ms. The 30 s is not masking a hang; it is ~100x headroom over a warm run. The cold-cache timeout the author saw (2 of 6 first runs, default 5 s) was not reproduced warm (cause not established, as the PR states).

## Q4 Whole suites at head
- security @ #1828: 35 files / 372 tests, all pass. (matches PR 372)
- nft-certificate @ #1831: 16 files / 120 tests, all pass. (matches PR 120). The three new files, run 3x consecutively with the 4 more: 8/8 each time (ks1836-log* glob).
- No timeouts, no re-runs needed.

## Q5 Spark shadow
- Ran spark_gate.sh (deterministic half only, via shadow_facts.py; no LLM review, spark_review.py NOT run) per PR, --work in scratchpad, --out spark_1828/ and spark_1831/ here. Head sha accepted as tip both. #1828: HEAD 4/4, BASE product 4/4. #1831: HEAD 13/13, BASE product 13/13. Equal-on-base is expected for a test-only PR (no product to revert); for #1828 the gate cannot show red-before because the docstring is itself a test file, my T1 above covers that.
- Spark LLM review: NOT RUN (script header scopes spark_gate.sh as the deterministic half; recent done.md shows op28/op30 on the Spark up to 15:1x, so I did not take it).

## Findings (ranked)
1. [note, NOT fix-before-merge] #1831 ks1836-log-silent-on-an-ordinary-own-rows-call.test.ts has the identical cold-import harness but its beforeEach has NO 30 s timeout (foreign-selector file has it). Same cold-run timeout risk under load; also the third copy of the same harness (with ks1836-nft-list-owner-bound) -> extract a shared helper later. Cheap fix: add `, 30000` for symmetry.
2. [note] #1831 Ma is killed by exactly one cell (L1). Coverage of the foreign-selector arm rests on that single cell. Acceptable; the PR states Mc/Md/F2/F3 are uncovered (confirmed none of the cells touch row-owner trim asymmetry).
3. [note] #1831 if beforeEach times out/throws, afterEach calls `server.close` on an undefined/previous server -> a second confusing error masks the first. Minor hygiene.
4. [note] #1828 the new test is intentionally brittle: it finds the docstring via `startsWith('/** `ADMIN`:')` and L4 pins the exact title of the RULED cell. Any rename of that cell breaks L4 (shown by T2) - cosmetic coupling the PR already declares. The sibling platform_admin docstring (line 82) still says UNDECIDED and L1 does not look at it (stated as out of scope).
5. [info] PR docs name develop 530f091120d5; develop has moved to 85cd24d81cb9; html conflicts resolve at merge as expected. Doc figures (372, 120, 13, 4) agree with my runs.

Fix-before-merge: none.

## Not tested
tsc/eslint with tests in the program (PR claims 0 errors; I did not re-run); the Spark LLM review; integration suites (DB), the four platform suites, Node 24 (I ran the local default node), any deploy; mutants beyond Ma/Mb/Mf (Mc/Md/F2/F3 per PR); the PR body Test Evidence text itself (unreadable from here); the merged result with develop after resolving html conflicts.

## Instrument errors
- Two Bash hook refusals (a `cd`, and a git write verb through a $VAR path); worked around by running scripts from the scratchpad with absolute paths. No effect on results.
- Mutant sources reconstructed (see Q2). My Mb differs slightly from the author's (still red as claimed).
