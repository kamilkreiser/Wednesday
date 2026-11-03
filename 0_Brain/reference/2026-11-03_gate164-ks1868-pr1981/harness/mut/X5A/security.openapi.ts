/**
 * =============================================================================
 * SECURITY SERVICE — OpenAPI registrations
 * =============================================================================
 *
 * Compliance + ops core: audit logs, security events, rate limits,
 * API key issuance + validation. Service-to-service mostly: every other
 * service writes audit entries here. (KS-952: this header used to say the
 * gateway also calls /rate-limit/check. It does not — see that operation.)
 * before forwarding sensitive endpoints; admin reads /events for the
 * SOC dashboard.
 *
 * Endpoints registered (12 paths covering all service routes). All
 * service-internal handlers live at /api/audit, /api/events, /api/keys,
 * /api/rate-limit; the api-gateway proxies /api/security/* and rewrites
 * the prefix, so the public-facing paths below carry the /api/security/
 * prefix:
 *   Audit log:
 *     - POST  /api/security/audit
 *     - GET   /api/security/audit
 *     - GET   /api/security/audit/{id}
 *   Security events:
 *     - POST  /api/security/events
 *     - GET   /api/security/events
 *     - PATCH /api/security/events/{id}/resolve
 *   API keys:
 *     - POST   /api/security/keys
 *     - GET    /api/security/keys
 *     - DELETE /api/security/keys/{id}
 *     - POST   /api/security/keys/validate
 *   Rate limits:
 *     - POST /api/security/rate-limit/check
 *     - POST /api/security/rate-limit/reset
 * =============================================================================
 */

import { z, sharedRegistry, commonErrorResponses, successEnvelope, FX } from '@secuura/shared';
import { MAX_RATE_LIMIT_WINDOW_MS } from './rateLimitBounds';
// KS-952: same rule as the line above — the published bound is IMPORTED from the
// module the runtime enforces, never restated, so the two cannot drift.
import { RATE_LIMIT_KEY_MAX } from './rateLimitScope';

// -----------------------------------------------------------------------------
// SCHEMAS
// -----------------------------------------------------------------------------

const SeveritySchema = z.enum(['low', 'medium', 'high', 'critical']);

const AuditLogCreateRequestSchema = sharedRegistry.register(
  'AuditLogCreateRequest',
  z.object({
    userId: z.string().optional(),
    organizationId: z.string().optional(),
    action: z.string().min(1),
    resourceType: z.string().min(1),
    resourceId: z.string().optional(),
    ipAddress: z.string().optional(),
    userAgent: z.string().optional(),
    details: z.record(z.string(), z.unknown()).optional(),
    previousState: z.record(z.string(), z.unknown()).optional(),
    newState: z.record(z.string(), z.unknown()).optional(),
    success: z.boolean().optional(),
    errorMessage: z.string().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    action: 'example-action',
    resourceType: 'example-resourceType',
  },
  }),
);

const AuditLogEntrySchema = sharedRegistry.register(
  'AuditLogEntry',
  z
    .object({
      id: z.string(),
      userId: z.string().nullable().optional(),
      organizationId: z.string().nullable().optional(),
      action: z.string(),
      resourceType: z.string(),
      resourceId: z.string().nullable().optional(),
      ipAddress: z.string().nullable().optional(),
      userAgent: z.string().nullable().optional(),
      details: z.record(z.string(), z.unknown()).nullable().optional(),
      success: z.boolean(),
      errorMessage: z.string().nullable().optional(),
      createdAt: z.string(),
    })
    .passthrough()
    .openapi({
               // KS-256: generated example (synthesised, masked). Guarded by
               // `npm run check:openapi` -> check-spec-examples (E1-E7).
               example: {
                 id: 'example-id',
                 action: 'example-action',
                 resourceType: 'example-resourceType',
                 success: true,
                 createdAt: 'example-createdAt',
               },
      description:
        'A platform audit log entry. PII-bearing fields in `details` are ' +
        'PII-encrypted at rest (audit 1.3 phase 5).',
    }),
);

