# Secuura Platform — Platform Hardening Change Summary

**Date:** 17 February 2026  
**Version:** 2.2.0  
**Branch:** main  
**Scope:** Auth security (httpOnly cookies), PostgreSQL persistence, anchoring service integration, SVS-compliant client-side hashing

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Auth Service — httpOnly Refresh Token Cookies](#2-auth-service--httponly-refresh-token-cookies)
3. [Document Storage — PostgreSQL Persistence](#3-document-storage--postgresql-persistence)
4. [Blockchain Anchoring Integration](#4-blockchain-anchoring-integration)
5. [Client-Side Document Hashing](#5-client-side-document-hashing)
6. [Frontend AuthContext Refactor](#6-frontend-authcontext-refactor)
7. [Bug Fixes and Incidental Changes](#7-bug-fixes-and-incidental-changes)
8. [Files Modified](#8-files-modified)
9. [Database Changes](#9-database-changes)
10. [Testing Results](#10-testing-results)

---

## 1. Executive Summary

This session resolves four outstanding platform items identified during the 17 February testing session. All four changes move the platform from development workarounds to production-ready implementations.

| Item | Before | After | SVS Impact |
|------|--------|-------|------------|
| **Auth refresh tokens** | Returned in JSON body; stored in localStorage as workaround | Set as httpOnly cookie; browser-managed | Prevents XSS token theft |
| **Document storage** | In-memory Map; lost on container restart | PostgreSQL via Prisma (DB + in-memory fallback) | True persistence across restarts |
| **Blockchain anchoring** | Simulated locally with fake txHash | Calls anchoring service; falls back to simulation | Real on-chain anchoring when Blockfrost key is set |
| **Document upload** | File sent to server via FormData | Client-side SHA-256 hash via Web Crypto API; only hash + metadata sent as JSON | SVS compliance — file never leaves browser |

**Key outcomes:**

- Refresh tokens are now httpOnly, SameSite=Strict, scoped to `/api/auth`, with 7-day expiry
- Documents persist in PostgreSQL and survive container restarts
- Anchoring endpoint calls the real anchoring service with automatic fallback
- Document registration hashes the file entirely in the browser — zero file upload

---

## 2. Auth Service — httpOnly Refresh Token Cookies

### Dependency Added

- `cookie-parser` (runtime) and `@types/cookie-parser` (devDependency) added to `services/auth/package.json`

### Middleware (`services/auth/src/index.ts`)

- `cookieParser()` middleware registered before body parsing
- CORS `credentials: true` already configured (no change needed)

### Login Endpoint (`POST /api/auth/login`)

After generating the token pair, the refresh token is set as an httpOnly cookie:

```
Set-Cookie: refresh_token=<JWT>; Max-Age=604800; Path=/api/auth; HttpOnly; SameSite=Strict
```

The JSON response still includes `refreshToken` for backward compatibility but clients should ignore it.

### Refresh Endpoint (`POST /api/auth/refresh`)

- Reads the token from `req.cookies.refresh_token` (falls back to `req.body.refreshToken` for backward compat)
- On success, sets a fresh (rotated) cookie with the new refresh token
- Response body returns only `accessToken` and `expiresIn` (no `refreshToken`)

### Logout Endpoint (`POST /api/auth/logout`)

- Clears the cookie via `res.clearCookie('refresh_token', { path: '/api/auth' })`

### Cookie Flow

```
Browser → POST /api/auth/login → Auth Service
  ← 200 OK + Set-Cookie: refresh_token (httpOnly)
  ← JSON { accessToken, user }

Browser → POST /api/auth/refresh (empty body, cookie sent automatically)
  ← 200 OK + Set-Cookie: refresh_token (rotated)
  ← JSON { accessToken }

Browser → POST /api/auth/logout
  ← 200 OK + Clear-Cookie: refresh_token
```

---

## 3. Document Storage — PostgreSQL Persistence

### New File: `services/originate/src/repositories/documentRepo.ts`

A repository layer following the same pattern as `certificationRepo.ts`:

- **`checkDb()`** — tests database connectivity on startup
- **In-memory `Map`** as fallback when DB is unavailable
- **`saveDocument()`** — dual-write to in-memory + PostgreSQL (raw SQL upsert via `ON CONFLICT (external_id)`)
- **`getDocument(id)`** — checks in-memory first, then DB (by `external_id`, then by UUID)
- **`listDocuments(filters)`** — merges in-memory and DB results, deduplicates by ID
- **`updateDocument(id, updates)`** — updates both stores
- **`seedDemoDocuments()`** — moved from routes; seeds both stores on startup

### Route Refactor: `services/originate/src/routes/documents.ts`

All direct `Map` operations replaced with calls to `documentRepo`. Route handlers are now thin wrappers that validate input and delegate to the repository.

### Database Index

A unique index was created on `documents.external_id` to support upsert operations:

```sql
CREATE UNIQUE INDEX idx_documents_external_id ON documents (external_id);
```

### Verified Persistence

After restart, seed documents are found in PostgreSQL:

| external_id | title | status |
|-------------|-------|--------|
| doc-demo-degree-001 | BSc Computer Science — University of Oxford | anchored |
| doc-demo-transcript-002 | Academic Transcript — 2022-2025 | signed |
| doc-demo-certificate-003 | Professional Certification — AWS Solutions Architect | anchored |

Documents created through the UI are also persisted and survive restarts.

---

## 4. Blockchain Anchoring Integration

### Updated: `POST /api/documents/:id/anchor`

The anchor handler now:

1. Attempts to call the real anchoring service at `http://anchoring:4005/api/anchors` with `{ documentId, contentHash, network }`
2. On success, uses the returned `txHash`, `blockHeight`, and `anchoredAt`
3. On failure (service unavailable), falls back to simulated anchoring with `tx_sim_*` prefix and a warning log

### Anchoring Service Status

The anchoring service container (`secuura-anchoring`) is not currently running in the local Docker Compose stack. When started with a valid `BLOCKFROST_API_KEY` for preprod, it will submit real Cardano transactions. The originate service gracefully degrades to simulation mode in its absence.

### Log Output

```
[Anchor] Anchoring service unavailable, simulating for doc-demo-certificate-003: fetch failed
```

---

## 5. Client-Side Document Hashing

### Updated: `frontend/issuer/src/components/DocumentUpload.tsx`

The document registration flow now:

1. **Hashes the file client-side** using `hashDocument()` from `utils/hashing.ts` (SHA-256 via Web Crypto API)
2. **Shows hashing progress**: "Generating cryptographic hash of your document..."
3. **Displays the computed hash** to the user after hashing completes
4. **Sends only JSON**: `{ title, documentType, description, contentHash }` — no `FormData`, no file
5. **Info alert** permanently visible: "Your document is hashed locally in the browser. The file never leaves your device — only the cryptographic hash and metadata are sent to the server."

### Updated: `frontend/issuer/src/services/api.ts`

`documentApi.create()` changed from:

```typescript
// BEFORE: File uploaded to server (SVS violation)
create: (formData: FormData) =>
  api.post('/documents', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
    timeout: 60000,
  })
```

To:

```typescript
// AFTER: Only hash + metadata sent as JSON
create: (data: { title: string; documentType: string; description?: string; contentHash: string }) =>
  api.post('/documents', data)
```

### UI Text Changes

| Element | Before | After |
|---------|--------|-------|
| Page heading | "Upload New Document" | "Register New Document" |
| Submit button | "Upload Document" | "Register Document" |
| Loading state | "Uploading..." | "Hashing & Registering..." |
| Success dialog title | "Document Uploaded Successfully" | "Document Registered Successfully" |
| Success description | "...has been uploaded and is ready..." | "...has been registered and is ready..." |

### SVS Compliance

This change fully satisfies the SVS development principle:

> **All document hashing MUST be performed client-side in the browser. Documents MUST NOT be uploaded to Secuura servers for hashing. Only the hash is transmitted to the backend.**

---

## 6. Frontend AuthContext Refactor

### Updated: `frontend/issuer/src/context/AuthContext.tsx`

- **Removed** all `localStorage` persistence (`auth_token`, `auth_user`, `refresh_token`)
- **Session restore on mount**: Calls `refreshToken()` which sends the httpOnly cookie automatically; if valid, fetches `/users/me` to populate user profile
- **Login**: Stores `accessToken` in memory only; cookie is set by the backend
- **Logout**: Clears in-memory state; cookie is cleared by the backend
- **Refresh**: Sends `POST /auth/refresh` with empty body and `withCredentials: true`; browser includes cookie automatically

### Improved User Experience

After refresh, the user profile now shows the full `displayName` ("Demo User") instead of the generic "User" that was stored in localStorage. The `/users/me` endpoint provides the complete profile.

---

## 7. Bug Fixes and Incidental Changes

### Nginx Gateway DNS Cache

After rebuilding and restarting the `issuer-frontend` container, the nginx gateway cached the old container's IP address, returning 502. Fixed by restarting `nginx-gateway` after any container recreation.

---

## 8. Files Modified

### Backend — Auth Service

| File | Change |
|------|--------|
| `services/auth/package.json` | Added `cookie-parser`, `@types/cookie-parser` |
| `services/auth/src/index.ts` | Added `cookieParser()` middleware |
| `services/auth/src/routes/auth.ts` | Login sets cookie; refresh reads cookie; logout clears cookie |

### Backend — Originate Service

| File | Change |
|------|--------|
| `services/originate/src/repositories/documentRepo.ts` | **NEW** — Document repository with DB + in-memory fallback |
| `services/originate/src/routes/documents.ts` | Refactored to use repo; added anchoring service call |

### Frontend — Issuer Portal

| File | Change |
|------|--------|
| `frontend/issuer/src/context/AuthContext.tsx` | Removed localStorage; cookie-based refresh; fetches /users/me |
| `frontend/issuer/src/components/DocumentUpload.tsx` | Client-side hashing; JSON-only submission; UI text updates |
| `frontend/issuer/src/services/api.ts` | `documentApi.create()` changed from FormData to JSON |

### Database

| Change | SQL |
|--------|-----|
| Unique index on `external_id` | `CREATE UNIQUE INDEX idx_documents_external_id ON documents (external_id)` |

---

## 9. Database Changes

### Schema

No Prisma schema changes — the `documents` table and all related tables already existed.

### Data

Three demo documents are seeded on every originate service startup (idempotent via upsert):

| ID | Title | Status |
|----|-------|--------|
| doc-demo-degree-001 | BSc Computer Science — University of Oxford | anchored |
| doc-demo-transcript-002 | Academic Transcript — 2022-2025 | signed |
| doc-demo-certificate-003 | Professional Certification — AWS Solutions Architect | draft → anchored (during testing) |

---

## 10. Testing Results

### Auth Flow (httpOnly Cookies)

| Test | Result |
|------|--------|
| Login returns `Set-Cookie: refresh_token` with httpOnly, SameSite=Strict | PASS |
| Refresh reads cookie, returns new accessToken, rotates cookie | PASS |
| Logout clears the cookie | PASS |
| Full page reload restores session via cookie refresh | PASS |
| User profile shows "Demo User" after refresh (not generic "User") | PASS |

### Document Persistence

| Test | Result |
|------|--------|
| Seed documents appear in PostgreSQL | PASS |
| New documents created via UI persist in PostgreSQL | PASS |
| Document status updates persist (e.g. anchored) | PASS |
| Dashboard shows correct document counts after restart | PASS |

### Blockchain Anchoring

| Test | Result |
|------|--------|
| Anchor endpoint attempts real service call | PASS |
| Falls back to simulation when service unavailable | PASS |
| Simulation uses `tx_sim_*` prefix (distinguishable) | PASS |
| Document status updated to "anchored" | PASS |

### Client-Side Hashing

| Test | Result |
|------|--------|
| File hashed in browser via Web Crypto API | PASS |
| Hash displayed to user before and after submission | PASS |
| Only JSON (hash + metadata) sent to server | PASS |
| No FormData or file in network request | PASS |
| Document created in DB with correct hash | PASS |
| Success dialog shows hash and document ID | PASS |

### End-to-End Browser Test (Playwright)

| Step | Result |
|------|--------|
| Navigate to issuer portal | PASS |
| Login with demo credentials | PASS |
| Dashboard loads with correct stats (4 docs, 1 certified, 1 pending, 2 on-chain) | PASS |
| Navigate to "New Document" | PASS |
| Page shows "Register New Document" heading | PASS |
| Upload file, auto-populate title | PASS |
| Submit → hash computed, document registered | PASS |
| Success dialog with hash and document ID | PASS |
| Return to dashboard → new document visible | PASS |
| Full page reload → session restored via cookie | PASS |
