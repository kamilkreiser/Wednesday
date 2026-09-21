# KS-1171 R16-8j-TSFIX - REBRIEF 1 of 1 (Kam's 2026-09-16 counter: round 2 of 2) - the R15-8j READY (checker PASS 8/8, run `runs/2026-09-21_ks1171-ornith35b-night`) re-issued with its THREE TypeScript errors fixed, at develop 64ab10513 (written 03:50 on 2026-09-22 by Wednesday's rebrief3 drafter from the R15 READY fence read whole, anchoring/src/anchorSubmission.ts:135-170 + :255-265, cardano/confirmation.ts:1-50 and the seat's tsc output)
File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts`
Tip: `64ab105132eada0621622acf4d6053bc59926780`
Runner: `vitest`

## Premises (measured by the rebrief3 drafter at 03:50:55 AEST on 2026-09-22, in a `--shared` scratchpad clone detached at 64ab10513; Wednesday re-derives before queueing)
- THE DEFECT of round 1 (`READY_KS-1171-8J-R15_..._PASS-8of8_2026-09-21.diff.md`, HELD 00:14 09-22): vitest green and checker PASS 8/8, but Seat B 16th's targeted type-check (a temp tsconfig extending anchoring's `tsconfig.json` - `strict`, `noUnusedLocals`, `noUnusedParameters` - with `files=[the test]`, `exclude []`, planted TS2322 control CAUGHT) reports THREE errors in the file, verbatim from `5_Project_History/2026-09-22_seatB-16th/raise/typecheck-ks1171-ks1171-8j-confirmed-wins-over-polled-zero-head.out`:
  - `(8,36): error TS6133: 'beforeEach' is declared but its value is never read.`
  - `(16,1): error TS6133: 'waitForConfirmation' is declared but its value is never read.`
  - `(44,22): error TS6133: 'confirmResult' is declared but its value is never read.`
- THE FIX (only these lines differ from the round-1 fence; every cell, tamper and control is the SAME): (1) line 8 imports `describe, it, expect, vi` only; (2) the `import { waitForConfirmation }` line is GONE (nothing in the file called it; the `vi.mock('../cardano/provider', ...)` block stays); (3) `makeHarness`'s parameter `confirmResult` is now USED: the harness's `confirm` dep is `vi.fn(async () => confirmResult)` (the two RED cells inject the same `confirmed: true ... polled: 0, errored: 3` object they always did, so the behaviour is byte-for-byte the round-1 behaviour; its type `Awaited<ReturnType<AnchorSubmissionDeps['confirm']>>` = the product's `ConfirmationLike` at anchorSubmission.ts:135-149, which the object literals satisfy). The round-1 fence had 128 '+' lines; this one has 127 (one import line removed).
- QUOTE RULE (IMPROVEMENTS 2026-09-22 02:35, the KS-947 finding: the model escapes double quotes on a mixed-quote line): the round-1 fence carried a double-quote character on 3 '+' lines. All three are rewritten single-quote-only WITHOUT changing what runs: the `INPUTS_SPENT_SHORT` message drops the inner quotes around `All inputs are spent` (the product matches `/all inputs are spent/i` at anchorSubmission.ts:115 - case-insensitive, no quotes in the pattern); the second RED cell's title is `RED KS-1171 8j - no never-reached-the-chain log when the transaction was found` (same cell, same assertions, a title with no quote character); one doc-comment word. `grep -c` for `"` over the '+' lines = 0, for a backslash = 0, non-ASCII = 0.
- VERIFIED by the drafter in the clone at 64ab10513: the fence written to its path and type-checked with the SAME instrument shape (`tsconfig.rebrief3-*.json` extending `./tsconfig.json`, `files=[src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts]`, `include []`, `exclude []`, `types ["node","vitest/globals"]`, `npx tsc -p`): 0 errors in the file (the round-1 fence under the same instrument: 3 - the positive control). Golden precheck (this fence as the model output through `tasks/test_only/checker.sh`): see the proposal.
- Tamper: `anchorSubmission.ts:260` at 64ab10513 is `      if (confirmation.confirmed) {` (6 leading spaces; whole-line exact match count 1 - the :401 twin has 10 leading spaces and is a different line; the checker plants by LINE after asserting the bytes). Same tamper as round 1.
- Ticket KS-1171: Backlog; the ticket's product question (the mixed-window design decision) stays with its owner. Nothing in the product changes.

## What is wrong (one paragraph)
`reconfirmKnownSubmission` in `services/anchoring/src/anchorSubmission.ts` checks `confirmation.confirmed` FIRST (:260) and only THEN maps `polled === 0` to `'unknown'`; nothing in the suite pins that ordering, so a future `&& confirmation.polled !== 0` on :260 would turn an injected `confirmed: true, polled: 0` into an un-confirmed row with a retry scheduled and a `never reached the chain` log. The code is RIGHT at the tip. This task is the PIN (test-only): one new vitest file whose two RED cells red under that tamper and whose control (polled: 2) stays green. Round 1 wrote exactly these cells and PASSed; it is re-issued ONLY because its file does not type-check under anchoring's tsconfig (three unused declarations). Reproduce the fence below byte for byte.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts` then ONE `@@ -0,0 +1,127 @@` hunk, every line `+`, no context, no `-`. No product hunk. Copy the 127 lines below byte for byte, in order. Every string in this file is single-quoted; there is NO double-quote character and NO backslash anywhere in the file - never add, escape or change a quote.

