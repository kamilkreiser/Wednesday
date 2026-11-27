VERDICT: NO GO

Round 3 closes every hole round 2 was failed for: all of the second checker's attacks that I re-ran end with 0 GOOD on an attack night, the suite is 568 passed and 0 failed in my own run, and the chunked engine lost nothing in any test I made. It is still NO GO, because the SEVERITY RULING makes a hard guarantee a Blocker on any input I can construct, and I constructed three. (1) Two sets of one client whose destination names nest (`X` and `X/sub`) overwrite each other's files and every night says GOOD while a planned file is not at the destination with its source's content. (2) A symlink planted in the destination chain on the share (three places tried: `General/Wednesday`, `current/<set>`, `versions`) makes the tool write outside this seat's destination folder; in my test it wrote 14 entries into another client's folder and said GOOD. (3) A planned file that is replaced, after the plan, by a hard link to a file inside `4_Credentials` travels, is proven and the night is GOOD. **None of the three is triggered by today's real conf or by anything I could see of the real share**: the real conf has 0 nested pairs within one client (measured), and the destination below `General/Wednesday` does not exist yet. Each fix is a few lines. Whether a NO GO that rests on constructed inputs ends the lane, or buys one narrow fix-and-recheck of about fifteen lines, is Kam's; my job is the ruling as written, and under it this is NO GO. One Major beside them: ANSWER-5's own condition is not met (what the secret-shape rule leaves out is recorded as counts only, never by name).

Checker: fresh third check, 2026-11-27 19:41 to 21:08 AEDT. Everything below is from this session, on a scratch COPY of the lane under `/private/tmp/qa3nb` against fake trees, plus read-only reads of the lane and of the saved real dry list. The lane's tools were never pointed at a NAS path by me. Scripts: `scripts/`. Raw output: `raw/`. The machine was loaded by other seats and by my own mutant runs throughout (load averages 4 to 28); every timing below has its `uptime` beside it in the raw file.

## THE NINE ITEMS

