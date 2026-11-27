# nas-backup: nightly, staggered, copy-only backup of a seat to the NAS (WED-170), round 4

Authority: Kam, live board 2026-11-27 12:03:29 (verbatim in `BRIEF.md`). Round 1 and round 2 were each checked independently on 2026-11-27 and each got NO GO (`0_Brain/reference/2026-11-27_qa-nasbackup/verdict.md`, `0_Brain/reference/2026-11-27_qa-nasbackup-r2/verdict.md`). Round 3 is built on one rule, ruled by Kam on card `wed-nas-backup-second-nogo-round3-1127` (2026-11-27 16:40): **unproven means failed.** The brief of round 3 is `ANSWER-4.md`. Round 3 was checked a third time and got NO GO on three constructed inputs and one unmet condition (`2_Project_Files/qa-checks/nasbackup-r3/verdict.md`). **Round 4 is one short fix round, ruled by Kam on card `wed-nas-backup-third-nogo-end-or-fix-four-1127` (2026-11-27 21:24): six named fixes and nothing else** (`ANSWER-6.md`). They are marked "round 4" below. Earlier files are kept in `round1/`, `round2/` and `round3/`.

**Nothing here is armed.** `HOLD_<seat>` files make every real run refuse; no launchd job exists; the only things ever done on a NAS from this lane are the two licensed moves of secrets folders on the Backup share (`RESULT-secrets-move.md`, `RESULT-secrets-move-2.md`) and the licensed erase of that quarantine folder (`RESULT-quarantine-erase.md`).

## The one rule

**A night is GOOD only if every file in the plan is PROVEN at the destination with the source's content. Anything else fails the night and is named.**

The plan of a set is the list of its in-scope files, made when that set starts (sets are planned one after another, each just before it is copied, so the list is as fresh as it can be). After that list is made, nothing can take a file out of it. At the end the tool subtracts what is proven and what is provably deleted; whatever is left is `NOT DELIVERED`, with the reason, and the night is not good.

- **Proven** means sha256 of the source equals sha256 of the destination, with the source unchanged across the read. A file the run did not send rests on an earlier proof of exactly that kind: same size at the destination and its exact stat in the local index, which only ever receives proven files.
- **A planned file that cannot be read at proof time is NOT DELIVERED, whatever the reason:** permission denied, an I/O error, a macOS privacy refusal, a folder that went away, a file that turned into a folder or a link. "Could not read it" is never taken to mean "it was deleted".
- **Deleted is the one exception, and it needs proof:** the set's root is still the very folder that was listed, the file's parent folder can be listed, and the name is absent from that listing, checked twice. Such files are counted and named in the run's output, in the GOOD line and in the manifest. More than 5 of them in one set, or more than 0.1% of a large set's plan (`max_deleted_files`, `max_deleted_fraction` in the conf), fails the night. A file whose parent folder is itself gone is NOT counted as deleted: a folder that cannot be listed proves nothing. So a folder with planned files in it that is removed during a run fails that night; the next run plans afresh. **Round 4 adds two conditions, because the third check counted two files as deleted that still existed:** the planned path must no longer resolve at all (on a drive that folds case, a file renamed to another case is absent from the listing by name while its old path still opens it), and the parent folder must still be the very folder that was listed, by device and inode (a folder replaced by a new one of the same name lists without the file, and the file lives on wherever the old folder went). So a folder that is REPLACED during a run fails the night exactly like one that is removed.
- **A set whose plan holds zero files fails the night**, on a first run too, with or without folders. The one exception is a set the conf names in an `allow_empty=<set>` line. One real set carries that mark today (`CODING/Docker - Containers`: one folder, no file in scope).
- **A sample finding is repaired in the same run or the night fails.** Each night 40 files per set that were not sent are read back and compared. One that no longer agrees loses its index row at once and is sent again; the wrong destination copy goes to `versions/`. If the destination copy itself was wrong, the earlier proofs of every other unsent file of that set are withdrawn too and each file is read back in the same run, because they are proofs of the kind that just turned out false. A file that cannot be repaired stays without an index row, so every later night compares it by content and fails until it is proven. A finding never ages out.
- **The engine's exit code decides nothing.** Exit 23 or 24 is survived only because every file is then proven one by one. Any other non-zero code fails the night even if everything arrived.
- **A set that lost more than half its files** against the last good run fails with both numbers. If the source really shrank: `--accept-shrink <card id>`, once, by hand. The nightly job cannot give that flag. The baseline is kept twice (state file and index), so a damaged state file does not switch the rule off.
- **A set the run never reached** (stopped by the cap, a stall, an unmount) is named as not proven.

