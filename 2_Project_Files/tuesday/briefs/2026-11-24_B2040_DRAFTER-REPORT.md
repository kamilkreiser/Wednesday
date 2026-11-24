STARTABLE: YES (once Tuesday fills slot DESIGN after the document agent's last round and the review's corrections are installed; until then Step 0 REFUSES by design)

# B2040 DRAFTER REPORT: kit `2026-11-24_B2040_SEAT-R313_oxpd2-r-design-recent-records.md` (seat R313, Datasec / OXPd 2)

## BLUF
- The kit attaches the new 02 and 03 (Word and PDF) to OXPD2-55 as four more attachments (the four from 12:02 stay), and posts ONE comment on it naming them the latest.
- It writes C-83: his tap of 12:54 on Recent with the note "rebuild without graph", his firmware messages of 12:22 and 12:31, the coordinator's F81 and F82 decisions (marked as the coordinator's), the M577 firmware context, and the new attachment and comment ids.
- In `BACKLOG.md` it ticks owed item 113 and files new owed items: OP-20's narrowed tenant test, the code read from pull request 45 on, and (slot CLARIFY OPEN only) his unanswered note.
- Under slot CLAUDEMD APPLY (the default) it makes the one exact-string edit of `CLAUDE.md` lines 58 to 62 and ticks 114. It also writes one history entry.
- Write order: Jira (4 uploads, then the comment), then CLARIFICATIONS, CLAUDE.md, BACKLOG, history. The records come after Jira because they name the ids Jira returns.
- The design files were still changing while I drafted: round 4 was installed at 13:01:19 and another save landed at 13:04:53. So the kit names no version. Slot DESIGN does, and Step 0 refuses any difference (D-0). It also refuses a file equal to what B2034 already attached (D-NEW).
- The kit's facts about the documents are 12 exact fragments. The seat re-checks each in the staged Word text, and a missing fragment is a STOP for Tuesday.
- His note was still unanswered at 13:14:40 (rulings reader; newest row 12:54:25). The kit carries both variants.
- Kit: 393 lines, 90664 bytes, 21 frozen texts. Sidecar: 88 claims. `stamp_check.py` exit 0.

## Facts re-measured with instruments (clocks from `date`; drafting 13:01:55 to about 13:16)
- **Board** (`kam_msgs.sh 15`, 13:02:04):
  - His rows after C-82: 12:22:36.723 (USB/firmware), 12:31:27.861 ("you can del"), and the Recent tap twice, at 12:54:23.837 and 12:54:25.665 (same text).
  - None after that, re-checked by `kam_rulings_today.sh` at 13:14:40.
- **Store** (`decision_queue.sh show datasec-oxpd-onedrive-recent-deprecated-1124`): choice b, ruled_ts 2026-11-24T12:55:44.256139+11:00, recommended a "Ask tonight, decide after".
- **The coordinator's board record** (`chat_tuesday.json`, extracted to `coord_msgs.txt`):
  - 12:55:59 the clarification question, with its default.
  - 12:59:07 the F81 notice ("you can reverse it").
  - 12:35:26 the stick ready, and his "you can delete".
- **Jira, GET only** through `b1785.py` (13:03:36 to 13:03:48):
  - OXPD2-55: Backlog, assignee 616503d4…, label `oxpd-reference-docs`, 1 Relates link to OXPD2-1, 0 comments. It holds exactly 4 attachments, 23947 to 23950, each with the right name and size.
  - Census: 61 issues. `attachments IS NOT EMPTY` returns [OXPD2-55]. Done returns the four. `uploadLimit` is 1073741824.
  - Phrase `remoteItem` returns [] (control: MASTER finds OXPD2-1). OXPD2-99999 returns 404.
- **Records equal B2034's READY.manifest:**

| File | sha256 (prefix) |
|---|---|
| CLARIFICATIONS.md | d1553c42 |
| BACKLOG.md | eb325dca |
| history.md | b4eccc14 |
| register | e2621f1b |
| CLAUDE.md | 1a2e5629 (unchanged since B2034) |

