#!/usr/bin/env python3
"""Gate 59 own mutants: apply one string replacement, run the ks1851 file (and optionally others), restore."""
import subprocess, sys, os, json, shutil
G = "/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-31_gate59-ks1851-1869"
V = f"{G}/repo/Blockchain/Dev/services/vc-issuer"
ROUTE = f"{V}/src/routes/credentials.ts"; OWN = f"{V}/src/ownership.ts"
T = "src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts"
CHECK = """    const record = await credentialRepo.getRecordById(id);
    if (!record || !mayRead(req, record.owner)) {
      throw new AppError('Credential not found', 404);
    }

    const revokedCredential = await credentialRepo.revoke(id, reason);
"""
M = [
 ("G59-M1 userId conjunct dropped (ownership.ts mayRead)", OWN,
  "return owner.userId === userId && owner.tenantId === claim(user?.tenantId);", "return owner.tenantId === claim(user?.tenantId);"),
 ("G59-M2 tenant conjunct dropped (ownership.ts mayRead)", OWN,
  "return owner.userId === userId && owner.tenantId === claim(user?.tenantId);", "return owner.userId === userId;"),
 ("G59-M3 check moved AFTER the write (route)", ROUTE, CHECK,
  """    const revokedCredential = await credentialRepo.revoke(id, reason);
    const record = await credentialRepo.getRecordById(id);
    if (!record || !mayRead(req, record.owner)) {
      throw new AppError('Credential not found', 404);
    }
"""),
 ("G59-M4 predicate deleted, existence-only check (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
 ("G59-M5 refused answers 403 (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record) throw new AppError('Credential not found', 404);\n    if (!mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 403);\n    }\n\n    const revokedCredential"),
 ("G59-M6 refused answers a different 404 message (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record) throw new AppError('Credential not found', 404);\n    if (!mayRead(req, record.owner)) {\n      throw new AppError('Credential not accessible', 404);\n    }\n\n    const revokedCredential"),
 ("G59-M7 reason logged before the check (route)", ROUTE,
  "    const record = await credentialRepo.getRecordById(id);\n    if (!record || !mayRead",
  "    logger.info('Revoke requested', { credentialId: id, reason });\n    const record = await credentialRepo.getRecordById(id);\n    if (!record || !mayRead"),
 ("G59-M8 owner-less rows always admitted (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record || (record.owner.userId !== null && !mayRead(req, record.owner))) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
 ("G59-M9 SYSTEM_ADMIN bypass added (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record || (!mayRead(req, record.owner) && (req as any).user?.role !== 'SYSTEM_ADMIN')) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
 ("G59-M10 ORG_ADMIN same-tenant bypass added (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record || (!mayRead(req, record.owner) && !((req as any).user?.role === 'ORG_ADMIN' && (req as any).user?.tenantId === record.owner.tenantId))) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
 ("G59-M11 no-principal guard removed (ownership.ts mayRead)", OWN,
  "  if (userId === null) return false;\n  if (!owner", "  if (!owner"),
 ("G59-M12 owner read via getById semantics: owner forced OWNERLESS (route)", ROUTE,
  "if (!record || !mayRead(req, record.owner)) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential",
  "if (!record || !mayRead(req, { userId: null, tenantId: null })) {\n      throw new AppError('Credential not found', 404);\n    }\n\n    const revokedCredential"),
]
env = dict(os.environ, TMPDIR=f"{G}/tmp")
results = []
for name, path, old, new in M:
    src = open(path).read()
    assert src.count(old) == 1, f"{name}: anchor count {src.count(old)}"
    shutil.copy(path, f"{G}/tmp/mut.bak")
    try:
        open(path, "w").write(src.replace(old, new))
        p = subprocess.run(["npm", "--prefix", V, "exec", "--", "vitest", "run", "--root", V, T], capture_output=True, text=True, env=env)
        out = p.stdout + p.stderr
        line = [l for l in out.splitlines() if "Tests " in l]
        results.append({"mutant": name, "rc": p.returncode, "killed": p.returncode != 0, "tests": line[-1].strip() if line else out[-300:]})
    finally:
        shutil.copy(f"{G}/tmp/mut.bak", path)
    print(json.dumps(results[-1]), flush=True)
json.dump(results, open(f"{G}/evidence/own_mutants.json", "w"), indent=1)