Named exceptions that are out of the plan by rule, counted in every run and listed in the manifest: symlinks (recorded, not created); names differing only in case from a sibling (the drive is case-sensitive, the NAS is not; neither is copied); files with more than one hard link.

**A planned file that gains a second hard link after the plan (round 4)** is not such an exception: it is in the plan, so it fails the night. Every file of a chunk is looked at again immediately before the chunk is handed to the engine; one that has more than one hard link by then is taken out of the chunk, not sent, and named `HARD LINK AFTER THE PLAN, NOT SENT`. If the second link appears after the hand-over, the arrival proof refuses to prove the file, and the run says `HARD LINK AFTER THE PLAN, SENT: <path> -> <destination path>`, with whether the content is at the destination now. This tool never deletes at the destination, so that copy stays there until someone removes it by hand.

## The pieces

| File | What it is |
|---|---|
| `nas_backup.sh` | The backup. **Dry run by default**; a real run needs `--run` |
| `nas_backup_nightly.sh` | What the scheduler calls. Runs when there is no good backup since the window opened; otherwise logs why not |
| `nas_backup_watch.sh` | The three-day check and the damage notice. Reads only the state on the drive and the clock |
| `nb_core.py` | The engine behind all three (Python 3.9+, standard library). `nb_common.sh`: seat and python lookup |
| `seats/wednesday.conf` | Sources, window and added exclusions. Ends with `END lines=<N>` |
| `seats/wednesday.tokens` | The other client's project names, for reporting. The seat maintains it |
| `jobs/nasbackup.plist.template` | The launchd template. Kept out of `scheduler/jobs/` until arming |
| `HOLD_wednesday`, `HOLD_tuesday`, `HOLD_friday` | While present, `--run` and the nightly script exit 3 |
| `proposed/` | The one arming change, the doctor block (a real file, tested), PORTABILITY text, instructions for the other seats |
| `tests/run.sh`, `tests/mutants.sh` | The suite on a fake NAS; deliberate breakages the suite must catch |
| `tests/scan_dry_lists.py` | An independent scan of a dry run's lists for secret-shaped names |
| `tests/claims_check.py`, `tests/claims.tsv` | A program that checks every coverage claim in STATUS against a suite run and a mutant run |
| `state/`, `logs/`, `manifests/` | Run state on the drive, git-ignored |

Only the Wednesday seat can run. Tuesday and Friday have no entry in the tool's seat table; from their trees every command exits 2.

## Where the copy goes

```
/Volumes/DEV-Working/<Client>/Wednesday/nightly-backup/
    current/<set>/...            the latest copy
    versions/<run stamp>/<set>/  the PREVIOUS copy of every file, or folder, that run replaced
    manifests/                   one manifest per run, and the symlink lists (never the left-out lists: below)
    runs/                        RUN_<stamp>_STARTED.txt, and _COMPLETE.txt only when the run was proven good
    _tmp_incoming/               the engine's temp files
```
`Secuura/Wednesday/` holds the Secuura client folder and Secuura's test material from `Testing Agent MAIN/projects/secuura`. `General/Wednesday/` holds the seat's own tree and the general projects.

## What a run may carry

### Secrets, by the shape of a name: best effort, and it cannot be complete

