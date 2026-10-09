/**
 * KS-1269 - POST /api/status/:id/unrevoke refuses a present index that is not an integer.
 *
 * The handler unrevokes by credentialId and never reads index, so index: {} answered 200 and the
 * unrevoke ran. The published schema declares index an optional integer. A present index that is
 * not an integer is now refused 400 before the status list is touched. An absent index, and an
 * integer index, are unchanged.
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
      user: { userId: 'ks1269u-test-user', role: 'SYSTEM_ADMIN', organizationId: 'org-test' },
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

/** Allocate and revoke a fresh credential, unrevoke it with the extra body fields, read its bit back. */
async function unrevokeWith(credentialId: string, extra: Record<string, unknown>) {
  const alloc = await dispatch('POST', '/default/allocate', { credentialId });
  await dispatch('POST', '/default/revoke', { credentialId });
  const r = await dispatch('POST', '/default/unrevoke', { credentialId, ...extra });
  const check = await dispatch('GET', '/default/check/' + String(alloc.body.index), undefined);
  return [r.status, r.body?.error?.code ?? null, check.body.isRevoked];
}

describe('KS-1269 POST /api/status/:id/unrevoke refuses a present index that is not an integer', () => {
  it('control: no index still unrevokes, 200', async () => {
    expect(await unrevokeWith('urn:uuid:ks1269u-absent', {})).toEqual([200, null, false]);
  });

  it('control: an integer index still unrevokes, 200', async () => {
    expect(await unrevokeWith('urn:uuid:ks1269u-integer', { index: 3 })).toEqual([200, null, false]);
  });

  it('🔴 KS-1269: index {} is refused 400 and the credential stays revoked', async () => {
    expect(await unrevokeWith('urn:uuid:ks1269u-object', { index: {} })).toEqual([400, 'BAD_REQUEST', true]);
  });

  it('🔴 KS-1269: a string index is refused 400 and the credential stays revoked', async () => {
    expect(await unrevokeWith('urn:uuid:ks1269u-string', { index: '3' })).toEqual([400, 'BAD_REQUEST', true]);
  });

  it('🔴 KS-1269: index 1.5 is refused 400 and the credential stays revoked', async () => {
    expect(await unrevokeWith('urn:uuid:ks1269u-fraction', { index: 1.5 })).toEqual([400, 'BAD_REQUEST', true]);
  });

  it('control KS-1371: index 0 still unrevokes, 200', async () => {
    expect(await unrevokeWith('urn:uuid:ks1371-zero', { index: 0 })).toEqual([200, null, false]);
  });

  it('control KS-1371: revoke still admits index -1 (the KS-662 ruling), 200', async () => {
    await dispatch('POST', '/default/allocate', { credentialId: 'urn:uuid:ks1371-revoke' });
    const r = await dispatch('POST', '/default/revoke', { credentialId: 'urn:uuid:ks1371-revoke', index: -1 });
    expect([r.status, r.body?.revoked]).toEqual([200, true]);
  });

  it('RED KS-1371 U1: index -1 is refused 400 and the credential stays revoked', async () => {
    expect(await unrevokeWith('urn:uuid:ks1371-minus-one', { index: -1 })).toEqual([400, 'BAD_REQUEST', true]);
  });

  it('RED KS-1371 U2: index -7 is refused 400 and the credential stays revoked', async () => {
    expect(await unrevokeWith('urn:uuid:ks1371-minus-seven', { index: -7 })).toEqual([400, 'BAD_REQUEST', true]);
  });
});
