# nas-backup: nightly, staggered, copy-only backup of a seat to the NAS (WED-170), round 2

Authority: Kam, live board 2026-11-27 12:03:29 (verbatim in `BRIEF.md`). Round 1 was built 2026-11-27 and checked independently the same day: NO GO (`0_Brain/reference/2026-11-27_qa-nasbackup/verdict.md`). Round 2 answers that verdict under Wednesday's rulings in `ANSWER-2.md`. Round 1's files are kept in `round1/`.

**Nothing here is armed.** `HOLD_<seat>` files make every real run refuse; no launchd job exists; the only thing ever written to a NAS from this lane is the licensed move of two secrets folders on the Backup share (`RESULT-secrets-move.md`).

## The pieces

| File | What it is |
|---|---|
| `nas_backup.sh` | The backup. **Dry run by default**; a real run needs `--run` |
| `nas_backup_nightly.sh` | What the scheduler calls. Runs when there is no good backup since the window opened; otherwise logs why not |
| `nas_backup_watch.sh` | The three-day check. Reads only the state file and the clock |
| `nb_core.py` | The engine behind all three (Python 3.9+, standard library). `nb_common.sh`: seat and python lookup |
| `seats/wednesday.conf` | Sources, window and added exclusions. Ends with `END lines=<N>` |
| `seats/wednesday.tokens` | The other client's project names, for reporting. The seat maintains it |
| `jobs/nasbackup.plist.template` | The launchd template. Kept out of `scheduler/jobs/` until arming |
| `HOLD_wednesday`, `HOLD_tuesday`, `HOLD_friday` | While present, `--run` and the nightly script exit 3 |
| `proposed/` | The one arming change, the doctor block (a real file, tested), PORTABILITY text, instructions for the other seats |
| `tests/run.sh`, `tests/mutants.sh`, `tests/scan_dry_lists.py` | The suite on a fake NAS; deliberate breakages the suite must catch; an independent scan of a dry run's lists |
| `state/`, `logs/`, `manifests/` | Run state on the drive, git-ignored |

Only the Wednesday seat can run. Tuesday and Friday have no entry in the tool's seat table; from their trees every command exits 2.

## Where the copy goes

```
/Volumes/DEV-Working/<Client>/Wednesday/nightly-backup/
    current/<set>/...            the latest copy
    versions/<run stamp>/<set>/  the PREVIOUS copy of every file, or folder, that run replaced
    manifests/                   one manifest per run, and the symlink lists
    runs/                        RUN_<stamp>_STARTED.txt, and _COMPLETE.txt only when the run was proven good
    _tmp_incoming/               the engine's temp files
```
`Secuura/Wednesday/` holds the Secuura client folder and Secuura's test material from `Testing Agent MAIN/projects/secuura`. `General/Wednesday/` holds the seat's own tree and the general projects. The seat's own tree goes whole to General, although it holds Secuura briefs and gate clones: it is the seat's record, not a client project.

## What a run may claim

**GOOD means every in-scope source file is proven at the destination with the source's content.**

- A file the run sent is proven by sha256: source and destination hash equal, with the source unchanged across the read.
- A file the run did not send is proven by an earlier proof: same size at the destination and its exact stat in the local index, which only ever receives proven files. A sample of 40 such files per set is re-hashed every night.
- A file that changes while the run is copying is sent again, up to two more passes, each into its own `versions/<stamp>_passN/` so a re-send never overwrites the copy kept from the night before.
- Anything left unproven **fails the run**, is named in the run's last lines (`NOT DELIVERED: <set>/<path>`) and in the state file, and the watch's line names the first one. It is not indexed, so the next night sends it again.
- The engine's exit code decides nothing. Exit 23 or 24 is survived only because every listed path is then proven one by one.
- A set with zero files, or one that lost more than half its files against the last good run, fails the run with both numbers. If the source really shrank: `--accept-shrink <card id>`, once.

Named exceptions, counted in every run and listed in the manifest, which do not fail it: symlinks (recorded, not created); names differing only in case from a sibling (the drive is case-sensitive, the NAS is not; neither is copied); files with more than one hard link.

## What a run may carry

