# STATUS ea8bd1f noted; two backlog candidates promoted (they are Kam's explicit requirement)

**BLUF.** **For session 41 (seat hpsm-982d).** Your status is noted, and the sequence is right. **Two of your six backlog candidates are NOT backlog: fix them before the demo switch goes on, RED-first, merged by you.**

1. **`release_artifact.generated_at` is caller-written: fix it.** The server sets it, and the caller cannot supply or override it.
2. **Client and engagement names on artefacts are not checked against their rows: fix it.** The names are derived server-side from the engagement and tenant rows at generation time, never taken from the caller.
   - **Why both:** Kam asked in his own words that every stored report carry *"the client details for which client it was generated and by whom"*. Until these two are fixed, a report can name the wrong client, or the wrong time, while looking authoritative.
   - **Owner:** lane E phase 2a if it is already in those files, otherwise a disjoint lane. Your call.
   - **Tests:** a caller-supplied time or name is ignored or refused, and the stored artefact matches the rows.
   - **Both are named attack targets in the combined tier-1 gate.**
3. **The other four stay BACKLOG as listed:** intake accepting unserved ids, the long-name Preview band, `@item` in the evidence matrix, non-transactional registration. The long-name length cap needs a ruling later, not now.
4. **Card `hpsm-composer-demo-release-unreachable-c12` is still OPEN with Kam.** Nothing is built on C12.

## Unchanged
- SWITCH ON sequence: lane E 2a (parts 1 and 2), then the default-OFF compose change, then your ON proof, then the SHA and env to S40, then pc-lane-a, then Azure. No push. A combined tier-1 gate is due before any push.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 12:59

Tuesday
