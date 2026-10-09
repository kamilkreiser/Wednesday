/**
 * KS-754 — `updateDSRStatus` could not write a non-uuid actor, and hid it.
 *
 * `processed_by` was `uuid` while `processedBy` is PUBLISHED as a plain string
 * (originate.openapi.ts:2630 request `z.string().min(1)`, :2541 response). So
 * `connector:<id>` — which the published contract explicitly permits — raised
 * 22P02, and the function reported it as an ordinary `false`.
 *
 * ⚠ THE TICKET SAYS "every caller ignores that return". THAT IS WRONG FOR ONE
 * OF THE TWO, AND THE TRUTH IS WORSE:
 *
 *   routes/gdpr.ts:361      reads it -> HTTP 200 `{success:false,
 *                           message:'DSR not found'}`  (a DB error reported as
 *                           a successful request about a missing record)
 *   gdprService.ts:842      step 12 of executeErasureImpl — ignores it entirely
 *
 * Two fixes, and they are independent:
 *   1. migration 048 widens the column to TEXT, so the cast is gone and a
 *      non-uuid actor is simply stored;
 *   2. the catch RETHROWS, so a DB failure can never again be dressed as
 *      "no such DSR".
 *
 * (1) alone would have left every OTHER failure on that statement silent.
 */

const mockExecuteRaw = jest.fn();
jest.mock('../db', () => ({
  prisma: { $executeRaw: mockExecuteRaw },
}));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import { updateDSRStatus } from '../services/gdprService';

const DSR = '11111111-1111-4111-8111-111111111111';

beforeEach(() => jest.clearAllMocks());

describe('KS-754 — a non-uuid actor is written, not cast', () => {
  it('sends processedBy as a plain parameter with NO ::uuid cast', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    await updateDSRStatus(DSR, 'completed', 'connector:abc', 'done');

    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    // Prisma tagged templates: [0] is the strings array, the rest are values.
    const [strings] = mockExecuteRaw.mock.calls[0];
    const sql = (strings as unknown as string[]).join('?');

    // The cast that made `connector:abc` unwritable is gone from THIS column.
    expect(sql).toContain('processed_by = ');
    expect(sql).not.toMatch(/processed_by\s*=\s*\?::uuid/);

    // CONTROL: the dsrId cast is still there — this assertion can tell apart
    // "the cast was removed from processed_by" from "all casts vanished",
    // which a looser check could not.
    expect(sql).toMatch(/WHERE id = \?::uuid/);
  });

  it('the actor also reaches the audit trail, unchanged by this fix', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    await updateDSRStatus(DSR, 'completed', 'connector:abc');
    const values = mockExecuteRaw.mock.calls[0].slice(1);
    const audit = values.find((v: unknown) => typeof v === 'string' && v.includes('"actor"'));
    expect(audit).toBeDefined();
    expect(JSON.parse(audit as string).actor).toBe('connector:abc');
  });
});

describe('KS-754 — a failed write is no longer reported as "no such DSR"', () => {
  it('RETHROWS a DB error instead of returning false', async () => {
    const err = Object.assign(new Error('invalid input syntax for type uuid'), { code: '22P02' });
    mockExecuteRaw.mockRejectedValueOnce(err);
    await expect(updateDSRStatus(DSR, 'completed', 'connector:abc')).rejects.toThrow(
      'invalid input syntax for type uuid',
    );
  });

  it('RETHROWS an infrastructure error too — every failure, not just the cast', async () => {
    const err = Object.assign(new Error('too many connections'), { code: '53300' });
    mockExecuteRaw.mockRejectedValueOnce(err);
    await expect(updateDSRStatus(DSR, 'completed', 'admin')).rejects.toThrow('too many connections');
  });

  it('CONTROL: a genuine no-such-row still returns false — absence is still absence', async () => {
    // 0 rows updated is the real "no such DSR", and it must stay distinguishable
    // from a failure. This is the cell that stops the fix over-correcting.
    mockExecuteRaw.mockResolvedValueOnce(0);
    await expect(updateDSRStatus(DSR, 'completed', 'admin')).resolves.toBe(false);
  });

  it('CONTROL: a successful write still returns true', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    await expect(updateDSRStatus(DSR, 'completed', 'admin')).resolves.toBe(true);
  });
});
