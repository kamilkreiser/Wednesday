PR 2236: GO WITH NOTES (at head a3f5e674161f3c42fe83f91e10f4b3846563c22a; tier 2)

Gate 359 (tier 2, Sonnet, row G2), 2026-11-15 17:37 to 17:45 AEDT. Findings only: nothing was fixed, pushed, posted, mailed, merged, or written to Linear or GitHub. All work in `scratch/` of this folder.

**Pins.** `gh api` and `git ls-remote` at 17:38:41 (`scratch/pin1.out`) and again at 17:44:13 (`scratch/pin2.out`), plus `gh api` state=open merged=false at 17:44. Neither moved.
- develop ce35818d50aebe7f41fc41f677ee03079c36d7ad
- PR 2236 head a3f5e674161f3c42fe83f91e10f4b3846563c22a (one commit, on 48883ba5976b)
- PR 2231 head 5dccb159d12960f14d31dd6bca20e7c524952486

**Load.** load1 was 30 at the first measurement (17:38), 12 to 16 during the mutant and suite runs, 12.6 at the last. The commission's gate (load1 < 12) was NOT met on the heavy legs; I ran at 12 to 16 and the host never queued a leg for me (results are deterministic pass/fail counts, not timings).

## FOUND

**G359-2236-1 (Info; test thinness, no product impact).** Two of my own mutants survive the 31 cells, so the cells do not pin them:
- `O2_header_when_no_user`: the caller read from `x-user-id` only when `req.user` is absent altogether. 0 reds in the ks2192 file AND 0 reds in the KS-2166 file (83 cells). Cause: every cell sets a principal. Reachability: the real `authenticate` answers before the route, so a request with no `req.user` should not reach `callerMayActOn` (read, not exercised; no running stack).
- `O4_no_empty_guard` (drop `caller !== ''`): 0 reds in ks2192, but 1 red in the KS-2166 file. So it is pinned, just not by this PR.
Not a defect in the PR's claim (it claims the claim-without-userId case, and that is pinned). Record for the board only if the owner wants the no-principal case pinned.

**G359-2236-2 (Info; evidence wording).** The PR's "check:test-types rc 0" is vacuous for kyc: root `package.json` `check:test-types` runs `scripts/typecheck-tests/check.cjs` for auth, api-gateway, vc-issuer, security and m365-integration only. kyc is not in the list. The seat's own scratch tsc over service plus tests (reproduced by me, rc 0, planted control rc 2) is the real instrument.

**G359-2236-3 (Info; pre-existing, not this PR).** `docs-fragments.mjs check` prints two ADVISORY lines (flow line 6249, cheat line 6235: committed page differs from the render inside the rendered range). They come from the committed pages lagging earlier fragments, not from KS-2192's two new fragment files. rc 0, "OK".

No Low-or-higher finding on this PR.

## TESTED

**Q1. Tests only.** `git diff --numstat origin/develop...refs/pr/2236`: 3 files, 245 + 16 + 13 added, 0 deleted: one test file and the KS-2192 flow and cheat fragments. No product file. Second instrument: `hash-object` of `services/kyc/src/index.ts` at develop and at the head are both 9becd6065b3e (identical), and `git diff --stat ce35818..a3f5e67 -- Blockchain/Dev/services/kyc` shows only the new test file.

**Q2. The cells are meaningful.** Vitest JSON, `scratch/out-plant-*`; each plant is a one-line edit of `index.ts` in my own worktree, restored by `git checkout HEAD --` and `hash-object` read back 9becd6065b3e every time; porcelain 0 at the end. Baseline (no plant): 31 of 31 pass, rc 0.

| Plant (mine) | Failed / 31 | Which |
|---|---|---|
| M19: `userId ?? x-user-id` | **4** | X1 x4 |
| M19b: `x-user-id ?? userId` | **12** | X1 x4, X2 x4, S x4 |
| M23: `toUpperCase()` over the two names | **8** | F1 x4, F2 x4 |

All three equal the builder's counts (4, 12, 8). The plants are my own text, not the seat's.

My own mutants:

| Plant | Failed / 31 | Which |
|---|---|---|
| O1: DELETE passes `platformMayRead=true` | 2 | P (DELETE x2 roles) |
| O3: role fold `normalize('NFKC').toUpperCase()` | 8 | F1 x4, F2 x4 |
| O5: initiate passes `platformMayRead=true` | 2 | P (initiate x2 roles) |
| O6: DELETE also admits `x-user-id === :userId` | 2 | X1, X2 (DELETE) |
| O2: header read only when no `req.user` | 0 | SURVIVES (G359-2236-1) |
| O4: drop `caller !== ''` | 0 | survives here; 1 red in the KS-2166 file |

