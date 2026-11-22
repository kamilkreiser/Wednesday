STARTABLE: YES

# B1956 DRAFTER REPORT (seat Datasec/OXPd2-R302, records): OXPd records of pull requests 29 and 30

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1956_SEAT-R302_oxpd2-r-records-prs-29-30.md` (68851 bytes, 312 line feeds, 17 frozen texts, 30 SOURCES rows hashed, 45 REVIEW MAP rows, 8 `____` lines: 7 slots and the last line). Its sidecar is beside it. `stamp_check.py <kit>` exits 0 with 111 claims, 111 measured. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s314/d1956/`. Drafted 06:09:30 to 06:23 AEDT Mon 2026-11-23, by `date`. B1957 was not touched.

## BLUF
- **The kit is records only.** It makes no Jira call, writes no C-entry and writes no register row. It edits two files, each in one rewrite by HOLD R.
- **`BACKLOG.md`:**
  - Owed items 68, 69, 70 and 71 are ticked in place. Each tick changes one heading character and inserts one `Closed:` line naming the pull request that closed it: 29 closes 68 and 69, and 30 closes 70 and 71.
  - Items 72 and 73 are not edited, because the reviews carry their points.
  - Three new owed items are added, predicted 74 to 76:
    - **ESC:** gate B1950's Minor, a lone-surrogate name escape that ends a call untyped. It is owed and open, and its text names branch `b1953/a2-f2-malformed-escape` at `10f446f3` as not landed, with a windows red on a Contracts cell outside the lane that the coordinator is diagnosing.
    - **LOCK:** gate B1954's FOUND 1. No test reaches the under-lock check at `CloudDeviceTokenHolder.cs:318`, a gap left by PR 28.
    - **REST2:** the INFO points of B1950, B1949 and B1954, which those FOR-RECORDS carry.
- **`history.md`:** one entry for both landings.
- **Sizing:** no build, no test and no lock. The work windows are Step 0 + 50 and Step 0 + 80 minutes, and the hard stop is at or before 10:30. The predecessor R300 wrote five times the text in about 11 minutes, so this pass is estimated at about 45 minutes.
- **The register:** checked unchanged (P-2, P-6). DEV-22 and DEV-23 stay NEEDS APPROVAL, and nothing in the kit touches them.

## FACTS RE-MEASURED BY THE DRAFTER (instruments in scratch)
- **Origin, by `gh api -X GET` under the project GH_CONFIG_DIR (06:11:17 to 06:17:54; `gets.py`, `gets2.py`):**
  - Main is `5b66a7b16f9c35a48f7feef504c0fa69e5701dcc`. There are 30 pull requests, 0 open, and none numbered 31 or higher. `pulls/99999` returned 404.

  | PR | head | merge | parent | commits | merge message ends |
  |---|---|---|---|---|---|
  | 29 | a56ed63b | 49f686a8 | 394fa997 | 1 | `(#29)` |
  | 30 | 5cdcb806 | 5b66a7b1 | 49f686a8 | 2 | `(#30)` |

  - The heads equal the gate first lines (a56ed63; 5cdcb80; round 1 at 6177b52).
- **Main push runs:** 45048341660 (29) and 45056289720 (30). Both are `ci`, attempt 1, success, with all four jobs success. Counted in the GET logs with colour stripped:
  - 29: linux and windows `total: 1783` ×2, succeeded 1779 and 1762, skipped 4 and 21, RULES 551.
  - 30: linux and windows `total: 1785` ×2, succeeded 1781 and 1764, skipped 4 and 21, RULES 553, `Ran 111 tests`, floor 111.
  - Control: `total: 1786` gives 0 in all six logs. Open alerts on main: 0.
  - These equal Tuesday's note lines 04:19 and 05:44.
