---
date: 2026-08-28
type: research
source: Wednesday research agent (web, read-only)
for: Kam — ATTIO / Vision Sales Portal
status: draft for Kam's review
---

# Dynamics 365 Sales as a replacement for Attio (+ parts of Vision) — can we trial it for real?

## BLUF

Yes on both counts, with one hard caveat. Dynamics 365 Sales (on Dataverse) natively covers everything Attio plus the bridge do today — accounts/contacts/opportunities, a configurable stage pipeline, custom columns (no 27-cap), follow-up automation (sequences + Power Automate), quotes with PDF-by-email, and Exchange Online mail/calendar sync in the *same* corporate tenant, which is exactly what ATTIO-8 is blocked on. A **30-day free trial** exists, starts from a Datasec work account, lands as a trial environment in the corporate tenant (ae7a1e46…), needs **no Azure subscription**, and includes a *premium* licence so you can test the full Sales Hub against real data; one 30-day extension, then convert-to-production without losing data. The caveat is the HP mailbox (next-to-last section): the email that actually carries HP sales correspondence lives in HP's tenant, so every mailbox-dependent D365 feature is off the table for it — exactly as it is with Attio today. The comparison is like-for-like on email; D365's real gains are structure, quoting, Power Platform automation, and the Datasec-tenant sync.

## Recommendation

Trial **Dynamics 365 Sales Enterprise** via the standard Sales trial (it provisions with a premium licence, so you also see Premium features with Enterprise's monthly caps). Do **not** target Sales Professional: it is the cheap tier but is capped at ~15 custom tables and has feature exclusions (forecasting, territories, embedded intelligence) — UNVERIFIED against a Microsoft page, third-party licence guides only. **Customer Insights (Journeys/Marketing) is not needed** — nothing in the current flow is marketing automation. **Business Central is ERP, not the CRM** — ignore it for this evaluation.

**Exact trial path:** sign in as a Datasec user (`@datasec.com.au`) → https://www.microsoft.com/dynamics-365/products/sales → "Try for free" → country/phone/credit-card details → "Launch trial". Alternative for an admin who wants control from the start: Power Platform admin center → Environments → New → Type **Trial** → Dataverse **Yes** → Enable Dynamics 365 apps **Yes** → Sales.

## The free trial, precisely (Sales Enterprise/standard trial)

| Item | Finding |
|---|---|
| Length | 30 days; **one** self-service extension of +30 days, offered only in the last 7 days. Then convert or lose it. |
| Includes | Full Sales Hub (trial app is a cut-down front; "Sales Hub" is one click away), sample data, Sales Insights (accelerator, conversation intelligence, predictive scoring) with limited monthly capacity; "includes a premium license" per Microsoft's FAQ. |
| Seats | Microsoft FAQ: "unlimited number of users" on the trial environment; add users via admin.microsoft.com. Trial-environments page says a subscription-based (admin) trial usually carries 25 licences. |
| Environment / capacity | One Dataverse trial environment. Trial environments do **not** consume paid capacity and show 0 GB. Cannot be backed up/copied/reset — delete only. Deleted after 30 days of inactivity. |
| Who can start it | Any user with a **work or school (Entra) account** — a Global Admin is *not* required to self-sign, unless the tenant's "Trial environment assignments" setting has been set to "Only specific admins" (default allows users; UNVERIFIED for Datasec's tenant). Personal-email trials work but cannot reach the admin centers. The standard-trial user needs a per-user trial entitlement (the Sales trial sign-up grants it). |
| Lands in | The existing corporate tenant ae7a1e46… when signed in with a Datasec account. **No Azure subscription is required** for D365 licensing, Dataverse, or the trial (the only Azure link is optional pay-as-you-go). Corporate having zero Azure subscriptions is irrelevant. |
| Convert to paid | Yes — "Convert to production" in PPAC; data and config kept. Requires the tenant to have ≥1 GB free production Dataverse capacity (a paid Sales licence brings tenant capacity; default tenant grant is 3 GB DB). Note the Sales FAQ *recommends* a fresh prod environment, but conversion is supported. Conversion needs someone allowed to convert (tenant admin decides). |
| Doc conflict to watch | create-environment page says "Dynamics 365 apps can't be enabled for trial type environments" while trial-environments page (newer, 2025-06) shows the option. Take the trials.dynamics.com path, which provisions the app itself. |
| List price after trial (AUD, ex GST, paid yearly, microsoft.com/en-au) | Sales Professional **AU$97.30**/user/mo · Sales Enterprise **AU$157.10** · Sales Premium **AU$224.50** (incl. 1,000 Copilot credits). Pricing URL in Sources. Direct credit-card purchase at admin.microsoft.com or via a partner/CSP. |

