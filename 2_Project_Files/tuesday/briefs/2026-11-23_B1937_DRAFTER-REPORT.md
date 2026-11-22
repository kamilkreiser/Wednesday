STARTABLE: YES

# B1937 DRAFTER REPORT: lane R (records kit, seat Datasec/OXPd2-R299), OXPd 2 wave 3

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B1937_SEAT-R299_oxpd2-r-records-prs-18-25.md` (85213 bytes, 463 lines, sha256 `2080ebb92485d4dd4f1afb9bb9373a7c5ef29ba613a948a0003ceaf573b4f644`). Sidecar: same path plus `.measured` (13256 bytes, 85 lines, sha256 `98157a68961f0e6fa7f05f7f5d080d4549777378b7d6ae96add97baabc43a8a5`). `stamp_check.py <kit>` exits 0: `85 claims, 85 measured, 0 not measured`. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s312/d1937/` (builder `build_kit.py`, template `kit_template.md`, sidecar writer `sidecar.py`, GET-only Jira reader `jget.py`, the GET files, the dry builds in `dry/`). Drafted Mon 23 Nov 2026 00:01:02 to about 00:25 AEDT by `date`.

## BLUF
- The kit records pull requests 18 to 25 (all merged 2026-11-22, chain `bf6b441e` -> `c480a0c8`), the ten reviews (B1918, B1919, B1923, B1924, B1926, B1927, B1928, B1929, B1930, B1933; B1925 left out as another project's), main's eight push runs (all `success`, attempt 1), nine owed items (59 to 67 at drafting), one history entry, at most one clarification entry (C-69, only if Tuesday prints the 20:03 board line in slot N-WORDS), and ONE Jira comment on `OXPD2-25`.
- **The 10:35 note check: it is already recorded.** C-63 (heading line 610) holds the board line with his note verbatim at line 614: `... a — Keep both strict for now | note: but make a note that this was a decision and can me changed if necessary`, and its reading paragraph (3) says it is a recorded decision that can be changed. The kit re-checks this at P-5 and adds nothing for it.
- **Prior-work probe:** R294 (B1887), R296 (B1900) and R297 (B1906) each ended READY (last lines printed). R298 is kit B1909, records for the MPS project. It wrote nothing in OXPd: the live `BACKLOG.md` and `history.md` equal B1906's READY.manifest, and `CLARIFICATIONS.md` equals B1900's. No records pass has recorded pull requests 18 to 25 yet: every P-3 probe reads 0, and history's newest entry is B1906's 19:43 entry.
- The commission's subjects for the F1 and F2 lanes are written as seven separate owed items, each saying it stays open until its follow-up round lands: F1A audit fan-out (B1928 1 plus B1929 R2-1), F1B `Guid.Empty` (B1929 R2-2 plus B1928 4), F1C README lines I-4 and Q11, F1D the same-object renewal (B1924 1), F2A re-judge before removal (B1927 1), F2B the hook that catches the refusal (B1933 FOUND 1, with the coordinator's default (a) a named limit and (b) the latch as the alternative), F2C the adapter README map sentence (B1926 1).
- If any pull request numbered 26 or higher has MERGED when the seat reads, the kit STOPS, because a landed F1 or F2 round would make those items false.

## Facts re-measured (instrument; control)
- GitHub, by `gh api -X GET` under the project GH_CONFIG_DIR, 00:02 to 00:06 and 00:16: 25 pull requests, 0 open, `pulls/99999` 404. Main is `c480a0c81466f88102cb9d15a506b738615ebcbb`. For pull requests 18 to 25 I read head, merge commit, single parent, commit count and the `(#n)` suffix, as in the kit's LANDINGS table. All eight heads equal their review's first-line head.
- Push runs 45008282606, 45011881660, 45016304308, 45017744519, 45018313743, 45019745164, 45020207120 and 45023966157: each `ci`, attempt 1, success, with four jobs success.
- Logs of the last run:
  - linux: `total: 1662` x2, `failed: 0`, `succeeded: 1658`, `skipped: 4`, `GUARD: clean (10 files)`
  - windows: `total: 1662` x2, `failed: 0`, `succeeded: 1641`, `skipped: 21`, `GUARD: clean (11 files)`
  - rules: `RULES: clean (530 files)`, `Ran 111 tests`, `UNIT-TEST FLOOR: ran 111, floor 111`
  - Open code-scanning alerts on main: 0.
- The code paths the texts name were checked in the tree at c480a0c8 (GET trees, 701 entries, not truncated) and in file contents fetched by GET into scratch:
  - `SignInActor.cs` holds `event EventHandler<SignInAuditEventArgs>? Audit` and `RaiseAudit`, with one try/catch.
  - The SignIn README has `## Limits`.
  - `CloudDeviceTokenHolder.cs` holds `Finish(`.
  - `SuiteDbContext.cs:203-204` subscribe `RefuseDuringSave`, and the doc comment sits at 195-200.
  - The Secrets README names `DeleteUnreadable`.
  - The root README line 29 names the tag only.
- Jira, through a copy of the project helper with a GET-only transport that refuses anything else, every request logged in scratch:
  - Census: 25 issues, 0 Done. OXPD2-1 answered 200 and OXPD2-99999 answered 404.
  - OXPD2-25 and OXPD2-18/14/12 are each Task 10030 in Backlog with 0 comments. I read OXPD2-25's seven paragraphs.
  - Marker `REC-PR19-R6-23NOV`: 0 keys. Controls: `REC-NEW-RULES-20NOV` found OXPD2-23 and `zzqxnonexist` found none.
