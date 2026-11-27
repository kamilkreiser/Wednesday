# brain-db: proposed changes to shared files

Written 2026-11-27 by the WED build seat "brain-db"; revised the same day for round 2 (`ANSWER-1.md` ruling 3: on demand, stopped at wrap). **None of these is applied.** Each has a rollback line. The coordinator applies or drops them.

| Shared file | Change proposed | Needed for the tool to work? |
|---|---|---|
| `PORTABILITY.md` item 25 | one sentence amended | no, it is the record |
| `PORTABILITY.md` new item 32 | new item | no, it is the record |
| `2_Project_Files/doctor.sh` | one check block | no |
| `Launch_Wednesday.command` | one block: `braindb.sh up` (start, check, rebuild when red) | no: `search`, `at`, `check` and `rebuild` bring the server up themselves |
| End-of-session ritual | one line: `braindb.sh stop` | no, but it is what makes "stopped at wrap" true |
| Drive-sync and eject paths | one note line (item 6) | no |
| Sync profiles | three ignore lines (item 7) | no |
| `2_Project_Files/PORTS.md` | **none**: Unix socket only, no port bound | - |
| root `.gitignore` | **none**: the lane's own `.gitignore` is enough (`git check-ignore` proved it for `pgdata-wednesday/`, `_probe_*/`, `_quarantine_*/`; control `braindb.sh` rc 1) | - |

---

## 1. `PORTABILITY.md` item 25: amended text

Only the "Machine-local" bullet's last sentence and the "No service" bullet change. Proposed replacement for those two bullets:

```
- **Machine-local:** `/opt/homebrew/opt/postgresql@15` (15.19_1). It pulled `icu4c@79` and `krb5`, and UPGRADED `libunistring` 1.4.2 -> 1.5 (old keg kept). Brew also created a non-started default cluster dir `/opt/homebrew/var/postgresql@15` (~38 MB): nothing uses it; never start a server on THAT directory.
- **No service:** no `brew services` job, no launchd plist; every suite/gate starts its own cluster on a private data dir + 127.0.0.1 port and stops it by pid. **One named exception (Kam, live board 2026-11-27 11:43, decision wed-fleet-structure-v2-where-postgres-runs-1127 = c):** the seat's brain search index (item 32) is started on demand by `2_Project_Files/brain-db/braindb.sh` from a data directory on the drive, on a Unix socket only, and stopped at wrap. It is still not a service: nothing starts it but that tool, and that tool stops it by pid.
```

