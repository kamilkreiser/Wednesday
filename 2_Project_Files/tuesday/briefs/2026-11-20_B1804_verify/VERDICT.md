GATE B1804: NO GO @ 6bcd02e on main 7bf3752

Gate G1 Tier 1, round 2 of 2 (the last), OXPd 2, WP1.10 after the fix round (kit B1798, seat X8). Head
`6bcd02ed05544e398262dee0f13282abd658255e` on main `7bf375268b9975ac9ece66579f7471ba7dbab11d`. Read and measured 2026-11-20,
20:12 to 20:43 AEDT (clocks by `date`), in the gate's own clone `/private/tmp/b1804-gate/clone` (push URL `invalid://no-push`).
Every number below was printed by a program; programs and logs are under `/private/tmp/b1804-gate/` (`scratch/`, `logs/`,
`probes/`, `codeql/`).

**BLUF.** NO GO on ONE finding, and it is not in the product code: the code-scanning check, run by this gate on this machine,
reports one alert of high severity on one line of TEST code the fix commit added, and the rule on `main` refuses a merge with
it. The fix is one line; it is measured (0 alerts, 192 tests green). **Everything the first verdict required is closed: its
Blocker and both its Majors, each re-run with the first review's own probe and mutants.** No value under a listed name
reaches a sink in any shape the first verdict required closed; no output of a scan repeats a known value; every one of the
first review's surviving mutants is now killed. The other findings are Minor and none blocks. **The host is still NOT wired to
this library: the list protects nothing and exposes nothing today.** By the round rule a NO GO goes to the product owner on
one card: the card is "one more commit of one line in a test file, and a check of that commit".

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Major** | **Yes** | **The hosted code-scanning check is measured to report one alert of high severity in test code this change adds.** `cs/cleartext-storage-of-sensitive-information`, security severity 7.5, at `tests/Datasec.Suite.Logging.Tests/KeyValueShapeTests.cs:126`; source line 90, `case 17: return Tuple.Create("Password", s);` (a method call with a constant argument that holds `password`, whose result reaches a logger call). Reproduction: this gate ran the C# extractor's managed program on this machine and the suite the default setup names (CodeQL 2.27.4, 63 rules): the head 1 result; `main` 0 results with the same 63 rules (equal to the hosted analysis of `main`); a copy of the head with the key word changed 0 results. The organisation rule on `main` refuses a merge with a security alert of high or above; the ruleset has no bypass. The value is synthetic and this is the scanner's heuristic, but an alert is never dismissed. What it does: this head cannot be landed as reviewed. The hosted check on a pull request is the authority and has not run (no pull request exists). | One new commit on the branch: line 90 `Tuple.Create("Passphrase", s)`; and line 76 the same word (not reported; the same shape). `Passphrase` is a listed name of the same class, so the cell tests what it tested. Measured: 0 results; build 0 warnings 0 errors; `total: 192`, `failed: 0`. Then a check of that one commit that re-pins the landing line. `CODEQL-FIRST-PR.md`. |
| 2 | Minor | No | **Four shapes in which a value beside a listed name still reaches both sinks, found by the gate, that the comment of the sink does not name as limits** (item 2 below): a pair whose KEY member itself has a listed name (`{ SecretName = "ApiKey", Value = x }`: 5 of 5 rows with `@`); a type named after what it holds (`record Password(Value)`: 10 of 10 rows, both forms); names and values in two parallel lists (4 of 6); the name in the template text beside a placeholder (`"Password={V}"`: 4 of 4). None was among the first verdict's 22 rows, none was required closed, each also leaked at the first head. The rule sentences of the comment are exact and true for all four (the first is stated word for word in the sibling rule); the LIST of limits is where a reader looks and it does not hold them, and its phrase "with no name-like scalar beside it" reads as if the first shape were stopped. | Four sentences in the limits paragraph of `DenyListSink`, in the lane that next touches the file; the rule shapes are in FOR-RECORDS.md, section 2, items 7 to 10, for the master list. Until then the kits of the lanes that log carry the rules of FOR-RECORDS.md, section 6. |
| 3 | Minor (the master list; decided by nobody) | No | **The cost of the fix, measured.** Of 230 sample events of the gate's own design that hold no secret, 108 lose at least one harmless value (223 of 1210 values): 64 events by the first 21 stems, 63 by what the fix added (35 by the 13 new stems, 28 by the sibling rule, 0 by the text rule). A replaced neighbour reads `[removed:password]` (or another class) where no password stood; in the open shapes that text can stand beside the value that was NOT removed. **A text an attacker controls can remove other fields of the same event: yes, inside one logged object or list (a user called `nobody` or `r.chandler` removes outcome, station and attempt count of an audit object; the line is written and names the user); no across the event's own properties or a plain dictionary.** Nothing leaks by it; a diagnostic or an audit fact is lost. | The master list, with the numbers (FOR-RECORDS.md, section 3). A rule for the lanes that log: an audit fact is a property of the event with a name of its own. Whether a replaced neighbour should read differently from a replaced value is a product word nobody has decided. |
| 4 | Minor (the master list) | No | **The named pipe: the named limit is true and one clause short.** Reproduced under the gate's own bound: with no writer the scan gives no result (8 s, 20 s). Not in the comment: when a writer opens the pipe, `LogScanner.Scan` ends with `System.NotSupportedException` and gives no result at all (3 of 3 cases, whatever the writer does); `Scan`'s comment lists one exception type and this is another. Never a clean result. The builder's length-0 proposal rests on a premise that is wrong in one point and is still the right small fix. | Carry as a named limit, not a Major (reasons in item 4). Close it (the length-0 rule and the stream error counted as unreadable) before the scanner is given a shell or pipeline entry point or a person is told to run it. FOR-RECORDS.md, section 4. |
| 5 | Minor | No | **Three things about the scanner's output measured and not said in its comments:** the name of an entry is printed as it is (a file name with a line feed put a forged summary line into the report); a file named like the withheld text cannot be told from a withheld one; the folder the caller gives is read through when it is itself a link. No output held a known value in any of them. | Print control characters of a name escaped; say the other two. A later lane's. |
| 6 | Minor | No | **Four of the gate's 36 valid new mutants leave all 192 tests green** (a stated behaviour with no control each): a non-scalar neighbour in a SEQUENCE; white space other than a space in the text rule; the path of a LINK searched; a path that holds two known values. And the link cell passes without running where a system lets a test make no link, so whether it ran on the Windows leg cannot be known from the hosted log. | A cell each; the link cell reports itself skipped. FOR-RECORDS.md, sections 4 and 5. |
| 7 | Minor (records) | No | The text rule and the list's rule do not agree on what a name is (a key with a space or an invisible character inside the stem: removed in a pair with `@`, passes without). On Windows every reparse point is "not a regular file" (UNMEASURED there): deduplicated volumes and cloud placeholders would give a finding per file and read nothing. | Records; the Windows point belongs to the lane that wires the host. |
| 8 | Minor (records, process) | No | The gate standard says the C# extractor cannot run on this machine: its managed program can (finding 1 is the proof). Build processes: with three settings in the runner's environment 0 processes of the gate outlived its 220 jobs; one compiler server of another seat's home was alive at 20:36 (the builder's finding: confirmed as far as it can be seen). | Correct the standard; put the three settings into the kits. FOR-RECORDS.md, section 7. |

