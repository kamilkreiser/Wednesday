// KS-1836: GET /api/nft/certificates took its owner from the query string (`?userId=`, default 'user-id') and let a
// `?walletAddress=` selector read any wallet, so any authenticated caller could list every recorded NFT. The fix binds
// the list to the verified caller (req.user.userId): rows come back only where the row's userId is the caller's, and
// both selectors can only narrow that set. A foreign selector answers the same empty 200 a caller with no rows gets
// (refusal reads as empty, never an existence oracle); the only 403 is a caller with no usable identity.
//
// The router runs on a small express app over an ephemeral port. A test-only middleware puts the identity on req.user,
// standing in for jwtAuthenticate (app.ts). The REAL minting service runs: the database boundary is a fake table that
// answers the service's own four SQL shapes and throws on any other, and the service's in-memory Map is real (fresh
// modules per cell). The chain module and the Blockfrost verifier are test doubles; no chain key is read or set.
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import express from 'express';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import { generateOpenApiDocument } from '@secuura/shared';
import '../nft-certificate.openapi';

type Row = Record<string, unknown>;

const table = vi.hoisted(() => ({ rows: [] as Record<string, unknown>[] }));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: async (text: string, params: unknown[] = []) => {
    const sql = text.replace(/\s+/g, ' ').trim();
    if (sql === 'SELECT * FROM svc_nft_certificates') return { rows: table.rows.slice() };
    if (sql === 'SELECT * FROM svc_nft_certificates WHERE id = $1') {
      return { rows: table.rows.filter(r => r.id === params[0]) };
    }
    if (sql === 'SELECT * FROM svc_nft_certificates WHERE user_id = $1 ORDER BY created_at DESC') {
      return { rows: table.rows.filter(r => r.user_id === params[0]) };
    }
    if (sql === 'SELECT * FROM svc_nft_certificates WHERE wallet_address = $1 ORDER BY created_at DESC') {
      return { rows: table.rows.filter(r => r.wallet_address === params[0]) };
    }
    throw new Error(`ks1836 fake table: unexpected SQL: ${sql.slice(0, 80)}`);
  },
}));

vi.mock('../cardano', () => ({
  isCardanoNFTReady: () => false,
  mintNFTOnChain: vi.fn(),
  getPolicyId: () => null,
  waitForNFTConfirmation: vi.fn(),
}));

vi.mock('../services/blockchain-verifier.service', () => ({
  blockchainVerifier: { verifyTransaction: vi.fn() },
}));

const W_A = 'addr_test1_ks1836_wallet_a';
const W_B = 'addr_test1_ks1836_wallet_b';
const W_SHARED = 'addr_test1_ks1836_wallet_shared';
const W_LEGACY = 'addr_test1_ks1836_wallet_legacy';
const W_MEM = 'addr_test1_ks1836_wallet_memory_only';
const B_KEY = 'ENC-KEY-B1-ks1836';

function row(id: string, userId: string, wallet: string, minute: number, encryptedKey: string | null = null): Row {
  return {
    id, certification_id: `cert-${id}`, user_id: userId, chain: 'cardano', wallet_address: wallet,
    policy_id: null, asset_name: null, asset_id: null, transaction_hash: null,
    storage_tier: 'basic', privacy_level: 'full_privacy', public_fields: '[]', status: 'minted',
    ipfs_cid: null, encrypted_key: encryptedKey, minting_cost: null, platform_fee: null, total_cost: null,
    error_message: null, created_at: new Date(Date.UTC(2026, 9, 29, 12, minute)),
    updated_at: new Date(Date.UTC(2026, 9, 29, 12, minute)), minted_at: null,
  };
}

const FIXTURE: Row[] = [
  row('a1', 'user-A', W_A, 1, 'ENC-KEY-A1-ks1836'),
  row('a2', 'user-A', W_SHARED, 2),
  row('b1', 'user-B', W_B, 3, B_KEY),
  row('b2', 'user-B', W_SHARED, 4),
  row('l1', 'user-id', W_LEGACY, 5),
];

const CALLER_A = { userId: 'user-A', email: 'a@example.test', role: 'ISSUER', tenantId: 'tenant-1', organizationId: 'org-1', verificationLevel: 'basic' };
const CALLER_Z = { userId: 'user-Z', email: 'z@example.test', role: 'ISSUER', tenantId: 'tenant-1', verificationLevel: 'basic' };
const EMPTY_BODY = JSON.stringify({ success: true, data: { certificates: [], count: 0 } });
const FORBIDDEN_BODY = { success: false, error: { code: 'FORBIDDEN', message: expect.any(String) } };

