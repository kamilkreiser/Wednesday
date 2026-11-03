# READY — KS-1868-KS-1868-O97-P6 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 17:31 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:31 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
71	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: ssrf-guard.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts 71 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 resolvePublicAddresses reads a lookup failure safely RED ks1868 R1 a revoked Proxy is refused with a constant reason', 'KS-1868 resolvePublicAddresses reads a lookup failure safely RED ks1868 R2 an Error whose message getter throws is refused with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1447 failed=1 | after: total=1451 failed=1` · `NEW reds: []` [baseline_suite.json total=1447 failed=1; after_suite.json total=1451 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts` (+71/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p6_shared_ssrf_guard_resolve_public_addresses_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts b/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
--- a/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
+++ b/Blockchain/Dev/packages/shared/src/security/ssrf-guard.ts
@@ -322,8 +322,14 @@
   try {
     addresses = await lookup(bare, { all: true, verbatim: true });
   } catch (err) {
+    let reason: string;
+    try {
+      reason = (err as Error).message;
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     return {
       ok: false,
-      error: `host "${bare}" could not be resolved (${(err as Error).message}) — refusing to contact an unverifiable destination`,
+      error: `host "${bare}" could not be resolved (${reason}) — refusing to contact an unverifiable destination`,
     };
   }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts
@@ -0,0 +1,71 @@
+import { describe, it, expect, vi } from 'vitest';
+
+// KS-1868: resolvePublicAddresses (src/security/ssrf-guard.ts) resolves a host and refuses it when the lookup fails: its catch
+// returns `{ ok: false, error: 'host "<h>" could not be resolved (${(err as Error).message}) - refusing to contact ...' }`.
+// The `.message` read is unguarded. When the value cannot be read (a revoked Proxy throws on any property read; an Error
+// whose `message` getter throws) the catch itself throws, so the call REJECTS instead of returning the refusal. The DNS
+// module is a plain stand-in whose lookup rejects with the cell's value; no network.
+const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
+
+vi.mock('dns/promises', () => ({
+  lookup: () => Promise.reject(h.toThrow),
+}));
+
+import { resolvePublicAddresses } from '../security/ssrf-guard';
+
+type Outcome = { rejected: boolean; result: { ok: boolean; error?: string } | undefined };
+
+async function run(value: unknown): Promise<Outcome> {
+  h.toThrow = value;
+  try {
+    const result = await resolvePublicAddresses('ks1868.example.test');
+    return { rejected: false, result };
+  } catch {
+    return { rejected: true, result: undefined };
+  }
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 resolvePublicAddresses reads a lookup failure safely', () => {
+  it('control ks1868 C1 an ordinary Error is refused with its message in the reason', async () => {
+    const out = await run(new Error('ENOTFOUND boom'));
+    expect(out.rejected).toBe(false);
+    expect(out.result?.ok).toBe(false);
+    expect(out.result?.error).toContain('host "ks1868.example.test" could not be resolved (ENOTFOUND boom)');
+  });
+
+  it('control ks1868 C2 a thrown plain string is refused with an undefined message in the reason', async () => {
+    const out = await run('plain text failure');
+    expect(out.rejected).toBe(false);
+    expect(out.result?.ok).toBe(false);
+    expect(out.result?.error).toContain('host "ks1868.example.test" could not be resolved (undefined)');
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is refused with a constant reason', async () => {
+    const out = await run(revokedProxy());
+    expect(out.rejected).toBe(false);
+    expect(out.result?.ok).toBe(false);
+    expect(out.result?.error).toContain('host "ks1868.example.test" could not be resolved (unreadable thrown value)');
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is refused with a constant reason', async () => {
+    const out = await run(getterThrows());
+    expect(out.rejected).toBe(false);
+    expect(out.result?.ok).toBe(false);
+    expect(out.result?.error).toContain('host "ks1868.example.test" could not be resolved (unreadable thrown value)');
+  });
+});
```
