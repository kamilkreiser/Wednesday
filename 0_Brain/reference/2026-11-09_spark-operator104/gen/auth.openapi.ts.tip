// KS-796 QA2-F4: LoginRequestSchema / WalletVerifyRequestSchema /
// OAuthAuthorizeRequestSchema are EXPORTED so the published wire contract can be
// asserted rather than described.
//
// ⚠ NOTHING IMPORTS THEM YET, and the reason is a defect, not an oversight. This
// module CANNOT be imported from a test today:
//
//   TypeError: MFA_CODE_ACCEPTED.optional(...).openapi is not a function   (:152)
//
// `packages/shared/src/openapi/registry.ts:245` states the rule — a consumer MUST
// import `z` from '@secuura/shared' so `extendZodWithOpenApi` lands on the same
// prototype — and `services/passwordLoginGate.ts:55` imports `z` from 'zod'
// directly, so `MFA_CODE_ACCEPTED` is built on an UNEXTENDED zod. The spec
// generator's single CJS resolution happens to unify the two; a vitest run does
// not. Filed separately; the fix is one import line with a blast radius across
// every schema that file publishes, so it is not being slipped into a follow-up.
//
// Until then the QA2-F4 guard asserts the GENERATED yaml instead — which is the
// artefact a client generates from, so it is the thing that would ship wrong.
// This also means the gate's canary still stands: a module-scope throw in this
// file leaves the auth suite green, because it is in no test's import graph.
/**
 * =============================================================================
 * AUTH SERVICE — OpenAPI registrations (Track 2 stage 3)
 * =============================================================================
 *
 * Primary public auth surface:
 *   - /api/auth/{login,logout,refresh,register,forgot-password,reset-password}
 *   - /api/users/me (GET + PATCH) + change-password
 *   - /api/sessions (list + revoke-by-id)
 *   - /api/auth/wallet/{challenge,verify}
 *   - /api/auth/mfa/verify
 *   - /api/oauth/{authorize,token,revoke,scopes,apps,apps/{id},apps/{id}/rotate-secret}
 *     — OAuth 2.0 Authorization Code Flow with PKCE (RFC 6749 + RFC 7636 + RFC 7009)
 *
 * Schemas mirror frontend/shared/src/schemas/auth.ts where they overlap
 * (LoginResponse, MeResponse, AuthUser). Until services can import from a
 * single shared schema source, keep these in lockstep.
 *
 * KS-712 (2026-08-29) — the auth half of the deferral below is now registered:
 * the /api/auth/mfa surface, wallet /authenticate + /status/{walletAddress} +
 * /link + /unlink, the /api/auth/social/* flows, and /api/users/me/mfa/*.
 * These were routed but absent from the published spec, so BOTH Akto and
 * Schemathesis were blind to them — an endpoint outside the spec is scanned by
 * neither. ("The whole /api/auth/mfa surface" reads as six operations only
 * because the sixth, /api/auth/mfa/verify, was already declared before this
 * change — it is the pre-auth one, and a reader will go looking for it.)
 *
 * This IS a runtime change at the edge — it is NOT documentation only. The
 * api-gateway derives two enforcement gates from this spec
 * (services/api-gateway/src/index.ts:965-1008, via specRouteMap.ts):
 *   - Method gate: an undeclared path is unmatched and falls straight through to
 *     the proxy. A declared one 405s at the edge on any method it does not
 *     declare.
 *   - Auth gate: `security: [{ bearerAuth: [] }]` makes the gateway 401 BEFORE
 *     proxying. For 9 of the 11 authed operations that is a no-op in outcome.
 *     For wallet /link and /unlink it is not — those carry NO service-side auth,
 *     so an unauthenticated call that previously reached the handler and got a
 *     400 is now refused at the edge. Beneficial, a partial mitigation of
 *     KS-720, and a change.
 * Measured on one commit by restarting only the gateway (it bind-mounts the
 * spec, so a restart publishes it): served paths 289 -> 303, and preflight's
 * spec-auth leg FAIL (3 operations) -> PASS (315/315), with no code change at
 * all. The declaration is the enforcement.
 *
 * Endpoints still not registered (deferred to follow-up commits):
 *   - auth: /verify-email
 *   - users: /admin/*, /me/verification, /verification/:id/review
 *   - sessions: DELETE / (revoke-all)
 *   - health (operational only, not API surface)
 *   - the remaining ~157 routed-but-undocumented operations measured on KS-712
 * =============================================================================
 */

// KS-256: FX/MOCK_JWT are the canonical published-example fixture set.
// These examples previously carried their literals inline (a live,
// loginable ISSUER_ADMIN address plus a hand-copied mock JWT), which is
// how the spec drifted into three example-email conventions. Drawing them
// from one place means the generated examples cannot drift from these.
// Enforced by `npm run check:openapi` -> check-spec-examples (E1, E5).
import {
  z, sharedRegistry, commonErrorResponses, successEnvelope, rateLimit, sla,
  FX, MOCK_JWT, mask,
} from '@secuura/shared';

// Type-only import: used by the SOCIAL_PROVIDER_NAMES drift guard below. Erased at
// compile time, so it pulls no provider constructor into spec generation.
import type { SocialProviderName } from './providers/social/types';
// KS-781 N-4 — the second factor's accepted shape is imported, never retyped.
// This file carried the regex as a hand-typed literal in two places, and the
// KS-781 fix round was about to add a third. The KS-622 lockstep guard reads
// the GENERATED yaml with `spec.includes(pattern)`, so it is occurrence-blind:
// one correct occurrence satisfies it while another drifts. Importing removes
// the class rather than testing for it. (Noted on KS-622; widening that guard
// is not this PR's job.)
import { MFA_CODE_ACCEPTED } from './services/passwordLoginGate';
// KS-1210: the OAuth app request schemas publish the SAME closed scope list the service enforces
// (routes/oauth.ts: z.enum(AVAILABLE_SCOPES) on create and update). It was `z.array(z.string())` here,
// so the spec called `{"scopes": [""]}` valid while the service answered 400 invalid_enum_value, which
// Schemathesis reported as positive_data_acceptance (KS-1408 sweep, 2026-10-05). Imported, not retyped.
import { AVAILABLE_SCOPES } from './services/oauth';

// -----------------------------------------------------------------------------
// SHARED SCHEMAS
// -----------------------------------------------------------------------------

// Mirrors frontend/shared/src/schemas/auth.ts AuthUserSchema.
const AuthUserSchema = sharedRegistry.register(
  'AuthUser',
  z
    .object({
      id: z.string(),
      email: z.string().email(),
      role: z.string(),
      verificationLevel: z.string().optional(),
      displayName: z.string().nullable().optional(),
      firstName: z.string().nullable().optional(),
      lastName: z.string().nullable().optional(),
      emailVerified: z.boolean().optional(),
      mfaEnabled: z.boolean().optional(),
      tenantId: z.string().nullable().optional(),
      tenantSlug: z.string().nullable().optional(),
    })
    .openapi({
      description:
        'Authenticated user record returned by /login + /users/me. Some fields are ' +
        'optional because different endpoints populate slightly different subsets.',
      example: {
        id: FX.issuer.id,
        email: FX.issuer.email,
        role: FX.issuer.role,
        verificationLevel: FX.issuer.verificationLevel,
        displayName: FX.issuer.displayName,
        firstName: FX.issuer.firstName,
        lastName: FX.issuer.lastName,
        emailVerified: true,
        mfaEnabled: false,
        tenantId: FX.tenant.id,
        tenantSlug: FX.tenant.slug,
      },
    }),
);

export const LoginRequestSchema = sharedRegistry.register(
  'LoginRequest',
  z
    .object({
      email: z.string().email(),
      // KS-3 tightening: mirror the runtime Zod (auth.ts:56) — empty string
      // is rejected with 400 at runtime so the spec must reflect it. Any
      // non-empty value is accepted; the actual password-validation
      // happens server-side.
      password: z.string().min(1),
      // Mirrors the runtime Zod schema in services/auth/src/routes/auth.ts.
      // `browser` clients omit refreshToken from the response body (set as
      // httpOnly cookie); `native` clients (mobile/desktop/CLI/automation)
      // request the body field by setting clientType: 'native'. `api` is
      // a single-session variant: each /login revokes prior 'api' sessions
      // for the same user (KS-43 — stolen-token protection for headless
      // callers). Browser and native are multi-session with LRU eviction.
      clientType: z.enum(['browser', 'native', 'api']).optional(),
      deviceId: z.string().optional(),
      // KS-283: a TOTP code is 6 decimal digits. `.length(6)` (UTF-16 code
      // units) diverged from the spec's code-point count, so astral-char
      // 6-code-point strings 400'd at runtime (positive_data_acceptance). The
      // numeric pattern mirrors the runtime loginSchema exactly and is
      // digit-only, so spec code-points == runtime code-units. Emits
      // `pattern: "^[0-9]{6}$"`.
      // KS-622: 6 digits = TOTP, 8 alphanumeric = backup code. Login is the
      // only redemption path now that /api/auth/mfa/verify is retired.
      // KS-781 P3-4: same union as /api/oauth/authorize, from the one shared
      // definition — the spec is the contract both doors publish.
      mfaCode: MFA_CODE_ACCEPTED.optional().openapi({ description: 'Second factor: 6 digits (TOTP) or an 8-character backup code. An empty string counts as absent, so a form-backed client that always submits the field is accepted (KS-781 P3-4).' }),
    })
    .openapi({
      example: {
        email: FX.issuer.email,
        // KS-165: placeholder, NOT the seeded demo password. The actual
        // demo password is documented in Blockchain/CLAUDE.md (seed table)
        // and supplied by Schemathesis via the persona-auth hooks
        // (ENABLE_HOOKS=1), so this example never reaches a live login. A
        // `*123` literal here re-introduces pen-test F-05 (caught by
        // scripts/check-no-default-passwords.sh).
        //
        // KS-256: '<your-password>' — REVERTED to this on Peter's instruction
        // (2026-07-20), having briefly been '<password>'.
        //
        // Credential placeholders are derived from the field name so a reader is
        // told which secret goes where. Passwords take the '<your-…>' form —
        // something the caller knows and types — so the change-password body
        // reads '<your-current-password>' and '<your-new-password>', still
        // distinct from each other. Tokens and keys keep their own name
        // ('<accessToken>'), because the caller cannot invent one and must have
        // obtained it from an earlier call.
        //
        // Contains no `*123` literal, so the F-05 property above is unchanged.
        password: '<your-password>',
        clientType: 'browser',
      },
    }),
);

// Mirrors frontend/shared/src/schemas/auth.ts LoginResponseSchema.
// refreshToken is OPTIONAL because the /login handler omits it from the
// body when clientType='browser' (set as httpOnly cookie instead).
const LoginResponseSchema = sharedRegistry.register(
  'LoginResponse',
  z
    .object({
      success: z.literal(true),
      data: z.object({
        accessToken: z.string().min(1),
        refreshToken: z.string().optional(),
        expiresIn: z.number().int().positive(),
        tokenType: z.literal('Bearer'),
        user: AuthUserSchema,
      }),
    })
    .openapi({
      example: {
        success: true,
        data: {
          // Signature segment is the inert `.MOCK_SIGNATURE` marker, so
          // rule E2 can tell this apart from a leaked live token.
          accessToken: MOCK_JWT,
          expiresIn: 3600,
          tokenType: 'Bearer',
          user: {
            id: FX.issuer.id,
            email: FX.issuer.email,
            role: FX.issuer.role,
            verificationLevel: FX.issuer.verificationLevel,
            displayName: FX.issuer.displayName,
            firstName: FX.issuer.firstName,
            lastName: FX.issuer.lastName,
            emailVerified: true,
            mfaEnabled: false,
            tenantId: FX.tenant.id,
            tenantSlug: FX.tenant.slug,
          },
        },
      },
    }),
);

const MeResponseSchema = sharedRegistry.register(
  'MeResponse',
  z.object({
    success: z.literal(true).optional(),
    data: AuthUserSchema,
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    data: {
      id: '00000000-0000-4000-8000-0000000000ff',
      email: FX.issuer.email,
      role: FX.issuer.role,
      verificationLevel: FX.issuer.verificationLevel,
      displayName: FX.issuer.displayName,
      firstName: FX.issuer.firstName,
      lastName: FX.issuer.lastName,
      emailVerified: true,
      mfaEnabled: false,
      tenantId: FX.tenant.id,
      tenantSlug: FX.tenant.slug,
    },
  },
  }),
);

// KS-440 (response-side): PATCH /api/users/me does NOT return the full AuthUser —
// the handler (routes/users.ts patch '/me') echoes only the profile fields it
// updates: id, email, first/last/displayName, phoneNumber, phoneVerified,
// updatedAt. It notably omits `role` (which MeResponseSchema/AuthUser mark
// required), so publishing MeResponseSchema for the PATCH made every real 200
// violate the response schema ("role is a required property"). Publish the real
// narrower shape returned by the update handler instead. GET /api/users/me
// still returns the full AuthUser and keeps MeResponseSchema.
const UpdateProfileResponseSchema = sharedRegistry.register(
  'UpdateProfileResponse',
  z
    .object({
      success: z.literal(true),
      data: z
        .object({
          id: z.string(),
          email: z.string().email(),
          firstName: z.string().nullable().optional(),
          lastName: z.string().nullable().optional(),
          displayName: z.string().nullable().optional(),
          phoneNumber: z.string().nullable().optional(),
          phoneVerified: z.boolean().optional(),
          updatedAt: z.string().optional(),
        })
        .passthrough(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      id: '00000000-0000-4000-8000-0000000000ff',
      email: FX.issuer.email,
    },
  },
  }),
);

