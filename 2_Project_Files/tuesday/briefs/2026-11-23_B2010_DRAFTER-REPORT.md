STARTABLE: YES

# B2010 DRAFTER REPORT (seat Datasec/OXPd2-R308, records): the records of pull requests 41 and 42, six ticks, five new owed items, and two C-entries

**Kit:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2010_SEAT-R308_oxpd2-r-records-wave3.md`
- Size: 109098 bytes, 520 line feeds, 8 `____` lines (seven slots and the last line).
- Contents: 23 frozen texts, 32 SOURCES rows (every row hashed, and re-hashed after the build: 32 of 32 equal), 63 REVIEW MAP rows (0 failures).
- 3 bytes are above 126, all in one place: the em dash of the rulings reader's verbatim 20:56 row in THE CARD PRINTS. No frozen text holds a byte above 126.
- Sidecar `.measured` sits beside the kit. `stamp_check.py <kit>` exits 0 with 196 claims, all 196 measured: 147 by a count over the measured sources, 49 marked not a literal the seat matches.

**Scratch:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s319/d2010/`
- Scripts: `gets.py`, `logs.py`, `blobs.py`, `codefacts.py`, `jira_search.py`, `jira_ctx.py`, `reviewmap.py`, `proto.py`, `build_kit.py`, `sidecar.py`.
- Data: `texts.md`, `texts_frozen.md`, `kit_template.md`, `dry/`, `get/`, `jira/`, two card prints, `rulings.txt`.

**Drafted:** 22:50:51 to about 23:07 AEDT, Mon 2026-11-23, by `date`.

## BLUF
**Three record files, each written once by HOLD R, in this order:** `CLARIFICATIONS.md`, then `BACKLOG.md`, then `history.md`. B2003's form is followed: no Jira call, no register row, no design amendment.

**Ticks in `BACKLOG.md`:** six items, each with one Closed line naming pull request 42 and the code line at `e39396f9` that proves it:

| Item | Name |
|---|---|
| 80 | PLAIN |
| 81 | SHOWN |
| 82 | DUP |
| 88 | ECHO |
| 89 | EXITS |
| 90 | LABTEXT |

I re-checked each against the merged diff of pull request 42 (read whole for `src/`). The table is in the kit's THE TICK PROOFS section.

**Five new owed items, numbered 93 to 97 at drafting (PREDICTED):**

| Item | What it records |
|---|---|
| W1URI | Gate B2008 FOUND 1 |
| W1UNDO | Gate B2008 FOUND 2 |
| PIPE | Gate B2009 FOUND 1 |
| STEPS24 | First-run steps 2 to 4 are NOT built (see below) |
| REST2 | Every Info and kit FOR RECORDS line of pull requests 41 and 42 |

STEPS24 rests on a re-count at `e39396f9`:
- The 4 SOAP 1.2 bindings hold 30 operations: Accessories 18, Authentication 6, Authorization 4 and DeviceInfo 2.
- None of the 30 is for steps 2 to 4.
- Over all 16 committed files, these each appear on 0 lines: `TestService`, `Screenshot`, `UIButton`, `Certificate`.
- Controls: `RegisterAuthenticationAgent` on 26 lines, `GetAuthenticationAgentRecords` on 18 lines.

**Owed C-entries: two, contrary to the commission's expectation.** The commission said none was expected tonight. `kam_rulings_today.sh` (marker in my scratch) shows three product-owner rows after B2003 was drafted, and `CLARIFICATIONS.md` holds none of their words (each count 0):
- 20:55: his NOTE on the first-run-ready card: "I cannot find the admin password. I will need to find it tomorrow unless you can advise how to factory reset and reset password". The store holds key c (Not yet).
- 20:56: option a, "Create it as designed", on the Azure test-resource card.
- 22:07: "Thank you. I will action both tomorrow morning".

`CLAUDE.md` line 12 says every word of his is in `CLARIFICATIONS.md`, so I filed two C-entries:
- **C-NOPASS (77)** records the note. The store's key is recorded as the store's, not his. The 22:07 message is quoted inside it.
- **C-AZTEST (78)** records the tap.

**History:** one entry of 11 lines, ending `(records seat)`.

**READY line:** `READY B2010: <40 hex> | C-77 C-78` (predicted).