Rollback: restore the two bullets to their 2026-11-04 wording (the file's git history holds it).

## 2. `PORTABILITY.md` new item 32

```
## 32. brain-db: the seat's local search index (Postgres 15, data ON THE DRIVE) (2026-11-27)
A full-text index over the files this seat is already allowed to read at boot (its two rules files, lessons, the rules index, the seat's ledger and archive, the seat's daily notes, skills, identity, people, architecture). No file that belongs to another seat or another client's project enters it. Kam, live board 2026-11-27 11:43: "Each external drive will now also hold the dB"; decision wed-fleet-structure-v2-where-postgres-runs-1127 = c (local index only). Code and design: `2_Project_Files/brain-db/` (`DESIGN.md`).
- **Machine-local:** the Postgres 15 binaries (item 25: `brew install postgresql@15`) and `python3`. A socket directory `/tmp/wed-braindb-<uid>-<seat>` (mode 700, created by the tool, holds no state).
- **On-drive:** the cluster, `2_Project_Files/brain-db/pgdata-<seat>/` (about 160 MB for the Wednesday seat; gitignored by the lane's own `.gitignore`).
- **Rebuildable: yes.** The files are the master. `braindb.sh rebuild` reloads everything in about 5 seconds; losing or quarantining `pgdata-<seat>/` loses nothing.
- **On demand, no service, no port:** `search`, `at`, `check` and `rebuild` start the server themselves when it is down; the launcher runs `braindb.sh up` at boot; the wrap runs `braindb.sh stop`. Unix socket only (`listen_addresses = ''` is in the cluster's own config). No password or key exists; access is the logged-in user through the socket.
- **Stop the index before ejecting or syncing the drive; the data directory is excluded from every copy because it is rebuildable.** (`braindb.sh stop`. A drive pulled under a running server costs only a rebuild.)
- **New Mac / another drive:** `brew install postgresql@15`, then `braindb.sh up`. A cluster made by a different Postgres major version is refused at `start` with the word "rebuild": move `pgdata-<seat>/` into a `_quarantine_<date>/` folder and run `braindb.sh up`.
- **Per seat:** one cluster per seat (`pgdata-wednesday`, `pgdata-tuesday`, `pgdata-friday`), each built only through that seat's own confirmed allow-list `2_Project_Files/brain-db/scope/<seat>.scope`. A seat with no scope file is refused.
```

Rollback: remove item 32.

## 3. `2_Project_Files/doctor.sh`: one check block

Placed after the existing `postgresql@15 keg` check (line 470 today). It uses doctor's own `ok` / `warn`, `$PROJECT_DIR` and `$_DOC_AGENT`. `BRAINDB_NO_AUTOSTART=1` keeps `check` from starting the server: a preflight must start nothing.

```bash
# brain-db (PORTABILITY 32, 2026-11-27): the seat's local search index. Warn-only: the index is a
# convenience, the files are the master. Three things: the binaries, the cluster's version, check.
_BDB="$PROJECT_DIR/2_Project_Files/brain-db"
if [ -x "$_BDB/braindb.sh" ] && [ -f "$_BDB/scope/$_DOC_AGENT.scope" ]; then
  _BDB_PG="/opt/homebrew/opt/postgresql@15/bin/postgres"
  _BDB_DATA="$_BDB/pgdata-$_DOC_AGENT"
  if [ ! -x "$_BDB_PG" ]; then
    warn "brain-db: Postgres 15 missing" "brew install postgresql@15 (PORTABILITY 25, 32)"
  elif [ ! -f "$_BDB_DATA/PG_VERSION" ]; then
    warn "brain-db: no cluster yet" "run 2_Project_Files/brain-db/braindb.sh up (PORTABILITY 32)"
  elif [ "$(tr -d ' \n' < "$_BDB_DATA/PG_VERSION")" != "$("$_BDB_PG" --version | sed -E 's/^[^0-9]*([0-9]+).*/\1/')" ]; then
    warn "brain-db: cluster version differs" "cluster $(tr -d ' \n' < "$_BDB_DATA/PG_VERSION") vs binaries $("$_BDB_PG" --version | awk '{print $3}'): quarantine pgdata-$_DOC_AGENT and run braindb.sh up"
  else
    _BDB_OUT="$(WED_AGENT="$_DOC_AGENT" BRAINDB_NO_AUTOSTART=1 "$_BDB/braindb.sh" check 2>&1)"; _BDB_RC=$?
    case "$_BDB_RC" in
      0) ok "brain-db index current ($(printf '%s' "$_BDB_OUT" | head -1 | sed -E 's/^check: //'))" ;;
      3) ok "brain-db: server stopped (on demand; the next search starts it)" ;;
      *) warn "brain-db: index stale" "$(printf '%s' "$_BDB_OUT" | head -1) -> braindb.sh rebuild" ;;
    esac
  fi
fi
```

`check` exits 0 green, 1 red (stale), 3 when the server is not answering and self-start is off. A stopped server is the normal resting state now, so rc 3 is an `ok` line, not a warning. The block was NOT run inside `doctor.sh` (this seat edits no shared file); the three exit codes were exercised through `braindb.sh` in `tests/run.sh`.

Rollback: remove the block.

## 4. `Launch_Wednesday.command`: `up` at boot (start, check, rebuild when red)

Placed after the rules-card block (line 272 onward today), before the prompt is built. It uses the launcher's own `$PROJECT_DIR` and `$AGENT`. `up` = create the cluster if missing, start it if stopped, run `check`, and `rebuild` only when `check` is red. A failure prints one warning and never blocks the boot. Nothing depends on this block having run: every command brings the server up itself.

```bash
# brain-db (WED-170 step 4, PORTABILITY 32): the seat's local search index. On demand, Unix socket
# only, no service; stopped at wrap. `up` starts it and rebuilds only when the files have moved on (about 5 s).
BRAINDB="$PROJECT_DIR/2_Project_Files/brain-db/braindb.sh"
if [ -x "$BRAINDB" ] && [ -f "$PROJECT_DIR/2_Project_Files/brain-db/scope/${AGENT:-wednesday}.scope" ]; then
  if BRAINDB_OUT="$(WED_AGENT="${AGENT:-wednesday}" "$BRAINDB" up 2>&1)"; then
    printf '%s\n' "$BRAINDB_OUT" | tail -1
  else
    echo "⚠ brain-db up FAILED (the brain files are unaffected; search is unavailable this boot):"
    printf '%s\n' "$BRAINDB_OUT" | tail -5
  fi
fi
```

Note for whoever applies it: the launcher sets `AGENT="${WED_AGENT:-}"` at line 29; I did not read how an empty value is later resolved to a seat name, so the block falls back to `wednesday` only where `AGENT` is empty. On a TUESDAY or FRIDAY tree, check that `$AGENT` holds the seat name at that point, or drop the explicit `WED_AGENT=` and let `braindb.sh` resolve the seat from the tree name itself (it does).

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

Not tested by the build seat: an eject with the server running, or a sync copying the directory.

Rollback: remove the line.

## 7. Sync profiles: the exclusion line itself

For every unison profile that copies a seat tree. The one I found and read the ignore syntax from is `/Volumes/DevMASTER/!SYNC FILES/devnas.prf` (lines 48 onward use `ignore = Name <name>`); I read only its `ignore` lines, not the whole profile, and I did not list or open the other profiles in that folder, so whoever owns them should confirm the list.

```
# brain-db: a rebuildable search index, never copied (PORTABILITY 32)
ignore = Name pgdata-wednesday
ignore = Name pgdata-tuesday
ignore = Name pgdata-friday
```

This does not conflict with "each external drive will now also hold the dB": each drive's seat builds its own cluster from its own files in about 5 seconds. A synced copy would be a second, stale index nobody asked for, and a copy taken from under a running server is not a usable cluster at all.

Rollback: remove the four lines.

## 8. `PORTS.md`

No line. The server is started with `listen_addresses = ''` (written into the cluster's `postgresql.conf` at `init` and passed again at `start`), and the tests assert with `lsof -i` that the process holds no network socket. The number 5432 appears only in the socket's file name (`.s.PGSQL.5432`) inside the private socket directory.
