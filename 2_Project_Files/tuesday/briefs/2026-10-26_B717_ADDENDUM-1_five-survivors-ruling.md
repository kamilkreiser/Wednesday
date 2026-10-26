# B717 ADDENDUM-1 (from Tuesday, Datasec / MPS) - ANSWER to your STOPPED: NEEDS TUESDAY of 11:33:21

**Ruling: commit and push the 9 rows as they are. Do NOT add rows for the five survivors.**

Why: the product owner's 2026-10-26 08:45 ruling on this PR was, verbatim, "Add the 3 rows first, then a gate, then land". Your stamp capped extra rows at 0 for that reason. The five survivors you found are new, real test gaps of the same class, so they are recorded and ticketed, not built into this round.

What to do, in order:
1. Commit and push the 9 rows (E1-E3) exactly as your brief says (one fast-forward commit on the existing branch; no force, no rebase, no merge of main).
2. In your STATUS, add a section `## SURVIVORS FOUND (ticket candidate, not built)` listing all five, each with: the one-edit variant (as you wrote them: (i) group key `ModelSheet.Trim()`; (iv-a) joined key `.Trim()`; (v-a) `link.Normalize()`; (v-d1) `TrimEnd('\t')`; (v-d2) `Trim(' ')`), the input shape that kills it, the number of cases, and the file and line it touches. Say plainly that they survive all 51 rows at your head.
3. Then write your READY FOR QA line as your brief specifies, adding `| 5 known survivors listed for a ticket (not built, by the product owner's 3-row ruling)` before the PRIOR WORK clause.

Tuesday tells the round-2 gate these five are KNOWN and listed, so it grades them as recorded residue, and the records seat files the ticket. The round count and the gate are Tuesday's.
