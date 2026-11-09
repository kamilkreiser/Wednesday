# HPSMPOC-16: where the built stack differs from SOW 4.1, for your sign-off

**What this is.** HPSMPOC-16 can close when two things are true: the decision record is signed off, and the deviations from SOW 4.1 are listed with their reasons. This page is that list. Nothing changes in Jira until you tap.

**Which "4.1".** SOW 4.1 here means the *Recommended Technology Stack* table in the draft SOW (v1, 23 Sep), which the ticket was written against. The signed SOW (rev 28 Sep) has no stack table. Its §4.1 is the list of deliverables. The same stack survives only as a skills list in §3.3, which names Adobe XD, not Figma, as the UX tool.

**What was compared.** Each row of the 4.1 table, checked against the code on main today (`fa401da9`, 9 Nov) and the decision record (`design-pack/10_ADRs.md`, last changed 4 Oct).

## Deviations

| # | 4.1 row: what the SOW asks for (paraphrased) | What was built | Why | Record | Already ruled? | Kam sign-off |
|---|---|---|---|---|---|---|
| 1 | **PDF** (§4.1): server-side reports with QuestPDF or an equivalent library | PdfPig 0.1.16 (Apache-2.0), behind a swappable renderer. Consequence: the PDF is not tagged for accessibility (PDF/UA). | QuestPDF's free licence may not cover this work (it is unclear whether HP or Datasec is the licensee). The paid tiers cost US$1,999 or US$4,999. PdfPig has no licence cost. | ADR-R01 (replaces AD-15); ADR-R11 | Yes: C-13, "stay on PdfPig" and "accept no PDF/UA" | |
| 2 | **UX** (§4.1): clickable designs and approved screen states made in Figma | No Figma. The coded, clickable prototype in the web app is the UX and the screen designs. | Your 1 Oct ruling. The signed SOW no longer lists a Figma prototype as a deliverable (C-35). | No ADR; ruling C-37 A (1 Oct) | Yes: "the coded prototype is the UX and the screen designs" | |
| 3 | **Source control / CI-CD** (§4.1): GitHub or Azure DevOps, with automated build, test and deployment | GitHub Actions builds, tests and scans every change, and keeps a tested deploy package from main. **The deploy is a runbook step run by hand from that package; no CI job deploys.** | An automated deploy needs a GitHub-to-Azure federated credential. Granting it is yours. The last record (HPSMPOC-58) says it is not in place. | AD-24 planned CI deploys; the build differs from it too | No | |
| 4 | **Testing** (§4.1): xUnit, Playwright and Postman for unit, browser and API checks | xUnit (including API tests against the published API contract), Playwright (browser journeys and accessibility) and Vitest (web unit tests). **No Postman.** | The test strategy puts the API checks in xUnit, run against the contract in CI on every change. No reason for leaving out Postman is written down. | AD-29 (test strategy, design pack 19) | No | |
| 5 | **Data** (§4.1): Azure SQL for customer, assessment, rules metadata and audit data | Azure SQL in the hosted environments. SQLite for local development and the main CI test run, plus a second CI run on SQL Server. | Development and tests need no Azure or Docker. The SQL Server run is not a required check. | ADR-A05 | No | |
| 6 | **Rules configuration** (§4.1): JSON or YAML, plus metadata in the database | Versioned, hash-stamped JSON files loaded at start-up. Each assessment records the ruleset id and version it was scored with. **There is no rules-metadata table in the database.** | A new ruleset is a new file version, not a database change. A table is planned for when content is imported at runtime. | ADR-A01, A02, A04 | No | |

## Rows checked with no deviation

Front end (Next.js 16.4.2, React 19.2.8) · API (ASP.NET Core on .NET 10) · Identity (Microsoft Entra ID; the local-only developer sign-in is ADR-A09, ruled C-15) · File storage (Azure Blob, a private `reports` container) · AI (Azure OpenAI `gpt-4.1-mini`, Standard deployment in Australia, AD-14) · Secrets (Key Vault, managed identities, AD-16) · Hosting (App Service B1, AD-10) · Observability (Application Insights and Log Analytics, AD-25) · IaC (Bicep, AD-24) · Security scanning (CodeQL, npm and NuGet audit, dependency review and gitleaks).

## Two things to know before you sign

- **The ADR count has changed since the card.** The card says 36 build ADRs (7 ruled, 29 decided). That is the count from 24 Sep. The record's own summary now lists 43 (ADR-A01 to A31 and R01 to R12): 8 ruled and 35 decided. A29 (showcase data scored by the draft ruleset) is flagged for you. Your sign-off would cover the 43.
- **Parts of the record are older than the code.** Two lines in the record are out of date. ADR-A18 says the Blob report store is "not built", but it is now in the code. ADR-R12 says the project uses "no Azure.Identity", but the Reporting module now uses it. Neither is a SOW 4.1 deviation. If you want, a records pass can bring the record up to date before the ticket closes.

**Options:** (a) sign off rows 1 to 6 as listed, and HPSMPOC-16 closes with this list attached; (b) sign off some rows and name the rest; (c) hold.
