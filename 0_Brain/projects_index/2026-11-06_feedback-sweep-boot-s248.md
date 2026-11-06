# Feedback sweep, boot s248 (2026-11-06 13:05 AEDT to ~13:15)

Read only. Jira cloud REST `GET /rest/api/3/search/jql` only, every JQL `project = <KEY> AND ( ... )`, paged to `isLast`; each project's own `4_Credentials/.env` read in-process by name, no token printed. Mail: `GET` list of `tuesday-agent@agentmail.to` only, subject/sender/timestamp. No HTTP to any app, demo or production host. Script was session-only (scratchpad), nothing else written. Method from [[2026-11-02_feedback-sweep-boot-s227]] and the 2026-11-03 00:40 note (`daily_tuesday/2026-11-03.md:32`).

## Frame (said plainly)

The commissioned frame is "since 2026-11-03 00:00 AEDT (s230)". **A later sweep record exists and I found it:** `2_Project_Files/tuesday/briefs/2026-11-03_FEEDBACK-0600.md` (06:01 to 06:07 on 11-03, drafter): HPSM 0, RD 0, VSP 0, mail 0, with HPSM-POC, Security Composer and MPS **excluded**. So the true last recorded sweep for the three in-scope projects closed 2026-11-03 06:07; for HPSM-POC, Composer and MPS no feedback sweep is on record after the exclusion began. No later sweep line in `daily_tuesday/2026-11-04..06` (grep "sweep" with "feedback": none). I used the wider window, `created >= 2026-11-03` (date-granular, so it also re-covers 00:00 to 06:07 on 11-03), and flag below which items fall inside the 06:07 sweep's already-covered span.

Filter F = `labels in (feedback, user-feedback, hp-feedback) OR summary ~ feedback` (applied by program over a full dump of each project, and server-side for the window).

## BLUF

**2 new feedback items, both in HPSM-POC (HPSMPOC-441, HPSMPOC-442), created 2026-11-03 15:29, i.e. after the 06:07 sweep. Both are already tickets (they are Jira issues) and both are Done (label `po-feedback`, branch tag b1216). Nothing to ticket.** Three in-scope projects (HPSM, NexusAI RD, Vision Portal VSP): 0 new feedback, each with a control. Composer and MPS: 0 new feedback. Live in-app stores remain UNMEASURED (fenced).

## Per project

Rule columns: 10-12 = the exclusion in force "at the moment" for HPSM-POC, Security Configuration (Composer) and MPS; 10-16 = the boot-sweep rule that covers each Datasec project. The excluded three are reported because 10-16 covers them; mark them as outside the 10-12 sweep.

| Project (key) | Rule | Store / instrument | Frame (all issues, newest) | Positive control (F, no date) | Negative control (`zebra quokka marmalade`) | New feedback (created >= 11-03) | All created >= 11-03 |
|---|---|---|---|---|---|---|---|
| HPSM (HPSM) | 10-16 and 10-12 scope | Jira GET dump | 41, HPSM-41 (2026-08-24) | 0 (weaker instrument, as in every sweep) | 0 | **0** | 0 |
| NexusAI (RD) | 10-16 and 10-12 scope | Jira GET dump | 920, RD-924 (equals prior 919/RD-923 plus one) | 21 (newest RD-840..842, equals prior 21) | 0 | **0** | 1 (RD-924) |
| Vision Portal (VSP) | 10-16 and 10-12 scope | Jira GET dump | 89, VSP-89 (equals prior) | 1 (VSP-88, equals prior) | 0 | **0** | 0 |
| HPSM-POC (HPSMPOC) | 10-16 only (10-12 excluded) | Jira GET dump (Admin feedback screen lands in Jira) | 445, HPSMPOC-445 | 43 (fires; newest 405, 441, 442) | 0 | **2** | 9 |
| Security Composer (PCOMP) | 10-16 only (10-12 excluded) | Jira GET dump | 127, PCOMP-127 | 0 (weaker instrument; no feedback label or word in the project) | 0 | **0** | 8 |
| MPS Calculator (MPSCALC) | 10-16 only (10-12 excluded) | Jira GET dump | 384, MPSCALC-384 | 17 (fires; newest 351, 354, 356) | 0 | **0** | 8 |

