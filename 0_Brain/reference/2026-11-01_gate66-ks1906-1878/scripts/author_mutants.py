#!/usr/bin/env python3
"""Gate 66 reconstruction of a SAMPLE of Seat E's named mutants (their script was not found); PR cells only."""
import sys, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate66-ks1906-1878/scripts')
import run as R
OWN = 'src/ownership.ts'; ROUTE = 'src/routes/credentials.ts'
HEAD_LINE = "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;"
M = {
 'SE_connector_admitted': [(OWN, HEAD_LINE, "if (role === null || !(isPlatformRole(role) || role === 'connector')) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;")],
 'SE_org_admin_readmitted': [(OWN, HEAD_LINE, "if (role === null || !(isPlatformRole(role) || role === 'ORG_ADMIN')) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;")],
 'SE_full_unicode_fold': [(OWN, HEAD_LINE, "if (role === null || !['SYSTEM_ADMIN','SUPER_ADMIN'].includes(role.toUpperCase())) return false;\n  return rowTenantId !== null && claim(user?.tenantId) === rowTenantId;")],
 'SE_tenant_compare_dropped': [(OWN, HEAD_LINE, "if (role === null || !isPlatformRole(role)) return false;\n  return rowTenantId !== null;")],
 'SE_byid_left_on_mayRead': [(ROUTE, "    // its tenant (ownership.ts mayReadCredential).\n    if (!record || !mayReadCredential(req, record.owner)) {", "    // its tenant (ownership.ts mayReadCredential).\n    if (!record || !mayRead(req, record.owner)) {"),
                             (ROUTE, "import { ownerOf, mayReadCredential } from '../ownership';", "import { ownerOf, mayReadCredential, mayRead } from '../ownership';")],
 'SE_revoke_left_on_mayRead': [(ROUTE, "    const record = await credentialRepo.getRecordById(id);\n    if (!record || !mayReadCredential(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
                                "    const record = await credentialRepo.getRecordById(id);\n    if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
                               (ROUTE, "import { ownerOf, mayReadCredential } from '../ownership';", "import { ownerOf, mayReadCredential, mayRead } from '../ownership';")],
}
res = {}
for name, edits in M.items():
    with R.swapped(edits):
        rc, cells = R.vitest(R.FILES, 'amut_' + name)
    red = sorted(k for k, v in cells.items() if v != 'passed')
    res[name] = {'cells': len(cells), 'red': len(red), 'red_names': red}
    print(name, len(red), '/', len(cells), flush=True)
json.dump(res, open(R.G + '/evidence/author_mutant_sample.json', 'w'), indent=1)
