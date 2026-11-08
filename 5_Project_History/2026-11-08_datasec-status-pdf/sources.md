# Sources for Datasec-status-2026-11-08.pdf

All figures read at source on Sunday 2026-11-08 between 20:10 and 20:15 AEDT (UTC+11) by a read-only session. Nothing was sent, written to a project, Jira or GitHub. No hosted site was contacted (UAT on hold, not checked live). Times in the PDF are AEDT; the raw GitHub output below is UTC (add 11 hours).

"Since 4 Nov" means from 2026-11-04 00:00 AEDT (= 2026-11-03T13:00:00Z). A first pass used a UTC cutoff and missed 5 pull requests merged on the morning of 4 Nov AEDT; it was redone and the raw output below is the second pass.

## Figure table
| Figure | Value | Instrument | Time |
|---|---|---|---|
| Main sha and date, per repo | HPSM-POC b14b6f29fe34 (2026-11-06T21:25:59Z); Composer a54250f48f41 (2026-11-03T20:16:17Z); MPS bb9bac9bf604 (2026-11-06T22:10:07Z); NexusAI fe75d7b2da83 (2026-11-06T20:25:20Z) | `gh api -X GET repos/<repo>/commits/main` | 20:11-20:12 |
| PRs merged since 4 Nov | HPSM-POC 14 (#281-#294); Composer 1 (#118); MPS 8 (#157-#164); NexusAI 17 (#165-#181); total 40 | `gh api -X GET repos/<repo>/pulls -f state=closed --paginate`, filter merged_at >= 2026-11-03T13:00:00Z | 20:11-20:12 |
| Open PRs | HPSM-POC 0; Composer 3 (#91, #86, #85 draft); MPS 0; NexusAI 0 | `gh api -X GET repos/<repo>/pulls -f state=open --paginate` | 20:11-20:12 |
| Tickets total/open/done | HPSMPOC 447 = 132 Backlog + 3 In Progress + 312 Done (open 135); PCOMP 127 = 95 Backlog + 32 Done; MPSCALC 385 = 227 Backlog + 158 Done; RD 975 = 395 To Do + 240 Testing + 199 Release Ready + 124 Done + 8 In Progress + 7 Put on Hold + 2 Declined (open 849 = 975 - 124 - 2) | `fleet/board_count.sh jira` via `/rest/api/3/search/jql`, JQL `project = <KEY> AND ( created >= '2000-01-01' OR created < '2000-01-01' )`, paged to isLast (tool refuses a capped total) | 20:10-20:11 |
| Moved to Done since 4 Nov | HPSMPOC 10; PCOMP 3; MPSCALC 13; RD 0; total 26 | `board_count.sh`, JQL `statusCategory = Done AND statusCategoryChangedDate >= '2026-11-04'`. Sample keys: HPSMPOC-254, 268, 349, 400, 412, 440, 441, 443, 444, 445; PCOMP-115, 119, 122; MPSCALC-107, 108, 116, 127, 134, 335, 336, 362, 374, 375, 376, 384 (+1 more). Check: the changelog of HPSMPOC-412, PCOMP-115, MPSCALC-376 shows Backlog -> Done on the morning of 4 Nov AEDT. The stricter query `status CHANGED TO Done AFTER '2026-11-04'` returns 7/1/12/0 because it excludes those 4 Nov moves; the PDF uses the inclusive one. | 20:10-20:11 |
| RD zero (positive control) | RD Done since 4 Nov = 0. Controls on the same field: `statusCategory = Done AND statusCategoryChangedDate >= '2026-01-01'` returned 124; `status CHANGED TO Done AFTER '2026-10-20'` returned 7; `status CHANGED TO Done AFTER '2026-11-03 23:59'` returned 0 | direct GET on `/rest/api/3/search/jql` | 20:12 |
| RD moved to Testing since 4 Nov | 24 | JQL `status CHANGED TO Testing AFTER '2026-11-03 23:59'` (same count with DURING) | 20:14 |
| RD-972, RD-973 | RD-972 (Medium, To Do, created 2026-11-07 06:29 AEDT): "Ending a user's open sessions after a deactivation or a password change does nothing: the update route tests for two store methods that do not exist". RD-973 (Medium, To Do): "setQuickQuestions in simpleDb.js sends ROLLBACK without waiting for it, so a read made after the rejection can see the uncommitted delete; one test cell has gone red once because of it". Titles read at source; "derived from source, not run" is from the product owner's brief and the morning card. | GET `/rest/api/3/search/jql`, `key in (RD-972,RD-973)` | 20:12 |
| Awaiting the product owner | 3: HPSM-POC 1 (hpsmpoc-319-local-probe-closes-1106, 47.9 h), MPS 1 (mps-106-price-guard-round-cap-1106, 45.8 h), Composer 1 (composer-l05-setup-card-too-1014, 611.5 h); NexusAI 0 | `tuesday/tools/kam_awaiting_counts.sh`; card bodies via `tools/decision_queue.sh show <id>` for those ids and for datasec-morning-plan-1107 (status withdrawn at 2026-11-08T20:10:06, reason: answered on the live board) | 20:12 |
| Claims, not checked at source | Log-sink round 1 no-go and round 2 prepared; follow-up worker moves HPSMPOC-446 and MPSCALC-106 tickets; composer card settled by an email of 23 Oct; nothing deployed since the 6 Nov hold | `0_Brain/tasks/NEXT-PICKUP-TUESDAY.md` DELTA 1077 to 1072 (read as claims only) and the product owner's stated ruling | 20:05 |
| Not read | No hosted site, CI run, or deployment state was read. Whether the MPS card default was the path to PR #164 is inferred from the timing (merged 2026-11-06T22:10:08Z = 09:10 AEDT on 7 Nov, card default 09:00). | | |

## Raw output: GitHub (second pass)
```
##### datasecau/HPSM-POC  (GH_CONFIG_DIR of HPSM-POC)  at 2026-11-08 20:12:07 AEDT
default_branch=main
main b14b6f29fe34568472e1c6e87178b0244ec32415 2026-11-06T21:25:59Z | Api tests: drop the SQLite assertion that no session was killed, which could not fail
-- merged PRs since 2026-11-04 00:00 AEDT = 2026-11-03T13:00:00Z
#281	2026-11-03T13:38:37Z	base=main	HPSMPOC-440: pin bad date before empty evidence for a word joiner (test rows only)
#282	2026-11-03T20:44:56Z	base=main	HPSMPOC-406 HPSMPOC-412 HPSMPOC-399 HPSMPOC-368: Home words; menu focus ring and page-end footer
#283	2026-11-03T22:32:57Z	base=main	HPSMPOC-443: pin a bad date before word-joiner-then-zero-width-space evidence (test rows)
#284	2026-11-04T00:46:42Z	base=main	Admin: the approval page gets its new title, and Feedback received lists only items sent with the review option
#285	2026-11-04T07:27:03Z	base=main	Shell: no Menu button in the top bar from 1024 px; a rail hamburger collapses the menu to clickable icons; logo left
#286	2026-11-04T23:38:22Z	base=main	Shell and pages: white menu, status colours, wider content, mock layout rows, account menu; report colours follow the site
#287	2026-11-05T04:14:06Z	base=main	Finish the HTML mock's page layout: page padding and head, tile icon chips, results split, cards, buttons, print
#288	2026-11-05T04:51:05Z	base=main	Review copy: the start page's logo opens the feedback review page to anyone, who can read, approve and delete held items
#289	2026-11-06T00:42:42Z	base=main	Review door: correct a false comment; pin HEAD on the list and an item, and the guard before sign-in
#290	2026-11-06T01:16:16Z	base=main	Runner tests: source-text pins accept a formatter's reflow; CI comment states the hosted test count
#291	2026-11-06T03:20:04Z	base=main	Mock-rows e2e: each frame waits for what its page shows instead of a fixed 500 ms pause
#292	2026-11-06T06:40:30Z	base=main	Retire the demo site paths: parameter file, sign-in lock branches, notice, README wording
#293	2026-11-06T08:21:10Z	base=main	Api tests: two hosts start together on one fresh SQL Server database after a real lock loss
#294	2026-11-06T21:26:00Z	base=main	Api tests: drop the SQLite assertion that no session was killed, which could not fail
-- open PRs
-- open PR count check:
       0
##### datasecau/Datasec-Security-Composer  (GH_CONFIG_DIR of Datasec Security Composer)  at 2026-11-08 20:12:12 AEDT
default_branch=main
main a54250f48f41b693ab73163531e7ca82425fce69 2026-11-03T20:16:17Z | Type-check the database test files in CI with a test project for packages/db/test (#118)
-- merged PRs since 2026-11-04 00:00 AEDT = 2026-11-03T13:00:00Z
#118	2026-11-03T20:16:18Z	base=main	Type-check the database test files in CI
-- open PRs
#91	2026-10-25T02:25:19Z	draft=false	base=main	Bump @vitest/mocker and vitest
#86	2026-10-20T22:10:51Z	draft=false	base=main	Bump vite from 8.3.0 to 8.3.4
#85	2026-10-20T11:34:38Z	draft=true	base=main	HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)
-- open PR count check:
       3
##### datasecau/MPS-Commercial-Calculator  (GH_CONFIG_DIR of Datasec MPS Commercial Calculator)  at 2026-11-08 20:12:16 AEDT
default_branch=main
main bb9bac9bf604af7c30826403889f8ecb995f940f 2026-11-06T22:10:07Z | Test only: pricing guard reads money by type, exemption keyed on a declaration (MPSCALC-106)
-- merged PRs since 2026-11-04 00:00 AEDT = 2026-11-03T13:00:00Z
#157	2026-11-03T23:39:27Z	base=main	Test only: pin per-site rows for a missing site entry and today's repeated id reading (MPSCALC-382)
#158	2026-11-04T03:14:43Z	base=main	Bump undici to 8.12.3 and zod to 4.6.7 in /web (lockfile only; replaces #120 and #121)
#159	2026-11-06T03:08:58Z	base=main	Test only: the summary census renders the rental proposal and the one-pager as surfaces S10 and S12 (MPSCALC-116)
#160	2026-11-06T03:09:15Z	base=main	Test only: the colour guard reads var() fallbacks and filter, and takes a token list (MPSCALC-107)
#161	2026-11-06T09:41:28Z	base=main	Test only: pin the collapsed reference path and the inside walk of the overlay start gate (MPSCALC-94)
#162	2026-11-06T09:41:07Z	base=main	A second press of a print button while a print waits for its images is now ignored (MPSCALC-108)
#163	2026-11-06T09:41:45Z	base=main	Test only: a timeout and killSignal on every pdftotext call in the e2e specs, and a row that holds them (MPSCALC-134)
#164	2026-11-06T22:10:08Z	base=main	Test only: the pricing guard reads money by type, keys its one exemption on a declaration and follows summed Object.values (MPSCALC-106)
-- open PRs
-- open PR count check:
       0
##### datasecau/Reporting_Dashboard_Au  (GH_CONFIG_DIR of NexusAI)  at 2026-11-08 20:12:19 AEDT
default_branch=main
main fe75d7b2da83496d9fb8e341b6dd849da3b9922f 2026-11-06T20:25:20Z | Merge pull request #181 from datasecau/records/b1363
-- merged PRs since 2026-11-04 00:00 AEDT = 2026-11-03T13:00:00Z
#165	2026-11-04T02:26:48Z	base=main	RD-902: the sync on GET /api/risk-conditions runs only when the administrator check passes
#166	2026-11-04T03:59:04Z	base=main	Records B1274: HISTORY entry for the landing of #165 as a move to Testing
#167	2026-11-04T11:35:12Z	base=main	RD-924: K1 pins the first-run input of the RD-902 read-path check and asserts sign-in is configured
#168	2026-11-04T15:19:12Z	base=main	Records B1292: HISTORY entry for the landing of #167 (RD-924)
#169	2026-11-04T22:09:03Z	base=main	RD-916: the jest block moves to jest.config.js, and two cells hold the default transform entry and the resolved plugin
#170	2026-11-05T06:18:02Z	base=main	Records B1308: HISTORY entry for the landing of #169 as a move to Testing
#171	2026-11-06T01:22:55Z	base=main	Records: pass over RD-782 to RD-789, RD-774 and RD-836
#172	2026-11-06T04:27:27Z	base=main	RD-798: five AI-suggestion log lines go through logSafe, and a cell red at the base holds each one
#173	2026-11-06T06:15:48Z	base=main	Records: HISTORY entry for the landing of #172 and the ticket pass over it
#174	2026-11-06T07:27:54Z	base=main	RD-573: the jest port band moves below Linux's ephemeral range, and a cell judges it
#175	2026-11-06T08:12:27Z	base=main	Records: HISTORY entry for the roles-and-layout tickets (RD-927 to RD-958)
#176	2026-11-06T10:05:15Z	base=main	RD-779, RD-781, RD-790, RD-803, RD-809, RD-812, RD-813: eight CodeQL alerts in developer tools and hand-run test pages are fixed by seven small edits that touch no product file
#177	2026-11-06T11:24:27Z	base=main	Records: HISTORY entry for the word pack decisions and the owed findings
#178	2026-11-06T13:01:11Z	base=main	RD-928: add a route-to-capability inventory measured over HTTP, with a census that fails on a route with no row
#179	2026-11-06T16:40:39Z	base=main	RD-928: a browser harness records today's layout at four widths and both themes, and its record writer refuses a link or an existing path
#180	2026-11-06T19:34:48Z	base=main	RD-936: the generated shell palette tokens, the guide section that rules them and a guard that measures every pair in a browser engine
#181	2026-11-06T20:25:21Z	base=main	Records: landings of RD-928 parts A and B, and their review findings
-- open PRs
-- open PR count check:
       0
```

## Raw output: Jira totals via board_count.sh (RD zero lines are the tool refusing an unvalidated zero; controls above)
```
### HPSMPOC | created >= '2000-01-01' OR created < '2000-01-01'
312  Done
  132  Backlog
  3  In Progress
TOTAL=447  (limit was 5001, so this is a real count and not a cap)
### HPSMPOC | statusCategory = Done AND statusCategoryChangedDate >= '2026-11-04'
10  Done
TOTAL=10  (limit was 5001, so this is a real count and not a cap)
### HPSMPOC | status CHANGED TO Done AFTER '2026-11-04'
7  Done
TOTAL=7  (limit was 5001, so this is a real count and not a cap)
### PCOMP | created >= '2000-01-01' OR created < '2000-01-01'
95  Backlog
  32  Done
TOTAL=127  (limit was 5001, so this is a real count and not a cap)
### PCOMP | statusCategory = Done AND statusCategoryChangedDate >= '2026-11-04'
3  Done
TOTAL=3  (limit was 5001, so this is a real count and not a cap)
### PCOMP | status CHANGED TO Done AFTER '2026-11-04'
1  Done
TOTAL=1  (limit was 5001, so this is a real count and not a cap)
### MPSCALC | created >= '2000-01-01' OR created < '2000-01-01'
227  Backlog
  158  Done
TOTAL=385  (limit was 5001, so this is a real count and not a cap)
### MPSCALC | statusCategory = Done AND statusCategoryChangedDate >= '2026-11-04'
13  Done
TOTAL=13  (limit was 5001, so this is a real count and not a cap)
### MPSCALC | status CHANGED TO Done AFTER '2026-11-04'
12  Done
TOTAL=12  (limit was 5001, so this is a real count and not a cap)
### RD | created >= '2000-01-01' OR created < '2000-01-01'
395  To Do
  240  Testing
  199  Release Ready
  124  Done
  8  In Progress
  7  Put on Hold
  2  Declined
TOTAL=975  (limit was 5001, so this is a real count and not a cap)
### RD | statusCategory = Done AND statusCategoryChangedDate >= '2026-11-04'
list. Those are indistinguishable from this side. (RD-586: a

  BOARD_COUNT_ZERO_OK='<control query> -> <its non-zero result>'

### RD | status CHANGED TO Done AFTER '2026-11-04'
list. Those are indistinguishable from this side. (RD-586: a

  BOARD_COUNT_ZERO_OK='<control query> -> <its non-zero result>'

```

## Raw output: Jira category-date vs changed-to-Done comparison
```
HPSMPOC cat-only: ['HPSMPOC-412', 'HPSMPOC-440', 'HPSMPOC-443'] chg-only: [] both 7
PCOMP cat-only: ['PCOMP-115', 'PCOMP-122'] chg-only: [] both 1
MPSCALC cat-only: ['MPSCALC-376'] chg-only: [] both 12
RD cat-only: [] chg-only: [] both 0
RD | statusCategory = Done AND statusCategoryChangedDate >= '2026-01-01' -> 124 ['RD-10', 'RD-107', 'RD-11', 'RD-118', 'RD-12', 'RD-122']
RD | status CHANGED TO Done AFTER '2026-09-01' -> 59 ['RD-118', 'RD-139', 'RD-140', 'RD-141', 'RD-142', 'RD-153']
RD | status CHANGED AFTER '2026-11-04' -> 23 ['RD-494', 'RD-573', 'RD-774', 'RD-779', 'RD-781', 'RD-782']
RD | status = Done AND updated >= '2026-11-04' -> 0 []
RD | updated >= '2026-11-04' -> 84 ['RD-494', 'RD-573', 'RD-691', 'RD-774', 'RD-779', 'RD-781']
RD | status CHANGED TO 'Release Ready' AFTER '2026-11-04' -> 0 []
RD | status CHANGED TO Testing AFTER '2026-11-04' -> 23 ['RD-494', 'RD-573', 'RD-774', 'RD-779', 'RD-781', 'RD-782']
RD | status CHANGED TO Done AFTER '2026-10-20' -> 7 ['RD-868', 'RD-889', 'RD-890', 'RD-903', 'RD-907', 'RD-919']
RD-973 To Do 2026-11-07T06:29:04.883+1100 setQuickQuestions in simpleDb.js sends ROLLBACK without waiting for it, so a read made after the rejection can see the uncommitted delete; one test cell has gone red once because of it
RD-972 To Do 2026-11-07T06:29:02.376+1100 Ending a user's open sessions after a deactivation or a password change does nothing: the update route tests for two store methods that do not exist
```

## Raw output: Jira in-progress / recent tickets
```
## HPSMPOC status = 'In Progress' 3
   HPSMPOC-91 In Progress Medium 2026-10-23T11:45 [C-30] Client collateral: pre-engagement, during-engagement and post-engagement packs
   HPSMPOC-90 In Progress High 2026-10-06T22:07 [C-30] Feedback button: each submission becomes an HPSMPOC Jira issue and an email to Kam
   HPSMPOC-87 In Progress High 2026-10-01T17:44 [C-30] Customer questions: use the 16 as the base, aligned to the Composer's policy principles (DRAFT for Kam)
## HPSMPOC key in (HPSMPOC-319,HPSMPOC-446,HPSMPOC-447) 3
   HPSMPOC-319 Backlog Medium 2026-11-06T19:57 [B469-2, -3, -5, -6] HostStartRetry (PR 183): a log clear no test needs, a retry count that misses an unterminated last line, erro
   HPSMPOC-447 Backlog Medium 2026-11-06T19:56 [B1343-4] Api test-host start retry: a session lost before EF's migration proper (SqlClient: connection broken, no recovery) is no
   HPSMPOC-446 Backlog Medium 2026-11-06T19:56 [B1343-1] ApiFactoryHostStartRetryTests: on SQLite the row's assertion that no session was killed cannot fail, because the kill co
## HPSMPOC status = Backlog AND created >= '2026-11-03' 4
   HPSMPOC-447 Backlog Medium 2026-11-06T19:56 [B1343-4] Api test-host start retry: a session lost before EF's migration proper (SqlClient: connection broken, no recovery) is no
   HPSMPOC-446 Backlog Medium 2026-11-06T19:56 [B1343-1] ApiFactoryHostStartRetryTests: on SQLite the row's assertion that no session was killed cannot fail, because the kill co
   HPSMPOC-439 Backlog Medium 2026-11-03T01:31 [B1147-2] Engagement overview: a single-line linked title in Recent activity sits 20 px above its detail line and a plain title do
   HPSMPOC-438 Backlog Medium 2026-11-03T01:31 [B1156-N2] Action register: the one rule line on the roadmap screen names Verified complete only, while Evidence submitted now nee
## RD status = 'In Progress' 8
   RD-427 In Progress Low 2026-10-05T08:52 First-run setup page never shows the provisioning panel: it sits inside a 'LEGACY - Hidden' wrapper (display:none since RD-135) th
   RD-643 In Progress Medium 2026-09-26T07:20 AOAI endpoint is validated only by the Marketplace wizard: mainTemplate azureOpenAIEndpoint and the boot path (model-config.js:207
   RD-662 In Progress High 2026-09-25T22:21 Customer test of the LIVE Marketplace listing in a separate tenant: round 1 = preparation (plan, cost, dry-run login; nothing crea
   RD-450 In Progress High 2026-09-25T13:08 Marketplace submission readiness: land the round-4 package branch on main, close B2 (the image customers deploy), merge the open b
   RD-81 In Progress Medium 2026-09-14T22:12 Decide + implement CI-driven deploy to the Container Apps demo env
   RD-431 In Progress Low 2026-09-14T21:07 RD-395 round-2 residue: Risk Alerts modal still titled 'AI Validation Result' when AI did not run; offline page logs a CSP inline-
   RD-432 In Progress Medium 2026-09-14T19:41 RD-412/419 gate residue: SMTP server reply text still reaches the admin's error message, error mapping keys on words inside the se
   RD-49 In Progress Medium 2026-09-07T11:13 Decommission 4.x demo VM (app stopped; Azure deallocation + consumer repoint outstanding)
## RD status = 'Put on Hold' 7
   RD-743 Put on Hold Medium 2026-10-05T00:29 C-190 landing scripts gate the main fast-forward on CodeQL only: a PR Build red outside the C-185 known set still lands
   RD-104 Put on Hold Medium 2026-09-07T19:09 gh auth token is not isolated by GH_CONFIG_DIR — a config dir with no hosts.yml returns a live keychain token (gh api correctly re
   RD-93 Put on Hold Low 2026-09-07T15:19 RD board config: remove or rename duplicate transition id 51 'Returned From Testing - Issues Found' (lands on Declined)
   RD-18 Put on Hold High 2026-08-04T15:55 Australian Privacy Act package: statement + sub-processors + DPA template
   RD-41 Put on Hold Medium 2026-08-04T15:55 Deploy Monday lead-sync creds to Container Apps (Monday go-live in prod)
   RD-33 Put on Hold Low 2026-05-21T11:44 Metered billing model (only if usage shapes justify it)
   RD-32 Put on Hold Low 2026-05-21T11:44 Multi-region deployment option (build only when a customer asks for it)
## RD status = 'To Do' AND created >= '2026-11-04' 55
   RD-928 To Do Medium 2026-11-07T06:29 Roles UI foundation: a committed route-to-capability inventory driven over HTTP, and a browser harness that records today's layout
   RD-979 To Do Low 2026-11-07T06:29 The header of shell-layout.spec.js says two admin.html pins and that each served file's hash is checked, but its program counts th
   RD-978 To Do Low 2026-11-07T06:29 The route inventory's gateInHandler column names check tokens that two handlers do not contain, because the scan runs to the next 
   RD-977 To Do Low 2026-11-07T06:29 The route inventory tool and its two committed outputs carry a build-numbered word in the sentinel value they send
   RD-976 To Do Low 2026-11-07T06:29 POST /api/learning/confirm-clarification answers 500 for every request that passes its input check: conversationSessions is not de
   RD-975 To Do Low 2026-11-07T06:29 The business-hours report reads created_at before the job's own start time, so a seeded row is judged by when the store was seeded
   RD-974 To Do Low 2026-11-07T06:29 The automatic insights check for unusual print times gives a job with no Job_Start_Time the current time, so undated jobs count as
   RD-973 To Do Medium 2026-11-07T06:29 setQuickQuestions in simpleDb.js sends ROLLBACK without waiting for it, so a read made after the rejection can see the uncommitted
   RD-972 To Do Medium 2026-11-07T06:29 Ending a user's open sessions after a deactivation or a password change does nothing: the update route tests for two store methods
   RD-971 To Do Low 2026-11-06T21:27 csp-convert.py after the CodeQL change: the end-tag pattern also closes a script block on a vertical tab, file separator or no-bre
   RD-970 To Do Low 2026-11-06T21:27 refactor-inline-styles.js after the CodeQL change: a path under a file (ENOTDIR) or an unreadable parent stops the run where the o
   RD-969 To Do Low 2026-11-06T21:15 Three routes answer 500 to an empty request on an empty store: POST /api/settings/agent, POST /api/settings/business-hours and GET
   RD-968 To Do Medium 2026-11-06T21:14 GET /api/setup/managed-identity answers a viewer 200 and makes the server try to connect to 169.254.169.254:80
   RD-967 To Do Low 2026-11-06T21:14 POST /api/setup/column-mapping is registered twice (the first answers) and GET /api/setup/column-mapping answers 500 for a viewer,
   RD-966 To Do Medium 2026-11-06T21:14 In open mode (no sign-in) 14 admin routes answer 403 and two answer 401, because their handlers compare req.user.role and open mod
## PCOMP status = Backlog 95
   PCOMP-116 Backlog Medium 2026-11-06T11:01 Route B completeness check: an older-minor script with a planted restrict line, footer block and unrestrict line in a function bod
   PCOMP-127 Backlog Medium 2026-11-03T19:42 Route B completeness check: three items left open after Composer PR #114 (gawk not run, the demo VM not re-proven, DEPLOY.md line 
   PCOMP-23 Backlog Medium 2026-11-03T07:34 Gate B136-F1 (Minor; B134 #269 / PR #73). What, verbatim (Briefs/2026-10-12_B136_STATUS.md:45): "with a long target name, the chan
   PCOMP-123 Backlog Medium 2026-11-03T07:34 Change report footer: size the footer by the real page count instead of the widest label (a measurement, 11 of 28 wide-letter foot
   PCOMP-121 Backlog Medium 2026-11-03T07:34 Change report footer: a name with a run of 40 or more tab characters renders on two rows where the footer model counts one (8 test
   PCOMP-120 Backlog Medium 2026-11-03T07:33 Change report footer: 18 of 9,508 test cells still lose the manifest hash line, because the footer model breaks lines at every spa
   PCOMP-114 Backlog Medium 2026-11-02T13:52 Engine timing test: the row 'resolves and validates in under 1 s (median of 7 runs after a warm-up)' times out at 5000 ms under a 
   PCOMP-98 Backlog Medium 2026-11-02T13:52 Cross-line context in the DEPLOY.md command-guard test scanner: 16 known lost cells, 187 sweep instances, test-only
## MPSCALC status = Backlog 227
   MPSCALC-334 Backlog Medium 2026-11-06T21:17 [B606-N3,N5,N8] Dev stub and e2e leftovers: no unit-test file for the stub, one stub key missing from the bundle check, and one sp
   MPSCALC-106 Backlog Medium 2026-11-06T21:16 Browser-pricing guard (E-3a) misses five forms of money arithmetic in the web code (gate B87 E87-1; [B85-3])
   MPSCALC-385 Backlog Medium 2026-11-06T21:15 [B1346-11] Proposal print: the pending flag is set before flushSync, so a throw inside flushSync would leave both print buttons ig
   MPSCALC-118 Backlog Medium 2026-11-06T15:29 In-app API stub emits none of B80's or B85's breakdown fields, so stub mode shows the note instead of a breakdown ([B80-2])
   MPSCALC-377 Backlog Medium 2026-11-06T11:30 [B1166-N1,2] Quantity audit tests: the boundary at one and the sign of a device line are pinned by no named row
   MPSCALC-358 Backlog Medium 2026-11-06T11:28 [B1075-8] Quantity rule on the purchase line contract: the Api, DTO, contract text and web half, with the spelling the reader acce
   MPSCALC-341 Backlog Medium 2026-11-06T11:28 [B732-3] Edges file: six assertions of the new refusal body are pinned by no mutant the gate ran
   MPSCALC-340 Backlog Medium 2026-11-06T11:28 [B732-1,2] Reference document validator: the supply-group key (first group wins; the default text of a supply with no rows cell) i
```

## Raw output: awaiting tool (re-run at end)
```
awaiting 1 for HPSM-POC
  hpsmpoc-319-local-probe-closes-1106  48.0h
awaiting 1 for MPS-Commercial-Calculator
  mps-106-price-guard-round-cap-1106  45.8h
awaiting 1 for Security-Composer
  composer-l05-setup-card-too-1014  611.6h
total awaiting: 3
read at 2026-11-08 20:14:35 AEDT
```
