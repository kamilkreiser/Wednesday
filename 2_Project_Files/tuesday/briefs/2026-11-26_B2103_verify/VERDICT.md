GATE B2103: GO WITH FINDINGS @ 1c7cdbb on main 1ccf6d0

Gate G1 (a lab write to a device path, a new admin read), ROUND 1 OF 2 of the row-4 write lane, one Opus reader
(claude-opus-5-5), in-session, read-only. OXPd 2, kit B2100 (seat X75; stamp S4: Q1 "a" cut from row 3's squash
1ccf6d0c, Q2 "a" the writer's own `ReadTopLevelButtonsAsync` through `SendAdminReadAsync` with the read catalogue
unchanged, Q7 "a" `undo-owed` keyed by host, family and id, each in words; Q3 to Q6 and Q8 to Q10 the defaults; S8 the
canonical heavy runner 31adedc8; every choice the coordinator's, none the product owner's). Head
`1c7cdbbb790f287c3ef9e9544fb3a1848f45bf49` on `b2100/row4-top-level-button`, ONE commit, one parent = main
`1ccf6d0c6a4d9af1da986ec528ac142c565c2edd` (PR 52). Main and the branch did NOT move during the gate (gh api -X GET
01:55:42 and 02:43:31; open pull requests 0 both times; open code-scanning alerts 0). Read and measured 2026-11-26 01:55
to 02:45 AEDT in my scratch `fleet/state/s328/g2103/`: `clone` (clone.py draft: push URL `invalid://no-push`, no
identity; detached at the head; the mutants ran here), worktrees `red` (BASE + `1-red.diff`) and `probe` (the head +
two probe files of mine, `GateProbeTests.cs` in each test project, never committed, never pushed). Every heavy job
through the kit's `heavy.py` (sha256 31adedc8...) and the wave lock, one at a time (lock waits 0 to 5 each, load-gated;
load1 reached 22.9 from other seats); the 67 released lock folders are mine, in `g2103/_quarantine/locks/`; no other
holder's lock or file touched; the lock absent at 02:43.

