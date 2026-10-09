/**
 * KS-1352 - a revoked credential must FAIL verification, by EITHER revoke route.
 *
 * Kam ruled option (a): "Fix verify properly: a revoked credential fails". So
 * `POST /api/credentials/verify` answers `verified: false` with `checks.status: false` and a
 * revocation reason in `result.errors` for a credential revoked through EITHER route:
 *   - `POST /api/credentials/:id/revoke`  -> credentialRepo.revoke(), which writes
 *     `revoked: true` into the STORED record's `credentialStatus`;
 *   - `POST /api/status/:id/revoke`       -> the status list manager's own revocation bit.
 * A never-revoked credential must still verify true.
 *
 * Before this change `verify` wired NO resolver of any kind, so `checkStatus()` could not reach
 * either authority: it returned `{ valid: errors.length === 0 }` over an empty error list, i.e.
 * VALID, and nothing anywhere read `credentialStatus.revoked`. Measured on develop `0d156d12`:
 * `git log -S statusListResolver` returns exactly one commit, the 2026-02-05 introduction.
 *
 * UNKNOWN IDs ARE DELIBERATELY NOT REFUSED (Wednesday's ruling on my Q1, option (b) pass-through).
 * The stored-record arm ABSTAINS when there is no record, because Kam ruled on revoked credentials,
 * not unknown ones, and failing closed would refuse every credential on a stack with no database
 * (`credentialRepo.loadFromDb` returns silently when the DB is unavailable). Cell C2 pins that
 * abstention so a later change cannot widen the ruling by accident.
 *
 * Harness: the ks1269 suite's dispatch double - the REAL credentialRoutes, the REAL statusRoutes
 * and the REAL errorHandler. No DB in this environment, so credentialRepo uses its memory store.
 */

import { describe, it, expect, beforeAll } from 'vitest';
import crypto from 'crypto';
import { credentialRoutes } from '../routes/credentials';
import { statusRoutes } from '../routes/status';
import { errorHandler } from '../middleware/errorHandler';

type Reply = { status: number; body: any };

/** Dispatch one request through a real router; errors go to the real errorHandler. */
function dispatch(router: unknown, method: string, url: string, body?: unknown): Promise<Reply> {
  return new Promise((resolve, reject) => {
    const req: any = {
      method,
      url,
      baseUrl: '',
      originalUrl: url,
      headers: {},
      body,
      params: {},
      query: {},
      // A platform-level actor: statusRoutes gates writes on this (KS-586/KS-692).
      user: { userId: 'ks1352-test-user', role: 'SYSTEM_ADMIN', organizationId: 'org-test' },
    };
    const res: any = {
      statusCode: 200,
      status(code: number) { this.statusCode = code; return this; },
      json(payload: unknown) { resolve({ status: this.statusCode, body: payload }); return this; },
    };
    const next = (err?: unknown) => {
      if (err) { errorHandler(err as Error, req, res, () => {}); }
      else { reject(new Error('route did not match ' + method + ' ' + url)); }
    };
    (router as (rq: any, rs: any, nx: (e?: unknown) => void) => void)(req, res, next);
  });
}

/**
 * FIXTURE, AND IT IS LOAD-BEARING. The issue route REFUSES without a real signing key
 * (credentials.ts:189-198, audit A-11: no hardcoded fallback, ever), so without this every cell
 * below fails 503 inside the issue helper - INCLUDING the controls, which is the tell that a run
 * measured the harness and not the product. Measured: that is exactly what my first red run did,
 * 5 failed / 5 with C1 and C2 among them.
 *
 * A freshly generated Ed25519 PKCS8 DER hex key (96 chars, > the 64 signCredential requires at
 * builder.ts:305) keeps the proof honestly labelled Ed25519Signature2020. The key is generated per
 * run and never leaves this process.
 */
beforeAll(() => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
});

const cred = (m: string, u: string, b?: unknown) => dispatch(credentialRoutes, m, u, b);
const stat = (m: string, u: string, b?: unknown) => dispatch(statusRoutes, m, u, b);

/** Issue a real credential and hand back the as-issued document. */
async function issue(tag: string) {
  const r = await cred('POST', '/', {
    documentId: 'doc-' + tag,
    documentHash: 'hash-' + tag,
    documentType: 'PropertyDeed',
    documentTitle: 'KS-1352 ' + tag,
  });
  if (r.status !== 201 && r.status !== 200) {
    throw new Error('issue failed for ' + tag + ': ' + r.status + ' ' + JSON.stringify(r.body));
  }
  const credential = r.body?.credential ?? r.body?.data?.credential ?? r.body;
  return credential;
}

