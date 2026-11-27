NO GO

# Independent QA of the brain-db lane (`2_Project_Files/brain-db/`)

Checker run 2026-11-27 12:32 to 12:54 AEDT (both times from `date`). I did not build this. Every number below is from a command I ran; the file holding its raw output is named beside it (all in this directory).

**Why NO GO, in three sentences.** One finding meets the Blocker definition I was given ("another seat's or a secret file can enter the index"): the two rules that decide which LESSONS enter (the frontmatter tier, and the rules-index `seats` column) both fail OPEN when their input is slightly malformed, so a lesson of the other client's project, or a lesson scoped only to another seat, enters the index and is searchable. It is latent, not live: the real Wednesday index holds none today (audited, 0 of 419 paths, 0 of 264 lessons). The fix is small (fail closed, about 30 lines plus fixtures); with F1 fixed and file `07` re-run clean, my verdict would be GO WITH NOTES, because nothing else found here blocks.

**What held up under attack.** The builder's suite passes for me (295 of 295) and 12 of 12 mutants I planted in a copy were caught. The real index contains no credentials, keys, dashboard, reference, sync-leftover or other-seat record path. No injection route executed anything or changed the database (26 payloads). No TCP listener; socket directory 0700. `stop` refused every foreign pid I gave it. The proposals do not break a boot in the four failure cases I simulated. The ten-question table and the 802-line `at` cross-check both reproduce exactly.

---

## FINDINGS

### F1. BLOCKER. The lesson deciders fail open: a mis-typed tier or a damaged rules-index row lets another client's or another seat's lesson in
- **Ran:** a hostile fixture tree (`scripts/atk_build.py`) over a byte copy of `scope/wednesday.scope` on a scratch cluster, then a whole-index `pg_dump` searched for each planted token (`scripts/atk_eval.sh`). Control: `xneighbour01` found 9 times; the builder's own `xcanary` tokens found 0 times.
- **Printed** (`07_attack_tree_base_scope.txt`, 69 expectations, 26 unexpected). Lessons whose frontmatter names the denied client's project, with NO rules-index row, that ENTERED the index:
  - a. key spelled `Tier:` (zatk10) or `TIER:` (zatk31); key in quotes `"tier":` (zatk27)
  - b. a UTF-8 BOM before `---` (zatk11); a blank line before `---` (zatk12); frontmatter never closed (zatk13)
  - c. value folded onto the next line (zatk17); `tier` given twice with the other client first (zatk14); two frontmatter blocks (zatk16)
  - d. tier `P-HPSM/General-ledger-import`: indexed because `own_clients` is matched as a substring and `general` occurs in the project name (zatk28). `wed` is a three-letter own-client word with the same exposure.
