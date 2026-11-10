# UAT scenarios judged against the current site

Site: code main `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb`, built and run locally in mock mode on 127.0.0.1:9861 and walked as Partner, Consultant, Admin and Demo; content judged from the source files at that commit. Nothing was run against the hosted UAT site.

**Limits of this judgement.** (1) The local build runs with sample data: the customer journey there uses placeholder questions, so the live 16 questions, findings and report wording were read from the content files and the server code, not seen on screen. (2) Verdicts marked "from source" or "not re-run in this pass" were read from code or from the repository's own test description, not exercised. (3) The v2.1 pack tests the HTML file, so "not met" here usually means "the page does not exist on the site", not "the site is broken".

Verdicts: **met** · **partly** · **not met** · **needs content** · **out of scope (change request)**. G-numbers refer to GAP-LIST.md, D-numbers to DECISION-DOCUMENT.md.

## Counts

| Set | Total | met | partly | not met | needs content | out of scope (change request) |
|---|---|---|---|---|---|---|
| Alignment document, release suite (UAT-01 to UAT-20) | 20 | 4 | 10 | 2 | 3 | 1 |
| v2.1 tracker, functional (UAT-001 to UAT-285) | 285 | 109 | 26 | 60 | 6 | 84 |
| v2.1 tracker, non-functional (NF-001 to NF-038) | 38 | 8 | 20 | 4 | 1 | 5 |
| v2.1 tracker, production gates (PRD-001 to PRD-032) | 32 | 1 | 10 | 14 | 1 | 6 |
| v2.1 plan, end-to-end journeys (E2E-01 to E2E-12) | 12 | 1 | 3 | 3 | 0 | 5 |

The two packs both use the prefix "UAT-". In this file the document's twenty are written with two digits (UAT-01) and the tracker's with three (UAT-001).

## 1. Alignment document: minimum release suite (section 8)

| ID | Test / expected result | Verdict against main | Evidence |
|---|---|---|---|
| UAT-01 | Opening an existing v2.1 customer never maps previous answers to new QIDs. | **partly** | The mechanism is in place: every assessment is stamped with the exact content package and ruleset it was answered under, and answers are stored per assessment and question id (api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs:61-78, 107-113). The readiness swap of 9 Nov used new ids (web/src/content/packages/playbook-placeholder.v0.7.0.json:22). Not yet testable for the snapshot: no revised question set exists, and it holds only if the new set gets new ids. G-001, G-002. |
| UAT-02 | Mixed fleet question supports partial coverage and unsupported-device note. | **not met** | Live answers are Yes / No / Unsure only (web/src/content/rulesets/snapshot-policy-aligned.v0.1.2.json:905-920); a free-text note exists (web/src/components/snapshot/QuestionCard.tsx:26). No coverage or device-capability field. G-014. |
| UAT-03 | Unknown answer creates verification guidance, not an asserted breach. | **partly** | Unsure fires the same rule as No (ruleset "when ... in [no, unsure]"), scores 0 and carries the action to apply settings (ruleset:1669). The finding title is worded "not confirmed", which is not an asserted breach, but there is no separate verification task. G-011. |
| UAT-04 | Compensating answer requires a documented alternative safeguard. | **not met** | No compensating state or rationale field in the live set. G-014. |
| UAT-05 | Evidence source can change from customer claim to tool/device evidence. | **partly** | The record stores the source per answer and the API accepts five values (Entities.cs:113; Endpoints/Requests.cs:164). The live question screen always writes "asserted" (web/src/components/snapshot/useSnapshot.ts:70) unless the answer came from an import. The scripted sample customer has the control (web/src/components/screens/QuestionBlock.tsx:15-21). G-012. |
| UAT-06 | Evidence verified remains independent of positive/negative answer. | **partly** | Independent in the data model (source is a separate field from the answer); not settable on the live screen. G-012. |
| UAT-07 | Q06 sign-in and Q07 role authorisation do not duplicate each other. | **met** | Two distinct questions: sign-in at the printer and role-based access (ruleset questions Q-CS-05 and Q-CS-07, lines 1083 and 1178), shown next to each other as questions 11 and 12. The numbers differ from the revised sequence. G-003. |
| UAT-08 | Firmware actions offer tested maintenance and supported tool options. | **needs content** | Question wording is "regular or automated updates" (ruleset:943); the action is the generic "Apply the HP Security Manager settings listed for this finding" (ruleset:1669); recommended setting "Remote Firmware Upgrade (RFU)" (ruleset:2368). Needs HP SME wording. G-006, G-007. |
| UAT-09 | Unsupported trusted-boot capability directs to lifecycle or exception review. | **needs content** | Recommendation is "Secure Boot Presence = Enable" (ruleset:2224) with a 30-day bucket; no unsupported path. Needs HP SME wording and the new answer states. G-008, G-014. |
| UAT-10 | Q13 certificate control captures ownership, renewal/expiry process. | **needs content** | One yes/no/unsure question on central management (ruleset:1555); no ownership or expiry capture. G-015. |
| UAT-11 | Changed answer invalidates related finding review, narrative and report release. | **partly** | Answers lock at scoring ("Submitting locks the answers against the versioned ruleset"). A changed finding marks the narrative stale and the report falls back to standard wording (web/src/components/customer/ApiNarrative.tsx:108-110, 198-200). No reopen path; a new assessment must be started. G-021. |
| UAT-12 | Edited narrative persists and generates a dated revision event. | **partly** | An edit is saved with a mandatory audit note, the reviewer and the time; the model text is kept beside it (Entities.cs:220-246; ApiNarrative.tsx:171). Only one edit, made at approval; no later revision. G-020. |
| UAT-13 | Approved narrative reflects saved edited content; regenerate requires reapproval. | **partly** | The report uses the approved or edited text only. A new draft is a new record that needs approval. A new draft is offered only when findings changed, the draft failed or was rejected (ApiNarrative.tsx:198-205). G-020. |
| UAT-14 | Customer report contents and return links navigate correctly. | **partly** | The PDF has an outline of bookmarks (api/src/HpsmPoc.Modules.Reporting/Pdf/PdfPigReportRenderer.cs:69) and nine numbered sections (Report/ReportModel.cs:16); no contents page in the body and no return links. G-022. |
| UAT-15 | Customer report contains no reseller pricing, GP or opportunity notes. | **met** | No price, margin or deal data exists anywhere in the site; the report section "Next engagement" shows no price (web/src/components/screens/NextEngagementScreen.tsx:53). Whether that section belongs in the report is decision D-019. G-023. |
| UAT-16 | Product-led reseller does not require consulting fees in its workflow. | **partly** | No step forces a fee, but the home page and the guided demo present consulting fees as the motion (web/src/content/walkthrough/steps.ts:144; partner-showcase content) and there is no operating-mode setting. G-026, G-027. |
| UAT-17 | Opportunity values remain separated by identified/qualified/quoted/booked/recognised stage. | **out of scope (change request)** | No opportunity record exists in the site. P2 in the document. G-029. |
| UAT-18 | Viewer role cannot edit assessment, evidence, commercial settings or narratives. | **met** | The Demo role is read-only and limited to seeded sample customers, enforced on the server (api/src/HpsmPoc.Modules.Assessment/Identity/Caller.cs:19, 42, 208-217). Judged from source and from the local mock walk as Demo; not exercised against a live API in this pass. |
| UAT-19 | Existing v2.1 sidebar, customer list, quotes and delivery pages still navigate. | **partly** | The site's own menu, customer list and delivery phases navigate (local walk as four roles, 0 failed page loads). Quote pages do not exist (change request). G-030, G-048. |
| UAT-20 | Offline local prototype clearly states no live HP device management or report delivery. | **met** | Equivalent statements on the site: Admin lists "HP Security Manager integration — Not connected" and "Customer email delivery — Not connected" (web/src/app/(app)/admin/page.tsx:35); the recommendation page says "No device is changed" (web/src/components/screens/RecommendationScreen.tsx:66). |

