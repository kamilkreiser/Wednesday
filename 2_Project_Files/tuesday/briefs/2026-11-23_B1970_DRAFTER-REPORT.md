STARTABLE: YES

# B1970 DRAFTER REPORT (seat Datasec/OXPd2-R304, records): OXPd records of pull requests 31 and 32, the OQ-6 approval and the kick-off message

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1970_SEAT-R304_oxpd2-r-records-prs-31-32-oq6.md` (78313 bytes, 346 line feeds, 20 frozen texts, 26 SOURCES rows hashed, 46 REVIEW MAP rows, 8 `____` lines: 7 slots and the last line). Its sidecar is beside it. `stamp_check.py <kit>` exits 0 with 110 claims, 110 measured. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s315/d1970/` (`gets.py`, `gets2.py`, `codefacts.py`, `build_kit.py`, `sidecar.py`, `kit_template.md`, `dryrun_section.md`, `dry/`, `get2/`, `blobs/`, `card_oq6.txt`, `rulings.txt`, `build_kit.log`). Drafted 10:17:39 to about 10:33 AEDT Mon 2026-11-23, by `date`.

## BLUF
- **Four record files, each written once by HOLD R, in this order:** `CLARIFICATIONS.md`, then the register, then `BACKLOG.md`, then `history.md`. The order is also the cut line.
- **`CLARIFICATIONS.md`:** two entries are appended, C-70 and C-71 at drafting (PREDICTED; the seat finds the numbers by program).
  - **C-OQ6** is the product owner's 06:59 OQ-6 tap. It holds no card id: it is worded as "his live-board answer of 2026-11-23 06:59 ... : a, Approve both rows". It also carries, from the store's print, the title, the coordinator's recommendation b, the option a label and detail, and the store's ruling time 07:00:17.497479.
  - **C-KICK** is his 10:10 message, verbatim, followed by the coordinator's reading, marked as the coordinator's and not his word.
- **The register:** rows DEV-22 and DEV-23 change their status cell from `NEEDS APPROVAL (03:378)` to `APPROVED: the product owner's approval of 2026-11-23 under OQ-6, C-<n> (CL:<line>, 03:378)`. Each row's source-lines cell gains `CL:<line>`. The line is the C-OQ6 quote line, 702 PREDICTED. One section, "## Approvals, 2026-11-23 (records pass)", is appended. No other line changes.
- **`BACKLOG.md`:**
  - Item 74 is ticked, because PR 32 closed it.
  - Two new owed items are added, 77 and 78 PREDICTED:
    - **RDME:** B1960 FOUND 1. `README.md:35` cites `CsaStore.cs:288/:305`, but the catches are now at `:294/:311`. This is owed to the next Identity lane and is not fixed by the kit.
    - **REST4:** the other points of B1963 and B1960.
  - Items 75 and 76 are untouched.
- **`history.md`:** one entry.
- **What the kit does not do:** no Jira call (no FOR-RECORDS line names a ticket), no register row for PR 32's change, and nothing to the printer or to any person.
- **The READY line** carries both C-numbers, in the form `READY B1970: <40 hex> | C-70 C-71`, so you can run `--delivered`.
- **Sizing:** no build, no test and no lock. The work windows are Step 0 + 50 and Step 0 + 80 minutes, and the hard stop is at or before 14:00. The pass is estimated at about 50 minutes; R302 finished at about +9 minutes with two files.

## FACTS RE-MEASURED BY THE DRAFTER (instruments in scratch)
- **Origin** (`gh api -X GET` under the OXPd GH_CONFIG_DIR, 10:20:18 to 10:20:26):
  - Main is `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b`. There are 32 PRs, 0 open, and none numbered 33 or higher. `pulls/99999` returned rc 1 (404).
  - **PR 31:** head `aa80178a`, merge `3e506e4b`, parent `5b66a7b1`, 1 commit, 2 Contracts test files, message ends `(#31)`.
  - **PR 32:** head `10f446f3`, merge `da8d64a8`, parent `3e506e4b`, 1 commit, 7 Identity files, message ends `(#32)`.
  - The heads equal the gates' first lines (aa80178, 10f446f).
