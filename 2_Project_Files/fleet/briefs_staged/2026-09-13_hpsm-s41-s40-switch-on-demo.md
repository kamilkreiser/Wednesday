# SWITCH ON — Kam RULED demo-content on his own card (11:19:24 AEST). Merge, then switch on for the local review stack and the Azure demo, every fence kept

**BLUF.** **For session 41 (seat hpsm-982d) and session 40 (PID 67724).** Kam tapped his card on Tuesday's panel tab at 2026-09-13T11:19:24 AEST, verbatim: *"Decision hpsm-composer-synthetic-demo-content-for-monday: demo-content — Yes — fenced synthetic demo content, releasable for synthetic tenants only"*. **This is his first-party ruling.** It SUPERSEDES the "switch stays OFF" line in Tuesday's 01:01:43Z, 01:03:54Z, 01:16:26Z and 01:18Z ANSWERs.

## What it permits, and the order
1. **S41 merges, as merge seat, in its normal order:** the default-OFF switch code (lanes G and F), then S40's `s40/demo-content` (`0fba0a4` or later), each with its own checks re-run by S41. A clean-clone `ci.sh` follows.
2. **Then switch ON is permitted on exactly two stacks:**
   - **(a) the local review stack `pc-lane-a`** (127.0.0.1:18580), done by whichever seat runs it;
   - **(b) Kam's live Azure demo** (`hpsm-dev-rg`), by S40 through its documented update path, using the merged head. **Access control stays on**, and it stays synthetic tenants only.
3. **Every fence stays, and a test proves each one:**
   - SYNTHETIC source_refs;
   - release only for a tenant flagged synthetic;
   - a SYNTHETIC watermark on every output;
   - never inside the real content release;
   - never releasable for a real tenant;
   - real content unchanged.
4. **Report when ON** (from S40 for Azure, from S41 for local): the head deployed, the stack, and one output rendered and opened, as the proof. Kam's aim is to proofread an output.

## Unchanged
- **No push to HPSM-light.** This is demo content on demo stacks, not a release of the product. **A combined tier-1 gate on everything since `1a6b68d` is due**, and it includes this switch and its fences as named attack targets. Tuesday's fresh seat commissions it.
- Q6: display name and role on documents, no email. Q9: the conditions as ruled.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-13 11:20

Tuesday
