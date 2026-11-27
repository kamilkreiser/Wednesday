# brain-db: design (one page)

First written 2026-11-27 11:55 AEDT by the WED build seat "brain-db", before any code. Revised the same day for round 2 (`ANSWER-1.md`: four rulings, three changes); revised points are marked **R2**. Brief: `BRIEF.md` in this directory.

## What it is
A local Postgres 15 cluster whose data directory sits on the drive (`pgdata-<seat>/` in this lane), holding a full-text index of the seat's markdown brain. The files stay the master. The index can be thrown away and rebuilt at any time; nothing is ever written back to the brain.

## The boundary (R2, Wednesday's ruling, in her words)
**The index holds only files this seat is already allowed to read at boot; no file that belongs to another seat or another client's project enters it.** Rows inside this seat's own files that NAME the other client stay, because shared rules name both clients. Nothing is dropped by client name. The boundary is drawn on files, by path and by tier, not on words.

## Pieces
| File | Job |
|---|---|
| `braindb.sh` | The one tool. Resolves the seat with `fleet/cockpit/seat_resolve.sh`, owns the cluster life cycle (`init`, `start`, `stop`, `status`, `up`) and hands `rebuild`, `check`, `search`, `at` to the indexer. |
| `braindb_index.py` | Standard-library Python. Reads the scope file, walks the allow-list, parses, and talks to the database through `psql` only. |
| `scope/<seat>.scope` | The allow-list for one seat, as a plain reviewable text file. A seat with no scope file is refused. Only `scope/wednesday.scope` ships live; the other two seats' files sit in `proposed/scope/` until their own coordinator confirms or changes them. |
| `tests/run.sh` | Builds a fixture tree and a scratch cluster outside the drive cluster and proves the exclusions, `check`, `stop`, the version refusal and the round-2 behaviours. |

## Choices, one line of why each
1. **Unix socket only, no TCP port.** `listen_addresses = ''` is written into `postgresql.conf` at `init`, so even a bare `pg_ctl start` opens no network listener. No `PORTS.md` line is needed.
2. **Socket directory `/tmp/wed-braindb-<uid>-<seat>`, mode 0700.** The macOS socket path limit is 104 bytes; a drive path on another seat may be longer, so one short rule serves every seat. The tool refuses a socket directory that is a symlink, not owned by the user, or not 0700. It holds no state.
3. **Peer authentication, host connections rejected.** No password or key exists anywhere.
4. **Unlogged tables.** After an unclean stop Postgres empties them, `check` goes red, and `rebuild` restores them. That is the disposable-index contract, and it avoids write-ahead-log volume on the external drive.
5. **`rebuild` is one transaction** (drop schema, create, `COPY`, index, commit). A failed rebuild leaves the previous index intact; a second run gives the same rows.
6. **The allow-list is a file, the exclusions are tested.** Each `allow` line is one directory plus one file-name pattern (no recursion, no symlinks, `.md` only, `.tsv` for the rules index). Paths under `4_Credentials/`, `3_Access_Keys/`, `0_Brain/dashboard/` and `0_Brain/reference/` are refused in code even if a scope file names them. **R2:** a file at the tree root may be allowed only by its exact name and only as kind `rules`.
7. **Which lessons (R2).** A lesson is decided by content, never by its file name:
   - excluded when its frontmatter tier names a denied client, is a project tier naming none of the seat's own clients, or is an unknown value (`W`, `M`, `MIXED` and untagged are in, as in `boot_digest.py`);
   - excluded when it has rows in the rules index and every row's `seats` column names only other seats; a lesson with no row is decided by tier alone;
   - inside an indexed lesson, a section marked `<!-- tier: P-<Client>/... -->` for a denied client is dropped, mirroring `boot_digest.py`.
   The tier test is applied first and the seats test second; a lesson of another client's project stays out even if a row scoped it `all` (my reading of ruling 1 against ruling 2; no such lesson exists today).
8. **Another seat's own records (R2).** A `deny_seat_word` (for this seat: `tuesday`, `friday`, `laptop_datasec`) excludes a path when the word is in a folder name, for any kind, or in the file name of a record kind (ledger, daily note). It never excludes a lesson, skill or architecture file by its name. `deny_path` (`(conflict_on_`, `.pre-`) still applies anywhere in the path.
9. **Search units.** Lessons, skills, identity, people and architecture files are split at headings and the best section per file is shown. Ledger rows and daily-note lines are one unit each. **R2:** a rules file (`CLAUDE.md`, `0_Brain/CLAUDE.md`) gives one row per numbered rule and one row for each heading section's remaining text. Typed tables (`lessons`, `rules`, `ledger_rows`, `daily_rows`) carry the columns the brief names; one table `chunks` carries the `tsvector` and the GIN index.
10. **Ranking.** Postgres full text has no rarity weighting, so common words would dominate. The query is split into its lexemes; each is weighted by a rarity score computed at rebuild from `ts_stat`, summed over `ts_rank`, and multiplied by the square of the share of the query's rarity mass the row matched. Title and file slug weigh most, then the section heading and the lesson's rules-index line, then the body. Rows whose rule is dead or superseded are halved and labelled. **R2:** the score is divided by the query's total rarity mass, which changes no ordering but makes it comparable between queries, so one threshold can call a match weak.
11. **What a search shows (R2).** With no `--kind`: knowledge first (rules files, lessons, skills, identity, people, architecture, by score), then up to two incident rows from the ledger and daily notes under their own heading. A rules-file row whose match is not weak goes ahead of every lesson; a weak one competes on score like any other row, so a rules file cannot become the new confident wrong neighbour. `--all` gives the old single mixed order; `--kind K` gives one kind. Every result line carries its kind. When the best result scores under 0.035 the tool prints `WEAK MATCH` and points at `at <trigger>`; with no match at all it prints `NO MATCH`.
12. **`at <trigger>` weights come from this seat's indexed ledgers only.** `rules_card.py` counts citations in every seat's ledger; reading the other seats' ledgers would break the allow-list. The set of rules matches the card; the order may differ.
13. **`check` also compares the indexer's and the scope file's own hashes** with those stored at rebuild, so a changed parser or allow-list reads as stale.
14. **Version guard.** `start` compares `pgdata/PG_VERSION` with the major version of the binaries and refuses with the word "rebuild" when they differ.
15. **Tests cannot touch the drive cluster.** Setting `BRAINDB_ROOT` (a fixture tree) without `BRAINDB_PGDATA` is refused.
16. **On demand, stopped at wrap (R2).** `rebuild`, `check`, `search` and `at` bring the server up themselves when it is down (and create the cluster when there is none); `search` and `at` also build the index when there is none. They do not rebuild a merely stale index: that costs five seconds and is `check`'s and the launcher's job. `BRAINDB_NO_AUTOSTART=1` turns the self-start off, for `doctor.sh`, which must start nothing.

## Not in this round
Vectors, any extension, any network call, any service or launchd job, any file outside the WEDNESDAY tree, any write outside this lane (other than the socket directory and the session scratchpad).
