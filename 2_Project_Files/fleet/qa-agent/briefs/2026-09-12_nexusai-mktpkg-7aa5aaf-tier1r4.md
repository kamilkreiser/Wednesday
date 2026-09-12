# QA GATE — TIER 1, round 4 (Kam-authorised) — Datasec/NexusAI Marketplace package @ 7aa5aaf

**Kam ruled round 4 at 08:50:53 AEST, verbatim: *"Yes - round 4 - make the deployed product GPT-only (wizard sets GPT, setup save works, Phi-3/Ollama removed), mask the tenant IDs, then re-check"*.** Behind it, his note of 2026-09-11 15:00, verbatim: *"Nexus II needs to be launched to the marketplace with GPT as its only option."* **You are that re-check, and your verdict decides whether this package goes to Kam as ready for upload.** **Head:** `s51-marketplace-remediation` @ `7aa5aaf646b9c89cffde6180f3adc7cfd1a2a203` (on origin; local == origin; `main` is `ae2588b`). **Range:** `b8c4646..7aa5aaf`, **10 commits**. **DRAFT package:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s56-marketplace-package/DRAFT-submission-package-7aa5aaf/` (two zips + `MANIFEST.txt`; copy the zips into your temp dir before unzipping). **This round runs on Kam's word beyond the cap; there is no round 5 without Kam.**

PRIOR ROUND: round 3 gated `b8c4646ab7d271567364876757403bfb8d23cf08`, verdict **NO GO FOR UPLOAD** (1 new Blocker NEW-1, 1 new Major NEW-2, 2 new Minor NEW-3/NEW-4, plus B2 carried).
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-b8c4646-tier1r3/report.md`
Dispositions (builder claims): **NEW-1** fixed (`3ac2b6b` server, `bb3f89a` package) · **item 2, GPT-only offered/default** (`4db1c6c`, `68d0d49`) · **NEW-2** fixed (`df53270`) · **NEW-3, NEW-4** to BACKLOG, NOT fixed (`3061dfd`) · **B2** untouched (Kam's registry word).

## Everything in round 3's and round 2's briefs still applies, with these changes
- Round 3: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_nexusai-mktpkg-b8c4646-tier1r3.md` · round 2: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-11_nexusai-mktpkg-20a723b-tier1r2.md`.
- Clone the worktree and check out `7aa5aaf646b9c89cffde6180f3adc7cfd1a2a203`; **`b8c4646` is the red control.**
- **The builder's READY FOR QA pack** is `evidence-s56-marketplace-package/` (instruments adapted from your round-3 `runU.sh`/`aoai-ui.cjs`, the census classifiers, `C-container/` runs, `G-gitleaks/`, `Z-CLEANUP-docker.txt`). It is a claim, not evidence you rely on. **Never write into it or into the NexusAI checkout.**
- Pick your own ports; S56 used 3701–3722 and reports 0 listeners there. The Docker daemon is shared: remove only the containers, images and volumes YOU create.

## THE BUILDER'S CLAIMS — verify each, relay none (S56 READY FOR QA 2026-09-12T00:14:51Z, spf/dkim/dmarc pass)
1. **NEW-1:** the real `/first-run-setup` in headless Chrome 153 (playwright-core), template-shaped env, a synthetic endpoint, `gpt-4.1`. Save → "Configured", still Configured after a reload; `/api/setup/ai-model` → `provider: azure-openai`; `settings.json` key stored `ENC:`; after `docker restart` the log reads `LLM hydrated from jsonStorage: azure-openai`; `ollama (phi3:medium)` 0 times. **The same result with `LLM_PROVIDER` removed from the env.** Round 3's failure reproduced at `b8c4646`. Also found and fixed: `GET /api/setup/ai-model` read only env; `#ai-continue` did not exist; `POST /api/setup/ai-test` tested ollama whatever it was sent.
2. **Item 2 (GPT-only):** a static census, classes D/R/V/L = 0 at head (16/16/13/1 at `b8c4646`) with a planted control; 217 lines of ollama/onnx adapter code reported as their own labelled class (Tuesday ruled ⚑B Option 1: the code stays, reachable only by an explicit `LLM_PROVIDER`); a runtime census of 9 served responses with 0 non-GPT and 0 VM mentions (61 and 17 at `b8c4646`); S54's `item5-enumerate.cjs` re-run unchanged.
3. **NEW-2:** your K3 run shape with your `stub2.cjs` unchanged: full tenant IDs 0 in `docker logs`, `combined.log`, `error.log` and all 3 discover responses at head; red at `b8c4646`.
4. **`npm run verify` at `7aa5aaf`:** PASS 2401/2401 across 127 suites; counts moved only through `--update-counts`.
5. **⚠ `9d454d8` changed four test files** after 8 tests went red: an isolation fix in `security-fixes.test.js`, and the first-run page DOM baselines (visible text nodes 974 → 951, light failure set 138 → 135), explained node by node in `DOM-baselines-explained-first-run-b8c4646-vs-head.txt`. The builder says none was weakened.
6. **Zips** from a clean `git archive` of `7aa5aaf`: the plan zip's 3 entries each equal their git blob; the listing zip's 15 entries equal git; `LLM_PROVIDER=azure-openai` unconditional in the zipped template; the wizard's AI step (4 outputs, key as a PasswordBox, rule accepts `gpt-4.1`); B2 defaults identical to `b8c4646`; gitleaks v8.30.1 in docker: tree 1 (the known baseline), range 0, zip contents 0.

## DEPARTURES and OPEN items — yours to grade
- **The builder's image proof ran on an image built at `955629f`, not `7aa5aaf`**; it says `git diff --name-only 955629f..7aa5aaf` is `BACKLOG.md HISTORY.md` only. Verify that. Any image you build, build from `7aa5aaf`.
- **OPEN, READ ONLY by the builder:** the saved-AOAI hydrate at boot sits inside the `USE_AZURE_LOG_ANALYTICS` branch of `initDataSource`. A package deployment always sets that variable (MAJ-3); a run without it was not measured.
- **New items the builder BACKLOGged — grade whether any stops upload for a GPT-only Marketplace offer:** `GET /api/models` answers 500 on every request (pre-existing); until AOAI is connected, every boot logs 13 `azure-openai query error … set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY env vars` lines, a remedy a Marketplace customer cannot use; with a saved but unreachable endpoint, warmup takes ~18 s and health answers at ~24 s (6–9 s at `b8c4646`); the first-run page still carries App Service instructions (`az webapp …`).
- **Builder NOT TESTED:** a real Azure OpenAI resource (the synthetic endpoint fails DNS); `createUiDefinition` rendered in the portal or its sandbox; ARM TTK or `az deployment validate`; the Container Apps instructions run; other routes that return Azure error text to the page; enforced auth; the Log Analytics 404 shape.

## 🔴 WHAT TO ATTACK FIRST
1. **NEW-1, your own way:** your round-3 `runU`/`aoai-ui` method on an image built from a `git archive` extract of `7aa5aaf`: Save, reload, restart, the hydrate line, your own counts. Then the negative paths round 3's defect lived on: an invalid endpoint format, a missing key, a failed Test followed by Save, a re-save to a different deployment name. **Does the UI ever show "Configured" when nothing was saved?**
2. **GPT-only, as a customer meets it:** your own census over the served responses and the first-run page, including any path the builder did not list. **Can a customer on a package deployment reach ollama or onnx at all** through anything they control (the wizard, the in-app settings, the API)? The template sets `LLM_PROVIDER=azure-openai` unconditionally, so say what, if anything, overrides it.
3. **NEW-2:** your K3 run unchanged at head, then the wider class the builder names as NOT TESTED: other routes that return Azure error text to the page. Does any leak a full tenant or workspace id?
4. **The re-pinned tests (`9d454d8`):** read each change against its explanation. A baseline re-pin that hides a real regression is a Major.
5. **Boot and health timing:** read the template's Container Apps probe configuration and say whether ~24 s to a healthy answer, with a saved unreachable endpoint, risks a probe restart loop on a real deployment. Measure it if you can.
6. **The zips:** every entry sha256 == `git show 7aa5aaf:<path>`; 3 + 15 entries; OPS-002 and MKT-002 still absent; the wizard JSON parses and its regexes compile; gitleaks as CI runs it.

## KNOWN — do NOT report as new
B2 (the dev registry default; Kam's word pending) · MIN-4 (owner name and email in the Datasheet text; Kam's) · `rd15-03` keeps a readable first name (Kam's card) · `docs/Authorized_Users.md` ships (Kam: keep) · the gitleaks baseline `docs/PEN-TEST-REPORT-2026-04-25.md:297` · NEW-3, NEW-4 (BACKLOG) · **the ollama and onnx-local adapter code remains in the image, unreachable on a package deployment** (⚑B Option 1, ruled by Tuesday; removal is BACKLOG) · 109 direct `console.*` calls bypass winston · the NexusAI main tree is a stale snapshot · the `backend/llm/tools.js` demo names (Kam-accepted) · 4 Dependabot alerts on `main`.

## Output
Findings-only. FOUND / TESTED / HOW plus an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY) on every finding; a control for every zero; never `rm`; head readings at start, mid and end. **Run long commands in the FOREGROUND; never end a turn waiting on a background notice.** **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-mktpkg-7aa5aaf-tier1r4/report.md`. **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace package @ 7aa5aaf (tier 1, round 4)`. Lead with GO, GO WITH FINDINGS or NO GO FOR UPLOAD, and **say in one sentence whether the package is ready for Kam to upload, and what besides B2 (if anything) stops it.** **Never `wednesday-agent@`.** You have no inbox.

PROVENANCE:
- Kam's round-4 ruling verbatim | kam_rulings_today.sh 2026-09-12 (08:50) + panel relay mail 2026-09-11T22:50:54Z | read 2026-09-12
- Kam's GPT-only note verbatim | kam_rulings_today.sh 2026-09-11 (15:00) | read 2026-09-12
- head 7aa5aaf, 10 commits on b8c4646, local == origin, worktree clean, main ae2588b | git rev-parse / rev-list / status on wt-s51-mktremed + git ls-remote, run by Tuesday s9 | read 2026-09-12
- claims 1-6, departures, open items, BACKLOG items, NOT TESTED | datasec-nexusai READY FOR QA 2026-09-12T00:14:51Z, spf/dkim/dmarc pass | read 2026-09-12
- round-3 verdict NO GO FOR UPLOAD, NEW-1..NEW-4, B2 carried | round-3 report.md lines 3-27 | read 2026-09-12
- DRAFT package zips + MANIFEST present | ls of DRAFT-submission-package-7aa5aaf, run by Tuesday s9 | read 2026-09-12
- ⚑B Option 1 ruling | Tuesday ANSWER 2026-09-11T23:07:23Z (briefs_staged/2026-09-12_nexusai-s56-answer-plan.md) | read 2026-09-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-12 10:18
