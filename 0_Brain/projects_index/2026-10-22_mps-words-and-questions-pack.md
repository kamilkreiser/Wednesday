# MPS Commercial Calculator: words and questions pack (decision pack for the product owner)

Drafted 2026-10-22 by a read-only drafter for Tuesday. Datasec / MPS Commercial Calculator only. Nothing here is ruled; every recommendation is a suggestion for the product owner.

## BLUF

- **55 new on-screen words** held across three branches: B444 = 10, B445 = 42 (33 screen words + 9 format messages), B446 = 3. All three counts match the gates (10, 42, 3).
- **8 product questions** (Q1 to Q8). None changes a customer-facing figure.
- **Recommended one-line answer (tap this):**
  `Words: approve all 55 as built, except two changes: B445 S15 "Deal: add consumable" becomes "Add deal consumable", and B446 W-1 last sentence becomes "Please try again later." Questions: Q1a Q2a Q3a Q4a Q5a Q6a Q7a Q8b.`
- If the product owner prefers no changes at all: "approve all 55 as built; Q1a Q2a Q3a Q4a Q5a Q6a Q7a Q8b" also works. The two changes are small; the second one fixes a sentence that can mislead (see B446 below).
- Heads read (read-only `ls-remote`, 2026-10-22 evening): B444 `e23cfb58298feb629d1b84d7cace85777345726d`, B445 `e869d461bcc1acf532fbb764b4c64b2f60239f45`, B446 `02a0cb17ccab59e452424d075c14b9fd3f0e8142`.
- One thing Tuesday must know before merging B444: the head `e23cfb58` is ONE commit past the head the last gate passed (`00f14bb4`, B455). That commit is a one-line escape fix (B455-1, Minor) in `QuoteEndpoints.cs`, "no behaviour change", and no word is touched. No QA gate names `e23cfb58` as its object. See FOUND.

How to read the lists: "Approve" means approve as built. "Alt" gives the exact replacement and one reason. "Visible" means shown on screen. "Screen-reader name" means the text is an accessible name (`aria-label`) that a sighted user does not see; the visible text beside it is an existing, already-approved word.

---

## WORDS

### Counts by program (asserted against the gates)

| Branch | Ticket | Gate | Words found at gated head | Gate's count | Match |
|---|---|---|---|---|---|
| B444 | MPSCALC-137, -172 | B451, B455 | 10 (5 screen + 5 error-box sentences) | 10 | yes |
| B445 | MPSCALC-160, -150 UI | B452, B457 | 33 screen words + 9 format messages = 42 | 33 + 9 = 42 (B452 C6, B457 "words unchanged 33 + 9") | yes |
| B446 | MPSCALC-174, -165 | B454 | 3 (MPSCALC-165 adds 0) | 3 | yes |

How the counts were checked: I read each `WORDS-PENDING` block at the gated head by `git show <sha>:<path>`, and counted the string literals inside each block with a program (a block-only extractor, comment lines dropped, positive control: a planted literal counted, a planted comment line not). B445 literal totals per file reconcile to 33 + 9 once the non-word literals are taken out (type tags `'Mono'|'Colour'`, `'Unit cost'|'Yield'`, the `Deal consumable ${i}` stem, and three reused column headings): draftModel 11 literals = 9 messages + 2 type tags... (full reconciliation in NOT TESTED note 2). Note that "Deal mono click", "Deal colour click" and "Deal ink rate" are counted twice on purpose: once as a field label (screen word) and once as the start of the "<name> is not a number" message (format message). That is how the gates count them too.

### B444: owner self-approval (137) and Approver outcome correction (172)

Branch `b444/self-approval-137-outcome-correction-172` @ `e23cfb58` (gated @ `00f14bb4`). Words are in two blocks headed `WORDS-PENDING B444`: `web/src/screens/Lifecycle.tsx:9-17` and `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:1228-1234`. All staff-only; none reaches a customer document.

