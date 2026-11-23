GATE B2008: GO WITH FINDINGS @ f039956 on main 2e2feae

Gate G1 (the project's first device-WRITE code, carrying the admin password), round 1 of 2 of lane W1, one Opus reader
(claude-opus-5-5), in-session, read-only. OXPd 2, lane W1, kit B2005 (seat X57; Q1 and Q2 "a" in words at stamp S4, Q3 to
Q9 the defaults; each the coordinator's, not the product owner's). Head `f039956da818a29d38633ad872d593cecafe83a0` on
`b2005/w1-oxpd1-signin-agent-write`, ONE commit, one parent `2e2feae8` (BASE = main = L5's squash, PR 40). Main did NOT
move during the gate (2e2feae8 by gh api -X GET at about 21:59 and 22:07 and by two fresh clones). Read and measured
2026-11-23 21:57 to 22:15 AEDT in my scratch `fleet/state/s318/g2008/`: `clone` (clone.py draft: push URL
`invalid://no-push`, no identity; the head checked out detached), worktrees `red` (BASE + `1-red.diff`), `pat` (the head
+ a gate probe file, now in `_quarantine/G2008Probe.cs.txt`), `basewt` (BASE, the adapter built for the reflection and
byte comparisons); `clone2` (a second draft clone) with worktree `mlh` (lane LH's pushed head merged with this head). Every
dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (40
released lock folders, all mine, in `g2008/_quarantine/locks/`; lock waits 0 or 1 per job; the lock absent at the end; no
other holder's lock touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub
or Jira; no push, no pull request, no re-run; no printer, no tenant; the project's 4_Credentials not read (only the gh
config dir used by `gh`); nothing deleted.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (temporary-index `write-tree`: red tree `18598ac9`,
both-patches tree `a1d181da` = `f039956d^{tree}`; both equal the drafter's trees); the ten tools and both patches equal
THE TOOLS' sha256 in my copy and in the seat's `.tools/b2005/gate`; the commit message is the tool's file. Six paths (2 A,
4 M), numstat equal to the kit's table; `checks_w1.py` 7 of 7 with every control. Red first: client 40 / 9 failed, the 9
planted cases exactly, 9 of 9 by an `Assert.` line. Green 2020 / 0 / 2016 / 4 (twice: before and after the mutants).
`MUTANTS: 11 of 11 MATCH, 11 of 11 undone equal` (my run of the frozen tool). **The G1 questions, MEASURED by a probe on
macOS:** a dry run opened 0 connections, sent 0 requests and read 0 settings in 12 call shapes; an executed register sent
exactly ONE password-bearing request in 36 of 36 shapes (18 ends x a fresh and a reused pooled connection: 401, 401 with a
challenge, 403, faults, 307, 302, oversized, time-out, reset, TLS and TCP close after the request, a broken status line,
and more); every end that may have applied carried an undo that is itself a dry run (sent as given: 0 requests); the
password or its Basic token was in no result text, fault code (one planted there) or record; only the two committed
operations were sent; `Oxpd1Client`'s public members equal BASE's (4 of 4, by reflection); the reads' envelopes equal
BASE's byte for byte (20 of 20). Hosted push run 45159822038 PASS on both legs (linux 2016, windows 1999, RULES 645). Two
Minor findings and six Info; none sends a byte, none blocks the landing.

## FOUND

1. **Minor (the record takes one address shape it says it refuses, and its body then fails HP's schema).**
   `Oxpd1Writer.cs:131` refuses user information by `value.UserInfo.Length != 0`. MEASURED (probe RECORD rows):
   `https://@lab-host.example/a` (an EMPTY user-information part) is TAKEN: `UserInfo` is empty, but `AbsoluteUri` keeps
   the `@` (27 characters written), and the register body then has **1 schema error** against HP's committed `LimitedUri`
   (`common.xsd:440`, pattern `(https?|file|ftp)://([^@]*/.*|[^@]*\?.*|[^@]*)`, which HP documents as "explicitly
   prohibiting the use of "@" in the domain part"). So two README sentences are false on this shape: `README.md:42` to
   `:43` "takes only absolute `https` addresses with no user information" and `:34` "both request bodies validate
   against HP's committed schema". Nothing is sent by the record or a dry run; an executed call would send a body HP's
   schema refuses (what a device answers is UNMEASURED; any non-answer end is `Unknown` with the undo, which is safe).
   Refused as they should be: `u@`, `u:p@`, `:p@` on either address, `http`, `ftp`, `file`, `wss`, relative, 257
   characters. Taken and schema-valid: `@` in the path or the query, `HTTPS` (normalised), an IDN host (written in
   Unicode, 24 characters; what a device accepts UNMEASURED). Fix (round 2): also refuse an authority that holds `@`
   (e.g. test `AbsoluteUri` against HP's pattern, or `OriginalString`'s authority), and a W07 row for `https://@host/`.
2. **Minor (the undo restores the device only when the id was not there before; nothing says so).** HP's committed text
   (`authentication.wsdl:70`): "If a record with the same ID already exists in the device's list, its content is replaced
   with the content of the new one." The undo the register hands back is the unregister of that id (`Oxpd1Writer.cs:167`,
   `:274`), which would REMOVE the pre-existing record, not restore it (DERIVED from HP's text and the code; UNMEASURED on
   a device; the stub replaces by id too, `StubDevice.cs:373`). W03's name says "leave the device as it was", true on an
   empty registry only. The enum's doc comment says "or replaces the record that already has its id"; the README's
   writes paragraph and its Limits do not say the undo is not a restore in that case. The caller picks the id (the cells
   use a fixed synthetic GUID). The safety question of the commission (undo after a time-out) holds as the kit says: HP's
   `:105` "this method will succeed (no exception thrown), but will have no effect" for an unknown id, and the probe's
   time-out end carried the undo; W05 shows it on the stub. Fix (round 2 or the lab wiring): a named limit in README
   Limits, and the lab write verb reads `GetAuthenticationAgentRecords` (already a read of the client) and refuses an id
   already present.
3. **Info (a control character in the name).** `Oxpd1SignInAgent` takes a name holding U+0001 (MEASURED: TAKEN); the dry
   run and an executed call then throw `ArgumentException` from `XmlWriter` before anything is sent (MEASURED: dry run
   THREW, 0 requests). Not a leak path (the call is built before any password is read). Also: the name's 1 to 100 is
   counted in UTF-16 units: 51 astral characters (valid by HP's character count) are refused, 50 taken; stricter than
   HP, harmless.
4. **Info (a blank setting is a password).** A setting value of one space is sent as the password (MEASURED: `Answered`,
   1 request); only null and empty end `NoCredential` (`Oxpd1Client.cs:99`, `string.IsNullOrEmpty`). Same rule as the
   landed reads (`:65`, `:74`). On a device with a five-attempt lockout a whitespace setting would spend an attempt;
   the lab's credentials file (L5) is the caller that should refuse it.
5. **Info (named limits the README does not carry).** A caller's cancellation throws and returns no result (kit H11:
   true, the `catch ... when (!cancellationToken.IsCancellationRequested)` does not take it); the README Limits are
   silent on it (the kit's FOR RECORDS has it). A dry run writes no record line (MEASURED: 12 dry runs, record file 0
   bytes). A time-out while connecting (nothing sent) also reads `Unknown` with the undo: conservative, the right side.
6. **Info (the H10 limit is now MEASURED for writes, macOS only).** The kit's H10 ("the HTTP layer resending the write"
   RELAYED from the reads' gate): 36 of 36 executed shapes gave one password-bearing request, including a TLS close and a
   TCP FIN right after the request on a REUSED pooled connection (the shape an HTTP stack may retry). Windows and Linux:
   the hosted cells only.
7. **Info (the word check's B-number class).** `words.py`'s B-number pattern is `B1[0-9]{3}` and does not match a
   `B2xxx` number. I counted `B2[0-9]{3}` separately over the added lines and the message: 0 and 0 (control 1). A tool
   gap for the next kits, not this head.
8. **Info (lane LH beside).** LH's head `25cb4cb2` (pushed, one commit on 2e2feae8, 16 Lab paths, NOT YET GATED) shares no
   path with this head; `merge-tree` rc 0, tree `4af54a4b`; that tree built and tested: 2054 / 0 / 2050 / 4, RULES 647,
   no lock file changed (landing.txt MAIN MOVES (B)).

## THE KIT'S GATE LIST (FOR TUESDAY)

- `BASE..head` read whole: `Oxpd1Writer.cs` (324 lines), the diffs of `Oxpd1Client.cs`, `Oxpd1Soap.cs`, README and
  `StubDevice.cs`, `WriteTests.cs` whole; the landed `SendAsync`, `Judge`, `ReadBoundedAsync`, `Pinned`, `Record`,
  `ContractTests.cs:121` to `:177`; HP's `authentication.wsdl:66` to `:76` and `:100` to `:111`, `authentication.xsd`
  (the record), `common.xsd` (`LimitedUri`, `DebugNameString`, `Timeout`, `Retries`, `RetryInterval`, `LocalizedString`).
- Patches and tools: 10 of 10 sha256 equal (both copies). Head tree = BASE + both patches (above).
- Red first: 40 / 9, the nine cases W02; W04; W05; W06 `forbidden`, `unauthorized`, `wrong-pin`; W07; W09 `child`,
  `other-element`; missing none, extra none; each by `Assert.True()`, `Assert.Equal()` (Expected Unknown or No, Actual
  Yes) or `Assert.Throws()`.
- Mutants: every row `Total 40`, each red on exactly its listed cells, `undone equal True`; after them the clone's status
  empty, a rebuild (the test bin's adapter dll 22:05:38, later than both mutated sources 22:04:32 and 22:04:46) and the
  whole solution 2020 / 0 / 2016 / 4 again.
- Can a request leave when `Execute` is not set? No path: `WriteAsync`'s only call of `SendWriteAsync` is after the
  `if (!call.Execute)` return (`Oxpd1Writer.cs:261` to `:266`); `Kind` and `AgentId` have no setter, `Execute` only an
  init; the call is a sealed record built only by the two factories. MEASURED: 12 dry shapes, 0/0/0.
- A second request on one call? `SendWriteAsync` calls `SendAsync` once; `SendAsync` calls `_http.SendAsync` once
  (`Oxpd1Client.cs:141`); the handler sets no `Credentials` (no challenge answered), `AllowAutoRedirect = false`, no
  proxy, HTTP/1.1 exact, `HttpClient.Timeout` infinite with one linked token. MEASURED: 36 of 36 one request (FOUND 6).
- Can `Applied` read `No` on an end that may have applied? `No` only on `NoCredential` (MEASURED 0 connections),
  `PinRefused` (MEASURED 1 handshake, 0 requests), 401 and 403 (HP: the methods require the admin credentials, DERIVED
  that nothing ran; UNMEASURED on a device). Every other value of `Oxpd1Outcome` (Fault, HttpStatus, MalformedAnswer,
  TooLarge, TimedOut, TransportFailed) falls to `Unknown` (the switch's default arm), MEASURED on 14 ends.
- Is the undo safe after a time-out? By HP's `:105` and the stub's `TryRemove` (no effect on an unknown id), yes; W05
  shows remove then repeat; it is NOT a restore when the id pre-existed (FOUND 2).
- The password's reach: `Request` is the envelope (no password; the Authorization header is not in it), `ToString` is
  outcome, status, fault code and applied; `FaultCode` is scrubbed and cut by `JudgeWrite` (MEASURED: a code holding the
  password and its token came back without either); exception texts: none thrown on any executed end; the record
  scrubs (MEASURED: 36 record files, 0 hits; each names `RegisterAuthenticationAgent`). The README's own limit: a caller
  who puts the password in a record name puts it in the envelope (H15).
- Landed read cells green with `SendAsync`'s new private signature: the whole solution 2020 / 0; the read envelopes 20 of
  20 equal BASE's bytes (FOUND list above); the `action` content-type parameter is the same row value passed in.
- Both request bodies against HP's committed schema: W01 green; the probe validated 12 more accepted record shapes,
  all 0 errors but FOUND 1's.
- Hosted run on both legs: `hosted3.py f039956d --total 2020 --rules 645 --skipped-linux 4 --skipped-windows 21 --unit
  111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15` (read 22:06): run 45159822038, attempt 1, every
  step success; linux `total: 2020` x2, `succeeded: 2016`, `skipped: 4`, GUARD 14; windows `succeeded: 1999`, `skipped:
  21`, GUARD 15; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3, NEUTRAL lines `wrong 0`, `not among ... 0`;
  rules `RULES: clean (645 files)`, floor 111; `HOSTED f039956d...: PASS`; `failed Datasec.` 0 and 0;
  `Adapters.Oxpd1.Tests.dll` 4 lines per leg. Check runs beside the four: 0 (the PR's run is the first CodeQL analysis).
- words and gitleaks: below (SCANS).

## WIDER (G1 depth): a test-only probe (`_quarantine/G2008Probe.cs.txt`, never committed; results
`g2008/scratch/probe-results.txt`, counts only, no value; the client executable whole `Total: 41, Errors: 0, Failed: 0`
twice)

- Dry run (no `Execute`), 12 shapes: register; unregister; `with { Execute = true } with { Execute = false }`; the call's
  `Undo`; the `Undo` of an executed-flag call; an edge record; a 2004-addressing client; a setting reader that throws; an
  unresolvable `.invalid` host on port 1; a disposed client; a cancelled token; 20 at once. Each `DryRun True`, `Applied
  No`, `Undo null`, 0 new TLS connections, 0 requests, 0 setting reads on every client.
- Executed register, 18 ends x fresh/reused connection (36 rows): exactly 1 request and 1 password-bearing each;
  401/401-challenge/403 `No`, no undo; answer and answer-then-close `Yes` with undo; every other end `Unknown` with undo;
  the undo `Execute False`, the same id, and sent as handed back a dry run with 0 new requests. Wrong pin: `PinRefused`,
  `No`, 0 requests. Setting null or empty: `NoCredential`, 0 connections.
- The record: FOUND 1 and 3; time-outs 0, -1, 301 and `int.MaxValue` refused, 1 and 300 taken; empty id refused (record
  and unregister); null name, null address, null record refused.
- Operations sent over every executed shape: body elements `RegisterAuthenticationAgent`, `UnregisterAuthenticationAgent`
  and the two matching actions; actions outside the committed bindings 0 (control: a planted `RegisterUIButton` action
  counted 1).
- Public surface: `Oxpd1Client` 4 public members at BASE and at the head, equal (constructor, `GetDiscoveryTreeAsync`,
  `ReadAsync`, `Dispose`); C04 green; the C04 helper names `RegisterAsync` on its planted type (control). Exported types
  6 -> 12: added `Oxpd1Applied`, `Oxpd1SignInAgent`, `Oxpd1WriteCall`, `Oxpd1WriteKind`, `Oxpd1WriteResult`,
  `Oxpd1Writer`; removed none; no other landed public type changed its members.

## FRAME (stamp checklist item 11: three shapes outside the tested one per every/never/at-most/only sentence)

| Sentence | Shapes outside the tested one | Cell, probe or stated limit |
|---|---|---|
| P1 a dry run sends nothing and reads no setting | Execute set then unset; disposed client; throwing reader; unresolvable host; cancelled token; 20 at once | probe: 0 connections, 0 requests, 0 reads in all |
| P2 an executed call sends at most ONE request, no retry | 401 challenge; 307/302; FIN or reset after the request on a reused connection; broken status line | probe: 36 of 36 one request (macOS); hosted cells on the other legs |
| P3 every end that may have applied carries its undo | 200 fault; 500 with the empty response; 200 empty body; oversized; partial status line | probe: undo set on every `Unknown` |
| P3b the undo is itself a dry run | undo of a result; undo of a call; undo sent as given | probe: Execute False, 0 requests |
| P4 `No` only where nothing could have applied | wrong pin; empty and blank setting; 401 with challenge | probe: pin 0 requests; blank setting IS sent (FOUND 4); 401/403 DERIVED from HP |
| P5 the password in no result text or record | password in the fault code; record on every end; exception texts | probe: 0 hits; the name-in-record case is a stated limit (H15) |
| P6 only operations of the committed bindings | every executed end; both kinds; the undo | probe: 2 operations, 0 outside; checks_w1 check 6 |
| R the record takes only https without user information, at most 256 | `https://@host`; `@` in path/query; IDN; upper-case scheme; 256/257 | probe: FOUND 1 (the empty-userinfo hole); the rest as stated |
| U "leave the device as it was" (W03's name; README "each with its undo") | the id already registered; a time-out after apply; the undo sent twice | FOUND 2 (not a restore); W05 (time-out, repeat) |

## SCANS

- gitleaks 8.30.1: control FIRST (a GitHub-token-shaped value built by a program from two halves and 36 random
  characters, never printed, alone in a new folder): rc 1, `leaks found: 1`, folder moved to `g2008/_quarantine/gl-control`.
  Then the head's 6 changed blobs, the added lines (786), the commit message as committed and both patches under neutral
  names `1.txt` to `10.txt`: rc 0, `no leaks found`.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; the added lines + the commit message as committed `WORDS: clean (2
  files)`; the squash subject (with #41), squash body and PR title `WORDS: clean (3 files)`. `B2[0-9]{3}` 0 and 0 over
  the added lines and the message (control 1; FOUND 7).
- squash_scan.py (the head's `build/`, equal to main's): subject with #41 + `squash-body.txt`: control rc 1 found 2,
  message rc 0 found 0, `SQUASH-SCAN: clean`.

## THE CHAIN AND THE MERGE

- Head (`clone`): locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test`: `total: 2020`,
  `failed: 0`, `succeeded: 2016`, `skipped: 4`. `repo_rules.py` (no `--source-documents`) `RULES-NOTE: R5 hash half NOT
  RUN`, `RULES: clean (645 files)`; `unittest` `Ran 111 tests` OK; `checks_w1.py` 7 of 7 (shared paths 53 rc 0, control
  rc 1; added 786, removed 22; public lines 43: Writer 32, README 1, tests 10).
- Merge with main of the moment (2e2feae8 = BASE): `git merge-tree --write-tree` rc 0, tree `a1d181da` = the head's. The
  merge is the head; measured above. Open PRs 0; open code-scanning alerts 0; main's analyses results 0.
- With lane LH's pushed head first (FOUND 8): 2054 / 0 / 2050 / 4, RULES 647.

## NOT RUN

- The probe on Windows and Linux (the one-request and dry-run results are MEASURED on macOS only; the hosted legs ran
  the cells).
- The two `dotnet publish` lines and `release_guard.py` locally (the hosted legs' GUARD 14 and 15 read instead; the
  seat ran both locally).
- CodeQL locally; the PR's merge-ref run (does not exist yet).
- An independent build of the mutants (my run is of the frozen tool, same as the seat's).
- Any device, simulator or tenant: every device answer, the endpoint path, the fault subcodes and apply-before-refuse.

## DISCLOSURE

- One hook refusal: `pretooluse_recursive_scope.sh` refused an unscoped `grep -rn` for `InternalsVisibleTo` over my
  clone's adapter folder (under fleet/state). I did not repeat it or reach it another way; the cells that use internal
  types compile, which is all that search would have shown.
- My scratch `clone2`'s `git commit-tree` (to stage the LH merge for a build) failed for want of an identity; I set none
  and instead put the merge tree into a worktree with `read-tree -u -m` (no commit, no ref).
- The probe's "120-character address that escapes past 256" shape did not test what it says: `Uri` trims trailing
  spaces, so it wrote 25 characters. Not counted as a finding either way.

## LANDING

`landing.txt`, `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md` in this folder.
Who decides to land: the coordinator (Tuesday), never the product owner. FOUND 1 and 2 are for round 2 of 2 of lane W1
(or the lab wiring lane for FOUND 2's read-first), not a hold on this landing: nothing in either sends a byte today, the
writer has no caller yet, and the lab wiring that will call it is a later commission.
