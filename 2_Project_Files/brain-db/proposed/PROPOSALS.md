# brain-db: proposed changes to shared files

Written 2026-11-27 by the WED build seat "brain-db"; revised for round 2 (`ANSWER-1.md`), round 3 (`ANSWER-3.md`, the checker's notes N2 and N3) and round 5 (`ANSWER-8.md`: the sentence of item 2 the third checker found false, its stale figures, the `doctor` table of item 3, and the launcher block of item 4, which now carries the count of files not indexed). **None of these is applied.** Each has a rollback line. The coordinator applies or drops them.

| Shared file | Change proposed | Needed for the tool to work? |
|---|---|---|
| `PORTABILITY.md` item 25 | one sentence amended | no, it is the record |
| `PORTABILITY.md` new item (number set at apply time, see 2) | new item | no, it is the record |
| `2_Project_Files/doctor.sh` | one short block that calls `braindb.sh doctor` | no |
| `Launch_Wednesday.command` | one block: `braindb.sh up` (start, check, rebuild when red) | no: `search`, `at`, `check` and `rebuild` bring the server up themselves |
| End-of-session ritual | one line: `braindb.sh stop` | no, but it is what makes "stopped at wrap" true |
| Drive-sync and eject paths | one note line (item 6) | no |
| Sync profiles | ignore lines (item 7) | no, but see the warning there |
| `2_Project_Files/PORTS.md` | **none**: Unix socket only, no port bound | - |
| root `.gitignore` | **none**: the lane's own `.gitignore` is enough (`git check-ignore` proved it for `pgdata-wednesday/`, `_probe_*/`, `_quarantine_*/`; control `braindb.sh` rc 1). Round 3 added `pgdata-*.lock` to the lane's file. | - |

---

## 1. `PORTABILITY.md` item 25: amended text

Only the "Machine-local" bullet's last sentence and the "No service" bullet change. Proposed replacement for those two bullets:

```
- **Machine-local:** `/opt/homebrew/opt/postgresql@15` (15.19_1). It pulled `icu4c@79` and `krb5`, and UPGRADED `libunistring` 1.4.2 -> 1.5 (old keg kept). Brew also created a non-started default cluster dir `/opt/homebrew/var/postgresql@15` (~38 MB): nothing uses it; never start a server on THAT directory.
- **No service:** no `brew services` job, no launchd plist; every suite/gate starts its own cluster on a private data dir + 127.0.0.1 port and stops it by pid. **One named exception (Kam, live board 2026-11-27 11:43, decision wed-fleet-structure-v2-where-postgres-runs-1127 = c):** the seat's brain search index (the brain-db item below) is started on demand by `2_Project_Files/brain-db/braindb.sh` from a data directory on the drive, on a Unix socket only, and stopped at wrap. It is still not a service: nothing starts it but that tool, and that tool stops it by pid.
```

Rollback: restore the two bullets to their 2026-11-04 wording (the file's git history holds it).

## 2. `PORTABILITY.md` new item

**Number:** the file's last item today is 31 (read 2026-11-27), so 32 is free. The sibling lane `2_Project_Files/nas-backup/` is proposing a `PORTABILITY.md` item of its own in the same round (the checker's note N2; I have not read that lane). **Wednesday numbers both at apply time**; the text below says NN.

```
## NN. brain-db: the seat's local search index (Postgres 15, data ON THE DRIVE) (2026-11-27)
A full-text index over the files this seat is already allowed to read at boot (its two rules files, lessons, the rules index, the seat's ledger and archive, the seat's daily notes, skills, identity, people, architecture). No lesson that is declared another seat's or another client's (by its row, its tier or a marker) enters it; nothing reads meaning, so a lesson about another client's work that is tagged `W` or `M`, scoped to this seat and carries no marker IS indexed (the remedy is to tag or mark the lesson). Kam, live board 2026-11-27 11:43: "Each external drive will now also hold the dB"; decision wed-fleet-structure-v2-where-postgres-runs-1127 = c (local index only). Code and design: `2_Project_Files/brain-db/` (`DESIGN.md`).
- **Machine-local:** the Postgres 15 binaries (item 25: `brew install postgresql@15`) and `python3`. A socket directory `/tmp/wed-braindb-<uid>-<seat>` (mode 700, created by the tool, holds no state).
- **On-drive:** the cluster, `2_Project_Files/brain-db/pgdata-<seat>/` (174 MB for the Wednesday seat, measured in rounds 3 to 4b) and its lock file `pgdata-<seat>.lock`; both gitignored by the lane's own `.gitignore`.
- **Rebuildable: yes.** The files are the master. `braindb.sh rebuild` reloads everything in 9 to 19 seconds as measured on this Mac under load averages of 11 to 24 (4.7 s was measured once at a lower load; there is no figure from a quiet machine); losing or quarantining `pgdata-<seat>/` loses nothing.
- **On demand, no service, no port:** `search`, `at`, `check` and `rebuild` start the server themselves when it is down; the launcher runs `braindb.sh up` at boot; the wrap runs `braindb.sh stop`. Unix socket only. No password or key exists; access is the logged-in user through the socket.
- **Stop the index before ejecting or syncing the drive; the data directory is excluded from every copy because it is rebuildable.** (`braindb.sh stop`.) After a power cut or a pulled drive the next start may print `STALE PID FILE` with one `mv -n` line to run by hand; then it costs a rebuild.
- **New Mac / another drive:** `brew install postgresql@15`, then `braindb.sh up`. A cluster made by a different Postgres major version is refused at `start` with the word "rebuild": move `pgdata-<seat>/` into a `_quarantine_<date>/` folder and run `braindb.sh up`.
- **Per seat:** the seat is the tree's folder name; `WED_AGENT`, if set, must agree. One cluster per seat, each built only through that seat's own confirmed allow-list `2_Project_Files/brain-db/scope/<seat>.scope`. A seat with no scope file is refused before anything is created.
```

Rollback: remove the item.

## 3. `2_Project_Files/doctor.sh`: one block

Placed after the existing `postgresql@15 keg` check (line 470 today). Round 3 moved the logic into the tool (`braindb.sh doctor`), so the block no longer hard-codes a Postgres path (the tool also accepts `/usr/local` and PATH) and no longer reports every unexpected exit code as "index stale" (the checker's note N2). `braindb.sh doctor` starts nothing and stops nothing; it prints ONE line beginning `OK ` or `WARN `, the warn line carrying its fix after ` | `.

```bash
# brain-db (PORTABILITY, 2026-11-27): the seat's local search index. Warn-only: the index is a
# convenience, the files are the master. The tool decides the seat from the tree and starts nothing.
_BDB="$PROJECT_DIR/2_Project_Files/brain-db/braindb.sh"
if [ -x "$_BDB" ]; then
  _BDB_LINE="$("$_BDB" doctor 2>&1 | tail -1)"
  case "$_BDB_LINE" in
    "OK "*)   ok "${_BDB_LINE#OK }" ;;
    "WARN "*) _BDB_LINE="${_BDB_LINE#WARN }"; warn "${_BDB_LINE%% | *}" "${_BDB_LINE#* | }" ;;
    *)        warn "brain-db: doctor gave no verdict" "$_BDB_LINE" ;;
  esac
fi
```

What `doctor` prints, each case exercised in `tests/run.sh` or in the simulation named at the end of this file:

| State | Line | rc |
|---|---|---|
| binaries missing | `WARN brain-db: Postgres 15 binaries missing \| brew install postgresql@15 ...` | 1 |
| seat has no scope file | `OK brain-db: not adopted on this seat (no scope/<seat>.scope)` | 0 |
| no cluster yet | `WARN brain-db: no cluster yet \| run .../braindb.sh up` | 1 |
| cluster version differs | `WARN brain-db: cluster is Postgres X, binaries are Postgres Y \| quarantine ... and run braindb.sh up` | 1 |
| server stopped (the normal resting state) | `OK brain-db: server stopped (on demand; the next search starts it), <data directory>; 0 other file(s) matched the allow-list and are NOT indexed (...)` | 0 |
| index current, nothing missing | `OK brain-db: index current, <data directory> (GREEN, N files ...; 0 other file(s) matched the allow-list and are NOT indexed (...))` | 0 |
| index current, but files that matched the allow-list are not in it (round 5) | `WARN brain-db: index current but it has GAPS, <data directory> \| put right the files braindb.sh check names, then braindb.sh rebuild (AMBER, ...; N other file(s) matched the allow-list and are NOT indexed (unreadable U, not a plain file L, cut C), and K lesson file(s) unreadable or not a plain file ...)` (N or K above 0; round 5b added K) | 1 |
| server stopped, and such files exist (round 5) | `WARN brain-db: server stopped, and N other file(s) matched the allow-list and are NOT indexed (unreadable U, not a plain file L, cut not known without the index), <data directory> \| ...` | 1 |
| index stale | `WARN brain-db: index stale, <data directory> \| braindb.sh rebuild (...)` | 1 |
| another cluster answers on this seat's socket directory | `WARN brain-db: ANOTHER cluster is answering on this seat's socket directory ...` | 1 |
| anything else (a scope error, `WED_AGENT` disagreeing with the tree, the tree changing while it was read: rc 5) | `WARN brain-db: check could not run (rc N) \| <first line>`, or the tool's own REFUSED line | 1 or 2 |

Rollback: remove the block.

## 4. `Launch_Wednesday.command`: `up` at boot (start, check, rebuild when red)

Placed after the rules-card block (line 272 onward today), before the prompt is built. `up` = create the cluster if missing, start it if stopped, run `check`, and `rebuild` only when `check` is red. A failure prints one warning and never blocks the boot. **Round 5 (the third checker's F2): the block carries the count of files that matched the allow-list and are not indexed.** It prints `check`'s first line, which now always holds that count; and when `up` exits 6 (`check` is AMBER: the index is current but has gaps) it prints that line under a warning instead of as success. Round 4b's block printed `check: GREEN ...` over an unreadable daily folder and a skipped ledger. A seat that has not adopted a scope file is passed over silently. Nothing depends on this block having run: every command brings the server up itself.

```bash
# brain-db (WED-170 step 4, PORTABILITY): the seat's local search index. On demand, Unix socket only,
# no service; stopped at wrap. `up` starts it and rebuilds only when the files have moved on (9 to 19 s
# measured under load). The tool takes the seat from this tree's folder name; WED_AGENT, when set, must agree.
# The check line it prints always carries the count of files that matched the allow-list and are NOT indexed.
BRAINDB="$PROJECT_DIR/2_Project_Files/brain-db/braindb.sh"
if [ -x "$BRAINDB" ]; then
  BRAINDB_OUT="$("$BRAINDB" up 2>&1)"; BRAINDB_RC=$?
  BRAINDB_LINE="$(printf '%s\n' "$BRAINDB_OUT" | sed -n '/^check: /p' | tail -1)"
  case "$BRAINDB_RC" in
    0) printf '%s\n' "$BRAINDB_LINE" ;;
    6) echo "⚠ brain-db: the index is current but has GAPS (search will not find what is in these files):"
       printf '%s\n' "$BRAINDB_LINE" ;;
    *) case "$BRAINDB_OUT" in
         *"no scope file for seat"*) : ;;   # this seat has not adopted brain-db: say nothing
         *) echo "⚠ brain-db up FAILED (the brain files are unaffected; search is unavailable this boot):"
            printf '%s\n' "$BRAINDB_OUT" | tail -5 ;;
       esac ;;
  esac
