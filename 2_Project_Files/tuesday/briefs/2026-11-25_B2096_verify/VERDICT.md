GATE B2096: GO WITH FINDINGS @ be650e1 on main baa32ea

Gate G1 (a lab write to a device path, a new admin send, a certificate parser), ROUND 1 OF 2 of the row-3 write lane,
one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2091 (seat X74; stamp S4: Q1 "a" row 4 serial
after this lands, Q2 "a" the writer's own `ReadCaStoreAsync` through `SendAdminReadAsync` with the read catalogue
unchanged, each in words; Q3 to Q10 the defaults; S8 the canonical heavy runner 31adedc8; every choice the
coordinator's, none the product owner's). Head `be650e1bec5b90106126d358272063a5591e844b` on `b2091/row3-ca-store`,
ONE commit, one parent = main `baa32eae27ddf1267ca1522ef7f1138a4dd832cd` (PR 51). Main and the branch did NOT move
during the gate (gh api -X GET 18:43 and 18:59; open pull requests 0 both times). Read and measured 2026-11-25 18:42 to
19:20 AEDT in my scratch `fleet/state/s327/g2096/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity;
detached at the head; the mutants ran here), worktrees `red` (BASE + `1-red.diff`) and `probe` (the head + two probe
files of mine, `GateProbeTests.cs` in each test project, never committed, never pushed). Every heavy job through the
kit's `heavy.py` (sha256 31adedc8...) and the wave lock, one at a time (lock waits 0 to 4 each, load-gated); the 53
released lock folders are mine, in `g2096/_quarantine/locks/`; no other holder's lock or file touched; the lock absent
at 19:15.

**BLUF.** On every path I could build the lane does what its G1 questions ask: **no path of `oxpd1 write` sends the
bytes of a file that holds a private key** (only the certificate's DER is ever sent: V01 reads the body back; a PEM
key, encrypted or not, is refused by the words check; a DER key and a PKCS#12 by the certificate rule; no key byte
printed, E5), **a leaf (C06, F15) or two certificates (U07, F11) are refused, a listed certificate is not imported
again (U03, `mListedIgnored`), absence is never inferred from a store read that could not be read whole** (33 store
shapes: every entry-level oddity that HP's schema refuses ends `MalformedAnswer`, exit 8, nothing written), **every
import that may have taken effect is owed** (Answered and Fault/Unknown owed, 401/403 not, the Pending line entered
before the send), and **the store read carries `admin` on every one of 33 probe reads, never `guest`**. The head is
BASE plus the two frozen patches byte for byte; red first exactly the 21 cases, each by assertion; `total: 2297`,
`failed: 0`; `MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal` (my run of the frozen tool), each red on exactly its
cases; `HOSTED be650e1b...: PASS` (my read). Four narrower defects, MEASURED, none reaching a device, a key or the
password: `undo-owed`'s key has no kind (FOUND 1, the seat's S-a confirmed and widened), the 64 KiB file bound holds for
regular files only (FOUND 2), a bare base64 key after the certificate is not refused (FOUND 3), and the store reader
takes a no-break space beside the entries (FOUND 4); three Info (FOUND 5 to 7). **None blocks the landing.**

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (`undo-owed` keys a write by host and id, not by kind: an owed import can be cleared or
   replaced by a sign-in agent write of the same id).** `LabFiles.cs:393` `(string, Guid) key = (w.Host, w.AgentId);`,
   `:396` `owed[key] = w;`, `:400` `owed.Remove(key);`. MEASURED (`logs/probe-e2e.tsv`, through the real `oxpd1
   undo-owed`): E2: an answered import (owed, exit 11), then an answered `UnregisterSignInAgent` whose agent id equals
   the certificate's id: exit 0 "nothing is owed"; E4: an import then a register of that id: exit 11 with ONE owed line,
   the register's: the import's owed remove VANISHES from the list; E3 (reverse): an owed register cleared by an
   answered `RemoveCaCertificate` of a certificate whose id equals it. Reach: only an operator typing a certificate's
   derived id (a version-8 UUID, printed by the run) as an `--agent-id`. Property P5 ("every import that may have
   taken effect owes the remove ... until an answered remove of it") is false for these inputs. The lab README's
   Limits sentence ("`undo-owed` keys an import and a remove by host and that id, as it keys a register by host and agent
   id") states the key, not the consequence. The seat named E2 and E3 (STATUS H20 S-a); E4 is new. Fix when next
   touched (row 4 adds two more writes to the same key): key by `(host, family, id)`.
2. **Minor, does NOT block (the certificate file's 64 KiB bound is the path's own size, so a link or a pipe delivers
   more).** `LabFiles.cs:242`-`:243` `FileInfo info = new(path); if (!info.Exists || info.Length > MaxBytes)`, then
   `:249` `File.ReadAllBytes(path)`. MEASURED (`logs/probe-files.tsv`, `CaCertificateFile.Read` on the head): a regular
   file of PEM + 70000 bytes REFUSED (F16, the control); a symlink to the same file TAKEN (F17: `FileInfo.Length 102`,
   the link's own size); a FIFO delivering PEM + 1 MiB TAKEN (F20: `FileInfo.Exists True`); a symlink to a key file
   still refused (F18: the words check reads the target's bytes). DERIVED, not run: a FIFO with no writer blocks the run
   before any folder or connection; a character device such as `/dev/zero` reads until .NET's array limit. Each is the
   operator's own path, before any folder or connection, and every check after the read runs on the bytes read.
   Over-claim: the lab README's "of at most 64 KiB". Fix: read through a stream bounded at 64 KiB + 1, or refuse a path
   that is not a regular file.
3. **Minor, does NOT block (a PEM certificate followed by a bare base64 private key is taken; "refuses a file holding a
   private key" over-claims).** `LabFiles.cs:257` searches the bytes for `PRIVATE KEY`; `:265`-`:270` take the first
   PEM block and refuse a second one only when `PemEncoding.TryFind` finds it. MEASURED (`probe-files.tsv`): F10, the
   CA's PEM then the base64 of a PKCS#8 key with no BEGIN/END lines: TAKEN; F07 (a DER PKCS#8 key) and F09 (a PKCS#12
   holding a CA and its key): REFUSED by the certificate rule, not the key rule (the seat's S-b, confirmed through the
   verb, E5: exit 2, "does not hold ONE CA certificate", no folder, 0 TLS connections, the key's base64 not in the
   output); F08 (an encrypted PEM key) and F18: REFUSED by the key rule. In every case only `Oxpd1CaCertificate`'s DER
   reaches the envelope (V01 reads the body back as exactly the DER) and no byte of the file but the certificate is
   printed. The lab README says "the words `PRIVATE KEY`" (accurate); the commit subject ("refuses a file holding a
   private key") and the kit's FOR RECORDS ("a file holding a private key refused before anything is read from it")
   over-claim. Harm: none to the device or the key (nothing of the key leaves the file); a wording to correct in the
   records (FOR-RECORDS.md does).
4. **Minor, does NOT block (the store reader takes non-ASCII white space beside the entries; HP's schema refuses it).**
   `Oxpd1Writer.cs:538` `!string.IsNullOrWhiteSpace(t.Value)` is .NET's white space, not XML's four characters (the
   class of gate B2070 FOUND 1, now in a second reader). MEASURED (`logs/probe-store.tsv` S16, through the real client
   and the stub): `<ExportCertificatesResult>&#xA0;<Certificate>...` reads `Answered`, listed 1; HP's committed schema
   errors 1 on that body. Harm: none to the decision: every ENTRY is still read whole and compared; only the container's
   text is wrongly taken. Fix with B2070 FOUND 1: `t.Value.All(c => c is ' ' or '\t' or '\r' or '\n')`.
