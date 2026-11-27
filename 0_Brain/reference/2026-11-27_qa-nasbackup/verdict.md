VERDICT: NO GO

The copy engine itself held up: across 17 oracle-checked destruction attacks on a fake NAS no content was ever lost at the destination, there is one rsync call and it carries no deleting flag, and the refusals (NAS not mounted, wrong case, lock, hold, window) all fired. It is NO GO for four other reasons, each reproduced here. (1) A run can be recorded GOOD while a changed file never reached the NAS, and the tool then never looks at that file again. (2) The secrets list matches names case-sensitively and exactly, so `4_credentials`, `.ENV`, `4_Credentials (conflict_on_…)` and 33 other shapes travel. (3) Another client's material travels: the seat's own real dry-run list holds 3,857 paths under `Testing Agent MAIN/projects/nexusai` (NexusAI is a Datasec project), and the Friday seat has no isolation at all. (4) A damaged or mistyped configuration widens what is copied, or empties it, and the run still says GOOD. The three-day flag also has two ways of never reaching Kam, and the test suite stays green with its central "counted on both sides" check removed.

Checker: independent QA, 2026-11-27 13:32 to 13:58 AEDT. Everything below was produced in this session on a scratch COPY of the lane against fake trees. Nothing was run against the real NAS. Scripts: `scripts/`. Raw output: `scripts/out/`.

## FINDINGS

### 1. Blocker — a run is recorded GOOD while a changed file was not delivered, and the file is then never checked again
- Reproduce: `scripts/H_false_good.sh` → `scripts/out/H_false_good.out`.
- What: a file changes at the source without changing size, and its transfer fails for that one file (rsync exit 23). Two triggers were used: the destination copy made immutable (`chflags uchg`, standing in for a file locked or permission-protected on the share), and a stub engine that skips one listed file and exits 23.
- Expected: the run fails, because one in-scope file is not at the destination with the source's content.
- Happened (H1): GOOD on 5 of 6 nights, with the engine's stderr carrying the rename error each night. Source `LEDGER-v7-BBBB`, destination still `LEDGER-v1-AAAA`. On night 7, with nothing changed at the source, the plan was `to copy: 0 files` and the run was GOOD again: the stale copy is now permanent. H2 (stub engine): GOOD on 8 of 10 nights.
- Why: `nb_core.py` lines 1132 to 1135 tolerate exit 23 on the promise that every file is "accounted for one by one afterwards"; that accounting (lines 1148 to 1157) compares SIZE only, then writes the file's new source stat into the index (line 1172), so later runs skip the hash. The 40-file sha256 sample is the only other check: it caught it on 1 of 6 and 2 of 10 nights in a 303-file set; in the real 265,195-file set the chance per night is 40 in 265,195.
- Controls: the same failure with a different-size change fails (rc 8); the same same-size change with a healthy engine arrives.
- Smallest fix: after the copy, compare by sha256 every file that was sent for reason `content` (they are few), index a file only when its arrival is proven, and treat exit 23 as a failure unless every listed path appears in the engine's itemised log.

### 2. Blocker — secrets travel when the name differs in case or decoration from the fixed list
- Reproduce: `scripts/B_secrets_isolation.sh` → `scripts/out/B_secrets_isolation.out` (sections B3, B4, B5/B6); real-scope scan `scripts/B2_scan_real_dry_lists.py`, `B2b_real_list_detail.py` → their `.out` files.
- Expected: no folder or file of these shapes reaches the NAS.
- Happened: every run exited 0 and said GOOD.
  - Case variants: 12 of 12 leaked (`4_credentials/`, `4_CREDENTIALS/`, `3_access_keys/`, `.ENV`, `.Env.local`, `server.PEM`, `private.KEY`, `ID_RSA`, `Credentials.json`, `Secrets.json`, `.SSH/`, `.AWS/`). The drive is case-sensitive and `Rules.match` uses `fnmatch.fnmatchcase`.
  - Unlisted shapes: 24 of 24 leaked, including `4_Credentials (conflict_on_2026-09-17)/`, `4_Credentials.bak/`, `4_Credentials copy/`, `old_3_Access_Keys/`, `.env (conflict_on_2026-09-17)`, `prod.env.bak`, `.envrc`, `github_deploy_rw` (this workspace's deploy-key name), `.git-credentials`, `key.ppk`, `terraform.tfstate`, `client_secret.json`. Conflict copies are a real shape on this drive: the seat's dry-run list holds 197 `conflict_on_` paths.
  - A hard link into `4_Credentials/` under an ordinary name: leaked (1 of 1). A symlink into it: kept out.
- Control: the 12 listed spellings, nested deep and under a path with spaces, were all kept out; the ordinary neighbour arrived.
- In today's real scope (names only, from the seat's own dry-run lists, 1,109,015 paths; no file opened): 0 paths with a `4_credentials` or `3_access_keys` component in any case; 0 key or certificate extensions; 1 file named `.env1` (`Agentic Coding/…/tac-2/app/server/.env1`, 271 bytes) and 63 `.envrc` files that WOULD travel. So the hole is open today for one real file and latent for the rest.
- Smallest fix: match the secret list case-insensitively and as a contained token for the two folder names (`*4_credentials*`, `*3_access_keys*`, `.env*`, `*.env.*`); add the common credential names; refuse an in-scope file whose inode is also inside an excluded secrets folder.

