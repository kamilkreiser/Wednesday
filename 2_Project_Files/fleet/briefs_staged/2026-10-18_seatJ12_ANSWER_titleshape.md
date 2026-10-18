## BLUF

**Build (A) WITHOUT `strategy`: a title hit answers exactly `{ verified: false, checks: { documentExists: true } }`.** This SUPERSEDES Q2's first bullet in Wednesday's 08:25Z ANSWER ("plan confirmation - Seat J 12th"). That bullet's shape broke the declared 200 contract (`VerifyResponseSchema.verified` is required, originate.openapi.ts:457-461, your read). Wednesday ruled it without reading the schema. You were right to stop.

## WHY THIS SHAPE

- `verified: false` keeps the route's own discriminator and claims nothing about a document the caller did not identify. It is the same value the miss already sends.
- `documentExists` sits at `checks.documentExists`, the declared path, where the miss and every other strategy already put it.
- **`strategy` is dropped** because, by your own measurement, the miss does not carry it. Keeping it would add a second hit/miss difference beyond the existence bit. Hit and miss should then differ only in `checks.documentExists` and in the miss's `error` string. If that error string itself differs between absent, other-tenant, draft and revoked, that is a leak: the four misses stay byte-identical, as the gate measured.
- Pin the hit body with a positive cell (the exact key set: assert no other keys), and a cell proving the four misses are one body.

## ALSO RULED

- **F2: CONFIRMED, your literal, NULL-safe reading.** Exclude `draft` and `revoked`, and do not invent a "published" allow-list. In the READY, list every document status value in the schema and say which ones a title hit can return. If `suspended` or `expired` exist, name them under residual, and Wednesday cards Kam if any of them looks like it should be hidden too.
- Your other "Meanwhile" items stand as you wrote them.

The gate still tests this shape as a claim. Wednesday's ruling is not evidence.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-18 19:31
