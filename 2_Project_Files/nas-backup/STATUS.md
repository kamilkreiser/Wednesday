READY FOR QA

**Both tasks of ANSWER-6 are done. `RESULT-quarantine-erase.md` was written first (first line DONE).** TASK 1 in two lines: the quarantine folder is erased from the Backup share, and so is the copy of it the NAS had put in its recycle bin (16,807 files, 1,010,204,025 bytes, each of the 39 folders counted equal to its record first); nothing else at the share's top level changed. One of the seven originals on the drive changed while I worked, because a live Secuura session is writing to it; my program has no write path on the drive.

**One thing for the coordinator before a checker is commissioned:** I found a sibling of finding 2 that is NOT on the closed list, measured it, and did not edit it, as the brief orders: a link planted at the fixed file name `README.txt` in the destination folder makes the tool create a file outside the seat's folder and say GOOD. One word fixes it. It is the first entry under "Siblings" below.

# ROUND 4 (2026-11-27 evening): six fixes after the third check (ANSWER-6.md)

Fresh build seat "nas-backup" (WED-170), Fable 5.2, 2026-11-27 21:27 to 00:01 AEDT. The earlier seats' files were my handover; round 3's code is kept in `round3/`. ROUND 3's status follows this section as that seat wrote it.

**Read whole before I changed anything:** ANSWER-6, BRIEF, ANSWER-4, ANSWER-5, RESULT-secrets-move-2, RESULT-secrets-move, STATUS lines 1 to 206, the third verdict (204 lines), and of its `scripts/`: `lib3.sh`, `A1`, `A3`, `A4`, `A5`, `A7`. **Not read whole:** the evidence folders of the two moves (I read both programs, the plan and the count files, the two process checks); of the verdict's `scripts/` the files `A8`, `A9`, `A10`, `A5_inject.py`, `S3`, `X_my_mutants.sh`, `Z9`; of its `raw/` only the outputs of A1, A3, A4, A5 and A7. The brief asked for scripts and raw as my acceptance attacks; I read the ones that belong to the six items.

**Holds, kept:** nothing written to any NAS mount except TASK 1's two licensed removals; nothing armed; no `launchctl` verb but `list`; the three HOLD files stay; no shared file edited; no commit, push, stash or checkout (read-only `git log`, `status`, `show` only); no mail, board or chat post. Evidence that nothing is armed: `evidence/round4/real_lane_checks.txt` (0 `nasbackup` rows in `launchctl list`, 0 plists, 0 templates, each beside a control of 1 for `naspush`; `--run` on the real lane exits 3).

## The numbers

