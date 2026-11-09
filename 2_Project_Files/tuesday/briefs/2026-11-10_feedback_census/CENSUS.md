# HPSM-POC feedback census (2026-11-10, read-only, 09:13 AEDT)

## BLUF for the product owner

**Every feedback item that has a fix is already on UAT. A deploy of current main (0820efe9) would add no feedback fix.** It would also put the old step 10 caveat on UAT, which you ruled out at 09:03.

**Counts.** There are 57 items in three groups, from Jira `HPSMPOC`, each counted once. A further 13 items were ruled next phase on 9 Nov, listed in section D.

| State | A. Feedback-button items | B. HP reviewer and showcase feedback | C. HP meeting asks | Total |
|---|---|---|---|---|
| FIXED-AND-ON-UAT (the fix is at or before 884fd72b) | 4 | 22 | 3 | **29** |
| FIXED-ON-MAIN, not on UAT | 0 | 0 | 0 | **0** |
| OPEN, agent-actionable | 0 | 3 (389, 401; 399 needs a records close only) | 0 | **3** |
| OPEN, needs your word or decision | 0 | 11 | 9 | **20** |
| NEXT-PHASE | 0 | 0 | 2 | **2** (plus 13 in the Phase 2 catalogue) |
| Not feedback (synthetic or deploy-test rows) | 3 | 0 | 0 | **3** |
| **Total** | **7** | **36** | **14** | **57** |

Section E lists 31 more tickets about the Feedback button's own engineering. Six of them are still open, and none was fixed by the five new PRs.

**What a deploy of main 0820efe9 would deliver.** It would add five PRs: #298, #299, #300, #301 and #302. None of them closes a feedback item:
- #298: sign-in token renewal is shared across parallel calls (HPSMPOC-228 N-5, an engineering note from a review gate).
- #299: the step 10 caveat in the Demo Walkthrough, from gate finding B1390-1. **This carries the OLD wording.** At 0820efe9, `web/src/content/walkthrough/steps.ts:130` reads "...score the assessment and approve the narrative before you show it...". UAT at 884fd72b has the shorter caveat, without that clause. Your 09:03 ruling (option b) says to reword without the score-and-approve instruction first. **Deploying main as it stands would put the wording you rejected on UAT.** The reword branch `b1392/hpsmpoc-caveat-reword` (B1392 ADDENDUM-2) did not exist at 09:13: `matching-refs/heads/b1392` returns only `-web-ui` and `-web-ui-d`. There are no open PRs.
- #300: one row spacing in Recent activity (HPSMPOC-439), and the mock's 400 list (HPSMPOC-323 B478-4). Both are gate findings.
- #301: tests and CI tooling only (HPSMPOC-352, HPSMPOC-356).
- #302: the API refuses a finding explanation when there is no visible finding (HPSMPOC-436).

**What a deploy of main would NOT deliver.**
- HPSMPOC-405 remainder: the Feedback pill still covers a row's Actions button at scroll 0 at 1280x900 and 1535x864. B1392 left this HELD for a scope call about where the pill goes (`B1392_STATUS.md:55`, `:125`), so it is not built.
- Every open item in the table needs a decision from you, input from HP, or an agent lane that has not yet been briefed.
- The Partner Readiness changes are not in the five PRs. #296 (squash fa401da9) is already on UAT: it is one commit before 884fd72b. A separate investigator is looking at why they cannot be seen.

**One gap I could not close under the read-only rules.** On UAT the feedback route is OFF (CLARIFICATIONS `:2175`, as relayed in the B1302 kit). Items sent on UAT are saved in UAT's own database and never reach Jira. They reach Jira only when a seat copies them by hand, as was done for 441 and 442 on 3 Nov. No Jira issue has been created since 6 Nov apart from the Phase 2 catalogue of 9 Nov (448-460). Any feedback sent on UAT after 3 Nov is therefore visible only on UAT's "Feedback received" page and on the approval page. **I did not read either page, because that needs a sign-in to an app host.** Someone who can open those two pages needs to read them before this census can be called complete.

## Method and pagination proof

