GATE B2112: GO WITH FINDINGS @ 8ce4a86 on main 8757daa

Gate G1, ROUND 1 OF 2 of lane OX-A (the OXPd 1.x client readers: owed 133, 143, 146, 126, 134 client half, 93, 85, 94
client half), one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2109 (seat X77; stamp S4: Q1 "a"
one kit for all eight, Q2 "a" the seat writes the code to the kit's specification, each in words; Q3 to Q10 the
defaults; S8 the canonical heavy runner 31adedc8; every choice the coordinator's, none the product owner's). Head
`8ce4a86cd43ca13556b33a55bce964daf7c4a547` on `b2109/lane-a-oxpd1-readers`, ONE commit, one parent = main
`8757daa6c48d1f6764460d378ce3c15863b383df` (PR 53). Main and the branch did NOT move during the gate (gh api -X GET
09:02:54 and 09:35:41 AEDT; open pull requests 0 both times; open code-scanning alerts 0). Read and measured 2026-11-26
09:02 to 09:39 AEDT in my scratch `fleet/state/s329/g2112/`: `clone` (clone.py draft: push URL `invalid://no-push`, no
identity; detached at the head; the mutants ran here), worktrees `red` (BASE plus the head's five test files) and
`probe` (the head plus one probe file of mine, `GateProbeTests.cs` in the adapter's tests, never committed, never
pushed). Every heavy job through the kit's `heavy.py` (sha256 31adedc8..., my copy 8 of 8 equal to THE TOOLS) and the
wave lock, one at a time (lock waits 0 each, load-gated; load1 reached 19.6 from other seats); the 37 released lock
folders are mine, in `g2112/_quarantine/locks/`; no other holder's lock or file touched; the lock absent at 09:38.

**AT THE HEAD (where a record or agent disagrees with what Tuesday stamped):**
1. **The kit's first-named form of mutant `mCallbackLoose` ("the answer taken whatever `ReadTextAnswer`'s outcome")
   cannot fail: it is an equivalent mutant.** MEASURED by my extra mutant `xCallbackFirstForm` (`return result?.Value;`):
   `Total 133 Failed 0 | red NONE`. The seat's DEVIATION 1 (the kit's alternative form) was right and is the only form
   that proves anything.
2. **The kit's P1, and the README sentence it asked for, are wider than the code** (FOUND 1): text at the SOAP envelope
   level is read past by every reader.
3. **Owed item 94's lab half is not missing.** The kit and the commission keep "94's lab half as item 106"; the owed
   list says 94 stays open "until both land", and the lab's read of the sign-in agent records before a register is
   already at BASE (`ReadBeforeRegisterAsync`, `Oxpd1Command.cs:925`/`:1009`); 106 is that read's looseness. With this
   squash both halves of 94 exist (FOR-RECORDS.md: the records seat decides).
4. The kit's H10 "UNMEASURED" is now MEASURED (the seat's mNoTab line and my probe): `Oxpd1Soap.Parse` KEEPS a
   white-space-only text node (2 of 2), `XDocument.Parse` without `PreserveWhitespace` drops it (0 of 2).

