# FOR RECORDS: OXPd 2 Universal Print registration material (lane F, kit B1840), gate G1 round 1, reader B1904

Not repository text. For the next OXPd records pass (backlog, runbook, design notes); nothing here was written into
the project. No person is named.

## What lands

- `src/Datasec.Suite.UniversalPrint/Registration/` (12 `.cs`, a README) and its test folder (9 `.cs`, 54 tests).
  `RegistrationKeys`: RSA-2048 key, PKCS#10 request (Workpath subject), the private key only as one record `uprint/<id>`
  of the secret store; an issued certificate kept only after rules (1) to (8) and (5b); attach once; delete.
  `CloudDeviceTokenHolder`: in memory, 90% on the monotonic clock, `Invalidate(id, refused)`, one bounded call per id.
- The library references `Datasec.Suite.Secrets`; four lock files changed by project entries only (UniversalPrint,
  its tests, Jobs, Jobs tests). Totals 1524 -> 1578 (both legs); rules files 478 -> 500; Ran 111, floor 111.
- Two commits: the kit's, and one fix after the first hosted Linux run (OpenSSL parsed a changed validity date late
  and threw from `NotBefore`): the fields are now read inside the parse rule; a throwing chain build is not trusted.

## From this gate (each for the backlog unless a fix round takes it)

1. **Removal is not serialised with an attach (F1, Minor).** `DeleteRegistration` does not take the attach lock.
   Measured (probe G01): with an attach paused inside its write, `DeleteRegistration` returned true; the attach then
   completed and the record (key and certificate) was back in the store under the removed id. Fix: the delete takes
   the same lock, plus a cell (delete during a paused attach: no record afterwards). Owed before the removal flow
   (WP4.5) calls `DeleteRegistration`.
2. **A blocking issuer escapes the bound (F2, Minor).** The 30-second bound starts on the task the issuer returns.
   Measured (probe G02): an issuer that blocks before returning its task held both callers of one id while the clock
   moved 120 s past the bound. Fix: start the issuer call off the caller's path so the bound covers it, plus a cell.
   Owed before the real device-token issuer lands.
3. **Cells that no mutant of the reader's could redden (test gaps, the code is right today):** clearing of the PKCS#8
   export in `CreateRegistration` (mutant mNoZeroPkcs8 green); the reader's re-check of a held certificate in the
   record (mReadCertLoose green: no R-row puts a record whose `certificate` member is not a certificate); the fix
   commit's two widened catches (mFixUndone and mCatchNarrow green on macOS: only the hosted Linux leg's C01 holds the
   first).
4. **Measured on macOS arm64 by the reader (the seat had RELAYED them):** a leaf from the trusted issuer marked CA:TRUE
   is ACCEPTED; a leaf with an unknown critical extension is IssuerNotTrusted; a leaf whose extended key usage is
   server authentication only is ACCEPTED (no rule reads key usage; the real certificate's extensions are UNMEASURED);
   the record put back to its first form after an attach reads as no certificate and a second, different good
   certificate is then accepted (version 4); two `RegistrationKeys` over one store both accepted one attach each in 20
   of 20 runs (the README's "within one instance only" limit); a key factory that throws lets a
   `CryptographicException` leave `CreateRegistration` with nothing stored (the seat's named limit 4(f)).
5. **An issuer that answers an already disposed token** is held and handed out as zero bytes (probe G03). The
   interface says the holder owns what it is handed; a check is cheap. Backlog.
6. **Kit wording for later kits:** Step 6(a)'s pathspec `tests/<project>/*.cs` crosses `/` in git and matches the new
   `Registration/*.cs` files (use `:(glob)`); SECRETS point 1 should allow a test to read a tracked source file
   (L03 reads the library's project file). Both of the seat's deviations accepted by this reader.
7. **The runbook gains this lane's checks:** the lock rule over four files (a program over package and project
   entries, two planted controls); `restore --locked-mode --force` with CI=true; the boundary scan with its controls;
   the raw scan of K04 and X01; the hosted C01 as the only proof of the late-parse fix; red first against stubs.
8. **Still open (NOT DECIDED of the kit, unchanged):** the real issuer of device certificates and how the host is
   given it; whether the service accepts the Workpath request from a server; whose app registration; where the device
   token lives across a restart; the store partition the host gives and who calls `DeleteRegistration` and `Remove`;
   the platform chain's answer at the exact NotBefore and NotAfter on Linux and Windows. The Jira ticket of WP4.1 stays
   open and unwritten.