**Screen: Quote screen, Review & approval**

| Id | Where it appears | Exact text | Recommendation |
|---|---|---|---|
| W-1 | Above Approve / Reject, for the quote's owner who holds Approver (`Lifecycle.tsx:11`) | `This is your own quote. Approving or rejecting it is recorded as a self-approval.` | Approve |
| W-2 | Button that opens the correction; also its screen-reader legend (`Lifecycle.tsx:13`) | `Correct outcome` | Approve |

**Screen: Quote screen, the outcome correction form**

| Id | Where it appears | Exact text | Recommendation |
|---|---|---|---|
| W-3 | Radio choice (`Lifecycle.tsx:14`) | `Clear outcome` | Approve (beside the existing "Won" and "Lost") |
| W-4 | Reason field label (`Lifecycle.tsx:15`) | `Correction reason (required)` | Approve |
| W-5 | Confirm button (`Lifecycle.tsx:16`) | `Save correction` | Approve |

**Screen: Quote screen, red error box (text from the server, `QuoteEndpoints.cs`)**

| Id | Shown when | Exact text | Recommendation |
|---|---|---|---|
| W-6 | Outcome already recorded (409). Changed sentence (`:1229`) | `This quote's outcome is already recorded. An Approver can correct it, with a reason.` (today: "This quote's outcome is already recorded; it cannot be changed.") | Approve |
| W-7 | Bad correction value (400) (`:1230`) | `outcome must be won, lost or cleared.` | Approve (the form only sends those three values, so a person rarely sees it) |
| W-8 | Missing or too long reason (400) (`:1231`) | `A correction needs a reason of 1 to 2000 characters.` | Approve |
| W-9 | No outcome recorded yet (409) (`:1232`) | `This quote has no recorded outcome to correct.` | Approve |
| W-10 | Correction equals the current outcome (409) (`:1233`) | `This quote's outcome is already won; a correction must change it.` ("lost" when lost; counted as one word) | Approve |

Reused and not counted: "Won", "Lost", "Cancel", "Approve", "Reject", the role refusal "This action needs the role Approver (SEC-RBAC-001).", and the control-character sentence. Removed from view: "You can't approve your own quote." beside disabled buttons.

B444 total: 10. Recommendation: **approve all 10 as built.**

### B445: partner referral rebate default (160) and deal usage screens (150 UI)

Branch `b445/rebate-default-160-usage-screens-150` @ `e869d461`. Seven blocks headed `WORDS-PENDING B445`, in `web/src/app/draftModel.ts:83-91`, `web/src/components/infoHintWords.ts:26-30`, `web/src/screens/bom/DealSupplies.tsx:13-27`, `DealUsage.tsx:15-24`, `DealUsageResultView.tsx:7-20`, `PageEstimateRow.tsx:10-15`, `PurchaseBomEditor.tsx:58-62`. Staff-only; none reaches the customer proposal. "Deal" prefixes are the builder's naming for the deal-level (whole quote) rates, as opposed to the old per-section rates.

**Screen 1: Purchase BOM panel, each section card (internal)**

| Id | Where | Exact text | Recommendation |
|---|---|---|---|
| S1 | Rebate input label (`PurchaseBomEditor.tsx:60-61`) | `Section n rebate · Partner referral rebate` (today "Section n rebate") | Approve (see Q3 for the prefix) |
| S2 | The (i) hint "About section rebate" (`infoHintWords.ts:28`) | `The partner referral rebate: a percentage of this section's total that is deducted from the margin. It does not change the customer's price. A new section starts with the standard rebate; set it to zero for a direct deal, which has no referral overhead.` | Approve (no figure in the text, so it stays true if the 7% changes) |

**Screen 2: Deal usage rates panel (top of the purchase BOM panel; see Q1 for placement)**

