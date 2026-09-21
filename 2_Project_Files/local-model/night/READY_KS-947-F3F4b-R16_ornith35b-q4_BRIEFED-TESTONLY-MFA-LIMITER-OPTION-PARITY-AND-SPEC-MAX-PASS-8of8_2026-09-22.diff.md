# READY — KS-947-F3F4b-R16 (Ornith, briefed, test_only, modify · vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 03:41 2026-09-22). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; golden not located — no byte-identity claim is made.

**Held 03:41 2026-09-22 by Wednesday after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/out.md.checker`, not typed).** Tip `64ab105132eada0621622acf4d6053bc59926780`. Touches ONE file: `Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts` (modify). `+` lines 66 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 10/10 cells. Tampers (3), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `F3SKIP` → red exactly ['RED KS-947 F3 - the users MFA mount declares no limiter opti']
- `F4AUTH` → red exactly ['PARITY — the users MFA limiter has the SAME window and max a', 'RED KS-947 F4 - every mfa-policy operation publishes x-ratel']
- `F4USERS` → red exactly ['PARITY — the users MFA limiter has the SAME window and max a', 'RED KS-947 F4 - every mfa-policy operation publishes x-ratel']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/input.json`. Brief: `night/briefs/KS-947-F3F4b-R16.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks947-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts
@@ -96,4 +96,70 @@
     expect(usersShape.windowMs).toBe(authShape.windowMs);
     expect(usersShape.max).toBe(authShape.max);
   });
+  // KS-947 F3 + F4 - the parity gate's blind spots. Titles are plain ASCII (the checker matches the rendered title).
+  const SPEC_YAML = readFileSync(join(__dirname, '..', '..', '..', '..', 'docs', 'openapi', 'secuura-api.yaml'), 'utf8');
+  const LF = String.fromCharCode(10);
+  const QUOTE = String.fromCharCode(39);
+  /** A single-quoted string literal on one line (the mount paths are the only literals a mount call carries). */
+  const STRING_LITERAL = new RegExp(QUOTE + '.*?' + QUOTE, 'g');
+  /** Every option key written in a mount call (nested keys included); string literals blanked and line comments dropped first. */
+  const optionKeys = (call: string): Set<string> => {
+    const blanked = call.replace(STRING_LITERAL, QUOTE + QUOTE).split(LF).map((line) => line.split('//')[0]).join(LF);
+    const keys = new Set<string>();
+    const re = /([A-Za-z_$][A-Za-z0-9_$]*) *:/g;
+    let m = re.exec(blanked);
+    while (m !== null) { keys.add(m[1]); m = re.exec(blanked); }
+    return keys;
+  };
+  /** The production arm of `max: isNonProd ? <nonprod> : <prod>`, as a number. */
+  const productionMax = (shape: { max: string }): number => Number(/[?] *[0-9]+ *: *([0-9]+)/.exec(shape.max)?.[1]);
+  /** `15 * 60 * 1000` evaluated as a product of integers. */
+  const windowMsValue = (shape: { windowMs: string }): number => shape.windowMs.split('*').map((n) => Number(n.trim())).reduce((a, b) => a * b, 1);
+  /** x-ratelimit-window-ms / x-ratelimit-max of every operation the spec files under the mfa policy (the two lines that follow it). */
+  const specMfaLimits = (): Array<{ max: number; windowMs: number }> => {
+    const out: Array<{ max: number; windowMs: number }> = [];
+    const lines = SPEC_YAML.split(LF);
+    for (let i = 0; i < lines.length - 2; i++) {
+      if (lines[i].trim() !== 'x-ratelimit-policy: mfa') continue;
+      out.push({ windowMs: Number(lines[i + 1].split(':')[1]), max: Number(lines[i + 2].split(':')[1]) });
+    }
+    return out;
+  };
+  it('RED KS-947 F3 - the users MFA mount declares no limiter option the auth MFA mount does not', () => {
+    // A `skip: () => true` on the users mount alone keeps the PARITY cell green (windowMs and max unchanged)
+    // while switching the limiter off: the whole option set is compared, not two values.
+    const authKeys = optionKeys(mountCall('/api/auth/mfa') as string);
+    const usersKeys = optionKeys(mountCall('/api/users/me/mfa') as string);
+    const extra = Array.from(usersKeys).filter((k) => !authKeys.has(k));
+    expect(extra, 'options on the users mount that the auth mount does not declare').toEqual([]);
+  });
+  it('KS-947 F3 control - the users MFA limiter is mounted before the createProxyRoutes mount', () => {
+    // routes/proxy.ts mounts /api/users/me inside createProxyRoutes; a limiter registered after it never sees the request.
+    const usersCall = mountCall('/api/users/me/mfa');
+    expect(usersCall, 'the users MFA mount was not found').not.toBeNull();
+    const usersAt = GATEWAY_SRC.indexOf(usersCall as string);
+    const proxyAt = GATEWAY_SRC.indexOf('app.use(createProxyRoutes');
+    expect(proxyAt, 'the createProxyRoutes mount was not found').toBeGreaterThan(-1);
+    expect(usersAt, 'the users MFA limiter must precede the proxy mount').toBeLessThan(proxyAt);
+  });
+  it('KS-947 F4 control - the spec files at least one operation under the mfa rate-limit policy', () => {
+    expect(specMfaLimits().length, 'no x-ratelimit-policy: mfa operation in secuura-api.yaml').toBeGreaterThan(0);
+  });
+  it('RED KS-947 F4 - every mfa-policy operation publishes x-ratelimit-max equal to the auth MFA production max', () => {
+    const authMax = productionMax(limiterShape(mountCall('/api/auth/mfa') as string));
+    const limits = specMfaLimits();
+    expect(limits.map((l) => l.max), 'published max vs the /api/auth/mfa mount').toEqual(limits.map(() => authMax));
+  });
+  it('RED KS-947 F4 - every mfa-policy operation publishes x-ratelimit-max equal to the users MFA production max', () => {
+    const usersMax = productionMax(limiterShape(mountCall('/api/users/me/mfa') as string));
+    const limits = specMfaLimits();
+    expect(limits.map((l) => l.max), 'published max vs the /api/users/me/mfa mount').toEqual(limits.map(() => usersMax));
+  });
+  it('KS-947 F4 control - every mfa-policy operation publishes x-ratelimit-window-ms equal to both mounts windowMs', () => {
+    const authWindow = windowMsValue(limiterShape(mountCall('/api/auth/mfa') as string));
+    const usersWindow = windowMsValue(limiterShape(mountCall('/api/users/me/mfa') as string));
+    expect(usersWindow, 'the two mounts share one window').toBe(authWindow);
+    const limits = specMfaLimits();
+    expect(limits.map((l) => l.windowMs), 'published window vs the mounts').toEqual(limits.map(() => authWindow));
+  });
 });
```
