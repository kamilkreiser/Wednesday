# Feedback sweep, boot s225: Jira half (2026-11-02)

Read only; Jira REST `POST /rest/api/3/search/jql` only, paginated (maxResults 100, nextPageToken followed to isLast), each project's own `4_Credentials/.env` loaded in-process, no token printed. Method, scope, exclusions, table shape and controls copied from [[2026-11-02_feedback-sweep-boot-s224]] (and s223/s222 it links). Script: session scratchpad `sweep.py` (unchanged from s224). Window `created >= "2026-11-02"`. Excluded: HPSM-POC, Security Composer, MPS Calculator. The VSP key `VSP` was supplied by the script.

## BLUF

**0 new feedback-shaped issues in HPSM, RD and VSP.** HPSM 41 and VSP 89 are UNCHANGED from s224. **RD frame is now 919 (was 915): +4, RD-920..RD-923, all internal records-seat findings, not feedback.** Controls matched s224. Vision QuickQuote has no Jira: UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same; weaker instrument) | 41 (newest HPSM-41) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest) | 919 (newest RD-923) | 0 | 9 (RD-915..923) |
| Vision Portal | VSP | **0** | 1 (VSP-88) | 89 (newest VSP-89) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

Every JQL is `project = <KEY> AND ( ... )`. Pagination followed to the last page; RD frame 919 was assembled across ten pages, not read off a cap.

## New items since s224

None feedback-shaped. New to the frame (RD-920..RD-923), all Task, labels `ai-assistant`, `b1100-finding`, `b1114-2026-11-02`, created 2026-11-02 11:10 +1100:

- RD-920 backend/simpleDb.js insertPrinterLog resolves undefined instead of the new row id
- RD-921 backend/simpleDb.js getAllPrinterLogs builds OFFSET with no LIMIT
- RD-922 scripts/clear_db.js awaits calls on the raw sqlite3 handle that are not promises
- RD-923 docker/docker-compose.yml builds Dockerfiles that do not exist

RD-915..RD-919 are the earlier known internal QA findings (labels `qa-gate-finding`, `b1069-finding`).

## UNMEASURED

Vision QuickQuote (no Jira); live in-app stores (fenced); Vision Portal #6 still unticketed; window is date-granular (so "since s224" is bounded by the day, not the hour; RD-920..923 identified by the frame delta and creation timestamps).

## Watermark

HPSM and VSP at 2026-11-02; RD at 2026-11-02, newest RD-923.