// KS-144: real response is flat `{ success, logs: [...], total }` (no `data`
// wrapper; key is `logs`, not `entries`).
const AuditLogListResponseSchema = sharedRegistry.register(
  'AuditLogListResponse',
  z
    .object({
      success: z.literal(true),
      logs: z.array(AuditLogEntrySchema),
      total: z.number().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    logs: [
      {
        id: 'example-id',
        action: 'example-action',
        resourceType: 'example-resourceType',
        success: true,
        createdAt: FX.timestamps.createdAt,
      },
      {
        id: 'example-id',
        action: 'example-action',
        resourceType: 'example-resourceType',
        success: true,
        createdAt: FX.timestamps.createdAt,
      },
    ],
  },
  }),
);

// KS-440 (response-side): POST /api/audit returns the canonical envelope
// `{ success, data: { id } }` (index.ts POST '/api/audit') — it echoes ONLY the
// new entry's id, not the full audit record. The old AuditLogEntrySchema (flat,
// requiring action/resourceType/success/createdAt) made every real 201 violate
// the response schema. Publish the real envelope. (AuditLogEntrySchema stays the
// shape for the GET list/detail reads, which return the full record.)
const AuditLogCreateResponseSchema = sharedRegistry.register(
  'AuditLogCreateResponse',
  successEnvelope(z.object({ id: z.string() }).passthrough()).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: 'example-id',
    },
  },
  }),
);

const SecurityEventCreateRequestSchema = sharedRegistry.register(
  'SecurityEventCreateRequest',
  z.object({
    eventType: z.string().min(1),
    severity: SeveritySchema,
    source: z.string().min(1),
    userId: z.string().optional(),
    ipAddress: z.string().optional(),
    details: z.record(z.string(), z.unknown()).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    eventType: 'example-eventType',
    severity: 'low',
    source: 'example-source',
  },
  }),
);

const SecurityEventSchema = sharedRegistry.register(
  'SecurityEvent',
  z
    .object({
      id: z.string(),
      eventType: z.string(),
      severity: SeveritySchema,
      source: z.string(),
      userId: z.string().nullable().optional(),
      ipAddress: z.string().nullable().optional(),
      details: z.record(z.string(), z.unknown()).nullable().optional(),
      resolved: z.boolean(),
      resolvedAt: z.string().nullable().optional(),
      resolvedBy: z.string().nullable().optional(),
      createdAt: z.string(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    eventType: 'example-eventType',
    severity: 'low',
    source: 'example-source',
    resolved: true,
    createdAt: 'example-createdAt',
  },
  }),
);

// KS-440 (response-side): POST /api/events returns the canonical envelope
// `{ success, data: <event> }` (index.ts POST '/api/events') — the old flat
// SecurityEventSchema made every real 201 violate the response schema ("id is a
// required property", because the event is nested under `data`). Publish the
// envelope wrapping the event.
const SecurityEventCreateResponseSchema = sharedRegistry.register(
  'SecurityEventCreateResponse',
  successEnvelope(SecurityEventSchema).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: 'example-id',
      eventType: 'example-eventType',
      severity: 'low',
      source: 'example-source',
      resolved: true,
      createdAt: FX.timestamps.createdAt,
    },
  },
  }),
);

// KS-144: real response is enveloped `{ success, data: { events, total, limit, offset } }`.
const SecurityEventListResponseSchema = sharedRegistry.register(
  'SecurityEventListResponse',
  successEnvelope(
    z
      .object({
        events: z.array(SecurityEventSchema),
        total: z.number().optional(),
        limit: z.number().optional(),
        offset: z.number().optional(),
      })
      .passthrough(),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      events: [
        {
          id: 'example-id',
          eventType: 'example-eventType',
          severity: 'low',
          source: 'example-source',
          resolved: true,
          createdAt: FX.timestamps.createdAt,
        },
        {
          id: 'example-id',
          eventType: 'example-eventType',
          severity: 'low',
          source: 'example-source',
          resolved: true,
          createdAt: FX.timestamps.createdAt,
        },
      ],
    },
  },
  }),
);