**Secrets are excluded by shape, case-insensitively, and the rule over-excludes on purpose.** A path component is secret-shaped when its lower-cased name:

- contains `4_credentials` or `3_access_keys` (so conflict copies, `.bak`, ` copy`, `old_` are caught);
- starts with `.env`, contains `.env.`, or ends with `.env`;
- ends with, or carries before a further suffix, `.pem .key .p12 .pfx .ppk .jks .keystore .kdbx .skey`;
- contains `.tfstate`; starts with `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`;
- is `.ssh .aws .azure .gh-config .gnupg .kube`, or `.netrc .npmrc .pypirc .pgpass .git-credentials credentials.json secrets.json secrets.yaml secrets.yml service_principal_entries.json`;
- starts with `client_secret`, `msal_token_cache` or `github_deploy`, contains `deploy_key` or `deploy-key`, or ends `_deploy_rw` / `_deploy_ro`.

**The accepted cost:** `.envrc`, `.env.example`, `.environment`, a Keynote `presentation.key`, a public `id_rsa.pub` and every `.npmrc` are left out too. A file with more than one hard link is skipped and named, because its other name may sit inside a secrets folder the walk never enters. Excluded entries are counted per shape in the run summary; names are never printed there. **What this cannot see:** a secret inside an ordinary-named file.

**Other clients and seats.**
- Sources: a `set=` path is resolved with `realpath` first; if any component of the given or the real path contains `datasec`, `tuesday` or `friday` in any case, it is refused. A source that is a symlink, or is reached through a symlinked parent, is refused.
- Inside every set: a name containing `datasec`, any case, is excluded. Inside the seat's own tree only: a name containing `tuesday` or `friday` (in project folders those words are library files).
- **The other client's project names are reported, not excluded.** Wednesday's reading of Kam's ruling `nas-shared-folders-owner` (2026-09-11) in `ANSWER-2.md`: the general folders and the seat's own tree are this seat's records even where a nested name carries a Datasec project name. Each run prints, per token in `seats/wednesday.tokens`, how many in-scope paths carry it. `mps` is matched only as a whole word (bounded by characters that are not letters or digits), so it counts `MPS Calculator` and not `lamps`.
- Where `ANSWER-2.md` and the verdict differed I took the stricter: the verdict's Q01 wants the other-client name exclusion kept and tested, so names containing `datasec` stay excluded everywhere, while project names are report-only as ruled.

**Fixed exclusions otherwise:** `.git` (so unpushed commits are NOT in the backup), `node_modules`, `worktrees`, virtualenvs and caches, `_quarantine_*`, the brain-db `pgdata-*` directory, system litter. `._*` is excluded for files only; a real folder of that shape is kept.

## The configuration fails closed

- The last content line must be `END lines=<N>`, N being the content lines before it. No marker, or a wrong count, is refused: a conf that lost a line never silently widens the scope.
- An `exclude_path` that names nothing at the source is refused by name.
- A pattern that matches every name (`*`) is refused.

## How one run works

1. **Refusals first:** unknown or disagreeing seat; `HOLD_<seat>`; conf not sealed; source not a local mount, not on the seat's drive, or forbidden; NAS not in the mount table as `smbfs`; client folder absent or in a different case; free space under 200 GiB; rsync not version 3; outside the window without `--out-of-sequence <card id>`; another run, or its engine, still alive.
2. **List the source** under the rules. **List the destination.** Decide per file: copy if absent, if the size differs, or if it is not proven and the sha256 differs.
3. **Type changes:** a folder that became a file, or the reverse, has its old destination entry moved into `versions/<stamp>/`, then the new one is copied.
4. **Copy** exactly the list: `rsync -t -O -I --from0 --files-from=<list> --backup --backup-dir=<versions/stamp> --temp-dir=<_tmp_incoming>`, in its own process group, recorded in the lock.
5. **Read the engine's log:** a `deleting` line fails the run (exit 9); a secret-shaped name in it fails the run.
6. **Prove every sent file** by sha256; re-send what changed meanwhile; sample the rest.
7. **Write** the manifest (drive and NAS), the COMPLETE marker only if good, and the state file.

