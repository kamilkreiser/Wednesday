GATE B1981: GO WITH FINDINGS @ 685d72b on main da8d64a

Gate G1 (security surface: the first HTTP routes a printer reaches, the per-device credential, the vault binding),
round 1 of 2 of lane H, one Opus reader (claude-opus-5-5), in-session, read-only toward the project, Jira and GitHub.
OXPd 2, lane H, kit B1974 (seat X48; Q1 = a in words at stamp S4; Q2 OVERRULED to HOLD; Q3 to Q7 the defaults; every
choice the coordinator's, none the product owner's). Head `685d72b66f1c87d78f7097af38a870fe037e7fbe` on
`b1974/h-host-composition-v0`, ONE commit, one parent `da8d64a83bf9f58e4b02fa2c11526dd6a7c7261b` (= main at every read,
12:17 to 12:41 AEDT). Measured 2026-11-23 12:18 to 12:41 AEDT in my own scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s316/g1981/` (clone by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity). Every dotnet job and test executable through the kit's `heavy.py` (sha256
`31adedc8...`) and `.tools/wave1-heavy.lock.d`, one at a time (lock waits 0 to 12 polls behind the B1979 and B1982
gates; their locks never touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR only. No push, no pull
request, no re-run, no Jira, no `cd`, nothing deleted (two probe files and the scanner control moved to
`g1981/_quarantine/`). No listener but the tests' own on 127.0.0.1 port 0; the server executable never started.

**BLUF.** The head is BASE plus the kit's two frozen patches byte for byte (14 of 14 files equal to `git show
<head>:<path>`; 3 M, 11 A; numstat equal to the kit's; slnx byte-equal to BASE). I ran the 13 cells myself: red first at
BASE + `1-red.diff` `Total: 13, Errors: 0, Failed: 12`, all 12 by `Assert.` (H12 green by design, 0 lines holding
"exception"); green at the head `Total: 13, Errors: 0, Failed: 0`; `MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal`, then
rebuilt and green again; whole solution at the head (= the merge with main of the moment: `merge-tree` tree `2d84a00e`
= the head's tree) `total: 1809`, `failed: 0`, `succeeded: 1805`, `skipped: 4`; the head's hosted run 45092676825 read by
the kit's `hosted3.py`: `HOSTED 685d72b6...: PASS` (rules 564, guards 14/15). Scans clean with fired controls. The
census holds: three endpoints (`ServerHost.cs:49` to `:51`), no middleware; a callback sink is reached only at
`Oxpd2CallbackHandler.cs:183`, after `Verify` (`:100`) and after the host's HTTPS check (`CallbackEndpoint.cs:15`); the
notification sink only at `NotificationEndpoint.cs:58`, after HTTPS (`:20`), `Verify` (`:29`) and both bounds. Hashes
are compared by `CryptographicOperations.FixedTimeEquals` (`ICallbackHashComparer.cs:14`). **Three Minor findings, no
Blocker** (FOUND 1 to 3): the one-header rule is untested on BOTH routes (the kit named one survivor; I measured a
second, and measured that two header lines are reachable in production and refused 401 at the head); the kit's
"no presented credential reaches a log line" does not hold at Debug for a malformed header line (MEASURED, framework
code, not lane code); the root README's two Server lines become false. H is HELD (S4): it lands only after L1 and the
slnx round; FOUND 1 to 3 fit that round.

## FOUND

1. **Minor (test gap on a security rule): the "exactly one `Authorization` header" rule is reached by no cell on
   EITHER route; the kit names only the callback survivor.** `CallbackEndpoint.cs:27` and `NotificationEndpoint.cs:29`
   each read `Authorization.Count == 1 ? [0] : null`. MEASURED by my probe (a raw HTTP/1.1 client over TLS against the
   rig, file `g1981/_quarantine/probe/GateProbeTwoHeaders.cs`, scratch only, never committed): at the head, one good
   line 200 on both routes (control); two separate lines (same, good-then-junk, junk-then-good) **401 on both routes,
   no sink call** (`sinks cb=1 nt=1` = the two controls only). With `Count >= 1` on the callback line (the kit's
   `mFirstOfTwoHeaders`): two-same 200, good-then-junk 200, junk-then-good 401, and the 13 cells all green (Total 14,
   only the probe red). With the same edit on the notification line (a survivor the kit does not name,
   `mNtFirstOfTwoHeaders`): nt two-same 200, good-then-junk 200, the 13 cells all green. So: **reachable in production**
   (any client that writes two header lines; .NET's HttpClient folds them into one line, which is why H03's doubled
   case never reaches the rule), and **not a Blocker**: the head is fail-closed, and the mutant would still need the
   valid credential in the first line (no request without the credential reaches a sink under either form). Fix in
   round 2: one raw-socket cell per route (two lines, both orders), and name both survivors. Both mutants undone and
   proved (`undone ... equal True`), probe moved out, rebuilt, `Total: 13, Errors: 0, Failed: 0`.
2. **Minor (an overstated property; framework behaviour): "no presented credential ... reaches a log line or scope"
   (kit property, Required Section H6, STATUS H6 row) is false at Debug for a malformed header line.** MEASURED by
   probe 2 (`g1981/_quarantine/probe/GateProbeBadHeaderLog.cs`): a header line `Authorization Bearer <marker>` with no
   colon is refused by Kestrel with 400 before routing, and the rig's Trace capture holds ONE line, category
   `Microsoft.AspNetCore.Server.Kestrel.BadRequests`, level `Debug`: `bad request data: "Invalid request header:
   'Authorization Bearer <MARKER>\x0D\x0A'"`. A control character (`\x01`) or a bare LF in the value: Kestrel admits the
   line, the adapter refuses it 401, marker hits 0; a NUL: 400, marker hits 0. Control: the planted log line is
   captured (control-hits 2). Not lane code, and a well-formed header never reaches it; whether the host emits Debug
   in deployment depends on configuration (the Server project ships no `appsettings.json`; the framework's default
   level is UNMEASURED by me). H11 (well-formed shapes) stays true. Fix in round 2 or the logging lane (Q5): a README
   Limits line naming it, and/or a filter holding that category at Information or above (a product choice for the
   coordinator).
