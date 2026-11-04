// Gate 186 matrix harness: mocks copied verbatim from ks1236-approve-never-lowers-a-subjects-verification-level.test.ts (lines 18-~122); real userRoutes + errorHandler.
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import type { AddressInfo } from 'node:net';
import type { Server } from 'node:http';
import express from 'express';

type Row = Record<string, unknown>;
const state = vi.hoisted(() => ({
  caller: { userId: 'admin', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' } as Record<string, string>,
  users: new Map<string, Record<string, unknown>>(),
  rows: new Map<string, Record<string, unknown>>(),
  calls: [] as string[],
  levelReadFails: false,
}));

const dbQuery = vi.hoisted(() => vi.fn(async (sql: string, params: unknown[] = []) => {
  if (sql.includes('INSERT INTO verification_upgrade_requests')) {
    state.calls.push('save:' + String(params[5]));
    state.rows.set(String(params[0]), { id: params[0], user_id: params[1], current_level: params[2], target_level: params[3], documents: params[4], status: params[5], submitted_at: params[6], reviewed_at: params[7], reviewed_by: params[8], rejection_reason: params[9] });
    return { rows: [], rowCount: 1 };
  }
  if (sql.includes('WHERE id = $1')) return { rows: state.rows.has(String(params[0])) ? [state.rows.get(String(params[0]))] : [] };
  return { rows: [] };
}));

vi.mock('../repositories/userRepo', () => {
  const repoMock = {
    getUserById: vi.fn(async (id: string) => state.users.get(id) ?? null),
    getUserByIdPlatformScope: vi.fn(async (id: string) => {
      if (state.levelReadFails) throw Object.assign(new Error('connect ECONNREFUSED 127.0.0.1:5432'), { code: 'ECONNREFUSED' });
      return state.users.get(id) ?? null;
    }),
    updateUser: vi.fn(async () => null),
    updateUserOrThrow: vi.fn(async () => null),
    updateUserPlatformScope: vi.fn(async (id: string, updates: Record<string, unknown>) => {
      state.calls.push('raise');
      const row = state.users.get(id);
      if (row) Object.assign(row, updates);
      return row ?? null;
    }),
    listUsers: vi.fn(async () => []),
    countUsers: vi.fn(async () => 0),
    listOrganizations: vi.fn(async () => []),
    getOrganizationTenant: vi.fn(async () => ({ tenantId: 'tenant-default' })),
    emailExists: vi.fn(async () => false),
    createUser: vi.fn(async (user: Record<string, unknown>) => user),
    createInvitedStub: vi.fn(async () => ({ user: {}, alreadyExisted: false })),
  };
  return { default: repoMock, __esModule: true, ...repoMock };
});
vi.mock('../middleware/authenticate', () => {
  const injectCaller = () => (req: express.Request & { user?: unknown }, _res: express.Response, next: express.NextFunction) => {
    (req as { user: unknown }).user = { ...state.caller };
    next();
  };
  return { authenticate: injectCaller, authenticateAccessOrConnector: injectCaller };
});
vi.mock('../db', () => ({ isDbAvailable: () => true, query: dbQuery }));
vi.mock('../services/session', () => ({ revokeAllUserSessions: vi.fn(async () => 0) }));
vi.mock('../services/password', () => ({
  hashPassword: vi.fn(async () => 'hashed'),
  checkPasswordStrength: vi.fn(() => ({ ok: true })),
  verifyPassword: vi.fn(async () => true),
}));
vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() } }));

import { userRoutes } from '../routes/users';
import { errorHandler } from '../middleware/errorHandler';

let server: Server;
let baseUrl: string;

beforeAll(async () => {
  const app = express();
  app.use(express.json());
  app.use('/', userRoutes);
  app.use(errorHandler);
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => {
      baseUrl = 'http://127.0.0.1:' + String((server.address() as AddressInfo).port);
      resolve();
    });
  });
});
afterAll(async () => { await new Promise<void>((resolve) => server.close(() => resolve())); });
beforeEach(() => {
  vi.clearAllMocks();
  state.users.clear();
  state.rows.clear();
  state.calls = [];
  state.levelReadFails = false;
});

function subject(id: string, level: string): void {
  state.users.set(id, { id, email: id + '@tenant.example', role: 'USER', status: 'ACTIVE', verificationLevel: level, mfaEnabled: false, tenantId: 'tenant-default' });
}
function pending(id: string, userId: string, target: string): void {
  state.rows.set(id, { id, user_id: userId, current_level: 'BASIC', target_level: target, documents: [], status: 'PENDING', submitted_at: '2026-09-17T00:00:00.000Z', reviewed_at: null, reviewed_by: null, rejection_reason: null });
}
const asPlatformAdmin = (): void => { state.caller = { userId: 'admin-1236', role: 'SYSTEM_ADMIN', tenantId: 'tenant-default' }; };
const asTenantAdmin = (): void => { state.caller = { userId: 'org-admin-1236', role: 'ORG_ADMIN', tenantId: 'tenant-default' }; };
async function review(requestId: string, action: string): Promise<{ status: number; json: Row }> {
  const res = await fetch(baseUrl + '/verification/' + requestId + '/review', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ action }) });
  return { status: res.status, json: (await res.json()) as Row };
}
const code = (json: Row): unknown => (json.error as Row | undefined)?.code;
import { writeFileSync } from 'node:fs';

const LEVELS = ['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT', 'WEIRD', 'social', 'none'];
const SUBMIT_TARGETS = ['STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT', 'NONE', 'BASIC', 'SOCIAL'];
const out: Record<string, unknown>[] = [];

async function submit(target: string): Promise<{ status: number; json: Row }> {
  const res = await fetch(baseUrl + '/me/verification', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ targetLevel: target }) });
  return { status: res.status, json: (await res.json()) as Row };
}

describe('gate186 matrix', () => {
  it('review approve: every current x target', async () => {
    for (const asTenant of [false, true]) {
      for (const current of LEVELS) {
        for (const target of LEVELS) {
          state.users.clear(); state.rows.clear(); state.calls = [];
          if (asTenant) asTenantAdmin(); else asPlatformAdmin();
          subject('u-g', current); pending('vr-g', 'u-g', target);
          const r = await review('vr-g', 'approve');
          out.push({ route: 'review', caller: asTenant ? 'ORG_ADMIN' : 'SYSTEM_ADMIN', current, target, status: r.status, code: code(r.json) ?? null, level: state.users.get('u-g')?.verificationLevel, row: state.rows.get('vr-g')?.status, calls: state.calls.join(',') });
        }
      }
    }
  });
  it('submit: every current x target', async () => {
    for (const current of LEVELS) {
      for (const target of SUBMIT_TARGETS) {
        state.users.clear(); state.rows.clear(); state.calls = [];
        state.caller = { userId: 'u-s', role: 'USER', tenantId: 'tenant-default' };
        subject('u-s', current);
        const r = await submit(target);
        out.push({ route: 'submit', caller: 'USER', current, target, status: r.status, code: code(r.json) ?? null, level: state.users.get('u-s')?.verificationLevel, row: [...state.rows.values()][0]?.status ?? null, calls: state.calls.join(',') });
      }
    }
    writeFileSync(process.env.GATE_OUT as string, JSON.stringify(out, null, 1));
  });
});
