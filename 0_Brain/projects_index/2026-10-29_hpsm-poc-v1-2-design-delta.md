---
date: 2026-10-29
type: design-delta (read-only draft for Tuesday)
project: Datasec / HPSM-POC (Jira HPSMPOC)
source_design: 0_Brain/reference/2026-10-29_hpsm-poc-hp-feedback/HP_Security_Services_Playbook_Prototype_v1_2.html (313 lines, 172,396 bytes, read whole)
source_notes: Click-through_271026_pete_-_AI_summary.docx (read whole; AI-generated, checked against the HTML below)
app_read: datasecau/HPSM-POC main c00e28284e9acacf16462ea3c2b533936b3db210 (fetched as tarball: SSH clone was refused "Permission denied (publickey)" under the project gh config; `gh api` tarball used instead, so no git history, sha confirmed via `gh api commits/main`)
status: DRAFT. Nothing created in Jira. Nothing built. Nothing sent to HP.
---

# HPSM-POC: v1.2 design vs the app at c00e2828

All CSS facts below are READ FROM THE CSS TEXT, not rendered (no browser was opened, per the brief). Anything that needs a rendered measurement says UNMEASURED.

## 1. BLUF

- **Big, but narrow.** The change is one new application shell (left sidebar, top bar) plus a visual restyle. Most screens the HTML shows already exist in the app with the same function (Customers, Engagements, journey steps, customer tabs, Action plan, Services, Revenue; judged by file and header, not line-diffed); the app is richer than the prototype (sort, mobile cards, audit notes, AI narrative, URLs). New content in the HTML is: two partner pages (My readiness as a page of its own, Training & playbooks), one contested page (Good / Better / Best packages), and a whole **Customer security workspace of 8 views** with a Partner/Customer switch.
- **30 proposed tickets**: 23 BUILD-NOW (1 shell first, then 22) and 7 GATHER (not built). **Up to 16 file-disjoint page lanes** can run in parallel, but only after the shell lane (L0) lands; realistic concurrency for the machine and review gates is 8 to 10, in two waves.
- **Most likely to go wrong:** this reverses Kam's own ruling B169 (2026-10-06 19:36, "nest the side elements into a burger menu", code and a Playwright spec built on "no left rail at any width"), and the layout uses viewport breakpoints (`lg:`, `xl:`) that assume the page owns the full width; a 228 px sidebar makes every two- and three-column screen cramped at 1024 to 1280 px unless each lane re-tunes its breakpoints.
- Second risk: the prototype's greys fail the project's WCAG gate (muted text 3.27:1, captions 2.4:1, measured below). Adopt layout and proportions, **not** the prototype's colours or its 9 to 13 px type.

## 2. Design delta, screen by screen

### 2.1 Shell (the priority)

| Aspect | v1.2 prototype (cite) | Current app (cite) | Verdict |
|---|---|---|---|
| Menu location | `aside.sidebar#app-sidebar` `aria-label="Primary navigation"`, sticky, left, `width:228px; height:100vh; background:var(--navy)=#0a2940`, `padding:22px 9px 10px`, scrolls (`overflow:auto`) | No rail. `components/shell/AppShell.tsx`: a "Menu" burger in the header opens `GlobalNav` as a panel over the page (B169). `aria-label="Main"` | MOVES to left column. Reverses B169. |
| Collapse | `.sidebar-toggle` (39x39, in the top bar) and `.sidebar-hide` (chevrons, in the brand row) both call `setSidebar`; state in `localStorage['hpsc-security-playbook-nav-v1']`; `.app.sidebar-closed>.sidebar{width:0}`; `aria-expanded`, `aria-controls`, `inert` + `aria-hidden` when closed; Escape closes (<=860 px only) and returns focus to the toggle | Burger toggles; Escape closes and refocuses burger (AppShell.tsx l.134-140); closes on outside click and on blur | KEEP the app's behaviours (Escape, focus return, outside click only in drawer mode). The prototype's hybrid (persistent but hideable) also honours Kam's burger instinct. |
| Mobile | <=860 px: `position:fixed; width:245px; z-index:31` drawer with `.nav-backdrop` (rgba(6,27,44,.54)); closes on navigate; default closed. (The v1.0 icon-only 70/54 px rail is overridden by v1.1 `!important` rules, so it is dead CSS.) | One burger at every width | NEW drawer + backdrop below 860. Focus trap is not in the prototype: ADD (UNMEASURED whether `inert` on the page behind is enough). |
| Brand block | `.brand`: white 48x48 tile with HP mark (`hpLogo(38)`), "HPSC" (21px/820), "HP SECURITY SERVICES" (9px). **Logo is hot-linked from upload.wikimedia.org with a base64 fallback** (HP_LOGO_SOURCE) | `HpLogo.tsx`: product owner's supplied PNG (2026-10-26), static import, `/workspace` link in the header | KEEP the owner's logo (`HpLogo`/`HpMark`); do NOT hot-link Wikimedia (runtime external fetch, CSP, brand). Brand text "HPSC" is the prototype's own; wording to confirm (GATHER branding). |
| Grouping, Partner | `MENU_SPEC.partner`: PARTNER WORKSPACE (Dashboard, My readiness, Training & playbooks) / CUSTOMER DELIVERY (Customer engagements, Assessment pipeline, Action plan) / SERVICE GROWTH (Good / Better / Best, Delivery phases, Revenue & proposals) / TOOLS & SUPPORT (Resources & modules, Automation metrics, Attribution preview, Administration). Group labels `.nav-section` 10px/850, `#6fa8c9` | Flat list, no groups: Home, Customers, Engagements, Action plan, Service offers, Assessments, Revenue, Resources (+ role extras). `GlobalNav.tsx` `MAIN_NAV` | NEW grouping + 4 new entries, 3 renamed (see matrix). |
| Customer workspace menu | `MENU_SPEC.customer`: SECURITY WORKSPACE (Security dashboard, Fleet & devices, Security assessments, Gaps & findings) / GOVERNANCE & REMEDIATION (Framework alignment, Remediation roadmap, Reports & evidence, Continuous assurance). `.side-mode` banner "CUSTOMER SECURITY" | none | NEW (8 routes). |
| Active state | `.nav-item.active{background:#244e6c; box-shadow:inset 3px 0 #18a4d7}`; `aria-current="page"` else `"false"` | `bg-primary text-on-primary`; `aria-current` page or absent; "most specific match wins" (`currentItem`) | KEEP the app's `currentItem` logic (the prototype only compares `ui.page`). Restyle to the left accent bar. `aria-current="false"` is redundant; omit. |
| Item size | `.nav-item` min-height 40px, 12px type, 17px icons | `min-h-11` (44px), 16px | KEEP 44px targets (WCAG 2.5.8 margin the app already holds). |
| Sidebar footer | `.sidebar-bottom`: WORKSPACE TOOLS (Export workspace JSON, Import local JSON, Send feedback), `.side-info` "Local demonstration", version line | Feedback is a floating pill (`FeedbackButton`, B104/C-42), sign-out and reset in header (`AppShell.tsx` l.105-125, l.172) | REMOVE export/import (the app is API-backed; those exist only because the prototype is local-storage). KEEP the feedback pill (the prototype also has `.feedback-fab` bottom-right). Account controls need a home: UNRESOLVED (see below). |
| Top bar | `.topbar` min-height 68, white, `border-bottom:1px solid var(--line)`, padding 12/28: left = toggle + `.top-title` ("HP SECURITY SERVICES / PARTNER / CRUMB" + bold page or customer name); right = `REVIEW / LOCAL` pill, **workspace switch** (Partner / Customer), **role `<select>`** (Partner, Consultant, Admin, Demo, Customer), **customer `<select>`**, **+ New customer** | Header: burger, logo link, Account nav with role badge (`data-testid="role-badge"`), Reset demo, Sign out. Breadcrumbs live in `CustomerShell` | Top bar content is mostly NEW. Role select and workspace switch: see 2.1b. |
| Content width | `.content{max-width:1530px; padding:25px 28px 45px}` | pages: `mx-auto max-w-7xl` (1280px) px-4/md:px-6 | Stay as is; pages are already `mx-auto w-full`, so they need no edit for the shell itself. |
| Banners | Per-page `.notice` boxes with an "i" tooltip; `.view-kicker` | ONE prototype banner per page (`PrototypeBanner.tsx`, C-27 b ruling) | KEEP the app's single banner (a Kam ruling). Do not copy the per-page notices. |
| Page header | `head(eyebrow,title,lede,buttons)`: `.eyebrow` 10px caps blue, `.page-title` 24px/790, `.lede` 12px muted max 770px, `.header-buttons` right | `ui/PageHeader.tsx`: eyebrow, `h1` (3xl bold, takes focus on client nav), tags, lead, actions | SAME pattern. Restyle only. KEEP focus-on-h1 behaviour (WCAG 2.4.3) and `tabindex=-1`. |
| Metric cards | `.cards4` 4 columns -> 2 at 1250 -> 1 at 620; `.metric` icon tile top right | `partner/parts.tsx` `KpiTile` | SAME pattern. |
| Buttons | `.btn` 11px, min-height 36; `.btn.small` 30 | `ui/Button.tsx` min-h-11 | KEEP 44. |
| Modals | `.modal-wrap` fixed, `role=dialog aria-modal`, Escape closes | `followup/ModalDialog.tsx` exists | no change |
| Print | hides `.sidebar,.topbar,...` | `globals.css` hides `nav, .no-print`; `print-rules.test.ts` pins the parser | New `aside` must be `no-print` AND the content column must not keep an empty left margin; add a rule without `:not()` (HPSMPOC-142). |
| Breakpoints (read from CSS) | 1250, 1150, 1050, 860, 750, 620, 450 | Tailwind sm 640, md 768, lg 1024, xl 1280 | UNMEASURED how each screen reads with 228px taken off. Plan: sidebar persistent from 1024 up (prototype opens it above 860), drawer below; each page lane re-tunes `lg:`/`xl:` to the content width. Needs screenshots at 1024, 1180, 1280, 1440. |
| Type | root 13px, Inter stack (not loaded; falls back), 9 to 12px in tables, pills, captions | 16px body, system stack, rem scale | KEEP the rem scale. |
| Colour | `--blue:#087cbe`, navy `#0a2940`/`#123a57`, text `#102f45`, muted `#7991a6` | `brand.css` `--brand-primary:#1d4f91`; tokens in `styles/tokens.css`; branding "UNDECIDED" (QA-027, HPSMPOC-21) | Pete: branding is later. Only ADD sidebar tokens (navy family); do not swap the primary. |

