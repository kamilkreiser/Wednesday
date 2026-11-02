// QA GATE 126 probe (not part of the PR): the REAL anchoring index.ts app (KS-1603/KS-1717 boot recipe), POST /api/anchors
// with a real RS256 connector bearer. Side effect observed: recordFlatAnchorProvenance (the handler's write) and the
// emitter-signature check (a SIGNED hop skips the recorder only if the signature verified over the exact raw bytes).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import { signEmitterHop } from '@secuura/shared';
import { token, setJwtEnv, shapes, boot, close, send, record, captureCapLines, countNodes, type Booted } from './zz-gate126-common';

vi.mock('../provenance', () => ({ recordFlatAnchorProvenance: vi.fn(async () => undefined) }));
const SECRET = 'gate126-anchoring-test-secret-0123456789abcdef';
const TENANT = 'a0000000-0000-4000-8000-000000000126';
const ORG = '1a126000-0000-4000-8000-000000000126';
const tok = () => token({ userId: 'connector:platform-s:gate126', role: 'connector', organizationId: ORG, tenantId: TENANT });
let seq = 0;
const valid = () => { seq += 1; return { documentId: `doc-${Date.now()}${seq}-g126s${seq}`, contentHash: 'b'.repeat(64), network: 'preview' }; };

let b: Booted; let rec: any; let cap: ReturnType<typeof captureCapLines>;
beforeAll(async () => {
  setJwtEnv(); delete process.env.PLATFORM_WALLET_MNEMONIC; delete process.env.BLOCKFROST_API_KEY;
  process.env.CARDANO_NETWORK = 'preview'; process.env.EMITTER_SIGNING_SECRET = SECRET;
  b = await boot(() => import('../index'));
  rec = (await import('../provenance')).recordFlatAnchorProvenance;
  cap = captureCapLines();
}, 60000);
afterAll(async () => { cap.restore(); await close(b); });

async function run(name: string, raw: string | undefined, ct: string | null, signed: boolean, nodes?: number) {
  const t = tok();
  const headers: Record<string, string> = { Authorization: `Bearer ${t}` };
  if (ct) headers['Content-Type'] = ct;
  if (signed && raw !== undefined) Object.assign(headers, signEmitterHop({ secret: SECRET, marker: 'originate-create', method: 'POST', url: `${b.base}/api/anchors`, authorization: `Bearer ${t}`, body: raw }));
  rec.mockClear(); const before = cap.lines.length;
  const r = await send(b, name.startsWith('edge_query') ? '/api/anchors?token=QUERY-SENTINEL' : '/api/anchors', raw, headers);
  await new Promise((x) => setTimeout(x, 30));
  record({ svc: 'anchoring', route: 'POST /api/anchors', case: name, signed, nodes, status: r.status, body: r.body, recorderCalls: rec.mock.calls.length, capLines: cap.lines.slice(before), ms: r.ms });
}

describe('gate126 anchoring', () => {
  it('shapes x unsigned/signed, edges, liveness', async () => {
    for (const signed of [false, true]) {
      for (const [name] of Object.entries(shapes(valid()))) {
        const body = shapes(valid())[name];
        // signed bodies are sent with odd whitespace, so a re-serialised body would NOT match the signature
        const raw = signed ? JSON.stringify(body, null, 3).replace(/\n/g, '\r\n ') : JSON.stringify(body);
        await run(name, raw, 'application/json', signed, countNodes(body));
      }
    }
    const v = valid();
    await run('edge_text_plain_overcap', JSON.stringify({ ...v, pad: Array(5000).fill(1) }), 'text/plain', false);
    await run('edge_empty_body_json_ct', '', 'application/json', false);
    await run('edge_no_body_no_ct', undefined, null, false);
    await run('edge_top_level_scalar_5', '5', 'application/json', false);
    await run('edge_top_level_string', '"x"', 'application/json', false);
    await run('edge_top_level_array_1001', JSON.stringify(Array(1001).fill(1)), 'application/json', false);
    await run('edge_top_level_array_1000', JSON.stringify(Array(1000).fill(1)), 'application/json', false);
    await run('edge_malformed', '{"documentId": "x", ', 'application/json', false);
    let deepObj: any = 1; for (let i = 0; i < 33; i += 1) deepObj = { a: deepObj };
    await run('edge_deep_objects_33', JSON.stringify(deepObj), 'application/json', false);
    let deepObj32: any = 1; for (let i = 0; i < 32; i += 1) deepObj32 = { a: deepObj32 };
    await run('edge_deep_objects_32', JSON.stringify(deepObj32), 'application/json', false);
    const wide: Record<string, unknown> = { ...valid() }; for (let i = 0; wide && Object.keys(wide).length < 20001; i += 1) wide[`k${i}`] = i;
    await run('edge_wide_object_20001_keys', JSON.stringify(wide), 'application/json', false, countNodes(wide));
    await run('edge_query_string_overcap', JSON.stringify({ ...valid(), pad: Array(1001).fill('VALUE-SENTINEL') }), 'application/json', false);
    await run('liveness_after_all', JSON.stringify(valid()), 'application/json', false);
  }, 240000);
});
