OXPd 2 print path, the IPP transport (WP1.7 part). One commit, `ea0df6c0`, on `da8d64a8`. Seven files are added
(six under the new `src/Datasec.Suite.Jobs.Transport/`, one test file) and three change (the Jobs `README.md`, the
Jobs test project's `.csproj`, one `ProjectReference`, and its lock file as the restore wrote it). No `.cs` file of the
job library, no package, no workflow, no `Directory.*` file and no `Datasec.Suite.slnx` line changes.

## Why

- `PrintJobSender` writes every request through an `IIppTransport`, and the job library held no implementation of it.
- The job library's cells L04 and J04 forbid `System.Net.Http` and `System.Net.Sockets` in that assembly, so the
  transport is its own assembly, referencing the job library only.

## What changed

- `HttpIppTransport`: one POST of `application/ipp` per request to the host, port and path of the printer address
  (`ipps://host:port/path` or `https://`), over its own `SocketsHttpHandler`: `UseProxy = false`,
  `AllowAutoRedirect = false`, no cookie, no decompression, `PooledConnectionLifetime = TimeSpan.Zero` and
  `Connection: close`, HTTP/1.1 exact.
- TLS trust is a pin only (`HttpIppTransport.cs:44`, `:171` to `:180`): the SHA-256 of the presented leaf certificate,
  compared in fixed time; a null certificate is refused; the chain is not consulted.
- The address check (`:115` to `:135`): plain `ipp`/`http` refused before any connection; any other scheme, no host, no
  port, user information, a query or a fragment refused.
- The body is the sender's write, streamed chunked, written at most once (`IppRequestContent`). Only a 200
  `application/ipp` HTTP/1.1 answer is handed back. Every failure of the exchange is one `IppTransportException`
  (7 reasons) with a fixed message and no inner exception.
- Cells N01 to N15 (30 cases) against a TLS stub printer (Kestrel) on 127.0.0.1, with certificates made in the test.

## What proves it

- Red first (macOS arm64): the cells with a permissive first shape (accept-all, redirects followed, plain HTTP,
  HTTP/2 offered, buffered body, any answer) at `da8d64a8`: 1839 total, 18 failed, all `HttpIppTransportTests`, each by
  an assertion. With the change: 1839 / 0 / 1835 / 4.
- 10 mutants, each red on exactly its cells, each undone.
- The branch's own push run: linux 1835 succeeded, windows 1818 succeeded (the first TLS listener this repository's
  tests have run, green on both), rules 560 files, secret scan clean.
- Merged with main `e193fb63` (TA and the lab tool landed): no conflict; 1904 / 0 / 1900 / 4 locally; rules 587.

## Still open

- No printer has answered this transport: the port and path a model answers IPP on, chunked bodies and HTTP
  authentication there are not measured.
- The transport project is not in `Datasec.Suite.slnx`, so the Release solution build compiles it as Debug (on both
  hosted legs as well): the tests run against a Debug build of it. Owed: its solution line.
- `IppTransportError.ConnectFailed`'s comment says it covers the connect bound passing; a handshake that never
  completes ends as `Failed` within the bound. A caller's own cancellation leaves as the platform's
  `TaskCanceledException`, not an `IppTransportException`. Owed: two sentences of text.
- A link-local IPv6 address loses its zone id in the target address (`Uri.Host` drops it).

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the separate assembly, the leaf pin,
one connection per request, no proxy. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
