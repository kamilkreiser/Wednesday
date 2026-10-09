/**
 * KS-1029 — PATCH /api/gdpr/dsr/:dsrId answers a malformed id with 404, never 500.
 * https://linear.app/secuura/issue/KS-1029
 *
 * Prior behaviour: the route passed :dsrId straight to gdprService.updateDSRStatus, whose
 * `WHERE id = ${dsrId}::uuid` cast raises 22P02 for a malformed id. Since KS-754 that function
 * rethrows a DB error (so a failed write is never reported as "no such DSR"), and the route's
 * catch answered 500 INTERNAL_ERROR. Schemathesis reproduced it on develop
 * (`not_a_server_error::PATCH /api/gdpr/dsr/{dsrId}`, dsrId=0).
 *
 * Now a non-canonical id is refused before the lookup with 404 NOT_FOUND 'DSR not found': the
 * answer GET /dsr/:dsrId already gives on the same path, a status the spec declares for this
 * route, and one Schemathesis's positive_data_acceptance accepts for a schema-valid string id
 * (400 is not in its expected statuses). The guard sits after the body checks, as it does in
 * POST /consent and POST /dsr, so a malformed id with an invalid body still gets that body's 400.
 *
 * Behaviour narrowing, deliberate: PostgreSQL's uuid input also accepts hyphenless and braced
 * forms, which used to reach a real row. UUID_PATTERN is canonical-only, so those now answer 404
 * as well (N1, N2). A canonical absent id is unchanged: 200 {success:false, 'DSR not found'}.
 *
 * Harness: ks444's (mounted router, auth passthrough) with ks754's db/logger mocks, so the real
 * updateDSRStatus and its KS-754 rethrow stay in the path. The DB mock MODELS PostgreSQL's uuid
 * input function; it is not a database.
 */

const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: { $executeRaw: mockExecuteRaw },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

jest.mock('../middleware/auth', () => ({
  // Auth/authz are not under test — pass everything through.
  authenticate: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  requireSelfOrRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  hasAnyRole: () => true,
}));

import express from 'express';
import { gdprRouter } from '../routes/gdpr';

/** A DSR that exists in the modelled table. */
const REAL_DSR_ID = '11111111-2222-4333-8444-555555555555';

/** A canonical id whose UPDATE fails at the database (53300, too_many_connections). */
const DB_ERROR_DSR_ID = 'dddddddd-dddd-4ddd-8ddd-dddddddddddd';

/** An uppercase canonical id that exists nowhere. */
const UPPERCASE_ABSENT_ID = 'AAAAAAAA-BBBB-4CCC-8DDD-EEEEEEEEEEEE';

/** A body the published DSRUpdateRequest contract accepts (Peter's Schemathesis repro body). */
const VALID_BODY = { status: 'pending', processedBy: 'example-processedBy' };

/**
 * Model of PostgreSQL's uuid input (src/backend/utils/adt/uuid.c, string_to_uuid): optional
 * braces, 32 hex digits, an optional hyphen after any even number of bytes, nothing trailing.
 *
 * @param value - the id as bound into the UPDATE.
 * @returns true when PostgreSQL's cast would accept it.
 * @example pgUuidAccepts('11111111222243338444555555555555') // true — PostgreSQL accepts hyphenless
 */
function pgUuidAccepts(value: string): boolean {
  const isHex = (c: string | undefined): boolean => c !== undefined && /^[0-9a-fA-F]$/.test(c);
  let i = 0;
  const braced = value[0] === '{';
  if (braced) i++;
  for (let byte = 0; byte < 16; byte++) {
    if (!isHex(value[i]) || !isHex(value[i + 1])) return false;
    i += 2;
    if (value[i] === '-' && byte % 2 === 1 && byte < 15) i++;
  }
  if (braced) {
    if (value[i] !== '}') return false;
    i++;
  }
  return i === value.length;
}

/**
 * The form a modelled row is stored under: lowercase hex with no hyphens or braces.
 *
 * @param value - an id PostgreSQL accepts.
 * @returns its storage form, for comparing ids across input spellings.
 * @example storedForm('{AAAAAAAA-BBBB-4CCC-8DDD-EEEEEEEEEEEE}') // 'aaaaaaaabbbb4ccc8dddeeeeeeeeeeee'
 */
function storedForm(value: string): string {
  return value.toLowerCase().replace(/[{}-]/g, '');
}

mockExecuteRaw.mockImplementation((_strings: unknown, ...values: unknown[]) => {
  // Prisma tagged template: the dsrId is the last bound value (`WHERE id = ${dsrId}::uuid`).
  const dsrId = String(values[values.length - 1]);
  if (!pgUuidAccepts(dsrId)) {
    return Promise.reject(Object.assign(new Error(`invalid input syntax for type uuid: "${dsrId}"`), { code: '22P02' }));
  }
  if (storedForm(dsrId) === storedForm(DB_ERROR_DSR_ID)) {
    return Promise.reject(Object.assign(new Error('sorry, too many clients already'), { code: '53300' }));
  }
  return Promise.resolve(storedForm(dsrId) === storedForm(REAL_DSR_ID) ? 1 : 0);
});