**A rule that recognises names can never be complete, and nobody should read a zero from it as "no secret travels".** A credential in a file called `notes.md`, `config.json` or `Agent Mail.md` looks like any other file to this tool. The rule exists to keep the well-known containers out; it over-excludes on purpose, and it will still miss a name nobody thought of. The real protections are these four: the folders named `4_Credentials` and `3_Access_Keys` are excluded by a contained name in any case and any decoration; a file with more than one hard link is skipped, because its other name may sit inside such a folder; another client's folder and the other seats' trees are refused as sources in both directions; and the NAS share is private to this network. Everything below is on top of those.

A path component is secret-shaped when its lower-cased name:

- contains `4_credentials` or `3_access_keys`;
- starts with `.env`, contains `.env.`, or ends with `.env`; or is `env.backup`, `env.bak`;
- ends with, or carries before a further suffix, `.pem .key .p12 .pfx .ppk .jks .keystore .kdbx .skey`;
- ends with `.p8 .der .pkcs12 .ovpn .mobileprovision .kdb .agekey .gpg .asc .cer .crt .vkey .addr .wallet .priv`; starts with `keystore` or `utc--`;
- contains `.tfstate` or `.tfvars`; starts with `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa`;
- is one of the stores `.ssh .aws .azure .gh-config .gnupg .kube .docker .auth gcloud .secret .secrets`;
- is one of `.netrc .npmrc .pypirc .pgpass .git-credentials credentials.json secrets.json secrets.yaml secrets.yml service_principal_entries.json local.settings.json application_default_credentials.json .dockercfg .vault-token .boto .s3cfg .terraformrc .yarnrc.yml credentials auth.json token.json tokens.json accesstokens.json azureprofile.json wallet.dat`;
- starts with `client_secret`, `msal_token_cache`, `github_deploy`, `htpasswd`, `.htpasswd` or `kubeconfig`; contains `deploy_key`, `deploy-key` or `.kubeconfig`; ends `_deploy_rw` / `_deploy_ro`;
- is a service-account key by name (`service-account*.json`, `serviceAccount*.json`, `*-sa.json`, `*sa-key*.json`);
- is `secret.<ext>` or `secrets.<ext>` with one extension (so `secrets.toml` and `secrets.ts` are out, `secrets.example.yml` is in);
- contains `credential` and ends in a data extension (`.json .yaml .yml .csv .ini .xml .txt .toml .db`);
- contains `private-key`, `private_key`, `privkey`, `signing-key`, `signing_key`, `mnemonic`, `seed-phrase` or `recovery-phrase` in any of their spellings.

The last eleven lines are round 3's additions. They cover the 23 conventional names the second check found still travelling, the two real files it found in the travel list (`local.settings.json`, and a token file inside a `.auth` folder), and every pattern in the tier it called "conventional names" in its own scan, so that both independent scans read zero on the real dry list.

**The accepted cost, with numbers from the real scope:** see STATUS for the counts of the last dry run. The old rule already left out `.envrc`, `.env.example`, a Keynote `presentation.key`, a public `id_rsa.pub` and every `.npmrc`. The new lines also leave out things that are not secrets: public certificates (`.crt`, `.cer`), test evidence whose file names contain `credentials`, source files named `secrets.ts`, a few documents whose titles contain "private key". A restore from this backup would have to get those from their repositories. Excluded entries are counted per shape in the run summary; names are never printed there, and never written to the share.

### What the rule left out, by name: on the drive only (round 4)

Every run, a dry run too, writes one file per set into this lane's `manifests/<seat>/` on the DRIVE, beside the symlink list: `<stamp>_<run or dry>_<set>_left_out_by_secret_shape.tsv`. One line per entry the secret-shape rule excluded: the path inside the set, a tab, the shape. A folder is one line; nothing under it was looked at. A backslash, tab or line break inside a name is written as `\\`, `\t`, `\n`, `\r`, so the number of lines is the number of entries, and it equals the per-set count the run prints. A set with nothing left out has an empty file. This is the list to read at restore time to see what the backup does not hold.

