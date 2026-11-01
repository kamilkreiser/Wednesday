# Feedback sweep, boot s223: Jira half (2026-11-02)

Read only; Jira REST `POST /rest/api/3/search/jql` only, paginated, each project's own `4_Credentials/.env` loaded in-process, no token printed. Method, scope, exclusions, table shape and controls copied from [[2026-11-02_feedback-sweep-boot-s222]]. Script: session scratchpad `sweep.py`. Window `created >= "2026-11-02"`. Excluded: HPSM-POC, Security Composer, MPS Calculator. The VSP key `VSP` was supplied by the script.

## BLUF

**0 new feedback-shaped issues in HPSM, RD and VSP. Totals are UNCHANGED from s222 (HPSM 41, RD 915, VSP 89).** All controls matched s222. Vision QuickQuote has no Jira: UNMEASURED.

Feedback filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback`

| Project | Key | New feedback in window | Positive control (F, no date) | Frame (`created >= 2020-01-01`) | Negative control (`summary ~ "zebra quokka marmalade"`) | All created in window |
|---|---|---|---|---|---|---|
| HPSM | HPSM | **0** | 0 (same; weaker instrument) | 41 (newest HPSM-41) | 0 | 0 |
| NexusAI | RD | **0** | 21 (RD-840..842 newest) | 915 (newest RD-919) | 0 | 5 (RD-915..919, same as s222) |
| Vision Portal | VSP | **0** | 1 (VSP-88) | 89 (newest VSP-89) | 0 | 0 |
| Vision QuickQuote | none | **UNMEASURED** | n/a | n/a | n/a | n/a |

Every JQL is `project = <KEY> AND ( ... )`.

## New items since s222

None. RD-915..RD-919 are the known internal QA findings (not feedback).

## UNMEASURED

Vision QuickQuote (no Jira); live in-app stores (fenced); Vision Portal #6 still unticketed; window is date-granular.

## Watermark

HPSM and VSP at 2026-11-02; RD at 2026-11-02, newest RD-919.