| Id | Where | Exact text | Recommendation |
|---|---|---|---|
| S3 | Panel group name, screen-reader name (`DealUsage.tsx:16`) | `Deal usage rates` | Approve |
| S4 | Panel heading (`:17`) | `Deal usage rates (ex GST)` | Approve |
| S5 | Panel note (`:18`) | `The charge to the customer for each page printed, set once for the whole deal. The pages each device is expected to print are entered under that device’s line.` | Approve |
| S6 | Field label (`:19`) | `Deal mono click` | Approve |
| S7 | Field label (`:20`) | `Deal colour click` | Approve |
| S8 | Field label (`:21`) | `Deal ink rate` | Approve |
| S9 | Field label (`:22`) | `Deal ink unit` | Approve |
| S10 | Placeholder in the three rate fields (`:23`) | `none` (today "calculated or none" on the old per-section fields) | Approve |

**Screen 3: Deal supplies, inside the deal panel (internal callers only)**

| Id | Where | Exact text | Recommendation |
|---|---|---|---|
| S11 | Tick box name, screen-reader name (`DealSupplies.tsx:14`); the visible text beside it is the existing "Calculate click rates from supplies (internal)" | `Deal calculate rates from supplies` | Approve |
| S12 | Percent field label (`:15`) | `Deal mono margin` | Approve |
| S13 | Percent field label (`:16`) | `Deal colour margin` | Approve |
| S14 | Table caption (`:17`) | `Deal consumables` | Approve |
| S15 | Add button (`:18`) | `Deal: add consumable` | **Alt: `Add deal consumable`.** Reason: it matches the other buttons ("Add section"); the colon reads like a heading, not an action. |
| S16 to S21 | Per-row cell names, screen-reader names (`:20-25`); visible headings are the existing Part, Description, Mono, Colour, Unit cost, Yield (pages) | `Deal consumable n part`, `Deal consumable n description`, `Deal consumable n mono`, `Deal consumable n colour`, `Deal consumable n unit cost`, `Deal consumable n yield` (6 words) | Approve |
| S22 | Row remove button name, screen-reader name (`:26`) | `Remove Deal consumable n` | Approve |

**Screen 4: Device line sub-line in the BOM table**

| Id | Where | Exact text | Recommendation |
|---|---|---|---|
| S23 | Caption (`PageEstimateRow.tsx:11`) | `Estimated pages per device per month` | Approve |
| S24 | Group name, screen-reader name (`:12`) | `BOM line n page estimate` | Approve |
| S25 | Field label (`:13`) | `BOM line n mono pages per device per month` | Approve ("BOM line n" is how the app already names line fields) |
| S26 | Field label (`:14`) | `BOM line n colour pages per device per month` | Approve |

**Screen 5: Deal usage result table (under the calculation)**

| Id | Where | Exact text | Recommendation |
|---|---|---|---|
| S27 | Table caption (`DealUsageResultView.tsx:8`) | `Deal usage` | Approve |
| S28 | Column (`:12`) | `Mono pages a month` | Approve |
| S29 | Column (`:13`) | `Colour pages a month` | Approve |
| S30 to S33 | Four columns shown only with internal metrics (`:18`) | `Deal mono cost per page`, `Deal colour cost per page`, `Deal calculated mono`, `Deal calculated colour` (4 words) | Approve |

Screen words: 2 + 8 + 12 + 4 + 7 = **33**. Reused unchanged, not counted: Basis, Devices, Mono click, Colour click, Ink rate, e.g. ml, Part, Description, Mono, Colour, Unit cost, Yield (pages), Remove, the "Calculate click rates from supplies (internal)" text.

**Format messages (9).** Each appears in the "fields to fix" list as `<name> is not a number` (`draftModel.ts:83-91`). All follow the existing "Section n: ..." pattern. Recommendation: **approve all 9 as built.**

