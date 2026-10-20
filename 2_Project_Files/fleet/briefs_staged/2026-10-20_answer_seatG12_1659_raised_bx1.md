## BLUF
#1659 is NOT GO yet: it is RAISED to TIER 1, gate BX1 (Opus). This supersedes the tier-2 framing of Wednesday's 00:56Z ANSWER. Two reasons: gate BV1 found a reader that admits on a NULL-derived empty owner, and BV1's verdict file does not reproduce its own sha256, so Wednesday does not rely on it. Carry on with KS-1558; do not merge #1659.

## The finding, from BV1's file (a lead, not yet evidence)
`documentRepo.ts:176` maps the owner to `owner_user_id || issuer_user_id || ''`, and `documents.ts:1124` cloaks only when that owner id is truthy. A connector certification with no holder used to FAIL its write (the non-UUID value); with the fold it now WRITES a row with an empty owner, possibly readable by any same-tenant user who has its id. BV1 derived this from code and did not drive it. BX1 drives it on real Postgres as a same-tenant user, an other-tenant user and the issuer, and compares with the existing bare-connector class.

## Your census was right about the DIRECT readers
BV1 agrees: the anchor guard denies on NULL, and verification.ts:334 is gated. The gap is one hop out, in the document read path that maps the owner. If BX1 confirms new reach, a remedy round follows (round 2 of 2) with the options BX1 names; if it does not, the GO follows.

## Provenance
BV1 verdict `0_Brain/reference/2026-10-20_gate-BV1-pr1659-ks1659/verdict.md` (trailer d88011fd3bfa; Wednesday's `sed '1d;$d' | shasum -a 256` = be82d1f856a9). BX1 brief `0_Brain/reference/2026-10-20_gate-BX1-pr1659-ks1659-tier1/GATE_BRIEF.md`. Heads: refs/pull/1659/head 97eaffe0d300, develop 610570e5a757 (ls-remote 12:0x AEDT).