- Lessons scoped ONLY to another seat in the rules index that ENTERED because their row was ignored: a TAB inside the rule field, 8 fields (zatk60); 6 fields (zatk68); key with a trailing space (zatk62); key written `file.md#1` (zatk63); key differing in case (zatk64); key written as a path (zatk70).
- **The same hole, wider** (`11_crash_probes.txt`, K4): with `_rules_index.tsv` absent, `rebuild` exits 0, prints no warning, and both of the builder's own other-seat canaries are in the index (`xcanary03=5 xcanary17=5`, control `xneighbour01=5`). On the real tree that would be the 26 lessons Wednesday ruled out in ANSWER-2 A.
- **Marked sections of the other client inside an indexed MIXED lesson that survived:** a blank line between the marker and its heading (zatk40); the bracket spelling `P (Datasec/OXPd)` that the tool accepts in frontmatter but not in a marker (zatk41); an indented marker (zatk43); a lower-case marker (zatk45); `Tier` capitalised (zatk46); and the `###` sub-section under a marked `##` section, whose own text is dropped while the sub-section stays (zatk44sub).
- **What was correctly refused in the same run:** 13 tier spellings (abbreviated client, spaced letters, en dash, Cyrillic look-alike, trailing comment, YAML list, CRLF, tab indent, four-dash fence, no-break space, and others), a NEWLINE inside a rule field, `Tuesday` capitalised, `tuesday;friday`, an empty seats column, a CRLF row.
- **Context I measured, so the size is not overstated.** (1) Real tree, independent raw read of all 293 lesson heads (`06_real_raw_audit.txt`): 0 indexed lessons whose head carries a tier line naming the other client; 0 malformed rules-index rows of 379; 0 keys with stray spaces; 3 indexed lessons with no tier line at all (none names a client); the two real marked sections have no sub-heading. (2) By reading `tools/boot_digest.py` lines 71 to 84 and 129 to 150 (not run): it parses frontmatter and markers the same way, so such a lesson is already read at boot as UNTAGGED. The index widens nothing beyond the boot, but the boot names its UNTAGGED lessons and `rebuild` does not. (3) The route is a typo, not an attack.
- **Smallest fix:** fail closed in `scan()`. (i) Read with `utf-8-sig`, skip leading blank lines, fold frontmatter keys with `.strip().strip('"').lower()`; if the head holds a line matching `(?i)^\W*"?tier"?\s*:` but no tier was parsed, or the frontmatter is unclosed, or `tier` occurs twice, EXCLUDE with the reason printed. (ii) Match own and denied clients against the client segment only (between `P-` or `P (` and the `/`), not as substrings. (iii) In `read_rules`, keep the rejected rows; a lesson whose name appears in the first field of any rejected row (stripped, case-folded, path removed) is excluded, and the report prints the count of ignored rows; if a `rules_index` allow line matches no readable file while lessons are allowed, refuse the rebuild. (iv) Markers: accept any case, any indent, either spelling, blank lines before the heading, and run the dropped span to the next heading of the same or a higher level. (v) List untagged lessons by name in the rebuild report. Each case in `scripts/atk_build.py` can be lifted into `tests/make_fixtures.py` as a canary.

### F2. MAJOR. The indexer knows its server only by socket directory; with `BRAINDB_NO_AUTOSTART=1` a command addressed to one data directory rebuilt another cluster's index and then read GREEN
- **Ran:** `scripts/proc.sh` P6. Cluster c1 running on a socket directory with a 59-file index; cluster c2 stopped. Then `BRAINDB_NO_AUTOSTART=1 BRAINDB_PGDATA=c2 BRAINDB_ROOT=<a one-file tree> braindb.sh rebuild` on the same socket directory.
- **Printed** (`10_process_safety.txt`): `rc=0`; `c1 index after 6b: 1 files ... root …/tiny`; then `check: GREEN, 1 files on disk match the index` rc 0 for c2, while `status` for c2 says `server: STOPPED`. With self-start ON (6a) the same call fails safely: rc 1, c1 unchanged at 59 files.
- **Why it matters:** it is the route round the guard "a fixture tree may never be loaded into the drive cluster" (`BRAINDB_ROOT` + any `BRAINDB_PGDATA` + `NO_AUTOSTART`, with the drive server up), and the proposed `doctor.sh` block uses exactly this mode, so on a Mac with two trees of one seat mounted (DevMASTER and its T9 copy) doctor can print "index current" about the other tree's cluster. Rated below Blocker because the write needs an environment override nobody sets with `rebuild` today, and what is overwritten is a rebuildable index that the owning tree's `check` then reads RED. By the letter ("corrupt something it does not own") it qualifies; that judgement is yours.
- **Smallest fix:** `braindb.sh` exports the data directory; `need_server()` runs `show data_directory` and dies unless it equals it (3 lines).

### F3. MAJOR. A hard link is indexed: a `4_Credentials` file hard-linked into `learnings/` as `20*.md` entered the index
- **Ran / printed:** same run as F1: `LEAK zatk02hard want absent got present (3)`. The symlinked FILE (relative and absolute) was correctly skipped (`zatk01`, `zatk03key` absent; rebuild listed `4 symlink`).
- **Rating:** by the letter this is "a secret file can enter the index". I rate it Major, not Blocker, because it needs a deliberate act by someone who can already write both folders and could as easily paste the secret into a lesson; no path rule can tell a hard link from a copy.
- **Smallest fix:** in `enumerate_files`, skip any file with `os.stat(p).st_nlink > 1`, reason "hard link" (one line), plus a fixture.