## 2. v2.1 UAT tracker: functional cases

The tracker's own state for every case is "Not run". Its reference application is the HTML file.

| ID | Module | Scenario | Role | Priority | Verdict against main | Evidence |
|---|---|---|---|---|---|---|
| UAT-001 | Navigation / Partner workspace | Open Dashboard from sidebar | Partner | P2 | **partly** | The page exists as "Home" (/home); the heading and content differ (G-053 to G-063). |
| UAT-002 | Navigation / Partner workspace | Navigate to Dashboard using browser history | Partner | P2 | **partly** | The page exists as "Home" (/home); the heading and content differ (G-053 to G-063). |
| UAT-003 | Navigation / Partner workspace | Open My readiness from sidebar | Partner | P2 | **met** | /assessments "Playbook Partner Readiness". |
| UAT-004 | Navigation / Partner workspace | Navigate to My readiness using browser history | Partner | P2 | **met** | /assessments "Playbook Partner Readiness". Browser Back and Forward work on real page addresses. |
| UAT-005 | Navigation / Partner workspace | Open Training & playbooks from sidebar | Partner | P2 | **met** | /training. |
| UAT-006 | Navigation / Partner workspace | Navigate to Training & playbooks using browser history | Partner | P2 | **met** | /training. Browser Back and Forward work on real page addresses. |
| UAT-007 | Navigation / My work | Open Guided onboarding from sidebar | Partner | P2 | **not met** | No such page (G-072). Next phase. |
| UAT-008 | Navigation / My work | Navigate to Guided onboarding using browser history | Partner | P2 | **not met** | No such page (G-072). Next phase. |
| UAT-009 | Navigation / My work | Open My action queue from sidebar | Partner | P2 | **not met** | No such page (G-073). Next phase. |
| UAT-010 | Navigation / My work | Navigate to My action queue using browser history | Partner | P2 | **not met** | No such page (G-073). Next phase. |
| UAT-011 | Navigation / My work | Open Engagement journey from sidebar | Partner | P2 | **not met** | No such page (G-075). Next phase. |
| UAT-012 | Navigation / My work | Navigate to Engagement journey using browser history | Partner | P2 | **not met** | No such page (G-075). Next phase. |
| UAT-013 | Navigation / My work | Open Activity history from sidebar | Partner | P2 | **not met** | No such page (G-076). Next phase. |
| UAT-014 | Navigation / My work | Navigate to Activity history using browser history | Partner | P2 | **not met** | No such page (G-076). Next phase. |
| UAT-015 | Navigation / Customers & opportunities | Open Customer engagements from sidebar | Partner | P2 | **met** | /customers (menu label "Customers"). |
| UAT-016 | Navigation / Customers & opportunities | Navigate to Customer engagements using browser history | Partner | P2 | **met** | /customers (menu label "Customers"). Browser Back and Forward work on real page addresses. |
| UAT-017 | Navigation / Customers & opportunities | Open Opportunity pipeline from sidebar | Partner | P2 | **out of scope (change request)** | No opportunity pages (G-029). P2. |
| UAT-018 | Navigation / Customers & opportunities | Navigate to Opportunity pipeline using browser history | Partner | P2 | **out of scope (change request)** | No opportunity pages (G-029). P2. |
| UAT-019 | Navigation / Customers & opportunities | Open Assessment pipeline from sidebar | Partner | P2 | **met** | /engagements (menu label "Engagements"). |
| UAT-020 | Navigation / Customers & opportunities | Navigate to Assessment pipeline using browser history | Partner | P2 | **met** | /engagements (menu label "Engagements"). Browser Back and Forward work on real page addresses. |
| UAT-021 | Navigation / Customers & opportunities | Open Action plan from sidebar | Partner | P2 | **met** | /action-plan (Partner and Admin). |
| UAT-022 | Navigation / Customers & opportunities | Navigate to Action plan using browser history | Partner | P2 | **met** | /action-plan (Partner and Admin). Browser Back and Forward work on real page addresses. |
| UAT-023 | Navigation / Security services delivery | Open Delivery & assessments from sidebar | Partner | P2 | **not met** | No such page (G-083). Next phase. |
| UAT-024 | Navigation / Security services delivery | Navigate to Delivery & assessments using browser history | Partner | P2 | **not met** | No such page (G-083). Next phase. |
| UAT-025 | Navigation / Security services delivery | Open Delivery phases from sidebar | Partner | P2 | **met** | /services "Delivery phases". |
| UAT-026 | Navigation / Security services delivery | Navigate to Delivery phases using browser history | Partner | P2 | **met** | /services "Delivery phases". Browser Back and Forward work on real page addresses. |
| UAT-027 | Navigation / Service growth | Open Good / Better / Best from sidebar | Partner | P2 | **not met** | No such page (G-034). Next phase. |
| UAT-028 | Navigation / Service growth | Navigate to Good / Better / Best using browser history | Partner | P2 | **not met** | No such page (G-034). Next phase. |
| UAT-029 | Navigation / Service growth | Open Proposal & quote builder from sidebar | Partner | P2 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-030 | Navigation / Service growth | Navigate to Proposal & quote builder using browser history | Partner | P2 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-031 | Navigation / Service growth | Open Contracts & renewals from sidebar | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-032 | Navigation / Service growth | Navigate to Contracts & renewals using browser history | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-033 | Navigation / Service growth | Open Revenue modelling from sidebar | Partner | P2 | **met** | /revenue (menu label "Revenue"). |
| UAT-034 | Navigation / Service growth | Navigate to Revenue modelling using browser history | Partner | P2 | **met** | /revenue (menu label "Revenue"). Browser Back and Forward work on real page addresses. |
| UAT-035 | Navigation / Revenue & attribution | Open Sales dashboard from sidebar | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-036 | Navigation / Revenue & attribution | Navigate to Sales dashboard using browser history | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-037 | Navigation / Revenue & attribution | Open Revenue attribution from sidebar | Partner | P2 | **out of scope (change request)** | Only the sample "Attribution (Preview)" exists (G-033). P2. |
| UAT-038 | Navigation / Revenue & attribution | Navigate to Revenue attribution using browser history | Partner | P2 | **out of scope (change request)** | Only the sample "Attribution (Preview)" exists (G-033). P2. |
| UAT-039 | Navigation / Tools & support | Open Resources & modules from sidebar | Partner | P2 | **met** | /playbook (menu label "Resources"). |
| UAT-040 | Navigation / Tools & support | Navigate to Resources & modules using browser history | Partner | P2 | **met** | /playbook (menu label "Resources"). Browser Back and Forward work on real page addresses. |
| UAT-041 | Navigation / Tools & support | Open Automation metrics from sidebar | Partner | P2 | **met** | /metrics (Consultant, Admin, Demo). |
| UAT-042 | Navigation / Tools & support | Navigate to Automation metrics using browser history | Partner | P2 | **met** | /metrics (Consultant, Admin, Demo). Browser Back and Forward work on real page addresses. |
| UAT-043 | Navigation / Tools & support | Open Administration from sidebar | Admin | P2 | **met** | /admin (Admin only). |
| UAT-044 | Navigation / Tools & support | Navigate to Administration using browser history | Admin | P2 | **met** | /admin (Admin only). Browser Back and Forward work on real page addresses. |
| UAT-045 | Navigation / Operational governance | Open Readiness & controls from sidebar | Partner | P2 | **not met** | No such page (G-091). Next phase. |
| UAT-046 | Navigation / Operational governance | Navigate to Readiness & controls using browser history | Partner | P2 | **not met** | No such page (G-091). Next phase. |
| UAT-047 | Navigation / Security workspace | Open Security dashboard from sidebar | Customer | P2 | **met** | /security/<customer>/dashboard. |
| UAT-048 | Navigation / Security workspace | Navigate to Security dashboard using browser history | Customer | P2 | **met** | /security/<customer>/dashboard. Browser Back and Forward work on real page addresses. |
| UAT-049 | Navigation / Security workspace | Open Fleet & devices from sidebar | Customer | P2 | **met** | /security/<customer>/fleet. |
| UAT-050 | Navigation / Security workspace | Navigate to Fleet & devices using browser history | Customer | P2 | **met** | /security/<customer>/fleet. Browser Back and Forward work on real page addresses. |
| UAT-051 | Navigation / Security workspace | Open Security assessments from sidebar | Customer | P2 | **met** | /security/<customer>/assessments. |
| UAT-052 | Navigation / Security workspace | Navigate to Security assessments using browser history | Customer | P2 | **met** | /security/<customer>/assessments. Browser Back and Forward work on real page addresses. |
| UAT-053 | Navigation / Security workspace | Open Gaps & findings from sidebar | Customer | P2 | **met** | /security/<customer>/findings. |
| UAT-054 | Navigation / Security workspace | Navigate to Gaps & findings using browser history | Customer | P2 | **met** | /security/<customer>/findings. Browser Back and Forward work on real page addresses. |
| UAT-055 | Navigation / Governance & remediation | Open Framework alignment from sidebar | Customer | P2 | **needs content** | Framework alignment is held until an approved mapping exists (web/src/components/shell/customer-nav.ts:7-8; G-116). |
| UAT-056 | Navigation / Governance & remediation | Navigate to Framework alignment using browser history | Customer | P2 | **needs content** | Framework alignment is held until an approved mapping exists (web/src/components/shell/customer-nav.ts:7-8; G-116). |
| UAT-057 | Navigation / Governance & remediation | Open Remediation roadmap from sidebar | Customer | P2 | **met** | /security/<customer>/roadmap. |
| UAT-058 | Navigation / Governance & remediation | Navigate to Remediation roadmap using browser history | Customer | P2 | **met** | /security/<customer>/roadmap. Browser Back and Forward work on real page addresses. |
| UAT-059 | Navigation / Governance & remediation | Open Reports & evidence from sidebar | Customer | P2 | **met** | /security/<customer>/reports. |
| UAT-060 | Navigation / Governance & remediation | Navigate to Reports & evidence using browser history | Customer | P2 | **met** | /security/<customer>/reports. Browser Back and Forward work on real page addresses. |
| UAT-061 | Navigation / Governance & remediation | Open Continuous assurance from sidebar | Customer | P2 | **met** | /security/<customer>/assurance. |
| UAT-062 | Navigation / Governance & remediation | Navigate to Continuous assurance using browser history | Customer | P2 | **met** | /security/<customer>/assurance. Browser Back and Forward work on real page addresses. |
| UAT-063 | Navigation / Shared actions | Open My remediation actions from sidebar | Customer | P2 | **not met** | No such page (G-120). Next phase. |
| UAT-064 | Navigation / Shared actions | Navigate to My remediation actions using browser history | Customer | P2 | **not met** | No such page (G-120). Next phase. |
| UAT-065 | Partner dashboard | Four commercial KPI blocks | Partner | P1 | **out of scope (change request)** | Commercial tiles need the opportunity register (G-055). |
| UAT-066 | Partner dashboard | Recommended action context | Partner | P1 | **out of scope (change request)** | Needs opportunities (G-057, G-058). |
| UAT-067 | Partner dashboard | Recommended action navigation | Partner | P1 | **out of scope (change request)** | Needs opportunities (G-057, G-058). |
| UAT-068 | Partner dashboard | Attention table links | Partner | P1 | **out of scope (change request)** | Needs opportunities (G-057, G-058). |
| UAT-069 | Partner dashboard | Action queue preview | Partner | P1 | **not met** | No action queue (G-059). |
| UAT-070 | Partner dashboard | Practice readiness summary | Partner | P1 | **met** | Home shows the readiness state and links to it ("Not assessed yet" until a run exists). |
| UAT-071 | Partner dashboard | New opportunity shortcut | Partner | P1 | **out of scope (change request)** | No opportunity record (G-054). |
| UAT-072 | Partner dashboard | No overstretched whitespace | Partner | P1 | **partly** | Different layout; the specific cards do not exist (G-063). |
| UAT-073 | Partner dashboard | Dashboard figure disclosure | Partner | P1 | **partly** | Home marks its revenue figures "Sample model" and "Sample data"; there are no commercial KPIs to label (G-056). |
| UAT-074 | Partner dashboard | Dashboard after change | Partner | P1 | **out of scope (change request)** | Needs opportunities. |
| UAT-075 | Sidebar and header | Main sidebar hide and reopen | Partner | P1 | **met** | The menu rail collapses to icons and reopens (web/src/components/shell/Sidebar.tsx:72). |
| UAT-076 | Sidebar and header | Independent menu accordions | Partner | P1 | **not met** | Menu groups do not collapse (open ticket HPSMPOC-464; G-038). |
| UAT-077 | Sidebar and header | Accordion state after navigation | Partner | P1 | **not met** | No group state to remember (G-038). |
| UAT-078 | Sidebar and header | White/blue comparison | Partner | P1 | **out of scope (change request)** | Prototype-only comparison tool; recommended not to build (D-041). Marked out of scope rather than a change request. |
| UAT-079 | Sidebar and header | Breadcrumb navigation | Partner | P1 | **partly** | Breadcrumbs on four pages only (G-045). |
| UAT-080 | Sidebar and header | Hash route recovery | Partner | P1 | **met** | Equivalent: every page has a real address that can be reopened; unknown addresses answer a not-found page. |
| UAT-081 | Sidebar and header | Mobile off-canvas menu | Partner | P1 | **met** | The site has an off-canvas menu and is tested at tablet and phone widths by its own end-to-end suite (web/README.md). Not re-run in this pass. |
| UAT-082 | Sidebar and header | Skip to content | Partner | P1 | **met** | "Skip to main content" link (web/src/app/layout.tsx:19). |
| UAT-083 | Partner onboarding | Five-step path coverage | Partner | P2 | **not met** | No guided onboarding page (G-072). |
| UAT-084 | Partner onboarding | Onboarding quick links | Partner | P2 | **not met** | No guided onboarding page (G-072). |
| UAT-085 | Partner onboarding | No false certification | Partner | P2 | **not met** | No guided onboarding page (G-072). |
| UAT-086 | Partner readiness | Readiness score from sixteen items | Partner | P2 | **met** | Score = number of statements ticked, out of 16 (content 0.7.0). |
| UAT-087 | Partner readiness | Toggle a readiness statement | Partner | P2 | **partly** | Statements are ticked inside a run, not on one live page with group subtotals (G-065). |
| UAT-088 | Partner readiness | Score bands | Partner | P2 | **met** | Four bands from the content package scoring (unchanged from the deck version). |
| UAT-089 | Partner readiness | Draft/competence distinction | Partner | P2 | **met** | "Your result is self-assessed: it is not a verified HP competency or accreditation." |
| UAT-090 | Partner readiness | Readiness local persistence | Partner | P2 | **met** | Saved on the server as you go; survives reload. |
| UAT-091 | Training and playbooks | Training module availability | Partner | P2 | **partly** | The page lists three stages and six Playbook modules; no curriculum descriptions (G-069, G-070). |
| UAT-092 | Training and playbooks | Sales readiness learning path | Partner | P2 | **partly** | No sales-oriented learning row as such (G-070). |
| UAT-093 | Training and playbooks | Technical readiness learning path | Partner | P2 | **partly** | No technical learning row as such (G-070). |
| UAT-094 | Training and playbooks | Resource navigation context | Partner | P2 | **met** | Module pages return to the list. |
| UAT-095 | Customer register | Customer list and identifiers | Partner | P2 | **partly** | Each customer appears once; no short identifier is shown (G-078). |
| UAT-096 | Customer register | Customer search | Partner | P2 | **met** | Search on the Customers page. |
| UAT-097 | Customer register | Customer filter combinations | Partner | P2 | **met** | Industry, status and stage filters with a count (web/src/components/customer/CustomerManagement.tsx:262). |
| UAT-098 | Customer register | Open customer overview | Partner | P2 | **met** | Customer overview with eight steps. |
| UAT-099 | Customer register | Create customer validation | Partner | P2 | **met** | Add customer requires a name (CustomerManagement.tsx:176). Judged from source. |
| UAT-100 | Customer register | Add and edit fictional customer | Partner | P2 | **partly** | Add and edit work with fewer fields: no owner, device or site count on the form (G-043). |
| UAT-101 | Customer register | Cross-customer context isolation in UI | Partner | P2 | **met** | Each customer page reads that customer only. |
| UAT-102 | Customer register | Customer-linked opportunity count | Partner | P2 | **out of scope (change request)** | No opportunities (G-094). |
| UAT-103 | Assessment pipeline | Underway list and progress | Partner | P2 | **met** | /engagements shows stage, progress, next milestone and "1 customer has no engagement yet". |
| UAT-104 | Assessment pipeline | Open next milestone | Partner | P2 | **met** | /engagements shows stage, progress, next milestone and "1 customer has no engagement yet". |
| UAT-105 | Assessment pipeline | No-engagement customer state | Partner | P2 | **met** | /engagements shows stage, progress, next milestone and "1 customer has no engagement yet". |
| UAT-106 | Security assessment journey | Eight-step stepper | Partner | P1 | **met** | Eight steps plus Metrics (web/src/lib/journey.ts). |
| UAT-107 | Security assessment journey | Profile input and save | Partner | P1 | **met** | Profile saves on the server. |
| UAT-108 | Security assessment journey | Snapshot start/resume | Partner | P1 | **met** | Start or resume a snapshot. |
| UAT-109 | Security assessment journey | Domain question groups | Partner | P1 | **partly** | Questions are grouped in a side map; there is no "show one group" filter (G-097). |
| UAT-110 | Security assessment journey | Yes/No/Unsure answer selection | Partner | P1 | **met** | Yes / No / Unsure on the live set. |
| UAT-111 | Security assessment journey | Question notes | Partner | P1 | **met** | A note per question. |
| UAT-112 | Security assessment journey | Skip and previous | Partner | P1 | **met** | "Skip for now" (web/src/components/snapshot/SnapshotRunner.tsx:253). |
| UAT-113 | Security assessment journey | Client follow-up review | Partner | P1 | **met** | Client follow-up with review of each returned answer (components/followup). |
| UAT-114 | Security assessment journey | Scoring and unknown handling | Partner | P1 | **partly** | Unsure is visible and counted, but it scores as zero like a No (G-011). |
| UAT-115 | Security assessment journey | Finding explainability | Partner | P1 | **met** | "Why this finding" on each finding. |
| UAT-116 | Security assessment journey | Finding approval and override | Partner | P1 | **met** | Override, suppress or accept risk with a mandatory audit note; the original stays (Entities.cs:188-201). |
| UAT-117 | Security assessment journey | Risk ordering | Partner | P1 | **met** | Most severe first, with text labels. |
| UAT-118 | Security assessment journey | HPSM recommendation tiers | Partner | P1 | **met** | Good / Better / Best groups with setting, control and finding; "No device is changed". |
| UAT-119 | Security assessment journey | Roadmap timing buckets | Partner | P1 | **met** | Four buckets with empty-state text. Only two are ever filled by the live rules (G-009). |
| UAT-120 | Security assessment journey | Narrative source and approval | Partner | P1 | **met** | Draft, edited and approved states are shown. |
| UAT-121 | Security assessment journey | Report issuance gate | Partner | P1 | **met** | "Approve the narrative first" blocks the report. |
| UAT-122 | Security assessment journey | Next engagement logic | Partner | P1 | **met** | Rule-chosen with the reason; "Price: Not shown". |
| UAT-123 | Security assessment journey | Journey metrics | Partner | P1 | **met** | "Nothing here is a claimed saving." |
| UAT-124 | Findings, HP policies and controls | Traceability from control question | Customer | P1 | **needs content** | The framework alignment page is held until an approved mapping exists (G-116). |
| UAT-125 | Findings, HP policies and controls | Control filter All/Gaps/Verify | Customer | P1 | **needs content** | The framework alignment page is held until an approved mapping exists (G-116). |
| UAT-126 | Findings, HP policies and controls | Control filter Declared/Pending | Customer | P1 | **needs content** | The framework alignment page is held until an approved mapping exists (G-116). |
| UAT-127 | Findings, HP policies and controls | Framework claim wording | Customer | P1 | **needs content** | The framework alignment page is held until an approved mapping exists (G-116). |
| UAT-128 | Findings, HP policies and controls | HPSM product applicability | Customer | P1 | **partly** | Recommendations are marked draft on the partner side; there is no customer-side control page (G-017). |
| UAT-129 | Findings, HP policies and controls | Evidence versus response | Customer | P1 | **met** | The customer preview shows consultant-reviewed findings only. |
| UAT-130 | Findings, HP policies and controls | Device scope unknown | Customer | P1 | **met** | Fleet page: "Not connected", "Not measured". |
| UAT-131 | Legacy task and document tools | Action plan page visibility | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-132 | Legacy task and document tools | Firmware risk task tabs | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-133 | Legacy task and document tools | Task checklist progress | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-134 | Legacy task and document tools | Document type selection | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-135 | Legacy task and document tools | Generated document provenance | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-136 | Legacy task and document tools | Client packs before/during/after | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-137 | Legacy task and document tools | Conversation coach customer context | Partner | P2 | **met** | Action plan, firmware task tabs and checklist, five document types, three client packs and the coach all exist and work in the local walk. |
| UAT-138 | Commercial pipeline | Pipeline summary cards | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-139 | Commercial pipeline | Search by opportunity | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-140 | Commercial pipeline | Search by owner or customer | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-141 | Commercial pipeline | Stage filter | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-142 | Commercial pipeline | Lead-source filter | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-143 | Commercial pipeline | Sort by close/date/value/name | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-144 | Commercial pipeline | Combined filters and clear | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-145 | Commercial pipeline | Empty pipeline state | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-146 | Commercial pipeline | Register opportunity validation | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-147 | Commercial pipeline | Register multiple opportunities for same customer | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-148 | Commercial pipeline | Unique opportunity reference | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-149 | Commercial pipeline | Pipeline CSV export | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-150 | Commercial pipeline | New lead defaults | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-151 | Commercial pipeline | Stage/probability assumption | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-152 | Commercial pipeline | Lost deal aggregation | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-153 | Commercial pipeline | Won gate without priced scope | Partner | P1 | **out of scope (change request)** | No opportunity pipeline (G-029). P2. |
| UAT-154 | Opportunity workspace | Open correct opportunity | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-155 | Opportunity workspace | Separate technical and commercial stage | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-156 | Opportunity workspace | Edit commercial owner and technical lead | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-157 | Opportunity workspace | Expected close and next action | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-158 | Opportunity workspace | Tab persistence within opportunity | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-159 | Opportunity workspace | Customer assessment shortcut | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-160 | Opportunity workspace | Contract fields visibility | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-161 | Opportunity workspace | Draft status labels | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-162 | Opportunity workspace | Unsaved edit protection | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-163 | Opportunity workspace | Long text and special characters | Partner | P1 | **out of scope (change request)** | No opportunity workspace (G-029). P2. |
| UAT-164 | Quote builder | Opportunity selector linkage | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-165 | Quote builder | Add valid one-time line | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-166 | Quote builder | Add recurring monthly line | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-167 | Quote builder | Add recurring annual line | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-168 | Quote builder | Deterministic 12-month calculation | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-169 | Quote builder | Deterministic weighted forecast | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-170 | Quote builder | 18-month annual proration | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-171 | Quote builder | Term boundary | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-172 | Quote builder | Quantity and pricing validation | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-173 | Quote builder | Zero selling price | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-174 | Quote builder | Remove line item | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-175 | Quote builder | Won deal mutability | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-176 | Quote builder | Proposal HTML export | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-177 | Quote builder | Line CSV export | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-178 | Quote builder | No false licensing entitlement | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-179 | Quote builder | Customer-facing output privacy | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-180 | Quote builder | Missing reviewed findings | Partner | P1 | **out of scope (change request)** | No quote builder (G-030). P2. |
| UAT-181 | Good Better Best | Compare all tiers | Partner | P2 | **not met** | No packages page; Good / Better / Best exists only as groups of recommended settings (G-034). |
| UAT-182 | Good Better Best | Choose package for opportunity | Partner | P2 | **not met** | No packages page; Good / Better / Best exists only as groups of recommended settings (G-034). |
| UAT-183 | Good Better Best | Independent assessment integrity | Partner | P2 | **not met** | No packages page; Good / Better / Best exists only as groups of recommended settings (G-034). |
| UAT-184 | Good Better Best | Tier wording and pricing disclaimer | Partner | P2 | **not met** | No packages page; Good / Better / Best exists only as groups of recommended settings (G-034). |
| UAT-185 | Revenue modelling | Customer-base mode | Partner | P2 | **met** | "Your customer base" mode. |
| UAT-186 | Revenue modelling | Single customer mode | Partner | P2 | **met** | "One customer" mode. |
| UAT-187 | Revenue modelling | Horizon 1/3/5 years | Partner | P2 | **met** | 1, 3 and 5 year horizons. |
| UAT-188 | Revenue modelling | Invalid numerical assumptions | Partner | P2 | **partly** | Inputs are typed and bounded; negative and non-numeric entry was not exercised in this pass. |
| UAT-189 | Revenue modelling | Revenue model independence | Partner | P2 | **met** | "A scratchpad ... never change the dashboard". |
| UAT-190 | Revenue modelling | Scenario CSV export | Partner | P2 | **met** | CSV export on the results page (web/src/components/partner/RevenueResults.tsx). |
| UAT-191 | Sales reporting | Open/weighted/booking separation | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-192 | Sales reporting | Recognised revenue manually entered | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-193 | Sales reporting | ARR only on Won | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-194 | Sales reporting | Booked TCV only on Won | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-195 | Sales reporting | Gross profit sum | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-196 | Sales reporting | Multi-deal aggregation | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-197 | Sales reporting | Financial legend/units | Partner | P2 | **out of scope (change request)** | No sales dashboard (G-032). P2. |
| UAT-198 | Contracts and renewals | Contract register | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-199 | Contracts and renewals | Draft vs signed records | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-200 | Contracts and renewals | Renewal date update | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-201 | Contracts and renewals | Upcoming expiry | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-202 | Contracts and renewals | Contracted recurring reconciliation | Partner | P2 | **out of scope (change request)** | No contracts page (G-031). P2. |
| UAT-203 | Revenue attribution | Participant list for selected deal | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-204 | Revenue attribution | Add sourcing contributor | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-205 | Revenue attribution | Add HP and reseller participants | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-206 | Revenue attribution | Remove test participant | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-207 | Revenue attribution | Contribution labels | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-208 | Revenue attribution | Attribution CSV export | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-209 | Revenue attribution | No attribution duplication | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-210 | Revenue attribution | Policy disclaimer | Partner | P1 | **out of scope (change request)** | No per-deal attribution (G-033). P2. |
| UAT-211 | Work queue | Default status filter | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-212 | Work queue | Status filter all values | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-213 | Work queue | Add action required fields | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-214 | Work queue | Create linked action | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-215 | Work queue | Edit action ownership | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-216 | Work queue | Verified-complete evidence gate | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-217 | Work queue | Verified-complete success | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-218 | Work queue | Customer visibility off default | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-219 | Work queue | Explicit visibility on | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-220 | Work queue | Incorrect customer isolation | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-221 | Work queue | Task category semantics | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-222 | Work queue | Task edit modal close | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-223 | Work queue | Task local persistence | Partner | P1 | **not met** | No action queue (G-073, G-074). |
| UAT-224 | Engagement journey | Select opportunity | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-225 | Engagement journey | Five-stage lifecycle | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-226 | Engagement journey | Handover readiness checklist | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-227 | Engagement journey | Draft handover | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-228 | Engagement journey | Blocked handover | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-229 | Engagement journey | Journey activity linkage | Partner | P2 | **not met** | No engagement journey page (G-075). |
| UAT-230 | Activity history | Activity list filter | Partner | P2 | **not met** | No activity history page (G-076). |
| UAT-231 | Activity history | Create activity | Partner | P2 | **not met** | No activity history page (G-076). |
| UAT-232 | Activity history | Missing actor/detail validation | Partner | P2 | **not met** | No activity history page (G-076). |
| UAT-233 | Activity history | Activity ordering | Partner | P2 | **not met** | No activity history page (G-076). |
| UAT-234 | Activity history | No external audit claim | Partner | P2 | **not met** | No activity history page (G-076). |
| UAT-235 | Customer workspace | Switch customer role | Customer | P1 | **partly** | There is no Customer role; partner staff switch to a read-only customer preview (G-044). |
| UAT-236 | Customer workspace | Customer security KPI accuracy | Customer | P1 | **partly** | Tiles show reviewed findings and answered counts, not definitive and unknown counts (G-109). |
| UAT-237 | Customer workspace | Not verified caveat | Customer | P1 | **met** | "Answers given in an assessment are self-reported and are not device verification." |
| UAT-238 | Customer workspace | Customer switching | Customer | P1 | **met** | Customer switcher on the customer pages. |
| UAT-239 | Customer workspace | No partner commercial leakage | Customer | P1 | **met** | No commercial data exists to leak. |
| UAT-240 | Customer workspace | Customer page link navigation | Customer | P1 | **met** | The customer stays selected across the seven pages. |
| UAT-241 | Fleet inventory | Sample site/device counts | Customer | P2 | **met** | Declared counts from the profile, "Not connected", per customer. |
| UAT-242 | Fleet inventory | Missing real device evidence | Customer | P2 | **met** | Declared counts from the profile, "Not connected", per customer. |
| UAT-243 | Fleet inventory | Customer switch on fleet page | Customer | P2 | **met** | Declared counts from the profile, "Not connected", per customer. |
| UAT-244 | Customer findings and remediation | Approved findings only | Customer | P1 | **met** | Reviewed findings only. |
| UAT-245 | Customer findings and remediation | Findings severity labels | Customer | P1 | **met** | Severity in words. |
| UAT-246 | Customer findings and remediation | Link to remediation | Customer | P1 | **partly** | Findings link to the roadmap; no finding id or priority carried into a task (no tasks). |
| UAT-247 | Customer findings and remediation | Empty findings state | Customer | P1 | **met** | "No consultant-reviewed findings yet." |
| UAT-248 | Customer roadmap | Roadmap actions from reviewed findings | Customer | P2 | **met** | Reviewed findings by timeframe. |
| UAT-249 | Customer roadmap | Task status separation | Customer | P2 | **partly** | No tasks exist, so nothing internal can show; nothing published either (G-120). |
| UAT-250 | Customer roadmap | Owner and priority | Customer | P2 | **partly** | "Owner: Not recorded" (G-117). |
| UAT-251 | Customer reporting | Report withheld before approval | Customer | P1 | **met** | "Not released". |
| UAT-252 | Customer reporting | Approved report available | Customer | P1 | **met** | An issued report is offered for that customer. |
| UAT-253 | Customer reporting | Customer report scope | Customer | P1 | **met** | Approved narrative and reviewed findings only; no commercial data exists. |
| UAT-254 | Customer reporting | Evidence status markers | Customer | P1 | **partly** | Two tiles, not the three-step status (G-118). |
| UAT-255 | Customer reporting | No external distribution claim | Customer | P1 | **partly** | No such note on the customer page; Admin shows "Customer email delivery — Not connected" (G-118). |
| UAT-256 | Continuous assurance | Assurance coverage display | Customer | P2 | **partly** | No unknown or unanswered count on this page (G-119). |
| UAT-257 | Continuous assurance | No fabricated telemetry | Customer | P2 | **met** | "Not connected", "Not scheduled". |
| UAT-258 | Continuous assurance | Repeat assessment state | Customer | P2 | **partly** | No reassessment guidance (G-119). |
| UAT-259 | Customer shared actions | Published action visibility | Customer | P1 | **not met** | No shared-actions page (G-120). |
| UAT-260 | Customer shared actions | No commercial task leakage | Customer | P1 | **not met** | No shared-actions page (G-120). |
| UAT-261 | Customer shared actions | Read-only customer actions | Customer | P1 | **not met** | No shared-actions page (G-120). |
| UAT-262 | Customer shared actions | Cross-customer object isolation UI | Customer | P1 | **not met** | No shared-actions page (G-120). |
| UAT-263 | Resources and modules | Eleven module index | Partner | P2 | **met** | Eleven modules with status tags, in order, with previous and next. |
| UAT-264 | Resources and modules | Module navigation | Partner | P2 | **met** | Eleven modules with status tags, in order, with previous and next. |
| UAT-265 | Resources and modules | Practice touchpoints | Partner | P2 | **met** | Eleven modules with status tags, in order, with previous and next. |
| UAT-266 | Resources and modules | Missing approved content | Partner | P2 | **met** | Eleven modules with status tags, in order, with previous and next. |
| UAT-267 | Administration and workspace tools | Admin-only menu | Admin | P1 | **met** | Admin page for Admin only. |
| UAT-268 | Administration and workspace tools | Partner/Consultant admin guard | Admin | P1 | **met** | Other roles do not get the Admin page. |
| UAT-269 | Administration and workspace tools | Demo access read-only | Admin | P1 | **met** | Demo is read-only (server-enforced). |
| UAT-270 | Administration and workspace tools | Export workspace JSON | Admin | P1 | **out of scope (change request)** | Prototype-only export and import; recommended not to build (D-041). Marked out of scope rather than a change request. |
| UAT-271 | Administration and workspace tools | Import valid JSON | Admin | P1 | **out of scope (change request)** | Prototype-only export and import; recommended not to build (D-041). Marked out of scope rather than a change request. |
| UAT-272 | Administration and workspace tools | Import invalid JSON | Admin | P1 | **out of scope (change request)** | Prototype-only export and import; recommended not to build (D-041). Marked out of scope rather than a change request. |
| UAT-273 | Administration and workspace tools | Feedback capture | Admin | P1 | **partly** | Feedback on the site is real: it is stored on the server and can be sent on, so "not sent to a recipient" is deliberately untrue here. |
| UAT-274 | Administration and workspace tools | Reset/erase safeguarding | Admin | P1 | **met** | "Reset demo" is restricted (Caller.cs:31). |
| UAT-275 | Access and role boundaries | Customer role cannot enter Partner workspace | Partner | P0 | **not met** | No Customer role (G-044). |
| UAT-276 | Access and role boundaries | Partner view does not expose customer secrets inadvertently | Partner | P0 | **met** | The customer preview shows only reviewed, customer-safe content. |
| UAT-277 | Access and role boundaries | Consultant/Admin available menus | Partner | P0 | **met** | Menus differ by role as designed (local walk as four roles). |
| UAT-278 | Access and role boundaries | Demo read-only across modules | Partner | P0 | **met** | Demo cannot change records (server-enforced). Judged from source. |
| UAT-279 | Access and role boundaries | Role switch resets incompatible route | Partner | P0 | **not met** | No in-app role switch; role is fixed at sign-in (G-044). |
| UAT-280 | Access and role boundaries | Blocked deep-link to admin | Partner | P0 | **met** | /admin as a non-admin does not show admin controls. |
| UAT-281 | Access and role boundaries | Role selector is explicitly demo | Partner | P0 | **partly** | The local sign-in says "Demo sign-in: no password"; the hosted site uses real sign-in, so the test does not apply as written. |
| UAT-282 | Operational gates | Eight operational requirements | Partner | P1 | **not met** | No operational readiness page (G-091). |
| UAT-283 | Operational gates | Self-declared gate count | Partner | P1 | **not met** | No operational readiness page (G-091). |
| UAT-284 | Operational gates | No security control implied | Partner | P1 | **not met** | No operational readiness page (G-091). |
| UAT-285 | Operational gates | Export requirements checklist | Partner | P1 | **not met** | No operational readiness page (G-091). |

