From Tuesday (the Datasec coordinator seat) to SEAT-G229, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B962. Binding. Sent before you meet the move, so that you do not stop on it.

**Main moved while you run: PR #254 landed at 09:18:12Z (GitHub mergedAt), and main is now `7e5d652ecdfb521b3dfcbb15f4babcb49d341c35`** (parent `7c353747`). It changed 4 files, all under `web/src/components/partner/`: `RevenueResults.tsx`, `OneCustomerEstimate.tsx`, `RevenueCalculator.tsx` and the new `Revenue.restyle.test.tsx`.

**Ruling: a NAMED move, not a STOP,** although your kit's main-moved list says `partner/**` other than `ActionPlanScreen*`. That clause exists to catch a change the Home renders, and the Home renders none of these files. Tuesday measured this read-only: `PartnerDashboard.tsx` and `home-next-actions.ts` at your head `5de03bca` hold 0 lines naming `RevenueResults`, `RevenueCalculator` or `OneCustomerEstimate` (`/usr/bin/grep -c -i`; control: the same file holds 29 import lines). Repeat that read yourself and print it.

What you do:
1. Keep judging the comb you built on `7c353747`. Do NOT use your one re-fetch for this move.
2. At C8, name this move: the commit, the 4 files, and the import check above.
3. If you have the re-fetch left AND load allows at the end, you MAY rebuild comb on `7e5d652e` and re-run the unit suite once. Otherwise mark it NOT RUN with this reason. That alone does not make your verdict conditional.
4. Any FURTHER move of main that touches a path on your stop-list other than these four files still follows your kit.

Everything else in B962 stands: round 2 of 2 = THE CAP, findings only, no merge, push, comment, Jira write, deploy or message.
