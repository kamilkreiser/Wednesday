/**
 * =============================================================================
 * VC-ISSUER SERVICE — OpenAPI registrations
 * =============================================================================
 *
 * W3C Verifiable Credential issuance, management, and verification — the
 * canonical credentials surface for gateway clients. The api-gateway
 * proxies /api/credentials/* and /api/status/* and /api/presentations/*
 * to this service (see services/api-gateway/src/routes/proxy.ts).
 *
 * Note: prism's service ALSO exposes /api/credentials/* on its own port,
 * but those are gateway-shadowed (the gateway routes /api/credentials to
 * vc-issuer, not prism). prism.openapi.ts has been updated to remove the
 * shadowed registrations; only its DID surface (/api/did/*) is canonical.
 *
 * Endpoints registered (20 routes, 18 unique paths):
 *   Credentials (mounted at /api/credentials):
 *     - POST /api/credentials                 — issue
 *     - GET  /api/credentials                 — list
 *     - GET  /api/credentials/{id}            — by id
 *     - POST /api/credentials/{id}/revoke
 *     - POST /api/credentials/verify          — verify a VC
 *     - GET  /api/credentials/by-hash/{hash}  — lookup by content hash
 *   Presentations (mounted at /api/presentations):
 *     - POST /api/presentations               — create VP from VCs
 *     - POST /api/presentations/verify        — verify VP
 *     - GET  /api/presentations/{id}
 *     - POST /api/presentations/request       — request a VP
 *   Identity credentials (mounted at /api/identity-credentials):
 *     - POST /api/identity-credentials/issue
 *     - GET  /api/identity-credentials/types
 *   Revocation status lists (W3C Status List 2021, mounted at /api/status):
 *     - POST /api/status                      — create list
 *     - GET  /api/status                      — list lists
 *     - GET  /api/status/{id}
 *     - GET  /api/status/{id}/check/{index}
 *     - GET  /api/status/{id}/revoked
 *     - POST /api/status/{id}/allocate
 *     - POST /api/status/{id}/revoke
 *     - POST /api/status/{id}/unrevoke
 * =============================================================================
 */

import { z, sharedRegistry, commonErrorResponses, FX } from '@secuura/shared';
// KS-444: single source of truth for the credential-issuance enums — the same
// shared enums the runtime validator (routes/credentials.ts) enforces with
// z.nativeEnum(). Declaring them here keeps the published contract honest.
import { SecuuraCredentialType, VerificationLevel } from '@secuura/shared/vc';

// -----------------------------------------------------------------------------
// SCHEMAS — credentials
// -----------------------------------------------------------------------------

// KS-444: the runtime (routes/credentials.ts POST /) enforces
// z.nativeEnum(SecuuraCredentialType) — 6 values (DocumentCertification …
// PropertyDeed). The spec previously declared a free string (with a prose
// pointer to the enum), so a spec-legal documentType like "" earned a
// validation 400. Declare the real enum.
const SecuuraCredentialTypeEnum = z.nativeEnum(SecuuraCredentialType).openapi({
  description:
    'Secuura-defined credential type. Mirrors the SecuuraCredentialType enum ' +
    'in packages/shared/src/vc/context.ts (the values the issuance endpoint ' +
    'actually accepts).',
});

// Identity-assurance levels (uppercase) — used by /api/identity-credentials/*,
// whose runtime (routes/identity-credentials.ts) enforces exactly this set.
const VerificationLevelEnum = z.enum([
  'NONE',
  'BASIC',
  'SOCIAL',
  'STANDARD',
  'ENHANCED',
  'HIGH',
  'GOVERNMENT',
]);

// KS-444: POST /api/credentials `verificationLevel` is a DIFFERENT enum from
// the identity-assurance one above — the runtime enforces the shared
// z.nativeEnum(VerificationLevel) (lowercase: none/basic/standard/enhanced/
// government). The spec previously reused the uppercase identity enum, so the
// spec-legal "NONE" earned a validation 400. Declare the enum the runtime
// accepts.
const VcVerificationLevelEnum = z.nativeEnum(VerificationLevel).openapi({
  description:
    'Verification level recorded on the issued credential. Mirrors the ' +
    'VerificationLevel enum in packages/shared/src/vc/context.ts.',
});

