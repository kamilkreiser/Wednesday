GATE B2070: GO WITH FINDINGS @ de8f2a4 on main 217286f

Gate G1 (the client gains a send under a second credential, `guest`, and the lab gains an inbound listener), ROUND 1 OF
2 of the echo lane, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2067 (seat X71; stamp S4:
Q1 "a" a plain HTTP/1.1 listener in the lab on 127.0.0.1, Q2 "a" guest only, ADMIN in the option exit 2 and in any
name of the file exit 12, each in words; Q3 to Q10 the defaults; every one the coordinator's, none the product owner's)
and its ANSWER-1 (one re-run of the chain's test). Head `de8f2a47df41e1b56218c6cb0c7a280cc5ea9ffe` on
`b2067/oxpd1-echo`, ONE commit, one parent = main `217286f321b1b5240856ffb15540f069775e9065` (PR 50). Main and the
branch did NOT move during the gate (gh api -X GET 01:15 and 01:38; open pull requests 0 both times). Read and measured
2026-11-25 01:15 to 01:40 AEDT in my scratch `fleet/state/s325/g2070/`: `clone` (clone.py draft: push URL
`invalid://no-push`, no identity; detached at the head), worktrees `red` (BASE + `1-red.diff`) and `probe` (the head +
two probe files of mine, never committed, never pushed). Every heavy job through the kit's `heavy.py` (sha256
31adedc8...) and the wave lock, one at a time, lock waits 0 each; the 49 released lock folders are mine, in
`g2070/_quarantine/locks/`; no other holder's lock or file touched; the lock absent at 01:38.

