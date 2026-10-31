#!/usr/bin/env python3
import sys, json, os
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate66-ks1906-1878/scripts')
import run as R
OWN = 'src/ownership.ts'; REPO = 'src/repositories/credentialRepo.ts'
M = {
 'GM1_null_tenant_guard_dropped': [(OWN, "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;",
                                         "if (role === null || !isPlatformRole(role)) return false;\n  return claim(user?.tenantId) === rowTenantId;")],
 'GM2_sql_flag_forced_true': [(REPO, "return [userId, tenantId, tenantId !== null && ownerlessCredentialReadable(reader, tenantId)];", "return [userId, tenantId, true];")],
 'GM3_userId_gate_dropped': [(OWN, "  if (claim(user?.userId) === null) return false;\n  if (!owner || owner.userId === null) return ownerlessCredentialReadable",
                                    "  if (!owner || owner.userId === null) return ownerlessCredentialReadable")],
 'GM4_sql_ownerless_tenant_compare_dropped': [(REPO, "` AND NULLIF(created_by_tenant_id, '') = $2::text))`", "` AND $2::text IS NOT NULL))`")],
 'GM5_sql_ownerless_nullif_dropped': [(REPO, "` OR ($3::boolean AND NULLIF(created_by_user_id, '') IS NULL`", "` OR ($3::boolean AND created_by_user_id IS NULL`")],
 'GM6_js_tenant_compare_case_folded': [(OWN, "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;",
                                              "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null && claim(user?.tenantId)?.toLowerCase() === rowTenantId.toLowerCase();")],
 'GM7_platform_admin_role_admitted': [(OWN, "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null",
                                             "if (role === null || !(isPlatformRole(role) || role.toUpperCase() === 'PLATFORM_ADMIN')) return false;\n  return rowTenantId !== null")],
 'GM8_owned_row_tenant_ignored': [(OWN, "  if (!owner || owner.userId === null) return ownerlessCredentialReadable(req, owner?.tenantId ?? null);\n  return mayRead(req, owner);",
                                         "  if (!owner || owner.userId === null) return ownerlessCredentialReadable(req, owner?.tenantId ?? null);\n  return owner.userId === claim(user?.userId);")],
 'GM9_role_trimmed': [(OWN, "const role = claim(user?.role);\n  if (role === null || !isPlatformRole(role)) return false;",
                             "const role = claim(typeof user?.role === 'string' ? (user.role as string).trim() : user?.role);\n  if (role === null || !isPlatformRole(role)) return false;")],
}
only = sys.argv[1:] or list(M)
res = {}
for name in only:
    edits = M[name]
    with R.swapped(edits):
        rc, cells = R.vitest(R.FILES, 'mut_' + name)
    with R.swapped(edits):
        prc, pst = R.probe('mut_' + name, 'g66boot')
    red = sorted(k for k, v in cells.items() if v != 'passed')
    pred = sorted(k for k, v in pst.items() if v != 'passed')
    res[name] = {'pr_cells': len(cells), 'pr_red': len(red), 'pr_red_names': red, 'probe_cells': len(pst), 'probe_red': len(pred), 'probe_red_names': pred}
    print(name, 'PR', len(red), '/', len(cells), 'probe', len(pred), '/', len(pst), flush=True)
    json.dump(res, open(R.G + '/evidence/own_mutants.json', 'w'), indent=1)