## Mapping our flow onto D365 Sales

| Ours (Attio / Vision) | D365 Sales equivalent | Rating |
|---|---|---|
| Attio **Deal** (stages incl. PoC, Won/Cancelled/On hold) | **Opportunity** + Business Process Flow stages; custom choice column for PoC/On hold; Won/Lost close dialog with reason | **native** (stage config needed) |
| Attio **Person** / **Company** | **Contact** / **Account** | native |
| 27 custom-attribute cap on Deal | Dataverse custom columns — no fixed count; only the SQL 8,060-byte row-size limit. Custom tables unlimited on Enterprise. | native |
| Daily follow-up digest (not-contacted / PoC-ending / renewal) | Sales accelerator **work list + sequences** (1,500 sequence-connected records/mo on Enterprise; unlimited on Premium), Assistant insight cards, or a **Power Automate** scheduled flow emailing a digest (reproduces our job 1:1). "Not contacted" needs activities in D365 — see HP-mailbox section. | needs config |
| PoC-end + renewal signals | Custom date columns on Opportunity + Power Automate/insight cards; or Assistant custom cards | needs config |
| M365 email + calendar sync (ATTIO-8 blocker) — **Datasec mailboxes** | **Server-side sync**, "Server-to-Server (Same Tenant)" profile, auto-created for Exchange Online in the same tenant; mailbox approval needs Global/Exchange admin + D365 sysadmin once (or a delegated approver). Appointments/contacts/tasks sync too. | native (needs one admin action) |
| Same, **HP-issued mailbox** | Not possible via Exchange (other tenant, no consent). See HP section. | **not possible** (workarounds below) |
| Templates & sequences | Email templates native; sequences native (see caps). Sending goes through a *D365-approved* mailbox → Datasec address only. | native / needs config |
| Vision Postgres → CRM sync | (a) keep the Node bridge, swap Attio SDK for **Dataverse Web API** (OData; Entra app registration + client secret/cert + Application User; MSAL) — most faithful; (b) **Power Automate PostgreSQL connector** — *Premium*, and its docs are on-prem-gateway oriented, throttled 300 calls/60 s; (c) **Dual-write is Finance & Operations ↔ Dataverse only** — not applicable. | needs custom code (a) |
| QuickQuote emailed PDF+XLSX | D365 **Quote** entity: product catalogue + price lists, Activate, **Export to PDF → Email**, Word templates. Replicating QuickQuote's HPAS/MPS maths (per-device/day, PoC gating, FX) = custom pricing rules or keep QuickQuote external and write the quote back via Web API. | needs config / keep external |
| Monday.com lead source | Lead entity + Power Automate **Monday.com connector** (exists; premium — UNVERIFIED which tier) or Web API upsert from the bridge. Leads table frozen since 07-02 either way. | needs config |
| Freshdesk | No native link; Power Automate Freshdesk connector or Web API. Out of scope for this trial. | needs config |
| Service-principal licence | Application user is explicitly **unlicensed**; API calls draw from the tenant's non-licensed pool (500k/day base + 5k per D365 USL). | native |

## The HP mailbox constraint (Kam: "How will this impact the performance and features of Dynamics?")