const app = express();
app.use('/api/gdpr', express.json(), gdprRouter);

let baseUrl = '';
let server: ReturnType<typeof app.listen> | undefined;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server?.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  if (server) server.close();
});

beforeEach(() => jest.clearAllMocks());

/** The route's two response shapes: the canonical error envelope and the 200 update result. */
interface DsrUpdateResponse {
  success?: boolean;
  message?: string;
  error?: { code?: string; message?: string };
}

/**
 * Send PATCH /api/gdpr/dsr/:dsrId with a JSON body.
 *
 * @param pathId - the path segment, URL-encoded where it needs to be.
 * @param body - the request body.
 * @returns the fetch Response.
 * @example await patchDsr('0', VALID_BODY)
 */
function patchDsr(pathId: string, body: unknown): Promise<Response> {
  return fetch(`${baseUrl}/api/gdpr/dsr/${pathId}`, {
    method: 'PATCH',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
}

describe('KS-1029 a malformed or non-canonical dsrId is refused before the lookup', () => {
  it.each([
    { row: 'M1', pathId: 'not-a-uuid' },
    { row: 'M2', pathId: '0' },
    { row: 'M3', pathId: `${REAL_DSR_ID}a` },
    { row: 'M4', pathId: '11111111-2222-4333-8444' },
    // N1 and N2 are the deliberate narrowing: PostgreSQL accepts both, UUID_PATTERN does not.
    { row: 'N1', pathId: storedForm(REAL_DSR_ID) },
    { row: 'N2', pathId: `%7B${REAL_DSR_ID}%7D` },
  ])('$row 404 NOT_FOUND with no DB call — $pathId', async ({ pathId }) => {
    const res = await patchDsr(pathId, VALID_BODY);
    expect(res.status).toBe(404);
    expect(((await res.json()) as DsrUpdateResponse).error).toEqual({ code: 'NOT_FOUND', message: 'DSR not found' });
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});

describe('KS-1029 controls — the rows the guard must not change', () => {
  it('U1 an uppercase canonical id passes the guard (the pattern is case-insensitive) and reaches the lookup', async () => {
    const res = await patchDsr(UPPERCASE_ABSENT_ID, VALID_BODY);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: false, message: 'DSR not found' });
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('A1 a canonical absent id is unchanged: 200 {success:false}', async () => {
    const res = await patchDsr('aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee', VALID_BODY);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: false, message: 'DSR not found' });
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('R1 a canonical real id is unchanged: 200 {success:true}', async () => {
    const res = await patchDsr(REAL_DSR_ID, VALID_BODY);
    expect(res.status).toBe(200);
    expect(await res.json()).toEqual({ success: true, message: 'DSR updated' });
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('D1 a database error on a canonical id still answers 500 (the KS-754 rethrow)', async () => {
    const res = await patchDsr(DB_ERROR_DSR_ID, VALID_BODY);
    expect(res.status).toBe(500);
    // The message is deliberately not asserted: the catch's err.message handling is KS-730's.
    expect(((await res.json()) as DsrUpdateResponse).error?.code).toBe('INTERNAL_ERROR');
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });

  it('O1 a malformed id with a wrong-typed body gets the body 400 first', async () => {
    const res = await patchDsr('not-a-uuid', { status: 'pending', processedBy: {} });
    expect(res.status).toBe(400);
    expect(((await res.json()) as DsrUpdateResponse).error?.code).toBe('VALIDATION_ERROR');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('O2 a malformed id with no status/processedBy gets the required-fields 400 first', async () => {
    const res = await patchDsr('not-a-uuid', {});
    expect(res.status).toBe(400);
    expect(((await res.json()) as DsrUpdateResponse).error?.code).toBe('BAD_REQUEST');
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});

describe('KS-1029 harness — the DB model reads ids the way PostgreSQL documents', () => {
  it('accepts canonical, uppercase, hyphenless and braced ids and rejects the malformed rows', () => {
    const accepted = [REAL_DSR_ID, UPPERCASE_ABSENT_ID, storedForm(REAL_DSR_ID), `{${REAL_DSR_ID}}`];
    const rejected = ['not-a-uuid', '0', `${REAL_DSR_ID}a`, '11111111-2222-4333-8444'];
    expect(accepted.map((id) => pgUuidAccepts(id))).toEqual([true, true, true, true]);
    expect(rejected.map((id) => pgUuidAccepts(id))).toEqual([false, false, false, false]);
  });
});