- **Where feedback lives:**
  - C-30 in `1_Project_Definition/CLARIFICATIONS.md:173` (the button: items go to the Jira board and by email), and `:175` (asks to HP).
  - The Feedback module README on main: the route-B label is `hp-feedback` (`Feedback:Label`), with a per-item idempotency label `hp-feedback-id-<id>` (`JiraRestMailSink.cs:49`). Route A (the Jira Automation webhook) creates `[HP feedback] <Category>: ...` issues labelled `hp-feedback`.
  - Items the product owner sends on UAT are copied by hand as `[UAT feedback FB-...]`, labelled `po-feedback`.
  - HP's v1.2 design and click-through notes became 33 tickets labelled `design-v12`. The source is `Source_Documents/2026-10-29_hp-feedback-v1-2-design-and-click-through-notes/`, which is git-ignored.
  - HP meeting asks are labelled `c30-…`, `c31-…` and `c34-…`. The showcase placeholder is HPSMPOC-242. The reviewer-walk word pack is HPSMPOC-310.
- **Reader:** a GET-only script at the scratchpad path `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/00755d0b-17ed-4742-8f90-5ae73a7a41a9/scratchpad/jr/jira_get.py`. It loads `4_Credentials/.env` in-process, uses only `/rest/api/3/search/jql` and `/rest/api/3/issue/{key}`, and prints no token. Every JQL has the form `project = HPSMPOC AND ( ... ) ORDER BY key ASC` and follows `nextPageToken` until it is gone.
- **Pagination proof (as printed):**
  - `key is not EMPTY`: pages=5, issues=460, isLast=True, nextPageToken=none. This is the whole project.
  - `labels is not EMPTY`: pages=5, 458.
  - `labels in (feedback, hp-feedback, po-feedback) OR summary ~ "feedback" OR issuetype = Epic`: pages=1, 53.
  - The design, request and decision labels query: pages=2, 106.
  - `labels in (c30…, c31…, c34…, c45…, word-pack…) OR summary ~ "B377"…`: pages=1, 24.
  - `created >= "2026-11-04"`: pages=1, 18.
- **Label counts across the whole project:** `hp-feedback` 5, `po-feedback` 2, `design-v12` 33, `feedback` 15 (engineering), `layout-v2-1` 13, `hp-request` 8, `awaiting-hp` 9. The `hp-feedback-id-*` label appears 0 times, so route B has never filed an issue.
- **On UAT or not:** main has only squash merges, and `compare 884fd72b...0820efe9` shows ahead 5, behind 0. I ran `compare <fix>...884fd72b` for each of the 30 fix commits cited below. All 30 came back "ahead, behind=0", so each one is an ancestor of the UAT build.
- **file:line:** read with `gh api -X GET contents?ref=0820efe9`. Items whose fix is only a PR or squash are cited that way.

## A. Feedback-button items (label `hp-feedback` or `po-feedback`): 7

| Key | Summary (paraphrased) | Status | Date | Raised by (role) | What it asks | State against the code |
|---|---|---|---|---|---|---|
| HPSMPOC-102 | Route A test 2 (SYNTHETIC) | Done | 2026-09-29 | coordinator seat (test) | none: a test row | NOT FEEDBACK (synthetic, closed by B58) |
| HPSMPOC-103 | B58 end-to-end test (SYNTHETIC) | Done | 2026-09-29 | build seat (test) | none | NOT FEEDBACK |
| HPSMPOC-190 | Idea: move Feedback to the bottom right, orange, floating over the site | Done | 2026-10-03 | Admin-role sender on the hosted site; adopted by the product owner's rulings C-42/C-43 | floating orange pill, bottom right | **FIXED-AND-ON-UAT**: PR #86, squash c2dd403. `web/src/components/feedback/FeedbackPill.module.css:13-15` (position fixed, right and bottom) |
| HPSMPOC-221 | Bug: an error on the narrative screen | Done | 2026-10-06 | Admin-role sender on the hosted site | no error when the narrative or report loads | **FIXED-AND-ON-UAT**: 25 s AI cap (C-72) and warm-up #121 (19c57ee); proved live on the c28343a deploy (C-78). Both are ancestors of 884fd72b |
| HPSMPOC-230 | Deploy test of 547d3ea | Done | 2026-10-07 | build seat (deploy check) | none: "Not a product report" | NOT FEEDBACK |
| HPSMPOC-441 | [UAT feedback FB-01a19e7a] No Menu button in the header; a hamburger collapses the rail to icons; logo on the left | Done | 2026-11-03 | product owner | three shell layout changes | **FIXED-AND-ON-UAT**: PR #285, squash fc2bc2fc. `web/src/components/shell/Sidebar.tsx:92-93` (the "Collapse menu" control) |
| HPSMPOC-442 | [UAT feedback FB-01a19e8b] A first feedback category to run an idea past the HP reviewer, held until approved, and an approval page | Done | 2026-11-03 | product owner | held category, plus approve or delete before Jira | **FIXED-AND-ON-UAT**: PR #280, squash 69338b64. `api/.../Endpoints/FeedbackEndpoints.cs:54` (`ReviewCategory`), `:127` (held), `web/src/app/(app)/admin/feedback/review/page.tsx:8,13`. The later title change (B1257/B1263) and the "open to anyone from the logo" change (B1302) are follow-on instructions of 4 and 5 Nov, not new feedback items |

