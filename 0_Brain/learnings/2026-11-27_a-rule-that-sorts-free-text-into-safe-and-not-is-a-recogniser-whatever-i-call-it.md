---
date: 2026-11-27
type: correction
source: "Three WED-170 build lanes (wake pack, brain index, NAS backup) each failed two independent checks in one afternoon on a clause Wednesday had commissioned; a fourth clause of the same kind was caught by the build seat in the evening. Checker verdicts under 0_Brain/reference/2026-11-27_qa-wake-r3/, 2026-11-27_qa-braindb-r3/, _qa-nasbackup-r2/ and 2_Project_Files/qa-checks/wake-r4/."
status: live
tier: M
supersedes: ""
---

# A rule that sorts free text into "safe" and "not" is a recogniser, whatever I call it: filter, exception, name list, shape fix

**The lesson:** When a safety property (nothing dropped, nothing leaked, nothing lost) is made to depend on code that reads free text and decides which items the rule applies to, that code is a recogniser and it cannot be finished. Commission the conservative rule instead: carry the whole thing, qualify or stay out, unproven means failed. This is the 2026-11-17 lesson with its handle widened; that lesson did not fire today because I had filed it under "safe shell commands".

**Context (four cases, one day, all Wednesday's own clauses).**

1. **Wake pack, "drop the dead grant rows".** Three answers in a row asked the seat for a better filter of dead rows in the grants register (a lexical signal plus a word list). The second checker built 38 hostile live rows; the filter dropped 30, a restriction among them. Cure, ruled by Kam on a card: the filter is deleted and the register is carried whole, byte for byte. The third check passed.
2. **Brain index, "fix each leaking shape".** ANSWER-3 asked for shape-by-shape fixes to keep another seat's or client's text out of the index. The second checker's 58 new must-be-absent shapes: 28 entered. Cure, ruled by Kam: qualify or stay out (one exact index row, one clean tier line, no marker), with the fence parsing deleted.
3. **NAS backup, "a file gone from the source is fine".** Wednesday's ANSWER-3 accepted an exception to the copy check without a test of it. Cure, ruled by Kam: one rule, unproven means failed; the exception withdrawn by name.
4. **Brain index again, "leave out a lesson that names the other client".** Written by Wednesday into the very brief that quoted the 11-17 lesson. A word list: it left out 57 lessons where the brief said 5, 55 of them this seat's own, cost two of the ten test answers, and still missed project names. The build seat measured it and asked; the name test was removed (ANSWER-7).

**Diagnosis (why the 11-17 lesson did not fire).** Its headline and its index rule say "safe shell commands" and "interpreter as a security boundary". None of today's four looked like a shell: they looked like a tidy-up filter, a list of fixes, a reasonable exception and a privacy rule. The retrieval handle named the costume, not the mechanism. The mechanism is: a guarantee that holds only if code correctly classifies open-ended text.

**How to apply.**

1. **Before a brief or answer leaves me, read each clause and ask: does a guarantee here depend on code deciding which free-text items count?** Words that mark it: filter, skip, except when, unless it looks like, leave out those that mention, recognise, detect, fix each shape. If yes, rewrite the clause as the conservative rule and state the cost (bytes carried, lessons left out, runs failed) as a number for Kam, not as a reason to classify.
2. **A check's NO GO that lists new shapes is the signal to remove the mechanism, at the FIRST such verdict, not the second.** Asking for the listed shapes to be fixed is the patch the lesson forbids.
3. **An exception to a hard rule is a recogniser of the exempt case.** It ships only with a test that plants the non-exempt look-alike and shows it refused; otherwise it is withdrawn.
4. **Convenience may still classify, as long as nothing is guaranteed by it.** Name-shape rules are best effort and are said to be so (the severity ruling given to the NAS checker: hard guarantees are Blockers on any input, name-shape rules best effort).
5. **Credit where it was caught:** the build seat that measured clause 4 against the brief's own figure and asked, and the fresh checkers. A seat that questions my clause is the system working.

**Related:** [[2026-11-17_a-recogniser-of-safe-shell-commands-cannot-be-finished]], [[2026-08-07_a-check-that-cannot-fail]], [[2026-09-05_qa-gate-tiers-and-the-two-nogo-cap]], [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]