Server-side F-in-window (`created >= "2026-11-03" AND ( ... F ... )`) agreed with the program count in every project (2 for HPSMPOC, 0 elsewhere). Pagination followed to the last page. Zeros: HPSM and VSP rest on frame equality plus an empty window (no issue created since 08-24 and 09-29); NexusAI zero is backed by a firing positive control (21) and a visible new-issue control (RD-924 appears in the window, so the window is not blind); Composer's zero rests on the all-created control (8 issues appear, none feedback-shaped) because its positive control is 0.

## New items

- HPSMPOC-441 (created 11-03 15:29, Done, `po-feedback`): UAT feedback FB-01a19e7a, shell has no Menu button in the header; a hamburger at the top of the menu rail. Ticketed: yes (it is the ticket). After the 06:07 sweep: new.
- HPSMPOC-442 (created 11-03 15:29, Done, `po-feedback`): UAT feedback FB-01a19e8b, a first category to run an idea past the HP reviewer, held until approved. Ticketed: yes. New.

Not feedback, for the record: RD-924 (internal QA follow-up of RD-902, labels `qa-gate-finding`); HPSMPOC-437..440, 443..445, PCOMP-120..127 and MPSCALC-377..384 are internal gate-finding/records tickets (labels of the form b####-gate, plan-comp-*, mpscalc-b*); none contains the word feedback in its summary or a feedback label (program count 0 beyond 441, 442).

Already ticketed? Both new items yes. Whether HPSM-POC has feedback items in its live Admin feedback store with no Jira ticket is UNMEASURED.

## Mail half (`tuesday-agent@agentmail.to`, subject and sender only)

First page, 100 rows, newest 2026-11-06T01:58:46Z (a coordinator FYI), oldest on that page 2026-10-19; listing reached the head (newest is today's). Rows after 2026-11-02 13:00Z: 9, none feedback copies: four ATTIO daily digests, two seat/outbound-reply rows about HPSM-POC SOWs, three coordinator FYI mails. Positive control: subject match /feedback/i on the page = 1 (an MPS question of 2026-10-22 about a feedback rate-limit key), so the regex fires. **0 feedback copies (QuickQuote, Vision) since 11-02.** Page 1 only was needed for the window; next-page token existed, older mail not read.

## UNMEASURED

QuickQuote stored items (Azure Table; mail shows none since 2026-10-09); Vision Postgres feedback table; NexusAI settings `feedbackItems`; HPSM-POC live Admin feedback store; HPSM Policy Composer live store; Vision Portal #6 (Social Media Engagement tile) still unticketed per earlier notes (not re-read). Whether feedback is filed in Jira without the word "feedback" or a feedback label (F cannot see it); the all-created-in-window counts above are the control. Window is date-granular.

## Disclosure

No fence broken: no `decision_queue.sh list`, no `cd`, no HTTP to any app/demo/production host, no mail sent, no Wednesday/Secuura tree read, no Jira write, no marker file. Read for the frame: the learning file, DRAFTER_RULES, the s227 note, `daily_tuesday/2026-11-03.md` (lines 28-37 plus grep hits), `briefs/2026-11-03_FEEDBACK-0600.md` (head). Reading `.env` files of six Datasec projects plus the Tuesday seat `.env` (AGENTMAIL key) happened in-process; nothing printed. One slip: my first grep to inspect daily-note lines failed with a regex-size error and printed nothing; re-done with a different command.

## Watermark

Jira feedback watermark advanced to 2026-11-06 13:15 AEDT for all six projects; newest items processed: HPSM-41, RD-924, VSP-89, HPSMPOC-445 (feedback: 442), PCOMP-127, MPSCALC-384. Mail watermark 2026-11-06T01:58Z.
