GATE B1982: GO WITH FINDINGS @ 8dc7390 on main da8d64a

Gate G1 (security surface: network reach, TLS trust, credential masking), round 1 of 2 of lane L1, one Opus reader.
OXPd 2, lane L1, kit B1971 (seat X45; Q1 = a in words at stamp S4: `probe` only, `read` a later round; Q2 to Q7 the
defaults; every choice the coordinator's, none the product owner's). Head `8dc7390dc51df081f8fe1963c1f74db9696ce992` on
`b1971/l1-lab-probe`, ONE commit, one parent `da8d64a8` (BASE = main). Read and measured 2026-11-23 12:18 to 12:47 AEDT
on Opus 5.5 in my own scratch `fleet/state/s316/g1982/`: `clone` (the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity; detached at the head), worktrees `red` (BASE + `1-red.diff`, then + `2-fix.diff`,
then + my probe file) and `mergeta` (lane TA's head `4d4e933c` + this head's diff, staged, never committed). Every
dotnet job through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (59 jobs by `gate.log`,
lock waits 0 to 14, load1 2.3 to 6.8); no other holder's lock touched. Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No
write to the project, GitHub or Jira; no push, no pull request, no re-run; no `cd`; nothing deleted; nothing connected
to any address but 127.0.0.1.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (tree `fd5604ab` both ways). Red first at BASE +
`1-red.diff`: the Lab executable 37 / 24 failed, every one by an `Assert` failure (24 `Assert.*() Failure` lines, 0
lines holding `Exception`), the 24 names exactly THE CONTROLS'; the whole solution 1846 / 24 / 1818 / 4, all 24 Lab.
The head: 1846 / 0 / 1842 / 4; 21 of 21 mutants MATCH and undone, rebuilt (the dll after the last undo), green again.
The hosted run 45093020558 PASS at --total 1846 --rules 571. The trust rule holds on every TLS path I can find: the
check is the handler's only certificate callback, it reads the leaf and accepts only `Pin is not null && Presented ==
Pin` (`CertificatePin.cs:63`), one handler and one connection per call (MEASURED: 3 TLS connections for 3 requests),
and a cached session does not bypass it (MEASURED: right pin, then a wrong pin, then no pin on the same stub: 0, 4, 3,
no request reached it after the first run). Read-only and plain-HTTP refusals sit in the channel before any
connection. The masking census finds no path where a value under a listed name reaches the output or the run folder.
**Three Minor findings, each a false sentence in the README (and code comment) about a shape the cells do not hand
the code; none lets a write, a redirect, an unpinned TLS request or a listed value through.** Nothing blocks the
landing on this lane's merits; round 1 of 2: fix now or carry is the coordinator's call.

## FOUND

1. **Minor (trust wording; `README.md:19-20`, `ProbeCommand.cs:158`): "Without `--pin` ... stops: nothing is sent" is
   false when `--plain-discovery-tree` is given and the HTTPS port gives no handshake.** The plan's order is
   servicesDiscovery (TLS), discovery tree (TLS), the plain discovery tree, then IPP (`ProbeCommand.cs:136-149`); the
   loop stops only on `FirstContact` or `PinRefused` (`:205-217`), and a call with no handshake is `NoAnswer`
   (`DeviceChannel.cs:123`), so it goes on to the plain GET. MEASURED (my probe, 127.0.0.1): no pin, HTTPS port
   closed, plain asked, IPP on the stub's TLS port: exit 3, ONE plain GET received, 0 TLS requests (S1a); HTTPS and IPP
   ports closed: exit 0, one plain GET, 0 TLS connections, `reading: only the OXPd 1.x discovery tree answered` (S1b):
   a "done" run with no pin and no certificate ever read. Two orders: if the HTTPS port answers its handshake first,
   the run stops and the plain GET is never sent (P01's shape); if it does not, the plain GET goes out. The plain call
   is read-only, opt-in, and its answer masked like any other; what it breaks is the first-contact promise, which the
   needs list's first run (row 0: the discovery tree) will lean on. Fix: refuse `--plain-discovery-tree` without
   `--pin` as a usage error (one P12 row), or stop a no-pin run at its first `NoAnswer`, or say it in the README.
2. **Minor (masking wording; `README.md:28`, `Masking.cs:16`): "A body of another type ... is not shown" is false
   for a body that starts with `{`, `[` or `<` and parses.** `KindOf` (`Masking.cs:50-69`) reads a body as JSON when
   its first byte is `{` or `[`, as XML when it is `<`, whatever its type. MEASURED: `application/octet-stream` `<r>m</r>`
   shown (S3b), `text/plain` `{"note":"m"}` shown (S4), no type `["m"]` shown (S4b), each masked by name only. M03's
   html row is `<html>` unclosed (an XML error), so no cell hands it a well-formed one. Also (same limit) an XML comment
   or processing instruction is shown whatever it holds (S6, S6c). The values are still masked by NAME, so this is the
   README Limits case (T7) under a sentence that says otherwise. Fix: sniff only when the type is absent, or show
   other types as type and length only; or correct the sentence.
3. **Minor (robustness): a JSON answer that holds one property name twice throws `ArgumentException` out of
   `Masking.Body`** (its catch at `Masking.cs:44` lists six types, not this one). MEASURED: S5 and S5b throw
   `System.ArgumentException` (the message names the property, never the value: marker in the exception text False).
   DERIVED: `RunRecorder.Record` and `DeviceChannel.SendAsync` do not catch it, so the run ends with an unhandled
   exception, no `summary.txt` and no printed lines; that call's file is not written (fail closed: no value leaves).
   Fix: catch `ArgumentException` beside `JsonException` (one M03 row), or parse with duplicates refused as a
   `JsonException`.

## INFO

1. **The trust rule, read whole.** `CreateHandler` (`DeviceChannel.cs:48-62`): `UseProxy = false` (53),
   `AllowAutoRedirect = false` (54), `UseCookies = false` (55), `ConnectTimeout` (56), `PooledConnectionLifetime =
   TimeSpan.Zero` (57), the callback (59), TLS 1.2 | 1.3 (60); a new `CertificateCheck` and handler per call (89-91),
   HTTP/1.1 exact (94-95). No other `HttpClient`, handler or socket in `src/Datasec.Suite.Lab/` (the lab's only network
   type is `SocketsHttpHandler` here). A pinned handshake whose request then fails reads `NoAnswer` (`:125`) and the
   run goes on; a pin refusal stops it. No path sends a TLS request before the pin holds.
2. **The masking census.** Output (`ProbeCommand.Line`, `:234-243`): label, address as typed, status, the device's
   content type, `Detail` (byte count, IPP status, the values of `printer-make-and-model` and
   `printer-firmware-string-version` through `Masking.ValueText`, names not on the list), the pin hash, the reading.
   No header or body reaches the output. Run folder (`RunRecorder.Record`, `:38-75`): request line, our own IPP request
   (masked), outcome, the presented hash, the exception TYPE name, status, every header through `Masking.Header`, the
   body through `Masking.Body`; `Summary` writes the printed lines. File names come from the plan's fixed labels, so
   nothing is written outside the run folder (`Path.Combine(Folder, name)`, no separator in any label). Values under
   unlisted names are shown (MEASURED: `Location`, `WWW-Authenticate`, `X-Auth-Key` headers shown, S9 to S9c): the
   README's named limit.
3. **Masking shapes that hold.** MEASURED: CDATA under a listed element (S6b), a prefixed listed element (S6d), a listed
   name holding an object (S7): not shown; a DOCTYPE (S6e), JSON 70 deep (S8), a UTF-8 BOM before JSON (S10): the
   not-shown form (fail closed).
4. **Only the Lab names the Lab.** `git grep -i -l Datasec.Suite.Lab` at the head: the slnx, the Lab's own files and
   its tests, nothing else under `src/` (control: the Lab's own csproj found). The lock files hold `Project` and two
   `CentralTransitive` (Serilog, Serilog.Sinks.File) entries, no new package; `xunit.v3` and the AspNetCore framework
   reference exist at BASE (`Directory.Packages.props:12`, Contracts.Tests csproj).
5. **The slnx, byte for byte:** the head's file equals BASE's with exactly the two Lab lines inserted after the two
   Jobs lines (program; control with one line only: False). Every other BASE entry (39) `diff --quiet` rc 0, control
   rc 1. Name-status 18 A + 1 M (control: a planted Core row fails the check). Numstat 1868 / 0 (compare API too).
6. **The seat's DEVIATION D-4 (the sidecar held no per-file numstat rows): it hides nothing.** The `.measured`
   sidecar (157 lines) is a per-literal provenance list; it holds no numstat rows, as the seat said. My `diff --stat`
   gives each file's count equal to THE CODE's (lock files 52 and 211). One sidecar line worth knowing: the
   prototype's red log `d-exe-red.log` held 3 `Exception` lines; the seat-form red log held 0 (the kit's figure), and
   mine holds 0.
7. **The frame question (stamp item 11), every "every / never / no path / only" sentence:**
   - "no accept-all" / "with --pin every connection must present the pin": (a) a cached TLS session: MEASURED held
     (S2, macOS only); (b) a second port with another certificate: P06; (c) a redirect to another host: P07. Linux and
     Windows resumption: UNMEASURED (the hosted legs pass P04 to P06, which do not resume after a success).
   - "without --pin nothing is sent": (a) HTTPS port silent + plain asked: FOUND 1; (b) a handshake with no
     certificate: `Validate` false, `NoAnswer`, nothing sent (DERIVED); (c) 443 silent, 631 answers: first contact on
     631, stops (DERIVED).
   - "the ONE call that may use plain HTTP": (a) another planned call turned to http: H01; (b) the refusal reads the
     call's `AllowsPlainHttp` flag, not its path or method, so a later plan line flagged true would pass: H03 holds
     the plan's labels; named limit (DERIVED); (c) a redirect to http: not followed (same flag as P07, DERIVED).
   - "refuses any call that is not read-only": (a) HEAD or OPTIONS: neither GET nor POST, refused (DERIVED); (b) a
     GET with a body: the channel adds a body only for an IPP operation, and a GET with one is refused (H02); (c) a
     POST whose body says another operation: the body is built from the same field the rule reads (P09 wire check).
   - "is not shown" (bodies): FOUND 2 (sniffed types), FOUND 3 (duplicates), S6e/S8/S10 hold.
   - "no other project under src/ references it": (a) a csproj with another path form: B02 reads text, covers it; (b)
     a reference by `Directory.Build.props` or an imported targets file: B02 reads `*.csproj` only, named limit; (c) a
     project outside `src/`: not covered by B02; the publish guards (10 and 11 files, unchanged) cover the server.
   - "never writes outside its run folder": labels fixed; the run folder itself is the operator's path
     (`Directory.CreateDirectory` makes parents); the exists-then-create check is not atomic (named limit).
   - Orders that matter: parse, then the folder, then the first connection (P12, P10); the handshake's callback before
     any request byte (by .NET's SslStream contract, UNMEASURED beyond the cells); recording after the exchange, so an
     exception in masking loses that call's file and the summary (FOUND 3).
8. **TA first (MAIN MOVES):** `git merge-tree --write-tree 4d4e933c 8dc7390d` rc 0, tree `2da9cc72`, no conflict;
   `mergeta` (TA head + this diff, index tree `2da9cc72`): locked restore rc 0 (no lock file changed), build 0/0,
   `total: 1874`, `failed: 0`, `succeeded: 1870`, `skipped: 4` (1846 + 28), `RULES: clean (580 files)` (571 + 9).

## WHAT I MEASURED

- THE TOOLS: `cp -Rc` of `fleet/state/s315/d1971/seat-tools/` to `g1982/gate/`; 10 of 10 sha256 equal to the kit's
  table and to the seat's `.tools/b1971/gate/` copy. `words.py --control` `CONTROL FIRED: 13 of 13`.
- THE COMMIT: one parent `da8d64a8`; stored message equals `commit-message.txt` (334 bytes); author and committer the
  project's own address (masked). Origin: main `da8d64a8`, branch `8dc7390d`, compare ahead 1 behind 0, 19 files,
  +1868 -0; open pull requests 0 (newest 32, merged); open alerts on main 0.
- RED (`red`, `1-red.diff` alone; `CODE red: 19 of 19 equal`): locked restore rc 0 (status: the 19 owned paths only);
  build 0/0; Lab executable `Total: 37, Errors: 0, Failed: 24` (H01 H02 H04 H05 M01 M02 M03x6 P01 P02 P03 P04 P05 P06
  P07 P10 P12x4), `Exception` 0, `Assert.*() Failure` 24; whole solution 1846 / 24 / 1818 / 4, `failed Datasec.` 24,
  all `Datasec.Suite.Lab.Tests.`.
- PATCHES = HEAD: `red` + `2-fix.diff`: `CODE both: 19 of 19 equal`; `write-tree` `fd5604ab` = the head's tree.
- GREEN (clone at the head): locked restore `--force` rc 0, status clean; build 0/0; whole solution 1846 / 0 / 1842 / 4;
  Lab executable 37 / 0.
- MUTANTS: `mutants_l1.py <clone> <keep> run g1982 'B1982 gate'` as ONE call: 21 rows, every row `Total 37`, MATCH,
  undone True; `MUTANTS: 21 of 21 MATCH, 21 of 21 undone equal` (rows equal to the seat's). After: status clean,
  `CODE both: 19 of 19 equal`; build 0/0 with `Datasec.Suite.Lab.dll` 12:41:27 after the last undo 12:40:16; Lab 37 / 0.
- PROBE (`G1982Probe.cs`, one fact, 21 shapes, outcomes only, no value printed; built 0/0 in `red`, run whole `Total:
  38, Errors: 0, Failed: 0`; outcomes `g1982/scratch/probe-out.txt`; the file then moved to `g1982/_quarantine/probes/`).
- HOSTED: `hosted2.py 8dc7390d... --total 1846 --rules 571 --skipped-linux 4 --skipped-windows 21 --unit 111 --floor
  111 --hardened-scan`: run 45093020558, four jobs success attempt 1, linux 1842, windows 1825, RULES 571, Ran 111,
  every hardened secret-scan row OK: `HOSTED 8dc7390d...: PASS`. `failed Datasec.` 0 in both legs; the Lab test dll
  `passed` on linux and windows (control). That push run has no Analyze rows: CodeQL is read on the pull request.
- MAIN OF THE MOMENT: main = BASE, so the merge is the head (`merge-tree` = `fd5604ab`). RULES on the head `clean (571
  files)` (`RULES-NOTE: R5 hash half NOT RUN`, never `--source-documents`).

## SCANS

- `words.py` over the 1605 added lines of `da8d64a8..8dc7390d` (lock files left out, as the kit) and the stored
  message: every count 0, `WORDS: clean (2 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token built by
  program from two halves and 36 random characters, alone in a new folder, never printed): rc 1, `leaks found: 1`,
  moved to `g1982/_quarantine/gl-control`; the 19 head blobs, the added lines and the message as 21 neutral files:
  rc 0, `no leaks found`.
- ASCII: 0 of 19 blobs with a byte outside printable ASCII, a tab or a CR; final LF on all but the two lock files
  (control: a planted U+200B line counts 1).
- Landing texts: `words.py` over `squash-subject.txt` (175 bytes), `squash-body.txt`, `pr-title.txt` (166 bytes):
  `WORDS: clean (3 files)`; `build/squash_scan.py <subject with #33> squash-body.txt --scanner gitleaks` (from the
  head's build/): control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs only); CodeQL (read on the pull request); the loop (the seat's
`LOOP green: 20 of 20` RELAYED); the chain's two publishes and `release_guard.py` locally (hosted GUARD 10 and 11 files);
`run_step.py`'s neutral scan locally (hosted secret-scan every row OK); `repo_rules.py --source-documents` (never); the
hosted run of any merge; any run of the tool against a device, a simulator or any address but 127.0.0.1; any re-run.

## DEVIATIONS

None from the commission. The probe file is a gate-scratch file in a worktree, never committed; it ran the tool
in-process against its own loopback stubs only, as the cells do. The loop (kit step) was not in the commission's list
and was not run.

## TREES LEFT

`g1982/clone` detached at `8dc7390d`, clean (mutants undone, rebuilt); worktree `g1982/red` at `da8d64a8` with both
patches in its working tree, staged (tree `fd5604ab`, never committed; probe file moved out, its build output under
`bin/`); worktree `g1982/mergeta` at `4d4e933c` with this head's diff staged (tree `2da9cc72`, never committed);
`g1982/logs/**`, `g1982/scratch/**`, `g1982/_quarantine/{locks,gl-control,probes}`. No process left running; the wave
lock not held by this reader.
