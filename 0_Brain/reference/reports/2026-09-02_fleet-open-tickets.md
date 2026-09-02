# Fleet — outstanding tickets by project (2026-09-02)

## BLUF

- **474 open tickets across 7 projects** (Platform K's 238 reused from this morning's report, not re-queried; 6 Datasec projects read live from Jira and file-backed backlogs at 2026-09-02T07:47:13Z). **Category 1 — ours, ready to action: 217** · **Category 2 — requires input: 126** · **Category 3 — done on our side, awaiting approval/close: 131**.
- Assigned to Kam: 263 tickets fleet-wide, of which 112 are category 1 (43%). On the Datasec Jira boards only NexusAI assigns anyone at all (all 131 to Kam); HPSM, ATTIO and CypherKey carry no assignee on any open ticket; the file-backed backlogs have no assignee field.
- Jira 'statusCategory != Done' is the open predicate for every Jira project; all statuses in the To-Do and In-Progress categories are included (Testing / Release Ready / Put on Hold are In-Progress-category in the RD workflow and are therefore open).

| Project | Open | Cat 1 ours | Cat 2 needs input (dominant) | Cat 3 awaiting | Kam-assigned | Kam-assigned actionable | Needs nobody outside Kam+Wed+agent |
|---|---|---|---|---|---|---|---|
| Secuura/Blockchain (Platform K) | 238 (27 archived incl.) | 129 | 49 (Peter (22) · Kam (19)) | 60 | 132 | 71 = 54% | not measured in that report |
| Datasec/NexusAI | 131 | 41 | 31 (Kam (31)) | 59 | 131 | 41 = 31% | 131 = 100% |
| Datasec/HPSM | 26 | 4 | 17 (HP (12) · Kam (5)) | 5 | 0 | n/a (no assignees) | 13 = 50% |
| Datasec/ATTIO | 16 | 6 | 6 (Kam (6)) | 4 | 0 | n/a (no assignees) | 14 = 88% |
| Datasec/CypherKey | 28 | 21 | 5 (Kam (5)) | 2 | 0 | n/a (no assignees) | 28 = 100% |
| Datasec/Vision_Sales_Portal (+QuickQuote) | 28 | 15 | 12 (Kam (12)) | 1 | n/a (file) | n/a (file-backed) | 28 = 100% |
| Datasec/Lead_Bot | 7 | 1 | 6 (Kam (6)) | 0 | n/a (file) | n/a (file-backed) | 7 = 100% |
| **Fleet** | **474** | **217** | **126** | **131** | **263** | **112 = 43%** | — |

Things to notice:

1. **NexusAI's queue is a QA/acceptance queue, not a build queue.** 59 of 131 open RD tickets are fixed, pushed or deployed and wait on Kam's acceptance or a browser check; 7 of those (RD-56/62/65/67/68/79/85) have been parked on RD-76 (agents cannot browser-verify behind Entra SSO) since 08-20. One ruling on RD-76 — a test identity, or Kam clicking through once — closes seven tickets.
2. **CypherKey has a dated item: CPKEY-165, rotate the Twilio auth token, due 2026-09-04** (two days). The board has had no activity since 08-04 otherwise; 17 tickets sit 'In Progress' with last activity in June–July.
3. **HPSM is almost entirely gated on HP** (signature, clinic date, asks) — 17 of 26; the two in our hands are the tracker (HPSM-12) and Kam's top-priority scoring model (HPSM-37). Three finished proposals (HPSM-29/30/32) and the drafted §13 CR (HPSM-41) are in Kam's hands to carry to HP.
4. **Vision Sales Portal has no open Jira tickets** (VSP: 64 issues, all Done; newest VSP-64, 2026-07-03) — its real backlog is 28 file-backed entries, 15 of them ours to action, and four QuickQuote go-live items that are Kam's DNS/Azure actions.
5. **Lead_Bot is 6 of 7 Kam-held**: the tenant name, the gh login and the HOLD on SALES_PORTAL_URL gate everything but the .env-path fix.

## What we can action today

Top five category-1 tickets per project by priority (full lists in the project sections).

**Datasec/NexusAI** (41 category-1)
- RD-50 (High) — Repoint Feedback System + Lead Bot off the retired 4.x VM -\> Container Apps env — Scoped 08-13; precondition RD-88 (COORDINATOR_SECRET + machine-consumer auth on Container Apps), then dispatch to the Feedback_System / Lead_Bot seats
- RD-143 (High) — DATA_DIR is silently overridden when the directory has no settings.json yet — a… — Reproduced live 09-01
- RD-148 (High) — F-1 is undelivered to the admin: no revoke control and no issued-at anywhere in… — F-1 UI half deferred here from RD-135
- RD-155 (High) — hasExistingSettings() returns false for numeric and boolean settings, so an exp… — Pre-existing on main (measured 09-01)
- RD-163 (High) — jsdom resolves the CSS cascade by SOURCE ORDER and ignores specificity — every… — jsdom cascade — measurement validity