**It is not on the share, on purpose.** It holds the names and places of the real secret files (`.env`, key files, the credentials folders). The share's manifest folder gets the symlink list and the counts; it never gets this list, and the manifest that is copied to the share carries only the count and the list's path on the drive. The list's own file name (`*_left_out_by_secret_shape.tsv`) is excluded from every set, so the lists do not travel as part of the seat's tree either. `manifests/` is git-ignored. What this cannot cover: if someone copies those names into a file with another name inside a backed-up folder (a report, a note), that file travels like any other.

### Other clients and seats

- **Forbidden roots, in both directions.** The forbidden roots are the other seats' trees (folders at the top of the drive, or beside this seat's tree, whose names contain `tuesday` or `friday`) and the other client's folders (a name containing `datasec` at the top of the drive or one level below it, where client folders live; on this drive today that is `Notes (MASTER)/Datasec`, and the other roots found are `TUESDAY` and `_handover/tuesday-seat`). A `set=` source is refused when its real path IS such a root, lies INSIDE one, or is an ANCESTOR of one. A source that is an ancestor of this seat's own tree is refused as well. So "add the rest of the drive" cannot be written as one line: folders are named one by one.
- A `set=` path is resolved with `realpath` first; any component that contains `datasec`, `tuesday` or `friday` in any case refuses it. A source that is a symlink, or is reached through a symlinked parent, is refused.
- One set inside another is refused unless the outer set has the matching `exclude_path` line, so nothing travels twice or by a second route.
- Inside every set: a name containing `datasec`, any case, is excluded; a FOLDER named exactly `tuesday` or `friday` is excluded. Inside the seat's own tree only: any name containing `tuesday` or `friday` (in project folders those words are library file names).
- **The other client's project names are reported, not excluded**, per Wednesday's reading of Kam's ruling `nas-shared-folders-owner` (2026-09-11) in `ANSWER-2.md`. Each run prints, per token in `seats/wednesday.tokens`, how many in-scope paths carry it.

**Fixed exclusions otherwise:** `.git` (so unpushed commits are NOT in the backup), `node_modules`, `worktrees`, virtualenvs and caches, `_quarantine_*`, the brain-db `pgdata-*` directory, system litter, and this tool's own left-out lists (`*_left_out_by_secret_shape.tsv`). `._*` is excluded for files only.

## The configuration fails closed

- The last content line must be `END lines=<N>`, N being the content lines before it. No marker, or a wrong count, is refused.
- A key given twice is refused: which line wins is never guessed.
- An `exclude_path` that names nothing at the source is refused by name; a wildcard in it is refused.
- **Destination names may not nest (round 4).** Two sets of one client where one destination name is a path prefix of the other (`X` and `X/sub`; compared part by part at `/`, ignoring case) are refused: the inner set would write inside the outer set's folder and the two would overwrite each other's files every night while each proof passed in turn. The same nested names under two different clients are fine: their folders differ (the real conf has one such pair).
- **One destination name under two clients is refused (round 4).** The baseline of the fall rule, `allow_empty` and the index are kept by the destination name alone; two sets with one name would share a row in each.
- A pattern that matches every name is refused before anything runs: `*`, `?*`, `**`, `*.*`, `[!~]*`, `*[a-z0-9]*` and the like (tested against ordinary probe names). Whatever still empties a set is caught by the zero-files rule.
- **What the END marker does not do:** it counts lines, it does not seal them. An `exclude_path` line replaced by another valid line keeps the count; the excluded bulk then travels and the run is good. Not fixed in round 3: a checksum line would catch accidental damage but not an edit, and it would make every hand edit of the conf need a tool. `max_files` per set is what bounds the result.

## How one run works

