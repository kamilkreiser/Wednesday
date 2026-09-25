#1237 KS-1229: pin that the /version relabel guard keys on presence, not truthiness
head cfa16eb70ba28c5833101e39e4e1cb1680b8dd6c

## BLUF

Test-only, one file: services/originate/src/__tests__/ks1213-a-derived-writer-relabel-is-refused.test.ts.

This is the one row of the gate's nine with no cell. Eight already have one (#1155 `ff532c0fe` five,
#1194 `da083427a` three); Q-VERSION-TRUTHY read zero.

The guard is `metadata.documentType !== undefined && metadata.documentType !== source.type`. Written as
`metadata.documentType && ...` instead, null / '' / false slip past it. Nothing is RELABELLED by that -
the served type is `data.documentType || type`, so the stored type still wins - which is exactly why the
whole suite stayed green under the gate's tamper. What is lost is the rule the route states: a
documentType that is PRESENT and not equal to the stored type is refused, whatever its truthiness.

The ticket offers either a presence-refusal cell OR a comment accepting the benign shape. Which is right
depends on what the route actually does, and that was not in the ticket - a validator could plausibly
refuse `null` with VALIDATION_ERROR before the guard ever sees it, in which case a cell asserting
BAD_REQUEST would pin the wrong component and the tamper would not red it. Measured first, on a clean
worktree at this base, with the probe reverted afterwards (porcelain back to 0):
    metadata.documentType = null   -> 400 BAD_REQUEST, 0 saved
    metadata.documentType = ''     -> 400 BAD_REQUEST, 0 saved
    metadata.documentType = false  -> 400 BAD_REQUEST, 0 saved
    absent (metadata: {})          -> 201, stored and served DOCUMENT
So it IS the guard refusing them, and the presence-semantics cell is the correct option: three RED cells
plus an absent-key control.

Test evidence
- Touched: one test file. No product byte.
- Ran: originate jest --runInBand 74 suites / 867 tests, rc 0. Bare serial baseline at this base is
  74 / 863, so bare 863 / patched 867 - the three cells plus the control, nothing else moved.
  tsc --noEmit rc 0. packages/shared vitest 46 files / 918 tests rc 0.
- RED-PROOF, ran and built. The guard shape appears at THREE sites (/version :2001, /sign-cert :2617,
  /sign-wallet :2886) - the first tamper attempt asserted a unique anchor, found 3, and REFUSED to plant,
  which is how that was caught. Tampering ONLY the /version site (presence -> truthiness):
      at head      114 passed / 114
      tampered       3 failed / 111 passed / 114
  and the three are EXACTLY QVT1, QVT2 and QVT3. The control cell and the sign-cert / sign-wallet cells
  stay green, so the new cells are specific to their route rather than to the shape. Product file restored
  and proved byte-identical by sha256; porcelain back to the one test file.
- NOT run: legs 3, 4, 8 (local stack not up); this PR has no product surface for them to exercise - the
  only changed file is under src/__tests__/. Not a claim that the gate is green. Integration config not
  run (needs a live Postgres). No image rebuilt.
- Migrations + config: none.


Refs KS-1229

🤖 Generated with [Claude Code](https://claude.com/claude-code)