let server: Server;
let base = '';
let svc: any;
let logger: any;
let userSpy: ReturnType<typeof vi.spyOn>;
let walletSpy: ReturnType<typeof vi.spyOn>;
const logCalls: Array<{ level: string; message: unknown; meta: unknown }> = [];

beforeEach(async () => {
  vi.resetModules();
  table.rows = FIXTURE.map(r => ({ ...r }));
  logCalls.length = 0;
  logger = (await import('../utils/logger')).logger;
  for (const level of ['error', 'warn', 'info', 'debug'] as const) {
    vi.spyOn(logger, level).mockImplementation(((message: unknown, meta: unknown) => {
      logCalls.push({ level, message, meta });
      return logger;
    }) as any);
  }
  svc = await import('../services/minting.service');
  userSpy = vi.spyOn(svc.nftMintingService, 'getUserNFTCertificates');
  walletSpy = vi.spyOn(svc.nftMintingService, 'getWalletNFTCertificates');
  const routes = (await import('../routes/nft.routes')).default;
  const app = express();
  app.use((req, _res, next) => {
    const h = req.headers['x-ks1836-user'];
    if (typeof h === 'string') (req as any).user = JSON.parse(h);
    next();
  });
  app.use('/api/nft', routes);
  server = await new Promise<Server>(resolve => {
    const s = app.listen(0, '127.0.0.1', () => resolve(s));
  });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
});

afterEach(async () => {
  vi.restoreAllMocks();
  await new Promise<void>(resolve => server.close(() => resolve()));
});

async function get(path: string, user?: unknown): Promise<{ status: number; text: string; json: any }> {
  const res = await fetch(`${base}${path}`, {
    headers: user === undefined ? {} : { 'x-ks1836-user': JSON.stringify(user).replace(/[\u007f-\uffff]/g, (ch) => '\\u' + ch.charCodeAt(0).toString(16).padStart(4, '0')) },
  });
  const text = await res.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = undefined; }
  return { status: res.status, text, json };
}

const ids = (r: { json: any }) => (r.json?.data?.certificates ?? []).map((c: any) => c.id);

const LEG_IDS = ['l1'];
const forbidden = (r: any) => r.status === 403 && r.json?.error?.code === 'FORBIDDEN';

describe('GATE23 attack: query-selector bypasses', () => {
  const cases: Array<[string, string]> = [
    ['userId=__proto__', '?userId=__proto__'],
    ['userId=constructor', '?userId=constructor'],
    ['userId[]=user-B', '?userId[]=user-B'],
    ['userId[]=user-A (own, array)', '?userId[]=user-A'],
    ['userId=user-B&userId=user-A', '?userId=user-B&userId=user-A'],
    ['userId[__proto__]=user-B', '?userId[__proto__]=user-B'],
    ['userId[toString]=x', '?userId[toString]=x'],
    ['userId=USER-B', '?userId=USER-B'],
    ['userId=%20user-B%20', '?userId=%20user-B%20'],
    ['userId=user-id', '?userId=user-id'],
    ['userId=%20user-A (padded own)', '?userId=%20user-A'],
    ['walletAddress[__proto__]=W_B', `?walletAddress[__proto__]=${W_B}`],
    ['walletAddress[a]=W_B', `?walletAddress[a]=${W_B}`],
    ['walletAddress=W_B&userId=user-B', `?walletAddress=${W_B}&userId=user-B`],
    ['walletAddress=W_LEGACY', `?walletAddress=${W_LEGACY}`],
    ['walletAddress=W_LEGACY&userId=user-id', `?walletAddress=${W_LEGACY}&userId=user-id`],
    ['walletAddress=%20 (space only)', `?walletAddress=%20`],
    ['walletAddress=%25 (sql wildcard)', `?walletAddress=%25`],
    ['walletAddress=W_B padded', `?walletAddress=%20${W_B}`],
  ];
  for (const [name, qs] of cases) {
    it(`A-Q ${name}: 200, no foreign/legacy row, no foreign id/key in body, service never sees non-string`, async () => {
      const r = await get(`/api/nft/certificates${qs}`, CALLER_A);
      expect(r.status).toBe(200);
      const got: string[] = ids(r);
      for (const id of got) expect(['a1', 'a2']).toContain(id);
      for (const needle of ['user-B', B_KEY, 'user-id', W_LEGACY]) expect(r.text.includes(needle), needle).toBe(false);
      for (const c of walletSpy.mock.calls) expect(typeof c[0]).toBe('string');
      for (const c of userSpy.mock.calls) expect(c[0]).toBe('user-A');
      // record for the verdict
      console.log(`GATE23 ${name} -> ${r.status} ids=${JSON.stringify(got)} wallet=${JSON.stringify(walletSpy.mock.calls)} user=${JSON.stringify(userSpy.mock.calls)}`);
    });
  }
});

