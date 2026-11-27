# BRIEF: WED build seat "brain-db" (WED-170 step 4). Build a LOCAL Postgres search index over the Wednesday seat's markdown brain, with its data ON THE DRIVE. A rebuildable index only: the files stay the master. New files only, inside your lane; nothing shared is edited; the round ends at READY FOR QA.

Commissioned by Wednesday (coordinator), 2026-11-27. Model: claude-fable-5-2 (Kam, 2026-11-27: Fable for this project's agents).

## AUTHORITY (verbatim)
- Kam, live board 2026-11-27 11:43:30: "thank you.  I like your recommendations.  Please put this into action for you.  Each external drive will now also hold the dB.  once you finish and test, prepare instructions and send to Tuesday and Friday"
- Kam, live board 2026-11-27 11:43:40: "Decision wed-fleet-structure-v2-where-postgres-runs-1127: c — Local index only". Option c's detail on the card: "no hosted database; rows stay in files and the union tools".
- Wednesday's reading: Postgres runs locally; its data directory lives on the seat's external drive (this seat: DevMASTER); it is an index rebuilt from the files, never the only copy of anything; no hosted database, no spend. This lifts `PORTABILITY.md` item 25's "never start a service on it" for this ONE use, and only in the on-demand form below (no launchd job, no `brew services`).

## READ FIRST (whole)
1. This brief.
2. The design, section 2: `/Volumes/DevMASTER/WEDNESDAY/1_Project_Definition/Architecture/2026-11-27_fleet-structure-v2-design.md`.
3. The census, sections B and E: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_fleet-structure-research/current_structure_census.md`.
4. The video research, sections LINKED ARTEFACTS and COMPARABLE APPROACHES (for the index-over-markdown pattern; do not adopt any product): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_fleet-structure-research/video_postgres_memory.md`.
5. `/Volumes/DevMASTER/WEDNESDAY/PORTABILITY.md` item 25 and `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/PORTS.md` (read, never edit).
6. The lesson pipeline you index (read, never edit): `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/_rules_index.tsv` (its header line says the columns), `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/_rules_index/README.md`, one or two lesson files for their frontmatter shape, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/rules_card.py`.
Never read `4_Credentials/` or `3_Access_Keys/`.

## FACTS MEASURED BY WEDNESDAY TODAY (re-measure each; a difference is a finding)
- `/opt/homebrew/bin/postgres` and `psql` exist, version 15.19 (census E3); no server runs.
- `/Volumes/DevMASTER` is Case-sensitive APFS with "Owners: Disabled" (`diskutil info`). Postgres insists its data directory is owned by the running user with mode 0700: PROVE on a scratch directory ON THE DRIVE that `initdb` and a start work there before anything else. If they do not, STOP with a QUESTION and the exact error; do not move the data off the drive as a workaround.
- Port block 47780 to 47789 is Wednesday's; 47781 to 47785 and 47789 are unassigned (`PORTS.md`).

## WHAT YOU BUILD (all under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/`)

### 1. `braindb.sh` — one tool, seat-aware by `fleet/cockpit/seat_resolve.sh`
- `init`: creates the cluster at `<lane>/pgdata-<seat>/` ON THE DRIVE (a `.gitignore` of your own inside your lane keeps it out of git; prove with `git check-ignore`). Refuses if the directory exists.
- `start` / `stop` / `status`: on demand only, by pid file, never a service. Unix socket only if you can make it work (`listen_addresses = ''`; note the macOS socket path length limit, so the socket directory may need to be a short machine-local path created 0700: that is run-time plumbing, not state). If a TCP port is unavoidable, bind 127.0.0.1 only on ONE unassigned port of the block and put the `PORTS.md` line in `proposed/`. `stop` stops only the pid it started (confirm by data directory, never by name).
- `rebuild`: drops and reloads everything from the files. Idempotent and total. Prints counts per kind and the time taken.
- `check`: compares the set of (path, sha256) on disk with the index; non-zero when they differ, naming up to 20 paths.
- `search "<words>" [--kind K] [--limit N]`: full-text search; prints path, heading, a snippet and the rank. `at <trigger>`: the rows whose rules-index triggers include that word, most reinforced first, as a cross-check against `rules_card.py --at`.
- Refuses to start on a Postgres major version different from the cluster's, saying "rebuild": the index is disposable by design.

