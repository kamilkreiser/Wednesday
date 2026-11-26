GATE B2130: GO WITH FINDINGS @ 0ae9066 on main 504ca04

Gate G1, ROUND 1 OF 2 of lane OX-B kit 2 (the lab tool `oxpd1`: `Oxpd1Command.cs`, `Oxpd1EchoVerb.cs`, the Lab README,
two test files and the stub; owed 106, 107, 109, 110, 135, 136), one Opus reader (claude-opus-5-5), in-session,
read-only. OXPd 2, kit B2128 (seat X79; stamp S4: Q1 "a" one kit, Q3 "a" the seat writes the code to the kit's
specification, each in words; Q2, Q4 to Q10 the defaults; S8 the canonical heavy runner 31adedc8; ANSWER-1 (a); every
choice the coordinator's, none the product owner's). Head `0ae90664aef54febc2624c54e71f35e2b60f1313` on
`b2128/lane-b-kit2-lab-oxpd1`, ONE commit, one parent = main `504ca043688e633a703abe47a1f9d4dcfe367518` (PR 55). Main and
the branch did NOT move during the gate (gh api -X GET 22:40:15 and 23:36:18 AEDT; open pull requests 0 both times;
open code-scanning alerts 0 both times). Read and measured 2026-11-26 22:39 to about 23:45 AEDT in my scratch
`fleet/state/s331/g2130/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity; detached at the head; the
mutants ran here), worktrees `red` (BASE plus the head's three test files, `git diff --quiet 504ca043 -- src` rc 0) and
`probe` (the head plus one probe file of mine, `GateProbeB2130Tests.cs`, never committed, never pushed). Every heavy job
through the kit's `heavy.py` (sha256 31adedc8..., my copy of the eight tools 8 of 8 equal to THE TOOLS) and the wave
lock, taken per job and released, one at a time (50 jobs, lock waits 0 each; load-gated, load1 reached about 14 from
other work); the 50 released lock folders are mine, in `g2130/_quarantine/locks/`; no other holder's lock or file
touched; the lock absent at 23:36.

**AT THE HEAD (where a record or the kit disagrees with what I measured):**
1. **The README's "a record holds a second element named `id` (in any namespace, at any depth)" reads wider than the
   code**: a second `id` inside a record element whose name the client's logging mask covers (HP's own
   `authenticationAgent/networkCredentials`, or any name holding a deny-list stem) is replaced by the mask before the
   lab reads it, and the register is written (FOUND 1).
2. **H9 is now MEASURED**, and one shape of it throws: a `--callback-host` holding a lone surrogate passes
   `Uri.CheckHostName` and the new length check's `UriBuilder` throws `UriFormatException` out of the parser (FOUND 2).
3. The kit's D7 says a short port makes the length refusal "up to four characters early"; the seat's README says six
   (its DEVIATION 7). MEASURED: six is right (a 199-character host reads 256 at port 65535 and 250 at port 80, which the
   address leaves out).

**BLUF.** The head does what its six items ask on every path the kit names. **No answer shape the lab is handed holds
the run's id and lets a register through beyond the named LIMIT rows, but one the client hides from it** (FOUND 1: the
masked element; plus the README's own limits: comment, processing instruction (MEASURED taken), the id inside a record's
other elements); **no address the three options take makes the envelope's writer throw** (436 runs: every printable
character in host, path and query, and 33 named shapes, 0 exceptions) and none reaches the device holding a character
outside ASCII, though within ASCII the device gets .NET's canonical form (FOUND 4); **no callback host the parser takes
makes the client throw** (ports 1, 80, 443, 8080, 65535 for each taken host), but one makes the PARSER throw (FOUND 2);
**no delay the parser takes is at least its wait or time-out** (8 cells and 20 probe lines); **no landed cell changed**
(removed lines under `tests/` 0). Red first exactly the 26 rows (`Total: 352, Errors: 0, Failed: 26`, each by assertion,
my run); green the Lab `Total: 352, Failed: 0` and the whole solution `total: 2422`, `failed: 0`, `succeeded: 2418`,
`skipped: 4` (my run); `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal` (my run of the seat's rows file through the
frozen tool, every row's red rows equal to the seat's); `HOSTED 0ae90664...: PASS` (my read; control FAIL 4). **Two
Minor findings, five Info. None blocks the landing.** Tuesday's points: (a) the ASCII rule refuses none of an IPv6
literal in brackets, a port, a percent-escaped path or an `xn--` host (all MEASURED taken): **Info**; (b) the parser's
address and the run's can differ in length only by the port's digits (same builder, same host string, same path
length): MEASURED, the parser never takes a host the client then refuses; (c) the four refusals take every answer in
HP's schema shape (DERIVED from the xsd, re-grepped) and refuse neither white space nor a namespace declaration on the
result or a record (MEASURED); (d) the ONE words.py hit is the README Limits line (`added.txt:118`), nothing else.

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (a second `id` hidden by the client's logging mask: the register is written).**
   `logs/probe.tsv` G1: another agent's record holding `<authenticationAgent><uri/><networkCredentials><id>RUN-ID</id>
   </networkCredentials></authenticationAgent>` (HP's own element names, the `id` outside HP's schema), or `<secret>`,
   `<token>`, `<body>` holding `<id>RUN-ID</id>`, or `<networkCredentials><password>RUN-ID</password>`: each `exit 0`,
   two requests, the agent written, `sign-in agent records on the device: 1, none with this id`. Why: the client's
   `Oxpd1Soap.Mask` (`Oxpd1Soap.cs:363` to `:366`) replaces the whole content of an element whose local name holds a
   deny-list stem (`DenyList.TryFindClass`, `Contains` on a normalised name; stems include `credential`, `password`,
   `secret`, `token`, `body`, `subject`, `handle`, `signature`) with the placeholder text, so C1 (c)'s descendant count
   reads 1. Harm: the same as owed 106's (the undo of this register removes an agent the run did not add); reach: a
   device answer outside HP's schema, in an element HP's record really has (`networkCredentials` under
   `authenticationAgent`, `common.xsd:683` area). Same class as H6 (what the client does not hand over), but the README's
   Limits do not name it and its "(in any namespace, at any depth)" claims it. Fix (records / a later round): a README
   Limits clause, and for the adapter lane a read that marks a masked element that held element children. Proposed as
   an owed item (FOR-RECORDS.md).
2. **Minor, does NOT block (a callback host holding a lone surrogate throws out of the parser; H9 MEASURED).**
   `probe.tsv` G3: `Uri.CheckHostName("a\uD800b.example")` = Dns; `Oxpd1EchoOptions.Parse` then throws
   `UriFormatException: Invalid URI: The hostname could not be parsed.` from `CallbackAddress` (`Oxpd1EchoVerb.cs:230`,
   `:258`); the verb calls `Parse` at `:273` with no catch, and `Program.cs` holds none (grep). At BASE the same host was
   taken and the builder threw in `AsyncAsync` after the run folder was made, so the head is strictly better (no
   folder), but P4's "never an exception" does not hold for this host. Reach: a command line that carries a lone
   surrogate (Windows' UTF-16 command line; on macOS and Linux invalid UTF-8 arrives as U+FFFD, which is taken).
   MEASURED beside it (H9): U+00FC, U+00DF, U+0130, U+200B, an emoji, U+FFFD, U+FF0E, U+3002 and `xn--a` are taken as
   Dns and written into the callback address as typed (its length counts the Unicode host, as the client's check does).
   Fix: the address options' printable-ASCII rule on `--callback-host` (and the device host), or the builder's
   exception as a usage error; one E09-family row. Proposed as an owed item.
3. **Info (C1's XML white-space test is pinned by no cell).** My extra mutant `xXmlSpaceLoose` (`XmlSpace` as
   `text.All(char.IsWhiteSpace)`): `Total 352 Failed 0 | red NONE` (`logs/mutants-extra.out`). The head is right:
   MEASURED a result and a record holding only U+00A0 are refused (exit 10) and white space only, or CDATA of white
   space, is taken (`probe.tsv` G1). One row would pin it.
4. **Info (Tuesday's point a; within ASCII the device gets .NET's canonical form).** The ASCII rule refuses none of
   `https://[::1]/agent`, `https://[2001:db8::1]:8443/agent`, `https://lab-host.example:8443/agent`,
   `https://lab-host.example/prompt-%C3%A9`, `https://xn--bcher-kva.example/agent` (each exit 0 and in the envelope as
   typed). It refuses text with a leading or trailing space, tab or line feed (exit 2; `Uri.TryCreate` would have trimmed
   it: DERIVED, not run on BASE), the cost of a pasted address. What reaches the device is `AbsoluteUri` (the writer,
   `Oxpd1Writer.cs:867`, `:891`, `:899`): MEASURED, an upper-case scheme or host is lowered, `:443` is dropped, dot
   segments are removed, `%41%7e` becomes `A~`, `"` `<` `>` `^` `` ` `` `{` `|` `}` and a lone `%` are percent-encoded, a
   `\` in a path becomes `/`, an IPv6 zone (`%25en0`) is dropped, and a `#` or `?` typed inside a host ends the host
   (`https://lab#host.example/agent` goes as host `lab`). Each is a valid URI the dry run prints; none is a character
   outside ASCII and none throws. Not this lane's property; a README sentence could say "sent as .NET writes it".
