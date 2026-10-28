# READY — KS-1591-KS-1591-ks_1591_p1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1-control/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts , Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	1	Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
78	0	Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (4 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 4 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts byte-exact incl. leading whitespace (apply mode strict): OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)` [a3i_indent.out: `OK 4 line(s) byte-exact incl. leading whitespace (of 4; 4 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts fails at the untouched tip (6 failed / 13 run; controls green; assertion reds)` [red_first.json: failed=6 of total=13; red cell(s): ['KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 R1 a role spelled with a dotless i is not a platform role', 'KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 R2 a role spelled with a long s is not a platform role', 'KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 R3 a role array holding SUPER_ADMIN is not a platform role', 'KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 R4 a role array holding system_admin is not a platform role', 'KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 R5 a system admin role spelled with a long s is not a platform role', 'KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role RED KS-1591 D1 decideTenantAccess does not give a dotless-i role the platform-admin pass']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts passes with the product hunk (13 passed / 13 run)` [green_after.json: failed=0 of total=13, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1039 failed=1 | after: total=1052 failed=1` · `NEW reds: []` [baseline_suite.json total=1039 failed=1; after_suite.json total=1052 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +82/-1 test=src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` (+4/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts` (+78/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1591): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1591_p1/KS-1591.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts b/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
--- a/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
+++ b/Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts
@@ -138,5 +138,8 @@
  * @returns true for SYSTEM_ADMIN / SUPER_ADMIN, false for everything else.
  */
 export function isPlatformRole(role: string | undefined): boolean {
-  return PLATFORM_ROLES.has(String(role || '').toUpperCase());
+  // KS-1591: `String(role).toUpperCase()` is not an identity test. U+0131 (dotless i) upper-cases to `I`, U+017F (long s) upper-cases to `S`, and an ARRAY role stringifies to its element, so all three
+  // read as SUPER_ADMIN. Only an ASCII fold is applied (a-z to A-Z, every other character untouched), and a role that is not a string is refused outright.
+  if (typeof role !== 'string') return false;
+  return PLATFORM_ROLES.has(role.replace(/[a-z]/g, (ch) => ch.toUpperCase()));
 }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts
@@ -0,0 +1,78 @@
+// KS-1591 (packages/shared security/keyRevokePolicy.ts isPlatformRole): the predicate decided "platform administrator" with `String(role || '').toUpperCase()`, which is not an identity test.
+// U+0131 (dotless i) upper-cases to `I` and U+017F (long s) upper-cases to `S`, so `super_admin` spelled with either read as SUPER_ADMIN; and a role ARRAY stringifies to its element, so
+// `['SUPER_ADMIN']` read as SUPER_ADMIN too. R1 to R5 pin that each of those is refused; C1 to C6 pin that every spelling the platform really uses is still admitted and that an ordinary role,
+// an empty role and an absent role are still refused; D1 and D2 go through decideTenantAccess, the caller of the predicate, so the refusal is seen where the decision is made.
+// All non-ASCII characters are written as \u escapes so this file is pure ASCII.
+import { describe, it, expect } from 'vitest';
+import { isPlatformRole, decideTenantAccess } from '../index';
+
+const DOTLESS_I = '\u0131';
+const LONG_S = '\u017f';
+
+function asRole(value: unknown): string | undefined {
+  return value as string | undefined;
+}
+
+describe('KS-1591: isPlatformRole is an exact ASCII fold and refuses a non-string role', () => {
+  it('RED KS-1591 R1 a role spelled with a dotless i is not a platform role', () => {
+    expect(isPlatformRole('super_adm' + DOTLESS_I + 'n')).toBe(false);
+  });
+
+  it('RED KS-1591 R2 a role spelled with a long s is not a platform role', () => {
+    expect(isPlatformRole(LONG_S + 'uper_admin')).toBe(false);
+  });
+
+  it('RED KS-1591 R3 a role array holding SUPER_ADMIN is not a platform role', () => {
+    expect(isPlatformRole(asRole(['SUPER_ADMIN']))).toBe(false);
+  });
+
+  it('RED KS-1591 R4 a role array holding system_admin is not a platform role', () => {
+    expect(isPlatformRole(asRole(['system_admin']))).toBe(false);
+  });
+
+  it('RED KS-1591 R5 a system admin role spelled with a long s is not a platform role', () => {
+    expect(isPlatformRole(LONG_S + 'ystem_admin')).toBe(false);
+  });
+
+  it('control KS-1591 C1 SUPER_ADMIN and SYSTEM_ADMIN are platform roles', () => {
+    expect(isPlatformRole('SUPER_ADMIN')).toBe(true);
+    expect(isPlatformRole('SYSTEM_ADMIN')).toBe(true);
+  });
+
+  it('control KS-1591 C2 super_admin and system_admin are platform roles', () => {
+    expect(isPlatformRole('super_admin')).toBe(true);
+    expect(isPlatformRole('system_admin')).toBe(true);
+  });
+
+  it('control KS-1591 C3 a mixed-case spelling is a platform role', () => {
+    expect(isPlatformRole('Super_Admin')).toBe(true);
+    expect(isPlatformRole('sYsTeM_aDmIn')).toBe(true);
+  });
+
+  it('control KS-1591 C4 ordinary roles are not platform roles', () => {
+    expect(isPlatformRole('ADMIN')).toBe(false);
+    expect(isPlatformRole('ISSUER_ADMIN')).toBe(false);
+    expect(isPlatformRole('user')).toBe(false);
+  });
+
+  it('control KS-1591 C5 an empty role and an absent role are not platform roles', () => {
+    expect(isPlatformRole('')).toBe(false);
+    expect(isPlatformRole(undefined)).toBe(false);
+    expect(isPlatformRole(asRole(null))).toBe(false);
+  });
+
+  it('control KS-1591 C6 a role with surrounding whitespace is still not a platform role', () => {
+    expect(isPlatformRole(' SUPER_ADMIN')).toBe(false);
+    expect(isPlatformRole('SUPER_ADMIN ')).toBe(false);
+  });
+
+  it('RED KS-1591 D1 decideTenantAccess does not give a dotless-i role the platform-admin pass', () => {
+    const decision = decideTenantAccess({ role: 'super_adm' + DOTLESS_I + 'n', tenantId: 'tenant-a' }, 'tenant-b');
+    expect(decision.allow).toBe(false);
+  });
+
+  it('control KS-1591 D2 decideTenantAccess still gives super_admin the platform-admin pass', () => {
+    const decision = decideTenantAccess({ role: 'super_admin', tenantId: 'tenant-a' }, 'tenant-b');
+    expect(decision).toEqual({ allow: true, reason: 'platform-admin' });
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD
- Source-read against the brief: ONE product line replaced by four (2 comment lines, `if (typeof role !== 'string') return false;`, ASCII fold `role.replace(/[a-z]/g, ch => ch.toUpperCase())` then the same PLATFORM_ROLES lookup) in `isPlatformRole` (keyRevokePolicy.ts). Nothing else touched; `isOrgBoundedRole` / `isScopedAdminRole` deliberately left alone (the brief says why). Every ASCII spelling admitted before is admitted now; dotless-i, long-s and array roles are now refused.
- Behaviour to state to the owner: `isPlatformRole` is imported by originate (certifications.ts, adminConfig.ts) and others; a role that arrives as a non-string now answers false instead of being stringified. Reachability of such a token is not established (the ticket says so), so this is a nit-level hardening that fails toward LESS access.
- SEQUENCE: KS-1591 has TWO READYs. This one (packages/shared) and `ks_1591_p2_security` (services/security/src/index.ts) share NO file and neither imports the other change; raise either first. Same ticket: link both as Refs KS-1591, close-word on neither until both are merged.
- Verdict: HOLD.
