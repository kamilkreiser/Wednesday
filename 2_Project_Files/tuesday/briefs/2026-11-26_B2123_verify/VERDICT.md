GATE B2123: GO WITH FINDINGS @ cd2a3e1 on main c73cda4

Gate G1, ROUND 1 OF 2 of lane OX-B kit 1 (the lab tool `oxpd1`: `LabFiles.cs` and the Lab README; owed 108, 111, 145,
142, 127, 150), one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2122 (seat X78; stamp S4: Q1
"a" kit 1 of 2, Q2 "a" the seat writes the code to the kit's specification, each in words; Q3 to Q10 the defaults; S8
the canonical heavy runner 31adedc8; every choice the coordinator's, none the product owner's). Head
`cd2a3e13ea8dbaf044ced35b959fc4f3cd2fa7e6` on `b2122/lane-b-lab-files`, ONE commit, one parent = main
`c73cda4cdf7bf5cd1c6c43cfc20a4c5c400c3809` (PR 54). Main and the branch did NOT move during the gate (gh api -X GET
13:11:58 and 13:46:52 AEDT; open pull requests 0 both times; open code-scanning alerts 0). Read and measured
2026-11-26 13:11 to 13:50 AEDT in my scratch `fleet/state/s330/g2123/`: `clone` (clone.py draft: push URL
`invalid://no-push`, no identity; detached at the head; the mutants ran here), worktrees `red` (BASE plus the head's
three test files, `git diff --quiet c73cda4c -- src` rc 0) and `probe` (the head plus one probe file of mine,
`GateProbeTests.cs` in the Lab's tests, never committed, never pushed). Every heavy job through the kit's `heavy.py`
(sha256 31adedc8..., my copy 8 of 8 equal to THE TOOLS) and the wave lock, taken per job and released, one at a time
(lock waits 0 each; load-gated, load1 reached 22.5 from other seats); the 34 released lock folders are mine, in
`g2123/_quarantine/locks/`; no other holder's lock or file touched; the lock absent at 13:46.

**AT THE HEAD (where a record or agent disagrees with what Tuesday stamped):**
1. **H9 is not a quiet limit: it is a false `nothing is owed`.** The kit names it "counted as a folder without a list
   (DERIVED, UNMEASURED)". MEASURED: a run folder of mode 0400 or 0600 holding an executed register, beside two clean
   lists, prints `nothing is owed` and ends 0 (FOUND 1).
2. **The 40-link bound that ends a link loop is in the code but pinned by no cell** (my mutant without `links++`: red
   NONE). The kit's H10 says loops are read as written by the landed rule with "R07 and S14 green": neither holds a loop
   (FOUND 2).
3. The seat's H13b ("a `..` typed after a link", UNMEASURED) is MEASURED consistent: `GitWorkTreeHolding` and
   `RunRecorder.Create` (`RunRecorder.cs:33`) both take `Path.GetFullPath` of the typed path, so the rule reads the
   folder the recorder makes (made at `a9/x9`, not under the link's target; into a tree: refused).
4. The README's new Limits clause "a certificate file that is a named pipe with no writer blocks the run the same way
   (UNMEASURED)" is now MEASURED (blocked 5 s, released only when my writer opened the pipe).

**BLUF.** The head does what its six items ask, on every path I could build. **`undo-owed` never says `nothing is
owed`, never ends 0 and never throws beside a folder it cannot open or list** (run folder modes 0000, 0100, 0300, a run
folder that is a link to a mode-000 folder, session modes 0100, 0300, 0400: each exit 11 naming the folder); **every
write kind has its own family arm and an unnamed kind throws**; **no path yields more than 64 KiB to the certificate
reader** (a link chain, a hard link, `/dev/zero`, a link to it, a sparse 10 GiB file, a pipe with an endless writer: each
refused at once; a growing file is taken only while it is at most 64 KiB); **no link shape the system resolves into a
work tree passes the run folder rule** (eighteen shapes, each refused in a tree and made where the system makes it
outside one; loops and chains past the system's limit end in 0 ms and the system refuses the folder); **no landed cell
changed** (removed lines under `tests/` 0). Red first exactly the 6 rows (`Total: 314, Errors: 0, Failed: 6`, each by
assertion, my run); green the Lab `Total: 314, Failed: 0` and the whole solution `total: 2384`, `failed: 0`,
`succeeded: 2380`, `skipped: 4` (my run); `MUTANTS: 6 of 6 MATCH, 6 of 6 undone equal` (my run of the seat's rows
file through the frozen tool); `HOSTED cd2a3e13...: PASS` (my read; control FAIL 4). **Two Minor findings (H9's false
clean; the link bound unpinned), six Info. None blocks the landing.** Tuesday's points: (a) the U07 row 6 re-pin is the
safe side D8 allows and a BETTER message than the kit's derived words: **Info**; (b) `RealPath` has no unbounded walk,
`..` at the root stays the root, and the 40-link bound holds on every path (but is unpinned: FOUND 2); (c) the bounded
read holds for a growing file and for a pipe with a writer; a pipe with no writer blocks (H8).

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (a run folder that can be listed but not entered gives a false `nothing is owed`, exit 0;
   the kit's H9, a stated coordinator's limit (D3, Q3 default), now MEASURED).** `logs/probe.tsv` G03: r1 a register,
   r2 its unregister, r9 a register, then r9 mode 0400 (or 0600): `undo list: 2 executed writes in 2 run folders`,
   `nothing is owed`, exit 0. Why: the listing (`LabFiles.cs:411`) succeeds with read permission, so C1's catch is not
   reached, and `File.Exists` of r9's list (`:421`) is false without search permission, so r9 counts as a folder
   without a list. Harm: an operator told nothing is owed skips the undo of a write that may be on the device. Reach:
   low (the lab makes its folders with the system's default mode; only a hand-changed mode makes this shape). The
   README's sentence "It says `nothing is owed` only when it read at least one list, every list holds an entry line,
   every line was read" (README `:186` to `:187`) reads wider than the code, and neither the README's Limits nor the
   pull request named it before this gate (pr-body.md now does). Fix (kit 2 or a later round): the kit's Q3
   alternative (a listing that names `undo-list.tsv` while the list cannot be found or read is unreadable), or a
   README Limits line. Proposed as an owed item (FOR-RECORDS.md).
2. **Minor, does NOT block (the 40-link bound of `RealPath` is pinned by no cell).** My extra mutant `xNoLinkCount`
   (`links++;` removed, `LabFiles.cs:146`): `Total 314 Failed 0 | red NONE` (`logs/mutants-extra.out`). Without it a
   link loop on the run folder's path would never end (DERIVED: each followed link puts its text's parts back in front
   of the walk, and nothing else ends the loop while `LinkText` returns a text). The code is right: MEASURED
   (`probe.tsv` G01) a self loop, a two-link loop and a three-link loop holding a `..` each return in 0 ms, read as
   written, and the system then refuses the folder (exit 5, `IOException`, nothing made), in a tree and outside one.
   No landed cell holds a loop (`grep` of `CreateSymbolicLink` over the Lab tests: Y05, S14 and this lane's cells
   only), so the kit's H10 "R07 and S14 stay green" proves nothing about loops. Fix: one S16-family row "a link loop on
   the run folder's path" (ends, exit 5, nothing made). Proposed as an owed item.
3. **Info (the read loop of the bounded certificate read is pinned by no cell).** `xSingleRead` (the `while` read as
   one `if`): red NONE: a regular file returns whole in one read. The loop is needed for a source that returns short
   reads: MEASURED, a pipe written in 100-byte pieces is read whole and taken (`probe.tsv` G02). A cell cannot make a
   pipe without starting a program (the kit's H8). Right as written.
4. **Info (`_ = entries.MoveNext()` is not what opens the run folder).** `xNoMoveNext` (`_ = entries.Current;`): red
   NONE: on .NET 10 on macOS the enumerator's construction (`EnumerateFileSystemEntries(...).GetEnumerator()`) already
   opens the folder and throws; the `MoveNext` is redundant and harmless. The property is pinned by `mFolderOpen` (the
   whole listing replaced: U06 rows 1 and 3).
5. **Info (pipes and non-folders in `undo-owed`).** An undo list that is a named pipe with no writer blocks `undo-owed`
   (MEASURED: blocked 5 s; when my writer opened and closed it, exit 11 `holds no entry line`); the README's `undo-owed`
   section does not name it (the credentials and certificate pipes are named in Limits). Entries of the session that
   are not folders (a dangling link, a link to itself) and an empty folder are passed silently (`nothing is owed` beside
   two clean lists, MEASURED): not run folders by design; a run folder whose link target was moved away is one of them.
6. **Info (the Windows leg tests none of the permission and link rows).** U06 (3 rows), U07 rows 4 to 6, U09 rows 3 and
   4 and S16 (2 rows), ten rows, return at once on Windows and count as passed there (`succeeded: 2363` = total minus
   the 21 skipped). D9's rule and the landed precedent (Y05, S14); the early returns are exactly the permission and
   link rows (read in the diff: U07 rows 1 to 3, U09 rows 1 and 2 and all of U08 run on Windows).
7. **Info (Tuesday's point a: the U07 row 6 re-pin).** See section 2.
8. **Info (record notes).** (a) The seat's DEVIATION 4 (`rm -f` of its own byte copy of the first red log): no evidence
   lost: the first red run is kept whole at `<lane>/_quarantine/red-lab.first-run-before-D8-repin.log` (8069 bytes,
   `Total: 314, Errors: 0, Failed: 7`, the seventh U07 row 6 with the message the STATUS quotes), and the second at
   `logs/red-lab.log` (equal to `red-lab2.log`, `cmp` rc 0, `Failed: 6`); still a breach of never-delete, as the seat
   says. (b) DEVIATION 5 (README reflowed after the green and the mutants): moot for proof: the README is an input of no
   build (the Lab csproj names no README, `grep -c -i readme` 0), the seat's mutants applied to the committed
   `LabFiles.cs` (its `applied:` sha256 6017d23c equals the head's blob), and my red, green, mutant and probe runs are
   all on the committed head. (c) DEVIATION 7 (`mSessionList`'s filter `when (unlisted is ArgumentNullException)`): the
   catch no longer catches `UnauthorizedAccessException`, the same property as `when (false)`; my run reddens U06 row 2
   alone. (d) DEVIATION 1 (CLARIFICATIONS.md C-1 to C-84 not read at boot): noted; no choice of this lane rests on a
   clarification I found (not re-read whole by this gate). (e) The squash body is a new text for the landing (the
   commit's body is the attribution line only). (f) On macOS the system's own link limit is below the rule's 40: a
   chain of 39 links is refused by the system (exit 5, `IOException`) while the rule resolves it (and refuses it in a
   tree): the safe side.

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole:** `diff --name-status` five rows, all `M`; numstat 102/29, 20/12, 50/0, 37/0, 126/0,
  equal to `compare`'s file list (GET 13:12); ONE commit (`rev-list --count` 1), parent c73cda4c, tree 7c987de4,
  author and committer the repo's `@datasec.com.au` address (masked); `ls-files` 679; the commit's message equals the
  frozen `commit-message.txt` byte for byte (373 bytes, by `cat-file`). Every changed `src/` line read (`LabFiles.cs`
  and the README) and the three test files' added lines read whole. The head's `LabFiles.cs` sha256 6017d23c... equals
  the green file the seat's mutants applied to.
- **Red first** (`g2123/red` = BASE + the head's three test files; `logs/r-*.log`): restore rc 0; build `0 Warning(s)`,
  `0 Error(s)`; Lab `Total: 314, Errors: 0, Failed: 6`; `[FAIL]` 6: U06 rows 1, 2, 3, U08 row 2, U09 row 3, S16 true,
  6 of 6 followed within five lines by an `Assert.<name>() Failure` line (`Equal`, `Equal`, `Null`, `Contains`, `Null`,
  `Throws`); the eleven green rows (U07 all six included, so the D8 re-pin holds on BASE) and every landed cell passed.
  Equal to the kit's PREDICTED red (after the D8 re-pin) and to the seat's second red run.
- **Head green** (`logs/h-*.log`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; Lab `Total: 314, Errors:
  0, Failed: 0`; whole solution `total: 2384`, `failed: 0`, `succeeded: 2380`, `skipped: 4`. Probe tree: build 0/0,
  Lab `Total: 360, Failed: 0` (314 + my 46 probe rows, which record and assert nothing).
- **Mutants** (`logs/mutants-seat.out`; the seat's `mutants.json`, sha256 8fe94947... equal to its STATUS, read by
  `cat` into my scratch; `--list` `LIST: 6 mutants, 5 new cells`; every OLD once in the head's file; my run of the
  frozen `mutants_b1.py`, 13:24 to 13:31): `MUTANTS: 6 of 6 MATCH, 6 of 6 undone equal`, every row's Total, Failed and
  applied sha256 equal to the seat's run. By ROW (`logs/mt-*.log`): `mFolderOpen` U06 rows 1 and 3; `mSessionList` U06
  row 2; `mFamilyDefault` U08 row 2; `mBoundPath` U09 row 3; `mBoundShort` U09 rows 2 and 3; `mLexical` S16 true.
  Nothing red outside the five new cells; the clone's status 0 lines after and HEAD still cd2a3e13, `LabFiles.cs`
  6017d23c. My six extra mutants (`logs/mutants-extra.out`): `xNoneOld` (the verb's `none` back to `Files == 0`) U06
  rows 2 and 3 (so C1 c is pinned); `xBoundGe` (`>=`) U09 row 1 (the exact bound pinned); `xAbsNoRestart` (an absolute
  link text walked from the current folder) S14's three `intoTree` rows and S16 true (the absolute restart pinned, by a
  landed cell too); `xNoLinkCount` red NONE (FOUND 2); `xSingleRead` red NONE (FOUND 3); `xNoMoveNext` red NONE (FOUND
  4).
- **Whether `undo-owed` can still print `nothing is owed` or end 0 beside a folder it could not open or list, or throw
  on one:** NO for a folder it cannot open or list (`probe.tsv` G03: run folder modes 0000, 0100, 0300 and a run folder
  that is a link to a mode-000 folder: `unreadable: r9 (the run folder cannot be opened)`, exit 11; session modes 0100
  and 0300: `unreadable: the session folder cannot be listed`, exit 11; session mode 0400: each run folder named
  unopenable, exit 11; a list of mode 000: named unreadable, exit 11; no exception in any). YES for a run folder it
  CAN list but not enter (FOUND 1, H9).
- **Whether ANY write kind can reach `Family` without its own arm:** NO. `Oxpd1WriteKind` holds 8 values (U08 row 1
  asserts exactly 8, so a ninth fails it), each in a named arm (`:487` to `:490`); the default throws (`:491`), pinned by
  `mFamilyDefault`. `Family`'s one caller (`:467`) gets only kinds `Parse` read by name (`:500`; an integer text such as
  `99` is not a name).
- **Whether ANY path can yield more than 64 KiB to the certificate reader:** NO. By construction (one buffer of
  65537 bytes, `:278`; more than 65536 read refused, `:289`; `bytes = buffer[..read]`, `:295`), and MEASURED
  (`probe.tsv` G02): a chain of three links to a 65537-byte file, a hard link to it, `/dev/zero`, a link to `/dev/zero`,
  a sparse 10 GiB file, a pipe with a writer of 100000 bytes and a pipe with an endless writer (stopped after 73728
  bytes when the reader closed): each `refused: the certificate file is missing or larger than 65536 bytes` in 0 ms.
  A folder and a link to a folder: refused as missing. A file of mode 000: `cannot be read`.
- **Whether ANY link shape the system resolves into a work tree passes the run folder rule:** NO (`probe.tsv` G01, each
  shape built twice, with and without `.git` in `d1/repo9`, run through `oxpd1 lab-cert` in the test process): a
  relative link through another link (S16's shape), a relative link to a relative link to an absolute one with `..`
  after, an absolute link inside a relative one, `..` past the root (twenty-odd `..` then the absolute path), `.` and
  `//` in the text, a trailing slash, an absolute text holding `..` through a link, chains of 30 and 39 links, a link to
  a file, a dangling link whose text walks `..`, and a `..` typed after a link: inside the tree each exit 9 naming
  `d1/repo9`, nothing made; outside it each made where `RealPath` said (or refused by the system, exit 5). Loops and
  chains of 41 and 45 links: exit 5 (the system's `ELOOP`), nothing made, the walk 0 ms.
- **Whether ANY landed cell changed:** NO. `checks_b1.py` on the head's index (`git diff --cached c73cda4c`) `CHECKS: 8
  of 8 PASS` (check 4: removed lines under `tests/` 0, control added 213); the three test files gain lines only.
- **The README sentences against the code** (head): the callback sentence (README `:225` to `:230`) says what
  `CallbackMessage` says at main (`Oxpd1Echo.cs:207` to `:226`, through `ReadTextAnswer`, `Oxpd1Soap.cs:236` to `:277`:
  one body element, `AsyncEchoStringComplete` with no attribute but a namespace declaration, ONE text-only non-empty
  `message`, nothing beside it but XML white space) and the 400 answers (`Oxpd1EchoVerb.cs:518` to `:524`); text at the
  envelope level is read past by that reader (gate B2112 FOUND 1's class, inherited, Info). The "Known, not changed
  here" bullet is gone (check 8: 0, BASE 1). The unreadable folders named (README `:190` to `:193`, `LabFiles.cs:403`,
  `:416`, `:552`), the exit codes (`:196` to `:197`), the bounded read (`:108` to `:111`, `:272` to `:295`), the link
  rule (`:242` to `:246`, `RealPath`), the pipe clause (`:303` to `:304`, MEASURED by this gate). Wider than the code:
  README `:186` to `:187` against H9 (FOUND 1).
- **The Windows early returns only in the permission and link rows:** yes (FOUND 6).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, about 13:24): run 45739684402,
  four jobs attempt 1 success, linux `total: 2384` twice, `succeeded: 2380`, `skipped: 4`, windows `succeeded: 2363`,
  `skipped: 21`, `RULES: clean (679 files)`, `UNIT-TEST FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15
  files)`, `failed Datasec.` lines 0 and 0 (colour codes stripped; control: 4 `Datasec.Suite.Lab.Tests.dll` lines per
  leg, `passed` on each); check runs beside the four: 0; last line `HOSTED cd2a3e13ea8dbaf044ced35b959fc4f3cd2fa7e6:
  PASS`; the control at `--total 2385` printed `FAIL 4`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. TUESDAY'S OWN POINTS

- **(a) The U07 row 6 re-pin (DEVIATION 2):** the safe side D8 allows: exit 11, `nothing is owed` absent (asserted in
  the cell), and the list counted (`1 run folders`). MEASURED twice: the seat's first red log and my red run (U07 row 6
  green on BASE with the re-pinned words). BETTER than the kit's derived words: `no undo list was read` would have
  told the operator "no folder directly inside the folder given holds undo-list.tsv (a session of dry runs only has
  none)", which is false (r1 holds an entry of that name whose target is gone: damage) and points at the wrong cause;
  `unreadable: r1/undo-list.tsv (FileNotFoundException) (not shown)` names the folder and the file and says why. The
  exception's name beside a file that is "there" is a small puzzle for a reader who does not know links; acceptable.
  **Info**, no change asked.
- **(b) C4's walk (`RealPath`, `LabFiles.cs:122` to `:163`):** no unbounded walk: the only way the list of parts grows
  is a followed link (`:153`), and every followed link increments `links` (`:146`) and is followed only while `links <
  MaxLinks` (`:143`); after 40, a link part is read as written (`Directory.Exists`, `:157`, then the rest kept as
  written); `.` and `..` only consume parts. A cycle therefore ends after at most 40 followed links (MEASURED: three
  loop shapes, 0 ms). `..` above the root: `Path.GetDirectoryName("/")` is null and `?? current` keeps the root (`:138`;
  MEASURED: "`..` past the root" refused in a tree, made at `d1/repo9/sub/run9` outside). The bound holds on every
  path: it counts every link followed in the whole walk, nested texts and the system's own links (macOS `/var`)
  included; the systems' own limits are at or below it (macOS refused a chain of 39 links, MEASURED; Linux's is 40,
  DERIVED, not run). A recursion is gone (the landed version recursed per link). Unpinned by a cell (FOUND 2).
- **(c) C3's bounded read (`:272` to `:295`):** a file that grows while read: 319 reads while a writer appended 64-byte
  pieces from 60000 to 316000 bytes: 5 taken (each while the file was at most 64 KiB when read; at most 65536 bytes
  kept, by construction), 314 refused, 0 other (`probe.tsv` G02). A pipe with a writer: read until the writer closes
  or the buffer fills: the CA written whole or in 100-byte pieces is taken; 100000 bytes or an endless writer refused
  (the writer gets a broken pipe after 73728 bytes). A pipe with no writer blocks in the open (MEASURED; H8, now named in
  the README's Limits).

## 3. ADVERSARIAL BEYOND THE KIT (three shapes outside each property)

- **P1** (undo-owed and an unlistable folder): a run folder listable but not searchable (mode 0400, 0600): a false
  `nothing is owed` (FOUND 1, named limit H9); a session folder listable but not searchable (0400): each run folder
  named unopenable, exit 11 (covered); a run folder that is a link to a mode-000 folder: named, exit 11 (covered); an
  undo list that is a pipe with no writer: blocks (FOUND 5).
- **P2** (every kind has an arm): `(Oxpd1WriteKind)99` throws (U08); a ninth kind added later reddens U08 row 1's count
  (covered by construction); an integer kind text in a list (`99`) is refused by `Parse`'s name check (covered, H11).
- **P3** (at most 64 KiB to the reader): a link chain, a hard link, `/dev/zero` and a link to it, a sparse 10 GiB file,
  an endless pipe, a growing file: covered (section 1, 2c); a pipe with no writer blocks (H8, a named limit).
- **P4** (the system's folder for a path with links): an absolute link inside a relative one, `..` past the root, a
  loop, a chain past 40, a dangling link with `..`, a link to a file, a typed `..` after a link: covered or refused by
  the system (section 1); a Windows junction or a drive-relative text (`\x`): NOT built (Windows returns early;
  `Path.GetPathRoot` of a rooted text without a drive would restart at `\`: DERIVED, a named limit for Windows).
- **P5** (the undo read's landed shapes keep their results): U01 to U05 and the CA store's U07/U08, T08, S11, S12,
  S14, R07, Y05, Y06 green at the head (the whole solution 2384 / 0 locally and on both legs); U07's six rows green on
  BASE and the head: covered.
- **P6** (no landed cell changes): removed lines under `tests/` 0; the Lab 314 / 0; the probe tree 360 / 0: covered.

## 4. SCANS

- **gitleaks 8.30.1:** control FIRST, a token built in-process from two halves and 36 random characters, never printed,
  outside the clone: rc 1, `leaks found` 1 line, moved to `g2123/_quarantine/gl-control-1`; then `gitleaks git` over
  `c73cda4c..cd2a3e13` rc 0 (`1 commits scanned`, `no leaks found`); the five head blobs, the commit's message, the
  seat's `mutants.json` and the whole diff as `1.txt` to `8.txt` in a new folder: rc 0, `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 335 added lines of `BASE..head`
  (`scratch/checks/added.txt`, made by `checks_b1.py`; 335 equals the commit's `335 insertions`) and the head's commit
  message: every class 0, `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0 (control: the kit counts 24 lines).
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#55`, `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 1 and `coordinator` 2 (the "Who decides" section), 4 bytes
  outside ASCII (the attribution line's emoji), every other class 0; `B[12][0-9]{3}` and `X7[0-9]` 0 in all four;
  `build/squash_scan.py` (the head's, equal to BASE's: `build/**` and `.github/**` not in the diff, `diff --quiet` rc
  0) with `#55`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`; gitleaks over this folder's seven
  files and the `#55` subject under neutral names, the control re-planted first (rc 1, `leaks found`, quarantined to
  `g2123/_quarantine/gl-control-2`): rc 0, `no leaks found` (13:49).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). The chain's publish and release guard, `repo_rules.py`, the unit tests
of `build/tests` and `run_step.py`'s neutral scan (RELAYED from the seat; equal on the hosted legs, my read: `RULES:
clean (679 files)`, `Ran 117 tests`, GUARD 14 and 15, the hosted neutral scan). The whole solution after the mutants (the
clone's status is 0 lines after the tool's undo, HEAD is cd2a3e13 and `LabFiles.cs` is 6017d23c, so the measured head is
the bytes that ran). Linux's own link limit and the probes on Linux (the probes ran on macOS arm64 only). A count of the
cells' temporary folders left with a changed mode (my shell's view of the temporary folder showed none of the tests'
folders, so the count is not a measurement; every mode is restored in a `finally`, by reading). Any device.

## OUTSIDE THE FENCES

None. Writes: this folder and `fleet/state/s330/g2123/` only (my clone, its two worktrees, logs, scratch, quarantine).
No pull request, no push (the clone's push URL is `invalid://no-push`), no re-run of a hosted job, no `cd`, nothing
deleted, no printer or device, no Azure, nothing to any person, no Jira. Every gh call a GET under the project's
GH_CONFIG_DIR. Reads of the project folder, by path only (no recursive read): the seat's STATUS, `CLAUDE.md` (lines 7,
55, 56, 82 and its sha256), the seat's `mutants.json` (copied into my scratch by `cat`), its two red logs and the list
of its `logs/` folder; nothing of the project's was written but what `heavy.py` does under the wave lock (the lock
folder, moved to my quarantine after each job). Two hook refusals, each a STOP for that action and re-issued in an allowed
form: an `echo` separator starting with `=` (zsh expansion; re-issued as `----`) and a `git switch` whose path was an
unexpanded variable (re-issued with the literal scratch path). My probe started
`/usr/bin/mkfifo` and `/bin/ln` inside the test process to build its pipes and hard link (my probe only, never
committed). No print of `kam_rulings_today.sh` or `kam_msgs.sh` was made or saved. No background process of mine is
left running; the wave lock is absent.
