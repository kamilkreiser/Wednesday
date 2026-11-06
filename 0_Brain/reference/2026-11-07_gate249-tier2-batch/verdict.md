# Gate 249 verdict, TIER 2 batch, round 1 of 2 (Secuura / Blockchain)

Readings (UTC, all by `git ls-remote`): start 20:28:53Z develop b27f5fb30f4a (branch develop); end 20:42:24Z develop b27f5fb30f4a. Every PR head equal at start and end. A GO is a statement about the SHA.

| PR | head | verdict |
|---|---|---|
| 2062 KS-864 | 71566cce6101 | GO |
| 2082 KS-1534 | 75c1282a64dc | GO WITH NOTES |
| 2083 KS-1505 | 72182689bace | GO WITH NOTES |
| 2084 KS-1858 | 223499281cb9 | GO WITH NOTES |
| 2086 KS-736 | c70f8182f43d | GO WITH NOTES |

No PR is NEEDS TIER 1. Evidence class for all findings below: MEASURED AT RUNTIME unless marked READ ONLY (vitest in my by-SHA trees under /private/tmp/g249/w).

## Environment caveat (applies to everything)
No `npm install` (network is git-only). I built the trees with `git archive` of each head, copied node_modules from the main checkout, built packages/shared/dist with local tsc (zod type errors, JS still emitted) and shimmed `zod` to the v4 entry because the installed root zod is 3.25.76 while shared needs v4. Effect: ks1364 (zod-openapi) cannot load, on develop and on the PR alike; whole api-gateway at 2083 = 165 files pass, 1735 of 1735 tests, 1 file unloadable (same on develop). Node v26.8.1, not 24. No Docker, no box, no live probe.

## PR 2062 (GO)
Diff read whole: +15/-1, one test file. THROWS set in the fetch stub, 3 cells, the beforeEach clear. Does what the READY says, nothing else.
- TESTED: 11 of 11 green on the head. Planted mutant A in system-status.ts:436 (`unreachable` counts as healthy): 3 cells red, all by assertion (the 3 new cells). Mutant B (`.slice(0,1).every`): 4 red, including 2 of the new cells. Product restored, diff clean.
- Not tested: real-socket probe, whole suite, tsc/eslint/test-types, Node 24.
- Overlap: older PR 2032 (KS-864, 2026-11-06, head 375084cf) also edits this test file and system-status.ts; `git merge-file` of the two versions is clean (rc 0). Its open/closed state I did not establish.

## PR 2082 (GO WITH NOTES)
The removed line: the COMPLETENESS cell's `expect([...RAN].sort()).toEqual([C1..C4, R1..R5])`. It is replaced by the same list plus `N1`, and the new cell does `RAN.add('N1')`, so nothing is weakened and the completeness check is strengthened. Nothing else in the diff is removed (+21/-1).
- F-1 (Minor) ks1534 test, new fixtures at lines ~63-66. FOUND: the claim "closes the ends-only gap" holds, but a non-string at the LAST index of a list of 3 or more is still pinned by no cell (lists with a trailing non-string are length 2 only; the length-5 fixture has its null at index 3). TESTED: mutants on `allowListHoldsANonString` in connectorAllowList.ts: ends-only 5 red; first-three-only 5 red; empty-string-counts-as-nonstring 1 red (N1 only); `.some()` (skips holes) 5 red; skip-index-1 5 red; but **skip the last element when length >= 5: 11 of 11 green, and skip the last when length >= 3: 11 of 11 green (survive)**. HOW: python substitution of the loop bound, test file run, source restored. Fix shape for the owner: add `['SSD_DOCUMENT','X','Y',1]`-style fixtures with the non-string last.
- Not tested: whole suite, the create/info routes beyond this file.

## PR 2083 (GO WITH NOTES). Product code: confirmed by my own diff, not NEEDS TIER 1
index.ts diff read whole (+16/-6). Non-comment changes are exactly: `const sameBytes = nextRaw === openApiSpecRaw;` and the log call becoming `if (sameBytes) log('warn', ...) else log('info', ...)`. Parse (`parseYaml`, `buildSpecMap`) and the three assignments are unchanged and in the same order; the whole block still sits inside `if (process.env.NODE_ENV !== 'production')`. `log` already accepts 'warn' (index.ts:210). Matches the seat's statement. The other 4 files: new test, two doc fragments, limiter-catalogue. I checked all 8 shifted `sourceLine` values against the head's index.ts: each lands on its `app.use('/api/auth/...', rateLimit({` line (991, 1003, 1010, 1017, 1024, 1031, 1038, 1063).
- TESTED: new file 5 of 5 on head; the same file against develop's index.ts: 4 failed, 1 passed (by assertion). Mutants: `false` instead of the comparison 4 red; warn changed to info 4 red; compare only first 1000 chars 2 red; **compare by length: 5 of 5 green (survives); compare after `.trim()`: 5 of 5 green (survives)**. Product restored, diff clean.
- F-1 (Minor) ks1505 test: the only "changed" control appends a comment line, so no cell has a changed spec of equal length or a whitespace-only change. A same-length real edit would be reported by a length-compare as "same, restart", and a whitespace-only change is warned as "same". The shipped code compares exact strings, so no defect today; the pin is loose. 
- F-2 (Info, READ ONLY) behaviour: a second fs.watch event more than 200 ms after the first for one save, with identical bytes, now logs the "restart api-gateway" warning although the reload was fine. Non-production only; log noise.
- Not tested: a real replaced bind mount, Node 24, the Playwright unit directory, ks1364.

