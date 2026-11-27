Test support and three README lines. One commit, `09b60507`, on `main` `760e1a64` (behind 0, ahead 1). Five files,
all changed, none added: the Server tests' `HostRig.cs` and `HostCellTests.cs`, and the README of the Jobs transport,
the OXPd 1.x client and the lab tool. No product code, no package, no lock file, no project file, no
`Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- A whole-solution `dotnet test` on macOS arm64 has hung in `Datasec.Suite.Server.Tests` with no result until the
  runner's own bound. The host's start and stop took no token and no cell had a time bound, so a start or stop that
  does not end would be a run that does not end rather than a red cell.
- Three device-facing HTTP handlers set no certificate chain policy, while the OXPd 2 device token client sets one with
  downloads off. Their READMEs did not say so.

## What changed

- **One helper.** `HostRig.BoundedAsync(step, bound, what)` hands the step a token that one clock cancels at the bound,
  waits until the step ends or the token is cancelled, then asks one question: is the token cancelled? Yes is a
  `TimeoutException` with the message `the host's <what> did not end within <seconds> s`, whatever order the step's
  end and the bound came in; no passes the step's own end on unchanged.
- **Its two uses.** `HostRig.StartAsync` runs the host's start through it (`start`); `DisposeAsync` runs the host's
  stop and its disposal through it as one step (`stop`); each under 60 s. Every landed Server cell that starts a host
  (13 of 16) is bounded this way with no line of it changed.
- **Two test seams and a settable bound,** used only by the new cells: an optional `beforeStart` of `StartAsync`, a
  settable `BeforeStop`, and `StepBound`.
- **Two cells.** H17 pins the helper in seven shapes (a step that ends; one that never ends; one that reads the token;
  one already ended by the token before the helper waits; its own timeout, another exception, a cancel by another
  token each left unchanged). H18 pins the two uses (a start and a stop that never end each end at a 1 s bound as the
  timeout that names them; a host started without a bound has 60 s and answers `/health`). Every wait of both cells
  sits under an outer 20 s wait, so a removed bound is a red assertion, never a hang.
- **README lines.** One Limits bullet each in `src/Datasec.Suite.Jobs.Transport/README.md`,
  `src/Datasec.Suite.Adapters.Oxpd1/README.md` and `src/Datasec.Suite.Lab/README.md`: the handler sets no
  `CertificateChainPolicy`, so nothing there turns certificate downloads off; whether the platform fetches an issuer
  certificate or a revocation list during the handshake is UNMEASURED on every platform. The lab line names the three
  handlers the tool uses.

## What proves it

- The Server tests `Total: 18, Failed: 0` locally; the whole solution `total: 2433`, `failed: 0`, `succeeded: 2429`,
  `skipped: 4`; the branch's push run: linux `succeeded: 2429`, windows `succeeded: 2412`, rules 679 files,
  `Ran 117 tests`, secret scan clean.
- Seven mutants of the helper and its uses, each turning its cells red and nothing outside them, run twice
  independently: the wait not ended at the bound; no clock; the decision by the step's completion; the step's own end
  wrapped; the step's own end dropped; the start unbounded; the stop unbounded. The decision by completion fails on the
  shape whose step is already ended by the token, in every run.
- Extra probes, not committed: 40000 calls of the helper leave no timer or memory behind; a step that throws before it
  returns a task leaves its own exception; two hosts in one cell each keep their own bound.

## Still open

- **The hang this was written for is not caught by it.** The one hang met while building this change (a whole
  `dotnet test`, the Server tests unfinished for 1800 s, no cell red) and the two met earlier share one shape in the
  host's native samples: one thread-pool thread blocked on a contended lock inside a method invoked by reflection. A
  blocked call is not an await, so no await-bound ends it. Its cause, its method and its lock are UNMEASURED; the next
  step is a managed stack read.
- The start bound covers the host's own start only: the temporary folder, the throwaway key and certificate, building
  the host, and the read of its addresses after the start are not bounded; neither is the folder delete after the stop.
- A start or stop that blocks its calling thread, and a hang in a cell's body, are not bounded. A timed-out host (its
  threads, its temporary folder) is left to the test process until it ends.
- The chain-policy option (the same policy in each handler) is not built; a fetch during the handshake is UNMEASURED
  on every platform.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (the bound in `HostRig` rather than a
test-platform time-out on each cell; 60 s; the stop and the disposal as one step; the helper's one question; the
frozen test-support and README text; new cells only; one README bullet per module with the contrast clause; no local
CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to or run against any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
