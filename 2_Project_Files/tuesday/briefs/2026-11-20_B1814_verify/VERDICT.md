GATE B1814: GO WITH FINDINGS @ afc4e19 on main 7bf3752

Delta review (gate G1 Tier 1, the same reviewer as the second check) of ONE commit, OXPd 2, WP1.10: head
`afc4e1946458ef26c99fa917a5c32acc32f70578` on `6bcd02ed05544e398262dee0f13282abd658255e`, main
`7bf375268b9975ac9ece66579f7471ba7dbab11d`. Read and measured 2026-11-20, 21:48 to 22:03 AEDT (clocks by `date`), in the gate's
own clone `/private/tmp/b1814-gate/clone` (push URL `invalid://no-push`). Every number below was printed by a program; programs
and logs are under `/private/tmp/b1814-gate/` (`scratch/`, `logs/`, `ql/`, `codeql/`, `api/`).

**BLUF.** **The hosted code scan can be expected to pass, and only the pull request shows it: it has not run.** The commit is
exactly the allowed change (two lines of one test file, the word `Password` to `Passphrase` in each, nothing else; tree
`c604d74d`). The same local scan that reports the alert at the head before it (the control, run in the same session: 1 result)
reports 0 results of 63 rules at this head. The four rows still test what they tested: three mutants turn them red exactly as
with the old word. The hosted run of the head is green in all four jobs. The commit message is true and clean. No sentence and
no number of the four landing texts became false; they are byte-equal copies, and `landing.txt` is new and pins this head.
**No finding blocks the merge.** The three findings are for the records. The product code is byte-equal to the head of the
second check, so everything that check measured about it stands, its Minor findings 2 to 8 included (not re-opened, not
re-graded). **The host is still NOT wired to this library.** Nothing goes back to the product owner from this check; what he
would be asked only if the hosted scan on the pull request prints a row all the same: "the scan on GitHub reports something the
local run did not; may one more line of test code change?"

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Records | No | **The local scan sees fewer logger calls than the hosted one may.** In the gate's database of this head 53 calls on the logger in the three test files have no resolved target (`Information` 42, `ForContext` 8, `Verbose`, `Warning`, `Error` 1 each), so their arguments are not counted as places a value is written to. The hosted analysis, with its own restore, may resolve them. This does not change the expectation at this head (item 2: the list of sources is complete without type resolution, and no source yields a value that is used), but "0 results locally" alone is weaker than the second check's text said. | For the kits and the gate standard: a local C# scan is read together with the scanner's own list of sources (the query `ql/sources.ql` of this gate), not by its result count alone. FOR-RECORDS.md, item 2. |
| 2 | Records | No | **The kit's sibling search is not the scanner's own list.** The drafter's text search lists 16 calls at this head; the scanner's own class lists 17. The search misses two (`DenyListTests.cs:336`, an argument that is a NAMED constant whose value holds the word; `KeyValueShapeTests.cs:78`, an entry of a collection initialiser, which the scanner reads as a call) and lists one that is no source (`KeyValueShapeTests.cs:95`). Both missed calls return nothing, so the kit's conclusion holds. | Replace the text search by the query in later kits. FOR-RECORDS.md, item 3. |
| 3 | Records | No | **`KeyValueShapeTests.cs:95` is one edit away from the same alert.** As written it is no source (its argument is a constant joined to a parameter and has no constant value: measured). In a scratch copy with the argument made one whole constant the scan reports 1 result, the same rule at line 126, path 95, 96, 125, 126. | Nothing in this round. A rule for whoever next touches that maker. FOR-RECORDS.md, item 4. |

## The rows, item by item (measured)