**BLUF.** The head does what its eight items ask, on every path I could build. **No reader of the four takes a character
other than XML's four beside the result, beside the store's entries or beside the button records** (twelve characters,
U+00A0, U+2028, U+3000, U+FEFF, U+0085, U+2003, U+200B among them, raw bytes too: every one `MalformedAnswer`, the
callback null); **the five `IsServiceEnabled` shapes of 126 and every other text, CDATA or attribute I put on the
response end `MalformedAnswer`**; **`CallbackMessage` and `ReadTextAnswer` cannot differ** (761 bodies, DIFFER 0, also
against the sync echo's reader on the same-shaped body); **no address holding a literal `@` passes either record** (nine
forms, three positions); **no landed cell changed** (removed lines under `tests/` 0). Red first exactly the 23 rows
(`Total: 133, Errors: 0, Failed: 23`, each by assertion, my run); green `Total: 133, Failed: 0` and the whole solution
`total: 2367`, `failed: 0`, `succeeded: 2363`, `skipped: 4` (my run); `MUTANTS: 9 of 9 MATCH, 9 of 9 undone equal` (my
run of the seat's rows file through the frozen tool, each red on at least its cells and nothing outside); `HOSTED
8ce4a86c...: PASS` (my read; control FAIL 4). **Two Minor findings (the envelope level; an unpinned CDATA arm), five
Info. None blocks the landing.** Tuesday's points: (a) Q6's stricter rule: **Info**, no real address of ours needs an
`@`; (b) DEVIATION 2: no non-TextOnly row's answer changes, cost negligible, the two mutants independent; (c)
DEVIATION 1: the alternative form proves P3 together with `mEchoNet` and `mNetWhiteSpace`; the first form proves nothing.

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (text at the SOAP envelope level is read past by every OXPd 1.x reader; the README's new
   four-characters sentence is wider than the code).** `ReadAnswer` (`Oxpd1Soap.cs:147`, `:153`), `ReadTextAnswer`
   (`:244`, `:245`), `ReadEmptyAnswer` (`:208`, `:209`), `ReadStore` (`Oxpd1Writer.cs:634`, `:635`) and `ReadButtons`
   (`:712`, `:713`) take `root.Elements(s + "Body")` and `bodies[0].Elements()` only. MEASURED (`logs/probe-ws.tsv`,
   through `Oxpd1Soap.Parse`, the client's own parse, `Oxpd1Client.cs:225`): every one of the fifteen texts (XML's four
   characters, the twelve others, a comment, a processing instruction) in the `Body` before the response, or in the `Envelope` before the
   `Body`, is `Answered` in all five readers (the callback: `m1`). Harm: none to an answer (the response element is
   still read whole and nothing at that level can change which element is read). Pre-existing (the same code at BASE),
   not introduced; but the README's new sentence (README `:146` to `:149`: "Where a reader allows white space beside an
   element ... a no-break space or any other character there is text, and the answer ends `MalformedAnswer`") and the
   kit's P1 claim more. SOAP 1.2 allows only white-space character children there (SOAP 1.2 Part 1; DERIVED: no envelope
   schema is committed under `contracts/`, so not measured by schema). Fix when next touched: one shared envelope-level
   test with `IsXmlWhiteSpace`, a row per reader, or narrow the sentence to the response and result levels.
2. **Minor, does NOT block (the CDATA arm of the new `TextOnly` text test is pinned by no cell).** My extra mutant
   `xTextOnlyNoCData` (`responseText` without `t is XCData ||`, `Oxpd1Soap.cs:184`): `Total 133 Failed 0 | red NONE`
   (`logs/mutants-extra.out`): T08's CDATA row holds `synthetic`, which the white-space arm also refuses. The code is
   right (a CDATA of only white space beside `enabled`: `MalformedAnswer`, `logs/probe-shapes.tsv`). The landed
   `ReadTextAnswer` and `OnlyElements` carry the same arm; A05/V06/B06 hold no white-space-only CDATA row either (not
   mutated by me). Fix: one T08 row "CDATA holding only white space" in a later round.
3. **Info (`IsServiceEnabled`'s VALUE is not checked by the client).** MEASURED (`logs/probe-ise.tsv`): `maybe`, `TRUE`,
   a no-break space before or after `false`, U+3000 before `true`: each `Answered` with the text as written, each one
   schema error against HP's `xs:boolean` (`test.xsd:928` to `:934`); `XmlConvert.ToBoolean`, which the lab's switch
   calls (`Oxpd1Command.cs` `ReadBeforeEnableAsync`), throws on each, so the lab writes nothing (exit `ReadFailed`;
   DERIVED for the lab path); `oxpd1 read` prints the raw text. ` true `, `1`, `0`, CDATA and a split comment read as
   HP's schema does. The seat named it (H14 (4)). The README's "read only in HP's shape" is about the shape, not the value.
4. **Info (text inside a button record beside its `id` is read past).** MEASURED (`probe-ws.tsv`, `in-record-before-id`):
   all fifteen texts `Answered listed 1`. Gate B2103 FOUND 3's class; by the README's design ("a record's other parts are
   the device's and are not read"); the seat named it (H14 (1)).
5. **Info (the readers refuse shapes HP's schema takes: the safe side).** MEASURED (`probe-shapes.tsv`, `probe-ws.tsv`):
   a CDATA section holding only white space (or empty) beside an element; `xsi:schemaLocation` or `xml:lang` on a response
   element: `MalformedAnswer` (the callback null) in all five readers, schema errors 0 for the Test service's three
   answers. A device that writes one would stop the read; carry into the device kits.
6. **Info (Tuesday's point a: Q6 refuses an `@` where HP's `LimitedUri` takes it).** MEASURED (`logs/probe-at.tsv`; HP's
   pattern of `common.xsd:440` applied to `AbsoluteUri`, anchored): `https://h/?q=a@b`, `https://h/#a@b`, `https://h/a@b`,
   `https://h:443/@x` and `https://h/%61@b` (normalised to `a@b`) are refused by the agent service, the prompt page and
   the button target while HP's pattern takes them; `https://@h/...` and `https://a%40b@h/` refused (HP's pattern refuses
   both too); `https://h/a%40b`, `%2540`, `?q=a%40b` and the look-alikes U+FF20 and U+FE6B (sent percent-encoded) are
   TAKEN and HP's pattern takes them. Reach of the strictness TODAY: none. MEASURED by `grep`: the records are built at
   two places only, both in the lab (`Oxpd1Command.cs:655` the button, `:727` the agent), from command-line text the
   lab's own `Address` already refuses when it holds any `@` (`Oxpd1Command.cs:770`, the test at `:771`); no server code builds one. An
   address of ours with an `@` after the first `/` would come only from a query value or path segment carrying an e-mail
   address in a device-wide record, which no design names; `%40` serves it if one ever does. Not a defect: a stated,
   README-named choice (README `:92` to `:94`).
