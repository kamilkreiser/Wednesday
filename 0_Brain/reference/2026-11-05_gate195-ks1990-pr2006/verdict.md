GO WITH NOTES — MERGE (no HOLD-FOR-KAM) — PR 2006, merge tree 941a1eca81f6ef0182775f918dfd7a6e828ad9b8 on develop 07a2d62be6a0

# QA Gate 195 (Tier 2, round 1): PR 2006 / KS-1990 seed-demo-users success and status follow the counts

**Subject.** Secuura/Distributed_Secuura PR 2006 (Seat W 28th), 1 commit.
- Start (ls-remote, read-only checkout, deploy key): `refs/pull/2006/head` = `6311c141f99e5ade8d94e60ee15b0c80006a52cd`, `refs/heads/develop` = `07a2d62be6a09c9cd504864d1cf1906543d55317`. End (11:48 AEDT): the same two values. Head did not move.
- Merge tree (my clone, `git merge-tree --write-tree`): rc 0, tree `941a1eca81f6ef0182775f918dfd7a6e828ad9b8`, equal to `6311c141f99e^{tree}` (logs/q7.txt). Merge onto develop `07a2d62be6a0`.
- Host: macOS arm64, Node v26.8.1 (NOT Node 24), TypeScript 5.9.3, jest 29 (ts-jest) from the head lock (`npm ci --ignore-scripts` rc 0, shared build rc 0).

**Method.** Tier proof first (Q1), then my own harness `gate_tests/gate195-matrix.test.ts`, adapted from the KS-1802 file shape: real express router, real adminConfig handler and real `requireRole`, listening on a loopback port; only `../db`, the logger, `runWithPlatformScope` and `authenticate` (principal role toggled) are faked. The same file ran against head bytes and against base bytes (adminConfig.ts overlaid from develop, blob id checked equal to base, restored from the head blob, blob-equal, `git status` empty). 20 cells. Mutants by `scripts/mutants.py` on the committed bytes. Suites and static checks by `scripts/suites.sh`. Every process ran with cwd `cwd/` under `env -i`, HOME and TMPDIR inside the workdir. PR body read by GitHub API GET (token never printed).

## Findings

### G195-F1 — LOW: the PR's own 20 cells do not pin the boundary "created 1 and failed above 0" (one of my own mutants survives them)
**FOUND:** my mutant g1 (`created === 0` -> `created < 2`) leaves all 20 of the seat's cells green (red 0 of 20). Its only observable effect is that the partial 1-created/13-failed run would answer 500 instead of the ruled 200 with `success: false`. The seat's partial cells are 13/1 (R2) and 10/4 (R4); none has created = 1. My matrix kills g1 (cell `partial_1created_13failed` differs). The head code is correct on that cell (200, false, c1 f13).
**TESTED:** the committed head code; this is a coverage gap in the PR's tests, not a defect in the route.
**HOW:** `logs/mutants.log` line g1; diff of `runs/mut_g1.jsonl` against `runs/matrix_head.jsonl`.

### G195-F2 — INFO: PR text nits (no behaviour impact)
**FOUND:** (a) the flow fragment's NOT-measured row says the stack run "reproduced the old behaviour and the cause, not the fixed route", while the PR body and READY say the fixed route was checked on the stack at head (500 through nginx and gateway): the fragment and the body disagree (not re-run here). (b) The fragment heading says "TIER 1" while the commission treats it as tier 2 (Wednesday's call, not a defect). (c) "Exactly 6 hunks" is true only at zero context; default `git diff` shows 4 hunks; the six changed lines are exactly R1..R5 and C1. (d) "file line count 161": `wc -l` gives 160 base and 160 head (equal either way). (e) The body says the OpenAPI spec has 9 `/admin` path lines; `git grep -c '/admin'` gives 13 (my count includes non-path lines); the claim that it has no entry for this route holds (0 hits for `seed-demo`).
**TESTED:** read against measurement.
**HOW:** `logs/pr2006_body.md`, `scripts/q7.sh` output.

### G195-F3 — INFO: docs-fragments check prints two ADVISORY lines at head
**FOUND:** `docs-fragments check` rc 0, "OK", but prints "ADVISORY the committed page differs from the render" for flow (line 6249) and cheat (line 6235). Not compared against base; I do not know whether it is pre-existing. A planted unclosed div in the new flow fragment makes the check fail (rc 1), so the instrument can fire.
**TESTED:** head only. **HOW:** `logs/q8_frag_clean.log`, `logs/q8_frag_planted.log`.

