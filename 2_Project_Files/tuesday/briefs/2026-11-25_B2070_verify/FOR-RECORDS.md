# FOR RECORDS: the echo lane round 1 of 2 (kit B2067, seat X71), `oxpd1 echo`, head de8f2a47 (gate B2070: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2067 THE AUTHORITY: `CLARIFICATIONS.md` counts `echo` 0, `guest` 0, `S14` 0; stamp S4 states Q1 and
Q2 in words as Tuesday's; ANSWER-1, Tuesday's, allowed the one re-run of the chain's test). The design B2001 G2 said "a
TLS callback listener"; Q1 "a" (plain HTTP/1.1 on loopback by default) departs from it, stated in the kit (D1).

## What the lane gives (CHECKED by the gate at de8f2a47)
- The OXPd 1.x client makes HP's two string echoes of the Test service (`SyncEchoString`, `AsyncEchoString`) through
  `Oxpd1Echo`, with HTTP Basic for the user `guest`, never `admin` (CHECKED: the gate's 21 end-to-end runs against the
  stub, sync, async, 401, fault and refused-file shapes, sent `admin` 0 times; mutant `mGuestAsAdmin` red on E01 E02).
  A sync answer is read only as one text-only result alone in the response (the five shapes gate B2058 measured on
  `IsServiceEnabled` are refused here, CHECKED; one narrower shape is read, gate B2070 FOUND 1).
- The lab's `oxpd1 echo` makes ONE echo per run, `--pin` required; a `--password-name` holding ADMIN is a usage error
  (exit 2) and a credentials file in which any name holds ADMIN is refused before any folder or connection (exit 12;
  names only are read; CHECKED with leading spaces, `export`, a comment line, CR-only line ends and UTF-16 with a BOM).
  An async echo listens on plain HTTP/1.1 (127.0.0.1 unless `--callback-bind` gives another IPv4 address), sends the
  device the run's own random path, and passes only on a POST there holding the message (exit 13 when none arrives
  within the wait; CHECKED: case, query, trailing slash, percent-encoding, absolute form, dot segment, another method
  all 404). It writes nothing to a device and owes no undo.
- Two new exit codes of `oxpd1`: 12 (an admin name in the credentials file) and 13 (no callback in time).

## Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate)
- **Owed 118 (the LAN run of the echo, the design's G3):** NOT closed: nothing here ran against a device. This lane is
  its prerequisite; the separate kit runs it after this lands (the listener bound to the lab machine's LAN address, the
  M577 calling 192.168.20.x from 192.168.8.x, `--addressing 2004`, the Test service turned on and off around it).
  Carry into that kit gate B2070 FOUND 4 and 5 (the listener reads one connection at a time; `0.0.0.0` binds every
  interface) and the UNMEASURED device behaviour (guest accepted, `http` callback, `Content-Length`, `Expect`, answer).
- **NEW owed item proposed: the landed `Datasec.Suite.Server.Tests` can hang a whole-solution run on macOS arm64.**
  Seen ONCE by seat X71 (2026-11-25 00:48:55 to 01:03:55, `c-test`: the host printed `Running tests from` and no
  result for 15 minutes; main thread in a managed `Monitor.Wait`, every thread waiting, no inet socket; `heavy.py`'s
  time-out ended `dotnet test` but left the test host alive with parent 1 until SIGKILL). Not seen in the seat's three
  other whole runs nor in the gate's six (one whole solution at 01:20, five runs of the Server.Tests executable alone at
  about 01:33, `Total: 15, Failed: 0`, each 3 to 4 s). Not this lane's: the Server.Tests closure is Server, Core,
  Adapters.Oxpd2 and Secrets (no Oxpd1 or Lab assembly in its bin folder), none changed by this diff. A candidate, not a
  cause: `HostRig.cs:108` `await app.StartAsync()` and `:171` `await _app.StopAsync()` take no token and the project
  sets no per-cell bound, so a host start or stop that never completes waits until the runner's bound. Two owed parts:
  (a) a per-cell time bound for the Server.Tests cells; (b) `heavy.py` (Tuesday's runner) ends `dotnet test` but not its
  test host: a hang leaves an orphan holding nothing but CPU-idle threads. Evidence: `<project>/.tools/b2067/logs/
  c-test.log`, `hang-server-tests-sample.txt`, `hang-server-tests-lsof-inet.txt`. Cause UNMEASURED.
- The release guard's landed `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` line (owed 2) is
  unchanged by this lane.

## Still open after this lane (none built; the coordinator's choices)
- No TLS listener (Q1 "a"); a TLS callback listener, if the Azure step needs one, waits on the development CA on the
  device (first-run step 3, owed 103).
- The admin-name refusal reads names, not values (named in the lab README's Limits; Q2 "a").
- Gate B2058 FOUND 1 (five `IsServiceEnabled` shapes HP's schema refuses still read) and FOUND 2 (a relative link
  through another link and `..`): named as known in both READMEs, not changed (Q3).
- The binary echoes and every other Test operation: not built.

## Added by the gate (MEASURED; see VERDICT.md)
- FOUND 1 Minor: the sync reader takes non-ASCII white space (a no-break space) beside the result as white space; HP's
  schema refuses it.
- FOUND 2 Minor: the callback reader passes bodies HP's schema refuses (text or an attribute beside `message`, an
  attribute or `xsi:nil` on `AsyncEchoStringComplete`, `xsi:type="xs:int"` on `message`); README sentences over-claim.
- FOUND 3 Minor: a `--callback-host` whose address would exceed 256 characters passes the parser and ends the run with
  an unhandled `ArgumentException` after the run folder is made (no summary; nothing sent).
- FOUND 4 Minor: a delay longer than the wait (async) or the time-out (sync) is accepted, and the run then ends exit 13
  or 8 with words that blame the path or the device.
- FOUND 5 Info: the listener reads one connection at a time (idle connections use up the wait; 16 quick requests end
  it; a 17th, even the real callback, is neither read nor listed); `--callback-bind 0.0.0.0` is accepted and listens on
  every interface; on macOS a listener on 127.0.0.1:P starts while another program holds 0.0.0.0:P.
- FOUND 6 Info: envelope-level shapes outside HP's element schema (text in `Body` or `Envelope`, an element after
  `Body`) are read, as the landed readers read them; the library's `Oxpd1Echo` sends whatever value the client's
  setting names, so a client built on the admin setting would send the admin password under the user `guest` (the lab
  verb cannot: exit 12 and exit 2 hold).
