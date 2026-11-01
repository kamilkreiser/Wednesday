---
title: Secuura Architecture Reference
created: 27-02-2026
updated: 23-06-2026
tags: [reference/architecture, reference/developer]
status: active
---

# Secuura Architecture Reference

## Summary

This document describes the complete system architecture of the Secuura Verification System (SVS) as it stands today. It covers all 20+ microservices, 5 frontend portals, the nginx gateway, the API gateway, data storage, authentication flows, and recent changes from the P1-P5 hardening work.

**Key Points:**
- Monorepo with 20+ backend services behind a single API gateway
- 5 frontend portals served through an nginx reverse proxy on port 6882
- PostgreSQL for persistent storage, Redis for caching/sessions/settings
- Cardano blockchain for anchoring, NFTs, DIDs, staking, and governance

---

## Table of Contents

- [System Architecture Diagram](#system-architecture-diagram)
- [Service Inventory](#service-inventory)
- [API Gateway Routing](#api-gateway-routing)
- [Nginx Gateway](#nginx-gateway)
- [Frontend Applications](#frontend-applications)
- [Data Flow Diagrams](#data-flow-diagrams)
- [Storage Architecture](#storage-architecture)
- [Authentication Architecture](#authentication-architecture)
- [Recent Changes (P1-P5 Fixes)](#recent-changes-p1-p5-fixes)

---

## System Architecture Diagram

```mermaid
graph TB
    subgraph "Client Layer"
        Browser["Browser / Mobile"]
    end

    subgraph "Gateway Layer (Port 6882)"
        NGINX["nginx-gateway<br/>(reverse proxy)"]
    end

    subgraph "Frontend Applications"
        IssuerFE["Issuer Portal<br/>React + MUI"]
        VerifierFE["Verifier Portal<br/>React + MUI"]
        AdminFE["Admin Portal<br/>React + MUI"]
        StatusFE["Status Page<br/>React"]
        WebsiteFE["Website<br/>Static"]
    end

    subgraph "API Layer"
        APIGW["API Gateway<br/>Express.js :8080"]
    end

    subgraph "Core Services"
        AUTH["Auth :4003"]
        ORIG["Originate :4000"]
        WALLET["Wallet Connector :4002"]
        ANCHOR["Anchoring :4005"]
        PRISM["PRISM/DID :4001"]
        TS["Timestamping :4004"]
        SEC["Security :4008"]
    end

    subgraph "Integration Services"
        KYC["KYC :4011"]
        M365["M365 Integration :4013"]
        MIDNIGHT["Midnight ZKP :4012"]
        ANALYTICS["Analytics :4010"]
        VC["VC Issuer :4014"]
        NFT["NFT Certificate :4018"]
    end

    subgraph "Business Services"
        STAKING["Staking :4015"]
        REFERRAL["Referral :4016"]
        GOV["Governance :4017"]
        BILLING["Billing :4019"]
        TRANSFER["Transfer :4020"]
    end

    subgraph "Phase 2 (Disabled)"
        GUARDIAN["Guardian :4006"]
        QUEUE["Queue :4007"]
    end

    subgraph "Infrastructure"
        PG["PostgreSQL :5432"]
        REDIS["Redis :6379"]
        PGBOUNCER["PgBouncer :6432"]
    end

    subgraph "Blockchain"
        CARDANO["Cardano Network<br/>(devnet/preprod/mainnet)"]
        BLOCKFROST["Blockfrost API"]
        KOIOS["Koios API"]
    end

    Browser --> NGINX
    NGINX --> IssuerFE
    NGINX --> VerifierFE
    NGINX --> AdminFE
    NGINX --> StatusFE
    NGINX --> WebsiteFE
    NGINX --> APIGW

    APIGW --> AUTH
    APIGW --> ORIG
    APIGW --> WALLET
    APIGW --> ANCHOR
    APIGW --> PRISM
    APIGW --> TS
    APIGW --> SEC
    APIGW --> KYC
    APIGW --> M365
    APIGW --> MIDNIGHT
    APIGW --> ANALYTICS
    APIGW --> VC
    APIGW --> NFT
    APIGW --> STAKING
    APIGW --> REFERRAL
    APIGW --> GOV
    APIGW --> BILLING
    APIGW --> TRANSFER

    AUTH --> PG
    AUTH --> REDIS
    ORIG --> PG
    ORIG --> REDIS
    APIGW --> PG
    APIGW --> REDIS
    ANCHOR --> BLOCKFROST
    ANCHOR --> CARDANO
    NFT --> BLOCKFROST
    STAKING --> BLOCKFROST
    PRISM --> CARDANO
    GOV --> CARDANO

    PGBOUNCER --> PG
```

---

## Service Inventory

### Infrastructure

| Service | Container | Internal Port | External Port | Database | Redis | Profile | Status |
|---------|-----------|--------------|---------------|----------|-------|---------|--------|
| PostgreSQL 15 | secuura-postgres | 5432 | 6432 | Primary DB | - | default | Active |
| Redis 7 | secuura-redis | 6379 | 6379 | - | Primary cache | default | Active |
| PgBouncer | secuura-pgbouncer | 6432 | 6433 | Connection pool | - | production | Staging/Prod |
| Grafana (observability) | secuura-obs-grafana | 3000 | 3000 | - | - | observability (standalone) | Optional |
| Prometheus (observability) | secuura-obs-prometheus | 9090 | 9090 | - | - | observability (standalone) | Optional |
| Loki | secuura-obs-loki | 3100 | 3100 | - | - | systemTest/observability | Optional |
| Grafana Alloy | secuura-obs-alloy | 12345 | 12345 | - | - | systemTest/observability | Optional |

### Core Services (Phase 1)

| Service | Container | Port (Internal) | Port (External) | DB | Redis | Functionality |
|---------|-----------|-----------------|-----------------|-----|-------|---------------|
| API Gateway | secuura-api-gateway | 8080 | (via nginx) | Yes | Yes | Central routing, rate limiting, auth middleware, local CRUD handlers |
| Originate | secuura-originate | 4000 | 6000 | Yes | Yes | Document creation and origination |
| Auth | secuura-auth | 4003 | 6003 | Yes | Yes | Login, register, JWT, MFA, password reset, sessions |
| Wallet Connector | secuura-wallet-connector | 4002 | 6002 | Yes | Yes | CIP-30 wallet connection, signing |
| Anchoring | secuura-anchoring | 4005 | 6005 | Yes | Yes | Blockchain hash anchoring |
| PRISM | secuura-prism | 4001 | 6001 | Yes | Yes | DID creation and resolution |
| Timestamping | secuura-timestamping | 4004 | 6004 | Yes | Yes | RFC-3161, OTS, blockchain timestamps |
| Security | secuura-security | 4008 | 6008 | Yes | Yes | Audit logging, security scanning |

### Integration Services (Phase 2-4)

| Service | Container | Port (Internal) | Port (External) | DB | Redis | Functionality |
|---------|-----------|-----------------|-----------------|-----|-------|---------------|
| KYC | secuura-kyc | 4011 | 6011 | Yes | Yes | Identity verification (Microsoft, mock) |
| M365 Integration | secuura-m365-integration | 4013 | 6013 | Yes | Yes | Microsoft 365 / SharePoint / Entra ID |
| Midnight | secuura-midnight | 4012 | 6012 | Yes | Yes | Zero-knowledge proofs (mock mode) |
| Analytics | secuura-analytics | 4010 | 6010 | Yes | Yes | Platform analytics (mock data) |
| VC Issuer | secuura-vc-issuer | 4014 | 6014 | Yes | Yes | W3C Verifiable Credentials |
| NFT Certificate | secuura-nft-certificate | 4018 | 6018 | Yes | Yes | NFT minting recording, verification |

### Business Services (Phase 3-5)

| Service | Container | Port (Internal) | Port (External) | DB | Redis | Functionality |
|---------|-----------|-----------------|-----------------|-----|-------|---------------|
| Staking | secuura-staking | 4015 | 6015 | Yes | Yes | Token staking and rewards |
| Referral | secuura-referral | 4016 | 6016 | Yes | Yes | Referral programme management |
| Governance | secuura-governance | 4017 | 6017 | Yes | Yes | DAO proposal voting |
| Billing | secuura-billing | 4019 | 6019 | Yes | Yes | Stripe integration, chargeable events |
| Transfer | secuura-transfer | 4020 | 6020 | Yes | Yes | Document transfer and ownership |

### Phase 2 (Disabled by Default)

| Service | Container | Port | Profile | Description |
|---------|-----------|------|---------|-------------|
| Guardian | secuura-guardian | 4006/6006 | phase2 | Guardian node management |
| Queue | secuura-queue | 4007/6007 | phase2 | Job queue processing |

### Blockchain (Optional Profiles)

| Service | Container | Ports | Profile | Description |
|---------|-----------|-------|---------|-------------|
| Cardano DevNet | secuura-cardano-devnet | 6091, 6092, 6093 | devnet | Yaci DevKit local network |
| Cardano Mock | secuura-cardano-mock | 6090 | mock | Nginx-based mock API |

---

## API Gateway Routing

The API gateway (`services/api-gateway/src/index.ts`) serves as the central entry point for all API requests. It handles requests in two modes:

### Local Handlers (Direct Responses)

Routes processed directly within the API gateway with PostgreSQL/Redis storage:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/api/auth/login` | No | Login (proxied to auth service) |
| `POST` | `/api/auth/register` | No | Registration (proxied to auth service) |
| `POST` | `/api/auth/refresh` | No | Token refresh (proxied to auth service) |
| `POST` | `/api/auth/password/forgot` | No | Password reset request |
| `POST` | `/api/auth/password/reset-request` | No | Password reset alias |
| `GET` | `/api/admin/document-types` | Admin | List document types (Redis) |
| `POST` | `/api/admin/document-types` | Admin | Create document type (Redis) |
| `GET` | `/api/admin/document-types/:id` | Admin | Get document type (Redis) |
| `PUT` | `/api/admin/document-types/:id` | Admin | Update document type (Redis) |
| `DELETE` | `/api/admin/document-types/:id` | Admin | Delete document type (Redis) |
| `GET` | `/api/admin/workflows` | Admin | List workflows (Redis) |
| `POST` | `/api/admin/workflows` | Admin | Create workflow (Redis) |
| `PUT` | `/api/admin/workflows/:id` | Admin | Update workflow (Redis) |
| `DELETE` | `/api/admin/workflows/:id` | Admin | Delete workflow (Redis) |
| `GET` | `/api/admin/verification-queue` | Admin | List verification items |
| `POST` | `/api/admin/verification-queue/:id/action` | Admin | Queue item action (approve/reject/escalate/assign) |
| `GET` | `/api/admin/settings` | Admin | Get platform settings (Redis) |
| `PUT` | `/api/admin/settings` | Admin | Update platform settings (Redis) |
| `GET` | `/api/admin/audit-logs` | Admin | Audit log entries (PostgreSQL) |
| `GET` | `/api/security/audit` | Admin | Alias for audit logs |
| `GET` | `/api/admin/identity/users` | Admin | List identity users (PostgreSQL) |
| `POST` | `/api/admin/identity/users` | Admin | Create identity user |
| `GET` | `/api/admin/organizations` | Admin | List organisations (PostgreSQL) |
| `POST` | `/api/admin/organizations` | Admin | Create organisation |
| `GET` | `/api/admin/documents/by-type/:typeId` | Admin | Documents by type |
| `GET` | `/api/admin/verification-policies` | Admin | List verification policies (Redis) |
| `POST` | `/api/admin/verification-policies` | Admin | Create policy |
| `GET` | `/api/admin/third-party-verifiers` | Admin | List providers |
| `POST` | `/api/admin/third-party-verifiers` | Admin | Create provider |
| `GET` | `/api/settings/notifications` | Optional | Notification settings (Redis) |
| `PUT` | `/api/settings/notifications` | Optional | Update notification settings |
| `GET` | `/api/privacy/settings` | Optional | Privacy settings (Redis) |
| `PUT` | `/api/privacy/settings` | Optional | Update privacy settings |
| `POST` | `/api/verification/verify` | No | Public document verification |

### Proxied Routes

Routes forwarded to downstream microservices via `http-proxy-middleware`:

| Path Pattern | Target Service | Auth Required |
|-------------|----------------|---------------|
| `/api/auth/*` | Auth Service (:4003) | No |
| `/api/users/*` | Auth Service (:4003) | Yes |
| `/api/originate/*` | Originate Service (:4000) | Yes |
| `/api/documents/*` | Originate Service (:4000) | Yes |
| `/api/wallet/*` | Wallet Connector (:4002) | Yes |
| `/api/anchors/*`, `/api/anchoring/*` | Anchoring Service (:4005) | Yes |
| `/api/timestamps/*` | Timestamping Service (:4004) | Yes |
| `/api/did/*` | PRISM Service (:4001) | Yes |
| `/api/security/*` | Security Service (:4008) | Yes |
| `/api/m365/*` | M365 Integration (:4013) | Yes |
| `/api/kyc/*` | KYC Service (:4011) | Yes |
| `/api/midnight/*`, `/api/proofs/*`, `/api/circuits/*`, `/api/commitments/*`, `/api/disclosure/*`, `/api/private/*` | Midnight (:4012) | Mixed |
| `/api/credentials/*`, `/api/presentations/*`, `/api/status/*` | VC Issuer (:4014) | Yes |
| `/api/analytics/*` | Analytics (:4010) | Yes |
| `/api/staking/*`, `/api/rewards/*`, `/api/pool/*` | Staking (:4015) | Yes |
| `/api/referral/*` | Referral (:4016) | Yes |
| `/api/governance/*` | Governance (:4017) | Yes |
| `/api/nft/*` | NFT Certificate (:4018) | Yes |
| `/api/billing/*` | Billing (:4019) | Yes |
| `/api/transfer/*` | Transfer (:4020) | Yes |

---

## Nginx Gateway

The nginx reverse proxy (`docker/nginx-gateway/nginx.conf`) provides a unified entry point on port 6882.

### Routing Rules

| Path | Upstream | Description |
|------|----------|-------------|
| `/` | `issuer-frontend:80` | Issuer Portal (default/catch-all) |
| `/verify/` | `verifier-frontend:80` | Verifier Portal |
| `/admin/` | `admin-frontend:80` | Admin Dashboard |
| `/status/` | `status-frontend:80` | System Status Page |
| `/website/` | `website-frontend:80` | Marketing Website |
| `/api/` | `api-gateway:8080` | API Gateway |
| `/originate/` | `originate:4000` | Originate Service (direct) |
| `/analytics/` | `analytics:4010` | Analytics Service (direct) |
| `/system/` | `api-gateway:8080` | System status aggregation |
| `/showcase/` | Static files | Demo recording title cards |
| `/health` | Static JSON | Gateway health check |

### Security Headers

All responses include:
- `X-Frame-Options: SAMEORIGIN`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

### HTTPS (Production)

HTTPS is configured but commented out. To enable:
1. Mount TLS certificates at `/etc/nginx/ssl/cert.pem` and `/etc/nginx/ssl/key.pem`
2. Set `ENABLE_HTTPS=true`
3. Uncomment the HTTPS server block in `nginx.conf`
4. Enables TLSv1.2/1.3, HSTS with 2-year max-age, and CSP headers

---

## Frontend Applications

| Portal | URL (via Gateway) | Direct URL | Framework | Build Tool | Key Environment Variables |
|--------|-------------------|------------|-----------|------------|--------------------------|
| **Issuer Portal** | `http://localhost:6882/` | N/A (nginx only) | React + MUI + TypeScript | Vite | `VITE_API_URL`, `VITE_CARDANO_NETWORK` |
| **Verifier Portal** | `http://localhost:6882/verify/` | N/A | React + MUI + TypeScript | Vite | `VITE_API_URL` |
| **Admin Portal** | `http://localhost:6882/admin/` | N/A | React + MUI + TypeScript | Vite | `VITE_API_URL`, `VITE_ORIGINATE_URL`, `VITE_ANALYTICS_URL` |
| **Status Page** | `http://localhost:6882/status/` | N/A | React + TypeScript | Vite | None |
| **Marketing Website** | `http://localhost:6882/website/` | `http://localhost:6881` | Static HTML/CSS/JS | None | None |
| **Tokenomics Website** | N/A | `http://localhost:8881` | Static | Docker | None |

---

## Data Flow Diagrams

### Document Certification Lifecycle

```mermaid
sequenceDiagram
    participant Issuer as Issuer (Browser)
    participant IssuerFE as Issuer Portal
    participant APIGW as API Gateway
    participant Originate as Originate Service
    participant Anchoring as Anchoring Service
    participant Cardano as Cardano Network

    Issuer->>IssuerFE: Select document
    IssuerFE->>IssuerFE: Hash document (SHA-256, client-side)
    IssuerFE->>APIGW: POST /api/documents {hash, metadata}
    APIGW->>Originate: Forward request
    Originate->>Originate: Store document record
    Originate-->>APIGW: Document created
    APIGW-->>IssuerFE: {documentId}

    IssuerFE->>APIGW: POST /api/anchors {documentId, hash}
    APIGW->>Anchoring: Forward request
    Anchoring->>Anchoring: Build Cardano transaction
    Anchoring->>Cardano: Submit transaction (via Blockfrost)
    Cardano-->>Anchoring: Transaction hash
    Anchoring-->>APIGW: {txHash, blockHeight}
    APIGW-->>IssuerFE: Anchor confirmed
```

### Verification Flow

```mermaid
sequenceDiagram
    participant Verifier as Verifier (Browser)
    participant VerifierFE as Verifier Portal
    participant APIGW as API Gateway
    participant Cardano as Cardano Network

    Verifier->>VerifierFE: Upload document or enter ID
    VerifierFE->>VerifierFE: Hash document (SHA-256, client-side)
    VerifierFE->>APIGW: POST /api/verification/verify {documentHash or documentId}
    APIGW->>APIGW: Lookup document by hash/ID
    APIGW->>APIGW: Find anchor transaction
    APIGW-->>VerifierFE: {verified, certifier, anchor, blockchain}
    VerifierFE->>Verifier: Display verification result
```

### NFT Minting Flow

```mermaid
sequenceDiagram
    participant User as Issuer (Browser)
    participant FE as Issuer Portal
    participant Wallet as CIP-30 Wallet
    participant APIGW as API Gateway
    participant NFT as NFT Service
    participant Cardano as Cardano

    User->>FE: Click "Mint NFT Certificate"
    FE->>FE: Build transaction (MeshSDK)
    FE->>Wallet: Request signature (CIP-30)
    Wallet-->>FE: Signed transaction
    FE->>Cardano: Submit transaction (via Blockfrost)
    Cardano-->>FE: Transaction hash
    FE->>APIGW: POST /api/nft/record {txHash, policyId, assetName}
    APIGW->>NFT: Forward recording
    NFT-->>APIGW: NFT certificate created
    APIGW-->>FE: {certificateId}
```

---

## Storage Architecture

### PostgreSQL

Primary relational database used by most services. Key tables (managed by each service's migrations):

| Owner Service | Table(s) | Purpose |
|---------------|----------|---------|
| Auth | `users`, `sessions`, `email_tokens`, `refresh_tokens`, `mfa_settings` | User accounts and authentication |
| Originate | `documents`, `document_events`, `document_access` | Document records and provenance |
| API Gateway | `organizations`, `svc_gateway_workflows`, `svc_gateway_rejections`, `svc_gateway_signatures`, `audit_logs` | Organisations, workflow state, audit trail |
| Anchoring | `anchors`, `anchor_batches` | Blockchain anchor records |
| Security | `security_events`, `audit_entries` | Security audit log |
| VC Issuer | `credentials`, `status_lists`, `presentations` | Verifiable Credentials |
| PRISM | `dids`, `did_documents` | Decentralised Identifiers |

**Connection:** `postgresql://secuura:secuura_dev_password@postgres:5432/secuura` (dev defaults)

### Redis

Used for caching, session management, and key-value storage:

| Prefix/Pattern | Owner | Purpose |
|----------------|-------|---------|
| `doc_types:*` | API Gateway | Document type definitions |
| `workflows:*` | API Gateway | Workflow definitions |
| `workflow_instances:*` | API Gateway | Active workflow instances |
| `pending_docs:*` | API Gateway | Pending document submissions |
| `verification_policies:*` | API Gateway | Verification policy configs |
| `settings:notifications:*` | API Gateway | User notification preferences |
| `settings:privacy:*` | API Gateway | User privacy preferences |
| `admin:settings` | API Gateway | Platform-wide admin settings |
| `session:*` | Auth Service | Active user sessions |
| `rate_limit:*` | API Gateway | Rate limiting counters |

**Connection:** `redis://:secuura_redis_dev@redis:6379` (dev defaults)

### In-Memory Stores

Several services use in-memory Maps as primary storage (flagged for database migration):

| Service | Store | Purpose | Migration Priority |
|---------|-------|---------|-------------------|
| API Gateway | `memWorkflowToDocumentMap` | Workflow-document mapping | Medium (DB fallback exists) |
| API Gateway | `memRejectedDocuments` | Rejected document state | Medium (DB fallback exists) |
| API Gateway | `memDocumentSignatures` | Document signatures | Medium (DB fallback exists) |
| KYC | `memVerifications`, `memConsents` | KYC verification state | High |
| M365 | `memConnections`, `memSites` | SharePoint connections | High |
| Timestamping | `timestamps`, `timestampsByDocument` | Timestamp records | High |
| NFT Certificate | `memNftCertificates` | NFT mint records | High |
| Referral | Multiple Maps | Referral programme data | High |
| Billing | `chargeEvents` | Chargeable event log | High |

---

## Authentication Architecture

### JWT Token Flow

```mermaid
sequenceDiagram
    participant Client as Browser
    participant APIGW as API Gateway
    participant Auth as Auth Service

    Client->>APIGW: POST /api/auth/login {email, password}
    APIGW->>Auth: Proxy login request
    Auth->>Auth: Verify credentials (bcrypt)
    Auth->>Auth: Check MFA requirement
    Auth->>Auth: Generate JWT pair (access + refresh)
    Auth-->>APIGW: {accessToken, refreshToken, user}
    APIGW-->>Client: Set httpOnly refresh cookie + return access token

    Note over Client: Access token stored in memory (not localStorage)
    Note over Client: Refresh token in httpOnly cookie

    Client->>APIGW: GET /api/documents (Authorization: Bearer <access>)
    APIGW->>APIGW: authenticateToken middleware verifies JWT
    APIGW->>APIGW: Attach user payload to request
    APIGW->>Auth: Proxy to target service
```

### Token Configuration

| Parameter | Value |
|-----------|-------|
| Access token lifetime | Configurable via `JWT_EXPIRES_IN` (default: `1d`) |
| Refresh token | Stored in httpOnly cookie |
| Algorithm | RS256 (RSA-SHA256, asymmetric) — RS256-only since KS-167/184/302; HS256 dropped |
| Keys | `JWT_PRIVATE_KEY` (auth signs) + `JWT_PUBLIC_KEY` (verifiers, fail-closed if missing) + `JWT_KEY_ID`; no shared secret |

### Authentication Middleware

Two middleware functions in the API gateway:

- **`authenticateToken(required = true)`** -- Verifies JWT from `Authorization: Bearer` header. When `required = false`, allows unauthenticated access with fallback to `x-user-id` header.
- **`requireAdmin`** -- Checks that `req.user.role === 'SYSTEM_ADMIN'`. Must be chained after `authenticateToken`.

### Roles

| Role | Description | Access Level |
|------|-------------|--------------|
| `SYSTEM_ADMIN` | Platform administrator | Full access, admin portal |
| `OWNER` | Document/organisation owner | Issuer portal, own resources |
| `VERIFIER` | Third-party verifier | Verifier portal, public verification |
| `HOLDER` | Rights holder | Issuer portal, own documents |

### Wallet Authentication

CIP-30 wallet connection for blockchain operations:
1. User connects wallet via CIP-30 browser extension
2. Server generates a nonce/challenge
3. Wallet signs the challenge (CIP-8 message signing)
4. Server verifies the signature against the wallet address
5. Session is created linking wallet address to user account

> **Note:** CIP-8 signature verification currently uses a development stub. Production requires the `@emurgo/cardano-message-signing` WASM library.

---

## Recent Changes (P1-P5 Fixes)

### Priority 1 -- Critical Fixes
- Verifier portal now performs client-side SHA-256 hashing (Web Crypto API) instead of uploading files
- Added `POST /api/admin/verification-queue/:id/action` for queue item management
- Added `GET/PUT /api/admin/settings` for platform settings (Redis-backed)
- Added `GET /api/security/audit` as alias for audit logs
- Added optional auth to notification and privacy settings endpoints

### Priority 2 -- Functional Fixes
- Admin profile page: error handling and change password flow
- Users page: block/unblock functionality wired to API
- Verification queue: verifier assignment dialog with dynamic user list
- Privacy preferences: blocked entity removal
- Report viewer: share button using Web Share API
- Activity feed: "More" menu with refresh and clear options
- Billing dashboard: pricing tier checkout flow
- DocumentTypeDetail: activity tab fetches real audit logs

### Priority 3 -- Mock Data Cleanup
- Removed "Test NFT Flow" debug button from issuer dashboard
- Gated dev simulation button behind `import.meta.env.DEV`
- Replaced hardcoded mock signature with dynamic placeholder
- Removed explicit mock context injection from approval queue

### Priority 4 -- Auth and UX Hardening
- Added auth headers to analytics dashboard, governance dashboard, and export dialog API calls
- Added copy-to-clipboard confirmation in verifier result page
- Fixed CardanoScan link conditional rendering (no "undefined" URLs)
- Fixed error boundary home navigation to respect React Router basename

### Priority 5 -- Polish
- Audit logs endpoint now handles `resourceType` and `offset` parameters
- Standardised API response format (`{ success: true, ...data }`) across 10+ endpoints
- Improved WalletSelector EVM tab with roadmap messaging
- LineageViewer demo data gated behind missing `certificationId`

---

## References

### Internal Links
- Secuura Crypto and Blockchain Developer Reference
- Secuura Security Reference
- Secuura Mock Data Audit

### External Links
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Express.js](https://expressjs.com/)
- [Material-UI](https://mui.com/)
- [Vite](https://vitejs.dev/)
