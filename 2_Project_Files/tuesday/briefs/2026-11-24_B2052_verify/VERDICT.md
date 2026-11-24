GATE B2052: GO WITH FINDINGS @ a7f74ff on main c6f5d36

Gate G1 (device-WRITE code: `EnableService` and `DisableService` with the admin credential, and a reviewed widening of the
read-only check), round 1 of 2 of lane L1, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L1,
kit B2048 (seat X63; Q1 and Q2 "a" in words at stamp S4, Q3 to Q11 the defaults; each the coordinator's, not the product
owner's). Head `a7f74ff39ca455626200fbc9e3c1b47624ba83ef` on `b2048/l1-oxpd1-test-service`, ONE commit, one parent
`c6f5d36a` (main = PR 46's squash; the seat rebased its unpushed commit from BASE e2a20aef). Main did NOT move during the
gate (c6f5d36a by gh api -X GET at 17:31 and 18:02 and by a fresh clone at 17:30); open pull requests 0 at both reads; the
branch still at a7f74ff3 at 18:02. Read and measured 2026-11-24 17:28 to 18:05 AEDT in my scratch
`fleet/state/s323/g2052/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity), worktrees `head`
(a7f74ff3, detached), `red` (c6f5d36a + `1-red.diff`), `rules` (a7f74ff3, untouched) and `pat` (a7f74ff3 + a gate probe
file, now `_quarantine/G2052Probe.cs.txt`). Every dotnet job and test executable through the kit's `heavy.py` (sha256
`31adedc8...`) and the wave lock, one at a time (58 released lock folders, all mine, in `g2052/_quarantine/locks/`; lock
waits 0 to 5; no other holder's lock touched; the lock absent at the end). Origin by `gh api -X GET` under the project
GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull request, no re-run; no printer, no device, no
tenant, no Azure; the M577 not touched; nothing deleted (moved to `_quarantine`).

**BLUF.** The head is c6f5d36a plus the two frozen patches byte for byte (temporary-index `write-tree`: red tree
`79e0c7d5`, both-patches tree `4933b988` = `a7f74ff3^{tree}`; the same patches on e2a20aef give `2580fab0`, so the rebase
moved only lane L2's seven paths; `2-fix.diff` alone refused on both, rc 1). The ten tools equal THE TOOLS' sha256 in my
copy, the seat's `.tools/b2048/gate` and the drafter's source (10 of 10 each); the commit message equals
`commit-message.txt` (487 bytes). Fifteen paths (2 A, 13 M), numstat equal to the kit; `checks_l1.py` 10 of 10 with every
control. Red first: adapter `Total: 47, Failed: 4`, Lab `Total: 219, Failed: 18`, 22 of 22 `[FAIL]` lines each followed
by an `Assert.` failure line, exactly THE CONTROLS' cases. Green 2153 / 0 / 2149 / 4 (twice: before the mutants and after
the gate's own mutants). `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal` (my run of the frozen tool). Hosted push run
45339675420 `HOSTED a7f74ff3...: PASS` (my hosted3.py read). **The G1 questions:** no name without `Get` but
`IsServiceEnabled` passes `IsReadName` or `ReadOnlyViolations` (ordinal by construction; T01, T02 and their mutants); no
`oxpd1 write` path reads the credentials file or connects without `--execute`; a refused password is never followed by
another password-bearing request; the undo is printed and owed only for an enable that was sent and may have applied.
Three Minor findings (an over-lenient read of `enabled`, and two README sentences that a measured shape makes false) and
nine Info; none blocks the landing, none sends a byte the README does not already allow for.

## FOUND

1. **Minor (the read before an enable takes the JOINED text of `enabled`, so some answers outside HP's schema are taken
   as off and ONE `EnableService` is sent).** `Oxpd1Command.cs:888` `enabled = XmlConvert.ToBoolean(read.Answer!.Value)`;
   `XElement.Value` joins every descendant text, and `Oxpd1Soap.ReadAnswer` (`Oxpd1Soap.cs:165`-`:166`) counts only the
   `enabled` elements, not their content or siblings. MEASURED (probe A, macOS arm64, the lab tool in process against the
   gate's TLS stub on 127.0.0.1): `<enabled><x>false</x></enabled>`, `<enabled>fa<x/>lse</enabled>`,
   `<enabled>false</enabled><extra>...</extra>` and `<enabled xsi:nil="true">false</enabled>` each: exit 0, 1
   `IsServiceEnabled` + 1 `EnableService`, the list row and the printed undo. HP's schema (`test.xsd:928`-`:934`): ONE
   element `enabled` of type `xs:boolean` (simple content). The Lab README (`Commands/Oxpd1/README.md:91`-`:92`) says an
   `enabled` value "that is not an `xs:boolean`" writes nothing. Harm is bounded: the undo is entered BEFORE the send,
   printed and owed, so the worst case is the README's own non-atomic case (a disable owed for a service that may already
   have been on). Fail-closed shapes MEASURED for contrast: two `enabled`, another namespace, no namespace, `TRUE`, `False`
   (exit 8, 0 enables); `true`, ` true `, `1` (exit 0 already on, 0 enables); `0`, `\nfalse\n`, CDATA, a comment inside
   (taken as off: xs:boolean lexical forms with white space collapsed, as the schema reads them). Fix (round 2): refuse
   an `enabled` with a child element (`HasElements`) or a response with any other element, beside the boolean parse.
2. **Minor (README: "the image is never in a commit" is false for a run folder reached through a symbolic link).**
   `Commands/Oxpd1/README.md:19`-`:20` and `LabFiles.cs:96` ("The run folder is refused inside a git work tree, so it is
   never committed"). `RunFolderRule.GitWorkTreeHolding` (`LabFiles.cs:76`-`:85`, landed) walks `Path.GetFullPath` and
   `DirectoryInfo.Parent`, which do not resolve links. MEASURED (probe C): `<root>/link -> <root>/repo/sub` with
   `<root>/repo/.git`, `--run <root>/link/run1`: exit 0, `panel.png`, `summary.txt`, `oxpd1-client.log` written inside the
   work tree; control: the same folder by its real path exit 9, nothing made; a run folder that IS a link to an existing
   folder: exit 5. The file is untracked, so "never in a commit" still needs a `git add`; the sentence's "so" is what is
   over-claimed. The rule is landed (not this lane's code), but this lane is the first to save a device's image there.
   Fix: name it in Limits, or resolve links (`ResolveLinkTarget`, or `realpath` of the parent) in the rule.
3. **Minor (README: "The password is ... not in the run folder" no longer covers `panel.png`).** Landed sentence
   `Commands/Oxpd1/README.md:37`-`:38`; the client scrubs the base64 TEXT (`Oxpd1Client.cs:201`), but `ScreenCapture.Save`
   writes the DECODED bytes unscrubbed (`LabFiles.cs:110`, `:126`). MEASURED (probe B): a synthetic PNG carrying the
   synthetic password's bytes after the signature: exit 0, `panel.png` saved whole holding them; the output, `summary.txt`
   and `oxpd1-client.log` held none. A real panel image carries pixels, so this needs a device that embeds the password in
   its PNG (UNMEASURED, unlikely); the kit's P8 "the password is in no output and no file of the run folder" and the
   cells' `AssertNowhere` hold only for the stubs' bytes. Fix: one Limits sentence ("`panel.png` is the device's bytes,
   not scrubbed"), or refuse a capture whose bytes hold the password or the Basic value.
4. **Info (three gate mutants survive: shapes no cell pins).** MEASURED (Lab executable whole, `Total: 219, Failed: 0`
   each, source restored and proved equal, rebuilt, whole solution green again 2153/0/2149/4):
   `gmSignatureOnlySaved` (`LabFiles.cs:118` `<=` to `<`: an 8-byte signature-only answer would be saved; the head
   refuses it, probe B); `gmBoolParse` (`XmlConvert.ToBoolean` to `bool.Parse`: `TRUE`/`False` would be taken, `1`/`0`
   refused; H11 untested by any cell); `gmPinRefusedReadGoesOn` (a pin-refused read before the enable goes on to the
   enable: DERIVED harmless, the enable is pin-refused by the same handler before any request, `Applied No`). Candidates
   for round 2 cells; none is a defect at the head.
5. **Info (the capture's real bound and the lenient base64).** MEASURED (probe B): 780,000 bytes saved whole; 790,000
   bytes ended `TooLarge` (exit 8, "the read did not answer", nothing saved): the image bound is about three quarters of
   `MaxAnswerBytes`, as the README's "1 MiB of answer" implies. Base64 with line breaks inside, and a result whose text is
   split by a child element, decode and are saved (bytes equal). Text after the base64, two results, an empty result and
   the signature alone: exit 8, no `panel.png*`. Trailing bytes after a PNG: saved whole (the kit's H23 limit). Neither
   the output nor any run file but the client's log held the base64 text.
6. **Info (two enables and the undo list).** MEASURED (probe D): enable (off to on, 1 `EnableService`), a second enable
   (on: nothing written, no list, exit 0), `undo-owed` exit 11 with ONE owed line; after the stub went off (a reboot) a
   third enable wrote; `undo-owed` still ONE owed line (the latest enable: the owed map is keyed by host and the all-zero
   id), and ONE answered disable cleared it (exit 0, "nothing is owed"). Right for an on/off switch.
7. **Info (refused password).** MEASURED (probe E): an enable answered 401 or 403 after a clean read: exit 6, exactly 2
   requests carried the password (the read, the enable), no third, no undo printed. S04 (read refused: 1 request) green.
8. **Info (the widening is a catalogue check, not a runtime gate).** `ReadOnlyViolations` has no caller in `src/`
   (`git grep` at the head: definitions only; callers C03 and T02); `ReadAsync` sends whatever row the closed enum names.
   This is the landed design (PR 40), unchanged; the closed enum and `ReadOperations` are the runtime limit.
   `IsReadName` is `StartsWith("Get", Ordinal) || Equals(NonGetRead, Ordinal)` (`Oxpd1Read.cs:113`-`:114`): case,
   spacing, look-alike letters and any other name are refused by construction; a planted allowed list cannot pass a
   non-`Get` name (T02). Any `Get…` name passes the form rule (landed); none of the seven bindings' `Get` operations is a
   write by its HP description (not re-read whole by the gate).
9. **Info (one stale README clause).** `Commands/Oxpd1/README.md:74`-`:75`: a dry run prints "for a register, the command
   of its undo"; the head's dry run also prints the enable's (`Oxpd1Command.cs:746`-`:748`; S01 asserts it). Incomplete,
   not false.
10. **Info (`IsServiceEnabled` is OXPd 1.7).** HP's committed `test.xsd:920`: "Added for OXPd Release 1.7" above
    `IsServiceEnabled`, `EnableService`, `DisableService`. Whether the M577's firmware (`2510156_069175`) answers them is
    UNMEASURED; the device kit's first read settles it (a fault there writes nothing: exit 8).
11. **Info (the seat's DEVIATIONS 2, closed by the gate).** The seat did not read `1-red.diff`'s test hunks line by line;
    the gate read both new test files whole and the four stub and count diffs whole at the head (below). The cells test
    what their names say; the lab stub answers a capture while off with a SOAP fault (status 500, `s:Fault`), as HP says.
12. **Info (WS-Addressing sentences).** Adapter `README.md` and Lab README: "MEASURED on one device ... M577 (firmware
    `2510156_069175`, 2026-11-24) ... 2005 answered with an empty HTTP 400 and 2004 with the read's answer" match the
    first-run seat's STATUS BLUF item 3 (`Briefs/2026-11-24_B2044_STATUS.md:26`, read by the gate); the default is
    unchanged (`Oxpd1ClientOptions.cs` not in the diff).

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item
- **`c6f5d36a..a7f74ff3` read whole.** All fifteen files' diffs read; `TestServiceTests.cs` (174 lines) and
  `Oxpd1TestServiceTests.cs` (354) read whole; `Oxpd1Client.cs`, `Oxpd1Soap.cs`, `Oxpd1ReadResult.cs`, `LabFiles.cs` and
  `Oxpd1Command.cs` 180-372 and 640-917 read whole at the head.
- **The tree = c6f5d36a + both patches byte for byte:** `4933b988` both ways (above).
- **Red first:** 22 of 22 by assertion (adapter T01 DoesNotContain; T03, T04, T05 `a fault` NotNull; Lab S02, S05 `500`
  Contains; S03, S04 x5, S07 `an enable with an agent id`, S09 `not a png`, S10 `1`, S11, S12 x6 Equal). Build
  `0 Warning(s)`, `0 Error(s)`. Logs `g2052/logs/r-*.log`.
- **16 mutants, each red on exactly its cells:**
  `mIsPrefixWidened` T01 | `mReadFormDropped` T02 | `mResultElementIgnored` K01 K12 S02 S03 S05 S10 S11 T03 T06 |
  `mEnableNoUndo` S02 S05 T03 T04 T05 | `mNoReadBeforeEnable` S02 S03 S04 S05 | `mOnIgnored` S03 | `mNoBooleanTaken` S04
  | `mRefusedReadEnables` S04 | `mReadEndEnables` S04 | `mServiceTakesAgentId` S07 | `mReadByNumber` S10 |
  `mCaptureNotSaved` S08 S09 | `mPngUnchecked` S09 | `mEnableNotOwed` S11 S12 | `mAnyDisableKind` U03 S12 |
  `mIdRuleDropped` S12: every row MATCH, undone equal True; `MUTANTS: 16 of 16 MATCH, 16 of 16 undone equal`.
- **Any non-`Get` name but `IsServiceEnabled` through `IsReadName` or `ReadOnlyViolations`:** none (FOUND 8; T01 covers 51
  binding names and seven near names; T02 every one planted in both the list and a row).
- **Any `oxpd1 write` path opening the credentials file or a connection without `--execute`:** none. `RunAsync`
  (`Oxpd1Command.cs:659`-`:694`): parse (no file IO: the parser's only credential call is `CredentialsFile.IsName`), the
  git rule, the folder, then `options.Execute ? ExecuteAsync : DryRunAsync` (`:684`); the dry run's client reads
  `_ => null` with no record file (`:736`) and the writer returns before `SendWriteAsync` when `Execute` is not set; the
  only `CredentialsFile.Read` of the verb is `:758`, inside `ExecuteAsync`. S01: 0 TLS connections, no list.
- **Any `EnableService` after a read that did not answer a boolean false:** only the FOUND 1 shapes (a joined-text
  `false`). Every non-`Answered` end returns before the write (`:871`-`:883`); a non-boolean text returns 8 (`:890`-
  `:894`); `true` returns 0 (`:896`-`:900`).
- **The undo printed or owed for an enable not sent, or missed for one that may have applied:** neither. Printed only
  when the writer's `Undo` is set (`:792`), which is null for `Applied No` (401, 403, a refused pin, no credential) and
  set for `Yes` and `Unknown` (fault, time-out, transport, other status, malformed, too large); the `Pending` row is
  entered before the send (`:788`) and stays owed if the run dies (H24, landed). `undo-owed` owes on `Applied != No`
  and clears only on an `Answered`/`Yes` disable of the same host after it (`LabFiles.cs:234`, `:238`); S05, S11, S12,
  probe D.
- **A refused password followed by another password-bearing request:** never (S04: 1; probe E: 2, the refused one last).
- **A capture printed, saved outside the run folder, saved when not a PNG, or saved in part:** not printed (S08; probe B:
  no base64 in the output or any file but the client's log, which holds every answer by design); saved only at
  `Path.Combine(runFolder, "panel.png")` (FOUND 2: a run folder behind a link); not a PNG or not base64 saves nothing
  (S09; probe B); written whole to `panel.png.new`, then moved (`LabFiles.cs:126`-`:127`): `panel.png` is never partial;
  an IO exception between them would leave a partial `.new` and no summary (DERIVED, no cell).
- **The password in the output, summary, undo list, `panel.png` or the client's log:** none in the output, summary, undo
  list or log in every cell and probe; `panel.png` FOUND 3.
- **The README sentences against the code:** the kit's table checked row by row; FOUND 1, 2, 3 and 9 are the
  differences; every other sentence holds (the four writes and their credentials, "the writer reads nothing first", "at
  most twice", the all-zero id rule, the Limits).
- **The four landed literals of D8 and nothing else of a landed cell:** `ContractTests.cs` 2 lines (C03 5 to 7; `Schemas()`
  gains `test.xsd`), `ClientTests.cs` 1 (K01 5 to 7), `WriteTests.cs` 1 (W01 2 to 4); no other landed test line. The two
  stubs: added branches for Test operations only; `Oxpd1Stub.cs` 5 changed lines are the constructor, `StartAsync`'s
  `app.Run` and return, `AnswerPlanned`'s signature and its doc comment; `StubDevice.TestServiceOn` defaults on (D7).
- **The hosted run on both legs:** PASS (below). **words.py and gitleaks:** clean (SCANS).

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)
- "No other name without `Get` passes": case and spacing (T01), look-alike letters (ordinal: DERIVED), a planted allowed
  list (T02). Covered. Limit: any `Get…` name passes the form rule (landed; FOUND 8).
- "An enable on a service already on writes nothing": `1` and ` true ` (probe A: exit 0, 0 enables), `TRUE` (exit 8,
  0 enables), a service turned on between the read and the enable (named limit H19). Covered or stated.
- "A read that is refused, faults, ends otherwise or answers a non-boolean writes nothing": a joined-text `false` (FOUND
  1), a pin refused on the read (no cell; `gmPinRefusedReadGoesOn` survives; DERIVED harmless), a time-out (H10, DERIVED;
  `mReadEndEnables` reds the 500 row on the same arm). One finding.
- "`panel.png` saved only when base64 and the PNG signature": base64 with line breaks (saved, equal bytes), text after
  the base64 (refused), the signature alone (refused; `gmSignatureOnlySaved` survives). Covered by probe, one cell gap.
- "The image is never in a commit": a link above the run folder (FOUND 2), a run folder that is a link (exit 5), a
  linked work tree's `.git` file (landed rule reads files too, DERIVED). One finding.
- "The password is never in the run folder": the client's log (scrubbed, cells), the summary (cells), `panel.png`'s
  decoded bytes (FOUND 3). One finding.
- "An enable is owed until a disable on the same host has answered after it": the same time (ordered by folder name:
  landed), the host spelled differently (stays owed: the safe side, DERIVED), two enables (probe D: one owed, one
  disable clears). Covered.
- "Every executed write is entered before it is sent": a run that dies after the send (the `Pending` row, landed H24),
  an already-on enable (no entry: S03), a read refused (no entry: S04). Covered.
- The kit's H1-H26: H1-H9, H12-H18 as the cells say (all green, the mutants above); H10, H11, H21 DERIVED or now MEASURED
  (probe A, B); H19, H20, H22-H25 named limits, H22 and H23 now MEASURED (probe B); H26: FOUND 1 to 3 are the shapes the
  kit's table did not hold.

## THE HEAD, MEASURED BY THE GATE (logs `g2052/logs/`)
- Locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test -c Release --no-build`: `total: 2153`,
  `failed: 0`, `succeeded: 2149`, `skipped: 4` (h-test, and again h-test2 after the gate mutants).
- `repo_rules.py` (plain form, `test ! -e <tree>/1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT RUN (no
  supplied-source folder here)`, `RULES: clean (659 files)`; `unittest discover -s build/tests`: `Ran 111 tests`, `OK`.
- `checks_l1.py <rules worktree> c6f5d36a`: `CHECKS: 10 of 10 PASS` (rows 15, A 2 M 13; shared files 78 paths rc 0; added
  982; public lines 24; WriteAsync 2, new Oxpd1Writer 2, lower-level sends 0; client `///` only; non-Get
  `['IsServiceEnabled']`), every control fired.
- Hosted push run 45339675420 (`hosted3.py a7f74ff3... --total 2153 --rules 659 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15`, 17:36): linux `succeeded: 2149`, windows
  `succeeded: 2132`, both `total: 2153` twice, `failed: 0`, GUARD 14 and 15; rules `RULES: clean (659 files)`, floor 111;
  secret-scan every proof line; `check runs beside the four: 0`; last line `HOSTED a7f74ff3...: PASS`. `failed Datasec.`
  lines 0 and 0 (case-insensitive); control: 4 `Datasec.Suite.Adapters.Oxpd1.Tests.dll` and 4 `Datasec.Suite.Lab.Tests.dll`
  lines per leg.
- Code scanning at main c6f5d36a: csharp, python, actions `results_count 0`; open alerts 0 (17:37). The head has no
  analysis yet (the PR's run is the first: landing.txt step 3).

## THE PROBE (scratch only, never committed: `_quarantine/G2052Probe.cs.txt`; output `scratch/probe-report.txt`)
One test file added to the Lab tests in the `pat` worktree (its own Kestrel TLS stub on 127.0.0.1 port 0, a raw SOAP body
per operation, synthetic password and images); the Lab executable run whole: `Total: 251, Errors: 0, Failed: 0` (219 + 32
probe cases), build `0 Warning(s)`. Rows A (16 `enabled` shapes), B (12 capture shapes), C (links into a work tree), D
(two and three enables), E (enable refused after a clean read): their results are in FOUND 1 to 7.

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by a program, scanned alone): rc 1, `leaks found: 1` (moved to
  `_quarantine/gl-control`); the fifteen head blobs, `added.txt`, `commit-message.txt` and both patches under neutral
  names (19 files): rc 0, `no leaks found`. This folder (the seven texts, 18:03, the control re-scanned first: `leaks found: 1`):
  `no leaks found`.
- `words.py --control`: `CONTROL FIRED: 13 of 13`; over `added.txt` (982 lines, byte-equal to the seat's `checks2/added.txt`)
  and `commit-message.txt`: `WORDS: clean (2 files)`; over the squash subject (with #47), the squash body and the PR
  title: `WORDS: clean (3 files)`. `B2[0-9]{3}` over `added.txt` and the message: 0 and 0 (control: the kit 23).
- `build/squash_scan.py` (the head's, equal to main's: `build/**` not in the diff) with `#47`: control rc 1 found 2;
  message rc 0 found 0; `SQUASH-SCAN: clean`.

## NOT RUN
- CodeQL locally (the C# extractor is x86_64; no Rosetta on this Mac, RELAYED from the drafter's FACTS 5): the pull
  request's code scanning is the CodeQL read (landing.txt step 3).
- Linux and Windows behaviour of the probe shapes: macOS arm64 only (the cells themselves ran green on both hosted legs).
- No merge with any other main was built (MAIN MOVES (B) in landing.txt).
- No device, no M577, no lab tool outside the test process.

## LANDING
`landing.txt` (head-pinned squash, `--min-checks 8` from PR 46's check names, the merge-ref proof, code scanning, squash
scan, MAIN MOVES), `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md`. Round 2 of
lane L1 should carry FOUND 1 (code), FOUND 2 and 3 (text, or code) and, at the coordinator's choice, cells for FOUND 4.
