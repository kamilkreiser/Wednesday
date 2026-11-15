# Wave 06:40, 2026-11-16: the morning sweep and three records-kit drafters (Tuesday s280)

Tracked so the commission survives rotation. A drafter whose output is absent at the next boot is RE-COMMISSIONED from its section below. Kam, Tuesday terminal ~06:2x, verbatim: "keep going with the tickets".

## For every drafter
1. Read `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole first (`/Volumes/Laptop-DEV/` paths mean `/Volumes/Datasec_DEV/`).
2. Copy the SHAPE of your template kit and read its drafter report. Write ONLY your kit, its `.measured` sidecar (via `stamp_check.py --init`; `stamp_check.py <kit>` must exit 0), your report (last line `DRAFTED B<n>: kit <lines> lines, sidecar rc <rc>, questions <n>`), and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s280/d<B-number>/`.
3. The SOURCE of what is owed is Tuesday's pickup `/Volumes/Datasec_DEV/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md`, DELTAs 1184 to 1187 (read whole; they head the file), plus the gate verdicts they name. Re-verify every landing at source (`gh api -X GET`) before you write it into a kit.
4. Kam's rulings since 11-15 13:47 are verbatim in `/Volumes/Datasec_DEV/TUESDAY/0_Brain/daily_tuesday/2026-11-15.md`. Cite each as "the product owner's 2026-11-15 ruling" in any text a seat copies into a record.
5. Fences: no push, no PR, no Jira WRITE (GET only, per DRAFTER_RULES), no mail, no board, no az, no cd. Print no token. Never read `0_Brain/learnings/_ledger.md`. Never publish (no Artifact tool). Never run `decision_queue.sh list`.

## SWEEP-0640: the Datasec actionable-lanes sweep (template: `2026-11-15_SWEEP-1925_datasec-actionable-lanes.md`)
Output `tuesday/briefs/2026-11-16_SWEEP-0640_datasec-actionable-lanes.md`. Boards: HPSM-POC, MPS Calculator, Security Composer, NexusAI (read-only). Exclude everything landed tonight (DELTA 1187's list), everything in records-owed, everything HELD or DROPPED in the pickup or the notes (grep each key), the HTML phase items (Kam + Paul decide), HP-tool integrations, and the HPSM deploy round. Propose lanes that share no files, each with keys, owned paths, model row and gate tier.

## B1600 SEAT-R241: HPSM-POC records (template: `2026-11-15_B1583_SEAT-R236_hpsmpoc-records-reviewer-feedback.md`)
Landings #321, #322, #323, #324 and #325 (#325 if landed by stamp time; else it is left to the next pass); Kam's q1/q5/narrative-migration rulings delivered (C-entries); the gate Minors (B1584 x5, B1586 F1 README ADR-R13, B1597 F1 stamped-set.test.ts:17, B1585 F1-F3, B1599 F1); HPSMPOC-485/-487 descriptions still say 'awaiting words'; HPSMPOC-489 does not quote the sentences; the ForwardedProof defect ticket (it cites PR #325); the move rules by each ticket's Done rule.

## B1601 SEAT-R242: MPS records (template: `2026-11-15_B1591_SEAT-R240_mps-records-195-331-341.md`)
Landings #197, #198, #199; MPSCALC-128, -229, -99, -397, -398 by the Done rule; 349 measured and confirmed (the 11-15 19:15 standing rule moves measurement-only tickets); 150 done as built (Kam 21:03), plus `decision_queue.sh --delivered mpscalc-150-usage-section-placement-1115` and `mpscalc-99-laneMA-round-cap-1115` against the C-entries (Tuesday runs these after READY, not the seat); 224 comment (built, open for its host read; stale needs-ruling label); B1593 gate F1-F4 as one follow-up ticket; B1594 residue (fsevents, 17 e2e skips); the B1596 round-3 Minors.

## B1602 SEAT-R243: NexusAI records (template: `2026-11-15_B1588_SEAT-R237_nexusai-records-201-202.md`)
Landings #204, #205; RD-988/926/888/456/492/808/475/560/481 by the Done rule; RD-189 a duplicate of RD-733; RD-117/188 to the next NX-F1 slice (a real-browser CSP check first); the rd452 'addition B' timing-flake ticket (gate B1598 F1); rd-721 needs an absolute href (gate B1595 F3); the coordinator-action route decision (RD-988's own text); stale comments rd465:164-166 and rd486:267; pointer :634 -> :647.
