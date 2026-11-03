// Gate 177 note cells (PRE-EXISTING check, not the PR's lines): verify() with NO didResolver, the config both vc-issuer
// callers use. A forged Ed25519-form proof 'zFORGED…', and a zDEV_ proof HMAC'd with the source's default dev key.
import { it } from 'vitest';
import { appendFileSync } from 'node:fs';
import { createHmac } from 'node:crypto';
import { VerifiableCredentialVerifier } from '../vc/verifier';
const OUT = process.env.GATE177_OUT!;
const body = { '@context': ['https://www.w3.org/2018/credentials/v1'], id: 'urn:gate177:forged', type: ['VerifiableCredential'], issuer: 'did:example:anyone',
  issuanceDate: '2026-01-01T00:00:00Z', credentialSubject: { id: 'did:example:s', documentHash: 'h' } };
const proof = { type: 'Ed25519Signature2020', created: '2026-01-01T00:00:00Z', verificationMethod: 'did:example:anyone#key-1', proofPurpose: 'assertionMethod' };
it('gate177 no-resolver note cells', async () => {
  const payload = JSON.stringify({ credential: { ...body, proof: undefined }, created: proof.created, verificationMethod: proof.verificationMethod, proofPurpose: 'assertionMethod' });
  const dev = 'zDEV_' + createHmac('sha256', 'secuura-dev-signing-key').update(payload).digest('base64url');
  for (const [name, pv] of [['forged Ed25519-form zFORGED', 'zFORGEDgate177'], ['zDEV_ HMAC with the default dev key', dev], ['control: unknown prefix xBAD', 'xBAD']]) {
    const r = await new VerifiableCredentialVerifier({}).verify({ ...body, proof: { ...proof, proofValue: pv } } as any);
    appendFileSync(OUT, JSON.stringify({ NODE_ENV: process.env.NODE_ENV, VC_SIGNING_KEY_set: process.env.VC_SIGNING_KEY !== undefined, cell: name, verified: r.verified, signature: r.checks.signature, errors: r.errors }) + '\n');
  }
});
