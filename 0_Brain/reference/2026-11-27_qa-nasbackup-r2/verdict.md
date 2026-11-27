VERDICT: NO GO

Round 2 fixed what round 1 was failed for, as far as the first checker's own attacks go: his two false-GOOD triggers now fail every night (0 GOOD in 17 nights), all 12 case variants and the hard link stay out, a damaged conf is refused, the type change works, the lock holds beside an orphan engine, the card reaches doctor, the install order no longer matters, and nothing was lost at the destination in 8 of 8 oracle checks. It is still NO GO, for one clear reason and four narrower ones, each reproduced here on a scratch copy. (1) The seat's stated departure from ruling 1 is a hole: any source file or folder that cannot be READ at proof time is counted "gone from the source" and dropped from scope, so a run says GOOD while files never reached the NAS, every night, and a changed file keeps last night's content at the destination for good. This answers the coordinator's question in ANSWER-3 with yes. (2) Conventional credential names still travel (`.htpasswd`, `terraform.tfvars`, `.docker/config.json`, `service-account*.json` and others), and two such files, both git-ignored and each holding one credential-like value, are in today's real travel list. (3) A `set=` that names a PARENT folder carries the TUESDAY and FRIDAY trees to the NAS. (4) A set with folders but zero files is GOOD when there is no earlier good run to compare with. (5) When the nightly sample finds a destination copy that differs, the run fails that night, repairs nothing, and says GOOD again on the next night the sample misses it. Fixes 1, 3, 4 and 5 are a few lines each; 2 is a list addition. Name rules are best-effort by nature and are judged that way below.

Checker: fresh independent re-check, 2026-11-27 15:27 to 16:01 AEDT. Everything below is from this session, on a scratch COPY of the lane against fake trees, plus read-only reads of the real drive. The lane's tools were never pointed at a NAS path. Scripts: `scripts/`. Raw output: `raw/`.

## PRIOR FINDINGS AND RULINGS