5. **Info (the certificates' public bytes reach the run folder's client record).** MEASURED (`probe-e2e.tsv` E1, an
   executed import against the stub holding one other CA): stdout holds the imported certificate's base64 0 times;
   `oxpd1-client.log` holds it 2 times (the import's envelope and the read after) and the OTHER stored certificate's
   export 4 times; `undo-list.tsv` and `summary.txt` 0 and 0; the password in none of the three files. This is the
   landed record's rule (every request and answer, scrubbed of the password, adapter README); the lab README's "The run
   prints the certificate's SHA-256 and its id ..., never its bytes" is true of the output only. Public certificates;
   worth one Limits clause when next touched, and the device kit should know the record holds the device's whole store.
6. **Info (a CA is taken on its basic constraints alone).** `Oxpd1Writer.cs:233`. MEASURED (`logs/probe-cert.tsv`): a
   CA whose key usage is `digitalSignature` only (no `keyCertSign`) TAKEN (C03); an expired CA TAKEN (C05); exactly
   10240 DER bytes TAKEN (C01), 10241 REFUSED (C02); basic constraints CA false REFUSED (C06); one trailing byte REFUSED
   (C08). Two basic constraints extensions: NOT BUILT (.NET's `CertificateRequest` refuses a second extension of one
   OID; the `constraints.Count == 1` rule is read, not run). What the M577 answers to the first two: UNMEASURED.
7. **Info (the store reader refuses several schema-VALID PEM forms: the safe side, but a device-run stopper if the
   M577 exports so).** MEASURED (`probe-store.tsv`, schema errors 0 each, outcome `MalformedAnswer`): an entry whose PEM
   text begins with a newline (S13) or with text before BEGIN (S14), a BOM before it (S09), a lower-case or `TRUSTED
   CERTIFICATE` label (S10, S11), white-space CDATA beside the entries (S19), `xml:lang` on an entry (S28). A PEM entry
   over 10240 bytes (a CA of DER 8000) is refused, as HP's schema refuses it (S21: schema errors 1), so a store that
   holds a CA of more than about 7.5 KB DER stops every import at exit 8. An entry holding a malformed first block then
   a certificate is read as that certificate (S30, schema-valid). The file side mirrors it: leading text such as
   OpenSSL's `Bag Attributes` (F02), a BOM (F04) or UTF-16 (F14) refused; leading blank lines (F03) and CRLF (F01)
   taken. Carry into the device kit: read the read-before line first (FOR-RECORDS.md).

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole** (`scratch/treecheck.py`): `--name-status` eleven rows, 2 `A`, 9 `M`; numstat equal to
  THE CODE's (22/2, 301/10, 34/8, 83/10, 128/16, 49/13, 211/0, 39/0, 1/1, 296/0, 60/0); ONE commit, parent baa32eae,
  author and committer the repo's `@datasec.com.au` address; `ls-tree` 675 at BASE, 677 at the head; the commit
  message equals `commit-message.txt` (446 bytes, subject 388). Every changed `src/` line read (both `.cs` files of the
  adapter, both of the Lab, both READMEs); the tests read whole (`CaStoreTests.cs`, `Oxpd1CaStoreTests.cs`, the two
  stubs' added lines).
- **The two patches against THE TOOLS:** my copy of the ten tools 10 of 10 equal to THE TOOLS' sha256 (`1-red.diff`
  e4f53889..., `2-fix.diff` cd5d608c..., `heavy.py` 31adedc8... = S8); temporary index `read-tree baa32eae`, `apply
  --cached` both rc 0, `write-tree` `385c1922` = `be650e1b^{tree}` (EQUAL); red tree `a3a0aa34`; each file's sha256
  and line count in the red tree and at the head equal THE CODE's two columns (11 of 11 each; both READMEs at BASE in
  the red tree).
