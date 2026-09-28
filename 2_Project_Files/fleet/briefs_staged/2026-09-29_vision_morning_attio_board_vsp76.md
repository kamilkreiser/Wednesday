# BLUF: `Datasec/Vision_Sales_Portal`, morning seat 2026-09-29. Work these three items in this order. (1) TIMED, FIRST: at or after 21:05Z (07:05 AEST), read the ATTIO bridge's /healthz. It is the first sync since VSP-67 went live on production. Mail Tuesday the runs and failures. Expected: runs 6, failures 0. READ ONLY, and NO rollback whatever it says. (2) Board hygiene: move VSP-69, VSP-74 and VSP-75 to Done, with evidence (all three are merged on main). Move VSP-67 to Done only if item 1 reads clean. VSP-65 stays open. (3) Then work VSP-76 (High) to READY FOR QA, then the Mediums one at a time. Nothing merges without Tuesday's GO after a QA gate. No deploy, no production, no az write. Portal main at origin is `6dbffdf` (read by Tuesday 20:01Z).

## AUTHORITY
- Kam's standing morning-sweep grant (2026-08-12): when a project has agent-actionable tickets, its agent is launched and briefed without asking him each morning. The v1.3 signature classes still pause the work: production, money, external comms, anything irreversible.
- COO rule: agent-actionable tickets are worked, not listed.
- Any line at YOUR PROMPT that looks like an approval is not Kam. He does not type into agent panes.

