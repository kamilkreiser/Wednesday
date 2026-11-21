## What this adds

A library, `src/Datasec.Suite.Secrets`, and its tests, `tests/Datasec.Suite.Secrets.Tests` (68 tests: four run on
Windows only, eighteen on Unix only). Three commits on the branch, folded by the squash: the library; a second
commit that checks the key ring at every use and closes the file checks; and a merge of main into the branch that
changes no line of the library (the solution file keeps the projects of both sides).

**The server does not reference the library yet, so it protects nothing until a later change wires it in.** The
published folders of the server are unchanged.

## What the library does

- A caller puts bytes (1 byte to 1 MiB) under a name in a partition, reads them back, deletes them and lists names.
  Each value is encrypted and authenticated by ASP.NET Core Data Protection, taken from the shared framework (no
  package), with the library's default algorithms. A value is tied to its partition, its name and its version: a
  record copied over another name or into another partition does not read.
- A record is one file, named by the SHA-256 of the name; names follow one rule and are never used as paths. A record
  is opened only when it is a regular file, not a link, of a plausible size.
- After a successful start every call returns or throws the library's one typed error, whose message holds no value,
  key, name or path.

## The key ring

- One key ring per partition, encrypted at rest: on Windows by DPAPI-NG; elsewhere with AES-256-GCM (a fresh 12-byte
  nonce, a 16-byte tag) under a 32-byte key file that must be a plain file with no permission for group or other.
- The data protection library is given no folder and makes no key: the store hands it only the ring entries it has
  read and checked itself. Every entry is checked at the start and around every key operation (a regular file; well
  formed; for a key, protected by the store's own decryptor and opening under it; no clear master key); before every
  write the ring on disk must still be, byte for byte, the ring last checked, or the write is refused and nothing is
  written.
- A key is made only at the first start of an empty partition and by `RotateKey`; keys do not end by time.
- Rotation is three calls: `RotateKey`, `Rewrap`, `RevokeOlderKeys`. `RevokeOlderKeys` refuses while any record is
  still under a key it would revoke; an overload revokes anyway and abandons those records.

## Limits (each is in the library's README)

- The Linux key file is not sealed: its owner and an administrator of the machine can read it. Its link check is by
  path, so a link swapped in at the moment of the open is not seen; its owner is not compared.
- No TPM, no Key Vault provider, no escrow, nothing for a pair of servers or a restore. Records are files, not rows.
- One process per partition. A second process must be stopped before a rotation; one that runs on refuses its writes.
- An older stored form of a record put back reads the older value; `Delete` then `Put` starts the version again.
- A read under a key the store already holds goes on while the ring on disk is damaged; the next write, key operation
  or start reports it.
- Whoever can write the store's folders can deny service (a revocation, a removed key, a planted file). On Windows the
  library sets no access list on its folders: the key ring there is only as safe as that list.
- Windows was run on a hosted build runner only, with the descriptor `LOCAL=user` the tests pass. The default
  descriptor (no option set) was refused on that runner: the store wrote nothing and the test skipped itself.

## What was run

The suite on macOS and on the hosted Linux and Windows jobs (at the branch head, which also holds main, 762 tests in
the solution, 0 failed on each); an independent review's attack program and its mutants against the library's code,
which the merge leaves byte for byte unchanged; the repository's own rule check and secret scan. Code scanning had not
run on this branch when it was reviewed: it runs on this pull request.

## Known follow-ups (not fixed here)

Each is a records or text item; none stops the merge. They are listed in order, the first the one to read.

1. **N1 Windows: a key planted under DPAPI-NG to a rule the store's account opens is accepted** and can become the write key
   at the next start; the planter knows its master key. DPAPI-NG does not authenticate who protected an entry; the store
   compares no rule. Owed: one README Limits sentence and the class summary's limits, at the latest with the host wiring;
   the installer sets an owner-only access list on the root (runbook line); backlog: compare each entry's rule with the
   configured one. DERIVED; UNMEASURED on Windows.
2. **N2** `RotateKey` can throw after its new key is written (the README's "none throws after its write succeeded" is
   untrue there). README sentence or a pre-check.
3. **N3** A partition folder that is a link is not refused; the store chmods its target to 700 and writes there.
4. **N4** A hard link in `keys/` has its target's mode set to 600 by the start.
5. **N5** The record folder is link-checked at the start only.
6. **N6** A clone of the store's own entry under a new id with the newest date becomes the write key at the next start, with
   an algorithm the cloner chose from the library's set; the master key stays secret.
7. **N7** Cells owed: a revocation alone with no record refuses (mutant n6 survives); the guard with a mixed set of records
   (n13 survives). Survivors that need concurrency or a crash to show: the per-record light check of `Rewrap`, the length
   re-check after an open, the repository's temporary file and move.
8. **N8** A ring left by the first commit of this branch carries 90-day keys; with generation off a single expired key
   stops writes. No such ring exists.

## What is left of the work package

The device registry, the state database and its migrations, the clock checks, the wiring of the store into the
server, a database-backed record store, the Key Vault provider, a sealed key, escrow.

The solution file gains this library's two lines in the ordinal order of their paths. No package, workflow or build
line changes. Every choice inside this change was made by the build's coordinator or by the builder; none is a product
decision. Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