| Id | Name that goes before "is not a number" |
|---|---|
| F1 | `Deal mono click` |
| F2 | `Deal colour click` |
| F3 | `Deal ink rate` |
| F4 | `Deal mono margin` |
| F5 | `Deal colour margin` |
| F6 | `BOM line n: Mono pages per device per month` |
| F7 | `BOM line n: Colour pages per device per month` |
| F8 | `Deal consumable n: Unit cost` |
| F9 | `Deal consumable n: Yield` |

B445 total: 33 + 9 = **42**. Recommendation: approve 41 as built; one alt (S15).

### B446: feedback rate limit (174) and start-refusal words (165)

Branch `b446/feedback-rate-limit-174-start-refusal-words-165` @ `02a0cb17`. Blocks headed `WORDS-PENDING B446` in `web/src/feedback/words.ts:13-15` and `src/MpsCalc.Api/Feedback/FeedbackEndpoints.cs:30-35`.

| Id | Where it appears | Exact text | Recommendation |
|---|---|---|---|
| W-1 | Feedback dialog, red line under the form after the 20th message in an hour (`words.ts:15`). All staff see this. | `You have sent a lot of feedback in the last hour. Please wait a few minutes and try again.` | **Alt: `You have sent a lot of feedback in the last hour. Please try again later.`** Reason: the limit is 20 in any rolling 60 minutes, so the wait can be up to an hour; "a few minutes" can be untrue. |
| W-2 | API reply detail only; no screen shows it (the dialog uses W-1) (`FeedbackEndpoints.cs:32-33`) | `This server stores at most {n} new feedback items per person in any 60 minutes. Nothing was stored; try again after the Retry-After time.` ({n} is 20 by default) | Approve |
| W-3 | Operator console at start only, if the setting is outside 1 to 10000; no staff or customer screen (`:35`) | `Start refused: MpsCalc:Feedback:RateLimit:PerHour must be a whole number from 1 to 10000 (default 20).` | Approve |

MPSCALC-165 adds 0 new words. Three existing console sentences gain the existing prefix `Start refused: ` (`DevStubAuth.cs`), shown only in the terminal or App Service log. Not counted, as the brief rules. B446 total: **3**. Recommendation: approve 2 as built, one alt (W-1).

### Words summary

| Branch | Held | Approve as built | Alt |
|---|---|---|---|
| B444 | 10 | 10 | 0 |
| B445 | 42 | 41 | 1 (S15) |
| B446 | 3 | 2 | 1 (W-1) |
| Total | 55 | 53 | 2 |

If the product owner picks an alt, the change is one line in one `WORDS-PENDING` block (S15: `DealSupplies.tsx:18`; W-1: `words.ts:15`). The test rows that look the text up by name would need the same one-word edit (builder seat, then a delta gate).

---

## QUESTIONS

Each question is one decision. "Who acts" names the next actor for each option. Code references are at the gated heads: B445 `e869d461`, B444 `e23cfb58`, B446 `02a0cb17`. Q1 to Q4 come from gate B452 Notes N1, N2, N5, N6; Q5 to Q8 from gate B457 Notes N1, N2, N3, N6. B457 held that none of these blocks a GO.

### Q1. Where should the deal usage rates panel sit? (B452 N1)

**Decision:** keep the panel at the top of the purchase BOM panel, or move it under the deal tile?
**Code today:** the panel is mounted at the top of the BOM panel, under the section-label hint, in the "sections" view only (`web/src/screens/bom/PurchaseBomEditor.tsx:222-223`). Moving it means a change in `QuoteScreen.tsx`, which the builder was told not to touch. The builder disclosed this (FOR TUESDAY 5); the gate rated it a layout call, not a defect.
**Options:**
- **a. Ship it where it is.** Who acts: Tuesday opens the PR and merges after the words ruling.
- **b. Ship now, raise a small ticket to move it under the deal tile later.** Who acts: Tuesday merges; the records seat files the ticket; a later builder seat does the move and a gate checks it.
- **c. Hold the branch until it is moved.** Who acts: Tuesday briefs a builder seat for `QuoteScreen.tsx`, then a new gate; the other words wait too.
**Recommendation: a.** It is layout only, nothing on the screen is wrong or missing, and holding three branches for it costs more than it fixes. (b is the next best if the product owner wants it moved eventually.)

