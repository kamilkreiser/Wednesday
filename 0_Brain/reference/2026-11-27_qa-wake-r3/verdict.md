VERDICT: NO GO

Second, independent check of the lane `2_Project_Files/wake/` (WED-170 step 1, round 3). Written 2026-11-27 14:20 AEDT (clock from `date`). Two findings sit in the classes the brief names as Blockers. (1) The grants filter still drops live rows that have not been written yet: 30 of 38 new hostile LIVE rows, among them rows worded in this register's own vocabulary and a RESTRICTION; round 3 cured the first checker's 15 rows by adding words, and the next set falls the same way, so the method is the fault, not the word list. (2) The new lock can report "STALE LOCK, that process is no longer running" for a lock that was released normally, and the recovery line it prints, run as told, loses an acknowledged block (deterministic reproduction only; 0 lost in 4,544 acknowledged natural writes). Both have small fixes, given below. Round 2's Blocker itself (two writers, no lock) is FIXED, the launcher change is clean for all three seats, and every number the seat reported reproduces. Nothing in the lane, the first checker's folder or the real tree was changed by me (proof at the end).

Read first: the two Blockers (N1, N2), then ORDER TO APPLY.

## PRIOR FINDINGS

| Finding (verdict 1 / ANSWER-3 item) | Now | Evidence (under `raw/`) |
|---|---|---|
| B1 two writers lose an acknowledged block (item 1) | FIXED | `lock_attacks_AB.txt`: 2, 3, 5, 10 writers, 939 acknowledged, 0 lost; negative control with the lock removed loses 1 in 40 trials; `race_stale.txt` 1,750 more, 0 lost; `starve.txt`; `checker1_race_unmodified.txt`. New faults in the lock: N2, N3 |
| M1 filter drops hostile live rows (item 2) | PARTLY | the first checker's 23 rows: 0 dropped (`checker1_wp2.txt`). My 38 new rows: 30 dropped (`grants_hostile.txt`). See N1 |
| M2 a part shrinks to a placeholder (item 3) | FIXED | `pack_attacks.txt` section 1: 55 of 55 missing / empty / unreadable / directory / dangling cases fail cleanly (rc 2, nothing written, part named, no traceback); `checker1_wp_tests.txt` section 3. Residue: N6, N7 |
| M3 fallback not loud; m2 trusts exit 0 (item 4) | FIXED | `launcher_harness.txt` section 2: 8 failure cases, each the legacy prompt whole with the notice as the first text after `ultrathink` and the reason in it |
| M4 proposals 2 and 3 (item 5) | FIXED | `proposals_check.txt` sections 1 to 3: 0 lines of the brain file removed; Kam's sentence present once before and after, its numbered item byte-identical. One wording note: N9 |
| M5 seed leaves OWED and STANDING behind (item 6) | FIXED | `seed_real.txt`: 5 of 5 and 3 of 3 standing lines carried, line numbers reported; `checker1_extra.txt` (8 of 8, 1,694 bytes) |
| m1 `--check` green on a hand edit (item 7) | PARTLY | pack: 12 tampers all RED. Sidecar: text appended to its own `generated:` line reads GREEN (`pack_attacks.txt` section 4). N5 |
| m2 exit 0 trusted without the file | FIXED | `launcher_harness.txt`: empty pack and no pack both fall back loudly |
| m3 unreadable gives a traceback | FIXED | `minors.txt` m3: 6 cases rc 4, no traceback, path named. (A new traceback elsewhere: N4) |
| m4 seams live in production | FIXED | `minors.txt` m4: 8 seam attempts on a non-temp tree all rc 2, nothing written (a symlink under the temp directory and `TMPDIR` included); must-succeed control passes. The engine called directly still takes any `--stamp` (it is documented as never called directly) |
| m5 a stack inside one block | PARTLY | `minors.txt` m5: 11 `#` forms refused; setext (`---` / `===` underline), blockquote, list-item and HTML headings accepted. Bounded by the cap. N11 |
| m6 gitignore ignores all of `out/` | FIXED in the proposal | `proposals_check.txt` section 4. But the tree's `.git/info/exclude` line 29 still ignores all of `out/`: N12 |
| m7 doctor discards stderr | FIXED | snippet: `2>/dev/null` 0 times, `2>&1` 3 times |
| m8 nine missed mutants | FIXED | `checker1_mutants_adapted.txt`: Q01, Q02, Q03, Q05, Q07, Q08, Q11, Q15, Q17 all CAUGHT. (Two others survive in adapted form: N8) |
| N5 backtick pair, proposal 9 (item 9) | FIXED | added lines hold 0 backticks; `checker1_h09.txt`: proposal 9 changes one line per seat and is separate |
| N6 census both ways (item 8) | FIXED | `census.txt`: the script's three totals equal my own sum |
| N7 scoreboard head also moves | FIXED | stated in `proposed/01_launcher_boot_prompt.md` |
| N8 proposal 6 dated with Kam's name; proposal 7 changes other seats' doctor output | FIXED | proposal 6's new text names no seat and no person; proposal 7 says so |

