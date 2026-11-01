import { z } from 'zod';
import { listDocuments, getWorkflowInstance, getConnectorInfo, getVerificationPolicy, getApiUrl, hasApiKey } from '../api-client.js';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

export function registerInfoTools(server: McpServer) {
  server.tool(
    'secuura_list_documents',
    'List documents registered on the Secuura platform. Requires an API key with "list" scope.',
    {
      page: z.number().optional().describe('Page number (default 1)'),
      limit: z.number().optional().describe('Results per page (default 20, max 100)'),
      status: z
        .enum(['draft', 'pending_approval', 'signed', 'anchored', 'revoked'])
        .optional()
        .describe('Filter by document status'),
    },
    async ({ page, limit, status }) => {
      try {
        const result = await listDocuments({ page, limit, status });
        if (!result.ok) {
          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({ success: false, error: `HTTP ${result.status}`, data: result.data }),
              },
            ],
            isError: true,
          };
        }
        const docs = result.data.documents || result.data.items || [];
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(
                {
                  total: result.data.total,
                  page: result.data.page,
                  limit: result.data.limit,
                  count: docs.length,
                  documents: docs.map((d: Record<string, unknown>) => ({
                    id: d.id,
                    title: d.title,
                    documentType: d.documentType,
                    status: d.status,
                    contentHash: d.contentHash,
                    createdAt: d.createdAt,
                  })),
                },
                null,
                2,
              ),
            },
          ],
        };
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return {
          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
          isError: true,
        };
      }
    },
  );

  server.tool(
    'secuura_check_workflow',
    'Check the status of a workflow instance. Use this after registering a document that returned pending_approval status to monitor whether it has been approved or rejected.',
    {
      workflowInstanceId: z.string().describe('The workflow instance ID returned from document registration'),
    },
    async ({ workflowInstanceId }) => {
      try {
        const result = await getWorkflowInstance(workflowInstanceId);
        if (!result.ok) {
          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({
                  success: false,
                  error: result.data?.error || `HTTP ${result.status}`,
                }),
              },
            ],
            isError: true,
          };
        }
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(
                {
                  id: result.data.id,
                  status: result.data.status,
                  workflowName: result.data.workflowName,
                  steps: result.data.steps,
                },
                null,
                2,
              ),
            },
          ],
        };
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return {
          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
          isError: true,
        };
      }
    },
  );

  server.tool(
    'secuura_get_connector_info',
    'Get information about this MCP connector — its allowed scopes, document types, workflow policy, and the current verification policy. Useful for understanding what this connector is permitted to do.',
    {},
    async () => {
      try {
        const [connectorResult, policyResult] = await Promise.all([
          getConnectorInfo().catch(() => null),
          getVerificationPolicy().catch(() => null),
        ]);

        const connector = connectorResult?.ok ? connectorResult.data : null;
        // KS-1541, corrected under KS-1620 item 2: every status but 401/404 is worded "refused" (kept, per the KS-1541 brief). A 403/503 fail-closed is a deliberate refusal; a 400, 429, 500 or proxy 502 is not, and the status in the note is how a reader tells them apart.
        // KS-1767: api-client.ts now declares `error` as the union the gateway sends (a string, or an object { code, message }), so the `as unknown as` cast that worked round the old `string` type is not needed. Same read, same value at run time.
        const gatewayError = connectorResult?.data?.error;
        const refusalText = typeof gatewayError === 'string' ? gatewayError : typeof (gatewayError as { message?: unknown } | undefined)?.message === 'string' ? (gatewayError as { message: string }).message : '';
        // KS-1620: bound the relayed gateway text to 200 characters (a non-gateway upstream, such as a proxy, can send any length).
        const connectorNote = connectorResult && !connectorResult.ok && connectorResult.status !== 401 && connectorResult.status !== 404
          ? `Connector info refused by the gateway (${connectorResult.status})${refusalText ? ': ' + refusalText.slice(0, 200) : ''}`
          : 'Connector info not available (endpoint may not exist yet or no API key set)';
        const policy = policyResult?.ok ? policyResult.data : null;

        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(
                {
                  apiUrl: getApiUrl(),
                  authenticated: hasApiKey(),
                  connector: connector
                    ? {
                        id: connector.id,
                        name: connector.name,
                        scopes: connector.scopes,
                        allowedDocumentTypes: connector.allowedDocumentTypes,
                        workflowPolicy: connector.workflowPolicy,
                        rateLimit: connector.rateLimit,
                      }
                    : { note: connectorNote },
                  verificationPolicy: policy || { note: 'Policy not available' },
                },
                null,
                2,
              ),
            },
          ],
        };
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return {
          content: [{ type: 'text' as const, text: JSON.stringify({ success: false, error: message }) }],
          isError: true,
        };
      }
    },
  );
}