- **Red first** (`g2096/red`, `logs/r-exe-adapter.log`, `r-exe-lab.log`, `scratch/redcheck.py`): locked restore rc 0,
  build 0/0; adapter `Total: 86, Errors: 0, Failed: 11`, Lab `Total: 274, Errors: 0, Failed: 10`; the 21 `[FAIL]` cases
  equal THE CONTROLS' list (program compare: True, True; missing 0, extra 0, other classes 0); 21 of 21 followed within
  five lines by an `Assert.<name>() Failure` line.
- **Head green** (`logs/h-test.log`): locked restore rc 0; build `0 Warning(s)`, `0 Error(s)`; `total: 2297`, `failed:
  0`, `succeeded: 2293`, `skipped: 4`. The probe tree (head + my two probe files) also ran each test executable whole:
  adapter `Total: 88, Failed: 0`, Lab `Total: 276, Failed: 0` (the 86 and 274 plus my probes).
- **Mutants** (`logs/mutants.out`, `logs/mutant-cases.out`; my run of the frozen `mutants_c1.py`, sha256 3838637a...,
  18:53 to 19:15, load-gated): `MUTANTS: 12 of 12 MATCH, 12 of 12 undone equal`, every row's Total and red set
  equal to the kit's MEASURED line; by CASE: `mLeafTaken` U07 `a leaf certificate`, V02; `mBoundDropped` V02;
  `mImportUndoDropped` U02, U05 `500`, V01, V03; `mBadEntrySkipped` U04 `an entry that is not a certificate`, V04 `not
  base64`, `not a certificate`, `two pem blocks in one entry`, `another element beside`, `an attribute on an entry`;
  `mStoreShapeTaken` V04 `text beside`, `an attribute on the response`; `mEntrySecondPemTaken` V04 `two pem blocks in
  one entry`; `mStoreReadAsGuest` U02, V03, V05; `mKeyFileTaken` U07 `a file holding a private key`, `the key file`;
  `mSecondPemTaken` U07 `two certificates in one file`; `mImportNotOwed` U08; `mListedIgnored` U03; `mNoReadAfter`
  U02, U06. Each is exactly the cases its edit can reach; no other class red; the clone's porcelain 0 lines after and
  HEAD still be650e1b.