## 3. v2.1 UAT tracker: non-functional cases

| ID | Area | Scenario | Verdict against main | Evidence |
|---|---|---|---|---|
| NF-001 | Responsive layout | No horizontal overflow at 390px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-002 | Responsive layout | No horizontal overflow at 430px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-003 | Responsive layout | No horizontal overflow at 768px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-004 | Responsive layout | No horizontal overflow at 820px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-005 | Responsive layout | No horizontal overflow at 1024px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-006 | Responsive layout | No horizontal overflow at 1280px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-007 | Responsive layout | No horizontal overflow at 1500px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-008 | Responsive layout | No horizontal overflow at 1600px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-009 | Responsive layout | No horizontal overflow at 1920px | **partly** | The site is tested for reflow at desktop, tablet and phone widths on its own pages by its end-to-end suite (web/README.md); four of the six named pages (Pipeline, Quote, Attribution, Controls) do not exist. Not re-run in this pass. |
| NF-010 | UI consistency | Consistent spacing on Partner dashboard | **partly** | Partner home exists with a different composition. |
| NF-011 | UI consistency | Consistent spacing on Opportunity pipeline | **out of scope (change request)** | Page does not exist (commercial, P2). |
| NF-012 | UI consistency | Consistent spacing on Opportunity detail | **out of scope (change request)** | Page does not exist (commercial, P2). |
| NF-013 | UI consistency | Consistent spacing on Quote builder | **out of scope (change request)** | Page does not exist (commercial, P2). |
| NF-014 | UI consistency | Consistent spacing on Revenue attribution | **out of scope (change request)** | Page does not exist (commercial, P2). |
| NF-015 | UI consistency | Consistent spacing on Work queue | **not met** | No work queue page. |
| NF-016 | UI consistency | Consistent spacing on Customer dashboard | **partly** | Customer dashboard exists with different tiles. |
| NF-017 | UI consistency | Consistent spacing on Control mapping | **needs content** | Control mapping page held. |
| NF-018 | UI consistency | Consistent spacing on Customer report | **partly** | The customer report is a PDF, not a page. |
| NF-019 | Accessibility / robustness | Keyboard-only navigation | **met** | Keyboard-only walk is part of the site's end-to-end suite (web/README.md). Not re-run in this pass. |
| NF-020 | Accessibility / robustness | Dialog focus containment | **not met** | The opportunity and task dialogs do not exist. |
| NF-021 | Accessibility / robustness | Visible focus at zoom | **partly** | Covered for the site's own pages by its automated accessibility checks; no manual zoom or screen-reader run in this pass. |
| NF-022 | Accessibility / robustness | Semantic inputs and errors | **partly** | Covered for the site's own pages by its automated accessibility checks; no manual zoom or screen-reader run in this pass. |
| NF-023 | Accessibility / robustness | Colour contrast | **met** | Every colour pair is contrast-tested (web/src/design/contrast.ts) and severity is always in words. From source. |
| NF-024 | Accessibility / robustness | Non-colour statuses | **met** | Every colour pair is contrast-tested (web/src/design/contrast.ts) and severity is always in words. From source. |
| NF-025 | Accessibility / robustness | Touch targets | **partly** | Not run in this pass; the site has automated checks only. |
| NF-026 | Accessibility / robustness | Reduced motion | **partly** | Not run in this pass; the site has automated checks only. |
| NF-027 | Accessibility / robustness | Screen-reader landmarks | **partly** | Not run in this pass; the site has automated checks only. |
| NF-028 | Accessibility / robustness | Error feedback aria-live | **partly** | Not run in this pass; the site has automated checks only. |
| NF-029 | Accessibility / robustness | Text scaling and reflow | **partly** | Not run in this pass; the site has automated checks only. |
| NF-030 | Accessibility / robustness | Browser Back and Forward | **met** | Real page addresses; Back and Forward work. |
| NF-031 | Accessibility / robustness | Direct-link invalid route | **met** | Unknown addresses answer a not-found page (web/src/proxy.ts). |
| NF-032 | Accessibility / robustness | Escaped user text | **met** | Entered text is escaped on screen and in the PDF; invisible-only names are refused by ruling. From source. |
| NF-033 | Accessibility / robustness | Local storage absent | **met** | Equivalent: records are on the server, not in browser storage. |
| NF-034 | Accessibility / robustness | Reload persistence | **met** | Equivalent: records are on the server, not in browser storage. |
| NF-035 | Accessibility / robustness | Large input bounds | **not met** | No task or activity fields to limit. |
| NF-036 | Accessibility / robustness | Bulk data performance | **out of scope (change request)** | Needs import and the commercial records. |
| NF-037 | Accessibility / robustness | Browser compatibility | **partly** | The site's suite runs in Chromium; other browsers not run in this pass. |
| NF-038 | Accessibility / robustness | Accessibility evidence | **not met** | No formal WCAG 2.2 AA audit with assistive technology on record. |

