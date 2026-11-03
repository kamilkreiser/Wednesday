STARTABLE: NO (until the product owner approves the word pack below and Tuesday fills the WORD-* slots; after that: YES, no other blocker found)

# B1206 drafter report: held "Run idea / feedback past <reviewer>" category and Admin review page (HPSM-POC)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-03_B1206_SEAT-H110_hpsmpoc-steve-feedback-review.md` (96 lines, ASCII, 17 stamp slots + the READ-WHOLE line = 18 lines matching `_{4}`).
Drafted between 2026-11-03 11:19:31 and 11:24:33 AEDT (`date`). Ruling used: the product owner's 2026-11-03 11:18:08 ruling, card `hpsmpoc-steve-review-page-1103`, option a "Admin opens the page for now" (card ids appear only here, not in the kit).

## BLUF
- Smallest shape that does what option a says: category `review` saved as new state `held`; the dispatcher already selects `pending` only, so nothing else in delivery changes; Admin-only page lists `?state=held` (existing filter, no new list op); Approve = held -> pending; Delete = per-item erase.
- **The existing erase is per USER, not per item** (`FeedbackPersonalData.cs:54`). "Reuses the existing erase path" therefore means extracting its row update (`:64-71`) and file removal (`:81`) into a helper both entries call. The ruling's "roughly 17 files" holds (count below, now ~19-20 with the merged contract json and the second openapi copy).
- Model row **C4** (Opus 5.5), not C2: Delete is a data-destroying path (`model-routing.md:94`; C2 `:92` excludes it). Gate after: tier 1 (G1 `:108`).
- Not startable until words are approved (a customer-visible label, a new status, a submitter message, buttons).

