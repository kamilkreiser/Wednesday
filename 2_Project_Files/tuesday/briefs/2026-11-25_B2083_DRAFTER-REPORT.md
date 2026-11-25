STARTABLE: YES

# B2083 DRAFTER REPORT: kit `2026-11-25_B2083_SEAT-R322_oxpd2-records-hp19-hpasks.md` (seat R322, OXPd 2 records and Jira)

Drafted Wed 25 Nov 2026 from 10:55:27 AEDT (`date`); the last drafting check at 11:10. The drafter wrote three files in the briefs folder (the kit, its `.measured` sidecar and this report) and its scratch `fleet/state/s326/d2083/`. Nothing was written to the project, Jira, GitHub or the card store.

## BLUF
- The kit records the product owner's 1.9 ruling and his "chasing" word in the B2072 form (HOLD R, HOLD R2, frozen texts, proofs by position) and the B2034 form (a C-entry built by program from the board and store prints; Jira POSTs behind a fence; a write log; read-backs).
- It writes six project files, each once: C-85; one register section in `Registers/QUESTIONS_BY_OWNER.md`; one change-log paragraph in each of 02 and 03; owed item 140; one history entry.
- It makes five Jira POSTs: comments on OXPD2-56, OXPD2-57 and OXPD2-1, and transition `31` (In Progress) on OXPD2-56 and OXPD2-57.
- RECORDS and JIRA default to HOLD.
- Checks: `stamp_check.py` rc 0 (82 claims, 82 measured); the dry build passed every proof; the project's scanner found 0 problems on 45 record lines.
- **The one design risk to weigh is Q1.** Adding change-log entries to the `.md` now makes 02 and 03 newer than their Word and PDF, and newer than the files attached to OXPD2-55. The 11-24 lesson wants the latest version on Jira in the same work unit, and a records seat cannot render. Owed item 140 carries this. Option (b) avoids it.

## Facts re-measured (each with its instrument)
- **Cards** (`decision_queue.sh show`, each into scratch, then an id inclusion filter):
  - `datasec-oxpd-hp-19-target-1125`: ruled a, `ruled_ts=2026-11-25T10:53:01.942292+11:00`, no note. The board tap was at 10:52:14 (`kam_msgs.sh 10`).
  - `datasec-oxpd-hp-questions-wording-1125`, `datasec-oxpd-passkey-route-1125` and `datasec-oxpd-two-labelled-docs-1125`: all OPEN.
  - The filter also found `datasec-oxpd-kd2-oxpd19-files-1124`. It appears only as a mention inside the 1.9 card's BLUF.
