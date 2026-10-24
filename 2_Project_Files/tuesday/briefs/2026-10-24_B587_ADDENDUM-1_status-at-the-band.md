From Tuesday, Datasec / Security Composer, to SEAT-J5 (brief B587). ADDENDUM-1, binding. It changes no scope.

**Why:** your statusline reads ctx 80% and your STATUS file's PROGRESS and RESUME section was last written at 17:05, before T2 and T3 were pushed. Tuesday read origin: `b587/composer-l3-structure` holds all six commits (T1, T2, T3, two each). If this session ends before STATUS is current, a fresh seat cannot continue from it.

**Do now, before any further check or heavy job:**
1. Rewrite `## PROGRESS and RESUME` in `1_Project_Definition/Briefs/2026-10-24_B587_STATUS.md`: per ticket T1, T2, T3, which of its checks (7a to 7j), mutants and pushes are done, partial or not started, with evidence paths; the step-8 checks state; the exact next commands; every scratch tree and mutant with its restore proof; ports, containers and images named `pc-b587-*` still running; the branch head by `ls-remote`.
2. Then finish the step you are in, if it fits; otherwise stop at a safe point (no mutant applied, no container left you would lose).
3. **Before 88% context:** if READY FOR QA is not yet reachable, stop every process and container of yours, restore every mutant, and end the FILE (not only your reply) with exactly: `STOPPED: NEEDS TUESDAY continue in a fresh seat from RESUME?`
4. Whatever you end with, the last line goes in the STATUS FILE. A line printed only in your reply is not seen.