## Facts re-measured (instrument, control)
F1. Main = `f464376b1f7b62e4a5bf0c73af6c14a8c29993ea` at 11:19:31 (`git ls-remote` over the URL; HEAD and refs/heads/main equal). Control: the same call listed `b02/engine` and `b02/infra`, so it reads refs.
F2. Dispatcher selects `Pending` only: `FeedbackDispatcher.cs:53, :69, :133`; sink-off return `:48`; hosted service only if route != off `FeedbackModule.cs:95`. Instrument: `/usr/bin/grep -n` over the raw file fetched by `gh api -X GET ... Accept: raw`; control: the same grep printed the 3 `Pending` lines plus `:142` (reschedule to Pending), so the pattern fires. A fourth write, `:236` (`!= Sent`), marks `sent` and cannot touch a `held` item that was never claimed.
F3. State list `FeedbackDbContext.cs:63-76`; CHECKs `:128` (category), `:129` (state), `:131-132` (erasure). Submit writes `Pending` `FeedbackEndpoints.cs:123`; list filters by `state` `:208-209,:216` and rejects states outside `All` (existing test uses `?state=lost`, `FeedbackApiTests.cs:203`). So adding `held` to `All` is the whole list change. D-1.
F4. Erase `:54`, `:64-71`, `:69-70` converts only `pending`; files `:81`; export `:30-52` has no state filter (so held rows are exported already; the kit still pins it with a test).
F5. The two `openapi.yaml` files are the same blob `ba2af3e6...` (`git/trees` GET, both paths; control: the tree walk also returned `schema.gen.ts` 56ac2a42 and merged json 07cf725f). Generated chain: yaml -> `openapi.merged.json` -> `schema.gen.ts`, pinned by `contract-drift.test.ts`.
F6. Admin index test `page.test.tsx:75-82` counts links by name = 1 and bans buttons on the index; a second, differently named link keeps both true. (The design input said "UNKNOWN: nav entry"; resolved: link from the admin index card, `admin/page.tsx:26`.)
F7. Overlap with the focus-ring branch `b1097/hpsmpoc-home-words-focus-ring` (head f39ac80e, 4 commits ahead; `compare main...b1097` GET): its 9 files are shell/Sidebar, globals.css, shell-sidebar.spec, AppShell.sidebar.test, PartnerDashboard x4, home-next-actions. Count of those matching my paths (`feedback|openapi|schema.gen|admin|Migrations`) = 0; control: `Sidebar` pattern matched 3. **Overlap: none.**
F8. Overlap with B1204 (rail lane, kit read whole): it owns `web/src/components/shell/**`, `security/{SidebarMenu,CustomerNav,WorkspaceSwitch}`, `globals.css`, `web/e2e/shell*.ts`; it lists "any page under `web/src/app/(app)/`" as NOT its own. My kit adds no rail entry and avoids all of those; B1206 edits `(app)/admin/**`, which B1204 leaves alone. From both sides: disjoint. B1204 waits on the focus-ring landing; B1206 does not need it (cut from main).
F9. Open PRs on HPSM-POC: 0 (`pulls?state=open`, `--jq length`; control: a `matching-refs/heads/b1097` GET returned 1). `heads/b1206` on origin: 0 (control b1097: 1). `.tools/b1206` absent (control `.tools/b1190` present).
F10. Panes: `tmux list-panes -a -F '#{@cockpit_name}'` shows `Datasec/HPSM-POC-G313` once (`grep -c -x` = 1); no H110. Not a stop, per the brief.
F11. Ports (`lsof -nP -iTCP:<block> -sTCP:LISTEN`, lines): 9660-9669 = 5 (G313, control fired); 9670-9679 = 0 but claimed by the B1204 kit (word scan hit 1); **9680-9689 = 0 listeners and 0 hits** in the non-`.pre-` SEAT kits of 11-02 and 11-03 (control: `9670-9679` hit 1 in B1204). 9700-9709 had 1 kit hit, so I avoided it. Chosen: **9680-9689**.
F12. Model id `claude-opus-5-5` at `models_latest.json:17`; routing rows C4 `:94`, C2 `:92`, G1 `:108`; `brief_seat.sh:24` defaults to opus (level written anyway).
F13. Landing: head-pinned squash, Tuesday lands through CodeQL (`CLARIFICATIONS.md` of the analysis repo, line 3617, "The landing form is a head-pinned squash"). Word-approval practice: C-39 (`:418`), C-40 (`:424`), C-99 (`:1107`), C-120 (`:1763`): the owner approves wording by a card, the wording is recorded as a clarification, then the seat is told the exact text.
F14. Existing reusable strings/patterns: confirm pattern `FollowUpPanel.tsx:143-150` ("Withdraw this link? It stops working at once." / danger button / "Keep it"); "Saved, not yet sent" (`feedbackApi.ts:84`); "Only the Admin role can see the feedback received." (`AdminFeedback.tsx:81`); "Download", "Filter by state", "No feedback yet." (`:89-90`). The web has no existing "Approve" button on a feedback page (code search "Approve" hits report/narrative files only).
F15. File count (counted from sites, not a measured diff): API src 5-6 (Endpoints, Module, DbContext, PersonalData, new review endpoints file, optional dispatcher note), migrations 6, openapi 2 + merged json 1 + schema.gen 1, web 5 (FeedbackButton, feedbackApi, AdminFeedback, new page, new component, admin index = 6), tests extra. About 20 non-test files; the ruling said roughly 17 "by a count": the two extra are the second openapi copy and the merged json.

