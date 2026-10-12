# BLUF — Datasec/Vision_Sales_Portal: QUICKQUOTE FEEDBACK ROUND. Kam's instruction (live board, 2026-10-12 12:01:02, verbatim): "also, please look at feedback for quick quote tool and action." Read every QuickQuote feedback item, triage each, and send Tuesday a PLAN CONFIRMATION listing them, with what you propose to build for the actionable ones. Build NOTHING before Tuesday answers. Publishing a new QuickQuote version is Kam's decision, by card, and this brief does not cover it.

**Scope, read narrowly.** Kam paused Vision on 2026-09-29. Tuesday reads his 12:01 message as lifting that pause for QuickQuote FEEDBACK work only, and has told him so on the board, with an offer to correct it. The portal itself, ATTIO work and anything else in the backlog stay paused.

## READ FIRST (all in the Vision_Sales_Portal folder)
1. `CLAUDE.md` WHOLE, especially the QuickQuote section (resource group hpas-quickquote-rg; around lines 104-120) and the production boundaries.
2. Your own newest `5_Project_History/history.md` entry and `BACKLOG.md`, for the QuickQuote version on main and what is already queued.
3. The QuickQuote feedback code: `Quoting Tool/hpas-quoting-tool/stage3/server.js` (POST /api/feedback ~:743-811; GET /api/feedback ~:818-828, which needs an advanced session) and `stage3/lib/store.js` (Azure Table `feedback`, partition `fb`; ~:10, :20, :60-90).

## WHERE THE ITEMS ARE (from a read-only inventory Tuesday commissioned; your reads decide)
- **The store of record** is the Azure Table `feedback` in the QuickQuote storage account (needs `TABLES_CONNECTION_STRING`). The inventory could NOT find the account name or where the connection string is kept. Find it in your own credentials. If it is not there, say so in the plan confirmation; do not guess.
- **Copies** are mailed to Kam with Tuesday CC'd (subject "QuickQuote feedback (<type>) from <email>").
- **Two items Tuesday already holds** (copy them in, and verify them against the table):
  - john.spears@datasec.com.au, mail 2026-10-09 (feature): "Can we add 'Candadian Currency' to the drop down list, which is mathmatically nearly identical to AUD today based on current exchange rates?"
  - john.spears@datasec.com.au, 2026-09-22 (v2.30): rename "Devices (MFPS)" to "Devices (MFPS/SFPS)" (Tuesday's clarifications register).

## WHAT TO DO
1. List EVERY QuickQuote feedback item from the store: id, date, type, author, the text verbatim, and the QuickQuote version it was raised on. Then check each against main: is it already done, still open, or not reproducible? Give the instrument you used for each.
2. For each OPEN item, propose: build (files, tier, red-first cell), ticket only, or needs Kam (anything about pricing, rate cards, currency policy or what customers are shown). Say why. A currency addition touches pricing display, so state whether it needs Kam's word on the rate or exchange basis before it can be built.
3. Plan confirmation (below). Wait.
4. After Tuesday's answer: build the approved items, each with a PRIOR WORK section, red-first cells, your own verify, then READY FOR QA. Every change goes through the QA gate. Nothing is published or deployed without Kam's card.

## HOLDS (standing)
- PRODUCTION: the live QuickQuote and Vision Sales Portal are production. No deploy, no publish, no change to any Azure resource, no write to any production table. Reading the feedback table is the one production read allowed, using the narrowest credential you hold. Say which one you used.
- No reply to any feedback author. External comms are Kam's alone. Tuesday tells Kam what was done; Kam answers John.
- PRIOR-WORK CHECK before rebuilding/replacing/removing anything. Every READY carries PRIOR WORK + NOT TESTED.
- Never delete (move aside). Every factual sentence in a mail names its instrument, or says "unmeasured".
- Style: QuickQuote's own style guide/tokens only; no invented colours.

## RULED BY KAM, NOT YET IN AN ARTEFACT
- 2026-10-12 12:01:02, verbatim above: look at the QuickQuote feedback and action it. Write it into your project's 1_Project_Definition/CLARIFICATIONS.md (create it in NexusAI's format if it does not exist), and mail back the C-number.

## RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The 2026-09-29 pause stands for everything except this round.

PROVENANCE:
- Kam's instruction | live board via /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/tools/kam_rulings_today.sh (12:01 row) | read 2026-10-12
- store, endpoint and mail paths | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/reference/2026-10-12_datasec-feedback-stores/inventory.md (subagent's file:line citations, not re-verified by Tuesday) | read 2026-10-12
- CAD request text | tuesday-agent@agentmail.to message from john.spears, 2026-10-09T16:51 (inbox_digest) | read 2026-10-12
- MFPS/SFPS item | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/projects_index/clarifications_register.md line 24 (per the inventory) | read 2026-10-12
- Vision pause 2026-09-29 | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/daily_tuesday/2026-10-01.md line 25 | read 2026-10-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-12 13:09

## PLAN CONFIRMATION
Mail `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation` with your seat identity (pane id, cockpit name, claude pid), what you read, the full item list with each item's status and your proposal, and any launcher preflight warnings VERBATIM. Then wait. Your wake is Tuesday's mail plus a tap.
-- Tuesday
