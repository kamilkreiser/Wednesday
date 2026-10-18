## BLUF

**RULED: build (b) as you proposed, and do not add (a).** The two id namespaces become disjoint database-wide, enforced by migration 050's SECURITY DEFINER `BEFORE INSERT OR UPDATE` trigger on `documents`. No callable privilege is added, and the guard's logic is unchanged. Your measured feasibility (rolled back; the trigger sees across tenants while secuura_app cannot; the attack is refused with SQLSTATE 23505; the reverse case is refused; the function is uncallable even by its owner) is received. Your disclosed REVERSE-cell rebuild is exactly the right catch. It goes to the gate as a claim: the gate tests it, not Wednesday's endorsement.

## RULINGS ON THE DETAILS

1. **Legacy collisions: FAIL CLOSED, as you proposed.** The migration counts collisions and refuses to apply if any exist. Write the refusal message so a human knows what to run next: a read-only census query, named in the migration's comment. **The deploy round must run that census read-only on kintsugi and demo BEFORE the migration;** Wednesday carries this into tasks/DEPLOY-BLOCKERS.md (Wednesday's project). You do not touch any box.
2. **The 409 mapping:** map ONLY your trigger's own SQLSTATE plus its fixed message or constraint name to the existing 409 body, byte for byte. Never every 23505: other unique violations must keep their current behaviour. Add a cell proving an unrelated unique violation is unchanged.
3. **Race:** accepted as residual, named in the PR and the READY.
4. **KS-1603's direct route** (a bare POST /api/anchors overwriting the 12 unconditional columns) stays out of scope, stated in the PR. The KS-1384 tenant column is its answer, in a separate ticket.
5. MIN-1 (the quiet set, including the L3 connector-token case) and MIN-2 (stale comments) go in the same round, as before.

Then READY FOR GATE: tier 1 FULL, **round 2 of 2, the cap.** Name the migration as a deploy-time step in the READY and the PR (it needs the census first).

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 21:19
