New library `Datasec.Suite.Adapters.Oxpd1` (plan work package WP0.4, the OXPd 1.x stubs) and its test project. One
commit, `1fca08cf`, on `da8d64a8`. 30 files, all added, under `contracts/oxpd1/`, `src/Datasec.Suite.Adapters.Oxpd1/`
and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`. No existing file changes, and no package is added.

**HELD: not to be opened until a fix round has a passing gate and the solution file holds the two projects.** The
text below describes the fixed head; at `1fca08cf` the four open items under "Still open" are not yet fixed.

## Why

- The printer to support first is an HP Color LaserJet MFP M577, an OXPd 1.x (FutureSmart 5) device. Nothing in the
  repository could read an OXPd 1.x device. This client reads what the pre-install checks need, and writes nothing.

## What changed

- `Oxpd1Client`: `GetDiscoveryTreeAsync` (a GET of `/DevMgmt/DiscoveryTree.xml`, no credentials, the answer checked to
  be well-formed and returned masked, never interpreted) and `ReadAsync(Oxpd1Read)` over a closed enum of five SOAP 1.2
  reads, each to `https://<host>:7627/hp/device/webservices/OXPd/<service>` with the binding's `soapAction`.
- Pinned TLS: a certificate is accepted only when the SHA-256 of its DER bytes is a pin, on every handshake; no
  redirect, no proxy, HTTP/1.1 only; no plain-HTTP and no accept-any setting.
- The admin password: read from a named setting at each call; the record is written through `SuiteLoggerFactory`
  (behind the deny-list); names on the deny-list are masked and the password and its Basic form are scrubbed.
- Every call ends in one `Oxpd1Outcome` (11 values).
- `contracts/oxpd1/`: HP's 14 service descriptions from the SDK 1.8.4.1 jar's `META-INF/wsdls/`, byte for byte, with
  `inputs.sha256`; `.gitattributes` keeps their bytes. The library reads none of them at run time.
- Tests: 18 cells against a stub device on 127.0.0.1 (Kestrel, a certificate made in the test) whose routes and
  actions are read from the committed bindings; every password and record in them is synthetic.

## What proves it

- Red first (macOS arm64): tests and a skeleton library, 18 cells, 13 failed, each by an assertion; with the library,
  18 / 0. 14 mutants, each red on exactly its cells (one named survivor: a second XML layer no cell can redden alone).
- The 14 descriptions equal the jar's entries by SHA-256 (the jar `f2bb325f...`).
- Whole solution at the gated head: 1809 / 0, rules 583 files; the branch's push run passes on both legs.

## Still open

- Not run against a device. Whether a FutureSmart 5 device requires or ignores the WS-Addressing headers, and whether
  the endpoint path holds for the three services whose specifications do not state it, are not measured.
- At `1fca08cf` (fix round owed): a deeply nested answer ends the process; the returned answer can hold the password in
  a split or name form; the WS-Addressing namespace differs from the one the descriptions use; an infinite time-out is
  accepted.
- The reverse-engineering clause of HP's terms is not settled; the client is built from the published descriptions only.

## Who decides

The coordinator chose, as coordinator, this lane and every choice inside it (one library on the logging library only,
the endpoint and action from the bindings, the headers, the pin rule duplicated, the descriptions by copy) and the
landing order. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
