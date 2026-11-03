# B1205 DESIGN - the product owner's "Run idea / feedback past Steve" request (HPSM-POC)

Drafted 2026-11-03 11:13 AEDT. Code read at origin main f464376b1f7b62e4a5bf0c73af6c14a8c29993ea (gh api -X GET, raw contents; every file:line below printed by awk/grep -n from those files).
Item: FB-01a19e8b-10b4-7fd8-86a3-7082b09a6f71, idea, page /home, Partner role, 2026-11-02T23:14:36Z (Briefs/2026-11-03_B1202_evidence/kam-feedback-items.md). His words, verbatim:
"Add as the first item in feedback What is it about - "Run idea / feedback past Steve" / add a new page that allows Steve to navigate to a feedback with all these submissions (the ones with his name) and approve or delete.  Once approved, they get submitted to Jira - Kam"
He wrote a slash with spaces: `Run idea / feedback past Steve`. Use it exactly.

## Who is Steve (sources, how sure)
- MEASURED: HP meeting 2026-09-29 with Steve Inch, Peter Blanchard, Paul Waite (CLARIFICATIONS.md:165). The deck lists "Steve Inch ... Channel Security Services Playbook Program Creator/Owner/Lead" (Source_Documents/2026-09-24_playbook-deck-v3/deck_text.md:1272). The Q&A set calls him the likely HP Sponsor, "inferred" (Questions_and_Answers/README.md:94, 00_MASTER_QA.md:74). The product owner himself wrote "feedback from Steve (HP)" (Briefs/2026-10-16_B250_ADDENDUM-2:7).
- Sure enough: the only Steve in the records is Steve Inch of HP (greps over 1_Project_Definition, control: "blanchard" 1 hit in B48 fired). The comment does not give a surname: HIGH likelihood, not confirmed by him. His job title beyond the deck line is UNKNOWN.

## How it works today (origin main)
- Button: FeedbackButton.tsx:24-29 CATEGORIES = bug "Something doesn't work", idea "An idea", content "The content", question "A question"; legend "What is it about?" at :56. The type is the contract enum (feedbackApi.ts:11).
- Category is checked in 4 places: FeedbackEndpoints.cs:53 (list), :231-232 (message "Choose bug, idea, content or question."), FeedbackDbContext.cs:128 (CHECK ck_feedback_category), openapi.yaml:3549 (and 3604, 3630; contract version 0.17.1-draft at :4).
- Admin page: web/src/app/(app)/admin/feedback/page.tsx:6-11 -> AdminFeedback.tsx (state filter :24-27). List endpoint FeedbackModule.cs:165 under AdminPolicy (:102 RequireRole Admin); it filters by state and limit only, NOT by category (FeedbackEndpoints.cs:208-216).
- Delivery: the dispatcher picks only state `pending` (FeedbackDispatcher.cs:53, claim :69) and does nothing when the sink is off (:48). Route off = DisabledFeedbackSink (IFeedbackSink.cs:114,121). Routes off/automation/rest; the shipped default is off (FeedbackModule.cs:28). States: pending, sent, failed, withdrawn (FeedbackDbContext.cs:63-76; CHECK :129).
- UAT route: MEASURED the settings-name list shows `Feedback__Route` present on 2026-10-24 (slotflags-api.txt:19; the file shows names and a slot flag, not values, so "unset" is NOT what it proves). MEASURED better: the admin list read on 2026-11-03 shows all 3 items route `off`, state `pending`, no Jira key (feedback-list.json). So today nothing reaches Jira from UAT.
- Erasure: FeedbackPersonalData.cs:64-70 sets ErasedAt, removes comment/page/files, turns a `pending` item into `withdrawn` (:69; only `pending` is converted), keeps the row; CHECK ck_feedback_erasure (DbContext) forbids a comment on an erased row. Audit rows are append-only (the context refuses change or delete).
- Submitter data: the row holds user id and role, not a name (FeedbackEndpoints.cs:112-119); the dialog says Jira gets "your role, not your name or e-mail" (FeedbackButton.tsx:80). So "the ones with his name" cannot mean a stored name.
- After send the person is told (feedbackApi.ts:75-88) "queued to go to Datasec's Jira board" (route on) or "Saved, not yet sent" (route off).
- Roles that exist: Admin, Consultant, Partner, Demo (Caller.cs:12-15,17). "Customer" is a data record, not a sign-in role. UAT sign-in: no people, four synthetic levels chosen on the start page, "Partner (review copy)" etc. (uatOpen.ts:21,32-35,128); the cookie id is random per browser. Entra sign-in is the other mode; the records show the product owner as a guest in the dev tenant (CLARIFICATIONS.md:28). Who at HP has any account: NOT in the records (greps for HP-account wording: 0 hits, control "entra" 4 hits fired) = UNKNOWN.

