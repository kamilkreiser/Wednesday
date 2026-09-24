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

## 🔴 LIVE AT 2026-09-24 ~14:5x (successor boot, ctx 32% after the load) — READ FIRST
- **Cards: 0 open.** Kam's 11 taps (12:01–14:20, three times over) were never recorded by the previous seat; `reconcile_rulings.py --apply` ruled all 11 at boot, the tiles are hidden (verified `hidden:true`), and they're delivered to **HPSM-POC CLARIFICATIONS C-15** + **Composer C-03** (+ Composer BACKLOG 5/6/8/9/10). **Run `reconcile_rulings.py` at EVERY checkpoint and before any handover** (ledger 2026-09-24 self-caught row). Reconciler stderr fix 3e25bea75.
- **RUNNING (3 seats, all verified rung 6):**
  - ~~`%15` Composer Seat A~~ **DONE 15:08: guide v1.2 emailed to Kam (2 mails, verified), pane closed.** Open: card `composer-guide-sme-practice-points` (default: the guide stands).
  - ~~`%17` HPSM-POC B06~~ **MERGED** PR #12 → main **438d5d7** (15:39; item-0 CI fix 3309437 by Seat C; main push CI green). Card open: `hpsmpoc-na-ignore-reading` (default: as built).
  - `%19` HPSM-POC **Seat C, B07** (`Briefs/2026-09-24_B07_SEAT-C_sqlite-points-check-and-first-signin-race.md`): SQLite 500 for 2–9 ticks + first-sign-in race. `api/` only. Friday opens the PR, merges on green.
  - `%20` HPSM-POC **Seat B, B07** (`Briefs/2026-09-24_B07_SEAT-B_web-readiness-plan-422-and-mock-switch.md`): the readiness plan shape vs the real API, 422 message, mock mirrors the switch (Kam's draft-ruleset-scoring b; a demo exception was NOT re-asked), axe flake. `web/` only.
  - `%18` Composer **Seat B, B04** (`Datasec Security Composer/1_Project_Definition/Briefs/2026-09-24_B04_SEAT-B_mobile-and-tablet-design-pass.md`): phone + tablet as real targets; branch `design/2026-09-24-mobile` from 5c0490d; **no merge, no deploy** → at READY Friday cards the deploy for Kam with screenshots.
- **Wake:** STATUS watcher = `<scratchpad>/watch_status.sh <seen-file>` (bash, nullglob, 30-s polls, 55-min legs, fires on a NEW READY FOR REVIEW / BLOCKED / STOP in B06-A, B07-B/C and Composer B04 STATUS files). Scratchpad dies with the session: re-create from this line.
- **Kam's hands:** 9 Azure providers (HPSM-POC; command on the panel) · the HP E8 SOW file into `Datasec Security Composer/1_Project_Definition/Source_Documents/` (empty at 14:5x). Spark powered down (on re-plug: run-a2.sh + the tunnel).

## 🔴 ROTATION HANDOVER 2026-09-24 ~14:4x (ctx 80%) — (superseded by the block above)
- **THE OPEN THREAD: Composer guide v1.2 for Paul.** Seat A RUNNING in pane %15 (`Datasec/Security-Composer-A`), brief `Datasec Security Composer/1_Project_Definition/Briefs/2026-09-24_B02_SEAT-A_guide-v1-2-salesperson.md` + ADDENDUM-1 (re-shoot the form screenshots after cold-reader run 3; the demo was redeployed). STATUS: `…/Briefs/2026-09-24_B02_STATUS.md`. **On READY:** review (runs in `User_Guide/2026-09-24_Paul_v1_2/cold-reader-runs/`: 0 guesses on the last run; the password in neither file, with a positive control; look at pages) → **EMAIL Kam** at kamil.kreiser@datasec.com.au as 2 mails (the PDF with the note, then the DOCX; the combined send is 413), verify both sent copies (AgentMail API from friday-laptop-agent@; the payload shape is in the 09-24 note ~12:45) → close %15 → post any new Kam decisions as cards.
- **Composer demo DEPLOYED 5c0490d** (the design fixes; Kam's word). Temp NSG rule + key REMOVED and proven. Kam's az login lives in `Datasec Security Composer/4_Credentials/.azure` (kreiser.org, sub 0c57ab37). Rollback = /opt/hpsm/composer.prev on the VM (reach it only by adding a temp NSG rule + a temp key via az vm run-command, then removing both).
- **HPSM-POC:** main e7a4d1b, all seats closed, all PRs merged (#1–#11). Nothing running.
- ~~Open cards (11)~~ ALL RULED by Kam; recorded at the 14:5x boot (see the block above).
- **Kam's hands:** 9 Azure providers for HPSM-POC (command on the panel). The Spark is stopped (the container is down; the laptop tunnel is closed); on re-plug: run-a2.sh + the tunnel.
- **Owed by Friday:** the Spark checker loosened for tests/UI/docs; verify the providers after Kam; Seat B's contract workaround can be dropped (HPSM-POC web); the stopped local stack pc-b03 (Composer) is kept.

## (older) LIVE AT 2026-09-24 12:4x (70% checkpoint)
- **HPSM-POC main @ 8d65fec** (B02 + B04-A/B-web pending + B04-C + B05-C merged; #8, #10 merged). **PR #9 (web) OPEN**: CI red round 1 (Node-24 sessionStorage) fixed; round 2 = mobile overflow 424>412 px on Linux fonts, **Seat B running in %14 (round 2 of 2, THE CAP: if still red, ship the closed parts and ticket the rest)**. **Seat A running in %11** (B05: fold the ADRs into the design pack + the root README + the analysis push). Merge on green, head-pinned.
- **Composer guide DONE + EMAILED to Kam** (2 mails, verified). Cards: composer-hp-sow-name-on-demo, composer-guide-font, composer-purge-test-engagements. Deploy key for HPSM-light is still absent.
- **Open cards (Friday tab):** na-rulings-confirm · readiness-answer-type · dev-signin · draft-ruleset-scoring · 403-for-missing-ids · partner-scope · the 3 composer cards. **Kam's hands:** 9 Azure providers.
- **OWED ACTION (Kam 2026-09-24 ~13:3x, verbatim: "send me the updated guide when it's ready"):** when Composer B02 (guide v1.2) is READY + reviewed (the salesperson cold-reader pass), email the .pdf and .docx to kamil.kreiser@datasec.com.au as TWO mails (one attachment each: the combined send is 413 over ~7 MB), and verify both sent copies.
- **Owed by Friday:** the Spark checker loosened for tests/UI/docs; verify the providers after Kam; the missing 3 of the '12'.

## (older) LIVE AT 2026-09-24 12:1x (65% checkpoint)
- **HPSM-POC:** main @ 32b74ba (B02 + B04-C merged). **PR #8 (B04-A, core platform) open, CI running → merge on green** (head cf66ef8, head-pinned squash, then main push CI green). Seat A/C panes CLOSED (A's local API still on :5180). **Seat B RUNNING in %8** (web Playbook + the deck's 16 questions; ADDENDUM-2/3). **Next briefs owed:** C (readiness report variant + A's SchemaRegistry.Global fix) · A-next (fold ADR-A01…A19 + openapi.delta into the design pack; root README run notes) · the Spark checker loosened for tests/UI/docs (Kam, `spark-byte-exact: b`).
- **Composer guide seat RUNNING in %10** (B01 + ADDENDUM-1). On READY: review, then EMAIL the .docx + .pdf to kamil.kreiser@datasec.com.au (owed, below).
- **Open Friday-tab cards:** na-rulings-confirm · readiness-answer-type · dev-signin · draft-ruleset-scoring · 403-for-missing-ids · partner-scope. **Kam's hands:** 9 Azure providers (command on the panel).

## (older) LIVE AT THE 2026-09-24 ~11:1x CHECKPOINT
- **HPSM-POC B04: three seats RUNNING**, panes %7 (A core-platform API), %8 (B web Playbook + 16-q snapshot), %9 (C reporting). Briefs: `HPSM-POC/1_Project_Definition/Briefs/2026-09-24_B04_SEAT-{A,B,C}_*.md`. Seats push branches `b04/*` ONLY; **Friday opens PRs and merges on green** as kamilDatasec (`friday_as.sh datasec gh …`; Kam "keep going and merge when green", "build as much as you can"). Merge pattern: head-pinned squash, one at a time, main push-CI green before the next (the script shape is in the 09-24 note).
- **Datasec Security Composer (NEW standalone project, claimed):** `/Users/kamilkreiser/1FILES TO SYNC/Datasec Security Composer`, cockpit key `Datasec/Security-Composer`. Seat %10 on B01 (Paul's user guide) + ADDENDUM-1 (Kam's template .docx is the base; the demo wins; cold-reader test). Demo login in its `4_Credentials/.env`. Deploy key absent (no push). HPSM originals untouched.
- ~~OWED: email the guide to Kam~~ DONE 12:45 (2 mails, sent copies verified).
- **Seat A rotation:** the launcher takes the NEWEST `_SEAT-A_` file, now ADDENDUM-1. Before relaunching A, write a `…_B04_SEAT-A_SUCCESSOR_…md` brief pointing at the main brief + ADDENDUM-1/2/3 + its STATUS.
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
