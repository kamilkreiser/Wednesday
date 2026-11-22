STARTABLE: YES (only after seat R294 / kit B1887 ends READY or HANDOVER, and only with Tuesday's answer to the STOP-class Question 1 in slot CREATE)

# B1900 drafter report (Opus, in-session, read-only), 2026-11-22

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1900_SEAT-R296_oxpd2-records-lanes-g-i-and-followup-ticket.md` (91755 bytes, 518 lines, 29 frozen texts, 37 SOURCES rows all hashed, 64 REVIEW MAP rows). Sidecar: the same name plus `.measured` (58 of 58 claims; `stamp_check.py <kit>` exits 0, output in `fleet/state/s309/d1900/stamp_check.out`). Scratch and programs: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s309/d1900/` (`tools/build.py` assembles the kit and runs the checks; `tools/sidecar.py`; `tools/jget.py` Jira GET only; `build_report.json`; `filled_proto.json`; `dry/`). Reads ran 17:21:23 to 17:38 AEDT (clocks by `date`).

## BLUF
- A NEW records kit for seat `Datasec/OXPd2-R296`, level opus. It writes: four clarification entries (J: the job service card, board 09:35:13; K: the CI guards round-2 card, 13:53:03; L: the round-3 card, 14:57:38; M: his message of 16:53:30), ONE Jira Task (the lane I follow-up ticket), three BACKLOG owed items (G: lane G after landing; I1: lane I records; I2: the two shapes, carrying the ticket key), and ONE history entry. It writes no provenance row, no comment, no ticket move.
- **Lane I is recorded as landed on his ruling over two NO GO verdicts (B1893, B1894 at a9dc8cd)**, in H-PR16, CLAR-L and BL-I1. Nowhere does it say "gated GO". Lane G is recorded as GO WITH FINDINGS by both round-3 readers at edaa1b7, the head that merged.
- **Sequencing.** Every number is computed by program at the seat's run. The PRIOR WORK P-1 to P-6 refuses to start until B1887 has ended. It finds B1887's added lines by diffing against B1887's own `.tools/b1887/before/` copies (those now exist: 5 files, made 17:31). It allows B1887 only to name the landings of 15 and 16 and the W02 cell, never their reviews. It points at B1887's W02 owed item by number instead of duplicating it (P-5; TEXT W02-REF or W02-NONE).
- **R294 WAS RUNNING WHILE THIS KIT WAS DRAFTED.** At 17:36 the pane `Datasec/OXPd2-R294` existed, and B1887's STATUS last line read `WORKING: Step 0, 17:31` (still the same at 17:38:00). At 17:27 the B1887 kit file had already been amended (192193 bytes, and 195543 at my hash). So R294 launched on B1899's amended kit or during the amendment. You know which; I did not check.

## Corrections to the commission (each measured)
- **D1. `2026-11-21_B1838-B1839_GATE_COMMISSION.md` is NOT lane G.** Its first line names "WP1.5: the session and token broker (kit B1831, seat X18) at head 70c1fad" (pull request 9). Lane G's rounds are B1859/B1860 (round 1: NO GO / GO WITH FINDINGS at 5dd0f85), B1866/B1867 (round 2: NO GO / GO at 8efae98) and B1888/B1889 (round 3: GO WITH FINDINGS by both at edaa1b7). The B1838 commission is in SOURCES as row 6, labelled NOT lane G, and no text uses it.
- **D2. Build seats X23 and X26 added NO entry to `history.md`.** The file is unchanged since B1887's drafting (sha256 2ba100ca..., 139 line feeds). Counts of lines holding `job service`, `WP1.7`, `b1841`, `edaa1b7`, `CI guard`, `R6`, `b1861`, `a9dc8cd`, `pull request 15`, `pull request 16`, `e1e8043d` and `185b9eef` are all 0 (control `WP0.3`: 8). The six STATUS files of B1841, B1862, B1872, B1861, B1882 and B1892 each hold 0 lines with `history`. So the history entry carries the landings and the review rounds itself (H-PR15, H-PR16). It does not "record only what those entries do not say".
- **D3. The only FOR-RECORDS files of lanes G and I are the four named:** B1888, B1879, B1890 and B1893. B1859 and B1866 have none; their surviving findings reach BL-G through B1888's items 4 and 5. B1838's FOR-RECORDS belongs to the broker lane. B1889's finding F1 is relayed from its VERDICT.
- **D4. PR 15 squash = `e1e8043d890185b66e83797490f13af3f10546f8`**, 1 parent ca94ed96, 33 files. PR 16 = `185b9eef...`, 1 parent e1e8043d, 9 files (GET). Both card prints' `delivered_artefact` lines agree. The ruling stamps are store prints: J 09:36:15.280438, K 13:53:27.382739, L 14:58:00.302349. The board stamps (09:35:13, 13:53:03, 14:57:38, 16:53:30) are the reader's.

## Facts re-measured (instrument, control)
- GitHub (`gh api -X GET`, project GH_CONFIG_DIR, 17:21:57 to 17:22:00): 16 pull requests, 16 merged, 0 open; `pulls/99999` rc 1 (404). Refs: 17. Main is 185b9eef. b1841 is at edaa1b70 and b1861 at a9dc8cd9. PR 15 head edaa1b70, merged 2026-11-21T23:59:23Z. PR 16 head a9dc8cd9, merged 2026-11-22T04:08:36Z. Both titles pass `scan_record` with 0 problems (planted card id: S-CARD). `ReceiverTests.cs` at 185b9eef: `W02_a_body_whose_read_throws` 0, control `W02_a_wipe_during` 1. This was a probe only; BL-18 belongs to B1887/B1899.
- Jira (GET, project helper's transport by importlib, 17:22:51 to 17:24:24):
  - The census reads 24 issues, 0 Done. OXPD2-1 reads 200 with 7 comments; OXPD2-99999 reads 404.
  - OXPD2-3 is an Epic (id 10000). OXPD2-20 to OXPD2-24 are each a Task (10030) with parent OXPD2-3, status Backlog and labels b1785, no-hardware, wp0-3.
  - The marker `REC-NEW-R6QUOTE-22NOV` finds 0 keys. Controls: `REC-NEW-RULES-20NOV` finds OXPD2-23; `zzqxnonexist` finds none.
  - Phrase searches are listed in the kit. `known limit` finds OXPD2-1; `flow mapping` and `quoted key` find OXPD2-23; `labels = b1785` finds 5 keys.
- Cards: `decision_queue.sh show` on the three exact ids returned rc 0 each, and each id appears once in its print. Board: `kam_msgs.sh 40` returned rc 0 at 17:21:36. For each of the four lines, `chars=` equals the text's own length (97, 101, 104, 88). Each tap holds one U+2014. M holds no byte above 126 and one run of two blanks.
- Scanner: a byte-equal copy of `b1785.py` (sha256 5e766b28..., `cmp` rc 0), loaded by importlib and never run.
  - `scan_jira` over the summary and 7 paragraphs: 0 problems.
  - `scan_record` over 71 filled non-quotation record lines: 0 problems.
  - Controls fired: planted name token gave S-NAME; planted card id gave S-CARD; planted double quote gave S-DQUOTE.
- Quoted-words check: CLAR-M has 2 strings, 0 outside its quotation lines; J, K and L have 0. Bytes above 126 outside quotation lines: 0 in every entry.
- Prior work on the live files at 17:34:49, before B1887 wrote anything: every P-3 and P-4 probe reads 0. Controls: `One more one-line round, then merge` 1 line in CLARIFICATIONS; `OXPD2-23` 1 line in BACKLOG; `pull request 1` 3 lines in history. P-6 mapping: OXPD2-20 to 24 are owed items 19 to 23, each once. Highest live owed number is 30, counted with `[[ x]]`; three items are ticked, so an open-only count would give 27. Highest heading is C-57.
- Dry build on scratch copies, before B1887 (PREDICTED for the seat):
  - CLARIFICATIONS 444 → 500 line feeds.
  - history 139 → 149.
  - BACKLOG 215 → 236.
- Read load (PREDICTED, by program): about 158106 bytes, of which the kit is 91755 and the sidecar 8004.
- Model: `models_latest.json` line 17 gives `claude-opus-5-5`. Routing row C8 (line 98) says Sonnet first. Project `CLAUDE.md` line 7 says the newest Opus, so the launch level is opus. Row C7 (line 97) covers the byte-for-byte approved body.

## Questions for Tuesday (each with a default)
1. **STOP-class: the authority to create the ticket.** His card L label: "Merge now, the two shapes ticketed as known limits". Its detail: "the two missed shapes are written down as named limits with a follow-up ticket".
   - The project `CLAUDE.md` neither grants nor refuses a records seat a create. Line 66 sets the form: "Tickets in BLUF form on `OXPD2`; each cites the work package (WP number) and the requirement row (F number) it serves". Lines 12 to 13 route QUESTIONS to OXPD2-1 "through Tuesday, never sent to a person".
   - I read this as silent, not forbidding. B1887's drafter read it as "no right to file one".
   - Precedent: the records kit B1785 (seat R286) created OXPD2-20 to OXPD2-24 under its own kit.
   - **Default (yours): CREATE YES.** The kit creates exactly this one ticket, which cites the ruling. CREATE NO leaves BL-I2 with `Jira: none` and the history line "nothing written to Jira by this pass".
2. **The ticket's form:** Task 10030, parent OXPD2-3, labels `b1900`, `no-hardware`, `wp0-3`, summary `[WP0.3] ...`, seven paragraphs in OXPD2-23's form (BLUF; the shapes; parser-dependence and backstop; fix sketches; carried items; Rows; Source with searches and marker). `b1900` follows B1785's practice of labelling with the kit's B-number. Default: as frozen.
3. **The ticket text is re-worded from B1893's THE FOLLOW-UP TICKET** so that `scan_jira` passes. These are all the changes:
   - Every double quotation mark and backtick is removed. The two code shapes (`a${{: "b }}`, `k "x: "a`) are described in words.
   - `yaml_scan`, `R6_EXPRESSION` and `REVIEWED_WORKFLOW` are kept bare.
   - The B-numbered carried items are named by content: "B1890 F2 / H39" becomes "a block start read after the expression removal ... invalid YAML", and "B1891 m9, m10, B1894 m11" becomes the mutants and formats by name.
   - "readers" becomes "reviews", because `lane`, `gate`, `seat` and `brief` are banned words.
   - BLUF, Rows and Source paragraphs are added. The F row reads "No F row is named for this package (pipeline infrastructure, work package WP0.3)", as on OXPD2-23.
   - Default: approve byte for byte through slot CREATE.
4. **Entry M (his 16:53:30 message).** Default: WRITE (slot M-ENTRY). It records his words and the reading that nothing touches the printer before his word on what to run.
5. **Not filed by this kit** (the reviews ask for them; they would edit existing lines or move tickets): marking owed items 19 to 23 with the landing; moving OXPD2-20 to OXPD2-24; `SETUP_RUNBOOK.md` item 4 naming `build/squash_scan.py`. BL-I1 records each as open. Default: a later pass with its own authority.
6. **P-4's allowance is a bounded judgement.** A B1887-added line may name the existence, title, merge or main of PR 15 or 16, or the W02 cell. Anything more is a STOP. I drafted it because B1899's amended B1887 BL-18 already says "landed as pull request 15 on 2026-11-22 without this cell" (kit line 895 at 17:27). Default: accept.

## UNMEASURED
- Everything B1887 will have written: the C-numbers, owed numbers, W02 owed number and OXPD2-1 comment ids the seat will meet. The kit computes them by program.
- GitHub's parser on the two shapes (the reviewers' UNMEASURED).
- The poster, the read-back, the census diff, HOLD R and HOLD R2 on live files, and P-2 and P-5 on B1887's real output. The kit lists all of these as never run on a real output.
- The seat's real read load.

## Chain inputs (each step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the stamped kit, sidecar, panes, df, clock | BASE |
| 1 | `b1785.py` (copy); B1887's helper (read only) | BASE (B1887 ended) |
| 2 | SOURCES files; GitHub; Jira; B1887 STATUS and `.tools/b1887/before/`; live record files | BASE |
| 3 | the frozen texts; card fills (in the kit); Step-2 facts | the kit, Step 2 |
| 4 | Step-3 filled CLAR texts; C-numbers from the live register | Step 3 |
| 5 | Step-3 ticket texts; marker and phrase results; `snap_before.json` | Steps 2, 3 |
| 6 | C-numbers (Step 4); the ticket key (Step 5); origin re-read; owed numbers | Steps 4, 5, 6 |
| 7 | all of the above | Steps 0 to 6 |

## Outside-the-fences disclosure
- **Writes:** only the kit, its sidecar, this report, and scratch under `fleet/state/s309/d1900/`. Three earlier sidecar skeletons of mine were moved to `d1900/_quarantine/` (`mv`, nothing deleted).
- **Reads:**
  - The project's `CLAUDE.md` and the three record files. The PROVENANCE file (the one `Source_Documents/` file excepted) was hashed and line-counted once, and counted for the overlap probes; it is not a SOURCES row, because this kit does not write it.
  - The STATUS files of B1841, B1862, B1872, B1861, B1882 and B1892: a count of `history` lines and their last lines only.
  - B1887's STATUS (last lines) and a listing of `.tools/b1887/` and `.tools/`.
  - `b1785.py`, copied by `cat` redirection into scratch.
  - Jira GET, `gh api -X GET`, `decision_queue.sh show` on three exact ids, and `tmux list-panes`.
  - The B1887 kit, its report and the B1899 commission. The gate commissions' heads, and the twelve VERDICT and four FOR-RECORDS files.
- **One fence to note:** `kam_msgs.sh 40` reads the live board, a hosted dashboard. DRAFTER_RULES fence 4 refuses HTTP to hosted hosts. The commission named this read explicitly, so it ran once, output to scratch.
- **Never touched:** `Source_Documents/` (beyond the PROVENANCE file path in a probe list), the NAS, `decision_queue.sh list`, `fleet/briefs_staged/`, any other client or project, B1898's or B1899's files. No `cd`. No write in any project file, Jira or GitHub.