### Q2. Should page estimates be offered on optional device lines? (B452 N2)

**Decision:** a device line ticked "optional" currently shows the page-estimate boxes; the calculation ignores them. Leave it, or hide the boxes on optional lines?
**Code today:** the sub-line shows for any device line that is not a credit line (`PurchaseBomEditor.tsx:383` `isDevice` excludes only `credit`; mounted at `:470-472`). The engine counts only lines that are not optional and not credit (`src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs:724`). Pages typed on an optional line are kept and sent but add nothing; they count if the line is later made non-optional.
**Options:**
- **a. Leave as built.** Who acts: Tuesday merges. Nothing wrong is totalled; the typed pages simply wait.
- **b. Hide the boxes on optional lines.** Who acts: Tuesday briefs a small builder fix (no new words), then a delta gate. Risk: pages already stored on a line that is later ticked optional vanish from view.
- **c. Keep them and add a note "not counted while optional".** Who acts: builder plus a new word for the product owner to rule, then a gate.
**Recommendation: a.** The totals are right either way, and the pages are not lost if the line becomes firm. Raise b only if staff are confused in use.

### Q3. Keep "Section n rebate" at the front of the rebate label? (B452 N5)

**Decision:** label reads `Section 2 rebate · Partner referral rebate`. Keep that, or drop the prefix?
**Code today:** `sectionRebateLabel = Section ${n} rebate · Partner referral rebate` (`PurchaseBomEditor.tsx:61`; used at `:308`). The builder kept the old prefix because three unit tests and `web/e2e/bom.spec.ts` find the field by it. The ruling K-13 says the rebate is "shown as Partner referral rebate".
**Options:**
- **a. Keep both parts (as built).** Who acts: Tuesday merges. The section number tells which section the rebate belongs to.
- **b. Show only `Partner referral rebate`.** Who acts: builder re-points the tests and e2e (`bom.spec.ts:204/340`), then a delta gate. Several sections would then show the same label.
- **c. `Section n partner referral rebate`** (no dot, plain sentence form). Who acts: same as b.
**Recommendation: a.** It already carries the ruled name, keeps sections apart, and costs nothing to ship. Prefer c only if the dot looks odd on the real screen.

### Q4. Build inputs for the K-11 target-click rates now? (B452 N6)

**Decision:** the two optional "target click" figures (`targetMonoClick`, `targetColourClick`) have no field on the deal screen. Build them in this round, or later?
**Code today:** the fields exist in the API contract (`web/src/api/generated/schema.ts:1612`) but no screen file reads them. A stored value is kept untouched when the supplies are edited (`DealSupplies.tsx:35`, the spread keeps unrelated members). The builder did not build them (ADDENDUM-4: "Not built").
**Options:**
- **a. Later.** Who acts: Tuesday merges now; a future brief covers the inputs and their words.
- **b. Build now.** Who acts: Tuesday briefs a builder seat (new fields and new words), a new gate, and the product owner rules the new words; all three branches' ship date moves.
**Recommendation: a.** Nobody can enter these today, so nothing is lost or wrong; stored values survive; building them adds more words to rule.

### Q5. Is a typed 7% on a new section fine without a reason? (B457 N1)

**Decision:** a new section starts at 7% and saves without a reason. A person who types 7 into that field gets the same treatment. Accept that?
**Code today:** the web compares by number (`web/src/screens/quote/autosave.ts:18`, applied to added sections at `:29`), and the percent box turns a typed 7 into `0.07` (`web/src/components/PercentInput.tsx:31-34`), so it cannot be told from the default. The server does the same (`src/MpsCalc.Api/Quotes/PriceAudit.cs:58`, `addedAtDefault`). At main, a typed 7% needed a reason.
**Options:**
- **a. Accept.** Who acts: Tuesday merges. The stored value is the default either way; any other rebate still needs a reason.
- **b. Exempt only an untouched default.** Who acts: builder (a "was typed" flag across the web, stub and server) plus a new gate; more code for no change in the saved number.
**Recommendation: a.** The saved figure is identical to the default, so a reason would explain nothing. Tuesday already accepted this reading at the stamp.

