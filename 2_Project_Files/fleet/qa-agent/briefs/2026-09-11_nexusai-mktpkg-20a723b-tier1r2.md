# QA GATE — TIER 1, round 2 of 2 — Datasec/NexusAI, the Marketplace submission package

**Head under test:** `s51-marketplace-remediation` @ `20a723b1fbdc5afeb2a1a3bd316d30689f75146b`, on origin (S53 pushed `ed8b208..20a723b`; `main` untouched at `cd2b543`). Worktree: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed`, clean (Tuesday read it with `git --no-optional-locks` at 09:1x).
**Range under test:** `ed8b208..20a723b`, 5 commits: `4e12089` M1 · `923c265` m1 · `45589c6` listing screenshots re-shot · `e65a0c5` suite counts · `20a723b` HISTORY.
**Also under test:** the DRAFT submission package at `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/evidence-s53-marketplace-package/DRAFT-submission-package-20a723b/`. It holds `DRAFT-pending-regate_plan-managed-ai_20a723b.zip`, `DRAFT-pending-regate_listing-assets_20a723b.zip` and `MANIFEST.txt`. **Read those files; never modify, move or rebuild them in place.**

PRIOR ROUND: round 1 gated `ed8b208dccccb74d449227e3b968eab1b30bd0f5`, verdict **GO — with findings**.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-10-s51-mktremed-ed8b208-tier1/`
Findings carried forward and their disposition: **M1** (client secret logged by the data-source save) fixed on `4e12089` · **m1** (Back-navigation ghost value) fixed on `923c265` · **m2** (the `AADSTS90002` error text carries the full tenant ID) unchanged, deferred for ticketing · **m3** (secret-class names outside the `.dockerignore` rules) unchanged, deferred for ticketing.

## WHY TIER 1
A secret-logging fix in the product, and **public listing assets plus the technical package that Kam uploads to Partner Center himself**. That is a security surface plus a human handover. **Round 2 of 2 under the cap:** a NO GO here goes to Kam as the list of what blocks upload, and there is no round 3 without his word.

## WHAT KAM ASKED — his words (panel, 2026-09-11 08:06)
> *"is the Nexus AI zip file for Azure Marketplace submission ready?"* · *"Don't forget all the screenshots and everything else."*
**Kam's rulings that bind this round:** `fix-first` on M1 (08:18: *"Fix it before the zip is built"*) · `reshoot` the listing screenshots (2026-09-10) · **KEEP `docs/Authorized_Users.md`** (2026-09-10 19:43; it ships, so do not report its presence) · the AI screenshot card `nexusai-ai-screenshot-local-model` is **UNRULED**, so `rd15-03` keeps its older blurred image by default (not a finding in itself).

## THE BUILDER'S CLAIMS — verify each, relay none (S53's READY FOR QA mail, 23:12:42Z)
1. **M1:** the `POST /api/setup/data-sources` log now carries `{ name, authMode, workspaceId masked, hasServicePrincipal }`; the pre-test note masks GUIDs to the first 8 and last 4 characters. Red-proof `m1-log-redproof.sh`: `ed8b208` gives 1 secret line, 2 tenant, 1 client, 1 workspace; `4e12089` gives 0/0/0/0. New cell `__tests__/data-source-save-log-redaction.test.js`: 2/4 fail at `ed8b208`, 4/4 pass at head. **S53 did NOT test a Docker container's log.**
2. **m1:** after Back the field is empty, the code reads empty, and the required error agrees; the masking control is intact (30 bullets + tail visible; code reads the full value). 8 jsdom cells. **Not tested:** Back after a saved config; Safari or Firefox.
3. **Screenshots:** rd15-01, -02, -04 and -05 re-shot plus NEW `listing-06-sustainability.png`, at 1280x720, DPR 1, on the synthetic feed, with fictional people only; captions rewritten; originals quarantined; PNG chunks are IHDR/IDAT/IEND only.
4. **`npm run verify`:** VERDICT PASS, 2312/2312 across 120 suites.
5. **The zips** were built from a clean `git archive` extract. The plan zip carries `mainTemplate.json`, `createUiDefinition.json` and `viewDefinition.json` at its root, each sha256-equal to its git blob. The listing zip carries 17 files, all sha256-equal to git.