const VcIssueRequestSchema = sharedRegistry.register(
  'VcIssueRequest',
  z.object({
    subjectId: z.string().optional(),
    documentId: z.string(),
    documentHash: z.string().min(1),
    documentType: SecuuraCredentialTypeEnum,
    documentTitle: z.string().min(1),
    documentDescription: z.string().optional(),
    certificationDate: z.string().optional(),
    expirationDate: z.string().optional(),
    issuerReference: z.string().optional(),
    verificationLevel: VcVerificationLevelEnum.optional(),
    metadata: z.record(z.string(), z.unknown()).optional(),
  }),
);

// W3C VC-Data-Model shape — kept permissive (.passthrough()) because
// service-level handlers accept extension fields.
const VcCredentialSchema = sharedRegistry.register(
  'VcCredential',
  z
    .object({
      '@context': z.array(z.string()),
      id: z.string(),
      type: z.array(z.string()),
      issuer: z.union([
        z.string(),
        z.object({ id: z.string() }).passthrough(),
      ]),
      issuanceDate: z.string(),
      expirationDate: z.string().optional(),
      credentialSubject: z.record(z.string(), z.unknown()),
      credentialStatus: z.record(z.string(), z.unknown()).optional(),
      proof: z.record(z.string(), z.unknown()).optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    '@context': [
      'example-@context[]',
      'example-@context[]',
    ],
    id: 'example-id',
    type: [
      'example-type[]',
      'example-type[]',
    ],
    issuer: 'example-issuer',
    issuanceDate: 'example-issuanceDate',
    credentialSubject: {},
  },
  }),
);

const VcVerifyRequestSchema = sharedRegistry.register(
  'VcVerifyRequest',
  z.object({
    credential: VcCredentialSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credential: {
      '@context': [
        'example-@context[]',
        'example-@context[]',
      ],
      id: 'example-id',
      type: [
        'example-type[]',
        'example-type[]',
      ],
      issuer: 'example-issuer',
      issuanceDate: 'example-issuanceDate',
      credentialSubject: {},
    },
  },
  }),
);

// KS-440 (response-side reconciliation; retires the historical `valid`-vs-
// `verified` drift by PUBLISHING REALITY): the runtime
// (routes/credentials.ts POST /verify) returns `{ verified, result }`, NOT the
// previously-published `{ valid, … }`. `verified` is the established contract —
// the verifier portal frontend consumes it — and `result` is the full
// CredentialVerificationResult (packages/shared/src/vc/types.ts). Verified live
// against the running stack (2026-07-13). The old `valid`-shaped schema had no
// runtime that ever produced it.
const VcVerificationResultSchema = sharedRegistry.register(
  'VcVerificationResult',
  z
    .object({
      verified: z.boolean(),
      credentialId: z.string(),
      issuer: z
        .object({
          did: z.string(),
          name: z.string().optional(),
          verified: z.boolean(),
        })
        .passthrough(),
      credential: z
        .object({
          documentHash: z.string(),
          documentType: z.string(),
          issuanceDate: z.string(),
          expirationDate: z.string().optional(),
          status: z.enum(['active', 'revoked', 'expired', 'suspended']),
        })
        .passthrough(),
      // Present only when the credential carries a Cardano anchor.
      blockchain: z
        .object({
          txHash: z.string(),
          blockHeight: z.number(),
          timestamp: z.string(),
          network: z.string(),
          verified: z.boolean(),
        })
        .passthrough()
        .optional(),
      checks: z
        .object({
          signature: z.boolean(),
          status: z.boolean(),
          expiration: z.boolean(),
          issuerDID: z.boolean(),
          blockchain: z.boolean(),
        })
        .passthrough(),
      errors: z.array(z.string()).optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    verified: true,
    credentialId: 'example-credentialId',
    issuer: {
      did: 'example-did',
      verified: true,
    },
    credential: {
      documentHash: 'example-documentHash',
      documentType: 'example-documentType',
      issuanceDate: 'example-issuanceDate',
      status: 'active',
    },
    checks: {
      signature: true,
      status: true,
      expiration: true,
      issuerDID: true,
      blockchain: true,
    },
  },
  }),
);