## What passed (measured)

**Q1 Scope / tier proof.** `git diff --name-only 07a2d62be6a0...6311c141f99e` = exactly 5 paths (adminConfig.ts, ks1802 test, new ks1990 test, flow and cheat fragments). adminConfig.ts: one hunk (+7/-2) at line 2146. sha256 of lines 1..2145 base = head = `8eabae25d3f3…` (this region holds the router-level `authenticate(), requireRole('SYSTEM_ADMIN','ORG_ADMIN')` at :45, the route registration, the `isDemoSeedEnabled()` gate and its 403 at :2042, the `users` array, the INSERT with `ON CONFLICT (email) DO NOTHING` at :2111, the per-user catch, and the org-link `catch { /* skip */ }` at :2145). Lines 2024..2145 sha `ae8ff12bdf56…` base = head. Everything after the hunk (base from 2152, head from 2157) sha `e94805cadd54…` equal. `utils/demoSeedGate.ts` is not in the diff. The only changed lines are the `res.json` -> `res.status(...).json` call and `success`. Tier 2 premise holds: the gate, the authorisation and the INSERT are byte-equal. Control for the sha instrument: the 2024..2145 region and the 1..2145 region differ from each other (different hashes), and the edited-copy control in Q2 reads unequal.

**Q2 ks1802.** 6 hunks at `-U0` (4 at default context), 6 lines changed, all `expect(await seed())` lines. 9 cells in the file at base and head, same titles in the same order. Changed: R1, R2, R3, R4 (KS-1818), R5 (KS-1818), C1. Byte-equal: R6, C2, C3. All non-expect lines identical. Control: a copy of base with one string edited inside C1 reads unequal (`False`). Evidence `logs/q2.txt`, `logs/q2_ks1802.diff`.

