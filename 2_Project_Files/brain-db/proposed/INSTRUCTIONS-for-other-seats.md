# brain-db on another seat: exact steps

For the Tuesday and Friday coordinators. Written 2026-11-27 by the WED build seat "brain-db" on the Wednesday tree (Kamils-Mac-mini, drive DevMASTER); revised after Wednesday's rulings (`ANSWER-1.md`) and after the independent checker's findings (`ANSWER-3.md`). **To be sent only after the Wednesday coordinator has tested it.** Nothing here has been run on a real Tuesday or Friday tree or on another machine; the build seat and the checker each ran it on a fixture tree named TUESDAY on this Mac. Where a step is unproven on your machine, it says so.

## STEP 1, before anything else: confirm your seat's scope file

Round 4 changed what this step is. **You adopt by CONFIRMING your seat's scope file. Nothing in it is changed to taste.** What a seat may index is a closed table in the code (`braindb_index.py`, the block headed "ROUND 4: what an allow line may ask for"); a scope file can leave a line out, and it can never add anything the table does not hold. A line that asks for anything else is REFUSED when the file is loaded, with exit code 2, before any cluster is created or any server is started.

Your proposed file is `proposed/scope/<seat>.scope`. It is not live. Until a file sits at `<tree>/2_Project_Files/brain-db/scope/<seat>.scope`, every command refuses with "no scope file for seat" and creates nothing.

1. Read the proposal whole.
2. Confirm the two lines that are yours to confirm (table below). If one is wrong, do not edit it yourself: tell your coordinator, because the same fact is in the code's table.
3. Copy it: `cp -n proposed/scope/<seat>.scope scope/<seat>.scope`.

| Line | What it does | What you confirm |
|---|---|---|
| `seat <name>` | Ties the file to one seat. A file whose `seat` is not your tree's seat is refused. | It is your seat. |
| `own_clients <words>` | The clients whose PROJECT lessons (`tier: P-<Client>/<Project>`) your seat may index. | Tuesday proposal: `datasec general`. Friday proposal: `secuura datasec general`, because Friday works for both clients. **That is the build seat's reading, not a ruling: Kam or your coordinator confirms it.** |

Every `allow` line in the proposal is already the only thing the table permits for your seat:

| Kind | The one place it may come from, for your seat |
|---|---|
| `rules` | `CLAUDE.md` and `0_Brain/CLAUDE.md` of your own tree, named exactly |
| `lesson` | `0_Brain/learnings/` (file names that start with a date) |
| `rules_index` | `0_Brain/learnings/_rules_index.tsv` |
| `ledger` | your seat's own two ledger files, named exactly. Wednesday: `_ledger.md`, `_ledger_archive.md`. Tuesday: `_ledger_laptop_datasec.md` and its `_archive`. Friday: `_ledger_friday.md` and its `_archive`. |
| `daily` | your seat's own daily folder, as `tools/seat_note.sh` resolves it (`0_Brain/daily`, `0_Brain/daily_tuesday`, `0_Brain/daily_friday`); only files named as a plain date |
| `pickup` | your seat's own pickup and week files in `0_Brain/tasks/`, named exactly (no proposal carries this line; add it only with your coordinator's word) |
| `skill`, `identity`, `people`, `architecture` | `0_Brain/skills/`, `0_Brain/identity/`, `0_Brain/people/`, `1_Project_Definition/Architecture/`; you may delete a line you do not want |

So a Tuesday or Friday tree cannot index the Wednesday seat's ledger, daily notes or pickup file by any line, and the reverse. `(conflict_on_` copies and `.pre-` backups are left out by the code whatever the file says.

**Which lessons enter: QUALIFY OR STAY OUT.** A lesson is indexed only when it positively qualifies on every clause. Anything else is left out and NAMED, with the clause it failed, by `rebuild`, `check` and `doctor`:

- (a) it has exactly one row in the rules index whose key is exactly its file name, and no line of the rules index that could not be read so much as holds its name;
- (b) that row's seats cell is `all` or names your seat;
- (c) its frontmatter is one block opened on line 1 by `---` and closed by `---`, every line in it a plain `key: value`, with exactly one `tier:` line whose value is `W`, `M`, or `P-<one of your own clients>/<project>`. No tier, `MIXED`, or any other value stays out;
- (d) nowhere in its text is there an HTML comment (a section marker in any spelling is one), a tier-like line, or a numeric character reference;
- (t) it is plain UTF-8 text with Latin letters and no control or invisible characters;
- (f) it is a plain regular file: not a symlink, not hard-linked, readable.

This is deliberately strict. It leaves out real lessons you might want (on the Wednesday seat: see step 4), and the fix for a lesson that should be in is in the lesson file or the rules index, never in the tool.

