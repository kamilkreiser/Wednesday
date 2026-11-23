# B1983 FOR RECORDS (gate G1, round 1 of 2 of lane IP; kit B1972, seat X46; head ea0df6c0)

Who decided: every choice of lane IP (its place, its cells, its README, D1 to D7, Q1 to Q7) is the coordinator's
(Tuesday's) as coordinator; none is the product owner's. Nothing here is a customer-facing word.

## From the kit (RELAYED, kit B1972 FOR RECORDS)
- The commission's path `src/Datasec.Suite.Jobs/Transport/` cannot hold network code: cells L04 and J04 forbid it. The
  transport is its own assembly, `Datasec.Suite.Jobs.Transport`, built and tested through the Jobs test project's
  reference, with no slnx line yet (owed: its slnx line; Q2).
- The transport's trust is one leaf pin; the customer-issued device certificate checked by chain
  (`02_architecture.md:605`) is not built (a named limit).
- Named limits: no proxy path cell (H7); the HTTP layer's resend path is unreached (H11); a renegotiation is
  unmeasured (H15); a real printer's port, path, chunked bodies and authentication are unmeasured (H17).
- First TLS listener in the repository's tests: the hosted legs ran it for the first time on this lane's head
  (run 45092918591): linux `failed: 0` (1835 succeeded), windows `failed: 0` (1818 succeeded).
- Carried, not in this lane: Print-URI, priority print, Get-Printer-Attributes; a pin store and onboarding.

## Deviations of the seat (RELAYED, seat STATUS; the gate agrees with both readings)
- **D-ENV:** the volume `/Volumes/Datasec_DEV` detached and remounted at about 11:38 (`disk7s1` to `disk5s1`) during
  the seat's first mutants run; the run died at mutant 3 of 10, the stranded mutant was undone by the program, and on
  ANSWER-1 the run was made once more, whole (10 of 10 MATCH). The gate re-ran all 10 itself: 10 of 10 MATCH.
- **D-GH:** GitHub's check run 137426289705 (`rules`, head `ea0df6c0`, run 45092918591) reads `status in_progress`
  with `conclusion success` and `completed_at 2026-11-23T01:09:32Z`; its job's six steps all `success`. The gate read
  it again at 12:55 to 12:57 (still stuck) and counted the job's log by GET itself (36553 bytes): `Ran 111 tests` 1,
  `UNIT-TEST FLOOR: ran 111, floor 111` 1, `RULES: clean (560 files)` 1, `OK` 2, control 0. `hosted2.py`'s
  `FAIL 1 (check run rules not completed success)` is that status field alone: GitHub's record, not the run. Not
  re-run. A second sighting of the shape (the first: head `5cdcb806`, earlier on 2026-11-23, RELAYED from the seat).

## The gate's own, for the records seat (owed items; none filed by the gate)
1. FOUND 1 (Minor): the transport project is built in **Debug** by the Release solution build, because it is not in
   `Datasec.Suite.slnx` (MEASURED locally and on both hosted legs: `Datasec.Suite.Jobs.Transport -> .../bin/Debug/...`
   while every other project is `bin/Release`). Q2's premise that the slnx line is "hygiene only" does not hold. Owed:
   the solution line `/src/Datasec.Suite.Jobs.Transport/...csproj` by the next lane that owns slnx (L1 has landed).
2. FOUND 2 (Minor): two sentences of repository text the code does not keep: `IppTransportError.ConnectFailed`'s
   comment ("or the connect bound passed": a handshake that never completes ends as `Failed`, MEASURED) and the
   README's "Every failure is an `IppTransportException` ... never an inner exception" (a caller's cancellation leaves
   as `TaskCanceledException` with the platform's inner chain, MEASURED; no address or port in its text on macOS).
3. Named limit, new: a link-local IPv6 printer address loses its zone id (`ipps://[fe80::1%25en0]:631/...` becomes
   `https://[fe80::1]:631/...`, MEASURED); fail-closed for trust (the pin still applies).
4. Named limit, new: an HTTP/1.0 answer is refused (`response.Version != 1.1`, DERIVED); whether any printer answers
   IPP over HTTP/1.0 is UNMEASURED.