const VcVerifyResponseSchema = sharedRegistry.register(
  'VcVerifyResponse',
  z.object({
    verified: z.boolean(),
    result: VcVerificationResultSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    verified: true,
    result: {
      verified: true,
      credentialId: 'example-credentialId',
      issuer: {
        did: 'example-did',
        verified: true,
      },
      credential: {
        documentHash: 'example-documentHash',
        documentType: 'example-documentType',
        issuanceDate: 'example-issuanceDate',
        status: 'active',
      },
      checks: {
        signature: true,
        status: true,
        expiration: true,
        issuerDID: true,
        blockchain: true,
      },
    },
  },
  }),
);

const VcRevokeRequestSchema = sharedRegistry.register(
  'VcRevokeRequest',
  z
    .object({
      reason: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    reason: 'example-reason',
  },
  }),
);

const VcListResponseSchema = sharedRegistry.register(
  'VcListResponse',
  z.object({
    credentials: z.array(VcCredentialSchema),
    total: z.number().int().nonnegative().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credentials: [
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
    ],
  },
  }),
);

// -----------------------------------------------------------------------------
// SCHEMAS — presentations
// -----------------------------------------------------------------------------

const VpCreateRequestSchema = sharedRegistry.register(
  'VpCreateRequest',
  z.object({
    credentials: z.array(VcCredentialSchema),
    holderDID: z.string().optional(),
    challenge: z.string().optional(),
    domain: z.string().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credentials: [
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
    ],
  },
  }),
);

const VpSchema = sharedRegistry.register(
  'Vp',
  z
    .object({
      '@context': z.array(z.string()),
      id: z.string().optional(),
      type: z.array(z.string()),
      verifiableCredential: z.array(VcCredentialSchema),
      holder: z.string().optional(),
      proof: z.record(z.string(), z.unknown()).optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    '@context': [
      'example-@context[]',
      'example-@context[]',
    ],
    type: [
      'example-type[]',
      'example-type[]',
    ],
    verifiableCredential: [
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
      {
        '@context': [
          'example-@context[]',
          'example-@context[]',
        ],
        id: 'example-id',
        type: [
          'example-type[]',
          'example-type[]',
        ],
        issuer: 'example-issuer',
        issuanceDate: 'example-issuanceDate',
        credentialSubject: {},
      },
    ],
  },
  }),
);

const VpVerifyRequestSchema = sharedRegistry.register(
  'VpVerifyRequest',
  z.object({
    presentation: VpSchema,
    challenge: z.string().optional(),
    domain: z.string().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    presentation: {
      '@context': [
        'example-@context[]',
        'example-@context[]',
      ],
      type: [
        'example-type[]',
        'example-type[]',
      ],
      verifiableCredential: [
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
      ],
    },
  },
  }),
);

const VpRequestRequestSchema = sharedRegistry.register(
  'VpRequestRequest',
  z
    .object({
      // KS-430: the runtime (routes/presentations.ts) requires `credentialTypes`
      // (an array — the core payload naming which credential types the holder must
      // present; 400 "credentialTypes is required" without it) and never reads the
      // previously-declared, silently-ignored `requestedTypes`. Declare the field the
      // runtime actually requires, and drop the misnamed one, so a spec-minimal body
      // no longer earns a validation 400.
      credentialTypes: z.array(z.string()),
      challenge: z.string().optional(),
      domain: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credentialTypes: [
      'example-credentialTypes[]',
      'example-credentialTypes[]',
    ],
  },
  }),
);

// KS-440 (response-side): POST /api/presentations wraps the created VP in a
// `{ success, presentation }` envelope — the runtime (routes/presentations.ts
// POST /) never returns the flat Vp the spec previously declared. Verified live.
const VpCreateResponseSchema = sharedRegistry.register(
  'VpCreateResponse',
  z.object({
    success: z.boolean(),
    presentation: VpSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    presentation: {
      '@context': [
        'example-@context[]',
        'example-@context[]',
      ],
      type: [
        'example-type[]',
        'example-type[]',
      ],
      verifiableCredential: [
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
      ],
    },
  },
  }),
);

