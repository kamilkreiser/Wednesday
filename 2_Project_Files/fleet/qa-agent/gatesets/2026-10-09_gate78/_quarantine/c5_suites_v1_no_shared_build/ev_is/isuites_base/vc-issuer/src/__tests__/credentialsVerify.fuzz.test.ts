/**
 * KS-445 regression — POST /api/credentials/verify must never 500 on a
 * fuzz-shaped credential (the op is PUBLIC since KS-442, so the crash was
 * unauthenticated-reachable).
 *
 * Root cause (KS-440 analysis): the shared verifier extracted `proof[0]`
 * and dereferenced `.type` on it — `proof: [null]` crashed with
 * "Cannot read properties of null (reading 'type')" → raw 500 INTERNAL_ERROR.
 *
 * Chosen semantic (KS-445, refined by KS-466 §5): the spec declares `proof`
 * a record, so a NON-OBJECT proof (array/scalar) is a request-shape
 * violation → Zod 400 before the verifier runs. Structural problems INSIDE
 * an object proof ("Proof missing type", …) remain a verification FAILURE —
 * 200 `verified: false` with the reason in `result.errors`. The shared
 * verifier's never-throw guards stay load-bearing regardless: presentations/
 * verify still feeds permissive inner credentials (arbitrary proof shapes)
 * to the same verifier.
 *
 * These tests drive the REAL router (same hand-rolled req/res double style as
 * errorHandler.auth.test.ts, which caught the KS-176 500-on-401 class) plus
 * the shared verifier directly.
 */

import { describe, it, expect } from 'vitest';
import { verifyCredential } from '@secuura/shared/vc';
import { credentialRoutes } from '../routes/credentials';
import { errorHandler } from '../middleware/errorHandler';

/** A structurally valid W3C VC body (no proof — added per test). */
function baseCredential(): Record<string, unknown> {
  return {
    '@context': ['https://www.w3.org/2018/credentials/v1'],
    id: 'urn:uuid:ks445-test-credential',
    type: ['VerifiableCredential'],
    issuer: 'did:prism:secuura_test_issuer',
    issuanceDate: '2026-01-01T00:00:00Z',
    credentialSubject: { documentHash: 'ab'.repeat(32) },
  };
}

/**
 * Dispatch a POST /verify through the real credentials Router with a mocked
 * req/res pair; route errors flow into the real shared errorHandler exactly
 * as they do in index.ts, so a crash would surface here as a 500 envelope.
 */
function dispatchVerify(body: unknown): Promise<{ status: number; body: any }> {
  return new Promise((resolve, reject) => {
    const req: any = {
      method: 'POST',
      url: '/verify',
      baseUrl: '/api/credentials',
      originalUrl: '/api/credentials/verify',
      headers: {},
      body,
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
        // Same wiring as index.ts: route errors land in the shared handler.
        errorHandler(err as Error, req, res, () => {});
      } else {
        reject(new Error('route did not match /verify'));
      }
    };
    (credentialRoutes as unknown as (rq: any, rs: any, nx: (e?: unknown) => void) => void)(req, res, next);
  });
}

describe('KS-445 — POST /credentials/verify fuzz-shaped proof handling', () => {
  it('proof: [null] returns the Zod 400 (KS-466 §5 — spec declares proof a record; was a raw 500 null-deref pre-KS-445)', async () => {
    const { status, body } = await dispatchVerify({
      credential: { ...baseCredential(), proof: [null] },
    });
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('proof: [] (array — spec-shape violation) returns the Zod 400', async () => {
    const { status, body } = await dispatchVerify({
      credential: { ...baseCredential(), proof: [] },
    });
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('proof as a primitive (spec-shape violation) returns the Zod 400', async () => {
    const { status, body } = await dispatchVerify({
      credential: { ...baseCredential(), proof: 'not-an-object' },
    });
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('proof with non-string fields returns 200 verified:false (no .startsWith/.replace crash)', async () => {
    const { status, body } = await dispatchVerify({
      credential: {
        ...baseCredential(),
        proof: { type: 123, verificationMethod: {}, proofValue: ['z'] },
      },
    });
    expect(status).toBe(200);
    expect(body.verified).toBe(false);
    expect(body.result.errors).toEqual(
      expect.arrayContaining([
        'Proof missing type',
        'Proof missing verificationMethod',
        'Proof missing proofValue',
      ]),
    );
  });

  it('a body violating the spec top-level shape still earns the Zod 400', async () => {
    const { status, body } = await dispatchVerify({ credential: { id: 42 } });
    expect(status).toBe(400);
    expect(body.success).toBe(false);
    expect(body.error.code).toBe('BAD_REQUEST');
  });

  it('shared verifyCredential never throws on the fuzz shapes (direct, all-null tour)', async () => {
    // Each shape used to be (or guards against) a null/shape-deref crash path.
    const shapes: unknown[] = [
      [null],
      [undefined],
      [],
      [42],
      ['x'],
      [[]],
      'str',
      0x10,
      true,
    ];
    for (const proof of shapes) {
      const result = await verifyCredential(
        { ...baseCredential(), proof } as any,
        { checkStatus: true, checkExpiration: true, checkBlockchain: false },
      );
      expect(result.verified).toBe(false);
    }
  });

  it('shared verifyCredential survives a fully-degenerate credential (presentations/verify path)', async () => {
    // POST /presentations/verify (also public per KS-442) validates each inner
    // credential only as `z.object({}).passthrough()`, so null issuer /
    // non-array type / missing credentialSubject reach the verifier there —
    // these exercise the KS-445 guards in verifyIssuerDID, verifyContext and
    // the result builder. Default config (checkBlockchain on) like that route.
    const degenerate = {
      '@context': 'not-an-array',
      id: null,
      type: 'not-an-array',
      issuer: null,
      issuanceDate: 42,
      credentialSubject: null,
      credentialStatus: 'truthy-primitive',
      cardanoAnchor: 'truthy-primitive',
      proof: [null],
    };
    const result = await verifyCredential(degenerate as any);
    expect(result.verified).toBe(false);
    expect(result.errors?.length).toBeGreaterThan(0);
  });
});
