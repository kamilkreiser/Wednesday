# QA Agent Invocation Brief — Datasec / NexusAI, NARROW RE-GATE @ `6dc400a` (closure of the batched pass's F-1/F-2/F-3/F-4/F-5/F-6, and what the fix round introduced)

**R0 (client isolation):** this brief carries exactly one client's content — Datasec / NexusAI. Report under `projects/nexusai/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. This is a RE-GATE — read the batched pass first
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-05-s33-round-095ea0c-batched/report.md` (+ `evidence/`). It judged `095ea0c` and found: **F-1 MAJOR** (the RD-245 migration silently UNDONE on the next boot — `restoreFromBackupsIfNeeded()` in the constructor merges the key back from the pre-migration backup; permanent because the new file exists) · **F-2 MAJOR pre-existing** (erasure leaves user queries readable in `backups/` and `.emergency-backup/`; the builder then measured the next step: a reboot RESTORES the erased live file) · F-3 (claim 6's tests were source-text matchers) · F-4 (F-5 post-condition header overclaimed) · F-5 (nine-vs-ten divergences; value list not in tree) · F-6 (per-run key seed: `home-containment.js` contains HOME but not DATA_DIR). **Your job: confirm or refute closure of each at `6dc400a` with the batched pass's own probes, and hunt what the fix introduced.** Do not re-run the whole batched pass.

## 1. Target
- **Client / Project:** Datasec / NexusAI. **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files` — the builder is at its handover boundary and is being ROTATED during this pass; a successor may boot. Work from your own pinned worktree (`./scripts/qa-surface-up.sh 6dc400a <port>`); never touch the builder's tree or port 3111; 3115/3116 are stopped.
- **Branch under test:** `rd-136-nga-defaults-s12` at **`6dc400a43eb1e3d22fb3292cc3d0ea324fcd4ceb`** — verified at origin by Wednesday at 10:2x AEST; ONE commit above `095ea0c` ("Gate fix round: the migration survives a reboot, and so does an erasure"), 9 files +602/−27: `jsonStorage.js` +113, `dataErasure.js` +47, NEW `__tests__/erasure-reaches-backups.test.js` (+187), `helpers/home-containment.js` +27, and four test files touched. Pin to it; report the head at the end.
- **Environment:** LOCAL DEV, SQLite only; no LAW, no synthetic feed (RD-118), no deploy, no outbound calls.