### F4. MINOR. A seat with NO scope file still gets a cluster created on its drive and a server left running before it is "refused"
- **Ran:** `scripts/sim_tuesday.sh`: the lane copied into a fixture tree named `TUESDAY`, `WED_AGENT` unset, no `scope/tuesday.scope`, then `braindb.sh check`.
- **Printed** (`13_sim_other_seat_tree.txt`): initdb ran, `start: running (pid 30479 ...)`, then `braindb: no scope file for seat 'tuesday'`, rc 2, `cluster dir created by the refused command? YES`, and the server stayed up until I stopped it. `INSTRUCTIONS` step 1 says every command refuses until the scope is adopted; it does, after creating about 39 MB and a process.
- **Smallest fix:** in `braindb.sh`, test `[ -f "$SCOPE" ]` before `ensure_up` for `rebuild|check|search|at`.

### F5. MINOR. Two commands at once: one loses on a stopped cluster; both lose, and `initdb` deletes the new directory, when there is no cluster yet
- **Ran:** `scripts/proc.sh` P1, P2, P2b.
- **Printed:** two `start`: rc 0 and rc 1 (`FATAL: lock file "postmaster.pid" already exists`), one server running. Two self-starting `search`: rc 0 and rc 1 (`the server did not start`). No cluster, two `search`, 4 trials of 4: both rc 1, `initdb: removing data directory` twice, `PG_VERSION MISSING`. A third command alone afterwards succeeded every time; no process was left.
- **Smallest fix:** after a failed `pg_ctl start`, re-test `running` and carry on if true; take a `mkdir "$PGDATA.lock"` lock round init and start.

### F6. MINOR. A stale `postmaster.pid` whose pid now belongs to a live unrelated process blocks `start`, `search` and `up` until someone moves the file by hand; nothing says so
- **Ran:** `scripts/proc.sh` P4, with a python sleeper that dies on SIGINT or SIGTERM as the unrelated process.
- **Printed:** `stop` REFUSED rc 1, sleeper alive; `start` rc 1, `search` rc 1, `up` rc 1 (`Is another postmaster (PID 4959) running in data directory`), sleeper alive throughout; after `mv -n` of the pid file, `start: running`. The safety property holds. The cost is that after a power cut or a pulled drive the claim in the instructions ("costs only a rebuild") is not always true.
- **Smallest fix:** in `cmd_start`, when the pid file names a live pid that is not ours, move it into the lane's `_quarantine_<date>/` and continue, or at least print that instruction and add the row to the instructions table.

### F7. MINOR. One bad file aborts the whole rebuild
- **Ran:** `scripts/crash.sh` K1, K2.
- **Printed** (`11_crash_probes.txt`): an unreadable lesson (mode 000): `rebuild` rc 1 and `check` rc 1, both a Python traceback (`PermissionError`). One section holding 300,000 different words: `ERROR: string is too long for tsvector (4200008 bytes, max 1048575 bytes)`, `REBUILD FAILED`; the old index stays and every later rebuild fails the same way. Margin on the real tree: the longest row is 15,562 bytes. A 30 MB daily bullet of repeated words rebuilt fine (K3).
- **Smallest fix:** `try/except OSError` per file in `scan()` (skip and list); cap a row's body at a fixed size before COPY.

### F8. MINOR. A false absence: a row containing byte 0x1E or 0x1F is dropped silently and `search` prints "NO MATCH: none of these words is in the index"
- **Ran / printed** (`08_injection.txt`): `search zatkctl1` gave `NO MATCH ... (0 results)` while `select count(*) from brain.chunks where body like '%zatkctl1%'` printed `1`. Real index: 0 of 22,254 rows contain either byte (control: 19,669 contain "the").
- **Smallest fix:** strip those two bytes in `read_file` beside the NUL strip.

