VERDICT: NO GO

Round 3 does fix what the first checker planted: its own attack tree now reads 0 unexpected of 69 for me, the suite is 483 passed and 0 failed under both Pythons, and the seat's 24 mutants are all caught. But the two Blocker classes are closed only for the shapes that were named, not as classes. With NEW shapes of the same kind, another seat's lesson and another client's marked section still enter the index with exit code 0 and no line naming them (findings N1, N2), and a `rebuild` addressed to one cluster still wrote into another and reported success about the first (N3). One adopted must-fix (item 1(i), "a line that looks like a tier line but no tier was parsed: EXCLUDE") is not actually built: the branch that should do it can never run (N4). All of it is latent, as before: the real Wednesday index is clean for every one of these classes today (counted, below). The fixes are small. With N1 to N4 fixed and `scripts/f1_new.py` and `scripts/seat_f2.sh` (section F2c) re-run clean, my verdict would be GO WITH NOTES.

Independent re-check of the brain-db lane, round 3. Run 2026-11-27 13:46 to 14:11 AEDT (both from `date`). I did not build this and I did not write the first verdict. Every number below is from a command I ran this session; the file holding the raw output is named beside it. All paths are under `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_qa-braindb-r3/scripts/` unless given in full.

---

## The first verdict's findings, re-run against round 3

| # | Finding (first checker) | Now | My evidence |
|---|---|---|---|
| F1 | Lesson deciders fail open | **PARTLY. Still a Blocker class.** The checker's 69 expectations: 0 unexpected (control `xneighbour01` found 9 times). My 58 new must-be-absent shapes: **28 enter the index**; 2 of 20 whole-index variants leak. See N1, N2, N4. | `out_chk_attack_tree.txt`, `out_f1_new.txt`, `out_f1_unit_and_search.txt` |
| F2 | Server known only by socket directory | **PARTLY.** The checker's P6 is fixed: `rebuild`, `check`, `search`, `at` each exit 4 and the other index stays at 59 files. But the identity test and the write are separate connections with a lock wait between them: I swapped the server in that gap and the rebuild wrote into the cluster it was not addressed to, rc 0. See N3. | `out_chk_proc.txt` (P6), `out_seat_f2.txt` (F2c) |
| F3 | Hard link indexed | **FIXED** for a hard link that sits still (`zatk02hard` absent; named "hard link (link count 2)"). A file flipped between regular and symlink while rebuilds run still gets through (N6). | `out_chk_attack_tree.txt`, `out_f3_f5_f7.txt` |
| F4 | No scope file, cluster still created | **PARTLY.** A MISSING scope file now creates nothing (no directory, no lock file, no server). A scope file that EXISTS but is refused (wrong `seat`, a hard-denied line, a typo) still creates the cluster and leaves a server running: 3 of 3. See N7. | `out_chk_sim_tuesday.txt`, `out_seat_f2_part2.txt` |
| F5 | Two commands at once | **FIXED.** Two starts rc 0 and 0; two searches on a stopped cluster rc 0 and 0; no cluster at all, 4 trials: both rc 0 and `PG_VERSION` present every time. My own 12 trials of four commands at once (48 commands, three starting states): 0 lost. | `out_chk_proc.txt` (P1, P2, P2b), `out_f3_f5_f7.txt` (F5c) |
| F6 | Stale pid file of a live foreign process | **FIXED.** `STALE PID FILE` line plus the exact `mv -n` line; file not moved; sleeper alive after `stop`, `start`, `search`, `up`. | `out_chk_proc.txt` (P4, P5) |
| F7 | One bad file aborts the rebuild | **FIXED.** Mode-000 lesson: rc 0, no traceback, listed; 300,000-word section and a 30 MB bullet: rc 0, truncated and listed; last line `DONE WITH FAULTS`. My extra odd files (0 bytes, invalid UTF-8, NUL, a directory, a FIFO, 20,000 headings, a 330,000-character title): rc 0, 0 tracebacks. | `out_chk_crash.txt`, `out_f3_f5_f7.txt` (F7) |
| F8 | Row with 0x1E / 0x1F silently lost | **FIXED.** `search zatkctl1` finds its row (1 result). | `out_f1_unit_and_search.txt` |
| F9 | Safety test that could not fail | **FIXED.** Under the seat's `F9_stop_trusts_pidfile` mutant the assertion `the foreign process was killed by stop` fails (3 lines on it, 29 red in all). | `mutants_seat24.log` |
| F10 | WEAK MATCH misleads | **FIXED as ANSWER-3 allowed** (removed; 0 occurrences of `WEAK` in the code or in my 17 search outputs). The neutral last line was true in 16 of 16 statements by an independent test. One new search defect: N9. | `out_search_truth.txt`, `out_search_limit.txt` |
| F11 | Seat-word guard depends on the declared kind | **FIXED for the routes named.** The checker's 40 hostile scopes: nothing sensitive in the index in any (rows 22 to 29 included). What stays open is the case the seat itself admits: N5. | `out_chk_scopes.txt`, `out_seat_f2_part2.txt` (S6) |
| Note | Seat follows `WED_AGENT` | **FIXED.** 13 folder names, 3 symlink forms, 2 nestings, 6 `WED_AGENT` values: every mismatch refused; the real folder's name wins over a symlink's. | `out_seat_f2.txt` (S1 to S5) |
| Note | `devnas.prf` line 53; probe cluster covered | Line number correct (first `ignore` is line 53). Coverage achieved, but by a pattern that is too wide: N12. | `out_proposals.txt` (D1) |
| Note | `PORTABILITY.md` item number | Correct: last item is 31; the proposal says NN and names the sibling lane. | `out_proposals.txt` (D1) |
| Note | Fixed test socket directory | Fixed: `/tmp/wed-bdb-t<pid>`; four suites ran side by side in the mutant harness without colliding. | `mutants_seat24.log` |

