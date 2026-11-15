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

## WAVE 19:15 (added by s279). Kam's rulings since 18:00 (live board, view=tuesday, verbatim):
- 18:29:53 `mpscalc-331-clause3-location-1115`: "a — Accept as built, narrow the ticket and close it" (repeated 19:15:21)
- 19:15:16 `mpscalc-341-measurement-move-1115`: "a — Move 341 now, and other measurement-only tickets the same way"
- (HPSM, not this wave: 18:29:59 narrative migration a; 18:30:07 q5 a; 18:30:12 q1 a.)

### B1591 SEAT-R240 — MPS records (template: `2026-11-15_B1589_SEAT-R238_mps-records-b1572-evidence.md` + its report, and B1574 for a landing record)
Record: (1) MPS PR #195 LANDED 18:42 (squash 56578ac6, one parent 3a69065a, tree = head 73b33ffa; MPSCALC-57 clause 3: the four PDF-text specs read the PDF from a temp file and run in CI's stub-off step with a poppler apt step; gate `2026-11-15_B1582_verify/VERDICT.md` GO WITH FINDINGS, its Minors as BACKLOG rows; NOT deployed): a C-entry, MPSCALC-57 comment, moved only per its own Done-when (clauses 1, 2, 4, 5 of comment 40621 are not this landing's: read them); (2) Kam's 331 ruling: a C-entry quoting it, a comment on MPSCALC-331 narrowing clause 3 to the accepted locations (TERM_GAP at the first remaining software row, CPP_INCONSISTENT at the device row, as B1589's comment 41233 records), then move 331 to Done; (3) Kam's 341 ruling: a C-entry quoting it as a STANDING RULE for MPS (a ticket that is only a measurement, with no merged change, moves to Done once an independent run has measured it), a comment on MPSCALC-341, move it to Done; and list (do not move) any OTHER open MPSCALC ticket the new rule could apply to, for Tuesday. Root records main is now bd98ce32 (B1589's land). After READY Tuesday runs `--delivered` for both cards. MPSCALC-333 and -207 are NOT in this kit.

## WAVE 19:40 (added by s279). Kam, Tuesday terminal ~19:25, verbatim: "keep going with the tickets". Source of the lanes: `tuesday/briefs/2026-11-15_SWEEP-1925_datasec-actionable-lanes.md` (read YOUR lane's section whole and its "questions for Tuesday"; re-measure every claim; the sweep's lane disjointness is by named path only: prove it against the live branch compares in your PRIOR WORK). Live/in-review branches to partition against: HPSM b1584 (lane P), b1585 (lane N), b1586 (lane R, gate), b1577 (PR #320); MPS b1578 (PR #196, held until B1591 READY; it edits docs/API.md); NexusAI b1568 (PR #203). NexusAI jest runs only through the shared lock (`nexusai-lock.sh`, `NEXUSAI_LOCK_BASE=.../session-tools/locks-laptop-1017`), one waiter each. Nothing deployed by any of these.

### B1592 SEAT-N133 — NexusAI lane NX-S1: backend/server.js security, RD-988 first (template: `2026-11-15_B1563_SEAT-N128_*` or the newest NexusAI security build kit you can find by `ls briefs | grep -i nexusai`; model row C3 Opus for an auth/permission surface; gate G1). Scope: RD-988 (a viewer can still re-triage a feedback item: the route PR #200 missed) and whichever of RD-888, 926, 830, 711 share its file region without making the kit large; the CodeQL set is a LATER kit unless trivially in the same lines. Say what you left for the next slice.

### B1593 SEAT-M142 — MPS lane M-O: package and SDK guard (template: `2026-11-15_B1582_SEAT-M141_mps-lane-mw1-pdf-text-specs-in-ci.md` for the MPS shape; model by row). Keys MPSCALC-224, 349, 397, 398 as the sweep lists them (note 349 is a measurement-only candidate under Kam's 19:15 standing rule: if its Done-when is only a measurement, say so and keep it out of the build). The correct csproj path is `src/MpsCalc.Api/MpsCalc.Api.csproj`.