// KS-440 (response-side): GET /api/presentations/{id} wraps the stored VP under
// `presentation` (no `success` key on the read). Verified live.
const VpGetResponseSchema = sharedRegistry.register(
  'VpGetResponse',
  z.object({
    presentation: VpSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    presentation: {
      '@context': [
        'example-@context[]',
        'example-@context[]',
      ],
      type: [
        'example-type[]',
        'example-type[]',
      ],
      verifiableCredential: [
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
        {
          '@context': [
            'example-@context[]',
            'example-@context[]',
          ],
          id: 'example-id',
          type: [
            'example-type[]',
            'example-type[]',
          ],
          issuer: 'example-issuer',
          issuanceDate: 'example-issuanceDate',
          credentialSubject: {},
        },
      ],
    },
  },
  }),
);

// KS-440 (response-side; same `valid`→`verified` reality publish as
// /credentials/verify): the runtime (routes/presentations.ts POST /verify)
// returns `{ verified, presentationId?, holder?, credentialResults[], checks }`.
// `presentationId`/`holder` are omitted when the presentation carries neither.
// Verified live.
const VpVerifyResponseSchema = sharedRegistry.register(
  'VpVerifyResponse',
  z.object({
    verified: z.boolean(),
    presentationId: z.string().optional(),
    holder: z.string().optional(),
    credentialResults: z.array(
      z
        .object({
          credentialIndex: z.number().int().nonnegative(),
          credentialId: z.string().optional(),
          verified: z.boolean(),
          issuer: z
            .object({
              did: z.string(),
              name: z.string().optional(),
              verified: z.boolean(),
            })
            .passthrough()
            .optional(),
          status: z.string().optional(),
          errors: z.array(z.string()).optional(),
        })
        .passthrough(),
    ),
    checks: z
      .object({
        allCredentialsValid: z.boolean(),
        presentationProofValid: z.boolean(),
        challengeValid: z.boolean(),
        domainValid: z.boolean(),
      })
      .passthrough(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    verified: true,
    credentialResults: [
      {
        credentialIndex: 0,
        verified: true,
      },
      {
        credentialIndex: 0,
        verified: true,
      },
    ],
    checks: {
      allCredentialsValid: true,
      presentationProofValid: true,
      challengeValid: true,
      domainValid: true,
    },
  },
  }),
);

// -----------------------------------------------------------------------------
// SCHEMAS — identity credentials
// -----------------------------------------------------------------------------

const IdentityCredentialIssueRequestSchema = sharedRegistry.register(
  'IdentityCredentialIssueRequest',
  z.object({
    subjectDid: z.string().min(1),
    assuranceLevel: VerificationLevelEnum,
    verificationMethods: z.array(z.string()).optional(),
    provider: z.string().optional(),
    region: z.string().optional(),
    expirationDate: z.string().optional(),
    metadata: z.record(z.string(), z.unknown()).optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    subjectDid: 'example-subjectDid',
    assuranceLevel: 'NONE',
  },
  }),
);

const IdentityCredentialTypesResponseSchema = sharedRegistry.register(
  'IdentityCredentialTypesResponse',
  z.object({
    types: z.array(
      z.object({
        assuranceLevel: VerificationLevelEnum,
        credentialType: z.string(),
      }),
    ),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    types: [
      {
        assuranceLevel: 'NONE',
        credentialType: 'example-credentialType',
      },
      {
        assuranceLevel: 'NONE',
        credentialType: 'example-credentialType',
      },
    ],
  },
  }),
);

// -----------------------------------------------------------------------------
// SCHEMAS — status lists
// -----------------------------------------------------------------------------

// KS-144: the list response items are `{ id, url }`; capacity/createdAt are only
// present on richer detail responses — relax them to optional.
const StatusListSchema = sharedRegistry.register(
  'StatusList',
  z
    .object({
      id: z.string(),
      url: z.string().optional(),
      purpose: z.enum(['revocation', 'suspension']).optional(),
      capacity: z.number().int().positive().optional(),
      allocated: z.number().int().nonnegative().optional(),
      revoked: z.number().int().nonnegative().optional(),
      createdAt: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
  },
  }),
);

