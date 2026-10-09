/**
 * KS-444 — write-path request-schema drift, vc-issuer presentations + status.
 *
 * Adjudicated findings covered here:
 *  - POST /presentations        (neg): a spec-violating credential item
 *    (`proof: 123`, `expirationDate: 5`) was minted into a stored VP with a
 *    201 — the validator now enforces the spec-declared field types.
 *  - POST /presentations/request (neg): `credentialTypes: [{}]` / `domain: {}`
 *    were echoed into a 201 — now Zod-validated to the spec shape.
 *  - POST /presentations/verify  (neg, semantic defect): an EMPTY
 *    verifiableCredential array plus a garbage `proof: [null, null]` came back
 *    `verified: true` from a PUBLIC endpoint (`[].every()` is vacuously true
 *    and a truthy non-object proof skipped every check). Now: no credentials
 *    presented → nothing verified (200 verified:false), and — per KS-466 §5 —
 *    a NON-OBJECT presentation proof is a spec-shape violation → 400 (the Vp
 *    schema declares proof a record); an OBJECT proof with malformed content
 *    stays 200 verified:false (the KS-445 verification-failure semantic).
 *  - POST /status               (neg): `id: {}` (truthy object) passed the
 *    bare `!id` check and was echoed into a 201 — now Zod-validated to the
 *    spec's declared types (id: non-empty string, purpose enum, capacity
 *    positive int).
 *
 * Same hand-rolled req/res double + real-router + real-errorHandler dispatch
 * style as credentialsVerify.fuzz.test.ts.
 */

import { describe, it, expect } from 'vitest';
import { presentationRoutes } from '../routes/presentations';
import { statusRoutes } from '../routes/status';
import { errorHandler } from '../middleware/errorHandler';

/**
 * Dispatch a request through a real Express router with a mocked req/res pair;
 * route errors flow into the real shared errorHandler exactly as in index.ts.
 */
function dispatch(
  router: unknown,
  method: string,
  url: string,
  body: unknown,
): Promise<{ status: number; body: any }> {
  return new Promise((resolve, reject) => {
    const req: any = {
      method,
      url,
      baseUrl: '',
      originalUrl: url,
      headers: {},
      body,
      // KS-586: status WRITES now sit behind an admin-class role gate at the
      // route table; these tests assert request-VALIDATION behaviour, which
      // lives behind that gate, so dispatch as a privileged caller. The gate
      // itself is pinned by ks586-status-write-authorization.test.ts.
      user: { userId: 'ks444-test-user', role: 'SYSTEM_ADMIN', organizationId: 'org-test' },
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
        reject(new Error(`route did not match ${method} ${url}`));
      }
    };
    (router as (rq: any, rs: any, nx: (e?: unknown) => void) => void)(req, res, next);
  });
}

/** A minimal spec-complete W3C VC item for the create-presentation payload. */
function baseCredential(): Record<string, unknown> {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id: 'urn:uuid:ks444-test-credential',
    type: ['VerifiableCredential'],
    issuer: 'did:prism:secuura_test_issuer',
    issuanceDate: '2026-01-01T00:00:00Z',
    credentialSubject: { documentHash: 'ab'.repeat(32) },
  };
}