1. **Refusals first:** unknown or disagreeing seat; `HOLD_<seat>` (tested before the conf is even read, round 4); conf not sealed or with a key twice; destination names that nest or repeat; source not a local mount, not on the seat's drive, forbidden, an ancestor of something forbidden, or nested without its exclude; NAS not in the mount table as `smbfs`; client folder absent or in a different case; a symlink anywhere in the destination chain; free space under 200 GiB; rsync not version 3; outside the window without `--out-of-sequence <card id>`; another run, or its engine, still alive.
2. **Per set, the mount table is checked again. Then the destination is checked (round 4):** no level of `<NAS>/<Client>/<Seat>/nightly-backup/current/<set>` may be a symlink (the client folder itself included), and the real paths of the set's destination, `versions`, `manifests`, `runs` and `_tmp_incoming` must lie inside the real path of this seat's own `nightly-backup` folder; otherwise the set is refused before anything is written for it. The same is asked again before every chunk, and once more before the manifest and the COMPLETE marker are written. Then the source is listed under the rules and the destination is listed, and the left-out list is written on the drive. Per file: copy if absent, if the size differs, or if it is not proven and the sha256 differs. A file found identical by sha256 is saved to the index as it is found.
3. **The sample** of unsent files is read back first; a finding joins the copy list (see the one rule).
4. **Type changes:** a folder that became a file, or the reverse, has its old destination entry moved into `versions/<stamp>/`.
5. **Copy in chunks** of 200 files (`chunk_files`) or 2 GiB, each chunk first stripped of any file that has gained a second hard link (round 4): `rsync -t -O -I --from0 --files-from=<chunk> --backup --backup-dir=<versions/stamp> --temp-dir=<_tmp_incoming>`, in its own process group, recorded in the lock with its start time. **After each chunk every file of it is proven and the proofs are committed to the index** before the next chunk starts. A file that changed meanwhile is sent again, up to two more passes, each into its own `versions/<stamp>_passN/`.
6. **Read the engine's output:** a `deleting` line fails the run (exit 9); a secret-shaped name in it fails the run.
7. **The accounting:** planned, minus proven, minus provably deleted. Then the mount table once more.
8. **Write** the manifest (drive and NAS), the COMPLETE marker only if good, and the state file. The lock is released whatever happened, also after an unexpected error, which is reported in one plain line.

A dry run does steps 1 and 2, lists the real destination read-only, and checks the list with `rsync -n` against an empty LOCAL folder. The engine is never handed a NAS path in a dry run. A dry run writes nothing to the state file or the index: a damaged one is reported and left where it is.

**Interruptions.** SIGTERM, SIGINT and SIGHUP (a closed terminal) stop the engine, keep every proof made so far, record the attempt as failed and release the lock. The cap (`max_seconds`, or `--max-seconds`) stops the engine and is also honoured between files while proving and comparing. A watchdog stops the whole run 15 minutes after the cap if a read is blocked. An interrupted run can never leave the state saying good: good is written in one place, after the accounting. The next run sends only what is not proven and re-reads only the files of the one chunk that was in flight.

## The three-day flag and the damage notice

