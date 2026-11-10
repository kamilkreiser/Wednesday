GATE B1400: GO WITH FINDINGS @ 67aa692 on main c5cd009

Tier G2 (tests only), per kit slot S8. Project MPS Calculator, repo datasecau/MPS-Commercial-Calculator.
Branch b1400/mps-web-unit-pins. Gate run 12:13 to 12:25 AEDT 2026-11-10. Node v24.22.2 / npm 11.19.1 under
the Tuesday tools PATH, printed for every web job (ci.yml:58 pins `node-version: 24`). The machine's v26 was not used.

## Findings

| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | Minor (claim owed) | The MPSCALC-369 acceptance ("named rows pass in all of 20 whole-suite runs started at a load average above seven") is still NOT fully met. The builder ran 0 runs above 7 and said so. This gate ran 9 whole-suite runs at head started at load1 14.31 to 46.58: 9 of 9 rc 0, 1492/1492 each, six rows 6/6 passed, slowest row 683 to 850 ms per run. **Also measured:** main passed 4 of 4 runs started at load1 27.19 to 45.42 (six rows max 791 to 915 ms), so the original 5 s timeout did NOT reproduce here even at main. The change's benefit under real load is therefore shown only by the planted 50 ms timeout, not by whole-suite load. The gate stopped at 13 runs because its own back-to-back runs were driving load to about 46 on a shared machine. | `out/load/runs.txt` and the JSON per run (gate scratchpad, see below) |
| F2 | Minor (scope, stated) | A sixth row, "building a purchase quote ... a new draft switches to purchase; ...", was changed although the ticket names five. It is inside an owned file and test only, and the builder states it in STATUS and in the commit body. No assertion or title was changed. | `git diff 97cf7a9a 67aa6921` |
| F3 | Minor (metadata) | The branch commit's author and committer are the owner's personal name and work address (git metadata, not message text). The name scan of added lines and the commit message is clean (0). Recent main commits are authored by the org's GitHub account. The squash creates a new commit, so check the landed author. The builder's claim "the same identity sister seat branches carry" is only partly true: one sibling lane branch matches, another uses the org account. | `git log -1 --format='%an'` on two sibling branches and main |
| F4 | Info | The open half of MPSCALC-334 is still open: `getQuoteFigures`, `recordOutcome` and `duplicateQuote` each have 0 rows in `stubApi.test.ts` at main (src counts 1, 4 and 2; control `createQuote` 30). The builder raised it, and it is not this lane's work. | grep -c at main c5cd009 |

No blocker and no major. No security-shaped issue.

## Checks (instrument / control)