5. **Info (P1 shapes outside the README's words).** MEASURED taken (register written): the run's id in an attribute of
   another record's OWN `id` element (`<id ref="RUN-ID">OTHER</id>`), and as an element named `ID`, `Id` or `agentId`
   (XML names are case-sensitive; HP's is `id`). Both are "the id where the run does not read it" and close to the
   README's "the id as the text or an attribute of a record's other elements", which does not literally cover the own
   `id` element. Refused as they should be: an own `id` holding a nested `id` (exit 10), `xml:lang` on a record,
   `xml:space` on the result, a deny-listed attribute on the result (masked but still an attribute), the same id in upper
   case, in braces or padded with white space (the landed same-id line).
6. **Info (D7's "four" is the drafter's; six is right).** See AT THE HEAD 3. README `:315` to `:317`.
7. **Info (record notes on the seat's DEVIATIONS).** (1) the typed `cd /dev/null` failed and changed nothing; (2)
   `words.py --control` re-run alone: my run `CONTROL FIRED: 13 of 13`; (3) the Edit tool's raw characters rewritten as
   escapes: check 5 passes at the head (every owned file printable ASCII); (4) V17's refused rows assert V12's set
   (an executed register connects and makes its folder by design), right; (5) V19's extra assertions are additive; (6)
   C4's `callbackHost is null ? 0` equals the async test: a sync echo with any callback option is refused earlier
   (`Oxpd1EchoVerb.cs:213` to `:217`) and an async one without a host just above; (7) see FOUND 6; (8)-(9) the reword
   and ANSWER-1's one hit: my `words.py` over the 363 added lines prints `decided, ruled, approved, instructed 1`, every
   other class 0, and the one line is the README Limits bullet; the commit message is clean and equals the frozen
   `commit-message.txt` byte for byte (383 bytes, `cmp` rc 0); (10) the run-1 folders were moved, not deleted.

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole:** `diff --name-status` six rows, all `M`; numstat 62/10, 34/2, 27/11, 89/0, 9/0, 142/0,
  equal to `compare`'s file list (GET 22:40); ONE commit, parent 504ca043, tree 22c5f214, author and committer the
  repo's `@datasec.com.au` address (masked); `ls-files` 679. Every changed `src/` line and every added test line read.
  The head's `Oxpd1Command.cs` (sha256 f0c6d4ca...) and `Oxpd1EchoVerb.cs` (31f7371b...) equal the green files the
  seat's second mutant run applied to (its `applied:` lines) and mine.
- **Red first** (`g2130/red`; `logs/r-*.log`): restore rc 0; build `0 Warning(s)`, `0 Error(s)`; Lab `Total: 352,
  Errors: 0, Failed: 26`; `[FAIL]` 26, all in V17, V18, E09, E10, E11 (pattern count 26), 26 of 26 followed within five
  lines by an `Assert.<name>() Failure` line: V17 rows 1 to 9 `Equal`; V18 rows 1 and 2 `Null` (the writer threw), rows
  3 to 7 and 10 `Equal`; E09 232 and 200 `Null`; E10 `Null`; E11 rows 1, 2, 3, 4, 7, 8 `Null`. The twelve green rows
  (V17 10 to 12, V18 8 and 9, V19 all, E09 199, E11 5 and 6) and every landed cell passed. Equal to the kit's PREDICTED
  red and to the seat's run.
- **Head green** (`logs/h-*.log`): locked restore rc 0; build 0/0; Lab `Total: 352, Errors: 0, Failed: 0`; whole solution
  `total: 2422`, `failed: 0`, `succeeded: 2418`, `skipped: 4`. Probe tree: build 0 errors, 0 warnings (warnings not
  made errors for my probe), Lab `Total: 357, Failed: 0` (352 + my 5 probe facts, which record and assert nothing).
- **Mutants** (`logs/mutants-seat.out`; the seat's `mutants.json`, sha256 a9239f6c... equal to its STATUS, read by `cat`
  into my scratch; `--list` `LIST: 11 mutants, 6 new cells`; my run of the frozen `mutants_b1.py`, 22:52 to 23:14):
  `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal`, every row's Total, Failed and applied sha256 equal to the seat's
  second run. By ROW (`logs/mt-*.log`): `mResultAttribute` V17 3, 4; `mResultText` V17 1, 2; `mRecordIds` V17 5, 6, 7;
  `mRecordNodes` V17 8, 9; `mAddressAscii` V18 1 to 7 and 10; `mCallbackLength` E09 232, 200 and E10; `mCallbackBound`
  E09 200; `mDelayAsync` E11 1, 3, 8; `mDelaySync` E11 2, 4, 7; `mDelayAsyncBound` E11 3, 8; `mDelaySyncBound` E11 4,
  7. Nothing red outside the six new cells; the clone's status 0 lines after, both files back at f0c6d4ca / 31f7371b.
  My nine extra mutants (`logs/mutants-extra.out`, `MUTANTS: 8 of 9 MATCH, 9 of 9 undone equal`): `xRecordAttrHalf`
  V17 row 9 and `xRecordTextHalf` V17 row 8 (each half of C1 d pinned alone); `xResultNsDecl` (every attribute refused)
  V17 row 10 (the namespace-declaration exemption pinned); `xAsciiUpper` (`<= U+00FF`) V18 rows 3, 6, 7 and
  `xAsciiLower` (`>= U+0020`) V18 row 10 (both ends of the range pinned); `xCallbackPort` (port 1 assumed) and
  `xCallbackNoDigits` (no 32 digits) E09 row 200 (the parser's form pinned); `xIdOwnNsOnly` (own-namespace descendants
  only) V17 rows 5, 6 (any namespace pinned; row 7 stays caught); `xXmlSpaceLoose` red NONE (FOUND 3).
- **Whether ANY answer shape the lab is handed can still hold the same id and let a register through (beyond rows 11
  and 12):** one class, FOUND 1 (masked elements); FOUND 5's shapes are the README's limit class. Thirty shapes in
  `probe.tsv` G1, the control row written.
- **Whether ANY address the three options take can make the envelope's writer throw or reach the device as other than
  typed:** no throw (436 runs, `THREW` 0); never a character outside ASCII; within ASCII .NET's canonical form (FOUND 4).
  Every refusal exit 2 with no folder and no connection (`tls 0` in every row). `--button-target` shares `Address`
  (V18 row 7; not swept by my probe).
- **Whether ANY callback host the parser takes can make the client throw:** NO (every taken host, five ports each,
  `Oxpd1EchoCall.Async` ok; the 199-character host reads 256 at 65535, upper case the same; 200 refused though it fits at
  ports 1 to 8080: the named early refusal). But the parser itself throws on one (FOUND 2).
- **Whether ANY delay the parser takes is at least its wait or time-out:** NO (E11 and `probe.tsv` G4: equal refused,
  one under taken, defaults counted, a repeated option's last value used, `-1` and a padded `00001000` handled).
- **Whether ANY landed cell changed:** NO. `checks_b2.py` on the head's index `CHECKS: 8 of 8 PASS` (check 4: removed
  lines under `tests/` 0, control added 240); every landed cell green in the whole solution.
- **The README sentences against the code** (head): the address sentences (`:80` to `:88`) against `Address` `:777` and
  the error lines `:536`, `:555`; the bound of 100 in UTF-16 code units against `value.Length` (unchanged) and the
  client's `Oxpd1Writer.cs:141`, `:285` (MEASURED 100 units taken, 101 refused, for pairs and combining marks); the read
  before a register (`:97` to `:105`) against `:1053` to `:1092`, wider than the code for FOUND 1; the exit-10 line
  (`:170` to `:173`); the delay sentence (`:222` to `:224`) against `:239`, `:246`; the callback sentence (`:228` to
  `:230`, "at most 199 characters") against `:230` (MEASURED 199 taken, 200 refused); the Limits bullets (`:312` to
  `:317`) against H6 and H15 (the processing instruction MEASURED dropped by the client; "six characters early"
  MEASURED).
- **The stub member used only by V17:** `ResultContent` occurs at `Oxpd1Stub.cs:44`, `:292`, `:294` and in one cell,
  `Oxpd1WriteTests.cs:703` (V17) (`git grep` at the head, `src` and `tests`); added lines only (check 7).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, about 22:54): run 45811257492,
  four jobs attempt 1 success, linux `total: 2422` twice, `succeeded: 2418`, `skipped: 4`, windows `succeeded: 2401`,
  `skipped: 21`, `RULES: clean (679 files)`, `UNIT-TEST FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15
  files)`, `failed Datasec.` lines 0 and 0 (control: 4 `Lab.Tests.dll` lines per leg); check runs beside the four: 0;
  last line `HOSTED 0ae90664aef54febc2624c54e71f35e2b60f1313: PASS`; the control at `--total 2423` printed `FAIL 4`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. TUESDAY'S OWN POINTS

- **(a) C2 against what an operator types:** none of the four named shapes is refused (FOUND 4, each MEASURED taken and
  written as typed). Refused beyond HP's `anyURI`: a host that is not ASCII (typed as `xn--`), a character outside ASCII
  in a path or query (percent-encoded by hand), a space, and a leading or trailing white-space character. **Info**: the
  stricter rule costs an operator one conversion and is said in the README and the error line.
- **(b) C4's length against the real call's:** the parser and `AsyncAsync` call the same `CallbackAddress` with the same
  host string and a path of the same length (`/oxpd1-echo/` and 32 digits; the run's are lower-case hex, no escaping),
  so only the port differs, and 65535 is the longest. Host case: `AbsoluteUri` lowers an ASCII host in both (199
  upper-case letters read 256, MEASURED). The default port 80 is left out (six characters shorter, MEASURED). An IPv6
  host is refused by the parser (`CheckHostName` = IPv6, MEASURED for `::1` and `[::1]`); an IPv4 host is at most 15
  characters (72 at port 65535, MEASURED). A host that is not ASCII is counted in Unicode by both (MEASURED). So the
  parser never takes a host the client then refuses; it can refuse one the client would take (the named early refusal).
  **No finding**, beyond FOUND 2 (the builder throwing in the parser).
- **(c) C1 against HP's schema:** in the committed xsd the record holds `id`, `name`, `localizedName`,
  `localizedDescription`, `authenticationAgent` (`authentication.xsd:7` onward); `name="id"` occurs once in
  `authentication.xsd` and 0 times in `common.xsd`; `xs:attribute` 0 and 0; `nillable` 0 and 0; `mixed` appears in
  `common.xsd` only inside a documentation word (`MixedLetterLegal`, line 290); `xs:any` only in `XMLElementContainer`
  (`common.xsd:1098` to `:1111`), which `authentication.xsd` never names (0). So every answer in HP's shape passes the
  four refusals (DERIVED; the landed cells holding HP-shaped records stay green). White space and namespace declarations:
  white space only as text of the result or a record, CDATA of white space, a namespace declaration on the result (V17
  row 10) and on a record: each taken (MEASURED). **No finding** (FOUND 3: the white-space test is unpinned).
- **(d) The ANSWER-1 word hit:** `words.py` over the 363 added lines: one hit, `added.txt:118`, the README line `- The
  read before a register cannot see an id held in a comment or a processing instruction (the client drops both`; 0 in
  the commit message. Within ANSWER-1's bound.

## 3. ADVERSARIAL BEYOND THE KIT (three shapes outside each property)

- **P1** (no register on an unreadable answer): a second `id` inside a masked element, HP's own `networkCredentials`
  among them: written (FOUND 1); an attribute on another record's own `id` element, and `ID`/`Id`/`agentId` elements:
  written (FOUND 5, the limit class); a result or record holding only U+00A0: refused (covered; unpinned, FOUND 3).
- **P2** (an address outside U+0021 to U+007E is a usage error, never an exception): U+0000 and U+007F in a path:
  exit 2, no folder (covered); every printable character in host, path, query: no exception (covered; canonical form,
  FOUND 4); a leading or trailing tab or line feed: exit 2 (covered).
- **P3** (the bound counts UTF-16 code units): 100 and 101 basic-plane letters; 49 pairs plus 2 and plus 3 letters; 50
  and 51 combining sequences: exit 0, 2, 0, 2, 0, 2 (covered; H16's limit: a combining sequence counts each unit).
- **P4** (a callback address over 256 is refused before any folder, never an exception): a lone surrogate in the host:
  the parser throws (FOUND 2); a host with a trailing dot at 199: taken, 256 (covered); labels of 64 and hosts over 253:
  refused by `CheckHostName` or the length rule, never the client (covered).
- **P5** (the delay is shorter than the wait): async `--timeout-seconds 1` with a delay of 59999 and a wait of 60: taken
  (the async rule reads the wait only: D8, the device answers at once, RELAYED); a repeated `--delay-ms`: the last wins
  and is checked; the defaults with the options in another order: checked (covered).
- **P6** (no landed cell changes): removed lines under `tests/` 0; the stub gains 9 lines only; Lab 352 / 0 and the
  whole solution 2422 / 0 locally and on both legs (covered).

## 4. SCANS

- **gitleaks 8.30.1:** control FIRST, a token built in-process from two halves and 36 random characters, never printed,
  outside the clone: rc 1, `leaks found: 1`, moved to `g2130/_quarantine/gl-control-1`; then `gitleaks git` over
  `504ca043..0ae90664` rc 0 (`no leaks found`); the six head blobs, the commit's message, the seat's `mutants.json` and
  the whole diff as `1.txt` to `9.txt` in a new folder: rc 0, `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 363 added lines (`checks_b2.py`'s
  `added.txt`; 363 equals the commit's insertions) and the commit message: one hit, ANSWER-1's (section 2 d);
  `B2[0-9]{3}` and `X7[0-9]` 0 and 0.
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#56`, `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)` (the squash body writes the node as `<?...?>`, not the XML term); `pr-body.md`: `product owner`
  1 and `coordinator` 2 (the "Who decides" section) and the attribution line's emoji bytes, every other class 0;
  `B[12][0-9]{3}` and `X7[0-9]` 0 in all four; `build/squash_scan.py` (the head's, equal to BASE's: `diff --quiet` over
  `build` and `.github` rc 0) with `#56`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`; gitleaks over
  this folder's seven files and the `#56` subject under neutral names, the control re-planted first (rc 1, quarantined
  to `g2130/_quarantine/gl-control-2`): rc 0, `no leaks found` (23:40).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). The chain's publish and release guard and `run_step.py`'s neutral
scan (RELAYED from the seat; equal on the hosted legs, my read: GUARD 14 and 15, the hosted neutral scan);
`repo_rules.py` (no `--source-documents`) and the `build/tests` unit tests I DID run on my clone: `RULES: clean (679
files)` with the R5 note, `Ran 117 tests`, `OK`. The whole solution after the mutants (the clone's status is 0 lines
after the tool's undo and both files are back at the head's hashes, so the measured head is the bytes that ran). The
device host (first word) under non-ASCII and lone-surrogate hosts (H9, UNMEASURED). `--button-target` in my address
sweep (it shares `Address`; V18 row 7). Any probe on Linux or Windows (macOS arm64 only). Any device.

## OUTSIDE THE FENCES

None written outside my two folders. Writes: this folder and `fleet/state/s331/g2130/` only (my clone, its two
worktrees, logs, scratch, quarantine). No pull request, no push (the clone's push URL is `invalid://no-push`), no
re-run of a hosted job, no `cd` run, nothing deleted, no printer or device, no Azure, nothing to any person, no Jira.
Every gh call a GET under the project's GH_CONFIG_DIR. Reads of the project folder, by path only (no recursive read):
the seat's STATUS, `CLAUDE.md` (line 82 and its sha256), the seat's `mutants.json` (copied into my scratch by `cat`),
the `.tools/` listing and the lock folder's absence. Four hook refusals, each a STOP for that action: a `cd` in my first
command (re-issued with absolute paths), an `echo` separator starting with `=` (re-issued as `----`), a `git checkout`
whose path was an unexpanded variable (re-issued with the literal scratch path), and a stray `rm -f /dev/null` I typed by
mistake (refused; nothing deleted; re-issued without it). One read of mine ran wider than meant: a `grep -rn .` and `ls`
with no folder ran from the TUESDAY working folder (not the OXPd folder) for under two minutes before I stopped it
(read-only; its output not used). No print of `kam_rulings_today.sh` or `kam_msgs.sh` was made or saved. No background
process of mine is left running; the wave lock is absent.
