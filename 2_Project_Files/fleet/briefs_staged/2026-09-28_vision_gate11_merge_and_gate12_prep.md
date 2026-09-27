# BLUF — `Datasec/Vision_Sales_Portal`: GATE 11 IS GO ON ALL FIVE. You are the MERGE AUTHOR. Phase 1: merge VSP-66, VSP-71, VSP-70, VSP-68, VSP-73 to portal main, one at a time, in that order. Phase 2: prepare the gate-12 branches (VSP-74, VSP-75, VSP-69) as listed, each ending READY FOR QA. No deploy, no production, nothing in Azure.

Verdict: QA/Vision-gate11, 07:54 AEST, report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/report.md` (read whole by Tuesday). Read its VERDICTS, FINDINGS INDEX and THE QUEUE before the first merge.

## PHASE 1 — THE RELEASE (five merges, this order, one at a time)
Main at this mail = `0d992e0` (ls-remote by Tuesday, 07:5x AEST). Heads at origin, read the same minute, EQUAL the gated heads:
1. VSP-66 `fix/vsp-66-checkout-link-death-2026-09-28` @ `1976275` (tier 1)
2. VSP-71 `fix/vsp-71-session-index-boot-2026-09-28` @ `5bdaeae` (tier 1)
3. VSP-70 `fix/vsp-70-restore-rollback-error-2026-09-28` @ `10ba4bb`
4. VSP-68 `fix/vsp-68-backup-missing-table-2026-09-28` @ `7ef698d`
5. VSP-73 `fix/vsp-73-backup-dump-replay-2026-09-28` @ `6d7ea73`
Per merge: re-read origin main; merge (fast-forward where possible, else a merge commit; never rebase a gated commit). `BACKLOG.md` conflicts: KEEP ALL BLOCKS in merge order (the gate measured BACKLOG as the only conflict). Then `npm test` and `test:db` as SETS against the gate's numbers (merged: unit 114, db 93, 0 names lost). Push, ls-remote, then the next. After all five, run the gate's "Cells to re-run on the merged head" list where you can locally. **CI is UNMEASURED** (Kam's gh login is still owed); say so in each MERGED line, and note the gate's warning: merged unit line coverage 80.79% against the 80% gate (local Node 26).
One MERGED mail per merge to tuesday-agent@: ticket, new main sha (ls-remote), parents, the two suite sets.

## PHASE 2 — GATE-12 PREP (after all five are on main)
Rulings by Tuesday (07:5x), each to be recorded on its Jira ticket by you:
1. **Forward-merge the new main into VSP-74, then into VSP-75 (it stacks on VSP-74), and into VSP-69.** Never rebase. Re-run each branch's own cells after.
2. **VSP-75: close the VSP-68 × VSP-75 semantic conflict on the VSP-75 branch.** The gate-12 drafter measured it at source: VSP-68's cell 1 expects total_rows 20 where 20 tables give 40, and the failure injector matches the table name UNQUOTED while VSP-75's SQL quotes it, so the injected failure never fires (cells 1, 3, 4 red). Fix it so the injected failure REALLY reaches the dump. Prove it with a mutant: a green that never reaches the dump is a fail.
3. **VSP-75 also takes VSP68-G11-F1 (Major):** an error with an EMPTY message is recorded as a dumped table with 0 rows and announced "DB Backup OK", including a whole database unreachable through a dual-address host. Fix shape (the gate's): record `err.message || err.code || err.name || 'unknown error'`, test for the error by presence, not truthiness; and a 0-row backup of a source that has rows is INCOMPLETE or FAILED. Red cell: a table dump rejecting with `new Error('')` is INCOMPLETE.
4. **VSP-75 also takes the `feedback` noise (gate 11 WRONG (n), ruled noise):** a table the app creates LAZILY (name each one from the code, with the line) and that does not exist yet is "absent, nothing to back up", not INCOMPLETE. Any other missing table stays INCOMPLETE. Cells for both.
5. **VSP-74: measure, then close, two holes the gate-12 drafter found reading the code (UNVERIFIED by Tuesday, verify first):** (a) deleting from `leads` cascades into meetings, email_log, reminders, monday_sync and lead_collateral_provided, and deleting from `quotes` cascades into quote_approvals and SET-NULLs quotes.lead_id, so a failed CHILD table can still be emptied or changed by a parent's delete; (b) a backup that lacks whole tables the database has is neither refused nor protected (every live backup today has only 10 tables). Kam's F-B ruling was "(3) both": the restore refuses an incomplete backup AND never empties a table it cannot restore. If either hole is real, it is inside that ruling. Red cells for each; if a hole is NOT real, say so with the measurement.
6. **VSP-69:** after the forward merge, re-run its five cells and its mutants (db.js changed under it with VSP-66).
Each branch then gets a READY FOR QA to tuesday-agent@ (new head, files touched, PRIOR WORK, NOT TESTED, tier: VSP-74 and VSP-75 tier 1, VSP-69 tier 1).

## TICKETS (file in Jira, BLUF-first, one ticket per fix one test pass proves)
- **VSP66-G11-F1 (Major, pre-existing):** after an in-flight pg_terminate_backend, a holder that releases in the same tick hands the DEAD client to the next caller; an innocent queued request answers 500. Fix shape + red cell in the report's FINDINGS INDEX. The VSP-66 READY's "the dead client is not reused" is false in this shape: say so on VSP-66.
- **VSP71-G11-P1 + P2 (Minor, one test pass):** the fixed LOGIN password 'vsp71' in session-index-boot.test.js:29; no cell pins WHEN OTHERS (the concurrent-boot pair reddens the narrow catch).
- **G11-M1:** a restore run by a role other than the app's boot role makes the next boot fail 42501 on `leads` (crash-loop). The VSP-71 READY's "a restore done as any role can no longer crash-loop" is false for that restore.
- **G11-O3 (Low):** a mixed-case sequence name makes backup-db 500 (pre-existing).

## ALSO
- **Your CLAUDE.md** says the QuickQuote sub-project never goes near Azure, but `hpas-quickquote` runs in Azure: Kam typed "Go ahead and publish the quick quote." on the live board at 2026-09-27 22:12:54 and v0.6.1 was published. Correct your own CLAUDE.md so the next seat is not confused, citing that line.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp65-production-deploy: "a — Log in to GitHub on the mini, then deploy after CI is read (recommended)" (live board 2026-09-28 06:57:40) -> already on VSP-65 (comment 38520). NOT to be deployed in this session: his gh login and his TYPED word come first.
- vision-prod-postgres-idle-transaction-timeout: "b — Set only idle_in_transaction_session_timeout to 10 minutes (recommended)" (06:57:51) -> already on VSP-67 (comment 38519). Production unchanged; it waits for his TYPED line (card vision-vsp67-second-consumer-attio-bridge). Not yours this session.
- vision-gh-login-for-ci: "a — Run the login when you are next at the mini" -> Kam's own hands; nothing to land.

## HOLDS
- No deploy, no production, no `az` write, no Partner Center. Portal main only for the five merges.
- PRIOR-WORK CHECK before rebuilding or removing anything; every READY carries PRIOR WORK.
- Local Postgres on 127.0.0.1:5433, your own databases only. Never delete; quarantine.
- The vault clone's divergence (ahead 14 / behind 550) is Kam's: do not touch it.

PROVENANCE:
- gate 11 verdicts, findings, merge list | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/report.md | read 2026-09-28 07:5x
- main 0d992e0 + five heads = gated; VSP-74 bf5bdc0, VSP-75 0d7a2fb | git ls-remote origin in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files | read 2026-09-28 07:5x
- VSP-68 x VSP-75 mechanism, VSP-74 cascade + missing-tables holes | the gate-12 drafter's WRONG AT SOURCE list (a subagent of Tuesday, read-only at source), relayed and UNVERIFIED by Tuesday | read 2026-09-28 07:1x
- QuickQuote publish word | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_msgs.sh 3 (source=live) row 2026-09-27T22:12:54 | read 2026-09-28 06:58
Self-check note: five merges in the gate's order; phase 2 rulings are Tuesday's inside Kam's F-B/F-A rulings; the drafter's holes are labelled unverified; no deploy anywhere.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 07:57
