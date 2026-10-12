From Friday (laptop seat), Datasec / MPS Commercial Calculator. No mail key in this project: the STATUS file is the wrap.
# BRIEF B65 · SEAT-B: FIX ROUND for gate B63 (X-1 Major, X-2 Blocker-class latent, plus the X-4 words) on B60's `e0bbc6f`

**Fired: 2026-10-13 06:35 AEDT.** Drafted by Friday's drafter 2026-10-13 06:2x–06:4x AEDT, using read-only git on the project (`ls-remote`, `log`, `show`, `diff`, `rev-parse`, `rev-list`, `merge-base`, `grep`, `ls-tree`). Write verbs ran only in a `clone --shared` in the drafter's own scratch dir.
**Pane:** `Datasec/MPS-B`. **Your commission is THIS file at `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/2026-10-13_B65_SEAT-B_gate-b63-feedback-fix-round.md` (Friday's tree, read-only to you). Step 0: copy it unchanged into your `1_Project_Definition/Briefs/` as the project's record.** Show the sha256 of both copies; they must be equal.
(Launcher check. `Launch_Claude.command:107` takes the seat letter from a pane name that matches `*MPS*-?`. `:111` makes the commission *"the NEWEST brief in 1_Project_Definition/Briefs/ whose file name contains _SEAT-${SEAT}_"*. At drafting, `ls -t Briefs | grep _SEAT-B_` lists `2026-10-13_B60_SEAT-B_b47-feedback-onto-main.md` first. That seat is finished: `B60_STATUS.md:174` is `READY FOR GATE: b60/feedback-pill-on-d711b42 e0bbc6f8…`. Your Step 0 copy makes this file the newest `_SEAT-B_` file, so it supersedes B60.)
**Seat:** Seat B, a Claude build seat. One branch, red-first. **QA tier 1** throughout. X-2 is a confidentiality hole: a second free-text channel into Jira.
**Round:** FIX ROUND. This is **round 2 of 2** under Kam's two-NO-GO cap. B63 was round 1 (`B63_STATUS.md:2`, `:9`). The next gate is a **deltas gate**. **If it says NO GO, Friday ships what is closed and tickets the rest. There is no round 3.** So close each row completely, or list it as NOT DONE. Never leave a row half-done.
**Report:** `1_Project_Definition/Briefs/2026-10-13_B65_STATUS.md`. Its **last line** is exactly one of these:
- `READY FOR GATE: b60/feedback-pill-on-d711b42 <sha>`, where `<sha>` is the full 40-hex SHA read back by `git ls-remote origin refs/heads/b60/feedback-pill-on-d711b42` in the same action as the push;
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.

## AUTHORITY
- **Gate B63** (`Briefs/2026-10-13_B63_STATUS.md`, Seat G, round 1, 290 lines; the last line, `:290`, is `READY FOR REVIEW: b60/feedback-pill-on-d711b42 e0bbc6f8… NO GO`). Its verdict:
  - `:6`: *"B60 e0bbc6f: **NO GO**: 2 findings at Major or above (X-1 Major, Y; X-2 Blocker-class, latent, J)."*
  - `:7`: (J) NO GO; (Y) NO GO. Every other area is GO or GO WITH NOTES: (A) (S) (T) (H) (C) (R) (K) (M) GO; (L) (P) (U) (W) GO WITH NOTES.
  - `:8`: FAST-FORWARD is void because main moved to `f4616886`. `:9`: overall NO GO.
  - Closure (`:12-26`): Item 5 (form) is **NOT CLOSED** (X-1) and Item 6 (tickets) is **NOT CLOSED** (X-2). Items 1, 3 and 7 are CLOSED. Items 2, 4 and 8 are CLOSED-WITH-NOTES. **Do not rebuild the closed rows. Keep them green.**
- **The gate's round-2 scope, proposed** (`:253`): *"X-1 (wrapper focusable/named), X-2 (route-shaped page check before Jira), X-4 (words card). X-7 stays Kam's (`[B47-D6]`, `[B60-1]`)."* Friday accepts this scope. The fix shape for X-2 is Friday's, set out below. It is not the gate's store-time shape, and row X-2 says why.
- **The spec stands:** `Briefs/2026-10-12_B47_SEAT-B_feedback-pill.md` (118 lines). The confidentiality rule is `:84`: price-book data never goes into Jira (spec §40, project `CLAUDE.md:54`), and *"a free-text message may contain prices"*. The item shape is `:73`. The form and the All feedback table are `:81`.
- **Kam, carried:** *"add a feedback button and function to the MPS calculator (orange pill at bottom right corner). Make sure you store all feedback captured and ideally create tickets automatically"* (B47 brief `:12`). **"Store all feedback" is why this round never refuses or blanks a page the user sent** (row X-2).
- These stand unchanged: Jira OFF by default; `IncludeMessage` default false; any signed-in caller may submit and only an Administrator lists or retries; `--feedback-bg #b84a00` on the pill only; the SITE HOLD; Q-09 (synthetic data only).

## PRIOR-WORK CHECK (do this first; report it in STATUS `## PRIOR WORK`)
Re-read each cite at `e0bbc6f` and record whether it is **still open, already closed, or moved**, with `file:line`. If an item is already closed, do not rebuild it; say so.
- **`B63_STATUS.md`:** run `wc -l` on it. The drafter read **290** lines, and the last line is `READY FOR REVIEW … NO GO`. If the verdict, the findings (`:191-201`) or any line quoted here has changed, record each change. **If a new Blocker or Major appears, STOP: NEEDS FRIDAY.**
- Code at `e0bbc6f`, read by the drafter with `git show`:
  - `src/MpsCalc.Api/Feedback/FeedbackEndpoints.cs:254-296` `ReducePage`. `:264-266` keeps a `#/…` route through `HashRoute` (`:289-293`), which cuts at a second `#` and at `?` only. `:282-285` applies the 2000-character cap. `:142` calls it on submit, and `:153` stores the result in the item.
  - `src/MpsCalc.Api/Feedback/FeedbackTickets.cs:395-410` `IssueJson`. `:400` is `$"Page: {item.PagePath ?? "not recorded"}"`, and `:406-410` adds the message only when `IncludeMessage` is true.
  - `web/src/feedback/FeedbackAdminPanel.tsx:48` is `<section className="feedback-admin" aria-label="All feedback list">`. `:61` is `<div className="feedback-table-wrap">`, with no `tabIndex`, no role and no name. `:62-104` is the table.
  - `web/src/feedback/feedback.css:51` is `.feedback-table-wrap { overflow-x: auto; max-width: 100%; }`. `:25` is the pill's focus ring `outline: 3px solid var(--accent); outline-offset: 2px`, the pattern to reuse.
  - `web/src/app/router.ts:44-56` `parseRoute`. **The app's whole route set is** `#/` (Home), `#/quotes` (list), `#/inventory`, `#/quotes/<id>` (quote) and `#/quotes/<id>/proposal` (`:49-55`, and `href` at `:63-74`). Server quote ids are `q_` + 32 lower-case hex (`QuoteStore.cs:115` `NewId`; `QuoteFileStore.cs:440-441` `IsId`).
  - Tests: `FeedbackApiTests.cs:270-292` (`PagePaths` / `The_page_is_reduced_to_a_path_on_the_server`, 9 rows), `:294-305`, `:307-314`. `FeedbackTicketTests.cs:103-136` (`Enabled_a_201_…_carries_no_message_text`; **`:132` asserts the description contains `"#/quotes/q_syn"`**), `:138-…` (`IncludeMessage_true_sends_the_message_text`), `:351-375` (logs; `PlantedPage` `:80`). `FeedbackAdminPanel.test.tsx:19`, `:46`, `:57`.
  - `docs/API.md:548-550` (at `e0bbc6f`): the Jira description *"category, page, time, display name, id and …"*.
- **The gate's instruments, read-only. Copy them; never run them in place:** `.tools/qa-B63/e2e/a11y63.spec.ts` (axe at 4 sizes), `.tools/qa-B63/tools/fakejira63.py`, `probe63_dev.py`, `qlib63.py`, `words63.py`, `selfscan63.py`. axe-core **4.10.2** was installed by the gate under `.tools/qa-B63/axe`. Install your own pinned copy (`npm install --prefix '<P>/.tools/qa-B65/axe' axe-core@4.10.2`). Never edit `web/package.json` or `package-lock.json`.
- Search for prior work: `git log --all --oneline -i --grep='X-1\|X-2\|B63\|B65\|feedback-table-wrap\|JiraPage'`. List the hits.

## Base and branch
- **Base: B60 head = `e0bbc6f80829aa4ed4bba954861a73dff8303f64`** (tree `fe04a7f0b98fc0e2c28bfaa77635a8d5035ee389`, `B63_STATUS.md:46`). B60 is **not merged** and has no PR.
- **What the drafter measured (read verbs only), 06:29:03 AEDT 2026-10-13, `git ls-remote origin` rc 0:**
  - `refs/heads/main` = **`f4616886ef232d7c39b7faa10bde4cb33a6f2c8b`**; `refs/heads/b60/feedback-pill-on-d711b42` = `e0bbc6f8…`; `refs/heads/b47/feedback-pill` = `81b0135d13a20b770df0669857d3043cf03653ec`; `refs/heads/b65*` = no line.
  - `log d711b42c..f4616886`: `65f82f1` *"B54 + B58: catalogue overlay store residue and its fix round (gates B57, B59) (#30)"* and `f461688` *"B62: version the leak scanner as tools/leakscan/ with a test (Friday ruling M3) (#31)"*.
  - `rev-list --left-right --count f4616886...e0bbc6f8` = **`2 6`**; `merge-base` = `d711b42c…`.
  - **Overlap by compare:** `diff --name-only d711b42c f4616886` gives **8** files: `Inventory/CatalogueOverlayStore.cs`, `Inventory/InventoryEndpoints.cs`, 3 `Overlay*` tests and 3 `tools/leakscan/*`. `diff --name-only d711b42c e0bbc6f8` gives **31**. `comm -12` = **0 shared files** (the same as `B63:8`).
  - **Semantic link checked:** `FeedbackEndpoints.cs:38` reads `CatalogueOverlayStore.Directory`. That property exists at both `d711b42c:…CatalogueOverlayStore.cs:101` and `f4616886:…:105` with the same body.
  - `merge-tree --write-tree f4616886 e0bbc6f8` (run in the drafter's scratch clone) gives tree **`d9c702b5a2c743734f66cfc6481d3baa9b8bba18`**, rc 0.
- **Friday's decision: continue on `b60/feedback-pill-on-d711b42`. Commit on it. Do NOT rebase it and do NOT merge main into it.**
  - Why: main moved under the branch in **0 shared files**, and the merge is clean. The deltas gate diffs `e0bbc6f...<your head>` exactly. A rebase would rewrite B60's six commits and need a force push, which is forbidden.
  - **B63 asked for the combined tree to be measured** (`:254`, `:274` UNMEASURED). You measure it in a clone (see the end of this section). Nothing lands on the branch from main.
- **Worktree:** `.tools/wt-B60` holds the branch. At drafting it was at `e0bbc6f8`, with `status --porcelain` showing 0 lines. B60 is finished, so **Friday hands `wt-B60` to you**. Take base measurements in a new `.tools/wt-B65-base`, created with `worktree add --detach … e0bbc6f8` (`chmod 700`). Tools and logs go in `.tools/qa-B65/` (0700).
- **Step 0 (before any edit):** run `git -C 2_Project_Files fetch origin`, then `git ls-remote origin refs/heads/main refs/heads/b60/feedback-pill-on-d711b42 'refs/heads/b65*'`. Record `M0` = main.
  - If `b60/…` is not `e0bbc6f8…`, `wt-B60` is not clean at `e0bbc6f8`, or a `b65*` ref exists: **STOP: NEEDS FRIDAY**.
  - `M0` must be `f4616886…` or a descendant of it. If it is a descendant, run `git diff --name-only f4616886 M0` and intersect it with your write set (below) and with B60's 31 files. **Any intersection: STOP: NEEDS FRIDAY.**
  - `git merge-tree --write-tree M0 e0bbc6f8` must give rc 0. Record the tree. It writes objects only, so it is allowed here.
- **At the end (after the last commit, before the push):** fetch again and record `M1`.
  - `git merge-tree --write-tree M1 HEAD` must give rc 0, with no conflict lines. Record the tree.
  - **Combined-tree suite (B63's UNMEASURED):** in `git clone --shared … .tools/qa-B65/clone` (push URL `NO-PUSH`; show that a dry push fails), commit that merge tree detached, with local identity `qa-b65@invalid`, never pushed. Then run Release build, the full `dotnet test`, Vitest and `b47-feedback.spec.ts` (stub) on it. Report it as a row in Test Evidence.
  - If `M1 ≠ M0`, `git diff --name-only M0 M1` must not intersect your write set. Any conflict or intersection: **STOP: NEEDS FRIDAY.** Never resolve it by rebasing.
- **Push your branch only, and read it back.** Friday opens the PR and lands it once CodeQL and the checks are green. **No PR from you. No force push. Never push to main.**

## Ports
- **6630–6639**, the lane's range (B47 brief `:68`, B60 STATUS `:159-165`). B60's processes were stopped (`:165`: `lsof` rc 1 at 04:15:52). Use API 6630, web 6633 (head) and 6634 (base), and fake Jira 6636.
- **Drafter's check at 06:31 AEDT:** `lsof -nP -iTCP:6630-6639 -sTCP:LISTEN` printed nothing (rc 1). `uptime` load was 9.08 / 9.14 / 9.83.
- **Run `lsof` again before every bind.** On any listener in your range, **STOP: NEEDS FRIDAY**; never move ranges. Never bind 6640–6649 (B63's) or any other range named in an earlier brief. Pass ports through env (`MPSCALC_WEB_PORT`, `MPSCALC_API_ORIGIN`, `MPSCALC_E2E_BASE_URL`); never edit a shared config default.

## Write set (PATHS; nothing outside it)
- X-2: `src/MpsCalc.Api/Feedback/FeedbackTickets.cs` and `tests/MpsCalc.Api.Tests/FeedbackTicketTests.cs`.
- X-1: `web/src/feedback/FeedbackAdminPanel.tsx`, `web/src/feedback/feedback.css`, `web/src/feedback/FeedbackAdminPanel.test.tsx`, and `web/src/feedback/words.ts` (only if you put the new label there). `web/e2e/b47-feedback.spec.ts` may get one added Administrator-at-390 keyboard test.
- Docs: `docs/API.md`, **only inside B47's `## Feedback (brief B47)` section** (the description sentence at `:548-550`).
- **9 paths at most.** Each is one of B60's 31 files. Their intersection with main's 8 moved files is **0** (measured above).
- **FROZEN (the diff must be empty):**
  - `FeedbackEndpoints.cs` (including `ReducePage`; row X-2 explains why), `FeedbackStore.cs`, `FeedbackDtos.cs` and `FeedbackLog.cs`;
  - `docs/api/openapi.json` (the stored `pagePath` contract does not change), `web/src/api/generated/**`, `page.ts`, `FeedbackDialog.tsx`, `FeedbackPill.tsx`, `stub.ts`, `api.ts` and `csv.ts`;
  - every file outside B60's 31, in particular `src/MpsCalc.Api/{Quotes,Inventory,Sources,Infrastructure,Contracts}/**`, `Program.cs`, `appsettings*.json`, `web/src/{app,screens,proposal,api,auth}/**`, `styles.css`, `package*.json`, `*.csproj`, `infra/**`, `scripts/**`, `tools/**` and `.github/**`;
  - every test of main's (beyond the 5 lines B60 already carries).
- **If a row needs a frozen file**, do not touch it. Mark the arm **NOT DONE: BLOCKED-BY-FILES (<file>)** and go on.

## Tier 1 (all rows)
- **The gate's Jira FAIL condition, verbatim** (B63 brief `:42`, applied at B63 STATUS `:112`): *"the message text, or a planted price-shaped value, in any Jira request body when `IncludeMessage` is not `true`"*. **For this round, the page line carries no client text even when `IncludeMessage` is `true`** (row X-2).
- **The a11y FAIL condition, verbatim** (B63 STATUS `:147`): *"any `serious`/`critical` axe violation on the pill or the dialog (Major); `moderate`/`minor` (Minor)."*
- **Every closed row stays closed.** That covers authZ 66/66, OFF by default (0 requests), store-then-confirm, restart byte-equal, value-free logs, hosted refusals 16/16 and the four held store keys unchanged. Nothing is refused that was accepted at `e0bbc6f`; **every page a user sends is still stored as it is stored today.**
- No token-shaped value other than the literal `test-token-not-real`. No price, total or applied percent moves on any fixture.

## ROWS (in this order; red test first for each; one commit per row)

### Row X-2 · Blocker class (latent) · free text after `#/` in the page path reaches the Jira description
- **Finding, verbatim (B63 `:193`):** *"X-2 · Blocker by the brief's Tier-1 class text (latent: needs Jira enabled) · INTRODUCED · `src/MpsCalc.Api/Feedback/FeedbackEndpoints.cs:254-296` (`ReducePage`) → `FeedbackTickets.cs:400`. FOUND: the server keeps any client text after `#/` up to `?` (≤ 2000 characters, spaces allowed). The text is stored and written into the Jira description line `Page: …` regardless of `IncludeMessage`."* Measured: the planted value is in the create body **4/4** (two forms × `IncludeMessage` unset/false), and **0/4** after `?` (`:124-127`). It is *"not reachable as shipped or as ruled: Jira is OFF by default (proven), and Kam's MPS-9 keeps hosted Jira off"*, and it is a **"Pre-enable condition for any Jira switch-on"**.
- **The options, from the code:**
  - **(A) Store-time allow-list in `ReducePage`** (the gate's HOW). Accept only the known routes, and refuse anything else (400) or store it as null.
    - Refusing breaks *"store all feedback"*: a user's feedback is lost because of the page they were on. It also turns 3 of the 9 `PagePaths` rows red (`/`, `/inventory`, `/some/path`; `FeedbackApiTests.cs:275-279`).
    - Storing null loses the exact page that Administrators see in All feedback (`FeedbackAdminPanel.tsx:79`) and the CSV (`csv.ts:18`).
    - **It also does not close the channel for items already stored.** Item files are never rewritten (B47 brief `:72`), and at start every item without `created` is re-queued (`:83`). So an item stored before the fix, holding free text, would still reach Jira the first time Jira is enabled.
  - **(B) Jira-time reduction in `FeedbackTickets.IssueJson`** (`:400`). The `Page:` line carries only a **route pattern from a closed list** that mirrors `router.ts:49-55`, and never the stored text.
    - The store, the contract, the Administrator view and the CSV are unchanged.
    - It covers every item whenever it was stored, because the reduction runs when the issue is built.
    - It changes one line plus one helper, inside one file that is already in the write set.
  - **(C) Drop the `Page:` line from Jira.** This closes the channel, but the ticket loses which screen the feedback is about, and the reader still has to open the calculator to triage.
  - **(D) Send the raw page only when `IncludeMessage` is true.** That widens Kam's `IncludeMessage` ruling (which is about the message) to a second field. It needs a ruling, and it still sends free text when the switch is on.
- **Friday's pick: (B), with the pattern sent whatever `IncludeMessage` says.** It keeps the feature (Jira says which screen; the calculator keeps the exact page, the same as *"Full text: in the calculator"*). It closes the channel for stored items too. It refuses nothing. The confidentiality rule (`B47:84`) is applied by treating the page as client text: client text never reaches Jira except the message under `IncludeMessage`. **The quote id is not sent either.** It is a client-supplied segment, and even the server's hex shape (`q_` + 32 hex) can carry a digit run. The Jira reader opens the item in All feedback for the exact page.
- **The mapping (exact, ordinal, on the stored value):**

  | Stored `pagePath` | Jira `Page:` text |
  |---|---|
  | null | `not recorded` (unchanged, `:400`) |
  | `#/` or `/` | `#/` |
  | `#/quotes` | `#/quotes` |
  | `#/inventory` | `#/inventory` |
  | `#/quotes/<one segment, no />` | `#/quotes/<id>` |
  | `#/quotes/<one segment, no />/proposal` | `#/quotes/<id>/proposal` |
  | anything else | `other (in the calculator)` |

  These are words Kam has not seen. Each new string goes in the NEW WORDS table. If you choose different words, say why. **Never** build the output from any part of the stored string. The function returns one of the 7 constants and nothing else, and a test asserts that.
- **Red-first cells:**
  - (1) **The gate's channel, in-process** (`FeedbackTicketTests`, the fake handler, `test-token-not-real`). Use the pages `#/quotes/PLANTED-B65-PRICE-9876.54`, `#/quotes/PLANTED-B65-PRICE 9876.54`, `#/PLANTED-B65 9876.54` and `/x/9876.54/y`, each with `IncludeMessage` unset, `false` and `true` (**12 arms**). Count `9876.54` in every create body: **0 in 12/12. RED at `e0bbc6f`** on the hash forms in at least the 4 unset/false arms the gate measured. Say exactly how many of the 12 are red there.
    - **Value control:** the planted value **is** in each stored item file (12/12).
    - **Message control:** with `true`, the planted message **is** in the body.
  - (2) **Every route maps exactly as the table** (a theory over the 7 rows, plus `#/quotes/q_syn` → `#/quotes/<id>`). The quote rows are **RED at `e0bbc6f`**; the `#/`, `#/quotes` and `#/inventory` rows are green at both (a guard; say so).
  - (3) **Already stored, then enabled** (option B's reason). Write an item through the API with Jira off and a planted page. Then start a new host on the same directory with Jira enabled. The re-queued create body holds **0** planted values. **RED at `e0bbc6f`.**
  - (4) **Closed output set:** for 200 random strings (seeded; print the seed), the `Page:` text is always one of the 7 constants.
  - **Modified pre-existing test (declare it before → after):** `FeedbackTicketTests.cs:132` expects `"#/quotes/q_syn"` in the description. It becomes `"#/quotes/<id>"`, because `q_syn` must no longer appear. Change nothing else in it.
  - **GREEN at head.**
  - **Tampered back RED (each on its own):** (a) `:400` uses `item.PagePath` again; (b) the quote rows pass the segment through; (c) unknown pages map to the stored text. Each must turn ≥ 1 named test RED.
- **The gate's own probe, re-run live** (DevStub head on 6630, your copy of `fakejira63.py` on 6636, your copy of `probe63_dev.py` with its ports changed to yours). Run the B63 `:121-128` table: channel (c) page hyphenated and with a space, × `IncludeMessage` unset, false and true.
  - **Expected: 0 in every cell** (the gate had 1 in each).
  - (a) message: still 0 / 0 / 1.
  - (d) display name: **unchanged at 1** (X-3, by design, NOT THIS ROUND).
  - Hosts contacted: only 127.0.0.1:6636. Report counts only.
- **Docs:** `docs/API.md` `:548-550`. *"a description with the category, page, …"* becomes *"… the page's route pattern only (never the path as sent; e.g. `#/quotes/<id>`), …"*. The text is yours; put it in NEW WORDS.

### Row X-1 · Major · the All feedback table's scroll wrapper is keyboard-unreachable at 390
- **Finding, verbatim (B63 `:192`):** *"X-1 · Major · INTRODUCED · `web/src/feedback/FeedbackAdminPanel.tsx:61` (`feedback.css:51`). FOUND: at 390 the All feedback table sits in `<div class="feedback-table-wrap">` (`overflow-x: auto`) that overflows (scrollWidth 479 > clientWidth 322) with no `tabindex` and no focusable descendant; axe 4.10.2 `scrollable-region-focusable` = serious, 1 node."* 1440 had 0 (no overflow). Chromium 155 reaches it by Tab; *"Safari is not measured and does not do this."*
- **Fix shape. The gate proposes, and Friday accepts; verify before building:** *"make the wrapper a focusable, named region (`tabindex="0"`, `role="region"`, an `aria-label` …, plus a visible focus style using `--accent`)"*.
  - The **name must differ from the section's `"All feedback list"`** (`:48`), or the two landmarks share a name. The drafter's default is **"All feedback table"**, a NEW WORD.
  - Focus style: `.feedback-table-wrap:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; }`, the pill's own pattern at `feedback.css:25`. **0 new colours** (check them with the gate's planted-control method, B63 `:157`).
  - Keep the `tabIndex` on the wrapper even when it does not overflow (at 1440). A conditional tab stop is fragile. One extra stop inside an Administrator-only tab is the accepted cost; say so in STATUS.
- **Red-first cells:**
  - (1) **Vitest** (`FeedbackAdminPanel.test.tsx`): with ≥ 1 row, `getByRole('region', { name: 'All feedback table' })` exists, has `tabIndex` 0 and contains the table. With 0 rows, there is no such region. **RED at `e0bbc6f`.**
  - (2) **The gate's axe run, copied** (`a11y63.spec.ts` → `qa-B65/e2e/a11y65.spec.ts`, your own Playwright config under `qa-B65/`, axe from `qa-B65/axe`). Run it on the stub web, Administrator, ≥ 3 synthetic rows, scoped to `dialog.feedback-dialog`, at **1440 · 1280 · 1024 · 390**, both personas, all 5 states (B63 `:148-153`).
    - **Expected: 0 serious/critical in every cell. 390 Admin All feedback: 1 → 0** (base column measured by you at `e0bbc6f`, head at your fix).
    - Control: an injected unlabelled button gives `button-name` (critical) and fires in 4/4.
    - Also report the `best-practice` tag counts for the dialog (as information; `landmark-unique` must be 0).
  - (3) **Keyboard, Chromium, 390 Admin:** Tab reaches the wrapper (`document.activeElement` is the region). ArrowRight moves `scrollLeft` above 0. The focus outline is computed as `3px solid rgb(21, 101, 192)` (B63's measured `--accent`, `:157`).
    - Add this as one test in `b47-feedback.spec.ts`. It must be **RED at `e0bbc6f`** on the role/name step; if Chromium's own scroller focus makes the Tab step pass at base, say so.
    - **WebKit:** run cell (3) in WebKit **only if** a Playwright WebKit build is already installed on this machine (`npx playwright install --list` or the cache directory). **Never download a browser.** Otherwise it is NOT TESTED, with that reason.
  - **GREEN at head.**
  - **Tampered back RED:** (a) remove `tabIndex`: Vitest and axe both RED; (b) remove `aria-label`: Vitest RED.
- **Re-run the gate's by-hand checks** (B63 `:154`): focus into the dialog, 0 escapes in 16 Tabs, Esc closes and focus returns to the pill (4/4), unlabelled controls 0. These must be unchanged.

### Row X-4 · Minor · INTRODUCED · undeclared words: TAKEN (STATUS only, no code)
- **Finding (B63 `:195`):** user-visible undeclared **1** (`FeedbackEndpoints.cs:284` *"pagePath is longer than {MaxPagePath} characters."*), about **32** operator-visible strings and **3** Jira-visible ones (*"Message:"*, *"not recorded"*, *"none"*). HOW: *"add them to the words card (table below); no code change needed."*
- **Do:** carry every row B63 marks **UNDECLARED** (`:230`, `:238-245`, `:247`) into your NEW WORDS table **verbatim, marked "declared by B65 (from B63 X-4)"**, plus every word this round adds. Run a copy of `words63.py` over `e0bbc6f...HEAD`. Undeclared after this round must be **0**. A planted undeclared string in an unpushed local commit must be flagged (control).

### Row 4 · The rest of B63: TAKEN / NOT THIS ROUND (drafter's call; each quoted by line)
**Moving a NOT THIS ROUND row to TAKEN is STOP: NEEDS FRIDAY.**

| Item (B63 line) | Grade | Call | Reason |
|---|---|---|---|
| **X-7** `[B60-1]` / `[B47-D6]` (`:198`, `:23-24`, `:61-71`) | **Note for Kam** | **NOT THIS ROUND; report only** | **B63's measurement at 1440 Home (Seller):** *"2 of 4 'Continue' covered at the top (filled panel: 4 of 34); both reachable by scroll and by Tab; a pointer click at the centre lands on the pill for 1 of 2"* (`:24`). Also at 1440: `#/quotes` "Open" ×2 (NEW: B60 had left that route UNMEASURED). Then 1280 `#/quotes` "Open" ×1, 1024 Home "Record outcome" ×2, and several at 390. **0 unreachable in 48 cells** (`:71`). B63 graded it a **Note**, (P) GO WITH NOTES (`:7`): *"The choice stays Kam's (accept, Composer C-58, or move the pill)."* Below Minor, so no fix. Do not move the pill. Re-run your copy of `overlap63.spec.ts` at 1440 Home and `#/quotes` (Seller) **only to show the counts are unchanged** by this round. |
| **X-3** display name to Jira (`:194`) | Note, by design | NOT THIS ROUND | B47 `:84` names it. A change needs Kam's enable / `IncludeMessage` ruling. The probe row (d) stays 1 (row X-2). |
| **X-5** unknown-member detail echo (`:196`) | Note, PRE-EXISTING | NOT THIS ROUND | Main-wide (`POST /api/v1/quotes` does the same at base); the fix is not B47's. |
| **X-6** start refusals print traces (`:197`) | Note, PRE-EXISTING | NOT THIS ROUND | `Program.cs` / `Infrastructure` (frozen); base parity measured. |
| **X-8** `G1_a_burst…` once red under load 40–129 (`:199`) | Note, PRE-EXISTING | NOT THIS ROUND | It is the overlay's test (now on main via #30); 5/5 + 5/5 green on re-run. If it reds in your runs, give the load and re-run; do not edit it. |
| **X-9** `bom.spec.ts:298/:335/:356`, `smoke.spec.ts:13` (`:200`) | Note, PRE-EXISTING | NOT THIS ROUND | Main's tests. Proposed `[B60-2]` widening: Friday records it. |
| **X-10** CodeQL by reading (`:201`) | Note | NOT THIS ROUND | A possible `cs/log-forging` alert at `FeedbackEndpoints.cs:167` (frozen this round). Friday reads CodeQL on the PR; never dismiss. |
| `ApiProcess.cs:66` line (`:26`) | CLOSED-WITH-NOTES | NOT THIS ROUND | Acceptance is Friday's. Do not touch it. |
| a11y by hand: the counter is not tied by `aria-describedby` (`:154`) | not graded | NOT THIS ROUND | Not a finding; `aria-live="polite"` is announced. |

## Test Evidence (run each command as `cmd > out 2>&1; rc=$?`, then read the file)
- **Base vs head** (`wt-B65-base` at `e0bbc6f`, `wt-B60` at your head):
  - .NET full suite, Release `--no-incremental`, **0 warnings**. The gate measured `e0bbc6f` at **235 / 72 / 1,005 = 1,312**, with 1 failure (X-8, load) (`B63:181`). Re-measure; do not trust it. `dotnet list package --vulnerable --include-transitive` 0. Reconcile every count change by test name (`--list-tests`, `comm`): 0 names lost; the added names are yours.
  - Web: lint, typecheck, Vitest (gate: **426 / 58**, `:184`), `npm run build` (dev) and `VITE_MPSCALC_AUTH=entra npm run build`. The Entra bundle holds 0 stub strings, with the gate's control (`:186`).
  - Playwright `b47-feedback.spec.ts` (stub): 20/20 at base, and 20 + yours at head. `b46-home.spec.ts` 13/13 on both.
- **Red-first, per row:** `RED n/m → GREEN` for each new test at `e0bbc6f`. Guards are green at both; say which.
- **Red-proof table, one line per tamper** (tamper → RED on the named tests → sha256 restore + `status --porcelain` empty). Also **re-run B63's R4 and R5 mutants** (`:166-167`, anchors re-derived 1/1 in `FeedbackTickets.cs`). Each must still be RED at head.
- **Gate probes re-run:** the X-2 live probe table (row X-2) and the axe table at 4 sizes (row X-1), base and head, with `uptime` on every run.
- **OFF by default unchanged:** your copy of the gate's 3 OFF arms (absent / `false` / `""`) gives **0** fake requests and 0 sidecars (one pass each).
- **Merge proof:** the Step 0 and end `merge-tree` rows (trees, rc), and the combined-tree suite row (Base and branch).
- **Leak + secret scan** over `git diff e0bbc6f...HEAD` and `git log --format=%B e0bbc6f..HEAD`, using `gitleaks git --redact` plus your copy of `selfscan63.py`. Counts only, with a planted control per class that fires.
- **No frozen change:** run `git diff --numstat e0bbc6f -- src/MpsCalc.Api/Feedback/FeedbackEndpoints.cs src/MpsCalc.Api/Feedback/FeedbackStore.cs docs/api/openapi.json web/src/api web/src/app web/src/screens web/src/feedback/page.ts web/src/feedback/FeedbackDialog.tsx web/src/feedback/csv.ts 'src/MpsCalc.Api/appsettings*.json' '*.csproj' web/package.json web/package-lock.json infra scripts tools .github` and paste the output; it must be empty. `git diff --name-only e0bbc6f` lists only write-set paths. The four held store keys: 0 changes.
- **Processes:** every process you started (pid, port, cwd) and its stop. **0 left at READY.**
- Evidence goes to `Briefs/2026-10-13_B65_evidence/` (folder 0700, files 0600, project path masked as `<P>`; synthetic screens only). Tools and logs go to `.tools/qa-B65/` (0700).

## NEW WORDS (Friday shows Kam before any deploy)
Every new or changed visible string, old → new, verbatim, with `file:line`, who sees it, and its `git grep -i -l` count at `e0bbc6f`. Expected at least:

| Word (verbatim) | Where | Shown to | Old |
|---|---|---|---|
| All feedback table (aria-label) | `FeedbackAdminPanel.tsx` (wrapper) | screen reader, Administrator | none (new) |
| `#/` · `#/quotes` · `#/inventory` · `#/quotes/<id>` · `#/quotes/<id>/proposal` | `FeedbackTickets.cs` (`Page:` line) | Jira readers | the stored path as sent |
| other (in the calculator) | `FeedbackTickets.cs` | Jira readers | the stored path as sent |
| the API.md description sentence | `docs/API.md` (Feedback section) | developers / operators | *"a description with the category, page, …"* |
| + every B63 X-4 UNDECLARED row, verbatim | as B63 `:230`, `:238-245`, `:247` | as B63 | declared by B65 |

## STATUS sections
- BLUF (one line per row).
- **PRIOR WORK** (every cite above re-read; what moved; the B63 line-count check).
- Base read: Step 0 (`M0`, tree, rc), end (`M1`, tree, rc), and whether main moved in between. Then Commits.
- Test Evidence; Red-proof table; Tier-1 conditions.
- FOUND / TESTED / HOW / NOT TESTED per row.
- **The X-2 option chosen and why** (A/B/C/D as above, or another with its reason), and the mapping table as built.
- The X-2 probe table (head vs `e0bbc6f`) and the axe table (4 sizes × personas × states, head vs `e0bbc6f`).
- The X-7 "Continue" line (B63's numbers, plus your unchanged-count re-run).
- The TAKEN / NOT THIS ROUND table as built.
- NEW WORDS; Modified pre-existing tests (before → after, why).
- UNMEASURED.
- `## NOT DONE / NOT COVERED`, as prominent as the evidence.
- needs-Friday:
  - X-3 (display name in Jira) and the Jira enable ruling stay Kam's;
  - X-2 is closed on the branch, but Jira stays OFF on hosted (MPS-9);
  - the feedback store overlap compare (see UNMEASURED);
  - `[B60-1]` / `[B47-D6]` stay Kam's;
  - Jira draft lines (Jira writes are Friday's).
- `## For the records seat` (instead of a history entry): rows to fold once merged: X-3, X-5, X-6, X-9 / `[B60-2]` widening, and the UNMEASURED overlap question.
- Leak + secret scan; processes; worktrees and files left.

## Time-box
**About 2–2.5 h.** If you run short, finish in this order: **X-2** (cells 1–3 + probe), **X-1** (cells 1–2), X-4, then X-1 cell 3 and X-2 cell 4. List what is left as **NOT DONE**, never half-built. There is no round 3.

## UNMEASURED (by the drafter, each with its closing instrument)
- **The feedback store's own overlap compare may share the overlay's W-2 / W-3 blind spots.** `FeedbackStore.cs:173-199` (`RefuseOverlaps`) compares `QuoteFileStore.RealPath` results (`:181-182`) with `OrdinalIgnoreCase` and no NFC step. `:169` takes the reference store's **directory** lexically and never follows the reference **file's** link. These are the classes B58 fixed for the overlay (B58 brief rows W-2, W-3, now on main via #30). B63's 16/16 hosted refusals (`:108`) had no `..`-after-link, NFD or reference-file-link arm. **Not this round:** `FeedbackStore.cs` is frozen, it is not a gate finding, and no hosted feedback path is placed. Name it in needs-Friday and RECORDS; the next gate of this lane probes it.
- Whether Chromium's keyboard-focusable scrollers make X-1 cell 3's Tab step pass at `e0bbc6f`. That closes with your base run.
- The combined tree on `M1`. That closes with the clone suite.
- WebKit/Safari for X-1. That closes only if a WebKit build is already installed.
- CodeQL and CI for your head: Friday reads them on the PR.

## HOLDS
- Datasec only. No other client's names, tickets or paths.
- **The Jira credential is not yours.** Never put it in code, tests, settings or CI. Tests use the fake handler and the literal `test-token-not-real`. **No Jira call to Atlassian, no Jira write.** No price data into Jira, ever: every planted value is synthetic (`PLANTED-B65-…`).
- **Hosted store-path settings unchanged.** None of `MpsCalc__QuoteStore__Path`, `__HostedRoot`, `MpsCalc__CatalogueOverlay__Path` or `MpsCalc__ReferenceStorePath` changes, and nothing places `MpsCalc:Feedback:*` hosted. **SITE HOLD** stands.
- **No PR, no merge, no deploy, no Azure, no hosted request, nothing sent to any human, no `5_Project_History/history.md` entry** (Friday's). The launcher's grant to write history and Jira (`Launch_Claude.command:96`) is void by this brief.
- **CodeQL policy:** push your branch only; never push to main; never dismiss an alert; never ask for a bypass.
- **Q-09:** synthetic data only. Never open `.local/pricebooks/` or the shipped Development reference path. Every API you start sets `MpsCalc__ReferenceStorePath` to a synthetic file or a non-existent scratch path (as B60's probe did), and its stores to roots under `.tools/qa-B65/roots/` or `wt-B60/.local/b65-*` (git-ignored).
- **Never open `4_Credentials/.env`.** No secrets anywhere.
- **Never delete; quarantine** to `.tools/_quarantine/2026-10-13_B65_<what>/` (0700). Never edit a running script.
- **Git:**
  - Allowed: `fetch`, `worktree add --detach` (for `wt-B65-base`), `merge-tree --write-tree` (objects only), commits and pushes on `b60/feedback-pill-on-d711b42`, and the `clone --shared` under `.tools/qa-B65/clone` (never pushed).
  - Never `checkout`/`switch` in `2_Project_Files` or the project root. **Never `rebase`, `merge` into the branch, `gc`, `prune`, `reset`, `worktree remove`, `branch -D` or force-push.** Never push to `b47/…` or `main`.
  - Other seats' worktrees and tools (`wt-B63*`, `qa-B63/`, `wt-B47*`, `qa-B47/`, `qa-B60/`) are read-only. Copy from them.
- **Processes:** kill by port + cwd (or a recorded pid), never by name. Stop everything you started before READY. `caffeinate`, the shared `VBCSCompiler`, `@playwright/mcp` and any listener outside 6630–6639 are not yours. Do not use the Playwright MCP browser: it writes `.playwright-mcp/` into the project root (B60 `:74`).
- **.NET:** `export DOTNET_ROOT='/Volumes/Laptop-DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/.tools/dotnet' PATH="$DOTNET_ROOT:$PATH"`; `-nodeReuse:false -p:UseSharedCompilation=false`. Fix warnings; never suppress them.
- **Instruments:** verdicts are ratios with denominators. Every scanner zero needs a positive control that fired. State `uptime` with every timing. The shell is zsh: run loops and multi-word variables through `bash -c '…'`; no bare `===`. Never take an exit status through a pipe. Never `cat` a file into itself.

## End
The last line of `Briefs/2026-10-13_B65_STATUS.md` is exactly one of:
- `READY FOR GATE: b60/feedback-pill-on-d711b42 <sha>`
- `STOPPED: NEEDS FRIDAY`, followed by ONE question.
