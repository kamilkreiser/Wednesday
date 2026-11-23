GATE B2026: GO WITH FINDINGS @ 28b2533 on main b0b26b6
**THE HOLD (for Tuesday; the two lift conditions, each by its measurement):**
**B2016 FOUND 1: CLOSED.** `undo-owed` no longer prints `nothing is owed` or ends 0 having read no entry: 0 of the 15 probe shapes that read no entry (B2016's four, symbolic links, a list that is a folder, permission, others): 3 end exit 2, 11 end exit 11, 1 throws.
**B2016 FOUND 2: CLOSED for every child ELEMENT of the read's result (exit 10, no write), NOT for the wider question of this commission:** an attribute, a processing instruction, a comment, text or CDATA in the result, and an `id` of another namespace beside a record's own, each let the register through (MEASURED, FOUND 1 below, Minor). HP's schema is element-only; the M577's answer is UNMEASURED.
**This gate's reading: land the head; both lift conditions are met as gate B2016 wrote them; lifting the hold is Tuesday's, and the remainder of FOUND 2 is carried by one step in the first real run (look at an `oxpd1 read --read GetAuthenticationAgentRecords` answer before any executed register) and a ticket.**

Gate G1, round 2 of 2 of lane W2 (round 1: gate B2016, GO WITH FINDINGS @ 67c24d1), one Fable reader (claude-fable-5-2),
in-session, read-only. OXPd 2, lane W2, kit B2021 (seat X61; S4: Q1 "a" and Q2 "a" in words, Q3 to Q10 the defaults; each
the coordinator's, none the product owner's). Head `28b25332432da5e43ea1db87c5442771dd910c70` on
`b2021/w2-lab-write-fixes`, ONE commit, one parent `b0b26b60` = main (BASE, stamp S2). Read and measured 2026-11-24 09:35
to 09:51 AEDT in my scratch `fleet/state/s320/g2026/`: `clone` (clone.py draft at 09:36: push URL `invalid://no-push`,
no identity; detached at the head), worktrees `red` (BASE + `1-red.diff`), `pat` (BASE + both patches, staged) and `prb`
(the head + ONE test-only probe file, `scratch/G2026ProbeTests.cs`, never committed). Every dotnet job and test executable
through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock (35 jobs, 35 released lock folders, all mine, in
`g2026/_quarantine/locks/`; the lock absent at the end; no other holder's lock touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No
write to the project, GitHub or Jira; no push, no pull request, no re-run; the lab tool was driven only in-process by the
test assembly against the tests' own 127.0.0.1 stubs; no printer, no tenant; nothing deleted.

**Tuesday's five facts, each re-measured (gh api -X GET, 09:36):** the branch ref = `28b25332432da5e43ea1db87c5442771dd910c70`
(one row under `heads/b2021`); compare main...head `ahead 1, behind 0`, merge base `b0b26b60`; exactly five files, all
`modified` (LabFiles.cs +35 -4, Oxpd1Command.cs +55 -10, the oxpd1 README +42 -15, Oxpd1Stub.cs +8 -0, Oxpd1WriteTests.cs
+157 -0); main `b0b26b60a37cf771a2121000ca60f420658e0088` (one parent `c5b103ee`, tree `b2a09571`); open pull requests 0
(newest 44, closed). The seat's STATUS (read whole, 294 lines) ends `READY B2021: 28b25332432da5e43ea1db87c5442771dd910c70`
and holds `HOSTED 28b25332432da5e43ea1db87c5442771dd910c70: PASS` (line 245). Each equal to what Tuesday read.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`pat` `write-tree` `ec57df8b` = `28b25332^{tree}`;
the five files' sha256 5 of 5 equal to THE CODE at BASE, after `1-red.diff` and after both; the commit message =
`commit-message.txt`, 423 bytes); the ten tools of my copy and of the seat's copy equal THE TOOLS' sha256 (10 of 10 each).
Five paths, all M, numstat equal to the kit's table, `checks_w2r2.py` 8 of 8 with every control. Red first on BASE: Lab
`Total: 187, Errors: 0, Failed: 16`, exactly the kit's 16 cases, each followed by an `Assert.Equal() Failure` line, none
outside `Oxpd1WriteTests`. Green 2112 / 0 / 2108 / 4. `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal` (my run of the frozen tool; after it the clone clean, both
mutated files equal to the head, rebuild 0/0, 2112 / 0 / 2108 / 4 again). RULES 657, `Ran 111 tests` OK. Hosted push run of the
head PASS on both legs (linux 2108, windows 2091). **The four questions, MEASURED with a probe of 74 cases (Lab executable
`Total: 261, Errors: 0, Failed: 0` = 187 + 74):** FOUND 1 of B2016 is closed (30 `undo-owed` shapes; one new silent pass
of a different kind, FOUND 3 below); FOUND 2 is closed for child elements and open for non-element content (FOUND 1
below); FOUND 3 is closed for the agent name (65536 of 65536 single code units: none accepted that the XML writer
refuses) and open for ONE code unit in the host of the two addresses (FOUND 2 below, the kit's H12); FOUND 4 is closed
(the printed undo, run as printed, reached the stub with the register's addressing, password name, port, pins and
time-out). Nothing the fixes touched is broken: every landed cell is green (the two test files have 0 deleted lines) and
a pretty-printed answer still reads. No Blocker, no Major, three Minor, three Info.

## WHAT ROUND 2 MUST ANSWER FIRST

### 1. B2016 FOUND 1 closed? YES.
Can `undo-owed` still print `nothing is owed` or exit 0 having read no entry? **No shape found (probe P1, 30 shapes; each
line is `exit`, then whether the output holds `nothing is owed`).**

| Shape | Exit | `nothing is owed` | What it printed |
|---|---|---|---|
| B2016 (a) the run folder itself given | 2 | no | `the folder given holds undo-list.tsv itself: it is a run folder ... nothing was read` |
| B2016 (b) the session one level below | 11 | no | `0 executed writes in 0 run folders`, `no undo list was read`, `not confirmed` |
| B2016 (c) an empty list; (d) a header-only list | 11 | no | `unreadable: r1/undo-list.tsv, which holds no entry line (not shown)` |
| links: a symbolic link to a run folder holding a register | 11 | no | followed and read: `owed: ...` |
| links: two linked run folders, a register and its answered unregister | 0 | yes | `2 executed writes in 2 run folders` (entries read) |
| links: a dangling link only | 11 | no | `no undo list was read` |
| links: the folder given is a link to a run folder | 2 | no | refused as a run folder |
| links: the folder given is a link to the session | 11 | no | read: `owed: ...` |
| links: the list is a link to a list elsewhere | 11 | no | read: `owed: ...` |
| links: the list is a dangling link (alone; beside a clean pair) | 11; 11 | no; no | `unreadable: r5/undo-list.tsv (FileNotFoundException) (not shown)` |
| folder: the list file is a folder, alone | 11 | no | `no undo list was read` |
| folder: the list file is a folder, beside a clean pair | 0 | yes | `2 executed writes in 2 run folders` (the two real lists read; a folder holds no entry) |
| folder: the folder given holds a FOLDER named `undo-list.tsv` and a run folder with a register | 11 | no | not taken for a run folder; read: `owed: ...` |
| permission: the list mode 000 (alone; beside a clean pair) | 11; 11 | no; no | `unreadable: r5/undo-list.tsv (UnauthorizedAccessException) (not shown)` |
| permission: the run folder mode 000, alone | 11 | no | `no undo list was read` |
| permission: the run folder mode 000 (holding a later register), beside a clean pair | **0** | **yes** | `2 executed writes in 2 run folders ... nothing is owed` (**FOUND 3**) |
| permission: the session folder mode 000 | throws | no | `UnauthorizedAccessException`, unhandled (FOUND 3) |
| only `undo-list.tsv.new` (kit H6) | 11 | no | `no undo list was read` |
| blank lines only | 11 | no | `unreadable: ... line 1`, `line 2` |
| a byte order mark and the header only | 11 | no | `which holds no entry line` |
| CRLF line ends, a register | 11 | no | read: `owed: ...` |
| a header-only list beside a clean pair | 11 | no | `2 executed writes in 3 run folders`, `0 undos owed, 1 unreadable` |
| the folder given is a file | 2 | no | `the session folder does not exist` |
| one answered unregister only; one refused register only (applied No) | 0; 0 | yes; yes | `1 executed writes in 1 run folders` (an entry read; nothing to owe) |
| controls: a clean pair; a register owed | 0; 11 | yes; no | as the landed cells |

Source (DERIVED, `LabFiles.cs:132` to `:176`, `:252`, `:269`, `:290`): every list the loop counts (`files++`, `:141`) ends
either in `unreadable` or with at least one line that does not start `#`, and each such line is an entry or `unreadable`;
`clean` needs `Files > 0` and no `unreadable`; so exit 0 implies at least one parsed entry. The code path and the 30
measurements agree. The six rows that print `nothing is owed` each read at least one entry. **The one row to act on is
the mode-000 run folder beside readable lists: it is not "no entry read", it is "a folder not looked into"; FOUND 3.**

### 2. B2016 FOUND 2 closed? For child elements YES; for the commission's wider list NO.
Does ANY child shape of the read's result outside HP's record shape let the register through? (probe P2, 23 answers to
`GetAuthenticationAgentRecords` from a raw stub; an executed register of id A; "sent" = one read, one write, exit 0, the
list `Answered`/`Yes`.)

| Answer shape | Outcome |
|---|---|
| a child element that is not a schema record: another namespace, wrapped, unqualified, another element; a record with two ids (cells V12, 5 rows; mutants `mOtherChildIgnored`, `mFirstIdOnly`) | exit 10, one request, no write, no list |
| the same id: plain; pretty-printed with white space; in parentheses; inside a child element of `id`; after 300 records of other ids | exit 10, no write (`a sign-in agent with this id is already on the device`) |
| an id with a `urn:uuid:` prefix; an `id` holding a comment only | exit 10, no write (`no readable id`) |
| two result elements | exit 8, no write (the client's own reading: malformed) |
| **an attribute on the result holding the id** | **sent** (`records on the device: 0`) |
| **a processing instruction in the result holding the id** | **sent** (0 records) |
| **a comment in the result holding a same-id record** | **sent** (0 records) |
| **text only: the records as escaped XML, the same id; CDATA only, the same** | **sent** (0 records) |
| **mixed content: another agent's record and text holding the id** | **sent** (1 record) |
| **a record of another id with an `id` of another namespace holding the same id beside its own** | **sent** (1 record) |
| **the same with an unqualified `id`; with another element (`agentId`) holding it; with an attribute of its `id` holding it** | **sent** (1 record) |
| **a same-id record beside the result, inside the response (kit H9)** | **sent** (0 records; `Oxpd1Soap.cs:165` takes the one result and reads no sibling) |
| a result marked `xsi:nil="true"`, no child | sent (0 records) |
| controls: no record; another agent only (also pretty-printed) | sent (0; 1 record), as cell V13 |

So: every child ELEMENT outside the record shape stops the register (what gate B2016's FOUND 2 asked: "fail closed when
the result holds any child element that is not a schema record"). Everything that is not a child element, and anything
inside a record but its own-namespace `id`, is not read. **FOUND 1 below.**

### 3. B2016 FOUND 3 and 4 closed? The name YES; the addresses but for ONE code unit; the undo YES.
- **The agent name (probe P3a).** Each of the 65536 UTF-16 code units placed alone between two letters, through
  `Oxpd1WriteOptions.Parse`, against an `XmlWriter` with the envelope's settings: accepted 63421, refused 2115, **accepted
  yet the writer throws 0**; refused yet writable 36 (the control characters XML allows; the landed control rule).
  Pairs: U+1F600 and U+10FFFF accepted and writable; a reversed pair, high+high+low, a high half at the end, a low half
  at the start, a high half then a letter: refused (the writer refuses each too). Real runs (P3c): a reversed pair and a
  high half at the end: exit 2, no run folder, TLS 0; U+FFFD and `<&>"'`: exit 0, written.
- **`--agent-service` and `--prompt-page`, the kit's H12 (probe P3b, P3c).** Each of the 65536 code units in the path, the
  query and the fragment of each option: 65535 accepted (`@` refused), **0 that the writer refuses**: `AbsoluteUri` is
  ASCII for all of them (U+FFFE is written `%EF%BF%BE`, a lone surrogate `%EF%BF%BD`, U+0001 `%01`); real runs dry and
  executed: exit 0, the envelope well-formed. In the HOST: 63395 accepted, 2141 refused (U+FFFE among them, exit 2),
  63317 accepted with a non-ASCII `AbsoluteUri` (the host is written as typed), and **ONE accepted that the writer
  refuses: U+FFFF.** Real runs with `https://lab<U+FFFF>host.example/...`: a dry run throws `ArgumentException` (from
  `XmlUtf8RawTextWriter`) after the run folder is made (no file in it, TLS 0); an executed register, in either option,
  throws AFTER its read (one request, no write), leaving `oxpd1-client.log` and an `undo-list.tsv` row `Pending`/`Unknown`
  for a write never sent, and no summary. **FOUND 2 below.**
- **The printed undo (probe P4).** A register with two pins, `--addressing 2004`, `--password-name SYNTHETIC_OTHER_NAME`,
  `--timeout-seconds 7` (dry and executed), and one with every option at its default but the port (executed): the printed
  line carries `--password-name`, both pins in order, `--soap-port`, `--addressing`, `--timeout-seconds`; parsed back,
  every connection option equals the register's (pins 2 of 2). **Run as printed** (the two placeholders filled, nothing
  else changed): exit 0, ONE request, its addressing namespace equal to the register's
  (`http://schemas.xmlsoap.org/ws/2004/08/addressing`; `http://www.w3.org/2005/08/addressing` for the default), the
  password under the same name (3 of 3 requests carrying it), the stub's agent removed; `undo-owed` over the two run
  folders then: exit 0, `nothing is owed`; the password in none of the three outputs. No option of
  `Oxpd1WriteOptions` that reaches `ClientOptions` (`Oxpd1Command.cs:676` to `:681`: host, pins, password name, SOAP port,
  time-out, addressing) is missing from `UndoLine` (`:688` to `:695`). The credentials file and the run folder are
  placeholders by design; the `undo-owed` hint line stays a sketch (kit H15, README Limits).

### 4. What the fixes may have broken: nothing found.
- Every landed cell of round 1 is green at the head: whole solution `total: 2112, failed: 0, succeeded: 2108, skipped: 4`
  (my run; the same on both hosted legs, windows 2091); the two test files' numstat is +8 -0 and +157 -0 (no landed cell,
  assertion or helper changed); `1-red.diff` on BASE leaves the 168 landed Lab cases green (187 - 19 new; 16 red, all
  new).
- The read's stricter loop still takes a real answer: white space between records and inside `id` (a pretty-printed
  answer), 300 records, another agent only: read as before.
- README against the code: the table below; two sentences are wider than the code (FOUND 1, FOUND 2).

## FOUND

1. **Minor (the read before a register reads child elements only).** `Oxpd1Command.cs:786` `answer.Elements()` visits
   elements; `:795` reads only `id` children in the result's namespace. MEASURED (P2, the bold rows above): the register is
   sent when the id the run is about to write sits in an attribute, a comment, a processing instruction, text or CDATA of
   the result, or inside another record as an `id` of another namespace, an unqualified `id`, another element or an
   attribute, or in a record beside the result. README `:66` to `:71` ends "an answer the run cannot read whole may hold
   that id": the sentence is wider than the code, and the kit's H9 (a named limit in STATUS) is not in README Limits.
   What bounds it: HP's committed `authentication.xsd` types the result as a sequence of `AuthenticationAgentRecord`
   (`:149`, `:150`, `:200`), with no wildcard and not mixed (grep: 0 `xs:any` and 0 `mixed=` lines in `authentication.xsd`), so
   none of these is a conforming answer; the only one a real service plausibly gives is the records as a string. The
   harm needs that AND an agent already on the device under the id the operator chose. Nothing was sent anywhere but the
   stub. For a ticket: exit 10 when the result holds any non-white-space text or CDATA, or any attribute but a namespace
   declaration; exit 10 when a record holds any child whose local name is `id` beyond its one own; a Limits line for the
   rest (comments, processing instructions, siblings of the result, which the client drops); a cell per shape.
2. **Minor (U+FFFF in an address's host reaches the envelope writer; kit H12, B2016 FOUND 3's class).** `Oxpd1Command.cs:619`
   `Address` checks `@`, https, no user information and length; nothing checks that `AbsoluteUri` is XML text. MEASURED
   (P3b, P3c): one code unit of 65536, in the host only, in either option. README `:87` "a run that stops before the
   write, enter[s] nothing" does not hold for it (a `Pending` row for a write never sent; `undo-owed` then owes an undo of
   nothing: the safe side); README `:56` names the character rule for the name only, which is true. For a ticket: the
   name's `XmlText` on each address's `AbsoluteUri` (or ASCII-only hosts) in the parser.
