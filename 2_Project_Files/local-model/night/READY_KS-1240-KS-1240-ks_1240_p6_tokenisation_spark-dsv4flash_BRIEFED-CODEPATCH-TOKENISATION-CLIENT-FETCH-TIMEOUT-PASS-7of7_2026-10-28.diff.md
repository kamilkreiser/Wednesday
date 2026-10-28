# READY — KS-1240-KS-1240-ks_1240_p6_tokenisation (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts b/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts' vs '+++ --- a/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts): `error: patch failed: Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts:17` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	0	Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts
111	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 6 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts byte-exact incl. leading whitespace (apply mode fuzzy): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 6 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 6 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts:17`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts fails at the untouched tip (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1240: the gateway tokenisation client bounds its fetches RED KS-1240 R1 the tokenise fetch carries an AbortSignal', 'KS-1240: the gateway tokenisation client bounds its fetches RED KS-1240 R2 the detokenise fetch carries an AbortSignal', 'KS-1240: the gateway tokenisation client bounds its fetches RED KS-1240 R3 the two bounds handed to AbortSignal.timeout are positive and at most 30000 ms', 'KS-1240: the gateway tokenisation client bounds its fetches RED KS-1240 R4 a tokenisation service that never answers a tokenise call ends in the empty map, not a hang', 'KS-1240: the gateway tokenisation client bounds its fetches RED KS-1240 R5 a tokenisation service that never answers a detokenise call ends in the empty map, not a hang']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1255 failed=0 | after: total=1263 failed=0` · `NEW reds: []` [baseline_suite.json total=1255 failed=0; after_suite.json total=1263 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +117/-0 test=src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts red_first=yes apply_mode=fuzzy`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts` (+6/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts` (+111/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p6_tokenisation/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts b/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts
--- a/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts
@@ -17,2 +17,6 @@
 const PLATFORM_DB_URL = process.env.PLATFORM_DATABASE_URL || '';
 const TOKENISATION_URL = process.env.TOKENISATION_URL || 'http://tokenisation:4021';
+
+// KS-1240: the longest the gateway waits for the tokenisation service. Neither fetch below carried a timeout, so a service that accepted the connection and never answered held the caller for as long as
+// the socket lived. On expiry the fetch rejects and the existing catch in each function logs and answers the empty map, exactly as it already does for an unreachable service.
+const TOKENISATION_FETCH_TIMEOUT_MS = 10_000;
@@ -111,6 +115,7 @@
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ tenantId, key, fields }),
+      signal: AbortSignal.timeout(TOKENISATION_FETCH_TIMEOUT_MS),
     });
     const data = (await res.json()) as {
       success: boolean;
@@ -146,6 +151,7 @@
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ tenantId, key, tokens }),
+      signal: AbortSignal.timeout(TOKENISATION_FETCH_TIMEOUT_MS),
     });
     const data = (await res.json()) as {
       success: boolean;
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts
@@ -0,0 +1,111 @@
+// KS-1240 (class: hand-built outbound fetches with no timeout), api-gateway services/tokenisation.ts: tokeniseFields and detokeniseValues each fetched the tokenisation service with no `signal`, so a
+// service that accepted the connection and never answered held the caller for as long as the socket lived. Each function already catches a failed fetch, logs a warning and answers an empty map. The
+// functions are driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing touches the network. R1 and R2 pin that each fetch carries an
+// AbortSignal, R3 that the two bounds are sane positive numbers, R4 and R5 that a service that never answers ends in the empty map and not a hang; C1 to C3 pin the unchanged answers.
+import { describe, it, expect, afterEach, vi } from 'vitest';
+
+const silent = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn(), log: vi.fn() }));
+vi.mock('../utils/logger', () => ({ logger: silent, createLogger: () => silent }));
+
+import { tokeniseFields, detokeniseValues } from '../services/tokenisation';
+
+function reply(body: unknown): Response {
+  return { ok: true, status: 200, json: async () => body, text: async () => JSON.stringify(body) } as unknown as Response;
+}
+
+type Seen = { url: string; signal: unknown };
+
+/** Answers both endpoints and records the signal each call carried. */
+function stubAnswering(seen: Seen[]): void {
+  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
+    const u = String(url);
+    seen.push({ url: u, signal: init?.signal });
+    if (u.endsWith('/api/tokenise')) return reply({ success: true, fields: [{ name: 'email', token: 'tok-1' }] });
+    if (u.endsWith('/api/detokenise')) return reply({ success: true, values: [{ token: 'tok-1', value: 'a@x.test' }] });
+    return reply({ success: false });
+  }) as never);
+}
+
+/** Every call honours its signal; a call with NO signal never answers (the hang the fix removes). */
+function stubNeverAnswering(): void {
+  vi.spyOn(globalThis, 'fetch').mockImplementation(((_url: unknown, init?: { signal?: AbortSignal }) =>
+    new Promise<Response>((_resolve, reject) => {
+      const signal = init?.signal;
+      if (!signal) return;
+      if (signal.aborted) reject(new Error('aborted'));
+      else signal.addEventListener('abort', () => reject(new Error('aborted')));
+    })) as never);
+}
+
+afterEach(() => { vi.restoreAllMocks(); });
+
+/** 'EMPTY MAP' when the call resolves to an empty map, 'HUNG' when it is still pending after 300 ms, else the map's size, so a hang is a red assertion and not a stuck run. */
+async function outcome(run: () => Promise<Map<string, string>>): Promise<string> {
+  return Promise.race([
+    run().then((m) => (m.size === 0 ? 'EMPTY MAP' : 'SIZE ' + m.size), () => 'REJECTED'),
+    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
+  ]);
+}
+
+describe('KS-1240: the gateway tokenisation client bounds its fetches', () => {
+  it('RED KS-1240 R1 the tokenise fetch carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await tokeniseFields('t1', 'k1', [{ name: 'email', value: 'a@x.test' }]);
+    expect(seen).toHaveLength(1);
+    expect(seen[0].signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R2 the detokenise fetch carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await detokeniseValues('t1', 'k1', ['tok-1']);
+    expect(seen).toHaveLength(1);
+    expect(seen[0].signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R3 the two bounds handed to AbortSignal.timeout are positive and at most 30000 ms', async () => {
+    const timeout = vi.spyOn(AbortSignal, 'timeout');
+    stubAnswering([]);
+    await tokeniseFields('t1', 'k1', [{ name: 'email', value: 'a@x.test' }]);
+    await detokeniseValues('t1', 'k1', ['tok-1']);
+    const bounds = timeout.mock.calls.map((c) => c[0] as number);
+    expect(bounds).toHaveLength(2);
+    for (const ms of bounds) {
+      expect(ms).toBeGreaterThan(0);
+      expect(ms).toBeLessThanOrEqual(30000);
+    }
+  });
+
+  it('RED KS-1240 R4 a tokenisation service that never answers a tokenise call ends in the empty map, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => tokeniseFields('t1', 'k1', [{ name: 'email', value: 'a@x.test' }]))).toBe('EMPTY MAP');
+  });
+
+  it('RED KS-1240 R5 a tokenisation service that never answers a detokenise call ends in the empty map, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => detokeniseValues('t1', 'k1', ['tok-1']))).toBe('EMPTY MAP');
+  });
+
+  it('control KS-1240 C1 a healthy tokenise answer still fills the map', async () => {
+    stubAnswering([]);
+    const map = await tokeniseFields('t1', 'k1', [{ name: 'email', value: 'a@x.test' }]);
+    expect(map.get('email')).toBe('tok-1');
+  });
+
+  it('control KS-1240 C2 a healthy detokenise answer still fills the map', async () => {
+    stubAnswering([]);
+    const map = await detokeniseValues('t1', 'k1', ['tok-1']);
+    expect(map.get('tok-1')).toBe('a@x.test');
+  });
+
+  it('control KS-1240 C3 an unreachable service still answers the empty map, and an empty request makes no call at all', async () => {
+    const spy = vi.spyOn(globalThis, 'fetch').mockImplementation((async () => { throw new Error('connect ECONNREFUSED'); }) as never);
+    expect((await tokeniseFields('t1', 'k1', [{ name: 'email', value: 'a@x.test' }])).size).toBe(0);
+    spy.mockClear();
+    expect((await detokeniseValues('t1', 'k1', [])).size).toBe(0);
+    expect(spy).not.toHaveBeenCalled();
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief and vs api-gateway `services/tokenisation.ts` at base: the two fetches (`/api/tokenise` :110, `/api/detokenise` :145) are the only ones in the file; each gains a `signal:` line and one `TOKENISATION_FETCH_TIMEOUT_MS = 10_000` constant follows `TOKENISATION_URL`. Both already sit in a try/catch that logs and returns the empty map, so a timeout takes the existing path.
- DECISIONS for Wednesday: (1) 10 000 ms is the drafter's. (2) FINDING at source: `tokeniseFields` and `detokeniseValues` have NO callers at the tip (`git grep` over the tree finds them only in tokenisation.ts itself, no caller and no test; api-gateway/src/index.ts imports only setTenantKey, getTenantKey, removeTenantKey from this module). The patch is correct but bounds currently-unused code. Wednesday rules whether a PR for dead code is wanted at all, or whether it waits for a caller.
- Apply mode: NOT STRICT. Section 1 (tokenisation.ts) applied with `--recount --ignore-whitespace -C1` (checker apply_mode=fuzzy); section 2 (the test) strict. Whole-patch lenient `git apply --check` passes at develop bd6697e0, strict fails. STRICT APPLY NOT CLAIMED.
- SEQUENCE: no shared file with any other held pass; 0 overlaps with the 14 open PRs. Refs KS-1240; close-word only after the last KS-1240 slice and the owner's call.
- Verdict: HOLD-WITH-DECISION.
