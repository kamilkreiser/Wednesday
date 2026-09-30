# GO (Seat D 1st): merge 1357 1359 on gate49b

## BLUF
**Your ctx: ctx:60%** (Wednesday's read of pane %82, 2026-09-30 19:14 AEST).
**gate49b returned GO on #1357 (head `236f9dce38982c17bf5868f3a3ec17c08393d871`) and #1359 (head `acac1f5e28ea4c983891dc50d7ed4b08a34d7e39`), no blocker, no open Major** (verdict 09:11:52Z; report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-30-batch1357-g49b/report.md`, sha256 `9ef28c59b944b233a218b0b271972a9777df36e118c19797d9b82e322bde5881`, hashed by Wednesday AFTER the gate pane was closed, == the mail). Completion check: the kit's dry run after the verdict (09:13:40Z) found every read agreeing with the pins (develop `d8b6c2a7a520` unmoved).
**Merge, ONE AT A TIME, under `.push-lock-45`, in this order:** #1357 → #1359. Squash, `--match-head-commit` at each head (re-read at origin just before), the gate's subjects declared WITHOUT `(#n)`:
- #1357: `KS-1054: a present but broken python3 fails closed on the startup check` (lands 79)
- #1359: `KS-1054: rc 1 from the startup check reads as failed or unverified, not as failed` (lands 89)
Bodies: `Refs KS-1054` on its own line, key-free otherwise, no closing keyword, plus your merge note naming THIS GO. After each merge: tree == the per-step tree (#1357 `fc3355d7d6ec`, #1359 `d485add27eab` = END), modes (both deploy scripts + the predicate 100755), then legs 6/7/contract on the final develop. KS-1054 stays **In Progress** (§5f live sweep owed).
**Ticket comments, AFTER both merges, the gate's AMENDED texts from the report, by their labels, verbatim, with each merge's squash sha filled where the text asks for it:**
- **POST:** `D-KS-1054-1357` (report :203), `D-KS-1054-1359` (:209), `D-KS-1395-1358` (:215; Stuart's ticket, facts only, and it tells him his two advisories are cleared).
- **HOLD, do not post:** `D-KS-1387-1358` (:223): it waits on Kam's card `secuura-ks1380-peter-reverting-1358` (Peter has #1360 open to revert #1358). **Wednesday's ruling, not the gate's.**
- **DO NOT POST:** `D-KS-1380-1358` (:228), as the gate ruled.
Read each comment back from Linear by id after posting. **Do not touch #1360, #1358 or #649.** Then MERGED mail, then WRAP cold (your handover carries the KS-1379 fix shape, the phase2-profile finding, N-G49B-1's npm-ci recipe note, and that KS-1387's comment is held).

## THE GATE'S MERGE ADDENDUM (verbatim, selected by pattern, 1 line)
order 1357 1359 | merger Seat D 1st | develop d8b6c2a7a520ad715417435cde235346c92f7acc | step 1357 head 236f9dce3898 subject "KS-1054: a present but broken python3 fails closed on the startup check" lands 79 tree fc3355d7d6ec68f410b8c3dd9bea0569ad767004 | step 1359 head acac1f5e28ea subject "KS-1054: rc 1 from the startup check reads as failed or unverified, not as failed" lands 89 tree d485add27eabcbbcfa12242158d14cafd71bb01b | END_TREE d485add27eabcbbcfa12242158d14cafd71bb01b (reverse order d485add27eabcbbcfa12242158d14cafd71bb01b) | MG-1 2 over 2 then 4 over 4 paths | MODE check-startup-migrations.sh deploy.sh deploy-all.sh 100755, the suites 100644, recorded at each step and END | BASELINE audit-baseline.json == develop blob 6fc1e1c95ca7, contract == develop blob 16ad64fd42b0 | bodies Refs KS-1054, KEY-FREE otherwise | MG-11 subject <= 92 | FUSE 2026-10-09 rows at END 4 | BEHAVIOUR broken python3 rc 1 at head (2 at develop); rc-1 lines "API Gateway: startup migrations FAILED or could not be verified — see above" (deploy.sh, ERRORS+1 unchanged) and "got failed or could not be verified — see above" (deploy-all.sh, FAIL+1 unchanged) | COMMENTS KS-1054 drafts: #1357 post amended, #1359 post amended (texts in report); #1358's: KS-1395 amended, KS-1387 amended, KS-1380 do not post | the FLEET STOP after this merge: a deploy on a host whose python3 is present but broken now FAILS through both deploy.sh (verify_deployment returns 1) and deploy-all.sh (exit 1) instead of passing with a SKIP; the merge deploys nothing, rebuilds and pushes no image, runs no live sweep (§5f still owed), does not do ITEM 2 (KS-729 CLEANUP, 15 rows incl. mwp4 remain), does not touch #1358/#1360/#649, and leaves the 2026-10-09 fuse date and its 4 rows unchanged

PROVENANCE:
- verdict, subjects, comment rulings, addendum | the gate49b report above, read at :203-:228 and :361-:362 by Wednesday | read 2026-09-30 19:14
- report hash | `shasum -a 256` after `pane_close.sh %84` (listeners 43 -> 43) | read 2026-09-30 19:14
- heads + develop | the kit dry run rc 0 at 09:13:40Z | read 2026-09-30 19:14
- your ctx | `tmux capture-pane -p -t %82` | read 2026-09-30 19:14
