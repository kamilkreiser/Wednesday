Five owed items of the other modules (the Graph layer, the OXPd 2 device token client, the Server, the Jobs transport
and the Identity card store), built and tested inside the test process only: the Graph cells against an in-process
fake handler, the Server cell against the host on 127.0.0.1 port 0. One commit, `641935b5`, on `main` `38a031e5`
(behind 0, ahead 1). Ten files, all changed, none added: `GraphClient.cs` and `GraphFailure.cs` under
`src/Datasec.Suite.Graph/`, `DeviceTokenClient.cs` under `src/Datasec.Suite.Adapters.Oxpd2/DeviceAuth/`, the Server
README, the Jobs transport README and `IppTransportException.cs`, the Identity README, and three test files
(`PagingTests.cs`, `HostCellTests.cs`, `HostRig.cs`). No package, no lock file, no project file, no
`Datasec.Suite.slnx` line, no workflow, no file under `contracts/` or `build/`.

## Why

- The Graph walk judged a loop by the next link's whole address, fragment included, so a next link that named an
  address already requested with a new fragment on each page was requested again up to the page bound (HTTP/1.1 sends
  no fragment, so the server saw the same request each time).
- The device token client set `CertificateRevocationCheckMode` to `NoCheck`, the property's own default, beside a chain
  policy that carries its own `RevocationMode`; the line had no effect and the cell that read it compared it with the
  default.
- The Server README said a vault that throws makes every check of a serial within the rule `503`; a serial whose hash
  the host holds in memory is checked without the vault.
- Two measured sentences of the Jobs transport named no platform; two citations of the Identity README pointed at lines
  that had moved.

## What changed

- **The loop key.** One private helper, `LoopKey`, is `address.GetLeftPart(UriPartial.Query)`; the walk keeps it for
  every address it requests (the first included) and compares a next link by it. The address requested is unchanged.
  The summaries of `GetPagesAsync` and `GraphFailure.PagingLoop` say "without its fragment".
- **The revocation line.** Removed, with a two-line comment; the chain policy (`RevocationMode` `NoCheck`, downloads
  off) is unchanged.
- **The Server README.** The credential sentence and the notification bullet say when a vault that throws is `503`
  (a serial within the rule whose hash the host does not hold) and when it is not (a hash the host holds: issued
  through its `CallbackCredentials`, or read from the vault once, until the process ends).
- **The Jobs transport** cancellation sentence and the doc comment of `ConnectFailed`: "measured on macOS arm64; other
  platforms UNMEASURED". **The Identity README**: `CsaStore.cs:294` in `PrefixOf` and `:311` in `BlobOf`.
- **Test support.** A `Broken` switch on the tests' in-memory secret store makes its reads throw (added lines only).

## What proves it

- Red first: on `main` with the new cells only, the Graph tests read `Total: 203, Failed: 3`, the three fragment rows,
  each by its assertion; the Server tests `Total: 16, Failed: 0` (the held-hash cell pins the sentence on the code as it
  was). Green: Graph `203 / 0`, Server `16 / 0`, the OXPd 2 adapter `88 / 0`; the whole solution `total: 2429`,
  `failed: 0`, `succeeded: 2425`, `skipped: 4`; the branch's push run: linux `succeeded: 2425`, windows
  `succeeded: 2408`, rules 679 files, `Ran 117 tests`, secret scan clean.
- Seven mutants, each turning at least its cells red and nothing outside them: the key back to the whole address (in the
  helper, at the keep only, at the compare only), a key that reads `%23` as a fragment, a key that keeps the host as
  typed, the revocation mode made `Online`, the policy's mode made `Online`.
- Seven new cases in two cells: a new fragment on every page, an empty fragment, the first address again with a
  fragment (each a loop); `%23` in a query and in a path (followed); the host in upper case (a loop); and one Server
  cell over a serial held by an issue, one held by a vault read, one not held (none, one and two header lines, both
  routes), one outside the serial rule, and the store answering again.

## Still open

- Nothing here has run against a device.
- Two addresses that differ in their text are two keys (parameters in another order, a trailing slash): the page bound
  ends such a walk. An explicit `:443`, `%41` for `A`, the host's or scheme's letter case and dot segments are .NET's
  canonical form, the same before and after this change.
- The host keeps a hash until the process ends: a credential re-issued, or a device forgotten, by another process over
  the same vault is not seen by a running host until it restarts (the re-issued credential is refused; the older one
  still passes).
- Owed: a host-side filter for the framework's Debug line on a malformed header (the logging work); the other
  device-facing handlers' revocation line and chain policy; the Server tests' time bound per cell.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (one change for the five items; the
product and text edits frozen and the two cells written to their table; compare without the fragment and request the
link as given; drop the revocation line; the held-hash sentence with a pinning cell and a store switch; the platform
words; the citations with their method names; no local CodeQL). No choice in this change is the product owner's.

Nothing is deployed; nothing was sent to any printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
