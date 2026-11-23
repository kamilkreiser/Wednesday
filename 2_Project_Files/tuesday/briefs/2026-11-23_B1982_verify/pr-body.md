The lab device-reach tool (WP0.1 connectivity, WP0.2 spike tooling), `probe` only. One commit, `8dc7390d`, on `da8d64a8`.
It adds 18 files under `src/Datasec.Suite.Lab/` and `tests/Datasec.Suite.Lab.Tests/` and two lines to
`Datasec.Suite.slnx`. No existing source file, package, lock, workflow or `build/` file changes.

## Why

- No lab or device-reach code exists on main. Before anything of the suite talks to a test printer, one tool must say
  which discovery a device answers (OXPd 2 service discovery, OXPd 1.x discovery tree, IPP) without assuming a
  generation, and must do so read-only, over a pinned certificate, with every exchange recorded masked.

## What changed

- `probe <host> --run <new folder> [--pin <sha256>]`: `GET /cdm/servicesDiscovery`, `GET /DevMgmt/DiscoveryTree.xml`
  (HTTPS), IPP Get-Printer-Attributes on 631 and 443; optional plain-HTTP discovery tree GET
  (`--plain-discovery-tree <port>`). Exit codes 0, 2, 3 (first contact), 4 (pin refused), 5 (run folder exists).
- Trust (`Device/CertificatePin.cs:63`, `Device/DeviceChannel.cs:48-62`): pin = SHA-256 of the leaf's DER bytes;
  one handler and one connection per call; no proxy, no redirect, no cookie, `PooledConnectionLifetime` zero,
  TLS 1.2/1.3, HTTP/1.1 exactly. Read-only and plain-HTTP refusals in the channel before any connection
  (`DeviceChannel.cs:70`, `:74`).
- Recording (`Recording/RunRecorder.cs`, `Recording/Masking.cs`): one file per call plus `summary.txt`; masking by
  name through the logging deny-list.
- 37 test cases (P01 to P13, H01 to H06, M01 to M03, B01 to B03) against a Kestrel stub on 127.0.0.1 with in-memory
  certificates.

## What proves it

- Red first (macOS arm64): the project with 15 guard lines stubbed, 24 of 37 cases red, every one by assertion;
  green with the guards. 21 mutants, each red on exactly its cells.
- Whole solution 1846 / 0 / 1842 / 4 locally; the branch's push run green on all four jobs (linux 1842 succeeded,
  windows 1825, RULES 571 files, secret-scan every proof line).

## Still open

- Without `--pin` but with `--plain-discovery-tree`, when the HTTPS port gives no handshake the plain discovery tree GET
  is still sent (measured on 127.0.0.1); the README's "without `--pin` ... nothing is sent" holds only for TLS.
- A body whose type is not JSON, XML or IPP is still read as one when its first byte is `{`, `[` or `<`, and then
  shown masked by name; XML comments and processing instructions are shown. The README says such a body is not shown.
- A JSON answer that holds one property name twice throws `ArgumentException` out of the masking, which ends the run
  without its summary (no value is written).
- Each is owed as a fix round or a README correction.
- What an HP device answers to any call is not measured: nothing here has run against a printer or a simulator.
  The first real run is a separate step.

## Who decides

The coordinator chose this round's cut (`probe` only; `read` a later round) and every choice inside it. No choice in
this change is the product owner's.

Nothing is deployed; nothing was sent; nothing connected to a device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
