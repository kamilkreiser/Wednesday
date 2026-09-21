# KS-1171 R15-8j - re-brief of the held READY at develop 9f0265eb0 (written 20:35 on 2026-09-21 by Wednesday's census15 drafter from the file at the tip - 0 lines read whole)
File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`

## Premises (measured by the census15 drafter at 20:35:38 AEST, in a `--shared` scratchpad clone detached at the tip; Wednesday re-derives before queueing)
- Source READY: `night/READY_KS-1171-8j_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15.diff.md` (its checker PASS was at an OLDER tip; run dir GONE/unnamed - the READY fence is the patch); canonical patch 5650 B sha256[:16] `d2e76d0a310be04c`, +108/-0.
- The old patch at the tip: strict rc 0 / --recount rc 0 / --directory=Blockchain/Dev rc 0 / -R rc 1 -> effective mode **strict**; the old READY's + lines PRESENT at the tip: NO (content absent - un-merged).
- The test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts` at the tip: ABSENT - ONE NEW FILE. Mode: **NEW**.
- Tamper source: the old brief `night/briefs/KS-1171.md` (its `## Tamper` line/from/to, converted to the current `### ID` shape). Each From located at the tip by exact whole-line match (count in the Tampers section).
- Ticket KS-1171: Backlog, assignee kamil.kreiser@secuura.ai, PR attachments none (all merged); briefs already on disk: KS-1171.md.
- Generator notes: none.

## What is wrong (one paragraph)
The held READY's own summary, verbatim from its header (the model wrote these cells once and the checker passed them at tip 2026-09-15; the run is re-done at the CURRENT tip so the checker verdicts it fresh):
> # READY — KS-1171-8j — Ornith ornith:35b-q8_0 PASS 7/7 first run on q8 (the q4 twin is held beside it; either may be raised), TEST-ONLY mode, 2026-09-15 12:33 — tip develop M55 48e65c435
> # Run: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1171-ornith35b-q8_0-night. Cells as the brief's; red under the tamper, green at the tip. HELD for a Secuura seat.
This task asks for the SAME cells, re-derived at develop `9f0265eb0`. Nothing in the product changes. The old diff still applies at the tip in mode strict - emit the same cells, anchored on the lines quoted below.

## THE MODE - read this twice
TEST-ONLY, ONE NEW FILE: your diff contains EXACTLY ONE file, the NEW test file above: `--- /dev/null` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts` then ONE `@@ -0,0 +1,N @@` hunk, every line `+`, no context, no `-`. No product hunk. 

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
+import { waitForConfirmation } from '../cardano/confirmation';
+
+const TX_A = '408e72087942198b69d686401829b5b9419d018dc4cc64917283aa3cdb084994';
+const ANCHOR_ID = 'anchor_a93bd8dd-10c8-4d52-b12e-c0bff6f5c790';
+
+/** The node reply guard 3 matches so it enters the re-poll path instead of retrying. */
+const INPUTS_SPENT_SHORT = () =>
+  new BlockfrostServerError({
+    status_code: 400,
+    error: 'Bad Request',
+    message: 'Transaction submission failed: ConwayMempoolFailure "All inputs are spent"',
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
+function makeHarness(confirmResult: ReturnType<typeof waitForConfirmation>) {
+  const SEED_USER_ID = 'seed-user-for-harness';
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
+  it('RED KS-1171 8j - no "never reached the chain" log when the transaction was found', async () => {
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

## Cells (every cell RED or CONTROL; the names below are the EXACT it() titles)
- `RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row`
- `RED KS-1171 8j - no "never reached the chain" log when the transaction was found`
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
Reds: `RED KS-1171 8j - an injected confirmed:true with polled 0 CONFIRMS the row`, `RED KS-1171 8j - no "never reached the chain" log when the transaction was found`
(From located at the tip: 1 match(es); the old brief/input said line 260)

## Controls
- `KS-1171 control - confirmed:true with polled 2 confirms the row too`

## Output
Exactly ONE ```diff block; paths repo-relative (`Blockchain/Dev/services/anchoring/src/__tests__/ks1171-guard-3-s-re-poll-reads.test.ts`); correct hunk counts; no `\$` / `\u` / backslash escapes in a `+` line; the cell titles EXACTLY as listed (the checker matches the full title).
