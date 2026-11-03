# READY — KS-1868-KS-1868-O94-P4 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/out.md.checker/patch.diff`** (from `ls` at 12:20 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts b/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts' vs '+++ --- a/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts): `error: patch failed: Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts:226` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 12:20 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `df0d1f8e4be5827b4ff7c156d599d0bd2c418ee6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
20	3	Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts
84	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (20 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: reanchorInFlight.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts 20 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts 84 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts:226`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1868 reanchorInFlight reads the rejection value safely RED ks1868 R1 isTimeoutError is false for a revoked Proxy', 'KS-1868 reanchorInFlight reads the rejection value safely RED ks1868 R2 a revoked Proxy rejection still reads as unavailable with a constant reason', 'KS-1868 reanchorInFlight reads the rejection value safely RED ks1868 R3 an Error whose message getter throws still reads as unavailable with a constant reason', 'KS-1868 reanchorInFlight reads the rejection value safely RED ks1868 R4 a revoked Proxy rejection still gives a failed POST outcome with a constant reason', 'KS-1868 reanchorInFlight reads the rejection value safely RED ks1868 R5 an Error whose message getter throws still gives a failed POST outcome with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2380 failed=11 | after: total=2398 failed=11` · `NEW reds: []` [baseline_suite.json total=2380 failed=11; after_suite.json total=2398 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts` (+20/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts` (+84/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `df0d1f8e4be5827b4ff7c156d599d0bd2c418ee6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p4_originate_reanchor_in_flight_rejection_reads_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts b/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts
--- a/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts
+++ b/Blockchain/Dev/services/originate/src/services/reanchorInFlight.ts
@@ -51,5 +51,10 @@
 /** True for the rejection a fetch gives when its AbortSignal.timeout fires (a DOMException named TimeoutError, or AbortError). */
 export function isTimeoutError(err: unknown): boolean {
-  const name = (err as { name?: unknown } | null)?.name;
+  let name: unknown;
+  try {
+    name = (err as { name?: unknown } | null)?.name;
+  } catch {
+    return false;
+  }
   return name === 'TimeoutError' || name === 'AbortError';
 }
@@ -190,7 +195,13 @@
     try { body = await resp.json(); } catch { body = undefined; }
     answer = { httpStatus: resp.status, body };
   } catch (err: unknown) {
-    answer = { httpStatus: null, fetchError: err instanceof Error ? err.message : String(err) };
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    answer = { httpStatus: null, fetchError: reason };
   }
   return decideInFlight(answer, ctx);
 }
@@ -226,4 +237,10 @@
     timers.fired = phase;
     abort.abort(new DOMException(`no ${phase} within ${ms} ms`, 'TimeoutError'));
   }, ms);
-  const message = (err: unknown) => (err instanceof Error ? err.message : String(err));
+  const message = (err: unknown): string => {
+    try {
+      return err instanceof Error ? err.message : String(err);
+    } catch {
+      return 'unreadable thrown value';
+    }
+  };
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts
@@ -0,0 +1,84 @@
+// KS-1868: src/services/reanchorInFlight.ts reads the value a fetch rejected with in three places, all unguarded: `isTimeoutError` reads
+// `.name`, the catch of `readInFlightAnchor` reads `err instanceof Error ? err.message : String(err)`, and the `message` helper of
+// `postReanchor` reads the same. A value whose read throws (a revoked Proxy; an Error whose `message` getter throws) made each of them throw, so the
+// retry route's fail-safe answers ('unavailable' for the read, 'failed' for the POST) never came back and the call REJECTED.
+// The fetch stand-ins are plain functions, not jest.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy first.
+import { isTimeoutError, readInFlightAnchor, postReanchor } from '../services/reanchorInFlight';
+
+function revokedProxy(): unknown {
+  const p = Proxy.revocable({}, {});
+  p.revoke();
+  return p.proxy;
+}
+
+function throwingMessageError(): unknown {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+}
+
+const ctx = {
+  tokenTenantId: '11111111-2222-4333-8444-555555555555',
+  documentTenantId: '11111111-2222-4333-8444-555555555555',
+  blobAnchorId: undefined,
+  documentContentHash: 'sha256:' + 'a'.repeat(64),
+  network: 'preprod',
+};
+
+/** The settled value of f, or the string 'rejected' when it throws or rejects (an assertion can then fail on it). */
+async function settle<T>(f: () => T | Promise<T>): Promise<T | 'rejected'> {
+  try {
+    return await f();
+  } catch {
+    return 'rejected';
+  }
+}
+
+const rejecting = (value: unknown): typeof fetch => ((..._args: unknown[]) => Promise.reject(value)) as unknown as typeof fetch;
+
+describe('KS-1868 reanchorInFlight reads the rejection value safely', () => {
+  it('control ks1868 C1 isTimeoutError is true for a TimeoutError and false for an ordinary Error', () => {
+    const t = new Error('slow');
+    t.name = 'TimeoutError';
+    expect(isTimeoutError(t)).toBe(true);
+    expect(isTimeoutError(new Error('boom'))).toBe(false);
+  });
+
+  it('control ks1868 C2 an ordinary Error still reads as unavailable with its message', async () => {
+    const d = await settle(() => readInFlightAnchor(rejecting(new Error('connection reset')), 'http://a.test', '', 'doc-1', ctx));
+    expect(d).toEqual({ kind: 'unavailable', reason: 'the anchoring service could not be read: connection reset' });
+  });
+
+  it('control ks1868 C3 an ordinary Error still gives a failed POST outcome with its message', async () => {
+    const o = await settle(() => postReanchor(rejecting(new Error('connection reset')), 'http://a.test/x', { method: 'POST' }));
+    expect(o).toEqual({ kind: 'failed', error: 'connection reset' });
+  });
+
+  it('RED ks1868 R1 isTimeoutError is false for a revoked Proxy', async () => {
+    expect(await settle(() => isTimeoutError(revokedProxy()))).toBe(false);
+  });
+
+  it('RED ks1868 R2 a revoked Proxy rejection still reads as unavailable with a constant reason', async () => {
+    const d = await settle(() => readInFlightAnchor(rejecting(revokedProxy()), 'http://a.test', '', 'doc-1', ctx));
+    expect(d).toEqual({ kind: 'unavailable', reason: 'the anchoring service could not be read: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 an Error whose message getter throws still reads as unavailable with a constant reason', async () => {
+    const d = await settle(() => readInFlightAnchor(rejecting(throwingMessageError()), 'http://a.test', '', 'doc-1', ctx));
+    expect(d).toEqual({ kind: 'unavailable', reason: 'the anchoring service could not be read: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 a revoked Proxy rejection still gives a failed POST outcome with a constant reason', async () => {
+    const o = await settle(() => postReanchor(rejecting(revokedProxy()), 'http://a.test/x', { method: 'POST' }));
+    expect(o).toEqual({ kind: 'failed', error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R5 an Error whose message getter throws still gives a failed POST outcome with a constant reason', async () => {
+    const o = await settle(() => postReanchor(rejecting(throwingMessageError()), 'http://a.test/x', { method: 'POST' }));
+    expect(o).toEqual({ kind: 'failed', error: 'unreadable thrown value' });
+  });
+});
```
