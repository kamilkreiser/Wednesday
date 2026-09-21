# READY — KS-1179-F1-R15 (Ornith, briefed, test_only, new · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1179-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 21:35 2026-09-21). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.

**Held 21:35 2026-09-21 by Wednesday (the 20:1x seat) after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1179-ornith35b-night/out.md.checker`, not typed).** Tip `9f0265eb06ecf24d4de18149ce862ad2330a61ee`. Touches ONE file: `Blockchain/Dev/packages/shared/src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts` (new). `+` lines 98 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 7/7 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F1` → red exactly ['RED KS-1179 1 - a name answering 10.0.0.5 is blocked and nev', 'RED KS-1179 2 - a name answering the metadata address is blo', 'RED KS-1179 3 - a name answering IPv6 loopback is blocked an', 'RED KS-1179 4 - a public answer FIRST and a private answer S']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1179-ornith35b-night/input.json`. Brief: `night/briefs/KS-1179-F1-R15.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1179-ornith35b-night/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts
@@ -0,0 +1,98 @@
+/**
+ * KS-1179 (KS-932 gate F-1) - safeOutboundRequest classifies every DNS answer
+ * before anything reaches the transport.
+ *
+ * `dns/promises` is mocked, and `https.request` is replaced by a counter that
+ * throws, so no cell opens a socket and no cell depends on a real address
+ * hanging (the KS-932 gate's F-2 lesson). The red cells pin the DNS-layer
+ * classification on the SHIPPED function: if the raced lookup ever resolves
+ * without classifying, a private answer reaches `https.request` and they red.
+ */
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+const { dnsMock, transportMock } = vi.hoisted(() => ({
+  dnsMock: vi.fn(),
+  transportMock: vi.fn((_options: any): never => {
+    throw new Error('KS-1179 transport seam: no socket is opened');
+  }),
+}));
+vi.mock('dns/promises', () => ({ lookup: dnsMock }));
+vi.mock('https', async (importOriginal) => {
+  const actual = await importOriginal<typeof import('https')>();
+  return { ...actual, default: actual, request: transportMock };
+});
+
+import { safeOutboundRequest } from '../security/ssrf-guard';
+
+const EXPECTED_CELLS = 6;
+let CELLS_RUN = 0;
+const TIMEOUT_MS = 1000;
+const SEAM_ERROR = 'KS-1179 transport seam: no socket is opened';
+const PUBLIC_V4 = '203.0.113.7';
+let answered: unknown = null;
+
+beforeEach(() => {
+  dnsMock.mockReset();
+  transportMock.mockClear();
+});
+
+describe('KS-1179 - safeOutboundRequest refuses a private DNS answer before the transport', () => {
+  it('RED KS-1179 1 - a name answering 10.0.0.5 is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '10.0.0.5', family: 4 }]);
+    const result = await safeOutboundRequest('https://rebind.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(dnsMock).toHaveBeenCalledTimes(1);
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 10.0.0.5, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-1179 2 - a name answering the metadata address is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '169.254.169.254', family: 4 }]);
+    const result = await safeOutboundRequest('https://imds.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 169.254.169.254, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-1179 3 - a name answering IPv6 loopback is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '::1', family: 6 }]);
+    const result = await safeOutboundRequest('https://loop6.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to ::1, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('RED KS-1179 4 - a public answer FIRST and a private answer SECOND is still blocked', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: PUBLIC_V4, family: 4 }, { address: '10.0.0.5', family: 4 }]);
+    const result = await safeOutboundRequest('https://mixed.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(dnsMock).toHaveBeenCalledTimes(1);
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 10.0.0.5, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('GREEN KS-1179 5 CONTROL - a public answer reaches https.request once, pinned to the classified address', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: PUBLIC_V4, family: 4 }]);
+    const result = await safeOutboundRequest('https://public.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(dnsMock).toHaveBeenCalledWith('public.example.com', { all: true, verbatim: true });
+    expect(transportMock).toHaveBeenCalledTimes(1);
+    expect(result).toMatchObject({ ok: false, reason: 'request_failed', error: SEAM_ERROR });
+    transportMock.mock.calls[0][0].agent.options.lookup('elsewhere.invalid', {}, (_e: unknown, addr: unknown) => {
+      answered = addr;
+    });
+    expect(answered).toBe(PUBLIC_V4);
+  });
+
+  it('GREEN KS-1179 6 CONTROL - an IP-literal private URL is refused by the literal layer, before any lookup', async () => {
+    CELLS_RUN += 1;
+    const result = await safeOutboundRequest('https://10.0.0.5/x', { timeoutMs: TIMEOUT_MS });
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('url host 10.0.0.5 is forbidden') });
+    expect(dnsMock).not.toHaveBeenCalled();
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('COMPLETENESS: every graded cell above actually ran', () => {
+    expect(CELLS_RUN).toBe(EXPECTED_CELLS);
+  });
+});
```
