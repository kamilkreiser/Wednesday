# brain-db: design

First written 2026-11-27 11:55 AEDT by the WED build seat "brain-db", before any code. Revised the same day for round 2 (`ANSWER-1.md`) and round 3 (`ANSWER-3.md`, after the independent checker's NO GO). Points changed in round 3 are marked **R3**. Brief: `BRIEF.md` in this directory.

## What it is
A local Postgres 15 cluster whose data directory sits on the drive (`pgdata-<seat>/` in this lane), holding a full-text index of the seat's markdown brain. The files stay the master. The index can be thrown away and rebuilt at any time; nothing is ever written back to the brain.

## The boundary (Wednesday's ruling, in her words)
**The index holds only files this seat is already allowed to read at boot; no file that belongs to another seat or another client's project enters it.** Rows inside this seat's own files that NAME the other client stay, because shared rules name both clients. Nothing is dropped by client name. The boundary is drawn on files, by path and by tier, not on words.

**R3: every decision that keeps a file out fails CLOSED.** When the tool cannot be sure a lesson is this seat's, the lesson stays out and the rebuild report names it and says why. The cost of a wrong "out" is one missing lesson that the report points at; the cost of a wrong "in" is another client's text in this seat's index.

## Pieces
| File | Job |
|---|---|
| `braindb.sh` | The one tool. Decides the seat from the tree, owns the cluster life cycle (`init`, `start`, `stop`, `status`, `up`, `doctor`) and hands `rebuild`, `check`, `search`, `at` to the indexer. |
| `braindb_index.py` | Standard-library Python. Reads the scope file, walks the allow-list, parses, and talks to the database through `psql` only. |
| `braindb_lock.py` | R3. Runs one command while holding the cluster's lock, so two commands cannot both initialise or start one data directory. |
| `scope/<seat>.scope` | The allow-list for one seat, as a plain reviewable text file. A seat with no scope file is refused before anything is created. Only `scope/wednesday.scope` ships live; the other two seats' files sit in `proposed/scope/` until their own coordinator confirms or changes them. |
| `tests/run.sh` | Copies the tool into a scratch tree named WEDNESDAY and proves the behaviours on a fixture brain and scratch clusters. |
| `tests/mutants.sh` | R3. Breaks the tool in a copy, one thing at a time, and requires the suite to go red on the matching assertion. |
| `tests/attack_tree.sh` | R3. Re-runs the independent checker's own attack tree against this tool. |

## Choices, one line of why each

**The server**
1. **Unix socket only, no TCP port.** `listen_addresses = ''` is written into `postgresql.conf` at `init`. No `PORTS.md` line is needed.
2. **Socket directory `/tmp/wed-braindb-<uid>-<seat>`, mode 0700.** The macOS socket path limit is 104 bytes; one short rule serves every seat. A symlink, another owner or another mode is refused. It holds no state.
3. **Peer authentication, host connections rejected.** No password or key exists anywhere.
4. **Unlogged tables.** After an unclean stop Postgres empties them; `check` says so and `search` rebuilds.
5. **`rebuild` is one transaction.** A failed rebuild leaves the previous index intact.
6. **On demand, stopped at wrap.** `rebuild`, `check`, `search` and `at` bring the server up themselves (and create the cluster when there is none); `search` and `at` build a missing index but not a stale one. `BRAINDB_NO_AUTOSTART=1` turns the self-start off.
7. **R3: a command acts only on the cluster it is addressed to.** A socket directory does not identify a cluster. Before anything else, every command that talks to the server asks it for its data directory and refuses with exit code 4 unless that equals the data directory the command was given. `check`, `status` and `rebuild` print the data directory they report on.
8. **R3: init, start and stop run one at a time per cluster**, under `flock` on `pgdata-<seat>.lock` (never deleted; the kernel frees it when the holder ends, so it cannot go stale). A second command waits, then finds the server running. Rebuilds take the same lock, so two first builds cannot both create the database. After a failed `pg_ctl start` the tool re-tests "running" and carries on if another command won the race.
9. **R3: a stale pid file naming a live process that is not ours is never moved by the tool.** `start` says so in one line and prints the exact `mv -n` command for a person or the coordinator. A wrong guess there would touch a live process that is not ours.
10. **`stop` stops only the process started with this data directory**, read from the process's own command line, never by name.
11. **Version guard.** `start` compares `PG_VERSION` with the binaries' major version and refuses with the word "rebuild".
12. **R3: the seat is the tree's folder name** (WEDNESDAY, TUESDAY, FRIDAY), through the fleet's own `tools/seat_note.sh`. `WED_AGENT` may only agree with it; a disagreement, or a folder with another name, is refused. Before round 3 the variable won, so a pane carrying the wrong variable would have built another seat's index from this tree.
13. **R3: the scope file is tested before anything is created.** A seat with no scope file gets no cluster and no server.

**What enters the index**
14. **The allow-list is a file.** Each `allow` line is one directory plus one file-name pattern (no recursion, `.md` only, `.tsv` for the rules index); a root file only by exact name and only as kind `rules`. Paths under `4_Credentials/`, `3_Access_Keys/`, `0_Brain/dashboard/` and `0_Brain/reference/` are refused in code whatever a scope file says.
15. **Symlinks are skipped; R3: so are hard links.** A file whose link count is above 1 is skipped with the reason "hard link". **What this cannot do:** a hard link and a copy are indistinguishable once the original is gone, and a secret pasted into a lesson is not a path problem at all. No path rule can see content; the allow-list keeps secret FILES out, not secret TEXT.
16. **R3: a file is taken only under the kind its name and folder say it is.** A lesson's name starts with its date; a daily note's name is a plain date and nothing else; a ledger file is indexed only by an `allow ledger` line; a daily-note folder only by an `allow daily` line.
17. **R3: another seat's records are refused whatever kind an allow line gives them.** A `deny_seat_word` excludes a path when the word is in any folder name, or in the file name, unless the file sits in its own kind's home folder (a lesson in `learnings/`, a skill in `skills/`, and so on), where ruling 2 of `ANSWER-1.md` lets a lesson or skill be NAMED for a seat. So `allow skill 0_Brain/tasks/*.md` cannot bring in `NEXT-PICKUP-TUESDAY.md`. **Limit:** the Wednesday seat's own records carry no seat word in their names (`_ledger.md`, `daily/`, `NEXT-PICKUP.md`); another seat is kept out of them by its allow-list and by point 16, not by a word.
18. **R3: which lessons.** In this order, each failing closed:
    - *The head must be unambiguous about the tier.* The file is read without a BOM; leading blank lines are skipped; frontmatter keys are folded (stripped, unquoted, lower case). The lesson is EXCLUDED when the frontmatter is not closed, when `tier` occurs more than once (in the block, in a second block, or as a stray line above the first heading), or when a line looks like a tier line but no tier value could be read.
    - *The tier.* `W`, `M`, `MIXED` and no tier at all are in (untagged lessons are listed by name in the report, as `boot_digest.py` names them). A project tier is in only when its CLIENT segment (between `P-` or `P (` and the `/`) is exactly one of the seat's own clients; a client's name occurring inside a project name does not count. A denied client's name anywhere in the value excludes. Anything else is unknown, and excluded.
    - *The rules index.* Keys are compared stripped, case-folded and without any path. A lesson named by ANY damaged row (wrong field count, bad `#n`) is excluded and listed. A lesson whose rows all name only other seats is excluded. A lesson with no row is decided by the tier alone.
    - *No usable rules index, no lessons.* If lessons are on the allow-list and no rules index with at least one well-formed row can be read, `rebuild` and `check` REFUSE. They do not index every lesson.
19. **R3: marked sections.** Inside an indexed lesson, a section marked `<!-- tier: ... -->` for a client the seat may not index is dropped: marker in any case, with any indent, in either spelling, blank lines allowed before its heading. The dropped span runs to the next heading of the same or a higher level, so sub-sections go with it; a marker with no heading directly under it drops everything to the next heading.
20. **R3: one bad file does not lose the rebuild.** An unreadable file is skipped and listed. A row over 80,000 characters (a heading over 20,000) is cut with a marker and listed; Postgres refuses a `tsvector` over 1 MB. A rebuild that skipped or cut anything says so on its last line, and `check` prints the counts.
21. **R3: the two bytes the tool splits `psql` output on (0x1E, 0x1F) are stripped on read**, beside NUL, so a row holding them cannot be silently lost from search results.

**Search**
22. **Units.** Lessons, skills, identity, people and architecture files are split at headings and the best section per file is shown. Ledger rows and daily-note lines are one unit each. A rules file gives one row per numbered rule and one per heading section's other text.
23. **Ranking.** The query is split into its lexemes; each is weighted by a rarity score computed at rebuild, summed over `ts_rank`, multiplied by the square of the share of the query's rarity mass the row matched, and divided by the query's total rarity mass. Title and file slug weigh most, then the heading and the lesson's rules-index line, then the body. Dead or superseded rules are halved and labelled.
24. **What a search shows.** With no `--kind`: knowledge first (rules files, lessons, skills and the like, by score), then up to two incident rows from the ledger and daily notes under their own heading. `--all` gives one mixed order; `--kind K` gives one kind. Every result line carries its kind.
25. **R3: no WEAK MATCH line. The last line states a fact instead.** In round 2 the tool called a result weak under a score of 0.035. The checker showed that figure mostly measures the length of the question. Its fix (measure on the question's rarest three or four words) was built and tried on 36 questions, 34 of them judged: at its best single threshold it was wrong on 5 of 34, the same as the old measure, and the gap it sat in was 0.0006 wide (`evidence/threshold_study_round3_confidence_measure.txt`). No threshold separates right from wrong honestly, so the line was removed, as `ANSWER-3.md` item 11 directs. The last line now reads, for example, `first result: score 0.0172; of the question's 4 rarest words it holds 2 [skip move] and lacks 2 [deploy fail]`. That is a fact the reader can weigh; it is not a verdict, and it is not a safe one either: 4 of 13 wrong first results held every rare word of their question (`evidence/threshold_study_round3_neutral_line.txt`).
26. **R3: a rules-file row goes ahead of the lessons only when it holds every one of the question's rarest words** (up to four). Otherwise it competes on score like any other row. This replaces round 2's "when its match is not weak", which depended on the removed threshold; the purpose is the same: one shared word must not put the rules file first.
27. **`at <trigger>` weights come from this seat's indexed ledgers only.** The set of rules matches `rules_card.py`; the order may differ.
28. **`check` also compares the indexer's and the scope file's own hashes** with those stored at rebuild.

## Not built
Vectors, any extension, any network call, any service or launchd job, any file outside the WEDNESDAY tree, any write outside this lane (other than the socket directory and the session scratchpad).