---

## NEW FINDINGS

### N1. BLOCKER. A rules-index row that does not EQUAL a lesson's file name is treated as "no row", so a lesson scoped only to another seat enters, silently
- **Reproduce:** `python3 scripts/f1_new.py <work> <tool> <sock>`; output `out_f1_new.txt` (cases 70 to 83 and the whole-index block).
- **Expected:** absent, or at least named. **Actual:** each of these `tier: W` lessons whose ONLY row says `tuesday` is in the index, rc 0, last line `rebuild: done`, and the report names none of them ("NOT NAMED ANYWHERE"):
  - key written without `.md` (case 72); one letter wrong (80); in double quotes, as a spreadsheet export writes it (73); as a wikilink (83)
  - a zero-width space after the key (74); a stray BOM at the start of the row (82)
  - file name stored NFD, key written NFC (71; on my scratch volume, see NOT TESTED)
  - **the row's TABs turned into spaces by an editor (75, and whole-index variant `one-good-rest-spaces`).** Here the report says `1 DAMAGED row(s) ignored ... a lesson named by one is excluded and listed below`, and nothing is listed: the lesson is in. ANSWER-3 item 1(iii) says "a lesson whose name APPEARS IN the first field of any rejected row ... is excluded"; the code tests equality after normalising, and the first field of a tab-less row is the whole line.
  - Control: the same lesson with a well-formed `tuesday` row is absent (case 70, named under "every rules-index row for it names only other seats"). `search qzcase75tok` and `search qzcase72tok` return those lessons as result 1 (`out_f1_unit_and_search.txt`).
- **Why this is the first checker's F1 and not a new idea:** its trailing-space, case and path keys were all "key does not match the file". Round 3 normalised those three spellings; the class is open.
- **Real tree today (counts, `out_realcopy.txt`):** 379 well-formed rows, 0 rejected; 0 keys that match no lesson file; 28 keys scoped to other seats only, all matching a file; 0 lesson names that are not ASCII. **Exactly 0 indexed lessons rely on "no row, tier alone"** (the one row-less file is a `(conflict_on_` copy, excluded by path).
- **Smallest fix:** (a) for a rejected row, exclude every lesson whose normalised name occurs ANYWHERE in the raw line; (b) NFC-normalise and strip format characters (category Cf) on both sides of the key comparison; (c) print by name every row, good or rejected, that matches no lesson file, and every indexed lesson that has no row; (d) since no real indexed lesson has no row today, "a lesson with no row is excluded and named" costs nothing and closes the class. (d) changes ANSWER-1 ruling 2, so it is Wednesday's to rule.

