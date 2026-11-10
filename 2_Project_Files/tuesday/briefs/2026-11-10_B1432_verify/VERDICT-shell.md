GATE B1432: GO WITH FINDINGS @ 5cc88ab on main 849b808

Branch `b1432/nexusai-f-shell-layout-header`, head `5cc88abe0eb77d58fc0405e0ea2be0d5da470cd3` (RD-979). Tier 2 (front end / tests). Verifier worked in its own clone and worktrees under the session scratchpad (push URL invalid, no dot component in any path), read-only to origin.

BLUF: 0 Blockers, 0 Majors, 3 Minors. 2 of 2 paths are inside OWNS-F. Overlap with sibling lanes and the other F branch is 0. The merge is clean and equals main plus the head blobs. The merge passes every test (5494/5494, 327 suites) but `npm run verify` reads `VERDICT: FAIL` until a counts commit sets scripts/verify-expected-counts.json to 5494 tests / 327 suites. That is the by-design precondition, not a code defect. The merge WOULD start a `Deploy demo` run (jobs gated, see row 9).

## Evidence
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | origin ref = `5cc88abe...` (read at start and end); main = `849b808c` (HISTORY.md only since the base `3929b794`) | `git ls-remote`; control `refs/heads/main` printed |
| 2 | Paths in OWNS-F | 2 of 2: `tests/e2e/shell-layout.spec.js` (M, `tests/e2e/*`), `__tests__/rd979-shell-layout-header-counts.test.js` (A, `+new rd<N>-*`, 979 is in the QUEUE, path absent at main) | fnmatch program over the kit OWNS-F block; controls: `backend/server.js` and the S-owned e2e file read False |
| 3 | Overlap | 0 with every `b1431/*` and `b1433/*` branch on origin and with the other F branch; no `b1430/*` ref. Open PRs: not read (no HTTP allowed); newest pull ref #185 has an empty diff against main | `git diff --name-only` per branch; `ls-remote` |
| 4 | Merge | `merge-tree --write-tree` rc 0, tree `253ca791`. main->merge changes exactly the 2 head paths with the head blobs (path, status and blob list byte-equal to base->head) | `git diff --raw`, `cmp` |
| 5 | Tree of head | `1cc79a75cd67`, equal to the builder's stated tree | `rev-parse HEAD^{tree}` |
| 6 | CI: verify at main / merge | main PASS 5493/5493, 326 suites. Merge: 5494 passed, 0 failed, 327 suites; `VERDICT: FAIL - committed expectation stale (expected 5493/326, measured 5494/327)`. Failed suites: none. | `scripts/verify-suite.sh --maxWorkers=2` under the jest lock |
| 7 | Added test | main->merge adds exactly 1 suite and 1 test (`rd979-shell-layout-header-counts`); removes none | suite counts 326->327, tests 5493->5494; single-file run |
| 8 | Red without the fix | the test planted on a copy of main (old header): RED, `total: header says undefined, program counts 11 / checked ... 7 / indexPins: NaN ... 4 / adminPins: undefined ... 3 / unchecked ... 4`. At the merge: 1 passed. | jest on the one file, `w-red` vs merge tree |
| 9 | Deploy demo | The merge TRIGGERS a run: `deploy-demo.yml` `push` to main, `paths-ignore` `**.md`, `docs/**`, `tests/**`; the new file is under `__tests__/` (not ignored). Jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'`; the variable was not read (no HTTP), so after landing the run must be read as all jobs `skipped`. | `git show origin/main:.github/workflows/deploy-demo.yml` |
| 10 | Other CI | `node -c` of build.yml was not run (the branch touches none of the three files it checks); gitleaks over the branch diff exit 0 (control: planted token exit 1). npm-audit and arm-ttk: no package or azure-marketplace change. Hosted CodeQL not run. | `gitleaks stdin` with the repo config |
| 11 | Repo-wide scans | Hidden-character (Cf) scan over all tracked text: 5 files / same 5 at main, merge. Name scan of added lines and the commit message: 0 hits; controls: 9 planted `_by_<name>_` fire, a longer word does not. Secrets, GUIDs, hosts, non-ASCII in added lines: 0. | python scans |
| 12 | CodeQL pre-scan | `new RegExp(` from a variable, hand-escape `.replace`, innerHTML, child_process, eval: 0 hits in added lines (all five patterns have a firing control). `vm.runInNewContext` runs the repo's own spec text, no external data. | grep with controls |
| 13 | Claims at source | Header numbers checked against the VENDOR table: 11 files, 7 hashed (4 `static/index.html integrity` pins, 3 admin pins), 4 font files with no hash. The four index pins equal the `integrity` attributes in `static/index.html`. Font hashes are recorded in the committed record `vendor` rows and compared in `diffRecords`. All true. | `git show`, `shell-layout-today.json` |
| 14 | Mutation probe | 7 mutants of the spec (header total, checked, admin pins, unchecked each changed; marker renamed; a 12th hashed pin; a hash removed) all read RED; the unmodified spec reads PASS. | node harness running the test file against mutated copies |

## Findings
| ID | Sev | Finding |
|---|---|---|
| F1 | Minor | The counts file is stale for this branch by design: a landing needs a counts commit first (see below), else the PR Build reads `VERDICT: FAIL`. |
| F2 | Minor | The test hard-codes `expect(c.total).toBe(11)`, so adding a legitimate VENDOR entry fails it twice (the census and the header). Intended friction, but a second place to edit. |
| F3 | Minor | The header says the four pinned files are "checked against the product's own `integrity` attribute"; the program compares against a copy of the value held in VENDOR, not against the HTML at run time. The old wording had the same shape; the values are equal today. |
| F4 | Minor (metadata) | Commit author and committer are `kamilDatasec <...users.noreply.github.com>`; the message and added lines carry no name. The same identity as the other lanes; noted for the merge history only. |

## Counts commit
`scripts/verify-expected-counts.json` is unchanged on this branch and equals main (5493 / 326). It does NOT match this branch's own suite: measured 5494 tests / 327 suites. The counts commit must set `"tests": 5494, "suites": 327` (regenerate with `npm run verify -- --maxWorkers=2 --update-counts` on the merged tree, then a plain run must read PASS). If the overflow branch lands first, its counts are unchanged and this branch still needs the same commit.

## Builder STATUS claims
| Claim | Grade |
|---|---|
| cause: 3 admin pins not 2; 4 fonts unhashed | true |
| red at base, green at head | true |
| tree `1cc79a75...` equals h2 less the counts file | true (head tree matches) |
| verify PASS 5494/327 after `--update-counts` | consistent: measured 5494/327, all passing |
| gitleaks 0, name scan 0, CodeQL pre-scan 0 | true |
| partition empty against other lanes | true |

## NOT RUN
- Hosted CodeQL, hosted gitleaks history scan, npm-audit, arm-ttk.
- The `CI_DEPLOY_ENABLED` variable and the open-PR list (no HTTP allowed): the deploy skip rests on the workflow text.
- The shell-layout recorder itself (boots servers on the jest helper's port band, outside the 9880-9889 block); this branch does not change its record.
- Jira (fence): RD-979 status not read.
- A separate verify at the head commit (head differs from the merge only by HISTORY.md, which the merge run includes).
