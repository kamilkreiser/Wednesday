VERDICT: GO WITH NOTES

Third, independent check of the lane `2_Project_Files/wake/` (WED-170 step 1, round 4), limited by Kam's ruling to N1, N2 and N3's three lines. Written 2026-11-27 18:43 AEDT (clock from `date`). **N1 is fixed:** the pack carries the real register byte for byte (89,267 bytes, 78 rows, at 18:09), the filter code is gone, and no hostile register I built made the pack change, drop, move or trim a row. **N2 is fixed:** I could not lose an acknowledged block. 5,221 acknowledged writes in races and displacements, 0 lost, with a negative control that does lose one; that includes 51 staged cases in which the lock of a live writer, paused at every point of its write, is moved away (15 of them by running the line the tool prints, as printed), and 238 cases where a live writer was caught at a random instant and its lock moved away. **N3's three lines are right.** Every number the seat reported reproduces. I found no Blocker and no Major. The notes are nine Minor findings (one of them a trap at the cut-over's first write, one a misleading "run it again" after an interrupted write, the rest test gaps and edges) and my judgement on the lock mechanism, which is: acceptable to ship, and worth replacing with a kernel file lock later as a small change, not as a condition. Nothing in the lane, the two earlier checkers' folders or the real tree was changed by me (proof at the end).