- **Main push runs:**
  - Run 45067340719 (3e506e4b) and run 45068273700 (da8d64a8): each `ci`, attempt 1, completed success, with all four jobs success.
  - Counted in the logs with colour stripped:
    - 31: `total: 1786` ×2 on linux and on windows, succeeded 1782 and 1765, skipped 4 and 21, GUARD 10 and 11, RULES 553, Ran 111, floor 111.
    - 32: `total: 1809` ×2 on each leg, succeeded 1805 and 1788, skipped 4 and 21, RULES 553, Ran 111, floor 111.
  - Control: `total: 1810` gives 0 in all six logs.
  - `failed Datasec.` gives 0 in all six logs. Its positive control is the old C7 windows log (job 137299375943, B1956's copy): 1 match when stripped, 0 unstripped, the same instrument defect your 07:46 note caught. The kit requires the strip.
  - Open alerts on main: 0.
- **Code at da8d64a8:**

  | File | Fact |
  |---|---|
  | `CsaStore.cs` | `catch (InvalidOperationException)` at 254; `catch (Exception)` at 294 and 311; lines 288 and 305 are `{` |
  | `CsaReading.cs` | 167 `names.Add(property.Name)`; 185 `_ = element.GetString();` |
  | Identity `README.md` | `CsaStore.cs:288` at line 35 (the Minor is still live); `CsaStore.cs:294` absent; control `CsaStore.cs:254` at 47 |
  | `GatewayStubTests.cs` | 89 `WaitForConnectionsAsync(2` |

- **Project files:**
  - `BACKLOG.md` (07086aad), `history.md` (afab36a2) and the register (065681ea) each equal `.tools/b1956/READY.manifest`.
  - `CLARIFICATIONS.md` is 3b0c0e8e, the same as the B1956 source row. `CLAUDE.md` is 1a2e5629.
  - Owed items run 1 to 76; 21 are ticked; item 74 is open at line 526; the anchor is at line 548.
  - C headings run 1 to 69. The file ends `.\n`.
  - The register has DEV-22 at line 40 and DEV-23 at line 41, both NEEDS APPROVAL. `NEEDS APPROVAL` is on 9 lines.
  - There is no existing owed item for the README pointer: `README.md:35` 0 and `CsaStore.cs:294` 0. Control: `CsaStore.cs:250` 1.
  - Every P-3 probe is 0, each with a control that fired.
- **The product owner's words:**
  - **Card:** `decision_queue.sh show <exact id>` was printed into scratch and read through an inclusion filter on the id (1 line). It reads status ruled, choice a, `ruled_ts=2026-11-23T07:00:17.497479+11:00`, recommended b, and the option a detail verbatim, as frozen.
  - **His rows today:** `kam_rulings_today.sh` at 10:18:19 shows 5 rows: 06:59 morning-plan a, 06:59 OQ-6 a, 10:07 NexusAI, 10:10 kick-off, 10:11 thank you. Only the two named rows belong to OXPd.
- **Panes:** `%0 tuesday`, `Datasec/NexusAI-N165` and unnamed panes. There is no `Datasec/OXPd2-` pane.
- **Model and tools:** CLAUDE.md line 7 (newest Opus) wins over routing row C8 (line 98). The model id is `claude-opus-5-5` (models_latest.json line 17). Python is `/opt/homebrew/bin/python3` 3.14.10. `df` shows 960 GiB.

## PROTOTYPE (dry/, scratch only)
| File | Line feeds | Added | Changed | Removed | Other checks |
|---|---|---|---|---|---|
| `CLARIFICATIONS.md` | 696 → 720 | 24 | 0 | 0 | the old bytes are a prefix of the new file; C headings 1 to 71; C-OQ6 quote at line 702 |
| register | 67 → 70 | 3 | 2 (rows 40, 41) | 0 | `| DEV-` rows stay 23; NEEDS APPROVAL 9 → 8 over the whole file, 9 → 7 over the old lines; `APPROVED: the product owner's` only at lines 40 and 41 |
| `BACKLOG.md` | 563 → 578 | 15 | 1 heading | 0 | Closed line at 533; ticked 21 → 22; owed numbers 1 to 78 |
| `history.md` | 223 → 234 | 11 | 0 | 0 | |

**Scans:** the project scanner's `scan_record` ran over 53 added or replaced lines (CL 23, REG 4, BL 16, HI 10). It found 0 problems, 0 bytes above 126 and no leftover fill. The five planted controls fired and a clean line stayed quiet. The green and race checks found 0 outside two allowed phrases.

## D-DECISIONS (the drafter's)
- **D1: one tick only.** PR 32 closes item 74, and B1960 FOR-RECORDS says CLOSED for its FOUND 1 and the two exits that predated it. Item 76 holds the points of B1950 that PR 32 carried without closing them, so 76 stays open and BL-REST4 says so. PR 31 closes no owed item: the BACKLOG has no C7 item. A case-blind `C7` count found 1 line, a false hit inside the sha `ec75619`.
- **D2: two new items, not three.** RDME is its own item because the commission names it owed to the next Identity lane. Every other point of B1963 (GO, no finding) and of B1960's INFO list goes into one REST4, as B1956 did with REST2.
- **D3: the register.** Line 5 of the register says the status list is closed and that "The status APPROVED is not on the list and no row carries it." The ruling's detail says the rows move "to approved". I kept line 5 unedited, matching how the earlier pass left the BLUF counts. The new section states that line 5 describes the draft before the ruling (Q2).
- **D4: C-OQ6 form.** The file's C-63 to C-67 put the board line with the card id inside a `>` quote. The commission forbids the id, so C-OQ6's first `>` line is the commission's prescribed wording and says so in the entry's lead paragraph. The board's own minute is 06:59 (the reader's print). The daily note's 06:59:08 and 06:59:21 do not say which tap is which, so no seconds are written.
- **D5: C-KICK bytes.** The message is copied by program from the commission's bytes, which hold 5 double blanks, as his C-68 and C-69 also do. The reader collapses blanks in its own code (`kam_rulings_today.sh` lines 142 and 171), so its 10:10 row equals the frozen message after collapsing and cannot show the blanks (Q4). The minute is written as `2026-11-23 10:10`. The commission's 10:10:14 was not used, because I could not tell whether it was the board's stamp or your read.
- **D6: the history entry does not name OXPD2-25.** My commission says nothing of it.