A dry run does steps 1 and 2, lists the real destination read-only, and checks the list with `rsync -n` against an empty LOCAL folder. The engine is never handed a NAS path in a dry run.

## The three-day flag

- The clock starts at the last good backup. Before the first one, at the first attempt or fire ever recorded (stored once, never rolled), or at the first time the watch saw the seat un-held with nothing on record. No other script has to set a mark.
- The nightly job calls the watch read-only. Its output goes to a launchd log no seat reads, so it never prints the card.
- **The channel to a seat is doctor.** `proposed/doctor_nasbackup_block.sh` prints a hard-failure line naming `nas_backup_watch.sh --card` while a card is due and not recorded as raised. The launcher already carries doctor's hard-failure lines into the boot prompt. No launcher change.
- `--card` prints the one `decision_queue.sh add` command and consumes nothing; it prints again until a seat records `--mark-raised <id>`. The id is fixed per gap and `decision_queue.sh` refuses a duplicate id.
- A damaged state file is moved into `state/_quarantine_<date>/`, said in one plain line, and flagged (exit 3); the next run starts clean and says so.
- Under `HOLD_<seat>` the watch says HELD and raises nothing; doctor reports HELD once a day.

## The lock

One writer per seat. The lock records the holder's pid, when that process started (a reused pid is not the holder), and the engine's process group. `--clear-stale-lock` and a new run both refuse while any engine process of this seat is alive, even if the tool that started it was killed.

## Design choices kept from round 1, one line each

- **rsync 3 is transport only; the tool decides what changed.** This NAS does not keep the file times rsync sets (measured on the Backup share), so size-plus-time would re-copy and re-version everything nightly.
- **One fixed folder with dated versions inside**, not a dated folder per night: that would add 68 GiB a night.
- **Nothing is ever pruned.** Clean-up is Kam's word.
- **Outside the window the nightly script does not run** (`late_fire=refuse`, the stricter reading of the brief).
- **A released lock is moved, not removed.** No delete verb anywhere in this lane.
- **A whole-run watchdog** (cap plus 15 minutes) stops a run blocked in a system call.

## Limits, stated and not fixed in code (ruling 9)

- **Two seats can copy at once.** The seats run on different machines and the lock is per seat. When one is catching up or running long, its hour can overlap another's.
- **No wake is scheduled.** A Mac asleep through its whole window does not back up that night; launchd fires once on wake, and outside the window that is a log line. A wake schedule is a machine setting and Kam's.
- **A rename that differs only in case** keeps the old spelling at the destination with the new content. Nothing is lost.
- **The watch and a running backup both write the state file** without a lock between them. Read in the code, not reproduced; the watch writes only on `--mark-raised`, `--mark-armed`, and once when nothing is on record.
- **The proof reads every sent file back from the NAS.** That adds to the first copy's time, which is already about 32 hours by extrapolation.

## Commands

```
bash nas_backup.sh                         dry run (lists both sides, writes nothing to the NAS)
bash nas_backup.sh --scan                  what is in scope, per set (reads the drive only)
bash nas_backup.sh --run                   real run, inside the window, hold lifted
bash nas_backup.sh --run --out-of-sequence <card id> [--max-seconds N]    outside the window, on Kam's approval
bash nas_backup.sh --run --accept-shrink <card id>                        accept once that a set really shrank
bash nas_backup.sh --clear-stale-lock      move a dead run's lock aside (refuses beside a live engine)
bash nas_backup_nightly.sh --decide-only   what a fire would decide now
bash nas_backup_watch.sh                   one status line; exit 3 overdue and no card raised, 4 overdue and raised
bash nas_backup_watch.sh --card            the one card command, when due
bash tests/run.sh [/private/tmp/dir]       the suite, fake NAS only
bash tests/mutants.sh [/private/tmp/dir]   prove the suite can fail (about 20 minutes)
python3 tests/scan_dry_lists.py logs/wednesday <stamp>    independent scan of a dry run's lists
```
Exit codes of `nas_backup.sh`: 0 good or dry run done · 2 refused · 3 held · 4 run-time cap · 5 engine error · 6 locked · 7 stalled · 8 not every in-scope file proven · 9 a deleting line in the engine's log.
