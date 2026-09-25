#1228 KS-1171 LASTANS: a transaction is ABSENT only when BOTH of Kam's conditions hold
head 43279280f76ed9982782ad7652288d2c3d522b71

## Ruled by Kam

> **Decision `secuura-ks1171-when-is-an-anchor-absent`: c — Both conditions (strictest, fewest double submissions)**

— Kam, live board, **2026-09-25 12:49:07 AEST**. Delivered to the ticket as comment `a5f75423` before this was built.

`reconfirmKnownSubmission` may return `'absent'` — which lets guard 3 schedule the ordinary retry, **minting a second fee-paying transaction** — only when **both** hold:

1. at least `ABSENT_MIN_ANSWERED_POLLS` (2) attempts **answered**, and
2. the last answer arrived at least `ABSENT_MIN_LAST_ANSWER_MS` (60 s) after polling began.

Anything less rests the row in `submitting` as `'unknown'` for the reconciler (KS-584). KS-726 closed the case where **no** attempt reached the chain; this closes its neighbour, where **one early** "not found" was read as definitive. Blockfrost answers 404 until a transaction is in a block *and* indexed, so an early answer is a likely false negative in exactly the case that matters — a same-hash duplicate submit, where TX_A entered the mempool seconds before the node's 400.

**The timing measure is conservative by construction.** `lastAnsweredElapsedMs` counts from the **start of polling**, which is at or after the 400 — so `>= 60 s since poll start` implies `>= 60 s since the 400`, never less. It can only ever retry *less* than the ruling allows, which is the side Kam chose. The accepted cost, named in the ticket: a genuinely absent transaction whose late attempts threw now rests ~24 h for the reconciler instead of retrying in ~15 s.

The thresholds are **exported constants** so a cell *names* the rule instead of repeating a magic number — and a control asserts they **are** the ruled values, so lowering them to make a test pass reds that cell. A configurable threshold was rejected: it would turn Kam's rule into a test parameter.

## A defect of mine that the coordinator's census caught

The first census run measured **seven** flipped cells. Three were not the ruling at all: the gate had collapsed two different operational facts into one log message, and three shipped KS-726 E8 cells assert the old text **while asserting behaviour this change does not touch**. They failed on the *string* with correct behaviour underneath — the worst kind of red, because it reads as a ruling consequence.

Fixed: the `polled === 0` case **keeps KS-726's message** ("never reached the chain" is still exactly what happened, and an operator needs to tell it from "the chain answered, but not definitively enough"). The new case gets its own wording. The three E8 cells recovered and the flip set dropped **7 → 4**.

## Four cells rewritten, never deleted — the measured set

| file:line | what changed |
|---|---|
| `ks726-gate-f1-unreachable-chain.test.ts:156` **CONTROL** | "not found ×3" on a 1 ms harness is no longer definitive; it **rests**. Its stale title *"(the (c) path, unchanged)"* is **corrected** — that label is exactly what would stop the next reader noticing the ruling changed this cell. |
| `ks726-gate-f1-unreachable-chain.test.ts:169` | the deliberate pin of the commissioned "any attempt" semantics, rewritten to the new rule. |
| `ks726-gate-f1-unreachable-chain.test.ts:178` **CONTROL** | keeps its CONTROL label with a **new meaning**: a counter-less result carries no evidence and is the one shape that does **not** earn a retry. |
| `ks726-write-ahead-tx-hash.test.ts:406` | purpose unchanged (a definitive rejection keeps the retry); the double now carries the evidence the ruling requires, and a sibling cell pins that the counter-less shape rests. |

**No `polled === undefined` carve-out in the product** — a branch whose only consumer is a test double later reads as intended behaviour, and production always goes through `waitForConfirmation`, which always reports both counters.

Also corrected: `ConfirmationLike`'s comment claimed *"a `confirm` that reports neither keeps the pre-fix reading (`'absent'`)"*. The ruling **reverses** that, so the comment is rewritten rather than left standing.

**Nine cells added**, including the coordinator's end-to-end cell driving the **real** `waitForConfirmation` (3 attempts, 1 ms): the chain answers ×3, the count condition is met, the elapsed condition is not, and the row rests. A double can be given any numbers; that cell can only pass if the product reads a genuine poll result the way Kam ruled.

## Test Evidence

**Touched:** `services/anchoring/src/cardano/confirmation.ts` (+27); `services/anchoring/src/anchorSubmission.ts` (+86/−?); `src/__tests__/ks726-gate-f1-unreachable-chain.test.ts`; `src/__tests__/ks726-write-ahead-tx-hash.test.ts`; `src/__tests__/ks1171b-absent-needs-both-conditions.test.ts` (NEW, 7 cells).

**Ran (locally, by the author, BARE and SERIAL — `npx vitest run --no-file-parallelism`):**
- `services/anchoring`: **bare 334 passed / 1 failed over 24 files → patched 343 passed / 1 failed over 25 files** (+9 cells).
- ⚠ **anchoring `343 passed / 1 failed`; the one failure is `threadTokenMint.test.ts > … deterministic per-seed policyId`, pre-existing at develop `6ab9d5021` (the same cell fails bare), not caused by this change** — **KS-562**, re-measured there today. An exception, not a timeout, so not the under-load false-red class.
- `npx tsc --noEmit`: **rc 0**.
- **Red proof** with the product read back from the object store and every test edit kept: **10 failed / 334 passed at develop** — nine of mine plus the pre-existing one — and **343 passed** with the product applied.
- Honest note: **RED (c), the positive arm, passes at develop too** (the old rule also retried there). It is labelled the positive control it is, not counted as a red.

**NOT run:** preflight legs **3, 4 and 8** — `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.`, three identical `SKIP — local stack not up on http://localhost:6882` lines. **Legs 3/4/8 are OWED at the gate** (anchoring surface). The four platform suites (Schemathesis · Akto · Playwright · k6) were **not run** — the local stack is not up this round by fleet rule.

**Migrations + config:** none. No migration, no env var, no dependency change, `docs/openapi/` untouched.

Refs KS-1171

🤖 Generated with [Claude Code](https://claude.com/claude-code)

