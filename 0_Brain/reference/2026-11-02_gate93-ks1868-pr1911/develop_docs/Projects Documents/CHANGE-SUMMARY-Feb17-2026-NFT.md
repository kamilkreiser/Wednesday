# Secuura Platform — NFT Wallet Flow Change Summary

**Date:** 17 February 2026
**Version:** 2.1.0
**Branch:** main
**Scope:** NFT certificate minting backend integration, code fixes, and documentation

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Backend Changes](#2-backend-changes)
3. [Frontend Changes](#3-frontend-changes)
4. [Infrastructure Changes](#4-infrastructure-changes)
5. [Bug Fixes](#5-bug-fixes)
6. [Documentation Updates](#6-documentation-updates)
7. [Configuration Changes](#7-configuration-changes)
8. [Files Modified](#8-files-modified)

---

## 1. Executive Summary

This change integrates the NFT certificate minting backend into the platform's API gateway, configures the Blockfrost preprod API key for on-chain transaction verification, and fixes several critical and medium-priority code issues in the NFT wallet flow. Documentation has been updated across the Issuer Stakeholder Guide and Stakeholder Test Guide.

**Key outcomes:**

- NFT Certificate Service now accessible via the API gateway at `/api/nft/*`
- Blockfrost preprod API key configured for on-chain transaction verification
- Critical API path bug fixed (double `/api/` prefix blocked all backend recording)
- 8 code issues resolved across frontend and backend
- Stakeholder documentation updated with full NFT minting flow
- User testing guide updated with detailed step-by-step NFT minting test scripts

---

## 2. Backend Changes

### API Gateway (`services/api-gateway/src/index.ts`)

| Change | Description |
|--------|-------------|
| Added NFT service config | New `nft` entry in `services` map pointing to `http://nft-certificate:4018` |
| Added proxy route | `/api/nft` proxy with `authenticateToken(false)` for public endpoints (tiers, chains) |
| Added to proxyPaths | `/api/nft` added to body-parsing skip list |
| Added API docs | NFT endpoints added to `/api` info response |
| Fixed governance port | Corrected governance service URL from port 4018 to 4017 |

### NFT Certificate Service (`services/nft-certificate/`)

| Change | Description |
|--------|-------------|
| Fixed default port | `server.ts` default port corrected from 4020 to 4018 |
| Enhanced RecordMintSchema | `txHash` now validates as 64-character hex string via regex |
| Added storageTier/privacyLevel to schema | `RecordMintSchema` now accepts optional `storageTier` and `privacyLevel` |
| Updated recordClientMint | Accepts and stores `storageTier` and `privacyLevel` from frontend instead of hardcoding |
| Route handler updated | `/record` endpoint now passes tier and privacy through to service |

---

## 3. Frontend Changes

### `frontend/issuer/src/utils/nftMinting.ts`

| Change | Description |
|--------|-------------|
| Fixed API path (CRITICAL) | Changed `api.post('/api/nft/record', ...)` to `api.post('/nft/record', ...)` — the `api` client already has `baseURL: '/api'`, so the previous path resulted in `http://localhost:8882/api/api/nft/record` |
| Fixed asset name length | Added 32-byte safety check using `TextEncoder` to comply with Cardano native asset name limits |
| Improved error logging | `recordMintOnBackend` now logs the actual error instead of just a message |

### `frontend/issuer/src/components/DocumentDetail.tsx`

| Change | Description |
|--------|-------------|
| Dynamic issuer name | Replaced hardcoded `'Secuura Issuer'` with dynamic lookup from document data (`document.issuer.name`, `document.issuerName`) with fallback to `'Secuura Platform'` |

---

## 4. Infrastructure Changes

### Docker Compose (`docker-compose.yml`)

| Change | Description |
|--------|-------------|
| Added BLOCKFROST_API_KEY | New environment variable for the NFT certificate container |
| Changed CARDANO_NETWORK | NFT service now defaults to `preprod` instead of `devnet` (matches Blockfrost key and Lace wallet) |

### Environment Configuration (`.env`)

| Change | Description |
|--------|-------------|
| Added BLOCKFROST_API_KEY | Preprod Blockfrost API key for on-chain verification |
| Updated CARDANO_NETWORK | Changed from `devnet` to `preprod` |

---

## 5. Bug Fixes

| # | Severity | Issue | Resolution |
|---|----------|-------|------------|
| 1 | **Critical** | Double `/api/` path in `nftMinting.ts` prevented backend recording | Changed path from `/api/nft/record` to `/nft/record` |
| 2 | **Critical** | NFT service default port was 4020 instead of 4018 | Corrected to 4018 in `server.ts` |
| 3 | **Critical** | Governance service URL pointed to port 4018 (NFT port) | Corrected to 4017 |
| 4 | **Medium** | `recordClientMint` ignored `storageTier` and `privacyLevel` from client | Now accepts and stores client-provided values |
| 5 | **Medium** | `txHash` validation accepted non-hex strings | Now validates with `/^[0-9a-fA-F]{64}$/` regex |
| 6 | **Medium** | Hardcoded issuer name in DocumentDetail | Now reads from document data dynamically |
| 7 | **Minor** | Asset name could exceed Cardano 32-byte limit | Added `TextEncoder` byte-length check with truncation |
| 8 | **Minor** | Silent error swallowing in `recordMintOnBackend` | Now logs the actual error object |
| 9 | **Critical** | `validateDocumentId` rejected `doc-{timestamp}-{id}` format (UUID-only) | Updated to accept both UUID and `doc-{timestamp}-{shortId}` formats |
| 10 | **Critical** | `DocumentDetail` crashed on missing `signatures`/`anchors` arrays | Added normalisation layer in `loadDocument` with safe defaults |

---

## 6. Documentation Updates

### Stakeholder-Guide-Issuer.md (v1.0 → v1.1)

- Added new **Section 11: NFT Certificates**
  - What Are NFT Certificates? (comparison table with standard anchoring)
  - Prerequisites (wallet, ADA balance, network)
  - Step-by-step minting guide (5 steps)
  - After Minting (Cardanoscan verification)
  - Supported wallets table
- Renumbered Sections 12–15

### Secuura-Stakeholder-Test-Guide.md (v1.0.0 → v1.1.0)

- Added **NFT Certificate Minting** row to Issuer capabilities table (Section 6)
- Added **Steps 6–6f** to Appendix C (Issuer Step-by-Step):
  - Step 6: Open certified document, click "Save as NFT"
  - Step 6a: Connect wallet (Lace)
  - Step 6b: Select storage tier (Basic/Standard/Premium)
  - Step 6c: Configure privacy level
  - Step 6d: Review and mint (with progress stages)
  - Step 6e: Verify on Cardanoscan
  - Step 6f: Close modal
- Added **Phase 3a** to cross-persona recruitment flow (Steps 15a–15e)
- Added **NFT Certificate API** to Test Environment Reference table

---

## 7. Configuration Changes

### NFT Service Environment

| Variable | Value | Purpose |
|----------|-------|---------|
| `BLOCKFROST_API_KEY` | `preprodumS...` (preprod) | On-chain transaction verification via Blockfrost API |
| `CARDANO_NETWORK` | `preprod` | Cardano network matching Blockfrost key and Lace wallet |
| `PORT` | `4018` | NFT certificate service port |

### API Gateway Routing

| Route | Target | Auth |
|-------|--------|------|
| `/api/nft/*` | `http://nft-certificate:4018/api/nft/*` | Optional (some endpoints public) |

---

## 8. Files Modified

| File | Type |
|------|------|
| `services/api-gateway/src/index.ts` | Backend — API gateway routing and service config |
| `services/nft-certificate/src/server.ts` | Backend — port fix |
| `services/nft-certificate/src/routes/nft.routes.ts` | Backend — validation and schema |
| `services/nft-certificate/src/services/minting.service.ts` | Backend — tier/privacy storage |
| `services/nft-certificate/.env` | Config — Blockfrost key |
| `frontend/issuer/src/utils/nftMinting.ts` | Frontend — API path fix, asset name safety |
| `frontend/issuer/src/components/DocumentDetail.tsx` | Frontend — dynamic issuer name, data normalisation |
| `frontend/issuer/src/utils/validation.ts` | Frontend — document ID validation fix |
| `docker-compose.yml` | Infrastructure — Blockfrost env var, network config |
| `.env` | Infrastructure — Blockfrost key, Cardano network |
| `Projects Documents/Stakeholder-Guide-Issuer.md` | Documentation — NFT section |
| `Projects Documents/Secuura-Stakeholder-Test-Guide.md` | Documentation — NFT test flow |
| `Projects Documents/CHANGE-SUMMARY-Feb17-2026-NFT.md` | Documentation — this file |

---

*End of Document*
