/**
 * KS-521 — updateDocument must not resurrect a revoked/deleted document.
 *
 * The async anchor pipeline (the accept-time update and the confirmation
 * poll, which can land up to 10 minutes after creation) writes
 * `status: 'anchored'`. Before the fix that write was unconditional, so a
 * `revoked` set by the owner in between was stomped back to `anchored` and
 * the revoked document verified again (the KS-521 finding).
 *
 * The guard lives IN the UPDATE statement itself — a CASE on the current
 * status, driven by a `preserveTerminalStatuses` boolean bound parameter —
 * so it is atomic against a revoke racing the read-modify-write.
 */

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
  },
  getTenantManager: jest.fn(() => null),
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

import { updateDocument } from '../repositories/documentRepo';

// Any valid v4-shaped uuid — the repo casts it to ::uuid in SQL only.
const TEST_TENANT = '00000000-0000-4000-8000-000000000000';

/** Minimal documents row as the repo's getDocument SELECT projects it. */
function makeDbRow(overrides: Record<string, unknown> = {}): Record<string, unknown> {
  return {
    id: '2539dc16-c5f1-4d8c-b7e4-2d3ff35559a2',
    external_id: 'doc-ks521',
    document_type: 'general',
    status: 'anchored',
    owner_user_id: 'owner-1',
    title: 'KS-521 doc',
    description: null,
    content_hash: 'sha256:ks521',
    metadata: {},
    certification_metadata: {},
    created_at: new Date('2026-01-01T00:00:00.000Z'),
    updated_at: new Date('2026-01-01T00:00:00.000Z'),
    ...overrides,
  };
}

beforeEach(() => {
  mockQueryRaw.mockReset();
  mockExecuteRaw.mockReset();
});

/** Join a tagged-template call's string parts for content assertions. */
function sqlOf(call: unknown[]): string {
  return (call[0] as readonly string[]).join('?');
}

/** Bound values of a tagged-template call (everything after the strings). */
function valuesOf(call: unknown[]): unknown[] {
  return call.slice(1);
}

describe('KS-521 updateDocument terminal-status guard', () => {
  it('binds preserveTerminalStatuses=true and guards the status write with a CASE on revoked/deleted', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow()]);
    mockExecuteRaw.mockResolvedValueOnce(undefined);

    await updateDocument(
      'doc-ks521',
      TEST_TENANT,
      { status: 'anchored' },
      undefined,
      { preserveTerminalStatuses: true },
    );

    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    const call = mockExecuteRaw.mock.calls[0];
    const sql = sqlOf(call);
    // The guard is part of the statement — atomic against a racing revoke.
    expect(sql).toContain('CASE');
    expect(sql).toContain("status IN ('revoked', 'deleted')");
    // First bound value is the guard flag itself.
    expect(valuesOf(call)[0]).toBe(true);
  });

  it('binds the guard flag false by default, so ordinary status writes behave as before', async () => {
    mockQueryRaw.mockResolvedValueOnce([makeDbRow({ status: 'draft' })]);
    mockExecuteRaw.mockResolvedValueOnce(undefined);

    await updateDocument('doc-ks521', TEST_TENANT, { status: 'signed' });

    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    const call = mockExecuteRaw.mock.calls[0];
    // Same statement shape either way; the flag decides at execution time.
    expect(valuesOf(call)[0]).toBe(false);
    // The requested status is still bound (CASE ELSE branch).
    expect(valuesOf(call)).toContain('signed');
  });
});
