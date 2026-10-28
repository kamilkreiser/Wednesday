# READY — KS-1240-KS-1240-ks_1240_p8_provisioning (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts b/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts' vs '+++ --- a/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts' vs '+++ --- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [section 3: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts): `error: patch failed: Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts:16` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts , Blockchain/Dev/services/tenant-provisioning/src/index.ts } + { Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts` (product) and `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts
5	0	Blockchain/Dev/services/tenant-provisioning/src/index.ts
94	0	Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: meteringKey.ts index.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts`, `Blockchain/Dev/services/tenant-provisioning/src/index.ts`; test(s): `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tenant-provisioning/src/index.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts 94 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts:16`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1240: tenant provisioning bounds its outbound fetches RED KS-1240 R1 the metering-key fetch carries an AbortSignal', 'KS-1240: tenant provisioning bounds its outbound fetches RED KS-1240 R2 the bound handed to AbortSignal.timeout is positive and at most 30000 ms', 'KS-1240: tenant provisioning bounds its outbound fetches RED KS-1240 R3 a security service that never answers ends in a rejection, not a hang', 'KS-1240: tenant provisioning bounds its outbound fetches RED KS-1240 R4 the generate-key fetch in index.ts carries a timeout signal', 'KS-1240: tenant provisioning bounds its outbound fetches RED KS-1240 R5 index.ts declares the generate-key bound as a positive number of at most 30000 ms']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=21 failed=0 | after: total=29 failed=0` · `NEW reds: []` [baseline_suite.json total=21 failed=0; after_suite.json total=29 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tenant-provisioning suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tenant-provisioning: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts` (+94/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts, Blockchain/Dev/services/tenant-provisioning/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p8_provisioning/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts b/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts
@@ -16,3 +16,7 @@
   /** The internal `key_…` record id, for later revoke / lookup. */
   id: string;
 }
+
+// KS-1240 (class): the longest provisioning waits for the security service to mint the metering key. The fetch carried no timeout, so a security service that accepted the connection and never answered
+// held the tenant-creation request for as long as the socket lived. On expiry the fetch rejects, requestMeteringKey throws, and the provisioning handler fails soft as it already does for a non-2xx.
+const METERING_KEY_FETCH_TIMEOUT_MS = 10_000;
@@ -55,6 +59,7 @@
       scopes: ['metering:read'],
       connectorId: 'platform-s',
     }),
+    signal: AbortSignal.timeout(METERING_KEY_FETCH_TIMEOUT_MS),
   });
   // Non-2xx → throw so the provisioning handler can fail soft (tenant already active).
   if (!res.ok) {
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/index.ts b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
--- a/Blockchain/Dev/services/tenant-provisioning/src/index.ts
+++ b/Blockchain/Dev/services/tenant-provisioning/src/index.ts
@@ -37,4 +37,8 @@
 const TOKENISATION_URL = process.env.TOKENISATION_URL || 'http://tokenisation:4021';
+
+// KS-1240 (class): the longest provisioning waits for the tokenisation service to generate a tenant key. The fetch carried no timeout, so a tokenisation service that accepted the connection and never
+// answered held the tenant-creation request for as long as the socket lived. On expiry the fetch rejects out of requestKeyGeneration to the handler's existing error path.
+const KEY_GENERATION_FETCH_TIMEOUT_MS = 10_000;
 // KS-336: the security service owns connector API keys (svc_api_keys, in the app
 // DB — a different DB from the platform tables this service writes). We mint the
 // per-tenant metering key over HTTP, not via platformQuery. Default matches the
@@ -135,6 +139,7 @@
       ...(authHeader ? { Authorization: authHeader } : {}),
     },
     body: JSON.stringify({ tenantId, tenantSlug }),
+    signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),
   });
   return res.json() as Promise<{
     success: boolean;
diff --git a/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts
@@ -0,0 +1,94 @@
+// KS-1240 (class: hand-built outbound fetches with no timeout), tenant-provisioning meteringKey.ts and index.ts: the metering-key mint (requestMeteringKey, exported) and the tenant key generation
+// (requestKeyGeneration, private to index.ts, which boots a server and so is read as TEXT here) fetched the security and tokenisation services with no `signal`, so a service that accepted the connection
+// and never answered held the tenant-creation request for as long as the socket lived. requestMeteringKey is driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there
+// is none). R1 pins that its fetch carries an AbortSignal, R2 that the bound is sane, R3 that a silent security service ends in a rejection and not a hang, R4 and R5 that index.ts bounds its fetch;
+// C1 to C3 pin the unchanged answers.
+import { describe, it, expect, vi, afterEach } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { fileURLToPath } from 'node:url';
+import { requestMeteringKey } from '../meteringKey.js';
+
+const SEC = 'http://security:4004';
+const INDEX_SRC = readFileSync(fileURLToPath(new URL('../index.ts', import.meta.url)), 'utf8');
+
+afterEach(() => { vi.restoreAllMocks(); vi.unstubAllGlobals(); });
+
+/** The key the security service mints, as a Response-like object. */
+function mintedKey(): Response {
+  return { ok: true, status: 201, json: async () => ({ success: true, data: { id: 'key_abc', key: 'sk_deadbeef', prefix: 'sk_deadbeef0' } }) } as unknown as Response;
+}
+
+/** Answers the mint and records the signal the call carried. */
+function stubAnswering(seen: unknown[]): void {
+  vi.stubGlobal('fetch', vi.fn(async (_url: unknown, init?: { signal?: unknown }) => { seen.push(init?.signal); return mintedKey(); }));
+}
+
+/** Every call honours its signal; a call with NO signal never answers (the hang the fix removes). */
+function stubNeverAnswering(): void {
+  vi.stubGlobal('fetch', vi.fn((_url: unknown, init?: { signal?: AbortSignal }) =>
+    new Promise<Response>((_resolve, reject) => {
+      const signal = init?.signal;
+      if (!signal) return;
+      if (signal.aborted) reject(new Error('aborted'));
+      else signal.addEventListener('abort', () => reject(new Error('aborted')));
+    })));
+}
+
+/** 'REJECTED' when the call rejects, 'RESOLVED' when it resolves, 'HUNG' when it is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
+async function outcome(run: () => Promise<unknown>): Promise<string> {
+  return Promise.race([
+    run().then(() => 'RESOLVED', () => 'REJECTED'),
+    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
+  ]);
+}
+
+describe('KS-1240: tenant provisioning bounds its outbound fetches', () => {
+  it('RED KS-1240 R1 the metering-key fetch carries an AbortSignal', async () => {
+    const seen: unknown[] = [];
+    stubAnswering(seen);
+    await requestMeteringKey(SEC, 'tenant-123', 'acme', 'Bearer admintoken');
+    expect(seen).toHaveLength(1);
+    expect(seen[0]).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R2 the bound handed to AbortSignal.timeout is positive and at most 30000 ms', async () => {
+    const timeout = vi.spyOn(AbortSignal, 'timeout');
+    stubAnswering([]);
+    await requestMeteringKey(SEC, 'tenant-123', 'acme');
+    const bounds = timeout.mock.calls.map((c) => c[0] as number);
+    expect(bounds).toHaveLength(1);
+    expect(bounds[0]).toBeGreaterThan(0);
+    expect(bounds[0]).toBeLessThanOrEqual(30000);
+  });
+
+  it('RED KS-1240 R3 a security service that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => requestMeteringKey(SEC, 'tenant-123', 'acme'))).toBe('REJECTED');
+  });
+
+  it('RED KS-1240 R4 the generate-key fetch in index.ts carries a timeout signal', () => {
+    expect(INDEX_SRC).toContain('signal: AbortSignal.timeout(KEY_GENERATION_FETCH_TIMEOUT_MS),');
+  });
+
+  it('RED KS-1240 R5 index.ts declares the generate-key bound as a positive number of at most 30000 ms', () => {
+    const match = /const KEY_GENERATION_FETCH_TIMEOUT_MS = ([0-9_]+);/.exec(INDEX_SRC);
+    const ms = match ? Number(match[1].replace(/_/g, '')) : NaN;
+    expect(ms).toBeGreaterThan(0);
+    expect(ms).toBeLessThanOrEqual(30000);
+  });
+
+  it('control KS-1240 C1 a healthy mint still returns the key material', async () => {
+    stubAnswering([]);
+    expect(await requestMeteringKey(SEC, 'tenant-123', 'acme')).toEqual({ key: 'sk_deadbeef', prefix: 'sk_deadbeef0', id: 'key_abc' });
+  });
+
+  it('control KS-1240 C2 a non-2xx answer still throws with the status in the message', async () => {
+    vi.stubGlobal('fetch', vi.fn(async () => ({ ok: false, status: 403, json: async () => ({}) })));
+    await expect(requestMeteringKey(SEC, 't', 's')).rejects.toThrow('403');
+  });
+
+  it('control KS-1240 C3 index.ts still sends the generate-key request to the tokenisation service', () => {
+    expect(INDEX_SRC).toContain('${TOKENISATION_URL}/api/generate-key');
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief and vs tenant-provisioning `src/meteringKey.ts` (:45) and `src/index.ts` (:131) at base: each file's one fetch gains a `signal:` line and a 10_000 ms constant. The new test mixes behaviour (meteringKey, stubbed fetch) and source text (index.ts boots a server).
- DECISIONS for Wednesday: (1) both 10 000 ms bounds are the drafter's. (2) FINDING at source: `requestKeyGeneration` is called inside a try whose catch only logs (index.ts:262-269), so a key-generation timeout does NOT fail tenant creation: the tenant is inserted with `vault_key_hash` NULL and the handler answers 201 `success: true` with `keyFile: null` ('will need manual generation'). Before, a hung tokenisation service hung the request; now it silently yields a key-less tenant after 10 s. The metering-key mint (:295) is documented fail-soft the same way. The brief said the handler's error path was 'not read here'; it is read now. Wednesday rules whether a key-less active tenant on timeout is acceptable.
- Apply mode: NOT STRICT. Section 1 (meteringKey.ts) applied with `--recount --ignore-whitespace -C1`; sections 2 (index.ts) and 3 (test) strict; whole-patch strict `git apply --check` fails, lenient passes at develop bd6697e0. STRICT APPLY NOT CLAIMED.
- SEQUENCE: no shared file with any other held pass; 0 overlaps with the 14 open PRs. Scope extension beyond the gateway ticket (owner confirms).
- Verdict: HOLD-WITH-DECISION.
