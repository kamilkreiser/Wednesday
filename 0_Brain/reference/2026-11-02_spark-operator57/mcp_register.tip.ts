import { z } from 'zod';
import { hashFile, extractFileName } from '../hashing.js';
import { registerDocument } from '../api-client.js';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

export function registerRegisterTools(server: McpServer) {
  server.tool(
    'secuura_register_document',
    'Register a single document on the Secuura platform. The contentHash should come from secuura_hash_document. The document metadata is sent to the API; the file itself is never uploaded. If the document type has an enforced workflow, the response will include a workflowInstanceId for tracking approval status.',
    {
      title: z.string().describe('Document title'),
      documentType: z.string().describe('Document type code (e.g. certificate, DEGREE, LICENSE)'),
      contentHash: z.string().describe('SHA-256 hash from secuura_hash_document (format: sha256:<hex>)'),
      description: z.string().optional().describe('Optional document description'),
    },
    async ({ title, documentType, contentHash, description }) => {
      try {
        const result = await registerDocument({ title, documentType, contentHash, description });

        if (!result.ok) {
          return {
            content: [
              {
                type: 'text' as const,
                text: JSON.stringify({
                  success: false,
                  httpStatus: result.status,
                  error: result.data?.error || 'Failed to register document',
                }),
              },
            ],
            isError: true,
          };
        }

        const data = result.data;
        const isPending = data.status === 'pending_approval';

        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(
                {
                  success: true,
                  documentId: data.id,
                  status: data.status,
                  contentHash: data.contentHash,
                  ...(isPending && {
                    workflowInstanceId: data.workflowInstanceId,
                    note: 'Document requires workflow approval. Use secuura_check_workflow to monitor progress.',
                  }),
                  ...(!isPending && {
                    note: 'Document registered and will be auto-anchored on the blockchain.',
                  }),
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
    'secuura_register_documents',
    'Register multiple documents in a single operation. Each document is hashed locally and then registered. Returns per-document results. If any document type has an enforced workflow, those documents will show pending_approval status.',
    {
      documents: z
        .array(
          z.object({
            filePath: z.string().describe('Path to the document file'),
            title: z.string().describe('Document title'),
            documentType: z.string().describe('Document type code'),
            description: z.string().optional().describe('Optional description'),
          }),
        )
        .min(1)
        .max(50)
        .describe('Array of documents to register (max 50)'),
    },
    async ({ documents }) => {
      const results: Array<Record<string, unknown>> = [];

      for (const doc of documents) {
        try {
          const contentHash = await hashFile(doc.filePath);
          const result = await registerDocument({
            title: doc.title,
            documentType: doc.documentType,
            contentHash,
            description: doc.description,
          });

          if (result.ok) {
            results.push({
              success: true,
              filePath: doc.filePath,
              fileName: extractFileName(doc.filePath),
              documentId: result.data.id,
              status: result.data.status,
              contentHash,
              workflowInstanceId: result.data.workflowInstanceId || null,
            });
          } else {
            results.push({
              success: false,
              filePath: doc.filePath,
              error: result.data?.error || `HTTP ${result.status}`,
            });
          }
        } catch (err: unknown) {
          const message = err instanceof Error ? err.message : String(err);
          results.push({ success: false, filePath: doc.filePath, error: message });
        }
      }

      const succeeded = results.filter((r) => r.success).length;
      const failed = results.length - succeeded;

      return {
        content: [
          {
            type: 'text' as const,
            text: JSON.stringify({ total: results.length, succeeded, failed, results }, null, 2),
          },
        ],
      };
    },
  );
}
