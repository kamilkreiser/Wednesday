# HPSMPOC close list: DONE on main 33abe1a

**Generated:** 2026-09-27 08:47:08 AEST. This file is read-only analysis. Nothing has been posted or transitioned.

**Counts:** 10 DONE and 0 DUPLICATE. Every row below has a ready-to-post comment. Line references are at `33abe1a6c17f0250f771b3c5d03b91210a0d0621`.

**Content caveat.** Several of these tickets close the machinery only. Where the content is placeholder, the SME/HP content ticket stays open and is named in the comment.

| Key | Summary | PRs | Proof |
|---|---|---|---|
| HPSMPOC-25 | Customer workspace | #8, #19, #22 | `AssessmentApiTests.cs:273` |
| HPSMPOC-27 | Guided assessment runner | #8, #9, #12, #15 | `AssessmentApiTests.cs:124` |
| HPSMPOC-33 | Scoring | #2, #12 | `GoldenTests.cs:18` |
| HPSMPOC-34 | Findings | #2, #8, #12, #19 | `FindingApiTests.cs:27` |
| HPSMPOC-39 | Azure OpenAI seam | #7, #23 | `NarrativePipelineTests.cs:131` |
| HPSMPOC-40 | Prompt templates | #7, #25, #26 | `ReviewAndTemplateTests.cs:186` |
| HPSMPOC-41 | Human review gate | #7, #8, #22 | `PdfReportGoldenTests.cs:159` |
| HPSMPOC-42 | AI failure + fallback | #7, #8, #25 | `NarrativePipelineTests.cs:167` |
| HPSMPOC-49 | No-device-change guard | #7, #22 | `PdfReportGoldenTests.cs:114` |
| HPSMPOC-54 | Next engagement | #2, #7, #22 | `TargetAndNextEngagementTests.cs:65` |

---

### HPSMPOC-25: [WS3-2] Customer workspace: create, select and status view
## BLUF
Done on main `33abe1a`. You can create or select a customer. The customer list shows status, score, priority risks and the next service.
## Recommendation
Close as Done.
## Detail
- **API:** create (synthetic only), get, update, soft delete and a scoped list are in https://github.com/datasecau/HPSM-POC/pull/8.
- **Web:** the customer management screen is in https://github.com/datasecau/HPSM-POC/pull/19. It reads each customer's own result since https://github.com/datasecau/HPSM-POC/pull/22.
- **Proof:** `api/tests/HpsmPoc.Api.Tests/Assessment/AssessmentApiTests.cs:273` `Lists_show_status_score_risks_and_the_next_service`, and `CustomerApiTests.cs:15` `Create_returns_201_with_location_etag_owner_and_a_uuid_v7_id`.

---

### HPSMPOC-27: [WS3-4] Guided assessment runner with persistence
## BLUF
Done on main `33abe1a`. The runner has sections, question types, conditional follow-ups, not-applicable answers, notes, evidence references, save-as-you-go with ETags, resume, submit and a lock after submit.
## Recommendation
Close as Done. The real customer questions are content, not code. They stay open on HPSMPOC-31. Until an approved ruleset exists, a live snapshot submit is refused outside showcase mode (C-15, C-19).
## Detail
- **Delivered in:**
  - https://github.com/datasecau/HPSM-POC/pull/8 (API)
  - https://github.com/datasecau/HPSM-POC/pull/9 (web runner)
  - https://github.com/datasecau/HPSM-POC/pull/12 (not-applicable handling)
  - https://github.com/datasecau/HPSM-POC/pull/15 (live API)
- **Proof:**
  - `api/tests/HpsmPoc.Api.Tests/Assessment/AssessmentApiTests.cs:124` `A_conditional_follow_up_appears_and_a_hidden_question_cannot_be_answered`
  - `:159` `Evidence_is_registered_as_ev_nnn_and_can_then_be_referenced`
  - `:203` `After_submit_answers_are_locked_409_and_a_retried_submit_returns_the_same_result`
  - Notes and evidence refs are persisted on `ResponseRecord` (`Persistence/Entities.cs:107-117`).

