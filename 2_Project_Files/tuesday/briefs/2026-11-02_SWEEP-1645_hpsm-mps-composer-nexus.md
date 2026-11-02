# SWEEP 1645 2026-11-02: lanes for HPSM-POC, MPS Calculator, Security Composer, NexusAI (read-only; drafter C8, Sonnet), DELTA on SWEEP-1305

Test (as 1305): no new user-facing word, no owner ruling, no production touch; Tuesday's own call is named and does not fail it. `date` first read 16:42:29 AEDT, last 16:50:48. Live, not free: G288 (b1097), G289 (b1095), H104 (b1113), M77 (`web/src/api/contract.sync.test.ts`), R141 (MPS records: MPSCALC-269 and three gap tickets it is filing: coming, not lanes), R136/R139 removals. Panes 16:50: no Composer or NexusAI pane. Load1 (`uptime`) 5.04 (16:42), 5.36 (16:44), 10.51, 11.01 (16:50): the launch rule (below 7 on two reads) is NOT met now.

## Controls
- Jira (1305's `fetch.py`): HPSMPOC 436 rows/max 436/unique 436/foreign 0/truncated 0, Done 292, Backlog 141. MPSCALC 369/369/369/0/0, Done 139, Backlog 230. PCOMP 119/119/119/0/0, Done 26, Backlog 93. RD 919 rows, max 923, To Do 372. `fleet/board_count.sh jira` agrees on each; control `key = HPSMPOC-311 AND status = Done` = 1; a nonsense status was refused.
- PRs (`gh api -X GET .../pulls state=all per_page=100`, each project's `GH_CONFIG_DIR`): rows = max = unique: HPSM 275, MPS 145, Composer 111, NexusAI 154. Open: MPS #121, #120 (`web/package-lock.json`); Composer #91 (`package.json`, lock), #86 (`apps/web/package.json`, lock), #85 (draft HOLD K6, 57 files); others none.
- Mains: HPSM `5f128fb8`, MPS `0d4022b9`, Composer `69b01339` and NexusAI `68b080d1` (both unchanged since 1305). Trees truncated False. Every `file:line` was printed by `grep -n`/`sed -n` on `contents/<path>?ref=<main>`. Parents: #275, #143-#145, Composer #111 = 1 (squash); NexusAI #154 = 2.

## 1. Landed since 1305 (ended 13:11:55), by PR at source
| PR | Merged AEDT | Squash | Files | Check runs |
|---|---|---|---|---|
| HPSM #275 (HPSMPOC-420/421; head b1104) | 15:02:25 | 5f128fb8 | 24: 3 API endpoint files, 2 API tests, 4 contract files, 6 `security/*`, 3 `CustomerShell*`, 6 other web | 19; 12 read (11 success, 1 skipped), 7 unread |
| MPS #143 (366, 345; b1116) | 14:17:38 | 17fc0dbc | 3: `docs/IMPORTER.md`, 2 `QuantityAudit*.test.tsx` | 8 of 8 success |
| MPS #144 (257, 367; b1117) | 15:41:35 | e970f7eb | 3: `ENGINE.md`, `PurchaseCalculator.cs`, 1 test | 8 of 8 success |
| MPS #145 (269; b1093) | 16:23:08 | 0d4022b9 | 14: `API.md`, `openapi.json`, `Program.cs`, 4 `Templates/*.cs`, 4 tests, 3 generated web | 8 of 8 success |
Composer, NexusAI: none since #111, #154.
- No PR: HPSMPOC-311 closed by evidence pass B1124 (comment 16:19:44, no file changed, 1000 of 1000 green): NH4 is done.
- Jira delta: HPSMPOC-421 Done 16:19:27; -420 commented, open; MPSCALC-366, -345, -257, -367 Done (16:20 to 16:21); -369 restated 16:21:51; PCOMP-119 created 13:52:24; PCOMP-98/-114 commented 13:52, still Backlog. Done: HPSMPOC 290 to 292, MPSCALC 135 to 139.
- Branches (`compare main...<b>`): b1113 now on origin @ d8a9456f (7 files); b1095 @ 76116bc6 (4); b1097 @ f9f1f490 (8). Paths held: b1095 `SqlServerWakeRetry.cs`, `NarrativeOutputValidator.cs`, 2 tests; b1097 `globals.css`, shell test + spec, `partner/*`; b1113 `ClientPacks.tsx`, `EngagementOverview.tsx`, `ServiceReport.tsx`, `DocumentGeneration.tsx`, 3 tests. No `b1125` head; MPS b1093/b1116/b1117 landed as #145/#143/#144. Owed at source: MPS #145 (R141 live).

## 2. Lanes with no shared path (project order)
Intersection by program against those sets and the open PRs: NONE except where stated; planted controls fired (`package.json` hit #91, `SqlServerWakeRetry.cs` hit b1095). No HP-tool integration this phase: word scan `securitymanager|fleet|firmware|siem` over the HPSM lane paths printed 0 (control `api/x/FleetThreat.cs` 1); HPSMPOC-82, 85, 86, 168, 191, 220, 240 (titles hit) are LEFT OUT.

### HPSM-POC (main 5f128fb8)
**NH2. HPSMPOC-407 item 2** (low value; fill a free seat). Done-when: "each item is built or recorded as declined ... Which items are built is a scope call that is not made here"; "the file and the whole infra suite stay green". Items 1, 3 landed (#264); vp1 to vp6 are green though none yields a unique name. Path `infra/tests/test_security_baseline.py` (2927 lines). Predicate `ci.yml:627` `run: bash infra/scripts/validate.sh` which runs it at `validate.sh:21`. Tuesday's call: name which argument positions "reach the value"; unnamed, it is measure-only and "declined" is a ruling. GUESS 1 file, 30-80 lines. C2 Sonnet (`:92`), G2 (`:109`).
**NH3. HPSMPOC-436, measure only.** Done-when: "it is measured whether any route can ask for a finding explanation with no finding"; build is words, excluded. Reads `Narrative/Providers.cs:53` and `NarrativeOutputValidator.cs:152` (`paragraphs.Count >= 1`); no edit (b1095 holds the validator). No gate. C2 Sonnet.
Others: 429, 430, 433 to 435 share b1095 files; 417 residual, 431 are b1113's.

### MPS Calculator (main 0d4022b9)
**NM3. MPSCALC-361, then 359 (360 only on Tuesday's line); engine, serial, one commit each.** M76 landed (#144); no live seat holds an engine path. Not built: `perSite`, `usageOnly`, `FleetTotal` each 0 in `PurchaseInput.cs`, `PurchaseRecomputation.cs`, `PurchaseCalculator.cs` (control `FixedPerGroup` 1). The contract has no quantity rule (`openapi.json`: `quantityRule` 0, control `perDevice` 50), so M77's guard is untouched.
- 361: "The pinning row exists and is green at the unedited product; after the change fleet-total quotes reconcile at every quantity, including the two cases that disagreed; the rows of MPS #137 stay green." Paths `Reconciliation/PurchaseRecomputation.cs` (`:52`), `docs/ENGINE.md` (X-34 `:160`, X-35 `:161`), `tests/MpsCalc.Engine.Tests/ComponentQuantityRuleTests.cs`.
- 359: "perSite has a register row and a red-first test for a quantity per site; a group of several sites counts the component once per site; an unknown rule is still refused; the three rules of MPS #137 are unchanged." 257 landed (`PurchaseInput.cs:72` `Sites`). Adds `Input/PurchaseInput.cs` (enum `:40`, member `:110`), `Calculation/PurchaseCalculator.cs` (`:181`, refusal `:389`), ENGINE.md beside X-40 `:166`, X-44 `:170`.
- 360: done-when opens "The reading is confirmed in writing"; the ticket makes it the coordinator's, so a Tuesday line, not the owner's.
GUESS 361 about 3 files, 359 about 5, 100-250 lines. Tier 1: C3 Opus (`:93`), G1 (`:108`). Heavy.
**NM7. MPSCALC-369, five web rows time out under whole-suite load (tests only).** "The named rows pass in all of 20 whole-suite runs started at a load average above seven, the load printed; no assertion removed or weakened; no title changed; no product byte changes." Paths `web/src/screens/bom/PurchaseBomEditor.test.tsx` (229 lines), `PriceReason.test.tsx` (51). Cause unmeasured. CI: check run `web (npm ci, lint, test, production build)`. Heavy; low load only. GUESS 2 files, under 60 lines. C2 Sonnet, G2.
Not lanes: 363 (M77); 362's residue waits on 358.

### Security Composer (main 69b01339; no seat; `.tools/composer-heavy.lock` absent, control `.tools` exists)
**NC1. PCOMP-23, CHANGE-REPORT half only.** "with a long target name, the change report's footer drops its manifest <hash> line"; fix-shape "Footer line budget, plus a test at 250 + 200 characters." `packages/renderers/src/change-report.ts:532` builds the footer with no budget; `test/change-report.test.ts` (316 lines) holds `footer` 0, `manifest` 35. Paths those two (NONE). The policy-PDF half and `document-pdf.ts` (`:179`, `:249`) share `document-pdf.ts` with open draft #85, so NOT free under this rule. GUESS 2 files, 40-100 lines. C2 Sonnet, G1. Heavy.
**CCD. PCOMP-115 + 116 + 117, after NC1 (same lock).** 115: "a typecheck project includes packages/db/test and lists every file under it; the CI typecheck step exits 0 on main; a planted type error in a file there turns it red; no product byte; the PR gets a gate of its own." `packages/db/tsconfig.json:8` `"include": ["src"]`; `package.json:18` `typecheck`; `tsconfig.build.json:20`; new `packages/db/tsconfig.test.json` (tree 0); NOT root `package.json` (PR #91). 116: awk `DEPLOY.md:203` accepts a function-body plant; new row in `packages/db/test/b778-route-b-script-complete.db.test.ts`. 117: `DEPLOY.md:263` and `b778...test.ts:769` say "as a pg_restore before 16.10 writes it" (fix-shape "as an older pg_restore writes it"); if Tuesday reads it as an owner word, it moves to section 3. CI `scripts/ci.sh:117`, `:118`. GUESS 4 paths, 60-150 lines. C2 Sonnet; G1 for DEPLOY.md, G2 for tsconfig.
**PCOMP-119 (new, tests only).** Proposed done-when: "each mutant turns a new row red; each block has a row green at the head; the edit stays in that test file; no product or DEPLOY.md byte; a gate of its own." One file, `packages/db/test/b616-deploy-commands.db.test.ts` (2639 lines; ticket's `:677`, `:733`, `:772` `unclosed:`, `:735`, `:876`, `:881`, `:915`, `:2052` all read as stated). Rows plus the `:915` comment only; "a fix of the scan was not ordered", so no scanner change. Disjoint from CCD.GUESS 1 file, 80-200 lines. C2 Sonnet, G2. Heavy lock.

### NexusAI (main 68b080d1; no seat, no open PR; merge-commit landing)
**NX1. RD-915 + RD-920 + RD-922, one seat, three commits; counts file written serially.**
- RD-920: "a red-first cell asserts a positive id and a clean close and passes; or the product owner has chosen to leave it". `backend/simpleDb.js:175`, `:193` prepare, `:194` run, `:225` `(err) =>`, `:229` `resolve(this.lastID)`. New `__tests__/rd920-insert-printer-log.test.js` (tree 0).
- RD-922: "the script waits for each statement and a run against a scratch database leaves every table empty". `scripts/clear_db.js:14,:17,:20,:23,:26,:30` (`:30` VACUUM). Only on a scratch database it creates.
- RD-915: `backend/dataExport.js:217` `zlib: { level: 9 }`; one cell in `__tests__/rd913-archiver-sqlite3-characterisation.test.js` (464 lines), red by dropping the option; `scripts/verify-expected-counts.json:4` `"tests": 5287`. Bound must hold on node 26 and 24, else STOP on 24.
CI `build.yml:84` `npm run verify -- --maxWorkers=2`. GUESS 5 paths, 80-200 lines. C2 Sonnet; G2 if nothing outside `insertPrinterLog` changes, else G1.
**RD-911 (tests only; second seat).** "each bound is either left with its reason in a comment on this ticket or replaced by a count with a red-first plant and a review gate." `rd407-r2-missing-mid-swap.test.js:44` `BUDGET`, `:45`, `:138` `Date.now() - startedAt > forMs`; `rd407-concurrent-settings-writers.test.js:68` `STORM_DEADLINE_MS = 60000`. A new cell moves the counts file: after NX1. GUESS 2 files, 0-60 lines. C2 Sonnet, G2. RD-916 (after NX1) is also path-free.

## 3. Needs a word or a ruling (cards: filter `client_project` starts `Datasec/`, 626 of 1113, key searched in whole card text; control HPSMPOC-420 returns 1)
- MPSCALC-368 (wire names "OPEN", blocks 267), 272, 274 (figures only on the list row; tile words), 358, 364, 365 (does quantity 0 count; Tuesday can answer): no card cites them. 360: Tuesday's line, above.
- PCOMP-113 (three outcomes, "awaiting the product owner"), PCOMP-12 (new screen words): no card.
- HPSMPOC-436 build, 432 (role + name = words), 424, 425, 410, 412 item 2, 407 "declined": no card. HPSMPOC-420: card `hpsmpoc-answers-so-far-words-1102` OPEN (`show` read).
- RD-921, 923, 917 (a)(b), 918, 908: no card. RD-907 (owner decides leave or wrap): cited by ruled card `nexusai-risk-store-writers-rd868-1029` (c), which ruled one ticket per writer, not wrap-or-leave.

## 4. Not measured
- 7 HPSM #275 check runs; the PCOMP-23 defect at 250 + 200 characters ("not seen live"); node 24 for RD-915 and M77; whether 20 whole-suite MPS runs finish at load 11.
- Inherited 0430/0940 "not lanes" (HPSM 308, 315, 318, 319, 323, 349, 352, 356; MPS 302, 310, 324, 325, 331 to 342; Composer list) not re-judged; MPSCALC-334, 335, 341, 297 read: built or held. RD below 895 not scanned; RD-904 to -906, -917(c) not judged.
- Cards ruling a ticket without citing its key; PR-body mentions; hosted state.
READ-WHOLE-BY-TUESDAY: ____
