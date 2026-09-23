---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, 65% checkpoint 2026-09-23 ~15:3x (not a wrap — the seat is still running)
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**The tree moved (Kam, 14:1x):** it now lives at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`. The move broke three loops (re-armed) and the
git credential helper (repointed); two scripts fixed for the space in the path (30f01874c). Any other tool that splices a path unquoted
will break the same way — if something fails with `/Users/kamilkreiser/1FILES: No such file`, that is the class.


## CHECKPOINT 65% (~15:3x) — what changed since 50%
- **Kam's HPSM-POC rulings C-01…C-08** are in `HPSM-POC/1_Project_Definition/CLARIFICATIONS.md` (the POC doesn't replace SOW-01; team = Kam + Friday; event Tue 1 Dec; Datasec owns the IP; Kam is PO; his Azure pays; SOW stack A, borrowing Composer CONTENT not code).
- **Done:** GitHub `datasecau/HPSM-POC` + rw deploy key; Azure RG `hpsm-poc-rg` + SP `hpsm-poc-deploy` (boundary proven); plan v2 re-based to 1 Dec (reviewed; the 63→64 slip fixed); folder SELF-CONTAINED (Reference_from_HPSM copies + its own launcher; Kam will sync it home); stakeholder question sets (md) + 3 Word docs (HP project owner / HP champion / Datasec experts), rendered via Word and checked.
- **RUNNING:** HPSM-POC build seat in cockpit pane `%2` on brief `HPSM-POC/1_Project_Definition/Briefs/2026-09-23_B01_setup-and-M2-drafts.md`; it reports to `…B01….STATUS.md` + history.md. A background watcher (this session only — it dies with the session) wakes on READY/BLOCKED or 10 min idle. **A successor must re-arm a watcher or just read the STATUS file.**
- **BLOCKED:** `datasec-hpsm-poc@agentmail.to` — create returned 200 but Friday's key gets 404 on it; no scoped key minted. The inbox exists (never delete); diagnose the scope before retrying.
- **NEW STANDING RULE (Kam):** local model first for tasks and tickets (`learnings/2026-09-23_use-the-local-model-as-much-as-possible.md`). → **The Spark smoke test (OWED item 2) is next**, then routing HPSM-POC tickets to the Spark once the skeleton exists.
- **Queued with Kam:** the 30-minute walkthrough (what a great 7 minutes on 1 Dec looks like), not yet scheduled.

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
