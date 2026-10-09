/**
 * =============================================================================
 * LIFECYCLE EVENT REPOSITORY — UNIT TESTS (KS-387)
 * =============================================================================
 * `prisma.$queryRaw` / `$executeRaw` mocked at the unit boundary (same pattern
 * as documentRepo.test.ts). Covers the logic the repo layers on top of raw SQL:
 *   - createLifecycleEvent: returned record shape, payload defaulting, and the
 *     LIFECYCLE_TARGET_NOT_FOUND mapping when the tenant-scoped external_id
 *     subquery resolves to NULL (the shareRepo detection pattern)
 *   - setLifecycleEventAnchor: fires the UPDATE
 *   - listLifecycleEvents: row → domain mapping incl. null/absent fields
 * Plus the KS-387/KS-389 action-vocabulary pin (lifecycleActions.ts): growing or
 * shrinking the endpoint's verb set is a cross-platform contract change.
 * =============================================================================
 */

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
  },
}));

jest.mock('../utils/logger', () => ({
  logger: {
    info: jest.fn(),
    warn: jest.fn(),
    error: jest.fn(),
    debug: jest.fn(),
  },
}));

import {
  createLifecycleEvent,
  setLifecycleEventAnchor,
  listLifecycleEvents,
} from '../repositories/lifecycleEventRepo';
import { LIFECYCLE_EVENT_ACTIONS } from '../lifecycleActions';

const TENANT = '11111111-2222-3333-4444-555555555555';

beforeEach(() => {
  jest.clearAllMocks();
});

describe('LIFECYCLE_EVENT_ACTIONS vocabulary pin', () => {
  it('accepts exactly the no-dedicated-endpoint verbs (KS-387 four + KS-389 delete/restore + KS-415 share-edit four + KS-534 attach-consent + KS-556 protect/unprotect + KS-1172/KS-1173 note/certified/verified)', () => {
    // Deliberate pin: verbs WITH dedicated endpoints (share, transfer-custody,
    // revoke, ...) must never appear here — S routes those to their own routes.
    expect([...LIFECYCLE_EVENT_ACTIONS].sort()).toEqual(
      [
        'delete',
        'protect',
        'rename',
        'restore',
        'unprotect',
        'note',
        'certified',
        'verified',
        'rights-unassign',
        'share-attach-consent',
        'share-expiry-change',
        'share-permission-change',
        'share-recipient-change',
        'share-resend',
        'share-revoke',
        'share-token-rotate',
      ].sort(),
    );
  });

  it('🔴 KS-1172 / KS-1173 — accepts note, certified and verified (Stuart 2026-09-15); declare keeps its dedicated route', () => {
    expect(LIFECYCLE_EVENT_ACTIONS).toContain('note');
    expect(LIFECYCLE_EVENT_ACTIONS).toContain('certified');
    expect(LIFECYCLE_EVENT_ACTIONS).toContain('verified');
    // CONTROL — green on both trees: a verb WITH a dedicated K route is never accepted here.
    expect(LIFECYCLE_EVENT_ACTIONS).not.toContain('declare');
  });
  it('RED KS-1275 ORDER-1: LIFECYCLE_EVENT_ACTIONS is declared in ONE order, the order z.enum publishes and the 400 message joins', () => {
    const declaredOrder = [...LIFECYCLE_EVENT_ACTIONS].join(',');
    expect(declaredOrder).toEqual('rights-unassign,share-revoke,share-permission-change,rename,delete,restore,share-recipient-change,share-expiry-change,share-token-rotate,share-resend,share-attach-consent,protect,unprotect,note,certified,verified');
  });
});

describe('createLifecycleEvent', () => {
  it('inserts and returns the stored record shape (payload defaulted to {})', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);

    const rec = await createLifecycleEvent({
      tenantId: TENANT,
      documentId: 'doc-123-abc',
      action: 'rights-unassign',
      actorUserId: '99999999-8888-7777-6666-555555555555',
    });

    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
    expect(rec.documentId).toBe('doc-123-abc');
    expect(rec.action).toBe('rights-unassign');
    expect(rec.payload).toEqual({});
    expect(rec.anchorId).toBeNull();
    expect(rec.id).toMatch(/^[0-9a-f-]{36}$/);
    expect(new Date(rec.createdAt).getTime()).not.toBeNaN();
  });

  it('maps a NULL subquery resolution to LIFECYCLE_TARGET_NOT_FOUND', async () => {
    // The tenant-scoped external_id → documents.id subquery found no row, so
    // Postgres rejects the NOT NULL parent_document_id — the route maps this to 404.
    mockExecuteRaw.mockRejectedValueOnce(
      new Error('null value in column "parent_document_id" of relation "document_lifecycle_events" violates not-null constraint'),
    );

    await expect(
      createLifecycleEvent({ tenantId: TENANT, documentId: 'doc-not-there', action: 'delete' }),
    ).rejects.toMatchObject({ code: 'LIFECYCLE_TARGET_NOT_FOUND' });
  });

  it('re-throws unrelated database errors untouched', async () => {
    mockExecuteRaw.mockRejectedValueOnce(new Error('connection refused'));

    await expect(
      createLifecycleEvent({ tenantId: TENANT, documentId: 'doc-123-abc', action: 'rename' }),
    ).rejects.toThrow('connection refused');
  });
});

describe('setLifecycleEventAnchor', () => {
  it('fires the anchor-id UPDATE', async () => {
    mockExecuteRaw.mockResolvedValueOnce(1);
    await setLifecycleEventAnchor('aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee', 'anchor_123');
    expect(mockExecuteRaw).toHaveBeenCalledTimes(1);
  });
});

describe('listLifecycleEvents', () => {
  it('maps rows to domain records including null/absent fields', async () => {
    // One fully-populated row + one minimal row (no actor, no anchor, Date object).
    mockQueryRaw.mockResolvedValueOnce([
      {
        id: 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee',
        tenant_id: TENANT,
        action: 'share-revoke',
        payload: { shareId: 'sh-1' },
        actor_user_id: '99999999-8888-7777-6666-555555555555',
        anchor_id: 'anchor_abc',
        created_at: new Date('2026-07-08T00:00:00.000Z'),
      },
      {
        id: 'ffffffff-0000-1111-2222-333333333333',
        tenant_id: TENANT,
        action: 'delete',
        payload: null,
        actor_user_id: null,
        anchor_id: null,
        created_at: '2026-07-07T00:00:00.000Z',
      },
    ]);

    const events = await listLifecycleEvents('doc-123-abc', TENANT);

    expect(events).toHaveLength(2);
    expect(events[0]).toMatchObject({
      action: 'share-revoke',
      payload: { shareId: 'sh-1' },
      anchorId: 'anchor_abc',
      documentId: 'doc-123-abc',
      createdAt: '2026-07-08T00:00:00.000Z',
    });
    expect(events[1]).toMatchObject({ action: 'delete', payload: {}, actorUserId: null, anchorId: null });
  });
});
