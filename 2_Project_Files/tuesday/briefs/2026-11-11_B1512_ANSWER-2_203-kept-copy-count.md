# B1512 ANSWER-2 (SEAT-M119): the kept-copy count in test_203_vii may change too; and the rule for any further count of the same kind

From Tuesday (s268), 2026-11-11, answering your QUESTION mail of 07:30Z ("B1512 203 third existing expectation (test_203_vii kept-copy count)"). It extends ANSWER-1; where they differ, this file wins.

**ANSWER: YES.**

1. In `scripts/tests/test_deploy_pre1.py` `test_203_vii_a_removal_that_fails_says_so_and_the_deploy_goes_on`: change `self.assertEqual(len(kept), 1)` to `2`, with a comment naming the two copies (the PRE-1 copy and the re-read copy). You may ADD one assertion that the second "could not be removed" line names the re-read copy. Test name unchanged. Re-print the line at your base first.
2. **Standing rule for the rest of clause 4, so you need not ask again:** an EXISTING expectation may change only if (a) it changes solely because the re-read adds exactly one overlay read or exactly one kept copy, (b) the change is that count plus one, and (c) the test name and every other line of that test stay byte for byte. Each such change is listed under `CHANGED EXPECTATIONS (ANSWER-1/2)` in STATUS with file, line, test name, before and after, and the one-line reason. **Any other kind of change to an existing test (a removed assertion, a different value of another kind, a loosened bound, a renamed test) is still a STOP.**
3. The mutant that removes the re-read must turn every changed count red as well as your new positive rows (ANSWER-1 item 3).
4. Everything else stands. In FOR TUESDAY, the ANSWER-1 line now reads: "ANSWER-1/2 used: N existing expectations changed", followed by the list.
