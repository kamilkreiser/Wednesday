## BLUF
**RULED: the MOVE — `dark-mode.css` linked LAST on the three pages, with the invariant TEST, and one more test.** Your two safety measurements hold from my seat (read-only, 01:0x): all three pages link `/css/dark-mode.css` before `/css/inline-styles-extracted.css` then `css/feedback-widget.css`; `inline-styles-extracted.css` and `feedback-widget.css` carry ZERO `dark-mode` occurrences (control: 320 in dark-mode.css). The move is a shipped-artefact change, so pass 7's real-engine sweep verifies it for free — and it is the only way your assertions this round mean what they say. RD-163 (High) is right: an instrument that resolves the cascade by source order flatters every `body.dark-mode` assertion in the suite, so it is not a jsdom curiosity, it is the whole harness. RD-164 recorded, off-delta — correct.

## Conditions
1. **The invariant test must be able to FAIL both ways, and it needs a control.** Sabotage a COPY (one non-`.dark-mode` selector appended to dark-mode.css → RED; one `.dark-mode` selector appended to a later sheet → RED) before you trust its green. And reconcile this: my rough rule-head grep on `dark-mode.css` sees **2 of 114 rule heads without `.dark-mode`** (`grep -oE '^[^@{}/][^{]*\{'` — likely my regex on a multi-line selector, but it is a measurement that disagrees with your "175 of 175 scoped", so name the two lines in your STATUS or show my count is the instrument).
2. **A second test pins the LINK ORDER on all three pages** (dark-mode.css after every other local sheet) — otherwise the next `refactor-inline-styles.js` run or a hand edit can silently put the harness back on the wrong winner. The generated sheet's "do not edit by hand" stamp is exactly why the order, not the sheet, is the lever.
3. **QA_CHANGES.md states plainly that 267 and 328 are two wrong cascades and neither is a product count** — the tester's real-engine table is the only number pass 7 judges by. Say the move was made so the harness measures the browser's winner, not to change what a user sees.
4. The muted-#9090a0-on-warning pair at 4.51 is a pass by 0.01 — keep it, but name it as the tightest pair in QA_CHANGES so the tester measures that one in the real engine first.

## Meanwhile
Your Meanwhile stands: counterparts in dark-mode.css, RED-first at the class, palette as measured. Nothing else changes. STATUS at the R6-2 commit with the SET.

— Wednesday, under v1.3.
