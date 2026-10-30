# KS-1515: timestamping createTimestamp: a TSA reply flagged mock must force eidasQualified false. Spark operator 19. code_patch2: ONE product line replaced + 1 NEW vitest file.
P='Blockchain/Dev/services/timestamping/src/index.ts'
TP='Blockchain/Dev/services/timestamping/src/__tests__/ks1515-a-mock-tsa-reply-is-never-eidas-qualified.test.ts'
OLD="      eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;\n"
NEW=("      // KS-1515: the `mock` flag decides `verified` on the next line, so it must also decide the qualification: a reply flagged mock can never count as eIDAS-qualified, or `requireEidas` would let it through.\n"
"      eidasQualified = tsaResult.token && tsaResult.mock !== true ? tsaResult.eidasQualified === true : false;\n")
TEST='''/**
 * =============================================================================
 * KS-1515 - a TSA reply flagged `mock` must never count as eIDAS-qualified (KS-753 gate m1)
 * =============================================================================
 * `createTimestamp` (index.ts) decides `verified` from the TSA reply's explicit `mock` flag (KS-753) but took `eidasQualified`
 * from the reply's own `eidasQualified` field. A reply flagged `mock: true` that also carried `eidasQualified: true` therefore
 * answered 201 with `eidasQualified: true`, and with `requireEidas: true` it answered 201 instead of 503, so a mock reply could
 * pass the `requireEidas` gate. Not reachable today (the real fallback hard-codes `eidasQualified: false`); this pins the
 * defence in depth. The TSA module is replaced by a stub that answers exactly the reply given; the real express app is driven
 * with a signed bearer token and the database mocked as available.
 * =============================================================================
 */
import { describe, expect, it, vi, afterEach } from 'vitest';

afterEach(() => {
  vi.doUnmock('../tsa/qualified-tsa');
  vi.doUnmock('../db');
  vi.resetModules();
});

/** A TSA module whose createTimestamp answers exactly `reply`; everything else is the real module. */
function mockTsa(reply: Record<string, unknown>) {
  vi.doMock('../tsa/qualified-tsa', async (importOriginal) => {
    const actual = await importOriginal<Record<string, unknown>>();
    return { ...actual, createTimestamp: async () => ({ success: true, timestamp: new Date().toISOString(), serialNumber: 'ab', provider: 'P', ...reply }) };
  });
}

/** POST /api/timestamps (rfc3161) against the real app with the database available; returns the status and the body. */
async function post(extra: Record<string, unknown>): Promise<{ status: number; body: any }> {
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
  const out = await new Promise<{ status: number; body: any }>((resolve) => {
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

const MOCK_TOKEN = Buffer.from(JSON.stringify({ mock: true })).toString('base64');
const REAL_TOKEN = 'cmVhbC10b2tlbg==';

describe('KS-1515 - the mock flag decides eidasQualified, not only verified', () => {
  it('RED KS-1515 Q1 a reply flagged mock that claims eidasQualified:true is answered 201 with eidasQualified false', async () => {
    mockTsa({ token: MOCK_TOKEN, tsaName: 'Ordinary TSA', eidasQualified: true, mock: true });
    const r = await post({});
    expect([r.status, r.body.data.eidasQualified, r.body.data.verified]).toEqual([201, false, false]);
  });

  it('RED KS-1515 Q2 the same reply with requireEidas:true is refused with 503 QUALIFIED_TSA_UNAVAILABLE', async () => {
    mockTsa({ token: MOCK_TOKEN, tsaName: 'Ordinary TSA', eidasQualified: true, mock: true });
    const r = await post({ requireEidas: true });
    expect([r.status, r.body.error?.code]).toEqual([503, 'QUALIFIED_TSA_UNAVAILABLE']);
  });

  it('CONTROL KS-1515 Q3 a real token that is eidasQualified:true stays qualified and verified', async () => {
    mockTsa({ token: REAL_TOKEN, tsaName: 'Real TSA', eidasQualified: true });
    const r = await post({});
    expect([r.status, r.body.data.eidasQualified, r.body.data.verified]).toEqual([201, true, true]);
  });

  it('CONTROL KS-1515 Q4 a real qualified token with requireEidas:true is still accepted', async () => {
    mockTsa({ token: REAL_TOKEN, tsaName: 'Real TSA', eidasQualified: true });
    const r = await post({ requireEidas: true });
    expect([r.status, r.body.data.eidasQualified]).toEqual([201, true]);
  });

  it('CONTROL KS-1515 Q5 a real token from a non-qualified provider is still not qualified, and requireEidas still refuses it', async () => {
    mockTsa({ token: REAL_TOKEN, tsaName: 'Real Non-eIDAS TSA', eidasQualified: false });
    const plain = await post({});
    expect([plain.status, plain.body.data.eidasQualified, plain.body.data.verified]).toEqual([201, false, true]);
    mockTsa({ token: REAL_TOKEN, tsaName: 'Real Non-eIDAS TSA', eidasQualified: false });
    const strict = await post({ requireEidas: true });
    expect(strict.status).toBe(503);
  });
});
'''
S=dict(dir='ks_1515_p1_mock_reply_not_qualified',ticket='KS-1515',
 title="timestamping src/index.ts createTimestamp: a TSA reply flagged mock must force eidasQualified false, so requireEidas refuses it (KS-1515, KS-753 gate m1): one line plus one NEW vitest file (RUNG 3, code_patch2)",
 intro="DRAFT by Spark operator 19 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / timestamping) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1515 (Opus QA gate of PR 1502, finding m1; Wednesday ruled P3 on 2026-10-12). The ticket spells out the fix line. **The change only REFUSES more** (a mock reply can no longer count as qualified); it is defence in depth, not reachable today because the real fallback hard-codes `eidasQualified: false` (`tsa/qualified-tsa.ts:333`). eIDAS qualification gates `requireEidas`: the raise PR should name that for the gate. Link the PR as Refs KS-1515, never a close-word. No open PR touches services/timestamping source or tests (only a package.json in PRs 575 and 649).",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: ONE hunk, the one `eidasQualified = ...` line at :469 replaced by a one-line comment plus the same line with `&& tsaResult.mock !== true`'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control); the real express app driven in-process with the TSA module stubbed, harness copied from ks753'],
 runner='vitest` (`npx vitest run src/__tests__/ks1515-a-mock-tsa-reply-is-never-eidas-qualified.test.ts` from `Blockchain/Dev/services/timestamping',
 tier='code_patch2', rung='3 (two files: a product file with one hunk, a new test given whole)',
 pins='''# code_patch2: timestamping src/index.ts (1 hunk) + a NEW vitest file; ref = ks753 (the harness this file's helpers are copied from); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/timestamping/src/__tests__/ks753-mock-tsa-fallback-is-not-verified.test.ts
line=469
ctx=65536
''',
 wrong="`createTimestamp` (`services/timestamping/src/index.ts:437`), in its `rfc3161` case, derives `verified` from the TSA reply's `mock` flag (`:470`, `if (tsaResult.mock === true || !tsaResult.token) verified = false;`, KS-753) but derives `eidasQualified` only from the reply's own field: `:469` `eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;`. A reply flagged `mock: true` that also carries `eidasQualified: true` therefore answers 201 with `eidasQualified: true`, and with `requireEidas: true` (`:501`, `if (data.requireEidas && !eidasQualified) throw new QualifiedTsaUnavailableError(...)`, mapped to 503 at :244) it answers 201 instead of 503, so a mock reply could pass the `requireEidas` gate. Fix: the same line also requires `tsaResult.mock !== true`. Behaviour for every real token (no mock flag) and for the no-token case is unchanged.",
 where="- `services/timestamping/src/index.ts:469` - **must change**: the one line `      eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false;` is replaced by a one-line comment and the same line with `tsaResult.token && tsaResult.mock !== true ?` (byte-exact in the diff below).\n- `:466-468` (the existing KS-523 comment above it), `:470` (the `verified` line), `:501-507` (the `requireEidas` refusal) and the route's 503 mapping at `:244` - (correct, STAY).",
 exactnote="ONE product hunk. The new comment line goes between the existing three-line KS-523 comment and the changed line.\n",
 donot="**Do NOT touch** the `verified` line, the `requireEidas` check, `tsa/qualified-tsa.ts`, the batch path, or any other line of `index.ts`; no other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It imports from `vitest`, stubs the TSA module with `vi.doMock`, and has no top-level await. The helpers are copied from `ks753-mock-tsa-fallback-is-not-verified.test.ts` on purpose: they are the known-good way to drive the real app in-process; do not trim them.",
 red=['RED KS-1515 Q1','RED KS-1515 Q2'],
 cells="- RED `Q1`: at the tip a reply `{ token, mock: true, eidasQualified: true }` answers 201 with `eidasQualified` true (the cell expects false) and `verified` false. RED `Q2`: the same reply with `requireEidas: true` answers 201 at the tip (the cell expects 503 QUALIFIED_TSA_UNAVAILABLE).\n- GREEN at the tip and after: `Q3` (a real qualified token stays qualified and verified), `Q4` (a real qualified token with requireEidas is accepted), `Q5` (a real non-qualified token: 201 not qualified but verified, and 503 under requireEidas).\n- After the edit all five are green.",
 premises="- `index.ts:466-468` (the KS-523 comment), :469 (the line), :470 (`verified`), :501 (the `requireEidas` check) and the 503 mapping at :244 are as quoted, read at the tip by script; the golden is generated from the tree at the tip, not typed.\n- `formatTimestampResponse` carries `eidasQualified` and `verified` into `data` (index.ts:817 for `eidasQualified`); the ks753 cells read `body.data.verified` the same way.\n- `mock` is an explicit field the TSA module sets on its own fallback (`tsa/qualified-tsa.ts`, KS-753); the ks753 test file stubs it exactly so.",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- Whether `body.data.eidasQualified` is the name the response uses at the tip: read from the ticket and `index.ts:817` (`eidasQualified: timestamp.eidasQualified`), not run.\n- The batch path (`/api/timestamps/batch`) also calls `createTimestamp`; it is not driven by a cell here.\n- Whether `ks753`'s `mock` flag is ever set together with `eidasQualified:true` by the real module: the ticket says not today (`qualified-tsa.ts:333`).",
 scope="**KS-1515 only.** Link the PR as Refs KS-1515, never a close-word. The change only refuses more; name `requireEidas` for the gate.",
)
