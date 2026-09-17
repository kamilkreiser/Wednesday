# NEXT SEARCH 2026-09-17p (22:53-23:12 AEST): Ornith queue empty after KS-1219; search at tip `27e53ec3a`

**BLUF: ONE ticket fits. KS-1227 (only its try/finally + pin half) is briefed, built with rc 0, and passed by the real checker (PASS 7/7 on the draft AND the placed input). No second or third fit exists in the post-12:00Z pool. Nothing is queued.**

The tip is `27e53ec3aa010b50cd9b2e4a1d15cbb34605ba7d` (#1029, KS-1180 part 1), as expected. It did not move between 22:53:45 and 23:10:33. The input is built at it.

1. **KS-1227 (code_patch test-only, vitest, modify ks1072 in place; try/finally + pin half).**
   - **E1** wraps `postTier2`'s verify call, status read and body read in `try { } finally { }`, so the listener is detached on every path (R-1029-3).
   - **E2** adds two cells:
     - **R1** uses `vi.stubEnv` to point the live chain scan (`verification.ts:585`) at the stub. A second, non-hit request then reaches the stub while tier 2 answers, and R1 asserts the witness reds. This is the pin R-1029-4 asked for.
     - **R2** forces a status red with `postTier2([])` and asserts `listenerCount('request')` is 1. This is the ticket's Q-D4-LEAK regression proof.
   - **Tamper** `:585` (the scan ignores `ANCHORING_SERVICE_URL`) reds R1 only, by assertion.
   - **Result:** golden **PASS (7/7)**; api-gateway goes from 556 to 558 tests; tsc rc 0.

**Queue line (NOT added):**
```
KS-1227 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1227.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

## Wednesday must read

1. **R1 pins the counting rule AS MERGED, and the ticket asks the owner to decide that rule.**
   - "Decide the counting rule on purpose. Either keep ... and say so in the comment, or filter by this document's path" is a pick. That half is SKIPPED, as the commission allowed.
   - But the "pin half" can only pin what exists: R1 asserts that a second, non-hit stub request reds the witness, which is the fail-closed "keep" behaviour.
   - If the owner rules "filter", R1's expectation flips and has to be rewritten in that change.
   - Before raising, either rule "keep" (then only the ticket's one-line comment is left), or raise it as "Refs KS-1227: pins the rule as merged; the decision stays open".
2. **The P-1029-1 message reword (`:128`, "tier 2 answered") is not briefed.** The ticket calls it optional and ties it to KS-1180's tier-1 half.
3. **Six trailing comments are load-bearing for the builder, not decoration.**
   - Re-indenting `expect(res.status).toBe(200);` and `anchorServer.off(...)` into the try/finally makes a `+` line identical, once stripped, to a `-` line. The builder's CONTEXT-AS-ADDITION gate refused the first draft for exactly this at 23:04:15 (the `});` closers).
   - So the two E1 lines carry `// KS-1227 ...` comments, and the two new closers are `}); // KS-1227 R1` / `}); // KS-1227 R2`. This matches the file's own `}); // KS-1180 control` at `:140`.
   - For the same reason, the fetch is written on one line with string concatenation and `jsonHead`, as the KS-1180 control does at `:137`. A re-indented template literal would put a backtick and `$` on a `+` line.
   - A model that drops any of these comments FAILS A3c. That is measured (`nocomment`).
4. **New PR #1034 opened during the search** (23:10:48): Seat A's KS-1215 (`api-gateway middleware/auth.ts` + the ks1215 test). It does not touch the ks1072 test or `verification.ts`.
5. **Prompt ~28.8K tokens** (builder estimate on the placed input), leaving ~36.8K at ctx 65536. The test file is 190 lines; the product file (70 KB) is in the input only for the tamper.
6. **KS-1219 is still running.** Its `oauth.ts` and ks1219 test do not overlap KS-1227 (a different service), so order does not matter.

## FOUND

| ticket | verdict | why | instr |
|---|---|---|---|
| **KS-1227 (try/finally + pin)** | **FITS, briefed** | Filed 12:48Z from the #1029 gate R-1029-2/3/4. One test file; no PR, head or READY touches it. Tamper-graded pin found on the product's live scan. | measured |
| KS-1227 counting-rule half | skipped | "Either keep ... or filter" is a pick; R1 pins the merged rule (see item 1). | read |
| KS-1227 P-1029-1 reword | skipped | Optional in the ticket; belongs to KS-1180's tier-1 half. | read |
| KS-1180 | refused | In Progress (updated 12:48Z = the KS-1227 relation); the tier-1 half is a seat lane; the builder's state gate refuses. | read |
| KS-1215 | refused | In Progress; PR #1034 opened 23:10. | REST GET |
| KS-1194 | refused | In Progress; PR #1032. | read |
| KS-763 | refused | In Progress; PR #1033 + Seat B's local PR-4. | read |
| KS-1211 | refused | In Progress; #1030 merged, remaining audit rows are Seat B's. | read |
| KS-1224 / KS-1225 / KS-1226 | stand (17o) | updatedAt unchanged 12:21Z; decision / manifest / no systemTest tier. | read |
| 17o leads | stand | KS-1152 R1 site 5: READY_KS-730-B still unraised (0 KS-730 commits at the tip). ks764 guard `:419-420`: needs backticks, and R1a/R1b are not merged. KS-1219 other params: wait on KS-1219. KS-1226 F5: no tier. | read + git log |