### N2. BLOCKER. Another client's marked section inside an indexed MIXED lesson survives in four new shapes, silently
- **Reproduce:** same run, cases 50 to 62. Control: the plain marker's section is absent (case 50).
- **Actual (token of the Datasec-marked section present, rc 0, nothing printed):**
  - the section holds a 4-backtick code fence with a 3-backtick fence inside it and a `# comment` line (51);
  - the section holds a ``` block containing a line `~~~` and then a `# shell comment` (52). Cause of both: `FENCE_RE` toggles on any fence line whatever its character or length, so a `#` line inside a code sample is read as a level-1 heading and ends the dropped span;
  - the marker written as a three-line HTML comment (53); the marker written as a list item `- <!-- tier: ... -->` (60).
- **Real tree today (`out_real_audit.txt`):** 5 indexed lessons carry a marker; 0 marker-like lines the tool's regex misses; 0 denied sections holding mixed fence kinds.
- **Smallest fix:** remember the opening fence's character and length and close only on the same character at the same or greater length; treat any line holding `<!--` and `tier` (and a `<!--` line followed by a `tier` line) as a marker; when a denied marker is seen and the span's end is in doubt (unbalanced fences inside it), drop to the end of the file and say so. Add the dropped sections' headings to the report by name.

### N3. BLOCKER by the severity rule given to me (a command acts on the wrong cluster with a clean exit code); narrow in practice. `rebuild` checks which cluster answers, then waits, then writes on a new connection
- **Reproduce:** `scripts/seat_f2.sh`, section F2c; output `out_seat_f2.txt`. c1 running on a socket directory; a holder takes c1's lock (stands for another rebuild in progress); `rebuild` addressed to c1 passes `need_server()` and waits for the lock; c1's server stops and c2's starts on the same socket; the holder lets go.
- **Expected:** refusal (rc 4). **Actual:** `the rebuild ADDRESSED TO c1 finished: rc=0`, it printed `data directory: f2/t1` and `rebuild: done`, and **c2, never addressed, now holds a `braindb` database with 3 files from the other tree**. c2's own `check` then reads RED.
- **Why it is reachable:** the socket directory is per user and seat (`/tmp/wed-braindb-<uid>-<seat>`), so two trees of one seat on one Mac (DevMASTER and its T9 sync copy) share it, and each has its own lock file, so the lock does not serialise them. The gap is the parse time (about 1 s on the real tree) plus any lock wait, which has no limit (N13). `check`, `search` and `at` have the same gap, read-only.
- **Not demonstrated:** the swap without my lock holder, and on two real trees.
- **Smallest fix:** assert the data directory inside the SAME psql session as the work: first statement of the rebuild transaction (and of each read query) compares `current_setting('data_directory')` with the addressed directory and raises. Then no window exists.

### N4. MAJOR. ANSWER-3 item 1(i) is not built as written: a tier-looking line inside the frontmatter block that does not parse as `tier` does NOT exclude the lesson
- **Reproduce:** `out_f1_unit_and_search.txt` (unit call of `parse_frontmatter`) and `out_f1_new.txt` cases 13, 14, 21.
- **Actual:** `- tier: P-Datasec/X`, `  - tier: ...`, `* tier: ...`, `> tier: ...`, `[tier: ...]` and a zero-width space before `tier:` all match the tool's own `TIERISH` regex, yield no tier and no fault: 6 of 6 are INDEXED as untagged (control: plain `tier: P-Datasec/X` is excluded). The cause is one line: `elif TIERISH.match(line)` sits under `if ":" in line`, and `TIERISH` requires a `:`, so the branch can never run. The seat's fixtures cover a stray tier line AFTER the block and never one inside it, so the suite and all 24 mutants pass.
- **The same hole, wider (13 more shapes that enter):** CR-only line endings with tier not the first key (11); a Cyrillic look-alike in the key (19); a full-width colon (20); a soft hyphen in the key (22); `tier (project):` (35); `tier = value` (36); TOML `+++` frontmatter (37); a fence written `--- # frontmatter` with tier after 62 keys (27) or after a YAML `# comment` line, which the stray-line scan reads as a heading and stops at (28); a second block closing 72 lines on (29); U+2028, form feed or byte 0x1E between `date:` and `tier:` (32, 33, 34; the tool itself strips 0x1E and so glues the two keys together).
- **Why Major and not Blocker:** every one of the 16 IS named in the rebuild report, under `UNTAGGED lessons indexed (... treated as W ...)`, and by the first checker's reading `boot_digest.py` reads them the same way at boot. So there is a line; it is a weak one (the real report already lists 3 untagged lessons as routine), and the report is not shown in normal use (N8).
- **Correctly refused in the same run (18 shapes):** CRLF; BOM + blank lines + CRLF; UTF-16 LE and BE; Latin-1; both YAML block scalars; block list and flow list values; tabs; a no-break space after the fence; an indented fence; an HTML comment before the fence; a second block within 47 lines; tier twice in two spellings; single-quoted key; a Cyrillic letter in the client name; CR-only with tier first.
- **Smallest fix:** test `TIERISH` BEFORE the colon split and count it; fold the key harder before comparing (NFKC, drop category Cf and non-alphanumerics, casefold) and fault any key that starts with `tier` and is not exactly `tier`; split lines with `str.splitlines()` after turning lone CR into LF; stop the stray-line scan only at a heading that follows a blank line or is outside any `---` pair; lift each case of `f1_new.py` into the fixtures.

