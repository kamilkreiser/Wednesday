READY FOR QA

# ROUND 2 (answer to `ANSWER-1.md`: four rulings, three changes)

WED build seat "brain-db". Round 2 finished; last process check printed `2026-11-27 12:23:19 AEDT`. All HOLDS kept: this lane only, no existing shared file edited, no git write, no mail, post or network call, nothing installed, no `rm`.

**In one paragraph.** All seven items are done and tested: 295 of 295 scratch tests pass, and the drive cluster is STOPPED. The `at` cross-check is now exact (802 rule lines on both sides). Lessons-first puts the right lesson in the first five for 8 of the ten questions with no flag needed, and the new WEAK MATCH line fires on both misses. **One expectation in the answer is not met: question 7 still does not find the hard rule**, because that rule's sentence is in the workspace file `/Volumes/DevMASTER/CLAUDE.md`, which item 6 rules out; the tool now says WEAK MATCH there instead of looking confident. Two new questions are at the end of this section.

## The seven items

| # | Item | What changed | Tests (each able to fail) |
|---|---|---|---|
| 1 | Boundary is path-and-tier | No code change. The boundary is stated in Wednesday's words in `DESIGN.md` ("The boundary") and at the top of `INSTRUCTIONS-for-other-seats.md` and in the proposed `PORTABILITY.md` item 32. No row is dropped by client name. | - |
| 2 | Narrow the name test | Lessons are decided by the rules index `seats` column: out when every row names only other seats; no row means the tier rule alone. `tuesday` / `friday` / `laptop_datasec` are now `deny_seat_word` lines: they exclude a folder name (any kind) or the file name of a ledger or daily note, and never a lesson, skill or architecture file. | Section 6: planted lessons scoped only to `friday` and only to `tuesday` are absent; neighbours present: a lesson with `tuesday` in its name scoped `all`, one with `laptop_datasec` in its name and no row, one with a row for another seat plus a row naming this seat, a skill and an architecture file named for Tuesday. Section 7a: with the ALLOW-LIST widened onto `daily_tuesday/`, `daily_friday/`, both other ledgers and `2_Project_Files/tuesday/`, the seat words still keep all five out; 7b: with the deny lines removed too, all five enter (the failing case). |
| 3 | On demand, stopped at wrap | `rebuild`, `check`, `search`, `at` start the server themselves (and create the cluster if there is none); `search` and `at` build a missing index. `BRAINDB_NO_AUTOSTART=1` turns that off for `doctor.sh`. `proposed/PROPOSALS.md`: launcher block does `up`; wrap line stops; item 6 is the one-line eject and sync note; item 7 is the exclusion line for the sync profile I found. | Section 13: with self-start off, `check` on a stopped server is rc 3 and starts nothing (the failing case); `search`, `check`, `at` each bring it up. Section 16: a self-start on a mismatched version marker is refused. Section 17: `search` on an emptied index rebuilds it. Section 18: `search` with no cluster at all creates one, builds and answers. |
| 4 | Other seats' scopes are theirs | Both stay in `proposed/scope/`. `INSTRUCTIONS-for-other-seats.md` now opens with "STEP 1, before anything else: confirm or change your seat's scope file before the first rebuild" and a table of what each line does. Nothing is decided for them; Friday's missing `deny_clients` line is marked as my guess. | Section 12: a seat with no scope file is refused; the wrong seat's file is refused. |
| 5 | Lessons first by default | No `--kind`: rules files, lessons, skills and the like by score, then up to two incident rows under their own heading. `--all` gives the old mixed order. | Section 11: for a word in five ledger headlines and one lesson body, the lesson is result 1 by default and a ledger row is result 1 under `--all`. |
| 6 | Rules files in scope | `CLAUDE.md` and `0_Brain/CLAUDE.md`, kind `rules`: 45 rows (34 and 11), one per numbered rule (including `0a` and `3b-i`) and one per heading section's other text. A rules row whose match is not weak is listed ahead of every lesson. A root file can be allowed only by exact name. | Section 6: seven expected rows with exact headings; a third `CLAUDE.md` elsewhere and a conflict copy of the root one are absent. Section 8: `../CLAUDE.md`, a root wildcard and a root file of another kind are refused. Section 11: the rules row is result 1; with the threshold raised above every score the same row is not promoted (the failing case). |
| 7 | Say what a result is | Every result line carries its kind. `WEAK MATCH` is printed when the best result scores under 0.035, `NO MATCH` when nothing matches; both point at `at <trigger>`. | Section 11: all result lines carry a kind (3 of 3); a one-word-in-four query prints WEAK MATCH; a good match does not; the same good match does when the threshold is raised; an excluded word prints NO MATCH and a found word does not. |

