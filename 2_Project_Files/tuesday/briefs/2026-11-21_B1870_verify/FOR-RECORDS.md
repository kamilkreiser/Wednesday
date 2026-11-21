# FOR RECORDS: WP1.1 remainder, the device registry and state database (lane B), round 1

For a records pass after the lane lands. Nothing here was written to the project.

## Runbook (`SETUP_RUNBOOK.md`)

- Line 50 (restores) is no longer true as written: on 2026-11-21 a seat made ONE supervised fetch from nuget.org into
  `<project>/.tools/nuget-packages` (95 versions before, 169 after: 74 new, 59 reached through the lock files and 15
  resolver lower bounds that no lock file names). Record: `1_Project_Definition/Briefs/2026-11-21_B1856_FETCH-RECORD.md`
  (24174 bytes, sha256 d59e7357244ed64d...). Every later restore ran offline; the cache listing after the fetch is
  `CACHE-LIST: 169 versions | sha256 f4a91f9d3c4dc782`, unchanged at this gate (22:08 AEDT and after every restore
  and scaffold run of the reader).
- The gate compared all 74 record file hashes (the `.nupkg.sha512` files) with nuget.org's published `packageHash`
  (registration leaf, then catalog entry, GET): 74 of 74 equal; the 149 lock-file entries of the four committed lock
  files match the cache's `.nupkg.metadata` content hashes, 149 of 149. A runbook line for the NEXT fetch should name
  this check as part of it.
- This lane's checks for the table: the scaffold program's two modes (`migrations`, `scripts`), the snapshot compare
  (C20), `fetch.py --list` around every restore, the lane's local count 144 (Devices.Tests 92, Data.Tests 52).

## Backlog (`BACKLOG.md`)

- The 15 lower bounds stay in the cache (Tuesday's ANSWER-1): inert (no lock file names them), but the reachability
  rule of the record program reads lock files only. Fix the rule before a next fetch.
- Test gaps the gate's mutants found (each caught by the gate's own probes, none by the lane's suite): a lookup by a
  serial whose case differs from the key (Find, Record*, Remove); the read-side check that the stored key equals the
  upper-cased stored serial; a capability snapshot bounded in UTF-16 characters instead of UTF-8 bytes.
- Typed-exception gaps: a duplicate Add that loses a race escapes as `DbUpdateException` (the database key still
  holds one row); a capability snapshot holding a lone surrogate escapes as `ArgumentException` (refused, nothing
  held).
- Read side: firmware and model text are returned without re-checking their rule (vocabularies, addresses, names,
  references, snapshots and matches are re-checked).
- The clock check truncates the offset to whole seconds after comparing the exact difference: 300.5 s reads
  `outside` with offset 300.
- A run of both migration sets against a real PostgreSQL 16 and SQL Server (a CI change; NOT DECIDED item 1).
- Database-level append-only enforcement for the audit log (grants or triggers; NOT DECIDED item 2).

## What is LEFT of WP1.1 after this lane

The device clock READ itself (an OXPd 2 call, with WP0.4's clients, WP1.2); the reference time source (an NTP client);
the sessions, jobs and Universal Print state tables (WP1.5, WP1.7, WP4.5); the host wiring and migrate-at-start; a
run of both migration sets against real databases; database-level append-only enforcement; the defect catalogue's
content; the Key Vault provider. **Jira OXPD2-12 stays open.**

## Open questions, decided by nobody yet

- Whether Microsoft.Data.SqlClient's Azure.Identity, Azure.Core, Microsoft.Identity.Client (and its Broker,
  Extensions.Msal, NativeInterop) and the IdentityModel packages may stay in the server's graph (NOT DECIDED item 3:
  the product owner's question, on Tuesday's card). Measured at the gate: none of them but Microsoft.Data.SqlClient
  was loaded in the Data test process, which generates the SQL Server script.
- The seat's note: C-24 ("store it encrypted", a device admin password) beside OQ-2 ("No: discarded after install",
  OXPd 2): the lane keeps an `oxpd1-admin-password` reference kind and no OXPd 2 kind.
- How the next lane that needs a package gets it (NOT DECIDED item 6).

## The seat's STATUS (records only)

- THE MIGRATIONS section still names the first scaffold's id `20261121102614_Initial` ("8 guards on ..."); the
  committed id is `20261121105111_Initial` (DEVIATION 8; 9 occurrences per snapshot, 0 of the old id in the tree).
