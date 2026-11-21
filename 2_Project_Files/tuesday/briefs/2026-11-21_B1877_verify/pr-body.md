Adds the OXPd 2 adapter beyond its generated clients (work package WP1.2, in part), in two commits: the adapter, and
a fix commit for concurrency, `Forget`, a throwing body stream and the grant's memory. The host does not use the
adapter yet: nothing outside its own folder and its test project references it, and the server's published output is
unchanged (release guard 10 and 11 files).

## Part 1: `Device/`, the server's calls to a printer

- `DeviceTokenHolder` keeps, per device serial, the access value in memory only (zeroed when replaced or forgotten)
  and a state; the refresh value lives only in the vault (`IDeviceSecretVault`). `SolutionTokenHandler` (one per
  device, a delegating handler) adds the access value to each request.
- A refresh happens before the first call when no access value is held, and after a 401; never on a timer. On a 401
  the handler refreshes once and sends the same request once more; a second 401 marks the device `NeedsRepair`, and
  no call goes out until an operator stores a new refresh value. Every other status passes through.
- Refreshes of one serial run one at a time. A request that waited for a refresh (after a 401, or because it found
  no access value while a refresh ran) uses that refresh's result, its access value or its failure; it refreshes for
  itself only when no refresh completed after it looked. Concurrent 401s, and requests that arrive during a refresh,
  cause one refresh.
- A grant that carries a new refresh value is written to the vault first; only then is the new access value kept and
  used (a failed write drops it: `VaultFailed`). A `SolutionTokenGrant` copies both values when it is made and refuses
  an empty access value or one holding a byte outside 0x21 to 0x7E.
- Each refresh is bounded by `RefreshTimeout` (default 30 seconds). `Forget` zeroes the held access value and deletes
  the refresh value; a refresh in flight when `Forget` runs stores nothing for the serial and ends `NoRefreshValue`.

## Part 2: `Callbacks/`, the printer's calls into the server

- `CallbackCredentials.Issue` draws 32 random bytes and returns them once as 43 base64url characters; only their
  SHA-256 is stored. Issuing again rotates; `Forget` deletes the vault record first, then the cached hash. Each takes
  effect for every check that starts after it returns, whatever a concurrent check is reading from the vault.
- `Verify` accepts exactly `Bearer` (any letter case), one space and the 43 characters, and compares hashes in fixed
  time; an unknown serial is compared with a random value, so the comparison is the same work.
- `Oxpd2CallbackHandler.HandleAsync` handles five operations (Authentication `POST /prePromptResult`,
  `/postPromptResult`, `/signoutNotification`; UsbAccessories `POST /registration`, `/operationCallback`) in this
  order: the credential before any member of the body is touched; the operation; the content type; a bounded read
  within `BodyReadTimeout`; the generated parser only; a stale-read guard on card reads; the sink under
  `AnswerTimeout`; the answer parsed again before it is returned. Fourteen typed outcomes; the new last one,
  `BodyFailed`, is a body stream that throws while it is read. `HandleAsync` throws nothing but
  `ArgumentNullException` and the caller's own cancellation.

## Limits, stated plainly

- `StoreRefreshValue` during a refresh: that refresh's result still follows it, and a request that waited for that
  refresh gets the same result (after `Forget` and a new store during one refresh, both end `NoRefreshValue`; the
  next request refreshes with the stored value).
- An access value handed out before `Forget` may still be sent once by the request that holds it.
- The vault call of a rotation and of `Forget` runs under that serial's lock, so a slow vault holds the serial's
  other requests for its duration (not measured with a real store).
- The vault lookup is not the same work: a serial with no cached hash reads the vault on every call, while a known
  one is served from memory, so whether a serial is enrolled may be told by timing (the serial is not a secret).
- Issue taking effect against a concurrent vault read is held by two mechanisms, so no single test pins the
  generation step inside `Issue`.
- A vault read that a credential check does not cache (another check filled the cache first, or `Issue` or `Forget`
  ran during the read), and a stored hash of the wrong length, are dropped without being zeroed. Each is the SHA-256
  of a credential, not the credential, and the same digest is held in the cache anyway.
- A refresh answered after `RefreshTimeout` is discarded, a rotated refresh value with it, and an endpoint that
  ignores its cancellation token overlaps the next refresh. If a device invalidates the old refresh value when it
  rotates, the device then needs repair (not measured). The endpoint should honour its token and copy the refresh
  value it is given, which the holder zeroes when the refresh ends.
- A 401 that arrives after a failed refresh gets that failure without a new endpoint call.
- A stored callback hash of the wrong length is read as an unknown device (`Unauthorized`), not as `Unavailable`.
- The holder zeroes the array the vault's `TryGet` returns, and the credential cache keeps and later zeroes it: a
  vault binding must return a fresh copy.
- `CallbackCredentials` caches each hash it reads: a rotation made through another instance is not seen by this one.
- The vault and token-endpoint bindings, how the host learns a device's serial, and what a device puts in the
  `Authorization` header of its callbacks are the host's and not measured; solution notifications, job statistics,
  user policy and the scan target are not handled.

## Tests and checks

57 new tests in the adapter's test project (1248 on the branch). No package, lock file, workflow or build line
changes; no generated code or contract test changes. The fix commit adds one test file and changes six files of the
adapter. Nothing is deployed; nothing was sent.