**1. THE COMMIT IS EXACTLY THE ALLOWED CHANGE: yes.** One commit, one parent `6bcd02ed05544e398262dee0f13282abd658255e`
(`rev-list --count` 1; `merge-base --is-ancestor` rc 0: a fast-forward). `git diff --numstat 6bcd02ed afc4e194`: ONE row,
`2 2 tests/Datasec.Suite.Logging.Tests/KeyValueShapeTests.cs`. By `awk`:
```
before 76:             case 10: return ImmutableDictionary<string, string>.Empty.Add("Password", s).Add("Kept", Kept);
before 90:             case 17: return Tuple.Create("Password", s);
after  76:             case 10: return ImmutableDictionary<string, string>.Empty.Add("Passphrase", s).Add("Kept", Kept);
after  90:             case 17: return Tuple.Create("Passphrase", s);
```
Blob `48216cd70e5a94eb3926e92d3d4c5890367aa410` (before `22d2c5e1`; equal to the blob of the copy the second check measured);
tree `c604d74db4b613ff9892205565260e5e83cf4218` (before `c01b3f0e`); 384 lines; 46 tracked files before and after.
`git diff --quiet 6bcd02ed afc4e194 --` over `src`, `Datasec.Suite.slnx`, `Directory.Packages.props`, `.github`, `build`,
`README.md`, both project files and both lock files: rc 0 each (each path exists); the control over `tests`: rc 1; everything but
the one file: rc 0. By GET at 21:54: `compare 6bcd02ed...afc4e194` ahead 1, behind 0, one file +2 -2; `compare main...head`
ahead 3, behind 0. No third line, no new file, no comment, no suppression, no fixed minor.
**Because no product line changed, every product measurement of the second verdict stands as it was written.**

**2. THE SCANNER RESULT.** By the gate's own method (the four command lines of its database logs of the second check, the
extractor's managed program, CodeQL 2.27.4, `csharp-security-extended.qls`), each step through the wave's lock, both trees in
one session (21:51):

| Tree | Rules | Results | Detail |
|---|---|---|---|
| the control, `6bcd02ed` | 63 | **1** | `cs/cleartext-storage-of-sensitive-information`, 7.5, `KeyValueShapeTests.cs:126`, path lines 90, 125, 125, 126 |
| the head `afc4e194` | 63 | **0** | |
| a scratch copy of the head with line 95 made one whole constant (the gate's probe) | 63 | 1 | the same rule at `:126`, path 95, 95, 96, 96, 96, 96, 125, 125, 126 |

Each run: 33 source files, 333 resolved references, 0 unresolved, "Failed to resolve 2 types": the numbers of the second check.
The hosted analysis of `main` by GET at 21:54: csharp 63 rules 0 results, python 50 rules 0 results, CodeQL 2.27.4; 0 open
alerts; the rule on `main` and the default setup unchanged (`extended`, threat model `remote`, C# and Python).

*Is there another line of the same shape?* Answered with the scanner's own class, not a text search: a query over the gate's
databases that lists every expression the rule treats as a source (`ql/sources.ql`). The head before: 19. This head: **17**, the
two that left being lines 76 and 90. Of the 17, all of kind "a call with a constant argument"; 0 of kind "a variable with such
a name". 12 return nothing; 2 return a truth value that goes into an assertion (`DenyListTests.cs:356`,
`KeyValueShapeTests.cs:366`); 3 are calls on the logger written as statements, their result unused
(`KeyValueShapeTests.cs:223`, `:254`, `LogScannerTests.cs:74`). **No source at this head yields a value that anything reads.**

*Line 95 and the makers built by a constructor or an initialiser: could the hosted analysis report them? No, as far as the
rule's source and this measurement reach.* A second query printed, for every call of the makers (lines 67 to 114), its kind
and the constant value of each argument: line 95 `call to method Parse`: "(no constant value)" (the argument joins a constant to
the parameter `s`; a parameter is never a constant, whatever the restore resolves). The makers with the key `Password`:
indexer accesses (lines 67, 68, 71 to 75, 77, 82, 92), object creations (87, 88), property accesses (89, 108 to 110): the
rule's source class holds method calls and variable accesses only, and that is a property of the syntax, not of resolved
types. Line 78 is read as a call (`Add` of a collection initialiser) and returns nothing. Line 114 is an object creation.
The probe shows the path from line 95 to the logger exists, so the constant-ness of its argument is the only thing between
that line and an alert: finding 3.

*What the hosted check is expected to print:* no row for C#; no row for Python (`build/**` and the workflow are byte-equal to
`main`'s analysed state plus the first commit, 0 results of 50 in the first review). *What in the local method could make that
wrong:* (a) finding 1: 53 logger calls unresolved locally, so the local run counts fewer sinks; it matters only if a source
with a used value exists, and none does; (b) the hosted version or query pack is newer than 2.27.4 on the day of the pull
request (read by GET today: the same); (c) the hosted run extracts with its own restore and without the built outputs this run
took its references from (it can report MORE, not less); (d) the other 62 rules were run, not read rule by rule: 0 results at
both trees; (e) Python was not re-run. **The hosted check on the pull request is the authority and has not run.**

*The drafter's `codeql_local.py`: a true transcription.* Its four command lines equal the four my database logs printed, flag
for flag (`init --language=csharp --build-mode=none --source-root`; `trace-command --no-tracing --working-dir` with the
project's `dotnet exec --runtimeconfig rc.json Semmle.Extraction.CSharp.Standalone.dll`; `finalize`; `analyze` with
`--format=sarif-latest --threads=4 --rerun`), its extractor folder is byte-equal to mine (`diff -rq` rc 0, 43 files), its runner
holds the three build settings, the closed proxy, the lock path and the load read; the seat's output shows the same extractor
numbers and the same 1 and 0. It prints the result count and not the source list: finding 1.

**3. THE CELL STILL TESTS WHAT IT TESTED: yes.** `src/Datasec.Suite.Logging/DenyListData.cs:18`:
`new("password", ["password", "passwd", "pwd", "passphrase", "otp"]),`. The suite at the head, the project's SDK 10.0.404, in
the gate's clone: build `0 Warning(s)`, `0 Error(s)`; `total: 192`, `failed: 0`, `succeeded: 192`, `skipped: 0` (the same in a
second work tree and at the head before). Cells by the indented patterns: `[Fact` 42, `[InlineData` 149, sum 191; column-1
counts 0 and 0. Detailed run: `KV kvU-at-10 clean`, `KV kvU-pl-10 clean`, `KV kvU-at-17 clean`, `KV kvU-pl-17 clean`, each once;
60 `KV` lines, 6 `LEAK` (the rows of makers 18, 26, 27, the named limits, as before). `python3 -I -m unittest`: `Ran 53 tests`,
`OK`; `RULES: clean (46 files)` (hash half NOT RUN).