### F9. MINOR. One safety test passes for the wrong reason
- **Ran:** mutant M2 (`pid_is_ours` always true, so `stop` signals whatever the pid file names) through the suite.
- **Printed** (`02_mut_M2_stop_trusts_pidfile.log` lines 347 to 351): `PASS a pid file naming a live foreign process is refused (rc 1)`, `FAIL and says REFUSED`, `PASS and the foreign process is still alive`. `stop3.out` shows `pg_ctl` signalling the sleeper for 60 seconds. The "still alive" assertion cannot fail: a background `sleep` started by a non-interactive bash ignores SIGINT, which is what `pg_ctl -m fast` sends. Only the text check caught the mutant.
- **Smallest fix:** use a sleeper that dies on SIGINT (for example `python3 -c 'import time; time.sleep(300)'`), as my P4 did.

### F10. MINOR. WEAK MATCH is not a confidence signal, and 0.035 is over-fitted
- **Ran:** the ten questions again, eight of my own, nine probes (`14_`, `15_`, `16_` raw files).
- **Printed:** the same top result for the same intent scores 0.0717 as `wake fire before wait` (no warning) and 0.0067 as the builder's question 5 (WEAK). The score falls with the number of words in the question. WEAK fired on 11 of 18 natural questions (5 of the ten, 6 of my eight); in 4 of those the right item was first (Q3, Q5, my N2 at 0.0311, and `ledger archive rows older than three days` at 0.0304). It stayed silent on `how do I name a git branch` (three unrelated lessons at 0.0547, 0.0517, 0.0505) and on `Kam` (0.1218). In my set no wrong first result went unflagged among full-sentence questions, so it is conservative there; on short queries it misses.
- **Plainly:** yes, it looks over-fitted. It sits in a gap 0.004 wide on ten points, and what it mostly measures is the length of the question. The builder said as much; the instructions should say "it also fires on long questions; retry with the three or four key words".
- **Smallest fix:** normalise by the rarity mass of the query's rarest three or four terms instead of all of them, then re-pick the line on more than ten questions.

### F11. MINOR. The seat-word guard depends on the kind the scope line declares
- **Ran / printed** (`09_scope_attacks.txt`, rows 22 to 25): `allow lesson 0_Brain/learnings/*.md` and `allow skill 0_Brain/learnings/_ledger_*.md` each put both other seats' ledgers in (`xcanary22`, `xcanary23`); `allow skill 0_Brain/tasks/*.md` put a pickup and a week file named for other seats in. `allow ledger 0_Brain/learnings/_ledger_*.md` and the daily and folder forms were correctly held (rows 26 to 29). Not reachable with the shipped scope; reachable by a seat that follows step 1 ("change what is wrong for your seat"). The builder disclosed the tasks case only. The real WEDNESDAY tree does hold those files (70 in `daily_tuesday/`, 36 in `daily_friday/`, both other ledgers).
- **Smallest fix:** test the seat words on the file name for every kind when the name begins `_ledger` or the folder is not that kind's usual one; refuse a `lesson` pattern that does not begin with a digit.

