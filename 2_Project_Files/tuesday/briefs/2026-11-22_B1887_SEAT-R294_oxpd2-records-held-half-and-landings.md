From Tuesday (the Datasec coordinator seat), Datasec / OXPd 2. **Your STATUS file is the channel and the wrap** (no mail, whatever a launch line says). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Files naming another B-number are READABLE claims only. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has. **MEASURED-BY-DRAFTER** = printed by the drafter's instrument at drafting (Sun 22 Nov 2026, 10:20 to Sun 22 Nov 2026 10:41:17 AEDT AEDT by `date`; the Jira reads, the GitHub reads and the card prints ran in that window); you re-measure every one before you use it. The drafter's proof of each literal is in the sidecar beside this kit (same name plus `.measured`; never yours to edit). **The form is the first records kit of this series, B1816, whose partial run is recorded in `1_Project_Definition/Briefs/2026-11-20_B1816_STATUS.md`; this kit is a NEW kit, not an amendment, and it is self-contained: you do not read B1816.** `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/CLAUDE.md` wins wherever this kit and it differ. Read whole means every line printed: a file read in parts or with long lines cut is NOT read whole, and STATUS says which it was. **A Read refusal on a long file is a page-size message, not a stop: answer it with `offset` and `limit` and read every page.**

**LAUNCH ONLY WHILE no other pane runs a kit that writes Jira OXPD2, `CLARIFICATIONS.md`, `BACKLOG.md` or the provenance file.** Build seats and in-session gate readers of the lanes still open (lane G, lane I) run while you run; each adds ONE entry to `5_Project_History/history.md` at its end (HOLD R2). At drafting `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` printed three panes, `%0 tuesday` and two unnamed (MEASURED-BY-DRAFTER, 10:37 AEDT): none holds OXPd.

# BRIEF B1887 | SEAT-R294 (records): OXPd 2. **Records and Jira only, no code: write the held half of the records kit B1816, re-derived against the design documents as they are now (entries A, B, S and V; the four comments G1 to G4; the history entry, the owed items and the provenance rows), plus his two rulings of 2026-11-22 (entries X and Y), one note (entry W), and the landing records of pull requests 3 to 14 with the reviews of lanes SL, B, E and T.** MODEL SONNET (the commission's level; see Question 1 of the drafter's report: the project's `CLAUDE.md` line 7 says the newest Opus). NO CODE BYTE, NO WRITE IN THE CODE REPOSITORY (no git verb there), NO DESIGN DOCUMENT EDITED, NO LINE OF `CLAUDE.md` EDITED, NO TICKET CREATED OR MOVED, NO FILE UNDER `Source_Documents/` OPENED BUT ITS PROVENANCE FILE, NOTHING TO HP OR TO ANY PERSON.

