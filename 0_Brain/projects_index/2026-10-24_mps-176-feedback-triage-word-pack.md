# MPSCALC-176 word pack: feedback triage and "My feedback"

Drafted by Tuesday, 2026-10-24, for the product owner's approval. Ruling that asked for it: card "MPS Calculator: feedback triage ... Draft the words now?", option a (2026-10-24 11:52): "Tuesday drafts every label and message for triage and 'My feedback' and posts it as one card for your approval. No build before that." **Nothing is built. Every word below is a proposal until the card is approved.**

Ticket: MPSCALC-176 "Feedback for Administrators and senders: triage status and notes, and "My feedback"" (Jira GET, status Backlog, priority Low). Its acceptance check reads: "A triage sidecar per item (item file never rewritten) and a caller-scoped list; words approved first."

## How each fact was read (this run)

- Project record, `Datasec MPS Commercial Calculator/`: `BACKLOG.md` lines 757 ([B47-D2]: "status (open, in progress, done, dismissed), priority and notes for Administrators"), 763 and 821 (TICKET BL-15 to MPSCALC-176), 815 ([B47-D10]: ""My feedback" for the person who sent it (Composer has it)"); register `1_Project_Definition/Registers/2026-10-16_*review-items.md` lines 168, 176, 355 (section 4a, row BL-15); `1_Project_Definition/CLARIFICATIONS.md` lines 336 (MPS-9), 361-372 (C-25), 392-404 (C-26), 420-430 (C-28), 472 and 481 (roles), 532-539 (C-37).
- Existing feedback words, code repo `2_Project_Files`, `git show` / `git grep` on `origin/main` = `a5b4bbb5d377f29dd63bf0c64d54b44c122a6055`: `web/src/feedback/words.ts`, `FeedbackAdminPanel.tsx`, `FeedbackDialog.tsx`, `FeedbackPill.tsx`; for house style also `web/src/screens/QuoteList.tsx`, `web/src/screens/inventory/PriceEditForm.tsx`, `web/src/proposal/template/sections.ts`, `web/src/proposal/fixtures/s4Proposal.ts`.
- Ruled cards, `decision_queue.sh show <id>`: `mpscalc-feedback-pill-words-1013`, `mpscalc-feedback-attachments-1013`, `mpscalc-feedback-401-words-1017` (all three status `ruled`, choice a).
- Jira: one GET of MPSCALC-176 (JQL began `project = MPSCALC AND`).

## House voice, as read

Sentence case (`Send feedback`, `All feedback`, `Last updated`). Status words are one capitalised word (QuoteList.tsx:135 prints `Draft`, `Submitted`). Messages are short full sentences with a full stop; failures are "The X could not be Y." (FeedbackAdminPanel.tsx:36, :51, :63) or "Your feedback could not be sent. Try again." (words.ts:10, ruled by the 401 card). Empty states are "No X yet." (FeedbackAdminPanel.tsx:81; QuoteList.tsx:241). Busy button text is "Saving…" (PriceEditForm.tsx:89). Buttons that save say "Save <thing>" (PriceEditForm.tsx:89 "Save price"; QuoteScreen.tsx:349 "Save draft"). Screen-reader names read "<Thing> list" / "<Thing> table" (FeedbackAdminPanel.tsx:70, :85).

## Where things live today (shapes the wording)

There is no separate "All feedback" page. The feedback pill (FeedbackPill.tsx:66, word `Feedback`) opens a dialog whose heading is `Feedback` (FeedbackDialog.tsx:141). Only an Administrator sees two tabs, `Send feedback` and `All feedback` (FeedbackDialog.tsx:146-154); anyone else sees only the send form. So "nav label" below means a tab in that dialog; no new page or menu entry is proposed.

## The pack

Mark: NEW = no existing word fits; REUSED = the exact existing word, with source.

### 1. Statuses

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| S1 | Status cell and Status filter (Administrator); Status cell (sender) | `Open` | One of the four named at BACKLOG.md:757. A new item starts here. Capitalised single word like QuoteList.tsx:135 | NEW |
| S2 | same | `In progress` | BACKLOG.md:757 ("in progress"), sentence case | NEW |
| S3 | same | `Done` | BACKLOG.md:757 | NEW |
| S4 | same | `Dismissed` | BACKLOG.md:757 | NEW |
| S5 | Under the Administrator's status picker (hint text, linked to the picker) | `Open: not looked at yet. In progress: someone is working on it. Done: dealt with. Dismissed: no action planned.` | Helper text; the record gives only the four names, so the meanings are Tuesday's draft. House pattern: muted small hint line (FeedbackDialog.tsx:203) | NEW |
| S6 | Column header, Administrator list and sender list | `Status` | QuoteList.tsx:105 | REUSED |
| S7 | Screen-reader name of the Administrator's status picker | `Status` | Same one-word picker name as QuoteList.tsx:38 (`aria-label="Owner"`) | REUSED |

