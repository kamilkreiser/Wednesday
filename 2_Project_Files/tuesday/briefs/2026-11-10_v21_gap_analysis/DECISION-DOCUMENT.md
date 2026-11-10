# HP Security Services Playbook: v2.1 HTML and alignment document, change by change

For the product owner and the deputy. Prepared 10 November 2026. Nothing in this document has been built, ticketed or changed.

## BLUF

There are **85 changes to decide**. The recommendation is **24 for this phase, 55 for the next phase, and 6 to drop** (keep the site as it is, because the site is already ahead or the item exists only because the HTML is an offline file).

| Recommendation | Small | Medium | Large | Total |
|---|---|---|---|---|
| THIS PHASE | 16 | 8 | 0 | 24 |
| NEXT PHASE | 18 | 21 | 16 | 55 |
| DROP (keep the site as it is) | 6 | 0 | 0 | 6 |
| Total | 40 | 29 | 16 | 85 |

Small = under a day. Medium = one to three days. Large = more than three days, or new stored data.

**How the recommendation was made.** This phase: corrections to what reviewers already see in the current UAT; items the alignment document marks P0 or P1 that fit the existing screens and records; and feedback the product owner has already given. Next phase: new pages, new stored records, new roles and the visual rebuild, in line with the product owner's ruling of 9 November that the layout changes are the first work of the next phase. The alignment document itself puts its P2 and P3 items behind an approved change request; 5 items carry that condition. 10 items cannot be finished without content from an HP SME, whichever phase they land in (marked "needs HP SME content"), and 11 more need wording or a content choice from the product owner.

**The five most important items**

1. **D-001 — Decide which 16-question set is the base.** Three different sets of 16 questions are in play. Nothing at question level can move until one is named. Recommendation: this phase.
2. **D-004 — Correct the firmware update question and its recommendations.** With D-005 and D-007: the firmware and trusted-startup wording a reseller has already challenged, and the automatic 30-day date. All P0. Recommendation: this phase.
3. **D-009 — Treat "Unsure" as something to verify, not as a failed control.** An "Unsure" answer is scored and reported as a failed control today. Recommendation: this phase.
4. **D-010 — Let the assessor record and change how each answer is known.** Every typed answer is recorded and printed as "stated by the customer" and cannot be changed. Rated Critical by the reseller reviewer; the record already has the field. Recommendation: this phase.
5. **D-024 — Opportunity register and pipeline (deals separate from assessments).** With D-025, D-026 and D-043: the commercial layer is the largest part of the HTML (deals, quotes, contracts, attribution, a new dashboard). The document rates it P2, which by its own rule needs a change request. Recommendation: next phase.

**Three things to know before starting**

- The HTML and the site ask different questions. The reseller reviewer's comments were about the site's questions, not the HTML's. The alignment document proposes a third list. See D-001.
- The alignment document describes a v2.2 demo that was not among the attachments. Several items rest on it. See D-082.
- Where the HTML and the site differ, the HTML is not always the better one. 6 items recommend keeping the site. Which sections of the HTML hold "the most accurate content" needs to be named. See D-081.

**How to use this document.** Each item has a BLUF, what the HTML shows against what the site does today, the part of the alignment document it serves, its size, its risk, a recommendation, and a decision line to fill in. The evidence (file and line) is in `GAP-LIST.md` under the G-numbers beside each item; the test scenarios are in `UAT-SCENARIOS.md`.

## Summary table

| ID | Change | Recommendation | Size | Document priority | Needs content from |
|---|---|---|---|---|---|
| D-001 | Decide which 16-question set is the base | THIS PHASE | S | P0 |  |
| D-002 | Put the fleet inventory question first and keep sign-in, roles and print release together | THIS PHASE | M | P1 |  |
| D-003 | Adopt the document's revised 16 topics (four added, three dropped, firmware questions reworded) | NEXT PHASE | L | P0 | HP SME |
| D-004 | Correct the firmware update question and its recommendations | THIS PHASE | S | P0 | HP SME |
| D-005 | Stop implying that HP Security Manager deploys firmware | THIS PHASE | S | P0 | HP SME |
| D-006 | Trusted startup: verify by model instead of "enable", and send unsupported devices to a lifecycle or exception review | THIS PHASE | M | P0 | HP SME |
| D-007 | Remove the automatic 30-day date | THIS PHASE | M | P0 | product owner |
| D-008 | Give each action a type and a lead responsibility | NEXT PHASE | M | none | HP SME |
| D-009 | Treat "Unsure" as something to verify, not as a failed control | THIS PHASE | M | P0 | product owner |
| D-010 | Let the assessor record and change how each answer is known | THIS PHASE | M | P0 |  |
| D-011 | Six answer states with coverage, compensating controls and residual risk | NEXT PHASE | L | P1 | HP SME |
| D-012 | Certificates question: capture ownership, renewal and expiry | NEXT PHASE | M | none | HP SME |
| D-013 | Replace "being finalised" on findings with real wording | THIS PHASE | M | none | HP SME |
| D-014 | Say plainly that HP Security Manager settings are unconfirmed for the customer's models | THIS PHASE | S | none |  |
| D-015 | Keep the site's weighted score (do not adopt the HTML's simple percentage) | DROP (keep the site as it is) | S | none |  |
| D-016 | Allow an approved narrative to be edited again, with a dated revision and re-approval | THIS PHASE | M | P0 |  |
| D-017 | Confirm that a changed answer or finding withdraws approval of the narrative and the report | THIS PHASE | S | P0 |  |
| D-018 | Add a contents page with links, and return-to-contents links, to the executive report | THIS PHASE | M | P1 |  |
| D-019 | Decide whether "Next engagement" belongs in the customer's security report | THIS PHASE | S | P0 |  |
| D-020 | Three report outputs: executive, technical remediation, internal commercial summary | NEXT PHASE | L | none |  |
| D-021 | Keep the report as a PDF (do not add the HTML's "review document" export) | DROP (keep the site as it is) | S | none |  |
| D-022 | Stop presenting consulting fees as the expected way to earn | THIS PHASE | S | P1 | product owner |
| D-023 | Three reseller operating modes that change the commercial pages but never the findings | NEXT PHASE | M | P1 | product owner |
| D-024 | Opportunity register and pipeline (deals separate from assessments) | NEXT PHASE | L | P2 |  |
| D-025 | Quote builder, contracts and renewals, sales dashboard | NEXT PHASE | L | P2 |  |
| D-026 | Revenue attribution by participant (replaces the attribution preview) | NEXT PHASE | L | P2 |  |
| D-027 | Good / Better / Best service packages page | NEXT PHASE | M | none | product owner |
| D-028 | Keep the site's revenue calculator (do not swap in the HTML's simpler one) | DROP (keep the site as it is) | S | none |  |
| D-029 | Connections to HP management tools | NEXT PHASE | L | P3 |  |
| D-030 | Product name: "HP Cyber Security Services Playbook" | NEXT PHASE | S | none | product owner |
| D-031 | White menu column with collapsible groups | THIS PHASE | S | none |  |
| D-032 | Menu column brand block, mode panel and footer | NEXT PHASE | S | none |  |
| D-033 | Top bar: location trail, product title, workspace switch, customer chooser and "+ New customer" | NEXT PHASE | M | none |  |
| D-034 | A real Customer sign-in, and a role chooser in the top bar | NEXT PHASE | L | P0 |  |
| D-035 | A breadcrumb on every page | NEXT PHASE | S | none |  |
| D-036 | Page heading style, colours and the HP signature card | NEXT PHASE | M | none |  |
| D-037 | One notice per page in the page's own words (replaces the single site-wide banner) | NEXT PHASE | M | none | product owner |
| D-038 | Partner menu: eight groups and 23 entries, with renamed entries | NEXT PHASE | L | none |  |
| D-039 | Who sees which menu entry | NEXT PHASE | M | none |  |
| D-040 | Customer menu: add "Framework alignment" and "My remediation actions" | NEXT PHASE | S | none |  |
| D-041 | Do not build the prototype-only tools | DROP (keep the site as it is) | S | none |  |
| D-042 | Hide the feedback button in the customer workspace | NEXT PHASE | S | none |  |
| D-043 | Rebuild the partner dashboard around the commercial pipeline | NEXT PHASE | L | P2 |  |
| D-044 | Dashboard and register: show assessment progress as "n of 16 answered" with the customer's owner | NEXT PHASE | M | none |  |
| D-045 | My readiness as one live page (statements, score and priorities together) | NEXT PHASE | M | none |  |
| D-046 | Take the customer snapshot launcher off the readiness page | NEXT PHASE | S | none |  |
| D-047 | Training page: descriptions, a six-part learning pathway and five assessment principles | NEXT PHASE | M | none | product owner |
| D-048 | Guided onboarding page | NEXT PHASE | S | none |  |
| D-049 | My action queue (tasks with owners, due dates and evidence-gated completion) | NEXT PHASE | L | none |  |
| D-050 | Engagement journey and handover checks | NEXT PHASE | L | none |  |
| D-051 | Activity history | NEXT PHASE | L | none |  |
| D-052 | Customer register: columns, stage chips, sorting | NEXT PHASE | M | none |  |
| D-053 | Assessment pipeline page: heading and two small additions | NEXT PHASE | S | none |  |
| D-054 | Action plan: tiles, an editable status and a source category | NEXT PHASE | M | none |  |
| D-055 | Delivery and assessments page | NEXT PHASE | M | none |  |
| D-056 | Delivery phases page: phase descriptions and an inline offer sheet | NEXT PHASE | M | none | product owner |
| D-057 | Resources and modules page: heading, counter and card style | NEXT PHASE | S | none |  |
| D-058 | Keep the site's Playbook module names and text | DROP (keep the site as it is) | S | none |  |
| D-059 | Automation metrics: add four summary tiles | NEXT PHASE | S | none |  |
| D-060 | Administration page: name, introduction and one extra line | NEXT PHASE | S | none |  |
| D-061 | Operational readiness and release gates page | NEXT PHASE | M | none |  |
| D-062 | Customer workspace: header, summary strip and overview tab | NEXT PHASE | M | none |  |
| D-063 | "Related commercial opportunities" on every customer tab | NEXT PHASE | M | none |  |
| D-064 | Journey rail: "Eight-step journey", numbered headings, Metrics set apart | NEXT PHASE | S | none |  |
| D-065 | Question screen: filter by group and a "Create follow-up draft" button | NEXT PHASE | S | none |  |
| D-066 | Action register: the agreed rule sentence | THIS PHASE | S | none |  |
| D-067 | Finding detail: replace "Not written yet" with the honest caveat | THIS PHASE | S | none |  |
| D-068 | Firmware risk task: use the HTML's checklist and guidance | THIS PHASE | S | none |  |
| D-069 | Conversation coach: add the HTML's five talk tracks | NEXT PHASE | S | none | product owner |
| D-070 | Keep the site's findings review, next engagement and metrics steps | DROP (keep the site as it is) | S | none |  |
| D-071 | Customer pages: a section line per page and the HTML's caveat | NEXT PHASE | S | none |  |
| D-072 | Customer dashboard: answer signal, coverage, unknowns, domains and confidence | NEXT PHASE | M | none |  |
| D-073 | Fleet page: heading and a scope-limitations panel | NEXT PHASE | S | none |  |
| D-074 | Customer assessments page: every question, its answer and its review status | NEXT PHASE | L | none |  |
| D-075 | Customer findings: answer, source question, framework relevance and evidence to verify | NEXT PHASE | L | none | HP SME |
| D-076 | Framework alignment page (ISO/IEC 27001 and NIST themes per question) | NEXT PHASE | L | none | HP SME |
| D-077 | Customer roadmap: counts, owner and status lines, closure note | NEXT PHASE | S | none |  |
| D-078 | Customer reports page: three-step evidence status and a distribution note | NEXT PHASE | S | none |  |
| D-079 | Continuous assurance page: open evidence requests, an assurance cycle and next steps | NEXT PHASE | M | none | product owner |
| D-080 | "My remediation actions": actions shared with the customer | NEXT PHASE | M | none |  |
| D-081 | Ask which sections of the HTML hold "the most accurate content" | THIS PHASE | S | none |  |
| D-082 | Ask for the v2.2 demo that the alignment document describes | THIS PHASE | S | none |  |
| D-083 | Adopt the document's 20 scenarios as the acceptance test for this phase's items | THIS PHASE | S | none |  |
| D-084 | Decide what the v2.1 UAT pack is for | THIS PHASE | S | none |  |
| D-085 | Record the seven sign-off gates and who holds each | THIS PHASE | S | none |  |

