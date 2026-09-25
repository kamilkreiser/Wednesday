# BLUF — NEW SEAT Datasec/NexusAI-L: PREPARE a full CUSTOMER test of the LIVE NexusAI Marketplace listing, deployed from the store into a SEPARATE tenant, exactly as a customer would. This round is PREPARATION ONLY: nothing is created, bought or logged into until Kam has logged in to the new tenant and Tuesday gives the GO. End at READY TO DEPLOY with the plan, a cost estimate and a tested login procedure.

**Addressed to the cockpit seat `Datasec/NexusAI-L` only.** No other NexusAI seat is live.

## AUTHORITY
- Kam, terminal, 2026-09-25 ~14:5x AEST, verbatim: *"The Nexus AI offer is live on the marketplace. Can you please set up a full customer test environment in Azure and then deploy the app from the store for testing purposes? I'd like to use a different tenant for this, so get me to log in to that tenant when you're ready."*
- Which tenant is Kam's call: card `nexusai-customer-test-tenant-choice` is on his board, with (a) a brand-new tenant plus a pay-as-you-go subscription recommended, or (b) an existing spare tenant. Plan for EITHER. The tenant id arrives in a Tuesday ANSWER.
- Also record, as a new C-number in CLARIFICATIONS, Kam's words that the offer is LIVE (the 2.2.0 resubmission: package commit 3464dd8, image sha256:fdda3309…7f66). Read the live listing to confirm the version it serves, and do not assert it from memory.

## HARD BOUNDARIES
- **NEVER** use any Datasec environment for this: not the corporate tenant ae7a1e46, not the agent-controllable tenant d500ebad (subs 0c57ab37 / 29b5c7de), not dev, not the sales demo. The whole point is a clean customer view. If any command would touch them, STOP.
- **A SEPARATE `AZURE_CONFIG_DIR`**: `4_Credentials/.azure-customer-test` (gitignored). Never the project's normal `.azure`. Every `az` command in this work runs with that dir, and `az account show` is checked before each one.
- **Kam logs in, not you.** Prepare `az login --use-device-code --tenant <id>` so the device code and URL can be posted to Kam's board (he is travelling and will enter it from his phone). Do not run it until Tuesday says the tenant id is known.
- **Money:** the Marketplace plan's price plus the Azure resources the template creates is spend on Kam's card = his signature class. Your plan must give the COST ESTIMATE (the plan's listed price, read from the live listing, plus the template's resources at list price per hour/month) so Tuesday can confirm it with him before any purchase.
- No merges, no pushes to main, no changes to the listing or Partner Center, nothing to any human but Tuesday.

## DELIVERABLE (READY TO DEPLOY → tuesday-agent@)
A plan document in the repo (a new branch, pushed): `docs/resubmission/2026-09-25_customer-test-plan.md`, containing:
1. Prerequisites the customer tenant needs (subscription, resource providers to register, the Entra app / security group the wizard asks for, quotas, the Azure OpenAI decision if the plan needs it). Measure each from the template and createUiDefinition at 3464dd8 and the live listing, not from memory. State the instrument.
2. The exact customer path: the Marketplace URL → Create → every wizard field and the value we will use → deploy → first-run setup → sign-in.
3. What we will TEST once it is up: the C-58 / 4a NOT-VERIFIED items (the Key Vault success path C-124, a real-Azure deployment C-20, anonymous image pull from the customer's subscription, first-run lock, sign-in with the customer's own Entra), each with its pass criterion.
4. The COST ESTIMATE, and the TEARDOWN steps (resource group delete, subscription cancel if new), which are Kam-approved separately.
5. The login procedure, dry-run as far as possible without logging in (the config dir exists, is empty, and is gitignored).
PRIOR-WORK CHECK: read docs/MARKETPLACE_TEST_PROCEDURE.md, the handover doc (c5da4d4), HANDOVER-S81J.md and the CLARIFICATIONS on C-20, C-58, C-69 and C-124 first. Much of this plan may already exist.

## PLAN CONFIRMATION
Mail `[Datasec/NexusAI-L -> Tuesday] QUESTION: plan confirmation` and start the read-only preparation without waiting.

PROVENANCE:
- Kam's words | this seat's terminal, 2026-09-25 ~14:5x AEST | read 2026-09-25
- package 3464dd8 / image fdda3309…7f66 / branch c5da4d4 | the package gate verdict mail 03:04Z and Tuesday's own ls-remote | read 2026-09-25
- Datasec environments and tenants | /Volumes/KK_T9_External_HDD/CLAUDE.md hard rule 4 | read 2026-09-25
Self-check note: re-read whole; nothing is created, bought or logged into in this round.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 14:55