describe('KS-444 — POST /presentations request-schema enforcement', () => {
  it('rejects a missing body (credentials required) with a 400 envelope', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/', undefined);
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('rejects a credential item with a non-object proof (proof: 123) — was a 201', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/', {
      credentials: [{ ...baseCredential(), proof: 123 }],
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('rejects a credential item with a non-string expirationDate — was a 201', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/', {
      credentials: [{ ...baseCredential(), expirationDate: 5 }],
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('still accepts a spec-complete unsigned presentation (no holderDID → no signing)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/', {
      credentials: [{ ...baseCredential(), proof: { type: 'Ed25519Signature2020' } }],
    });
    expect(status).toBe(201);
    expect(body.success).toBe(true);
    expect(body.presentation.verifiableCredential).toHaveLength(1);
  });
});

describe('KS-444 — POST /presentations/request request-schema enforcement', () => {
  it('rejects a non-string domain (domain: {}) — was echoed into a 201', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/request', {
      credentialTypes: ['DocumentCertification'],
      domain: {},
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('rejects non-string credentialTypes items ([{}]) — was echoed into a 201', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/request', {
      credentialTypes: [{}],
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('still rejects a missing credentialTypes with 400', async () => {
    const { status } = await dispatch(presentationRoutes, 'POST', '/request', {});
    expect(status).toBe(400);
  });

  it('still accepts a spec-complete request (and honours extension fields)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/request', {
      credentialTypes: ['DocumentCertification'],
      challenge: 'c-1',
      domain: 'https://verifier.example',
      purpose: 'KYC onboarding',
    });
    expect(status).toBe(201);
    expect(body.success).toBe(true);
    expect(body.request.credentialTypes).toEqual(['DocumentCertification']);
    expect(body.request.challenge).toBe('c-1');
    expect(body.request.purpose).toBe('KYC onboarding');
  });
});

describe('KS-444 — POST /presentations/verify must not verify fuzz garbage', () => {
  it('proof [null,null] violates the declared Vp shape → 400 (KS-466 §5; spec declares proof a record)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': [],
        id: '',
        type: [],
        verifiableCredential: [],
        holder: '',
        proof: [null, null],
      },
      challenge: '',
      domain: '',
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('an OBJECT proof reaches the verification logic — content problems stay a 200 verification failure (KS-445 boundary)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': ['https://www.w3.org/2018/credentials/v1'],
        type: ['VerifiablePresentation'],
        verifiableCredential: [baseCredential()],
        proof: { type: 'Ed25519Signature2020', challenge: 'other' },
      },
      challenge: 'expected',
    });
    expect(status).toBe(200);
    expect(body.verified).toBe(false);
    expect(body.checks.presentationProofValid).toBe(false);
  });

  it('empty verifiableCredential alone (no proof) → verified:false — nothing was verified', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': ['https://www.w3.org/2018/credentials/v1'],
        type: ['VerifiablePresentation'],
        verifiableCredential: [],
      },
    });
    expect(status).toBe(200);
    expect(body.verified).toBe(false);
    expect(body.checks.allCredentialsValid).toBe(false);
  });

  it('a non-object proof (string) violates the declared Vp shape → 400 (KS-466 §5)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': ['https://www.w3.org/2018/credentials/v1'],
        type: ['VerifiablePresentation'],
        verifiableCredential: [baseCredential()],
        proof: 'not-an-object',
      },
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('an unverifiable inner credential stays a 200 verification failure (KS-445 semantic)', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': ['https://www.w3.org/2018/credentials/v1'],
        type: ['VerifiablePresentation'],
        // Degenerate item — permissive per the KS-445 decision; the shared
        // verifier reports it as a verification failure, never a 500/400.
        verifiableCredential: [{ garbage: true }],
      },
    });
    expect(status).toBe(200);
    expect(body.verified).toBe(false);
    expect(body.checks.allCredentialsValid).toBe(false);
    expect(body.credentialResults).toHaveLength(1);
    expect(body.credentialResults[0].verified).toBe(false);
  });

  it('a missing presentation still earns the Zod 400', async () => {
    const { status, body } = await dispatch(presentationRoutes, 'POST', '/verify', {});
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('a non-string holder violates the declared Vp shape → 400', async () => {
    const { status } = await dispatch(presentationRoutes, 'POST', '/verify', {
      presentation: {
        '@context': [],
        type: [],
        verifiableCredential: [],
        holder: {},
      },
    });
    expect(status).toBe(400);
  });
});

