# READY — KS-1283-PROVADMIN-1 (Ornith, briefed, test_only, vitest) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1283-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 01:00 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS.

**Held 01:00 2026-09-21 by the 23:4x Wednesday seat after a source read.** Tip `778e6cfe2b6061d60ffcf3a57a951c84dc152b67`. Adds ONE cell to `api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts` (the direct driver of the REAL `requireOrgProvisioner`, fake req/res) pinning that a tenant ADMIN role (`ADMIN` and `admin`) is refused 403 with no provisionerKind — the widened-SUPER_ROLES shape KS-1283 describes ("would let register-connector mint a key"). **Scope stated:** this pins the GUARD the lead row mounts (`:489 → :91 → :97`), NOT the register-connector mount/handler/key-mint outcome, nor the five `requireSuperAdmin` routes — those need the ks1215 real-app shape (a Claude seat, or a later brief once the held ks1215 READYs merge). KS-1283 stays OPEN.

**Source read (Wednesday, same action):** 4 `+` lines, all 4 byte-present in `night/briefs/KS-1283-PROVADMIN-1.md`; 0 `-`; one test file (T2); sibling KS-1232 control 1/4. First sample, round 1.

**Tampers (T6 each reds exactly `provadmin`; T8 restored by bytes, sha `7d04a92ca724` = tip blob):** WIDENROLES — `routes/platform.ts:64` `const SUPER_ROLES = ['super_admin', 'SUPER_ADMIN', 'platform_admin', 'SYSTEM_ADMIN'];` (count 1 at the tip, control `SUPER_ROLES.includes` = 2, byte-checked by Wednesday); ADMINBRANCH — `:97` `  if (SUPER_ROLES.includes(user.role)) {` (count 1). Controls: 3 full `it` titles, green under both.

**Checker (01:00):** `RESULT: PASS (8/8)`; whole api-gateway 678/678 bare → 679/679 with the cell (drafter's precheck at 778e6cfe2, `runs/2026-09-21_search-widen-drafter-precheck/`).

**For the raise seat:** strict apply; TEST-ONLY (STOP on any product byte); api-gateway vitest 679 expected; `Refs KS-1283`. Partition: the ks480-org-provisioner-gate file is owned by no live seat (Seat B 11th's ks480 file is `ks480-connector-auth.test.ts` — a different file; Seat A is anchoring). **Banked for the NEXT raise seat: THREE — KS-1203 NESTEDTYPE-1 + WSTRIM-1 (one PR), KS-1283 PROVADMIN-1.**

---
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks480-org-provisioner-gate.test.ts
@@ -83,1 +83,5 @@
+  it('RED KS-1283: refuses a tenant ADMIN role (ADMIN and admin) with 403 and marks no provisionerKind - the widened SUPER_ROLES shape that would let register-connector mint a key', () => {
+    const outcomes = ['ADMIN', 'admin'].map((role) => { const r = harness({ role }); return [role, r.passed, r.status, /platform-admin role/.test(r.body?.error?.message ?? ''), r.kind]; });
+    expect(outcomes).toEqual([['ADMIN', false, 403, true, undefined], ['admin', false, 403, true, undefined]]);
+  });
 });
