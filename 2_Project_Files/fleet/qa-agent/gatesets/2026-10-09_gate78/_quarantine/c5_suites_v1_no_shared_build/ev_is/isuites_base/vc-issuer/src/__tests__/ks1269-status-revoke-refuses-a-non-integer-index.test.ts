/**
 * KS-1269 - POST /api/status/:id/revoke refuses a present index that is not an integer.
 *
 * The handler revokes by credentialId and never reads index, so index: {} answered 200 and the
 * revoke ran. The published schema declares index an optional integer. A present index that is
 * not an integer is now refused 400 before the status list is touched. An absent index, and an
 * integer index (including -1, the KS-662 ruling), are unchanged.
 *
 * Harness: the ks444 suite's dispatch double - the real statusRoutes and the real errorHandler.
 */

import { describe, it, expect } from 'vitest';
import { statusRoutes } from '../routes/status';
import { errorHandler } from '../middleware/errorHandler';

/** Dispatch one request through the real status router; errors go to the real errorHandler. */
function dispatch(method: string, url: string, body: unknown): Promise<{ status: number; body: any }> {
  return new Promise((resolve, reject) => {
    const req: any = {
      method,
      url,
      baseUrl: '',
      originalUrl: url,
      headers: {},
      body,
      user: { userId: 'ks1269-test-user', role: 'SYSTEM_ADMIN', organizationId: 'org-test' },
    };
    const res: any = {
      statusCode: 200,
      status(code: number) {
        this.statusCode = code;
        return this;
      },
      json(payload: unknown) {
        resolve({ status: this.statusCode, body: payload });
        return this;
      },
    };
    const next = (err?: unknown) => {
      if (err) {
        errorHandler(err as Error, req, res, () => {});
      } else {
        reject(new Error('route did not match ' + method + ' ' + url));
      }
    };
    (statusRoutes as unknown as (rq: any, rs: any, nx: (e?: unknown) => void) => void)(req, res, next);
  });
}

/** Allocate a fresh credential, revoke it with the extra body fields, and read its bit back. */
async function revokeWith(credentialId: string, extra: Record<string, unknown>) {
  const alloc = await dispatch('POST', '/default/allocate', { credentialId });
  const r = await dispatch('POST', '/default/revoke', { credentialId, ...extra });
  const check = await dispatch('GET', '/default/check/' + String(alloc.body.index), undefined);
  return [r.status, r.body?.error?.code ?? null, check.body.isRevoked];
}

describe('KS-1269 POST /api/status/:id/revoke refuses a present index that is not an integer', () => {
  it('control: no index still revokes, 200', async () => {
    expect(await revokeWith('urn:uuid:ks1269-absent', {})).toEqual([200, null, true]);
  });

  it('KS-1269 N71-2 ordering: on /revoke, a bad index on an UNKNOWN credential is 400, before the 404', async () => {
    const r = await dispatch('POST', '/default/revoke', { credentialId: 'urn:uuid:ks1269-never-allocated', index: {} });
    expect([r.status, r.body?.error?.message]).toEqual([400, 'index must be an integer']);
  });
  it('KS-1269 N71-2 ordering: on /revoke, a bad index with a bad reason answers the index error', async () => {
    const c = 'urn:uuid:ks1269-both-bad';
    await dispatch('POST', '/default/allocate', { credentialId: c });
    const r = await dispatch('POST', '/default/revoke', { credentialId: c, index: {}, reason: {} });
    expect([r.status, r.body?.error?.message]).toEqual([400, 'index must be an integer']);
  });
  it('control: an integer index still revokes, 200', async () => {
    expect(await revokeWith('urn:uuid:ks1269-integer', { index: 3 })).toEqual([200, null, true]);
  });

  it('control: index -1 is still admitted (the KS-662 ruling), 200', async () => {
    expect(await revokeWith('urn:uuid:ks1269-minus-one', { index: -1 })).toEqual([200, null, true]);
  });

  it('🔴 KS-1269: index {} is refused 400 and the credential is not revoked', async () => {
    expect(await revokeWith('urn:uuid:ks1269-object', { index: {} })).toEqual([400, 'BAD_REQUEST', false]);
  });

  it('🔴 KS-1269: a string index is refused 400 and the credential is not revoked', async () => {
    expect(await revokeWith('urn:uuid:ks1269-string', { index: '3' })).toEqual([400, 'BAD_REQUEST', false]);
  });

  it('🔴 KS-1269: index 1.5 is refused 400 and the credential is not revoked', async () => {
    expect(await revokeWith('urn:uuid:ks1269-fraction', { index: 1.5 })).toEqual([400, 'BAD_REQUEST', false]);
  });
  it('RED KS-1269 N71-1: on /revoke, index null is refused 400 and the credential is not revoked', async () => {
    expect(await revokeWith('urn:uuid:ks1269-null', { index: null })).toEqual([400, 'BAD_REQUEST', false]);
  });
  it('RED KS-1269 N71-1: on /unrevoke, index null is refused 400 and the credential stays revoked', async () => {
    const c = 'urn:uuid:ks1269-unrevoke-null';
    const slot = await dispatch('POST', '/default/allocate', { credentialId: c });
    await dispatch('POST', '/default/revoke', { credentialId: c });
    const u = await dispatch('POST', '/default/unrevoke', { credentialId: c, index: null });
    const bit = await dispatch('GET', '/default/check/' + String(slot.body.index), undefined);
    expect([u.status, u.body?.error?.code ?? null, bit.body.isRevoked]).toEqual([400, 'BAD_REQUEST', true]);
  });
});
