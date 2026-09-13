# Both seat notes are accepted. Two conditions on lane Q's compose grant, because pc-lane-a and Azure upgrade from your compose

**BLUF.** **For session 42 (seat hpsm-3e04). No reply needed; keep going.**
1. **Seat note 1 (directory DDL re-applied after the migrations over the superuser connection, guarded on `pc.tenant` existing, proven fresh AND on upgrade from 0014): ACCEPTED.** It is exactly ruling (i): superuser-owned, no pc_owner membership.
2. **Seat note 2 (lane Q's one-off grant on `compose.yaml` api environment/depends_on, and on the lockfile only if a pinned storage client is added): ACCEPTED, with two conditions.**
   - **(a) An upgrade must not break a live stack.**
     - The compose change publishes **no new host port**; any port stays on 127.0.0.1 and internal.
     - Every new api variable has a default that lets an existing stack (`pc-lane-a`, the Azure demo) start after upgrade.
     - Any variable a live stack MUST newly set goes into your SHA-and-env message to S40, **right under the D1 check, as a named pre-upgrade step.**
     - **Test:** an upgrade of a stack started from `b01c5a5`'s compose to the new head, with no new env, starts healthy. Otherwise the message to S40 names the required env explicitly.
   - **(b) The root-credential fallback for the object store is local-only.**
     - It is acceptable on the internal Docker network for Monday.
     - It goes to BACKLOG as you said, and it is a **named target in the combined tier-1 gate**.
     - The Azure demo must not expose the object store publicly; S40 checks its NSG and edge before switch-on.
3. **The rest of your ACK is noted as written:** lanes G and Q running; W on Q's contract commit; D1 line first in the S40 message.

## Unchanged
- No push. Switch OFF on every lane stack. A combined tier-1 gate is due before any push. Card c12 is still OPEN with Kam.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 13:28

Tuesday
