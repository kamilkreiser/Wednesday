GATE B1514: GO WITH FINDINGS @ 0315bd9 on main aae420f

Tier G2. Head 0315bd9b3404abab45cad23a7a270c7f4587abe3 (4 commits, ahead 4 behind 0), main aae420ff8a9e3f8a34be0aff22f8934e1708911a. Landing: head-pinned squash. MPSCALC-110 code change: none (Blocker check passed).

## Refs and lane
- ls-remote of refs/heads/b1514*: ONE ref, b1514/mps-w3a-web-look-print = 0315bd9b (equals READY). Main read now = aae420ff (the builder's base; unmoved).
- 6 of 6 changed paths inside OWNS: web/e2e/home-tiles-fill.spec.ts, web/src/proposal/{OnePager.tsx, OnePager.test.tsx, RentalDocument.tsx, RentalDocument.test.tsx}, web/src/styles.css. No siteLetters files. Nothing for 110 (no one-pager.css, ONE_PAGER_CAPS, ProposalPage change).
- Open PRs: #181 (14 files under infra, scripts, tools/demo) and #180 (tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs): overlap 0. No sibling lane pushed ref touches the six paths.
- Merge: main is an ancestor of head, `git merge-tree --write-tree` clean, tree 0097f1f6b721 equals the head tree (main plus head blobs).

## Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| 1 | Minor | Scrollbar sensitivity of the media-query edges (698, 918, 1138, 1357) is unmeasured: edges measured in headless Chrome with overlay scrollbars. A classic scrollbar moves the viewport-vs-container edge by about 15 px, so on such a browser a sliver of roughly 1358-1375 px (six tiles) could still wrap 5 + 1 (builder item 3, DERIVED, agreed). The new rows sit 40 px inside each edge, so hosted CI is not affected. | 1 px sweep below |
| 2 | Minor | Administrator at 601-697 px keeps a lone fifth tile ([2,2,1]); six tiles [2,2,2]. Recorded, not built (Q-W3A-3). Unchanged from main. | sweep |
| 3 | Minor | rental-book.spec.ts "draft: Full prints" failed once at head with `spawnSync pdftotext ETIMEDOUT` in a 37-row group run; passed 3 of 3 alone and the whole group passed 37 of 37 on re-run; main group 37 of 37. This is the known stdin-pipe flake the kit names; the spec is outside CI and the diff. | e2e-head-print logs |
| 4 | Minor | Seller page has a pre-existing horizontal overflow (scrollWidth above clientWidth from 601 px up) at main and at head alike (574 vs 575 widths); not caused by this branch, tile layout is unrelated. Observation only. | sweep |
| 5 | Minor | ProposalDocument.tsx:326 still letters purchase cards with String.fromCharCode(65 + i); not reachable above 20 (MaxSections = 20 at src/MpsCalc.Api/Quotes/PurchaseValidation.cs:14). Builder claim true. | source |

No Blocker, no Major. Hosted CodeQL pre-scan (step 7): 0 hits (see Scans).

## CI by program (main aae420ff vs head 0315bd9b; Node 24.22.2, npm ci offline from a copy of a seat cache, no network)
| Job / step | main | head |
|---|---|---|
| web npm ci | rc 0 | rc 0 |
| web npm run lint | rc 0 | rc 0 |
| web npm test (vitest) | 145 files, 1517 passed, 0 failed | 145 files, 1531 passed, 0 failed |
| test names (sorted, comm) | n/a | lost 1 (the OnePager title with "1 more rates", renamed in the same hunk), gained 15, net +14 |
| web production build + check-bundle | rc 0, 8 files, markers 0/57 | rc 0, 8 files, markers 0/57 |
| e2e, stub mode (npx playwright test, CI config, whole CI set) | 168 passed, 5 skipped | 192 passed, 5 skipped (+24 = the new rows); skipped set identical (md5 equal) |
| e2e, api-off mode | 22 passed | 46 passed (+24) |
| home-tiles-fill, b46-home, b100-quote-390, v1b-frame (head, stub, 2 runs) | n/a | 80 passed twice (42, 15, 5, 18) |
| Specs outside CI that read the changed files: rental-book, proposal-purchase, proposal-buttons, itemised-summaries (stub off, pdftotext) | 37 passed | 37 passed (one flake, finding 3) |
| python job tests that read the paths: test_ci_workflow.py, test_demo_doc.py (search with positive control found only these two) | OK | OK |
| Repo-wide tracked-file scan for Cf (format) characters, 699 files | 17 | 17 (equal; none added) |
Merge-state CI equals head CI (merge tree is the head tree).

## Red without the fix (own copy, fix removed)
- Vitest, OnePager.tsx restored to main and siteLetter set to the old expression: 10 red, all with real assertion messages: moreRates(1) received `and 1 more rates (see full proposal)`; the edited 7-rate row; letters 26, 27, 51, 52, 701, 702 received `[`, `\`, `t`, `u` and two non-ASCII; the 28-site book; the 500-site book received `Stream <U+0234>` against `Stream SF`. Green by design as guards (fix removed): letters 0 and 25, the 8-rate row, moreRates(2), moreRates(10).
- Playwright home-tiles-fill with styles.css at main: 15 of 24 new rows red (six-tile roles at 1317, 1280, 1178, 1097, 1100, 958 px; Administrator at 1097, 1100, 958), 27 passed. With the one-rule CSS of the earlier head (94fec47): exactly the 3 Administrator rows at 1317, 1280, 1178 red, which is what ANSWER-1 asked.

## Probes
- 1 px sweep 500 to 1500 px, seller (6 tiles) and Administrator (5), main vs head, same Chrome:
  - six tiles: main [1x6] to 600, [2,2,2] 601-697, [3,3] 698-917, [4,2] 918-1137, [5,1] 1138-1357, [6] from 1358. Head: [3,3] across 698-1357; everything else identical to main.
  - five tiles: main [1x5], [2,2,1] 601-697, [3,2] 698-917, [4,1] 918-1137, [5] from 1138. Head: [3,2] across 698-1137, [5] from 1138; below 698 identical to main.
  - So six tiles never show a lone tile 698 and up; five tiles keep one row from 1138 (ANSWER-1 met); 601 px and below unchanged. Edges 698, 918, 1138, 1357/1358 confirmed.
- Only Dashboard.tsx uses `.kpis`; tile counts there are 5 or 6 (appended list); rule 2 (`.kpis` at 918-1137) therefore cannot strand a tile on another count. `:has(> .kpi:nth-child(6))` picks the six-tile case: confirmed by the sweep (five tiles unaffected).
- siteLetter: indices 0, 25, 26, 27, 51, 52, 701, 702 and 499 (SF) all asserted and run; loop has no cap and no table.
- Code-fact sentences: String.fromCharCode occurrences, the phrase "more rate(s)" (OnePager.tsx:6 comment, :37), MaxSections = 20, MaxFleetLines = 500 all read at source and as the builder wrote.

## Scans (added lines 108, 4 commit messages)
- Ban-list names (standard step 7 list), underscore-aware, 0 in added lines and 0 in messages; a planted _by_<name>_ control fired. (Commit author and committer addresses are the repo's configured identity, outside the scan.)
- Non-ASCII 0; Cf 0 (control fired); secrets/ids/hosts/guids 0; B-numbers and card ids 0; price-like digit.digit 0; skip/only/fixme/eslint-disable/ts-ignore/waitForTimeout 0.
- Removed lines: 7, all on the kit's list (3 `//` comment lines in the spec, OnePager.test.tsx title and expectation, OnePager.tsx:37, RentalDocument.tsx:40); none in styles.css.
- CodeQL pre-scan, JS/TS: `new RegExp(` with a variable 0; `.replace(/[...]/g` hand-escape 0; innerHTML/dangerouslySetInnerHTML 0; child_process 0. Python row: no Python file in the diff; os.chmod/makedirs mode/os.open/Path.chmod/0o modes 0. Hits: none, no Major from CodeQL.
- New product word: only `and 1 more rate (see full proposal)` (112), equal to the ruling's text; AA/AB per the 131 ruling.

## Claims graded (builder STATUS and ANSWER-1)
| Claim | Grade |
|---|---|
| Head 0315bd9b, ahead 4 behind 0, six files | true |
| Main moved once (acd6aec to aae420ff), used as base | true (head is on aae420ff; main unmoved since) |
| Vitest 1517 to 1531, lost 1 (rename), gained 15 | true |
| Lint, typecheck, build, check-bundle rc 0 | true (lint, build, bundle run here; typecheck is inside build `tsc -b`) |
| Edges 698 / 1357 (six), 918 / 1138 (five) | true (own sweep) |
| Before/after perRow table in ANSWER-1 section | true at every listed width |
| home-tiles-fill 42 of 42 in both modes; b46 15, b100 5, v1b 18 | true (42 in api-off and stub CI sets; 80 in stub set of four) |
| 15-then-24 new rows red at base | true (15 red; Administrator rows red on the one-rule CSS) |
| 110 numbers: cover room 50-131 mm on 9 of 9, short form 3 pages, rental 1/1/1/2/3 pages | true (reproduced, B109ROOM and B86RENTAL lines identical) |
| infra test_infra.py needs Bicep | not shown (not re-run here; in the hosted python job Bicep is installed) |
| PartnerRebate.b456 timeout once at load | not shown (not seen in 2 whole-suite runs here) |
| package.sh rc 0 and zip sha | not shown (not re-run) |
| ProposalDocument.tsx:326 unreachable above 20 | true by source |

## NOT RUN
- Hosted CI, hosted CodeQL (JS and Python), hosted Chrome, any hosted site.
- dotnet build and test (no src/ or tests/ path in the diff); infra/tests (needs Bicep, none on this machine); the full python loop (only the two tests that read changed paths); scripts/package.sh; gitleaks (regex scan for ghp_, AKIA, BEGIN, eyJ done instead).
- smoke.spec.ts, b83-feedback-attachments.spec.ts, print-book-styles.spec.ts, b100-picker-many.spec.ts (left out of CI by the config for their stated reasons); a Linux or Windows Chrome; a classic-scrollbar browser.
- Deploy trigger: this repo has no deploy workflow (ci.yml only, no deploy job); a merge deploys nothing.