---

### HPSMPOC-33: [WS4-3] Scoring: overall and domain, current and target
## BLUF
Done on main `33abe1a`. Scoring is deterministic and rule-based, with no AI. It produces section and overall scores, current and target values, and bands, and each score can be traced to its answers.
## Recommendation
Close as Done. The weights are SME content, tracked on HPSMPOC-31. Reconciling to the SME's own expected results stays on HPSMPOC-37.
## Detail
- **Delivered in:** https://github.com/datasecau/HPSM-POC/pull/2 (engine) and https://github.com/datasecau/HPSM-POC/pull/12 (not-applicable ruling C-15).
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Rules.Tests/Golden/GoldenTests.cs:18` `Fixture_is_byte_identical_to_the_oracle` (172 goldens, 0 divergences from the reference scorer)
  - `PropertyTests.cs:19` `Scoring_is_deterministic_across_repeated_runs_and_fresh_loads`
  - `Engine/TargetAndNextEngagementTests.cs:47` `Static_target_is_the_sme_target_per_scored_section`

---

### HPSMPOC-34: [WS4-4] Findings with severity, evidence, rationale, recommendation and source rule
## BLUF
Done on main `33abe1a`. Every finding stores its originating responses and its source rule. The API and the finding-detail screen show severity, evidence, recommendation and source rule.
## Recommendation
Close as Done. The finding wording is placeholder (C-17). The real wording is SME content on HPSMPOC-31.
## Detail
- **Delivered in:**
  - https://github.com/datasecau/HPSM-POC/pull/2 (engine)
  - https://github.com/datasecau/HPSM-POC/pull/8 (finding endpoint)
  - https://github.com/datasecau/HPSM-POC/pull/12 (not-applicable)
  - https://github.com/datasecau/HPSM-POC/pull/19 (finding-detail screen)
- **Proof:** `api/tests/HpsmPoc.Api.Tests/Assessment/FindingApiTests.cs:27` `Every_finding_of_a_scored_snapshot_comes_with_its_rule_controls_and_recommendations_from_the_stamped_ruleset`.

---

### HPSMPOC-39: [WS5-1] Azure OpenAI integration behind a provider seam
## BLUF
Done on main `33abe1a`. The narrative goes through a provider seam. There is a deterministic default and a keyless Azure OpenAI provider, which is live on the project's own Azure OpenAI resource. Only allow-listed structured findings are sent. There is no chat surface.
## Recommendation
Close as Done.
## Detail
- **Seam and provider:** https://github.com/datasecau/HPSM-POC/pull/7.
- **Keyless token source and live connection:** https://github.com/datasecau/HPSM-POC/pull/23 (C-22).
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Reporting.Tests/Narrative/NarrativePipelineTests.cs:131` `Configured_azure_call_is_keyless_schema_constrained_and_carries_only_the_allow_list`
  - `AzureCredentialTokenSourceTests.cs:33` `An_endpoint_without_a_credential_fails_closed_with_no_call`

---

