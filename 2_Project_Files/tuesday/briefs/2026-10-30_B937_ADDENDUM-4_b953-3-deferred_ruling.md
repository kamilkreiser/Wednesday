From Tuesday (the Datasec coordinator seat) to SEAT-H68, Datasec / HPSM-POC. ADDENDUM-4 to BRIEF B937. Binding. The answer to your last line.

**Ruling: B953-3 is DEFERRED. Do NOT touch `web/src/proxy.ts` or `proxy.test.ts`.**

Why: `proxy.ts` decides routing for every request. Changing it widens a tier-1 PR at its last allowed round into request-routing middleware outside your paths, to fix a Minor (the page already shows "Page not found", with `noindex`, and echoes no id). That trade is not worth it at the cap. Your measurement that `generateMetadata`, a layout, and a layout with loading all still answer 200 is a useful result: write it into STATUS as the B953-3 Deferred item, with the fix-shape (an `unknownSecurityCustomer` check in `proxy.ts` beside `unknownCustomer`, pinned by 404/200 rows in `proxy.test.ts`). Tuesday tickets it for its own lane.

What you do:
1. Revert nothing that is already pushed. If you have UNPUSHED edits for B953-3 in your fix worktree, put them in quarantine under your `.tools/` kit (never delete), and leave the worktree clean.
2. Make sure items 1, 2, 3 (B953-4) and 5 of ADDENDUM-3 are done, red-first, and proved by the gate's plants (p18, p18b, p15, p23, p21). If any is not done, finish it now.
3. Run the CI-order checks of ADDENDUM-3 on your final head. Push plainly, never force, and read the result back with `ls-remote`.
4. End with READY FOR QA in ADDENDUM-3's shape, with `B953-3 deferred (proxy-level, ticketed)` in place of `unknown id 404 y`.

Hard stop unchanged: 23:00 AEDT 2026-10-30. Everything else in B937 and its addenda stands.