## D-decisions (made in the kit; Tuesday may overrule)
D-1. List: reuse `?state=held` (add to `All` and the openapi enums). Smaller than a category filter (no new parameter, no contract operation change, no extra test matrix); `held` only arises from `review`, and approved items leave the page by construction.
D-2. Nav: no rail entry; a second link in the existing admin index "Feedback received" card (keeps B1204's files untouched; keeps `page.test.tsx:75-82` true).
D-3. Delete = erase the text and files, keep the row and the id, state `withdrawn`, audit `feedback.review-deleted` (the product owner chose "removes the text for good and keeps a log line"; no new `rejected` state).
D-4. Approve/Delete are two new contract operations (`approveFeedback`, `deleteFeedback`) under the existing Admin policy; no new role (option a).
D-5. Model: Opus 5.5 row C4; tier-1 gate.
D-6. Migration `Down`: convention has one; the kit makes the seat choose and test what it does to rows holding `review`/`held` and report it.
D-7. A6 SQL Server: the seat may not run docker; it must say NOT TESTED on SQL Server rather than claim; Tuesday's gate/CI runs it (`ci.yml` job "api on SQL Server"). Predicate: every CI step exit 0, CodeQL clean.
D-8. The kit quotes the product owner's feedback item verbatim (which names the reviewer) in its Authority line, because the label must be exact; the kit tells the seat the name stays out of commit, comments and STATUS except the stamped label constant.

## WORD PACK (every new customer-visible word; proposals are minimal; the product owner approves, then Tuesday stamps)
Existing strings reused are marked (R).
1. WORD-CATEGORY: `Run idea / feedback past Steve` (the product owner's own, verbatim; first in the list; no hint). Note: the label names a person; the dialog is seen by every role.
2. WORD-HINT: none (proposed). Optional alternative, only if he wants one: "It goes to Steve first".
3. WORD-SUBMITTER (after a held submit): title "Saved, held for review"; body "Thank you. Your feedback is saved in the Playbook and held for review. It goes on to Datasec's Jira board only if it is approved." Replaces the "queued to go to Jira" text that would be false for this category.
4. WORD-HELD-STATE: Admin list state word "Held for review"; filter option "Held for review" (in `STATE_FILTER` and `deliveryWords`).
5. WORD-PAGE: page title and tab title "Feedback for review"; lead "Items sent with Run idea / feedback past Steve wait here. Approve sends one on to Datasec's Jira board. Delete removes its text for good."; admin index link "See the feedback waiting for review"; loading label "Loading the feedback for review..." (pattern of `AdminFeedback.tsx:87`). No column headings (cards as the existing list); item lines reuse "From the <role> role on <page>" (R).
6. WORD-ACTIONS: buttons "Approve" and "Delete"; confirm sentence "Delete this feedback? Its text is removed for good." with danger "Delete" and "Keep it" (R, `FollowUpPanel.tsx:147`).
7. WORD-RESULTS: after Approve, delivery on: "Approved. It will go to Datasec's Jira board in the next few minutes."; delivery off (UAT): "Approved. Saved, not yet sent." (R: "Saved, not yet sent"); after Delete: "Deleted. The text is gone for good." (Delete busy label "Deleting...", Approve busy label "Approving...", the pattern of "Withdrawing...").
8. WORD-EMPTY-ERR: empty title "Nothing is waiting for review."; 403 "Only the Admin role can review feedback." (variant of R); 409 "This item is no longer waiting for review."; service error "The service answered with an error (<n>)." (R pattern, `AdminFeedback.tsx:82`); API invalid-category message "Choose review, bug, idea, content or question."
Not customer words (log vocabulary, not for approval): audit actions `feedback.review-approved`, `feedback.review-deleted`; ids `review`, `held`; operation ids.

## Q-questions for Tuesday (each with a default)
Q-1. Do the held and review words (pack items 3-8) go to the product owner as one card, or only the category label (his own) is treated as approved and the rest proposed? Default: one card, option a "Approve all as proposed"; the label needs no approval but is listed.
Q-2. Who the page's users really are on UAT: the sign-in picker offers an Admin level (the design input read four synthetic levels, `uatOpen.ts`); should the launch note tell the seat to confirm Admin is on the picker? Default: the seat's e2e uses the Admin level exactly as `playbook-feedback-b241.spec.ts` does; if absent it STOPs.
Q-3. Should the kit wait for the focus-ring landing as B1204 does? Default: no (disjoint paths, F7); launch order is free.
Q-4. Hard stop: kit default target 180 / hard stop 300 minutes (larger than the shell kit: migration x2 providers plus contract regeneration). Default stands unless the usage gate says otherwise (P2/P3 are Tuesday's call).

## UNMEASURED
Hours of effort; whether SQLite's added-CHECK migration rebuilds the table cleanly (the seat prints EF's output); whether `ContractTests.cs` (api) pins the operation list/count (not read; the seat finds out red-first); the BFF allow-list for the two new routes (`web/src/server`, not read; the mock answers 404 in demo mode and the page shows the existing offline message); whether the UAT picker has an Admin level (Q-2); hosted `Feedback__Route` value.

## Outside the fences (disclosure)
None crossed. Reads: tracked briefs/specs under TUESDAY, the local analysis-repo `CLARIFICATIONS.md` first (stale, 192 lines, no C-39; discarded) then the origin copy via `gh api -X GET`; `gh api -X GET` search/code (GET) for strings. No Jira, no hosted HTTP, no `decision_queue.sh`, no briefs_staged/scoreboard/ledger/WED trees. Scratch files in the session scratchpad only. One hook refusal (a variable named `cd_unused`, then a leading `==` echo) cost two retries; nothing ran.
