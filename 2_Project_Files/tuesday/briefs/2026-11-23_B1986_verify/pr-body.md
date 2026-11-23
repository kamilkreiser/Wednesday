Host composition v0 (WP1.11 part). Three commits on `cad65b86` (main): `685d72b6` (the host, its routes and 13 cells,
on `da8d64a8`), `4c415f9a` (a merge of main `cad65b86`, no hand edit: its tree is `git merge-tree`'s), `0c65be47` (five
files: the solution lines, two cells, the two READMEs). Against main: 16 files, all under `src/Datasec.Suite.Server/`
and `tests/Datasec.Suite.Server.Tests/` plus `Datasec.Suite.slnx` and the root `README.md`. No package, no workflow
line. Landed as ONE squash.

## Why

- At main the Server "maps no route" (`src/Datasec.Suite.Server/Program.cs:2` at `cad65b86`). The adapter's callback dispatcher says mapping its outcomes to
  HTTP statuses is the host's (`src/Datasec.Suite.Adapters.Oxpd2/README.md:75`), and binding `IDeviceSecretVault` to
  the secret store is the host's (`README.md:122`-`:123`, `Device/IDeviceSecretVault.cs:5`).
- The Jobs transport project was not in `Datasec.Suite.slnx`, so the Release solution build compiled it as Debug.

## What changed

- `ServerHost.Build` (`ServerHost.cs:25`) composes the services and maps `GET /health` (`:49`),
  `POST /oxpd2/devices/{serial}/notifications` (`:50`) and `POST /oxpd2/devices/{serial}/{target}/{operation}` (`:51`).
  `Program.cs` runs it and keeps the Windows-service lifetime.
- Both OXPd 2 routes answer 403 to a request that is not HTTPS, before the host's own code reads anything else
  (`CallbackEndpoint.cs:15`, `NotificationEndpoint.cs:20`). The credential is read only from a request with exactly one
  `Authorization` header line (`CallbackEndpoint.cs:27`, `NotificationEndpoint.cs:29`). The callback route writes each
  of the 14 outcomes as a status by one table (`:42`). The notification route checks the credential first, bounds the
  body, hands the bytes to a sink unparsed (`:58`) and zeroes them (`:71`).
- `SecretStoreDeviceVault` binds the adapter's vault to the local secret store, resolved at each call; each read hands
  out a new array and disposes the store's value.
- TLS certificate and addresses: the framework's `Kestrel` configuration section; no line of this change reads them.
- New `tests/Datasec.Suite.Server.Tests/`: 15 cells, Kestrel on 127.0.0.1 port 0, a throwaway certificate. H14 and
  H15 write raw HTTP/1.1 over TLS (pinned to the served certificate) with two `Authorization` lines in three shapes,
  each with a one-line 200 control (HttpClient folds two values into one line, so it cannot send them).
- `Datasec.Suite.slnx`: two lines, the Server test project and `src/Datasec.Suite.Jobs.Transport` (the transport now
  builds in Release in the solution build, on both legs).
- Server README: the 403 sentence narrowed to the host's own code, the one-header-line rule, and a Limits line for
  Kestrel's `Microsoft.AspNetCore.Server.Kestrel.BadRequests` category at `Debug`. Root `README.md:14-15`: the Server
  as it now is.

## What proves it

- Red first (macOS arm64) in the first commit: the shells only, 13 cells, 12 failed, each by its own assertion. In
  the last commit the 15 cells green; 14 mutants, each red on exactly its cells, among them `Count == 1` to
  `Count >= 1` on each route (red on H14 and H15 alone, `Expected: 401 Actual: 200`).
- Whole solution at the head (= the merge with main `cad65b86`): 1919 / 0 / 1915 / 4; at the merge commit alone
  1904 / 0 / 1900 / 4, no Server test line and the transport under `bin/Debug` (the solution lines' control).
  RULES 598; the release guard 14 and 15 files; unit tests 111.
- The branch's push run 45101722950: four jobs green; linux 1919 / 1915 / 4, windows 1919 / 1898 / 21; the Server
  test assembly `passed` on both legs (2s 686ms, 7s 684ms), the first hosted run of these cells; the transport under
  `bin/Release` on both legs.

## Still open

- With a vault that throws (for example no `Secrets` configuration), a request with none or two `Authorization` lines
  is 503, not 401 (fail closed, measured); the Server README's one-header-line sentence says 401 without that clause.
  Owed: one clause of text.
- At Debug, the framework logs a malformed header line's text, value included (now a named Limit); no host-side
  filter is set (owed to the logging work).
- The rest of the root `README.md` layout list still lists only the Core test project.
- What a device sends to these routes, and what it does with each status, are UNMEASURED; no forwarded-header
  handling.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the route shape, HTTPS only, the status
table, the notification route's credential, no logging library, the sinks, the merge of main, the two solution
lines, and holding this pull request until the solution lines were in. No choice in this change is the product
owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
