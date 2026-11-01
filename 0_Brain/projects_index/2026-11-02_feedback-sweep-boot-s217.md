# Feedback sweep, boot s217: Jira half (2026-11-02)

Read only. No Jira writes, no az, no ssh, no HTTP to any hosted, demo or production app host. The only network calls were Jira REST searches (`POST /rest/api/3/search/jql`, paginated to `isLast`), each made with the project's own `4_Credentials/.env` loaded inside the process (no token printed). Window: `created >= "2026-11-01"` (the watermark advanced by [[2026-11-01_feedback-sweep-boot-s215]]).

Excluded per `learnings/2026-10-12_boot-sweeps-all-feedback-repositories.md`: HPSM-POC, Security Composer, MPS Calculator.

**Helper note:** no in-scope project has a Jira read helper; same throwaway REST script as s215, in the session scratchpad. The VSP `.env` carries no `JIRA_PROJECT_KEY`, so the key `VSP` was supplied by the script (confirmed by the positive control firing).

## BLUF

**0 new feedback-shaped Jira issues since 2026-11-01 in every in-scope Jira project.** Vision QuickQuote has no Jira, so its half is UNMEASURED here.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Jira key | New feedback since 11-01 | Positive control | Negative control (`summary ~ "zebra quokka marmalade"`) | All issues created since 11-01 |
|---|---|---|---|---|---|
| HPSM | HPSM | **0** | F without date -> 0 (same as sweeps 1 and s215); `created >= "2020-01-01"` -> 41 (matches) | 0 | 0 (still dormant) |
| NexusAI | RD | **0** | F without date -> 21 (newest RD-840..842); `created >= "2020-01-01"` -> 910 | 0 | 3 (RD-912, RD-913, RD-914; none feedback-shaped: two follow-ups on roster reads, one npm-audit red) |
| Vision Portal | VSP | **0** | F without date -> 1 (VSP-88); `created >= "2020-01-01"` -> 89 | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a |

JQL used (per project, KEY substituted), all `project = <KEY> AND ( ... )`:
- `project = <KEY> AND ( (F) AND created >= "2026-11-01" )`
- `project = <KEY> AND ( F )` (positive control)
- `project = <KEY> AND ( created >= "2020-01-01" )` (positive control for dormant HPSM; frame check for all)
- `project = <KEY> AND ( summary ~ "zebra quokka marmalade" )` (negative control)
- `project = <KEY> AND ( created >= "2026-11-01" )` (context)

## New items

None feedback-shaped. Context only: RD-912, RD-913, RD-914 (created 2026-11-01, engineering follow-ups).

## UNMEASURED

- **Vision QuickQuote:** no Jira project; tracker is BACKLOG.md, and the feedback signal is the tuesday-agent@ CC mail. Not read in this Jira-only half.
- **All live in-app stores** (NexusAI share, Vision Portal prod Postgres, QuickQuote Azure Table): unchanged; they need az or a sign-in that writes. Jira 0 means nothing reached Jira, not that the stores are empty.
- **Vision Portal #6** ("Social Media Engagement" tile request) remains unticketed; no VSP issue was created since 11-01. Still standing.
- **Same-day gap:** the window is `created >= "2026-11-01"` (date granularity), so items created on 11-01 are inside it; none were feedback-shaped.

## Watermark

Advance the Jira watermark for HPSM, RD and VSP to **2026-11-02** (this sweep).