**Measured contrast of prototype colours (python3, WCAG formula).** Muted text `#7991a6` on white 3.27:1; metric detail `#8ca3b5` 2.62; table sub-text `#94a9b9` 2.43; step-row text `#94aabc` 2.40; top-title `#7f99ad` 2.97; grey pill `#70879a` on `#eef2f6` 3.32; feedback pill white on `#e98419` 2.70. All fail AA 4.5:1 for small text, so `src/design/contrast.test.ts` would fail the build if adopted. Passing: nav label `#6fa8c9` on navy 5.78; nav item `#d4eaf9` on navy 12.06; active white on `#244e6c` 8.82; version line `#6c9fbd` on navy 5.22; primary button white on `#067dbc` 4.50 (borderline); link `#087cbe` on white 4.53. Current app comparators: `#1d4f91` on white 8.14; `#4a5568` 7.53.

#### 2.1a Role matrix (nav entries)

| Role | Current app (`GlobalNav.tsx`, 8 to 11 entries) | v1.2 (`MENU_ALLOWED`, `MENU_SPEC.partner`) |
|---|---|---|
| Partner | Home, Customers, Engagements, Action plan, Service offers, Assessments, Revenue, Resources (8; pinned by `playbook-burger-menu.spec.ts` KAMS_LIST) | Dashboard, My readiness, Training & playbooks, Customer engagements, Assessment pipeline, Action plan, Good / Better / Best, Delivery phases, Revenue & proposals, Resources & modules (10) |
| Consultant | Home, Customers, Engagements, Assessments, Revenue, Automation metrics, Attribution (Preview), Resources (8). **No** Action plan, **no** Service offers | Dashboard, My readiness, Training & playbooks, Customer engagements, Assessment pipeline, Good / Better / Best, Delivery phases, Revenue & proposals, Resources & modules, Automation metrics, Attribution preview (11). **Gains** Delivery phases and the two new partner pages; no Action plan. This matches Pete's "consultant covers every customer and the partner capabilities, plus audit and metrics". |
| Admin | all 11 (adds Admin) | all 13 (adds Action plan, Administration) |
| Demo | as Consultant (metrics allowed, `METRICS_ROLES`) | same list as Consultant |
| Customer (NEW role) | none | `Customer: []` partner menu; sees only the 8 customer pages; partner workspace refused with a toast; no feedback button (`.cust-only .feedback-fab{display:none}`) |

Consequence: Consultant and Demo gain access to Service offers (route `/services` is `PARTNER_SIDE` today). Check the BFF/API role rules (UNMEASURED: `x-roles` on those routes) before widening the menu; a nav entry must never promise a route the API refuses.

#### 2.1b Top-bar controls: what is real and what is demo furniture

