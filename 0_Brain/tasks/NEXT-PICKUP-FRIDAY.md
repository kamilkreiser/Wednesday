---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, 70% checkpoint 2026-09-23 ~15:4x (not a wrap — the seat is still running)
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**The tree moved (Kam, 14:1x):** it now lives at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`. The move broke three loops (re-armed) and the
git credential helper (repointed); two scripts fixed for the space in the path (30f01874c). Any other tool that splices a path unquoted
will break the same way — if something fails with `/Users/kamilkreiser/1FILES: No such file`, that is the class.


## CHECKPOINT 70% (~15:4x) — current state, read this first
- **HPSM-POC (Datasec, claimed):** rulings C-01…C-08 in its CLARIFICATIONS. Build seat in cockpit pane `%2` finished **B01 → READY FOR REVIEW**; Friday REVIEWED + ACCEPTED it (`HPSM-POC/1_Project_Definition/Briefs/2026-09-23_B01_setup-and-M2-drafts.REVIEW.md`; independently checked: GitHub main `8869b1a`, CI + CodeQL SUCCESS, analysis repo 0 forbidden files). The seat is IDLE by design. **Waiting on Kam** to review 4 drafts for M2 (Fri 9 Oct): rules schema RS-01…10, SME template, demo script v0, AD-01…09. Then brief **B02** (carry-overs listed in the REVIEW file: commit Friday's Q&A files, launcher sources `.tools/env.sh`, carve WS4 engine work into Spark-sized tasks).
- **Spark loop PROVEN** (smoke 6/6, both deliberate breaks caught after the C1 anchor fix; runner accepts only whole-answer unfenced diffs; clones live in the system temp dir; self-tests in `2_Project_Files/friday/spark/tests/`). **Kam's standing rule: local model FIRST for tasks and tickets** (Datasec work only on the Spark until he rules on Secuura).
- **Word question sets** (HP project owner / HP champion / Datasec experts) are in `HPSM-POC/1_Project_Definition/Questions_and_Answers/` — Kam's to send; nothing sent.
- **BLOCKED:** `datasec-hpsm-poc@agentmail.to` (created 200, invisible to Friday's key → no scoped key). Briefs are FILES for now.
- **Kam, 2026-09-23 ~15:5x, verbatim:** *"I have a meeting tomorrow to start going through the walkthrough and will respond to you once that's done."* → HPSM-POC HOLDS until he responds (no B02, no seat launch). The walkthrough agenda is §1 of `HPSM-POC/1_Project_Definition/Questions_and_Answers/2026-09-23_stakeholder-questions-to-ask_POC.md`. When he responds: log his answers verbatim (Q&A answers log + CLARIFICATIONS), then brief B02. The seat pane %2 was CLOSED (idle, state on disk); B02 relaunches via `cockpit.sh launch Datasec/HPSM-POC`.
- No mail pending (no reply from Tuesday on the Spark or HPSM); no Kam panel rulings today (kam_rulings_today 0).

## OWED — first work of the next session
1. **Datasec/HPSM-POC (claimed by Friday).** Scaffold, plan, Q&A and Jira are DONE (see the project's `CLAUDE.md` + `BACKLOG.md`).
   Waiting on **Kam's five W1 decisions** (BACKLOG.md): SOW-01 relationship + who the Development Team is; the event date (Amplify
   5–10 Dec would break the 12-week plan); IP incl. any Composer reuse; named PO/SME + SME hours; Azure tenant + payer.
   Owed setup (SETUP_RUNBOOK): the project's `git init` belongs to the project seat (the hook refused Friday; correctly); launcher;
   inbox; GitHub repo; Azure. **Build seats run in visible cockpit panes** (Kam's ruling today).
2. **Spark smoke test (owed item from the previous pickup, still OPEN).** Harness BUILT and self-tested:
   `2_Project_Files/friday/spark/{spark_run.py, spark_check.py}` (NOT yet committed — commit with this checkpoint). Smoke brief +
   expect.json are committed at `2_Project_Files/friday/spark/briefs/SMOKE-arms-path.{md,expect.json}`. Target: our own `tests/absence_claim_check_arms.sh` line 3 (hardcoded DevMASTER
   path; fix proven green 9/0 on a copy; tip 15189f1f3 — re-derive the tip before running, it will have moved). Then the two deliberate
   breaks (wrong expected line → C2 must fail; non-existent line → C1 must fail), then report to Kam. Datasec-only default for the box stands.
3. **Datasec/HPSM (claimed):** filed and read. N-1 (round 3) is Kam's; default hold. Nothing else owed.

## Done this session (do not redo)
- FIRST-BOOT line removed from Friday's boot prompt (f08a65e23).
- Loops re-armed from the new path; publisher self-match bug + wake_watch unquoted path fixed (30f01874c); git push repaired.
- HPSM archive unpacked and merged additively (M2/m2 case collision preserved); Tuesday mailed about the HPSM claim.
- HPSM-POC: scaffold; SOW filed; scope diff, reuse inventory, delivery plan, master Q&A (183 rows); Jira HPSMPOC id 10588 board 606,
  9 epics + 55 tasks verified; token in `HPSM-POC/4_Credentials/.env` (Kam pasted it in chat — rotation suggested once).
- Lesson: build seats in cockpit panes (ledger row, digests regenerated, pushed).

## Open claims by Friday
Spark loop (OPEN) · Datasec/HPSM (OPEN) · Datasec/HPSM-POC (OPEN) · space-in-path fixes (release after this checkpoint's commit).
