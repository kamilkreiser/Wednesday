STARTABLE: YES

# B2034 DRAFTER REPORT (Opus, in-session, read-only): kit for seat R311, OXPd 2 Jira docs, Kam's actions, four closes, records

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2034_SEAT-R311_oxpd2-r-jira-docs-actions.md` (96142 bytes, 481 line feeds, 26 frozen texts, 10 slot lines).
Sidecar: same name plus `.measured` (97 claims, all measured; `stamp_check.py <kit>` exit 0).
Scratch (programs and evidence): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s321/b2034/` (`jira_get.py`, `texts.py`, `kit_skel.md`, `build_kit.py`, `sidecar.py`, `cards/`, `get/jira.json`, `kam_msgs_20.txt`, `dry/`).

## BLUF
- The kit is shaped on B2030 (R310) and adds three new Jira verbs. Each verb has its own fence and idempotency read:
  - **T-R:** one reference issue, plus four multipart uploads (T-U1 to T-U4) to it.
  - **T-A1 to T-A6:** six action issues, each assigned to Kam.
  - **T-C1 to T-C4:** four transitions to Done, on OXPD2-33, OXPD2-39, OXPD2-41 and OXPD2-47 only, with transition id 41 and no comment. These come from Tuesday's ADDENDUM and Kam's 11:31 tap, option c.
- **Records:**
  - C-82: Kam's messages from 11:10 to 11:30, his three OXPd taps, and the documents-map lines for the four tickets.
  - Owed items 113 (OneDrive "Shared with me" leaves the design) and 114 (`CLAUDE.md:58-62` and Azure).
  - One history entry, which includes the B2031 Azure boundary proof, relayed from its FOR RECORDS section.
- **Write order:** C-82, then T-R, then the uploads, then T-A1 to T-A6, then the closes, then BACKLOG, then history.
- **Commission discrepancy:** the commission dates Kam's message at 11:30:54. The board reader prints `2026-11-24T11:30:40.468`, and the kit uses the board's time.