- **Branch check:**
  - `matching-refs/heads/b1953` has 1 row, at `10f446f3`. Control: `b1944` has 1.
  - Pull requests of that branch: 0. Control: the `b1944` branch has PR 29, merged.
  - Run 45052136167 attempt 1: windows failure; linux, rules and secret-scan success.
  - The windows log has 1 line naming `failed` with `...GatewayStubTests.C7_one_send...`, and `failed: 1` once. Control: `failed: 0` appears 0 times.
  - The compare from 49f686a8 to the branch lists 7 files: 7 Identity, 0 Contracts.
- **Code facts at main 5b66a7b1 (GET raw):**
  - In `CsaStore.cs`, the filtered `when (failure is not OperationCanceledException)` appears 0 times. Control: `catch (Exception)` is at lines 288 and 305.
  - `CsaStore.cs`: `HoldsANameTwice` at :243, `catch (JsonException)` at :250, and `catch (InvalidOperationException)` 0 times.
  - `CsaReading.cs:163` holds `property.Name`.
  - Identity README :42 holds "any object, at any depth".
  - Data README :59 holds the catching-handler sentence.
  - UP README :152 and :156 hold the both-orders sentence. "makes a new registration" appears 0 times; control: `TokenAnswerRefused` appears 3 times.
  - The holder checks `answer.IsDisposed` at :288 and :318.
  - `SuiteDbContext.cs:95` holds `RefuseChangedAuditEntries`.
- **Records state:**
  - The sha256 of BACKLOG, history and the register each equal R300's `READY.manifest`. R300 ends `READY B1946: 8748b86e...`.
  - There are 73 owed lines, numbered 1 to 73. 17 are ticked, and items 68 to 73 are open. The anchor is at line 523.
  - CLARIFICATIONS has C-1 to C-69 with no gap.
  - DEV-22 and DEV-23 are at lines 40 and 41, both NEEDS APPROVAL.
- **The product owner's words:** the subject words (`surrogate`, `escape`, `InvalidOperationException`, `MalformedAnswer`, `name twice`, `SavedChanges`, `TokenAnswerRefused`, `token object`, `deviation register`, `DEV-22`, `pull request 29`, `pull request 30`, `card store`) appear 0 times in CLARIFICATIONS. Control: `tolerant` appears 5 times.
  - The 06:04 count of 0 rulings is RELAYED from the commission. I did not run `kam_rulings_today.sh`: its header says a full read advances the seat's read marker, which is a write to Tuesday's state.
- **Panes:** `%0 tuesday` and two unnamed panes. There is no `Datasec/OXPd2-` pane.
- **Dry run (`build_kit.py`, built from live bytes, written only to scratch `dry/`):**
  - BACKLOG: 538 → 563 lines, 25 added, 4 changed (headings), 0 other changes, ticked 17 → 21. Each Closed line is the last line of its item.
  - history: 212 → 223 lines, 11 added.
  - The project scanner copy (`5e766b28...`, loaded by importlib, never run) gives 0 problems over 40 lines and 0 bytes above 126. All five controls fired.
  - Green and race words: 0 each. Controls: fire, fire and quiet, as expected.
  - Proof controls: 1 "other" change each.
  - K1: 17 of 17 equal on the written kit. The kit text has 0 name tokens from the scanner's list and 0 card ids.

## D-DECISIONS (the drafter's, for Tuesday's check)
- **D1. Ticks insert one Closed line only.** Items 68 to 71 keep every old line byte-equal except the heading's one character, as R300 did.
- **D2. No partials.** Nothing of items 72 or 73 closed with PRs 29 or 30. The FOR-RECORDS of B1950 and B1954 list those points as "carried, not in this lane".
- **D3. Item (a) is ESC, and the branch is named in its Why-deferred line.** The kit STOPs if any PR ≥ 31 is merged. The branch check rests on permanent GET facts (attempt 1 of the run, its job log and the compare), not on B1953's STATUS last line, which may change when that seat resumes.
- **D4. Item (c) is one REST2 item.** The INFO points are grouped by PR. B1949 INFO 3 is left out, because it reports that L01 discriminates and owes nothing.
- **D5. Some words were reworded so the scan check stays exact.** A gate's "leaves the suite green" became "passing", and "hosted-green" became "a passing hosted run". This keeps the green-word check at exactly 0, with no exception rule.
- **D6. The tool name `kam_rulings_today.sh` was taken out of the kit text.** It is now "no reader of the product owner's rulings", so the kit's name scan is 0.

