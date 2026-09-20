# READY — KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1 (Ornith, briefed, test_only, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1284-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 02:03 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden hunk (`cmp`, Wednesday).

**Held 02:03 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (= develop at the hold; #1105 merged). Adds ONE cell to `ks1175-anchor-readback.test.ts` (`buildVerifyResponse` describe) pinning TODAY's chain-source read-back: a schema-valid 76-char `documentId`/`certId` that chunks on chain (2-element arrays, measured) reads back JOINED under `metadata.documentId` and `metadata.certId` after `fromCardanoMetadatum`. Closes the #1105 gate's NOT-PINNED row CHUNKED-DOCUMENTID-ROUNDTRIP. Refs KS-1284 (and KS-1175); NEVER Closes.

**Source read (Wednesday, same action):** 7 `+` lines, all 7 byte-equal (ordered) to `night/briefs/KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1.md`; 0 `-`; one test file (T2); the run's patch BYTE-IDENTICAL to the drafter's golden (`cmp`). First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** DOCIDFROMROWONLY `anchorReadback.ts:111`, CERTIDFROMROWONLY `:112` (each reds exactly the new cell), CODECJOINDROPPED `cardanoMetadatum.ts:81` (reds the new cell + the existing `:88` chain-source cell — declared). Every From byte-matches the tip (count 1 by `grep -c -F -x`, controls `documentid` 2 / `join` 3, checked by Wednesday); T8 restored `9a41f455eb22` / `48497ffc0937` = tip blobs. Controls: 3 full `it` titles, green under all three.

**Checker (tonight):** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_ks1105rows-drafter-precheck/`).

**Collision (measured by Wednesday in a scratch repo at the tip):** the two hunks on `ks1175-anchor-readback.test.ts` (CHUNKED `@@ -80,1 +80,8 @@`, EXPLORERBASE `@@ -107,1 +107,6 @@`) apply in BOTH orders → one sha `431b51cb378e933c`, 133 lines (121+7+5); bad-context control rc 1. IDENTITY-EMPTY-OBJECT is on `ks1175-identity-anchoring.test.ts` (no shared hunk). Drafter's all-six-permutations measure agrees (`runs/2026-09-21_ks1105rows-drafter-precheck/collision_all_orders.log`); both files with all three cells 64/64 green; whole anchoring suite 318/319 at the tip → 321/322 with the three (the 1 red = develop's own `threadTokenMint`, the gate's count). Held READYs touching `services/anchoring/`: KS-1171-8j (new file) and KS-1172-B3 (`anchorSchema.ts:60`, disjoint from `:142-155`/`:306-312`) — no shared file. No live seat owns anchoring (Seat B 11th's six files exclude it, its STATUS 15:28Z).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); anchoring vitest 322 expected with all three (319 + 3), same 1 pre-existing red; tier 2 (test-only pins on anchoring, no auth surface) unless the gate says otherwise; **raise the two readback cells as ONE PR (CHUNKED's hunk first in the diff) and IDENTITY-EMPTY-OBJECT as its own PR, or all three as one — no sequencing needed.** Partition: `services/anchoring/src/__tests__/` owned by no live seat.

---
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts
@@ -80,1 +80,8 @@
+  it('RED KS-1284: chain source: a 76-char documentId and certId that chunked on chain read back joined under metadata.documentId and metadata.certId', () => {
+    const id = 'doc-1-' + 'x'.repeat(70);
+    const chunked = toCardanoMetadatum({ secuura: { hash: 'c'.repeat(64), documentId: id, certId: id } }) as { secuura: Record<string, unknown> };
+    expect(Array.isArray(chunked.secuura.documentId)).toBe(true); // the fixture really is chunked (76 chars is over the 64-byte cap)
+    const body = buildVerifyResponse('chain', fromCardanoMetadatum(chunked), undefined, { hash: 'c'.repeat(64), network: 'preview' });
+    expect([body.metadata.documentId, body.metadata.certId]).toEqual([id, id]);
+  });
   it('db source: metadata.identity beside metadata.identityCommitment, from the logical payload', () => {