const SecurityEventResolveRequestSchema = sharedRegistry.register(
  'SecurityEventResolveRequest',
  z
    .object({
      resolvedBy: z.string().optional(),
      resolutionNotes: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    resolvedBy: 'example-resolvedBy',
    resolutionNotes: 'example-resolutionNotes',
  },
  }),
);

const ApiKeyCreateRequestSchema = sharedRegistry.register(
  'ApiKeyCreateRequest',
  z.object({
    // KS-33: organizationId is now optional. Callers that issue
    // tenant-scoped keys without picking a specific org (SYSTEM_ADMIN
    // flows, originate's POST /api/admin/api-keys) pass null/undefined.
    organizationId: z.string().optional(),
    // KS-33: explicit tenantId override. When omitted the service
    // resolves tenant via x-tenant-id header → organizations.tenant_id
    // lookup → default-tenant fallback.
    tenantId: z.string().uuid().optional(),
    name: z.string().min(1).max(100),
    scopes: z.array(z.string()).optional(),
    rateLimit: z.number().int().min(1).max(10000).optional(),
    rateLimitWindow: z.number().int().min(60).max(86400).optional(),
    expiresAt: z.string().datetime().optional(),
    connectorId: z.string().optional(),
    // KS-1434: the runtime create schema (index.ts, the `rotate` field KS-577 added) has accepted `rotate`
    // since revoke-on-rotate landed, but this published schema omitted it, so an integrator reading the
    // contract, and a spec-driven caller such as Schemathesis, could not see the behaviour or send the
    // field. Declared with the runtime's own optionality and default (optional, false). Spec only: no
    // service source imports this file, only the OpenAPI generator and tests do. Every clause of the
    // description is traced to index.ts in the PR body.
    rotate: z.boolean().optional().default(false).openapi({
      description:
        'When true and a connectorId is supplied, the other active API keys for that connector in the same tenant are retired after the new key is minted: ' +
        'with API_KEY_ROTATION_GRACE_SECONDS unset or 0 they are deactivated, and with a positive value they are given an expiry that many seconds from now if that is earlier than their current one. ' +
        'In that case the 201 response reports priorKeysRevoked, where null means the retirement was attempted and failed and the prior key is still valid. ' +
        'Without a connectorId no prior key is retired.',
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    name: 'example-name',
  },
  }),
);

// KS-440 (response-side): POST /api/keys returns the canonical envelope
// `{ success, data: {...} }` (index.ts POST '/api/keys'), and the plaintext key
// field is `key` (not `apiKey`), with a `prefix` — and NO rateLimitWindow /
// expiresAt in the create response. The old flat schema (id/apiKey/... at top
// level, requiring rateLimitWindow) made every real 201 violate the response
// schema ("id is a required property", because id is nested under `data`).
// Publish the real envelope + real data fields.
const ApiKeyCreateResponseSchema = sharedRegistry.register(
  'ApiKeyCreateResponse',
  successEnvelope(
    z
      .object({
        id: z.string(),
        key: z.string().openapi({
          description:
            'PLAINTEXT key. Returned ONLY at creation time. Caller must store ' +
            'it; the service stores only a hashed version.',
        }),
        prefix: z.string(),
        name: z.string(),
        scopes: z.array(z.string()),
        rateLimit: z.number().int().positive(),
        createdAt: z.string(),
      })
      .passthrough(),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: 'example-id',
      key: 'example-key',
      prefix: 'example-prefix',
      name: 'example-name',
      scopes: [
        'example-scopes[]',
        'example-scopes[]',
      ],
      rateLimit: 1,
      createdAt: FX.timestamps.createdAt,
    },
  },
  }),
);

