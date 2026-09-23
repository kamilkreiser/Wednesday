---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, 75% handover 2026-09-23 ~16:2x (rotation band next)
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**The tree moved (Kam, 14:1x):** it now lives at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`. The move broke three loops (re-armed) and the
git credential helper (repointed); two scripts fixed for the space in the path (30f01874c). Any other tool that splices a path unquoted
will break the same way — if something fails with `/Users/kamilkreiser/1FILES: No such file`, that is the class.


## HANDOVER 75% (~16:2x) — current state, read this first
- **HPSM-POC B02 is RUNNING as THREE concurrent seats** (Kam C-11, verbatim in `HPSM-POC/1_Project_Definition/CLARIFICATIONS.md`: start the build agent, local LLM as much as possible, concurrent agents OK; quality bar = thorough testing · security · GDPR · software-design best practice · graphic/UX UI):
  - pane `%3` **Datasec/HPSM-POC-A** — design pack + security/GDPR pack + read-only Azure OpenAI availability + Bicep draft (no deploy) + test strategy. Brief `…/Briefs/2026-09-23_B02_SEAT-A_design-pack-and-infra.md`.
  - pane `%4` **Datasec/HPSM-POC-B** — design system + clickable prototype of the 7-min journey + Playwright/axe tests + screenshots. Brief `…_B02_SEAT-B_clickable-prototype-and-design-system.md`.
  - pane `%5` **Datasec/HPSM-POC-C** — C# rules engine through the LOCAL MODEL (the seat runs `HPSM-POC/tools/spark/` itself; Friday copied the proven harness in, self-contained) + golden tests vs `reference_scorer.py`. Brief `…_B02_SEAT-C_rules-engine-via-local-model.md`.
  - Each seat: own worktree `.tools/wt-<A|B|C>` + own branch (`b02/infra`, `b02/web-prototype`, `b02/engine`); `.tools/.git-lock` around ref writes; **nothing merges to main without Friday's review + GO**; only seat A commits the analysis repo. Reports: `…_B02_SEAT-X_….STATUS.md` → READY FOR REVIEW.
  - **Verified at launch:** each claude process carries `YOUR SEAT: A|B|C` (ps argv) and each created its worktree (wt-A/B/C) with CPU in use. ⚠ **The panes are only 12–14 rows tall, so pane TEXT shows nothing** — judge seats by their STATUS files, worktrees and branch pushes, NOT by capture-pane. (Kam can zoom a pane: tmux prefix + z.)
  - A background watcher in THIS session (dies with it) wakes on any STATUS READY/BLOCKED. **Successor: re-arm one, or poll the three STATUS files.**
  - **UPDATE ~16:4x — SEAT B DONE:** READY FOR REVIEW → Friday REVIEWED + ACCEPTED (`…_B02_SEAT-B_….REVIEW.md`; branch `b02/web-prototype` head `0587fd4` checked on GitHub; no CI on the branch — workflow runs on main/PR). **Pane %4 CLOSED** (idle; listeners 21→21). NOT merged: merge later via a PR once `ci.yml` also runs vitest + typecheck (B's finding 2).
  - **Seat C ADDENDUM-1** (`…_B02_SEAT-C_ADDENDUM-1_not-applicable-findings.md`, tapped as a pointer): B found the reference scorer fires a finding on a NOT-APPLICABLE question; C must NOT freeze that into golden tests; not-applicable → no finding, PROPOSED to Kam as **RS-11**; the scorer fix (`Architecture/rules-schema-v0/tools/reference_scorer.py`) is OWED to a later brief.
  - **UPDATE ~16:5x — SEAT C DONE:** READY → REVIEWED + ACCEPTED (`…_B02_SEAT-C_….REVIEW.md`; `b02/engine` head `2ab4b21` on GitHub; 19 Spark PASS / 0 FAIL verdicts). **Pane %5 CLOSED.** NOT merged. ⚠ **Local-model ledger, honest reading:** 18/18 units PASS first brief, but CLAUDE authored every line (clause 2 needs byte-exact `+` lines in the brief) → saving is small → **decision put to Kam** (loosen clause 2 for some task classes so the model authors, tests judging — or keep byte-exact).
  - **Only seat A (%3) still running;** watcher covers A only. When A is READY: review, then MERGE PLAN = A, B, C one at a time via PRs (CI must run; add vitest + typecheck to ci.yml first), only after Kam's decisions that gate each (RS-11, ADR-C01 JsonSchema.Net licence, not-applicable in multi-question rules, Entra app registration).
- **Review duty when a seat reports READY:** delivered-vs-commissioned against its brief + the C-11 quality bar; check claims AT SOURCE (branch SHA on GitHub, CI run, test counts re-run where cheap, Spark ledger for seat C); then GO a merge to main, one branch at a time.
- **Launcher is seat-aware** (`HPSM-POC/Launch_Claude.command`: waits for `@cockpit_name`, appends the seat line); launchers.conf has `Datasec/HPSM-POC` + `-A/-B/-C` (backups `.pre-0923-1525-hpsmpoc`, `.pre-0923-1610-seats`).
- **Also today:** Kam ruled C-09 (HP-Project-Owner questions answerable by Datasec, not a priority unless blocking) and edited the HP-champion Word doc himself (C-10; now 19 questions incl. a flow/process/outputs section). He has a **walkthrough meeting tomorrow** and will send answers after — log them verbatim.
- Spark loop PROVEN; local-model-first is a standing rule. Datasec only on the Spark.
- BLOCKED as before: `datasec-hpsm-poc@agentmail.to` (no scoped key).

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
Spark loop (OPEN) · Datasec/HPSM (OPEN) · Datasec/HPSM-POC (OPEN — three B02 seats running).
