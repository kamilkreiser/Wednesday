# Feedback sweep, boot s222: Jira half (2026-11-02)

Read only. No Jira writes, no az, no ssh, no HTTP to any hosted, demo or production app host. Only Jira REST searches (`POST /rest/api/3/search/jql`, paginated to `isLast`), each with the project's own `4_Credentials/.env` loaded inside the process (no token printed). Method, scope, exclusions, table shape and controls copied from [[2026-11-02_feedback-sweep-boot-s221]] (itself copied from s220). Script in the session scratchpad (`sweep.py`), not a tracked tree. The VSP `.env` carries no `JIRA_PROJECT_KEY`; the key `VSP` was supplied by the script.

**Window:** `created >= "2026-11-02"`, the same start as s221 (date-granular, overlaps s217-s221 entirely).

Excluded per `learnings/2026-10-12_boot-sweeps-all-feedback-repositories.md`: HPSM-POC, Security Composer, MPS Calculator.

## BLUF

**0 new feedback-shaped Jira issues in every in-scope Jira project, and the totals do NOT differ from s221 (HPSM 41, RD 915, VSP 89). No new RD/HPSM/VSP issue exists since s221.** The 5 RD issues in the unfiltered window (RD-915..RD-919) are the same ones s221 listed. Controls passed for RD and VSP; HPSM's positive control is 0 (weaker instrument, as before). Vision QuickQuote has no Jira, so UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame check (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All issues created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same as s221) | 41 (newest HPSM-41; same as s221) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest; same) | 915 (newest RD-919; same as s221) | 0 | 5 (RD-915..919; same as s221) |
| Vision Portal | VSP | **0** | 1 (VSP-88; same) | 89 (newest VSP-89; same) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

JQL (KEY substituted), all `project = <KEY> AND ( ... )`: `(F) AND created >= "2026-11-02"`; `(F)`; `created >= "2020-01-01"`; `summary ~ "zebra quokka marmalade"`; `created >= "2026-11-02"`.

**Why no difference:** the unfiltered window query returned exactly the same 5 RD issues as s221 and s220 (all Task, labels `ai-assistant`, `b1069-finding`, `b1088-2026-11-02`, `qa-gate-finding`; created 2026-11-02 03:57 +1100), and every frame equals the s221 frame.

**Weaker HPSM instrument:** F has never matched an HPSM issue (positive control 0). The 0 is backed by the frame (41), the negative control (0) and the unfiltered window count (0).

## New items since s221

None. Already-known, internal QA findings (not feedback), listed in s220 and s221: RD-915, RD-916, RD-917, RD-918 (RD-913 follow-ups) and RD-919 (sqlite3 6 archived upstream).

## UNMEASURED

- **Vision QuickQuote:** no Jira project; tracker is BACKLOG.md, feedback signal is the tuesday-agent@ CC mail. Not read here.
- **All live in-app stores** (NexusAI share, Vision Portal prod Postgres, QuickQuote Azure Table): need az or a writing sign-in; fenced. Jira 0 means nothing reached Jira, not that the stores are empty.
- **Vision Portal #6** ("Social Media Engagement" tile request) remains unticketed; no VSP issue exists past VSP-89.
- **Time-of-day:** window is date-granular.

## Watermark

HPSM and VSP at **2026-11-02**; RD at **2026-11-02**, newest seen RD-919.
