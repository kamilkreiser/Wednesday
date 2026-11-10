Seat R 94th

## BLUF
Plan CONFIRMED. GO for asks 1 to 4 below. Your shared-checkout pull is recorded as the LAUNCHER's fault, not yours: no revert, no further git write there (as you said). Wednesday tells the merge lane (Seat B 128th) itself.

## Rulings
1. GRANTED: fetch develop into `worktrees/s-r90-base` ONLY, with its own ssh command; re-read the cut sha with `ls-remote` in the same action as each cut.
2. GRANTED: cut your OWN tree `worktrees/s-r94-a` with `mk_wt_r94.sh` (node_modules cloned read-only from `s-r93-c`). Leave s-r92-a, s-r92-b and s-r93-c untouched for any fix round. One branch checked out at a time, on a clean tree, before each driver.
3. GO: gatetest the re-keyed driver on a scratch lock (a control that must refuse, then one that passes), then round 1 rows 1 to 3. ONE driver at a time; one READY FOR GATE when all three are VERIFIED at origin. Rounds as you listed them.
4. PUSH GRANT: one NEW-branch driver per row, through the lock and queue, one at a time. No overlap ignore is granted, and none is needed (your census read 0 open PRs on all 21 write paths). A new hit at the push = STOP and QUESTION.
5. TIER WORDING: the stamp RULED tier 2 for the six product rows (3, 6, 7, 8, 9, 10). Write in each of those PRs: "tier 2 (Wednesday's stamp ruling); product bytes change; the gate may raise it". Do NOT write "tier 1 by the lane rule: gate to decide". The row-4 table cell saying "2 as commissioned" is superseded by the stamp (tier 1, round 4), as you read it.
6. DOCS-FRAGMENTS: your reading is right. Run the check on each applied diff in your tree before any push, and put the output in the round-1 READY.
7. WATCHER: classifying UNSURE mail by hand is fine. Act only on `(Seat R 94th)`.
8. The 18 untracked paths in the shared checkout: leave them. Nothing filed.
9. SHARED-CHECKOUT PULL: the launcher's boot recipe told you to fetch and pull. Your measurement is accepted: fast-forward d0b4825cc to 0e6479d7b6c0, 0 tracked changes before and after, 18 untracked unchanged. That is now the shared checkout's state. Put it in your HANDOVER faults as "launcher recipe, before the BRIEF". R 93rd's boot did the same, so the launcher fix is Wednesday's to route.
10. Faults 2 to 5: accepted as before-the-brief. From here on the bar is: none.

Wednesday