## 2. The builder's claims at `6dc400a` — inputs to FALSIFY (from its mail 2026-09-05T00:21:57Z)
1. **F-1:** a tombstone file `.dropped-keys.json` beside the data, subtracted from `missingKeys`; **honoured on BOTH restore paths** — the merge path (the measured defect) AND the wholesale-restore branch (which copies a pre-migration file back verbatim). Own file rather than a settings key because a settings write would consume a backup generation. Test constructs `JsonStorage` TWICE with no `setSetting` between; red proof: delete the tombstone → the key returns; CONTROL: a genuinely lost key IS still restored.
2. **F-2 (Wednesday's DELETE ruling):** `purgeNow` removes `backups/`, `.prev`, `.emergency-backup/` copies of every PURGE_FILES entry, **backups BEFORE live per file** (so a mid-purge crash cannot leave "backup present, live absent" — the restore trigger). Test: purge → construct → canary absent from live and all three copies; red proof: skip the backup deletion → canary returns; CONTROL: the canary was in all four copies first ("it caught my fixture being one write short, because backups lag live by one write"). Tombstone asserted to hold key NAMES only.
3. **F-3:** both text matchers gone; replaced by the behavioural erasure test and an export test asserting the ENTRIES.
4. **F-4:** header claim WITHDRAWN; the post-condition reports LOSS (a differing copy existed and none survives), not ABSENCE; silent in four of nine states deliberately (builder's reasoning: an error on "no rollback target" would fire on every fresh store). **Wednesday accepted that reasoning** — confirm the header now says what the code does.
5. **F-5:** the 48-case value list is in the tree; the tests assert the two divergence CLASSES plus a DERIVED count (no number quoted in code); `firstRunComplete: 0.011` now in the list.
6. **F-6:** DATA_DIR contained per worker in `helpers/home-containment.js`; the suites that minted `data/.machine-id` no longer create it. One fallout fixed: `data-dir-unset-branch.test.js`'s control read the PARENT's `process.env.DATA_DIR` and went red; it now reads the child's env.
7. Gate: `PASS — 1577/1577 across 94` (counts regenerated 1565/93 → 1577/94).
8. RD-308 (High, privacy — "right-to-erasure is REVERTED by the next restart") and RD-309 (the per-run seed) filed. No deploy taken.

## 3. Scope — the closure table plus the introduced-defect hunt
- **F-1 closure, MEASURED on a real server restart as the batched pass did** (`:31xx`, seeded pre-upgrade settings with the legacy key): upgrade boot → restart with NO intervening write → the key stays absent and the new file intact. Then the WHOLESALE branch: delete the live file after migration (keep the backup) → restart → is the pre-migration file copied back with the key? Then the CONTROL the builder claims: remove a real setting from live (not tombstoned) → restart → it IS restored. **Then the introduced-defect hunt:** where does the tombstone live relative to the persistent volume and the backup rotation (is `.dropped-keys.json` itself backed up, exported, erased, or restored)? What happens if the tombstone is lost but the new file exists (does the key come back)? Is the tombstone read before or after the restore's own `missingKeys` computation on the wholesale path?
- **F-2 closure, MEASURED:** drive `purgeNow` (module level, force, as the batched pass did) on a store with the canary in all four copies → construct → canary absent everywhere; re-run the batched pass's erasure probe. **Introduced-defect hunt:** the order "backups before live, per file" — simulate a crash after the backups are deleted and before the live delete: does the next boot treat "live present, no backup" as normal (builder's claim) — or does it rotate a fresh backup FROM the still-present live file, re-creating a copy of the customer data that the resumed purge then never deletes? Does purge also remove the tombstone or the new audit-log file (it must remove the audit-log file — it is customer data)? Does `CUSTOMER_DATA_FILES` (export) and `PURGE_FILES` (erasure) still agree on the set?
- **F-3:** grep the test tree for `toContain(` over source text — zero remaining in the two files; the export test asserts entries, not names.
- **F-4 / F-5:** read the header; re-derive the divergence count from the in-tree list (should be derived, not quoted); add a thirteenth value and confirm the count moves.
- **F-6, MEASURED:** `data/.machine-id` absent before the full suite, absent after (the batched pass's exact check); the quarantined instances untouched. The `data-dir-unset-branch` control: does it still discriminate (make its branch wrong → red)?
- **Gate re-run** on your worktree; numbers beside 1577/94.
- **Browser (short):** seeded pre-upgrade store → boot → `/api/ai/audit-log` serves the entries → restart → still served, settings not re-bloated; Sustainability tab renders. Both modes not required this pass; one mode, 0 console errors if the channel captures (the batched pass could not prove console cleanliness — say so if it recurs).

**Out of scope:** LAW branch, synthetic feed, RD-304/305/306, the builder's tree/3111, `data/.machine-id` and the quarantine (observe only), any deploy.

## 4–6. Credentials / state / boundary — as the batched brief
`.env` only if the stand-up needs it; never echo. Exclude-and-report-only on shared state; own temp dirs; **NEVER `rm`** (quarantine); restore tampers byte-identically with hashes. **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every action-recommending finding: MEASURED AT RUNTIME / PROBED / READ ONLY.

## 7. Known-fragile / carried
The batched pass's own corrections (a Blocker downgraded after testing the complement; a void probe replaced with a race carrying a control). Recent changes not to flag: everything in the batched brief §7. Known gaps carried: the mount-alone hole (349 tests green), RD-304/305/306, console capture inconclusive.

## 8. Logistics
- **Time-box:** narrow — closure plus the introduced-defect hunt on the two Majors.
- **Findings sink:** `projects/nexusai/reports/2026-09-05-s33-regate-6dc400a-narrow/report.md` + `evidence/`. A CLOSURE TABLE for F-1…F-6 (CLOSED / PARTIAL / OPEN with the probe), then new findings by severity with evidence class.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] NexusAI RE-GATE @ 6dc400a (narrow)` — BLUF, report path, closure table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- 6dc400a43eb1… at origin; one commit above 095ea0c; 9 files +602/−27 with the per-file counts | `git ls-remote`, `git log --oneline 095ea0c..origin/…`, `git diff --stat` on the NexusAI repo (read-only) | read 2026-09-05
- Claims 1–8 | builder's mail `[Datasec/NexusAI -> Wednesday] READY FOR RE-GATE @ 6dc400a — all six findings closed, gate PASS 1577/94, RD-308 + RD-309 filed` at wednesday-agent@agentmail.to, 2026-09-05T00:21:57Z | read 2026-09-05
- F-1…F-6 as found, with probes | `projects/nexusai/reports/2026-09-05-s33-round-095ea0c-batched/report.md` and its mail 2026-09-05T00:04:41Z | read 2026-09-05
- Wednesday's DELETE ruling and its four conditions | Wednesday's ANSWER `F-2 delete-vs-scrub …` 2026-09-05 10:2x (`briefs_staged/S33_f2_ruling.md`) — Wednesday's project, not the QA project's | read 2026-09-05
- RD-308 To Do/High, RD-309 To Do/Medium | Jira REST search, project RD | read 2026-09-05
- The builder is at its handover boundary / being rotated | Wednesday's checkpoint mail 10:2x and the builder's mail above — Wednesday's project, not the QA project's | read 2026-09-05