## 🔴 WHAT TO ATTACK FIRST
1. **THE SECRET IN THE CONTAINER.** Customers run the IMAGE, not `node` on a Mac. Build `--target production` at `20a723b`, run it, perform a real data-source save carrying a synthetic client secret, and read `docker logs` for the secret, the tenant, the client and the workspace IDs. Include a control that proves your instrument finds a planted value in that same log. Also: does any OTHER log line on that path (error, retry, pre-test failure) still print the body?
2. **THE PACKAGE IS WHAT KAM UPLOADS — open everything in it.** For every file in both zips: is its sha256 equal to `git show 20a723b:<path>`? Is there anything present that git does not hold, or held by git and missing? Is any secret-class file present? **Open every PDF and read every embedded image and its metadata** for real names, surnames, emails, tenant or company names. S53 itself says the **Datasheet PDF embeds a PRE-BLUR image**, so measure what that image shows. Check PNG/PDF metadata, XMP, thumbnails and trailing bytes.
3. **S53's THREE "BEFORE ANY UPLOAD" ITEMS — measure each and give it an evidence class:** (a) the Datasheet PDF's pre-blur embed; (b) the deployment wizard defaulting to the **publisher's dev ACR**. What would a customer's deployment pull, and from where? Read `createUiDefinition.json` and `mainTemplate.json`. (c) the pre-existing gitleaks hit at `PEN-TEST-REPORT:297`: is that file inside either zip or the image?
4. **Screenshots:** any legible real person or organisation at any zoom, in any of the 6 listing images **and** rd15-03. Do the captions describe what each frame shows?
5. **Partner Center shape, READ ONLY:** is the plan zip's root layout what a managed-application submission expects? Does `createUiDefinition.json` parse as valid JSON?

## HOW TO DRIVE IT
- **Never write into the NexusAI checkout, its `.git`, or the evidence folder.** Clone into your OWN `mktemp -d`: `git clone --no-hardlinks '/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/wt-s51-mktremed' "$T/repo"` and check out `20a723b1fbdc5afeb2a1a3bd316d30689f75146b` there. Copy the zips into your temp dir before unzipping.
- `npm ci && npm run verify`: **read the VERDICT line, not the exit code.**
- **Docker is shared on this Mac** (another Datasec seat's gate ran on it this morning). Remove only images and containers YOU built, and say so. Use ports outside 3531–3560 and 18080.
- **Browser:** a local server of THIS commit on a fresh data directory (S53's recipe is in its READY mail: `DATA_DIR`, `DB_PATH`, `PORT`, `NODE_ENV=development`, `COOKIE_SECURE=false`, a random `SESSION_SECRET`; for screenshot surfaces add `SYNTHETIC_DEMO_FEED=true USE_AZURE_LOG_ANALYTICS=true SEED_DEMO_DATA=true`). **Fingerprint any extension-driven Chrome** against this Mac first; prefer a headless driver that is provably local.
- **`2_Project_Files/` in the NexusAI project is a Kam-ruled keep-as-is snapshot.** Do not build from it or touch it.

## KNOWN — do NOT report as new
- m2 and m3 from round 1 (deferred, above). **First-run completion leaves the dashboard open without Entra until Enforce runs.** The Enforce step shows an error after it succeeds. `docs/Authorized_Users.md` ships (Kam: keep). `rd15-03` is the older blurred image (card unruled). An unsaved identifier does not survive Back (accepted as privacy).

## WHAT WOULD MAKE THIS A NO GO FOR UPLOAD
- A secret, or a full tenant/client/workspace ID, in the container log on the data-source save path.
- A legible real name or real organisation, or PII, in any listing asset: PNG, PDF, an embedded image or metadata.
- A file in either zip that differs from git at `20a723b`, or a secret-class file inside either zip.
- `npm run verify` not reporting PASS, or the masking control regressed.
- A deployment wizard that makes a customer's deployment depend on a Datasec DEV registry. **Measure it; the priority call on it is Kam's.**

## CONTROLS THIS GATE OWES ITSELF
**Every zero gets a control that would have produced a non-zero, run in the same action.** An instrument that cannot reach its case is marked **NOT TESTED** with the blocker. Every action recommendation carries **MEASURED AT RUNTIME · PROBED · READ ONLY**. Every finding carries FOUND / TESTED / HOW. **Never `rm`**: one `mktemp -d` per attempt. Report head readings at start, mid and end, with the branch beside each SHA.

## YOU ARE FINDINGS-ONLY
Never fix, re-shoot, rebuild the zip, commit or file tickets. Report. Grade Blocker / Major / Minor.

## 🔴 MAIL YOUR VERDICT
Report on disk: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-11-mktpkg-20a723b-tier1r2/report.md`. **Send the verdict to `tuesday-agent@agentmail.to`**, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace package @ 20a723b (tier 1, round 2)`. **Lead with GO, GO WITH FINDINGS or NO GO FOR UPLOAD.** **NOT `wednesday-agent@`.** You have no inbox, so a verdict you do not mail is lost.

PROVENANCE:
- claims 1-5, the DRAFT paths and the three before-upload items | datasec-nexusai READY FOR QA 2026-09-10T23:12:42Z + Session wrap 23:13:03Z, spf/dkim/dmarc pass | read 2026-09-11
- range ed8b208..20a723b (5 commits) and HEAD == branch == 20a723b | git --no-optional-locks log/rev-parse on wt-s51-mktremed by Tuesday | read 2026-09-11
- round 1 verdict and findings M1/m1/m2/m3 | round-1 report.md headings | read 2026-09-11
- Kam's 08:06 asks and 08:18 fix-first | kam_rulings_today.sh | read 2026-09-11
- KEEP Authorized_Users, reshoot, AI card unruled | NEXT-PICKUP-TUESDAY.md + decision_queue | read 2026-09-11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-11 09:15