## Tests

`evidence/test_run_round2.log`, tail:

```
finished 2026-11-27 12:20:09 AEDT
RESULT: 295 passed, 0 failed  (run directory .../scratchpad/braindb-test-20261127-121953-12601)
```

295 PASS, 0 FAIL, 22 lines marked `(can fail)`; 36 planted tokens absent and 37 neighbour tokens present in the whole-index dump (round 1: 217 passed; 35 and 23). The first round-2 run had 6 failures, all from two fixture tokens I had not renamed for files that are now rightly indexed; fixed in the fixtures.

## Real run, round 2 (`evidence/measurements_round2.txt`)

| Measure | Round 1 | Round 2 |
|---|---|---|
| Files indexed | 433 | 419 |
| Lessons indexed | 281 | 264 |
| Search rows | 22,203 | 22,246 (45 of them rules rows) |
| Rule lines | 364 | 345 |
| Not indexed, of files matching an allow line | 16 | 32: 26 lessons by the seats column, 2 by tier, 4 conflict copies |
| Rebuild | 4.6 to 4.8 s | 4.4 to 4.6 s |
| Size on the drive | 158 MB | 157 MB |
| Search, default order | - | 117 to 237 ms |
| Cold start: one search on a stopped server | - | 0.53 s in all |
| End state | STOPPED | STOPPED: `stop` rc 0 (pid 17759), second `stop` rc 0, `status` rc 3, no `postmaster.pid`, 0 processes whose executable is postgres (control: 5 bash) |

**The `at` cross-check after ruling 2** (`evidence/at_crosscheck_round2.txt`): 802 rule lines in the index, 802 on the card, none only on either side, across all 22 triggers. The 5 lines that were only on the card in round 1 are in the index. What still differs is order only: the first five differ in order for 12 of 22 triggers and in membership for 10, because the index counts citations in this seat's two ledgers and the card counts every seat's.

**What ruling 2 moved.** Two lessons excluded by name in round 1 are back (`claim-a-task-with-tuesday-before-starting-it`, `tuesday-never-wait-on-kam-cards...`), and so is the architecture file `2026-09-16_tuesday-vs-wednesday-structure.md`. In the other direction, the seats column now removes 26 lessons that round 1 indexed; they are listed by name in `evidence/excluded_files_round2.txt`. See question A.

## The ten questions, second table (default order, round 2)

Same questions, typed as before. The first table, below in the round-1 report, is unchanged. Scores are on the new normalised scale, so they are not comparable with round 1's numbers; the ordering rule is the same.

