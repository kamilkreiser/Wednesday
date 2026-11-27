# FOR RECORDS: gate B2210 (lane L1x, OXPd 1.x context calls, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **Lane L1x (plan r2 row C12) DONE when the squash lands:** `Oxpd1ContextCaller.CallAsync` makes one of six calls of
  the closed list `Oxpd1ContextKind` (reserve and release of an authentication context; open, start reading, stop
  reading and close of an HID accessory) with the guest user over the client's pinned connection, each a dry run unless
  asked and each carrying its undo when it may have taken effect; a reserve is answered only with one context id of
  HP's nonce form. Cells N01 to N10 (39 cases) against the stub; eight mutants turn them red. Against a stub only: how
  an M577 answers each call, and whether it accepts guest for them, is UNMEASURED (RELAYED from the kit's FOR RECORDS).
- **Not built:** where an accessory context id comes from (lane L8), the report events the device sends (lane L8), a
  scrub of the context ids in the client's record (R10), any call beyond the six (RELAYED).
- **Unblocks:** lane L1 (the agent host) calls this class; L6 and OX-A may start on the module after it lands (plan r2
  lines 85 and 87, RELAYED from the kit).
- **Owed to lane L1 (the agent host), from this gate's reads and runs (VERDICT.md):**
  1. `CallAsync` can THROW after an executed request left (findings F1 and F4): a caller cancellation in flight, and a
     reserve whose returned id the client's mask changed. The host treats an exception from an executed reserve, open
     or start of reading as "may have taken effect": for an HID call it sends the close / stop of the id it holds; for
     a reserve it has no id (as R11).
  2. The host undoes a start of reading before an open (HP, `accessories.wsdl:634`), and keeps a reserve's id for the
     release (RELAYED from the kit's FOR TUESDAY).
  3. The `Oxpd1Client` it hands in is the host's to build, own and dispose.
- **Open for the coordinator (not blocking):** F1 (a mask-changed reserve id throws out of `CallAsync`: a one-line
  in-lane fix, `IsNonce(contextId)` before the undo factory, ending `MalformedAnswer` with no id, or a client change
  so the reserve's result is not masked); F2 (the guest request's password is the device admin password setting's
  value, the landed guest sender's choice: an OX-A item for a separate, non-secret guest value, which HP's quoted
  "password={anything}" admits; that quote is in the landed echo summary, not in a committed contract file).
- Nothing here ran against a device or a tenant.