Mutants, the gate's own wording of the second check, on a work tree at this head, each laid beside the gate's own log of the
second check (the old word):

| Mutant | Now (`Passphrase`) | Then (`Password`) | The set of failed tests | Rows of makers 10 and 17 red, now and then |
|---|---|---|---|---|
| mK1, the structure half of the sibling rule removed | 13 failed of 192 | 13 failed of 192 | identical | maker 10 with `@`; the same |
| mK2, the sequence half removed | 4 failed | 4 failed | identical | maker 17 with `@` and plain; the same |
| mK3, the text rule removed | 26 failed | 26 failed | identical | maker 10 plain; the same |

Each of the four rows is turned red by one of the three, as before; no mutant that turned a row red then leaves it green now.
After every mutant the undo was proved (`git diff --quiet` rc 0); after the last, 192 of 192 green.

**4. THE HOSTED RUN OF THE HEAD: confirmed.** Run `44721789891`, head `afc4e194`, event push, attempt 1, success; 4 check
runs (`linux`, `windows`, `secret-scan`, `rules`), each completed success, none beside them; four job logs by GET with
`--allow-escape-sequences`, the return code asserted, the runner's echo left out. `linux` and `windows`: `total: 192` 2 lines
each, `succeeded: 192` 1, `failed: 0` 1, `0 Warning(s)` 1, `0 Error(s)` 1, `GUARD: clean (10 files)` and `(11 files)`,
`skipped: 0`. `rules`: `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (46 files)` 1, lines exactly `OK`
2. `secret-scan`: the two planted-control lines 1 each (`25 of 25`), `no leaks found` 3, and
`NEUTRAL-SCAN: stored objects 229 (156 blob, 11 commit, 62 tree), copies written 458, objects of this commit not among them 0`,
`11 commits scanned.` The control line counts 0 in each log; 0 proof lines differ; log sizes 30623, 25499, 26924, 25770 bytes,
as the STATUS says. **The 229 and the 11 are every object the six branches of the origin reach** (the job fetches
`+refs/heads/*`): counted in the gate's own clone: 229 objects (156 blob, 62 tree, 11 commit); 11 commits = 2 on `main`, 3 more
on the first lane's old branch, 3 on this lane, 1 each on the card, print and secret-store lanes. The second verdict's 150 and
8 were five branches and one commit fewer here. The line equals the builder's local line; no branch moved between the push and
22:00 (the six heads read by GET twice by this gate, 21:54 and 22:00, equal to the commission's).

**5. THE COMMIT MESSAGE AND THE SCOPE OF TEXT: holds.** The message of the commit object: 750 bytes, sha256
`6b21a59bedd52c19aa0bbb42a7a8997e4c43f97352c0ef9bf6b4cc3c5b188bae`, byte-equal to the drafter's file; subject
`Use the key word Passphrase in two key-and-value test makers (WP1.10)`. Counts over the message and the 2 added lines: 0
ban-list names, B-numbers, clarification ids, ticket keys, seat or card ids, 0 "product owner", "coordinator", "review",
"gate", "ruling", 0 "decided, ruled, approved, instructed, allowed, ordered, asked", 0 finding or round numbers (14 of 14 control
lines fire); the one address is the attribution line, once, the last line; 0 bytes outside printable ASCII and line feed; the
commit object holds no field beside tree, parent, author, committer. Author and committer: each equal to the repository
checkout's own configured name and address, and to those of the two earlier commits of the branch (compared in-process, never
printed; a made-up address does not match). Every sentence read against the head: two makers, the tuple and the immutable
dictionary (lines 90 and 76): true; a method call with a constant argument whose result goes to a logger: true (item 2); the
value is synthetic and built at run time (`ValueFor`, line 49): true; `Passphrase` in the same class: true (item 3); no product
code changes: true (item 1); 192 tests: true. It says "A code scanner reads the result of such a call as a stored credential":
true, and it names no tool, person or decision. Read note, not a finding: "the two rows" are the two makers; they are four
test rows (each maker with and without `@`). `gitleaks` 8.30.1 with the workflow's options: history rc 0 (11 commits, no leaks
found), tree rc 0.

