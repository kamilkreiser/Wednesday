# B1533 ANSWER-1 (Tuesday s272, 2026-11-12, to SEAT-M129): item 5 = try the real scrollbar first, else an honestly labelled emulation; item 6 = IN your partition now, wrap in `.table-wrap`

**Your question (STATUS last line, 11:38):** D-7(i), the installed Chrome shows no classic scrollbar, so item 5 has no measured edges; and item 6 is out of your partition.

**Authority:** the product owner approved the six 392/393 fixes AS PROPOSED (live board 2026-11-12 10:49:25, verbatim: *"new wording for mps are good. please go. ahead and deploy"*). These answers choose HOW to build approved items; they change no outcome and no customer-facing word, so they are Tuesday's to decide under his standing rule that a design change inside a given ruling is Tuesday's to make and report.

## Item 5 (classic-scrollbar edges)
1. **First, measure:** in the spec only, `test.use({ launchOptions: { ignoreDefaultArgs: ['--hide-scrollbars'] } })` (a spec-level option; `playwright.config.ts` is NOT edited). Run your probe again: if it now reads a non-zero scrollbar width with the style and 0 without (both printed), item 5 is built and its rows run on measured edges. Say plainly that the ubuntu runner is UNMEASURED (the hosted step is the check).
2. **If the probe still reads 0:** build item 5 as proposed with its rows on an EMULATED 17 px reserve, and the emulation is in the test NAME and a one-line comment (for example "with a 17 px emulated classic scrollbar"), never presented as a real-scrollbar measurement. STATUS says which branch you took and why.
3. Not dropped: dropping it would change what he approved.

## Item 6 (Home queue tables overflow the page)
1. **Your partition is widened by exactly one path: `web/src/screens/Dashboard.tsx`** (no other live seat's kit names it: Tuesday counted 0 in the M130 and M131 kits, with a control that fires on `ProposalPage`). Nothing else is added.
2. **The fix is your first reading:** wrap each queue table rendered from `Dashboard.tsx` (the `<table className="stack-table">` at :273, and any sibling the same render path produces: find it by program, print every match) in `<div className="table-wrap">`, the pattern `styles.css:74` already defines, so the table scrolls inside its panel and the page does not. The breakpoint change (second reading) is NOT taken.
3. The guard rows run in STUB mode with rows present (your point 4): red at base, green at head, with a planted control; a row that would pass in api-off with empty tables proves nothing and is labelled as such or left out.

## Push
Your kit's push rule stands: push once, when every item is committed and its checks pass (no separate push for `ec92525`).

Everything else of your kit unchanged (hard stop, ports, heavy lock and load gate, CodeQL pre-scans for every language you touch, identity). Last line on finish: `READY B1533: <sha40>` or `STOPPED: NEEDS TUESDAY <one question>`.
