The local secret store's removal guard and three follow-ups: owed item 42(2) and owed item 34 N3, N5 and N7 of the
backlog. One commit on this branch (`253d217b`, parent `7b0f4f55`). Six existing files change, all under
`src/Datasec.Suite.Secrets/` and `tests/Datasec.Suite.Secrets.Tests/`. No file is added, and no public member,
`SecretStoreError` member, package, project, lock, solution or workflow file changes.

## Why

- Owed item 42(2): a failure of the decryption that is not the record's own read as a record that does not open, and
  `DeleteUnreadable` removed the record. Measured on macOS at `main`: with the store's own data protection services
  released under it, a good record under the current key was removed.
- Owed item 34 N3: a partition folder that is a symbolic link was not refused at the start.
- Owed item 34 N5: the record folder was link-checked at the start only.
- Owed item 34 N7: two behaviours had no cell (a key ring holding a revocation alone and no record; the
  `RevokeOlderKeys` guard with a mixed set of records).

## What changed

- `DeleteUnreadable` removes a record it judged unreadable through a private `RemoveUnopened`. When the record's
  payload names a key of the verified ring that is not revoked, a 32-byte random probe must make a protect and
  unprotect round trip under the current key (`ProbeRoundTrips`), else `StorageFailed` and nothing is removed. A
  record under a key the ring does not hold, or holds only as revoked, is removed as before.
- The start refuses a partition folder that is a link with `StorageFailed`, before it creates anything there.
- `FileSecretRecordStore` checks its folder by path at the top of `TryRead`, `Write`, `Delete` and `ListIds`
  (`RefuseLinkedFolder`), thrown as `StorageFailed`.
- README: the removal paragraph, the start's link checks, a new limit (both link checks are by path) and the removal
  limit rewritten to say what the guard catches and what it does not.
- Cells: U22, R17, R18, R19 and G03. R18 and R19 are skipped on Windows, as R10's link half is. No existing cell,
  helper or assertion changes.

## What proves it

- Red first on macOS arm64 against `main`: U22, R18 and R19 fail by their own assertions (Secrets assembly 94 cases,
  3 failed); with the change, all green.
- Mutants on the change (Secrets assembly, 94 cases): turning the guard off, inverting its key test or probing for
  every record turns U22 red; refusing every record not under an active key turns U04, U13 and U22 red; removing
  either link check turns R18 or R19 red; accepting a revocation alone turns R17 red; reading only the first record in
  the guard turns G03 red. With the earlier test files every one of these survives, so the new cells are what hold
  them.
- The public surface of `Datasec.Suite.Secrets.dll`, read by reflection, is the same before and after (160 lines,
  byte for byte); `ISecretStore` still has its four members.
- C# totals 1586 on both legs at the head (1581 + 5), skipped 4 on linux and 21 on windows (19 + 2), RULES 500 files,
  111 unit tests with floor 111. Merged with the current `main` the totals are 1594.

## Still open

- A key of the ring that is not revoked and fails alone while the current key's probe passes: its record is still
  removed. Not measured; it needs a fault inside the data protection library for one key.
- The guard proves the protection works after the record was judged, not at the same instant: a failure that ends
  between the judgement and the probe still removes the record. Not measured.
- Both link checks are by path; a link swapped in between the look and the file operation is not seen. The partition
  folder is checked at the start only: swapped for a link under a running store, writes go where the link points.
- DPAPI-NG on Windows is not measured. Owed items 34 N1, N2, N4, N6, N8 and 42 (1), (3) to (6) are unchanged.

## Who decides

The coordinator chose, as coordinator, to make the guard and the three follow-ups one change, and chose every choice
inside it: the guard scoped to records under an active key, the probe under the current key, the guard on every
unreadable verdict, `StorageFailed` for both link refusals, and the two designed Windows skips.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