3. **Minor (`undo-owed` counts a run folder it cannot open as a folder without a list).** `LabFiles.cs:136`
   `File.Exists(path)` is false when the run folder gives no search permission, and the folder is skipped like a dry
   run's. MEASURED (P1): run folder `r5` mode 000 holding a register dated after a clean pair: exit 0,
   `2 executed writes in 2 run folders`, `nothing is owed`. Alone it is exit 11 (no list read). And a session folder that
   cannot be listed (`:132`) throws `UnauthorizedAccessException` unhandled (what exit code the lab's process gives then
   is UNMEASURED: the probe calls the command in-process). README `:104` holds as written (it did read a list, every list
   it saw held an entry); what is missing is that a folder not looked into is not a folder without a list. Needs a
   deliberate or damaged permission; run folders are made by the same user. For a ticket: a run folder whose list cannot
   be tested is named unreadable (exit 11); the session listing's refusal is caught as exit 11.
4. **Info (what the device is given is not always what was typed).** MEASURED (P3b): a non-ASCII host is written as typed
   (`https://lab<U+00E9>host.example/x`, not its ASCII form; 63317 of 65536 single code units), a lone surrogate in a
   path, query or fragment is written as `%EF%BF%BD` (U+FFFD), with exit 0. HP's `anyURI` pattern and what a device does
   with either are UNMEASURED.
