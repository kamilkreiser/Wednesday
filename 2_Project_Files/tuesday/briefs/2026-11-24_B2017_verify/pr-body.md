HP's OXPd 1.x service descriptions for first-run steps 2, 3 and 4. One commit, `d3d10b71`, on `e39396f9` (main after
pull request 42; ahead 1, behind 0). Nine files are added under `contracts/oxpd1/hp/`, byte for byte from the pinned SDK
1.8.4.1 jar; five change: `contracts/oxpd1/inputs.sha256` (+9 lines), `contracts/oxpd1/README.md`,
`src/Datasec.Suite.Adapters.Oxpd1/README.md` (two lines), and one pin each in
`tests/Datasec.Suite.Adapters.Oxpd1.Tests/ContractTests.cs` (line 66) and `StubDevice.cs` (lines 180 and 182). No package,
no `.csproj`, no lock file, no `Datasec.Suite.slnx` line, no workflow, no generated client, no adapter source.

## Why

- The project's rule is that a SOAP operation comes only from HP's description files under `contracts/oxpd1/`. First-run
  steps 2 (the Test service on and off, one panel screenshot), 3 (a development CA certificate uploaded, then removed)
  and 4 (one top-level test button registered, then unregistered) need the Test, CertificateManagement and
  UIConfiguration services, which were not there.
- The same jar the first 14 files came from holds all three.

## What changed

- The nine files: for each of the three services its SOAP 1.2 binding, its port-type file and its schema, at the jar's own
  folder names. Their imports close over the already committed `common.xsd`. The Test service's callback pair is left
  out (the device calls it; step 2 does not).
- `inputs.sha256`: 14 lines become 23, the first 14 unchanged and in order, sorted by path.
- The two pins that count the committed descriptions: C01's file count 14 to 23, and the stub's binding-port count 4 to 7
  (`StubDevice.AddressingNamespace`). Nothing else in C#; no case added, loosened or removed.
- `contracts/oxpd1/README.md`: 23 files, seven bindings, why they are kept (the words recorded in the project's
  clarifications, with their dates), and per service which step it serves and what a later write must READ first, in HP's
  own words: `IsServiceEnabled` before `EnableService`; `ExportCertificates` before `ImportCertificate`;
  `GetTopLevelButtonRecords` before `RegisterTopLevelButton`.
- `src/Datasec.Suite.Adapters.Oxpd1/README.md`: the limits line now says these descriptions are committed; the library
  still makes none of these calls.

## What proves it

- Red first: the list and count without the files, Oxpd1 cases 40 / 2 failed (C01 names the nine missing files, C02 counts
  11); the files without the port pin, 40 / 26 failed (C07 and every case that starts the stub); all applied, 40 / 0.
- Each of the nine files with one byte changed reddens exactly C01 and C02 (9 of 9, each undone and proved).
- The nine files fetched again from the pinned jar are equal byte for byte to the branch's blobs.
- The branch's push run 45181263021: linux and windows `total: 2054` (linux 2050 succeeded, windows 2033), rules 656 files,
  111 unit tests, secret scan clean. The windows leg's Oxpd1 cases pass, so HP's CRLF bytes survive the checkout there.

## Still open

- HP's specification "Legal Notices" ("No part of this documentation may be ... reproduced ... without prior consent")
  and the open question to HP on the reverse-engineering clause: reported, not decided here. The nine files themselves
  carry no licence or copyright text.
- HP writes that self-signed certificates are "not recommended/supported" in the OXPd CA certificate store; whether that
  excludes a development root CA is open for the step-3 write.
- The stub answers every operation of the seven bindings with a generic envelope; no case calls the three new services,
  and the three new schemas are compiled by no case (they compile cleanly with xmllint). The write lanes add those.
- An eighth binding reddens the same 26 cases until the port pin moves again (the README says the pins move with the
  list).
- No device has been reached.

## Who decides

The coordinator chose this change and every choice inside it (the nine files and the callback pair left out, the pin
moved rather than loosened, the README lines, no new case). Keeping HP's files in the repository rests on the product
owner's words as recorded with their dates: 2026-11-21, "hp files have been provided to us"; "we can store them where we
want (and will try to do it safely)", said of HP's OXPd 2 specification files and read by the coordinator as covering
these OXPd 1.x files too; and 2026-11-23, "our license / commercial agreement allows us to use HP code as part of our
code."

Nothing is deployed; nothing was sent.
