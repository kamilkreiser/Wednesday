# FOR RECORDS: gate B1809, OXPd 2, WP1.1 cut to the local secret store (kit B1789), head 42f926d, NO GO

For a records pass. Nothing here was filed by the gate: no ticket, no backlog line, no runbook line was written. Sources: the
builder's STATUS (`<project>/1_Project_Definition/Briefs/2026-11-20_B1789_STATUS.md`, FOR TUESDAY items 1, 7, 8, 9) and the gate's
VERDICT.md. "Decided by nobody" means: no clarification of the product owner covers it and no kit decision settles it.

## 1. State of the lane

- The branch `b1789/wp11-local-secret-store` at 42f926d is NOT landed. Round 1 of 2 read NO GO: one Blocker by the commission's
  rule (the store works on over a key ring it can no longer read) and one Major (an unprotected key is accepted). A fix round
  follows; its kit takes VERDICT.md findings 1 and 2 as its work and findings 3, 4, 6, 8, 9 and 13 as "in the same commit if
  small".
- `OXPD2-12` (the work package's ticket) STAYS OPEN after this lane lands: the lane builds one of its three parts.

## 2. What is left of WP1.1 after this lane (the builder's item 1, checked against the kit's BLUF 5)

1. The device registry (C1).
2. The state database, its entities and its migrations for PostgreSQL and SQL Server (C17).
3. A database-backed place for the encrypted records (the seam exists: `ISecretRecordStore`).
4. The server clock check and the device clock read (F64).
5. The wiring of the store into the server host (`AddLocalSecretStore` exists; the host does not call it).
6. The Key Vault provider (C15 provider (b)).
7. A TPM-bound or otherwise SEALED key on either operating system (the seam exists: `IKeyRingKeySource`).
8. The escrow of the key for the pair and for the backup.
9. The rotation screens of the admin console (F67, WP5.3).

## 3. Open points for the project's master list (each decided by nobody)

1. **What "sealed" means for the Linux key file, and what performs the sealing** (design `02:375`, `02:560`, `02:926` say the
   words and nothing more). Until it is defined, the Linux half is "encrypted under an owner-only file" that the file's owner
   and a machine administrator can read. Whether that is acceptable for a first installation is not a seat's call. The gate
   adds one fact for whoever defines it: sealing protects the key file from being READ; it does not stop a key being PLANTED
   in the key folder (VERDICT.md finding 2), so the key ring's check must be fixed whatever "sealed" turns out to be.
2. **The DPAPI-NG descriptor for a single Windows node and for the pair** (design `02:560` names a domain group only for the
   pair). The product default is the library's call with no descriptor; the public documentation says that is the rule
   `SID={current account SID}` and that a domain controller distributes the keys. The tests pass `LOCAL=user`, which ties the
   key ring to one account on one machine and is no descriptor for a pair. Which descriptor a stand-alone server gets is a
   packaging decision (WP5.1).
3. **Where the encrypted values live once the database exists** (files, rows or both), and so what the backup of design
   `02:789` copies. The builder's note: a record is an opaque byte string per 64-hex id, so a table of (id, bytes) is enough;
   the KEY RING stays in files unless a later lane gives the library a database repository.
4. **Whether the amended deployment utility shares the device registry**: untouched by this lane.
5. **The value cipher.** The library's default is kept: AES-256-CBC with HMAC-SHA256 (read from a key file on a Mac by builder
   and gate; not printed on Linux or Windows). The design's line `02:702` says "AEAD with random nonces". The gate reads the
   default as acceptable against that line (VERDICT.md finding 10). Whether to name AES-256-GCM for the values too is open.
6. **Rollback.** Nothing stops an older record of the same name being put back (VERDICT.md finding 3). Whether the store owes
   more than a sentence in its README (an authenticated list of names and versions per partition) is a design point.
7. **A guard on `RevokeOlderKeys`** before any operator surface calls it (VERDICT.md finding 4), and a call that names the
   records a re-wrap failed on (finding 5).
8. **Two processes on one partition.** The design's deployment is one server or an active/passive pair (`02:559`, `02:925`).
   The store assumes one process and has no lock between processes; a process that runs on while another rotates and revokes
   writes records nobody can read afterwards (finding 11). What the pair does at switch-over is WP5.7's.
9. No customer-facing word and no question for HP arose in this lane.

## 4. Backlog lines the builder proposes (its item 8; not written by it, kit decision D14), with the gate's additions

Builder's:
- Secret store: decide and build what "sealed" means for the Linux key file. Where: `src/Datasec.Suite.Secrets/FileKeyRingKeySource.cs`,
  `IKeyRingKeySource`. Symptom: the key file is owner-only, nothing binds it to the machine. Why deferred: no design
  definition. Discovered 2026-11-20, WP1.1 secret-store lane.
- Secret store: establish whether DPAPI-NG without a descriptor works for an account without a domain. Where:
  `LocalSecretStore.BuildProtection`, the Windows-only default test. Symptom: unknown; the test accepts both outcomes. Why
  deferred: no Windows machine; the hosted log cannot show it. Discovered 2026-11-20. (The gate's cheapest decisive
  measurement: a Windows-only test that requires the default to work and SKIPS itself with a written reason when the store
  refuses; the hosted log prints skipped tests with their reason.)
