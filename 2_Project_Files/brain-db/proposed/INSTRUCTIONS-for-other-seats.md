# brain-db on another seat: exact steps

For the Tuesday and Friday coordinators. Written 2026-11-27 by the WED build seat "brain-db" on the Wednesday tree (Kamils-Mac-mini, drive DevMASTER); revised after Wednesday's rulings (`ANSWER-1.md`) and after the independent checker's findings (`ANSWER-3.md`). **To be sent only after the Wednesday coordinator has tested it.** Nothing here has been run on a real Tuesday or Friday tree or on another machine; the build seat and the checker each ran it on a fixture tree named TUESDAY on this Mac. Where a step is unproven on your machine, it says so.

## STEP 1, before anything else: confirm or change your seat's scope file before the first rebuild

**This choice is yours, not Wednesday's and not the build seat's.** Your scope file is the allow-list: a file enters your index only if a line in it says so. A proposal for your seat is at

```
<tree>/2_Project_Files/brain-db/proposed/scope/<seat>.scope
```

It is not live. Until you put a file at `<tree>/2_Project_Files/brain-db/scope/<seat>.scope`, every command refuses with "no scope file for seat", and creates nothing: no cluster, no server. Read the proposal whole, change what is wrong for your seat, then copy it into place (a copy, so the proposal stays for comparison):

```
cp -n "<tree>/2_Project_Files/brain-db/proposed/scope/<seat>.scope" "<tree>/2_Project_Files/brain-db/scope/<seat>.scope"
```