describe('GATE23 attack: token identity variants', () => {
  const forbiddenIds: Array<[string, unknown]> = [
    ['User-Id', 'User-Id'], ['\\tuser-id\\n', '\tuser-id\n'], ['nbsp+user-id', ' user-id'], ['bom+user-id', '﻿user-id'],
    ['number 0', 0], ['number 1', 1], ['null', null], ['true', true], ['array [user-A]', ['user-A']],
    ['object', { toString: 'user-A' }], ['empty', ''],
  ];
  for (const [name, uid] of forbiddenIds) {
    it(`A-T403 token userId ${name} -> 403, no service call`, async () => {
      const r = await get('/api/nft/certificates', { ...CALLER_A, userId: uid });
      expect(forbidden(r)).toBe(true);
      expect(userSpy).not.toHaveBeenCalled();
      expect(walletSpy).not.toHaveBeenCalled();
    });
  }
  it('A-T403 user without userId but with sub/id -> 403', async () => {
    const { userId, ...rest } = CALLER_A as any;
    const r = await get('/api/nft/certificates', { ...rest, sub: 'user-A', id: 'user-A' });
    expect(forbidden(r)).toBe(true);
  });
  it('A-T403 user JSON with own __proto__ carrying userId -> 403', async () => {
    const res = await fetch(`${base}/api/nft/certificates`, { headers: { 'x-ks1836-user': '{"__proto__":{"userId":"user-B"},"role":"ISSUER"}' } });
    expect(res.status).toBe(403);
  });
  for (const [name, u] of [['string user', 'user-A'], ['array user', ['user-A']], ['number user', 7]] as Array<[string, unknown]>) {
    it(`A-T403 req.user is ${name} -> 403`, async () => {
      const r = await get('/api/nft/certificates', u);
      expect(forbidden(r)).toBe(true);
    });
  }
  const lookalikes: Array<[string, string]> = [
    ['U+2010 hyphen', 'user‐id'], ['U+2011 nb-hyphen', 'user‑id'], ['U+2212 minus', 'user−id'],
    ['fullwidth', 'ｕｓｅｒ-id'], ['cyrillic u/e', 'usеr-id'], ['dotless i', 'user-ıd'],
    ['ZWSP suffix', 'user-id​'], ['ZWJ inside', 'user-‍id'], ['combining', 'user-i̇d'],
    ['Turkish dotted I upper', 'USER-İD'], ['underscore', 'user_id'],
  ];
  for (const [name, uid] of lookalikes) {
    it(`A-T lookalike ${name}: never 403 required, but never receives a legacy row (bare, wallet, userId selector)`, async () => {
      const paths = ['/api/nft/certificates', `/api/nft/certificates?walletAddress=${W_LEGACY}`, '/api/nft/certificates?userId=user-id',
        `/api/nft/certificates?userId=${encodeURIComponent(uid)}`];
      for (const p of paths) {
        const r = await get(p, { ...CALLER_A, userId: uid });
        if (r.status === 403) continue;
        expect(r.status).toBe(200);
        expect(r.text).toBe(EMPTY_BODY);
      }
    });
  }
  it('A-T padded own token " user-A " reads user-A rows (trim is by design, G1) - recorded', async () => {
    const r = await get('/api/nft/certificates', { ...CALLER_A, userId: ' user-A ' });
    console.log(`GATE23 padded token -> ${r.status} ${JSON.stringify(ids(r))}`);
    expect(r.status).toBe(200);
  });
});

