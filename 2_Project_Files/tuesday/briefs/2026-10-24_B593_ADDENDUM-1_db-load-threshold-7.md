From Tuesday (the product owner's Datasec coordinator seat), Datasec / Security Composer. ADDENDUM-1 to B593 (SEAT-G84). Written 19:44 AEDT 2026-10-24. Changes ONE line of your LOAD section; everything else in B593 stands.

**SUPERSEDES** the LOAD clause "below 6 for anything that starts a database stack". **New rule: a database-stack job starts when `uptime` load1 is below 7 at two reads 4 s apart** (the fleet's own launch line), the same as before in every other respect: one heavy job at a time behind your own lock, record the reading beside the result, poll 20 s while at or above 7.

Why: your STATUS (19:27) shows 1 of 72 mutants run, the queue held by the load gate since 19:05 with load1 6-12 from other projects' jobs. At 6 the gate cannot finish before its hard stop. This is Tuesday's decision, not yours to widen further.

Guard that stays binding: if a database test goes red ONLY under load (green when re-run alone at load1 below 6), it is a load artefact, not a finding: re-run it once alone and record both runs. Report in STATUS under Corrections that the threshold was changed by this ADDENDUM-1, with its time.
