ROUTE = 'Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts'
GATE = 'Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts'
TDIR = 'Blockchain/Dev/services/nft-certificate/src/__tests__/'
REF = TDIR + 'ks1836-nft-list-owner-bound.test.ts'
RUNNER = 'vitest` (`npx vitest run src/__tests__/<the new file>` from `Blockchain/Dev/services/nft-certificate`; hoisted vitest, run from the package like the sibling KS-1836 files'
GATE_NOTE = "QA gate 23 on PR 1819 (KS-1836, merged as e3d8456ec81d), `0_Brain/reference/2026-10-30_gate23-1819/verdict.md` finding F1 and its mutant scripts."
HARNESS = r'''import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import express from 'express';
import type { Server } from 'http';
import type { AddressInfo } from 'net';

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
    throw new Error(`ks1836 log fake table: unexpected SQL: ${sql.slice(0, 80)}`);
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

const W_A = 'addr_test1_ks1836log_wallet_a';
const W_B = 'addr_test1_ks1836log_wallet_b';
const B_KEY = 'ENC-KEY-B1-ks1836log';
const NARROWED = 'NFT certificate list narrowed to the caller';

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
  row('a1', 'user-A', W_A, 1, 'ENC-KEY-A1-ks1836log'),
  row('a2', 'user-A', W_A, 2),
  row('b1', 'user-B', W_B, 3, B_KEY),
];

const CALLER_A = { userId: 'user-A', email: 'a@example.test', role: 'ISSUER', tenantId: 'tenant-1', verificationLevel: 'basic' };
// user-Z owns no row in the fixture: its fetched set is empty on every path.
const CALLER_Z = { userId: 'user-Z', email: 'z@example.test', role: 'ISSUER', tenantId: 'tenant-1', verificationLevel: 'basic' };
const EMPTY_BODY = JSON.stringify({ success: true, data: { certificates: [], count: 0 } });

let server: Server;
let base = '';
const logCalls: Array<{ level: string; message: unknown; meta: unknown }> = [];

beforeEach(async () => {
  vi.resetModules();
  table.rows = FIXTURE.map(r => ({ ...r }));
  logCalls.length = 0;
  const logger: any = (await import('../utils/logger')).logger;
  for (const level of ['error', 'warn', 'info', 'debug'] as const) {
    vi.spyOn(logger, level).mockImplementation(((message: unknown, meta: unknown) => {
      logCalls.push({ level, message, meta });
      return logger;
    }) as any);
  }
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
    headers: user === undefined ? {} : { 'x-ks1836-user': JSON.stringify(user) },
  });
  const text = await res.text();
  let json: any;
  try { json = JSON.parse(text); } catch { json = undefined; }
  return { status: res.status, text, json };
}

const ids = (r: { json: any }) => (r.json?.data?.certificates ?? []).map((c: any) => c.id);
const narrowedLogs = () => logCalls.filter(c => c.level === 'warn' && c.message === NARROWED);
'''
