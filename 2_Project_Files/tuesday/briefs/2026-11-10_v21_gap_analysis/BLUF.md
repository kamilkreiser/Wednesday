# BLUF: v2.1 HTML and alignment document against main `6b0c5f2c`

For the coordinator. 10 November 2026. Read-only analysis: nothing built, ticketed, deployed or sent.

## What was produced

- `DECISION-DOCUMENT.md`: 85 numbered changes (D-001 to D-085) for the product owner and the deputy to decide one at a time.
- `GAP-LIST.md`: 126 gaps (G-001 to G-126) with HTML and site evidence, file and line.
- `UAT-SCENARIOS.md`: 387 scenarios judged against main.
- This file.

## Counts

**Decision items: 85.** Recommended this phase 24, next phase 55, drop 6.

| Recommendation | S | M | L | Total |
|---|---|---|---|---|
| THIS PHASE | 16 | 8 | 0 | 24 |
| NEXT PHASE | 18 | 21 | 16 | 55 |
| DROP (keep the site as it is) | 6 | 0 | 0 | 6 |

- Needing HP SME content before they can be finished: 10 (D-003, D-004, D-005, D-006, D-008, D-011, D-012, D-013, D-075, D-076).
- Needing wording or a content choice from the product owner: 11 (D-007, D-009, D-022, D-023, D-027, D-030, D-037, D-047, D-056, D-069, D-079).
- Behind a change request by the alignment document's own rule (P2, P3): 5 (D-020, D-024, D-025, D-026, D-029).
- Decision items by document priority: P0 12, P1 5, P2 4, P3 1, none 63.

**Gaps: 126.** 79 restate the earlier layout catalogue (P2-001 to P2-096, already filed as HPSMPOC-449 to HPSMPOC-460) against today's main; 47 are new in this pass.

| | layout | content | behaviour | data model | Total |
|---|---|---|---|---|---|
| P0 | 0 | 7 | 4 | 1 | 12 |
| P1 | 1 | 3 | 1 | 1 | 6 |
| P2 | 3 | 0 | 1 | 7 | 11 |
| P3 | 0 | 0 | 0 | 1 | 1 |
| none | 30 | 44 | 6 | 16 | 96 |
| Total | 34 | 54 | 12 | 26 | 126 |

**Scenarios against main**

| Set | Total | met | partly | not met | needs content | out of scope (change request) |
|---|---|---|---|---|---|---|
| Document release suite UAT-01..20 | 20 | 4 | 10 | 2 | 3 | 1 |
| v2.1 tracker functional UAT-001..285 | 285 | 109 | 26 | 60 | 6 | 84 |
| v2.1 tracker non-functional | 38 | 8 | 20 | 4 | 1 | 5 |
| v2.1 tracker production gates | 32 | 1 | 10 | 14 | 1 | 6 |
| v2.1 plan end-to-end journeys | 12 | 1 | 3 | 3 | 0 | 5 |

## The five most important changes, in plain words

1. **Decide which 16-question set is the base (D-001).** Three different sets of 16 questions are in play. Nothing at question level can move until one is named.
2. **Correct the firmware update question and its recommendations (D-004).** With D-005 and D-007: the firmware and trusted-startup wording a reseller has already challenged, and the automatic 30-day date. All P0.
3. **Treat "Unsure" as something to verify, not as a failed control (D-009).** An "Unsure" answer is scored and reported as a failed control today.
4. **Let the assessor record and change how each answer is known (D-010).** Every typed answer is recorded and printed as "stated by the customer" and cannot be changed. Rated Critical by the reseller reviewer; the record already has the field.
5. **Opportunity register and pipeline (deals separate from assessments) (D-024).** With D-025, D-026 and D-043: the commercial layer is the largest part of the HTML (deals, quotes, contracts, attribution, a new dashboard). The document rates it P2, which by its own rule needs a change request.

## Findings the product owner may not expect