const StatusListCreateRequestSchema = sharedRegistry.register(
  'StatusListCreateRequest',
  z.object({
    // KS-430: the runtime (routes/status.ts POST /) requires a caller-supplied `id`
    // — it names the list and is rejected with 400 "id is required" when absent — but
    // the spec omitted it. Declare it required so a spec-minimal body reaches the
    // handler (which then 409s only on a genuine duplicate id).
    // KS-444: the runtime also rejects an EMPTY id (`!id`), so declare minLength 1 —
    // a spec-legal "" must not earn a 400.
    id: z.string().min(1),
    purpose: z.enum(['revocation', 'suspension']).optional(),
    capacity: z.number().int().positive().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
  },
  }),
);

const StatusListEntryAllocateRequestSchema = sharedRegistry.register(
  'StatusListEntryAllocateRequest',
  z
    .object({
      // KS-430: the runtime (routes/status.ts POST /:id/allocate) requires
      // `credentialId` — the credential the allocated index is bound to; 400
      // "credentialId is required" without it. It was marked optional here, so a
      // spec-minimal body earned a validation 400. Make it required to match.
      // KS-444: the runtime also rejects an EMPTY credentialId (`!credentialId`),
      // so declare minLength 1 — a spec-legal "" must not earn a 400.
      credentialId: z.string().min(1),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credentialId: 'example-credentialId',
  },
  }),
);

// KS-440 (response-side): the runtime (routes/status.ts POST /:id/allocate)
// returns `{ statusListId, credentialId, index, allocatedAt }` — the index key
// is `index`, not the previously-published `statusListIndex`, and it echoes the
// bound `credentialId` + allocation timestamp. Verified live.
const StatusListEntryAllocateResponseSchema = sharedRegistry.register(
  'StatusListEntryAllocateResponse',
  z.object({
    statusListId: z.string(),
    credentialId: z.string(),
    index: z.number().int().nonnegative(),
    allocatedAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    credentialId: 'example-credentialId',
    index: 0,
    allocatedAt: FX.timestamps.createdAt,
  },
  }),
);

// KS-440 (response-side): GET /api/status/{id} returns the full W3C
// StatusList2021 credential wrapped under `credential` — NOT the StatusList
// summary object the spec previously declared (StatusListSchema stays the shape
// of the LIST items on GET /api/status). Verified live.
const StatusListCredentialResponseSchema = sharedRegistry.register(
  'StatusListCredentialResponse',
  z.object({
    credential: VcCredentialSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credential: {
      '@context': [
        'example-@context[]',
        'example-@context[]',
      ],
      id: 'https://api.example.com/v1/resource',
      type: [
        'example-type[]',
        'example-type[]',
      ],
      issuer: 'example-issuer',
      issuanceDate: FX.timestamps.createdAt,
      credentialSubject: {},
    },
  },
  }),
);

// KS-440 (response-side): POST /api/status returns the created list's
// identifiers `{ statusListId, purpose, createdAt }` — not the StatusList
// summary. Verified live.
const StatusListCreateResponseSchema = sharedRegistry.register(
  'StatusListCreateResponse',
  z.object({
    statusListId: z.string(),
    purpose: z.string(),
    createdAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    purpose: 'example-purpose',
    createdAt: FX.timestamps.createdAt,
  },
  }),
);

// KS-440 (response-side): GET /api/status/{id}/revoked returns
// `{ statusListId, revokedIndexes, totalRevoked }` — the index array key is
// `revokedIndexes`, not the previously-published `indices`. Verified live.
const StatusRevokedListResponseSchema = sharedRegistry.register(
  'StatusRevokedListResponse',
  z.object({
    statusListId: z.string(),
    revokedIndexes: z.array(z.number().int().nonnegative()),
    totalRevoked: z.number().int().nonnegative(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    revokedIndexes: [
      0,
      0,
    ],
    totalRevoked: 0,
  },
  }),
);

