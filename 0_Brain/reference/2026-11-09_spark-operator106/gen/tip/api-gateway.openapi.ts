/**
 * =============================================================================
 * API-GATEWAY SERVICE — OpenAPI registrations (Track 2 stage 4)
 * =============================================================================
 *
 * api-gateway proxies most /api/* requests to backend services (auth,
 * originate, anchoring, ...) — those endpoints are documented in their
 * respective <svc>.openapi.ts files. This file documents api-gateway's
 * OWN endpoints (the ones not proxied to a downstream service):
 *
 *   - /api/batch/* — bulk certify/verify/delegate
 *   - /api/notifications/* — user notification CRUD
 *   - /api/system/health/dashboard — aggregated health view
 *   - /api/admin/audit/export — audit log export
 *   - /api/document-types — public document-types list
 *   - /api/platform/document-lookup — public tenant lookup by content hash or document id (KS-1773)
 *
 * Endpoints not yet registered (deferred to follow-up commits):
 *   - admin.ts: large admin CRUD surface (document-types/workflows/
 *     integrations/verification-policies/etc.) — deserves its own
 *     `services/api-gateway/src/admin.openapi.ts` file
 *   - platform.ts: multi-tenancy provisioning + tenant management
 *   - proxy.ts / verification.ts / versioning.ts: thin pass-through
 *     handlers (covered by the upstream service's openapi.ts)
 *   - system-status.ts: operational dashboard, not public API surface
 *   - extension/desktop downloads: binary delivery, not typical API
 *   - rate-limit-only mounts (e.g. app.use('/api/auth/login', rateLimit))
 *     don't add new endpoints, just middleware
 * =============================================================================
 */

import { z, sharedRegistry, commonErrorResponses, FX } from '@secuura/shared';

// -----------------------------------------------------------------------------
// SHARED SCHEMAS
// -----------------------------------------------------------------------------

const BatchCertifyRequestSchema = sharedRegistry.register(
  'BatchCertifyRequest',
  z
    .object({
      documentIds: z.array(z.string()).min(1),
      reason: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    // KS-665 item 1 (same class as the singular `documentId`): the synthesiser
    // published its own placeholder (`example-documentIds[]`), which names no
    // document anywhere. One element, because repeating a single fixture id is
    // a duplicate rather than a batch.
    //
    // Custody rebase (KS-256 delta pass, F-1 + F-2): the original wording here
    // claimed the placeholder is "rejected by the documentId regex". There is
    // no regex — all three batch bodies are `z.array(z.string()).min(1)`. And
    // the 400 a caller actually gets from these endpoints comes from the
    // top-level KEY NAME, not from the id value: the runtime reads
    // `documents[]` / `hashes[]` / `delegations[]` (routes/batch.ts:21-45),
    // so this change does not remove it. That spec-vs-runtime divergence is
    // byte-identical on develop — it is not #568's defect and is filed apart.
    documentIds: [FX.document.id],
  },
  }),
);

const BatchVerifyRequestSchema = sharedRegistry.register(
  'BatchVerifyRequest',
  z
    .object({
      hashes: z.array(z.string().regex(/^[a-f0-9]{64}$/)).min(1).optional(),
      documentIds: z.array(z.string()).min(1).optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    hashes: [
      'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789',
      'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789',
    ],
    // KS-665 item 1 (same class as the singular `documentId`): the synthesiser
    // published its own placeholder (`example-documentIds[]`), which names no
    // document anywhere. One element, because repeating a single fixture id is
    // a duplicate rather than a batch.
    documentIds: [FX.document.id],
  },
  }),
);

const BatchDelegationsRequestSchema = sharedRegistry.register(
  'BatchDelegationsRequest',
  z
    .object({
      documentIds: z.array(z.string()).min(1),
      delegateUserId: z.string(),
      role: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    // KS-665 item 1 (same class as the singular `documentId`): the synthesiser
    // published its own placeholder (`example-documentIds[]`), which names no
    // document anywhere. One element, because repeating a single fixture id is
    // a duplicate rather than a batch.
    documentIds: [FX.document.id],
    delegateUserId: 'example-delegateUserId',
  },
  }),
);