### N5. MAJOR (Blocker by the letter of the rule; rated lower because it needs a wrong line in a scope file). A TUESDAY tree indexes the Wednesday seat's ledger, daily notes and pickup file with one allow line each, rc 0, nothing printed
- **Reproduce:** `scripts/seat_f2_part2.sh` section S6; output `out_seat_f2_part2.txt`. Control T0 (proposed scope unchanged): none of Wednesday's tokens; Tuesday's own ledger token present 8 times.
- **Actual:** `allow ledger 0_Brain/learnings/_ledger.md` puts Wednesday's ledger in (10 hits); `_ledger*.md` adds its archive (4 more); `allow daily 0_Brain/daily/20*.md` puts Wednesday's daily notes in (10); `allow skill 0_Brain/tasks/*.md` puts `NEXT-PICKUP.md` in (2). Friday's records were refused by the seat word in every probe (T5, T6), and `allow lesson 0_Brain/daily/20*.md` was refused (T7).
- **Is "the instructions say so" enough? No, for daily notes and pickup files; a ruling is needed for the ledger.** The brief's bar is "structurally unable to enter". For daily notes the structure already exists: `braindb.sh` sources `tools/seat_note.sh`, which sets `SEAT_NOTE_REL` to the seat's own daily folder (`0_Brain/daily`, `daily_tuesday`, `daily_friday`); the tool has that value in hand and ignores it. Refusing an `allow daily` line whose folder is not `SEAT_NOTE_REL` is a few lines and makes step 1 of the instructions safe to follow carelessly. For the ledger, `tools/rules_card.py` line 101 calls `_ledger.md` and its archive "the SHARED files (they also hold other seats' rows)", so whether a Tuesday index may hold it is Wednesday's or Kam's to rule; whichever way, it belongs in code (a seat-to-own-ledger table like the one `rules_card.py` carries), not in a sentence.

### N6. MAJOR (same note on the rule). A file swapped between a regular file and a symlink to a `4_Credentials` file while rebuilds run: the secret text entered the index in 10 of 40 rebuilds
- **Reproduce:** `scripts/f3_f5_f7.sh` section F3c; `out_f3_f5_f7.txt`. Control: the regular text was indexed in 5 rebuilds, so the instrument sees both states; a symlink that sits still, a chain of three, and a symlink to `/dev/zero` were all skipped.
- **Cause:** `enumerate_files` tests `lstat` and `islink`, then `scan` opens the same path later by name. Each rebuild still ended `rebuild: done`.
- **Rated below Blocker because** it needs a process already able to write in `learnings/` and read the secret, flipping at the right moment; that process could paste the text instead. **Smallest fix:** open with `os.O_NOFOLLOW`, then `fstat` the descriptor (regular file, link count 1) and read from it.

### N7. MINOR. F4 is half fixed: a scope file that exists but is refused still leaves a cluster and a running server
`out_seat_f2_part2.txt`, first block: `seat tuesday`, `allow skill 4_Credentials/*.md` and a mistyped directive each give rc 2, **cluster directory created: YES, server left running: 1**, 3 of 3. The instructions tell a seat to "change what is wrong for your seat" and then say every refusal "creates nothing". Fix: load and validate the scope (a `braindb_index.py` dry call) before `ensure_up`.