### HPSMPOC-40: [WS5-2] Prompt templates for executive summary, finding explanation and remediation narrative
## BLUF
Done on main `33abe1a`. The three templates are versioned and hash-pinned in `Prompts/registry.json`. Version 1.0.1 is approved (C-26). Every stored narrative records its template id, version and hash, its provider and its model deployment.
## Recommendation
Close as Done. Any change to template text makes a new version, which needs approval again (ADR-R04).
## Detail
- **Delivered in:**
  - https://github.com/datasecau/HPSM-POC/pull/7 (templates and registry)
  - https://github.com/datasecau/HPSM-POC/pull/25 (1.0.1 proposed)
  - https://github.com/datasecau/HPSM-POC/pull/26 (1.0.1 approval recorded)
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Reporting.Tests/Narrative/ReviewAndTemplateTests.cs:186` `A_silently_edited_template_is_refused_at_load`
  - Per-output fields at `api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs:180-184`. The model is identified by its pinned deployment (AD-14, no auto-upgrade).

---

### HPSMPOC-41: [WS5-3] Human review step before report generation
## BLUF
Done on main `33abe1a`. A narrative can be approved, edited (text plus note) or rejected (note), and every review is audited. The report uses only approved or edited text. Anything unreviewed, rejected or failed falls back to the deterministic text, and the report says so.
## Recommendation
Close as Done.
## Detail
- **Review rules and report selector:** https://github.com/datasecau/HPSM-POC/pull/7.
- **Review endpoint:** https://github.com/datasecau/HPSM-POC/pull/8.
- **Web review on API customers:** https://github.com/datasecau/HPSM-POC/pull/22.
- **Proof:** `api/tests/HpsmPoc.Modules.Reporting.Tests/Pdf/PdfReportGoldenTests.cs:159` `Narrative_fallback_is_used_and_declared_when_the_narrative_is_not_approved`. The endpoint is at `ReportingEndpoints.cs:212-247`.

---

### HPSMPOC-42: [WS5-4] Log AI generation status and failures, with a deterministic fallback
## BLUF
Done on main `33abe1a`. Every AI failure is stored and logged with an error code, and prompt text is never logged. Failures covered: timeout, throttling, unavailable, content filter, validation, not configured, and template not approved. The report still builds from the structured findings.
## Recommendation
Close as Done.
## Detail
- **Delivered in:**
  - https://github.com/datasecau/HPSM-POC/pull/7 (pipeline)
  - https://github.com/datasecau/HPSM-POC/pull/8 (stored failures and the F2 fallback)
  - https://github.com/datasecau/HPSM-POC/pull/25 (retry and "Try again")
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Reporting.Tests/Narrative/NarrativePipelineTests.cs:167` `Provider_failures_map_to_05_error_codes_and_never_throw`
  - `PdfReportGoldenTests.cs:159` (the report falls back to deterministic text)

---

### HPSMPOC-49: [WS6-4] 'No production device change' guard and disclaimer
## BLUF
Done on main `33abe1a`. A recommendation not marked no-device-change is refused. "Recommendation only — no live device change." prints on the PDF section and on every item, and the web view shows "No device is changed". No code path writes to a device: the only outbound HTTP client in the API is the Azure OpenAI one.
## Recommendation
Close as Done. The wording can be swapped for the approved disclaimer when HPSMPOC-44 lands.
## Detail
- **Delivered in:** https://github.com/datasecau/HPSM-POC/pull/7 (guard and PDF) and https://github.com/datasecau/HPSM-POC/pull/22 (web view on API customers).
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Reporting.Tests/Pdf/PdfReportGoldenTests.cs:114` `HPSM_section_says_recommendation_only_no_live_device_change_on_the_section_and_on_every_item`
  - `Hpsm/HpsmOutputTests.cs:50` `A_recommendation_not_marked_noDeviceChange_is_refused`
  - `web/src/components/screens/RecommendationScreen.tsx:47`
  - The only HTTP client registration is `api/src/HpsmPoc.Modules.Reporting/ReportingModule.cs:37`.

---

### HPSMPOC-54: [WS7-4] Rule-based next-engagement recommendation
## BLUF
Done on main `33abe1a`. The engine picks the next engagement deterministically and gives its rationale. It appears on the workspace screen and in the PDF's "Next Engagement" section, and the preview and the PDF now agree.
## Recommendation
Close as Done. The service catalogue is still placeholder. Real services and wording are HP/Datasec content.
## Detail
- **Delivered in:**
  - https://github.com/datasecau/HPSM-POC/pull/2 (selector)
  - https://github.com/datasecau/HPSM-POC/pull/7 (PDF section 8)
  - https://github.com/datasecau/HPSM-POC/pull/22 (web reads the API result; the preview/PDF mismatch is fixed)
- **Proof:**
  - `api/tests/HpsmPoc.Modules.Rules.Tests/Engine/TargetAndNextEngagementTests.cs:65` `Worked_example_recommends_SVC_91_with_the_numbers`
  - `api/tests/HpsmPoc.Modules.Reporting.Tests/Report/ReportModelTests.cs:42` (asserts "Recommended next engagement: …")
