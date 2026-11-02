# Feedback sweep, boot s226: Jira half (2026-11-02)

Read only; Jira REST `POST /rest/api/3/search/jql` only, paginated (maxResults 100, nextPageToken to isLast), each project's own `4_Credentials/.env` loaded in-process, no token printed. Method, scope, exclusions, table and controls copied from [[2026-11-02_feedback-sweep-boot-s225]]. Script: `sweep.py` (same as s225). Window `created >= "2026-11-02"`. Excluded: HPSM-POC, Security Composer, MPS Calculator.

## BLUF

**0 new feedback-shaped issues in HPSM, RD, VSP. All totals UNCHANGED from s225** (HPSM 41, RD 919, VSP 89). Controls matched. Vision QuickQuote has no Jira: UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame | Negative control | All created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same) | 41 (newest HPSM-41) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest) | 919 (newest RD-923) | 0 | 9 (RD-915..923) |
| Vision Portal | VSP | **0** | 1 (VSP-88) | 89 (newest VSP-89) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

## New items since s225

None. RD-915..923 are the known internal QA/records findings.

## UNMEASURED

Vision QuickQuote (no Jira); live in-app stores (fenced); Vision Portal #6 still unticketed; window is date-granular.