- The clock starts at the last good backup. Before the first one, at the first attempt or fire ever recorded (stored once, never rolled), or at the first time the watch saw the seat un-held with nothing on record.
- **The hold does not run the clock.** A refusal under `HOLD_<seat>` is recorded as `held`, not as an attempt, and the first run, fire or check after the hold is lifted starts the clock then. (Round 2 let refusals under the hold start it, so lifting the hold for the first copy would have raised OVERDUE at once. Round 3 still read the conf before it looked at the hold, so a held run with an unconfirmed conf was recorded as refused and started the clock; round 4 tests the hold first, so under the hold every `--run` is `held`, whatever else is wrong.)
- The nightly job calls the watch read-only. Its output goes to a launchd log no seat reads, so it never prints the card.
- **The channel to a seat is doctor.** `proposed/doctor_nasbackup_block.sh` prints a hard-failure line naming `nas_backup_watch.sh --card` while a card is due and not recorded as raised. `--card` prints the one `decision_queue.sh add` command and consumes nothing; it prints again until a seat records `--mark-raised <id>`.
- **A damaged state file or index leaves a notice, whoever finds it.** State: unreadable, not JSON, valid JSON that is not a valid state, or a recorded time in the future. Index: not a database, or failing its check. The file is moved into `state/_quarantine_<date>/`, one plain line says so, and a line is appended to `state/DAMAGE_NOTICE_<seat>.jsonl`. While that notice exists the watch says so at every call and exits 5, and doctor's block prints its own hard-failure line (`NAS BACKUP STATE WAS FOUND DAMAGED`), held or not, at every boot. Only a seat clears it: `nas_backup_watch.sh --ack-damage` (the notice is moved aside, not deleted). The nightly job can find the damage; it cannot use the notice up.
- The cost, unchanged from round 2: the record of the last good backup goes with a damaged state file, so the three-day clock restarts at the damage.

## The lock

One writer per seat. The lock records the holder's pid and when that process started (a reused pid is not the holder), and the engine's process group and when its leader started (a reused group id is not the engine). `--clear-stale-lock` and a new run both refuse while any engine process of this seat is alive, found by the recorded group or by an rsync command line naming this seat's destination, even if the tool that started it was killed.

## Limits, stated and not fixed in code

- **One altered destination file may go unnoticed for a very long time.** The nightly sample is 40 unsent files per set, at most 600 of about a million files (0.059%). By the second check's arithmetic, one altered file in the Secuura set (587,130 files) is expected to be noticed after 14,678 nights (median 10,174); in the seat's tree after 6,630 nights; in Secuura's test material after 3,633. A destination file DELETED behind the tool is noticed the next night and sent again. What round 3 changed is what happens after a finding (full read-back of the set, repair or fail), not the chance of finding. A periodic full read-back would turn this into a real check; it is not built.
- **A slow shrink is not seen.** The fall rule compares with the last good night only: 1,000 files down to 3 over ten nights, 45% a night, is ten good nights.
- **Growth is unguarded.** 5,000 files appearing in a set overnight are copied without a line. Only `max_files` bounds a set.
- **Versions are never pruned**, and no run prints the size of `versions/`. The stop is the 200 GiB free-space floor, which refuses the run and so reaches the three-day flag: late, not silent.
- **`--accept-shrink` is by hand and not sticky.** The nightly job has no way to accept a shrink.
- **A wrong but existing `exclude_path`** is accepted: the tool cannot know intent.
- **Two seats can copy at once.** The seats run on different machines and the lock is per seat.
- **No wake is scheduled.** A Mac asleep through its whole window does not back up that night; the three-day flag is what says so.
- **A rename that differs only in case** keeps the old spelling at the destination with the new content.
- **The watch and a running backup both write the state file** without a lock between them. Read in the code, not reproduced.
- **A live tree.** A file that is rewritten during every pass is never proven, and a folder removed mid-run takes its planned files with it as NOT DELIVERED. A long daytime first copy may well end FAILED naming a few files. That is the tool being honest; the re-run is short.
- **The proof reads every sent file back from the NAS.** That adds to the first copy's time, which is already about 32 hours by extrapolation and is not measured.
- **An orphan engine.** After SIGKILL of the tool the engine still finishes the chunk it was given (at most 200 files); nothing proves or records them until the next run compares them.

### Round 4: what the fixes do not close, and what the third check found that this round does not touch

