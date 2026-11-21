## What this adds

Two commits on one branch, landed as one squash. The local secret store (work package WP1.1) gains a second interface,
`ISecretStoreInventory`, with two members: `ListAll()` and `DeleteUnreadable(recordId)`. One line registers it beside the
store. `ListNames`, the record store, the key ring, `ISecretStore`, `ISecretStoreMaintenance` and every existing test
file are unchanged. 21 new tests in one new test file (the branch's suite: 920). No package, no workflow line, no build
file and no other project changes.

The first commit adds the listing and the removal. The second makes the removal refuse whatever it cannot judge from
the record's own bytes, and makes it run the key-ring check every write runs first.

## What the listing does

- `ListAll()` judges every record exactly as `ListNames` does (the stored form parses, the SHA-256 of the name it states
  is its id, that name follows the name rule, its value opens) and returns every name that reads, in ordinal order, plus
  one entry per record that does not, in the order the record store lists the ids. It never throws for a record that
  does not read.
- An entry that does not read carries its id and, only where its stored form parses, the name follows the name rule and
  hashes to the id, the name it states. **That stated name is not authenticated:** whoever can write the records folder
  can plant a record that states any name the rule allows, at the id of that name. No entry carries a value or a version.
- A record whose file the store cannot read at all (see below) is listed with no stated name, as `ListNames` throws
  `UnreadableRecord` for it. A folder, or a link to a folder, at a record's path is not listed.
- A failure of the record store itself (for example a listing of the records folder that fails) is `StorageFailed`,
  with nothing listed.

## What the removal does

- `DeleteUnreadable(recordId)` refuses an id that is not 64 lower-case hex characters with `InvalidName` before
  anything is touched.
- Under the store's lock it first runs the check every write runs: the key ring on disk must be the one this store last
  checked and, elsewhere than Windows, the key source must still hold its keys. Otherwise `KeyNotAvailable`, and nothing
  is removed. So a second store after another one rotated, and a running store after a revocation was moved out of the
  key folder, refuse the removal as they refuse a write.
- It then reads the record again and removes it **only when its bytes were read in full and fail as a record**: they do
  not parse, the stated name does not hash to the id, the name breaks the rule, or the value does not open with the keys
  this store holds. A record that reads, or is absent, returns false and is left as it is.
- **A file the store cannot open or read is never removed**, for any reason: no file descriptor left, a file held open by
  another opener without read sharing, a file of mode 000. Neither is a path that holds no plain record file: an empty
  file, a file larger than a record can be, a link, a pipe, a folder, a link to a folder. The call throws `StorageFailed`
  and an operator moves such a file. A failing delete of the record store is `StorageFailed` too.

## Limits (also in the store's README)

- The removal is for good. It still removes the records under a key this store revoked with `RevokeOlderKeys(true)`
  while the way back (moving the revocation out of the key folder) is open, and, in a store started after a key entry
  was moved out, every record under that key.
- A failure of the decryption itself that is not the record's own (for example DPAPI-NG not available on Windows at that
  moment) reads as a record that does not open, and the record is removed. Not measured.
- With a second process over the same partition and no change of the key ring, the re-check is atomic only against
  callers of this store: a record the other process writes again between the re-check and the removal is removed. One
  process per partition is assumed.
- `Delete` of a stated name removes exactly that record only at the moment of the listing; `Delete` re-checks nothing.
- The listing opens every record: one decryption per record, as `ListNames`.
- **Nothing in the product calls `DeleteUnreadable` yet**, and the host does not use the store yet. Who may call the
  removal is still open.

## What the tests prove and do not prove

Every value, key and record in the tests is synthetic and made at run time. The descriptor test runs on Unix only (it
asserts it is on Windows and returns there); the sharing test's refusal is measured on macOS and ran green on the
hosted Windows and Linux legs. No test makes DPAPI-NG itself fail. Nothing is deployed; nothing was sent.