const RegisterRequestSchema = sharedRegistry.register(
  'RegisterRequest',
  z
    .object({
      email: z.string().email(),
      // KS-3 tightening: runtime requires min 8 (auth.ts:78). Anything
      // shorter is rejected with 400 — schemathesis would have flagged
      // this as 'API rejected schema-compliant request'.
      password: z.string().min(8),
      // Runtime: name/firstName/lastName all z.string().min(1).optional()
      // (auth.ts:79-81). Empty strings are rejected; the spec must reflect.
      name: z.string().min(1).optional(),
      firstName: z.string().min(1).optional(),
      lastName: z.string().min(1).optional(),
    })
    .openapi({
      example: {
        // KS-256: the registrant is the FX holder — registration is how
        // that account comes into being, so the fixture set stays coherent
        // with the share / delegate / verify examples downstream.
        email: FX.holder.email,
        // ⚠ MASKED — the earlier reasoning here was WRONG and is recorded so
        // nobody re-argues it. This published a concrete passphrase, on the
        // grounds that it "illustrates the min-8 rule". But Schemathesis's
        // Examples phase EXECUTES request examples: it registered the account,
        // after which the published spec documented a credential pair that
        // authenticated (account ff5038bf-…, role OWNER, created 2026-08-05
        // 16:51Z by the first suite run). A published value that BECOMES real
        // is the same defect as a leaked one.
        //
        // Guard rule E9 now fails the build on any request example carrying
        // both an email-shaped and a password-shaped field, so this cannot
        // return here or on another endpoint.
        password: mask('password') ?? '<your-password>',
        firstName: FX.holder.firstName,
        lastName: FX.holder.lastName,
      },
    }),
);

const ForgotPasswordRequestSchema = sharedRegistry.register(
  'ForgotPasswordRequest',
  z.object({
    email: z.string().email(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    email: FX.issuer.email,
  },
  }),
);

const ResetPasswordRequestSchema = sharedRegistry.register(
  'ResetPasswordRequest',
  z.object({
    token: z.string(),
    // KS-255: the runtime field is `password` (auth.ts resetPasswordSchema) —
    // advertising `newPassword` made every spec-compliant reset 400 with
    // "password: Required" (verified live 2026-06-12).
    password: z.string().min(8),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    token: 'example-token',
    password: '<your-password>',
  },
  }),
);

const ChangePasswordRequestSchema = sharedRegistry.register(
  'ChangePasswordRequest',
  // KS-444: publish the runtime's real constraints (changePasswordSchema in
  // routes/users.ts) — the spec advertised bare strings, so a spec-legal
  // empty-string request 400'd. An empty currentPassword can never verify and
  // newPassword min 8 is the actual password policy (mirrors the KS-255
  // ResetPasswordRequest precedent above; runtime is authoritative per KS-430).
  z.object({
    currentPassword: z.string().min(1),
    newPassword: z.string().min(8),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    currentPassword: '<your-current-password>',
    newPassword: '<your-new-password>',
  },
  }),
);

const WalletChallengeRequestSchema = sharedRegistry.register(
  'WalletChallengeRequest',
  z.object({
    walletAddress: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    walletAddress: FX.wallet.address,
  },
  }),
);

const WalletChallengeResponseSchema = sharedRegistry.register(
  'WalletChallengeResponse',
  z.object({
    challengeId: z.string(),
    nonce: z.string(),
    challenge: z.string(),
    expiresAt: z.string().datetime(),
    message: z.string(),
    format: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    challengeId: '00000000-0000-4000-8000-0000000000ff',
    nonce: '00000000-0000-4000-8000-0000000000ff',
    challenge: 'example-challenge',
    expiresAt: FX.timestamps.createdAt,
    message: 'example-message',
    format: 'example-format',
  },
  }),
);

// Mirrors verifySignatureSchema (services/auth/src/routes/wallet.ts:96-105).
// This schema serves BOTH /api/auth/wallet/verify and /api/auth/wallet/authenticate
// because they are literally the same handler (wallet.ts:337-338), so correcting
// it corrects the pre-existing /verify declaration too.
//
// The previous shape — `challengeId: z.string()`, required, any string — was wrong
// in two directions at once. It REJECTED the payload the issuer portal actually
// sends ({walletAddress, signature, nonce}, frontend/issuer/src/services/api.ts:429),
// and it generated non-uuid challengeIds for the sweep that the handler can only
// ever 400, which is part of what KS-712 filed under "precondition-dependent".
export const WalletVerifyRequestSchema = sharedRegistry.register(
  'WalletVerifyRequest',
  z
    .object({
      challengeId: z.string().uuid().optional(),
      nonce: z
        .string()
        .optional()
        .openapi({ description: 'Accepted alias for challengeId' }),
      walletAddress: z.string().min(1),
      signature: z.string().min(1),
      key: z
        .string()
        .optional()
        .openapi({ description: 'CIP-8 COSE_Key public key (hex)' }),
      // KS-796 (KS-781 door 3): a wallet signature proves control of the
      // WALLET. It says nothing about a second factor, and a wallet account can
      // have one — it is created with mfaEnabled false, but the holder may
      // switch it on later through /api/users/me/mfa/*, which needs no account
      // linking. Empty counts as absent, because a form-backed client posts its
      // whole state and sends "" for an account with no second factor (the
      // shape that returned 400 to every non-MFA user on door 1 — KS-781 N-1).
      // KS-781 P3-4 (carried into door 3 on the rebase): the SHARED definition,
      // not a third hand-typed copy of the same union. This site originally
      // re-typed `z.union([z.string().regex(MFA_CODE_PATTERN), z.literal('')])`
      // — the exact shape #812 factored out precisely because two copies of it
      // had already drifted between login and authorize.
      mfaCode: MFA_CODE_ACCEPTED
        .optional()
        .openapi({
          description:
            'Second factor: 6 digits (TOTP) or an 8-character backup code. REQUIRED when the ' +
            'account has MFA enabled — omitting it returns 403 MFA_REQUIRED (KS-796). An empty ' +
            'string counts as absent.',
        }),
    })
    .openapi({
      description:
        'At least one of challengeId or nonce is required — enforced by .refine() in the ' +
        'handler and not expressible in JSON Schema, so it is stated here. 400 otherwise.',
      // KS-256: generated example (synthesised, masked). Guarded by
      // `npm run check:openapi` -> check-spec-examples (E1-E7).
      // Custody rebase (KS-256): RELOCATED here from the pre-rebase
      // WalletVerifyRequest body. develop rewrote this schema (challengeId now
      // `.uuid().optional()`, plus nonce and key), so git aligned the example
      // against WalletAuthResponse instead — dropping it would have silently
      // lost a piece of #568. Still format-true, and now load-bearing: the
      // fixture is a valid v4 uuid and challengeId is `.uuid()` on develop.
      example: {
        challengeId: FX.wallet.challengeId,
        signature: '<signature>',
        walletAddress: FX.wallet.address,
      },
    }),
);

// The wallet verify/authenticate 200 is NOT the LoginResponse envelope. The handler
// spreads the token pair at the TOP level and returns no `success` key at all
// (wallet.ts:319-330), so LoginResponse — which requires `success` + a `data`
// wrapper — could never match it on either route.
const WalletAuthResponseSchema = sharedRegistry.register(
  'WalletAuthResponse',
  z.object({
    accessToken: z.string().min(1),
    refreshToken: z.string().min(1),
    expiresIn: z.number().int().positive(),
    token: z.string().min(1).openapi({ description: 'Alias of accessToken' }),
    user: z.object({
      id: z.string(),
      email: z.string(),
      role: z.string(),
      verificationLevel: z.string(),
      walletAddress: z.string().nullable().optional(),
    }),
    sessionId: z.string(),
  }),
);

const MfaVerifyRequestSchema = sharedRegistry.register(
  'MfaVerifyRequest',
  z.object({
    userId: z.string(),
    code: z
      .string()
      .openapi({
        description: 'TOTP code (6 digits) OR backup code (8 chars, alphanumeric)',
      }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    userId: FX.issuer.id,
    code: '000000',
  },
  }),
);

// KS-144: match the real session shape — `userId` is not returned; the fields
// are `ipAddress`/`lastActivityAt`/`isCurrent` (not `ip`/`lastSeenAt`).
const SessionItemSchema = sharedRegistry.register(
  'SessionItem',
  z
    .object({
      id: z.string(),
      userId: z.string().optional(),
      ipAddress: z.string().nullable().optional(),
      userAgent: z.string().nullable().optional(),
      createdAt: z.string(),
      lastActivityAt: z.string().nullable().optional(),
      expiresAt: z.string().nullable().optional(),
      isCurrent: z.boolean().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    createdAt: 'example-createdAt',
  },
  }),
);

// KS-144: real response is the canonical envelope `{ success, data: [...] }`.
const SessionListResponseSchema = sharedRegistry.register(
  'SessionListResponse',
  successEnvelope(z.array(SessionItemSchema)).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: [
      {
        id: 'example-id',
        createdAt: FX.timestamps.createdAt,
      },
      {
        id: 'example-id',
        createdAt: FX.timestamps.createdAt,
      },
    ],
  },
  }),
);

