STARTABLE: YES

# B2087 DRAFTER REPORT: OXPd records pass for the product owner's taps of 2026-11-25 11:24, 11:25 and 14:30 (kit for seat R324)

Drafter: in-session, read-only, for Tuesday s327. Clock at start `Wed 25 Nov 2026 15:00:30 AEDT`, last measurement `15:12:52` (both printed by `date`). The kit holds no typed clock in a slot; its MEASURED-BY-DRAFTER clocks are `date` prints.

Files written (and nothing else outside scratch):
- the kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2087_SEAT-R324_oxpd2-records-kam-1125-rulings.md` (sha256 `7a274ed3...`, 80 KB)
- its sidecar `.measured` (78 claims, 0 TODO; `stamp_check.py <kit>` rc 0)
- this report
- scratch only under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s327/d2087/`

## BLUF
- **The kit writes:** ONE C-entry (C-86): the three taps, his 10:52:56 note carried again beside the 11:24 tap, and the coordinator's correction of its false store "delivered" text. ONE appended register section, which supersedes line 1082 ("is open, so no wording is recorded here as decided") by name and does not edit it; it records the wording as ruled, no H9, H7's follow-up still standing, HD-4 to HD-7 PARKED, and corrections to the 11:21 section's last paragraph. ONE Jira create: his action ticket to save the unlabelled copies, assigned to him, label `oxpd-kamil-action`, relating to OXPD2-1, no due date. TWO Jira comments, on OXPD2-57 and OXPD2-1. ONE history entry.
- **It does not touch:** `BACKLOG.md`, 02, 03, `CLAUDE.md` or `HP_QUESTIONS_DRAFT.md`. It makes no Jira move.
- **Seat R324 is free.** It is on 0 of the SEAT kits of 11-24 and 11-25; the controls R322 (3 kits) and R323 (1 kit) were found.
- **OXPd is clear to launch:** 0 panes named OXPd2 and 0 open PRs on `datasecau/OXPd_2` at 15:02. Every project file equals B2083's READY.manifest.

## Facts re-measured, with instruments
- **Cards** (`decision_queue.sh show <id>` into scratch; no `list`):
  - wording card: ruled a at `2026-11-25T14:31:37.129846+11:00`, detail "H1 reworked, H6 2b out, no H9". Its `delivered_artefact` (14:31:43) says the register's B2083 additions "already carry that wording". That is FALSE: register line 1082 says the card is open.
  - passkey card: ruled c, `11:26:03.322474`.
  - labelled-docs card: ruled a, `11:26:00.257737`, no note on the ruling.
