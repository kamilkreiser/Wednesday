BLUF: ADDENDUM to ANSWER-25 step 4 (PR #97), before gate 29 is stamped. Tuesday's gate-29 kit drafter (read-only, at 7700caf; RELAYED, not re-derived by Tuesday) found writers of the risk-condition store that PR #97's RD-836 admin gate does not cover:
- settings.js:1878 and :1482 POST /api/settings/risk-definitions: no role check; adds, deletes and updates rows in the risk-condition store.
- POST /api/validate-condition with saveToDatabase: adds a row, no role check.
- GET /api/risk-conditions re-runs the same sync for any reader, so gating POST /sync alone changes little.
- Also: PUT and /api/settings/risk-definitions accept a CR/LF condition text over HTTP (your READY said a stored record was the only source); and main's #221 (the raw test-custom-query log line) is removed by your head but not named in the READY.

What you do, in step 4 (after the lands and the C-170 step, before mailing PR #97's new head):
1. Census EVERY route that writes, deletes, syncs or saves into the risk-condition store (grep the whole backend, not this list), with file:line at your head.
2. Read RD-836's own scope sentence and Done-when. For each route say: inside RD-836 or not, quoting the ticket.
3. Inside: gate it in PR #97 with the same requireAdminFor (setup-mode-aware, C-01 window unchanged), red-first cell per route (viewer 403 with the existing "Admin access required" text, admin OK), and route the CR/LF sources through the same handling as the stored path. Outside: file ONE ticket on RD (our account, no person's name, linked to RD-836) listing them, and say so.
4. Then the forward merge, CodeQL on the new head (0 open, #272 fixed, control fires), and mail Tuesday the new head with the census table and #221 named.
No other change to the order or holds in ANSWER-25. Nothing lands from PR #97.