- Secret store: no coordination between two processes over one partition; no access control list set on Windows; nothing
  tested for a crash between a record's temporary file and its move. (The builder's fourth clause, "the mutants were not
  re-run after the last three small changes", is closed by the gate: all sixteen were re-run at the head.)
- Secret store: the host does not use it; records are files (a database-backed `ISecretRecordStore` is owed with the rest of
  WP1.1).

The gate's, for whatever the fix round does not take:
- Secret store: the record store reads whatever is at a record's path: a named pipe hangs a read and holds the store's lock;
  a folder, an unreadable file or a file of 3 GiB leaves as a raw I/O error naming a path; no size bound (300 MiB allocated
  before the typed error). Where: `FileSecretRecordStore.TryRead`. Discovered 2026-11-20 in review.
- Secret store: `OwnerOnly.TightenFiles` follows links (a link in `keys/` had its target outside the root set to mode 600)
  and runs outside the typed catch (a dangling link there makes `Put` throw after the record is written).
- Secret store: the key-file checks are by path before the open (a link was accepted under a race, 1,423 of 582,229 loads);
  the file's owner is not compared with the account; a linked parent folder and a folder any user can write are accepted; a
  weak key (32 zero bytes) is accepted.
- Secret store: temporary files of an interrupted write are never removed.
- Secret store: `Rewrap` does not say which records it failed on; `ListNames` fails whole on one unreadable record.
- Secret store tests: the 17 surviving faults of VERDICT.md finding 8, above all: the key id is pinned by no test; the at-rest
  check of the key ring is by element names; the partition binding is held by the separate key rings alone; the link row of
  K08; two mode bits; the partition-name edges; the wrapper added after the builder's mutant runs has no test on Unix.
- Secret store: `RotateKey` sleeps (1 ms steps, at most 200) and reads the clock inside the library.
- The solution file: this lane's `src` line stands after the Server line; ordinal order puts it before (finding 13).
- The root README: `src/Datasec.Suite.Secrets` is still under reserved names (its line 50) and the layout list does not name
  the two projects: the one README pass after the wave.

## 5. Runbook lines the builder proposes (its item 9; not written by it)

- A clone made with `GIT_SSH_COMMAND` taken from the project checkout's local `core.sshCommand` works for clone and push
  (confirmed again by the builder; the gate's clone was made the same way and fetch works; the gate never pushes).
- After a dotnet job the compiler server `VBCSCompiler` stays running and is shared between lanes.
- `dotnet test` does not print a test's diagnostic messages even with a runner configuration file that asks for them. (The
  gate adds: it DOES print every skipped test by name with its reason, on both hosted legs.)
- A tool call that holds a backslash-u escape may reach the file as the character itself: write such an escape by program and
  run the ASCII check.

The gate's, for the next kits:
- The heavy lock `<project>/.tools/wave1-heavy.lock.d` worked as the kit's stamp wrote it: 124 takes by this gate, each
  released by a move.
- A test program that references a library with a framework reference to ASP.NET Core needs that shared framework on the
  machine that runs it: its run-time configuration names it. Both hosted legs have it.
- A probe that starts a store with a RELATIVE root writes into the current directory: a harness sets its own directory first
  (the gate made this slip once and moved the folder into its scratch: VERDICT.md, last section).
- The library's cache: a running Data Protection provider of this framework version does not read again a key it has
  already opened, even after its cache ends (measured, VERDICT.md finding 1). A kit that reasons about "the next re-read"
  must measure, not assume.

## 6. For the kits of the lanes that follow

- The host lane: a value read from this store that is named like a password and reaches a logger or a file write is a
  code-scanning alert at 7.5 (VERDICT.md, item 7); the fix is never to log or store it.
- The host lane: one store per partition per process, registered as a singleton (`AddLocalSecretStore` does that); the store
  must be disposed at shutdown so that the key bytes are cleared.
- Any lane that adds an operator surface for rotation: stop every other process on the partition before `RevokeOlderKeys`,
  and never offer the three calls as separate buttons without the guard of point 3.7.

## 7. The builder's deviations, each as the gate reads it

1. The Windows tests pass `LOCAL=user`; the product default is no descriptor: VERDICT.md finding 9 (a named limit; the
   decisive test is cheap).
2. The version in the purpose chain: sound (a record whose clear version is changed does not read: measured). It does not
   stop an older record being put back (finding 3).
3. More public types than the contract lists: the decryptor must be public for the library to build it by name; the rest
   (the key source, the key, the record store) are the two seams. Keep.
4. One more reason code (`InvalidConfiguration`): keep.
5. The three late changes: re-read, and every mutant re-run at the head (VERDICT.md, measured rows).
6. The builder's two shell slips: no effect seen by the gate (the clone is clean, nothing of the project is missing).
7. The stubs moved to its quarantine: outside the repository.
8. No question arose and no mail was sent.
