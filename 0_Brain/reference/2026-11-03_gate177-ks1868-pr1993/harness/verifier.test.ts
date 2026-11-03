// Gate 177 Q1 recorder: drives the REAL VerifiableCredentialVerifier.verify() (whichever verifier.ts blob swap.sh wrote).
// The credential is a REAL Ed25519-signed credential from the package's own signCredential (builder.ts), so every check
// other than the one under test passes; the only way verified can be true is a passing signature check.
// The Ed25519 key pair is generated in memory per run and never written anywhere.
import { it } from 'vitest';
import { appendFileSync } from 'node:fs';
import { generateKeyPairSync } from 'node:crypto';
import { VerifiableCredentialVerifier } from '../vc/verifier';
import { signCredential } from '../vc/builder';
import { VALUES, SENT, capture, kind, hits } from './values';

const OUT = process.env.GATE177_OUT!;
const TAG = process.env.GATE177_TAG!;
const rec = (o: Record<string, unknown>) => appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');
const norm = (s: unknown) => (typeof s === 'string' ? s.replace(/SNTL177[-\w]*/g, 'S') : `<${typeof s}>`);

const kp = generateKeyPairSync('ed25519');
const PRIV = (kp.privateKey.export({ format: 'der', type: 'pkcs8' }) as Buffer).toString('hex');
const PUB = (kp.publicKey.export({ format: 'der', type: 'spki' }) as Buffer).toString('hex');
const ISSUER = 'did:example:gate177-issuer';
const base = () => ({
  '@context': ['https://www.w3.org/2018/credentials/v1'],
  id: 'urn:uuid:gate177-cred',
  type: ['VerifiableCredential'],
  issuer: ISSUER,
  issuanceDate: '2026-01-01T00:00:00Z',
  credentialSubject: { id: 'did:example:subject', documentHash: 'abc', documentType: 'gate177' },
});
let SIGNED: any;
const ok = { publicKey: PUB, verified: true };

type Resolver = (did: string) => Promise<{ publicKey: string; verified: boolean }>;
// Each trigger: the proof value form and the resolver; `calls` counts resolver calls.
function trigger(t: string, mk: () => unknown, calls: { n: number }): { cred: any; resolver: Resolver } {
  const ed = SIGNED; // real Ed25519 credential (proofValue starts with 'z')
  const hmac = { ...SIGNED, proof: { ...SIGNED.proof, proofValue: 'zHMAC_gate177' } };
  const first = (onFirst: () => Promise<any>): Resolver => async () => (++calls.n === 1 ? onFirst() : ok);
  switch (t) {
    case 'T1 hmac: resolver rejects (signature call only)':
      return { cred: hmac, resolver: first(() => Promise.reject(mk())) };
    case 'T2 ed25519: resolver rejects (signature call only)':
      return { cred: ed, resolver: first(() => Promise.reject(mk())) };
    case 'T3 hmac: publicKey getter throws (outer try)':
      return { cred: hmac, resolver: first(async () => ({ verified: true, get publicKey(): string { throw mk(); } })) };
    case 'T4 ed25519: inner catch (publicKey getter throws on 2nd read)': {
      let r = 0;
      return { cred: ed, resolver: first(async () => ({ verified: true, get publicKey(): string { if (++r === 1) return PUB; throw mk(); } })) };
    }
    case 'T5 ed25519: resolver rejects on EVERY call (issuer DID too)':
      return { cred: ed, resolver: async () => { calls.n++; throw mk(); } };
  }
  throw new Error('bad trigger ' + t);
}
const TRIGGERS = [
  'T1 hmac: resolver rejects (signature call only)',
  'T2 ed25519: resolver rejects (signature call only)',
  'T3 hmac: publicKey getter throws (outer try)',
  'T4 ed25519: inner catch (publicKey getter throws on 2nd read)',
  'T5 ed25519: resolver rejects on EVERY call (issuer DID too)',
];

async function drive(cred: any, resolver: Resolver | undefined) {
  const v = new VerifiableCredentialVerifier(resolver ? { didResolver: resolver } : {});
  const { result, lines } = await capture(async () => {
    try {
      return { outcome: 'resolved', r: await v.verify(cred) } as const;
    } catch (e) {
      return { outcome: 'REJECTED', e } as const;
    }
  });
  return { result, lines };
}

it('gate177 Q1 verifier', async () => {
  SIGNED = await signCredential(base() as any, ISSUER, PRIV);
  // CONTROLS, no throw.
  const controls: Array<[string, any, Resolver | undefined]> = [
    ['C1 valid Ed25519, resolver returns the real key', SIGNED, async () => ok],
    ['C2 INVALID signature (subject tampered after signing)', { ...SIGNED, credentialSubject: { ...SIGNED.credentialSubject, documentHash: 'tampered' } }, async () => ok],
    ['C3 valid Ed25519 but resolver returns a DIFFERENT key', SIGNED, async () => ({ publicKey: (generateKeyPairSync('ed25519').publicKey.export({ format: 'der', type: 'spki' }) as Buffer).toString('hex'), verified: true })],
    ['C4 HMAC proof with wrong key', { ...SIGNED, proof: { ...SIGNED.proof, proofValue: 'zHMAC_gate177' } }, async () => ok],
    ['C5 valid Ed25519, NO resolver configured (NODE_ENV=test)', SIGNED, undefined],
  ];
  for (const [name, cred, res] of controls) {
    const { result, lines } = await drive(cred, res);
    const r: any = (result as any).r;
    rec({ q: 'Q1C', site: 'controls', value: name, outcome: result.outcome, verified: r?.verified, signature: r?.checks?.signature, issuerDID: r?.checks?.issuerDID, errors: (r?.errors ?? []).map(norm), logSentinel: hits(lines) });
  }
  for (const t of TRIGGERS) {
    for (const [vname, mk] of VALUES) {
      const calls = { n: 0 };
      let thrownOrig: unknown;
      const mk2 = () => (thrownOrig = mk());
      const { cred, resolver } = trigger(t, mk2, calls);
      const { result, lines } = await drive(cred, resolver);
      const r: any = (result as any).r;
      let answerSentinel = 0;
      try { answerSentinel = JSON.stringify(r ?? null).includes(SENT) ? 1 : 0; } catch { answerSentinel = -1; }
      rec({
        q: 'Q1', site: t, value: vname, outcome: result.outcome,
        verified: r?.verified, signature: r?.checks?.signature, issuerDID: r?.checks?.issuerDID,
        errors: r ? (r.errors ?? []).map(norm) : undefined,
        rejectKind: result.outcome === 'REJECTED' ? kind((result as any).e, thrownOrig) : undefined,
        resolverCalls: calls.n, answerSentinel, logSentinel: hits(lines),
      });
    }
  }
});
