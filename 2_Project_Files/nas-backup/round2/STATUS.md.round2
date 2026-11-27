READY FOR QA

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
