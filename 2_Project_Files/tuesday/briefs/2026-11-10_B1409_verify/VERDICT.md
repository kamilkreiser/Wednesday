GATE B1409: GO WITH FINDINGS @ 26400b5 on main 0b9aad0

Tier G1 (product code), per the kit's S8. Gate run 12:13-12:55 AEDT 2026-11-10 in my own clone under the session scratchpad (push URL set to INVALID-NO-PUSH; nothing pushed). Last origin read by `git ls-remote` over the deploy key at 12:52:49 AEDT: branch `b1409/mps-api-contract-quote-validation` = 26400b57895bc5bd2482cd6187756b13eb5e6b05 (= READY sha); main = 0b9aad04db5af9482c8a70ce26a6b0e9bb635b2e; `b1400/mps-web-unit-pins` = 67aa6921. Main moved during the gate, from c5cd009a (12:13) to 0b9aad04 (the B1400 lane's change, MPSCALC-369: only `web/src/screens/bom/PriceReason.test.tsx` and `PurchaseBomEditor.test.tsx`). The dotnet job ran on the c5cd009a merge (the new commit changes no dotnet path). The web job and the merge check were run again on the 0b9aad04 merge.

Toolchain: dotnet SDK 10.0.401 (the project-local one; global.json pins 10.0.100 with rollForward latestFeature). Node `node --version` = v24.22.2, npm 11.19.1, from Tuesday's tools path, prefixed in the same command (ci.yml pins `node-version: 24`).