5. **Info (the name's length counts UTF-16 code units).** 50 emoji (100 code units) accepted, 51 refused though the README
   says "1 to 100 characters" (`:55`). The adapter's own rule is the same count (`Oxpd1Writer.cs:84`).
6. **Info (probe shapes with no cell).** Cell U05 holds six `undo-owed` shapes; symbolic links, permission, a list that is
   a folder, a byte order mark and blank lines are measured here only. Each is right at the head but FOUND 3's.

## WHAT THE KIT'S GATE LIST ASKED (FOR TUESDAY "THE GATE")

| Question | Answer | How |
|---|---|---|
| `<BASE>..<head>` whole | read whole: the five files' diff (the two sources by `git diff -U1`, the tests and the README at the head), `Oxpd1Writer.cs` whole, `Oxpd1Soap.cs` 118-179, HP's `authentication.xsd` by grep | Read |
| the two patches against THE TOOLS' sha256 | equal (10 of 10 tools, mine and the seat's); BASE + both = the head's tree `ec57df8b`; `2-fix.diff` alone applies on BASE (rc 0: disjoint paths, as the kit says) | `s1.py`, `s2.py` |
| red first on BASE, the 16 cases by assertion | `Total: 187, Errors: 0, Failed: 16`; 16 `[FAIL]` lines, each followed by `Assert.Equal() Failure`; V12 x5, V14 x4, V16 x2, U05 x5; 0 outside the class | `runA.py red`, log `g2026/logs/r-lab.log` |
| each of the 11 mutants red on exactly its cells | 11 of 11 MATCH, each red on exactly its listed cell (Failed 1, 2, 2, 4, 1, 1, 4, 1, 2, 2, 2: the kit's and the seat's counts), 11 of 11 undone equal; clone status 0 lines after | `mutants_w2r2.py run` (my run of the frozen tool) |
| `undo-owed` printing `nothing is owed` or exit 0 having read no entry | no: section 1 | probe P1 |
| a child shape of the result outside HP's record shape letting the register through | elements: none; non-element content and foreign ids: yes (FOUND 1) | probe P2 |
| a name XML cannot carry reaching the envelope writer, also through the two addresses | the name: none of 65536; the addresses: U+FFFF in the host (FOUND 2) | probe P3 |
| the printed undo reaching a device with other options | no: section 3 | probe P4 |
| the README sentences against the code | table below | Read, probe |
| the hosted run on both legs | `HOSTED 28b25332...: PASS` (run 45279875689, attempt 1 each, my read by `hosted3.py`): linux total 2112 x2, succeeded 2108, skipped 4, GUARD 14; windows 2112 x2, 2091, 21, GUARD 15; rules RULES 657, 111 tests, floor 111; secret-scan every proof line; `failed Datasec.` 0 and 0 (control: `skipped Datasec.` 4 and 21); `Datasec.Suite.Lab.Tests.dll` 4 lines each leg; check runs beside the four: 0 (no CodeQL on a branch push) | `hosted3.py` (gate copy), `scan.py legs` |
| `words.py` and gitleaks over the added lines and the message | SCANS below: clean | |