const ApiKeySchema = sharedRegistry.register(
  'ApiKey',
  z
    .object({
      id: z.string(),
      organizationId: z.string(),
      name: z.string(),
      scopes: z.array(z.string()),
      rateLimit: z.number().int().positive(),
      rateLimitWindow: z.number().int().positive(),
      expiresAt: z.string().nullable().optional(),
      lastUsedAt: z.string().nullable().optional(),
      revokedAt: z.string().nullable().optional(),
      createdAt: z.string(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    organizationId: FX.tenant.id,
    name: 'example-name',
    scopes: [
      'example-scopes[]',
      'example-scopes[]',
    ],
    rateLimit: 1,
    rateLimitWindow: 1,
    createdAt: 'example-createdAt',
  },
  }),
);

const ApiKeyListResponseSchema = sharedRegistry.register(
  'ApiKeyListResponse',
  z.object({
    keys: z.array(ApiKeySchema),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    keys: [
      {
        id: 'example-id',
        organizationId: FX.tenant.id,
        name: 'example-name',
        scopes: [
          'example-scopes[]',
          'example-scopes[]',
        ],
        rateLimit: 1,
        rateLimitWindow: 1,
        createdAt: 'example-createdAt',
      },
      {
        id: 'example-id',
        organizationId: FX.tenant.id,
        name: 'example-name',
        scopes: [
          'example-scopes[]',
          'example-scopes[]',
        ],
        rateLimit: 1,
        rateLimitWindow: 1,
        createdAt: 'example-createdAt',
      },
    ],
  },
  }),
);

const ApiKeyValidateRequestSchema = sharedRegistry.register(
  'ApiKeyValidateRequest',
  // KS-444: the runtime field is `key` (index.ts POST /api/keys/validate), and
  // the api-gateway — the endpoint's real service-to-service caller — sends
  // `{ key }` (api-gateway/src/middleware/auth.ts validateApiKey). The spec
  // advertised `apiKey`, so every spec-compliant request 400'd with
  // "API key required" (verified live 2026-07-13; same class as the KS-255
  // ResetPasswordRequest field-name drift). min(1) mirrors the runtime's
  // non-empty requirement.
  z.object({
    key: z.string().min(1),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    key: 'example-key',
  },
  }),
);

// KS-440 (response-side): the handler wraps the validation result in the
// canonical envelope `{ success, data: { valid, ... } }` (index.ts POST
// '/api/keys/validate') — the flat schema (bare `valid` at top level) made
// every real 200 violate the response schema ("valid is a required property",
// because valid is nested under `data`). PR #499 fixed this op's REQUEST field
// (apiKey→key); this is the separate RESPONSE-side envelope fix. Publish the
// envelope. `tenantId` is NOT always a UUID at runtime (the default-tenant
// fallback returns the literal string "default"), so it's a plain string here.
const ApiKeyValidateResponseSchema = sharedRegistry.register(
  'ApiKeyValidateResponse',
  successEnvelope(
    z
      .object({
        valid: z.boolean(),
        keyId: z.string().nullable().optional(),
        organizationId: z.string().nullable().optional(),
        // KS-33: tenantId is returned on every successful validation so the
        // gateway can populate req.tenantId for sk_*-authenticated requests
        // without a second roundtrip.
        tenantId: z.string().nullable().optional(),
        scopes: z.array(z.string()).optional(),
        rateLimit: z.number().int().nullable().optional(),
        rateLimitWindow: z.number().int().nullable().optional(),
        connectorId: z.string().nullable().optional(),
        reason: z.string().optional(),
      })
      .passthrough(),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      valid: true,
    },
  },
  }),
);