3. **Minor (documentation; repository text made false, `<project>/CLAUDE.md` "No invented facts"): root `README.md:14`
   says the Server "references Core" and `README.md:15` "maps NO route, reads NO configuration secret; never started by
   any test".** At the head it references Core, Adapters.Oxpd2 and Secrets, maps three routes, reads the `Secrets`
   section, and is started by 10 of the 13 cells (all but H06, H10, H12). The kit forbade the root README (the lane could not fix it), and the
   layout list was already behind main before this lane (it lists only the Core test project). Owed: one README pass
   after landing (records lane), or the coordinator lets round 2 of this lane touch those two lines.

## INFO

1. **Patches and tools.** THE TOOLS 11 of 11 equal to the kit's sha256 in three copies (the drafter's `seat-tools`, the
   seat's `.tools/b1974/gate`, mine); control: one byte changed differs. `1-red.diff` applies at BASE; after both
   patches the work tree equals the head's 14 blobs.
2. **The 3 modified files, hunk by hunk.** csproj: two project references and `InternalsVisibleTo` the tests; the
   publish folders grow by the four files the kit names (hosted guards 14 and 15, MEASURED by `hosted3.py`). Lock
   file: two `Project` entries, nothing else. `Program.cs`: the same `WebApplication.CreateBuilder(args)` and
   `AddWindowsService()` (now inside `ServerHost.Build`); new for the existing caller (the container `ENTRYPOINT`,
   `packaging/linux/Dockerfile:9`, unchanged): three routes and a lazily created secret store
   (`SecretStoreServiceCollectionExtensions.cs:12-13`, "created ... when it is first resolved"), so a deployment with no
   `Secrets` section still starts (H08). Which address an unconfigured host binds is the framework's default
   (UNMEASURED); if it is plain HTTP, both OXPd 2 routes answer 403 there (fail closed, DERIVED from `:15`/`:20`).