- **Whether ANY path of `oxpd1 write` sends a file that holds a private key, a leaf or two certificates:** no path sends
  a FILE: the body is `Convert.ToBase64String(call.Certificate!.Der)` (`Oxpd1Writer.cs:602`) and `Oxpd1CaCertificate`
  is made only from DER that loads as exactly one certificate (`:233`, `RawData` equal to the bytes). Leaf: refused
  (C06, F15, U07). Two certificates: refused in one file (U07, F11) and as DER (V02, C08). A file holding a key: FOUND
  3 (only the certificate is sent). **Imports a certificate the store already lists:** no (U03; probe S27 the same CA
  twice listed 2, `Lists` True). **Infers absence from a store read it could not read whole:** no: 33 shapes, every one
  that is not one certificate per entry ends `MalformedAnswer` (exit 8 before any write, U04); the one schema-refused
  shape read (S16) is outside the entries (FOUND 4). Named limits H13 (another export form) and H14 (a race) stand.
  **Leaves an import that may have taken effect not owed:** the writer owes the remove whenever `Applied` is Yes or
  Unknown (`Oxpd1Writer.cs` `WriteAsync`, Answered Yes; NoCredential, PinRefused, 401, 403 No; every other end
  Unknown); the lab enters the Pending line BEFORE the send and the end after; U05 (`500` owed, `403` not), U08,
  `mImportNotOwed`, `mImportUndoDropped`. Exception: FOUND 1 (a sign-in agent write of the same id).
- **The export shapes HP's schema refuses** (`probe-store.tsv`, each with HP's committed schema's error count): an entry
  in another namespace (S04) or none (S05), `xsi:nil` on an entry (S06) or the result (S07), `xsi:type` on an entry
  (S08), a no-break space inside the base64 (S17), an empty entry (S23), a child element (S24), an attribute on the
  result (S31): all `MalformedAnswer`. A processing instruction (S01), a comment (S02) and a character reference (S03)
  inside an entry are schema-VALID and read (the parser drops PIs and comments; the base64 is whole). A BOM inside the
  PEM (S09) and a PEM label in another case (S10) are schema-valid base64 and REFUSED. CRLF (S12), line breaks inside
  the base64 (S18) and CDATA holding the entry (S20) read, as the schema allows. The one schema-refused shape read:
  S16 (FOUND 4).
- **Whether the store read can carry `guest`:** no. `SendAdminReadAsync` (`Oxpd1Client.cs:119`) passes the constant
  `AdminUser` (`:129`) and reads `_options.AdminPasswordSetting`; its only caller is `ReadCaStoreAsync` (`git grep`: 1
  definition, 1 call in `src/Datasec.Suite.Adapters.Oxpd1`, 2 calls of `ReadCaStoreAsync` in the Lab). Every probe read
  carried `Basic YWRt...` (admin) 33 of 33; `mStoreReadAsGuest` red on U02, V03, V05.