## FACTS RE-MEASURED (instruments in scratch)
**Origin** (`gh api -X GET`, OXPd GH_CONFIG_DIR, 22:50:59 to 22:51:12):
- Main is `e39396f91dbfba3c46cc43d7790adb59581d2853`. There are 42 PRs, 0 open, all merged.
- `pulls/43` and `pulls/99999` each return rc 1.

| PR | Merge | Parent | Tree | Head | Files |
|---|---|---|---|---|---|
| 41 | b4b4ef60 | 2e2feae8 | a1d181da | f039956d | 6 |
| 42 | e39396f9 | b4b4ef60 | 4af54a4b | 25cb4cb2 | 16 |

- Compare `b4b4ef60...e39396f9` reads ahead 1 with 16 files; `2e2feae8...b4b4ef60` reads ahead 1 with 6 files. The reverse compare reads behind (control).

**Main push runs** (attempt 1, all four jobs success):

| Run | Commit | Linux / windows total | Failed | Rules files | Unit tests |
|---|---|---|---|---|---|
| 45164375478 | b4b4ef60 | 2020 | 0 | 645 | 111/111 |
| 45167272161 | e39396f9 | 2054 | 0 | 647 | 111/111 |

- Controls: `total: 2055` is on 0 lines of the 6 logs. `failed Datasec.` is on 0 lines of the 4 test logs. The positive control (the C7 log) gives 1 stripped and 0 raw.
- Code scanning: 0 open alerts on main. The csharp analysis at both merge commits reads 0.

**Code at `e39396f9`:** 59 code facts, 53 at their printed lines and 6 counted on 0 lines (`codefacts.json`). Zero controls each hold:
- `unknown option` is on 0 lines of the print, oxpd1 and probe commands.
- `ONE way to a device` is on 0 lines of DeviceChannel.cs.
- The exact list `"probe", "print", "oxpd1"` is on 0 lines of PrintTests.cs.

The verbatim HP text is on line 70 (replace) and line 105 (no effect) of the committed `authentication.wsdl`, and the `LimitedUri` pattern is on line 440 of `common.xsd`.

**Record files:**
- The sha256 of each of the three record files and the register equals `.tools/b2003/READY.manifest`. `CLAUDE.md` equals B2003's SOURCES row 1.
- BACKLOG holds 92 owed lines, numbered 1 to 92, 24 ticked. Items 80 to 90 are as quoted. The anchor shape is intact.
- `CLARIFICATIONS.md` runs C-1 to C-76. The `S-CARD` rule fires on 80 lines.
- The `history.md` head is the 20:47 records entry.
- The project folder has no `.git`.

**Jira OXPD2:** GET only, through `b1785.py` loaded in place with its write logger refused. The census is 25 issues; controls 200/404.
- New subjects: 0 issues for each, except `named pipe` and `admin password`.
- Each of those two hits only OXPD2-1, on another subject (I read the context: a log-scanner pipe, and the newer-printer password question).

**Prototype (`dry/`, from the live bytes):**

| File | Line feeds | Added | Changed |
|---|---|---|---|
| CLARIFICATIONS.md | 798 → 830 | 32 | 0 |
| BACKLOG.md | 681 → 722 | 41 | 6 headings |
| history.md | 251 → 262 | 11 | 0 |

- `CLARIFICATIONS.md`: the old bytes are a prefix of the new.
- `BACKLOG.md`: the proof removes inserted lines by position. Ticked headings go from 24 to 30, owed numbers run 1 to 97, and each Closed line is the last line of its item.
- `history.md`: every old line stays in order.
- The project's `scan_record` found 0 problems over 81 filled lines, with 6 controls firing and a clean line quiet. The race and green checks found 0, with their controls firing.

## D-DECISIONS (the drafter's)
- **D1: no records branch or PR.** The commission says "through the project's records branch and PR form of B2003", but B2003 had neither: its record files sit in the project folder, which is not a git repo. The kit writes in place by HOLD R, as B2003's seat did, and says so.
- **D2: every code fact is pinned to `e39396f9`, not to main.** Lane W2 (B2011) may land first and move Lab lines. A merged PR 43 or higher is named in STATUS, not a stop. PR 41 or 42 not reading as frozen is a stop.
- **D3: the PIPE tick handling.** Item 89 (EXITS) is ticked: its own subjects (blank `--run`, blank `--credentials-file`, mode 000, dangling link) are built. The named pipe is a new item (PIPE), and TK-89 cites it.
- **D4: the REST2 item.** One grouped item holds every Info and kit record line, like B2003's REST3 and REST5. The lab wiring and the undo list are named in it as the coordinator's next lane.
- **D5: the 22:07 message is quoted inside C-NOPASS, not given its own entry.** C-AZTEST cites it.