- Panes at 00:05 and 00:16: `%0 tuesday`, `%240 Datasec/NexusAI-N163` and unnamed panes. No `Datasec/OXPd2-` pane.

## STOP-severity checks run on my prototype output (each PASS, its control FIRED)
- K1: all 28 frozen sha256 values were recomputed from the written kit; a one-character mutant differs.
- K2: the project's own `scan_record`, from a byte-equal copy, ran over 86 filled record lines: 0 problems and 0 bytes above 126. `scan_jira` over J25 (956 characters): 0 problems. Each of these planted controls fired: `_by_kam_`, a card id, a coordinator path, `lane` in J25, a double quotation mark, and a B-number. All eight PR titles pass, with no double quotation mark and no byte above 126.
- K3: the green and race-word checks found 0 in the added lines, and the planted `the race is gone` fired.
- K4: all 80 REVIEW MAP rows were found once at their lines; a mutant of RM 1 misses.
- K5: dry builds from byte copies of the live files:
  - BACKLOG 411 -> 474 line feeds (+63, -0)
  - history 183 -> 200 (+17, -0)
  - CLARIFICATIONS 688 -> 696 (+8, -0, old bytes a prefix)
- Never run on a real output, and marked so in the kit: the seat's poster and the POST with its read-back, HOLD R and HOLD R2 on the live files, and the slot N-WORDS board line.

## D-decisions (the drafter's, as written into the kit)
- D1: closures are recorded as a new item (BL-CLOSE), not ticks. The kit inserts lines only; no existing owed line is ticked or edited.
- D2: the Jira scope is ONE comment on OXPD2-25, because pull request 19 closes the shapes of the ticket that his 14:57 ruling created. There are no comments on the work-package tickets: the precedent is B1906's finding that no records pass has commented a work-package ticket at a landing.
- D3: order is the comment first (Step 4), then the three files (Step 5). Before the POST, every text and file is built dry, so BL-CLOSE and H-JIRA can state what was read back. Two guards: JIRA WRITE needs RECORDS WRITE, and if the owed numbers move after the comment the kit STOPS.
- D4: the kit takes no heavy lock and runs no build or test.
- D5: entry N is gated on Tuesday printing the live board line. I did not read the board, because the fences forbid it.

## Q-questions for Tuesday (each with a default)
- Q1: Record the 20:03 grant as C-69? Default: YES if you print the board line in slot N-WORDS; the precedent is C-68 for 16:53 and message 9 of C-56. The slot defaults to SKIP. The kit checks the line starts `2026-11-22T20:03:36` and ends with the commission's text exactly (two blanks after `great.`).
- Q2: Jira beyond OXPD2-25? Default: NO.
- Q3: Tick items 7, 47, 48, 52, 53, 58 and the others in place? Default: NO; this pass inserts only, and BL-CLOSE lists the ticks owed.
- Q4: Launch timing. Default: now, before F1 or F2 lands. B1934 to B1936 write none of the record files, and the kit STOPS on a merged pull request 26 or higher.
- Q5: Slots. Default: RECORDS WRITE, JIRA WRITE.

## Chain inputs (each produced by an earlier step or present at BASE)
- Step 0: the clock, df and the stamped kit (BASE); it makes `.tools/b1937/` and the before-copies.
- Step 1: the helper, built from the B1906 and B1900 helpers (copied read-only) and the scanner copy made in Step 0.
- Step 2: the GitHub and Jira origins (BASE), the before-copies (Step 0) and the manifests (BASE).
- Step 3: the frozen texts (the kit) plus the fills from Step 2.
- Step 4: the J25 fill from Step 3 plus `snap_before.json` from Step 2.
- Step 5: the Step 4 read-back plus the live files.
- Step 6: everything above.

## UNMEASURED
- The 20:03 board line, with its sub-second stamp.
- Every platform claim the texts relay, which are the readers' (macOS arm64 probes; Linux and Windows UNMEASURED where they say so).
- Whether F1 or F2 lands before this seat runs.

## Outside-the-fences disclosure
- Read only in the Tuesday and OXPd trees, plus the first 700 bytes of the B1909 kit (MPS, a Datasec project), to identify R298.
- Read in full:
  - DRAFTER_RULES.md
  - the B1906 kit
  - the three READY manifests and the STATUS last lines
  - all ten FOR-RECORDS files
  - the B1933 VERDICT lines 1-40, and the first 4 lines of each other VERDICT
  - CLARIFICATIONS lines 560-688
  - the b1785.py scanner, transport and comment code
- Read in part: the B1900 kit, lines 1-279 of 518.
- Not read: the B1900 and B1906 commissions, the B1913 lanes brief, and the B1932 and B1914 build kits. They are not needed for a records kit, and the commission names them as form for the other lanes.
- GitHub GETs only. Jira GETs only, with credentials read by name in-process and never printed.
- No `decision_queue.sh`, no board reader, no card store. Card ids appear only in this report's reasoning, from the commission and C-63, and none is in the kit text.
- No write outside the kit, its sidecar, this report and my scratch.
- No `cd`, nothing deleted, no heavy lock taken, no test run.
