# S40 verifier on 7135dec noted. Triage of F1–F8: the demo-visible web fixes go before Monday, and the e2e suite must pass with the switch ON

**BLUF.** **For session 42 (seat hpsm-3e04), copy to session 40 (seat hpsm-dc13).**
- **S40's independent verification of `7135dec` is noted: GREEN end to end.** Host 910, clean-clone ci.sh 16/16, demo-ON stack, the fence's positive control, S1→S10 with 0 console errors, both Export PDFs, technical approval.
- **S40: stand by for S42's next upgrade message.**
- **S42: rulings on the eight findings below.**

1. **F1 (e2e suite RED on a demo-ON stack: 0 passed, 20 failed, 14 not run; the fixture seeds non-synthetic tenants): FIX BEFORE MONDAY, lane W (`apps/web/e2e/**`).**
   - **Why:** the switch-ON configuration is exactly what Kam reviews and what both live stacks run, yet CI's stack is switch-OFF, so today nothing proves the web works on it.
   - **The fixture** seeds tenants that fit the stack's switch state: `synthetic: true` when ON, so a positive-control engagement is not refused.
   - **The suite must pass on BOTH** a switch-OFF and a switch-ON stack.
   - **The merge chain gains an e2e run on a switch-ON seat stack from now on.** If ci.sh cannot carry a second stack cheaply, the merge seat runs it and records it.
2. **F7 (the fixture leaves "E2E …" tenants with memberships): with F1, lane W.**
   - The fixture tears down what it creates.
   - **The e2e suite is NEVER run against `pc-lane-a` or the Azure demo.** Write that into the suite's README and its guard, e.g. refuse the known live ports and host.
3. **F5 (Approval screen's "Failing terms" still lists "Technical review approved" after that approval): FIX BEFORE MONDAY, lane W.** Kam will click through approvals on the demo, so the screen must not contradict the API. Either re-read the terms after an approval, or state plainly that they are from the last validation run and offer the re-run. Take the wording from the spec if it defines one.
4. **F6 ("provisional" on S1/S3/S5 while S8 and the PDFs say "synthetic"): lane W, before Monday if cheap.**
   - On synthetic content, the early screens also say it is synthetic demo content.
   - Keep "provisional" where it is true; both facts hold.
5. **F8 (breadcrumb "›Details" missing a space): lane W, cheap. The npm fsevents warning goes to BACKLOG.**
6. **F4 (policy document prints "Posture: balanced" while S3 says posture cannot be read or set in this release): lane R, same basis as the other proofreading fixes.** State it truthfully, from the architecture's wording, e.g. that posture is not settable in this release and what default applies, or omit it. Name the wording in the READY.
7. **F3 (device group UUID): already lane R (d). S40 adds that `scope.device_groups` in the manifest carries no name.**
   - **Prefer a renderer-side lookup from the render input**, if the name reaches it.
   - **If the manifest itself must carry the name,** that is `packages/engine` (lane C12's path) and a manifest-shape change: name the hash impact in the READY. It becomes a gate target. Your routing call.
8. **F2 (Admin tenant list empty): expected.** The Q9 API is lane Q's, after 2b. No new action.

**Suggested for Monday (your call, disjoint paths permitting):** split lane W.
- **W1:** the verifier fixes F1, F5–F8; merge right after lane R.
- **W2:** 2b screens + the Q9 selector; merge after Q.

## Unchanged
- No push. A combined tier-1 gate is due before any push. **Its targets now also include:**
  - e2e on switch-ON and switch-OFF;
  - the fixture's live-stack guard;
  - approval-screen freshness;
  - the posture statement.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 14:31

Tuesday
