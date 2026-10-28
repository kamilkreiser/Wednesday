# READY — KS-1240-KS-1240-ks_1240_p7_ipfs (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts , Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	1	Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
154	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (13 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 14 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts byte-exact incl. leading whitespace (apply mode strict): OK 13 line(s) byte-exact incl. leading whitespace (of 13; 14 line(s) added by the apply)` [a3i_indent.out: `OK 13 line(s) byte-exact incl. leading whitespace (of 13; 14 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (hunks=9, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts fails at the untouched tip (8 failed / 11 run; controls green; assertion reds)` [red_first.json: failed=8 of total=11; red cell(s): ['KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R1 every pinata fetch (upload, pin, unpin) carries an AbortSignal', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R2 every infura fetch (upload, pin, unpin) carries an AbortSignal', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R3 the web3.storage upload fetch carries an AbortSignal', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R4 the gateway read in IPFSService.fetch carries an AbortSignal', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R5 the eight bounds handed to AbortSignal.timeout are positive and at most 120000 ms', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R6 a pinata upload endpoint that never answers ends in the failure answer, not a hang', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R7 a pinata pin endpoint that never answers ends in false, not a hang', 'KS-1240: the IPFS service bounds its outbound fetches RED KS-1240 R8 a gateway that never answers a read ends in the 503, not a hang']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts passes with the product hunk (11 passed / 11 run)` [green_after.json: failed=0 of total=11, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=61 failed=0 | after: total=72 failed=0` · `NEW reds: []` [baseline_suite.json total=61 failed=0; after_suite.json total=72 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +168/-1 test=src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (+14/-1 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts` (+154/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p7_ipfs/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
--- a/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
@@ -13,3 +13,9 @@
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an IPFS provider or gateway that accepts the connection and never answers holds the caller for as long as the
+// socket lives. On expiry the fetch rejects and the existing handling answers as it already does for an unreachable service (upload: success false; pin and unpin: false; gateway read: a 503).
+const IPFS_UPLOAD_TIMEOUT_MS = 60_000;
+const IPFS_PIN_TIMEOUT_MS = 15_000;
+const IPFS_GATEWAY_READ_TIMEOUT_MS = 30_000;
+
 // =============================================================================
 // IPFS PROVIDER INTERFACE
 // =============================================================================
@@ -74,4 +80,5 @@
           pinata_secret_api_key: this.secretKey,
         },
         body: formData,
+        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
       });
@@ -110,4 +117,5 @@
           pinata_secret_api_key: this.secretKey,
         },
         body: JSON.stringify({ hashToPin: cid }),
+        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
       });
@@ -126,4 +134,5 @@
           pinata_api_key: this.apiKey,
           pinata_secret_api_key: this.secretKey,
         },
+        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
       });
@@ -169,4 +178,5 @@
           Authorization: `Basic ${auth}`,
         },
         body: formData,
+        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
       });
@@ -195,6 +205,7 @@
       const response = await fetch(`https://ipfs.infura.io:5001/api/v0/pin/add?arg=${cid}`, {
         method: 'POST',
         headers: { Authorization: `Basic ${auth}` },
+        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
       });
       return response.ok;
     } catch {
@@ -208,6 +219,7 @@
       const response = await fetch(`https://ipfs.infura.io:5001/api/v0/pin/rm?arg=${cid}`, {
         method: 'POST',
         headers: { Authorization: `Basic ${auth}` },
+        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
       });
       return response.ok;
     } catch {
@@ -243,4 +255,5 @@
           'X-Name': filename,
         },
         body: blob,
+        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
       });