## 4. v2.1 UAT tracker: production gates

The tracker marks all 32 "Blocked — not implemented" for the HTML. The site is a hosted application, so some are partly in place. These verdicts are shallow: each rests on the one fact named, and a gate is "not met" where this pass found no evidence, which is not proof of absence.

| ID | Domain | Requirement | Verdict against main | Evidence |
|---|---|---|---|---|
| PRD-001 | Identity | Entra OIDC sign-in and trusted session | **partly** | Hosted sign-in with Microsoft Entra exists (web/README.md); the UAT site currently runs its open review sign-in. |
| PRD-002 | Identity | Conditional Access and MFA | **not met** | Tenant policy; nothing in this repository. |
| PRD-003 | Authorisation | Partner-to-customer scope | **partly** | Partner sees own customers only (Caller.cs:208). |
| PRD-004 | Authorisation | Customer-to-customer isolation | **not met** | No customer sign-in exists. |
| PRD-005 | Authorisation | Admin/consultant privilege boundaries | **partly** | Role checks on every endpoint (Caller.cs). |
| PRD-006 | Authorisation | Revocation of delegated access | **not met** | No delegated access. |
| PRD-007 | Authorisation | Backend-owned approval gates | **met** | The report refuses to issue without an approved narrative, on the server. |
| PRD-008 | Data | Durable, encrypted record storage | **partly** | Database storage with stamped records; encryption settings not assessed in this pass. |
| PRD-009 | Data | Data segregation and residency | **not met** | Not assessed in this pass. |
| PRD-010 | Data | Retention and erasure | **partly** | Open ticket HPSMPOC-100 (retention). |
| PRD-011 | Audit | Tamper-evident event records | **partly** | Append-only audit; the ledger table is open ticket HPSMPOC-117. |
| PRD-012 | Audit | Security event monitoring | **not met** | Open ticket HPSMPOC-224 (no telemetry). |
| PRD-013 | Evidence | Evidence upload safety | **not met** | No evidence file upload; evidence is a typed reference. |
| PRD-014 | Evidence | Signed report approvals | **partly** | The reviewer's role and time are recorded with the approval. |
| PRD-015 | Reports | Secure customer exports | **partly** | PDF with checksum verified on download; no secure sharing link. |
| PRD-016 | Integrations | HP/HPSM technical applicability | **needs content** | Needs HP technical validation. |
| PRD-017 | Integrations | Microsoft Entra/Intune/Universal Print | **out of scope (change request)** | Integration. |
| PRD-018 | Integrations | CRM opportunities and idempotency | **out of scope (change request)** | Integration. |
| PRD-019 | Integrations | Pricebook/SKU synchronisation | **out of scope (change request)** | Integration. |
| PRD-020 | Integrations | Finance ERP recognition | **out of scope (change request)** | Integration. |
| PRD-021 | Commercial | Commission policy approval | **out of scope (change request)** | Commercial policy. |
| PRD-022 | Commercial | Signed contract workflow | **out of scope (change request)** | Commercial workflow. |
| PRD-023 | Security | Threat model and penetration test | **not met** | No independent penetration test on record. |
| PRD-024 | Security | Input validation and injection | **partly** | Server-side validation exists; not assessed in depth in this pass. |
| PRD-025 | Security | Rate limits and denial-of-service | **not met** | Not assessed in this pass. |
| PRD-026 | Performance | Production page and API latency | **not met** | Not assessed in this pass. |
| PRD-027 | Resilience | Conflict resolution on concurrent edits | **partly** | Concurrent edits are refused with a clear message (version stamps). |
| PRD-028 | Resilience | Backup restore and disaster recovery | **not met** | Not assessed in this pass. |
| PRD-029 | Accessibility | Formal WCAG 2.2 AA audit | **not met** | No formal audit on record. |
| PRD-030 | Governance | Security and legal release approval | **not met** | Not held. |
| PRD-031 | Governance | Real reseller and customer pilot | **not met** | Not held. |
| PRD-032 | Governance | Production deployment rollback | **not met** | Not assessed in this pass. |

