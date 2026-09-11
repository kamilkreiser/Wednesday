# ROUND 3 — Datasec/NexusAI Marketplace package, on Kam's word

**BLUF.** The round-2 tier-1 gate on `20a723b` said **NO GO FOR UPLOAD**. **Kam ruled round 3 at 14:59:37, verbatim: *"Yes — fix B1, MAJ-1, MAJ-2 and MAJ-3, then re-gate; the registry waits for your word"*.** This session fixes exactly those four, rebuilds the DRAFT zips, and **stops at READY FOR QA.** **B2 (the wizard's default container registry) is NOT in scope:** Kam has not named a registry, so leave `createUiDefinition.json`'s image and registry defaults unchanged, and build or push no image.

## READ FIRST
The round-2 report, the source (do not work from this brief's summary): `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2/report.md`, sections 0 and 2 (B1, MAJ-1, MAJ-2, MAJ-3), plus its NOT TESTED and Minors. Also S53's `HISTORY.md` entry and `evidence-s53-marketplace-package/` for how the package was built.

## QUEUE (worktree `wt-s51-mktremed`, branch `s51-marketplace-remediation`, head `20a723b`)
1. **B1: Kam's full name in two listing assets.** Replace `docs/marketing/video/nexusai-demo-thumbnail-1280x720.png` with a frame from the synthetic feed. **Regenerate** `Final Documents/Working Documents/NEXUSAI-MKT-001_Datasheet_v1.1.pdf` so its page-3 image is the re-shot `rd15-01`. Quarantine the originals (never `rm`). **Proof:** extract the images (`pdfimages -all`, a 4x crop of the thumbnail header) and read them. No real person's name remains, and the report's own method reproduces the name at `20a723b` as a red control. **Keep the pre-change crops out of any evidence file**; they show the name.
2. **MAJ-1:** remove `NEXUSAI-OPS-002_Customer-Onboarding-Guide_v1.0.pdf` (internal, Confidential, retired VM plan) from the listing bundle, and fix the pointers that call it the customer's "Full guide" (`MARKETPLACE_LISTING_CONTENT.md`, `MARKETPLACE_LISTING_ASSETS.md`). **Drop it; do not write a new guide this round.**
3. **MAJ-2:** remove `NEXUSAI-MKT-002_ROI-Business-Case-One-Pager_v1.0.pdf` (marked draft, garbled example) from the listing bundle and fix its pointers. **Drop it; do not rewrite it this round.**
4. **MAJ-3:** a deployment from this package never sets `USE_AZURE_LOG_ANALYTICS`, so the saved Log Analytics config is never read. **Make a deployment that completes in-app setup actually read Log Analytics**, in the template or the product, with the smallest honest change, and **say which you chose and why**. **Proof:** the production image as the template configures it; save two data sources through the real wizard; restart the container; `/api/service-check` no longer reports `Local Database`, and the `Loading saved Log Analytics configuration` line appears. **Control:** the same run at `20a723b` reproduces the report's zeros. Real Azure is NOT available: the Azure call may fail at auth, and that is fine as long as the product ATTEMPTS it. Say exactly what was and was not reached.
5. **READ-ONLY, report only (Kam's note, panel 15:00:49, verbatim: *"Nexus II needs to be launched to the marketplace with GPT as its only option. No need for a VM with Fire 3."*, read as NexusAI and phi3):** enumerate every place the package, the wizard (`createUiDefinition.json`, `mainTemplate.json`) and the listing copy OFFER or MENTION an AI provider other than GPT/Azure OpenAI (Private AI, a local model, phi3, Ollama, a VM). Give file and line. **Change nothing for this item.** Tuesday takes it to Kam, because what the product offers is his call.
6. **`npm run verify` VERDICT PASS** (update counts only as the tool instructs). **Rebuild both DRAFT zips from a clean `git archive` extract of your new head** into a NEW folder `evidence-s54-marketplace-package/DRAFT-submission-package-<head7>/` with a MANIFEST. **Keep S53's folder untouched.**
7. **Push the feature branch** (never main), verify local == origin, then **READY FOR QA** to Tuesday with the head SHA (40 chars), the exact commit count in `20a723b..HEAD`, per-item FOUND / TESTED / HOW, and what was NOT tested. **Stop.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- `nexusai-marketplace-package-round3`: **round3** (panel 2026-09-11 14:59:37). Lands in: this round's commits and READY FOR QA.
- `nexusai-main-tree-is-a-stale-snapshot`: **investigate** (*"Keep the tree as-is until the mechanism is explained, then restore"*). Lands in: your report. **`2_Project_Files` stays untouched.**
- `nexusai-ai-screenshot-local-model`: Kam tapped **install-ollama** at 15:00:49, with the note above that points the other way. **Tuesday has asked him which he means. Until he answers: install NOTHING, and `rd15-03` stays unchanged.** Lands in: your report (item 5).
- `rd104-gh-identity-acceptance-false-premise`: **youcheck** (2026-09-07; Kam checks two GitHub settings pages himself). **Not this round's work.** It bears on merges, and this round merges nothing.
Delivered and standing: `reshoot` (done at `45589c6`), `keep` for `docs/Authorized_Users.md` (it still ships), `fix-first` on M1 (done at `4e12089`).

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- Item 3 (names in `backend/llm/tools.js`, demo usernames) is Kam-ACCEPTED; do not change it or re-raise it. The AI screenshot card (`nexusai-ai-screenshot-local-model`) is still unruled: `rd15-03` stays as it is. **Report that its "Kamil" stays readable, as the gate noted; do not change it.**
- No merges, no deploys, nothing to Partner Center, no image built or pushed.

## HOLDS
**NEVER PUSH TO MAIN** (it deploys the demo VM). **SUBMISSION IS KAM'S.** **KEEP docs/Authorized_Users.md.** **No az, no gh.** No container registry login or push. Never reproduce a secret value, prefix or length. **Never `rm`**; quarantine. Mail `tuesday-agent@agentmail.to` only (plan confirmation, questions, READY FOR QA, wrap).

PROVENANCE:
Kam's round-3 ruling verbatim | panel relay mail to tuesday-agent@ 2026-09-11T04:59:38Z | read 2026-09-11
Kam's AI-screenshot tap and GPT-only note verbatim | panel relay mail to tuesday-agent@ 2026-09-11T05:00:51Z | read 2026-09-11
B1, B2, MAJ-1..3 findings, file paths and the MAJ-3 chain | round-2 report.md sections 0 and 2, read by Tuesday | read 2026-09-11
head 20a723b on origin, branch s51-marketplace-remediation | datasec-nexusai READY FOR QA 2026-09-10T23:12:42Z + round-2 gate head readings | read 2026-09-11
Authorized_Users.md present at 20a723b; reshoot at 45589c6 | git ls-tree / git log on wt-s51-mktremed by Tuesday | read 2026-09-11
rd104 ruling youcheck; main-tree investigate | decision_queue.sh show / list ruled --undelivered | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 15:03