### 3. Blocker — another client's material travels
- Reproduce: `scripts/B2c_real_list_clients.py` → `.out`; `scripts/B7b_B12_clients_seats.sh` → `.out`; `scripts/B_secrets_isolation.sh` section B9.
- Real scope, names only, from the seat's dry-run lists: the "general" set `CODING/Testing Agent MAIN` holds `projects/nexusai` (3,857 paths) and `projects/hpsm` (2,551 paths); the WEDNESDAY tree holds 1,114 paths with `nexusai` in the name; `Security Testing Agent` holds `Security_Audit_NexusAI_2026-04-26.md`. The workspace `CLAUDE.md` lists NexusAI as a Datasec project. All of it would land in `General/Wednesday/` on the NAS. (Whose client `hpsm` is I do not know.) The same set also puts 166,196 paths of Secuura test material into the General folder, not the Secuura one.
- The only other-client rule is the two globs `*[Dd]atasec*` and `*DATASEC*`. Measured on fakes: `DataSec`, `DATAsec`, `dataSEC` leak (4 of 4 mixed-case spellings; the 3 listed spellings are kept out); a Datasec project under its own name leaks (3 of 3: `NexusAI`, `Vision_Sales_Portal`, `nexusai`).
- A `set=` source reaches another client's folder by two routes the forbid check misses: through a symlinked parent (`CODING/alias/proj`, alias → `Datasec`: exit 0, copied) and through a folder whose name merely contains the client (`CODING/Datasec-archive`: exit 0, copied). Seven other spellings were refused.
- Tuesday seat (fake TUESDAY tree): writes only to `Datasec/Tuesday` and refuses the three cross-client `set=` lines tried, but carries Secuura's projects under their own names (`Blockchain`, `Platform-K`), `SecUura` in mixed case, and the Wednesday seat's folders in the shared tree (`2_Project_Files/wednesday`, `0_Brain/daily_wednesday`) into the Datasec folder.
- Friday seat as shipped in `SEATS` (`forbid: []`, no other-client names): a Datasec folder, a Secuura folder, a tuesday folder and `set=` lines pointed at both client folders all arrive in `General/Friday` (5 of 5). Today only `status=unconfirmed` and the hold stand in front of that.
- Smallest fix: per seat, a list of the other clients' PROJECT names matched case-insensitively; resolve `set=` sources with `realpath` before the forbid check and forbid by containment, not by exact component; two `exclude_path` lines for `Testing Agent MAIN` now, or Kam's ruling that test reports about a Datasec project are general; no Friday entry in `SEATS` until Kam rules.

### 4. Blocker — a damaged or mistyped configuration fails open, and an emptied scope is reported GOOD
- Reproduce: `scripts/B_secrets_isolation.sh` sections B8 and B10 → `scripts/out/B_secrets_isolation.out`.
- Expected: a conf that lost lines, or whose exclusion names nothing, is refused or at least reported.
- Happened, each with exit 0 and a GOOD line:
  - truncated 40 bytes before the end: the quarantine folder excluded by the lost line was copied;
  - every `exclude…` line lost: the excluded bulk and the quarantine folder were copied;
  - `exclude_path` with a one-letter typo: accepted silently, the bulk was copied;
  - `exclude_name=*`: nothing at all was backed up, and the run said GOOD;
  - a source set that became empty after a good 3-file night: GOOD with 0 files, no line about the drop.