- **The hard-link check narrows a race, it does not end it.** A second link that appears while a chunk is in flight (at most 200 files or 2 GiB) is sent; the proof then refuses it, the night fails and the path is named, but the content is at the destination and stays there. A link that appears and is removed again before the proof is not seen at all. And once a file has a second link when a later night's plan is made, it is left out by the ordinary rule and that night can be GOOD while the copy from the failed night is still at the destination: the failed night's line is the notice.
- **A planned FOLDER swapped for a secrets folder** between plan and copy delivers same-named files under the ordinary folder name (the third check's note, inherent to a rule that reads names).
- **The symlink checks are made when a set starts, before every chunk, and before the manifest is written.** A link planted in `versions/` or `_tmp_incoming/` while a chunk is in flight receives that one chunk's writes (at most 200 files); the run stops before the next chunk and fails. A symlinked subfolder INSIDE a set's destination is replaced by a real folder by the engine and the link is kept in `versions/` (held since round 3).
- **Found in round 4 and NOT fixed (outside the six items; listed in STATUS for a ruling):** the tool writes one file with a fixed name into its destination folder, `README.txt`, and it asks whether that file exists in a way that follows links. A link planted at that name and pointing at a file that does not exist yet makes the tool create that file, with the README text, wherever the link points (measured on a fake NAS: `evidence/round4/probe_sibling_readme_file_symlink_NOT_FIXED.txt`). The fix is one word (`lexists`). The real share has no `nightly-backup` folder yet, so nothing is planted there today.
- **Until round 4 is committed, the committed engine is round 3's.** Another session's commit in this repo briefly swaps uncommitted files for the committed ones (seen at 22:15 on 2026-11-27, `evidence/round4/note_the_22-15_commit_window.txt`). A run that STARTS in such a moment executes the committed engine. Commit this lane before any real run.
- **Not addressed in round 4, by ruling (each is a finding of the third check, numbered as there):** 7 the per-set deletion limits add up across sets, and the state file names only the first 20 deleted files; 8 a signal after the accounting leaves a traceback and the state `running`; 9 a traceback when the state folder cannot be written; 11 a healthy index that is only locked is moved aside as damaged; 12 the mount check accepts any share mounted at the path; notes 13 to 21 (among them: a missing or wrong-sized destination copy is re-sent without a line; look-alike folder names such as `4-Credentials` travel; `allow_empty` also switches the fall rule off for its set; the read-back may be served from the Mac's cache).

## Commands

```
bash nas_backup.sh                         dry run (lists both sides, writes nothing to the NAS)
bash nas_backup.sh --scan                  what is in scope, per set (reads the drive only)
bash nas_backup.sh --run                   real run, inside the window, hold lifted
bash nas_backup.sh --run --out-of-sequence <card id> [--max-seconds N]    outside the window, on Kam's approval
bash nas_backup.sh --run --accept-shrink <card id>                        accept once that a set really shrank
bash nas_backup.sh --clear-stale-lock      move a dead run's lock aside (refuses beside a live engine)
bash nas_backup_nightly.sh --decide-only   what a fire would decide now
bash nas_backup_watch.sh                   one status line; exit 3 overdue and no card raised, 4 overdue and raised, 5 damage notice waiting
bash nas_backup_watch.sh --card            the one card command, when due
bash nas_backup_watch.sh --ack-damage      a seat has read the damage notice
bash tests/run.sh [/private/tmp/dir]       the suite, fake NAS only (about three minutes)
bash tests/mutants.sh [/private/tmp/dir]   prove the suite can fail (long: one suite run per mutant)
python3 tests/scan_dry_lists.py logs/wednesday <stamp>    independent scan of a dry run's lists
python3 tests/claims_check.py <suite output> <mutants output>   check STATUS's coverage claims against the runs
```
Exit codes of `nas_backup.sh`: 0 good or dry run done · 2 refused · 3 held · 4 run-time cap or watchdog · 5 engine error, an interruption, or an unexpected error · 6 locked · 7 stalled · 8 not every planned file proven · 9 a deleting line in the engine's log.

While a real run goes: its output prints one line per chunk and, for a set of more than one chunk, how many planned files are proven and saved so far. `logs/<seat>/<stamp>_run_<set>.rsync.log` collects what the engine said for every chunk of that set.
