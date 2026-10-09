/**
 * KS-1375 — verify fails CLOSED when no authority holds a record for the submitted id.
 *
 * gate38's N-1330-1, measured at runtime: a credential revoked through
 * `POST /api/credentials/:id/revoke`, resubmitted with any OTHER `id`, answered `verified: true`
 * with `checks.status: true`. Both revocation resolvers key on the caller-supplied `credential.id`
 * and the stored arm ABSTAINED on `found: false`, so editing one field un-revoked the credential.
 *
 * Kam ruled option (b) on `secuura-ks1352-unknown-id-policy-after-gate38`: no issuer record ->
 * `verified: false` with the reason `'no issuer record'`. That is also option 2 of the KS 1368
 * policy ticket, word for word.
 *
 * Both verify routes are driven, because both wire `revocationVerifierConfig()`:
 * `routes/credentials.ts` POST /verify and `routes/presentations.ts` POST /verify. The
 * presentations route is asserted through `credentialResults[]`, which is per-credential and
 * therefore independent of `presentationProofValid` — a control there is not confounded by the
 * presentation's own proof.
 *
 * C4 is the cell that protects every OTHER consumer: a verifier built with NO
 * storedRecordResolver must behave exactly as it did before this change.
 */
import { describe, it, expect, beforeAll } from 'vitest';
import crypto from 'crypto';
import { credentialRoutes } from '../routes/credentials';
import { presentationRoutes } from '../routes/presentations';
import { errorHandler } from '../middleware/errorHandler';
import { verifyCredential } from '@secuura/shared/vc';

type Reply = { status: number; body: any };