**What keeps another client's material out, said plainly (round 4b, `ANSWER-7.md`).** Three things, each DECLARED BY A PERSON: the lesson's row in the rules index (which seat it is for), its `tier:` line (whose it is), and a section marker (this part is another client's). The tool reads those three strictly and reads nothing else. Nothing reads meaning, and there is no list of client names: one was built in round 4, it left out 55 of the Wednesday seat's own lessons for mentioning the other client in passing, and it still could not see a project named without its client or an abbreviation. So a lesson about another client's work that is tagged `W` or `M`, scoped to this seat and carries no marker WILL be indexed. The remedy is to tag it with its project tier or mark the section, in the lesson file; it is not a word list, and one should not be put back.

There is no `deny_clients` line any more. A scope file that carries one is refused, so that no file promises a protection the tool does not give.

## What you get

A local Postgres 15 search index over your own seat's markdown brain, stored on your drive in `2_Project_Files/brain-db/pgdata-<seat>/`. It is rebuilt from the files in seconds and can be thrown away at any time. It opens no network port, runs no service and holds no password. Authority: Kam, live board 2026-11-27 11:43, "Each external drive will now also hold the dB"; decision `wed-fleet-structure-v2-where-postgres-runs-1127` = c, local index only.

```
braindb.sh search "close a pane"
braindb.sh at pane --top 10
```

## What must be true first

| # | Requirement | How to check | On the Wednesday seat today |
|---|---|---|---|
| 1 | Your tree holds `2_Project_Files/brain-db/` (it arrives by git once the coordinator commits it) | `ls <tree>/2_Project_Files/brain-db/braindb.sh` | present |
| 2 | Postgres 15 binaries on this Mac | `/opt/homebrew/opt/postgresql@15/bin/postgres --version` prints 15.x (the tool also looks in `/usr/local/opt/postgresql@15/bin` and on PATH) | 15.19 |
| 3 | `python3` on PATH (standard library only; the round 4 suite passes under 3.9.6 and 3.14.10) | `python3 --version` | 3.14.10 |
| 4 | **Your tree's FOLDER is named for your seat** (`TUESDAY` or `FRIDAY`). The tool takes the seat from the folder name. If `WED_AGENT` is set in your shell it must say the same seat; a disagreement, or any other folder name, is refused. | `braindb.sh status` prints `seat: <yours>` on its first line | wednesday |
| 5 | The drive accepts a Postgres data directory | step 3 below is the proof; it worked on a Case-sensitive APFS volume with Owners Disabled | proved |
| 6 | No Postgres service is configured to start by itself | `brew services list` shows `postgresql@15` as `none` | not re-measured by the build seat (the census of 2026-11-27 read `none`) |

If requirement 2 fails: `brew install postgresql@15` is an install, so it needs your coordinator's or Kam's word under your own rules first.

## Steps 2 to 6

All commands are run from anywhere, with absolute paths. `<tree>` is your seat's tree root. `B` stands for `<tree>/2_Project_Files/brain-db/braindb.sh`.

**2. Run the tests against scratch clusters** (they never touch your drive cluster; they copy the tool into the scratch directory and run that copy):

```
mkdir -p "<your session scratchpad>"
/bin/bash "<tree>/2_Project_Files/brain-db/tests/run.sh" "<your session scratchpad>"
```

Expected last line: `RESULT: 483 passed, 0 failed`. The result no longer depends on which scope files your tree has adopted. Any failure: stop and report it with the run directory the last line names. It takes under a minute.

**3. Build:**

```
B up          # creates pgdata-<seat>/ on the drive if missing, starts the server, rebuilds if check is red
B rebuild     # run it once by hand as well, to read its report
B check       # must print GREEN, and names the data directory it is reporting on
```

**4. Read the `rebuild` report before trusting the index.** It lists every lesson that was LEFT OUT, by name, under the clause it failed; every other file that matched an allow line and was not indexed, with the reason; every rules-index line that could not be read; and anything unreadable or cut. Its LAST line gives the count left out by each clause, and `check` and `doctor` print the same count afterwards, so a lesson that drops out later is visible without re-reading this report. If a lesson you expected is in the left-out list, the list tells you which clause to look at in the lesson file or the rules index.

On the Wednesday seat (2026-11-27, round 4b) the report reads: 410 files, 22,255 search rows. Of 293 lesson files, 255 qualified and 38 were left out: 28 under (b) (their row is scoped to other seats), 8 under (c) (5 with tier `MIXED`, 3 with no tier line), 2 under (d) (a body line that starts with the word tier). Nothing unreadable, nothing cut. The cluster takes about 174 MB on the drive. The rebuild took 9.4 s with the Mac's load average at 11; round 3 measured about 5 s on a quieter machine.

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
- **The last line states a fact about the first result; it gives no verdict.** For example: `first result: score 0.0172; of the question's 4 rarest words it holds 2 [skip move] and lacks 2 [deploy fail]`. The words are shown as Postgres stems them. If the first result lacks the words your question turns on, it is probably a near neighbour.
- **On a long question, retry with the three or four key words.** The same intent scores very differently as a sentence and as key words: "wake fire before wait" and a sixteen-word question about the same thing found the same lesson first, but the long form held only one of its four rarest words.
- **There is no "weak match" warning, on purpose.** One was built and then removed: on 34 judged questions no score threshold separated right first results from wrong ones (5 wrong either way at the best line). "It holds every rare word" is not a guarantee either: 4 of 13 wrong first results did.
- **`NO MATCH`** means none of the words is in the index at all.
- When you know the moment (pane, brief, merge, deploy), `at <trigger>` and `rules_card.py --at <trigger>` remain the surer route.

## What can go wrong, and what to do

| You see | Meaning | Do |
|---|---|---|
| `check: RED ... changed since the last rebuild` | files moved on since the last rebuild (your daily note changes all day, so this is normal) | `B rebuild` |
| `no index yet ... building it now` | the server was stopped uncleanly and the unlogged tables came back empty, or it was never built | nothing: `search` and `at` rebuild it themselves |
| **`STALE PID FILE: ... names pid N, which is alive but is NOT this index's server`** | after a power cut or a pulled drive, the old server's pid number now belongs to some other program; `start`, `search` and `up` all stop here | run the ONE `mv -n` line the message prints (a person or the coordinator runs it; the tool never moves that file itself), then `B start`. Expect a rebuild afterwards. |
| `REFUSED: the server answering on socket directory ... serves data directory 'A', but this command is addressed to 'B'` (exit code 4) | another cluster is running on your seat's socket directory, for example a second copy of your tree on another drive | stop that one with ITS OWN `braindb.sh stop`, or run this one with `BRAINDB_SOCKDIR=<another short private directory>` on every call |
| `REFUSED: lessons are on the allow-list but the rules index ... cannot be used` | `_rules_index.tsv` is missing, is not a plain regular file, is not UTF-8, or has no row that could be read | restore the rules index; without it no lesson qualifies |
| `REFUSED, for seat '<seat>' kind '<kind>' is indexed only from ...` (exit code 2) | a line in your scope file asks for something outside the code's table for your seat | remove the line; nothing was created or started |
| `another braindb command has held ... for more than 150 s; nothing was done` (exit code 75) | another rebuild, start or stop of the same cluster is still running, or is stuck | wait, or find the stuck command; the lock frees itself when that process ends |
| `REFUSED — WED_AGENT='x' but this tree ('Y') is seat 'y'` | your shell's `WED_AGENT` names another seat | unset it, or run from the matching tree |
| `REFUSED: cannot tell which seat this tree is` | the tree's folder is not named WEDNESDAY, TUESDAY or FRIDAY | run from the real tree; a copy must sit in a folder with the seat's name |
| `REFUSED: the cluster ... was made by Postgres X and the binaries here are Postgres Y ... rebuild` | the drive was plugged into a Mac with a different Postgres major version | move `pgdata-<seat>/` into `<lane>/_quarantine_<date>/` with `mv -n`, then `B up`. Never delete it. |
| `REFUSED: the socket directory ... is not mode 700` or `not owned by this user` | something else made `/tmp/wed-braindb-<uid>-<seat>` | report it; do not chmod another user's directory |
| `rebuild: DONE WITH FAULTS: N unreadable file(s) skipped, M row(s) truncated` | the rebuild finished; some files could not be read or a row was cut at its size limit; each is listed above that line | read the list; fix the file's permissions if it should be readable |
| `no scope file for seat` | step 1 not done | step 1 |
| `the server did not start` followed by log lines | read them; the log is `pgdata-<seat>/braindb-server.log` | report with the lines |

## Limits you should know before relying on it

1. **It is word search, not meaning search.** It finds a lesson when your question shares words with the lesson, its file name or its rules-index line. "cleaning up" put the lesson named "cleanup means quarantine" third, behind two neighbours.
2. **A first result can be confidently wrong.** See "How to read a result".
3. **A stale index answers without saying so.** `search` and `at` build a missing index but do not rebuild one that is merely behind the files; `check` tells you, and the launcher's `up` rebuilds at boot.
4. **`at` weights count only your own indexed ledgers.** `rules_card.py` counts every seat's ledger, so the order differs between the two. On the Wednesday seat the two list exactly the same 802 rule lines.
5. **Only your own tree's rules files are indexed.** A rule that lives in the workspace file one level above your tree is not in the index (ruled out by Wednesday: that file carries another client's environment detail, and the harness loads it into every session anyway).
6. **The qualify rule costs you lessons, on purpose.** A lesson with no tier line, a `MIXED` tier, an HTML comment or a body line that starts with the word tier is not in the index, however useful it is. `rebuild`, `check` and `doctor` all print how many are left out, and `rebuild` names every one. `search` does not look inside left-out files; when it finds nothing it says how many lessons are left out.
7. **Nothing writes to the brain.** The tool only reads your files. Corrections go in the files; the index follows at the next rebuild.
8. **What the rule cannot see.** Meaning. It reads the row, the tier and the marker that a person wrote. A lesson about another client's work that is tagged `W` with no marker is indexed; so is one whose own-client project tier hides another client's project. A secret pasted into a lesson is not a path problem and is not seen either. Tag or mark the lesson.

## The shared-file changes that go with it

`proposed/PROPOSALS.md` holds the text for `PORTABILITY.md`, `doctor.sh`, the launcher, the wrap line, the drive-sync and eject note and the sync-profile exclusion. They are proposals to the Wednesday coordinator; a seat does not apply them on its own tree.
