## BLUF — you are at 50% context. CHECKPOINT, not a rotation. Three things, then carry on.
**1. Refresh `HANDOVER-s147.md` NOW**, while you have the room to do it well rather than under
pressure. **2. Start nothing that will not fit.** **3. Keep going** — 50% is not a wind-down.

## WHAT THE HANDOVER MUST CARRY, because your successor lands on it and nothing else
- **The PR board with its holds and WHY each is held**, not just its state: #889 `9898ae724` held on
  **Kam's** trust-boundary ruling (carded, not yours) · #891 **Kam's own click** · #892 `f54b2dce1`
  **gate live, verdict goes to Wednesday** · #893 `ab1053141` **gate QUEUED behind #892 — queuing is
  not acceptance** · develop `6c60cc09b`, demo still `632f16dfe`.
- **KS-970's remaining items 1, 2, 4, 6**, with item 1 leading and the reason: `/reset` with a
  whitespace-only `tenantId` silently retargets the caller's own bucket **and answers 200**.
- **KS-968 is UNMEASURED, not clear** — the probe returned zeros from an instrument nobody has shown
  can return non-zero. **The control query is carded to Kam with default STOP. Your successor must not
  run anything on that box on silence**, and must not read the zeros as an all-clear.
- **Your standing rules:** force-push narrow-allow (own unshared branch, both checks proven with
  controls, then `ALLOW_FORCE=1`; anything shared is Kam's) · the `:6882` stack's DATA is untrusted
  until re-seeded · build your own environment from the repo's provisioning path, confirming the
  migration you depend on **by name** · **anyone quoting "the 12" or "the 8" names the predicate**.
- **The two method rules you produced today**, in your own words, because they are yours and a
  successor will need them: *"a comment that claims a behaviour should be a cell, not prose"* and
  *"I am not going to be the one who ships it because the answer happened to be convenient."*

## THEN CARRY ON
Take KS-970's items in order. **Hand over rather than starting an item that will not fit** — a
half-built behaviour change is worth less than a clean boundary. **Mail each leg; that mail is the
wake.** When you approach your band, wrap and Wednesday relaunches. **Nothing is waiting on your seat
except the queue itself**, so there is no reason to push past a clean stopping point.