**What depends on the mailbox, and what it degrades to without the HP one:**

- *Server-side sync / email tracking / timeline email activities* — off for HP mail. Timeline shows only what users log manually or what arrives via a Datasec address.
- *Auto capture* — requires Exchange **in the same tenant** as D365; off for HP mail.
- *Enhanced relationship analytics, who-knows-whom, response-time KPI* — Exchange-fed and Premium-gated; you get the **basic** versions computed from activities *in* D365 only. "Last contacted" is only as good as what is logged.
- *Sequences with email steps, email engagement (open/click), Copilot email summaries* — send/track from an approved D365 mailbox → Datasec address only; HP-mailbox threads invisible.
- *App for Outlook* — requires server-side sync on that mailbox → out for HP.

**Still works fully** with the Datasec mailbox: everything above, for Datasec-address correspondence; plus all non-mail features (pipeline, quotes, Power Automate, dashboards, forecasting, Web API bridge).

**Workarounds needing no HP admin consent (HP mailbox *policy* unknown — any could be blocked there, UNVERIFIED):**
1. **Forward/auto-BCC to a tracked Datasec mailbox or queue** (user-side Outlook rule). D365's forward-mailbox pattern is supported (not recommended for scale; incoming only; the rule must forward *as attachment*). Cheapest and most likely allowed.
2. **POP3/SMTP email-server profile** with user-supplied credentials — D365 supports POP3/SMTP (not IMAP); email only, no appointments/contacts/tasks. Requires HP to expose POP3 + basic/legacy auth for that mailbox — Exchange Online has basic auth off by default → very likely blocked. UNVERIFIED.
3. **Power Automate** flow on a *Datasec* mailbox that receives the forwarded copy → creates Email activity against the matched Contact/Opportunity. Same dependency as (1).

**Net:** this is the same limitation Attio has today (ATTIO-8 was the Datasec-tenant consent; the HP mailbox was never integrable there either). D365 loses its Exchange-fed intelligence for HP threads exactly as Attio does — like-for-like — and gains Datasec-tenant sync with a single admin action.

## What it would cost us (beyond licences)

- **Bridge rebuild:** Node bridge stays; replace the Attio client with Dataverse Web API (OData v4, MSAL client-credentials, `<env>/.default` scope). Entra app registration + Application User with a custom security role; **no licence** for it. Estimate: a focused week incl. tests (270-test suite has to be re-pointed).
- **Migration from Attio:** REST API export of People/Companies/Deals → Dataverse import (Excel/CSV import or Web API upserts). Small data set (~153 leads, 18 deals). One-off import must happen **before the Attio trial ends ~09-04** if we want Attio-side data.
- **Portal changes:** none required for a trial; later, QuickQuote write-back of generated quotes into D365 Quote/Opportunity.
- **Operations:** someone holds Power Platform admin / D365 admin in the corporate tenant; mailbox approval needs Global or Exchange admin once; solution/environment hygiene (dev → prod) is a new discipline.
- **vs staying on Attio Pro:** Attio Pro is US$79/user/mo annual (~AU$120) vs D365 Enterprise AU$157.10 — for 3 seats ≈ AU$3.3k vs AU$5.7k/yr. Attio is lighter to run and the bridge already works; D365 buys the same-tenant mail sync, unlimited custom schema, a real quote object, Power Automate, and the Microsoft partner-story fit — at ~AU$2.4k/yr more plus one week of bridge work.

## Open questions for Kam

1. Seat count and roles — who beyond you needs a full Enterprise seat vs a Team Member/read-only?
2. Replace Attio outright, or run D365 alongside through the trial window (Attio Pro trial ends ~09-04 — keep/drop and ATTIO-15 are coupled)?
3. Who holds Global Admin on ae7a1e46… — needed once for mailbox approval and for "convert to production"; does the tenant restrict trial-environment creation to admins?

## Sources (all fetched 2026-08-28)