## THE README SENTENCES AGAINST THE CODE (head; "every / never / only / nothing", shapes outside the tested one)

| Sentence (`Commands/Oxpd1/README.md` at the head) | Shapes outside the tested one | Holds? |
|---|---|---|
| `:55`-`:57` the name: no control character and no character XML cannot carry; exit 2 before any folder or connection | 65536 single code units; five ill-formed pair shapes; two well-formed pairs | yes (P3a, P3c, V14, V15); length in code units (FOUND 5) |
| `:64`-`:72` a register reads first; exit 10 on the same id, an unreadable id, "any element that is not a record of HP's schema"; "an answer the run cannot read whole may hold that id" | 23 answers | the element clause yes; the last clause no (FOUND 1) |
| `:72` "A device that holds other agents only is written to" | one record; one pretty-printed; 300 | yes (V13, P2) |
| `:73`-`:76` no request after a refused password; "the lab retries nothing" | unchanged code (gate B2016 measured it); `checks_w2r2.py` check 7: 2 `WriteAsync` calls, equal to BASE | yes; .NET's own re-send UNMEASURED (README `:150`) |
| `:77`-`:83` the undo carries every connection option, "so the undo reaches the device the way the register did"; an exception after the send prints no undo, the `Pending` row stays | two pins, 2004, another name, 7 s; every default; run as printed | yes (P4, V16); the exception clause DERIVED (no `try` in `ExecuteAsync`), as gate B2016 measured for a throw |
| `:84`-`:87` every executed write is entered BEFORE it is sent; "a run that stops before the write, enter[s] nothing" | a host with U+FFFF | the first yes; the second no for that shape (FOUND 2) |
| `:95`-`:102` `undo-owed`: recorded time, ties by folder name, the host as typed, a list with no entry line unreadable | unchanged order code (`LabFiles.cs:178`); empty, header-only, a byte order mark, blank lines | yes (P1); ties and the clock as gate B2016 measured |
| `:104`-`:107` "says `nothing is owed` only when it read at least one list, every list holds an entry line, every line was read"; `no undo list was read`, exit 11 | 30 shapes | yes as written; a folder it cannot open is not a "list" (FOUND 3) |
| `:108`-`:109` a folder that holds `undo-list.tsv` itself is refused before anything is read (exit 2) | given directly; through a link; holding a FOLDER of that name (not refused, and rightly) | yes (P1; mutant `mRunFolderGivenRead`) |
| `:110`-`:111` exit codes 0, 11, 2 | an unlistable session folder throws | yes but for that (FOUND 3) |
| `:144`-`:151` Limits: the clock; the owed line's host and id; the host as typed; .NET's re-send UNMEASURED | text only | read; consistent with the code; nothing on non-element content (FOUND 1) |

