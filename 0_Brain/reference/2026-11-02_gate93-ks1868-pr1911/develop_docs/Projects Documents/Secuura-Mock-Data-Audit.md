---
title: Secuura Mock Data and Placeholder Audit
created: 27-02-2026
updated: 27-02-2026
tags: [audit/mock-data, reference/production-readiness]
status: active
---

# Secuura Mock Data and Placeholder Audit

## Summary

This document is the definitive audit of every mock, placeholder, stub, and in-memory store in the Secuura codebase. It is categorised by production impact severity to guide the order in which items must be addressed before production deployment.

**Key Points:**
- 50+ in-memory Map stores across services, all requiring database migration for production
- Analytics service generates entirely random data via `randomInt()`/`randomFloat()`
- 7 files in the admin `__mocks__/` directory providing fallback data
- Properly gated demo features (behind environment variables or `import.meta.env.DEV`)
- 1 critical production TODO: CIP-8 signature verification stub

---

## Table of Contents

- [Critical -- Must Replace for Production](#critical----must-replace-for-production)
- [High -- In-Memory Stores Need Database Migration](#high----in-memory-stores-need-database-migration)
- [Medium -- Mock Modes (Properly Gated)](#medium----mock-modes-properly-gated)
- [Low -- Legitimate Dev/Demo Features](#low----legitimate-devdemo-features)
- [Production TODOs Identified in Code](#production-todos-identified-in-code)
- [Summary Statistics](#summary-statistics)

---

## Critical -- Must Replace for Production

### 1. Analytics Service Returns Random Data

**File:** `services/analytics/src/services/analyticsService.ts`

The entire analytics service generates fake metrics using `randomInt()` and `randomFloat()` helper functions. No real data is collected or aggregated.

| Line Range | Mock Content |
|-----------|-------------|
| L27-33 | `randomInt()` and `randomFloat()` utility functions |
| L89 | `generateMockActivity()` called in constructor |
| L104-140 | Mock user, organisation, certification, verification, blockchain, and privacy metrics |
| L159-205 | Mock certification totals, breakdown by type, top issuers (hardcoded names), time series |
| L218-266 | Mock verification totals, top verifiers (hardcoded names), performance metrics |
| L286-314 | Mock governance proposals, voting metrics, categories, top voters (hardcoded names) |
| L334-383 | Mock revenue metrics, revenue by tier, churn metrics, hardcoded cohort data |
| L396-444 | Mock user totals, counts, roles breakdown, activity/engagement metrics, users by region |
| L457-470 | Mock real-time metrics and system health |
| L502-540 | `generateMockActivity()` function with hardcoded event generation |

**Impact:** All analytics dashboards (admin and issuer portals) display fabricated numbers.

**Fix Required:** Connect to real data pipeline using PostgreSQL aggregation queries across service databases.

---

### 2. Referral Leaderboard -- Hardcoded Mock Users

**File:** `services/referral/src/routes/leaderboard.ts`

| Line Range | Content |
|-----------|---------|
| L249-280 | Hardcoded `mockEntries` array with 3 users: `CryptoKing`, `BlockchainPro`, `SecuuraFan` |
| L69 | Comment: "Rebuild leaderboard (in production, this would query database)" |
| L242 | Comment: "In production, this would be a database query" |

**Impact:** Leaderboard shows fake users and scores.

**Fix Required:** Replace with PostgreSQL query of actual referral data.

---

### 3. Admin Frontend `__mocks__/` Directory

**Directory:** `frontend/admin/src/__mocks__/`

7 files providing fallback mock data for the admin portal:

| File | Content |
|------|---------|
| `dashboardData.ts` | Dashboard statistics and charts |
| `integrationData.ts` | 4 demo integrations (`[Demo] SharePoint`, `[Demo] Entra ID`, `[Demo] Onfido KYC`, `[Demo] AWS S3`) |
| `verificationQueueData.ts` | Verification queue items |
| `documentTypesData.ts` | Document type definitions |
| `workflowData.ts` | Workflow definitions |
| `reportsData.ts` | Report data |
| `index.ts` | Barrel export for all mock modules |

**Impact:** Admin portal falls back to these mock datasets when API calls fail or return empty results. Some pages import mock data directly as initial state.

**Fix Required:** Ensure all admin pages fetch from real API endpoints and handle empty states gracefully. Remove mock imports from production builds.

---

### 4. Placeholder Password Hash for Seeded Identity Users

**File:** `services/api-gateway/src/index.ts` (L2179)

```
'$2b$10$placeholder'
```

Used when creating seeded identity users in the admin identity management endpoint.

**Impact:** Users created via seed have an invalid password hash that cannot be verified via bcrypt. They cannot log in via password.

**Fix Required:** Generate real bcrypt hashes at seed time or remove seeded identity users from production.

---

## High -- In-Memory Stores Need Database Migration

All of the following services use in-memory `Map` objects as their primary data store. Data is lost on container restart.

### KYC Service

**File:** `services/kyc/src/index.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L133 | `memVerifications` | KYC verification records |
| L134 | `memVerificationsByUser` | User-to-verification mapping |
| L135 | `memConsents` | User consent records |
| L136 | `memUploadedImages` | Uploaded verification images |

---

### M365 Integration Service

**File:** `services/m365-integration/src/index.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L97 | `memConnections` | SharePoint/M365 connections |
| L98 | `memSites` | SharePoint sites |
| L99 | `memSyncedDocuments` | Synced document records |

---

### Timestamping Service

**File:** `services/timestamping/src/index.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L57-59 | `timestamps`, `timestampsByDocument`, `timestampsByUser` | All timestamp records |

---

### NFT Certificate Service

**File:** `services/nft-certificate/src/services/minting.service.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L35 | `memNftCertificates` | NFT certificate records |
| L36 | `certificationCache` | Certification data cache |

---

### Referral Service (Multiple Files)

**Files:**
- `services/referral/src/services/fraudDetection.ts` (L65-68) -- 4 Maps for fraud detection
- `services/referral/src/services/milestoneService.ts` (L101-102) -- `memUserProgress`, `memRewardsPending`

---

### Billing Service

**File:** `services/billing/src/chargeable-events.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L102 | `chargeEvents: Map<string, ChargeEvent>` | All chargeable event records |

---

### Transfer Service

**File:** `services/transfer/src/index.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L145 | `memTransfers` | Transfer records |
| L146 | `memTransfersByDocument` | Document-to-transfer mapping |
| L147 | `memTransfersByOwner` | Owner-to-transfer mapping |
| L148 | `memNotifications` | Transfer notifications |

---

### Governance Service

**File:** `services/governance/src/services/governanceService.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L34-36 | `memProposals`, `memParticipants`, `memDelegations` | DAO governance state |

---

### Staking Service

**File:** `services/staking/src/routes/stake.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L61 | `stakePositions` | User stake positions |

---

### Midnight Service (Multiple Files)

**Files:**
- `services/midnight/src/index.ts` (L160-161) -- `memProofs`, `memCommitments`
- `services/midnight/src/services/privacyPreferencesService.ts` (L26-28) -- Privacy preference Maps
- `services/midnight/src/services/selectiveDisclosure.ts` (L29-31) -- Selective disclosure Maps
- `services/midnight/src/services/privateStateService.ts` (L27, L30) -- `shieldedDocuments`, `unshieldedDocuments`

---

### VC Issuer Service

**Files:**
- `services/vc-issuer/src/routes/presentations.ts` (L58) -- `memPresentationStore`
- `services/vc-issuer/src/routes/status.ts` (L24) -- `statusListManagers`

---

### Auth Service (Fallback)

**Files:**
- `services/auth/src/repositories/userRepo.ts` (L19-20, L484-485) -- `memUsers`, `memUsersByEmail`, `memResetTokens`, `memEmailTokens`
- `services/auth/src/services/session.ts` (L65-66) -- `memSessions`, `memUserSessions`
- `services/auth/src/routes/wallet.ts` (L39) -- `memChallenges`
- `services/auth/src/routes/users.ts` (L362) -- `memVerificationRequests`
- `services/auth/src/routes/mfa.ts` (L33) -- `pendingSetups`

> **Note:** Auth service Maps serve as fallbacks when PostgreSQL is unavailable. The primary storage path uses the database.

---

### Originate Service

**Files:**
- `services/originate/src/repositories/certificationRepo.ts` (L49-50) -- `memCertifications`, `memShareRecords`
- `services/originate/src/routes/anchors.ts` (L30) -- `anchors` Map
- `services/originate/src/services/chargeEvents.ts` (L119) -- `memChargeEvents`

---

### Anchoring Service

**File:** `services/anchoring/src/index.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L87-88 | `anchors`, `anchorsByDocument` | Anchor records and document mapping |

---

### Analytics Service

**Files:**
- `services/analytics/src/services/metricsCollector.ts` (L42-43) -- `counters`, `gauges`
- `services/analytics/src/services/reportGenerator.ts` (L24) -- `reportStore`
- `services/analytics/src/services/analyticsService.ts` (L70) -- `memActivityFeed`

---

### API Gateway (Redis Fallbacks)

**File:** `services/api-gateway/src/services/redis.ts`

| Line | Store | Purpose |
|------|-------|---------|
| L41-48 | `bruteForce`, `rateLimit`, `workflows`, `rejectedDocs`, `workflowDocMap`, `privacy`, `trustedVerifiers`, `signatures` | Redis fallback Maps |
| L242 | `integrationStore` | Integration config storage |
| L440 | `documentTypesStore` | Document type fallback |
| L493 | `workflowInstancesStore` | Workflow instance fallback |
| L531 | `pendingDocumentsStore` | Pending document fallback |
| L564 | `verificationPoliciesStore` | Policy fallback |
| L611 | `notificationSettingsStore` | Notification settings fallback |

> **Note:** API Gateway Maps are fallbacks for when Redis is unavailable. Primary storage uses Redis.

---

## Medium -- Mock Modes (Properly Gated)

These services have mock modes controlled by environment variables and are designed to be switched to real implementations.

### PRISM Service -- Mock DID Client

- **Control:** `PRISM_MODE` environment variable
- **Modes:** `mock`, `basic`, `testnet`, `mainnet`
- **Current default:** `basic` (docker-compose)
- **Mock behaviour:** In-memory DID operations, no blockchain interaction
- **File:** `packages/shared/src/prism/mock-client.ts`

### Midnight Service -- Mock ZK Proofs

- **Control:** `MIDNIGHT_MODE` environment variable
- **Modes:** `mock`, `testnet`, `mainnet`
- **Current default:** `mock` (docker-compose)
- **Mock behaviour:** Simulated proof generation and verification, no real ZK circuits
- **File:** `services/midnight/src/index.ts`

### KYC Provider -- Mock Verification

- **Control:** `KYC_PROVIDER` environment variable
- **Modes:** `mock`, `microsoft`, `onfido`
- **Mock behaviour:** Auto-approves verification requests
- **File:** `services/kyc/src/index.ts`

### Blockchain Anchoring -- Simulated Anchors

- **Control:** Automatic when blockchain service is unavailable
- **Detection:** `simulated: true` flag on anchor records
- **Behaviour:** Creates a local anchor record without submitting to Cardano
- **File:** `services/anchoring/src/index.ts`

### Timestamping -- Mock Proofs

- **Control:** Automatic when TSA is unavailable
- **Behaviour:** Generates mock RFC-3161, OTS, and blockchain timestamp proofs
- **File:** `services/timestamping/src/index.ts`

### IPFS Provider -- Mock Storage

- **Control:** `IPFS_PROVIDER` environment variable
- **Modes:** `mock`, `pinata`, `infura`, `web3storage`
- **Current default:** `mock` (docker-compose)
- **Mock behaviour:** Returns fake CIDs without uploading to IPFS
- **File:** `services/nft-certificate/src/services/minting.service.ts`

### Stripe -- Test Mode

- **Control:** `STRIPE_MODE` environment variable
- **Modes:** `test`, `live`
- **Current default:** `test` (docker-compose)
- **Mock behaviour:** Uses Stripe test keys, no real charges

---

## Low -- Legitimate Dev/Demo Features

These are intentional development and demonstration features that are properly gated.

### Demo Credentials

| Email | Password | Role | Gate |
|-------|----------|------|------|
| `demo@secuura.io` | `demo123` | Issuer | `ENABLE_DEMO_SEED` env var |
| `admin@secuura.com` | `admin123` | Admin | `ENABLE_DEMO_SEED` env var |

**File:** `services/auth/src/repositories/userRepo.ts` (L591+)

Credentials are seeded via `seedDemoUsers()` at auth service startup. Should be disabled in production by not setting `ENABLE_DEMO_SEED`.

### Demo Documents in Originate Service

**File:** `services/originate/src/repositories/documentRepo.ts`

| Line | Document |
|------|----------|
| L340 | `[Demo] BSc Computer Science — University of Oxford` |
| L368 | `[Demo] Academic Transcript — 2022-2025` |
| L391 | `[Demo] Professional Certification — AWS Solutions Architect` |

All prefixed with `[Demo]` for easy identification. Created via `seedDemoDocuments()` at startup.

### Demo Lineage Data

**File:** `frontend/issuer/src/components/lineage/demoData.ts`

- `RECRUITMENT_DEMO` export with a full recruitment document lineage scenario
- Only shown when no `certificationId` is provided (LineageViewer `isDemo` state)
- Scenario toggle buttons only visible in demo mode

### Dev Simulation Buttons

Gated behind `import.meta.env.DEV` (only present in Vite development builds):

| Component | File | Feature |
|-----------|------|---------|
| MicrosoftVerification | `frontend/issuer/src/components/kyc/MicrosoftVerification.tsx` | "DEV: Simulate Completion" button |

### WalletConnect Mock

**Behaviour:** When `WALLETCONNECT_PROJECT_ID` is not set, WalletConnect features are disabled with a fallback message.

### NFT Service Demo Names

**File:** `services/nft-certificate/src/services/minting.service.ts`

| Line | Content |
|------|---------|
| L111 | `name: 'Secuura Demo Issuer'` (fallback issuer name) |
| L115 | `name: 'Demo Recipient'` (fallback recipient name) |

---

## Production TODOs Identified in Code

### Critical

| File | Line | TODO |
|------|------|------|
| `packages/shared/src/cardano/wallet.ts` | L251 | Replace CIP-8 signature verification with `@emurgo/cardano-message-signing` WASM library |

> The stub at L262 logs: "CIP-8 signature verification using development stub -- not suitable for production". In production mode (`NODE_ENV=production`), the function returns `false` and logs an error.

### High

| File | Location | TODO |
|------|----------|------|
| `services/staking/src/routes/rewards.ts` | L373 | `POST /api/rewards/add-mock` endpoint should be removed or gated for production |
| `docker/pgbouncer/userlist.txt` | L21-27 | Placeholder SCRAM-SHA-256 hashes need to be replaced with real credentials |

---

## Summary Statistics

| Category | Count | Production Impact |
|----------|-------|-------------------|
| **Critical items** | 4 | Must fix before any production deployment |
| **In-memory stores** | 50+ Maps across 15+ services | Data loss on restart; must migrate to DB |
| **Mock modes** | 7 services with mock/gated modes | Configurable; switch to real providers |
| **Demo features** | 5 categories (credentials, documents, lineage, dev buttons, names) | Properly gated; disable via config |
| **Production TODOs** | 3 | CIP-8 critical; staking/pgbouncer high |

### Migration Priority Order

1. **CIP-8 signature verification** -- Security critical, blocks wallet auth in production
2. **Analytics service** -- Displays entirely fabricated data to admin users
3. **Placeholder password hash** -- Blocks identity user login
4. **PgBouncer credentials** -- Security risk in production deployment
5. **In-memory stores** (by service criticality):
   - Auth service fallbacks (already has DB path)
   - Originate/Anchoring (core document flow)
   - Transfer/Billing (financial data)
   - KYC/M365 (compliance data)
   - Remaining services
6. **Referral leaderboard mock data** -- Cosmetic but misleading
7. **Admin `__mocks__/` directory** -- Ensure frontend handles empty API responses
8. **Mock staking endpoint** -- Remove `POST /api/rewards/add-mock`

---

## References

### Internal Links
- Secuura Security Reference (known security considerations section)
- Secuura Architecture Reference (storage architecture section)

### External Links
- [@emurgo/cardano-message-signing](https://www.npmjs.com/package/@emurgo/cardano-message-signing-nodejs)