## The first verdict's findings 1 to 11, each

| First verdict | Now | Proof |
|---|---|---|
| 1 Blocker (a value under a listed key in a collection that is not captured as a dictionary) | **CLOSED** | the first review's probe, unchanged but for its scratch path, at the head: 58 rows `kvU-*`: 6 LEAK (the three named limits, both forms), 52 clean, 30 changed from LEAK to clean, 0 rows differ from the builder's table (below) |
| 2 Major (the separator half has no control) | **CLOSED** | the first review's mutants G2a, G2b, G2c at the head: RED 3, 3 and 9 cells (L16 in each: 1, 1, 4 rows) |
| 3 Major (a scan's output repeats a value in a path; a value that is only a name is no finding) | **CLOSED** | the first review's rows `output-names` and the missing folder: no value in the report, 4 path findings; the gate's 32 path and link rows: 0 outputs hold a value in any of 12 spellings, through `ToReport`, `ToString`, every public property, a JSON form and `Deconstruct` of result and findings |
| 4 Minor (limits not named; one false STATUS sentence) | closed as worded; new gaps are finding 2 | each limit sentence read against a measurement (item 7) |
| 5 Minor (11 surviving mutants) | closed | 10 killed, 1 (`G22`) no longer applies: its lines are gone and CR LF files still give their findings (gate row p25) |
| 6 Minor (scanner limits) | (a) closed as designed: 252 base64 rows, found exactly when the offset is a multiple of 3; (b) named, not closed: finding 4; (c) closed: no link followed or opened, loops included; (d) closed: refused; (e) named exactly | item 4 |
| 7 Minor (38 names with no stem) | 16 closed by 13 new stems, 22 on the master list | the first review's 78 name rows: 30 listed then, 46 now; no listed name let a value through |
| 8, 9, 10, 11 (records) | untouched, as the kit ordered | the diff holds 10 paths, all in the two folders |

## The attack table, row by row (item 1): the first review's probe at the new head beside the builder's READY TABLE part 1

The probe is the first review's `probes/Attack/Program.cs` (sha256 begins `6fce74952743273f`), copied; the only change is its
scratch path in three places (`b1796-gate` to `b1804-gate`), so that nothing ran in place. Built against the head's library
(the copied library file is byte-equal to the clone's build). A row is LEAK when the file or the collector holds the value as
it is, as hexadecimal or as base64 without padding. File and collector never disagreed.

| Maker | Shape | First review `@` / plain | Gate now `@` / plain | Builder now `@` / plain | Agree |
|---|---|---|---|---|---|
| 1 | Dictionary&lt;string,string> | clean / clean | clean / clean | clean / clean | yes |
| 2 | Dictionary&lt;string,object> | clean / clean | clean / clean | clean / clean | yes |
| 3 | Dictionary&lt;string,string[]> | clean / clean | clean / clean | clean / clean | yes |
| 4 | Dictionary&lt;HeaderKind,string> | clean / clean | clean / clean | clean / clean | yes |
| 5 | Dictionary&lt;object,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 6 | ConcurrentDictionary&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 7 | SortedDictionary&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 8 | SortedList&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 9 | ReadOnlyDictionary&lt;string,string> | clean / clean | clean / clean | clean / clean | yes |
| 10 | ImmutableDictionary&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 11 | Hashtable | LEAK / LEAK | clean / clean | clean / clean | yes |
| 12 | NameValueCollection | clean / clean | clean / clean | clean / clean | yes |
| 13 | ExpandoObject | LEAK / LEAK | clean / clean | clean / clean | yes |
| 14 | List&lt;KeyValuePair&lt;string,string>> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 15 | KeyValuePair&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 16 | anonymous {Name,Value}[] | LEAK / LEAK | clean / clean | clean / clean | yes |
| 17 | Tuple&lt;string,string> | LEAK / LEAK | clean / clean | clean / clean | yes |
| 18 | ValueTuple (Password: s, Kept: k) | LEAK / LEAK | LEAK / LEAK | LEAK / LEAK | yes |
| 19 | JsonObject | clean / LEAK | clean / clean | clean / clean | yes |
| 20 | JsonElement | clean / LEAK | clean / clean | clean / clean | yes |
| 21 | HttpRequestHeaders | LEAK / clean | clean / clean | clean / clean | yes |
| 22 | record Cred | clean / LEAK | clean / clean | clean / clean | yes |
| 23 | class Poco with ToString | clean / LEAK | clean / clean | clean / clean | yes |
| 24 | anonymous object | clean / LEAK | clean / clean | clean / clean | yes |
| 25 | anonymous with Lazy&lt;string> Password | clean / clean | clean / clean | clean / clean | yes |
| 26 | List&lt;string> (value is an element) | LEAK / LEAK | LEAK / LEAK | LEAK / LEAK | yes |
| 27 | byte[] | LEAK / LEAK | LEAK / LEAK | LEAK / LEAK | yes |
| 28 | MemoryStream | clean / clean | clean / clean | clean / clean | yes |
| 29 | Uri with the value in its query | LEAK / LEAK | clean / clean | clean / clean | yes |

Counted by program: the first head 36 LEAK and 22 clean; the gate now 6 LEAK and 52 clean; changed from LEAK to clean 30; rows
where the gate differs from the builder's table 0; still LEAK `kvU-at-18`, `kvU-pl-18`, `kvU-at-26`, `kvU-pl-26`, `kvU-at-27`,
`kvU-pl-27`. **No row the first verdict required closed still leaks.** The 12 other rows: `scalarobj` and `stringify` changed to
clean; `chainU2/31/32`, `dictkey`, `exmsg`, `exinner`, `exprop`, `typetag`, `positional`, `template` arrive as before, each a
named limit or the design. The 58 rows under a LISTED property name: 0 leaks, as before. Names: 78 rows, 30 listed at the first
head, 46 now, 16 changed, 0 listed names with a value in a sink.

## The rows, item by item (measured)

**1. THE FIRST VERDICT'S BLOCKER AND TWO MAJORS: each closed** (the two tables above). Finding 3 in the gate's own rows
(`logs/attack2-scan.log`): a value as a file name, a folder name, a folder two levels up, a link's name, the scanned folder's
own name, a missing folder's path, a path that is a file; a value that spans a folder name, the separator and a file name;
the value as base64, percent-encoded and JSON-escaped in a name: each is a path finding with the path withheld, or the path is
never printed. The entry number is the ordinal place (entries 2 and 4 of 4, as predicted). A name that holds the value twice
gives one finding per spelling.

**2. THE NEW MECHANISM, ATTACKED.** The gate's own generator (`probes/Attack2`, an outside assembly): 155 rows through
`SuiteLoggerFactory.Create`, the file sink and a collector; 84 rows leak; 0 threw; file and collector never disagreed.

*The required question: what does the cleaning step see that is not one of the shapes the fix names, and does a value under a
listed name still reach a sink?* **Yes.** The step sees, beyond "a name-like value beside a value in one structure or
sequence" and "a listed name, a separator and more text in one scalar": the NAME of the member that holds the name-like value
(when that name is itself listed the rule stands down); the TYPE TAG of a structure (never looked up); a name-like value in a
NEIGHBOURING sequence (parallel lists); the TEMPLATE TEXT around a placeholder (never read); the two values of a dictionary
entry pair; a name one level down; any joining character but three. In each of those a value beside a listed name reaches
both sinks.

The builder's three open shapes (its FOR TUESDAY, master-list items 2, 3, 4):

| Shape | In the first verdict's 22 leaking rows? | Reproduced | Named in the comment | Grade by the round rule |
|---|---|---|---|---|
| two VALUES of one dictionary | no: new (no row of the first table builds it) | 6 of 10 rows leak (a plain dictionary, a list of dictionaries, the read-only wrapper; a JSON object node is closed by its text form) | yes: "a name and its value held as two VALUES of one dictionary both pass" | the naming is true and complete: records |
| a name one level deeper than its value | no: new | 8 of 8 rows leak (a nested object, a nested list, an XML element in both forms) | yes: "not one that sits a level deeper" | true and complete: records |
| a text outside the rule's wording | no: new (the first table's string rows all use `=` or `,`) | 30 of 40 rows leak: a space, a tab, an arrow, a bar, a semicolon, XML tags, brackets, a slash, a command line, encoded or escaped separators, `Bearer x`, `Basic x`, full-width separators, the value first, a twice-escaped JSON text; the 10 that are clean all hold one of the three separators after a listed name | yes, by the rule's exact wording ("one of the three separators") and by the limit "no listed name and separator before it" | true; one sentence of examples would make it complete: records |

Shapes NEITHER the first verdict NOR the builder names: finding 2 (four shapes), and in the same run: `Bearer x` as the text of
an authentication header object logged without `@` (leaks; with `@` and the scheme `Bearer` it is clean, with `Basic` it
leaks); a lookup or a grouping (the key is lost by the package, the value arrives alone); a hand-built structure whose type
tag is a listed name. Closed and worth knowing: value tuples in a list, a dictionary entry, a claim, a pair holding an object
or a byte array, the value before the name, an enumeration value as the name, a header line as a dictionary value, a name
with a trailing colon, an array of command-line arguments with `--password` (clean; `-p` leaks: no stem).
Speed of the two rules, one event each: a scalar of 5,000,000 letters 0.03 s; 1,600,000 short runs each before a separator
0.47 s; a sequence of 200,000 strings 0.10 s. Linear.

**3. THE COST OF THE FIX: finding 3**; numbers, how the 230 events were chosen, the names and the neighbour texts in
FOR-RECORDS.md, section 3. A log of such events is not "mostly removed text" (18 values in 100), but configuration dumps are
hit hardest (50 of 55 events) and a list of configuration pairs printed as strings lost five of its six pairs to one key.
Said plainly: an attacker who chooses a user name or a file name can remove the other members of a logged object or list
that holds it; cannot remove a property of the event; cannot make a line disappear; cannot make a value appear.

**4. THE SCANNER.**
- The path output, the builder's choices (a) to (h) by effect: (a) a folder is an entry and has a place in the count
  (measured); (b) one finding per spelling per path, not per occurrence (measured; a path with two values has no cell:
  finding 6); (c) the separator of the operating system (a value that spans it is found here; Windows UNMEASURED); (d) path
  and link findings first (measured); (e) the folder's own path neither searched nor printed (measured, 3 rows); (f) the kind
  read once at the listing (DERIVED; a swap between listing and read is not run); (g) the reparse-point mark (finding 7 for
  Windows); (h) one withholding function (gate mutant P01 turns S13 and S14, P15 turns S14).
- Links, with the gate's own: a link to a file outside, to a folder outside (holding a value file and a pipe), `a/back -> ..`
  with `self -> .`, a mutual loop of two folders, a dangling link, a link to itself, a chain of two links, a link to a NAMED
  PIPE (the scan returned: not opened), a link whose target text holds a value: each one `NotARegularFile` finding, 0 values
  found through a link, the one real value file found once. A hard link is a regular entry and is read as a second file.
- **The named pipe: finding 4.** The wait is real and the limit sentence is true; exactly worded it is not, because it stops
  at "does not return before that". **Reading: a named limit to carry, not a Major.** Reasons: (1) it can never be read as
  clean: no result, or an exception; the scanner's one promise holds; (2) the first verdict graded it Minor and allowed
  naming; (3) nothing runs the scanner: it is a library call with no entry point, and no person has been told to run it;
  (4) to put a pipe into a log folder one must already be able to write there, and whoever can may delete the logs; (5) the
  fix is two small rules and belongs with the entry point. It becomes a Major the day the scanner is run by an operator or a
  pipeline step with this still open: a stalled or aborted check that nobody is watching reads as "no findings reported".
  The builder's instrument output is reproduced (a pipe and a socket read as ordinary files of length 0). Its length-0
  proposal says an entry of length 0 "gives it no text either way": for a pipe that is not what happens (reading the stream's
  length throws); the proposed rule would still avoid both the wait and the error.
- The empty list: refused, the message holds no value. Base64: 252 rows (6 lengths, 7 offsets, 3 tails, both alphabets):
  found exactly when the offset is a multiple of 3; 0 rows disagree with the comment. The glued token: not found after
  letters, a digit, a hyphen, an underscore; found after a space, `=`, a quotation mark, a dot, a slash, a colon: as the
  comment says.

**5. CELLS AND MUTANTS.** The suite at the head in the gate's clone, the project's SDK 10.0.404: build `0 Warning(s)`,
`0 Error(s)`; `total: 192`, `failed: 0`, `succeeded: 192`, `skipped: 0`. Cells by the indented patterns: `[Fact` 42,
`[InlineData` 149, sum 191, column-1 counts 0; plus the 1 test of the other project. `python3 -I -m unittest`: `Ran 53 tests`,
`OK`; `repo_rules.py`: `RULES: clean (46 files)` (hash half NOT RUN: the gate does not open the supplied source).
- The first review's 52 mutants (2 reverts, the first seat's 7, its own 43), re-run from the saved copy: **50 killed, 0
  survive, 2 do not apply** (`G16`, `G22`). Judged: `G16` (sub-folders not read) cannot be written as it was because the
  listing was rewritten; the builder's mS6 does the same work on the new line and turns S12 and S14: accepted. `G22`: the
  lines are removed and no output depends on them (gate row p25): accepted. The 13 survivors of round 1 that still apply:
  each RED now (G1b L18; G2a, G2b, G2c L16; G7 L19; four G13 and three G14 one S22 row each; G27 S21).
