# FOR RECORDS: lane CT (kit B2014, seat X60), HP's OXPd 1.x descriptions for first-run steps 2 to 4, head d3d10b71 (gate B2017)

For the records lane only; nothing here is written into a project file by the gate. Who decided the lane, its scope and
its defaults: the coordinator (Tuesday), as coordinator (S4: Q1 IN, Q2 IN, Q3 to Q6 the defaults). Keeping HP's files in
the repository rests on the product owner's words as recorded with their dates (CLARIFICATIONS.md line 394, 2026-11-21
09:40:49, said of HP's OXPd 2 specification files; line 758, his live-board note of 2026-11-23 17:56); reading the
2026-11-21 words as covering these OXPd 1.x files is the coordinator's reading, not his.

## From the kit's FOR RECORDS (RELAYED, copied)
- HP's descriptions of the Test, CertificateManagement and UIConfiguration services (first-run steps 2, 3, 4) are
  committed under `contracts/oxpd1/hp/` from the pinned SDK 1.8.4.1 jar (23 files listed). Authority: the product
  owner's ruling C-56 (option b, "Keep HP's files in the repository"; card subject OXPd 2 specification files; read by
  the coordinator as covering these OXPd 1.x files) and his note C-74. Reported, not decided: HP's spec "Legal Notices",
  the library README's beta line, R32.
- The two test pins that count the committed descriptions now read 23 files and seven ports; a later binding moves both
  again.
- Three write lanes follow (one per step), each a pair with its undo and the READ first the contracts README names:
  `IsServiceEnabled` before step 2's enable; `ExportCertificates` before step 3's import (HP: an import of an existing
  certificate "will have no effect", so a blind remove deletes a certificate that was there); `GetTopLevelButtonRecords`
  before step 4's register (HP: a matching guid "overwrites the existing one"). HP's "self-signed certificates ... not
  recommended/supported" bears on step 3's development CA: open, for the step-3 kit or HP.
- The Test binding holds 17 live operations (two of the 19 names are inside comments), correcting B2012.

## Measured by the gate (MEASURED, macOS arm64, .NET 10.0.404, scratch fleet/state/s319/g2017/)
- The nine files re-fetched from the pinned jar by the gate's own `fetch_ct.py` copy (jar sha256 equal to the pin):
  9 of 9 equal byte for byte to the branch's blobs (control: one byte changed in memory, not equal).
- Import closure over all 23 committed files: 0 dangling `import`/`include`; each new binding imports its port-type file,
  each port-type file its schema, each schema `../..._common_2010_04_14/common.xsd`. (B2012 line 128 says the port-type
  files import `common.xsd`; it is the schemas that do. The README's "import closure" is right.) Every `wsdl:part`
  names a global element of its schema; every binding operation is a port-type operation and the reverse. All nine
  schemas (the seven services, `common.xsd`, `securitydomain.xsd`) compile with `xmllint --nonet` (control: a broken
  schema fails).
- H6 measured, no longer RELAYED: 78 soapActions over the seven bindings, 0 clashes within or across bindings; seven
  distinct service names (the stub's routes); new soapActions 17 + 6 + 25 = 48. H5: 0 uses of the August 2004
  addressing namespace over all 14 `.wsdl` files (14 declare it).
- No licence, copyright, "rights reserved", "confidential", "proprietary", "redistribut" or "consent" line in the nine
  files (the only "Legal" hits are a paper size; control fires). The jar was touched only through `fetch_ct.py`, so its
  other entries were not read by the gate (B2012 section 5: no LICENSE or NOTICE entry, RELAYED). B2012 line 105 records
  the "beta ... must not be redistributed" line as Friday's own README summary, "not HP's text".
- "Nothing in this repository calls these three services yet": 0 hits outside `contracts/oxpd1/` by operation name, by
  namespace or soapAction URI, and by route or service name, at the head and at lane W2's head `67c24d18` (control
  `RegisterAuthenticationAgent` in `src`: found).

## Gate findings to carry (VERDICT.md FOUND; all Info; none blocking)
- FOUND 1: the stub answers every operation of the seven bindings with a generic envelope; no cell calls the three new
  services; a write lane needs its own stub answers and cells.
- FOUND 2: the three new schemas are compiled by no cell (C05 compiles the four read schemas only); measured clean here.
- FOUND 3: the README's second Test-service quote ("When disabled, only this method, ...") is HP's text on
  `IsServiceEnabled`; the README does not name the method "this method" means.
- FOUND 4: the port pin counts ports, not files; a new schema or port-type file moves C01 only.
- FOUND 5: `words.py` (kit B1813's, frozen) counts B-numbers as `B1nnn` only; the gate's own count of `B2nnn` and
  `C-nnn` over every repository text of this lane: 0 (control 8).
- FOUND 6: the commit subject is 240 characters (the squash subject adds the pull request number).
