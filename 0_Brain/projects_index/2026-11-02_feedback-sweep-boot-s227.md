# Feedback sweep, boot s227: Jira half (2026-11-02)

Read only; Jira REST `POST /rest/api/3/search/jql` only, paginated (maxResults 100, nextPageToken to isLast), each project's own `4_Credentials/.env` loaded in-process, no token printed. Method, scope, exclusions, table and controls copied from [[2026-11-02_feedback-sweep-boot-s226]]. Script: inline, session-only (the s225/s226 `sweep.py` was no longer on disk, so it was re-implemented to the same spec and nothing was written beyond this note). Window `created >= "2026-11-02"` (opens where s226's closed; date-granular). Excluded: HPSM-POC, Security Composer, MPS Calculator.

## BLUF

**0 new feedback-shaped issues in HPSM, RD, VSP. All totals UNCHANGED from s226** (HPSM 41, RD 919, VSP 89). Controls matched s226 exactly. Vision QuickQuote has no Jira: UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same; weaker instrument) | 41 (newest HPSM-41) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest) | 919 (newest RD-923) | 0 | 9 (RD-915..923) |
| Vision Portal | VSP | **0** | 1 (VSP-88) | 89 (newest VSP-89) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

Every JQL is `project = <KEY> AND ( ... )`. Pagination followed to the last page (RD frame 919 assembled across ten pages).

## Compared with s226

No delta in any cell. HPSM 41/41, RD 919/919 (newest RD-923), VSP 89/89. RD-915..923 are the known internal QA/records findings.

## New items since s226

None.

## UNMEASURED

Vision QuickQuote (no Jira); live in-app stores (fenced); Vision Portal #6 still unticketed; window is date-granular, so an item created earlier today and already counted in the frame cannot be told apart from one created since s226 except by the frame delta (delta is zero). HPSM's positive control is 0, so for HPSM the "0 new" rests on the frame count and the empty window, not on a feedback-filter hit.

## Watermark

HPSM and VSP at 2026-11-02; RD at 2026-11-02, newest RD-923.
