// KS-1087 — workflow approve must keep the pending doc when originate fails
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { RequestHandler } from 'express';

const DOC_ID = 'doc-ks1087';
const WFI_ID = 'wfi-ks1087';
let gateway: Server | null = null;
let originator: Server | null = null;
let gatewayPort = 0;
let originatorPort = 0;
let currentOriginatorStatus = 201;
/** deletePendingDocument calls on the main gateway (read by the 401 cell and the control). */
let deleteCount = 0;

beforeAll(async () => {
  originator = http.createServer((_req, res) => {
    res.writeHead(currentOriginatorStatus, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ id: DOC_ID }));
  });
  originator.listen(0, '127.0.0.1');
  await new Promise<void>((r) => originator!.once('listening', () => r()));
  originatorPort = (originator.address() as AddressInfo).port;

  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
  const app = express();
  app.use(
    createVerificationRoutes({
      authenticateToken: () => (_req, _res, next) => next(),
      mockBodyParser,
      query: vi.fn(async () => ({ rows: [] })) as never,
      isDbAvailable: () => false,
      redisService: {
        getWorkflowInstance: vi.fn(async (id: string) =>
          id === WFI_ID ? { status: 'pending_approval', documentId: DOC_ID, steps: [{ name: 'Approve' }], currentStepIndex: 0 } : null,
        ),
        getAllWorkflowInstances: vi.fn(async () => []),
        setWorkflowInstance: vi.fn(async () => undefined),
        getPendingDocument: vi.fn(async (id: string) =>
          id === DOC_ID ? { title: 't', contentHash: 'h', createdBy: 'u' } : null,
        ),
        deletePendingDocument: vi.fn(async () => { deleteCount++; }),
      } as never,
      services: { originate: { url: `http://127.0.0.1:${originatorPort}` }, anchoring: { url: '' } } as never,
      log: () => undefined,
      memWorkflowToDocumentMap: new Map(),
      memRejectedDocuments: new Map(),
      dbSaveRejection: vi.fn(async () => undefined),
      ADMIN_ROLES: ['ADMIN'],
      enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
      createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
      meetsVerificationLevel: () => true,
    }),
  );
  gateway = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gateway!.once('listening', () => r()));
  gatewayPort = (gateway.address() as AddressInfo).port;
});

afterAll(async () => {
  if (gateway) await new Promise<void>((r) => gateway.close(() => r()));
  if (originator) await new Promise<void>((r) => originator.close(() => r()));
});

async function approve(): Promise<Response> {
  return fetch(`http://127.0.0.1:${gatewayPort}/api/workflow-instances/${WFI_ID}/approve`, { method: 'POST' });
}

describe('KS-1087 — workflow approve keeps pending doc on originate failure', () => {
  it('🔴 KS-1087 — originate 401: no 200 approved, and the pending document survives', async () => {
    currentOriginatorStatus = 401;
    const deletesBefore = deleteCount;
    const res = await approve();
    expect(res.status).not.toBe(200);
    expect(res.status).toBe(502);
    expect(deleteCount, 'the pending document survives a refused forward').toBe(deletesBefore);
  });

  it('🔴 KS-1087 — originate unreachable: the pending document survives', async () => {
    // Point at a closed port so http.request errors out immediately.
    const { createVerificationRoutes } = await import('../routes/verification');
    const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
    const deadApp = express();
    let _deadAppDeleteCount = 0;
    deadApp.use(
      createVerificationRoutes({
        authenticateToken: () => (_req, _res, next) => next(),
        mockBodyParser,
        query: vi.fn(async () => ({ rows: [] })) as never,
        isDbAvailable: () => false,
        redisService: {
          getWorkflowInstance: vi.fn(async (id: string) =>
            id === WFI_ID ? { status: 'pending_approval', documentId: DOC_ID, steps: [{ name: 'Approve' }], currentStepIndex: 0 } : null,
          ),
          getAllWorkflowInstances: vi.fn(async () => []),
          setWorkflowInstance: vi.fn(async () => undefined),
          getPendingDocument: vi.fn(async (id: string) =>
            id === DOC_ID ? { title: 't', contentHash: 'h', createdBy: 'u' } : null,
          ),
          deletePendingDocument: vi.fn(async () => { _deadAppDeleteCount++; }),
        } as never,
        services: { originate: { url: `http://127.0.0.1:1` }, anchoring: { url: '' } } as never,
        log: () => undefined,
        memWorkflowToDocumentMap: new Map(),
        memRejectedDocuments: new Map(),
        dbSaveRejection: vi.fn(async () => undefined),
        ADMIN_ROLES: ['ADMIN'],
        enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
        createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
        meetsVerificationLevel: () => true,
      }),
    );
    const deadServer = deadApp.listen(0, '127.0.0.1');
    await new Promise<void>((r) => deadServer.once('listening', () => r()));
    const _deadPort = (deadServer.address() as AddressInfo).port;
    // Re-mount with the unreachable URL by re-creating routes pointing at port 1.
    const unreachableApp = express();
    let uDeleteCount = 0;
    unreachableApp.use(
      createVerificationRoutes({
        authenticateToken: () => (_req, _res, next) => next(),
        mockBodyParser,
        query: vi.fn(async () => ({ rows: [] })) as never,
        isDbAvailable: () => false,
        redisService: {
          getWorkflowInstance: vi.fn(async (id: string) =>
            id === WFI_ID ? { status: 'pending_approval', documentId: DOC_ID, steps: [{ name: 'Approve' }], currentStepIndex: 0 } : null,
          ),
          getAllWorkflowInstances: vi.fn(async () => []),
          setWorkflowInstance: vi.fn(async () => undefined),
          getPendingDocument: vi.fn(async (id: string) =>
            id === DOC_ID ? { title: 't', contentHash: 'h', createdBy: 'u' } : null,
          ),
          deletePendingDocument: vi.fn(async () => { uDeleteCount++; }),
        } as never,
        services: { originate: { url: `http://127.0.0.1:1` }, anchoring: { url: '' } } as never,
        log: () => undefined,
        memWorkflowToDocumentMap: new Map(),
        memRejectedDocuments: new Map(),
        dbSaveRejection: vi.fn(async () => undefined),
        ADMIN_ROLES: ['ADMIN'],
        enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
        createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
        meetsVerificationLevel: () => true,
      }),
    );
    const reachableGateway = unreachableApp.listen(0, '127.0.0.1');
    await new Promise<void>((r) => reachableGateway.once('listening', () => r()));
    const reachablePort = (reachableGateway.address() as AddressInfo).port;
    try {
      const res = await fetch(`http://127.0.0.1:${reachablePort}/api/workflow-instances/${WFI_ID}/approve`, { method: 'POST' });
      expect(res.status).not.toBe(200);
      expect(uDeleteCount).toBe(0);
    } finally {
      await new Promise<void>((r) => reachableGateway.close(() => r()));
      await new Promise<void>((r) => deadServer.close(() => r()));
    }
  });

  it('KS-1087 control — originate 201: approved and the pending document is deleted', async () => {
    currentOriginatorStatus = 201;
    const deletesBefore = deleteCount;
    const res = await approve();
    expect(res.status).toBe(200);
    expect(deleteCount - deletesBefore, 'the pending document is deleted once originate accepts').toBe(1);
    const body = await res.json();
    expect(body.success).toBe(true);
    expect(body.message).toContain('created');
  });
});
