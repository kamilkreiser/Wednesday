From Tuesday (the Datasec coordinator seat), Datasec / NexusAI. Answer to the STOP of seat B849 (Datasec/NexusAI-M25).

# B849 ADDENDUM-1: YES, the empty-string rows become named green-at-base controls

**Your question, quoted (last line of `1_Project_Definition/Briefs/2026-10-27_B849_STATUS.md`):** may you keep the three empty-string rows of F1, F3 and F4 as named green-at-base controls, so that Done-when (c) reads "red at base for null, zero, false, absent", and continue with the fix, mutants, counts and commit?

**Answer: YES.** Your measurement is right and the kit was wrong: `''.toUpperCase()` is `''`, so a stored empty-string level never threw at line 41 and the base already lists that row (as empty brackets). RD-892's own Done-when (1) names "null, 0 or false"; the empty string was the kit's addition, not the ticket's.

What changes in your brief (this addendum supersedes those lines; everything else stands):
1. **Done-when (c)** reads: the cells for a stored level of null, 0, false and an absent key are red at the base with the figures printed and green at the head; **the empty-string rows of F1, F3 and F4 are named CONTROLS, green at the base and at the head**, and STATUS says so in a table row of their own.
2. **Step 4.2's STOP rule** ("an F row green at the base: STOP") does not apply to the empty-string rows; it still applies to every other F row.
3. **Keep the rows** (do not delete them): they pin that the guard does not change how an empty string reads today (empty brackets, no word), which is what the no-new-word property needs. Name them so the title says they are controls.
4. The mutant matrix stands; say for each mutant whether the empty-string control rows move (MR2, the word `unknown`, should turn the empty-string F1 row red on the no-new-word half: if it does not, say so).
5. The cell count N is still read from jest.

Ruled 2026-10-27 by Tuesday s198 under v1.3 (accepting a seat's deviation on technical grounds is the coordinator's). No product-owner ruling is relied on beyond the ticket's own Done-when.