The kit's H1-H20 table, attacked: H1 to H5 hold and widen (30 shapes); H6 MEASURED as DERIVED (exit 11); H7, H8 hold; H9
MEASURED: a record beside the result is not read and the register is sent (FOUND 1); H10, H11 hold for every code unit;
H12 MEASURED (FOUND 2); H13 holds, and the undo runs as printed; H14 MEASURED (every default; two pins); H15 to H19 are
README text, read. One shape outside the table: a run folder that cannot be opened (FOUND 3).

## MERGE AND MAIN MOVES

- Main at the gate: `b0b26b60` (gh at 09:36 and at the last read, 09:51). compare main...28b25332: ahead 1, behind 0,
  five files with the kit's numstat; open pull requests 0; code scanning at b0b26b60 csharp, python, actions results 0,
  open alerts 0. The squash's tree on this main is the head's tree `ec57df8b` (657 files): measured above (2112 / 0 /
  2108 / 4, RULES 657).
- Nothing else is in flight for the repository (no open pull request, no branch newer than this one; the records seat
  of kit B2022 lands through no repository path). If main moves: landing.txt MAIN MOVES (B), not measured here.

## SCANS

- `words.py --control`: `CONTROL FIRED: 13 of 13`. `words.py` over the 297 added lines (`checks_w2r2.py`'s `added.txt`) and
  the head's own message (423 bytes, cat-file): `WORDS: clean (2 files)`; over `squash-subject.txt` (with #45),
  `squash-body.txt` and `pr-title.txt`: `WORDS: clean (3 files)`. `B2[0-9]{3}` lines: 0 and 0 (control: the kit 36).
- gitleaks 8.30.1: control FIRST (a token built by a program from two halves and 36 random characters, never printed,
  scanned alone): rc 1, `leaks found: 1`, the token not in the output; moved to `g2026/_quarantine/gl-control-*`. Then
  the added lines, the head's message, both patches, the five head blobs and the four landing texts under neutral names
  `1.txt` to `13.txt` in a NEW folder: rc 0, `no leaks found`.
- `build/squash_scan.py squash-subject(#45) squash-body.txt --scanner gitleaks` from the clone (build/ equal to main's:
  not in the diff): control rc 1 found 2; message rc 0 found 0; `SQUASH-SCAN: clean`.

## DISCLOSURE

- Two hook refusals at the very start, before any measurement: `pretooluse_no_cd.sh` refused a first listing that began
  with `cd`; `pretooluse_zsh_wordsplit.sh` refused its re-issue for an unquoted `======` separator. Both were the same
  read-only listing of the round 1 folder, re-issued in the allowed form (absolute paths, a `----` separator): the
  hooks' own stated fix, not another route to a refused end. `pretooluse_grep_case.sh` printed three advisories (not
  refusals) on greps whose results this verdict does not rest on. Those first calls also chained more than one command; from
  the clone on, every call is one command or one `python3 -I` program of my scratch.
