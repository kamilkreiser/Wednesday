# Wave 18:00, 2026-11-15: common commission for four in-session kit drafters (Tuesday s279)

Tracked file, so the commission survives this seat's rotation. Each drafter gets this file plus its own
paragraph below. A drafter whose output files are absent at the next boot is RE-COMMISSIONED from this file.

## For every drafter
1. Read `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole, first. Its paths say
   `/Volumes/Laptop-DEV/`; on this machine every such path is `/Volumes/Datasec_DEV/` (same tree, renamed drive).
2. Copy the SHAPE of your template kit (named below) and read its drafter report for the method.
3. Write ONLY your kit and your report into `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/`, plus
   the `.measured` sidecar via `stamp_check.py --init` and your own scratch files under
   `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s279/d<B-number>/`.
4. `stamp_check.py <kit>` must exit 0 before you report STARTABLE. The report's LAST line is
   `DRAFTED B<n>: kit <lines> lines, sidecar rc <rc>, questions <n>`.
5. Kam's rulings today (live board, view=tuesday), verbatim:
   - 13:47 `mpscalc-170-fleet-line-id-name-1115`: "a — fleetLineId, screen unchanged"
   - 13:48 `nexusai-field-grant-holder-1115`: "a — Viewer keeps them"
   - 13:48 `mpscalc-rollforward-stop-words-1115`: "a — Approve the words as written"
   - 13:48 `datasec-morning-plan-1115`: "a — Noted, carry on"
   - 13:48 `hpsmpoc-168-industry-list-1115`: "a — Keep the ten-option customer list as built; make the snapshot
     placeholder field a four-choice list (Healthcare, Financial services, Public sector, Other)"
   - 17:16:37 (free text): "please action the reviewers feedback.   keep the 16 questions.  and yes, the
     stated-by-the-customer label does print in the exported report" (HPSM-POC; not this wave's subject)
   Read a card's full text only by `decision_queue.sh show <exact id>` into a scratch file (DRAFTER_RULES fence 1).
   In kit text the seat copies into commits/comments, cite a ruling as "the product owner's 2026-11-15 ruling".
6. Kam's standing words today: "keep going with the tickets" (Tuesday terminal, three times).
7. Open cards waiting on Kam (NOT ruled; nothing of theirs is built or recorded as ruled):
   `hpsmpoc-q1-partly-answer-1115`, `hpsmpoc-q5-covered-another-way-1115`, `mpscalc-99-laneMA-round-cap-1115`
   (MPS LaneMA, default 09:00 Mon: hold unmerged), `hpsmpoc-narrative-reedit-migration-1115`.
8. Live seats at commission (~18:00): `Datasec/MPS-M140` (B1578 MPSCALC-170 fleetLineId, Step 7 chain),
   `Datasec/HPSM-POC-H167` (B1584 lane P), `Datasec/HPSM-POC-H169` (B1586 lane R), `Datasec/HPSM-POC-R236`
   (B1583 HPSM records; may still be waiting to launch). In-session gates: B1577 G1 (HPSM), B1582 G2 (MPS
   MPSCALC-57 clause 3, branch b1582). Re-read `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` yourself.
9. Before you list any lane or ticket as actionable, grep the pickup
   (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md`) and today's note
   (`/Volumes/Datasec_DEV/TUESDAY/0_Brain/daily_tuesday/2026-11-15.md`) for its key and read every DROPPED/HELD line
   (ledger 2026-11-15 s278: a held lane was re-commissioned from a stale sweep).

