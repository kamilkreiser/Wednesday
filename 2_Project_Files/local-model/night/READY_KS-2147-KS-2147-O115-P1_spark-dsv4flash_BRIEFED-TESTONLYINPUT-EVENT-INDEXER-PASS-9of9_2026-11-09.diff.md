# READY - KS-2147-KS-2147-O115-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2147_o115_p1_event_indexer_site3_process_transaction_rate_limit_cells/out.md.checker/patch.diff` (from `ls` at 16:45 2026-11-09; sha256[:16] 8aeff8a57746c0ec, 2107 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 16:45 2026-11-09 by Spark operator o115 after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2147_o115_p1_event_indexer_site3_process_transaction_rate_limit_cells/out.md.checker`; product bytes were RE-MEASURED here.** Tip `6beac8734a2f607200e3e71371b84268e1599029`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-poll-survives-an-unreadable-throw-at-the-rate-limit-check.test.ts']; `+` lines 38 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` blob b7516622960b; plant file(s) also unchanged.
- Red cells [input.json]:
  - `ks2147 N1 site 3: a 429 thrown by txsUtxos backs off`
  - `ks2147 N2 site 3: an unreadable value thrown by txsUtxos reaches onError once as an Error`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-poll-survives-an-unreadable-throw-at-the-rate-limit-check.test.ts)`
  - `PASS A3p the plant applies at the tip (1 pinned line(s))`
  - `PASS A4 GREEN WITHOUT PLANT: 2 red cell(s) exist and pass on the unmodified product; declared files 8 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1618 -> 1620, red 1 -> 1`
  - `PASS A5 RED WITH PLANT: 2 red cell(s) fail by assertion under the plant (Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-poll-survives-an-unreadable-throw-at-the-rate-limit-check.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-poll-survives-an-unreadable-throw-at-the-rate-limit-check.test.ts
@@ -118,4 +118,42 @@
     expect(inner.lastProcessedBlock).toBe(5);
     expect(received.length).toBe(1);
   });
+
+  // KS-2147 (gate 273 G273-2104-1): site 3, the catch in processTransaction, is driven by no cell above. One block, one transaction, txsUtxos throws.
+  async function pollSiteThree(value: unknown) {
+    const received: unknown[] = [];
+    const indexer = new ContractEventIndexer({
+      policyIds: ['ks2147-policy'],
+      onError: (e: Error) => {
+        received.push(e);
+      },
+    } as never);
+    const inner = indexer as unknown as { running: boolean; api: unknown; lastProcessedBlock: number; backoffMs: number; poll(): Promise<void> };
+    inner.running = true;
+    inner.lastProcessedBlock = 5;
+    inner.api = {
+      blocksLatest: async () => ({ height: 6 }),
+      blocksByNumber: async () => ({ tx_count: 1 }),
+      blocksByNumberTxs: async () => ['ks2147-tx'],
+      txsUtxos: async () => {
+        throw value;
+      },
+    };
+    await inner.poll();
+    return { received, backoffMs: inner.backoffMs, lastProcessedBlock: inner.lastProcessedBlock };
+  }
+
+  it('control ks2147 N1 site 3: a 429 thrown by txsUtxos backs off, does not reach onError and the block is marked processed', async () => {
+    const out = await pollSiteThree(new Error('429 Too Many Requests'));
+    expect(out.received.length).toBe(0);
+    expect(out.backoffMs).toBe(2000);
+    expect(out.lastProcessedBlock).toBe(6);
+  });
+
+  it('control ks2147 N2 site 3: an unreadable value thrown by txsUtxos reaches onError once as an Error and the block is left unprocessed', async () => {
+    const out = await pollSiteThree(revokedProxy());
+    expect(out.received.length).toBe(1);
+    expect(out.received[0] instanceof Error).toBe(true);
+    expect(out.lastProcessedBlock).toBe(5);
+  });
 });
```
