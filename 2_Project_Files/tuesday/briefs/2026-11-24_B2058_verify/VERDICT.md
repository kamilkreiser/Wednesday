GATE B2058: GO WITH FINDINGS @ 105b346 on main 89a10a1

Gate G1 (device-WRITE code path: the read that gates `EnableService`, the run-folder rule that keeps a panel image out of
a git tree, and a capture refusal on the password's bytes), ROUND 2 OF 2 of lane L1, one Opus reader (claude-opus-5-5),
in-session, read-only. OXPd 2, lane L1, kit B2053 (seat X65; Q1 and Q2 "a" in words at stamp S4, Q3 to Q9 the defaults;
each the coordinator's, not the product owner's). Head `105b34653b4d14f6edfc395fb1a650f65670026a` on
`b2053/l1-round2-found-1-3`, ONE commit, one parent `89a10a1ba26a16aae7996e059d548bf53531fd44` (main = PR 47's squash; no
rebase). Main did NOT move during the gate (89a10a1b by a fresh clone at 20:44 and by gh api -X GET at 20:51); open pull
requests 0; the branch at 105b3465 at both reads. Read and measured 2026-11-24 20:43 to 21:20 AEDT in my scratch
`fleet/state/s324/g2058/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity), worktrees `w` (BASE +
`1-red.diff` for RED, then + `2-fix.diff` = the head's tree, then + a gate probe file, now
`_quarantine/G2058Probe.cs.txt`; `w` equals the head again at the end: `git diff --stat 105b3465` empty) and `rules`
(105b3465, untouched). Every dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the
wave lock, one at a time (42 released lock folders, all mine, in `g2058/_quarantine/locks/`; lock waits 0 to 2; seat X66
of kit B2056 held the lock between my jobs once, never touched; the lock absent at the end). Origin by `gh api -X GET`
under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull request, no re-run; no
printer, no device, no Azure; the M577 not touched; nothing deleted (moved to `_quarantine`).

**BLUF.** The head is BASE plus the two frozen patches byte for byte (temporary index: red tree `5599f157`, both-patches
tree `72c05b08` = `105b3465^{tree}`); the ten tools equal THE TOOLS' sha256 in the drafter's source, the seat's
`.tools/b2053/gate` and my copy (10 of 10 each); the commit message equals `commit-message.txt` (400 bytes). Nine paths,
all M, numstat equal to the kit (gh compare: ahead 1, behind 0, 9 files); `checks_r2.py` 10 of 10 with every control.
Red first: adapter `Total: 55, Failed: 4`, Lab `Total: 229, Failed: 8`, 12 of 12 `[FAIL]` lines each followed by an
`Assert.Equal() Failure` line, exactly THE CONTROLS' cases. Green 2171 / 0 / 2167 / 4 (twice: before and after the
mutants). `MUTANTS: 10 of 10 MATCH, 10 of 10 undone equal` (my run of the frozen tool). Hosted push run 45366993513
`HOSTED 105b3465...: PASS` (my hosted3.py read). **The G1 questions:** every one of gate B2052's FOUND 1 to 3 shapes is
now closed (probe A's four rows exit 8 with 0 enables; probe B's password row exit 8, nothing saved; probe C1 exit 9,
nothing made). Two narrower residual shapes of the same two findings remain, MEASURED: an answer HP's schema refuses
that is still read as `false` (text beside `enabled`, an attribute on the response element: ONE `EnableService` sent,
undo entered, printed and owed), and a run folder whose real path is inside a work tree that is still accepted (a
relative link whose target passes `..` through another link: `panel.png` written inside the tree). Both are Minor, the
same class and harm as round 1's FOUND 1 and 2, and make two README sentences over-claim; none blocks the landing.

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (FOUND 1 residual: five answers HP's schema refuses are still read as `false`, ONE
   `EnableService` is sent).** `Oxpd1Soap.cs:174`: the `TextOnly` rule counts the response's ELEMENTS
   (`first.Elements().Count() != 1`) and the result's attributes, not the response's text nodes or the response
   element's own attributes. MEASURED (probe A, the lab tool in process against the gate's TLS stub on 127.0.0.1; each
   body also validated against HP's committed `test.xsd` with .NET's validator): `junk<enabled>false</enabled>`,
   `<enabled>false</enabled>junk`, `<![CDATA[junk]]><enabled>false</enabled>` (text beside `enabled`), an unqualified
   attribute on `IsServiceEnabledResponse`, and `xsi:nil="true"` on `IsServiceEnabledResponse`: each HP schema errors 1,
   exit 0, `IsServiceEnabled 1 EnableService 1`, the list row and the printed undo. `oxpd1 read --read IsServiceEnabled`
   on `...</enabled>junk`: exit 0, prints `false` (A9). The kit named "text beside" as H7 ("left as landed", DERIVED) but
   the README Limits do not; an attribute on the response element is in no row of H1 to H21. README sentences that
   over-claim: adapter `README.md:43` "that one element alone in the response" and Lab `Commands/Oxpd1/README.md:95`-`:96`
   "ONE `enabled` element ... alone in the response". Harm bounded exactly as round 1's FOUND 1 (the undo is entered
   before the send, printed and owed; worst case the README's non-atomic case). Fix when next touched: also refuse a
   non-white-space `XText` among `first.Nodes()` and any non-declaration attribute of `first`; or name the shapes in
   Limits.
2. **Minor, does NOT block (FOUND 2 residual: one run folder whose real path is inside a git work tree is still
   accepted, and the image is written there).** `LabFiles.cs:87`-`:121` `RealPath` takes
   `ResolveLinkTarget(returnFinalTarget: true)` and then `Path.GetFullPath(target.FullName)`; for a RELATIVE link target
   holding `..`, the returned path is normalised lexically (the `..` is collapsed against the link's text before the
   system resolves the link it passes through), so it is not the system's real path. MEASURED (probe C9):
   `<root>/a9/s -> <root>/d1/d2/d3`, `<root>/a9/esc -> s/../../repo9/sub` (relative), `<root>/d1/repo9/.git`;
   `--run <root>/a9/esc/run9`: `RealPath` gives `<root>/repo9/sub/run9` (does not exist), exit 0, the run folder and
   `panel.png` made INSIDE `<root>/d1/repo9/sub` (the system resolves `s` first, then `..` twice). The Lab README's
   capture bullet (`Commands/Oxpd1/README.md:20`-`:21`, "so the image is not written inside one") and the run-folder
   section (`:146`-`:148`, "every symbolic link among its existing folders resolved, so a link that leads into a work
   tree is refused too") are false for this shape. The shape needs a hand-made relative link that walks `..` through
   another link; the file is untracked (a `git add` is still needed to commit it). Fix when next touched: resolve one
   component at a time from a resolved prefix (each `..` against the resolved folder), or take the real path of the
   deepest existing ancestor (`realpath(3)` semantics); or name the shape in Limits.
3. **Info (answers HP's schema accepts that are now refused: the safe side).** MEASURED (probe A): `xsi:type="xs:boolean"`
   and `xsi:schemaLocation="..."` on `enabled` (HP schema errors 0; XSD lets `xsi:type` name the declared type and
   `xsi:schemaLocation` sit on any element), and `xml:lang` on `enabled` (errors 0 by .NET's validator): each exit 8,
   0 enables, nothing written. The README says "no attribute but a namespace declaration", which is what the code does;
   only "read only in HP's shape" is narrower than HP's schema. A processing instruction inside `enabled`, a comment or
   white space beside it, a character reference (`&#102;alse`) and a default-namespace redeclaration are schema-valid
   and read as `false` (consistent with HP's schema). `xsi:nil="false"` is refused by both (errors 1, exit 8).
4. **Info (the password check: the named limits MEASURED, and one unnamed fail-closed effect).** MEASURED (probe B): the
   password's UTF-8 bytes 400,001 bytes into a 500,000-byte capture: exit 8, nothing saved. The password's Basic form
   (`admin:<password>` base64) and its UTF-16LE bytes inside a capture: saved whole holding them (exit 0): the named
   limit (README Limits). The client's log of a refused capture: in 3 of the probe's logs the base64 text decodes to
   bytes holding the password (none holds its plain text): the named limit. NOT named: a short password matches by
   chance; a synthetic password `PNG` (bytes of the PNG signature itself) refused EVERY capture (B2: exit 8, "holds the
   password's bytes"). Fail-closed, nothing saved; an operator would see the refusal line.
5. **Info (`RealPath` cannot loop, throw out of the verb, or pass its bound silently on this Mac).** Recursion is bounded
   by `links < MaxLinks` (each recursion adds one; past 40 the walk goes on as written, no recursion). MEASURED (probe
   C10 to C13): a link loop above the run folder exit 5 (`IOException` at the making, caught); a dangling link exit 5; a
   folder with mode 000 above the run folder: `GitWorkTreeHolding` null, no exception (the `LinkTarget` read outside the
   `try` did not throw), verb exit 5; a path of 41 links (the 41st into the tree) and one of 40: exit 5, nothing made (the
   system's own link limit stops the making before the bound matters). Linux and Windows UNMEASURED (S14 returns at once
   on Windows by Q4; Linux's own limit of 40 links per lookup is UNMEASURED here). A path of more than 40 links read as
   written is stated in the doc comment (`LabFiles.cs:73`), not in the README.
6. **Info (the other link shapes the commission names are refused).** MEASURED, each exit 9, nothing made: the leaf's
   parent a link into the tree (C1, round 1's escape), a link to a link (C3), two links in the path (C4), a relative
   link (C5), a relative link with `..` NOT passing through another link (C6), a linked `.git` FILE (C7), a `.git` that
   is a dangling link (C7b), a link above the work tree's root (C8: found on the path as written). The run folder itself
   a link to an existing folder: exit 9 now (C2; round 1 exit 5). `link/../x14/run14`: made at `<root>/x14/run14`,
   outside the tree (the path is normalised as written, as the making does).
7. **Info (the seat's DEVIATIONS 2 is right).** My post-mutant build shows the same times: the adapter assembly
   (21:02:17) later than `Oxpd1Read.cs` and `Oxpd1Soap.cs` and earlier than `LabFiles.cs` (21:06:21), which is in
   `Datasec.Suite.Lab` and is not compiled into `Datasec.Suite.Adapters.Oxpd1.dll`; the Lab assembly (21:07:32) later
   than all three; the whole solution green again 2171 / 0 / 2167 / 4. No stale binary.
8. **Info (unchanged from round 1, by the coordinator's Q1 and Q6).** `GetScreenCapture`'s row is not `TextOnly`: a
   result whose base64 is split by a child element is still decoded and saved (probe B, bytes equal). Round 1's three
   surviving gate mutants of FOUND 4 have no cell (Q6). `2-fix.diff` applies alone to BASE (its six files are disjoint
   from `1-red.diff`'s three): not a defect; red first stands on its own logs.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item
- **`89a10a1b..105b3465` read whole:** the nine diffs read whole; `Oxpd1Soap.cs` `Parse` and `ReadAnswer`,
  `LabFiles.cs` `RunFolderRule` and `ScreenCapture`, `Oxpd1Command.cs` 253-372, 640-700, 855-917 and
  `RunRecorder.Create` read at the head; no catch above the verbs (`Program.cs`, `CommandRegistry.cs`: none).
- **The tree = BASE + both patches byte for byte:** `72c05b08` both ways; patches' sha256 equal THE TOOLS.
- **Red first:** 12 of 12 by `Assert.Equal()` (adapter T07 four refusal rows; Lab S13 four, S14 read/write/lab-cert
  `True`, S15 `True`); restore rc 0 (exactly the patch's 3 paths ` M`), build `0 Warning(s)`, `0 Error(s)`. Logs
  `g2058/logs/r-*.log`, `red-*.log`.
- **10 mutants, each red on exactly its cells:** `mTextOnlyOff` S13 T07 (8) | `mSiblingTaken` S13 T07 (2) |
  `mChildTaken` S13 T07 (4) | `mAttributeTaken` S13 T07 (2) | `mNamespaceDeclarationRefused` T07 (1) | `mCDataRefused`
  T07 (1) | `mLinksNotResolved` S14 (3) | `mLastLinkOnly` S14 (3) | `mCapturePasswordSaved` S15 (1) |
  `mCaptureNearPasswordRefused` S15 (1): every row MATCH, undone equal True.
- **Any `IsServiceEnabled` answer HP's schema refuses still read as `false`:** yes, five shapes (FOUND 1). Round 1's
  four, the processing instruction (schema-valid), `xsi:type` (refused), `xsi:nil="false"` (refused), an attribute in
  another namespace (refused): FOUND 3 and the probe table. **Any answer HP's schema accepts now refused:** yes, the safe
  side (FOUND 3).
- **Any run folder whose real path is in a work tree still accepted:** yes, one shape (FOUND 2); the commission's six
  named shapes are refused (FOUND 6).
- **`RealPath` loop, throw, 40-link bound:** none on this Mac (FOUND 5).
- **The password's bytes reaching `panel.png`:** UTF-8 never (S15, probe B two rows); Basic form and UTF-16 do (the named
  limit, MEASURED); the client's log holds a decodable copy (the named limit, MEASURED).
- **The README sentences against the code:** the kit's table checked row by row against `Oxpd1Read.cs:96`,
  `Oxpd1Soap.cs:174`, `LabFiles.cs:74`, `:78`, `:87`, `:177`, `Oxpd1Command.cs:357`, `:881` (each re-printed at the head):
  every sentence holds but two over-claims, adapter `README.md:43` and Lab `:95`-`:96` ("alone in the response", FOUND
  1) and Lab `:20`-`:21` and `:146`-`:148` (FOUND 2). The Limits sentences hold (UTF-8 only; the record's base64; checked
  once; a link that cannot be resolved read as written: MEASURED for a loop, a dangling link and no permission).
- **The four new cells and nothing else of a landed cell:** `checks_r2.py` check 9: removed lines under `tests/` 1, the
  stub's planned answer line, now the fallback of `EnabledResponse` (`Oxpd1Stub.cs:193`-`:194`); new public lines 4 (T07,
  S13, S14, S15). Cells read: T07 validates each body against HP's schema in the same cell; S14's message check reads
  the real path's suffix; S15's control row saves equal bytes.
- **The hosted run on both legs:** PASS (below); S14 on `windows` returns at once (DERIVED from the cell's first line;
  windows `succeeded: 2150` = 2171 - 21). **words.py and gitleaks:** clean (SCANS).

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)
- "read only in HP's shape ... any other shape ends `MalformedAnswer`": text beside `enabled` (FOUND 1), an attribute on
  the response element (FOUND 1), `xsi:type="xs:boolean"` (refused although schema-valid: FOUND 3), a processing
  instruction inside (schema-valid, read: covered by probe). Two findings.
- "the path ... again with every symbolic link among its existing folders resolved, so a link that leads into a work
  tree is refused too": a relative link through another link and `..` (FOUND 2), a link above the work tree's root (C8,
  refused), a 41-link path (C13, exit 5 on this Mac: stated in the doc comment only). One finding.
- "so the image is not written inside one": FOUND 2's shape; a `.git` that is a dangling link (refused, the safe side);
  a link changed between the check and the making (the named limit H15, not measured). One finding.
- "a capture whose bytes hold the password's UTF-8 bytes is not saved": deep in a large image (refused), the Basic form
  and UTF-16 (the named limit, saved), a short password matching by chance (fail-closed, FOUND 4 Info). Covered or stated.
- "A link that cannot be resolved (no permission, a loop) is read as written": a loop (exit 5), a dangling link (exit 5),
  no search permission on a folder (no throw, exit 5). Covered.
- The kit's H1-H21: H1-H5, H10, H11, H16, H17 as the cells say (green, each red under its mutants); H6 MEASURED
  (`xsi:nil="false"`, `xsi:type`, other attributes: refused); H7 MEASURED (text beside: FOUND 1; a processing
  instruction: read, schema-valid); H8, H12, H13 MEASURED (probe A rows; C2 now exit 9; R07 green); H9 MEASURED (A9);
  H14 MEASURED (C10 to C12); H15 not measured (named limit); H18, H19 MEASURED (named limits hold); H20 the hosted
  windows leg green; H21: the response element's attributes (FOUND 1) and the relative link through a link (FOUND 2) are
  the shapes the kit's table did not hold.

## THE HEAD, MEASURED BY THE GATE (logs `g2058/logs/`)
- Locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release --no-build`: `total: 2171`,
  `failed: 0`, `succeeded: 2167`, `skipped: 4` (h-test, and again h-test2 after the mutants and a rebuild).
- `repo_rules.py` (plain form, `test ! -e <tree>/1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT RUN (no
  supplied-source folder here)`, `RULES: clean (659 files)`; `unittest discover -s build/tests`: `Ran 111 tests`, `OK`;
  `ls-files` 659.
- `checks_r2.py <rules worktree> 89a10a1b`: `CHECKS: 10 of 10 PASS` (rows 9, all M; shared files 84 paths rc 0; added
  246; public lines 4; WriteAsync 2, new Oxpd1Writer 2, lower-level sends 0; removed test lines 1, the stub line; callers
  3 and 1), every control fired.
- Hosted push run 45366993513 (`hosted3.py 105b3465... --total 2171 --rules 659 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`, 20:51): linux `succeeded: 2167`, windows
  `succeeded: 2150`, both `total: 2171` twice, `failed: 0`, GUARD 14 and 15; rules `RULES: clean (659 files)`, floor 111;
  secret-scan every proof line; `check runs beside the four: 0`; last line `HOSTED 105b3465...: PASS`. `failed Datasec.`
  lines 0 and 0 (case-insensitive); control: 4 `Datasec.Suite.Lab.Tests.dll` lines per leg.
- Code scanning at main 89a10a1b: csharp, python, actions `results_count 0`; open alerts 0 (20:51). The head has no
  Analyze run yet (the branch push ran the four jobs only): the pull request's run is the first (landing.txt step 3).

## THE PROBE (scratch only, never committed: `_quarantine/G2058Probe.cs.txt`; output `scratch/probe-report.txt`)
One test file added to the Lab tests in `w` (its own Kestrel TLS stub on 127.0.0.1 port 0, a raw SOAP body per
operation, HP's committed `test.xsd` for the schema column, synthetic password, images and links under the system
temporary folder); the Lab executable run whole: `Total: 281, Errors: 0, Failed: 0` (229 + 52 probe cases), build
`0 Warning(s)`. Rows beside round 1 (gate B2052's `probe-report.txt`):

| Row (round 1's shape) | Round 1 (a7f74ff3) | Round 2 (105b3465) |
|---|---|---|
| A false in a child element | exit 0, 1 EnableService | exit 8, 0 EnableService |
| A false split by an element | exit 0, 1 EnableService | exit 8, 0 |
| A false and an extra sibling | exit 0, 1 EnableService | exit 8, 0 |
| A false nil attribute | exit 0, 1 EnableService | exit 8, 0 |
| A two enabled / another namespace / unqualified / TRUE / False | exit 8, 0 | exit 8, 0 (unchanged) |
| A true / 1 / space true space | exit 0, 0 (already on) | exit 0, 0 (unchanged) |
| A 0 / newline false / CDATA false / comment inside false | exit 0, 1 (off) | exit 0, 1 (unchanged; schema-valid) |
| B password bytes inside the image | exit 0, saved, password in panel.png | exit 8, nothing saved |
| B the other eleven capture shapes | (round 1 table) | identical exits and saves (780,000 saved; 790,000 exit 8) |
| C1 parent a link into the tree | exit 0, panel.png inside the tree | exit 9, nothing made |
| C1-control by the real path | exit 9 | exit 9 |
| C2 the run folder itself a link | exit 5 | exit 9 |

New rows (round 2 only): A text before / after / CDATA text beside `enabled`, an attribute or `xsi:nil` on the response
element: exit 0, 1 EnableService (FOUND 1); A `xsi:type`, `xsi:schemaLocation`, `xml:lang`, `xsi:nil="false"`, other
attributes on `enabled`: exit 8, 0; A processing instruction, comment or white space beside, character reference,
default-namespace redeclaration: read as HP's schema reads them. B Basic form and UTF-16LE: saved; UTF-8 deep in 500,000
bytes: refused; password `PNG`: every capture refused. C3 to C8: exit 9; C9: exit 0 inside the tree (FOUND 2); C10 to
C13: exit 5; C14: outside the tree. Probes D and E (two enables; refused enable) were not re-run: no line they read
changed (`Oxpd1Command.cs` changed one line, the capture arm).

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by a program, scanned alone): rc 1, `leaks found: 1` (moved to
  `_quarantine/gl-control-head-*`); the nine head blobs, `added.txt`, `commit-message.txt` and both patches under neutral
  names (13 files): rc 0, `no leaks found`. This folder's seven texts (21:16, the control re-scanned first: rc 1,
  `leaks found: 1`): rc 0, `no leaks found`.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; over `added.txt` (246 lines) and `commit-message.txt`:
  `WORDS: clean (2 files)`. `B2[0-9]{3}` over `added.txt` and the message: 0 and 0 (control: the kit 27).
- Over the squash subject (with #48), `squash-body.txt` and `pr-title.txt`: `WORDS: clean (3 files)`.
  `build/squash_scan.py` (the head's, equal to main's) with `#48`: control rc 1 found 2; message rc 0 found 0;
  `SQUASH-SCAN: clean`.

## NOT RUN
- CodeQL locally (the C# extractor is x86_64; no Rosetta on this Mac, RELAYED from the kit's FACTS 5): the pull
  request's code scanning is the CodeQL read (landing.txt step 3).
- Linux and Windows behaviour of the probe shapes: macOS arm64 only (the cells themselves ran green on both hosted legs;
  S14 returns at once on Windows).
- Probes D and E of round 1 (not re-run: unchanged code). No merge with any other main was built (MAIN MOVES (B)).
- No device, no M577, no lab tool outside the test process.

## LANDING
`landing.txt` (head-pinned squash, `--min-checks 8` from PR 47's check names, the merge-ref proof, code scanning, squash
scan, MAIN MOVES), `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md`. This is
round 2 of 2: FOUND 1 and 2 above are Minor residuals for the records (named limits) or a later lane at the
coordinator's choice; none blocks this landing, and lane L1 needs no round 3 to land. Landing closes owed item 124.