const AuthSuccessSchema = sharedRegistry.register(
  'AuthSuccess',
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
// ROUTES — /api/auth (core)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/login',
  security: [],
  tags: ['Auth'],
  summary: 'Email + password login',
  description:
    'Returns access + refresh tokens. When clientType=browser, refreshToken ' +
    'is set as an httpOnly cookie and omitted from the response body. ' +
    'clientType=browser and clientType=native allow concurrent sessions per ' +
    'user (LRU eviction at cap); clientType=api is single-session — each ' +
    'new login revokes prior api sessions for the same user (KS-43).',
  ...rateLimit('login'),
  ...sla('write'),
  request: {
    body: {
      // KS-283: an absent body is not a valid positive case — the runtime 400s
      // on missing email/password. Marking the body required stops Schemathesis
      // generating empty-body "positive" requests that then 400.
      required: true,
      content: {
        'application/json': { schema: LoginRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Login successful',
      content: { 'application/json': { schema: LoginResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Invalid credentials' },
    403: { ...commonErrorResponses[403], description: 'MFA required (provide mfaCode in next request)' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/logout',
  tags: ['Auth'],
  summary: 'Logout (invalidates current session)',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Logout successful',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
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
  path: '/api/auth/refresh',
  // KS-561: public pre-auth op — the credential IS the refresh token
  // (httpOnly cookie for web, body for native). Declaring bearerAuth here
  // made the gateway's spec-auth gate 401 every cookie-only silent refresh.
  security: [],
  tags: ['Auth'],
  summary: 'Exchange refresh token for new access token',
  description:
    'For web clients, the refresh token is read from the httpOnly cookie ' +
    'set by /login; for mobile/desktop/api clients, it is read from the ' +
    'request body as `refreshToken`.',
  ...rateLimit('refresh'),
  ...sla('read'),
  request: {
    body: {
      content: {
        'application/json': {
          schema: z
            .object({ refreshToken: z.string().optional() })
            .passthrough(),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'New access token issued',
      content: { 'application/json': { schema: LoginResponseSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Refresh token missing or expired' },
    400: commonErrorResponses[400],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/register',
  security: [],
  tags: ['Auth'],
  summary: 'Register a new account',
  description:
    'Unauthenticated. Tenant context is derived by the gateway from the ' +
    'request hostname (the gateway strips client-sent x-tenant-* and ' +
    're-injects the resolved value). Direct service hits land on the ' +
    'no-tenant path.',
  ...rateLimit('register'),
  ...sla('write'),
  request: {
    body: {
      // KS-283: required so an absent body is a schema violation (negative),
      // not a "positive" case — the runtime 400s on missing email/password.
      required: true,
      content: {
        'application/json': { schema: RegisterRequestSchema },
      },
    },
  },
  responses: {
    201: {
      description: 'Registration successful — session created',
      content: { 'application/json': { schema: LoginResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Malformed payload — missing/invalid fields or bad JSON' },
    // KS-255: weak password and the forbidden `role` field raise ValidationError,
    // which the auth errorHandler maps to 422 (verified live 2026-06-12) — not 400.
    422: { ...commonErrorResponses[422], description: 'Weak password, or client-supplied `role` field (not permitted)' },
    409: { ...commonErrorResponses[409], description: 'Email already registered' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/forgot-password',
  security: [],
  tags: ['Auth'],
  summary: 'Request a password reset email',
  description:
    'Always returns 200 to prevent email enumeration. If an account exists, ' +
    'a reset link is sent via the configured email provider (ACS Email in dev).',
  ...rateLimit('forgot_password'),
  ...sla('write'),
  request: {
    body: {
      // KS-283: required so an absent body is a schema violation (negative),
      // not a "positive" case — the runtime 400s on the missing email field.
      required: true,
      content: {
        'application/json': { schema: ForgotPasswordRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Always — to prevent enumeration',
      content: { 'application/json': { schema: AuthSuccessSchema } },
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
  method: 'post',
  path: '/api/auth/reset-password',
  security: [],
  tags: ['Auth'],
  summary: 'Reset password using emailed token',
  request: {
    body: {
      content: {
        'application/json': { schema: ResetPasswordRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Password reset successful',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Malformed payload, or reset token expired' },
    // KS-255: weak password raises ValidationError -> 422 (checked before the
    // token lookup, so it can occur with any token value).
    422: { ...commonErrorResponses[422], description: 'New password too weak' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: { ...commonErrorResponses[404], description: 'Reset token invalid or already used' },
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/users
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/users/me',
  tags: ['Users'],
  summary: 'Get the authenticated user',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Current user',
      content: { 'application/json': { schema: MeResponseSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// F-06 (audit 2026-05-15): /api/auth/me alias of /api/users/me. Same handler,
// same response shape — registered separately so OpenAPI consumers see both
// surfaces. Issuer/admin/verifier portals + e2e-v2 tier1 auth.api.spec hit
// /api/auth/me; the canonical path stays /api/users/me.
sharedRegistry.registerPath({
  method: 'get',
  path: '/api/auth/me',
  tags: ['Auth'],
  summary: 'Get the authenticated user (alias of /api/users/me)',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Current user',
      content: { 'application/json': { schema: MeResponseSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// KS-69: email → userId resolver, used by cert-issuance flows.
const UserLookupResponseSchema = sharedRegistry.register(
  'UserLookupResponse',
  z.object({
    success: z.literal(true),
    data: z.object({
      userId: z.string().uuid(),
      organizationId: z.string().uuid().optional(),
      tenantId: z.string().uuid().optional(),
      displayName: z.string().optional(),
      verificationLevel: z.string(),
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    data: {
      userId: FX.issuer.id,
      verificationLevel: 'example-verificationLevel',
    },
  },
  }),
);

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/users/lookup',
  tags: ['Users'],
  summary: 'Resolve an email to a userId within the caller\'s tenant (KS-69)',
  description:
    'Cert-issuance bridge — SSD and other issuer flows often have the ' +
    'recipient\'s email but not the platform userId required by ' +
    'POST /api/certifications/issue. This endpoint resolves the email ' +
    'when the user exists in the caller\'s tenant. Returns 404 (not ' +
    '200-empty) so positive existence isn\'t trivially readable from ' +
    'response shape — the users:read scope or one of the cert-issuance ' +
    'roles (ISSUER_ADMIN / ORG_ADMIN / SYSTEM_ADMIN / SUPER_ADMIN) is ' +
    'the actual gate.',
  security: [{ bearerAuth: [] }],
  request: {
    query: z.object({
      email: z.string().email().min(3).max(320).openapi({
        description: 'Email address to resolve, normalised to lower-case before lookup.',
        // KS-256: was a third persona existing nowhere else in the set.
        example: FX.holder.email,
      }),
    }),
  },
  responses: {
    200: {
      description: 'User found in the caller\'s tenant',
      content: { 'application/json': { schema: UserLookupResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Missing or malformed email query parameter' },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks both an allowed role AND the users:read scope',
    },
    404: {
      ...commonErrorResponses[404],
      description: 'No user with that email in the caller\'s tenant (or in a different tenant — indistinguishable on purpose)',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/users/me',
  tags: ['Users'],
  summary: 'Update the authenticated user profile',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': {
          // KS-430 (Kam 2026-07-11: "no null", runtime is authoritative): the runtime
          // updateProfileSchema (routes/users.ts) is non-nullable and .strict(), so the
          // spec's .nullable() + .passthrough() were both spec-legal shapes the runtime
          // 400s. Drop nullable (names can't be cleared to null) and align to strict
          // (unknown keys rejected); add the runtime's phoneNumber field.
          // KS-475 (§2): when present the runtime requires non-empty trimmed
          // values (updateProfileSchema .trim().min(1) + max caps) — publish
          // the same bounds. Fields stay optional (partial update).
          schema: z
            .object({
              firstName: z.string().min(1).max(100).optional(),
              lastName: z.string().min(1).max(100).optional(),
              displayName: z.string().min(1).max(200).optional(),
              phoneNumber: z.string().optional(),
            })
            .strict(),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'Updated user',
      content: { 'application/json': { schema: UpdateProfileResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
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
  path: '/api/users/me/change-password',
  tags: ['Users'],
  summary: 'Change own password (requires current password)',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': { schema: ChangePasswordRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Password changed',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Wrong current password or new password too weak' },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/users/admin/* (KS-486 remediation #3)
// These admin, role-assigning operations were live-but-unpublished — outside the
// contract, so Schemathesis + Akto never reached them (the condition that hid the
// KS-486 case-variant privesc). Published here so the suites cover them. All
// require an admin role (the handlers' ADMIN_ROLES gate); a wrong/absent role is
// 403, unauthenticated is 401. Role/status/verificationLevel are published as
// permissive strings — the runtime is authoritative (it canonicalises accepted
// values and 400s the rest), and over-tightening these into enums would make
// spec-legal alias inputs the runtime accepts read as violations.
// -----------------------------------------------------------------------------

const AdminUserRowSchema = z
  .object({
    id: z.string(),
    email: z.string(),
    firstName: z.string().nullable().optional(),
    lastName: z.string().nullable().optional(),
    displayName: z.string().nullable().optional(),
    role: z.string(),
    status: z.string(),
    verificationLevel: z.string(),
    organizationId: z.string().nullable().optional(),
    lastLoginAt: z.string().nullable().optional(),
    createdAt: z.string().nullable().optional(),
  })
  .openapi('AdminUserRow');

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/users/admin/list',
  tags: ['Users'],
  summary: 'Admin: list users (own tenant for tenant admins; cross-tenant for platform admins)',
  security: [{ bearerAuth: [] }],
  request: {
    query: z.object({
      limit: z.coerce.number().int().min(1).max(200).optional().openapi({ description: 'Page size (default 50, max 200)' }),
      offset: z.coerce.number().int().min(0).optional().openapi({ description: 'Row offset (default 0)' }),
      search: z.string().optional().openapi({ description: 'Free-text filter on name / email' }),
      role: z.string().optional().openapi({ description: 'Filter by role' }),
    }),
  },
  responses: {
    200: {
      description: 'User list',
      content: {
        'application/json': {
          schema: successEnvelope(
            z.object({
              users: z.array(AdminUserRowSchema),
              total: z.number(),
              limit: z.number(),
              offset: z.number(),
            }),
          ),
        },
      },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: { ...commonErrorResponses[403], description: 'Admin role required, or tenant context missing for a tenant-scoped admin' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/users/admin/organizations',
  tags: ['Users'],
  summary: 'Admin: list organisations (own tenant for tenant admins; cross-tenant for platform admins)',
  security: [{ bearerAuth: [] }],
  responses: {
    200: {
      description: 'Organisation list',
      content: {
        'application/json': {
          schema: successEnvelope(
            z.object({
              organizations: z.array(z.record(z.string(), z.unknown())),
              total: z.number(),
            }),
          ),
        },
      },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: { ...commonErrorResponses[403], description: 'Admin role required, or tenant context missing for a tenant-scoped admin' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/users/admin/create',
  tags: ['Users'],
  summary: 'Admin: create a user',
  description:
    'Creates a pre-verified user. A tenant-scoped admin creates in its own tenant and may not assign a ' +
    'platform-admin role (403). `role` accepts any canonical UserRole or a case/alias variant and is folded ' +
    'to the canonical role; an unknown role is 400.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': {
          schema: z
            .object({
              email: z.string().email(),
              password: z.string().min(1),
              firstName: z.string().optional(),
              lastName: z.string().optional(),
              role: z.string().optional().openapi({ description: 'Canonical UserRole or case/alias variant; defaults to OWNER' }),
              verificationLevel: z.string().optional().openapi({ description: 'Verification level; defaults to BASIC' }),
            })
            .openapi('AdminCreateUserRequest'),
        },
      },
    },
  },
  responses: {
    201: {
      description: 'User created',
      content: {
        'application/json': {
          schema: successEnvelope(
            z.object({
              id: z.string(),
              email: z.string(),
              displayName: z.string(),
              role: z.string(),
              verificationLevel: z.string(),
              status: z.string(),
            }),
          ),
        },
      },
    },
    400: { ...commonErrorResponses[400], description: 'Missing email/password, or an unknown role' },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: { ...commonErrorResponses[403], description: 'Admin role required; a tenant admin may not assign a platform-admin role' },
    409: { ...commonErrorResponses[409], description: 'A user with this email already exists' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/users/admin/{id}',
  tags: ['Users'],
  summary: 'Admin: update a user (role, status, profile, organisation)',
  description:
    'Updates safe fields on a user. A tenant-scoped admin may only touch a user in its own tenant (else 404) ' +
    'and may not grant a platform-admin role (403); no caller may change its own role through this route. ' +
    '`role`/`status` accept canonical values or case/alias variants and are folded to the canonical value; ' +
    'an unknown value is 400. A SUSPENDED/DEACTIVATED status revokes the target’s active sessions.',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({
      // KS-1013: the runtime rejects a non-UUID id with 400 before the lookup,
      // so publish the format it actually enforces (runtime-is-truth). Was a
      // bare `z.string()`, which declared every string a legal id while a
      // malformed one raised 22P02 in Postgres and surfaced as a raw 500.
      // Matches the three sibling `{id}` params in this file.
      id: z.string().uuid().openapi({ description: 'Target user id', example: FX.holder.id }),
    }),
    body: {
      content: {
        'application/json': {
          schema: z
            .object({
              // KS-486 sweep follow-up: the runtime folds case/alias variants
              // but 400s an EMPTY string ("Invalid role"/"Invalid status") —
              // publish the real min-length so a spec-legal body is
              // runtime-legal (runtime-is-truth; these fields were first
              // published 2026-07-29, no external consumers).
              status: z.string().min(1).optional(),
              role: z.string().min(1).optional(),
              verificationLevel: z.string().optional(),
              displayName: z.string().optional(),
              firstName: z.string().optional(),
              lastName: z.string().optional(),
              organizationId: z.string().nullable().optional().openapi({ description: 'Organisation id; explicit null clears the assignment' }),
            })
            .openapi('AdminUpdateUserRequest'),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'User updated',
      content: {
        'application/json': {
          schema: successEnvelope(
            z.object({
              id: z.string(),
              email: z.string(),
              role: z.string(),
              status: z.string(),
              verificationLevel: z.string(),
            }),
          ),
        },
      },
    },
    400: { ...commonErrorResponses[400], description: 'A malformed (non-UUID) id, no valid fields, or an unknown role/status/organizationId' },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: { ...commonErrorResponses[403], description: 'Admin role required; may not grant a platform-admin role or change your own role' },
    404: { ...commonErrorResponses[404], description: 'User not found (or a foreign-tenant target for a tenant admin)' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/sessions
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/sessions',
  tags: ['Sessions'],
  summary: 'List active sessions for the authenticated user',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Active sessions',
      content: { 'application/json': { schema: SessionListResponseSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
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
  path: '/api/sessions/{id}',
  tags: ['Sessions'],
  summary: 'Revoke a specific session',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({
      id: z.string().openapi({ description: 'Session id to revoke' }),
    }),
  },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Session revoked',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    404: { ...commonErrorResponses[404], description: 'Session not found or already revoked' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/auth/wallet (Cardano CIP-8 challenge/response)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/wallet/challenge',
  security: [],
  tags: ['Auth', 'Wallet'],
  summary: 'Issue a CIP-8 challenge for wallet authentication',
  description:
    'Step 1 of wallet auth: request a challenge string for the given wallet ' +
    'address. The wallet signs it (CIP-8) and returns the signature to /verify.',
  request: {
    body: {
      content: {
        'application/json': { schema: WalletChallengeRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Challenge issued',
      content: { 'application/json': { schema: WalletChallengeResponseSchema } },
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
  method: 'post',
  path: '/api/auth/wallet/verify',
  security: [],
  tags: ['Auth', 'Wallet'],
  summary: 'Verify a wallet signature against a previously issued challenge',
  description:
    'Step 2 of wallet auth. Returns the standard login envelope (access + ' +
    'refresh tokens) on success. Aliased as /api/auth/wallet/authenticate. ' +
    'KS-796: the signature proves control of the wallet; before a credential is ' +
    'issued the ACCOUNT it resolves to is gated the same way POST /api/auth/login ' +
    'gates one — account lockout, account status, and the second factor. A ' +
    'SUSPENDED or DEACTIVATED account is refused 401 and issues nothing.',
  request: {
    body: {
      content: {
        'application/json': { schema: WalletVerifyRequestSchema },
      },
    },
  },
  responses: {
    200: {
      description: 'Wallet auth successful',
      content: { 'application/json': { schema: WalletAuthResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Signature did not verify' },
    403: { ...commonErrorResponses[403], description: 'MFA_REQUIRED — the account has a second factor and no usable mfaCode was supplied (KS-796)' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — /api/auth/mfa
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/mfa/verify',
  security: [],
  deprecated: true,
  tags: ['Auth', 'MFA'],
  summary: 'RETIRED — always returns 410 Gone',
  description:
    'RETIRED (KS-622). This endpoint redeemed a backup code with no proof of ' +
    'factor one: it took `userId` from the request body, carried no ' +
    '`authenticate()`, and the login account-lockout could not engage on it ' +
    'because it never saw an email. It now always returns **410 Gone** and ' +
    'performs no lookup and no redemption. Send the TOTP or backup code as ' +
    '`mfaCode` on `POST /api/auth/login` instead, which verifies the password ' +
    'first. Kept in the contract rather than removed so the retirement is ' +
    'discoverable to any existing caller.',
  ...rateLimit('mfa'),
  ...sla('write'),
  request: {
    body: {
      content: {
        'application/json': { schema: MfaVerifyRequestSchema },
      },
    },
  },
  responses: {
    410: {
      description:
        'Gone — this endpoint is retired. Send the code as `mfaCode` on POST /api/auth/login.',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    // KS-622 (#745 ask 4): 410 is not the ONLY status this route can produce, and the first
    // narrowing of this block said it was. Found by the pre-merge Schemathesis sweep's
    // status_code_conformance check ("Received: 400, Documented: 410, 415, 429, 500, 502, 503"),
    // not by reading, and pinned by ks622-retired-route-contract.test.ts.
    //
    // TWO app-level middlewares answer 400 before the retirement handler runs, both MEASURED on
    // the running stack rather than reasoned about (KS-622 review, F-11/F-12):
    //   · `express.json()` on a malformed body -> errorHandler turns `entity.parse.failed` into
    //     400 INVALID_JSON;
    //   · `rejectNulBytes()` (KS-471), mounted immediately after it, on a U+0000 anywhere in the
    //     body -> 400 VALIDATION_ERROR "Must not contain a NUL (U+0000) byte".
    //
    // An earlier version of this comment said "a ZodError lands on the same 400". That is FALSE:
    // MfaVerifyRequestSchema is only registered here and referenced as this operation's
    // requestBody — `.parse()` is called on it nowhere (control: setupSchema.parse and
    // disableSchema.parse do exist in routes/mfa.ts, so the absence is real). The conclusion the
    // sentence drew happened to be true for a different reason nobody had enumerated.
    //
    // 401/404/200 are deliberately NOT restored: those were the live handler's and really are
    // unreachable now.
    400: commonErrorResponses[400],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// SCHEMAS — KS-712 auth surface (MFA / wallet / social)
// -----------------------------------------------------------------------------

const MfaStatusResponseSchema = sharedRegistry.register(
  'MfaStatusResponse',
  successEnvelope(
    z.object({
      mfaEnabled: z.boolean(),
      // null when no TOTP secret is stored; 'totp' is the only implemented type.
      mfaType: z.literal('totp').nullable(),
      backupCodesRemaining: z.number().int().nonnegative(),
    }),
  ),
);

const MfaSetupStartResponseSchema = sharedRegistry.register(
  'MfaSetupStartResponse',
  successEnvelope(
    z.object({
      secret: z.string().openapi({ description: 'TOTP shared secret (base32)' }),
      otpAuthUri: z.string().openapi({ description: 'otpauth:// URI for QR rendering' }),
      expiresAt: z.string().datetime().openapi({ description: 'Pending setup expiry — 10 minutes' }),
    }),
  ),
);

// 6 digits exactly — mirrors setupSchema in services/auth/src/routes/mfa.ts.
const MfaTotpCodeRequestSchema = sharedRegistry.register(
  'MfaTotpCodeRequest',
  z.object({
    totpCode: z.string().length(6).regex(/^\d+$/),
  }),
);

const MfaSetupVerifyResponseSchema = sharedRegistry.register(
  'MfaSetupVerifyResponse',
  successEnvelope(
    z.object({
      mfaEnabled: z.literal(true),
      backupCodes: z.array(z.string()).openapi({ description: 'Shown once — not retrievable later' }),
      message: z.string(),
    }),
  ),
);

const MfaDisableRequestSchema = sharedRegistry.register(
  'MfaDisableRequest',
  z.object({
    // KS-732 (#872 review, note 1): optional, and it MUST track disableSchema in
    // routes/mfa.ts — these are two separate declarations of one contract, and
    // they had already drifted: relaxing the handler's copy left this one still
    // publishing `required: [password]`. ks732-mfa-disable-proof pins them
    // together so the next divergence reddens instead of shipping.
    password: z.string().min(1).optional(),
    totpCode: z.string().length(6).regex(/^\d+$/).optional(),
    // KS-732: additive. Accepted for accounts with no password (wallet /
    // social), which cannot prove possession any other way.
    backupCode: z.string().regex(/^[A-Za-z0-9]{8}$/).optional(),
  }),
);

const MfaBackupCodesResponseSchema = sharedRegistry.register(
  'MfaBackupCodesResponse',
  successEnvelope(
    z.object({
      backupCodes: z.array(z.string()),
      message: z.string(),
    }),
  ),
);

// The handler returns two shapes on 200 depending on registration: `{ exists: true }` and `{ exists: false, message }`.
// KS-1009: it no longer returns the account's id, role or creation time to an unauthenticated caller.
const WalletStatusResponseSchema = sharedRegistry.register(
  'WalletStatusResponse',
  z
    .object({
      exists: z.boolean(),
      message: z.string().optional(),
    })
    .passthrough(),
);

// key is REQUIRED — verifyCIP8Signature has no fallback path (audit A-02).
const WalletLinkRequestSchema = sharedRegistry.register(
  'WalletLinkRequest',
  z.object({
    walletAddress: z.string().min(1),
    signature: z.string().min(1),
    challengeId: z.string().uuid(),
    key: z.string().min(1).openapi({ description: 'CIP-8 COSE_Key public key (hex)' }),
  }),
);

const WalletLinkResponseSchema = sharedRegistry.register(
  'WalletLinkResponse',
  z.object({
    success: z.boolean(),
    message: z.string(),
    walletAddress: z.string(),
  }),
);

const SocialProvidersResponseSchema = sharedRegistry.register(
  'SocialProvidersResponse',
  z.object({
    providers: z.array(z.string()).openapi({
      description:
        'Only providers enabled in this deployment. A provider registered in the factory but ' +
        'lacking credentials is filtered out here (see KS-714 re: Apple).',
    }),
  }),
);

const SocialAuthUrlResponseSchema = sharedRegistry.register(
  'SocialAuthUrlResponse',
  z.object({
    authUrl: z.string().url(),
    state: z.string().uuid(),
  }),
);

// Source of truth: the SocialProviderName union in ./providers/social/types.ts,
// which keys PROVIDER_MAP in ./providers/social/provider-factory.ts. Held as a
// literal here so generating the spec does not import the provider constructors;
// the two conditional types below fail the BUILD if the list and the union ever
// drift apart — in either direction, which a plain `satisfies` would not catch.
//
// Declaring it as an enum rather than z.string() is what lets the sweep generate
// values that can succeed: every random string is schema-compliant against
// z.string() and guaranteed-400 at the handler, which manufactured two of the
// failures KS-712 reported as deployment-config.
const SOCIAL_PROVIDER_NAMES = [
  'google',
  'linkedin',
  'facebook',
  'apple',
  'github',
  'microsoft_personal',
] as const;
type _ProviderListIsSubsetOfUnion =
  Exclude<(typeof SOCIAL_PROVIDER_NAMES)[number], SocialProviderName> extends never ? true : never;
type _ProviderUnionIsSubsetOfList =
  Exclude<SocialProviderName, (typeof SOCIAL_PROVIDER_NAMES)[number]> extends never ? true : never;
const _socialProviderListMatchesUnion: [_ProviderListIsSubsetOfUnion, _ProviderUnionIsSubsetOfList] = [
  true,
  true,
];
void _socialProviderListMatchesUnion;

const SocialProviderNameSchema = z.enum(SOCIAL_PROVIDER_NAMES).openapi({ example: 'google' });

const SocialLinkRequestSchema = sharedRegistry.register(
  'SocialLinkRequest',
  z.object({
    provider: SocialProviderNameSchema,
    code: z.string().min(1),
  }),
);

// The social callback 200 is NOT the LoginResponse envelope either: the handler
// spreads generateTokenPair() alongside `success` at the top level
// (services/auth/src/routes/auth.ts:899-902), and generateTokenPair yields only
// {accessToken, refreshToken, expiresIn} (services/auth/src/services/jwt.ts:208-215).
// So there is no `data` wrapper, no `tokenType` and no `user`. Latent only while
// providers are unconfigured — the first deployment with real OAuth credentials
// would fail response_schema_conformance against the spec, not against the app.
const SocialCallbackResponseSchema = sharedRegistry.register(
  'SocialCallbackResponse',
  z.object({
    success: z.literal(true),
    accessToken: z.string().min(1),
    refreshToken: z.string().min(1),
    expiresIn: z.number().int().positive(),
  }),
);

const SocialLinkResponseSchema = sharedRegistry.register(
  'SocialLinkResponse',
  z.object({
    success: z.boolean(),
    provider: z.string(),
    linked: z.boolean(),
  }),
);

const UserMfaEnableResponseSchema = sharedRegistry.register(
  'UserMfaEnableResponse',
  successEnvelope(
    z.object({
      secret: z.string(),
      qrCode: z.string(),
      message: z.string(),
    }),
  ),
);

const UserMfaVerifyResponseSchema = sharedRegistry.register(
  'UserMfaVerifyResponse',
  successEnvelope(
    z.object({
      message: z.string(),
      backupCodes: z.array(z.string()),
      verificationLevel: z.string(),
    }),
  ),
);

// 6-digit code — the /api/users/me/mfa/* trio validates inline, not via zod.
const UserMfaCodeRequestSchema = sharedRegistry.register(
  'UserMfaCodeRequest',
  z.object({
    code: z.string().length(6).regex(/^\d+$/),
  }),
);

// -----------------------------------------------------------------------------
// ROUTES — KS-712: /api/auth/mfa (the four previously undocumented operations)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/auth/mfa/status',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'MFA'],
  summary: "Read the caller's own MFA state",
  description: 'Returns whether MFA is enabled, its type, and how many backup codes remain.',
  ...rateLimit('mfa'),
  ...sla('read'),
  responses: {
    200: {
      description: 'MFA status',
      content: { 'application/json': { schema: MfaStatusResponseSchema } },
    },
    400: commonErrorResponses[400],
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
  path: '/api/auth/mfa/setup/start',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'MFA'],
  summary: 'Begin TOTP enrolment — issue a secret and otpauth URI',
  description:
    'Step 1 of enrolment. Stores a pending setup valid for 10 minutes. Returns 409 when ' +
    'MFA is already enabled. Complete with /api/auth/mfa/setup/verify.',
  ...rateLimit('mfa'),
  ...sla('write'),
  responses: {
    200: {
      description: 'Pending setup created',
      content: { 'application/json': { schema: MfaSetupStartResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    409: { ...commonErrorResponses[409], description: 'MFA is already enabled' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/mfa/setup/verify',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'MFA'],
  summary: 'Complete TOTP enrolment and receive backup codes',
  description:
    'Step 2 of enrolment. On success MFA is enabled and backup codes are returned ONCE — ' +
    'they are stored hashed and cannot be retrieved again.',
  ...rateLimit('mfa'),
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: MfaTotpCodeRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'MFA enabled',
      content: { 'application/json': { schema: MfaSetupVerifyResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Invalid code, or no pending setup' },
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
  path: '/api/auth/mfa/disable',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'MFA'],
  summary: 'Disable MFA for the caller',
  description:
    'Accepts {password?, totpCode?, backupCode?} and disables MFA for the bearer. ' +
    'Disabling MFA costs a proof of possession: an account WITH a password must supply a ' +
    'correct one, and an account WITHOUT a password (wallet / social — password_hash is ' +
    'nullable and getOrCreateWalletUser sets none) must supply a valid totpCode or a valid ' +
    'backupCode. A supplied totpCode is always verified, so a wrong code fails rather than ' +
    'being ignored. No path disables MFA on a bearer token alone. ' +
    '(KS-732: this description previously documented the opposite — the password was ' +
    'required by the schema and never verified, and the totpCode check was conditional on ' +
    'the code being present, so any bearer disabled MFA with {"password":"anything"}. ' +
    'That is fixed; the narration is removed with it, because a contract describing a ' +
    'defect is as wrong as one describing an absent check.)',
  ...rateLimit('mfa'),
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: MfaDisableRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'MFA disabled',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    400: commonErrorResponses[400],
    401: {
      ...commonErrorResponses[401],
      description:
        'Missing or invalid bearer token; a WRONG password on an account that has one; ' +
        'a password omitted by an account that has one; an invalid totpCode when one was ' +
        'supplied; or no valid totpCode/backupCode on an account with no password. ' +
        '(KS-732: this response previously documented "NOT returned for a wrong password: ' +
        'the password is never checked" — which was true, and was the defect. It is the ' +
        'check that now runs.)',
    },
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
  path: '/api/auth/mfa/backup-codes/regenerate',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'MFA'],
  summary: 'Regenerate backup codes, invalidating the previous set',
  description: 'Requires a valid TOTP code. Returns 10 new codes ONCE; the old codes stop working.',
  ...rateLimit('mfa'),
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: MfaTotpCodeRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'New backup codes issued',
      content: { 'application/json': { schema: MfaBackupCodesResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'MFA is not enabled' },
    401: { ...commonErrorResponses[401], description: 'Invalid TOTP code' },
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — KS-712: /api/auth/wallet (authenticate / status / link / unlink)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/wallet/authenticate',
  security: [],
  tags: ['Auth', 'Wallet'],
  summary: 'Verify a wallet signature (alias of /api/auth/wallet/verify)',
  description:
    'Same handler as /api/auth/wallet/verify — both are mounted to handleWalletVerify. ' +
    'Documented separately because it is a distinct routed operation.',
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: WalletVerifyRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'Wallet auth successful',
      content: { 'application/json': { schema: WalletAuthResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Signature did not verify' },
    403: { ...commonErrorResponses[403], description: 'MFA_REQUIRED — the account has a second factor and no usable mfaCode was supplied (KS-796)' },
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/auth/wallet/status/{walletAddress}',
  security: [],
  tags: ['Auth', 'Wallet'],
  summary: 'Check whether a wallet address is registered',
  description:
    'Public read (security: [] — unauthenticated by design). The response says only whether ' +
    'the address is registered: {exists:true} for a registered one, {exists:false, message} ' +
    'otherwise. It never carries an account attribute (no user id, role or creation time). ' +
    'Registration itself remains an existence signal for a public address, which sign-in needs.',
  ...sla('read'),
  request: {
    params: z.object({
      walletAddress: z.string().openapi({ example: 'addr_test1qrjjw7rr' }),
    }),
  },
  responses: {
    200: {
      description: 'Registration status',
      content: { 'application/json': { schema: WalletStatusResponseSchema } },
    },
    400: commonErrorResponses[400],
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
  path: '/api/auth/wallet/link',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'Wallet'],
  summary: "Link a wallet to the caller's account",
  description:
    'Consumes a challenge issued by /api/auth/wallet/challenge. The CIP-8 public key is ' +
    'required — signature verification has no fallback path without it (audit A-02).',
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: WalletLinkRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'Wallet linked',
      content: { 'application/json': { schema: WalletLinkResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: { ...commonErrorResponses[404], description: 'Challenge not found or expired' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'delete',
  path: '/api/auth/wallet/unlink',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'Wallet'],
  summary: "Unlink the wallet from the caller's account",
  description: 'Returns 400 when no wallet is linked.',
  ...sla('write'),
  responses: {
    200: {
      description: 'Wallet unlinked',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'No wallet linked to this account' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — KS-712: /api/auth/social (OAuth sign-in flows)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/auth/social/providers',
  security: [],
  tags: ['Auth', 'Social'],
  summary: 'List the social providers enabled in this deployment',
  ...sla('read'),
  responses: {
    200: {
      description: 'Enabled providers',
      content: { 'application/json': { schema: SocialProvidersResponseSchema } },
    },
    400: commonErrorResponses[400],
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
  method: 'get',
  path: '/api/auth/social/{provider}',
  security: [],
  tags: ['Auth', 'Social'],
  summary: 'Begin a social sign-in flow',
  description:
    'Returns the provider authorisation URL and a state nonce. The nonce is PERSISTED ' +
    'server-side (KS-722), single-use, bound to this provider, and expires in 10 minutes; ' +
    'the callback refuses anything it cannot match. 400 when the provider is unknown OR is ' +
    'registered but not enabled in this deployment.',
  ...sla('read'),
  request: {
    params: z.object({
      provider: SocialProviderNameSchema,
    }),
  },
  responses: {
    200: {
      description: 'Authorisation URL issued',
      content: { 'application/json': { schema: SocialAuthUrlResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Unknown or not-enabled provider' },
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
  method: 'get',
  path: '/api/auth/social/{provider}/callback',
  security: [],
  tags: ['Auth', 'Social'],
  summary: 'Social OAuth callback — exchange the code and issue tokens',
  description:
    'Consumes the external identity assertion. Resolves the user by provider id. When no such ' +
    'identity is on file it may fall back to an email match, but ONLY for a provider whose ' +
    'emailVerified is derived from the provider own verification signal AND is true (KS-795). ' +
    'Otherwise the existing account is left untouched and the request is refused. ' +
    'Every refusal that depends on the ACCOUNT returns one indistinguishable shape ' +
    '(403 SOCIAL_SIGN_IN_REFUSED, KS-795 F-6) so an unauthenticated caller cannot tell a ' +
    'healthy account from a disabled one, or either from an address with no account; ' +
    'MFA_REQUIRED stays distinct, consistent with password login. A profile carrying no ' +
    'email address is refused terminally (403 SOCIAL_EMAIL_UNAVAILABLE, KS-795 F-4) when no ' +
    'account was resolved by provider id, because an empty address is neither a link key nor ' +
    'a create key. Creates a new user when no account matches at all, then returns the ' +
    'standard token envelope. 400 on a missing code, an unknown provider, or a failed code ' +
    'exchange.',
  ...sla('write'),
  request: {
    params: z.object({
      provider: SocialProviderNameSchema,
    }),
    query: z.object({
      code: z
        .string()
        .min(1)
        .openapi({ description: 'Authorization code from the provider' }),
      // KS-722 Shape 1: REQUIRED, and verified. It was optional here and
      // ignored by the handler — minted at initiate, never stored, never read
      // back. A callback that cannot be tied to a flow this deployment started
      // is now refused.
      state: z
        .string()
        .min(1)
        .openapi({
          description:
            'The single-use nonce returned by GET /api/auth/social/{provider}. Verified and ' +
            'burned on use, and bound to the provider it was issued for. KS-819: the burn now ' +
            'happens AFTER the request-only checks below, so a callback that cannot complete ' +
            'never consumes it.',
        }),
      // KS-819 F-4: the provider's own refusal (RFC 6749 4.1.2.1). Present
      // INSTEAD of `code` when the user cancels or the provider denies the
      // request. Handled before the state consume, so a cancel does not burn
      // the nonce and the retry works. Never echoed back to the caller.
      error: z
        .string()
        .optional()
        .openapi({
          description:
            'Set by the provider when it refused the authorization (for example access_denied). ' +
            'Answered with 400 OAUTH_PROVIDER_ERROR. The value is logged, never reflected.',
        }),
    }),
  },
  responses: {
    200: {
      description: 'Authenticated',
      content: { 'application/json': { schema: SocialCallbackResponseSchema } },
    },
    400: {
      ...commonErrorResponses[400],
      description:
        'Missing code, unknown provider, or a failed code exchange. Also OAUTH_PROVIDER_ERROR ' +
        '(KS-819 F-4) when the provider itself refused the authorization and redirected with ' +
        'error= rather than code= - a user who cancels reaches this, and the state is NOT ' +
        'consumed, so starting again works. The provider error value is logged, never echoed.',
    },
    401: commonErrorResponses[401],
    403: {
      ...commonErrorResponses[403],
      description:
        'Four distinct codes, and the split is deliberate. ' +
        'OAUTH_STATE_INVALID (KS-722) - the callback could not be attributed to a flow this ' +
        'deployment started. ONE shape covering absent, expired, already-used and ' +
        'wrong-provider state alike, because splitting them would tell a prober which ' +
        'condition it hit and the remedy is identical in all four: start again. Checked ' +
        'BEFORE the provider code exchange, so a forged callback drives no outbound request - ' +
        'and, since KS-819, AFTER the checks that need only the request, so a codeless probe ' +
        'answers 400 whether the state was real or forged and burns neither. ' +
        'SOCIAL_SIGN_IN_REFUSED (KS-795 F-6) - the account may not be signed in with this ' +
        'provider. ONE shape covering every account-dependent refusal: an email match whose ' +
        'provider email claim is not sufficient proof to attach the identity, and an account ' +
        'whose status or lockout state forbids a credential. They are indistinguishable on ' +
        'purpose; differentiating them leaked account existence and account state to an ' +
        'unauthenticated caller. The message names no remedy while ' +
        'POST /api/auth/social/link does not persist a social id. ' +
        'SOCIAL_EMAIL_UNAVAILABLE (KS-795 F-4) - the provider supplied no email address and no ' +
        'account was resolved by provider id; refused terminally, because two different ' +
        'identities carrying empty addresses would otherwise collapse onto one row. ' +
        'MFA_REQUIRED - the account has a second factor and this callback has no channel to ' +
        'carry one. Distinct by design, consistent with password login.',
    },
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/auth/social/link',
  security: [{ bearerAuth: [] }],
  tags: ['Auth', 'Social'],
  summary: "Link a social account to the caller's existing account",
  description:
    'Returns 409 when the social account is already linked to a different user. Raises ' +
    'verificationLevel to SOCIAL when it was NONE or BASIC.',
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: SocialLinkRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'Linked',
      content: { 'application/json': { schema: SocialLinkResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'provider and code are required, or unknown provider' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    409: { ...commonErrorResponses[409], description: 'Already linked to another user' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// ROUTES — KS-712: /api/users/me/mfa (the self-service MFA trio)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/users/me/mfa/enable',
  security: [{ bearerAuth: [] }],
  tags: ['Users', 'MFA'],
  ...rateLimit('mfa'),
  summary: 'Begin MFA enrolment via the users surface',
  description:
    'Parallel to /api/auth/mfa/setup/start. Returns an otpauth:// URI in a field NAMED ' +
    '`qrCode` (services/auth/src/routes/users.ts:895) — a URI, not image data; a client ' +
    'author expecting a rendered QR code from that field will not get one. Both surfaces ' +
    'exist and both are routed. ⚠ They are not equivalent: /api/auth/mfa/setup/verify ' +
    'hashes the backup codes, while this trio stores them in PLAINTEXT (users.ts:920).',
  ...sla('write'),
  responses: {
    200: {
      description: 'Enrolment started',
      content: { 'application/json': { schema: UserMfaEnableResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'MFA is already enabled' },
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
  path: '/api/users/me/mfa/verify',
  security: [{ bearerAuth: [] }],
  tags: ['Users', 'MFA'],
  ...rateLimit('mfa'),
  summary: 'Complete MFA enrolment via the users surface',
  description: 'Returns backup codes ONCE and raises verificationLevel to STANDARD.',
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: UserMfaCodeRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'MFA enabled',
      content: { 'application/json': { schema: UserMfaVerifyResponseSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'Invalid code, or setup not initiated' },
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
  path: '/api/users/me/mfa/disable',
  security: [{ bearerAuth: [] }],
  tags: ['Users', 'MFA'],
  ...rateLimit('mfa'),
  summary: 'Disable MFA via the users surface',
  description: 'Requires a valid 6-digit code. Unlike /api/auth/mfa/disable it does not take a password.',
  ...sla('write'),
  request: {
    body: {
      required: true,
      content: { 'application/json': { schema: UserMfaCodeRequestSchema } },
    },
  },
  responses: {
    200: {
      description: 'MFA disabled',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    400: { ...commonErrorResponses[400], description: 'MFA not enabled, or invalid code' },
    401: commonErrorResponses[401],
    403: commonErrorResponses[403],
    404: commonErrorResponses[404],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// -----------------------------------------------------------------------------
// SCHEMAS — /api/oauth (OAuth 2.0 Authorization Code Flow with PKCE)
// -----------------------------------------------------------------------------

const OAuthTokenResponseSchema = sharedRegistry.register(
  'OAuthTokenResponse',
  z.object({
    access_token: z.string(),
    token_type: z.literal('Bearer'),
    expires_in: z.number().int().positive(),
    refresh_token: z.string().optional(),
    scope: z.string().optional(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    access_token: 'example-access_token',
    token_type: 'Bearer',
    expires_in: 1,
  },
  }),
);

const OAuthAppCreateRequestSchema = sharedRegistry.register(
  'OAuthAppCreateRequest',
  z.object({
    name: z.string().min(1).max(100),
    redirectUris: z.array(z.string().url()).min(1),
    scopes: z.array(z.enum(AVAILABLE_SCOPES as unknown as [string, ...string[]])).optional(),
    description: z.string().optional(),
    // KS-821: published because it is now VALIDATED. It used to be read from
    // the raw body after this schema parsed, so the contract was silent about
    // a field that decided whether the app must present PKCE (KS-804) or a
    // client secret (KS-820). Case is folded on the way in, so 'Public' is
    // accepted and stored as 'public'; anything outside the set is a 400.
    appType: z.enum(['public', 'confidential']).optional().openapi({
      description:
        'Client type. public (desktop/SPA/mobile) must use PKCE at the token endpoint; ' +
        'confidential (server-side) is issued a client_secret ONCE at registration and must ' +
        'authenticate with it at the token endpoint. Defaults to public. Case-insensitive; ' +
        'any other value is rejected with 400.',
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    name: 'example-name',
    redirectUris: [
      'https://example.com/resource',
      'https://example.com/resource',
    ],
  },
  }),
);

// KS-440 (response-side): rotate-secret returns `{ success, clientSecret, warning }`
// (no app), so this flat schema stays the rotate-secret response shape. The
// create endpoint returns a DIFFERENT wrapper (`{ success, app: {...},
// clientSecret }`) — see OAuthAppRegisterResponseSchema below.
const OAuthAppCreateResponseSchema = sharedRegistry.register(
  'OAuthAppCreateResponse',
  z.object({
    id: z.string(),
    clientId: z.string(),
    clientSecret: z.string().openapi({
      description:
        'PLAINTEXT secret. Returned ONLY at creation time and on rotate. Caller must persist it.',
    }),
    name: z.string(),
    redirectUris: z.array(z.string()),
    scopes: z.array(z.string()),
    createdAt: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    clientId: 'example-clientId',
    clientSecret: '<clientSecret>',
    name: 'example-name',
    redirectUris: [
      'example-redirectUris[]',
      'example-redirectUris[]',
    ],
    scopes: [
      'example-scopes[]',
      'example-scopes[]',
    ],
    createdAt: 'example-createdAt',
  },
  }),
);

// KS-440 (response-side): POST /api/oauth/apps returns `{ success, app: {...},
// clientSecret?, warning? }` (routes/oauth.ts POST '/apps'), NOT the flat
// id/clientId/... object the old OAuthAppCreateResponseSchema advertised — so
// every real 201 violated the response schema ("id is a required property",
// because id is nested under `app`). Publish the real wrapper. The nested `app`
// carries only the create-time subset (id, name, clientId, redirectUris,
// allowedScopes, appType). clientSecret + warning are present only for
// confidential apps, so both are optional.
const OAuthAppRegisterResponseSchema = sharedRegistry.register(
  'OAuthAppRegisterResponse',
  z
    .object({
      success: z.literal(true),
      app: z
        .object({
          id: z.string(),
          name: z.string(),
          clientId: z.string(),
          redirectUris: z.array(z.string()),
          allowedScopes: z.array(z.string()),
          appType: z.string(),
        })
        .passthrough(),
      clientSecret: z.string().nullable().optional().openapi({
        description:
          'PLAINTEXT secret. Returned ONLY at creation time, and only for confidential apps. Caller must persist it.',
      }),
      warning: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    app: {
      id: '00000000-0000-4000-8000-0000000000ff',
      name: 'example-name',
      clientId: 'app_01HC9ZP5FIXTUREID01',
      redirectUris: [
        'example-redirectUris[]',
        'example-redirectUris[]',
      ],
      allowedScopes: [
        'example-allowedScopes[]',
        'example-allowedScopes[]',
      ],
      appType: 'example-appType',
    },
  },
  }),
);

// KS-440 (response-side): the runtime OAuthApp record (services/oauth.ts
// mapAppRow) uses `allowedScopes` + `isActive`, not the `scopes` + `active` this
// schema previously required — so the real GET /api/oauth/apps items violated it
// ("scopes is a required property"). Rename to the real field names; `.passthrough()`
// already tolerates the extra fields the list returns (description, logoUrl, …).
const OAuthAppSchema = sharedRegistry.register(
  'OAuthApp',
  z
    .object({
      id: z.string(),
      clientId: z.string(),
      name: z.string(),
      description: z.string().nullable().optional(),
      redirectUris: z.array(z.string()),
      allowedScopes: z.array(z.string()),
      appType: z.string(),
      logoUrl: z.string().nullable().optional(),
      websiteUrl: z.string().nullable().optional(),
      isActive: z.boolean(),
      createdAt: z.string(),
      updatedAt: z.string().optional(),
    })
    .passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: 'example-id',
    clientId: 'example-clientId',
    name: 'example-name',
    redirectUris: [
      'example-redirectUris[]',
      'example-redirectUris[]',
    ],
    allowedScopes: [
      'example-allowedScopes[]',
      'example-allowedScopes[]',
    ],
    appType: 'example-appType',
    isActive: true,
    createdAt: 'example-createdAt',
  },
  }),
);

// KS-440 (response-side): the list handler returns `{ success, apps: [...] }`
// (routes/oauth.ts GET '/apps') — include the `success` flag it really sends.
const OAuthAppListResponseSchema = sharedRegistry.register(
  'OAuthAppListResponse',
  z.object({ success: z.literal(true), apps: z.array(OAuthAppSchema) }).passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    apps: [
      {
        id: '00000000-0000-4000-8000-0000000000ff',
        clientId: 'app_01HC9ZP5FIXTUREID01',
        name: 'example-name',
        redirectUris: [
          'example-redirectUris[]',
          'example-redirectUris[]',
        ],
        allowedScopes: [
          'example-allowedScopes[]',
          'example-allowedScopes[]',
        ],
        appType: 'example-appType',
        isActive: true,
        createdAt: FX.timestamps.createdAt,
      },
      {
        id: '00000000-0000-4000-8000-0000000000ff',
        clientId: 'app_01HC9ZP5FIXTUREID01',
        name: 'example-name',
        redirectUris: [
          'example-redirectUris[]',
          'example-redirectUris[]',
        ],
        allowedScopes: [
          'example-allowedScopes[]',
          'example-allowedScopes[]',
        ],
        appType: 'example-appType',
        isActive: true,
        createdAt: FX.timestamps.createdAt,
      },
    ],
  },
  }),
);

// KS-455: the single-app handlers (routes/oauth.ts GET/PATCH '/apps/:id')
// return `{ success, app }` — the bare OAuthApp the spec declared never
// matched a real response.
const OAuthAppDetailResponseSchema = sharedRegistry.register(
  'OAuthAppDetailResponse',
  z.object({ success: z.literal(true), app: OAuthAppSchema }).passthrough().openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    app: {
      id: '00000000-0000-4000-8000-0000000000ff',
      clientId: 'app_01HC9ZP5FIXTUREID01',
      name: 'example-name',
      redirectUris: [
        'example-redirectUris[]',
        'example-redirectUris[]',
      ],
      allowedScopes: [
        'example-allowedScopes[]',
        'example-allowedScopes[]',
      ],
      appType: 'example-appType',
      isActive: true,
      createdAt: FX.timestamps.createdAt,
    },
  },
  }),
);

const OAuthScopesResponseSchema = sharedRegistry.register(
  'OAuthScopesResponse',
  z.object({
    // KS-118: the handler returns richer scope objects than {name,description}.
    scopes: z.array(z.object({
      scope: z.string(),
      resource: z.string(),
      action: z.string(),
      description: z.string(),
    })),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    scopes: [
      {
        scope: 'example-scope',
        resource: 'example-resource',
        action: 'example-action',
        description: 'example-description',
      },
      {
        scope: 'example-scope',
        resource: 'example-resource',
        action: 'example-action',
        description: 'example-description',
      },
    ],
  },
  }),
);

// -----------------------------------------------------------------------------
// ROUTES — /api/oauth (OAuth 2.0 endpoints proxied verbatim from auth service)
// -----------------------------------------------------------------------------

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/oauth/authorize',
  security: [],
  tags: ['OAuth'],
  summary: 'OAuth 2.0 authorization endpoint (renders consent page)',
  description:
    'Step 1 of the Authorization Code flow with PKCE. Validates client_id, ' +
    'redirect_uri, response_type=code, code_challenge, code_challenge_method ' +
    '(S256 recommended) and renders the consent page. ' +
    'KS-822 F-6 — `code_challenge_method` accepts only `S256` or `plain` (RFC 7636 4.3); anything else, INCLUDING lowercase `s256`, is refused 400 invalid_request rather than treated as `plain`. Omitting it defaults to `S256`. ' +
    'KS-822 SCOPE HANDLING, all three cases: (a) OMITTED — a pre-defined default per RFC 6749 3.3, and the default is the app\'s ENTIRE registered allow-list. An empty or whitespace-only `scope` (and one of only separators) is treated as omitted and takes the same default. (b) PARTIAL overlap — the permitted subset is granted and the unpermitted entries are filtered out, not refused; the set you actually received is reported in the token response\'s `scope` field (RFC 6749 3.3). (c) ONLY unpermitted — REFUSED 400 `invalid_scope` (F-5), because a filter that removes everything is not a grant anybody decided on. So omitting `scope` grants the most and naming only things you may not have grants nothing at all: send the scopes you actually want. ' +
    'KS-839 WILDCARD: a legacy app whose allow-list contains `*` is granted NOTHING, including an entry that only becomes `*` once split on spaces or commas (` *`, `openid,*`); new registrations are closed to the nine published scopes, so such an app exists only as an older registration. A request that names scopes is refused 400 `invalid_scope`; an omitted `scope` gives an empty grant, so the token carries no scopes. An OAuth token with no scopes satisfies no scope requirement, so a route that requires a scope refuses it (403), unless the route also admits the caller by role; a route that requires no scope does not refuse it for want of one, though a role check on that route can still refuse it. ',
  request: {
    query: z.object({
      client_id: z.string(),
      // KS-822 F-7: optional. The resolver falls back to the app's registered
      // URI when EXACTLY one is registered, and refuses the omission otherwise
      // (RFC 6749 3.1.2.3). Declared required here while GET already accepted
      // it absent.
      redirect_uri: z.string().optional(),
      response_type: z.literal('code'),
      scope: z.string().optional(),
      state: z.string().optional(),
      // KS-822 F-QA-2: was `z.string()` — published as REQUIRED while the route
      // requires it only for PUBLIC clients (`resolveAuthorizeClient` RULE 3).
      // A confidential GET with no `code_challenge` answers 200 and always has;
      // the contract overstated a requirement the route does not enforce.
      code_challenge: z
        .string()
        .optional()
        .openapi({
          description:
            'REQUIRED for PUBLIC clients — a public app has no secret, so PKCE is the only ' +
            'credential that can carry the code, and omitting it is refused 400 invalid_request. ' +
            'OPTIONAL for CONFIDENTIAL clients, which authenticate with client_secret at the token ' +
            'endpoint instead.',
        }),
      code_challenge_method: z.enum(['S256', 'plain']).optional(),
    }),
  },
  responses: {
    // The handler renders an HTML consent page (res.send(consentHtml) with
    // Content-Type: text/html). Declaring the text/html body — rather than a
    // bare content-less 200 — keeps the response sample-able so Akto's native
    // OpenAPI 3.1 importer creates the endpoint (KS-322).
    200: {
      description: 'Consent page (HTML).',
      content: { 'text/html': { schema: z.string() } },
    },
    400: { ...commonErrorResponses[400], description:
      'KS-804: GET and POST share one resolver, so both refuse on the SAME app rules and with the same code. (KS-822 F-8: the count that stood here — "four" — was hand-maintained and was already wrong once F-6 and F-5 each added a rule. A number nobody derives is a claim that drifts, so the number is gone rather than corrected; the rules themselves are enumerated below.) unsupported_response_type (response_type is not `code`); invalid_client (unknown or malformed client_id); invalid_redirect_uri (not registered for the app, not an absolute URL, or an executable scheme such as javascript:/data: — KS-804 Q4); invalid_request (a required parameter is missing, or a PUBLIC client sent no code_challenge, which is refused rather than minted because exchangeCode can only verify PKCE when a challenge was stored); invalid_request also covers a `code_challenge_method` outside {S256, plain} (KS-822 F-6 — including lowercase `s256`); invalid_request also covers an OMITTED `redirect_uri` when the app registers other than exactly one (KS-822 F-7 — with exactly one registered it may be omitted and that one is used); invalid_scope (KS-822 F-5 — the request named ONLY scopes this client may not hold, so the filter would have left an empty grant; PARTIAL overlap is still filtered rather than refused, and the granted set is reported in the token response `scope` field per RFC 6749 3.3).' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// KS-781 F-7: authorize had NO requestBody schema at all — `mfaCode` was
// documented in prose only, and the credential fields were undescribed. This is
// the same shape the route now enforces (authorizeCredentialsSchema), so the
// contract and the runtime agree rather than merely coexisting.
export const OAuthAuthorizeRequestSchema = sharedRegistry.register(
  'OAuthAuthorizeRequest',
  z.object({
    // KS-781 N-2 (related): the runtime trims before validating, so a spec
    // without .trim() is NARROWER than the runtime and a spec-driven generator
    // can never produce the padded-email class that was F-1's Blocker. Mirror
    // it, and the corpus contains the input that broke the lockout.
    email: z.string().trim().email().openapi({ description: 'Account email. Trimmed and lower-cased before use, exactly as at /api/auth/login.' }),
    password: z.string().min(1),
    mfaCode: MFA_CODE_ACCEPTED.optional().openapi({ description: 'Second factor: 6 digits (TOTP) or an 8-character backup code. REQUIRED when the account has MFA enabled — omitting it returns 403 MFA_REQUIRED (KS-781). An empty string counts as absent, so a form-backed client that always submits the field is accepted (KS-781 N-1). Same shape as POST /api/auth/login, from one shared definition (KS-781 P3-4).' }),
    client_id: z.string(),
    // KS-822 F-7: optional, on the same rule as the GET query above.
    redirect_uri: z.string().optional(),
    scope: z.string().optional(),
    state: z.string().optional(),
    code_challenge: z.string().optional(),
    // KS-822 F-6: was `z.string()`, which published a freedom the route does not
    // grant. The resolver refuses anything but these two with 400
    // invalid_request, so an open string told integrators that `s256` was
    // acceptable when it is the exact value that used to downgrade in silence.
    code_challenge_method: z.enum(['S256', 'plain']).optional(),
    action: z.string().optional().openapi({ description: "'deny' redirects back with error=access_denied." }),
  }).openapi({ description: 'Consent-form submission. The credential fields are gated exactly as /api/auth/login gates them (KS-781).' }),
);

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/oauth/authorize',
  security: [],
  tags: ['OAuth'],
  summary: 'Submit consent decision (issues authorization code)',
  // KS-781 F-7: login carries rateLimit('login'); this door authenticates the
  // same credential and carried no annotation at all.
  ...rateLimit('login'),
  request: {
    body: {
      required: true,
      content: {
        // KS-781: JSON ONLY, and the 415 the registry injects for it is the
        // truth. An earlier round of this PR also declared
        // x-www-form-urlencoded here so the shipped consent page's own form
        // would be contractual; that was REVERTED on Kam's ruling
        // (2026-09-05) — see FORM_ALLOWED_PATHS in the gateway's
        // contentType.ts. In short: the page is stopped one layer earlier by
        // CSRF regardless (a pre-existing defect, its own ticket), so the
        // relaxation bought nothing, and it opened a preflight-free
        // cross-origin path to an endpoint that verifies a password.
        'application/json': { schema: OAuthAuthorizeRequestSchema },
      },
    },
  },
  description:
    'After the user approves on the consent page, the authorization code ' +
    'is issued and the browser is redirected back to redirect_uri with ' +
    '?code=...&state=.... ' +
    'KS-781: before a code is issued this endpoint applies account lockout, ' +
    'account status, password verification and the second factor. It is not ' +
    'identical to POST /api/auth/login: login additionally resolves platform ' +
    'admins and upgrades a legacy password hash on success, neither of which ' +
    'happens here. An account with MFA enabled must supply `mfaCode` in the ' +
    'body (6 digits = TOTP, 8 alphanumeric = backup code); omitting it returns ' +
    '403 MFA_REQUIRED and issues no code. An empty `mfaCode` is treated as ' +
    'absent, so a client that always submits the field is accepted. ' +
    'The request body must be application/json: a non-JSON body is refused ' +
    '415 at the gateway before this endpoint runs. ' +
    'KS-822 F-6 — `code_challenge_method` accepts only `S256` or `plain` (RFC 7636 4.3); anything else, INCLUDING lowercase `s256`, is refused 400 invalid_request rather than treated as `plain`. Omitting it defaults to `S256`. ' +
    'KS-822 SCOPE HANDLING, all three cases: (a) OMITTED — a pre-defined default per RFC 6749 3.3, and the default is the app\'s ENTIRE registered allow-list. An empty or whitespace-only `scope` (and one of only separators) is treated as omitted and takes the same default. (b) PARTIAL overlap — the permitted subset is granted and the unpermitted entries are filtered out, not refused; the set you actually received is reported in the token response\'s `scope` field (RFC 6749 3.3). (c) ONLY unpermitted — REFUSED 400 `invalid_scope` (F-5), because a filter that removes everything is not a grant anybody decided on. So omitting `scope` grants the most and naming only things you may not have grants nothing at all: send the scopes you actually want. ' +
    'KS-839 WILDCARD: a legacy app whose allow-list contains `*` is granted NOTHING, including an entry that only becomes `*` once split on spaces or commas (` *`, `openid,*`); new registrations are closed to the nine published scopes, so such an app exists only as an older registration. A request that names scopes is refused 400 `invalid_scope`; an omitted `scope` gives an empty grant, so the token carries no scopes. An OAuth token with no scopes satisfies no scope requirement, so a route that requires a scope refuses it (403), unless the route also admits the caller by role; a route that requires no scope does not refuse it for want of one, though a role check on that route can still refuse it. ',
  responses: {
    302: { description: 'Redirect to redirect_uri with code+state' },
    400: { ...commonErrorResponses[400], description:
      'KS-804: GET and POST share one resolver, so both refuse on the SAME app rules and with the same code. (KS-822 F-8: the count that stood here — "four" — was hand-maintained and was already wrong once F-6 and F-5 each added a rule. A number nobody derives is a claim that drifts, so the number is gone rather than corrected; the rules themselves are enumerated below.) unsupported_response_type (response_type is not `code`); invalid_client (unknown or malformed client_id); invalid_redirect_uri (not registered for the app, not an absolute URL, or an executable scheme such as javascript:/data: — KS-804 Q4); invalid_request (a required parameter is missing, or a PUBLIC client sent no code_challenge, which is refused rather than minted because exchangeCode can only verify PKCE when a challenge was stored); invalid_request also covers a `code_challenge_method` outside {S256, plain} (KS-822 F-6 — including lowercase `s256`); invalid_request also covers an OMITTED `redirect_uri` when the app registers other than exactly one (KS-822 F-7 — with exactly one registered it may be omitted and that one is used); invalid_scope (KS-822 F-5 — the request named ONLY scopes this client may not hold, so the filter would have left an empty grant; PARTIAL overlap is still filtered rather than refused, and the granted set is reported in the token response `scope` field per RFC 6749 3.3).' },
    403: { ...commonErrorResponses[403], description: 'MFA_REQUIRED — the account has a second factor and no usable mfaCode was supplied (KS-781)' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

// KS-823 — NOT NARRATED IN THE PUBLISHED DESCRIPTION, deliberately (Wednesday's
// 2026-09-05 ruling). On grant_type=refresh_token NO client is authenticated
// at all today, for either app type. That is an OPEN DEFECT (KS-823, High,
// file-only by ruling), not the rule below applied one grant over.
//
// It is recorded HERE, in source, and NOT in `description` because a published
// contract states what an endpoint DOES on the grant it describes; it does not
// advertise an unfixed authentication gap, or a ticket id, to every consumer
// that can read the spec. A defect is not a guarantee.
//
// The reason the note has to exist at all: read as a universal, "a PUBLIC app
// authenticates no client" supplies an innocent-sounding explanation for the
// refresh path's silence, and would let the next maintainer close KS-823 as
// working-as-intended. The description below is scoped to ONE grant so the
// implication cannot be drawn; this comment is where the gap is named.
sharedRegistry.registerPath({
  method: 'post',
  path: '/api/oauth/token',
  security: [],
  tags: ['OAuth'],
  summary: 'Exchange authorization code (or refresh token) for tokens',
  description:
    'Standard OAuth 2.0 token endpoint. application/x-www-form-urlencoded ' +
    'body. grant_type=authorization_code (with code + code_verifier + ' +
    'redirect_uri + client_id) or grant_type=refresh_token. ' +
    'KS-820 — CLIENT AUTHENTICATION, on grant_type=authorization_code. The client_id is ' +
    'resolved first: an unknown or deactivated one is 401 invalid_client. A CONFIDENTIAL app ' +
    'MUST then authenticate, by HTTP Basic (client_id:client_secret, RFC 6749 2.3.1) or a ' +
    'client_secret body parameter; a missing or wrong secret is 401 invalid_client, and a ' +
    'valid PKCE verifier does NOT substitute for it (RFC 6749 4.1.3). A PUBLIC app has no ' +
    'secret, so ON THIS GRANT it authenticates no client and must instead carry PKCE. So a ' +
    'code is redeemable only on the credential its client type demands — a verified secret ' +
    'for a confidential app, a verified PKCE challenge for a public one — and never on ' +
    'neither. Before this, a code with no code_challenge (every confidential app, plus rows ' +
    'minted before KS-804) redeemed with no credential at all.',
  responses: {
    200: {
      description: 'Token response',
      content: { 'application/json': { schema: OAuthTokenResponseSchema } },
    },
    // F-1b — `invalid_client` is NOT published here. Measured on the route:
    // in `routes/oauth.ts`, BOTH `res.status(401)` returns carrying
    // `message: 'invalid_client'` — the one described 'Unknown or inactive
    // client' and the one described 'Client authentication failed' — answer
    // 401. Listing it at 400 told integrators to branch on a status this
    // endpoint never returns for that cause.
    //
    // Cited by ANCHOR, not by line: the first version of this comment said
    // `:611`/`:619`, which its own insertion pushed to `:620`/`:628` in the
    // same commit. A line number is stale the moment the file above it moves.
    400: { ...commonErrorResponses[400], description: 'invalid_grant / invalid_request / unsupported_grant_type' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    // F-1b — this operation is `security: []`: there is no bearer token to be
    // missing. The shared 401 says "missing, expired, or invalid bearer token —
    // acquire a fresh token via POST /api/auth/login", which sends a client that
    // presented a WRONG SECRET to go log in as a user. Wrong credential, wrong
    // remedy. Stated for what this endpoint actually refuses.
    401: {
      ...commonErrorResponses[401],
      description:
        'invalid_client, on grant_type=authorization_code — the client_id is unknown ' +
        "or deactivated, or a confidential app's client_secret is missing or wrong. " +
        'This is CLIENT authentication (HTTP Basic or a client_secret body parameter), ' +
        'not user authentication: there is no bearer token on this operation and ' +
        'logging in does not resolve it.',
    },
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/oauth/revoke',
  security: [],
  tags: ['OAuth'],
  summary: 'Revoke a token (RFC 7009)',
  description:
    'Token revocation endpoint. Returns 200 regardless of whether the ' +
    'token was active, per RFC 7009.',
  responses: {
    400: commonErrorResponses[400],
    200: { description: 'Token revoked (always)' },
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
  path: '/api/oauth/scopes',
  security: [],
  tags: ['OAuth'],
  summary: 'List the OAuth scopes the platform supports',
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Available scopes',
      content: { 'application/json': { schema: OAuthScopesResponseSchema } },
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    404: commonErrorResponses[404],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
    401: commonErrorResponses[401],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/oauth/apps',
  tags: ['OAuth', 'Apps'],
  summary: 'Register a new OAuth client app',
  description:
    'Returns the plaintext client_secret ONCE — caller must persist it. ' +
    'Service stores only a hash. appType is validated against the closed set ' +
    '{public, confidential} and case-folded (KS-821); it used to be read from the raw body ' +
    'outside the request schema, so a caller could register an app that was neither — and an ' +
    'app that is neither takes the else-branch of BOTH the PKCE rule and the client-secret ' +
    'rule. The column now carries a matching CHECK constraint (migration 047).',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: { 'application/json': { schema: OAuthAppCreateRequestSchema } },
    },
  },
  responses: {
    201: {
      description: 'App registered (plaintext secret returned ONCE, confidential apps only)',
      content: { 'application/json': { schema: OAuthAppRegisterResponseSchema } },
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
  path: '/api/oauth/apps',
  tags: ['OAuth', 'Apps'],
  summary: 'List the caller\'s OAuth apps',
  security: [{ bearerAuth: [] }],
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'App list (no secrets)',
      content: { 'application/json': { schema: OAuthAppListResponseSchema } },
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
  path: '/api/oauth/apps/{id}',
  tags: ['OAuth', 'Apps'],
  summary: 'Get OAuth app details',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'App detail (no secret)',
      // KS-455: runtime returns { success, app }
      content: { 'application/json': { schema: OAuthAppDetailResponseSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'App not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'patch',
  path: '/api/oauth/apps/{id}',
  tags: ['OAuth', 'Apps'],
  summary: 'Update an OAuth app (name / redirect URIs / scopes)',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string() }),
    body: {
      content: {
        'application/json': {
          schema: z
            .object({
              name: z.string().min(1).max(100).optional(),
              redirectUris: z.array(z.string().url()).min(1).optional(),
              scopes: z.array(z.enum(AVAILABLE_SCOPES as unknown as [string, ...string[]])).optional(),
              description: z.string().optional(),
            })
            .passthrough(),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'App updated',
      // KS-455: runtime returns { success, app }
      content: { 'application/json': { schema: OAuthAppDetailResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'App not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'delete',
  path: '/api/oauth/apps/{id}',
  tags: ['OAuth', 'Apps'],
  summary: 'Deactivate (soft-delete) an OAuth app',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'App deactivated',
      content: { 'application/json': { schema: AuthSuccessSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'App not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/oauth/apps/{id}/rotate-secret',
  tags: ['OAuth', 'Apps'],
  summary: 'Rotate the client secret for an OAuth app',
  description:
    'Returns the new plaintext secret ONCE. Old secret is invalidated immediately.',
  security: [{ bearerAuth: [] }],
  request: { params: z.object({ id: z.string() }) },
  responses: {
    400: commonErrorResponses[400],
    200: {
      description: 'Secret rotated (plaintext returned ONCE)',
      content: { 'application/json': { schema: OAuthAppCreateResponseSchema } },
    },
    401: commonErrorResponses[401],
    404: { ...commonErrorResponses[404], description: 'App not found' },
    403: commonErrorResponses[403],
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

// =============================================================================
// ISSUER CERTS — KS-83 PR 1
// =============================================================================

const IssuerCertSummarySchema = sharedRegistry.register(
  'IssuerCertSummary',
  z.object({
    id: z.string().uuid(),
    name: z.string(),
    organizationId: z.string().uuid().nullable(),
    fingerprintSha256: z.string(),
    subject: z.string(),
    issuer: z.string(),
    serialNumber: z.string(),
    validFrom: z.string(),
    validUntil: z.string(),
    keyAlgorithm: z.string(),
    keySizeBits: z.number().int().nullable(),
    trustLevel: z.enum(['self-signed', 'ca-anchored', 'aatl']),
    status: z.enum(['active', 'revoked', 'expired']),
    uploadedAt: z.string(),
    uploadedById: z.string().uuid(),
    revokedAt: z.string().nullable(),
    revokedById: z.string().uuid().nullable(),
    revocationReason: z.string().nullable(),
    previousCertId: z.string().uuid().nullable(),
    certPem: z.string(),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    id: '550e8400-e29b-41d4-a716-446655440000',
    name: 'example-name',
    organizationId: FX.tenant.id,
    fingerprintSha256: 'example-fingerprintSha256',
    subject: 'example-subject',
    issuer: 'example-issuer',
    serialNumber: 'example-serialNumber',
    validFrom: 'example-validFrom',
    validUntil: 'example-validUntil',
    keyAlgorithm: 'example-keyAlgorithm',
    keySizeBits: 1,
    trustLevel: 'self-signed',
    status: 'active',
    uploadedAt: 'example-uploadedAt',
    uploadedById: '550e8400-e29b-41d4-a716-446655440000',
    revokedAt: 'example-revokedAt',
    revokedById: '550e8400-e29b-41d4-a716-446655440000',
    revocationReason: 'example-revocationReason',
    previousCertId: '550e8400-e29b-41d4-a716-446655440000',
    certPem: 'example-certPem',
  },
  }),
);

const IssuerCertUploadRequestSchema = sharedRegistry.register(
  'IssuerCertUploadRequest',
  z.object({
    name: z.string().min(1).max(200).openapi({
      description: 'Human-readable label, e.g. "Acme Corp 2026 signing cert".',
    }),
    certPem: z.string().min(1).openapi({
      description:
        'PEM-encoded X.509 cert. Single end-entity cert only — multi-cert chain bundles are rejected with 400 MULTI_CERT_PEM in v1.',
    }),
    privateKeyPem: z.string().min(1).openapi({
      description: "PEM-encoded private key matching the cert's public key.",
    }),
    privateKeyPassword: z.string().optional().openapi({
      description: 'Passphrase for the private key (omit for unencrypted keys).',
    }),
    organizationId: z.string().uuid().optional().openapi({
      description:
        'Optional org binding. v1 supports tenant-wide certs (NULL); user-level + per-org certs are follow-ups.',
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    name: 'example-name',
    certPem: 'example-certPem',
    privateKeyPem: 'example-privateKeyPem',
  },
  }),
);

const IssuerCertListResponseSchema = sharedRegistry.register(
  'IssuerCertListResponse',
  z.object({
    success: z.boolean(),
    certs: z.array(IssuerCertSummarySchema),
    pagination: z.object({
      total: z.number().int().nonnegative(),
      limit: z.number().int().positive(),
      offset: z.number().int().nonnegative(),
    }),
  }).openapi({
  // KS-256: generated example (synthesised, masked). Guarded by
  // `npm run check:openapi` -> check-spec-examples (E1-E7).
    example: {
    success: true,
    certs: [
      {
        id: '550e8400-e29b-41d4-a716-446655440000',
        name: 'example-name',
        organizationId: FX.tenant.id,
        fingerprintSha256: 'example-fingerprintSha256',
        subject: 'example-subject',
        issuer: 'example-issuer',
        serialNumber: 'example-serialNumber',
        validFrom: 'example-validFrom',
        validUntil: 'example-validUntil',
        keyAlgorithm: 'example-keyAlgorithm',
        keySizeBits: 1,
        trustLevel: 'self-signed',
        status: 'active',
        uploadedAt: 'example-uploadedAt',
        uploadedById: '550e8400-e29b-41d4-a716-446655440000',
        revokedAt: 'example-revokedAt',
        revokedById: '550e8400-e29b-41d4-a716-446655440000',
        revocationReason: 'example-revocationReason',
        previousCertId: '550e8400-e29b-41d4-a716-446655440000',
        certPem: 'example-certPem',
      },
      {
        id: '550e8400-e29b-41d4-a716-446655440000',
        name: 'example-name',
        organizationId: FX.tenant.id,
        fingerprintSha256: 'example-fingerprintSha256',
        subject: 'example-subject',
        issuer: 'example-issuer',
        serialNumber: 'example-serialNumber',
        validFrom: 'example-validFrom',
        validUntil: 'example-validUntil',
        keyAlgorithm: 'example-keyAlgorithm',
        keySizeBits: 1,
        trustLevel: 'self-signed',
        status: 'active',
        uploadedAt: 'example-uploadedAt',
        uploadedById: '550e8400-e29b-41d4-a716-446655440000',
        revokedAt: 'example-revokedAt',
        revokedById: '550e8400-e29b-41d4-a716-446655440000',
        revocationReason: 'example-revocationReason',
        previousCertId: '550e8400-e29b-41d4-a716-446655440000',
        certPem: 'example-certPem',
      },
    ],
    pagination: {
      total: 0,
      limit: 1,
      offset: 0,
    },
  },
  }),
);

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/issuer-certs',
  tags: ['IssuerCerts'],
  summary: 'Upload an X.509 cert + private key for document signing (KS-83 PR 1)',
  description:
    'KS-83 (2026-05-15): per-org X.509 cert lifecycle. Cert metadata is parsed ' +
    'at upload (subject, issuer, validity, fingerprint, key algorithm). The ' +
    'private key is verified against the cert via a sign+verify roundtrip on a ' +
    'random nonce, then encrypted at rest via AES-256-GCM with AAD bound to the ' +
    'cert row id (packages/shared encryptField pattern).\n\n' +
    'v1 sub-decisions (Kam, 2026-05-15):\n' +
    '  - **Self-signed allowed** — `trustLevel` field surfaces it; consumers decide.\n' +
    '  - **Refused at upload if expired** — existing signatures stay valid forever; new ones don\'t.\n' +
    '  - **Org-level only for v1** — user-level certs are a follow-up.\n' +
    '  - **Encrypted blob storage** — KV HSM upgrade is a swap behind a single helper.\n\n' +
    'Idempotent: re-POSTing a cert with a fingerprint that already exists in ' +
    'this tenant returns the existing row with `idempotent: true` instead of ' +
    'creating a duplicate.\n\n' +
    'RBAC: ORG_ADMIN+ role OR `issuer-certs:write` scope.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': { schema: IssuerCertUploadRequestSchema },
      },
    },
  },
  responses: {
    201: {
      description: 'Cert uploaded',
      content: {
        'application/json': {
          schema: z.object({ success: z.boolean(), cert: IssuerCertSummarySchema }),
        },
      },
    },
    200: {
      description: 'Cert already existed (idempotent re-upload by fingerprint)',
      content: {
        'application/json': {
          schema: z.object({
            success: z.boolean(),
            cert: IssuerCertSummarySchema,
            idempotent: z.literal(true),
          }),
        },
      },
    },
    400: {
      ...commonErrorResponses[400],
      description:
        'INVALID_CERT_PEM (cert unparseable), MULTI_CERT_PEM (chain bundle, v1 single only), KEY_PARSE_ERROR (key malformed or wrong passphrase), VALIDATION_ERROR (missing/invalid request fields), TENANT_REQUIRED (JWT has no tenantId claim).',
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and the `issuer-certs:write` scope.',
    },
    422: {
      ...commonErrorResponses[400],
      description:
        'CERT_EXPIRED (validUntil already passed), CERT_NOT_YET_VALID (validFrom > now+24h), KEY_MISMATCH (private key does not match cert public key).',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/issuer-certs',
  tags: ['IssuerCerts'],
  summary: "List issuer certs in the caller's tenant",
  description:
    "Paginated list of issuer certs scoped to the caller's tenant. Optional " +
    '`status` filter (active | revoked | expired). Encrypted private keys are ' +
    'never included in the response — only public-cert PEM + parsed metadata.',
  security: [{ bearerAuth: [] }],
  responses: {
    200: {
      description: 'Cert list',
      content: { 'application/json': { schema: IssuerCertListResponseSchema } },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and the `issuer-certs:read` scope.',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'get',
  path: '/api/issuer-certs/{id}',
  tags: ['IssuerCerts'],
  summary: 'Get a single issuer cert by id',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string().uuid() }),
  },
  responses: {
    200: {
      description: 'Cert detail',
      content: {
        'application/json': {
          schema: z.object({ success: z.boolean(), cert: IssuerCertSummarySchema }),
        },
      },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and the `issuer-certs:read` scope.',
    },
    404: { ...commonErrorResponses[404], description: 'Cert not found in this tenant' },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/issuer-certs/{id}/revoke',
  tags: ['IssuerCerts'],
  summary: 'Revoke an issuer cert (KS-83 PR 2)',
  description:
    'Logical revoke — sets status=revoked + records revoked_at + revoked_by_id + ' +
    "optional reason. Existing signatures made when the cert was active stay valid " +
    'forever (digital signatures attest to a moment in time, not perpetual cert ' +
    "validity). Future calls to `POST /api/documents/{id}/version action='sign-cert'` " +
    'will refuse to use a revoked cert.\n\n' +
    'Idempotency: re-revoking returns **409 ALREADY_REVOKED** with the existing ' +
    'cert state, not a 200 — clear signal you\'re acting on stale state.\n\n' +
    'RBAC: ORG_ADMIN+ role OR `issuer-certs:revoke` scope.',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string().uuid() }),
    body: {
      content: {
        'application/json': {
          schema: z.object({
            reason: z.string().max(500).optional().openapi({
              description: 'Free-form revocation reason recorded on the row (e.g. "key compromise", "no longer in use").',
            }),
          }),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'Cert revoked',
      content: {
        'application/json': {
          schema: z.object({ success: z.boolean(), cert: IssuerCertSummarySchema }),
        },
      },
    },
    400: commonErrorResponses[400],
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and the `issuer-certs:revoke` scope.',
    },
    404: { ...commonErrorResponses[404], description: 'Cert not found in this tenant' },
    409: {
      ...commonErrorResponses[400],
      description: 'ALREADY_REVOKED — cert was revoked previously. Response includes the existing cert state.',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/issuer-certs/{id}/rotate',
  tags: ['IssuerCerts'],
  summary: 'Rotate an issuer cert (KS-83 PR 2)',
  description:
    'Atomic rotation — revokes the old cert and inserts a new cert with ' +
    '`previous_cert_id` linked to the predecessor, all in a single ' +
    'transaction. Either both succeed or neither does.\n\n' +
    'Historical signatures stay valid forever — they reference the OLD cert ' +
    'by fingerprint, which is preserved as a row in `status=revoked`. The ' +
    'verify endpoint can walk `previous_cert_id` to surface rotation history.\n\n' +
    'Pre-conditions:\n' +
    '  - Old cert exists in tenant (404 NOT_FOUND otherwise)\n' +
    '  - Old cert is currently active (409 NOT_ACTIVE if revoked/expired)\n' +
    '  - New cert fingerprint differs from old (400 SAME_FINGERPRINT — no-op rotation rejected)\n\n' +
    'Body: same shape as `POST /api/issuer-certs` plus an optional `reason` ' +
    "field that lands on the revoked-old row (defaults to 'rotated'). The " +
    "new cert inherits the old cert's name and organizationId unless " +
    'explicitly overridden.\n\n' +
    'RBAC: ORG_ADMIN+ role OR (`issuer-certs:write` AND `issuer-certs:revoke`) scopes.',
  security: [{ bearerAuth: [] }],
  request: {
    params: z.object({ id: z.string().uuid() }),
    body: {
      content: {
        'application/json': {
          schema: IssuerCertUploadRequestSchema.extend({
            // KS-430: rotate inherits the old cert's name unless explicitly
            // overridden (see this op's description), so `name` is optional
            // here — the runtime rotateSchema already treats it as optional.
            // The base upload schema marks name required, which was wrong for
            // rotate and made the published contract stricter than the runtime.
            name: z.string().min(1).max(200).optional(),
            reason: z.string().max(500).optional(),
          }),
        },
      },
    },
  },
  responses: {
    201: {
      description: 'Rotation succeeded',
      content: {
        'application/json': {
          schema: z.object({
            success: z.boolean(),
            newCert: IssuerCertSummarySchema,
            revokedCert: IssuerCertSummarySchema,
          }),
        },
      },
    },
    400: {
      ...commonErrorResponses[400],
      description:
        'INVALID_CERT_PEM, MULTI_CERT_PEM, KEY_PARSE_ERROR, VALIDATION_ERROR, TENANT_REQUIRED, or SAME_FINGERPRINT (new cert matches old — no-op rotation rejected).',
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and BOTH `issuer-certs:write` + `issuer-certs:revoke` scopes.',
    },
    404: { ...commonErrorResponses[404], description: 'Old cert not found in this tenant' },
    409: {
      ...commonErrorResponses[400],
      description: 'NOT_ACTIVE — old cert is in status revoked/expired and cannot be rotated.',
    },
    422: {
      ...commonErrorResponses[400],
      description: 'CERT_EXPIRED, CERT_NOT_YET_VALID, or KEY_MISMATCH on the new cert.',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});

sharedRegistry.registerPath({
  method: 'post',
  path: '/api/issuer-certs/sign',
  tags: ['IssuerCerts'],
  summary: 'Sign a content hash with the tenant\'s active cert (KS-83 PR 3)',
  description:
    'Active X.509 signing primitive — decrypts the tenant\'s active cert ' +
    'private key (AAD-bound to row id), signs the supplied sha256 content ' +
    'hash, returns signature + algorithm + public cert in a single envelope ' +
    'shape callers can wrap into a `.sig.json` companion file.\n\n' +
    'Cert selection: `certId` body field targets a specific cert by id ' +
    '(useful for replaying historical signatures). When omitted, the most ' +
    'recently uploaded active cert for the caller\'s tenant is used (v1 ' +
    'rule — KS-83 sub-decision 4: org-level only).\n\n' +
    'Refuses to sign with revoked or expired certs (409 CERT_NOT_ACTIVE / ' +
    'CERT_EXPIRED). Existing signatures made when the cert was active stay ' +
    'valid forever — digital signatures attest to a moment in time, not ' +
    'perpetual cert validity.\n\n' +
    'Originate\'s `POST /api/documents/{id}/sign-cert` calls this internally ' +
    '(forwards the caller\'s Bearer token so this route\'s RBAC applies).\n\n' +
    'RBAC: ORG_ADMIN+ role OR `issuer-certs:sign` scope.',
  security: [{ bearerAuth: [] }],
  request: {
    body: {
      content: {
        'application/json': {
          schema: z.object({
            contentHash: z.string().openapi({
              description: 'sha256 hex digest to sign (64 lowercase hex chars, optional `sha256:` prefix).',
            }),
            certId: z.string().uuid().optional().openapi({
              description: 'Optional cert id override. When omitted, picks the tenant\'s most recently uploaded active cert.',
            }),
          }),
        },
      },
    },
  },
  responses: {
    200: {
      description: 'Signed — envelope ready for `.sig.json` wrapping',
      content: {
        'application/json': {
          schema: z.object({
            success: z.boolean(),
            signature: z.string().openapi({ description: 'Base64-encoded signature bytes.' }),
            signatureAlgorithm: z.enum(['RS256', 'ES256', 'EdDSA']),
            signedContentHash: z.string(),
            signedAt: z.string(),
            cert: z.object({
              id: z.string().uuid(),
              fingerprintSha256: z.string(),
              subject: z.string(),
              issuer: z.string(),
              certPem: z.string(),
              validFrom: z.string(),
              validUntil: z.string(),
              trustLevel: z.enum(['self-signed', 'ca-anchored', 'aatl']),
            }),
          }),
        },
      },
    },
    400: {
      ...commonErrorResponses[400],
      description: 'VALIDATION_ERROR (missing fields), INVALID_CONTENT_HASH (not sha256 hex), TENANT_REQUIRED (no tenantId in JWT).',
    },
    401: { ...commonErrorResponses[401], description: 'Missing or invalid Bearer token' },
    403: {
      ...commonErrorResponses[403],
      description: 'Caller lacks ORG_ADMIN+ role and the `issuer-certs:sign` scope.',
    },
    404: {
      ...commonErrorResponses[404],
      description: 'NO_ACTIVE_CERT — no active issuer cert for this tenant (or the supplied certId was not found).',
    },
    409: {
      ...commonErrorResponses[400],
      description: 'CERT_NOT_ACTIVE (status=revoked/expired) or CERT_EXPIRED (validUntil passed since last sweep).',
    },
    422: {
      ...commonErrorResponses[400],
      description: 'UNSUPPORTED_KEY_ALGORITHM — cert key isn\'t RSA/EC/Ed25519.',
    },
    429: commonErrorResponses[429],
    500: commonErrorResponses[500],
    502: commonErrorResponses[502],
    503: commonErrorResponses[503],
  },
});
