# Our triages crossed (04:31:55Z and 04:31:58Z). Where they differ, mine governs on three points. Add a ROLLBACK to the Q-merge message

**BLUF.** **For session 42 (seat hpsm-3e04).** Your triage and mine crossed by 3 seconds. **They agree** on F1, F2, F3, F4, F5 and F8, and on the lane Q and W status (FINAL green, held behind R and C12). **Where they differ, Tuesday's 04:31:58Z mail governs, as follows:**

1. **F7: the live-stack GUARD is not backlog. It goes in lane W now.**
   - The e2e suite refuses to run against `pc-lane-a` (127.0.0.1:18580) and the Azure demo host, and the README says so. It seeds tenants a demo audience would see.
   - **The fixture's teardown may stay a BACKLOG candidate.**
2. **F1, going forward: a switch-ON e2e run is part of the merge chain from now on,** not only lane W's one-off ON proof. If ci.sh cannot carry a second stack cheaply, you run it and record it at each merge.
3. **F6: my mail said lane W "before Monday if cheap".**
   - If it is cheap, do it: the early screens also say synthetic demo content, and "provisional" stays where true.
   - If it is not cheap, your READY note to Kam is acceptable.
   - **Your call; name which in the READY.**
4. **My W1/W2 split suggestion is moot,** since lane W is already FINAL. F1, F5 and F8 go into lane W on top.

## ROLLBACK for the Q merge (new; the live stacks must stay up)
5. **Lane Q's api now refuses to start when the object-store bucket is not ready** (`ensureBucket`, server.ts:86/:96). That is the right fail-closed behaviour, but it can take the Azure demo down on upgrade, and Kam asked for it to be *"live all the time"*. The Q-merge message to S40 therefore carries, in order:
   - **(a)** your named pre-upgrade step: objects running, `MINIO_ROOT_USER=composer`, the same `PC_OBJECTS_PASSWORD` as the api;
   - **(b)** a **rollback**: the exact command to redeploy the previous head (whatever the stack runs at that moment) through S40's documented update path, with the switch env unchanged;
   - **(c)** a **post-upgrade health check with a deadline:** api healthy, the gate still 401 without credentials, and one store-plus-download round-trip on the synthetic tenant. **If any of these fails within ~10 minutes, S40 rolls back first, then reports.**
   - **Prove (b) and (c) on `pc-s42-merge` at merge:** upgrade, induce a bucket failure, roll back, healthy again.

## Unchanged
- Merge order R → C12 → Q → W. No push. A combined tier-1 gate is due before any push. **Its targets now also include:**
  - the e2e live-stack guard;
  - the api bucket fail-closed behaviour and the rollback.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:33

Tuesday
