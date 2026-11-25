# FOR RECORDS: the row-3 write lane round 1 of 2 (kit B2091, seat X74), the OXPd 1.x CA store writes, head be650e1b (gate B2096: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2091 THE AUTHORITY: `CLARIFICATIONS.md` counts `ImportCertificate` 0, `RemoveCertificate` 0,
`ExportCertificates` 0, `CA store` 0; stamp S4 states Q1 and Q2 "a" in words as Tuesday's, Q3 to Q10 the defaults).
Q1 "a" departs from the commission's "must not share a file" (stated in the kit, D1, and accepted at S4).

## What the lane gives (RELAYED from the kit's FOR RECORDS, CHECKED by the gate at be650e1b where marked)
- The OXPd 1.x client imports a CA certificate into a device's OXPd CA store and removes it (HP's `ImportCertificate`
  and `RemoveCertificate`, admin), each a dry run unless executed; it takes ONE DER certificate of 1 to 10240 bytes
  whose basic constraints name an authority (CHECKED: 10240 taken, 10241 refused, a leaf refused, a trailing byte
  refused); an import's undo is the remove of the same certificate. It reads the store (`ExportCertificates`, admin;
  CHECKED: `admin` on every one of 33 probe reads, never `guest`) through the writer only, answered only when every
  entry is one certificate; the read catalogue is unchanged.
- The lab's `oxpd1 write --write ImportCaCertificate|RemoveCaCertificate --certificate <file>` takes ONE CA certificate
  file. **Corrected wording (gate FOUND 3):** a file holding the words `PRIVATE KEY` (any PEM private key, encrypted or
  not) is refused before the certificate is read from it; a DER key or a PKCS#12 is refused by the certificate rule; a
  bare base64 key after the certificate (no BEGIN line) is NOT refused, and only the certificate's DER is sent. An
  executed import reads the store first and writes nothing when the certificate is there; an answered import or remove
  reads the store after and says whether it is there; `undo-owed` owes the remove of an import.
- Named limits: not run against a device; whether the M577 takes the development root (owed item 103), how it exports
  an entry and whether it then uses the CA are UNMEASURED; a fault's subcode is not read; a certificate added between
  the read and the import is not seen.

## Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate)
- **Owed item 103 (whether the M577 takes the development root in its OXPd CA store): NOT closed.** This lane is its
  prerequisite. **The test route for the later device run** (a separate kit after this lands; under the standing
  set-up grant, `CLARIFICATIONS.md:1078`, as Tuesday's register scopes it; RELAYED from the kit's FOR TUESDAY): on the
  M577 (`--addressing 2004`), with a fresh `oxpd1 lab-cert` `ca.crt`: (1) `oxpd1 write ... --write
  ImportCaCertificate --certificate ca.crt` as a dry run, then executed (the read before, the import, the read after);
  (2) the device's own answer is the test: `Answered` with "the certificate is in the device's CA store after the
  write" = the M577 TOOK the self-signed root; `Fault` (HP: `InvalidParameter` for an unsupported certificate) = it did
  not, and item 103 stays open with that answer recorded; `Answered` with "NOT in the device's CA store" is the
  export-form case (H13/H16) and is a question for the coordinator, not a pass; whether the device then TRUSTS the CA
  for a TLS server is not this test; (3) the remove, always, when the import may have taken effect (`undo owed`), then
  `oxpd1 undo-owed` on the session: "nothing is owed"; (4) never a reset, a clean or a firmware step
  (`CLARIFICATIONS.md:734`). **Add from this gate:** (a) read the read-before line FIRST: if the M577 exports an entry
  in a form the reader refuses (gate FOUND 7: a leading newline, text before the BEGIN line, another label, a PEM over
  10240 bytes), the import stops at exit 8 with nothing written, and that line (not item 103) is the answer to record;
  (b) run the session's `undo-owed` with no other write in that session typed with the certificate's id (gate FOUND 1);
  (c) the run folder's `oxpd1-client.log` will hold the device's whole CA store as base64 (public certificates; gate
  FOUND 5): keep the run folder outside any shared or synced place as any run folder.
- **Row 4 serial (Q1 "a", stamp S4):** row 4's branch (UIConfiguration `RegisterTopLevelButton` /
  `UnregisterTopLevelButton`, read first `GetTopLevelButtonRecords`) is cut from `main` only AFTER this lane's pull
  request has landed, never beside it; it shares eight of this lane's eleven paths (`Oxpd1Writer.cs`, the adapter
  `README.md`, `LabFiles.cs`, `Oxpd1Command.cs`, the Lab `Commands/Oxpd1/README.md`, `StubDevice.cs`, `WriteTests.cs`
  (W01's count 6 to 8), `Oxpd1Stub.cs`). Its button needs the product owner's word before it goes on the home screen
  (readiness note B2089 row 4, RELAYED). Row 4's kit should also carry gate FOUND 1's fix if the coordinator takes it
  (row 4 adds two more writes to the same `(host, id)` key).
- **NEW owed item proposed: `undo-owed` keys writes by `(host, id)` without the kind** (gate FOUND 1, Minor; the seat
  named it first, STATUS H20 S-a). Fix candidates: key by `(host, family, id)` (agent, test service, CA store), or
  refuse an `--agent-id` that equals a certificate id. MEASURED: E2, E3, E4 in the gate's `probe-e2e.tsv`.
- **NEW owed item proposed: the certificate file's 64 KiB bound** (gate FOUND 2, Minor): read through a stream bounded
  at 64 KiB + 1, or refuse a path that is not a regular file (a link's own size is what `FileInfo.Length` reads).
- The release guard's landed `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` line (owed 2) is
  unchanged by this lane (printed at BASE too).

## Still open after this lane (none built; the coordinator's choices)
- The device run of first-run row 3 (above). The remote-app certificate calls are not built. Row 4 is the next lane.
- Gate B2070 FOUND 1's class (`string.IsNullOrWhiteSpace` taking non-ASCII white space beside elements) now also sits
  in the store reader (gate FOUND 4): one fix for both readers when next touched.

## Added by the gate (MEASURED; see VERDICT.md)
- FOUND 1 Minor: `undo-owed`'s `(host, id)` key: an answered unregister typed with the certificate's id clears an owed
  import; a later register of that id REPLACES it (the import's owed line vanishes); a remove of a certificate whose id
  equals an owed agent's clears the register.
- FOUND 2 Minor: the 64 KiB file bound holds for regular files only (a symlink to a 70 KB file and a FIFO delivering
  1 MiB are taken).
- FOUND 3 Minor: a PEM certificate followed by a bare base64 private key (no BEGIN line) is taken; the "refuses a file
  holding a private key" wording over-claims (only the certificate's DER is sent; no key byte printed).
- FOUND 4 Minor: the store reader answers with a no-break space beside the entries (HP's schema refuses it).
- FOUND 5 Info: the run folder's `oxpd1-client.log` holds the imported certificate's base64 and every stored
  certificate's export (public certificates; never the password; never on stdout).
- FOUND 6 Info: a CA is taken on basic constraints alone (no key usage `keyCertSign` and an expired CA are taken).
- FOUND 7 Info: the store reader refuses several schema-valid PEM forms (safe side; carry into the device kit).
