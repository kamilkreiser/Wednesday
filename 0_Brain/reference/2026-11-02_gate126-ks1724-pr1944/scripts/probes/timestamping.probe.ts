// QA GATE 126 probe (not part of the PR): the REAL timestamping index.ts app (default 100kb parser), no DB.
// POST /api/timestamps (single, rfc3161) and POST /api/timestamps/batch, real RS256 bearer. Side effect observed: the
// OUTBOUND TSA call (qualified-tsa createTimestamp, replaced by a counting stub so nothing leaves the host).
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import { token, setJwtEnv, shapes, boot, close, send, record, captureCapLines, countNodes, type Booted } from './zz-gate126-common';

const h = vi.hoisted(() => ({ tsa: 0 }));
vi.mock('../tsa/qualified-tsa', async (orig) => {
  const m: any = await orig();
  return { ...m, createTimestamp: async () => { h.tsa += 1; return { token: Buffer.from('gate126').toString('base64'), timestamp: new Date('2026-11-02T00:00:00Z'), tsaUrl: 'http://127.0.0.1:9/tsa', tsaName: 'gate126-stub', serialNumber: '1', eidasQualified: false, verified: true }; } };
});
const TENANT = 'a0000000-0000-4000-8000-000000000126';
const ORG = '1a126000-0000-4000-8000-000000000126';
const tok = () => token({ userId: 'b0000000-0000-4000-8000-000000000126', role: 'admin', organizationId: ORG, tenantId: TENANT });
let seq = 0;
const hex = () => { seq += 1; return seq.toString(16).padStart(64, 'd'); };

let b: Booted; let cap: ReturnType<typeof captureCapLines>;
beforeAll(async () => { setJwtEnv(); b = await boot(() => import('../index')); cap = captureCapLines(); }, 60000);
afterAll(async () => { cap.restore(); await close(b); });

async function run(route: string, path: string, name: string, body: unknown, raw?: string, ct = 'application/json') {
  const t0 = h.tsa; const before = cap.lines.length;
  const r = await send(b, path, raw ?? JSON.stringify(body), { 'Content-Type': ct, Authorization: `Bearer ${tok()}` });
  await new Promise((x) => setTimeout(x, 20));
  record({ svc: 'timestamping', route, case: name, nodes: body === undefined ? undefined : countNodes(body), status: r.status, body: r.body.replace(/"(id|createdAt|timestamp|hash|token|proof|serialNumber)":"[^"]*"/g, '"$1":"~"'), tsaCalls: h.tsa - t0, capLines: cap.lines.slice(before), ms: r.ms });
}

describe('gate126 timestamping', () => {
  it('single + batch: shapes, edges, liveness', async () => {
    for (const name of Object.keys(shapes({ hash: hex() }))) await run('POST /api/timestamps', '/api/timestamps', name, shapes({ hash: hex(), timestampType: 'rfc3161' })[name]);
    for (const name of Object.keys(shapes({ hashes: [] }))) await run('POST /api/timestamps/batch', '/api/timestamps/batch', name, shapes({ hashes: [{ hash: hex() }, { hash: hex() }], timestampType: 'rfc3161' })[name]);
    await run('POST /api/timestamps/batch', '/api/timestamps/batch', 'batch_101_items_schema_cap', { hashes: Array.from({ length: 101 }, () => ({ hash: hex() })) });
    await run('POST /api/timestamps', '/api/timestamps', 'edge_text_plain', undefined, JSON.stringify({ hash: hex(), pad: Array(5000).fill(1) }), 'text/plain');
    await run('POST /api/timestamps', '/api/timestamps', 'edge_malformed', undefined, '{"hash": [', 'application/json');
    await run('POST /api/timestamps', '/api/timestamps', 'liveness_after_all', { hash: hex() });
  }, 240000);
});
