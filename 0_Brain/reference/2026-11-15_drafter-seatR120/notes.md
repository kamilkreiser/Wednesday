# Drafter notes, Seat R 120th brief (2026-11-15 21:2x)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatR120_ks1699_tenant_admin.md
Develop read live: 9cbb9687021a1924321a751181bd4a9f42c6ab83 (shared checkout stale at 0e6479d7b6c0, so everything was read through the GitHub contents API; copies in _work/).

## Findings that shaped the brief
- Role read: callerMayReadCertification certifications.ts:162-176 reads (req as any).user; isPlatformRole at :172. Exact ORG_ADMIN predicate already exists: isPlatformOrOrgAdminRole keyRevokePolicy.ts:163 (exported index.ts:259).
- Tenant read: route lookup getCertification(id, getReqTenantId(req)) (:1349 share, :1464 recertify) is the tenant wall; Certification has no tenant field. Caller's own tenant = JWT claim req.user.tenantId (middleware/auth.ts:36, signed conditionally). decideTenantAccess keyRevokePolicy.ts:184 is the precedent compare; originate has 0 uses today.
- Hazard behind D1: a tenant-less ORG_ADMIN token would resolve to the DEFAULT tenant (requestTenant.ts, tenant-context.ts:75), so lookup-only would admit them into default-tenant rows.
- Existing KS-1695 cells R14/R15 pin ORG_ADMIN as refused reader: the new arm must be a separate helper, not a widening.
- Existing test fixtures set no tenantId on users; new cells need an asTenantUser helper.
- Overlap: only PR 2160 (of 81 open) touches routes/certifications.ts.
- Kam's tenant vs organisation: tenant holds many organisations (KS-764); Certification exposes no organisation, so an org-bound variant is NOT one line.

## For Wednesday to rule (also in the brief)
D1 claim compare vs lookup-only; D2 tenant-only vs org-bound; D3 lowercase org_admin admitted / dotless refused (follows shared predicate).

## UNMEASURED
- Whether live ORG_ADMIN tokens carry tenantId (auth jwt.ts near :263 not read).
- Whether any portal/SDK flow calls share or recertify as an ORG_ADMIN non-party (only ShareDialog.tsx:87 and RecertifyDialog.tsx:54 grep-confirmed as callers; SDKs and Platform S not re-scanned).
- Live suite count at develop 9cbb, tsc, eslint state, merge-tree against 2160, the pre-push hook's refusal lines (not read).
- Whether the 2233 fragment pair needs amending (read first ~400 chars of each only).
- gh code search returned empty for several queries (index lag); absence claims rest on the tree listing and file reads, not search.
