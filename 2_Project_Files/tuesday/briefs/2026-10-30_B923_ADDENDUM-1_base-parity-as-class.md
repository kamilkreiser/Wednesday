From Tuesday (the Datasec coordinator seat) to SEAT-M59, Datasec / NexusAI. ADDENDUM-1 to BRIEF B923. Binding. Answers your STOPPED question in `Briefs/2026-10-30_B923_STATUS.md` (its last line).

**Answer: YES, parity of CLASS replaces text equality with base, with conditions. Continue with Steps 7 to 10.**

Reasoning: the product owner's ruling asks that "an unusual data-source response would give an error instead of the old answer" be fixed. Your measurement shows base itself answers a non-list roster read with an error message ("Sorry, I encountered an error analyzing the user activity. Please try again.", HTTP 200) because base's fallback lookup reads the window unguarded, so base's armed text is not an answer to match. The fixed head answering exactly as the same boot does when the read is a list (the skip-list path, the same state as a failed read) is the behaviour the guard was asked for. Base parity was the kit's proxy for "the old answer path"; the class is the property.

**Conditions (each printed in STATUS with a control that can fail):**
1. **The class, measured:** for every armed ask at the fixed head: HTTP 200; the body holds no `Error processing chat message`, no `is not a function`, and no `encountered an error`; and the answer equals the same boot's unarmed answer of the same question (F1, unchanged). Control: the same predicate on base's armed answers must FAIL on the `encountered an error` clause (it reads that text), and on the unmodified `802c0cfc` it must FAIL on HTTP 500.
2. **Base's armed answers recorded verbatim** in STATUS under TESTED (status, body text), with the sentence: "base answers a non-list roster read with an error message of its own; the fix answers it as a failed read". Do NOT assert base text equality anywhere in the test file.
3. **No test change for this:** Group F as written already asserts the same-boot equality; if any cell or comment in your added tests names base's text, remove that assertion only, and say so under Corrections.
4. **Corrections:** list the kit's base-parity sentence as superseded by this addendum, with the reason above.
5. **FOR TUESDAY:** state the base-vs-fix difference in one plain line so the re-check gate judges it (it is a behaviour difference on a defect-only path: base errors, the fix answers).

Nothing else in B923 changes: the one-line guard, the four cells, the mutants (NOOP, MU, MG), counts 5266/311, one commit, the push, the narrow differential items, the hard stop.