- The Write tool turned eleven `\u` escapes of the probe file into the characters themselves (53 non-ASCII bytes; the
  drafter's own report names the same). Probe run 1 (71 cases) was built from that file; I rewrote the characters as
  escapes by program (`nonascii.py`: 0 non-ASCII bytes), added three host rows by program and ran the probe again whole
  (run 2, 74 cases): every line of run 1 is equal in run 2; this verdict quotes run 2. Run 1's results are in
  `g2026/_quarantine/`.
- Two heavy sequences overlapped in time (the mutants in the background, the probe in the foreground); each job took
  the one lock by itself, so no two jobs ran together. The probe built with `-p:TreatWarningsAsErrors=false` (2
  warnings, in the probe file) in worktree `prb` only; the probe file was never in `clone`, `pat` or `red`. The worktree
  index of `pat` was staged (`add -A`) to read its tree; no commit, no ref, nothing pushed (push URL
  `invalid://no-push`). The probe's permission rows set mode 000 on files and folders of the test's own temporary folder
  and restored them.
- The squash body's last line is the head commit's own attribution line, copied: the code is the seat's, and this gate
  wrote none of it.
- Not run: CodeQL locally; any Windows or Linux leg locally (the head's push run is the only cross-platform proof; the
  permission and symbolic-link rows of the probe are macOS only); `run_step.py`'s neutral scan (the hosted secret-scan
  job's proof lines read instead); the lab tool as a process; any device.
