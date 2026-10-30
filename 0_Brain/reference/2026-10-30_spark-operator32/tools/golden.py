import sys,os
T='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-30_spark-operator32/clone/Blockchain/Dev/services/api-gateway/src/__tests__/'
E={
'ks1374':[('ks1374-global-limiter-at-demo-limit.test.ts',"    const body = await r.json();\n    expect(r.status).toBe(429);\n    expect(body.error.code).toBe('RATE_LIMIT_EXCEEDED');","    const body = (await r.json()) as { error: { code: string } };\n    expect(r.status).toBe(429);\n    expect(body.error.code).toBe('RATE_LIMIT_EXCEEDED');")],
'ks695':[('ks695-ask3-erase-connector-door.test.ts',"warn.mock.calls.filter((c) => String(c[0]).includes('KS-843'))","warn.mock.calls.filter((c: unknown[]) => String(c[0]).includes('KS-843'))")],
'ks1464':[('ks1464-limiter-key-hygiene.test.ts',"warn.mock.calls.map((c) => String(c[0])).filter((l) => l.includes('has no rateLimit'))","warn.mock.calls.map((c: unknown[]) => String(c[0])).filter((l: string) => l.includes('has no rateLimit'))")],
'ks1457':[('ks1457-audit-finish-reads-use-the-entry-path.test.ts',"type LogMock = Mock<(level: string, msg: string, ctx?: Record<string, unknown>) => void>;\n","type LogMock = Mock<(level: string, msg: string, ctx?: Record<string, unknown>) => void>;\ntype AuditLog = Parameters<typeof createAuditMiddleware>[0]['log'];\n"),
 ('ks1457-audit-finish-reads-use-the-entry-path.test.ts',"isDbAvailable: () => true, log: opts.log }));","isDbAvailable: () => true, log: opts.log as unknown as AuditLog }));"),
 ('ks1457-audit-finish-reads-use-the-entry-path.test.ts',"isDbAvailable: () => true, log: makeLog() }));","isDbAvailable: () => true, log: makeLog() as unknown as AuditLog }));")],
'ks1165':[('ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts',"const { protect } = createCsrfMiddleware();","const protect = createCsrfMiddleware().protect as (req: Request, res: Response, next: unknown) => void;"),
 ('ks1165-api-gateway-csrf-excludedpaths-carries-no.test.ts',"expect((await other.json()).error.code).toBe('CSRF_TOKEN_MISSING');","expect(((await other.json()) as { error: { code: string } }).error.code).toBe('CSRF_TOKEN_MISSING');")],
'csrf':[('csrf.test.ts',"const { protect } = createCsrfMiddleware();","const protect = createCsrfMiddleware().protect as (req: Request, res: Response, next: unknown) => void;")],
'rate':[('rateLimitEnforce.test.ts',"import { describe, it, expect, vi } from 'vitest';","import { describe, it, expect, vi } from 'vitest';\nimport type { Response } from 'express';"),
 ('rateLimitEnforce.test.ts',"function makeRes(): MockRes {","function makeRes(): MockRes & Response {"),
 ('rateLimitEnforce.test.ts',"  return res;\n}\n\n// In-memory","  return res as unknown as MockRes & Response;\n}\n\n// In-memory")],
}
for k in sys.argv[1:]:
    for f,o,n in E[k]:
        s=open(T+f).read(); c=s.count(o)
        assert c==1,(k,o,c); s=s.replace(o,n)
        open(T+f,'w').write(s)
print('applied',sys.argv[1:])