- Held: empty conf, missing conf, missing `status=`, a garbage line and a UTF-8 BOM were refused; CRLF endings parsed correctly.
- On the real conf, by arithmetic on the seat's own figures (not measured): losing only the last line (`exclude_path=Secuura|Blockchain/scratchpad`, 73,847 files) gives 660,932 files, under `max_files=700000`, so that run would pass.
- Smallest fix: an end marker or line count the parser requires; refuse an `exclude_path` that does not exist at the source; fail (or flag) a set whose in-scope count falls to zero or drops sharply against the last good run.

### 5. Major — the three-day flag never fires if the arming mark is missing
- Reproduce: `scripts/C_lock_catchup_watch.sh` section C4b → `scripts/out/C_lock_catchup_watch.out`.
- With no good backup on record and `--mark-armed` never run, 10 nights of refused fires (40) and 10 boot checks produced 0 card commands; the watch said `ok; 56.5 h since the first recorded attempt` every day from day 3. Cause: the "first attempt" is the minimum of a rolling list of 12, and four fires a night push the oldest out before 72 hours pass. Control: the same 10 days with `--mark-armed` gave exactly 1 card on day 3.
- The mark is set only by one proposed line in `install_all_jobs.sh`. The real lane's state today is `armed_at=None`, one attempt.
- Smallest fix: store `first_attempt_at` once and never roll it.

### 6. Major — the one card command lands in a launchd log, and the launcher proposal has no channel to the seat
- Reproduce: `scripts/C_lock_catchup_watch.sh` section C4d; `scripts/E_proposals.sh` section E5 → `scripts/out/E_proposals.out`.
- The nightly job calls the watch with `--flag`, so on night 3 the single `CARD-COMMAND` line goes to the job's stdout (`~/Library/Logs/<seat>_nasbackup.out` under launchd). The launcher's `--flag` at the next boot then prints 0 card lines, only a reminder pointing at `--reprint`. The proposed doctor hint says "run `--flag` (it prints the ONE card)": it will not. The suite asserts this behaviour as correct (T8).
- The launcher proposal pipes into `tee -a "$PREFLIGHT_LOG"`. The real launcher has 0 occurrences of that name, runs under `set -u`, and its only preflight file is a temp file removed straight after doctor. Applied literally: `PREFLIGHT_LOG: unbound variable` at every boot of every seat and the watch's line is lost (the boot itself continues). Nothing carries launcher scrollback into the seat's prompt except `✗` lines on a rotation.
- Net: after arming as proposed, no card reaches Kam unless a seat notices a doctor warning and works out `--reprint`.
- Smallest fix: the nightly call uses `--check`; only a caller a seat reads marks the card as issued; doctor's hint names `--reprint`; the launcher lines write to a real file that the boot prompt reads.

### 7. Major — a folder replaced by a file of the same name makes every later run fail
- Reproduce: `scripts/A_destruction.sh` sections A6 and A5 → `scripts/out/A_destruction.out`.
- A6: after `thing/` becomes a file `thing`, the run fails (rc 8), the next night fails the same way, `last_good` never advances and the new file is on the NAS 0 times. Nothing in the tool can resolve it, an approved out-of-sequence run included.
- A5 (file becomes folder): the run says "not copied" and fails, but the engine did replace the destination file with the folder, keeping the old file under `versions/`; the next night is GOOD. Nothing lost, the message is wrong.
- Smallest fix: on a type change, move the old destination entry into `versions/<stamp>/` and copy the new one.

### 8. Major — after SIGKILL the engine keeps writing, and the "stale" lock can be cleared beside it
- Reproduce: `scripts/A3_interrupt_full_REDO.sh` → `scripts/out/A3_interrupt_full_REDO.out`.
- 2 s after `kill -KILL` of the tool, 3 rsync processes were still running and files were still arriving. `--clear-stale-lock` succeeded (rc 0) while they ran, and a second run then ran beside the orphan and said GOOD. Nothing was lost in this one trial (oracle 0 of 8; all 5 old copies kept). The lock's purpose, one writer, did not hold.
- SIGTERM is clean: child stopped, run recorded failed, lock released, rerun GOOD.
- Smallest fix: `--clear-stale-lock` refuses while any rsync holds the seat's destination path; start the engine in its own process group and record that id in the lock.

