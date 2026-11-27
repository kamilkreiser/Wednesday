This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-26_coagent_POLICY-B_brief.md`. Seat POLICY-B only. It answers your STOP Q9. Report under "## ADDENDUM 8 (answer Q9)" in your STATUS file.

If your context was compacted while you waited: re-read your brief, addenda 1 to 8 and your STATUS file WHOLE before doing anything.

# POLICY-B ADDENDUM 8: Q9. Your option (i): the by-name tail rule is removed from the comparer, on four conditions. Control (a) of addendum 7 is WITHDRAWN BY NAME.

Friday read your "ADDENDUM 7 (answer Q8)" section whole (STATUS lines 465 to 478). Nothing in it was re-run by Friday, and Friday has still not read either comparer file. Every figure below is yours.

The stop was right, and it found a fault in the coordinator's own addendum: control (a) of A-3 asked for a refusal that the tail rule alone explains, without first asking whether such a refusal can exist. By your search and your eight added rows it cannot: after hunk 1 the rule lives only under a relative working folder, and there the engine asks. **Control (a) of addendum 7 A-3 is withdrawn; it is not to be met in any other form.**

## The ruling

A rule of the comparer that decides no cell on either corpus, and reports a miss where the engine's answer is (by your reading) right, measures nothing and can only cry wolf. It goes. What it was meant to see is then OUTSIDE the oracle, and that is said in plain words, not left silent.

**R-1. Remove the by-name tail rule from the corrected comparer** (a third file; `cmp_r2.py` and `cmp_r2_next.py` are both kept as they are, each with its sha256; record the new file's sha256 and quote the removed lines).

**R-2. Show the removal changes nothing on the real corpora, by program:** for seed 1 AND seed 2, every count of the comparison with the tail rule (your `cmp_r2_next.py`, narrowed) equals the count without it, both comparisons each (`5cab5e4` to HEAD, `cd7b6fd` to HEAD). You stated 0 tail-alone cells for seed 1; seed 2 is unmeasured: measure it. **If any count differs on either seed: `STOP Q10`**, with the differing cells listed. That would mean the rule did decide something, and the coordinator rules again.

**R-3. Re-run controls (b) and (c) of addendum 7 on the FINAL comparer** (it changed again, so their earlier firing does not carry over). Both must fire, first report lines quoted. Either silent: `STOP Q10`.

**R-4. The eight relative-folder rows are measured in the two earlier trees.** Run your `ctl_a_rows.jsonl` through the harness in the `5cab5e4` tree and the `cd7b6fd` tree (short runs; the heavy rule applies if one is over five minutes) and print the three answers per cell. Expected by the coordinator, unmeasured: the same answer in all three trees. **If the head is LOOSER than either earlier tree on any cell: `STOP Q10`** (that would be a product difference, not a comparer matter). If it is equal or stricter: record it.

**R-5. The limit, written down.** In your STATUS, under its own heading "What the differential's oracle does not cover", one paragraph in your words from your measurements: a name that is reached only through a RELATIVE working folder is not judged by the oracle's MISSED count; on such rows the engine's answers in the three trees are the ones R-4 printed; LOOSER and UNATTRIBUTED still compare those rows between trees. This paragraph is for the second check, which will be told to attack exactly this with its own comparer. Nothing about it goes into the repository in this round.

**R-6. Then A-4 of addendum 7** with the final comparer: both seeds, both comparisons each, PASS with MISSED 0, LOOSER 0, UNATTRIBUTED 0; `OLD-GAP` printed per comparison; every plant still reported with its first report quoted. A plant no longer reported: `STOP Q10`.

**R-7. No further change to the comparer by you after this.** A further fault in any of its rules is a stop.

Everything else of addenda 5, 6 and 7 stands. After R-6: the red script and clippy as planned, one heavy run at a time, then your last line `READY FOR QA POLICY-B r2` with the head SHA above it.
