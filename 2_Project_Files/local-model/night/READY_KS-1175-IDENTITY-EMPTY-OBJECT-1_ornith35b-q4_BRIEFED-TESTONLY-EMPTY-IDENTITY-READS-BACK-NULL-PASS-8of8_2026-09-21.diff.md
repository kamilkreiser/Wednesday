# READY — KS-1175-IDENTITY-EMPTY-OBJECT-1 (Ornith, briefed, test_only, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1175-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 02:03 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden hunk (`cmp`, Wednesday).

**Held 02:03 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (= develop at the hold; #1105 merged). Adds ONE cell to `ks1175-identity-anchoring.test.ts` (negative-controls describe) pinning TODAY's chain: `identity: {}` on the request parses, anchors NO identity key (the builder's seven spreads), and reads back `identity: null` on the view, never `{}` (`anchorReadback.ts:52`). Uses the file's own `SEVEN` and `await import('../anchorReadback')` inside the async cell (the KS-753 idiom) so it stays one hunk. Closes the #1105 gate's NOT-PINNED row IDENTITY-EMPTY-OBJECT. Refs KS-1175; NEVER Closes.

**Source read (Wednesday, same action):** 7 `+` lines, all 7 byte-equal (ordered) to the brief; 0 `-`; one test file; the run's patch BYTE-IDENTICAL to the golden; green at the tip 52/52 cells in the file. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** EMPTYIDENTITYKEPT `anchorReadback.ts:52` → `    identity,` (reds exactly the new cell in its file; frame stated: the same tamper reds 4 absent-identity cells in the SIBLING readback file — `:52` was pinned for the ABSENT case; this cell adds the `{}` case through schema→builder→view). From byte-matches the tip (count 1, checked by Wednesday); T8 restored by bytes. Controls: 3 full `it` titles.

**Checker (tonight):** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_ks1105rows-drafter-precheck/`).

**Collision (measured by Wednesday in a scratch repo at the tip):** the two hunks on `ks1175-anchor-readback.test.ts` (CHUNKED `@@ -80,1 +80,8 @@`, EXPLORERBASE `@@ -107,1 +107,6 @@`) apply in BOTH orders → one sha `431b51cb378e933c`, 133 lines (121+7+5); bad-context control rc 1. IDENTITY-EMPTY-OBJECT is on `ks1175-identity-anchoring.test.ts` (no shared hunk). Drafter's all-six-permutations measure agrees (`runs/2026-09-21_ks1105rows-drafter-precheck/collision_all_orders.log`); both files with all three cells 64/64 green; whole anchoring suite 318/319 at the tip → 321/322 with the three (the 1 red = develop's own `threadTokenMint`, the gate's count). Held READYs touching `services/anchoring/`: KS-1171-8j (new file) and KS-1172-B3 (`anchorSchema.ts:60`, disjoint from `:142-155`/`:306-312`) — no shared file. No live seat owns anchoring (Seat B 11th's six files exclude it, its STATUS 15:28Z).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); anchoring vitest 322 expected with all three (319 + 3), same 1 pre-existing red; tier 2 (test-only pins on anchoring, no auth surface) unless the gate says otherwise; **raise the two readback cells as ONE PR (CHUNKED's hunk first in the diff) and IDENTITY-EMPTY-OBJECT as its own PR, or all three as one — no sequencing needed.** Partition: `services/anchoring/src/__tests__/` owned by no live seat.

---
--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts
@@ -176,1 +176,8 @@
+  it('RED KS-1175: identity: {} on the request anchors no identity key and reads back identity: null on the view, never {}', async () => {
+    const { anchorIdentityView } = await import('../anchorReadback');
+    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, identity: {} });
+    expect(result.success).toBe(true);
+    const sec = buildFlatAnchorMetadataPayload(anchorDocumentSchema.parse({ ...BASE_BODY, identity: {} }), 'preview').secuura;
+    expect([SEVEN.filter((k) => k in sec), anchorIdentityView(sec).identity]).toEqual([[], null]);
+  });
   it('R5: an unknown key inside identity is stripped and its free text never reaches the payload', () => {
