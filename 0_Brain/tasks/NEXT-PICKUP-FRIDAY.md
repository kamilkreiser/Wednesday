---
date: 2026-09-23
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, rotation handover 2026-09-23 ~16:5x (ctx 78–80%)
supersede: replace wholesale at every wrap; do not append
---

# NEXT PICKUP — FRIDAY

**The tree lives at `/Users/kamilkreiser/1FILES TO SYNC/FRIDAY`** (Kam moved it 2026-09-23 14:1x). Paths with spaces broke
two scripts and the git credential helper; all fixed (30f01874c). If a tool fails with `/Users/kamilkreiser/1FILES: No such
file`, that is the class — quote the path.

## 🔴 LIVE AT THE 2026-09-24 ~11:1x CHECKPOINT (read first)
- **HPSM-POC B04: three seats RUNNING**, panes %7 (A core-platform API), %8 (B web Playbook + 16-q snapshot), %9 (C reporting). Briefs: `HPSM-POC/1_Project_Definition/Briefs/2026-09-24_B04_SEAT-{A,B,C}_*.md`. Seats push branches `b04/*` ONLY; **Friday opens PRs and merges on green** as kamilDatasec (`friday_as.sh datasec gh …`; Kam "keep going and merge when green", "build as much as you can"). Merge pattern: head-pinned squash, one at a time, main push-CI green before the next (the script shape is in the 09-24 note).
- **Datasec Security Composer (NEW standalone project, claimed):** `/Users/kamilkreiser/1FILES TO SYNC/Datasec Security Composer`, cockpit key `Datasec/Security-Composer`. Seat %10 on B01 (Paul's user guide) + ADDENDUM-1 (Kam's template .docx is the base; the demo wins; cold-reader test). Demo login in its `4_Credentials/.env`. Deploy key absent (no push). HPSM originals untouched.
- **STATUS watcher:** `scratchpad/watch_status.sh <seen-file>` (bash, nullglob; 580-s legs, re-arm). Scratchpad paths die with the session: a successor re-creates it from this description.
- **2026-09-24 ~12:1x:** Kam's 11 rulings executed (C-13). The deck arrived: the 16 = PARTNER READINESS SELF-ASSESSMENT (C-14, content extract in HPSM-POC Architecture/content/). ADDENDUM-2/3 with seats A/B. The live board fix is deployed (Friday cards on the FRIDAY tab). **WAITING ON KAM:** 9 Azure providers (command on the panel); cards `hpsmpoc-na-rulings-confirm` + `hpsmpoc-readiness-answer-type`. **OWED BY FRIDAY:** the Spark checker loosened for tests/UI/docs (Kam `spark-byte-exact: b`); Seat C's next brief (the readiness report variant); verify the providers after Kam; check the missing 3 of the '12'.

