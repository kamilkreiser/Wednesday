# HPSMPOC board reconcile against HPSM-POC main

**Generated:** 2026-09-27 08:47:08 AEST (read-only analysis subagent for Friday). No Jira writes, no git writes, nothing in the HPSM-POC folder was changed.

## How this was read
- **Jira:** `project = HPSMPOC ORDER BY key ASC` via `/rest/api/3/search/jql`, paginated (1 page, no nextPageToken). **64 issues read; 62 not in statusCategory Done** (the 2 Done are HPSMPOC-2 and HPSMPOC-8). That matches the 64/62 Friday measured at 08:3x. All 62 are in status `Backlog`. The 62 are 9 epics and 53 tasks. Every existing comment on all 62 was also read (GET only).
- **Code:** HPSM-POC `main` = `33abe1a6c17f0250f771b3c5d03b91210a0d0621`, read back from `commits/main` at the start. The tarball of that SHA was read locally. PRs #1–#32 were read through the GitHub API (all closed; #5 and #6 are red-proofs that were never merged).
- **Records:** Briefs `*STATUS.md` (B01–B28), `CLARIFICATIONS.md` (C-01…C-27), `BACKLOG.md`, the design pack, the requirements map (B15, read at `61f6f06`, re-checked here at `33abe1a` wherever it mattered), the demo script v0 and `Registers/2026-09-23_jira-seed-log.json`.
- **The rule used:** DONE only when the ticket's own acceptance criterion is met on main. Where the AC says "approved" content (SME/HP), the machinery can be on main and the ticket is still **PARTLY / C**.

## Totals
| Verdict | Count |
|---|---|
| DONE | 10 |
| PARTLY | 40 (9 epics + 31 tasks) |
| NOT STARTED | 12 |
| DUPLICATE | 0 |
| UNCLEAR | 0 |
| **Total** | **62** (= the not-done set) |

For the 52 that are not DONE:

| Class | Count |
|---|---|
| A | 10 |
| B | 14 |
| C | 8 |
| D | 20 (9 epics + 11 tasks) |

**Duplicates:** none were proven. The overlaps below were checked and are distinct asks, so both tickets stay open:
- 28 (audit) and 36 (override audit)
- 29 (M3 demo in UAT) and 60 (Playwright in UAT/Demo)
- 15 (AI criteria) and 41 (review gate)

## Rows
Column key:
- **Verdict:** D = DONE, P = PARTLY, NS = NOT STARTED.
- **Cls:** class / size / route.
- **Paths:** paths are at `33abe1a`. PR = https://github.com/datasecau/HPSM-POC/pull/n.

