KS-794 verify-file returns `fileSize` on every 200 and neither response schema declares it
state In Progress

## What

Both verify-file handlers return `fileSize` (bytes of the uploaded body) on **every 200** — `verification.ts` in all three of its 200 shapes, and `verificationV2.ts`. Neither `VerifyResponse` nor `V2VerifyResponse` declares it.

Both bases are `.passthrough()`, so the responses **validate**. The contract is simply narrower than the behaviour: a consumer reading the spec cannot know `fileSize` is there.

## Why it was not fixed inside KS-791

I first fixed it the obvious way — `VerifyResponseSchema.extend({ fileSize })` as two new registered schemas. `check:openapi` **refused it, correctly.** `.extend()` carries the base's `example` across, so the large `matches` example was duplicated under new schema names, and the E8 identifier-literal guard fired on the copies.

The base examples ARE allowlisted — but read the stated reason:

> *"KS-584 P3 leg 2 (d47f63202) authored this example on develop; the block is byte-identical to origin/develop and is not this branch's work. Its four identifier literals … are synthetic but predate FX."*

**That reason is false for a copy I just created.** Adding an allowlist entry for `V2VerifyFileResponse` would have meant writing an exemption whose justification did not hold — which is precisely the failure the guard exists to catch. So KS-791 reverted to the ratified design (reuse the base schemas) and documents `fileSize` in the two response **descriptions** instead, naming this ticket.

## The options, for whoever picks this up

1. **Add** `fileSize: z.number().int().optional()` **to the two BASE schemas.** No new schema, no new example, no allowlist entry. Cost: `/verify` and `/v2/verify` would declare an optional field they never return — a mild over-description traded for the current mild under-description.
2. **Extend, and author a fresh FX-drawn example** for each new schema rather than inheriting one. Correct and fully honest; costs a hand-written `matches` example per schema.
3. **Leave it.** The descriptions carry the fact and the responses validate. Defensible, but the fact then lives only in prose.

My preference is (1) — it is the smallest change that puts the field in a schema, and "optional and absent" is an honest description of `/verify`.

## Done means

`fileSize` is discoverable from the schema (not only the description) for both verify-file operations, `check:openapi` is green, and no allowlist entry was added carrying a reason that is not true of the thing it exempts.
