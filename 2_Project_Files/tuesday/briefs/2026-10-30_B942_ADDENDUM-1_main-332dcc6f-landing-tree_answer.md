From Tuesday (the Datasec coordinator seat) to SEAT-G219, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B942. The answer to your last line ("accept the verdict above, or send a fresh seat to re-run the C2 builds and C5 on the main 332dcc6 merge?"). Tuesday read it read-only after 17:36 AEDT 2026-10-30 and touched nothing of yours.

**Answer: your verdict is accepted for the stylesheet property. Before it lands, ONE measurement is owed on the real landing tree, and it is yours, in this pane: the whole unit suite on the merge of main `332dcc6f` with head `df5d24fc`.**

Why the stylesheet half needs no rebuild (Tuesday's read-only measurement; repeat it if you doubt it):
- `gh api -X GET repos/datasecau/HPSM-POC/compare/7365165d...332dcc6f`: 17 product files under `web/src` (test and e2e files excluded) moved, with 359 added lines. GlobalNav.tsx is one of them.
- Tokenised on whitespace, quotes, braces and brackets, those 359 lines hold **0** of your 31 removed class candidates (28 distinct tokens checked: `m-3`, `m-5`, `size-9`, `bg-white`, `sm:p-3` and the rest of your C2 list). Control: the same tokenisation finds `min-h-11` and `px-3` in those lines.
- Structurally: the three `@source not` lines exclude test files and `web/e2e` only, and product files are still scanned. So a class that a moved product file uses still ships from the merge build. Main's move cannot make your C2 result false for a product class.

Why one run is still owed: `HpLogo.test.tsx` at your head renders `AppShell` (lines 29, 116, 135, 147 and 542), and `AppShell` renders `GlobalNav`, whose nav model changed on main (#249: two entries now built, "My readiness" and "Training & playbooks"). Your landing-tree unit run (merge2) was on `7365165d`. The `332dcc6f` merge bundle was withdrawn at 17:33, so the new rows of your test file have not been run against the moved nav.

What to do:
1. Run the whole unit suite (`vitest run`, the JSON reporter as in C5) once on your existing `wt-b942-merge3` tree (`c996c29c`, main `332dcc6f` plus head). Use your heavy gate and the load rule, as before. Then run `HpLogo.test.tsx` alone three times on the same tree. A red seen under load is re-run alone 3 times before it is called a failure.
2. Write the result into STATUS under C5 (files, passed, failed, skipped, with the frame "merge3 = main 332dcc6f + head").
3. If green: rewrite your FIRST line so the verdict names main `332dcc6f` and the merge3 unit figure, keep B942-1 as a Condition that is now measured, and end the FILE with your READY-style verdict line (GO WITH FINDINGS). If red: the verdict changes on the evidence, as your brief's rules say.
4. Do not re-run the C2 builds, the plants or the e2e suite. Do not fetch again (you already hold `332dcc6f`). If main moves again before you finish, write what moved and stop. Do not chase it.

New hard stop for this addendum only: **18:45 AEDT 2026-10-30.** The round (1 of 2), the class and every other line of B942 are unchanged. You still do not merge, push, comment or deploy. Landing is Tuesday's.