**BLUF.** (1) **What is already written** (by the partial run of B1816, 2026-11-21 23:41 AEDT, STATUS of that run): entries C-55 (the logging ruling), C-56 (his words of 2026-11-21) and C-57 (five lines of 2026-11-20), and lines 7, 51 and 86 of the project `CLAUDE.md`. You write none of them again: Step 2 probes find them and the kit's `<<C-R>>`, `<<C-T>>`, `<<C-U>>` are their numbers. (2) **Why the rest was held, and what changed.** The three design documents `02`, `03`, `05` were revised on 2026-11-21 (08:34 to 08:37) after B1816 was drafted. They now CARRY his answers, each change marked B1817 with its row id; B1816's entry A said a correction pass was owed and its owed item BL-1 said no answer was written into them: both are no longer true. **Entry A is re-derived** (TEXT CLAR-A-READ says where each answer now stands); **BL-1 is retired**; the open questions the revision wrote are owed item BL-9. B1816's BL-2, BL-3, BL-4, BL-8, BL-9, comment G4, entries S and V and the history lines are re-derived or patched, each change named in the drafter's report. (3) **New here:** entry X (his ruling of 2026-11-22 09:36 on the SQL Server driver's sign-in packages), entry Y (his ruling of 2026-11-22 10:35:55 on tolerant device answers, with his note), entry W (a note that two forward references of C-56 are met), the quotation line that gives entry V's tenth string its source (the coordinator's own answer of 2026-11-21 21:07:43, never his), owed items BL-13 to BL-19 (lanes SL, B, E, T and two follow-ups) and the history lines of the landings. (4) **Who decided.** Only words between quotation marks are the product owner's. Every reading, grouping and record line is the coordinator's; the follow-up questions FQ are a reader's proposals, posted only as slot FQ names them. (5) **The design documents, the reports and the rules are NOT edited.** (6) The record files are not in a git repository: each is rewritten once, whole, by HOLD R. (7) Origin at drafting (GET, 10:20 AEDT): main `ca94ed966ff476d31e2d35cb1ae0cc5c5d4b39b5`; 14 pull requests, all merged, 0 open; open lane branches `b1841/wp17-scan-and-print-jobs` (lane G, at edaa1b70, a merge of main) and `b1861/wp03-ci-guard-follow-ups`. Jira at drafting: 24 issues, 0 Done, OXPD2-1 holds 7 comments (newest id 41419).

**Launch (Tuesday), level inside the quotes:** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/OXPd2-R294 "BRIEF_SEAT_LEVEL=sonnet bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2' '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1887_SEAT-R294_oxpd2-records-held-half-and-landings.md'"`. Model row C8 of `fleet/specs/model-routing.md` (line 98, brief drafting; the commission's level); model id `claude-sonnet-5-5` (`models_latest.json` line 23). No listener, no port. **Toolchain:** no build, no test; `python3` is what `command -v python3` prints (the drafter's printed `/opt/homebrew/bin/python3`, Python 3.14.10); every helper runs as `python3 -I -B`. No dotnet, no docker.

**Context band and handover.** At about 70% context start no new step; at about 75% stop at a safe boundary (files whole, no write half-done, no process left) and write `1_Project_Definition/Briefs/2026-11-22_B1887_HANDOVER.md` (done / in hand / next / processes left / decisions a successor keeps: every C-number written, every comment id, which files are replaced), last line `HANDOVER B1887: next <step> | done <steps>`, and make that the STATUS last line too. **A successor never re-posts and never re-writes:** it runs every marker search first and greps each record file for the heading or line it would add. **Cut line:** entries first, then Jira in the order G1, G2, G3, G4, then the records.

## WHERE THIS KIT DIFFERS FROM B1816, AND WHAT IS FOLDED IN
- **Folded in from the partial run's Deviations and Corrections:** (a) THE SOURCES rows of the three design documents are HASHED AT DRAFTING in this kit (rows 5 to 7) and the seat re-hashes them at Step 0: a difference holds entry A and every text that fills `<<C-A>>`; (b) the table SOURCES READ WHOLE is printed by program before the first write; (c) every pointer into a design document was re-printed at its line by the drafter and a row that no longer holds its fragment holds the texts named in its last column; (d) a fragment of a pointer row that matches on more than one line is read at the line the row names, never by search (B1816's re-derivation by fragment landed one row on the wrong decision: `D1` is now at `02:900`, and `02:920` is decision D21).
- **No ticket is created or moved.** The project's `CLAUDE.md` gives a records pass no right to file one; the only Jira writes are comments on OXPD2-1.
- **The tree counts** of the new source folders (provenance rows) are measured by YOU (`os.walk`, regular files, `lstat`; no listing printed). The drafter measured none (the commission forbids touching `Source_Documents/`); the figures of B1816's partial run, RELAYED, were: cc-api-main 158, CypherKey-cypherkey 413, the SDK folder 1514 files and 805564065 bytes, the library folder 31481 files and 6277940515 bytes, control hpam-api-main 18 (its provenance row says 18).
- **`.tools/b1816/` exists** (the partial run's helper, its facts and dry files): you may READ it and COPY the helper (`cp -n` into `.tools/b1887/`, never edit the original, never run it in place) as a model; its tables are bound to B1816's texts, so the copy must be adapted to THIS kit's texts, fills and tables and pass its own selftest before any write.

## READ FIRST (read-only) AND THE LOAD
Whole, with the Read tool, BEFORE the first write: this kit and its sidecar; the extract (row 1); the project's PROVENANCE file; the newest comment of OXPD2-1 (the form of a comment) by GET, rendered to a text file under your scratch. **By line range, each range read whole:** `CLARIFICATIONS.md` lines 370 to 444 (entries C-55 to C-57) and the last lines of the file; `BACKLOG.md` lines 1 to 6 and 185 to 215; `5_Project_History/history.md` lines 1 to 14. **By program (print the line cut at 400 characters, read it):** every row of THE DESIGN POINTERS. **CHECKED BY PROGRAM, printed cut at 160 characters, not read for content (the drafter read them; the check is the fragment at the line):** THE REVIEW MAP, MAP 2, MAP 3, THE REPORT POINTERS, THE CLARIFICATION POINTERS, THE QUOTE MAP. **HASH ONLY** (the sha256 of THE SOURCES is checked; the drafter read them): `CLAUDE.md` (print its lines 7, 51 and 86 and its line count), the four FOR-RECORDS files and the eight VERDICT files of rows 22 to 33, the answers record, the B1816 STATUS, the project helper, the chat store. **The load**, summed by the drafter's program from the actual files: files read whole and ranges 22465 bytes; design pointer lines cut at 400 about 53093 bytes including the 160-character rows and a 6000-byte allowance; this kit 187500 bytes and its sidecar and the Jira comment estimated at 24000; total about 287058 bytes against the 300000 a Sonnet seat reads. This is a PREDICTION, not a measure: if your own sum of what you printed passes 300000, say so in STATUS and split the READ.

## BINDING HOLD
You write nothing in the CODE repository (`<project>/2_Project_Files`, origin `datasecau/OXPd_2`): **no git verb there**; the origin is read by `gh api -X GET` under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/4_Credentials/.gh-config'` (`gh auth status` first, no account name printed). **`gh` is `-X GET` only.** You write: (1) Jira OXPD2 through THE JIRA CLOSED LIST; (2) four record files in the project folder, each once, by HOLD R: `1_Project_Definition/CLARIFICATIONS.md` (append), `5_Project_History/history.md` (one entry inserted), `BACKLOG.md` (owed items inserted), `1_Project_Definition/Source_Documents/2026-11-20_from-product-owner/PROVENANCE.md` (rows and paragraphs); (3) files under `<project>/.tools/b1887/`, your STATUS and your Step-0 copies. You never write `CLAUDE.md`, `SETUP_RUNBOOK.md`, `Launch_Claude.command`, anything under `Design/`, `Analysis/`, `Review/` or `Registers/`, any other file under `Source_Documents/`, `3_Access_Keys/`, `4_Credentials/`, any other project, the NAS, or the reviews' folders in the coordinator's tree. **Nothing of the HPSM project is opened.** No `az`, docker, ssh, mail, no `decision_queue.sh`. **Every `decide`, `ask`, `send`, `correct`, `apply`, `file` or `land` the texts name is later work, never yours.** Never delete (quarantine to `.tools/b1887/_quarantine/` with `mv`); no `rm`; no `sed -i`; **never type `cd`**. Of `Source_Documents/` you open its PROVENANCE file only; every other path is counted, never opened, never listed by name (a folder under it holds a file whose NAME is a secret: print no directory listing).

## WHO DECIDED
- **The product owner's:** the words of entries A and B (cut from the extract; frozen from the board); the seven quotation lines of entry S; the board lines and card lines of entry V; the card print and board line of entry X; the board line, his note and the card print of entry Y; and nothing else. His note of entry Y is printed whole in the entry with his typing kept (`can me changed`): never correct it.
- **The coordinator's, written as such:** every reading in every entry; the wording of the note W; the choice of which follow-ups are posted (slot FQ); the shortening of G4; every record line; the model and the departure of lane E from the plan (a coordinator's decision, never his); everything in the owed items that begins with a reader's grading.
- **A reader's proposals, written as proposed:** FQ-9, FQ-11, FQ-13, FQ-16; the corrections of reports A12 and B4.
- **The coordinator's own answer of 2026-11-21 21:07:43** (the last quotation line of entry V) is the coordinator's and is labelled so; the sentence "an unknown value never counts as success" is the coordinator's addition, never his.

## THE SOURCES (hashed by the drafter at drafting, MEASURED-BY-DRAFTER by `hashlib`; **every row of this table was hashed, the design documents included**: B1816's stamp did not hash them and 28 of its 29 pointers then failed)
| # | What | Path | sha256 | Line feeds | Bytes | Last non-empty line starts | Read by the seat |
|---|---|---|---|---|---|---|---|
| 1 | extract of his notes | `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-20_kam-oxpd-questions-notes/kam_notes_verbatim_2026-11-20_2104.txt` | fb963a54b548ec70980aca9b583ab13718c17b47c0fadd6b7edb8ed092324957 | 35 | 4122 | `Recreate the document starting with list` | WHOLE |
| 2 | CLARIFICATIONS.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/CLARIFICATIONS.md` | 763a76e5cd7cee7079fc91b0b0a0bab5c149621ff42f0996fe259acac34d91c8 | 444 | 43605 | `Messages 4 and 5 (18:47:35 and 18:47:55)` | RANGE 370-444 (C-55 to C-57) and the CP rows |
| 3 | project CLAUDE.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/CLAUDE.md` | 1a2e5629c0e7b69510f0a42fd20c5a95c3693e988361e8496dfe65ca93d9d5c0 | 89 | 10721 | `- **Analysis folder.** Reports A9 and A1` | HASH ONLY (lines 7, 51, 86 printed) |
| 4 | PROVENANCE.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Source_Documents/2026-11-20_from-product-owner/PROVENANCE.md` | d38adef19906b274bfb9cc7db87581daf182a55abec0290c9c8232268392b6b6 | 16 | 955 | `Secrets: these trees hold keystores, a l` | WHOLE |
| 5 | 02_architecture.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/02_architecture.md` | de71e0377a67e3db96e99c0a892c8662a0227d6b1c9c20bdb146d578c44c1a95 | 1276 | 311204 | `**Still owed after this pass**: the prod` | POINTERS |
| 6 | 03_plan-of-attack-and-build.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/03_plan-of-attack-and-build.md` | 523a3a3a92dff980ed05dfa5e171ad291869d8177b1ee19ecd3fe71f42fcb25f | 667 | 177325 | `**Still owed after this pass**: the prod` | POINTERS |
| 7 | 05_readiness-to-build.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Design/05_readiness-to-build.md` | 74036ee2bcdf522957c325755b0f9ad1a1e7246a39b55bc758ed24fded5dd49f | 304 | 62932 | `Details: one row per review finding in `` | POINTERS |
| 8 | B1812 answers record | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Review/B1812_Q_FOR-RECORDS_2026-11-20.md` | 0ab25685e9a3576cd8c8907240e7d319ea440afa8891d06bec9705067d53c715 | 223 | 34404 | `- The library on the NAS was not searche` | HASH ONLY |
| 9 | B1817 change list | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Review/B1817_DESIGN-CHANGE-LIST_2026-11-20.md` | a67e6083b65ab3ad8715e94c755859b83e7930bc8e4380f37fc0a18572e49109 | 377 | 69063 | `STATE: COMPLETE` | POINTERS |
| 10 | report A8 | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Analysis/A8_sharepoint-app-and-common-library.md` | 871f41000b4aa5c78dd8857a322b3ee7b8f5cbc5c4001464d655a8d499d58a7b | 326 | 53886 | `- **Git history** of neither tree was av` | POINTERS |
| 11 | report A12 | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Analysis/A12_phone-app-and-legacy-keycloak-api-source.md` | 2a99a367ade3bc29e19d48786babab6ed39069bc3e988c9fbfae9c5ed56a4003 | 176 | 33141 | `- The fifteen earlier reports were searc` | POINTERS |
| 12 | report B4 | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Analysis/B4_oxpd2-sdk-beta10-nas-folder.md` | 8ff2caa88888cb39d063b2d5afbb419936645b125c515c1a95fa21490e0379e9 | 179 | 26324 | `- The count of "distinct SDK file names ` | POINTERS |
| 13 | report D2 | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Analysis/D2_current-solution-deployment-second-review.md` | 8c10e633b4915822c7c8503099aaeb74bbad99e856a5bd24bea462984c5794f2 | 332 | 48859 | `- One file name in `UniversalPrint-main/` | POINTERS |
| 14 | BACKLOG.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/BACKLOG.md` | 8edb689cd0d4bd81c8d491d2891ee2b9df819240eda998af79906a9d852cacda | 215 | 26514 | `/ WP6.7 Deviation register / `OXPD2-19` ` | RANGES 1-6, 185-215 |
| 15 | history.md | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/5_Project_History/history.md` | 2ba100ca6c477932a72272063e0ad6ce8063c7bb28e7de3c241235fab4f611cc | 139 | 37590 | `- On the product owner's word to start t` | RANGE 1-14 (differs from B1816 by design) |
| 16 | B1816 STATUS | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Briefs/2026-11-20_B1816_STATUS.md` | 98ceddad6f344be67d101733509cf855af9078c821628817ddc91d34e74d3510 | 186 | 20844 | `READY B1816: fe0b2d288f91b631cdcdd311303` | HASH ONLY |
| 17 | project helper b1785.py | `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/.tools/b1785/b1785.py` | 5e766b28f9b90f8f02b371e0acadee39b9f0cafd5e94a9e8d51924f1e868a078 | 1084 | 54539 | `        sys.exit(3)` | HASH ONLY (copied) |
| 18 | coordinator chat store | `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/chat_tuesday.json` | ca38691020b40b59f3116611c53e2302b59e37591ad51ad5dab8eec8701a704f | 11803 | 1367833 | `]` | HASH ONLY (row 2026-11-21T21:07:43.940908 printed) |
| 19 | card print 1 (driver packages) | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1887/card_show.txt` | 6933e45e608b6cac8eb22d51b5c719c4af17051b82fad54195724e562e151db8 | 13 | 1985 | `ruling:  choice='a'  ruled_ts=2026-11-22` | PASTED IN THE KIT |
| 20 | card print 2 (tolerant device answers) | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1887/card_show2.txt` | dd63dfd7a166f77f77e6899af9b0979a9ef89579879475707f2b2a2a1e778e54 | 13 | 1558 | `ruling:  choice='a'  ruled_ts=2026-11-22` | PASTED IN THE KIT |
| 21 | rulings today | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s308/d1887/rulings_today.txt` | 8d8036e01924af017e547ca0be32bfe3eab9394fb299a3eec593c57b30d21e89 | 8 | 973 | `# TAPPED-BUT-OPEN: none (every card he t` | LINE 5 QUOTED |
| 22 | review V1864 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1864_verify/VERDICT.md` | d07e1cbb9c963a1424f68c01072b8b380c853f6ec3ca35233bc09c96d1888ac4 | 201 | 18302 | `- The seat's mBoth, mFalse, mListDrop an` | HASH + RM3 ROWS |
| 23 | review F1864 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1864_verify/FOR-RECORDS.md` | 11776de493eddc6308bf5b1dc8f6b340df1de239ee77e3293b599b093699c03c | 39 | 2605 | `  of paths). No project file is affected` | HASH + RM3 ROWS |
| 24 | review V1865 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1865_verify/VERDICT.md` | 2d36c9c76d70c214960f539243295be4ad742d97b0d332cc27fd28c7e1d3eded | 86 | 15239 | `- A second PROCESS (only two stores in o` | HASH + RM3 ROWS |
| 25 | review V1870 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1870_verify/VERDICT.md` | 7f75a24a71c39bc24d404a2febd18e3002f12490fba68d19ebf4bbe4538c00ef | 180 | 15497 | `the probes above.` | HASH + RM3 ROWS |
| 26 | review F1870 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1870_verify/FOR-RECORDS.md` | 526eb5d749b01d547cd94d1d0d4c3d3752edb22da4193143e36811e8aaed196e | 57 | 4206 | `  committed id is `20261121105111_Initia` | HASH + RM3 ROWS |
| 27 | review V1871 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1871_verify/VERDICT.md` | 727290e6c9d5ad00fed7129955385c4831bb420f166b95f0f2b02cff0cfa4764 | 91 | 18564 | ``fetch.py --list` after my last job: `CA` | HASH + RM3 ROWS |
| 28 | review V1877 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1877_verify/VERDICT.md` | fe73c28f7c542b640b779a9fe75d3d2ae21dcef6d62c359753aa2a61dae497ae | 228 | 20555 | `  races in depth; the builder's 57 cells` | HASH + RM3 ROWS |
| 29 | review F1877 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1877_verify/FOR-RECORDS.md` | de2b0337f2d3794ea08ce9b115b6f0256720dda174a0973139d1537fc307f783 | 53 | 4331 | `  questions, administrator password, cus` | HASH + RM3 ROWS |
| 30 | review V1878 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-21_B1878_verify/VERDICT.md` | 0a9df8cc9417148fff82405d1c027566a9920fc234550e9b03cda705abf6f0b9 | 90 | 13203 | ``GateB1878Probes.cs.txt`, `probes-head-1` | HASH + RM3 ROWS |
| 31 | review V1885 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1885_verify/VERDICT.md` | bdb33d1b24d0d297880d691ff09baa38b08a128716763ca41ea97b91006fcfe0 | 185 | 17980 | `second reader's (B1886).` | HASH + RM3 ROWS |
| 32 | review F1885 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1885_verify/FOR-RECORDS.md` | e090a00dc71ef699f200e56268f977fa3e7802191368df06cf575b7da5f1fb7a | 47 | 4097 | `    in practice (DERIVED from the code; ` | HASH + RM3 ROWS |
| 33 | review V1886 | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1886_verify/VERDICT.md` | a041cfab9db9328e7bdcf4ddaa42d676c8c99705b3dd7b21a110ef662b2f69ba | 79 | 16052 | `The merge and the landing texts (B1885's` | HASH + RM3 ROWS |
33 rows. The extract's line 1 is the coordinator's heading, line 2 is empty, lines 3 to 35 are his 33 paragraphs, line 36 does not exist. **A source whose sha256 differs is read for what it says, and every pointer into it is re-derived at its line before use; a difference in `02`, `03` or `05`, in the extract, in a FOR-RECORDS file or in a VERDICT line a row names HOLDS every text that rests on it.** `CLARIFICATIONS.md` (ends `C-57`), `CLAUDE.md`, `BACKLOG.md` and the provenance file must equal their rows (the partial run's sha256 after-values, RELAYED, are the CLARIFICATIONS and CLAUDE.md rows); `history.md` WILL differ if a build seat has ended since drafting, and that alone is no stop. **Step 2a:** print `SOURCES READ WHOLE` by program into `.tools/b1887/facts/sources-read.txt` before the first write.

## THE POINTER TABLES (line numbers by program at drafting; at your check print each row's line and read it; a row whose line no longer holds its fragment HOLDS every text named in its last column and nothing else; a row is read AT ITS LINE, not by search)
**THE DESIGN POINTERS** (`02`, `03`, `05` are rows 5 to 7 of THE SOURCES; every pointer of the texts CLAR-A-READ, CLAR-S and BL-3 has a row; 49 rows):
| DP | Document | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | 02 | 564 | `more than N seconds after it was read` | BL-3 |
| 2 | 02 | 900 | `Ruled by the product owner 2026-11-20 22:03` | CLAR-A-READ, CLAR-S |
| 3 | 02 | 918 | `Firm as design; not ruled and different from Workpath` | CLAR-A-READ |
| 4 | 02 | 925 | `CHANGED by W2` | CLAR-A-READ |
| 5 | 02 | 932 | `Ruled, C-16; CHANGED` | CLAR-A-READ |
| 6 | 02 | 1132 | `2026-11-21: the product owner's rulings of the evening` | CLAR-A-READ |
| 7 | 02 | 1166 | `B1817 / R2-16` | CLAR-A-READ |
| 8 | 02 | 1192 | `B1817 / R4-28` | CLAR-A-READ |
| 9 | 02 | 1196 | `B1817 / R4-37` | CLAR-A-READ |
| 10 | 02 | 1273 | `| N-16 |` | CLAR-A-READ |
| 11 | 03 | 189 | `six UI languages seeded from the Workpath string resources` | CLAR-A-READ |
| 12 | 03 | 214 | `HPK Deployment Utility amended for OXPd` | CLAR-A-READ |
| 13 | 03 | 594 | `2026-11-21: the product owner's words of the evening` | CLAR-A-READ |
| 14 | 05 | 5 | `Updated again on 2026-11-21 (B1817)` | CLAR-A-READ, CLAR-S |
| 15 | 05 | 27 | `R1-42` | CLAR-S |
| 16 | 05 | 88 | `card emulation and app settings move from the printer panel to the server console` | CLAR-A-READ |
| 17 | 05 | 105 | `8. Is the card key in the library` | CLAR-A-READ |
| 18 | 05 | 106 | `R4-17` | CLAR-A-READ |
| 19 | 05 | 114 | `Default: assumed (a); nothing is built on it before you answer.` | CLAR-A-READ |
| 20 | 05 | 120 | `(a) offer it as Workpath does, risk recorded` | CLAR-A-READ |
| 21 | 05 | 121 | `Recommendation: (b).` | CLAR-A-READ |
| 22 | 05 | 138 | `R4-07` | CLAR-A-READ |
| 23 | 05 | 144 | `Phase 2 we will have a local server` | CLAR-A-READ |
| 24 | 05 | 151 | `None is agreed.` | CLAR-A-READ |
| 25 | 05 | 168 | `Yes, as for Workpath roll-outs today` | CLAR-A-READ |
| 26 | 05 | 170 | `On a branch of its own repository` | CLAR-A-READ |
| 27 | 05 | 171 | `OXPd path only; Workpath jobs behave exactly as today` | CLAR-A-READ |
| 28 | 05 | 172 | `R2-54): answered` | CLAR-A-READ |
| 29 | 05 | 173 | `Both exist: every gateway change ships both ways` | CLAR-A-READ |
| 30 | 05 | 174 | `the gateway package live in the Marketplace today` | CLAR-A-READ |
| 31 | 05 | 175 | `Capture it in the test tenant` | CLAR-A-READ |
| 32 | 05 | 178 | `No: what you sent is the last state` | CLAR-A-READ |
| 33 | 05 | 180 | `Emulator only; nothing is treated as proven on hardware` | CLAR-A-READ |
| 34 | 05 | 186 | `Build all eight languages as the code has them` | CLAR-A-READ |
| 35 | 05 | 188 | `OPEN QUESTIONS ADDED ON 2026-11-21 (B1817)` | CLAR-A-READ |
| 36 | 05 | 196 | `P-1 (B1817 P-1)` | CLAR-S |
| 37 | 05 | 199 | `P-4 (B1817 P-4)` | CLAR-A-READ, CLAR-S |
| 38 | 05 | 201 | `P-6 (B1817 P-6)` | CLAR-A-READ, CLAR-S |
| 39 | 05 | 211 | `N-17 (B1817 R2-55)` | CLAR-A-READ |
| 40 | 05 | 213 | `N-13 (B1817 R4-09)` | CLAR-A-READ |
| 41 | 05 | 214 | `N-14 (B1817 R4-42)` | CLAR-A-READ |
| 42 | 05 | 215 | `N-15 (B1817 R4-44)` | CLAR-A-READ |
| 43 | 05 | 226 | `Windows machine ready.` | CLAR-A-READ |
| 44 | 05 | 228 | `the Workpath product owner holds a lab` | CLAR-A-READ |
| 45 | 05 | 229 | `We will use my access during the dev process` | CLAR-A-READ |
| 46 | 05 | 235 | `A test Microsoft tenant with` | CLAR-A-READ |
| 47 | 05 | 238 | `HP is reached through its portal` | CLAR-A-READ |
| 48 | 05 | 245 | `firmware version does not matter` | CLAR-A-READ |
| 49 | 05 | 267 | `eight for the OneDrive and SharePoint pages` | CLAR-A-READ |

**THE REVIEW MAP** (reviews of 2026-11-20, the first reviews of wave 1; `V` = VERDICT.md and `F` = FOR-RECORDS.md of the folder `2026-11-20_B<number>_verify`, the later folders `2026-11-21_B<number>_verify` or `2026-11-22_...`; a single quote in a fragment may stand for a backtick; rows 11, 16, 23 and 26 to 30 of B1816 are not carried; 32 rows):
| RM | File | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | V1799 | 1 | `GATE B1799: NO GO @ 9f4238a on main 7bf3752` | history: the encoder, its head |
| 2 | V1799 | 22 | `Closing the stream while a read is in flight does not stop that read.` | history: the encoder, one Major |
| 3 | V1799 | 198 | `FOUND: 1 Major (close under a read)` | history: the encoder, one Major |
| 4 | V1799 | 24 | `0x00 and 0x06 to 0x0f refused` | comment G4, RP-6 |
| 5 | V1799 | 27 | `An answer that gives ONE byte and then fails` | comment G4, RP-7 |
| 6 | V1806 | 1 | `GATE B1806: NO GO @ 6499bd1 on main 7bf3752` | history: the decoders, their head |
| 7 | V1806 | 9 | `One Blocker and one Major, both in the assembler` | history: the decoders |
| 8 | V1806 | 10 | `The five routines are exact` | history: the decoders |
| 9 | V1806 | 228 | `FOUND: 1 Blocker (time), 1 Major (the rest of a refused read)` | history: the decoders |
| 10 | V1806 | 162 | `13 comparison rows 7 differ` | comment G4, RP-1 |
| 12 | V1809 | 1 | `GATE B1809: NO GO @ 42f926d on main 7bf3752` | history: the secret store, its head |
| 13 | V1809 | 9 | `One Blocker by the commission's own rule for item 3 and one Major` | history: the secret store |
| 14 | V1809 | 9 | `Both are in the key` | history: the secret store |
| 15 | V1809 | 159 | `FOUND: 1 Blocker by the commission's rule` | history: the secret store |
| 17 | V1809 | 32 | `The product default is the library's call with no descriptor.` | comment G4, RP-3 |
| 18 | V1804 | 1 | `GATE B1804: NO GO @ 6bcd02e on main 7bf3752` | history: logging, its head |
| 19 | V1804 | 3 | `round 2 of 2` | history: logging, the second review |
| 20 | V1804 | 9 | `NO GO on ONE finding, and it is not in the product code` | history: logging |
| 21 | V1804 | 10 | `reports one alert of high severity on one line of TEST code` | history: logging |
| 22 | V1804 | 11 | `Everything the first verdict required is closed` | history: logging |
| 24 | V1804 | 24 | `108 lose at least one harmless value (223 of 1210 values)` | comment G4, RP-5 |
| 25 | V1804 | 25 | `with no writer the scan gives no result` | comment G4, RP-4 |
| 31 | F1799 | 72 | `prints ONE summary` | owed item 4 |
| 32 | F1799 | 73 | `the wave's heavy lock` | owed item 4 |
| 33 | F1799 | 71 | `the wave.` | owed item 4 (one README pass after the wave) |
| 34 | F1806 | 46 | `a trimmed environment must pass` | owed item 4 |
| 35 | F1809 | 95 | `stays running and is shared between lanes` | owed item 4 |
| 36 | F1809 | 30 | `words and nothing more` | comment G4, RP-2 (the design says the words and nothing more) |
| 37 | F1809 | 59 | `the key file is owner-only, nothing binds it to the machine` | comment G4, RP-2 |
| 38 | F1809 | 34 | `names a domain group only for the` | comment G4, RP-3 |
| 39 | F1804 | 56 | `Whether a replaced NEIGHBOUR should read differently from a replaced VALUE` | comment G4, RP-5 |
| 40 | F1806 | 78 | `Today's default follows the design sentence (the older routines for the four enabled readers).` | comment G4, RP-1 |

**THE REVIEW MAP 2** (the later reviews of the four wave-1 libraries and the lanes after them; ANS1 is the coordinator's `2026-11-21_B1831_ANSWER-1_r03-fail-closed.md`; CHG the change list; P1823 the coordinator's `2026-11-21_B1823_OXPD-LANE-PLAN-WAVE2.md`; REG the register; rows 28 and 36 to 38 of B1816 are not carried; 34 rows):
| RM2 | File | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | V1814 | 1 | `GATE B1814: GO WITH FINDINGS @ afc4e19` | BL-10 |
| 2 | F1814 | 12 | `ticket still stays open for the scan of logs from a real sign-in` | BL-10 |
| 3 | F1814 | 18 | `53 calls on the logger` | BL-10 |
| 4 | F1814 | 36 | `a NAMED constant counts as well as a literal` | BL-10 |
| 5 | V1819 | 1 | `GATE B1819: GO WITH FINDINGS @ ec75619` | BL-11 |
| 6 | F1819 | 50 | `Minor: one stated behaviour of the fix has no test that can fail` | BL-11 |
| 7 | F1819 | 59 | `a close can now wait, and in one shape never return` | BL-11 |
| 8 | F1819 | 74 | `changed its public answer` | BL-11 |
| 9 | V1821 | 1 | `GATE B1821: GO WITH FINDINGS @ ce38c25` | H-LAND, BL-11 |
| 10 | F1821 | 21 | `cannot fail on a wrong identity` | BL-11, BL-6 |
| 11 | V1822 | 1 | `GATE B1822: GO WITH FINDINGS @ 9fe5356` | H-LAND, BL-12 |
| 12 | F1822 | 32 | `One wrong time value on two consecutive calls ends the discarding early` | BL-12 |
| 13 | F1822 | 71 | `Does a printer ever deliver the same stale event again` | BL-12 |
| 14 | F1822 | 73 | `How long does one card read take on each reader` | BL-12 |
| 15 | V1824 | 1 | `GATE B1824: GO WITH FINDINGS @ bf1a4a2` | BL-5 |
| 16 | F1824 | 37 | `N1 Windows: a key planted under DPAPI-NG` | BL-5 |
| 17 | F1824 | 52 | `A ring left by the round-1 head carries 90-day keys` | BL-5 |
| 18 | F1824 | 13 | `The server does not use the store` | BL-5 |
| 19 | V1828 | 1 | `GATE B1828: GO WITH FINDINGS @ 9826559` | H-LAND, BL-5, BL-6 |
| 20 | V1828 | 201 | `| R1` | Records |
| 21 | V1828 | 202 | `| R2` | Records |
| 22 | V1828 | 203 | `| R3` | Records |
| 23 | V1830 | 1 | `GATE B1830: GO WITH FINDINGS @ 48120e5` | H-LAND, BL-7 |
| 24 | V1830 | 35 | `| F4` | Minor (process) |` |
| 25 | V1830 | 36 | `| F5` | Records (design point) |` |
| 26 | V1830 | 37 | `| F6` | Records |` |
| 27 | V1830 | 38 | `| F7` | Records |` |
| 29 | F1830 | 20 | `THE R5 FOLLOW-UP` | BL-7 |
| 30 | F1830 | 50 | `Enum drift on the callbacks` | BL-9 |
| 31 | F1830 | 62 | `stays open: contract tests against simulator responses wait for hardware` | BL-7 |
| 32 | ANS1 | 9 | `Alternative (C), a listing that also yields the names of records that do not open` | BL-8 |
| 33 | CHG | 282 | `| N-1` | Does the on-panel Microsoft step apply` |
| 34 | CHG | 299 | `| N-18` | Kit item 16 under Azure hosting` |
| 35 | P1823 | 121 | `| Q-B` | May Datasec's own app strings under` |

**THE REVIEW MAP 3** (the reviews of lanes SL, B, E, T and the later reviews that G4 leans on; each fragment is on exactly one line of its file, MEASURED-BY-DRAFTER; 78 rows):
| RM3 | File | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | V1854 | 1 | `GATE B1854: NO GO @ a5ba020 on main 61b17ec` | H-LANE-SL |
| 2 | V1855 | 1 | `GATE B1855: NO GO @ a5ba020 on main 61b17ec (second reader)` | H-LANE-SL |
| 3 | V1864 | 1 | `GATE B1864: GO WITH FINDINGS @ 8578d96 on main 977cbeb` | H-LAND, H-LANE-SL, BL-13 |
| 4 | V1865 | 1 | `GATE B1865: GO WITH FINDINGS @ 8578d96 on main 977cbeb (second reader)` | H-LAND, H-LANE-SL, BL-13 |
| 5 | F1864 | 22 | `1. Who may call `DeleteUnreadable` in the product is open` | BL-13 |
| 6 | F1864 | 31 | `A second process over the partition writing without changing the key ring can still race the removal` | BL-13 |
| 7 | F1864 | 33 | ``EIO` and `ENFILE` take the open-failure path by source reading` | BL-13 |
| 8 | F1864 | 17 | `is now refused` | BL-13 |
| 9 | V1865 | 64 | `Measured, Unix analogue (P13)` | BL-13 |
| 10 | V1865 | 68 | `Precondition before any caller is wired` | BL-13 |
| 11 | V1865 | 78 | `Untyped `FileNotFoundException` under descriptor exhaustion with a cold decoder, kept by the runtime.` | BL-13 (second reader F1) |
| 12 | V1865 | 79 | `The README's `DeleteUnreadable` sentence lists "no file descriptor left"` | BL-13 (second reader F2) |
| 13 | V1865 | 80 | `D22 (a) as graded above: a named limit with a residual window` | BL-13 (second reader F3) |
| 14 | V1870 | 1 | `GATE B1870: GO WITH FINDINGS @ c5a6ff8 on main 8ae5e08` | H-LAND, H-LANE-B |
| 15 | V1871 | 1 | `GATE B1871: GO WITH FINDINGS @ c5a6ff8 on main 8ae5e08 (second reader)` | H-LAND, H-LANE-B |
| 16 | V1870 | 143 | `- F1 Minor: a duplicate `AddAsync` that loses a race` | BL-14 |
| 17 | V1870 | 146 | `- F2 Minor: `CapabilitySnapshot.Create` with a lone surrogate` | BL-14 |
| 18 | V1870 | 148 | `- F3 Minor: firmware and model are returned` | BL-14 |
| 19 | V1870 | 150 | `- F4 Minor (text of a result)` | BL-14 |
| 20 | V1870 | 152 | `- F5 Minor (tests): three mutants survive` | BL-14 |
| 21 | V1871 | 69 | `- **F1 (Minor; text false as written).**` | BL-14 |
| 22 | V1871 | 72 | `- **F2 (Minor).** A stored device firmware or model` | BL-14 |
| 23 | V1871 | 75 | `- **F3 (Minor; for B1870's C12 and the host's later wiring).**` | BL-14 |
| 24 | V1871 | 77 | `- **F4 (Minor; records).**` | BL-14 |
| 25 | V1871 | 81 | `The clock check reads the server's time BEFORE it awaits the source.` | BL-14 |
| 26 | F1870 | 7 | `Line 50 (restores) is no longer true as written` | BL-15 |
| 27 | F1870 | 14 | `74 of 74 equal` | BL-15 |
| 28 | F1870 | 22 | `The 15 lower bounds stay in the cache` | BL-15 |
| 29 | F1870 | 24 | `Test gaps the gate's mutants found` | BL-15 |
| 30 | F1870 | 32 | `The clock check truncates the offset to whole seconds` | BL-14 |
| 31 | F1870 | 34 | `A run of both migration sets against a real PostgreSQL 16 and SQL Server` | BL-15 |
| 32 | F1870 | 35 | `Database-level append-only enforcement for the audit log` | BL-15 |
| 33 | F1870 | 42 | `**Jira OXPD2-12 stays open.**` | H-LANE-B, BL-15 |
| 34 | F1870 | 46 | `Whether Microsoft.Data.SqlClient's Azure.Identity` | BL-15, CLAR-X |
| 35 | F1870 | 52 | `How the next lane that needs a package gets it` | BL-15 |
| 36 | F1870 | 56 | `THE MIGRATIONS section still names the first scaffold's id` | BL-15 |
| 37 | V1868 | 1 | `GATE B1868: NO GO @ 523204d on main 8ae5e08` | H-LANE-E |
| 38 | V1869 | 1 | `GATE B1869: NO GO @ 523204d on main 8ae5e08 (second reader)` | H-LANE-E |
| 39 | V1877 | 1 | `GATE B1877: GO WITH FINDINGS @ 610bb7d on main 5bb1418` | H-LAND, H-LANE-E |
| 40 | V1878 | 1 | `GATE B1878: GO WITH FINDINGS @ 610bb7d on main 5bb1418 (second reader)` | H-LAND, H-LANE-E |
| 41 | V1869 | 6 | `- **NO GO on one Major (F1, D9).**` | H-LANE-E |
| 42 | V1878 | 6 | `- **Round-1 Major F1 (D9) is closed.**` | H-LANE-E |
| 43 | F1877 | 21 | `StoreRefreshValue during a refresh is followed by that refresh's result` | BL-16 |
| 44 | F1877 | 25 | `An access value handed out before Forget may still be sent once` | BL-16 |
| 45 | F1877 | 26 | `The vault call of a rotation and of Forget runs under the serial's lock` | BL-16 |
| 46 | F1877 | 30 | `The Issue rotation cell is held by two mechanisms` | BL-16 |
| 47 | F1877 | 32 | `a credential digest read from the vault but not cached` | BL-16 |
| 48 | F1877 | 37 | `B1868 F4 / B1869 F6: a refresh answered after RefreshTimeout is discarded` | BL-16 |
| 49 | F1877 | 40 | `B1869 F7: a 401 after a failed refresh` | BL-16 |
| 50 | F1877 | 41 | `B1869 F8: a wrong-length stored hash` | BL-16 |
| 51 | F1877 | 42 | `B1869 F9: the holder zeroes the array TryGet returns` | BL-16 |
| 52 | F1877 | 44 | `Forget whose vault delete throws during a refresh` | BL-16 |
| 53 | F1877 | 50 | `Whether a stranger's unknown serials are cached negatively` | BL-16 |
| 54 | F1877 | 52 | `Round 1's NOT DECIDED items 1 to 7` | BL-16 |
| 55 | F1877 | 16 | `Local totals: branch 1234 -> 1248` | BL-16 |
| 56 | V1878 | 11 | `Records only, no Minor or above: R1` | BL-16 |
| 57 | V1885 | 1 | `GATE B1885: GO WITH FINDINGS @ b514a6b on main f01b907` | H-LAND, H-LANE-T |
| 58 | V1886 | 1 | `GATE B1886: GO WITH FINDINGS @ b514a6b on main f01b907 (second reader)` | H-LAND, H-LANE-T |
| 59 | V1885 | 34 | `| F1 | Minor (test gap) |` | BL-17, BL-19 |
| 60 | V1885 | 35 | `| F2 | Records | **H8 (the seat's deviation):**` | BL-17 |
| 61 | V1885 | 36 | `| F3 | Records | **The converter refuses enums without wire names**` | BL-17 |
| 62 | V1885 | 37 | `| F4 | Records | **K6b is a one-line scan**` | BL-17 |
| 63 | V1885 | 38 | `| F5 | Records | D8's README line on maps not added` | BL-17 |
| 64 | V1886 | 74 | `- **F1 Minor (records).** The kit's H8 row` | BL-17 |
| 65 | F1885 | 16 | `1. The runbook gains the regen discipline for tolerant enums` | BL-17 |
| 66 | F1885 | 18 | `2. The backlog gains NOT DECIDED 1` | BL-17 |
| 67 | F1885 | 25 | `3. **A missing cell (F1 of VERDICT.md):**` | BL-19 |
| 68 | F1885 | 38 | `7. **K6b's red-first is by a stub only:**` | BL-17 |
| 69 | F1885 | 12 | `Local and hosted totals: 1392 -> 1404` | BL-17 |
| 70 | F1814 | 10 | `- `OXPD2-15` ([WP1.10] Logging deny-list)` | G4 (RP-4, RP-5 carried) |
| 71 | F1814 | 3 | `Only what THIS round adds. Everything else stands as the second check` | G4 (RP-4, RP-5 carried) |
| 72 | F1822 | 68 | `Round 1's list A (the Datasec team, the family question first, with its consequence)` | G4 (RP-1 carried) |
| 73 | F1824 | 76 | `4. **The DPAPI-NG descriptor** for a stand-alone Windows node and for the pair` | G4 (RP-3) |
| 74 | F1824 | 78 | `5. **What "sealed" means for the Linux key file**` | G4 (RP-2) |
| 75 | V1828 | 108 | `The default DPAPI-NG descriptor was refused on this machine.` | G4 (RP-3) |
| 76 | V1819 | 33 | `DELIMITERS: 0x00 `refused/refused`, 0x01 to 0x0f each `taken/taken`` | G4 (RP-6) |
| 77 | F1819 | 44 | `Item 11 (does the print service ever send a group other than` | G4 (RP-6) |
| 78 | F1819 | 34 | `4. No ceiling on fetches per document` | G4 (RP-7) |

**THE REPORT POINTERS** (reports A12 and B4; a single quote in a fragment stands for a backtick):
| RP | Report | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | A12 | 12 | `seven fields` | owed item 3, fact 3 |
| 2 | A12 | 15 | `9 proposed corrections; 14 secret locations` | owed item 2; the provenance paragraph |
| 3 | A12 | 121 | `takes both addresses from the QR` | owed item 3, fact 3 |
| 4 | A12 | 145 | `1. '02:46' (P13) and '02:1086'` | owed item 2 (1) |
| 5 | A12 | 146 | `2. '03:404' and '05:173' (OP-11)` | owed item 2 (2) |
| 6 | A12 | 147 | `3. '03:403' and '05:172' (OP-10), '05:200' (kit item 12), '05:242'` | owed item 2 (3) |
| 7 | A12 | 148 | `4. '02:420' (M3)` | owed item 2 (4) |
| 8 | A12 | 149 | `5. '03:143' (WP0.7) and '03:177' (WP3.1)` | owed item 2 (5) |
| 9 | A12 | 150 | `6. '02:612' and '05:102-103'` | owed item 2 (6) |
| 10 | A12 | 151 | `7. '02:367' (C7)` | owed item 2 (7) |
| 11 | A12 | 152 | `8. 'A9:261'` | owed item 2 (8) |
| 12 | A12 | 153 | `9. '05:252'` | owed item 2 (9) |
| 13 | A12 | 24 | `Its file name is withheld here` | the provenance paragraph |
| 14 | B4 | 12 | `1,511 of its 1,514 files are byte-identical` | entry B; the provenance paragraph |
| 15 | B4 | 14 | `This folder is the OXPd 2 SDK.` | entry B; span FQ-10 |
| 16 | B4 | 99 | `Starts at zero for any given target/operation` | owed item 3, fact 1 |
| 17 | B4 | 99 | `'02:362'` | owed item 2 (S-2) |
| 18 | B4 | 99 | `a loss before it cannot be seen` | owed item 3, fact 1 |
| 19 | B4 | 100 | `will always be delivered in order` | owed item 3, fact 1 |
| 20 | B4 | 100 | `'02:368'` | owed item 2 (S-3) |
| 21 | B4 | 100 | `'03:154'` | owed item 2 (S-3) |
| 22 | B4 | 101 | `STAYS UNMEASURED` | owed item 3, fact 1 |
| 23 | B4 | 102 | `no time of reading` | owed item 3, fact 2 |
| 24 | B4 | 102 | `CONTRADICTS the wording` | owed item 2 (S-5) |
| 25 | B4 | 102 | `more than N seconds after it was read` | owed item 3, fact 2 |
| 26 | B4 | 103 | `'02:804'` | owed item 2 (S-6) |
| 27 | B4 | 106 | `SETTLES HALF` | owed item 2 (S-9) |
| 28 | B4 | 106 | `'02:379', '02:1029', '03:54'` | owed item 2 (S-9) |
| 29 | B4 | 116 | `'02:452'` | owed item 2 (S-12) |
| 30 | B4 | 165 | `Private key of HP's SDK development root CA` | the provenance paragraph |
| 31 | B4 | 166 | `Passphrase for that key` | the provenance paragraph |

**THE CLARIFICATION POINTERS** (for entry S; the register is row 2 of THE SOURCES, report D2 is row 13):
| CP | File | Line | The line holds | Used by |
|---|---|---|---|---|
| 1 | the register, entry C-29 | 176 | `Phone code or phone link` | entry S, message 1 |
| 2 | the register, entry C-43 | 280 | `also, Datasec has a deployment utility so you should use this or amend it so we can use it for this project` | entry S, message 2 |
| 3 | the register, entry C-43 | 282 | `deployment for OXPd uses Datasec's existing HPK Deployment Utility, amended where OXPd needs it, in place of a new installer` | entry S, message 2 |
| 4 | the register, entry C-26 | 158 | `On each site's network` | entry S, messages 3 to 5 |
| 5 | the register, entry C-17 | 104 | `Both equally` | entry S, messages 3 to 5 |
| 6 | the register, entry C-42 | 274 | `Still his, unchanged by this tap: anything to HP or any person, any spend, any Azure resource` | entry S, message 6 |
| 7 | report D2 | 148 | `(C-43): there are two` | entry S, message 2 |
| 8 | report D2 | 155 | `ASM/Directory.Build.props:6` | entry S, message 2 |
| 9 | report D2 | 155 | `338 of 344 files dated 2026-11-11` | entry S, message 2 |
| 10 | report D2 | 161 | `is an INFERENCE from the dates` | entry S, message 2 |

**THE QUOTE MAP** (the eight strings that stand between single quotes in comment G4 as the first reviews' own words; each is found in the lines named once those lines are stripped, joined by one space and freed of the bold marks):
| QM | File | Lines | The words |
|---|---|---|---|
| 1 | F1806 | 72 | `Which family of decoding routines produced the card strings that today's customers have stored` |
| 2 | F1806 | 74 | `the two give different strings from the same card in 7 of 13 compared inputs` |
| 3 | F1806 | 77 to 78 | `Nobody is signed in as someone else by this; people are refused.` |
| 4 | F1804 | 118 to 119 | `closed before the scanner is given a shell or a pipeline entry point, or before any person is told to run it.` |
| 5 | F1804 | 76 | `108 of 230 events lose at least one harmless value (47 in 100); 223 of 1210 values (18 in 100).` |
| 6 | F1799 | 63 | `Does the print service ever answer with an attribute group other than operation, job, printer or unsupported` |
| 7 | F1799 | 41 | `an answer that gives one byte and then fails resets the retry count` |
| 8 | F1799 | 41 | `a ceiling on fetches or on elapsed time per document` |

**E-WORDS** (his words between single quotes in comments G1 and G2; each found exactly once in the extract at the line named and once in its span; they keep his spelling and his two blanks after a full stop):
| EW | Comment | Extract line | His words |
|---|---|---|---|
| 1 | G1 | 28 | `assume English for phase 1 but add to jira questions` |
| 2 | G1 | 29 | `I do not know and will ask workpath team.  Ask as a follow up question, add to jira questions` |
| 3 | G1 | 30 | `Ask as a follow up question for workpath team, add to jira questions` |
| 4 | G2 | 24 | `I do not believe so but I will check` |

**THE NAME TOKENS** (his notes name people; no person's name may stand anywhere but inside the quotation of entry A, and this kit holds none). Cut them by program from the extract, never by eye, never printed: split the line on white space, count tokens from 0, strip everything but letters, lower-case: line 9 tokens 28 and 29; line 10 tokens 6, 7 and 38. That gives 3 distinct words of 4, 5 and 6 letters; the sha256 of the three, sorted and joined by commas, is `e2111b425ebab8bee2fc629c17d2a41a6eb04f72fa28a1d86820ff6285d668c7` (MEASURED-BY-DRAFTER: equal). Token 37 of line 14 is a fourth, lower case and an ordinary English word: only its Capitalised form is banned. Rule X: none of the three words (any case, underscore-aware) and not the Capitalised fourth, in any Jira text and in any added record line that is not a quotation line. Control: each token planted as `_by_<token>_` must fire.

## THE CARD PRINTS, THE BOARD LINE AND THE COORDINATOR'S ANSWER (the basis of entries X and Y and of the tenth string of entry V; printed by the drafter with the read verb `show`, 10:2x to 10:37 AEDT)
**Card print 1** (`decision_queue.sh show` of the card of the driver packages), whole:
```
id:      datasec-oxpd-sqlserver-driver-identity-packages-1121
status:  ruled   (Datasec/OXPd)
title:   OXPd database: the standard SQL Server driver brings Microsoft's sign-in packages with it. Keep them?
bluf:    No action needed tonight: the default keeps them. The state database lane uses Microsoft's own SQL Server driver (Microsoft.Data.SqlClient 6.1.7). That driver always brings along Microsoft's cloud sign-in libraries: Azure.Identity 1.17.1, Azure.Core 1.50.0, the Microsoft identity client 4.84.2 with its broker and helpers, and six identity-model packages. A reviewer checked every package against nuget.org's own published hash (74 of 74 equal) and found that only the driver itself loads in our tests; the sign-in libraries are used only if a customer connects to SQL Server by signing in with Entra ID (read from the packages' documentation, not run). They sit in the database library only, not in the server program today. A telemetry package seen in the list (Application Insights) belongs to the test tools only and was already there. Who decides: you (what ships in the server's dependencies). (Override note: your 'Fetch them once' ruling covered the four packages and their dependencies, but its card named only Entity Framework Core and the PostgreSQL driver, never these sign-in libraries, and the lane's own kit left their staying open for you; the other matches are other subjects.)
options (recommended: a):
  [a] Keep them (standard driver)
        detail: They come with Microsoft's supported driver; they also allow Entra ID sign-in to a customer's SQL Server later
  [b] Remove them
        detail: Means a different, non-standard way to talk to SQL Server; a new lane, a new package question, and no Entra sign-in to SQL Server
  [c] Decide later
        detail: Keep them for now; ask again before the first customer release
default: a: keep the standard driver and its sign-in libraries
ruling:  choice='a'  ruled_ts=2026-11-22T09:36:12.227298+11:00
```
Entry X's fills are cut from it by program: `<<X-TS>>` the value after `ruled_ts=` (2026-11-22T09:36:12.227298+11:00); `<<X-TITLE>>` the line `title:` after its label and spaces; `<<X-DEFAULT>>` the `default:` line after its label; `<<X-LABEL>>` the text after `[a] ` on the option line; `<<X-DETAIL>>` the text after `detail: ` on the line below it. The `bluf:` paragraph and options b and c are the coordinator's and are not copied.

**Card print 2** (the card of tolerant device answers; the coordinator's ADDENDUM-1 of 2026-11-22 10:4x asked for it), whole:
```
id:      datasec-oxpd-tolerant-device-answers-1122
status:  ruled   (Datasec/OXPd)
title:   OXPd: read the printer's own answers tolerantly too, and accept a new kind of result?
bluf:    No action needed; the default keeps today's strict reading. Override of prior rulings: the 50 matches are other subjects except the parent card on callbacks (ruled b), whose option detail named callbacks only; this card asks exactly what it left out. Your ruling of Friday night is built and on main (pull request 14): a printer callback with a value we do not know is read, the value kept as unknown, never counted as success. Two things that ruling did not cover stay strict until you say: (1) the printer's own answers to our questions (its status or supplies after a firmware update) are still refused whole if they carry a value we do not know; (2) a callback that carries a NEW kind of result (for example a new kind of sign-in outcome) is still refused, because we cannot tell what it means. The review measured both as strict today.
options (recommended: a):
  [a] Keep both strict for now
        detail: Revisit after Monday's printer test shows real traffic
  [b] Device answers tolerant too
        detail: Read the printer's own answers the same way as callbacks (a later lane with its own design and review); a new kind of result stays refused
  [c] Decide after Monday
        detail: Same as a until you have seen the printer test
default: a: keep both strict; revisit after the printer test
ruling:  choice='a'  ruled_ts=2026-11-22T10:36:21.662870+11:00
```
Entry Y's fills are cut from it the same way (`<<Y-TS>>` is 2026-11-22T10:36:21.662870+11:00; the store prints the seconds with six decimals). **His note is not in the store's ruling field.** It is the fifth line of the coordinator's print of the day's rulings (`tools/kam_rulings_today.sh`, run by the drafter), printed whole here and quoted whole in entry Y (a quotation line, so it keeps its dash, a non-ASCII byte, and his typing):
```
10:35 [live] | Decision datasec-oxpd-tolerant-device-answers-1122: a — Keep both strict for now | note: but make a note that this was a decision and can me changed if necessary
```
The reader prints the clock 10:35 only; the board's own stamp of the tap, 10:35:55, is the coordinator's freshness line, RELAYED. **The coordinator's answer of 2026-11-21 21:07:43.940908+11:00** (entry V's last quotation line) is the whole text of the one row of the chat store `0_Brain/dashboard/data/chat_tuesday.json` with that `ts`, role `wednesday` (the store's old name for the coordinator), 571 characters, ASCII, no double quote (MEASURED-BY-DRAFTER: one row holds the string, and no other); you do not open the store: slot V-WORDS is Tuesday's compare.

## THE ORIGIN, THE LANDINGS FILL AND THE GATING HEADS (MEASURED-BY-DRAFTER by `gh api -X GET`, 10:2x AEDT; you re-measure at Step 2 and again inside the process that writes the records)
- `pulls?state=all&per_page=100`: 14 pull requests, all closed and merged; `pulls/99999` is 404 (control). `git/matching-refs/heads`: 17 refs; main at `ca94ed966ff476d31e2d35cb1ae0cc5c5d4b39b5`.
- **THE LANDINGS FILL.** Inside the process that writes the records, GET `repos/datasecau/OXPd_2/pulls?state=all&per_page=100` (the URL quoted). Take every pull request whose `merged_at`, turned into Australia/Sydney time, is on or after 2026-11-21 00:00, in the order of `merged_at`; for each, GET `repos/datasecau/OXPd_2/commits/<merge_commit_sha>`. Each item is exactly `pull request <n>, titled "<title, as the pull request GET prints it>", merged as <first 8 of merge_commit_sha> with <k> parent` (`parents` when k is not 1); items joined by a semicolon and one blank; `<<LANDED-COUNT>>` their number; `<<MAIN-SHORT>>` the first 8 of main; `<<PR-TOTAL>>`, `<<PR-OPEN>>` the counts; `<<ORIGIN-CLOCK>>` the clock from `date` at the read. A title that holds a double quotation mark, or fails the scanner, HOLDS TEXT H-LAND (`STOPPED: NEEDS TUESDAY`, never a re-wording). The drafter's prototype (the fill's items, built by the same rule; pull requests 1 and 2 merged on 2026-11-20 AEDT and are not in it): pull request 4, titled "Add the IPP reader and writer, two request builders and the resumable document stream for Universal Print; nothing talks to anything yet (WP4.2, part)", merged as bb8a49e2 with 1 parent; pull request 3, titled "Add the card decoder library: five decoding routines, the reader table and read assembly; nothing reads a reader yet (WP1.3)", merged as ddbdf800 with 1 parent; pull request 5, titled "Add the local secret store library: encrypted records, a key ring checked at every use, rotation, re-wrap and a guarded revocation; the server does not use it yet (WP1.1, part)", merged as bb914334 with 1 parent; pull request 6, titled "Add HP's OXPd 2 specification inputs with a fingerprint list, generated clients and callback models with a bounded parser, and a gateway test stub (WP0.4, part)", merged as 5e36d8dc with 1 parent; pull request 7, titled "OXPd 2 contracts: read-only schema and catalogue lists, a bounded body limit, and cells for the Unicode length rule (WP0.4)", merged as 0804860b with 1 parent; pull request 8, titled "Repository rule R5: exempt HP's 37 listed specification inputs by path and sha256 together, and never open a key folder of the supplied source (WP0.4 follow-up)", merged as 61b17ec0 with 1 parent; pull request 9, titled "Add the session and token broker: sessions per device, opaque handles, a bounded refresh through an interface, records only through the secret store (WP1.5)", merged as 762e774e with 1 parent; pull request 10, titled "Add the shared Graph HTTP layer: paging, Retry-After, one token refresh on 401, chunked uploads; unreadable answer text is a malformed response (WP3.8)", merged as 977cbeb2 with 1 parent; pull request 11, titled "Secret store: list the records it cannot read, and remove one only when its bytes were read and fail as a record (WP1.1)", merged as 8ae5e08c with 1 parent; pull request 12, titled "Add the device registry and state database: EF Core, migrations for PostgreSQL and SQL Server, clock check (WP1.1 part)", merged as 5bb1418c with 1 parent; pull request 13, titled "OXPd 2 adapter: a per-device solution-token holder with one refresh per burst, a constant-time callback credential check and bounded handlers of five printer callbacks (WP1.2, part)", merged as f01b907e with 1 parent; pull request 14, titled "OXPd 2 contracts: read printer callbacks tolerantly (an unlisted enum value of a service target reads as Unrecognized, never a success and never written; an optional property sent as null reads as absent)", merged as ca94ed96 with 1 parent
- **THE GATING HEADS.** TEXT H-LAND says that the merged head of pull requests 3, 4, 5, 6, 11, 12, 13 and 14 was read GO WITH FINDINGS: for each n the first 7 characters of the pull request's `head.sha` must equal the head named in the first line of the review rows: 3 `9fe5356` (V1822), 4 `ce38c25` (V1821), 5 `9826559` (V1828), 6 `48120e5` (V1830), 11 `8578d96` (V1864, V1865), 12 `c5a6ff8` (V1870, V1871), 13 `610bb7d` (V1877, V1878), 14 `b514a6b` (V1885, V1886) (MEASURED-BY-DRAFTER: all eight equal the pull requests' head shas). A head that differs drops the pull request's name from that sentence and STATUS says so.
- **THE LANE G CHECK (gate of owed item BL-18):** GET the file `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs` at the ref `b1841/wp17-scan-and-print-jobs` (raw), count the name `W02_a_body_whose_read_throws` (the drafter read 0) and, as control, `W02_a_wipe_during` (the drafter read 1). Only 0 and 1 write BL-18; any other reading HOLDS BL-18 and STATUS names it (the cell may have landed).

## THE JIRA ROWS, THE CLOSED LIST AND THE TEXT RULES
- **OXPD2-1**: Task, Backlog, labels `master-list`, `questions`, 7 comments (ids 41405, 41406, 41408, 41412, 41413, 41414, 41419) at drafting. Its newest comment is the form: one paragraph, BLUF first, the sentence that nothing moves, `Records note, <date>`, the marker in square brackets last. Never written: any other key, a create, a transition, an edit.
- **Census at drafting:** 24 issues OXPD2-1 to OXPD2-24, 0 in Done; controls OXPD2-1 reads 200, OXPD2-99999 reads 404. Expected after: 24 and 0, exactly ONE key changed, OXPD2-1, and on it only the comment count and ids.
- **Markers** (`project = OXPD2 AND ( text ~ "\"<marker>\"" )`): `REC-FQ-ASKED-20NOV`, `REC-FQ-OWNCHECK-20NOV`, `REC-FQ-RAISED-20NOV`, `REC-REVIEW-POINTS-20NOV` each 0 keys at drafting; control `REC-MVP-ANSWER-20NOV` finds OXPD2-1, `zzqxnonexist` finds none. The marker date stays 20NOV. At Step 0 `date +%d%b` must read 22Nov or 23Nov; any other: `STOPPED: NEEDS TUESDAY the clock reads <date>`.
- **Phrase searches (the same JQL form; re-run before the first write; a key outside the expected set is read whole, named, and HOLDS the comment it would duplicate):** `add to jira questions` 0 keys; `quick messages` OXPD2-1; `licence server` OXPD2-1; `sealed` 0; `named pipe` 0; `decoding routines` 0; `group delimiter` 0; `DPAPI` 0; `sign-out confirmation` 0; `FutureSmart 6` OXPD2-1 and OXPD2-2; `defect level` OXPD2-1; `unknown value` 0; `tolerant` 0; `labels = b1785` 5 keys (control) (MEASURED-BY-DRAFTER, GET, 10:2x).
- **THE JIRA CLOSED LIST. Property:** OXPD2-1 only; **at most FOUR POST requests, all to `/rest/api/3/issue/OXPD2-1/comment`**, one per group that slot COMMENTS names, in the order G1, G2, G3, G4, each its exact text as ONE paragraph (ADF: one `paragraph` node holding one `text` node), each only when its marker search reads 0, entry A is written and its filled text passes every rule below; G3 only when slot FQ names at least one number. Each is read back by its comment id byte-equal (a one-character mutant compares unequal), the key's status, labels and description hash unchanged, its comment total up by one. **Any other request shape: prove it meets the property or STOP.** Your poster refuses, each on its own reason: another key, a create, a transition, a PUT, a DELETE, a fifth POST, a group the slot does not name, a second post of a group, a marker that already reads, a text that fails a rule or whose spans differ from their frozen sha256, any write while slot JIRA is DRY, any call while `.tools/b1887/HOLD` exists. Credentials are read BY NAME in-process from `<project>/4_Credentials/.env` (never printed, never on argv); every request is logged to `.tools/b1887/logs/jira-requests.log` BEFORE it is sent (method, path, body sha256). GETs at most 4 per second, writes at least 3 seconds apart; `snap_before.json` before the first write and the after-census diffed against it. After a failed post run the marker search before anything else.
- **THE TEXT RULES: the scanner is the PROJECT'S OWN.** Copy `<project>/.tools/b1785/b1785.py` to `.tools/b1887/proj_b1785_copy.py` with `cp -n`, prove it with `cmp` and print its sha256 (the drafter's copy read `5e766b28f9b90f8f02b371e0acadee39b9f0cafd5e94a9e8d51924f1e868a078`, MEASURED-BY-DRAFTER, equal to the project file); **never edit it, never run it as a program**; load it with `importlib` and call `scan_jira` (every Jira text) and `scan_record` (every added record line that is not a quotation line); on top of it rule X. **A hit is a STOP for that text, never a re-wording by you.** Exemptions, each by name: quotation lines (they start with `>`) of the entries are his words, the card's or the coordinator's and are not scanned; the card id stands in no record line (entries X and Y quote the store's print, which holds none). The drafter ran both scanners over every filled non-quotation line of the 70 texts with stand-in fills: 0 problems (control: a planted name token and a planted card id each fired).

## HOW A FROZEN TEXT IS READ
Every text stands in a fenced block whose first line is `[[TEXT <id>]]`; the text is every line after the id line up to the closing fence, joined by line feeds, no line feed at its end. Its length and sha256 (UTF-8, unfilled) are in THE FROZEN TABLE; **check every one BEFORE filling; a difference is a STOP.** Fill-ins are `<<NAME>>`, replaced by program only; **no `<<` may remain in anything you write.** `<<OUTCOME>>` is `This note moves nothing and the ticket stays open.` (sha256 `c892c556ac0cb2acf69bdede06785a96e4a2b9510b2b441b314295a1af7fd19b`). `<<WRITE-DATE>>` is `date +%Y-%m-%d` at the write; `<<HHMM>>` the clock of the history write from `date`, once. `<<C-A>>`, `<<C-B>>`, `<<C-S>>`, `<<C-V>>`, `<<C-X>>`, `<<C-Y>>`, `<<C-W>>` are the numbers YOUR program gave the entries it wrote (the highest live `## C-<n>` heading plus 1, 2 and so on in the order A, B, S, V, X, Y, W; an entry that is held takes no number and the next moves up). `<<C-R>>`, `<<C-T>>`, `<<C-U>>` are the headings of the entries already written, found by program: the heading above the line `> One more one-line round, then merge`, above the line that starts `> 2026-11-21, about 14:30 by the coordinator's log` and above the line that holds `keys added so please check` (each probe must hit exactly once; they read C-55, C-56 and C-57 at drafting). `<<V-REF>>` is `<<C-V>>` when entry V was written, else the words `his rulings of the evening of 2026-11-21 (not recorded by this pass)`. `<<OWED-k>>` is the number your program gave the owed item BL-k: the highest owed number of the live `BACKLOG.md` (30 at drafting) plus its place in the insertion order BL-2, BL-3, ... BL-19 (so BL-2 is 31 and BL-19 is 48; BL-1 of B1816 is retired and has no number); a held item takes no number and the later ones move up. `<<EXTRACT-SHA>>` the extract's sha256 as you read it; the others are named where used.

## PART 1: THE CLARIFICATION ENTRIES (slot CLAR; appended to `CLARIFICATIONS.md` in ONE rewrite, before any Jira write)
At drafting the file has 444 line feeds, 43605 bytes, sha256 `763a76e5cd7cee7079fc91b0b0a0bab5c149621ff42f0996fe259acac34d91c8`, ends with exactly one line feed, and its last heading is `## C-57`. The new tail is: one empty line, entry A, then (each preceded by one empty line, each only when its slot allows) B, S, V, X, Y, W, and one line feed at the end. **The old bytes are a prefix of the new file, byte for byte.** Prototype figures, computed by the drafter's program from the texts with stand-in fills (PREDICTED for your run, not measured on a built file): see THE DRY-RUN FIGURES.
**Entry A** = TEXT CLAR-A-HEAD, one empty line, THE QUOTE BLOCK, one empty line, TEXT CLAR-A-READ. **THE QUOTE BLOCK is built from the extract:** for each of the lines 3 to 35, in order, the line `> <n>. <the extract's line, every byte>` with n from 1 to 33, and between two such lines one line holding the single character `>`. It has 65 lines; its sha256 (UTF-8, no line feed at its end) is `e89dca6f9921de49bbbfb83d6087c7e8df2d3af47085382e21c32d7d44324248` (the same block B1816 built and checked). A different sha256 is a STOP.
```
[[TEXT CLAR-A-HEAD]]
## <<C-A>>

Live board, view=tuesday, 2026-11-20 21:04:30 AEDT, a message with no words of his own (the text reads "3 files attached") and three attachments: `Question by owner document.docx` (18354 bytes, sha256 a13a0fac0a1ee9e28607d15e3e51062f3f36ed9d354d1f08de57d69b37682655), `cc-api-main.zip` and `CypherKey-cypherkey.zip`. The Word file holds his notes on the questions document (`Registers/QUESTIONS_BY_OWNER.md`). Its 33 non-empty paragraphs follow, verbatim and in order, copied by a program from the coordinator's extract of the Word file (lines 3 to 35 of that extract; the extract's sha256 is <<EXTRACT-SHA>>). The number in front of each paragraph is its place in his document and is not his.
```
```
[[TEXT CLAR-A-READ]]
Tuesday's reading, nothing wider. This entry was held on 2026-11-21 because the three design documents (`02`, `03` and `05` under `Design/`, cited here as document:line of the copies in this folder on <<WRITE-DATE>>) were revised on 2026-11-21, between 08:34 and 08:37, after the kit that held it was drafted. That revision is made: it applied his words of 2026-11-20 between 21:59 and 22:04 and these notes through a change list (`Review/B1817_DESIGN-CHANGE-LIST_2026-11-20.md`), each change marked B1817 with the row's id and his words beside it (`05:5`, `02:1132`, `03:594`). So this entry no longer says that a correction pass of the three documents is owed. It says, for each answer, where the revised documents now stand, read from their own text and change logs. Every line named below was printed and read when this entry was written. People he names stay inside the quotation.

His instructions (paragraphs 2, 3, 4 and 33): redo the questions document so that it starts with the BLUF, asks one question per item, can be filled in, and starts with list B. A redone document, `Registers/QUESTIONS_BY_OWNER_v2_2026-11-20.docx` with a `.pdf` beside it, is in this folder (both files listed when this entry was written). That it went to him the same evening is the coordinator's statement, relayed.

Answers that CHANGED a default the design carried, each with where the revised documents now stand. Paragraph 9 (P2): the firmware version of his printer is not needed, because the printer will be wiped for developer mode; applied: `05:245` now says that the firmware version does not matter (change list row R4-46), and still says that which OXPd generation his printer model runs is not established. Paragraph 12 (P3): mirror how the current product signs users in; MFA is on by default and the sign-in options depend on the set-up. The first reading of this entry, written before the revision, took it as option (a) of the question it sits under (QR sign-in without MFA, `05:120`, where the document recommends (b) at `05:121`). The revised documents do not read it so: `05:215` (open question N-15, row R4-44) records that his words do not name QR and so do not settle that question, and keeps default (a). This entry follows the documents: it does not read P3 as an answer to that question. He also asks that the sign-in paths of the current product be understood and documented, and offers to share the videos again; change list rows R4-28 to R4-30, R4-36 and R4-37 (`02:1192` to `02:1196`) carry what the revision took from the reports on those paths, and whether they are documented in full is not said by his words or by this entry. Paragraph 15 (A4): everything is in the customer's tenant, the OXPd servers included, and customers deploy in their own Entra tenant; the revised documents apply it together with his later messages (<<C-S>>): decision D1 at `02:900` now reads in the client's Azure subscription for Phase 1, one server per site, with the network shape open (P-4, `05:199`); and `05:114` keeps default (a) for Datasec's own Universal Print registration while N-14 (`05:214`) asks whether his words mean that each customer registers their own. Paragraph 17 (A6): a licence server through Azure or through Datasec, two deployment options; applied: `05:172` marks point OP-7 answered (row R2-54), and the sentence of `02` that the server calls the Datasec-hosted licence service is replaced by the two options (change log item 24, `02:1166`, row R2-16). Paragraph 20 (A9): he attached source for the phone app; applied: `05:175` marks point OP-10 answered, the source being in hand (row R4-11, report A12). Paragraph 23 (A15): a separate app, with integration intended after the MVP; applied: `05:170` marks point OP-5 answered, and work package WP5.8 (`03:214`) and decision D26 (`02:925`) now name the newer tool, the HP AuthSuite Manager, with the OXPd part as a separate app; which tool, and in what form, is open (P-6 and N-9, both at `05:201`). Paragraph 24 (A16): any worthwhile improvement will be done; applied: `05:171` marks point OP-6 answered and keeps its default cell as it was. Paragraph 26 (A18): assume English for phase 1; applied: `05:186` (OP-21), `05:267` (WP3.12) and `03:189` give English for Phase 1 and keep the question on the master list (rows R4-02 to R4-05); which apps that covers is not said by his words, and the revised documents note that Phase 1 with a capital P is his word and not the plan's phase 1 (`02:1132`).

Answers that CONFIRM what the design carries. Paragraph 13 (P4): the same function as the product in the market, deployed as OXPd; it agrees with C-48 and decision D34 (`02:932`). The hand-over half of P4 is not answered. Paragraph 14 (A2): mirror the existing operation of the apps; after sign-in it is the user's own token and so the user's own access. It gives no yes or no on the personal OneDrive app. The revised documents carry it beside the four design choices that differ from Workpath (`05:88`; decision D19 at `02:918`), which are asked back one by one and are decided by nobody, and beside open question N-10 (whether OneDrive's Shared with me is in the shipped app; change list rows R4-31 to R4-34; default kept, marked as resting on source). Paragraph 16 (A5): internet is essential for now; a local server that needs no internet is named for a phase 2; applied: `05:144` marks question 13 answered (row R2-53). Paragraph 19 (A8): yes, as the default of point OP-9 at `05:174` has it (marked answered there, row R2-56). Paragraph 25 (A17): yes for now, as the default of point OP-3 at `05:168` has it (marked answered there, row R3-40).

Answers that give a fact and leave their question open. Paragraph 6: he and each member of the Workpath team have HP access, and his is used during development (kit item 5, `05:229`, row R4-48). Paragraph 7: HP is reached through its portal for general questions, and he escalates when needed (kit item 14, `05:238`, row R4-49). Paragraph 8: a printer at his home; a lab with several printers and readers at a colleague's; HP's Experience Centre (kit item 4, `05:228`, row R4-45). Paragraph 10: Datasec holds the commercial agreement and, for a rework at its own cost, the right to distribute and to profit; the agreement has not been seen by the project, and the rule of C-11 on HP's beta library is not changed by this; the revised documents ask whether his words cover HP's library terms or the reverse-engineering clause (N-16, `02:1273`, row R4-52). Paragraph 11: the Windows machine is ready (kit item 2, `05:226`, row R4-47); the two points of C-53 are not mentioned. Paragraph 18 (A7): the Azure Marketplace; no number and nothing on the script route, so the default of point OP-8 at `05:173` stands, and N-17 (`05:211`) asks for the counts. Paragraph 21 (A11): not much more than what was provided; the default of point OP-13 at `05:178` stands and is not marked answered in full. Paragraph 22 (A12): he does not believe so and will check; the default of point OP-15 at `05:180` stands. Paragraphs 27 and 28 (A19, A20): follow-up questions for the Workpath team, to be added to the master list (change list rows R4-53 and R4-54). Paragraph 30 (A22): beta attached; no attachment of that message is an SDK and his next message points to a folder, which the revised documents read as the OXPd 2 SDK Beta 10 and not an OXPd 1.x SDK, with question 12 still open (`05:138`, row R4-07). Paragraph 31 (A23): anything that is needed (kit item 11, `05:235`, row R4-50). Paragraph 32 (A24): as close to commercial ready as possible; no threshold is given, `05:151` still reads that none is agreed, and N-13 (`05:213`) asks for one.

Not answered by these notes: the card key, the first point of the master list (question 8, `05:105`, narrowed by row R4-17 at `05:106` to whether a store build is made from the source unchanged). Paragraphs 1, 5 and 29 are a title, a heading and a pointer. The follow-up questions he asked for (A18, A19, A20) and his own check (A12) go to the master list, Jira `OXPD2-1`, through the records pass that wrote this entry. The open questions that the revision itself wrote (P-1 to P-9 and N-1 to N-18, `05:188` to `05:215`) are the coordinator's to put to him; none is decided by this entry.
```
**Entry B** (only when slot B-WORDS reads CONFIRMED):
```
[[TEXT CLAR-B]]
## <<C-B>>

Live board, view=tuesday, four messages of 2026-11-20 that followed his notes of 21:04:30 (<<C-A>>), verbatim. The clock in front of each is the one the coordinator read on the board; the words and the clocks reached the records pass through the coordinator's commission, and the coordinator confirmed them against the board before this entry was written.

> 2026-11-20 21:06:53 [live] | here is the beta code for /Volumes/DEV-Working/Datasec/WIP/OXPd2-SDK-Beta-10-20260416

> 2026-11-20 21:07 [live] | this should have been part of the original files from Friday, along with supporting documents, videos, etc.  some of the questions should be easily answered with this info.  please let me know if its not there

> 2026-11-20 21:17:36 [live] | copy the oxpd to our working drive as it will be necessary

> 2026-11-20 21:18:54 [live] | please do another review of the files you have, especially the supporting documents to understand how the current solution operates and is deployed.  The videos will provide screenshots and guidance as well

Tuesday's reading, nothing wider, and what was done on each (the coordinator's own record of that evening, relayed; none of it is the product owner's statement). On 21:06:53 and 21:07: he names a folder on the NAS as the beta code, says that it should have been among the original files together with supporting documents and videos, and asks to be told if it is not there. The folder was read the same evening (report `Analysis/B4_oxpd2-sdk-beta10-nas-folder.md`): by that report it is the OXPd 2 SDK Beta 10, and 1,511 of its 1,514 files are byte-identical to the copy the library already held. What the coordinator answered him is the coordinator's and is not recorded here. On 21:17:36: read by the coordinator as the SDK folder he had named AND the whole OXPd library on the NAS. Both were copied into `1_Project_Definition/Source_Documents/`: the SDK folder with 1514 files and 805564065 bytes, the library with 31481 files and 6277940515 bytes, each equal on both sides by a file count and a byte total, not by a hash of each file. Counted again by the records pass on <<WRITE-DATE>>, on the project's side only: <<COUNT-RESULT>>. On 21:18:54: a further review of the files held, the supporting documents first, of how the current solution operates and is deployed was commissioned by the coordinator the same evening. Whether it is finished is not stated by this entry, and no result of it is recorded here.
```
**Entry S** (only when slot S-WORDS reads CONFIRMED and entry A is written; B1816's text with five changes, named in the drafter's report):
```
[[TEXT CLAR-S]]
## <<C-S>>

Live board, view=tuesday, seven messages of 2026-11-20 that followed his notes of 21:04:30 (<<C-A>>) and his four messages of 21:06:53 to 21:18:54, verbatim, with his spelling and his two blanks after a full stop kept. The clock in front of each is the one the coordinator read on the board; the words and the clocks reached the records pass through the coordinator's commission of the design revision, and the coordinator confirmed them against the board before this entry was written.

> 2026-11-20 21:59:41 [live] | if my ruling moved it to the phone that is a mistake.  we must mirror the flow set in extra.  for Microsoft authenticator, that is initiate, display 2 digit in iframe, enter 2 digit in authenticator app.  we cannot interfere with the login flow or the token management done by microsoft

> 2026-11-20 22:00:26 [live] | of the two tools, check that they do the same thing.  I do not think so, but whichever is newer.

> 2026-11-20 22:01:21 [live] | p6.  yes.  clients deploy to their own tenant and our solution is subservient to the source of truth they use, currently entra

> 2026-11-20 22:03:25 [live] | one server per site on the customer's network is not inconsistent with them deploying through azure in their tenant.  Phase 1 will be hosted through azure and this offers different hosting options for the client

> 2026-11-20 22:03:48 [live] | OXPd runs in the clients azure subscription

> 2026-11-20 22:04:02 [live] | please go ahead and revise all docs and start building

> 2026-11-20 22:11:05 [live] | email me the PDF and doc version of the docs when they are finished and continue building what you can

Tuesday's reading, nothing wider. Each message is his ruling in his own words and is taken exactly as far as those words go; where a sentence below goes beyond them it is marked as the coordinator's reading. What the coordinator answered him between the messages is the coordinator's and is not recorded here. No design document is changed by this entry. Messages 1 to 6 bear on the design; message 7 bears only on the delivery of documents. Every line of an earlier entry that is quoted below was printed and read when this entry was written.

Message 1 (21:59:41). Settled by his words: "if my ruling moved it to the phone that is a mistake"; the flow must mirror "the flow set in extra"; for Microsoft Authenticator that flow is "initiate, display 2 digit in iframe, enter 2 digit in authenticator app"; and "we cannot interfere with the login flow or the token management done by microsoft". The coordinator's reading: "extra" is Entra (a dictation slip), and "it" is the Microsoft number step of the sign-in, which the design placed on the phone and cited C-29 for. NOT settled by his words: what is done if the printer panel cannot show that frame; whether a path on the phone stays beside it; any sign-in method other than Microsoft Authenticator. Against C-29: the register holds of C-29 only his tap, whose label is "Phone code or phone link"; the detail of that option is not in the register. His words are conditional ("if my ruling moved it") and reverse C-29 only so far as it was taken to move the Microsoft step to the phone. They do not withdraw the tap and do not say what else the option covered: which other parts of C-29 stand is decided by nobody. Of C-43, C-26 and C-17 it names none and reverses none. The revised documents apply it: the Microsoft step stays on the printer panel (`05:27`, row R1-42), and the sentence of C-29's option detail that the QR app is not counted as MFA stands (`05:196`, P-1).

Message 2 (22:00:26). Settled by his words: there are two tools; it is to be checked whether they do the same thing; he does not think they do; and the one to use is "whichever is newer". NOT settled by his words: he names neither tool and does not say which is the newer. The coordinator's reading: the two are the HPK Deployment Utility he attached with C-43 and the HP AuthSuite Manager, and the newer is the HP AuthSuite Manager, version 1.1.0. That reading rests on report `Analysis/D2_current-solution-deployment-second-review.md`, section 3 (printed at its lines 148, 155 and 161 when this entry was written): one reader's reading of the files, neither tool was run, the newer one is told from a version number and file dates, and the report itself calls the succession an inference. The revised documents record the same two readings side by side: by file dates the AuthSuite Manager is newer, by version number the Utility's 3.0.0 is higher than the Manager's 1.1.0, and which tool, and in what form, is open (P-6 and N-9, `05:201`). Against C-43: his words there, "also, Datasec has a deployment utility so you should use this or amend it so we can use it for this project", are not withdrawn: a deployment tool that Datasec already has is used or amended. What changes is which tool: the reading written in C-43, "deployment for OXPd uses Datasec's existing HPK Deployment Utility, amended where OXPd needs it, in place of a new installer", named the utility he attached, and under the coordinator's reading of "whichever is newer" it is the other tool. His answer A15 in <<C-A>> (a separate app, integration intended after the MVP) bears on the same point; how the two sit together is not settled. Of C-29, C-26 and C-17 it names none and reverses none.

Messages 3, 4 and 5 (22:01:21, 22:03:25 and 22:03:48), recorded as written. Message 3 begins "p6.  yes.". By the coordinator's statement (relayed), question P6 of the redone questions document asks an either-or: the OXPd server on the customer's own network, or in the customer's Azure subscription. A yes to an either-or picks no side by itself, and messages 4 and 5 followed it. What the three say together, in his words and no further: "clients deploy to their own tenant"; the solution is "subservient to the source of truth they use, currently entra"; "one server per site on the customer's network is not inconsistent with them deploying through azure in their tenant"; "Phase 1 will be hosted through azure and this offers different hosting options for the client"; and "OXPd runs in the clients azure subscription". NOT settled by his words: whether phase 1 also has a server at a site; how a printer at a site, an older printer above all, reaches a server hosted through Azure; what the hosting options are and who chooses among them; the packaging of the server. The coordinator's reading: in phase 1 the OXPd server is hosted through Azure in the client's own subscription and tenant, and a server at the customer's site is a hosting option and not the only shape. Against C-26: the register holds his tap, whose label is "On each site's network". No word of his withdraws that tap in terms. In his words phase 1 "will be hosted through azure" and "OXPd runs in the clients azure subscription", which the tap did not say; and one server per site on the customer's network "is not inconsistent" with deploying through Azure in their tenant, so a server per site is not ruled out by his words. Whether a server per site is still part of phase 1, and in what role, is not settled by his words; the coordinator's reading: a hosting option and not the only shape. Against C-17, which the coordinator's commission of the design revision ties to the packaging of the server (the appliance and the installer): the register holds his tap, whose label is "Both equally". None of the seven messages names packaging: C-17 is reversed by no word of his, and that hosting through Azure changes it is the coordinator's reading. Question P6 has no decision card (the coordinator's statement, relayed); these three messages are its answer in his words. The revised documents apply them: decision D1 (`02:900`) and open question P-4 (`05:199`), which lists three shapes of Phase 1 and says that which one is meant is not said. Of C-29 and C-43 they name neither and reverse neither.

Message 6 (22:04:02). Settled by his words: "please go ahead and revise all docs and start building". NOT granted by those words, and still his: anything that creates Azure resources or costs money, and anything sent to HP or to any person. He names none of these in the message; the coordinator told him so on the board the same evening (the coordinator's statement, relayed), and the sentence of C-42, "Still his, unchanged by this tap: anything to HP or any person, any spend, any Azure resource", is lifted by no word of his. That "all docs" means the three design documents under `Design/` is the coordinator's reading; that revision was made on 2026-11-21 (`05:5`; <<C-A>> says where each answer now stands), and no result of any build is recorded here. It reverses no part of C-29, C-43, C-26 or C-17 by itself.

Message 7 (22:11:05). Settled by his words, and for these records only this: he asks to be emailed "the PDF and doc version of the docs when they are finished", and he says "continue building what you can". Nothing in it bears on the design. The coordinator's reading: "doc version" is a Word document, and "the docs" are the design documents revised on 2026-11-21; sending them is the coordinator's later work, and no sending is recorded here. NOT settled by his words: which documents, beyond that reading. It names no one but himself to receive anything, and it lifts nothing of what stays his after message 6: anything that creates Azure resources or costs money, and anything sent to HP or to any other person. It reverses no part of C-29, C-43, C-26 or C-17.
```
**Entry V** (only when slot V-WORDS reads CONFIRMED; B1816's text with four changes and one added quotation line):
```
[[TEXT CLAR-V]]
## <<C-V>>

Live board, view=tuesday, his two taps on decision cards of the coordinator's on the evening of 2026-11-21, the second with a note of his, verbatim, oldest first, each with the board's own time stamp; after each, the card's question and the chosen option's detail as the decision store prints them, with the store's time of the ruling. The board lines were printed from the live board and compared with the coordinator's reader of his board messages, which shows a run of blanks as one blank: the two blanks after his full stops in the note are the board's. The coordinator confirmed the two board lines against the board, and the four card lines against the decision store, and the coordinator's own answer (the last quotation line) against the coordinator's own chat store, before this entry was written.

> 2026-11-21T19:02:58.022000+11:00 [live] | Decision datasec-oxpd-lane-b-database-packages-1121: a — Fetch them once

> the card's question (the decision store; the coordinator's words): OXPd: may the build fetch the database packages from Microsoft's package site?

> option a, its detail (the decision store; ruled 2026-11-21T19:03:56.891246+11:00): Tuesday runs one supervised restore that downloads exactly those four packages (plus their dependencies) from nuget.org into the project cache, records the list and hashes, then seats work offline as before

> 2026-11-21T21:06:34.031000+11:00 [live] | Decision datasec-oxpd-firmware-unknown-value-callbacks-1121: b — Accept unknown values | note: how do we stay up to date with updates.  If we do not have current feeds, we need to accept.  HP has strict controls over what goes on the printer

> the card's question (the decision store; the coordinator's words): OXPd: when a printer's callback carries a value we do not know (after a firmware update), refuse it or accept it?

> option b, its detail (the decision store; ruled 2026-11-21T21:07:29.476335+11:00): Callbacks are read tolerantly: an unknown value is kept as 'unknown' and the rest of the callback is used (a later lane, needs its own design and review)

> 2026-11-21T21:07:43.940908+11:00 [the coordinator's answer to him on the board, from the coordinator's own chat store; the coordinator's words, not his] | Datasec/OXPd: got it, accept unknown values, and I have closed the card. My reading of your note: we cannot track every firmware update, and HP controls what reaches the printer, so a callback with a value we have never seen is read and kept, not refused. One safety line I am adding, mine: an unknown value never counts as success. For example an unknown sign-in result is treated as not signed in. The change belongs in the shared callback reader, not in tonight's adapter lane, so I am commissioning it as its own small lane. It lands after the adapter, with a review.

Tuesday's reading, nothing wider. Each tap is taken exactly as far as his words and the chosen option's detail go. The card's question, its other options and its default are the coordinator's and are named here only to show what he chose between. What the coordinator answered him is the coordinator's and is not recorded here, except the one addition named below. No design document is changed by this entry.

Ruling 1 (19:02:58 on the board, 19:03:56 in the decision store), option a: "Fetch them once". Settled by the option's detail, and no further: ONE supervised restore, run by the coordinator, that downloads exactly four packages and their dependencies from nuget.org into the project's package cache and records the list and hashes; after it, seats work offline "as before". The four, as the package-cache check of the lane's own kit lists them: `Microsoft.EntityFrameworkCore.SqlServer`, `Microsoft.EntityFrameworkCore.Sqlite`, `Microsoft.EntityFrameworkCore.Design` and `Npgsql.EntityFrameworkCore.PostgreSQL`. The card's default was option b, the device registry only and no download; he chose a. NOT changed by his tap, in the coordinator's reading of the words "then seats work offline as before": the project rule that a seat never downloads an SDK or a tool (`CLAUDE.md` line 83) stands for every seat and for every other package; the one fetch is the coordinator's, not a seat's. The lane it was asked for is the device registry and state database, which landed as pull request 12 (the project's history, written by the same pass that wrote this entry, records the merge). Since then, by the gate of the lane that asked for it (relayed from that gate's record list; the coordinator's and the gate's record, not his statement): one supervised package fetch was made on 2026-11-21 into the project's package cache, 95 versions before and 169 after (74 new), its record is `1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md`, and the gate compared all 74 downloaded files with the package site's own published hashes and found 74 of 74 equal.

Ruling 2 (21:06:34 on the board, 21:07:29 in the decision store), option b: "Accept unknown values", with his note, quoted whole in its quotation line above. Settled by the option's detail, and no further: "Callbacks are read tolerantly: an unknown value is kept as 'unknown' and the rest of the callback is used"; it is "a later lane, needs its own design and review". His note gives his reason, "If we do not have current feeds, we need to accept" and "HP has strict controls over what goes on the printer", and asks "how do we stay up to date with updates": that question is recorded as his and is not answered by this entry. The card's default was option a, keep refusing until the printer test; he chose b. What it changes: point F5 of the review of the OXPd 2 contracts (a whole inbound printer callback is refused when it carries a value that HP's inputs do not list, or a null), a design point that review left open for the product owner, is answered by this tap: the tolerant reading. NOT settled by his words: which values and which callbacks the tolerant reading covers, how an unknown value is held, whether a null is read the same way, and whether the inputs are also regenerated for each new beta; each belongs to the later lane's own design and review, and no result of that lane is recorded here. The coordinator's own addition, the coordinator's and not his (its answer to him on the board the same evening, quoted whole in the last quotation line above): "an unknown value never counts as success". In the coordinator's reading, the later lane that this ruling names is the one that landed on 2026-11-22 as pull request 14; the project's history records it, and no result of it is recorded here.
```
**Entry X** (only when slot X-WORDS reads CONFIRMED; its fills are cut from card print 1):
```
[[TEXT CLAR-X]]
## <<C-X>>

His tap of 2026-11-22 on a decision card of the coordinator's about the packages that Microsoft's standard SQL Server driver brings with it, ruled <<X-TS>> by the decision store's own print, which reached the records pass through the coordinator's stamp. The card's title, the card's default, and the option he chose with its label and its detail, verbatim from that print:

> title: <<X-TITLE>>

> the card's default (the coordinator's recommendation, not his word): <<X-DEFAULT>>

> the option he chose, its label: <<X-LABEL>>

> the option he chose, its detail: <<X-DETAIL>>

Tuesday's reading, nothing wider. He chose option a, which is also the card's default: the packages stay in the server's dependencies. Which packages, by the record list of the gate of the device registry and state database lane (relayed): the sign-in libraries that Microsoft.Data.SqlClient brings with it, Azure.Identity, Azure.Core, Microsoft.Identity.Client with its Broker, Extensions.Msal and NativeInterop, and the IdentityModel packages; the same gate measured that, of these, only Microsoft.Data.SqlClient was loaded in the data test process that generates the SQL Server script, and the option's detail says that they allow an Entra ID sign-in to a customer's SQL Server later, which is the card's own reading of the packages' documentation and was not run. That record list names the point as decided by nobody, the product owner's question, on the coordinator's card; in the coordinator's reading this tap answers it. NOT said by his tap: that any Entra ID sign-in to a customer's SQL Server is built or planned (the option's detail says only that the packages allow it later); and nothing about packages other than the ones the card names. The card's explanatory paragraph, its other two options and their details, and its note on his earlier ruling <<V-REF>> on fetching four database packages are the coordinator's and are not recorded here. The tap is his; every reading in this paragraph is the coordinator's. No design document is changed by this entry.
```
**Entry Y** (only when slot Y-WORDS reads CONFIRMED; its fills are cut from card print 2 and the board line above):
```
[[TEXT CLAR-Y]]
## <<C-Y>>

His tap of 2026-11-22 (the board's own stamp 10:35:55 by the coordinator's reader) on a decision card of the coordinator's about reading the printer's own answers tolerantly and accepting a new kind of result, with a note of his, verbatim; and, from the decision store's print, the card's title, the card's default, and the option he chose with its label and its detail, with the store's time of the ruling <<Y-TS>>. The board line keeps his typing, and the store's ruling field does not hold his note:

> 10:35 [live] | Decision datasec-oxpd-tolerant-device-answers-1122: a — Keep both strict for now | note: but make a note that this was a decision and can me changed if necessary

> title: <<Y-TITLE>>

> the card's default (the coordinator's recommendation, not his word): <<Y-DEFAULT>>

> the option he chose, its label: <<Y-LABEL>>

> the option he chose, its detail: <<Y-DETAIL>>

Tuesday's reading, nothing wider; his note is part of the ruling. (1) The printer's own answers to our questions stay strictly refused when they carry a value we do not know. (2) A callback that carries a new kind of result stays refused. Both are what the card's explanatory paragraph, which is the coordinator's and not recorded here, says the lane review measured as strict today, and the option's detail says that the point is revisited after Monday's printer test shows real traffic. (3) This is a recorded decision and not a fixed property of the design: in his words it can be changed if necessary, and he asked that this be noted; the card names Monday's printer test (2026-11-23, C-51) as the point to revisit it. NOT said by his words: when or whether it will be changed. It goes beyond nothing and leaves the parent ruling on callbacks (<<V-REF>>, option b, unknown values kept as unknown, a later lane) as it stands: that ruling named callbacks only, and this one rules on what it left out. The lane that built it landed as pull request 14 (main ca94ed96 at that landing; the project's history records it). The tap and the note are his; every reading in this paragraph is the coordinator's.
```
**Entry W** (only when slot W-NOTE reads WRITE; it carries no word of his):
```
[[TEXT CLAR-W]]
## <<C-W>>

Tuesday's note, nothing wider, written by the records pass of 2026-11-22. It carries no new word of the product owner's and corrects no word of his or of any earlier entry; a later entry names an earlier one, and this one does so for two forward references of <<C-T>> that have since been met.

First: message 2 of <<C-T>> says that the architecture and the plan of attack are `02` and `03` under `Design/` once revised, and that sending them is the coordinator's later work. They were revised on 2026-11-21 (`03` and `05` at 08:34, `02` at 08:37, by their file times), with his words of 2026-11-20 applied through a change list; `05:5`, `02:1132` and `03:594` say so. Whether the revised documents were sent to him is not recorded by this note, and <<C-T>> said no more than it said. Second: messages 5 and 6 of <<C-T>> say that whether the rule text states the exception for HP's files is stated in the project's history. The three lines of the project's `CLAUDE.md` that carry it (lines 7, 51 and 86) were changed by the records pass of 2026-11-21 (STATUS of that pass, 23:41 AEDT) and cite <<C-T>>; the history entry written by this pass records the change.

No sentence of <<C-R>>, <<C-T>> or <<C-U>> is false as written: the three were read for the words owed, later work and revision, and the only revision sentence is the one above. Entries <<C-A>> and the later ones of this pass are numbered in the order they were written, not in the order of their days: each says its own dates.
```
**The check of the quoted words** (run on each filled text before the write; a failure HOLDS that entry): every string between double quotation marks in a line of CLAR-S that is not a quotation line is a plain substring of one of its seven quotation lines or of a register line a CP row names (MEASURED-BY-DRAFTER: 30 strings, 0 outside); the same for CLAR-V against its seven quotation lines (10 strings, 0 outside, the tenth, "an unknown value never counts as success", found in the new quotation line); CLAR-X, CLAR-Y, CLAR-A-READ, CLAR-W and CLAR-B hold 0 such strings in a non-quotation line. A planted string with one letter changed must be refused. **Prior-work probes (Step 2), each without regard to case in the live register, a hit dropping that entry and STATUS naming the entry that carries it:** `Fetch them once` and `Accept unknown values` for V (0 and 0 at drafting); `hp files have been provided to us` is C-56 (1: it is the probe for `<<C-T>>`, not a drop); the plain string of his second message of entry S, `whichever is newer` (0 at drafting; control `Both equally` 1 line); `Keep them (standard driver)` for X (0); `Keep both strict for now` for Y (0); `Tuesday's note, nothing wider, written by the records pass of 2026-11-22` for W (0); the extract's line 12 as a plain string for A (0).

## PART 2: THE COMMENTS ON OXPD2-1 (slots JIRA, COMMENTS and FQ; after entry A is written; each one paragraph)
G3 is built by program: TEXT G3-HEAD, then the spans the FQ slot names in rising order, then TEXT G3-TAIL, joined by ONE blank. FQ-9, FQ-11, FQ-13 and FQ-16 are the four offered spans; B1816's FQ-7, FQ-8, FQ-10, FQ-12, FQ-14 and FQ-15 are NOT carried (FQ-7 is answered by his messages recorded in entry S; FQ-14 asks the same as the open question N-9, which stays owed item BL-9).
```
[[TEXT G1]]
BLUF. The product owner answered part of the questions document on 2026-11-20; his notes are recorded word for word as clarification <<C-A>> in the project's clarifications record. For three of his answers he asked that a follow-up question be added to this list. They are FQ-1 to FQ-5 below, one question each. <<OUTCOME>> Records note, <<WRITE-DATE>>; the split into single questions is the coordinator's and nothing wider is written here. On question A18 his words were: 'assume English for phase 1 but add to jira questions'. FQ-1 (from A18, for the Workpath team): on a printer running the current OneDrive and SharePoint apps, with the panel set to a language other than English, do the apps show their own screens in that language or in English? One photo of each app's first screen is enough. Until answered: English is assumed for phase 1, as he said. On question A19 his words were: 'I do not know and will ask workpath team.  Ask as a follow up question, add to jira questions'. FQ-2 (from A19, for the Workpath team; he will ask): has any shipped version of Mailflow shown quick messages on the printer panel? FQ-3 (from A19, for the Workpath team): if yes, in which version? Until answered: quick messages are left out, as the code has them switched off. On question A20 his words were: 'Ask as a follow up question for workpath team, add to jira questions'. FQ-4 (from A20, for the Workpath team): SharePoint 4.4.6: when scanning into a library, how many of the library's custom fields can be filled in at the panel? The manual says four; the source shows no cap. FQ-5 (from A20, for the Workpath team): OneDrive: the code has a sign-out confirmation screen that nobody has seen on a printer; does it appear on a printer? Nothing has been sent to the Workpath team or to any person by this note. [REC-FQ-ASKED-20NOV]
```
```
[[TEXT G2]]
BLUF. On question A12 of the questions document (was the earlier OXPd 1 code ever run on a physical printer) the product owner wrote on 2026-11-20 that he will check. It is kept here as FQ-6 so that it is not lost. <<OUTCOME>> Records note, <<WRITE-DATE>>; his notes are recorded word for word as clarification <<C-A>> in the project's clarifications record, and nothing wider is written here. His words on A12: 'I do not believe so but I will check'. FQ-6 (from A12, for the product owner, his own check): was the earlier OXPd 1 code ever run against a physical printer? Until answered the default of point OP-15 stands: emulator only, and nothing is treated as proven on hardware. [REC-FQ-OWNCHECK-20NOV]
```
```
[[TEXT G3-HEAD]]
BLUF. Follow-up questions raised by the product owner's answers of 2026-11-20 (clarification <<C-A>> in the project's clarifications record). They were proposed by the reader of his notes and are put on this list by the coordinator; none of them is his own request. <<OUTCOME>> Records note, <<WRITE-DATE>>.
```
```
[[TEXT FQ-9]]
FQ-9 (from P2, for the build team, from HP's documents): which OXPd generation can an HP MFP M577 run, and can it take FutureSmart 6 firmware at all? His answer makes the firmware version on the panel unnecessary; it does not say which generation the model runs.
```
```
[[TEXT FQ-11]]
FQ-11 (from A6, for the product owner or the Workpath team): is any customer running their own licence server today?
```
```
[[TEXT FQ-13]]
FQ-13 (from A18, for the product owner): does English for phase 1 cover every app, or only the OneDrive and SharePoint apps the question named?
```
```
[[TEXT FQ-16]]
FQ-16 (from A23, for the Workpath team): which printer models and firmware versions are in the lab he names?
```
```
[[TEXT G3-TAIL]]
Nothing has been sent to the product owner, to the Workpath team or to any person by this note. [REC-FQ-RAISED-20NOV]
```
```
[[TEXT G4]]
BLUF. Seven open product points from the independent reviews of the four libraries of wave 1 (card decoders, logging deny-list, print-protocol encoder, local secret store). All four libraries are now on main (pull requests 2 to 5); each point is still decided by nobody and is built one way today, as the review that raised it read it unless a sentence says otherwise, and each is a point for the Datasec product team or for a design decision. <<OUTCOME>> Records note, <<WRITE-DATE>>; words between single quotes are the first reviews' own, the rest is the coordinator's shortening. RP-1 (card decoders, WP1.3, for the Workpath product team): 'Which family of decoding routines produced the card strings that today's customers have stored': the older one (firmware before Android 12) or the newer one (Android 12 firmware)? The review's consequence: 'the two give different strings from the same card in 7 of 13 compared inputs', so cards enrolled under the other family would read as not known on every OXPd printer although they work on Workpath; 'Nobody is signed in as someone else by this; people are refused.' Built today: the older routines for the four enabled readers. RP-2 (local secret store, WP1.1): what sealed means for the Linux key file, and what performs the sealing; the design says the word and nothing more. Built today: an owner-only key file that nothing binds to the machine. RP-3 (local secret store, WP1.1; a packaging decision of WP5.1): which DPAPI-NG descriptor a stand-alone Windows server gets, and which the pair; the design names a domain group only for the pair. Built today: the library's call with no descriptor, which the hosted Windows build refused, so the Windows test skipped itself. RP-4 (logging, WP1.10): a named pipe in a folder the log scanner reads: with no writer the scan gives no result, and when a writer opens the pipe the scan ends with an exception and no result at all. The review's condition: 'closed before the scanner is given a shell or a pipeline entry point, or before any person is told to run it.' RP-5 (logging, WP1.10): the cost of the logging filter, measured by the second review on 230 sample events that hold no secret: '108 of 230 events lose at least one harmless value (47 in 100); 223 of 1210 values (18 in 100).' Is that cost acceptable, and should a replaced neighbour read differently from a replaced value? RP-6 (print-protocol encoder, WP4.2; a question for the Workpath team meanwhile): the first review found the reader refusing a whole packet that holds a group delimiter from 0x06 to 0x0f; after the fix round the reader takes a delimiter from 0x01 to 0x0f and keeps its tag (0x00 is still refused), so the answer decides only whether that tolerant reading is ever exercised. 'Does the print service ever answer with an attribute group other than operation, job, printer or unsupported' in practice? RP-7 (print-protocol encoder, WP4.2): there is no ceiling on fetches per document: 'an answer that gives one byte and then fails resets the retry count'. Should there be 'a ceiling on fetches or on elapsed time per document'? The reviews' record lists hold further questions for the Workpath team and questions only a printer can settle; they are not on this list yet. Nothing has been sent to the Workpath team or to any person by this note. [REC-REVIEW-POINTS-20NOV]
```
G1 and G2 are B1816's frozen spans, unchanged; their design checks are the rows of THE DESIGN POINTERS that the A8 report and `05:72`, `05:180` and `05:261` give (DERIVED by the drafter: `05:72` reads `Under default (a) they are left out.`, `05:261` holds both the sign-out screen and `in SharePoint 4.4.6`, `05:180` reads the OP-15 default). G4 is B1816's span re-derived: RP-3 and RP-6 and its opening are changed (named in the drafter's report); every other clause is as B1816 froze it, and THE QUOTE MAP and THE REVIEW MAP 3 are its checks.

## PART 3: THE RECORDS (slot RECORDS; three files, each rewritten ONCE by HOLD R, after the Jira step; every sentence that states a filing, a comment or a state is filled from what happened)
**3a. `5_Project_History/history.md`:** ONE entry inserted after line 2 (line 1 is `# OXPd 2: project history (newest at top)`, found once; line 2 is empty; line 3 must start with `## `), then one empty line. **THE HISTORY ENTRY** is these texts, one per line, joined by line feeds, in this order: H-HEAD; H-NOTES; (H-B-WRITTEN or H-B-HELD); (H-S-WRITTEN or H-S-HELD); H-R-DONE; H-T-DONE; H-RULES-DONE; (H-V-WRITTEN or H-V-HELD); (H-X-WRITTEN or H-X-HELD); (H-Y-WRITTEN or H-Y-HELD); H-W-WRITTEN only when entry W was written; H-LAND; H-LANE-SL; H-LANE-B; H-LANE-E; H-LANE-T; H-WAVE1; H-G4-LINE; H-SRC; H-JIRA; H-NOTDONE; H-FULL. `<<H-G4>>` is TEXT H-G4-WRITTEN when comment G4 was posted and read back (`<<G4-ID>>` its id), else TEXT H-G4-HELD. `<<JIRA-SHORT>>` by program from the poster's log: `one comment on OXPD2-1 for each of <the groups posted, by what they hold> (ids <ids>); no ticket created or moved; after: <n> issues, <d> Done`, or under JIRA DRY or COMMENTS NONE the words `nothing written to Jira by this pass`. A line that states a lane's landing is dropped (and STATUS says so) when its gating head or its review row HELD. **HOLD R2 applies to this file.**
```
[[TEXT H-HEAD]]
## <<WRITE-DATE>> <<HHMM>> AEDT: the records held on 2026-11-21 and the landings since: his notes and later words, the design revision that followed them, pull requests 3 to 14 and the reviews of four lanes (records seat)
```
```
[[TEXT H-NOTES]]
- The product owner's notes on the questions document (live board, 2026-11-20 21:04:30 AEDT; a Word file of 33 paragraphs) are in 1_Project_Definition/CLARIFICATIONS.md as <<C-A>>, word for word, with the coordinator's reading beside them. The three design documents were revised on 2026-11-21, between 08:34 and 08:37, to carry them; <<C-A>> says where each answer now stands. What that revision left open (the pulls P-1 to P-9 and the questions N-1 to N-18 of the documents, and question Q-B) is BACKLOG.md owed item <<OWED-9>>. No design document was changed by this pass.
```
```
[[TEXT H-B-WRITTEN]]
- His four later messages of the same evening (21:06:53, 21:07, 21:17:36 and 21:18:54) are <<C-B>>. Done on them by the coordinator's record (relayed): the OXPd 2 SDK beta folder and the OXPd library were copied from the NAS into 1_Project_Definition/Source_Documents/ (1514 files and 805564065 bytes; 31481 files and 6277940515 bytes). Counted again by this seat on the project's side: <<COUNT-RESULT>>. A further review of how the current solution operates and is deployed was commissioned: whether it is finished is not stated here, and no result of it is recorded.
```
```
[[TEXT H-B-HELD]]
- His four later messages of the same evening are NOT recorded by this pass (held: their wording was not confirmed against the board). The two copies into 1_Project_Definition/Source_Documents/ were counted by this seat on the project's side: <<COUNT-RESULT>>.
```
```
[[TEXT H-S-WRITTEN]]
- His seven later messages of the same evening (21:59:41 to 22:11:05) are <<C-S>>, word for word, each with what his words settle and what they leave open; every reading beside them is marked as the coordinator's. The seventh asks for the revised documents by email as a PDF and a doc version, in his words, and settles nothing of the design. No design document was changed by this pass. Still his after his word to start building: anything that creates Azure resources or costs money, and anything sent to HP or to any person (the coordinator's statement to him on the board, relayed).
```
```
[[TEXT H-S-HELD]]
- His seven later messages of the same evening (21:59:41 to 22:11:05) are NOT recorded by this pass (held: their wording was not confirmed against the board).
```
```
[[TEXT H-R-DONE]]
- His ruling on the logging lane after its second review is <<C-R>>, word for word with the chosen option's label and detail; it was written by the first, partial run of the records pass on 2026-11-21 (23:41 AEDT), not by this pass.
```
```
[[TEXT H-T-DONE]]
- His words of 2026-11-21 (seven lines of the live board and two typed in the coordinator's terminal) are <<C-T>>, and five lines of his of 2026-11-20 that the register did not hold are <<C-U>>, word for word, with the coordinator's reading beside them; both were written by the first, partial run on 2026-11-21 (23:41 AEDT). Among them: his word on the model (the latest Opus; Fable not used unless it is flagged as necessary) and his tap of 09:40 to keep HP's files in the repository.
```
```
[[TEXT H-RULES-DONE]]
- CLAUDE.md, text only, three lines changed in place by that first run (lines 7, 51 and 86; the line count unchanged): the model line names the newest Opus, with Fable only where a need for it is flagged first, and the rule on Source_Documents/ carries one exception, the files of HP's OXPd 2 specification that contracts/oxpd2/inputs.sha256 lists; each change cites <<C-T>>. This pass did not touch the file.
```
```
[[TEXT H-V-WRITTEN]]
- His two card rulings of the evening of 2026-11-21 are <<C-V>>, word for word with each chosen option's detail: one supervised fetch by the coordinator of four database packages and their dependencies into the project's package cache, after which seats work offline as before; and printer callbacks read tolerantly, an unknown value kept as unknown and the rest used, a later lane with its own design and review. The second answers point F5 of the review of the OXPd 2 contracts (BACKLOG.md, owed item <<OWED-9>>).
```
```
[[TEXT H-V-HELD]]
- His two card rulings of the evening of 2026-11-21 are NOT recorded by this pass (held: their wording was not confirmed against the board and the decision store).
```
```
[[TEXT H-X-WRITTEN]]
- His ruling of 2026-11-22 on the packages that Microsoft's standard SQL Server driver brings with it (keep them, the standard driver) is <<C-X>>, with the card's title, default and the chosen option's label and detail word for word. It answers, in the coordinator's reading, the question left open by the gate of the device registry lane (BACKLOG.md, owed item <<OWED-15>>).
```
```
[[TEXT H-X-HELD]]
- His ruling of 2026-11-22 on the packages that Microsoft's standard SQL Server driver brings with it is NOT recorded by this pass (held: its wording was not confirmed against the board and the decision store).
```
```
[[TEXT H-Y-WRITTEN]]
- His ruling of 2026-11-22 10:35:55 on the printer's own answers and on a new kind of result in a callback (both stay strictly refused, to be revisited after Monday's printer test, with his note that it is a decision and can be changed) is <<C-Y>>, word for word with his note. It leaves the ruling on callbacks <<V-REF>> as it stands; pull request 14 builds that one.
```
```
[[TEXT H-Y-HELD]]
- His ruling of 2026-11-22 10:35:55 on the printer's own answers and on a new kind of result is NOT recorded by this pass (held: its wording was not confirmed against the board and the decision store).
```
```
[[TEXT H-W-WRITTEN]]
- A note, <<C-W>>, names two forward references of <<C-T>> that have since been met (the revision of the design documents; the three lines of CLAUDE.md); it carries no word of his.
```
```
[[TEXT H-LAND]]
- The pull requests merged from 2026-11-21 (AEDT) to this seat's read by GET (<<ORIGIN-CLOCK>>), <<LANDED-COUNT>> in all: <<LANDED>>. Main at that read is <<MAIN-SHORT>>; <<PR-TOTAL>> pull requests exist in all, <<PR-OPEN>> open. For pull requests 3, 4, 5 and 6 the merged head is a head that a further review read GO WITH FINDINGS, and for pull requests 11, 12, 13 and 14 the merged head is the head that both readers of the lane's last round read GO WITH FINDINGS (the reviews' first lines, relayed); for every other one, gated: see that pull request's landing record. The record lists of the reviews and checks of 2026-11-20 to 2026-11-22 that no earlier owed item held, and the open questions not on the master list, are BACKLOG.md owed items <<OWED-5>> to <<OWED-19>>; none was filed as a ticket by this pass.
```
```
[[TEXT H-LANE-SL]]
- Lane SL, the secret store's list-and-remove members (WP1.1, pull request 11): round 1 read NO GO at a5ba020 on one Major (both readers' first lines, relayed); the fix round's head 8578d96c, the head that merged, read GO WITH FINDINGS by both round-2 readers. Nothing in the product calls the removal (the reviews' search of main at the gate read 0 lines). The readers' open points (a decryption fault that is not the record's own, an untyped fault under descriptor exhaustion that is already on main, two text points) and the lane's backlog lines are BACKLOG.md owed item <<OWED-13>>. Jira OXPD2-12 is not moved.
```
```
[[TEXT H-LANE-B]]
- Lane B, the device registry and the state database (WP1.1 remainder, pull request 12): both round-1 readers read GO WITH FINDINGS at c5a6ff84, the head that merged. One supervised package fetch was made first (95 to 169 versions in the project's package cache; the first reader found 74 of 74 downloaded files equal to the package site's published hashes). The limits the readers name (an audit entry that can be changed through a handler or an interceptor on the context; a lost duplicate race that spoils the next audit append; two fields not re-checked on read) are BACKLOG.md owed item <<OWED-14>>, and the runbook, fetch and test-gap lines are owed item <<OWED-15>>. Jira OXPD2-12 stays open.
```
```
[[TEXT H-LANE-E]]
- Lane E, the OXPd 2 adapter (WP1.2 in part, pull request 13): round 1 read NO GO at 523204dd on one Major, the callback credential cache after Forget or a rotation (both readers' first lines, relayed); the one fix commit 610bb7d2, the head that merged, read GO WITH FINDINGS by both round-2 readers, and the second reader found the Major closed. The named limits, the second reader's records, and the lane's departure from the plan (its own vault interface, the coordinator's decision as coordinator and not the product owner's) are BACKLOG.md owed item <<OWED-16>>. No ticket is moved by this pass.
```
```
[[TEXT H-LANE-T]]
- Lane T, the tolerant reading of printer callbacks (pull request 14, merged on 2026-11-22 AEDT): the first and second readers read GO WITH FINDINGS at b514a6b0, the head that merged, one commit and no fix round. In the coordinator's reading it is the later lane that his tap on unknown values in printer callbacks asks for (<<V-REF>>). The findings (one test gap, the rest records) and the points the kit sends to the records are BACKLOG.md owed items <<OWED-17>> and <<OWED-19>>; what a printer does with a refused or a tolerated callback is UNMEASURED until a printer test.
```
```
[[TEXT H-WAVE1]]
- The first four independent reviews of wave 1 (2026-11-20) each read NO GO at the head they read: the print-protocol encoder (WP4.2 part, head 9f4238a): one Major, closing the stream while a read is in flight does not stop that read. The card decoders (WP1.3, head 6499bd1): one Blocker and one Major, both in the assembler; the five decoding routines read exact against the source. The local secret store (WP1.1 part, head 42f926d): one Blocker by the rule of that review's own commission and one Major, both in the key ring. The logging deny-list (WP1.10, head 6bcd02e, the second review of that lane): NO GO on one finding, a code-scanning alert of high severity on one line of test code. Each library has since landed after a fix round and a later review (pull requests 2 to 5, the lines above and BACKLOG.md owed items <<OWED-5>>, <<OWED-10>>, <<OWED-11>> and <<OWED-12>>).
```
```
[[TEXT H-G4-WRITTEN]]
seven of them are on the master list (one comment on OXPD2-1, id <<G4-ID>>).
```
```
[[TEXT H-G4-HELD]]
none was put on the master list by this pass (held).
```
```
[[TEXT H-G4-LINE]]
- Open product points the reviews leave decided by nobody: <<H-G4>> The reviews' other open points and the four builders' first proposed record lines are listed by source in BACKLOG.md, owed item <<OWED-4>>; none was filed as a ticket by this pass.
```
```
[[TEXT H-SRC]]
- Source reads of the evening of 2026-11-20: reports A12 (the phone app's source and the older API's source) and B4 (the OXPd 2 SDK beta folder) are in 1_Project_Definition/Analysis/. Eight of A12's nine proposed corrections were applied by the design revision of 2026-11-21; the rest, and B4's, are not applied (BACKLOG.md, owed item <<OWED-2>>); two of their facts bear on work in flight (owed item <<OWED-3>>). Provenance rows for the two unpacked archives, the SDK folder and the library copy were added to PROVENANCE.md under Source_Documents/2026-11-20_from-product-owner/. No file under Source_Documents/ but that one was opened by this seat.
```
```
[[TEXT H-JIRA]]
- Jira (every choice here is the coordinator's; the product owner asked for the questions of A18, A19 and A20 to be added, in his own words in <<C-A>>): <<JIRA-SHORT>>
```
```
[[TEXT H-NOTDONE]]
- NOT done: no design document edited; no file of the code repository touched, nothing fetched or pushed; no ticket created or moved; no setting changed; nothing sent to HP, to the product team or to any person.
```
```
[[TEXT H-FULL]]
- Full record: 1_Project_Definition/Briefs/2026-11-22_B1887_STATUS.md.
```
**3b. `BACKLOG.md`:** the TEXTs BL-2 to BL-19 that are not held, joined by line feeds in the order of THE OWED ITEMS, inserted before the empty line that stands in front of the heading `## The no-hardware work packages and their Jira keys` (found once; the line before that empty line starts with `    - Discovered:`). **THE OWED ITEMS, in insertion order:** BL-2, BL-3, BL-4, BL-5, BL-6, BL-7, BL-8, BL-9, BL-10, BL-11, BL-12, BL-13, BL-14, BL-15, BL-16, BL-17, BL-18, BL-19. `<<BL4-G4>>` is TEXT BL4-G4-WRITTEN or BL4-G4-HELD as for the history; `<<BL4-JIRA>>` is `OXPD2-1 (comment <id>)` or `none`; `<<BL9-F5>>` is TEXT BL9-F5-WRITTEN when entry V was written, else TEXT BL9-F5-HELD (replaced BEFORE `<<C-V>>`). At drafting the file has 215 line feeds and 30 owed items. BL-2 and BL-3 rest on THE REPORT POINTERS and on the B1817 marks: **before BL-2 is written, count by program that each of the row ids R4-10 to R4-23 appears as `B1817 R4-nn` or `B1817 / R4-nn` in at least one of `02`, `03`, `05` (MEASURED-BY-DRAFTER: 14 of 14), and that the change list names none of S-2, S-3, S-5, S-6, S-9, S-12 (0 each; control: R4-06 names B4)**; a failure HOLDS BL-2. BL-18 is gated by THE LANE G CHECK.
```
[[TEXT BL-2]]
<<OWED-2>>. - [ ] Corrections proposed by the two source reads of the evening of 2026-11-20: eight of the nine of report A12 applied by the design revision, the rest not applied
    - Where: `1_Project_Definition/Analysis/A12_phone-app-and-legacy-keycloak-api-source.md`, section 8 (lines 145 to 153); `1_Project_Definition/Analysis/B4_oxpd2-sdk-beta10-nas-folder.md`, section 5 (lines 98 to 144); the change list `1_Project_Definition/Review/B1817_DESIGN-CHANGE-LIST_2026-11-20.md`
    - Symptom: Report A12 proposes nine corrections to the design as it stood on 2026-11-20 (its line numbers are those of the documents before the revision). The design revision of 2026-11-21 applied eight of them, each under its row id: (1) the older API's source was received and read (R4-14); (2) point OP-11 is answered from source (R4-12, R4-13); (3) the phone app's source is in hand (R4-10, R4-11, R4-21, R4-22); (4) the phone's message has seven fields and its email field carries the sign-in name (R4-15); (5) capturing the phone's message is no longer an open input (R4-19, R4-20); (6) the phone app's source holds the same key literal as the Workpath source (R4-16, R4-17); (7) each phone a user signs in on is a separate card id (R4-18); (9) the superseded line (R4-23). NOT applied: (8), the scope the phone requests in report A9 line 261, which is a report and not a design document. Report B4 gives no numbered list; its rows whose verdict settles, qualifies or contradicts a line of the design are S-2, S-3, S-5, S-6, S-9 and S-12 (design lines of the documents before the revision: `02:362`, `02:368`, `03:154`, `02:563`, `02:804`, `02:379`, `02:1029`, `03:54`, `02:452` and `02:458`); the change list names report B4 only at its section 6 (rows R4-06 and R4-07) and at no S row, so these six are NOT applied, and their lines must be re-derived by fragment before use
    - Why deferred: each is a reader's proposal from source and from HP's specification, not run on a printer, a simulator or a tenant; the design and report A9 are corrected by a pass of their own
    - Source: the two reports, written on 2026-11-20 by the readers the coordinator commissioned; neither has had a second reader; the change list and the B1817 marks of the three design documents, counted by the records pass of 2026-11-22
    - Jira: none
    - Discovered: 2026-11-20 by the two source reads
```
```
[[TEXT BL-3]]
<<OWED-3>>. - [ ] Two facts from the source read of the SDK folder that bear on work in flight
    - Where: the card decoders' assembler of work package WP1.3 (landed as pull request 3) and the OXPd 2 adapter's callback handling with its stale-read guard (landed as pull request 13); the design's stale-tap wording (`02:564`)
    - Symptom: read in HP's specification, not run: (1) the read event's sequence number starts at zero for each target and operation, and the data is delivered in order (report B4, rows S-2 and S-3, lines 99 and 100), where the decoder kit held that a loss before the first event cannot be seen; whether the number grows by exactly 1 stays unmeasured (row S-4, line 101). (2) The read event carries no time of reading (row S-5, line 102), against the design's wording that the adapter discards a read that arrives "more than N seconds after it was read" (`02:564`): the guard has to rest on arrival time. The reviews of the two landed lanes carry their own open questions on stale and repeated events (owed items <<OWED-12>> and <<OWED-16>>); whether the landed code uses these two facts is not read by this pass
    - Why deferred: each needs a decision in the kit of the lane it touches, and both need a printer or the simulator to confirm
    - Source: `1_Project_Definition/Analysis/B4_oxpd2-sdk-beta10-nas-folder.md`, section 5.1
    - Jira: none
    - Discovered: 2026-11-20 by the source read of the SDK folder
```
```
[[TEXT BL-4]]
<<OWED-4>>. - [ ] Open points of the first reviews of wave 1 and the four builders' first proposed record lines of 2026-11-20, not filed
    - Where: the STATUS files of the four build seats in `1_Project_Definition/Briefs/` (`2026-11-20_B1786_STATUS.md`, sections FOR RECORDS and FOR TUESDAY; `2026-11-20_B1788_STATUS.md`, sections RECORDS PROPOSED and FOR TUESDAY; `2026-11-20_B1789_STATUS.md`, section FOR TUESDAY; `2026-11-20_B1798_STATUS.md`, section FOR TUESDAY) and the record list of each lane's first independent review
    - Symptom: nothing of these lists is written into `SETUP_RUNBOOK.md`, the repository's README or a ticket: the runbook lines the builders propose (one summary line for two test projects; the wave's heavy lock; the compiler server that stays running; the dotnet environment), the one README pass after the wave (the layout and the reserved names), the backlog lines of each lane, the questions for the Workpath team (the print protocol, the cards) and the questions only a printer can settle. <<BL4-G4>>
    - Why deferred: each list was true at the head its first review read; the four libraries have since landed (pull requests 2 to 5) and the record lists of the later reviews are owed items <<OWED-5>>, <<OWED-10>>, <<OWED-11>> and <<OWED-12>>; this pass does not refile the first lists
    - Source: the four independent reviews of wave 1, 2026-11-20 (each one's record list), and the four STATUS files named above
    - Jira: <<BL4-JIRA>>
    - Discovered: 2026-11-20 by the four independent reviews of wave 1
```
```
[[TEXT BL4-G4-WRITTEN]]
Seven product points of the reviews are on the master list (Jira OXPD2-1, comment <<G4-ID>>)
```
```
[[TEXT BL4-G4-HELD]]
Seven product points of the reviews are named in the kit of the records pass of the evening and are not yet on the master list
```
```
[[TEXT BL-5]]
<<OWED-5>>. - [ ] The local secret store after its landing: the second review's eight Minor findings, the builder's backlog lines and six open points, not yet filed
    - Where: `src/Datasec.Suite.Secrets` on main (pull request 5) and its tests; the store's README, its Limits section
    - Symptom: Minor, none blocking, each decided by nobody: N1 on Windows a key planted under DPAPI-NG to a rule the store's account opens is accepted and can become the write key at the next start (DERIVED; UNMEASURED on Windows); N2 `RotateKey` can throw after its new key is written; N3 a partition folder that is a link is not refused; N4 a hard link in `keys/` has its target's mode set to 600 at the start; N5 the record folder is link-checked at the start only; N6 a clone of the store's own entry under a new id with the newest date becomes the write key at the next start; N7 cells owed (a revocation alone with no record; the guard with a mixed set of records); N8 a ring with 90-day keys stops writes when one expires (no such ring exists). The builder's nine backlog lines, each kept by the review (among them: `Rewrap` names no record it failed on and `ListNames` fails whole on one unreadable record; the value cipher; a lock between processes over one partition; temporary files of an interrupted write never removed). Six open points for the master list, not posted by this pass: the key lifetime; the value limit of 1 MiB and the words a caller reads; the value cipher; the DPAPI-NG descriptor and who may write the key folder on Windows; what sealed means for the Linux key file; rollback
    - Why deferred: each is a follow-up the review graded Minor or a product point; none blocks the landed library, and the server does not use the store yet
    - Source: the second review of the store, 2026-11-21 (GO WITH FINDINGS at bf1a4a2), its record list sections 3 to 5, and the check of its merge commit (GO WITH FINDINGS at 9826559, the head that merged)
    - Jira: none
    - Discovered: 2026-11-21 by the second review of the local secret store
```
```
[[TEXT BL-6]]
<<OWED-6>>. - [ ] Three record points of the check of the secret store's merge commit, for the kits that follow
    - Where: the proof programs and landing texts of the build kits (no file of the code repository)
    - Symptom: R1 the builder's identity proof P8 compares the commit with the clone's own config and its control compares a constant with that config, so it cannot fail on a wrong identity (the commit's identity was right by the check's own compare with the checkout; the check of the print protocol's resolution commit found the same); R2 the builder's local neutral-scan line counted 327 objects against 323 hosted, four unreachable local objects of the trial and the merge, and a fresh clone counted 323; R3 the pull request body said review twice and coordinator once, and the squash body coordinator once, carried from the second verdict's texts; whether that word was changed before the merge was not read by this pass
    - Why deferred: records and process points, none in the product code; each is for the next kit's proof program or text scan
    - Source: the check of the store's merge commit, 2026-11-21, its findings table rows R1 to R3 and its record list section 8
    - Jira: none
    - Discovered: 2026-11-21 by the check of the local secret store's merge commit
```
```
[[TEXT BL-7]]
<<OWED-7>>. - [ ] HP's OXPd 2 contracts and clients after their landing: the review's follow-ups, not yet filed
    - Where: `contracts/oxpd2/`, `src/Datasec.Suite.Adapters.Oxpd2`, `tests/Datasec.Suite.Contracts.Tests` and `build/repo_rules.py` on main (pull request 6); `SETUP_RUNBOOK.md`; the repository's README; Jira `OXPD2-9`
    - Symptom: F4 the kit's run of rule R5 over `Source_Documents/` hashed the files under the SDK's `tools/certificates/` (HP's development root CA private key), against the kit's own line never to hash them (8 files, DERIVED by subtraction; nothing printed or copied): later kits prune that folder, or the R5 follow-up excludes it. The R5 follow-up: exempt exactly the files that `contracts/oxpd2/inputs.sha256` lists, matched by path and hash, read from the list. The runbook gains the regeneration test and how to regenerate, the R5 exception for those files, the local restore form under the closed proxy, and the test temp folders that accumulate. The one README pass after the wave gains `contracts/oxpd2/`, `src/Datasec.Suite.Adapters.Oxpd2` and `tests/Datasec.Suite.Contracts.Tests`. Backlog: F1 four public lists hand out their arrays; F2 an overflow at a caller limit of the largest integer; F3 string length in Unicode scalar values; F6 an `IOException` from a body stream passes out of a client method beside `HttpRequestException`, and the strict reading of N11 applies only to error bodies, which the clients do not parse; D11 test temp folders removed. F7 the device-answer models carry HP's credential-shaped fields (the `BearerAuthorization` family, a solution-token operation): the logging deny-list and any store must cover them when a later work package consumes the clients. What the real customer gateway answers to a body with no realm is UNMEASURED. `OXPD2-9` stays open (contract tests against simulator responses; the 1.x stubs); its second half is answered in the coordinator's reading by his tap of 2026-11-21 09:40, and the ticket is not written by this pass. F5, a design point for the product owner, is carried in owed item <<OWED-9>>
    - Why deferred: follow-ups and kit rules, none blocking; the runbook and the README are written by passes of their own
    - Source: the review of the OXPd 2 contracts lane, 2026-11-21 (GO WITH FINDINGS at 48120e5, the head that merged), its findings F4 to F7 and its record list items 3 to 8
    - Jira: none
    - Discovered: 2026-11-21 by the review of the OXPd 2 contracts lane
```
```
[[TEXT BL-8]]
<<OWED-8>>. - [ ] The secret store could not list past an unreadable record: closed by pull request 11 for two new members; `ListNames()` keeps its behaviour
    - Where: `src/Datasec.Suite.Secrets` (the store's listing) and the token broker of work package WP1.5 (landed as pull request 9)
    - Symptom: one corrupt or foreign record file makes `ListNames()` throw, and record files are named by a hash of the name, so a consumer cannot learn which record is bad; the token broker therefore refuses to start while such a record is in its partition (fail closed: the coordinator's decision of 2026-11-21 on the broker's test R03, not the product owner's). Lane SL (pull request 11, landed 2026-11-21) added `ListAll`, which lists the records it cannot read, and `DeleteUnreadable`, which removes one only when its bytes were read and fail as a record; nothing in the product calls either at the gate's main, and whether the broker will is not read by this pass. The lane's remaining points are owed item <<OWED-13>>
    - Why deferred: wiring the broker to the new members is a change of its own with its own review
    - Source: the coordinator's answer of 2026-11-21 to the token broker's build (its point 3, alternative C), relayed; the two round-2 reviews of lane SL, 2026-11-21 (GO WITH FINDINGS at 8578d96)
    - Jira: none
    - Discovered: 2026-11-21 by the token broker's build
```
```
[[TEXT BL-9]]
<<OWED-9>>. - [ ] Open questions for the product owner that are not on the master list OXPD2-1
    - Where: Jira `OXPD2-1`, the master list; the design documents' own open questions, the pulls P-1 to P-9 and the questions N-3, N-13 to N-15, N-17 and N-18 in `1_Project_Definition/Design/05_readiness-to-build.md` (lines 188 to 215), and N-1 to N-18 with their defaults in `1_Project_Definition/Review/B1817_DESIGN-CHANGE-LIST_2026-11-20.md` (lines 282 to 299); the coordinator's wave-2 plan of 2026-11-21, question Q-B
    - Symptom: none of P-1 to P-9 and N-1 to N-18 is on the master list (the revised `05` says they go there through the coordinator), and neither is Q-B, "May Datasec's own app strings under `Source_Documents/` be copied to seed the UI languages?" (default meanwhile: the rule stands, nothing copied; in the coordinator's reading the tap of 2026-11-21 09:40 on HP's files does not answer it). The reader's follow-up FQ-14 (is the deployment tool a new app before the MVP) is the same point as N-9 (which tool, and in what form) and is not posted separately. The second printer test (spike S14) waits for his word and for an Azure resource. Also asked, F5 of the review of the OXPd 2 contracts: an enum value that HP's inputs do not list, or a JSON null for an optional property, makes a whole inbound printer callback refused; on a firmware newer than the Beta 10 inputs, job statistics or a sign-in prompt result could be refused until the inputs are regenerated, and what a printer does with a refused callback is UNMEASURED. Question: a tolerant reading per site (an unknown marker), or a regeneration on every beta with a contract diff that fails the build? Built when the review read it: refused. <<BL9-F5>>
    - Why deferred: a comment on the master list is a body the coordinator approves word for word, and this pass posts only the four comments its kit froze
    - Source: the design change list of 2026-11-20, its table of open questions; the revised `05`; the coordinator's wave-2 plan of 2026-11-21, its question Q-B and its finding that the master list holds none of them (relayed); the review of the OXPd 2 contracts lane, 2026-11-21, its finding F5
    - Jira: none
    - Discovered: 2026-11-21 by the coordinator's wave-2 plan
```
```
[[TEXT BL9-F5-WRITTEN]]
F5 is no longer open: the product owner answered it on 2026-11-21 (<<C-V>>, his tap and note on a decision card): unknown values are accepted and read tolerantly, a later lane with its own design and review; that lane landed as pull request 14 on 2026-11-22 (owed item <<OWED-17>>); the question above is kept as it was asked. Every other question here is decided by nobody
```
```
[[TEXT BL9-F5-HELD]]
A ruling of 2026-11-21 on F5 is not recorded by this pass (held); every other question here is decided by nobody
```
```
[[TEXT BL-10]]
<<OWED-10>>. - [ ] The logging deny-list after its landing: the third check's record points, not yet filed
    - Where: `src/Datasec.Suite.Logging` on main (pull request 2) and its tests; the kits of the lanes that log; Jira `OXPD2-15`
    - Symptom: `OXPD2-15` stays open after the landing for the scan of logs from a real sign-in (exit test E1.8), which needs a printer; still owed: the host wired to the library, and the one README pass after the wave. A local C# code scan that gives 0 results does not by itself prove 0 hosted results (53 logger calls in the three test files had no resolved target locally): print the scanner's list of sources, and treat every source whose value something reads as a risk. The rule for the kits of the lanes that log: no method call whose argument has a constant value holding a credential word (password, passwd and the other words the check names), when the call's result can reach a logger, a file write or a trace call; a named constant and a collection-initialiser entry count as such. The test maker at `KeyValueShapeTests.cs:95` is one edit away from such a source
    - Why deferred: records and kit rules; none blocks the landed library
    - Source: the third check of the logging lane, 2026-11-20 (GO WITH FINDINGS at afc4e19), its record list sections 1 to 4
    - Jira: none
    - Discovered: 2026-11-20 by the third check of the logging lane
```
```
[[TEXT BL-11]]
<<OWED-11>>. - [ ] The print-protocol reader and writer after their landing: the fix round's and the resolution commit's record points, not yet filed
    - Where: `src/Datasec.Suite.UniversalPrint` on main (pull request 4) and its tests; the kit of the transport lane, the stream's first caller; Jira `OXPD2-18`
    - Symptom: WP4.2 and `OXPD2-18` stay open after the landing; the server does not reference the library; every byte fixture is provisional until a capture exists. One Minor: the stated behaviour that the caller's own cancellation leaves as the cancellation exception has no test that can fail. Records: a close can wait behind a fetch, delay or jitter call and in one shape deadlock (the transport lane's fetch function returns its task at once and never blocks); a close while the jitter function runs lets the wait start (up to about 8.3 seconds after the close); a body whose own disposal throws makes the close throw; `IppTag.IsKnownGroup` changed its public answer for 0x06 to 0x0f (for the change log of the first release). Eight open rulings decided by nobody, among them no ceiling on fetches per document and the exception types of a close and of a second read; the twelve questions for the Workpath team carried from the first review. The resolution commit: the identity proof P8 cannot fail on a wrong identity; a gate that publishes behind the closed proxy passes `-p:NuGetAudit=false` to the publish as well
    - Why deferred: records and kit rules; none blocks the landed library
    - Source: the review of the fix round, 2026-11-21 (GO WITH FINDINGS at ec75619), its record list sections 1 to 6, and the check of the resolution commit (GO WITH FINDINGS at ce38c25, the head that merged), its record list section 2
    - Jira: none
    - Discovered: 2026-11-21 by the review of the fix round of the print-protocol reader and writer
```
```
[[TEXT BL-12]]
<<OWED-12>>. - [ ] The card decoders after their landing: the second review's record points, not yet filed
    - Where: `src/Datasec.Suite.Cards` on main (pull request 3) and its tests; the kits of the adapters that call the assembler; Jira `OXPD2-13`
    - Symptom: WP1.3, `OXPD2-13` and exit test E1.3 stay open after the landing (the comparison with real readers and the golden files of spike S3); every golden value is provisional; the server does not reference the library and nothing reads a real reader. Minors for the records: one wrong time value on two consecutive calls ends the discarding early and gives the tail of a refused read as a card; three behaviours of the new mechanism have no cell that can fail; one wrong time far ahead in the middle of a read gives two refusals for one tap; chatter at one window or slower gives one refusal per event; a held event that gives no character is counted; a dropped repeat of an old event with bytes keeps the reader deaf. Two questions only a printer can settle: does a printer ever re-send a stale event seconds later, and how long does one card read take on each reader, first event to last (a read of one second or more is refused). Three open rulings decided by nobody: what a dropped repeat does to the quiet window; which time before a step counts in a series; one message per tap after two refusals for one tap. For the adapter kits: the caller takes the time at each call from a monotonic clock under the lock that serialises the calls, and calls Tick at least once per window
    - Why deferred: records, questions and kit rules; none blocks the landed library
    - Source: the second review of the card decoders, 2026-11-21 (GO WITH FINDINGS at 9fe5356, the head that merged), its record list sections 1 to 7
    - Jira: none
    - Discovered: 2026-11-21 by the second review of the card decoders
```
```
[[TEXT BL-13]]
<<OWED-13>>. - [ ] The secret store's list-and-remove members after their landing: the readers' open points and the lane's backlog lines, not yet filed
    - Where: `src/Datasec.Suite.Secrets` on main (pull request 11): `ListAll`, `DeleteUnreadable`, `ISecretStoreInventory`; `tests/Datasec.Suite.Secrets.Tests/InventoryTests.cs`; the store's README; `SETUP_RUNBOOK.md` (check table); Jira `OXPD2-12`
    - Symptom: (1) who may call `DeleteUnreadable` in the product is open, and nothing calls it. (2) D22 (a), graded a Minor records limit by the second reader: a decryption failure that is not the record's own reads as a record that does not open, and the record is removed; measured on Unix only (the decryptor ran 2 times at the store's open and 0 times at the removal); a key-ring reload after the library's cache expires, the same under DPAPI-NG on Windows, and a process fault inside the decryption are DERIVED and UNMEASURED. The first reader's smallest guard: when the record names a key that is active in the verified ring, refuse the removal unless the decryption failed as an authentication failure; the second reader's, before any caller is wired: require that the record's key id is a key of this store's ring that is not revoked and that a protect and unprotect round trip of a probe value succeeds under the current key, else `StorageFailed` and nothing removed (about 10 lines). (3) The second reader's F1 (Minor, records, store-wide, already on main in the frozen `SecretRecord.cs`): a process with no free descriptor and a JSON decoder not yet loaded throws an untyped `FileNotFoundException` from every read member, `TryGet` and `ListNames` included, and the runtime keeps that failed load until restart; nothing is removed. Fix shape for a later store kit: type a runtime fault inside `Decode` (`FileNotFoundException`, `FileLoadException`, `TypeInitializationException`) as `StorageFailed`, never as `UnreadableRecord` (typed so, the kept failure would make every record unreadable and `DeleteUnreadable` would remove them all); optionally warm the decoder when the store opens. (4) The second reader's F2 (text): the README's `DeleteUnreadable` sentence lists no file descriptor left under `StorageFailed`; with the ring check first it is `KeyNotAvailable`. (5) A second process over the partition writing without changing the key ring can still race the removal (named in the README; one process per partition is assumed); `EIO` and `ENFILE` are by source reading only, `EMFILE` is measured. (6) The round-1 line that listed a record file of mode 000 among the records the removal destroys is superseded: such a file is now refused with `StorageFailed` and left for an operator. Runbook: local totals 920 at the head alone and 1191 merged with main 977cbeb2 (rules 295 and 370 files); the descriptor cell lowers the process's open-file limit, runs alone in its own collection and does nothing on Windows
    - Why deferred: each is a later store kit's work or a records line; none blocks the landed members, which nothing calls
    - Source: the round-2 reviews of lane SL, 2026-11-21 (GO WITH FINDINGS at 8578d96 by both readers): the first reader's record list, and the second reader's findings F1 to F3 and its D22 (a) grading
    - Jira: none
    - Discovered: 2026-11-21 by the two round-2 reviews of lane SL
```
```
[[TEXT BL-14]]
<<OWED-14>>. - [ ] The device registry and state database after their landing: the limits the two readers name, for a later data kit
    - Where: `src/Datasec.Suite.Data` and `src/Datasec.Suite.Devices` on main (pull request 12) and their READMEs; `tests/Datasec.Suite.Data.Tests` and `tests/Datasec.Suite.Devices.Tests`
    - Symptom: (1) The second reader's F1 (Minor; text false as written): the Data README and decision D15 say that `SaveChanges` refuses an audit entry that is modified or removed and saves nothing; code that holds the context can still change entries after the guard, through the context's `SavingChanges` event or a `SaveChangesInterceptor` in its options (measured: no exception, all 3 rows' actor id changed). Name the limit as the other limits are named (any code holding the context: `ExecuteUpdate`, `ExecuteDelete`, raw SQL, a `SavingChanges` handler, a save interceptor) or close it, for example by refusing in a `ChangeTracker.StateChanged` handler; if "through the library" is read as any use of `SuiteDbContext`, this is the one item that would be a Major. (2) The second reader's F3 and the first reader's F1 (Minor, for a later data kit): the registry and the audit log share ONE scoped context; when `AddAsync` loses a duplicate race (another writer inserts the key between the check and the save) it throws an untyped `DbUpdateException`, not `SuiteDataException DuplicateDevice`, and the failed entity stays tracked, so the next audit append on the same context fails too and the audit row of that failure is never written (simulated with an interceptor; the database key still holds one row). Fix: map the key's `DbUpdateException` to `DuplicateDevice` and clear the tracker, as the stale-update path does, or document that the audit log needs its own context. (3) The first reader's F2: a capability snapshot holding a lone surrogate escapes as `ArgumentException` (refused, nothing held). (4) The first reader's F3 and the second reader's F2: firmware and model are returned by `FindAsync` and `ListAsync` without re-checking their rule (0 of 6 stored shapes failed closed), and `UpdateAsync` of such a `Device` is then refused; fix: the rule check inside the mapping of a stored device, plus a fail-closed row for each. The text rule is printable ASCII only, so a printer that reports a model or firmware with any other character could not be registered at all: what HP devices report is UNMEASURED. (5) The first reader's F4 and the second reader's F4: the clock result's offset is truncated to whole seconds, so `outside 300` can be stored beside a 300-second tolerance (300.5 s), and above about 34 years a value can be one too high; the outcome is always right; fix `difference.Ticks / TimeSpan.TicksPerSecond` and one README line. (6) A record, not a finding: the clock check reads the server's time before it awaits the device source, so a slow source adds its own latency to the offset, and no time bound exists for a source that never answers (for the onboarding wiring, WP1.11)
    - Why deferred: each is a later data kit's work or a README line, graded Minor or records by both readers; none blocks the landed libraries
    - Source: the first and second readers' verdicts on the device registry and state database lane, 2026-11-21 (GO WITH FINDINGS at c5a6ff8 by both)
    - Jira: none
    - Discovered: 2026-11-21 by the two readers of the device registry and state database lane
```
```
[[TEXT BL-15]]
<<OWED-15>>. - [ ] The device registry and state database after their landing: the fetch record, the runbook and backlog lines, the open questions, not yet filed
    - Where: `SETUP_RUNBOOK.md` (line 50, restores, and its check table); the project's package cache and the record program of the fetch; `1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md`; Jira `OXPD2-12`
    - Symptom: (1) Runbook line 50 (restores) is no longer true as written: on 2026-11-21 ONE supervised fetch from the package site went into the project's package cache (95 versions before, 169 after: 74 new, 59 reached through the lock files and 15 resolver lower bounds that no lock file names); every later restore ran offline; the first reader compared all 74 record file hashes with the package site's published hashes, 74 of 74 equal, and the 149 lock-file entries with the cache's metadata, 149 of 149; a runbook line for the NEXT fetch should name that check. (2) The 15 lower bounds stay in the cache (the coordinator's answer): inert, but the record program's reachability rule reads lock files only; fix the rule before a next fetch. (3) Test gaps the first reader's own probes caught and the lane's suite did not: a lookup by a serial whose case differs from the key (`Find`, `Record*`, `Remove`); the read-side check that the stored key equals the upper-cased stored serial; a snapshot bound counted in UTF-16 characters instead of UTF-8 bytes; and, from the second reader, the clock offset truncated on exact seconds and a stored clock outcome of unknown text read as unknown. (4) Left of WP1.1 after this lane: the device clock read itself (an OXPd 2 call, with the clients), the reference time source (an NTP client), the sessions, jobs and Universal Print state tables, the host wiring and migrate-at-start, a run of both migration sets against real databases, database-level append-only enforcement for the audit log, the defect catalogue's content, the Key Vault provider; Jira `OXPD2-12` stays open. (5) Open questions of the first reader's list: a run of both migration sets against a real PostgreSQL 16 and a real SQL Server (a CI change); database-level append-only enforcement for the audit log (grants or triggers); how the next lane that needs a package gets it; and whether Microsoft.Data.SqlClient's sign-in libraries may stay in the server's graph, which his tap of 2026-11-22 (<<C-X>>) answers in the coordinator's reading. (6) The seat's note: decision C-24 (store a device administrator password encrypted) stands beside OQ-2 (discarded after install, OXPd 2): the lane keeps an `oxpd1-admin-password` reference kind and no OXPd 2 kind. (7) Text: the lane's STATUS section on migrations still names the first scaffold's id `20261121102614_Initial`; the committed id is `20261121105111_Initial`
    - Why deferred: runbook and backlog lines are written by passes of their own; the questions are decided by nobody
    - Source: the first reader's FOR RECORDS list on the device registry and state database lane, 2026-11-21, and its fetch record check (GO WITH FINDINGS at c5a6ff8)
    - Jira: none
    - Discovered: 2026-11-21 by the first reader of the device registry and state database lane
```
```
[[TEXT BL-16]]
<<OWED-16>>. - [ ] The OXPd 2 adapter after its landing: the named limits, the second reader's records and the lane's departure from the plan, not yet filed
    - Where: `src/Datasec.Suite.Adapters.Oxpd2` (`Device/`, `Callbacks/`) and `tests/Datasec.Suite.Adapters.Oxpd2.Tests` on main (pull request 13) and the adapter's README; the project's deviation register draft (WP6.7), not edited by this pass
    - Symptom: Landed: a per-device solution-token holder (lazy refresh and refresh on a 401, one retry, `NeedsRepair` after a second 401, rotation written before use, single flight per serial, `Forget` during a refresh stores nothing) and the callback credentials (32 random bytes, only the SHA-256 kept, fixed-time compare, five handled callbacks, 14 outcomes); local totals 1234 to 1248 (57 lane tests). Named limits, to state in the README (today only the timing one is there): (1) `StoreRefreshValue` during a refresh is followed by that refresh's result, and a request that waited on it gets the same result (measured: both end `NoRefreshValue` though the vault already holds the new value; the next request succeeds with one more endpoint call); (2) an access value handed out before `Forget` may still be sent once by the request that holds it (DERIVED); (3) the vault call of a rotation and of `Forget` runs under the serial's lock, so a slow vault holds that serial's callers, and `Dispose` can hold every other serial's lookup behind a slow vault call (DERIVED, UNMEASURED with a real store); (4) the timing of the enrolled-serial vault lookup (in the README); (5) the Issue rotation cell is held by two mechanisms, so no single mutant of its generation bump reddens a cell; (6) a credential digest read from the vault but not cached, and a wrong-length read, are dropped unzeroed (the second reader agrees it is Minor or less: a SHA-256 of a random value, not the credential); (7) a refresh answered after `RefreshTimeout` is discarded with any rotated refresh value, and an endpoint that ignores its token overlaps the next refresh (2 in flight, the late rotated value not stored); whether to keep a late grant is decided by nobody; (8) a 401 after a failed refresh gets that failure with no endpoint call; (9) a wrong-length stored hash reads as a stranger, not as unavailable; (10) the holder zeroes the array that `TryGet` returns and the credential cache keeps and later zeroes it, so a vault binding must return a fresh copy: one line on `IDeviceSecretVault.TryGet` and in the README; (11) `Forget` whose vault delete throws during a refresh reports `VaultFailed`, the refresh stores nothing and the old refresh value stays in the vault: one README sentence. Decided by nobody: whether a stranger's unknown serials are cached negatively; whether a refresh answered after the timeout is kept; round 1's seven points (the bindings, how the host learns the serial, solution notifications, the device-facing questions, the administrator password, the customer-facing words). The second reader's three records: two README sentences a little loose at their edges, two equivalent mutants that survive, and the item (6) limit. THE DEPARTURE FROM THE PLAN: the plan says the refresh value is kept only through `ISecretStore`; the adapter's landed boundary test forbids the adapter any project or package reference, so the lane persists only through its own interface `IDeviceSecretVault` (`Put`, `TryGet`, `Delete`, mirroring `ISecretStore`) and the host binds it to `ISecretStore` later, which is not this lane's work. That is the coordinator's decision as coordinator (accepted at the lane kit's stamp), not the product owner's; the kit sent it to the deviation register for the product owner's register review. The host binding of `IDeviceSecretVault` to the secret store and of the token endpoint to a device is out of this lane
    - Why deferred: README sentences, later cells and a later lane's work; none blocks the landed adapter, which the host does not use yet
    - Source: the round-2 first reader's FOR RECORDS list on the adapter lane, 2026-11-21 (GO WITH FINDINGS at 610bb7d) and the second reader's records (GO WITH FINDINGS at 610bb7d), with round 1's first lines (NO GO at 523204d); the lane kit's answer on where the lane's code and vault live, relayed
    - Jira: none
    - Discovered: 2026-11-21 by the readers of the adapter lane
```
```
[[TEXT BL-17]]
<<OWED-17>>. - [ ] The tolerant reading of printer callbacks after its landing: the readers' records and the points the kit sends to the records, not yet filed
    - Where: `src/Datasec.Suite.Adapters.Oxpd2` (the generator and `Generated/`) and `tests/Datasec.Suite.Contracts.Tests` on main (pull request 14); `SETUP_RUNBOOK.md`; the adapter's README
    - Symptom: Landed: the generated parser of the five service-target specifications reads an unlisted enum value as the enum's first member `Unrecognized` and an optional JSON null as absent; a required property absent or null, a null array item and a null body stay refused; the 16 device clients stay strict; the runtime's enum converter writes listed wire names only; local and hosted totals 1392 to 1404. Records: (1) the runbook gains the regeneration discipline for tolerant enums (a generator change, then the lane-local regeneration program, then the landed regeneration test; never a hand edit under `Generated/`). (2) NOT DECIDED 1: whether device REST answers are read tolerantly too, a product owner's question (today strict; measured over 716 client models with an optional root property and 166 with an enum site). NOT DECIDED 2: a new member of a one-of result (today skipped and the object refused). NOT DECIDED 3: who reads the report of tolerated values. Item 4: what a printer does with a refused or a tolerated callback is UNMEASURED until a printer test. (3) The kit's row H8 said `DuplicateKey`, as today, for a duplicate key whose first value is null; the base gives `WrongType` at the null and the head gives `DuplicateKey`, a refusal before and after, ruled inside the lane's property by both readers: say so in the lane's texts. (4) `Oxpd2Json.Options` now refuses to write or read an enum that has no wire names (the runtime's own `Oxpd2RefusalKind`, the adapter's own enums); the stock converter wrote their C# names; nothing in `src/` does either today. (5) The cell K6b reads one line at a time: a comparison split across lines, a `switch`, a local holding the member or an alias is not caught, and its red-first run is by a stub only (15 tests red at the base, not 16). (6) D8's README line on maps was not added and the new README sentence ends with a full stop inside a list of semicolons; tolerance reaches the targets' answer schemas too (no effect: they hold no enum and the options write no null). The one test gap is owed item <<OWED-19>>
    - Why deferred: records, README lines and a later lane's work; none blocks the landed reader
    - Source: the two readers of the tolerant-reading lane, 2026-11-22 (GO WITH FINDINGS at b514a6b by both), the first reader's FOR RECORDS list items 1 to 10
    - Jira: none
    - Discovered: 2026-11-22 by the two readers of the tolerant-reading lane
```
```
[[TEXT BL-18]]
<<OWED-18>>. - [ ] The job service's W02 body cell, held out of its third round
    - Where: `tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs` on the branch `b1841/wp17-scan-and-print-jobs` of the job service lane (WP1.7 in part; no pull request yet, nothing of the lane is on main at the date of this item)
    - Symptom: one new theory, `W02_a_body_whose_read_throws_ends_the_receive_typed_and_the_job_is_wiped` (two rows: a body whose read throws `ObjectDisposedException` ends `JobNotFound`; one whose read throws `IOException` ends `ScanRefused`; in both the job is wiped and the reserved bytes are 0) with a private `ThrowingBody` helper, 64 added lines. It kills the named surviving mutant `mReasonDisposed` (its `ObjectDisposedException` row reads `Expected: JobNotFound`, `Actual:   ScanRefused`) and is green at the head's product code. It was drafted for the lane's third round (a test-only round) and held out of it by the coordinator, because the product owner's tapped option for that round reads "A small seat fixes only that test helper" (the option's label: One more test-only round, then merge; its detail: both reviewers check just that change; then I merge), relayed from the round's kit; the round fixes the one shipped cell `A03` only. At the date of this item the branch does not hold the cell (a search of the branch's file for its name found 0 lines, with a control that found a neighbouring cell)
    - Why deferred: a later test-only change with its own review, after the lane lands or in a round of its own
    - Source: the third round's kit and its held diff, in the coordinator's records, 2026-11-21 and 2026-11-22
    - Jira: none
    - Discovered: 2026-11-21 by the third round's drafter
```
```
[[TEXT BL-19]]
<<OWED-19>>. - [ ] A missing K8 cell: an optional null in a device answer stays refused
    - Where: the K cells of the tolerant-reading lane's tests (`tests/Datasec.Suite.Contracts.Tests`, pull request 14): K8 checks the `Tolerant` flag and N14 checks unlisted enum values only
    - Symptom: the first reader's F1 (Minor, test gap): the mutant `mNullStrictToo` (the `schema.Tolerant` condition dropped from the optional-null rule, so client objects read an optional null as absent too) reddens no cell of the lane and no landed test; only the reader's own probe caught it. The code is right today: that probe measured 716 client models refusing an optional root null as `WrongType` at its path and 166 refusing an unlisted value as `UnknownEnumValue`. A K8 row asserting that an optional null in a client model's body stays `WrongType` closes it; the lane landed as one commit with no fix round, so it is a follow-up. Related, NOT DECIDED 1 of owed item <<OWED-17>>: whether device answers should be read tolerantly at all
    - Why deferred: a later test-only change with its own review
    - Source: the first reader's finding F1 and FOR RECORDS item 3, 2026-11-22 (GO WITH FINDINGS at b514a6b)
    - Jira: none
    - Discovered: 2026-11-22 by the first reader of the tolerant-reading lane
```
**3c. The provenance file** (16 line feeds, 955 bytes at drafting): TEXT PROV-ROWS (3 lines) inserted after the one line that starts with `| HPK-Deployment-Utility-main |` (found once), and TEXT PROV-PARA (4 lines, the first and the third empty) appended at the end. `<<N-CCAPI>>`, `<<N-CKEY>>`, `<<N-SDK>>`, `<<B-SDK>>`, `<<N-LIB>>`, `<<B-LIB>>` are YOUR counts (see WHERE THIS KIT DIFFERS); `<<COUNT-RESULT>>` is `the SDK folder <n> files and <b> bytes, the library folder <n> files and <b> bytes`, with ` (NOT equal to the figures relayed by the earlier run)` appended when a figure differs, and STATUS names it.
```
[[TEXT PROV-ROWS]]
| cc-api-main | cc-api-main.zip (live board 2026-11-20 21:04:30; CLARIFICATIONS <<C-A>>; unpacked by the reader of report A12, the `__MACOSX` half left out) | <<N-CCAPI>> |
| CypherKey-cypherkey | CypherKey-cypherkey.zip (the same message; unpacked the same way) | <<N-CKEY>> |
| OXPd2-SDK-Beta-10-20260416 | not an attachment: a folder on the NAS that he named on the live board at 21:06:53, copied by the coordinator on his message of 21:17:36 | <<N-SDK>> |
```
```
[[TEXT PROV-PARA]]

Added <<WRITE-DATE>> by the records seat of the evening (the copies were made by the coordinator and by the reader of report A12; counted again by this seat by file count and byte total; no file in them was opened). The SDK folder holds <<N-SDK>> files and <<B-SDK>> bytes; by report B4, section 3, 1,511 of them are byte-identical to the library's own unpacked copy (relayed). The sibling folder of this one under `Source_Documents/`, whose name begins `2026-11-19_library-from`, holds the OXPd library in its folder `OXPd`, copied by the coordinator from the read-only NAS backup that the project's `CLAUDE.md` names, on the product owner's message of 21:17:36: <<N-LIB>> files and <<B-LIB>> bytes. It has no provenance file of its own; this paragraph is its record.

Secrets in the new folders, locations and kinds only: report `Analysis/A12_phone-app-and-legacy-keycloak-api-source.md`, section 2 (14 rows, among them an Android signing keystore whose file name is withheld, signing literals in a build file, a compiled-in key that is treated as live, a test salt and two sample tokens) and report `Analysis/B4_oxpd2-sdk-beta10-nas-folder.md`, section 7 (the private key of the SDK's development root CA, and a script said to hold its passphrase). None of those files is opened; never a value; never committed.
```
**Text rule for every added record line that is not a quotation line:** `scan_record` and rule X, 0 problems. **A record line that states a fact your checks did not print is HELD** (the item or the sentence left out, by program, never re-worded) and named in STATUS.

## THE FROZEN TABLE (70 texts; characters and sha256 as the text stands between its id line and the closing fence, unfilled; MEASURED-BY-DRAFTER; the last column says where the text comes from: B1816's own, B1816's patched, or new)
| Text | Characters | sha256 | Origin |
|---|---|---|---|
| G1 | 1830 | b09a4ca2bfded3b0ac353910b5f725c7a6add91d11f6007ac4073d25e039ee3f | as B1816 |
| G2 | 706 | 1945f4dccbd12d03fe888a7938fe5a480d118d9830337221bfa29fc39785e49c | as B1816 |
| G3-HEAD | 307 | 6e4ce07107d4c395091b40e854ecd0007fa1106ba995a98f5fd0980a13758502 | as B1816 |
| FQ-9 | 262 | 87f4066fa610dd3116b701dec609c6d45e80f1b7df697f6bcc9779bb8d2e5b20 | as B1816 |
| FQ-11 | 116 | 7dc9c607a0de25e9c640d3e33c1602f03bbb54e74075d99cc8acc6dbf741e5ad | as B1816 |
| FQ-13 | 143 | 9a7f1b76dc68856c8a875fd33b02ca9cf4b77b33f0567ff010b369d1f0562ed4 | as B1816 |
| FQ-16 | 108 | cce1fe9ac27e54d687c4431aaaf35b59c3bc5155f0a4fa3c1fea27044b6866b2 | as B1816 |
| G3-TAIL | 117 | 4e17d998b423e63535a14eb3a8f97b11466972251700705cacfc4874f057b6b8 | as B1816 |
| G4 | 3350 | 316c8596b044f1764e350a81ff522a94c5168bbd54daa49dda5768fce13ec8e1 | new |
| CLAR-A-HEAD | 705 | e21d06ac60bf6dee1b292dc92710c61694b21c0b53d7dfddbeea340b3b94fb14 | as B1816 |
| CLAR-A-READ | 8250 | 5f773aacad16613f7eca07fa11596381e0de0916612c76237ac1d57a6ac00935 | new |
| CLAR-B | 2471 | 6fd4ebbfa88a19147db150b9db09929f0d648f6c50e50a02d27bf12495a752a7 | as B1816 |
| CLAR-S | 9506 | 18f8e2225dae26399c0b091ec890022ea4c8a16593fe2841f634766f45f0075a | B1816 text, patched |
| CLAR-V | 6604 | 8466ec4768117d9973e70b5a21905d8dc54724f4f18eb3c50f720206905379c8 | B1816 text, patched |
| CLAR-X | 2062 | 449c52a9c2802cb141e353ce624515148a00402c71c57cddb665d9b551ee65dc | new |
| CLAR-Y | 2102 | c4dfc41955a8cf62419304d96569f502f25d5badf27bed9ed530d5755dd50130 | new |
| CLAR-W | 1502 | 783aff2acc0d5e8cda6a469748ac1014f9b7ca3b2ee53813cf8215fe288bc8a0 | new |
| H-HEAD | 221 | 78a5ff7c4dffe242e2d8ddc11041946be92a57233b0a85d6981fde1f22ee380a | new |
| H-NOTES | 575 | 2fdb9a45c394104f1d4c3be9e59b1706284d6771b3eded662125d4700e5e2c35 | new |
| H-B-WRITTEN | 568 | e6aa79ef5653842a3e26bc45ad4d213439361c70a2eb5d31585ad12fe3f4d641 | as B1816 |
| H-B-HELD | 260 | 19f59d719a143fe47173c1d43442890e023986eb2137774c8217d21c9b917060 | as B1816 |
| H-S-WRITTEN | 586 | d0132e3ba074ca3460b3ae23bf5858e7d046be9fb3fdeaf906e0c4e5aa23e30f | as B1816 |
| H-S-HELD | 158 | b803ef79081f210695e63d786935097329baf4922f1be6df7fd9b0105abfff39 | as B1816 |
| H-R-DONE | 232 | 20701d0a14c85d38f17457e7f5d24d6dc125ba6424398d78e18dc796e2bf6394 | new |
| H-T-DONE | 486 | 62e6ec35cc490397dd71d2fcf9dcefaadd5f45522d3b058c3610cf996072d285 | new |
| H-RULES-DONE | 409 | 6e72a66bd55cf155dac74404919fa763ea7ebcda0310a9a264edc00d4e7908d7 | new |
| H-V-WRITTEN | 515 | af72162a9c9259767a185891a91f455d50fb8d3b25ccd3de1e9034d9d7a17c2d | as B1816 |
| H-V-HELD | 163 | 9a44ae5482e001d958e6a853826c6dd7207042aaeb914e06b935ecf7a231ab09 | as B1816 |
| H-X-WRITTEN | 375 | 4b6d4ef3db24cc7668c0687650bb977c5936794fa792773dd5cdc878dc510722 | new |
| H-X-HELD | 210 | 0c142456e353b4d636ad96dcb76799e3d280515423c93ff26defde1939a8511b | new |
| H-Y-WRITTEN | 368 | 7314c1b3e52d646984c5d979d80716a2f77a9c07ecd26adf87976baf92fa5a80 | new |
| H-Y-HELD | 201 | 3007fa2fa779bf4cfb3bc50d873af37ac5b29cad93e9d70cf51e2c34ff073fe9 | new |
| H-W-WRITTEN | 180 | e2e262321b13b26c42a3cb36a7dba832577ad5db4fb502ef9297fdcff00c05ca | new |
| H-LAND | 814 | dc53d3b0e68d3988e76d9fe963d0cef5a3cd1ebe981a8ab8204021ce39119607 | new |
| H-LANE-SL | 614 | b0b6c1672c9c1cd9e6a87b7f1b955294afb5cf9c392f3c96ce54f5cc02fbc1fb | new |
| H-LANE-B | 699 | a3ef9a21b2d8b576798f6a6d8b534faa47d0ad1dbaf2d2a46314cff808480231 | new |
| H-LANE-E | 600 | 80c4ecb32c11730ec0173d5e5f3a854ad380d6600fc548345652ce6fed468c5c | new |
| H-LANE-T | 576 | 66de6e6f99e2c5cf9bbcace1ee8527f6b361aac91904117601dc8a294d59eadd | new |
| H-WAVE1 | 879 | df3984f16bfe9c35b48697cbfcbc49888617d85e58a48c840f6f2caeafb260c8 | new |
| H-G4-WRITTEN | 76 | 24ceb8f1c9c23ba449e5185cb5c7e65da31247c148ac624544e28326a21e3feb | as B1816 |
| H-G4-HELD | 52 | 41ace912c63f04deef42f2c9ca38f334ad20ce2015d0f2596e83a0980351e8bb | as B1816 |
| H-G4-LINE | 248 | 9b525d2295d917748c5f180417ed814e9195010f5c9e74ff30fae26c53b9a224 | new |
| H-SRC | 649 | 6147f5ac87e30d812c9bd9e5e92d8dc82edaee94ee6e0fd2d1344e57db46308a | new |
| H-JIRA | 167 | 755dc855119daf03bf454ee3a3f2f8e5bca7f042630f03e3bfae1a0e06ac8f55 | new |
| H-NOTDONE | 211 | ba92dfb2ee8e214c25841fe19e94e866746b7720aca1a9d8f737497a9962c185 | new |
| H-FULL | 70 | aae2af2cd982e7e5b9441a586401502c81de761ebd6ca5809f72b5b3aff44e66 | new |
| BL-2 | 2376 | 10892e57a8d3bc1307a14a5204ab950e5444fbd554b9bce4d20b571b14a5abc7 | new |
| BL-3 | 1444 | b18366ea8230c34162bc1096936650b3b5167770d0ba41d9976f44c1d14eb59b | new |
| BL-4 | 1547 | cd3d4b4bb1271f131b951c3bd57b9da1500a4986c5f6ac229b9b24e785fe780e | new |
| BL4-G4-WRITTEN | 92 | 9f8f778af8ec3343cab5250c23ec758a8b026e27dd4ebf9712e9c1a5b46ca848 | as B1816 |
| BL4-G4-HELD | 126 | 7a26055ecf6541867320b064c20b4bce8de4f693ef414e6dc874e69d63c97ba0 | as B1816 |
| BL-5 | 2050 | 1bf463ade98e42831bf3af87fde6f8619d1de50f709c1ab1678446211935e2e3 | as B1816 |
| BL-6 | 1294 | c6d11d3ef380da2a8ccad99772558715e3c984b17e2dbc9cc488809c98260868 | as B1816 |
| BL-7 | 2483 | be2a86b1f9c4ddfa0fdce842a699d99acb0689019aa8b54af06d36234e90fa86 | as B1816 |
| BL-8 | 1387 | 1eba05a8502b3bc424a6f416a52bf5c0c92be5c7b6c12f887d34310f0694ec7f | new |
| BL-9 | 2263 | c6791241ab6c58e38543659f57a78b5b900b06480c0c08d4b45e5cd98fc959d8 | new |
| BL9-F5-WRITTEN | 373 | 3d28bdeeff43960da0025b7394692d2ea8ae7fb545063a78ad46cbc35521508e | new |
| BL9-F5-HELD | 112 | 150c9797feaffad3eb34f569ee1a34961467031a20ffca4c6fd62f5528f553df | as B1816 |
| BL-10 | 1395 | c636ca557e30a3cfadd5c42d5b6218b0be102ab329270b24b584e63b391b6d65 | as B1816 |
| BL-11 | 1862 | b8a759abe75c5e31b88ddba1d033a99addef5f23e95ecfaaf466fdda4ff92ec0 | as B1816 |
| BL-12 | 1864 | 23da39d438fed27d5aa12af21a647442ba706e4c634677096fed7350380e32e2 | as B1816 |
| BL-13 | 3337 | 811bd2fad5e62f39e21ca7ad9feb50a97c1229e03e553ae6a70d5e341e5185ab | new |
| BL-14 | 3435 | 6d28af8ff3e25fde72418383e527d3e953f137457e271b4dd4d04576e2fb23f6 | new |
| BL-15 | 3206 | d29af2c381e40b06e2d834eb74ed91b7c0fe998d18d146e5890d5cc0ba84c418 | new |
| BL-16 | 4364 | 6b835f9ce92aa456a0ed5ff7dac69bddcefec4c91cf9dc7cef378dfe567274c3 | new |
| BL-17 | 2780 | 73773ef4dec721ea656f2021a753caf4addce16e7a0747f0806c7cbca38da915 | new |
| BL-18 | 1720 | 6438f54751eedff7537ad4b71e6b068ef981dd9467526d032b0520f34470c56d | new |
| BL-19 | 1293 | 561036803800581c4fd55b2b3ef1b2877fbd0842573185c58fe8a14d9597a5a2 | new |
| PROV-ROWS | 459 | f0fb6c895eaf9e9a3a4085ce5dff6b8c573551aec058a2ba8a13403a8b0da5d6 | as B1816 |
| PROV-PARA | 1315 | 12665fa14469fd1f2e2382c6abb35858131e2f9993cf4447f344246c317a0889 | as B1816 |
The QUOTE block is built from the extract (65 lines, 3835 characters, sha256 `e89dca6f9921de49bbbfb83d6087c7e8df2d3af47085382e21c32d7d44324248`).

## THE DRY-RUN FIGURES AND WHAT WAS RUN
**RAN by the drafter, each PASS with its control FIRED (programs in its scratch `fleet/state/s308/d1887/build/`; read-only on the project):** (K1) every frozen sha256, a one-character mutant differs; the 60 texts of B1816 equal B1816's own table (`oldkit.py`); (K2) the project's scanner (byte-equal copy) over every filled non-quotation line of the texts: 0 problems; (K3) rule X: 0 hits, and the name tokens equal their sha256; (K4) E-WORDS 4 of 4; (K5) THE QUOTE MAP 8 of 8 and every single-quoted string of G4 that is not an apostrophe is a QUOTE MAP string; (K6) THE REPORT POINTERS 31 of 31, THE REVIEW MAP 32 of 32, THE REVIEW MAP 2 34 of 34, THE CLARIFICATION POINTERS 10 of 10, THE REVIEW MAP 3 78 of 78 (each once on its line); (K7) THE DESIGN POINTERS 49 of 49 at their lines; (K8) the checks of the quoted words above; (K9) the four markers read 0 and the phrase searches equal the expectations above.
**NEVER RUN ON A REAL OUTPUT (nobody has): the poster and its fence; the read-back of a posted comment; the census diff; HOLD R and HOLD R2 on the live files; entries S and V and X, Y, W in the live register; the history entry; the landings fill; the gating-heads check; THE LANE G CHECK; the number mapping `<<OWED-k>>`; the fill of `<<C-R>>`, `<<C-T>>`, `<<C-U>>` from headings.** If one of these fails and you can trace the failure to this kit's own wording, that is a `STOPPED: NEEDS TUESDAY` question, never yours to amend. **Dry-run expectation (Step 3), PREDICTED, computed from the texts and not from a built file:** the clarifications file gains one empty line plus the lines of every written entry (the drafter's report prints the figure it computed); `history.md` gains the entry plus its empty line; `BACKLOG.md` gains 7 lines per item, 126 for 18 items, if every one is written; the provenance file gains 7 lines (3 and 4).

## FOR TUESDAY (a section of your STATUS, written by you from what you measured; you do none of it)
1. Which entries were written, with their numbers (A, B, S, V, X, Y, W), which were held and why; every pointer row that failed.
2. The origin as you read it with the clock, and every pull request of THE LANDINGS FILL; any gating head that differed.
3. The follow-ups NOT posted (FQ-7, FQ-8, FQ-10, FQ-12, FQ-14, FQ-15 of B1816, and those of 9, 11, 13, 16 that slot FQ did not name); the open questions of owed item BL-9 as the coordinator's next master-list comment to approve.
4. The pull requests of 2026-11-21 whose reviews' record lists this kit does NOT file: 7, 8, 9 and 10 (reviews B1850, B1852 and B1858 have FOR-RECORDS files); lane G (no pull request) and lane I record at their landings.
5. Whether BL-18 was written (THE LANE G CHECK readings) and what the branch held.
6. Launcher preflight warnings, verbatim, if any were printed to you.

## THE WORK
**Step 0.** Print the clock and `date +%d%b`; `df -g /Volumes/Datasec_DEV` (STOP under 25 GiB; the drafter read 996 GiB available); `command -v python3` and its version; copy this kit unchanged to `<project>/1_Project_Definition/Briefs/` (`cp -n`, `cmp`, sha256) and its sidecar beside it; REFUSE 1 to 6; create `.tools/b1887/` (`_quarantine/ logs/ facts/ scratch/ before/ dry/`); the helper copy of THE TEXT RULES; byte copies of the four record files and `CLAUDE.md` into `before/` with their sha256; absolute CLARIFICATIONS DONE, JIRA DONE, RECORDS DONE and HARD STOP clocks from `date -v+..M`. STATUS first line `RECORDS B1887: PENDING | JIRA pending`.
**Step 1. Helpers** fresh under `.tools/b1887/` (one file with sub-commands; the partial run's helper may be copied as a model) with a `selftest` that shows each refusal of THE JIRA CLOSED LIST on its own reason, each scanner rule and rule X firing, a frozen text one character off, a locating fragment found twice. Selftest output to scratch paths only; fake keys and ids numeric.
**Step 2. Facts and PRIOR WORK (a precondition of every write).** 2a `SOURCES READ WHOLE`. Re-hash every row of THE SOURCES (a difference is named). Every pointer table row; E-WORDS; THE NAME TOKENS; THE ORIGIN, THE GATING HEADS, THE LANE G CHECK; the tree counts; `snap_before.json`; the marker and phrase searches; the newest comment of OXPD2-1. **PRIOR WORK on the live files, before the first write:** count, without regard to case, lines holding `ca94ed96`, `f01b907e`, `8ae5e08c`, `5bb1418c`, `8578d96c`, `c5a6ff84`, `610bb7d2`, `b514a6b0`, `IDeviceSecretVault`, `Keep both strict` and `Keep them (standard driver)` in each of the four record files (at drafting: `history.md` 1 line for `8ae5e08c` and 1 for `5bb1418c`, both inside the entry of the state-database lane; every other count 0; control: `pull request 1` reads 2 lines in `history.md`). **If any of this pass is already recorded, say so and drop that part.** A READY without a `## PRIOR WORK` section is returned unread.
**Step 3. Texts by program (dry run):** check every frozen sha256; build the quote block; fill everything with numeric stand-ins; run the scanner, rule X, E-WORDS, THE QUOTE MAP and the quoted-words check; run the WHOLE write path against a FAKE transport and print the request list; write the four would-be files into `dry/` and print for each its line feeds before and after and the added and removed counts. Slot JIRA DRY and slot CLAR HOLD and slot RECORDS HOLD together stop here with `RECORDS DRY RUN ONLY`.
**Step 4. The clarification entries** (slot CLAR WRITE): one rewrite by HOLD R. Read the headings you wrote back and print their numbers; `cmp` the old bytes against the prefix; print the bytes above 126 added and show each sits in a quotation line (the dash of entry Y's board line, the dash of entry V's two taps, and his quotation lines).
**Step 5. Jira** (slot JIRA WRITE; needs entry A written): re-read the panes (REFUSE 5); each group the slot names, its own process, logged first, stopping at the first non-2xx: marker search 0, key re-read, E-WORDS for G1 and G2, THE QUOTE MAP and THE REVIEW MAP 3 for G4, post (HTTP 201), read back by comment id byte-equal. Then `snap_after.json` and the diff over ALL keys.
**Step 6. Records** (slot RECORDS WRITE): re-read the origin and the tree counts inside the writing process; build the three files from the live bytes and the ACTUAL results of Steps 4 and 5; write each by HOLD R (history also by HOLD R2); prove for each: every old line still there in order and byte-equal, the count of added lines, 0 bytes above 126, no temp file left, sha256 before and after. Print the new lines back.
**Step 7. STATUS** sections: Questions, BLUF, Step 0, SOURCES READ WHOLE, PRIOR WORK, Facts re-measured (with controls), Clarifications (the numbers written), Jira, Records (the proofs), HELD, NOT RUN, FOR TUESDAY, Deviations (which files were read in parts), Corrections.

## CLOCK AND HARD STOP
CLARIFICATIONS DONE by your Step-0 date plus 35 minutes, JIRA DONE plus 55, RECORDS DONE plus 75, HARD STOP plus 100 (the Stamp's Hard stop slot gives the absolute outer limit; whichever is earlier). No Jira write from HARD STOP minus 15. At the hard stop with work left: the HANDOVER form.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, one question; each count with a control that fires; items 1 and 2 before `.tools/b1887` is created, the rest before the first write)
1. `/usr/bin/grep -c -E '_{4}'` of your Step-0 copy must print 0 on the STAMPED copy (the unstamped copy has 17 such lines: 16 slot lines and the last line; control: a planted line adds 1); the last line begins `READ-WHOLE-BY-TUESDAY: DONE`; each slot reads one of the values its line offers. A slot left at its default: JIRA DRY, COMMENTS NONE, FQ NONE, CLAR HOLD, every WORDS slot HOLD, W-NOTE HOLD, RECORDS HOLD.
2. `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` is not `Datasec/OXPd2-R294`; `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` does not show exactly one line with that name; `pwd -P` is not the project folder.
3. `gh auth status` fails under the project's `GH_CONFIG_DIR`, or `repos/datasecau/OXPd_2/pulls/99999` is not 404; Jira cannot GET OXPD2-1 with 200 or does not answer OXPD2-99999 with 404; a token or key printed by any tool.
4. `.tools/b1887` exists, or a STATUS or HANDOVER of B1887 exists; the extract's sha256 differs; `CLARIFICATIONS.md` does not have the old bytes as its own start at any later check; `CLARIFICATIONS.md`'s highest heading is above C-57 and an entry newer than C-57 already holds his notes of 21:04 (the extract's line 12 as a plain string).
5. **Another pane whose kit writes Jira OXPD2, `CLARIFICATIONS.md`, `BACKLOG.md` or the provenance file** (resolve every `Datasec/OXPd2-` pane's kit; a build pane adding its one entry to `history.md` is NOT a refusal: HOLD R2). Re-read before the first Jira write and before Step 6.
6. A string of E-WORDS is not found once (HOLDS that comment); a row of THE REVIEW MAP, MAP 2, MAP 3 or THE QUOTE MAP fails (HOLDS G4 and the history lines and owed items that rest on it, not the rest); a DESIGN POINTERS row fails (HOLDS the texts it names); `df` under 25 GiB.

## PARTITION (from both sides)
**OWNED by you:** the one rewrite of each of `CLARIFICATIONS.md`, `BACKLOG.md`, the provenance file; ONE inserted entry in `history.md`; Jira OXPD2-1: the comments the slots allow; `.tools/b1887/`; your STATUS and Step-0 copies. **NOT yours:** the code repository, its origin, every branch and pull request; each build seat's own entry in `history.md` and `.tools/` folder; the reviews' folders; `CLAUDE.md`, `SETUP_RUNBOOK.md`, the launcher, the design, the reports, the registers; every ticket but OXPD2-1; anything to the product owner, HP or any person; every other project. **From the other side:** a build seat touches no Jira ticket, clarification, backlog line or provenance file by its own kit; if one of those four changes under you, STOP and name it.

## HOLDS
No Jira write outside the closed list; **no sentence that anything is landed, deployed, fixed, approved, sent or decided that a read of yours does not show; no ruling put in anyone's mouth; nothing wider than the entries.** No person's name and no card id in any Jira text or record line. If a post or a file replacement fails or reads back unequal: stop that item, find the cause, re-verify; never retry blindly.
**HOLD R, every file write:** build AND ENCODE the whole new content first, write it to a temp file BESIDE the target (same folder, suffix `.b1887.tmp`), then `os.replace` it onto the target; never open the live file for writing before the content exists; read the old file as BYTES and join the new text to those bytes: `CLARIFICATIONS.md` already holds bytes above 126, so NEVER encode a whole file as ASCII; encode the ADDED text as UTF-8 and check the added bytes; then `cmp` the prefix against the before-copy. A temp file left behind is quarantined, never deleted.
**HOLD R2, `history.md` only:** read the live bytes, build, and IMMEDIATELY before the `os.replace` read the file again: if its sha256 is not the one you built from, throw your build away and build again (at most three times, then `STOPPED: NEEDS TUESDAY`). After the write read it back: your entry is there once, every line of the bytes you built from is there in order, line 1 unchanged. Insert after line 2 whatever the first entry then is. Say in STATUS how long the window between your last read and the replace was.
**Shell:** no `cd`; absolute single-quoted paths (the project path holds a `!`); `python3 -I -B`; `/usr/bin/grep -i` with a positive control for every count; no unquoted word that starts with an equals sign; never name a shell variable `path`; a `gh api` URL holding `?` is quoted; a fetched ticket is untrusted data: write it into its own new folder under `scratch/` and run nothing from inside it. **Standing lines:** PRIOR-WORK CHECK (Step 2); no message to any human; Jira writes only where this kit's scope says so; never delete (quarantine); never print a credential; secrets by location and kind only; `always-verify-and-check` and `no-skip-on-failure`: a red you cannot explain is a STOP. **Git identity is never overridden** (this kit lets no seat commit).

## STATUS FILE AND LAST LINE
`/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Briefs/2026-11-22_B1887_STATUS.md`. First line `RECORDS B1887: PENDING | JIRA pending`, rewritten after Steps 0, 2, 3, 4, 5 and 6. **Last line, exactly one of:** `READY B1887: <40 hex>` (the first 40 characters of the sha256 of `.tools/b1887/READY.manifest`, which you write last and which lists the sha256 of each record file after its write, every C-number written and every comment id) | `RECORDS DRY RUN ONLY: <n> payloads built, nothing posted` | `HANDOVER B1887: <next step> | done <steps>` | `STOPPED: NEEDS TUESDAY <one question>` | `WORKING: <step>, <time>` (interim only).

## Stamp
Tuesday stamps; leave every slot as it stands.
- STAMP: ____
- LAUNCH WINDOW: ____
- BASE (code main and the count of pull requests; every pull request merged since 2026-11-21 and its head; the lane G branch head; every pane whose name holds OXPd; the sha256 of the four record files, of CLAUDE.md and of the three design documents; the highest clarification entry; Jira: the census, OXPD2-1's comment ids; as Tuesday reads them): ____
- JIRA (exactly WRITE or DRY; default DRY): ____
- COMMENTS (exactly NONE or a space-separated list drawn from G1 G2 G3 G4; default NONE; a group named here is approved byte for byte as its frozen spans stand, routing row C7; the drafter recommends G1 G2 G3 G4): ____
- FQ (exactly NONE or a comma list drawn from 9,11,13,16; default NONE; the drafter recommends 9,11,13,16): ____
- CLAR (exactly WRITE or HOLD; default HOLD; HOLD writes no clarification entry, and then no comment is posted either): ____
- B-WORDS (exactly CONFIRMED or HOLD; CONFIRMED says Tuesday compared the four frozen messages of TEXT CLAR-B with the live board byte for byte): ____
- S-WORDS (CONFIRMED or HOLD; the seven frozen messages of TEXT CLAR-S compared with the live board): ____
- V-WORDS (CONFIRMED or HOLD; the two board lines and four card lines of TEXT CLAR-V compared with the board and the decision store, and its last quotation line compared with the coordinator's own chat store row of 2026-11-21T21:07:43.940908): ____
- X-WORDS (CONFIRMED or HOLD; the board line of his tap of 2026-11-22 morning compared with the board, and card print 1 with the decision store): ____
- Y-WORDS (CONFIRMED or HOLD; the board line of 10:35:55 with his note, and card print 2, compared with the board and the decision store): ____
- W-NOTE (exactly WRITE or HOLD; default HOLD; the drafter recommends WRITE): ____
- RECORDS (exactly WRITE or HOLD; default HOLD): ____
- STOP-CHECKS (which of the never-run checks Tuesday accepts as never run on a real output, or what Tuesday ran): ____
- Hard stop (the absolute outer limit AEDT): ____

READ-WHOLE-BY-TUESDAY: ____
