# BLUF — `Datasec/Vision_Sales_Portal`: a SHORT fix round on the gate-12 branches BEFORE the gate runs (not a gate round). Two defects found at source by Tuesday's gate-12 drafter in VSP-74/VSP-75, plus three small items. Each fix ends in a fresh READY FOR QA for the branch it changes. No merge to main, no deploy, no Azure.

Heads now (ls-remote by the drafter 08:38 AEST): main `609e967`, VSP-74 `f62917f`, VSP-75 `69157de` (stacks on VSP-74), VSP-69 `e79682a`. Your predecessor's READYs: `TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp{74,75,69}-r2-READY-mail.txt`; its wrap mail is in your inbox (22:37Z).

## FIX 1 — the "lacking" group keeps EMPTY live tables (VSP-74's restorePlan, as merged into VSP-75)
Reported at source (UNVERIFIED by Tuesday; measure it first): restorePlan skips tables with no live rows for its "failed dumps" and "outside RESTORE_ORDER" groups, but NOT for "tables the backup lacks". So every existing 10-table backup is refused on the VSP-75 tree even into an empty database, and with --allow-incomplete the closure then keeps users, leads and partner_orgs, so they are never restored.
Ruling: make the lacking group consistent with the other two: a lacking table whose live copy is EMPTY cannot lose anything to a clear and is not kept. A lacking table WITH rows stays refused by default (that part is correct: clearing its parents would cascade into it).
Cells, red-first: (i) a 10-table backup into a database where the other 10 tables are empty restores all 10 of its tables completely, no flag; (ii) the same backup where `quotes` has rows is refused by default and, with the flag, keeps quotes and its FK parents (say in the READY exactly which tables an old backup therefore cannot restore once quotes exist — Tuesday tells Kam at deploy time).
Apply on VSP-74 first (it is VSP-74's function), then merge VSP-74 forward into VSP-75. Never rebase.

## FIX 2 — `test/db/backup-lazy-absent.test.js` hard-codes the shared database `salesportal_test_lazy`
Lines 17-18 and 30-31 (the drafter's read). It ignores `TEST_DATABASE_URL`, so any test run, including the gate's, writes into your database. Make it derive its database from `TEST_DATABASE_URL` (for example that name plus a `_lazy` suffix), created if missing, never dropped. Prove it: with `TEST_DATABASE_URL` pointed at a fresh name, `salesportal_test_lazy` is not touched.

## ALSO
3. **Ticket** the dispatcher's catch that releases a client after a FAILED ROLLBACK with no error (the VSP-70 / VSP-76 class): add it to VSP-76 if one test pass proves both, else its own ticket; say which.
4. **Jira status** of the five merged tickets (VSP-66, 71, 70, 68, 73): move to Done with one comment each: "merged to portal main (sha), NOT deployed; the deploy is tracked on VSP-65 and is Kam's."
5. **The F1 clause narrowed (record on VSP-75):** "a 0-row backup of a source that has rows is INCOMPLETE or FAILED" is satisfied by all-tables-failed = FAILED. A clean dump of a genuinely empty database is correctly OK; pointing at the wrong database is out of scope. No code for this.
6. Your predecessor's unanswered QUESTION (~22:10Z, where VSP-80's BACKLOG line lands): its safe route (a ticket, main untouched) stands. The BACKLOG line rides the next non-gate commit to main.

## READY FOR QA
One per changed branch (VSP-74, VSP-75), with new head, files, PRIOR WORK, NOT TESTED, tier 1, the suite sets vs main 609e967 and local coverage. VSP-69 needs no new READY unless something changes it. Then WRAP.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp65-production-deploy: "a — Log in to GitHub on the mini, then deploy after CI is read (recommended)" -> on VSP-65 (comment 38520). Not yours: no deploy.
- vision-prod-postgres-idle-transaction-timeout: "b — Set only idle_in_transaction_session_timeout to 10 minutes (recommended)" -> on VSP-67 (38519). Waits for his typed line. Not yours.
- vision-gh-login-for-ci: "a — Run the login when you are next at the mini" -> Kam's hands.

## HOLDS
No deploy, no production, no az write, no merge to main. Local Postgres 127.0.0.1:5433, own databases only. PRIOR-WORK CHECK. Never delete; quarantine. The vault clone is Kam's.

PROVENANCE:
- FIX 1 and FIX 2 defects | Tuesday's gate-12 refresh drafter (a read-only subagent), WRONG AT SOURCE items 1 and 3, relayed and UNVERIFIED by Tuesday | read 2026-09-28 08:4x
- heads | the drafter's git ls-remote origin at 08:38:45 AEST, relayed | read 2026-09-28 08:4x
- predecessor wrap (tickets VSP-76..80, open items) | its wrap mail 22:37Z, DKIM pass | read 2026-09-28 08:4x
Self-check note: two pre-gate fixes on VSP-74/75 only; no merge; Kam's cards are not this seat's.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 08:55
