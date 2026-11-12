# HPSM-POC Playbook site: where the messaging document lands

Prepared 2026-11-12 for the product owner's request of 10:51 ("please find attached additional feedback to the HP messaging. Please use these and deploy").
Nothing here has been built, committed or sent. This is the map a builder applies.

Conventions used in every table:
- "MA:n" = line n of `messaging_alignment.txt` in the 2026-11-12 attachments folder under `2_Project_Files/fleet/state/` (the .docx sits beside it) (the extracted text; the original .docx was read with python zipfile to resolve line breaks inside cells and the table pairing, e.g. the awareness copy is four separate lines, and every Use / Avoid row pairs as printed).
- "file:line" = at origin main, sha `c717ba1a945191ffa31f13320c19967a6cf7f15a` (committed 2026-11-11T10:24:41Z; origin main read again at 2026-11-12 and still that sha). The local checkout is stale (HEAD `8869b1a9`, 2026-09-23), so it was NOT used. Paths are under `web/src/` unless they start `api/`.
- Quoted copy is ASCII here. The document uses typographic apostrophes, quotes and arrows; the builder copies them from the document (the walkthrough file already holds typographic characters). In "today" cells, "[em dash]" and "->" stand for the characters in the source.
- Classes: **A** the document gives the exact words for the slot; **B** a language-rule fix, the sentence is NEW WORDS composed from the rule; **C** held; **D** a section 8 claim that needs HP or SME verification: the proposed text is the qualified form, built from words the document itself gives.
- "New words" in a proposed cell means the product owner has not seen that sentence.

## BLUF

