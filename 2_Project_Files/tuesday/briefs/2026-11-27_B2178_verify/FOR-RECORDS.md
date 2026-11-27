# FOR RECORDS: lane OX-C kit 2 part 2 round 1 of 2 (kit B2170, seat X89), head 09b60507 (gate B2178: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2170 THE AUTHORITY; owed 121 names "the coordinator's choice" in the owed list's own words,
RELAYED; stamp S4 states Q1 and Q3 "a" in words). Nothing here ran against a device.

## Owed 121: CLOSE on this squash, by its README-line option
The README of the Jobs transport, the OXPd 1.x client and the lab tool each say that no handler there sets a
`CertificateChainPolicy`, so nothing there turns certificate downloads off (the OXPd 2 device token client sets a
policy with downloads off), and that a fetch of an issuer certificate or a revocation list during the handshake is
UNMEASURED on every platform. CHECKED by the gate at 09b60507: one `SocketsHttpHandler` per module
(`HttpIppTransport.cs:33`, `Oxpd1Client.cs:49`, `DeviceChannel.cs:52`), the policy words on 0 lines of the three
modules, no `new X509Chain`, the lab makes no other handler. The chain-policy option (the same policy in each handler)
is not built; it stays the coordinator's to commission (kit NOT DECIDED 2). Note (gate F6, Info): the transport's
handler sets `CertificateRevocationCheckMode = X509RevocationMode.NoCheck` (`HttpIppTransport.cs:43`), which its new
line does not mention.

## Owed 137: the bound it names LANDS; the hang it was filed for is NOT caught (gate F1)
- What lands (RELAYED from the kit, CHECKED by the gate): every Server cell's host start (`app.StartAsync`) and its
  host stop with the disposal run under a 60 s bound in the tests' `HostRig` (`BoundedAsync`, one clock, one question
  after the wait), so a start or stop that does not end AS AN AWAIT is a red cell whose message names the step; cells
  H17 (seven shapes) and H18 (the two uses through two test seams) pin it; seven mutants turn them red (MATCH 7 of 7,
  run by the seat and again by the gate). The helper's first form let .NET's own timeout out once in the first pin run
  and was re-frozen before any commit.
- **What does NOT land:** the hang itself. At this head the seat's first whole-solution `dotnet test` hung in
  `Datasec.Suite.Server.Tests` for the runner's 1800 s, no cell red, no `did not end within` line (seat X89's STATUS
  and `.tools/b2170/logs/chain-test.log`; the head ran green on the next run and BASE green in a new worktree). The
  gate read the three native samples of owed 137's hang (`.tools/b2067/logs/hang-server-tests-sample.txt`,
  `.tools/b2134/logs/orphan-server-tests-sample.txt`, `.tools/b2170/logs/orphan-server-tests-sample.txt`): in all
  three the one abnormal thread is a thread-pool worker blocked in `Monitor.Enter` (a contended lock) inside a method
  invoked by reflection (`RuntimeMethodHandle_InvokeMethod`), about 400 unnamed managed frames below the invoke and
  46 / 46 / 54 above it; the main thread in `Monitor.Wait`; one `Kestrel Timer`. A blocked call is not an await, so
  this bound cannot end it (the kit's named limit R7; the gate's probe G03 measured that a blocking step is reported
  only when it returns). Every occurrence so far was under `dotnet test` (the test platform's server mode), none in
  the Server executable run alone. Which method, which lock and who holds it: UNMEASURED.
- **Proposed record (the records seat decides):** owed 137's own words are "this item stays open until a bound lands
  or the cause is found". Either (a) tick 137 for the bound with this paragraph's evidence and FILE A NEW OWED ITEM for
  the hang the bound does not catch (Where: the Server tests under `dotnet test` on macOS arm64; Symptom: the three
  samples above, the one blocked lock wait; Why deferred: a managed stack read is the next step, for example the test
  platform's hang-dump extension (a package this tree does not carry) or a managed stack tool on this machine, the
  coordinator's choice since a seat downloads no tool; Discovered: 2026-11-25, seen again 2026-11-27 twice), or (b)
  keep 137 open with this evidence added. The gate recommends (a): the bound is real and tested; the hang is a
  different shape from the one the item's fix named.
- Named limits that land with the bound (kit R3b, R6, R7, R8; gate F2): a step that ends in the last instant read after
  the bound is reported late; a disposal that does not end is reported as the stop's; a call that blocks its thread
  is not bounded; a timed-out host is left to the test process; the temporary folder, the key and certificate,
  `ServerHost.Build` and the address read after the start, and the folder delete after the stop, are outside the
  bound.

## Owed 138: stays open (Q2)
A change of the heavy-job runner outside the repository (a new process group per job, ended at the bound), being
built in Tuesday's tree as B2172 (stamp S4, RELAYED). This lane met its shape once more: the orphan of the hung run
outlived the runner's bound and TERM did not end it; KILL did (seat X89's STATUS).

## Seen, not this lane's
An orphan test host of a much earlier gate (`/private/tmp/b1839-gate/clone/tests/Datasec.Suite.Sessions.Tests/...`,
six days old) was alive on this machine at the seat's read (RELAYED from its STATUS); untouched by the seat and by the
gate.