**Datasec/HPSM** (4 category-1)
- HPSM-37 (Highest) — T30: [KAM TOP PRIORITY] Purview/Compliance Manager scoring model - weights are… — Kam's TOP PRIORITY; O1 continuation under his get-ahead grant — mechanism specified, work continues
- HPSM-12 (Medium) — T7: SOW execution & prerequisite tracker — SOW execution tracker, current to 08-20; ours to keep current
- HPSM-19 (Medium) — T14: Weekly programme status + prerequisite chase list — Weekly status W0 current to 08-20; next issue is ours
- HPSM-20 (Medium) — T15: HP Amplify launch alignment - 5-10 Dec 2026 (six-day event, not a single d… — Amplify 5–10 Dec; date fact recorded, register alignment ours

**Datasec/ATTIO** (6 category-1)
- ATTIO-2 (Medium) — E0 — Foundations — E0 epic container
- ATTIO-3 (Medium) — E1 — Integrate: Vision → Attio — E1 epic container
- ATTIO-4 (Medium) — E2 — Deploy on Datasec infrastructure — E2 epic container
- ATTIO-5 (Medium) — E3 — Train: people, best of both systems — E3 epic container
- ATTIO-23 (Medium) — Bridge monitoring + runbook

**Datasec/CypherKey** (21 category-1)
- CPKEY-9 (Medium) — KeyMap engine, RNG/entropy, registration HSM op, randomness proof — Phase-1 epic
- CPKEY-10 (Medium) — .NET auth core: serial issuance, hash-verify, activation window, device-cert mT… — Phase-1 epic; local stack verified
- CPKEY-11 (Medium) — Swift + Kotlin apps: QR registration, device tokenisation, secure KeyMap store,… — Phase-2 epic
- CPKEY-12 (Medium) — Both options: EAM second-factor AND federated passwordless IdP (OIDC/SAML) — Phase-3 epic
- CPKEY-13 (Medium) — Tenant/user/device/cert lifecycle, connector config, audit review — Phase-4 epic; mTLS done 06-28

**Datasec/Vision_Sales_Portal (+QuickQuote)** (15 category-1)
- VSP-B1 (High) — npm audit: 5 high remaining (archiver/minimatch/lodash, path-to-regexp, ip-addr… — Own test pass; some want major bumps (express 5)
- QQ-B5 (High) — v2.20 on main but NOT deployed (PoC lines dropped) — Stale: v2.30 (v0.4.5) deployed 09-01 ships d258651, which postdates e711771 — verify and tick
- QQ-B6 (High) — stage3: 3 high advisories — extract-zip via puppeteer-core (GHSA-jmr9-qjv8-65gv) — Recorded twice (08-14, 09-01); breaking bump on the PDF engine needs its own session + A4 print re-verify
- QQ-B2 (Medium) — Page scrolls sideways ~38px on a phone (.ticket summary table) — Build, then Kam eyeballs the totals layout
- QQ-B4 (Medium) — No .dockerignore — image ships the builder's node_modules; switch to npm ci — Recorded twice in the file (08-26, 09-01); one row here. Own session + digest re-verify

**Datasec/Lead_Bot** (1 category-1)
- LB-B4 (Medium) — .env location does not match what config.js / docker-compose read — Propose launcher-managed copy or --env-file; build it

**Secuura/Blockchain (Platform K)** — see the [Platform K report](2026-09-02_secuura-platform-k-open-tickets.md): KS-695 (Stuart is waiting on us), KS-593, KS-591, KS-578, KS-739; and the category-3 batch (merge #764/#738, deploy decision on the merged-not-deployed set).

## What we must follow up

Category-2 tickets grouped by who must act.

**Datasec/NexusAI** (31)

- **Kam** (31): RD-13 (Partner Center); RD-18 (parked until RD-13); RD-20 (money, vendor); RD-21 (money, vendor); RD-28 (money); RD-75 (ruling); RD-177 (ruling: CSSOM workaround vs accept); RD-193 (ruling); RD-196 (ruling); RD-6 (commercial track); RD-7 (commercial track); RD-8 (commercial track); RD-15 (assets); RD-22 (hiring); RD-29 (money); RD-30 (Partner Center); RD-31 (hiring); RD-41 (parked until RD-13); RD-49 (dev-tenant fc05dcdd access); RD-69 (re-film assets); RD-76 (Entra test identity); RD-83 (gh auth, RD-74); RD-104 (ruling); RD-202 (ruling); RD-32 (customer demand); RD-33 (usage evidence); RD-34 (Partner Center); RD-54 (dev-tenant admin); RD-93 (Jira admin); RD-160 (brand-chrome card); RD-198 (ruling)

**Datasec/HPSM** (17)

- **Kam** (5): HPSM-40 (2-min gh device flow); HPSM-8 (dev-environment/tenant decision); HPSM-9 (next HP conversation); HPSM-26 (PRD re-issue + P06); HPSM-27 (ruling)
- **HP** (12): HPSM-38 (clinic date); HPSM-1 (SOW signature); HPSM-2 (SOW signature); HPSM-3 (clinic date); HPSM-4 (asks); HPSM-5 (SOW signature); HPSM-15 (clinic date); HPSM-21 (open asks); HPSM-25 (signature date); HPSM-28 (clinic date); HPSM-31 (clinic date); HPSM-35 (post-signature alignment)

**Datasec/ATTIO** (6)

- **Kam** (6): ATTIO-8 (Entra admin consent); ATTIO-10 (pricing enquiry); ATTIO-15 (tier/dispose); ATTIO-24 (+1–2 reps); ATTIO-25 (+reps); ATTIO-27 (ruling)

**Datasec/CypherKey** (5)

- **Kam** (5): CPKEY-16 (money, vendors); CPKEY-44 (money, vendor); CPKEY-45 (money, vendor); CPKEY-93 (sequenced after 161/162; store accounts); CPKEY-165 (Twilio console)

**Datasec/Vision_Sales_Portal (+QuickQuote)** (12)

- **Kam** (12): QQ-B1 (custom sending domain at go-live: DNS); QQ-B10 (domain + DNS); QQ-B15 (custom domain); VSP-B3 (gh auth login in a launcher shell); VSP-B4 (HOLD ruling 08-06); QQ-B11 (one-time Owner grant); VSP-B2 (dev-data call); QQ-B7 (ruling); QQ-B9 (ruling); QQ-B12 (decide); QQ-B22 (customer-facing print change); QQ-B23 (ruling)

**Datasec/Lead_Bot** (6)

- **Kam** (6): LB-B1 (HOLD ruled 08-06; waits on (b); LB-B2 (name the Azure tenant); LB-B3 (gh auth login as datasecau); LB-B5 (which document is right); LB-B6 (credentials); LB-B7 (blocked behind LB-B3)

**Secuura/Blockchain (Platform K)** — 49 category-2 (Peter 22 · Kam 19 · Stuart 8, per the Platform K report): Kam's 19 rulings are listed in that report's 'Waiting on' column; Peter's and Stuart's items are their own tickets.

## Datasec/NexusAI

Jira project `RD` on `team-1634009483756.atlassian.net` · `project = RD AND statusCategory != Done ORDER BY key ASC` · read 2026-09-02 · **131 open** · category 1 / 2 / 3 = 41 / 31 / 59 · Kam-assigned 131 (41 category-1 = 31%).

### 1. In our hands — ready to action (41)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| RD-50 | Repoint Feedback System + Lead Bot off the retired 4.x VM -… | High | To Do | Kam | operations | 2026-08-13 | Scoped 08-13; precondition RD-88 (COORDINATOR_SECRET + machine-consumer auth on Container Apps), then dispatch to the Feedback_System / Lead_Bot seats |
| RD-143 | DATA_DIR is silently overridden when the directory has no s… | High | To Do | Kam | operations | 2026-09-01 | Reproduced live 09-01 |
| RD-148 | F-1 is undelivered to the admin: no revoke control and no i… | High | To Do | Kam | operations | 2026-09-02 | F-1 UI half deferred here from RD-135 |
| RD-155 | hasExistingSettings() returns false for numeric and boolean… | High | To Do | Kam | operations | 2026-09-01 | Pre-existing on main (measured 09-01) |
| RD-163 | jsdom resolves the CSS cascade by SOURCE ORDER and ignores… | High | To Do | Kam | operations | 2026-09-02 | jsdom cascade — measurement validity |
| RD-167 | Dark mode is a THREE-page feature: 11 of the 14 shipped pag… | High | To Do | Kam | operations | 2026-09-02 | 11 of 14 pages never link dark-mode.css |
| RD-197 | R3 derives every dark accent against the CARD, so 7 of 10 f… | High | To Do | Kam | operations | 2026-09-02 | — |
| RD-199 | The brand conformance check resolves HEX only — every rgba(… | High | To Do | Kam | operations | 2026-09-02 | — |
| RD-200 | Dark-mode colours set from JavaScript are outside the brand… | High | To Do | Kam | operations | 2026-09-02 | — |
| RD-201 | jsdom does not substitute var() — 78 colour declarations ac… | High | To Do | Kam | operations | 2026-09-02 | — |
| RD-81 | Decide + implement CI-driven deploy to the Container Apps d… | Medium | In Progress | Kam | — | 2026-08-13 | Commit b54ee24 landed 08-13; demo has been redeployed since — verify what of the CI-deploy decision is live, then move or resume |
| RD-131 | Export CSV → Fleet Health silently omits the Drum Status ta… | Medium | To Do | Kam | operations | 2026-08-27 | Proposal sized 08-27; two functions, none commissioned |
| RD-132 | README and DEPLOYMENT_GUIDE still present the decommissione… | Medium | To Do | Kam | operations | 2026-08-27 | Docs still name the 4.x VM |
| RD-133 | SchedulerAudit.readRecent silently truncates by line count,… | Medium | To Do | Kam | operations | 2026-08-27 | — |
| RD-134 | All 12 schedulers had zero test coverage because requiring… | Medium | To Do | Kam | operations | 2026-08-27 | — |
| RD-141 | jira-query.sh --count silently caps at 100 — it ignores nex… | Medium | To Do | Kam | operations | 2026-09-02 | --count cap reproduced 09-02; this report paginated around it |
| RD-142 | SimpleDb.close() fires and forgets — a failed close becomes… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-144 | Dashboard tab strip has no tablist/tab/tabpanel semantics —… | Medium | To Do | Kam | operations | 2026-09-01 | WCAG 4.1.2 |
| RD-145 | All vendor CSS/JS loads from cdn.jsdelivr.net — in an egres… | Medium | To Do | Kam | operations | 2026-09-01 | CDN egress |
| RD-146 | The product has no currency configuration — '$' is hardcode… | Medium | To Do | Kam | operations | 2026-09-01 | Currency config |
| RD-150 | jsonStorage.getSetting returns `value \|\| null`, so a stor… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-151 | Cost settings errors are shown as a page banner and the ser… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-152 | Three different Bootstrap versions across the pages (5.1.3… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-153 | verify-suite.sh deleted its jest JSON report on failure — t… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-154 | Unreproduced suite FAIL: 774/776 on one run with no code ch… | Medium | To Do | Kam | operations | 2026-09-01 | Unreproduced; filed for record |
| RD-156 | Clearing a cost field reports "saved successfully" and chan… | Medium | To Do | Kam | operations | 2026-09-01 | — |
| RD-164 | Dark mode's neutral card border #3a3a5a on #1e1e3f is 1.47:… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-175 | P8-07: span.consumable-text is white on the light #e9ecef t… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-187 | Three /api/normalized/* endpoints return 503 on every dashb… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-188 | The first-run wizard violates the product's own CSP ~20 tim… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-194 | span.badge.bg-info is white on Bootstrap's cyan at 1.96:1 i… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-195 | The contrast sweep cannot run twice inside its own rate-lim… | Medium | To Do | Kam | operations | 2026-09-02 | — |
| RD-55 | RSA private key + old SP secrets in git history — rotate +… | Low | To Do | Kam | security | 2026-08-15 | Rotation ours; three burned credentials in scope (PT-011 added 08-15); any history rewrite pauses for Kam |
| RD-117 | first-run-setup applies a CSP-blocked inline style — error… | Low | To Do | Kam | operations | 2026-08-24 | — |
| RD-162 | Settings Appearance toggle does nothing until Save, which r… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-166 | The loading overlay renders white text on a white panel at… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-176 | Provisioning mode cards paint their ground from JS inline s… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-178 | Critical dark-ground \<style\> block allowed by a CSP style… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-180 | Scan destination badge is 3.23:1 in BOTH modes — a 12-colou… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-189 | checkEntraStatus throws TypeError: Cannot set properties of… | Low | To Do | Kam | operations | 2026-09-02 | — |
| RD-190 | The RD-166 .loading-overlay allow-list entry suppresses not… | Low | To Do | Kam | operations | 2026-09-02 | — |

### 2. Requires input (31)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| RD-13 | DEV offer in Partner Center + end-to-end $0 test purchase | High | To Do | Kam | horizon-1, marketplace | 2026-06-05 | Kam (Partner Center) | Runbook drafted 06-05; the DEV offer + $0 purchase need Kam's Partner Center identity |
| RD-18 | Australian Privacy Act package: statement + sub-processors… | High | Put on Hold | Kam | horizon-1, legal, needs-decision | 2026-08-04 | Kam (parked until RD-13) | Confirmed parked 08-04 |
| RD-20 | Engage SOC 2 / ISO 27001 vendor (Vanta or Drata) — start ob… | High | To Do | Kam | compliance, horizon-2 | 2026-05-20 | Kam (money, vendor) | SOC 2 / ISO vendor engagement |
| RD-21 | Annual third-party penetration test (CREST-accredited) | High | To Do | Kam | horizon-2, security | 2026-05-20 | Kam (money, vendor) | CREST pen test |
| RD-28 | SOC 2 Type II audit closes | High | To Do | Kam | compliance, horizon-3 | 2026-05-20 | Kam (money) | H3 audit close |
| RD-75 | No working mechanism for Kam-traceable authorisation of app… | High | Testing | Kam | needs-decision, operations | 2026-08-21 | Kam (ruling) | needs-decision; criterion 3 (DKIM recipe in workspace CLAUDE.md) unmet 08-21 |
| RD-177 | P8-A: the flash of light content survives RD-169 — dark-mod… | High | Testing | Kam | operations | 2026-09-02 | Kam (ruling: CSSOM workaround vs accept) | Part (a) fixed 7568302; part (b) is a decision, not work |
| RD-193 | The COMPUTE ruling for the three dark sustainability KPIs i… | High | To Do | Kam | needs-decision, operations | 2026-09-02 | Kam (ruling) | needs-decision: COMPUTE ruling not executable as written |
| RD-196 | RD-192 puts two windows on one screen — the KPI tiles read… | High | To Do | Kam | needs-decision, operations | 2026-09-02 | Kam (ruling) | needs-decision card issued 09-02 (two windows on one screen) |
| RD-6 | H1: Commercial GA Unblock | Medium | To Do | Kam | commercialisation | 2026-05-20 | Kam (commercial track) | H1 epic container; moves with RD-13 |
| RD-7 | H2: Sell With Confidence | Medium | To Do | Kam | commercialisation | 2026-05-20 | Kam (commercial track) | H2 epic container |
| RD-8 | H3: Scale | Medium | To Do | Kam | commercialisation | 2026-05-20 | Kam (commercial track) | H3 epic container |
| RD-15 | Marketing assets: logos, 5 screenshots, demo video, datashe… | Medium | Testing | Kam | horizon-1, marketing | 2026-08-21 | Kam (assets) | 23 in-repo assets exist; remaining half is Kam's and now stale (RD-69) |
| RD-22 | Onboard first contracted Tier 1 support person | Medium | To Do | Kam | hiring, horizon-2, support | 2026-05-20 | Kam (hiring) | Tier 1 support contractor |
| RD-29 | ISO 27001 certification (typically bundled with SOC 2) | Medium | To Do | Kam | compliance, horizon-3 | 2026-05-20 | Kam (money) | H3 certification |
| RD-30 | IP co-sell eligible status | Medium | To Do | Kam | horizon-3, sales | 2026-05-20 | Kam (Partner Center) | IP co-sell status |
| RD-31 | Tier 2 / engineering hire — Kam steps out of daily support | Medium | To Do | Kam | hiring, horizon-3 | 2026-05-20 | Kam (hiring) | Tier 2 hire |
| RD-41 | Deploy Monday lead-sync creds to Container Apps (Monday go-… | Medium | Put on Hold | Kam | automation, horizon-2 | 2026-08-04 | Kam (parked until RD-13) | Do NOT deploy creds — Kam 08-04 |
| RD-49 | Decommission 4.x demo VM (app stopped; Azure deallocation +… | Medium | In Progress | Kam | operations | 2026-08-27 | Kam (dev-tenant fc05dcdd access) | Blocked on access, not authority; deletion stays Kam's signed mail |
| RD-69 | RD-15 demo video + screenshots predate the synthetic feed —… | Medium | To Do | Kam | — | 2026-08-24 | Kam (re-film assets) | Synthetic fleet is permanent (08-24); video/screenshots need redoing — Kam's assets + RD-76 |
| RD-76 | Agent sessions cannot browser-verify the demo — Entra SSO b… | Medium | To Do | Kam | operations | 2026-09-01 | Kam (Entra test identity) | Blocks browser verification of 7 finished tickets |
| RD-83 | Audit + prune stale GitHub repo Actions secrets (retired st… | Medium | To Do | Kam | — | 2026-08-12 | Kam (gh auth, RD-74) | Needs authenticated gh; K2 login landed 08-20 — re-test before treating as blocked |
| RD-104 | gh auth token is not isolated by GH_CONFIG_DIR — a config d… | Medium | Put on Hold | Kam | needs-decision, operations, security | 2026-08-20 | Kam (ruling) | Put on Hold, needs-decision; measurements re-run after K2 |
| RD-202 | The LIGHT active dashboard tab is #667eea on #f0f2fd at 3.2… | Medium | To Do | Kam | needs-decision, operations | 2026-09-02 | Kam (ruling) | needs-decision: indigo tab pairing vs brand |
| RD-32 | Multi-region deployment option (build only when a customer… | Low | Put on Hold | Kam | horizon-3, scale | 2026-05-21 | Kam (customer demand) | Parked per Kam 05-21 |
| RD-33 | Metered billing model (only if usage shapes justify it) | Low | Put on Hold | Kam | horizon-3, monetisation | 2026-05-21 | Kam (usage evidence) | Parked per Kam 05-21 |
| RD-34 | Marketplace Rewards / App Accelerate enrolment | Low | To Do | Kam | horizon-3, sales | 2026-05-20 | Kam (Partner Center) | Rewards enrolment |
| RD-54 | Rotate (or confirm dead) the leaked Log Analytics shared ke… | Low | To Do | Kam | security | 2026-08-07 | Kam (dev-tenant admin) | Needs Datasec dev-tenant admin; re-tiered Low 08-04 |
| RD-93 | RD board config: remove or rename duplicate transition id 5… | Low | Put on Hold | Kam | needs-decision, operations | 2026-08-27 | Kam (Jira admin) | Put on Hold; board-config change, second naming defect added 08-27 |
| RD-160 | P6-04: white on #0096d6 brand chrome is 3.32-3.34:1 in both… | Low | In Progress | Kam | operations | 2026-09-02 | Kam (brand-chrome card) | Measurements only; brand chrome is Kam's decision |
| RD-198 | The dark neutral ramp has a fourth step but it is named --n… | Low | To Do | Kam | needs-decision, operations | 2026-09-02 | Kam (ruling) | needs-decision: naming of the fourth ramp step |

### 3. Done on our side — awaiting approval (59)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|
| RD-118 | Synthetic demo feed does not isolate the AI table-discovery… | Highest | Testing | Kam | operations, security | 2026-08-24 | Kam (accept) | Highest; deployed with rollback revision held |
| RD-61 | Global Variables LAW ingest dead since 2026-06-01 — demo da… | High | Release Ready | Kam | operations | 2026-08-24 | Kam (close) | Kam ruled synthetic data is the standing state 08-24; annotate + close |
| RD-106 | gitleaks azure-client-secret rule only matches '=' — a real… | High | Testing | Kam | operations, security | 2026-08-22 | Kam (QA/close) | Fixed a59a981 |
| RD-109 | mainTemplate.json's real secret parameters (printerDataClie… | High | Testing | Kam | operations, security | 2026-08-22 | Kam (QA/close) | Fixed 45fd47f |
| RD-110 | gitleaks workflow has no canary step — a rule-coverage regr… | High | Testing | Kam | operations, security | 2026-08-23 | Kam (QA/close) | Canary armed |
| RD-115 | package-lock.json is blind to the secret gate even with our… | High | Testing | Kam | operations, security | 2026-08-23 | Kam (QA/close) | Fixed 6c4b451 |
| RD-116 | Feedback has no attachment path at all — users cannot attac… | High | Testing | Kam | operations | 2026-08-26 | Kam (accept) | Deployed to demo, verified end-to-end 08-24 |
| RD-119 | SESSION_SECRET is a plaintext env var on the running Contai… | High | Testing | Kam | operations, security | 2026-08-24 | Kam (accept) | secretRef live, secret rotated |
| RD-121 | AI is handed the wrong table list — discoverTables' 7-day w… | High | Testing | Kam | operations | 2026-08-25 | Kam (accept) | Deployed to demo 08-25 |
| RD-157 | P6-01: first-run wizard children keep light colours inside… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | In Testing since s15 |
| RD-159 | P6-03: index.html's div.controls and .ai-assistant-section… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | R6-3 delivered |
| RD-168 | npm run verify went from 88s to 10m33s in one session — the… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 3d4b789 |
| RD-169 | P7-02 REGRESSION (mine, RD-158): the dark-mode.css link was… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Regression fixed 8efae42 |
| RD-173 | P8-01: dark mode has ZERO .bg-* counterparts — Bootstrap's… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 5ddcb9c |
| RD-174 | P8-02 REGRESSION (round 7, a0d5dfd/RD-170): body.dark-mode… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 5ddcb9c |
| RD-181 | The repository has no style guide, brand-token file or pale… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Style guide + tokens at e6c3fca |
| RD-182 | The dark theme is an invented palette, not a dark rendering… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Palette ruled NEUTRAL 09-02; landed 01007c3 |
| RD-183 | The contrast sweep measures the dashboard on its EMPTY defa… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | f876732 |
| RD-184 | a.btn.btn-success is allow-listed under a reason that is fa… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | f876732 |
| RD-192 | Sustainability opens on a window with no data, so a user's… | High | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Verified in a browser on :3023 |
| RD-62 | Data-freshness monitoring: health + status page must flag a… | Medium | Testing | Kam | operations | 2026-08-21 | Kam (browser verify, RD-76) | 3 of 4 criteria verified; 4th needs a browser |
| RD-65 | Appearance dark-mode setting calls nonexistent /api/setting… | Medium | Testing | Kam | — | 2026-08-21 | Kam (browser verify, RD-76) | Defect proven gone; regression leg needs a browser |
| RD-67 | Maintenance cartridge table: colour swatch dots are CSP-blo… | Medium | Release Ready | Kam | — | 2026-08-24 | Kam (browser verify, RD-76) | Fix live on rev 0000084 |
| RD-68 | Mono printers show '100% EST' for colour toner they do not… | Medium | Release Ready | Kam | — | 2026-08-20 | Kam (browser verify, RD-76) | Fix live on rev 0000084 |
| RD-79 | Session expiry mid-use surfaces as raw 401/403 error in AI… | Medium | Testing | Kam | — | 2026-08-21 | Kam (browser verify, RD-76) | Interceptor shipped; real-401 render needs a browser |
| RD-85 | Fleet Health pill labels clip at low percentages — 33% read… | Medium | Testing | Kam | — | 2026-08-21 | Kam (browser verify, RD-76) | Fix live; visual check needs a browser |
| RD-99 | gitleaks path allowlist creates three silent blind spots (p… | Medium | Testing | Kam | operations, security | 2026-08-23 | Kam (QA/close) | Fixed 6c4b451 |
| RD-100 | npm test reports success while running zero tests — devDepe… | Medium | Release Ready | Kam | operations | 2026-08-26 | Kam (close) | Verified 08-20 with a failing control |
| RD-101 | CI test gate is decorative — build.yml runs the suite with… | Medium | Release Ready | Kam | operations | 2026-08-20 | Kam (close) | Gate seen red in CI 08-20 |
| RD-102 | 57 tracked .sh files are non-executable in git (core.fileMo… | Medium | Release Ready | Kam | operations | 2026-08-20 | Kam (close) | Both criteria discharged 08-20 |
| RD-103 | Four npm scripts point at root-level shell scripts that hav… | Medium | Testing | Kam | operations | 2026-08-22 | Kam (QA/close) | Landed 5743494 |
| RD-105 | 15 tracked shell scripts have no reference anywhere in the… | Medium | Testing | Kam | operations | 2026-08-23 | Kam (close) | Last criterion closed via RD-112 |
| RD-108 | session-or-jwt-secret-inline misses quoted JSON/JS syntax —… | Medium | Testing | Kam | operations, security | 2026-08-22 | Kam (QA/close) | Fixed 67ad264 |
| RD-111 | gitleaks dir . scans gitignored files — the local pre-commi… | Medium | Testing | Kam | operations, security | 2026-08-24 | Kam (close) | AC-2 record-only per Kam's 08-24 card |
| RD-112 | scripts/setup-encryption.sh offers to overwrite .env and wr… | Medium | Testing | Kam | operations, security | 2026-08-23 | Kam (close) | Deleted per ruling, 9f4db34 |
| RD-114 | health-check.sh requires static/upload.html, a file that ha… | Medium | Testing | Kam | operations | 2026-08-23 | Kam (close) | Done 99bc5ad |
| RD-120 | Running demo revision still carries AZURE_WORKSPACE_ID=8dbc… | Medium | Testing | Kam | operations | 2026-08-24 | Kam (accept) | Dead-workspace vars removed |
| RD-125 | Retention sweep is a permanent no-op for feedback — routes/… | Medium | Testing | Kam | compliance, operations | 2026-08-27 | Kam (accept) | Live audit line confirmed 08-27 |
| RD-128 | Export CSV → Job History ignores the Copy Only / Fax Only f… | Medium | Testing | Kam | operations | 2026-08-27 | Kam (accept) | Deployed 1.21.0 |
| RD-129 | A dead Jira token reads as an empty board, not an error — j… | Medium | Testing | Kam | operations | 2026-08-27 | Kam (close) | jira-query.sh gate landed 9cdd5ca |
| RD-130 | HealthSweeperScheduler still probes the decommissioned 4.x… | Medium | Testing | Kam | operations | 2026-08-27 | Kam (accept) | Both halves observed live |
| RD-135 | Feedback #4 (2026-09-01, Settings): tie into Entra for busi… | Medium | Testing | Kam | needs-decision, operations | 2026-09-01 | Kam (QA accept) | needs-decision label; refine round 2 pushed c1fe9ea, SCIM OFF |
| RD-136 | Sustainability Analytics (spec v1.0) — commission parent: s… | Medium | Release Ready | Kam | operations | 2026-09-02 | Kam (accept/close) | Deployed to demo 09-01, rev 0000092 |
| RD-137 | Sustainability: Settings tab to define costs + configurable… | Medium | Release Ready | Kam | operations | 2026-09-02 | Kam (accept/close) | Deployed to demo 09-01 |
| RD-138 | Sustainability: dashboard tab — MVP KPI set with evidence c… | Medium | Release Ready | Kam | operations | 2026-09-02 | Kam (accept/close) | Deployed to demo 09-01 |
| RD-139 | Sustainability KPI reader has no SQL date filter and caps a… | Medium | In Progress | Kam | operations | 2026-09-01 | Kam (QA) | Fixed ef9859d on branch; 'move to Testing' |
| RD-147 | Dark mode leaves .table-title at 1.55:1 — 16 headings acros… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Folded into RD-159 commit 0c4ea07 |
| RD-158 | P6-02: wizard surfaces painted from inline-styles-extracted… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Round 7 items 2/4, a0d5dfd |
| RD-165 | Dark-mode counterparts keyed to extracted .s-xxxxxxxx hashe… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 3d4b789 |
| RD-170 | Bootstrap's .btn-outline-primary/.btn-outline-secondary hav… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | a0d5dfd |
| RD-171 | .result-box.warning is set from JavaScript in four places a… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 6b78315 |
| RD-172 | tests/e2e/dark-mode-contrast.spec.js has no settle conditio… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | 0ef10d9 |
| RD-179 | Bootstrap's success/danger/secondary family has no dark cou… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | e2b2341 |
| RD-185 | RD-172's determinism criterion compares five EMPTY lists at… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | f876732 |
| RD-186 | input#aiQuery is a white box on the dark dashboard, and NO… | Medium | Testing | Kam | operations | 2026-09-02 | Kam (QA) | f876732 |
| RD-56 | Toner-pill width class is a broken template-literal — two F… | Low | Release Ready | Kam | — | 2026-08-20 | Kam (browser verify, RD-76) | Fix live on rev 0000084; needs a dashboard look |
| RD-113 | scripts/health-check/ documents ./health-check.sh but does… | Low | Testing | Kam | operations | 2026-08-23 | Kam (close) | Done 99bc5ad |
| RD-140 | costPerSheetSimplex is a dormant cost setting — API-writabl… | Low | In Progress | Kam | operations | 2026-09-01 | Kam (QA/close) | Retired, not wired |
| RD-161 | formatCurrency(136.345) renders $136.34 while the KPI tile… | Low | Testing | Kam | operations | 2026-09-02 | Kam (QA) | Fixed 6b78315 |

## Datasec/HPSM

Jira project `HPSM` on `team-1634009483756.atlassian.net` · `project = HPSM AND statusCategory != Done ORDER BY key ASC` · read 2026-09-02 · **26 open** · category 1 / 2 / 3 = 4 / 17 / 5 · Kam-assigned 0.

### 1. In our hands — ready to action (4)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| HPSM-37 | T30: [KAM TOP PRIORITY] Purview/Compliance Manager scoring… | Highest | Backlog | — | — | 2026-08-20 | Kam's TOP PRIORITY; O1 continuation under his get-ahead grant — mechanism specified, work continues |
| HPSM-12 | T7: SOW execution & prerequisite tracker | Medium | Backlog | — | — | 2026-08-20 | SOW execution tracker, current to 08-20; ours to keep current |
| HPSM-19 | T14: Weekly programme status + prerequisite chase list | Medium | Backlog | — | — | 2026-08-20 | Weekly status W0 current to 08-20; next issue is ours |
| HPSM-20 | T15: HP Amplify launch alignment - 5-10 Dec 2026 (six-day e… | Medium | Backlog | — | — | 2026-08-17 | Amplify 5–10 Dec; date fact recorded, register alignment ours |

### 2. Requires input (17)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| HPSM-38 | T31: [CLINIC - DATE UNSET] Which deployment topology? Kam's… | High | Backlog | — | — | 2026-08-18 | HP (clinic date) | Working paper filed; clinic decides |
| HPSM-40 | T33: [KAM - 2 MIN] K5 analysis repo - local commit DONE (96… | High | Backlog | — | — | 2026-08-20 | Kam (2-min gh device flow) | K5 repo committed locally; remote needs Kam |
| HPSM-1 | HPSM Epic: Project Setup & Environments | Medium | Backlog | — | — | 2026-08-12 | HP (SOW signature) | Epic container; environments follow signature + HPSM-8 |
| HPSM-2 | HPSM Epic: Commercial & Document Hygiene | Medium | Backlog | — | — | 2026-08-12 | HP (SOW signature) | Epic container |
| HPSM-3 | HPSM Epic: Architecture Refinement Session | Medium | Backlog | — | — | 2026-08-12 | HP (clinic date) | Epic container; clinic unscheduled |
| HPSM-4 | HPSM Epic: Content & Data Prerequisites | Medium | Backlog | — | — | 2026-08-12 | HP (asks) | Epic container |
| HPSM-5 | HPSM Epic: Programme Coordination | Medium | Backlog | — | — | 2026-08-12 | HP (SOW signature) | Epic container |
| HPSM-8 | T3: Dev environment decision record | Medium | Backlog | — | — | 2026-08-12 | Kam (dev-environment/tenant decision) | Decision record not started |
| HPSM-9 | T4: [RULED 2b] SOW-01 s.14 payment-table correction — folds… | Medium | Backlog | — | — | 2026-08-12 | Kam (next HP conversation) | Ruled 2b 08-12: folds into Kam's HP conversation |
| HPSM-15 | T10: [CLINIC - DATE UNSET] D01 Architecture & Delivery Base… | Medium | Backlog | — | — | 2026-08-20 | HP (clinic date) | D01 v0.6, 47 verdict slots, clinic unscheduled |
| HPSM-21 | HP asks register - [KAM RULED 2(b) 08-20: M0 day-one accept… | Medium | Backlog | — | — | 2026-08-24 | HP (open asks) | API ask answered 08-24 (doc 26_0172); H3 and Data Protection evidence still open with HP |
| HPSM-25 | T19: [RE-DERIVED 08-18 - AMPLIFY NOW MISSED ENTIRELY] Signa… | Medium | Backlog | — | — | 2026-08-18 | HP (signature date) | Release 15–18 Dec; Amplify missed on the 25–28 Aug signature premise |
| HPSM-26 | T20: [KAM - PRD re-issue + P06] Assessment model defects -… | Medium | Backlog | — | — | 2026-08-16 | Kam (PRD re-issue + P06) | Defect reframed 08-16; Kam carries to HP |
| HPSM-27 | T21: [KAM-RULING] criticalSolution posture - telemetry guar… | Medium | Backlog | — | — | 2026-08-15 | Kam (ruling) | Approval-class; readiness done, ruling not given |
| HPSM-28 | T22: [CLINIC - DATE UNSET] Tenant isolation is a FOUR-layer… | Medium | Backlog | — | — | 2026-08-17 | HP (clinic date) | Clinic decision D-07 |
| HPSM-31 | T25: [CLINIC - DATE UNSET] HP tools & operational model reg… | Medium | Backlog | — | — | 2026-08-17 | HP (clinic date) | Clinic item |
| HPSM-35 | T28: [KAM RULED 1(b) 08-20 - SIGN AS-IS] Post-signature ali… | Medium | Backlog | — | — | 2026-08-20 | HP (post-signature alignment) | Ruled 1(b) sign as-is; clause pack negotiated post-signature |

### 3. Done on our side — awaiting approval (5)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|
| HPSM-41 | T34: [KAM RULED 2026-08-24 - RAISE THE s13 CR] HPSM REST AP… | Highest | Backlog | — | — | 2026-08-24 | Kam (raise at execution) | Ruled 08-24; CR drafted into the R1–R6/W1–W5 bundle, fires at execution |
| HPSM-29 | T23: [KAM - PRD re-issue] PRD s.14 marks AI capabilities PO… | Medium | Backlog | — | — | 2026-08-15 | Kam (carry H8 to HP) | M6 AI acceptance-criteria proposal delivered 08-15 |
| HPSM-30 | T24: [KAM - H9] Rollback is TWO capabilities - narrow defin… | Medium | Backlog | — | — | 2026-08-15 | Kam (carry H9 to HP) | Rollback-scope proposal delivered 08-15 |
| HPSM-32 | T26: [SIGN-OFF ~08-25/28 - FREE AGAIN] CT s16 warranty retr… | Medium | Backlog | — | — | 2026-08-20 | Kam (take W1–W5 to HP) | Warranty clause drafted 08-20; travels with R2 |
| HPSM-39 | T32: [KAM-REQUESTED] Review fully-localized AI models for c… | Medium | Backlog | — | — | 2026-08-20 | Kam (accept) | Localised-model review + continuity addendum delivered 08-20 |

## Datasec/ATTIO

Jira project `ATTIO` on `team-1634009483756.atlassian.net` · `project = ATTIO AND statusCategory != Done ORDER BY key ASC` · read 2026-09-02 · **16 open** · category 1 / 2 / 3 = 6 / 6 / 4 · Kam-assigned 0.

### 1. In our hands — ready to action (6)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| ATTIO-2 | E0 — Foundations | Medium | To Do | — | — | 2026-08-21 | E0 epic container |
| ATTIO-3 | E1 — Integrate: Vision → Attio | Medium | To Do | — | — | 2026-08-21 | E1 epic container |
| ATTIO-4 | E2 — Deploy on Datasec infrastructure | Medium | To Do | — | — | 2026-08-21 | E2 epic container |
| ATTIO-5 | E3 — Train: people, best of both systems | Medium | To Do | — | — | 2026-08-21 | E3 epic container |
| ATTIO-23 | Bridge monitoring + runbook | Medium | To Do | — | — | 2026-08-21 | — |
| ATTIO-26 | Training materials from real screens | Medium | To Do | — | — | 2026-08-21 | Needs real screens — after the pilot |

### 2. Requires input (6)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| ATTIO-8 | [KAM] Entra admin consent for Attio (M365 email/calendar sy… | Medium | To Do | — | — | 2026-08-21 | Kam (Entra admin consent) | [KAM] tagged |
| ATTIO-10 | [KAM] Enterprise pricing enquiry (Entra SSO/SAML + SCIM) | Medium | To Do | — | — | 2026-08-21 | Kam (pricing enquiry) | [KAM] tagged |
| ATTIO-15 | Custom object: Quotes (Pro tier gate) | Medium | To Do | — | — | 2026-08-21 | Kam (tier/dispose) | Free-tier object cap; dispose/park recommended on ATTIO-19 |
| ATTIO-24 | Pilot: Kam + 1-2 reps on dev workspace with migrated real d… | Medium | To Do | — | — | 2026-08-21 | Kam (+1–2 reps) | Pilot needs people |
| ATTIO-25 | Side-by-side period (weeks 3-6) + weekly feedback loop | Medium | To Do | — | — | 2026-08-21 | Kam (+reps) | Sequenced after the pilot |
| ATTIO-27 | Cutover review against exit criteria | Medium | To Do | — | — | 2026-08-21 | Kam | Cutover review after side-by-side |

### 3. Done on our side — awaiting approval (4)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|
| ATTIO-16 | Port the 13 email templates; build sequences for pre/post c… | Medium | In Progress | — | — | 2026-08-22 | Kam (fill content, accept) | Implemented + tested 2ddaa7a; [[FILL]] content markers are Kam's |
| ATTIO-19 | Quote round-trip proof (3 real quotes) | Medium | To Do | — | — | 2026-08-24 | Kam (close) | Recommendation: close — zero leads have ever had a quote |
| ATTIO-29 | Daily follow-up workflow — uncontacted / upcoming renewals… | Medium | In Review | — | — | 2026-08-23 | Kam (accept/close) | Four defects fixed, deployed, proven live 08-23 |
| ATTIO-30 | Standard sales reporting pack — per-stage, total pipeline,… | Medium | In Review | — | — | 2026-08-23 | Kam (one UI filter, then close) | Report 2 filter is a UI-seat change (no API surface) |

## Datasec/CypherKey

Jira project `CPKEY` on `team-1634009483756.atlassian.net` · `project = CPKEY AND statusCategory != Done ORDER BY key ASC` · read 2026-09-02 · **28 open** · category 1 / 2 / 3 = 21 / 5 / 2 · Kam-assigned 0.

### 1. In our hands — ready to action (21)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| CPKEY-9 | KeyMap engine, RNG/entropy, registration HSM op, randomness… | Medium | In Progress | — | phase-1, roadmap | 2026-06-28 | Phase-1 epic |
| CPKEY-10 | .NET auth core: serial issuance, hash-verify, activation wi… | Medium | In Progress | — | phase-1, roadmap | 2026-06-28 | Phase-1 epic; local stack verified |
| CPKEY-11 | Swift + Kotlin apps: QR registration, device tokenisation,… | Medium | In Progress | — | phase-2, roadmap | 2026-06-28 | Phase-2 epic |
| CPKEY-12 | Both options: EAM second-factor AND federated passwordless… | Medium | In Progress | — | phase-3, roadmap | 2026-06-28 | Phase-3 epic |
| CPKEY-13 | Tenant/user/device/cert lifecycle, connector config, audit… | Medium | In Progress | — | phase-4, roadmap | 2026-06-28 | Phase-4 epic; mTLS done 06-28 |
| CPKEY-14 | IaC, Container Apps/AKS, Managed HSM + Key Vault, WAF, obse… | Medium | In Progress | — | phase-5, roadmap | 2026-06-28 | Phase-5 epic |
| CPKEY-15 | Lower-assurance fallback: on-demand KeyMap generated in HSM… | Medium | In Progress | — | phase-6, roadmap | 2026-06-28 | Phase-6 epic |
| CPKEY-23 | Registration HSM operation | Medium | In Progress | — | phase-1, roadmap | 2026-06-24 | — |
| CPKEY-38 | IaC + environments (Bicep/Terraform) | Medium | In Progress | — | phase-5, roadmap | 2026-07-03 | Hardened IaC still open; ACA demo env kept warm |
| CPKEY-39 | Managed HSM + Key Vault + managed identities | Medium | In Progress | — | phase-5, roadmap | 2026-07-16 | Component N1 of hardened arch; SoftHSM path chosen 06-30 |
| CPKEY-40 | WAF + private networking + observability | Medium | In Progress | — | phase-5, roadmap | 2026-07-06 | Observability slice done 07-06; WAF/private networking open |
| CPKEY-46 | IRAP prep + NIST 800-53 mapping + evidence pack | Medium | In Progress | — | phase-7, roadmap | 2026-07-16 | Evidence pack in progress |
| CPKEY-49 | Prod HSM (PKCS#11) + QRNG DRBG: replace in-memory reference… | Medium | In Progress | — | roadmap, security | 2026-07-16 | Component N2; QRNG hardware would be Kam's purchase |
| CPKEY-54 | PILLAR D: Live HSM op + DRBG via PKCS#11/SoftHSM | Medium | In Progress | — | — | 2026-06-30 | SoftHSM production approach |
| CPKEY-75 | Client onboarding wizard: guided environment deployment, us… | Medium | In Progress | — | — | 2026-06-27 | Wizard epic; slice live |
| CPKEY-156 | N4: post-quantum transport — hybrid ML-KEM TLS + crypto-agi… | Medium | To Do | — | hardened-arch | 2026-07-16 | N4 |
| CPKEY-157 | N5: hardware-attested device keys — verify Secure Enclave /… | Medium | To Do | — | hardened-arch | 2026-07-16 | N5 |
| CPKEY-161 | iOS: visible activation-window countdown + expiry messaging… | Medium | To Do | — | — | 2026-08-02 | Gates CPKEY-93 |
| CPKEY-162 | Top-up ceremony: low-watermark warning is a dead end on bot… | Medium | To Do | — | — | 2026-08-02 | Gates CPKEY-93 |
| CPKEY-163 | Android parity pass: push auto-open (CPKEY-138), KeyMap gri… | Medium | To Do | — | — | 2026-08-04 | Fail-closed posture ruled 08-04 |
| CPKEY-164 | iOS parity pass: name the relying party on the challenge sh… | Medium | To Do | — | — | 2026-08-02 | — |

### 2. Requires input (5)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| CPKEY-16 | External pen test, quantum/supercomputer red-team, IRAP pre… | Medium | To Do | — | phase-7, roadmap | 2026-06-24 | Kam (money, vendors) | Phase-7 epic: pen test, red-team, IRAP |
| CPKEY-44 | External penetration test + remediation | Medium | To Do | — | phase-7, roadmap | 2026-06-24 | Kam (money, vendor) | External pen test |
| CPKEY-45 | Quantum/supercomputer red-team validation | Medium | To Do | — | phase-7, roadmap | 2026-06-24 | Kam (money, vendor) | Red-team validation |
| CPKEY-93 | Publish the OneTimePad apps to the App Store + Google Play | Medium | To Do | — | — | 2026-08-04 | Kam (sequenced after 161/162; store accounts) | Ruled 08-04 |
| CPKEY-165 | Rotate the Twilio auth token (demo SMS provider) - due 2026… | Medium | To Do | — | — | 2026-08-04 | Kam (Twilio console) | DUE 2026-09-04 — token rotation on the demo SMS provider |

### 3. Done on our side — awaiting approval (2)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|
| CPKEY-30 | iOS app MVP (Swift/SwiftUI) | Medium | In Progress | — | phase-2, roadmap | 2026-06-30 | Kam (test + accept MVP) | On Kam's iPhone via TestFlight since 06-30 |
| CPKEY-31 | Android app MVP (Kotlin/Compose) | Medium | In Progress | — | phase-2, roadmap | 2026-07-03 | Kam (accept MVP) | Full iOS parity 07-03 |

## Datasec/Vision_Sales_Portal (+QuickQuote)

Jira project `VSP` has **0 open** issues (64 total, all Done; read 2026-09-02); project key `WIL` is not visible to this token (Will's Linear, not accessible — per the QuickQuote BACKLOG). Backlog is **file-backed, no tracker**: `2_Project_Files/BACKLOG.md` (rows VSP-B*) and `Quoting Tool/hpas-quoting-tool/BACKLOG.md` (rows QQ-B*). Each unchecked `- [ ]` entry is one row; two entries recorded twice in the QuickQuote file are one row each (QQ-B4, QQ-B6). **28 open** · category 1 / 2 / 3 = 15 / 12 / 1. Row IDs are this report's own.

### 1. In our hands — ready to action (15)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| VSP-B1 | npm audit: 5 high remaining (archiver/minimatch/lodash, pat… | High | open | n/a (file) | — | 2026-08-04 | Own test pass; some want major bumps (express 5) |
| QQ-B5 | v2.20 on main but NOT deployed (PoC lines dropped) | High | open | n/a (file) | — | 2026-08-14 | Stale: v2.30 (v0.4.5) deployed 09-01 ships d258651, which postdates e711771 — verify and tick |
| QQ-B6 | stage3: 3 high advisories — extract-zip via puppeteer-core… | High | open | n/a (file) | — | 2026-09-01 | Recorded twice (08-14, 09-01); breaking bump on the PDF engine needs its own session + A4 print re-verify |
| QQ-B2 | Page scrolls sideways ~38px on a phone (.ticket summary tab… | Medium | open | n/a (file) | — | 2026-08-28 | Build, then Kam eyeballs the totals layout |
| QQ-B4 | No .dockerignore — image ships the builder's node_modules;… | Medium | open | n/a (file) | — | 2026-09-01 | Recorded twice in the file (08-26, 09-01); one row here. Own session + digest re-verify |
| QQ-B13 | Stage 3 hosted UI has no sign-out control | Medium | open | n/a (file) | — | 2026-08-11 | POST /auth/logout exists; UI half missing |
| QQ-B16 | Open sign-in makes /auth/request a mail-spray surface | Medium | open | n/a (file) | — | 2026-08-11 | Per-IP / global send budget |
| QQ-B3 | Logo ink inset drifts ~2px once the logo scales down | Low | open | n/a (file) | — | 2026-08-28 | Known 2px; won't-fix candidate |
| QQ-B14 | QA F3: standard security headers absent (HSTS, CSP, XFO, no… | Low | open | n/a (file) | — | 2026-08-11 | Headers middleware is ours; Kam only prioritises |
| QQ-B17 | Session durability across container swaps unverified (ARRAf… | Low | open | n/a (file) | — | 2026-08-11 | Deploy-side swap test with affinity off |
| QQ-B18 | Emailed PDF FX provenance says 'seeded table' for a live cl… | Low | open | n/a (file) | — | 2026-08-10 | Attribution-only; client sends fxState |
| QQ-B19 | Seed FX rates are stale-able, no refresh or age warning | Low | open | n/a (file) | — | 2026-08-08 | — |
| QQ-B20 | Print fidelity is Chrome-only | Low | open | n/a (file) | — | 2026-08-08 | Verify one other engine |
| QQ-B21 | Datasec_QuickQuoteTool_v2.0.6_beta.html on Will's disk is b… | Low | open | n/a (file) | — | 2026-08-08 | Record only; no contact with Will (Kam 08-07) |
| QQ-B24 | strip.js success line reports chars but says 'bytes' | Low | open | n/a (file) | — | 2026-09-01 | Buffer.byteLength |

### 2. Requires input (12)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| QQ-B1 | Sign-in single point of failure: ACS managed-domain mail qu… | High | open | n/a (file) | — | 2026-08-26 | Kam (custom sending domain at go-live: DNS) | Cooldown shipped 08-26; the ruled second half is Kam's DNS |
| QQ-B10 | Custom Datasec sending domain (ACS) — name domain + 4 DNS r… | High | open | n/a (file) | — | 2026-08-10 | Kam (domain + DNS) | Go-live item; also lifts the ~30/hr cap |
| QQ-B15 | ACS managed domain caps mail at ~30/hour | High | open | n/a (file) | — | 2026-08-11 | Kam (custom domain) | Same fix as QQ-B10 |
| VSP-B3 | CI status unreadable — project GH_CONFIG_DIR unauthenticate… | Medium | open | n/a (file) | — | 2026-08-04 | Kam (gh auth login in a launcher shell) | Cross-client risk flagged |
| VSP-B4 | Key rotation — Lead_Bot side still pending (set new key, po… | Medium | open | n/a (file) | — | 2026-07-03 | Kam (HOLD ruling 08-06) | Same item as Lead_Bot (a) |
| QQ-B11 | MI + AcrPull instead of ACR admin creds | Medium | open | n/a (file) | — | 2026-08-10 | Kam (one-time Owner grant) | Go-live item |
| VSP-B2 | Local dev DB volume is PG15, compose image postgres:16 — wo… | Low | open | n/a (file) | — | 2026-08-04 | Kam (dev-data call) | Kam already ruled won't-fix on the same defect 07-03 (side-car); this 08-04 re-entry can be closed on that ruling |
| QQ-B7 | PoC deal threshold — exact boundary (5 vs \>5 vs 10) not ru… | Low | open | n/a (file) | — | 2026-08-14 | Kam (ruling) | One named constant; flagged 08-14 |
| QQ-B9 | Surface saved regional PS rates in the main UI | Low | open | n/a (file) | — | 2026-08-10 | Kam (ruling) | Proposed 08-10 (Kam's item 4) |
| QQ-B12 | Custom site domain (quickquote.datasec…) if wanted | Low | open | n/a (file) | — | 2026-08-10 | Kam (decide) | Go-live item |
| QQ-B22 | Printed POA tail still carries cents while amounts are whole | Low | open | n/a (file) | — | 2026-08-28 | Kam (customer-facing print change) | One argument at two call sites once ruled |
| QQ-B23 | Should printed RATES go whole-dollar too? | Low | open | n/a (file) | — | 2026-08-28 | Kam (ruling) | On-screen pane done (v2.28); printed rates never asked |

### 3. Done on our side — awaiting approval (1)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Approval needed from | Note |
|---|---|---|---|---|---|---|---|---|
| QQ-B8 | F21 access word is a speed bump, not protection | Low | open | n/a (file) | — | 2026-08-11 | Kam (close the entry) | Posture ruled by-design 08-11 (QA F2); entry is a record, not work |

## Datasec/Lead_Bot

No tracker. Backlog is **file-backed**: `Lead_Bot/BACKLOG.md` (7 unchecked entries). **7 open** · category 1 / 2 / 3 = 1 / 6 / 0. Row IDs are this report's own.

### 1. In our hands — ready to action (1)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Note |
|---|---|---|---|---|---|---|---|
| LB-B4 | .env location does not match what config.js / docker-compos… | Medium | open | n/a (file) | — | 2026-08-06 | Propose launcher-managed copy or --env-file; build it |

### 2. Requires input (6)

| Ticket | Title | Pri | Status | Assignee | Labels | Last activity | Waiting on | Note |
|---|---|---|---|---|---|---|---|---|
| LB-B1 | (a) Point the bot at prod — SALES_PORTAL_URL still localhos… | High | open | n/a (file) | — | 2026-08-06 | Kam (HOLD ruled 08-06; waits on (b)) | Flipping it makes real leads go live |
| LB-B2 | (b) Locate any running Lead_Bot instance — may still hold t… | High | open | n/a (file) | — | 2026-08-06 | Kam (name the Azure tenant) | Needs az on a tenant not yet assigned (hard rule 4) |
| LB-B3 | No git repository for this project at all | High | open | n/a (file) | — | 2026-08-06 | Kam (gh auth login as datasecau) | Every file is one uncommitted copy |
| LB-B5 | DASHBOARD_URL has two contradicting definitions (code vs VS… | Medium | open | n/a (file) | — | 2026-08-06 | Kam (which document is right) | — |
| LB-B6 | Telegram and SMTP notification paths unconfigured | Medium | open | n/a (file) | — | 2026-08-06 | Kam (credentials) | CHAT_ID, SMTP_USER, SMTP_PASS empty |
| LB-B7 | No deploy key generated | Low | open | n/a (file) | — | 2026-08-06 | Kam (blocked behind LB-B3) | — |

### 3. Done on our side — awaiting approval (0)

_none_

## Secuura/Blockchain (Platform K)

Not re-queried. Reused from [2026-09-02_secuura-platform-k-open-tickets.md](2026-09-02_secuura-platform-k-open-tickets.md): 238 open (27 archived), category 1 / 2 / 3 = 129 / 49 / 60; Kam-assigned 132 of which 71 category-1 = 54%.

## Method and corpus

**Categories** (same rules as the Platform K report). 1 = unassigned or assigned to Kam, state open, and the newest comment shows no pending ruling, credential, money or external-human dependency — our agents can start it. 2 = the next action belongs to someone other than our agents: a Kam ruling/credential/money/identity, or a client human (HP; Stuart/Peter on Platform K). 3 = the work is built, pushed, deployed or delivered and the ticket waits on QA acceptance, a browser verification, a sign-off or a close. Where a ticket fitted two, the category names who must act next and the Note says so. Epic containers follow their programme's gate (HPSM epics → HP; ATTIO/CypherKey epics → ours). 'Assigned to Kam' = assignee email `kamil.kreiser@…` / `kreiser.org@…` or display name Kam/Kamil. The last column of the BLUF table counts tickets whose next actor is Kam, Wednesday or the agent (categories 1 and 3 plus category-2 rows waiting on Kam alone).

- **Datasec/NexusAI** — Jira REST `/rest/api/3/search/jql`, `project = RD AND statusCategory != Done ORDER BY key ASC`, `maxResults=100` with `nextPageToken`; pages [100, 31], last page `isLast: True`; total 131. Positive control `project = RD` returned ≥1 issue (RD-129 blindness guard) and `/myself` answered as `Kamil Kreiser`. Statuses included: To Do 60, Testing 50, Release Ready 10, Put on Hold 6, In Progress 5. Excluded: every status in the Done category. Comments read per issue via `/issue/{{key}}/comment` (all pages), sorted by `created` ascending, newest taken. Labels `needs-decision` / `blocker`: needs-decision on 9 RD tickets, blocker on 0.
- **Datasec/HPSM** — Jira REST `/rest/api/3/search/jql`, `project = HPSM AND statusCategory != Done ORDER BY key ASC`, `maxResults=100` with `nextPageToken`; pages [26], last page `isLast: True`; total 26. Positive control `project = HPSM` returned ≥1 issue (RD-129 blindness guard) and `/myself` answered as `Kamil Kreiser`. Statuses included: Backlog 26. Excluded: every status in the Done category. Comments read per issue via `/issue/{{key}}/comment` (all pages), sorted by `created` ascending, newest taken. Labels `needs-decision` / `blocker`: none on this board.
- **Datasec/ATTIO** — Jira REST `/rest/api/3/search/jql`, `project = ATTIO AND statusCategory != Done ORDER BY key ASC`, `maxResults=100` with `nextPageToken`; pages [16], last page `isLast: True`; total 16. Positive control `project = ATTIO` returned ≥1 issue (RD-129 blindness guard) and `/myself` answered as `Kamil Kreiser`. Statuses included: To Do 13, In Review 2, In Progress 1. Excluded: every status in the Done category. Comments read per issue via `/issue/{{key}}/comment` (all pages), sorted by `created` ascending, newest taken. Labels `needs-decision` / `blocker`: none on this board.
- **Datasec/CypherKey** — Jira REST `/rest/api/3/search/jql`, `project = CPKEY AND statusCategory != Done ORDER BY key ASC`, `maxResults=100` with `nextPageToken`; pages [28], last page `isLast: True`; total 28. Positive control `project = CPKEY` returned ≥1 issue (RD-129 blindness guard) and `/myself` answered as `Kamil Kreiser`. Statuses included: In Progress 17, To Do 11. Excluded: every status in the Done category. Comments read per issue via `/issue/{{key}}/comment` (all pages), sorted by `created` ascending, newest taken. Labels `needs-decision` / `blocker`: none on this board.
- **Datasec/Vision_Sales_Portal** — Jira `VSP` via the project's own token: `project = VSP` → 64 issues, every one in status Done (single page, `isLast: true`); `project = WIL` → positive control empty and `WIL` absent from the token's visible project list (36 projects), so it is not a Jira project on this site. File-backed rows read from the two BACKLOG.md files (136 and 676 lines) on 2026-09-02; only unchecked `- [ ]` entries counted; the 'Parked deliberately' and 'must not reverse' sections are not tickets.
- **Datasec/Lead_Bot** — no tracker key in its `.env`; `Lead_Bot/BACKLOG.md` (85 lines, 7 unchecked entries).
- **Secuura/Blockchain** — reused; see that report's Method section.
- **Not measured.** GitHub PR states were not read for any project (no `gh` identity is used from this seat). Jira issue descriptions were not read — classification rests on summary, status, labels and the newest comment. The RD `--count` cap (RD-141) was bypassed by paginating the REST search directly; the count of 131 was made by this report, not by `jira-query.sh`.
- **Unread from this seat:** nothing — every project either answered its board read or has no board. Will's Linear (`WIL-*`) is unreachable by design (Kam's no-contact ruling) and is not counted.

## Sources

- Jira site `team-1634009483756.atlassian.net`, projects RD, HPSM, ATTIO, CPKEY, VSP — read 2026-09-02T07:47:13Z with each project's own read token from its `4_Credentials/.env` (sourced in a subshell, never printed).
- `!CODING/Datasec/NexusAI/2_Project_Files/scripts/jira-query.sh` — auth/endpoint pattern (read only).
- `!CODING/Datasec/Vision_Sales_Portal/2_Project_Files/BACKLOG.md`, `!CODING/Datasec/Vision_Sales_Portal/Quoting Tool/hpas-quoting-tool/BACKLOG.md`, `!CODING/Datasec/Lead_Bot/BACKLOG.md`.
- `0_Brain/reference/reports/2026-09-02_secuura-platform-k-open-tickets.md` (Platform K numbers).
