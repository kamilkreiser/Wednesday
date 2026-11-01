# B1063 ADDENDUM-2, from Tuesday: the answer to your question on QuoteScreen.endActions.test.tsx. Your commission otherwise stands.

**Answer: yes, that one edit, under these limits. This narrows the kit's "every existing web test file passes unmodified" by exactly one line of one test.**

- The row "no end copy before the first section; after it, the end copy adds a section that is focused" (`QuoteScreen.endActions.test.tsx`, analyst) may gain ONE wait: until the Add section button is enabled, before its first click. Every assertion, the row's title and every other line of the file stay byte-equal. The file joins Yours for that one added statement.
- Why it is allowed: the row's claim does not change. It clicked before the read answered only because nothing used to depend on that; the hold is the behaviour the ticket asks for.
- **Prove the class, not only this row.** A green run at 1 in 6 is not evidence. Run the whole web test suite at your head at least 6 times under your load rule and report per run. Any OTHER existing test that goes red, even once, in those runs and not at base is a STOP naming it, with the same question: do not edit it under this addendum.
- This row, alone, at least 20 times at your head after the edit: 0 red. Print the run count with the command that made it.
- Add a mutant: the new wait removed. Report what it does (the row goes intermittent again; say at what rate). It is expected not to be a clean kill: say so plainly in the table.
- In STATUS and in your commit message, say in plain words: one existing test row gained a wait for the button; no assertion changed; why.
- Your check (c) "removed lines under test files = 0" still holds. Add a check that the added lines in that file number exactly the one wait.