## The exact change
```
+/**
+ * KS-1171 - Record 8j TEST-ONLY MODE. The product file at the tip is CORRECT;
+ * `reconfirmKnownSubmission` checks `confirmation.confirmed` FIRST and only
+ * THEN maps `polled === 0` to `'unknown'`. This test exists so a future tamper
+ * of line 260 (`&& confirmation.polled !== 0`) reddens these cells - proving
+ * the ordering matters for one early not-found then an unreachable chain.
+ */
+import { describe, it, expect, vi } from 'vitest';
+import { BlockfrostServerError } from '@blockfrost/blockfrost-js';
+import { createAnchorSubmitter, type AnchorSubmissionDeps, type AnchorSnapshot } from '../anchorSubmission';
+
+vi.mock('../cardano/provider', async (importOriginal) => {
+  const orig = await importOriginal<typeof import('../cardano/provider')>();
+  return { ...orig, getTransaction: vi.fn() };
+});
+
+const TX_A = '408e72087942198b69d686401829b5b9419d018dc4cc64917283aa3cdb084994';
+const ANCHOR_ID = 'anchor_a93bd8dd-10c8-4d52-b12e-c0bff6f5c790';
+
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
+ * Harness copied from ks726 with ONE change: the confirm dep ignores the chain
+ * entirely - injected double returns FOUND but counters say no attempt reached
+ * the chain. Under the ticket's tamper this is what makes the row rest in
+ * 'submitting' instead of 'confirmed'.
+ */
+function makeHarness(confirmResult: Awaited<ReturnType<AnchorSubmissionDeps['confirm']>>) {
+  const SEED_USER_ID = 'seed-user-k1171';
+  const row: AnchorSnapshot = {
+    id: ANCHOR_ID, status: 'pending', transactionHash: undefined, retryCount: 0,
+    metadataLabel: 674, metadataPayload: { documentId: `doc-${SEED_USER_ID}` },
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
+    // INJECTED DOUBLE: ignores the chain and returns the injected confirmResult as-is (confirmed:true, polled: 0 in the RED cells).
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
+  const statusSeq = () => statusWrites.map(w => w.status).filter((s): s is string => typeof s === 'string');
+  const calls = (fn: unknown) => (fn as ReturnType<typeof vi.fn>).mock.calls.length;
+  return { deps, row, statusSeq, signedHashes, logs, calls };
+}
+
+describe('KS-1171 - injected confirmed:true with polled:0 must still CONFIRM the row', () => {
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
+});
+
+describe('KS-1171 control - confirmed:true with polled > 0 confirms too', () => {
+  it('KS-1171 control - confirmed:true with polled 2 confirms the row too', async () => {
+    // Second harness whose stub returns polled: 2, errored: 0. Green at tip AND under tamper.
+    const SEED_USER_ID_C = 'seed-user-k1171-control';
+    const rowC: AnchorSnapshot = {
+      id: ANCHOR_ID, status: 'pending', transactionHash: undefined, retryCount: 0,
+      metadataLabel: 674, metadataPayload: { documentId: `doc-${SEED_USER_ID_C}` },
+    };
+    const logsC: Array<{ level: string; message: string }> = [];
+    const signedHashesC: string[] = [];
+    const submitC = vi.fn(async (_label: number, _payload: object, options?: { onSigned?: (txHash: string) => Promise<void> }) => {
+      if (options?.onSigned) { signedHashesC.push(TX_A); await options.onSigned(TX_A); }
+      throw INPUTS_SPENT_SHORT();
+    });
+    const depsC: AnchorSubmissionDeps = {
+      getAnchor: vi.fn(async () => ({ ...rowC })),
+      submit: submitC,
+      confirm: vi.fn(async () => ({ confirmed: true, confirmations: 1, blockNumber: 4242, slot: 99, blockHash: 'b'.repeat(64), polled: 2, errored: 0 })),
+      updateStatus: vi.fn(async (_id: string, updates: Record<string, unknown>) => {
+        if (typeof updates.status === 'string') rowC.status = updates.status as AnchorSnapshot['status'];
+        if (typeof updates.transactionHash === 'string') rowC.transactionHash = updates.transactionHash;
+      }),
+      bumpRetryCount: vi.fn(),
+      scheduleRetry: vi.fn(),
+      log: vi.fn((level, message) => { logsC.push({ level, message }); }),
+      withWalletLock: makeLock(),
+    };
+    await createAnchorSubmitter(depsC)(ANCHOR_ID);
+
+    expect(rowC.status).toBe('confirmed');
+    expect(logsC.some(l => l.message.startsWith('Anchor confirmation poll never reached the chain'))).toBe(false);
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
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts`); the header `@@ -0,0 +1,127 @@` (127 '+' lines - count them; the R15 batch over-declared new-file headers by 2-20 lines); single quotes only, no `"`, no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
