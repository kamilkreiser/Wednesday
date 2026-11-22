STARTABLE: YES

# B1946 DRAFTER REPORT (lane R, seat Datasec/OXPd2-R300): records of pull requests 26 to 28

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1946_SEAT-R300_oxpd2-r-records-prs-26-28.md` (94232 bytes, 507 line feeds, 44 frozen texts, 33 SOURCES rows hashed, 79 REVIEW MAP rows). Its sidecar is beside it. `stamp_check.py <kit>` prints rc 0 with 124 claims and 124 measured. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s313/d1946/`. Drafted 02:58 to 03:20 AEDT Mon 2026-11-23, by `date`.

## BLUF
- **The lane is records only. It makes no Jira call that writes, and no C-entry.** It edits `BACKLOG.md` in one rewrite:
  - 14 owed items are ticked in place: 7, 47, 48, 51, 52, 53, 58, 59, 60, 61, 62, 63, 64 and 66. The tick is one character on the heading, plus one inserted `Closed:` line naming the pull request that closed the item.
  - 8 items are marked closed in part and stay open: 34, 42, 43, 45, 46, 54, 55 and 65. Each gets one inserted `Closed in part` line.
  - Item 46's two NOT DECIDED sentences are replaced in place against C-63. His label, note and option detail are quoted verbatim.
  - Six new owed items are added, predicted 68 to 73:
    - A2F1 and A2F2: the two Minors of gate B1941, owed until A2-F lands.
    - F3A and F3B: the Minors of gates B1939 and B1943, owed until F3 lands.
    - A2REST: what the card store's first slice leaves.
    - REST: the other record points.
- **Deviation register:** the project already has one, so no new file is made. The search was a `find` over `1_Project_Definition`, which gave exactly 1 hit: `Registers/DEVIATION-REGISTER_DRAFT.md`, 21 rows. The kit inserts two rows and appends one dated paragraph:
  - DEV-22: class 3, weakness W10. A failed card search is a typed failure.
  - DEV-23: class U. A next page reads `Ambiguous`.
  - Both are NEEDS APPROVAL under OQ-6 (`03:378`). The approver is the product owner only, and no person is added.
- **History:** one history entry.
- **Sizing:** the seat runs no build or test and takes no lock. Its windows are Step 0 + 50 and + 80 minutes, inside the 09:00 grant end. The Stamp slot gives the absolute stop.

## FACTS RE-MEASURED BY THE DRAFTER (instruments in scratch)
- **Origin, by `gh api -X GET` under the project GH_CONFIG_DIR, 03:00 to 03:18:**
  - main is `394fa997826e3d102fafa6a0c05a4847132cb01a`. There are 28 pull requests and 0 open; `pulls/99999` gives rc 1, Not Found.
  - PR 26: head b74f0f0c, merge 39f57d6a, parent c480a0c8, 1 commit.
  - PR 27: head 75fb5fdf, merge 0c3900b7, parent 39f57d6a, 1 commit.
  - PR 28: head 93ea278e, merge 394fa997, parent 0c3900b7, 2 commits.
  - Each merge commit's first line ends `(#n)`. The gating heads equal the reviews' first lines (b74f0f0, 75fb5fd, 93ea278).
- **Main push runs:** 45032456562, 45035239506 and 45040156344. Each is `ci`, attempt 1, success, with all four jobs success.
- **Logs of the last run:**
  - linux: `total: 1759` ×2, `failed: 0`, `succeeded: 1755`, `skipped: 4`, `GUARD: clean (10 files)`.
  - windows: `total: 1759` ×2, `succeeded: 1738`, `skipped: 21`, `GUARD: clean (11 files)`.
  - rules: `RULES: clean (551 files)`, `Ran 111 tests`, floor 111.
  - Control: `total: 1760` gives 0 in each log. Open alerts on main: 0.
- **Records state:** the sha256 of `BACKLOG.md`, `history.md` and `CLARIFICATIONS.md` each equal R299's `READY.manifest`. R299's STATUS ends `READY B1937: f42c1fb0...`. There are 67 owed headings, numbered 1 to 67; 3 are ticked (3, 4, 9) and the anchor is at line 459. C-69 is the highest C-entry.
- **Probes and code facts:** P-3 probes are 0 each, and the controls fire. Code facts at main were read from GET copies:
  - `CsaStore.cs:282/:299`, `:196/:207`, `:68`, `:236`; `CsaReading.cs:47/:57`.
  - The Dockerfile digest.
  - Data README `:56`/`:58`; Registration README `:104-106`, `:147`.
  - Adapter README: `finally` 0 lines, control `late grant` 1.
- **Plan and design pointers:** `03:108`, `03:224`, `03:378`, `02:69`, `02:72`, `02:691`, `A1:208`, `A1:564`, each 1 hit. Control: `02:70` is not F6.
- **Panes:** `%0 tuesday` and two unnamed panes. No `Datasec/OXPd2-` pane.
- **Dry run in scratch `dry/`, built from the live bytes:**
  - `BACKLOG.md`: 474 → 538 lines, 64 added, 15 changed (14 headings and 1 Symptom span), 0 other.
  - Register: 62 → 67 lines, 5 added. The two new rows have 8 cells, as the header does. Classes after: `3` 2, `U` 6, 23 rows.
  - `history.md`: 200 → 212 lines, 12 added.
  - The project scanner copy (`5e766b28...`, via importlib) gives 0 problems over 88 added or changed lines, and 0 bytes above 126. Every control fired.
  - Race and green words: 0. The tick-proof controls fired.