## Steps and results
| # | Step | Instrument | Control that can fail | Result |
|---|---|---|---|---|
| 1 | Refs | `git ls-remote` (deploy key) | main read in the same call | branch = READY. merge-base(main, head) = 31234f5f (S2). Head is 2 ahead and 7 behind 0b9aad04 (6 behind c5cd009a, the builder's count). PASS |
| 1 | Paths in OWNS | `git diff --name-only S2 head` against the kit's allowed list | the B1403 gate's earlier listing; 33 paths differ between main and head, so the filter does not pass everything | 10 of 10 inside OWNS: `docs/API.md`, `docs/api/openapi.json`, `src/MpsCalc.Api/Contracts/Dtos.cs`, `src/MpsCalc.Api/Quotes/{Proposal,PurchaseMapping}.cs`, `tests/MpsCalc.Api.Tests/LaneM11{PurchaseProjection,QuantityRuleResult}Tests.cs`, `web/src/api/generated/{SOURCE.txt,openapi.snapshot.json,schema.ts}`. PASS |
| 1 | Overlap with main's moves (#169-#173) | `comm -12` of the head paths and the paths in `S2..main` (29 paths) | self-overlap of the branch = 10 | 0. PASS |
| 1 | Overlap with sibling lanes and PR heads | fetched all 172 `refs/pull/*/head` and every `b14*` branch, each diffed from its merge-base with main | b1409 itself = 10 | Every PR head that touches these paths has landed (its "(#n)" squash appears in the main log), except #17, #105 and #139: old heads that the stamp's "open PRs 0" (S3, RELAYED) rules out. #167-#172 are on main. b1400 (67aa6921) touches 2 web test files: 0 overlap. A three-way `merge-tree` of main+head with b1400 is clean (tree 74ac2201), and it equals the tree of the 0b9aad04 merge, which is now real. PASS |
| 2 | Merge | `git merge-tree --write-tree` in my own clone, against c5cd009a and again against 0b9aad04 | blob-by-blob comparison of each head path | clean both times (rc 0; trees 03b9739c and 74ac2201). The merge's diff from main = exactly the 10 head paths, every blob equal to head's (0 mismatches). PASS |
| 3 | CI `dotnet` (`ci.yml:42-43`) | `dotnet build MpsCalc.slnx -c Release` + `dotnet test --no-build`, counts taken from the trx files | the planted-fault runs in row 4 make the runner exit rc 1 | main c5cd009a: 0 Warning(s), 0 Error(s); Engine 743/743, Import 196/196, Api 3452/3452. head: 0/0; 743, 196, 3381. merge: 0/0; 743, 196, **3466** (= 3452 + 14). By name, main to merge: lost 0, gained 14, all `LaneM11*`. PASS |
| 3 | CI `web` (`ci.yml:61-66`) | `npm ci` (offline, from a copy of the user's npm cache), `npm run lint`, `npm test` with the JSON reporter (not CI's flags), `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` | a planted 1-byte drift in the snapshot: `contract.sync.test.ts` fails 2 rows, rc 1 | all 4 steps exit 0 at main, head, the c5cd009a merge and the 0b9aad04 merge; 144 files, 1492 passed, 0 failed, 0 skipped each time; the name lists of main and merge are equal (0 differences). The contract sync and contract tests (4 rows) pass at head and at both merges. Bundle: 0/57 markers. PASS |
| 3 | CI `python` (the one file that reads a changed path) | `python3 -I scripts/tests/test_deploy_pre1.py` (reads `Dtos.cs`) | - | 27 tests OK at main, head and merge. The rest of the python job (bicep, infra) reads no changed path: NOT RUN. PASS |
| 3 | Repo-wide hidden-character scan | python, Unicode category Cf over every tracked file | planted U+200B = 1 | 17 at main, head and merge, all in existing test fixtures; the changed files add 0. PASS |
| 4 | Red without the fix | copy A: attribute removed + mapping never fills; copy B: filter removed, a zero projection mapped when the engine has none, `Restrict` keeps the projection, the attribute set to `Always`, `Note` ignored when null | each copy builds with 0 warnings; rc 1 | A: 7 of the 14 new tests red. B: 10 of the 14 red, including all 7 that stayed green under A. **Every one of the 14 new tests goes red under a planted fault.** PASS (finding F3) |
| 5 | Closed lines | the builder's ALREADY-ON-MAIN lines, re-read at main c5cd009a | constant count `MaxWalkEntriesListed` = 11 in PurchaseValidation.cs | 325, 338 and 339 hold at every cited line: PurchaseValidation.cs:32, :131, :136, :142, :147, :160, :165, :309; QuoteEndpoints.cs:1434 and :1450-1451 each have 1 `.Take(PurchaseValidation.MaxWalkEntriesListed)`; QuoteWalkCaps.cs:17, :367, :375, :387, :634. 169 is held by C-68 (`CLARIFICATIONS.md:1348-1356`, "No contract change is made until you approve the exact text on that card"); no approval is on record. PASS |
| 6 | Probes (the contract and its restriction) | 3 gate-written Api rows run in DevStub and Entra (a throw-away copy) | `Restrict` keeping the projection turns the snapshot probe red (2 of 6, rc 1) | (a) Submitted snapshot: an internal-metrics read has `projection`, a restricted read has none, and the restricted calculation is still there. (b) The proposal of a projection quote carries no `projection`, `recurringGrossProfit`, `clickCost` or `managedServiceCost`, and still carries none with the mapping's internal-metrics filter planted away: the allow-list holds on its own. (c) A restricted GET of the quote and of the quote list carries no `projection` (it does not discriminate: it also passed with the filter planted away). Every response is checked against openapi.json by the test client, including the 14 new rows; nothing the server sends is outside the contract. The member is response-only: no request DTO and no endpoint reads it, so the server refuses no input the contract accepts. PASS |
| 6 | Docs code-facts | `docs/API.md` section and the openapi descriptions, against the source | - | true at source: annual = monthly x 12 (`PurchaseCalculator.cs`, `Of`); contract figure from the result's own contract figures; null when there is no supplies source and no fee (:291-294); formed only on the priced path (:269); no Api input can state a fee (0 `ManagedService` inputs under `src/MpsCalc.Api`); `Restrict` sets `Projection = null`; allow-list classes as stated (`Proposal.cs`). PASS |
| 6 | Re-sync of the generated copies | `node web/scripts/sync-contract.mjs 26400b57` in a copy | - | snapshot and schema body byte-equal; only the `Contract source` header line differs (F1) |
| 7 | Scans | python `(?<![A-Za-z])<name>(?![a-z])` (case-insensitive) over 347 added lines and both commit messages; secret, GUID and host regexes; gitleaks 8 | planted `x_by_Kam_y`, `_by_Waite_` and `Paul` fire 3/3; planted `B1409`, `SEAT-M110` and a `ghp_` token fire; random `ghp_` canary: gitleaks rc 1 | ban names 0; B-number or seat id 0; secrets, tenant/subscription GUIDs, hosts 0 (only `analyst@example.test` in a test and the attribution email); Cf 0; gitleaks over `S2..head` rc 0, "no leaks found". Non-ASCII added lines: 2, both the generator's U+00B7 in the header (`sync-contract.mjs:27`, same as the line it replaces). PASS |
| 9 | Tier | S8: G1 | - | no security-shaped issue found: the new member is internal on every read path probed. |
| - | Deploy | `.github/workflows/ci.yml` at head | - | no deploy job; a main push keeps a package artifact only. A merge deploys nothing. |

## Findings
| ID | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | `web/src/api/generated/SOURCE.txt` and the `schema.ts` header name commit `7e9afb18`, a temporary commit that is not on the branch or at origin. The blob id and sha256 they record do match the branch's openapi.json, so the sync test is green. The builder disclosed it and cites a precedent (`52adf97f` at base). | Re-sync from 26400b57: only that header line differs (2 lines, 2 files). If a reachable pointer is wanted, re-sync after the squash; optional. |
| F2 | Minor | STATUS claim "`grep -n 'MPSCALC-169'` in CLARIFICATIONS: 1 line, :1348" is false: there are 2 lines. The second (:1995) is a records pass listing 169 among hits it reported and did not touch, not an approval, so the C-68 hold stands. | `/usr/bin/grep -n 'MPSCALC-169'` prints :1348 and :1995 |
| F3 | Minor (not vacuous) | 7 of the 14 new tests stay green with the fix simply removed (the two 378 control rows; the 368 absence rows: no filter, none when the engine has none, no member on the wire, and both copies of the no-supplies-model Api row). Each one guards a wrong fix, not the missing one: under planted wrong fixes every one goes red. The project rule counts a planted fault. | copy B: 10 of 14 red, covering all 7 |
| F4 | Info | The commits' git author name is a ban-list name (the repo's local git identity); the commit messages and added lines carry none. Main's commits are authored `kamilDatasec`, so the author line differs from main's convention. A squash by the landing account sets its own author. | `git log --format=%an` |
| F5 | Info (gate process) | My first web test run was rooted wrongly (`npm exec` from the shell cwd). Vitest collected files under the Tuesday folder; they failed to import and nothing was written there except a vitest cache `node_modules/.vite/.../results.json` in the Tuesday root. I MOVED that to `scratchpad/g1409/_quarantine_2026-11-10/TUESDAY-root-node_modules` (nothing deleted); Tuesday's `git status` no longer lists it. That first `npm ci` also printed npm's update notice; whether npm's update check contacted the registry is UNMEASURED. Later runs set `NPM_CONFIG_UPDATE_NOTIFIER=false` and printed no notice. The reported web results are all from the correctly rooted runs. | `out/web-head` (void) vs `out/web-head2` |

