## BLUF
#1788 (KS-1240 part 2) passed its tier-1 delta gate (gate 7, round 2 of 2): GO WITH NOTES, Seat X 3rd. The three ruled items are CLOSED: no token-endpoint body reaches the client in any of the six adapters; the round-1 profile-check mutants are all killed; /social/link answers 503. The delta matched your description exactly. Your merge slot stays docs section **95**. Wednesday mails your turn after #1782's merge is verified. Do not prep yet.

## Before your merge turn: search the board, then file what is missing (one ticket per logical path, on our board account, BLUF-first, search quoted)
1. **1788-10 (Low), its own ticket:** a provider answering 200 with a NON-JSON body still puts its first 10 characters into the callback's 400. The parse error quotes them, and routes/auth.ts:1078 echoes any exchange error's message. Same class as the leak you just closed.
2. **Round-1 residue, if not already filed:** 1788-3 (GitHub's three calls can reach 30 s, equal to production nginx's timeout), 1788-6 (the internal.ts call has no timeout), 1788-7 (Apple id_token not verified). File each one that has no ticket yet. Do not file one that already does: comment your evidence on it instead.
3. Mail the ids (or "already filed as KS-…") in your next STATUS.

## Gate notes (no fix round)
- Four of the gate's 20 own mutants survive: H9/H12 (what counts as "unreachable" is pinned for Apple only), H5 (the 200-character log cut is unpinned), G3 (the dead AbortError branch). Accepted as notes under the cap.
- Your figures were reproduced: 22F/41P to 63/0; auth 1244 to 1258 with no new failures (ks949 is timing, 31/31 alone).

## Provenance
- Verdict: 0_Brain/reference/2026-10-28_gate7-tier1/verdict.md (claude-opus-5-5; Spark shadow first). Pins at start and end: develop b67a1c8d3a52, #1788 7eeedb825c5c.
- The gate did not read the PR body (no gh identity); your commit message stood in.
