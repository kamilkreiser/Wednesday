# READY — KS-1972-KS-1972-O107-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/out.md.checker/patch.diff`** (from `ls` at 04:17 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:17 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2935f723109756a60cadc5521977c7a036ec322d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
9	0	Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
100	0	Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: event-indexer.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts 9 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts 100 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1972 ContractEventIndexer.poll survives a thrown value whose read throws RED ks1972 R1 a revoked Proxy reaches onError as an Error with a constant reason and poll resolves', 'KS-1972 ContractEventIndexer.poll survives a thrown value whose read throws RED ks1972 R2 a Proxy whose get trap throws reaches onError as an Error with a constant reason and poll resolves', 'KS-1972 ContractEventIndexer.poll survives a thrown value whose read throws RED ks1972 R3 an Error whose message getter throws reaches onError as is and poll resolves']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1597 failed=1 | after: total=1602 failed=1` · `NEW reds: []` [baseline_suite.json total=1597 failed=1; after_suite.json total=1602 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts` (+9/-0 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts` (+100/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2935f723109756a60cadc5521977c7a036ec322d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1972_o107_p1_shared_event_indexer_is_rate_limited_survives_unreadable_value/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts b/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
--- a/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
+++ b/Blockchain/Dev/packages/shared/src/blockchain/event-indexer.ts
@@ -334,2 +334,11 @@
   private isRateLimited(err: any): boolean {
+    try {
+      return this.readsAsRateLimited(err);
+    } catch {
+      // KS-1972: a thrown value whose read throws is not a rate limit; answer false so the caller reaches handleError.
+      return false;
+    }
+  }
+
+  private readsAsRateLimited(err: any): boolean {
     return (
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1972-event-indexer-is-rate-limited-unreadable-throw.test.ts
@@ -0,0 +1,100 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1972: ContractEventIndexer.isRateLimited (src/blockchain/event-indexer.ts) reads `err?.status_code`, `err?.statusCode`,
+// `err?.response?.status` and `err?.message` of a thrown value with no guard, and poll() calls it BEFORE handleError. When the
+// read throws (a revoked Proxy, a Proxy whose get trap throws, an Error whose message getter throws) the throw leaves poll()'s
+// catch, so poll() rejects and handleError (which already survives such values) is never reached. The cells make the Blockfrost
+// stand-in reject with such a value and assert poll() resolves and onError is called, as for an ordinary Error. The api object
+// is a plain stand-in, the indexer is reached through a type cast, no network, no timers.
+import { ContractEventIndexer } from '../blockchain/event-indexer';
+
+type Outcome = { rejected: boolean; received: unknown[]; backoffMs: unknown };
+
+async function pollWith(value: unknown): Promise<Outcome> {
+  const received: unknown[] = [];
+  const indexer = new ContractEventIndexer({
+    onError: (e: Error) => {
+      received.push(e);
+    },
+  } as never);
+  const inner = indexer as unknown as { running: boolean; api: unknown; backoffMs: number; poll(): Promise<void> };
+  inner.running = true;
+  inner.api = {
+    blocksLatest: async () => {
+      throw value;
+    },
+  };
+  let rejected = false;
+  try {
+    await inner.poll();
+  } catch {
+    rejected = true;
+  }
+  return { rejected, received, backoffMs: inner.backoffMs };
+}
+
+const messageOf = (o: Outcome): unknown => (o.received[0] as { message?: unknown } | undefined)?.message;
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getTrapThrows = (): unknown =>
+  new Proxy(
+    {},
+    {
+      get() {
+        throw new Error('get trap boom');
+      },
+    },
+  );
+
+const messageGetterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1972 ContractEventIndexer.poll survives a thrown value whose read throws', () => {
+  it('control ks1972 C1 an ordinary Error reaches onError as is and poll resolves', async () => {
+    const err = new Error('rpc down');
+    const out = await pollWith(err);
+    expect(out.rejected).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(out.received[0] === err).toBe(true);
+  });
+
+  it('control ks1972 C2 a 429 Error backs off and does not reach onError', async () => {
+    const out = await pollWith(new Error('429 Too Many Requests'));
+    expect(out.rejected).toBe(false);
+    expect(out.received.length).toBe(0);
+    expect(out.backoffMs).toBe(2000);
+  });
+
+  it('RED ks1972 R1 a revoked Proxy reaches onError as an Error with a constant reason and poll resolves', async () => {
+    const out = await pollWith(revokedProxy());
+    expect(out.rejected).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(messageOf(out)).toBe('unreadable thrown value');
+  });
+
+  it('RED ks1972 R2 a Proxy whose get trap throws reaches onError as an Error with a constant reason and poll resolves', async () => {
+    const out = await pollWith(getTrapThrows());
+    expect(out.rejected).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(messageOf(out)).toBe('unreadable thrown value');
+  });
+
+  it('RED ks1972 R3 an Error whose message getter throws reaches onError as is and poll resolves', async () => {
+    const err = messageGetterThrows();
+    const out = await pollWith(err);
+    expect(out.rejected).toBe(false);
+    expect(out.received.length).toBe(1);
+    expect(out.received[0] === err).toBe(true);
+  });
+});
```
