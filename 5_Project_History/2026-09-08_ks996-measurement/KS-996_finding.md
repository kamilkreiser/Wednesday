# KS-996 — MEASURED. The cascade explains 10 of the 95, not the population.

**For posting verbatim on KS-996 by the Secuura seat. Wednesday holds read-only tracker
access and does not write to the board.**

## BLUF
**The hypothesis is CONFIRMED but BOUNDED, and the bound is the finding.** Of the 95 archived
non-terminal tickets, **10 are cascade collateral** — their parent is archived at an *identical
`archivedAt` to the millisecond*. **84 have no parent at all** and therefore cannot be; 1 has a
parent that is not archived. **Three of the ten are `In Progress`** — live work, archived by a
side effect, invisible on the board.

**So "archiving swallowed the backlog" is wrong. Something archived 84 non-terminal tickets
deliberately, and that is a separate question this measurement does not answer.**

## THE FRAME, stated because it is load-bearing
`archivedAt != null`, state type not `completed`/`canceled`, **excluding the 21 in `Duplicate`**.

- With `Duplicate` excluded: **95** — which reproduces s149's figure exactly.
- With `Duplicate` included: **116**. The 21 Duplicates are the entire difference between the
  two numbers. **Neither count is wrong; they are different frames**, and s149's is the one used
  here so the two are comparable.
- Retrieved by **paginating to exhaustion — 14 pages, 1,354 archived issues**, with
  `hasNextPage` false on the last. **Not a cap equal to its own limit.**

## THE RESULT

    NO PARENT AT ALL               84   cannot be cascade collateral
    parent exists, NOT archived     1   cannot be cascade collateral
    parent archived TOO            10   candidates
       archivedAt IDENTICAL        10   DECISIVE for cascade
       archivedAt differs           0   would have closed nothing

## THE TEN, by parent

    KS-781 -> KS-796, KS-802
    KS-366 -> KS-371, KS-373
    KS-130 -> KS-131, KS-132
    KS-489 -> KS-774
    KS-488 -> KS-633
    KS-271 -> KS-227
    KS-160 -> KS-174

    states: In Progress 3 · Backlog 7

## THE CONTROL, because a discriminator that only says YES is not a discriminator
**The test returned NOT-cascade for 85 of the 95.** It can say no, and it did, for the large
majority. That is what makes the 10 a measurement rather than a pattern found by looking for one.

**Its one-directional limit, kept from the original ruling:** an identical millisecond is decisive
FOR cascade. A differing one would have closed nothing — here there were none, so the limit was
never load-bearing.

## WHAT THIS DOES NOT ESTABLISH
- **Why the other 84 are archived in non-terminal states.** They may be deliberate; archiving a
  dead backlog item is a normal act. Nothing here says otherwise.
- **When the ten were archived, or by whom.** The timestamps pair them to their parents; they do
  not attribute the act.
- **Whether any of the ten should be restored.** That is a board change and it is Kam's — carded.

## PROVENANCE
- All figures | Linear GraphQL, read-only, Secuura project key, paginated to exhaustion in one
  action | read 2026-09-08
- s149's 95 | its 00:44Z mail | read 2026-09-08
- The cascade mechanism itself | s149's measurement of today's own pass (KS-918/KS-920, delta
  −25 vs −23, both restored) | relayed, not re-derived by Wednesday | read 2026-09-08