## B. HP reviewer and showcase feedback: 36

| Key | Summary (paraphrased) | Status | Date | Raised by (role) | What it asks | State against the code |
|---|---|---|---|---|---|---|
| HPSMPOC-242 | Placeholder: an HP attendee's feedback from the 7 Oct showcase | Backlog | 2026-10-08 | HP partner-side showcase attendee, via the product owner | general agreement so far; the detailed notes have not been supplied | **OPEN-NEEDS-PO**: the notes are still owed (comment of 23 Oct). Nothing to build yet |
| HPSMPOC-310 | Word pack items 3-8 from the hosted reviewer walk (B377) | Done | 2026-10-21 | hosted reviewer walk (B377) | time zones, Home title, spellings, tools label, 401 text, unknown-customer text | **FIXED-AND-ON-UAT**: PR #192 (ee26d9fc) and PR #194 (7c9f66c2). `web/src/lib/dates.ts:2,7` (zone on every time). Item 5a (US/UK spellings) was left as it is |
| HPSMPOC-369 | v1.2 grouped menu sections and per-role entries | Done | 2026-10-29 | HP reviewer (v1.2 design notes) | per design | **FIXED-AND-ON-UAT**: #240 9659148c, #249 37bc6323, #256 2d0f0a17 |
| HPSMPOC-371 | v1.2 shared components restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #241 94274a75 |
| HPSMPOC-372 | v1.2 Partner home, two columns | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #252 c69febbb |
| HPSMPOC-373 | v1.2 Customers and Engagements lists | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #255 41922a36 |
| HPSMPOC-374 | v1.2 customer frame, tabs, journey rail | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #245 332dcc6f |
| HPSMPOC-375 | v1.2 journey steps 1-2 restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #260 e8ac3f29 |
| HPSMPOC-376 | v1.2 journey steps 3-5 restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #257 edf36342 |
| HPSMPOC-377 | v1.2 Roadmap remediation register | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #257 edf36342 |
| HPSMPOC-378 | v1.2 journey steps 6-8 and Metrics restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #259 a026cb30 |
| HPSMPOC-379 | v1.2 Tasks, Documents, Coach tabs | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #258 297be679 |
| HPSMPOC-380 | v1.2 My readiness page | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #249 37bc6323 |
| HPSMPOC-381 | v1.2 Training and playbooks page | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #249 37bc6323 |
| HPSMPOC-382 | v1.2 Action plan restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #248 7c353747 |
| HPSMPOC-383 | v1.2 Service offers page | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #256 2d0f0a17 |
| HPSMPOC-384 | v1.2 Revenue calculator restyle | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #254 7e5d652e |
| HPSMPOC-385 | v1.2 Resources module grid | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #247 571fc9d9 |
| HPSMPOC-386 | v1.2 Metrics, Attribution, Administration | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #246 b5b6aa34 |
| HPSMPOC-387 | v1.2 Customer security workspace A | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #253 32fc1750 |
| HPSMPOC-388 | v1.2 Customer security workspace B | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #269 1f4bf7bc, #271 a3a06b9a |
| HPSMPOC-397 | v1.2 sidebar tests | Done | 2026-10-29 | HP reviewer (v1.2) | per design | **FIXED-AND-ON-UAT**: #240 9659148c |
| HPSMPOC-402 | v1.2 Previous-button follow-ups | Done | 2026-10-30 | gate on v1.2 work | per design | **FIXED-AND-ON-UAT**: #259/#260/#263/#254/#255 (a026cb30, e8ac3f29, c364caf0, 7e5d652e, 41922a36) |
| HPSMPOC-368 | v1.2 shell: persistent left sidebar and top bar | Backlog | 2026-10-29 | HP reviewer (v1.2) | per design | Built and on UAT (#240 9659148c, #282 a8497578). Still open because clause 2 is not met as written: the collapsed icon rail is not inert (records check of 10 Nov at 884fd72b). **OPEN-NEEDS-PO**: decide whether the collapse your own feedback 441 asked for meets this clause |
| HPSMPOC-370 | v1.2 top-bar customer picker ("the product owner may drop it") | Backlog | 2026-10-29 | HP reviewer (v1.2) | keep or drop the picker | Built and on UAT (#240). **OPEN-NEEDS-PO**: keep or drop (tied to 391) |
| HPSMPOC-389 | v1.2 cross-page quality check after all lanes | Backlog | 2026-10-29 | HP reviewer (v1.2) | a11y, keyboard, responsive, print | **OPEN-AGENT-ACTIONABLE** (a measuring lane; no word needed) |
| HPSMPOC-390 | v1.2 needs input: role definitions, Customer role? | Backlog | 2026-10-29 | HP reviewer (v1.2) | definitions | **OPEN-NEEDS-PO**: a draft exists (B1443, today). Phase 2 ticket 451 also covers the Customer role |
| HPSMPOC-391 | v1.2 needs input: switching customers inside a customer page | Backlog | 2026-10-29 | HP reviewer (v1.2) | keep or drop the picker | **OPEN-NEEDS-PO** |
| HPSMPOC-392 | v1.2 needs input: Good/Better/Best packages and labels | Backlog | 2026-10-29 | HP reviewer (v1.2) | words and pricing reading | **OPEN-NEEDS-PO** |
| HPSMPOC-393 | v1.2 needs input: framework alignment mapping | Backlog | 2026-10-29 | HP reviewer (v1.2) | an approved standards mapping | **OPEN-NEEDS-PO** (HP or SME content; Phase 2 ticket 460 holds it) |
| HPSMPOC-394 | v1.2 needs input: the five independent assessment principles | Backlog | 2026-10-29 | HP reviewer (v1.2) | content, and whether the page is in scope | **OPEN-NEEDS-PO**: draft from B1443. HP's v1.2 prototype may already list the five |
| HPSMPOC-395 | v1.2 needs input: audience testing plan | Backlog | 2026-10-29 | HP reviewer (v1.2) | a plan | **OPEN-NEEDS-PO**: draft from B1443 |
| HPSMPOC-396 | v1.2 needs input: branding, metric scope, calculator inputs | Backlog | 2026-10-29 | HP reviewer (v1.2) | decisions | **OPEN-NEEDS-PO** |
| HPSMPOC-399 | v1.2 follow-ups B908-4/-6/-7/-8 | Backlog | 2026-10-30 | gate on v1.2 work | layout fixes | All four FIXED-AND-ON-UAT: CLOSED-WITH-EVIDENCE in `B1392_STATUS.md:44-47` (CustomerManagement.tsx:114, shell-sidebar.spec.ts:442-443, parts.tsx:69, globals.css:123-125 at fa401da9). **OPEN-AGENT-ACTIONABLE (records only)**: the ticket can be closed |
| HPSMPOC-401 | v1.2: tables in sideways-scroll regions reach too far right | Backlog | 2026-10-30 | gate on v1.2 work | layout fix | **OPEN-AGENT-ACTIONABLE** (not in any of the five PRs) |
| HPSMPOC-164 | HP review sessions: a build HP can open, with the feedback button live | Backlog | 2026-10-01 | HP meeting (via the product owner's notes, C-34) | a live feedback route for HP | **OPEN-NEEDS-PO**: you ruled the route OFF on UAT and ON on the demo. Whether HP should send on UAT is your call |

## C. HP meeting asks (C-30, C-31, C-34; asks made of Datasec, not asks of HP): 14 (164 is counted in B)

| Key | Summary (paraphrased) | Status | Date | Raised by (role) | State |
|---|---|---|---|---|---|
| HPSMPOC-87 | Customer questions: the 16 as a base, aligned to policy principles (draft) | In Progress | 2026-09-29 | HP meeting attendees | **OPEN-NEEDS-PO** (draft for your word). Possibly the Partner Readiness questions. The other investigator owns that question |
| HPSMPOC-88 | Playbook sections by audience | Done | 2026-09-29 | HP meeting | **FIXED-AND-ON-UAT** (merged before 884fd72b, which is on a linear main) |
| HPSMPOC-89 | Unanswered questions sent to the client to complete | Done | 2026-09-29 | HP meeting | **FIXED-AND-ON-UAT** (as 88) |
| HPSMPOC-90 | The Feedback button itself (Jira issue plus email) | In Progress | 2026-09-29 | product owner (C-30) | Built (route A, ruled 29 Sep). **OPEN-NEEDS-PO**: the route is off on UAT by ruling; ticket closure is yours |
| HPSMPOC-91 | Client collateral packs, pre, during and post | In Progress | 2026-09-29 | HP meeting | **OPEN-NEEDS-PO** (needs SME content and your word) |
| HPSMPOC-92 | Align to more sophisticated engagements | Backlog | 2026-09-29 | HP meeting | **NEXT-PHASE** |
| HPSMPOC-94 | Guided expert remediation from HP's knowledge base | Backlog | 2026-09-29 | HP meeting | **OPEN-NEEDS-PO** (needs HP content) |
| HPSMPOC-95 | Good / better / best tiers with revenue lines | Done | 2026-09-29 | HP meeting | **FIXED-AND-ON-UAT** |
| HPSMPOC-96 | Voice / conversational assessment | Backlog | 2026-09-29 | HP meeting | **NEXT-PHASE** |
| HPSMPOC-162 | AI at the printer: a phase-one position (draft for HP review) | Backlog | 2026-10-01 | HP meeting | **OPEN-NEEDS-PO** (needs HP content) |
| HPSMPOC-163 | Traffic-light meaning (draft for HP vetting) | Backlog | 2026-10-01 | HP meeting | **OPEN-NEEDS-PO** |
| HPSMPOC-164 | HP review sessions (listed in B) | Backlog | 2026-10-01 | HP meeting | see B |
| HPSMPOC-165 | Consulting offer content, G/B/B | Backlog | 2026-10-01 | HP meeting | **OPEN-NEEDS-PO** |
| HPSMPOC-167 | Phase pages aligned to HP's current partner framing | Backlog | 2026-10-01 | HP meeting | **OPEN-NEEDS-PO** (awaiting HP's deck) |
| HPSMPOC-168 | Industry choices and a fleet-size note (proposal) | Backlog | 2026-10-01 | HP meeting | **OPEN-NEEDS-PO** |

Excluded as asks OF HP, not feedback: HPSMPOC-82 to -86, -97, -166, -181, -241 (awaiting HP) and -191 (SM integration).

## D. Phase 2 catalogue (13: HPSMPOC-448 epic plus 449-460)

The v2.1 layout was reviewed with the partners in mind. You ruled on 9 Nov that these are "the first changes of phase 2", to be catalogued and not made now. All 13 are in Backlog. **NEXT-PHASE.**

## E. Engineering tickets on the Feedback feature itself (gate notes, not user feedback): open ones

| Key | What | State |
|---|---|---|
| HPSMPOC-405 | The Feedback pill covers a row's Actions button | Part fixed and on UAT (#274 4b3cefae, room at the end of the page). The remainder is HELD for a scope call on where the pill goes (`B1392_STATUS.md:55`). **OPEN-NEEDS-PO**. Not in the five PRs |
| HPSMPOC-99 | QA notes N-4, N-7, N-8, N-9 | N-7 and N-8 were closed with evidence on main (`B1394_STATUS.md:42-43`) and on UAT. N-4 needs your route ruling (NEEDS-PO). N-9 waits for a hosted scale-out |
| HPSMPOC-109 | O-1: route A "sent" is not proof of delivery | O-2 is met (ci.yml:602). **O-1 is OPEN-NEEDS-PO** |
| HPSMPOC-226 | Attachment follow-ups | All closed, built or accepted, except B177 N-1 (words for a slow sender): **OPEN-NEEDS-PO** |
| HPSMPOC-257 | NFKC over-refusal of some file names | **OPEN-NEEDS-PO** (a decision) |
| HPSMPOC-315 | A flaky lease-lost note | Closed with evidence on main (PR #200), and on UAT. Only the 60-run SQL Server loop is held. **Records close (agent)** |

Done and on UAT: 98, 133, 177, 179, 216, 258, 260, 265, 276, 279-281, 284-286, 288-290, 294, 306, 308, 314, 317, 340, 347.

## Mapping the five PRs not yet on UAT to feedback items

| PR | Squash | Tickets | Feedback item it closes |
|---|---|---|---|
| #298 | 192c0a94 | HPSMPOC-228 N-5 | none |
| #299 | 90d30d5f | gate B1390-1 (step 10 caveat) | none. **This is the old wording, which you ruled must be reworded first** |
| #300 | 0820efe9 | HPSMPOC-439, HPSMPOC-323 B478-4 | none |
| #301 | 7d4e3142 | HPSMPOC-352, HPSMPOC-356 | none (tests and CI only; nothing that ships runs it) |
| #302 | 856d15d1 | HPSMPOC-436 | none |

**Deploy recommendation (for the coordinator, not acted on):** land the caveat reword first, then deploy main to UAT. That deploy carries five quality fixes and no feedback fix. Before calling the feedback census complete, someone with access to UAT's "Feedback received" and approval pages must read them, because UAT's route is off and its items are not in Jira.