const RateLimitCheckRequestSchema = sharedRegistry.register(
  'RateLimitCheckRequest',
  z.object({
    // KS-952 F10: the runtime bounds the key length; the contract says so too.
    key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
    limit: z.number().int().min(1).optional(),
    // #882 gate F2: the RUNTIME gained `.max(MAX_RATE_LIMIT_WINDOW_MS)` (KS-698
    // fix 1) while this published schema kept only a `.min()`. A client following
    // the contract could send a legal-per-spec windowMs the runtime answers 400
    // to — and the tool that FOUND KS-698 is spec-driven, so it generates exactly
    // those values. Imported from the shared bounds module rather than restated,
    // so the two cannot drift again.
    windowMs: z.number().int().min(1000).max(MAX_RATE_LIMIT_WINDOW_MS).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    key: 'example-key',
  },
  }),
);

// KS-455: the runtime wraps the result in the {success,data} envelope and adds
// retryAfter (seconds) on the denied branch — the bare object never matched.
const RateLimitCheckResponseSchema = sharedRegistry.register(
  'RateLimitCheckResponse',
  successEnvelope(
    z.object({
      allowed: z.boolean(),
      remaining: z.number().int().nonnegative(),
      resetAt: z.string(),
      retryAfter: z.number().int().nonnegative().optional(),
    }),
  ).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      allowed: true,
      remaining: 0,
      resetAt: FX.timestamps.createdAt,
    },
  },
  }),
);

const RateLimitResetRequestSchema = sharedRegistry.register(
  'RateLimitResetRequest',
  // KS-444: min(1) mirrors the runtime's non-empty requirement (the handler
  // 400s an empty/missing key), matching RateLimitCheckRequest above.
  z.object({
    key: z.string().min(1).max(RATE_LIMIT_KEY_MAX),
    // KS-952: the scope the bucket lives under. /check derives its bucket from
    // the caller, so a reset has to be able to name whose bucket it clears —
    // that cross-tenant reach is the intended function of a platform-operator
    // reset, and this route is platform-gated. Omitted => the caller's own.
    //
    // KS-970 item 6: the runtime refuses a BLANK value and an unpaired
    // surrogate on both fields, and neither refusal was published — the same
    // class as round 1's F1, where /check refused with 403 and the responses
    // block did not say so. A zod `.refine()` never reaches the generated
    // schema, so the constraint has to be stated in the description or it is
    // not in the contract at all. `maxLength` here counts CODE POINTS, and
    // KS-970 item 4 aligned the runtime bound to the same unit.
    tenantId: z
      .string()
      .min(1)
      .max(RATE_LIMIT_KEY_MAX)
      .optional()
      .openapi({
        description:
          'Whose bucket to clear. Omit to target the caller. Refused with 400 if present ' +
          'but blank, or if it contains an unpaired surrogate. `maxLength` counts code points.',
      }),
    userId: z
      .string()
      .min(1)
      .max(RATE_LIMIT_KEY_MAX)
      .optional()
      .openapi({
        description:
          'Whose bucket to clear, within `tenantId`. Omit to target the caller. Refused with ' +
          '400 if present but blank, or if it contains an unpaired surrogate. `maxLength` ' +
          'counts code points.',
      }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    key: 'example-key',
  },
  }),
);