## Facts re-measured (instrument, clock, control)
- **Clocks:** `date` read 11:32:56 at the start and 11:48:14 at the last Jira GET (the build's summary searches).
- **Board:** `kam_msgs.sh 20` (WED_AGENT=tuesday) printed 20 rows, from 10:26:52 to 11:31:12.
  - The rows since C-81's last line (10:37:19) are 11:10:58, 11:11:44, 11:12:26, 11:18:57, 11:21:51 (owner-login b), 11:28:07 (NexusAI rd1035; not recorded), 11:30:40, 11:30:55 (OneDrive a) and 11:31:12 (four-tickets c).
- **Store:** `decision_queue.sh show <exact id>` for 11 cards (ka1 to ka5, kd1 to kd3, onedrive, owner-login, docs-answer), each into its own file.
  - The four-tickets card reads `ruling: choice='c' ruled_ts=2026-11-24T11:33:15.656593+11:00`. Its option c is "Close the four", detail "Mark them answered by our documents; no message beyond Jira's own."
  - In `texts.tap()`, each tap's board line equals `Decision <id>: <key> — <label>` built from the store print (an assert, 3 of 3).
- **Jira (GET only):** read through `b1785.py`, loaded in place with importlib. The transport refuses any method but GET.
  - **Kam's account:** `myself` is 616503d4bfa2c1006b1971d1, Kamil Kreiser. **The project's Jira login is Kam's own account.** OXPD2-26's reporter and creator are the same id.
  - **Assignable search:** `kamil` and `kreiser` each return that one row; the control `zzqxnonexist` returns 0. He is also the project lead.
  - **Attachments:** `attachment/meta` reads enabled true, uploadLimit 1073741824. The largest file is 2808081 bytes. `attachments IS NOT EMPTY` returns 0 issues.
  - **The four to close:** each reads Backlog (10052), assignee 626881c70f0cc0006f8ee5c9, 1 link, 0 comments, resolution null. Their transitions are 11, 21, 31 and 41. Transition 41 goes to 10022 Done, with hasScreen false and isConditional false. `statusCategory = Done` returns 0 issues in the project.
  - **Searches:** the census returns 54 (OXPD2-1 to OXPD2-54); `oxpd-workpath-question` 29; control `no-hardware` 23; `oxpd-kamil-action` 0; `oxpd-reference-docs` 0.
  - **Summary phrases:** each of the 7 summary searches returns 0 hits at 11:48:14. The control `MASTER: questions...` returns OXPD2-1.
- **Design files** (`ls -lT`, `shasum -a 256`, `os.stat`):
  - 02 docx and pdf were saved at 08:38:52; 02 md at 08:38:44.
  - 03 docx was saved at 10:28:56 and 03 pdf at 10:28:57; 03 md at 10:28:56.
  - So D-1 (a version pair is consistent) holds. Sizes and hashes are in the kit table.
- **Record files:** each equals its line in `.tools/b2030/READY.manifest` (CLARIFICATIONS d8278e2f, BACKLOG 5982bae9, history 07ab7891, register e2621f1b). CLAUDE.md reads 1a2e5629.
  - C headings run 1 to 81, and the owed items 1 to 112. The anchor is at line 817, and history line 3 is the 11:19 entry.
- **Dry builds** (scratch `dry/`):
  - CLARIFICATIONS: 978 to 1038 line feeds (60 added), C-82 at line 980.
  - BACKLOG: 14 lines added; new headings at 816 and 823; owed 1 to 114 with no gap; removing the added lines by position gives back the old file.
  - history: 10 lines added.
- **scan_record over every added record line** (prototype fills): 0 problems, and quoted lines show S-NAME only. Controls fired: `_by_kamil_`, a card id, `/TUESDAY/`, an em dash and `<<X>>`.
- **scan_jira codes** (filled texts):
  - T-R: S-NAME.
  - T-A1 to T-A3, T-A5, T-A6: S-DQUOTE, S-NAME.
  - T-A4: plus S-WORD:lane (his "swim lane").
  - ADF round trip: 7 of 7 equal; the mutant control is unequal.
- **K1:** all 26 texts re-parsed from the written kit equal their built text and their FROZEN TABLE row.
- **H-AZURE fragments:** each of 8 is in B2031's FOR RECORDS section; the control `zzqx` reads 0.

## D-decisions (the drafter's, each in the kit)
- **D1 (his six actions):** KA-1 to KA-4, plus C-77 (the admin password) and C-76 (the test tenant user).
  - Both C entries say the item is his, and no later entry closes either. C-77 is his note "I will need to find it tomorrow". C-76's detail reads "Needs a test tenant user from you". KAMIL-ACTIONS:150 also lists both as open.
  - Left out: KA-5, which went to Steve as OXPD2-52 to OXPD2-54, and KD-1 to KD-3, which are Tuesday's.
- **D2 (ticket text):**
  - The rulings are quoted from his board line ("a, <label>; note"), not from the option details, because the details of ka1 and ka2 name "Tuesday".
  - The NAS path in his ka4 note is not quoted, because it holds "Friday" (S-NAME). The ticket points to C-81 instead.
  - A5 and A6 say "Until then:" rather than "the default the card set", because no card default exists for them.
- **D3 (labels):** `oxpd-reference-docs` for T-R and `oxpd-kamil-action` for the actions. The history names the actions label only as "the project's one label for his actions", because the label holds "kamil" (S-NAME in records).
- **D4 (uploads):**
  - Each file is staged with `cp -n -p`. Its hash is named in the description.
  - D-3 re-checks the live file before T-R and before each upload, because a document pass for the OneDrive change is owed.
  - A `.md` source newer than its Word or PDF is a STOP.
- **D5 (no transport exists):** `b1785.py` has no multipart path (my grep found 0 hits for `multipart`, `/attachments` or `no-check`; the only `.tools` hits were r5_controls.py's `--no-checkout`). The seat builds one transport, and the fence admits it only for `<REF-KEY>/attachments`.
- **D6 (one slot for all of Jira):** a single slot JIRA covers creates, uploads and closes. JIRA HOLD means a dry run only (no record write), because the history names the keys.

## Chain inputs (each produced by an earlier step or at BASE)
| Step | Inputs | From |
|---|---|---|
| 0 | kit, sidecar, record files, CLAUDE.md, register | BASE |
| 1 | b2030.py and b1785.py (read as models) | BASE |
| 2 | sources rows 1-29, the four design files, B2031 STATUS, Jira GETs | BASE |
| 3 | frozen texts, staged copies (`upload/`), live record bytes | kit, Step 2 |
| 4a | C-82 filled | Step 3 |
| 4b-4c | `<<FILE-n>>`, staged copies, T-R key | Step 2 and the 4b write log |
| 4d-4e | write log, P-8 snapshot | 4b, Step 2 |
| 4f-4g | owed numbers, write-log keys | live BACKLOG, 4b-4e |

## Q-questions for Tuesday (each has a default; the kit's Q1 to Q9 carry the same)
- **Q1 (slot JIRA):** WRITE all 15 POSTs now. Default WRITE.
- **Q2:** T-R is assigned to Kam and labelled `oxpd-reference-docs`. Default as tabled.
- **Q3:** R-D promises that later versions are attached with a "latest" comment and that old attachments stay. Default as frozen.
- **Q4 (slot DUE):** T-A1 to T-A5 are due 2026-11-24, from "now", "today", "tonight" and the "tomorrow" he wrote on 11-23. T-A6 and T-R have no due date. Default AS-TABLED.
- **Q5:** T-A2's third edit. The card says "add the OXPd 1.9 files to H7". Kam's 10:27 tap said "1.9 means our 1.x line, No SDK needed", with the note "I will request whether there is anything more recent". The ticket words the edit as "ask whether anything is more recent than 1.9". Default as frozen.
- **Q6:** CLAUDE.md is not edited by this kit (owed item 114). The drafter proposes one exact-string edit for a later pass, which is in the kit. Default: a later pass.
- **Q7:** C-82 quotes his 11:11:44 message whole, which includes his corporate login address. His 11:10:58 message is named without its URL. Default as frozen.
- **Q8:** create T-A4 (videos) and T-A5 (password) even though either may already be done, given his 10:33 folder note, his 08:34 line and his 11:18 line. Default: create, with "if done, say so here".
- **Q9:** the closes carry no comment, per his option c. Default as ruled.
- **Q10 (launch order; report only):** launch R311 now, which attaches the 08:38 and 10:28 versions, rather than after the OneDrive document pass. Default: now. Owed item 113 carries the re-attach.

## UNMEASURED
- The multipart request shape, Jira's answer to it and the attachment read-back. No attachment exists on OXPD2 to model them on.
- The resolution Jira sets on transition 41 (the kit prints it and does not check it).
- Whether Jira notifies Kam about issues his own account creates and assigns to himself.
- Whether any of his six actions is already done (the video folder, the password, H5 and H3 sent).
- Whether 02 or 03 gets a new version before the seat runs. D-1 and D-3 catch it.
- Whether "C-72" holds the no-reset rule word for word. It is relayed from C-77's reading.

## Outside the fences (disclosure)
- **Card reads:** I ran `decision_queue.sh show` for 11 exact Datasec/OXPd ids, each into its own scratch file. I printed those files whole: each holds one card, so the inclusion filter is the id.
- **Board reads:** I ran `kam_msgs.sh` 8 and 20. They print one Datasec/NexusAI tap line (11:28), which is not used.
- **Jira:** I made GETs only, including `/myself` and one read of OXPD2-26's reporter and creator. No POST was made.
- **Design files:** I hashed the four design files and statted the two `.md` files. I did not open any `.md` or `.pre-1124` file.
- **Not read:** the NAS or Friday folder, `Source_Documents/`, `4_Credentials/`, and any WEDNESDAY or FRIDAY tree.
- **Background search:** a background grep of `.tools` and `!CODING/Datasec` for `multipart` timed out and was stopped by me. It was read-only.
- **Writes:** only the kit, its sidecar, this report and the scratch folder. No mail, no Artifact.
