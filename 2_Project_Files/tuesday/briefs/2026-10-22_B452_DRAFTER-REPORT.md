# B452 drafter report (read-only drafter, 2026-10-22 about 13:10 AEDT by `date`)

Kit: `2026-10-22_B452_SEAT-G2_mps-b445-gate-tier1.md` (118 lines, stamp-slot grep reads 4 unstamped: 3 slots + last line; 0 person names).

## MEASURED (read verbs, 12:59-13:08)
- ls-remote: main `f5b6f5a7` (unmoved), b445 `aee0edd0`, b444 `3832abec`, b450 `e03fe7c7`; b446, b449, b451, b452 none. rev-list main...head = `0 3`. load1 7.01.
- 23 paths, web only (no `src/`, no `tests/`). `web/src/api/types.ts` NOT in the diff. B445 x B444 = 0 shared paths; B445 x B450 = 0 (B450 touches only `FeedbackTicketTests.cs`). `QuoteScreen.tsx` numstat 1/1.
- Supplies capability, BY CODE READ of the diff (not run):
  - Base: `PurchaseBomEditor` mounted `UsageRates` in every section of every purchase quote; it offers calculate-from-supplies (consumables, margins, pages per device, colour share, device quantity).
  - Head: `UsageRates` is mounted only when `onSectionRates` (= `clickRates.length > 0`, latched per editor session). A new quote, or any quote with no `clickRates` row, never sees it. `DealUsage.tsx` has four fields (mono click, colour click, ink rate, ink unit) and no supplies control; `setDealUsage` keeps a stored `usage.supplies` but nothing edits it.
  - Existing quote with a `clickRates` row: `UsageRates.tsx` is unchanged, so supplies stay editable.
  - Middle case: a stored quote with `clickRates` absent or `[]` loses the per-section block that base offered.
- Ruling check (RELAYED): B103 STATUS "NEEDS LANE A" says the deal tile carries `usage.supplies` (internal), replacing the per-section block for new quotes. D-06 = a keeps one deal-level calculation and book costs. C-17 is the accessory ruling and carries only the words default. I found no ruling that drops the supplies path, so the kit treats the loss as Major unless C3 finds one.
- Related leads the kit carries:
  - `infoHintWords.ts:60,66` still say "calculated from supplies" and now show on the deal panel.
  - `bom.spec.ts:311` asserts the supplies label is absent for a non-internal caller, which can no longer fail for a new quote.
  - The e2e spec and `b100` hint list lost the supplies path.
- `InfoHintPlacement.test.tsx` and `InventoryPickerMany.test.tsx` were edited, but THE WORK names no ruling for them. The kit makes the gate classify them.
- `draftModel.ts` has no `WORDS-PENDING` block, and its five format messages sit outside the 21 (the builder admits 26). The other five files carry the blocks.
- `addSection(` is called only from the editor in non-test web source.

## RELAYED
Builder counts (1106 to 1147, lost 0, 41 added), RED splits, mutant tables, the words pack, and the pushed-head claim all come from the builder STATUS. The Jira Done-when text comes from the STATUS Item 0.

## UNMEASURED
No Jira, `gh api`, PR or CI GET by the drafter (PR state unknown). No npm, vitest or dotnet run. No render, so the capability loss is a code read. `.env` and `AGENTMAIL_API_KEY` presence were not opened.

## Open questions for Tuesday
1. The kit leaves the PARTLY-DONE tokens to the gate (GO WITH FINDINGS for scope vs NO GO on a Major). Confirm that reading.
2. Should the five `draftModel` format messages count toward the pack (26)? The kit reports them as found-not-in-pack and rules nothing.
3. Whether the supplies loss is acceptable pending a W2 editor, or should block merge, is Tuesday's or the product owner's ruling. The kit asks the gate only to measure it and quote the rulings.

READ-WHOLE-BY-TUESDAY: ____
