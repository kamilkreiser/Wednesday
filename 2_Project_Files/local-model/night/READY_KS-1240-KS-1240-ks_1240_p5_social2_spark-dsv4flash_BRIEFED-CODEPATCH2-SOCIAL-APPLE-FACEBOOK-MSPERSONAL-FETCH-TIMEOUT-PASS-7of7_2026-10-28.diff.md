# READY — KS-1240-KS-1240-ks_1240_p5_social2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/section_4.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/apple.ts b/Blockchain/Dev/services/auth/src/providers/social/apple.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/apple.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/apple.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 35 (0 '-' / 1 '+' lines; model header -32,4 +36,5);reanchored 2/2 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/facebook.ts b/Blockchain/Dev/services/auth/src/providers/social/facebook.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/facebook.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/facebook.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 31 (0 '-' / 1 '+' lines; model header -28,4 +32,5);hunk 3: reanchored at 41 (0 '-' / 1 '+' lines; model header -39,3 +44,4);reanchored 3/3 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 3: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts b/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 36 (0 '-' / 1 '+' lines; model header -33,4 +37,5);hunk 3: reanchored at 46 (0 '-' / 1 '+' lines; model header -44,3 +49,4);reanchored 3/3 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 4: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/auth/src/providers/social/apple.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/apple.ts:1`; section 2 (Blockchain/Dev/services/auth/src/providers/social/facebook.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/facebook.ts:1`; section 3 (Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts:1` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/providers/social/apple.ts , Blockchain/Dev/services/auth/src/providers/social/facebook.ts , Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/providers/social/apple.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts` (test) — equal to numstat.out's set (4 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	0	Blockchain/Dev/services/auth/src/providers/social/apple.ts
6	0	Blockchain/Dev/services/auth/src/providers/social/facebook.ts
6	0	Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
131	0	Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: apple.ts facebook.ts microsoft-personal.ts`
- CODE_PATCH2 (rung 3, 3 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/providers/social/apple.ts`, `Blockchain/Dev/services/auth/src/providers/social/facebook.ts`, `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/providers/social/apple.ts 5 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/providers/social/facebook.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts 131 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=4 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/providers/social/apple.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/apple.ts:1`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/providers/social/facebook.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/facebook.ts:1`)
- section 3 `section_3.diff` → `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts` (hunks=3, miscount=0; applied file per `section_3.opts`: `section_3.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts:1`)
- section 4 `section_4.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts` (hunks=1, miscount=0; applied file per `section_4.opts`: `section_4.diff`, git-apply options: `(none — strict)`; `apply_check_strict_4.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (7 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=7 of total=9; red cell(s): ['KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R1 the apple token fetch carries an AbortSignal', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R2 both facebook fetches (token, me) carry an AbortSignal', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R3 both microsoft fetches (token, graph me) carry an AbortSignal', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R4 the five bounds handed to AbortSignal.timeout are positive and at most 30000 ms', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R5 an apple token endpoint that never answers ends in a rejection, not a hang', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R6 a facebook token endpoint that never answers ends in a rejection, not a hang', 'KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches RED KS-1240 R7 a microsoft token endpoint that never answers ends in a rejection, not a hang']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 3 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=0 | after: total=1209 failed=0` · `NEW reds: []` [baseline_suite.json total=1200 failed=0; after_suite.json total=1209 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=3 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/providers/social/apple.ts` (+5/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts` (+131/-0); 4 files in all (code_patch2: products Blockchain/Dev/services/auth/src/providers/social/apple.ts, Blockchain/Dev/services/auth/src/providers/social/facebook.ts, Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.reanchored.diff`: `git apply -p1` (strict); section 2 `section_2.reanchored.diff`: `git apply -p1` (strict); section 3 `section_3.reanchored.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p5_social2/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/providers/social/apple.ts b/Blockchain/Dev/services/auth/src/providers/social/apple.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/apple.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/apple.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -32,4 +36,5 @@
         grant_type: 'authorization_code',
         redirect_uri: this.config.callbackUrl,
       }),
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
diff --git a/Blockchain/Dev/services/auth/src/providers/social/facebook.ts b/Blockchain/Dev/services/auth/src/providers/social/facebook.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/facebook.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/facebook.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -28,4 +32,5 @@
         redirect_uri: this.config.callbackUrl,
         code,
       })}`,
+      { signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS), },
     );
@@ -39,3 +44,4 @@
     const profileRes = await fetch(
       `https://graph.facebook.com/v19.0/me?fields=id,email,name,first_name,last_name,picture&access_token=${access_token}`,
+      { signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS), },
     );
