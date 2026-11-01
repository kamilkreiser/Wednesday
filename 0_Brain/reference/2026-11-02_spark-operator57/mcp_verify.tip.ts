import { z } from 'zod';
import { hashFile, extractFileName } from '../hashing.js';
import { verifyDocument } from '../api-client.js';
import type { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';

function formatVerificationResult(data: Record<string, unknown>): Record<string, unknown> {
  return {
    verified: data.verified,
    documentId: data.documentId,
    matchedBy: data.matchedBy,
    strategy: data.strategy,
    ...(data.verified
      ? {
          status: data.status,
          checks: data.checks,
          blockchain: data.blockchain,
          verifiedAt: data.verifiedAt,
        }
      : {
          reason: data.reason,
          verifiedAt: data.verifiedAt,
        }),
  };
}

export function registerVerifyTools(server: McpServer) {
  server.tool(
    'secuura_verify_by_id',
    'Verify a document by its Secuura document ID. Returns verification status, checks, and blockchain proof.',
    {
      documentId: z.string().describe('The Secuura document ID (e.g. doc-1234567890-abcdef)'),
    },
    async ({ documentId }) => {
      try {
        const result = await verifyDocument({ documentId });
        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(formatVerificationResult(result.data as Record<string, unknown>), null, 2),
            },
          ],
        };
      } catch (err: unknown) {
        const message = err instanceof Error ? err.message : String(err);
        return {
          content: [{ type: 'text' as const, text: JSON.stringify({ verified: false, error: message }) }],
          isError: true,
        };
      }
    },
  );

  server.tool(
    'secuura_verify_by_file',
    'Verify a document by re-uploading the original file. The file is hashed locally (never uploaded) and the hash is compared against blockchain records using the admin-configured matching strategy.',
    {
      filePath: z.string().describe('Path to the document file to verify'),
      fileName: z
        .string()
        .optional()
        .describe('Override file name for title matching (defaults to actual filename)'),
    },
    async ({ filePath, fileName }) => {
      try {
        const contentHash = await hashFile(filePath);
        const resolvedName = fileName || extractFileName(filePath);
        const result = await verifyDocument({ contentHash, fileName: resolvedName });

        return {
          content: [
            {
              type: 'text' as const,
              text: JSON.stringify(
                {
                  ...formatVerificationResult(result.data as Record<string, unknown>),
                  localHash: contentHash,
                  fileUsed: resolvedName,
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
          content: [{ type: 'text' as const, text: JSON.stringify({ verified: false, error: message }) }],
          isError: true,
        };
      }
    },
  );

  server.tool(
    'secuura_verify_documents',
    'Verify multiple documents in a single operation. Each document can be verified by file path or document ID.',
    {
      documents: z
        .array(
          z.object({
            filePath: z.string().optional().describe('Path to file (for file-based verification)'),
            documentId: z.string().optional().describe('Document ID (for ID-based verification)'),
            fileName: z.string().optional().describe('Override file name for title matching'),
          }),
        )
        .min(1)
        .max(50)
        .describe('Array of documents to verify (max 50)'),
    },
    async ({ documents }) => {
      const results: Array<Record<string, unknown>> = [];

      for (const doc of documents) {
        try {
          if (doc.documentId) {
            const result = await verifyDocument({ documentId: doc.documentId });
            results.push({
              input: { documentId: doc.documentId },
              ...formatVerificationResult(result.data as Record<string, unknown>),
            });
          } else if (doc.filePath) {
            const contentHash = await hashFile(doc.filePath);
            const resolvedName = doc.fileName || extractFileName(doc.filePath);
            const result = await verifyDocument({ contentHash, fileName: resolvedName });
            results.push({
              input: { filePath: doc.filePath, fileName: resolvedName },
              localHash: contentHash,
              ...formatVerificationResult(result.data as Record<string, unknown>),
            });
          } else {
            results.push({
              input: doc,
              verified: false,
              error: 'Either filePath or documentId is required',
            });
          }
        } catch (err: unknown) {
          const message = err instanceof Error ? err.message : String(err);
          results.push({ input: doc, verified: false, error: message });
        }
      }

      const verified = results.filter((r) => r.verified).length;
      const failed = results.length - verified;

      return {
        content: [
          {
            type: 'text' as const,
            text: JSON.stringify({ total: results.length, verified, failed, results }, null, 2),
          },
        ],
      };
    },
  );
}
