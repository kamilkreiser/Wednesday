Host composition v0 (WP1.11 part). One commit, `685d72b6`, on `da8d64a8`. Fourteen paths, all under
`src/Datasec.Suite.Server/` and `tests/Datasec.Suite.Server.Tests/` (3 modified, 11 added). No package, no workflow
line. **This text is HELD with the pull request: it is re-cut, and every number below re-measured, in the round that
adds the test project's solution line after the Lab lane lands.**

## Why

- At `da8d64a8` the Server "maps no route" (`Program.cs:2`). The adapter's callback dispatcher says mapping its
  outcomes to HTTP statuses is the host's (`src/Datasec.Suite.Adapters.Oxpd2/README.md:75`), and binding
  `IDeviceSecretVault` to the secret store is the host's (`README.md:95`, `Device/IDeviceSecretVault.cs:5`).

## What changed

- `ServerHost.Build` (`ServerHost.cs:25`) composes the services and maps `GET /health` (`:49`),
  `POST /oxpd2/devices/{serial}/notifications` (`:50`) and `POST /oxpd2/devices/{serial}/{target}/{operation}` (`:51`).
  `Program.cs` runs it and keeps the Windows-service lifetime.
- Both OXPd 2 routes answer 403 to a request that is not HTTPS before anything else (`CallbackEndpoint.cs:15`,
  `NotificationEndpoint.cs:20`). The callback route hands the adapter the path's serial and the `Authorization` header
  only when there is exactly one (`CallbackEndpoint.cs:27`), and writes each of the 14 outcomes as a status by one
  table (`:42`). The notification route checks the credential first (`NotificationEndpoint.cs:29`), bounds the body,
  hands the bytes to a sink unparsed (`:58`) and zeroes them (`:71`).
- `SecretStoreDeviceVault` binds the adapter's vault to the local secret store, resolved at each call; each read hands
  out a new array and disposes the store's value.
- TLS certificate and addresses: the framework's `Kestrel` configuration section; no line of this change reads them.
- New `tests/Datasec.Suite.Server.Tests/` (13 cells, Kestrel on 127.0.0.1 port 0, a throwaway certificate).

## What proves it

- Red first (macOS arm64): with the shells only, 13 cells, 12 failed, each by its own assertion; green with the change:
  13 / 0. Twelve mutants, each red on exactly its cells.
- Whole solution unchanged at 1809 / 0 (the new test project is not in the solution in this commit); RULES 564; the
  release guard 14 and 15 files (the adapter and secret-store assemblies added). The branch's push run: four jobs green.
- In the solution-line round: the 13 cells on both hosted legs (the totals plus 13).

## Still open

- The one-header rule is reached by no cell on either route (measured reachable by a raw client and refused 401);
  cells owed.
- At Debug, the framework logs a malformed header line's text (category `Microsoft.AspNetCore.Server.Kestrel.BadRequests`);
  a Limits line or a log filter owed.
- The root `README.md` lines 14-15 still describe the Server before this change; owed.
- What a device sends to these routes, and what it does with each status, are UNMEASURED; no forwarded-header handling.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the route shape, HTTPS only, the status
table, the notification route's credential, no logging library, the round's sinks, and holding this pull request until
the solution-line round. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
