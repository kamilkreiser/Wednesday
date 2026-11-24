# FOR RECORDS: lane L2 (kit B2049, seat X64), the library follow-ups (owed 79, 87, 83, 84 parts 1 and 3), head 77641b0e (gate B2051)

For the records lane only, after the landing; nothing here is written into a project file by the gate. Who decided every
choice of this lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE AUTHORITY;
CLARIFICATIONS.md counts 0 on every subject of the lane, RELAYED from the drafter; S4 states Q1 "a" and Q2 "a" in words as
Tuesday's decisions).

## Ticks (the kit's FOR RECORDS, RELAYED, checked by the gate against the head)
- **Tick 79.** The OXPd 2 device token client refuses a device root whose path is not `/` (`InvalidArgument`, cell DA17;
  `DeviceTokenClient.cs:48` to `:49` at the head) and builds the TLS chain with certificate downloads off and revocation
  off (`:83` to `:87`; cell DA18, red on main's own settings). Both halves of the item's "until both land" are in.
  Named limit: what a platform fetches with the policy is UNMEASURED on Linux and Windows (macOS: see the gate's
  measurements below).
- **Tick 87.** One README bullet in the adapter's "Limits of the generated reading" (`README.md:213` to `:219`); the 16
  generated summaries are unchanged.
- **Tick 83.** The doc comment of `IppTransportError.ConnectFailed` (`IppTransportException.cs:13` to `:15`) and two
  transport README sentences (`README.md:28` to `:38`); the code is unchanged (no mapping to `ConnectFailed`). See the
  gate's FOUND 2 (a platform word missing from two of these sentences): a text follow-up, not a reopening.
- **84 stays `[ ]`.** Parts (1) and (3) landed (the clause "while the vault answers", the `503` sentence, the rewrap of
  line 25: 63 words before and after, equal in order, the gate's program); **part (2), the framework's Debug line on a
  malformed header, stays open** (the logging work's). Note for the item: the new `503` sentence is narrower in truth than
  in words (the gate's FOUND 1).

## Named limits (the kit's H3, H4, H8, H9, H12, H16 and the seat's H17; RELAYED, with the gate's corrections)
- H3: `//` and `///` refused; `/./`, `/../`, `/a/..`, `/%2e/`, `/%2E%2E/`, `/.%2E/`, `/.`, `/..` normalised by `Uri` to `/`
  and taken (MEASURED); **a backslash right after the authority (`https://host:port\`, `https://host:port\base\`) makes
  `new Uri` throw `UriFormatException`** (MEASURED; the kit had DERIVED "turned into `/` then refused"). Fail closed.
- H4: IPv6, a default port with or without the slash, a trailing-dot host, an upper- or mixed-case scheme: taken
  (MEASURED). `https://@host/` (empty user information) is taken too (MEASURED; not on the wire, DERIVED).
- H8: Linux and Windows fetch behaviour with the policy UNMEASURED. H9: renegotiation, stapling, HTTP/2 UNMEASURED.
- H12: a read of the returned body stream after `SendAsync` returns is the caller's; also an exception from
  `ReadAsStreamAsync` inside `SendAsync` (`HttpIppTransport.cs:94`, rethrown at `:96` to `:100`) leaves as it is, not as an
  `IppTransportException` (DERIVED, the gate).
- H16: a caller's buffering handler bounds the read with `HttpClient.Timeout` (DERIVED).
- H17 (seat): the seam returns the handler's live options (now MEASURED, below); DA17's "0 connections" cannot fail
  (the constructor never connects, even on main).
- Local CodeQL not runnable on this Mac (no Rosetta): the pull request's code scanning is the CodeQL read of this change.

## Changed by the gate's measurements (MEASURED, gate probe, macOS arm64, .NET 10.0.404, the cells' TLS stub on 127.0.0.1)
- 40 root spellings: 0 taken whose `AbsolutePath` is not `/`; 6 taken spellings called: 6 requests, all to
  `/cdm/oauth2/v1/token`.
- The chain built in the client's own handshake (read inside the pin callback, wrapped through `TlsOptions`): revocation
  `NoCheck`, downloads disabled `True`; a wrong pin `TlsFailed` with 0 requests; the issuer-never-sent leaf taken.
- `CertificateRevocationCheckMode` is NOT read when a chain policy is set: mode `Online` with policy `NoCheck` built a
  `NoCheck` chain; mode `NoCheck` with policy `Online` built an `Online` chain. The landed mode line has no effect now
  (a gate mutant removing it survived all cells, DA18 included: its assertion reads the type's default).
- Fetches to an AIA (issuer and OCSP) and CRL address on 127.0.0.1 during the handshake: 0 in each of 5 variants (as
  built twice, main's settings, no policy with mode `Online`, policy with downloads ON and revocation `Online`); control
  (a direct connect) counted 1. So on macOS the policy changes nothing measurable; the README's "with the policy ...
  UNMEASURED" is now measured for macOS (0), still UNMEASURED on Linux and Windows.
- `TlsOptions` is the handler's own `SslOptions` (the same object on two reads; a callback set through it before the first
  send ran in the handshake). After the first send, a callback set through it did not run, but a change to its
  `X509ChainPolicy` object reached the next connection's chain. Internal, two test assemblies only; no production reader.
- `CallbackCredentials.Verify` with a vault that throws: a serial issued in this instance (cached) gives `false` (401) for
  none, one wrong or a malformed header; a fresh instance (uncached) throws (503); a serial outside the rule gives `false`
  without a vault read.

## For a later round of lane L2 or a text pass (VERDICT.md FOUND 1 and 2, both Minor; text only)
- Server README `:23` to `:25`: say that a vault that throws makes it `503` for a serial whose hash is not cached in the
  process; a cached serial is judged without the vault (`CallbackCredentials.cs:170` returns the cached hash before the vault read at `:178`).
- Transport README `:34` to `:35` "(measured: a `TaskCanceledException` ...)" and `IppTransportException.cs:13` to `:15`
  ("is `Failed`, not this"): add "on macOS arm64" (the reader's probes P06 to P08 ran there; other platforms UNMEASURED).

## Candidates for the owed list (Info, not this lane's)
- The other device-facing `SocketsHttpHandler`s have no chain policy: `Oxpd1Client.cs:44`, `HttpIppTransport.cs:33`,
  the lab's `DeviceChannel.cs:52`. Owed 79's Linux and Windows fetch concern applies to each (UNMEASURED); the transport
  README's "the chain, its errors and revocation are not consulted" is silent on downloads.
- The landed `CertificateRevocationCheckMode = NoCheck` line in `DeviceTokenClient.cs:82` is dead beside the policy
  (keep or drop: the kit's Q2 alternative c).
