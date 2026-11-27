# FOR RECORDS: gate B2196 (lane L3a, host composition part A, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **Lane L3a part A (plan r2 row C17) DONE when the squash lands:** the host reads one `Suite` section; with
  `Suite:Tls` it serves the HTTPS certificate and key from the secret store and refuses to build unless the
  certificate is readable, valid now, for server authentication (when an EKU is present) and named exactly for
  `Suite:HostName` (CN equal and a SAN DNS match, no wildcard, no CN fallback, no IP host name); one certificate source
  at a time; the Graph client (no redirect, no cookie, no default header), the OneDrive browser, the session record
  store, the token broker (refresher not wired), the job spool and the scan receiver wired, each made at first use.
  Cells W01 to W11 (25 cases); nine mutants turn them red (gate re-run: 9 of 9 MATCH). H12 pins seven project
  references (RELAYED from the kit's FOR RECORDS, confirmed by the gate).
- **Not built:** the registry (state database; its connection-string custody goes to L3b), the `IAppModule` contract
  and lines (an INFRA kit after L0), the print sender (per printer), Entra's refresher (L3b), `MyDriveFiles` wiring
  (upload and download; landed by L5 after this kit was drafted), the deployment's boot copy of the TLS values from Key
  Vault into the store (AZ lanes), a settings file, any route, any chain or revocation check, the 30-day renewal alert.
- **Owed to L3b (from the gate's VERDICT.md):** replace the `ITokenRefresher` registration with Entra's; wire
  `MyDriveFiles` with a download client that carries no default Authorization header; consider disposing the half-built
  host on a refused build (F2) and mapping the store-open failure into `TlsStoreFailed` (F3).
- **Owed to the AZ lanes:** the host expects two secrets in its local store at start: `<Suite:Tls:CertificateSecret>`
  (PEM, the LEAF FIRST, then issuers; only the first certificate is served and checked) and `<Suite:Tls:KeySecret>`
  (PKCS#8 PEM of the leaf's key); plain ASCII (a UTF-8 byte-order mark is refused as unreadable); the deployment
  configures only HTTPS endpoints (`Suite:Tls` does not refuse an HTTP endpoint beside it).
- **The Server.Tests hang (Tuesday's point a):** not reproduced by the gate (Server.Tests alone 5 of 5 green on the
  head, 3 of 3 on main cf224e1f, plus whole-solution runs on the head); the new cells hold no unbounded wait. It stays
  the pre-existing open item (owed 137), not this lane's. Windows hosted time of the executable rose 12 s -> 53 s with
  the new cells (cost, not a hang).
- Nothing here ran against a device, a printer, a tenant or Azure.