### 2. Priority

The record names no levels: BACKLOG.md:757 and Jira MPSCALC-176 say only "priority". Smallest useful set proposed: **two levels**.

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| P1 | Column header and picker label, Administrator list | `Priority` | sections.ts:415 (`'Priority'`) | REUSED |
| P2 | Priority picker, default for every item | `Normal` | Default level; two levels are enough to separate "look at this first" from the rest | NEW |
| P3 | Priority picker | `High` | s4Proposal.ts:97 (`priority: 'High'`) | REUSED |
| P4 | Screen-reader name of the priority picker | `Priority` | Same pattern as S7 | REUSED |

(If three levels are wanted, `Medium` is REUSED from s4Proposal.ts:98 and `Low` would be NEW; see question 2.)

### 3. Administrator notes field

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| N1 | Label of the notes box on an item (Administrator only) | `Notes` | Plain one-word label, like `Message` and `Category` (FeedbackDialog.tsx:161, :178) | NEW |
| N2 | Hint under the label | `Only Administrators can see notes.` | Makes the audience plain; matches the Administrator-only rule already told for files (C-28, CLARIFICATIONS.md:426) | NEW |
| N3 | Placeholder in the empty box | `Add a note` | Short imperative, as `Add item` (ManualItemForm.tsx:108) | NEW |
| N4 | Shown in place of the notes when none are saved | `No notes yet.` | Pattern of FeedbackAdminPanel.tsx:81 and QuoteList.tsx:241 | NEW |
| N5 | Save button | `Save note` | Pattern of `Save price` (PriceEditForm.tsx:89) | NEW |
| N6 | Save button while saving | `Saving…` | PriceEditForm.tsx:89 | REUSED |
| N7 | Message after a successful save (status role, not alert) | `Note saved.` | Pattern of words.ts:7 ("Thanks, your feedback is saved.") | NEW |
| N8 | Message when the save fails (alert) | `The note could not be saved. Try again.` | Pattern of words.ts:10 and FeedbackAdminPanel.tsx:51 | NEW |
| N9 | Character counter under the box | `{length} / {max}` | Same counter shape as FeedbackDialog.tsx:175. The maximum is not in the record; 2000 is suggested because the quote notes field uses 2000 (openapi.snapshot.json:853); a number, not a word | REUSED (shape) |

### 4. Administrator triage list (the `All feedback` tab)

Existing columns stay as they are: When, From, Category, Page, Message, Attachments, Ticket (FeedbackAdminPanel.tsx:89-95). Three are added after Ticket: Status, Priority, Notes.

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| T1 | Tab label and title (unchanged) | `All feedback` | words.ts:6 | REUSED |
| T2 | Screen-reader names (unchanged) | `All feedback list`, `All feedback table` | FeedbackAdminPanel.tsx:70, :85; the second was approved by card mpscalc-feedback-pill-words-1013 | REUSED |
| T3 | New column headers | `Status`, `Priority` | S6, P1 | REUSED |
| T4 | New column header | `Notes` | N1 | NEW |
| T5 | Filter: Status picker, first option (all shown) | `All statuses` | Pattern of `All owners` (QuoteList.tsx:39) | NEW |
| T6 | Filter: Status picker, other options | `Open`, `In progress`, `Done`, `Dismissed` | S1 to S4 | NEW (same as S1-S4) |
| T7 | Filter reset button | `Clear filters` | QuoteList.tsx:54 | REUSED |
| T8 | Empty state, no feedback at all | `No feedback yet.` | FeedbackAdminPanel.tsx:81 | REUSED |
| T9 | Empty state, filter matches nothing | `No feedback matches these filters.` | Pattern of T8; no existing "no match" sentence found in `web/src` | NEW |
| T10 | Loading and refresh (unchanged) | `Loading…`, `Refresh` | FeedbackAdminPanel.tsx:80, :73 | REUSED |
| T11 | Confirmation after a status change (status role) | `Status changed to {status}.` | Pattern of N7; `{status}` is one of S1 to S4 | NEW |
| T12 | Confirmation after a priority change (status role) | `Priority changed to {priority}.` | Same | NEW |
| T13 | Error when a status change fails (alert) | `The status could not be changed. Try again.` | Pattern of words.ts:10 | NEW |
| T14 | Error when a priority change fails (alert) | `The priority could not be changed. Try again.` | Same | NEW |
| T15 | Error when the list does not load (unchanged) | `The feedback list could not be loaded.` | FeedbackAdminPanel.tsx:36 | REUSED |

### 5. Sender's "My feedback"