7. **Info (kit and record notes).** (a) Equivalent mutant: point 1 at the head. (b) H10 MEASURED: point 4 at the head.
   (c) The `ReadStore` and `ReadButtons` doc comments (`Oxpd1Writer.cs`, above `:628` and `:706`) still say "white-space
   text"; the white space they name is now XML's through `OnlyElements` (the seat's H14 (3)). (d) `ContractTests.Validate`
   (`ContractTests.cs:164`) loads with `XDocument.Parse` and no `PreserveWhitespace`, so a white-space-only value reads as
   empty there (my probe: a message of one space counted one schema error, an artefact; no landed or new cell depends on
   it). (e) The squash body is a new text for the landing (the commit's body is the attribution line only).

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole:** `diff --name-status` ten rows, all `M`; numstat 4/2, 9/10, 17/5, 22/14, 33/22, 25/0,
  33/0, 32/0, 37/0, 15/0, equal to `compare`'s file list (GET 09:02); ONE commit (`rev-list --count` 1), parent 8757daa6,
  author and committer the repo's `@datasec.com.au` address (masked); `ls-files` 679; the commit's message equals the
  frozen `commit-message.txt` byte for byte (374 bytes, subject 316). Every changed `src/` line read (four `.cs` files and
  the README) and the five test files' added lines read whole. The seat's second-pass mutant run applied to the
  committed bytes (its `applied:` sha256s 818a34a8 `Oxpd1Soap.cs`, 84935a98 `Oxpd1Writer.cs`, a983d4bf `Oxpd1Echo.cs`
  equal the head's blobs).
- **Red first** (`g2112/red` = BASE + the head's five test files, `git diff --quiet 8757daa6 -- src` rc 0;
  `logs/r-exe-adapter.log`): restore rc 0; build `0 Warning(s)`, `0 Error(s)`; adapter `Total: 133, Errors: 0, Failed:
  23`; `[FAIL]` 23, all in the seven new cells (A04 2, A05 9, T08 6, V06 2, B06 2, B07 1, W10 1), 23 of 23 followed
  within five lines by an `Assert.<name>() Failure` line; the six green rows and every landed cell passed. Equal to the
  kit's PREDICTED red and to the seat's run. (B07 and W10 are Facts: on BASE their first `Assert.Throws` fails, so the
  path-`@` assertion is not seen red there; my mutants `xAgentAtAuthorityOnly` and `xButtonAtAuthorityOnly`, which
  refuse an `@` in the authority only, redden W10 and B07 alone: the path rows are pinned.)
- **Head green** (`logs/h-*.log`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; adapter `Total: 133, Errors:
  0, Failed: 0`; whole solution `total: 2367`, `failed: 0`, `succeeded: 2363`, `skipped: 4`. Probe tree: adapter
  `Total: 138, Failed: 0` (133 + my five probes), Lab `Total: 297, Failed: 0`.
- **Mutants** (`logs/mutants-seat.out`; the seat's `mutants.json`, sha256 aadf791d... equal to its STATUS; every OLD once
  in the head's files; my run of the frozen `mutants_a1.py`, 09:12 to 09:28, load-gated): `MUTANTS: 9 of 9 MATCH, 9 of 9
  undone equal`, every row's Total and red set equal to the seat's second pass. By ROW: `mNetWhiteSpace` the eight
  no-break-space rows (A04 2, A05 1, T08 1, V06 2, B06 2); `mNoTab` the five XML-white-space control rows (A04 row 3, A05
  row 2, T08 row 7, V06 row 3, B06 row 3); `mEchoNet` A04 rows 1 and 2, A05 row 6; `mOnlyElementsNet` V06 rows 1 and 2,
  B06 rows 1 and 2; `mTextOnlyNoText` T08 rows 1, 2, 3, 6; `mTextOnlyNoAttribute` T08 rows 4, 5; `mCallbackLoose` A05 3 to 11; `mAgentAt` W10; `mButtonAt` B07. Nothing red
  outside the seven new cells; the clone's status 0 lines after and HEAD still 8ce4a86c. My four extra mutants
  (`logs/mutants-extra.out`): `xCallbackFirstForm` red NONE (equivalent: head point 1); `xAgentAtAuthorityOnly` W10;
  `xButtonAtAuthorityOnly` B07; `xTextOnlyNoCData` red NONE (FOUND 2).
- **Whether ANY reader of the four still takes a character other than XML's four beside an element:** beside the
  response's result, the store's entries and the button records: NO (twelve characters x five readers x every position,
  `probe-ws.tsv`; a no-break space INSIDE a store entry's base64 also ends `MalformedAnswer`). At the envelope level:
  YES, any character (FOUND 1). Inside a button record beside its `id`: YES, by design (FOUND 4).
- **Whether ANY `IsServiceEnabled` shape HP's schema refuses is still read:** of the response's own shape, none I could
  build: text before or after `enabled`, CDATA, an attribute, `xsi:nil`, `xml:lang`, `xsi:schemaLocation` (the last two
  schema-valid: FOUND 5), and the twelve non-XML texts beside `enabled` each `MalformedAnswer` (T08 and `probe-ws.tsv`,
  `probe-shapes.tsv`). Still read: a value outside `xs:boolean` (FOUND 3) and text at the envelope level (FOUND 1).
- **Whether `CallbackMessage` and `ReadTextAnswer` can now differ on any body:** NO. By construction
  (`Oxpd1Echo.cs:224`: `Parse`, then `ReadTextAnswer`, then the result's `Value` only when `Answered`); MEASURED over 761
  bodies (`logs/probe-callback.tsv`: fourteen texts beside the message x six attributes on the element x nine message
  values, plus a fault, two bodies, a SOAP 1.1 envelope, a message of no namespace and a DTD): the callback, a direct
  `ReadTextAnswer` and the sync echo's reader on the same-shaped body agree on every one, `DIFFER 0`, 49 answered. The one
  designed difference: a fault body is `Fault` to the echo and null to the callback.
- **Whether ANY address with `@` passes either record:** NO literal `@` passes (FOUND 6: nine forms refused in the agent
  service, the prompt page and the button target). Taken: `%40` forms and look-alike characters, which hold no `@`.
  `https://lab-host.example\@evil.example/` throws `UriFormatException` at `new Uri` before either record.
- **Whether ANY landed cell changed:** NO. `checks_a1.py` on the head's index (`git diff --cached 8757daa6`) `CHECKS: 8 of
  8 PASS` (check 4: removed lines under `tests/` 0, control added 142); the five test files gain lines only.
- **The README sentences against the code** (head): the "Known, not changed here: five `IsServiceEnabled` answers" bullet
  is gone (check 8: 0, BASE 1); the four characters are named (README `:146` to `:149`; `Oxpd1Soap.cs:41`), wider than
  the code at the envelope level (FOUND 1); the `@` clause (README `:75` the agent, `:92` to `:94` the target, `%40` not
  mentioned; `Oxpd1Writer.cs:188`, `:291`); the item-94 bullet (README `:183` to `:187`, "from HP's text; UNMEASURED on
  a device", true to the code: `Undo` unchanged); `IsServiceEnabled` (README `:55` to `:59`, `Oxpd1Soap.cs:183` to
  `:185`); the store and buttons "nothing beside it but XML white space" (`OnlyElements`); the callback sentence (README
  `:118` to `:121`, `Oxpd1Echo.cs:215` to `:226`, `test.xsd:578`); the `Timeout` summary (`Oxpd1ClientOptions.cs:86` to
  `:89`) equal in sense to the README's Typed ends.
- **Whether the Lab's cells over `CallbackMessage` and `IsServiceEnabled` stay green:** yes. Locally: the whole solution
  green, and the Lab executable whole `Total: 297, Failed: 0` in the probe tree (`Oxpd1EchoTests` E02, E03, E08 read the
  callback; `Oxpd1TestServiceTests` reads `IsServiceEnabled`). Hosted: `Datasec.Suite.Lab.Tests.dll ... passed` on linux
  and windows (`logs/hosted/job-*.log`). No Lab file changed (`diff --quiet -- src/Datasec.Suite.Lab` rc 0).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, 09:09): run 45708576106, four jobs
  attempt 1 success, linux `total: 2367` twice, `succeeded: 2363`, windows `succeeded: 2346`, `skipped: 21`, `RULES:
  clean (679 files)`, `UNIT-TEST FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15 files)`, `failed Datasec.`
  lines 0 and 0 (colour codes stripped; control: 4 `Oxpd1.Tests.dll` and 4 `Lab.Tests.dll` lines per leg); check runs
  beside the four: 0; last line `HOSTED 8ce4a86cd43ca13556b33a55bce964daf7c4a547: PASS`; the control at `--total 2368`
  printed `FAIL 4`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. TUESDAY'S OWN POINTS

- **(a) Q6, any `@` in `AbsoluteUri`:** Info (FOUND 6). No address our code registers can hold an `@` today (two builders,
  both in the lab, behind a rule that refuses every `@`); a future server-built address that needs one (an e-mail in a
  query value or a path segment of a device-wide record) has `%40`, which both records and HP's pattern take. Does NOT
  block.
- **(b) DEVIATION 2, the two named locals computed for every row:** no non-TextOnly row's answer changes: both locals are
  read only inside `row.TextOnly && (...)` (`Oxpd1Soap.cs:185`, short-circuit), and computing them cannot throw
  (`Attributes()`, `Nodes()`, `IsXmlWhiteSpace` over a string); MEASURED: every landed read cell green (whole solution
  2367 / 0). Cost: one pass over the response element's own attributes and its DIRECT child nodes (not descendants),
  each `Any` short-circuiting, linear and far below the parse and the mask already done on the same document under
  `MaxAnswerBytes`; negligible. The mutants still prove each test independently: `mTextOnlyNoText` reddens exactly T08
  rows 1, 2, 3, 6 and `mTextOnlyNoAttribute` exactly rows 4, 5 (disjoint, together the six red rows); the CDATA arm alone
  is not pinned (FOUND 2).
- **(c) DEVIATION 1, the alternative form of `mCallbackLoose`:** the alternative (`message` read by name, anywhere, with
  nothing else checked) reddens all nine strict rows of A05 (3 to 11), so A05 proves the callback is read strictly; that
  it is read by EXACTLY the sync rules is proved by the code (`Oxpd1Echo.cs:224` calls `ReadTextAnswer`) together with
  `mEchoNet` and `mNetWhiteSpace` (a change inside `ReadTextAnswer` reddens A05's no-break-space row) and my 761-body
  equality. P3 holds. The kit's first form is an equivalent mutant (head point 1); the seat's choice was the right one.

## 3. ADVERSARIAL BEYOND THE KIT (the commission's six shapes, then three outside each property)

- **Other Unicode white space beside each reader** (U+2028, U+3000, U+FEFF, U+0085, plus U+00A0, U+2003, U+200B, as
  references and as raw bytes): `MalformedAnswer` in the sync echo, `IsServiceEnabled`, the CA store and the button
  records, null in the callback, before and after the result and beside entries and records (`probe-ws.tsv`, schema
  errors 1 each for the Test service's answers). At the envelope level: read (FOUND 1).
- **A white-space-only text node dropped or kept on each host:** KEPT by `Oxpd1Soap.Parse` on macOS arm64 (2 of 2,
  `probe-shapes.tsv`; and `mNoTab` reddens the stub-fed control rows, so the stub path keeps them); on linux and windows
  UNMEASURED directly, but the parse is the same .NET code and every white-space control row is green on both hosted legs,
  and the rows hold either way (the kit's H10).
- **CDATA holding only white space** beside the result, `enabled`, the message, the entries or the records:
  `MalformedAnswer` (null) in all five readers, schema-valid as .NET validates (FOUND 5); the new `TextOnly` arm that
  refuses it is not pinned (FOUND 2).
- **An `xmlns` default-namespace declaration on the response element:** accepted in all five readers (`Answered`, the
  callback `m1`); an extra `xmlns:z` declaration likewise (`probe-shapes.tsv`).
- **An `@` encoded as `%40` in each address:** TAKEN in the agent service, the prompt page and the button target, sent as
  `%40` (`AbsoluteUri` keeps it encoded), HP's pattern takes it (FOUND 6).
- **An empty `message` on the sync echo, compared with the callback:** the sync echo `MalformedAnswer`, the callback null:
  the same rule (`ReadTextAnswer`'s non-empty text). A message of one space: `Answered` " " by both; a no-break space:
  `Answered` by both (`probe-ise.tsv`).
- **Three shapes outside each property** (the kit's P1 to P5):
  P1 (only XML white space beside an element in the four readers): text in the `Body` beside the response (FOUND 1), text
  in the `Envelope` beside the `Body` (FOUND 1), text inside a button record beside its `id` (FOUND 4); a no-break space
  inside a store entry's base64: covered (`MalformedAnswer`).
  P2 (`IsServiceEnabled` answered only with no attribute but namespace declarations and no text but XML white space): a
  non-boolean value (FOUND 3), `xsi:schemaLocation` on the response (refused though schema-valid: FOUND 5), a SOAP
  `Header` beside the `Body` (read, schema-valid): covered or named.
  P3 (the callback read by exactly the sync rules; an empty message null): a fault body (null; `Fault` to the echo), a
  message split by a comment (`m1` to both), a SOAP 1.1 envelope (null to both): covered (761 bodies, DIFFER 0).
  P4 (neither record takes an address holding `@`): `%40` (taken, no `@`), U+FF20 (taken, sent `%EF%BC%A0`), a backslash
  before `@` (`UriFormatException` at `new Uri`): covered or named (FOUND 6).
  P5 (no landed cell changes; every landed cell green): removed lines under `tests/` 0; the Lab executable whole 297 / 0;
  the whole solution 2367 / 0 locally and on both legs: covered.

## 4. SCANS

- **gitleaks 8.30.1:** control FIRST, a token built in-process from two halves and 36 random characters, never printed,
  outside the clone: rc 1, `leaks found: 1`, moved to `g2112/_quarantine/gl-control-*`; then `gitleaks git` over
  `8757daa6..8ce4a86c` rc 0 (`1 commits scanned`, `no leaks found`); the ten head blobs, the commit's message, the seat's
  `mutants.json` and the whole diff as `1.txt` to `13.txt` in a new folder: rc 0, `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 227 added lines of `BASE..head`
  (`scratch/checks/added.txt`, made by `checks_a1.py`; 227 equals the commit's `227 insertions`) and the head's commit message:
  every class 0, `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0 (control: the kit counts 21 lines).
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#54`, `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 1 and `coordinator` 2 (the "Who decides" section), 4 bytes
  outside ASCII (the attribution line's emoji), every other class 0; `B[12][0-9]{3}` and `X7[0-9]` 0 in all four;
  `build/squash_scan.py` (the head's, equal to BASE's: `build/**` and `.github/**` not in the diff, `diff --quiet` rc 0)
  with `#54`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`; gitleaks over this folder's seven files and the
  `#54` subject under neutral names, the control re-planted first (rc 1, `leaks found: 1`, quarantined): rc 0, `no leaks
  found` (09:40).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). The chain's publish and release guard, `repo_rules.py`, the unit tests
of `build/tests` and `run_step.py`'s neutral scan (RELAYED from the seat; equal on the hosted legs, my read: `RULES:
clean (679 files)`, `Ran 117 tests`, GUARD 14 and 15, the hosted neutral scan). The whole solution after the mutants (the
clone's status is 0 lines after the tool's undo and HEAD is 8ce4a86c, so the measured head is the bytes that ran). The
lab's switch and `oxpd1 read` on a non-boolean `enabled` (DERIVED from `ReadBeforeEnableAsync`). A white-space-only text
node on linux and windows directly. Any device.

## OUTSIDE THE FENCES

None. Writes: this folder and `fleet/state/s329/g2112/` only (my clone, its two worktrees, logs, scratch, quarantine).
No pull request, no push (the clone's push URL is `invalid://no-push`), no re-run of a hosted job, no `cd`, nothing
deleted, no printer or device, no Azure, nothing to any person, no Jira. Every gh call a GET under the project's
GH_CONFIG_DIR. Reads of the project folder: the seat's STATUS, `CLAUDE.md` lines 7 and 82, `BACKLOG.md` items 85, 94,
126 and the item headers, the seat's `mutants.json` and its second mutant log (copied into my scratch by `cat`); nothing
of the project's was written but what `heavy.py` does under the wave lock (the lock folder, moved to my quarantine after
each job). Two hook refusals, each a STOP for that action and re-issued in an allowed form: a `git checkout` with an
unexpanded variable in the path, and a `cp` whose source was in the project folder (re-issued as `cat` into my
scratch). No print of `kam_rulings_today.sh` or `kam_msgs.sh` was made or saved. No background process of mine is left
running; the wave lock is absent.