const SecuritySuccessSchema = sharedRegistry.register(
  'SecuritySuccess',
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
// ROUTES — /api/audit
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/audit',
  tags: ['Audit'],
  summary: 'Append an audit log entry',
  description:
    'Service-to-service: every other service writes user/admin actions ' +
    'here. PII-bearing fields in `details` are encrypted at rest (audit ' +
    '1.3 phase 5).',
  security: [{ bearerAuth: [] }],
  request: {
    body: { content: { 'application/json': { schema: AuditLogCreateRequestSchema } } },
  },
  responses: {
    201: {
      description: 'Audit entry created (echoes the new entry id)',
      content: { 'application/json': { schema: AuditLogCreateResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/security/audit',
  tags: ['Audit'],
  summary: 'List audit log entries (paginated)',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Audit log page',
      content: { 'application/json': { schema: AuditLogListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/security/audit/{id}',
  tags: ['Audit'],
  summary: 'Get a single audit entry',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Audit entry',
      content: { 'application/json': { schema: AuditLogEntrySchema } },
    },
    401: commonErrorResponses[401],
    404: commonErrorResponses[404],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/events (security events)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/events',
  tags: ['Security Events'],
  summary: 'Record a security event',
  description:
    'Higher-signal than /api/audit: severity-tagged, surfaces in the SOC ' +
    'dashboard, can trigger alerts. Use /api/audit for routine actions.',
  security: [{ bearerAuth: [] }],
  request: {
    body: { content: { 'application/json': { schema: SecurityEventCreateRequestSchema } } },
  },
  responses: {
    201: {
      description: 'Event created',
      content: { 'application/json': { schema: SecurityEventCreateResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/security/events',
  tags: ['Security Events'],
  summary: 'List security events',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Event list',
      content: { 'application/json': { schema: SecurityEventListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/security/events/{id}/resolve',
  tags: ['Security Events'],
  summary: 'Mark a security event as resolved',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: {
      content: { 'application/json': { schema: SecurityEventResolveRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'Event resolved',
      // KS-455: runtime wraps the event in {success,data}
      content: { 'application/json': { schema: SecurityEventCreateResponseSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'Event not found' },
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/keys (API keys)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/keys',
  tags: ['API Keys'],
  summary: 'Issue an API key',
  description:
    'The plaintext key is returned ONLY in this response. Service stores ' +
    'only a hash. Caller must persist the plaintext immediately.',
  security: [{ bearerAuth: [] }],
  request: {
    body: { content: { 'application/json': { schema: ApiKeyCreateRequestSchema } } },
  },
  responses: {
    201: {
      description: 'API key issued (plaintext returned ONCE)',
      content: { 'application/json': { schema: ApiKeyCreateResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/security/keys',
  tags: ['API Keys'],
  summary: 'List API keys for the caller\'s organisation',
  description:
    'Lists metadata only (no plaintext, no hash). Use /api/keys/validate ' +
    'to verify a specific key.',
  security: [{ bearerAuth: [] }],
  request: { query: z.object({ organizationId: z.string().uuid() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'API key list',
      content: { 'application/json': { schema: ApiKeyListResponseSchema } },
    },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'delete',
  path: '/api/security/keys/{id}',
  tags: ['API Keys'],
  summary: 'Revoke an API key',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Key revoked',
      content: { 'application/json': { schema: SecuritySuccessSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'Key not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// KS-1570 PR B: an ADMIN's organisation scope, written and read by a platform role only.
const AdminScopePutRequestSchema = sharedRegistry.register(
  'AdminScopePutRequest',
  z.object({
    tenantId: z.string().uuid(),
    // Replaces the whole set; an empty list clears it. Every id must be an organisation of `tenantId`.
    organizationIds: z.array(z.string().uuid()).max(1000),
  }),
);

const AdminScopeResponseSchema = sharedRegistry.register(
  'AdminScopeResponse',
  z.object({
    success: z.literal(true),
    data: z.object({
      userId: z.string().uuid(),
      tenantId: z.string().uuid(),
      // Present on PUT only: the set before this write.
      before: z.array(z.string().uuid()).optional(),
      organizationIds: z.array(z.string().uuid()),
    }),
  }),
);

sharedRegistry.registerPath({
  method: 'put',
  path: '/api/security/keys/admin-scopes/{userId}',
  tags: ['API Keys'],
  summary: "Replace an ADMIN's organisation scope (platform roles only; audited)",
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ userId: z.string().uuid() }),
    body: { content: { 'application/json': { schema: AdminScopePutRequestSchema } } },
  },
  responses: {
    200: { description: 'Scope replaced', content: { 'application/json': { schema: AdminScopeResponseSchema } } },
    400: { ...commonErrorResponses[400], description: 'Validation failed, or an organisation is not of that tenant' },
    401: commonErrorResponses[401],
    403: { ...commonErrorResponses[403], description: 'Not a platform role' },
    404: { ...commonErrorResponses[404], description: 'No ADMIN with that id in that tenant' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/security/keys/admin-scopes/{userId}',
  tags: ['API Keys'],
  summary: "Read an ADMIN's organisation scope (platform roles only)",
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ userId: z.string().uuid() }),
    query: z.object({ tenantId: z.string().uuid() }),
  },
  responses: {
    // The pull request 1539 gate's n3: this operation declared a 404 it never produces. An unknown
    // user, or a target that is not an ADMIN, answers 200 with an EMPTY organizationIds list —
    // measured by the gate against an ISSUER_ADMIN target. The 404 is removed rather than the
    // behaviour changed: a reader cannot tell 'no scope' from 'no such user' here, and that is the
    // non-probing answer. The PUT's 404 is real and stays.
    200: { description: "The scope. An unknown user, or a target that is not an ADMIN, answers 200 with an empty organizationIds list rather than a 404.", content: { 'application/json': { schema: AdminScopeResponseSchema } } },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: { ...commonErrorResponses[403], description: 'Not a platform role' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/keys/validate',
  security: [{ bearerAuth: [] }],
  tags: ['API Keys'],
  summary: 'Validate an API key (returns its scopes + org if valid)',
  description:
    'Service-to-service: api-gateway calls this on every connector-API ' +
    'request to authenticate.',
  request: {
    body: {
      content: { 'application/json': { schema: ApiKeyValidateRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'Validation result (HTTP 200 even on invalid; check `valid`)',
      content: { 'application/json': { schema: ApiKeyValidateResponseSchema } },
    },
    400: commonErrorResponses[400],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/rate-limit
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/rate-limit/check',
  security: [{ bearerAuth: [] }],
  tags: ['Rate Limits'],
  summary: 'Check + decrement a rate-limit bucket',
  description:
    'Check and decrement the CALLING principal\'s rate-limit bucket. `key` ' +
    'names a bucket within the caller\'s own namespace (KS-952): it is ' +
    'combined with the tenant and user from the verified token, so it cannot ' +
    'select another principal\'s bucket. Returns `allowed`, remaining budget ' +
    'and reset time. A token carrying neither a tenant nor a user claim is ' +
    'refused 403. ' +
    'This previously read "Service-to-service: api-gateway calls before ' +
    'forwarding sensitive endpoints". That consumer does not exist — a census ' +
    'of the tracked tree finds no caller outside this service, against controls ' +
    'that do find the gateway\'s real calls to /keys/validate and /audit/logs. ' +
    'The gateway rate-limits with its own in-process middleware.',
  request: {
    body: { content: { 'application/json': { schema: RateLimitCheckRequestSchema } } },
  },
  responses: {
    200: {
      description: 'Rate-limit result',
      content: { 'application/json': { schema: RateLimitCheckResponseSchema } },
    },
    429: { ...commonErrorResponses[429], description: 'Limit exceeded (also signaled by allowed=false at 200)' },
    400: commonErrorResponses[400],
    // KS-952 F1: this route ADDS a 403 (a token carrying neither a tenant nor a
    // user claim is refused rather than sharing a bucket) and the description
    // three blocks above already says so — but the responses block omitted it,
    // so the published contract disagreed with its own prose and with the code.
    // The `/reset` sibling below has carried this line all along.
    403: commonErrorResponses[403],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/security/rate-limit/reset',
  tags: ['Rate Limits'],
  summary: 'Reset a rate-limit bucket (admin)',
  description:
    'Clears a rate-limit bucket. Requires a platform role. `tenantId` and ' +
    '`userId` name WHOSE bucket is cleared (KS-952); omit them to clear the ' +
    'caller\'s own. Buckets are stored per principal, so a bare `key` clears ' +
    'only the bucket of the principal named by those fields.',
  security: [{ bearerAuth: [] }],
  request: {
    body: { content: { 'application/json': { schema: RateLimitResetRequestSchema } } },
  },
  responses: {
    200: {
      description: 'Bucket reset',
      content: { 'application/json': { schema: SecuritySuccessSchema } },
    },
    401: commonErrorResponses[401],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});
