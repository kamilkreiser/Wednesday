# SCREEN 1745 2026-11-02: the 23 "needs a word or a ruling" tickets of SWEEP-1645 section 3, read whole at source (read-only, drafter C8)

Written 2026-11-02 17:56:06 AEDT by program output below (clock printed by `date` in the generating run). Main shas read by `gh api -X GET` (each project's own `GH_CONFIG_DIR`): MPS `0d4022b9`, HPSM-POC `5f128fb8`, Composer `69b01339`, NexusAI `68b080d1`. No card, no Jira write, no message was made; `decision_queue.sh show` was the only queue verb used.

## BLUF

**Counts printed by the generating program over its own 23 rows: A (truly the owner's) = 3, B (not his) = 16, C (already ruled or stale) = 4; total 23.** Most are B, as the sweep's own test predicts. By who acts: coordinator decides 14, agent lane with no word needed 2, owner 3, already ruled 4.

Per project (A/B/C): HPSM 2/3/3; MPS 1/6/0; PCOMP 0/2/0; RD 0/5/1.

- **Three questions are the owner's** (ready-to-paste below): MPSCALC-364 (two published developer-doc sentences, and one code comment, that are partly false), HPSMPOC-424 (stored remediation entries: what happens when one fails the current rules), HPSMPOC-425 (does "Evidence submitted" refuse an invisible-only reference). Each has a default that keeps work moving.
- **Four are already ruled or stale**, and the sweep's section 3 was out of date on one: HPSMPOC-420 was ruled b at 16:51:53 and its tile card b at 17:09:27 (both after the sweep's last read); HPSMPOC-412 (ruled 06:09; item 1 already built at main); HPSMPOC-410 (ruled 2026-10-29, one gap named); RD-918 (the sqlite3 ruling of 2026-11-02 covers part a; part b is RD-923).
- **The three the coordinator asked about** are all his: RD-907 (facts: 10 literals, 0 alerts on the line; recommend leave), MPSCALC-365 (recommend: a quantity-0 device line does not count), MPSCALC-360 (the reading to confirm, with the engine rows it touches). See their blocks.
- **One finding about the records, not the sweep:** CLARIFICATIONS.md says the wire spelling of the quantity rule (MPSCALC-358) needs the owner's word. I read it as a contract identifier the coordinator can fix by the convention in `ApiJson.cs`; the block gives the one-sentence fallback card if Tuesday would rather ask.
- **A reading I could not confirm from allowed files:** whether the owner has delegated "leave it" outcomes on low-likelihood tickets to the coordinator. Five RD tickets (907, 908, 917, 921, 923) say "or the product owner has chosen to leave it". I applied the MPS precedent of coordinator rulings recorded as Tuesday's. If that is wrong, those five move from B to A and the question is the same one each time.

## Instruments and controls

- Tickets read whole: Jira REST v3 `GET issue` (description) and `GET issue/comment` (paged), project `.env` read in-process, no token printed. 23 of 23 fetched; statuses Backlog 17, To Do 6; comment counts total vs fetched equal for all (yes). Control: `MPSCALC-99999` answered HTTP 404 in the same run; a ticket with comments (HPSMPOC-407, 3) returned 3.
- Every Done-when quoted below is checked by the program to be a verbatim substring of the fetched ticket text (whitespace-normalised); a planted wrong quote exits the program (selftest: a planted wrong quote was refused).
- Section 3 coverage: every one of my keys is matched in the sweep's section 3 by project prefix plus bare number on one bullet line: 23 of 23 (control `MPSCALC-999`: False). Prefixed keys in section 3 that are not in my rows: none (the sweep also names 360 and 436/407 sub-items; bare numbers such as 267 in "blocks 267" are not tickets I was asked to read).
- Card store: `0_Brain/dashboard/data/decisions.json` read with Python through an inclusion filter `client_project` starts with `Datasec/`: 627 of 1114 cards (the sweep read 626 of 1113; one card was added since). Each key searched word-bounded in the whole card text; each subject searched with a regex per ticket (title words, not the key). Control: `HPSMPOC-420` returns 2 cards (`hpsmpoc-answers-so-far-words-1102`, `hpsmpoc-snapshot-recap-tile-words-1102`; the sweep saw 1, the second was filed after it); nonsense string returns 0. Cards read whole only with `decision_queue.sh show <exact id>` (24 ids). No `list` verb was used.
- Key hits in the card store: only HPSMPOC-420 (2) and RD-907 (`nexusai-risk-store-writers-rd868-1029`, ruled c); every other key returns 0. Subject searches returned cards for MPSCALC-358/365 (the 253 quantity-readings card and the API-error-words card, judged not the same question), HPSMPOC-410/412/432/420, RD-918, plus PCOMP-113 and RD-923 neighbours that I read and rejected as other subjects. Loose regexes (PCOMP-12 "device-group", 86 hits) were replaced by a tight one (`typed sub-answer|Expert Discovery|draftKey`: 2 cards, neither about it).
- `file:line` pointers: printed by the generating program with a regex over a raw copy of each file fetched at the main sha above (`gh api -X GET repos/.../contents/<path> -H "Accept: application/vnd.github.raw"`); a pointer that does not match aborts the run. Pointers into `1_Project_Definition/CLARIFICATIONS.md` are into the MPS project's local working-tree copy (mtime 2 Nov 16:58, read-only, not origin: the records root is not in the code repository).
- Class counts: Python `Counter` over the rows below. Control: a planted row with class `z` is refused; a planted extra `a` row raises the A count by 1.
- NexusAI CodeQL: 123 open alerts read with `--paginate`, all at one commit; positive control: 49 `js/log-injection` rows in `backend/server.js`.
- Bicep census (HPSMPOC-407): 2 uses of `uniqueString` in all 10 tracked `.bicep` files, in 2 files; 2 of the pinned shape.

## Rows (one per ticket)

| Ticket | Class | Who acts | In one line |
|---|---|---|---|
| MPSCALC-368 | B  not his | COORD | Wire names and the restricted-caller rule for the purchase projection are a contract choice, not a word; the coordinator names them, then a builder lane runs. |
| MPSCALC-272 | B  not his | LANE | The ticket itself says "Start: now, no ruling needed (plan section 4)"; tile labels ride the word pack. One dependency: the recurring-GP tile has no server figure yet. |
| MPSCALC-274 | B  not his | COORD | Same as 272 on words (pack), but the Api has no field: the coordinator fixes two small shape points (length cap, optional) and it joins the contract-sync serial queue. |
| MPSCALC-358 | B  not his | COORD | The wire spelling is a contract identifier with a precedent in the Api itself; the coordinator picks it by that convention. Error words and editor labels ride the pack. The records call it the owner's; I disagree, and give the fallback. |
| MPSCALC-364 | A  owner's | OWNER | Two published developer-doc sentences are partly false; the project's own practice is that the owner approves each such sentence by a card. Question below; the sentence is code-read, not request-run. |
| MPSCALC-365 | B  not his | COORD | "The product owner or the coordinator states" - the coordinator can. Facts and a recommended answer (a zero line does not count) below. |
| MPSCALC-360 | B  not his | COORD | The ticket makes the reading the coordinator's ("confirmed in writing"). Facts for the reading below; D-06 a already fixes the frame; number-affecting, so a card follows the build, as for MPSCALC-253. |
| PCOMP-113 | B  not his | COORD | Three options, all on one operator-runbook paragraph (DEPLOY.md), none customer-facing; the coordinator picks. Recommend the shortest true one. |
| PCOMP-12 | B  not his | COORD | Latent, code-read only, no done-when, no trigger today; the coordinator leaves it in Backlog. Not a question for the owner. |
| HPSMPOC-436 | B  not his | LANE | Step one is a read-only measurement an agent does; the build choice after it ("refuse / sentence / declined") is the coordinator's scope call and only a sentence would be a word. |
| HPSMPOC-432 | B  not his | COORD | Same fix class as HPSMPOC-409, which the owner ruled "keep the named area" on 2026-11-02; the coordinator extends it and tells him, and sequences after 409's branch lands. |
| HPSMPOC-424 | A  owner's | OWNER | A product behaviour with data loss and a possible new message; the ticket asks the owner (a to d). Recommendation: drop only the failing entry. |
| HPSMPOC-425 | A  owner's | OWNER | Whether "Evidence submitted" should refuse an invisible-only reference is a product rule on a customer screen; the ticket asks the owner. |
| HPSMPOC-410 | C  ruled or stale | RULED | The owner ruled "keep the sample names" for Demo on 2026-10-29 (alias rule covers the customer frame only); the sample label is in the name. Coordinator records it. |
| HPSMPOC-412 | C  ruled or stale | RULED | Ruled 2026-11-02 06:09 (keep "Delivery phases" and match the Home tile and the Home sentence); item 1 is already built at main, item 2 is a one-line follow-up for a lane. |
| HPSMPOC-407 | B  not his | COORD | Items 1 and 3 landed; items 2 and 4 are a scope call the ticket leaves open. Recommend the coordinator records both as declined with the reason below. |
| HPSMPOC-420 | C  ruled or stale | RULED | The sweep read the card as OPEN; it was ruled b at 16:51:53, one minute after the sweep's last read, and the tile card at 17:09:27. What remains is a build. |
| RD-921 | B  not his | COORD | A dormant code path (no caller passes an offset); three behaviours offered; the coordinator picks the smallest. Low likelihood, own gate. |
| RD-923 | B  not his | COORD | Retire or repair a legacy compose path that no customer image uses; the coordinator picks (recommend retire under RD-494), noting the one test that pins a file. |
| RD-917 | B  not his | COORD | Three behaviours of an export function; the coordinator decides what (a) and (b) should do (correctness, not words). Share a file with RD-915, so serial. |
| RD-918 | C  ruled or stale | RULED | Part (a) is the "npm blocks install scripts" trigger the owner's 2026-11-02 sqlite3 ruling records; part (b) is RD-923's decision. |
| RD-908 | B  not his | COORD | A missing assertion in a test (product behaves correctly); the gate itself said to ride with the next change to that file. Coordinator: ride along, do not commission alone. |
| RD-907 | B  not his | COORD | Facts below let the coordinator answer: the logged value can only be one of 10 literals and no CodeQL alert sits there. Recommend leave and record Declined, with the strict-reading fallback. |

## Blocks (B and C, then A), each with the Done-when quoted from Jira

### MPSCALC-368  (B  not his; Backlog; [B1057-OPEN-1] Purchase recurring projection on the Api: the DTO member, mapping, contract text and generated )

Done-when / acceptance (verbatim): "A caller of the purchase result reads the six measures, monthly, annual and contract, as the engine formed them"; "a caller without internal-metrics reads no member the contract marks internal"

- The ticket calls the member names OPEN and says which of the six a restricted caller may read "is not ruled". Neither is a user-facing word: the Api JSON is camelCase (`src/MpsCalc.Api/Infrastructure/ApiJson.cs:9`) and the six measures already have engine names (`src/MpsCalc.Engine/Results/CalculationResult.cs:244`: Pages, ClickCost, ManagedServiceCost, ClickRevenue, ServiceRevenue, RecurringGrossProfit, each `src/MpsCalc.Engine/Results/CalculationResult.cs:238` Monthly/Annual/Contract). The purchase side holds it at `src/MpsCalc.Engine/Results/PurchaseResult.cs:287`; the register row is X-39 (`docs/ENGINE.md:165`).
- The Api DTO has no member: `projection` occurs 0 times in Dtos.cs (control: PurchaseResult.cs 2); the DTO is `src/MpsCalc.Api/Contracts/Dtos.cs:891`.
- **Coordinator decides (two lines):** (1) wire names = the engine member names in camelCase (`projection.pages|clickCost|managedServiceCost|clickRevenue|serviceRevenue|recurringGrossProfit`, each `{monthly, annual, contract}`), left out when the engine leaves it out. (2) A caller without internal-metrics: recommend the whole `projection` member is absent (fail closed). Reason: three of the six are cost or GP (clickCost, managedServiceCost, recurringGrossProfit) and the DTO already marks such figures "Staff-only (internal-metrics)" (`src/MpsCalc.Api/Contracts/Dtos.cs:462`); revenue and pages would be derivable partners of those. Widen later only on a card. Rental R-30 stays out (the ticket leaves it undecided).
- Words: the openapi/API.md descriptions of the new member are developer text and ride the existing word-pack rows (BACKLOG [B1111-WORDS-1] / [B1137-WORDS-1], read in the records BACKLOG.md); no card now.
- Sequencing: same files and the same contract sync as MPSCALC-358 and -274 (Dtos.cs, openapi.json, `web/scripts/sync-contract.mjs`): one seat, serial, one commit each. MPSCALC-267 (the web table) and the annual-recurring tile of MPSCALC-272 wait on this.

### MPSCALC-272  (B  not his; Backlog; [T-V7-1] Review summary tiles (staff-only))

Done-when / acceptance (verbatim): "The tiles show the server's figures for the quote under review; a caller without internal-metrics sees none and the response carries none; component test."

- Ruled path: the plan lane was accepted whole by the owner (`1_Project_Definition/CLARIFICATIONS.md:654`: "Lanes start in waves as soon as you tap. Every new customer-facing word still comes to you as a word pack before it ships"). The ticket text: "Start: now, no ruling needed (plan section 4)". So the labels are pack rows, not a card.
- Dependency measured at main 0d4022b9: `annualRecurringGp` is never filled (`src/MpsCalc.Api/Quotes/QuoteFigures.cs:73` reads the Staff function at `src/MpsCalc.Api/Quotes/QuoteFigures.cs:125`, whose purchase branch passes `null` second). The "annual recurring GP" tile has no server figure until MPSCALC-315 or -368 lands; the other four tiles name figures whose availability I did not check (UNMEASURED).
- Paths: `web/src/screens/Lifecycle.tsx` (in the tree at main) and new `web/src/screens/review/**` (no such folder in the tree: 0 files). No open PR touches them (open PRs #121/#120 touch `web/package-lock.json`, per the sweep).
- Coordinator: nothing to answer. Launch after MPSCALC-368, or build four tiles and show "not recorded" on the fifth (that wording is a pack row).

### MPSCALC-274  (B  not his; Backlog; [T-V7-3] "Authorisation reference" field on approve; the approver stays the signed-in identity)

Done-when / acceptance (verbatim): "The reference is stored and shown in the quote events; the approver recorded is the signed-in identity whatever is typed; component test."

- The Api approve request carries one member, `Comment` (`src/MpsCalc.Api/Contracts/Dtos.cs:127` then `src/MpsCalc.Api/Contracts/Dtos.cs:129`); `authorisation reference` occurs 0 times in Dtos.cs and 0 in openapi.json (control: the word Authorization is in API.md 1 time, the bearer header, unrelated). So this is a contract change plus a stored field, not a UI-only ticket: it shares Dtos.cs/openapi.json with MPSCALC-358 and -368.
- Owner ruling: the plan accepted whole (C-45 option a; `1_Project_Definition/CLARIFICATIONS.md:679` keeps the approval checklist). The label "Authorisation reference" is the v13.4.1 pack's own wording: a pack row.
- **Coordinator decides:** optional, maximum length (recommend the same cap as `Comment`; read it from the validator before the brief), and that the approver stays the signed-in identity (the ticket already says so).

### MPSCALC-358  (B  not his; Backlog; [B1075-8] Quantity rule on the purchase line contract: the Api, DTO, contract text and web half, with the spel)

Done-when / acceptance (verbatim): "A request can state each of the three rules; an unknown rule gets a 400 naming the field; any spelling other than the chosen one is refused"

- Mechanism measured: the Api reads an enum from exactly one name, the member name or a `JsonStringEnumMemberName` attribute (`src/MpsCalc.Api/Infrastructure/ApiJson.cs:55`). `ComponentQuantityRule` has no attribute (`src/MpsCalc.Engine/Input/PurchaseInput.cs:40`), so today the only accepted spelling would be `PerDevice`, `FixedPerGroup`, `Manual`; the engine registers use the same words (X-40 `docs/ENGINE.md:166`).
- Convention in the contract: engine-owned enums are on the wire as member names (e.g. `docs/api/openapi.json:1531`, `docs/api/openapi.json:957`); Api-owned enums use attribute names in lower camel (e.g. `src/MpsCalc.Api/Contracts/Dtos.cs:662`). Single-line enum arrays in openapi.json: 60 begin lower case, 29 begin upper case (grep -c, control: both counts nonzero and the file has 2442 lines).
- **Coordinator decides:** recommend the exact member names (`PerDevice`, `FixedPerGroup`, `Manual`): it is the gate's own shape (the ticket quotes it), it is what the engine, register and tests already say, and it needs no attribute. Any other spelling is refused (the Done-when). Unmeasured: how many callers exist (none: "no caller can state a rule yet", per MPSCALC-253 comment).
- The records say otherwise: `1_Project_Definition/CLARIFICATIONS.md:2128` ("needs the product owner's word on the spelling and the words"). My reading: a spelling is a developer-facing identifier; the words (error text `INVALID QUANTITY RULE`, the editor labels) are his and are already pack rows (BACKLOG [B1111-WORDS-1]). If Tuesday prefers his tap on the spelling, the question is one sentence: "In the quote API, should a component quantity rule be written PerDevice / FixedPerGroup / Manual (as the engine names them)? Default: yes." Cost of asking: none blocks; cost of a wrong guess: a contract rename before any caller exists.
- Sequencing: same files as MPSCALC-368/-274; one seat, serial.

### MPSCALC-365  (B  not his; Backlog; [B1078-4] Quantity audit: whether a device line of quantity 0 counts as a counted device line (the web counts )

Done-when / acceptance (verbatim): "The answer is recorded; one committed row with a device line of quantity 0 expects it and fails when the rule is flipped the other way."

- Web: the audit builds the counted set from device lines that are neither credit nor optional (`web/src/screens/bom/quantityAuditModel.ts:100`) and flags nothing when two or more are counted (`web/src/screens/bom/quantityAuditModel.ts:104`); the device total is the sum of quantities (`web/src/screens/bom/quantityAuditModel.ts:101`).
- Engine: devices are summed quantities over Device, non-credit lines (`src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs:732`; deal devices `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs:920`). A zero line adds zero devices. (The ticket's `PurchaseCalculator.cs:692` is stale: main moved by MPS #145; use these.)
- Effect: a section of device 12, device 0, care pack 24 is read as "several device lines" and loses every flag, although the engine sees 12 devices and the care pack is 2 per device. Before MPS #138 the zero line was flagged "0 per device" (gate B1078, as the ticket reports). Owner rulings that touch zero: C-80 (`1_Project_Definition/CLARIFICATIONS.md:2122`) keeps "a group of zero devices still bills fixed and manual lines as typed" - a billing rule, not an audit rule; it says a typed quantity counts as typed, which for 0 is 0.
- **Coordinator answers:** a device line of quantity 0 does NOT count as a counted device line (it has no devices). Filter at the counted set gains `quantity > 0`; the zero line itself stays listed and flagged as 0 per device. One committed row: device 12, device 0, care pack 24, expecting the care pack flagged at 2 per device; the row must fail when the filter is removed. Precedent for the coordinator answering: MPSCALC-300 comment 40648 ("MET ON THE COORDINATOR'S WORD of 2026-11-02"). If Tuesday wants it on the record as a ruling, the CLARIFICATIONS "Tuesday's rulings" section is the place.
- Lane after the answer: `web/src/screens/bom/quantityAuditModel.ts` + `web/src/screens/bom/QuantityAudit.severalDevices.test.tsx`, about 2 files, under 40 lines; low-load launch only (the whole-suite web tests are heavy).

### MPSCALC-360  (B  not his; Backlog; [B1075-F3] usageOnly: usage-only component lines carry volume only into the one deal calculation)

Done-when / acceptance (verbatim): "The reading is confirmed in writing;"

- Frame ruled by the owner: D-06 a, "keep one deal-level calculation (K-09) fed by group volumes, keep book-derived costs, no unassigned pool" (`1_Project_Definition/CLARIFICATIONS.md:674`); its "Lets" cell names "T-V4-2's usageOnly rule feed one deal-level calculation".
- What the engine counts today (main 0d4022b9): X-25 deal pages = sum of quantity x estimate over non-optional, non-credit device lines, devices = sum of quantity (`docs/ENGINE.md:152`); X-27 the replacement shortfall per line per device (`docs/ENGINE.md:154`); X-28 deal supplies profit (`docs/ENGINE.md:155`); X-41 FixedPerGroup (`docs/ENGINE.md:167`). `usageOnly` is not a member: `0` hits in PurchaseInput.cs (members at `src/MpsCalc.Engine/Input/PurchaseInput.cs:43`).
- **Coordinator confirms (the reading to write on the ticket):** a usage-only line contributes (i) its pages to X-25 and its shortfall to X-27 inside the single deal calculation; (ii) NO hardware cost, margin or sell (X-05..X-07), NO device to the device count, tier pool (R-03), fee N (X-38) or section device quantity. That is "carries volume only". Unresolved inside it: whether its quantity is "devices" in X-25's device total; recommend no, since D-06 a says volume only and the device total feeds the tier pool.
- Order and gate: after 361 and 359 (same files, sweep NM3); tier 1, Opus. Because it is number-affecting and the owner took the two readings of MPS #137 by card after the build (`mps-253-two-quantity-readings-1102` ruled a; `1_Project_Definition/CLARIFICATIONS.md:2122`), the same flow applies: confirm, build, then one card with example amounts.

### PCOMP-113  (B  not his; Backlog; DEPLOY.md 0021 pin paragraph: name the four remaining row 8 pins or say it names only the words (Low, Note, wo)

Done-when / acceptance (verbatim): "which of the three is wanted is not decided; the 15 rows stay green; no product byte changes."

- Still open at main 69b01339: the pin paragraph names the words it pins in the Proven-on sub-section (`DEPLOY.md:248`) and ends "Nothing else in the command is pinned" (`DEPLOY.md:255`); the paragraph spans lines 218-255 (from the first line of the block to the line holding "Nothing else in the command is pinned"), and within it the four refused shapes are not named: occurrences of `Every command above` 0, `was run on a local stack` 0, `second table row` 0, `second paragraph` 0, `renamed` 0 (control: `Route B as written here` 1, which it does name). `both steps exit 0` appears 1 time(s) as part of a pinned cell, not as the second-row refusal.
- **Coordinator decides** between: (1) name the four; (2) one sentence saying the paragraph names only the `Route B as written here` and completeness-check words and that other refusals of row 8 are not named; (3) accept unnamed. Recommend (2): true, shortest, one sentence, no test byte. No customer or owner sees DEPLOY.md; the owner's relevant ruling is the round-cap pattern (`composer-99-routeb-pins-round-cap-1027` ruled a: land and ticket the gap), which treats such gaps as Notes.
- Sequencing: PCOMP-117 edits the same file (`DEPLOY.md:263`) and 113 edits the paragraph above it: one seat, one file, serial (sweep CCD). PCOMP-119 is test-only and disjoint.

### PCOMP-12  (B  not his; Backlog; The Expert Discovery screen's typed editor writes every declared sub-answer at the engagement level (draftKey()

Done-when / acceptance (verbatim): the ticket has no Done-when (its text ends at the BLUF sentence; verified: the string "Done" does not occur: False)

- Still true at main 69b01339: the typed editor reads and writes at engagement level (`apps/web/src/screens/Discovery.tsx:271` then `apps/web/src/screens/Discovery.tsx:272`). The API refuses a group-level typed write with 400 (ticket, B30).
- Trigger that would make it live: a content release that declares a device-group typed sub-answer. The ticket says both releases declare 0. My scan of `content/release-draft/bundle.json` and `content/release-demo/bundle.json` for a key named like `device_group` found 0, but I have no positive control for what a declared per-group sub-answer looks like, so this is UNMEASURED, not confirmation.
- Coordinator: record "wakes when a content release declares one" on the ticket and leave it. A new per-group editor would carry screen words (a pack row) and is not asked for by any current content.

### HPSMPOC-436  (B  not his; Backlog; [B1071-8] Offline template: a finding explanation of zero findings is written with zero paragraphs and refused)

Done-when / acceptance (verbatim): "it is measured whether any route can ask for a finding explanation with no finding; then either that request is refused with a plain reason, or the template writes a sentence, or the item is recorded as declined."

- Mechanism at main 5f128fb8: the template writes one paragraph per finding (`api/src/HpsmPoc.Modules.Reporting/Narrative/Providers.cs:53`); the validator needs at least one (`api/src/HpsmPoc.Modules.Reporting/Narrative/NarrativeOutputValidator.cs:152`).
- Reach, from the code I read: the projector takes every visible finding by default and, when `findingIds` is non-null, only those named (`api/src/HpsmPoc.Modules.Reporting/Narrative/NarrativeInputProjector.cs:21`); it throws for an unknown id and for more than 50, and has no check for zero (`api/src/HpsmPoc.Modules.Reporting/Narrative/NarrativeInputProjector.cs:30`). So zero reaches the template when an assessment has no visible findings, or when a caller passes an empty list. Whether any route does either is the measurement (callers of `NarrativeInputProjector.Project` were not read).
- Lane: read callers, run one local test with a zero-finding assessment; 0 product bytes. Then the coordinator picks the outcome; recommend "refused with a plain reason" only if a route reaches it, else "declined, unreachable".

### HPSMPOC-432  (B  not his; Backlog; [B1072-N5] Finding page at 360 px: axe reports one serious scrollable-region-focusable on an overflow-x-auto b)

Done-when / acceptance (verbatim): "the finding is built or recorded as declined."

- Wrapper at main 5f128fb8: `web/src/components/customer/FindingDetail.tsx:171`; `TableScroll` does not exist at main (count in FindingDetail.tsx: 0; control: `data-scroll-x` 1), because 409's branch has not landed.
- Ruling: card `hpsmpoc-409-region-read-aloud-1102`, ruled a at 2026-11-02 06:09:08 (keep the named scroll area; one separate commit so a veto is a small revert); its default tells the owner on the board at the merge. It was asked about the one-customer table; 432 is a second wrapper with the same axe rule.
- **Coordinator decides:** apply the same fix to the finding page wrapper as a separate commit after 409's landing, name text as a pack row, tell the owner at the merge. The only new fact he lacks is that the evidence table's caption would be read twice on this page too (not measured here; the 409 measurement was on another table).

### HPSMPOC-407  (B  not his; Backlog; [B961-1, B943-2, B943-3, B943-5] Infra binding rule after PR #251: a falsy non-bool condition, argument-positi)

Done-when / acceptance (verbatim): "each item is built or recorded as declined, and the file and the whole infra suite stay green."

- Item 2 (argument-position leniency) concerns evasions, not use: the six cells vp1..vp6 are constructed shapes. In the real templates, `uniqueString` occurs 2 times and both are the exact shape `take(uniqueString(resourceGroup().id, environmentName), 6)` (`infra/main.bicep:56`; `infra/showcase-ai.bicep:43`; instrument: `uniqueString` counted in all 10 tracked `.bicep` files = 2, located in 2 files; control: pinned-shape count 2 equals the total).
- Cost of building item 2: the sweep (NH2) estimates 30-80 lines in a 2927-line test; first the coordinator must define which argument positions "reach the value" for take/concat/coalesce/first/last/if, which no ticket does. Cost of declining: a Bicep author could add a template line that passes the rule but yields no unique name; the next real use would be one of the two shapes above.
- **Coordinator decides:** record items 2 and 4 as "declined: no real template uses these shapes (2 of 2 uses are the pinned form); reopen if a third use differs", with the instrument. That satisfies the Done-when ("recorded as declined"). It is a coordinator ruling recorded as Tuesday's (as in the MPS "Tuesday's rulings (coordinator, not Kam's)" sections), not the owner's.

### RD-921  (B  not his; To Do; backend/simpleDb.js getAllPrinterLogs given an offset without a limit builds OFFSET with no LIMIT and rejects )

Done-when / acceptance (verbatim): "the intended behaviour is decided and a red-first cell holds it; or the product owner has chosen to leave it and this ticket is closed with the decision recorded."

- At main 68b080d1: `backend/simpleDb.js:314` builds `OFFSET ?` with no LIMIT guard. `offset` occurs 0 times in `backend/server.js` (control: `getAllPrinterLogs(` occurs 50 times there; those are the file's own wrapper, a different function). Callers outside server.js were not searched.
- **Coordinator decides:** recommend "add LIMIT -1 when an offset arrives without a limit" (SQLite idiom, no caller affected, smallest). Or leave and record it declined: no caller, likelihood low. Either way a change to simpleDb.js needs its gate; sequence after RD-915/-920/-922 (shared `simpleDb.js` with RD-920's `insertPrinterLog`).

### RD-923  (B  not his; To Do; docker/docker-compose.yml builds docker/Dockerfile.frontend and docker/Dockerfile.codellama and neither file i)

Done-when / acceptance (verbatim): "the compose path is retired, or its three Dockerfiles exist and build; or the product owner has chosen to leave it and this ticket is closed with the decision recorded."

- At main 68b080d1: the compose file names three Dockerfiles (`docker/docker-compose.yml:8`, `docker/docker-compose.yml:23`, `docker/docker-compose.yml:45`); the tree holds `docker/Dockerfile.backend` and `docker/docker-compose.yml` under `docker/` (2 files) and the repo root has its own `docker-compose.yml` and `docker-compose.dev.yml`. RD-494 already says the backend Dockerfile cannot build.
- Trap: a test requires `docker/Dockerfile.backend` to stay tracked (`__tests__/auth-gate-fail-closed.test.js:750`); retiring it means changing that line and moving `scripts/verify-expected-counts.json` only if a cell goes. Code search of the repo for the string `docker/docker-compose` returned 0 (control: `Dockerfile.backend` returned 2: this compose file and that test; the code-search index can lag, so this is a weak zero).
- **Coordinator decides:** recommend retire `docker/docker-compose.yml` and `docker/Dockerfile.backend` together under RD-494 (one gated change, the test line edited); "whether anyone runs it locally" is not answerable from the repo (UNMEASURED), but the root compose files exist for local use. Closes RD-918 part (b) as well.

### RD-917  (B  not his; To Do; RD-913 follow-up: streamExport (backend/dataExport.js) stays pending when its destination is destroyed without)

Done-when / acceptance (verbatim): "the three behaviours are decided and each branch has a red-first cell, with a review gate; or the product owner has chosen to leave them and this ticket is closed with the decision recorded."

- At main 68b080d1: the ENOENT warning branch returns silently (`backend/dataExport.js:224`); the archive is created at `backend/dataExport.js:217` (RD-915's `zlib: { level: 9 }` is on the same line; sweep NX1 holds this file).
- **Coordinator decides:** (a) a destroyed destination: reject (recommend; a pending promise is the worst outcome); (b) a vanished file: drop it from the manifest and `filesIncluded` (recommend; the export must not overstate itself); (c) one red-first cell per branch. No word is involved. Whether POST /api/admin/export reaches (a) is unmeasured; it needs a local read of the route, not a hosted call.
- Owner rulings nearby, none covering it: `nexusai-rd913-archiver-route-1101` (ruled b, archiver 8) concerns the dependency, not these branches.

### RD-908  (B  not his; To Do; RD-899 follow-up (gate note on cell J): no cell asserts that the write probe's file is removed after a failed )

Done-when / acceptance (verbatim): "cell J asserts that the directory holds no probe-prefix entry after each failed write and is red under the mutant and green at main, and a gate has read the change; or the product owner has chosen to leave it and this ticket is closed with the decision recorded."

- At main 68b080d1: the unlink is at `backend/jsonStorage.js:413` inside `backend/jsonStorage.js:402`; cell J is `__tests__/rd891-probe-name-race.test.js:594`.
- The ticket's recommendation names "The product owner decides whether it is pinned", then "The gate suggested it ride with the next change to that test file; if it is built alone it needs a gate". No queued lane touches `rd891-probe-name-race.test.js`. **Coordinator decides:** leave in To Do with the note "rides with the next change to rd891-probe-name-race.test.js"; adding an assertion moves no counts. Not worth a gate of its own.

### RD-907  (B  not his; To Do; RD-868 writer: /api/chat logs context.lastSuggestion without logSafe (backend/server.js:7007); the value comes)

Done-when / acceptance (verbatim): "the product owner has decided; if wrapped, the line uses logSafe with a gated change; if left, this ticket is closed with the decision recorded."

- At main 68b080d1 (the ticket was written at 42c7f840; lines moved): the log line is `backend/server.js:7007`; `logSafe` is imported at `backend/server.js:45` and used 26 times in the file.
- The only non-null assignment of `lastSuggestion` in the file is `backend/server.js:8418`; `pattern` comes from `backend/server.js:8359`, whose `suggestion:` values are 10 string literals (lines 8362-8407; counted between the array start and the loop at 8413). The other assignments are `null` (`backend/server.js:5974`, and the clear after the log line). The value is held in a server-side Map keyed by conversation id (`backend/server.js:5961`). Other files were not searched for assignments (UNMEASURED).
- CodeQL: 123 open alerts, all at commit 68b080d1 (the current main); 49 are `js/log-injection` in `backend/server.js` (control: the counter finds them); alerts within `backend/server.js` lines 6990-7020: 0. Instrument: `gh api -X GET repos/.../code-scanning/alerts state=open --paginate`.
- **Coordinator answers:** leave it. A fixed literal cannot inject a log line and the scanner agrees (0 alerts on the line); wrapping costs a red-first cell and its own gate for no change in behaviour. Record it as Declined with these numbers; reversal is cheap because CodeQL would alert if request text ever reached the variable.
- Why this is Tuesday's and not the owner's: the owner's 2026-10-29 ruling on RD-868 (`nexusai-risk-store-writers-rd868-1029`, ruled c, one ticket per writer, delivered as RD-902..RD-907) fixed the process, not this outcome; the ticket text hands the leave-or-wrap choice to "the product owner" only by habit. **Fallback if Tuesday reads that ruling as "each writer is fixed or retired, never left":** wrap it - one line at that location, one red-first cell, a gate; no overlap with the sweep lanes (server.js is not in NX1).
- Same shape, not in this list: RD-902..RD-906 each end with "The product owner decides". One coordinator rule on how those are answered would close all six.

### HPSMPOC-410  (C  ruled or stale; Backlog; [B953] A Demo viewer sees a sample customer's full name on the Home Upcoming activity list and on /customers/q)

Done-when / acceptance (verbatim): "the Demo view of both pages is decided (name kept as a sample, or alias used as the security pages do) and the decision is built or recorded."

- Ruling: card `hpsmpoc-demo-sample-names-services-1029`, ruled a (keep the sample names) at 2026-10-29 20:41:18; delivered as HPSM-POC CLARIFICATIONS C-225. Its text: "Home already shows Demo one sample name today"; "they are labelled sample data, and the alias rule covers the customer frame only". Card `hpsmpoc-sample-customers-placeholders` (ruled a) concerns the seed content.
- Gap I found: that card names Home and the Service offers pages; `/customers/quollridge` (the profile "Customer name") is not named. It is not the customer frame, and the name reads "(sample)", so the same reasoning covers it; that is the coordinator's extension and goes into the record as such. If Tuesday doubts it, it is a one-line card; I judge it covered.

### HPSMPOC-412  (C  ruled or stale; Backlog; [B960-3] Follow-up to PR #256: the Home third tile and one next-actions sentence still carry the old Services )

Done-when / acceptance (verbatim): "both are changed to the new label or recorded as declined."

- Ruling: card `hpsmpoc-services-menu-label-1101`, ruled a at 2026-11-02 06:09:41, delivered as HPSM-POC records C-270: "The tile change goes ahead ... The one Home sentence changes too, as a small follow-up that is tested."
- Item 1 is built at main 5f128fb8: `web/src/components/partner/PartnerDashboard.tsx:249`. Item 2 is not: `web/src/components/partner/home-next-actions.ts:12`. The ruled replacement is the old word swapped for the new; the mechanical result "Compare the delivery phases, phase by phase." repeats "phase", so the final wording is one pack row (a records or build seat proposes; no card).
- Lane: `web/src/components/partner/home-next-actions.ts` + its test, about 2 files, under 20 lines; no shared path with the sweep's live seats (H104 holds `ClientPacks.tsx` etc., not these).

### HPSMPOC-420  (C  ruled or stale; Backlog; [B967-5] Wording for the product owner: the customer frame chip reads "1 of 3 questions answered" while the As)

Done-when / acceptance (verbatim): "the wording is ruled (kept, or one count made to agree with the other) and built, or the item is recorded as declined."

- Cards (read with `decision_queue.sh show`): `hpsmpoc-answers-so-far-words-1102` - ruled b (change "N answers so far" lines to the scored count too) at 2026-11-02T16:51:53; `hpsmpoc-snapshot-recap-tile-words-1102` - ruled b (label "Scored questions answered", N of M, "Not recorded" when no figure) at 2026-11-02T17:09:27; `hpsmpoc-frame-chip-count-1101` and `hpsmpoc-scored-tile-label-1102` earlier. The ticket's own comment 40670 (16:19) says the remaining lines are "the product owner's words decision": that decision is made.
- Remaining: a builder change for the engagement overview, the snapshot launcher and the snapshot result tile (the card's default says it goes ahead "once the links fix lands"); the words are the accepted ones from the cards. Not a question.

### RD-918  (C  ruled or stale; To Do; RD-913 follow-up: sqlite3 6 arrives through an install script that npm 11.19 warns about on every install, and)

Done-when / acceptance (verbatim): "the install path is measured and either named in the allow list or shown unnecessary, and the compose base image is raised or the path recorded as retired; or the product owner has chosen to leave it and this ticket is closed with the decision recorded."

- Ruling: card `nexusai-sqlite3-successor-recommendation-1102`, ruled a at 2026-11-02T10:30:49 (stay on sqlite3 6.0.1; record four triggers, one being "npm blocking install scripts by default"); delivered as NexusAI CLARIFICATIONS C-230 and RD-919 comment 40657. Nothing is built by it.
- Measured already (RD-918 comment 40656): the script runs today on npm 11.19; a deny entry breaks the driver; an approve entry is config only. So part (a) is "shown unnecessary today" and the trigger is recorded. Part (b) (the compose base image) is the compose path: decided by RD-923 (retire).
- Action: a records seat comments the above on RD-918 and moves it with RD-923. Not a question.

### MPSCALC-364  (A  owner's; Backlog; [B1086-5] Published sentences about the four staff list columns say no row carries them; the code fills three )

Done-when / acceptance (verbatim): "The product owner has approved the sentences;"

- Stale text now (all printed at main 0d4022b9): `docs/API.md:367`; `docs/api/openapi.json:1508`; code comment `src/MpsCalc.Api/Contracts/Dtos.cs:461` (not published). The code fills three of four columns for a purchase quote and one for a rental (`src/MpsCalc.Api/Quotes/QuoteFigures.cs:125` to the next two lines; code-read only, no request run).
- Why the owner: the records list "the ownership of the developer-docs wording" as an open point (CLARIFICATIONS "Open, not ruled" (b), `1_Project_Definition/CLARIFICATIONS.md:2387`), and he has ruled developer-doc sentences one per card before: `mps-unchanged-save-api-sentence-1025` (ruled a), `mps-345-importer-sentence-1102` (ruled a, the second with a default of "the new sentence stands"). No card cites MPSCALC-364.
- Before asking: a local request (not a hosted one) to confirm what a list row carries; that is an agent step with no word. The question below is written so it can go after it, with the sentence marked as the seat's measurement.

### HPSMPOC-424  (A  owner's; Backlog; [B989-6] Remediation register: one old Verified-complete entry with invisible-only evidence in a tab makes the)

Done-when / acceptance (verbatim): "the product owner has chosen, and the choice is built and pinned by a row, or the item is recorded as declined."

- Mechanism at main 5f128fb8: one failing entry makes the parser return null (`web/src/components/customer/remediation-store.ts:75`), and the register falls back to empty. The parser also returns null for any entry not exactly as this build wrote it (`web/src/components/customer/remediation-store.ts:59`), so every future tightening of `checkEntry` has the same blast radius, not only invisible characters. Storage is the tab's sessionStorage (`web/src/components/partner/browser-store.ts:36`).
- No card or ruling cites HPSMPOC-424 (key search 0; subject searches "remediation register|Verified complete" 0; the 2026-10-01 card `hpsmpoc-refuse-more-invisible-characters` ruled a is about which characters to refuse, not about what happens to stored entries).

### HPSMPOC-425  (A  owner's; Backlog; [B989-12] Remediation register: invisible-only evidence is still accepted for Evidence submitted (and for Not )

Done-when / acceptance (verbatim): "the product owner has chosen, and the choice is built and pinned by rows, or the item is recorded as declined."

- The rule applies to one state only (`web/src/components/customer/remediation-store.ts:40`); the refusal sentence already exists, so options b and c add no new word.
- No card cites it (key 0, subject 0). Same file and same gate as HPSMPOC-424: if both are built, one seat.

## (A) Ready-to-paste owner questions (cards are NOT posted; `decision_queue.sh add` is the coordinator's)

Each follows the queue's fields. Plain words, one question each, a default that keeps work moving. Check the prior-ruling gate (`decision_queue.sh prior --id ... --title ...`, read-only) before adding.

### Q1  `mps-364-staff-column-sentences-1102`  (Datasec/MPS-Commercial-Calculator)  [ask after the seat confirms by a local request what a list row carries]
- title: MPS calculator: approve a corrected sentence for the quote-list staff columns?
- bluf: Kam, two developer-document sentences say the four staff-only figures on the quote list are "not filled yet". The code fills three of the four for a purchase quote and one for a rental (read from the code; a request will confirm before this is built). The docs are developer-only; no customer reads them; nothing is deployed. Proposed, for API.md and for the `oneOffGp` description in the contract file: "On a purchase quote a list row carries oneOffGp, tcv and totalGp; annualRecurringGp is not filled yet. On a rental quote a row carries tcv only." and "Absent for any other caller, for a quote with no calculation, and for a rental quote." The sentences change again when the recurring-GP ticket (MPSCALC-315) lands.
- options: a: Approve these two sentences (a builder edits the contract file, the contract text and the generated copies together, through a gate; ships with the next MPS deploy, its own card). b: Change the words (reply with them). c: Leave the sentences as they are (they stay untrue for three columns).
- recommended: a
- default_action: Treated as c: the sentences are not edited and nothing else waits; the ticket stays open.
- recommendation measured by: UNMEASURED (code read only); the recommendation holds if the local request agrees.

### Q2  `hpsmpoc-424-saved-register-one-bad-entry-1102`  (Datasec/HPSM-POC)
- title: HPSM-POC: if one saved remediation entry no longer passes the rules, should the whole saved list vanish?
- bluf: Kam, today one old entry that the current rules refuse (for example a "Verified complete" entry whose evidence is only invisible characters) makes the roadmap read the whole saved register as empty after a reload, with no message; the next save then overwrites the rest. It happens only in a browser tab that was left open across the change, and only for entries an earlier build wrote. Nothing is deployed.
- options: a: Keep as now. b: Drop only the failing entry and keep the rest (no new words). c: Keep the rest and show a message that some saved values could not be read (a new sentence, which would come to you as words). d: Leave it; no change, ticket closed as declined.
- recommended: b. Measured by: the gate's browser run (one failing entry lost the whole register and one later save lost the rest); how often a tab is left open across a change is unmeasured. The parser also drops the whole register for any entry not written exactly as this build writes it, so every future rule change has the same effect.
- default_action: Treated as d: nothing is built; HPSMPOC-424 is recorded as declined. Nothing else waits.

### Q3  `hpsmpoc-425-evidence-submitted-invisible-1102`  (Datasec/HPSM-POC)
- title: HPSM-POC: should "Evidence submitted" refuse an evidence reference that shows nothing?
- bluf: Kam, "Verified complete" already refuses evidence made only of invisible characters; "Evidence submitted", "Not started" and "In progress" still accept it. A reference that shows nothing is not a reference, and "Evidence submitted" says one was given. The refusal sentence already exists, so no new word. Nothing is deployed.
- options: a: Leave as now (Verified complete only). b: Refuse it for Evidence submitted too. c: Refuse it for every state that carries evidence.
- recommended: b. Measured by: the gate ran the three other states in unit rows and saw the Verified complete refusal on the real screen; the effect on a customer is unmeasured.
- default_action: Treated as a: nothing is built; HPSMPOC-425 stays open (or is recorded as declined). Nothing else waits.

## UNMEASURED

- MPSCALC-364: what a list row actually returns for a purchase and a rental quote (code read only; no request run).
- MPSCALC-272: which of the five tiles other than annual recurring GP have a server figure today.
- MPSCALC-274: the maximum length of the existing approval `Comment` (not read).
- MPSCALC-360: whether a usage-only line's quantity is "devices" in X-25's device total (a reading, recommended no).
- PCOMP-12: whether any content release declares a device-group typed sub-answer (my scan found no key named like `device_group` but had no positive control).
- HPSMPOC-436: whether any route calls `NarrativeInputProjector.Project` with a zero-finding assessment or an empty id list (callers not read).
- HPSMPOC-432: whether a screen reader reads the evidence table caption twice (the 409 measurement was on another table).
- HPSMPOC-424: how often a tab stays open across a change.
- RD-907: assignments of `lastSuggestion` in files other than `backend/server.js`.
- RD-917: whether POST /api/admin/export can reach the destroyed-destination case.
- RD-921: callers of the method outside `backend/server.js`.
- RD-923: whether anyone still runs the `docker/` compose path locally.
- Whether the owner has delegated "leave it" outcomes on low-likelihood tickets to the coordinator (not stated in any file I may read).
- The seven check runs the sweep left unread on HPSM #275; the 23 tickets' other fields (links, assignee) beyond description and comments.

## Outside the fences

Nothing written outside this file. Reads beyond the briefed inputs, all read-only: Jira GET (the 23 tickets, plus MPSCALC-253, -267, -300, -315, HPSMPOC-408, RD-494, RD-902..906 for context, and the 404 control); `decision_queue.sh show` on 24 card ids; `decisions.json` through the `Datasec/` inclusion filter; `gh api -X GET` for contents, trees, commits and code-scanning alerts on the four Datasec repositories (file contents saved to the session scratchpad, not the project); the MPS records file `1_Project_Definition/CLARIFICATIONS.md` and `BACKLOG.md` on the local working tree (read, not origin); `DRAFTER_RULES.md` and the sweep brief. One fence note: the drafter rules forbid reading a card except by `show`; the `Datasec/` filter over `decisions.json` is the sweep's own method and the brief's instruction, and printed only ids and status for matches. No hosted host was contacted. No `git` command was run in any project repository. The scratch fetcher reads each project `.env` in-process and prints no token.

READ-WHOLE-BY-TUESDAY: ____
