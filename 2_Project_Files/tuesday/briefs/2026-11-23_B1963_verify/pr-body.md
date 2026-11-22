Follow-up of the gateway stub's lane (WP0.4, pull request 6). One commit, `aa80178a`, on `5b66a7b1`. Two existing files
change, both under `tests/Datasec.Suite.Contracts.Tests/`: `GatewayStub.cs` (+98 -2) and `GatewayStubTests.cs` (+15 -1).
No file is added, and no `src/` line, package, project, lock, solution or workflow file changes.

## Why

- Contracts cell `GatewayStubTests.C7_one_send_reaches_every_connection_once_and_bad_bodies_send_nothing` failed once in
  63 hosted Windows runs that held it ("no hub message arrived within 5 s"); Linux was green in all 63.
- The test client treats the handshake answer `{}` as connected, and the cell POSTs `/api/send` right after both
  connects. The SignalR server writes that answer before it adds the connection to the ones a send reaches
  (`HubConnectionHandler<THub>.OnConnectedAsync`: `HandshakeAsync`, then `HubLifetimeManager<THub>.OnConnectedAsync`,
  which is `HubConnectionStore.Add`, then `RunHubAsync`, which calls the hub's own `OnConnectedAsync`; read in the IL
  of the shipped `Microsoft.AspNetCore.SignalR.Core` 10.0.15). A send in that gap reaches nobody and nothing is kept
  for the connection, so no longer wait can fix it.

## What changed

- `PrinterHub.OnConnectedAsync` (`GatewayStub.cs:30`) counts each connection in a per-stub singleton `HubRegistrations`
  (`:38`, registered at `:108`); `GatewayStub.WaitForConnectionsAsync(int, CancellationToken)` (`:142`).
- The shared C7 send body awaits `stub.WaitForConnectionsAsync(2, guard.Token)` after both connects and before its
  first send (`GatewayStubTests.cs:89`). The 5 s read window and the 10 s guard are unchanged; no retry, no poll.
- A test seam, off by default: `StartAsync(..., TimeSpan lateRegistration = default)` (`GatewayStub.cs:102`) registers
  `LateRegistration` (`:183`, a subclass of the framework's `DefaultHubLifetimeManager<PrinterHub>`) only when the step
  is above zero; it adds the k-th connection k steps late. Every other caller gets the framework's own manager.
- One new cell, `C7_one_send_reaches_every_connection_once_when_the_hub_adds_each_connection_late`, runs the C7 body
  with a 500 ms step. The `HubTestClient` doc says a handshake answer does not mean the connection is added.

## What proves it

- Red first (macOS arm64): the seam and the new cell alone at `5b66a7b1`: 1786 total, 1 failed, the new cell, by
  `no hub message arrived within 5 s`; the Contracts executable alone red in 20 of 20 runs, the unchanged C7 green in
  all 20. With the change: 1786 / 0 / 1782 succeeded / 4 skipped; the Contracts executable green 30 of 30.
- 4 mutants, each red on exactly its cells: the wait removed, a wait for 1, a count check that never holds back (the
  new cell, by the 5 s message), the hub never counting (both send cells, by the 10 s guard's cancellation; no hang).
- On the shipped 10.0.15 framework, over 1000 connections: the connection was among those a send reaches every time
  the hub's `OnConnectedAsync` ran (1000 of 1000); with no delay at all, a client still read `{}` before the add in
  3 of 1000 connections when the manager did one small read before adding.
- The branch's own push run: linux (1786, succeeded 1782), windows (1786, succeeded 1765), rules (553 files, 111 unit
  tests) and secret-scan green. This pull request's own checks are the ones that count.

## Still open

- The hosted Windows failure itself is not reproduced on a runner; that its gap is this gap follows from the framework's
  order and the run's shape. One hosted run of each leg is the only hosted proof; no hosted loop was run.
- Named limit: the count only rises, so a connection that drops before a send would still be counted. No cell drops a
  connection before a send, and the server's own closes need 15 s or 30 s, past the 10 s guard.
- The late cell costs about 0.8 s more than C7 in one local run (1.07 s against 0.29 s).

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the hub's own count and the wait for 2,
the seam kept off by default with one permanent cell, the 500 ms k-step. No choice in this change is the product
owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
