# Fleet claims — who is working on what, across Wednesday seats

**Why (Kam, 2026-09-08 10:17 + 10:19, one instruction across two messages):** *"with two agents we
need to … ensure you get instructions and as you take on a task so that the other agent knows who is
working on what and vice versa."*

## The design, and why it is per-seat files
**One file PER SEAT. A seat writes ONLY its own file and never another's.**
That is not a rule to be policed — it is the structure. Two seats can never conflict on a file only
one of them writes, so the shared-file race that nearly deleted four of Kam's rulings on 2026-09-07
cannot happen here by construction.

    claims_studio.md   the Studio seat  (currently: SECUURA only, Kam 2026-09-08 07:08:23)
    claims_laptop.md   the laptop seat  (currently: DATASEC)

**Sync is git.** Both seats push to `kamilkreiser/Wednesday`, so a claim is visible to the other seat
after its next pull. **A claim is therefore eventually-consistent, not instant** — see the honest
limit below.

## The protocol
1. **Before starting a task**, read the OTHER seat's file. If it claims the same thing, do not start
   — mail the other seat and let Kam know one of you is standing down.
2. **On taking a task**, add a line to YOUR file and push. One line: what, which client/project,
   when, and the ticket or PR if there is one.
3. **On finishing or handing over**, mark it done in the same line rather than deleting it — the
   record of who did what is the point, and deletion loses it.
4. **At a rotation**, the successor inherits the file as-is. It is the seat's claim, not the
   session's.

## The honest limit, stated rather than discovered later
**This is eventually-consistent and it is not a lock.** If both seats claim the same task inside one
pull interval, both claims land and neither seat sees the other's until it pulls. **It reduces
collisions; it does not prevent them.** The thing that actually prevents them today is the client
split Kam set (Secuura here, Datasec on the laptop) — this file makes that split VISIBLE and catches
the cases the split does not cover: fleet work, the vault, WED tooling, anything unowned.