59 rows to change or hold: **A = 22, B = 13, C = 13, D = 11** (counts printed from this file's tables by `awk`, instrument in "Instruments" below).

- **Can ship now (text only, no layout, no new element): 22 A + 13 B = 35 rows**, plus **9 of the 11 D rows in their qualified form** (they remove or soften an unverified claim and use the document's own alternative words). That is 44 rows, all string swaps in 8 source files plus one C# file for the report's tier sentence.
- **D rows held: 2** (the Playbook deck's own sentences at the Phase 2 module, and the firmware question). Those are HP's deck text and the assessment content: changing them needs a new content version and an HP SME sentence the document does not give.
- **Held as C: 13.** The biggest: the document's **Primary partner landing page copy deck (MA:208-231)**. The site has no landing, about or marketing page (56 page routes read; the only marketing-style words are the sign-in side panel and the Home page), so the headline, intro, six modules and closing copy have no slot. Next biggest: the journey rename (Discover, Assess, Recommend, Engage), held by the product owner's 2026-11-10 ruling. The other C rows are new pages or elements (customer-report introduction, hero block, three operating modes, Good/Better/Best packages page, commercial stages in the dashboard) that the phase document puts in the next phase.
- **Walkthrough**: the demo narrative is the largest single surface (19 rows). Most of the document's "Activate" step (MA:273) lands there.
- **Constraints that bite**: the Home page text is pinned whole by a test that records the product owner's ruled words (2 states), the section region is named by a heading three tests and one e2e find by name, and the tier sentence is shared by screen, PDF and 5 tests. All listed under "For the builder".

## Recommendation

1. Ship one text-only pass: A rows, B rows, and the 9 D rows in qualified form. Update the pinned tests in the same change (list below). No layout, no new element, no new route, no data-model change, no content-package version.
2. Do not build any C row. Put each C row's question (below) to the product owner; the default for every one is "hold".
3. Hold the two D rows on HP's deck text and the firmware question; they ride with the phase document's firmware wording items (D-004, D-005, D-006), which already need an HP SME.
4. Three rows alter words the product owner ruled earlier and are pinned as ruled (Home lead and closing block; the phase panel's "Partner earns" and legend). The document is newer and is his own feedback, so they are in the A/B set, but the commit message should say so.
5. The morning's revised Playbook Messaging loses to this document wherever they differ (see Conflicts). One of its sentences, "Recommendations map findings to named HP Security Manager policy settings", must NOT be pasted anywhere: the document lists that pattern under "Avoid" (MA:62) and a standing test already forbids it in the walkthrough.

## Overlap with the phase decision document (2026-11-10)

Read from `DECISION-DOCUMENT.corrected.md` (BLUF lines 1-30, then grep for home, hero, landing, messaging, wording, rename, journey, with the row and section headings). Overlaps:

| D-item | Phase | Rows here |
|---|---|---|
| D-022 stop presenting consulting fees as the expected way to earn | THIS PHASE | H-legend, H-earns x3, W12, W13, W14 |
| D-014 say plainly that HP Security Manager settings are unconfirmed | THIS PHASE | R1, W11 |
| D-004, D-005, D-006 firmware, "HPSM deploys firmware", trusted startup | THIS PHASE (needs HP SME) | K3, W10 context |
| D-019 does "Next engagement" belong in the customer report | THIS PHASE (a ruling) | R5 |
| D-023 three reseller operating modes | NEXT PHASE | C-modes |
| D-027 Good / Better / Best service packages page | NEXT PHASE | C-gbb |
| D-030 product name "HP Cyber Security Services Playbook" | NEXT PHASE | no change here (the title stays) |
| D-037 one notice per page | NEXT PHASE | no change (the prototype banner stays) |
| D-043 partner dashboard rebuilt around the pipeline | NEXT PHASE | C-hero, C-stages |
| D-047 training page descriptions | NEXT PHASE | C-training |
| D-056 delivery phases page descriptions | NEXT PHASE | C-phase3, V1 |
| D-058 keep the site's Playbook module names and text | DROP | C-deck |
| D-064 journey rail rename | NEXT PHASE | C-rename |
| D-069 conversation coach talk tracks | NEXT PHASE | C-coach |

No D-item is about the sign-in panel, page titles or meta description: those rows are not covered by the phase document either way.

## Surface 1: page titles and meta

Per-route titles (`metadata.title` in 56 route files) are navigation names, not positioning: unchanged. The default title "HP Security Services Playbook" (`app/layout.tsx:7`) stays (D-030 holds the name).

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| M1 | `app/layout.tsx:8` (meta description) | "HP Security Services Playbook digital proof of concept (Datasec). Clickable prototype, synthetic data." | "A simpler way to sell, deliver and grow print security services with HP. Digital proof of concept (Datasec): clickable prototype, synthetic data." (the promise first, the demonstrator status kept because MA:233 requires it) | promise MA:78; status rule MA:233 | B |

## Surface 2: sign-in (the only public-facing marketing words)

Three states render these words: the mock sign-in (`SignInScreen.tsx:60`), the Microsoft sign-in (`:150`), and the side panel (`:110-121`, `aria-hidden`, and `hidden` below the lg breakpoint, so a phone or tablet never shows it). The UAT start page (`UatStartScreen.tsx:92`, "This is a review copy with sample customers only. Choose how you would like to see it.") is operational and unchanged.

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| S1 | `components/screens/SignInScreen.tsx:60` and `:150` (lead; eyebrow "Proof of concept" stays) | "From readiness to recurring revenue, in one guided workflow." | "A simpler way to sell, deliver and grow print security services with HP." | MA:78 (primary product promise), verbatim | A |
| S2 | `components/screens/SignInScreen.tsx:116` (panel headline, three lines with line breaks) | "Greater security." / "Stronger practice." / "Recurring revenue." | "The trust you've earned." / "The opportunity ahead." (two lines) | MA:75 (campaign headline), verbatim | A |
| S3 | `components/screens/SignInScreen.tsx:118` (panel sentence) | "Practical guidance, tools and resources to assess customers, deliver secure print services and grow a managed service." | "Guided assessments, evidence-based recommendations, relevant HP solution opportunities and ongoing customer value." | MA:81 (value proposition), verbatim | A |

## Surface 3: Home (the partner dashboard) and its phase panel

Home is the "Playbook home / hero" surface of MA:172-175 (audience: HP account managers, resellers, partner principals; CTA "Start a customer assessment"). It has a title, a lead, a greeting, KPI tiles and the phase panel; it has no hero block.

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| H1 | `components/partner/PartnerDashboard.tsx:74` (lead under the title "Home") | "Your overview of readiness, customers, actions and opportunities." | "A simpler way to sell, deliver and grow print security services with HP." (displaces the overview sentence; the title "Home" and the greeting stay) | MA:78; surface MA:172-175 | A |
| H2 | `components/partner/PartnerDashboard.tsx:79` (button) | "Start a customer snapshot" | "Start a customer assessment" | MA:175 (CTA for Playbook home), verbatim | A |
| H3 | `components/partner/PartnerDashboard.tsx:271-272` (closing block heading and sentence) | "Drive more customer success" / "Run a snapshot with a customer to see their security posture and the next engagement." | Heading "Start with one customer. Build what comes next." Sentence "You have the customer relationship. You have the HP expertise. Now you have a clearer way to turn both into customer value." (also drops "security posture", which MA:238 says a questionnaire alone does not prove) | MA:231 (closing copy), MA:90 | A |
| H4 | `components/partner/PartnerDashboard.tsx:275` (button, same destination) | "Start a customer snapshot" | "Start a customer assessment" | MA:175 | A |
| H5 | `components/partner/PartnerDashboard.tsx:254` ("Where to next" tile text) | "Model the opportunity across the three phases." | "Model an illustrative opportunity across the three phases." (new words) | MA:67-68, MA:160 | B |
| H6 | `components/partner/PartnerDashboard.tsx:135` (tile "Managed service run-rate, end of year 3") and `:180` (panel "Revenue mix"); both already carry the Illustrative tag | tag text "Illustrative" | add to the tag's title attribute and the tile `sub` line: "Estimate, not booked or recognised revenue." (new words; the tag stays) | MA:160, MA:256 | B |
| H-hero | Home, new block under the greeting: trust-led promise, three lifecycle phases, partner models, short proof points | none exists | none proposed (a new block is layout; the document gives the emphasis, not the words, for this block) | MA:172-175 | C |
| P1 | `components/home/phase-flow.ts:20` (panel title; also the region's accessible name) | "Three phases, one simple partner motion" | "Assess. Implement. Optimize." | MA:84 (lifecycle), verbatim | A |
| P2 | `components/home/phase-flow.ts:21` (panel lead) | "Use the playbook like a services operating system: assess, implement, then optimize and renew." | "One guided experience. Multiple partner business models." | MA:87 (differentiator), verbatim | A |
| P3 | `components/home/phase-flow.ts:22` (legend) and `:23` (screen-reader label on 11 of the 13 activities) | "Datasec Consulting Services touchpoints" / "Datasec Consulting Services touchpoint" | "Optional Datasec services touchpoints (paid or no-fee)" / "Optional Datasec services touchpoint" (new words) | MA:48, MA:65-66 | B |
| P4 | `components/home/phase-flow.ts:24` (theme) and `:28` (`besideTheme`, which a test reads) | "HP-backed tools" | "Applicable HP solutions" (change both strings together) | MA:61 (Use column); MA:46 (HP-backed needs approval) | D |
| P5a | `components/home/PhaseFlow.tsx:65` (label) | "Partner earns:" | "Possible commercial follow-up:" | MA:126 (column heading) | A |
| P5b | `components/home/phase-flow.ts:40` (Assess `earns`) | "discovery revenue + roadmap ownership" | "No-fee or paid review; discovery; gap assessment; qualified attach." | MA:130, verbatim | A |
| P5c | `components/home/phase-flow.ts:51` (Implement `earns`) | "project revenue + solution attach" | "HP software, secure print, authentication, configuration, services, lifecycle." | MA:134, verbatim | A |
| P5d | `components/home/phase-flow.ts:62` (Optimize `earns`) | "retainer or per-device managed services revenue" | "Managed assurance, renewals, services, fleet improvement and retention." | MA:138, verbatim | A |
| P6 | `components/home/phase-flow.ts:39`, `:50`, `:61` (Tools / assets lists name HP Firmware Security Tool, HP Threat Assessment, HP Threat Assessment Reporting, "SIEM integration if available") and the heading `components/home/PhaseFlow.tsx:52` | the lists, with no status | keep the lists; add one line under each "Tools / assets" heading: "Tools named here are planned or subject to implementation until release validation is complete." (MA:260 wording). Whether "SIEM integration if available" stays on a page shown to HP is the product owner's call (standing rule: no integration is shown as done) | MA:260 | D |

## Surface 4: the demo walkthrough (`content/walkthrough/steps.ts`)

This is "demo narrative" of MA:273. The cover and 14 steps are data in one file. Steps already hedge several claims correctly (the draft-score caveat at `:103`, "representative ... where one is mapped" at `:111`, the illustrative note at `:191`): those are listed under "checked, no change".

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| W1 | `content/walkthrough/steps.ts:41` (cover headline) | "Print security services. Simple to sell. Built to grow." | "The trust you've earned. The opportunity ahead." | MA:75 | A |
| W2 | `content/walkthrough/steps.ts:42` (cover lead) | "A practical way for HP partners to turn one customer conversation into a guided assessment, HP-backed action and recurring services[em dash]without becoming a cybersecurity company." | "From trusted print partner to security-led business growth. The Playbook connects guided assessments, reviewed findings, HP-aligned recommendations, customer reporting and commercial next steps. Partners can deepen existing relationships, deliver relevant technology and services, and build recurring engagement without having to become cybersecurity consultancies." | MA:96 (breakthrough value description), verbatim | A |
| W3 | `content/walkthrough/steps.ts:53` (step 1 `say`, last sentence) | "Today, we are going to show a simpler way to sell, deliver, and grow with HP security." | "Today, we are going to show a simpler way to sell, deliver and grow print security services with HP." | MA:78 | A |
| W4 | `content/walkthrough/steps.ts:58` (step 2 `key`) | "Sellers: what to say. Delivery: what to do. Business: a repeatable revenue path." | "Sellers: what to say. Delivery: what to do. Business: a repeatable commercial path." (new words) | MA:48, MA:66 | B |
| W5 | `content/walkthrough/steps.ts:59` (step 2 `purpose`) | "A guided motion from customer uncertainty to an HP-backed next action." | "A guided motion from customer uncertainty to a next action mapped to applicable HP capabilities." | MA:46 (the document's own alternative), MA:62 | D |
| W6 | `content/walkthrough/steps.ts:61` (step 2 `say`) | "...to an assessment, an HP-backed action, and a commercial next step... a repeatable path to revenue." | "...to an assessment, a recommendation mapped to applicable HP capabilities, and a commercial next step... a repeatable path to new opportunities." (rest of the sentence unchanged) | MA:46; MA:48, MA:66 | D |
| W7 | `content/walkthrough/steps.ts:66-70` (step 3 "Assess -> Implement -> Optimize"; no `caveat` today) | no caveat | add `caveat`: "It guides the workflow; delivery may require HP management products, other authorised systems, qualified personnel and customer change approval." | MA:139 (second and third sentences), verbatim | A |
| W8 | `content/walkthrough/steps.ts:107` (step 8 `title`) | "From finding to HP-backed action" | "From finding to action" | MA:46, MA:62 | D |
| W9 | `content/walkthrough/steps.ts:108` (step 8 `key`) | "One clearly scoped next step, backed by HP technical depth." | "One clearly scoped next step, mapped to applicable HP capabilities." | MA:46 | D |
| W10 | `content/walkthrough/steps.ts:111` (step 8 `say`, last two sentences) | "You keep control, use HP-backed technical depth, and create a natural bridge to implementation, HP security solutions, and the wider print relationship." | "You keep control, use the applicable HP capabilities, and create a natural bridge to implementation, HP security solutions, and the wider print relationship." (keeps the two phrases a test requires) | MA:46, MA:241 | D |
| W11 | `content/walkthrough/steps.ts:112` (step 8 `caveat`) | "HP/HPSM mapping and exact device setting applicability require validation before deployment." | the same sentence plus: "Mapping to named settings applies only where supported for the relevant device, firmware and HP Security Manager edition." (new words) | MA:241, MA:244 | B |
| W12 | `content/walkthrough/steps.ts:145` (step 12 `key`) | "Discovery fees -> implementation and attach -> reviews and managed services." | "Optional paid or no-fee assessment -> implementation and attach -> reviews, renewals and managed services." (new words) | MA:66, MA:130-138 | B |
| W13 | `content/walkthrough/steps.ts:148` (step 12 `say`) | "Assess creates discovery revenue. Implement creates project revenue and solution attach. Optimize creates reviews, retainers, and per-device managed services revenue." | "Assess can open a no-fee or paid review, discovery, a gap assessment or a qualified attach. Implement can lead to HP software, secure print, authentication, configuration, services and lifecycle work. Optimize can lead to managed assurance, renewals, services, fleet improvement and retention." (the document's phrases joined by new connecting words) | MA:130, MA:134, MA:138; MA:68 | B |
| W14 | `content/walkthrough/steps.ts:155` (step 13 `purpose`) and `:157` (step 13 `say`, last sentence) | "...and recurring revenue." (both) | "...and recurring engagement." (both; the pinned phrases "implementation (including security software attach)" and "implementation, including software attach" stay) | MA:96, MA:160 | B |
| W15 | `content/walkthrough/steps.ts:163` (step 14 `key`) | "Easier to sell. Repeatable to deliver. Supported by HP." | "Start with one customer. Build what comes next." (removes "Supported by HP", an unverified backing claim) | MA:90 | A |
| W16 | `content/walkthrough/steps.ts:165` (step 14 `cue`) | "Return to Home. Keep Assess -> Implement -> Optimize on screen and make one invitation." | "Return to Home. Keep Assess -> Implement -> Optimize on screen and make one invitation: Select one account -> run a guided conversation -> agree the next step." | MA:55, verbatim | A |
| W17 | `content/walkthrough/steps.ts:166` (step 14 `say`) | "...turns findings into HP-backed action, and grows into assessment, implementation, attach, and recurring-services revenue." | "...turns findings into recommendations mapped to applicable HP capabilities, and grows into assessment, implementation, attach and recurring services." (the first sentence "You do not need to become a cybersecurity company..." stays: MA:26 keeps the idea) | MA:46, MA:26, MA:96 | D |
| W18 | `content/walkthrough/steps.ts:187-189` (bridge cell `revenue` field, drawn as "01 / Assess [em dash] ...") | "Discovery revenue" / "Project + solution attach" / "Recurring service revenue" | "No-fee or paid review; discovery; gap assessment; qualified attach." / "HP software, secure print, authentication, configuration, services, lifecycle." / "Managed assurance, renewals, services, fleet improvement and retention." | MA:130, MA:134, MA:138, verbatim | A |
| W19 | `content/walkthrough/steps.ts:187-189` (bridge cell `text` field) | "Security snapshot, evidence review and scoped roadmap" / "Hardening, services, software and approved devices" / "Reviews, retainers and per-device managed assurance" | "Understand the fleet, confirm evidence and prioritise issues." / "Act through configuration, platform, identity, process, remediation or suitable replacement." / "Maintain assurance, monitor drift and revisit customer needs." | MA:128, MA:132, MA:136, verbatim | A |

## Surface 5: recommendations, tiers, next engagement, revenue pages, reports

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| R1 | `components/screens/RecommendationScreen.tsx:44` (lead) | "Each finding maps to a representative policy setting recommendation." | "Recommendations are mapped to applicable HP capabilities where a mapping exists. The setting shown is representative and must be checked for the customer's device, firmware and HP Security Manager edition." (new words, built from the document's qualified phrases) | MA:62 (avoid "every finding maps to..."), MA:46, MA:241 | D |
| R2 | `components/screens/RecommendationScreen.tsx:34-36` (`TIERS_EXPLAINED`) and the PDF's same sentence `api/src/HpsmPoc.Modules.Reporting/Report/ReportModelBuilder.cs:282-285` (`TiersExplained`); the two must stay equal | "...Groupings only: no prices or revenue. Grouping proposed for HP to vet." | keep both pinned sentences exactly, and insert between them: "Tiers are options informed by risk and scope, selected by the partner. None requires paid consulting or a hardware replacement." (new words) | MA:250 | B |
| R3 | `components/screens/NextEngagementScreen.tsx:23` (lead) | "The logical next paid engagement, chosen by rule, with the reason shown." | "The logical next engagement (a paid assessment, a no-fee review or a managed review), chosen by rule, with the reason shown." (new words) | MA:65-66 | B |
| R4 | `components/shell/PrototypeBanner.tsx:20` (second banner line on the two revenue pages) | "Every figure on this page comes from the sample revenue model. [notice]" | append the document's sentence: "Opportunity estimates must not be equated with contracted revenue, gross profit or employee commission." (the notice string stays) | MA:160, verbatim | A |
| R5 | `components/partner/RevenueCalculator.tsx:75` (lead) and `components/partner/RevenueResults.tsx:48` (lead) | "Model the opportunity and forecast revenue across assessment, implementation and managed service." / "The financial picture of security services across your customer base: adjust the inputs, compare scenarios, export." | "Model an illustrative opportunity across assessment, implementation and managed service." / "The illustrative financial picture of security services across your customer base: adjust the inputs, compare scenarios, export." (new words) | MA:67-68, MA:256 | B |
| R6 | the customer report (PDF, `api/.../ReportModelBuilder.cs`; screen `components/screens/ReportScreen.tsx`): a new introduction | no introduction exists. The cover is "Security Assessment [em dash] Executive Report", section 1 opens with key figures | none proposed: the document names "customer report introductions" as an activity (MA:273) and lists emphasis for the surface (MA:192-195) but gives no sentence | MA:192-195, MA:273 | C |
| R7 | the report's section "Next Engagement" (`api/.../Report/ReportModel.cs:25`, `ReportScreen.tsx:139`) | section 8 of 9 | held for the phase document's ruling on whether it belongs in the customer report | MA:161; D-019 | C |
| R8 | `components/screens/RecommendationScreen.tsx:66` "No device is changed" and `api/.../Hpsm/HpsmOutputBuilder.cs:28` "Recommendation only -- no live device change." | as is | no change (already says what MA:139 and MA:244 ask) | MA:139, MA:244 | (no change, not counted) |

R8 is a checked row, not one of the 59.

## Surface 6: services, training, coach and the other partner pages

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| V1 | `components/partner/ServicesHub.tsx:24` (lead of "Delivery phases") | "From assessment to implementation to a managed service: each phase of a customer engagement." | "Assess, Implement, Optimize: each phase of a customer engagement, with the options a partner can choose at each." (new words; the page title "Delivery phases" stays, the product owner's 2026-11-11 ruling) | MA:84, MA:87, MA:127-138 | B |
| C-phase3 | `content/partner/partner-showcase.v0.1.0.json:55-63` and the client copy `content/client/partner-showcase.v0.1.0.json:55-63` (phase labels "Phase 1 - Assessment", "Phase 3 - Managed service"), and the page title "Phase 3 - Managed service" at `app/(app)/services/managed/page.tsx:4` | "Phase 3 - Managed service" | a rename to "Optimize" would drop managed service as the only third phase (MA:140-157 has three motions); held with D-056 | MA:84, MA:142-157 | C |
| C-modes | `content/client/partner-showcase.v0.1.0.json:121-134` (delivery models "Partner delivered", "Co-delivered", "Referral") | three delivery models | the document's three motions (product-led reseller, managed services partner, security services specialist, MA:142-157) are a switchable commercial mode, not a label swap; D-023 is next phase | MA:142-163 | C |
| C-training | `components/partner/TrainingScreen.tsx:12` (`TRAINING_STEPS`: "Discover and scope", "Assess and verify", "Advise and deliver") | three labels | the partner workflow Discover, Assess, Recommend, Engage (MA:106-121, MA:207) | MA:106-121, MA:207 | C |
| C-rename | the customer workspace's eight-step journey labels (`components/shell/customer-nav.ts`, `components/shell/CustomerShell.tsx`) and every "Discover / Assess / Recommend / Engage" use | Profile, Assessment, Score & findings, ... | held: the journey RENAME and any layout or workflow change | MA:99-121, MA:206-207; the product owner's 2026-11-10 ruling; D-064 | C |
| C-coach | `components/customer/ConversationCoach.tsx:174` and the coach content | "Practise customer conversations: messaging, objection handling and next steps." | the document's account-manager opener (MA:297) and talk track (MA:94) have no coach slot; D-069 is next phase | MA:297, MA:94 | C |
| C-gbb | Good / Better / Best as partner-selected packages (a page) | tiers appear only as groups of recommended settings | a packages page is new; D-027 is next phase. The wording rule is applied in R2 | MA:250 | C |
| C-stages | commercial stages identified, qualified, quoted, booked, recognised, as dashboard states (and the attribution preview, `components/screens/AttributionPreviewScreen.tsx`) | none; the preview is labelled next phase and sample | new records and states; D-024 to D-026 and D-043 are next phase. R4/H6 carry the language rule meanwhile | MA:159-163, MA:256 | C |
| C-metrics | the document's success metrics to instrument (MA:281-287) | none | instrumentation is new behaviour; D-059 is next phase | MA:281-287 | C |

## Surface 7: the Playbook module text (HP's deck) and assessment content

These are the deck's own words, byte-pinned by hash in three copies each (`content/packages/`, `content/client/`, `api/src/HpsmPoc.Api/SeedContent/`); `content/client/` is generated from `content/packages/` by `scripts/client-content.mjs`. A change is a new content version.

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| C-deck | `content/client/playbook-placeholder.v0.7.0.json` (117 case-insensitive hits for revenue, consult, HP-backed, automatic, recurring, trust; for example `:83`, `:92` "trusted advisor", `:110`, `:159`, `:315`) | the deck's marketing voice | no change: it is HP's deck, not the product's own positioning (D-058 keeps it) | MA:11; D-058 | C |
| K2 | `content/client/playbook-placeholder.v0.7.0.json:2108` and `:2129` | "The good news is that HP Security Manager deploys them automatically across the entire fleet. It's not a manual process for each device. For most customers, the deployment takes less than an hour..." (`:2108`); "Protect Devices [em dash] Firmware updated and HP Security Manager policy deployed for continuous compliance" (`:2129`) | hold: needs an HP Security Manager SME sentence on what is deployed, to which devices, with what prerequisites. The document gives the rule, not the sentence. Not changed in this pass | MA:62, MA:241-245, MA:64 ("Automatic remediation" under Avoid) | D |
| K3 | `content/client/playbook-placeholder.v0.7.0.json:4182` (question "Is your printers' firmware kept current through regular or automated updates?") and the 13 findings that say "Apply the HP Security Manager settings listed..." | as is | hold with D-004 and D-005 (this phase, needs HP SME wording) | MA:244 | D |

## Surface 8: the document's own landing page and off-site assets

| ID | Where | Today | Proposed | Source | Class |
|---|---|---|---|---|---|
| C-landing | "Primary partner landing page": headline "YOUR CUSTOMERS TRUST YOU WITH THEIR PRINT ENVIRONMENT. HELP THEM SECURE WHAT COMES NEXT.", the introduction, the six modules (Start with a conversation / Turn uncertainty into clarity / Connect findings to action / Help decision-makers act / Create opportunity your way / Stay valuable beyond the first project) and the closing copy | no landing, about or marketing page (56 `page.tsx` routes read under `web/src/app`; none is one; no `web/public` folder) | not built: a new page or a new Home block. The words are the document's and are ready to place once a location is chosen | MA:208-231 | C |

Not on the site, so not mapped: the EDM sequence, executive HP overview, seller talk track document, and Appendix A variants (MA:180-191, MA:290-303) are assets outside the web app; Option C (MA:297) is the coach row above.

## Checked, no change (positive findings, not counted)

- Narrative copy (`content/narrative-provenance.ts:37-48`: "a person reviews and approves it", "Template text, reviewed by a consultant"): already what MA:253 asks.
- Customer security preview (`components/security/*`): "Not connected", "Not scheduled", "self-reported and are not device verification" (`SecurityFrame.tsx:9`): already what MA:233 and MA:260 ask.
- Walkthrough draft-score caveat (`steps.ts:103`), representative-setting wording (`steps.ts:111`), illustrative bridge note (`steps.ts:191`), prototype banner (`PrototypeBanner.tsx:11`), footer "Prototype [middle dot] sample data only" (`app/layout.tsx:29`): keep.
- "Guided assessment" page title and lead (`AssessmentScreen.tsx:59`, `:85`): the word "guided" is the document's own; the "how we know it" line already covers MA:42.
- The report's methodology section (`ReportModelBuilder.cs:343-384`) already states sample data, representative guidance, and who reviewed the narrative.

## Conflicts

Order of precedence applied: the document (12 November, described as feedback on the messaging) beats the morning's revised copy (12 November, earlier the same day), which beats the earlier 09:15 copy. The product owner's rulings on the site (2026-11-09 to 2026-11-11) are older than both but pinned by tests; where the document is silent they stand.

| # | Topic | Morning revised copy | This document | Wins |
|---|---|---|---|---|
| 1 | Apple-style headline | "The trust you've earned. The security business you can build." | "The trust you've earned. The opportunity ahead." (MA:75) | document |
| 2 | Primary promise | "A simpler way to turn print security needs into customer confidence--and new service opportunities." | "A simpler way to sell, deliver and grow print security services with HP." (MA:78) | document |
| 3 | Paid services as the outcome | Summary: "a repeatable path from print security conversations to paid services"; main: "Turn assessments into paid discovery" | Not all partners charge; lead with several opportunity types (MA:48, MA:66) | document |
| 4 | Named settings | main: "Recommendations map findings to named HP Security Manager policy settings, including where to find them and what to set" (left unchanged by the review) | Avoid "every finding maps to an HP Security Manager setting" (MA:62); name settings only where supported for device, firmware and edition (MA:241). A standing test also forbids "named HP Security Manager policy setting" in the walkthrough | document |
| 5 | HP-backed | replaced by "grounded in HP Security Manager policy settings" and "HP-aligned" with CHECK markers | prefer "HP-aligned, product-validated recommendations" only after approval, or "recommendations mapped to applicable HP capabilities" (MA:46) | document: use the second form now; the first waits for approval |
| 6 | Good, Better, Best | "Good, Better, Best options for every finding" (CHECK marker) | partner-selected packages informed by risk and scope; no automatic requirement for paid consulting or hardware replacement (MA:250) | document |
| 7 | Closing call to action | "Start with one customer. Help them see the risk, choose a path forward, and trust you to guide the next step." | "Start with one customer. Build what comes next." (MA:90), with a named first action (MA:55) | document |
| 8 | Not becoming a cybersecurity firm | "without building a cybersecurity practice from scratch" | "not a requirement to become a cybersecurity company" (MA:26); "without having to become cybersecurity consultancies" (MA:96) | document |
| 9 | HP relationship or HP expertise | "Built on your HP relationship" (CHECK: flip to expertise if the audience is HP-certified partners) | "built around your HP expertise" (MA:98, MA:231) | document; HP brand and legal approval still pending (MA:11) |
| 10 | Managed services | "the managed services you build on them" (CHECK: only if the app supports managed services) | managed services partner is one of three valid motions (MA:29, MA:142-157); the app has a sample managed-service tracker only | document supports the wording; the site must still say "sample" (kept by the banner) |
| 11 | Trust repeated | trust appears in the headline, opener, closing and CTA | use it once, as the anchor (MA:39-40) | document |
| 12 | "service offers" vs "delivery phases" | the review changed "service offers" to "delivery phases" | the document's Engage stage lists "service offers" (MA:121, MA:202) | tie: the product owner's own 2026-11-11 ruling named "Delivery phases" and a test pins it; the document's term sits inside the held journey rename. Keep "Delivery phases" until he says 'rename too' |
| 13 | Revenue calculators | "revenue calculators" listed as visibility | separate lead and forecast values from booked and recognised revenue (MA:256); estimates are not contracted revenue (MA:160) | document (rows H6, R4, R5) |

Compatible, no conflict: "surface likely risks" and "clear customer conversation" (the review's edits) sit inside MA:42's rule; "Assess, Implement, Optimize" appears in both.

## Held (C/D) with the question each needs

One question per item; the default is what the builder does if he does not answer.

1. **Journey rename (C-rename, C-training).** Do you want the in-app journey renamed to Discover, Assess, Recommend, Engage now, with the layout and workflow it implies? Default: no, held with your 2026-11-10 ruling; he may say 'rename too'.
2. **Landing copy deck (C-landing, H-hero).** Where should the six-module landing copy live: a new block on Home, or a new page? Default: nowhere; Home gets only the promise, the CTA and the closing copy (H1-H4).
3. **Customer report introduction (R6).** Do you want to supply the introduction sentence, or approve one drafted from MA:192-195? Default: none; the report keeps its cover and methodology.
4. **Next engagement in the customer report (R7, D-019).** Does the section stay in the customer's report? Default: it stays.
5. **Three operating modes (C-modes, D-023) and the Optimize / managed-service naming (C-phase3).** Next phase as the phase document says? Default: yes, next phase; the wording rows (P3, P5, W12-W13) already stop presenting fees as the standard motion.
6. **Good / Better / Best packages page (C-gbb, D-027).** Next phase? Default: yes; R2 applies the wording rule to the existing tier sentence.
7. **Commercial stages and success metrics (C-stages, C-metrics).** Next phase? Default: yes; H6, R4 and R5 carry the language rule meanwhile.
8. **Coach opener (C-coach, D-069).** Add the account-manager opener to the coach now? Default: no; next phase.
9. **HP-backed (P4, W5-W10, W17; D).** Has HP approved "HP-aligned, product-validated recommendations"? Default: no; the qualified form ("mapped to applicable HP capabilities", "Applicable HP solutions") ships.
10. **Deck sentences (K2, K3).** Can an HP Security Manager SME supply the sentence on what the product deploys and to which devices? Default: unchanged; they ride with D-004 to D-006.
11. **Tools shown on Home (P6).** Does "SIEM integration if available" stay on a page HP sees? Default: it stays, with the "planned or subject to implementation" line.
12. **Home lead (H1).** Replace "Your overview of readiness, customers, actions and opportunities." with the promise? Default: yes.
13. **Assessment or snapshot (H2, H4).** The document's home CTA is "Start a customer assessment"; the product calls the same thing a "snapshot" in about 20 places. Rename the two buttons only? Default: two buttons only.

## For the builder

**Files to edit (origin main, sha above):**
- `web/src/components/screens/SignInScreen.tsx` (S1-S3)
- `web/src/app/layout.tsx` (M1)
- `web/src/components/partner/PartnerDashboard.tsx` (H1-H6)
- `web/src/components/home/phase-flow.ts` and `web/src/components/home/PhaseFlow.tsx` (P1-P6)
- `web/src/content/walkthrough/steps.ts` (W1-W19)
- `web/src/components/screens/RecommendationScreen.tsx`, `web/src/components/screens/NextEngagementScreen.tsx` (R1-R3)
- `web/src/components/shell/PrototypeBanner.tsx`, `web/src/components/partner/RevenueCalculator.tsx`, `web/src/components/partner/RevenueResults.tsx` (R4, R5)
- `web/src/components/partner/ServicesHub.tsx` (V1)
- `api/src/HpsmPoc.Modules.Reporting/Report/ReportModelBuilder.cs` (R2, the PDF's tier sentence)
- Nothing else. Do NOT edit `content/packages/`, `content/client/` or `api/.../SeedContent/` (hash-pinned; C/D rows). `content/client/partner-showcase*.json` is generated from `content/partner/` and is not touched by this pass.

**Tests that pin the current strings (found with `grep -F -i` over `web/src`, `web/e2e`, `api`, `scripts`, `infra`; each positive control fired, see Instruments):**

| Rows | Test file and line | What it pins | Action |
|---|---|---|---|
| H1-H4, P1-P5 | `web/src/components/partner/PartnerDashboard.text.test.tsx:25-66` and `:69-108` | the WHOLE Home page text in two states, written as "the product owner's ruled words" | rewrite both literals from the rendered page; the control sentence in the test names the ruled note, keep it |
| P1 | `web/src/components/partner/PartnerDashboard.layout.test.tsx:226` (region name), `:228`; `web/src/components/home/PhaseFlow.test.tsx:12`, `:55`, `:77`; `web/e2e/playbook-home-phase-flow.spec.ts:12` | the panel's accessible name "Three phases, one simple partner motion" | change all 5 to the new title; the greeting heading "Welcome back" (anchor at layout test `:228` and e2e `:40`) is not changed |
| P3 | `web/src/components/home/PhaseFlow.test.tsx:46-48` | the screen-reader label "(Datasec Consulting Services touchpoint)" on 11 activities | update the label |
| P4 | `web/src/components/home/PhaseFlow.test.tsx:15` (themes `toEqual`), `:84` (`data-placeholder-for`) | "HP-backed tools" | update both |
| P5 | `web/src/components/home/PhaseFlow.test.tsx:40` | reads `p.earns` from data and the label "Partner earns:" | label string changes; data follows |
| H5 | `web/src/components/partner/PartnerDashboard.tiles.test.tsx` (tile names, 4 hits for the section) | the "Where to next" tile names and links | check text of the Revenue tile only |
| S1-S3, M1 | none: no test pins the sign-in lead, side panel or meta description (positive control: the same test files do pin "HP Security Services Playbook") | none | none |
| W1 | `web/src/components/walkthrough/WalkthroughPanel.test.tsx:166`; `web/e2e/playbook-walkthrough.spec.ts:50` | cover headline | update both |
| W8 | `web/src/content/walkthrough/steps.test.ts:28` | the 14 step titles, `toEqual` | update the one title |
| W6, W10, W17 | `web/src/content/walkthrough/steps.test.ts` (claims block): the walkthrough text must not match /named HP Security Manager policy setting/ or /Each finding maps/, step 8 `say` must match /representative HP Security Manager policy setting/ and /where one is mapped/ | existing claim constraints | keep those phrases (the proposals do) |
| W14 | `steps.test.ts` revenue step: `say` and `cue` match /implementation \(including security software attach\)/, `key` matches /implementation, including software attach/ | existing | keep those phrases (the proposals do) |
| W7, W11, W16 | `steps.test.ts` instruction scan on every `cue` and `caveat` (no "score/approve/save/submit" followed by an object) | existing | the proposed words pass (they contain "approval", not "approve the"); run it |
| R1 | `web/src/components/screens/RecommendationScreen.tiers.test.tsx:66` | the exact lead | update |
| R2 | `RecommendationScreen.tiers.test.tsx:48`, `:49`; `web/e2e/playbook-content-050-live-api.spec.ts:94` (one regex spanning "set in the rules content, not chosen by AI. Groupings only: no prices or revenue. Grouping proposed for HP to vet."); `api/tests/HpsmPoc.Api.Tests/Assessment/Content050ApiTests.cs:81-82`; `api/tests/HpsmPoc.Modules.Reporting.Tests/Report/RecommendationTiersTests.cs:69`, `:70`, `:102` | the two sentences, as substrings | the proposal keeps both substrings intact, but the e2e regex spans both with no gap: inserting the new sentence BETWEEN them breaks it. Either insert after "Grouping proposed for HP to vet." or relax the regex |
| R3-R5, V1, M1 | none found | none | none |
| all | `web/src/productName.test.tsx` (scan "no old word in what the web's source renders") | any rendered string with a bare "Security Services Playbook" or capital-S "DataSec" | new copy uses "HP Security Services Playbook" and "Datasec"; run it |
| all | `infra/tests/test_hidden_characters.py` (scans every tracked file) and `web/e2e/playbook-invisible-characters.spec.ts` | hidden or text-direction characters | the document's text holds only U+2014, U+201C, U+201D, U+2019, U+2192 and U+2022 (counted: 19, 17, 17, 5, 12, 1; no U+00A0, U+200B or U+202E); paste from the .txt, not from Word |

**Visual and e2e checks:** no screenshot comparison exists (`toHaveScreenshot`, `toMatchSnapshot`: 0 files; the only .png files are four logo assets). The e2e files that load the changed pages and need a run are `playbook-home-phase-flow.spec.ts`, `playbook-walkthrough.spec.ts`, `walkthrough-uat.spec.ts`, `smoke.spec.ts`, `journey.ts`/`journey.spec.ts` (page titles and the sign-in screen), `a11y.spec.ts`, `responsive.spec.ts`, `html-layout.spec.ts` (the longer Home/phase-panel strings change heights at 320 px and 1440 px; the panel lines in P5 are three to six times longer than today's), and `playbook-content-050-live-api.spec.ts` (R2, needs the live API).

**Layout risk to look at in a browser:** P5b-P5d put 70-85 character sentences in a bold "Partner earns" box that holds 20-50 characters today; W18 does the same in the walkthrough's bridge strip (`WalkthroughPanel.tsx:257`). Wrapping is expected; check the three-card row at lg and the narrow panel.

**Standing HPSM lines for the kit:** This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. Every row above is a string change; none builds or shows an integration as done (P6 adds the "planned" line for the ones named).

## Instruments

- **Tree:** `gh api -X GET repos/datasecau/HPSM-POC/tarball/c717ba1a945191ffa31f13320c19967a6cf7f15a` under the project's own `GH_CONFIG_DIR`, extracted into `fleet/state/s271/dmsg/tree/`; every `file:line` was printed with `grep -nF` over that tree. Control: `gh api -X GET repos/datasecau/HPSM-POC/commits/main` returned `c717ba1a94` before and after the reading, and the local checkout's `git rev-parse HEAD` was `8869b1a9`, so it was stale and unused.
- **String search:** `/usr/bin/grep -rn -i -E` over `web/src` for `HP-backed|every finding|maps to|automatic|Datasec Consulting|consulting|discovery (fee|revenue)|recurring revenue`, tests excluded; positive control: the same scan counts 2 hits for "Three phases, one simple" in `phase-flow.ts` (it fires). Page and route census: `find web/src/app -name page.tsx` = 56; `find ... -iname '*about*' -o -iname '*landing*' -o -iname '*welcome*'` = 0 (control: the same `find` form returns the 56 for `page.tsx`).
- **Test pins:** `fleet/state/s271/dmsg/pins.sh` runs `grep -rF -i` for each current string over `web/src`, `web/e2e`, `api`, `scripts`, `infra`. Positive controls that fired: "Three phases, one simple partner motion" (6 files), "HP-backed tools" (4), "Start a customer snapshot" (2). Zeros read as absence (sign-in lead, side panel, meta description, R3-R5, V1) were each checked with a second grep on the same test files for a string that must be there ("HP Security Services Playbook" present in `SignInScreen.test.tsx`, `UatStartScreen.test.tsx`, `smoke.spec.ts`, `journey.ts`; "describe" count 2 in `SignInScreen.test.tsx`).
- **Activity census:** `phase-flow.ts` holds 13 activities, 11 with `touchpoint: true` (two `grep -c` counts on the file). The phase decision document says "11 of the 14"; the file reads 11 of 13 at this sha.
- **Document structure:** `python3 -I docx_paras.py` over the .docx (zipfile + ElementTree), output `docx_structure.txt` (164 lines); used to resolve the line breaks inside the awareness-copy and landing-page cells.
- **Character census:** `python3 -I` counted non-ASCII characters in the extracted text (U+2014 x19, U+201C x17, U+201D x17, U+2192 x12, U+2019 x5, U+2022 x1); control: the NBSP detector fired on a planted U+00A0.
- **Class counts:** printed with `awk -F'|'` over the table rows of this file, last cell trimmed, rows whose first cell matches the ID forms used here; result A 22, B 13, C 13, D 11, total 59. The two non-counted rows are R8 and the "no change" lists.
- **Not read:** the production or hosted site (no HTTP), Jira, the decision queue, any project outside HPSM-POC. Scratch: `fleet/state/s271/dmsg/` only.