- **Whether a certificate's or a key's bytes reach any output beyond the dry run's envelope:** a key's: no (E5, F07 to
  F10, U07's `AssertNowhere`). A certificate's: not the output (E1: 0); YES the run folder's client record (FOUND 5,
  Info).
- **The README sentences against the code:** every changed or added sentence of both READMEs read against the head:
  the three CertificateManagement rows (`Oxpd1Writer.cs:91`-`:92`, `:465`; `Oxpd1Client.cs:119`, `:129`), "Six writes"
  (W01 6), "The CA store." (`:180`, `:191`, `:218`, `:233`, `:281`, `:486`, `:536`, `:542`; `ReadOnlyViolations` still
  refuses `ExportCertificates`: landed `TestServiceTests.cs:39`), the Limits ("Only first-run steps 5, 2 and 3", "not
  run against a device", H13's sentence); the Lab's `write` heading and options (`Oxpd1Command.cs:503`, `:588`), "A
  certificate write takes ONE CA certificate file" (FOUND 2's "at most 64 KiB" over-claim), "An import reads first, and
  both read after" (`:851`, `:875`, `:1002`, `:1020`), the refused-password count ("an import at most three times":
  U02 `admin` 3; a remove at most twice), the undo and `undo-owed` paragraphs (`LabFiles.cs:324`, `:394`), the Limits
  (H14's sentence; the key sentence of FOUND 1). Two over-claims of the lane's own words (FOUND 2's bound in the README;
  FOUND 3's "file holding a private key" in the commit subject and the kit's records text).
- **D8's one landed literal and nothing else of a landed cell:** removed lines under `tests/`: exactly 1
  (`WriteTests.cs` `Assert.Equal(4, Oxpd1WriteCatalogue.Rows.Count);` to 6); both stubs gain lines only (39/0, 60/0);
  `Oxpd1Read.cs`, `contracts/`, `.github/`, `build/`, `Datasec.Suite.slnx`, `Directory.Packages.props`: `diff --stat`
  empty; added lines naming `X509Store`, `Process.`, `GetEnvironmentVariable` or `PackageReference`: 0.
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, 18:49): run 45569238645, four
  jobs attempt 1 success, linux `succeeded: 2293`, windows `succeeded: 2276`, `RULES: clean (677 files)`, `UNIT-TEST
  FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15 files)`, `failed Datasec.` lines 0 and 0 (control: 4
  `Oxpd1.Tests.dll` and 4 `Lab.Tests.dll` lines per leg); check runs beside the four: 0; last line `HOSTED
  be650e1bec5b90106126d358272063a5591e844b: PASS`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3).

## 2. ADVERSARIAL BEYOND THE KIT (the commission's six shapes, then three outside each property)

- **A PEM with CRLF line ends:** taken from a file (F01) and read in a store entry (S12). Covered.
- **Leading text before the BEGIN line:** a file with OpenSSL's `Bag Attributes` preamble REFUSED (F02, exit 2 by the
  verb's rule; only white space is trimmed, `LabFiles.cs:265`); a store entry with any leading byte, even a newline,
  `MalformedAnswer` (S13, S14; FOUND 7). The safe side.
- **A CA by basic constraints whose key usage forbids certificate signing:** TAKEN (C03; FOUND 6, Info).
- **Exactly 10240 and 10241 DER bytes:** 10240 TAKEN (C01), 10241 REFUSED (C02) by `Oxpd1Writer.cs:191`.
- **A symlinked certificate path:** to `ca.crt` taken (F19); to a key refused (F18); to a file over 64 KiB TAKEN
  (F17: FOUND 2).
- **A file that grows between the check and the read:** a FIFO (size 0 at the check) delivering PEM + 1 MiB TAKEN
  (F20: FOUND 2). A regular file appended between `:243` and `:249`: NOT RUN (no race harness); DERIVED the same:
  every later check runs on the bytes read, so the only effect is the bound.
