Seat S 6th. KAM RULED: BUILD THE GUARD.

Kam's ruling, verbatim (live board, 2026-10-29 19:51:25 AEDT): "Decision secuura-ks1175-private-jwk-guard-1029: a — Add a narrow guard before deploying (recommended)"
The card's option a, as he tapped it: "Seat S builds a small separate PR: decode the did:jwk value only to refuse private-key members (d, p, q, dp, dq, qi, k), with a 400 and a clear message. Nothing else about the JWK is checked. Gated, merged, then deployed with did:jwk in the next round."

## BLUF
Build it from the spec in your HANDOVER, on a NEW branch and worktree off develop fd84001c738a1bf9071d2d8a5cac6e953ad95789 (re-pin first; it carries #1805, #1806 and #1804). ONE PR, tier 1. Then READY FOR GATE with the head sha. Wednesday commissions the gate, and merges on its GO.

## Scope, read narrowly (this is the ruling, not Wednesday's design)
- Decode the base64url JWK segment of a did:jwk in actorDid/orgDid ONLY far enough to see its member names.
- Refuse (400, the same validation path the schema already uses) if ANY of d, p, q, dp, dq, qi, k is present.
- If the segment does not decode to a JSON object, REFUSE too: an undecodable did:jwk is not a public key. Say this explicitly in the PR as the one design choice the ruling implies.
- Nothing else about the JWK is checked: no kty/crv validation, no key use.
- Cells: each of the 7 private members refused (red-proven against develop); a real public P-256 and Ed25519 did:jwk still accepted (controls); a non-JSON segment refused; did:key and did:web unchanged.
- Your 1805-1/1805-2 test pins are NOT in scope (they are being filed); do not widen.
- Docs: Projects Documents entry at develop's highest + 1 at push time (107 is #1806's, so 108 if nothing else lands).

## Hold
No deploy from this seat. KS-1454 (a held Spark diff) also edits anchorSchema.ts and is raised AFTER your guard merges, so you own that file until then. If your context nears its band before READY, put the exact state in your HANDOVER and wrap: a successor continues from it.

Wednesday
