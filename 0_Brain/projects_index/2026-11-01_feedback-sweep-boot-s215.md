# Feedback sweep, boot s215: Jira half (2026-11-01)

Read only. No Jira writes, no az, no ssh, no HTTP to any hosted, demo or production app host. The only network calls were Jira REST searches (`POST /rest/api/3/search/jql`, paginated to `isLast`), each made with the project's own `4_Credentials/.env` loaded inside the process (no token printed). Window: `created >= "2026-10-25"` (later than the 10-16 watermarks in [[2026-10-16_feedback-sweep-2]]).

Excluded per `learnings/2026-10-12_boot-sweeps-all-feedback-repositories.md`: HPSM-POC, Security Composer, MPS Calculator.

**Helper note:** no in-scope project has a Jira read helper under `.tools/` (only HPSM-POC, excluded, has `b60-jira.py`). Sweep 2 used each project's `.env` with REST search directly; this sweep did the same with a throwaway script in the session scratchpad.

## BLUF

**0 new feedback-shaped Jira issues since 2026-10-25 in every in-scope Jira project.** Vision QuickQuote has no Jira, so its half is UNMEASURED here.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Jira key | New feedback since 10-25 | Positive control | Negative control (`summary ~ "zebra quokka marmalade"`) | All issues created since 10-25 |
|---|---|---|---|---|---|
| HPSM | HPSM | **0** | F without date → 0 (same as sweep 1); so used `created >= "2020-01-01"` → 41 (matches sweep 1) | 0 | 0 (project still dormant) |
| NexusAI | RD | **0** | F without date → 21 (newest RD-840..842, the 10-13 `Feedback #8-#10` tickets) | 0 | 32 (none feedback-shaped) |
| Vision Portal | VSP | **0** | F without date → 1 (VSP-88, a feedbackDigest DB-permission bug, 09-29); `created >= "2020-01-01"` → 89 | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a |

JQL used (per project, KEY substituted), all `project = <KEY> AND ( ... )`:
- `project = <KEY> AND ( (F) AND created >= "2026-10-25" )`
- `project = <KEY> AND ( F )` (positive control)
- `project = <KEY> AND ( summary ~ "zebra quokka marmalade" )` (negative control)
- `project = <KEY> AND ( created >= "2026-10-25" )` (context)

## New items

None.

## UNMEASURED

- **Vision QuickQuote:** no Jira project; tracker is BACKLOG.md, and the feedback signal is the tuesday-agent@ CC mail (`QuickQuote feedback (`). Not read in this Jira-only half.
- **All live in-app stores** (NexusAI share, Vision Portal prod Postgres, QuickQuote Azure Table): unchanged from sweeps 1-2; they need az or a sign-in that writes. Jira 0 means nothing reached Jira, not that the stores are empty.
- **Vision Portal #6** (2026-04-15, "Social Media Engagement" tile request) was unticketed at sweep 1; this sweep found no VSP ticket for it (the F filter would not match it by wording, and no VSP issue was created since 10-25). Still standing.

## Watermark

Advance the Jira watermark for HPSM, RD and VSP to **2026-11-01** (this sweep).
