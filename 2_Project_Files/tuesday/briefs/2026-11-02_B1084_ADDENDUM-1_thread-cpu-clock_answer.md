# B1084 ADDENDUM-1, from Tuesday: the answer to your STOP on the row's clock. Your commission otherwise stands. Stay in this seat; no fresh seat is needed.

**Answer: option (b). Switch this one row's clock to thread CPU time, the 1000 bound unchanged, as `s47-crf2-linear-detector.test.ts` does (PR #81). This is the coordinator's decision, not the product owner's ruling on row #428: say so in STATUS and leave row #428 reading not ruled.**

Why, so you can test it: your 10 cells at main and 10 at the edit show that a wall-clock median under this hog measures the host's contention as well as the engine; a timeout cannot fix that; and this package already decided the same question this way, with the bound kept. Your scratch run is 10 of 10 green. It is a scratch run: it proves nothing about the committed file until the steps below run.

**What the change costs, and it must be written down, not hidden:** the row's title says "in under 1 s", and after this change the median it checks is CPU time on the row's thread, not elapsed time. A real slowdown that is only waiting on a CPU no longer turns it red; that is the point, and it is also what the row stops seeing. Say it in one plain sentence in the comment above the row, in the commit message, and in STATUS. The title stays byte-equal.

**Limits:**
- Still one path, `packages/engine/test/performance.test.ts`, test only. The bound stays 1000. The timeout stays your derived 60,000 (the row's wall time is what the timeout guards; re-derive it if a new worst row duration exceeds a quarter of it, and say so).
- Use the same fallback shape as crf2 (`process.threadCpuUsage()`, falling back to `process.cpuUsage()`); read its lines 44-70 again and name any difference in STATUS. A helper in this one file; no shared helper.
- **Red proofs are now the whole question.** P1 and P2 must still go red by the row's assertion under the new clock. A plant that burns no CPU cannot be seen by this clock, so P1 must burn CPU; if your plant does not, resize it under PROPERTY 2 once and say so. **Add P4, which the kit lacks: a plant that only waits (an awaited sleep on the measured path), which the row must now leave GREEN.** State it as the proof of what the row no longer sees. If P4 goes red, the clock is not what you think: STOP.
- Re-run from the top of your Step 6 on the new file: quiet 3, hog 10 with 0 red by any message, the row alone, the shuffle seed, Steps 7 to 10 as written. Any red in the hog 10 is a STOP with the table, not a third design and not a bound change.
- Your edit in `.tools/wt-b1084-fix` stays; build on it. Nothing is rerun at main.
- **The thin margin stays a finding, in FOR TUESDAY:** your scratch max is 822.2 ms, within 20 percent of the bound. Report the new table's max beside it.
- The READY line says "wall clock replaced by thread CPU time on this row, bound unchanged, by the coordinator's decision".

**Unmeasured by me:** I read your STATUS and the kit, not your tables or the crf2 file. The 3 red cells' cause is still unmeasured, and this answer does not claim they were host contention.

Hard stop and target are unchanged (target READY 05:39, hard stop 07:09, your Step-0 clocks). The gate after you stays tier 2, round 1 of 2 on your kit's new counter; I will tell the gate this reading is open to challenge.