---

## A. Assessment content and accuracy (15 items)

### D-001 — Decide which 16-question set is the base

**BLUF.** There are three different 16-question sets in play, and they must not be mixed. Until one is named as the base, every question-level change below is blocked.

**HTML against the site today.** The HTML asks its own 16 questions (first: "Are printer administration functions restricted to authorised administrators only?"). The site asks a different 16 (first: "Can your printers check that their firmware is trusted when they start up, and block code that is not authorised?"), taken from the Playbook deck and aligned to the Datasec policy tool. The alignment document lists a third, revised set of 16 control topics (first: "Complete printer/MFP inventory and ownership") and says of the HTML: "The source v2.1 demo uses a different question bank from the version [the reseller reviewer] reviewed." The reseller reviewer's comments (question 1 trusted startup, 2 firmware updates, 9 inventory, 11 and 12 sign-in and roles, 13 certificates) match the site's on-screen order exactly, so the review was of the site's set.

**Alignment document.** Section 3 (revised sequence), P0 "Assessment schema and data provenance"

**Size and what it touches.** Small · question set (decision only)

**Risk or dependency.** Needs the product owner's decision. The revised list in the document gives topics only, not question wording; the v2.2 demo that holds the wording was not among the attachments.

**Recommendation: THIS PHASE.** A decision, not a build; it unblocks six other items and costs nothing.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-001, G-002

### D-002 — Put the fleet inventory question first and keep sign-in, roles and print release together

**BLUF.** A reviewer starts with "what do you have?" before "how is it secured?". Today the inventory question is ninth and the sign-in, role and release questions are split across two groups.

**HTML against the site today.** The alignment document's order starts with fleet inventory, then platform integrity, then document and identity security (release, sign-in, roles, administration). The site shows inventory as question 9 of 16, held print release as question 5 and sign-in and roles as questions 11 and 12. The HTML itself does not do this (its question 1 is administrator access and it has no inventory question).

**Alignment document.** Section 2 ("Move inventory to first question"; "keep near secure release"), section 3, P1 "UX, report navigation and sequencing"

**Size and what it touches.** Medium · question set

**Risk or dependency.** Re-ordering the existing questions needs no new security wording. It must ship as a new content version so that assessments already recorded keep the order and numbers they were answered under (the same method used for the readiness statements on 9 November). On-screen numbers change, so every earlier comment that cites a question number refers to the old order.

**Recommendation: THIS PHASE.** Named "Adopt" in the document, no new content needed, and reviewers in the current UAT see the order on every run.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-003

### D-003 — Adopt the document's revised 16 topics (four added, three dropped, firmware questions reworded)

**BLUF.** The revised set changes what is asked, not only the order. It adds default credentials, network segmentation, protocol hardening and security event review, and no longer asks about encrypted storage, secure erase or data-protection risk.

**HTML against the site today.** The alignment document lists 16 control topics in four domains. Compared with the site: 9 topics exist today (some reworded), 4 are new and exist as questions in the HTML ("Are default credentials and unused accounts removed or disabled?", "Are printers located on approved network segments with restricted inbound connectivity?", "Are insecure or unnecessary printer network protocols disabled where not required?", "Are security events and device alerts reviewed by a responsible operations team?"), and 3 site questions have no place in the revised list.

**Alignment document.** Section 3, P0 "Assessment schema and data provenance"; appendix gate "Assessment/question logic"

**Size and what it touches.** Large · question set, data model

**Risk or dependency.** Needs HP SME content: final wording, weights, findings, recommended settings and timeframes for all 16, none of which the document supplies. The document calls reassigning question numbers "a material data-integrity risk"; the site already protects against it (each assessment is stamped with the exact question set it was answered under), provided the new set gets new question identifiers rather than reusing the old ones.

**Recommendation: NEXT PHASE.** Large, and blocked on wording and scoring that only the content owner and HP can approve; the reorder item delivers the visible part now.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-004, G-005

### D-004 — Correct the firmware update question and its recommendations

**BLUF.** The site asks whether firmware is kept current "through regular or automated updates" and recommends switching remote firmware upgrade on. The document says this must change to an approved, risk-based, tested update process.

**HTML against the site today.** Site, question 2: "Is your printers' firmware kept current through regular or automated updates?" with recommended settings such as "Remote Firmware Upgrade (RFU) = Enable with signatures verified". HTML: "Is fleet firmware inventoried and maintained against a defined update standard?" with the action "Inventory firmware and establish a documented, tested update schedule." Document: "Replace 'automatic updates required' with approved risk-based firmware governance".

**Alignment document.** Section 2 (question 2, "Must change"), section 4 guardrails, P0 "Firmware and hardware recommendation correction"

**Size and what it touches.** Small · question set

**Risk or dependency.** Needs HP SME content for the final wording (the document asks for HP sign-off on these mappings). The HTML's wording is available as a starting draft. Ships as a new content version.

**Recommendation: THIS PHASE.** P0 in the document and a factual accuracy point a reseller has already challenged.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-006

### D-005 — Stop implying that HP Security Manager deploys firmware

**BLUF.** Every finding on the site carries the same action: apply the HP Security Manager settings listed. For firmware findings that reads as if HP Security Manager installs firmware, which the document says it does not.

**HTML against the site today.** Site, every finding: "Apply the HP Security Manager settings listed for this finding (the Datasec baseline). The detailed action wording is being finalised." Document: HP Security Manager "should not be described as a firmware deployment engine"; HP Web Jetadmin and eligible WXP Print Management can deploy firmware. HTML marks its mappings as unconfirmed: "HP Security Manager — firmware assessment (mapping pending)".

**Alignment document.** Section 4 guardrails, P0 gate "No HPSM firmware deployment claims"

**Size and what it touches.** Small · question set

**Risk or dependency.** Needs HP SME content for the replacement action wording per finding. Ships with the firmware wording item.

**Recommendation: THIS PHASE.** P0 in the document; one sentence repeated on all 16 findings is the cheapest high-value correction.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-007

### D-006 — Trusted startup: verify by model instead of "enable", and send unsupported devices to a lifecycle or exception review

**BLUF.** A mixed fleet cannot simply switch trusted startup on. The site recommends "Enable" and gives a 30-day timeframe; the document asks for model-level checking and a lifecycle or exception path for devices that cannot support it.

**HTML against the site today.** Site, question 1 recommendations: "Secure Boot Presence = Enable", "Whitelisting Presence = Enable", "Intrusion Detection Presence = Enable", timeframe 30 days. Document: these protections "depend on eligible hardware/firmware and can operate by design without a configuration switch; use model-level verification". HTML: "Are secure boot or firmware integrity checks enabled and monitored where supported?" with the action "Validate supported firmware integrity protections and review compliance exceptions."

**Alignment document.** Section 2 (question 1, "Must change"), section 4 guardrails, P0

**Size and what it touches.** Medium · question set

**Risk or dependency.** Needs HP SME content (the document names an HP print hardware SME gate for model eligibility). Showing per-device coverage properly depends on the six-state answer item.

**Recommendation: THIS PHASE.** P0 in the document; the wording part can ship with the firmware corrections even if per-device coverage waits.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-008

### D-007 — Remove the automatic 30-day date

**BLUF.** Today every high-severity finding is given a 30-day timeframe by rule, including ones that mean replacing hardware. The document calls a default 30-day hardware action unacceptable.

**HTML against the site today.** Site rule: high severity gives "30-day", medium gives "60-90-day"; the other two columns of the roadmap are never used by the live question set. HTML: each question carries its own timeframe ("Immediate", "30-day", "60–90-day", "Ongoing") and the roadmap says "timings are indicative priority buckets, not a committed project plan". Document: "do not assign a default 30-day date"; target dates come from action type, risk, feasibility, dependency and customer agreement.

