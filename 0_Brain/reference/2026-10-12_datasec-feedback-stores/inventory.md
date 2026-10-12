---
date: 2026-10-12
type: reference
source: read-only Explore subagent commissioned by Tuesday s103 (file:line evidence inside); not re-verified line by line by Tuesday
status: live
---

I found five places where user feedback for Datasec products is stored, plus the Tuesday inbox that gets copies by email. Only NexusAI has a sweep script that reads its live store. QuickQuote's stored items need Azure credentials. The one QuickQuote item I could read without credentials is in Tuesday's own notes, not in a Datasec project.

D = `/Volumes/KK_T9_External_HDD/!CODING/Datasec`

## Feedback stores

**1. QuickQuote, hosted version (Vision_Sales_Portal)**
- **Collects:** bug, feature or feedback text from signed-in users, with context (tool version, mode, devices, term, currency, grand total). `stage3/server.js:743`
- **Endpoint:** `POST /api/feedback` at `server.js:767`. Each item is saved to the Azure Table Storage table `feedback` (partition `fb`, newest first) at `stage3/lib/store.js:20,60-90`, and mailed at `server.js:796-811`.
- **Email:** To `kreiser.org@me.com`, CC `tuesday-agent@agentmail.to`, subject `QuickQuote feedback (${type}) from ${email}`. Default recipients at `server.js:167`; an env override exists at `:247`.
- **How to read the stored items:**
  - Through the app: `GET /api/feedback` returns 200 items, but only in an "advanced" session (`server.js:818-828`).
  - Directly: the table needs `TABLES_CONNECTION_STRING` (`store.js:10`). The storage account is in resource group `hpas-quickquote-rg` (`D/Vision_Sales_Portal/CLAUDE.md:104-110`). I did not find its name or credential path in the files I read.
- **Sweep script:** none. **New-since marker:** none in the store.
- `server.js` and `store.js` are under `D/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool/`.

**2. Vision Sales Portal (main portal)**
- **Collects:** feedback widget items (type, title, description, page URL, priority, triage status).
- **Store:** PostgreSQL table `feedback` on `datasec-sales-db.postgres.database.azure.com`. Table created at `2_Project_Files/server/routes/feedback.js:25`, insert at `:175`.
- **Endpoints:**
  - `GET /api/feedback/report` returns open and in-progress items (`:83`). No `requireAuth` on that route. I did not check whether a global gate sits in front of it.
  - `/summary` at `:133`.
  - `GET /api/feedback/coordinator-state` needs an `X-Coordinator-Secret` header (`:344`).
- **Email:** one mail per item, subject `Vision feedback #<id> (<type>): <title>`, to Kam with Tuesday CC'd (`server/feedbackNotify.js:25,75`).
- **Hourly digest:** written to `2_Project_Files/generated-docs/feedback-digest-latest.json` (`server/feedbackDigest.js:1-13`).
- **Credentials:** `D/Vision_Sales_Portal/4_Credentials/.env` (`DATABASE_URL`) and `4_Credentials/accounts.md` (`CLAUDE.md:117-120,141`).
- **New-since marker:** yes. The DB table `feedback_coordinator_state` holds `sentItemKeys` and `lastPollAt` (`routes/feedback.js:331-363`).
- **Sweep script:** none.

**3. NexusAI (Reporting Dashboard)**
- **Collects:** human feedback items, plus items auto-created by the AI audit (`backend/server.js:180-211`).
- **Endpoint:** `/api/feedback` (`server.js:20868`).
- **Store:** `settings.json['feedbackItems']` on Azure file share `nexusai-data`, storage account `stnexusaidmjy25ipoih5eo` (`2_Project_Files/scripts/feedback-sweep.sh:35-38`).
- **Sweep command:** `cd D/NexusAI/2_Project_Files && ./scripts/feedback-sweep.sh` (`D/NexusAI/CLAUDE.md:345-368,381`). It is read-only, always exits 0, and prints `UNAVAILABLE` rather than 0 if it cannot read the store.
- **Credentials:** `D/NexusAI/4_Credentials/.azure` (`AZURE_CONFIG_DIR`, read via `--auth-mode key`) and `D/NexusAI/4_Credentials/.env` (`JIRA_API_TOKEN`) (`sweep.sh:52-56`).
- **New-since marker:** none. It reports the newest timestamp and which item ids no RD Jira ticket mentions (`sweep.sh:113-198,215`).