## Builder STATUS claims, graded
| Claim | Grade |
|---|---|
| Head 26400b57, 2 commits on S2, read back | true |
| 378: 3 rows, red first on unchanged code (1 red, 2 controls green) | true (copy A: the same 1 red; the 2 controls are killed in copy B) |
| 368: 8 row methods, 11 test names | true (5 + 3 methods; 5 + 3x2 names) |
| 368: 6 planted faults, each row killed | not re-run as written; my own plants kill all 14 rows |
| dotnet 0 warnings; Engine 743, Import 196, Api 3367 -> 3381; lost 0, gained 14 | head 3381 true; gained 14 true (on the merge, by name); base 3367 at S2 not re-run (main has moved, 3452 there) |
| web npm ci/lint/test/build all rc 0; 144 files 1492 -> 1492; contract sync tests green at head | true |
| 2 non-ASCII added lines, both generator-written | true |
| gitleaks over the range rc 0 | true |
| compare main...head ahead 2, behind 6, files exactly the 10 owned | true at c5cd009a (behind 7 since 0b9aad04) |
| `grep -n 'MPSCALC-169'` in CLARIFICATIONS: 1 line | false (F2) |
| C-68 bars a 169 contract change | true at source |
| ALREADY-ON-MAIN 325 / 338 / 339 file:line | true at main c5cd009a |
| node v24.22.2 / npm 11.19.1 | true |
| Main moved only onto paths outside the lane | true (and again at 0b9aad04: 0 overlap) |

## Landing order
No overlap with any live lane. B1400 has already landed (0b9aad04) and merges clean with this head. Contract changers that land later must re-sync the generated copies, because the sync test pins byte equality.

## NOT RUN
- Hosted CI (dotnet, web, python, package) and CodeQL: hosted CI on the PR is the proof.
- CI `python` job beyond `scripts/tests/test_deploy_pre1.py` (bicep needs `az bicep install`; no other python test reads a changed path). CI `package` job (`scripts/package.sh`): no changed path feeds it beyond the build already run; hosted CI is the proof.
- The dotnet job on the 0b9aad04 merge: that main commit changes only two web test files, so the dotnet tree is identical to the c5cd009a merge that was run.
- The dotnet build used `dotnet restore --source ~/.nuget/packages` then `build --no-restore` (an offline restore), not CI's implicit online restore.
- Web tests ran with the JSON reporter on macOS, not CI's flags and runner.
- Open-PR state through the GitHub API, and Jira: not read (fence: no HTTP to hosted hosts). Overlap was shown from fetched refs instead.
- e2e / Playwright: not run (not this lane's).
- No push, no PR, no Jira, no mail, no az, no deploy.
