# READY — KS-1637-RETIREDVERIFYAPPCELL-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1637_p1/out.md.checker/patch.diff`** (from `ls` at 14:04 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1637_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:04 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1637_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `04a4a33938f05312a184fd2ca294745d628ff75d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/index.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (21 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 24 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 21 line(s) byte-exact incl. leading whitespace (of 21; 24 line(s) added by the apply)` [a3i_indent.out: `OK 21 line(s) byte-exact incl. leading whitespace (of 21; 24 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/index.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `3509925724c17e5a` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/index.ts:901)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1637_p1_135013/clone/Blockchain/Dev/services/api-gateway/src/index.ts:901: '  app.use(createVerificationRoutes({' -> "  app.post('/api/documents/:id/verify', (_req: Request, res: Response) => { res.status(200).json({ reAdded: true }); }); app.use(createVerificationRoutes({"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/index.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 901. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts fails at the untouched tip (1 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=1 of total=8; red cell(s): ['KS-1628 — the gateway no longer serves POST /api/documents/:id/verify RED KS-1637 G4: on the REAL gateway app a POST to the retired path is refused 401 by the /api/documents proxy mount, not answered by a handler registered ahead of it']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts passes with the product hunk (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1117 failed=0 | after: total=1119 failed=0` · `NEW reds: []` [baseline_suite.json total=1117 failed=0; after_suite.json total=1119 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +24/-0 test=src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts` (+24/-0 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/index.ts` is the tamper target and is byte-unchanged (sha256 3509925724c17e5a, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `04a4a33938f05312a184fd2ca294745d628ff75d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1637_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1637_p1/KS-1637.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1637_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1628-gateway-documents-verify-is-removed.test.ts
@@ -198,2 +198,26 @@
   });
+
+  // KS-1637 Minor 1: G1 reads the router stack and G2 drives an app that mounts ONLY the router, so a handler re-added in
+  // `index.ts` ahead of `app.use(createVerificationRoutes(` would reach neither. The next two cells drive the REAL gateway app,
+  // where an unauthenticated POST to a path no handler serves falls through to the `/api/documents` proxy mount and is
+  // refused 401 by its authenticateToken. A re-added handler answers with its own body instead.
+  async function postToIndex(path: string): Promise<{ status: number; code: string | null }> {
+    const res = await realFetch(`http://127.0.0.1:${indexPort}${path}`, {
+      method: 'POST',
+      headers: { 'content-type': 'application/json' },
+      body: '{}',
+    });
+    const body = (await res.json().catch(() => null)) as { error?: { code?: string } } | null;
+    return { status: res.status, code: body?.error?.code ?? null };
+  }
+
+  it('RED KS-1637 G4: on the REAL gateway app a POST to the retired path is refused 401 by the /api/documents proxy mount, not answered by a handler registered ahead of it', async () => {
+    const r = await postToIndex(`/api/documents/${DOC_ID}/verify`);
+    expect([r.status, r.code]).toEqual([401, 'UNAUTHORIZED']);
+  });
+
+  it('CONTROL KS-1637 G-C4: the same real app refuses a POST to a path the router DOES serve, /api/documents/:id/sign, with the same 401, so G4 reads the proxy mount and not an empty answer', async () => {
+    const r = await postToIndex(`/api/documents/${DOC_ID}/sign`);
+    expect([r.status, r.code]).toEqual([401, 'UNAUTHORIZED']);
+  });
 });
```
