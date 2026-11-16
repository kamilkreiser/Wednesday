GATE B1646: GO WITH FINDINGS @ 3669403 on main 41a75c5

Gate tier G2. Branch b1642/mps-lane-me2-dialog-own-box-390px, READY sha 3669403445736ba0d4c7e1a9e91d2619df3b0b7f, base 56bfe232cbf4c98a9752f949f1f279d755565750.
Main read by git ls-remote at the end: 41a75c5e7358c5413d693908235e9b758955bf97 (moved from 56bfe232 during the gate by one commit that touches only tests/MpsCalc.Api.Tests/FleetLineIdTests.cs, PR #206 landed). Merge run against BOTH mains (see row 2). The web results below were measured at main 56bfe232 and at the head; since main moved by no web path, they carry to main 41a75c5 (the merge tree of head onto 41a75c5 is main plus the one spec blob, 620de10a). Hosted CI on the merged main is the final proof of that carry.
I took no lock in the MPS project folder (read-only to me; I wrote nothing there). Work folder /private/tmp/b1646-gate/ (own clone, worktrees main and head, push URL set invalid, never pushed).

## Findings
| # | Sev | Finding |
|---|---|---|
| 1 | Minor | Builder STATUS line counts are false: it says the file went 55 -> 89 lines with 34 lines appended. Measured: 55 -> 95 lines, 40 added lines (`git diff -U0`: `@@ -55,0 +56,40 @@`), 0 removed. The change itself is as claimed; only the count is off. |
| 2 | Minor | Builder ran no whole-stub baseline (it said so). Gate did: main 258 passed + 17 skipped, head 260 passed + 17 skipped (+2, skips unchanged). |
| 3 | Minor (gate note) | npm ci made one registry call: the npm audit POST to registry.npmjs.org (advisories/bulk). 0 package fetches (all from cache). I also ran two read-only `gh api -X GET` reads (open PR list and main sha) before I switched to `git ls-remote`; no hosted HTTP beyond that. |

No Blocker, no Major.

## Rows
1. Refs: ls-remote of branch = 3669403445736ba0d4c7e1a9e91d2619df3b0b7f (equal to READY). Changed paths: 1 of 1 = web/e2e/dashboard-390.spec.ts; 1 commit ahead of base. Open PR #206 (b1640, FleetLineIdTests.cs) overlap 0 (now merged into main as 41a75c5); b1641 branch (web/src/api/stub/purchaseQuotes.ts, stubApi.test.ts) overlap 0. Commit address = repo's own, author = committer; one Co-Authored-By trailer (Claude Sonnet 5.5, as the builder's session reminder gives).
2. Merge: `git merge-tree --write-tree` clean (rc 0) at main 56bfe232 -> tree 94e6efdf, equal to the head tree (main plus the head spec blob). At main 41a75c5 -> clean (rc 0); diff of that merge tree vs main = exactly the one file, blob 620de10a = head blob.
3. Diff at merge: exactly one spec file; removed lines 0 (own `git diff -U0`: one hunk `-55,0 +56,40`).
4. Predicate: `left < 0 || right > client` (both edges); message prints left, right, clientWidth; control plants `style.minWidth = '600px'`. In MY copy (head worktree, undone with cp, cmp equal after each):
   - mE1 (styles.css:124 `.drawer { min-width: 600px; ...`): new row RED `dialog left -210 right 390 vs clientWidth 390`; control green; 6 passed, 1 failed.
   - mE2 (control minWidth 390px): control RED `dialog left 0 right 390 vs clientWidth 390`; new row green; 6 passed, 1 failed.
   - Right-edge-only plant (width 600px, flexShrink 0, backdrop justifyContent flex-start, planted into the new row): the row CATCHES it, RED `dialog left 0 right 600 vs clientWidth 390`.
   - File alone at head, stub step: 7 passed.
5. Whole steps (port 9975, load1 under 24 on two reads 120 s apart, not independent; lsof 9975 count 0 after every run; no timeout wrapper):
   - stub: main 56bfe232 `Total: 275 tests in 19 files`, run 258 passed 17 skipped rc 0 (4.3 m); head `Total: 277 tests in 19 files`, run 260 passed 17 skipped rc 0 (4.3 m). Main + 2: yes.
   - api-off: main `Total: 157 in 8 files`, 157 passed rc 0 (2.6 m); head 157 in 8 files, 157 passed rc 0 (2.6 m). Equal: yes.
   - Head: whole web vitest 146 files, 1610 tests passed, 0 failed (includes pdftotextTimeout scanner); `npx eslint .` rc 0; `npx tsc -b` rc 0.
6. CodeQL CLI 2.27.4, javascript pack, suite javascript-security-and-quality.qls (201 rules), databases in /private/tmp/b1646-gate/cq: spec at main 0 results, spec at head 0 results. New vs main: 0. (Pre-scan only; no planted-hit control run in this gate; not hosted CodeQL.)
7. Scans over the 40 added lines and the commit message: non-ASCII lines 0; Cf/Cc 0; underscore-aware ban-list scan 0 for all nine names (control `x_by_Kam_y` fires); B-numbers 0; secrets/tenant ids/hosts 0; `new RegExp`, innerHTML, child_process, eslint-disable, waitForTimeout, test.only, screenshot/video/trace, backslash escape all 0 (`eval` 2 = Playwright `.evaluate`). package.json and lockfile untouched.
8. Claims graded: one file true; 0 removed true; line counts 89/34 FALSE (95/40); mE1 message true; mE2 message true; stub list 275->277 and api-off 157 true; file alone 7 passed true; whole stub/api-off pass true (260 passed 17 skipped; 157 passed); vitest 146/1610 true; eslint, tsc rc 0 true; CodeQL 0 results true; the dialog is 390 wide at 390 px true (the new row is green at base).
9. Tier G2: no security-shaped issue (tests only, no product byte).

## NOT RUN
- Hosted CI and hosted CodeQL (the proof for the merged main 41a75c5; its one new commit touches only a C# test file, so no web or e2e path changed).
- Gate did not re-run the web steps at main 41a75c5 itself (carry argued above).
- dotnet/C# jobs, scripts/package.sh, entra build, CodeQL csharp (cannot extract on arm64).
- CodeQL planted-hit control.
