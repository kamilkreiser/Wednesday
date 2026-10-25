BLUF: All 10 "buildable now" tickets of the 22 Oct plan are gone: 137/172 (#95), 174/165 (#96), 160/150 (#97) merged, so wave 1 is done. Of the 5 left (161, 169, 170, 176 plus the 151 deploy), 161/169/170 and 288/204 are BLOCKED BY #102 because they edit `QuoteEndpoints.cs`, a #102 path. **Three file-disjoint lanes are ready now (overlap with #102 = 0 each): L1 proposal one-pager combined rate pair (228, ruled C-49 rule 1) + docs sweep; L2 readiness/reconciliation hardening (291, 292, 293, 294, 295); L3 importer and source-version test pins (318, 319, 320, 303, 200).** Jira status is useless as a filter: all 306 open MPSCALC rows read `Backlog` (14 are Done), so "covered" below comes from merged-PR/commit text plus the repo's own records. Opus-tier flags: 302, 288, 222/226/202, 261, 286.

# MPS next build lanes (read-only screener, 2026-10-24)

Updates `2026-10-22_mps-open-items-lane-plan.md`. Marks: MEASURED = read by me today; RELAYED = from a named record; UNMEASURED = said so.

## 0. Base and method

- Main: `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055` (MEASURED `gh api git/ref/heads/main`, equals the given sha). Open PRs: only #102 (MEASURED `pulls?state=open`, 1 row). #98, #99, #100, #101, #103 each `merged=true` (MEASURED per-PR GET).
- The local clone `2_Project_Files` is STALE (its `origin/main` is `e3624f00`, no `a5b4bbb5`; `git cat-file -t a5b4bbb5` failed). All file reads below are from a GET tarball of exactly `a5b4bbb5` (read-only, in the scratchpad), not the clone.
- #102 (`b518/mps-api-input-hardening`, head `275349907500...`) paths, 21 files (MEASURED `pulls/102/files --paginate`, line count 21): `src/MpsCalc.Api/Infrastructure/ApiJson.cs`, `Quotes/PurchaseValidation.cs`, `Quotes/QuoteEndpoints.cs`, `Sources/ActiveSources.cs`, `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs`, `src/MpsCalc.Import/Store/ReferenceStoreDocument.cs`, and 15 test files under `tests/MpsCalc.Api.Tests/` (`DealUsageNoCountedDevice`, `LineMarkupTests`, `QuoteInputHardening.*` x9, `StoreLoadRows*` x3) plus `tests/MpsCalc.Engine.Tests/PurchasePageEstimate.cs`. It covers MPSCALC-215/-216/-210/-217/-196/-230 (so those are out).
- Jira (GET only, `project = MPSCALC AND ...`, paginated by `nextPageToken`): `statusCategory != Done` COUNT 306, all status `Backlog`; `statusCategory = Done` COUNT 14 (positive control that the filter splits); key >= 136 and not Done COUNT 185.
- "Covered by a merged PR": keys found in the text of merged PR titles/bodies and main commit messages (`gh api pulls?state=closed` 100 merged rows read, 4,199 commit-message lines). 185 open >= 136, minus the keys that text names, minus the 6 #102 keys, left 87 (printed by the command). This is a floor of coverage, not proof: PR #87/#88/#90 name some tickets only by lane, so each candidate below was also checked against source or its own ticket text.

## 1. Update of the 22 Oct plan (what happened to its 16)

| Plan item | Now | Source |
|---|---|---|
| 137, 172 | MERGED PR #95 | commit `44297b59`, PR body |
| 174, 165 | MERGED PR #96 | `7836196c` |
| 160, 150 | MERGED PR #97 (the 7% default and deal usage screens) | `e027ebd0` |
| 151 | MERGED earlier (PR #86); only a deploy card remains | unchanged |
| 161 archive | NOT built; **blocked by #102** (needs `QuoteEndpoints.cs` routes, `QuoteStore`, `QuoteEvents`) | MEASURED grep: no Archive route in source |
| 169 source set on lineMarkups | NOT built; **blocked by #102** (`QuoteEndpoints.cs:1012-1079` builds `LineMarkups`, `LineMarkupsOverlayVersion`) | MEASURED |
| 170 fleet line identity | partly: #103 landed the web half (198, 199); server audit rows B159-5/-9 untouched; `PriceAudit.cs` + `QuoteEndpoints.cs` -> **blocked by #102** | UNMEASURED for the server half |
| 176 triage + My feedback | NOT built (no `triage` / `MyFeedback` symbol under `src` or `web/src`); words gate first; adds operations to `openapi.json`/`API.md`/generated client, which L1 owns this wave, so it follows L1 | MEASURED grep, 0 hits; positive control: the same grep style finds `FeedbackItem` in 12 files |
| 136, 144, 153, 163, 187 | unchanged BLOCKED (owner's Entra step, reviewer's file, K-04/MPSCALC-212, load rule, hosted-restart card) | plan |
| 198, 199, 208, 220, 301 | MERGED PR #103 (web) | PR body |
| 197, 211 | MERGED PR #99 | PR body |
| 189, 190, 191, 192, 193 | MERGED PR #100 | PR body |
| 229 | MERGED PR #101 | PR body |
| 230 | in #102 | C-49 delivered line |
| 312 (readyToExport 400 wording) | appears fixed by PR #98 (docs/openapi no longer say "refused 400" for `readyToExport`; grep for `readyToExport` lines with `400|refus|until` = 0 hits; positive control: `INVALID_FILTER` still found at `docs/API.md:596`) | MEASURED; treat as covered, ticket not closed in Jira |

## 2. Candidate table

Size: S under about 1 day, M 1-3 days, L more. "Overlap" = count of the ticket's files that are in #102's list (measured by anchored grep over the 21 paths; positive control: `QuoteEndpoints.cs` returns 1).

| Ticket | Summary | Status | Agent-actionable because | Files at main | Overlap | Size |
|---|---|---|---|---|---|---|
| MPSCALC-228 | One-pager repeats the same mono/colour pair per device class; six-rate cap hides rows | Backlog (label `needs-ruling`, now RULED) | Ruled C-49 rule 1 by the product owner 2026-10-23 ("one combined pair per deal", option a). Builder needs no human; the new "Device class" column wording goes to the owner at the words gate before any deploy. Not money design (layout of already-applied rates). Not a deploy. | `src/MpsCalc.Api/Quotes/Proposal.cs` (:525-526 area), `src/MpsCalc.Api/Contracts/Dtos.cs` (`ProposalUsageRate.deviceClass` is `required`), `web/src/proposal/model.ts`, `web/src/proposal/OnePager.tsx` (`ONE_PAGER_CAPS`), `docs/API.md`, `docs/api/openapi.json`, `web/src/api/generated/**`, `tests/MpsCalc.Api.Tests/QuoteApiTests.Showcase.cs` | 0 | M |
| MPSCALC-219 | Catalogue docs out of date (supplies and care rows, key sentences, X-31) | Backlog | Doc sentences only, regenerate contract with the sync script, send changed sentences to the words gate | `docs/API.md`, `docs/api/openapi.json`, `docs/ENGINE.md:147`, generated client; its `docs/IMPORTER.md:16` line goes to L3 | 0 | S |
| MPSCALC-195 | Contract and engine docs owed (negatives, fleet line numbers, rate-limit wording, headers) | Backlog | Doc-only; PR #98 may have done part (UNMEASURED which); seat re-measures each clause first | `docs/API.md`, `docs/ENGINE.md`, `docs/api/openapi.json`, generated header line | 0 | S |
| MPSCALC-291 | Purchase reconciliation checks supplies cost only per month | Backlog | Tier-1 verification code, recommendation names three fixes, none needs a person; fix shape is "compare at contract scale" | `src/MpsCalc.Engine/Reconciliation/PurchaseRecomputation.cs` (UNMEASURED path as ticketed: file list at main shows `QuoteReconciler.cs`, `ReconciliationTypes.cs`; seat locates the recompute code), `docs/RECONCILIATION.md`, `tests/MpsCalc.Engine.Tests/Reconciliation*.cs` | 0 | M |
| MPSCALC-292 | "Uses none of the calculators" guard can be bypassed | Backlog | Test-only; replace regex with reflection test | `tests/MpsCalc.Engine.Tests/ReconciliationTests.cs:457-476`, `docs/RECONCILIATION.md` | 0 | S |
| MPSCALC-294 | Reconciliation trusts recorded SellBasis; docs do not name it | Backlog | Docs + XML summary; optional cross-check is the seat's call and listed as a note | `docs/RECONCILIATION.md:14-16`, `src/MpsCalc.Engine/Reconciliation/QuoteReconciler.cs` | 0 | S |
| MPSCALC-293 | Readiness CSV export drops the Passed state | Backlog | Recommendation exports `Passed` in the existing Severity column; a new header would be a word, so the seat uses the existing one | `web/src/screens/quote/ReadinessPanel.tsx` (+ `ReadinessPanel.test.tsx`) | 0 | S |
| MPSCALC-295 | Non-empty readiness check says "at least one device line" for a quote with none | Backlog | Tuesday's 2026-10-20 ruling 6(b) accepts it for a later lane: sentence becomes "at least one line"; add a Review (not Blocking) check. The new sentence is a NEW WORD: word pack to the owner, not shipped until ruled. | `src/MpsCalc.Engine/Readiness/ReadinessEvaluator.cs:87-90`, `tests/MpsCalc.Engine.Tests/ReadinessTests.cs` | 0 | S |
| MPSCALC-318 | No row pins the empty-id branch of the source version id comparison | Backlog | Test-only; production line `SourceDocumentChecks.cs:132` is unchanged | new file under `tests/MpsCalc.Api.Tests/` beside `SourceLifecycleTests.B520EmptyId.cs` | 0 | S |
| MPSCALC-319 | Negative-price guard of the reference validator not pinned at its edge | Backlog | Test-only; synthetic data only (no real price rows) | `tests/MpsCalc.Import.Tests/ReferenceDocumentValidatorTests.cs` (or a new file beside it); production `ReferenceDocumentValidator.cs:211` untouched | 0 | S |
| MPSCALC-320 | Id-key property row reads its oracle from the code's own table | Backlog | Test-only; literal expectations | `tests/MpsCalc.Api.Tests/SourceLifecycleTests.B520IdCase.cs:107-171` | 0 | S |
| MPSCALC-303 | Colour-panel import: a plain-word cell ends the section silently | Backlog | Importer code change per recommendation (pass the map's option SKUs, or raise a Warning). Importer code, tier 1; synthetic fixtures only. | `src/MpsCalc.Import/Books/SynnexBook.cs:309,334-336`, `tests/MpsCalc.Import.Tests/PanelSectionEndTests.cs` | 0 | M |
| MPSCALC-200 | Importer coverage table: care-row counts contradict, two read gaps unexplained | Backlog | Doc re-measure, counts only | `docs/IMPORTER.md:112,117` | 0 | S |
| MPSCALC-313 | Stub mode cannot answer `readyToExport` or create a quote | Backlog | Web stub fix, no human | `web/src/api/stub/stubApi.ts:209`, `web/e2e/b28.spec.ts`, `web/e2e/b30.spec.ts` | 0 | S |
| MPSCALC-317 | Add section before the price list loads starts without the 7% default | Backlog (follow-up the owner asked to be filed) | Recommendation: disable Add section until inventory loads; a disabled state may need a hint word (check) | `web/src/screens/QuoteScreen.tsx:99-100`, `web/src/screens/bom/PurchaseBomEditor.tsx:141`, `web/src/screens/bom/bomModel.ts:51-53` | 0 | S |
| MPSCALC-218 | Price-audit tests lack re-order and description rows | Backlog | Test-only | `tests/MpsCalc.Api.Tests/TargetWhatIfAuditApiTests.cs`, `CareKeyPatternApiTests.cs` | 0 | S |
| MPSCALC-221 | Secret-scan false positive on a synthetic care key | Backlog | Reshape a test constant | `tests/MpsCalc.Api.Tests/CareKeyPatternApiTests.cs:15` | 0 | S |
| MPSCALC-205 | Packaging refuses a tree that already holds a Release build | Backlog | Script fix, not a deploy | `scripts/package.sh:45` | 0 | S |
| MPSCALC-201 | Entra app script follow-ups (group lookup before writes, flags) | Backlog | Edits the script only; running it against Entra is the owner's, never run by the seat | `scripts/entra_apps.py:172,174,356-358` | 0 | S |

Reserve (not in a lane, file-disjoint, can fill a fourth seat later): 313, 317, 218, 221, 205, 201. They are small and independent; L1/L2/L3 are the value order.

## 3. Excluded

### 3a. Needs the product owner's words or a ruling (card these)

- 316 quoteRef "100 characters" vs UTF-16 units: owner chooses state-the-unit docs wording or counting text elements (label `needs-ruling`).
- 300 quantity audit on a multi-device section: the rule is not ruled (wait for single-model groups, MPSCALC-252, or flag per device line).
- 314 autosave writes an event and a revision per typing pause: "the choice is open and not ruled" (BACKLOG B351-B348-2).
- 204 out-of-range order (WHO-before-WHAT): needs a ruling; also edits `QuoteEndpoints.cs` (#102 path).
- 261 rental credits: the authorisation rule is ruled (C-50 option a), but who counts as Approver and whether no-self-approval applies is "not settled", so words and a rule are still owed.
- 153 / 212 usage-rate hints: owner's K-04 (no agreed ink rate) and the governed-setting store (MPSCALC-212/V11, cards D-10 and D-14).
- 144 large-format items: the reviewer's spreadsheet and a hosted data step after MPSCALC-202/-203 are live.
- 187 hosted restart proof: needs a deploy card (approval-class).
- 163 overlay concurrency: Tuesday's ruling on "under load" (load rule forbids artificial load).
- 136 roles: the owner's Entra group assignment.
- 176 triage and "My feedback": builds only after the owner approves the words; follows L1 because it edits the same contract files.
- 315 per-year recurring GP and rental whole-term GP on the quote list: touches the calculation register (V4); a register row and owner ruling first.
- 314/317-type rows with new user-facing words: any sentence the seat adds is listed as a word pack to the owner before a deploy (K-02).
- T-V4 to T-V11 plan rows (252-260, 264, 265, 267-287, 243, 246, 237, 273-275): UNMEASURED individually. They carry lane labels `lane-v4`..`lane-v11`, `calc-register` (254, 256, 258, 259, 260), `later-phase` (260) and wait on v13.4.1 D-cards and words; not screened for file overlap because most edit the quote contract (`QuoteEndpoints.cs`, `Dtos.cs`) which is #102-locked or L1-locked this wave.
- Deferred or ruled-no-build: 149, 152, 154, 159, 181, 188 (as in the 22 Oct plan).

### 3b. Covered by a merged PR (not built again)

137, 172 (#95); 174, 165 (#96); 160, 150 (#97); 151, 262, 263, 266 (#86); 198, 199, 208, 220, 301 (#103); 197, 211, 104 (#99); 189, 190, 191, 192, 193 (#100); 229 (#101); 214 (#82); 213 (#80); 203 (#81, retention half; deploy-script follow-ups remain in MPSCALC-202/-203); 231 (#83); 289 (#93); 304, 305 (#92); 306-311 (#91); 244, 28, 245 (#89); 238-242, 249, 296-299, 27, 34 (#88/#90); 232-236, 209 (#85, partly through #98 words); 312 (#98 wording, MEASURED above). In #102 (open): 215, 216, 210, 217, 196, 230.

### 3c. Blocked by #102's paths (QuoteEndpoints.cs), buildable after #102 merges or is closed

161 archive, 169 source set, 170 server half, 288 callerCan reject vs approve, 204. When #102 lands they form the next Q-chain lane in the 22 Oct plan's order (161, 169, then 170, then 176).

### 3d. Opus-tier (security-design, approval design, or data-destroying risk)

- 302 parity proof AGREE on a count-preserving tamper: integrity-check design (`ParityProof.cs`); needs an Opus gate; kept out of L3.
- 288 callerCan.approve vs reject: approval-design surface (C3 in the 22 Oct plan).
- 222 / 226 / 202 rollback past care-pack and staging classes, and deploy PRE-1 counting: could hide or drop stored quote rows on rollback; `needs-ruling`; deploy-script and store-reader design.
- 261 credit authorisation, 286 approval thresholds, 274 authorisation reference: approval and money-control design.
- 181 quote and snapshot stores on a database: deferred, Azure and money.

## 4. Proposed lanes (at most 3, file-disjoint, ordered by value)

Overlap check run on the lane paths against the 21 #102 files: L1 0, L2 0, L3 0 (positive control: `QuoteEndpoints.cs` gives 1). Lane vs lane: L1 owns the contract (`Dtos.cs`, `docs/API.md`, `docs/ENGINE.md`, `docs/api/openapi.json`, `web/src/api/**`, `web/src/proposal/**`, `Proposal.cs`); L2 owns `src/MpsCalc.Engine/Reconciliation/**`, `Readiness/**`, `docs/RECONCILIATION.md`, `web/src/screens/quote/ReadinessPanel*`; L3 owns `src/MpsCalc.Import/**` (Parity, Books, Validation), `tests/MpsCalc.Import.Tests/**`, `SourceLifecycleTests.B520*`, `docs/IMPORTER.md`. No path appears in two lanes.

### L1 (highest value): combined usage-rate pair on the proposal, plus docs sweep

- Tickets: 228 (first), then 219, 195 (docs; 219's `docs/IMPORTER.md:16` line is handed to L3).
- Paths: `src/MpsCalc.Api/Quotes/Proposal.cs`, `src/MpsCalc.Api/Contracts/Dtos.cs`, `web/src/proposal/**`, `docs/API.md`, `docs/ENGINE.md`, `docs/api/openapi.json`, `web/src/api/generated/**`, `web/src/api/types.ts`, `tests/MpsCalc.Api.Tests/QuoteApiTests.Showcase.cs` (+ new test files).
- Done-when: a deal-usage quote prints one combined mono/colour pair per deal on the one-pager and full proposal with no per-class repeat and no "and N more rates" hiding; contract, docs and generated client agree; the new column wording is listed as a word pack for the owner; tier-1 gate GO.
- Size M. Model: Sonnet C2 (the rule is ruled). Not touching `QuoteEndpoints.cs`.

### L2: readiness and reconciliation hardening

- Tickets: 291 (first), 294, 292, 293, 295.
- Paths: `src/MpsCalc.Engine/Reconciliation/**`, `src/MpsCalc.Engine/Readiness/**`, `docs/RECONCILIATION.md`, `tests/MpsCalc.Engine.Tests/Reconciliation*.cs`, `tests/MpsCalc.Engine.Tests/ReadinessTests.cs`, `web/src/screens/quote/ReadinessPanel.tsx` and its test.
- Done-when: a contract-level supplies cost error above one cent is refused by the reconciler; the calculator-free guard cannot be bypassed by alias or using-static; the CSV export shows Passed; sell basis is named as a read-back fact; readiness sentence for no-device quotes is the ruled one (words pending owner); each red-first, tier-1 gate GO.
- Size M. Model: Sonnet C2 with a tier-1 gate (291 touches the verification of calculated figures, no calculation rule changes; if the seat finds a calculation-register row is needed it stops with one question).

### L3: importer and source-version test pins

- Tickets: 318, 319, 320 (test-only, first), 303 (importer), 200 and 219's importer line (docs).
- Paths: `src/MpsCalc.Import/Books/SynnexBook.cs`, `tests/MpsCalc.Import.Tests/**`, `tests/MpsCalc.Api.Tests/SourceLifecycleTests.B520*.cs` (new files beside them), `docs/IMPORTER.md`. Production source-version files are not edited.
- Done-when: each of 318/319/320 has a committed row that goes red on its named mutant and green on main; a plain-word cell in a colour-panel block no longer ends the section silently (Warning or member, per the ticket); the IMPORTER coverage table is re-measured with counts only; no price or BID value appears in tests, docs or comments; gate GO.
- Size S-M. Model: Sonnet C2. Synthetic fixtures only (pricebook data is confidential).

Why not Q-chain lanes now: 161, 169, 170, 288, 204 all edit `QuoteEndpoints.cs` and would collide with #102 until the product owner rules on it.

## 5. Open questions for Tuesday

1. Does Tuesday want 228 built before the owner has read the new "Device class" column words (the build can proceed, the words ship after the owner rules)?
2. Fate of #102 decides when the Q-chain (161, 169, 170, 288, 176) can start; until then L1/L2/L3 are the only disjoint work.
3. Close the stale Jira rows for the 31 merged tickets? Jira shows all `Backlog` and no project rule moves a ticket on merge (`JIRA.md:174,185,208`); not mine to change.
