# FOR RECORDS: lane W1 (kit B2005, seat X57), `Oxpd1Writer`, first-run step 5's pair, head f039956d (gate B2008)

For the records lane only; nothing here is written into a project file by the gate. Who decided every choice of this
lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY; CLARIFICATIONS.md counts 0
on every subject of the lane, RELAYED from the drafter; S4 states Q1 "a" and Q2 "a" in words as Tuesday's decisions).

## From the kit's FOR RECORDS (RELAYED, copied)
- The OXPd 1.x adapter gained its first device-write code: `Oxpd1Writer`, the register and unregister of a sign-in agent
  (first-run step 5), each a dry run unless `Execute` is set, one request per executed call, the register's undo carried
  whenever it may have applied. Neither call has run against a device.
- Steps 2 (the Test service and a panel capture), 3 (certificate import and delete) and 4 (a button's register and
  unregister) are NOT built: their operations are in no committed file under `contracts/oxpd1/` (the drafter's count over
  the four bindings: 30 operations, none of them). They need HP's descriptions of those services committed first (a
  contracts lane), then a write lane each. **HP's committed bindings hold no operation for steps 2 to 4.**
- The guard after a refused password stays the caller's: L5's per-run guard is the Lab command's structure, and the lab
  wiring of these writes (a later lane, after W1 and LH land) reuses it; the per-device count is the shared device-trust
  component's (B1996 F16).
- Named limits: the writer counts nothing across calls (H7); a caller's cancellation returns no result and so no undo
  (H11); a dry run's envelope is not scrubbed (H15); the undo of an unregister is not offered and nothing lists what a
  session left registered (H18, B1996 F19's "confirm all undone", a later lab command); a fault's subcode is not read;
  whether a device applies a write before it refuses credentials, and every device answer, are UNMEASURED (H19).
- The client's record line reads `OXPd 1.x call` for reads and writes (it read `OXPd 1.x read`).

## Changed by the gate's measurements (MEASURED, gate probe, macOS arm64, .NET 10.0.404, raw TLS stub on 127.0.0.1)
- **H10 is no longer only RELAYED for writes.** 18 ends of an executed register (an answer; 401; 401 with a
  `WWW-Authenticate: Basic` challenge; 403; a 500 fault; a fault whose code holds the password and its Basic token; a 200
  fault; a 500 holding the empty response; a 200 with an empty body; 307; 302; an oversized answer; a time-out after the
  stub read the request; a reset; a TLS close and a TCP FIN after the request with no answer; a broken status line; an
  answer then a close), each on a FRESH connection and on a REUSED pooled connection: 36 of 36 gave exactly ONE
  password-bearing request. The FIN-after-request on a reused connection is the shape an HTTP stack may retry; it did not.
  Windows and Linux: the hosted cells only (UNMEASURED by the probe there).
- **H9 is no longer only DERIVED:** 307, 302, oversized, reset, FIN and a broken status line each end `Unknown` with the
  undo; the redirect is not followed (1 request).
- The dry run, 12 shapes: 0 connections, 0 requests, 0 setting reads, no record line written.
- The reads' envelopes are byte for byte BASE's (20 of 20: 5 rows x 2 addressing versions x 2 language codes, compared
  against BASE's built assembly by reflection).

## For a later round of lane W1 (VERDICT.md FOUND 1 and 2, both Minor)
- The undo is a restore only when the id was absent before the register (HP: a register "replaces" a record of the same
  id). A named limit in the README and, in the lab wiring, a read of `GetAuthenticationAgentRecords` before the register
  that refuses an id already on the device.
- `https://@host/...` (empty user information) is taken by the record and its body fails HP's `LimitedUri` pattern.

## For the lab wiring lane (not this lane's)
- An `oxpd1` write verb that runs ONE `WriteAsync` per run, a dry run unless `--execute`, stops on 401 or 403 with L5's
  message, prints the undo, and reads the agent records first (FOUND 2).