3. **D1 (route shape) for the install sequencer.** It must register the callback base
   `https://<host>/oxpd2/devices/<serial>/<target>` with `<target>` spelled exactly `Authentication` or
   `UsbAccessories` (the adapter compares ordinally, `Oxpd2CallbackHandler.cs:249`, targets at `:26`), and the
   notification target `.../notifications`; the serial must meet the adapter's serial rule or every call is 401. It
   must issue credentials through the host's own `CallbackCredentials` singleton: the adapter caches a hash per
   instance (`CallbackCredentials.cs:165` to `:199`), so a rotation by ANOTHER process after the host cached the old
   hash leaves the host on the old one until restart (DERIVED; two orders: host reads first, then the other rotates =
   stale; the other rotates first, then the host reads = H07, green). `IOxpd2NotificationSink` is `internal` to the
   Server (`Sinks.cs:6`): a sequencer outside the Server project cannot implement it; that placement is the wave-2
   lane's choice.
4. **D3 (status table) for the sign-in lane.** Every outcome maps (H10, 14 of 14); `SinkFailed` and `AnswerInvalid`
   share 500, `Refused` and `BodyFailed` share 400; the sign-in lane replaces `NotWiredCallbackSink`
   (`ServerHost.cs:40`, an internal registration it edits). What a device does with any non-200 is UNMEASURED (both
   service-target files list 200 only, RELAYED from the kit). Adequate for v0.