- **Board** (`kam_msgs.sh 12`): 11:24:56.310, 11:25:06.551 and 14:30:48.830, each view=tuesday.
- **Rulings** (`kam_rulings_today.sh`, 15:00:54): the 10:52 note row is "as an agent of mine you are part of internal."; no OXPd ruling after 14:30; TAPPED-BUT-OPEN none.
- **Handover reading, commission item 1** (confirmed from the card and from the PDF's Markdown, `HP-QUESTIONS.md` lines 157-297): CONFIRMED, with two precisions.
  - H1 is the register's 20 Nov rework (QBO:511-541) WITH his 24 Nov sign-off, and its opening line is still his to fill in.
  - The PDF's H7 is the 24 Nov text ("newer than 1.8.4.1"), which predates his 10:52 tap. The kit reads 14:30 as not touching H7, so the 10:52 follow-up stands (Q3).
- **Register:** line 1082 holds the open sentence (1 line, case-blind). LIST C's H6 point 2b is at line 750. The file ends with ONE LF.
- **Jira** (GET only, the project reader behind a fence that refused POST, PUT, DELETE and PATCH):
  - The census is 62. `oxpd-kamil-action` is exactly OXPD2-56 to OXPD2-61, and none of them is about the labelled documents.
  - Phrases `unlabelled`, `Internal Use Only`, `Steves Readme`, `Understanding the HP OXPd`, `labelled` and `sensitivity label` each find 0 issues. Controls: `MASTER: questions…` finds OXPD2-1; `chase HP for the OXPd 2 tools` finds OXPD2-56.
  - OXPD2-57: In Progress, 1 comment (41484). OXPD2-1: 12 comments, 1 of them starting `Records pass, 2026-11-25`. That is why this kit's comments start `Second records pass, …`.
  - Link type `10003` is Relates. The assignable user is `616503d4…`.
- **Commission item 4(a), 13:17 versus 13:28:** `ls -lT Design/` shows all four Word/PDF files at `24 Nov 13:17:48`. The OXPD2-55 attachments are `created 13:28:32` to `13:28:45`, with equal sizes. Item 140's "versions of 13:17" is the save time, so it is NOT an error. No BACKLOG edit; one history line (H-FIX) closes B2083's D9.
- **Commission item 4(b), records naming the wording as decided before 14:30 or open after it:**
  - No project record was written after 11:23: the latest mtimes are 11:20 to 11:23.
  - Records saying the wording is "open" were true when written: register :1082 and :1098, C-85's NOT-settled list, and B2083's history H-OWNER. None says it was decided before 14:30.
  - The kit supersedes them; it edits none.
- **Commission item 4(c), the B2078 REVIEW items B2083 left open:**
  - 5.1 and 5.2 are closed by the 14:30 tap, and this kit records them.
  - 5.3(a) and (b) are in the coordinator's tree: PK4:5, AM0:221-222, KA:24/38. They are FOR TUESDAY 3.
  - 5.3(b) for OXPD2-57 and 5.3(c) were closed by B2083's J-57.
  - 5.4 (owed item 103 as H9) is closed by "no H9", recorded in C-86 and REG2.
  - 5.5 (did H5/H3 go out) is folded into C-85's "chasing" reading and C-86's NOT-settled line.
- **Dry build** (`dry.py`, scratch only):
  - 13 texts frozen. K4 (C-86 against the board and store prints) passed 24 of 24.
  - `scan_record` gave 0 problems on 38 lines, with 0 bytes above 126. Jira codes: S-DQUOTE and S-NAME on all three.
  - Line feeds: CLARIFICATIONS 1146 to 1186; register 1098 to 1116; history 350 to 358. The append and position proofs passed, and every scanner control fired.

## D-decisions (the drafter's)
- **D1:** one C-entry for all three taps, in the form of C-85.
- **D2:** the register is changed by appending a section, never by editing line 1082.
- **D3:** no BACKLOG write. Item 140's 13:17 is correct, and item 103 is covered by text.
- **D4:** the ticket names the first document without the person's name in its file name (DRAFTER_RULES 7).
- **D5:** the passkey recommendation line in C-86 quotes the card label "Paul's app later" verbatim. `scan_record` passes it, and C-85's 10:09 line is the precedent.
- **D6:** the H-JIRA wording was changed once, before freezing, because the label `oxpd-kamil-action` fired S-NAME in a record line.
- **D7:** no due date on the new ticket, the same as OXPD2-61.
- **Chain inputs** (each produced earlier or present at BASE):

  | Step | Needs | Made by |
  |---|---|---|
  | 4a | live CLAR, C-number | P-7 |
  | 4b | live register, C-number | 4a / P-7 |
  | 4c T-A7 | C-number | P-7 |
  | 4c J-57 | C-number | P-7 |
  | 4c J-1 | NEW-KEY | T-A7 log |
  | 4d | NEW-KEY, CMT-57, CMT-1, C-number | 4c log |

## Q-questions for Tuesday (each with its default; Q1 to Q9 in the kit)
1. **Register:** append, superseding line 1082 by name. *Default: append.*
2. **C-entries:** one entry, C-86. *Default: one.*
3. **H7:** read as untouched by 14:30, so the 10:52 follow-up stands. *Default: as written.* Alternative: a card to Kam.
4. **HD-4 to HD-7:** parked, "not to be sent while the route is parked". *Default: as written.*
5. **Item 140's 13:17:** not an error; one history line. *Default: as written.*
6. **Ticket due date:** none. *Default: none.*
7. **Ticket naming the documents:** no person's name. *Default: as written.*
8. **Item 103:** unchanged; "no H9" is recorded in C-86 and REG2. *Default: as written.*
9. **Handover reading:** confirmed, with the two precisions above. *Default: as written.*

## UNMEASURED
- Whether Kam has already sent the PDF's texts.
- The PDF's exact rendering. I read its Markdown source, not the PDF.
- Jira's answer to a paragraphs-only create with no `duedate`. B2034's creates used blockquotes and dues.
- The seat's helper, its selftest and every live POST (marked NEVER RUN in the kit).

## Outside-the-fences disclosure
- I invoked `kam_rulings_today.sh` and `kam_msgs.sh 12` (the board reader) without reading their headers first. The commission names the first.
  - The rulings print in scratch (`kam_rulings_today.txt`, row 15) holds an HPSM message with a temporary password typed by Kam at 11:52. It is on another project.
  - That password was not copied into the kit, the sidecar or this report. The file sits in the coordinator's scratch only. **Tuesday may want to quarantine it.**
- One GET `user/assignable/search` printed Kam's work e-mail address and the Jira site host into my context. Neither went into any file.
- One `gh api -X GET` (open and closed pulls) ran under the project's `GH_CONFIG_DIR`.
- One Bash call with `cd` was refused by the hook. It had no effect.
- `decision_queue.sh show` was run 3 times, each into scratch with an exact id; `list` was never used.
- Nothing was written to the project, Jira, GitHub or the card store. Nothing was sent to any person.
