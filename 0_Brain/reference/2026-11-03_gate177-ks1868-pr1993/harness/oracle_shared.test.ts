// Gate 177 mutant oracle (shared): asserts the class bar for every value class V01-V17 at the three shared sites.
// verify(): resolves, verified false, signature false, one 'Signature verification error: <string>' entry.
// resolveDID(): resolves, didDocument null, error notFound, errorMessage a string. healthCheck(): resolves, healthy false, error a string.
import { it, expect, vi } from 'vitest';
import { VerifiableCredentialVerifier } from '../vc/verifier';
import { IdentusClient } from '../prism/identus-client';
import { ServiceClient } from '../resilience/service-client';
import { VALUES } from './values';
const V17 = VALUES.filter(([n]) => !n.startsWith('V18') && !n.startsWith('V19'));
const cred = { '@context': ['https://www.w3.org/2018/credentials/v1'], id: 'urn:x', type: ['VerifiableCredential'], issuer: 'did:example:i',
  issuanceDate: '2026-01-01T00:00:00Z', credentialSubject: { id: 'did:example:s' },
  proof: { type: 'X', created: '2026-01-01T00:00:00Z', verificationMethod: 'did:example:i#k', proofPurpose: 'assertionMethod', proofValue: 'zHMAC_x' } };
for (const [name, mk] of V17) {
  it(`oracle verify ${name}`, async () => {
    let n = 0;
    const v = new VerifiableCredentialVerifier({ didResolver: async () => { if (++n === 1) throw mk(); return { publicKey: 'k', verified: true }; } });
    const r = await v.verify(cred as any);
    expect(r.verified).toBe(false);
    expect(r.checks.signature).toBe(false);
    expect(r.errors?.length).toBe(1);
    expect(r.errors?.[0]).toMatch(/^Signature verification error: /);
  });
  it(`oracle resolveDID ${name}`, async () => {
    vi.stubGlobal('fetch', async () => { throw mk(); });
    const r = await new IdentusClient({ cloudAgentUrl: 'http://agent.invalid' }).resolveDID('did:prism:x');
    vi.unstubAllGlobals();
    expect(r.didDocument).toBeNull();
    expect(r.didResolutionMetadata.error).toBe('notFound');
    expect(typeof r.didResolutionMetadata.errorMessage).toBe('string');
  });
  it(`oracle healthCheck ${name}`, async () => {
    vi.stubGlobal('fetch', async () => { throw mk(); });
    const r = await new ServiceClient({ baseUrl: 'http://svc.invalid', serviceName: 'o', retries: 0 }).healthCheck();
    vi.unstubAllGlobals();
    expect(r.healthy).toBe(false);
    expect(typeof r.error).toBe('string');
  });
}
