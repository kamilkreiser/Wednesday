# FOR RECORDS: OXPd 2 local secret store removal guard (kit B1920, lane S), gate G1 round 1, reader B1927

Not repository text. For the next OXPd records pass (backlog owed items 34 and 42, Jira `OXPD2-12`); nothing here was
written into the project. No person is named. Who decided: the coordinator (Tuesday), as coordinator; nothing here
says the product owner decided anything about this round.

## What lands

- One commit `253d217b` squashed onto main: six existing files under the store's two folders (product +74 -7, tests
  +133 -0 against `7b0f4f55`). C# totals +5 on both legs (1594 on main `83683af4`); skipped linux 4, windows 21
  (19 + 2: R18 and R19 designed skips); RULES 500 files; unit tests 111, floor 111. Public surface of
  `Datasec.Suite.Secrets.dll` unchanged (160 lines, byte for byte).
- Owed item 42(2) closes by the removal guard (U22; red at main by its own assertion).
- Owed item 34 N3 closes (R18), N5 closes (R19), N7 closes (R17, G03; each red only against its mutant).
- Owed item 34 N1, N2, N4, N6, N8 and item 42 (1), (3) to (6) unchanged.

## From this gate (for the backlog)

1. **Minor, owed (new residual of item 42(2), named in pr-body, not in the README):** the guard probes after the record
   was judged, so a failure of the protection that ends between the judgement's `Open` and the probe removes a good
   record (DERIVED from the code; not measured: it needs a timed fault inside the data protection library). Fix sketch:
   after a passing probe, judge the record again and remove only if it is still `DoesNotRead`. Owed before any caller
   of `DeleteUnreadable` is wired (item 42 (1)); nothing calls it today.
2. **Info:** the named residual (an older active key failing alone while the current key works) is narrower than the
   README says: the start's full check proves every non-revoked key makes an encryptor, and the light check before
   every removal proves the key source holds every active key's protecting key by id, so in-process it needs a failure
   after the start for that one key (DERIVED).
3. **Info, measured (probe P4):** a partition folder swapped for a link under a running store is not seen: `Put`
   returned 1 and wrote where the link points; `ListNames` listed 2. The README's "at the start only" covers it; the
   next start refuses it `StorageFailed` (measured).
4. **Info, measured (P1 to P3, P5):** an older active key's record with a changed payload byte, protection released:
   `StorageFailed`, file byte-equal; working: removed, the other record reads. A record whose stated name does not hash
   to its id, payload under the current key, protection released: `StorageFailed` (D2's one extra refusal); working:
   removed. A foreign partition's record and a non-record file under released protection: removed. A dangling record
   folder link: `StorageFailed` for list and write, nothing made at the target. `FileSecretRecordStore` over a link
   path with a trailing separator: refused `StorageFailed` (the check is not blinded by the separator).
