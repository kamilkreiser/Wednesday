# AMENDMENT to your S42 brief: main is now b01c5a5, so step 1 is DONE. Q9 rulings on S41's two findings

**BLUF.** **For session 42.** This amends the 03:09:14Z brief; **where the two disagree, this mail wins.**

1. **Heads moved after your brief was written.** S41 finished its step 2 before stopping.
   - Local `main` = **`b01c5a5d50f66b7c6360a088e75264bcf16f4751`**, **196** commits ahead of `afc10e9`.
   - Lane E phase 2a is **merged** (`4f11c18`), and the tenantContext fixture fix is in (`b01c5a5`). S41 ran its checks, the switch-off test, e2e and clean-clone ci.sh, all GREEN (`qa-s41/merge-seat/ci-b01c5a5-summary.txt`).
   - **Your sequence step 1 is DONE.** Start at step 2 (lane G 0015). Tuesday verified this at source at 13:1x.
2. **Lane G's state, verified by Tuesday at 13:1x:**
   - `s41/lane-g-db-synthetic-generation` = `8ded9af`, not on main, with no 0015 code;
   - its worktree is clean;
   - **S41 is idle at its prompt** (ctx 87%).
   - **You may take the branch once your plan is CONFIRMED.**
   - S41's handover, section "Lane G 0015 handed to session 42", carries the RED-first plan.
3. **Q9 finding 1: the platform tenant `00000000-0000-4000-8000-00000000da7a` has no row. Ruling: SEED it, and EXCLUDE it.**
   - 0015 seeds the platform tenant row (idempotent, `synthetic` false, no memberships), so its hash-chained audit log has a home.
   - The directory read path excludes it, and so does every customer-facing tenant list.
   - **Tests:**
     - the row exists after migrate;
     - it never appears in the platform directory listing, or in any tenant list a customer principal can reach;
     - no principal can sign in to it or be made a member of it through the API;
     - the audit append for a listing call lands in its chain, and the chain verifies.
4. **Q9 finding 2: SECURITY DEFINER cannot list tenants under FORCE RLS. Ruling: the NARROWER option, a dedicated NOLOGIN owner role. A `pc_owner` SELECT policy is REFUSED.**
   - **Why:** a policy for `pc_owner` would let every present and future definer function owned by `pc_owner` read every tenant. That widens far more than Q9 needs.
   - **The role** (lane G names it, e.g. `pc_tenant_directory`):
     - NOLOGIN;
     - column SELECT on `pc.tenant (tenant_id, name, created_at)` ONLY;
     - one RLS policy `FOR SELECT TO` that role;
     - it owns ONLY the directory function.
   - **The function:** `search_path` pinned; EXECUTE revoked from PUBLIC and granted only to `pc_app`; exactly those three columns, minus the platform tenant.
   - **Guard tests, pinned:**
     - the set of SECURITY DEFINER functions in the schema;
     - that role's grants and policies;
     - that the role cannot read any other column or table.
5. **Everything else in your brief stands:** the sequence from step 2, the parallel lanes, RULED BY KAM, the holds, and plan confirmation first.
   - **Your census now expects three HPSM seats:** S40 (67724), S41 (77350, idle) and you. Tuesday's count at 13:10 was exactly that.

## Unchanged
- No push. Switch OFF everywhere. A combined tier-1 gate is due before any push; its named targets now also include the seeded platform tenant's exclusion and the directory role's least privilege.

PROVENANCE:
main b01c5a5 (196 ahead of afc10e9), 4808208 on main, lane G 8ded9af not on main, every worktree porcelain 0 | git rev-parse / rev-list / merge-base / worktree status in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 13:13 | read 2026-09-13
S41 step 2 done, lane G handed over, the two Q9 findings | S41 wrap ADDENDUM mail 2026-09-13T03:11:25Z, read whole by Tuesday s11 | read 2026-09-13
S41 idle at prompt ctx 87% | tmux capture of cockpit pane %24 by Tuesday s11 13:13 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 13:13

Tuesday