fi
```

The block no longer passes `WED_AGENT`: round 3 made the tree's folder name the seat, so the launcher's `AGENT` variable (line 29, `AGENT="${WED_AGENT:-}"`) is not needed and cannot disagree.

Rollback: remove the block. The cluster stays on the drive, stopped, and harms nothing.

## 5. End of session: stop the server (ruled: stopped at wrap)

Proposed line for the wrap ritual (root `CLAUDE.md` session end, and wherever in `0_Brain/skills/` the wrap is written down):

```
3d. brain-db: `2_Project_Files/brain-db/braindb.sh stop` (the index server is on demand only; the next search or the next boot's launcher starts it again). Say the process check in the wrap: `braindb.sh status` prints `server: STOPPED`.
```

Rollback: remove the line.

## 6. Drive-sync and eject paths: one note line

For the head of `/Volumes/DevMASTER/!SYNC FILES/Sync All Drives.command` (as a comment and an echoed reminder), for the nightly NAS sync's notes in `PORTABILITY.md`, and for any eject instruction:

```
Stop the index before ejecting or syncing the drive (2_Project_Files/brain-db/braindb.sh stop); the data directory is excluded from every copy because it is rebuildable.
```

Not tested by the build seat or the checker: an eject with the server running, or a sync copying the directory.

Rollback: remove the line.

## 7. Sync profiles: the exclusion lines

For every unison profile that copies a seat tree. The one I found is `/Volumes/DevMASTER/!SYNC FILES/devnas.prf`; its `ignore` lines begin at **line 53** (`ignore = Name .git`; round 2 said 48, which is the `# --- Ignores ---` comment, corrected by the checker). I read only its `ignore` lines, not the whole profile, and I did not open the other profiles in that folder, so whoever owns them confirms the list. I have not run unison; the pattern syntax below follows the profile's own `ignore = Name <name>` lines and unison's documented shell-style patterns.

```
# brain-db: a rebuildable search index and its probe, never copied (PORTABILITY brain-db item)
ignore = Path WEDNESDAY/2_Project_Files/brain-db/pgdata-*
ignore = Path TUESDAY/2_Project_Files/brain-db/pgdata-*
ignore = Path FRIDAY/2_Project_Files/brain-db/pgdata-*
ignore = Path WEDNESDAY/2_Project_Files/brain-db/_quarantine_*/_probe_*
```

**Round 4 (the second checker's N12): these are `Path` lines scoped to this lane's folder, not `Name` patterns.** Round 3 proposed `ignore = Name pgdata-*`, `Name pgdata-*.lock` and `Name _probe_*`. A `Name` pattern matches that name anywhere under the synced roots: the checker found `Name _probe_*` already matching 6 unrelated paths under `0_Brain/reference/`, which would silently have stopped reaching the NAS. A `Path` line is matched against the whole path from the profile's root, which in `devnas.prf` is the drive root (its own lines 114 and 115 are written `ignore = Path WEDNESDAY/2_Project_Files/local-model/models`), so each line above can only ever match inside a `brain-db` lane.

- `pgdata-*` in a lane covers `pgdata-<seat>` and its lock file `pgdata-<seat>.lock` (the `*` does not cross a `/`).
- The fourth line covers the dead 39 MB cluster in this lane's quarantine, `_quarantine_2026-11-27/_probe_1127`, left by the round-1 drive proof. It exists only on the Wednesday tree.
- Not run: I have not run unison. The syntax follows the profile's own `Path` lines.

**Until these lines are applied, the next NAS sync copies `pgdata-wednesday/` (about 157 MB), and copies it live if the server is up.** That copy is harmless to the drive and useless at the far end; it is a reason to apply this item with the launcher block, not after it.

This does not conflict with "each external drive will now also hold the dB": each drive's seat builds its own cluster from its own files in a few seconds.

Rollback: remove the lines.

## 8. `PORTS.md`

No line. The server is started with `listen_addresses = ''` (written into the cluster's `postgresql.conf` at `init` and passed again at `start`); the tests and the checker both read `lsof -i` on the server's pid and found nothing. The number 5432 appears only in the socket's file name inside the private socket directory.

## How the two blocks were exercised

The checker ran round 2's blocks in a stub harness under bash 3.2.57 (its file `17_proposals_simulated.txt`). Round 3 changed both blocks, so I re-ran them the same way, with stub `ok` and `warn` functions, against the real cluster and against a tree with no scope file; the output is `evidence/proposals_simulated_round3.txt`. Round 5 changed the launcher block; it and the unchanged `doctor.sh` block were run the same way, the text taken from this file by the stub itself, on scratch trees: nothing missing, the third checker's tree of gaps, a seat with no scope file, and a failing `up`; the output is `evidence/proposals_simulated_round5.txt`, and again after round 5b, with one more case (one unreadable lesson and nothing else wrong), `evidence/proposals_simulated_round5b.txt`. They have still not been run inside the real `doctor.sh` or launcher: this seat edits no shared file.