**Q3 Contract table, base vs head, real router (20 cells, `logs/compare.txt`).** 10 changed, 10 unchanged, **head more permissive than base: 0 of 20**.
- all 14 inserts fail (ordinary Error, revoked Proxy, throwing getter): base 200/true c0 a0 f14 -> head **500/false** c0 a0 f14 (3 cells); ORG_ADMIN all-fail: same change.
- 0 created, 1 already present, 13 failed -> head 500/false; 0 created, 13 present, 1 failed -> head 500/false (counts unchanged).
- partial 13/1 and 1/13 -> head 200/**false**, counts unchanged.
- all succeed 200/true c14, all present 200/true a14, 1 created + 13 present 200/true, all succeed with org-link throwing 200/true: unchanged.
- gate closed (ALLOW false, ENABLE false, both false): 403 each, unchanged. Non-admin (VIEWER, success and all-fail): 403, unchanged.
- throw outside the loop (gate closed + logger.warn throwing -> outer catch): 500/false, no report fields, unchanged.
- Response keys on the 500: `alreadyPresent,created,failed,seededUsers,success` (the same five as before; no new field, no new message text).
- Not driven: no token (see NOT tested).

**Q4 Leak.** Planted token in the thrown error's message, detail, hint, where, meta, plus SQLSTATE 42P10, table name, seed e-mail, file path. Head, 500 cell and partial cell: 0 hits for 10 needles in the whole body and all headers (body 76 and 77 bytes). Positive controls in the same run: the token is in the captured log (`logHasToken true`) on both cells; mutant m4 (raw error in the body) makes the same instrument read hits (hits: the token, `users_email_idx`, the e-mail, `/srv/app`, `adminConfig.ts`, `insert failed`; the SQLSTATE field itself is not echoed by that mutant) on both cells.

**Q5 Mutants (`logs/mutants.log`, `runs/mut_*.json`).** Clean run before and after: 20 of 20 seat cells and 20 matrix cells, 0 red. Every anchor count 1 (m4 has two anchors, each 1), every mutant parsed, every restore sha256-equal to the head blob, final blob equal head. The seat's table exists in the READY only as prose; I counted its raw rows: **8** (m1..m8), as the headline says. I reproduced all 8 by their description (my anchors; my red counts on the seat's 20 cells): m1 11, m2 4, m3 8, m4 18, m5 8, m6 1, m7 5, m8 4. Seat reports m1 11, m2 4, m3 8, m4 19, m5 8, m6 1, m7 2, m8 4: m4 and m7 differ because my mutant bodies differ from the seat's (m7 mine also turns the already-present-only cells red); killed **8 of 8**. My own: g1 (`created < 2`) SURVIVES the seat's cells (F1), killed by my matrix; g2 (`created <= 0`) survives and is EQUIVALENT (created is a count that is never negative; matrix diff 0); g3 (`success: failed < 2`) killed (4); g4 (500 -> 503) killed (8). Total 12 mutants: 11 killed by the seat's cells or mine, 1 equivalent survivor, 1 non-equivalent survivor against the seat's cells only (g1).

**Q6 Consumers.** `git grep -n 'seed-demo-users'` at head: 64 hits in 23 files (positive control: includes the route's own definition at adminConfig.ts:2037). Outside docs and tests the only code that reads the response is `systemTest/schemathesis/tests/support/demo_seed_gate.py` (`parse_seed_counts`: status 200 and `success is True`; `rerun_overwrote_nothing`), used by `tests/integration/test_seed_demo_gate.py` leg B via `fixtures/seed_gate.py:post_seed`. No frontend, script or OpenAPI entry (0 `seed-demo` hits in secuura-api.yaml, 13 `/admin` hits as control). I ran the real helper from the head blob: base all-fail body -> `SeedCounts(0,0,14)` and `rerun_overwrote_nothing` True (green on an all-failed stack); head 500 body -> `None` (leg B goes red); healthy -> `SeedCounts(14,0,0)`. The PR body names this availability cost. Claim confirmed.

**Q7 Merge tree.** rc 0, tree `941a1eca81f6ef0182775f918dfd7a6e828ad9b8` = head tree.

**Q8 Suites and static (`logs/q8_*`).** Whole originate workspace default workers: head **211 of 211 files, 2496 of 2496 cells, rc 0**; base **210 of 210, 2485 of 2485, rc 0** (+11 = the new file). Red-first: the PR's tests at head with adminConfig.ts at base: 12 of 2496 cells fail, all by assertion (ks1990 R1..R5 and L1; ks1802 R1..R5 and C1), 2484 pass. tsc service config at head: rc 0, 0 errors; planted type error: rc 2 (TS2322). eslint on the 3 touched .ts files: rc 0, no output; planted `debugger`/unused file: rc 1 (1 error, 1 warning). docs-fragments: OK rc 0; planted unclosed div: rc 1. After every overlay the tree was restored by `git show`, `git status` empty. KS-1989 not run (default workers) and not counted.

**Q9 PR body (`logs/pr2006_body.md`, 10250 chars, sha1 `419b6df9…`).** Title 82 chars, starts `Refs KS-1990:`; state open, not draft, head = `6311c141f99e`, base develop, 1 commit, 5 files, +229/-8; mergeable true / state "unstable" (checks, not examined). Close-word hits 0 (control 2 of 2). Present: the contract (table) and who ruled it (Wednesday, inside commissioned work; Kam has not ruled on this route); the cause with proof and the KS-960 pointer (comment `cbc5250e`, sibling KS-962); the availability cost; Node v26.8.1 not 24 with LTS status not verified; a NOT-run list. Sentences my measurement contradicts: none in the body; two small nits in F2.

## NOT tested
- No token / 401 (my harness replaces `authenticate`; the real authenticate was not driven here). The seat's stack run (401 and 403 controls, the 500 through nginx and the gateway, the 42P10 cause) was NOT re-run, as commissioned.
- No real database; the INSERT's behaviour against Postgres (42P10) is read from the PR body, not measured.
- Node 24, kintsugi or demo, a deploy, the Schemathesis leg itself (only its helper functions, on literal bodies), the four platform suites, hook legs 3/4/8, `--maxWorkers=4` (KS-1989).
- Whether the seeded accounts' passwords, roles or tenant are untouched is established by the byte-equality of the INSERT and `users` region (Q1), not by a database read.
- Whether the docs-fragments ADVISORY lines are pre-existing (F3).
- "Reachable"/"in production" claims: none made.

## Plain answer for Kam
This change only alters what the demo-user seeding button tells the person who runs it. Before, it said "success" even when every one of the 14 accounts failed to be created; now it says failure (an error status) when nothing was created, and "not fully successful" when only some were. The part that decides who may run it, and the part that creates the accounts, are exactly as before, so no passwords, roles or access change. The reason it has been failing is a separate database problem the author recorded on a different ticket and deliberately did not touch. One automated test leg in the Schemathesis suite currently passes when everything fails, and will go red after this merge, which is the correct outcome and is stated in the PR. Nothing here needs your decision; I found one small gap in the PR's own tests and no case where the new behaviour is more permissive than the old.