| # | Round 1 finding | Round 2 | Evidence |
|---|---|---|---|
| 1 | False GOOD (Blocker) | **PARTLY.** His triggers are fixed: H1 (immutable destination) 0 GOOD in 7 nights, H2 (stub skips a file, exit 23) 0 GOOD in 10, both controls right. The class is not closed: new finding 1 | `raw/r1_H_false_good.out`, `raw/N1_good_truth.out` |
| 2 | Secrets by case and decoration (Blocker) | **PARTLY.** 12 of 12 listed names, 12 of 12 case variants, the hard link: kept out. Of his 24 unlisted shapes, 16 kept out, **8 still travel** (new finding 2) | `raw/r1_B_secrets_isolation.out` |
| 3 | Other clients (Blocker) | **FIXED as ruled.** 9 of 9 source spellings refused (symlinked parent, `Datasec-archive`, `..`); Datasec names 7 of 7 excluded; other seats' names 5 of 5 excluded in the seat tree; project names travel and are counted, as the corrected bullet says. A new route by an ancestor folder: new finding 3 | `raw/r1_B_secrets_isolation.out` B9, `raw/r1_B7b_B12_clients_seats.out`, `raw/N6_flag_lock_seats.out` N9 |
| 4 | Conf fails open (Blocker) | **PARTLY.** His five cases fixed: 9 damaged confs refused (exit 2), CRLF parsed with exclusions honoured, emptied set exit 8 twice. Zero files with folders and no baseline is GOOD: new finding 4 | `raw/r1_B_secrets_isolation.out` B8, B10; `raw/N3_index_shrink_conf.out` N4c, N4d |
| 5 | Flag never fires without arming | **FIXED** (the seat's T9 in my run of the suite; its mutant N10 caught in my rerun). My adapted copy of his C4b is void: it calls `--flag`, which round 2 removed | `raw/suite_run.txt`, `raw/seat_mutants_rerun.txt` |
| 6 | Card lands in a launchd log | **FIXED.** 0 card commands from three nightly fires; doctor prints the hard-failure line under doctor's own `set -uo pipefail`; cut at 400 characters it still names the command | `raw/N6_flag_lock_seats.out` N6a |
| 7 | Type change fails forever | **FIXED.** Folder to file and file to folder: GOOD, next nights GOOD, 0 lost | `raw/r1_A_destruction.out` A5, A6; `raw/N1_good_truth.out` N2c |
| 8 | Lock clearable beside an orphan engine | **FIXED for the lock.** After SIGKILL: clear refused (exit 6), second run refused, nightly skips; clear works once the engine ended. The orphan still finishes its copy, as the seat states | `raw/N6_flag_lock_seats.out` N7a |
| 9 | Damaged state stops backup and flag | **PARTLY.** Garbage, empty, truncated: plain line, moved aside, next run works. Valid JSON with fields missing is still a traceback; the damage notice can be consumed by the nightly job: new findings 6 and 13 | `raw/r1_C_lock_catchup_watch.out` C4e, `raw/N3_index_shrink_conf.out` N5f, `raw/N6_flag_lock_seats.out` N6b |
| 10 | Suite green with guards removed | **PARTLY.** All 63 of the seat's mutants caught in my rerun, his 18 among them. Of my 24 new mutants 15 survive: new finding 9 | `raw/seat_mutants_rerun.txt`, `raw/K_my_mutants.out` |
| 11 | Install order walks past the hold | **FIXED.** Template first, lines first, both: a valid plist or none, and the script launchd calls exits 3 under the hold | `raw/N8_proposals.out` E1 to E3 |
| 12 | Minors | **FIXED**: loser told "another run holds the lock" 8 of 8; reused pid is stale; PORTABILITY says NN; wall-time window right on both change days. HELD once a day and `._*` files only rest on the seat's T9 and T13 in my suite run | `raw/r1_C_lock_catchup_watch.out` C1, C2; `raw/N8_proposals.out` E4, E6 |
| 13 | Notes | **FIXED per the seat's evidence**, which I read and did not repeat: 15 "listed on the NAS (read-only)" lines, before and after listings identical. Case-only rename unchanged, stated | lane `evidence/round2/` |

| Ruling (ANSWER-2) | State |
|---|---|
| 1 proof by sha256, exit 23, named, Q02 red | PARTLY: all built; the "gone" departure is new finding 1 |
| 2 secrets by shape, hard links, counts, real list 0 | PARTLY: built; my own scan also finds 0 of the tool's own shapes; conventional names outside the list travel (finding 2) |
| 3 forbidden roots, tokens reported, Secuura mapping, seats removed | FIXED as ruled; ancestor route is finding 3 |
| 4 END marker, exclude_path must exist, zero or sharp fall fails, `*` refused | PARTLY: finding 4 |
| 5 and 9 `first_attempt_at` once; damaged state moved aside, exit 3 | FIXED, with findings 6, 10, 13 |
| 6 the card reaches a seat; no launcher variable | FIXED |
| 7 type change, process group, install as one change | FIXED |
| 8 the 14 survivors caught; 15 new mutants | FIXED as ruled; finding 9 |
| 9 minors | FIXED |
| 10 real dry run lists the real destination | FIXED per evidence |

## NEW FINDINGS

### 1. HARD (GOOD is truthful). Blocker. A source that cannot be read is counted "gone" and the run says GOOD
- Reproduce: `scripts/N1_good_truth.sh` (N1a, N1b, N1c), `scripts/N1x_whole_source_unreadable.sh` → `raw/N1_good_truth.out`, `raw/N1x_whole_source_unreadable.out`.
- Expected: a file in scope that is not at the destination with the source's content fails the run.
- Actual:
  - N1a, a file with mode 000 from the first night: GOOD on 3 of 3 nights, the file never at the destination, "gone from the source during the run: 1" each night. Control (same file readable): arrives.
  - N1b, a backed-up file that changes and then cannot be read: GOOD on 2 of 2 nights; destination still `LEDGER-v1`, source `LEDGER-v2-newer-content`.
  - N1c, a folder of 51 files that becomes unreadable between the listing and the copy: GOOD, 0 of 51 at the destination, state `good`.
  - N1x, the coordinator's question. Every folder under the set's root unreadable mid-run: 42 of 42 "gone", GOOD, 0 files at the destination. The same on a later night with 40 files changed: GOOD, all 40 destination copies still hold last night's content, and GOOD again the following night. Only when the ROOT itself cannot be entered does the run fail, because the engine then exits 3 (not 23).
- Why: `prove_arrival` returns `vanished` for ANY `OSError` on the source (`nb_core.py` lines 1058 to 1066), and vanished files are removed from scope (line 1393). Permission denied, an I/O error and a macOS privacy refusal all look like "deleted".
- Real scope today, measured: 0 of 1,012,087 listed files are unreadable by this user (`raw/S_scan_real_lists.out`; control: a mode-000 scratch file reads False). So nothing triggers it today by file mode. It was not measured under launchd, where the privacy consent the seat expects for `python3` is exactly this kind of refusal.
- Smallest fix: only "no such file" (ENOENT or ENOTDIR) is `vanished`, and only if the set's root is still the folder that was listed; every other error is `differs` and fails the run. Add tests: one unreadable file, one unreadable folder.

### 2. NAME-SHAPE. Blocker under rule B (i) and (ii). Conventional credential names travel, and two are in today's real travel list
- Reproduce: `scripts/N11_first_copy.sh` section N12, `scripts/S_scan_real_lists.py`, the probe in `raw/S_conventional_hits_probe.out`.
- Travels today (my own scan of the seat's 1,109,007 real dry-run paths, names only; unit controls 22 of 22; positive controls 52,189, 5,422 and 7,060):
  - `Secuura/Extranet/api/local.settings.json` (283 bytes): the Azure Functions local-secrets file; git-ignored in its repo (`**/local.settings.json`); 1 setting whose name contains KEY, SECRET, PASSWORD or TOKEN with a value of 8 or more characters.
  - `Secuura/Blockchain/2_Project_Files/systemTest/playwright/.auth/token.json` (786 bytes, dated 2 September): Playwright's stored-login folder; git-ignored (`.auth/`); 1 JWT-shaped string. I counted patterns and printed no value; whether the token is still live I do not know.
  - Count: **2 files.** Every shape the tool itself lists: 0, by my scan and by the seat's.
- Conventional names (see the table below): of the coordinator's own examples, `service-account*.json`, `.htpasswd`, `terraform.tfvars` and `.docker/config.json` travel on a fake.
- It does not fail open on damaged input: the rule is code, not data.
- Smallest fix: add to the list `local.settings.json`, a `.auth` component, `service-account*` and `serviceaccount*` `.json`, `application_default_credentials.json`, `.htpasswd`, `*.tfvars`, `.docker`, `.dockercfg`, `.vault-token`, `kubeconfig`, a bare `credentials`, `.p8`, `.der`; then re-run the dry run and both scans.

### 3. HARD (root isolation). Blocker under rule A; needs a conf line that names a parent. An ancestor `set=` carries the other seats' trees
- Reproduce: `scripts/N6_flag_lock_seats.sh` section N9c → `raw/N6_flag_lock_seats.out`.
- `set=General|DRIVE|<the folder that holds WEDNESDAY, TUESDAY, FRIDAY>`: exit 0, GOOD; TUESDAY's two marked files and FRIDAY's one are on the fake NAS under `General/Wednesday/`. The Datasec folder under the same root is kept out (0 copies), because that name is excluded in every set. Control: an ordinary folder under the same root arrives.
- Why: the forbid check reads the components of the source path itself; `tuesday` and `friday` are excluded by name only when the set IS the seat's tree. The real drive has `/Volumes/DevMASTER/TUESDAY` beside the vault and `Setup and System`, which Kam's ruling gives to this seat, so a later "add the rest of the drive" line is a plausible edit.
- Smallest fix: refuse a `set=` whose real path is an ancestor of the seat's own tree or of any `set=` already given; or apply the other-seat names at the first two levels of every set.

### 4. HARD (conf fails closed). Blocker under rule A; needs no earlier good run. A set with folders and zero files is GOOD
- Reproduce: `scripts/N3_index_shrink_conf.sh` N4c, N4d → `raw/N3_index_shrink_conf.out`.
- First run of a set holding two folders and 0 files: exit 0, GOOD, no EMPTY SCOPE line. Control (no folders either): exit 8.
- `exclude_name=*.*` on a first run: GOOD on 0 files. `?*` and `**` are refused; `[!~]*` and `*[a-z0-9]*` empty the set and fail only because no folder is left.
- A damaged state file the same night as a mistyped exclusion (20 of 22 files gone): GOOD, because the baseline went into quarantine with the state.
- Why: line 948 fails zero files only when there are also zero folders; the fall rule needs a last good count.
- Smallest fix: zero files in a set always fails; after a state reset the first run needs `--accept-shrink` or prints that it has no baseline.

### 5. HARD (GOOD is truthful). Blocker under rule A; needs the destination altered behind the tool. A mismatch the sample found is not repaired, and later nights say GOOD
- Reproduce: `scripts/N11_first_copy.sh` N3e, `scripts/N3_index_shrink_conf.sh` N3d → their `raw/` files.
- One destination file altered (same size) in a 12-file set: nights 1 and 2 FAILED naming it; **night 3 GOOD with the destination still wrong**; nights 4 to 8 FAILED. "to copy: 0 files" on all 8 nights. With all 30 files altered: FAILED 6 nights running, 30 still wrong.
- Why: a failed sample removes the file from tonight's proven set but leaves its row in the index, so it is never re-sent and is trusted again whenever the sample misses it. README says "It is not indexed, so the next night sends it again"; that is true only for files that were sent.
- Smallest fix: on a sample mismatch delete the index row (the next plan then compares by content and re-sends, keeping the wrong copy under `versions/`).

### 6. HARD (the flag). Major. A damaged state file found first by the nightly job delays the flag by three days and its notice reaches nobody
- Reproduce: `scripts/N6_flag_lock_seats.sh` N6a, N6b.
- Control: last good day 0, NAS away: doctor fails hard on day 3. Same, with the state damaged on day 2 and the nightly job the next reader: the three DAMAGED lines go to the job's own output; doctor says nothing on day 3 and nothing on day 5; the hard failure comes on day 6.
- Ruling 5 accepted the restart of the clock. What it did not accept is the flag-worthy exit being spent on a caller no seat reads.
- Smallest fix: keep `damage` in the new state as "not yet shown to a seat"; doctor's block fails hard on it until a seat acknowledges; the nightly call never clears it.

### 7. HARD (state fails closed, but unreadably). Major. A damaged index stops every run with a traceback and leaves the lock
- Reproduce: N3c. `sqlite3.DatabaseError: file is not a database`, exit 1, lock left behind, state untouched. The next run says STALE lock; clearing it leads to the same crash. The watch says ok until 72 hours pass. A dry run survives it.
- The code calls the index "rebuildable: losing it costs one night". A damaged one costs every night until a person moves it.
- Smallest fix: open the index inside the `try`; on a database error move it into `state/_quarantine_<date>/`, say so in one line, start an empty one.

### 8. Major (resumability; matters most for the first copy). Proof work is saved only at the end of a pass
- Reproduce: N11a, N11b, N11c.
- SIGTERM mid-copy: 358 files delivered, 0 index rows; the resume re-read all of them, then finished GOOD. Stopped by the cap: what was delivered is proven and indexed (332 index rows; 331 of the 1,500 planted files delivered), and the resume carries on. Safe both ways: state never said good.
- N11c, on a patched copy (the 900-second margin made 2 seconds, each hash slowed 20 ms, to fit the case in seconds): the watchdog fired inside the proof loop, 0 rows saved; the next two runs spent their whole allowance re-reading what was already delivered and started 0 engine passes. That is a loop with no exit. In the real tool it needs the re-read of an interrupted set to outlast cap plus 900 seconds; with a 587,130-file set and a 5-hour cap I could not measure whether it does.
- Smallest fix: write index rows every few thousand files in the proof loop and in the plan's hash loop; let both loops stop at the deadline instead of relying on the alarm.

### 9. Major (evidence). One claim in STATUS is wider than the tests, and 15 of my 24 mutants survive
- STATUS finding 2 says T13 holds "the checker's 12 case variants and 24 unlisted shapes". T13 plants 35 files; 8 of his 24 are not among them and still travel when his own B4 is run on round 2: `env.backup`, `.docker/config.json`, `token.json`, `azureProfile.json`, `Agent Mail.md`, `cert.crt`, `.htpasswd`, `application_default_credentials.json`. ANSWER-2's list did not name these, so the build followed the ruling; the sentence in STATUS does not.
- The seat's reason for not running his scripts is true: `lib.sh` hard-codes his scratch folder and writes a conf with no END marker. Three edits made them run (`raw/r1_adaptation.diff`).
- My mutants (`raw/K_my_mutants.out`): 25 written, 24 applied, **9 caught, 15 survived**. Survivors that are untested guards on a hard guarantee: K10 the nightly job passes `--accept-shrink` itself; K19 an unreadable DESTINATION counts as proven; K06 the engine accepts a tree of any name; K18 an engine is recognised only by its recorded group; K14 a folder missing at the destination is ignored; K16 a dry run opens the index for writing; K17 the watchdog is never armed (stated by the seat); K12 the test-mode fence on `nas_root`; K25 the fire record. Survivors that are equivalent or backstops in today's code: K02, K03, K05, K21, K22, K23.
- Everything outside test mode (`nas_root` fixed at the real path, the real mount table, `statvfs`) is run by no test. By design; it means the first real run is its first test.

### 10. Minor (flag). Refusals under the HOLD start the three-day clock
- N6d, with a copy of the real state file (first attempt 2026-11-27 14:46, refused by the hold): lifting the hold on 1 December gives OVERDUE at once, and doctor fails hard during a running first copy ("90.3 h since the first attempt"). There is no command that resets the clock.
- Smallest fix: a refusal with the held exit code does not set `first_attempt_at`; or lifting the hold restarts it.

### 11. Minor (lock). SIGHUP is not handled
- N7b: SIGTERM ends cleanly (engine stopped, lock released, state failed). SIGHUP kills the tool, leaves 1 engine process running, the lock in place and the state `running`. Closing the terminal of a hand-run first copy does this.

### 12. Minor (GOOD and the mount). The NAS is checked in the mount table once, before the first set
- N10: the fake mount table lost its NAS line during set 1; both sets were processed and the run said GOOD. On a fake the folder stays, so nothing was misplaced; on the real share an unmount removes the path and the engine fails (his C5 still holds: 0 files written into a local folder). Fix: re-check before each set and before GOOD.

### 13. Minor (state). Valid JSON that is not a valid state
- N5f: `last_good` without `time` → `KeyError` traceback from the nightly job and the watch (exit 1). N5e: a `last_good` time in the future (one run under a wrong clock) → the nightly job skips every night and the watch says ok with negative hours.

### 14. Minor (conf). Duplicate keys, and what the END marker does not do
- N5b: `status=unconfirmed` then `status=confirmed` runs, with no warning. N5a: replacing an `exclude_path` line by any other valid line keeps the count, so the excluded bulk travels and the run is GOOD. The marker catches lost lines, which is what ruling 4 asked for; it does not seal content. A checksum line would.

### 15. Minor (doctor block and lock)
- N6c: when doctor is the first reader of a damaged state it prints "NO GOOD NAS BACKUP FOR 3 DAYS ... RUN --card"; `--card` then says ok. The text should say the state file was damaged.
- N7c: a dead holder whose recorded engine group id now belongs to an unrelated process blocks `--clear-stale-lock` until that process ends. Fails closed; record the engine's start time as is done for the pid.

### Notes (limits to state, not defects to chase)
- **The nightly sample.** 40 unsent files per set per night is at most 600 of 1,012,092 files (0.059%). One altered destination file in the Secuura set (587,130 files) is expected to be noticed after 14,678 nights (median 10,174); in the seat tree after 6,630; in the Secuura test material after 3,633 (`raw/sample_detection_arithmetic.out`). On my fake, 12 of 12 nights were GOOD with one file altered among 402. A destination file DELETED behind the tool is noticed the next night and re-sent (N3a). My view: acceptable only as a stated limit; README should carry the numbers, and a monthly full read-back would turn it into a real check.
- **Slow shrink.** 1,000 files to 3 in 10 nights at 45% a night, every night GOOD (N4b). The fall rule compares with the last good night only.
- **Growth.** 5,000 files appearing in the seat tree overnight are copied without a line (N4e). Only `max_files` bounds a set.
- **`--accept-shrink`** cannot be given by the nightly script or the plist (0 occurrences in each), and it is not sticky (N4a).
- **Versions.** Nothing is pruned and no run prints the total size of `versions/`. A re-send goes to its own `_passN` folder and last night's copy is kept (N2a: 3 copies, the night-0 one among them). The stop is the 200 GiB free-space floor, which refuses the run and so reaches the three-day flag: late, not silent.
- **A wrong-but-existing `exclude_path`** is accepted (N5c). The tool cannot know intent.
- **A dry run with a damaged state file moves it aside**, although a dry run says it writes nothing to the state file.

## NAME-SHAPE TABLES

Name rules cannot be complete. The real protections are the forbidden roots, the secrets folders being excluded by a contained name in any case, the hard-link rule, and the NAS being private. The tables say what the rule does today.

**Travels today, real scope (1,109,007 paths, names only):** 2 files, both in finding 2. Other hits I read and judge not secrets by name: 68 `.crt`, `.cer` and similar (public trust anchors); 6 `auth.json` (5 large evidence files with 0 JWT-shaped strings, 1 Redis command file); 150 names containing `credentials` (test evidence and source files); 92 `secrets.ts` or `.py` (source code); 20 names containing "private key" (documents); `vc_signing_key.out` (39 bytes, 0 pattern hits). Broad heuristics (names containing secret, password, credential, api key, token: 6,610 hits, 923 distinct names) were read by their most common names only; I did not review every name.

**Conventional credential names on a fake (N12, 40 names, neighbour arrived):**

| Kept out (17) | Travels (23) |
|---|---|
| `.netrc`, `.pgpass`, `credentials.json`, `.aws/credentials`, `.kube/config`, `*.keystore`, `*.jks`, `secrets.yml`, `.npmrc`, `.git-credentials`, `id_ed25519`, `*.skey`, `*.kdbx`, `terraform.tfstate`, `.env.production`, `client_secret*.json`, `.pypirc` | `service-account.json`, `service-account-prod-1234.json`, `serviceAccountKey.json`, `application_default_credentials.json`, `.htpasswd`, `htpasswd`, `terraform.tfvars`, `prod.auto.tfvars`, `.docker/config.json`, `.dockercfg`, `api/local.settings.json`, `playwright/.auth/token.json`, `auth.json`, `.vault-token`, `kubeconfig`, `.boto`, `secrets.toml`, a bare `credentials`, `AuthKey_*.p8`, `key.der`, `private_key.txt`, `mnemonic.txt`, `wallet/seed-phrase.txt` |

No wallet mnemonic or seed file name appears in the real lists (1 hit, a test result named `T6-no-MNEMONIC.json`).

**Exotic shapes that get through (notes only):** `env.backup`; `azureProfile.json`; `Agent Mail.md`; `cert.crt`; `Data sec` with a space; `DS-NexusAI`; a folder named `tuesday` inside a project set (by design: those words are library files there).

**Over-exclusion in the real scope (my own read-only walk; totals equal the seat's: 2,326):**

| Shape | Entries | What they are |
|---|---|---|
| env-file | 2,128 | 1,796 templates (`.env.example` 1,558, `docker.env.example` 84, `.env.local.example` 63, `.env.sample` 31); `pins.env` 110; `.envrc` 63; real `.env` 15 or 16; small test files |
| credential-file | 130 | `.npmrc` 128; `secrets.yml` 2 |
| key-or-certificate | 54 | 29 files named `predict.index.<n>.key.<hash>` (not keys); 10 `.pfx` and 5 `.key` test identities; `cacert.pem` 2; `master.key`; **1 folder, `diagrams.key`, a Keynote document** |
| credentials-folder-name | 14 | 12 real secrets folders; 2 are this lane's own evidence files (`05_move_4_Credentials.txt`, `06_move_3_Access_Keys.txt`) |

495 of the 2,326 sit under dated session-history folders. No project loses a config directory. A restore is not materially broken by this: `.git` is excluded too, so working trees come back from their remotes, and what the backup uniquely holds is the untracked material. One item is a real document left out: the Keynote file. Minor.

## FIRST FULL COPY: what governs it, and the sequence I would use (after a GO, not before)

What governs such a run, from the code and from N11:
- **The cap** is `--max-seconds` (the conf's default is 18,000 s). It stops the ENGINE. The proof loop has no deadline of its own; a watchdog stops the whole run 900 s after the cap. A run stopped by the cap in the middle of a big set loses that set's proof work if the read-back takes more than 900 s (finding 8). So the cap must be far above the estimate, not near it.
- **Order and size:** 15 sets one after another. Copy time alone at the conf's 8.9 files a second: 31.6 h; Secuura 18.3 h, the seat tree 8.3 h, Secuura's test material 4.5 h. The read-back of every sent file is on top and is not measured.
- **Resumable:** yes. A finished pass indexes what it proved; an interrupted pass leaves files at the destination that the next run re-reads once and does not re-send (N11a: 359 re-read, 1,143 sent). An interrupted first copy cannot leave the state saying good (N11a, N11b: `last_good` None, 0 COMPLETE markers).
- **Outside the window** needs `--out-of-sequence <card id>` (six characters or more) and the hold moved aside. The hold is honoured with every flag (5 of 5 held runs exit 3).
- **What the watch says meanwhile:** "lock: pid N RUNNING". If the run is still going after 2026-11-30 14:46 it also says OVERDUE and doctor would fail hard (finding 10); that is the old clock, not a fault in the copy.
- **A live tree:** a file written during every pass is never proven, so a 32-hour daytime run may well end FAILED (exit 8) naming a few files. That is the tool being honest. The re-run is short.

Sequence, for Wednesday:
1. Fixes in and a GO. Then `bash nas_backup.sh --dry` (7 minutes), no PROBLEM line, totals near 1,012,092 files; run the seat's scan and `scripts/S_scan_real_lists.py` on its stamp: tier A and B both 0.
2. Confirm nothing else holds the NAS for two days: `naspush` fires at 03:30 on this Mac with a 4-hour cap and re-sends about 128,000 files a night. Whether to hold it for these nights is Kam's.
3. `mv -n HOLD_wednesday HOLD_wednesday.lifted-<date>`. Do not install the job.
4. In a tmux window that will stay open, with the Mac kept awake:
   `caffeinate -i bash 2_Project_Files/nas-backup/nas_backup.sh --run --out-of-sequence <id of Kam's 13:35 approval card> --max-seconds 432000 > <a log file outside the lane's tree> 2>&1`
   Five days of allowance; no `tee` (it hides the exit code); no `--accept-shrink`.
5. First 15 minutes: watch the Mac's screen for a privacy dialog for `rsync` or `python3` and answer Allow. Unanswered, the run ends STALLED (exit 7) after 900 s.
6. While it runs: the set being copied is the newest `logs/wednesday/<stamp>_run_<set>.rsync.log`, and its line count is the files delivered; `bash nas_backup_watch.sh` shows the lock RUNNING. Never `--clear-stale-lock` while an rsync of this seat is alive (the tool refuses anyway).
7. When it ends: exit 0 and the GOOD line, or the same command again. Exit 8 with a short NOT DELIVERED list is a live file: re-run, in the window if possible. Exit 4, 5 or 7: read the reason, re-run; it resumes.
8. After GOOD, read-only: one `RUN_<stamp>_COMPLETE.txt` in each of `General/Wednesday` and `Secuura/Wednesday`; the manifest's totals against the dry run's; a `find` for secret-shaped names on the share with a positive control. Then move the HOLD file back until the arming change is applied.

## THE DOCTOR LINE: fail or warn

It cannot strand a rotation. `Launch_Wednesday.command` lines 404 to 412: when `SEAT_ROTATION` is set, a non-zero doctor exit is logged, the `✗` lines are put into `PREFLIGHT_HARD`, and the exit code is set to 0; lines 905 to 914 append them to the boot prompt. Every unattended caller goes through `wednesday_rotate.sh` line 72, which sets `SEAT_ROTATION`. Without it (a person at the keyboard) the launcher asks "Continue anyway? Type yes". So the block as proposed only pauses a human launch. The patched copy of the real doctor.sh passes `bash -n`, and of the 19 names the block and its two sourced files define, 18 are used nowhere else in doctor.sh and `seat_resolve` appears once, in a comment (`raw/N8_proposals.out` E5). My view: keep `fail`; it is the only path into a rotation's prompt and Kam asked to be flagged. Fix findings 10 and 15 first, or the first copy itself will raise it.

## WHAT HELD

- **No content lost:** 8 of 8 oracle checks read 0 lost (changed, shrunk, same size, removed at source, both type changes, file to symlink, case-only rename, NFC to NFD, tool-named folders, unwritable `versions/`); the oracle's own control fires.
- **His false-GOOD triggers:** 0 GOOD in 17 failing nights; a destination altered between copy and proof fails (N2b); a file appended after every pass fails and is named after 3 passes (N2a); a file swapped for a symlink into a secrets folder fails with 0 copies of the secret on the NAS (N2d); 2.2 GiB file copied and proven in 10 s.
- **Secrets:** 12 of 12 listed, 12 of 12 case variants, symlink and hard link into a secrets folder kept out.
- **Conf:** 9 of 9 damaged or mistyped confs refused; a line after END refused; an exclude that names nothing refused.
- **Seats:** 36 of 36 command runs from TUESDAY and FRIDAY trees exit 2, 0 files written, 0 state files; 10 of 10 other routes refused (disagreeing `WED_AGENT`, a symlink named WEDNESDAY, the engine called directly five ways, a mixed-case tree, a WEDNESDAY folder inside TUESDAY).
- **Lock:** 8 of 8 simultaneous starts have one winner and the right message; owner-less lock fresh and old; reused pid.
- **Hold:** nightly exits 3; `--run` with `--out-of-sequence` at four times and with `--accept-shrink` exits 3; nothing started.
- **Schedule:** 24 fires at minute 30; first fires that can start a backup are 00:30, 02:30 and 04:30 for the three windows, two hours apart; a wake at 07:10 is a logged skip and the night is caught up at the next window; a Mac asleep through every window never backs up and the three-day flag is what says so.
- **Install:** three orders, valid plist or none, idempotent, `--check` agrees, `naspush` still renders.
- **Evidence matches STATUS:** suite 319 passed, 0 failed (my run); mutants 63 of 63 (my rerun); 1,012,092 files, 68.05 GiB, 7,343 excluded, secret-shape counts 2,128, 130, 54, 14 (my walk gives the same four), 9 hard links, 14 case clashes, 0 PROBLEM lines, NAS listings identical.
- **Not armed:** 0 `nasbackup` plists in `~/Library/LaunchAgents` and 0 templates in `scheduler/jobs` (control: 1 `naspush` in each); 3 HOLD files.

## NOT TESTED

- **Anything on the real NAS**, in any mode: I did not repeat the dry run. SMB renames, times, names the share rejects, speed, the read-back at scale.
- **launchd and launchctl:** no verb run. "Not armed" rests on file listings. The privacy-consent behaviour under launchd, which finding 1 may meet, is not tested.
- **The real code path outside test mode.**
- **The patched doctor.sh run whole**, and the launcher carrying the line into a real boot. Read and syntax-checked only.
- **Scale:** a million files, memory, the real watchdog, whether a re-read can outlast the cap (finding 8 uses a patched copy).
- **A case-sensitive source.** The scratch volume folds case; I made no disk image. Case collisions, and a hold file spelled in another case on the real drive, are untested.
- **His scripts A2, A3, D, E and G:** not run. A3 is replaced by my N7a, D by the seat's rerun of his 18, E by my N8; G names real mount paths and I left it out; A2 was his own flawed run.
- **Tuesday's daylight-saving window** (02:30 on the spring-forward day): the seat's T19 only.
- **The suite's own tests T12 to T20** were not read line by line; my mutants stand in for that.
- **File contents.** The two files in finding 2 were probed by pattern count only. A secret in an ordinary-named file is invisible to all of this.
- **Tuesday's and Friday's machines and scopes.**

## FOUND / TESTED / HOW

- **Instruments:** a scratch copy of the lane in a WEDNESDAY-named tree; fake source and NAS trees; stub engines; a stub `launchctl` with a scratch HOME; the first checker's oracle; marker strings; my own name scan and read-only walk of the real source sets; one patched engine copy (N11c only, stated there).
- **Positive controls:** the unmutated suite passes before any mutant; the oracle reports a removed file; an ordinary neighbour arrives beside every exclusion test; `os.access` returns False on a mode-000 file; 22 of 22 synthetic secret names match their patterns and none fires on an ordinary source path; the pattern probe finds its planted strings; the before-and-after diff reports a planted change.
- **Negative controls:** readable twin beside N1a; no-folder twin beside N4c; intact conf beside N5a; undamaged state beside N6b; SIGTERM beside SIGHUP.
- **What I adapted in his scripts** (`scripts/r1_adapted/`, diff in `raw/r1_adaptation.diff`): the scratch path and lane path in `lib.sh`; `write_conf` appends the `END lines=<N>` marker; the same in `sconf` of `B7b`. Nothing else.
- **My own instrument errors, outputs kept:**
  1. N2e first used `/usr/bin/mkfile`, which this Mac lacks; that block in `raw/N1_good_truth.out` is void and is redone in `raw/N11_first_copy.out`.
  2. N7c's last line ("after that process ended: clear rc=6") is void: the "unrelated" group was my own script's group, still alive.
  3. N1x part 3, night 2, is labelled "the stub now a no-op". It is not: the stub made the folders unreadable again. The line shows a second faulty night, not a recovery.
  4. K13 was not applied (wrong indentation in my target), so 24 mutants, not 25.
  5. In his adapted `C_lock_catchup_watch.sh`, C4b, C4d and the watch half of C4e call `--flag` or `--reprint`, which round 2 removed, and the daylight-saving snippet crashes on the new function signature. Those lines are void; N6 and N8 replace them.
  6. The N9a table was folded by `uniq`: 18 rows of 2 are the 36 runs.
  7. In N4a the "2 SCOPE FELL" count is one event printed twice by the tool.

## DID THE CHECKER MODIFY ANYTHING

`raw/Z_nothing_modified.out`.
- Lane: sha256 of all 101 files outside `logs/` identical before and after. The stat listing of all 210 entries differs in one file and its folder: `ANSWER-3.md`, written by the coordinator at 15:29:10 during this check. Its content hash is the same in both of my lists; I wrote nothing in the lane.
- First checker's folder: 41 files, sha256 identical.
- The three NAS mounts: `df` line and top-level name, size and time of every entry, 59 lines, identical. No script of mine names a path under them.
- No launchctl verb, no git write, no network.
