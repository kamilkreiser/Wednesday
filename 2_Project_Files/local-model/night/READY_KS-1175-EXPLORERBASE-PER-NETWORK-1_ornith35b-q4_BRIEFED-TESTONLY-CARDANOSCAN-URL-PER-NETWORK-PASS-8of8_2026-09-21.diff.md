# READY — KS-1175-EXPLORERBASE-PER-NETWORK-1 (Ornith, briefed, test_only, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1175-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 02:03 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden hunk (`cmp`, Wednesday).

**Held 02:03 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (= develop at the hold; #1105 merged). Adds ONE cell to `ks1175-anchor-readback.test.ts` pinning TODAY's `cardanoScanUrl` per network: mainnet has no subdomain, every other network is prefixed with its own name (`buildVerifyResponse` over mainnet/preview/preprod). Closes the #1105 gate's NOT-PINNED row EXPLORERBASE-PER-NETWORK. **Gate slip found by the drafter and carried:** the row said no cell names cardanoscan — `:113` already pins the PREVIEW URL (count 2 in the file); only the MAINNET arm was unpinned, and MAINNETPREFIXED isolates it. Refs KS-1175; NEVER Closes.

**Source read (Wednesday, same action):** 5 `+` lines (URLs by `+` concatenation, no backtick), all 5 byte-equal (ordered) to the brief; 0 `-`; one test file; the run's patch BYTE-IDENTICAL to the golden. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** NETWORKINVERTED `anchorReadback.ts:74` (`===`→`!==`, the gate's; reds the new cell AND the existing `CONTROL:` cell at `:113` — declared), MAINNETPREFIXED `:75` (mainnet gains a `mainnet.` subdomain; reds the new cell only). Both From lines byte-match the tip (count 1 each, control `cardanoscan` 3, checked by Wednesday); T8 restored by bytes. Controls: 3 full `it` titles.

**Checker (tonight):** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_ks1105rows-drafter-precheck/`).

**Collision (measured by Wednesday in a scratch repo at the tip):** the two hunks on `ks1175-anchor-readback.test.ts` (CHUNKED `@@ -80,1 +80,8 @@`, EXPLORERBASE `@@ -107,1 +107,6 @@`) apply in BOTH orders → one sha `431b51cb378e933c`, 133 lines (121+7+5); bad-context control rc 1. IDENTITY-EMPTY-OBJECT is on `ks1175-identity-anchoring.test.ts` (no shared hunk). Drafter's all-six-permutations measure agrees (`runs/2026-09-21_ks1105rows-drafter-precheck/collision_all_orders.log`); both files with all three cells 64/64 green; whole anchoring suite 318/319 at the tip → 321/322 with the three (the 1 red = develop's own `threadTokenMint`, the gate's count). Held READYs touching `services/anchoring/`: KS-1171-8j (new file) and KS-1172-B3 (`anchorSchema.ts:60`, disjoint from `:142-155`/`:306-312`) — no shared file. No live seat owns anchoring (Seat B 11th's six files exclude it, its STATUS 15:28Z).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); anchoring vitest 322 expected with all three (319 + 3), same 1 pre-existing red; tier 2 (test-only pins on anchoring, no auth surface) unless the gate says otherwise; **raise the two readback cells as ONE PR (CHUNKED's hunk first in the diff) and IDENTITY-EMPTY-OBJECT as its own PR, or all three as one — no sequencing needed.** Partition: `services/anchoring/src/__tests__/` owned by no live seat.

---
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts
@@ -107,1 +107,6 @@
+  it('RED KS-1175: cardanoScanUrl: mainnet has no subdomain, every other network is prefixed with its own name', () => {
+    const tx = 'h'.repeat(64);
+    const urls = ['mainnet', 'preview', 'preprod'].map((n) => buildVerifyResponse('db', {}, { transaction_hash: tx }, { hash: HASH, network: n }).cardanoScanUrl);
+    expect(urls).toEqual(['https://cardanoscan.io/transaction/' + tx, 'https://preview.cardanoscan.io/transaction/' + tx, 'https://preprod.cardanoscan.io/transaction/' + tx]);
+  });
   it('CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction', () => {