The whole check ran on a loaded machine: load1 was between 11 and 43 on 8 cores for every run (other seats' tests). No run failed on timing, so nothing here rests on a re-run.

Read first: the table, then THE LOCK MECHANISM, then ORDER TO APPLY.

## N1, N2, N3

| Point | Now | Evidence (under `raw/`) |
|---|---|---|
| N1 the register is carried whole | FIXED | `n1_register.txt` section 1: block between the markers equals the file, 89,267 of 89,267 bytes; 78 of 78 rows once each, in file order; a made-up row found 0 times. Section 2: 18 hostile registers: 8 carried byte for byte, 1 carried with one newline added (it had none at its end), 9 refused with nothing written. Sections 5 to 7: over budget refuses and leaves an older pack untouched; 11 one-byte and one-row edits of the block all RED; the old flag rc 2; no second file; the deleted names occur 0 times in `wake_pack.py`. `n1_extra.txt`. Residue: findings 3, 4, 5 |
| N2 the lock | FIXED | `r3_false_stale.txt` (the second checker's reproduction: the waiter no longer says STALE; the line run anyway: lost none); `n2_lock_DTK_and_S_run1_instrument_error.txt` sections D, T, K (51 displaced-writer and 9 kill cases, lost 0); `n2_fuzz.txt` (238 random displacements, lost 0); `n2_race.txt` (820 acknowledged with 3, 5, 10 and 20 writers, lost 0; control loses 1); `n2_volume_devmaster.txt` (480 more on the DevMASTER volume itself); `n2_lock_SX.txt`; `n2_lock_O_real_wait.txt`; `n2_signals.txt`. Residue: findings 1, 2, 6 |
| N3 ignore pattern, doctor warning, proposal 6 | FIXED | `n3_checks.txt`: 15 of 15 lock, temp and set-aside paths ignored by proposal 5; the six STATE files not ignored (and listed as untracked in a throw-away repo); doctor warns on every lock shape with the tool's own line and is silent on a set-aside one. `r3_launcher_harness.txt`: Tuesday 21,163 and Friday 22,048 bytes byte-identical before and after. Wording notes: finding 7 |

## NEW FINDINGS

No Blocker. No Major.

### Minor

**1. A write interrupted by Ctrl-C (SIGINT) leaves a lock that reads "LOCK BUSY, run it again" for a minute.**
- Ran: `scripts/n2_signals.py`. Output `raw/n2_signals.txt` section 1.
- Reproduction: writer paused after its second temp file is written; `kill -INT <pid>`. The writer exits with a Python traceback. Its `finally` removes the owner file, then `rmdir` fails because the temp files are still inside. Left: `STATE-wednesday.lock.d/` holding `archive.tmp.*` and `state.tmp.*`, no owner.
- Expected: the next write is told STALE at once (as after SIGTERM, SIGHUP and kill -9: 0.1 s, in the same file). Actual: `rc 5 LOCK BUSY` for the first 60 seconds, each attempt costing the full wait (20 s by default), with the words "run it again". After a minute it turns STALE.
- Nothing is lost (S0 1, S1 1, F 1 at every point). The cost is a minute and a wrong instruction at the handover.
- Same shape, same cure: when the owner file cannot be written after `mkdir` succeeded (injected ENOSPC), the call exits rc 4 and leaves the directory it had just made (section 2).
- Smallest fix: on any exit path, move the call's temp files out before removing the owner (the code already does this for an I/O fault and for LOCK LOST), and remove the directory the call itself made when the owner write fails.

**2. rc 6 after something else appeared inside the lock directory leaves the lock standing.**
- Ran: `scripts/n2_lock.py X`. Output `raw/n2_lock_SX.txt` section X.
- A foreign file put into the lock directory during the write (`.DS_Store`): both files replaced, owner removed, `rmdir` fails, rc 6. The state file holds the new block. The lock directory stays, owner-less. The caller's next write: LOCK BUSY, then STALE after a minute.
- This is the only way I found to reach rc 6 without the recovery line. It needs an outside actor in a window of milliseconds. In ordinary use: 60 plain writes in a row, exit codes `{0: 60}`; 1,300 racing writes, 0 with rc 6. A `._*` file does not do it: macOS removed it with the directory and the write was acknowledged.
- What is on disk in every rc 6 case (4 in that file, 10 more in sections D and T): the state file is this call's block, the archive holds the previous block, the state file is one block, `check` rc 0. A caller that reads rc 6 as "not written" and writes again gets its own block twice (once in the archive, once as state). Never a loss. Proposal 6's sentence (look with `show`) is right for it.
- Smallest fix: the same as finding 1 (do not remove the owner unless the directory can go), so the leftover reads STALE at once.

**3. Register text can imitate the pack's own markers and part headings.**
- Ran: `scripts/n1_register.py` section 3. Output `raw/n1_register.txt`.
- A register holding an END line, then `## c. State (the one-block handover)`, `## FIRST WORK`, an instruction, `## e. Own ledger`, and a BEGIN line builds rc 0. The pack then has 2 END lines, 2 BEGIN lines, two `## c. State` headings and two `## e.` headings. A reader who stops at the first END takes 89,268 of 89,717 bytes as the register and reads the forged FIRST WORK as a pack part. `--check` is GREEN (it is what a rebuild gives).
- The block is still the file byte for byte, and the part's first sentence gives the file's size and sha256, so the forgery is detectable by arithmetic, not by eye.
- Today's real register holds none of it: BEGIN or END text 0, a `---` line 0, a pack part heading 0 (control: its own `## ` headings 2). The register is written by the fleet's own seats, so this needs a careless paste, not an attacker.
- Smallest fix: fail the build when a register line equals the BEGIN or END line; or put the file's sha256 into both marker lines.

**4. `--check` reads GREEN on one kind of edited pack.**
- Same script, section 6. 11 edits of the register block RED; the twelfth GREEN: the three bytes of a U+FFFD character in the block replaced by one invalid byte 0xFF.
- Cause: `--check` hashes the decoded text, and an invalid byte decodes to the same replacement character.
- Not reachable today: U+FFFD occurs 0 times in the real register and 0 times in the real pack.
- Smallest fix: compare the file's bytes.

**5. The suite does not protect four register properties that hold in the code.**
- Ran: `scripts/my_mutants.py` (21 new mutants). Output `raw/my_mutants.txt`: 10 caught, 11 survive.
- Survivors that matter for N1:
  - G3, a register line over 2,000 characters is cut. The real register has 1 such line (2,151 characters).
  - G10, over budget the register is trimmed to half instead of the build refusing. "Never trim to fit" has no test in which trimming would make it fit.
  - G6, `--check` compares length, not content. The suite has no same-length edit.
  - G1, G2, G5, G7: trailing spaces stripped, CRLF normalised, no newline before END, NUL bytes removed. The fixture has none of these. (The real register has none either: 0 trailing spaces, 0 CR, 0 NUL.)
- I tested each property directly on the real code and it holds (`n1_register.txt`). The seat's sentence "a mutant that drops any row must go red" is true for its 12 mutants; it is not true of every such mutant.
- Smallest fix: one fixture row with a trailing space, one over 2,000 characters, a CRLF copy, a same-length `--check` edit, and an over-budget build whose refusal is compared with the register's size.

**6. The suite does not protect three lock paths.**
- Same file. L2: the owner is re-read before the archive rename only, not before the state rename; survives. L5: a failed release (owner or directory could not be removed) reported as released, so rc 0 and "written"; survives. L7: the token is the pid alone; survives (it needs a reused pid).
- L10 (the second look accepts any stale lock, not the same one) survives and I count it as equivalent.
- The code is right on all of these; no check would notice if it stopped being.

**7. Proposal 6 and the cut-over text: two missing sentences.**
- LOCK BUSY does not always mean "a write is running". It is also what the tool says, every time, for a lock whose owner names another host, has no host line, names a pid that has been reused by a live process, or was left by SIGINT less than a minute ago (`n2_lock_SX.txt` section S). The tool's own message carries the way out (the `pgrep` test and the line); proposal 6's sentence says only "run the command again". Add: "a LOCK BUSY that repeats: run `pgrep -fl handover_core.py`; if it prints nothing, run the line the message prints".
- `HANDOVER_CAP_BYTES` is named 0 times in `proposed/` (control: `handover.sh` 22 times). See ORDER TO APPLY step 3 for why it must be named.

**8. A write with a raised cap passes, and every later boot then fails its pack build.**
- Ran: `scripts/seed_cap_trap.py`. Output `raw/seed_cap_trap.txt`.
- A 10,086-byte block: refused rc 3 at the default cap. With `HANDOVER_CAP_BYTES=12000` for that one call: rc 0. Then `handover.sh check` (as doctor runs it): rc 1. Then `wake_pack.py` (as the launcher runs it): rc 2, no pack, "the block is 10086 bytes; the cap is 10000".
- The fallback is loud, so this is not a blind boot. It is a boot on the legacy reads at every launch until the block is rewritten.
- Smallest fix: one sentence in proposal 6 ("never raise the cap for a write; cut the block"), or have the header record the cap the block was written under.

**9. A register at a FIFO hangs the build, and so the launcher.**
- `n1_register.txt` section 2: no return after 8 s. Hunk A calls `wake_pack.py` with no time limit. Not a blind boot: no boot. Nobody makes the register a FIFO by accident; noted because the brief asked.

### Notes

- **A register rewritten in place in two steps** can be read half-way: 30 of 40 builds carried a half file, rc 0 (`n1_register.txt` section 4; my writer paused between the halves on purpose). With one plain `write()` per rewrite: 1,374 rewrites during 60 builds, 60 whole, 0 partial (`n1_extra.txt`). Replaced by rename: 40 of 40 whole. This is the second checker's N7, which the seat lists as not fixed.
- **A register that does not end in a newline** gets one added before the END line. Nothing is lost; the block is then the file plus one byte.
- **Set-aside material is never cleaned up.** `STATE-<seat>.lock.d.stale-<stamp>/` and `STATE-<seat>.md.tmp.<pid>` stay in `0_Brain/tasks/` for good. Proposal 5 ignores both. The same printed line run twice puts the second lock inside the first set-aside directory (rc 0 both times, still ignored).
- **The recovery line run while writers are alive never lost a block, but it can cost acknowledgements.** In the 6 three-actor cases where the displaced writer had not yet written its owner file, it wrote it into the NEW holder's lock; one or both writers then ended rc 4, 5 or 6, and in 3 of the 6 an owner-less lock was left for the next writer (`n2_lock_DTK_and_S_run1_instrument_error.txt` section T, the `C@after-mkdir` rows). All of it is refusal, none of it loss.
- **A closed stdout:** the writer exits rc 120 after writing and releasing (`n2_signals.txt` section 3). Written, not acknowledged; harmless.
- `proposed/01_launcher_boot_prompt.md` says "115 added lines"; the diff has 116 (`raw/lane_stored_evidence.txt`).
- The archive is rewritten whole at every write and has no rotation. At 10 KB a block it grows by megabytes a month. Not a fault today.

## THE LOCK MECHANISM (my judgement, for Wednesday and Kam)

**Plainly: the directory lock with a recovery line is acceptable for a seat that must hand over at 85% context. I would ship it. I would still replace it with a kernel file lock afterwards, as a small separate change, because that removes a class of leftovers this design can only report.**

What I could and could not do against the seat's stated limit (the guard is as strong as `rename(2)`, not stronger):
- I could not make it lose a block. For a loss, a second writer must take the lock, read both files, write and sync two temp files and rename both, all inside one rename system call of the first writer. User space cannot pause a process inside a system call (SIGSTOP takes effect at its edge), so this cannot be staged; it can only be hoped for.
- How hard I tried: 119 trials in which a real writer was frozen by SIGSTOP at a random instant while holding the lock, its lock moved away, two more writers run, and the writer resumed; 119 more with the lock moved away under a running writer. In those 238 the lock held, at that instant, the owner alone 149 times, the archive temp file 27 times, both temp files 32 times, the state temp file alone 8 times, nothing 22 times. Acknowledged 2,262, lost 0. Plus the 51 staged cases at every Python-visible point.
- So the limit is real in theory and I rate it as not reachable in practice on a local APFS volume. On a network volume a rename is a round trip and the window is wider; neither the tool nor I have run there.

Why it is acceptable:
- Every failure I produced ends in a refusal with an exact line, or in a non-acknowledgement with the block on disk. None ends in a loss or in a silent success.
- A stale lock costs the seat one `mv -n` line, which the tool prints, which doctor now prints at boot, and which a seat may run itself.
- Contention is the exception here: one seat writes its own state file.

Why a kernel lock (`flock` on a permanent lock file beside the state file) is still the better mechanism:
- It dies with its holder. No stale lock, no recovery line, no owner file, no second look, no one-minute rule, no rc 6, no pid reuse, no "another host" case, no set-aside directories. Findings 1 and 2 and half of finding 7 cannot occur.
- The recovery line is the only thing in this design that a careless hand can turn against a live writer. Round 4 made that safe by putting the temp files inside the lock. A kernel lock has no such line to misuse.
- It is less code than what round 4 added.
- Its own limits: it is advisory, it is per host, and it is unreliable on SMB and NFS. It protects no better than the directory lock across two machines, and no worse.

What I would not do: make the kernel lock a condition of this cut-over. That is a fourth round for a mechanism change, in a lane on its last life, against a risk I could not turn into one lost block in 5,221 attempts.

## ORDER TO APPLY (updated for round 4)

Safe to apply now, Wednesday's own action:
1. **Proposal 5 (`.gitignore`)**, and in the same action remove line 29 of `.git/info/exclude`. Checked: `raw/n3_checks.txt`. While line 29 stands, `2_Project_Files/wake/out/STATUS_round3.md` is ignored by it (seen in that file).
2. **Proposal 2, replacements B and C only** (master drive, voice), as the second verdict said. Each old text is in its target once (`raw/r3_proposals_check.txt`). They change shared text; tell the other two seats.

One sitting, after Tuesday and Friday have agreed to the launcher change:
3. **The first STATE block, then proposal 1, never apart.**
   - Run `handover.sh seed --from-legacy` dry at that moment and read the size it prints. The size follows the live pickup's newest block: 8,031 bytes at 13:28 (second verdict), 10,086 at 17:00 (the seat), **8,914 at 18:31** (mine, on a scratch copy of the real pickup: `raw/seed_cutover.txt`). It is under the cap now and may not be when you run it.
   - Do not use `--run` as it stands. GRANTS IN PLAY is seeded as "none stated in the legacy block" (52 bytes). Fill it by hand, then pipe the block to `handover.sh write --stdin`.
   - If the block is over 10,000 bytes: cut the largest part (FLOOR is 3,283 bytes, OWED 2,872) and leave a pointer to the daily note. **Do not raise `HANDOVER_CAP_BYTES` for that write** (finding 8).
   - If the block quotes a clock with an x digit, the hand path needs `HANDOVER_ALLOW_XCLOCK='<why, 15 characters or more>'`; `seed --run` would have set it for you.
   - Then: `handover.sh check` prints OK; `python3 2_Project_Files/wake/wake_pack.py --seat wednesday` exits 0; commit `STATE-wednesday.md` (the first write makes no archive file); apply proposal 1; `/bin/bash -n` on the launcher.
   - Step 1 must already be in: the build creates `0_Brain/wake/` and the rotation refuses on an untracked path.
4. **Proposals 4 and 7 (doctor)** together.
5. **Proposal 2 replacement A, proposal 3, proposal 6** in one commit. I would add finding 7's two sentences to proposal 6 first; that is Wednesday's edit, not a reason to wait.
6. **Proposal 8** once the state file has reached the NAS; **proposal 10** before the frozen pickup is a week stale.

Must wait for the other two seats' agreement: proposal 1 (the shared launcher; their prompts measured byte-identical, the file is still theirs too), proposals 4 and 7 (their doctor output: 7 changes one line; 4 is silent on a tree with no lock, no state file and no pack, measured for both), proposal 9.

Must wait for Kam: `FOR-KAM_lesson-load-ruling.md`; the daily-notes switch (`WAKE_NOTES`). New, and not blocking: whether the kernel lock is built later.

## WHAT HELD

- **Suite:** 199 passed, 0 failed, three times: Python 3.14.10; the system Python 3.9.6 as the interpreter; and again with 3.9.6 as the only `python3` on PATH, so that `handover.sh` itself runs on it (`suite_py314.txt`, `suite_py39.txt`, `suite_py39_only_on_path.txt`).
- **The lane's mutants:** 115 of 115 caught, the full run on the final code, in four ranges: 1 to 27, 28 to 44 (the 17 lock mutants, as their own stream), 45 to 89, 90 to 115. 0 not caught, 0 needle errors (`mutants_*.txt`). The lock stream took 24 minutes and did not have the machine to itself: the other ranges and my own tests ran beside it, under load 11 to 41. All 12 register mutants and all 17 lock mutants are in it.
- **My mutants:** 21 new, 10 caught, 11 survive (findings 5 and 6). `never_red.py`: of the 199 checks, 138 went red under at least one of the 136 mutants; 61 never did (`never_red.txt`). 13 of the 61 are must-succeed controls by their own text. The other 48 are positive-path and refusal checks with no mutant of their own; none is in the lock group, and in the register's path they are W06, W11, W11f, W18e and W18f. I read those five: each compares an exit code with a message or a file's presence and can fail. I found no check that cannot fail.
- **The second checker's scripts** (copies; only the scratch path in `qlib.py` changed): `false_stale.py` deterministic part: the waiter is refused LOCK BUSY at 29.95 s, never STALE; the line run anyway: A 1, C 0, D 1, lost none. Natural part 300 acknowledged, 0 lost. `lock_attacks.py` A: 940 acknowledged, 0 lost, 0 duplicated, 0 left. C: 16 of 16 owner shapes rc 5, no traceback, lock left as it was. D: 8 kill points, 0 lost. E1, E2, E3 conserved. `starve.py`: 1, 5 and 10 queued writers all rc 5 in 1.1 to 1.4 s, then all land once. `race_stale.py`: 200, 0 lost. The three differences the seat announced are as it said: part B stops at its own assert (my control replaces it); `kill:mkdir` and `kill:unlock-mid` read BUSY inside the first minute; `grants_hostile.py` cannot run (it calls a deleted function), and its 41 rows are in the suite's W05h, which passes.
- **Displaced writers** (the printed line run while the writer is alive): 15 pause points with D, E and F following, 78 acknowledged, 0 lost; a caller that writes again after a non-zero exit never lost or stacked a block, and got a second copy of its own block in 4 of 15. 36 three-actor cases, 141 acknowledged, 0 lost. Two displaced writers with the same line run twice: lost none.
- **kill -9 at 9 points:** 0 lost; temp files are found only inside the lock directory and leave with it; `check` rc 0 throughout.
- **Catchable signals at 5 points each:** SIGINT, SIGTERM, SIGHUP: 0 lost (finding 1 is about what the next writer is told).
- **Lock shapes:** 16, all rc 5, no traceback, left exactly as they were, state unchanged; a file or an owner-less directory older than a minute is STALE; a symlink to a directory with a dead owner is STALE; another host, a missing host line and a live unrelated pid are BUSY.
- **The owner-less rule with a real wait:** a writer killed between `mkdir` and the owner file; one waiter with a 120 s wait was told STALE when the lock was 60 s old (`n2_lock_O_real_wait.txt`).
- **On the DevMASTER volume itself** (APFS; both earlier checks ran on the internal disk only): 480 acknowledged with 3, 5, 10 and 20 writers, 0 lost; 3 kill points and one displaced writer, conserved.
- **Launcher:** the diff applies; `patch -R` restores the original byte for byte; `/bin/bash -n` passes on 3.2.57; 116 lines inserted, 0 removed. Tuesday and Friday byte-identical, no output, no pack built. Wednesday: the pack prompt when the pack builds; the loud notice first for a missing tool, a failed build, an older pack on disk, an empty pack, no pack, no python3, over budget and a hostile failure line. No `PWNED` file; the added lines hold 0 backticks and 2 command substitutions, both in the build step (they run `python3`, `printf` and `tail`).
- **The lane's stored evidence** equals its status: the stored pack's block is 87,458 bytes with the sha256 the status gives; the file sizes it lists are the sizes on disk; its mutant log holds 115 RED lines, 0 others (`lane_stored_evidence.txt`).

## NOT TESTED

- A real launch; `doctor.sh`, `nas_staleness.sh` and `stuart_weekly.sh` run with the proposals in them.
- Two hosts on one tree; a network volume; a non-APFS volume (there an AppleDouble file inside the lock directory could matter).
- The census was not re-measured by me. It is outside N1 to N3.
- Tuesday's and Friday's packs on their real files.
- Durability across a power cut; real token counts.
- The mutant runs on Python 3.9.
- How a seat reads proposal 6's changed sentence.
- A machine at rest: every run was under load 11 to 43.

## FOUND / TESTED / HOW

- Scratch root: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/435f0b28-fa4c-43b1-8811-a27f707f05c7/scratchpad/qa-wake-r4/`. One set of trees was made inside this folder on purpose, as `vol_tree/` (the lock on the DevMASTER volume itself: copies of the tools with their own `0_Brain/tasks`; 671 files, 14 MB). After the run I moved it to the scratch root with `mv -n`, so that this folder holds only the verdict, the scripts and the raw output; `raw/n2_volume_devmaster.txt` is what it produced.
- The second checker's scripts: `scripts/r3_copies/`. Adapted: `qlib.py` line 7, the scratch path, nothing else. Not run: `grants_hostile.py`, `grants_real.py`, `my_mutants.py`, `minors.py`, `census_check.py`, `seed_real.py`.
- Mine: `n1_register.py`, `n1_extra.py`, `pwrap.py` (pause, kill or plant at a named point of a write), `n2_lock.py`, `n2_race.py`, `n2_fuzz.py`, `n2_volume.py`, `n2_signals.py`, `n3_checks.py`, `my_mutants.py`, `never_red.py`, `seed_cutover.py`, `seed_cap_trap.py`, `hash_tree.sh`.
- Against the real tree: reads only, and `git check-ignore --no-index` with a scratch excludes file. No `handover.sh` or `wake_pack.py` call targeted the real tree.
- Controls: the no-lock race loses 1 of 168 acknowledged and refuses 12; the made-up row is found 0 times; `handover.sh` occurs 22 times where `HANDOVER_CAP` occurs 0; the two `--check` controls are GREEN beside 11 RED; the must-succeed budget build passes beside the refusal.
- Instrument errors of mine, kept:
  - `n2_lock.py` section S crashed on its last case (listing a mode-000 directory) and printed "state still S0 False" for 15 cases because it read the state after the retry. Output kept as `n2_lock_DTK_and_S_run1_instrument_error.txt` (sections D, T and K in it are sound and are the ones cited).
  - The re-run reused the first run's trees and stopped at case 4: `n2_lock_S_run2_instrument_error.txt`. The third run, on fresh trees, is `n2_lock_SX.txt`.
  - `n3_checks.py` run 1 made two lock paths as files and then could not make files inside them: `n3_checks_run1_instrument_error.txt`.
  - `n1_register.py` section 4 prints "header's sha16 matches the block: False" for the half-read builds; that compares against a block to which the tool had added a newline, and says nothing about the tool.
  - `n2_fuzz.py`: both modes hit the window in exactly 119 of 250 trials. The delays come from one seeded sequence, so the hit is mostly decided by the delay drawn; the two modes are less independent than two runs would be.
  - `n3_checks.py` flags `out/STATUS_round3.md` as "not as expected": my expectation ignored `.git/info/exclude` line 29, which is the known stop-gap.
  - One shell call of mine used an unquoted `==========` and was refused by a hook; another read `$?` after a pipeline. Neither result is used.

## PROOF NOTHING WAS MODIFIED

Hashes (sha256) taken at 18:04:49 before my first run and at 18:42:51 after my last, compared with `diff` (`raw/hashes_before.txt`, `raw/hashes_after.txt`, `raw/hashes_diff.txt`).
- the lane, 83 files: identical;
- the first checker's folder, 37 files: identical;
- the second checker's folder, 56 files: identical;
- `Launch_Wednesday.command`, both `CLAUDE.md` files, and 7 of the 9 `NEXT-PICKUP*.md` files: identical;
- **three live files differ, and not by my hand:** `EXPIRING-GRANTS.md` (last written 18:39:54, now 90,044 bytes; it was 89,267 when I copied it at 18:09), `NEXT-PICKUP.md` (last written 18:06:09) and `NEXT-PICKUP-TUESDAY.md` (last written 18:39:54). They are the running seats' working files. My scripts open a real-tree path for writing 0 times (control: they open the real register for reading 2 times); every build and every write ran on a copy.
- `0_Brain/tasks` holds 0 `STATE-` entries (control: 365 `NEXT-PICKUP` names); `0_Brain/wake` does not exist; no `__pycache__` appeared in the lane.
- `git status` was not used as proof: the lane's files show as modified against HEAD from the seat's own uncommitted work.
- In my own folder: `verdict.md`, `STATUS.md`, `scripts/` (14 files and `r3_copies/`), `raw/` (35 files). `COMMISSION.md` is the coordinator's.
