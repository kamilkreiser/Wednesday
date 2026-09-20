# READY — KS-1284-T12-CHAINREAD-DECODE-1 (Ornith, briefed, test_only NEW FILE, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1284-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 02:38 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 02:38 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds a NEW test file `ks1284-chain-read-order.test.ts` (43 lines): a six-line order/uniqueness guard on `index.ts:695-702` (the `for (const { tx, md } of metas)` loop in `handleAnchorVerifyByHash` — `fromCardanoMetadatum` is applied to the chain entry BEFORE the hash compare) plus a behavioural `scan()` twin as CONTROL. The #1105 gate's NOT-PINNED row T12-CHAINREAD-DECODE. Refs KS-1284; NEVER Closes.

**Source read (Wednesday, same action):** 43 `+` lines (`--- /dev/null`), all 43 byte-equal (ordered) to the brief; 0 `-`; one new file; patch BYTE-IDENTICAL to the golden. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** CHAINREADNODECODE `index.ts:699` (the gate's: the decode removed) and HASHCOMPARERAW `:701` (each reds exactly its declared cell; From lines byte-match the tip, count 1 each, checked by Wednesday); T8 restored by bytes. Measured cross-red (drafter): the held CHUNKED brief's CODECJOINDROPPED reds this file's CONTROL only — stated, not a collision. 2/2 cells green at the tip.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_wave3-drafter-precheck/`).

**Collision (drafter, 8 orders on a fresh clone; Wednesday re-derived the tamper lines and key sets):** NEW files collide with nothing by construction; the tamper files (`index.ts`, `transaction.ts`) are planted-and-restored. With the three held readback/identity READYs, every order applies rc 0 (held files `431b51cb378e933c` / `ee1cbe52ea87bc02` unchanged); whole anchoring with all six cells **329/328/1** (the 1 red = develop's own `threadTokenMint`, the gate's count). `grep night/READY_*` for `anchoring/src/index.ts`, `cardano/transaction.ts` and the three new names: 0. No live seat owns anchoring.

**For the raise seat:** strict apply (`--- /dev/null` new file); TEST-ONLY (STOP on any product byte); anchoring vitest at the tip 319 → with all SIX anchoring READYs 329 (+3 cells here across the three new files + 3 in the held two); tier 2 unless the gate says otherwise; **raise all six anchoring READYs as ONE PR** (readback pair first in the diff, then identity, then the three new files) — no sequencing needed.

---
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1284-chain-read-order.test.ts
@@ -0,0 +1,43 @@
+/**
+ * KS-1284 - verify-by-hash decodes the chain payload BEFORE it compares the hash (the #1105 gate's T12-CHAINREAD-DECODE
+ * seam). The loop lives in index.ts's handleAnchorVerifyByHash, and index.ts calls app.listen on import, so it cannot be
+ * imported here. Two cells: a SOURCE-TEXT guard that the five loop lines are still there, in that order, with the
+ * fromCardanoMetadatum decode on the line before the hash compare; and a behavioural twin that copies those lines into a
+ * local scan() and shows WHY the order matters - a chunked sha256:-prefixed hash is found only through the decode.
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+import { toCardanoMetadatum, fromCardanoMetadatum } from '../cardano/cardanoMetadatum';
+const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+const LOOP = [
+  'for (const { tx, md } of metas) {',
+  "const secEntry = (md || []).find((m: any) => String(m.label) === '674');",
+  'const sec: any = fromCardanoMetadatum(secEntry?.json_metadata?.secuura);',
+  'if (!sec) continue;',
+  "const onChainHash = String(sec.hash || '').replace(/^sha256:/i, '').toLowerCase();",
+  'if (onChainHash !== hash) continue;',
+];
+type Meta = { tx: { tx_hash: string }; md: any[] | null };
+function scan(metas: Meta[], hash: string, decode: (v: unknown) => unknown): string | null {
+  for (const { tx, md } of metas) {
+    const secEntry = (md || []).find((m: any) => String(m.label) === '674');
+    const sec: any = decode(secEntry?.json_metadata?.secuura);
+    if (!sec) continue;
+    const onChainHash = String(sec.hash || '').replace(/^sha256:/i, '').toLowerCase();
+    if (onChainHash !== hash) continue;
+    return tx.tx_hash;
+  }
+  return null;
+}
+describe('KS-1284 verify-by-hash chain read: decode before compare (source guard + behavioural twin)', () => {
+  it('RED KS-1284: the six loop lines of handleAnchorVerifyByHash are present once, in order, with the decode before the hash compare', () => {
+    const at = LOOP.map((l) => SRC.indexOf(l));
+    expect([at.every((i) => i > 0), at.every((i, k) => k === 0 || i > at[k - 1]), LOOP.every((l) => SRC.indexOf(l) === SRC.lastIndexOf(l))]).toEqual([true, true, true]);
+  });
+  it('CONTROL: a chunked sha256:-prefixed hash on chain is found through the decode and never without it', () => {
+    const h = 'c'.repeat(64);
+    const metas: Meta[] = [{ tx: { tx_hash: 'a'.repeat(64) }, md: [{ label: '674', json_metadata: toCardanoMetadatum({ secuura: { hash: 'sha256:' + h } }) }] }];
+    expect([scan(metas, h, fromCardanoMetadatum), scan(metas, h, (v) => v)]).toEqual(['a'.repeat(64), null]);
+  });
+});