- **`kam_rulings_today.sh` at 10:55:57** (run with `KAM_READ_MARKER` pointed at scratch, so Tuesday's read marker was not moved):
  - 10 rows. No correction of 10:17:56.
  - New: **10:52:56, a note on the labelled-docs card: "as an agent of mine you are part of internal."** No option was chosen and the card is still open. The kit records it in C-85 (Q9).
  - Rows at 10:48 and 10:58 are HPSM. The 06:57 rows are other cards.
- **Project record files** (`shasum`): the five files of the B2072 manifest all equal it. B2072 STATUS ends `READY B2072: 26bb1132…`. Owed items 1 to 139 (94 open, 45 ticked). C-1 to C-84. The anchor heading is at line 1022.
- **Design and discovery tree** (`sed`/`grep`):
  - 02 line 266 says "treat as absent"; 03 line 466 says "build on 1.8.4.1".
  - Both files end with a "Still owed after this pass" line.
  - Discovery-tree line 3 holds `OXPd:Action` and `OXPd:Security`, both 2025/01/29.
- **The register** (`tail -c`): `QUESTIONS_BY_OWNER.md` ends with TWO line feeds. PART 2 appends with no extra empty line; the dry build proves this.
- **Jira** (GET only; the fence refused POST, PUT, DELETE and PATCH):
  - Census 62 issues.
  - OXPD2-56 and OXPD2-57: Backlog, 0 comments, transition `31` to status `3` offered with `hasScreen` false.
  - OXPD2-57's description holds `Registers/HP_QUESTIONS_DRAFT.md` and "anything more recent than OXPd 1.9 … no SDK is asked for".
  - OXPD2-1 has 11 comments.
  - OXPD2-55's newest attachments are the 13:17 Word and PDF files (ids 23951 to 23954).
  - Phrase checks: `started chasing`, `1.9 SDK`, `HD-1`, `Target HP` and `WebAuthn` each find 0. `QUESTIONS_BY_OWNER` finds OXPD2-1.
- **No OXPd pane is live** (`tmux list-panes -a`: `%0 tuesday` and two unnamed panes). R322 is free.

## The partition finding (commission item 3)
- **Project records:** only Jira OXPD2-57. It points at the superseded `HP_QUESTIONS_DRAFT.md`, and its H7 wording is now superseded too. The kit corrects both by comment J-57. The description is not edited.
- **Tuesday's own briefs** (all in `tuesday/briefs/2026-11-24_B2027_answers/`; outside the seat's scope and listed in the kit's FOR TUESDAY 3):
  - `pack-v4/…_v4.md` line 5: "2 sent to HP".
  - `ANSWERS-MAP.md` lines 221 and 222: Q40 and Q41 marked "sent to HP".
  - `KAMIL-ACTIONS.r1.md` lines 24 and 38.
  - Also: the B2078 `HP-QUESTIONS.md` and PDF carry the H7 text from before the 1.9 ruling.
- **Project folder check:** a name search over the project, with `Source_Documents/`, `2_Project_Files/`, `.tools/` and the credential folders pruned, found no copy of the pack, the answers map or the actions file.

## D-decisions (the drafter's)
- **D1. Register:** the HP drafts go in `QUESTIONS_BY_OWNER.md`, because its line 3 names it the working document. `HP_QUESTIONS_DRAFT.md` is not touched.
- **D2. Write order:** C-85, then the register, then 02 and 03, then Jira, then the BACKLOG, then history. The Jira comments therefore point only at text that already exists. The history entry names the comment ids.
- **D3. The register text does not assert the Jira moves**, because it is written before them.
- **D4. Comment read-back is compared by paragraphs.** The reader's `adf_text` joins paragraphs with no separator, as measured on the OXPD2-57 description.
- **D5. How the kit file was built:** texts were substituted into the kit, and its tables filled, by the drafter's Python (`texts.py`, then an inline program). Only the kit file was written. Disclosed below because DRAFTER_RULES says "with the Write/Edit tools".

## Questions for Tuesday (each with its default; listed fully in the kit as Q1 to Q10)
1. **Q1, design text.** Default: change-log entries in 02 and 03 now, with the Word and PDF re-render and the attachment to OXPD2-55 owed as item 140. Alternative (b): no design write now, so no stale Jira reference.
2. **Q2, the moves.** Default: In Progress. Alternatives: Done, or comments only.
3. **Q3, scope of C-85.** Default: every one of his OXPd words of the day (09:58:59 to 10:52:56), under the project rule "every word". Alternative: only 10:17 and the two 10:52 rows.
4. **Q4, which register.** Default: `QUESTIONS_BY_OWNER.md`.
5. **Q5, numbering.** Default: HD-1 to HD-7, so none collides with the "H9" the wording card offers.
6. **Q6, OXPD2-1.** Default: one comment (J-1), under CLAUDE.md lines 12 and 13.
7. **Q7, where each HP question goes.** Default: WIP Q1 becomes H7; WIP Q3, Q4 and Q7 become HD-1 to HD-3; the four passkey questions become HD-4 to HD-7.
8. **Q8, his questions from the two documents.** Default: no tickets. The lesson covers actions he puts on himself, and C-84 (14:07) says to put them on the fleet activity.
9. **Q9, the 10:52:56 note.** Default: recorded in C-85; the card stays open and nothing is acted on.
10. **Q10, passkey section 11.** It is not carried while its card is open (the commission's rule).

## UNMEASURED
- Which text of H1 to H8 he actually sent. The kit says so in every text.
- Whether a correction of the "chasing" reading arrives before the stamp. The CHASING slot holds this, and REFUSE 6 stops the run if the slot says anything but `no correction`.
- The seat's helper, HOLD R and R2 on live files, and every Jira POST and read-back have never run on a real output. The comment POST and the `31` move are new to this project's kits.

## Outside-the-fences disclosure
- I read the NAS file `/Volumes/DEV-Working/Datasec/WIP/OXpd1.9/1.9.0 Release Notes.txt` (`ls`, `shasum`, `sed -n 1,9p`; read-only) to confirm the facts the kit relays. The seat is forbidden to read it.
- I ran a `find` (names only) over the OXPd project with `Source_Documents/` pruned, plus `.tools/`, `2_Project_Files/` and the credential folders.
- I ran `kam_msgs.sh 10` (read-only; no attachment fetch) and `kam_rulings_today.sh` (marker pointed at scratch).
- Jira: GET only, through a byte copy of the project's reader.
- The kit file was written by a Python program (D5).
- The kit's C-85 quotes a colleague's first name verbatim, in his 10:09 message. This is the C-82 precedent, and `scan_record` does not flag it. The Jira texts name him as "Kam", the B2034 precedent, and the coded `S-NAME` stands.
- No test was run and no lock was touched. B2081's NexusAI jest lock was left alone.