| # | Item (ANSWER-4) | State | Evidence |
|---|---|---|---|
| 1 | Unreadable is NOT DELIVERED; the deletion proof | **FIXED.** The second checker's N1a, N1b, N1c, N1x re-run from copies: 0 GOOD on 10 attack nights, every control GOOD. FIFO, symlink and a name that reappears between the two listings: NOT DELIVERED. The accounting is one subtraction; I found no other route out of the plan in the code. Two edges where a file that still exists is counted deleted: finding 6. Naming is capped: finding 7 | `raw/R2_N1_good_truth.txt`, `raw/R2_N1x_whole_source_unreadable.txt`, `raw/A3_deleted_proof.txt` |
| 2 | Zero-file plans, `allow_empty`, the fall rule's double baseline | **FIXED.** 9 emptying patterns: 4 refused, 4 fail on the zero rule (exit 8), 1 ordinary and GOOD. First run with folders and no files: exit 8. Damaged state plus a mistyped exclusion: fails. A file in set 2 made while set 1 copies is in set 2's plan and arrives. One leak when two clients' sets share a name: finding 5 | `raw/A8_items_2_3_4.txt`, `raw/R2_N3_index_shrink_conf.txt`, `raw/A1_dest_overlap.txt` |
| 3 | Sample finding: repaired in the run or the night fails; full read-back | **FIXED.** N3d re-run: night 1 GOOD with 0 of 30 altered copies left. Cap passing during the read-back: exit 4, the set's earlier proofs already withdrawn (1 index row left of 62), next night re-sends all 61 and is GOOD. kill -9 during the read-back: the rows were already gone (1 left of 62), next night repairs all. A destination copy missing or of another size is re-sent without a read-back: note 13 | `raw/R2_N3_index_shrink_conf.txt`, `raw/A8_items_2_3_4.txt` |
| 4 | `set=` containment in both directions; `forbidden_roots` | **FIXED for sources.** 4 of 4 spellings of a client folder three levels down refused; an ancestor of a root found at level 1 or 2 refused (the suite's T24, green in my run). An ancestor of a seat-named folder at level 3 is accepted: Datasec mark 0, exact `Friday` folder 0, `tuesday-seat` travels (the seat states this limit; note 15). **Destinations are not checked for containment at all: finding 1** | `raw/A8_items_2_3_4.txt`, `raw/A1_dest_overlap.txt` |
| 5 | Damage: state, index, the notice, the lock | **PARTLY.** Nightly, watch and a real run each leave a notice (1 line) and the watch then exits 5; a dry run moves nothing and writes no notice; the lock was released on every path I forced, including a signal after the accounting. Not fixed: three tracebacks (findings 8 and 9), and a healthy but locked index is quarantined as damaged (finding 11) | `raw/A5_damage_lock_signals.txt` |
| 6 | The chunked engine | **FIXED on the fake NAS; never run on a real one.** 18 odd names (newline, leading dash, `--delete`, `*`, trailing space, backslash, control characters) in chunks of 4: GOOD, 21 of 21 files identical. Option words over every engine call the tool built: `--backup --backup-dir --files-from --from0 --no-h --stats --temp-dir --timeout -I -O -t`, none deleting; the code builds exactly two argument lists and checks both. Two runs in one night and three passes on one file: 4 distinct contents of the file in 4 `versions/` files, nothing overwritten. SIGKILL in chunk 3 of 5: 10 index rows kept, state `running`, lock left, a second run refused while the orphan engine lived; the resume compared the orphan's 5 files by content, found the 1 I had altered and repaired it. `good` is written in one place (one `note_attempt("good"...)` call) | `raw/A4_dest_escape_and_chunks.txt`, `raw/A9_chunk_overhead.txt` |
| 7 | Secrets and the name rule | **Folder rule: holds for case and decoration** (12 of 12 spellings that contain either name in any case kept out). Look-alikes travel (note 14). **Hard-link rule: holds at plan time, fails to a swap after the plan (finding 3).** Name list, best effort: lane's scan 0, second checker's scan tier A 0 and tier B 0, my own 0, all on the saved real dry list of 1,109,051 paths with controls 52,213, 5,422, 7,060. **ANSWER-5's condition not met: finding 4** | `raw/A7_secrets.txt`, `raw/S1_*.txt`, `raw/S2_*.txt`, `raw/S3_my_scan.txt` |
| 8 | The Minors of round 2 | 10 hold and the clock: **PARTLY** (finding 10). 11 SIGHUP: **FIXED** in the run; a window at the very end remains for any signal (finding 8). 12 mount per set, per chunk, before GOOD: **FIXED** (share leaves during chunk 2 of 4: stopped before chunk 3, exit 2, 8 index rows kept). 13 invalid state, future time: **FIXED**. 14 duplicate keys: **FIXED**; END seal left and stated. 15 doctor text and reused group id: **FIXED** (suite T25, T27 green in my run). Another share at the same path is accepted: finding 12 | `raw/A5_damage_lock_signals.txt`, `raw/01_suite_run.txt` |
| 9 | Evidence honesty | Suite: **568 passed, 0 failed** (my run, 1 min 48 s). Mutants: **126 of 126 caught, 0 survived or broken**, the whole set run by me (19:49 to 21:07, four at a time, load average 4 to 28), each by a FAIL line carrying the name the lane's list gives it. Claims program: 140 claims, 0 not supported, on the seat's outputs and on my own suite and mutant outputs (`raw/C5`). My own mutants: 18 written, 18 applied, **7 caught, 11 survived** (note 21). The seat's account of its first pass (118 of 126, the eight named) matches its evidence files line for line; the sha256 it recorded for `nb_core.py`, `run.sh` and `mutants.sh` are the files as they are now | `raw/01_suite_run.txt`, `raw/02_mutants_full.txt`, `raw/C1` to `raw/C4`, `raw/X_my_mutants.txt` |

## NEW FINDINGS

### 1. HARD (GOOD is truthful). Blocker under the ruling; needs a conf with two sets of ONE client whose destination names nest
- Reproduce: `scripts/A1_dest_overlap.sh` → `raw/A1_dest_overlap.txt`. Conf lines `set=General|WEDNESDAY|<seat tree>` and `set=General|WEDNESDAY/docs|<another folder>`; both sources hold a `readme.txt` (in the seat tree at `docs/readme.txt`).
- Expected: refused at load, like a nested SOURCE is. Or the night fails.
- Actual: exit 0, GOOD, COMPLETE marker, state `good`, on 3 of 3 nights. After each run `current/WEDNESDAY/docs/readme.txt` holds the INNER set's content; the seat tree's file is not at the destination with its content (its copy is under `versions/<stamp>/`, so nothing was destroyed). Nights 2 and 3 each "to copy: 1 files ... 1 changed" for both sets: they overwrite each other every night and both proofs pass in turn. Control: the same two sets with the inner one named `Docs2`: GOOD and identical.
- Why: `load_conf` refuses equal destination names per client and nested SOURCES, never nested DESTINATIONS. The first set's proof is made before the second set writes over it.
- Real conf today: 0 such pairs in one client; 1 pair across two clients (`General|CODING/Testing Agent MAIN` and `Secuura|CODING/Testing Agent MAIN/projects/secuura`), which is harmless because the client folders differ (`raw/Z2_real_conf_overlap_check.txt`). Moving that Secuura set back under `General` would make the pair nest; there it happens to be saved by its `exclude_path`.
- Smallest fix: in `load_conf`, refuse when, within one client, one set's destination name is a path prefix of another's (compare the `/`-split parts, case-folded). Three lines and a test.

### 2. HARD (no write outside the seat's destination). Blocker under the ruling; needs a symlink in the destination chain on the share
- Reproduce: `scripts/A4_dest_escape_and_chunks.sh` A4a, A4b, A4d → `raw/A4_dest_escape_and_chunks.txt`.
- Expected: refused, nothing written.
- Actual:
  - A4b, `<NAS>/General/Wednesday` is a symlink to `<NAS>/Datasec/x`: exit 0, GOOD; 14 entries of this seat's backup now lie under the other client's folder (the count printed is 15 with the folder itself).
  - A4a, `current/WEDNESDAY` is a symlink to a folder outside the seat's folder: exit 0, GOOD; `a.txt` and `sub/` written beside the outsider's `keep.txt`.
  - A4d, `versions` is a symlink to outside: exit 0, GOOD; the replaced file's old copy was written outside.
  - Held: a symlinked SUBFOLDER inside a set (A4c) is replaced by a real folder by the engine, the outside folder is untouched and the symlink itself is kept under `versions/`.
- Why: `ensure_dest_chain` accepts a level when `os.path.isdir` says yes, which follows symlinks; `real_name_check` compares names only; the engine is handed the path with a trailing slash.
- Real share: per the seat's saved dry-run listing, `General/Wednesday` exists with 1 entry and nothing exists below it for this tool; `Secuura/Wednesday` does not exist. I did not list the share below its top level (not licensed), so whether `General/Wednesday` is a plain folder is unchecked by me: condition 3 below.
- Smallest fix: in `ensure_dest_chain`, refuse a level for which `os.path.islink` is true; before each set, require `os.path.realpath` of the set's destination, of `versions`, `manifests`, `runs` and `_tmp_incoming` to lie inside `realpath(<NAS>/<Client>/<Seat>/nightly-backup)`. About six lines and two tests.

### 3. HARD (hard-link rule). Blocker by the letter of the ruling; a race: needs a planned file swapped for a hard link between the plan and the copy
- Reproduce: `scripts/A7_secrets.sh` section b → `raw/A7_secrets.txt`. `files/later.txt` is an ordinary planned file; during the first engine call's start it is replaced by a hard link to `4_Credentials/token.txt`.
- Expected: not sent, or the night fails naming it.
- Actual: exit 0, GOOD; the secret's marked content is on the fake NAS at `current/WEDNESDAY/files/later.txt`, proven. In the same run the hard link that existed at plan time and both symlinks into the folder stayed out (control).
- Why: the link count is read once, in the walk. The plan-to-copy window is the length of a set (hours for the two big ones on a first copy).
- Not the same thing (a Note, inherent to a name rule): a planned FOLDER swapped for the secrets folder (section c) delivers the same-named file's content under the ordinary folder name; no folder named `4_Credentials` reaches the NAS.
- Smallest fix: in `prove_arrival`, `os.lstat(src).st_nlink > 1` is a verdict of its own that is never proven; the failure line must say that the content already reached the destination and name the path, because the tool never deletes there. That makes the night fail and the leak known; it does not prevent the write. Preventing it needs the check immediately before each chunk as well, which narrows the race to one chunk.

### 4. Major (ANSWER-5 item 1's condition). What the secret-shape rule leaves out is recorded as COUNTS ONLY
- Reproduce: `scripts/A7_secrets.sh` section d. Four ordinary files the wide rule excludes (`src/secrets.ts`, `certs/root-ca.crt`, `ev/post_api_credentials_ok.json`, `.env.example`) beside one that travels.
- Actual: each of the four names appears 0 times in the run's output, 0 times in the lane's logs, 0 in the lane's manifests, 0 in the NAS manifests. Control: the travelling `main.ts` is named in 4 log files, and a hard-link skip IS named in the manifest. The manifest holds `{'category': 'secret', 'pattern': 'credential-file', 'entries': 2}` and the like. README says it in words: "names are never printed there".
- So on the real scope the 2,697 entries the rule excludes (the seven shape counts of the seat's saved dry run, which I added up; the seat counts 373 real paths as newly left out, mostly not secrets) are invisible at restore time except as seven numbers. Wednesday's condition for keeping the wide rule is not met.
- Smallest fix: write the excluded-by-shape relative paths, one per line with the shape, to a file per set beside the symlink list in the lane's `manifests/` on the drive (the symlink list is already written exactly this way). Whether the same list should also go to the share is a decision: it puts the names of real secret files (`.env`, key files) where anyone who can read the share can read them. My view: drive only, and say so in README.
- Until then, the gap can be listed on demand by the second checker's walk (`evidence/round3/S_over_exclusion_adapted_one_line.py`), which the seat ran at 19:37.

### 5. Minor (zero rule, fall rule). Two sets of different clients may share a destination name; the baseline, `allow_empty` and the index are keyed by the name alone
- Reproduce: `scripts/A1_dest_overlap.sh` A2. `set=General|Proj|...` (12 files) and `set=Secuura|Proj|...` (1 file).
- Actual: the recorded baseline is `{'Proj': 1, ...}` (the last set wins), so the 12-file set fell to 2 and the night was GOOD with no SCOPE FELL line. `allow_empty=Proj`, meant for one, let the other go to 0 files: GOOD, "the conf allows it to be empty". The index rows of the two sets replace each other, which only costs a re-hash each night.
- Real conf: 0 shared names. Fix: refuse a destination name used under two clients, or key the three tables by `<client>/<name>`.

### 6. Minor (deletion proof). Two ways a file that still exists is counted DELETED AT SOURCE
- `scripts/A3_deleted_proof.sh` a, c, f.
- a. The parent folder is REPLACED by another folder of the same name (`mv sub sub.old; mkdir sub`): GOOD, "DELETED at the source during the run: 1", the file lives on at `sub.old/b.txt`. README says a folder removed during a run fails the night; a folder replaced does not, up to the limit. This is inside the brief's sentence (parent listable, name absent) and the file is named, so I call it Minor, not a breach.
- c. On a case-FOLDING source volume a file renamed to another case and made unreadable is counted deleted (GOOD) while its planned path still resolves. The unit shows the same for NFC against NFD. The real drive is Case-sensitive APFS (`diskutil`), where a case rename really removes the name, so this cannot happen there; it would on a seat whose drive folds case.
- Held: a FIFO or symlink under the same name, a name back before the second listing, the root swapped, the root gone.
- Fix: also require `not os.path.lexists(path)`; one line.

### 7. Minor (the deleted are named). The limits add up, and the naming is capped
- With the defaults a GOOD night may let 1,058 planned files go as deleted across the 15 real sets (587 in the Secuura set alone); at the conf's ceiling (100 files, 1%) 11,175. 101 and 0.02 are refused, 100 and 0.01 accepted (my mutant X02 removes that ceiling and the suite stays green).
- 650 deletions in one set (GOOD under the ceiling): 600 named in the last lines plus "... and 50 more, all in the manifest"; manifest 650; **state file 20**. STATUS says they are named in the state. Above 5,000 the manifest is cut too and its "all in the manifest" line would be false.

### 8. Minor (interruptions). A signal after the accounting gives a traceback and leaves the state `running`
- `scripts/A5_inject.py` (fault injection: a signal delivered while the manifest is written, and after the COMPLETE marker) → `raw/A5_damage_lock_signals.txt` section a. SIGTERM and SIGHUP alike: exit 130, 1 traceback, lock released, state `running` (README: "record the attempt as failed"). In the second position the run had printed GOOD and the COMPLETE marker is on the NAS while the state has no good backup; the watch says "ok ... last attempt running". All files were proven in both cases, so this is not a false GOOD. The next run is GOOD.
- Fix: catch `KeyboardInterrupt` in `cmd_backup` as well, or restore default handlers before the tail.

### 9. Minor (damage). Three callers give a traceback when the state folder cannot be written
- A damaged state file in a read-only `state/` folder: real run, watch and nightly each exit 1 with a `PermissionError` traceback. The doctor block maps exit 1 to a warning, so it is seen at a boot but not carried into a boot prompt.

### 10. Minor (round 2's minor 10, partly). A `--run` under the HOLD that is refused for another reason starts the clock
- Under the hold with `status=unconfirmed`: recorded as `refused`, `first_attempt_at` set. Hold lifted four days later: OVERDUE at the first check, and the line says "103.0 h since the hold was lifted", which is wrong twice. The conf is read before the hold is looked at. Fix: test the hold first.
- Held: 4 of 4 flag combinations and the nightly script exit 3 under the hold, 0 engine starts, the fake NAS unchanged.

### 11. Minor. A healthy index that is only LOCKED is moved aside as damaged
- Another process holding the index for 14 s: "INDEX DAMAGED ... (database is locked)", the good index quarantined, a damage notice written, the run GOOD after re-comparing everything. On the real data that re-comparison is a full read of the share. Fix: treat `database is locked` as a refusal, not as damage.

### 12. Minor. The mount check accepts any share mounted at the path
- A mount line naming `//.../SomeOtherShare` at the NAS path: GOOD. The tool looks for ` on <path> (smbfs`. The real line names `//DotORG@192.168.20.154/DEV-Working`; a conf key for the expected share name would close it.

### Notes (limits, or stated by the seat; nothing to chase before a first copy)
13. A destination copy that is MISSING or of ANOTHER SIZE while the index holds its proof is re-sent as "new" or "changed", with no line saying the destination had been altered and no read-back of the set: with the sample off, 10 same-size altered copies beside them stayed wrong on a GOOD night. The sample's odds are the stated limit; this is evidence the tool has in hand and does not use.
14. Folder-name look-alikes travel: 8 of 21 spellings (`4_Credentialſ` with a long s, fullwidth `４`, a zero-width space inside, dotless `ı`, Cyrillic `С`, `4-Credentials`, `4 Credentials`, `4_Creds`). README defines the rule as "its lower-cased name contains", and under that wording none of these is covered; the first one is equal to the real name under Unicode case folding, so `casefold()` after NFKC would be the better test. In the real dry list: 0 such components (my scan).
15. A set whose source is an ancestor of a seat-named folder three or more levels down is accepted and a folder such as `tuesday-seat` travels (STATUS says so). What then protects: `datasec` by contained name in every set, and folders named exactly `tuesday` or `friday`.
16. `allow_empty` also switches the fall rule off for its set: 9 files to 0 is GOOD. The conf comment says what the mark costs.
17. `claims_check.py` matches substrings. It called SUPPORTED a claim whose text was false in meaning (argument `T21`, or `GOOD`, or `(= 0)`), and refused the three controls. With one FAIL line planted in a copy of my suite output only the `total` claim caught it. The seat states this limit ("it does not judge whether a test is a good test").
18. `engine_passes` in the manifest stops at 400 entries per set; a first copy has about 5,100 engine calls. The per-set `.rsync.log` holds all of them.
19. The real dry list holds 6 names ending in a dot or a space. How the share stores them is untested; expect them among the first NOT DELIVERED names if it mangles them.
20. The read-back that proves a file is a read through the same SMB mount seconds after the write. Whether macOS serves it from its cache is not something a fake NAS can show.
21. **Minor (evidence). 11 of my 18 new mutants survive the suite** (`scripts/X_my_mutants.sh`, `raw/X_my_mutants.txt`; a mutant counted as caught on ANY failing line, which is looser than the lane's own rule). Each survivor is a guard of round 3 with no test that can fail:
    - on a hard guarantee: **X15** a run stays GOOD and records good when the manifest or the COMPLETE marker cannot be written on the NAS; **X09** the mount is not checked before GOOD; **X08** nor before each chunk (the suite's unmount test is answered by the per-set check alone; my A5e shows the per-chunk check does work); **X28** two sets may share one destination; **X01** the deletion is checked once, not twice; **X02** the conf ceiling on deletions is removed;
    - on the cap: **X04** the cap is ignored in the full read-back; **X37** and while comparing in the plan (my A8 3a shows the first works);
    - others: **X13** the roots beside the seat's tree are not searched (every fixture puts the tree at the top of its drive); **X34** the nightly job does not restart the clock when the hold is lifted; **X40** the deleted files are missing from the manifest.
    - Caught, 7: X03, X12, X18, X21, X26, X33, and X41 (by an exit code, not by a check that the old content is in `versions/`).
    - These are untested guards, not broken ones: in my own attacks the guarded behaviour was present wherever I exercised it.

## ANSWER-5: my judgement of the three answers

1. **Keep the wide rule: sound as a direction, but its stated condition fails (finding 4).** Erring toward leaving out costs completeness, not secrecy, and both scans read 0. The condition Wednesday attached is not met by the build: counts only, by design. Either the names file is added (drive only), or the rule is narrowed, or Kam is told plainly that 2,697 entries are left out and are listable only by a separate walk.
2. **Keep the strict sentence: agreed, with one correction to what it says.** It will fail honest nights on a live tree, and that is the right direction. But the code is not as strict as README's sentence: a folder REPLACED by another counts its files as deleted (finding 6a). Add the one-line `lexists` check or correct the sentence.
3. **Keep the `allow_empty` mark: agreed.** The set stays visible. Two things to know: the mark also switches off the fall rule for that set (note 16), and it is matched by name alone (finding 5), which is harmless in today's conf.

On the seat's departure "the plan is made per set": I agree with it. A file created in a later set before that set's plan is copied; a file deleted before its set's plan is simply not planned and not counted; nothing left a plan once made in any test.

## THE CHUNKED ENGINE: measured overhead and an estimate

Measured on the fake NAS (a local APFS folder, not SMB), 20,002 small files, one run each, machine loaded (`raw/A9_chunk_overhead.txt`):

| chunk_files | engine calls | wall time | load average then |
|---|---|---|---|
| 30,000 (one chunk) | 1 | 24.6 s | 8.1 |
| 200 (the default) | 101 | 36.3 s | 13.4 |
| 50 | 401 | 64.0 s | 13.0 |
| 30,000 again | 1 | 53.0 s | 19.6 |
| 200 again | 101 | 99.5 s | 15.1 |

Per extra engine call: 0.12 s and 0.10 s in the first three runs, 0.46 s in the second pair under heavier load. I have no quiet-machine figure; treat 0.1 to 0.5 s as the range on a local disk.

**Estimate, not a measurement:** 1,012,110 files at 200 a chunk is about 5,070 engine calls, plus at most 34 more where the 2 GiB bound ends a chunk early: about 5,100. On a local disk that overhead is 9 to 43 minutes in total. On the share each call also starts rsync against SMB, checks the destination, the `versions` folder and the temp folder, and the tool reads the mount table and runs `ps` three times; if that is 1 to 3 s a call it is 1.4 to 4.3 hours. The copy itself at the conf's 8.9 files a second is 31.6 hours. The read-back of every sent file is unmeasured: between 43 minutes (if it reads as fast as the share lists, 390 a second) and another 31 hours (if it reads as slowly as it writes). So: **about 35 to 70 hours, most likely two days**, and the first fifteen minutes of "after chunk N of M: X of Y planned files proven and saved" lines will give the real rate.

## CONDITIONS FOR THE FIRST REAL COPY (an order to run, for whichever build is allowed to run)

Before anything is written:
1. **The fixes for findings 1 and 2 are in and re-checked** (their two reproduction scripts turned into tests that fail without the fix). Finding 3's proof-time check and finding 4's names file belong in the same change if the wide rule stays.
2. A fresh `bash nas_backup.sh --dry`: exit 0, no PROBLEM line, totals near 1,012,110 files and 68.27 GiB; then `tests/scan_dry_lists.py` and the second checker's `S_scan_real_lists.py` on its stamp: 0, tier A 0, tier B 0, controls above 0.
3. Read the share yourself, read-only: `mount` shows `//DotORG@192.168.20.154/DEV-Working on /Volumes/DEV-Working (smbfs` (the tool checks only the word `smbfs`); `ls -ld` of `/Volumes/DEV-Working/General`, `/Volumes/DEV-Working/General/Wednesday` and `/Volumes/DEV-Working/Secuura` each starts with `d`, never `l`. Free space: the seat's saved `df` line shows about 10.8 TiB free against a 200 GiB floor.
4. The conf: `scripts/` has no tool for it, so by eye or with the six lines in `raw/Z2_real_conf_overlap_check.txt`'s script: no two sets of one client with nested destination names (0 today), no name used twice (0 today).
5. Holds: `mv -n HOLD_wednesday HOLD_wednesday.lifted-<date>`. `HOLD_tuesday` and `HOLD_friday` stay. Do not install the job; nothing is armed today (0 `nasbackup` plists, 0 templates in `scheduler/jobs`, control 1 `naspush` in each; `raw/Z1_armed_and_neighbours.txt`). Never try a `--run` while the hold is still in place and the conf is in doubt (finding 10).
6. **The old job.** `com.wednesday.naspush` is loaded and fires at 03:30 every night; it writes to the other share (`/Volumes/Backup`) from the same drive. The two do not share a lock, a folder or a state file, so they can run on one night; the cost is speed on both, and the first copy will cross at least one 03:30. Whether `naspush` is held for those nights is Kam's. Do not unload it on your own.
7. The log of the run goes OUTSIDE every backed-up folder (for example `~/Library/Logs/`): a log inside the seat's tree is a planned file that changes during the run and fails the night.

The run:
8. **One small set first, with the tool as built.** There is no flag for one set. Move one small `set=` line (one of the eleven small general projects that holds files) to be the FIRST `set=` line; the END count stays 49. Then, in a tmux window: `caffeinate -i bash 2_Project_Files/nas-backup/nas_backup.sh --run --out-of-sequence <id of Kam's approval card> --max-seconds 900 > ~/Library/Logs/nasbackup_first_small.log 2>&1`. Watch the screen for a privacy dialog for `rsync` or `python3` and answer Allow. Expected end: exit 4, "stopped by the run-time cap", the small set complete, the next set partly sent, state not good, no COMPLETE marker. That is the first real test of the folder chain, the chunked engine, `--backup-dir`, `--temp-dir` and the read-back on SMB.
9. Read after it, read-only: in the log, every `chunk ... engine pass` line says `rc=0` and `deleting lines: 0` with no `stderr (` part; the small set's line says `NOT PROVEN: 0`. On the share: the small set's file count under `current/<set>` equals its "source in scope" number; `versions/` holds no file; nothing new exists outside `General/Wednesday/nightly-backup` and `Secuura/Wednesday/nightly-backup`. On the drive: `state/wednesday.json` says `killed-cap`, `state/wednesday.index.sqlite` exists.
10. Then the long run, same command with `--max-seconds 432000` and a new log name. No `tee`, no `--accept-shrink`, no change to `max_deleted_*`.
11. While it runs: the newest `after chunk N of M` line is the progress and the rate; `bash nas_backup_watch.sh` shows `lock: pid N RUNNING`; `logs/wednesday/<stamp>_run_<set>.rsync.err` should hold only the `## chunk` headers.
12. When it ends: exit 0 and the GOOD line with the state saying good (`bash nas_backup_watch.sh` names the last good backup), one `RUN_<stamp>_COMPLETE.txt` per client folder, the manifest's totals against the dry run's, the `DELETED AT SOURCE` lines read one by one. Then put the HOLD file back until arming.

What a failed first night looks like, and what not to do:
13. **Most likely: exit 8 with NOT DELIVERED names.** Over a day or two on a live tree, files change during all three passes and folders are removed; the strict rule fails the night for each. That is the tool being honest. Run the same command again: it lists the destination (about 43 minutes for a million files at the conf's 390 entries a second), trusts the index, and sends only what is not proven. Exit 4, 5 or 7: read the reason, run again.
14. **Do not:** clear the lock while any rsync of this seat is alive (the tool refuses; do not work around it); kill with `-9` (the engine lives on; use Ctrl-C or SIGTERM); delete or move the index or the state file "to start clean" (the index is the proof of what arrived: losing it means reading the whole share back); delete, move or rename anything under `nightly-backup/` on the share to tidy a partial copy; add `allow_empty`, raise `max_deleted_files` or pass `--accept-shrink` to make a failed night pass; edit the conf while a run is going; read a GOOD line or a COMPLETE marker as good when the state file does not say good (finding 8).
15. **Stop and put the HOLD back** on any of: exit 9 (a deleting line), "a secret-shaped name travelled", a file of this backup found outside the two `nightly-backup` folders, or `INDEX DAMAGED`/`STATE FILE DAMAGED` during the run.

Proposals, in order:
16. `proposed/PORTABILITY.proposed.md`: text only, Wednesday's own file, safe at any time after the first GOOD.
17. The doctor block (one sourced line in the shared `doctor.sh`): after the first GOOD. It is a shared file, so it runs at every seat's boot: on TUESDAY and FRIDAY trees it prints the held warning once a day. Apply it as Wednesday's shared change and tell both seats the same day. Unfixed, findings 9 and 10 make it warn or fail on states that are not a missed backup.
18. `proposed/install_all_jobs.proposed.md` (the template and two installer lines) is arming: Kam's word, after a first GOOD by hand and with `HOLD_wednesday` lifted. `proposed/launcher.proposed.md` proposes no change.
19. `proposed/INSTRUCTIONS-for-other-seats.md` is sent only when Wednesday says go; Tuesday needs her scope added to the lane first, and Friday needs two rulings from Kam that the file names. Neither is touched by a Wednesday first copy.

## WHAT HELD

- **Round 2's holes:** N1a 3 nights, N1b 2, N1c 1, N1x 3 (and its night 1 with 40 changed files): 0 GOOD, every destination copy accounted for; N3d GOOD on night 1 with 0 altered copies left; 5 emptying patterns refused; a slow shrink is still 10 GOOD nights (stated limit); the nightly job cannot accept a shrink.
- **No content lost:** in every test where a destination file was replaced, the earlier content was found under `versions/` (4 of 4 distinct contents across passes and two runs; the altered copies of N3d and of my SIGKILL test; the outer set's file in finding 1).
- **Case-sensitive source** (a disk image; the earlier checks had none): 12 real colliding pairs and 2 colliding folders: 24 files left out, all 24 named in the manifest, 8 of 8 others proven, **0 destination files holding another file's content**; dotless-i pairs are not folded by the tool or by the scratch volume and both arrive; a case-only rename keeps the old spelling with the new content, as README states (`raw/A10_case_sensitive_source.txt`).
- **Secrets:** 12 of 12 case and decoration spellings of the two folder names, the plan-time hard link, a symlink to a secret file and a symlinked secrets folder: 0 on the fake NAS. Three name scans on the real dry list: 0.
- **Hold:** 5 of 5 held calls exit 3 with nothing started.
- **Damage:** 4 of 4 callers handled as designed; the notice survives until `--ack-damage` (suite T16, T25).
- **Real lane as found:** 15 engine list checks in the saved dry run, 15 with `deleting lines: 0`, 0 PROBLEM lines, 15 "listed on the NAS (read-only)" lines.

## NOT TESTED

- **Anything on the real NAS, in any mode.** I ran no dry run; I used the seat's saved lists. SMB renames, names ending in a dot or space, the cache question of note 20, speed, the chunked engine and the read-back at scale.
- **Whether `General/Wednesday` on the real share is a plain folder** (finding 2): not licensed to list below the top level.
- **launchd**, the privacy prompts, the doctor block inside the real `doctor.sh`, the launcher. No launchctl verb except a read-only `list`.
- **The real code path outside test mode** (`nas_root` fixed, the real mount table, `statvfs`).
- **Scale:** a million files, memory, the index at a million rows, the watchdog's real margin.
- **A quiet-machine timing** of anything: the load average was never below 3.7.
- **The second checker's N6, N8 and N11 scripts and the first checker's A, B, C, H:** not re-run by me; the seat's re-runs are in its evidence and I read their summary lines only. My A4, A5 and A7 cover the same ground with new inputs.
- **`tests/claims.tsv` line by line** against STATUS's wording: I ran the program and attacked it; I did not read all 140 claims.
- **File contents.** A secret in an ordinary-named file is invisible to every test here.
- **A HOLD file spelled in another case on the case-sensitive drive:** my fixture's lane folder was on the case-folding scratch volume.

## FOUND / TESTED / HOW

- **Instruments:** a scratch copy of the lane in a WEDNESDAY-named tree (`nb_core.py` and `run.sh` sha256 equal to the lane's, shown in `raw/` by the suite run's header and in my setup output); fake source and NAS trees; stub engines that act between plan and proof; one fault-injection driver (`scripts/A5_inject.py`, used for finding 8 only); a 300 MB case-sensitive APFS disk image at `/private/tmp/qa3nb`, mounted under the fixture with `-nobrowse` and detached at the end of the script (0 mounts left); my own names-only scan; an oracle that compares every source file with its destination by sha256.
- **Positive controls:** the unmutated suite passes before any mutant; every refusal test has an accepted neighbour (the `Docs2` control beside finding 1; 100 and 0.01 beside 101 and 0.02; a travelling `main.ts` beside the unnamed exclusions; the plan-time hard link beside the swapped one; 52,213 `.md` paths beside each 0 of the scans; the claims program refusing 3 planted controls).
- **What I adapted in the second checker's scripts:** one line, in a COPY (`raw/R2_my_adaptation_of_his_lib.diff`): the scratch path in `r1_adapted/lib.sh`. His display greps for "gone from the source" find nothing now because that sentence no longer exists; I read the rc and GOOD columns.
- **My own instrument errors, outputs kept:**
  1. `raw/A5_damage_lock_signals.txt` section c, row "found by dry" shows "moved aside=1": that count was taken after my own follow-up `watch` call, which is what moved the file. The dry run itself wrote 0 notice lines and moved nothing (the suite's T25 shows the same).
  2. `raw/A3_deleted_proof.txt` section g prints the tail of a refusal line ("fire must be HH:") as its reason; the refusal is the right one, my `cut` was too short.
  3. `scripts/A3_deleted_proof.sh` section h has a stray empty `for` loop over 70,000 numbers and its heading says "700 of 1000"; the test that ran is 650 deletions of 70,002 planned files.
  4. `raw/A8_items_2_3_4.txt` section 3c cannot show whether one set's finding withdraws another set's proofs: the second set's own one-file sample happened to hit an altered file. The code withdraws per set only.
  5. `raw/A9_chunk_overhead.txt`: the second pair of timings ran under my own mutant runs; I kept both pairs and give the range.
  6. In `raw/R2_N1x_whole_source_unreadable.txt` the last line ("night 2 ... rc=8") is the second checker's own instrument error 3 again (his stub makes the folders unreadable a second time), not a failure of recovery.

## DID THE CHECKER MODIFY ANYTHING

`raw/Z9_nothing_modified.txt` (script `scripts/Z9_nothing_modified.sh`), lists taken at 19:41 before anything else and again at 21:07 after everything:
- Lane: sha256 of all 333 files, before and after: identical (diff exit 0).
- Both earlier checkers' folders: 94 files: identical.
- `ls -la` of `/Volumes/Backup` and `/Volumes/DEV-Working` (28 lines: names, sizes, times): identical. No script of mine names a path under them; `raw/S1` to `S3` read the lane's saved dry lists only.
- Control: the same diff on a copy with one character changed exits 1.
- What I did outside my folder: scratch trees and one disk image under `/private/tmp/qa3nb` (image detached, 0 mounts of mine left); a read-only `launchctl list`; `diskutil info` on two volumes; read-only reads of the lane, the two verdict folders and `~/Library/LaunchAgents`. No launchctl verb that changes anything, no git write, no network, no tmux keys, nothing opened inside any `4_Credentials` or `3_Access_Keys` folder.
- I wrote in `2_Project_Files/qa-checks/nasbackup-r3/` only (`verdict.md`, `STATUS.md`, `scripts/`, `raw/`).
