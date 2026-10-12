From Friday (laptop seat), Datasec / MPS Commercial Calculator. ADDENDUM-1 to B69 (evidence only; your brief and holds are unchanged).

MPS main moved: PR #32 (B60 feedback pill + B70's test-only fix) merged at 08:2x → main **220956b19ab104d1df33e643e238167a286673f2** (Friday copied it from merge_when_green's output; commits API agrees). It touches no overlay file: B60/B65 are Feedback/** and web; B70 is FeedbackTicketTests.cs only. Branch `b69/…` from f4616886 is still fine; say in your STATUS whether you rebased or tested the merge onto 220956b1.

Main's own ci on 220956b1 (run 38310606551) failed ONE test, yours:
`H3_many_waiting_changes_all_answer_Busy_within_the_bound_and_a_read_meanwhile_is_fast(waiting: 16)` — "16/16 answered later than 2500 ms (max 2507 ms)" (OverlayResidueTests.B54.cs:522).
Log: `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B69-B70_ci-evidence/run_38310606551.log`.

Friday's observation (unmeasured, a hypothesis for you to test, not a ruling): EVERY one of 16 waiters late, the max only 7 ms over, reads like a fixed offset added to every wait (the bound counted from a later start, or one extra wait slice) rather than random runner slowness. Compare the 63/64 (max 2845) case. Your classification still decides it.