### N8. MINOR. What fails closed is invisible in normal use
- A hard-linked OWN lesson and skill are skipped and named in the rebuild body, but the last line reads `rebuild: done; no file was unreadable and no row was truncated`, `check` is GREEN with 0 lines about them, and `search` for their words says `NO MATCH: none of these words is in the index` (`out_f3_f5_f7.txt`, F3a).
- In the proposed launcher block a lesson with a broken tier line produced `check: GREEN, 419 files` and nothing else: `up` does not even rebuild, because `check` and `rebuild` agree to leave the file out (`out_proposals.txt`, a5). The instructions' limit 6 says "the rebuild report is where you see it; nothing else tells you", and the launcher discards that report.
- Fix: `check` (and so `doctor` and the launcher line) prints the count of files kept out for safety (tier unreadable, damaged row, hard link) and of untagged lessons, with names up to a limit; the rebuild's last line counts them too.

### N9. MINOR. "A rules-file row goes first when it holds every one of the question's rarest words" is applied after the top-N cut, so result 1 depends on `--limit`
`out_search_limit.txt`: `never edit files inside other coding projects` gives the lesson first at the default limit and at `--limit 20` gives rule 0a first (which holds all four rare words and is the rule asked for). 1 of 6 questions changed; the other 5 were stable. Fix: select the rules rows that hold every key word in SQL, before the cut.

### N10. MINOR. A data directory spelled with a trailing or doubled slash: `start` launches the server, reports failure, and the tool's own `stop` then refuses it
`out_seat_f2_part2.txt`, F2a: `start` rc 1 "pg_ctl reported a start but no server of ours is running", 1 server running; `stop` with the same spelling REFUSED; only the plain spelling stops it. Through a symlink: `status` says STOPPED (rc 3) while `check` says GREEN for the same cluster; nothing wrong is acted on. Only reachable through `BRAINDB_PGDATA`. Fix: one `realpath` of `PGDATA` at the top of `braindb.sh`.

### N11. MINOR. Two exit-code and wording faults round the identity check
- `status` exits 0 while its indexer part prints `REFUSED: the server answering ... serves data directory ...` (`out_seat_f2_part2.txt`, F2b).
- When the server goes away between "is it up" and "which directory", the tool exits 4 and says another cluster "serves data directory '(unknown)'" and "is using this socket directory": 1 of 6 stop-versus-search trials (`out_f3_f5_f7.txt`, F5d trial 5). `doctor` would print "ANOTHER cluster is answering" for a server that merely stopped. Fix: an empty answer is rc 3, "not answering".

### N12. MINOR (fix before applying). The proposed sync ignore lines match by NAME anywhere under the synced roots
`ignore = Name _probe_*` already matches 6 unrelated paths in `0_Brain/reference/` within depth 6 (`_probe_copies`, `_probe_copy_head.ts`, and others; `out_proposals.txt`, D1), which would silently stop reaching the NAS. `Name pgdata-*` has no other match today but would hide any future one in any client project. Fix: `ignore = Path` lines scoped to `*/2_Project_Files/brain-db/`.

### N13. MINOR. The indexer's own lock wait has no time limit and prints nothing
A `rebuild` behind a live holder waited 20 s with 0 bytes of output and would have waited on (`out_f3_f5_f7.txt`, F5a); the wrapper round init/start/stop gives up at 150 s. The launcher block would stall a boot behind a stuck holder. Fix: the same deadline and message as `braindb_lock.py`.

### N14. MINOR. Evidence: 18 of my 30 new mutants survive the suite, and one test passes for the wrong reason
See "Suite and mutants". The test "a socket directory that is not mode 700 is refused" (run.sh line 585) puts its mode-755 directory inside the long run directory, so the call is refused by the 103-byte length check before the mode is ever read; with the mode check removed (mutant N14) the suite stays 483 of 483.

### Notes
- The rules-index header line is a comment and is never read: with `seats` and `status` swapped every lesson that has a row is excluded as "names only other seats" (2 of 2, loud but misattributed); with triggers in the seats slot and a trigger named `all`, a tuesday-only lesson entered (contrived; `out_f1_new.txt`).
- `at pane --top -5` prints `(+5 more ...)` and no rules. `NO MATCH: none of these words is in the index` is printed for a question of stop words only. A one-word question (`Kam`) puts whichever rules row scores best first.
- `INSTRUCTIONS-for-other-seats.md`: line 61 says round 3 "has run only under 3.14.10" (it passes under 3.9.6 for me and for the seat); step 4 quotes 22,263 search rows (STATUS says 22,267; my copy built 22,270); "each test fails closed; the rebuild report names every lesson kept out" is not true for N1, N2 and N4.
- The seat's mutant harness leaves the F9 mutant's test server running when it ends ("server processes left: 1" in `mutants_seat24.log`); it had exited by my next process list. The seat disclosed this.

