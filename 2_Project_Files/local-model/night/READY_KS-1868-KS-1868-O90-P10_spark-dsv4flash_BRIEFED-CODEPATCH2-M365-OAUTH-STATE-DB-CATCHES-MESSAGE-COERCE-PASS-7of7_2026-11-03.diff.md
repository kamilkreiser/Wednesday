# READY — KS-1868-KS-1868-O90-P10 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 05:31 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 05:31 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/m365-integration/src/oauthState.ts } + { Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/oauthState.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/m365-integration/src/oauthState.ts
122	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: oauthState.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/m365-integration/src/oauthState.ts`; test(s): `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/m365-integration/src/oauthState.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts 122 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/oauthState.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 m365 OAuth state: the two DB catches survive a thrown value they cannot read RED ks1868 R1: a revoked Proxy from the state save is logged as text and the save resolves', 'KS-1868 m365 OAuth state: the two DB catches survive a thrown value they cannot read RED ks1868 R2: an Error whose message getter throws from the state save is logged as text and the save resolves', 'KS-1868 m365 OAuth state: the two DB catches survive a thrown value they cannot read RED ks1868 R3: a revoked Proxy from the state consume is logged as text and null is answered', 'KS-1868 m365 OAuth state: the two DB catches survive a thrown value they cannot read RED ks1868 R4: an Error whose message getter throws from the state consume is logged as text and null is answered']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=280 failed=0 | after: total=286 failed=0` · `NEW reds: []` [baseline_suite.json total=280 failed=0; after_suite.json total=286 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/oauthState.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts` (+122/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/m365-integration/src/oauthState.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4307ac876caea7d1835b17d6360760b7ec6e6bbe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/oauthState.ts b/Blockchain/Dev/services/m365-integration/src/oauthState.ts
--- a/Blockchain/Dev/services/m365-integration/src/oauthState.ts
+++ b/Blockchain/Dev/services/m365-integration/src/oauthState.ts
@@ -93,6 +93,13 @@
       encryptToken(rec.codeVerifier, 'code_verifier', rec.connectionId), rec.expiresAt,
     ]);
   } catch (err: any) {
-    logger.warn('DB save OAuth state failed', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB save OAuth state failed', { error: reason });
   }
 }
@@ -127,7 +134,14 @@
       expiresAt: new Date(row.expires_at),
     };
   } catch (err: any) {
-    logger.warn('DB consume OAuth state failed', { error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.warn('DB consume OAuth state failed', { error: reason });
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts
@@ -0,0 +1,122 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868 (operator 90 screen, m365-integration OAuth state): the two DB catches of services/m365-integration/src/oauthState.ts,
+// saveOAuthState (line 96) and consumeOAuthState (line 130), pass `err?.message` straight into the logger's meta object, unguarded.
+// `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws)
+// makes the catch throw, so the call REJECTS where an ordinary Error gets a logged warning and the documented outcome (save: the
+// state stays in memory and the call resolves; consume: `null`, which the callback treats as an unknown state). The cells make the
+// database stand-in reject with such a value and assert the call still resolves with that outcome and the warning carries text.
+// The stand-in rejects with a plain function, not vi.fn(): a spy could inspect a revoked Proxy and fail before the code under test
+// saw it. Harness: the real module with ./db, ./security/tokenCrypto and ./utils/logger replaced by plain stand-ins; no database,
+// no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+
+vi.mock('../security/tokenCrypto', () => ({
+  encryptToken: (value: string) => value,
+  decryptToken: (value: string | null) => value,
+}));
+
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { logger: { debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') } };
+});
+
+import { saveOAuthState, consumeOAuthState } from '../oauthState';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logs.length = 0;
+});
+
+const SAVE = 'DB save OAuth state failed';
+const CONSUME = 'DB consume OAuth state failed';
+const LOG = (message: string) => h.logs.filter((l) => l.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta?: Record<string, unknown> } | undefined): string => {
+  const e = l?.meta?.error;
+  return typeof e === 'string' ? e : '<' + typeof e + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const REC = {
+  bindingHash: 'binding-hash-ks1868',
+  connectionId: 'conn-ks1868',
+  organizationId: 'org-ks1868',
+  initiatedBy: 'user-ks1868',
+  codeVerifier: 'verifier-ks1868',
+  expiresAt: new Date(Date.now() + 600_000),
+};
+
+async function saveWith(value: unknown): Promise<{ threw: boolean }> {
+  h.toThrow = value;
+  try {
+    await saveOAuthState('state-hash-ks1868', REC);
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+async function consumeWith(value: unknown): Promise<{ threw: boolean; value?: unknown }> {
+  h.toThrow = value;
+  try {
+    return { threw: false, value: await consumeOAuthState('state-hash-ks1868', 'binding-hash-ks1868') };
+  } catch {
+    return { threw: true };
+  }
+}
+
+describe('KS-1868 m365 OAuth state: the two DB catches survive a thrown value they cannot read', () => {
+  it('control ks1868 C1: an ordinary Error from the state save is logged with its message and the save resolves', async () => {
+    expect(await saveWith(new Error('db boom'))).toEqual({ threw: false });
+    expect(LOG(SAVE)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE)[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: an ordinary Error from the state consume is logged with its message and null is answered', async () => {
+    expect(await consumeWith(new Error('db boom'))).toEqual({ threw: false, value: null });
+    expect(LOG(CONSUME)).toHaveLength(1);
+    expect(reasonOf(LOG(CONSUME)[0])).toBe('db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the state save is logged as text and the save resolves', async () => {
+    expect(await saveWith(revokedProxy())).toEqual({ threw: false });
+    expect(LOG(SAVE)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from the state save is logged as text and the save resolves', async () => {
+    expect(await saveWith(getterThrows())).toEqual({ threw: false });
+    expect(LOG(SAVE)).toHaveLength(1);
+    expect(reasonOf(LOG(SAVE)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoked Proxy from the state consume is logged as text and null is answered', async () => {
+    expect(await consumeWith(revokedProxy())).toEqual({ threw: false, value: null });
+    expect(LOG(CONSUME)).toHaveLength(1);
+    expect(reasonOf(LOG(CONSUME)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from the state consume is logged as text and null is answered', async () => {
+    expect(await consumeWith(getterThrows())).toEqual({ threw: false, value: null });
+    expect(LOG(CONSUME)).toHaveLength(1);
+    expect(reasonOf(LOG(CONSUME)[0])).toBe('unreadable thrown value');
+  });
+});
```
