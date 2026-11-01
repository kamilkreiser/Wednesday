# QA Gate 80 verdict: Secuura/Distributed_Secuura PR 1895 (KS-1868, governance x5), tier 2

Work dir: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate80-ks1868-governance-1895/ (logs in `logs/`, scripts in `scripts/`, side evidence in `evidence/`). Node v26.8.1, npm 11.19.0. Every suite ran under `nice -n 10`, `--maxWorkers=2`, load1 at start 4.2 to 6.0 (never above 20).

## BLUF

GO WITH NOTES

The code, the tests and the one-line hand edit all check out. The only notes are about wording, and one behaviour change the PR text could state more plainly. It is the unreadable-thrown-value case only: before the PR the helper threw, and after it the helper fails open (G80-F1). Nothing is worse for an ordinary Error. Details below.

## Heads

| What | sha | Log |
|---|---|---|
| PR 1895 head START | cdf01b411f83c981f832041f7faee964810f34ca (matches expected) | logs/head_start.log |
| develop START | d7691f35312ea158f043e87a3227e477cccb183d (is the commit's parent) | logs/head_start.log |
| origin refs/pull/1895/head END | cdf01b411f83c981f832041f7faee964810f34ca | logs/head_end.log |
| origin refs/heads/develop END | d7691f35312ea158f043e87a3227e477cccb183d | logs/head_end.log |
| Worktrees at END | head wt = cdf01b41..., base wt = d7691f35...; head tree `git status` clean (excluding node_modules) | logs/head_end.log |

One commit on develop (`git log develop..head`: `cdf01b411 Refs KS-1868: governance DB read catches log an unreadable thrown value`). The ls-remote at START matched the fetch. The SSH push URL was set to `no_push_qa_gate`, and the `core.sshCommand` was set as specified (logs/fetch.log).

## FINDINGS

- **G80-F1 (note, medium): for an unreadable thrown value the PR turns a rejection into a fail-open return, and the fragment text calls this "unchanged".**
  - At base, if the thrown value is unreadable (revoked Proxy, or an Error whose `message` getter throws), the catch block's own read throws, so the helper REJECTS. Evidence: logs/red_base.log shows `Received promise rejected instead of resolved` ×10, rejecting with `TypeError: Cannot perform 'getPrototypeOf' on a proxy that has been revoked` ×5 and `Error: getter boom` ×5.
  - At head the same input logs the constant `unreadable thrown value` and returns `undefined` / `[]` / `[]` / `[]` / `0` (logs/green_head.log, 15 of 15).
  - So for this one case the PR moves a loud failure into the existing fail-open path (which KS-1732 tracks). For an ordinary Error nothing changes: the control cell C1 is green at base and at head in all five files.
  - The fragments say "The returned values and the log text are unchanged" and "this change keeps that behaviour exactly". Both are true for the ordinary-Error path. The flow fragment also says the helper "rejected without logging" before, so it is not hidden. The cheat fragment drops the contrast. Suggest one sentence: "for an unreadable thrown value the helper previously rejected and now returns the empty value like any other read failure".
  - Impact on `getTotalVotePower` is in section 1.
- **G80-F2 (info, low): small count slips in the fragment.**
  - It says the new test files are "54 lines". The canonical text is 54 lines and the committed files are 55 (logs/q2_test_vs_canonical.log, "committed lines= 55 canon lines= 54"). The 55 includes the approved `export {};` line.
  - The flow fragment names one caller per helper (`getProposal`, `getProposals`, ...). `dbGetProposal` actually has 6 call sites (583, 624, 652, 755, 807, 858; logs/callers.log). This is not wrong, but it understates reach.
  - The "+35/-5, +7/-1 per site" figure is right: 40 changed lines, equal to the canonical 40 (logs/q2_test_vs_canonical.log, "canon product +/- lines: 40 ; head product +/- lines: 40", multiset diff rc=0).
- **G80-F3 (info): KS-1732 rebase hazard is real and is disclosed.** The five catch lines are the same lines KS-1732 would rewrite. The fragment says so.
- **G80-F4 (limit): disjointness could only be checked against 13 KS-1868 sibling branches, not the 19 open PRs.** No `gh` login existed here (logs/gh_auth.log: "You are not logged into any GitHub hosts"). I fetched every `feature/ks-1868-253-*` branch instead (logs/fetch_ks1868_branches.log). None overlaps these 8 files (section 5).
- **G80-F5 (info, positive): every check that could fail did.** Red-first is by assertion (not a crash) for 10 of 10 red cells. 25 of 25 mutants were killed. 5 of 5 planted fragment defects were caught. All restores were verified by sha256.

## 1. The five hunks, source-level

Diff saved to `evidence/product.diff`. Every hunk replaces

`logger.error('<msg>', { ..., error: err instanceof Error ? err.message : String(err) });`

with

```
let reason: string;
try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }
logger.error('<msg>', { ..., error: reason });
```

| # | Helper | Line (head) | Log text | Return value | Direct callers (head, logs/callers.log) |
|---|---|---|---|---|---|
| 1 | dbGetProposal (O43-P2) | 219 | 'DB get proposal failed' with `{ id, error }`, unchanged | falls through to `return undefined` (unchanged) | 583 submitProposal, 624 getProposal, 652 castVote, 755 finalizeProposal, 807 executeProposal, 858 cancelProposal (plus the declaration at 214) |
| 2 | dbGetAllProposals (O44-P1) | 255 | 'DB get all proposals failed', unchanged | `return []` (unchanged) | 525 createProposal (max-active check), 635 getProposals, 1007 getGovernanceStats, 1043 processExpiredProposals |
| 3 | dbGetAllParticipants (O44-P2) | 313 | 'DB get all participants failed', unchanged | `return []` (unchanged) | 459 getParticipants (routes/governance.ts:65 calls it), 1008 getGovernanceStats |
| 4 | dbGetActiveDelegations (O44-P3) | 342 | 'DB get active delegations failed', unchanged | `return []` (unchanged) | 915 delegateVotePower, 947 revokeDelegation, 963 getDelegatedPowerFor |
| 5 | getTotalVotePower (O44-P4) | 448 | 'DB get total vote power failed', unchanged | `return 0` (unchanged) | 601 submitProposal, 1009 getGovernanceStats (exported) |

The six call sites listed for #1 are the full set in logs/callers.log.

**What does NOT change:** the log message strings, the log level, the log field names and the return values (checked line by line in `evidence/product.diff`). The `try` and `catch` structure is only added around the read of the thrown value.

**What the empty or zero return means downstream:**
- `dbGetProposal` returning `undefined` makes callers throw `NotFoundError('Proposal')`. A read failure therefore shows as a 404-style answer (this is KS-1732's fail-open class).
- `dbGetAllProposals` returning `[]` makes `createProposal` believe there are 0 active proposals, so the max-active cap is not enforced (the KS-1732 case).
- `dbGetActiveDelegations` returning `[]` makes `delegateVotePower` skip revoking old delegations, and `getDelegatedPowerFor` return 0 delegated power.
- `getTotalVotePower` returning `0`: `submitProposal` snapshots `proposal.totalVotePower = 0` at 601/607 and saves it as an active proposal. Arithmetic in logs/zero_power_arith.log (`node` over the formulas at `governance.types.ts:477` hasProposalPassed, `governanceService.ts:780` finalize, `:738-745` early finalize):
  - 1 vote for or against gives participationBps `Infinity`, and 0 votes gives `NaN`. Neither is `< quorumThresholdBps`, so the quorum test never fails (`quorumFails:false` in all 4 rows).
  - `earlyPass:true` on the first vote for, `earlyFail:true` on the first vote against.
  - So quorum is effectively waived and approval alone decides.
- **Is this the SAME as what an ordinary Error produces at base?** Yes. At base an ordinary Error already lands in the catch and returns `0` (control C1 is green at base for all five files, logs/red_base.log). The head returns the same `0` for the unreadable case. The PR adds no new bad value. It only extends the same outcome to a case that used to throw.
- **Does the PR make anything worse?** Only in the narrow unreadable-value case, and only in G80-F1's sense: at base, `submitProposal` would have aborted before saving (reject at line 601). At head it saves an active proposal with a zero snapshot. For ordinary Errors, nothing is worse. KS-1732 (Backlog) still covers the fail-open reads as such. I could not read Linear (no access, and the instructions forbid commenting), so KS-1732's scope is taken from the PR's own text and the source.

## 2. Hand edit and canonical comparison

Method: for each test file I took the `+` lines of `section_2.diff` in the Spark run dir (`out.md.checker/`) under /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/ (o43_p2 `-r2`; o44_p1..p4), minus the `+++` header, and diffed that against the committed file. Log: logs/q2_test_vs_canonical.log. Canonical copies: `evidence/canon_*.ts`. Read-only on the run dirs.

| Test file | diff vs canonical | committed lines | canonical lines | `^export {};$` count |
|---|---|---|---|---|
| ks1868-db-get-proposal-unreadable-throw | `5a6 > export {};` only | 55 | 54 | 1 |
| ks1868-get-all-proposals-unreadable-throw | `5a6 > export {};` only | 55 | 54 | 1 |
| ks1868-get-all-participants-unreadable-throw | `5a6 > export {};` only | 55 | 54 | 1 |
| ks1868-get-active-delegations-unreadable-throw | `5a6 > export {};` only | 55 | 54 | 1 |
| ks1868-get-total-vote-power-unreadable-throw | `5a6 > export {};` only | 55 | 54 | 1 |

5 of 5 files equal canonical plus exactly one inserted `export {};` line (after the header comment, line 6) and nothing else. Product bytes: canonical `section_1.diff` +/- lines (40) equal the head's +/- lines (40) as a sorted multiset (`product multiset diff rc=0`). Caveat: the o43_p2 run used is `-r2`, per the brief. The other four use their only run dirs (a `-control` dir exists beside each and was not used).

## 3. Red-first and mutants

Tests ran with the root-relative pattern `__tests__/ks1868-`. (A bare `ks1868` matches every file here because the work-dir name itself contains "ks1868"; I caught and fixed that before the results below. The first, wrong runs are overwritten.)

**Red at base** (new tests copied into the base worktree; product unmodified): logs/red_base.log: `Test Suites: 5 failed, 5 total`, `Tests: 10 failed, 5 passed, 15 total`, rc=1. The 10 failures are the R1 and R2 cells of each file, all `Received promise rejected instead of resolved`. The 5 passes are the C1 controls. They fail by assertion, not by a crash or import error.

**Green at head:** logs/green_head.log: `Test Suites: 5 passed, 5 total`, `Tests: 15 passed, 15 total`, rc=0.

**Mutants** (script `scripts/mutants.py`; one test file run per mutant; logs `logs/mut_H<n>_<name>.log`, summary logs/mutants_summary.log; original sha256 in logs/mutants_orig.sha256, product sha256 `2346aba10fa9ce1690a9900de6ede9435093ed1a928ffa95195f3c20d630916e`; every restore re-checked, `restored_sha_ok=True` ×25):

| Hunk | A revert to base line | B empty reason `''` | C wrong return | E log call dropped | F inner catch rethrows (`err.message`) |
|---|---|---|---|---|---|
| H1 dbGetProposal | killed (2 failed, 1 passed) | killed (2 failed, 1 passed) | killed (3 failed) | killed (3 failed) | killed (2 failed, 1 passed) |
| H2 dbGetAllProposals | killed (2 failed, 1 passed) | killed (2 failed, 1 passed) | killed (3 failed) | killed (3 failed) | killed (2 failed, 1 passed) |
| H3 dbGetAllParticipants | killed (2 failed, 1 passed) | killed (2 failed, 1 passed) | killed (3 failed) | killed (3 failed) | killed (2 failed, 1 passed) |
| H4 dbGetActiveDelegations | killed (2 failed, 1 passed) | killed (2 failed, 1 passed) | killed (3 failed) | killed (3 failed) | killed (2 failed, 1 passed) |
| H5 getTotalVotePower | killed (2 failed, 1 passed) | killed (2 failed, 1 passed) | killed (3 failed) | killed (3 failed) | killed (2 failed, 1 passed) |

25 of 25 killed. C mutants: `return [];` became `return undefined as any;`; `return 0;` became `return -1;`; and for `dbGetProposal` the trailing `return undefined;` became `return null as any;`.

## 4. Governance suite and tsc

Setup: `npm ci --ignore-scripts` at the workspace root `Blockchain/Dev` (logs/npm_ci.log: `added 1795 packages in 27s`, rc=0), then `npm run build` in `packages/shared` (logs/build_shared.log: rc=0). The base worktree reuses the head's `node_modules` by symlink, with the lockfile unchanged by the PR (no `package*.json` in the diff).

| Run | Result | Log |
|---|---|---|
| Whole suite at base, new tests excluded (`--testPathIgnorePatterns '__tests__/ks1868-'`) | 7 suites passed, 179 of 179 passed, rc=0 | logs/suite_base.log |
| Whole suite at head | 12 suites passed, 194 of 194 passed, rc=0 | logs/suite_head.log |
| Plain `tsc -p services/governance/tsconfig.json --noEmit` at head | rc=0, no output | logs/tsc_plain_head.log |
| Whole-program tsc WITH tests at head (my config `scripts/tsconfig.all_head.json` extends the service config, includes `src/**/*`, types node and jest) | rc=0, 0 errors | logs/tsc_all_head.log |
| Same, base untouched (new tests moved out) | rc=0, 0 errors | logs/tsc_all_base_untouched.log |
| Same, base with the Spark canonical tests (no `export {}`) | rc=2, 10 errors, all `TS2451` | logs/tsc_all_base_canonical_no_export.log |
| Same, base with the committed (edited) tests | rc=0, 0 errors | logs/tsc_all_base_with_copied_tests.log |

Delta: 179 to 194 = +15 cells in +5 files, as claimed. The 10 TS2451 without the edit, and 0 with it, reproduce the PR text. The edit is what makes the whole-program compile clean.

## 5. Merge and file overlap

`git merge-tree --write-tree refs/gate/develop refs/gate/pr1895`: rc=0, tree `4a523f3d597125a88c61e6c1814e0eca755fe0d8` (logs/merge_tree.log). No conflicts.

File overlap (logs/disjoint.log): I fetched all 13 other `feature/ks-1868-253-*` branches (`x-analytics`, `x-analytics-export-jobs`, `x-analytics2`, `x-audit`, `x-boot`, `x-demo`, `x-demostate`, `x-mcp`, `x-nft`, `x-persona`, `x-shared`, `x-vci`, plus this PR's own `x-governance`). All are 1 commit ahead of develop. Overlap of the other 12 with this PR's 8 files is 0 in every case. `x-persona` (head 3a88693f, PR 1894) touches 4 files, none of them in these 8. The only 8-of-8 overlap is the PR's own branch (self-match, `cdf01b41`). Limit: see G80-F4.

## 6. Fragment check

Script `scripts/frag.py`, runs `Blockchain/Dev/scripts/docs-fragments.mjs check --root <head worktree>`. Start sha256: flow `b20f9c776cc6f37c30e7f0e1d4737f156d336d58c11419378df8af609d6f3f9a`, cheat `1c5068613715834eae05d11246f867c2a5f2b477d1c5f9868f7949a675664905` (logs/frag_summary.log).

| Case | rc | Last line | Restored |
|---|---|---|---|
| Clean tree | 0 | OK | n/a (logs/frag_check_clean.log) |
| P1 flow: unclosed `<div>` appended | 1 | FAIL, 1 finding | OK |
| P2 flow: literal `9999.` replacing the `<!--n-->` number token | 1 | FAIL, 2 findings | OK |
| P3 cheat: unclosed `<div>` appended | 1 | FAIL, 1 finding | OK |
| P4 cheat: carries an `<!--n-->` token | 1 | FAIL, 1 finding | OK |
| P5 flow: second numbered entry added | 1 | FAIL, 1 finding | OK |
| After restore | 0 | OK | n/a |

The clean run prints two ADVISORY lines (committed page differs from the render at flow line 6249 and cheat line 6235, "a hand step"). The same ADVISORY appeared in Gate 79's clean log (logs/frag_check_clean.log of gate79), so it looks like a property of the render, not of this PR. Final line: `docs-fragments: flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes html_docs_check`. Content review of both fragments: see G80-F1 and G80-F2. The "seven more unguarded reads" list is accurate: 167, 187, 205 (rethrow), 277, 287, 390 (`verifyDbReady`), 1056 (`processExpiredProposals`), per logs/unguarded_sites_head.log (12 `err instanceof Error` sites at base; 5 hunks leave 7).

## 7. END heads

See the Heads table and logs/head_end.log: PR head and develop unchanged from START at 23:11:04. The head worktree's product file hash `1261c5c8b33d...` equals the committed blob, so every mutant was restored byte for byte.

## NOT TESTED

- A booted governance service or a real database failure. The tests use a `../db` stand-in.
- HTTP behaviour under Express (route error handling for `NotFoundError` etc.).
- The 19 open PRs beyond the 13 KS-1868 branches (no `gh` login); the content of KS-1732 and any Linear state (no Linear access).
- The repo's own whole-program tsc config. I wrote `scripts/tsconfig.all_*.json`, so there is no claim about any CI config.
- eslint (not asked), the four platform suites, an LTS Node (ran Node v26.8.1), any deploy.
- The PR body text and the READY mail claims beyond what is quoted above; the push-hook preflight (13 of 16 legs) is the author's report and I did not verify it. The mail is treated as unverified.
- The cases where the stand-in `query` rejects with values other than a revoked Proxy and a throwing `message` getter (for example an object whose `toString` returns a non-string; KS-1904's class).
