# brain-db on another seat: exact steps

For the Tuesday and Friday coordinators. Written 2026-11-27 by the WED build seat "brain-db" on the Wednesday tree (Kamils-Mac-mini, drive DevMASTER); revised the same day after Wednesday's rulings (`ANSWER-1.md`). **To be sent only after the Wednesday coordinator has tested it.** Nothing here has been run on a Tuesday or Friday tree or on another machine; where a step is unproven there, it says so.

## STEP 1, before anything else: confirm or change your seat's scope file before the first rebuild

**This choice is yours, not Wednesday's and not the build seat's.** Your scope file is the allow-list: a file enters your index only if a line in it says so. A proposal for your seat is at

```
<tree>/2_Project_Files/brain-db/proposed/scope/<seat>.scope
```

It is not live. Until you put a file at `<tree>/2_Project_Files/brain-db/scope/<seat>.scope`, every command refuses with "no scope file for seat". Read the proposal whole, change what is wrong for your seat, then copy it into place (a copy, so the proposal stays for comparison):

```
cp -n "<tree>/2_Project_Files/brain-db/proposed/scope/<seat>.scope" "<tree>/2_Project_Files/brain-db/scope/<seat>.scope"
```

**The boundary the scope must keep (Wednesday's ruling, 2026-11-27):** the index holds only files your seat is already allowed to read at boot; no file that belongs to another seat or another client's project enters it. Rows inside your own files that name the other client stay, because shared rules name both clients; nothing is dropped by client name.

**What each line does:**

| Line | What it does | What to check for your seat |
|---|---|---|
| `seat <name>` | Ties the file to one seat. The tool refuses a scope file whose `seat` is not the seat your tree resolves to. | It is your seat. |
| `own_clients <words>` | A lesson whose frontmatter tier is a project tier (`P-<Client>/<Project>`) is indexed only if the tier names one of these. | Tuesday proposal: `datasec general`. Friday proposal: `secuura datasec general`. |
| `deny_clients <words>` | A lesson whose tier names one of these is excluded, and a section marked `<!-- tier: P-<that client>/... -->` inside an indexed lesson is dropped. | Tuesday proposal: `secuura`. **Friday proposal: no such line**, because Friday works for both clients. That is the build seat's guess, not a ruling: decide it. |
| `allow rules CLAUDE.md` and `allow rules 0_Brain/CLAUDE.md` | Indexes your tree's two rules files, one row per numbered rule or heading section. A file at the tree root can only be named exactly. | That these two files in YOUR tree are the rules your seat boots on. |
| `allow lesson 0_Brain/learnings/20*.md` | Indexes lesson files. Which lessons is decided by content, not by name: a lesson is left out when its tier fails the two lines above, or when it has rows in the rules index and every row's `seats` column names only other seats. A lesson with no index row is decided by tier alone. | Nothing to change; read the "NOT indexed" list in step 4. |
| `allow rules_index 0_Brain/learnings/_rules_index.tsv` | Loads the rules index: it feeds `at <trigger>` and decides lessons as above. | - |
| `allow ledger <file>` (two lines) | Indexes YOUR ledger and its archive, one row per table row. | Tuesday: `_ledger_laptop_datasec.md` and `_ledger_laptop_datasec_archive.md` (the historical file name). Friday: `_ledger_friday.md` and `_ledger_friday_archive.md`. |
| `allow daily <folder>/20*.md` | Indexes YOUR daily notes, one row per bullet line. | Tuesday: `0_Brain/daily_tuesday/`. Friday: `0_Brain/daily_friday/`. |
| `allow skill`, `allow identity`, `allow people`, `allow architecture` | Index those folders' `.md` files, split at headings. | Whether your seat reads all four at boot; delete a line you do not want. |
| `deny_path (conflict_on_` and `deny_path .pre-` | Sync conflict copies and backups are excluded wherever that text appears in the path. | Keep. |
| `deny_seat_word <word>` | Another seat's own records: the word excludes a path when it is in a FOLDER name (any kind) or in the FILE name of a ledger or daily note. It never excludes a lesson, skill or architecture file by its name. | Tuesday proposal: `friday`, `wednesday`. Friday proposal: `tuesday`, `wednesday`, `laptop_datasec`. The Wednesday seat's own ledger and daily folder carry no seat word in their names (`_ledger.md`, `daily/`); they are kept out of your index by not being on your allow-list. |

Things the scope file cannot do, by design: name anything under `4_Credentials/`, `3_Access_Keys/`, `0_Brain/dashboard/` or `0_Brain/reference/`; use `..`, an absolute path, a wildcard in a folder name, or a pattern that does not end in `.md`. Each is refused when the file is loaded.

## What you get

A local Postgres 15 search index over your own seat's markdown brain, stored on your drive in `2_Project_Files/brain-db/pgdata-<seat>/`. It is rebuilt from the files in seconds and can be thrown away at any time. It opens no network port, runs no service and holds no password. Authority: Kam, live board 2026-11-27 11:43, "Each external drive will now also hold the dB"; decision `wed-fleet-structure-v2-where-postgres-runs-1127` = c, local index only.

```
braindb.sh search "what must be true before I close a pane"
braindb.sh at pane --top 10
```

## What must be true first

| # | Requirement | How to check | On the Wednesday seat today |
|---|---|---|---|
| 1 | Your tree holds `2_Project_Files/brain-db/` (it arrives by git once the coordinator commits it) | `ls <tree>/2_Project_Files/brain-db/braindb.sh` | present |
| 2 | Postgres 15 binaries on this Mac | `/opt/homebrew/opt/postgresql@15/bin/postgres --version` prints 15.x | 15.19 |
| 3 | `python3` on PATH (standard library only; the file parses under 3.9.6, it has run only under 3.14.10) | `python3 --version` | 3.14.10 |
| 4 | Your tree's folder name, or `WED_AGENT`, resolves to your seat | `braindb.sh status` prints `seat: <yours>` on its first line | wednesday |
| 5 | The drive accepts a Postgres data directory | step 3 below is the proof; it worked on a Case-sensitive APFS volume with Owners Disabled | proved |
| 6 | No Postgres service is configured to start by itself | `brew services list` shows `postgresql@15` as `none` | not re-measured by the build seat (the census of 2026-11-27 read `none`) |

If requirement 2 fails: `brew install postgresql@15` is an install, so it needs your coordinator's or Kam's word under your own rules first.

## Steps 2 to 6

All commands are run from anywhere, with absolute paths. `<tree>` is your seat's tree root. `B` stands for `<tree>/2_Project_Files/brain-db/braindb.sh`.

**2. Run the tests against a scratch cluster** (they never touch your drive cluster):

```
mkdir -p "<your session scratchpad>"
/bin/bash "<tree>/2_Project_Files/brain-db/tests/run.sh" "<your session scratchpad>"
```

Expected last line: `RESULT: 295 passed, 0 failed`. Two assertions in section 12 ("seat tuesday with no scope/tuesday.scope is refused" and the line after it) describe a tree where Tuesday has NOT adopted a scope. **On a tree where `scope/tuesday.scope` already exists, those two fail**; that is the test describing the Wednesday tree, not a fault in your setup. Any other failure: stop and report it with the run directory the last line names.

**3. Build:**

```
B up          # creates pgdata-<seat>/ on the drive if missing, starts the server, rebuilds if check is red
B rebuild     # run it once by hand as well, to read its report
B check       # must print GREEN
```

**4. Read the `rebuild` report before trusting the index.** The block headed "matched an allow line but NOT indexed" lists every file the exclusions removed, with the reason. If a file you expected is there, or a file you did not expect is missing from it, stop and tell your coordinator: that is your scope file being wrong for your seat.

On the Wednesday seat the report reads: 419 files, 22,246 search rows, about 4.6 s; 32 files not indexed (26 lessons whose every rules-index row names only other seats, 4 sync conflict copies, 2 lessons of another client's project). The cluster takes about 157 MB on the drive.

**5. Confirm the git ignore** (the cluster must never be committed):

```
git -C "<tree>" check-ignore -v "<tree>/2_Project_Files/brain-db/pgdata-<seat>/x"
```

It must print a line naming `2_Project_Files/brain-db/.gitignore`.

**6. Use it, and stop it at wrap.**

```
B search "<words>"                  # rules and lessons first, then up to two incident rows
B search "<words>" --kind ledger    # one kind: rules lesson ledger daily skill identity people architecture
B search "<words>" --all            # every kind in one order by score
B at <trigger> [--top N]
B status
B stop                              # at the end of the session, and before ejecting or syncing the drive
```

`search`, `at`, `check` and `rebuild` start the server themselves when it is down, so nothing depends on a launcher having run. `stop` only ever stops the process that was started with your own data directory; it refuses anything else. A second `stop` is a no-op.

## How to read a result

- Every result line carries its kind in square brackets: `[rules]`, `[lesson, live, ×14]`, `[ledger, 2026-09-27]`. A `[rules]` row is your own rules file; a `[lesson]` row prints the lesson's rules-index line under it; `[ledger]` and `[daily]` rows are what happened, not the rule.
- **`WEAK MATCH`** after the results means the best one scored under 0.035. Treat the list as near neighbours, not as the answer: reword with the rule's own words, or use `at <trigger>`. The threshold was fitted on ten questions on the Wednesday brain; on those it flagged all three wrong first results and also two right ones. It is a prompt to check, not a verdict.
- **`NO MATCH`** means none of the words is in the index at all.
- No warning does not mean the first result is right. It means the words matched well.

## What can go wrong, and what to do

| You see | Meaning | Do |
|---|---|---|
| `check: RED ... changed since the last rebuild` | files moved on since the last rebuild (your daily note changes all day, so this is normal) | `B rebuild` (about 5 s) |
| `no index yet ... building it now` | the server was stopped uncleanly (crash, drive pulled) and the unlogged tables came back empty, or it was never built | nothing: `search` and `at` rebuild it themselves |
| `REFUSED: the cluster ... was made by Postgres X and the binaries here are Postgres Y ... rebuild` | the drive was plugged into a Mac with a different Postgres major version | move `pgdata-<seat>/` into `<lane>/_quarantine_<date>/` with `mv -n`, then `B up`. Never delete it. |
| `REFUSED: the socket directory ... is not mode 700` or `not owned by this user` | something else made `/tmp/wed-braindb-<uid>-<seat>` | report it; do not chmod another user's directory. `BRAINDB_SOCKDIR=<another short private directory>` is the override, and it must then be set on every call |
| `no scope file for seat` | step 1 not done | step 1 |
| `the server did not start` followed by log lines | read them; the log is `pgdata-<seat>/braindb-server.log` | report with the lines |

## Limits you should know before relying on it

1. **It is word search, not meaning search.** It finds a lesson when your question shares words with the lesson, its file name or its rules-index line. "cleaning up" put the lesson named "cleanup means quarantine" third, behind two neighbours. When you know the moment (pane, brief, merge), `at <trigger>` and `rules_card.py --at <trigger>` remain the surer route.
2. **A stale index answers without saying so.** `search` and `at` build a missing index but do not rebuild one that is merely behind the files; `check` tells you, and the launcher's `up` rebuilds at boot.
3. **`at` weights count only your own indexed ledgers.** `rules_card.py` counts every seat's ledger, so the order differs between the two. On the Wednesday seat the two list exactly the same 802 rule lines.
4. **Only your own tree's rules files are indexed.** A rule that lives in the workspace file one level above your tree is not in the index. On the Wednesday seat, "a deploy failed, can I skip it" still does not find the hard rule, because that rule's sentence is in the workspace `CLAUDE.md`; the tool prints `WEAK MATCH` there.
5. **Nothing writes to the brain.** The tool only reads your files. Corrections go in the files; the index follows at the next rebuild.

## The shared-file changes that go with it

`proposed/PROPOSALS.md` holds the text for `PORTABILITY.md`, `doctor.sh`, the launcher, the wrap line, the drive-sync and eject note and the sync-profile exclusion. They are proposals to the Wednesday coordinator; a seat does not apply them on its own tree.