@@ -460,7 +473,7 @@
     const url = this.getGatewayUrl(cid);
     let response: Awaited<ReturnType<typeof fetch>>;
     try {
-      response = await fetch(url);
+      response = await fetch(url, { signal: AbortSignal.timeout(IPFS_GATEWAY_READ_TIMEOUT_MS) });
     } catch (error) {
       // DNS / connection failure — the IPFS gateway is unreachable.
       logger.warn('IPFS gateway unreachable', {
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts
@@ -0,0 +1,154 @@
+// KS-1240 (class: hand-built outbound fetches with no timeout), nft-certificate services/ipfs.service.ts: the Pinata, Infura and Web3.Storage providers (upload, pin, unpin: seven fetches) and the gateway
+// read in IPFSService.fetch (one more) passed no `signal`, so an IPFS endpoint that accepts the connection and never answers held the caller for as long as the socket lived. Each already has handling for
+// a failed fetch (upload answers success false, pin and unpin answer false, the gateway read throws a 503). The service is driven through its public methods with a stubbed global fetch that honours
+// `init.signal` (and never answers when there is none); nothing touches the network. R1 to R4 pin that every fetch carries an AbortSignal, R5 that the eight bounds are sane, R6 to R8 that a silent endpoint
+// ends in the existing failure answer and not a hang; C1 to C3 pin the unchanged answers.
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import { IPFSService } from '../services/ipfs.service';
+
+const KEYS = { apiKey: 'key-ks1240', secretKey: 'secret-ks1240' };
+const REQUEST = { data: Buffer.from('abc'), filename: 'a.txt', mimeType: 'text/plain', encrypted: false };
+
+function reply(body: unknown): Response {
+  return {
+    ok: true,
+    status: 200,
+    json: async () => body,
+    text: async () => JSON.stringify(body),
+    arrayBuffer: async () => new ArrayBuffer(3),
+  } as unknown as Response;
+}
+
+type Seen = { url: string; signal: unknown };
+
+/** Answers every endpoint and records the signal each call carried. */
+function stubAnswering(seen: Seen[]): void {
+  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
+    const u = String(url);
+    seen.push({ url: u, signal: init?.signal });
+    if (u.includes('pinFileToIPFS')) return reply({ IpfsHash: 'QmPinata', PinSize: 3 });
+    if (u.includes('/api/v0/add')) return reply({ Hash: 'QmInfura', Size: '3' });
+    if (u.includes('api.web3.storage/upload')) return reply({ cid: 'bafyW3' });
+    return reply({});
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
+/** The settled value rendered as text, or 'HUNG' when the call is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
+async function outcome(run: () => Promise<unknown>): Promise<string> {
+  return Promise.race([
+    run().then((v) => 'VALUE ' + JSON.stringify(v, (_k, x) => (typeof x === 'string' && x.length > 60 ? x.slice(0, 60) : x)), (e: any) => 'THREW ' + (e?.statusCode ?? e?.message)),
+    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
+  ]);
+}
+
+describe('KS-1240: the IPFS service bounds its outbound fetches', () => {
+  it('RED KS-1240 R1 every pinata fetch (upload, pin, unpin) carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    const svc = new IPFSService('pinata', KEYS);
+    await svc.upload(REQUEST);
+    await svc.pin('QmX');
+    await svc.unpin('QmX');
+    expect(seen).toHaveLength(3);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R2 every infura fetch (upload, pin, unpin) carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    const svc = new IPFSService('infura', KEYS);
+    await svc.upload(REQUEST);
+    await svc.pin('QmX');
+    await svc.unpin('QmX');
+    expect(seen).toHaveLength(3);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R3 the web3.storage upload fetch carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new IPFSService('web3storage', { apiKey: 'token-ks1240' }).upload(REQUEST);
+    expect(seen).toHaveLength(1);
+    expect(seen[0].signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R4 the gateway read in IPFSService.fetch carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new IPFSService('pinata', KEYS).fetch('QmX');
+    expect(seen).toHaveLength(1);
+    expect(seen[0].signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R5 the eight bounds handed to AbortSignal.timeout are positive and at most 120000 ms', async () => {
+    const timeout = vi.spyOn(AbortSignal, 'timeout');
+    stubAnswering([]);
+    const pinata = new IPFSService('pinata', KEYS);
+    await pinata.upload(REQUEST);
+    await pinata.pin('QmX');
+    await pinata.unpin('QmX');
+    await pinata.fetch('QmX');
+    const infura = new IPFSService('infura', KEYS);
+    await infura.upload(REQUEST);
+    await infura.pin('QmX');
+    await infura.unpin('QmX');
+    await new IPFSService('web3storage', { apiKey: 'token-ks1240' }).upload(REQUEST);
+    const bounds = timeout.mock.calls.map((c) => c[0] as number);
+    expect(bounds).toHaveLength(8);
+    for (const ms of bounds) {
+      expect(ms).toBeGreaterThan(0);
+      expect(ms).toBeLessThanOrEqual(120000);
+    }
+  });
+
+  it('RED KS-1240 R6 a pinata upload endpoint that never answers ends in the failure answer, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    const result = await outcome(() => new IPFSService('pinata', KEYS).upload(REQUEST));
+    expect(result).toContain('"success":false');
+  });
+
+  it('RED KS-1240 R7 a pinata pin endpoint that never answers ends in false, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new IPFSService('pinata', KEYS).pin('QmX'))).toBe('VALUE false');
+  });
+
+  it('RED KS-1240 R8 a gateway that never answers a read ends in the 503, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new IPFSService('pinata', KEYS).fetch('QmX'))).toBe('THREW 503');
+  });
+
+  it('control KS-1240 C1 a healthy pinata upload still answers its cid and size', async () => {
+    stubAnswering([]);
+    const result = await new IPFSService('pinata', KEYS).upload(REQUEST);
+    expect(result).toMatchObject({ success: true, cid: 'QmPinata', size: 3, pinned: true });
+  });
+
+  it('control KS-1240 C2 the in-memory mock provider still round-trips and makes no fetch', async () => {
+    const spy = vi.spyOn(globalThis, 'fetch');
+    const svc = new IPFSService('mock');
+    const up = await svc.upload(REQUEST);
+    expect((await svc.fetch(up.cid as string)).toString()).toBe('abc');
+    expect(spy).not.toHaveBeenCalled();
+  });
+
+  it('control KS-1240 C3 an unreachable endpoint still answers false for a pin', async () => {
+    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => { throw new Error('connect ECONNREFUSED'); }) as never);
+    expect(await new IPFSService('pinata', KEYS).pin('QmX')).toBe(false);
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief and vs nft-certificate `services/ipfs.service.ts` at base: its 8 outbound fetches (Pinata :70 :105 :123, Infura :166 :195 :208, Web3.Storage :239, gateway read :463) are exactly the 8 sites patched (the one other 'fetch' hit is the doc comment at :27 and the method name :455). Three constants: upload 60_000, pin/unpin 15_000, gateway read 30_000.
- DECISIONS for Wednesday: (1) the THREE bounds (60 s / 15 s / 30 s) are the drafter's. (2) Scope: KS-1240 is the api-gateway ticket; applying it to nft-certificate is the drafter's extension, which the owner confirms. (3) FINDING at source: the gateway read's `AbortSignal.timeout` also bounds the body read, but `await response.arrayBuffer()` (:487) sits OUTSIDE the try that maps a connection failure to `ServiceUnavailableError('IPFS gateway')`, so a stall during the body (after headers) surfaces as the raw timeout/abort error (likely a 500), not the 503 the constants comment promises; and a legitimately large object that needs more than 30 s to download now fails. Only the connect/header phase maps to 503.
- Apply mode: STRICT on both sections (apply_mode=strict; whole-patch `git apply --check` passes at develop bd6697e0).
- SEQUENCE: no shared file with any other held pass; 0 overlaps with the 14 open PRs.
- Verdict: HOLD-WITH-DECISION.
