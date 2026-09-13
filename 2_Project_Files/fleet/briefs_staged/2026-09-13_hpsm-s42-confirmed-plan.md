# CONFIRMED: S42 plan (lanes G, Q, W + merge seat). D1 and D2 accepted with conditions; lane G's ownership trap ruled; "no sign-in" defined

**BLUF.** **For session 42 (seat hpsm-3e04). Your plan is CONFIRMED as written, including the parts not listed below. Lanes start now.**
- **Tuesday checked at source (13:20):** census shows three HPSM seats (67724, 77350, 98162); main `b01c5a5`; lane G `8ded9af` with a clean worktree; S41 `%24` idle at its prompt (ctx 87%).
- **S41's pane will be closed by Tuesday after this mail.** Its stacks stay down and its volumes are kept, as the handover says.
1. **D1: (a) ACCEPTED, with one condition.** The api refuses to start when `PC_PLATFORM_TENANT_ID` has no tenant row. RED-first in lane Q.
   - **Condition:** this can take a live stack down on upgrade. **Your SHA-and-env message to S40 must say, in its first lines, that S40 checks `PC_PLATFORM_TENANT_ID` on `pc-lane-a` and on Azure BEFORE upgrading.** It must be unset or equal to the seeded default. If it differs, S40 stops and asks Tuesday.
2. **D2: ACCEPTED.** Lane Q builds phase 2b (stored per-client outputs, Kam's own ask) before the Q9 API. Q9 is off the switch-on path.
3. **Lane G's ownership trap (pc_owner cannot give the function to a role it cannot SET ROLE to). Ruling, in order of preference:**
   - **(i) Preferred:** create the role, the function and its ownership in `bootstrap.sql`, over the superuser connection that already runs on every migrate. **pc_owner gets NO membership in the directory role.** 0015 then holds only what pc_owner can own. It must be idempotent: CREATE OR REPLACE, and ownership re-asserted on every run.
   - **(ii) Only if (i) is measured impossible:** do not build a membership fallback. **Bring the measurement to Tuesday first.** Even WITH INHERIT FALSE, a membership that permits SET ROLE lets any pc_owner session become the directory role. That is the widening already refused, by another route.
   - **Guard tests, whichever path:**
     - pc_owner is not a member of the directory role (`pg_auth_members` pinned);
     - pc_owner cannot SET ROLE to it;
     - the definer-function set is pinned;
     - the role's grants and its single policy are pinned.
4. **"No sign-in to the platform tenant" means:**
   - no tenant-scoped session operating on that tenant's DATA (engagements, policies, artefacts, memberships);
   - no membership rows on it (your DB refusal is accepted as defence beneath the API);
   - no customer principal ever selecting it.
   **A platform_admin token that carries the platform id as its authority context is ALLOWED,** provided it grants no tenant-data access inside that tenant. Test it that way. If lane Q measures something that still conflicts, bring it before building, as you planned.
5. **S40 channel:** `claude-bridge` reported CONNECTION_CLOSED at your boot. If the cross-session message does not deliver, use a seat-addressed mail to `datasec-hpsm@`, subject naming seat hpsm-dc13, the way S41 did, with a copy to Tuesday. **Delivery is read back either way.**
6. **Records:** as planned. The 30 stale `(conflict_on_2026-08-25|26)` sync copies stay untouched; Tuesday tells Kam. The orphan `tail` PID 31948 is left alone.

## Unchanged
- No push. Switch OFF until your ON proof and S40's checks. A combined tier-1 gate is due before any push. Its named targets now also include:
  - the api startup refusal (D1);
  - the directory role's non-membership and the SET ROLE guard;
  - the platform tenant's exclusion and data refusal.
- Card `hpsm-composer-demo-release-unreachable-c12` is still OPEN with Kam.

PROVENANCE:
census 67724 / 77350 / 98162 only | ps run by Tuesday s11 13:21 | read 2026-09-13
main b01c5a5, lane G 8ded9af, lane-g worktree porcelain 0 | git rev-parse + status (--no-optional-locks) in Datasec/HPSM 6_Policy_Composer, run by Tuesday s11 13:21 | read 2026-09-13
S41 idle at prompt ctx 87% | tmux capture of cockpit pane %24 by Tuesday s11 13:21 | read 2026-09-13
S42 plan, D1, D2, lane G trap, claude-bridge closed, sync copies | S42 plan-confirmation mail 2026-09-13T03:18:59Z, read whole by Tuesday s11 | read 2026-09-13

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 13:21

Tuesday
