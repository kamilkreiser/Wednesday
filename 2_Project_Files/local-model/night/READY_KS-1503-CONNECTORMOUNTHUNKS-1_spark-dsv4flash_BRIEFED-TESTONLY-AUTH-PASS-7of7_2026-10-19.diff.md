# READY — KS-1503-CONNECTORMOUNTHUNKS-1 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1503_p1/out.md.checker/patch.diff`** (from `ls` at 14:04 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1503_p1/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 14:04 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1503_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `04a4a33938f05312a184fd2ca294745d628ff75d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
38	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (34 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 38 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 34 line(s) byte-exact incl. leading whitespace (of 34; 38 line(s) added by the apply)` [a3i_indent.out: `OK 34 line(s) byte-exact incl. leading whitespace (of 34; 38 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `817845efd299c097` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:294)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-19_ks_1503_p1_135557/clone/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:294: '    // Not a verifiable token (bad signature, expired, malformed, no key): not a connector credential, so it goes on exactly' -> "    throw new Error('ks1503 tamper: the guard rethrows an unverifiable Bearer');"` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/middleware/auth.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 294. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts fails at the untouched tip (2 failed / 21 run; controls green; assertion reds)` [red_first.json: failed=2 of total=21; red cell(s): ['KS-1470 the real app, NODE_ENV=test — a connector JWT as a Bearer never reaches an upstream RED KS-1503 M1 - a type:connector token with a BAD signature goes on to the mount that forwards it: 200 and ONE upstream hit, not a 500', 'KS-1470 the real app, NODE_ENV=test — a connector JWT as a Bearer never reaches an upstream RED KS-1503 M2 - an EXPIRED type:connector token (good signature) goes on the same way: 200 and ONE upstream hit, not a 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts passes with the product hunk (21 passed / 21 run)` [green_after.json: failed=0 of total=21, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1117 failed=0 | after: total=1120 failed=0` · `NEW reds: []` [baseline_suite.json total=1117 failed=0; after_suite.json total=1120 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +38/-1 test=src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts` (+38/-1 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` is the tamper target and is byte-unchanged (sha256 817845efd299c097, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `04a4a33938f05312a184fd2ca294745d628ff75d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1503_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1503_p1/KS-1503.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1503_p1/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1470-a-connector-bearer-is-refused-before-every-mount.test.ts
@@ -43,2 +43,2 @@
-const EXPECTED_CELLS = 17;
+const EXPECTED_CELLS = 20;
 let CELLS_RUN = 0;
@@ -353,2 +353,39 @@
   });
+
+  // KS-1503 Minor 1: cell J asserts only "not the connector refusal", so it passes whether an unverifiable Bearer is forwarded,
+  // answered 401, or answered 500. If the front door's `catch` ever rethrew, every forged, expired or malformed Bearer would
+  // answer 500 on every route and J would stay green. The next two cells say what the Bearer DOES get; the third keeps the
+  // guard itself pinned. The forged and expired tokens below carry type:connector on purpose: that is the claim the guard acts on.
+  const unverifiable = {
+    forged: (): string => {
+      const { privateKey } = generateKeyPairSync('rsa', { modulusLength: 2048 });
+      return jwt.sign({ userId: 'connector:ks1503-forged', role: 'connector', type: 'connector', tenantId: TENANT }, privateKey.export({ type: 'pkcs1', format: 'pem' }) as string, { algorithm: 'RS256', expiresIn: '10m' });
+    },
+    expired: (): string =>
+      jwt.sign({ userId: 'connector:ks1503-expired', role: 'connector', type: 'connector', tenantId: TENANT, exp: Math.floor(Date.now() / 1000) - 3600 }, PRIV, { algorithm: 'RS256' }),
+  };
+
+  it('RED KS-1503 M1 - a type:connector token with a BAD signature goes on to the mount that forwards it: 200 and ONE upstream hit, not a 500', async () => {
+    CELLS_RUN += 1;
+    const bearer = 'Bearer ' + unverifiable.forged();
+    const mark = hits.length;
+    const r = await send(gateway!.url, 'GET', '/api/documents/ks1503/sig-json', { authorization: bearer });
+    await settle(60);
+    expect([r.status, isRefusal(r), hits.slice(mark).filter((h) => h.authorization === bearer).length]).toEqual([200, false, 1]);
+  });
+
+  it('RED KS-1503 M2 - an EXPIRED type:connector token (good signature) goes on the same way: 200 and ONE upstream hit, not a 500', async () => {
+    CELLS_RUN += 1;
+    const bearer = 'Bearer ' + unverifiable.expired();
+    const mark = hits.length;
+    const r = await send(gateway!.url, 'GET', '/api/documents/ks1503/sig-json', { authorization: bearer });
+    await settle(60);
+    expect([r.status, isRefusal(r), hits.slice(mark).filter((h) => h.authorization === bearer).length]).toEqual([200, false, 1]);
+  });
+
+  it('CONTROL KS-1503 M3 - a type:connector token with a GOOD signature is still refused 401 with the connector refusal and 0 upstream hits (the guard itself is unchanged)', async () => {
+    CELLS_RUN += 1;
+    const { res, forwarded } = await sendConnector(gateway!.url, 'GET', '/api/documents/ks1503/sig-json');
+    expect([res.status, isRefusal(res), forwarded.length]).toEqual([401, true, 0]);
+  });
 });
```
