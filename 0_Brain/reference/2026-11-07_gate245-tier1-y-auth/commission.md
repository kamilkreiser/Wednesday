# Gate 245, tier 1, round 1 of 2: Y 6th's auth PRs, 2066, 2073, 2075

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Clone: /private/tmp/g245. Tier reason: credential minting, key rotation, session end.

- PR 2066, KS-2032, head baf577c78e7f [H/2026-11-06_seatY-6th/pr/ks2032/ready.txt]. Card secuura-ks2032-non-live-admin-token-mints-tenant-keys-1106 = a. It cites a KS 1585 cheat resolution from a develop merge: check it.
- PR 2073, KS-1152 record R-880-1 only, head 9709acff5c5f [H/2026-11-06_seatY-6th/pr/ks1152/ready.txt]. Card secuura-ks-1152-rotate-says-rotated-when-old-key-lives-1106 = b. It adds two optional fields to a published contract.
- PR 2075, KS-2083, head d2245bf37fe0 [H/2026-11-06_seatY-6th/pr/sessend/ready.txt]. Card secuura-ks2063-add-session-end-on-role-change-1106 = a, 'Both'. The READY says two auth cells did not pass in the full run: find out exactly why, at this head and at develop. A failing auth cell the seat cannot explain is not a note.