### Notes
- **N1. Seat follows `WED_AGENT`, not the tree.** On the `TUESDAY`-named fixture tree, `WED_AGENT=wednesday braindb.sh status` printed `seat: wednesday tree: TUESDAY`. Once all three scope files are committed every tree holds all of them and every seat's records, so a pane carrying the wrong variable builds the other seat's index from this tree. This is the brief's own design (seat by `seat_resolve.sh`); optional guard: refuse when `WED_AGENT` and the tree name disagree.
- **N2. Proposals read against their targets.** The quoted text exists as quoted: `PORTABILITY.md` item 25's two bullets (1 match each), launcher line 29 `AGENT="${WED_AGENT:-}"`, `doctor.sh` line 470. All three files are tracked, so the rollback lines are real. Small errors: `devnas.prf` ignore lines start at line 53, not 48. Item number 32 is free today, but the sibling lane `nas-backup/proposed/PORTABILITY.proposed.md` proposes a "## 31", which is already taken, so whoever applies both must renumber. The three `ignore = Name pgdata-*` lines do not cover the lane's `_quarantine_2026-11-27/_probe_1127/pgdata` (a dead 39 MB cluster), and until they are applied the next NAS sync copies `pgdata-wednesday/` (157 MB), live if the server is up. The doctor block hard-codes `/opt/homebrew/...` although the tool also accepts `/usr/local` and PATH, and it reports every exit code other than 0 and 3 as "index stale" (a scope error is rc 2).
- **N3. Proposed blocks under macOS bash 3.2.57** (`17_proposals_simulated.txt`): `bash -n` clean for both blocks, `braindb.sh` and `tests/run.sh`; no bash 4 construct found. Launcher block: first boot built and printed GREEN in 2 s; cluster marked version 14, Postgres absent, python3 absent, seat without a scope file: each printed its warning or skipped, and the launcher continued. Doctor block: no cluster, current, stale, stopped (started nothing: 0 processes after), version differs: each printed the intended line. `out=$(braindb.sh up 2>&1)` returned in 1 s. Worst-case boot delay is `pg_ctl -t 60`.
- **N4. Instructions for other seats** (`13_sim_other_seat_tree.txt`): on a tree named `TUESDAY` the steps worked as written; the suite gave exactly the two failures the instructions predict (293 passed, 2 failed, both in section 12). `tests/run.sh` uses one fixed socket directory `/tmp/wed-braindb-<uid>-test` and a default `PGBIN` under `/opt/homebrew`, so two seats running step 2 at once on one Mac will collide.
- **N5. Small rough edges:** `at $'pane\n'` is accepted (Python `$` matches before a final newline) and prints 0 rules, harmless; `BRAINDB_WEAK=abc` is a traceback; an interrupted rebuild prints `Exception ignored ... BrokenPipeError` after its clean message.

---

## TESTED

| # | Scope | Result | Evidence |
|---|---|---|---|
| 1 | Builder's suite, my scratch | 295 passed, 0 failed, 22 can-fail lines | `01_baseline_suite.log` |
| 1 | The same under Python 3.9.6 (builder: not tested) | 295 passed | `12_suite_python39.log` |
| 1 | 12 mutants in a COPY of the tool (deny_path off, stop trusts the pid file, symlinked directory through, WEAK line off, symlinked file through, seats test off, tier always passes, check always green, version guard off, hard denies off, seat words off, lessons-first off); unmutated copy as control | control 295 of 295; every mutant red (1 to 16 failing lines); see F9 for M2 | `02_mutations_summary.txt`, `02_mut_*.log` |
| 2 | Isolation, 69 planted cases | 26 unexpected: F1, F3, and 3 look-alike daily names I rate as passes (below) | `07_attack_tree_base_scope.txt` |
| 2 | 40 hostile scope files | 0 structural escapes: `..`, absolute, `~`, `$HOME`, NUL, wildcard folder, upper-case and double-slash spellings of the denied folders, a symlinked folder, BOM, tabs all refused or matched nothing; trailing spaces, CRLF, a 2 MB line and a 300 KB pattern handled; 4 kind-dependent cases are F11 | `09_scope_attacks.txt` |
| 2 | Crashes of the indexer on the attack tree | none: invalid UTF-8, NUL bytes, empty file, `---` only, impossible date, a 2 MB line, a directory and a FIFO named `20*.md`, unclosed code fence, file names holding quotes, tabs, newlines, `$()`, backticks | `07_`, rebuild rc 0 |
| 3 | Real index, path column | 419 paths; 0 under `4_Credentials`, `3_Access_Keys`, `0_Brain/dashboard`, `0_Brain/reference`; 0 with `friday`, `laptop_datasec`, `daily_tuesday`, `daily_friday`, `pickup`, `conflict_on_`, `.pre-`, a dot-file or `..`; control: 264 match `learnings/2026-`. The 3 `tuesday` paths are two lessons and one architecture file (ruling 2); the 8 `week` paths are this seat's lessons and skills. No table holds a path absent from `brain.files`; 0 rule lines without an indexed lesson; ledgers are `_ledger.md` and `_ledger_archive.md` only | `05_real_path_audit.txt` |
| 3 | `check` on the real tree | RED before my rebuild (2 live files had moved), GREEN after it (419 files); red path proven on scratch by mutant M8 | `03_`, `04_` |
| 4 | No TCP, socket 0700 | `lsof -i` on the server pid and its 5 children: nothing; control `lsof -U` shows the socket; `listen_addresses` empty; directory `drwx------`, socket `srwx------`; `pg_hba` peer for local, reject for host | `05_real_path_audit.txt` |
| 4 | Foreign pids | stale pid of a live unrelated process, a byte copy of another server's pid file, another server's pid with our directory: `stop` REFUSED each time, the other process alive | `10_process_safety.txt` P4, P5 |
| 4 | Stop during rebuild; search during rebuild; two rebuilds at once (builder: not tested) | stop rc 0, rebuild rc 1 with the rollback message, after restart the previous index intact and GREEN; search waited 6 s then answered; both rebuilds rc 0, GREEN | P3 |
| 4 | Nothing left running | 0 after every scenario, counted by data directory | end of each file |
| 5 | Injection: 26 payloads through `search`, `at`, `--kind`, `--limit`, `--top`; plus file names, headings, bodies and rules-index fields carrying `'; drop schema`, `$()`, backticks, `\!`, `\copy ... program`, `\.`, `\N` | no file created (control: the same walk finds `expect.json`); files/chunks/rules/tables/databases/login-roles `59/99/11/8/4/1` before and after; `check` GREEN. Values reach psql only as `-v` variables read with `:'name'`, or as escaped COPY rows | `08_injection.txt` |
| 6 | The ten questions | every first result and score equals STATUS table 2; WEAK on 3, 5, 6, 7, 10 as reported | `14_ten_questions_rerun_raw.txt` |
| 6 | `at` against `rules_card.py --at`, 22 triggers | 802 and 802, 0 only on either side | `19_at_crosscheck.txt` |
| 6 | My questions | below | `15_`, `16_` |
| 7 | Proposals and instructions | N2, N3, N4 | `17_`, `13_` |
| 8 | Builder's NOT-tested list | done: racing self-starts, search during rebuild, Python 3.9, the blocks in a harness, threshold beyond ten, a second seat's tree (fixtures) | as above |