## Smallest shape that does what he asked
1. New category id `review`, label `Run idea / feedback past Steve`, FIRST in CATEGORIES. A hint line is a NEW WORD (needs his OK); none by default.
2. New delivery state `held`. A `review` item is saved as `held`, so the dispatcher (which reads `pending` only, :53/:69) never touches it. Safe by default.
3. Review page (new route + component) listing only `review` items, with Approve and Delete per item; needs a category filter on the list or a new list operation.
4. Approve: `held` -> `pending` (audit `feedback.review-approved`, actor id). It then takes the normal path, so it reaches Jira only where a route is on. Route off (UAT today): approved = saved, not sent.
5. Delete: two choices. D1 ERASE (reuse the erase code: text, page, files removed; row, id and audit line stay; state `withdrawn`). Cheapest; the text is gone for good. D2 REJECT AND KEEP (new state `rejected`, text kept, never sent, shown to Admin): needs one more CHECK edit; keeps the evidence. A true row delete is not offered: it would leave an audit line pointing at nothing.
6. Submitter sees new words (his to approve): e.g. "Saved. This goes to Steve first. It reaches Datasec only if he approves it." The existing "queued to go to Jira" text would be false for this category.
7. Audit: approve and delete each write an append-only row (id, category, actor id; never the comment), as submit does (FeedbackEndpoints.cs:134).

## Who can open the page (the real fork)
- R1 any Admin (existing policy, no new role). Cost: least. Steve himself cannot use it; Admin also carries personal-data export/erase and demo reset (Caller.cs:31 comment).
- R2 a new `Reviewer` role added to Caller.cs:17 + policy + role mapping. In Entra: one account for Steve with that role (does not exist today). In the UAT level picker: a fifth level would be open to EVERY UAT visitor, since there are no named people there.
- R3 a named list of user ids in config. Needs Entra sign-in; impossible in UAT open mode (random id).
Fact: the UAT review site cannot identify Steve at all today.

## Cost (counted from the sites above, not a measured diff)
- Category + held + page + approve + D1, Admin-only (R1): API 5 source files (Endpoints, Module, DbContext, PersonalData, one new endpoints file), 6 migration files (Sqlite + SqlServer: migration, designer, snapshot each), openapi.yaml (enum x3, 2 operations, version bump), generated schema.gen.ts, web 4 (FeedbackButton, feedbackApi, new page, new component) = about 17 files, plus tests (API tests must pass on SQL Server as CI does; web unit; e2e). PersonalData :69 must also turn `held` into `withdrawn`, else an erased held item stays held.
- R2/R3 add Caller.cs, the role mapping, sign-in config and an HP sign-in: about 3 more files and an account HP does not have.
- D2 adds one state and a CHECK edit, a migration line; new words for the page, the buttons, the empty state and the submitter message.
- UNKNOWN: BFF allow-list for the new routes (web/src/server, not read); nav entry for the page; whether `held` needs a filter value in AdminFeedback (:24-27); effort in hours (not measured).

## Plain facts about HP gating Datasec's Jira
This puts an HP person between a submission and Datasec's Jira for one category. A Datasec consultant who picks it could have the item deleted by the reviewer; the other four categories are untouched, and anyone can simply choose another category. Delete (D1) cannot be undone. Jira is Datasec's tool, not HP's. Datasec decides whether the route is ever switched on (K1 card not ruled, README:38).

Phase line: "This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM). Next-phase items are stored and architected only (notes, designs, inputs from HP), never built, and never shown to HP as done."
Note: this is a feature inside the Playbook, not an HP-tool integration.

## Not sourced
Steve's sign-in method; any HP account list; hosted value of Feedback__Route (only the 3 listed items' route); BFF allow-list; hours.