- **Record counts:** 82 C headings; 114 owed items; anchor at line 831. All P-3 probes are as printed in the kit, each with its control.
- **CLAUDE.md:** lines 58 to 62, as one string, occur once. The dry build keeps 89 lines, and the new sha256 is PREDICTED as 307f16f8.
- **Design files at 13:13:25:**

| File | Bytes | Saved |
|---|---|---|
| `02_architecture.docx` | 171285 | 13:04:53 |
| `02_architecture.pdf` | 2879946 | 13:04:53 |
| `03_plan-of-attack-and-build.docx` | 111175 | 13:04:53 |
| `03_plan-of-attack-and-build.pdf` | 1660936 | 13:04:53 |

  Each differs from B2034's attached sha256. All 12 fact fragments are present (control `zzqxnonexist` reads 0).
- **Seat id R313 is free:**
  - A whole-word scan of today's and yesterday's 52 SEAT kits finds R313 0 times (control R311: 2 files; R312: 1).
  - `tmux list-panes -a` shows `%0 tuesday` and two unnamed panes, with no OXPd pane.
- **Model:** project `CLAUDE.md` line 7, over `model-routing.md` line 98 (row C8). `models_latest.json` line 17 gives `claude-opus-5-5`.

## D-decisions (the drafter's)
- **D1. Jira writes come first, records after.** C-83 and the 113 tick must carry the attachment and comment ids. B2034 wrote CLARIFICATIONS first because its C-82 needed no ids.
- **D2. The new version stands on a slot, not on hashes in the kit.** The files will change again after I finish (lane D, then the review's corrections). D-0 makes the stamp the version. D-NEW stops a re-attach of the 12:02 files.
- **D3. Fact fragments in the staged Word text.** These stand in for an `.md` read: the seat never opens an `.md`. Word text is plain stdlib (zip and `word/document.xml`), with no new dependency.
- **D4. The comment's idempotency comes from the comment list, not a JQL search.** The list is read on OXPD2-55 itself: total 0 → post; an equal comment → skip; any other comment → STOP.
- **D5. Upload idempotency.** The four old ids must still be there. A new attachment with the same name and the staged size is a skip. The same name with another size is a STOP.
- **D6. CLAUDE.md edit keeps 89 lines.** It is a 5-line span becoming 5 lines, so every `CLAUDE.md:<n>` pointer outside 58 to 62 still holds.
  - Line 62 is changed too, because owed item 114 names it: "No agent has run anything on a printer, a simulator or a Microsoft 365 tenant yet", plus a pointer to the first Azure run.
  - The spend sentence is written as the coordinator's reading, not his word.
- **D7. Three owed items for what stays open.** BL-NOTE is filed only under CLARIFY OPEN, and is numbered last so the other numbers never move.
- **D8. Clocks from the board, not the commission.**
  - The commission's 12:22:55 is 12:22:36 on the board, and its 12:54:25 tap is two board rows, 12:54:23 and 12:54:25. C-83 writes both, in C-81's "the board holds the same message twice" form.
  - The commission's "C-76..C-78" for the M577 is C-72, C-76 and C-77 in the record: C-78 is the Azure test VM. C-83 cites C-72, C-76 and C-77.
- **D9. Wording kept neutral.**
  - No owner word for the release notes or guide in the comment or in C-83 (see Q6).
  - The comment names no person. `scan_jira` prints `S-DQUOTE` only.

## Q-questions for Tuesday (each with a default)
- **Q1, slot JIRA:** default WRITE.
- **Q2, slot CLARIFY:** default OPEN.
  - If he answers before the stamp with words that keep the default reading, use `ANSWERED <HH:MM:SS> | <print path> | <sha256>`. That needs a fresh `kam_msgs.sh` print saved by Tuesday.
  - **If he means "no Graph at all", do not launch:** the documents' reading changes.
- **Q3, slot CLAUDEMD:** default APPLY (the commission's default).
- **Q4, PART 5 wording:** default as frozen. The text includes "creates there only what its brief names", a narrowing of his "full control", written as the rule. If Tuesday wants his note's breadth instead, CLAUDE-NEW is re-hashed.
- **Q5, the comment calls the 12:02 four "the earlier version" and says they stay:** default as frozen.
- **Q6, no owner word for HP's release notes or the OneDrive guide:** default as frozen. This is the review's i1, and C-82 says "Datasec's own customer guides".
- **Q7, three owed items:** default as frozen. The alternative leaves OP-20 to the documents' own open-points list.
- **Q8, C-83 relays the coordinator's USB-stick preparation and its reading of "you can del":** default as frozen.
- **Q9 (new), the fragment list:** if the review's corrections re-word any of FF1 to FF12, Step 0's fragment check stops the seat. Re-run `docx_frag.py` on the stamped files at the stamp.
  - Default: Tuesday re-runs it (1 command, below) and accepts.
  - If a fragment is gone, re-commission a fragment refresh. The texts CM and C-83 rest on them.
  - Command: `python3 -I -B /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/b2040/docx_frag.py '<docx>' '<fragment>' ...`

## Chain inputs (each step's inputs exist at BASE or are made by an earlier step)

| Step | Inputs | Where from |
|---|---|---|
| 0 | kit, sidecar, slots, Design files, B2034 manifest | BASE (stamp) |
| 1 | b1785.py, b2034.py (models) | BASE |
| 2 | sources rows 1–13, staged copies | BASE; staging in Step 2 itself (D-2) |
| 3 | frozen texts, live record bytes, staged copies, prototype ids | kit, BASE, Step 2 |
| 4a/4b | staged copies, filled CM | Steps 2 and 3 |
| 4c to 4f | write log ids from 4a/4b; live record bytes | Steps 4a/4b; BASE |

## UNMEASURED
- The seat's `b2040.py` and its selftest have not been written or run.
- No POST of this kit has ever run. No comment exists on OXPD2 to model the read-back from: the comment shape is B1785's `do_comment`.
- How Jira handles a second same-named attachment on one issue.
- The tick proof and the `CLAUDE.md` HOLD R on the live files.
- The CLARIFY ANSWERED path, which was scanned only with a prototype answer.
- Whether `05_readiness-to-build` (its `.md` and PDF were re-saved at 12:58:25, with a `.pre-1124b` copy beside it) agrees with the new 02 and 03. Not read, not attached, and named in FOR TUESDAY 5.
- The documents still say "C-entry to follow" where C-83 will stand. A later document pass may fill in the number; this kit edits no document.

## Outside-the-fences disclosure
- **Read:**
  - Lane D's scratch in the coordinator's tree: `s322/D/apply_b2037_r4.py`, and a `/usr/bin/grep` of `r4/*.md` for `B2037`.
  - The live Design `.md` files: `02_architecture.md` lines 3, 98, 170, 171, 212 and 231, r4's `02_architecture.md` from line 1368 to its end (the change log), and `03_plan-of-attack-and-build.md` lines 312 and 539. The kit forbids the SEAT from opening an `.md`; I read them to learn the changes.
  - The review `B2038_review/REVIEW.md`.
  - The commission B2037.
  - `chat_tuesday.json`: three coordinator rows, filtered by clock.
  - The first rows of `EXPIRING-GRANTS.md` (the preview of the first row).
  - `CLAUDE.md` whole (89 lines), and CLARIFICATIONS ranges 1-4, 722-740, 920-928 and 978-1000.
- **Ran:** `kam_msgs.sh 15`, `kam_rulings_today.sh` twice, and `decision_queue.sh show <exact id>` once. Never `list`.
- **Jira GETs:** 22 named reads (11 issue or attachment GETs, 6 searches, 5 phrase searches; a search may page) through the project reader (`jira_get.py`). Its JSON log was written under my scratch `get/`.
- **No write** outside `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/b2040/`, the kit, its `.measured` sidecar, and this report.
- **Not used:** az, gh, git, mail, Artifact or Docs.
- **No `.pre-stamp` copy:** none was made; that is Tuesday's at the stamp.