## D-DECISIONS (the drafter's, for Tuesday's check)
- **D1. A tick inserts one `Closed:` line and edits nothing else on the item.** The Symptom and Why-deferred lines are not rewritten. Old lines stay byte-equal except one heading character, which can be proved by program. Item 7 uses three-blank indentation, as items 1 to 9 do.
- **D2. Item 66 is ticked.** Its list is fully dealt with by this pass: some items ticked, some marked in part, and item 46 corrected. The partial closings of PRs 21, 22, 24 and 25 stay open on their own items.
- **D3. Item 65 is closed in part only.** The map sentence closed with PR 26. The reader's second point, the late-grant `finally` limit, is not in the adapter README at main: `finally` appears on 0 lines.
- **D4. Merge shas and review heads are frozen in the texts, not filled.** A differing landing value is a STOP, not a re-wording.
- **D5. B1941's seven lane-owed items are numbered as parts (1) to (7) of one item, A2REST.** The earlier pattern is items 43 and 45.
- **D6. No C-entry.** The product owner gave no new word on 2026-11-23 (RELAYED). C-63 is quoted, not re-recorded.

## Q-QUESTIONS FOR TUESDAY (each with a default; the Stamp slot Q-ANSWERS holds them)
- **Q1. Should the lane write to Jira?**
  - Default: no Jira call at all. The commission allows comments only and names none to post.
  - Alternative: one frozen comment on `OXPD2-14` for PRs 27 and 28, and on `OXPD2-12` for PR 26. That would need the poster, marker and scanner machinery of R299's kit, which this kit does not carry.
- **Q2. Should item 51 be ticked while `OXPD2-25` stays open?**
  - Default: tick it. Its review records that the two shapes are closed. The Closed line says the ticket stays open by the coordinator's call.
  - Alternative: mark it closed in part and leave it open until the ticket is closed.
- **Q3. Should item 64 be ticked?** Gate B1939 reads the shape as "NAMED, not closed".
  - Default: tick it. The item owed the coordinator's default (a), and (a) landed. The text says "named, not closed", and the remainders are routed to F3A (the `SavedChanges` line) and REST (the latch).
  - Alternative: leave it open.
- **Q4. How should the register rows be added?**
  - Default: put the rows into the existing DRAFT file and append a dated "Additions" paragraph. Lines 12 and 42 are not edited: the BLUF's count of 21 and the line listing five class-U rows describe the 2026-11-21 draft, and the paragraph says so.
  - Alternative: correct lines 12 and 42 in place.
  - Neither the commission nor R299's kit names `Registers/` as writable for a records seat. R299's kit fenced it, and this commission asks for the rows. The kit writes that one file only.
- **Q5. Should B1941's two other choices become register rows?** These are: an enrolment refused when any other user holds the prefix, and the schema checked but never created.
  - Default: not rows. For the first, the Workpath rule is UNMEASURED, so no difference is known. For the second, creation is later scope, and "a deviation is never used to defer scope" (`03:108`). Both are named in A2REST.
  - Alternative: rows DEV-24 and DEV-25, class U.
- **Q6. How should item 46 be corrected?**
  - Default: replace exactly the OLD-46 span in place. The old text is kept in the seat's `before/` copy.
  - Alternative: leave the Symptom line as it is and add a correction sub-line. That keeps the stale words visible.

## CHAIN (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, its sidecar and the Stamp; the project files; the scanner `.tools/b1785/b1785.py` | BASE (Tuesday's stamp) |
| 1 | `.tools/b1937/b1937.py` (model, read only); `.tools/b1946/` | BASE; Step 0 |
| 2 | THE SOURCES files; the GET origin, runs, logs and code facts; THE REVIEW MAP files; the live record files | BASE; Step 0's folders |
| 3 | the frozen texts (kit); the fills (owed numbers and DEV ids from Step 2's P-4 and P-6; main and clock from Step 2) | Steps 0 and 2 |
| 4 | the dry builds and the checks; the slots RECORDS and REGISTER | Step 3; Stamp |
| 5 | everything above | Steps 0 to 4 |

## UNMEASURED
- Nothing has been run on a real output for:
  - the seat's `b1946.py` and its selftest;
  - HOLD R and HOLD R2 on live files;
  - the owed numbers and DEV ids at the seat's run.
- The drafter did not read the live board, a fence. The 0-rulings fact is RELAYED from the commission, line 9.
- The record points the texts relay (probes, counts, platform behaviour) are the readers', not re-measured. The kit marks them so.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Reads:**
  - `gh api -X GET` only, under the project GH_CONFIG_DIR. The calls were pulls, refs, commits, runs, jobs, job logs, `contents` of 11 files at main, and code-scanning alerts.
  - `tmux list-panes`, once.
  - Read-only reads of the project's record files, design files, Analysis A1, the CLARIFICATIONS entries C-63 to C-69, the deviation register, `BACKLOG.md` and R299's STATUS.
  - In Tuesday's tree: the verify folders named, and `grep` lines of kit B1934.
- **Not done:** no Jira call, no write to the project, GitHub or Jira, no `cd`. Nothing deleted, and nothing under `Source_Documents/` was touched.
- **Writes outside my lane's three files:** only scratch. That includes a byte copy of the project scanner and the dry builds.
- **One deviation:** the first `build` run used `python3 -B` without `-I`. Every later run used `-I -B`.