## Q-QUESTIONS FOR TUESDAY (each with a default; the stamp's Q-ANSWERS slot lists Q1 to Q7)
- **Q1:** no Jira ticket; every Minor and Info becomes an owed item. Default: as frozen.
- **Q2:** the grouping of the five items. Default: as frozen.
- **Q3:** item 81 is ticked whole. My reading is that an XML comment or processing instruction in a body read as XML stays under the README's limit that masking is by name only. Default: tick whole.
- **Q4:** C-NOPASS records store key c as the store's, not as his choice. The rulings reader shows only his note for that card (1 row), and no tap. Default: as frozen.
- **Q5:** the coordinator's reading of "both" in 22:07 is the password plus the Azure login steps. This comes from s318's DELTA 1384 item 5, which I read in `NEXT-PICKUP-TUESDAY.md` via `git show 33a6470657`; I did not read the board exchange itself. Default: keep it, written as the coordinator's.
- **Q6:** two C-entries rather than none, and no third entry for 22:07. Default: as frozen.
- **Q7:** facts are pinned to `e39396f9`, so a landing of lane W2 is not a stop. Default: yes.
- **Q8 (report only):** THE CARD PRINTS are pasted whole, as B2003 did. The Azure card's `delivered_artefact` line names a person and a coordinator path, and the 20:56 rulings row holds an em dash. No record line holds either: `scan_record` found 0 on the added lines. Default: keep verbatim.

## CHAIN INPUTS (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Where from |
|---|---|---|
| 0 | the kit, the sidecar, the scanner `b1785.py`, the record files | at BASE (Tuesday's briefs, the project) |
| 1 | `.tools/b2003/b2003.py` (model, read only), the scratch copies | at BASE; Step 0 |
| 2 | SOURCES files, the GitHub origin, the live record files | at BASE / GET |
| 3 | frozen texts (the kit), the live numbers (Step 2), the scanner copy (Step 0) | Steps 0 to 2 |
| 4 | the dry builds (Step 3), the before-copies (Step 0), the re-read origin | Steps 0 and 3 |
| 5 | the proofs (Step 4) | Step 4 |

## UNMEASURED / NEVER RUN
- Never run: the seat's `b2010.py` and its selftest, HOLD R and HOLD R2 on the live files, the numbers at the seat's run, the three-write order, and the REFUSE 2/5 pane checks. At drafting the panes were `%0 tuesday` and two unnamed panes, with no OXPd pane.
- Whether lane W2 lands before launch: its records are the next pass's.
- Every device answer and every Linux and Windows behaviour the items relay.

## OUTSIDE THE FENCES (disclosure)
**Reads:**
- Read whole: the commission; the B2005-B2006 and B1944-B1946 commissions; DRAFTER_RULES; the B2003 and B1995 commissions; the B2003 report; the B2008 and B2009 VERDICT and FOR-RECORDS files.
- Read in parts: the B2003 kit (lines 1-260, 260-460, 460-480, 596-685, 706-741, 756-858; PART 2's other items and C-entries were not read); the B2005 and B2006 kits (FOR RECORDS, NOT DECIDED and Stamp).
- Read for the four facts it relays (D1, D3, the 22:07 reading and lane W2's beside-run): s318's handover, via `git show 33a6470657` on the TUESDAY repo.

**Writes:**
- Only the kit, its sidecar, this report and scratch.
- Nothing to the project, GitHub or Jira. Both card reads were `decision_queue.sh show <exact id>`.

**Hook refusals and stops:**
- One hook refusal: `pretooluse_recursive_scope.sh` refused an unscoped `grep -r` over my scratch GET copy of `contracts/` (to see context for 3 hits of "Button"). I did not repeat it. The kit claims no "Button" line count; it claims only that none of the 30 operation names holds it.
- My first `grep -rl "DELTA 1384"` over `0_Brain` and the briefs ran past the 2-minute foreground timeout and was moved to the background. I stopped it with TaskStop before it printed anything.
- One echo separator was refused by the zsh hook and re-issued as `----`.