describe('GATE23 attack: memory-only rows and leaks', () => {
  it('A-M1 memory-only legacy and foreign rows: bare list, wallet, userId selectors all withhold', async () => {
    table.rows = [row('m1', 'user-B', W_MEM, 6, B_KEY), row('m2', 'user-id', W_MEM, 7, 'ENC-LEG'), row('m3', 'user-A', W_MEM, 8)];
    await svc.loadFromDb();
    table.rows = [];
    const want = JSON.stringify({ success: true, data: { certificates: [], count: 0 } });
    for (const p of [`?walletAddress=${W_MEM}&userId=user-B`, '?userId=user-B', '?userId=user-id', `?walletAddress=${W_MEM}&userId=user-id`]) {
      const r = await get(`/api/nft/certificates${p}`, CALLER_A);
      expect(r.text, p).toBe(want);
    }
    const own = await get(`/api/nft/certificates?walletAddress=${W_MEM}`, CALLER_A);
    expect(ids(own)).toEqual(['m3']);
    const bare = await get('/api/nft/certificates', CALLER_A);
    expect(ids(bare)).toEqual(['m3']);
    for (const t of [own.text, bare.text]) for (const n of ['user-B', B_KEY, 'ENC-LEG', '"user-id"']) expect(t.includes(n), n).toBe(false);
  });
  it('A-M2 row with non-string / null user_id is withheld', async () => {
    table.rows = [row('n1', null as any, W_A, 9), row('n2', 'user-A ', W_A, 10)];
    const r = await get(`/api/nft/certificates?walletAddress=${W_A}`, CALLER_A);
    console.log(`GATE23 padded-row/null-row -> ${JSON.stringify(ids(r))}`);
    expect(ids(r)).not.toContain('n1');
  });
  it('A-L1 count/ordering: foreign wallet with 0, 1 and 50 rows answers byte-identical bodies', async () => {
    table.rows = [];
    for (let i = 0; i < 50; i++) table.rows.push(row(`f${i}`, 'user-B', 'addr_many', i % 59, B_KEY));
    table.rows.push(row('one', 'user-B', 'addr_one', 1, B_KEY));
    const a = await get('/api/nft/certificates?walletAddress=addr_none', CALLER_A);
    const b = await get('/api/nft/certificates?walletAddress=addr_one', CALLER_A);
    const c = await get('/api/nft/certificates?walletAddress=addr_many', CALLER_A);
    expect(a.text).toBe(EMPTY_BODY); expect(b.text).toBe(EMPTY_BODY); expect(c.text).toBe(EMPTY_BODY);
    expect(a.status).toBe(b.status); expect(b.status).toBe(c.status);
  });
  it('A-L2 log lines: foreign read logs no foreign owner id and no key; logs record withheld count', async () => {
    await get(`/api/nft/certificates?walletAddress=${W_SHARED}`, CALLER_A);
    await get('/api/nft/certificates?userId=user-B', CALLER_Z);
    const s = JSON.stringify(logCalls);
    console.log(`GATE23 logs: ${s}`);
    expect(s.includes('user-B') && !s.includes('"userIdSelector":"user-B"')).toBe(false);
    expect(s.includes(B_KEY)).toBe(false);
    expect(s.includes('ENC-KEY-A1')).toBe(false);
  });
  it('A-L3 error body on a wallet-path fault carries no wallet/owner', async () => {
    walletSpy.mockRejectedValueOnce(new Error(`boom ${W_B} user-B ${B_KEY}`));
    const r = await get(`/api/nft/certificates?walletAddress=${W_B}`, CALLER_A);
    expect(r.status).toBe(500);
    for (const n of [W_B, 'user-B', B_KEY]) expect(r.text.includes(n)).toBe(false);
    const s = JSON.stringify(logCalls);
    console.log(`GATE23 500 log carries foreign key? ${s.includes(B_KEY)}`);
  });
  it('A-L4 timing (informational): foreign wallet 0 vs 2000 rows', async () => {
    table.rows = [];
    for (let i = 0; i < 2000; i++) table.rows.push(row(`t${i}`, 'user-B', 'addr_big', i % 59, B_KEY));
    const time = async (w: string) => { const xs: number[] = []; for (let i = 0; i < 15; i++) { const t0 = performance.now(); await get(`/api/nft/certificates?walletAddress=${w}`, CALLER_A); xs.push(performance.now() - t0); } xs.sort((p, q) => p - q); return xs[7]; };
    const none = await time('addr_none'); const big = await time('addr_big');
    console.log(`GATE23 timing median ms: none=${none.toFixed(2)} big2000=${big.toFixed(2)}`);
  });
});

describe('GATE23 legit caller and other routes', () => {
  it('A-G1 connector-style userId "connector:api-key" is accepted (200), not 403', async () => {
    const r = await get('/api/nft/certificates', { ...CALLER_A, userId: 'connector:api-key', role: 'connector' });
    expect(r.status).toBe(200);
  });
  it('A-G2 a real uuid userId owning a row reads it', async () => {
    const u = '3f2a1c9e-0b7d-4e55-9a10-2c4b6d8e0f11';
    table.rows.push(row('u1', u, 'addr_u', 30));
    const r = await get('/api/nft/certificates', { ...CALLER_A, userId: u });
    expect(ids(r)).toEqual(['u1']);
  });
});