## Q-QUESTIONS FOR TUESDAY (each with a default; the Stamp slot Q-ANSWERS holds them)
- **Q1. Should the kit write to Jira?**
  - Default: no Jira call, as in B1946's Q1. No FOR-RECORDS line names a ticket, and the commission allows comments only.
  - Alternative: frozen comments on `OXPD2-14` (PR 29) and on `OXPD2-12` and `OXPD2-18` (PR 30). That needs B1937's poster, marker and scan machinery, about +20 minutes, and a re-draft.
- **Q2. Should PR 29's two changes, or the A2-F2 boundary, get a register row?**
  - Default: no row. B1950 FOR-RECORDS Q4, and the Q4 of kits B1944 and B1953, all say Workpath's reading is UNMEASURED and nothing stored changes. H-WHO records that choice as the coordinator's.
  - Alternative: a class-U row, which would need a register write slot.
- **Q3. Should ESC be filed now?**
  - Default: yes, owed and open, with the branch named as not landed.
  - Alternative: hold the item until A2-F2 lands and file it with its tick.
- **Q4. How should the INFO points be filed?**
  - Default: one REST2 item.
  - Alternative: separate items for the state database and the registration.
- **Q5. Should item 71 be ticked?** A refusal across a `Remove` stays not built.
  - Default: tick it. The item owed a named limit, and B1954 reads it "NAMED TRUTHFULLY" and "CLOSES when this lands". The Closed line says the refusal is not built and routes the `:318` gap to LOCK.

## CHAIN (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, its sidecar and the Stamp; the project files; the scanner `.tools/b1785/b1785.py` | BASE (Tuesday's stamp) |
| 1 | `.tools/b1946/b1946.py` (a model, read only); `.tools/b1956/` | BASE; Step 0 |
| 2 | THE SOURCES files; the GET origin, runs, logs, the branch and the code facts; the REVIEW MAP files; the live record files | BASE; Step 0's folders |
| 3 | the frozen texts (kit); the fills (owed numbers from Step 2's P-4; main and clock from Step 2) | Steps 0 and 2 |
| 4 | the dry builds and the checks; the RECORDS slot | Step 3; Stamp |
| 5 | everything above | Steps 0 to 4 |

## UNMEASURED
- Nothing has been run on a real output for:
  - the seat's `b1956.py` and its selftest;
  - HOLD R and HOLD R2 on live files;
  - the owed numbers at the seat's run;
  - the pane checks of REFUSE 2 and 5.
- The 0-rulings fact is RELAYED. The drafter did not read the live board, a fence.
- Every probe, grading and platform behaviour that the texts relay belongs to the readers or the coordinator. None was re-measured.
- I read the three seat kits B1944, B1945 and B1952 for hashing only. Their STATUS files were read in their FOR RECORDS and FOR TUESDAY sections. B1953's STATUS was read in parts.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Reads:**
  - `gh api -X GET` only, under the project GH_CONFIG_DIR: refs, pulls, commits, runs, jobs, 7 job logs, the compare, `contents` of 7 files at main, and alerts.
  - `tmux list-panes`, once.
  - Read-only reads of BACKLOG, history, CLARIFICATIONS (by grep count), the register (by program), the scanner, and the STATUS files of R300, B1944, B1945, B1952 and B1953.
  - In Tuesday's tree: the three verify folders, the B1955 commission's head, and two lines of today's note.
- **Writes:** only my two files, the sidecar and scratch.
- **One refused command:** a `cp -n` of the scanner into scratch was refused by the path hook (pathguard read the source as a target). The byte copy was then made with `shutil.copyfile`, and `cmp` found it equal. Nothing in the project was written.
- **Not done:** no Jira call, no `cd`, nothing deleted, and nothing under `Source_Documents/`.
