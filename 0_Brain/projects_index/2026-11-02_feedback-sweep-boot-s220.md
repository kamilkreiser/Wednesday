# Feedback sweep, boot s220: Jira half (2026-11-02)

Read only. No Jira writes, no az, no ssh, no HTTP to any hosted, demo or production app host. Only Jira REST searches (`POST /rest/api/3/search/jql`, paginated to `isLast`), each with the project's own `4_Credentials/.env` loaded inside the process (no token printed). Method, scope, exclusions, table shape and controls copied from [[2026-11-02_feedback-sweep-boot-s219]] (itself from s217/s218). Script in the session scratchpad (`sweep.py`), not a tracked tree. The VSP `.env` carries no `JIRA_PROJECT_KEY`; the key `VSP` was supplied by the script. One extra read (`rd.py`, same endpoint, fields summary/labels/created/issuetype) listed the 5 RD issues found in the window.

**Window:** `created >= "2026-11-02"`, the same start as s219, so this window OVERLAPS s219 (and s217/s218) entirely and only catches what was created since s219 ran. JQL date granularity, so anything created earlier on 11-02 is inside it too.

Excluded per `learnings/2026-10-12_boot-sweeps-all-feedback-repositories.md`: HPSM-POC, Security Composer, MPS Calculator.

## BLUF

**0 new feedback-shaped Jira issues in every in-scope Jira project, but the totals DIFFER from s219 in RD: 5 new RD issues (RD-915..RD-919) were created since s219 (frame 910 -> 915). All five are QA-gate findings from B1088 (label `qa-gate-finding`), none matches filter F, none is user feedback.** HPSM and VSP unchanged from s219. Controls passed for RD and VSP; HPSM's positive control is 0, so its instrument is weaker (see note). Vision QuickQuote has no Jira, so UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame check (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All issues created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same as s215/s217/s219) | 41 (newest HPSM-41) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest; same as s219) | **915** (newest RD-917..919; s219 said 910, DIFFERS) | 0 | **5** (s219: 0, DIFFERS) |
| Vision Portal | VSP | **0** | 1 (VSP-88; same) | 89 (same; newest VSP-89) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

JQL (KEY substituted), all `project = <KEY> AND ( ... )`: `(F) AND created >= "2026-11-02"`; `(F)`; `created >= "2020-01-01"`; `summary ~ "zebra quokka marmalade"`; `created >= "2026-11-02"`.

**Why the RD difference is real, not an instrument fault:** the frame check moved by exactly the 5 issues the unfiltered window query returned (910 + 5 = 915), the negative control stayed 0, the F positive control stayed 21 (so the 5 new issues are not F matches), and HPSM and VSP frames are unchanged. Created stamps are 2026-11-02 03:57 +1100.

**Weaker HPSM instrument:** HPSM's positive control returns 0 (no historical HPSM issue matches F), so the filter has never been shown to catch feedback there. Its 0 is backed by the frame check (41), the negative control (0) and the unfiltered window count (0): no HPSM issue of any kind was created in the window.

## New items

The 5 new RD issues (Task, labels `ai-assistant`, `b1069-finding`, `b1088-2026-11-02`, `qa-gate-finding`), classified as internal QA findings, not feedback:

- RD-915: RD-913 follow-up, no cell pins the compression level of the data export.
- RD-916: RD-913 follow-up, scoped jest transform in package.json has no cell for its default entry.
- RD-917: RD-913 follow-up, `streamExport` (backend/dataExport.js) stays pending when its destination is destroyed.
- RD-918: RD-913 follow-up, sqlite3 6 arrives through an install script that npm 11.19 warns about (also label `dependencies`).
- RD-919: sqlite3 6, the NexusAI database driver, is archived upstream with no successor chosen (also label `dependencies`).

Nothing else new.

## UNMEASURED

- **Vision QuickQuote:** no Jira project; tracker is BACKLOG.md, feedback signal is the tuesday-agent@ CC mail. Not read here.
- **All live in-app stores** (NexusAI share, Vision Portal prod Postgres, QuickQuote Azure Table): need az or a writing sign-in; fenced. Jira 0 means nothing reached Jira, not that the stores are empty.
- **Vision Portal #6** ("Social Media Engagement" tile request) remains unticketed; no VSP issue exists past VSP-89.
- **Time-of-day:** window is date-granular; the exact s219 minute is not used.

## Watermark

Keep the Jira watermark for HPSM and VSP at **2026-11-02**; RD at **2026-11-02**, newest seen RD-919.