## Q-QUESTIONS FOR TUESDAY (each with a default)
- **Q1: Jira?** Default: no Jira call. Neither FOR-RECORDS names a ticket (count 0; control: BACKLOG has 58 OXPD2- lines).
- **Q2: the register status word.** Default: `APPROVED: the product owner's approval of 2026-11-23 under OQ-6, C-<n> (CL:<line>, 03:378)` in both status cells, with `CL:<line>` added to the source cells. Line 5's closed-list sentence is not edited; REG-NOTE names it. The alternative is to edit line 5 too, which needs a new frozen text.
- **Q3: a register row for PR 32's change?** B1960 FOR-RECORDS 8 says "Q4 not a register row, the records seat to judge". Default: no row (how Workpath reads such answers is UNMEASURED and nothing stored changes), stated in H-WHO, as B1956 did.
- **Q4: C-KICK's blanks.** Default: the commission's bytes with the five double blanks. If you print the raw board text and it differs, the frozen text and its row must be rebuilt before the stamp.
- **Q5: REST4 as one item** for both reviews' other points. Default: yes.

## UNMEASURED
- The seat's helper and selftest, HOLD R and HOLD R2 on the live files, the numbers at the seat's run, and the stop after a partial write (Step 4). All of these are named "never run" in the kit.
- The raw board bytes of the 10:10 message (Q4).
- The ASP.NET Core version on the hosted runners: DERIVED, relayed as B1963 graded it.
- Whether PR 32's own pull-request windows leg passed. Your 07:46 note says it did; the kit does not claim it, and H-PR32 says only that it landed after 31, in the order the review's record names.

## OUTSIDE THE FENCES (disclosure)
- **The `cp` refusal.** My `cp -n` of the project scanner into my scratch was REFUSED by the TUESDAY tree's pathguard hook, which read the source path as a write. I did not make the copy any other way. I loaded the scanner in place with `importlib` under `python3 -I -B`, a read with no bytecode written; afterwards `.tools/b1785/` has no `__pycache__`, and its sha256 `5e766b28...` was checked before the load. The kit still tells the seat to `cp -n` it into `.tools/b1970/`, as R302 did successfully inside its own project.
- **The rulings reader.** I ran `kam_rulings_today.sh` because the commission says to. A full read records the newest row shown in the seat's read marker (`fleet/state/kam_read_<WED_AGENT>`). `kam_read_tuesday` reads mtime 10:26 now: a later read, not mine at 10:18. My run may have advanced it before that.
- **The card.** I ran `decision_queue.sh show` once, with the exact id, into scratch. It is read-only.
- **Everything else:**
  - Reads of the project, the coordinator's briefs and the note.
  - `gh api -X GET` only.
  - No Jira, no mail and no write to the project.
  - The kit, its sidecar, this report and the scratch folder are the only files written.
- **Kit-level notes:**
  - The kit carries no card id. The `datasec-oxpd-[a-z]` pattern matches 0 times in the kit, and the kit has 0 lines with bytes above 126.
  - The C-entries name "Tuesday's reading", following the file's form.