## NEW FINDINGS

### N1. Blocker: the grants filter proves each drop from ONE lexical signal, and live rows in this register's own wording are dropped

- Ran: `scripts/grants_hostile.py` (41 rows through `classify_grant` on a scratch copy, then planted in a scratch copy of the real register and built). Output `raw/grants_hostile.txt`: `LIVE rows: 38; wrongly dropped: 30`; the build agrees row for row; all 3 controls drop.
- Today's real register is unharmed: 45 of 45 dropped rows judged right (table below).
- The dropped shapes that use words this register already holds (counted in the real file: LIFTED 10, "ends on his word" 7, "holds" 7, "half" 6):
  - past date: the register's line-34 sentence without the word CHANGED ("the END-OF-SUNDAY end of this grant is LIFTED; it now ends on his word"), prefixed to the first cell with the old EXPIRES cell left as it was, which is how line 66 was extended;
  - past date: Kam's words "until I say stop" quoted in the first cell;
  - past date: a RESTRICTION (the line-134 shape) kept in place by a later note in the scope cell. Dropping a restriction is the unsafe direction: the seat has no reason to look for it;
  - dead marker: "ENDED 2026-11-25 for the DEMO half only; the Kintsugi half is unchanged" (lines 49 and 126 record halves).
- Other dropped shapes (plausible, not yet seen): a new end date in the first or scope cell (only the EXPIRES cell is searched); `MONDAY 2026-11-23, for 14 days` read as an end; "rolled over", "still applies", "re-granted"; `CLOSED <date> made PERMANENT` on this seat's own row; CLOSED used for a HOLD; a lower-case "reopened"; another seat's row binding "the Studio seat", "no seat", "nobody else", "ALL-SEATS", "all 3 seats", the coordinators, `Launch_Wednesday.command`, a Platform K or Kintsugi slot.
- Expected: a row is dropped only on proof. Actual: every drop rests on one pattern plus a list of about 40 stop-words; a row that avoids the list is "proven".
- I rated two rows down after counting the register's vocabulary ("Studio" occurs 0 times, "no seat" once); the raw file keeps my first labels.
- Smallest fix shape: two independent signals per drop, not more words.
  - Dead: the marker with its date AND the rest of the cell says DEAD, SPENT, "do not rely" or "EVENT happened" (20 of today's 21 dead rows do, counted; line 24 would be kept, 1,411 bytes).
  - Past date: switch the class off until the register has a status column, or require that no other cell carries a later date and the first cell has no status prefix. Off costs today's 4 rows, 3,624 bytes.
  - Another seat's: drop only when the row also names that seat's client or project and none of this seat's words. Today's 14 rows for the other client still drop; six general-project rows of another seat would be kept, 6,565 bytes (counted).
  - Total about 11.5 KB on a 72.7 KB pack: about 21K of 60K tokens. The whole register kept (49,131 more bytes) would be about 30K. The budget is not the constraint; inclusion is cheap.

### N2. Blocker by the brief's rule (low likelihood): a false STALE LOCK report, and its recovery line loses an acknowledged block

- Ran: `scripts/false_stale.py`. Output `raw/false_stale.txt`.
- `acquire_lock` reads the owner file, then asks whether that pid is alive. Holder A finishes normally between the two; waiter B then prints `STALE LOCK ... held by pid <A> ... that process is no longer running (a write died part-way...)` with the `mv -n` line, in 0.01 s of a 30 s wait. Nothing died. The path the line names is by then writer C's live lock.
- The line run as printed, then the write repeated: `D rc 0; C then finishes rc 0. On disk: A 1, C 1, D 0` and `acknowledged block LOST: D`. Both exit 0.
- Natural runs under load: 371 trials of 5 writers, 1,855 acknowledged, 0 lost, 0 refusals. In my first race run one writer of 150 was refused rc 5 inside a 30 s wait; I had not kept its stderr, and 3,605 later acknowledged writes did not repeat it. Unexplained, consistent with this fault.
- Related, same cure: the recovery line run while a writer is alive (the LOCK BUSY message prints it too) loses a block, and the displaced writer only prints a WARNING at release and exits 0 (`raw/lock_attacks_CDEF.txt`, E1 and E3).
- Smallest fix shape: (a) report STALE only after a second look (retry `mkdir`, re-read the owner, same dead pid still there); (b) before each rename confirm the lock's owner is still this pid, else stop with rc 5 and rename nothing; (c) a writer that finds its lock gone at release exits non-zero.

### N3. Major: the recovery path ends in a refused rotation, and nothing sees a leftover lock before the next write

- The recovery line leaves `STATE-<seat>.lock.d.stale-<stamp>/owner`. Proposal 5's pattern `STATE-*.lock.d/` does not match it (`raw/proposals_check.txt` section 4: "not ignored"). `wednesday_rotate.sh` lines 154 to 158 refuse on any uncommitted or untracked path. So: crash, recovery, handover written, rotation REFUSED on a stray directory, at 85 to 90% context.
- Proposal 6 tells the seat a refused write "is simply run again". True for LOCK BUSY; a STALE lock refuses every time until the line is run.
- The doctor snippet says nothing about a lock directory (`proposals_check.txt` section 5; my printed "True" there is an instrument error, "lock" matched inside "block").
- Fix shape: ignore `0_Brain/tasks/STATE-*.lock.d*`; one doctor line that warns when a lock directory exists, with the recovery line; correct proposal 6's sentence.

**Is "a stale lock blocks every later handover until someone acts" the right failure direction?** Yes for the blocking, no for where it is discovered.
- Blocking is right: breaking a lock automatically is how a live lock gets broken (N2 shows the liveness test is already wrong once), and the refusal is immediate (0.1 s), loud, rc 5, with an exact line. The seat is an agent and can run one line; no person is needed, and the texts should say so.
- What is wrong is the timing: a lock left by a death at 10:00 is first met at the 85% handover. The smallest safe improvement is detection at boot (doctor or the launcher), not self-healing.
- Two smaller gaps: a writer killed between `mkdir` and the owner file, or between removing the owner file and `rmdir`, leaves an owner-less lock that costs the full 20 s wait on every attempt and is told "run it again" first (`lock_attacks_CDEF.txt` section D: 2 of 8 kill points). Reporting an owner-less lock older than a minute as stale would close it.

### Minor

- **N4.** An owner file whose pid exceeds a C int gives a Python traceback, rc 1, no recovery line (`lock_attacks_CDEF.txt` section C, 2 of 16 owner shapes). Nothing is written. Fix: catch `OverflowError` in `pid_alive`.
- **N5.** `--check` accepts free text in the sidecar's own `generated:` line (GREEN with a sentence appended). The pack's stamp line is protected only by accident, because the manifest prints its own size. Fix: validate the stamp's format in both.
- **N6.** The pack builds, rc 0 and silent, on a STATE file whose header names another seat or whose block was appended to by hand (`pack_attacks.txt` section 2). Doctor's check would warn, but the launcher builds and uses the pack regardless. Fix: the state part refuses what `handover.sh check` refuses.
- **N7.** A source cut short still builds rc 0: the grants file cut at 40% gives "28 rows in the file, 8 kept"; an identity file cut to 1 byte passes as not empty (`pack_attacks.txt` section 1, 9 cases). Truncation cannot be proven from the file alone; a cheap floor is a warning when a source shrank by more than half since the last build.
- **N8.** Test gaps. 11 of my 16 new mutants survive (`raw/my_mutants_Y.txt`); 2 of the first checker's 18 survive in adapted form. The ones that matter:
  - Y01 release removes a lock that is not this process's (the property "removes only its own lock" has no test);
  - Y02 STALE declared for a dead pid on any host;
  - Y03 an archive edit during the write is unseen;
  - Y09 the pack accepts a STATE file with no FLOOR part;
  - Y11 the launcher accepts an EMPTY pack file (`-e` for `-s`), and Q14 the launcher ignores the exit code when an older pack is on disk: "never boots on a stale pack" holds by my hand test and has no test in the suite;
  - Y07, Y08 two `--check` faults unreported; Y16 a typed `HANDOVER_TEST_STAMP` honoured on a real tree; Q12 an end date found anywhere in the cell.
  - Y10, Y12 are small; Y15 (no fsync) cannot be tested. I found no check that cannot fail.
- **N9.** Proposals 2 and 3 say the pack is read "in place of steps 1 to 3" and "items 1 to 5". Step 2 and item 3 are Kam's full-lesson-load sentence, so the added paragraph tells the pack seat not to do what the untouched sentence says, before he has answered. Wording that avoids it: "in place of steps 1 and 3; for step 2 see the question put to Kam". `FOR-KAM_lesson-load-ruling.md` itself is accurate: both quoted sentences are in the files word for word, and the two phrases it puts in Kam's mouth are the ones the launcher records.
- **N10.** `tools/stuart_weekly/stuart_weekly.sh` line 137 stages the top block of `NEXT-PICKUP.md`. After the cut-over that block is frozen and the script will stage it without complaint. No proposal names it.

### Notes

- **N11.** Handover edge behaviour changed from round 2 (`checker1_ho_tests.txt`): a CRLF block is refused with 10 heading faults whose message hides the carriage return; a block quoting an `# ARCHIVED` line is refused; a dangling-symlink state file is rc 4. All fail closed. Setext and quoted headings are accepted (m5).
- **N12.** `.git/info/exclude` line 29 ignores the lane's whole `out/`. It must go when proposal 5 is applied, or the round statuses there never reach git.
- **N13.** If the pack path is a directory the build fails rc 2 after writing the sidecar and leaving a temp file. "Nothing written" is not literal on that path.
- **N14.** `wake_pack.py` has no tree guard: `--seat tuesday` on a Wednesday tree builds from whatever Tuesday files that tree holds. The launcher passes `$AGENT`, so this is a hand-use risk only.
- **N15.** Seed: the block is 8,031 of 10,000 bytes at birth. GRANTS IN PLAY reads "none stated" while the carried STANDING lines (under FIRST WORK) hold the board grant whose outer read is today. The file's own 8-line header is not mentioned in the report.
- **N16.** Census: the AFTER figure is 57% the two daily notes (123,283 of 216,562 bytes) and moves through the day: 82.6% at the seat's 13:28, 81.8% at my 14:10.

## THE 45 DROPPED ROWS OF THE REAL REGISTER

Built on a scratch copy of the real inputs; the sidecar's line set equals the lane's stored one; 76 rows, 31 in the pack verbatim, 45 in the sidecar, none in both or neither (`raw/grants_real.txt`). Each row judged from its own text. **Right 45, wrong 0, doubtful 0.**

| Lines | Class | Judgement | Why |
|---|---|---|---|
| 10, 18, 19, 29, 30, 33, 35, 55, 57 | dead marker | right | another seat's grant; the cell records its end event as happened and says DEAD |
| 39, 41, 48, 53, 54, 61, 62, 64, 68, 69 | dead marker | right | this seat's own old grant; the cell says "DEAD, do not rely on it" (54 was a restriction whose end event the cell records) |
| 24 | dead marker | right | CLOSED because made permanent; the struck grant was another seat's and the rule lives in that seat's lesson |
| 72 | dead marker | right | END EVENT REACHED; the cell says spent, re-ask; another seat's project |
| 11, 17, 23, 27, 28, 32 | other seat | right | another seat's permission on its own claimed project; gives this seat nothing and binds it to nothing |
| 15, 16, 21, 22, 25, 37, 42, 43, 50, 63, 97, 98, 104 | other seat | right | another seat's work for the client this seat must not touch |
| 26 | other seat | right | another seat's HOLD on that client's project; right for this seat (a Friday build keeps the shape) |
| 49 | past date | right | 14-day window ended 2026-11-09; the cell records both halves retired |
| 59, 126, 142 | past date | right | true end dates weeks past; no later date or extension in the row |

Round 2's doubtful row (line 65) is now kept.

## ORDER TO APPLY

Safe now:
1. **Proposal 5 (gitignore)**, with the lock pattern widened to `0_Brain/tasks/STATE-*.lock.d*` (N3), and `.git/info/exclude` line 29 removed in the same action (N12).
2. **Proposal 2, replacements B and C only** (master drive, voice). True corrections, each old text present once; `speak.sh` lines 13 to 25 confirm C. They change shared text, so tell the other two seats.

After a round 4 that fixes N1 and N2 (and N3's three lines), and a re-check of those two only:
3. **Seed and launcher together, never apart.** A STATE file seeded days before the launcher change goes stale while the seat keeps writing the legacy pickup, and the first pack boot would then carry it. Seed dry, fill GRANTS IN PLAY by hand, write through `handover.sh write --stdin`, commit both STATE files, then apply **proposal 1** in the same sitting. Proposal 5 must already be in: the launcher creates `0_Brain/wake/` and the rotation refuses on an untracked path.
4. **Proposals 4 and 7 (doctor)** together, with the lock warning added.
5. **Proposal 2 replacement A, proposal 3, proposal 6** in one commit, with N9's wording and proposal 6's rc 5 sentence corrected.
6. **Proposal 8** once the state file has reached the NAS; a change for `stuart_weekly.sh` (N10) before the pickup is a week stale.

Must wait for the other two seats' agreement: proposal 1 (shared launcher; their prompts measured byte-identical, the file is still theirs too), proposals 4 and 7 (doctor output on their machines; 7 changes one line there), proposal 9.

Must wait for Kam: `FOR-KAM_lesson-load-ruling.md`; the daily-notes switch (`WAKE_NOTES`).

## WHAT HELD

- **Suite:** 177 passed, 0 failed on Python 3.14.10, and again on the system Python 3.9.6 (`suite_run.txt`, `suite_run_python39.txt`). **Mutants:** 114 of 114, the full run (`suite_mutants.txt`).
- **Races:** 4,544 acknowledged writes across 2, 3, 5 and 10 writers, 0 lost, 0 duplicated, 0 archive entry counts wrong, no lock or temp file left. With the lock removed the same harness sees a loss.
- **Starved writers:** 1, 5 and 10 queued behind a paused holder: all rc 5 in 1.1 to 1.2 s, LOCK BUSY naming the holder's pid, stdout empty, nothing written; run again they all land once.
- **kill -9 at 8 steps of a write**, then the printed recovery line, then a write: 0 acknowledged blocks lost at every step; one duplicate archive entry at the between-renames step only; `check` rc 0 throughout.
- **Foreign locks:** 14 of 16 owner shapes refused rc 5 with the lock left exactly as it was (a live unrelated pid, another host, garbage, a file, a dangling symlink among them); a foreign lock standing at release is left alone. No path writes without the lock: `write_locked` is called from two places, one dry.
- **rc 5** reaches a caller through a plain call, a pipe into the tool, and `&&`. It is hidden only by piping the tool's output into another command without `pipefail`.
- **Launcher:** the diff applies, `patch -R` restores the original byte for byte, `/bin/bash -n` (3.2.57) passes; 115 lines inserted, 0 removed; the only statement outside an `if AGENT = wednesday` block is four assignments of names the launcher did not use. Tuesday 21,100 bytes and Friday 21,991 bytes byte-identical before and after, no output, no pack built. Wednesday: pack prompt when the pack builds; loud fallback first for missing tool, missing source, older pack on disk, empty pack, no pack, no python3, over budget, hostile failure text. No `PWNED` file from hostile build output; the trace shows 3 added command substitutions, all in the build step, none in the prompt text.
- **Pack:** over budget writes nothing and leaves an older pack untouched; 12 planted conflict and `.pre-` files never read ("POISON-QA" 0 times; control "WEDNESDAY" 14 times); 6 simultaneous builds and 30 builds beside handover writes all consistent.
- **Seed:** dry writes nothing; 7 of 7 lines of the newest block and 8 of 8 standing lines carried; `--run` on the scratch copy rc 0, `check` OK, second run refused, legacy copy unchanged.
- **Census:** BEFORE 1,315,038 bytes with the two conflict copies, 1,190,847 without; AFTER 216,562 as proposed (pack 72,669), 93,279 with earlier notes on demand. Reduction 81.8% against the lower BEFORE, 83.5% against the higher.

## NOT TESTED

- A real launch, and the statusline after a pack boot.
- `doctor.sh` and `nas_staleness.sh` run with the proposals in them (text, syntax and the snippet in a stub harness only).
- The pack, seed and filter on Tuesday's and Friday's real files.
- The lock on the DevMASTER volume itself and across two hosts: my trees were on the internal disk (both APFS); "another host" was an owner file naming one.
- Durability across a power cut; real token counts (bytes/4 only).
- How a seat reads the changed sentences of proposals 2, 3 and 6.
- The mutant run on Python 3.9; `--trust-expired-heading` beyond the suite; the `WAKE_NOTES="ondemand"` branch beyond the suite's P12.
- The first checker's `kept.py`, `rows.py`, `table.py` were not re-run (my own row judgement replaces them).

## FOUND / TESTED / HOW

- Scratch root: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/16b0d124-652d-4b80-961e-2819b9865881/scratchpad/qa-wake-r3/`. Scripts in `scripts/`, raw output in `raw/`. Full text of the judged register rows is in scratch only (it carries other seats' rows).
- Mine: `qlib.py`, `lock_attacks.py`, `kwrap.py` (SIGKILL at a chosen step), `race_stale.py`, `false_stale.py`, `starve.py`, `grants_real.py`, `grants_hostile.py`, `pack_attacks.py`, `seed_real.py`, `launcher_harness.py`, `proposals_check.py`, `census_check.py`, `minors.py`, `my_mutants.py`.
- The first checker's scripts were run as unmodified copies from scratch (`race.py`, `extra.py`, `ho_tests.py`, `wp_tests.py`, `wp2.py`, `harness.py`, `h09.py`, `props.py`). Adapted: only its mutant list, in `my_mutants.py`, where 8 needles no longer occur (Q07, Q08, Q11, Q12, Q13, Q14, Q17, Q18); each adaptation breaks the same behaviour at today's line and is marked "adapted". Q14's adaptation is narrower than the original (the file test is kept), which is why it now survives.
- `race.py`'s last interleave line prints "LOST" for writer A; A exited rc 5 and was never acknowledged, as the seat said. Its natural part: 60 trials, 0 lost.
- Against the real tree: reads only, plus `wake_census.sh` (a scratch copy) with `--root` on the real tree, which reads sizes.
- Controls: every zero above has a positive control beside it in the raw file (the no-lock race, the three filter controls, the must-succeed seam case, the fresh and restored `--check`, the "WEDNESDAY" count, the `if [` count).
- Instrument errors of mine, kept:
  - `launcher_harness.py` run 1 compared each fallback with another tree's original prompt (all read "OTHER") and miscounted statements outside the guard; fixed and re-run; run 1 is `raw/launcher_harness_run1_instrument_error.txt`.
  - The first race run did not keep refused writers' stderr, so one rc 5 is of unknown kind.
  - `lock_attacks.py` part A2 meant to starve writers and starved none (0 refusals); `starve.py` does it properly.
  - `proposals_check.py` prints "True" for a doctor lock warning that does not exist.
  - Two plausibility labels in `grants_hostile.py` were too high and are corrected in N1.
  - `minors.py` left a small non-temp tree with copies of the two handover files at `nontemp_tree/` in this folder (needed to test m4); nothing was written into it by the tool.

## PROOF NOTHING WAS MODIFIED

Hashes taken at 13:51 and again at 14:21, after the last run (`raw/*_before.txt`, `raw/*_after.txt`), compared with `diff`. (`git status` shows four lane files as modified: that is the seat's own uncommitted round-3 work against HEAD, present at my baseline; the hashes show no change during this check.)
- lane, 46 files: identical (rc 0);
- first checker's folder, 37 files: identical (rc 0);
- `Launch_Wednesday.command`, both `CLAUDE.md` files, `.gitignore`, `doctor.sh`, `nas_staleness.sh`, `NEXT-PICKUP.md`, `EXPIRING-GRANTS.md`, `_ledger.md`: identical (rc 0);
- `ls -la 0_Brain/tasks`: identical (rc 0); `STATE-` 0 entries and `lock.d` 0 entries (control: `NEXT-PICKUP` 365 names); `0_Brain/wake` does not exist.
`ANSWER-4.md` (13:48, the coordinator's hold note) was in the lane before my baseline and is not mine.