diff --git a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts b/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -33,4 +37,5 @@
         grant_type: 'authorization_code',
         scope: 'openid email profile User.Read',
       }),
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
@@ -44,3 +49,4 @@
     const profileRes = await fetch('https://graph.microsoft.com/v1.0/me', {
       headers: { Authorization: `Bearer ${access_token}` },
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts
@@ -0,0 +1,131 @@
+// KS-1240 (class: hand-built outbound fetches with no timeout), services/auth social adapters apple.ts, facebook.ts and microsoft-personal.ts: their five fetches (apple token; facebook token and /me;
+// microsoft token and graph /me) passed no `signal`, so an identity provider that accepts the connection and never answers held the OAuth callback open for as long as the socket lived. Facebook's two
+// fetches were called with a URL only, so they gain an init object. The adapters are driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing
+// touches the network. R1 to R3 pin that every fetch carries an AbortSignal, R4 that each bound is a sane positive number, R5 to R7 that a provider that never answers ends in a rejection, not a hang.
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import { AppleProvider } from '../providers/social/apple';
+import { FacebookProvider } from '../providers/social/facebook';
+import { MicrosoftPersonalProvider } from '../providers/social/microsoft-personal';
+
+const CONFIG = { clientId: 'cid-ks1240', clientSecret: 'secret-ks1240', callbackUrl: 'https://app.test/cb', enabled: true };
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
+type Seen = { url: string; signal: unknown };
+
+/** An Apple id_token whose payload segment carries `sub`, as the adapter decodes it. */
+function appleIdToken(): string {
+  return 'h.' + Buffer.from(JSON.stringify({ sub: 'a1', email: 'a@x.test', email_verified: true })).toString('base64') + '.s';
+}
+
+/** Answers by URL and records the signal each call carried (the second argument may be missing). */
+function stubAnswering(seen: Seen[]): void {
+  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
+    const u = String(url);
+    seen.push({ url: u, signal: init?.signal });
+    if (u.includes('appleid.apple.com/auth/token')) return reply(200, { id_token: appleIdToken() });
+    if (u.includes('graph.facebook.com/v19.0/oauth/access_token')) return reply(200, { access_token: 'tok' });
+    if (u.includes('graph.facebook.com/v19.0/me')) return reply(200, { id: 'f1', email: 'f@x.test', name: 'F B' });
+    if (u.includes('login.microsoftonline.com/consumers')) return reply(200, { access_token: 'tok' });
+    if (u.includes('graph.microsoft.com/v1.0/me')) return reply(200, { id: 'm1', mail: 'm@x.test', displayName: 'M S' });
+    return reply(404, 'unexpected url ' + u);
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
+/** 'REJECTED' when exchangeCode rejects, 'RESOLVED' when it resolves, 'HUNG' when it is still pending after 300 ms, so a hang is a red assertion and not a stuck run. */
+async function outcome(run: () => Promise<unknown>): Promise<string> {
+  return Promise.race([
+    run().then(() => 'RESOLVED', () => 'REJECTED'),
+    new Promise<string>((resolve) => setTimeout(() => resolve('HUNG'), 300)),
+  ]);
+}
+
+describe('KS-1240: the apple, facebook and microsoft-personal adapters bound their outbound fetches', () => {
+  it('RED KS-1240 R1 the apple token fetch carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new AppleProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(1);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R2 both facebook fetches (token, me) carry an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new FacebookProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(2);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R3 both microsoft fetches (token, graph me) carry an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(2);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R4 the five bounds handed to AbortSignal.timeout are positive and at most 30000 ms', async () => {
+    const timeout = vi.spyOn(AbortSignal, 'timeout');
+    stubAnswering([]);
+    await new AppleProvider(CONFIG).exchangeCode('code');
+    await new FacebookProvider(CONFIG).exchangeCode('code');
+    await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code');
+    const bounds = timeout.mock.calls.map((c) => c[0] as number);
+    expect(bounds).toHaveLength(5);
+    for (const ms of bounds) {
+      expect(ms).toBeGreaterThan(0);
+      expect(ms).toBeLessThanOrEqual(30000);
+    }
+  });
+
+  it('RED KS-1240 R5 an apple token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new AppleProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('RED KS-1240 R6 a facebook token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new FacebookProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('RED KS-1240 R7 a microsoft token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new MicrosoftPersonalProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('control KS-1240 C1 the full exchange of each adapter still resolves to the same provider id', async () => {
+    stubAnswering([]);
+    expect((await new AppleProvider(CONFIG).exchangeCode('code')).providerId).toBe('a1');
+    expect((await new FacebookProvider(CONFIG).exchangeCode('code')).providerId).toBe('f1');
+    expect((await new MicrosoftPersonalProvider(CONFIG).exchangeCode('code')).providerId).toBe('m1');
+  });
+
+  it('control KS-1240 C2 a refused apple token exchange still throws its own message', async () => {
+    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => reply(400, 'invalid_grant')) as never);
+    await expect(new AppleProvider(CONFIG).exchangeCode('code')).rejects.toThrow('Apple token exchange failed: invalid_grant');
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief and vs the providers at base: apple.ts (one fetch, :25), facebook.ts (:24, :39), microsoft-personal.ts (:25, :44) are ALL their fetches (5 sites). apple and microsoft-personal gain `signal:` inside the existing init object; facebook's two fetches had NO init object, so each gains a second argument `{ signal: AbortSignal.timeout(...), }` (style note: a trailing comma inside a one-property literal; a formatter may rewrite it).
- DECISIONS for Wednesday: (1) 10 000 ms is the drafter's. (2) A timeout surfaces as in ks_1240_p4_social: 400 'OAuth authentication failed: <abort text>' on the login callback (auth.ts:1074, state already consumed) and an unclassified rejection on `POST /social/link` (auth.ts:1360, no local try). Not changed or pinned here.
- Apply mode: NOT STRICT. Sections 1-3 REANCHORED by the checker (hunks rebuilt from their -/+ lines at the real location), section 4 strict; a strict `git apply --check` of patch.diff fails (`patch failed: ...apple.ts:1`), also at develop bd6697e0. The raise seat applies the `section_N.reanchored.diff` files. STRICT APPLY NOT CLAIMED.
- SEQUENCE: no shared file with any other held pass; 0 overlaps with the 14 open PRs. The two social-provider READYs (p4, p5) can be one PR or two; the constant has the same name in each file, which is fine (module-local).
- Verdict: HOLD-WITH-DECISION.