| # | Question | Default `search`, first five | WEAK MATCH printed? | Against round 1 |
|---|---|---|---|---|
| 1 | what must be true before I close a pane | #1 `a-pane-close-is-a-session-kill` (0.0501) | no | same as before |
| 2 | what do I check before telling Kam something is absent | #1 `a-false-absence-is-usually-my-own-instrument` (0.0382) | no | same |
| 3 | rules about typed clock times | #1 the "GENERATE timestamps, never type them" section (0.0260); #2 `read-the-clock-at-boot` | yes, wrongly | was five ledger rows and no lesson; now right without `--kind` |
| 4 | what provenance does each fact in a brief need before I send it | #1 `brief-provenance-enforcement` (0.0716); #2 `classification-is-the-field-that-grants-authority` | no | same |
| 5 | an agent has gone quiet, what proves the wake can fire before I wait on it | #1 `an-instruction-to-wait-must-name-what-wakes` (0.0067); #2 `exercise-mechanisms-before-arming` | yes, wrongly | now right without `--kind`; but this morning's ledger row for exactly this failure, #3 in round 1, is no longer shown (the two incident rows printed are older ones); `--all` still shows it |
| 6 | what do I do instead of deleting files when cleaning up | #3 `never-delete-cleanup-means-quarantine`; #1 is a neighbour (0.0294) | yes, rightly | was absent from the first five; now #3 |
| 7 | a deploy failed, can I skip it and move on | nothing right; #1 is still `if-something-blocks-move-on-to-the-next` (0.0172); no rules row in the five | yes, rightly | same wrong neighbour, now flagged |
| 8 | the usage gauge is high, which model do I launch a seat on | #1 and #2 the two usage lessons (0.0544), #3 the routing lesson | no | same |
| 9 | how do I word a decision card for Kam | #1 `decisions-go-on-the-fleet-activity-panel` (0.0674) | no | was #4; now #1 |
| 10 | what do I verify before merging after the QA gate returns | #4 `secuura-we-approve-and-merge-our-own-tested-work` only; the QA-gate lesson is not in the five (#1 scores 0.0340) | yes, rightly | was nothing right; now a related lesson at #4, flagged |

Right lesson in the first five: 8 of 10 with no `--kind` (round 1: 5 of 10 without it, 8 of 10 with `--kind lesson`). Right lesson first: 7 of 10.

**Question 7 and the rules files (item 6), reported as found.** The sentence "Never skip a failure. If a deploy fails..." is hard rule 7 of `/Volumes/DevMASTER/CLAUDE.md`, the workspace file one level above the tree, which item 6 excludes. The tree's own `CLAUDE.md` holds only rule 6, "`always-verify-and-check` and `no-skip-on-failure` apply here exactly as in the main workspace", and the question's words do not match it (Postgres stems "failed" and "failure" to different words). `search "..." --kind rules` returns that rule 6 row first with a score of 0.0004. Searching the rule's own name, `no-skip-on-failure`, does return `CLAUDE.md:89` (rule 6) first. The rules kind itself works: "portability first" returns `CLAUDE.md` rule 0 first at 0.1027, ahead of the portability lesson. To make question 7 find hard rule text, the workspace `CLAUDE.md` would have to be allowed, which is a ruling for Wednesday (question B).

**The threshold, 0.035, and how far to trust it.** On the ten questions the first result's score was 0.0382 to 0.0716 for the five right answers that were not flagged, and 0.0172, 0.0294 and 0.0340 for the three wrong first results, all flagged. The two right answers at 0.0260 and 0.0067 are flagged wrongly. So on this data the line catches every wrong first result and cries wolf on 2 of 7 right ones. It is fitted to ten points and the gap it sits in is narrow (0.0340 to 0.0382). I set 0.035 before I had seen the normalised scores, as a conversion of a 0.30 cut on round 1's scale, and kept it when the data agreed; a probe outside the ten ("ledger archive rows older than three days") found the right rule first at 0.0304 and was flagged. Read WEAK MATCH as "check this", not as "wrong". `BRAINDB_WEAK` overrides it.

## Readings and deviations in round 2