| Key | Summary | Status now | Verdict | Evidence / what is left | Cls |
|---|---|---|---|---|---|
| HPSMPOC-1 | EPIC Commercial & Governance | Backlog | P | 2 of 8 children Done (CG-1, CG-7); 3, 4, 5, 6 PARTLY; 7, 9 NOT STARTED. Closes with its children. | D (children) |
| HPSMPOC-3 | [CG-2] Executed POC SOW + Development Team | Backlog | P | Team ruled: Kam + Friday (C-02; Jira comment 38101). **Left:** the SOW signed by both parties; a named Tech Lead. | B |
| HPSMPOC-4 | [CG-3] IP and licensing | Backlog | P | Position ruled: Datasec owns (C-04; comment 38103). Licence facts on main: PdfPig Apache-2.0, JsonSchema.Net 8.0.5 MIT (ADR-R01/C01). **Left:** the §11.3 contract clause, in the SOW Kam is writing (C-20). | B |
| HPSMPOC-5 | [CG-4] Event date, window, audience | Backlog | P | Date ruled: Tue 1 Dec 2026 (C-03). Plan re-based in `Architecture/2026-09-23_POC-delivery-plan-v2-1Dec.md`. **Left:** the event window and audience (demo script v0 U1–U11 all UNKNOWN). | B |
| HPSMPOC-6 | [CG-5] PO and Security SME | Backlog | P | PO = Kam (C-05). **Left:** the SME named (C-05 reads it as Kam "until he says otherwise"); a deputy PO named. | B |
| HPSMPOC-7 | [CG-6] SME funding §9.1 or §9.3 | Backlog | NS | Nothing recorded (K-14 UNDECIDED in the B15 map). | B |
| HPSMPOC-9 | [CG-8] Stage-gate evidence pack + CR log | Backlog | NS | No M1–M8 template or CR form exists in HPSM-POC (searched `1_Project_Definition`). The only hits are plans and the SOW. The ticket is agent-owned. | A / M / Claude |
| HPSMPOC-10 | EPIC WS1 Discovery & Architecture | Backlog | P | Children 11–17 are all PARTLY, and every one waits on Kam's M2 approval. | D (children) |
| HPSMPOC-11 | [WS1-1] Kick-off, SME cadence, backlog baseline | Backlog | P | Backlog imported: `Registers/2026-09-23_jira-seed-log.json` (64 issues). **Left:** kick-off minutes and an SME office-hours slot. The team is Kam + Friday (C-02), so Kam decides whether to record a kick-off or waive it. | B |
| HPSMPOC-12 | [WS1-2] Demo story + 7-min script v0 | Backlog | P | `1_Project_Definition/Demo/2026-09-23_demo-story-and-7min-script-v0.md`: 12 steps = 6:15 (comment 38109). **Left:** PO review is not recorded anywhere. The script also predates C-12 (the deck + 16-question focus) and C-17/19/21 (the showcase). | B |
| HPSMPOC-13 | [WS1-3] Architecture pack, data model, API contracts | Backlog | P | `design-pack/00–19`, `api/openapi.yaml`. The contract on main is `api/.../Contract/openapi.yaml` 0.5.x. **Left:** written PO approval (M2). The DP `db/001_schema.sql` is not reconciled with the EF model (comment 38161). | B |
| HPSMPOC-14 | [WS1-4] Versioned rules schema | Backlog | P | `api/src/HpsmPoc.Modules.Rules/Schema/ruleset.schema.json` has `version`, `controlRefs`, `applicableWhen`/`showWhen`, `weight`, `severity`, `bucket`, `hpsmPath`, `noDeviceChange`. It came in PR #2 and the loader validates against it. **Left:** Kam's rulings on RS-03…RS-10 (only RS-11 is ruled, C-15). `importRuleset` is still in `ContractTests.NotYetImplemented` (no DB-side ruleset metadata). | B |
| HPSMPOC-15 | [WS1-5] AI boundary spec + AI acceptance criteria | Backlog | P | Boundary spec: `design-pack/05_ai-narrative-pipeline.md`, built in PRs #7/#23/#25/#27/#32. **Left:** no document holds the POC AI acceptance criteria adapted from HPSM-29 AC-AI-02/03/04/05/07 (the string "AC-AI" appears only in the plan and the reuse inventory). Then PO approval. | A / S / Claude (then Kam approves) |
| HPSMPOC-16 | [WS1-6] Stack decision record | Backlog | P | `design-pack/10_ADRs.md`: 7 RULED / 29 DECIDED (comment 38167). C-08 fixes the stack. **Left:** sign-off of the record as a whole; §4.1 deviations listed with reasons (no Figma; PdfPig not QuestPDF). | B |
| HPSMPOC-17 | [WS1-7] Acceptance matrix §8.1 → tests | Backlog | P | `design-pack/09_acceptance-matrix.md` maps 13/13 rows (commit 594fa16). **Left:** every row still reads DESIGNED against planned ids (SEC-nn, G0–G2). None points at a test that now exists on main. Re-point each row to real tests at 33abe1a, then Kam confirms the proposed bars. | A / S / Claude |
| HPSMPOC-18 | EPIC WS2 UX/UI | Backlog | P | 19 and 22 PARTLY; 20 and 21 NOT STARTED. | D (children) |
| HPSMPOC-19 | [WS2-1] Figma flows | Backlog | P | A coded clickable prototype covers all seven flows and more (PRs #3, #9, #17, #19). There is **no Figma** (comments 38110, 38153). **Left:** Kam rules whether the coded prototype replaces Figma (B15 map POC-G02). | B |
| HPSMPOC-20 | [WS2-2] Prototype review + written PO approval | Backlog | NS | The review guide exists (`Design/2026-09-23_M2-prototype-review-guide.md`). No written approval is recorded. | B |
| HPSMPOC-21 | [WS2-3] Branding source | Backlog | NS | Neutral tokens in one file (`web/src/styles/brand.css`; PDF `Pdf/BrandTokens.cs`). No decision is recorded (QA-027). | B |
| HPSMPOC-22 | [WS2-4] Event-ready screen states | Backlog | P | Prototype and B04 screens have empty, loading, error and fallback states: `web/e2e/states.spec.ts` (tests at :35, :57, :104), comments 38113/38154. **Left:** the B09/B11/B17 showcase screens (customer and partner) have e2e for headings, axe and keyboard, but no loading/error/empty state proofs. The fallback-customer path needs to be written into the demo pack. | A / M / Claude |
| HPSMPOC-23 | EPIC WS3 Core Platform | Backlog | P | 25 and 27 DONE; 24, 26 and 28 PARTLY; 29 NOT STARTED. | D (children) |
| HPSMPOC-24 | [WS3-1] Entra sign-in with 4 roles | Backlog | P | API: JwtBearer fail-closed plus the roles claim, configured for `hpsm-poc-api-dev` (`EntraConfigTests`, PR #8; comment 38152). **Left:** the web sign-in is a mock (`SignInScreen.tsx` "MOCK ENTRA ID"). There is no BFF/MSAL, no web app registration, and a real token has never been exercised. | D: needs a web host / registration (HPSMPOC-57; C-13 entra-app: a). Auth, so Claude/L when unblocked. |
| HPSMPOC-25 | [WS3-2] Customer workspace | Backlog | **DONE** | PRs #8, #19, #22. `AssessmentApiTests.cs:273 Lists_show_status_score_risks_and_the_next_service`; `CustomerApiTests.cs:15 Create_returns_201_with_location_etag_owner_and_a_uuid_v7_id`; web `CustomerManagement.tsx`. | — |
| HPSMPOC-26 | [WS3-3] Customer profile capture | Backlog | P | API: `ProfileApiTests.cs:22 First_save_uses_if_none_match_then_if_match_and_get_returns_it` (PR #8). Web saves industry, staff size, sites and printers through `updateCustomer` (`ApiSteps.tsx:50`, C-21, PR #24). **Left:** the web never calls `putCustomerProfile`, so environment, print/security posture and existing controls (the ruleset `profileFields`) are not captured for API customers. The field wording is a placeholder, pending HP's data dictionary. | A / M / Claude |
| HPSMPOC-27 | [WS3-4] Guided assessment runner with persistence | Backlog | **DONE** | PRs #8, #9, #12, #15. `AssessmentApiTests.cs:124 A_conditional_follow_up_appears_and_a_hidden_question_cannot_be_answered`, `:159 Evidence_is_registered_as_ev_nnn_and_can_then_be_referenced`, `:203 After_submit_answers_are_locked_409…`. Notes and evidence refs are on `ResponseRecord` (`Persistence/Entities.cs:107-117`). The customer question content is placeholder, which is tracked in HPSMPOC-31. | — |
| HPSMPOC-28 | [WS3-5] Audit trail | Backlog | P | Create, answer, report and review actions are audited: `AuditTrailTests.cs:35 Every_state_change_writes_exactly_its_audit_event…` (PR #8). **Left:** "override" cannot be audited because override does not exist (HPSMPOC-36). The Azure SQL ledger table is not carried (comment 38150). | D: HPSMPOC-36 |
| HPSMPOC-29 | [WS3-6] M3 happy path in UAT | Backlog | NS | No UAT environment exists (only the AOAI subset is deployed, B18). | D: HPSMPOC-57 (+24) |
| HPSMPOC-30 | EPIC WS4 Rules & Scoring | Backlog | P | 33 and 34 DONE; 31, 32, 35, 36 and 37 PARTLY. | D (children) |
| HPSMPOC-31 | [WS4-1] SME authors representative content | Backlog | P | Authoring template v0 (`Content/SME-authoring-template-v0/`, comment 38108); loader ready. The customer questions have been requested by Kam and not yet received (C-19 addendum). | C |
| HPSMPOC-32 | [WS4-2] Rules loader + ruleset-version stamping | Backlog | P | Loader plus stamp in PRs #2 and #10. The version is stored: `Entities.cs:75 RulesetVersion`, `AssessmentApiTests.cs:50 Creation_stamps_the_content_and_ruleset_immutably`. **Left:** the version is **not shown in the report**. `ReportModelBuilder.cs:309-310` prints the ruleset title and approval status only. B14 F-07/F-41 removed `id@version` on purpose (`ReportModelTests.cs:71-82`). Add a plain-words "Rules version 0.1.0" line. | A / S / Claude |
| HPSMPOC-33 | [WS4-3] Scoring overall/domain, current/target | Backlog | **DONE** | PRs #2, #12. `Rules.Tests/Golden/GoldenTests.cs:18 Fixture_is_byte_identical_to_the_oracle` (172 goldens, 0 divergences, comment 38166); `PropertyTests.cs:19 Scoring_is_deterministic…`; `TargetAndNextEngagementTests.cs:47 Static_target_is_the_sme_target_per_scored_section`. The weights are SME content (31). | — |
| HPSMPOC-34 | [WS4-4] Findings with severity, evidence, rationale, recommendation, source rule | Backlog | **DONE** | PRs #2, #8, #12, #19. `FindingApiTests.cs:27 Every_finding_of_a_scored_snapshot_comes_with_its_rule_controls_and_recommendations_from_the_stamped_ruleset`; web `FindingDetail.tsx`. The titles are placeholders (C-17), which is tracked in 31. | — |
| HPSMPOC-35 | [WS4-5] Remediation buckets | Backlog | P | Buckets exactly as the SOW has them: `Rules/Engine/Model.cs:89` `["immediate","30-day","60-90-day","ongoing"]`, one action per finding (`PropertyTests.cs:53`). The PDF roadmap has all four (`ReportModelTests.cs:46`). The web roadmap reads the API result (PR #22). **Left:** the AC says "one **approved** remediation", and the remediation text is SME content (31). No code is left (`getRoadmap` stays unimplemented, but the result carries the roadmap). | C |
| HPSMPOC-36 | [WS4-6] Consultant override with audit note | Backlog | P | Prototype-only: the demo customer's override lives in the web session store (`e2e/states.spec.ts:78`). **Left:** the whole product path. `putFindingDisposition` is in `ContractTests.cs:47 NotYetImplemented`. That means an API with note plus audit, the original outcome kept visible, and web wiring for API customers. SOW §3.1 forbids severity edits (X-13). | A / L / Claude |
| HPSMPOC-37 | [WS4-7] Golden scenarios reconcile to SME results | Backlog | P | The harness plus oracle reconciliation (172/172) is on main (PRs #2, #12). **Left:** the SME's scenarios and expected results (comments 38124/38166). | C |
| HPSMPOC-38 | EPIC WS5 AI & Reporting | Backlog | P | 39, 40, 41 and 42 DONE; 43 PARTLY; 44 NOT STARTED. | D (children) |
| HPSMPOC-39 | [WS5-1] Azure OpenAI behind a provider seam | Backlog | **DONE** | PRs #7, #23 (live, B18: `oai-hpsmpoc-dev-bdn2se`, keyless). `NarrativePipelineTests.cs:131 Configured_azure_call_is_keyless_schema_constrained_and_carries_only_the_allow_list`; `AzureCredentialTokenSourceTests.cs:33`. There is no chat surface. | — |
| HPSMPOC-40 | [WS5-2] Prompt templates, versioned; prompt + model stored per output | Backlog | **DONE** | PRs #7, #25, #26 (1.0.1 approved, C-26). `ReviewAndTemplateTests.cs:186 A_silently_edited_template_is_refused_at_load`. Per-output `PromptTemplateId/Version/Hash`, `Provider`, `ModelDeployment` are at `Entities.cs:180-184`. The model is identified by its pinned deployment (AD-14, NoAutoUpgrade). | — |
| HPSMPOC-41 | [WS5-3] Human review before report | Backlog | **DONE** | PRs #7, #8, #22. `PdfReportGoldenTests.cs:159 Narrative_fallback_is_used_and_declared_when_the_narrative_is_not_approved`; review endpoint `ReportingEndpoints.cs:212-247`; web review in `ApiNarrative.tsx`. | — |
| HPSMPOC-42 | [WS5-4] AI failure logged + deterministic fallback | Backlog | **DONE** | PRs #7, #8, #25. `NarrativePipelineTests.cs:167 Provider_failures_map_to_05_error_codes_and_never_throw`; the fallback PDF is proven by the same `PdfReportGoldenTests.cs:159`; the F2 lookup is at `ReportingEndpoints.cs:183-200`. | — |
| HPSMPOC-43 | [WS5-5] Executive PDF, nine sections, in Blob | Backlog | P | Nine sections, write-once with sha256 (PRs #7, #8; comment 38139). **Left:** no Blob adapter. The only `IReportStore` is `FileReportStore` (`Reporting/ReportingIntegration.cs:28`), and the Azure.Storage SDK is absent. The branding decision is HPSMPOC-21. | A / M / Claude |
| HPSMPOC-44 | [WS5-6] Report language and disclaimers approved | Backlog | NS | The methodology and disclaimer text is placeholder (B15 POC-P02). | C |
| HPSMPOC-45 | EPIC WS6 HP/HPSM Recommendation | Backlog | P | 49 DONE; 47 and 48 PARTLY; 46 NOT STARTED. | D (children) |
| HPSMPOC-46 | [WS6-1] Approved HP/HPSM examples | Backlog | NS | `Reporting/Content/hpsm-guidance.synthetic.json` is placeholder. | C |
| HPSMPOC-47 | [WS6-2] Finding → HP/HPSM mapping config | Backlog | P | Mechanism on main: `HpsmOutputBuilder.cs`, `HpsmMutationTests` (PR #7; comment 38140). **Left:** the AC asks for "approved recommendations", and the config is synthetic. It needs 46's content; no code is needed. | C |
| HPSMPOC-48 | [WS6-3] Recommendation view + report section | Backlog | P | Web `RecommendationScreen.tsx` (PRs #3, #22, #28) and PDF section 6 (`ReportModelTests.cs:58`). **Left:** "implementation-ready" is not met while the guidance prints "Placeholder guidance: the wording is not yet approved". This waits on 46. | C |
| HPSMPOC-49 | [WS6-4] No-device-change guard + disclaimer | Backlog | **DONE** | PRs #7, #22. `PdfReportGoldenTests.cs:114 HPSM_section_says_recommendation_only_no_live_device_change_on_the_section_and_on_every_item`; `HpsmOutputTests.cs:50 A_recommendation_not_marked_noDeviceChange_is_refused`; web `RecommendationScreen.tsx:47`. The only outbound HTTP client in `api/src` is Azure OpenAI (`ReportingModule.cs:37`). | — |
| HPSMPOC-50 | EPIC WS7 Metrics & Commercial | Backlog | P | 54 DONE; 51, 52 and 53 PARTLY; 55 NOT STARTED. | D (children) |
| HPSMPOC-51 | [WS7-1] Manual baseline + metric definitions | Backlog | P | Definitions M1–M7 drafted (`design-pack/07_metrics-instrumentation.md`, PROPOSED). **Left:** baseline hours with their source; approved definitions. The API returns `baseline = null` (`ReportingEndpoints.cs:446`). | B |
| HPSMPOC-52 | [WS7-2] Instrument time, effort, findings, overrides, report time | Backlog | P | `usage_event` plus `MetricsCalculator` (`MetricsTests.cs:66`); `GET /assessments/{id}/metrics` is wired in the web (`ApiSteps.tsx:128`). **Left:** the manual-override metric cannot be captured until override exists. Kam has to confirm T_idle/T_last (QA-129). | D: HPSMPOC-36 |
| HPSMPOC-53 | [WS7-3] Automation metrics dashboard | Backlog | P | Per-assessment metrics view (`ApiMetrics`). **Left:** `getMetricsSummary` is NotYetImplemented (`ContractTests.cs:47`); there is no cross-run view. The baseline column stays blank until 51. | A / M / Claude |
| HPSMPOC-54 | [WS7-4] Rule-based next engagement | Backlog | **DONE** | PRs #2, #7, #22. `TargetAndNextEngagementTests.cs:65 Worked_example_recommends_SVC_91_with_the_numbers`; PDF `ReportModelTests.cs:42` ("Recommended next engagement: …"); the workspace screen reads the API result. The preview/PDF mismatch F-40 is GONE (B22 STATUS). The catalogue is placeholder. | — |
| HPSMPOC-55 | [WS7-5] Trial runs and metrics output | Backlog | NS | Nothing yet. It needs SME trial runs and the baseline (51). | C |
| HPSMPOC-56 | EPIC WS8 DevOps, QA & Event | Backlog | P | 57, 58, 59 and 60 PARTLY; 61–64 NOT STARTED. | D (children) |
| HPSMPOC-57 | [WS8-1] Dev/UAT/Demo via IaC, Key Vault, App Insights | Backlog | P | `infra/main.bicep` plus modules (PR #4). Only the AOAI subset, App Insights and Log Analytics are deployed (B18 STATUS). **Left:** three environments deployed, Key Vault, and the App Insights SDK in code (none in `api/src` or `web/package.json`). Six providers are still NotRegistered (B18 STATUS l.55). | D: Kam registers providers (C-13 azure-providers: a) |
| HPSMPOC-58 | [WS8-2] CI/CD, branch protection, review | Backlog | P | CI in PR #1. Branch protection is set as ruled (C-13: PR + green CI, 0 approvals). **Left:** auto-deploy to Dev/UAT. `.github/workflows/ci.yml:1` says "No deploy job". | D: HPSMPOC-57 |
| HPSMPOC-59 | [WS8-3] Security scans + OWASP review | Backlog | P | CodeQL (default setup) and Dependabot alerts are on (B15 ADDENDUM-3). **Left:** no `dependency-review-action` or `npm audit` in `ci.yml`; secret scanning OFF; the OWASP/ASVS review not run against the built code (the drafts assume a BFF/CSRF that is not built). | A / M / Claude |
| HPSMPOC-60 | [WS8-4] Playwright happy path of event journey | Backlog | P | `web/e2e/journey.spec.ts` times the 14-span journey under 7:00, but on the prototype demo customer, locally. **Left:** a run in UAT and Demo (none exist); the journey re-based on the final script. | D: HPSMPOC-57, -12 |
| HPSMPOC-61 | [WS8-5] UAT execution + defect triage | Backlog | NS | There is no UAT. | D: HPSMPOC-57 (+ SME time) |
| HPSMPOC-62 | [WS8-6] Freeze Demo, fallback customer, restart, rehearsal | Backlog | NS | Precursors only: showcase seed/reset (`ShowcaseResetTests`), `scripts/showcase.sh`. No Demo environment. | D: HPSMPOC-57, -12 |
| HPSMPOC-63 | [WS8-7] Event-day on-call, handover docs, Phase 2 backlog | Backlog | NS | M8. Only the READMEs exist; no admin guide. | D: the event (1 Dec) / M8 |
| HPSMPOC-64 | [WS8-8] 30-day hypercare | Backlog | NS | Post-event. | D: the event (1 Dec) |

## Missing from the board (for Friday; no tickets were created)
- There is no ticket for the **C-12 minimum**, the digitised Playbook deck: 5 of 6 modules are placeholders (B15 POC-D01/D02). This is the largest gap, and nothing on the board carries it.
- There is no ticket for **C-27 showcase labelling / findings order / auto-citation** (built in PRs #31, #32) or for the B23 validator (#27). This was work with no ticket.
- There is no ticket for the **partner readiness 16-question flow and action plan** (C-14/C-18, PRs #9–#21). That is the main delivered scope, and it maps to no HPSMPOC issue.
- There is no ticket for **GDPR subject requests** (`exportUserPersonalData`/`eraseUserPersonalData` NotYetImplemented) or for **demo reset in the API** (`resetDemoData` NotYetImplemented).

## UNMEASURED
- Nothing was built or run. Test names were read statically at `33abe1a`, so their pass state rests on the merged PRs' green CI and was not re-run here.
- Current Azure state was not queried; B18's STATUS is the source.
- Whether Kam reviewed the demo script, the prototype or the design pack outside the recorded channels. No record was found in CLARIFICATIONS, STATUS files or Jira comments.
