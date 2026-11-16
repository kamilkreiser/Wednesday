GATE B1644: GO @ c527989 on main 56bfe23

Gate tier G2 (Sonnet). Branch b1641/mps-lane-ms2-stub-followups (kit B1641, MPSCALC-408). Work folder /private/tmp/b1644-gate (own clone, push URL invalid, nothing pushed). I took no lock in the MPS project folder (read-only to me; I wrote nothing there). Node v24.21.0 (the HPSM-POC .tools node24, read-only). Loads before heavy runs: 7.8 / 10.2, then 11.0 / 15.0, one heavy job of mine at a time.

## Findings
| # | Sev | Row | Result |
|---|---|---|---|
| 1 | - | Refs | `ls-remote` of the branch = c5279894be4b6f0a48115073c5977f17c571f416 = READY. Main re-read three times (start, before outputs, at the end) = 56bfe232cbf4c98a9752f949f1f279d755565750 = base; open PRs 0. |
| 2 | - | Paths | Merge paths: 2 of 2 are web/src/api/stub/stubApi.test.ts and web/src/api/stub/purchaseQuotes.ts. Sibling b1640 (tests/MpsCalc.Api.Tests/FleetLineIdTests.cs) and b1642 (web/e2e/dashboard-390.spec.ts, now on origin) share 0 paths. |
| 3 | - | Merge | `git merge-tree --write-tree origin/main head` rc 0, tree ce2bb2d4...; it equals the head tree (0 differing paths); main == base, so the head runs below are the merge runs. |
| 4 | - | Removed lines | Part A (e2b7930e): 0 removed. Part B: 7 removed by `git diff -U0` program; each is reproduced exactly by substituting the constant's text into the matching head line (7 of 7); literal-bearing lines 7 at base, 3 at head (the three constant definitions). |
| 5 | - | Titles verbatim | By program: each of the three constants equals the base literal byte for byte (3 distinct literals, counts 2/3/2 at base; at head each literal appears once, in its constant). Fourth text "Editing a draft needs the Seller role. (stub)" 2 at base, 2 at head, unchanged. Added lines hold no non-ASCII and no Cf character. |
| 6 | - | Red without the fix | Own copy, 136 tests in the two lane files, 0 red with no mutant. mA1 (c<31): 1 red, the code-31 row. mA2 (c<33): 1 red, the existing space row. mA3 (c<=158): 1 red, the code-159 row. mA4 (c<=160): 1 red, the existing no-break-space row. mA5 (target !== undefined): 1 red, the null row. mB1 (guarded internal title reworded): 1 red, the comparing row (internal). mB2 (manual, in requireCopyable): 1 red, comparing row (manual). mB3 (price, requireCopyable overrides): 1 red, comparing row (price). mB4 (fixed-rate refusal reworded): 2 red, the existing fixed-rate row and the comparing row. mB5 (manual constant reworded): 2 red, the existing manual item and manual line rows; the comparing row stays green because both paths read the one constant. Every file restored; `git diff --quiet` rc 0; content equal to the original by program. |
| 7 | - | Null row not vacuous | The row asserts `JSON.stringify(stored.draft.assumptions)` contains `"targetGrossMargin":null` as the analyst before the Seller's Duplicate; mA5 turns exactly it red. |
| 8 | - | Whole web | Vitest at main 146 files, 1610 passed, 0 failed; at head 146 files, 1616 passed, 0 failed; by name program (`LC_ALL=C comm`): lost 0, gained exactly the six new test names (two code rows, one null row, three comparing rows). eslint rc 0 and `tsc -b` rc 0 at both, no output. |
| 9 | - | Entra build | At head: `VITE_MPSCALC_AUTH=entra npm run build` rc 0; `node scripts/check-bundle.mjs dist` rc 0 ("8 files, 1109639 bytes; markers found 0/57"). |
| 10 | - | Playwright, as CI runs them, port 9974 | Stub step: main 258 passed, 17 skipped, rc 0; head 258 passed, 17 skipped, rc 0 (EQUAL). api-off step: main 157 passed rc 0; head 157 passed rc 0 (EQUAL). 0 failed in all four. `lsof -nP -iTCP:9974 -sTCP:LISTEN | wc -l` = 0 before and after each run. No run wrapped in `timeout`. |
| 11 | - | CodeQL | CLI v2.27.4, javascript-code-scanning.qls (87 rules) over the two files (copied into a work folder, database there): 0 results at main, 0 at head, so 0 new. Control: a planted file made the same suite report js/incomplete-sanitization and js/xss. This is a pre-scan, not hosted CodeQL. |
| 12 | - | Scans | Ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite), underscore-aware, over added lines and both commit messages: 0 each (planted `_by_<name>_` control fires 1 for each). No B-number, no `eslint-disable`, no `new RegExp(`, `innerHTML`, `child_process`, `eval`; no sensitive-name write; no host, tenant or subscription id. gitleaks over the 2 commits: no leaks (random `ghp_` canary rc 1). |
| 13 | - | Author | Both commits `kamil.kreiser@datasec.com.au` author and committer: the repo's own address per the kit, not a ban-list hit in a message or added line. |
| 14 | - | Claims | STATUS claims graded: whole web 1610 -> 1613 -> 1616, 0 failed: true (1610 and 1616 measured; the 1613 midpoint not run, Part A alone). Mutants mA1-mA5, mB1-mB5 as predicted: true. Entra build + check-bundle rc 0 at head: true. `rm -f` that matched nothing and an npm audit POST at `npm ci`: not independently checkable by me (disclosures only). |
| 15 | Minor | Trailer | The two branch commits end `Co-Authored-By: Claude Sonnet 5.5`; the repo's two most recent squashes on main use `Claude Opus 5.5`. Immaterial on a head-pinned squash, since the squash body carries the usual trailer. |
| 16 | Minor | Not shown | The ticket's survivor `if (target)` (a numeric 0 target) and the fourth duplicated text are reported by the kit, not built; not a defect of this lane. |

Deploy: nothing in this lane triggers a deploy (dev stub files under web/src/api/stub/ only; MPS has a hosted deploy per card).

## NOT RUN
- Hosted CI and hosted CodeQL (the gate's CodeQL is a local pre-scan).
- Part A alone as its own whole suite (1613): the head state and base were run; Part A's 3 rows are covered by name and by mutants.
- Registry: `npm ci --prefer-offline --no-audit` rc 0 at both trees; the log holds no fetch line, but I did not instrument the network; a registry fetch cannot be ruled out by me.
- Python, dotnet and the other CI jobs: no changed file is read by them.
