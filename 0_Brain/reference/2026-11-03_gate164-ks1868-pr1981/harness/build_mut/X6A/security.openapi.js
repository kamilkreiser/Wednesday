"use strict";
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
Object.defineProperty(exports, "__esModule", { value: true });
const shared_1 = require("@secuura/shared");
const rateLimitBounds_1 = require("./rateLimitBounds");
// KS-952: same rule as the line above — the published bound is IMPORTED from the
// module the runtime enforces, never restated, so the two cannot drift.
const rateLimitScope_1 = require("./rateLimitScope");
// -----------------------------------------------------------------------------
// SCHEMAS
// -----------------------------------------------------------------------------
const SeveritySchema = shared_1.z.enum(['low', 'medium', 'high', 'critical']);
const AuditLogCreateRequestSchema = shared_1.sharedRegistry.register('AuditLogCreateRequest', shared_1.z.object({
    userId: shared_1.z.string().optional(),
    organizationId: shared_1.z.string().optional(),
    action: shared_1.z.string().min(1),
    resourceType: shared_1.z.string().min(1),
    resourceId: shared_1.z.string().optional(),
    ipAddress: shared_1.z.string().optional(),
    userAgent: shared_1.z.string().optional(),
    details: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).optional(),
    previousState: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).optional(),
    newState: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).optional(),
    success: shared_1.z.boolean().optional(),
    errorMessage: shared_1.z.string().optional(),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        action: 'example-action',
        resourceType: 'example-resourceType',
    },
}));
const AuditLogEntrySchema = shared_1.sharedRegistry.register('AuditLogEntry', shared_1.z
    .object({
    id: shared_1.z.string(),
    userId: shared_1.z.string().nullable().optional(),
    organizationId: shared_1.z.string().nullable().optional(),
    action: shared_1.z.string(),
    resourceType: shared_1.z.string(),
    resourceId: shared_1.z.string().nullable().optional(),
    ipAddress: shared_1.z.string().nullable().optional(),
    userAgent: shared_1.z.string().nullable().optional(),
    details: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).nullable().optional(),
    success: shared_1.z.boolean(),
    errorMessage: shared_1.z.string().nullable().optional(),
    createdAt: shared_1.z.string(),
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
    description: 'A platform audit log entry. PII-bearing fields in `details` are ' +
        'PII-encrypted at rest (audit 1.3 phase 5).',
}));
// KS-144: real response is flat `{ success, logs: [...], total }` (no `data`
// wrapper; key is `logs`, not `entries`).
const AuditLogListResponseSchema = shared_1.sharedRegistry.register('AuditLogListResponse', shared_1.z
    .object({
    success: shared_1.z.literal(true),
    logs: shared_1.z.array(AuditLogEntrySchema),
    total: shared_1.z.number().optional(),
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
                createdAt: shared_1.FX.timestamps.createdAt,
            },
            {
                id: 'example-id',
                action: 'example-action',
                resourceType: 'example-resourceType',
                success: true,
                createdAt: shared_1.FX.timestamps.createdAt,
            },
        ],
    },
}));
// KS-440 (response-side): POST /api/audit returns the canonical envelope
// `{ success, data: { id } }` (index.ts POST '/api/audit') — it echoes ONLY the
// new entry's id, not the full audit record. The old AuditLogEntrySchema (flat,
// requiring action/resourceType/success/createdAt) made every real 201 violate
// the response schema. Publish the real envelope. (AuditLogEntrySchema stays the
// shape for the GET list/detail reads, which return the full record.)
const AuditLogCreateResponseSchema = shared_1.sharedRegistry.register('AuditLogCreateResponse', (0, shared_1.successEnvelope)(shared_1.z.object({ id: shared_1.z.string() }).passthrough()).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        success: true,
        data: {
            id: 'example-id',
        },
    },
}));
const SecurityEventCreateRequestSchema = shared_1.sharedRegistry.register('SecurityEventCreateRequest', shared_1.z.object({
    eventType: shared_1.z.string().min(1),
    severity: SeveritySchema,
    source: shared_1.z.string().min(1),
    userId: shared_1.z.string().optional(),
    ipAddress: shared_1.z.string().optional(),
    details: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).optional(),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        eventType: 'example-eventType',
        severity: 'low',
        source: 'example-source',
    },
}));
const SecurityEventSchema = shared_1.sharedRegistry.register('SecurityEvent', shared_1.z
    .object({
    id: shared_1.z.string(),
    eventType: shared_1.z.string(),
    severity: SeveritySchema,
    source: shared_1.z.string(),
    userId: shared_1.z.string().nullable().optional(),
    ipAddress: shared_1.z.string().nullable().optional(),
    details: shared_1.z.record(shared_1.z.string(), shared_1.z.unknown()).nullable().optional(),
    resolved: shared_1.z.boolean(),
    resolvedAt: shared_1.z.string().nullable().optional(),
    resolvedBy: shared_1.z.string().nullable().optional(),
    createdAt: shared_1.z.string(),
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
}));
// KS-440 (response-side): POST /api/events returns the canonical envelope
// `{ success, data: <event> }` (index.ts POST '/api/events') — the old flat
// SecurityEventSchema made every real 201 violate the response schema ("id is a
// required property", because the event is nested under `data`). Publish the
// envelope wrapping the event.
const SecurityEventCreateResponseSchema = shared_1.sharedRegistry.register('SecurityEventCreateResponse', (0, shared_1.successEnvelope)(SecurityEventSchema).openapi({
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
            createdAt: shared_1.FX.timestamps.createdAt,
        },
    },
}));
// KS-144: real response is enveloped `{ success, data: { events, total, limit, offset } }`.
const SecurityEventListResponseSchema = shared_1.sharedRegistry.register('SecurityEventListResponse', (0, shared_1.successEnvelope)(shared_1.z
    .object({
    events: shared_1.z.array(SecurityEventSchema),
    total: shared_1.z.number().optional(),
    limit: shared_1.z.number().optional(),
    offset: shared_1.z.number().optional(),
})
    .passthrough()).openapi({
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
                    createdAt: shared_1.FX.timestamps.createdAt,
                },
                {
                    id: 'example-id',
                    eventType: 'example-eventType',
                    severity: 'low',
                    source: 'example-source',
                    resolved: true,
                    createdAt: shared_1.FX.timestamps.createdAt,
                },
            ],
        },
    },
}));
const SecurityEventResolveRequestSchema = shared_1.sharedRegistry.register('SecurityEventResolveRequest', shared_1.z
    .object({
    resolvedBy: shared_1.z.string().optional(),
    resolutionNotes: shared_1.z.string().optional(),
})
    .passthrough().openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        resolvedBy: 'example-resolvedBy',
        resolutionNotes: 'example-resolutionNotes',
    },
}));
const ApiKeyCreateRequestSchema = shared_1.sharedRegistry.register('ApiKeyCreateRequest', shared_1.z.object({
    // KS-33: organizationId is now optional. Callers that issue
    // tenant-scoped keys without picking a specific org (SYSTEM_ADMIN
    // flows, originate's POST /api/admin/api-keys) pass null/undefined.
    organizationId: shared_1.z.string().optional(),
    // KS-33: explicit tenantId override. When omitted the service
    // resolves tenant via x-tenant-id header → organizations.tenant_id
    // lookup → default-tenant fallback.
    tenantId: shared_1.z.string().uuid().optional(),
    name: shared_1.z.string().min(1).max(100),
    scopes: shared_1.z.array(shared_1.z.string()).optional(),
    rateLimit: shared_1.z.number().int().min(1).max(10000).optional(),
    rateLimitWindow: shared_1.z.number().int().min(60).max(86400).optional(),
    expiresAt: shared_1.z.string().datetime().optional(),
    connectorId: shared_1.z.string().optional(),
    // KS-1434: the runtime create schema (index.ts, the `rotate` field KS-577 added) has accepted `rotate`
    // since revoke-on-rotate landed, but this published schema omitted it, so an integrator reading the
    // contract, and a spec-driven caller such as Schemathesis, could not see the behaviour or send the
    // field. Declared with the runtime's own optionality and default (optional, false). Spec only: no
    // service source imports this file, only the OpenAPI generator and tests do. Every clause of the
    // description is traced to index.ts in the PR body.
    rotate: shared_1.z.boolean().optional().default(false).openapi({
        description: 'When true and a connectorId is supplied, the other active API keys for that connector in the same tenant are retired after the new key is minted: ' +
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
}));
// KS-440 (response-side): POST /api/keys returns the canonical envelope
// `{ success, data: {...} }` (index.ts POST '/api/keys'), and the plaintext key
// field is `key` (not `apiKey`), with a `prefix` — and NO rateLimitWindow /
// expiresAt in the create response. The old flat schema (id/apiKey/... at top
// level, requiring rateLimitWindow) made every real 201 violate the response
// schema ("id is a required property", because id is nested under `data`).
// Publish the real envelope + real data fields.
const ApiKeyCreateResponseSchema = shared_1.sharedRegistry.register('ApiKeyCreateResponse', (0, shared_1.successEnvelope)(shared_1.z
    .object({
    id: shared_1.z.string(),
    key: shared_1.z.string().openapi({
        description: 'PLAINTEXT key. Returned ONLY at creation time. Caller must store ' +
            'it; the service stores only a hashed version.',
    }),
    prefix: shared_1.z.string(),
    name: shared_1.z.string(),
    scopes: shared_1.z.array(shared_1.z.string()),
    rateLimit: shared_1.z.number().int().positive(),
    createdAt: shared_1.z.string(),
})
    .passthrough()).openapi({
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
            createdAt: shared_1.FX.timestamps.createdAt,
        },
    },
}));
const ApiKeySchema = shared_1.sharedRegistry.register('ApiKey', shared_1.z
    .object({
    id: shared_1.z.string(),
    organizationId: shared_1.z.string(),
    name: shared_1.z.string(),
    scopes: shared_1.z.array(shared_1.z.string()),
    rateLimit: shared_1.z.number().int().positive(),
    rateLimitWindow: shared_1.z.number().int().positive(),
    expiresAt: shared_1.z.string().nullable().optional(),
    lastUsedAt: shared_1.z.string().nullable().optional(),
    revokedAt: shared_1.z.string().nullable().optional(),
    createdAt: shared_1.z.string(),
})
    .passthrough().openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        id: 'example-id',
        organizationId: shared_1.FX.tenant.id,
        name: 'example-name',
        scopes: [
            'example-scopes[]',
            'example-scopes[]',
        ],
        rateLimit: 1,
        rateLimitWindow: 1,
        createdAt: 'example-createdAt',
    },
}));
const ApiKeyListResponseSchema = shared_1.sharedRegistry.register('ApiKeyListResponse', shared_1.z.object({
    keys: shared_1.z.array(ApiKeySchema),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        keys: [
            {
                id: 'example-id',
                organizationId: shared_1.FX.tenant.id,
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
                organizationId: shared_1.FX.tenant.id,
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
}));
const ApiKeyValidateRequestSchema = shared_1.sharedRegistry.register('ApiKeyValidateRequest', 
// KS-444: the runtime field is `key` (index.ts POST /api/keys/validate), and
// the api-gateway — the endpoint's real service-to-service caller — sends
// `{ key }` (api-gateway/src/middleware/auth.ts validateApiKey). The spec
// advertised `apiKey`, so every spec-compliant request 400'd with
// "API key required" (verified live 2026-07-13; same class as the KS-255
// ResetPasswordRequest field-name drift). min(1) mirrors the runtime's
// non-empty requirement.
shared_1.z.object({
    key: shared_1.z.string().min(1),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        key: 'example-key',
    },
}));
// KS-440 (response-side): the handler wraps the validation result in the
// canonical envelope `{ success, data: { valid, ... } }` (index.ts POST
// '/api/keys/validate') — the flat schema (bare `valid` at top level) made
// every real 200 violate the response schema ("valid is a required property",
// because valid is nested under `data`). PR #499 fixed this op's REQUEST field
// (apiKey→key); this is the separate RESPONSE-side envelope fix. Publish the
// envelope. `tenantId` is NOT always a UUID at runtime (the default-tenant
// fallback returns the literal string "default"), so it's a plain string here.
const ApiKeyValidateResponseSchema = shared_1.sharedRegistry.register('ApiKeyValidateResponse', (0, shared_1.successEnvelope)(shared_1.z
    .object({
    valid: shared_1.z.boolean(),
    keyId: shared_1.z.string().nullable().optional(),
    organizationId: shared_1.z.string().nullable().optional(),
    // KS-33: tenantId is returned on every successful validation so the
    // gateway can populate req.tenantId for sk_*-authenticated requests
    // without a second roundtrip.
    tenantId: shared_1.z.string().nullable().optional(),
    scopes: shared_1.z.array(shared_1.z.string()).optional(),
    rateLimit: shared_1.z.number().int().nullable().optional(),
    rateLimitWindow: shared_1.z.number().int().nullable().optional(),
    connectorId: shared_1.z.string().nullable().optional(),
    reason: shared_1.z.string().optional(),
})
    .passthrough()).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        success: true,
        data: {
            valid: true,
        },
    },
}));
const RateLimitCheckRequestSchema = shared_1.sharedRegistry.register('RateLimitCheckRequest', shared_1.z.object({
    // KS-952 F10: the runtime bounds the key length; the contract says so too.
    key: shared_1.z.string().min(1).max(rateLimitScope_1.RATE_LIMIT_KEY_MAX),
    limit: shared_1.z.number().int().min(1).optional(),
    // #882 gate F2: the RUNTIME gained `.max(MAX_RATE_LIMIT_WINDOW_MS)` (KS-698
    // fix 1) while this published schema kept only a `.min()`. A client following
    // the contract could send a legal-per-spec windowMs the runtime answers 400
    // to — and the tool that FOUND KS-698 is spec-driven, so it generates exactly
    // those values. Imported from the shared bounds module rather than restated,
    // so the two cannot drift again.
    windowMs: shared_1.z.number().int().min(1000).max(rateLimitBounds_1.MAX_RATE_LIMIT_WINDOW_MS).optional(),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        key: 'example-key',
    },
}));
// KS-455: the runtime wraps the result in the {success,data} envelope and adds
// retryAfter (seconds) on the denied branch — the bare object never matched.
const RateLimitCheckResponseSchema = shared_1.sharedRegistry.register('RateLimitCheckResponse', (0, shared_1.successEnvelope)(shared_1.z.object({
    allowed: shared_1.z.boolean(),
    remaining: shared_1.z.number().int().nonnegative(),
    resetAt: shared_1.z.string(),
    retryAfter: shared_1.z.number().int().nonnegative().optional(),
})).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        success: true,
        data: {
            allowed: true,
            remaining: 0,
            resetAt: shared_1.FX.timestamps.createdAt,
        },
    },
}));
const RateLimitResetRequestSchema = shared_1.sharedRegistry.register('RateLimitResetRequest', 
// KS-444: min(1) mirrors the runtime's non-empty requirement (the handler
// 400s an empty/missing key), matching RateLimitCheckRequest above.
shared_1.z.object({
    key: shared_1.z.string().min(1).max(rateLimitScope_1.RATE_LIMIT_KEY_MAX),
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
    tenantId: shared_1.z
        .string()
        .min(1)
        .max(rateLimitScope_1.RATE_LIMIT_KEY_MAX)
        .optional()
        .openapi({
        description: 'Whose bucket to clear. Omit to target the caller. Refused with 400 if present ' +
            'but blank, or if it contains an unpaired surrogate. `maxLength` counts code points.',
    }),
    userId: shared_1.z
        .string()
        .min(1)
        .max(rateLimitScope_1.RATE_LIMIT_KEY_MAX)
        .optional()
        .openapi({
        description: 'Whose bucket to clear, within `tenantId`. Omit to target the caller. Refused with ' +
            '400 if present but blank, or if it contains an unpaired surrogate. `maxLength` ' +
            'counts code points.',
    }),
}).openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        key: 'example-key',
    },
}));
const SecuritySuccessSchema = shared_1.sharedRegistry.register('SecuritySuccess', shared_1.z
    .object({
    success: shared_1.z.boolean(),
    message: shared_1.z.string().optional(),
})
    .passthrough().openapi({
    // KS-256: generated example (synthesised, masked). Guarded by
    // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
        success: true,
    },
}));
// -----------------------------------------------------------------------------
// ROUTES — /api/audit
// -----------------------------------------------------------------------------
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/audit',
    tags: ['Audit'],
    summary: 'Append an audit log entry',
    description: 'Service-to-service: every other service writes user/admin actions ' +
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
        400: shared_1.commonErrorResponses[400],
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'get',
    path: '/api/security/audit',
    tags: ['Audit'],
    summary: 'List audit log entries (paginated)',
    security: [{ bearerAuth: [] }],
    responses: {
        400: shared_1.commonErrorResponses[400],
        200: {
            description: 'Audit log page',
            content: { 'application/json': { schema: AuditLogListResponseSchema } },
        },
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'get',
    path: '/api/security/audit/{id}',
    tags: ['Audit'],
    summary: 'Get a single audit entry',
    security: [{ bearerAuth: [] }],
    request: { params: shared_1.z.object({ id: shared_1.z.string() }) },
    responses: {
        400: shared_1.commonErrorResponses[400],
        200: {
            description: 'Audit entry',
            content: { 'application/json': { schema: AuditLogEntrySchema } },
        },
        401: shared_1.commonErrorResponses[401],
        404: shared_1.commonErrorResponses[404],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
// -----------------------------------------------------------------------------
// ROUTES — /api/events (security events)
// -----------------------------------------------------------------------------
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/events',
    tags: ['Security Events'],
    summary: 'Record a security event',
    description: 'Higher-signal than /api/audit: severity-tagged, surfaces in the SOC ' +
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
        400: shared_1.commonErrorResponses[400],
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'get',
    path: '/api/security/events',
    tags: ['Security Events'],
    summary: 'List security events',
    security: [{ bearerAuth: [] }],
    responses: {
        400: shared_1.commonErrorResponses[400],
        200: {
            description: 'Event list',
            content: { 'application/json': { schema: SecurityEventListResponseSchema } },
        },
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'patch',
    path: '/api/security/events/{id}/resolve',
    tags: ['Security Events'],
    summary: 'Mark a security event as resolved',
    security: [{ bearerAuth: [] }],
    request: {
        params: shared_1.z.object({ id: shared_1.z.string() }),
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
        401: shared_1.commonErrorResponses[401],
        404: { ...shared_1.commonErrorResponses[404], description: 'Event not found' },
        400: shared_1.commonErrorResponses[400],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
// -----------------------------------------------------------------------------
// ROUTES — /api/keys (API keys)
// -----------------------------------------------------------------------------
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/keys',
    tags: ['API Keys'],
    summary: 'Issue an API key',
    description: 'The plaintext key is returned ONLY in this response. Service stores ' +
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
        400: shared_1.commonErrorResponses[400],
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'get',
    path: '/api/security/keys',
    tags: ['API Keys'],
    summary: 'List API keys for the caller\'s organisation',
    description: 'Lists metadata only (no plaintext, no hash). Use /api/keys/validate ' +
        'to verify a specific key.',
    security: [{ bearerAuth: [] }],
    request: { query: shared_1.z.object({ organizationId: shared_1.z.string().uuid() }) },
    responses: {
        400: shared_1.commonErrorResponses[400],
        200: {
            description: 'API key list',
            content: { 'application/json': { schema: ApiKeyListResponseSchema } },
        },
        401: shared_1.commonErrorResponses[401],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'delete',
    path: '/api/security/keys/{id}',
    tags: ['API Keys'],
    summary: 'Revoke an API key',
    security: [{ bearerAuth: [] }],
    request: { params: shared_1.z.object({ id: shared_1.z.string() }) },
    responses: {
        400: shared_1.commonErrorResponses[400],
        200: {
            description: 'Key revoked',
            content: { 'application/json': { schema: SecuritySuccessSchema } },
        },
        401: shared_1.commonErrorResponses[401],
        404: { ...shared_1.commonErrorResponses[404], description: 'Key not found' },
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
// KS-1570 PR B: an ADMIN's organisation scope, written and read by a platform role only.
const AdminScopePutRequestSchema = shared_1.sharedRegistry.register('AdminScopePutRequest', shared_1.z.object({
    tenantId: shared_1.z.string().uuid(),
    // Replaces the whole set; an empty list clears it. Every id must be an organisation of `tenantId`.
    organizationIds: shared_1.z.array(shared_1.z.string().uuid()).max(1000),
}));
const AdminScopeResponseSchema = shared_1.sharedRegistry.register('AdminScopeResponse', shared_1.z.object({
    success: shared_1.z.literal(true),
    data: shared_1.z.object({
        userId: shared_1.z.string().uuid(),
        tenantId: shared_1.z.string().uuid(),
        // Present on PUT only: the set before this write.
        before: shared_1.z.array(shared_1.z.string().uuid()).optional(),
        organizationIds: shared_1.z.array(shared_1.z.string().uuid()),
    }),
}));
shared_1.sharedRegistry.registerPath({
    method: 'put',
    path: '/api/security/keys/admin-scopes/{userId}',
    tags: ['API Keys'],
    summary: "Replace an ADMIN's organisation scope (platform roles only; audited)",
    security: [{ bearerAuth: [] }],
    request: {
        params: shared_1.z.object({ userId: shared_1.z.string().uuid() }),
        body: { content: { 'application/json': { schema: AdminScopePutRequestSchema } } },
    },
    responses: {
        200: { description: 'Scope replaced', content: { 'application/json': { schema: AdminScopeResponseSchema } } },
        400: { ...shared_1.commonErrorResponses[400], description: 'Validation failed, or an organisation is not of that tenant' },
        401: shared_1.commonErrorResponses[401],
        403: { ...shared_1.commonErrorResponses[403], description: 'Not a platform role' },
        404: { ...shared_1.commonErrorResponses[404], description: 'No ADMIN with that id in that tenant' },
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'get',
    path: '/api/security/keys/admin-scopes/{userId}',
    tags: ['API Keys'],
    summary: "Read an ADMIN's organisation scope (platform roles only)",
    security: [{ bearerAuth: [] }],
    request: {
        params: shared_1.z.object({ userId: shared_1.z.string().uuid() }),
        query: shared_1.z.object({ tenantId: shared_1.z.string().uuid() }),
    },
    responses: {
        // The pull request 1539 gate's n3: this operation declared a 404 it never produces. An unknown
        // user, or a target that is not an ADMIN, answers 200 with an EMPTY organizationIds list —
        // measured by the gate against an ISSUER_ADMIN target. The 404 is removed rather than the
        // behaviour changed: a reader cannot tell 'no scope' from 'no such user' here, and that is the
        // non-probing answer. The PUT's 404 is real and stays.
        200: { description: "The scope. An unknown user, or a target that is not an ADMIN, answers 200 with an empty organizationIds list rather than a 404.", content: { 'application/json': { schema: AdminScopeResponseSchema } } },
        400: shared_1.commonErrorResponses[400],
        401: shared_1.commonErrorResponses[401],
        403: { ...shared_1.commonErrorResponses[403], description: 'Not a platform role' },
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/keys/validate',
    security: [{ bearerAuth: [] }],
    tags: ['API Keys'],
    summary: 'Validate an API key (returns its scopes + org if valid)',
    description: 'Service-to-service: api-gateway calls this on every connector-API ' +
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
        400: shared_1.commonErrorResponses[400],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
        401: shared_1.commonErrorResponses[401],
    },
});
// -----------------------------------------------------------------------------
// ROUTES — /api/rate-limit
// -----------------------------------------------------------------------------
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/rate-limit/check',
    security: [{ bearerAuth: [] }],
    tags: ['Rate Limits'],
    summary: 'Check + decrement a rate-limit bucket',
    description: 'Check and decrement the CALLING principal\'s rate-limit bucket. `key` ' +
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
        429: { ...shared_1.commonErrorResponses[429], description: 'Limit exceeded (also signaled by allowed=false at 200)' },
        400: shared_1.commonErrorResponses[400],
        // KS-952 F1: this route ADDS a 403 (a token carrying neither a tenant nor a
        // user claim is refused rather than sharing a bucket) and the description
        // three blocks above already says so — but the responses block omitted it,
        // so the published contract disagreed with its own prose and with the code.
        // The `/reset` sibling below has carried this line all along.
        403: shared_1.commonErrorResponses[403],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
        401: shared_1.commonErrorResponses[401],
    },
});
shared_1.sharedRegistry.registerPath({
    method: 'post',
    path: '/api/security/rate-limit/reset',
    tags: ['Rate Limits'],
    summary: 'Reset a rate-limit bucket (admin)',
    description: 'Clears a rate-limit bucket. Requires a platform role. `tenantId` and ' +
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
        401: shared_1.commonErrorResponses[401],
        400: shared_1.commonErrorResponses[400],
        403: shared_1.commonErrorResponses[403],
        429: shared_1.commonErrorResponses[429],
        500: shared_1.commonErrorResponses[500],
        404: shared_1.commonErrorResponses[404],
        502: shared_1.commonErrorResponses[502],
        503: shared_1.commonErrorResponses[503],
    },
});