**My five questions (default search, top five), judged by reading the headings:**

| Question | First five | WEAK? | Sensible? |
|---|---|---|---|
| how do I brief a builder seat so it does not edit shared files | near neighbours only (#1 other projects' repos are read-only) | yes | yes |
| when Kam says good night what do I do first | #1 and #2 are the right section of `CLAUDE.md` (session end rules 5 and 2a); rule 1, the literal answer, is not in the five | yes (0.0311) | fires on the right section |
| can I tell Kam a task is done before I have checked it myself | nothing right; #1 is a wrong neighbour about claiming a task | yes | yes |
| which coordinator gets the wrap mail for a Datasec project | nothing right (the rule is in the workspace file, ruled out of scope) | yes | yes |
| the drive is about to be ejected, what must be stopped or synced first | three related drive and sync lessons; no rule on ejecting exists yet | yes | yes |

Controls: nonsense (`sourdough bread at high altitude`) scored 0.0003, WEAK. `one question at a time` returned rule 0b first at 0.1212 with its lesson second, no warning. `never edit files inside other coding projects` returned the manage-don't-do lesson first at 0.0421, no warning; rule 0a itself was not in the five.

**Passes worth stating, because the attack failed:** symlinked file and symlinked directory; every structural scope escape; every injection; every kill route; daily notes named with a Cyrillic or full-width look-alike of a seat word, or `fri-day`, do enter (zatk81 to 83), but they sit in this seat's own daily folder on its own allow line, and the capitalised form was refused, so I count them as passes and not as findings.

**NOT tested, and why:**
- Another machine, another drive, a real TUESDAY or FRIDAY tree: only a fixture tree named TUESDAY on this Mac.
- Ejecting or pulling the drive under a running server; a sync or NAS backup copying `pgdata-*`: would touch the real drive and other lanes.
- A real Postgres major-version difference: only version 15 is installed; the marker test and the launcher simulation stand in.
- The proposals applied in the real `doctor.sh`, launcher, `CLAUDE.md` or `devnas.prf`: I edit nothing; they ran in a stub harness.
- Two mutants I chose not to run: a TCP listener (would open a 127.0.0.1 port) and the `BRAINDB_ROOT` guard removed (would start a server on the real socket directory).
- Unicode-normalisation or ignorable-codepoint spellings of the denied folder names on the case-sensitive DevMASTER volume (my scratch is on the internal volume); file names that are not valid UTF-8.
- `PG*` environment variables in the caller's shell; the `/tmp` cleaner removing the socket directory; a reboot.
- Search quality beyond 27 queries, and with no ground truth other than my reading of headings and the builder's table.
- I read no other seat's content. I listed other seats' file NAMES and counts only.

---

## HOW

- **Rules kept:** no `cd`; absolute paths; nothing removed (`mv -n` into `_quarantine_`); no git write, mail, post, network or install; `4_Credentials` and `3_Access_Keys` never read (my fixtures used fake folders of those names inside scratch). Nothing in the lane was edited: the only lane file newer than my start outside `pgdata-wednesday/` is `ANSWER-2.md` (12:32, Wednesday's, not mine), and the code files still carry their 12:15 to 12:23 stamps (`18_final_stop_and_process_check.txt`).
- **Real drive cluster:** I ran `status`, `check`, ONE `rebuild`, read-only `psql` SELECTs on the path columns and settings, 27 searches, then `stop`. Final state: `stop: stopped pid 10649`, second stop a no-op, `server: STOPPED`, no `postmaster.pid`, socket directory empty; processes started with `-D` under the lane: 0; processes whose executable is postgres, any directory: 0 (control: 20 bash lines of 821). The index is as my 12:37 rebuild left it; `check` already read RED again at 12:51 because today's daily note moved on, which is normal.
- **Scratch:** everything under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/23d4d320-ba8d-40d8-b71d-f351bda82b71/scratchpad/qa-braindb/`. **One deviation:** the socket path limit (103 bytes) forced two socket directories outside the scratchpad, `/tmp/qa-bdb-501` and `/tmp/qa-bdb-501-b`, mode 700; both are now moved into my scratch `_quarantine_`. The builder's suite used its own `/tmp/wed-braindb-501-test`, left empty. For process scenario P3 a scratch cluster was built from the real WEDNESDAY tree (read-only, this seat's own scope); it lives only in the scratchpad.
- **Controls:** every absence is paired with a presence from the same output (named in each row). Process counts take one `ps` snapshot first and grep it, by data directory.
- **Scripts:** in `scripts/` beside this file, as run.
- **Things of mine that went wrong, and what I did:**
  1. My first path audit ran under zsh without word splitting and printed only errors; that part of `04_real_rebuild_path_audit.txt` is void. Re-run from a bash file: `05_real_path_audit.txt`.
  2. My first process run left my own attack cluster on the socket directory the scenarios needed, so its P1 to P3 results are void, and in it I moved a live scratch server's pid file aside by mistake; I put it back and stopped that server through the tool. Kept as `10a_process_safety_FIRST_RUN_FLAWED_my_error.txt`; the valid run is `10_process_safety.txt`.
  3. Three process counts taken with a live `ps | grep` counted the grep itself ("1", "2", "1"); each was re-taken from a snapshot and read 0.
  4. In `18_`, `check rc=0` and `status rc=0` are the exit codes of `head` and `tail`, not of the tool; the printed lines (`check: RED`, `server: STOPPED`) are the facts. In `17_`, the "grep rc" line is the pipeline's; the fact is that no line was printed.
  5. `11_crash_probes.txt` has one awk syntax error of mine on a line that only printed a file size.
  6. My fixture for "a project name containing wed" used `Powered`, which does not contain it; that case (zatk19) proves nothing. The substring exposure is shown by the `general` case (zatk28).
- **Hooks:** none refused a command; four advisories fired (case-sensitive grep, grep into cut, `$?` after a pipe) and are answered in items 3 and 4 above.
