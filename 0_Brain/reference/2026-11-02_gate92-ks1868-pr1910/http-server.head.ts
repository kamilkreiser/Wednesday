#!/usr/bin/env node
/**
 * HTTP/REST server that mirrors the MCP tools as REST endpoints.
 * Designed for ChatGPT Actions and other HTTP-based AI agent integrations.
 * Start with: npx tsx src/http-server.ts
 */
import express from 'express';
import { hashFile, extractFileName, hashBuffer } from './hashing.js';
import {
  registerDocument,
  verifyDocument,
  listDocuments,
  getWorkflowInstance,
  getConnectorInfo,
  getVerificationPolicy,
} from './api-client.js';
import { generatePackage } from './package-generator.js';
import type { AgentType } from './package-generator.js';
import { enforceProductionConfig, rejectNulBytes } from '@secuura/shared';

// Production startup guard — refuse to start with dev defaults in production
enforceProductionConfig('mcp-server', {
  requiredEnvVars: ['DATABASE_URL'],
  forbiddenValues: {},
  requireRealProviders: true,
});

const app = express();
app.use(express.json({ limit: '1mb' }));
// KS-800: mounted AFTER the parser — the guard reads `req.body`, so above the
// parser it inspects nothing. mcp-server carried a parser and no guard; see the
// note in demo-service/src/app.ts for why the class test did not catch it.
app.use(rejectNulBytes());

const PORT = parseInt(process.env.MCP_HTTP_PORT || '7890', 10);

// KS-1901: reads a caught value for the SERVER LOG only. Before, the two batch routes copied `err instanceof Error ? err.message : String(err)`
// into `results[i].error` (inside a 200 body). This read cannot itself throw (an Error whose `message` getter throws, or a revoked Proxy, used to
// escape the per-item catch) and it writes no field VALUE of a non-Error (Kam's ruling on KS 1346: log the kind of thing thrown and the NAMES
// of its fields, never their values). A thrown STRING is a non-Error too: it used to be logged as itself and is now logged by kind (gate 82
// G82-F1). Its result is never returned to a caller.
function describeThrown(err: unknown): string {
  try {
    if (err instanceof Error) return err.message;
    if (typeof err === 'object' && err !== null) return `non-Error object thrown (fields: ${Object.keys(err).join(', ') || 'none'})`;
    return `non-Error ${err === null ? 'null' : typeof err} thrown`;
  } catch {
    return 'unreadable thrown value';
  }
}

app.get('/health', (_req, res) => {
  res.json({ status: 'ok', service: 'secuura-mcp-http', version: '1.0.0' });
});

app.post('/hash', async (req, res) => {
  try {
    const { filePath, content } = req.body;
    let contentHash: string;
    let fileName: string;

    if (filePath) {
      contentHash = await hashFile(filePath);
      fileName = extractFileName(filePath);
    } else if (content) {
      const buffer = Buffer.from(content, 'base64');
      contentHash = hashBuffer(buffer);
      fileName = req.body.fileName || 'uploaded-document';
    } else {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Provide filePath or base64-encoded content' } });
      return;
    }

    res.json({ success: true, fileName, contentHash, algorithm: 'SHA-256' });
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : String(err);
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });
  }
});

app.post('/register', async (req, res) => {
  try {
    const { title, documentType, contentHash, description } = req.body;
    if (!title || !documentType || !contentHash) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'title, documentType, and contentHash are required' } });
      return;
    }
    const result = await registerDocument({ title, documentType, contentHash, description });
    res.status(result.status).json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] POST /register failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.post('/register-batch', async (req, res) => {
  try {
    const { documents } = req.body;
    if (!Array.isArray(documents) || documents.length === 0) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documents array is required' } });
      return;
    }

    const results: Array<Record<string, unknown>> = [];
    for (const doc of documents.slice(0, 50)) {
      try {
        let contentHash = doc.contentHash;
        if (!contentHash && doc.filePath) {
          contentHash = await hashFile(doc.filePath);
        }
        const result = await registerDocument({
          title: doc.title,
          documentType: doc.documentType,
          contentHash,
          description: doc.description,
        });
        results.push({ success: result.ok, ...result.data });
      } catch (err: unknown) {
        // KS-1901: the thrown text went to the caller as `results[i].error` under HTTP 200 (`error: message`). It is logged here and the caller gets
        // the constant the 500 handlers have answered since KS 1410; `success: false` and the title stay as they were.
        console.error('[mcp-http] POST /register-batch item failed:', describeThrown(err));
        results.push({ success: false, title: doc.title, error: 'An unexpected error occurred' });
      }
    }
    res.json({ total: results.length, results });
  } catch (err: unknown) {
    console.error('[mcp-http] POST /register-batch failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.post('/verify', async (req, res) => {
  try {
    const { documentId, contentHash, fileName, filePath, metadata } = req.body;
    let hash = contentHash;
    let name = fileName;

    if (!documentId && !hash && filePath) {
      hash = await hashFile(filePath);
      name = name || extractFileName(filePath);
    }

    if (!documentId && !hash) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Provide documentId, contentHash, or filePath' } });
      return;
    }

    const result = await verifyDocument({ documentId, contentHash: hash, fileName: name, metadata });
    res.json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] POST /verify failed:', describeThrown(err));
    res.status(500).json({ verified: false, error: 'An unexpected error occurred' });
  }
});