5. **Pre-credential work.** A request with any serial that meets the rule and is not cached reads the secret store
   before it is refused (the adapter's own named limit, `CallbackCredentials.cs:13`); the host adds no rate limit, so
   an unauthenticated client can drive one store read per request. A hardening item for a later lane, not this one.
6. **Frame question (stamp checklist item 11).** For each "every / never / only / no path" sentence, three handed
   shapes that are not the tested one:
   - README "Both OXPd 2 routes answer 403 to a request that did not come over HTTPS, before anything else is read":
     (a) a TLS proxy forwarding HTTP: 403, named limit H10; (b) a path with an extra segment or trailing slash: no
     cell; every match lands in one of the two handlers whose first statement is the check, a non-match is the
     framework's 404 (DERIVED); (c) HTTP/2 over cleartext: no cell, `IsHttps` false whatever the protocol (DERIVED).
     "Before anything else": lane code only; the framework has already parsed the header block (FOUND 2 shows it can
     log a malformed line first).
   - README "the `Authorization` header when there is exactly one (none otherwise)": (a) two lines, both orders:
     MEASURED by my probe, 401, no cell (FOUND 1); (b) one comma-joined line: H03; (c) none: H03.
   - README "only `Answered` writes a body": (a) `AnsweredEmpty`: H02 asserts 200 but not an empty body (DERIVED from
     `CallbackEndpoint.cs:34`); (b) the 4xx/5xx: no status-page or exception middleware is wired, so the framework
     writes none (DERIVED, no cell); (c) a handler exception or abort: no cell.
   - README "every read hands out a new array ... and disposes that value": (a) the in-memory store: H06; (b) the real
     `LocalSecretStore` read on success: no cell (H08 covers only a store that cannot open); (c) concurrent reads: no
     cell. A store `TryGet` that throws: propagates as `Unavailable` (H08 shape).
   - README "The bytes are zeroed when the sink returns": (a) a sink that returns: no cell inspects the zeroing (the
     recording sink copies; DERIVED from `NotificationEndpoint.cs:71`, a `finally`); (b) a sink that throws: same
     `finally`, no cell (this round's sink drops, Q6); (c) an abort during the sink: same, no cell. Two orders: a sink
     that keeps the memory and reads after returning sees zeros (the contract says "valid until the call returns",
     `Sinks.cs:5`).
   - Kit "a body over 1048576 bytes reaches no sink whether declared or not": declared and chunked, both routes (H04,
     H09), exactly the bound accepted (H09); not tested: a declared length shorter than the bytes sent (the framework
     ends the body at the declared length, DERIVED), HTTP/2 frames (H11 limit), a declared length over the bound refused
     unread versus read (H13 limit).
   - Kit "no presented credential ... reaches a log line": well-formed wrong and right headers (H11); a malformed line
     (FOUND 2, MEASURED reaches Debug); the Windows event log (H14 limit).
   - Kit census "two routes" / "`/health` reads nothing": at the head three `Map*` calls and no middleware
     (`git grep` over `src/` for `Map*(`, `UseEndpoints`, `UseRouting`: only `ServerHost.cs:49` to `:51`); `/health` is a
     parameterless lambda (`:49`).
7. **Hosted.** `HOSTED 685d72b6...: PASS` re-read at 12:29: linux 1809 twice / succeeded 1805 / skipped 4 / GUARD 14;
   windows 1809 twice / 1788 / 21 / GUARD 15; RULES 564; Ran 111, floor 111; hardened secret-scan rows all OK
   (`NEUTRAL-SCAN: stored objects 1491 ... not among them 0`). Lines holding `failed Datasec.`, `error CS` or
   `Datasec.Suite.Server.Tests` in either leg's log: 0 and 0 (control: `Datasec.Suite.Server` 6 and 6). So the hosted
   legs build, publish and guard the Server and run none of the 13 cells, as the kit says. No `Analyze` row on the
   branch head and 0 code-scanning analyses for its ref: CodeQL is read on the pull request.
8. **Not checked or not run by me:** every cell on Linux and Windows; CodeQL; the drafter's `checks_h.py`, `run_step.py`
   neutral scan and the release guard locally (the hosted run carries the guard and the hardened scan; the seat ran
   them, RELAYED); the red at the whole-solution level (the seat's `total: 1809` at the red tree, RELAYED).

## MEASURED (my runs; logs in `g1981/logs/`)

- Origin 12:17 to 12:41: main `da8d64a8...` (twice); `matching-refs/heads/b1974` one row = `685d72b6...`; open pull
  requests 0 (newest 32, closed); `compare da8d64a8...685d72b6` ahead 1, behind 0, 14 files, +1179 -6; code-scanning
  open alerts on main 0; analyses for the branch ref 0.
- Red (`g-red-*`): locked restores rc 0 and rc 0; build `0 Warning(s)`, `0 Error(s)`; exe `Total: 13, Errors: 0,
  Failed: 12`; `[FAIL]` pattern 12, H12 pattern 0; by `Assert.` 12 of 12 (10 `Assert.Equal()`, H07 `Assert.Single()`,
  H10 `Assert.Empty()`; e.g. H01 `Expected: OK / Actual: NotFound`).
- Green (`g-green-*`): `0 Warning(s)`, `0 Error(s)`; `Total: 13, Errors: 0, Failed: 0`.
- Mutants (`mutants-run.out`): the 12 rows each `Total 13`, each `MATCH`, each `undone equal True`; last line
  `MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal`. After: 14 files equal to the head; rebuild; green 13 / 0.
- Probes (`g-probe-*`, `g-mfirst-*`, `g-probe2-*`): as FOUND 1 and 2. After: probes quarantined, `g-final2-build` rc 0,
  `g-final2-exe` `Total: 13, Errors: 0, Failed: 0`; `status` = exactly the 14 owned paths.
- Whole solution (`g-sln-*`): build 0 / 0 (28 assemblies); `Test run summary: Passed!`, `total: 1809`, `failed: 0`,
  `succeeded: 1805`, `skipped: 4`.
- Scans: gitleaks 8.30.1 control first (a token built by program from two halves and 36 random characters, never
  printed) rc 1, `leaks found: 1`, moved to `_quarantine/gl-control`; the 14 head blobs, the 979 added lines, the
  message and the 200 test-lock lines under neutral names (17 files) rc 0 `no leaks found`; `gitleaks git
  --log-opts=BASE..HEAD` rc 0, `1 commits scanned`, `no leaks found`. `words.py --control` `CONTROL FIRED: 13 of 13`;
  over the 979 added lines (test lock left out by name) and the commit message: `WORDS: clean (2 files)`; the test
  lock's 200 lines alone: `seat ids 2`, both `linux-x64`/`win-x64` (lines 165, 182), as the kit says.
- Landing texts in this folder: see `landing.txt` (SCANS at its end).

## DEVIATIONS

- `mutants_h.py run` ran as one background shell call (the harness bounds a foreground call at 10 minutes), one
  process, every job through `heavy.py`; I started no other heavy job until it ended.
- Two probe files were compiled into MY scratch clone only (never into the head, never pushed), then moved to
  `_quarantine/probe/` and the clone rebuilt and re-run green. They are evidence, not cells; adding cells is round 2's.