### 9. Major — a damaged state file stops the backup and the flag together
- Reproduce: `scripts/C_lock_catchup_watch.sh` section C4e.
- With a garbage, empty or truncated `state/<seat>.json`: the watch, the nightly job and a manual run all exit 1 with a Python traceback; the nightly job writes no line to `nightly.log`. The proposed doctor block would show `nas_backup_watch.sh exited 1 — Traceback (most recent call last):` (`scripts/out/E_proposals.out`, E6 d). No card can be raised.
- Smallest fix: catch the JSON error, print one plain line naming the file, exit 3 from the watch.

### 10. Major — the suite stays green with central guards removed
- Reproduce: `scripts/D_my_mutants.sh` → `scripts/out/D_my_mutants.out`.
- My 18 mutants (none repeats one of the seat's): **4 caught, 14 survived**, 0 not applied; the unmutated control passed 167 of 167 first.
- Survived, each with 167 PASS and 0 FAIL:
  - Q02 the arrival check made vacuous (every sent file counted as arrived): the claim "exit 0 is not success, the equal counts are" has no test. This is the guard finding 1 is about.
  - Q09 the sha256 sample result ignored.
  - Q01 the other-client name exclusion removed.
  - Q03 and Q04 `exclude_path`, `exclude_name` and `exclude_name_in` ignored: the lines that take the scope from 8.9 million files to 1 million are untested.
  - Q10 `.env.*`, `*.env`, `*.key`, `*.p12`, `*.pfx` dropped from the secret list.
  - Q05 symlinked source allowed; Q07 `..` in a destination name allowed (the guard itself works, see WHAT HELD); Q06 the `/private/tmp` fence on test mode removed.
  - Q08 rsync version check off; Q11 type conflict not reported; Q12 unreadable source folders not reported; Q17 state file of another seat accepted; Q18 attempt history cut to 1.
- Caught: Q13 dry run creates folders, Q14 window never closes, Q15 COMPLETE marker always written, Q16 forbid check off.
- The seat's claim "each test shown able to fail" is true for the 20 guards it chose (re-run here on my copy: control 167 passed, 20 caught, 0 survived). It does not show that each guard has a test.

### 11. Major — install proposal: Step 1 before Step 2 walks past the hold
- Reproduce: `scripts/E_proposals.sh` section E1.
- With the template copied into `scheduler/jobs/` and the installer not yet edited (the order the proposal gives), the unmodified installer ignores `HOLD_wednesday`, writes `com.wednesday.nasbackup.plist` with eight unrendered `@NB…@` placeholders and calls `launchctl load` on it. `plutil -lint` rejects that file, so launchd very probably refuses it (real launchctl was NOT run here); `--check` then reports the job MISSING and doctor would advise running the installer.
- With Step 2 applied first everything behaved: held seat skipped, unconfirmed conf skipped, plist valid, times right, arming mark set, `naspush` still renders.
- Smallest fix: swap the steps, or ship both in one change.

### 12. Minor findings
- **Loser of a simultaneous start is told the wrong thing.** 8 of 8 trials: exactly one winner, and the loser was told `STALE lock` about a live run (it looks before the owner file is written). `scripts/out/C_lock_catchup_watch.out` C1.
- **A reused pid whose command line contains `nas_backup` counts as a live holder.** The run refuses, the nightly job skips "in progress", and `--clear-stale-lock` refuses, until that process ends. An unrelated `sleep` is correctly treated as stale. C2.
- **PORTABILITY proposal says the last section is 30 and proposes "## 31".** A section 31 already exists. E7.
- **Doctor proposal.** It warns HELD at every boot on every held seat (Friday permanently). With `WED_AGENT` unset on a TUESDAY tree doctor's own default makes the block look at `HOLD_wednesday`. E6.
- **Daylight saving.** On the spring-forward day Tuesday's window computes as 03:30 to 06:30, so her 03:20 fire is skipped and the window runs an hour past her 05:30 shift change. C3.
- **`._*` excludes a real folder of that shape** with its contents (counted under `system`). `scripts/out/G_misc.out` G2.
- **INSTRUCTIONS-for-other-seats.** Step 6 has Tuesday and Friday apply the installer edits themselves to a shared tracked file Wednesday will already have changed. Step 5 omits `--max-seconds`, so a large first copy stops at the cap. Friday's two open questions are listed as a prerequisite but nothing says stop. Nothing in it writes or deletes on the share. The suite passes from a TUESDAY tree (167 of 167, `scripts/out/I_suite_on_tuesday_tree.out`).
- **Schedule.** First fires are two hours apart as asked (00:30, 02:30, 04:30), and the three rendered plists lint OK. The retry fires interleave (Wednesday 02:50 and 04:00, Tuesday 02:30 to 05:00, Friday from 04:30), the lock is per seat, so two seats can copy to the NAS at once whenever a first fire was missed or a run is long. No wake is scheduled: a Mac asleep through its whole window does not back up that night.

### 13. Notes
- A rename that differs only in case keeps the OLD spelling at the destination with the new content (`report.txt` holds `REPORT.txt`'s content). Nothing lost.
- The real dry run never handed the engine a NAS path (0 of 14 engine lines; the destination did not exist, so it compared against a local empty folder). "A dry run writes nothing to the NAS" is therefore proven here on a fake only, not on the share.

## WHAT HELD

- **No content lost at the destination: 17 of 17 oracle checks read 0 lost** (8 in `A_destruction.out`, 5 in the valid sections of `A2_interrupt_full_case.out`, 3 in `A3_interrupt_full_REDO.out`, 1 in `G_misc.out`). Cases: Changed, shrunk to zero, same-size change, removed at source, file to folder, folder to file, file to symlink, case-only rename (file and folder), NFC to NFD rename, source folders named like the tool's own, unwritable `versions/`, SIGTERM mid-copy, SIGKILL mid-copy with a concurrent rerun, full destination (twice), real case-colliding pairs on a case-sensitive source, a colliding sibling appearing then the original going, NFC source against an NFD-returning destination, 17 odd names changed. Oracle control: a file taken away by hand is reported lost.
- **One engine call, no deleting flag.** `rsync [-n] -t -O -I --from0 --files-from=<list> --backup --backup-dir=<versions/stamp/set> --timeout=<n> --out-format='%i %n%L' --stats --no-h [--temp-dir=<_tmp_incoming>] <src>/ <dest>/`. No `--delete*`, `--remove-source-files`, `--inplace`, `--force`, `-r`, `-a`, `-l`. No `rm`, `unlink` or `rmtree` in the five code files; the three renames are the state file and the lock.
- **Full destination:** the run fails (rc 5), not recorded good, nothing lost, no temp files left.
- **A dry run writes nothing** to an existing fake destination (stat listing identical; control changes it).
- **Listed secret names:** 12 of 12 kept out, nested and under spaces. Symlinks are recorded, never followed.
- **Destination escape:** 10 of 10 `set=` lines aimed outside the seat's folder refused, tree unchanged.
- **Not mounted:** refused, 0 entries created in the local folder, never counted as a backup, flagged after 3 days. Share swapped for an empty local folder mid-run: failed, 0 files written into it.
- **Locking:** 8 of 8 simultaneous starts had one winner; dead pid and unrelated pid treated as stale and left in place.
- **Catch-up:** one run per window; three missed nights caught up by exactly one run; outside the window never runs; a window crossing midnight behaves.
- **Flag:** fires at 72 h after the last good start, not at 71.98 h; 30 further boots printed 0 more cards; quiet under the hold.
- **Evidence files match STATUS:** 167 PASS and 0 FAIL, 20 CAUGHT, 18 and 2 on the first pass, 1,012,113 files and 67.83 GiB, 982 symlinks, 7,085 exclusions, 421 s, NAS listing identical before and after. The 32-hour figure is labelled an extrapolation.
- **Not armed:** 0 `nasbackup` templates in `scheduler/jobs`, 0 `nasbackup` plists in `~/Library/LaunchAgents` (control: 1 `naspush`), 3 HOLD files present.

## NOT TESTED

- **Anything on the real NAS**, in any mode: SMB rename and temp-folder behaviour, whether it keeps file times, names SMB rejects (`:`, `?`, trailing dot or space), path-length limits, Unicode as the share returns it, real free space (`statvfs`), speed. My case-insensitive fake was an HFS+ disk image, not SMB.
- **launchd and launchctl.** I ran no launchctl verb at all; "not armed" rests on file listings. Whether launchd refuses the unrendered plist of finding 11 is inferred from `plutil`.
- **The real, non-test code path end to end** (fixed NAS root, real mount table inside a run). Only the two mount-parsing functions were called directly.
- **The patched doctor and launcher as whole scripts.** The doctor block ran in a harness with launchctl stubbed; the patched doctor got `bash -n` only.
- **Scale:** a million files, the index at that size, memory, the whole-run watchdog, the 5-hour cap.
- **A reboot or power loss mid-run**; sleep during a run.
- **Finding 1 with a naturally occurring trigger.** I forced the per-file failure; I did not find which real share conditions produce exit 23 for one file. A too-long `versions/` path is a candidate I did not test.
- **Finding 8** was one trial; a race that loses data there is not excluded.
- **State-file races** between the watch and a running backup (read, then write, no lock): read in the code, not reproduced.
- **Contents of any file.** Secret and client findings on the real scope are by NAME from the seat's dry-run lists of 12:59; `.env1` was not opened. A secret in an ordinary-named file is invisible to all of this.
- **Tuesday's and Friday's real trees and machines.**
- **Python 3.9** beyond the suite's own T10.

- **The lane as it changed during this check.** Between 13:37 and 13:39 someone else added 16 files to the lane (`ANSWER-1.md`, `RESULT-secrets-move.md`, `evidence/secrets-move/*`), edited `scheduler/nas_push.sh`, and a folder `_quarantine_2026-11-27_secuura-secrets` appeared on the Backup share. I reviewed none of that; this verdict covers the lane as hashed at 13:32.

## DID THE CHECKER MODIFY ANYTHING

Check: `scripts/out/Z_nothing_modified.out` (sha256 and stat lists of the lane before and after; `df` and top-level stat of the three shares before and after).
- Real lane: of the 85 files hashed at 13:32, 0 changed and 0 were removed. 16 files were ADDED, not by me (named above; their own timestamps are 13:37 to 13:39, and they are the build seat's secrets-move evidence).
- `/Volumes/DEV-Working` and `/Volumes/Seagate Hub`: `df` and top-level stat lines identical before and after.
- `/Volumes/Backup`: NOT identical. One new top-level folder, `_quarantine_2026-11-27_secuura-secrets`, mtime 13:39:27, 1,344 KB more used. Not mine: the lane's `evidence/secrets-move/04_mkquar.txt` carries that minute, and the only lines in my scripts that name a real NAS path are three in `G_misc.sh` (two strings passed to a mount-table parser, one grep of the seat's evidence file). I cannot prove a negative beyond that.
- Scratch disk images: all three detached.

## FOUND / TESTED / HOW

- **Scope:** the lane as it stood at 13:32 (85 files hashed), all five proposals, and their four real targets read.
- **Instruments:** a scratch copy of the lane; fake source trees and fake NAS folders under the session scratchpad; three disk images made with `hdiutil` inside scratch (two 12 MB case-insensitive HFS+ as NAS, one 40 MB case-sensitive APFS as source); `scripts/oracle.py` (sha256 of every destination file before and after); marker strings in file content with `grep -r` for arrival; stub engines; a stub `launchctl` and a scratch `HOME` for the installer.
- **Positive controls:** the oracle reports a removed file; the arrival grep finds an ordinary neighbour and the planted secret at the source; the stat-listing hash changes when a file is added; the unmutated suite passes before any mutant; the real-list scan finds 52,170 `.md` paths.
- **Negative controls:** listed secret names kept out; intact conf excludes what the damaged ones let through; different-size and healthy-engine cases beside finding 1; `--mark-armed` beside finding 5.
- **Errors of my own instrument, outputs kept:**
  1. `A2_interrupt_full_case.sh` built its "big" files at 350 KB instead of 1 MB and 2.5 MB, so SIGKILL arrived after the copy and the 12 MB image never filled. Its A10-KILL and A11 lines are void (`A2_interrupt_full_case.FLAWED-first-run.out`); redone in `A3_interrupt_full_REDO.sh`. Its A10-TERM and A15 sections stand.
  2. `B_secrets_isolation.sh` B7 planted `DataSec`, `DATAsec` and `TuesDay` beside the listed spelling on a case-insensitive volume, so they were the same folder; those "kept out" lines are void. Redone in `B7b_B12_clients_seats.sh`.
  3. B9 reuses one fixture, so its "on NAS" counts are cumulative: the leaks are the rows where a count first becomes 1.
  4. In E2 the `--check` line "1 missing" is `naspush` under my stub, not `nasbackup`.
  5. I predicted the literal launcher block would kill the boot; the test showed it does not (finding 6 states what it does).