const BatchResultEnvelopeSchema = sharedRegistry.register(
  'BatchResultEnvelope',
  z.object({
    success: z.boolean(),
    processed: z.number().int().nonnegative(),
    failed: z.number().int().nonnegative(),
    results: z.array(z.record(z.string(), z.unknown())).optional(),
    errors: z.array(z.record(z.string(), z.unknown())).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    processed: 0,
    failed: 0,
  },
  }),
);

const NotificationItemSchema = sharedRegistry.register(
  'NotificationItem',
  z
    .object({
      id: z.string(),
      userId: z.string().optional(),
      type: z.string(),
      title: z.string().optional(),
      message: z.string().optional(),
      read: z.boolean(),
      createdAt: z.string(),
      data: z.record(z.string(), z.unknown()).optional().nullable(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    type: 'example-type',
    read: true,
    createdAt: 'example-createdAt',
  },
  }),
);

// KS-423: the live route answers with the platform `{success, data}` envelope
// (routes/notifications.ts), not a bare `notifications` array — modelled to
// match the real response so response_schema_conformance holds.
const NotificationListResponseSchema = sharedRegistry.register(
  'NotificationListResponse',
  z.object({
    success: z.boolean(),
    data: z.array(NotificationItemSchema),
    pagination: z
      .object({
        total: z.number().int().nonnegative(),
        limit: z.number().int().nonnegative(),
        offset: z.number().int().nonnegative(),
      })
      .optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: [
      {
        id: 'example-id',
        type: 'example-type',
        read: true,
        createdAt: 'example-createdAt',
      },
      {
        id: 'example-id',
        type: 'example-type',
        read: true,
        createdAt: 'example-createdAt',
      },
    ],
  },
  }),
);

// KS-423: real shape is `{success, data: {unreadCount}}` (routes/notifications.ts).
const UnreadCountResponseSchema = sharedRegistry.register(
  'UnreadCountResponse',
  z.object({
    success: z.boolean(),
    data: z.object({
      unreadCount: z.number().int().nonnegative(),
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      unreadCount: 0,
    },
  },
  }),
);

const NotificationCreateRequestSchema = sharedRegistry.register(
  'NotificationCreateRequest',
  z
    .object({
      // KS-444: the handler's guard is a truthiness check, so an EMPTY string in
      // any of the four core fields also 400s ("Missing required fields: …") —
      // publish that genuine non-empty requirement as min(1); empty strings were
      // spec-legal but rejected (positive_data_acceptance).
      userId: z.string().min(1),
      // KS-455 (Kam decision 2026-07-16): publish the runtime's six-value type
      // enum. The runtime has always rejected anything else ("Invalid
      // notification type…"), the frontends key icons/filters off these values,
      // and there are no external consumers yet — the open string was the drift.
      type: z.enum(['purchase', 'certification', 'verification', 'transfer', 'security', 'system']),
      // KS-430: the runtime handler (routes/notifications.ts POST /) rejects a
      // request missing title or message with a 400 ("Missing required fields:
      // userId, type, title, message"). Both are the core notification payload —
      // a notification cannot exist without them — so mark them required here to
      // match the runtime; a spec-minimal {userId,type} body no longer 400s.
      title: z.string().min(1),
      message: z.string().min(1),
      data: z.record(z.string(), z.unknown()).optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    userId: FX.issuer.id,
    type: 'purchase',
    title: 'example-title',
    message: 'example-message',
  },
  }),
);

// KS-144: real response has `services` as an object map keyed by service name
// (`{ originate: { status, latencyMs, url }, ... }`), not an array; `status` may
// carry values beyond the three-way enum. Modelled to match the live response.
const HealthDashboardResponseSchema = sharedRegistry.register(
  'HealthDashboardResponse',
  z
    .object({
      status: z.string(),
      services: z.record(
        z.string(),
        z
          .object({
            status: z.string(),
            latencyMs: z.number().nullable().optional(),
            url: z.string().optional(),
          })
          .passthrough(),
      ),
      timestamp: z.string(),
    })
    .passthrough()
    .openapi({
               // KS-256: generated example (synthesised, masked). Guarded by
               // `npm run check:openapi` -> check-spec-examples (E1-E7).
               example: {
                 status: 'example-status',
                 services: {},
                 timestamp: FX.timestamps.createdAt,
               },
      description:
        'Aggregated health across all backend services with latency tracking. ' +
        'Parallel checks keep response fast.',
    }),
);

