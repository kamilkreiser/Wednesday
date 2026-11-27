## Why

The server host needs its own settings, its HTTPS certificate from the place the deployment keeps secrets, and the
landed libraries wired in. This is plan lane L3a, the first part of the host's composition. It builds no registry
(database) and no app module lines: those wait for their own questions and lanes. Every choice in it (two PEM secrets,
the strict name rule, one certificate source, refusal at first use, no settings file, no print sender) is the
coordinator's.

## What changed

12 files, all under `src/Datasec.Suite.Server/` and `tests/Datasec.Suite.Server.Tests/` (6 added, 6 changed: the
server project gains four project references, NuGet rewrote its two lock files, one landed cell (H12) names the new
references; no package is added).

- `SuiteHostOptions` reads `Suite:HostName`, `Suite:Tls:CertificateSecret`, `Suite:Tls:KeySecret`,
  `Suite:Graph:Cloud`, `Suite:Graph:BaseAddress` and `Suite:Jobs:SpoolRoot`, and refuses at build: a certificate from
  two sources, one secret name without the other, store TLS without a host name, a host name outside the rule or an IP
  address.
- `StoreCertificate` reads the two secrets (the certificate's PEM text with its issuers, the PKCS#8 key), makes and
  re-imports the certificate, and refuses to build unless it is readable, valid now, for server authentication when it
  has an enhanced key usage extension, and named exactly for the host name (CN equal and a DNS name matching with no
  wildcard and no CN fallback). Both store values are disposed and the buffers zeroed.
- `LibraryWiring` registers one HTTP client for Graph (no redirect, no cookie, no header or base address of its own),
  `GraphClient`, `MyDriveBrowser`, the session record store, `TokenBroker` over a refresher that throws until Entra is
  wired, `JobSpool` and `ScanReceiver`, each made at its first resolve.
- `ServerHost.Build` reads the settings, registers the libraries and serves the store's certificate through Kestrel's
  HTTPS defaults. The server README documents the settings, the refusal kinds and the limits.

## What proves it

- Cells W01 to W11 (25 cases) start the host on 127.0.0.1 port 0 with certificates made in the test; the server test
  executable `Total: 43, Failed: 0`; whole solution 2513 / failed 0 locally and on both hosted legs of the branch push
  (locked restore on both legs; release guard 28 and 29 files: the six wired project assemblies with their symbols and
  the two logging assemblies, nothing else).
- Nine mutants of the change each turn their intended cell red (re-run independently: 9 of 9 MATCH).
- Secret scan and word scan clean over the added lines and the message.

## Named limits

1. No chain is built and no revocation is read for the served certificate; the issuers in the secret are served as
   the chain unchecked; no renewal alert; the certificate is read once at build (a renewal needs a restart).
2. Only the FIRST certificate of the certificate secret is the served one: a secret holding several certificates is
   not searched for the valid or the longest-lived one (a mismatched key or an expired first certificate refuses the
   build).
3. A refused build leaves the half-built host undisposed (the process ends on it; the cells cannot dispose it either).
4. A local secret store that cannot open, with `Suite:Tls` set, refuses the build with the store's own fixed-text
   exception rather than `TlsStoreFailed`; a malformed enhanced key usage extension refuses it with the platform's
   exception.
5. `Suite:Tls` does not force HTTPS: a plain HTTP endpoint configured beside it is served.
6. How the deployment puts the two TLS values into the store, and the TLS path under the Windows service's own
   account, are not built or run here. `MyDriveFiles` (upload and download) is not wired.

## Who decides

The coordinator lands this pull request (squash, pinned to the reviewed head). Nothing ran against a device, a
printer, a tenant or Azure. Nothing is deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