## PR 2084 (GO WITH NOTES). The "green by construction" tamper
Diff read whole: +93, new file, no product code. 6 of 6 green on head (34 of 34 across the 5 ks1858 files).
- The listed tamper (answered token written without its spaces) stays green: that is a tamper of the test's own fixture, not a product mutant, so it is not a hole in what the test detects, but it is a trap for a later "tidy" of ANSWERED. It is real only in the sense that nothing guards the fixture; the control cell uses an unspaced token, so removing the spaces leaves 6 of 6 green.
- F-1 (Minor) the pin is about the FIRST send only, and only about trimming. TESTED: google token sent with `.toLowerCase()`: 6 of 6 green (survives; fixtures are already lowercase). GitHub emails call (github.ts:112, `Bearer ${access_token}` when the profile has no email) trimmed: 6 of 6 green (survives; the fixture user has an email so that second send never fires). GitHub profile call trimmed (line 97): 1 red, as claimed. So "sent exactly as answered on all five" is true of the profile call only; GitHub has a second send of the same token that no cell reaches. Fix shape: one GitHub cell with a profile lacking email, asserting the `/user/emails` header, and a mixed-case fixture token.
- Not tested: real Request wire normalisation, real provider, whole auth suite.

## PR 2086 (GO WITH NOTES)
Card secuura-ks736-made-up-token-result-1106 read: ruled `b` (record the guards and fix the check, no behaviour change, ruled 2026-11-06 21:04). The PR matches: tests only, no product code, no login added.
- No assertion is weakened: the 6 removed lines are the six existing reason strings, each kept verbatim with a `+ specGateRecord(...)` appended. The existing 9 cells are unchanged; 14 of 14 pass on head (develop: 9 of 9), reproduced by me, not taken from V 25th. The reasons still carry the "open half of KS-736" wording; the appended text states it is superseded. Not a security judgement beyond a test read, so not NEEDS TIER 1.
- Mutants of my own: strip bearerAuth from GET /api/billing/bundles in the real spec: K2 and K4 red. Give POST /api/credentials/verify bearerAuth: K2 and K4 red. Disable authed-method collection in specRouteMap.ts:48: K2, K2 control, K4 red. All restored.
- F-1 (Minor, scope) **Disabling the real auth gate in index.ts (`if (!hasBearer && !hasApiKey)` made `if (false)`): ks570 14 of 14 stay green.** The new K cells ask the gate's two helper functions about the spec; they do not run the `app.use` gate. The PR says this ("narrow claim") and the gate is covered elsewhere: with the same mutant ks1244, ks1461, ks1469 show 8 red cells, but those cells are on credentials, referrals and governance; I did not establish equivalent app-level coverage for billing, nft or certifications. The reasons' claim "refused with no credential" for those three rests on the spec data plus the gate's code, READ ONLY.
- F-2 (Info) K3 matches seven phrases per reason by regex and "GET <mount>" as a substring; wording drift fails loud, rewording is cheap. Fine.
- Overlap with PR 2060 (head 796ea55fb8eb, unchanged at end): 2060 changes the one line 211 `platform_admin` to `super_admin`. `git merge-file` of 2086 over 2060 against develop base: clean, rc 0, no conflict markers, 'super_admin' present in the merged file (line 265). Whichever merges second merges develop in. NOT tested: running the merged file (needs 2060's product change).
- Not tested: live probe, valid/expired/wrong-tenant token, backend check behind certifications, the other 66 operations.

## Shared paths among the five
Changed paths are pairwise disjoint (2062: ks864f test; 2082: ks1534 test; 2083: index.ts + its test + 2 fragments + limiter-catalogue.ts; 2084: new auth test; 2086: ks570 test), checked by `git diff --name-only` per PR. `git merge-tree` was refused by the session hook as a write verb outside the project, so I did no merge-tree; the only shared file is with PRs outside the batch (2060, 2032) and I used `git merge-file` on blobs for those. Sequencing: 2083 shifts index.ts line numbers by +10; any other open PR touching index.ts above line ~990 or the auth rate-limiter mounts would stale limiter-catalogue.ts. Among PR refs 2030-2095 only 2083 touches either file. 

## Conduct
- Findings only: nothing fixed, posted, or run against any box; network used for git clone/fetch of blobs only. I wrote only inside this gate folder and /private/tmp/g249.
- The commission said remove the clone; the QA template's no-rm rule wins, so **/private/tmp/g249 is left in place, 12 GiB** (repo blobless clone, six by-SHA trees under w/, node_modules copies, plus w/_quarantine_2026-11-07 holding the first node_modules copies I moved aside). It can be deleted by a human.
- The session hooks blocked `git fetch`/`checkout`/`merge-tree` with -C on the clone (path outside the project); I used one `git clone` (with a PR-ref refspec) and `git archive` instead.
- My first mutation harness lines had mistakes (a YAML edit that left a duplicate key gave "no tests"; two runs before the zod shim gave "no tests"); I discarded those readings and re-ran. All planted defects restored by diff against saved originals.
- A grep-case advisory was shown on case-sensitive greps; none of them was used for a zero claim.
- Not done: Node 24, Schemathesis, Akto, Playwright, full auth suite, tsc/eslint/test-types ratchets, round 2.