**6. THE LANDING, RE-PINNED, AND THE TEXTS, TESTED.** 30 numbers and checkable sentences of the four texts read against the
head: **0 false** (`/private/tmp/b1814-gate/logs/table.out`; every number that stands in the texts is named in a row).

| The sentence or number | Instrument | Value at the head | |
|---|---|---|---|
| 191 test cells | indented `[Fact` and `[InlineData` lines of the test folder | 191 | true |
| the solution now runs 192 tests | `dotnet test` in the gate's clone; both hosted legs | 192, 0 failed | true |
| six classes, by name; 34 stems; the first 21 and the later 13 | `DenyListData.cs` at the head and at the first commit of the branch | 6; the six names in order; 34; 21 and 13 | true |
| deeper than 32 levels | `MaximumDepth` in `DenyListSink.cs` | 32 | true |
| the three separators; `[removed:<class>]`; `[path withheld: entry n]` | the library source | each present | true |
| `Serilog` `[4.4.0]`, `Serilog.Sinks.File` `[7.0.0]`; locked by content hash; Apache-2.0 | `Directory.Packages.props`, the two lock files, the two nuspec files | as written | true |
| two lines added to each shared file; the README lists updated later | `git diff --numstat main head`; `README.md` unchanged | 2 0 and 2 0; rc 0 | true |
| the host does not log through the library | mentions of the library or its package under `src/Datasec.Suite.Server` (control counts 2) | 0 | true |
| the cost numbers 230, 108, 223 of 1210, 64, 63, 35, 28; the base64 offsets; every named limit that is a sentence about the code | NOT RE-RUN: they stand by item 1's proof (`src` byte-equal, rc 0) | as measured in the second check | true |
| the example "a pair with the key `Password`" | it describes the rule, not the test file; `password` is a stem | | true |

