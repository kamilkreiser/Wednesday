---
title: Secuura Platform — Test Findings and Fixes Report
created: 17-02-2026
updated: 17-02-2026
tags: [secuura/testing, secuura/development, secuura/fixes]
status: active
---

# Secuura Platform — Test Findings and Fixes Report

---

| **Document** | Test Findings and Fixes Report |
|---|---|
| **Version** | 1.0.0 |
| **Date** | 17 February 2026 |
| **Classification** | Internal — Development |

---

## Summary

During end-to-end testing of the NFT wallet flow and broader issuer portal functionality, several critical issues were identified and resolved. This document catalogues each finding, its root cause, the fix applied, and any remaining items for future attention.

**Key Points:**
- 8 issues identified and fixed across 3 services (originate, api-gateway, issuer-frontend)
- Test data now persists across container restarts via seed data
- Missing API endpoint (`GET /documents`) added
- API gateway mock handlers refactored to forward to originate service
- Frontend data normalisation improved for backend compatibility

---

## Table of Contents

- [Finding 1: No Data Persistence Across Container Restarts](#finding-1-no-data-persistence-across-container-restarts)
- [Finding 2: Missing GET /documents List Endpoint](#finding-2-missing-get-documents-list-endpoint)
- [Finding 3: API Gateway Mock Handlers Intercepting Originate Service](#finding-3-api-gateway-mock-handlers-intercepting-originate-service)
- [Finding 4: Dashboard Data Path Mismatch](#finding-4-dashboard-data-path-mismatch)
- [Finding 5: Document ID Validation Rejecting Seed IDs](#finding-5-document-id-validation-rejecting-seed-ids)
- [Finding 6: Signature and Date Field Naming Mismatch](#finding-6-signature-and-date-field-naming-mismatch)
- [Finding 7: Status Configuration Missing for Backend Statuses](#finding-7-status-configuration-missing-for-backend-statuses)
- [Finding 8: POST /documents Dual Payload Format](#finding-8-post-documents-dual-payload-format)
- [Future Work: Items Not Yet Resolved](#future-work-items-not-yet-resolved)

---

## Finding 1: No Data Persistence Across Container Restarts

### Severity: HIGH

### Problem
The originate service stores all documents in an in-memory `Map<string, Document>`. When the Docker container restarts, all documents are lost. There was no seed data mechanism, meaning the UI always started empty and required manual document creation via cURL or the upload form before any testing could proceed.

The auth service also uses in-memory storage but already has a `seedDemoUsers()` function that recreates demo users (`demo@secuura.io` / `demo123`) on startup. However, the originate service had no equivalent.

### Root Cause
- `services/originate/src/routes/documents.ts` — `const documents = new Map<string, Document>()` initialised empty
- `package.json` referenced a `seed` script (`tsx src/seed.ts`) but the seed file did not exist

### Fix Applied
Added a `seedDemoDocuments()` function to `documents.ts` that runs on module load and populates 3 demo documents with varied statuses:

| Document ID | Title | Status | Has Signatures | Has Blockchain |
|---|---|---|---|---|
| `doc-demo-degree-001` | BSc Computer Science — University of Oxford | `anchored` | Yes (1) | Yes (txHash, block) |
| `doc-demo-transcript-002` | Academic Transcript — 2022-2025 | `signed` | Yes (1) | No |
| `doc-demo-certificate-003` | Professional Certification — AWS Solutions Architect | `draft` | No | No |

The seed function only runs when `NODE_ENV !== 'production'`, matching the auth service's behaviour.

### Files Modified
- `Blockchain/Dev/services/originate/src/routes/documents.ts`

---

## Finding 2: Missing GET /documents List Endpoint

### Severity: HIGH

### Problem
The originate service only had `GET /api/documents/:id` (single document by ID). There was no `GET /api/documents` endpoint to list all documents. The frontend's `DocumentList` component and `Dashboard` component both called this endpoint and received 404 errors, resulting in empty document lists and zero-value stat cards.

### Root Cause
The endpoint was simply never implemented. The `documentsRouter` had `POST /`, `GET /:id`, `POST /:id/sign`, `POST /:id/anchor`, and `POST /:id/verify` but no `GET /`.

### Fix Applied
Added `GET /api/documents` endpoint with:
- Pagination support (`page`, `limit` query parameters)
- Status filtering (`status` query parameter)
- Newest-first sorting
- Response format: `{ documents: [...], total, page, limit }`

### Files Modified
- `Blockchain/Dev/services/originate/src/routes/documents.ts`

---

## Finding 3: API Gateway Mock Handlers Intercepting Originate Service

### Severity: CRITICAL

### Problem
The API gateway (`services/api-gateway/src/index.ts`) had mock endpoint handlers registered before the proxy routes that forward requests to the originate service. These mock handlers always returned fabricated data and never called `next()`, meaning requests never reached the originate service.

Affected mock handlers:
- `GET /api/documents/:id` — Always returned `{ type: 'DOCUMENT', status: 'draft', data: {} }` regardless of actual document state
- `POST /api/documents` — Created mock documents in the gateway instead of forwarding to originate
- `POST /api/documents/:id/sign/request` — Returned mock signing data
- `POST /api/documents/:id/sign` — Stored signatures in Redis only, not in originate
- `POST /api/documents/:id/anchor` — Returned mock transaction data without updating document status

This meant that even though the originate service had correct implementations with seed data, the frontend never received real data.

### Root Cause
These mock handlers were added during early development before the originate service had full endpoint coverage. They were registered before `app.use('/api/documents', createProxyMiddleware(...))` and matched first due to Express route precedence.

### Fix Applied
1. **`GET /api/documents/:id`**: Changed to only intercept workflow-rejected documents (checking `rejectedDocuments` Map). All other requests call `next()` to pass through to the originate proxy.
2. **`POST /api/documents`**: Changed to only intercept `requiresApproval` workflow documents. Non-workflow document creation is forwarded to the originate service via an internal HTTP call (necessary because the body stream was consumed during inspection).
3. **Sign/request, Sign, Anchor**: Mock handlers removed entirely. These endpoints are now handled by the originate service through the proxy.

### Files Modified
- `Blockchain/Dev/services/api-gateway/src/index.ts`

---

## Finding 4: Dashboard Data Path Mismatch

### Severity: MEDIUM

### Problem
The Dashboard component accessed document data via `response.data.data?.documents` but the actual API response (from both the gateway mock and the originate service) returns data at `response.data.documents`. This resulted in the Dashboard always showing zero documents and zero stats.

### Root Cause
The Dashboard was coded expecting a nested `{ data: { documents: [...] } }` response structure, likely from an older API format, while the actual response is `{ documents: [...], total, page, limit }`.

### Fix Applied
Changed the access path to `response.data?.documents || response.data?.data?.documents || []` for backward compatibility.

### Files Modified
- `Blockchain/Dev/frontend/issuer/src/components/Dashboard.tsx`

---

## Finding 5: Document ID Validation Rejecting Seed IDs

### Severity: MEDIUM

### Problem
The `DocumentDetail` component validates document IDs before making API calls. The validation regex only accepted UUIDs and `doc-{timestamp}-{shortId}` format. The seed document IDs (`doc-demo-degree-001`, etc.) were rejected as "Invalid document ID format", causing a "Document not found" error.

### Root Cause
The `documentIdSchema` in `utils/validation.ts` used:
- `/^[0-9a-f]{8}-[0-9a-f]{4}-...$/` for UUIDs
- `/^doc-\d{10,15}-[a-z0-9]{6,12}$/` for timestamp-based IDs

Neither pattern matched `doc-demo-degree-001`.

### Fix Applied
Added a third pattern: `/^doc-[a-z0-9][a-z0-9-]{2,48}[a-z0-9]$/` to accept slug-style document IDs used by seed and demo documents.

### Files Modified
- `Blockchain/Dev/frontend/issuer/src/utils/validation.ts`

---

## Finding 6: Signature and Date Field Naming Mismatch

### Severity: MEDIUM

### Problem
The `DocumentDetail` component rendered signatures using field names (`sig.signer_wallet_address`, `sig.created_at`) that did not match the originate service's response format (`sig.walletAddress`, `sig.signedAt`). This caused a `RangeError: Invalid time value` crash when `format(new Date(undefined))` was called, triggering the React error boundary.

### Root Cause
The frontend template used snake_case field names (likely from an earlier API version or mock), while the originate service returns camelCase.

### Fix Applied
Added normalisation logic in the `loadDocument` function to map between formats:
```
sig.walletAddress → sig.signer_wallet_address
sig.signedAt → sig.created_at
```
Also improved anchor normalisation to extract blockchain data (`txHash`, `anchoredAt`) into the anchors array.

### Files Modified
- `Blockchain/Dev/frontend/issuer/src/components/DocumentDetail.tsx`

---

## Finding 7: Status Configuration Missing for Backend Statuses

### Severity: LOW

### Problem
The `DocumentList` status chip configuration only included `draft`, `pending`, and `certified`. The originate service uses `pending_signature`, `signed`, `anchored`, and `revoked` as additional statuses. Documents with these statuses rendered without a status chip icon or colour.

Similarly, the "Save as NFT" button condition only checked for `certified` and `draft`, missing `signed` and `anchored`.

### Root Cause
The frontend was designed for an earlier backend that used different status names. The originate service's status enum (`draft | pending_signature | signed | anchored | revoked`) was not fully mapped in the frontend.

### Fix Applied
1. Extended `statusConfig` in `DocumentList.tsx` to include all backend statuses
2. Updated the "Save as NFT" button condition to `['certified', 'draft', 'signed', 'anchored'].includes(document.status)`
3. Updated Dashboard stats counting to include `signed` in certified count and `pending_signature` in pending count

### Files Modified
- `Blockchain/Dev/frontend/issuer/src/components/DocumentList.tsx`
- `Blockchain/Dev/frontend/issuer/src/components/DocumentDetail.tsx`
- `Blockchain/Dev/frontend/issuer/src/components/Dashboard.tsx`

---

## Finding 8: POST /documents Dual Payload Format

### Severity: LOW

### Problem
The originate service's `POST /api/documents` required `type` and `data` fields (validated by express-validator), while the frontend sends `title`, `documentType`, `contentHash`, and `description`. This mismatch caused 400 validation errors when creating documents through the frontend.

### Root Cause
The frontend was designed for a newer API format that the backend had not been updated to accept.

### Fix Applied
Updated the POST handler to accept both payload formats:
- **Legacy**: `{ type, data: { ... } }`
- **Frontend**: `{ title, documentType, contentHash, description }`

The handler auto-detects which format is being used and normalises internally.

### Files Modified
- `Blockchain/Dev/services/originate/src/routes/documents.ts`

---

## Future Work: Items Not Yet Resolved

### 1. Auth Token Persistence (Temporary localStorage Workaround)
**Severity**: MEDIUM (development only)

The frontend currently stores the access token and user data in `localStorage` to survive page reloads. This is a temporary workaround because the auth service does not set `httpOnly` refresh token cookies. In production, the backend must implement proper refresh token cookies and the frontend should use token refresh instead of localStorage.

**Current state**: `AuthContext.tsx` stores/restores from `localStorage`
**Production fix needed**: Auth service must set `httpOnly` cookies for refresh tokens

### 2. In-Memory Document Storage
**Severity**: HIGH (before production)

Documents created dynamically (not from seed) are still stored in memory and lost on restart. The originate service needs database persistence (PostgreSQL via Prisma is partially configured but not active for documents). Seed data restores only the 3 demo documents.

**Current state**: Seed data restores on restart; dynamic documents do not
**Production fix needed**: Migrate document storage from `Map` to PostgreSQL

### 3. Document Upload Flow
**Severity**: MEDIUM

The "New Document" / "Upload" flow creates documents via `FormData` POST but the originate service now expects JSON. The upload flow needs to be updated to:
1. Hash the file client-side (Web Crypto API — per SVS requirements)
2. Send only the hash and metadata as JSON

### 4. Refresh Token Flow
**Severity**: HIGH (before production)

The auth service returns refresh tokens in the JSON response body instead of setting `httpOnly` cookies. This is an XSS risk. The token refresh flow is not functional.

### 5. Real Blockchain Anchoring
**Severity**: MEDIUM

The anchor endpoint simulates blockchain anchoring with random `txHash` values. Integration with the actual Cardano blockchain via the anchoring service is pending.

---

## Verification

After applying all fixes, the following was verified:

| Test | Result |
|---|---|
| `GET /api/documents` returns seed data | PASS |
| `GET /api/documents/:id` returns full document with title, signatures, blockchain | PASS |
| `POST /api/documents` creates document in originate (not gateway mock) | PASS |
| `POST /api/documents/:id/anchor` updates status to `anchored` | PASS |
| Container restart preserves seed documents | PASS |
| Dashboard shows stats and recent documents | PASS |
| Document list shows all seed documents with correct statuses | PASS |
| Document detail renders title, hash, description, signatures, anchors | PASS |
| "Save as NFT" button visible for all non-revoked documents | PASS |
| No JavaScript console errors on Dashboard or Document pages | PASS |

---

## Files Modified (Complete List)

### Backend — Originate Service
- `Blockchain/Dev/services/originate/src/routes/documents.ts`
  - Added `seedDemoDocuments()` function
  - Added `GET /` list endpoint
  - Updated `GET /:id` response to include title, documentType, description, blockchain.anchored
  - Updated `POST /` to accept dual payload formats (legacy + frontend)

### Backend — API Gateway
- `Blockchain/Dev/services/api-gateway/src/index.ts`
  - Refactored `GET /api/documents/:id` mock to pass through to originate for non-rejected documents
  - Refactored `POST /api/documents` mock to forward non-workflow documents to originate
  - Removed mock handlers for sign/request, sign, and anchor endpoints

### Frontend — Issuer Portal
- `Blockchain/Dev/frontend/issuer/src/components/Dashboard.tsx`
  - Fixed data access path for document list
  - Updated status counting logic
- `Blockchain/Dev/frontend/issuer/src/components/DocumentList.tsx`
  - Extended statusConfig for all backend statuses
- `Blockchain/Dev/frontend/issuer/src/components/DocumentDetail.tsx`
  - Added signature field normalisation
  - Added anchor normalisation from blockchain data
  - Updated "Save as NFT" button condition
- `Blockchain/Dev/frontend/issuer/src/utils/validation.ts`
  - Extended document ID validation to accept slug-style IDs

---

## References

### Internal Links
- [[Projects Documents/Secuura-Usability-Test-Report-Feb17]] — Usability and browser test report
- Originate service source: `Blockchain/Dev/services/originate/src/routes/documents.ts`
- API gateway source: `Blockchain/Dev/services/api-gateway/src/index.ts`
- Issuer frontend source: `Blockchain/Dev/frontend/issuer/src/`
