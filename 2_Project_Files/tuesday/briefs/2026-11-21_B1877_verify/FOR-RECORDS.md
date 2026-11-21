# FOR RECORDS: OXPd 2 adapter lane (WP1.2 in part, lane E), gate round 2, reader B1877

Not repository text. For Tuesday's records pass (backlog, design notes); nothing here was written into the project.

## What landed in this lane (both commits, squashed)

- Device/: per-device solution-token holder; lazy refresh and refresh on 401, never on a timer; one retry of the
  same request; NeedsRepair on a second 401; rotation written before use; single flight per serial with completed
  flights counted (a waiter uses the result of the flight it waited for: access value or failure); a grant copies
  both values and checks the access value; Forget during a refresh stores nothing (per-entry generation under the
  entry's lock; the refresh ends NoRefreshValue).
- Callbacks/: callback credentials (32 random bytes, 43 base64url characters, SHA-256 stored, fixed-time compare);
  Forget deletes the vault record first; Issue and Forget bump a per-serial generation, and a cache fill whose
  generation moved is never cached; five handled callbacks in a fixed check order; 14 outcomes, BodyFailed appended
  last; HandleAsync throws only ArgumentNullException and the caller's own cancellation.
- Local totals: branch 1234 -> 1248 (57 lane tests); rules files 402 -> 403. Merged with main 5bb1418c: 1392 tests,
  443 files (MEASURED by this reader).

## Named limits (state in the README at the next records pass; today only the timing one is in the README)

1. StoreRefreshValue during a refresh is followed by that refresh's result, and a request that waited on that
   refresh gets the same result. Measured (probe G18 (a)): Forget then StoreRefreshValue while A's refresh runs and B
   waits: A and B both NoRefreshValue though the vault already holds the new value; the next request succeeds with 1
   more endpoint call.
2. An access value handed out before Forget may still be sent once by the request that holds it (DERIVED).
3. The vault call of a rotation and of Forget runs under the serial's lock (a slow vault holds that serial's callers;
   UNMEASURED with a real store). Dispose takes the instance lock and then each entry's lock, so a Dispose that meets
   a slow vault call under an entry lock also holds every other serial's Entry lookup for that time (DERIVED).
4. Enrolled-serial timing of the vault lookup (in the README).
5. The Issue rotation cell is held by two mechanisms (generation and first-fill-wins): no single mutant of Issue's
   generation bump reddens a cell.
6. Tuesday's item 4: a credential digest read from the vault but not cached (lost fill, or Issue/Forget during the
   read) and a wrong-length read are dropped unzeroed (`CallbackCredentials.cs:178-181`, `:187-190`, `:192-198` at
   610bb7d2). Reader view: records, at most Minor (a SHA-256 of a 256-bit random value, not the credential, not
   usable to authenticate, and the same digest is cached for the instance's life). Two ZeroMemory lines and a cell
   in a later lane if wanted.
7. B1868 F4 / B1869 F6: a refresh answered after RefreshTimeout is discarded with any rotated refresh value; an
   endpoint ignoring its token overlaps the next refresh (G13 at 610bb7d2: 2 in flight, the late rotated value not
   stored). NOT DECIDED item 3 of the kit (whether to keep a late grant).
8. B1869 F7: a 401 after a failed refresh gets that failure with no endpoint call (unchanged by the fix).
9. B1869 F8: a wrong-length stored hash reads as a stranger (Unauthorized), not Unavailable.
10. B1869 F9: the holder zeroes the array TryGet returns and the credential cache keeps and later zeroes it: a vault
    binding must return a fresh copy (one line on IDeviceSecretVault.TryGet and in the README).
11. Forget whose vault delete throws during a refresh: Forget reports VaultFailed, the refresh stores nothing and ends
    NoRefreshValue, the old refresh value stays in the vault (probe G18 (b)); consistent with the exception, worth one
    README sentence.

## Not decided (unchanged from the kit)

- Whether a stranger's unknown serials are cached negatively (B1868 F6, B1869 F2).
- Whether a refresh answered after RefreshTimeout is kept (item 7 above).
- Round 1's NOT DECIDED items 1 to 7 (bindings, how the host learns the serial, solution notifications, device-facing
  questions, administrator password, customer-facing words).
