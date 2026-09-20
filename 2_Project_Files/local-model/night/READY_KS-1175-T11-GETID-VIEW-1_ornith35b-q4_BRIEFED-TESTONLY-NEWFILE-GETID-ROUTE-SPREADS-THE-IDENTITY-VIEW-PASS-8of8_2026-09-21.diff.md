# READY — KS-1175-T11-GETID-VIEW-1 (Ornith, briefed, test_only NEW FILE, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1175-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 02:38 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 02:38 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds a NEW test file `anchoring/src/__tests__/ks1175-getid-view-wired.test.ts` (26 lines, `test_mode: new` — the builder's documented mode, 4 prior inputs): an fs source-text guard that the `app.get('/api/anchors/:id', …)` block in `index.ts` carries the `...anchorIdentityView((anchor.metadataPayload as any)?.secuura)` spread (the #1105 gate's NOT-PINNED row T11-GETID-VIEW — `index.ts` calls `app.listen` on import, so the route cannot be driven bootless; the real pin is the §5f live sweep, Kam's). Refs KS-1175; NEVER Closes.

**Source read (Wednesday, same action):** 26 `+` lines (`--- /dev/null`), all 26 byte-equal (ordered) to the brief; 0 `-`; one new file; the run's patch BYTE-IDENTICAL to the golden. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** GETIDVIEWDROPPED `index.ts:890` (the gate's: the spread → a comment) and GETIDVIEWWRONGSOURCE `:890` (each reds exactly `spread` by assertion; From byte-matches the tip, count 1, control `anchorIdentityView` 2, checked by Wednesday); T8 restored by bytes. Controls: 1 full `it` title (the block is found). 2/2 cells green at the tip.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_wave3-drafter-precheck/`).

**Collision (drafter, 8 orders on a fresh clone; Wednesday re-derived the tamper lines and key sets):** NEW files collide with nothing by construction; the tamper files (`index.ts`, `transaction.ts`) are planted-and-restored. With the three held readback/identity READYs, every order applies rc 0 (held files `431b51cb378e933c` / `ee1cbe52ea87bc02` unchanged); whole anchoring with all six cells **329/328/1** (the 1 red = develop's own `threadTokenMint`, the gate's count). `grep night/READY_*` for `anchoring/src/index.ts`, `cardano/transaction.ts` and the three new names: 0. No live seat owns anchoring.

**For the raise seat:** strict apply (`--- /dev/null` new file); TEST-ONLY (STOP on any product byte); anchoring vitest at the tip 319 → with all SIX anchoring READYs 329 (+3 cells here across the three new files + 3 in the held two); tier 2 unless the gate says otherwise; **raise all six anchoring READYs as ONE PR** (readback pair first in the diff, then identity, then the three new files) — no sequencing needed.

---
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-getid-view-wired.test.ts
@@ -0,0 +1,26 @@
+/**
+ * KS-1175 - GET /api/anchors/:id is wired to anchorIdentityView (the #1105 gate's T11-GETID-VIEW seam).
+ * index.ts calls app.listen on import, so no test imports it and the route body cannot be driven in-process.
+ * This is a SOURCE-TEXT guard: it reads index.ts and asserts the app.get('/api/anchors/:id') handler still spreads
+ * anchorIdentityView(...) over the row's metadata_payload secuura block into its res.json. It stops the spread being
+ * dropped or re-pointed silently (every cell of the suite stayed green under both at the #1105 gate); the REAL pin is
+ * the section 5f live sweep (GET /:id on the correct host returning identity for a confirmed anchor).
+ */
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+function handlerBlock(opener: string, lastLine: string): string {
+  const from = SRC.indexOf(opener);
+  const end = from < 0 ? -1 : SRC.indexOf(lastLine, from);
+  return from < 0 || end < 0 ? '' : SRC.slice(from, end + lastLine.length);
+}
+const GET_BY_ID = handlerBlock("app.get('/api/anchors/:id',", 'retryCount: anchor.retryCount ?? 0,');
+describe('KS-1175 GET /api/anchors/:id carries the identity view (source guard: index.ts is bootless)', () => {
+  it('RED KS-1175: the GET /api/anchors/:id handler spreads anchorIdentityView of the row metadata_payload secuura block into res.json', () => {
+    expect([GET_BY_ID.length > 0, GET_BY_ID.includes('...anchorIdentityView((anchor.metadataPayload as any)?.secuura),')]).toEqual([true, true]);
+  });
+  it('CONTROL: the located block is ONE handler, the anchor-by-id route (contentHash and the KS-535 errorMessage are in it)', () => {
+    expect([GET_BY_ID.split('app.get(').length, GET_BY_ID.includes('contentHash: anchor.contentHash,'), GET_BY_ID.includes('errorMessage: anchor.errorMessage || null,')]).toEqual([2, true, true]);
+  });
+});
