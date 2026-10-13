# HPSM-POC board screen: every open HPSMPOC ticket, sorted (read-only)

Datasec / HPSM-POC only. Written 2026-10-13 ~18:55 AEDT by an in-session screen agent for Friday. Read-only: Jira GETs only, with no comment, transition or write; git reads only, with no fetch; this file is the only write.

## Provenance and count
- **The count comes from full pagination, not from `board_count.sh`.** `fleet/board_count.sh jira … 'project = HPSMPOC AND statusCategory != Done'` exited 1 with `MORE PAGES EXIST — this is not a total.` The script asks for `maxResults=250`, but Jira serves at most 100 per page, so it gets a `nextPageToken` and refuses. It never paginates, so it cannot count any Jira query above 100. **Tool gap:** the script needs a pagination loop.
- **The pagination:** `/rest/api/3/search/jql` with `nextPageToken`, followed until no token remained.
  - `project = HPSMPOC`: **250 issues, 3 pages** (done 137, new 108, indeterminate 5).
  - `project = HPSMPOC AND statusCategory != Done`: **113 issues, 2 pages** (Backlog 108, In Progress 5).
  - Cross-check: counting non-done issues inside the 250-issue list gives 113 again.
- **Other sources read:**
  - Code repo `2_Project_Files`: local `origin/main` = `dc136e6`, which is B238's deployed head. No fetch was run.
  - Analysis repo: local `origin/main` = `ce6ad2c`, with CLARIFICATIONS up to C-103.
  - Project files: CLAUDE.md, BACKLOG.md, and the STATUS files for B238, B239 and B240.
  - Not opened: `HP Reporting and Docs/` and the SOW.
- **Context for tomorrow, 14 Oct:**
  - The hosted site is FROZEN under C-103 until Kam names his window.
  - Hosted runs `dc136e6` (B238 DONE, ADDENDUM-1 accepted).
  - B239 closed HPSMPOC-149 and HPSMPOC-152 and created HPSMPOC-250.
  - Nothing in bucket A needs hosted access.

## Counts (from the lists below)
| Bucket | Count |
|---|---|
| A. Agent-actionable now | **15** |
| B. Needs Kam | **58** |
| C. Needs HP or another human | **16** |
| D. Effectively done, still open | **10** |
| E. Unclear | **14** |
| **Total** | **113** (= 113 open; checked by script: each key exactly once) |

How the labels were applied:
- `owner-kam`, `needs-kam` and `for-kam` count as B unless the ticket text shows otherwise. The overrides are HPSMPOC-241 (Kam sent the questions on 8 Oct, so it is now C), HPSMPOC-82–86, -97, -166 and -181 (the text is "awaiting HP", so C) and HPSMPOC-91 (built, so D).
- `owner-datasec-sme` counts as B, because C-05 reads the SME as Kam until he says otherwise.

---

## A. AGENT-ACTIONABLE NOW (15)
Each line gives: the fix shape · the area or files · the size · whether it has a security surface.

1. **HPSMPOC-225**: anchor the ~20 API shape regexes with `\z` instead of `$`, plus one table-driven trailing-LF test.
   - Area: `api/src` Requests.cs Shape, ActionPlan/Finding/Reporting/Showcase endpoints, ShowcaseStartup, DevelopmentAuthentication, ReadinessResultReader. FeedbackEndpoints' page-path pattern goes to Lane 2.
   - Still open: `git grep` at `dc136e6` finds 23 `GeneratedRegex("…$")`. Only the import run id was fixed, in #119.
   - **M** · security **yes** (input validation).
2. **HPSMPOC-229**: build R3-2's second half, a sweep that reconciles pending import runs (check each stored path, then finish the run or mark it failed).
   - Area: `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportEndpoints.cs`.
   - Still open: #146 `a5fd635` did R3-1 and R3-2's first half only ("The pending-run sweep … is NOT built"). Must be done before imports are switched on on hosted.
   - **M** · security **yes** (untrusted upload path).
3. **HPSMPOC-250**: add three tests only (o1, o7, o8), each turned red by its mutant. No change under `api/src` or `web/src` (C-101).
   - Area: api tests for `ReportingEndpoints.cs` (the Demo name check).
   - **S** · security **yes** (tests on a privacy guard).