- **The HTML is not the question set the reseller reviewed.** The reviewer's question numbers (1 trusted startup, 2 firmware updates, 9 inventory, 11 and 12 sign-in and roles, 13 certificates) match the site's on-screen order one for one. The HTML has its own, different 16 questions; the alignment document says so in section 3. Copying the HTML's questions would not answer the review.
- **The v2.2 demo was not supplied.** The document says the revised questions, six answer states, narrative revisions, report contents and three reseller modes are implemented in a v2.2 standalone demo. Only v2.1 and v2.0 were attached. The revised question wording exists nowhere in the inputs.
- **The site is ahead of the HTML in several places** (Playbook module text, findings review with audit notes, narrative and PDF report, measured metrics, revenue calculator). 6 items recommend keeping the site.
- **Most of the assessment content on both sides is unapproved.** The HTML labels its questions, findings, mappings, tiers and offers as draft; the site labels its own as draft for HP to vet. "Most accurate" needs naming section by section (D-081).
- **The v2.0 HTML adds nothing new.** Its guided demo is already the site's Demo Walkthrough (14 of 14 step titles); its screens are an earlier layer of v2.1.
- **The v2.1 UAT pack tests the HTML, not the site.** Run against the site, 109 of 285 functional cases are met; most of the rest are pages that do not exist yet (D-084).

## Risks

- **Question-number migration (the document's "material data-integrity risk").** How the site stores answers: one row per assessment and question id, and every assessment is stamped with the content package id, version and hash and the ruleset id, version and hash it was answered under (`api/src/HpsmPoc.Modules.Assessment/Persistence/Entities.cs:61-78, 107-113`). Versions are never edited in place. So a re-sequenced or revised set, shipped as a new version, does not touch existing assessments: UAT assessments already recorded keep the old questions, order and scores, and only new assessments use the new set. The risk is real in three narrower ways: (1) if a new set reused the existing ids (Q-CS-01…) with new meanings, reports and exports that join on the id would mislabel; new ids avoid it, as was done for readiness on 9 November; (2) on-screen numbers change, so every earlier review comment that cites "question 9" points at a different question afterwards; (3) scores from the old and new sets are not comparable, and an assessment in progress stays on the old set. The stored UAT data itself was not inspected (no hosted host was contacted), so how many assessments exist there is not known here.
- **Invented security content.** 10 items need wording that is in neither source. The product owner's ruling of 10 November has an agent draft such content for his review, marked as draft and not loaded until approved; nothing in these files should be loaded as content.
- **Scope.** The commercial layer is P2 in the document, which the document itself puts behind an approved change request. Building it without one would be outside the agreed commitments.
- **Running UAT.** Menu renames, the product name and the visual rebuild would change what testers see mid-review and invalidate the UAT guide; they are recommended for the next phase for that reason.
- **A Customer sign-in** is a security change (per-customer isolation on the server), not a layout change.
- **Two earlier rulings are reversed by the HTML** if adopted: one banner per page, and no Good / Better / Best menu entry. The three-phase panel on Home, which the product owner asked for, is absent from the HTML dashboard.

## Suggested order for the sitting

Decide these five first, because the others depend on them: D-081 (ask which sections of the html hold "the most accurate content"), D-082 (ask for the v2.2 demo that the alignment document describes), D-001 (decide which 16-question set is the base), D-084 (decide what the v2.1 uat pack is for), D-083 (adopt the document's 20 scenarios as the acceptance test for this phase's items). Then section A (assessment content) and section B (narrative and report), which hold every P0 item. Then C to G in order; most of those are a single ruling each ("next phase, with the layout epic").

## What was not verified

- The hosted UAT site and its data: not contacted. The comparison is against a local build of the same commit in mock mode.
- The live customer journey on screen with the real 16 questions: the mock build shows placeholder questions; live content was read from files.
- Non-functional and production-gate verdicts: read from source and the repository's own test description, not re-run.
- The readiness result page (bands and 30-day plan) was not reached in the local walk.
- Whether the security content in the HTML or the document is correct: not judged.

## Local servers

One web server was started on 127.0.0.1:9861 for the walk and stopped at the end; ports 9860 to 9869 are at 0 listeners (checked with `lsof`). **One slip to know about:** the stop command matched any process named `next-server` on the machine, not only the one on port 9861, so if another seat had a local Next.js server running at 14:10 it was stopped too and needs restarting. Dependencies for the local build were installed from the public npm registry into the session scratchpad (the project folder's installed packages were for an older commit).