// KS-440 (response-side): POST /api/status/{id}/revoke returns the per-credential
// revocation record `{ statusListId, credentialId, revoked, reason?, revokedAt }`
// — NOT the `{ success }` VcSuccess envelope the spec previously declared.
// Verified live.
const StatusListEntryRevokeResponseSchema = sharedRegistry.register(
  'StatusListEntryRevokeResponse',
  z.object({
    statusListId: z.string(),
    credentialId: z.string(),
    revoked: z.boolean(),
    reason: z.string().optional(),
    revokedAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    credentialId: 'example-credentialId',
    revoked: true,
    revokedAt: FX.timestamps.createdAt,
  },
  }),
);

// KS-440 (response-side): POST /api/status/{id}/unrevoke returns
// `{ statusListId, credentialId, revoked, unrevokedAt }` — again not the
// `{ success }` VcSuccess envelope. Verified live.
const StatusListEntryUnrevokeResponseSchema = sharedRegistry.register(
  'StatusListEntryUnrevokeResponse',
  z.object({
    statusListId: z.string(),
    credentialId: z.string(),
    revoked: z.boolean(),
    unrevokedAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    credentialId: 'example-credentialId',
    revoked: true,
    unrevokedAt: FX.timestamps.createdAt,
  },
  }),
);

const StatusListEntryRevokeRequestSchema = sharedRegistry.register(
  'StatusListEntryRevokeRequest',
  z.object({
    // KS-430: the runtime (routes/status.ts POST /:id/revoke and /:id/unrevoke)
    // revokes/unrevokes BY `credentialId`, which it requires (400 "credentialId is
    // required" without it) — it never reads `index`. The spec declared `index`
    // required and omitted `credentialId`, so a spec-minimal `{ index }` body earned a
    // validation 400. Declare the field the runtime requires, and loosen the
    // runtime-ignored `index` to optional (the handler harmlessly ignores it either
    // way) so both describe the same request contract.
    // KS-444: the runtime also rejects an EMPTY credentialId (`!credentialId`),
    // so declare minLength 1 — a spec-legal "" must not earn a 400.
    credentialId: z.string().min(1),
    index: z.number().int().nonnegative().optional(),
    reason: z.string().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    credentialId: 'example-credentialId',
  },
  }),
);

// KS-440 (response-side): GET /api/status/{id}/check/{index} returns
// `{ statusListId, index, isRevoked, checkedAt }` — the revocation flag key is
// `isRevoked`, not the previously-published `revoked`. Verified live.
const StatusCheckResponseSchema = sharedRegistry.register(
  'StatusCheckResponse',
  z.object({
    statusListId: z.string(),
    index: z.number().int().nonnegative(),
    isRevoked: z.boolean(),
    checkedAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    statusListId: '1',
    index: 0,
    isRevoked: true,
    checkedAt: FX.timestamps.createdAt,
  },
  }),
);