---

## WHAT HELD (counts)

- **The checker's tree:** 69 expectations, 0 unexpected; rebuild rc 0; 0 PWNED files (control: `expect.json` found by the same `find`).
- **The four scripts the seat did not run:** `proc.sh` (P1 to P7 and P3: every command rc 0 or a correct refusal; 0 processes left), `crash.sh` (K1 to K5: 0 tracebacks; no rules index: rc 2 and neither other-seat canary in the index, control 9), `sim_tuesday.sh` (no scope: nothing created; with the proposed scope: suite 483 of 483 on the TUESDAY tree, index holds Tuesday's own 57 files), `atk_scopes.py` (40 scopes: 0 sensitive tokens in the index; control `xneighbour01` present), `atk_inject.py` (26 payloads: state `59/97/12/8/4/1` before and after; 0 PWNED files).
- **My injection payloads:** 11 hostile file names, a lone `\.` line in a body, a ledger row, a daily bullet, a rules file and the rules-index rows for them (9 joined), then 30 argument payloads and 3 environment payloads: state `15/16/9/8/4/1/0` unchanged; 0 PWNED files; the text after the lone `\.` line is in the index (1); 0 tracebacks (`out_inject_new.txt`).
- **Seat rule:** 24 name, symlink, nesting and `WED_AGENT` probes: every one resolved to the real folder's seat or was refused.
- **Locking:** 48 commands at once, 0 lost; a holder killed with SIGKILL frees the lock (start rc 0 after 4 s); `flock` is exclusive on the drive volume (three 2 s holders took 6.3 s on DevMASTER and 6.3 s on the internal volume).
- **Rules-index faults that DO fail closed:** CR-only, 0-byte, header-only, 8 columns, a symlink, a hard link, mode 000, a directory, a FIFO, all TABs lost, a capital `.TSV`: 11 of 11 refused with rc 2. CRLF, BOM, UTF-16, a NUL in the key, three disagreeing rows with one damaged: correct.
- **Search:** 16 of 16 neutral last lines true by my own count of rarest words and my own test of the first row; the first result was the one I had written down beforehand for 11 of the 12 questions that have one (the miss is N9).
- **Proposals:** both blocks apply at the anchors named and parse under bash 3.2.57; 11 harness cases (a twelfth is void, see my errors): no boot break, no hard-coded seat, a seat without a scope file gets nothing created (no directory, no lock file) on TUESDAY and FRIDAY trees; `doctor` started nothing (0 servers after). The launcher block does create the cluster and start a server with no human step on an adopted seat; that is ANSWER-1 ruling 3, not a finding.

## Suite and mutants (my runs)

- Suite, Python 3.14.10: **483 passed, 0 failed**, rc 0, 33 `(can fail)` lines. `/usr/bin/python3` 3.9.6: **483 passed, 0 failed** (`suite_default.log`, `suite_py39.log`). Note: my F1 attack ran on the same Mac during these two runs.
- The seat's harness: control 483 and 0; **24 of 24 caught on the expected assertion** (`mutants_seat24.log`).
- Mine (`my_mutate.py`, `out_my_mutants.txt`): 33 mutants. The first checker's M6, M7 and M13, re-anchored on round-3 text: 3 of 3 caught. **30 new: 12 caught, 18 survive.**
  - Survive because another guard catches the same input (4): N12, N13, N22, N25.
  - Near-equivalent under the Wednesday scope (1): N05 (denied-client substring test).
  - **Claims with no test that can fail (13):** N01 second frontmatter block alone; N06 "a ledger only by `allow ledger`"; N07 "a daily folder only by `allow daily`"; N10 `status` asks which cluster answers; N11 the rebuild lock; N14 socket directory mode; N15 socket directory symlink; N18 `check` notices a changed indexer; N24 `check` notices a changed scope file; N21 the re-test after a failed start; N26 a marker with no heading under it; N27 a credentials folder below the top level; N28 the `chat_` refusal.

## NOT TESTED

- The real drive cluster (never started, by instruction); a real TUESDAY or FRIDAY tree; another machine or drive; ejecting or syncing with the server up; unison with the proposed ignore lines; a real Postgres major-version difference.
- The proposed blocks run inside the whole real `doctor.sh` or launcher (patched scratch copies were parsed with `bash -n`; the blocks ran in a stub harness).
- N3 without my lock holder, and on the seat's default socket directory with two real trees.
- A device node as a lesson (needs root; a symlink to `/dev/zero` was tested); a FIFO swapped in mid-rebuild; file names that are not valid UTF-8 (APFS refuses them).
- The NFD/NFC file-name case on the case-sensitive drive volume (my scratch is on the internal volume).
- The 150 s give-up path of `braindb_lock.py` to its end (20 s of waiting observed).
- The first checker's mutants M1, M3, M5, M8, M9, M11 (not re-run; M4 no longer applies).
- The seat's 36-question threshold study (not re-derived). Search quality beyond my 17 questions and 6 limit probes, judged by my reading of headings.
- `PG*` variables in the caller's shell; the `/tmp` cleaner; a reboot; Friday's proposed scope beyond the suite's own section 12.

## FOUND / TESTED / HOW

- **Rules kept:** no `cd`; absolute paths; nothing removed; no git write, mail, post, network or install; no file under any real `4_Credentials` or `3_Access_Keys` opened (my fixtures used fake folders of those names in scratch). The tool was always run from a byte copy in `<scratch>/lanecopy/WEDNESDAY/` (`diff -r` against the lane: no difference outside pgdata, quarantine and pycache). Real brain files were read only through the tool's own scan with its shipped scope, into a scratch copy of the 419 files it would index.
- **Adapted copies of the first checker's scripts** (`scripts/adapted/`; originals untouched, `atk_build.py` byte-identical): its scratch path replaced by mine; the tool path replaced by my copy in a folder named WEDNESDAY; socket directory `/tmp/qa3c`; `proc.sh` P3 pointed at my copy of the real allowed files instead of the real tree; `sim_tuesday.sh` also copies `braindb_lock.py` and `tools/seat_note.sh` (round 3 needs both).
- **Proof nothing of theirs changed** (`out_final_proof.txt`): a manifest taken at 13:46 and again at 14:11 (sha256 of every lane file outside pgdata; path, size and mtime of all 1,375 entries under `pgdata-wednesday`, the lock file and the quarantine; sha256 of every file in the first checker's folder) is IDENTICAL, 2,470 lines. Real pid file: absent. Real socket directory: empty. `git status` shows only the seat's own earlier changes and my new folder.
- **Processes:** selected by executable, then each one's `-D` read: 1 postgres process on this Mac, pid 67200, data directory under another project's session scratchpad (`...-CODING-Secuura-Blockchain/.../w78/pgdev`); not mine, not touched. With a data directory under my scratch or the lane: 0. My 14 socket directories under `/tmp` were empty and are moved into scratch. I killed nothing but my own sleepers and lock holders, by the pid `$!` gave me.
- **Controls:** every absence has a presence from the same output (named in each row above). The mutant control ("none") passes 483 of 483.
- **Things of mine that went wrong, kept:**
  1. `seat_f2.sh` S6 printed rc 1 and all zeros for every probe: my S5 probe had left a server on the shared socket directory (that is finding N7). The control (Tuesday's own ledger token = 0) caught it; re-run in `seat_f2_part2.sh`.
  2. `seat_f2.sh` F2a: my trailing-slash `init` never created a cluster, so its symlink probes addressed nothing; re-run in part 2.
  3. In S6 the token `xneighbour21` is a prefix of `xneighbour21z`, so the "archive" column reads 7 in the control; the true reading is the difference (0 in T0, 4 in T2).
  4. `pgprocs.sh` first used `basename` on a name starting with `-` and printed a usage error; the count was right; fixed with `${comm##*/}`.
  5. `proposals.sh` case f emptied PATH so far that my own `awk` and `sed` vanished; that case proves nothing (the first checker covered a missing python3).
  6. The process counts inside the adapted `sim_tuesday.sh` ("processes: 1") come from a live `ps | grep` and count the grep; the final list by executable is the fact.
  7. My first shell command used a bare `======` separator and was refused by the zsh hook; nothing had run.
  8. `f3_f5_f7.sh` outran the tool's 180 s foreground limit and finished in the background; its output is whole.
- **Hooks:** one refusal (item 7); advisories about case-sensitive grep and grep into `cut` on display-only lines; no absence in this file rests on a truncated view.