| | Round 3 | Round 4 |
|---|---|---|
| Suite (`tests/run.sh`, fake NAS only) | 568 passed, 0 failed | **694 passed, 0 failed** (126 new cells, T29 to T34) |
| The same suite file on ROUND 3's engine (red first) | | **607 passed, 87 failed**: all 87 in T29 to T34, 0 anywhere else |
| Mutants (`tests/mutants.sh`) | 126 of 126 | **143 of 143 caught, 0 survived or broken** (round 3's 126 and 17 new, one or more per new guard, each caught by the cell NAMED for it) |
| The third checker's scripts for findings 1, 2, 3, 4, 6, 10, re-run from copies | reproduce on round 3's engine | **refused or failing as required** on round 4's (table below) |
| Real dry run | 1,012,110 files, 68.27 GiB | **1,026,146 files, 69.22 GiB**, exit 0, no PROBLEM line |
| Secret-shaped names in the real dry list, lane's scan | 0 | **0** (controls 52,987, 5,559, 7,188) |
| The same list, the second checker's own scan, tiers A and B | 0 and 0 | **0 and 0** (8 and 14 patterns; tier D 0) |
| Names of what the secret-shape rule leaves out | counts only | **15 lists on the drive, 2,767 lines, each list's line count equal to the dry run's count for its set; 0 such files on the share** |
| Coverage claims in this section checked by a program | 140 | **223 claims, 0 not supported** |

## Where the brief and what I measured differ, and which I took

ANSWER-6 says the verdict's measurement wins where they differ, and to say so.

1. **Item 5, "one line".** The brief (and the verdict's "smallest fix") says the deletion proof also requires `not os.path.lexists(path)`, and that the checker's A3 a then reads NOT DELIVERED. It does not: in A3 a the parent folder is replaced by a new empty one, so the planned path does not resolve and `lexists` is false. I ran it; the one line fixes A3 c only. To make A3 a hold I added what the function already does for the set's root: the parent folder must still be the very folder that was listed (device and inode, recorded when the set is listed). The `lexists` line is there too. So item 5 is two conditions and about fifteen lines, not one.
2. **Item 3, "A7 section b, both ways".** His stub swaps the file in during the engine call that already carries it. That is the case "after the hand-over": sent, never proven, the night fails, named. For "before the chunk" I wrote a second stub that swaps one chunk earlier. His own script, re-run, now ends rc 8 with the marked copy on the fake NAS: that is the first case, and the run says so by name.
3. **Item 2, how far "the destination chain" reaches.** The brief names `ensure_dest_chain` levels and a realpath check "before each set". I did both, and three things more that I read as the same item: the folder the walk starts from (the client folder, `<NAS>/General`) is refused when it is a link; the realpath check is made again before every chunk; and again before the manifest and the COMPLETE marker are written. Each has a cell and a mutant. If that is wider than meant, each is one call site to take out.
4. **Item 4, one line beyond the brief.** The lane lies inside the seat's tree, and `manifests/` is backed up as a record. A names list written there would have travelled to the share with the next night's copy of the tree. So the list's own file name is excluded from every set (one line in the fixed exclusions, its own cell and mutant).
5. **Item 1.** Parts are compared case-folded as asked, and NFC-normalised as well. Two sets of one client with the SAME name were already refused by round 3; they are now refused by this rule too, and the checker's surviving mutant X28 has a cell.

## Per item: what changed, the red cell on round 3's engine, the green cell, the mutant

Every cell and mutant named here is a line of `tests/claims.tsv` (ids starting `r4-`), checked by `tests/claims_check.py` against the final suite output and the final mutant output. Red means: the final `tests/run.sh` run against `round3/nb_core.py.round3` (`evidence/round4/red_first_the_final_suite_on_round3_code_607_passed_87_failed.txt`).

### 1. Nested destinations (finding 1), and one name under two clients (finding 5's smallest form). Fixed.
- `load_conf`: within one client, a set whose destination name is a path prefix of another's is refused, naming both; the same name under two clients is refused. The real conf loads: 0 nested pairs in one client, 0 names used twice, 1 nested pair across two clients, which is accepted (`evidence/round4/real_lane_checks.txt`, and the dry run).
- Red on round 3 (9 cells), for example: `T29 A1: set=General|WEDNESDAY and set=General|WEDNESDAY/docs: exit 2 (expected '2', got '0')`; `T29 finding 5: ONE destination name under TWO clients ...: exit 2 (expected '2', got '0')`.
- Green now: those, plus the fake NAS unchanged by hash after the refusal (checked for the A1 pair and for the two-clients pair); the inner name given first; the checker's `Docs2` control GOOD with both files holding their own content; a name that only starts with the other's letters (`WEDNESDAY-docs`) accepted; the nested name under another client accepted.
- Two cells of T29 are green on round 3 as well, and I say so: the pair spelled in another case (round 3 refused it later, for the case clash on the share), and two sets with the same name.
- Mutants: F01 (nesting allowed), F02 (one name under two clients allowed), F03 (names compared as strings, not part by part).

### 2. A symlink in the destination chain (finding 2). Fixed for folders; one file-level sibling is listed below, not fixed.
- `ensure_dest_chain` refuses a level that is a link, and the folder it starts from. `dest_escape` requires the real paths of the set's destination, `versions`, `manifests`, `runs` and `_tmp_incoming` to lie inside the real path of `<NAS>/<Client>/<Seat>/nightly-backup`: before each set (a dry run too), before each chunk, and before the manifest is written.
- Red on round 3 (31 cells), for example: `T30 A4a ...: exit 2 (expected '2', got '0')`; `T30 A4b ... entries under the other client's folder: only itself (expected '1', got '24')`; `T30 A4d ... files under the outside folder: the one that was there (expected '1', got '2')`.
- Green now: A4a, A4b, A4d each refused (exit 2) with the outside folder unchanged by hash (a listing with sizes, times and inodes, plus sha256 of every file) and the whole fake NAS unchanged; a dry run with `versions/` leading out refused; the client folder as a link refused; `manifests/` swapped for a link during the run: nothing written through it, no COMPLETE marker; `versions/` swapped during chunk 1 of 3: the run stops before chunk 2, and 2 of the 6 replaced files went through the link, not 6. **A4c stays as it held:** GOOD, the outside file untouched, the subfolder a real folder with the source's content.
- Mutants: F04 (a linked level accepted), F05 (a linked client folder accepted), F06 (no check per set), F07 (no check before the manifest), F17 (no check before a chunk).

### 3. A hard link swapped in after the plan (finding 3). Fixed as far as a check can; the race is narrowed, not ended.
- Immediately before each chunk is handed to the engine (every pass), a file that now has more than one hard link is taken out of the chunk: not sent, never proven, the night fails, named `HARD LINK AFTER THE PLAN, NOT SENT`. In `prove_arrival`, more than one link is a verdict of its own, never proven; the run then compares the destination copy with the source and prints `HARD LINK AFTER THE PLAN, SENT: <set>/<path> -> <destination path> (its content is there now: YES|no)`, and the failure line says "THE CONTENT ALREADY REACHED THE DESTINATION and this tool never deletes there".
- Red on round 3 (14 cells), for example: `T31 swap between the hand-over of its chunk and the proof: NOT exit 0`; `T31 swap BEFORE its chunk: the secret's content is NOT on the fake NAS (0 marked copies) (expected '0', got '1')`.
- Green now, both ways. Swap before its chunk: 0 marked copies on the fake NAS, no file of that name at the destination, exit 8, named NOT SENT and NOT DELIVERED, the set's other files arrive. Swap after the hand-over: exit 8, no GOOD line, no COMPLETE marker, named, and the line's statement is checked against the fake NAS (the marked content IS at the path it names). Control without a swap: GOOD.
- Mutants: F08 (no check before the chunk), F09 (a linked file proven).

### 4. The names of what the secret-shape rule leaves out (finding 4; ANSWER-5's condition). Fixed.
- Per set, every run and every dry run writes `manifests/<seat>/<stamp>_<run|dry>_<set>_left_out_by_secret_shape.tsv` on the drive, beside the symlink list: one line per excluded entry, path TAB shape, sorted. It is written as soon as the set is listed. It is never copied to the share (the symlink list still is); the manifest that goes to the share carries the count and the list's path on the drive. README says where the list is and why it is not on the share.
- Red on round 3 (13 cells), for example: `T32 the drive list names 'src/secrets.ts' with its shape (expected '1', got '')`; `T32 a DRY run writes the list too: 5 lines, the same names (expected '5/1', got '/')`.
- Green now: the checker's four names each present in the drive list with its shape; line count 5 equal to the number the run printed (a name holding a newline is one line); each of the four names absent from every file on the fake NAS by content and by name, beside a control that both searches do find things there; no list on the fake NAS while the symlink list is; a list lying inside the source tree does not travel and an ordinary neighbour does; the dry run writes 5 lines and nothing on the fake NAS.
- Three of the four "absent" cells are green on round 3 too (round 3 wrote the names nowhere); they exist for mutant F11.
- Mutants: F10 (names not recorded), F11 (names put into the manifest that goes to the share), F12 (the list's own name not excluded).

### 5. The deletion proof (finding 6). Fixed, by two conditions (see "differ" 1).
- Red on round 3 (12 cells), for example: `T33 A3a the parent folder REPLACED by a new one of the same name: NOT exit 0`; `T33 A3c a file renamed to another case and made unreadable: NOT exit 0`.
- Green now: A3 a and A3 c each NOT DELIVERED by name, not counted deleted; A3 b (parent replaced by a link) not counted deleted; the readable rename still GOOD; a real deletion still let go and named; the function with and without the parent's id (without it, it answers as round 3 did: that cell is the can-fail).
- Mutants: F13 (deleted although the path resolves), F14 (a replaced parent accepted), F15 (the parent's id not passed).

### 6. The hold is tested before the conf is read (finding 10). Fixed.
- Red on round 3 (8 cells), for example: `T34 a --run under the hold with an UNCONFIRMED conf: exit 3 (held), not 2 (expected '3', got '2')`; `T34 the hold lifted four days later, first check: exit 0, not OVERDUE (expected '0', got '3')`.
- Green now: exit 3, recorded as held, no clock; the same with a conf that cannot be read at all; lifted four days later: exit 0, the clock starts at that check; without the hold the same conf is refused (exit 2) and does start the clock.
- Mutant: F16 (the conf read first).
- The nightly script already tested the hold first; nothing changed there.

## Suite and mutants

- **The final pass ran from a snapshot outside the repo** (`evidence/round4/snap.sh`; reason under "My slips" 1): the suite once (694 passed, 0 failed, `evidence/round4/tests_run_round4_final_694.txt`), then every mutant.
- **Mutants: 143 of 143 caught, 0 survived or broken (`evidence/round4/mutants_round4_final_143_of_143.txt`). The pass: suite from 22:53:01, mutants from 22:55:03 to 23:53:45, eight at a time. The ten files it ran are listed with their sha256 in `evidence/round4/final_pass_snapshot_sha256_before.txt`; hashed again after the pass: identical; and the lane's own files against that list afterwards: all ten the same (`final_pass_lane_against_the_snapshot_after.txt`).**
- A mutant counts as caught only when the cell NAMED for it fails. 17 are new (F01 to F17). 126 are round 3's; **four of those had to be re-pointed, because round 4 changed the line or the behaviour they aim at** (slip 2): R01 and R06 aim at two lines I rewrote (same intent, the new text); N07 (hard links travel) is now named for the cell `T13 the hard-linked file is skipped and counted`, because with the walk's rule broken the new check before the chunk still keeps the file off the NAS, so its old cell `T13 NOT ONE of the 35` stays green; R02 (deleted although still listed) now breaks both the old `name in names` line and the new `lexists` line, because for a name that is present either one alone answers. That last one is worth knowing: **the old `name in names` test is now redundant for a present name**; I left it in, as the brief words the proof.
- Before the pass I checked without running any suite that every one of the 143 mutations still applies to the engine (`evidence/round4/mutants_all_143_mutations_apply_no_suite_run.txt`: 0 BROKEN), and ran the six nearest the changed guards on their own (6 of 6 caught by name, `mutants_the_six_nearest_the_changed_guards_rerun.txt`).
- `tests/claims_check.py` on the final outputs: 223 claims checked, 0 NOT SUPPORTED, exit 0 (`evidence/round4/claims_check.out`). 83 of them are round 4's (ids `r4-`); the other 140 are round 3's, re-checked against tonight's outputs, with the two totals updated to 694 and 143.

## The third checker's scripts, re-run from copies

The 14 files of his `scripts/` were copied byte for byte (compared) and run with two environment variables his `lib3.sh` reads: where the lane copy is, and where fixtures go. Nothing in them was edited. Outputs: `evidence/round4/checker_rerun/round4_code/` and `.../round3_code/`.

| Script, section | On round 3's engine | On round 4's |
|---|---|---|
| A1 nested names | GOOD on 3 of 3 nights, the inner set's content at the outer set's path | rc 2 on 3 of 3 nights, 0 GOOD; `Docs2` control GOOD |
| A1, A2 one name, two clients | GOOD on 3 nights; the baseline holds `'Proj': 1` for a set of 12 files | rc 2, refused by name |
| A4a `current/<set>` a link | GOOD; `a.txt`, `sub` beside the outsider's file | rc 2; the outside folder holds `keep.txt` only |
| A4b the seat folder a link | GOOD; 15 entries under the other client's folder | rc 2; 1 entry (itself) |
| A4c a linked subfolder | GOOD, outside untouched | the same |
| A4d `versions` a link | GOOD; 1 file written outside | rc 2; 0 files outside |
| A6a, A6b, A6c (chunks; not in this round) | as the verdict reports | the same: 21 of 21 odd names identical, 4 distinct contents kept, the resume GOOD |
| A7 b hard link swapped in | rc 0, GOOD, the marked copy on the fake NAS | rc 8, 0 GOOD; the marked copy is on the fake NAS and the run names it (his stub swaps after the hand-over) |
| A7 c a folder swapped (a note, not in this round) | GOOD, marked copy under `conf/` | the same |
| A7 d names of the left-out | each of 4 names: lane manifests 0 | each of 4 names: lane manifests 1; run output 0, lane logs 0, NAS manifests 0 |
| A3 a parent replaced | GOOD, 1 counted deleted | rc 8, NOT DELIVERED, none counted deleted |
| A3 b parent a link | rc 8, 1 counted deleted | rc 8, none counted deleted |
| A3 c case rename, unreadable | GOOD, 1 counted deleted | rc 8, NOT DELIVERED |
| A3 f his unit calls | a name on disk in another case: deleted True; NFD on disk, NFC asked: True | False and False. His third call ("parent is a symlink") still answers True: it calls the function without the parent's id, which only the run supplies (section b shows the run's answer) |
| A5 d held with an unconfirmed conf | rc 2, recorded refused, clock started; four days later OVERDUE, "103.0 h" | rc 3, recorded held, no clock; four days later rc 0, the clock starts then |
| A5 a, b, c, e (findings 8, 9, 11, 12; not in this round) | as the verdict reports | unchanged |

## The real dry run, both scans, the names lists

One dry run, 22:11:34 to 22:21:09 (575 s under load averages 14 to 16; not a speed figure), reads only, exit 0, stderr empty.

| | Files | Bytes |
|---|---|---|
| WEDNESDAY tree, to `General/Wednesday` | 279,072 | 28.05 GiB |
| Testing Agent MAIN without Secuura's material, to General | 6,322 | 247 MiB |
| Eleven smaller general projects, to General (one empty and allowed to be) | 8,099 | 0.82 GiB |
| Secuura client folder, to `Secuura/Wednesday` | 587,374 | 30.97 GiB |
| Secuura's test material from Testing Agent MAIN, to Secuura | 145,279 | 9.14 GiB |
| **Would copy** | **1,026,146** | **69.22 GiB** |

- 14,036 files more than round 3's dry run five hours earlier: the tree is live.
- 0 PROBLEM lines; 15 engine list checks, each with 0 deleting lines; 15 "listed on the NAS (read-only)" lines. Excluded entries 7,814; by secret shape 2,767 (env-file 2,184; credential-file 412; key-or-certificate 126; private-key-or-wallet-name 28; credentials-folder-name 14; terraform-variables 2; credential-store 1); 9 files with more than one hard link; 16 left out for case-only name clashes; 982 symlinks recorded.
- The real share, read-only: `/Volumes/DEV-Working/General`, `General/Wednesday` and `Secuura` are plain folders, not links; `General/Wednesday` holds 1 entry; `Secuura/Wednesday` does not exist; no `nightly-backup` folder exists. Listings, folder times and `df` identical before and after (`evidence/round4/nas_diff.txt` is empty, rc 0).
- **Both scans on its stamp `2026-11-27_221134_46090`** (1,124,752 paths): the lane's `tests/scan_dry_lists.py`: 0, controls 52,987, 5,559, 7,188, rc 0. The second checker's `S_scan_real_lists.py` from where it lies: tier A 0 in 8 of 8 patterns, tier B 0 in 14 of 14, tier D 0, unit controls 22 of 22, 1,026,145 files asked and 0 not readable by this user (1 gone since the listing), rc 0.
- **The names lists** (`evidence/round4/left_out_lists_against_the_dry_run.txt`, by a program): 15 files on the drive, one per set; each file's line count equals that set's count in the dry run's output and in its manifest (WEDNESDAY 1,182; Secuura 786; Secuura's test material 727; Agentic Coding 40; Paperclip 17; Testing Agent MAIN 9; three sets with 2; six sets with 0); 2,767 lines in all, and by shape the same seven numbers the run printed. Files named `*left_out_by_secret_shape*` under the two destination parents on the real share: 0. I did not copy any of these lists into `evidence/`, and no name from them is in this file.
- **This dry run ran on the engine as it was at 22:11** (sha256 `3ed3e1df...`). One edit came after it: the containment check before each chunk, which a dry run never reaches. The suite and the mutants ran on the final engine (`beb8ffdb...`).

## Siblings: found, listed, NOT edited (the brief's closed list)

1. **A file-level link at `README.txt` in the destination folder. Measured, a real hole of finding 2's kind.** The tool writes one file with a fixed name, `<NAS>/<Client>/<Seat>/nightly-backup/README.txt`, when `os.path.exists` says it is not there. A link planted at that name, pointing at a file that does not exist yet, is "not there": the tool then writes the README text through the link. On a fake NAS: rc 0, GOOD, `planted.txt` created in an outside folder (`evidence/round4/probe_sibling_readme_file_symlink_NOT_FIXED.txt`; with the link pointing at an existing file nothing is written). What lands outside is the fixed README text, not backup content. The fix is one word, `os.path.lexists`, and one cell. It is not one of the six items, so I did not make it. The real share has no `nightly-backup` folder yet, so nothing can be planted there before a first run creates it. **This needs a word before the re-check: a checker who tries file-level links will find it.**
2. **The comparison during planning does not look at the link count.** A planned file of the same size as its destination copy and not yet in the index is compared by sha256 while the set is planned; if it gained a second hard link since the listing and its content equals the destination's, it is recorded proven. Nothing is sent in that case (the content is already there). Read in the code, not run.
3. **Deeper levels are not looked at for links:** `versions/<stamp>/...` (the stamp is not predictable), and the manifest and marker file names (they carry the stamp). Read in the code, not run.
4. **`source_deleted` called without the parent's id** answers as round 3 did. The run always passes the id; a future caller that forgets would lose the check. I left the parameter optional so the checker's own unit calls still run.
5. Not siblings, but the checker's 11 surviving mutants: X28 now has a cell (T29). The other ten are untouched, as the brief says.

## What I could not make sound

1. **The hard-link check narrows a window, it does not close it.** A second link that appears while a chunk is in flight (at most 200 files or 2 GiB) is sent. The proof then refuses it, the night fails and the path is named, but the content is at the destination and stays: this tool never deletes there. A link that appears and is gone again before the proof is not seen. And from the next night on, that file has two links when the plan is made, so it is left out by the ordinary rule and the night can be GOOD while the copy from the failed night is still on the share. The failed night's line is the only notice.
2. **The same for a link planted in the destination while a chunk is in flight:** that one chunk's writes go through it (cell: 2 of 6 files).
3. **A planned folder swapped for a secrets folder** (the verdict's note under finding 3) still delivers same-named files. A rule that reads names cannot see it.
4. **The names lists are as private as the drive.** They are kept out of the share and out of every set by their file name. A copy of those names in a file with another name (a report, a note, a checker's raw output inside this tree) travels like any other file.
5. **How the share presents a link made by another client is not known to me.** Every link in my tests is a local one on a fake NAS. If the share shows a server-side link as a plain folder, `islink` and `realpath` cannot see it. The real share's three folders read as plain folders today.
6. Findings 7, 8, 9, 11, 12 and notes 13 to 21 of the verdict are not touched, as ruled. README lists them under "Round 4: what the fixes do not close".

## My slips, this round

1. **A suite run I started from the lane itself was hit by another session's commit, and for a few minutes I took its result for a fault in my code.** At 22:15:19 the coordinator's session committed in this repo. For a moment the lane's uncommitted files were the committed ones, and one fixture of my suite (started 22:15:22) ran round 3's engine: it said GOOD where round 4 refuses. I found it from that run's own output (no "left out by secret shape" line) and from the three files' modification time of 22:15, a minute I had not written them in. That the commit set local changes aside and put them back is my reading of those two facts; I did not watch it happen. The same fixture, run nine more times in isolation, was refused every time. From 22:19 every suite and mutant run was made from a snapshot outside the repo. Evidence: `evidence/round4/note_the_22-15_commit_window.txt`. **What it means for a first real run is under "For the coordinator".**
2. **I started the whole mutant pass before checking round 3's mutants against my own changes, and had to stop it at 48 of 143.** 47 were caught; N07 was caught by two other cells of its family but not by the one named for it (above). Looking at why, I found two more that would have ended BROKEN later in the pass (R01, R06: I had rewritten the lines they aim at) and one that would have survived (R02). All four were faults in the mutant list, not in the tool; I corrected the list, proved all 143 apply, re-ran the six nearest, and started the pass again on a fresh snapshot with the same engine and suite files (compared). The stopped pass is kept: `mutants_first_final_pass_stopped_*`. Cost: about 25 minutes.
3. **I ran the second checker's scan with a missing argument** (`--access` wants a control file after it). Its last line raised an error and it exited 1 after printing every count. I ran it again properly (rc 0); the first output is kept as `scan_checker_first_try_my_wrong_argument.*`.
4. **One new cell had a wrong expectation** (it counted COMPLETE markers of both nights where it meant the second night); its first run showed it. Another assumed a link count of 2 where the fixture gives 3; found before any run.
5. **The dry run ran before my last engine edit** (above). I did not spend the one licensed dry run twice.
6. **In TASK 1's first precheck one exit code is the filter's**, not the command's (a hook said so). It is the one meant there; the result file says so.
7. **A `du` over `/private/tmp` that I started to see who was filling the disk ran past two minutes; I stopped it.** It read only.
8. **I typed `git stash list` to look for the cause of slip 1; a hook refused it** (the verb is on its write list, though `list` only reads). It did not run. Everything I ran in git was `log`, `status` and `show`.

## What is NOT tested in round 4

- **Any write to the real NAS by this tool**, as before. The new guards have only ever seen local links on a fake NAS (point 5 above).
- **The real code path of a real run** with the new checks: the per-chunk link check and the per-chunk containment check add an `lstat` per file and five `realpath` calls per chunk; at about 5,100 chunks that cost is not measured.
- **A case-sensitive source for A3 c.** The scratch volume folds case, which is what that test needs; the real drive is case-sensitive, where a case rename really removes the name.
- **Python 3.9** on the new paths beyond what T10 covers (one real run under `/usr/bin/python3`, green).
- **The names list at restore time:** nobody has tried to restore from it.
- **Whether tonight's 03:30 `naspush` run re-creates a secrets folder on the Backup share** (TASK 1's result says the same).
- **The proposals** (`proposed/`) were not re-read against round 4; none of the six items changes what they say, and I did not edit them.
- `tests/claims_check.py` matches text, as the verdict's note 17 says. It checks that a named cell passed and a named mutant was caught; it does not judge the cell.

## For the coordinator

1. **Commit this lane before any real run.** Until then the committed engine is round 3's, and a run that STARTS in the moment another session commits can execute it (slip 1). A run already going is not affected: it loaded its code at the start.
2. **The `README.txt` sibling** (above): one word, your call, before the checker.
3. **Disk:** free space on `/` went from 152 GiB (21:27) to 124 GiB while I worked. My scratchpad holds about 7.4 GB; the rest is not mine. The lowest I read was 91 GiB (23:23), above the 50 GiB floor; a watchdog would have stopped my mutant pass at 52.
4. TASK 1's open ends are in its result: whether the NAS keeps snapshots or versions elsewhere is invisible from here; `#recycle/DevMASTER-mirror` was there before and I did not walk it.

## For the checker: where to look first

- `nb_core.py`, every change is marked `ROUND 4`: `load_conf` (the block after the forbidden-roots loop), `ensure_dest_chain`, `dest_escape` and its three call sites, `hard_linked_now`, `prove_arrival`, the pass loop in `backup_body` (search `linked = set(`), `source_deleted`, `parent_id_of`, `write_left_out_list`, the `own-left-out-list` line of `EXCLUDES`, the top of `cmd_backup`.
- **Run from a copy outside the repo**, as you did (`evidence/round4/snap.sh` makes one and checks it): a commit by another session can swap the lane's files under a running suite.
- Re-run: `bash tests/run.sh /private/tmp/<dir>` (about three minutes); `bash tests/mutants.sh /private/tmp/<dir> 8` (143 suite runs: 59 minutes tonight, eight at a time, under load averages of 8 to 22; a third argument such as `'F'` runs only round 4's 17, about nine minutes); `python3 tests/claims_check.py <suite output> <mutants output>`.
- Red first: put `round3/nb_core.py.round3` in a copy as `nb_core.py` and run the same `tests/run.sh`.
- Your `lib3.sh` reads `LANE_OVERRIDE` and `FXBASE`; that is all I set to re-run your scripts.

## What I built or changed (sizes in bytes)

`nb_core.py` 162,476 (was 145,042) · `tests/run.sh` 139,316 (was 114,480) · `tests/mutants.sh` 33,823 (was 29,499) · `tests/claims.tsv` 21,000 (was 12,552) · `README.md` 30,721 (was 22,736) · `RESULT-quarantine-erase.md` 15,788 (new) · `evidence/quarantine-erase/` (new: 42 files, 70,106 bytes) · `evidence/round4/` (new: 51 files, 409,680 bytes) · `round3/` (new: round 3's engine, suite, mutants, claims, README and four more, as they were).

Unchanged, compared byte for byte with the copies in `round3/`: `nas_backup_watch.sh`, `seats/wednesday.conf`, `tests/claims_check.py`, `tests/scan_dry_lists.py`, `proposed/doctor_nasbackup_block.sh`. Unchanged by `git status` (not listed as modified): `nas_backup.sh`, `nas_backup_nightly.sh`, `nb_common.sh`, `jobs/nasbackup.plist.template`, everything in `proposed/`, `seats/wednesday.tokens`, the HOLD files, `CENSUS.md`, `BRIEF.md`, the ANSWER files, the two earlier RESULT files. `git status` of the lane at the end:

```
 M 2_Project_Files/nas-backup/README.md
 M 2_Project_Files/nas-backup/STATUS.md
 M 2_Project_Files/nas-backup/nb_core.py
 M 2_Project_Files/nas-backup/tests/claims.tsv
 M 2_Project_Files/nas-backup/tests/mutants.sh
 M 2_Project_Files/nas-backup/tests/run.sh
?? 2_Project_Files/nas-backup/evidence/quarantine-erase/
?? 2_Project_Files/nas-backup/evidence/round4/
?? 2_Project_Files/nas-backup/round3/
```

Run state on the drive, git-ignored, written by the one dry run and one held `--run`: `logs/wednesday/` (the dry run's lists), `manifests/wednesday/` (its manifest, its symlink lists and the 15 names lists), `state/wednesday.json` (one more `held` record).

---

(ROUND 3's status follows as that seat wrote it; its first line was `READY FOR QA`.)

READY FOR QA

**Both tasks of ANSWER-4 are done. `RESULT-secrets-move-2.md` was written first (first line DONE): all 37 folders moved, counts equal, 0 left under the mirror.** This section is TASK 2, round 3 of the backup job.

# ROUND 3 (2026-11-27): one rule, "unproven means failed" (ANSWER-4.md)

Fresh build seat "nas-backup" (WED-170), Fable 5.2, 2026-11-27 16:43 to 19:36 AEDT. The earlier seat's files were my handover. Read whole before I changed anything: ANSWER-4, BRIEF, ANSWER-1, ANSWER-2, ANSWER-3, RESULT-secrets-move and its three evidence files, STATUS round 2, the second verdict, and of its `scripts/` the files `K_my_mutants.sh`, `lib2.sh`, `N1`, `N1x`, `N3`, `N6`, `N11`, `S_scan_real_lists.py` and `r1_adapted/lib.sh`. Read whole later in the session: `N8_proposals.sh` and `S_over_exclusion.py`. **Not read line by line:** the five `r1_adapted` attack scripts (I read their heads, checked them for real mount paths and ran copies of them) and most of `raw/` (I read `K_my_mutants.out` and `S_scan_real_lists.out` whole and part of the probe output). The brief asked for the folder whole; this is short of that. Round 2's files are kept in `round2/`, round 1's in `round1/`. ROUND 2's status follows this section as that seat wrote it.

**Holds, kept:** nothing written to any NAS mount except TASK 1's 37 licensed renames (and the parent folders for them inside the existing quarantine); nothing armed; no `launchctl` verb that changes anything (`launchctl list` only); the three HOLD files stay; no shared file edited (proposals only); no commit, no push; no mail, board or chat post. Evidence that nothing is armed: `evidence/round3/real_lane_checks.txt` (0 `nasbackup` rows in `launchctl list`, 0 plists in LaunchAgents, 0 templates in `scheduler/jobs`, each beside a control of 1 for `naspush`; `--run` exits 3 under the hold).

## The numbers

| | Round 2 | Round 3 |
|---|---|---|
| Suite (`tests/run.sh`, fake NAS only) | 319 passed, 0 failed | **568 passed, 0 failed** |
| Mutants (`tests/mutants.sh`) | 63 of 63 of the seat's; **15 of the second checker's 24 survived** | **126 of 126 caught, each by the test named for it (final pass, one version of every file)** |
| The second checker's 15 survivors | survived | **15 of 15 caught, each by a named test** (table under item 9) |
| The checker's attack scripts N1, N1x, N3, N6, N11, re-run from a copy against round 3 | GOOD while planned files were unreadable (his N1a, N1b, N1c, N1x) | **0 GOOD on any attack night** of N1 and N1x; every GOOD line there is a control or a recovery night (`evidence/round3/checker_attacks_rerun/`) |
| The first checker's attacks A, B, B7b, C, H (his adapted copies), re-run the same way | held in round 2 | **destruction oracle: 27 of 27 held, 0 contents lost** with the chunked engine; H: 0 GOOD in 17 failing nights; B: 61 marked files kept out, 3 arrive, the same three the second verdict lists as notes (`Agent Mail.md`, `Data sec` with a space, `DS-NexusAI`) |
| Real dry run | 1,012,092 files, 68.05 GiB | **1,012,110 files, 68.27 GiB**, exit 0, no PROBLEM line |
| Secret-shaped names in the real dry list, lane's scan | 0 | **0** |
| The same list, the checker's own scan, tiers A and B | 0 and **344** | **0 and 0** |
| Coverage claims in this file checked by a program | not done (one claim was wider than the suite) | **140 claims, 0 not supported** |

## Where the brief and the verdict differed, and which I took

ANSWER-4 says the verdict's measurement wins where they differ, and to say so. Three places:

1. **Item 7, how far the name rule goes.** The brief asks for the 23 conventional names and the two real files' patterns, then "0 by each" of the two scans. The verdict's own acceptance step is narrower in words and wider in fact: its scan must read 0 in tier A **and tier B**, and tier B holds whole patterns (anything named `*credentials*.json`, `secrets.<ext>`, `.crt`, "private key" in a name) that matched 344 real paths in round 2, most of which the checker himself judged not secrets. I took the verdict's measure: the rule now covers every tier B pattern, and both scans read 0. **The cost is 373 real paths left out that are mostly not secrets** (table under item 7). That is a decision someone may want to reverse; it is question 1 below.
2. **Item 3, what happens after a sample finding.** The verdict's smallest fix was "delete the index row, the next plan re-sends". The brief is stricter: repaired in that run or the night fails. I built the brief's, and one step more, because the checker's own attack N3d showed the brief's wording was not enough on its own (below).
3. **Item 1, when the plan is made.** The brief says "the plan made at the start of the run". The tool plans each set when that set starts, as rounds 1 and 2 did, so the destination listing and the file list are fresh when a 30-hour copy reaches its last set. Nothing leaves a set's plan once made. I kept this and am saying so plainly; if "one plan for all sets at second zero" is wanted, it is a small change and costs memory (a million file records held at once).

## Per item: what changed, and the test that owns it

Every test and mutant named here is a line of `tests/claims.tsv`, and `tests/claims_check.py` checked each against the suite output and the mutant output before this section was written: 140 claims checked, 0 NOT SUPPORTED (`evidence/round3/claims_check.out`).

### 1. A planned file that cannot be read is NOT DELIVERED. There is no "gone" category. Fixed.
- `prove_arrival` has four verdicts: proven, unstable, differs, **unreadable**. Unreadable is any failure to read the source: permission, I/O error, privacy refusal, no such file, no longer a regular file. It fails the night unless `source_deleted()` then proves a deletion: the set's root is still the folder that was listed (device and inode), the file's parent folder can be listed, and the name is absent from it, twice, 0.2 s apart.
- Deleted files are counted and named three times: in the set's lines, one `DELETED AT SOURCE: <set>/<path>` line each in the run's last lines, and in the manifest and the state. **The limit: 5 files per set, or 0.1% of the set's plan if that is more** (`max_deleted_files`, `max_deleted_fraction`; the conf cannot raise them above 100 files and 1%). Above it the night fails.
- **The accounting is one subtraction:** planned, minus proven, minus provably deleted. Nothing else can take a file out of the plan. Wednesday's wider exception in ANSWER-3 is withdrawn in the code as the brief withdrew it by name: no line of round 2's "vanished" logic is left.
- **A strict reading I took, and what it costs:** the brief says "its parent directory is listable AND the name is absent". A file whose parent folder was itself removed has no listable parent, so it is NOT DELIVERED and the night fails. On a live tree a folder with planned files in it that is removed mid-run fails that run; the next run plans afresh. Question 2.
- Tests, T21 (12 cases, lifted from the checker's N1, N1x, N2): mode-000 file from night 1 (fails both nights, named with its reason, marker not on the NAS; readable twin GOOD); changed-then-unreadable (fails two nights running, destination still old; readable again GOOD); a 31-file folder unreadable between listing and copy; every folder unreadable mid-run with all 20 files changed (the question of ANSWER-3: NOT PROVEN 20, 20 destination copies still old, not GOOD; readable again GOOD and none stale); the set's root moved away mid-run; one real deletion (GOOD, counted, named); six deletions fail and five pass; parent folder gone; file became a folder; destination copy unreadable; delivered then unreadable; and the deletion proof as a function (7 assertions).
- Mutants caught: R01 to R06, K19, K02, Q02.

### 2. A set whose plan holds zero files fails the night, first run included. Fixed.
- Zero files fails with or without folders and with or without an earlier good run. The rule is applied to the plan as it finally stands (after names differing only in case are taken out).
- `match_everything` refuses a pattern that matches every plain probe name or every dotted one: `*`, `?*`, `**`, `*.*`, `[!~]*`, `*[a-z0-9]*`. What still empties a set at run time is caught by the zero rule.
- **One real set needs the allowed-empty mark, as the brief asked me to say:** `CODING/Docker - Containers` holds one folder and no file in scope (both dry runs today). `seats/wednesday.conf` now has `allow_empty=CODING/Docker - Containers` with its reason; the END count is 49. Without it every night would fail on that set. Question 3.
- **The baseline of the fall rule is kept twice** (state file and a `meta` row in the index), so a damaged state file the same night as a mistyped exclusion no longer reads GOOD. A first run with nothing to compare against prints `NO BASELINE` per set.
- Tests, T22: folders and zero files on a first run (exit 8); one file added (GOOD); `allow_empty` (GOOD, said in the output); five emptying patterns each refused; the pattern rule as a function (7 refused, 7 ordinary accepted); damaged state plus 20 of 25 files excluded the same night (fails, both numbers printed); the nightly job on a set that fell 25 to 8 (fails; it has no way to accept, the checker's K10); a set with a broken scope is not copied (K03). T11: a set whose only files are a case-colliding pair has an empty plan.
- Mutants caught: K21, N05, R26, R27, K10, K03, R38.

### 3. A sample finding is repaired in the same run, or the night fails and keeps failing. Fixed, and widened.
- The sample is taken first. A sampled file that is no longer proven loses its index row at once (committed) and joins tonight's copy list; the engine's `--backup` keeps the wrong destination content in `versions/`. If the repair is not proven the file is NOT DELIVERED. With no index row, every later night compares it by content, so it cannot rest on the old proof again.
- **Widened after re-running the checker's N3d against my first version.** With 30 destination copies altered and a sample of 10, my first version repaired the 10 it had looked at and said GOOD over 20 it had not. That is the brief's wording satisfied and its rule broken. Now **one wrong destination copy withdraws every earlier proof of that set**: the remaining unsent files are all read back in the same run, what agrees is proven again, what does not is re-sent. If the cap passes first the night fails and the next run continues the comparison. N3d re-run: night 1 GOOD with 0 altered copies left (was 13 left after night 2, 4 after night 6).
- What this does NOT change: the chance that the sample finds a single altered file at all. That is the stated limit (README, with the checker's numbers).
- Tests: T12 (found, repaired in the same run, wrong content kept in `versions/`, counted); T3 with the sample switched off (a same-size change at the source is still seen, by its stat alone, so the repair cannot hide a tool that trusts its index); T23 (immutable destination copy: fails; next night with the sample switched off still fails and sends it again; the night after still fails; replaceable again: GOOD; ten altered, all sampled: all repaired; 35 altered with a sample of 3: full read-back, all 35 repaired in one night).
- Mutants caught: R07, R08, R36, Q09, K11, M20.

### 4. A `set=` source is refused in both directions of containment. Fixed.
- `forbidden_roots()` finds the real folders: other seats' trees (a name containing `tuesday` or `friday` at the top of the drive or beside this seat's tree) and the other client's folders (a name containing `datasec` at the top of the drive or one level below). A source is refused when it is such a root, inside one, or an ANCESTOR of one. A source that is an ancestor of this seat's own tree is refused too. One set inside another is refused unless the outer set carries the matching `exclude_path` (the real conf has exactly one such pair, with its exclude).
- Also: in every set a FOLDER named exactly `tuesday` or `friday` is excluded (the contained-word rule stays limited to the seat's own tree).
- On the real drive the roots it finds today are three: `/Volumes/DevMASTER/TUESDAY`, `/Volumes/DevMASTER/Notes (MASTER)/Datasec` and `/Volumes/DevMASTER/_handover/tuesday-seat` (`evidence/round3/forbidden_roots_on_the_real_drive.out`; this drive has no `!CODING/Datasec` folder). The real conf loads and none of its 15 sets is refused.
- Tests, T24: the drive root (exit 2, "ANCESTOR of the forbidden root", nothing started, 0 copies of TUESDAY's, FRIDAY's or Datasec's markers); the folder that holds the client folders; a folder holding a `tuesday-handover` folder; ordinary folders named one by one arrive; the roots as a function; an ancestor of the seat's own tree where no forbidden root exists; nested sets with and without the exclude; a folder named exactly as a seat. T14 from round 2 still covers "inside a root", and now also a source four levels down, deeper than the root search looks, given by its real path and through a symlinked parent: there the rule on every path component is the only thing that refuses.
- Mutants caught: R09, R10, R11, R12, Q16, N23.

### 5. Damage reaches a seat whoever finds it; a damaged index never leaves the lock. Fixed.
- **A damage notice on the drive.** Whoever finds a damaged state file or index appends a line to `state/DAMAGE_NOTICE_<seat>.jsonl` (what, when, who found it, where it was moved). While it exists the watch says so at every call and exits 5, and the doctor block prints its own hard-failure line, `NAS BACKUP STATE WAS FOUND DAMAGED`, held or not, at every boot. Only `nas_backup_watch.sh --ack-damage` clears it (moved into the lane's quarantine). The nightly job can find damage; it cannot use the notice up. This also ends the mislabel of minor 15.
- **A valid state is checked, not assumed** (`validate_state`): JSON that is not a state, missing fields, and a recorded time more than 5 minutes in the future are all damage: one plain line, the file moved aside.
- **A damaged index** is moved aside in one plain line and an empty one started; the run goes on and compares by content. Everything after the lock is taken runs inside `try/finally`, so the lock is released after any error, and an unexpected error is one line (`FAILED: the run stopped on an unexpected error`) with the attempt recorded as failed, not left `running`.
- **A dry run moves nothing:** a damaged state file or index is reported and left where it is (the verdict's note).
- Tests, T25 and T16: the checker's N6b from "damaged on day 2, nightly job is the next reader" to doctor failing hard on day 3 and day 4, also while held, until `--ack-damage`; damaged index (dry run: said, untouched; real run: GOOD, moved, no lock left, no traceback); dry run with a damaged state; two shapes of valid-JSON-invalid-state (no traceback from watch or nightly); `last_good` 400 days ahead (damage; the nightly job decides RUN, not skip); a run that cannot write its manifest (one line, lock released, next run GOOD).
- Mutants caught: R13 to R18, K08, R33, N11.

### 6. Proof is saved as it goes. Fixed, by copying in chunks.
- The engine is called per chunk of 200 files (`chunk_files`) or 2 GiB. After each chunk every file of it is proven and the proofs are committed to the index (`Saver`, at least every 200 files) before the next chunk starts. Files found identical during planning are saved as they are found. The cap is honoured between chunks, between files in the proof loop and in the comparison loop, not left to the watchdog.
- So an interruption costs at most the one chunk in flight. The checker's N11a re-run: after SIGTERM 200 index rows (was 0); the resume re-read 160 files (was 354) and sent the rest. N11b under the cap: 200 rows, then 574, then done (was 0, 331).
- **An interruption cannot leave the state saying good:** `good` is written in exactly one place, after the accounting. Tested for SIGTERM, SIGHUP, the cap and the watchdog.
- One log, one error file and one list per set per run, however many chunks (`logs/<seat>/<stamp>_run_<set>.rsync.log`); the run prints a line per chunk and a running count.
- Tests, T26: 25 files in chunks of 5, the engine hangs in its third call, SIGTERM (and again with SIGHUP): 10 index rows, state never good, attempt failed, lock released, engine stopped; the resume is GOOD, sends 15 and re-reads nothing proven. The cap: exit 4, rows kept, the unreached set named, next run GOOD. The watchdog with a blocked read (test-mode hooks `NB_TEST_WATCHDOG_MARGIN` and `NB_TEST_HASH_DELAY`, ignored outside test mode, which is also tested).
- Mutants caught: R19, R20, K17, R34, R35, K01.

### 7. The name rule: wider, and said to be incomplete. Done as best effort.
- Added (list in README): the 23 names of the checker's table, the two real files' patterns (`local.settings.json`; a `.auth` folder), and every tier B pattern of his scan.
- **Both scans on the fresh real dry list (stamp `2026-11-27_172323_81704`, 1,109,051 paths): the lane's `tests/scan_dry_lists.py` 0 (controls 52,213, 5,422, 7,060); the checker's `S_scan_real_lists.py` run from where it lies: tier A 0, tier B 0, tier D 0, unit controls 22 of 22, the same three positive controls.** His access check on the same list: 1,012,105 files asked, 0 not readable by this user, 5 gone since the listing (`evidence/round3/scan_*`).
- README carries the honest paragraph: a name rule cannot be complete; the real protections are the two secrets-folder names in any case, the hard-link rule, the forbidden roots, and the share being private.
- **What it newly leaves out of the real scope: 373 paths** (`evidence/round3/over_exclusion_of_the_round3_name_rule.out`, names only): 169 files with `credential` in the name and a data extension (test evidence, .json and .txt), 98 `secrets.<ext>` (91 of them `.ts` source files), 68 `.crt`, 24 with private-key, signing-key or mnemonic in the name (18 of them .html documents), 7 by exact name (`auth.json`, `token.json`, `local.settings.json`), 3 paths of the `.auth` folder, 2 `htpasswd*`, 2 `*.tfvars`.
- The checker's own over-exclusion walk (`S_over_exclusion.py`, a copy with one line added because round 3's rule object reads `state_dir`) on the real scope at 19:37: 2,767 entries excluded as secret-shaped, against 2,697 in the 17:23 dry run. The tree is live and had grown by about 13,600 in-scope files in those two hours by his count (1,025,685 against 1,012,110); 56 of the 70 extra entries are `.env` templates. Its table of names is in `evidence/round3/over_exclusion_checkers_S_over_exclusion_adapted_one_line.out`: by far the most are templates (`.env.example` 1,606), `.npmrc` 132, `secrets.ts` 92 and the certificate and evidence names listed above.
- Tests, T28: the checker's 40 names (program-checked against his script: all 40 planted), 25 more (one is an ordinary-named file inside a `.auth` folder), 10 ordinary neighbours that must arrive (`secrets.example.yml`, `credentials.ts`, `tokenomics.md` among them); the lane's scan passes a clean list and fails one holding the two real names.
- Mutants caught: R28 to R31.

### 8. The Minors.
| Minor | State | Test and mutant |
|---|---|---|
| 10 the hold started the three-day clock | **Fixed.** A refusal under the hold is recorded as `held` and never starts the clock; the first run, fire or check after the hold is lifted starts it then, once. Pre-round-3 records of such refusals (the real lane's state has two) are recognised and relabelled at that moment | T27 with the real lane's state shape: lifted four days later, not overdue, doctor quiet; overdue three days after the lift. R21, R22 |
| 11 SIGHUP | **Fixed.** Handled like SIGTERM | T26 (the HUP half). R32 |
| 12 the mount checked once | **Fixed.** Checked before every set, before every chunk and before GOOD | T27 (the share leaves the table during set 1: not GOOD, set 2 not started). R23 |
| 13 valid JSON that is not a state; `last_good` in the future | **Fixed** (item 5) | T25. R16, R17 |
| 14 duplicate conf keys | **Fixed.** A key given twice is refused by name | T22. R25 |
| 14 the END marker does not seal content | **Left, with its reason:** a checksum would catch accidental damage, not an edit, and every hand edit of the conf would then need a tool. Stated in README. The checker's N5a still shows it | none |
| 15 doctor mislabelled damage | **Fixed** (item 5) | T25 |
| 15 a reused engine group id | **Fixed.** The lock records when the engine's group leader started; a live process with that id and another start time is not the engine. A lock written by round 2 code has no such record and still fails closed, as the checker's N7c shows | T27 (both ways). R24 |

The limits the checker asked to have STATED are in README under "Limits": the sample (0.059% a night; one altered file in the Secuura set expected after 14,678 nights, median 10,174; seat tree 6,630; test material 3,633), the slow shrink, unguarded growth, versions never pruned, `--accept-shrink` by hand only. No machinery was built for them.

### 9. Tests, and the claims program.
- **Every one of the checker's 15 surviving mutants is caught by a named test:**

| His mutant | Caught by |
|---|---|
| K02 unaccounted files ignored | T12 H1 (the accounting is now the only route to "not proven") |
| K03 broken scope still copied | T22, a new file in a broken set did not travel |
| K05 wildcards in `exclude_path` | T22, refused as not a literal path |
| K06 the engine accepts any tree name | T27, the engine called directly |
| K10 the nightly job accepts a shrink | T22, the nightly job on a set that fell |
| K12 test-mode fence on `nas_root` | T27, refused by the fence |
| K14 a missing destination folder ignored | T27, an engine that does not create one planned folder |
| K16 a dry run opens the index for writing | T1, no index file created |
| K17 the watchdog never armed | T26, a blocked read past the cap |
| K18 an engine seen only by its group id | T27, an rsync writing to this seat's folder with no recorded group |
| K19 an unreadable destination counts as proven | T21j |
| K21 a sharp fall accepted (zero with folders) | T22, first run with folders and zero files |
| K22 exit code 12 tolerated | T27, an engine that exits 12 |
| K23 a source need not be a folder | T22, a source that is a file |
| K25 the nightly job records no fire | T7, the fire and its decision are in the state |

  Where round 3 rewrote the line his mutant aimed at, the mutant in `tests/mutants.sh` breaks the line that now does that job; his K13, which did not apply in his run, applies here and is caught.
- `tests/mutants.sh` holds 126 mutants: the seat's 20 from round 1, the first checker's 18, round 2's 25, the second checker's 25, and 38 new on round 3's code. A mutant counts as caught only when the test NAMED for it fails.
- **The first full pass caught 118 of 126 by name, and the other 8 were my harness and my tests, not the tool** (`evidence/round3/mutants_round3_first_full_pass_118_of_126.txt`). Five were caught, but by another test than the one named, because round 3's new behaviour answers first: M20 (the sample repair hid a tool that trusts its index, and whether the old named test failed depended on the random sample), Q16 (the new root check refused the fixture before the component rule was reached), K17, R36 and R32 (I had named the exit-code line where the telling line was another). One, K07, was not caught at all and only looked caught: its own name, `tuesday-added-to-SEATS`, became a folder in the fixture path and made every source "forbidden"; the second checker's own K07 shows 184 FAIL lines starting at T1, which I take to be the same artefact. Two, N23 and R31, were genuinely untested guards: the real-path component rule (now masked by the root check at two levels) and the `.auth` folder rule (the planted file was also excluded by its own name). I added six test lines that reach those guards directly and one more planted name, renamed K07, corrected five names, re-ran the eight (8 of 8 caught, `mutants_round3_the_eight_corrected_rerun.txt`) and then the whole set again on the final files (the number in the table).
- **`tests/claims_check.py`** reads the suite output, the mutant output and `tests/claims.tsv` (140 claims: every test and mutant this section names, the checker's survivor list read from his own raw output, his 40 names read from his own script) and exits 1 if any claim is not supported. Two older mutants (M04, M10) were being caught by a different test than the one named, because round 3's new rules refused the same fixture earlier; an early pass that I stopped showed it, and the names were corrected and one fixture changed so the guard is really reached.

## The re-measured real dry run (17:23:22 to 17:37:48, reads only, exit 0)

It ran while a mutant run was loading the machine, so its 14 minutes are not a speed measurement (round 2's took 7).

| | Files | Bytes |
|---|---|---|
| WEDNESDAY tree, to `General/Wednesday` | 265,280 | 27.12 GiB |
| Testing Agent MAIN without Secuura's material, to General | 6,322 | 247 MiB |
| Eleven smaller general projects, to General (one of them empty and allowed to be) | 8,099 | 0.82 GiB |
| Secuura client folder, to `Secuura/Wednesday` | 587,130 | 30.95 GiB |
| Secuura's test material from Testing Agent MAIN, to Secuura | 145,279 | 9.14 GiB |
| **Would copy** | **1,012,110** | **68.27 GiB** |

- Excluded entries: 7,716. By secret shape 2,697 (env-file 2,128; credential-file 406; key-or-certificate 122; private-key-or-wallet-name 24; credentials-folder-name 14; terraform-variables 2; credential-store 1); another client's name 1,125; other seats' names 356; `.git` 231; quarantine 177; rebuildable 1,864; system 237; by the conf 1,017; hard links 9; the live database folder 2; the tool's own run-state folder 1.
- 982 symlinks recorded; 14 files left out for case-only name clashes; no PROBLEM line; 15 engine list checks, each with 0 deleting lines.
- In-scope paths carrying a Datasec project name (reported, not excluded): nexusai 4,558; hpsm 2,666; mps 9; quickquote 6; mypki 2; oxpd 2; cypherkey 1.
- What it listed on the NAS, read-only: `/Volumes/DEV-Working/General/Wednesday` (1 entry) and `/Volumes/DEV-Working/Secuura` (1 entry); the destination below them does not exist yet. NAS unchanged: listings, folder mtimes and `df` identical before and after (`evidence/round3/nas_diff.txt` is empty, rc 0).
- **This was the one licensed dry run, and two edits to `nb_core.py` came after it started.** (1) A real run now prints one `DELETED AT SOURCE` line per deleted file in its last lines: no dry-run path. (2) The empty-plan and fall rules now use the file count after case-colliding names are taken out. I found that from this dry run's own output: its `NO BASELINE` note for the Secuura set says 587,140 where the scope line says 587,130. The numbers above are not affected (they come from the scope lines); the notes in the evidence file carry the old count for two sets. The suite (568) and the final mutant pass ran on the final code.

## What I could not make sound, or chose not to

1. **The sample is a sample.** One altered destination file among 587,130 will almost never be looked at. Round 3 makes a finding count for the whole set; it does not make findings likely. Only a periodic full read-back would, and the brief said not to build that this round.
2. **The strict deletion rule will fail honest nights on a live tree.** A folder removed during a run takes its planned files with it as NOT DELIVERED. I could make it sound the other way (accept a file when the nearest surviving ancestor is listable and lacks the next folder name), but that is wider than the brief's sentence, so I did not.
3. **The name rule.** It is a list. It reads 0 on two scans today and that is not the same as "no secret travels". A secret in `config.json` or `notes.md` is invisible to it.
4. **The END marker counts, it does not seal** (minor 14, left).
5. **The orphan engine after SIGKILL** still finishes the chunk it was given: now at most 200 files, not a whole set.
6. **The state file has no lock between the watch and a running backup.** Unchanged, read in the code, not reproduced.
7. **Order at the very end of a good run:** the COMPLETE marker is written on the NAS before the state file records good. If the state write then fails, the NAS says complete and the drive does not; the next night runs again. The safe direction, but two records can disagree.
8. **A lock written by round 2 code** (no engine start time) beside a reused group id still refuses to clear until that process ends. Fails closed.

## My own slips, this round

- **My first sample repair was the brief's letter and not its rule** (item 3). I only saw it because I re-ran the checker's N3d instead of trusting my own test.
- **I stopped and restarted the mutant run three times before it ever finished.** First: the harness did not copy `scan_dry_lists.py`, which a new test calls. Second: I decided late that every deleted file must be named in the last lines. Third: the empty-plan count (above), found from the dry run's own output. Each time I stopped the run rather than mix code versions in one result. **Then the first pass that did finish showed 8 mutants not caught by their named tests** (item 9): all eight were faults in my tests or my mutant list, and two of them were guards I had left without a test of their own. The final pass is one version of every file, with the sha256 list taken before and after it in `evidence/round3/`.
- **Four mistakes in my own new tests, found by their first run:** a `find` whose error line was counted as a marker; a Python check run without the test-mode variable; a helper that waited 60 s on a child's open pipe; a control name my own scan could not match.
- **The chunk size.** I first set 2,000 files. The checker's N11a showed 0 index rows after an interruption of a 1,500-file copy, so the proof of the first copy would still have been lost in pieces of several minutes. It is 200 now.
- **A quoting error in `tests/mutants.sh`** (caught by `bash -n` before any run).
- In TASK 1's first precheck one exit code was read after a pipeline, so it is the filter's, not the command's (a hook said so). The line it sits beside is the mount line itself, which is the evidence; the later process check does not repeat it.

## What is NOT tested in round 3

- **Any write to the real NAS by this tool.** The chunked copy is thousands of engine calls into one `--backup-dir` and one temp folder on an SMB share: first real run is its first test. So is the read-back at scale and the full read-back after a sample finding.
- **Scale.** A million files: about 5,000 chunks, the per-chunk overhead (an engine start, a mount-table read, two `ps` calls), memory, the index at a million rows. Not measured. The 31.6-hour estimate is the old job's file rate and includes neither the proof nor the chunk overhead.
- **launchd.** No job loaded. The privacy prompt for `python3` and `rsync` under launchd is exactly a "cannot read" case: under round 3 it fails the night and names files, it cannot read GOOD. That path is reasoned, not run.
- **The doctor block inside the real `doctor.sh`**, and the launcher carrying its lines into a boot prompt. The block was run with doctor's three helpers copied, as in round 2.
- **The real code path outside test mode** (`nas_root` fixed, the real mount table, `statvfs`), beyond the dry run and the refused `--run`.
- **A case-sensitive source.** The scratch volume folds case; collisions are supplied as a listing (T11).
- **`forbidden_roots` on any drive but this one and the fixtures.** It looks two levels deep; a client folder kept three levels down would be missed by it (the name exclusion inside every set still applies to `datasec`, and exact seat-named folders are excluded in every set).
- **Python 3.9** beyond T10 (one real run under `/usr/bin/python3`, still green).
- **The checker's N8 (proposals and install order) was not re-run**; the template and the install proposal are unchanged since round 2, and T20 still passes.
- **The claims program checks that a named test passed and a named mutant was caught.** It does not judge whether a test is a good test.

## QUESTIONS (none blocks QA)

1. **The 373 paths.** Keep the name rule as wide as the checker's tier B (two scans read 0; test evidence, `secrets.ts` sources and public certificates are left out), or narrow it to the 23 names and the two real patterns (his tier B then reads about 340 on the real list)?
2. **Deleted folders.** Keep the brief's strict sentence (a planned file whose folder was removed mid-run fails the night), or accept a deletion proven one level up?
3. **`allow_empty=CODING/Docker - Containers`:** keep the mark, or drop the set from the conf (it is then reported as not backed up at every run)?
4. Round 2's open questions stand: `0_Brain/reference/` stays out; the token counts are reported to Kam.

## For the checker: where to look first

- `nb_core.py`: `prove_arrival`, `source_deleted`, `deleted_allowed`, the accounting near "THE ACCOUNTING" in `backup_body`, `plan_set` (the empty-plan block), `forbidden_roots`, `validate_state`, `note_damage`, `Index`, `Saver`, `make_chunks`, `hold_lifted`.
- Re-run: `bash tests/run.sh /private/tmp/<dir>` (about three minutes); `bash tests/mutants.sh /private/tmp/<dir> 8` (126 suite runs: about an hour; a third argument such as `'M20|Q16'` runs only those); `python3 tests/claims_check.py <suite output> <mutants output>`; `bash nas_backup.sh --dry` (reads only); both scans on its stamp.
- **If you copy the lane the way `K_my_mutants.sh` does, copy `tests/scan_dry_lists.py` too**: T28 calls it, and without it the control fails. **And do not put a seat's or the other client's name in a mutant's folder name:** the fixture lives under it, and the tool then refuses every source for that reason alone (your K07 in round 2, mine in this round's first pass).
- Your earlier instruments that no longer apply as written: `S_over_exclusion.py` builds a bare context object, and `Rules` now reads `ctx.state_dir` from it, so it needs one more attribute (my adapted copy is in `evidence/round3/`); the N11c patch looks for `signal.alarm(int(cap) + 900)`, which is now `signal.alarm(int(cap) + margin)`; the test-mode variables `NB_TEST_WATCHDOG_MARGIN` and `NB_TEST_HASH_DELAY` do what that patch did. N7c's owner record needs `engine_started` to exercise the reused-group fix. The output line that said "gone from the source during the run" now says "deleted at the source and confirmed absent". Engine lines read `chunk N of M, engine pass P`.
- Evidence: `evidence/round3/`: the suite output (the control of the final mutant pass, 568), the final mutant output (126 of 126) with the sha256 of every file before and after that pass (identical), the first full pass (118 of 126) and the re-run of its eight, the claims check, the dry run with the NAS before and after, both scans, both over-exclusion counts, the re-runs of both checkers' attack scripts, the forbidden roots found on the real drive, the lane checks. **No file of the tool or its tests changed after the final mutant pass ended at 19:35.**

## What I built or changed (sizes in bytes)

`nb_core.py` 145,042 (was 100,803) · `tests/run.sh` 114,480 (was 63,242) · `tests/mutants.sh` 29,499 (was 15,729) · `tests/claims_check.py` 5,306 (new) · `tests/claims.tsv` 12,552 (new) · `tests/scan_dry_lists.py` 5,433 (was 3,478) · `README.md` 22,736 (rewritten) · `seats/wednesday.conf` 7,856 (one `allow_empty` line, END count 49) · `nas_backup_watch.sh` 3,142 (`--ack-damage`) · `proposed/doctor_nasbackup_block.sh` 4,015 (the damage line) · `proposed/doctor.proposed.md`, `INSTRUCTIONS-for-other-seats.md`, `PORTABILITY.proposed.md` (round 3 notes) · `RESULT-secrets-move-2.md` 15,828 (new) · `evidence/secrets-move-2/`, `evidence/round3/`, `round2/` (new). Unchanged: `nas_backup.sh`, `nas_backup_nightly.sh`, `nb_common.sh`, `jobs/nasbackup.plist.template`, `proposed/install_all_jobs.proposed.md`, `proposed/launcher.proposed.md`, the HOLD files, `CENSUS.md`.

---

(ROUND 2's status follows as that seat wrote it; its first line was `READY FOR QA`.)

# ROUND 2 (2026-11-27): answer to the NO GO verdict, under the rulings in ANSWER-2.md

Build seat "nas-backup" (WED-170), Fable 5.2. Round 1's text is kept below, unchanged, under "ROUND 1". Round 1's files are kept in `round1/`.

**Context, as ANSWER-2 asked:** I cannot measure my context use. I judged it under the 70% mark when I started, did the whole round in this session, and did not stop early. A checker should weigh that: this was a long session, and the engine was rewritten whole, not patched.

**Holds, kept:** nothing written to the NAS in this round (ANSWER-1's licensed move is the one exception, done and reported in `RESULT-secrets-move.md`); nothing armed; no `launchctl` verb; the three HOLD files stay; no shared file edited; no commit, no push.

**Also from ANSWER-1, for whoever reads only this file:** the sweep of the Backup share found 37 more secrets folders on the old mirror, eight of them further copies of the two that were moved. I touched none. See `RESULT-secrets-move.md`.

## The numbers

| | Round 1 | Round 2 |
|---|---|---|
| Suite (`tests/run.sh`, fake NAS only) | 167 passed, 0 failed | **319 passed, 0 failed** |
| Mutants (`tests/mutants.sh`) | 20 of the seat's own caught; 14 of the checker's 18 survived | **63 of 63 caught**: the seat's 20, the checker's 18, and 25 new on round 2's code |
| Real dry run | 1,012,113 files, 67.83 GiB | **1,012,092 files, 68.05 GiB** |
| Secret-shaped names in the real dry list (independent scan) | 240 | **0** (the same scan run on round 1's list finds the 240) |

Evidence: `evidence/round2/`.

## Per finding: what changed, and the test that owns it

### 1. Blocker: false GOOD. Fixed.
- **GOOD now means every in-scope file is proven at the destination with the source's content.** Every file a run sends is compared by sha256 afterwards, source against destination, with the source unchanged across the read (`prove_arrival` in `nb_core.py`). A file enters the index only when proven. A file not sent rests on an earlier proof (same size and its exact stat in the index), and 40 a night per set are re-hashed.
- The engine's exit code decides nothing. Exit 23 or 24 is survived only because every listed path is then proven one by one.
- An undelivered file fails the run, is named in the last lines (`NOT DELIVERED: <set>/<path>`), counted and named in `state/<seat>.json`, and the watch's line names the first one.
- Tests, T12: the checker's trigger H1 (destination copy immutable, same-size change): not exit 0, no GOOD, file named, state counts it, the next night with nothing changed is still not good and sends it again; lifted lock: GOOD. Trigger H2 (stub engine skips one file, exits 23): not exit 0, file named, the file that did arrive is current. Exit 23 with everything arrived: GOOD. A destination copy changed behind our back: caught by the sample.
- **The checker's mutant Q02 (arrival check vacuous) is red: 14 FAIL lines.** Q09 (sample ignored): red.
- **One place I did not follow ruling 1 to the letter, and why.** It says exit 23 fails "unless every listed path is proven arrived". A listed file that no longer exists at the source when it is checked cannot arrive. I count it as gone from scope, not as a failure; otherwise a temp file deleted mid-run fails the night. It is counted in every run ("gone from the source during the run").
- **New behaviour to know.** A file that changes while the run is copying is sent again, up to two more passes, each into its own `versions/<stamp>_passN/`, so a re-send never overwrites the copy kept from the night before (T12; mutant N20 red). A file that changes after every pass is never proven, so the run FAILS and names it. On a live tree one constantly-written file could fail every night until it is excluded. Not exercised on the real tree.

### 2. Blocker: secrets. Fixed, by shape, any case.
- `secret_shape()` in `nb_core.py`, on the lower-cased name of every path component: contains `4_credentials` or `3_access_keys`; starts `.env`, contains `.env.`, ends `.env`; the key and certificate extensions, also before a further suffix; `.tfstate`; ssh key names; credential stores; deploy-key and credential file names. The full list is in README.
- **Over-exclusion is the accepted cost, and README says so:** `.envrc`, `.env.example`, a Keynote `.key`, `id_rsa.pub`, every `.npmrc`.
- A regular file with more than one hard link is skipped, counted, and named in the manifest.
- The run summary counts exclusions per shape and never prints a name.
- Tests, T13: 35 marked files (the checker's 12 case variants and 24 unlisted shapes, with a few more, and a hard link into `4_Credentials` under an ordinary name): 0 on the fake NAS; the neighbour arrives; a marked file planted by hand is found by the same count. Mutants Q10, M02, N07, N08, N09 red.
- **Real dry list:** `tests/scan_dry_lists.py`, written separately from the tool's rule, reads the 1,109,007 paths of the round 2 dry run: 0 secret-shaped, 0 containing `datasec`. Positive controls: 52,189 `.md` paths, 5,422 ordinary names containing `env`, 7,060 ordinary names containing `key`. The same scan on round 1's list exits 1 with 240.
- **Excluded by secret shape in the real scope (entries, counts only):** env-file 2,128; credential-file 130; key-or-certificate 54; credentials-folder-name 14. Total 2,326. Hard-linked files skipped: 9 (git objects in a bare repository inside Secuura's test material).

### 3. Blocker: other clients. Fixed as ruled, with one stricter choice.
- **Sources:** each `set=` path is resolved with `realpath` first. Any component of the given or the real path that CONTAINS `datasec`, `tuesday` or `friday`, any case, is refused. A source that is a symlink, or reached through a symlinked parent, is refused. T14: `Datasec-archive`, `alias -> Datasec`, a symlinked source, a symlinked clean parent: all exit 2, nothing started; the real path is named. Mutants Q05, Q16, N23 red.
- **Inside the sets:** a name containing `datasec`, any case, is excluded in every set (T14: `DataSec`, `DATAsec-notes`, `dataSEC`). A name containing `tuesday` or `friday` is excluded inside the seat's own tree only. Mutant Q01 red.
- **Project-name tokens are reported, not excluded**, per the corrected bullet. One data file, `seats/wednesday.tokens`, with a comment that the seat maintains it. `mps` is bounded as a whole word: a match must have a character that is not a letter or digit (or the start or end of the path) on each side, so `MPS Calculator` counts and `lamps` does not (T14).
- **Where ANSWER-2 and the verdict differed I took the stricter.** The corrected bullet says the seat's own tree is backed up whole. The verdict's Q01 wants the other-client name exclusion kept and tested. I kept excluding names that contain `datasec` (1,125 entries in the real scope) and other seats' names inside the seat tree (356), and made the project names report-only.
- **In-scope paths carrying a Datasec project name (reported for Kam, not excluded):** nexusai 4,558; hpsm 2,670; mps 9; quickquote 6; mypki 2; oxpd 2; cypherkey 1; the others 0.
- **Secuura material now lands under Secuura.** `Testing Agent MAIN/projects/secuura` is its own set to `Secuura/Wednesday/` (145,313 files, 9.14 GiB) and is excluded from the General set by path. Secuura folder total: 732,443 files; General: 279,649. Not moved: Secuura briefs and gate clones inside the seat's own tree stay with the tree in General. It can be done inside the lane with more `set=` lines; I did not, because the ruling says the tree is backed up whole.
- **Friday and Tuesday are removed from `SEATS`.** Only Wednesday can run. A TUESDAY or FRIDAY tree exits 2 for every command, a dry run included (T14). Their placeholder confs were moved to `round1/` (git shows them as deleted from `seats/`; they were moved, not deleted). INSTRUCTIONS says so as step 1, says STOP where a prerequisite is open, and no longer has any seat edit the shared installer.

### 4. Blocker: configuration fails open. Fixed.
- The conf's last content line must be `END lines=<N>`. No marker, or a wrong count, is refused with both numbers.
- An `exclude_path` that does not exist at the source is refused by name. A pattern that matches every name is refused.
- A set with zero files in scope, or one that fell by more than half against the last good run, FAILS the run with the two numbers. `--accept-shrink <card id>` accepts a real shrink once. The fraction is `max_drop_fraction` in the conf (default 0.5).
- Tests, T15: the checker's five cases (truncated; exclude lines lost; one-letter typo; `exclude_name=*`; emptied set) and a 17-to-3 fall; `exclude_path`, `exclude_name` and `exclude_name_in` each proven to keep a marked folder out. Mutants Q03, Q04, N01 to N06 red.

### 5 and 9. Major: the flag. Fixed.
- `first_attempt_at` is stored once and never rolled. When nothing at all is on record and the seat is not held, the watch starts the clock itself. No other script sets a mark. T9: forty refused fires over ten days, never armed: overdue, clock at day 1. Mutants N10, N22 red.
- A damaged state file: one plain line naming it, the watch exits 3, the file is moved into `state/_quarantine_<date>/`, and the next run starts clean and says so in its output and in `nightly.log`. T16 (truncated, garbage, empty). Mutant N11 red. **Cost, stated:** the record of the last good backup goes with the damaged file, so the three-day clock restarts at the damage.

### 6. Major: the card must reach a seat. Redesigned and proven.
- The nightly job calls the watch read-only and never prints the card.
- **The channel is doctor.** I read the real launcher: under `set -u` it carries one thing into a seat's boot prompt, doctor's `✗` lines (lines 400 to 417 and 904 to 914), each cut at 400 characters. `proposed/doctor_nasbackup_block.sh` prints a `✗` line that starts with the command to run, `nas_backup_watch.sh --card`, while a card is due and not recorded as raised.
- `--card` consumes nothing. It prints the command at every call until a seat records `--mark-raised`. The card id is fixed per gap and `decision_queue.sh` refuses a duplicate id (its line 155).
- **The launcher proposal is withdrawn: no launcher change is needed.** It names no variable at all now.
- Test, T8, from "three failed nights" to the place a seat reads: the nightly output has no card; the doctor block prints the `✗` line; cut at 400 characters it still names the command; running the command prints the card with all three attempts in the BLUF; a second call prints it again; after `--mark-raised` no `✗` and no card; a new gap gets a new id. Mutants N12, M18, M19, Q18 red.
- **Cost, stated:** a `✗` line stops a human launch at the preflight prompt until someone answers. It ends when the card is recorded as raised. One word in the block (`fail` to `warn`) removes the gate and, with it, the only path into a seat's prompt.

### 7. Major: type change. Fixed.
The old destination entry is moved into `versions/<stamp>/`, then the new one is copied. T17: folder to file and file to folder in one night: GOOD, both old contents under `versions/`, the next night GOOD. Mutant Q11 red.

### 8. Major: the lock after SIGKILL. Fixed for the lock; the orphan itself cannot be stopped.
- The engine runs in its own process group, recorded in the lock. `--clear-stale-lock` and a new run both refuse while any engine process of this seat is alive. T18: the tool is killed outright while its engine is running; clear refuses, a second run refuses; once the engine has ended, clear works and the next run is GOOD. Mutants N13, N14 red.
- **What is not fixed and cannot be from here:** after SIGKILL of the tool the engine still finishes its list. Nothing proves or records that run; the next run lists the destination and decides from what is there.

### 10. Major: tests. Every one of the 14 survivors now has a named test.
All 18 of the checker's mutants re-pointed at round 2's code: 18 caught (`evidence/round2/mutants_round2.txt`, the `Q` lines, each with the test that caught it). 25 new mutants on round 2's code (the `N` lines): 25 caught.

### 11. Major: install order. Fixed by removing the dependency.
The template now uses only the three placeholders the installer already renders, the schedule is read from the seat's conf, and the hold is enforced by the script launchd calls. T20: rendered with the unedited installer's own five `sed` expressions it lints OK with no placeholder left; the nightly script under the hold exits 3 and logs it. The proposal is ONE change, applied by Wednesday. Mutants M12, N19 red.

### 12. Minors. All fixed, as ruled.
- Loser of a simultaneous start: a lock with no owner record yet is "another run holds the lock", not STALE (T18; N15).
- Reused pid: the lock records when the holder started; a different start time is not the holder (T18; N16).
- PORTABILITY proposal says NN.
- Doctor block: HELD at most once a day; the seat comes from the tree through `tools/seat_note.sh` (T9).
- Daylight saving: the window is local wall time; tested on both change days for Australia/Sydney (T19; N17).
- `._*` matches files only (T13; N18).
- INSTRUCTIONS: no seat edits a shared file; `--max-seconds` is in the first-copy step; Friday's open questions say STOP.
- Schedule overlap across seats and the missing wake: stated in README as limits, not changed, as ruled.

### 13. Notes.
- **The real dry run now lists the real destination, read-only.** What it listed: `/Volumes/DEV-Working/General/Wednesday` (1 entry at its top level) and `/Volumes/DEV-Working/Secuura` (1 entry). The destination below them does not exist yet, so everything is new. The engine is never handed a NAS path in a dry run; it checks the list against an empty local folder. On a fake with an existing destination: the dry run lists it, measures "to copy" against it, and the NAS is unchanged by name, size, time and inode (T20, with a control that the snapshot changes when a file is added).
- A case-only rename still keeps the old spelling at the destination. Unchanged; stated in README.

## The re-measured real dry run (14:31:03 to 14:38:11, reads only, exit 0)

| | Files | Bytes |
|---|---|---|
| WEDNESDAY tree, to `General/Wednesday` | 265,214 | 26.89 GiB |
| Testing Agent MAIN without Secuura's material, to General | 6,326 | 247 MiB |
| Eleven smaller general projects, to General | 8,109 | 0.82 GiB |
| Secuura client folder, to `Secuura/Wednesday` | 587,130 | 30.95 GiB |
| Secuura's test material from Testing Agent MAIN, to Secuura | 145,313 | 9.14 GiB |
| **Would copy** | **1,012,092** | **68.05 GiB** |

- Excluded entries: 7,343. By secret shape 2,326 (above); another client's name 1,125; other seats' names 356; `.git` 231; quarantine 177; rebuildable 1,864; system 237; by the conf 1,016; hard links 9; the live database folder 2.
- 982 symlinks recorded; 14 files left out for case-only name clashes; no PROBLEM line; 0 deleting lines.
- NAS unchanged: listings, folder mtimes and `df` identical before and after (`evidence/round2/nas_diff.txt` is empty, rc 0).
- Estimate, unchanged in kind: about 32 hours for the first copy at the 8.9 files a second the old job managed, **plus reading every sent file back for the proof**, which round 1 did not do. Not measured.

## What I could not fix, or chose not to

1. **The checker's scripts were not run from where they lie.** Their fixtures write a conf without the END marker, which round 2 refuses by design, and their `lib.sh` writes into the checker's own scratch folder, which is not mine. I lifted the attacks into `tests/run.sh` (T12 to T20) and re-pointed all 18 mutants.
2. **The state file has no lock between the watch and a running backup.** Read in the code, not reproduced, not fixed. The watch writes only on `--mark-raised`, `--mark-armed` and once when nothing is on record.
3. **The orphan engine after SIGKILL** (finding 8, above).
4. **Content.** Every secret and client rule is by NAME. A secret or another client's material inside an ordinary-named file travels.
5. **Tuesday and Friday** have nothing runnable. Their scopes are theirs to state and Wednesday's to add.

## My own slips, this task

- Round 1 called a file arrived by size alone and indexed it. That is finding 1, and it is mine.
- Round 1's secret list was exact names, case-sensitive, on a case-sensitive drive.
- Round 1's launcher proposal named `$PREFLIGHT_LOG`, a placeholder I never checked against the launcher. The PORTABILITY proposal said 31 from a partial read that ended at section 30.
- Round 1's suite asserted the flawed flag behaviour (card printed into the nightly log) as correct.
- Round 2, caught before this file: my first T18 killed the launching shell, not the tool, so it tested nothing (it failed, which is how I saw it); three expectations in T13 and T15 were miscounted by me; the first round 2 mutant pass reported 61 of 63 because two mutants were caught by a different test than the one I had named; and those runs showed the card's failure reason was cut at 220 characters, which hid it under a long path (now 400).
- ANSWER-1: the first step's exit code did not print (a shell variable empty in zsh). Stated in that result file.

## What is NOT tested in round 2

- **Any write to the real NAS.** Renames into `versions/`, the temp folder, long paths, names SMB dislikes, whether the share keeps times. The first real run is the first test of all of it, and of the sha256 read-back at scale.
- **launchd.** No job loaded, no `launchctl` verb. The 24-fires-a-day template was linted, not run. Expect a macOS privacy prompt for `python3` as well as `rsync`.
- **The doctor block inside the real `doctor.sh`**, and the launcher carrying its line into a real boot prompt. The block was run with doctor's three helpers copied; the launcher path was read.
- **The installer with the two proposed lines.**
- **Scale.** A million-file real run: the proof pass, the index, memory, the whole-run watchdog, the cap.
- **A real, naturally occurring exit 23**, a reboot or sleep mid-run, and finding 8 beyond one scripted kill.
- **A constantly-written file on the real tree** (it would fail the night; see finding 1).
- **Real case collisions on disk** (T11 supplies the listing; the scratch volume folds case).
- **`late_fire=run`** beyond its decision. **Python 3.9** beyond T10 (one real run under `/usr/bin/python3`).
- **The 32-hour estimate.**

## QUESTIONS (not blocking this round)

1. **The `✗` gate** (finding 6): keep the hard failure that stops a human launch until the card is raised, or drop to a warning that no prompt carries?
2. **Secuura material inside the seat's own tree** (briefs, gate clones): leave it with the tree under General, as built, or split it out to the Secuura folder?
3. **The token counts above** (4,558 paths with `nexusai`, 2,670 with `hpsm` in folders this seat owns): Wednesday said Kam may narrow her reading. One `exclude_path` line per folder would do it.
4. Round 1's questions 2, 3, 6 and 7 (`reference/`, the narrowing, the 32-hour first copy, `.git`) stand as asked below.

## For the checker: where to look first

- `nb_core.py`: `secret_shape`, `SEATS`, `Ctx.load_conf`, `plan_set`, `prove_arrival`, the pass loop in `cmd_backup`, `cmd_watch`.
- Re-run: `bash tests/run.sh /private/tmp/<dir>` (about a minute and a half), `bash tests/mutants.sh /private/tmp/<dir>` (about 15 minutes, five at a time), `bash nas_backup.sh --dry` (seven minutes, reads only), `python3 tests/scan_dry_lists.py logs/wednesday <stamp of that dry run>`.
- Not armed: `evidence/round2/real_lane_checks.txt` (0 `nasbackup` rows in `launchctl list` and 0 templates in `scheduler/jobs`, each beside a control of 1 for `naspush`; three HOLD files; `--run` exits 3).

---

# ROUND 1 (kept as written; superseded above where round 2 says so)

READY FOR QA

Build seat "nas-backup" (WED-170), Fable 5.2. Nothing is armed, nothing was installed, nothing was written to the NAS, no existing file was edited. Full detail: `CENSUS.md` (facts with their instrument), `README.md` (design and the reason for each choice), `evidence/` (test, mutant, scan and dry-run output).

## Two things the coordinator should read before anything else

1. **Secrets are on the NAS already, put there by the job that is armed today.** `/Volumes/Backup/DevMASTER-mirror/!CODING/Secuura/Blockchain/4_Credentials` (23 entries) and `.../3_Access_Keys` (6 entries) exist on the Backup share. `scheduler/nas_push.sh` excludes neither name. I read existence and entry counts only, opened nothing, and touched nothing. This is workspace hard rule 3, and what happens next is Kam's.
2. **That same job (`com.wednesday.naspush`, 03:30) has not completed a run on this Mac.** STALLED on 11-12 and 11-13, then stopped by its 4-hour cap on all 13 nights from 11-14 to 11-26. It re-sends the same 128,000 files every night because the share does not keep the file times rsync sets. The mirror's `WEDNESDAY` folder is empty.

## Census headline

- **Exists:** `tools/nas_offload.sh` (by hand, dated offloads to DEV-Working); `scheduler/nas_sync.sh` (two-way unison, can delete); `scheduler/nas_push.sh` (one-way rsync, whole drive to the Backup share); `nas_staleness.sh`, `nas_sync_lib.sh`; doctor's NAS checks.
- **Held, and by whose word:** `nassync`, both seats. `NASSYNC_HOLD_wednesday`: "Re-arm ONLY on Kam's word" (2026-10-04, card `wed-nassync-rearm-shape-1004`). `NASSYNC_HOLD_tuesday`: "Lift: Kam's word only" (2026-10-16); `com.tuesday.nassync => disabled` on this Mac. PORTABILITY 20: "The NAS leg stays OFF until the case is fixed (Kam's card `nas-case-fold-datasec`)." This build does not re-arm it and does not use its engine.
- **Armed:** `naspush`, on Kam's cards `wed-nassync-rearm-shape-1004` = a and `wed-nightly-nas-mirror-old-nas-1111` = a. See the two points above.
- **The NAS:** `/Volumes/DEV-Working` is smbfs, 10.79 TiB free, top-level names `#recycle .DS_Store Datasec Friday General Personal Projects Secuura`. It is NOT case-sensitive (found without writing: `pathconf` and a read-only stat of the case-flipped names). The drive IS case-sensitive.
- **Recommendation: build beside, not extend.** New share, new folders, new label, own lock, state and hold. After its first good run, one card for Kam: hold `naspush`, and decide about the mirror and the secrets on it.
- **Scope:** as first written the backup was 8.9 million files (6,425,033 in the seat tree outside `reference/`, 2,464,442 in the Secuura folder). Narrowed in `seats/wednesday.conf` to **1,012,113 files, 67.83 GiB**. Every exclusion is listed with its measured size in the conf and in CENSUS section D.

## What I built (bytes)

| File | Size | What |
|---|---|---|
| `nas_backup.sh` | 2,695 | The backup. Dry run by default; `--run` for real. Seat via `fleet/cockpit/seat_resolve.sh`, plus two stricter checks |
| `nas_backup_nightly.sh` | 1,879 | What the scheduler calls: catch-up, skip-if-running, never outside the window |
| `nas_backup_watch.sh` | 2,263 | The three-day check; prints the one card command, never runs it |
| `nb_core.py` | 87,320 | The engine (Python 3.9+, standard library only) |
| `nb_common.sh` | 2,646 | Seat and python lookup, sourced by the three scripts |
| `seats/wednesday.conf` | 6,441 | Confirmed: 14 sets, schedule, exclusions |
| `seats/tuesday.conf`, `seats/friday.conf` | 1,111 / 986 | Placeholders, `status=unconfirmed`: the tool refuses them |
| `jobs/nasbackup.plist.template` | 2,689 | launchd template, four fire times per seat. Deliberately NOT in `scheduler/jobs/` |
| `HOLD_wednesday`, `HOLD_tuesday`, `HOLD_friday` | 474 / 468 / 465 | While present, `--run` exits 3 |
| `proposed/install_all_jobs.proposed.md` | 4,367 | Lines, each with a rollback |
| `proposed/doctor.proposed.md` | 3,527 | |
| `proposed/PORTABILITY.proposed.md` | 3,223 | |
| `proposed/launcher.proposed.md` | 2,116 | |
| `proposed/INSTRUCTIONS-for-other-seats.md` | 6,237 | Steps for Tuesday and Friday, what must be true first, how to prove the first run |
| `tests/run.sh` | 32,962 | 167 checks on a fake NAS |
| `tests/mutants.sh` | 7,017 | 20 deliberate breakages the suite must catch |
| `CENSUS.md`, `README.md` | 20,316 / 8,261 | |
| `.gitignore` | 143 | `state/ logs/ manifests/ __pycache__/` |
| `evidence/` | 124 KB | Outputs named below |

Engine in one sentence: the tool lists both sides itself, decides what changed (absent, size differs, or the source's own stat changed AND the sha256 differs), and hands rsync 3 an explicit list with `--backup --backup-dir=versions/<stamp>`, so a changed file's previous copy is kept and nothing is removed. It does not rely on file times on the NAS, because this NAS does not keep them.

Destination: `/Volumes/DEV-Working/<Client>/<Seat>/nightly-backup/{current,versions,manifests,runs}`. Wednesday: `Secuura/Wednesday/` and `General/Wednesday/`. The client list per seat is hard-coded; a conf cannot add to it.

## Tests

`bash tests/run.sh <dir under /private/tmp>`: fake NAS and fake source in the session scratchpad, never the real NAS (test mode is refused for any path outside `/private/tmp`).

```
T10 the oldest python on the target machines (/usr/bin/python3)
  PASS  T10 a real run under Python 3.9.6: exit 0 (= 0)
  PASS  T10 GOOD

T11 names that differ only in case: neither is copied, both are named (the scratch volume cannot hold such a pair, so the listing is supplied)
  PASS  T11 the planner ran (= 0)
  PASS  T11 only the non-colliding file is planned for copy
  PASS  T11 a folder pair that collides is not created; the clean folder is
  PASS  T11 four files under four colliding names are counted as not backed up, and it is not a failure

=== 167 passed, 0 failed
```
Full output: `evidence/tests_run_final.txt`. `grep -c '  PASS  '` is 167 and `grep -c '  FAIL  '` is 0 on it.

Covered: dry is the default and writes nothing (T1); a real run copies and counts both sides (T2); a changed file keeps its previous version, including a same-size change; a file removed at the source stays at the destination; a lost index re-copies nothing (T3); secrets, `.git`, `node_modules`, quarantine, `pgdata-*` and another seat's folder do not arrive while the ordinary file beside them does (T4); every refusal with its must-succeed neighbour: NAS not mounted, a local folder at the NAS path, client folder absent, top-level and seat-level names differing in case, free space, live lock, stale lock (reported, left, then moved by `--clear-stale-lock`), source not the seat's drive, another client's folder as destination and as source, seat disagreement, unknown tree, outside the window, hold file, unconfirmed conf, deletion-capable flags, a set over the file ceiling, an unlisted project folder (T5); a planted `*deleting` line fails the run at exit 9 although the engine exited 0; stall and cap (T6); catch-up with the clock supplied: first night, second fire the same night, missed one night, outside the window, a run in progress (T7); missed three nights: the card command appears exactly once per gap, and once again for a new gap (T8); the watch flags a job that was armed and never fired once, works with the NAS away, and stays quiet while held (T9).

**Each test shown able to fail.** `bash tests/mutants.sh`: copies the lane to scratch, breaks one property in the copy, runs the suite on it.
```
  CONTROL   the unmutated copy: exit 0 — === 167 passed, 0 failed
=== 20 mutants caught, 0 survived or broken
```
The first pass caught 18 of 20 (`evidence/mutants_first_pass_2_survivors.txt`). Both survivors were mutants that removed one of two guards: rsync 3 treats `--backup-dir` as implying `--backup`, and the allow-list is checked twice. The script now removes both guards for those two. Inside the suite, the additive and secret checks are also re-run against sabotaged engines ("CAN-FAIL" lines).

## The one real dry run (reads only), 12:59:26 to 13:06:28

`bash nas_backup.sh --dry`, exit 0. Output: `evidence/real_dry_run_2026-11-27.out`.

| | Files | Bytes |
|---|---|---|
| WEDNESDAY tree to `General/Wednesday` | 265,195 | 26.67 GiB |
| Secuura folder to `Secuura/Wednesday` | 587,085 | 30.95 GiB |
| Testing Agent MAIN | 151,723 | 9.38 GiB |
| Eleven smaller general projects | 8,110 | 0.82 GiB |
| **Would copy (everything is new: the destination does not exist)** | **1,012,113** | **67.83 GiB** |

Also in it: 982 symlinks recorded, not copied; 7,085 entries excluded; 14 files left out because 14 names differ only in case from a sibling; the engine's dry list agreed with the plan for all 14 sets; 0 deleting lines; no PROBLEM line.

NAS unchanged: top-level and own-client folder names, their mtimes, and `df` used blocks (117175864) are identical before and after (`evidence/nas_before_and_after_dry_run.txt`).

**Estimated duration.** I could not measure write speed read-only. The nearest measurement is the armed leg's own logs to the same NAS box: 8.9 files a second, three nights running. At that rate the first copy takes **about 32 hours**. That is an extrapolation from another job on another share, and that job also renames a previous copy for every file, which a first copy does not, so it may be up to twice as fast. After the first copy, a night's run lists about a million destination files at the 390 entries a second I measured (**about 43 minutes**) and copies only what changed.

## Proposed times, and collisions

| Seat | Fires | Window |
|---|---|---|
| Wednesday | 00:30, 01:40, 02:50, 04:00 | 00:30 to 05:30 |
| Tuesday | 02:30, 03:20, 04:10, 05:00 | 02:30 to 05:30 |
| Friday | 04:30, 05:40, 06:50, 08:10 | 04:30 to 09:30 |

No same-minute collision with any job found (01:15, 03:30, 05:30, 06:00, 06:45, 15:00, 23:00, 23:30, Monday 08:00). The known 23:00 collision on Tuesday's seat is untouched. Two overlaps on this Mac that are not collisions: `stalescreen` at 01:15 (model box, not the NAS), and `naspush` from 03:30 to 07:30 (same disk, same NAS box, different share). Later fires are not hourly at minute 30 because Wednesday's would land on 03:30 and Tuesday's on 05:30.

## Deviations, each with its reason

1. **The engine decides what changed; rsync only carries an explicit list.** The brief's example (`rsync --backup --backup-dir`) is kept, but plain rsync decides by size and time, and this NAS loses the time. On it that design re-copies and re-versions every file every night.
2. **One fixed `nightly-backup/` folder with dated `versions/` inside**, not a dated folder per night as the 2026-11-11 convention reads. A dated folder per night would add 68 GiB a night.
3. **More was excluded than the brief lists**: nine paths of caches, model weights and work clones in the seat tree, and eleven folder names plus one path inside the Secuura set. Without them the job is 8.9 million files. Precedent: Kam's `narrow-hard` ruling of 2026-09-11. All listed for him below.
4. **Four fire times in the template, not one.** One fire a night cannot serve "the NAS was away at 00:30".
5. **Three shell scripts over one Python engine** rather than three standalone shell scripts: the target Macs ship bash 3.2, and the counting, JSON state and clock logic are testable in Python and not in that shell.
6. **Names differing only in case are left out and reported, not refused.** A refusal would block the whole Secuura set.
7. **Symlinks are recorded in the manifest, not created on the NAS.**
8. **The watch says HELD and raises no card while `HOLD_<seat>` exists.** Otherwise a held, never-armed seat would raise a card after three days.
9. **I ran `nas_backup.sh --run` once in the real lane, to prove the hold.** It refused at exit 3 before touching the NAS. It left one `refused` record in `state/wednesday.json`.
10. **Friday's allow-list is `General` only**, a placeholder (question 5).
11. **`max_files` raised to 700,000 for this seat** (default 400,000): the Secuura set is 587,085 files, most of it session evidence.

## What I did NOT test

- **Any write to the real NAS.** So: whether DEV-Working accepts the engine's temp-folder rename and the move into `versions/`; whether it keeps file times; long paths and names SMB dislikes; Unicode names as the share returns them. The first real run is the first test of all of these.
- **Anything under launchd.** The job was never loaded. Expect a macOS privacy prompt for `python3` as well as `rsync` on the first scheduled run (PORTABILITY 15a is the rsync one).
- **The whole-run watchdog** (cap plus 15 minutes). The engine stall and cap were tested with stub engines only.
- **A signal or a reboot in the middle of a run.** The stale-lock path was tested with a dead process id, not a real interruption.
- **Scale beyond the dry run.** The whole dry run over a million files took 421 s. The real run's step of checking each sent file at the destination (a million stats over SMB), the index at a million rows, and memory use were not exercised.
- **A real case collision on disk.** The scratch volume folds case, so T11 supplies the listing.
- **The proposed lines** for doctor, the launcher and the installer: written, not run.
- **Tuesday's and Friday's configurations**: placeholders. Nothing was run for those seats.
- **`late_fire=run`**: its decision only, not a run. **Daylight-saving changeover** in the window arithmetic: not tested.
- **The 32-hour estimate**: an extrapolation, not a measurement.
- **Content isolation.** Exclusion is by NAME. A file in the Wednesday tree that mentions Datasec and is not named for it (a brief, a chat log, a ticket export) travels to `General/Wednesday/`.
- `0_Brain/reference` was not re-measured (279 GB and 5.9 million files is Wednesday's figure).

Housekeeping: the dry run left 240 MB in `logs/wednesday/` (the million-line file lists). A night's real run logs only what changed. Nothing in this lane prunes logs.

## QUESTIONS

The round is not blocked. These are for the coordinator and Kam before arming; where the brief contradicted itself I took the stricter reading.

1. **The brief contradicts itself on a late fire.** It says "a fire after a sleep still runs" and also "It never runs outside its window on its own". Stricter reading taken: a fire outside the window is logged and skipped, and the missed night is caught up when the next window opens. A fire after a sleep that lands inside the window does run (the windows are 3 to 5 hours and launchd fires once on wake). The other reading is one line: `late_fire=run` in the seat's conf.
2. **`0_Brain/reference`: in or out?** Out for now, as the brief asked. 279 GB and 5.9 million files. In would make the file count about seven times what it is now.
3. **Is the narrowing right?** Out: `local-model/spark/cache` (237.66 GiB), `local-model/spark-ab/work` (141.98 GiB), `tools/omlx/models` (198.18 GiB), `local-model/runs` (20.18 GiB), smaller caches; in Secuura, folders named `wt`, `quarantine*`, `*node_modules*`, `clone`, `deploy-clones`, the per-seat temp folders, `Blockchain/scratchpad`. Kept in: Secuura's session evidence (most of its 587,085 files), `fleet/qa-agent/gatesets` (193,238 files), `Testing Agent MAIN` (151,723 files). Each can be flipped by one line.
4. **The armed `naspush` job and the secrets on the Backup share** (top of this file). Not mine to act on. Suggested: one card to Kam now for the secrets, and after the new job's first good run, hold `naspush`.
5. **Friday.** Two rulings are missing: which client folder or folders Friday writes to (it works both clients), and whether the laptop may carry a scheduled job at all (Kam's 2026-09-23 ruling says none; his 2026-11-27 instruction says each agent).
6. **The first copy is about 32 hours, far outside a night.** It needs Kam's approval as an out-of-sequence run with a raised cap (`--run --out-of-sequence <card id> --max-seconds <n>`), or the scope cut further. Run night by night under the 5-hour cap instead, it would report "stopped by the cap" for several nights and raise the three-day flag.
7. **`.git` is excluded, so commits not yet pushed are not in the backup.** Accept that, or add a per-repository `git bundle` step in a later round?

## For the checker: where to look first

- The safety claims: header of `nb_core.py`; `SEATS`, `EXCLUDES`, `FORBIDDEN_RSYNC` near its top; `preflight()`, `plan_set()`, `cmd_backup()`.
- Re-run: `bash tests/run.sh /private/tmp/<dir>` then `bash tests/mutants.sh /private/tmp/<dir>`; then `bash nas_backup.sh --dry` (seven minutes, reads only).
- Not armed: `ls HOLD_*`; `launchctl list | grep -i -c nasbackup` is 0 (positive control: `naspush` counts 1); `ls scheduler/jobs | grep -i -c nasbackup` should be 0.

---
Last updated by the build seat: 2026-11-27 13:20:34 AEDT. Stopped at READY FOR QA.

---
ROUND 2 written by the build seat: 2026-11-27 15:03:18 AEDT. Stopped at READY FOR QA.
