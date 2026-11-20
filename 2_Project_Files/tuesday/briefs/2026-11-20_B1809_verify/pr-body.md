## What this adds

A library, `src/Datasec.Suite.Secrets`, and its tests, `tests/Datasec.Suite.Secrets.Tests` (25 tests; the solution now runs 26).

**The server does not reference this library yet. It protects nothing until a later change wires it into the server. The two published folders are unchanged (10 and 11 files).**

## What the library does

- A caller puts bytes under a name, in a partition, and reads them back. A value is bytes of any kind.
- Each value is encrypted and authenticated by ASP.NET Core Data Protection, taken from the shared framework (no package is added). The library's default algorithms are kept: AES-256-CBC with HMAC-SHA256, a random key modifier and a random IV for every value.
- A value is tied to its partition, its name and its version number. A record copied over another name, or into another partition, does not read.
- A record is one small file, named by the SHA-256 of the name. The name and the version number are in clear inside it.
- A read returns the bytes, or the library's one typed error. It never returns an empty or partial value. An empty value is refused at the write.
- Names follow one rule (lower-case letters, digits, `.`, `_`, `-`, `/`, at most 200 characters, no `..`). A name is never used as a path.
- Nothing in the library logs, prints or opens a connection.

## What protects the key ring, and what does not

Each partition has its own key ring. It is encrypted at rest:

- **On Windows** by DPAPI-NG, through the Data Protection library's own call. The descriptor is an option.
- **Elsewhere** under a 32-byte key read from a key file, with AES-256-GCM: a fresh random 12-byte nonce for every encryption and a 16-byte tag. The key file must be a plain file of exactly 32 bytes with no permission bit for group or other.

A store does not start over a key ring that holds an entry it cannot open, so a wrong key file does not lead to a new key beside the old ones.

What does NOT protect it:

- **The key file is not sealed.** Nothing ties it to the machine. Its owner, and an administrator of the machine, can read it and open the key ring.
- No TPM. No Key Vault provider. No escrow. Nothing for a pair of servers or for a restore.
- On Windows the library sets no access list on its folders.

## Rotation

Three calls, in this order: `RotateKey` (a new key; later writes use it), `Rewrap` (every record encrypted again under the current key; it returns how many it read, rewrote and failed on), `RevokeOlderKeys` (older keys are revoked). The key file rotates through a list of retired key files.

`RevokeOlderKeys` does not check that a re-wrap ran. A record that was not re-wrapped first stops reading.

## What was run, and where

- On a Mac and on the hosted Linux job: 26 tests, 23 passed, 3 skipped (the three Windows-only tests).
- **Windows was run on the hosted job only**: 26 tests, 21 passed, 5 skipped (the five tests of the key file). The Windows tests pass the descriptor `LOCAL=user`. The default (no descriptor) was not shown to work: by the public documentation it rests on a domain controller, and its one test accepts a working store or a clean refusal.
- In review: the sixteen deliberate faults of the build each turn their own test red; 37 more faults were tried, 20 turn a test red and 17 do not (the tests to add are listed for the next change).
- In review, against hostile files: over 1,000 damaged, cut, swapped or replaced record files and 39 damaged key rings. No read returned a value that was not put under that name and partition, and no value or key was found in any file or error text.

## Known at this head, and not right yet

- **A key file with no protection, put into the key folder, is accepted.** The store starts, and its next write is sealed under that key; a reader holding only that key and the record can then read the value, without the key file.
- **The key ring is checked at start only.** A running store goes on writing from the key it holds in memory after its key file entry is damaged or removed. A rotation run then makes a new key and completes. A store started over a key folder that was emptied makes a new key and carries on; the older records give the typed error.
- An older record of the same name, put back, reads (the older value). Deleting a name and writing it again starts its version at 1 again.
- A listing shows the name and version each record file states, without opening it.
- A named pipe in place of a record makes a read wait for ever and holds up every other call on that store. A folder, an unreadable file or a file of 3 GiB in place of a record leaves as a plain I/O error that names a path, not as the typed error.
- The check that the key file is not a link is made before the file is opened; under a deliberate race a link was accepted (about 1 load in 400).
- With two processes on one partition, a process that keeps running while another rotates and revokes writes records that nobody can read afterwards.

## Limits, as the library's own README names them

The key file is owner-only and not sealed; no TPM; no Key Vault provider; no escrow, nothing for a pair or a restore; records are files, not database rows; the Windows half is proven on a hosted runner only, with `LOCAL=user`; no access list set on Windows; one process per partition; the server does not use the store yet.

## What is left of the work package

The device registry; the database, its entities and its migrations; a database-backed place for the records; the server clock check and the device clock read; the wiring of the store into the server; the Key Vault provider; a sealed or TPM-bound key; the escrow of the key; the rotation screens.

## Shared files

Two lines added to `Datasec.Suite.slnx`. No package, no line in `Directory.Packages.props`, no workflow line, nothing under `build/`. The root README lists are updated later.

## Who chose what

Every choice inside this change was made by the build's coordinator or by the builder: files for the records, one key ring per partition, the key file and its cipher, the default algorithms for the values, one version per name, the three rotation calls, the error behaviour. None is a product decision. What "sealed" means for the key file, and which Windows descriptor a server without a domain gets, are open.

Nothing is deployed. Nothing was sent to anyone.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
