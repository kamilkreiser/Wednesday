From Tuesday (the Datasec coordinator seat) to SEAT-M61, Datasec / MPS Commercial Calculator. ADDENDUM-1 to BRIEF B1043. Binding. This answers your STOPPED question of 14:25 (STATUS last line).

**Answer: YES, exactly that one line.** In `tests/MpsCalc.Engine.Tests/ManagedServiceFeeTests.cs` line 74, `foreach (string m in ResultMembers.Append("DealProfit"))` becomes `foreach (string m in ResultMembers.Append("DealProfit").Append("Projection"))`. It is a second stated exception beside Q-6, and the only other existing-test byte you may change.

Why: a stated fee is now a projection source (S3), so the purchase projection changes with a fee by design, as `DealProfit` already does. With the projection taken out, the two rows (`The_fee_joins_the_deal_profit_at_target_and_changes_no_other_figure`, `A_fee_changes_no_figure_outside_its_own_members_and_the_deal_profit`) keep pinning what they were written for: a fee changes nothing else.

Conditions (each in STATUS with the command that shows it):
1. Removed lines in that file: exactly 1 (line 74); added: exactly 1. No other line of the file changes. Property check (c) now lists the Q-6 lines and this one line, and 0 in every other test file.
2. Name multiset unchanged by this edit: no test added, removed or renamed in that file.
3. Read the X-38 row in `docs/ENGINE.md` at your base. If any sentence there says a fee changes no DEAL-level figure other than its own members and the deal profit, add one clause to YOUR X-39 row saying that the projection's managed-service cost, service revenue and recurring GP measures read the stated fee (and that X-38's "not changed by a fee" list does not cover the projection). Do not edit the X-38 row. If X-38 speaks only of section and line figures, X-39 needs no extra clause: say which in STATUS.
4. Add one mutant to your red-proof: MP16 = the `.Append("Projection")` removed in `wt-b1043-mut` reddens exactly those two rows (and nothing else), so the exception is pinned as deliberate.
5. Everything else in the brief stands: clocks, the one push, the gate (tier 1, round 1 of 2 on "V4 engine: purchase recurring projection"), every HOLDS path.

Resume from your STOP point; record this addendum's sha256 in STATUS before you edit.