/** Verify a document through the real public route and reduce it to what this ticket is about. */
async function verify(document: unknown) {
  const r = await cred('POST', '/verify', { credential: document });
  return {
    httpStatus: r.status,
    verified: r.body?.verified,
    statusCheck: r.body?.result?.checks?.status,
    docStatus: r.body?.result?.credential?.status,
    errors: (r.body?.result?.errors ?? []) as string[],
  };
}

const mentionsRevocation = (errors: string[]) =>
  errors.some((e) => /revok/i.test(e));

describe('KS-1352 a revoked credential fails verification by either route', () => {
  it('F0 fixture health: issuance works, so a red below is the product and not the harness', async () => {
    const r = await cred('POST', '/', {
      documentId: 'doc-f0', documentHash: 'hash-f0',
      documentType: 'PropertyDeed', documentTitle: 'KS-1352 f0',
    });
    expect(r.status).toBe(201);
    expect(typeof r.body?.credential?.id).toBe('string');
    expect(r.body?.credential?.proof?.type).toBe('Ed25519Signature2020');
  });

  it('R1 revoked via POST /api/credentials/:id/revoke - the AS-ISSUED document must fail', async () => {
    const document = await issue('r1');
    const rv = await cred('POST', '/' + encodeURIComponent(document.id) + '/revoke', { reason: 'KS-1352 R1' });
    expect(rv.status).toBe(200);

    const v = await verify(document);
    expect({ verified: v.verified, statusCheck: v.statusCheck, docStatus: v.docStatus, saysRevoked: mentionsRevocation(v.errors) })
      .toEqual({ verified: false, statusCheck: false, docStatus: 'revoked', saysRevoked: true });
  });

  it('R2 revoked via POST /api/credentials/:id/revoke - the RE-READ document must fail', async () => {
    const document = await issue('r2');
    await cred('POST', '/' + encodeURIComponent(document.id) + '/revoke', { reason: 'KS-1352 R2' });

    const reread = await cred('GET', '/' + encodeURIComponent(document.id));
    expect(reread.status).toBe(200);
    // The re-read record is the one that carries revoked: true.
    expect(reread.body?.credential?.credentialStatus?.revoked).toBe(true);

    const v = await verify(reread.body.credential);
    expect({ verified: v.verified, statusCheck: v.statusCheck, docStatus: v.docStatus, saysRevoked: mentionsRevocation(v.errors) })
      .toEqual({ verified: false, statusCheck: false, docStatus: 'revoked', saysRevoked: true });
  });

  it('R3 revoked via POST /api/status/:id/revoke - the AS-ISSUED document must fail', async () => {
    const document = await issue('r3');
    const alloc = await stat('POST', '/default/allocate', { credentialId: document.id });
    expect(alloc.status).toBe(200);
    const rv = await stat('POST', '/default/revoke', { credentialId: document.id, reason: 'KS-1352 R3' });
    expect(rv.status).toBe(200);

    const v = await verify(document);
    expect({ verified: v.verified, statusCheck: v.statusCheck, docStatus: v.docStatus, saysRevoked: mentionsRevocation(v.errors) })
      .toEqual({ verified: false, statusCheck: false, docStatus: 'revoked', saysRevoked: true });
  });

  it('C1 control: a NEVER-revoked credential still verifies true', async () => {
    const document = await issue('c1');
    const v = await verify(document);
    expect({ verified: v.verified, statusCheck: v.statusCheck, docStatus: v.docStatus })
      .toEqual({ verified: true, statusCheck: true, docStatus: 'active' });
  });

  it('C2 control: an id with NO stored record is REFUSED (KS-1375, fail closed)', async () => {
    // Never issued here, so neither authority holds a record for it.
    // RE-PINNED BY KS-1375. This used to assert the stored-record arm ABSTAINS and that such a
    // credential "still verifies true". Kam ruled option (b) on the card
    // `secuura-ks1352-unknown-id-policy-after-gate38` -- no issuer record now FAILS CLOSED -- so the
    // boundary this cell pins genuinely MOVED. The title moved with the assertion: a cell still
    // named "still verifies true (pass-through)" while asserting the opposite would lie about
    // itself. This is not a weakened pin: it asserts the same two fields, with the values the
    // ruling now requires, and it is the cell KS 1368 names as the one to edit.
    const document = await issue('c2');
    const stranger = { ...document, id: 'urn:uuid:ks1352-never-issued-anywhere' };
    const v = await verify(stranger);
    expect({ verified: v.verified, statusCheck: v.statusCheck }).toEqual({ verified: false, statusCheck: false });
  });
});