**Alignment document.** Section 2 ("30-day hardware remediation: Critical"), section 4, P0 gate "no arbitrary 30-day hardware action"

**Size and what it touches.** Medium · question set, report

**Risk or dependency.** The interim fix (label the columns as proposed priorities and take hardware-dependent findings out of the 30-day column) needs the content owner to say which findings are hardware-dependent. The full fix depends on the action-types item.

**Recommendation: THIS PHASE.** Marked Critical in the document; the label change is small and removes a statement the reseller reviewer rejected.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-009

### D-008 — Give each action a type and a lead responsibility

**BLUF.** Fixing a setting, updating firmware, renewing a certificate and replacing a device are different jobs for different people. The site shows one undifferentiated action per finding.

**HTML against the site today.** Document: seven action classes (evidence verification, firmware deployment, HPSM configuration, certificate lifecycle, document and identity, hardware lifecycle, governance), each with how the Playbook should respond and who leads. Neither the HTML nor the site has this; both show one action line per finding in four time columns.

**Alignment document.** Section 4 (action class table), executive decision 3, section 7 ("Findings and remediation categorisation")

**Size and what it touches.** Medium · data model, question set, report

**Risk or dependency.** Needs HP SME content: the class for each finding. Not in the HTML at all (it is a v2.2 item), so there is no layout to copy.

**Recommendation: NEXT PHASE.** New structure in the rules, the roadmap and the report, and it needs validated content first.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-010

### D-009 — Treat "Unsure" as something to verify, not as a failed control

**BLUF.** On the site an "Unsure" answer scores zero and raises the same high-severity finding and the same fix as a "No". The document and the HTML both say an unknown is a verification task, not a confirmed gap.

**HTML against the site today.** Site: one rule fires for both No and Unsure, with one title (for example "Regular firmware updates not confirmed") and the action to apply settings. HTML: findings from Unsure show "Requires review"; the customer view shows "Unknown responses — Unsure + unanswered; not scored as failed" and "Verification required"; the score is "Yes ÷ definitive Yes/No answers". Document: "Unverified: insufficient evidence; create verification task, not a confirmed control failure."

**Alignment document.** Section 3 (answer model), P0 gate "unknown ≠ failed rule verified"

**Size and what it touches.** Medium · question set, data model, report

**Risk or dependency.** Changes scores: existing scored assessments keep theirs (they are stamped), new ones would score differently, so before-and-after figures are not comparable. Needs the content owner to approve the verification wording.

**Recommendation: THIS PHASE.** P0 in the document, and it is the difference between an honest report and an overstated one.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-011

### D-010 — Let the assessor record and change how each answer is known

**BLUF.** Every answer typed into the live assessment is stored as "stated by the customer" and the report prints that. The assessor cannot change it to checked evidence. The reseller reviewer rated this Critical.

