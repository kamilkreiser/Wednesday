---
title: Secuura Security Reference
created: 27-02-2026
updated: 23-06-2026
tags: [reference/security, reference/developer]
status: active
---

# Secuura Security Reference

## Summary

This document covers the complete security posture of the Secuura Verification System. It details authentication and authorisation mechanisms, client-side hashing enforcement, data protection, API security, blockchain security, and the most recent hardening changes from the P1-P5 fix cycle.

**Key Points:**
- JWT-based authentication with httpOnly refresh cookies and in-memory access tokens
- Client-side document hashing enforced (SVS principle: documents never leave the browser)
- Input sanitisation, rate limiting, brute force protection, and suspicious request detection
- All password storage uses bcrypt; all hash comparisons use constant-time comparison

---

## Table of Contents

- [Authentication](#authentication)
- [Authorisation](#authorisation)
- [Client-Side Hashing](#client-side-hashing)
- [Data Protection](#data-protection)
- [API Security](#api-security)
- [Blockchain Security](#blockchain-security)
- [Smart Contract Audits](#smart-contract-audits)
- [Environment Security](#environment-security)
- [Recent Hardening (P1-P5)](#recent-hardening-p1-p5)
- [Known Security Considerations](#known-security-considerations)
- [Security Checklist for Code Review](#security-checklist-for-code-review)

---

## Authentication

### JWT Implementation

| Parameter | Value |
|-----------|-------|
| Algorithm | RS256 (RSA-SHA256, asymmetric) — RS256-only since the KS-167/184/302 cutover; HS256 fully dropped |
| Access token storage | In-memory (JavaScript variable, never localStorage) |
| Refresh token storage | httpOnly, secure cookie |
| Access token lifetime | Configurable via `JWT_EXPIRES_IN` (default: 1 day) |
| Keys | `JWT_PRIVATE_KEY` (auth signs) + `JWT_PUBLIC_KEY` (verifiers) + `JWT_KEY_ID` (kid). No shared secret. |
| Fail-fast | Auth exits if `JWT_PRIVATE_KEY` is missing; verifiers fail-closed (reject all) if `JWT_PUBLIC_KEY` is missing |

### Token Rotation

1. Client authenticates with email/password via `POST /api/auth/login`
2. Auth service validates credentials using bcrypt
3. Auth service generates a JWT pair (access + refresh)
4. Access token returned in response body
5. Refresh token set as httpOnly cookie
6. Client stores access token in memory (not localStorage or sessionStorage)
7. On expiry, client calls `POST /api/auth/refresh` with the httpOnly refresh cookie
8. Auth service generates a new token pair and invalidates the old refresh token

### MFA Support

- TOTP (Time-based One-Time Password) support via `totp` service
- Backup codes for recovery
- MFA verification required at login when `mfaEnabled: true` on user account
- MFA code validated via `POST /api/auth/login` with `mfaCode` field

### Session Management

- Sessions stored in Redis with `session:*` prefix
- Each session tracks: userId, deviceId, IP, user-agent, creation time
- Session revocation supported (`POST /api/auth/logout`)
- Admin can view and terminate active sessions

### Wallet Authentication (CIP-30)

1. User connects their Cardano wallet via CIP-30 browser extension
2. Server generates a random nonce/challenge
3. Wallet signs the challenge using CIP-8 message signing
4. Server verifies the signature against the declared wallet address
5. Session created linking wallet address to user account

> **Important:** CIP-8 signature verification currently uses a development stub that only checks for non-empty values. Production deployment requires integration with `@emurgo/cardano-message-signing` WASM library. In production mode, the stub returns `false` and logs an error.

### Password Security

| Parameter | Value |
|-----------|-------|
| Hash algorithm | bcrypt |
| Minimum length | 8 characters (registration schema) |
| Strength check | Custom `checkPasswordStrength()` with feedback |
| Reset flow | Token-based: `POST /api/auth/password/forgot` generates SHA-256 hashed token with 24h expiry |
| Reset token storage | PostgreSQL (`email_tokens` table) |

### Social OAuth and Enterprise IdP

Supported providers (credentials loaded via `.env.local`):
- Google OAuth
- GitHub OAuth
- Microsoft Entra ID (formerly Azure AD)
- Auth0

### Input Validation

All authentication endpoints use Zod schemas for strict input validation:
- `loginSchema`: email (valid format), password (min 1 char), optional mfaCode (6 chars), optional deviceId
- `registerSchema`: email, password (min 8), optional firstName, lastName, organizationId (UUID)
- `refreshSchema`: refreshToken (string)
- `forgotPasswordSchema`: email (valid format)
- `resetPasswordSchema`: token (string), password (min 8)

---

## Authorisation

### Role-Based Access Control

| Role | Code Value | Access |
|------|-----------|--------|
| System Administrator | `SYSTEM_ADMIN` | Full platform access, admin portal |
| Owner | `OWNER` | Issuer portal, own organisation's resources |
| Verifier | `VERIFIER` | Verifier portal, public verification endpoints |
| Holder | `HOLDER` | Issuer portal, own documents and credentials |

### Middleware Chain

Two middleware functions enforce authorisation in the API gateway:

**`authenticateToken(required: boolean = true)`**
- Extracts JWT from `Authorization: Bearer <token>` header
- Verifies signature and expiry
- Attaches `UserPayload` to `req.user`
- When `required = false`: allows unauthenticated access, falls back to `x-user-id` header for user identification

**`requireAdmin`**
- Must be chained after `authenticateToken(true)`
- Checks `req.user.role === 'SYSTEM_ADMIN'`
- Returns `403 Forbidden` if not admin

### Per-Endpoint Auth Requirements

| Category | Auth Required | Middleware |
|----------|--------------|-----------|
| Public verification | No | None |
| Auth endpoints (login, register, refresh) | No | None |
| Billing pricing (GET) | No | None |
| Midnight ZKP verification | No | None |
| User-specific settings (notifications, privacy) | Optional | `authenticateToken(false)` |
| Standard API (documents, wallet, etc.) | Yes | `authenticateToken(true)` |
| Admin endpoints | Yes + Admin | `authenticateToken(true)`, `requireAdmin` |

---

## Client-Side Hashing

### SVS Principle

All document hashing MUST be performed client-side in the browser. The original document file never leaves the user's device. Only the resulting hash is transmitted to Secuura services.

### Implementation

**Verifier Portal** (`frontend/verifier/src/components/VerifyPage.tsx`):
```typescript
const buffer = await file.arrayBuffer();
const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
const hashArray = Array.from(new Uint8Array(hashBuffer));
const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
// Only the hash is sent to the API
```

**Issuer Portal** (`frontend/issuer/src/utils/hashing.ts`):
- Same approach using Web Crypto API
- Works offline (no server dependency for hashing)

### Backend Hashing (Server-Side)

Backend services use `packages/shared/src/crypto/index.ts` for:
- Certification hash computation (BLAKE2b-256 of structured JSON)
- Provenance chain hashing (BLAKE2b-256)
- Hash verification with constant-time comparison (`crypto.timingSafeEqual`)

### Hash Formats

| Algorithm | Format | Usage |
|-----------|--------|-------|
| SHA-256 | `sha256:{64 hex chars}` | Client-side verification |
| BLAKE2b-256 | `blake2b:{64 hex chars}` | Backend certification and provenance |

---

## Data Protection

### No Document Storage

Secuura does NOT store original documents. What is stored:

| Stored | Not Stored |
|--------|-----------|
| Document hash (on blockchain) | Original document files |
| Document metadata (title, type, timestamps) | Document content |
| Document location URI (optional reference) | Binary file data |
| Certification and verification records | Copies of documents |
| Provenance data | |

### Encryption at Rest

- **AES-256-GCM** for off-chain encrypted metadata
- 12-byte IV, 16-byte auth tag
- Keys derived via PBKDF2 (SHA-512, 100,000 iterations)

### GDPR Endpoints

Privacy settings endpoints allow users to manage their data preferences:
- `GET/PUT /api/privacy/settings` -- User privacy preferences
- Privacy preferences stored in Redis with `settings:privacy:*` prefix

---

## API Security

### Rate Limiting

Three tiers of rate limiting, configurable per environment:

| Tier | Window | Max (Dev) | Max (Prod) | Scope |
|------|--------|-----------|-----------|-------|
| Authentication | 15 minutes | 10 | 5 | Login attempts |
| General API | 1 minute | 100 | 60 | Standard API calls |
| Verification | 1 minute | 200 | 100 | Public verification |

Rate limiting uses `express-rate-limit` with Redis-backed storage (fallback to in-memory).

### Brute Force Protection

- Redis-backed tracking of failed login attempts per IP
- Free retries: 5
- Progressive delay: 500ms minimum, 30s maximum
- Lockout window: 5 minutes

### Input Sanitisation

All incoming request bodies are sanitised to prevent XSS:
- `&` → `&amp;`
- `<` → `&lt;`
- `>` → `&gt;`
- `"` → `&quot;`
- `'` → `&#x27;`

Arrays are preserved during sanitisation (not converted to objects).

### Suspicious Request Detection

Incoming requests are scanned for patterns indicating:
- **Path traversal:** `../`
- **XSS attempts:** `<script`
- **SQL injection:** `union select`
- **Command injection:** `exec(`

Matched requests are logged with severity level and rejected with `400 Bad Request`.

### CORS Configuration

- Allowed origins configured via `CORS_ORIGINS` environment variable
- Default (dev): `http://localhost:6100,6101,6102,6103,6882,6881`
- Production: set to actual deployment domains

### CSRF Protection

- CSRF secret configurable via `CSRF_SECRET` environment variable
- Cookie security configurable via `CSRF_COOKIE_SECURE`

### Security Headers (Nginx)

All responses from the nginx gateway include:

| Header | Value |
|--------|-------|
| `X-Frame-Options` | `SAMEORIGIN` |
| `X-Content-Type-Options` | `nosniff` |
| `X-XSS-Protection` | `1; mode=block` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |

Production HTTPS configuration adds:

| Header | Value |
|--------|-------|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains; preload` |
| `Content-Security-Policy` | `default-src 'self'; script-src 'self' 'unsafe-inline'; ...` |

### Security Logging

Dedicated `securityLog()` function records security events with:
- Request ID, user ID, IP address
- HTTP method and path
- User-agent
- Severity level (`low`, `medium`, `high`, `critical`)
- Event-specific details

Logged to Winston with `type: 'security'` metadata for filtering.

### Request Tracking

Every request is assigned a unique `requestId` (UUID v4) for correlation across services.

---

## Blockchain Security

### Transaction Signing

- Platform wallet (anchoring, backend operations): BIP-39 mnemonic stored in `PLATFORM_WALLET_MNEMONIC` environment variable
- User wallets (NFT minting): CIP-30 browser extension signing -- private keys never leave the user's wallet
- Transaction building via MeshSDK (client) or `@emurgo/cardano-serialization-lib-nodejs` (server)

### Wallet Mnemonic Protection

- Mnemonic is passed via environment variable, never stored in code or configuration files
- In Docker Compose, loaded via `env_file` or environment variable expansion
- Development fallback: empty string (operations that require a wallet will fail gracefully)

### Anchor Verification

- Each anchor transaction is submitted via Blockfrost and recorded with transaction hash and block height
- Verification queries the Cardano blockchain to confirm the transaction exists and contains the expected metadata
- Simulated anchors (when blockchain is unavailable) are flagged with `simulated: true`

### NFT Policy Scripts

- Minting policies use Cardano native scripts
- Policy IDs are deterministic (derived from the script)
- Client-side minting ensures the user controls the transaction

---

## Smart Contract Audits

Three independent smart contract audits have been completed:

| Audit | Scope | Issues Found | Issues Fixed |
|-------|-------|-------------|-------------|
| Audit 1 | Staking validator | 8 | 8 |
| Audit 2 | Revenue distribution | 9 | 9 |
| Audit 3 | Token policy | 5 | 5 |
| **Total** | | **22** | **22** |

All identified issues were resolved. Audit reports are available in the project documentation.

---

## Environment Security

### Secrets Management

All sensitive configuration is managed through environment variables:

| Category | Variables | Storage |
|----------|----------|---------|
| JWT | `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` / `JWT_KEY_ID` | Env var + Key Vault (RS256; fail-fast / fail-closed) |
| Database | `POSTGRES_PASSWORD` | Env var |
| Redis | `REDIS_PASSWORD` | Env var |
| Blockchain | `BLOCKFROST_API_KEY`, `PLATFORM_WALLET_MNEMONIC` | Env var |
| OAuth | `AZURE_AD_CLIENT_SECRET`, `ENTRA_CLIENT_SECRET` | `.env.local` file |
| Stripe | `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` | Env var |
| IPFS | `PINATA_SECRET_KEY`, `INFURA_PROJECT_SECRET` | Env var |

### Development Fallbacks

Several values have development-only fallbacks that are explicitly logged as warnings:

| Variable | Dev Fallback | Warning |
|----------|-------------|---------|
| `JWT_PRIVATE_KEY` / `JWT_PUBLIC_KEY` | RS256 keypair generated locally by `bootstrap-env.sh` | Auth won't boot without the keypair |
| `POSTGRES_PASSWORD` | `secuura_dev_password` | Docker Compose default |
| `REDIS_PASSWORD` | `secuura_redis_dev` | Docker Compose default |

### Mock Mode Warnings

Services operating in mock mode log warnings at startup:

| Service | Mode Variable | Modes |
|---------|--------------|-------|
| PRISM | `PRISM_MODE` | `mock`, `basic`, `testnet`, `mainnet` |
| Midnight | `MIDNIGHT_MODE` | `mock`, `testnet`, `mainnet` |
| IPFS | `IPFS_PROVIDER` | `mock`, `pinata`, `infura`, `web3storage` |
| Stripe | `STRIPE_MODE` | `test`, `live` |

---

## Recent Hardening (P1-P5)

### Authentication Hardening

- **Notification settings** (`GET/PUT /api/settings/notifications`): Added `authenticateToken(false)` middleware (was previously unprotected)
- **Privacy settings** (`GET/PUT /api/privacy/settings`): Added `authenticateToken(false)` middleware
- **Analytics dashboard**: Added auth headers (`Authorization: Bearer` and `x-user-id`) to all fetch calls
- **Governance dashboard**: Added auth headers to all governance API calls
- **Export dialog**: Added auth headers to analytics export requests

### Client-Side Hashing Migration

The verifier portal previously uploaded the document file to the server for hashing. This has been changed to:
1. User drops/selects a file in the browser
2. Web Crypto API hashes the file client-side using SHA-256
3. Only the hash string is sent to `POST /api/verification/verify`
4. Server uses the hash to look up the document record

### Response Format Standardisation

Over 10 API endpoints were updated to return consistent response format:
```json
{
  "success": true,
  "data": { ... }
}
```

This prevents information leakage from inconsistent error formats and simplifies frontend error handling.

### Error Handling

- Admin profile page: proper error messages on save failure (was silently failing)
- Error boundary: respects React Router `basename` for home navigation (was navigating to `/` instead of `/verify/`)
- CardanoScan link: conditional rendering prevents linking to `undefined` transaction hashes

---

## Known Security Considerations

### Must Fix Before Production

| Item | Location | Risk | Fix Required |
|------|----------|------|-------------|
| CIP-8 signature verification stub | `packages/shared/src/cardano/wallet.ts` L251-263 | **Critical** | Integrate `@emurgo/cardano-message-signing` WASM library |
| Placeholder password hash | `services/api-gateway/src/index.ts` seeded identity users | **High** | Use bcrypt hashes or remove seed data |
| PgBouncer placeholder SCRAM hashes | `docker/pgbouncer/userlist.txt` L21-27 | **High** | Generate real SCRAM-SHA-256 hashes |
| Demo credentials | `demo@secuura.io`/`demo123`, `admin@secuura.com`/`admin123` | **Medium** | Disable in production (gated by `ENABLE_DEMO_SEED`) |
| Mock staking endpoint | `services/staking/src/routes/rewards.ts` `POST /api/rewards/add-mock` | **Medium** | Remove or gate behind dev-only flag |
| Analytics service returns random data | `services/analytics/src/services/analyticsService.ts` | **Medium** | Connect to real data pipeline |
| In-memory stores (6+ services) | KYC, M365, Timestamping, NFT, Referral, Billing | **Medium** | Migrate to PostgreSQL/Redis |

### Accepted Risks (Development Phase)

| Item | Justification |
|------|---------------|
| Development JWT fallback secret | Only active when `NODE_ENV !== 'production'` and logs a warning |
| Mock PRISM/Midnight modes | Properly gated by environment variables; real modes available |
| Demo seed data | Gated by `ENABLE_DEMO_SEED`; intended for development/demo only |
| `import.meta.env.DEV` simulation buttons | Only visible in Vite development builds |

---

## Security Checklist for Code Review

### Authentication
- [ ] No hardcoded credentials, API keys, or secrets in code
- [ ] No exposed tokens or passwords in comments or logs
- [ ] JWT secret validated at startup (fail-fast in production)
- [ ] Refresh tokens stored in httpOnly cookies only
- [ ] Access tokens stored in memory (not localStorage)
- [ ] Password hashing uses bcrypt with sufficient cost

### Input Validation
- [ ] All user inputs validated with Zod schemas
- [ ] Request body sanitised (XSS entities encoded)
- [ ] Suspicious patterns rejected (path traversal, SQL injection, XSS, command injection)
- [ ] File uploads: only hashes accepted, no binary content stored

### API Security
- [ ] Rate limiting applied to all endpoints
- [ ] Brute force protection on login
- [ ] CORS configured for allowed origins only
- [ ] Security headers present in all responses
- [ ] Request tracking via unique request ID

### Data Protection
- [ ] No original documents stored
- [ ] Sensitive data encrypted at rest (AES-256-GCM)
- [ ] Hash comparisons use constant-time comparison
- [ ] GDPR endpoints available for privacy management

### Blockchain
- [ ] Wallet mnemonics in environment variables only
- [ ] Client-side signing (private keys never leave wallet)
- [ ] Anchor verification checks on-chain transaction existence
- [ ] NFT minting is client-initiated and user-signed

---

## References

### Internal Links
- Secuura Crypto and Blockchain Developer Reference
- Secuura Architecture Reference
- Secuura Mock Data Audit

### External Links
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CIP-30 dApp Connector](https://cips.cardano.org/cip/CIP-0030/)
- [CIP-8 Message Signing](https://cips.cardano.org/cip/CIP-0008/)
- [Express Rate Limit](https://www.npmjs.com/package/express-rate-limit)
- [Zod Validation](https://zod.dev/)
