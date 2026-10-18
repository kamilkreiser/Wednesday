# READY — KS-1617-PROFILEFETCHSTATUS-1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker/patch.diff`** (from `ls` at 10:44 2026-10-19; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 10:44 2026-10-19 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `78cb3c3939e319332e387ffecb075a169edd4a39`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/providers/social/google.ts , Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/providers/social/google.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/auth/src/providers/social/google.ts
1	1	Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
62	0	Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: google.ts microsoft-personal.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/providers/social/google.ts`, `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/providers/social/google.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts 62 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/providers/social/google.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1617 A.3 - a refused profile fetch names the HTTP status RED KS-1617 P1: Google, a 503 from the profile endpoint reads "(HTTP 503)"', 'KS-1617 A.3 - a refused profile fetch names the HTTP status RED KS-1617 P2: Microsoft, a 401 from the profile endpoint reads "(HTTP 401)"']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1061 failed=0 | after: total=1066 failed=0` · `NEW reds: []` [baseline_suite.json total=1061 failed=0; after_suite.json total=1066 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/providers/social/google.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts` (+62/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/auth/src/providers/social/google.ts, Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `78cb3c3939e319332e387ffecb075a169edd4a39` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1617_p1/KS-1617.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1617_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/providers/social/google.ts b/Blockchain/Dev/services/auth/src/providers/social/google.ts
index 6b18d0242..08a879b18 100644
--- a/Blockchain/Dev/services/auth/src/providers/social/google.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/google.ts
@@ -49,3 +49,3 @@
     if (!profileRes.ok) {
-      throw new Error('Failed to fetch Google user profile');
+      throw new Error(`Failed to fetch Google user profile (HTTP ${profileRes.status})`);
     }
diff --git a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts b/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
index a37fd0cba..47b515e1b 100644
--- a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
@@ -48,3 +48,3 @@
     if (!profileRes.ok) {
-      throw new Error('Failed to fetch Microsoft user profile');
+      throw new Error(`Failed to fetch Microsoft user profile (HTTP ${profileRes.status})`);
     }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts
new file mode 100644
index 000000000..a7dd284cb
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1617-social-profile-fetch-failure-names-the-http-status.test.ts
@@ -0,0 +1,62 @@
+/**
+ * KS-1617 item A.3 - when the identity provider's profile endpoint refuses, the adapter threw "Failed to fetch Google user
+ * profile" (and the Microsoft twin) with no HTTP status, so a 401 (the token was refused) and a 503 (the provider is down)
+ * read the same in the log and in the 400 the callback answers. The status now rides in the message: "(HTTP 503)".
+ * The adapters are driven directly with a stubbed global fetch; nothing here touches the network.
+ */
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import { GoogleProvider } from '../providers/social/google';
+import { MicrosoftPersonalProvider } from '../providers/social/microsoft-personal';
+
+const CONFIG = { clientId: 'cid-ks1617', clientSecret: 'secret-ks1617', callbackUrl: 'https://app.test/cb', enabled: true };
+
+function reply(status: number, body: unknown): Response {
+  return {
+    ok: status >= 200 && status < 300,
+    status,
+    json: async () => body,
+    text: async () => (typeof body === 'string' ? body : JSON.stringify(body)),
+  } as unknown as Response;
+}
+
+/** The token endpoint answers `token`, then the profile endpoint answers `profile`. */
+function stubFetch(token: Response, profile: Response): void {
+  const queue = [token, profile];
+  vi.spyOn(globalThis, 'fetch').mockImplementation((async () => queue.shift() as Response) as never);
+}
+
+afterEach(() => { vi.restoreAllMocks(); });
+
+/** The message an adapter's exchangeCode rejects with ('did not throw' when it resolves), so a mismatch is an assertion failure. */
+async function failureOf(run: Promise<unknown>): Promise<string> {
+  try { await run; return 'did not throw'; } catch (e) { return e instanceof Error ? e.message : String(e); }
+}
+
+describe('KS-1617 A.3 - a refused profile fetch names the HTTP status', () => {
+  it('RED KS-1617 P1: Google, a 503 from the profile endpoint reads "(HTTP 503)"', async () => {
+    stubFetch(reply(200, { access_token: 'tok-g' }), reply(503, 'unavailable'));
+    expect(await failureOf(new GoogleProvider(CONFIG).exchangeCode('code-1'))).toBe('Failed to fetch Google user profile (HTTP 503)');
+  });
+
+  it('RED KS-1617 P2: Microsoft, a 401 from the profile endpoint reads "(HTTP 401)"', async () => {
+    stubFetch(reply(200, { access_token: 'tok-m' }), reply(401, 'unauthorized'));
+    expect(await failureOf(new MicrosoftPersonalProvider(CONFIG).exchangeCode('code-2'))).toBe('Failed to fetch Microsoft user profile (HTTP 401)');
+  });
+
+  it('CONTROL KS-1617 P3: Google, a healthy profile still maps to the provider id and email', async () => {
+    stubFetch(reply(200, { access_token: 'tok-g' }), reply(200, { id: 'g-123', email: 'a@ks1617.test', verified_email: true }));
+    const profile = await new GoogleProvider(CONFIG).exchangeCode('code-3');
+    expect([profile.providerId, profile.email]).toEqual(['g-123', 'a@ks1617.test']);
+  });
+
+  it('CONTROL KS-1617 P4: Microsoft, a healthy profile still maps to the provider id and email', async () => {
+    stubFetch(reply(200, { access_token: 'tok-m' }), reply(200, { id: 'm-456', mail: 'b@ks1617.test' }));
+    const profile = await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code-4');
+    expect([profile.providerId, profile.email]).toEqual(['m-456', 'b@ks1617.test']);
+  });
+
+  it('CONTROL KS-1617 P5: a refused TOKEN exchange keeps its own message (this change does not touch it)', async () => {
+    stubFetch(reply(400, 'invalid_grant'), reply(200, {}));
+    expect(await failureOf(new GoogleProvider(CONFIG).exchangeCode('code-5'))).toBe('Google token exchange failed: invalid_grant');
+  });
+});
```
