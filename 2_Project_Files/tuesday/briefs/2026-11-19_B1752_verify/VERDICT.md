GATE B1752: GO WITH FINDINGS @ 39f0c0c on main e036c96

Gate G1 Tier 1 (independent, Opus), round 1 of 2. Target: datasecau/MPS-Commercial-Calculator, branch b1746/mps-v13-lane1-projection-table-267, head 39f0c0c3eca15011f8dc22dd2a9646cc4f1f1ca2, lane base 317bbb14c7258023b1d2855a9bcce1b9b07b93f6, main e036c9661afab6f4339b53095afd37eb06026d5c. Clocks by `date`: start 18:49:32, end 19:05:51 AEDT 2026-11-19. Work under /private/tmp/b1752-gate/ (clone push URL invalid://no-push; logs in logs/).

## Findings

| Severity | Finding | Recommendation |
|---|---|---|
| Minor | The fixture's comment (`web/src/test/projectionFixture.ts:2-3`) says a browser that computed annual as monthly x 12 "would print a different figure". This is false for one cell. Click cost monthly 63.125 x 12 = 757.500 shows `$757.50`, the same text as the server's annual 757.504. Measured: my mutant M5 (money annual computed `Number(monthly) * 12`) left R3 green. R2, R8 and the money guard caught it (guard read `browser money arithmetic: 2`, `ProjectionTable.tsx:31 operator *`). No effect on the product; the other five annual cells and all 6 contract cells do differ. | A later test-only touch can give clickCost.annual a value whose 2 dp text differs from 757.50 (e.g. 757.6), or correct the comment. Not a landing blocker. |
| Minor | `docs/ENGINE.md:166` (X-39) still reads "Engine only: the contract and the screens do not carry it (the web table, T-V5-7)". After this merge the screen carries it, and the contract already did since #174. `docs/**` is outside this lane. | A docs follow-up updates the sentence. Out of lane, so not here. |
No Blocker. No Major. Two Minors.

Notes (no severity):
- (N1) At 390 px the table scrolls 64 px inside its own `.table-wrap` (overflow-x auto). The page itself scrolls 0 px, measured in Chrome by a gate probe. That is the project's convention (`itemised-summaries.spec.ts` `sideways()`: "Tables scroll inside their own wrapper, never the page"), so S12's "no sideways scroll" means the page.
- (N2) An empty `{}` or partial projection object throws a TypeError in render (gate rows G1 to G3). The contract makes all six members and all three figures required (`schema.ts:1845-1863`), and the Api builds all six (`PurchaseMapping.cs:269-277`). So only a non-conforming server could cause it; it shows nothing and is not a leak.
- (N3) For the word pack: the quote list already shows a staff column "Annual recurring GP (AUD ex GST)" (`QuoteList.columns.tsx:15`). W3 `Annual` and W10 `Recurring GP` are still new as standalone words. The census at main: 0 single-quoted literals for each of the ten (control `'Mono click'` 5). One double-quoted selector fragment `[data-label^="Annual"]` is in a test assertion (`QuoteList.columns.test.tsx:73`), not a screen word.

## Measured rows (the nine to rule on)

1. **SCOPE: PASS.**
   - `git diff --numstat 317bbb1 39f0c0c`: exactly six paths.
     - `itemised-summaries.spec.ts` 41 0
     - `purchaseQuotes.ts` 6 2
     - `ProjectionTable.test.tsx` 146 0
     - `ProjectionTable.tsx` 67 0
     - `PurchaseResultView.tsx` 2 0
     - `projectionFixture.ts` 13 0
   - `PurchaseResultView.tsx` gains one import line and one JSX line (`:201`). Its non-ASCII bytes are 16 on 5 lines at base and head, with 0 CR.
   - The spec keeps 15 non-ASCII bytes. Head minus (the import at `:9` plus the appended 40-line block) equals base byte for byte, so S1, S5 and S11 are unchanged.
   - Stub: the projection is added only under `internal(persona)`. The 2 removed lines are the `notPriced` signature and its call.
   - No CSS, config, package, generated, contract or workflow path changed.
   - Merge: `git merge-tree --write-tree e036c96 39f0c0c` rc 0, tree `dc202e96`. The merge differs from main by exactly the six head blobs, and from the head by exactly main's two C# paths. Its `web/`, `.github/` and `scripts/` trees equal the head's (web tree `3ab28b5`).
   - Refs: main = e036c96 and branch = 39f0c0c (gh api), ahead 1 and behind 1; merge-base = the lane base. Open PRs: 0.
2. **THE LEAK: NOT FOUND (attacked; no route reproduced).**
   - Component: absent, `null` and `undefined` give no table.
   - `PurchaseResultView`, with every purchase fixture the test folder offers (seller and analyst), each as-is, with `projection: undefined` and with `projection: null`: 3 tables, no Projection table, 0 words and 0 of 18 texts. The planted control G6 (seller plus fixture) finds 10 of 10 and 18 of 18.
   - Stub, for all five dev personas plus a null persona:

     | Persona | internal-metrics | projection key | `projection` in JSON | table |
     |---|---|---|---|---|
     | seller | no | no | 0 | no |
     | approver | no | no | 0 | no |
     | admin | no | no | 0 | no |
     | null | no | no | 0 | no |
     | analyst | yes | yes | 1 | yes |
     | adminAnalyst | yes | yes | 1 | yes |

   - Api, read at head (equal to the base for `src/`):
     - `PurchaseMapping.cs:264` sets `Projection = internalMetrics && ... : null`.
     - `PurchaseMapping.Restrict` `:342` sets `Projection = null`, and `Mapping.Restrict` calls it at `:229`.
     - The only other sites that set `Projection` are in the engine (`PurchaseCalculator.cs:269`, `QuoteCalculator.cs:627`).
     - Every read that serves a calculation is gated or restricted:
       - calculate, `QuoteEndpoints.cs:299` (`caller.SeesInternalMetrics`)
       - snapshot read, `:740-742` (Restrict)
       - home list, `:773` (Restrict)
       - version diff, `:938-941` (Restrict)
       - proposal, `:892` (internalMetrics false) and `Proposal.cs:426` (Restrict)
       - `QuoteFigures.cs:96/117` (staff columns only for internal callers)
     - `ProposalDto` carries no projection (`Proposal.cs:166` classifies `PurchaseResultDto.Projection` as internal).
   - Printed and customer documents: `PurchaseResultView` is rendered only by `QuoteScreen.tsx:572`. `proposal/OnePager.tsx:17` imports only the string constant `PURCHASE_BREAKDOWN`. No proposal, print or one-pager component renders the view or the table.
   - Act-as narrows on the server (header, intersection), and a persona switch remounts `QuoteScreen` (`App.tsx:20` key includes the persona), so no previous persona's calculation stays on screen.
   - The `.internal` class is a background colour only (`styles.css:80`); there is no hide-internal mode to bypass.
   - The Api's own leak tests (`LaneM11PurchaseProjectionTests.cs`): NOT RUN (C#, see NOT RUN). Hosted dotnet CI is their proof.
3. **NO BROWSER ARITHMETIC: PASS.**
   - The component touches the figures only through `formatCount` and `formatMoney`, with no operator, comparison, `Number`, `Math` or sort (read at source).
   - `noBrowserPricing.test.ts`: `browser money arithmetic: 0 (files scanned 106)`, 61 passed.
   - Planted `Number(monthly) * 12`: the guard goes red (`... 2 ...`, `ProjectionTable.tsx:31 operator *`).
   - The fixture's annual differs from monthly x 12 on all six raw values and on 5 of 6 shown texts (see the Minor finding). Contract / monthly is never a whole term.
   - R2 and R3 go red on a contract read from annual (M4).
   - The contract head has no bracketed multiplier: `schema.ts:1859` "contract is the result's own contract figure, not monthly x term"; `docs/ENGINE.md:166` "the contract column is not formed as monthly x term".
4. **THE WORDS: PASS.**
   - The screen-visible string literals of `ProjectionTable.tsx` are exactly W1 to W10. Everything else is code text: import paths, `row`, `col`, `internal`, `num internal`, `table-wrap`, type keys.
   - 0 JSX text nodes; 0 `title`, `aria-label`, `placeholder` or `alt` attributes.
   - Added view literal: only the import path. Added stub literals: only `'0'` x3.
   - Each word equals the kit's table and appears, lower case, in gap row V-55 (`2026-10-20_v13.4.1_GAP_ANALYSIS.md:178`, read at source).
   - The WORD-PACK lists all ten, where each shows, the "Not built" items (a) to (d) and the rental question.
   - No text says the product owner approved a word or the member name.
   - C-45 option a's detail is at `CLARIFICATIONS.md:660` and C-110's at `:2729`, read at source and matching the kit's quotes. Tuesday's reading is not contradicted by either.
5. **ACCESSIBILITY AND LAYOUT: PASS** (real Chrome, gate probe plus S12 and S13).
   - Caption `Projection` (the table's accessible name).
   - `thead th` scopes are col x3; `tbody th` scopes are row x6; the corner cell is a `TD`.
   - Page sideways scroll is 0 at 390 and at 1440. The inner wrapper scrolls 64 px at 390 (N1).
6. **CELLS AND MUTANTS: PASS.**
   - The new file is 9 of 9 green (R5, R6 and R7 print 0/0; R8 prints 10 of 10 and 18 of 18).
   - S12 and S13 are green at 1440 and 390 in the real stub-off run.
   - Gate mutants (each restored, `git diff --quiet` rc 0):
     - M1, the unguarded mount: R5, R6, R7 red.
     - M2, the stub gives every persona the projection: R9 red.
     - M3, Click cost and Click revenue heads swapped: R1, R2, R3 red.
     - M4, the contract column read from annual: R2, R3, R4, R8 red.
     - M5, annual computed as monthly x 12: the guard, R2 and R8 red; R3 green (Minor).
   - Deviation 1 (the constant specifier) is justified, measured (M6). With the component absent and the base view and stub, the constant specifier gives R1, R2, R3, R4, R8 and R9 red one by one with R5, R6 and R7 green. The kit's literal `await import('./ProjectionTable')` fails the whole file at collection ("Failed to resolve import ... Does the file exist?", no tests). So a row still fails alone when the component is absent, and the type cast keeps it type-checked.
   - Deviation 2 (one import line in the e2e spec) is needed for a static import in a Playwright spec. The existing rows are byte-unchanged (row 1). Accepted.
   - The builder's "more rows red than predicted" is expected, not vacuous: R2 reads each row head, R3 and R4 find rows by head, and R8 scans all 18 texts. My M3 and M4 reproduce the builder's mP2 and mP5 sets exactly.
7. **FULL WEB CHECKS at the merge (tree dc202e96; its web tree equals the head's)**, node v24.22.2 and npm 11.19.1 from the S8 folder (read-only); npm cache and prefix under /private/tmp/b1752-gate:

   | Step | Result |
   |---|---|
   | `npm ci --prefer-offline` | rc 0, added 273. All 273 tarballs came from the npm registry (my cache started empty; 273 `GET 200` in the log). |
   | `npm audit --omit=dev --audit-level=high` | rc 0, "found 0 vulnerabilities" (asks the registry, as CI does) |
   | `npm run lint` | rc 0 |
   | `npm test` | rc 0, **Test Files 147 passed (147), Tests 1625 passed (1625)**, 0 failed |
   | e2e stub on (port 9961) | rc 0, **260 passed, 17 skipped**, 0 failed, 257 s |
   | e2e stub off, no API (port 9961; API origin pinned to the empty 127.0.0.1:9969) | rc 0, **161 passed**, 0 failed, 0 skipped, 160 s; pdftotext present |
   | `VITE_MPSCALC_AUTH=entra npm run build && node scripts/check-bundle.mjs dist` | rc 0, `dist: 8 files, 1111036 bytes; markers found 0/57` (byte count and asset hashes equal to the builder's) |

   Positive control for the bundle check: a real marker (`mpscalc.stub.purchaseQuotes`) planted into a copy of dist gives `markers found 1/57`, rc 1. The stub is not in the production bundle. Ports 9960-9969 had 0 listeners before and after every run.
8. **CODEQL: rc 0 PASS** (`pr_codeql_check.sh --base e036c96... --head 39f0c0c... --lang javascript`; main used as base as commissioned). Verdict table:
   ```
   VERDICT TABLE (severity rule: security-severity >= 7.0, else problem.severity == error)
     results   head 0   base 0
     KEPT      total 0   high+ 0   (post-filter: primary or any related location START line is an added line)
     NEW       total 0   high+ 0   (rule,file,primaryLocationLineHash multiset, head minus base)
     GONE      total 0
     RESULT    rc 0 PASS (KEPT high+ 0, NEW high+ 0)
   ```
   - Head SARIF: 103 rules, 660 artifacts, including the four new and edited web files; the analyse log shows 105/105 queries evaluated.
   - Positive control (same CLI 2.27.4 and suite): planted `document.write(location.hash)` gives 1 result, `js/xss` at `planted.js:2`.
   - CodeQL csharp and actions: NOT RUN (no C# or workflow path in the lane; the C# extractor cannot run on arm64).
   - The hand rows over the 275 added lines (`new RegExp(var)`, hand-escape, `innerHTML`, `child_process`, `eval`, `document.write`) gave 0 hits each, each control firing. The sensitive-name row hit once, on the import path `../../auth/dev/devPersonas`, which writes no value, so it is not a finding.
   - The hosted CodeQL on the PR head stays the authority (0 hosted check-runs on the head today; no PR).
9. **TEXT: PASS.**
   - Added lines: 275, all ASCII, 0 Cf characters (planted U+200B control fires).
   - Ban list (Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, plus Wednesday, Tuesday, Friday), underscore-aware: 0 in added lines and 0 in the commit message, each `_by_<name>_` control firing.
   - B-numbers, seat or card ids: 0 (control `B1746 SEAT-M164 C-110` fires).
   - The only key is MPSCALC-267. No sentence says the product owner approved anything; the only `approv` hits are the existing helper `serveApproved`.
   - Commit: one, `kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`, one Co-Authored-By line, subject 111 characters.

## Builder STATUS claims graded

| Claim | Grade |
|---|---|
| Six paths; numstat view 2 0, stub 6 2, spec 41 0 | true |
| Non-ASCII 16 and 15 unchanged | true |
| npm test 147 files and 1625 tests, 0 failed | true |
| Guard 0 with files scanned 106 | true |
| e2e stub on 260 passed, 17 skipped | true |
| e2e stub off 161 passed | true |
| Bundle 1111036 bytes, markers 0/57 | true |
| npm audit rc 0 | true |
| CodeQL pre-scan 0 results | true (my tool run: 0 head, 0 base) |
| New file 9 of 9 | true |
| Red at base R1-R4, R8, R9 red; R5-R7 green | true (M6) |
| Literal specifier fails the file at collection | true |
| Mutant sets mP2 and mP5 | true (reproduced) |
| mP1, mP3, mP4 sets | not shown by me in the same form (my M5, M1 and M2 differ in shape); consistent |
| Package files unchanged | true |
| Clean merge expected | true |
| "0 registry fetches" for the builder's own `npm ci --offline` | not shown (machine cache; not re-measurable here) |

## FOUND / TESTED / HOW

- FOUND: no leak, no Blocker, no Major; two Minors and three notes above.
- TESTED: every web CI step at the merge, as CI runs them (ports moved to 9961, API origin pinned to an empty port in my block); the CodeQL tool step with a positive control; my own leak attack file (7 rows, quarantined after: /private/tmp/b1752-gate/_quarantine/gateLeak.b1752.test.tsx); six mutants; the layout probe in Chrome (appended to my clone's spec copy, restored, `git diff --quiet` rc 0); the Api mapping and every calculation-serving endpoint read at source; the text, name and id scans with controls.
- NOT RUN:
  - the dotnet job, including the Api leak tests `LaneM11PurchaseProjectionTests.cs`, and the python job (no C# or python path in the lane; hosted CI is the proof);
  - `scripts/package.sh`;
  - CodeQL csharp and actions;
  - hosted CI and hosted CodeQL (no PR exists; Tuesday's at landing);
  - a real API behind the browser (the e2e is route-served or stub, as CI);
  - Firefox and Safari (CI uses Chrome only).
- HOW: own clone `/private/tmp/b1752-gate/clone` (index and working tree = merge tree dc202e96, never pushed), logs in `/private/tmp/b1752-gate/logs/`, scripts in `/private/tmp/b1752-gate/scripts/`, CodeQL work in `/private/tmp/b1752-gate/codeql/`. Load1 stayed between 4.9 and 9.9 throughout; one heavy job at a time. Nothing deleted (my attack file is quarantined). No push, PR, Jira, deploy, az or hosted-host request; network use was gh GETs, the clone, and the npm registry for `npm ci` and `npm audit`.
