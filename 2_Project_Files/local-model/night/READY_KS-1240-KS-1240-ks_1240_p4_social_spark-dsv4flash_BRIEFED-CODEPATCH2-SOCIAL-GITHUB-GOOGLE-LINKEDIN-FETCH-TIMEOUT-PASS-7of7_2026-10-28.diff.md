# READY — KS-1240-KS-1240-ks_1240_p4_social (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/patch.diff`** (from `ls` at 16:10 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/section_3.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/section_4.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/github.ts b/Blockchain/Dev/services/auth/src/providers/social/github.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/github.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/github.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 35 (0 '-' / 1 '+' lines; model header -32,4 +36,5);hunk 3: reanchored at 45 (0 '-' / 1 '+' lines; model header -43,3 +48,4);hunk 4: reanchored at 59 (0 '-' / 1 '+' lines; model header -56,6 +62,7);reanchored 4/4 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/google.ts b/Blockchain/Dev/services/auth/src/providers/social/google.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/google.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/google.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 36 (0 '-' / 1 '+' lines; model header -33,4 +37,5);hunk 3: reanchored at 47 (0 '-' / 1 '+' lines; model header -45,3 +50,4);reanchored 3/3 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 3: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts b/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts' vs '+++ --- a/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/auth/src/providers/social/linkedin.ts: REANCHORED — the model's context lines did not match the file; every hunk rebuilt from its -/+ lines at the file's real location (hunk 1: reanchored at 2 (0 '-' / 4 '+' lines; model header -1,1 +1,5);hunk 2: reanchored at 34 (0 '-' / 1 '+' lines; model header -31,4 +35,5);hunk 3: reanchored at 44 (0 '-' / 1 '+' lines; model header -42,3 +47,4);reanchored 3/3 hunk(s);); strict rc=1 lenient rc=1 fuzzy rc=1] [section 4: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/auth/src/providers/social/github.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/github.ts:1`; section 2 (Blockchain/Dev/services/auth/src/providers/social/google.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/google.ts:1`; section 3 (Blockchain/Dev/services/auth/src/providers/social/linkedin.ts): `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/linkedin.ts:1` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 16:10 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/providers/social/github.ts , Blockchain/Dev/services/auth/src/providers/social/google.ts , Blockchain/Dev/services/auth/src/providers/social/linkedin.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/providers/social/github.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (4 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	0	Blockchain/Dev/services/auth/src/providers/social/github.ts
6	0	Blockchain/Dev/services/auth/src/providers/social/google.ts
6	0	Blockchain/Dev/services/auth/src/providers/social/linkedin.ts
128	0	Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: github.ts google.ts linkedin.ts`
- CODE_PATCH2 (rung 3, 3 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/providers/social/github.ts`, `Blockchain/Dev/services/auth/src/providers/social/google.ts`, `Blockchain/Dev/services/auth/src/providers/social/linkedin.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/providers/social/github.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/providers/social/google.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/providers/social/linkedin.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts 128 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=4 measured=4 ok=4 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=4 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/providers/social/github.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/github.ts:1`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/providers/social/google.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/google.ts:1`)
- section 3 `section_3.diff` → `Blockchain/Dev/services/auth/src/providers/social/linkedin.ts` (hunks=3, miscount=0; applied file per `section_3.opts`: `section_3.reanchored.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/auth/src/providers/social/linkedin.ts:1`)
- section 4 `section_4.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_4.opts`: `section_4.diff`, git-apply options: `(none — strict)`; `apply_check_strict_4.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (7 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=7 of total=9; red cell(s): ['KS-1240: the social adapters bound their outbound fetches RED KS-1240 R1 every github fetch (token, user, emails) carries an AbortSignal', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R2 every google fetch (token, userinfo) carries an AbortSignal', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R3 every linkedin fetch (token, userinfo) carries an AbortSignal', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R4 the seven bounds handed to AbortSignal.timeout are positive and at most 30000 ms', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R5 a github token endpoint that never answers ends in a rejection, not a hang', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R6 a google token endpoint that never answers ends in a rejection, not a hang', 'KS-1240: the social adapters bound their outbound fetches RED KS-1240 R7 a linkedin token endpoint that never answers ends in a rejection, not a hang']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 3 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=0 | after: total=1209 failed=0` · `NEW reds: []` [baseline_suite.json total=1200 failed=0; after_suite.json total=1209 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=4 products=3 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/providers/social/github.ts` (+7/-0 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts` (+128/-0); 4 files in all (code_patch2: products Blockchain/Dev/services/auth/src/providers/social/github.ts, Blockchain/Dev/services/auth/src/providers/social/google.ts, Blockchain/Dev/services/auth/src/providers/social/linkedin.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.reanchored.diff`: `git apply -p1` (strict); section 2 `section_2.reanchored.diff`: `git apply -p1` (strict); section 3 `section_3.reanchored.diff`: `git apply -p1` (strict); section 4 `section_4.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p4_social/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/providers/social/github.ts b/Blockchain/Dev/services/auth/src/providers/social/github.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/github.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/github.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -32,4 +36,5 @@
         code,
         redirect_uri: this.config.callbackUrl,
       }),
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
@@ -43,3 +48,4 @@
     const profileRes = await fetch('https://api.github.com/user', {
       headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
@@ -56,6 +62,7 @@
     if (!email) {
       const emailsRes = await fetch('https://api.github.com/user/emails', {
         headers: { Authorization: `Bearer ${access_token}`, Accept: 'application/json' },
+        signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
       });
       if (emailsRes.ok) {
         const emails = (await emailsRes.json()) as { email: string; primary: boolean; verified: boolean }[];
diff --git a/Blockchain/Dev/services/auth/src/providers/social/google.ts b/Blockchain/Dev/services/auth/src/providers/social/google.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/google.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/google.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -33,4 +37,5 @@
         redirect_uri: this.config.callbackUrl,
         grant_type: 'authorization_code',
       }),
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
@@ -45,3 +50,4 @@
     const profileRes = await fetch('https://www.googleapis.com/oauth2/v2/userinfo', {
       headers: { Authorization: `Bearer ${tokens.access_token}` },
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
diff --git a/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts b/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts
--- a/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts
+++ b/Blockchain/Dev/services/auth/src/providers/social/linkedin.ts
@@ -1,1 +1,5 @@
 import { SocialProvider, SocialProviderConfig, SocialProfile } from './types';
+
+// KS-1240 (class): every hand-built outbound fetch carries a timeout signal. Without one an identity provider that accepts the connection and never answers holds the callback request open for as
+// long as the socket lives. On expiry the fetch rejects, exchangeCode rejects, and the callback's existing catch answers as it already does for any other provider failure.
+const SOCIAL_PROVIDER_FETCH_TIMEOUT_MS = 10_000;
@@ -31,4 +35,5 @@
         client_secret: this.config.clientSecret,
         redirect_uri: this.config.callbackUrl,
       }),
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
@@ -42,3 +47,4 @@
     const profileRes = await fetch('https://api.linkedin.com/v2/userinfo', {
       headers: { Authorization: `Bearer ${access_token}` },
+      signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS),
     });
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts
@@ -0,0 +1,128 @@
+// KS-1240 (class: hand-built outbound fetches with no timeout), services/auth social adapters github.ts, google.ts and linkedin.ts: their seven fetches (github token, user, user/emails; google token,
+// userinfo; linkedin token, userinfo) passed no `signal`, so an identity provider that accepts the connection and never answers held the OAuth callback open for as long as the socket lived. The adapters are
+// driven directly with a stubbed global fetch that honours `init.signal` (and never answers when there is none); nothing touches the network. R1 to R3 pin that every fetch carries an AbortSignal, R4 that
+// each bound is a sane positive number, R5 to R7 that a provider that never answers ends in a rejection, not a hang. C1 and C2 pin that the full exchange and the refusal message are unchanged.
+import { describe, it, expect, afterEach, vi } from 'vitest';
+import { GitHubProvider } from '../providers/social/github';
+import { GoogleProvider } from '../providers/social/google';
+import { LinkedInProvider } from '../providers/social/linkedin';
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
+/** Answers by URL and records the signal each call carried. `emailless` makes github's user profile carry no email, so the emails fetch happens too. */
+function stubAnswering(seen: Seen[], emailless = false): void {
+  vi.spyOn(globalThis, 'fetch').mockImplementation((async (url: unknown, init?: { signal?: unknown }) => {
+    const u = String(url);
+    seen.push({ url: u, signal: init?.signal });
+    if (u.includes('github.com/login/oauth/access_token')) return reply(200, { access_token: 'tok' });
+    if (u.endsWith('api.github.com/user')) return reply(200, emailless ? { id: 7, login: 'octo', name: 'Octo Cat' } : { id: 7, login: 'octo', email: 'o@x.test', name: 'Octo Cat' });
+    if (u.endsWith('api.github.com/user/emails')) return reply(200, [{ email: 'o@x.test', primary: true, verified: true }]);
+    if (u.includes('googleapis.com/token')) return reply(200, { access_token: 'tok' });
+    if (u.includes('googleapis.com/oauth2/v2/userinfo')) return reply(200, { id: 'g1', email: 'g@x.test', verified_email: true });
+    if (u.includes('linkedin.com/oauth/v2/accessToken')) return reply(200, { access_token: 'tok' });
+    if (u.includes('api.linkedin.com/v2/userinfo')) return reply(200, { sub: 'l1', email: 'l@x.test', email_verified: true });
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
+describe('KS-1240: the social adapters bound their outbound fetches', () => {
+  it('RED KS-1240 R1 every github fetch (token, user, emails) carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen, true);
+    await new GitHubProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(3);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R2 every google fetch (token, userinfo) carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new GoogleProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(2);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R3 every linkedin fetch (token, userinfo) carries an AbortSignal', async () => {
+    const seen: Seen[] = [];
+    stubAnswering(seen);
+    await new LinkedInProvider(CONFIG).exchangeCode('code');
+    expect(seen).toHaveLength(2);
+    for (const call of seen) expect(call.signal).toBeInstanceOf(AbortSignal);
+  });
+
+  it('RED KS-1240 R4 the seven bounds handed to AbortSignal.timeout are positive and at most 30000 ms', async () => {
+    const timeout = vi.spyOn(AbortSignal, 'timeout');
+    stubAnswering([], true);
+    await new GitHubProvider(CONFIG).exchangeCode('code');
+    await new GoogleProvider(CONFIG).exchangeCode('code');
+    await new LinkedInProvider(CONFIG).exchangeCode('code');
+    const bounds = timeout.mock.calls.map((c) => c[0] as number);
+    expect(bounds).toHaveLength(7);
+    for (const ms of bounds) {
+      expect(ms).toBeGreaterThan(0);
+      expect(ms).toBeLessThanOrEqual(30000);
+    }
+  });
+
+  it('RED KS-1240 R5 a github token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new GitHubProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('RED KS-1240 R6 a google token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new GoogleProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('RED KS-1240 R7 a linkedin token endpoint that never answers ends in a rejection, not a hang', async () => {
+    vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => AbortSignal.abort());
+    stubNeverAnswering();
+    expect(await outcome(() => new LinkedInProvider(CONFIG).exchangeCode('code'))).toBe('REJECTED');
+  });
+
+  it('control KS-1240 C1 the full exchange of each adapter still resolves to the same provider id', async () => {
+    stubAnswering([], true);
+    expect((await new GitHubProvider(CONFIG).exchangeCode('code')).providerId).toBe('7');
+    expect((await new GoogleProvider(CONFIG).exchangeCode('code')).providerId).toBe('g1');
+    expect((await new LinkedInProvider(CONFIG).exchangeCode('code')).providerId).toBe('l1');
+  });
+
+  it('control KS-1240 C2 a refused github token exchange still throws its own message', async () => {
+    vi.spyOn(globalThis, 'fetch').mockImplementation((async () => reply(401, 'bad_verification_code')) as never);
+    await expect(new GitHubProvider(CONFIG).exchangeCode('code')).rejects.toThrow('GitHub token exchange failed: bad_verification_code');
+  });
+});
```


## DECISION NOTE (source-read, Spark operator 3 for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: golden.diff vs brief and vs the three providers at base: github.ts (token exchange :23, profile :43, emails :57), google.ts (:26, :45), linkedin.ts (:24, :42) are ALL their fetches (7 sites, `grep -n 'fetch('` per file); each gains `signal: AbortSignal.timeout(SOCIAL_PROVIDER_FETCH_TIMEOUT_MS)` and each file one 10_000 ms constant. Nothing else changes.
- DECISIONS for Wednesday: (1) the 10 000 ms bound is the drafter's. (2) What a timeout now answers: on the login callback (routes/auth.ts:1074) the exchange sits in a try whose catch throws `BadRequestError('OAuth authentication failed: ' + exchangeErr.message)`, so a hung provider becomes a 400 whose message is the abort text; the OAuth state is already consumed (consumeOAuthState runs first), so the user must restart the login. On `POST /social/link` (auth.ts:1360) the exchange has NO local try: the rejection goes to `next(err)` as an unclassified error (a 500 unless the error handler maps TimeoutError). Neither was changed or pinned by this patch.
- Apply mode: NOT STRICT. Sections 1-3 (the three provider files) were REANCHORED by the checker: the model's context lines did not match, every hunk was rebuilt from its -/+ lines at the file's real location (github: hunks at 2, 35, 45, 59; header e.g. `-1,1 +1,5` is not the real anchor); section 4 (the new test) strict. A strict `git apply --check` of patch.diff FAILS (`patch failed: ...github.ts:1`), also at develop bd6697e0; the raise seat must apply the three `section_N.reanchored.diff` files named in the CANONICAL PATCH note (or insert the '+' lines at the stated lines), and say so. STRICT APPLY NOT CLAIMED.
- SEQUENCE: shares no file with any other held pass (ks_1240_p5_social2 is apple/facebook/microsoft-personal); 0 overlaps with the 14 open PRs.
- Verdict: HOLD-WITH-DECISION.