**BLUF.** On every path I could build, the lane does what its G1 questions ask: **no path of `oxpd1 write` sends a
register whose id a record already holds, in any letter case** (T03 both cases; my E1: held lower, typed upper: exit 10,
ONE request, no list), **absence is never inferred from a records read it could not read whole** (50 records shapes, controls included:
every shape whose ids cannot all be read as HP's 8-4-4-4-12 form ends `MalformedAnswer`, exit 8, nothing written),
**no record carries an icon, a credential, a post body or a non-https target** (the register body's elements are
exactly id, title, description, requestedPosition, browserTarget/webApplication/uri, binding; the target rule refuses
`http`, user information and more than 256 characters, in the writer and the lab alike), **every register that may
have taken effect is owed** (Answered Yes and Fault/Unknown owed, 401/403 not, the Pending line entered before the send;
a dead run's Pending line owed: my F5), and **the records read carries `admin` on all 29 probe reads whose header I recorded, never `guest`**.
**`undo-owed`'s family key (D7) closes gate B2096 FOUND 1** (its E2 and E4 re-run: the import stays owed; a register of
its id is owed beside it) **and changes nothing within one family** (import/remove, register/unregister, enable/disable
each "nothing is owed"; every landed cell green). The head is BASE plus the two frozen patches byte for byte; red first
exactly the 27 cases, each by assertion; `total: 2338`, `failed: 0`; `MUTANTS: 17 of 17 MATCH, 17 of 17 undone equal`
(my run of the frozen tool), each red on exactly its cases; `HOSTED 1c7cdbbb...: PASS` (my read). **Tuesday's point
(`Family`'s default arm): a Minor, not a blocker** (FOUND 1). One more Minor (FOUND 2, the B2096 FOUND 4 class, now in
a third reader), five Info. **None blocks the landing.**

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (Tuesday's S1 point: `Family`'s default arm `_ => "button"` puts any write kind without its
   own arm in the button family).** `LabFiles.cs:414`-`:420`; the arm at `:419`. MEASURED (`logs/probe-family.tsv`,
   `UndoList.Family` over `Enum.GetValues<Oxpd1WriteKind>()`): the eight kinds map to four families exactly (agent 2,
   test 2, certificate 2, button 2: `kinds 8 families 4`); an unnamed value `(Oxpd1WriteKind)99` maps to `button`. Reach
   TODAY: none. `UndoList.Parse` (`LabFiles.cs:428`, inside `:422`-`:436`) refuses any write that is not one of the eight NAMES, and
   only the eight are owed or clear (`:398`, `:403`), so the default arm is reached by the two button kinds alone. The
   latent defect: a ninth kind added to the closed enum and to the owed/clear sets without its own `Family` arm would
   silently share the button family's owed rule (an unregister of the new kind clearing an owed button, and the
   reverse), and NO cell would fail: `WriteTests.W01` pins the catalogue against the enum, nothing pins `Family`
   (T08 and `mFamilyDropped` prove the key holds the family, not that every kind has its own). The kit's own sentence
   "no two families share one" (`:413`) is true of today's enum only. Acceptable for a closed enum of eight AS IT
   STANDS; a Minor because it defeats the property it states without a test when the enum next grows, and the enum is
   expected to grow (the end-of-session list's firewall rule). Fix when the next write kind is added: name the button
   kinds in their own arm, make the default throw, and add a cell that maps every enum value to a family.
2. **Minor, does NOT block (the button records reader takes a no-break space beside the records or beside the result;
   HP's schema refuses both).** `Oxpd1Writer.cs` `OnlyElements` (the landed helper, `.NET`'s `IsNullOrWhiteSpace`, not
   XML's four characters), called at `:720` and `:726` by `ReadButtons`. MEASURED through the real client and the stub
   (`logs/probe-records.tsv` S09, S10; `logs/probe-records-full.tsv` F09, F10, with full schema-valid records whose
   control F00 reads schema errors 0): `Answered`, listed 1, HP's committed schema errors 1 each. Harm: none to the
   decision: every RECORD is still read whole and its id compared. Gate B2096 FOUND 4's class, now in a third reader;
   the kit named it (Q10, "the button reader inherits its no-break-space limit") and left `OnlyElements` unchanged by
   its HOLDS. Over-claim: the adapter README's "holding ONE `GetTopLevelButtonRecordsResult` and nothing beside it".
   Fix with B2070 FOUND 1 and B2096 FOUND 4: one change to `OnlyElements`.
3. **Info (the records reader does not check a record's parts beside its id; by D3's design).** `ReadButtons`
   (`Oxpd1Writer.cs:732`-`:737`) takes `record.Elements(ns + "id")` alone. MEASURED (`probe-records-full.tsv`): a foreign
   element after the id (F12), text inside a record (F13), the id after the other parts (F14), and a record of an id
   alone (F30): each `Answered`, each HP-schema errors 1. In every one the id is read whole and compared, so the
   register's decision is right; the kit states the design ("A record's title, target and icon are the device's and
   are not read"). The reader is therefore stricter than the schema on the id and looser on the rest.
4. **Info (the writer's record type takes a title XML cannot carry; building the request then throws before any
   connection).** `Oxpd1Writer.cs:283`-`:287` checks blank and length only, as the landed `Oxpd1SignInAgent` does (the
   seat's H20 b, which marked the envelope's behaviour UNMEASURED). MEASURED (`logs/probe-body.tsv` N01 to N03, N07):
   U+FFFE, U+0001 and a lone high surrogate: the type takes them, `WriteAsync` (a dry run) throws `ArgumentException`
   from the `XmlWriter` (`CheckCharacters` is on by default); a tab and a line feed: taken and written, schema errors
   0. The lab refuses every one at the command line, exit 2, no folder, 0 TLS connections (`logs/probe-cli.tsv` C10 to
   C12; T07). Since the envelope is built before `SendWriteAsync` (`Oxpd1Writer.cs:575`), no byte leaves; reach only
   through the library called directly.
5. **Info (the lab writes and sends every id in lower case, so it cannot unregister a record the device holds in upper
   case).** `Oxpd1Writer.cs` `Body` writes `AgentId.ToString("D")`; the lab parses `--button-id` to a `Guid`. MEASURED
   (`logs/probe-exec.tsv`): E2, the device holds the id lower case, the unregister typed upper case: exit 0, removed;
   E3, the device holds the id UPPER case (another caller's record), the unregister: answered, the stub's record stays
   (HP: ids compared as case-sensitive strings), the read after prints "a button with this id is on the device after
   the write", and the undo list row is `UnregisterTopLevelButton ... Answered Yes`. The run's OWN register is always
   written lower case and its undo sent lower case, so the owed rule is right for the lane's writes; the read after is
   reported only (D5). Carry into the device kit: note how the M577 writes ids.
6. **Info (the records reader refuses `xml:lang` on a record, which HP's schema takes: the safe side).** MEASURED
   (`probe-records-full.tsv` F23): `MalformedAnswer`, schema errors 0. A device that writes it would stop every
   register at exit 8 with nothing written; carry into the device kit (read the read-before line first).
7. **Info (a target with a non-ASCII host is written in its Unicode form).** MEASURED (`probe-body.tsv` T10):
   `https://bücher.example/b` taken, the body's `uri` is the Unicode `AbsoluteUri`, schema errors 0. The lab's
   `Address` (`Oxpd1Command.cs:770`) makes the same `Uri` (DERIVED, not run through the lab). What the M577 does with it:
   UNMEASURED.

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole** (`scratch/treecheck.py`): `--name-status` eleven rows, 2 `A`, 9 `M`; numstat equal to
  THE CODE's (4/3, 263/9, 37/10, 25/7, 154/8, 50/17, 32/0, 219/0, 1/1, 62/0, 267/0) and to `compare`'s file list; ONE
  commit, parent 1ccf6d0c, author and committer the repo's `@datasec.com.au` address; `ls-tree` 677 at BASE, 679 at the
  head; the commit message equals `commit-message.txt` (442 bytes, 3 lines, subject 384). Every changed `src/` line
  read (both `.cs` files of the adapter, both of the Lab, both READMEs); the tests read whole (`TopLevelButtonTests.cs`,
  `Oxpd1TopLevelButtonTests.cs`, the two stubs' added lines, `WriteTests.cs`'s one line).
- **The two patches against THE TOOLS:** my copy of the ten tools 10 of 10 equal to THE TOOLS' sha256 (`1-red.diff`
  a588bae7..., `2-fix.diff` 6f995bd0..., `mutants_b4.py` af0c1f33..., `heavy.py` 31adedc8... = S8); temporary index
  `read-tree 1ccf6d0c`, `apply --cached` both rc 0, `write-tree` `e20eeff6` = `1c7cdbbb^{tree}` (EQUAL); red tree
  `4d515102` (= the kit's red tree); each file's sha256 and line count at BASE, in the red tree and at the head equal
  THE CODE's three columns (11 of 11 each; both READMEs at BASE in the red tree).
- **Red first** (`g2103/red`, `logs/r-exe-adapter.log`, `r-exe-lab.log`, `scratch/redcheck.py`): locked restore rc 0
  with exactly the patch's 9 paths in the status (7 ` M`, 2 `??`); build `0 Warning(s)`, `0 Error(s)`; adapter
  `Total: 104, Errors: 0, Failed: 14`, Lab `Total: 297, Errors: 0, Failed: 13`; the 27 `[FAIL]` cases equal THE
  CONTROLS' list (program compare: True, True; missing 0, extra 0, other classes 0); 27 of 27 followed within five
  lines by an `Assert.<name>() Failure` line.
- **Head green** (`logs/h-test.log`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; `total: 2338`, `failed:
  0`, `succeeded: 2334`, `skipped: 4`. The probe tree (head + my two probe files) ran each test executable whole:
  adapter `Total: 106, Failed: 0` then `Total: 107, Failed: 0` (a third probe added), Lab `Total: 301, Failed: 0` (the
  104 and 297 plus my probes).
- **Mutants** (`logs/mutants.out`, `scratch/mutcases.py`; my run of the frozen `mutants_b4.py`, 02:00 to 02:43,
  load-gated): `MUTANTS: 17 of 17 MATCH, 17 of 17 undone equal`, every row's Total and red set equal to the kit's
  MEASURED line; by CASE: `mPositionUnbounded` B02; `mTargetHttpTaken` B02; `mRegisterUndoDropped` B01, B03, T02, T05
  `500`; `mBodyPositionDropped` B01; `mBadRecordSkipped` B04 `a record with no id`, `a record with two ids`, `an
  attribute on a record`, `an id holding an element`, `an id that is not a uuid`, `an id with white space`, `another
  element beside`, T04 `a record with no id`; `mResponseAttributeTaken` B04 `an attribute on the response`;
  `mResultTextTaken` B04 `text beside`; `mUuidLoose` B04 `an id that is not a uuid`, `an id with white space`;
  `mHoldsCaseSensitive` B04 `the id in upper case`, T03 `the same id in upper case`; `mButtonReadAsGuest` B03, B05,
  T02; `mHeldIgnored` T03 both rows; `mNoReadBefore` T02, T03 both, T04 all four, T05 both; `mNoButtonReadAfter` T02,
  T06; `mUnregisterTakesRecord` T07 `an unregister with a title`; `mOtherWriteTakesButton` T07 `a test service write
  with a button id`; `mButtonNotOwed` T08; `mFamilyDropped` T08. Each is exactly the cases its edit can reach; no other
  class red; the clone's porcelain 0 lines after and HEAD still 1c7cdbbb.
- **Whether ANY path of `oxpd1 write` sends a register whose id a record already holds (in any letter case):** no. The
  register is sent only after `ReadBeforeButtonAsync` (`Oxpd1Command.cs:1148`) returned null, which needs an
  `Answered` read and `!records.Holds(buttonId)` (`:1166`); `Holds` (`Oxpd1Writer.cs:447`) compares parsed `Guid`s,
  so any case. T03 (both cases), my E1 (held lower, typed upper: exit 10, posts 1, no list), S18/S19 and F19 (mixed
  and upper case read and held). Named limit H14 (a button added between the read and the register) stands.
  **Infers absence from a records read it could not read whole:** no: 50 shapes (`probe-records.tsv` 29,
  `probe-records-full.tsv` 21, two of them controls; B04's 14 among the kinds), every one whose ids are not all one text-only `id` of HP's
  form ends `MalformedAnswer` (exit 8 before any write, T04); the schema-refused shapes that ARE read (FOUND 2, FOUND
  3) each still read every id whole. **Sends a record with an icon, a credential, a post body or a non-https target:**
  no: `Body` (`Oxpd1Writer.cs:841`-`:866`) writes exactly id, title, description, requestedPosition and
  browserTarget/webApplication/uri/binding `Plain` (my P02: the register body's descendants listed; `networkCredentials`
  0, `initialPost` 0; "icon" appears only inside the namespace word `uiconfiguration`); `git grep -i` of `icon`,
  `networkCredentials`, `initialPostQuery` in the two source files: no element written. The target: `http`, user
  information and over 256 (`AbsoluteUri`) refused by the type (`:290`) and by the lab's `Address` (`:770`), which
  also refuses any `@`. **Leaves a register that may have taken effect not owed:** no: `WriteAsync`'s `Applied` is No
  only for NoCredential, PinRefused, 401 and 403 (`Oxpd1Writer.cs:583`-`:587`) and the undo travels whenever it is not
  No (`:590`); the lab enters the Pending line BEFORE the send (`Oxpd1Command.cs:961`-`:963`); `undo-owed` owes every
  register not `Applied No` (`LabFiles.cs:398`); T05 (`500` owed, `403` not), my F5 (Pending owed) and F10 (403 not),
  `mButtonNotOwed`, `mRegisterUndoDropped`.
- **The records shapes HP's schema refuses** (`probe-records.tsv`, `probe-records-full.tsv`, each with HP's committed
  schema's error count; the full-record control F00 reads 0): a processing instruction (S01, F01), a comment (S02, F02)
  and a character reference (S03, F03) inside an id are schema-VALID and read (the parser drops PIs and comments; the
  text is whole), as is CDATA (S17, F17); an id in another namespace (S04, F04) or in none (S05), `xsi:nil` on the id
  (S06, F06), a record (S07) or the result (S08), braces (S15, F15) or no hyphens (S16, F16) (H13), white space in or
  around the id (S11, S22, F22), a non-ASCII digit or hyphen (S24, S27), a record of another name (S20): all
  `MalformedAnswer`. A no-break space beside the records (S09, F09) or the result (S10, F10): READ (FOUND 2). Text, a
  foreign element or order inside a record (F12 to F14, F30): READ (FOUND 3). `xml:lang` on a record: refused,
  schema-valid (FOUND 6).
- **Whether the records read can carry `guest`:** no. `ReadTopLevelButtonsAsync` (`Oxpd1Writer.cs:677`) calls only
  `SendAdminReadAsync` (`:686`), which passes the landed constant `admin`; `git grep`: `SendAdminReadAsync(` 1
  definition (`Oxpd1Client.cs:120`) and 2 calls (`Oxpd1Writer.cs:610`, `:686`); `ReadTopLevelButtonsAsync(` called by
  the Lab twice (`Oxpd1Command.cs:990`, `:1150`). Every one of the 29 probe reads whose header I recorded (`probe-records.tsv`) carried `Basic YWRt...` (admin);
  `mButtonReadAsGuest` red on B03, B05, T02.
- **Whether `undo-owed`'s family key changes any landed `undo-owed` behaviour within one family:** no. Within one
  family the match is as before (`LabFiles.cs:397`: the family is a function of the kind, and a write and its undo share
  one, `probe-family.tsv`); MEASURED through the real verb (`logs/probe-owed.tsv`): F7 import then remove, F8 agent
  register then unregister, F9 enable then disable, each exit 0 "nothing is owed"; F11 a faulted unregister clears
  nothing; every landed cell of `Oxpd1WriteTests`, `Oxpd1TestServiceTests` and `Oxpd1CaStoreTests` green (Lab
  executable whole `Total: 297` then `301`, `Failed: 0`). Across families it now holds: F1 (B2096 E2) the import still
  owed, exit 11; F2 (B2096 E4) the import AND the register owed; F3 a button still owed after a certificate remove of
  its id; F4 another host clears nothing. **Gate B2096 FOUND 1 is closed by this head** (FOR-RECORDS.md).
- **The README sentences against the code:** every changed or added sentence of both READMEs read against the head:
  the three UIConfiguration rows (`Oxpd1Writer.cs:113`-`:114`, `:677`, `:686`), "Eight writes" (W01 8), "The top-level
  buttons." (`:269`, `:290`, `:295`, `:365`, `:447`, `:700`, `:739`, `:752`, `:836`, `:844`; FOUND 2's "nothing beside
  it" over-claim), the Limits ("Only first-run steps 5, 2, 3 and 4", "not run against a device"); the Lab's opening,
  the `write` heading and options (`Oxpd1Command.cs:513`, `:631`, `:659`, `:667`), "A button register reads first, and
  both button writes read after" (`:954`, `:991`, `:1148`, `:1166`), the refused-password counts (T02 `admin` 3; T06 two
  requests), the undo and undo-list sentences, exit 10 (`Oxpd1Command.cs:207`), the `undo-owed` family paragraph
  (`LabFiles.cs:397`, `:414`; F1 to F4), the Limits (H14's sentence, the CA store sentence's "host, family and that
  id"). One over-claim (FOUND 2); none of the lane's own words over-claims beyond it.
- **D8's one landed literal and nothing else of a landed cell:** removed lines under `tests/`: exactly 1
  (`WriteTests.cs` `Assert.Equal(6, Oxpd1WriteCatalogue.Rows.Count);` to 8); both stubs gain lines only (32/0, 62/0);
  `Oxpd1Read.cs`, `Oxpd1Soap.cs`, `contracts/`, `.github/`, `build/`, `Datasec.Suite.slnx`, `Directory.Packages.props`:
  `diff --stat` empty; added lines naming `X509Store`, `Process.`, `GetEnvironmentVariable` or `PackageReference`: 0
  (control: `ReadTopLevelButtonsAsync` counts 13 in the same file).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, 02:01): run 45637707044, four
  jobs attempt 1 success, linux `succeeded: 2334`, windows `succeeded: 2317`, `RULES: clean (679 files)`, `UNIT-TEST
  FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15 files)`, `failed Datasec.` lines 0 and 0 (colour codes
  stripped; control: 4 `Oxpd1.Tests.dll` and 4 `Lab.Tests.dll` lines per leg); check runs beside the four: 0; last
  line `HOSTED 1c7cdbbb790f287c3ef9e9544fb3a1848f45bf49: PASS`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. TUESDAY'S OWN POINT (the kit's S1)

`Family` (`LabFiles.cs:414`) maps agent, test and certificate kinds and sends every other kind through `_ => "button"`.
For the closed enum of eight AS IT STANDS this is correct and exhaustive (MEASURED, FOUND 1), and no input reaches the
default arm but the two button kinds (`Parse` refuses unnamed values). It is a **Minor** finding, not acceptable as a
permanent form: the arm is a silent sink for the next kind, and nothing in the suite would notice. Does NOT block.

## 3. ADVERSARIAL BEYOND THE KIT (the commission's six shapes, then three outside each property)

- **An id with braces or no hyphens in a device answer (H13):** both `MalformedAnswer`, HP schema errors 1 each (S15,
  S16, F15, F16): the register stops at exit 8 with nothing written. The named limit holds, on the safe side. On the
  command line both are usage errors (C08, C09).
- **A title with characters XML cannot carry:** the lab refuses U+FFFE, a lone surrogate and U+0001 (C10 to C12, exit 2,
  no folder, 0 TLS); the writer's type takes them and the request build throws before any connection (FOUND 4);
  markup characters are escaped and schema-valid (C13, N04).
- **A target of exactly 256 and 257 characters:** 256 TAKEN (T01: `AbsoluteUri` 256, the body's `uri` 256, schema 0;
  C01 exit 0), 257 REFUSED (T02 `ArgumentException`; C02 exit 2). A target that the `Uri` lengthens past 256 (spaces
  escaped) is refused by both (T07, C20); one it shortens (`:443` dropped, the host lower-cased) to 254 is taken and
  sent as 254 (T06).
- **A target with a fragment or a non-default port:** both TAKEN and sent as written, schema 0 (T03, T04; C03, C04);
  `:443` written is dropped (T05, C05).
- **An id upper case on the device and lower case in the register:** exit 10, one request, nothing written (T03 `the
  same id in upper case`; the reverse, my E1). The unregister side: FOUND 5.
- **An unregister while a register of the same id is owed on another host:** clears nothing (T08 r3; my F4: exit 11,
  the owed line names 127.0.0.1).
- **Three shapes outside each property** (the kit's P1 to P6):
  P1 (ONE record in HP's shape, nothing else): a title with tab and line feed (N07, sent, schema 0), a unicode host
  (T10: FOUND 7), an `@` in the target's path (T08: the writer takes it, schema 0; the lab refuses it, C06): covered.
  P2 (a register only after an answered read listing no record with its id, any case): the id held twice (S21/F21:
  listed 2, held), held in mixed case (S18), the read answering an empty result (S26/F00b: Answered 0, schema 0, the
  register proceeds, as HP's description allows): covered.
  P3 (answered only when every record holds one UUID-form id): a no-break space beside the records (S09: FOUND 2), a
  foreign element after the id (F12: FOUND 3), `xml:lang` on a record (F23: FOUND 6).
  P4 (every register that may have taken effect owed until an answered unregister on the same host; only the button
  family clears it): a Pending line of a dead run (F5 owed), a faulted unregister (F11 still owed), a certificate
  remove of the same id (F3 still owed): covered; a future kind without its own family (FOUND 1).
  P5 (`admin`, never `guest`): no setting (B05: no connection), every recorded probe read (29 of 29 admin), `mButtonReadAsGuest`:
  covered.
  P6 (the password in no output or file): the dry run reads no password and prints none (E4: password False, tls 0);
  the cells' `AssertNowhere` (T02 to T06); my P02 (the request text holds the password: False): covered.

## 4. SCANS

- **gitleaks 8.30.1** (`logs/gitleaks.out`): control FIRST, a token built in-process from two halves and 36 random
  characters, never printed, outside the clone: rc 1, `leaks found: 1`, moved to `g2103/_quarantine/gl-control-code`;
  then `gitleaks git` over `BASE..1c7cdbbb` rc 0 (`1 commits scanned`, `no leaks found`); the eleven head blobs, both
  patches, the message file, `mutants_b4.py`, `checks_b4.py` and the commit's own message as `1.txt` to `17.txt` in a
  new folder: rc 0 `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 1114 added lines of `BASE..head`
  (`scratch/added.txt`, made by `git diff` for this gate, the same count as the seat's `checks_b4.py` `added 1114`),
  the head's commit message and `commit-message.txt`: every class 0, `WORDS: clean (3 files)`; `B2[0-9]{3}` 0 and 0
  (control: the kit counts 29 lines).
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#53`, `squash-body.txt` and
  `pr-title.txt`: `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 2 and `coordinator` 2 (the "Still open" and
  "Who decides" sections: the device run needs his word, as the commission asks), 4 bytes outside ASCII (the
  attribution line's emoji), every other class 0; `B[12][0-9]{3}` and `X7[0-9]` 0 in all four; `build/squash_scan.py`
  (BASE's, equal to the head's: `build/**` and `.github/**` are not in the diff, `diff --quiet` rc 0) with `#53`:
  control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`; gitleaks over this folder's six landing texts and
  the `#53` subject under neutral names, the control re-planted first (rc 1, `leaks found: 1`, quarantined): rc 0,
  `no leaks found` (02:18); again after the last edits, with VERDICT.md, 8 files, control first: rc 0 (02:45).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). `checks_b4.py` (it reads a STAGED tree; the seat's `CHECKS: 10 of 10
PASS` is RELAYED; its rows 1, 3, 5, 7, 8, 9 and 10 re-measured above by `git diff` and `git grep`). The chain's publish
and release guard, `repo_rules.py`, the unit tests of `build/tests` (RELAYED from the seat; equal on the hosted legs, my
read). The whole solution after the mutants (the clone's porcelain is 0 lines after the tool's undo and HEAD is
1c7cdbbb, so the measured head is the bytes that ran). The unicode host through the lab (FOUND 7, DERIVED). A button
added between the read and the register (H14, no race harness). Any device.

## OUTSIDE THE FENCES

None. Writes: this folder and `fleet/state/s328/g2103/` only (my clone, its two worktrees, logs, scratch, quarantine).
No pull request, no push (the clone's push URL is `invalid://no-push`), no re-run of a hosted job, no `cd`, nothing
deleted, no printer or device, no Azure, nothing to any person, no Jira. Every gh call a GET under the project's
GH_CONFIG_DIR. One in-place `sed -i` on my own uncommitted probe file in my scratch worktree (a rename of a local
function before its first build); nothing of the project's was edited. No print of `kam_rulings_today.sh` or
`kam_msgs.sh` was made or saved. No background process of mine is left running; the wave lock is absent.
