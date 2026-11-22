# FOR RECORDS: OXPd 2 gateway stub connection race fix (lane C7F, kit B1961, seat X44), gate G2 round 1 of 2 of lane C7F, reader B1963

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this lane and every choice inside it (kit B1961 Q1 = a in words
at its stamp S4; Q2 to Q6 the defaults) and the landing order (this lane first, lane A2-F2 after). Nothing here says the
product owner decided, ruled or approved anything about this lane (kit B1961's CLARIFICATIONS greps for the subject
words counted 0, RELAYED).

## State at this gate

- Verdict GO at `aa80178a` on main `5b66a7b1` (round 1 of 2 of lane C7F). Lands as ONE squash, first (landing.txt in
  this folder): C# totals +1 on both legs (1786), skipped 4 / 21 unchanged, RULES 553 unchanged, unit tests 111, floor
  111. The merge with main `5b66a7b1` is the head's own tree `ab0873b2` (main has not moved off the parent).
- **The race found and closed (diagnosis B1955):** a hub send between the server's handshake answer `{}` and the
  connection's add to the lifetime manager reaches nobody, and nothing is kept for that connection. MEASURED at this
  gate on the shipped framework the runners load (ASP.NET Core 10.0.15, `Microsoft.AspNetCore.SignalR.Core` file
  10.0.1526.53008, commit `8e0f8ed2`; the hosted legs install SDK 10.0.404 and find runtime 10.0.15 already present,
  read in the head's job logs): the IL order is `HandshakeAsync` -> `HubLifetimeManager.OnConnectedAsync` (=
  `HubConnectionStore.Add`) -> `RunHubAsync` -> `HubDispatcher.OnConnectedAsync` -> `Hub.OnConnectedAsync`, the same as
  the release/10.0 source the diagnosis read; behaviourally the connection was among those a send reaches at the hub's
  `OnConnectedAsync` in 1000 of 1000 connections, and with a manager doing one reflection read before its add a client
  read `{}` before the add in 3 of 1000 (0 of 1000 with the framework's own manager): the gap exists natively on the
  shipped runtime, rare on an idle macOS host.
- Closed in the cell by the hub's own count and `WaitForConnectionsAsync(2, ...)` before the first send. Red first
  repeated by this gate: at `5b66a7b1` + the seam, the new late cell red in 20 of 20 runs by C7's own message, the
  unchanged C7 green in all 20; the head green 30 of 30; 4 mutants each red on exactly its cells.

## From this gate (for the backlog)

1. **Still not reproduced: the hosted Windows failure itself** (run 45052136167, job 137299375943). That its gap is the
   seam's gap is DERIVED from the framework's order (now read in the shipped IL, not only the source branch) and the
   run's shape. One hosted run of each leg of the head is green; no hosted loop was run (kit Q5: not in this lane).
2. **The seam's named limit:** the count only rises. A connection that drops after its add and before a send is still
   counted, so the wait can pass while that send reaches only the other connection. Not reachable in any cell
   (DERIVED): no cell closes a client before a send, and the server's own closes need the handshake timeout (15 s, only
   before a handshake) or the client timeout (30 s) (MEASURED: `HubOptionsSetup` defaults on 10.0.15), both past the
   cells' 10 s guard. A future cell that disconnects and reconnects would need a count that also falls.
3. **The late cell's cost:** MEASURED in one local run 1.065 s against C7's 0.293 s (about 0.8 s more), inside the same
   test class; the Contracts assembly 4.8 s locally. Hosted Contracts times vary too much to see it (head 30.9 s linux,
   26.4 s windows; diagnosis B1955: p50 20.5 s, p90 42.5 s over 62 green runs, RELAYED).
4. **The seam is off by default (MEASURED by effect):** in 20 red-loop runs at BASE + the seam, C7 (zero step) stayed
   green while its late twin was red, so the zero-step path runs the framework's own manager. Only
   `GatewayStubTests.cs:70` passes a step above zero (`git grep` at the head).
5. **Census re-run (MEASURED):** `HubTestClient.ConnectAsync` is called only at `GatewayStubTests.cs:85` and `:86`; the
   one hub send is `GatewayStub.cs:166`; no other file in `src/` or `tests/` names SignalR, `IHubContext` or a hub
   connection (the only other `SendCoreAsync` is the Graph client's own private method, not a hub). No other cell of
   any suite sends to a hub connection.
6. **Kit pointer drift (no effect, RELAYED from the seat and re-printed):** kit B1961 BLUF item 2 cites `:62` and `:68`
   for the two cells' calls of the shared body; at the head those are the declarations, the calls are at `:64` and `:70`.
7. **Carried, not in this lane (RELAYED from kit B1961):** what the real customer gateway answers to a body with no realm
   (UNMEASURED, gate B1830 FOR-RECORDS 7d); the Contracts suite's other cells; Q5 (a hosted Windows loop of C7) as a
   possible lane of its own, needing a workflow line.
8. **UNMEASURED:** every probe on Linux and Windows (the gate ran on macOS arm64 only); the ASP.NET Core shared framework
   version the hosted test hosts load (DERIVED 10.0.15 from the install lines: runtime 10.0.15 and SDK 10.0.404 found
   already installed; no runner line prints the ASP.NET Core version); CodeQL on the pull request.