**HTML against the site today.** Site: the live question screen has the answer and a note only; the source is fixed, and the report states each answer as "stated by the customer". (The site's older scripted sample customer does offer five choices: verified, observed, asserted, assumed, not assessed.) Document: "No uneditable 'customer stated' assertions; preserve author, source and verification status"; "A self-declared 'Yes' must not be described as independently verified." HTML: a note per question only; it words the limit well ("A Yes answer indicates an assertion by the assessor or customer, not evidence of implementation").

**Alignment document.** Section 2 ("Customer-statement provenance: Critical"), section 3 (evidence fields), P0

**Size and what it touches.** Medium · screen, data model (the field already exists)

**Risk or dependency.** The record already stores the source for each answer and the scripted sample already has the control, so this is mostly a screen change on the live question card. It changes what the report says, so report wording should be checked at the same time.

**Recommendation: THIS PHASE.** Critical in the document, and most of the plumbing is already there.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-012, G-013

### D-011 — Six answer states with coverage, compensating controls and residual risk

**BLUF.** Yes, No and Unsure cannot describe a mixed fleet or a control met another way. The document asks for six states and the fields that go with them.

**HTML against the site today.** Document: Implemented, Partial, Not implemented, Compensating, Unsupported, Unverified; plus fleet coverage, device capability, compensating-control rationale, risk owner, approver, expiry and residual risk. HTML and the live site: Yes / No / Unsure. (The site's scripted sample customer has Yes / Partly / No / Not applicable.)

**Alignment document.** Section 3 (answer and evidence model), sections 2 and 8, P1 "Multi-state questions and exceptions"

**Size and what it touches.** Large · data model, question set, report

**Risk or dependency.** Needs HP SME content and an approved severity model (how each state scores). Changes the scoring engine, the rules format, every results screen and the report. Not in the HTML (a v2.2 item).

**Recommendation: NEXT PHASE.** The largest single change in the document; it should follow the question-set decision and approved scoring, not run alongside the current UAT.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-014

### D-012 — Certificates question: capture ownership, renewal and expiry

**BLUF.** Whether certificates are managed "from a central tool" does not tell a customer who owns them or when they lapse.

**HTML against the site today.** Site, question 13: "Are printer device certificates managed across the fleet from a central tool?" with settings such as "Use CA-signed 2048+ bit, auto-renew annually". Document: capture certificate ownership, deployment, renewal and lifecycle, and confirm that certificate management is in the licensed edition before proposing it. The HTML has no certificate question.

**Alignment document.** Section 2 (question 13, "Must change"), section 4 guardrails (WXP edition)

**Size and what it touches.** Medium · question set, data model

**Risk or dependency.** Needs HP SME content (the document names a WXP product and licensing gate). The extra captured fields arrive with the six-state item.

**Recommendation: NEXT PHASE.** Depends on licensing facts HP must confirm and on the new answer fields.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-015

### D-013 — Replace "being finalised" on findings with real wording

**BLUF.** Every finding on the site says its explanation and its action are "being finalised". The HTML has a specific finding title and action for each of its questions.

**HTML against the site today.** Site: "The answer did not confirm this. The explanation of why it matters for this customer is being finalised." HTML example: finding "Firmware update controls not confirmed", action "Inventory firmware and establish a documented, tested update schedule."; finding "Printer network isolation not verified", action "Validate VLAN placement, firewall policy and required outbound connectivity."

**Alignment document.** Section 4 (technically accurate remediation); executive recommendation

**Size and what it touches.** Medium · question set, report

**Risk or dependency.** Needs HP SME content. The HTML's wording belongs to the HTML's own questions, so only the overlapping topics can be reused as drafts; the rest must be written. The product owner's ruling of 10 November already has drafts prepared for his review.

**Recommendation: THIS PHASE.** It is the most visible content gap in the current UAT and the drafting is already under way.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-016

### D-014 — Say plainly that HP Security Manager settings are unconfirmed for the customer's models

**BLUF.** The site lists 54 exact settings (for example a 12-character password rotated every 90 days). The document says such features need model, edition and version confirmation.

**HTML against the site today.** Site: exact recommended values in Good, Better and Best groups, marked draft. HTML: each mapping is hedged in place ("mapping pending", "verify with HP", "outside HPSM") and the page says "HP must vet control terminology, support by model and settings before customer use." Document control note: "require model-, edition- and version-specific confirmation".

**Alignment document.** Document control note, section 4 guardrails

**Size and what it touches.** Small · screen, report

**Risk or dependency.** Wording only; the sentence exists in the HTML, so nothing is invented.

**Recommendation: THIS PHASE.** Small, and it protects the reseller from presenting unverified settings as HP guidance.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-017

### D-015 — Keep the site's weighted score (do not adopt the HTML's simple percentage)

**BLUF.** The HTML scores by a plain percentage of Yes answers. The site uses weights and shows a current and a target score. The site is the more complete of the two.

**HTML against the site today.** HTML: "Illustrative calculation: score = percentage of recorded answers that are 'Yes'"; green from 75, amber from 45. Site: weighted by question, target score after the first actions, green from 70, amber from 40.

**Alignment document.** Not in the document

**Size and what it touches.** Small · question set

**Risk or dependency.** None if kept. Adopting the HTML's formula would discard the weighting work already vetted in draft.

**Recommendation: DROP (keep the site as it is).** The site is ahead here; nothing in the document asks for the simpler formula.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-018, G-019


---

## B. Narrative and report (6 items)

### D-016 — Allow an approved narrative to be edited again, with a dated revision and re-approval

**BLUF.** Once a narrative is approved on the site it cannot be edited again unless a finding changes. The document asks for edit, regenerate and re-approve at any time, each leaving a revision record.

**HTML against the site today.** Site: edit and approve happen in one step with a mandatory audit note; after approval the only route to a new version is when findings change. HTML: "Regenerate from reviewed findings" and "Approve summary" only. Document: "Allow narrative draft/edit/regenerate/reapprove with an immutable production audit trail"; "Editing narrative prose must not change answer state, severity, evidence, product eligibility or the underlying score."

**Alignment document.** Section 2 ("Approved narrative edits: Must change"), section 5, P0 "Narrative/report approval state"

**Size and what it touches.** Medium · screen, data model

**Risk or dependency.** The site already keeps the original text, the edited text, who reviewed and why; what is missing is a second and later revision. An issued report must stay as issued, so a re-edit has to produce a new report version.

**Recommendation: THIS PHASE.** P0 in the document and a direct reseller request; it builds on what exists.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-020

### D-017 — Confirm that a changed answer or finding withdraws approval of the narrative and the report

**BLUF.** If the facts change, the approved words must not go out unchanged. The site already does most of this; the gap is proof and one missing path.

**HTML against the site today.** Site: answers lock when scored; when a finding is changed afterwards the narrative shows "The findings changed since this was approved: generate again" and the report falls back to standard wording. There is no way to reopen a scored assessment; a new one must be started. Document: "On any changed question, evidence or reviewed finding, invalidate dependent narrative approval and report-release state"; reopening "must create a new report version, not silently overwrite an issued copy".

**Alignment document.** Section 5, P0 gate "Edits invalidate approval"

**Size and what it touches.** Small · report

**Risk or dependency.** Mostly a test and a written statement of the rule. If the product owner wants a true reopen, that is a larger change.

**Recommendation: THIS PHASE.** Cheap to prove, and it closes a P0 gate.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-021

### D-018 — Add a contents page with links, and return-to-contents links, to the executive report

**BLUF.** A reader of the report cannot jump from a contents list to a section and back. The reseller reviewer asked for this.

**HTML against the site today.** Site: the report has nine sections and a bookmarks pane, but no contents page in the body and no return links. HTML: a single scrolling page with no contents list. Document: "Clickable sections, bookmarks/links and return-to-contents in HTML/PDF where supported."

**Alignment document.** Section 2 ("Executive report navigation: Adopt"), P1 "UX, report navigation and sequencing"

**Size and what it touches.** Medium · report

**Risk or dependency.** Report layout only; no content change. Needs print and screen-reader checks.

**Recommendation: THIS PHASE.** Named "Adopt" in the document and self-contained.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-022

### D-019 — Decide whether "Next engagement" belongs in the customer's security report

**BLUF.** The document says commercial material is never in the security report by default. The site's report ends with a recommended next paid engagement.

**HTML against the site today.** Site: section 8 of 9 in the executive report is "Next engagement — the recommended follow-on" (no price is shown). HTML: the customer report "excludes internal partner pricing and sales notes". Document: the commercial opportunity summary is internal and "Never included in security report by default".

**Alignment document.** Section 5 (report outputs), P0 gate "customer report excludes commercial data"

**Size and what it touches.** Small · report

**Risk or dependency.** A decision first. No price, margin or deal note appears in the report today, so the stricter test in the document already passes; the question is only this one section.

**Recommendation: THIS PHASE.** A P0 gate that may already be met; it needs a ruling rather than work.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-023

### D-020 — Three report outputs: executive, technical remediation, internal commercial summary

**BLUF.** Engineers need more than executives; sales need a separate internal view. The site has one report with selectable sections.

**HTML against the site today.** Document: an executive customer report, a technical remediation report (per-control evidence, affected devices, change dependencies, owner, verification) and an internal commercial opportunity summary. Site: five document types cut from the same nine sections. HTML: the same five types.

**Alignment document.** Section 5 (report outputs table)

**Size and what it touches.** Large · report, commercial

**Risk or dependency.** The technical report needs affected-device and action-type data that do not exist yet. The commercial summary depends on the opportunity register, which the document places behind a change request.

**Recommendation: NEXT PHASE.** Depends on three other next-phase items.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-024

### D-021 — Keep the report as a PDF (do not add the HTML's "review document" export)

**BLUF.** The HTML exports its report as a web page for review. The site issues a fixed PDF with a checksum, which is the stronger record.

**HTML against the site today.** HTML: "Generate review document (HTML)", "Export HTML report", "Print / save as PDF". Site: a generated PDF, stored and verified on download.

**Alignment document.** Section 7 ("HTML review export; browser print to PDF" is the demo's stand-in)

**Size and what it touches.** Small · report

**Risk or dependency.** None if kept.

**Recommendation: DROP (keep the site as it is).** The site is ahead; the HTML export is a prototype convenience.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-025


---

## C. Commercial model (8 items)

### D-022 — Stop presenting consulting fees as the expected way to earn

**BLUF.** The reseller reviewer does not charge for assessments. The site's home page, service pages and guided demo present discovery fees and "Datasec Consulting Services" touchpoints as the standard motion.

**HTML against the site today.** Site home: each activity is tagged "(Datasec Consulting Services touchpoint)" and the phases read "Partner earns: discovery revenue + roadmap ownership"; the guided demo says "Discovery fees → implementation and attach → reviews and managed services." Document: "Default product-led reseller motion; optional managed services and specialist tiers"; an operating model "that does not presume chargeable consulting".

**Alignment document.** Section 2 ("No consulting fees: Commercial principle"), section 6, P1 "Commercial mode configuration"

**Size and what it touches.** Small · screen, commercial

**Risk or dependency.** Wording change only, but the replacement wording is a commercial position that the product owner should supply or approve. The home page's phase panel was the product owner's own earlier request.

**Recommendation: THIS PHASE.** P1 in the document and the reseller's central objection; small if limited to wording.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-026, G-027

### D-023 — Three reseller operating modes that change the commercial pages but never the findings

**BLUF.** A product-led reseller, a managed-services partner and a security specialist sell differently. The document asks for a setting that switches the commercial experience while the technical findings stay identical.

**HTML against the site today.** Document: mode A product-led (no-fee review), B managed services, C security specialist. Not in the HTML (a v2.2 item). The site has one fixed commercial presentation.

**Alignment document.** Section 6, executive decision 5, P1 "Commercial mode configuration"

**Size and what it touches.** Medium · commercial, data model

**Risk or dependency.** Needs the product owner to define each mode's wording and which pages change. Production use needs it set per partner by an authorised person.

**Recommendation: NEXT PHASE.** The wording item removes the objection now; a switchable mode is new behaviour across several pages.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-028

### D-024 — Opportunity register and pipeline (deals separate from assessments)

**BLUF.** The HTML adds a full deal record beside each customer: stage, value, owner, next action. The site has no deal concept at all.

**HTML against the site today.** HTML: "Commercial opportunity pipeline — Manage multiple deals per customer with separate commercial stages, owners, expected close dates and next actions"; an opportunity workspace with tabs Overview, Quote & margin, Contributors, Delivery; "Related commercial opportunities" on every customer tab. The HTML's stages are Lead to Won or Lost; the document's are identified, qualified, quoted, booked, recognised.

**Alignment document.** Section 6, section 7 ("Opportunity register"), P2 "Device mapping / quote and renewal logic"

**Size and what it touches.** Large · commercial, data model

**Risk or dependency.** A change request under the document's own rule for P2. New records, new permissions, and a hard rule that none of it reaches a customer view. The two stage lists disagree and one must be chosen.

**Recommendation: NEXT PHASE.** P2 in the document: outside the agreed commitments without an approved change request.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-029

### D-025 — Quote builder, contracts and renewals, sales dashboard

**BLUF.** These pages price a deal, track what is signed and report the pipeline. All depend on the opportunity register.

**HTML against the site today.** HTML: "Proposal & quote builder" (line items with sell and cost, gross margin, draft proposal export), "Contracts & renewals", "Commercial performance dashboard" with the rule "booked, ARR and recognised amounts must not be summed together." Site: none.

**Alignment document.** Section 6, P2

**Size and what it touches.** Large · commercial, data model

**Risk or dependency.** A change request (P2). Needs approved price books before any figure is more than an example; cost and margin need their own access rules.

**Recommendation: NEXT PHASE.** P2 in the document, and it cannot start before the opportunity register.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-030, G-031, G-032

### D-026 — Revenue attribution by participant (replaces the attribution preview)

**BLUF.** The HTML records who sourced, influenced, sold and delivered each deal, and is explicit that this is not commission.

**HTML against the site today.** HTML: "Opportunity attribution centre" with "Attribution ≠ commission. Participants document involvement only". Site: "Attribution (Preview)", sample figures by month, partner and engagement, marked as next-phase.

**Alignment document.** Section 6 ("separate ... internal sales attribution"), P2

**Size and what it touches.** Large · commercial, data model

**Risk or dependency.** A change request (P2). The product owner must say whether the new page replaces the current preview or both stay.

**Recommendation: NEXT PHASE.** P2 in the document; the site's own page already says next phase.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-033

### D-027 — Good / Better / Best service packages page

**BLUF.** The HTML brings back a page describing three service tiers and a scoped handoff for a chosen customer. An earlier ruling removed this entry from the site's menu.

**HTML against the site today.** HTML: "01 / GOOD Security Essentials", "02 / BETTER Managed Fleet Security", "03 / BEST Continuous Security Governance", each with inclusions and a "Commercial motion"; a note "Do not automatically present product licensing as a required fix for a security control." Site: Good, Better and Best appear only as groups of recommended settings.

**Alignment document.** Section 6 (operating modes); not a named priority

**Size and what it touches.** Medium · commercial

**Risk or dependency.** Reverses an earlier ruling. The tier descriptions are proposed packages ("not approved HP service offers or prices") and need the product owner's approval as content.

**Recommendation: NEXT PHASE.** Commercial content awaiting approval, and it overlaps the operating-modes decision.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-034

### D-028 — Keep the site's revenue calculator (do not swap in the HTML's simpler one)

**BLUF.** The HTML's calculator has five inputs on one page. The site's has more inputs, saved scenarios and a comparison, and was already accepted.

**HTML against the site today.** HTML: "Revenue opportunity model" with customer base, conversion, three sample fees and a horizon. Site: a five-step calculator and a results page with scenarios and export.

**Alignment document.** Not in the document (section 6 warns that estimates are not booked revenue)

**Size and what it touches.** Small · commercial

**Risk or dependency.** None if kept. The HTML's page title and its "Sample scratchpad only" notice could be adopted as wording.

**Recommendation: DROP (keep the site as it is).** The site is ahead; only the wording is worth taking, and that is cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-035

### D-029 — Connections to HP management tools

**BLUF.** Neither the HTML nor the document's demo connects to any HP tool. The document places integrations last and behind a change request.

**HTML against the site today.** HTML: "No live HP, CRM, customer tenant or finance connection." Document: "HP integrations / AI / live fleet evidence: NOT connected"; P3 "HP management tool integrations". Site: an import of HP Security Manager results as observed evidence is designed and partly built on the server.

**Alignment document.** Section 7, P3

**Size and what it touches.** Large · data model

**Risk or dependency.** A change request (P3). Needs HP interface approval and tenant permissions.

**Recommendation: NEXT PHASE.** P3 in the document.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-036


---

## D. Page frame, menu and roles (13 items)

### D-030 — Product name: "HP Cyber Security Services Playbook"

**BLUF.** The HTML and both UAT documents use a new product name. The site still says "HP Security Services Playbook".

**HTML against the site today.** HTML title bar, page title and menu footer: "HP Cyber Security Services Playbook". Site: "HP Security Services Playbook" on the sign-in page, the browser tab and the Playbook page (the logo's hidden description already uses the longer name).

**Alignment document.** Not in the document (its own title uses "HP Security Services Playbook")

**Size and what it touches.** Small · screen

**Risk or dependency.** The two sources disagree, so the product owner must confirm the name. The report and the UAT user guide carry the name too.

**Recommendation: NEXT PHASE.** A naming decision with knock-on effects on the report and the guide; better made once, at the start of the next phase.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-037

### D-031 — White menu column with collapsible groups

**BLUF.** The HTML's menu is white and each group can be folded away. These are two of the product owner's own open UAT feedback items.

**HTML against the site today.** HTML: each group heading is a button with a small arrow; the state is remembered. Site: fixed group headings on a coloured column; the whole menu can shrink to icons.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** None beyond the usual keyboard and screen-reader checks.

**Recommendation: THIS PHASE.** Already asked for by the product owner in UAT feedback, small, and no data involved.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-038, G-039

### D-032 — Menu column brand block, mode panel and footer

**BLUF.** The HTML puts the brand at the top of the menu, a panel naming the workspace, and a footer with a version line.

**HTML against the site today.** HTML: brand mark with "Cyber Security Services"; "PARTNER ENABLEMENT — Readiness, delivery & revenue" or "CUSTOMER SECURITY — Posture, evidence & remediation"; footer "Local demonstration — Sample content and draft rules. Nothing is sent to customers, HP or a CRM." Site: the logo sits in the page header; no footer.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** The footer's "nothing is sent" sentence is untrue for the site (feedback is stored on a server), so it needs rewording.

**Recommendation: NEXT PHASE.** Layout; part of the frame rebuild.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-040, G-041

### D-033 — Top bar: location trail, product title, workspace switch, customer chooser and "+ New customer"

**BLUF.** The HTML moves the Partner / Customer switch and the customer chooser into a top bar shown on every page.

**HTML against the site today.** HTML top bar: "HP CYBER SECURITY SERVICES / PARTNER / OVERVIEW", the product title, a Partner | Customer switch, a customer list and "+ New customer" (asking for organisation, industry, owner, printers and sites). Site: the switch is at the foot of the menu; adding a customer is on the Customers page and asks for name and industry.

**Alignment document.** Not in the document

**Size and what it touches.** Medium · screen, data model (owner, devices, sites on a new customer)

**Risk or dependency.** Touches every page; the new-customer form needs three more stored fields.

**Recommendation: NEXT PHASE.** Layout; part of the frame rebuild.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-042, G-043

### D-034 — A real Customer sign-in, and a role chooser in the top bar

**BLUF.** The HTML lets a reviewer switch between five roles, including a Customer who sees only the customer workspace. The site has four roles fixed at sign-in and shows the customer view only as a preview to partner staff.

**HTML against the site today.** HTML: role list Partner, Consultant, Admin, Demo, Customer, labelled "Review role (demonstration only)"; "The Customer role cannot access partner commercial content." Site: no Customer role by design.

**Alignment document.** Section 7 ("Workflow RBAC"), release-suite scenario 18; the v2.1 UAT pack tests it as P0

**Size and what it touches.** Large · data model, sign-in

**Risk or dependency.** A real customer sign-in means per-customer isolation enforced on the server and a security review. A role chooser on a live site would let anyone change role, so it cannot be copied as it is.

**Recommendation: NEXT PHASE.** A security-sensitive change that should not be made during a running UAT.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-044

### D-035 — A breadcrumb on every page

**BLUF.** The HTML shows where you are on every page. The site does so on four pages only.

**HTML against the site today.** HTML: for example "Partner workspace / Overview", "Customer security / Security overview". Site: breadcrumbs on the action plan, delivery phases, offer sheet and revenue pages.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Layout; part of the frame rebuild.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-045

### D-036 — Page heading style, colours and the HP signature card

**BLUF.** The HTML uses a capital-letter section line above each heading, a navy and blue palette, and an HP "Cyber Security Services" card at the top right.

**HTML against the site today.** HTML: section line such as "PARTNER WORKSPACE / COMMERCIAL COMMAND CENTRE"; tiles with a blue accent bar; colour-coded stage chips. Site: its own heading component and a neutral palette set in an earlier design round.

**Alignment document.** Not in the document (section 7 asks for a branded template and accessibility checks before production)

**Size and what it touches.** Medium · screen

**Risk or dependency.** Touches every page and must pass the contrast checks again. Branding is not yet ruled.

**Recommendation: NEXT PHASE.** A visual rebuild; better done once with the frame.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-046

### D-037 — One notice per page in the page's own words (replaces the single site-wide banner)

**BLUF.** The HTML explains on each page exactly what is and is not real. The site shows one general banner.

**HTML against the site today.** HTML examples: "Fictional commercial demonstration. Opportunity values, HPSM licence prices, attribution and contract references are illustrative only."; "Draft rules. This customer's sample scores, findings, HPSM control suggestions and narrative require review and approval. No printer settings are changed." Site: "Prototype with sample content: figures and wording marked below are placeholders until the approved content arrives."

**Alignment document.** Not in the document (it does ask that the prototype "clearly states" its limits: scenario 20)

**Size and what it touches.** Medium · screen

**Risk or dependency.** Conflicts with the earlier ruling of one banner per page; the product owner must say which stands. Several HTML notices say "local" or "browser only", which is untrue for the site.

**Recommendation: NEXT PHASE.** Needs a ruling and a rewrite of each notice for a hosted site.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-047

### D-038 — Partner menu: eight groups and 23 entries, with renamed entries

**BLUF.** The HTML's menu is organised around the reseller's work: my work, customers and opportunities, delivery, growth, revenue. Eleven of its entries are pages the site does not have.

**HTML against the site today.** HTML groups: PARTNER WORKSPACE, MY WORK, CUSTOMERS & OPPORTUNITIES, SECURITY SERVICES DELIVERY, SERVICE GROWTH, REVENUE & ATTRIBUTION, TOOLS & SUPPORT, OPERATIONAL GOVERNANCE. Renames of existing entries: Home to "Dashboard", Customers to "Customer engagements", Engagements to "Assessment pipeline", Revenue to "Revenue modelling", Resources to "Resources & modules", Admin to "Administration". Site: four groups, twelve entries.

**Alignment document.** Release-suite scenario 19 (existing navigation must keep working)

**Size and what it touches.** Large · screen

**Risk or dependency.** Each new entry needs its page first, so the menu grows as pages land. The renames alone are small but would change labels the current UAT guide uses.

**Recommendation: NEXT PHASE.** Most entries have no page yet, and renaming mid-UAT confuses testers.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-048

### D-039 — Who sees which menu entry

**BLUF.** The HTML shows partners every commercial page but not metrics or administration; consultants and demo users see everything except the action plan and administration.

**HTML against the site today.** HTML: a per-role list for all 23 partner entries and nine customer entries. Site: per-role rules for its twelve entries, enforced on the server as well.

**Alignment document.** Section 6 ("Data access must separate customer assessment evidence from partner deal economics"), scenario 18

**Size and what it touches.** Medium · data model

**Risk or dependency.** Every new page needs the same rule on the server, not only in the menu.

**Recommendation: NEXT PHASE.** Follows the pages it governs.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-049

### D-040 — Customer menu: add "Framework alignment" and "My remediation actions"

**BLUF.** The HTML's customer menu has two entries the site lacks.

**HTML against the site today.** HTML customer menu: Security dashboard, Fleet & devices, Security assessments, Gaps & findings, Framework alignment, Remediation roadmap, Reports & evidence, Continuous assurance, and SHARED ACTIONS: My remediation actions. Site: seven entries; Framework alignment is deliberately held back.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** Both entries wait on their pages (see the framework alignment and shared actions items).

**Recommendation: NEXT PHASE.** Depends on two next-phase pages.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-050

### D-041 — Do not build the prototype-only tools

**BLUF.** The HTML carries tools that exist only because it is a single offline file: export and import of the workspace, a sidebar colour comparison and a "REVIEW / LOCAL" chip.

**HTML against the site today.** HTML: "↓ Export workspace", "↑ Import local JSON", "Sidebar: White ⇄", "REVIEW / LOCAL". Site: data is on a server; there is a "Reset demo" for administrators.

**Alignment document.** Section 7 (the demo uses "isolated local storage")

**Size and what it touches.** Small · screen

**Risk or dependency.** Eight cases in the v2.1 UAT pack test these tools and would need to be marked not applicable.

**Recommendation: DROP (keep the site as it is).** They solve a problem the site does not have.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-051

### D-042 — Hide the feedback button in the customer workspace

**BLUF.** The HTML does not show the internal feedback button to a customer.

**HTML against the site today.** HTML: the orange "✎ Feedback" button is hidden in the customer workspace. Site: shown on every signed-in page, the customer preview included.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** While the customer view is only a preview for partner staff, reviewers may want to give feedback there.

**Recommendation: NEXT PHASE.** Only matters once a real customer can sign in.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-052


---

## E. Partner pages (19 items)

### D-043 — Rebuild the partner dashboard around the commercial pipeline

**BLUF.** The HTML's dashboard leads with pipeline value and the next action on a deal. The site's home page leads with readiness, customers and the three-phase overview.

**HTML against the site today.** HTML: "Reseller security services dashboard"; tiles "Open pipeline TCV", "Weighted forecast", "Won / booked TCV", "Contracted annual run-rate"; a "Next recommended action" strip; "Opportunities needing attention"; "My action queue"; "Reseller next steps"; "Commercial control". Site: "Home" with a welcome, the three phases, four headline figures, customers by stage, revenue mix, upcoming activity and recommended next actions.

**Alignment document.** Section 6; P2 for the pipeline figures

**Size and what it touches.** Large · screen, commercial

**Risk or dependency.** Depends on the opportunity register and the action queue. It removes the three-phase panel, which was the product owner's own earlier request, and the welcome, upcoming activity and where-next panels.

**Recommendation: NEXT PHASE.** It cannot be built before the commercial records exist.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-053, G-054, G-055, G-056, G-057, G-058, G-059, G-060, G-061, G-062, G-063

### D-044 — Dashboard and register: show assessment progress as "n of 16 answered" with the customer's owner

**BLUF.** The HTML shows how far each assessment has got in questions answered, and who owns the customer.

**HTML against the site today.** HTML: "Snapshot completion 38% — 6 / 16 answered", with the owner ("Example partner") and a short code under each name. Site: stage, score and last activity on the home page; "1 of 8 steps" on the Customers page.

**Alignment document.** Not in the document

**Size and what it touches.** Medium · screen, data model (owner)

**Risk or dependency.** Needs an owner recorded for each customer and the answered count in the customer list.

**Recommendation: NEXT PHASE.** Part of the register changes.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-064

### D-045 — My readiness as one live page (statements, score and priorities together)

**BLUF.** In the HTML a partner ticks statements and sees the score, band and learning priorities change on the same page. On the site this is a start page, a run and a separate result. The 16 statements themselves already match the HTML.

**HTML against the site today.** HTML: "Partner capability & readiness" with tiles (Readiness score, Capability coverage, Learning priorities, Practice areas), four groups with a subtotal each, "Readiness interpretation" and "Suggested learning priorities". Site: "Playbook Partner Readiness", "Start a self-assessment", then a result with a band and a 30-day plan.

**Alignment document.** Not in the document

**Size and what it touches.** Medium · screen

**Risk or dependency.** The site keeps a history of runs and builds the action plan from the result; a single live page must not lose either.

**Recommendation: NEXT PHASE.** A layout change to something that works and was changed only yesterday.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-065, G-066

### D-046 — Take the customer snapshot launcher off the readiness page

**BLUF.** The HTML keeps readiness about the partner and points to the customer register separately.

**HTML against the site today.** HTML: "Next customer engagement — Readiness is separate from customer security posture. A partner can be ready to start without having assessed a customer's devices." Site: a "Customer snapshot" section on the readiness page.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Goes with the readiness page change.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-067

### D-047 — Training page: descriptions, a six-part learning pathway and five assessment principles

**BLUF.** The HTML's training page explains each stage and lists a curriculum and five principles of independent assessment. The site shows three labels and six Playbook modules.

**HTML against the site today.** HTML: "01 Discover & scope — Set boundaries, identify customer contacts, agree sites, models, evidence and authorised activities."; pathway rows such as "Findings & security control mapping — Traceability, framework relevance and limitation statements"; principles including "Separate assessed facts, self-declared responses and unknown controls" and "Keep commercial proposals out of the customer risk score". Site: "Discover and scope", "Assess and verify", "Advise and deliver" with no descriptions (removed on purpose earlier), then six module links.

**Alignment document.** Executive recommendation (evidence-led assessment); not a named priority

**Size and what it touches.** Medium · screen (wording)

**Risk or dependency.** The pathway rows are titles with no lessons behind them: the product owner must say which module each opens, or supply the content. The five principles and whether this page is in scope are an open question already on the board. One open UAT feedback item also asks for the three stage labels to look less like progress markers.

**Recommendation: NEXT PHASE.** Content choices are open and the curriculum has no material behind it yet.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-068, G-069, G-070, G-071

### D-048 — Guided onboarding page

**BLUF.** A five-step path for a new reseller, from capability to renewal.

**HTML against the site today.** HTML: "Guided reseller onboarding — A practical route from partner capability to customer delivery and recurring revenue", five steps each with "Open this step". Site: none (the guided demo walkthrough is a different thing: a presenter's script).

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** Two of its five steps open pages that do not exist yet (opportunity, proposal).

**Recommendation: NEXT PHASE.** Needs the pages it links to.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-072

### D-049 — My action queue (tasks with owners, due dates and evidence-gated completion)

**BLUF.** The HTML gives each person a list of customer-linked tasks; a task cannot be marked verified complete without an evidence reference, and a task is shared with the customer only when ticked.

**HTML against the site today.** HTML: "My action queue — Prioritise customer follow-ups, service delivery actions, due dates and review evidence"; "Share action status in customer workspace — Never share internal pricing, margins, commercial notes or account details." Site: none; the nearest things are the readiness action plan and the per-finding action register.

**Alignment document.** Section 3 (risk owner, target date), section 5 ("monitor follow-up"); not a named priority

**Size and what it touches.** Large · data model, screen

**Risk or dependency.** A new record type with its own permissions; the customer-visible flag is a privacy control and must be enforced on the server. In the HTML tasks hang off opportunities, which do not exist on the site.

**Recommendation: NEXT PHASE.** New data and new permissions; depends on the opportunity decision.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-073, G-074

### D-050 — Engagement journey and handover checks

**BLUF.** One page showing where a deal is across five stages and whether it is ready to hand to delivery.

**HTML against the site today.** HTML: "Engagement journey & approvals"; stages Qualify, Assess, Propose, Deliver, Optimise; five handover checks with the caveat "This checklist does not certify assessment quality or approve contractual terms." Site: none.

**Alignment document.** Section 5 (recommended lifecycle)

**Size and what it touches.** Large · data model, screen, commercial

**Risk or dependency.** Depends on opportunities and the activity history.

**Recommendation: NEXT PHASE.** Depends on two next-phase items.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-075

### D-051 — Activity history

**BLUF.** A timeline of calls, decisions and approvals per deal.

**HTML against the site today.** HTML: "Engagement activity — Record important sales, assessment and delivery decisions in one opportunity-linked timeline", with the note "A production audit trail must be server-generated and tamper-evident." Site: an audit record of assessment actions on the server, not shown as a timeline.

**Alignment document.** Section 3 ("revision history"), section 5

**Size and what it touches.** Large · data model, screen

**Risk or dependency.** A hand-typed history is not an audit trail; the page must say so, as the HTML does.

**Recommendation: NEXT PHASE.** New data; depends on opportunities.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-076

### D-052 — Customer register: columns, stage chips, sorting

**BLUF.** The HTML's register is simpler to scan and filters by stage with one tap.

**HTML against the site today.** HTML: "Customer register (4)"; columns customer, industry, devices / sites, stage, assessment progress, last activity, open; stage chips All / New lead / Assessment in progress / Findings ready / Report issued; sort by name, progress or devices; a card linking to the opportunity pipeline. Site: more columns, a per-row actions menu, and filter lists.

**Alignment document.** Release-suite scenario 19

**Size and what it touches.** Medium · screen

**Risk or dependency.** The site's row menu (findings, firmware task, documents, coach) would be lost unless kept.

**Recommendation: NEXT PHASE.** Layout; goes with the register data changes.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-077, G-078, G-079, G-080

### D-053 — Assessment pipeline page: heading and two small additions

**BLUF.** The page the site calls "Engagements" is almost the same in the HTML.

**HTML against the site today.** HTML: section line "CUSTOMER LIFECYCLE", a "View all customers" button, a footnote "1 sample customer(s) without an engagement." Site: "Engagements" with the same table and the same footnote in other words.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Cosmetic; goes with the menu rename.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-081

### D-054 — Action plan: tiles, an editable status and a source category

**BLUF.** The HTML's action plan shows the programme phase and counts, and lets status be changed in the list.

**HTML against the site today.** HTML: "Action plan — Your practice-level activities for moving from assessment capability through implementation and ongoing service delivery"; tiles Programme phase, Actions, Completed, In progress; "Your next 30 days". Site: "Partner Action Plan", built from the readiness result.

**Alignment document.** Not in the document

**Size and what it touches.** Medium · screen, data model

**Risk or dependency.** Needs a programme phase and a category stored for each action.

**Recommendation: NEXT PHASE.** Layout and small data additions.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-082

### D-055 — Delivery and assessments page

**BLUF.** A list joining each deal to its technical progress.

**HTML against the site today.** HTML: "Delivery and assessment queue — Keep customer security review, remediation projects and delivery responsibilities distinct from sales status." Site: none.

**Alignment document.** Section 6 (keep sales and assessment separate)

**Size and what it touches.** Medium · screen, commercial

**Risk or dependency.** Depends on opportunities.

**Recommendation: NEXT PHASE.** Depends on a next-phase item.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-083

### D-056 — Delivery phases page: phase descriptions and an inline offer sheet

**BLUF.** The HTML describes each phase in one line and shows the offer sheet on the same page.

**HTML against the site today.** HTML: heading "Service offers"; "Phase 1: Assessment & design — Fleet discovery, security snapshot, evidence review and proposed remediation roadmap."; "Phase 2: Implementation — Validate policy control mapping, apply approved remediation under change control and document exceptions."; "Phase 3: Managed service — Recurring posture review, advisory monitoring, exception management and security reporting." Site: "Delivery phases" with its own one-line descriptions, separate offer-sheet pages and two sample tracker pages. Both say the offer content is a placeholder.

**Alignment document.** Section 6

**Size and what it touches.** Medium · screen (wording)

**Risk or dependency.** The product owner must say whether the separate offer pages and trackers stay. The phase descriptions are offer content awaiting approval in both.

**Recommendation: NEXT PHASE.** Offer content is still a placeholder on both sides.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-084, G-085

### D-057 — Resources and modules page: heading, counter and card style

**BLUF.** Cosmetic changes to the Playbook module list.

**HTML against the site today.** HTML: section line "KNOWLEDGE CENTRE", "Playbook modules — 0 of 11 viewed", cards "MODULE 01 / 11" with "Open module →". Site: "The Playbook, digital", cards "Module 1" with status tags.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** A viewed counter needs somewhere to remember what each person has opened.

**Recommendation: NEXT PHASE.** Cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-086

### D-058 — Keep the site's Playbook module names and text

**BLUF.** The HTML's module pages are three-line placeholders and five of its module names are its own proposals. The site carries the actual Playbook deck text.

**HTML against the site today.** HTML: "Module summary is a review aid, not a replacement for the approved HP Playbook deck"; every module shows the same Purpose / What to validate / Output text; names such as "Scoring and evidence" and "Commercial opportunity" are described as "proposed navigation headings". Site: eleven modules in the deck's order with the deck's wording.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** None if kept.

**Recommendation: DROP (keep the site as it is).** The site is ahead: this is one section where the HTML is plainly not the more accurate source.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-087, G-088

### D-059 — Automation metrics: add four summary tiles

**BLUF.** The HTML summarises the runs in four tiles above the table.

**HTML against the site today.** HTML: tiles Runs counted, Median elapsed time, Findings raised, Manual baseline; "Definitions are proposed and elapsed-time baselines have not been measured. No time savings are claimed." Site: a table with nine measures per run and the same no-saving statement.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** Keep the site's nine columns: they are the measures the statement of work asks for.

**Recommendation: NEXT PHASE.** Cosmetic addition.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-089

### D-060 — Administration page: name, introduction and one extra line

**BLUF.** Small wording changes to the administrator's page.

**HTML against the site today.** HTML: "Administration — Local design-review settings and feedback. User management, content packages and tenant integrations are not included"; adds "Content-package administration — Future phase". Site: "Admin" with feedback links and four connection lines.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** The HTML's "local" wording is untrue for the site and must not be copied word for word.

**Recommendation: NEXT PHASE.** Cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-090

### D-061 — Operational readiness and release gates page

**BLUF.** A checklist of what must be true before real customer data is used.

**HTML against the site today.** HTML: "Operational readiness & release gates" with eight requirements (sign-in, isolation, storage, audit, integrations, security testing, accessibility, user acceptance) and tiles "0/8", "0 Production integrations configured", "LOCAL". Site: none.

**Alignment document.** Appendix (release sign-off record), section 7 ("Required for production")

**Size and what it touches.** Medium · screen

**Risk or dependency.** Copied as it is, the page would be untrue: the site already has sign-in, server-side roles and durable storage. It needs rewriting as a true status page.

**Recommendation: NEXT PHASE.** Needs a rewrite against the real state of the site, and the sign-off record can be kept as a document meanwhile.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-091


---

## F. Customer engagement (the eight-step journey and its tabs) (9 items)

### D-062 — Customer workspace: header, summary strip and overview tab

**BLUF.** The HTML opens each customer with a one-line summary of where the assessment stands and what happens next.

**HTML against the site today.** HTML: "Manufacturing · 220 printers and MFPs · 5 sites · Example partner"; strip "16 / 16 captured · 7 draft findings · Findings ready"; "What happens next? 1. Confirm assessment evidence. 2. Approve material findings. 3. Vet control mappings. 4. Review the narrative before producing the customer document." Site: customer details, sites and devices, engagement progress, engagement summary and recent activity.

**Alignment document.** Not in the document

**Size and what it touches.** Medium · screen

**Risk or dependency.** The site's overview holds more (contact role, existing controls, recent activity); decide what stays.

**Recommendation: NEXT PHASE.** Layout.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-092, G-093

### D-063 — "Related commercial opportunities" on every customer tab

**BLUF.** Shows the deals for this customer under each tab, in the partner view only.

**HTML against the site today.** HTML: "Related commercial opportunities — Separate deal records for this customer; available only in the partner workspace." Site: none.

**Alignment document.** Section 6

**Size and what it touches.** Medium · screen, commercial

**Risk or dependency.** Depends on opportunities; must never appear in the customer view.

**Recommendation: NEXT PHASE.** Depends on a next-phase item.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-094

### D-064 — Journey rail: "Eight-step journey", numbered headings, Metrics set apart

**BLUF.** The HTML numbers the eight steps and treats Metrics as an extra, not a ninth step.

**HTML against the site today.** HTML: rail headed "EIGHT-STEP JOURNEY" with "⋯ Metrics" below; headings "1. Customer profile" to "8. Next engagement"; the metrics page is "Customer automation metrics". Site: nine equal steps, headings without numbers, "Automation metrics".

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-095, G-096

### D-065 — Question screen: filter by group and a "Create follow-up draft" button

**BLUF.** The HTML lets the assessor show one group of questions at a time and start a follow-up from the question screen.

**HTML against the site today.** HTML: "Show questions for" (Everyone or one of five groups); "Create follow-up draft"; a side list of all 16. Site: a side map of all questions by group, "Skip for now", and a follow-up panel on the customer's assessment page.

**Alignment document.** Not in the document

**Size and what it touches.** Small · screen

**Risk or dependency.** Where the site's follow-up control sits compared with the HTML's was not settled in the earlier catalogue either.

**Recommendation: NEXT PHASE.** Cosmetic; the function exists.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-097

### D-066 — Action register: the agreed rule sentence

**BLUF.** The line above the action register should say that both "Evidence submitted" and "Verified complete" need an evidence reference. The product owner approved the sentence this morning; it is not yet on the site.

**HTML against the site today.** HTML: "Consultant action register ... Marking an action complete requires an evidence reference, but this local demo does not independently verify it." Site: "Verified complete needs an evidence reference. The reference is not checked independently."

**Alignment document.** Section 3 (supporting reference); not a named priority

**Size and what it touches.** Small · screen

**Risk or dependency.** None; already ruled.

**Recommendation: THIS PHASE.** Already decided by the product owner; it only needs building.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-098

### D-067 — Finding detail: replace "Not written yet" with the honest caveat

**BLUF.** A finding's business impact reads "Not written yet" on the site. The HTML says what is true: impact must be evidenced, not assumed from an answer.

**HTML against the site today.** HTML: "Potential business impact — Draft / to be validated. This item highlights a possible control gap. Customer impact and affected devices need to be evidenced, not inferred from a Yes/No answer alone." Site: "Business impact — Not written yet".

**Alignment document.** Section 3 ("A self-declared 'Yes' must not be described as independently verified")

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** The sentence is in the HTML, so nothing is invented. Real impact wording per finding still needs HP SME content.

**Recommendation: THIS PHASE.** One sentence, visible on every finding in the current UAT.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-099

### D-068 — Firmware risk task: use the HTML's checklist and guidance

**BLUF.** The site's checklist for this task is four partner readiness statements from the old deck, which are not steps of a task. The HTML has four actual steps.

**HTML against the site today.** HTML checklist: "Review supported device models and firmware versions", "Compare firmware to HP security advisories", "Record prioritised exceptions and affected devices", "Approve a remediation or monitoring plan"; guidance "Verify the manufacturer's latest advisories, supported management functions and policy syntax before applying configuration changes." Site checklist: "We ensure customer printers can verify trusted firmware at boot and block unauthorized code." and three more in the same form.

**Alignment document.** Section 4 (firmware: "Test, schedule, change control and rollback")

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** The wording is in the HTML. One site item ("regular or automated updates") repeats the claim the document says must change.

**Recommendation: THIS PHASE.** Small, visible in UAT, and it removes a second copy of the automatic-updates wording.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-100, G-101

### D-069 — Conversation coach: add the HTML's five talk tracks

**BLUF.** The HTML has five short talk tracks tied to the three phases. The site has eight general guides plus guides built from the customer's own findings.

**HTML against the site today.** HTML: "Opening a print security conversation", "Explaining an unresolved finding" ("We have an answer that needs validation before we call it a confirmed risk."), "Why HP Security Manager?", "How do we commercialise remediation?", "Building a recurring security service". Site: guides on cost, competing priorities, decision process, disruption, proving value, comparison and next step, marked as sample.

**Alignment document.** Not in the document (the fourth track touches the consulting-fee question)

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** The product owner must choose: add the five, replace the eight, or keep the eight. Audience testing of the coach is an open item.

**Recommendation: NEXT PHASE.** A content choice, not a correction.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-102

### D-070 — Keep the site's findings review, next engagement and metrics steps

**BLUF.** On three journey steps the site does more than the HTML and nothing should be taken back.

**HTML against the site today.** HTML: a single "Mark finding reviewed" button; a fixed placeholder next engagement ("Print-device hardening and control validation"); four metric tiles with "Consultant time — Not measured". Site: review with override, risk acceptance and a mandatory audit note; a next engagement chosen by rule with the reason shown; six measured metrics.

**Alignment document.** Section 3 (revision history), section 5

**Size and what it touches.** Small · screen

**Risk or dependency.** None if kept.

**Recommendation: DROP (keep the site as it is).** The site is ahead on all three.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-103, G-104, G-105, G-106


---

## G. Customer security workspace (10 items)

### D-071 — Customer pages: a section line per page and the HTML's caveat

**BLUF.** The HTML tells the customer on every page what the answers are and are not.

**HTML against the site today.** HTML: "Customer security experience · <customer>. Self-reported assessment responses are not device verification. Only consultant-reviewed gaps appear in customer remediation and reporting; all control mapping is indicative." Site: "This is a read-only preview of what a customer would see. Answers given in an assessment are self-reported and are not device verification. Only findings a consultant has reviewed appear here."

**Alignment document.** Section 3 (self-declared is not verified)

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** The site's wording is right while the customer view is a preview for partner staff.

**Recommendation: NEXT PHASE.** Changes meaning only when a customer can sign in.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-107

### D-072 — Customer dashboard: answer signal, coverage, unknowns, domains and confidence

**BLUF.** The HTML shows a customer how much is known, how much is unknown and how confident the picture is. The site shows counts of reviewed findings and answered questions.

**HTML against the site today.** HTML: "Print & edge security posture"; tiles "Answer-based signal 64/100 — Yes ÷ definitive Yes/No answers; draft formula", "Definitive coverage 88%", "Reviewed gaps 5", "Unknown responses 2 — Unsure + unanswered; not scored as failed"; "Security domains" bars; "Assessment confidence — An assessment score alone is insufficient to establish fleet security posture." Site: "Security dashboard" with four tiles and the priority findings.

**Alignment document.** Section 3 (unknown is not failed), section 5 ("evidence confidence")

**Size and what it touches.** Medium · screen, data model

**Risk or dependency.** It shows a draft score to a customer; the product owner must agree to that. It uses the HTML's simple formula, which differs from the site's weighted score, so two different scores could appear for one customer.

**Recommendation: NEXT PHASE.** Needs a ruling on customer-visible scores and follows the Unsure change.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-108, G-109, G-110, G-111

### D-073 — Fleet page: heading and a scope-limitations panel

**BLUF.** The HTML adds a plain statement of what the fleet page does not know.

**HTML against the site today.** HTML: "Print fleet & edge devices"; "Scope limitations — The prototype does not invent individual device models, compliance states, firmware versions, locations or vulnerability results. This keeps the assessment honest where inventory data has not been supplied." Site: "Fleet and devices" with the same tiles and table.

**Alignment document.** Section 3 (inventory first; "include non-HP and unknown devices")

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Cosmetic; the facts shown are the same.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-112

### D-074 — Customer assessments page: every question, its answer and its review status

**BLUF.** The HTML shows the customer each question with the recorded answer and whether it is a reviewed gap, declared in place or needing verification. The site shows only that an assessment exists and its status.

**HTML against the site today.** HTML: "Assessment overview"; tiles Yes / No / Unsure / Not answered; "Question responses by domain" with "Reviewed gap", "Declared in place", "Verification required"; "A Yes answer indicates an assertion by the assessor or customer, not evidence of implementation." Site: "Security assessments", one line per assessment.

**Alignment document.** Section 3

**Size and what it touches.** Large · screen, data model

**Risk or dependency.** Showing raw answers to a customer is a visibility decision for the product owner, and the server must release them to the customer view deliberately.

**Recommendation: NEXT PHASE.** A visibility decision plus server work.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-113

### D-075 — Customer findings: answer, source question, framework relevance and evidence to verify

**BLUF.** The HTML explains each finding to the customer: what was answered, which question it came from, what evidence would confirm it.

**HTML against the site today.** HTML: "Reviewed risks & gap analysis"; per finding "Recorded response: No · Traceable to: Q01", "Framework relevance: ISO/IEC 27001:2022 A.5.15 / A.8.2 · Protect · Identity & access", "Evidence to verify: Admin-role listing and permission review"; a legend including "Alignment: an ISO/NIST mapping does not establish standards compliance". Site: "Gaps and findings" with severity, title and action.

**Alignment document.** Section 3 (evidence fields), section 5 ("evidence-linked findings")

**Size and what it touches.** Large · screen, data model, question set

**Risk or dependency.** Needs HP SME content: the framework references and the evidence list exist only for the HTML's 16 questions and are described there as indicative. The standards mapping is an open content question on the board.

**Recommendation: NEXT PHASE.** Blocked on an approved mapping and tied to the question-set decision.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-114, G-115

### D-076 — Framework alignment page (ISO/IEC 27001 and NIST themes per question)

**BLUF.** A table mapping each question to standards themes. The site holds this page back until an approved mapping is supplied.

**HTML against the site today.** HTML: "Security controls & gap mapping"; 16 rows such as "Q02 · Monitor firmware versions and implement a defined update standard — A.8.8 — Identify / Protect · Vulnerability management"; "Framework relationships are indicative review mappings, not a formal ISO/IEC 27001 audit, certification, NIST CSF conformance statement or proof that a control is implemented. Mapping and terminology require specialist review." Site: held.

**Alignment document.** Not in the document

**Size and what it touches.** Large · screen, data model, question set

**Risk or dependency.** Needs HP SME content: the mapping is in the HTML but says itself that it requires specialist review, and it maps the HTML's questions, not the site's.

**Recommendation: NEXT PHASE.** Held on purpose until an approved mapping exists; nothing has changed that.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-116

### D-077 — Customer roadmap: counts, owner and status lines, closure note

**BLUF.** Small additions that tell the customer who is to act and what closing an item requires.

**HTML against the site today.** HTML: "Prioritised remediation roadmap"; "Owner: To be assigned · Status: Not started"; "Remediation closure should require an owner, change reference, test evidence, re-assessment and customer sign-off." Site: "Remediation roadmap", grouped actions, "Owner: Not recorded".

**Alignment document.** Section 3 (risk owner, target date), section 4

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** The roadmap inherits the automatic 30-day column until that item is done.

**Recommendation: NEXT PHASE.** Cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-117

### D-078 — Customer reports page: three-step evidence status and a distribution note

**BLUF.** The HTML shows the customer the three things a report rests on and says nothing is sent.

**HTML against the site today.** HTML: "Reports & assessment evidence"; "Evidence status: 01 Assessment responses, 02 Findings reviewed, 03 Executive narrative"; "External distribution — No emails, portal invitations, PDF delivery, external document retention or audit integration are connected in this version." Site: "Reports and evidence", the report card and two tiles.

**Alignment document.** Section 7 ("Export / customer delivery"), scenario 20

**Size and what it touches.** Small · screen (wording)

**Risk or dependency.** None.

**Recommendation: NEXT PHASE.** Cosmetic.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-118

### D-079 — Continuous assurance page: open evidence requests, an assurance cycle and next steps

**BLUF.** The HTML shows what is still unknown and proposes a cycle of observe, evaluate, report.

**HTML against the site today.** HTML: "Continuous improvement"; tile "Open evidence requests 2 — Unknown or unanswered controls"; "Proposed assurance cycle"; five next steps. Site: "Continuous assurance" with three tiles.

**Alignment document.** Section 5 ("monitor follow-up")

**Size and what it touches.** Medium · screen

**Risk or dependency.** The assurance cycle is proposed service content; the product owner should confirm it.

**Recommendation: NEXT PHASE.** Follows the Unsure change and the dashboard.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-119

### D-080 — "My remediation actions": actions shared with the customer

**BLUF.** A customer sees the tasks the partner has chosen to share, and nothing commercial.

**HTML against the site today.** HTML: "Remediation action status — Review the subset of security actions specifically shared for this customer"; "commercial notes, prices, margins and internal tasks are excluded." Site: none.

**Alignment document.** Section 6 (data separation)

**Size and what it touches.** Medium · screen, data model

**Risk or dependency.** Depends on the action queue and on a customer-safe way to read it.

**Recommendation: NEXT PHASE.** Depends on two next-phase items.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-120


---

## H. Testing, sources and sign-off (5 items)

### D-081 — Ask which sections of the HTML hold "the most accurate content"

**BLUF.** The instruction says the HTML has the most accurate content "for some sections" without naming them. This analysis found sections where the HTML is ahead, sections where the site is ahead, and sections where neither is approved.

**HTML against the site today.** HTML ahead: readiness statements (already adopted), firmware task checklist, finding-impact caveat, per-page notices, the customer view's handling of unknowns. Site ahead: Playbook module text, findings review, narrative and report, metrics, revenue calculator. Neither approved: the 16 questions, findings wording, HP Security Manager mappings, framework mapping, service tiers and offers.

**Alignment document.** Section 9 ("prioritise content accuracy before adding commercial automation")

**Size and what it touches.** Small · decision only

**Risk or dependency.** Without the list, content could be copied from the wrong side.

**Recommendation: THIS PHASE.** A question for the product owner that steers every content item above.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-121

### D-082 — Ask for the v2.2 demo that the alignment document describes

**BLUF.** The document says a v2.2 standalone demo implements the revised questions, six answer states, narrative revisions, report contents, three reseller modes and an opportunity register. That file was not among the attachments; only v2.1 and v2.0 were.

**HTML against the site today.** Document section 7: "Revised 16-question set — Implemented; new schema and isolated local storage" and seven more capabilities marked implemented in the v2.2 demo. Attachments received: the v2.1 layout alignment HTML, the v2.0 guided demo HTML, the UAT plan and tracker, and the document.

**Alignment document.** Section 7 (prototype implementation status)

**Size and what it touches.** Small · decision only

**Risk or dependency.** Without it the revised question wording and the six-state screens have no reference.

**Recommendation: THIS PHASE.** A request, not work.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-122, G-123

### D-083 — Adopt the document's 20 scenarios as the acceptance test for this phase's items

**BLUF.** The document gives a minimum release suite of 20 scenarios. Against the site today: 4 met, 10 partly met, 2 not met, 3 waiting on content, 1 behind a change request.

**HTML against the site today.** The suite covers question numbering, mixed fleets, unknowns, compensating controls, evidence source, firmware actions, certificates, narrative and report approval, report navigation, commercial separation, read-only roles and navigation. See UAT-SCENARIOS.md for each verdict.

**Alignment document.** Section 8 ("Acceptance/UAT scenarios — minimum release suite")

**Size and what it touches.** Small · testing

**Risk or dependency.** Several scenarios cannot pass in this phase whatever is built (they need the six states or the opportunity register), so the suite should be split by phase at the same sitting.

**Recommendation: THIS PHASE.** It turns the decisions in this document into a pass or fail list.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-124

### D-084 — Decide what the v2.1 UAT pack is for

**BLUF.** The UAT plan and tracker (285 functional cases, 38 non-functional, 32 production gates, 12 end-to-end journeys) test the HTML file, not the site. Run against the site today, 109 of the 285 functional cases are met in full.

**HTML against the site today.** The pack names the HTML as its "reference application" and its testing boundary as an "offline fictional-data HTML demonstration". Of the 285 functional cases: 109 are met by the site, 26 partly, 60 not met (the page does not exist), 6 wait on content, 84 are behind a change request or are prototype-only. See UAT-SCENARIOS.md.

**Alignment document.** Section 9 ("Baseline UAT outcomes and issues against the existing v2.1 test suite"), appendix gate "Regression / accessibility"

**Size and what it touches.** Small · testing

**Risk or dependency.** If testers run this pack against the site as it is, most failures will be next-phase pages rather than defects. Its case numbers (UAT-001 to UAT-285) collide with the document's UAT-01 to UAT-20.

**Recommendation: THIS PHASE.** It affects the UAT that is running now; a one-line ruling prevents a wave of false defects.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-125

### D-085 — Record the seven sign-off gates and who holds each

**BLUF.** The document ends with seven gates that must be signed before v2.2 is distributed as approved guidance. None has a named person yet.

**HTML against the site today.** Gates: assessment and question logic; HP hardware controls; firmware and HPSM; WXP certificates and licensing; security and data governance; channel validation; regression and accessibility. The document describes itself as "Internal working document; not customer-approved HP product guidance."

**Alignment document.** Appendix (internal release sign-off record), section 8 (ownership and decision gates)

**Size and what it touches.** Small · records only

**Risk or dependency.** Four of the seven gates need an HP SME. Every item above marked "needs HP SME content" waits on one of them.

**Recommendation: THIS PHASE.** Records only, and it shows at a glance which decisions are blocked on HP.

**Decision:** [ ] This phase  [ ] Next phase  [ ] Drop

Notes:

Evidence: G-126


---

## What this document does not cover

- It compares the HTML with a local build of the site running on sample data. The live 16 questions, findings and report wording were read from the site's content files, not seen on a running UAT screen, and the hosted UAT site and its stored assessments were not opened.
- It does not judge whether the security content in the HTML or in the alignment document is correct. That is for the HP SMEs named in the document's appendix.
- Sizes are estimates for discussion, made without design work.