4. **HPSMPOC-134**: the remaining half of N-4 (i): a test that checks each operation's declared statuses against the code.
   - Area: `api/tests/.../Contract/`. N-5, N-8, N-9 and the wording half are merged (#70, #77, #104).
   - **M** · security no.
5. **HPSMPOC-246**: N-5 to N-7, which Friday routed on 13 Oct to "a timing lane after 13 Oct".
   - N-5: note or fix the log-template shape. N-6: stop 3213 logging the exception object, which carries the login name. N-7: test-only note.
   - Area: `api/src/HpsmPoc.Api/.../RequestTimingLog.cs`, `HostedDemo/HostedDemoStartup.cs:199-201`. N-4 belongs to the deploy seat and is not in this lane.
   - **S** · security **yes** (N-6 is a login name in the log).
6. **HPSMPOC-245**: N-4, N-5 and N-6, which Friday routed on 13 Oct into "the next BFF lane". Its blocker, #147, is merged.
   - N-4: re-check `STANDALONE_REQUIRED` in `scripts/deploy-package.py:82-86` and `web/scripts/package-standalone.mjs`.
   - N-5: a guard on `SendsFileContent => false` in `FeedbackDispatcher.cs:79-82`.
   - N-6: refuse the COM0 and LPT0 reserved names, CON + NBSP, and fullwidth CON in `FeedbackFiles.cs`.
   - **M** · security **yes**.
7. **HPSMPOC-228**: the remaining notes.
   - N-3: the R11 guard should see FeedbackDispatcher's timer (`infra/tests`).
   - N-4: template every non-fixed path segment in `bff.ts` routeTemplate (log privacy).
   - N-7: the report alert title "The report is taking longer than usual", which Kam approved in C-99 POC-12.
   - Already merged in #147/#133: N-2, N-6, N-8 and N-9. N-5 is superseded. The two timed-out save sentences wait on Kam's words card (POC-12 "to be drafted").
   - **M** · security **yes** (N-4).
8. **HPSMPOC-226**: the remaining feedback-attachment notes.
   - N-6: make the BFF enforce the 20 MiB file total, not only the 21 MiB request cap.
   - N-8: on a timeout after the commit, a retry duplicates the item (needs an idempotency shape).
   - B177 N-1/N-2: the meter and its words.
   - A1-N1: the "contract 0.12.0" comment at `ContractTests.cs:50`. Do it in Lane 1 with HPSMPOC-134, which owns that file.
   - Already done: N-4, N-5 and N-7 in #129. Kam ruled N-3 and N-9 as built (C-99 POC-8).
   - Area: `web/src/server` (feedback route) and `api/src/HpsmPoc.Modules.Feedback`.
   - **M** · security **yes**.
9. **HPSMPOC-235**: keep the BFF→API connections alive longer (a dispatcher for the API origin with a longer keep-alive). Measure first on the laptop.
   - Area: `web/src/server/bff.ts`.
   - Closing it needs a hosted measurement after a deploy, so it does not close tomorrow.
   - **M** · security no.
10. **HPSMPOC-98**: add the missing "Filter by state" to the Admin feedback list.
    - Area: the web Admin feedback screen. The list was built in #120 and the attempts count was added in #129 `3a9288a`, which states "Filter by state … is not built here".
    - **S** · security no.
11. **HPSMPOC-148**: three small items.
    - C-2: the discarded-plan message shows above another session's plan (web screen).
    - C-3: "At most 1 follow-ups" pluralisation (`FollowUpEndpoints.cs:77`).
    - N-3: the mock 429 carries no detail (mock `problem()`, `web/src/server/mock`).
    - **S** · security no. C-3 changes words, so show it to Kam if the shape changes.
12. **HPSMPOC-218**: move the braces exception date from 2026-10-31 to 2026-11-30, as Kam ruled (C-99 POC-4 (a)).
    - Where: `.github/workflows/ci.yml:375-376` still says "lapses after 2026-10-31". It goes through the CodeQL-gated PR route.
    - **S** · security **yes** (dependency exception). Deadline 31 Oct: from 1 Nov every web PR goes red.
13. **HPSMPOC-227**: fix or retarget the 3 failing live-API specs (6 tests), then add an on-demand-only CI job, as ruled (C-99 POC-7 (a)).
    - Area: `web/e2e/*live-api*.spec.ts` and a new `workflow_dispatch` workflow under `.github/workflows/`.
    - **M** · security **yes** (workflow).
14. **HPSMPOC-155**: add a pinned SQL Server container step to `ci.yml` (image by digest, a random `sa` password per run), plus a by-name check that the SQL Server tests ran (the Azurite pattern).
    - Area: `.github/workflows/ci.yml`, plus at most one new test-collection file.
    - Cost: CI time. Measure it, because the api job limit is now 25 min (#148).
    - **M** · security **yes** (CI secret).
15. **HPSMPOC-224**: add the Azure Monitor OpenTelemetry distro to the API and the web, with personal data scrubbed.
    - Kam ruled (C-99 POC-2 (a)): "after 13 Oct, … You see the deploy card before it is created."
    - Agent-actionable is the **build on a branch only**; the Azure resource and the deploy are on a card.
    - Area: `api/src/HpsmPoc.Api/Program.cs`, the web instrumentation file, `csproj` / `package.json`.
    - **L** · security **yes** (telemetry export, PII scrubbing).

## B. NEEDS KAM (58); the decision is named
- **HPSMPOC-1**: Commercial & Governance epic (`owner-kam`). It closes when its children close; open children are -3, -5, -6, -169 … -176 (all B), -82 … -86, -97 (C).
- **HPSMPOC-3**: name the Development Team and its Tech Lead. The PO approval that fully executes the SOW is HP's side.
- **HPSMPOC-5**: the event window and audience. The date is ruled (C-36 A, 1 Dec).
- **HPSMPOC-6**: name the Security SME (or confirm it is Kam) and a deputy PO.
- **HPSMPOC-11**: approve the M1 kick-off/cadence record draft (records/b109). The SME cadence is not recorded.
- **HPSMPOC-12**: PO review of the 7-minute script v1 (demo pack v0, records/b110).
- **HPSMPOC-13**: written PO approval of design pack v0.3.
- **HPSMPOC-14**: rule RS-03…RS-10 (scoring math), and say whether the file-based ruleset catalogue meets the "DB metadata" part of the title.
- **HPSMPOC-16**: sign off the stack decision record once the list of §4.1 deviations is added.
- **HPSMPOC-19**: does the coded prototype replace Figma (comment 38110, unanswered)?
- **HPSMPOC-20**: written PO approval of the prototype (M2 gate evidence).
- **HPSMPOC-24**: Entra sign-in works on hosted Demo (B238: demo Admin signed in first time). The ticket's bar is UAT, which is not provisioned (card K-3 / C-52).
- **HPSMPOC-29**: the M3 happy path in UAT. UAT needs provisioning (Kam, Azure).
- **HPSMPOC-31**: approve the HPSMPOC-87 question set so that it loads as v1 (SME = Kam).
- **HPSMPOC-35**: the SME's approved remediation per finding. The machinery is done; the text is placeholder.
- **HPSMPOC-44**: report language and disclaimers approved for event use (SME = Kam).
- **HPSMPOC-46**: approved HP/HPSM policy-configuration examples (SME = Kam).
- **HPSMPOC-47**: waits on HPSMPOC-46. The config is synthetic and no code is left.
- **HPSMPOC-48**: waits on HPSMPOC-46. The placeholder guidance line is still printed.
- **HPSMPOC-51**: baseline hours with their source; approve metrics M1–M7.
- **HPSMPOC-52**: confirm T_idle/T_last (QA-129). The override metric's dependency, -36, is closed.
- **HPSMPOC-55**: SME trial runs (and the HPSMPOC-51 baseline).
- **HPSMPOC-57**: provision Dev and UAT (card K-3). Demo is live.
- **HPSMPOC-58**: half 2, the deploy job with a federated Entra credential, is Kam's. CI and branch protection are done.
- **HPSMPOC-60**: the Playwright journey must pass in UAT and Demo (needs UAT, plus hosted runs inside Kam's windows).
- **HPSMPOC-61**: UAT execution. The M6 acceptance-test script is drafted for Kam (records/b114).
- **HPSMPOC-62**: M7 freeze, fallback and rehearsal. These are event-gated (date, window).
- **HPSMPOC-63**: M8 event-day on-call and handover (not yet due; HP accepts the handover).
- **HPSMPOC-64**: a hypercare window that ends by 31 Dec (Kam and HP).
- **HPSMPOC-87**: approve the DRAFT aligned question set (In Progress).
- **HPSMPOC-90**: the route-A Jira Automation rule and secret on hosted, and the end-to-end delivery proof (see HPSMPOC-109).
- **HPSMPOC-92**: next phase only. Priorities go in the Phase 2 backlog; Friday kept it parked on 13 Oct (comment on HPSMPOC-232).
- **HPSMPOC-96**: next phase only (voice assessment). Kam's Phase 2 priorities.
- **HPSMPOC-99**: N-4 asks whether Kam's Automation rule has the duplicate check. N-9 waits for a scale-out.
- **HPSMPOC-100**: K10, the retention period for client follow-up contact data (proposed 12 months).
- **HPSMPOC-109**: O-1, how a "sent" route-A item is proved delivered. O-2 is merged (#105).
- **HPSMPOC-117**: whether LEDGER tamper evidence is needed before any real customer data. Parked by Friday on 13 Oct.
- **HPSMPOC-162**: a DRAFT phase-one AI-at-the-printer position for Kam, then Steve and Paul. Content is SME territory (CLAUDE.md "do not invent security policy").
- **HPSMPOC-163**: DRAFT meanings for the traffic-light bands, for Kam and then HP vetting.
- **HPSMPOC-164**: whether the HP review-session readiness items are closed. The hosted link exists; feedback delivery on hosted is unproven (HPSMPOC-109).
- **HPSMPOC-165**: the first "good" consulting package (Kam, Paul, Peter).
- **HPSMPOC-168**: the fleet-size fit note (yes/no, and the threshold, 250 or 2,500, unsettled). The industry half is built and ruled (C-93, C-94, #135).
- **HPSMPOC-170**: review the admin guide v0 (records/b110). The UAT walk-through needs UAT.
- **HPSMPOC-171**: review the known-limitations and test-evidence index v0.
- **HPSMPOC-172**: review demo pack v0, plus the story, audience and date confirmation.
- **HPSMPOC-173**: Phase 2 backlog priorities (v0 drafted).
- **HPSMPOC-174**: hours for the weekly status reports (card K-10); Kam sends to HP.
- **HPSMPOC-175**: the two CONFIRM placeholders (Azure OpenAI tenant; no-training confirmation per tool). The record is drafted.
- **HPSMPOC-176**: confirm the controller contact; approve the RoPA and privacy notice drafts.
- **HPSMPOC-177**: Kam's word on refusing invisible characters in feedback comments. #129 left that rule unchanged on purpose.
- **HPSMPOC-178**: Kam's word on refusing hidden and text-direction characters in customer names.
- **HPSMPOC-187**: second half: one action sentence repeated per finding in the approved template text, which "is not ruled by Kam's card". The first half is merged (#95, C-48).
- **HPSMPOC-193**: VNet integration or a BFF shared-secret header for KnownProxies. This is an infra/secret change on hosted, and the residual has been live since C-59.
- **HPSMPOC-196**: forwarded-header shape measurement at the next hosted deploy. It needs Kam's window (C-103); nothing is hosted on 14 Oct.
- **HPSMPOC-203**: does an issued report keep its issue-time file name? Option (b) needs a schema change.
- **HPSMPOC-204**: approve the wording of the PDF profile caption.
- **HPSMPOC-237**: money: B1 versus a larger plan or separate plans. The Server-Timing prerequisite exists.
- **HPSMPOC-242**: Paul's detailed showcase feedback, through Kam (comment of 9 Oct: "detailed test … over the weekend").

## C. NEEDS HP OR ANOTHER HUMAN (16)
- **HPSMPOC-21**: HP brand assets. C-49: the PDF waits for them.
- **HPSMPOC-37**: HP approval of the demo-scenario scores (H-2, for M4).
- **HPSMPOC-82**: a live Security Manager system and HP's integration overview and API reference.
- **HPSMPOC-83**: Quick Assess access. HP's 2 Oct narrowing (HPSMPOC-181) says Quick Assess is out.
- **HPSMPOC-84**: Control Hub access, owned by Steve.
- **HPSMPOC-85**: access to the firmware vulnerability tool and how to integrate it.
- **HPSMPOC-86**: Fleet Threat Assessment assets and access.
- **HPSMPOC-94**: HP's expert remediation knowledge base (the session Steve is arranging).
- **HPSMPOC-97**: the checklist of HP follow-ups from 29 Sep.
- **HPSMPOC-166**: the checklist of HP follow-ups from 1 Oct.
- **HPSMPOC-167**: HP's current generic partner deck.
- **HPSMPOC-180**: waits for the HP-vetted weights re-issue (C-32 #6). The schema bump rides on it.
- **HPSMPOC-181**: HP's four access and input workstreams.
- **HPSMPOC-191**: answers from Terry (HP) to the 8 integration questions. E1 and E2 are done (B108).
- **HPSMPOC-240**: a supported HP printer or simulator reachable from vm-hpsm-sm.
- **HPSMPOC-241**: answers to the 21 questions Kam sent Terry on 8 Oct.

## D. EFFECTIVELY DONE BUT STILL OPEN (10): evidence
- **HPSMPOC-88**: B49 #51 `1bcbeb1` built the audience model, and B56 #54 `99a5ac6` loaded the five sections (content 0.5.0, C-32). The ticket's own condition was "Keep In Progress until B56 merges 0.5.0". The section wording stays DRAFT under HPSMPOC-87.
- **HPSMPOC-91**: all three packs are built. #50 `70eb4f0` built packs 1 and 3, and B55 #53 built pack 2 (`ClientPacks.test.tsx:85` "pack 2 is built"). What remains is Kam/SME wording on the marked placeholders (K7), which could be one line on HPSMPOC-44.
- **HPSMPOC-95**: Kam ruled C-32 "Tiers as groupings only … no prices". Built in #54 `99a5ac6` and #57 `f403251`.
- **HPSMPOC-127**: Kam ruled C-47 (b) and approved the 1.0.2 words (C-54). Merged as #99 `04aae93`, which is in the deployed `dc136e6`. The comment says "Closing it is Friday's call (Q-B127-2)".
- **HPSMPOC-159**: #147 `b7dbaf9`: "HPSMPOC-159: resetShowcase reads the 503's problem+json". Live in B238's `dc136e6`.
- **HPSMPOC-238**: #134 `03bd293`: "F-22 waits for the action plan's loaded content, not networkidle".
- **HPSMPOC-239**: #134 `03bd293`: "the file-scanning web unit tests get an explicit timeout with the reason".
- **HPSMPOC-243**: N-2 is live (#130), N-1 is live (#132, C-82), and the M-1 test gap is fixed (#133 `a50b22d` "HPSMPOC-243 M-1"), hosted since C-83.
- **HPSMPOC-244**: #147 `b7dbaf9`: "an F-22 sibling whose partner HAS a plan … (tests only)".
- **HPSMPOC-247**: #146 `a5fd635`: "cap-file test runs alone (HPSMPOC-247)". This is the ticket's recommended option (b).

## E. UNCLEAR (14)
- **HPSMPOC-10, -18, -23, -30, -38, -45, -50, -56**: epics. They are containers with no work of their own and close when their children close. HPSMPOC-56 is the parent of several A tickets (-232 … -247).
- **HPSMPOC-126**: a checklist of hosted measurements that was never ticked. Later deploys measured some items (B238: start limits 600/600; Entra sign-in works). A records seat could reconcile it against B198, B210, B221 and B238, but which items are still owed is unclear.
- **HPSMPOC-169**: re-basing the gate pack on the signed SOW is agent work in principle (matrix SD-01/SD-36 exists). Its source is the signed SOW, which this screen's Restricted hold does not open. Friday decides whether the matrix is enough.
- **HPSMPOC-207**: a watch item. 3211 and 3213 recurred at B238's start. B238 Open 2 points to HPSMPOC-248/-249, which are not open. The ticket names no next step.
- **HPSMPOC-220**: an umbrella ticket for the SM import. A1–A3 are merged (#116, #119, and the follow-ups #136/#138/#140/#146), but what is still owed (the A5 upload screen? switch-on?) is not stated on the ticket.
- **HPSMPOC-232**: Friday accepted reading (b) on one start. A rolled-back write warm-up was named as the post-13-Oct candidate, but the 13 Oct comment says "window … spent … Not reopened". B238 now gives a second start (1,719 ms; caller 1,087, of which write 986). Friday needs to say whether to build or close.
- **HPSMPOC-234**: parked by Friday on 13 Oct. The render warm-up needs PORT allowed by infra, which is a hosted change.

---

## Lanes for A: 3 lanes, file-disjoint

**Lane 1: API correctness and tests** (`api/src` outside `Modules.Feedback`, and `api/tests`)
- Tickets: HPSMPOC-225 (without the FeedbackEndpoints pattern), -229, -250, -134 (plus -226's A1-N1 one-word fix in `ContractTests.cs:50`), -246 (N-5 to N-7).
- Files: Requests.cs, Action/Finding/Reporting/Showcase endpoints, ShowcaseStartup, DevelopmentAuthentication, ReadinessResultReader, `Ingest/ImportEndpoints.cs`, RequestTimingLog.cs, HostedDemoStartup.cs, and api tests (Contract, Reporting, Ingest, a new shape test).
- Size: 2 M, 3 S. Most of it is tests-first; no contract change is expected.

**Lane 2: BFF, web and Feedback** (`web/src` except instrumentation, `web/src/server/**`, `web/scripts/package-standalone.mjs`, `scripts/deploy-package.py`, `api/src/HpsmPoc.Modules.Feedback/**`, `FollowUpEndpoints.cs`, `infra/tests`)
- Tickets: HPSMPOC-245, -228, -226 (N-6, N-8, B177), -235, -98, -148, and FeedbackEndpoints' page-path regex from -225.
- Friday already named this "the next BFF lane" on HPSMPOC-245 (13 Oct), and its blocker #147 is merged.

**Lane 3: CI workflows and telemetry** (`.github/workflows/**`, `web/e2e/*live-api*.spec.ts`, `api/src/HpsmPoc.Api/Program.cs`, the web instrumentation file, `csproj`/`package.json`)
- Tickets: HPSMPOC-218, then -227, then -155, then -224 (build only; the Azure resource is on a deploy card).
- Every workflow change goes through the CodeQL-gated PR route (memory: datasec-github-codeql-policy).

**Start first: Lane 2.**
- Friday already unblocked and scoped it (HPSMPOC-245, 13 Oct).
- It carries the words Kam approved in C-99 POC-12, which are not built yet (HPSMPOC-228 N-7).
- It owns `scripts/deploy-package.py`. That is where B238's unticketed live-check `.tar.zst` gap lives: B238 Open 1 says "Every web deploy (and rollback) from now on ends rc 3 until it can". Fixing it in this lane, once Friday files the ticket, clears the next deploy before Kam names a window.
- Run Lane 3's HPSMPOC-218 beside it as a one-line PR. It is S and has the only hard date (31 Oct).
- Lane 1 can run in parallel without conflict.

## Not on the board (A-shaped, NOT counted above)
These come from BACKLOG.md, B238 and C-99, and have no open ticket:
- The live-check `.zst` gap (B238 Open 1; Friday's ticket candidate).
- POC-9 (b): the web page asks only when the record says a profile or score exists (BACKLOG B208 row; ruled, "Not built yet").
- POC-5 (a): withhold free text in Demo (ruled; "a priority lane").
- POC-3 HSTS: the header change, built after 13 Oct, deploys on a card.
- The B202 `RequestTimingLogTests` 1 ms-under flake.
- The stale e2e title at `web/e2e/hosted-reset.spec.ts:55` (B238 Open 4).
