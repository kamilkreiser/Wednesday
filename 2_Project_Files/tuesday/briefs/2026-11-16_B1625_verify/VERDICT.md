GATE B1625: GO WITH FINDINGS @ f825a9e on main efe6cdd

Gate G2 for the 390 px dashboard spec lane (one new file, web/e2e/dashboard-390.spec.ts). Independent run in /private/tmp/b1625-gate/clone (push URL invalid, nothing pushed). Main moved twice during the gate (5e80009 -> 72fa8d9 -> efe6cdd); the merge was redone against efe6cdd and the whole web chain re-run there. Head and main re-read at the end: head f825a9ecf86dcbbc0e33b1c6c6bf1b3ba22347d6 (equals READY), main efe6cdd5e156c20bb9b17c36d170f1bf0355f60a.

## Findings
| # | Sev | Finding |
|---|---|---|
| 1 | Minor | The branch is based on 5e80009 and is 3 commits behind main (72fa8d9, 9c219cb, efe6cdd). Not a defect: the merge is clean at efe6cdd and every comparison below was run on the merge. Landing by squash is unaffected. |
| 2 | Minor | The builder's STATUS (residue 1) says its push script printed a moved main and pushed anyway; checked here: the move touched none of the paths the kit lists as read. No effect on the head. |
| 3 | Minor | Builder residue 2 and 3 (an rm -f of a not-yet-existing marker file; npm's built-in audit POST during npm ci). Process notes, no product or diff effect. |
| 4 | Minor | tools/demo/test/test_run_demo.py has 2 failures (the two Ctrl-C tests of C5StopsExactlyWhatItStarted) in this non-tty shell, identically at main and at the merge. Not the lane; hosted CI is the proof for the python job. |
| 5 | Info | The new spec checks the PAGE scroll width with the New quote dialog open; it does not measure the dialog's own box (builder said so; agreed). The new file runs in the stub step only (in neither list of playwright.config.ts). |

No Blocker, no Major.

## What was verified (own instruments)
- Refs: git ls-remote of the branch = f825a9ecf86dcbbc0e33b1c6c6bf1b3ba22347d6 = READY. One commit; author and committer both the repo's own address (the lane's identity). Changed paths vs main: exactly `A web/e2e/dashboard-390.spec.ts` (1 of 1 in OWNS). Open PRs at the end: #201 (web/src/api/stub/purchaseQuotes.ts, stubApi.test.ts) and #202 (docs/API.md, docs/ENGINE.md) were read at the start and both have since landed in main; shared paths with this lane: 0.
- Merge: `git merge-tree --write-tree` against 72fa8d9 and again against efe6cdd: rc 0, clean; merge tree = main tree plus the one head blob (blob f25d3bcd identical to the head's; `diff --name-status main merge` shows only the A).
- Whole web chain at the merge with efe6cdd (offline `npm ci --offline --ignore-scripts` rc 0; vitest 146 files / 1610 tests passed, 0 failed (at 72fa8d9 merge: 1580; the +30 is #201's stub tests); eslint rc 0; `tsc -b` rc 0).
- Playwright lists: stub main 270 in 18 files, merge 275 in 19; api-off 157 in 8 files both.
- Stub step WHOLE: main (72fa8d9 tree, new spec set aside) 253 passed + 17 skipped, 0 failed; merge 258 passed + 17 skipped, 0 failed (+5 exactly); re-run at the efe6cdd merge 258 passed + 17 skipped, 0 failed. The five new rows all appear green in the log.
- api-off step WHOLE: main 157 passed; merge 157 passed (twice, at 72fa8d9 and efe6cdd merges). Unchanged.
- New spec alone at merge: 5 passed.
- Red without the fix (own copy, each undone, `git diff --quiet` rc 0, cmp equal): mB1 (`.kpis` + `min-width: 600px`, styles.css): the 3 role rows and the form row RED, each `scrollWidth 616 vs clientWidth 390`, control GREEN. mB2 (planted control width 300 px): control RED (`scrollWidth 390 vs clientWidth 390`), 4 layout rows GREEN.
- Scans of the one added file (48 lines) and the commit message: non-ASCII 0 (control rows in the standard); Cf characters 0; ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite; underscore-aware, case-insensitive) 0 hits in the file and the message (control `x_by_Kam_y` fires); new RegExp, hand-escape, innerHTML, eval, child_process, eslint-disable, waitForTimeout, .only, sensitive-name row, URLs, tenant words, B-numbers: all 0. gitleaks: random ghp_ canary rc 1; the spec rc 0; commit range rc 0. The commit author name field holds the repo's configured identity, which is the lane's own (not an added line).
- CodeQL CLI v2.27.4, javascript-code-scanning.qls (87 rules), database in /private/tmp/b1625-gate/db-js over the spec: 1 of 1 file scanned, 0 results. Control: a planted innerHTML-from-location and an unescaped-backslash replace gave js/xss and js/incomplete-sanitization (2 results). Pre-scan only, not hosted CodeQL.
- Deploy trigger: this repo's CI is ci.yml only; the diff is an e2e test file; no deploy workflow exists in this repo's .github; nothing is triggered by this merge beyond ci.
- Port 9972: lsof listener count 0 after every browser run and at the end. No timeout wrapper on a browser run.

## Claims in the builder's STATUS (graded)
| Claim | Grade |
|---|---|
| Stub subset 125 passed; api-off -g '390' 13 passed (Part A, at 5e80009) | not shown here as such: I ran the WHOLE steps instead (stub 253 -> 258, api-off 157), which contain those rows, all 0 failed. Counts of the subsets not re-measured. |
| Part B five rows green at base; mB1 turns four layout rows red, control green; mB2 turns control red | true (measured above) |
| Whole stub step 258 passed + 17 skipped; api-off 157 passed | true |
| vitest 146 files / 1580 tests at 5e80009 | true at that tree (1580 at the 72fa8d9 merge; 1610 at efe6cdd) |
| eslint rc 0, tsc rc 0 | true |
| stub list 275 in 19 files, api-off 157 in 8 | true |
| CodeQL pre-scan 0 results | true (own run, with control) |
| Diff is exactly one file, ASCII, no names | true |
| home-tiles-fill.spec.ts:221 is a 641 px control, so the kit's FACT 4 holds for 390 px only | not re-read; unshown |

## NOT RUN
- Hosted CI, hosted CodeQL (the proof for the dotnet, python and package jobs).
- dotnet job; package job (scripts/package.sh); the entra production build (`VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist`): the diff touches no product, package or lock file, so it is not affected; not run.
- python job: tools/leakscan test 25 tests OK; tools/demo test 2 failures at main and merge alike (finding 4); the infra and scripts tests were not run (they read none of the changed paths: grep of tests, scripts, infra, tools, src and .github for web/e2e, package-lock, web/package.json, playwright hits only tools/demo, tools/leakscan and ci.yml).
- tools/leakscan diff and files modes: NOT RUN (their lists live under .local, which this gate does not read).
- Mutant runs were at the 72fa8d9 merge; the spec and styles.css are unchanged at efe6cdd (the move touched only docs and web/src/api/stub).
- Stub main at efe6cdd was not re-run on its own (main at 72fa8d9 gave 253 + 17; efe6cdd's change is a unit-test and stub-API file set; the merge at efe6cdd gave 258 + 17 = +5).
- Axe (MPSCALC-139 clause 4): not in this lane (Q2 = NO); stays open.