Positive control for every zero: the same harness reddened under the other plants, and the baseline passes. So the 31 cells are meaningful for the two gate-338 rules and the platform-on-DELETE/initiate rule; the cells' stated gap is only the no-principal path.

**Q3. Pass at head and develop; whole kyc suite.** Node v26.8.1, vitest 4.1.12, interleaved dev, head, dev, head. Each tree had its own `npm ci --ignore-scripts` (rc 0) and `packages/shared` build (rc 0).

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop ce35818d50ae | 18 files, 177/177, rc 0 | same |
| head a3f5e674161f | 19 files, 208/208, rc 0 | same |

177 + 31 = 208, equal to the READY. The ks2192 file alone: 31/31 at head. "Cells pass on develop" in the sense of the seat's claim ("31 of 31 on develop by construction") holds: the cells are green on a tree whose kyc source equals develop's.

**Q4. PR 2231 and PR 2236, both orders.** `merge-tree --write-tree` (`scratch/out-mt.txt`), all rc 0 with no conflict markers:
- develop x 2236: tree 0cc028a0215f, same in both orders.
- develop x 2231: tree 21661655a4faf, same in both orders.
- 2236 x 2231: tree 008ac1e442f4, same in both orders.
- Paths: PR 2231 touches kyc `index.ts` (the DELETE route), its own ks2185 test and its own two fragments; PR 2236 touches only its own test and fragments. Disjoint, zero overlap.
- Semantic interaction, measured on a real merge commit of the two heads (tree 008ac1e4, index.ts blob e2bef0b96435 = PR 2231's): the whole kyc suite is 20 files, **218/218**, rc 0 (177 base + 31 + 10). PR 2236's DELETE cells (X1, X2, P, S on `DELETE /api/kyc/user/:userId/data`) pass against PR 2231's try/catch route. Reason, from the code: PR 2231 changes only the body after the owner check (`callerMayActOn(req, req.params.userId, false)` at line 1277 is unchanged, per gate 353), and PR 2236 pins only the 403 side.
- Instrument note: the merged run swapped PR 2231's `index.ts` and test file into my head worktree (restored by blob; porcelain 0). It was not a separately built worktree.
- No conflict and no semantic interaction to name.

**Q5. Static checks with controls.**
- tsc `--noEmit -p services/kyc/tsconfig.json`: rc 0. That tsconfig excludes `src/__tests__`, so a scratch `tsconfig.t.json` (extends it, includes all of `src/**/*`) was also run: rc 0, 0 errors. Planted TS2322 in the new test file: rc 2, error reported at the file (restored).
- eslint (ESLint API, Dev root flat config, cwd = Dev): 0 errors and 0 warnings on the new test file, and on `index.ts`. Control: `lintText` of `debugger; var g359x = 1;` against the same path: 2 errors (no-debugger, no-var) plus no-unused-vars. (The CLI with `--config` gave a parse error on the test file; that was my invocation, not the file, and the API run with the repo's own config is the valid instrument.)
- docs-fragments `check --root <worktree>`: rc 0, "lint clean, render passes html_docs_check" (246 new flow and cheat entries). Planted unclosed `<div>` in the KS-2192 flow fragment: rc 1 "tags are not balanced" (restored). The sparse worktree needed `systemTest/__tests__/support` added for the checker. Fragments read whole: accurate against my measurements (counts 4/12/8, 177 to 208, "no red on develop by construction"). Their base sha 48883ba is the PR's own base, as stated.

## HOW
- Clone `scratch/clone` via `--reference` to the Blockchain project's object store; fetched with that project's deploy key by a one-shot `GIT_SSH_COMMAND`; push URL set to DISABLED. Worktrees `wt-dev`, `wt-head`, `wt-mrg` (the last only for blob/tree identity; the merged suite run used `wt-head` with swapped files).
- Scripts in `scratch/`: `mt.sh`, `wt.sh`/`wt2.sh`, `install.sh`, `plant.py`, `plants.sh`, `suites.sh`, `merged2.sh`, `tsc.sh`, `eslint.cjs`, `lint.sh`. No writes outside this folder.

## NOT TESTED (UNMEASURED)
- A running stack, Postgres, a real token through the gateway (whether it strips or sets `x-user-id` before kyc sees it), the shared `isPlatformRole` itself, Node 24, a container build, Schemathesis, Akto, Playwright, k6.
- The pre-push preflight (the builder reports 13/16 legs, 3 skipped, nothing failed; I did not rerun it), and the full `check:test-types` (it does not cover kyc).
- A separately `npm ci`-built merged tree for PR 2231 plus PR 2236 (I swapped files into the head tree instead).
- Linear: KS-2192's state and comment were not read.
- Reachability of G359-2236-1's O2 beyond reading that `authenticate` runs first.