const DocumentTypeSchema = sharedRegistry.register(
  'DocumentType',
  z
    .object({
      id: z.string(),
      name: z.string(),
      description: z.string().optional().nullable(),
      schema: z.record(z.string(), z.unknown()).optional().nullable(),
      isActive: z.boolean().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    name: 'example-name',
  },
  }),
);

// KS-118: GET /api/document-types returns a bare array (res.json(active) in
// routes/verification.ts) — the frontends consume it as such, so the spec is
// aligned to the actual shape rather than the handler being re-wrapped.
const DocumentTypesListResponseSchema = sharedRegistry.register(
  'DocumentTypesListResponse',
  z.array(DocumentTypeSchema).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: [
    {
      id: 'example-id',
      name: 'example-name',
    },
    {
      id: 'example-id',
      name: 'example-name',
    },
  ],
  }),
);

const GatewaySuccessSchema = sharedRegistry.register(
  'GatewaySuccess',
  z
    .object({
      success: z.boolean(),
      message: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
  },
  }),
);

// -----------------------------------------------------------------------------
// ROUTES — /api/batch
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/batch/certifications',
  tags: ['Batch'],
  summary: 'Bulk certify a list of documents',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      // KS-1364: the published contract declares this request body required.
      required: true,
      content: {
        'application/json': { schema: BatchCertifyRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Batch results with per-item status',
      content: { 'application/json': { schema: BatchResultEnvelopeSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/batch/verify',
  tags: ['Batch', 'Verification'],
  summary: 'Bulk verify a list of document hashes or ids',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': { schema: BatchVerifyRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Batch verification results',
      content: { 'application/json': { schema: BatchResultEnvelopeSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Validation error (provide hashes OR documentIds)' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/batch/delegations',
  tags: ['Batch'],
  summary: 'Bulk delegate documents to another user',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      // KS-1364: the published contract declares this request body required.
      required: true,
      content: {
        'application/json': { schema: BatchDelegationsRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Batch delegation results',
      content: { 'application/json': { schema: BatchResultEnvelopeSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/notifications
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/notifications',
  tags: ['Notifications'],
  summary: 'List notifications for the authenticated user',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Notifications list',
      content: { 'application/json': { schema: NotificationListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/notifications/unread/count',
  tags: ['Notifications'],
  summary: 'Unread notification count for the authenticated user',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Unread count',
      content: { 'application/json': { schema: UnreadCountResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/notifications/{id}/read',
  tags: ['Notifications'],
  summary: 'Mark a single notification as read',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Marked as read',
      content: { 'application/json': { schema: GatewaySuccessSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'Notification not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/notifications/read-all',
  tags: ['Notifications'],
  summary: 'Mark all notifications as read for the authenticated user',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Marked all as read',
      content: { 'application/json': { schema: GatewaySuccessSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

sharedRegistry.registerPath({
  method: 'delete',
  path: '/api/notifications/{id}',
  tags: ['Notifications'],
  summary: 'Delete a notification',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Notification deleted',
      content: { 'application/json': { schema: GatewaySuccessSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'Notification not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

// KS-1448: the summary said "internal", naming service-to-service use, and the description said backend services push here,
// naming originate and anchoring. Both were false. Read at develop: 0 callers in frontend, mobile, packages or services;
// originate's client posts to a separate notification service; transfer keeps its own local function.
sharedRegistry.registerPath({
  method: 'post',
  path: '/api/notifications',
  tags: ['Notifications'],
  summary: 'Create a notification for the authenticated caller',
  description:
    'Creates a notification in the list of the caller. `userId` must be the id of the caller; any other value answers 403 ' +
    'for every principal, administrators and connector keys included.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      // KS-498: required — the runtime 400s a bodyless request (userId/type/
      // title/message are mandatory), so an absent body is not a valid
      // positive case (the KS-283/KS-444 pattern).
      required: true,
      content: {
        'application/json': { schema: NotificationCreateRequestSchema },
      },
    },
  },
  responses: {
    201: {
      description: 'Notification created',
      // KS-498: the handler wraps the created notification in the platform
      // `{ success, data }` envelope like the list/count routes above.
      content: {
        'application/json': {
          schema: z.object({ success: z.literal(true), data: NotificationItemSchema }),
        },
      },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/system/health
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/system/health/dashboard',
  security: [],
  tags: ['Health'],
  summary: 'Aggregated dashboard of service health + latency',
  description:
    'Parallel health checks against every backend service. Authentication is ' +
    'configurable per env (open in dev, gated behind admin in demo).',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Aggregated health snapshot',
      content: { 'application/json': { schema: HealthDashboardResponseSchema } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    401: commonErrorResponses[401],
    404: commonErrorResponses[404],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/admin/audit
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/admin/audit/export',
  tags: ['Admin', 'Audit'],
  summary: 'Export audit logs as CSV or JSON',
  // KS-1645 item 4: the description and parameters now match the route (audit-export.ts). Before: `from` and `to` were optional date-times, but the route requires
  // both and reads plain YYYY-MM-DD UTC dates (it answers 400 "Use YYYY-MM-DD"); the 200 JSON body was declared as { entries }, but the route answers
  // { success, meta, data }. KS-1645 item 3: no `type` parameter is declared because the route no longer reads one.
  description:
    'Admin-only audit log export. The query string controls format (csv|json) ' +
    'and the date range: both `from` and `to` are required, plain YYYY-MM-DD UTC dates, and `to` includes the whole of its UTC day. ' +
    'Output is a single file download. At most the newest 10,000 platform audit rows are visible to this export, ' +
    'and a file holds at most 10,000 rows: in the JSON body `meta.total` is the row count the audit service reports for the range and ' +
    '`meta.truncated` is true when the file holds fewer rows than that. A CSV has no meta, so a truncated CSV carries the response header X-Audit-Export-Truncated: true.',
  security: [{ bearerAuth: [] }],
  request: {
    query: z.object({
      format: z.enum(['csv', 'json']).optional(),
      from: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).openapi({ description: 'First day of the range, a plain YYYY-MM-DD UTC date (required).' }),
      to: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).openapi({ description: 'Last day of the range, a plain YYYY-MM-DD UTC date (required); the whole of that UTC day is included.' }),
    }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Audit log export (file download)',
      // KS-1645 item 1: a CSV has no meta, so a truncated export says so in this header (present only when true).
      headers: {
        'X-Audit-Export-Truncated': {
          description: 'Present, with the value true, only on a CSV export whose file holds fewer rows than the audit service reported for the range.',
          schema: { type: 'string', enum: ['true'] },
        },
      },
      content: {
        'text/csv': { schema: z.string().openapi({ description: 'CSV bytes: a header row, then one row per audit entry (id, timestamp, action, userId, ipAddress, userAgent, resource, resourceId, details as JSON, outcome)' }) },
        'application/json': {
          // KS-1645 item 4: was { entries: [...] }, a key the route never sent. The route answers { success, meta, data }.
          schema: z.object({
            success: z.boolean(),
            meta: z.object({
              from: z.string(),
              to: z.string(),
              totalEntries: z.number().int().openapi({ description: 'Rows in this file.' }),
              total: z.number().int().openapi({ description: 'Rows the audit service reports for the range (at most the newest 10,000 platform audit rows are visible to this export).' }),
              truncated: z.boolean().openapi({ description: 'True when this file holds fewer rows than total.' }),
              exportedAt: z.string(),
            }),
            data: z.array(z.record(z.string(), z.unknown())),
          }),
        },
      },
    },
    401: commonErrorResponses[401],
    403: { ...commonErrorResponses[403], description: 'Admin role required' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/document-types
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/document-types',
  tags: ['Documents'],
  summary: 'List available document types (public reference data)',
  description:
    'Returns the catalog of document types the platform supports. Used by ' +
    'the issuer portal to populate the document-creation type dropdown.',
  security: [], // KS-144: intended-public endpoint (no auth required)
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Document types list',
      content: {
        'application/json': { schema: DocumentTypesListResponseSchema },
      },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/settings + /api/privacy  (KS-719)
// -----------------------------------------------------------------------------
//
// These four operations live in routes/admin.ts and were absent from the spec
// entirely, so neither Schemathesis nor Akto had ever tested them (KS-712).
// They were deliberately held out of PR #760 because their auth contract was
// undecided: both PUTs accepted UNAUTHENTICATED writes into a shared 'default'
// bucket, and documenting that as-is would have blessed the defect rather than
// ruling on it.
//
// Kam ruled the contract on 2026-08-29: the PUTs require authentication; the
// GETs keep optional auth so an anonymous caller still receives the documented
// defaults. The registrations below describe the POST-FIX behaviour.
//
// The GETs carry `security: []` because no credential is REQUIRED to call them
// successfully — which is what a scanner needs to know. A bearer, when present,
// scopes the read to that caller's own settings instead of the shared defaults.
// There is no precedent in this repo for OpenAPI's optional-auth form
// (`security: [{}, { bearerAuth: [] }]`), so this does not introduce one.

const PrivacySettingsSchema = sharedRegistry.register(
  'PrivacySettings',
  z
    .object({
      autoRejectUnknown: z.boolean().optional(),
      preferRangeProofs: z.boolean().optional(),
      preferCommitments: z.boolean().optional(),
      logAllDisclosures: z.boolean().optional(),
      notifyOnDisclosure: z.boolean().optional(),
    })
    .passthrough(),
);

const PrivacySettingsResponseSchema = sharedRegistry.register(
  'PrivacySettingsResponse',
  z
    .object({
      success: z.boolean(),
      settings: PrivacySettingsSchema,
    })
    .passthrough(),
);

const PrivacySettingsUpdateResponseSchema = sharedRegistry.register(
  'PrivacySettingsUpdateResponse',
  z
    .object({
      success: z.boolean(),
      settings: PrivacySettingsSchema,
      updatedAt: z.string(),
    })
    .passthrough(),
);

// The notification handlers spread the stored object into the response body
// (`res.json({ success: true, ...data })`) rather than nesting it under a key,
// so the response is modelled flat to match the live shape.
const NotificationSettingsResponseSchema = sharedRegistry.register(
  'NotificationSettingsResponse',
  z
    .object({
      success: z.boolean(),
      certificationNotifications: z.boolean().optional(),
      verificationNotifications: z.boolean().optional(),
    })
    .passthrough(),
);

const NotificationSettingsUpdateRequestSchema = sharedRegistry.register(
  'NotificationSettingsUpdateRequest',
  z
    .object({
      certificationNotifications: z.boolean().optional(),
      verificationNotifications: z.boolean().optional(),
    })
    .passthrough(),
);

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/privacy/settings',
  tags: ['Settings'],
  summary: 'Read privacy settings',
  description:
    'Returns the caller’s privacy settings. Optional auth: an anonymous caller ' +
    'receives the documented platform defaults; a bearer scopes the read to ' +
    'that user’s own stored settings.',
  security: [], // KS-719: optional auth — no credential is required to succeed
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Privacy settings (per-user when authenticated, defaults otherwise)',
      content: { 'application/json': { schema: PrivacySettingsResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

sharedRegistry.registerPath({
  method: 'put',
  path: '/api/privacy/settings',
  tags: ['Settings'],
  summary: 'Update the authenticated user’s privacy settings',
  description:
    'Requires authentication (KS-719). Writes are scoped to the calling user; ' +
    'there is no shared anonymous settings bucket.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: { 'application/json': { schema: PrivacySettingsSchema } },
    },
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Privacy settings updated',
      content: { 'application/json': { schema: PrivacySettingsUpdateResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/settings/notifications',
  tags: ['Settings'],
  summary: 'Read notification settings',
  description:
    'Returns the caller’s notification settings. Optional auth: an anonymous ' +
    'caller receives the documented platform defaults; a bearer scopes the ' +
    'read to that user’s own stored settings.',
  security: [], // KS-719: optional auth — no credential is required to succeed
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Notification settings (per-user when authenticated, defaults otherwise)',
      content: { 'application/json': { schema: NotificationSettingsResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

sharedRegistry.registerPath({
  method: 'put',
  path: '/api/settings/notifications',
  tags: ['Settings'],
  summary: 'Update the authenticated user’s notification settings',
  description:
    'Requires authentication (KS-719). Writes are scoped to the calling user; ' +
    'there is no shared anonymous settings bucket.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: { 'application/json': { schema: NotificationSettingsUpdateRequestSchema } },
    },
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Notification settings updated',
      content: { 'application/json': { schema: NotificationSettingsResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/connector/info
// -----------------------------------------------------------------------------
//
// KS-1531: this route (services/api-gateway/src/services/health.ts:42) has never
// been in the published contract. The schema below is derived from what the
// handler returns at health.ts:103-110.
//
// Two fields are declared `string` but are NOT validated by the handler: `name`
// and `workflowPolicy` are read from the stored connector config, which is typed
// `Record<string, unknown>`. A non-string stored there would be echoed as-is.
// Everything else is guaranteed by the handler: `id`, `scopes` and `rateLimit`
// come from the typed ConnectorMeta (middleware/auth.ts:61-69), and
// `allowedDocumentTypes` is refused with 403 unless it is absent, null or a list of
// strings (KS-1534: a list that holds a non-string is refused too, so the declared
// `z.array(z.string())` below is now what the handler guarantees).

const ConnectorInfoSchema = sharedRegistry.register(
  'ConnectorInfo',
  z
    .object({
      id: z.string(),
      name: z.string(),
      scopes: z.array(z.string()),
      allowedDocumentTypes: z.array(z.string()).openapi({
        description:
          'The document types this connector may act on. Empty means no restriction — ' +
          'every type is permitted.',
      }),
      workflowPolicy: z.string().openapi({
        description: 'The connector’s workflow policy. Defaults to `enforce` when none is stored.',
      }),
      rateLimit: z.number(),
    })
    .passthrough(),
);

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/connector/info',
  tags: ['Connectors'],
  summary: 'The calling connector’s own identity, scopes and limits',
  // KS-1757: this said "a user or admin bearer token is refused with 403". authenticateToken(true) runs first and answers
  // 401 for a bearer it rejects (invalid or expired: middleware/auth.ts:530; session revoked: :495), so only a valid
  // bearer with an active session reaches the handler's 403 (services/health.ts:44-46). The 401 response below (KS-1753)
  // carries the detail; this sentence points at it.
  description:
    'Returns the connector identified by the `x-api-key` credential on the request: ' +
    'its id, display name, granted scopes, document-type allow-list, workflow policy ' +
    'and rate limit. Available only to API-key authenticated connectors — a valid user or ' +
    'admin bearer token with an active session is refused with 403; one that authentication ' +
    'itself rejects is answered 401 first (see the 401 response). A stored allow-list that ' +
    'cannot be read, or that is present but is not a list of strings, is refused rather than treated as ' +
    '“no restriction”.',
  security: [{ connectorApiKey: [] }],
  responses: {
    200: {
      description: 'The calling connector’s own record',
      content: { 'application/json': { schema: ConnectorInfoSchema } },
    },
    401: {
      ...commonErrorResponses[401],
      description:
        'No usable connector credential on the request: the `x-api-key` header is missing, ' +
        'or the key it carries is not a valid connector key. A connector JWT presented as a ' +
        'Bearer credential is also answered 401, telling the caller to present its API key ' +
        'instead. A user or admin bearer token is also answered 401 when authentication ' +
        'itself rejects it — the token is invalid or expired, or its session has been ' +
        'revoked; a valid user or admin bearer with an active session gets past ' +
        'authentication and is refused 403 instead.',
    },
    403: {
      ...commonErrorResponses[403],
      description:
        'The caller is not an API-key authenticated connector; or the stored connector ' +
        'allow-list is malformed — a container that is not a list, an entry that is not an ' +
        'object, a second entry for this connector, or a document-type allow-list that is ' +
        'present but is not a list of strings — and is refused rather than read as unrestricted.',
    },
    503: {
      ...commonErrorResponses[503],
      description:
        'The connector allow-list configuration is currently unreadable. The request is ' +
        'refused rather than answered with an empty allow-list.',
    },
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/platform/document-lookup
// -----------------------------------------------------------------------------
//
// KS-1773: this route (services/api-gateway/src/routes/platform.ts:1106) was live and absent from
// the published contract, so the contract said nothing about an anonymous caller, who gets a 400
// when no parameter is sent and not a 401. Kam ruled on 2026-10-28 (07:14 AEDT): "a — Keep it
// public and publish it". It is public on purpose: the handler carries no authentication and its
// own comment (platform.ts:1096-1104) names the verifier portal as the caller. The operation
// declares `security: []`, as /api/document-types does (KS-144).
//
// Every answer below is read from the handler; none is invented:
//   400  neither `hash` nor `documentId` (an empty value counts as absent)     platform.ts:1110-1111
//   503  PLATFORM_DATABASE_URL is unset                                         platform.ts:1114-1116
//   200  { success: true, results: [...] }, at most 5 rows, seven fields        platform.ts:1125-1148
//   500  any other failure, a constant body                                     platform.ts:1152-1170
// There is NO 404: a lookup that matches nothing is a 200 with `results: []` (platform.ts:1137-1148).
// `hash` is tested first, so when both parameters are sent `documentId` is ignored (platform.ts:1125-1134).
// 429 is the gateway's global per-minute limiter (index.ts:479). This path is not in its exempt list
// (middleware/rateLimitSkip.ts:23), so it applies here as it does to every other /api route.
//
// Column types are read from the init DDL (docker/init-platform/01-platform-schema.sql:209-221):
// tenant_slug, document_type, title, status and certified_at are nullable there. The live database
// was not queried.
//
// Publishing is not inert. The gateway reads this spec at boot (index.ts:612) and answers 405 with
// `Allow: GET` to any method the spec does not declare on a documented path (index.ts:1064-1081).
// After a deploy and a gateway restart every non-GET method on this path, HEAD included, is a 405 with
// `Allow: GET` (the method set holds only declared methods, specRouteMap.ts:39-44, so declaring GET does
// not admit HEAD). Methods such as POST and DELETE were the fall-through 404; HEAD was answered by the
// GET handler, so it changes too. KS-1773 gate D M1, 2026-10-28, wording only: this sentence said "a
// non-GET ... where it was the fall-through 404", which is wrong for HEAD.
// No `bearerAuth` is declared, so the edge auth gate stays unarmed for this route (specRouteMap.ts:47).

const DocumentLookupResultSchema = sharedRegistry.register(
  'DocumentLookupResult',
  z.object({
    documentId: z.string(),
    tenantId: z.string().openapi({ description: 'The owning tenant’s id (a UUID in the registry table).' }),
    tenantSlug: z.string().nullable(),
    documentType: z.string().nullable(),
    title: z.string().nullable(),
    status: z.string().nullable().openapi({ description: 'The registry status; the column defaults to `active`.' }),
    certifiedAt: z.string().datetime().nullable().openapi({ description: 'When the document was certified (ISO 8601, UTC); null when none is recorded.' }),
  }),
);

const DocumentLookupResponseSchema = sharedRegistry.register(
  'DocumentLookupResponse',
  z.object({
    success: z.literal(true),
    results: z.array(DocumentLookupResultSchema).max(5).openapi({
      description:
        'The registry rows that match, at most five. An empty list means nothing matched: that is a ' +
        '200 with no results, not a 404.',
    }),
  }),
);

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/platform/document-lookup',
  tags: ['Documents'],
  summary: 'Look up which tenant owns a document, by content hash or document id (public)',
  description:
    'Public by design: no credential is required or checked. The verifier portal calls it to find the ' +
    'tenant that owns a document before it verifies. Send `hash` (the document’s content hash) or ' +
    '`documentId`; at least one is required, and an empty value counts as absent. When both are sent, ' +
    '`hash` is used and `documentId` is ignored. Returns up to five registry rows, each with the owning ' +
    'tenant and the document’s type, title, status and certification time. A lookup that matches nothing ' +
    'answers 200 with an empty `results` list, not 404.',
  security: [], // KS-1773: intended-public endpoint (Kam, 2026-10-28), as KS-144 did for /api/document-types
  request: {
    query: z.object({
      hash: z.string().optional().openapi({ description: 'The document’s content hash. Takes precedence over `documentId` when both are sent.' }),
      documentId: z.string().optional().openapi({ description: 'The document id. Used only when `hash` is absent or empty.' }),
    }),
  },
  responses: {
    200: {
      description: 'The matching registry rows (possibly none)',
      content: { 'application/json': { schema: DocumentLookupResponseSchema } },
    },
    400: {
      ...commonErrorResponses[400],
      description: 'Neither `hash` nor `documentId` was sent, or both were empty. `error.code` is `BAD_REQUEST`.',
    },
    429: {
      ...commonErrorResponses[429],
      description:
        'The gateway’s global per-minute rate limit was exceeded. This comes from the gateway, not from the ' +
        'handler; the path is not exempt from it.',
    },
    500: {
      ...commonErrorResponses[500],
      description:
        'The lookup failed for any other reason, for example the platform database could not be reached or ' +
        'the query was refused. The body is a constant (`error.code` `INTERNAL_ERROR`, message ' +
        '`Document lookup failed`); the cause is logged, not returned.',
    },
    503: {
      ...commonErrorResponses[503],
      description:
        'The platform database is not configured on this deployment (`PLATFORM_DATABASE_URL` is unset). ' +
        '`error.code` is `SERVICE_UNAVAILABLE`.',
    },
  },
});