- The builder's own, in the gate's wording of each edit: mK1 13 red, mK2 4, mK3 26, mK4 3 (L03, L04, L06), the three quiet
  controls mQ1 14, mQ2 9, mQ3 12, mS5 2, mS6 2: the same counts and the same cells as the STATUS, each.
- The gate's own 37 new mutants on the two rules and the path output: 36 valid (one did not compile and was written again
  in a wording that does), **32 killed, 4 survive: finding 6.** After every mutant the undo was proved (`git diff --quiet` rc 0, 0 exceptions).
- The four assertion lines of three existing cells (the builder's DEVIATIONS 1): exactly 4 lines removed in
  `LogScannerTests.cs`, 0 in `DenyListTests.cs`; each compares the same file at the same line and column, relative where it
  was absolute. **Not weakened** (gate mutant P09, the full path back in the findings of a file's lines, turns all three).

**6. THE HOSTED RUN `44707287524`: confirmed.** Head `6bcd02ed`, event push, attempt 1, success; four job logs by GET with
`--allow-escape-sequences`, return code asserted, the runner's echo left out. `linux` and `windows`: `total: 192` 2 lines each,
`succeeded: 192` 1, `failed: 0` 1, `0 Warning(s)` 1, `0 Error(s)` 1, `GUARD: clean (10 files)` and `(11 files)`. `rules`:
`Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (46 files)` 1, lines exactly `OK` 2. `secret-scan`: the
two planted-control lines 1 each, `NEUTRAL-SCAN: stored objects 150 (94 blob, 8 commit, 48 tree), copies written 300, objects
of this commit not among them 0` 1, `8 commits scanned.` 1, `no leaks found` 3. Every count equals the STATUS's; the control
line counts 0 in each log; log sizes 30784, 25489, 25771, 26678 bytes, as the STATUS says. **The link cell on the Windows leg:
what can be known is that it did not fail and was not reported skipped (`skipped: 0`; 0 lines of either log name it). It
returns as passed when no link can be made, so whether it ran is unknown and cannot be read from these logs (finding 6).**

**7. SCOPE AND TEXT.** By GET at 20:17: branch at the head; `compare 2c231b44...6bcd02ed` ahead 1, behind 0, 10 files, 0
outside the two folders; `compare main...head` ahead 2, behind 0; 4 check runs each success; `main` unchanged; pull requests
1 closed, 0 open; the origin now holds three other lane branches. In the clone: 10 paths (9 `M`, 1 `A`), all `.cs` in the two
folders (control: a planted row is reported); no line of `Datasec.Suite.slnx`, `Directory.Packages.props`, `ci.yml`,
`build/**`, `README.md`, either project file or either lock file (`git diff --quiet` rc 0 for each; control rc 1); 1221 lines
added, 49 removed; one parent; `git merge-tree --write-tree main head` equals the head's tree. The 1221 added lines and the
commit message: 0 ban-list names, B-numbers, clarification ids, ticket keys, seat or card ids, 0 "product owner",
"coordinator", "review", "gate", 0 "decided, ruled, approved", 0 finding or round numbers (12 of 12 control lines fire); the
one address is the attribution line; 0 bytes outside printable ASCII, 0 tabs, every file ends in a line feed. The clarification
entries C-42 and C-45 read at source: nothing in the change says he decided anything. `gitleaks` 8.30.1 with the workflow's
options: tree rc 0, history rc 0. No regular expression in the library (0; control 1).
- The XML comments, each limit sentence against a measurement: `DenyListSink`: every sentence true; the list is short by the
  four shapes of finding 2. `LogScanner`: every sentence true; the pipe sentence is one clause short (finding 4); the three
  points of finding 5 are not said. `LogScanFinding`, `LogScanResult.ToReport`, `TokenShape`, `KnownValueForms`: true as
  measured. No sentence is untrue; none of the gaps is one a reader would rely on for safety while the host is not wired.
- The builder's process finding: finding 8.

**8. CODEQL AND THE PULL REQUEST: finding 1**, `CODEQL-FIRST-PR.md`.

**9. THE TEXTS.** Written for the head as reviewed, marked not for use in `landing.txt`, and worded so that the one-line fix
changes no sentence and no number of them. **Through the function** (`neutral_export` cut from the head's `ci.yml`, lines 120
to 128; each text a commit message of a scratch repository; `gitleaks` 8.30.1 with the workflow's four options):
`pr-title.txt` rc 0, no leaks found; the title with `pr-body.md` rc 0, no leaks found; `pr-body.md` rc 0, no leaks found; the
squash subject with a number and `squash-body.txt` rc 0, no leaks found; the same with `#PRNUM` rc 0, no leaks found;
`squash-body.txt` rc 0, no leaks found; the repository's default squash shape rc 0, no leaks found; `landing.txt` rc 0, no
leaks found; CONTROL (the squash message with the workflow's planted value joined in): rc 1, leaks found: 2. In the four
texts: 0 names, B-numbers, clarification ids, ticket keys, seat or card ids, 0 "product owner", 0 "decided, ruled, approved";
0 non-ASCII bytes outside the one footer line; each says the host is not wired. `landing.txt` is a head-pinned squash of the
two commits with one parent, the checks to wait for, and what the solution file must read after each lane by ordinal order.

## TESTED, and what was NOT

NOT RUN or NOT TESTED by this gate:
- **The hosted code-scanning check** (no pull request exists; finding 1 is a local run of the same queries and version).
- The scanner, the links and the instrument on Windows and on Linux; whether the link cell ran on the Windows leg.
- A device file in a scanned folder; an entry swapped between the listing and the read; peak memory of a scan.
- Known vulnerabilities and signatures of the two packages (no package changed in this round).
- The two publishes, the release guard and the container on this machine (hosted lines read); the hash half of rule R5.
- CodeQL for Python again (`build/**` and the workflow file are byte-equal to the first commit).
- The branch of the secret-store lane (it appeared on the origin after the gate's fetch); the other lanes' kits; Jira.
- Any log of a real sign-in, printer, simulator or tenant.
- One row group of the gate's own audit probe was written wrongly (a list passed as the argument list) and is left out of
  every count.
- No fix was built into the branch: the fix shape of finding 1 was applied in the gate's work tree, measured and undone.

How the gate worked, said so that it can be judged: every dotnet job and every CodeQL step ran through one runner
(`scratch/heavy.py`) that reads the load first (under 7 required; highest read 5.02), takes the wave's lock by `mkdir` of
exactly `<project>/.tools/wave1-heavy.lock.d` with an `owner.txt`, runs one command under a time bound and moves the lock
folder into the gate's scratch: 220 jobs, the lock never waited for, no lock folder of the gate left (at 20:42 another review held the lock). That folder is the gate's only write
under the project. Every job ran with a closed local proxy; the C# extractor's own restore was refused there. The first
review's programs were copied and never run or edited in place. Left in `/private/tmp/b1804-gate/`: the clone, a work tree for
the mutants (clean), the probes (a few named pipes, sockets and links among their fixtures), three CodeQL databases, the
package-cache copy, 220 released lock folders. Nothing was pushed, opened, merged, deployed or sent; no ticket was written; no
setting was changed; the only hosted calls were `gh api -X GET` and one clone and fetch of the origin.
