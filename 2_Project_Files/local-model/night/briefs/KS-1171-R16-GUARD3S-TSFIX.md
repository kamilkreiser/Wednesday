# KS-1171 R16-GUARD3S-TSFIX - REBRIEF 1 of 1 (Kam's 2026-09-16 counter: round 2 of 2) - the R15 GUARD3S READY (checker PASS 8/8, run `runs/2026-09-21_ks1171-ornith35b-night2`) re-issued with its FOUR TypeScript errors fixed, at develop 64ab10513 (written 03:50 on 2026-09-22 by Wednesday's rebrief3 drafter from the R15 READY fence read whole, anchoring/src/anchorSubmission.ts:135-170 + :255-265, cardano/confirmation.ts:1-50 and the seat's tsc output)
File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts`
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the rebrief3 drafter at 03:51:47 AEST on 2026-09-22, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- THE DEFECT of round 1 (`READY_KS-1171-8J-GUARD3S-R15_..._PASS-8of8_2026-09-21.diff.md`, HELD 00:14 09-22): vitest green and checker PASS 8/8, but Seat B 16th's targeted type-check (a temp tsconfig extending anchoring's `tsconfig.json` - `strict`, `noUnusedLocals`, `noUnusedParameters` - with `files=[the test]`, `exclude []`, planted TS2322 control CAUGHT) reports FOUR errors in the file, verbatim from `5_Project_History/2026-09-22_seatB-16th/raise/typecheck-ks1171-ks1171-guard-3-s-re-poll-reads-head.out`:
  - `(49,9): error TS6133: 'SEED_USER_ID' is declared but its value is never read.`
  - `(84,29): error TS2353: Object literal may only specify known properties, and 'confirmed' does not exist in type 'Promise<ConfirmationResult>'.`
  - `(93,29): error TS2353: ...` (the same, the second RED cell's `makeHarness({ confirmed: true, ... })` call)
  - `(101,29): error TS2353: ...` (the same, the control's call)
- THE CAUSE of the three TS2353: round 1 typed the parameter `confirmResult: ReturnType<typeof waitForConfirmation>` - `waitForConfirmation` returns `Promise<ConfirmationResult>` (cardano/confirmation.ts:39-45), so the parameter was a PROMISE and an object literal cannot be one. The real type is the exported interface `ConfirmationResult` at cardano/confirmation.ts:11-27 (`confirmed: boolean; blockHash?; blockNumber?; slot?; confirmations?; error?; polled?; errored?`), which the three `{ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: N, errored: M }` literals satisfy; the harness's `confirm: vi.fn(async () => confirmResult)` then resolves to `ConfirmationResult`, which is assignable to the product's `Promise<ConfirmationLike>` (anchorSubmission.ts:164; `ConfirmationLike` :135-149 is the same shape minus `error`).
- THE FIX (only these lines differ from the round-1 fence; every cell, tamper and control is the SAME): (1) the import line `import { waitForConfirmation } from '../cardano/confirmation';` becomes `import type { ConfirmationResult } from '../cardano/confirmation';` (a type-only import: erased by esbuild under vitest, and the file already uses inline `type` imports on its anchorSubmission line); (2) `function makeHarness(confirmResult: ConfirmationResult) {`; (3) the unused `const SEED_USER_ID = 'seed-user-for-harness';` line is GONE (the row's `documentId` was already a literal). The round-1 fence had 108 '+' lines; this one has 107.
- QUOTE RULE (IMPROVEMENTS 2026-09-22 02:35, the KS-947 finding: the model escapes double quotes on a mixed-quote line): the round-1 fence carried a double-quote character on 2 '+' lines. Both are rewritten single-quote-only WITHOUT changing what runs: the `INPUTS_SPENT_SHORT` message drops the inner quotes around `All inputs are spent` (the product matches `/all inputs are spent/i` at anchorSubmission.ts:115 - no quotes in the pattern); the second RED cell's title is `RED KS-1171 8j - no never-reached-the-chain log when the transaction was found` (same cell, same assertions, a title with no quote character). `grep -c` for `"` over the '+' lines = 0, for a backslash = 0, non-ASCII = 0.
- VERIFIED by the drafter in the clone at 64ab10513: the fence written to its path and type-checked with the SAME instrument shape (`tsconfig.rebrief3-*.json` extending `./tsconfig.json`, `files=[src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts]`, `include []`, `exclude []`, `types ["node","vitest/globals"]`, `npx tsc -p`): 0 errors in the file (the round-1 fence under the same instrument: 4 - the positive control). Golden precheck (this fence as the model output through `tasks/test_only/checker.sh`): see the proposal.
- SIBLING: `KS-1171-R16-8j-TSFIX.md` re-issues the OTHER held KS-1171 file (`ks1171-8j-confirmed-wins-over-polled-zero.test.ts`) with the same tamper. Two files, two briefs, one ticket - exactly as round 1 (both READYs were held together as PR 8 of the 16th round).
- Tamper: `anchorSubmission.ts:260` at 64ab10513 is `      if (confirmation.confirmed) {` (6 leading spaces; whole-line exact match count 1 - the :401 twin has 10 leading spaces and is a different line; the checker plants by LINE after asserting the bytes). Same tamper as round 1.
- Ticket KS-1171: Backlog; the ticket's product question (the mixed-window design decision) stays with its owner. Nothing in the product changes.

## What is wrong (one paragraph)
Guard 3's re-poll in `services/anchoring/src/anchorSubmission.ts` reads a MIXED window (some attempts reached the chain, some threw) correctly at the tip because `reconfirmKnownSubmission` checks `confirmation.confirmed` FIRST (:260) and only THEN maps `polled === 0` to `'unknown'`. Nothing in the suite pins that ordering. The code is RIGHT at the tip. This task is the PIN (test-only): one new vitest file whose two RED cells red when :260 is tampered to `confirmed && polled !== 0` and whose control (polled: 2) stays green. Round 1 wrote exactly these cells and PASSed; it is re-issued ONLY because its file does not type-check under anchoring's tsconfig (a Promise-typed harness parameter and one unused constant). Reproduce the fence below byte for byte.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts` then ONE `@@ -0,0 +1,107 @@` hunk, every line `+`, no context, no `-`. No product hunk. Copy the 107 lines below byte for byte, in order. Every string in this file is single-quoted; there is NO double-quote character and NO backslash anywhere in the file - never add, escape or change a quote.

## The exact change
```
+/**
+ * KS-1171 - Guard 3's re-poll reads a MIXED window as ABSENT (#805 tier-1 r3 residue).
+ *
+ * TEST-ONLY MODE. The product at the tip is CORRECT: `reconfirmKnownSubmission`
+ * checks `confirmation.confirmed` FIRST and only THEN maps `polled === 0` to
+ * `'unknown'`. This task pins that behaviour with one new test file whose cells
+ * RED when line 260 is tampered to gate the confirmed check on `polled !== 0`,
+ * then go GREEN again once the tamper is removed (the untouched tip).
+ */
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import { BlockfrostServerError } from '@blockfrost/blockfrost-js';
+import { createAnchorSubmitter, type AnchorSubmissionDeps, type AnchorSnapshot } from '../anchorSubmission';
+
+vi.mock('../cardano/provider', async (importOriginal) => {
+  const orig = await importOriginal<typeof import('../cardano/provider')>();
+  return { ...orig, getTransaction: vi.fn() };
+});
+import type { ConfirmationResult } from '../cardano/confirmation';
+
+const TX_A = '408e72087942198b69d686401829b5b9419d018dc4cc64917283aa3cdb084994';
+const ANCHOR_ID = 'anchor_a93bd8dd-10c8-4d52-b12e-c0bff6f5c790';
+
+/** The node reply guard 3 matches so it enters the re-poll path instead of retrying. */
+const INPUTS_SPENT_SHORT = () =>
+  new BlockfrostServerError({
+    status_code: 400,
+    error: 'Bad Request',
+    message: 'Transaction submission failed: ConwayMempoolFailure All inputs are spent',
+    url: 'x',
+  });
+
+function makeLock() {
+  let chain: Promise<unknown> = Promise.resolve();
+  return function lock<T>(fn: () => Promise<T>): Promise<T> {
+    const next = chain.catch(() => undefined).then(() => fn());
+    chain = next.catch(() => undefined);
+    return next;
+  };
+}
+
+/**
+ * Harness for KS-1171 - same shape as ks726's but the confirm dep ignores the
+ * chain and always returns FOUND with polled: 0 / errored: 3. Under the tamper
+ * at line 260 (`confirmed && polled !== 0`) this injected double would read as
+ * NOT confirmed -> unknown -> retry scheduled; at the untouched tip it confirms
+ * the row because `confirmed` is checked first regardless of counters.
+ */
+function makeHarness(confirmResult: ConfirmationResult) {
+  const row: AnchorSnapshot = {
+    id: ANCHOR_ID, status: 'pending', transactionHash: undefined, retryCount: 0,
+    metadataLabel: 674, metadataPayload: { documentId: 'doc-1787874883988-04d3ee24' },
+  };
+  const statusWrites: Array<Record<string, unknown>> = [];
+  const signedHashes: string[] = [];
+  const logs: Array<{ level: string; message: string; meta?: Record<string, unknown> }> = [];
+  const submit = vi.fn(async (_label: number, _payload: object, options?: { onSigned?: (txHash: string) => Promise<void> }) => {
+    if (options?.onSigned) { signedHashes.push(TX_A); await options.onSigned(TX_A); }
+    throw INPUTS_SPENT_SHORT();
+  });
+  const deps: AnchorSubmissionDeps = {
+    getAnchor: vi.fn(async () => ({ ...row })),
+    submit,
+    // Stub that ignores the chain entirely - always reports found with the given counters.
+    confirm: vi.fn(async () => confirmResult),
+    updateStatus: vi.fn(async (_id: string, updates: Record<string, unknown>) => {
+      statusWrites.push(updates);
+      if (typeof updates.status === 'string') row.status = updates.status as AnchorSnapshot['status'];
+      if (typeof updates.transactionHash === 'string') row.transactionHash = updates.transactionHash;
+    }),
+    bumpRetryCount: vi.fn(async () => { row.retryCount += 1; }),
+    scheduleRetry: vi.fn(),
+    log: vi.fn((level, message, meta) => { logs.push({ level, message, meta }); }),
+    withWalletLock: makeLock(),
+  };
+  const calls = (fn: unknown) => (fn as ReturnType<typeof vi.fn>).mock.calls.length;
+  return { deps, row, signedHashes, logs, calls };
+}
+
+beforeEach(() => { vi.clearAllMocks(); });
+
+describe('KS-1171 - confirmed:true with polled:0 confirms the row at the tip (test-only mode)', () => {
+  it('RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row', async () => {
+    const h = makeHarness({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 0, errored: 3 });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.row.status).toBe('confirmed');
+    expect(h.row.transactionHash).toBe(TX_A);
+    expect(h.calls(h.deps.scheduleRetry)).toBe(0);
+  }, 60_000);
+
+  it('RED KS-1171 8j - no never-reached-the-chain log when the transaction was found', async () => {
+    const h = makeHarness({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 0, errored: 3 });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.logs.some(l => l.message.startsWith('Anchor confirmation poll never reached the chain'))).toBe(false);
+    expect(h.logs.some(l => l.message === 'Anchor confirmed on Cardano')).toBe(true);
+  }, 60_000);
+
+  it('KS-1171 control - confirmed:true with polled 2 confirms the row too', async () => {
+    const h = makeHarness({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 2, errored: 0 });
+    await createAnchorSubmitter(h.deps)(ANCHOR_ID);
+
+    expect(h.row.status).toBe('confirmed');
+    expect(h.row.transactionHash).toBe(TX_A);
+    expect(h.logs.some(l => l.message === 'Anchor confirmed on Cardano')).toBe(true);
+  }, 60_000);
+});
```

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles - literal rendered strings)
- `RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row`
- `RED KS-1171 8j - no never-reached-the-chain log when the transaction was found`
- `KS-1171 control - confirmed:true with polled 2 confirms the row too`  (CONTROL - green on both trees)

## Tampers
### 8J
File: `Blockchain/Dev/services/anchoring/src/anchorSubmission.ts`
Line: 260
From:
```
      if (confirmation.confirmed) {
```
To:
```
      if (confirmation.confirmed && confirmation.polled !== 0) {
```
Reds: `RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row`, `RED KS-1171 8j - no never-reached-the-chain log when the transaction was found`
(From located at 64ab10513 by exact whole-line match: 1 match, at :260. Reachability: both RED cells inject `confirmed: true, polled: 0`; under the tamper :260 is false, the row is not confirmed, `scheduleRetry` is called and the `Anchor confirmation poll never reached the chain` log fires - both cells red by assertion. The control injects `polled: 2`, so the tampered :260 is still true - green.)

## Controls
- `KS-1171 control - confirmed:true with polled 2 confirms the row too`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts`); the header `@@ -0,0 +1,107 @@` (107 '+' lines - count them; the R15 batch over-declared new-file headers by 2-20 lines); single quotes only, no `"`, no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