1. **Refs.**
   - `git ls-remote` (deploy key, read only) shows `refs/heads/b1400/mps-web-unit-pins` = 67aa692124fc740a31fac33705c01f0e044cb19a, which equals READY.
   - Main is c5cd009ae3d7fea788a55ec1fb354151ee003deb. merge-base 97cf7a9a; head is ahead 1, behind 2.
   - Main since base: 3a7a804 (#171, Feedback/**) and c5cd009 (#172, QuoteRefusalOrder.cs), 11 files, 0 under web/. #169 and #170 are ancestors of base (8d665e3 and 97cf7a9).
   - OWNS: 2 of 2 changed paths are in the lane list; outside count 0 (control: planted `web/x.ts` counts 1).
   - Overlap: 0 lane-path hits over 32 other refs (PR heads #150 to #172 from `refs/pull/*/head`, plus every sibling lane branch of the sweep). Control: this branch hits 2. The e2e lane's branch is not on origin.
2. **Merge.**
   - `git merge-tree --write-tree main head` in the gate's own clone (push URL invalid, never pushed) gives rc 0, tree 29a26dd2.
   - Merge vs main: exactly the 2 lane paths differ, and both merge blobs equal the head blobs (5895c771, 447d1552).
3. **CI job web** (the only job reading the changed files; .github unchanged, diff rc 0). Commands as ci.yml:61-66 from web/, except a JSON reporter on `npm test` and `--prefer-offline` on `npm ci` (rc 0, local cache):

   | tree | lint | test (files / passed / failed / skipped) | build + check-bundle |
   |---|---|---|---|
   | main c5cd009 | rc 0 | rc 0: 144 / 1492 / 0 / 0 | rc 0: 8 files, 1108407 bytes, markers 0/57 |
   | head 67aa692 | rc 0 | rc 0: 144 / 1492 / 0 / 0 | rc 0: same |
   | merge (local af91196) | rc 0 | rc 0: 144 / 1492 / 0 / 0 | rc 0: same |

   - By program (compare.py over the full test names): head vs main lost 0, gained 0, gone 0; merge vs main the same. Test titles are therefore unchanged.
   - The runner fails on a red: the planted-load runs below exit rc 1.
   - Repo-wide hidden characters over tracked files at all three trees: the same 6 pre-existing files with Cf characters (all .cs or .py test fixtures; none web, none in the lane) at main, head and merge. Control: a planted U+200B counts 1.
   - Relative links over tracked .md: 9 files, 1 link, 0 broken at main and merge. Control: a planted broken link counts 1.
4. **Red without the fix** (both files, `--testTimeout=50`, Node 24):
   - main: 6 of 6 target rows time out ("Test timed out in 50ms.").
   - head: 6 of 6 pass (181 to 627 ms).
   - head with the six budgets removed (a throw-away tree, 6 replacements by program): 6 of 6 time out.
   - Unbudgeted sibling rows time out in all three trees, as expected at 50 ms.
5. **Closed lines at main c5cd009.**
   - MPSCALC-198: the row is still at FleetGrid.test.tsx:210 and the key at FleetGrid.tsx:100 `key={rows.keys[i]}`.
     - Mutant `key={f.lineNumber}` in a throw-away tree: FleetGrid tests rc 1, 1 failed (exactly the :210 row), 27 passed.
     - Unmutated main: 28/28, rc 0.
     - This also re-runs the row-key mutant check the builder could not.
   - MPSCALC-334: stubApi.test.ts is 350 lines, and `'mpscalc.stub.createdQuotes'` is at check-bundle.mjs:35.
6. **Probes.**
   - Removed lines holding expect(/it(/describe(/test(: 0 (control 1).
   - Added `.skip/.only/todo/eslint-disable/ts-ignore/setTimeout/sleep/waitFor(`: 0 (control `it.skip` 1).
   - Budgets added: 6. All carry the repository's own existing comment text, as at QuoteScreen.addSectionWait.test.tsx:80 and BomClassColumn.test.tsx:129.
   - Default testTimeout is the 5 s default: vite.config.ts `test: {` at :124 sets none.
   - The module-level `userEvent.setup({ delay: null })` matches 14 existing test files on main.
7. **Scans** (added lines and commit message, python re, case-insensitive):
   - Ban-list names: 0 (control: two planted `_by_<name>_` tokens from the list fire 2).
   - B-numbers, seat ids, secrets, GUIDs: 0 (each control fires).
   - Hosts: only `noreply@anthropic.com` in the attribution line.
   - Cf: 0; non-ASCII: 0.
   - gitleaks 8.30.1: `ghp_` canary rc 1 first, then range 97cf7a9a..67aa692 rc 0, "no leaks found".
8. **Deploy.** The only workflow is ci.yml, which has no deploy job and no secret. A merge to main runs CI and keeps a package artifact (7 days). Nothing deploys.

## Builder STATUS claims

| Claim | Grade |
|---|---|
| Base 97cf7a9a; main c5cd009a 2 ahead, 11 files, none under web/ | true |
| Branch = 67aa6921, ahead 1 / behind 2, files exactly the 2 test files | true |
| Diff 2 files, +41 -35; removed assertion/title lines 0 | true |
| web job main and head: lint, test 144/1492/0/0, build + bundle rc 0 | true (re-measured, plus merge) |
| Bundle 8 files, 1108407 bytes, markers 0/57 at both | true |
| Red-first at 50 ms: main 6/6 red, head 6/6 green, no-budget 6/6 red | true (re-measured by whole-file runs, not `-t`) |
| Six 15_000 budgets; no assertion or title changed | true |
| Lock files equal main vs head | true |
| gitleaks canary rc 1, range rc 0; name scan 0 | true |
| Commit subject 104 characters by `wc -c` | true |
| 20/20 whole-suite load runs green, all started below load 7 | not shown (the builder's logs were not read by the gate) |
| T=200 cascade into the price-audit row | not shown (not re-run) |
| The "above load 7" acceptance clause is NOT MET | true (see F1; still partial after 9 gate runs) |
| Commit identity matches sister seat branches | partly true (F3) |
| MPSCALC-198 / -334 ALREADY-ON-MAIN for this lane | true (198 by mutant; 334 by source) |

## NOT RUN

- Hosted CI and CodeQL: they are the landing proof.
- CI jobs dotnet, python and package (package needs dotnet, and python needs `az bicep`). None of them reads the changed files; package's web half is the same build plus check-bundle as above.
- e2e / Playwright (not in CI, not owned).
- Open-PR state by the GitHub API (fence: no HTTP to a hosted host). The proxy was `git ls-remote refs/pull/*/head` with diffs of every PR head from #150 to #172.
- The rest of the ticket's 20 runs above load 7: 9 done, stopped to spare the shared machine.
- The gate did not take the project's `.tools/.heavy-lock-*` slots, because writing there is outside the gate's output fence. It ran every suite serially instead.

Gate scratch (not committed): /private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/017af1b7-c908-4074-bd26-db14582a6cfd/scratchpad/b1400v (clone, worktrees main/head/merge/nobudget/mut198, out/).