1. **Tier is still tested before the seats column.** Ruling 1 keeps another client's project files out; ruling 2 says a lesson with rows is decided by `seats`. Where both apply I keep the stricter: a lesson of a denied client's project tier stays out even if a row scoped it `all`. The two such lessons today are scoped to other seats anyway, so nothing turns on it yet.
2. **"Rule lines ahead of ledger rows" (item 5):** rule lines are not separate search rows. Each lesson's rules-index line is indexed inside that lesson's rows at heading weight and printed under every lesson result. `at <trigger>` remains the list of rule lines.
3. **A rules-file row goes ahead of lessons only when its match is not weak** (score at or above the threshold). Item 6 says "ranked above lessons"; ranking every rules row first regardless would make the rules file the new confident wrong neighbour that item 7 guards against.
4. **Default output is five knowledge results plus up to two incident rows**, so it prints up to seven. The cost is in question 5's row above.
5. **`search` and `at` do not rebuild a stale index**, only a missing one. A rebuild is about five seconds; `check`, and `up` in the launcher, are where staleness is caught.
6. **Pickup and week files** (ruling 2 names them) are not on any allow-list and there is no record kind for them. If a scope ever allowed `0_Brain/tasks/` under a document kind, a file named `NEXT-PICKUP-TUESDAY.md` would not be stopped by its name. Today the allow-list is what keeps them out.
7. **Scores changed scale** (divided by the query's rarity mass). Order within a query is unchanged by that.
8. **Evidence files:** round-1 files are untouched; round 2 wrote `*_round2*` files beside them.

## Not tested in round 2 (in addition to round 1's list below)

- Two commands racing to self-start the server at the same moment.
- The proposed `doctor.sh`, launcher, wrap and sync lines in place.
- The threshold on any question beyond the ten and the probes named above.

## QUESTIONS from round 2 (none blocks QA)

A. **The seats column now removes 26 lessons from the Wednesday index** that round 1 held, because every rules-index row for them names only other seats. Some look as if this seat might want them: `2026-11-18_the-kit-stamp-checklist.md`, `2026-09-23_use-the-local-model-as-much-as-possible.md`, `2026-09-22_ornith-is-studio-only-not-datasec.md`, `2026-11-21_a-holding-helper-gets-the-next-useful-job.md`. That is the rules index's data, not the tool, and I did not read those lessons to judge it. Is the list in `evidence/excluded_files_round2.txt` what you intended?

B. **Question 7 cannot find the hard rule under item 6 as written**, for the reason above. Do you want the workspace `/Volumes/DevMASTER/CLAUDE.md` allowed as a third rules file (it is outside the tree, and it carries the other client's tenant and environment detail), or is WEAK MATCH the accepted answer there?

---

# ROUND 1 report (as submitted; its figures are round 1's, superseded where ROUND 2 above says so)

WED build seat "brain-db" (WED-170 step 4). Last process check printed `2026-11-27 12:09:04 AEDT`. Nothing shared was edited; no git write, mail, post or network call was made.

**In one paragraph.** The index works on the drive: `braindb.sh` creates a Postgres 15 cluster in `pgdata-wednesday/` on DevMASTER, serves it on a Unix socket only, rebuilds from 433 files in under 5 seconds, and the scratch test suite passes 217 of 217. The drive cluster is STOPPED. On the ten questions, lesson search put the right lesson in its first five for 8, against 6 for `rules_card.py --at`; the two miss different questions. Full text is useful enough to build on without vectors, with two real weaknesses stated below. Four questions for the coordinator are at the end; the first matters most: the brief's exclusions (by path and by tier) do not keep the other client's name out of the index.

## What exists (bytes, from `stat`)

| File | Bytes | What it is |
|---|---|---|
| `braindb.sh` | 8,777 | the tool: `init start stop status up rebuild check search at` |
| `braindb_index.py` | 37,109 | the indexer (standard library; database access through `psql` only) |
| `scope/wednesday.scope` | 1,153 | the live allow-list for this seat |
| `DESIGN.md` | 4,795 | one page, written before the code |
| `tests/run.sh` | 22,926 | the suite; takes a scratch directory |
| `tests/make_fixtures.py` | 7,273 | builds the fixture brain (planted `xcanaryNN` files, `xneighbourNN` neighbours) |
| `proposed/PROPOSALS.md` | 9,807 | text for `PORTABILITY.md` 25 and a new 32, `doctor.sh`, the launcher, the wrap, the sync profiles; a rollback line each |
| `proposed/INSTRUCTIONS-for-other-seats.md` | 9,095 | exact steps for Tuesday and Friday |
| `proposed/scope/tuesday.scope`, `friday.scope` | 918, 1,028 | proposed allow-lists, NOT live |
| `evidence/ten_questions.md` | 1,285 | the ten questions, written before any search existed |
| `evidence/ten_questions_raw.txt` | 100,780 | every result for all ten, three ways |
| `evidence/at_crosscheck.txt` | 1,958 | `at` against `rules_card.py --at`, all 22 triggers |
| `evidence/measurements.txt` | 3,169 | size, rebuild time, latency, other-client counts |
| `evidence/excluded_files.txt` | 2,367 | the 16 files the exclusions removed, with reasons |
| `evidence/test_run_final.log` | 15,017 | the final test run, whole |
| `.gitignore` | 133 | ignores `pgdata-*/`, `_probe_*/`, `_quarantine_*/` |
| `pgdata-wednesday/` | 158 MB | the drive cluster, STOPPED, gitignored |
| `_quarantine_2026-11-27/` | 39 MB | the first drive probe cluster and its socket directory (moved, not deleted) |

## Facts re-measured (no difference from the brief)

- `/opt/homebrew/bin/postgres` and `psql` report 15.19.
- `diskutil info /Volumes/DevMASTER`: Case-sensitive APFS, Owners Disabled.
- Drive proof, before anything else: `initdb` on `_probe_1127/` in this lane succeeded (directory mode 700), a socket-only server started, answered `select version()`, and `lsof -i` on its pid printed nothing.
- One thing the brief did not say: another project's seat had its own Postgres running on this Mac during my first test run (data directory under a Secuura scratchpad, `listen_addresses=127.0.0.1`). My tools never touched it; `stop` identifies a server by its data directory only. It was gone by the end.

## Tests (`tests/run.sh <scratch>`, scratch cluster only)

Final run, tail of `evidence/test_run_final.log`:

```
finished 2026-11-27 12:08:54 AEDT
RESULT: 217 passed, 0 failed  (run directory .../scratchpad/braindb-test-20261127-120844-70326)
```

217 PASS lines, 0 FAIL lines, 18 lines marked `(can fail)`. What the suite proves:

| Section | Proof | How it is shown able to fail |
|---|---|---|
| 5, 6 | The indexed path set is exactly the 15 expected paths. 35 planted tokens are absent from a whole-index `pg_dump`; 23 neighbour tokens are present. One planted file per exclusion: `tuesday`, `friday`, `laptop_datasec`, `(conflict_on_`, `.pre-` (both name shapes), two Datasec tier spellings, a project tier naming no client, a Datasec-marked section inside a MIXED lesson, `0_Brain/dashboard/` (chat store and markdown), `0_Brain/reference/`, `4_Credentials/` (reached through a symlink), `3_Access_Keys/`, other seats' ledgers and daily folders, a sub-folder, an off-list folder | the absence assertion pointed at a neighbour token is red; the presence assertion pointed at a planted token is red |
| 7 | With the `deny_path` and `deny_clients` lines removed from the scope, 11 of the planted files DO enter the index | this is the failing case for section 6, run for real |
| 8 | Ten scope lines naming credentials, keys, dashboard, reference, a chat store, `..`, an absolute path, a wildcard directory, a non-`.md` pattern or an unknown kind are each refused, and the index is unchanged. A symlinked directory is skipped | `check` stays green after the refusals |
| 9 | `check` is red on a changed, added and removed file and names the path; an excluded file changing is not named; 26 differences print exactly 20 paths and `(+6 more)`; green after `rebuild` | green control before the first change |
| 10 | Two rebuilds give byte-identical dumps (the build time and `pg_dump`'s random token aside) | the permissive dump, filtered the same way, differs |
| 11 | `search` finds by word, honours `--kind` and `--limit`, gives zero for an excluded file's word and for stop words; `at pane` lists the right two rules, most reinforced first, and refuses a trigger that is not one word | zero-result assertion is red on a neighbour word |
| 12 | Seat `tuesday` is refused with no scope file; the wrong seat's scope file is refused; the proposed Tuesday and Friday scopes give mirror-image results on the fixtures | - |
| 13, 14 | `stop` leaves no process; a second `stop` is rc 0; a pid file pointing at a live foreign process is refused and that process stays alive; a pid file naming another data directory is refused; a stale pid is a no-op | one-process control before the stop |
| 15 | A socket path over 103 bytes and a socket directory not mode 700 are refused, and nothing starts | - |
| 16 | A start on a mismatched `PG_VERSION` marker is refused with the word "rebuild" | with the real marker back, the same start succeeds |
| 17 | After an immediate (unclean) stop the index is empty, `check` says so, `rebuild` restores it | - |

The first test run had 10 failures. All ten were faults in the tests, not the tool: a `ps | grep` that counted itself, an override the test wrapper did not pass through, and a random token `pg_dump` 15.19 writes into every dump. Fixed in the tests.

## Real run on the drive cluster

| Measure | Value | Source |
|---|---|---|
| Files indexed | 433 (281 lessons, 115 daily notes, 21 architecture, 9 skills, 2 ledgers, 2 identity, 2 people, 1 rules index) | first `rebuild` output |
| Search rows | 22,203 (19,289 daily, 1,938 ledger, 684 lesson sections, 237 architecture, 47 skill, 6 identity, 2 people) | first `rebuild` output |
| Rule lines | 364 of the 379 in the rules index (15 belong to excluded lessons) | first `rebuild` output |
| Source bytes | 19,637,231 | `evidence/measurements.txt` |
| Rebuild time | 4.82 s first; then 4.72, 4.72, 4.56 s | `rebuild` output |
| Size on the drive | 158 MB for `pgdata-wednesday/` (`du`), of which the database is 117 MB | `evidence/measurements.txt` |
| `check` | GREEN, 433 files, 0.20 s | `evidence/measurements.txt` |
| Query latency | 28 to 34 ms with `--kind lesson`; 96 to 233 ms across all kinds | the figure `search` prints, 18 runs plus the ten questions |
| Whole command, lesson search | 0.13 s | `time` |
| `at`, all 22 triggers | 790 rule lines against the card's 802; none only in the index; the 5 only on the card all belong to two lessons excluded for "tuesday" in their name | `evidence/at_crosscheck.txt` |
| End state | STOPPED: `stop` rc 0 (pid 48946), second `stop` rc 0, `status` rc 3, no `postmaster.pid`, 0 processes whose executable is postgres (control: 5 bash) | process checks at 12:06:41 and 12:09:04 |

## The ten questions

Questions were written before any search existed and typed exactly as written; no ranking constant was changed after seeing results. "Right lesson" is my judgement from the rules index. For 7, 9 and 10 I looked the right lesson up by grep after seeing the results.

| # | Question | `search`, all kinds, top 5 | `search --kind lesson`, top 5 | `rules_card.py --at`, top 5 | Found it |
|---|---|---|---|---|---|
| 1 | what must be true before I close a pane | #1 `a-pane-close-is-a-session-kill` | #1 same | `pane` (21): not in the top 5; nearest is `check-the-refusal-before-the-kill` | search |
| 2 | what do I check before telling Kam something is absent | #1 `a-false-absence-is-usually-my-own-instrument` | #1 same | `report` (62): #4 and #5, the same lesson | both |
| 3 | rules about typed clock times | five ledger rows, each a typed-clock incident; no lesson | #1 the section "GENERATE timestamps, never type them"; #2 `read-the-clock-at-boot` | `report`: #2 "generate it... never retype it" | both; search only with `--kind lesson` |
| 4 | what provenance does each fact in a brief need before I send it | #1 `brief-provenance-enforcement`; #2 `classification-is-the-field-that-grants-authority` | same | `brief` (115): the provenance rule is not in the top 5 | search |
| 5 | an agent has gone quiet, what proves the wake can fire before I wait on it | #3 today's ledger row for exactly this failure; the rest are related incidents | #1 `an-instruction-to-wait-must-name-what-wakes`; #2 `exercise-mechanisms-before-arming` | `wait` (25): #5 the same lesson | both |
| 6 | what do I do instead of deleting files when cleaning up | not in the top 5 | #3 `never-delete-cleanup-means-quarantine` | `drive` (23): #1 | card |
| 7 | a deploy failed, can I skip it and move on | nothing right | #1 `if-something-blocks-move-on-to-the-next`, which reads as the opposite advice | `deploy` (16): nothing right | neither |
| 8 | the usage gauge is high, which model do I launch a seat on | #1 and #2 the two usage lessons, #4 the routing lesson | #1 to #4 | `usage` (8): #2, #3, #4 | both; search better ordered |
| 9 | how do I word a decision card for Kam | #4 `decisions-go-on-the-fleet-activity-panel` | #1 same; the BLUF-first lesson is not found | `card` (52): none of the card-shape rules | search, partly |
| 10 | what do I verify before merging after the QA gate returns | nothing right | #5 `secuura-we-approve-and-merge-our-own-tested-work` only | `merge` (20): #5 `qa-gate-before-my-verification` | card |

Right lesson in the first five: search across all kinds 5 of 10; search with `--kind lesson` 8 of 10; the rules card 6 of 10. They miss different questions (search misses 7 and 10; the card misses 1, 4, 7 and 9).

**Is full text too weak? No, but it has two weaknesses and one trap.**

1. **It matches words, not meaning.** Question 6 says "cleaning up"; the lesson says "cleanup", which Postgres stems to a different word. Question 10's words (verify, merge, gate, returns) are spread thinly over dozens of lessons. This is the case vectors exist for. I would not add them yet: the cheaper fix is that the card already covers this case when the seat knows its trigger.
2. **Ledger rows crowd lessons out.** There are 1,938 ledger rows and 19,289 daily rows against 684 lesson sections, and an incident row repeats the question's words more densely than the rule does. Questions 3, 5 and 6 only work with `--kind lesson`. Showing lessons first by default is the obvious next change; I did not make it after seeing the results, so that the table above stays an honest first reading.
3. **The trap: a confident wrong neighbour.** Question 7's rule lives in `CLAUDE.md` hard rule 7 and a vault skill, neither of which is on the allow-list, so search returned the nearest lesson, which says to skip a blocked item. A seat reading that mid-task would be misled. The root rules files are worth adding to the scope.

What search adds that the card cannot: the section of the lesson and a snippet, the incident rows (question 5 surfaced this morning's wake failure), and no need to know the trigger word. What the card has that search lacks: fleet-wide reinforcement order, and it works with no server.

## Deviations from the brief, each with its reason

1. **Untagged lessons are indexed** (5 on this seat). The brief names only lessons whose tier names another client; `boot_digest.py` also treats untagged as included.
2. **Stricter than the brief on tiers:** a project tier that names none of the seat's own clients, or any unrecognised tier value, is excluded. None exists today.
3. **Sections marked `<!-- tier: P-Datasec/... -->` inside an indexed lesson are dropped** (2 on this seat), mirroring `boot_digest.py`. The brief only speaks of whole lessons.
4. **Daily notes:** a non-bullet line is folded into the bullet above it, or kept as its own row, rather than dropped. The brief says one row per bullet line; dropping the rest would lose text.
5. **`at` weights count this seat's two indexed ledgers only**, so the order of the first five differs from the card for 12 of 22 triggers (and the set of the first five for 10). Reading the other seats' ledgers to count citations would break the allow-list.
6. **`deny_path` words are matched case-insensitively on the tree-relative path**, so the tree's own folder name (`/TUESDAY/`) can never exclude everything.
7. **Extras not asked for:** an `up` command (the launcher line needs it), `at --top N`, `check` also going red when the indexer or the scope file has changed, and the Tuesday and Friday scopes as proposals exercised on fixtures.
8. **The test socket lives in `/tmp/wed-braindb-501-test`, not the scratchpad.** The scratchpad path is about 98 bytes and the macOS socket limit is 103. The scratch cluster itself is in the scratchpad.
9. **Left behind outside the lane:** two empty mode-700 directories, `/tmp/wed-braindb-501-wednesday` and `/tmp/wed-braindb-501-test`. Not removed (no `rm`).
10. **`__pycache__/` (60 KB) in the lane**, made by my own syntax check; gitignored.
11. **Read beyond the read-first list, all read-only:** parts of `boot_digest.py`, `seat_resolve.sh`, the head and some greps of `doctor.sh`, greps of `Launch_Wednesday.command`, the `ignore` lines of `devnas.prf`, lesson frontmatters, sample ledger rows and one daily note's line starts. `rules_card.py --at` was run 32 times (it writes nothing). `git check-ignore` and `git status` were run.
12. **Hooks:** one command was refused (an unquoted variable in zsh) and rerun under bash; several advisories fired on case-sensitive greps and on reading `$?` after a pipe. One early line printed `initdb rc=` blank for that reason; the `initdb` result was read from its own output and the start that followed.

## What I did NOT test

- Any other machine, drive or seat tree. The Tuesday and Friday scopes ran on fixtures only.
- The `doctor.sh` block and the launcher block in place (I edit no shared file). Their three `check` exit codes were exercised through `braindb.sh`.
- Ejecting the drive with the server running, a drive pulled mid-run, and the drive sync or NAS sync copying `pgdata-wednesday/`.
- A real Postgres major-version difference (only a changed `PG_VERSION` marker).
- Running under Python 3.9 (the file parses under 3.9.6; it ran only under 3.14.10).
- Two seats' servers on one Mac at once, and a `search` during a `rebuild`.
- Whether the launcher's environment differs from this pane's in a way that matters to `pg_ctl`.
- Search quality beyond these ten questions.

## QUESTIONS (none blocks QA)

1. **The brief's aim and its mechanism disagree.** It says "Another client's text must not be able to enter this index" and defines the exclusions by path and by tier. With exactly those exclusions, the index still names Datasec in 53 of 281 lessons, 815 of 19,290 daily rows, 79 of 1,938 ledger rows, 56 architecture sections and 11 of 364 rule lines (control: 6,478 rows name Secuura). These are the Wednesday seat's own files, which it already reads at boot, so the index exposes nothing new; but the sentence as written is not met. Is path-and-tier the accepted boundary, or do you want rows that name the other client dropped as well (which would also drop shared rules)?
2. **"Path contains tuesday or friday" removes 9 lessons and one architecture file from the Wednesday index**, and 5 rule lines that the rules index scopes to all seats and that `rules_card.py --at` shows this seat today (`claim-a-task-with-tuesday-before-starting-it` and four from `tuesday-never-wait-on-kam-cards...`). I took the strict reading. Should the word test apply only to the ledger and daily names it was meant for? The list is `evidence/excluded_files.txt`.
3. **Stop at wrap, or leave it running between sessions?** The launcher line starts the server; nothing stops it unless the wrap does. `proposed/PROPOSALS.md` item 5 has the line.
4. **Friday's proposed scope denies no client**, because Friday works for both. That, and the Tuesday scope's `deny_clients secuura`, are my reading and need the coordinators' word before `INSTRUCTIONS-for-other-seats.md` is sent.