## B1587 SEAT-N132 — NexusAI: rebuild b1568's counts against main 6335717d (template: `2026-11-15_B1579_SEAT-N131_nexusai-rebuild-202-counts.md` + its report; the landing files `2026-11-15_B1568_verify/{landing.txt,merge-subject.txt,merge-body.txt,VERDICT.md}`)
NexusAI main = `6335717d` (PR #202 landed 17:44 by merge commit, parents 0fdc77f0 + 17b7511d; Deploy demo skipped). Branch
`b1568/nexusai-f2-banner-above-overlay`, READY head `a63389b1` (built on base 4ba2e03c), gate B1568 G2 = GO WITH FINDINGS
(VERDICT.md: Major 1 = the counts conflict at current main, expected; Minors 2-4 go to the NexusAI records pass, not this
kit). The seat: ONE merge commit of origin main into the b1568 branch (the only allowed conflict is
`scripts/verify-expected-counts.json`; any other conflicted path = STOP), regenerate the counts with the project's own
`--update-counts` command on the merged tree (NEVER by hand), one counts commit, ONE plain fast-forward push (no force),
PROOF rows of B1579's form (the new head differs from a63389b1 only by main's changes plus the counts file, by program).
The expected pair is DERIVED by you from real runs or marked DERIVED; never typed as measured. Jest only through
`nexusai-lock.sh` with `NEXUSAI_LOCK_BASE` as B1579 used it. Say whether a gate round is owed or Tuesday's own PROOF
re-run suffices (B1579's rule). Then Tuesday re-runs the PROOF rows, reads hosted CI on the new head, opens or updates
the PR and lands by merge commit pinned to the new head. Nothing deployed; the demo hold stands.

## B1588 SEAT-R237 — NexusAI records (template: `2026-11-15_B1561_SEAT-R231_nexusai-records-200.md` + its report)
Record: the #201 landing (B1563 RD-932 audit; main 0fdc77f0; its gate's F1 = under a mounted router the refused-request
row logs the router-relative path, as STATE_MUTATION already does: FILE it as ONE ticket, words in the gate's VERDICT
`2026-11-15_B1563_verify/VERDICT.md`); the #202 landing (B1567 RD-576/590/826 test pins, counts rebuilt by B1579; main
6335717d); Kam's ruling `nexusai-field-grant-holder-1115` = "a — Viewer keeps them" (read the card by `show` for what
it rules) as a C-entry, after which Tuesday runs `decision_queue.sh --delivered`. The B1568 Minors are NOT in this kit
(b1568 has not landed). Move each RD ticket only per its own Done-when, read at source. NexusAI board and records form as
the template (find the project's records file and board by its CLAUDE.md, not from memory).

## B1589 SEAT-R238 — MPS records (template: `2026-11-15_B1574_SEAT-R233_mps-records-193-194.md` + its report)
Source: B1572's evidence (kit `2026-11-15_B1572_SEAT-M138_mps-lane-ma-slice2-evidence.md`; its STATUS and evidence
folder in the MPS project's Briefs, find by `ls`): 7 MET (302, 324, 325, 333, 338, 340, 341) and 2 PARTIAL (207 clause 3,
a missing literal; 331 clause 3, needs a ruling). Read EACH evidence file whole; a MET key moves to Done only if its own
Done-when is met at code main by program. 341's measurement-only point and 331 clause 3 need Kam's words: do NOT record
them as ruled; list the exact question for each in the report so Tuesday can card them. 207 clause 3: a ticket comment
naming the missing literal. B1573 (LaneMA round 2 of 2) is NO GO on a card waiting on Kam: NOT in this kit.

## B1590 SEAT-R239 — Security Composer records (template: `2026-11-15_B1576_SEAT-R235_composer-records-129.md` + its report)
Record: #130 landed (PCOMP-82 policy PDF cover date in the brand profile's Sydney day, W-b words; main b4681297, squash,
NOT deployed): a C-entry, and PCOMP-82 commented/moved per its own Done-when read at source; the gate's two Minors
(`2026-11-15_B1581_verify/VERDICT.md` F1 a released row cannot tell released_at from generated_at; F2 dateWordsInZone
accepts an undefined zone / non-ISO input) as tickets or backlog rows per the project's form; and a HELD mark on
PCOMP-75 (a comment saying it is held under the product owner's Guided hold, COMP-2 (a), `CLARIFICATIONS.md:1298`
"No Guided work until you turn it back on", so sweeps stop listing it). Composer deploys only on the product owner's
card: nothing here says deployed.
