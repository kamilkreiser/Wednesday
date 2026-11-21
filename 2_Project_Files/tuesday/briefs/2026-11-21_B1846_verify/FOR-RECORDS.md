# FOR RECORDS: gate B1846 (OXPd 2, lane C fix round, head 9d49695 on main 5e36d8d)

What a records pass should file once the head lands. The gate wrote none of it into the project.

## Closed by commit 9d49695 (once landed)

- **F1 of gate B1830** (public lists handed out their backing arrays): CLOSED. My own walk covered every public
  static member (1238) of the adapter's 1445 public types, every adapter object reached from them (8496), and every
  collection reached (1510). 0 writable, 0 of 3016 identity writes accepted, 0 of 43962 non-identity writes accepted
  (clearing Required on every property of 4362 schemas, replacing enum values, swapping operations, replacing content
  types, through `IList<T>`, `IList` and array casts). The targeted-case digest and the round-1 callback case were
  the same before and after (`MissingRequired at $.usbCallback`). Against the base adapter the same program found
  exactly the four members and changed later parses (control fired).
- **F2 of gate B1830** (an `OverflowException` from a client at a body limit near `int.MaxValue`): CLOSED by refusing
  the limit when it is made. `Array.MaxLength` 2147483591 and `HighestMaxBodyBytes` 2147483590, measured on .NET
  10.0.15 arm64. 3618 client calls (all 201 methods, 9 small answers, depth 32 and 4096) at the highest accepted
  limit: 0 exceptions.
- **F3 of gate B1830** (no cell for counting string lengths in scalar values): CLOSED. My mutant m8 now turns 5 N9
  cases red by assertion, and 311 of my own 5128 targeted cases change under it (0 on the head).

## The runbook line (behaviour change, accepted at the kit's stamp)

`Oxpd2ParseLimits` refuses a `maxBodyBytes` above `Oxpd2ParseLimits.HighestMaxBodyBytes`
(`System.Array.MaxLength - 1`; 2147483590 on .NET 10.0.15) with `ArgumentOutOfRangeException` naming `maxBodyBytes`.
`int.MaxValue - 1`, accepted before, is now refused.

## Records points of this gate (none blocks the merge)

- **R1.** The kit's control row K4 said the client-edge cell is "proved by mutant mBig". It cannot be: the edge value
  never overflowed, so no mutant of the bound reddens it. Builder's deviation 2 says this, and my base run agrees
  (0 exceptions at `Array.MaxLength - 1` on the base adapter). For future kits: F2's proof is the constructor cell
  (K3 with mBig); the client cell is a regression guard with no red of its own.
- **R2.** Stamp S1 of kit B1834 says "kit 202 lines". `wc -l` prints 201, and the file ends with a line feed.
  Builder's deviation 5.
- **R3.** `Oxpd2Schema.PropertyArray` is `internal`, and the adapter's `InternalsVisibleTo` names
  `Datasec.Suite.Contracts.Tests` by simple name with no public key. So any assembly in the process that takes that
  name reaches the arrays without reflection (the gate's probe takes that name to see internals, and it did not use
  this member). This is the same power reflection already gives (the kit's named limit H6). A later lane that loads
  plug-ins in the server process should know it.
- **R4.** N9's astral rows visit the first two bounded string sites of each operation (lane C's `Take(2)`). My own
  626 astral and non-ASCII length cases cover every site my spec reading reaches. The limit is named in the
  builder's STATUS.
- **Still owed from gate B1830:** F4 (process: prune `tools/certificates` from any R5 hash run), F5 (firmware enum
  drift and optional nulls on callbacks: decide before WP1.2 wires callbacks), F6 (N11 moot today; a client lets an
  `IOException` from the body stream through), F7 (credential-shaped fields in device-answer models: the logging
  deny-list lane).