app.post('/verify-batch', async (req, res) => {
  try {
    const { documents } = req.body;
    if (!Array.isArray(documents) || documents.length === 0) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'documents array is required' } });
      return;
    }

    const results: Array<Record<string, unknown>> = [];
    for (const doc of documents.slice(0, 50)) {
      try {
        let hash = doc.contentHash;
        let name = doc.fileName;
        if (!doc.documentId && !hash && doc.filePath) {
          hash = await hashFile(doc.filePath);
          name = name || extractFileName(doc.filePath);
        }
        const result = await verifyDocument({
          documentId: doc.documentId,
          contentHash: hash,
          fileName: name,
        });
        results.push(result.data as Record<string, unknown>);
      } catch (err: unknown) {
        // KS-1901: the thrown text went to the caller as `results[i].error` under HTTP 200 (`error: message`). It is logged here and the caller gets
        // the constant the 500 handlers have answered since KS 1410; `verified: false` stays as it was.
        console.error('[mcp-http] POST /verify-batch item failed:', describeThrown(err));
        results.push({ verified: false, error: 'An unexpected error occurred' });
      }
    }
    res.json({ total: results.length, results });
  } catch (err: unknown) {
    console.error('[mcp-http] POST /verify-batch failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.get('/documents', async (req, res) => {
  try {
    const page = req.query.page ? parseInt(req.query.page as string, 10) : undefined;
    const limit = req.query.limit ? parseInt(req.query.limit as string, 10) : undefined;
    const status = req.query.status as string | undefined;
    const result = await listDocuments({ page, limit, status });
    res.status(result.status).json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] GET /documents failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.get('/workflow/:id', async (req, res) => {
  try {
    const result = await getWorkflowInstance(req.params.id);
    res.status(result.status).json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] GET /workflow/:id failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.get('/connector', async (_req, res) => {
  try {
    const result = await getConnectorInfo();
    res.status(result.status).json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] GET /connector failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

app.get('/policy', async (_req, res) => {
  try {
    const result = await getVerificationPolicy();
    res.json(result.data);
  } catch (err: unknown) {
    console.error('[mcp-http] GET /policy failed:', describeThrown(err));
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
  }
});

const VALID_AGENT_TYPES: AgentType[] = [
  'cursor', 'claude_desktop', 'chatgpt_actions', 'openai_assistants',
  'windsurf', 'generic_http', 'ci_cd',
];

app.post('/generate-package', async (req, res) => {
  try {
    const {
      agentType, apiKey, apiUrl, connectorName, connectorId,
      scopes, allowedDocumentTypes, workflowPolicy, rateLimit,
    } = req.body;

    if (!agentType || !VALID_AGENT_TYPES.includes(agentType)) {
      res.status(400).json({
        success: false,
        error: { code: 'BAD_REQUEST', message: `Invalid agentType. Must be one of: ${VALID_AGENT_TYPES.join(', ')}` },
      });
      return;
    }
    if (!apiKey) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'apiKey is required' } });
      return;
    }

    const slug = (connectorName || 'secuura-mcp')
      .toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');

    res.setHeader('Content-Type', 'application/zip');
    res.setHeader(
      'Content-Disposition',
      `attachment; filename="secuura-mcp-${slug}-${agentType}.zip"`,
    );

    await generatePackage(
      {
        agentType,
        apiKey,
        apiUrl: apiUrl || 'http://localhost:6882',
        connectorName: connectorName || 'Secuura MCP Connector',
        connectorId: connectorId || '',
        scopes: scopes || ['register', 'verify', 'list'],
        allowedDocumentTypes: allowedDocumentTypes || [],
        workflowPolicy: workflowPolicy || 'enforce',
        rateLimit: rateLimit || 100,
      },
      res,
    );
  } catch (err: unknown) {
    console.error('[mcp-http] POST /generate-package failed:', describeThrown(err));
    if (!res.headersSent) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } });
    }
  }
});

const server = app.listen(PORT, () => {
  process.stderr.write(`Secuura MCP HTTP server listening on port ${PORT}\n`);
});
// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;