### Q6. Should the audit still record the default rebate of a new section? (B457 N2)

**Decision:** when a section is added at 7% the audit trail now records no rebate line for it, even if the person typed a reason for other changes in that save. Accept that?
**Code today:** `PriceAudit.cs:58-62` skips the `sections[id].rebatePercent` entry for a section added at the default on a non-create save. On create, every starting value is still recorded. The value itself is saved in the quote; the first later change of that rebate is audited and needs a reason.
**Options:**
- **a. Accept.** Who acts: Tuesday merges. The trail still shows every change away from the default.
- **b. Record the default with a fixed reason text.** Who acts: builder plus a new word for the product owner to rule, then a delta gate.
- **c. Record it only when the person did type a reason.** Who acts: builder (web, stub and server), then a delta gate.
**Recommendation: a.** The 7% is a rule (K-13), not a choice by the person; what an auditor needs is each departure from it, and those are recorded.

### Q7. Should removing a saved default section need a reason? (B457 N3)

**Decision:** a section added at 7% and saved becomes a stored section. Removing it later needs a price-change reason. Keep that?
**Code today:** the web (`autosave.ts:42-45`, stored ids at `:44`) and the server (`PriceAudit.cs:50-62`) treat the stored 7% going to "removed" as an audited change. Measured by the gate: add returns 200, then remove without a reason returns `400 PRICE_REASON_REQUIRED`. At main a new section had no rebate, so add, save, remove needed none.
**Options:**
- **a. Keep (as built).** Who acts: Tuesday merges. It follows the ruling "a stored section's rebate change still needs a reason".
- **b. Exempt removal when the rebate is still the default.** Who acts: builder (both tiers) plus a delta gate.
**Recommendation: a.** Removing a section changes the quote's price and margin, so a reason is the right trail; it is one short sentence typed once.

### Q8. What if "Add section" is clicked before the price list has loaded? (B457 N6)

**Decision:** a section added in the first moments, before the inventory reply arrives, gets no 7% default. Fix that?
**Code today:** the editor decides pricing rights from `pricing = mayEditQuotePricing(...) && inventory?.internalMetricsIncluded` (`web/src/screens/QuoteScreen.tsx:99-100`), which is false until the inventory loads; `addSection(draft, '', newClass, pricing)` then adds no rebate (`PurchaseBomEditor.tsx:141`; `bomModel.ts:51-53`). The gate's probe: six rapid clicks, section 1 sent with no rebate, sections 2 to 6 at 0.07. The field is editable, so the person can set it; nothing warns them. A missing rebate means a higher margin than intended on that section.
**Options:**
- **a. Accept, no follow-up.** Who acts: Tuesday merges.
- **b. Ship now and raise a small follow-up ticket** (wait for the inventory before enabling Add section, or apply the default when it arrives). Who acts: Tuesday merges; the records seat files the ticket; a later builder seat fixes it with a gate.
- **c. Hold the branch for the fix.** Who acts: Tuesday briefs a builder fix round on B445, then a new gate.
**Recommendation: b.** The window is short and the fix is small, but the whole point of ticket 160 is the default, so it should not be left unfiled. It does not justify holding the branch.

---

## FOUND / TESTED / HOW / NOT TESTED / UNMEASURED