**BLUF.** The lane does what its G1 questions ask on every path I could build: **no path of `oxpd1 echo` sent `admin`**
(21 end-to-end runs against the stub, sync, async, 401, fault, refused files: admin-sent 0 in each), **no value was read
from a file in which a name (text before the first `=`) holds ADMIN** (exit 12, no folder, 0 connections, with leading
spaces, `export`, a `#` line, CR-only line ends and UTF-16 with a BOM), **the guest value reached no output, summary or
client log** (0 in every run, the bare value and its Basic form), **the callback passes only for a POST to the exact
path** (case, query, trailing slash, percent-encoding, absolute form, dot segment, `//`, fragment, another method: all
404), and **the listener is never held past its wait** (every bound case ended within 3 ms of its wait or its 5 s
read bound). The head is BASE plus the two frozen patches byte for byte; red first exactly the 23 cases by
`Assert.Equal()`; `total: 2261`, `failed: 0`; `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal` (my run of the frozen
tool), each red on exactly its cases; `CHECKS: 10 of 10 PASS`; `HOSTED de8f2a47...: PASS` (my read). Five narrower
defects, MEASURED, none reaching a device or a secret: the sync reader takes a no-break space beside the result (FOUND 1),
the callback reader passes five schema-refused bodies and two README sentences over-claim it (FOUND 2), a long
`--callback-host` crashes the run after its folder is made (FOUND 3), a delay longer than the wait or the time-out ends
with words that blame the path (FOUND 4), and the listener's one-at-a-time reading and the wildcard bind are unnamed
(FOUND 5, Info). **None blocks the landing.** The landed `Server.Tests` hang did not recur in six runs (Section 2).

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (the sync reader takes non-ASCII white space beside the result; HP's schema refuses it).**
   `Oxpd1Soap.cs:252` `!string.IsNullOrWhiteSpace(t.Value)` uses .NET's white space (U+00A0, U+2000 to U+200A, U+3000,
   U+0085, U+2028 ...), not XML's four characters. MEASURED (`logs/probe-adapter.tsv` S34, through the real
   `Oxpd1Soap.Parse` and `Oxpd1Echo.Read`): `<SyncEchoStringResponse>&#xA0;<SyncEchoStringResult>m1</...>` reads
   `Answered` `m1`; HP's committed schema (`ContractTests.Schemas()`) errors 1 on that element. Through the verb it would
   then print exit 0 (DERIVED: `JudgeGuest` reads with the same reader; the verb compares only the result's text). The
   adapter README (`:70`-`:71` "nothing beside it but white-space text") is literally true in .NET's sense, false in
   XML's. Harm: none beyond a false "answered" on a device that sends a no-break space; the echo writes nothing. Fix
   when next touched: test `t.Value.All(c => c is ' ' or '\t' or '\r' or '\n')`. All the commission's named shapes are
   handled (S01 to S33): a processing instruction (S02, S05), a comment (S03, S04) and a character reference (S06) are
   read and are schema-VALID (the parser drops PIs and comments, `Oxpd1Soap.cs:98`-`:99`); `xsi:type` on the result
   (S07, S08) and `xsi:nil` (S09, S10) are refused; B2058's five FOUND 1 shapes refused (A02, red first and mutants).
2. **Minor, does NOT block (the callback reader passes bodies HP's schema refuses; two README sentences over-claim).**
   `Oxpd1Echo.cs:218`-`:226` counts only ELEMENTS of `AsyncEchoStringComplete` and reads `message`'s value; it does not
   look at text beside `message` or at any attribute. MEASURED (`probe-adapter.tsv` C02 to C05, C15, C23; schema errors
   1 each; and `probe-judge.tsv` through the listener's `Judge`: 200 `the callback`): text before or after `message`,
   an attribute on `message`, an attribute or `xsi:nil` on `AsyncEchoStringComplete`, `xsi:type="xs:int"` on
   `message`: each returns the message, so the run passes (exit 0). Over-claims: adapter `README.md:73`-`:74` "with the
   same strict parser: ONE `AsyncEchoStringComplete` holding ONE text-only `message`" (the PARSER is the same; the
   READING is not the sync reader's, which refuses exactly these shapes), and Lab `Commands/Oxpd1/README.md:170` "whose
   body is HP's `AsyncEchoStringComplete` holding the message". The kit's H11 lists only a child element, two messages,
   another element, a DTD and not-XML (each refused here: C06 to C09, C19, C26). Harm: a path test reads "the callback
   arrived" for a body that holds the message in a shape HP's schema refuses; the message still crossed the path, so the
   test's question is still answered; nothing is written. Q8's "strict" default holds for extra ELEMENTS (C19: null) but
   not for text or attributes. Fix: the same three rules as `ReadTextAnswer` on `Complete` and `message`, or one Limits
   sentence.
3. **Minor, does NOT block (a long `--callback-host` ends the run with an unhandled exception after the run folder is
   made).** `Oxpd1EchoVerb.cs:125`-`:133` accepts any `Uri.CheckHostName` DNS name (up to 255 characters); `:334` builds
   the callback URI and `:337` `Oxpd1EchoCall.Async` throws `ArgumentException` when it exceeds 256 characters
   (`Oxpd1Echo.cs:121`-`:124`); nothing catches it (`LabCommands.RunAsync`, `CommandRegistry.cs:39`-`:56`, has no
   catch). MEASURED (`probe-e2e.tsv`, a 232-character host): `THREW ArgumentException`, posts 0, the run folder made
   holding only `oxpd1-client.log`, no summary, no exit code of the README's list. Harm: none to a device (no request),
   no secret (the message is a fixed sentence); a run folder left without its summary. Fix: check the callback URI's
   length in the parser (exit 2) or build the call before the folder.
4. **Minor, does NOT block (a delay longer than the wait or the time-out is accepted and then blamed on the path).**
   `Oxpd1EchoVerb.cs:117`-`:124` (delay 0 to 60000), `:153`-`:161` (wait 1 to 300 s) and `:179`-`:186` (time-out 1 to
   120 s) are checked separately. MEASURED (`probe-bind.tsv`): `--delay-ms 60000 --callback-wait-seconds 1` (async) and
   `--delay-ms 60000 --timeout-seconds 1` (sync) both parse. DERIVED (HP: the device answers the async echo at once and
   calls back "after the delay"; the sync answer comes after it): the async run then ends exit 13 with "the path from
   the device to this listener did not carry it (a firewall, a route, an address the device cannot reach), or the device
   did not send it" (`:356`-`:357`), the sync run exit 8 "the echo did not answer". Not measurable on the stub (it calls
   back 50 ms after its answer and ignores the delay). Harm: a misleading diagnosis in the very run (the LAN path test)
   that is meant to diagnose the path. Fix: refuse a delay of at least the wait (async) or the time-out (sync) as a
   usage error, or say it in the exit-13 line.
5. **Info (the listener: one connection at a time; the wildcard bind; macOS reuse).** MEASURED (`probe-bounds.tsv`,
   `probe-bind.tsv`): the bounds hold (B2 to B4: an idle connection, a slow head, a short body each 400 after 5 s; the
   wait ends at 8001 to 8002 ms of 8 s; B8 to B10 chunked, a head over 16 KiB, a `Content-Length` of 65537: 400 at
   once; B5: 16 quick requests end the wait at 6 ms). But the listener reads ONE connection at a time
   (`Oxpd1EchoVerb.cs:448`-`:470`): one idle connection delays the real callback by 5 s (B6: 200 at 5003 ms); three idle
   connections and a 12 s wait lose it (B7: exit-13 path, three 400s listed, the callback never read); after 16 quick
   requests a 17th, even the real callback, is neither read nor listed (B5), and the exit-13 words say none "reached the
   listener". `--callback-bind 0.0.0.0` parses and listens on every interface (the README says "an IPv4 address"; the
   Limits say loopback "in every cell"); on macOS `Start(127.0.0.1, P)` succeeds while another program listens on
   `0.0.0.0:P` (kit H16 holds only for the same address: AddressAlreadyInUse). An address that is not local
   (`192.168.255.254`: AddressNotAvailable) or `255.255.255.255` (AddressFamilyNotSupported) ends exit 8 as H16 says.
   `Expect: 100-continue` with the body 2 s later passes (B12); HTTP/1.0 passes (B11). On loopback by default, a 128-bit
   path and a 64-bit message must both match: Info for this lane; the LAN run's kit should name it.
6. **Info (outside HP's element schema; the library's setting).** Envelope-level shapes are read as the landed readers
   read them (S13 text in `Body`, S27 text in `Envelope`, S16 an attribute on `Body`, S26 a SOAP element after `Body`,
   S21 an unknown `mustUnderstand` header; C10 text in `Body`): each HP-element-valid, outside the SOAP envelope's own
   rules; not this lane's to change alone. Refused although schema-valid (the safe side): white-space CDATA beside the
   result (S12), `xsi:type="xs:string"`, `xml:lang`, `xml:space` (S07, S18, S29), a `#` comment line holding ADMIN in
   the credentials file (F9, exit 12). The library: `SendGuestAsync` (`Oxpd1Client.cs:121`) reads the client's ONE
   setting name (`AdminPasswordSetting`), so a library caller that builds an `Oxpd1Echo` on a client set up for reads
   would send the ADMIN password under the user `guest` (to the same pinned device). The lab verb cannot (its client is
   built on the guest name only, `Oxpd1EchoVerb.cs:280`-`:287`, after exit 2 and exit 12). The adapter README says "the
   setting's name is the caller's choice": true, unnamed as a hazard. Credentials-file shapes consistent with "names
   only" (H17): a homoglyph `ADMIN` (fullwidth F7, Cyrillic F8), `ADMIN` in a value (F5), no `=` (F6), and a line joined
   by U+2028 (F11: .NET's `File.ReadLines` does not split there, so the text after it, `..._ADMIN_PASSWORD=x`, became
   part of the guest VALUE sent as the guest password; contrived, the same class as H17). The two file reads
   (`NameHolding`, then `Read`, `Oxpd1EchoVerb.cs:256` and `:264`) are separate: a file changed between them is not
   seen (not measured; operator-controlled).

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole** (`logs/tree_check.out`): `--name-status` twelve rows, 4 `A`, 8 `M`, numstat equal to
  THE CODE's (67/7, 263/0, 51/0, 24/4, 32/0, 15/3, 591/0, 53/4, 83/0, 1/1, 228/0, 86/4); ONE commit, parent 217286f3;
  each file's sha256 and line count at the head equal THE CODE's "After both" column (12 of 12); the commit message
  equals `commit-message.txt` (446 bytes, subject 388); `ls-tree` 671 at BASE, 675 at the head.
- **The two patches against THE TOOLS:** my copy and the seat's `.tools/b2067/gate` both 10 of 10 equal to THE TOOLS'
  sha256 (`1-red.diff` b71426d2..., `2-fix.diff` 3cb66d25...); temporary index `read-tree 217286f3`, `apply --cached`
  both rc 0, `write-tree` `2c27aa34` = `de8f2a47^{tree}` (EQUAL); red tree `c1f8fe2b`.
- **Red first** (`g2070/red`, `logs/red-check.out`): adapter `Total: 70, Errors: 0, Failed: 8`, Lab `Total: 254, Errors:
  0, Failed: 15`; the 23 `[FAIL]` cases equal THE CONTROLS' list (program compare: True, True; missing 0, extra 0);
  23 of 23 followed within five lines by `Assert.Equal() Failure`.
- **Head green** (`logs/h-test.log`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; `total: 2261`, `failed:
  0`, `succeeded: 2257`, `skipped: 4`; `Datasec.Suite.Server.Tests.dll ... passed (10s 410ms)`.
- **Mutants** (`logs/mutants.out`, `logs/mutant-cases.out`; my run of the frozen `mutants_e1.py`, sha256 327bd50a...):
  `MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal`; by CASE: `mGuestAsAdmin` E01, E02; `mAdminNameTaken` E04 rows 1-2;
  `mAdminFileTaken` E04 rows 3-4; `mOtherMessageTaken` E07 `another message`; `mTextBesideTaken` A02 `text before`,
  `text after`, `cdata beside`, E07 `text beside the result`; `mResponseAttributeTaken` A02 `an attribute on the
  response`, `nil on the response`, E07 `an attribute on the response`; `mResultShapeTaken` A02 `an attribute on the
  result`, `a child element`, E07 `a child element`; `mEmptyResultTaken` A02 and E07 `an empty result`;
  `mCallbackPathIgnored` E03 `other path`; `mCallbackMessageIgnored` E03 `other message`; `mNoCallbackPasses` E03 all
  four. Each is exactly the cases its edit can reach; no other class red; the clone's porcelain 0 lines after.
- **Any path of `oxpd1 echo` that sends `admin`:** none (`probe-e2e.tsv`: admin-sent 0 in 21 runs; source: the verb's one
  client call is `Oxpd1Echo.EchoAsync` (`:305`, `:339`), its one send `SendGuestAsync` with `GuestUser`; `checks_e1.py`
  check 10: `SendGuestAsync` 2 lines, `GuestUser` 2 lines). **A value from a file in which a name holds ADMIN, or under
  such a name:** none (F2, F3, F9, F10, F12 exit 12, posts 0, no folder; the `--password-name` rule `:100` plus
  `IsName`). FOUND 6 names the library hazard and the U+2028 line.
- **Any sync answer HP's schema refuses read as the message:** one shape, FOUND 1; the commission's PI, comment and
  character reference are schema-valid and read; `xsi:type` refused (S07, S08).
- **Any request but a POST to the run's path holding the message passing as the callback:** path shapes none
  (`probe-judge.tsv`); body shapes: the message in another namespace (C07) or unqualified (C06), a second envelope
  (C08), two `Complete` (C09), two `Body` (C16), SOAP 1.1 (C14): refused; FOUND 2's five schema-refused bodies pass.
- **The listener held past its bounds:** never (FOUND 5's MEASURED rows). **Bind anything but the given address:**
  no; the given address may be the wildcard (FOUND 5).
- **The guest value reaching the output, the summary or the client's log:** never (`probe-e2e.tsv` guest-in-output 0,
  guest-in-files 0 in every run, including a result equal to the guest value (A1), a result holding it (A2) and a fault
  code holding it (A3): the client's mask and scrub hold).
- **The README sentences against the code:** every changed or added sentence of both READMEs read against the head:
  the echo rows (`Oxpd1Echo.cs:198`, `Oxpd1Client.cs:118`, `:128`), the bounds (`Oxpd1Echo.cs:67`, `:72`, `:121`), the
  exit codes (`Oxpd1Command.cs:182`-`:215`, `Oxpd1EchoVerb.cs:246`-`:358`), the order (`:249`, `:256`, `:264`, `:272`),
  the listener's numbers (`:405`-`:411`), "Five verbs" (`Oxpd1Command.cs:255`), the Limits (no TLS, names not values,
  B2058's two residuals). Two over-claims (FOUND 2) and one literal-but-narrow sentence (FOUND 1).
- **The one landed literal and the stub's four landed lines, nothing else of a landed cell:** removed lines under
  `tests/`: exactly 5 (`LabCertTests.cs:93` 3 to 4; `Oxpd1Stub.cs` the constructor signature, the `app.Run` line, the
  `return new Oxpd1Stub(...)` line, the `AnswerPlanned` signature), `checks_e1.py` check 9 PASS; L03's other three
  rules hold over the new file (green).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, 01:22): run 45411074875, four jobs success,
  linux `succeeded: 2257`, windows `succeeded: 2240`, `RULES: clean (675 files)`, `UNIT-TEST FLOOR: ran 117, floor
  117`, `GUARD: clean (14 files)` / `(15 files)`, `failed Datasec.` lines 0 and 0 (control 4 and 4); check runs beside
  the four: 0; last line `HOSTED de8f2a47df41e1b56218c6cb0c7a280cc5ea9ffe: PASS`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. THE LANDED `Datasec.Suite.Server.Tests` HANG (against the LANDED suite, not this lane)

Not reproduced: my whole solution at the head (01:20) passed it in 10 s; five runs of its executable alone (01:33 to
01:34, `TIMEOUT=180`) each `Total: 15, Errors: 0, Failed: 0` in 3 to 4 s, `pgrep` empty after each (`logs/
server-runs.out`). The seat's evidence, read: `c-test.log` (17 of 18 assemblies `passed`; Server.Tests `Running tests
from` and no result), `hang-server-tests-sample.txt` (21 threads, 1575 samples each; top of stack `__psynch_cvwait`
18900, `kevent` 4725, `mach_msg2_trap` 3150, one each `__open_nocancel` / `__poll_nocancel` / `__read_nocancel` /
`__workq_kernreturn`: every thread waiting, none running; main thread in a managed wait; `Kestrel Timer`, `Console
logger queue processing thread`, `.NET File Watcher` present, so a host had been started), the lsof file empty (no inet
socket). **This lane's diff cannot reach that assembly:** `Datasec.Suite.Server.Tests.csproj` references
`src/Datasec.Suite.Server` only, which references Core, Adapters.Oxpd2 and Secrets; its bin folder holds no
`Datasec.Suite.Adapters.Oxpd1.dll` or `Datasec.Suite.Lab.dll`; none of those four projects is in the diff. A candidate
cause, not measured: `HostRig.cs:108` `await app.StartAsync()` and `:171` `await _app.StopAsync()` take no token, and
the project sets no per-cell bound. Recorded as an owed-item proposal in FOR-RECORDS.md, with the runner's orphaned
host (`heavy.py` ends `dotnet test`, not its child).

## 3. FRAME (stamp checklist item 11): each every/never/only sentence the change adds

- "never `admin`" (adapter README `:66`, `Oxpd1Echo` doc): sync (E01), async (E02), 401 (async 401 probe), a fault
  (A3), a refused file (F2 to F12): covered, 0 each. Shape outside: the library on an admin setting (FOUND 6, a finding).
- "no value of that file is read, so the admin password is never read by this verb" (Lab README `:153`-`:155`): leading
  spaces, `export`, CR-only, UTF-16: covered (exit 12). Outside: U+2028 (FOUND 6), homoglyphs (H17's stated limit),
  a change between the two reads (stated here, not measured).
- "read only in HP's shape (ONE text-only `SyncEchoStringResult` alone in the response)" (Lab `:162`, adapter `:70`):
  PI, comment, character reference (schema-valid, read), `xsi:type` (refused): covered. Outside: a no-break space
  (FOUND 1).
- "ONE callback: a POST to that path whose body is HP's `AsyncEchoStringComplete` holding the message" (Lab `:170`):
  query, case, trailing slash, percent-encoding, other namespace, second envelope: covered (refused). Outside: text or
  attributes beside `message` (FOUND 2).
- "every other request is answered 404 or 400 and listed" (Lab `:172`): covered for the first 16. Outside: a 17th, a
  request after the callback, or one queued when the wait ends (FOUND 5).
- "at most 16 requests, one per connection, each within 5 s, a head of at most 16 KiB and a body of at most 64 KiB"
  (Lab `:173`-`:174`): slow head, short body, idle connection, chunked, 16 KiB+ head, 65537 length: covered (MEASURED).
- "before any folder is made or any connection opened (exit 12)" (Lab `:153`): covered (no folder, posts 0). Outside:
  a run folder inside a git work tree is exit 9 first (both before any folder: consistent).
- "`--callback-bind` (an IPv4 address, `127.0.0.1` unless given)" (Lab `:166`): `127.1`, `::1`, `010.0.0.1` refused;
  `0.0.0.0` accepted (FOUND 5); `255.255.255.255` parses and fails at start (exit 8, as H16).
- "It writes nothing to the device and owes no undo" (Lab `:147`): `checks_e1.py` check 7 (writer calls 2, the write
  verb's; 0 added Lab lines naming a lower-level send); the verb builds no `Oxpd1Writer`: covered.

## 4. SCANS

- **gitleaks 8.30.1** (`logs/gitleaks.out`): control FIRST, a token built in-process from two halves and 36 random
  characters, never printed, outside the clone: rc 1, `leaks found: 1`, moved to `g2070/_quarantine/gl-control-...`;
  then `gitleaks dir` over the clone rc 0 `no leaks found`; `gitleaks git` over `BASE..de8f2a47` rc 0 (`1 commits
  scanned`, `no leaks found`); the twelve head blobs, both patches, the message, `mutants_e1.py` and `checks_e1.py` as
  `1.txt` to `17.txt` in a new folder: rc 0 `no leaks found`. The texts of this folder: see SCANS-2 below.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 1494 added lines
  (`scratch/checks/added.txt`, written by `checks_e1.py`) and `commit-message.txt`: every class 0, `WORDS: clean (2
  files)`; `B2[0-9]{3}` 0 and 0 (control: the kit counts 32).
- **checks_e1.py** (`logs/checks.out`): `CHECKS: 10 of 10 PASS`, each control as the kit says.
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#51`, `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)`; `build/squash_scan.py` (the head's, equal to main's) with `#51`: control rc 1 found 2,
  message rc 0 found 0, `SQUASH-SCAN: clean`; gitleaks over this folder's seven texts under neutral names, the control
  re-scanned first (rc 1, `leaks found: 1`, quarantined): rc 0, `no leaks found` (01:40, `logs/gitleaks-texts.out`).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). The whole solution after the mutants (the clone's porcelain is 0
lines after the tool's undo, so the measured head is the bytes that ran; the seat ran it). The LAN run (not this lane).
The FOUND 4 consequence on a device (DERIVED; the stub ignores the delay).

## OUTSIDE THE FENCES

None. Writes: this folder and `fleet/state/s325/g2070/` only (my clone, its two worktrees, logs, scratch, quarantine).
No pull request, no push (the clone's push URL is `invalid://no-push`), no re-run of a hosted job, no `cd`, nothing
deleted, no printer or device, no Azure, nothing to any person. Every gh call a GET under the project's GH_CONFIG_DIR.
One read command of mine sent a GET's stderr to `/dev/null` (a `commits/<bad sha>` probe; no effect on any result).