- **Three shapes outside each property** (the kit's P1 to P7):
  P1 (ONE CA certificate's DER and nothing else): a PEM + a bare key (F10), a broken first block then the PEM (F12),
  a PEM then a broken second block (F13): each sends the certificate's DER alone (covered by `Body`, V01).
  P2 (no write from a key, a leaf or two certificates): a DER key (F07, refused), a PKCS#12 (F09, refused), a bare
  base64 key after the PEM (F10, TAKEN: FOUND 3).
  P3 (an import only after an answered read that does not list it): a no-break space beside the entries (S16, answered:
  FOUND 4), an entry holding a broken block then the certificate (S30, read as it), an entry in another form (H13,
  named limit).
  P4 (answered only when every entry is one certificate in HP's shape): PI, comment, character reference (schema-valid,
  read: covered), `xsi:nil`/`xsi:type`/other namespace (refused: covered), S16 (FOUND 4).
  P5 (every import that may have taken effect owes the remove): a Fault (U05: owed, covered), a Pending line of a run
  that died (landed form, the line entered before the send: covered by reading `Oxpd1Command.cs:860`-`:862`, not run), a sign-in agent
  write of the same id (E2, E4: FOUND 1).
  P6 (`admin`, never `guest`): no setting (V05: no connection), a 401 on the read (U04: exit 6, one request), every
  probe shape (33 of 33 admin): covered.
  P7 (the password in no output or file; no key byte printed): E1 three files and stdout 0; E5 the key's base64 0;
  U07's `AssertNowhere`: covered; the certificate's bytes in the record: FOUND 5.

## 3. SCANS

- **gitleaks 8.30.1** (`logs/gitleaks.out`): control FIRST, a token built in-process from two halves and 36 random
  characters, never printed, outside the clone: rc 1, `leaks found: 1`, moved to `g2096/_quarantine/gl-control-code`;
  then `gitleaks git` over `BASE..be650e1b` rc 0 (`1 commits scanned`, `no leaks found`); the eleven head blobs, both
  patches, the message file, `mutants_c1.py`, `checks_c1.py` and the commit's own message as `1.txt` to `17.txt` in a
  new folder: rc 0 `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 1224 added lines of `BASE..head`
  (`scratch/added.txt`, made by `git diff` for this gate, the same count as the seat's `checks_c1.py` `added 1224`)
  and `commit-message.txt`: every class 0, `WORDS: clean (2 files)`; `B2[0-9]{3}` 0 and 0 (control: the kit counts 20
  lines).
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#52`, `squash-body.txt` and `pr-title.txt`:
  `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 1 and `coordinator` 2 (the "Who decides" section, as gate
  B2070's body), 4 bytes outside ASCII (the attribution line's emoji), every other class 0; `build/squash_scan.py`
  (BASE's, equal to the head's: `build/**` is not in the diff) with `#52`: control rc 1 found 2, message rc 0 found 0,
  `SQUASH-SCAN: clean`; gitleaks over this folder's seven texts and the `#52` subject under neutral names, the control re-planted
  first (rc 1, `leaks found: 1`, quarantined): rc 0, `no leaks found` (19:17, `logs/gitleaks-texts.out`).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). `checks_c1.py` (it reads a STAGED tree; the seat's `CHECKS: 10 of 10
PASS` is RELAYED; its rows 1, 3, 5, 8, 9 and 10 re-measured above by `git diff` and `git grep`). The chain's publish and
release guard, `repo_rules.py`, the unit tests of `build/tests` (RELAYED from the seat; equal on the hosted legs, my
read). The whole solution after the mutants (the clone's porcelain is 0 lines after the tool's undo and HEAD is
be650e1b, so the measured head is the bytes that ran). A regular file appended between the size check and the read;
a FIFO with no writer; `/dev/zero` (DERIVED in FOUND 2). Two basic constraints extensions (FOUND 6). Any device.

## OUTSIDE THE FENCES

None. Writes: this folder and `fleet/state/s327/g2096/` only (my clone, its two worktrees, logs, scratch, quarantine).
No pull request, no push (the clone's push URL is `invalid://no-push`), no re-run of a hosted job, no `cd`, nothing
deleted, no printer or device, no Azure, nothing to any person, no Jira. Every gh call a GET under the project's
GH_CONFIG_DIR. One read command of mine sent stderr to `/dev/null` (a `cat` of a log that did not exist yet; no effect
on any result). No print of `kam_rulings_today.sh` or `kam_msgs.sh` was made or saved.
