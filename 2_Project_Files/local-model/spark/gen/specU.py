P='Blockchain/Dev/services/timestamping/src/index.ts'
TP='Blockchain/Dev/services/timestamping/src/__tests__/ks1515-a-mock-tsa-reply-is-never-eidas-qualified.test.ts'
E1=("      eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;\n",
    "      eidasQualified = tsaResult.token && tsaResult.mock !== true ? tsaResult.eidasQualified === true : false;\n")
TEST='''// KS-1515 (timestamping, createTimestamp, rfc3161 branch): the TSA module's `mock` flag already decides `verified` (KS-753) but not `eidasQualified`, so a reply flagged mock that also says eidasQualified:true
// would be reported qualified and would pass a requireEidas request with 201. The real fallback hard-codes eidasQualified:false so the combination is not reachable today; this is defence in depth.
// The cells drive the real express app with the TSA module's createTimestamp answering exactly the reply under test and the database mocked (the same harness shape as ks753-mock-tsa-fallback-is-not-verified, but the TSA module is replaced whole rather than spread over the original).
import { describe, expect, it, vi, afterEach } from 'vitest';

afterEach(() => {
  vi.doUnmock('../tsa/qualified-tsa');
  vi.doUnmock('../db');
  vi.resetModules();
});

/** POST /api/timestamps through the real app; the TSA module answers exactly `reply`. */
async function post(reply: Record<string, unknown>, extra: Record<string, unknown>) {
  // A self-contained factory (no importOriginal): the real module pulls in rfc3161-verify, which needs packages a bare checkout may lack.
  vi.doMock('../tsa/qualified-tsa', () => ({
    createTimestamp: async () => ({ success: true, timestamp: new Date().toISOString(), serialNumber: 'ab', provider: 'P', ...reply }),
    selectTSAProvider: () => ({ name: 'Test TSA', url: 'https://tsa.test.invalid' }),
    verifyTimestamp: async () => ({ valid: true }),
  }));
  const nodeCrypto = await import('crypto');
  const { privateKey, publicKey } = nodeCrypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
  const b64url = (s: string | Buffer) => Buffer.from(s).toString('base64url');
  const signingInput = b64url(JSON.stringify({ alg: 'RS256', typ: 'JWT' })) + '.' + b64url(JSON.stringify({ userId: 'u-ks1515', email: 'ks1515@secuura.io', role: 'user', verificationLevel: 'email', exp: Math.floor(Date.now() / 1000) + 300 }));
  const bearer = 'Bearer ' + signingInput + '.' + b64url(nodeCrypto.sign('sha256', Buffer.from(signingInput), privateKey));
  const saved = { JWT_PUBLIC_KEY: process.env.JWT_PUBLIC_KEY, PORT: process.env.PORT };
  process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
  process.env.PORT = '0';
  vi.doMock('../db', () => ({ initDb: async () => true, isDbAvailable: () => true, query: async () => ({ rows: [], rowCount: 0 }), closeDb: async () => undefined }));
  vi.resetModules();
  const { default: app } = await import('../index');
  const out = await new Promise<any>((resolve) => {
    const headers: Record<string, unknown> = {};
    const req: any = { method: 'POST', url: '/api/timestamps', headers: { authorization: bearer }, body: { hash: 'a'.repeat(64), timestampType: 'rfc3161', ...extra } };
    const res: any = { statusCode: 200, locals: {}, on: () => res, status: (c: number) => { res.statusCode = c; return res; }, json: (b: unknown) => { resolve({ status: res.statusCode, body: b }); return res; } };
    res.send = res.json; res.end = () => res.json(null);
    res.setHeader = (k: string, v: unknown) => { headers[k.toLowerCase()] = v; return res; };
    res.getHeader = (k: string) => headers[k.toLowerCase()]; res.removeHeader = (k: string) => { delete headers[k.toLowerCase()]; };
    app(req, res, () => resolve({ status: -1, body: null }));
  });
  for (const k of ['JWT_PUBLIC_KEY', 'PORT'] as const) { if (saved[k] === undefined) delete process.env[k]; else process.env[k] = saved[k]; }
  return out;
}

describe('KS-1515: a TSA reply flagged mock is never reported eIDAS-qualified', () => {
  it('RED KS-1515 R1 a mock reply that claims eidasQualified:true answers 201 with eidasQualified false and verified false', async () => {
    const r = await post({ token: 'bW9jaw==', tsaName: 'Ordinary TSA', eidasQualified: true, mock: true }, {});
    expect([r.status, r.body.data.eidasQualified, r.body.data.verified]).toEqual([201, false, false]);
  });

  it('RED KS-1515 R2 the same reply with requireEidas:true is refused with 503 QUALIFIED_TSA_UNAVAILABLE', async () => {
    const r = await post({ token: 'bW9jaw==', tsaName: 'Ordinary TSA', eidasQualified: true, mock: true }, { requireEidas: true });
    expect([r.status, r.body.error?.code]).toEqual([503, 'QUALIFIED_TSA_UNAVAILABLE']);
  });

  it('control KS-1515 C1 a REAL qualified token (no mock flag) stays eidasQualified true and verified true', async () => {
    const r = await post({ token: 'cmVhbC10b2tlbg==', tsaName: 'Real TSA', eidasQualified: true }, {});
    expect([r.status, r.body.data.eidasQualified, r.body.data.verified]).toEqual([201, true, true]);
  });

  it('control KS-1515 C2 a REAL qualified token with requireEidas:true is still accepted (201)', async () => {
    const r = await post({ token: 'cmVhbC10b2tlbg==', tsaName: 'Real TSA', eidasQualified: true }, { requireEidas: true });
    expect([r.status, r.body.data.eidasQualified]).toEqual([201, true]);
  });

  it('control KS-1515 C3 a REAL non-qualified token stays eidasQualified false and verified true', async () => {
    const r = await post({ token: 'cmVhbC10b2tlbg==', tsaName: 'Real Non-eIDAS TSA', eidasQualified: false }, {});
    expect([r.status, r.body.data.eidasQualified, r.body.data.verified]).toEqual([201, false, true]);
  });
});
'''
S=dict(dir='ks_1515_p2',ticket='KS-1515',
 title='Timestamping: a TSA reply flagged mock must force eidasQualified false, so requireEidas refuses it (KS-753 gate m1) (RUNG 2, code_patch: one line + one NEW app-driving vitest file)',
 intro="DRAFT by a Spark brief drafter for Wednesday, batch 5 of 2026-10-28 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. The ticket states the exact line; defence in depth, not reachable today.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, one line replaced'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control; drives the real express app, the TSA module and the database mocked)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1515-a-mock-tsa-reply-is-never-eidas-qualified.test.ts` from `Blockchain/Dev/services/timestamping',
 tier='code_patch', rung='2 (one line byte-exact; the new test given whole)',
 pins='''# code_patch, ONE line in timestamping src/index.ts + a NEW vitest file; ref = the ks753 spec (same harness shape); line = the changed line.
tier=code_patch
ref=Blockchain/Dev/services/timestamping/src/__tests__/ks753-mock-tsa-fallback-is-not-verified.test.ts
line=469
ctx=65536
''',
 wrong="In `createTimestamp` (rfc3161 branch) of `services/timestamping/src/index.ts`, `:469` sets `eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;`. The TSA module's `mock` flag decides `verified` on the next line (KS-753) but not `eidasQualified`, so a reply `{ token, mock: true, eidasQualified: true }` is reported qualified and, with `requireEidas: true`, answers 201 instead of 503. The change adds the mock flag to the condition on that one line: `tsaResult.token && tsaResult.mock !== true ? tsaResult.eidasQualified === true : false`. For every reply without `mock: true` the result is unchanged.",
 where="- `src/index.ts:469` - **must change**: the single line `eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;` (inside `case 'rfc3161'`, after the KS-523 comment) gains `&& tsaResult.mock !== true` after `tsaResult.token`. Nothing else on the line changes.\n- Every other line of the file, including the `verified` line below it, is NOT touched.",
 exactnote="ONE hunk: one line removed, one line added.\n",
 donot="**Do NOT touch** any other line of `index.ts`, or any other file.",
 testnote2="A NEW file, given whole. Its `+` lines are the entire file, byte for byte. Pure ASCII, vitest imports, no top-level await. It copies the harness of the existing `ks753-mock-tsa-fallback-is-not-verified.test.ts` (real express app driven with fake req/res, `../tsa/qualified-tsa` and `../db` mocked with `vi.doMock`), except that the TSA mock is a whole replacement, not `importOriginal`.",
 red=['RED KS-1515 R1','RED KS-1515 R2'],
 cells="- RED `R1`: at the tip the mock reply answers 201 with `eidasQualified: true`; after the edit `false`.\n- RED `R2`: at the tip `requireEidas: true` with the mock reply answers 201; after the edit 503 `QUALIFIED_TSA_UNAVAILABLE` (index.ts:244-245).\n- CONTROL `C1` to `C3`: green at the tip AND after (real tokens: qualified stays true, requireEidas still accepted, non-qualified stays false).",
 premises="- `src/index.ts:469` is the line quoted above and the only line in the file containing `eidasQualified = tsaResult` (read at the tip).\n- `tsaResult.mock` is already read two lines below (`if (tsaResult.mock === true || !tsaResult.token) verified = false;`), so the property type-checks.\n- The route maps `QualifiedTsaUnavailableError` to 503 `QUALIFIED_TSA_UNAVAILABLE` (index.ts:244-245); `requireEidas` is accepted by `createTimestampSchema` (schemas.ts:35).\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- The ticket says the combination is not reachable today (`tsa/qualified-tsa.ts:333` hard-codes eidasQualified:false); the cells inject it through the TSA-module mock.\n- Open PRs touching this file: none by the file lists of every open PR read on 2026-10-28.",
 scope="**Closes KS-1515** (one line plus the cells the ticket asks for). Link the PR as Refs KS-1515 until the QA gate has passed.",
)