**The boundary the scope must keep (Wednesday's ruling, 2026-11-27):** the index holds only files your seat is already allowed to read at boot; no file that belongs to another seat or another client's project enters it. Rows inside your own files that name the other client stay, because shared rules name both clients; nothing is dropped by client name.

**What each line does:**

| Line | What it does | What to check for your seat |
|---|---|---|
| `seat <name>` | Ties the file to one seat. The tool refuses a scope file whose `seat` is not your tree's seat. | It is your seat. |
| `own_clients <words>` | A lesson whose tier is a project tier (`P-<Client>/<Project>` or `P (<Client>/<Project>)`) is indexed only if its CLIENT is exactly one of these words. A client's name inside a project name does not count. | Tuesday proposal: `datasec general`. Friday proposal: `secuura datasec general`. |
| `deny_clients <words>` | A lesson whose tier names one of these anywhere is excluded, and a section marked `<!-- tier: P-<that client>/... -->` inside an indexed lesson is dropped with its sub-sections. | Tuesday proposal: `secuura`. **Friday proposal: no such line**, because Friday works for both clients. That is the build seat's guess, not a ruling: decide it. |
| `allow rules CLAUDE.md` and `allow rules 0_Brain/CLAUDE.md` | Indexes your tree's two rules files, one row per numbered rule or heading section. A file at the tree root can only be named exactly. | That these two files in YOUR tree are the rules your seat boots on. |
| `allow lesson 0_Brain/learnings/20*.md` | Indexes lesson files (a lesson's name starts with its date). Which lessons is decided by content, never by name, and every doubt keeps a lesson OUT: see "Which lessons" below. | Nothing to change; read the "NOT indexed" list in step 4. |
| `allow rules_index 0_Brain/learnings/_rules_index.tsv` | Loads the rules index: it feeds `at <trigger>` and decides lessons. **Without a readable rules index holding at least one well-formed row, `rebuild` refuses**; it will not index every lesson. | Keep. |
| `allow ledger <file>` (two lines) | Indexes YOUR ledger and its archive, one row per table row. A ledger file can only be indexed by an `allow ledger` line. | Tuesday: `_ledger_laptop_datasec.md` and `_ledger_laptop_datasec_archive.md` (the historical file name). Friday: `_ledger_friday.md` and `_ledger_friday_archive.md`. |
| `allow daily <folder>/20*.md` | Indexes YOUR daily notes, one row per bullet line. Only files named as a plain date (`2026-11-27.md`) are taken, and a daily-note folder can only be indexed by an `allow daily` line. | Tuesday: `0_Brain/daily_tuesday/`. Friday: `0_Brain/daily_friday/`. |
| `allow skill`, `allow identity`, `allow people`, `allow architecture` | Index those folders' `.md` files, split at headings. | Whether your seat reads all four at boot; delete a line you do not want. |
| `deny_path (conflict_on_` and `deny_path .pre-` | Sync conflict copies and backups are excluded wherever that text appears in the path. | Keep. |
| `deny_seat_word <word>` | Another seat's own records. The word excludes a path when it is in ANY folder name, or in the file name, whatever kind the allow line declares. One exception: a lesson in `learnings/`, a skill in `skills/`, an identity, people or architecture file in its own folder may be NAMED for a seat (Wednesday's ruling). | Tuesday proposal: `friday`, `wednesday`. Friday proposal: `tuesday`, `wednesday`, `laptop_datasec`. |

**One thing the seat words cannot do for you.** The Wednesday seat's own records carry no seat word in their names (`_ledger.md`, `_ledger_archive.md`, `daily/`, `tasks/NEXT-PICKUP.md`). They are kept out of your index by not being on your allow-list, and by the two rules above (a ledger only by `allow ledger`, a daily folder only by `allow daily`). Do not add an allow line that names them.

**Which lessons enter (each test fails closed; the rebuild report names every lesson kept out and why):**
1. The lesson's head must be unambiguous about its tier. A lesson is kept out when its frontmatter is not closed, when `tier` is given more than once, or when a line looks like a tier line but no value could be read.
2. The tier: `W`, `M`, `MIXED` or no tier are in (untagged ones are listed by name); a project tier only for your own client; anything unrecognised is out.
3. The rules index: a lesson named by a damaged row (wrong number of fields, a bad `#n`) is out; a lesson whose rows all name only other seats is out; a lesson with no row is decided by its tier alone.

Things the scope file cannot do, by design: name anything under `4_Credentials/`, `3_Access_Keys/`, `0_Brain/dashboard/` or `0_Brain/reference/`; use `..`, an absolute path, a wildcard in a folder name, or a pattern that does not end in `.md`. Each is refused when the file is loaded. Symlinks and hard links are skipped. **A secret pasted into a lesson is not something a path rule can see.**

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
| 3 | `python3` on PATH (standard library only; the checker ran the round-2 suite under 3.9.6; round 3 has run only under 3.14.10) | `python3 --version` | 3.14.10 |
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

**4. Read the `rebuild` report before trusting the index.** It lists every file that matched an allow line and was NOT indexed, with the reason; every lesson kept out because its tier or its rules-index row could not be read safely, by name; every UNTAGGED lesson that was indexed, by name; and anything unreadable or cut. If a file you expected is in the "NOT indexed" list, or a file you did not expect is missing from it, stop and tell your coordinator: that is your scope file, a lesson's frontmatter, or the rules index being wrong, and the fix is there, not in the tool.

On the Wednesday seat the report reads: 419 files, 22,263 search rows, about 5 to 7 s; 32 files not indexed (26 lessons whose every rules-index row names only other seats, 4 sync conflict copies, 2 lessons of another client's project); 3 untagged lessons; nothing unreadable, nothing cut. The cluster takes about 157 MB on the drive.

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
| `REFUSED: lessons are on the allow-list but no readable rules index ...` | `_rules_index.tsv` is missing, unreadable or has no well-formed row | restore the rules index; the tool will not guess |
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
6. **Fail closed costs you lessons when a file is malformed.** A lesson with a mistyped frontmatter or a damaged rules-index row disappears from the index until the file is fixed. The rebuild report is where you see it; nothing else tells you.
7. **Nothing writes to the brain.** The tool only reads your files. Corrections go in the files; the index follows at the next rebuild.

## The shared-file changes that go with it

`proposed/PROPOSALS.md` holds the text for `PORTABILITY.md`, `doctor.sh`, the launcher, the wrap line, the drive-sync and eject note and the sync-profile exclusion. They are proposals to the Wednesday coordinator; a seat does not apply them on its own tree.