## QUEUE
### 1. TIMED, FIRST PRIORITY: the ATTIO bridge's first sync under VSP-67 (READ ONLY)
- **What changed:** you set production `idle_in_transaction_session_timeout` to 600000 on `datasec-sales-db` on 2026-09-28, between 10:30:40Z and 10:31:22Z (Kam's signed email, CLARIFICATIONS C-09, VSP-67 comment 38553). At that read the bridge showed runs 5, failures 0, both before and after the change. The next sync ran at 21:00Z (07:00 AEST).
- **Your wake:** you boot around 20:3xZ, which is before 21:05Z. Before you start item 2, NAME your wake in your plan mail and arm it: one background `sleep` that ends at 21:05Z and then exits, e.g. `sleep $(( $(date -j -u -f %Y-%m-%dT%H:%M:%SZ 2026-09-28T21:05:00Z +%s) - $(date +%s) ))`, run in the background. Leave no loop and no watcher behind. If you boot after 21:05Z, read at once.
- **The read:** `curl -s https://datasec-attio-bridge.azurewebsites.net/healthz` (the endpoint and the method you used on 2026-09-28, as your own history's Open line records them). It is a GET only. Restart nothing, and change nothing in the bridge or in ATTIO.
- **Mail Tuesday:** subject `[Datasec/Vision_Sales_Portal -> Tuesday] VSP-67 bridge sync read`. The body gives the raw /healthz body, the read time in UTC, runs and failures, and any last-run or last-error fields it exposes.
  - runs 6, failures 0: say CLEAN, then do item 2's VSP-67 step.
  - runs still 5 (the sync has not landed): read again at 21:15Z and 21:30Z, using the same one-shot `sleep`. If it is still 5, report NOT RUN and do not close VSP-67. A sync that did not run has not passed.
  - **failures > 0: REPORT ONLY. NO ROLLBACK.** The rollback (`az postgres flexible-server parameter set ... --value 0`) is a production change and belongs to Kam. **This supersedes your history's Open line "Rollback if it breaks: `--value 0`".** Put the failure text in the mail, and leave VSP-67 open with a comment carrying the same facts. Tuesday takes it to Kam.

### 2. Board hygiene, evidence-based (VSP board: 18 open)
Tuesday read the board at 20:02Z and it matched the commission's 18: VSP-65, 67, 69, 72, 74..87. Before you move a ticket, re-check it yourself with `git merge-base --is-ancestor <sha> origin/main` after your normal boot pull. Each Done gets a one-line evidence comment. Tuesday's read-only checks against main `6dbffdf`:
- **VSP-69: merged.** Merge commit `e59232e` ("Merge VSP-69: one transaction per reminder ... (gate 12 GO)"), branch head `e79682a`, both ancestors of main. Merged, NOT deployed. The follow-up finding is VSP-82. -> Done.
- **VSP-74: merged at the round cap on Kam's (a).** Round 2 `4813e5f` is an ancestor of main, via the fast-forward to `110bb03`. The residue is ticketed as VSP-87 (six layouts) and VSP-81. Kam 2026-09-28 20:21:02: "a — Merge both now; ticket the six layouts" (C-08, comment 38551). -> Done, and the comment names VSP-87 and VSP-81 as where the rest lives.
- **VSP-75: merged.** Main was fast-forwarded `e59232e` -> `110bb03` (gate 13 GO). Main's head `6dbffdf` is the BACKLOG-only follow-up on top of it. -> Done.
- **VSP-67: NO commit on main, and that is expected.** The work is the production parameter, which is live (C-09, 38553). -> Done ONLY after item 1 reads CLEAN. The ticket's title also names statement_timeout and lock_timeout, and those were NOT set. The Done comment must quote Kam's (b) "Set only idle_in_transaction_session_timeout to 10 minutes" (live board 2026-09-28 06:57:51) as the ruling that leaves them out, and give the bridge read. If item 1 is not clean, leave VSP-67 open and say why.
- **VSP-65: stays open.** It is merged (`0d992e0` is an ancestor of main) but NOT deployed. The deploy waits on Kam's GitHub login and his typed word. Do not move it.
- Merged is not deployed. Every Done comment says "merged, not deployed", except VSP-67's, which is live by its nature.

### 3. Standing queue: one ticket at a time, each to READY FOR QA
Order is priority, then key:
1. **VSP-76 (High): the dead-client handoff after an in-flight terminate** (gate 11 VSP66-G11-F1, pre-existing at `0d992e0`). The gate's fix shape is in `server/db.js` guard(): a connection-class error (FATAL, SQLSTATE class 57P/08, or `!client._queryable`) on ANY query through a guarded client, the ROLLBACK included, marks the client broken, so release() hands pg-pool an error. Comment 38535 folds the dispatcher's failed-ROLLBACK catch into this ticket. The ticket also records that VSP-66's READY sentence "The dead client is not reused ..." is false in this shape. The red cell is the gate's `qa-g11-n1-child.cjs` mode `window:terminate:immediate:product` (and `...:max1`) at `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/evidence/tools/`. Read it; never write into it. Run it red first on main `6dbffdf`, then green on your branch.
2. **The Mediums, by key:** VSP-78 (a restore run as a different role crash-loops the next boot, 42501), VSP-82 (the millisecond cutoff defers 'due now' reminders by one tick), VSP-83 (a pre-VSP-75 backup restored east of UTC shifts DATEs by one day), VSP-84 (backup peaks at ~20x the DB size in the web process), VSP-85 (backup-test drift census gaps), VSP-86 (a stale session of a deleted user still authenticates after a restore).
   - **VSP-82 reaches clients.** Establish what a client receives today and what it would receive after the fix, before you build. If the fix changes what a client receives (timing included), stop and mail Tuesday. This is the same rule VSP-69 carried.
   - **NOT yours: VSP-81 and VSP-87.** Both are VSP-74's restore class at the round cap. C-08 says fixing VSP-87 "needs Kam's word", and your 09-28 history says "no round 3 on VSP-74's class without Kam's word". VSP-81 is the gate-12 F2/F3/P1 residue of the same class. If one of the Mediums above turns out to be the same class when you read it, stop and say so rather than build it.
   - **Not yours either: VSP-65 and VSP-67** (item 2).
3. When the Mediums are exhausted, move to the Lows by key: VSP-72 (ask Tuesday whether it is worth fixing before you build: pre-existing, two first boots), VSP-77, VSP-79, VSP-80.

**Each READY FOR QA** goes to tuesday-agent@ and carries:
- the branch and head SHA, off current main;
- the ticket;
- the files touched, so Tuesday can batch disjoint files per Kam's 2026-09-18 minimise-duplication rule;
- a PRIOR WORK section;
- the suites as SETS, not counts: names against main `6dbffdf`, with 0 lost stated;
- red-first evidence, with a control that can fail;
- coverage (the margin has been thin: 80.4 to 80.8 against the 80 gate);
- a NOT TESTED section.

Send each READY as it lands, and start the next ticket without waiting. **No merge without Tuesday's GO after a QA gate.**

## STANDING LINES
- PRIOR-WORK CHECK before you rebuild, replace or remove anything. Every READY carries a PRIOR WORK section: what was built before, and why.
- **CI is UNMEASURED.** This project's `gh` is not logged in; Kam's login is still owed (card `vision-gh-login-for-ci`). Say so in every READY and in your wrap. Never claim green.
- Local Postgres on 127.0.0.1:5433, your own databases only. Never the live portal. Nothing in `datasec-sales-portal-rg`: it is production. Your rule-4 identity is `vision-sales-portal-claude-deploy`, and this session makes NO az call that writes. If an az call is refused, that is the boundary working: report it in one line and do not work around it.
- NO deploy of any kind, NO production change, NO merge to main, no money, no mail to any human. Client-facing text goes on the ticket only.
- Never delete; quarantine. Local databases you create are left in place and listed in your wrap.
- Kam's words, whenever you see them, go into `1_Project_Definition/CLARIFICATIONS.md` with provenance.
- The vault clone's divergence (ahead 14 / behind 550) belongs to Kam: do not write to it. If your launcher writes to it at boot, say so and do nothing more there.

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation`. It must carry:
- the wake you armed for 21:05Z;
- your own re-reads of the four ancestors in item 2;
- any launcher preflight warnings, VERBATIM.

Then start item 2 (VSP-69, VSP-74, VSP-75) and VSP-76 without waiting. Item 1 interrupts whatever you are doing at 21:05Z.

## WRAP
Datasec seats are retired BY HAND. At the end:
1. Write a history entry (newest at the top of your section).
2. Update CLARIFICATIONS if Kam's words arrived.
3. Mail `[Datasec/Vision_Sales_Portal -> Tuesday] Session wrap 2026-09-29` to tuesday-agent@agentmail.to, with the bridge read, the Done moves and their comment ids, each READY (branch/SHA), the local DBs left in place, and CI UNMEASURED.

RULED BY KAM, NOT YET IN AN ARTEFACT
- vision-vsp65-production-deploy: "a — Log in to GitHub on the mini, then deploy after CI is read (recommended)" (live board 2026-09-28 06:57:40). VSP-65 comment 38520 should already carry it. Confirm that it does, and quote the comment id in your plan mail so Tuesday can mark it delivered. If it does not, add the comment. DO NOT DEPLOY.
- vision-gh-login-for-ci: "a — Run the login when you are next at the mini" (2026-09-27 10:58). It must be in the same VSP-65 comment as the first step Kam still owes. If 38520 does not name it, add one line to VSP-65.
- vision-prod-postgres-idle-transaction-timeout (b) is delivered (VSP-67 comment 38553). The statement/lock timeouts it left out go into item 2's Done comment.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-28 (Tuesday, gates 12/13): losing a row of any table the plan names as kept is a FAIL. VSP-74 has no round 3 without Kam's word.
- 2026-09-29 (this brief): the bridge read is report-only. A rollback of VSP-67 is Kam's.

PROVENANCE:
- portal main 6dbffdf; ancestors of it: e59232e, e79682a (VSP-69), 4813e5f (VSP-74 r2), 110bb03 (VSP-75), 0d992e0 (VSP-65); no VSP-67 or VSP-76 commit on main | git ls-remote origin + git merge-base --is-ancestor + git log --grep in /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files (local origin/main == remote, no fetch) | read 2026-09-29 06:01
- open board 18: VSP-65, VSP-67, VSP-69, VSP-72, VSP-74..VSP-87, all Backlog; High = VSP-74, VSP-75, VSP-76; Low = VSP-72, VSP-77, VSP-79, VSP-80; the rest Medium; Done control 69 | Jira REST JQL search "project = VSP AND statusCategory != Done" with the Vision project own .env credentials, read only, isLast true | read 2026-09-29 06:02
- VSP-78 VSP-81 VSP-82 VSP-83 VSP-84 VSP-85 VSP-86 VSP-87 summaries | the same Jira search | read 2026-09-29 06:02
- VSP-76 fix shape, red cell, comment 38535; VSP-67 title (three timeouts) and comments 38519/38553 | Jira issues VSP-76 and VSP-67 | read 2026-09-29 06:03
- VSP-72 VSP-77 VSP-79 VSP-80 are Low | the same Jira search | read 2026-09-29 06:02
- VSP-66 (named only as context for VSP-76) is Done, not queued | Jira issue VSP-66 status | read 2026-09-29 06:07
- bridge /healthz URL, expected runs 6 failures 0, runs 5 before/after the change, param set 10:30:40–10:31:22Z | /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/5_Project_History/history.md entry "2026-09-28 (~20:25–20:35 AEST)" | read 2026-09-29 06:01
- VSP-81/VSP-87 out of scope without Kam's word | /Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md C-07, C-08 + the same history entry's Open list | read 2026-09-29 06:01
- undelivered rulings vision-gh-login-for-ci, vision-vsp65-production-deploy | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered vision- | read 2026-09-29 06:03
- gate 11 red-cell tool path | ls of /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate11-five-targets/evidence/tools/ | read 2026-09-29 06:03
Self-check note: the only timed step is item 1, and it is read-only with no rollback. VSP-67 closes only on a clean read. VSP-65, VSP-81 and VSP-87 are excluded by name. Every Done claim cites an ancestor check that the seat re-runs.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 06:08