Written into this folder: `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`: byte-equal copies (`cmp` rc 0
each; none changed). `landing.txt`: NEW; it pins `afc4e1946458ef26c99fa917a5c32acc32f70578` in `--match-head-commit` (once; the
old head as a pin 0 times), names the three commits, reads "three commits on the branch" and "(three here)" where the old one
read two, keeps the check wait (with the run and clock of this head) and the solution-file paragraph, and points at this
folder's two squash files. **Its DO NOT LAND head is gone and a head that says GO WITH FINDINGS, nothing blocks, and nothing
lands before the hosted scan is green stands in its place. The commission says "drops the DO NOT LAND head only if your verdict
is GO"; the gate read that as "unless NO GO", because by the grading rule records findings do not hold the merge. If the
coordinator reads it the other way, that one paragraph is the thing to change.**
Through the workflow's own function (`neutral_export` cut from the head's `ci.yml`, lines 120 to 128; `.github` byte-equal to
the head before; each text a commit message of a scratch repository; `gitleaks` 8.30.1, the workflow's four options):
`pr-title.txt` rc 0, no leaks found; the title with `pr-body.md` rc 0, no leaks found; `pr-body.md` rc 0, no leaks found; the
squash subject with a number and `squash-body.txt` rc 0, no leaks found; the same with `#PRNUM` rc 0, no leaks found;
`squash-body.txt` rc 0, no leaks found; the repository's default squash shape with the THREE commit messages rc 0, no leaks
found; the new `landing.txt` rc 0, no leaks found; CONTROL (the squash message with the workflow's planted value joined in):
rc 1, leaks found: 2. In the four texts: 0 names, B-numbers, clarification ids, ticket keys, seat or card ids, 0 "product
owner", 0 "decided, ruled, approved"; each says the host is not wired. (`landing.txt` is the coordinator's instruction sheet,
not repository text: it holds this folder's path and the words "product owner" once.)

**7. PROCESS.** Every dotnet job and every code-scan step ran through one runner (`scratch/heavy.py`, the runner of the second
check with its scratch path changed): it reads the load first (under 7 required; highest read 6.5), takes the wave's lock by
`mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d` with an `owner.txt`, runs one command under a time bound and moves the
lock folder into the gate's scratch. **40 jobs; the lock was waited for twice** (10 and 13 tries of 5 seconds, at 21:55 and
21:57: another seat held it; a wait is not a finding); no lock folder of the gate left (absent at 22:00). The three build
settings (node reuse off, the build server off, the shared compiler off) and the closed local proxy in every job; the
extractor's own restore was refused there. 0 processes of the gate alive at 22:00 (searched by its environment mark; the
control count fired). That lock folder is the gate's only write under the project.

## TESTED, and what was NOT

NOT RUN or NOT TESTED by this gate:
- **The hosted code-scanning check** (no pull request exists; item 2 is a local run of the same version and suite).
- CodeQL for Python (not re-run: `build/**` and `.github` are byte-equal to the head before).
- Anything about the product code: not re-measured, by the commission; it stands by item 1's proof. The second verdict's
  findings 2 to 8 were not re-opened.
- The other mutants of the second check (three were asked for and run); the cost probe; the attack tables.
- The other lanes' branches; the two publishes, the release guard and the container on this machine (hosted lines read); the
  hash half of rule R5; Jira.
- The 62 other rules of the suite were run, not read one by one.

How the gate worked: one clone and one fetch of the origin with the project's deploy key; two work trees of that clone (the
head before, for the control; a tree for the mutants, left clean); my own programs of the second check and the drafter's were
copied into `copies/` and none was run or edited in place (the drafter's were read, not run). Left in `/private/tmp/b1814-gate/`
(898 MB): the clone, the two work trees, three source copies and three CodeQL databases (`old`, `new`, `probeA`), the probe
queries and their outputs (`ql/`), the package-cache copy, the scratch repositories of the text scan, 40 released lock folders.
Nothing was pushed, opened, merged, deployed or sent; no ticket was written; no setting was changed; nothing was deleted; the
only hosted calls were `gh api -X GET` and one clone and fetch of the origin.
