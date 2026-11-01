# B1093 ADDENDUM-1, from Tuesday: the answer to your STOP on F-1. Your commission otherwise stands. Stay in this seat.

**Answer: yes. Edit `tests/MpsCalc.Api.Tests/EntraAuthTests.cs` inside commit 1: the two pins 37 to 43, the six template rows in `ApiOperations()`, and the pin comments extended in the file's own form. Nothing else in that file.**

Why, so you can test it:
- Read by Tuesday in your `wt-b1093-fix`: both pins are `Assert.Equal(37, ...)` at lines 70 and 118, and their comments record earlier lanes extending them the same way.
- This is the test doing its job: it forces every new operation onto the auth list. The six rows therefore put your operations UNDER that check, so they must assert what the file's other rows assert. If any new operation cannot pass that file's auth checks as written, that is a finding: STOP, do not weaken a row or a helper.
- The exception is this file and these edits only. It is not a standing widening of HOLDS.

**The main move.** The kit's rule reads STOP on a HOLDS file in a move. Your treatment is accepted for this one move: `19d084fa` is MPS #140, which I landed; your 4-path list from `compare` has 0 overlap with your paths. No rebase. Re-pin before the push as your steps say, and any further move goes through the rule as written.

Say in your READY line and FOR TUESDAY: this file was added to your path list by this addendum, the merged tree with `19d084fa` was not built by you unless your steps do so, and clause 4 and clause 5 of the Done-when stand as you wrote them.
