# Feedback sweep, boot s219: Jira half (2026-11-02)

Read only. No Jira writes, no az, no ssh, no HTTP to any hosted, demo or production app host. Only Jira REST searches (`POST /rest/api/3/search/jql`, paginated to `isLast`), each with the project's own `4_Credentials/.env` loaded inside the process (no token printed). Method, scope, exclusions and controls copied from [[2026-11-02_feedback-sweep-boot-s217]] and [[2026-11-02_feedback-sweep-boot-s218]]. Script in the session scratchpad (`sweep.py`), not a tracked tree. The VSP `.env` carries no `JIRA_PROJECT_KEY`; the key `VSP` was supplied by the script.

**Window:** `created >= "2026-11-02"` (same start as s218, which read the same day, so this window OVERLAPS s218 and s217 entirely and only catches what was created since s218 ran; JQL date granularity, so anything created earlier on 11-02 is inside it). Items from 11-01 were covered by s217.

Excluded per `learnings/2026-10-12_boot-sweeps-all-feedback-repositories.md`: HPSM-POC, Security Composer, MPS Calculator.

## BLUF

**0 new feedback-shaped Jira issues since 2026-11-02 in every in-scope Jira project (overlaps s218; nothing created since it). Controls passed for RD and VSP; HPSM's positive control is 0, so its instrument is weaker (see note).** Vision QuickQuote has no Jira, so UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame check (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All issues created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same as s215/s217) | 41 | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest) | 910 (newest RD-912..914) | 0 | 0 |
| Vision Portal | VSP | **0** | 1 (VSP-88) | 89 | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

Counts match s217 and s218 exactly (41 / 910 / 89 totals; no issue newer than RD-914, VSP-89, HPSM-41).

JQL (KEY substituted), all `project = <KEY> AND ( ... )`: `(F) AND created >= "2026-11-02"`; `(F)`; `created >= "2020-01-01"`; `summary ~ "zebra quokka marmalade"`; `created >= "2026-11-02"`.

**Weaker HPSM instrument:** HPSM's positive control returns 0 (no historical HPSM issue matches F), so the filter has never been shown to catch feedback there. Its 0 is backed only by the frame check (41), the negative control (0) and the unfiltered "all issues created in window" count (0), which is the real evidence: no HPSM issue of any kind was created in the window.

## New items

None.

## UNMEASURED

- **Vision QuickQuote:** no Jira project; tracker is BACKLOG.md, feedback signal is the tuesday-agent@ CC mail. Not read here.
- **All live in-app stores** (NexusAI share, Vision Portal prod Postgres, QuickQuote Azure Table): need az or a writing sign-in; fenced. Jira 0 means nothing reached Jira, not that the stores are empty.
- **Vision Portal #6** ("Social Media Engagement" tile request) remains unticketed; no VSP issue exists past VSP-89.
- **Time-of-day:** window is date-granular; the exact s217 minute is not used.

## Watermark

Keep the Jira watermark for HPSM, RD and VSP at **2026-11-02**.