const VcSuccessSchema = sharedRegistry.register(
  'VcSuccess',
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
// ROUTES — credentials
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/credentials',
  tags: ['VC'],
  summary: 'Issue a Secuura credential against a document',
  description:
    'Mints a W3C VC pinned to a document hash + type. Status-list entry ' +
    'is allocated automatically so the credential can be revoked later.',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: the runtime rejects a body-less request (required fields), so the
    // body itself must be declared required — otherwise a spec-legal request
    // with no body earns a validation 400.
    body: {
      content: { 'application/json': { schema: VcIssueRequestSchema } },
      required: true,
    },
  },
  responses: {
    201: {
      description: 'Credential issued',
      content: { 'application/json': { schema: VcCredentialSchema } },
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
  path: '/api/credentials',
  tags: ['VC'],
  summary: 'List credentials issued by/for the caller',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Credential list',
      content: { 'application/json': { schema: VcListResponseSchema } },
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
  path: '/api/credentials/{id}',
  tags: ['VC'],
  summary: 'Get a credential by id',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Credential',
      content: { 'application/json': { schema: VcCredentialSchema } },
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

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/credentials/{id}/revoke',
  tags: ['VC'],
  summary: 'Revoke a credential',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: { content: { 'application/json': { schema: VcRevokeRequestSchema } } },
  },
  responses: {
    200: {
      description: 'Credential revoked (status-list entry flipped)',
      content: { 'application/json': { schema: VcSuccessSchema } },
    },
    401: commonErrorResponses[401],
    404: commonErrorResponses[404],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/credentials/verify',
  // KS-442: public by product decision — tokenless verification.
  security: [],
  tags: ['VC'],
  summary: 'Verify a Secuura credential (signature + status + expiry)',
  request: {
    // KS-444: `credential` is required, so the body itself is required too.
    body: {
      content: { 'application/json': { schema: VcVerifyRequestSchema } },
      required: true,
    },
  },
  responses: {
    200: {
      description: 'Verification result',
      content: { 'application/json': { schema: VcVerifyResponseSchema } },
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

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/credentials/by-hash/{hash}',
  tags: ['VC'],
  summary: 'Lookup a credential by document content hash',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({
      hash: z.string().regex(/^[a-f0-9]{64}$/i).openapi({ example: FX.document.contentHash }),
    }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Credential',
      content: { 'application/json': { schema: VcCredentialSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'No credential matches that hash' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — presentations
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/presentations',
  tags: ['VP'],
  summary: 'Create a Verifiable Presentation from a set of credentials',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: the runtime requires `credentials`, so a body-less request 400s —
    // declare the body required (Schemathesis' positive body-less probe was
    // spec-legal before this).
    body: {
      content: { 'application/json': { schema: VpCreateRequestSchema } },
      required: true,
    },
  },
  responses: {
    201: {
      description: 'VP created',
      content: { 'application/json': { schema: VpCreateResponseSchema } },
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
  method: 'post',
  path: '/api/presentations/verify',
  // KS-442: public by product decision — tokenless verification.
  security: [],
  tags: ['VP'],
  summary: 'Verify a Verifiable Presentation',
  request: {
    // KS-444: `presentation` is required, so the body itself is required too.
    body: {
      content: { 'application/json': { schema: VpVerifyRequestSchema } },
      required: true,
    },
  },
  responses: {
    200: {
      description: 'Verification result',
      content: { 'application/json': { schema: VpVerifyResponseSchema } },
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

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/presentations/{id}',
  tags: ['VP'],
  summary: 'Get a stored presentation by id',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Presentation',
      content: { 'application/json': { schema: VpGetResponseSchema } },
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

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/presentations/request',
  tags: ['VP'],
  summary: 'Request a presentation (verifier → holder challenge)',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: `credentialTypes` is required, so the body itself is required too.
    body: {
      content: { 'application/json': { schema: VpRequestRequestSchema } },
      required: true,
    },
  },
  responses: {
    // KS-475 (§6): the runtime answers 201 with {success, request:{…}}
    // (routes/presentations.ts res.status(201)) — the previous 200
    // {requestId, challenge} was never emitted in either status or shape.
    201: {
      description: 'Presentation request issued',
      content: {
        'application/json': {
          schema: z.object({
            success: z.literal(true),
            request: z
              .object({
                id: z.string(),
                type: z.literal('PresentationRequest'),
                credentialTypes: z.array(z.string()),
                requiredFields: z.array(z.string()),
                purpose: z.string(),
                challenge: z.string(),
                domain: z.string(),
                createdAt: z.string(),
                expiresAt: z.string(),
              })
              .passthrough(),
          }),
        },
      },
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

// -----------------------------------------------------------------------------
// ROUTES — identity credentials
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/identity-credentials/issue',
  tags: ['VC', 'Identity'],
  summary: 'Issue an identity assurance credential',
  description:
    'Issues a Secuura identity-assurance VC at the requested LoA. ' +
    'verificationMethods + provider + region get embedded in ' +
    'credentialSubject for downstream verifiers.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: { 'application/json': { schema: IdentityCredentialIssueRequestSchema } },
    },
  },
  responses: {
    // KS-476: the runtime wraps the credential ({credential, message} —
    // routes/identity-credentials.ts) — publishing the true shape as the op
    // becomes gateway-routable for the first time.
    201: {
      description: 'Identity credential issued',
      content: {
        'application/json': {
          schema: z.object({
            credential: VcCredentialSchema,
            message: z.string(),
          }),
        },
      },
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
  path: '/api/identity-credentials/types',
  security: [],
  tags: ['VC', 'Identity'],
  summary: 'List supported identity credential types per assurance level',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Type catalog',
      content: { 'application/json': { schema: IdentityCredentialTypesResponseSchema } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — status lists (W3C Status List 2021)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/status',
  tags: ['Status List'],
  summary: 'Create a new revocation/suspension status list',
  security: [{ bearerAuth: [] }],
  request: {
    // KS-444: `id` is required, so the body itself is required too.
    body: {
      content: { 'application/json': { schema: StatusListCreateRequestSchema } },
      required: true,
    },
  },
  responses: {
    201: {
      description: 'Status list created',
      content: { 'application/json': { schema: StatusListCreateResponseSchema } },
    },
    401: commonErrorResponses[401],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    // KS-475 (§6): the runtime 409s on a duplicate status-list id
    // (routes/status.ts AppError 409) — previously undocumented.
    409: { ...commonErrorResponses[409], description: 'Status list with this ID already exists' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/status',
  tags: ['Status List'],
  summary: 'List status lists',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Status lists',
      content: {
        'application/json': {
          schema: z
            .object({ statusLists: z.array(StatusListSchema), total: z.number().optional() })
            .passthrough(),
        },
      },
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
  path: '/api/status/{id}',
  security: [{ bearerAuth: [] }],
  tags: ['Status List'],
  summary: 'Get a status list',
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Status list credential (W3C StatusList2021)',
      content: { 'application/json': { schema: StatusListCredentialResponseSchema } },
    },
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/status/{id}/check/{index}',
  security: [{ bearerAuth: [] }],
  tags: ['Status List'],
  summary: 'Check whether a specific status-list index is revoked',
  description:
    'Public endpoint — verifiers walk this to check VC revocation status ' +
    'per W3C Status List 2021.',
  request: {
    params: z.object({
      id: z.string(),
      // KS-423: pin the emitted type (coerce+nonnegative renders [integer, "null"]).
      // KS-1287: coerce parses null as 0, so the lib reads the param as nullable and publishes required: false - pin it.
      index: z.coerce.number().int().nonnegative().openapi({ type: 'integer', minimum: 0, param: { required: true } }),
    }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Status (revoked or not)',
      content: { 'application/json': { schema: StatusCheckResponseSchema } },
    },
    404: { ...commonErrorResponses[404], description: 'List not found' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/status/{id}/revoked',
  security: [{ bearerAuth: [] }],
  tags: ['Status List'],
  summary: 'List all revoked indices in a status list',
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Revoked indices',
      content: {
        'application/json': { schema: StatusRevokedListResponseSchema },
      },
    },
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/status/{id}/allocate',
  tags: ['Status List'],
  summary: 'Allocate a new status-list index (issue-time hook)',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: {
      content: { 'application/json': { schema: StatusListEntryAllocateRequestSchema } },
      // KS-444: `credentialId` is required, so the body itself is required too.
      required: true,
    },
  },
  responses: {
    200: {
      description: 'Allocated index',
      content: {
        'application/json': { schema: StatusListEntryAllocateResponseSchema },
      },
    },
    400: { ...commonErrorResponses[400], description: 'List capacity exhausted' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/status/{id}/revoke',
  tags: ['Status List'],
  summary: 'Mark an index as revoked',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: {
      content: { 'application/json': { schema: StatusListEntryRevokeRequestSchema } },
      // KS-444: `credentialId` is required, so the body itself is required too.
      required: true,
    },
  },
  responses: {
    200: {
      description: 'Index revoked',
      content: { 'application/json': { schema: StatusListEntryRevokeResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Validation error or index already revoked' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/status/{id}/unrevoke',
  tags: ['Status List'],
  summary: 'Reverse a revocation (admin)',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: {
      content: { 'application/json': { schema: StatusListEntryRevokeRequestSchema } },
      // KS-444: `credentialId` is required, so the body itself is required too.
      required: true,
    },
  },
  responses: {
    200: {
      description: 'Index unrevoked',
      content: { 'application/json': { schema: StatusListEntryUnrevokeResponseSchema } },
    },
    401: commonErrorResponses[401],
    400: commonErrorResponses[400],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});