**Screens:** Linear 22:54:08 (8 KS issues created or updated since 2026-09-17T12:00Z) and 23:10:48 (9; KS-1215 updated 12:59Z). Record check: `grep` of queue.md, done.md and candidates.md for KS-1227 = 0 (positive control: 45 / 175 / 295 `KS-1` lines).

## TESTED

- **Direct, clone2** (`k1227/measure.sh`, 23:03:26-23:04:06):
  - tip file 6/6;
  - patch 8/8;
  - patch + tamper: only R1 red (`expected 'no red' to contain 'KS-1180: tier 2 answered, one anchor-...'`);
  - E2 without E1: only R2 red (`expected [ true, 2 ] to deeply equal [ true, 1 ]`);
  - patch + hit-only filter: only R1 red;
  - tip + tamper: 6/6 green; tip + hit-only filter: 6/6 green (both gaps are real);
  - whole api-gateway: 57/556 at the tip, 57/558 patched, 0 failed; project tsc rc 0 both;
  - tests-included tsc: 49 diagnostics, identical sets, the one ks1072 diagnostic (`:102` TS2741) present on both trees.
- **Builder:**
  - draft rc 2 at 23:04:15 (the context-as-addition gate on `});`), fixed in the brief;
  - draft rc 0 at 23:04:40;
  - placed rc 0 at 23:08:40, rebuilt rc 0 at 23:10:01 after a token-count correction in the Notes.
- **Real checker** (sha256 `b9fd00065fba...`, unchanged):
  - **draft input:** golden **PASS (7/7)**, strict, A4 1 failed / 8 (R1 by assertion); `nofinally` FAIL A3c; `noenv` FAIL A3c; `nocomment` FAIL A3c; `hitonly` FAIL A5+A6;
  - **draft input, A3c emptied:** `nofinally` FAIL A4 (R2 control red); `noenv` FAIL A5+A6;
  - **placed input:** golden PASS (7/7) at 23:08:54 and again at 23:10:05 on the rebuilt input; `hitonly` FAIL A5+A6; `nofinally` FAIL A3c.

## NOT TESTED

- No model round (nothing queued).
- vitest 4.1.11: the farm is the source's installed 4.1.10. The same caveat applies as for the #1029 gate (R-1029-5).
- Behaviour when `anchoring:4005` resolves somewhere real. R1's tamper run and the existing cells both rely on that lookup failing fast, which it did (every file run took about 1 s).

## HOW

- **Tip:** `ls-remote` of the source's origin URL from scratch clone `search17p/clone`, using the source's `core.sshCommand` (22:53:45, 23:10:33). Source porcelain was 0 at every read.
- **Partition:**
  - `gh_prs.py` (REST GET): 21 PRs at 22:54:07, 22 at 23:10:48.
  - `partition.sh` (for-each-ref + three-dot + blob compare against `27e53ec3a`): 38 live heads. The ks1072 test differs only on the squash-merged `feature/ks-1072-ornith-…` (#1016).
  - `ready.py`: 138 READY diffs, 49 dated 09-17, 0 touching the file.
- **Git:** only read verbs ran on the source checkout. The write verbs (clone, checkout, apply, `checkout --`) ran in `search17p/clone` and `search17p/clone2`, from scripts. Both clones end at porcelain 0. Nothing was deleted.
- **Scripts:**
  - `search17p/`: `setup.sh`, `tipcheck.sh`, `gh_prs.py`, `linear_issue.py`, `pool.py`, `partition.sh`, `ready.py`.
  - `k1227/`: `prep.sh`, `assemble.py`, `measure.sh`, `restore.sh`.
- **Files written:**
  - `night/briefs/KS-1227.md`, `night/inputs/code_1227.json`;
  - the `## SEARCH 17p` block in `candidates.md` (backup `candidates.md.pre-2311-search17p`);
  - this report.
- **Not touched:** `queue.md`, `night_run.sh`, the builders, the checkers. Nothing was pushed, commented, filed or mailed.
