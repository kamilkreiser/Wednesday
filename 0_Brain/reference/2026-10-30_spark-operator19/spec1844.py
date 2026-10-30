# KS-1844: originate certifications.ts GET /:id catch reads a thrown value unguarded. Spark operator 19. code_patch2: ONE product file (2 edit points, one hunk) + 1 NEW jest file.
P='Blockchain/Dev/services/originate/src/routes/certifications.ts'
TP='Blockchain/Dev/services/originate/src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts'
OLD1=("      const pgCode = (error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code;\n"
"      if (pgCode === '22P02' || (error instanceof Error && error.message.includes('22P02'))) {\n")
NEW1=("      // KS-1844: the reads below touch the thrown value itself (`code`, `meta.code`, `instanceof`, `message`). A revoked Proxy, or an Error whose getter throws, made one of them throw out of this catch,\n"
"      // and on an async Express 4 handler that left the request with no answer. A value that cannot be read is not a 22P02 and falls through to the constant 500 below.\n"
"      let invalidId = false;\n"
"      try {\n"
"        const thrownCode = (error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code;\n"
"        invalidId = thrownCode === '22P02' || (error instanceof Error && error.message.includes('22P02'));\n"
"      } catch {\n"
"        invalidId = false;\n"
"      }\n"
"      if (invalidId) {\n")
OLD2="      logger.error('Failed to get certification', { error: error instanceof Error ? error.message : String(error) });\n"
NEW2=("      let reason: string;\n"
"      try {\n"
"        reason = error instanceof Error ? error.message : String(error);\n"
"      } catch {\n"
"        reason = 'unreadable thrown value';\n"
"      }\n"
"      logger.error('Failed to get certification', { error: reason });\n")
TEST='''/**
 * KS-1844 - GET /api/certifications/:id: the catch must survive a thrown value it cannot read.
 *
 * The handler's catch read `code`, `meta.code`, `error instanceof Error` and `error.message` straight off the thrown value with no
 * try of its own. A revoked Proxy (every property read and `instanceof` throw), or an Error whose `code` or `message` getter throws,
 * therefore threw inside the catch of an async Express 4 handler, and the request got NO answer. A request with no answer in 1500 ms
 * is reported here as the string NO ANSWER, so a hang is a red assertion and not a stuck run. The controls pin what must not change:
 * the three readable 22P02 shapes still answer 404, and an ordinary Error still answers the constant 500 and is logged by message.
 */
const mockGetCertification = jest.fn();
const mockSaveCertification = jest.fn(async (..._a: unknown[]) => undefined);
const mockGetShares = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockGetLineageEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockCreateChargeEvent = jest.fn(async (..._a: unknown[]) => ({ id: 'charge-new', eventType: 'evidence_export' }));
const mockGetChargeEvents = jest.fn(async (..._a: unknown[]) => [] as unknown[]);
const mockLog = { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() };

jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: (...a: unknown[]) => mockGetCertification(...a),
  saveCertification: (...a: unknown[]) => mockSaveCertification(...a),
  listCertifications: jest.fn(),
  saveShare: jest.fn(),
  getSharesByCertification: (...a: unknown[]) => mockGetShares(...a),
  getLineageEvents: (...a: unknown[]) => mockGetLineageEvents(...a),
  deleteCertification: jest.fn(),
  reserveCertificationRow: jest.fn(),
}));
jest.mock('../db', () => ({
  prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 1), $executeRawUnsafe: jest.fn() },
}));
jest.mock('../services/chargeEvents', () => ({
  createChargeEvent: (...a: unknown[]) => mockCreateChargeEvent(...a),
  getChargeEventsByCertification: (...a: unknown[]) => mockGetChargeEvents(...a),
}));
jest.mock('../utils/notificationClient', () => ({
  notifyDocumentCertified: jest.fn(async () => undefined),
  notifyDocumentRevoked: jest.fn(async () => undefined),
  notifyDocumentShared: jest.fn(async () => undefined),
}));
jest.mock('../events', () => ({
  publishEvent: jest.fn(async () => undefined),
  EventTypes: { CERTIFICATION_ISSUED: 'certification.issued' },
}));
jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(),
  saveDocument: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  generateContentHash: jest.fn(() => 'hash'),
}));
let testUser: Record<string, unknown> | null = null;
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = testUser; next(); },
}));
jest.mock('../utils/logger', () => ({ logger: mockLog }));

import express from 'express';
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-0000000000aa';
const CERT_ID = 'aaaaaaaa-1111-4111-8111-111111111111';

const app = express();
app.use((req: any, _res: unknown, next: () => void) => { req.tenantId = TENANT; next(); });
app.use('/api/certifications', express.json(), certificationsRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;
beforeAll(async () => {
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});
afterAll(() => { server?.close(); });

beforeEach(() => {
  jest.clearAllMocks();
  testUser = null;
});

type Answer = { status: number | string; code?: string };

// What GET /api/certifications/:id answers when getCertification rejects with `thrown`: the status and the error code of the envelope, or NO ANSWER after 1500 ms.
async function answerFor(thrown: unknown): Promise<Answer> {
  mockGetCertification.mockRejectedValueOnce(thrown);
  try {
    const res = await fetch(`${baseUrl}/api/certifications/${CERT_ID}`, { signal: AbortSignal.timeout(1500) });
    const body = (await res.json()) as { error?: { code?: string } };
    return { status: res.status, code: body.error?.code };
  } catch {
    return { status: 'NO ANSWER' };
  }
}

const revokedProxy = (): object => {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
};
const throwingGetter = (name: 'code' | 'message'): object =>
  Object.defineProperty(new Error('ks1844 getter'), name, {
    get(): string {
      throw new Error(`ks1844 ${name} getter threw`);
    },
  });

describe('KS-1844 GET /api/certifications/:id survives a thrown value it cannot read', () => {
  it('RED KS-1844 D1 a revoked Proxy from getCertification is answered with the constant 500', async () => {
    expect(await answerFor(revokedProxy())).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
  });

  it('RED KS-1844 D2 an Error whose code getter throws is answered with the constant 500', async () => {
    expect(await answerFor(throwingGetter('code'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
  });

  it('RED KS-1844 D3 an Error whose message getter throws is answered with the constant 500', async () => {
    expect(await answerFor(throwingGetter('message'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
  });

  it('CONTROL KS-1844 C1 a bare pg code 22P02 on the thrown value is still answered 404 NOT_FOUND', async () => {
    expect(await answerFor(Object.assign(new Error('invalid input syntax for type uuid'), { code: '22P02' }))).toEqual({ status: 404, code: 'NOT_FOUND' });
  });

  it('CONTROL KS-1844 C2 a 22P02 only in meta.code (no own code) is still answered 404 NOT_FOUND', async () => {
    expect(await answerFor(Object.assign(new Error('Raw query failed'), { meta: { code: '22P02' } }))).toEqual({ status: 404, code: 'NOT_FOUND' });
  });

  it('CONTROL KS-1844 C3 a 22P02 only inside the message text is still answered 404 NOT_FOUND', async () => {
    expect(await answerFor(new Error('Raw query failed. Code: `22P02`. Message: invalid input syntax for type uuid'))).toEqual({ status: 404, code: 'NOT_FOUND' });
  });

  it('CONTROL KS-1844 C4 an ordinary Error is still answered with the constant 500 and logged by its message', async () => {
    expect(await answerFor(new Error('ks1844 ordinary'))).toEqual({ status: 500, code: 'INTERNAL_ERROR' });
    expect(mockLog.error).toHaveBeenCalledWith('Failed to get certification', { error: 'ks1844 ordinary' });
  });
});
'''
S=dict(dir='ks_1844_p1_get_cert_hostile_throw',ticket='KS-1844',
 title="originate routes/certifications.ts GET /:id: the catch reads code, meta.code, instanceof and message off the thrown value unguarded, so a hostile throw gets no answer (KS-1844): read them inside a try (RUNG 3, code_patch2: one product file, two edit points in one hunk + one NEW jest file)",
 intro="DRAFT by Spark operator 19 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / originate) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1844 (found while building KS-1798; sibling of the KS-1798 gdpr fix and KS-1780). The fix is a defensive try around reads that only ever NARROW to the constant 500 for a value that cannot be read; behaviour for every readable thrown value is unchanged (controls C1-C4). Link the PR as Refs KS-1844, never a close-word. certifications.ts is touched by no open PR (checked 2026-10-30 against the GitHub pulls API per-PR file lists).",
 products=[(P,[(OLD1,NEW1),(OLD2,NEW2)])],
 prodnote=['product, modified in place: ONE hunk, two edit points in the `catch` of `GET /:id`: the first two lines of the catch body replaced by a commented try/catch that sets `invalidId`, and the `logger.error` line replaced by a guarded `reason`'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, jest, given in full below; 7 cells (3 red, 4 control); the real router on a loopback listener with the repository mocked, harness copied from ks1695'],
 runner='jest` (`npx jest src/__tests__/ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` from `Blockchain/Dev/services/originate',
 tier='code_patch2', rung='3 (two files: a product file with one hunk, a new test given whole)',
 pins='''# code_patch2: originate routes/certifications.ts (1 hunk, 2 edit points) + a NEW jest file; ref = ks1695 (the harness this file's mocks are copied from); line = the first changed line in the FIRST product.
tier=code_patch2
ref=Blockchain/Dev/services/originate/src/__tests__/ks1695-certification-reads-need-issuer-holder-or-admin.test.ts
line=1073
ctx=65536
''',
 wrong="The catch of `GET /api/certifications/:id` (`routes/certifications.ts`, handler at :1020, catch at :1065) reads the thrown value without any guard: `(error as { code?: string })?.code ?? (error as { meta?: { code?: string } })?.meta?.code` (:1073), `error instanceof Error && error.message.includes('22P02')` (:1074) and, for the log line, `error instanceof Error ? error.message : String(error)` (:1077). A thrown value whose property read throws (a revoked Proxy: every read AND `instanceof` throw; an Error whose `code` or `message` getter throws) throws inside the catch. The handler is `async` on Express 4, which does not forward a rejected handler promise, so the request gets no answer at all (the same mechanism KS-1798 measured on the gdpr routes). Fix: do the classification reads inside a `try` that falls to `invalidId = false`, and the log-line read inside a second `try` that falls to a fixed text, so a value that cannot be read gets the constant 500 below. Behaviour for every readable thrown value is unchanged.",
 where="- `services/originate/src/routes/certifications.ts:1073-1074` - **must change**: the two lines `      const pgCode = (error as { code?: string })?.code ?? ...` and `      if (pgCode === '22P02' || (error instanceof Error && error.message.includes('22P02'))) {` become the commented try/catch plus `      if (invalidId) {` (byte-exact in the diff below). The 404 `return` (:1075) and its closing `}` (:1076) are NOT touched.\n- `certifications.ts:1077` - **must change**: the `logger.error(...)` line becomes a guarded `reason` plus `logger.error('Failed to get certification', { error: reason });`.\n- `:1078` (the 500 response) and everything outside the catch of `GET /:id` - (correct, STAYS). The other `extractPgCode` use at :926 is NOT touched.",
 exactnote="ONE product hunk with two edit points (the second three lines below the first). The replaced 404 branch keeps its original body lines as context. The first comment is two physical lines.\n",
 donot="**Do NOT touch** the 404 `return` line, the 500 response line, the handler's `try` body, any other route's catch, `utils/pgErrors.ts`, or any other file.",
 testnote2="The test section is a NEW jest file given whole. The `+` lines are byte-exact. The mock block (lines 1-65) is copied from `ks1695-certification-reads-need-issuer-holder-or-admin.test.ts` on purpose: it is the known-good way to load the real router; do not trim it. No top-level await.",
 red=['RED KS-1844 D1','RED KS-1844 D2','RED KS-1844 D3'],
 cells="- RED `D1` (revoked Proxy), `D2` (Error with a throwing `code` getter), `D3` (Error with a throwing `message` getter): at the tip the request gets NO answer in 1500 ms (reported as `NO ANSWER`), an assertion red; after the edit all answer 500 with `error.code` `INTERNAL_ERROR`.\n- GREEN at the tip and after: `C1` (bare `code` 22P02 -> 404 NOT_FOUND), `C2` (`meta.code` 22P02 with no own `code` -> 404), `C3` (22P02 only in the message text -> 404), `C4` (an ordinary Error -> 500 INTERNAL_ERROR and `logger.error('Failed to get certification', { error: 'ks1844 ordinary' })`).",
 premises="- `certifications.ts:1065` (`} catch (error) {`), :1073 (the `pgCode` line), :1074 (the `if`), :1077 (the `logger.error`), :1078 (the 500) are as quoted, read at the tip by script; the golden is generated from the tree at the tip, not typed.\n- `extractPgCode` (`utils/pgErrors.ts:52`) is already import-ed in the file (:58) and is NOT used by this fix, to keep the 22P02 matching exactly as it is (`includes('22P02')` on the message, not the word-bounded regex).\n- The ks1695 harness (`getCertification` mocked, real router on a loopback port, `req.tenantId` set by a middleware, auth mocked) loads the router without a database; `GET /:id` calls `getCertification` before any other repository call.",
 unmeasured="- The drafter did NOT run the new file; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- Whether `getCertification` can throw a non-Error value at all in production (the ticket says it cannot be sent from outside; priority 4).\n- Whether an unhandled rejection in the red state is reported by jest as a failure of its own beyond the assertion (the KS-1798 cells D1-D3 use the same pattern and passed their control).\n- Measured by the first control run (a harness finding, not changed by this brief): a Prisma-shaped error with BOTH `code: 'P2010'` and `meta.code: '22P02'` and no 22P02 in its message is answered 500 at the tip, because `a ?? b` takes the non-nullish `'P2010'`. C2 therefore uses an error with `meta.code` only. The fix keeps that behaviour byte for byte (the expression is unchanged inside the try).\n- Other originate catches that read a thrown value (KS-1780's census was 17): not touched.",
 scope="**KS-1844 only (the `GET /:id` catch in certifications.ts).** Link the PR as Refs KS-1844, never a close-word. Not an auth/token surface; it only narrows to the constant 500 for an unreadable value.",
)
