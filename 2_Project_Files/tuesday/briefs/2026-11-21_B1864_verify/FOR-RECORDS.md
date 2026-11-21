# FOR RECORDS: WP1.1, the secret store listing and removal (lane SL), round-2 delta check

For a records pass after the lane lands. Nothing here was written to the project.

## Runbook (`SETUP_RUNBOOK.md`, check table)

- Local totals, measured by this reader through the wave lock:
  - head 8578d96c alone: 920 (899 + 14 + 7), failed 0, skipped 4; RULES: clean (295 files); build/tests Ran 60
  - merged with main 977cbeb2: 1191 (1170 + 14 + 7), failed 0, skipped 4; RULES: clean (370 files); build/tests Ran 60
- The lane's own count is 21 tests, all in `tests/Datasec.Suite.Secrets.Tests/InventoryTests.cs`.
- The descriptor cell (U16) lowers the process's open-file limit; it runs alone in the collection `process-limit-alone`,
  and does nothing on Windows.

## The store's README (already in the lane)

The store's README states the listing, the removal and the limits. Records only: the round-1 FOR RECORDS line that
listed "a record file of mode 000" among the records the removal destroys is superseded (such a file is now refused
with `StorageFailed` and left for an operator).

## BACKLOG (`BACKLOG.md`)

1. Who may call `DeleteUnreadable` in the product is open; nothing calls it at main 977cbeb2.
2. Before a product caller is wired (D22 (a)): a decryption failure that is not the record's own reads as a record
   that does not open, and the record is removed. Measured here on macOS with a key source that fails one decryption:
   the store decrypts its keys when it starts (a failure there makes it refuse to start, `KeyNotAvailable`) and made 0
   key decryptions during a later listing, removal and reads. What stays open (DERIVED, not measured): a refresh of the
   data protection library's key cache in a long-running store, the same on Windows under DPAPI-NG, and a process
   fault inside the decryption (`Open` maps every exception but the store's own to `UnreadableRecord`). Smallest guard
   if a caller needs it: when the record names a key that is active in the verified ring, refuse the removal unless the
   decryption failed as an authentication failure.
3. A second process over the partition writing without changing the key ring can still race the removal (named in
   the README; one process per partition is assumed).
4. `EIO` and `ENFILE` take the open-failure path by source reading; only `EMFILE` is measured (and then the ring check
   meets the fault first: `KeyNotAvailable`).

## Notes of this check

- The builder wrote a note into its own assistant memory folder (outside the project and outside the kit's closed list
  of paths). No project file is affected.