## 5. v2.1 UAT plan: end-to-end journeys

| ID | Journey | Role | Priority | Verdict against main | Evidence |
|---|---|---|---|---|---|
| E2E-01 | Partner onboarding to first opportunity | Partner | P0 | **partly** | Readiness and training exist; onboarding and opportunity registration do not. |
| E2E-02 | HP referral through customer qualification | Partner | P0 | **out of scope (change request)** | Needs opportunities and contributors. |
| E2E-03 | Independent customer security assessment | Consultant | P0 | **partly** | The assessment, notes, score and findings work; the ISO/NIST mapping step is held. |
| E2E-04 | Assessment to Good/Better/Best proposal | Partner | P0 | **out of scope (change request)** | Needs opportunities and the quote builder. |
| E2E-05 | Proposal to signed Won deal | Partner | P0 | **out of scope (change request)** | Needs opportunities. |
| E2E-06 | Reseller and HP contribution record | Partner | P0 | **out of scope (change request)** | Needs attribution. |
| E2E-07 | Action ownership, verification and customer publication | Partner then Customer | P0 | **not met** | Needs the action queue and shared actions. |
| E2E-08 | Customer security report publication | Consultant then Customer | P0 | **met** | Report blocked before approval, issued after, and shown in the customer preview with no commercial data. The export is a PDF. |
| E2E-09 | Delivery handover and renewal | Partner | P1 | **not met** | Needs the engagement journey and contracts. |
| E2E-10 | Sales dashboard and contract reconciliation | Partner | P0 | **out of scope (change request)** | Needs the sales dashboard. |
| E2E-11 | Role-switch privacy boundary | Partner then Customer then Demo | P0 | **partly** | The customer preview holds no commercial content and Demo cannot edit; there is no Customer role or in-app role switch. |
| E2E-12 | Operational readiness and deployment decision | Admin and release owners | P0 | **not met** | No operational readiness page. |