- **Customer `<select>`** ("Select a customer"): NEW in the app. Pete questioned exactly this (switching customers inside a customer page). The HTML keeps it. See Pete item 4.
- **Role `<select>`**: the prototype changes role in-session. The app takes the role from sign-in (mock chooser in `SignInScreen.tsx` `MockSignIn`; four-level start page `UatStartScreen.tsx` on the UAT copy; Entra app role when hosted). In-session role switching must not exist on Entra-hosted. Classify: a mock/UAT-only convenience, GATHER (Pete's "optional role selector" is already met by the sign-in chooser).
- **Workspace switch Partner / Customer**: NEW. Needed only if the Customer workspace is built (2.14).
- **`REVIEW / LOCAL` pill**: replaced by the app's single prototype banner.
- **Sign out / Reset demo / role badge**: absent from the prototype and **required** by the app (`AppShell.tsx` l.105-125, Entra sign-out, Admin-only reset on hosted, `data-testid="role-badge"` used by 8 specs). Home UNRESOLVED: top bar right (as now) is the lowest-risk choice.

### 2.2 Partner dashboard

Prototype `partnerHome()` (the v1.2 `dashboard` override) vs `partner/PartnerDashboard.tsx` at `/home`.
- STAYS: four KPI tiles (readiness n/16, customers, reports, open actions), customer pipeline, three-phase motion.
- CHANGES: pipeline table sits left under the tiles with right column "Recommended next actions" (4 quick links) and "Practice readiness" card (`summary-columns` 1.55fr / 1fr, one column below 1050).
- REMOVED vs current: Welcome card with dismissible tip, "Where to next" card row, CTA band, "Upcoming activity" sample calendar, "Revenue mix" and "by stage" panels (the prototype has none of them).
- DECISION for Kam: the prototype's three phase boxes (ASSESS / IMPLEMENT / OPTIMISE, one sentence each) are a thinner version of the existing `home/PhaseFlow.tsx` that Kam specified from his own image (B170, 2026-10-06 19:42). Recommend KEEP PhaseFlow; take only the column layout.
- Terminology: the HTML writes OPTIMIZE in v1.1 `phaseCards()` and OPTIMISE in v1.2 `partnerHome()`; the app says "Phase 3: Managed service". GATHER (terminology).

### 2.3 Customers (register) and Engagements (assessment pipeline)

Prototype `customers()`, `customerTable()`, `customerFilters()`, `engagements()` vs `customer/CustomerManagement.tsx` (`/workspace`, `/customers`) and `EngagementsList.tsx`.
- The app already has search, industry, status, stage filters, sortable column headers, mobile cards, add-customer, devices/sites. The prototype adds: stage **chips** instead of a select, a **progress bar per row** (N of 16 answered), a sort control. 
- Progress per row needs "questions answered / 16" per customer: `useDirectory` rows carry a stage; whether the summary carries an answered count is UNMEASURED (`customer/directory.ts` not diffed). If it does not, show the engagement step count the Engagements page already computes (`journeyProgress`).
- Engagements: same columns in both (Customer, Stage, Progress, Next milestone, Last activity). Rename nav label to "Customer engagements" (Customers) and "Assessment pipeline" (Engagements). NOTE the prototype's label for the register is "Customer engagements" while the page itself is titled "Customers": confusing; confirm the words.
- The Demo alias (ORG-nnnnn) the prototype uses in `named()` already exists in the app (B208, `useCustomerShownAs`): KEEP.

### 2.4 Customer workspace frame

Prototype `customer()`: header card (name, `x / 16 captured`, `n draft findings`, stage chips) with tabs Overview, Assessment journey, Findings, Tasks, Documents, Coach vs `shell/CustomerShell.tsx` + `customer/tabs.ts` `CUSTOMER_TABS` (the same six tabs, same order). Delta:
- STAYS: six tabs, journey rail on step pages. The app's rail already numbers 8 work steps plus an unnumbered Metrics (WORK_STEPS in `engagement.ts`); the prototype's "EIGHT-STEP JOURNEY" list also shows 9 entries (Profile to Metrics), so the labels agree.
- CHANGES: rail drops the "Overview" entry (the app lists it first, `JOURNEY[0]`), is a white card with `position:sticky;top:15px`, width 226 (app: `lg:w-64` = 256px, un-boxed). Breadcrumbs (app) become the top bar title (prototype). KEEP the breadcrumbs: they carry customer link, finding name (B24 N-08) and alias rules; the prototype's top-title is a weaker substitute.
- Back button "<- Customer register" added.
- Rail breakpoint: the app switches rail to a `<details>` below `lg`; with the sidebar present that should become `xl`. UNMEASURED.

### 2.5 Journey steps (prototype `stepProfile` ... `stepMetrics`)

| Step | Prototype | Current file | Delta |
|---|---|---|---|
| 1 Profile | form grid, 2 columns, "Save profile" | `screens/ProfileScreen.tsx`, `customer/ApiProfile` | restyle only; the app also has the C-21 facts fields |
| 2 Assessment | question card + "All questions" list (right), group filter, Previous / Skip / Next, notes, "Create follow-up draft" | `screens/AssessmentScreen.tsx`, `snapshot/*` (`QuestionCard`, `QuestionMap`, `SnapshotRunner`, `useSnapshot`) | restyle only; follow-up exists (`followup/*`, real links, not a local draft) |
| 3 Score & findings | score ring, "By section: current vs target" bars, finding cards with Reviewed / Requires review | `screens/ResultsScreen.tsx`, `results/ResultsView.tsx`, `screens/FindingCard.tsx`, `customer/FindingDetail.tsx` | restyle only; the app already has override with audit note (stronger than the prototype's "mark reviewed") |
| 4 HP/HPSM recommendation | Good / Better / Best blocks | `screens/RecommendationScreen.tsx` (`TIERS`) | restyle only; "groupings only, no prices" already ruled (B56, HPSMPOC-95) |
| 5 Roadmap | four buckets + **Consultant action register** (owner, target date, state, evidence ref; "Verified complete" needs evidence) | `screens/RoadmapScreen.tsx` | buckets same; **register is NEW** (needs a store; precedent `partner/browser-store.ts`; API support UNMEASURED) |
| 6 Narrative | Regenerate / Approve | `screens/NarrativeScreen.tsx` | app is stronger (AI provenance, stale, review); restyle only |
| 7 Executive report | preview / HTML / mark issued | `screens/ReportScreen.tsx` | app produces the PDF; restyle only |
| 8 Next engagement | placeholder card, "Price: not shown" | `screens/NextEngagementScreen.tsx` | restyle only |
| Metrics | 4 tiles | `screens/MetricsScreen.tsx` | restyle only |
| Nav between steps | Previous and Next buttons (`stepNav`) | `shell/NextStep.tsx`: Next only | NEW: add Previous |

### 2.6 Customer tabs

Findings tab (`findingsPanel`) -> `ResultsScreen` at `/findings`: same. Tasks (`tasks()`: Overview, Checklist, Findings, Evidence, Guidance sub-tabs) -> `customer/FirmwareTask.tsx`: sub-tab structure of the app UNMEASURED (not diffed). Documents (`documents()`: type chips, Export HTML, Print, three client packs) -> `customer/DocumentGeneration.tsx` + `collateral/ClientPacks.tsx`: app is a superset. Coach (`coach()`: 5 talk tracks) -> `customer/ConversationCoach.tsx`: restyle.

### 2.7 Partner: My readiness (page of its own)

Prototype `partnerReadiness()`: 4 metric tiles, four **named blocks of four checkboxes** (Strategy and engagement / Assessment and expertise / Implementation and delivery / Managed service and growth), "Readiness interpretation" with bands 12-16 / 8-11 / 4-7 / 0-3, top-5 "learning priorities", link to the next step. Current: `/assessments` (`readiness/AssessmentsHub.tsx`) + `/assessments/readiness/[id]` (`ReadinessRunner.tsx`) + `/result`. The runner already scores the deck's 16 statements (C-14). Delta: relabel nav "My readiness" and restyle; the "learning priorities" panel is NEW (derive from unchecked statements, no new content). Pete's "step zero" is answered by placing this FIRST under PARTNER WORKSPACE.
The prototype's own area names differ from the v1.1 ones in the same file (`readinessGroups` vs the "Practice strategy / Delivery skills / ..." bar labels in `assessments()`); the app follows the deck (C-14, deck slide 99). Keep the deck's names.

### 2.8 Partner: Training & playbooks (NEW)

Prototype `partnerTraining()`: 3 steps (Discover & scope / Assess & verify / Advise & deliver), a six-row learning pathway whose rows open Playbook modules 0, 3, 5, 6, 7, 8, and an "Independent assessment principles" list (5 bullets). No current route. The pathway is navigation over existing modules; the five principles are new policy-like wording written by the prototype's author, **not** SME-supplied: rule "Do not invent security policy" (project CLAUDE.md) -> hold that bullet list (GATHER).

### 2.9 Good / Better / Best services (partner packages)

Prototype `partnerPackages()`: three "level cards" with item lists, a "Commercial motion" line ("One-time assessment ...", "Project + software + scoped recurring managed service"), a select-tier button, "Export draft service scope", software recommendations (HP Security Manager, Authentication Manager, Universal Print / HPAS, Nexus AI). Conflicts: (a) Kam 2026-09-29 "Tiers as groupings only (good/better/best), no prices" (B56 / HPSMPOC-95) and `TIERS_EXPLAINED`; (b) Pete asked what the tiers mean and whether they read as pricing; (c) it defines a **second** meaning for the same words (what the customer buys vs the recommendation grouping), which the HTML itself admits ("Two separate frameworks"); (d) product-licensing claims need HP/SME. -> **GATHER. Do not build.** Keep the nav slot out until decided.

### 2.10 Delivery phases / Service offers

Prototype `offers()` (three phase cards, offer sheet with PLACEHOLDER rows) vs `partner/ServicesHub.tsx`, `OfferSheet.tsx`, `ImplementationScreen.tsx`, `ManagedServiceScreen.tsx`, `/services/*`. App is richer (sample engagements, trackers). Restyle only; rename nav "Delivery phases".

### 2.11 Revenue

Prototype `revenue()` (5 inputs, 4 tiles, 3 bars, CSV export) vs `RevenueCalculator.tsx`, `RevenueResults.tsx`, `OneCustomerEstimate.tsx` (richer, three-year model, scenarios). Restyle only; rename "Revenue & proposals" (no proposals feature exists: wording GATHER).

### 2.12 Action plan

Prototype `actionPlan()` (4 tiles, table with status select, Add / Remove, supporting-resource buttons) vs `partner/ActionPlanScreen.tsx` (415 lines; richer). Restyle only.

### 2.13 Resources & modules

Prototype `resources()`: header + grid of 11 module cards; `moduleText()`: overview card + "Related steps" card, "All modules", "Next module"; **no module rail** on a module page. Current: `playbook/layout.tsx` -> `PlaybookShell.tsx` puts a 288px left module rail (with viewed progress bar) beside every playbook page, and `PlaybookHome.tsx`. With the new sidebar that is a **second left rail**: remove the rail, use the grid on `/playbook`, keep prev/next on `ModuleScreen` (already has `prev`/`next`). The "N of 11 viewed" chip survives from the rail progress.

### 2.14 Metrics, Attribution, Administration

- Metrics: prototype `metrics()` (4 tiles, per-assessment table) vs `screens/MetricsDashboardScreen.tsx`: restyle only. 
- Attribution: prototype is a 3-step text card; the app has `AttributionPreviewScreen.tsx` (B202, labelled preview, synthetic data): KEEP the app's. Pete: scope questions are GATHER.
- Administration: prototype merges "Feedback received" and a "Content and connections" status list into one page; the app has `/admin` (a placeholder) and `/admin/feedback` (built, with attachments). Delta: fill `/admin` with the status list and a feedback summary; keep `/admin/feedback`. Pete: "admin should expose the settings and permissions they can change" -> role definition GATHER.

### 2.15 Customer security workspace (NEW, 8 views)

Prototype `customerHome`, `customerFleet`, `customerAssessment`, `customerFindings`, `customerControls`, `customerRoadmap`, `customerReports`, `customerAssurance`, entered by the Partner/Customer switch or the `Customer` role. Customer-safe rules in the HTML: only consultant-**reviewed** findings are shown; "No" answers are not findings until reviewed; no pricing; reports only when `report && narrativeApproved`. The app has the data concepts (dispositions accepted, report issued, narrative approved, follow-up client pages in `(client)/`), but there is **no customer-facing authenticated area**: `(client)/follow-up` is a token link only. UNMEASURED: whether the API exposes a customer-scoped read of reviewed findings (it does not have a Customer app role: `Role = consultant | admin | partner | demo`, `lib/session.ts`). Consequences:
- Build the 8 views as a **read-only preview inside the existing roles** (as the HTML does for Partner/Consultant/Admin/Demo), reusing existing reads; do NOT add a Customer auth role (GATHER: Pete asked for role definitions first).
- `customerControls` (Framework alignment) carries a 16-row ISO/IEC 27001:2022 clause, NIST CSF and CIS table (`FMW`) that was authored by the prototype, not supplied by HP or the SME: -> GATHER; hold the page.
- `customerFleet` is mostly "Not connected" placeholders (device count, sites from the profile): cheap.

### 2.16 Things in the app that the prototype does not show, and must survive

Sign-in and UAT start pages; skip link ("Skip to main content", root `layout.tsx`); breadcrumbs; the single prototype banner and hosted demo notice; `FeedbackButton` pill and its attachments; Reset demo (confirm step) and Sign out; role badge; client follow-up pages `(client)/`; real URLs for every screen (the prototype is a single-page state machine with no URLs: deep links, print, back button all must keep working); API loading and error states; the finding override flow; AI narrative provenance; PDF report.

## 3. Pete's items

Class: **BUILD-NOW** = answered by the HTML / navigation / workflow; **GATHER** = needs HP or partner input, a roles definition, branding, a terminology decision or audience testing. Pete himself put visual polish and branding later, and recommended "prioritising workflow refinements before visual polish or broader content changes".

| # | Pete's item (from the AI summary) | Does v1.2 answer it? (cite) | Class |
|---|---|---|---|
| 1 | Role-based entry; production should log in and apply permissions; for demos a username/password flow with optional role selector | PARTLY. The HTML has a top-bar role select (`data-change="role"`) but no login. The APP already has the role chooser sign-in (`SignInScreen.tsx` MockSignIn), a four-level UAT start (`UatStartScreen.tsx`) and Entra when hosted. | GATHER (role-to-permission definition, item 5); nothing to build for the demo path |
| 2 | Partner readiness as "step zero" before customer engagement | YES. `MENU_SPEC.partner`: My readiness is the 2nd item under PARTNER WORKSPACE, before CUSTOMER DELIVERY; `partnerReadiness()` states "Readiness is separate from customer security posture" | BUILD-NOW |
| 3 | Persistent or semi-persistent side navigation to retain context | YES. `aside.sidebar` persistent, hideable (`syncSidebar`, `NAV_STORAGE`) | BUILD-NOW |
| 4 | Should users switch customers from inside a customer page? multiple routes confuse | The HTML KEEPS a top-bar customer select (`data-change="customer"`) plus "<- Customer register" and the register's Open buttons. Not resolved by the design. | BUILD-NOW as drawn (low cost, isolated) with a Kam decision to confirm; Pete's question itself is GATHER |
| 5 | Clearer definition of administrator; admin area should show the settings and permissions they can change | NO. `admin()` is feedback + "Not connected" list; no permissions. | GATHER (role definitions); build only the page layout |
| 6 | Role scope: consultant sees every customer and partner capabilities, plus audit and metrics; admin adds feedback and administration | YES for menus (`MENU_ALLOWED`): Consultant list is Partner list + metrics + attribution, Admin = all 13 | BUILD-NOW (menu matrix 2.1a), subject to API role checks |
| 7 | Scoring terminology and audience clarity | NO. Score shows "Overall score x/100" and "Rating Green/Amber/Red"; no new wording. | GATHER (terminology) |
| 8 | "Good / Better / Best" may read as commercial pricing levels; suggest high / medium / low impact | NO, WORSE: `partnerPackages()` presents them as purchasable packages with a "Commercial motion". `stepRecommendation()` keeps the grouping, and v1.2 adds "Two separate frameworks" copy. | GATHER; do not build packages page |
| 9 | Roadmap content looked like placeholder; could be editable with audit notes | PARTLY. `partnerRemediation()` adds editable owner / date / state / evidence on the roadmap step. | BUILD-NOW (front-end register, see ticket); persistence is a separate decision |
| 10 | Executive report clarity needs audience testing | NO | GATHER |
| 11 | Conversation coach output needs audience testing | NO (`coach()` is static talk tracks) | GATHER |
| 12 | Customers vs engagements: grouping of customers, engagements, assessments | The HTML keeps both pages ("Customer engagements", "Assessment pipeline"), no explanation | BUILD-NOW as drawn; naming is a GATHER |
| 13 | Metric scope: individual vs portfolio vs partner aggregate; attribution scope | NO | GATHER |
| 14 | Revenue calculator: more inputs? | NO (5 inputs, simpler than the app) | GATHER (partner input) |
| 15 | Prioritise tools, simplify or consolidate pathways, subtle workflow adjustments | YES: v1.2 drops the combined Assessments hub and adds My readiness + Assessment pipeline, drops Help/Settings | BUILD-NOW (nav consolidation) |
| 16 | Branding, design guides, self-branding | NO (HP logo hot-linked; no guide) | GATHER (later, per Pete) |
| 17 | Follow-ups: Steve to gather partner feedback; team to prioritise workflow, define roles, review nav, terminology, audience validation, branding, partner input | Process tasks | GATHER |

Claim checks against the HTML (the AI summary is mostly right): "prototype opens directly into a demo experience" TRUE; "three-phase structure" TRUE; "Good Better Best ... no prices or revenue" TRUE of v1.1 `stepRecommendation()`, FALSE of v1.2 `partnerPackages()` (commercial motion, scope export; "Price: Not approved" only); "customer snapshot ... compares current performance with target performance by section" PARTLY: the HTML's heading says "By section: current vs target" but renders only the current percentage (no target bar); "Phase 1/2/3 offer sheets" TRUE; "revenue calculator ... saves a scenario" NOT in the HTML (it has CSV export and reset only); "audit notes required for changes" TRUE of the app, in the HTML only the "Verified complete needs evidence" rule.

## 4. Proposed tickets (HPSMPOC; do not create yet)

Format: title / what / acceptance criteria (testable) / files / depends. Build order is top to bottom. "(app)" = `web/src/app/(app)`.

### BUILD-NOW

**T01 Left sidebar and top bar shell (FIRST; blocks everything).**
What: replace the header burger with a persistent left sidebar (`aside` landmark, 228 px, navy tokens) and a top bar (title/crumb, role badge, account controls). Below 860 px the sidebar is a drawer with backdrop. Pages are not edited.
AC: (1) at 1280x800 and 1024x768 the Main nav is visible without a click, `nav[aria-label="Main"]` inside `aside`; (2) toggle button has `aria-expanded` and `aria-controls`, state persists across reload (localStorage, try/catch), closed sidebar is `inert`; (3) at 390x844 the drawer opens over the page with a backdrop, Escape closes and returns focus to the toggle, a click on the backdrop closes it, picking a page closes it; (4) `aria-current="page"` on exactly one link; (5) skip link still the first Tab stop and targets `#main`; (6) role badge `data-testid="role-badge"`, Sign out, Reset demo (confirm step, hosted Admin only, never on UAT) still work; (7) `@media print` hides the sidebar with no empty margin; (8) no horizontal scroll at 390/768/1024/1280/1440 (`responsive.spec.ts`); (9) axe clean open and closed.
Files: `components/shell/AppShell.tsx`, new `components/shell/Sidebar.tsx`, `components/shell/GlobalNav.tsx` (layout only), `app/globals.css`, `styles/tokens.css`, `design/contrast.ts` + `contrast.test.ts` (new pairs), `app/layout.tsx` (footer inside the content column), `app/(app)/layout.tsx`.
Depends: none.

**T02 Navigation model: groups and the role matrix.**
What: grouped sections (PARTNER WORKSPACE / CUSTOMER DELIVERY / SERVICE GROWTH / TOOLS & SUPPORT), new labels, entries per role per 2.1a; keep `currentItem` most-specific match; hide entries with no built page (HPSMPOC-183 rule).
AC: per role, the ordered link list equals the matrix (unit test, replaces `GlobalNav.test.ts` lists); no link leads to a page saying "Not in this build yet" (`nav-dead-ends`); Consultant/Demo menu shows Service offers only if the route allows that role (check recorded in the PR); group headings are real headings or `aria-labelledby` groups.
Files: `components/shell/GlobalNav.tsx`, `shell/nav-dead-ends.test.ts`, `GlobalNav.test.ts`. (same lane as T01)
Depends: T01.

**T03 Top-bar customer picker.**
What: "Select a customer" control that opens that customer's workspace; Demo sees aliases (ORG-nnnnn, B208).
AC: lists the same customers as `/customers` for the role; choosing one navigates to `/customers/<id>`; the option text for Demo is the alias; keyboard operable; hidden on sign-in/client pages.
Files: `shell/AppShell.tsx`/`Sidebar.tsx` (T01 lane), reads `customer/useDirectory.ts`, `useCustomerShownAs.ts`.
Depends: T01. Flag: Pete's question (item 4); Kam may drop it.

**T04 Shell test and helper migration.**
What: replace the burger tests with sidebar tests; update shared e2e helpers.
AC: `playbook-burger-menu.spec.ts` replaced by a sidebar spec asserting persistent nav at desktop and drawer at 390; `shell.ts` `menuButton/openMainMenu` work at both; `playbook.ts` sign-out helper (l.170) works; unit tests listed in section 6 pass.
Files: `e2e/shell.ts`, `e2e/playbook.ts`, `e2e/playbook-burger-menu.spec.ts`, `e2e/nav-dead-ends.spec.ts`, `src/components/shell/AppShell.{burger,compact,badge,reset}.test.tsx`, `AppShellFeedback.test.tsx`, `hosted.test.tsx`, `PrototypeBanner.test.tsx`, `src/app/print-rules.test.ts`.
Depends: T01, T02.

**T05 Tokens and primitives restyle.**
What: apply the v1.2 look to shared components without changing props: PageHeader (caps eyebrow, lede), Card, pills/Tag, KPI tile and Panel, tables, progress bar; keep 44 px targets and AA contrast.
AC: no existing prop removed (type-check of every caller); `contrast.test.ts` passes; design-system page shows the new look; all unit tests unchanged-pass.
Files: `components/ui/*.tsx`, `components/partner/parts.tsx`, `components/customer/parts.tsx`, `components/shell/NextStep.tsx` (add Previous), `screens/DesignSystemScreen.tsx`, `app/design-system/page.tsx`.
Depends: T01 token commit only.

**T06 Partner Home.** Column layout (pipeline + phase motion left; next actions + readiness right), keep PhaseFlow. AC: KPI tiles unchanged data; "Recommended next actions" links resolve; no horizontal scroll; `kpi-*` test ids kept. Files: `partner/PartnerDashboard.tsx`, `home/PhaseFlow.tsx`, `home/phase-flow.ts`. Depends: T01, T05.

**T07 Customers register and Engagements.** Stage chips, progress column, sort kept. AC: filters and sort behave as now; progress bar has text alternative "N of M"; mobile cards kept. Files: `customer/CustomerManagement.tsx`, `EngagementsList.tsx`, `directory.ts` (read only unless progress needs a field: then flag as API ask). Depends: T01, T05.

**T08 Customer frame and overview.** Tab bar, header card with chips, sticky journey rail without the Overview entry, "Back to customers", breadcrumbs kept. AC: `aria-label` names "Customer sections" and "Assessment journey" kept (or all dependent specs updated in the same PR); rail collapses to `<details>` below the new breakpoint; alias rules (B208) unchanged. Files: `shell/CustomerShell.tsx`, `customer/tabs.ts`, `customer/EngagementOverview.tsx`, `customer/CustomerHeading.tsx`. Depends: T01, T05.

**T09 Journey: Profile and Assessment.** Restyle; add nothing. Files: `screens/ProfileScreen.tsx`, `AssessmentScreen.tsx`, `QuestionBlock.tsx`, `customer/ApiProfile.tsx`, `ApiSteps.tsx`, `snapshot/QuestionCard.tsx`, `QuestionMap.tsx`, `SnapshotRunner.tsx`, `ReviewPanel.tsx`, `useSnapshot.ts`, `playbook/[moduleId]/assessments/...`. Depends: T08.

**T10 Journey: Findings, Recommendation, Roadmap.** Restyle; sections-vs-target caption fixed to what the data shows. Files: `screens/ResultsScreen.tsx`, `FindingCard.tsx`, `RecommendationScreen.tsx`, `RoadmapScreen.tsx`, `results/ResultsView.tsx`, `customer/FindingDetail.tsx`, `FindingOverride.tsx`. Depends: T08.

**T11 Roadmap remediation register.** Owner, target date, state (Not started / In progress / Evidence submitted / Verified complete), evidence reference; "Verified complete" refused without an evidence reference; browser-held like the action plan unless an API field exists. AC: unit test for the refusal; value survives reload; marked as sample/local. Files: `screens/RoadmapScreen.tsx` (T10 lane, after T10), new `customer/remediation-store.ts`. Depends: T10. Open: persistence (API ask) = Kam.

**T12 Journey: Narrative, Report, Next engagement, Metrics.** Restyle. Files: `screens/NarrativeScreen.tsx`, `ReportScreen.tsx`, `NextEngagementScreen.tsx`, `MetricsScreen.tsx`, `customer/ApiNarrative.tsx`, `ServiceReport.tsx`. Depends: T08.

**T13 Customer tabs: Tasks, Documents, Coach.** Restyle. Files: `customer/FirmwareTask.tsx`, `DocumentGeneration.tsx`, `ConversationCoach.tsx`, `collateral/ClientPacks.tsx`, `PackView.tsx`, `(app)/coach`, `(app)/documents` pages. Depends: T08.

**T14 My readiness.** Relabel the Assessments hub as My readiness; four-area blocks, interpretation panel, "learning priorities" from unchecked statements. AC: priorities list = first 5 unchecked statements, derived only from the deck content; bands unchanged. Files: `readiness/AssessmentsHub.tsx`, `ReadinessRunner.tsx`, `ReadinessResult.tsx`, `parts.tsx`. Depends: T01, T05.

**T15 Training & playbooks page (new).** Route with the 3 steps and the six-row pathway linking to existing modules. The five "principles" bullets are NOT included (GATHER G5). AC: each row links to an existing `/playbook/<id>`; page added to the nav matrix by T02's file owner (note: T02 must ship the entry, hidden until this route exists). Files: new `(app)/training/page.tsx`, new `components/partner/TrainingScreen.tsx`. Depends: T01, T05.

**T16 Action plan restyle.** Files: `partner/ActionPlanScreen.tsx`, `action-plan.ts`, `browser-store.ts`. Depends: T01, T05.

**T17 Delivery phases (Service offers).** Files: `partner/ServicesHub.tsx`, `OfferSheet.tsx`, `ImplementationScreen.tsx`, `ManagedServiceScreen.tsx`, `service-parts.tsx`. Depends: T01, T05.

**T18 Revenue.** Files: `partner/RevenueCalculator.tsx`, `RevenueResults.tsx`, `OneCustomerEstimate.tsx`, `revenue-words.ts`. Depends: T01, T05.

**T19 Resources and modules.** Remove the module rail from `PlaybookShell`, grid on `/playbook`, prev/next + "All modules" on module pages, keep "N of 11 viewed". AC: no second left rail; `aria-current` for Resources while on a module page (`playbook-customer-screens.spec.ts` l.91); Playbook module deep links unchanged. Files: `playbook/PlaybookShell.tsx`, `PlaybookHome.tsx`, `ModuleScreen.tsx`, `BlockRenderer.tsx`, `SnapshotLauncher.tsx`, `(app)/playbook/layout.tsx`. Depends: T01, T05.

**T20 Metrics, Attribution preview, Administration.** `/admin` gets the connections-status list and a link/summary to feedback; keep `/admin/feedback`. Files: `screens/MetricsDashboardScreen.tsx`, `AttributionPreviewScreen.tsx`, `(app)/admin/page.tsx`, `feedback/AdminFeedback.tsx`. Depends: T01, T05.

**T21 Customer security workspace A: switch, dashboard, fleet, assessments (preview, existing roles, read-only).** AC: only reviewed findings are shown; an unreviewed "No" never appears as a finding; nothing priced; no write calls (test spies on the client); the Partner/Customer switch is not offered when the session is Entra-hosted Customer-less (no new role). Files: new `(app)/security/**`, new `components/security/*`, new `shell/customer-nav.ts`. Depends: T01, T02, T05.

**T22 Customer security workspace B: findings, remediation roadmap, reports and evidence, continuous assurance.** Same rules; report only when issued and narrative approved. Files: new `components/security/findings*.tsx`, `roadmap*.tsx`, `reports*.tsx`, `assurance*.tsx`, routes `(app)/security/...`. Depends: T21 (routes/nav stub) and T11 for owner/status display.

**T23 Cross-cutting QA gate (no feature code).** Run axe, keyboard walk, responsive, print and screenshot sets at 390/768/1024/1280/1440 after all lanes merge; fix only test files. Files: `e2e/a11y.spec.ts`, `keyboard.spec.ts`, `responsive.spec.ts`, `journey.ts`, `playbook-quality.spec.ts`, `playbook-b17-clicks.spec.ts`, `playbook-print.spec.ts`. Depends: all.

### GATHER (do not build; each one an ask)

- **G1 Role definitions** (partner / consultant / admin / demo / customer: permissions, dashboards, admin settings; whether a Customer app role exists). From: HP + Kam. Blocks: Customer role, Admin page content, in-session role switcher.
- **G2 Customer-switching in a customer page** (keep or drop the top-bar picker). From: Kam/Pete.
- **G3 Good / Better / Best vs impact labels; services packages page; "Revenue & proposals" and "Customer engagements" wording.** From: HP/Kam. Blocks: the p-packages page.
- **G4 Framework alignment content** (ISO/IEC 27001:2022, NIST CSF, CIS mapping table). From: Datasec SME / HP. Blocks: customer "Framework alignment" page.
- **G5 Training principles wording** and whether Training & playbooks is in this phase's scope. From: SME.
- **G6 Audience testing** of the executive report, narrative and coach output (Pete items 10, 11).
- **G7 Branding and self-branding, HP logo/brand assets, metric and attribution scope, revenue-calculator inputs.** Later per Pete.

## 5. Parallel lanes (BUILD-NOW tickets)

Single-owner files (no two lanes touch the same file):

| Lane | Tickets | Owns (file set) |
|---|---|---|
| **L0 Shell** | T01, T02, T03, T04 | `shell/AppShell.tsx`, `shell/Sidebar.tsx` (new), `shell/GlobalNav.tsx`, `shell/PrototypeBanner.tsx`, `shell/DemoNotice.tsx`, `shell/HpLogo.tsx`, `app/globals.css`, `styles/tokens.css`, `styles/brand.css` (untouched), `design/contrast*`, `app/layout.tsx`, `app/(app)/layout.tsx`, `feedback/FeedbackButton.tsx`, shared e2e helpers (`e2e/shell.ts`, `playbook.ts`, `axe.ts`), all shell unit tests, `print-rules.test.ts`, `nav-dead-ends.*`, `playbook-burger-menu.spec.ts` |
| **L1 Primitives** | T05 | `components/ui/*`, `partner/parts.tsx`, `customer/parts.tsx`, `shell/NextStep.tsx`, `screens/DesignSystemScreen.tsx`, `app/design-system/page.tsx` |
| L2 | T06 | `partner/PartnerDashboard.tsx`, `home/*` |
| L3 | T07 | `customer/CustomerManagement.tsx`, `EngagementsList.tsx`, `directory.ts`, `useDirectory.ts` |
| L4 | T08 | `shell/CustomerShell.tsx`, `customer/tabs.ts`, `EngagementOverview.tsx`, `CustomerHeading.tsx`, `shell/CustomerContext.tsx` |
| L5 | T09 | `screens/ProfileScreen`, `AssessmentScreen`, `QuestionBlock`, `customer/Api{Profile,Steps}`, `snapshot/*`, `(app)/playbook/[moduleId]/assessments/**` |
| L6 | T10 then T11 | `screens/ResultsScreen`, `FindingCard`, `RecommendationScreen`, `RoadmapScreen`, `results/*`, `customer/FindingDetail`, `FindingOverride`, new `remediation-store.ts` |
| L7 | T12 | `screens/{Narrative,Report,NextEngagement,Metrics}Screen`, `customer/ApiNarrative`, `ServiceReport` |
| L8 | T13 | `customer/{FirmwareTask,DocumentGeneration,ConversationCoach}`, `collateral/*`, `(app)/{coach,documents}` |
| L9 | T14 | `readiness/*` |
| L10 | T15 | new `training` route and `TrainingScreen` |
| L11 | T16 | `partner/{ActionPlanScreen,action-plan,browser-store}` |
| L12 | T17 | `partner/{ServicesHub,OfferSheet,ImplementationScreen,ManagedServiceScreen,service-parts}`, `(app)/services/**` |
| L13 | T18 | `partner/{RevenueCalculator,RevenueResults,OneCustomerEstimate,revenue-words}` |
| L14 | T19 | `playbook/*` (all), `(app)/playbook/layout.tsx` |
| L15 | T20 | `screens/{MetricsDashboard,AttributionPreview}Screen`, `(app)/admin/**`, `feedback/AdminFeedback` |
| L16 | T21 | new `components/security/*` (set A), new routes (set A), `shell/customer-nav.ts` (stub created by L0 in T02, then owned here) |
| L17 | T22 | new `components/security/*` (set B), routes (set B) |
| **LQ** | T23 | cross-page e2e specs only; runs last |

Shared files and their single owner: `globals.css`, `tokens.css`, `app/layout.tsx`, `(app)/layout.tsx`, `GlobalNav.tsx` -> **L0**. `ui/*`, `partner/parts.tsx`, `customer/parts.tsx`, `NextStep.tsx` -> **L1**. `partner/content.ts` (SHOWCASE), `customer/engagement.ts`, `lib/*`, `api/*` -> **frozen** (no lane edits; an ask goes to L0 for tokens or to Tuesday for API). `SnapshotLauncher.tsx` is imported by the Home dashboard (`MockTag`): owned by L14, export signatures frozen. Rule for everyone: use existing Tailwind utilities and tokens; a new CSS class needs L0.

Must wait for L0 (T01 merged, not just started): every lane except L1's token-free prop work. L1 waits only for L0's first commit that adds the sidebar/topbar tokens. L16 and L17 also wait for T02 (nav stub). L6's T11 waits for T10; L17 waits for T11 and L16's route stub. LQ waits for all.

**How many truly in parallel:** wave 0 = 2 (L0, L1 token-only start). Wave 1 (after L0 merges) = 14 file-disjoint lanes (L2 to L15) could run at once; wave 2 = L16, L17 (needs the nav stub); then LQ. Recommend capping at 8 to 10 concurrent builders to keep review gates and CI sane (CI load flakes are already on file in BACKLOG B221/B202 items).

## 6. Risks and tests

**Tests that WILL break (named).**
- e2e: `playbook-burger-menu.spec.ts` (asserts "no rail", `aside nav` count 0, burger geometry; wholly obsolete), `nav-dead-ends.spec.ts`, `shell.ts` (`menuButton`: waits for `nav[Account]`, expects a Menu button), `playbook.ts` (l.170-171 sign-out path through "Menu"; l.177 Customer sections), `attribution-preview.spec.ts`, `metrics-dashboard.spec.ts`, `playbook-b17-clicks.spec.ts` (4x `openMainMenu`), `playbook-customer-screens.spec.ts` (l.89-91, l.228), `playbook-quality.spec.ts`, `customer-frame-alias.spec.ts`, `customer-headings-alias.spec.ts` (Customer sections / Assessment journey navs), `playbook-narrative-attention-live-api.spec.ts` (journey rail), `playbook-print.spec.ts` (banner count 0 when printed; sidebar must not print), `playbook-feedback-pill.spec.ts` (no Feedback in the banner), `hosted-reset.spec.ts` and `hosted-entra.spec.ts` (role badge, Sign out, Reset demo placement), `keyboard.spec.ts` (Tab walk: the sidebar adds 8 to 13 stops before `main`; `tabTo` max 120 presses and the "skip link first stop" assertion), `responsive.spec.ts` and `a11y.spec.ts` (new widths).
- unit: `AppShell.burger.test.tsx` (obsolete), `AppShell.compact.test.tsx`, `AppShell.badge.test.tsx`, `AppShell.reset.test.tsx`, `AppShellFeedback.test.tsx`, `hosted.test.tsx`, `GlobalNav.test.ts`, `nav-dead-ends.test.ts`, `PrototypeBanner.test.tsx`, `productName.test.tsx`, `CustomerShell.{b24,b45,b59,alias}.test.tsx`, `tabs.test.ts`, `print-rules.test.ts` (rule parser), `design/contrast.test.ts` (new token pairs must be added or the new colours go unmeasured).

**Accessibility.** Sidebar: `aside` with a `nav` named "Main" (keep the accessible name the specs use), `aria-current="page"` on one link, `aria-expanded` / `aria-controls` on the toggle, Escape and focus return, drawer on narrow screens needs a focus trap or `inert` on the page behind (the prototype only sets `inert` on the closed sidebar), visible 3px focus ring on the navy background (the app's ring uses `--ds-focus` = brand primary `#1d4f91`, which is nearly invisible on `#0a2940`: needs a light ring token measured >= 3:1, UNMEASURED), 44 px targets, group labels not just colour, `prefers-reduced-motion` honoured for the 0.22 s slide. Contrast per section 2.1.

**Responsive.** Viewport breakpoints in screens assume full width. Known two- and three-column spots: `PhaseFlow` (`lg:grid-cols-3`), `PartnerDashboard` (`xl:grid-cols-4`, `lg:grid-cols-2 xl:grid-cols-3`), `CustomerShell` rail (`lg:flex-row`, `lg:w-64`), `PlaybookShell`, `CustomerManagement` filters (`xl:grid-cols-[2fr_1fr_1fr_1fr_auto]`). Each lane re-tunes its own; LQ proves it at 1024/1180/1280/1440.

**Behavioural.** No in-session role switching on Entra-hosted. No local-storage workspace/JSON import/export. Real URLs preserved. Consultant/Demo menu widening vs API role rules (verify before shipping T02). Demo alias (ORG-nnnnn) must hold in the new picker and top-bar title (B208/B215 specs).

**Deploy / UAT.** None of this work deploys anything; the hosted UAT/demo copies stay on the current build until Kam sends a deploy brief. Once merged to main, CI deploy workflows may fire on push: confirm the repo's deploy trigger (UNMEASURED; not read) before the first merge. The UAT review copy (B409/B434) has its own header badge text ("Consultant (review copy)"); the new top bar must keep the compact form below `md`.

**Content/IP.** The HTML hot-links an HP logo from Wikimedia: never ship. ISO/NIST/CIS table and the "Independent assessment principles" are un-sourced policy-like wording (project rule: do not invent security policy). Nothing goes to HP without Kam's send.

## 7. Duplicates and prior work

- **B169** (Kam, terminal 2026-10-06 19:36, "should be nested into a burger menu and function as a top-level menu"): `AppShell.tsx` comments, `GlobalNav.tsx` header, `AppShell.burger.test.tsx`, `playbook-burger-menu.spec.ts`. **The new commission supersedes it.** Per the settled-decisions rule, record the supersession as a new clarification entry (CLARIFICATIONS.md ends at C-30, 2026-09-29; B169 is not in it: UNMEASURED whether a card or entry exists elsewhere).
- **B14 F-19/F-20**: role-filtered menu, Partner Action plan and Service offers, most-specific highlight (`GlobalNav.tsx`). Extend, do not redo.
- **HPSMPOC-183** (B97 found): Help and Settings removed from the menu while empty; `nav-dead-ends` pins it. Keep (the v1.2 menu also has no Help/Settings).
- **B170** (Kam 2026-10-06 19:42): `PhaseFlow` from Kam's image. Keep over the prototype's thinner phase boxes.
- **B56 / HPSMPOC-95** (Kam 2026-09-29): tiers are groupings, no prices (`RecommendationScreen.tsx` `TIERS_EXPLAINED`). Conflicts with the packages page.
- **C-27 b**: one prototype banner per page (`PrototypeBanner.tsx`). Keep.
- **C-14 / C-13**: partner readiness = deck slide 99, 16 checkbox statements, four areas, bands 12/8/4/0. My readiness follows it.
- **C-30 (Kam's notes 2026-09-29)**: client follow-up (built: `followup/*`, `(client)/`), collateral packs (built: `collateral/*`), "more sophisticated engagements = next phase, backlog only" (applies to Pete's engagement-grouping and metric-scope questions).
- **B202** (card hpsmpoc-tuesday-dashboard-vs-next-phase-1011): attribution preview page, labelled preview. Keep the app's.
- **B208 / B215**: Demo alias on frames and headings. Must survive any header or picker.
- **B104 (C-42)** feedback pill, **HPSMPOC-93 / -142** print rules, **B24 N-08** finding names in crumbs, **B409 / B434** UAT start page and review-copy badge, **QA-027 / HPSMPOC-21** branding undecided.
- **QA-027** also answers Pete's branding item: the swap point is `styles/brand.css`.
- Jira backlog itself NOT searched (out of scope; `BACKLOG.md` is a pointer plus W1 decisions and follow-ups B06 to B221; none mention navigation, sidebar, roles or layout work beyond the items above).

SELF-CHECK: read WHOLE: the v1.2 HTML (all 313 lines), Pete's summary (all), `(app)/layout.tsx`, `app/layout.tsx`, `globals.css`, both customer/playbook layouts, `design-system/page.tsx`, `AppShell.tsx`, `GlobalNav.tsx`, `CustomerShell.tsx`, `PlaybookShell.tsx`, `PartnerDashboard.tsx`, `PageHeader.tsx`, `PhaseFlow.tsx`, `HomeScreen.tsx`, `NextStep.tsx`, `PrototypeBanner.tsx`, `HpLogo.tsx`, `tabs.ts`, `journey.ts`, `brand.css`, `shell.ts`, `nav-dead-ends.spec.ts`, `playbook-burger-menu.spec.ts`, `responsive.spec.ts`, `keyboard.spec.ts`, project `CLAUDE.md`, `BACKLOG.md`. Read PARTLY: every `page.tsx` (first 14 lines each, enough to map route to component), `CustomerManagement.tsx` (lines 150-288), `EngagementsList.tsx` (15-74), `RecommendationScreen.tsx` (1-60), `SignInScreen.tsx` (1-60), `tokens.css` (1-80), `Button.tsx`, `AppShell.burger.test.tsx` (1-60), `print-rules.test.ts` (1-45), `CLARIFICATIONS.md` (grep plus lines 160-192). NOT read: `web/src/components/**` other than the above (Tasks, Documents, Coach, readiness, services, revenue, snapshot, screens' bodies were mapped by file name and `PageHeader` calls only, so "restyle only" verdicts for them are by name and header, UNMEASURED in detail), `globals`' tests beyond print, `design/contrast.ts`, the other e2e specs (named from grep hits only), `api/`, Jira, the rest of CLARIFICATIONS.md, the Click-through video (not filed). Not rendered: all measurements are from CSS or code text; contrast ratios are computed.