### 2. What is indexed (the WEDNESDAY seat's scope ONLY, by an explicit allow-list of paths)
- Lessons `0_Brain/learnings/20*.md`: frontmatter fields as columns (date, type, status, tier), heading, body; the rules-index rows joined on file name (family, triggers, rule line, status, seats).
- This seat's own ledger and its archive: one row per table row (date, headline, rule sentence, body).
- This seat's daily notes `0_Brain/daily/20*.md`: one row per bullet line with its time stamp.
- `0_Brain/skills/*.md`, `0_Brain/identity/*.md`, `0_Brain/people/*.md`, `1_Project_Definition/Architecture/*.md`.
- EXCLUDED, and tested as excluded with planted fixtures: any path containing `tuesday`, `friday`, `laptop_datasec`, `(conflict_on_`, `.pre-`; lessons whose frontmatter tier names another client's project; `0_Brain/dashboard/`, `0_Brain/reference/`, the chat stores, `4_Credentials/`, `3_Access_Keys/`. Another client's text must not be able to enter this index: the allow-list is the mechanism, the exclusions are the test.
- Full text first (`tsvector`, GIN). NO vectors, no extension beyond what ships with Postgres 15, no network, no model call.

### 3. Evidence that it is useful (this decides whether the next step is worth building)
Ten realistic questions a coordinator asks mid-task (write them down first, before running anything; for example "what must be true before I close a pane", "what do I check before telling Kam something is absent", "rules about typed clock times"). For each: the top 5 results from `search`, the top results from `rules_card.py --at` for the nearest trigger, and your honest judgement of which found the right lesson. Report rebuild time, database size on the drive, and query latency. Say plainly if full text is too weak and why.

### 4. `proposed/` — changes to shared files, as PROPOSALS ONLY (you apply none)
The amended text of `PORTABILITY.md` item 25 and a new item for this database (machine-local: the Postgres binaries; on-drive: the data; rebuildable: yes); a `doctor.sh` check (binary present, cluster version matches, `check` clean); the `PORTS.md` line if a port is used; the launcher line that starts it at boot and rebuilds when `check` fails; the root `.gitignore` line if your own is not enough. A rollback line for each. And `INSTRUCTIONS-for-other-seats.md`: the exact steps another seat on another drive and machine would follow, with what must be true first; written to be sent to Tuesday and Friday after the coordinator has tested it.

### 5. `tests/` and `STATUS.md`
- `tests/run.sh` runs against a SCRATCH cluster in your session scratchpad first (never the drive cluster) with fixture files: every exclusion has a planted file that must be absent AND a neighbour that must be present; `check` goes red on a changed fixture and green after `rebuild`; `stop` leaves no process and a second `stop` is a clean no-op; a start on a mismatched version marker refuses. Show each test can fail.
- Only when the scratch tests pass: `init`, `start`, `rebuild`, `check`, the ten questions, `stop` on the real drive cluster. Leave it STOPPED at the end, and say so with the process check.

## HOLDS (the whole session)
- You write ONLY under `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/`, your session scratchpad, and a short machine-local socket directory if needed. No edit to any existing file anywhere. No `git add`, commit, push, stash, checkout or branch; no mail; no board or chat post; no `note_entry`; no `decision_queue`; no cockpit command; no Linear call; no network call; nothing installed (no `brew`, no `pip`): the Postgres 15 already on this Mac and the Python standard library only (use `psql` for database access from scripts).
- Never `rm`: move with `mv -n` into `_quarantine_<date>/` inside your lane. Never `cd` in a shell command (a hook refuses it): absolute paths. No unquoted word starting with `=`. `/usr/bin/grep -i`, with a positive control before you write that something is absent. Never type a clock: use `date`. Never discard stderr.
- No `brew services`, no launchd job, no listener on any address but 127.0.0.1, no password or key written anywhere.
- Other WED build seats may be running in sibling lanes (`2_Project_Files/wake/`, later `2_Project_Files/skills-registry/`). Their directories are not yours.
- If the brief looks wrong or contradicts itself, say so in STATUS.md under QUESTIONS and take the stricter reading. A design choice inside these requirements is yours: make it and write one line saying why.

## STATUS.md (`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/brain-db/STATUS.md`), updated at every stop
First line one of: `WORKING`, `QUESTION` (blocked; one question), `READY FOR QA`. Then: what exists (files with sizes), the test run's output tail and counts, the real-run numbers, the ten-question table, every deviation with its reason, what you did NOT test, QUESTIONS. Write a one-page `DESIGN.md` first, then build without waiting. Stop at READY FOR QA; a separate checker reads your work next.

PROVENANCE:
- Postgres 15.19 present, no server; drive filesystem and Owners flag; port block | census section E3 at /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-27_fleet-structure-research/current_structure_census.md; `diskutil info /Volumes/DevMASTER` run by Wednesday; /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/PORTS.md | read 2026-11-27
- Kam's two messages and option c's detail | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_msgs.sh output and decision_queue.sh show wed-fleet-structure-v2-where-postgres-runs-1127 | read 2026-11-27
- PORTABILITY item 25 wording | census section E3 quoting /Volumes/DevMASTER/WEDNESDAY/PORTABILITY.md | read 2026-11-27 (the seat re-reads the file itself)