describe('KS-444 — POST /status request-schema enforcement', () => {
  it('rejects id sent as an object ({} is truthy) — was echoed into a 201', async () => {
    const { status, body } = await dispatch(statusRoutes, 'POST', '/', {
      id: {},
      purpose: 'revocation',
      capacity: 1,
    });
    expect(status).toBe(400);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('rejects an empty id (spec declares minLength 1)', async () => {
    const { status } = await dispatch(statusRoutes, 'POST', '/', { id: '' });
    expect(status).toBe(400);
  });

  it('rejects a purpose outside the declared enum', async () => {
    const { status } = await dispatch(statusRoutes, 'POST', '/', {
      id: 'ks444-bad-purpose',
      purpose: 'bogus',
    });
    expect(status).toBe(400);
  });

  it('rejects a non-positive-integer capacity', async () => {
    const { status } = await dispatch(statusRoutes, 'POST', '/', {
      id: 'ks444-bad-capacity',
      capacity: 0,
    });
    expect(status).toBe(400);
  });

  it('still creates a list from a spec-complete body, and 409s a duplicate id', async () => {
    const created = await dispatch(statusRoutes, 'POST', '/', {
      id: 'ks444-list-1',
      purpose: 'suspension',
      capacity: 100,
    });
    expect(created.status).toBe(201);
    expect(created.body.statusListId).toBe('ks444-list-1');
    expect(created.body.purpose).toBe('suspension');

    const duplicate = await dispatch(statusRoutes, 'POST', '/', { id: 'ks444-list-1' });
    expect(duplicate.status).toBe(409);
  });

  it('allocate still requires a non-empty credentialId and works with one (KS-444 pos re-adjudication)', async () => {
    const empty = await dispatch(statusRoutes, 'POST', '/default/allocate', { credentialId: '' });
    expect(empty.status).toBe(400);

    const ok = await dispatch(statusRoutes, 'POST', '/default/allocate', {
      credentialId: 'urn:uuid:ks444-cred',
    });
    expect(ok.status).toBe(200);
    expect(ok.body.credentialId).toBe('urn:uuid:ks444-cred');
    expect(typeof ok.body.index).toBe('number');
  });

  it('revoke/unrevoke of an unallocated credential is a 404, not a raw 500 (KS-445 tail)', async () => {
    // The manager throws a plain Error for an unknown credential; without the
    // route guard that became a 500. An unallocated credential is not-found.
    const revoke = await dispatch(statusRoutes, 'POST', '/default/revoke', {
      credentialId: 'urn:uuid:never-allocated',
    });
    expect(revoke.status).toBe(404);
    expect(revoke.body.error.code).toBe('NOT_FOUND');

    const unrevoke = await dispatch(statusRoutes, 'POST', '/default/unrevoke', {
      credentialId: 'urn:uuid:never-allocated',
    });
    expect(unrevoke.status).toBe(404);
  });

  it('rejects a non-string credentialId / reason instead of echoing it into the response (KS-440)', async () => {
    // The fuzzer sent credentialId:{} / reason:{}, which the old truthy check let
    // through and the handler echoed back — violating the response schema (both
    // declared string). Now a 400 before any allocation/revoke.
    const allocObj = await dispatch(statusRoutes, 'POST', '/default/allocate', { credentialId: {} });
    expect(allocObj.status).toBe(400);
    const allocEmpty = await dispatch(statusRoutes, 'POST', '/default/allocate', { credentialId: '' });
    expect(allocEmpty.status).toBe(400);
    const revObjCred = await dispatch(statusRoutes, 'POST', '/default/revoke', { credentialId: {} });
    expect(revObjCred.status).toBe(400);
    const revObjReason = await dispatch(statusRoutes, 'POST', '/default/revoke', {
      credentialId: 'urn:uuid:x',
      reason: {},
    });
    expect(revObjReason.status).toBe(400);
  });

  it('rejects a negative index on check instead of echoing it (KS-440)', async () => {
    // A bitstring position is a non-negative integer; a negative index used to be
    // echoed back, violating the response schema (index minimum 0).
    const neg = await dispatch(statusRoutes, 'GET', '/default/check/-1', undefined);
    expect(neg.status).toBe(400);
  });
});
