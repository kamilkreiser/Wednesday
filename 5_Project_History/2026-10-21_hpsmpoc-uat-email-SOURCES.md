# Sources for the UAT email to Kam (2026-10-21)

B410 = /Volumes/Laptop-DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-21_B410_STATUS.md
UatStartScreen = git show ae7a2c860a5e909b3430dadeacf1985c7142e4da:web/src/components/screens/UatStartScreen.tsx
Register = /Volumes/Laptop-DEV/TUESDAY/0_Brain/projects_index/clarifications_register.md
Readiness = /Volumes/Laptop-DEV/TUESDAY/0_Brain/projects_index/2026-10-21_hpsmpoc-hp-review-readiness.md

| Email sentence | Source |
|---|---|
| Subject line | NEW wording (title). Plain description of the link and levels. |
| "Here is the review copy of the HP Security Services Playbook" + link | NEW plain factual sentence. Link: B410 last line (DEPLOYED). Product name from the approved heading. |
| "There is no sign-in. The start page asks you to choose a level." | NEW plain factual sentence. Fact: Register line 28 (14:41 "Anyone with a link can access the site"); UatStartScreen:3-5, 46. |
| Heading and lead sentence | Card hpsmpoc-uat-start-page-words-1021 (ruled a, 15:12:54); UatStartScreen:46. Verbatim, match. |
| Four level bullets | Card bluf; UatStartScreen:20-23. Verbatim, match (the card's bluf gives the text after "Partner: " etc.; the source prefixes the level name). |
| "After you choose, the page names your level: ..." (four labels) | Labels verbatim from B410:526-529 and B410:605 (approved 18:19). The lead-in sentence is NEW wording. |
| "If you try something that is switched off, you will see: ..." | Quote: card bluf (blocked action sentence). Lead-in is NEW wording. |
| "Some pages carry content still awaiting approval. Each is marked DRAFT" | Card hpsmpoc-draft-content-show-or-hide-1021 (a, 14:43:30): "show it, each marked DRAFT once per page; the cover note lists them." Sentence is NEW wording. |
| The four DRAFT topics | Tickets HPSMPOC-87, -162, -168, -91 named by the card; topic names condensed from Readiness lines 80, 82, 94, 100. NEW customer-facing wording; Tuesday to decide. Actual page names are NOT established. |
| "Guided remediation and HP recommendations ... wait on content from HP first" | Card hpsmpoc-hp-content-gaps-tell-hp-1021 (a, 14:42:55); tickets -94, -47, -48 (Readiness lines 61, 62, 84). NEW wording. Ticket keys left out. |
| Levels in "for you" (reach) | B410:524-531 (level table). |
| Five refusals | B410:534-541 (reset demo, erase personal data, view personal data, reset showcase, delete customer). |
| Feedback saved, not sent to Jira | B410:569 and card hpsmpoc-uat-start-page-words-1021 bluf. |
| Telemetry not on | B410:561, 636; HPSMPOC-224 at B410:188. |
| About A$121 a month; scale-down is his call | B410:636 (A$121/month). "His call" is from this task's brief; no card was read for it. |
| Synthetic data only, one test feedback item | B410:625, 572. |
| Nothing reaches HP until he forwards | Card hpsmpoc-uat-start-page-words-1021 option a detail. |

## Could not establish
- The dates HP needs to supply content by. The card says "with the dates HP needs to supply", but no card or file I read gives them. Readiness line 181 repeats the same phrase with no dates. Only HPSMPOC-5 (event date 1 Dec) appears, which is not a supply date. Flagged to Kam in the email.
- Names of the DRAFT pages. Only the four tickets are named.
- Whether the cover note is wanted as a separate document: card hpsmpoc-hp-cover-note-refresh-1021 (a) says draft it for him; this email carries the content, not the refreshed 8 Oct document.

## Deliberately left out
- Card hpsmpoc-hosted-demo-data-cleanup-1021 (ruled c, leave as they are): its option c text says the cover note should mention a hand-entered customer and internal feedback. That is the DEMO's data. UAT holds synthetic seed data only (B410:625, 510), so I did not claim it of UAT and put nothing about it in the email.
- No seat numbers, gate ids, brief ids, person names. Ticket key HPSMPOC-224 appears only in the "for you" section.

## Counts
Forwardable part (greeting to "wait on content from HP first"): about 245 words including the link, bulleted text and quotes; it should be re-counted by Tuesday if edited.
