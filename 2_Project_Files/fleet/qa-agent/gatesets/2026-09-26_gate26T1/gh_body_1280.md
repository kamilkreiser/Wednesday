#1280 KS-1129: coerce chain.blockNumber so the heal persists a number
head 12c197a9215e3156d48cf47fbcec09292619cb68

## What

`block_number` is a `BIGINT`, and `pg` returns int8 as a **string** by default with no int8 parser anywhere in `Blockchain/Dev`. #1220 fixed anchoring's verify body to report a number; the heal path in originate must not depend on that, because whatever the heal composes is handed to `persistHealedAnchor`, which **writes** it to the document blob — and the gateway's tier-1 read refuses a string (`typeof persistedBlockHeight === 'number'`), so a healed document answers off-chain-only for a document that **is** on chain.

## 🔴 Two persisting sites, not one — and a cell found the second

The ticket, its gate report, and my own first measurement all name only `verification.ts:338`. There is a **second**: v2 heals through its own `healBlobWithChainFact` (`verificationV2.ts:143`), a near-duplicate of `confirmStalePendingAnchor`'s tail carrying the identical `chain.blockNumber ?? blob.blockHeight ?? 0`, whose result goes to `persistHealedAnchor` at `:191` — **a persisted write on the v2 verify path.**

It was not found by reading. It was found by a cell: the cell drove v2, asserted the write was reached, and **read back `"4242"` as a string after the v1 site had already been coerced.** Both sites are coerced here.

The complete sweep of originate's heal compositions, with each traced to its write:

| site | function | reaches a persisted write? | this PR |
|---|---|---|---|
| `verification.ts:368` | `confirmStalePendingAnchor` | **yes** — `persistHealedAnchor` at `:688`, `:1118` | **coerced** |
| `verificationV2.ts:143` | `healBlobWithChainFact` | **yes** — `persistHealedAnchor` at `:191` | **coerced** |
| `verification.ts:607` | chain-first branch | no — `res.json` only | untouched |
| `verification.ts:1058` | chain-first branch | no — `res.json` only | untouched |
| `verificationV2.ts:235` | chain-first branch | no — `res.json` only | untouched |

The three response-only sites each parse their **own** anchoring reply, so there is no single `chain` parse point to coerce at — which is why the coercion is at the sites rather than "once where `chain` is parsed". Typing the published `blockchain` block is ruled out (`secuura-ks1019-blockchain-block-untyped` = a), so those three stay as they are.

**Also measured and NOT in this PR:** `services/anchorStateSync.ts:231`, `:266`, `:346`, `:380` write `blockHeight: anchor.blockNumber || 0` and all four persist. They read `GET /api/anchors/:id`, which is a different endpoint from the one #1220 fixed, so whether they carry the same defect is **unmeasured**. Raised for a ruling rather than folded in silently — those four are KS-1074's writers and a different claim from this ticket's.

## `toBlockHeight`

Mirrors anchoring's `toBlockNumber` (#1220) deliberately, including its two refusals: an **empty** string becomes `null`, never `Number('') === 0` — a zero height is a claim, absence is not; and an unconvertible value becomes `null`, never `NaN`. A real `0` is preserved, and both call sites keep `??` rather than `||`, so a zero height still means zero.

**Behaviour change, stated:** before, `chain.blockNumber = ''` or `'abc'` was persisted verbatim (neither is null, so `??` kept it). Now each falls through to the stored height. That is the intended fix, not a side effect.

## Why the cell file matters more than usual here

**No test file in this suite names `persistHealedAnchor`**, and the closest sibling (`ks584-p3-verify-list.test.ts`) **cannot reach the write**: its row fixture carries no `tenant_id`, so `persistHealedAnchor` returns at `if (!docId || !tenant) return;` before calling `updateDocument`. That is why its incomplete `documentRepo` mock never blows up — and a cell copied from it would assert a property of **a write that never happened**, and pass for that reason.

So every cell asserts the write was **reached** before asserting anything about its content, and one cell is the control for exactly that: with `tenant_id` removed, `updateDocument` is called **0** times while the response still presents `confirmed`. That is what makes "called exactly once" load-bearing rather than decorative.

## Test Evidence

**Touched:** `services/originate/src/routes/verification.ts`, `services/originate/src/routes/verificationV2.ts`, and a new `services/originate/src/__tests__/ks1129-heal-persists-a-number.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`. (develop has since moved to `df5e9f5da6d2`; this worktree does not contain that.)

| arm | result |
|---|---|
| originate BARE — both sources restored **and the new cell file moved aside** | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **883 passed / 883, 75 suites**, rc 0 (+5 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

Both source restores asserted by sha256 after the bare arm.

**Five red arms, one per conjunct, each reddening exactly the named cells:**

| arm | conjunct falsified | cells that red |
|---|---|---|
| R1 | v1's coercion reverted, `verification.ts` only | V1PERSISTSANUMBER |
| R2 | v2's coercion reverted, `verificationV2.ts` only | PERSISTSANUMBER + FALLTHROUGH |
| R3 | `toBlockHeight` becomes the identity | both PERSISTS cells + COERCION + FALLTHROUGH |
| R4 | the empty string becomes `0` instead of `null` | COERCION + FALLTHROUGH |
| R5 | `persistHealedAnchor` stops requiring a tenant | CONTROL-REACHED |

R1 and R2 are separate arms **because the two compositions are separate functions** — a cell on one proves nothing about the other, and my first version of this suite drove v2 only, so reverting v1 would have reddened nothing.

⚠ **R2 and R3 proved nothing in their first form**, and the runner caught it rather than scoring it. Reverting v2's site left `toBlockHeight` **imported and unused**, which `tsc` refuses; and R3's early `return` left the rest of the function **unreachable**. Both are compile-breaking tampers: the suite never runs, reds nothing, and looks exactly like an inert tamper if only the failed set is read. The runner's `LOADFAIL` verdict (0 passed **and** 0 failed) is what distinguished them. R2 now also removes the import; R3 replaces the whole body.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- The four `anchorStateSync.ts` writers are **not** covered — see above; they are raised, not fixed.
- The gateway's own tier-1 read is not exercised here; this PR fixes what originate persists, and the gateway is a held surface.
- The JSONB round-trip item on this ticket stays open.

Refs KS-1129

🤖 Generated with [Claude Code](https://claude.com/claude-code)