**FOUND**
1. Word counts match every gate: B444 10, B445 33 + 9 = 42, B446 3. Total 55.
2. The B445 builder STATUS still says "words held: 21" in its BLUF and word pack (written at the first commit); it grew to 33 + 9 at ADDENDUM-4 (`6d0726e1`) and stayed there through B456 (`e869d461`). The 21 is stale, not a mismatch. The B452 and B457 gates both count 33 + 9 and both found 0 words outside the pack.
3. B444's current remote head `e23cfb58` is one commit past the gated head `00f14bb4` (B455 verdict). The extra commit changes one line in `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs` ("escape the bidi bounds in HasBidiControl (B455-1); no behaviour change"). `git diff --stat 00f14bb4 e23cfb58` = 1 file, 1 insertion, 1 deletion. The B444 builder reports filters 115/115 and 98/98 on it. No gate STATUS file names `e23cfb58` as its object (B457 only lists it as a branch pin). Tuesday should decide whether that is covered by its own delta rule before merging; it is not a word.
4. The words of B444 at `e23cfb58` equal the pack (W-1 to W-10 read from the two blocks).
5. Several B445 "words" are screen-reader names, not visible text: S3, S11, S16 to S22, S24 (verified at `DealSupplies.tsx:40,77-89` and `DealUsage.tsx:56`). Approving them is a formality for a sighted user but they are counted in the 33, as the gates count them.
6. B446 W-1 says "wait a few minutes" while the server limit is a rolling 60 minutes; that is the reason for the alt.
7. B446 W-2 and W-3 are never shown on a staff or customer screen (API detail and console), so they carry no usability risk.
8. Remote refs also show `b450/feedback-ticket-test-main-red` at `e03fe7c7` and main at `35887699` (moved since the B444/B445/B446 stamps at `f5b6f5a7`); the B457 gate checked B445 against `35887699`. Not re-checked here.

**TESTED**
- Heads for B444, B445, B446 read with `git ls-remote origin` (read-only, `--no-optional-locks`); each word block read with `git show <sha>:<path>`.
- Per-file literal counts inside the B445 blocks, with a positive control (a planted literal counted, a planted comment line not; control returned 1 of 1).
- Code references for Q1 to Q8 read at the gated head; `path:line` as printed above.
- All nine STATUS files (B444, B445, B446, B451, B452, B454, B455, B456, B457) read for the verdicts, the Notes and the word counts.

**HOW**
- Read-only git and file reads only. No fetch, no checkout, no worktree, no Jira, no HTTP, no `az`, no mail, no publish. One file written (this one).
- Wording alternatives are the drafter's judgement for plain Australian English; they are not tested on a screen.

**NOT TESTED**
1. No screen was run or rendered (no server, per the fences): visible versus screen-reader status of each word is read from the source, not seen. The only check is the `aria-label` lines named above.
2. The B445 literal reconciliation: draftModel block 11 literals = 5 field names + the `BOM line n` stem + `Mono`/`Colour` tags + the `Deal consumable n` stem + `Unit cost`/`Yield` tags (9 messages built from 5 + 2 + 2); DealSupplies 13 = 12 words + the `Deal consumable ${i}` stem; DealUsage 8 = 7 + placeholder; DealUsageResultView 12 = caption + 7 column strings (3 reused: Basis/Devices excluded, Mono click/Colour click/Ink rate reused) + 4 internal... The totals agree with the gates' independent count of 33 + 9; I did not re-derive the gates' program.
3. I did not open any test file, so which tests would change with S15 or W-1 is not listed.
4. I did not run, and did not re-measure, the B457 probe rows behind Q5 to Q8 (they are the gate's measurements, cited).

**UNMEASURED**
- How many of the 55 words a sighted staff member actually sees: 15 are screen-reader names or console / API-only text, but the exact visible set was not rendered.
- Whether any staff would type pages on optional device lines (Q2) or click Add section before the inventory loads (Q8) in real use; no usage data exists.
- Whether the 7% default appears in any real saved quote today (no hosted data was opened).
- Whether `e23cfb58` has passed a full CI line on the hosted runner (builder's local line only).
