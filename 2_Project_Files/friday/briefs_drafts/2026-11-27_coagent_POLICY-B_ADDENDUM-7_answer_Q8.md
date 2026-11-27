This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-26_coagent_POLICY-B_brief.md`. Seat POLICY-B only. It answers your STOP Q8. Report under "## ADDENDUM 7 (answer Q8)" in your STATUS file.

If your context was compacted while you waited: re-read your brief, addenda 1 to 7 and your STATUS file WHOLE before doing anything.

# POLICY-B ADDENDUM 7: Q8. Yes, the comparer may be corrected once more, on three conditions that make the corrected comparer prove it can still report a miss.

Friday read your STATUS lines 395 to 463 whole (ADDENDUM 6, the commits, section 6 (a), (b), (e), (g), the seed 1 runs and Q8). Nothing in it was re-run by Friday, and Friday has NOT read `cmp_r2.py` or `cmp_r2_next.py`: this answer rests on your description of the two rules. Every figure below is yours.

The stop was right. A rule of the comparer that has been wrong twice is the instrument, not the engine, and a comparer corrected until it passes is a check that cannot fail. So the correction is allowed only together with proof that it still fires.

## The answer

**A-1. The by-name tail rule (297 cells): your hunk 1 is allowed** (the tail rule applies only where the joined path is not absolute), as the ONE re-check of this rule. Do not drop the tail rule entirely: that is unmeasured, and it removes a way to see a miss.

**A-2. The folding rule (77 cells): your hunk 2 is allowed in a NARROWER form, not as written.** A candidate that holds a zero-width or other ignorable character is taken out of MISSED only when, for that cell, the head's answer equals the answer of `cd7b6fd` AND the answer of `5cab5e4`. Such cells are not dropped: they are printed as their own count, named `OLD-GAP (ignorable character)`, with the three answers. A cell of that kind where the head differs from either earlier tree stays in MISSED. Reason, the coordinator's: the documents of commit 1 say such a name is not a piece and is not checked, as at the base; that makes it a known, old gap, and a known gap is counted, not hidden. By your own line 455 the answers are equal on every one of the 374 cells: so the expected count is 77, YOUR figure, unmeasured under the narrower rule. If it is not 77: say what it is and why; that alone is not a stop.

**A-3. Before any re-compare result counts, three must-fire controls of the corrected comparer (Python only, on COPIES of the outputs already made; the originals are not edited):**
- (a) *The tail rule still fires where it applies.* Take one cell whose refusal the tail rule alone explains (a relative or empty working folder). In a copy of the head's output change that one answer to a not-refused answer. The corrected comparer must report it MISSED.
- (b) *Hunk 1 did not remove the joined-path case.* Take one cell with an ABSOLUTE working folder where a bare or relative word, joined to that folder, lies inside a rooted pattern (the shape `<ws>` + `secret/plan.txt` against `<ws>/secret/**`), refused at the head. In a copy change that one answer to not-refused. The corrected comparer must report it MISSED. If the 16,342 rows hold no such cell: say so with the search you ran, then add one such row through your harness in the head tree (one short run; the heavy rule applies if it is over five minutes) and use it.
- (c) *The narrowing of A-2 holds.* Take one of the 77 cells. In a copy change the HEAD's answer only, to any other answer than the one it has. The corrected comparer must NOT count that cell as OLD-GAP: it reports it as MISSED, as LOOSER or as an unattributed difference (say which, and why that is the right one for the answer you planted).
Quote each control's first report line. **If any of the three does not fire: `STOP Q9`, with the comparer left as it is.**

**A-4. Then re-compare** both seeds and every plant with the corrected comparer (Python only, the outputs already made). Required: the two real comparisons PASS with MISSED 0, LOOSER 0, UNATTRIBUTED 0, every other count equal to the committed comparer's (say so by program); every plant still reported, its first report quoted; the `OLD-GAP` count printed for each comparison. A plant that is no longer reported is `STOP Q9`.

**A-5. Records.** The committed comparer's results stay in STATUS as run (the FAIL on 374, with the two causes). Both comparer files are kept; the corrected one's sha256 is recorded with the two hunks quoted. A further fault found in EITHER rule after this is `STOP Q<n>` with no further correction by you.

**A-6. The two points you raised that are not part of the stop.** (a) Five commits, not four: accepted, for the reason you give (no amending). (b) Commit 3's two new tests pass at `cd7b6fd` by design, and their reds are the by-hand mutant reds: accepted as you state it; the second check will be told to look at exactly this.

Nothing else of addenda 5 and 6 changes. After A-4: the red script and clippy as planned, one heavy run at a time, then your last line `READY FOR QA POLICY-B r2` with the head SHA above it. Your wake is your own running chain; Friday's is your STATUS file's last line.
