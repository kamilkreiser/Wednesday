# COMMISSION — Datasec/NexusAI: prepare the Azure Marketplace submission package

**BLUF.** Kam, panel 2026-09-11 08:06: *"is the Nexus AI zip file for Azure Marketplace submission ready?"* and *"Don't forget all the screenshots and everything else."* **It is not ready.** This session makes it ready for his review: push the remediation branch, fix two findings, re-shoot the listing screenshots he ruled, and assemble a **DRAFT** submission zip from the resulting head. **Nothing merges, nothing deploys, nothing goes to Partner Center. SUBMISSION IS KAM'S.**

## STATE, MEASURED

- Branch `s51-marketplace-remediation` @ `ed8b208`, clean, **NOT on origin**; origin `main` is `cd2b543`. Worktree: `wt-s51-mktremed`.
- The tier-1 QA gate on `ed8b208` (2026-09-10 evening): **GO with findings, no Blocker.** Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-10-s51-mktremed-ed8b208-tier1/report.md`. Its verdict mail was never sent; that file IS the verdict.
- `deploy-demo.yml` fires on pushes to `main` only; a feature-branch push triggers `npm-audit` only.

## QUEUE

1. **PUSH the branch** — the feature branch, never `main` — using the repo-local `core.sshCommand` deploy key. Verify local equals origin.
2. **FIX M1** (report section 2): `backend/server.js:15961` logs `req.body`, which carries the service-principal client secret, when a data source is saved. Kam's card on it is OPEN, recommended and defaulted to fix first. **Make it its OWN commit**, so it can be dropped if he rules otherwise. Red-proof: save a data source with a synthetic secret and the container log carries 0 secret lines; control: the boot banner is still logged.
3. **FIX m1** (report section 2): the Back-navigation "ghost value" regression introduced by `ec7a3ad` — the repro steps are in the report. Own commit. The repro must fail at `ed8b208` and pass at your head.
4. **RE-SHOOT the listing screenshots** (Kam ruled it). About six, one per caption, 1280×720, on the **synthetic demo feed** so no real names appear and no blurs are needed: overview KPIs and charts · Fleet Health consumables · AI assistant answer · cost-centre report · Sustainability · setup wizard at Log Analytics or User Access with identifiers masked. Update the captions in `docs/marketing/MARKETPLACE_LISTING_ASSETS.md` to match. S52 noted the synthetic feed sits inside the Log Analytics branch (`server.js:3633`) and probably needs `USE_AZURE_LOG_ANALYTICS=true` — not tried. **Replaced images are quarantined, not deleted.** Any browser you drive is fingerprinted as this Mac first.
5. **DRAFT SUBMISSION ZIP** from your final head, built from a clean `git archive` extract — never `2_Project_Files`. **`AZURE_MARKETPLACE_SUBMISSION_PACKAGE.md` disagrees with itself**: section 1 lists `azure-marketplace/mainTemplate.json` and an App Service `app.zip`; section 3 says `azure-marketplace/combined/mainTemplate.json` and the application container. **Establish from the template the build actually uses which shape is current, report the disagreement, and do NOT edit the document to make it agree.** Put the zip and a manifest of its contents in an evidence folder, labelled DRAFT, pending re-gate.
6. **STOP at READY FOR QA.** Your commits move the head off the gated SHA; Tuesday commissions the re-gate before Kam submits.

Report which of the QA report's m2 and m3 findings, and REPORT-S52 section 5's items, should be ticketed. **Search the board before proposing any; file nothing this session.**

## RULED BY KAM, NOT YET IN AN ARTEFACT

- `nexusai-marketplace-screenshot-reshoot` — **reshoot** — *"Yes - a new series of about six, on synthetic data"* (panel 2026-09-10 19:42). Timing made explicit 2026-09-11 08:06: before the package. Lands in: the new images and the caption commit.
- `nexusai-authorized-users-md-remove` — **keep** — *"Keep it for now - it ships in tomorrow's build"* (19:43). Lands in: your report. **KEEP docs/Authorized_Users.md** — it stays and ships.
- `nexusai-main-tree-is-a-stale-snapshot` — **investigate** — *"Keep the tree as-is until the mechanism is explained, then restore"* (10:48 and 20:15). Lands in: your report — `2_Project_Files` untouched.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- Item 3 (the names in `backend/llm/tools.js`, the demo usernames) is Kam-ACCEPTED: do not change them or re-raise them.
- No merges, no deploys, nothing to Partner Center.

## HOLDS

- **NEVER PUSH TO MAIN.** A push to `main` deploys the demo VM.
- **SUBMISSION IS KAM'S.** Nothing goes to Partner Center.
- **KEEP docs/Authorized_Users.md.**
- **No `az`, no `gh`.** If a step needs either, stop and ask Tuesday.
- **Never reproduce a secret value, prefix or length. Never `rm`** — quarantine.
- **Mail `tuesday-agent@agentmail.to`**: plan confirmation, questions, READY FOR QA, wrap. Not `wednesday-agent@`.

## REPORT

Per queue item: what changed (commit SHAs), the evidence (command, output, control), what was not tested. Lead with whether the draft zip exists and what it contains.

PROVENANCE:
Kam's 08:06 ask, verbatim | panel relay mails to tuesday-agent@ 2026-09-10T22:06:38Z and 22:06:48Z | read 2026-09-11
branch at ed8b208, clean, not on origin; origin main cd2b543 | git rev-parse, status and ls-remote in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed | read 2026-09-11
QA verdict GO with findings; M1 at server.js:15961; m1, m2, m3 | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-10-s51-mktremed-ed8b208-tier1/report.md sections 0 and 2 | read 2026-09-11
deploy-demo fires on main only | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed/.github/workflows/deploy-demo.yml at ed8b208 | read 2026-09-10
the package document disagrees with itself | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed/AZURE_MARKETPLACE_SUBMISSION_PACKAGE.md sections 1 and 3 | read 2026-09-11
the three Kam rulings and their choices | decision_queue.sh show in /Volumes/KK_T9_External_HDD/TUESDAY | read 2026-09-11
synthetic feed note | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s52-marketplace-verification/REPORT-S52.md section 3 | read 2026-09-10

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 08:18
