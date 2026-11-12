# B1533 ANSWER-2 (Tuesday s272, 2026-11-12, to SEAT-M129): YES, keep the five-tile rule at 601 to 714 px and push the two commits as they are (head a2f152b)

**Your question (STATUS last line, 13:38):** with a real 17 px scrollbar an Administrator is 2+2+1 at 698-714 px, so you built the five-tile rule as 601 to 714 px instead of 601 to 697. Push as is, or keep 697 and drop the 698/706/714 classic rows and the Administrator property?

**Answer: keep 601 to 714 px and push `a2f152b` (both commits) under your kit's push rule.** The product owner approved the 392/393 fixes as proposed (live board 2026-11-12 10:49:25, verbatim: *"new wording for mps are good. please go. ahead and deploy"*), and the outcome those fixes promise is D-7(iv): no lone tile, either scrollbar, 500-1500 px. D-6's "the pair stays" was a number written before anyone measured a classic scrollbar; your measurement shows that number breaks the approved outcome for the Administrator. Moving one edge by 17 px to keep the approved outcome is a design choice inside his ruling, which is Tuesday's to make and report (this answer is that decision; Tuesday reports it to him).

**Conditions:**
1. Say it in the commit body and the evidence `pr-body.txt` as a stated deviation with its measurement: *"the five-tile rule runs 601 to 714 px, not 601 to 697: with a classic 17 px scrollbar three 210 px tracks need 715 px of container, so 698 to 714 px would otherwise show a lone fifth tile"*, with the rows that prove it (698/706/714 classic) named.
2. Keep the 698/706/714 classic rows and the Administrator property rows; keep every red-first row and control as built.
3. Nothing else changes: if anything other than this one number differs from the rules as stated, STOP and ask.

Everything else of your kit and ANSWER-1 unchanged. Last line on finish: `READY B1533: <sha40>` or `STOPPED: NEEDS TUESDAY <one question>`.
