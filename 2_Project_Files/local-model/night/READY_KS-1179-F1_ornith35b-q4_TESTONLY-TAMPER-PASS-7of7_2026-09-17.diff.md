# READY — KS-1179 F-1 ONLY (TEST-ONLY, tamper-graded: safeOutboundRequest refuses a private DNS answer before the transport — the KS-932 gate's TG tamper) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (00:51). Held by Wednesday at 01:17 AEST. Run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-17_ks1179-ornith35b-night
# Source read by me (Wednesday): ONE new file ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts (--- /dev/null); product untouched; the model's 98 `+` lines are BYTE-IDENTICAL to the brief's fenced block (python line compare, 0 mismatches); apply strict (no repair); A4 4 red by assertion under TG with both controls + completeness green; A6 whole packages/shared 849/849, NEW reds []; A7 tsc rc 0. Cells: 🔴1 10.0.0.5 · 🔴2 169.254.169.254 · 🔴3 ::1 · 🔴4 public-first-then-private · 🟢5 public reaches https.request once, pinned · 🟢6 IP-literal refused before lookup · COMPLETENESS.
# PR NOTES: "Refs KS-1179 (F-1)" — NEVER Closes: F-2/F-3 (edits to ks932-timeout-bounds-dns.test.ts), F-4/F-5 (ssrf-guard.ts docblock/error text) and F-6 (a PRODUCT change: clear the DNS timer in a finally) stay open. packages/shared is Seat A's partition — raise it through that seat. Do not rename the mocks (dnsMock/transportMock): the checker's decl_splice mis-reads destructured declarations (IMPROVEMENTS row stamped 2026-09-17 00:42).

```diff
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts
@@ -0,0 +1,98 @@
+/**
+ * KS-1179 (KS-932 gate F-1) — safeOutboundRequest classifies every DNS answer
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
+describe('KS-1179 — safeOutboundRequest refuses a private DNS answer before the transport', () => {
+  it('🔴 KS-1179 1 — a name answering 10.0.0.5 is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '10.0.0.5', family: 4 }]);
+    const result = await safeOutboundRequest('https://rebind.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(dnsMock).toHaveBeenCalledTimes(1);
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 10.0.0.5, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('🔴 KS-1179 2 — a name answering the metadata address is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '169.254.169.254', family: 4 }]);
+    const result = await safeOutboundRequest('https://imds.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 169.254.169.254, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('🔴 KS-1179 3 — a name answering IPv6 loopback is blocked and never reaches https.request', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: '::1', family: 6 }]);
+    const result = await safeOutboundRequest('https://loop6.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to ::1, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('🔴 KS-1179 4 — a public answer FIRST and a private answer SECOND is still blocked', async () => {
+    CELLS_RUN += 1;
+    dnsMock.mockResolvedValue([{ address: PUBLIC_V4, family: 4 }, { address: '10.0.0.5', family: 4 }]);
+    const result = await safeOutboundRequest('https://mixed.example.com/x', { timeoutMs: TIMEOUT_MS });
+    expect(dnsMock).toHaveBeenCalledTimes(1);
+    expect(result).toMatchObject({ ok: false, reason: 'blocked', error: expect.stringContaining('resolves to 10.0.0.5, which is forbidden') });
+    expect(transportMock).not.toHaveBeenCalled();
+  });
+
+  it('🟢 KS-1179 5 CONTROL — a public answer reaches https.request once, pinned to the classified address', async () => {
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
+  it('🟢 KS-1179 6 CONTROL — an IP-literal private URL is refused by the literal layer, before any lookup', async () => {
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