Placement proposed: a third tab in the same dialog, so no new menu. Today the tab strip is drawn only for Administrators (FeedbackDialog.tsx:146); it would be drawn for everyone, with `Send feedback` and `My feedback` (and `All feedback` for Administrators).

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| M1 | Tab label (the "nav label") and the screen's title | `My feedback` | The record's own words: BACKLOG.md:815, register row at line 176 | NEW |
| M2 | Dialog heading (unchanged) | `Feedback` | FeedbackDialog.tsx:141 | REUSED |
| M3 | The other tab (unchanged) | `Send feedback` | words.ts:5 | REUSED |
| M4 | Screen-reader names | `My feedback list`, `My feedback table` | Pattern of FeedbackAdminPanel.tsx:70, :85 | NEW |
| M5 | Columns, in this order | `When`, `Category`, `Message`, `Status`, `Reference` | When, Category, Message: FeedbackAdminPanel.tsx:89, :91, :93; Status: S6; `Reference` is the word shown after sending (FeedbackDialog.tsx:229; the reference is the first 8 characters of the item id, :129). No `From`, `Page`, `Attachments` or `Ticket`: the sender knows these, cannot download files (C-28), and the Jira ticket is off (MPS-9, CLARIFICATIONS.md:336) | REUSED |
| M6 | Status as the sender sees it | `Open`, `In progress`, `Done`, `Dismissed` | Same four words as S1 to S4. Recommended: the sender sees status only | NEW (same as S1-S4) |
| M7 | Administrator notes and priority | **not shown to senders** | Nothing in the record says senders see either (BACKLOG.md:815 "a sender sees the reference once, after sending"). Notes may hold candid comments. Flagged as question 1 | n/a |
| M8 | Empty state | `No feedback yet.` | FeedbackAdminPanel.tsx:81 | REUSED |
| M9 | Error when the list does not load | `The feedback list could not be loaded.` | FeedbackAdminPanel.tsx:36 | REUSED |
| M10 | Loading (unchanged) | `Loading…` | FeedbackAdminPanel.tsx:80 | REUSED |

### 6. Email or notification text

| ID | Where it appears | Proposed words | Why / source | Mark |
|---|---|---|---|---|
| E1 | none | **None.** | Nothing in the record requires a message to the sender when a status changes: BACKLOG.md:757, :815 and Jira MPSCALC-176 ask for none, and MPS-9 (CLARIFICATIONS.md:336) records "No credential is placed and no outbound connection is opened." The sender finds the status by opening `My feedback`. | n/a |

## Row count

Counting the pack rows above (S1-S7, P1-P4, N1-N9, T1-T15, M1-M10, E1 = 46 rows; M7 and E1 carry no words):

- **NEW: 24** (S1, S2, S3, S4, S5; P2; N1, N2, N3, N4, N5, N7, N8; T4, T5, T6, T9, T11, T12, T13, T14; M1, M4, M6).
- **REUSED: 20** (S6, S7; P1, P3, P4; N6, N9; T1, T2, T3, T7, T8, T10, T15; M2, M3, M5, M8, M9, M10).
- **No words (n/a): 2** (M7, E1).

Several NEW rows repeat words already counted (T6, M6 repeat S1 to S4); the distinct new words are fewer than 24.

## Open questions for the product owner

1. **Do senders see the Administrator's notes and priority on `My feedback`?** Recommended default: **no**; senders see their own message, category, reference and the four-word status only.
2. **How many priority levels?** Recommended default: **two** (`Normal`, `High`), because the record names none and two is the smallest set that separates urgent from the rest. Alternative: three (`Low`, `Medium`, `High`).
3. **Where does `My feedback` live, given the 16 October direction on roles?** Recommended default: **a third tab in the Feedback dialog, shown to every signed-in person**, built as written whatever the roles ruling becomes. The record quotes a direction to make everyone an Administrator (CLARIFICATIONS.md:472) and says how roles are granted is not settled (:481). If that is ruled, every person would also see `All feedback`, and `My feedback` stays useful as the personal view.

## UNMEASURED

- The code was read on `origin/main` `a5b4bbb5`; I did not check whether another branch or open pull request already touches these files.
- Whether the Administrator's CSV download (csv.ts, not opened) should gain Status, Priority and Notes columns; no CSV words are proposed.
- How the item's status is stored (BACKLOG.md:758 says a sidecar file) and what happens when two Administrators change the same item at once; no "changed by someone else" message is drafted.
- The maximum length of a note (N9 suggests 2000, unchosen).
- Whether `Dismissed` reads harshly to a sender; no sender-facing alternative was tested.
- Whether a status change should show who changed it and when (no "Last updated" or "Changed by" word drafted; QuoteList.tsx:106 has `Last updated` if wanted).
- Mobile and narrow-width fit of three extra columns; no screen was run (the hosted app was not contacted).