### B1594 SEAT-M143 — MPS lane M-W2: the ruled screens MPSCALC-229, 128, 150 (template: as B1593). Read each ticket's ruling at source (CLARIFICATIONS + Jira); any user-facing word not already ruled = NEEDS-WORD, excluded and listed for a card.

### B1595 SEAT-N134 — NexusAI lane NX-F1: first-run, login and settings (template: the newest NexusAI web build kit; model by row; gate by row). Keys RD-456, 492, 475/560, 189, 117/188, 481, 808 as the sweep lists them; keep it to what one seat can finish in ~4 h, ranked by the sweep's order, and list the rest for the next slice. RD-475/560 (SRI hash) is security-shaped: G1.

### B1596 SEAT-M144 — MPS LaneMA round-3 fix (MPSCALC-99), Kam 19:43:43 verbatim: "Decision mpscalc-99-laneMA-round-cap-1115: a — Allow one small fix seat and a third review round on the hand-off row only (recommended)" (template: `2026-11-15_B1573_SEAT-M139_mps-ma-round2-pool-determinism.md` + its report). Source of the fix: the round-2 verdict `tuesday/briefs/2026-11-15_B1573_verify/VERDICT.md` (read whole): F1 stands but moved to the hand-off row, `LaneMAPollAndHandOffTests.cs:122` pin, SourceStoreUnavailableException at :150 when the third steps pass their 2 s bound; 7/60 red interleaved at load ~19 vs 1/60 on the old head; its named fix: remove the :122 pin, optionally release at ~1.2 s, re-measure 60 interleaved runs at load 17-25, m2 3/3. Branch b1564/mps-lane-ma-source-wait-pins (head 29b1bea2 at round 2): read it at origin; ONE fix commit on top, plain push, no PR. SCOPE: the hand-off row ONLY (its test and, if the verdict names it, the one product timing line); F2/F3 closed, not reopened. Then Tuesday commissions round 3 of the gate on the hand-off row only (this is the LAST round: a NO GO leaves MPSCALC-99 open and unmerged). Main moved since (56578ac6, maybe #196): merge main into the branch only if the kit's template shape says so; state the plan. Nothing deployed.

### B1597 SEAT-H170 — HPSM-POC lane Q: the question set (F1, F4, F5/F6, F7) as ONE new content version on top of 0.7.1 / 0.1.3 (template: `2026-11-15_B1577_SEAT-H166_hpsmpoc-168-industry-choice.md` + its report and the B1577 gate's findings; plan `tuesday/briefs/2026-11-15_hpsm-reviewer-feedback-check/ACTION-PLAN.md` lane Q, read whole). b1577 LANDED as HPSM main f4e79a7a (#320). Tickets: HPSMPOC-485 (F1), -487 (F4), -488 (F5+F6 reorder), -489 (F7 Q11/Q12 words). Kam's words, verbatim: 18:30:12 "a — Approve as written (Q1 only, scored 50)" (F1: the answer 'Partly: some printers can, others cannot', Q-CS-01 only, still raises the trusted-start-up finding); 18:30:07 "a — Approve the words; it counts as covered (score 100, no finding, so it does not appear in the PDF)" (F4: 'Covered another way (for example, printers in a secured room)' + the help line from the card); 17:16 "keep the 16 questions" (reorder/reword only; F7 the reviewer's own two sentences, Tuesday's reading recorded on HPSMPOC-489). Also fold in the B1577 gate's F1: `web/src/content/PROVENANCE.md:14` (0.1.2 is no longer the hosted-demo version). Lanes P (b1584), N (b1585), R (b1586) are live/in review: partition against them (they own snapshot UI, narrative, PDF; lane Q owns web/src/content/**, SeedContent/**, the ruleset files, HostedDemo pins, infra appservice ruleset value and their tests). Deploy: none (Kam's 19:16 note: one deploy round after ALL feedback lanes land). Model by row (content version + client-visible scoring: likely C2 Sonnet + G1).
