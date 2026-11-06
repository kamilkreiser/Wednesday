# Feedback sweep, boot s254 (window: created or updated since 2026-11-06 13:05 AEDT)

Read only. Jira cloud `GET /rest/api/3/search/jql`, every JQL `project = <KEY> AND (...)`, paged to `isLast`. Each project's own `4_Credentials/.env` read in-process (JIRA_SITE or JIRA_BASE_URL variants handled by name), no token printed. Mail: list of `tuesday-agent@agentmail.to` only. No HTTP to any hosted site. Method and filter F as in [[2026-11-06_feedback-sweep-boot-s248]]. F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`. No project reader scripts were used; one session-only Python script in the scratchpad.

## BLUF

**0 new user feedback across all six Datasec Jira projects and the tuesday-agent inbox since 13:05 AEDT.** 50 issues were created in the window, all by our own records/gate seats, so none is user feedback. Two F hits in the window are false positives (RD-958, HPSMPOC-308).

## Per project

| Project | Created in window | Created or updated in window | F in window | Positive control (F, no date) | Total issues / newest | New feedback |
|---|---|---|---|---|---|---|
| HPSM | 0 | 0 | 0 | 0 (weak instrument, as in s248) | 41 / HPSM-41 (unchanged) | 0 |
| NexusAI (RD) | 47 (RD-925..971) | 63 | 1 (RD-958) | 22 (fires; s248 had 21, RD-958 is the +1) | 967 / RD-971 | 0 |
| Vision Portal (VSP) | 0 | 0 | 0 | 1 (VSP-88, as before) | 89 / VSP-89 (unchanged) | 0 |
| HPSM-POC | 2 (HPSMPOC-446, 447) | 10 | 1 (HPSMPOC-308) | 43 (fires; same as s248) | 447 / HPSMPOC-447 | 0 |
| Security Composer (PCOMP) | 0 | 0 | 0 | 0 (no feedback label or word in project; weak instrument) | 127 / PCOMP-127 (unchanged) | 0 |
| MPS (MPSCALC) | 1 (MPSCALC-385) | 11 | 0 | 17 (fires; same as s248) | 385 / MPSCALC-385 | 0 |

Zeros: HPSM, VSP and PCOMP rest on frame equality with s248 (same total and newest key) plus an empty window. RD, HPSMPOC and MPSCALC windows are visibly non-blind (47, 2 and 1 new issues appear) and their F positive controls fire.

## Excluded as our own records seats' tickets (not user feedback)

50 created-in-window issues excluded: RD 47, HPSM-POC 2, MPS 1.
- RD-925/926 (b1323-finding, b1337-2026-11-06); RD-927..958 (b1341-2026-11-06, roles-ui-2026-11); RD-959..971 (b1353-2026-11-06, several also roles-ui-2026-11).
- HPSMPOC-446/447 (b1349-2026-11-06); MPSCALC-385 (mpscalc-b1355).
- Control key: RD-962, labels `b1353-2026-11-06, roles-ui-2026-11`, summary "settings.html is 60 px wider than the viewport at 390 px width" - a QA finding, not a user report.
- Updated-only hits (13 RD, 8 HPSMPOC, 10 MPSCALC) are old gate/CodeQL/records tickets touched in bulk tonight; none created in window.
- F false positives: RD-958 (summary mentions "feedback" settings as a route a viewer can change; labels b1341/roles-ui/security) and HPSMPOC-308 (CI shard named "api-other-and-feedback", label b399-gate). Neither is a user report.

## Mail (`tuesday-agent@agentmail.to`, subject/sender/timestamp)

Rows since 2026-11-06T02:05Z: 1. `2026-11-06T02:58:57Z | Wednesday <wednesday-agent@agentmail.to> | [Wednesday -> Tuesday] panel_sync: chat streams and ack_state now union on conflict` - a coordinator FYI, not feedback. Page of 30 reached the head (newest is this row). I did not run a /feedback/i control on the page this time, so the mail zero rests on this one-row window.

## Could not read / UNMEASURED

Live in-app stores (QuickQuote Azure Table, Vision Postgres feedback table, NexusAI `feedbackItems`, HPSM-POC Admin feedback store, HPSM Policy Composer store), and feedback filed in Jira without the word feedback or a feedback label (F cannot see it; the all-created counts above are the control). Jira's window time was interpreted in the API user's timezone, not verified as AEDT; the created-in-window sets (RD-925 onward at 16:17 UTC-shown times) are consistent with tonight's records, so the edge risk is low. Everything was readable.