## STATE — Datasec/HPSM-POC (claimed by Friday), the main work
- **🔴 2026-09-24 REFOCUS (C-12):** the MINIMUM = the Playbook PPT made digital + the 16 snapshot questions, working WELL; everything built is KEPT (main @19fba6e, tag `b02-full-build-2026-09-24`). More detail from Kam early next week (after the meeting with Pete). **WAITING: the Playbook PPT** (not in the folder). Analysis repo has NO remote; Kam's sync is the backup until he says otherwise.
- **Folder:** `/Users/kamilkreiser/1FILES TO SYNC/HPSM-POC` — SELF-CONTAINED by Kam's ruling (he syncs it home). Start at its
  `CLAUDE.md`, `BACKLOG.md`, `1_Project_Definition/CLARIFICATIONS.md` (**C-01…C-11**, Kam's rulings verbatim).
- **B01 + B02 COMPLETE, all REVIEWED + ACCEPTED, NOTHING MERGED.** Reviews sit beside each brief in
  `1_Project_Definition/Briefs/`. Code repo `datasecau/HPSM-POC`: `main` 8869b1a; branches **`b02/infra` 0e3c1f4 (A),
  `b02/web-prototype` 0587fd4 (B), `b02/engine` 2ab4b21 (C)**. Analysis repo (project root, no remote) HEAD ≥ d0fbc7c.
- **All build panes are CLOSED** (idle; state on disk). Relaunch a seat: `cockpit.sh launch Datasec/HPSM-POC[-A|-B|-C]` — the
  launcher reads the newest brief tagged `_SEAT-<X>_` (untagged seat: newest brief).
- **WAITING ON KAM (put to him on the panel; defaults stated):**
  1. His **walkthrough meeting is tomorrow (2026-09-24)**; he'll send answers after → log verbatim (Q&A answers log + CLARIFICATIONS).
  2. M2 review of the drafts: RS-01…RS-11 (RS-11 = not-applicable → no finding, PROPOSED), AD-01…29, the prototype
     (`Design/2026-09-23_M2-prototype-review-guide.md`), SME template, demo script. M2 gate = Fri 9 Oct.
  3. **Local-model clause-2 question** (asked 16:5x, default KEEP EXACT): loosen byte-exact added lines for low-risk classes
     (tests, UI, docs) so the Spark authors content with tests judging? Seat C's ledger: 18/18 first-brief PASS but Claude
     authored every line → little saving today.
  4. ADR-C01 (JsonSchema.Net licence) · not-applicable in multi-question rules · **Entra app registration** · **register the 12
     Azure resource providers** (Owner only; SP can't; `infra/README.md` P1) before any deploy brief.
- **2026-09-24: B03 phases 1+2 DONE — B02 MERGED to main @19fba6e (PRs #1–#4), CI green with every check running; red-proof PRs #5/#6 closed. Record: `Briefs/2026-09-23_B03-P1_…REVIEW.md`. PRs are opened from Friday as kamilDatasec (project gh login still empty, runbook step 11). NEXT: phase 3 (RS-11 scorer fix, routed local first, + regenerate the prototype data) when Kam rules RS-11; branch protection = a decision for Kam.** (Superseded text below.)
- **B03 is DRAFTED and STAGED, not launched:** `HPSM-POC/1_Project_Definition/Briefs_staged/2026-09-23_B03_DRAFT_merge-B02-CI-and-RS-11.md` (outside Briefs/, because the launcher takes the newest Briefs/ file). Phase 1 (CI + PRs, no merge) needs no Kam gate; Phases 2–3 wait on G1–G4. Re-derive the SHAs before launch.
- **NEXT when Kam answers:** B03 = merge plan (PRs one at a time, CI must run; add `npm test` + `npm run typecheck` to ci.yml
  first — Seat B's finding) + the reference-scorer fix for RS-11 + first Dev deploy (billable → tell Kam before, C-07) + the
  Spark splitting per Kam's answer to #3.
- **Mail:** `datasec-hpsm-poc@agentmail.to` still BLOCKED (created 200, invisible to Friday's key → no scoped key). Briefs are FILES.
- **Question sets** (Word + md) in `HPSM-POC/1_Project_Definition/Questions_and_Answers/`; Kam edited the HP-champion doc
  (C-10); HP-Project-Owner questions are Datasec's to answer, not a priority unless blocking (C-09). Nothing sent to HP.

## STATE — the Spark (local model), Friday's
- **PROVEN** 2026-09-23: smoke 6/6, both deliberate breaks caught after the C1 ANCHOR fix; runner accepts only whole-answer
  unfenced diffs; clones in the system temp dir. Harness `2_Project_Files/friday/spark/` (+ tests/), kit 04 amended (modes 8–9).
  A copy lives in `HPSM-POC/tools/spark/` (self-contained). **Standing rule (Kam): local model FIRST** for tasks and tickets.
  Datasec work only on the Spark until Kam rules on Secuura (still open).

## STATE — Datasec/HPSM (claimed): filed + read; N-1 (round 3) is Kam's, default hold. Nothing owed.

## Owed housekeeping
- Tuesday never replied (Spark handover 04:07Z; HPSM claim 04:31Z) — read her reply if one lands.
- A transcript file sits in the recreated `/Users/kamilkreiser/FRIDAY/4_Credentials/.claude/…` (pre-move seat) — Kam's call.
- Kam's Linear key and Jira token were pasted in chat — rotation suggested once each; his call.

## Open claims by Friday
Spark loop · Datasec/HPSM · Datasec/HPSM-POC (all OPEN).
