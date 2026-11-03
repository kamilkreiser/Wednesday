# READY — KS-1868-KS-1868-O93-P4 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 10:02 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:02 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `66cbe4e52d5afadc9d13ca141200026cc68d5095`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/anchorStateSync.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
119	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchorStateSync.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/anchorStateSync.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts 119 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the healAnchorForVerify write catch presents the healed blob and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the write is logged as text and the verify presents the confirmed blob, as for an ordinary Error', 'KS-1868 the healAnchorForVerify write catch presents the healed blob and logs text for a hostile thrown value RED ks1868 R2: an Error whose message getter throws from the write is logged as text and the verify presents the confirmed blob, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2375 failed=11 | after: total=2379 failed=11` · `NEW reds: []` [baseline_suite.json total=2375 failed=11; after_suite.json total=2379 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/anchorStateSync.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts` (+119/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/anchorStateSync.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `66cbe4e52d5afadc9d13ca141200026cc68d5095` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p4_originate_anchor_state_sync_heal_write_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts b/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
--- a/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
+++ b/Blockchain/Dev/services/originate/src/services/anchorStateSync.ts
@@ -597,7 +597,13 @@
       logger.info('Verify heal: anchor state confirmed through the resolver (KS-584, KS-1384 R2b)', { documentId: input.documentId, anchorId, txHash: d.tx, via: d.via, written });
     } catch (err: unknown) {
       // Presentation already has the decision; the write is convergence, and the reconcile and the poller are the catch-all.
-      logger.warn('Verify heal: the confirmed write failed (presentation unaffected)', { documentId: input.documentId, error: err instanceof Error ? err.message : String(err) });
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.warn('Verify heal: the confirmed write failed (presentation unaffected)', { documentId: input.documentId, error: reason });
     }
   }
   return healed;
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts
@@ -0,0 +1,119 @@
+// KS-1868 (operator 93 screen, originate anchorStateSync): the catch around the confirmed write of healAnchorForVerify (line 600) of
+// services/originate/src/services/anchorStateSync.ts reads `err instanceof Error ? err.message : String(err)` inside the logger call's arguments, unguarded.
+// A thrown value whose read throws (a revoked Proxy: `instanceof` throws; an Error whose message getter throws) makes the catch throw, so
+// healAnchorForVerify REJECTS and the verify presents nothing, where an ordinary Error is logged ("presentation unaffected") and the healed blob is
+// returned for presentation;  The cells make the
+// conditional blob write reject with such a value and assert the verify resolves with the confirmed blob and the line carries text (the constant
+// when the value cannot be turned into text). Harness: the ks1384 verify-heals suite (same mocks and fetch stand-in); the write stand-in is a plain
+// function, not jest.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+const mockState: { toThrow: unknown; warned: unknown[][]; writes: number } = { toThrow: undefined, warned: [], writes: 0 };
+
+jest.mock('../repositories/documentRepo', () => ({
+  getDocument: async () => null,
+  updateDocument: async () => {
+    throw new Error('updateDocument must not be called by a heal');
+  },
+  writeAnchorBlobIf: (..._a: unknown[]) => {
+    mockState.writes += 1;
+    return Promise.reject(mockState.toThrow);
+  },
+}));
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    error: () => undefined,
+    warn: (...args: unknown[]) => {
+      mockState.warned.push(args);
+    },
+  },
+}));
+
+import { healAnchorForVerify } from '../services/anchorStateSync';
+import { verifyHealFetch } from './helpers/verifyHealFetch';
+
+const DOC = 'doc-ks1868-heal-write';
+const PK = '7c1868b2-0000-4000-8000-0000000000a5';
+const TENANT = 'a0000000-0000-4000-8000-000000000001';
+const TX_OLD = '0a'.repeat(32);
+const TX_CREATE = 'c1'.repeat(32);
+const T_CREATE = '2026-10-31T10:00:00.000Z';
+const OLD = '2026-10-31T09:00:00.000Z';
+const realFetch = global.fetch;
+
+beforeEach(() => {
+  mockState.toThrow = undefined;
+  mockState.warned.length = 0;
+  mockState.writes = 0;
+  const f = verifyHealFetch({
+    row: { id: 'anchor_v', documentId: DOC, status: 'failed', transactionHash: null, errorMessage: 'All inputs are spent' },
+    ownCreate: { outcome: 'found', bound: { tx: TX_CREATE, blockNumber: 4242 }, loose: [] },
+  });
+  global.fetch = f.fetch as unknown as typeof fetch;
+});
+afterAll(() => {
+  global.fetch = realFetch;
+});
+
+const WRITE_FAILED = 'Verify heal: the confirmed write failed (presentation unaffected)';
+const LINE = (): Record<string, unknown>[] =>
+  mockState.warned.filter((a) => a[0] === WRITE_FAILED).map((a) => a[1] as Record<string, unknown>);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
+
+async function heal(value: unknown): Promise<{ threw: boolean; status: unknown; txHash: unknown }> {
+  mockState.toThrow = value;
+  try {
+    const presented = (await healAnchorForVerify({
+      documentId: DOC,
+      documentPk: PK,
+      tenantId: TENANT,
+      blob: { status: 'pending', txHash: TX_OLD, anchorId: 'anchor_v', createAttempts: [T_CREATE], blockHeight: null, anchoredAt: T_CREATE },
+      contentHash: 'a'.repeat(64),
+      updatedAt: OLD,
+      authHeader: 'Bearer v',
+      write: true,
+    })) as Record<string, unknown> | null;
+    return { threw: false, status: presented?.status, txHash: presented?.txHash };
+  } catch {
+    return { threw: true, status: undefined, txHash: undefined };
+  }
+}
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the healAnchorForVerify write catch presents the healed blob and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the write is logged with its message and the verify presents the confirmed blob', async () => {
+    expect(await heal(new Error('write boom'))).toEqual({ threw: false, status: 'confirmed', txHash: TX_CREATE });
+    expect(mockState.writes).toBe(1);
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('write boom');
+  });
+  it('control ks1868 C2: a thrown plain string is logged as its text and the verify presents the confirmed blob', async () => {
+    expect(await heal('plain boom')).toEqual({ threw: false, status: 'confirmed', txHash: TX_CREATE });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('plain boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the write is logged as text and the verify presents the confirmed blob, as for an ordinary Error', async () => {
+    expect(await heal(revokedProxy())).toEqual({ threw: false, status: 'confirmed', txHash: TX_CREATE });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the write is logged as text and the verify presents the confirmed blob, as for an ordinary Error', async () => {
+    expect(await heal(getterThrows())).toEqual({ threw: false, status: 'confirmed', txHash: TX_CREATE });
+    expect(LINE()).toHaveLength(1);
+    expect(reasonOf(LINE()[0])).toBe('unreadable thrown value');
+  });
+});
```
