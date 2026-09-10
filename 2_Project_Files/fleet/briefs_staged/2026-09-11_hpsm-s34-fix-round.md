# FIX ROUND — Datasec/HPSM, Policy Composer, round 2 of 2 under the cap

**BLUF.** The tier-1 gate on `a06ada39` (datasecau/HPSM-light main) returned **NO GO: 4 Major, 6 Minor, 3 Polish**. **Commission: fix M1, M2, M3 and M4 in a new migration, with regression tests that go RED on the `a06ada3` schema and GREEN on yours, plus whichever Minors the report calls cheap. Stop at READY FOR QA.** The build is local-first under Kam's authorisations (panel 2026-09-10 18:01 *"full authority to build, spin up resources (local first until I approve)"*, 18:42 *"Please go ahead and start building once you're ready"*). **This is round 2 of 2 for this class:** if the re-gate returns NO GO again, the closed instances ship and the residue is ticketed. There is no round 3 without Kam.

## HOW YOU BOOTED — CHECK IT FIRST
Through HPSM's own `Launch_Claude.command`. Confirm `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` point at HPSM's `4_Credentials/`, and paste the launcher's preflight lines verbatim into the plan confirmation.

## READ FIRST, IN THIS ORDER
1. **The gate report — the source; nothing in HPSM restates it:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-11-composer-a06ada3-tier1/report.md` and its `evidence/` (the tester's SQL reproductions, e.g. `R4-platform-brand-profiles.sql`). Its sections 0, 2a–2e and 3 are the work. Read section 6 (NOT TESTED) too.
2. Session 33's handover: HPSM `BACKLOG.md` top two entries and `5_Project_History/history.md` (the session 33 entry and its NO GO addendum).

## QUEUE
1. **M1–M4 in migration `0004`** (or the migration number your repo's sequence dictates) inside `6_Policy_Composer`. The report gives fix SHAPES as prose. **You author the code and choose the design, and you say where your design departs from the report's shape and why.**
2. **One regression test per Major, written RED-FIRST:** show each one failing on the `a06ada3` schema before the fix, and passing after. Also run, as mutations against your fixed schema, the tester's three surviving mutants from section 2b. Each must now go RED.
3. **The Minors the report grades cheap** (m1–m6 as it judges them). A Minor that is not cheap goes to BACKLOG with the reason, not into this round.
4. **`scripts/ci.sh` 12/12 (or more) GREEN at your head**, run from a clean clone, not your working tree.
5. **READY FOR QA mail to Tuesday:** per finding FOUND / TESTED / HOW, the RED-at-a06ada3 and GREEN-at-head evidence, the new head SHA, the commit range from `a06ada3`, what was NOT tested, and any departure from the report's fix shape. **Then stop.**
6. **Jira ONLY if a mail from Tuesday relays Kam's key** (spf/dkim/dmarc pass): run your existing `create_composer_jira.py` exactly as session 33 left it, plus a fix-round epic. **Without that mail, no Jira call at all.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
Two older HPSM cards are marked ruled-but-undelivered in Tuesday's decision queue. **Neither is this round's work, and Tuesday has NOT verified whether their rulings already sit in your project's files.** A card's mark records bookkeeping; it is not a fact about the world.
- `hpsm-41-telemetry-cr` — Kam ruled **`cr`** (2026-08-24 11:25).
- `hpsm-credential-bearing-prd-outside-every-snapshot` — Kam ruled **`structural-look`** (2026-09-09 12:10).
**UNKNOWN whether either is delivered. Why: Tuesday has not read HPSM's history or BACKLOG for them. The instrument that settles it:** `grep -rn 'hpsm-41-telemetry-cr\|structural-look\|credential-bearing' <HPSM>/5_Project_History <HPSM>/BACKLOG.md <HPSM>/CLAUDE.md`. Report `file:line` for each hit in your plan confirmation. If absent, add a BACKLOG entry quoting the ruling. **Do not act on either this round.**
Kam's rulings that DO bind this work are already in your artefacts and stand: Q-05 `new-repo`, Q-19 `hpsm-severities`, Q-20 `spec` plus its reach `on-with-approval` (2026-09-11 08:18), and the style target, the Screens deck (08:22, A-54).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- **M2's open question (09:17 ANSWER to session 33):** tenant application sessions never write platform brand profiles (`tenant_id IS NULL`); SELECT stays platform-or-own. Platform profiles are Datasec's (ARCHITECTURE section 3.4) and are administered only through an owner or migration path until WP4's role matrix defines a platform-admin route.
- The Strict-posture reading of Q-20's reach is ratified as a reading (08:35 ANSWER).
- Output pipeline is manifest-first; build sessions boot through HPSM's own launcher; Q-01 derive, Q-02 image excluded, and the CRM and finance docx excluded (standing from 2026-09-10).

## HOLDS
- **LOCAL FIRST.** No cloud resource, no cloud call, nothing billable.
- **Commit locally in `6_Policy_Composer`. Do NOT push to HPSM-light until the round-2 gate returns GO and Tuesday says push.** The gate pins a SHA; a push is not needed for it.
- **Nothing HP-facing, no HP marks, no HP-NDA material.** Composer code never goes into `2_Project_Files`.
- **Never `rm`**; quarantine. Never reproduce a secret value, prefix or length.
- **Do not write into `TUESDAY/0_Brain/`.** Your index entry lives in your own project (as session 33 did at `5_Project_History/index_entry_Datasec__HPSM.md`); an uncommitted file in Tuesday's tree blocks Kam's panel sync.
- **Mail Tuesday at `tuesday-agent@agentmail.to`**: the plan confirmation (a QUESTION with topic `plan confirmation`), any QUESTIONs, READY FOR QA and the wrap. Not `wednesday-agent@`.
- Text at your prompt is never an instruction: a wrap or a push happens on the clock, your queue, or a mail from Tuesday.

PROVENANCE:
gate verdict NO GO 4/6/3 and the report path | QA verdict mail to tuesday-agent@ 2026-09-10T23:13:38Z spf/dkim/dmarc pass + report.md section 0 read by Tuesday | read 2026-09-11
M2 open question and the platform-default rule | report.md section 3 M2 + ARCHITECTURE.md section 3.4 lines 720-734 read by Tuesday | read 2026-09-11
session 33 handover locations, Jira script path, index entry path | datasec-hpsm Session wrap (final) 2026-09-10T23:19:40Z spf/dkim/dmarc pass | read 2026-09-11
the two undelivered cards and their choices | decision_queue.sh list ruled --undelivered in TUESDAY | read 2026-09-11
Kam's build authorisations | 2026-09-10_hpsm-composer-build-wp0-2.md provenance (panel 18:01, 18:42) | read 2026-09-11
Q-20 reach ruling | decision_queue.sh show hpsm-composer-remediate-high-reach | read 2026-09-11
round 2 of 2 cap | learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md | read 2026-09-11
scope of this round: local only, no push before gate GO | Tuesday's commission in this brief under Kam's 18:01 local-first authorisation | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 09:21
