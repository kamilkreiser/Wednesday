OXPd 2 server-to-device trust step (WP1.2 part). One commit, `4d4e933c`, on `da8d64a8`. Nine files are added (eight
under `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/`, one test file) and two change (the adapter `README.md` and the
doc comment of `Device/IDeviceSecretVault.TryGet`). No project, lock, package, solution or workflow file changes, and
no existing public member changes.

## Why

- The token holder (`Device/DeviceTokenHolder`, pull requests 13 and 28) refreshes through an `ISolutionTokenEndpoint`
  that nothing in the repository implemented; the README called it "the host's". The onboarding order of the
  architecture also needs the administrator password grant and the install-code exchange against the device itself.
- The adapter's one network rule (cell L03) forbids a `System.Net.Sockets` or logging reference, not HTTP; the adapter
  already sends HTTP (`SolutionTokenHandler`, the generated clients). So the client lives in the adapter, where the
  product server can use it.

## What changed

- `DeviceTokenClient`: one form-encoded POST per call to the device root plus `TokenPath` (default
  `/cdm/oauth2/v1/token`), over its own `SocketsHttpHandler` with `UseProxy = false` and `AllowAutoRedirect = false`
  (`DeviceTokenClient.cs:69`, `:70`). TLS trust is a pin only: `CheckPin` (`:177` to `:186`) compares the SHA-256 of
  the presented certificate with `PinnedCertificateSha256` in fixed time, whatever the chain and name errors say.
- Three grants: `RequestAdminAccessAsync` (`grant_type=password`; `DeviceAdminAccess`, memory only, zeroed by
  `Dispose`), `ExchangeInstallCodeAsync` (`grant_type=authorization_code`, `client_id=com.hp.cdm.client.hpE2Solution`,
  `refresh_token_requested=true`; refused with nothing sent past `InstallCodeWindow`, `:120`), `RefreshAsync`
  (`grant_type=refresh_token`, the same `client_id`).
- Strict answer reading: status 200, at most `MaxAnswerBytes` read, a JSON object with no repeated name, values of
  bytes 0x21 to 0x7E, `expires_in` a whole number above 0; 400 and 401 refuse, any other non-200 is
  `UnexpectedStatus`, a 3xx is `Redirected` and never followed; every call bounded by `RequestTimeout`.
- `DeviceSolutionTokenEndpoint`: the holder's endpoint over the clients an `IDeviceTokenClientSource` finds by serial;
  a refusal is null (`NeedsRepair`), any other failure throws (`RefreshFailed`); it reads the refresh bytes before it
  returns its task, so the holder's `finally` zeroing cannot change what is sent.
- README: Part 3, the rewritten endpoint sentence of Limits, the holder's `finally` limit and a block of the client's
  limits; `TryGet`'s fresh-copy sentence.
- Cells DA01 to DA16 (28 cases) against a TLS stub on 127.0.0.1 that the tests start, with throwaway certificates.

## What proves it

- Red first (macOS arm64): the cells with a skeleton whose members throw `NotImplementedException`, at `da8d64a8`:
  1837 total, 27 failed, all `DeviceAuthCellTests` (DA16, a census the skeleton already meets, green). With the change:
  1837 / 0 / 1833 / 4.
- 17 mutants, each red on exactly its cells, and each undone.
- The branch's own push run: linux 1833 succeeded, windows 1816 succeeded (the TLS cells green on both), rules 562
  files, secret scan clean. Main has not moved since the branch was cut, so that run's tree is the merge's.

## Still open

- No device, simulator or printer has answered this client. The field names are OAuth 2.0's (RFC 6749); what a device
  answers, which of the two documented paths it serves, and whether its refresh needs the `client_id`, are not
  measured.
- A device root with a path (`https://host/base/`) is accepted, and its path is dropped: the request goes to
  `/cdm/oauth2/v1/token`, not `/base/cdm/oauth2/v1/token` (`new Uri(root, path)` with an absolute path,
  `DeviceTokenClient.cs:62`). The README's "the device root plus `TokenPath`" does not say so. Owed: refuse such a root
  or state the rule.
- Chain building before the pin check: the client turns revocation off but does not set
  `X509ChainPolicy.DisableCertificateDownloads`, so whether .NET fetches a missing issuer named in a presented
  certificate's AIA extension before `CheckPin` runs is measured on macOS only (no fetch); on Linux and Windows it is
  not measured.
- Caller cancellation leaves as `TaskCanceledException` (not a `DeviceAuthException`), as the holder expects; there
  is no cell for it.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it: the placement in the adapter, pin-only
trust, the grants' forms, the strict reading and the refusal statuses. No choice in this change is the product
owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
