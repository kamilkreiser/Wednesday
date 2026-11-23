GATE B2016: GO WITH FINDINGS @ 67c24d1 on main e39396f

Gate G1 (the lab tool's first device-WRITE verb, and it carries the admin password), round 1 of 2 of lane W2, one Opus
reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane W2, kit B2011 (seat X59; S4: Q1 "a" print-only and Q2 "a"
the read's guard structure and words, in words; Q3 to Q12 the defaults; each the coordinator's, none the product
owner's). Head `67c24d1860f2a5ec9b92d65dfa1cbe8ce203ca58` on `b2011/w2-oxpd1-lab-write`, ONE commit, one parent
`e39396f9` = main (BASE, stamp S2). Read and measured 2026-11-24 00:10 to 00:33 AEDT in my scratch
`fleet/state/s319/g2016/`: `clone` (clone.py draft at about 00:12: push URL `invalid://no-push`, no identity; detached at
the head), worktrees `red` (BASE + `1-red.diff`), `pat` (BASE + both patches, staged), `prb` (the head + ONE test-only
probe file, `scratch/G2016ProbeTests.cs`, never committed) and `ctm` (lane CT's pushed head `d3d10b71` + both patches,
staged: the CT-first merge). Every dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`)
and the wave lock, one at a time (42 released lock folders, all mine; the lock absent at the end; in `g2016/_quarantine/locks/`; no other holder's lock
touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no
pull request, no re-run; the lab tool was driven only in-process by the test assembly against the tests' own 127.0.0.1
stubs; no printer, no tenant; nothing deleted.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`pat` `write-tree` `22a59491` = `67c24d18^{tree}`;
`2-fix.diff` alone on BASE refused, rc 1; the six files' sha256 6 of 6 equal to THE CODE after `1-red.diff` and after
both; the commit message = `commit-message.txt`, 445 bytes); the ten tools of my copy equal THE TOOLS' sha256 (10 of 10).
Six paths (1 A, 5 M), numstat equal to the kit's table, `checks_w2.py` 8 of 8 with every control. Red first: Lab
`Total: 168, Errors: 0, Failed: 22`, exactly the kit's 22 cases, each followed by an `Assert.` line (20 `Equal`, 1
`False` (V10), 1 `Contains` (V11)), none outside `Oxpd1WriteTests`. Green 2093 / 0 / 2089 / 4. `MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal` (my run of the frozen tool; after it the clone clean, both mutated files equal to the head, rebuild 0/0, 2093 / 0 / 2089 / 4 again). RULES 648,
`Ran 111 tests` OK. Hosted push run of the head PASS on both legs (linux 2089, windows 2072). **The G1 questions,
MEASURED with a probe of 50 cases (Lab executable `Total: 218, Errors: 0, Failed: 0` = 168 + 50):** no dry run opened a
connection (TLS 0 on every dry row) and no dry path calls the credentials reader; no read that did not answer (401, 403,
a fault, a 404, a time-out, a dropped connection, malformed XML) or that held the id (upper case, braces, no hyphens,
padded) or an unreadable id (text, empty, attribute only) was followed by a write: 15 of 15 shapes ONE request, no
write, no list; a refused password was never followed by another request (read refused: 1 request; write refused: 2,
nothing after); the undo list cannot miss an executed write (the `Pending` row precedes the only executed send; any
throw after it leaves the row owed, MEASURED); the password reached no output and no run file even when the device echoed
it in a record name and a fault code. **Where it does NOT hold (FOUND 1 to 3):** `undo-owed` prints `nothing is owed`,
exit 0, when it read no list at all (the run folder itself given, a folder above the session, an empty or header-only
list); a same-id record in a non-schema shape is not seen and the register is sent; a name with U+FFFE, U+FFFF or a lone
surrogate passes the lab and throws in the envelope writer. One Major, three Minor, five Info; none sends a byte the kit
did not intend to a device the gate could see, none prints a value; the Major is print-only and is round 2's first item.

## FOUND

1. **Major (`undo-owed` says "nothing is owed" after reading nothing).** Oxpd1 `README.md:86` to `:92` "It reads the
   `undo-list.tsv` of each run folder there ... and names every register still owed its undo ... Exit 0 when nothing is
   owed and every line was read". MEASURED (probe P3), each exit 0 with `nothing is owed`: (a) the RUN folder given in
   place of the session (`undo list: 0 executed writes in 0 run folders under <session>/r1`), its own `undo-list.tsv`
   holding a register `Answered`/`Yes`; (b) the session nested one level below the folder given (`0 run folders`);
   (c) an empty `undo-list.tsv` and (d) one holding only its header line (`0 executed writes in 1 run folders`). Code:
   `LabFiles.cs:129` reads only folders directly inside the given one and never the given folder's own list; a list with
   no entry line adds no write and no unreadable place, and `:243` to `:245` print `nothing is owed` whenever both lists
   are empty. (a) and (b) are the README Limits' "a run whose folder sits elsewhere is not counted", but the verdict line
   the operator acts on is `nothing is owed`, exit 0, the same words as a clean session: this is the F19 "confirm all
   undone" check and its one failure mode is the silent pass. (c) and (d) cannot come from `UndoList.Enter` (header and
   line written together, then a move), only from damage. Nothing is sent and the device is untouched. Round 2: never
   print `nothing is owed` (exit 11, or 2) when no list was read or a list holds no entry line; read or refuse a given
   folder that itself holds `undo-list.tsv`; a cell per shape.
2. **Minor (the read before a register fails OPEN on a non-schema answer).** `Oxpd1Command.cs:748` counts only
   `AuthenticationAgentRecord` elements that are direct children of the result in the result's own namespace. MEASURED
   (P1): a record holding the SAME id in another namespace, wrapped one level deeper (`AuthenticationAgentRecords`), or
   unqualified: exit 0, the read and the write both sent, the list `Answered`/`Yes`, the output `sign-in agent records on
   the device: 0, none with this id`. HP's committed schema (`contracts/oxpd1/hp/.../authentication.xsd`:
   `elementFormDefault="qualified"`, `GetAuthenticationAgentRecordsResult` of type `AuthenticationAgentRecords`, a
   sequence of `AuthenticationAgentRecord`) is exactly the shape the code reads, so a conforming device is handled; how
   the M577 answers is UNMEASURED. The README's "When a record with the same id is already there ... or a record's id
   cannot be read, the run writes nothing" (`README.md:62` to `:65`) holds only for schema-shaped records. Round 2: fail
   closed (exit 10 or 8) when the result holds any child element that is not a schema record.
3. **Minor (the name check is narrower than XML's character rule).** `Oxpd1Command.cs:473` refuses `char.IsControl`
   only. MEASURED (P4): U+0001, U+007F and U+0085 exit 2 before any folder or connection; U+FFFE, U+FFFF and a lone
   surrogate U+D800 pass the parser and the writer's `XmlWriter` throws `ArgumentException`: a dry run after the run
   folder is made (no summary, no list); an executed register AFTER its read (ONE password-bearing request sent), with a
   `Pending`/`Unknown` row entered for a write that was never sent (so `undo-owed` owes an undo of nothing) and no
   summary. README `:79` "a run that stops before the write, enter[s] nothing" does not hold for this shape. A lone
   surrogate cannot arrive through UTF-8 argv (UNMEASURED); U+FFFE and U+FFFF can (valid UTF-8). Gate B2008 FOUND 3's
   class, at the lab. Round 2: refuse every character `XmlConvert.IsXmlChar` (with surrogate pairs) rejects, in the
   parser.
4. **Minor (the printed undo is not the register's connection).** `Oxpd1Command.cs:654` to `:657` (`UndoLine`) prints the
   host, the pins and `--soap-port` only. MEASURED (P6): a register given `--addressing 2004 --password-name
   SYNTHETIC_OTHER_NAME --timeout-seconds 7` prints an undo with none of the three. Run as printed, the undo reads the
   DEFAULT password name (exit 7 if absent; if that name holds another password, a 401 that counts toward the device's
   five-attempt lockout) and speaks 2005 addressing to a device the register reached with 2004. README `:72` to `:75`
   calls it "the ... command" of the undo. Round 2: carry every connection option into `UndoLine`.
5. **Info (a path with no cell).** No cell registers on a device that already holds ANOTHER agent (`records: n, none with
   this id`, n > 0). MEASURED (P1 `another agent only`): exit 0, read then write, correct. A mutant that refuses on any
   record would survive the 39 cases.
6. **Info (ties and the recorded clock).** `LabFiles.cs:169` orders by the recorded time, then by folder name. MEASURED
   (P3): register in `a`, unregister in `b`, the same time: `nothing is owed`; the folder names swapped: owed. A clock set
   back between two runs reorders them the same way. The kit names it (H21); the README says only "orders the writes by
   their time". Round 2: one Limits line.
7. **Info (no undo printed when the run dies after the send).** README `:72` "The undo is printed after every executed
   write that may have taken effect": DERIVED, not for a cancellation in flight (H22) or a throw after the send (the
   client's record, the list's second write: H20); the list keeps its `Pending` row and `undo-owed` owes it (MEASURED for
   a throw: P4's executed rows). The safe side; one README clause.
8. **Info ("nothing is retried").** The lab makes at most two password-bearing requests per register, one per
   unregister, MEASURED on every probe row (`carrying` 1 or 2); the client sends HTTP Basic preemptively (no handler
   credentials, so no 401 challenge round, `Oxpd1Client.cs` `SendAsync`). Whether .NET's `SocketsHttpHandler` re-sends a
   request that failed on a reused pooled connection (the write reuses the read's connection) is UNMEASURED by this gate:
   the landed client's behaviour, not this lane's code.
9. **Info (the host is compared as typed).** MEASURED (P3): a register on `LAB-HOST.example` and an answered unregister on
   `lab-host.example`: still owed; an IP and its name likewise (DERIVED, ordinal key `LabFiles.cs:173`). The safe side.

## WHAT THE GATE LIST ASKED (kit FOR TUESDAY "THE GATE", commission items 1 and 2)

| Question | Answer | How |
|---|---|---|
| `<BASE>..<head>` whole | read whole: the six files' diff, the adapter's `Oxpd1Writer.cs`, `Oxpd1Soap.cs`, `Oxpd1Client.cs` 1-140, HP's `authentication.xsd` | Read |
| the two patches against THE TOOLS' sha256 | equal (10 of 10 tools); BASE + both = the head's tree `22a59491` | `shasum`, `pat.py` |
| red first, the 22 cases by assertion | `Total: 168, Errors: 0, Failed: 22`; 22 `[FAIL]` lines, each followed by `Assert.`; exactly the kit's list; 0 outside the class | `run1.py red`, log `g2016/logs/r-lab.log` |
| each of the 14 mutants red on exactly its cells | 14 of 14 MATCH, each red on exactly its listed cells (mNoReadFirst on V02 V03 V04 V05 V06 V10, 12 cases), 14 of 14 undone equal; clone status 0 lines after | `mutants_w2.py run` (my run of the frozen tool) |
| ANY path of `write` opening the credentials file or a connection without `--execute` | none. `CredentialsFile.Read` callers: `:321` (read verb), `:680` (`ExecuteAsync`, reached only from `:631` when `options.Execute`); `DryRunAsync` (`:660`) builds the client over `_ => null` with no record file; the writer returns before `SendWriteAsync` when `Execute` is false (`Oxpd1Writer.cs` `WriteAsync`). MEASURED: V01 (absent file, TLS 0), P4 dry rows and P6 (TLS 0) | source, probe |
| ANY path writing after a read that did not answer, held the id, or held an unreadable id | none for HP's record shape: 15 of 15 shapes ONE request, 0 writes, no list (exit 6, 6, 8 x5, 10 x7 by shape); 3 non-schema shapes DO write (FOUND 2) | probe P1 |
| a refused password followed by another password-bearing request | never: read 401/403 = 1 request; write 401/403 = 2, the second refused, none after; each 401/403 arm returns (`:736`, `ExecuteAsync`'s switch) | V04, V06, P1, P5 |
| the undo list missing an executed write | cannot: `:701` `Enter(... null)` precedes `:702`, the only executed `WriteAsync`; a throw in `:701` stops before the send; any throw after it leaves `Pending`/`Unknown` (owed) | source; V11; P4 executed rows |
| `undo-owed` saying "nothing is owed" while a register that may have applied has no answered unregister after it | YES for four shapes (FOUND 1) and for a tie or a clock set back (FOUND 6); NO for an unregister of the same id on ANOTHER host (owed, exit 11), unknown, refused, pending | probe P3, U01-U03 |
| the password in the output, the summary, the undo list or the client's log | never: the device echoing it in a record name and a fault code, a refused read, a refused write: 0 hits in the output and in `summary.txt`, `undo-list.tsv`, `oxpd1-client.log` | probe P5; the V cells' `AssertNowhere` |
| the README sentences against the code | each row of the kit's table holds at the head but for FOUND 1 (`:86`-`:92`), FOUND 2 (`:62`-`:65`), FOUND 3 (`:79`), FOUND 4 and 7 (`:72`-`:75`) | Read, probe |
| the hosted run on both legs | `HOSTED 67c24d18...: PASS` (run 45180555693, attempt 1 each): linux total 2093 x2, succeeded 2089, skipped 4, GUARD 14; windows 2093 x2, 2072, 21, GUARD 15; rules RULES 648, 111 tests, floor 111; secret-scan every proof line; `failed Datasec.` 0 and 0; `Datasec.Suite.Lab.Tests.dll` 4 lines each leg | `hosted3.py` (gate copy), `legs.py` |
| `words.py` and gitleaks over the added lines and the message | SCANS below: clean | |
| read-before-register under 401, 403, fault, time-out, a dropped connection, the same id in another case, an unreadable id | as the kit says: ONE request each, no write | P1 |
| an `--execute` unregister of an id the device does not hold | the stub's empty answer: exit 0, ONE request, no read, row `Answered`/`Yes` (HP: "an id the device does not hold succeeds with no effect", `Oxpd1Writer.cs` doc); a fault: exit 8, row `Fault`/`Unknown` | P2 |
| `undo-owed`: register on one host, answered unregister of the same id on ANOTHER host after it | owed, exit 11 | P3 |
| two folders whose recorded times tie | ordered by folder name: one order clears, the other owes (FOUND 6) | P3 |
| an `undo-list.tsv` truncated mid-line | inside the id, inside `applied` (`Ye`), or the undo column missing: `unreadable: r1/undo-list.tsv line 2 (not shown)`, exit 11; cut inside the undo column (the 7th field, never parsed): still read, owed, exit 11 | P3 |
| gate B2008 FOUND 1 `https://@host/` and a control character in the name, at the lab before any connection | `@` in `--agent-service` or `--prompt-page` (empty user info, a user, `@` in the path) and U+0001, U+007F, U+0085 in the name: exit 2, no run folder, TLS 0, the address not echoed. U+FFFE, U+FFFF, U+D800: FOUND 3 | P4 |

## THE FRAME QUESTION (every / never / only / nothing; three shapes outside the tested one each)

| Sentence (head) | Shapes outside the tested one | Covered by |
|---|---|---|
| README `:57`-`:59` the dry run "reads no password (the credentials file is not opened) and connects to nothing" | a non-default `--password-name` and `--addressing 2004` (P6: TLS 0); a name the writer refuses (P4 dry: TLS 0, throws); an unregister (V01 row 2) | P4, P6, V01; source (no reader call) |
| README `:62`-`:65` "the run writes nothing" when a record holds the id or an unreadable id | braces, no hyphens, padded, attribute-only, empty (P1: exit 10); another namespace, wrapped, unqualified (P1: WRITES) | FOUND 2 |
| README `:66`-`:67` "When the read is refused ... faults, times out or ends in any other way, nothing is written" | 404, a dropped connection, malformed XML | P1: exit 8, 0 writes |
| README `:68`-`:71` "no request after it carries the password ... nothing is retried" | refused read; refused write; the password echoed by the device | V04, V06, P1, P5; .NET pool re-send UNMEASURED (FOUND 8) |
| README `:72`-`:75` "The undo is printed after every executed write that may have taken effect" | a fault (V05), a 401 on the write (V06, none printed, correct), a throw after the send | FOUND 7 (named here) |
| README `:76`-`:79` "Every executed write is entered ... BEFORE it is sent ... a run that stops before the write enter[s] nothing" | a throw inside the writer before the send (P4: `Pending` entered, never sent); a refused read (no list); a wrong pin (V10, no list) | FOUND 3 |
| README `:86`-`:92` "names every register still owed ... Exit 0 when nothing is owed and every line was read" | the run folder given, a nested session, an empty list, a header-only list, a tie | FOUND 1, FOUND 6 |
| README `:88`-`:90` "an unregister that ended unknown or was refused clears nothing" / "of the same id on the same host" | another host (owed), another case of the host (owed), an unregister answered for an id not held (clears: HP's "no effect" answer) | U03, P3, P2 |
| README `:90` "A line it cannot read is named by its file and line number, never shown" | truncated in the id, in `applied`, missing a column (named, line 2); an unreadable FILE (named with the exception's type, no line: `LabFiles.cs:146`); an empty list (not named: FOUND 1) | P3 |
| README `:91`, `:124` and doc comments "It sends nothing" / "never sends an undo" | `undo-owed` holds no client: `LabFiles.cs` names no `Oxpd1Client`, `Oxpd1Writer`, `HttpClient` or socket (grep, 0 lines; control `UndoList` found); U01's request count unchanged across `undo-owed` | source, U01 |
| Lab README `:27`-`:30` "without it, a dry run that connects to nothing" | as row 1 | as row 1 |
| `Oxpd1WriteOptions.Options` doc "the only words a usage error repeats" | a name with U+0001 (no echo), an `@` address (no echo, P4 `@-echo False` 4 of 4), an id not a UUID (V08) | P4, V08 |

The kit's H1-H25 table, attacked: H8 (V08) holds for 9 more shapes (P4) but not U+FFFE/U+FFFF/U+D800 (FOUND 3); H13/H14
hold, H21's tie is MEASURED (FOUND 6) and the given-folder shapes are not in the table (FOUND 1); H4 holds for 7 more id
shapes but not for non-schema records (FOUND 2); H16 holds (one `WriteAsync` call per path, `checks_w2.py` 7); H19 and H22
DERIVED as the kit says (FOUND 7). No other shape met.

## MERGE AND MAIN MOVES

- Main at the gate: `e39396f9` (gh at about 00:12 and at the last read, 00:32). compare main...67c24d18: ahead 1,
  behind 0, six files with the kit's numstat; open pull requests 0; code scanning at e39396f9 csharp, python, actions
  results 0, open alerts 0. The squash's tree on this main is the head's tree `22a59491`: measured above (2093 / 0 /
  2089 / 4, RULES 648).
- **CT first (MAIN MOVES (B) of landing.txt), measured on CT's PUSHED head `d3d10b71`:** `git merge-tree --write-tree d3d10b71 67c24d18` rc 0, no conflict, tree `b2a09571` = CT head + both frozen patches (write-tree in `ctm`); CT touches 14 paths, all `contracts/oxpd1/**`, the adapter README and two adapter test files (no Lab path, no lock, project, `Directory.*`, `.github` or `build` path); CT head tree `ab8093c6`, one parent e39396f9. Measured in `ctm`: locked restore rc 0; build 0 Warning(s) 0 Error(s); `total: 2093, failed: 0, succeeded: 2089, skipped: 4` (CT +0 tests); `RULES: clean (657 files)` (= 648 + 9), ls-files 657. NOT measured: CT's hosted legs and CT's own gate; if CT lands any head other than d3d10b71, landing.txt MAIN MOVES (C).

## SCANS

- `words.py --control`: `CONTROL FIRED: 13 of 13`. `words.py` over the 1192 added lines (`checks_w2.py`'s `added.txt`) and
  the head's own message (445 bytes, cat-file): `WORDS: clean (2 files)`; over `squash-subject.txt` (with #43),
  `squash-body.txt` and `pr-title.txt`: `WORDS: clean (3 files)`. `B2[0-9]{3}` lines: 0 and 0 (control: the kit 33).
- gitleaks 8.30.1: control FIRST (a token built by a program from two halves and 36 random characters, never printed,
  scanned alone): rc 1, `leaks found: 1`, the token not in the output; moved to `g2016/_quarantine/gl-control-*`. Then
  the added lines, the head's message, both patches and the six head blobs under neutral names `1.txt` to `10.txt` in a
  NEW folder: rc 0, `no leaks found`.
- `build/squash_scan.py squash-subject(#43) squash-body.txt --scanner gitleaks` from the clone (build/ equal to main's):
  control rc 1 found 2; message rc 0 found 0; `SQUASH-SCAN: clean`.

## DISCLOSURE

- One hook refusal: `pretooluse_zsh_wordsplit.sh` refused a `cat` of the two message files with an unquoted `===`
  separator. I did not re-issue it; the comparison was made by `cmp` (it differed only by the trailing newline `git log
  %B` adds) and then by a program reading the raw commit object (`msg.py`: equal, 445 bytes).
- The probe built with `-p:TreatWarningsAsErrors=false` (it built 0 Warning(s) 0 Error(s) anyway) in worktree `prb` only;
  the probe file is in my scratch and was never in `clone`, `pat`, `red` or `ctm`. Worktree indexes of `pat` and `ctm`
  were staged (`add -A`) to read their trees; no commit, no ref, nothing pushed (push URL `invalid://no-push`).
- Not run: CodeQL locally; any Windows or Linux leg locally (the head's push run is the only cross-platform proof); the
  seat's `run_step.py` neutral scan (the hosted secret-scan job's proof lines read instead); any device.
