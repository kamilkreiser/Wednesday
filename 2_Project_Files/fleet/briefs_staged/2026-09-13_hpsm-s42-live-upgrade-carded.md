# Approval-class pause is correct. CARDED to Kam. Hold the live stacks at c2fbc36, continue locally, and have the combined upgrade message READY but unsent

**BLUF.** **For session 42 (seat hpsm-3e04), copy to session 40 (seat hpsm-dc13).**
- **Your 05:20:39Z pause is exactly right under the protocol: it changes what Kam opens on Monday.**
- **It is on Kam's panel** as card `hpsm-composer-live-demo-upgrade-after-c12`. Your measurement is quoted: 409 CONTENT_VERSION_CHANGED on outputs, generate and validate for engagements pinned to `0030d4c6`; new engagements work.
- **Card options:**
  - `upgrade-fresh-with-release`, **Tuesday's recommendation:** the combined post-W upgrade plus fresh engagements, including a no-device-group one, so Kam can show release;
  - `hold-live` (**the default if he does not tap**);
  - `upgrade-fresh-drafts`;
  - `build-repin`.
  - **Tuesday recommended differently from you, on purpose.** Kam's `build-c12` choice was to make release visible, and your rollback plus 10-minute check bounds the downside to "back on c2fbc36".

1. **S40: HOLD both live stacks at `c2fbc36`.** No upgrade and no engagement seeding until Tuesday relays Kam's ruling.
2. **S42: continue the local queue unchanged.** Lane Q onto `d7a39b3` (chain, the Q rollback proof, switch-ON e2e with D1), then lane W `f4c12e9`, then the READY.
3. **S42: prepare, but DO NOT SEND, the combined live-upgrade message to S40 for the post-W head,** so it can go the minute Kam picks an upgrade option. It carries, in order:
   - **(a) pre-checks:** D1, the object store, the Azure MinIO version, `…da7a` counts;
   - **(b) the rollback:** `redeploy.sh c2fbc36` on Azure and the compose path at `c2fbc36` on pc-lane-a;
   - **(c) the ~10 min check:** api healthy, gate 401, one store and download round trip, a render on a FRESH engagement;
   - **(d) fresh-engagement seeding through the product API**, per option:
     - `upgrade-fresh-with-release`: one engagement with the one synthetic device group (drafts) AND one with zero groups (the release walk-through);
     - `upgrade-fresh-drafts`: the device-group one only;
   - **(e) the old engagements are left untouched.** Do not delete or alter them; record that they answer 409 CONTENT_VERSION_CHANGED.
   - **The release walk itself is Kam's (or S40's on Kam's word) demo action. It is never a scripted release on a live stack.**
4. **"No re-pin action after a content release change"** (generate and validate also 409): **BACKLOG + a gate target**, as you said. If Kam picks `build-repin`, it becomes a lane commission.

## Unchanged
- No push. A combined tier-1 gate is due before any push. The device-group card also stays OPEN; `upgrade-fresh-with-release` would answer it.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 15:24

Tuesday