**4. HPSM Policy Composer** (this is the main HPSM product, not HPSM-POC)
- **Collects:** tenant users' feedback items plus attachments.
- **Store:** Postgres tables `feedback_item` and `feedback_attachment` (`D/HPSM/6_Policy_Composer/packages/db/migrations/0016_feedback.sql:14,71`). API at `apps/api/src/routes/feedback.ts`, registered at `app.ts:145`.
- **Status:** live on Azure since S45 (`D/HPSM/CLAUDE.md:348`).
- **Sweep command:** `scripts/feedback-sweep.sh --edge http://127.0.0.1:<port>`. It only accepts a local stack's address (`feedback-sweep.sh:46-52`), so **the live Azure store has no sweep**. It signs in as the stack's mock platform-admin, so no credential file is needed. The Jira check is unavailable (`:16-18,58-63`).
- **New-since marker:** none. It reports newest, past-retention and untriaged items.
- **Email:** none. I found no agentmail or notify code under `apps/`.

**5. Feedback_System** (a framework, not a store)
- **What it is:** a coordinator (port 4900) that polls each app's `/api/feedback/report`, plus a drop-in Express feedback module, with Telegram triage (`D/Feedback_System/CLAUDE.md:6-21`).
- **Not set up:** only `projects.example.json` exists, `4_Credentials/` is empty, and there are no Azure resources.
- **New-since marker:** `sentItemKeys` is held in memory only (`packages/coordinator/telegramBot.js:24,95`). It persists only through Vision's state table (store 2).
- I see no evidence the coordinator is running anywhere.

**6. Email inbox `tuesday-agent@agentmail.to`** (receives copies from stores 1 and 2)
- **How to read:** `bash /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/inbox_digest.sh` (header at `:1-21`, inbox set at `:46`).
- **Credential:** `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (`:32`).
- **New-since marker:** yes, `fleet/state/seen_ids.txt` (`:28,82`).

## Excluded or not stores
- **HPSM-POC, the Security Configuration tool, the MPS Calculator:** I saw none of these by name. I did not look for them specifically.
- **`D/Security Review/Source_Code/Reporting_Dashboard_Au-main/`:** a static copy of the NexusAI source code (it has the same `routes/feedback.js`), not a live store.
- **NexusAI local backups:** `D/NexusAI/4_Credentials/demo-share-backup-*/settings.json` probably hold old NexusAI feedback items. They sit in a credentials folder, so I did not open them.
- **No feedback store found in:** ATTIO, Commercial Readiness, CypherKey (its matches are SMS/SAML code), Lead_Bot, Marketing_Collateral, myPKI (backlog wording only), RESEARCH, Task_Dispatcher, Websites.

## QuickQuote items readable without credentials
- **One item**, in Tuesday's notes rather than a Datasec file: `/Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/projects_index/clarifications_register.md:24`. From john.spears@datasec.com.au, 2026-09-22T02:07Z, v2.30: rename "Devices (MFPS)" to "Devices (MFPS/SFPS)".
- **CAD-currency request:** `NEXT-PICKUP-TUESDAY.md:16` mentions a CAD-currency request from John Spears (mail dated 10-09). I did not find the item text.
- **No local copy of QuickQuote items exists.** Reading the rest needs either the Azure table connection string (store 1) or the agentmail key plus the inbox script (store 6). I stopped there.
- **Vision's local digest file is test data:** its only item is "ZZSECRETFB title" (2026-09-28).

## Not found or not read
- The QuickQuote storage account name and where its connection string is kept.
- Whether Vision's `/report` route sits behind a global auth gate.
- Any live database or table contents, and no item counts for stores 1 to 4.