- https://learn.microsoft.com/en-us/dynamics365/sales/sign-up-for-sales-trial — 30-day trial, work account, credit card
- https://learn.microsoft.com/en-us/dynamics365/sales/sales-trial-faq — unlimited users, one extension, convert to paid, premium licence in trial, features
- https://learn.microsoft.com/en-us/power-platform/admin/trial-environments — trial types, no paid capacity, extension in last 7 days, convert to production, account types
- https://learn.microsoft.com/en-us/power-platform/admin/create-environment — who can create environments, 1 GB rule, D365-apps-on-trial conflict, pay-as-you-go optional
- https://learn.microsoft.com/en-us/power-platform/admin/control-environment-creation — tenant setting restricting trial creation
- https://learn.microsoft.com/en-us/power-platform/admin/capacity-storage — trial environments 0 GB, default 3 GB, convert needs 1 GB
- https://www.microsoft.com/en-au/dynamics-365/products/sales/pricing — AUD prices
- https://learn.microsoft.com/en-us/dynamics365/sales/digital-selling — Enterprise vs Premium caps (1,500/mo), basic vs advanced relationship insights
- https://learn.microsoft.com/en-us/dynamics365/sales/create-manage-sequences — sequences, sales accelerator prerequisite
- https://learn.microsoft.com/en-us/dynamics365/sales/relationship-analytics-overview — basic vs enhanced, Exchange dependency
- https://learn.microsoft.com/en-us/dynamics365/sales/who-knows-whom — basic vs Exchange-enhanced
- https://learn.microsoft.com/en-us/dynamics365/sales/auto-capture and https://learn.microsoft.com/en-us/dynamics365/sales/configure-auto-capture — same-tenant Exchange prerequisite
- https://learn.microsoft.com/en-us/power-platform/admin/set-up-server-side-synchronization-of-email-appointments-contacts-and-tasks — Exchange vs POP3 scope
- https://learn.microsoft.com/en-us/power-platform/admin/connect-exchange-online — same-tenant S2S profile, mailbox approval roles
- https://learn.microsoft.com/en-us/power-platform/admin/connect-to-pop3-or-smtp-servers — POP3/SMTP profile, no appointments/contacts/tasks
- https://learn.microsoft.com/en-us/power-platform/admin/forward-mailbox-vs-individual-mailboxes — forward-mailbox pattern and caveats
- https://learn.microsoft.com/en-us/dynamics365/outlook-app/deploy-dynamics-365-app-for-outlook — App for Outlook needs server-side sync
- https://learn.microsoft.com/en-us/dynamics365/sales/create-edit-quote-sales — quotes, Export to PDF → email, Word templates
- https://learn.microsoft.com/en-us/power-apps/developer/data-platform/authenticate-oauth — connect as app, no paid licence for application user
- https://learn.microsoft.com/en-us/power-platform/admin/manage-application-users — unlicensed application user
- https://learn.microsoft.com/en-us/power-platform/admin/api-request-limits-allocations — non-licensed pool 500k + 5k/USL
- https://learn.microsoft.com/en-us/connectors/postgresql/ — Premium connector, gateway, 300 calls/60 s
- https://learn.microsoft.com/en-us/dynamics365/fin-ops-core/dev-itpro/data-entities/dual-write/dual-write-overview — dual-write is F&O ↔ Dataverse
- https://docs.attio.com/rest-api/overview — Attio REST API exists
- https://attio.com/pricing — Pro US$79 annual / US$99 monthly
- Web search (learn.microsoft.com) for Dataverse column limits — 8,060-byte row limit (troubleshoot article "maximum-row-size-exceeds"); Sales Professional 15-custom-table limit from third-party licence guides only (serversys.com, encorebusiness.com) — UNVERIFIED
- **Fetch failures (404):** learn.microsoft.com/…/sales/sign-up-free-trial, …/sales/compare-sales-offerings, …/sales/sales-premium-intro, …/sales/customize-limit-sales-professional, …/sales-professional/overview
