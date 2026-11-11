# B1502 ANSWER-1 (SEAT-M114): MPSCALC-130's per-page word-set row stays OUT; the clause stays open

From Tuesday (s269), 2026-11-11, answering your STATUS last line `STOPPED: NEEDS TUESDAY MPSCALC-130's per-page word sets cannot match the approved mock by CSS ...` (written 18:56). This file amends your kit; where they differ, this file wins.

**ANSWER: none of the three for this seat. Do not drop, rewrite or refresh anything. The word-set clause of MPSCALC-130 stays NOT MET and open.**

Why: the differences you printed are WORDING (a totals footnote the app has and the mock lacks; mock text the app lacks; the draft ribbon word; one page of the large book). Which side is right is a words question for the product owner, not a test-design choice: rewriting the row as "structural" would quietly turn "not equal to the approved mock" into "passes", and refreshing the mock changes an approved artefact. Tuesday takes the question to the product owner with your printed lists as the evidence.

**What you do now:**
1. Commit nothing more. The red word-set rows stay out of the branch, as they are now (your spec text is kept at `out/print-book-styles.WITH-WORDSETS.spec.ts.txt` and the evidence at `out/p10-wordset-red-after-reset.json`: write both sha256 in STATUS so the next seat can reuse them).
2. In STATUS, under a heading `ANSWER-1 (Tuesday)`: MPSCALC-130 style half MET (your rows), word-set half NOT MET and left open by the coordinator pending the product owner's words; the 15-vs-16-page note for the large book stands as a finding.
3. Re-read your branch ref by `gh api -X GET` once. If it still reads `b46322dd972bf7ed4ce36e46173675c4113a79b3`, replace the last line with exactly `READY B1502: b46322dd972bf7ed4ce36e46173675c4113a79b3`. If it reads anything else: `STOPPED: NEEDS TUESDAY <what you read>`.
4. Then stop. Your gate is a separate kit Tuesday commissions; your seven "seen outside my tickets" items and the PNG words question go to the records pass and the product owner from your FOR TUESDAY, unchanged.
