// QA GATE 126 probe (not part of the PR): the REAL vc-issuer index.ts app (limit 10mb), no DB (in-memory).
// Routes: POST /api/credentials/verify (public), POST /api/presentations/verify (public), POST /api/credentials (issue,
// real RS256 bearer). Side effect observed on issue: credentialRepo.store calls (wrapped, real implementation kept).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import { token, setJwtEnv, shapes, boot, close, send, record, captureCapLines, countNodes, type Booted } from './zz-gate126-common';

const h = vi.hoisted(() => ({ stores: 0 }));
vi.mock('../repositories/credentialRepo', async (orig) => {
  const m: any = await orig();
  return { ...m, store: async (...a: unknown[]) => { h.stores += 1; return m.store(...a); } };
});

const LARGEST_CREDENTIAL = {
  '@context': ['https://www.w3.org/2018/credentials/v1'], id: 'urn:vc:g126', type: ['VerifiableCredential', 'SecuuraCredential'],
  issuer: { id: 'did:secuura:issuer-1', name: 'Issuer' }, issuanceDate: '2026-11-02T00:00:00.000Z',
  credentialSubject: { id: 'did:secuura:holder-1', documentHash: 'sha256:abc' },
  credentialStatus: { id: 'urn:status:1', type: 'StatusList2021', revoked: false },
  proof: { type: 'Ed25519Signature2020', created: '2026-01-01', verificationMethod: 'did:secuura:issuer-1#k', proofPurpose: 'assertionMethod', proofValue: 'z...' },
};
const TENANT = 'a0000000-0000-4000-8000-000000000126';
const ORG = '1a126000-0000-4000-8000-000000000126';
const tok = () => token({ userId: 'b0000000-0000-4000-8000-000000000126', sub: 'b0000000-0000-4000-8000-000000000126', role: 'admin', organizationId: ORG, tenantId: TENANT });
let seq = 0;
const issueValid = () => { seq += 1; return { documentId: `g126-doc-${seq}`, documentHash: 'c'.repeat(64), documentType: 'DocumentCertification', documentTitle: `Gate 126 ${seq}` }; };

let b: Booted; let cap: ReturnType<typeof captureCapLines>;
beforeAll(async () => { setJwtEnv(); delete process.env.VC_ISSUANCE_DISABLED; process.env.VC_SIGNING_KEY = crypto.generateKeyPairSync('ed25519').privateKey.export({ type: 'pkcs8', format: 'der' }).toString('hex'); b = await boot(() => import('../index')); cap = captureCapLines(); }, 60000);
afterAll(async () => { cap.restore(); await close(b); });

async function run(route: string, path: string, name: string, body: unknown, raw?: string, ct = 'application/json', auth = false) {
  const headers: Record<string, string> = { 'Content-Type': ct };
  if (auth) headers.Authorization = `Bearer ${tok()}`;
  const s0 = h.stores; const before = cap.lines.length;
  const r = await send(b, path, raw ?? JSON.stringify(body), headers);
  await new Promise((x) => setTimeout(x, 20));
  record({ svc: 'vc-issuer', route, case: name, nodes: body === undefined ? undefined : countNodes(body), status: r.status, body: r.body.replace(/"(id|issuanceDate|created|proofValue|jws|statusListIndex|statusListCredential)":"[^"]*"/g, '"$1":"~"'), storeDelta: h.stores - s0, capLines: cap.lines.slice(before), ms: r.ms });
}

describe('gate126 vc-issuer', () => {
  it('verify / presentation verify / issue: shapes, golden, edges, liveness', async () => {
    for (const [name, body] of Object.entries(shapes({ credential: LARGEST_CREDENTIAL }))) await run('POST /api/credentials/verify', '/api/credentials/verify', name, body);
    // the golden credential with ONE subject array at 1000 and at 1001 (inside the credential, as condition 4's control)
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'golden_subject_items_1000', { credential: { ...LARGEST_CREDENTIAL, credentialSubject: { ...LARGEST_CREDENTIAL.credentialSubject, items: Array(1000).fill(1) } } });
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'golden_subject_items_1001', { credential: { ...LARGEST_CREDENTIAL, credentialSubject: { ...LARGEST_CREDENTIAL.credentialSubject, items: Array(1001).fill(1) } } });
    const vp = { presentation: { '@context': ['https://www.w3.org/2018/credentials/v1'], type: ['VerifiablePresentation'], verifiableCredential: [LARGEST_CREDENTIAL] } };
    for (const [name, body] of Object.entries(shapes(vp))) await run('POST /api/presentations/verify', '/api/presentations/verify', name, body);
    for (const [name] of Object.entries(shapes(issueValid()))) await run('POST /api/credentials', '/api/credentials', name, shapes(issueValid())[name], undefined, 'application/json', true);
    // edges on the 10mb parser
    const wide: Record<string, unknown> = { credential: LARGEST_CREDENTIAL }; for (let i = 0; Object.keys(wide).length < 20001; i += 1) wide[`k${i}`] = i;
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_wide_object_20001_keys', wide);
    const wideOk: Record<string, unknown> = { credential: LARGEST_CREDENTIAL }; for (let i = 0; countNodes(wideOk) < 20000; i += 1) wideOk[`k${i}`] = i;
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_wide_object_at_20000_nodes', wideOk);
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_text_plain_overcap', undefined, JSON.stringify({ credential: LARGEST_CREDENTIAL, pad: Array(5000).fill(1) }), 'text/plain');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_form_urlencoded', undefined, 'a=1&b[]=2', 'application/x-www-form-urlencoded');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_empty_json', undefined, '', 'application/json');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_top_level_scalar', undefined, '7', 'application/json');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_malformed', undefined, '{"credential": ', 'application/json');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'edge_1mb_flat_array_524k', undefined, JSON.stringify({ credential: LARGEST_CREDENTIAL, pad: Array(524284).fill(0) }), 'application/json');
    await run('POST /api/credentials/verify', '/api/credentials/verify', 'liveness_after_all', { credential: LARGEST_CREDENTIAL });
  }, 300000);
});
