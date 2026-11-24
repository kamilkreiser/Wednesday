Library follow-ups of the OXPd 2 device token client, the IPP transport, the server host and the OXPd 2 adapter. One commit,
`77641b0e`, on `main` `e2a20aef` (behind 0, ahead 1). Seven files change and none is added: `DeviceTokenClient.cs`,
`DeviceAuthOptions.cs`, `DeviceAuthCellTests.cs`, the OXPd 2 adapter README, `IppTransportException.cs` (a doc comment only),
the transport README and the server README. No package, no lock file, no project file, no `Datasec.Suite.slnx` line, no
workflow, no file under `Generated/` or `contracts/`, no OXPd 1.x file.

## Why

- A device root with a path (for example `https://host/base/`) was taken and its path dropped in silence: the token call went
  to `/cdm/oauth2/v1/token` on the right, pinned host, not to the path the setting named.
- The client's TLS handshake turned revocation off but left the platform free to download a missing issuer during chain
  building. On macOS no such fetch was seen; on Linux and Windows a fetch would let a device or a man in the middle make
  the host send one GET to an address of its choosing before the pin refuses.
- Four sentences of the transport, server and adapter text said more than the code does.

## What changed

- `DeviceTokenClient`'s constructor refuses a device root whose `AbsolutePath` is not exactly `/` with
  `DeviceAuthException(InvalidArgument)`, before any connection, beside the earlier user, query, fragment and host rule.
- The handler's `SslOptions` add `CertificateChainPolicy { RevocationMode = NoCheck, DisableCertificateDownloads = true }`
  beside the earlier `CertificateRevocationCheckMode = NoCheck`. The pin callback is unchanged: trust is still the pin alone.
- An `internal` property `TlsOptions` returns the handler's own `SslOptions` for the cells (the adapter's internals are
  visible to its two test assemblies only). No public member is added.
- Text: the doc comments of the client, its constructor and `DeviceAuthOptions.DeviceRoot` (the path rule); the adapter
  README (the root rule, the chain policy, its Limits, and the other exceptions and the body-read bound of a generated
  client); the doc comment of `IppTransportError.ConnectFailed` and the transport README (a handshake past `ConnectTimeout`
  is `Failed`; a caller's cancellation leaves as `OperationCanceledException`; a call after `Dispose` or with a null
  argument throws before anything is sent); the server README (`401` while the vault answers, a vault that throws is `503`,
  and one 209-character line rewrapped with no word changed).

## What proves it

- Red first on `main`'s own settings: the two new cells DA17 and DA18, with the test property and no other change, fail
  by assertion (`accepted /base/`; `policy set False`), the adapter's other 86 cells green. Green: 2114 / 0 / 2110 / 4.
- Four mutants, each red on exactly its cell, none surviving: the root rule taken away, downloads on, the policy's
  revocation online, the policy removed.
- 40 root spellings were tried against the constructor: none whose `AbsolutePath` is not `/` was taken. Dot segments that
  `Uri` resolves to `/` are taken and reach `/cdm/oauth2/v1/token`; IPv6, a default port and an upper-case scheme are taken.
- On macOS, the chain built during the client's handshake carries revocation `NoCheck` and downloads disabled, a wrong pin
  is still refused with no request, and a leaf whose issuer is never sent is still taken by its pin.
- The branch's push run 45332864758: linux 2110 succeeded, windows 2093 succeeded, rules 657 files, secret scan clean.

## Still open

- What a platform fetches during the handshake with the policy set is measured on macOS only (no connection to an AIA,
  OCSP or CRL address on 127.0.0.1, with or without the policy); on Linux and Windows it is not measured.
- When a chain policy is set, the platform reads the policy's revocation mode and not `CertificateRevocationCheckMode`
  (measured on macOS); both say off, so the earlier line now has no effect.
- The server README's `503` sentence holds for a serial whose stored hash is not yet cached in the process; a serial the
  host has already cached answers `401` to none, one or two lines while the vault throws.
- Two transport sentences carry a measurement without naming its platform (the cancellation's `TaskCanceledException`,
  and the `ConnectFailed` comment); the measurements were on macOS.
- The other device-facing handlers (the OXPd 1.x client, the IPP transport, the lab's device channel) have no chain policy.
- The framework's Debug line on a malformed header (part of the same server item) is the logging work's.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (refuse a root with a path rather than state
the rule; the chain policy beside the earlier revocation setting, proved through an internal property; new cells rather
than rows in an earlier cell; text only for the transport; no local CodeQL, so the code scanning of this pull request is
the CodeQL read). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.