function dispatch(router: unknown, method: string, url: string, body?: unknown): Promise<Reply> {
  return new Promise((resolve, reject) => {
    const req: any = {
      method, url, baseUrl: '', originalUrl: url, headers: {}, body, params: {}, query: {},
      user: { userId: 'ks1375-test-user', role: 'SYSTEM_ADMIN', organizationId: 'org-test' },
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

beforeAll(() => {
  const { privateKey } = crypto.generateKeyPairSync('ed25519');
  process.env.VC_SIGNING_KEY = privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex');
});

const cred = (m: string, u: string, b?: unknown) => dispatch(credentialRoutes, m, u, b);
const pres = (m: string, u: string, b?: unknown) => dispatch(presentationRoutes, m, u, b);

async function issue(tag: string) {
  const r = await cred('POST', '/', {
    documentId: 'doc-' + tag, documentHash: 'hash-' + tag,
    documentType: 'PropertyDeed', documentTitle: 'KS-1375 ' + tag,
  });
  if (r.status !== 201 && r.status !== 200) {
    throw new Error('issue failed for ' + tag + ': ' + r.status + ' ' + JSON.stringify(r.body));
  }
  return r.body?.credential ?? r.body?.data?.credential ?? r.body;
}

/** The credentials route, reduced to what this ticket is about. */
async function verifyCred(document: unknown) {
  const r = await cred('POST', '/verify', { credential: document });
  return {
    verified: r.body?.verified,
    statusCheck: r.body?.result?.checks?.status,
    errors: (r.body?.result?.errors ?? []) as string[],
  };
}

/** The presentations route, asserted PER CREDENTIAL so the presentation's own proof cannot confound it. */
async function verifyInPresentation(document: unknown) {
  const r = await pres('POST', '/verify', {
    presentation: {
      '@context': ['https://www.w3.org/2018/credentials/v1'],
      type: ['VerifiablePresentation'],
      id: 'urn:uuid:ks1375-presentation',
      holder: 'did:secuura:ks1375-holder',
      verifiableCredential: [document],
    },
  });
  const first = r.body?.credentialResults?.[0];
  return {
    httpStatus: r.status,
    allCredentialsValid: r.body?.checks?.allCredentialsValid,
    credentialVerified: first?.verified,
    errors: (first?.errors ?? []) as string[],
  };
}

const saysNoIssuerRecord = (errors: string[]) => errors.some((e) => /no issuer record/i.test(e));
const mentionsRevocation = (errors: string[]) => errors.some((e) => /revok/i.test(e));

describe('KS-1375 verify fails closed when no authority holds a record for the id', () => {
  it('F0 fixture health: issuance works, so a red below is the product and not the harness', async () => {
    const c = await issue('fixture');
    expect(typeof c?.id).toBe('string');
  });

  it('RED KS-1375 E-CRED: a revoked credential resubmitted with an EDITED id is refused', async () => {
    const c = await issue('edit-cred');
    const rev = await cred('POST', `/${encodeURIComponent(c.id)}/revoke`, { reason: 'KS-1375 edit' });
    expect(rev.status).toBe(200);
    const v = await verifyCred({ ...c, id: 'urn:uuid:ks1375-some-other-id' });
    expect({ verified: v.verified, statusCheck: v.statusCheck, reason: saysNoIssuerRecord(v.errors) })
      .toEqual({ verified: false, statusCheck: false, reason: true });
  });

  it('RED KS-1375 U-CRED: an id that was NEVER issued is refused with the reason', async () => {
    const c = await issue('unknown-cred');
    const v = await verifyCred({ ...c, id: 'urn:uuid:ks1375-never-issued' });
    expect({ verified: v.verified, statusCheck: v.statusCheck, reason: saysNoIssuerRecord(v.errors) })
      .toEqual({ verified: false, statusCheck: false, reason: true });
  });

  it('RED KS-1375 E-PRES: the same edited id is refused on the PRESENTATIONS route', async () => {
    const c = await issue('edit-pres');
    const rev = await cred('POST', `/${encodeURIComponent(c.id)}/revoke`, { reason: 'KS-1375 edit pres' });
    expect(rev.status).toBe(200);
    const v = await verifyInPresentation({ ...c, id: 'urn:uuid:ks1375-other-id-pres' });
    expect({ cred: v.credentialVerified, all: v.allCredentialsValid, reason: saysNoIssuerRecord(v.errors) })
      .toEqual({ cred: false, all: false, reason: true });
  });

  it('RED KS-1375 U-PRES: a never-issued id is refused on the PRESENTATIONS route', async () => {
    const c = await issue('unknown-pres');
    const v = await verifyInPresentation({ ...c, id: 'urn:uuid:ks1375-never-issued-pres' });
    expect({ cred: v.credentialVerified, all: v.allCredentialsValid, reason: saysNoIssuerRecord(v.errors) })
      .toEqual({ cred: false, all: false, reason: true });
  });

  it('control KS-1375: a genuine unrevoked credential still verifies on the credentials route', async () => {
    const c = await issue('control-cred');
    const v = await verifyCred(c);
    expect({ verified: v.verified, statusCheck: v.statusCheck }).toEqual({ verified: true, statusCheck: true });
  });

  it('control KS-1375: a genuine unrevoked credential still verifies on the presentations route', async () => {
    const c = await issue('control-pres');
    const v = await verifyInPresentation(c);
    expect({ cred: v.credentialVerified, all: v.allCredentialsValid })
      .toEqual({ cred: true, all: true });
  });

  it('control KS-1375: a credential revoked by its OWN id still fails for REVOCATION, not for a missing record', async () => {
    const c = await issue('own-id-revoke');
    const rev = await cred('POST', `/${encodeURIComponent(c.id)}/revoke`, { reason: 'KS-1375 own id' });
    expect(rev.status).toBe(200);
    const v = await verifyCred(c);
    expect({
      verified: v.verified,
      saysRevoked: mentionsRevocation(v.errors),
      saysNoRecord: saysNoIssuerRecord(v.errors),
    }).toEqual({ verified: false, saysRevoked: true, saysNoRecord: false });
  });

  it('control KS-1375 C4: a verifier with NO storedRecordResolver is UNCHANGED by this ticket', async () => {
    const c = await issue('no-resolver');
    // No config at all: the stored arm is not wired, so the unknown id must NOT start failing.
    const r = await verifyCredential({ ...c, id: 'urn:uuid:ks1375-unwired' } as never, {});
    // `errors` is OPTIONAL on CredentialVerificationResult (types.ts:202) and is UNDEFINED when
    // there are none -- calling .some() on it directly crashed this cell rather than measuring it.
    const errors = r.errors ?? [];
    expect({
      verified: r.verified,
      saysNoRecord: errors.some((e: string) => /no issuer record/i.test(e)),
    }).toEqual({ verified: true, saysNoRecord: false });
  });
});
