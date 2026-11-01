# Secuura — White Paper

**Document Authenticity on the Cardano Blockchain**

**Document Title:** Secuura Platform White Paper  
**Version:** 1.0  
**Date:** 15 February 2026  
**Classification:** Public  
**Prepared by:** Secuura Engineering

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura Engineering | Initial white paper |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Problem](#2-the-problem)
3. [The Secuura Solution](#3-the-secuura-solution)
4. [Core Concepts](#4-core-concepts)
5. [Platform Architecture](#5-platform-architecture)
6. [The Secure Verification Service (SVS)](#6-the-secure-verification-service-svs)
7. [Blockchain Integration](#7-blockchain-integration)
8. [Stakeholder Roles and Interactions](#8-stakeholder-roles-and-interactions)
9. [Use Cases](#9-use-cases)
10. [Privacy and Compliance](#10-privacy-and-compliance)
11. [Security Architecture](#11-security-architecture)
12. [Smart Contract Framework](#12-smart-contract-framework)
13. [Frontend Applications](#13-frontend-applications)
14. [Integrations and Extensibility](#14-integrations-and-extensibility)
15. [Chargeable Events and Revenue Model](#15-chargeable-events-and-revenue-model)
16. [Technology Stack](#16-technology-stack)
17. [Development Roadmap](#17-development-roadmap)
18. [Competitive Landscape](#18-competitive-landscape)
19. [Conclusion](#19-conclusion)
20. [Glossary](#20-glossary)

---

## 1. Executive Summary

Secuura is a document authenticity platform built on the Cardano blockchain. It enables organisations to certify the genuineness of documents and allows third parties to independently verify that a document has not been tampered with since its original certification. Secuura addresses the pervasive problem of document fraud, which costs the global economy an estimated $600 billion annually, by providing an immutable, blockchain-anchored proof of document authenticity.

**What Secuura does:** Secuura provides cryptographic proof that a document is genuine and unaltered. When an authorised issuer certifies a document, Secuura creates a unique cryptographic hash (fingerprint) of that document and permanently records it on the Cardano blockchain. Any subsequent attempt to verify the document compares a fresh hash against the blockchain record — any modification, however minor, will be detected.

**What Secuura is not:** Secuura is not a document storage solution, a digital signature tool, or an encryption service. It focuses exclusively on authenticity — proving a document is what it claims to be, issued by whom it claims to be issued by, and unmodified since certification.

**Key differentiators:**

- **Hash-based, document-less architecture** — Secuura never stores, transmits, or has access to original documents. Client-side hashing ensures documents never leave the user's device. This fundamentally eliminates the risk of document data breaches and simplifies compliance with data protection regulations.

- **Cardano blockchain immutability** — Certification records are anchored to the Cardano blockchain, providing a tamper-proof, publicly verifiable record that no single party can alter or delete. Cardano's proof-of-stake consensus mechanism ensures energy efficiency and low transaction costs.

- **Creator/Owner separation model** — The entity that issues a document (Creator) and the entity the document belongs to (Owner) are treated as distinct roles with different permissions. This reflects real-world document relationships — a university creates a degree, but the graduate owns and controls it.

- **Privacy-first compliance** — Full GDPR compliance including consent management, data subject request processing, right-to-erasure execution, and data portability. The hybrid on-chain/off-chain architecture ensures personal data can be managed per regulatory requirements while cryptographic proofs remain immutable.

- **Multi-level identity verification** — Five verification levels from basic email confirmation to government-issued identity checks, configurable per document type and per deployment jurisdiction.

Secuura targets organisations transitioning from legacy document management systems — universities issuing degrees, enterprises managing employment records, government agencies handling official documentation, and any sector where proving document authenticity to third parties is critical.

---

## 2. The Problem

### 2.1 The Scale of Document Fraud

Document fraud is a global challenge affecting every industry that relies on paper and digital records for critical decisions. Fraudulent academic credentials, forged employment records, counterfeit certificates, and tampered legal documents undermine trust in institutions and cause significant financial and reputational harm.

**The fundamental problem is simple:** How does a third party know that a document they have received is genuinely what it claims to be?

### 2.2 Current Solutions Are Inadequate

| Approach | Limitation |
|----------|-----------|
| **Manual verification** | Time-consuming, expensive, and error-prone. Requires contacting the issuing institution directly. |
| **Digital signatures** | Prove who signed, but not whether the underlying document is authentic or unmodified after signing. Signatures can be forged. |
| **Centralised verification databases** | Single points of failure. Can be hacked, corrupted, or discontinued. Trust depends entirely on the database operator. |
| **QR codes and holograms** | Can be copied, scanned from legitimate documents, and applied to fraudulent ones. Physical security features degrade. |
| **Email or phone confirmation** | Requires the issuer to maintain verification capacity. Not scalable. Susceptible to social engineering. |

### 2.3 The Trust Gap

There is a fundamental asymmetry in document verification. The issuer of a document has high confidence in its authenticity at the time of issuance. But that confidence degrades through the document's lifecycle:

- Copies are made
- Documents change hands
- Organisations are restructured or closed
- Records are lost, corrupted, or altered
- Verification staff change
- Systems are decommissioned

By the time a verifier (an employer, a bank, a regulator) needs to confirm authenticity, the chain of trust between the original issuance and the current moment may be broken.

### 2.4 The Blockchain Opportunity

Blockchain technology offers a unique solution to the trust gap. By recording a cryptographic fingerprint of a document at the time of certification, and doing so on an immutable, publicly accessible ledger, it creates a permanent, tamper-proof reference point. Any modification to the document — however small — produces a different fingerprint, immediately revealing tampering.

---

## 3. The Secuura Solution

### 3.1 Principles

Secuura is built on five core principles:

1. **Originator-only certification** — Only the entity that created or issued a document can certify its authenticity. This preserves the trust chain from origin.

2. **Full provenance** — Every significant action in a document's lifecycle is recorded, creating a complete chain of custody from creation to the present day.

3. **Immutable records** — Certification records on the blockchain cannot be altered, deleted, or backdated by any party, including Secuura.

4. **Privacy by design** — The platform is designed to operate without ever seeing, storing, or transmitting original documents. Only cryptographic hashes are processed.

5. **Governance-driven** — Changes to platform rules require governance approval, and meta-rules (rules about rules) are immutable, preventing unilateral policy changes.

### 3.2 How It Works

```
DOCUMENT CERTIFICATION FLOW

1. ISSUER uploads document      → Hash computed client-side (BLAKE2b-256)
   to their local browser         Document NEVER leaves the device

2. CERTIFIER signs the hash     → Cryptographic proof of certification
   with their Cardano wallet      Non-repudiable witness signature

3. Hash is ANCHORED to          → Transaction recorded on Cardano
   Cardano blockchain              Permanent, public, immutable record

4. VERIFIER uploads document    → Fresh hash computed, compared to chain
   for verification                Match = authentic, Mismatch = tampered
```

### 3.3 The Hash-Based Architecture

The most important architectural decision in Secuura is that the platform operates on hashes, not documents. When a document is certified, the following occurs:

1. The document is provided to the client-side application (browser)
2. A cryptographic hash is computed locally using BLAKE2b-256
3. Only the hash is transmitted to the Secuura backend
4. The hash is anchored to the Cardano blockchain
5. The original document is discarded from memory

This means:
- **No document data breaches** — There is no document data to breach
- **No storage costs** — No document storage infrastructure required
- **GDPR-friendly** — No personal data in documents is processed or stored
- **Tamper-evident** — Any modification to the document changes the hash
- **Universal** — Works with any file format (PDF, images, Office documents, etc.)

---

## 4. Core Concepts

### 4.1 Creator vs Owner Model

Secuura distinguishes between the entity that creates a document and the entity that owns or controls it.

| Role | Definition | Rights |
|------|------------|--------|
| **Creator (Issuer)** | Entity that creates and certifies the document | Certify authenticity, modify, revoke |
| **Owner (Rights Holder)** | Individual or entity the document belongs to | Control sharing, grant access, transfer ownership |

In most real-world scenarios, the Creator and Owner are different entities. A university (Creator) issues a degree to a graduate (Owner). An employer (Creator) issues a reference letter about an employee (Owner). A government agency (Creator) issues a licence to a professional (Owner).

This separation ensures:
- Only the Creator can certify authenticity (preserving the trust chain)
- Only the Owner can control who sees and verifies the document (preserving privacy)
- Rights can transfer without Creator approval (permissionless ownership transfer)

### 4.2 Certification Events

Every significant action in a document's lifecycle is recorded as a certification event. These events form an immutable provenance chain:

| Event | Description | Blockchain Record |
|-------|-------------|-------------------|
| **Issue** | Document first created and certified | Hash + timestamp + certifier proof |
| **Sign** | Certifier signs the document hash | Wallet signature + transaction |
| **Anchor** | Hash recorded on Cardano blockchain | Transaction hash + block number |
| **Verify** | Third party verifies document | Verification result + timestamp |
| **Share** | Owner shares certification | Share record + recipient |
| **Transfer** | Ownership changes hands | Transfer record + new owner |
| **Revoke** | Certification cancelled | Revocation reason + timestamp |

### 4.3 Chargeable Events

Certain actions are designated as chargeable events, forming the basis of Secuura's revenue model. Pricing is configurable per deployment:

| Event | Default Price (ADA) | Default Price (USD) | Typical Payer |
|-------|---------------------|---------------------|---------------|
| Certification issued | 5.0 | 2.50 | Issuer |
| Certification signed | 2.0 | 1.00 | Certifier |
| Verification (pass) | 1.5 | 0.75 | Verifier |
| Verification (fail) | 0.5 | 0.25 | Verifier |
| Document shared | 0.5 | 0.25 | Owner |
| Rights transferred | 3.0 | 1.50 | Transferor |
| Certification revoked | 1.0 | 0.50 | Certifier |

---

## 5. Platform Architecture

### 5.1 Microservices Architecture

Secuura is built as a cloud-native microservices platform with 22 services (19 backend microservices + 3 frontend portals). All services are accessible exclusively through a unified Nginx gateway — only two ports are exposed externally: **8881** (Marketing Website) and **8882** (Nginx Gateway for all applications and APIs).

| Service | Internal Port | Responsibility |
|---------|:---:|---------------|
| **API Gateway** | 8080 | Central routing, rate limiting, security headers, request sanitisation |
| **Originate** | 4000 | Document certification, hashing, GDPR compliance, chargeable events |
| **PRISM** | 4001 | Decentralised Identity (DID) management via Atala PRISM |
| **Wallet Connector** | 4002 | CIP-30 wallet integration, CIP-8 message signing |
| **Auth** | 4003 | Authentication, JWT, MFA, SSO (Entra ID, Auth0) |
| **Timestamping** | 4004 | RFC-3161 compliant timestamps |
| **Anchoring** | 4005 | Cardano blockchain transaction submission |
| **Security** | 4008 | OWASP compliance, security audit logging |
| **Analytics** | 4010 | Platform analytics and usage metrics |
| **KYC** | 4011 | Microsoft Entra Verified ID integration for identity verification |
| **Midnight** | 4012 | Zero-knowledge proof selective disclosure via Cardano Midnight |
| **M365 Integration** | 4013 | Microsoft 365 / SharePoint integration |
| **VC Issuer** | 4014 | W3C Verifiable Credentials issuance |
| **Staking** | 4015 | Token staking and reward distribution |
| **Referral** | 4016 | Referral programme management |
| **Governance** | 4017 | DAO governance, proposal management, token-weighted voting |
| **NFT Certificate** | 4018 | NFT certificate minting on Cardano |
| **Billing** | 4019 | Stripe payment integration and chargeable events |
| **Transfer** | 4020 | Document ownership transfer and delegation workflows |
| **Issuer Frontend** | 80 | Issuer Portal (served at `/` via gateway) |
| **Verifier Frontend** | 80 | Verifier Portal (served at `/verify/` via gateway) |
| **Admin Frontend** | 80 | Admin Dashboard (served at `/admin/` via gateway) |

> **Note:** All internal ports listed above are accessible only within the Docker network. External access is routed exclusively through the Nginx gateway on port 8882.

### 5.2 Hybrid On-Chain/Off-Chain Architecture

Secuura employs a hybrid storage model that balances blockchain immutability with privacy compliance:

**On-Chain (Cardano Blockchain):**
- Document hash
- Certification timestamp
- Event hash
- Issuer proof (wallet address)
- Certificate ID

**Off-Chain (Encrypted PostgreSQL Database):**
- User profiles
- Full metadata
- Access rules
- Audit logs
- Event details
- Consent records

**Why hybrid?**

| Concern | Solution |
|---------|----------|
| GDPR Right to Erasure | Personal data is off-chain and can be deleted |
| Transaction costs | Only hashes on-chain — minimal Cardano fees |
| Query performance | Fast reads from PostgreSQL; blockchain for verification |
| Privacy | Sensitive details encrypted in database |
| Immutability | Blockchain hashes prove integrity regardless of off-chain changes |

### 5.3 Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Database | PostgreSQL 15 | Primary data store with SCRAM-SHA-256 authentication |
| Cache | Redis 7 | Session storage, rate limiting, temporary state |
| Connection Pooling | PgBouncer | Database connection management for production |
| Containerisation | Docker / Docker Compose | Service orchestration and isolation |
| Reverse Proxy | Nginx | Frontend gateway (port 8882) |
| Blockchain | Cardano (Yaci DevKit for development) | Immutable certification records |

---

## 6. The Secure Verification Service (SVS)

### 6.1 Document Lifecycle

The SVS defines a structured lifecycle for document certifications:

```
DOCUMENT LIFECYCLE PHASES

Phase 1: CERTIFICATION
  Draft → Hashed → Pending Sign → Signed → Anchoring → Certified

Phase 2: VERIFICATION
  Certified → Verified (or Verification Failed)

Phase 3: RE-CERTIFICATION
  Verified → Pending Sign → Signed → Anchoring → Certified
  (Verifier becomes Certifier for next phase)

Terminal States:
  → Revoked (certification cancelled)
  → Expired (certification past expiry)
```

### 6.2 Phase Transitions

Each transition follows strict rules enforced by the platform:

| From State | To State | Required Action |
|------------|----------|-----------------|
| Draft | Hashed | Document hash computed |
| Hashed | Pending Sign | Certification request submitted |
| Pending Sign | Signed | Certifier signs with wallet |
| Signed | Anchoring | Transaction submitted to blockchain |
| Anchoring | Certified | Blockchain confirmation received |
| Certified | Verified | Verifier confirms authenticity |
| Certified | Verification Failed | Verifier's document doesn't match hash |
| Certified | Revoked | Certifier revokes certification |
| Any | Expired | Time-based expiration |

### 6.3 Document Lineage Visualisation

Secuura provides an interactive graph-based visualisation of a document's complete history:

- **Nodes** represent certification events (issuance, signing, anchoring, verification)
- **Edges** show the progression through the document lifecycle
- **Colour coding** distinguishes chargeable events, blockchain confirmations, and user actions
- **Expandable/collapsible nodes** allow drill-down into event details
- **Date-based filtering** enables historical analysis
- **Evidence panels** display blockchain transaction links and verification data

The visualisation is powered by React Flow with Dagre layout, providing an intuitive directed-graph representation of the complete provenance chain.

---

## 7. Blockchain Integration

### 7.1 Why Cardano

Secuura chose Cardano as its blockchain for several strategic reasons:

| Factor | Cardano Advantage |
|--------|-------------------|
| **Energy efficiency** | Proof-of-Stake consensus uses fraction of energy vs Proof-of-Work |
| **Low fees** | Transaction fees typically under 0.20 ADA (~$0.10) |
| **Native assets** | NFT certificates without smart contract overhead |
| **Formal verification** | Haskell-based, mathematically verifiable |
| **Metadata support** | Native transaction metadata (Label 674) for document anchors |
| **Governance** | Built-in governance framework (Project Catalyst, CIP process) |
| **Midnight sidechain** | Zero-knowledge proof selective disclosure — operational at `/api/midnight/selective-disclosure/generate` and `/verify` |

### 7.2 Anchoring Process

1. **Hash preparation** — Document hash and metadata packaged as transaction metadata
2. **Transaction construction** — Cardano transaction with metadata label 674
3. **Submission** — Transaction submitted to Cardano network via node API
4. **Confirmation** — Transaction confirmed in a block (typically 20-60 seconds)
5. **Recording** — Transaction hash and block number stored in database
6. **Verification** — Any party can verify the anchor on any Cardano explorer

### 7.3 Smart Contract Framework

Secuura's smart contracts are written in Aiken (Cardano's native smart contract language) and define:

- **Document types** — Classification of certifiable documents
- **Role permissions** — What each stakeholder role can do
- **Certification actions** — Valid certification and verification operations
- **Immutable rules** — Meta-rules that cannot be changed
- **Multi-signature governance** — Multi-party approval for rule changes

### 7.4 Network Support

| Network | Purpose | Explorer |
|---------|---------|---------|
| **Mainnet** | Production certifications | cardanoscan.io |
| **Preprod** | Pre-production testing | preprod.cardanoscan.io |
| **Preview** | Development testing | preview.cardanoscan.io |
| **Devnet** | Local development (Yaci DevKit) | Local explorer |

---

## 8. Stakeholder Roles and Interactions

### 8.1 Role Definitions

| Role | Description | Key Actions |
|------|-------------|-------------|
| **Issuer** | Organisation that initiates certification | Upload documents, create certification requests, assign certifiers |
| **Certifier** | Authorised signatory who certifies authenticity | Review requests, sign with wallet, revoke certifications |
| **Subject** | Entity the document is about | Receive notifications, view certifications, request revocation |
| **Rights Holder** | Entity that owns/controls the certification | Share certifications, transfer rights, grant access |
| **Verifier** | Third party checking authenticity | Upload document for verification, view results, receive certificates |
| **System Admin** | Platform administrator | Manage users, organisations, configuration, monitor system health |

### 8.2 User Verification Levels

Secuura implements a tiered identity verification framework:

| Level | Method | Typical Use Case |
|-------|--------|------------------|
| **Basic** | Email or SMS verification | Low-risk document access |
| **Standard** | Multi-factor authentication (TOTP) | Standard operations |
| **Enhanced** | Federated identity (Microsoft Entra ID, Auth0) | Enterprise users |
| **High** | Third-party KYC (Onfido, Jumio) | Financial documents |
| **Government** | 100-point ID check, Gov.UK Verify | Legal documents, property titles |

Verification requirements are configurable per document type, per organisation, and per deployment jurisdiction.

### 8.3 Platform User Roles

| Role | Scope | Permissions |
|------|-------|-------------|
| **OWNER** | Document-level | Full control of owned documents |
| **ISSUER_ADMIN** | Organisation-level | Prepare and submit certification requests |
| **ISSUER_APPROVER** | Organisation-level | Approve and sign certifications |
| **VERIFIER** | Platform-level | Verify certifications |
| **ORG_ADMIN** | Organisation-level | Manage organisation settings and members |
| **SYSTEM_ADMIN** | Platform-level | Full administrative access |

---

## 9. Use Cases

### 9.1 Education — Academic Credentials

**Scenario:** A university certifies a graduate's degree. The graduate later applies for employment and the employer needs to verify the qualification.

**Flow:**
1. University registrar (Issuer) uploads the degree certificate
2. University dean (Certifier) signs the certification with their wallet
3. Hash is anchored to Cardano blockchain
4. Graduate (Rights Holder) receives certification and shares with employer
5. Employer (Verifier) uploads the same document and receives instant verification

**Value:** Eliminates weeks of manual verification contact between employer and university. Provides cryptographic proof that the document is genuine and unaltered.

### 9.2 Recruitment — Employment Verification

**Scenario:** A company issues an employment reference for a departing employee. A new employer needs to verify the reference is genuine.

**Flow:**
1. HR department (Issuer) creates reference document
2. Hiring manager (Certifier) signs certification
3. Employee (Rights Holder) shares certification link with new employer
4. New employer (Verifier) verifies instantly via Secuura portal

**Value:** Prevents reference fraud. Provides instant verification without contacting previous employer.

### 9.3 Professional Certifications

**Scenario:** A professional body certifies an accountant's qualification. Clients and regulators need ongoing verification.

**Flow:**
1. Professional body (Issuer) certifies qualification
2. Certification linked to professional's account (Rights Holder)
3. Clients and regulators (Verifiers) verify qualification status in real-time
4. If qualification is revoked, blockchain record updates accordingly

### 9.4 Property and Land Titles

**Scenario:** A government agency certifies property ownership. When property is sold, the title needs to transfer securely.

**Flow:**
1. Land registry (Issuer) certifies title
2. Property owner (Rights Holder) holds certification rights
3. On sale, rights transfer to buyer via permissionless transfer
4. Buyer's bank (Verifier) verifies title authenticity

### 9.5 Product Authenticity

**Scenario:** A manufacturer certifies the authenticity of luxury goods. Buyers need to verify products are genuine.

**Flow:**
1. Manufacturer (Issuer) creates product certificate
2. QR code linked to certification record
3. Buyer (Verifier) scans QR code to verify authenticity
4. Full provenance chain visible (manufacturer → distributor → retailer → buyer)

---

## 10. Privacy and Compliance

### 10.1 Privacy by Design

Secuura's architecture embodies privacy by design principles as mandated by GDPR Article 25:

| Principle | Implementation |
|-----------|---------------|
| **Data minimisation** | Only cryptographic hashes processed; documents never stored |
| **Purpose limitation** | Data collected only for specified certification/verification purposes |
| **Storage limitation** | Automated retention policies with configurable expiration |
| **Accuracy** | Blockchain immutability ensures certification records are accurate |
| **Integrity and confidentiality** | Encryption at rest and in transit; access controls |
| **Accountability** | Comprehensive audit logging; consent records; deletion logs |

### 10.2 GDPR Compliance

Secuura implements comprehensive GDPR controls, all fully operational via dedicated API endpoints:

**Consent Management:**
- Purpose-specific consent records with version tracking
- Consent expiration support
- Consent withdrawal with timestamp
- Consent validity checking

**Data Subject Rights:**
- Right of access — Data export in JSON format
- Right to rectification — DSR system with audit trail
- Right to erasure — Cascading deletion across 9 data categories
- Right to portability — Downloadable data export
- Right to restriction — Processing restriction support
- Right to object — Objection request handling

**GDPR API Endpoints (all operational):**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/gdpr/consent` | POST | Record user consent |
| `/api/gdpr/consent/withdraw` | POST | Withdraw consent |
| `/api/gdpr/consent/check` | GET | Check valid consent |
| `/api/gdpr/consent/:userId` | GET | List all user consents |
| `/api/gdpr/dsr` | POST | Create Data Subject Request |
| `/api/gdpr/dsr/pending` | GET | List pending DSRs (admin) |
| `/api/gdpr/dsr/:dsrId` | PATCH | Update DSR status |
| `/api/gdpr/export/:userId` | GET | Export user data (Article 20) |
| `/api/gdpr/export/:userId/download` | GET | Download user data as file |
| `/api/gdpr/erasure/:userId` | POST | Execute right-to-be-forgotten |
| `/api/gdpr/retention` | GET | List retention policies |
| `/api/gdpr/retention/enforce` | POST | Trigger retention enforcement |
| `/api/gdpr/deletion-log` | GET | View deletion audit trail |

**Data Retention:**
- Automated retention enforcement (daily scheduler)
- Configurable per data type
- Deletion methods: hard delete, soft delete, anonymise
- Deletion audit log

**Database Tables:** `consent_records`, `data_subject_requests`, `data_deletion_log`, `data_retention_policies` — all with UUID primary keys, foreign key relationships, and audit timestamps.

### 10.3 Blockchain and GDPR Compatibility

A key challenge for blockchain systems is GDPR's right to erasure. Secuura resolves this through its hybrid architecture:

- **On-chain data** consists exclusively of cryptographic hashes — these are not personal data under GDPR as they cannot be reversed to reveal the original document or individual
- **Off-chain data** (user profiles, metadata, access rules) is stored in PostgreSQL and can be fully deleted or anonymised on request
- When erasure is executed, the on-chain hash becomes an orphaned reference with no personal data linkage

---

## 11. Security Architecture

### 11.1 Authentication

| Method | Use Case | Implementation |
|--------|----------|---------------|
| **JWT tokens** | API authentication | Access + refresh token pair; rotation support |
| **Multi-factor authentication** | Enhanced security | TOTP (Google Authenticator compatible); backup codes |
| **Microsoft Entra ID** | Enterprise SSO | OAuth 2.0 flow with tenant management |
| **Auth0** | Social/enterprise SSO | OpenID Connect integration |
| **Cardano wallets** | Blockchain operations | CIP-30 connection; CIP-8 message signing |
| **API keys** | Programmatic access | Scoped keys with rate limiting; hash-stored (not plaintext) |

### 11.2 Application Security

| Control | Implementation |
|---------|---------------|
| **Input sanitisation** | XSS prevention, SQL injection detection, path traversal blocking, command injection prevention |
| **Security headers** | Helmet.js: CSP, HSTS (1 year), X-Content-Type-Options, X-Frame-Options, Referrer-Policy, Permissions-Policy |
| **Rate limiting** | Global: 100 req/min; Auth: 10 req/15 min; Verification: 200 req/min; Redis-backed with in-memory fallback |
| **CORS** | Whitelist-based origin control; credentials enabled |
| **Brute-force protection** | Exponential backoff (500ms–30s); Redis-backed; 5-minute lockout |
| **Error handling** | Standardised error classes; production-safe responses (no stack traces) |
| **Parameterised queries** | Prisma ORM prevents SQL injection |

### 11.3 Infrastructure Security

| Control | Implementation |
|---------|---------------|
| **Container isolation** | Docker containers with network segmentation |
| **Secret management** | Environment variable-based; no hardcoded secrets |
| **Database security** | PostgreSQL with SCRAM-SHA-256; Redis with password authentication |
| **Health monitoring** | Service health endpoints; container restart policies |
| **Graceful shutdown** | Signal handling; connection draining |
| **Logging** | Winston structured logging; file transports in production; error tracking |

---

## 12. Smart Contract Framework

### 12.1 Aiken Smart Contracts

Secuura's on-chain logic is implemented in Aiken, Cardano's purpose-built smart contract language:

**Document Contract** — Core certification logic:
- Document status transitions (Draft → Certified → Verified)
- Certifier authorisation verification
- Hash integrity checking

**Provenance Contract** — Chain of custody:
- Event recording
- Provenance chain validation
- Temporal ordering enforcement

**Multi-Sig Contract** — Governance:
- Multi-party approval for configuration changes
- Threshold signatures
- Governance proposal execution

**Platform Governance Contract** — Meta-rules:
- Platform-level rules enforcement
- Immutable rule protection
- Deployment-specific rule configuration

### 12.2 Immutable Rules

Certain rules are designated as immutable and cannot be changed even by governance:
- Only the originator can certify authenticity
- Every action creates a blockchain record
- Hash algorithms cannot be downgraded
- Audit trail cannot be disabled

---

## 13. Frontend Applications

### 13.1 Issuer Portal

The primary interface for organisations certifying documents:
- **Dashboard** — Overview of documents, statistics, recent activity
- **Document Management** — Upload, certify, monitor, share, revoke
- **Document Lineage** — Interactive graph visualisation of document history
- **Wallet Connection** — CIP-30 wallet integration for signing
- **Analytics** — Certification volume, verification rates, usage trends
- **Billing** — Chargeable events, pricing, payment management

### 13.2 Verifier Portal

Public-facing interface for document verification (accessible at `http://localhost:8882/verify/`):
- **File Upload** — Drag-and-drop verification by document upload (POST `/api/verification/verify`)
- **Document ID** — Verification by certification identifier (navigates to `/result/:documentId`)
- **QR Code** — Camera-based QR code scanning for instant verification
- **Results** — Displays verification checks (exists, hash valid, blockchain anchored, not revoked, signatures), issuer details, and blockchain proof (transaction hash, block height, confirmation date)

### 13.3 Admin Dashboard

Platform administration interface:
- **User Management** — Create, disable, manage users and roles
- **Organisation Management** — Organisation setup and configuration
- **Document Types** — Configure certifiable document types
- **Workflows** — Define certification workflows
- **System Health** — Error monitoring, service health, GDPR DSR tracking
- **Audit Logs** — Comprehensive activity logging
- **API Keys** — Manage programmatic access
- **Pricing Configuration** — Configure chargeable event pricing

### 13.4 Status Page

Public system status monitoring interface.

---

## 14. Integrations and Extensibility

### 14.1 Current Integrations

| Integration | Purpose | Protocol |
|-------------|---------|----------|
| **Microsoft Entra ID** | Enterprise SSO authentication | OAuth 2.0 |
| **Microsoft 365 / SharePoint** | Document source integration | Microsoft Graph API |
| **Auth0** | Social and enterprise SSO | OpenID Connect |
| **Stripe** | Payment processing | Stripe API + Webhooks |
| **Cardano wallets** | Blockchain operations | CIP-30 / CIP-8 |
| **Atala PRISM** | Decentralised identity | PRISM SDK |
| **IPFS (Pinata)** | NFT metadata storage | IPFS API |
| **Onfido / Jumio** | KYC identity verification | REST API |

### 14.2 API-First Architecture

Secuura's entire functionality is accessible via RESTful APIs, enabling:
- **Third-party integrations** — Any system can certify and verify documents
- **White-labelling** — Custom frontends using Secuura's API
- **Webhook notifications** — Real-time event notifications
- **SDK support** — JavaScript/TypeScript SDK for rapid integration

### 14.3 Future Integrations

- **Midnight sidechain** — Zero-knowledge proofs for selective disclosure (operational — generate and verify endpoints available)
- **European Digital Identity Wallets** — eIDAS 2.0 compatibility
- **Government identity services** — Gov.UK Verify, Australian myGovID
- **Document management systems** — Additional DMS integrations
- **Mobile applications** — iOS and Android native apps

---

## 15. Chargeable Events and Revenue Model

### 15.1 Event-Based Pricing

Secuura's revenue model is based on chargeable events — specific actions within the certification and verification lifecycle that generate platform fees. Pricing is stored in a database and can be configured per deployment.

### 15.2 Pricing Tiers

| Tier | Included Events | Additional Cost | Target |
|------|----------------|-----------------|--------|
| **Basic** | 100/month | Per-event pricing | Small organisations |
| **Standard** | 500/month | Discounted per-event | Medium organisations |
| **Premium** | 2,000/month | Further discounted | Large organisations |
| **Enterprise** | Unlimited | Custom pricing | Enterprise clients |

### 15.3 Revenue Streams

1. **Platform fees** — Per-event charges for certifications and verifications
2. **Subscription tiers** — Monthly/annual subscription with included event volumes
3. **Enterprise licensing** — Custom pricing for large-scale deployments
4. **White-label licensing** — Fees for white-labelled deployments
5. **API access** — Programmatic access tiers

---

## 16. Technology Stack

### 16.1 Backend

| Technology | Purpose |
|-----------|---------|
| **Node.js / TypeScript** | Service runtime and type safety |
| **Express.js** | HTTP framework |
| **Prisma ORM** | Database access and migrations |
| **PostgreSQL 15** | Primary data store |
| **Redis 7** | Caching, sessions, rate limiting |
| **Winston** | Structured logging |
| **Docker / Docker Compose** | Containerisation and orchestration |

### 16.2 Frontend

| Technology | Purpose |
|-----------|---------|
| **React 18** | UI framework |
| **TypeScript** | Type safety |
| **Vite** | Build tooling |
| **Material UI (MUI)** | Component library |
| **React Flow (@xyflow/react)** | Document lineage graph visualisation |
| **Dagre** | Directed graph layout |
| **React Router** | Client-side routing |

### 16.3 Blockchain

| Technology | Purpose |
|-----------|---------|
| **Cardano** | Layer 1 blockchain |
| **Aiken** | Smart contract language |
| **Yaci DevKit** | Local development network |
| **BLAKE2b-256 / SHA-256** | Cryptographic hashing |
| **CIP-30 / CIP-8** | Wallet integration standards |

### 16.4 Security

| Technology | Purpose |
|-----------|---------|
| **Helmet.js** | Security headers |
| **bcryptjs** | Password hashing |
| **jsonwebtoken** | JWT authentication |
| **express-rate-limit** | Rate limiting |
| **CORS** | Cross-origin resource sharing |

---

## 17. Development Roadmap

### Phase 1 — Core Platform (Current)

- Document certification and verification
- Cardano blockchain anchoring
- JWT + MFA authentication
- Issuer, Verifier, and Admin frontends
- GDPR compliance (consent, DSR, erasure, portability)
- Error tracking and structured logging
- Chargeable events with configurable pricing
- Microsoft Entra ID integration
- CIP-30 wallet integration
- Document lineage visualisation

### Phase 2 — Extended Capabilities

- Mobile applications (iOS, Android)
- Midnight sidechain integration (zero-knowledge proofs) — **implemented and operational**
- Ownership transfer workflows — **implemented** (simple, sale, inheritance, corporate types)
- Advanced KYC integration (government identity services)
- White-labelling for enterprise clients
- Self-hosted deployment option

### Phase 3 — Governance and Scale

- On-chain governance (DAO) — **implemented** (auto-registration, token-weighted voting, min 50-char proposal descriptions)
- Smart contract rules engine
- Multi-chain support consideration
- Advanced analytics and reporting
- Token staking and rewards

---

## 18. Competitive Landscape

| Solution Type | Examples | Secuura Differentiator |
|---------------|---------|----------------------|
| **Digital signature platforms** | DocuSign, Adobe Sign | Secuura focuses on authenticity, not signing workflows |
| **Blockchain notarisation** | Stampery, OriginStamp | Secuura provides full lifecycle management, not just timestamping |
| **Document management** | SharePoint, Box | Secuura is complementary — verifies documents stored elsewhere |
| **Credential platforms** | Accredible, Credly | Secuura is document-agnostic and supports any certification type |
| **Identity solutions** | uPort, Civic | Secuura focuses on documents, not identity alone |

**Secuura's unique position:** A comprehensive document authenticity platform combining blockchain immutability, privacy-first architecture, regulatory compliance, and enterprise integration capabilities.

---

## 19. Conclusion

Secuura addresses a fundamental challenge in the digital economy: proving that documents are genuine and unaltered. By combining the immutability of the Cardano blockchain with a privacy-first, hash-based architecture, Secuura provides a solution that is simultaneously tamper-proof and privacy-compliant.

The platform's microservices architecture ensures scalability and maintainability. Its comprehensive compliance framework — spanning GDPR, ISO 27001, SOC 2, OWASP, and blockchain standards — provides the assurance required by regulated industries. And its flexible verification levels and configurable pricing make it adaptable to deployment in any jurisdiction and industry.

As document fraud continues to evolve in sophistication, the need for a trustworthy, independently verifiable source of truth becomes ever more critical. Secuura provides that source of truth — anchored in mathematics, recorded on blockchain, and designed for the real world.

---

## 20. Glossary

| Term | Definition |
|------|-----------|
| **Anchoring** | Recording a document's cryptographic hash on the Cardano blockchain |
| **BLAKE2b-256** | Cryptographic hash function used as default in Secuura |
| **Cardano** | Third-generation proof-of-stake blockchain platform |
| **Certification** | The process of creating a verifiable record of document authenticity |
| **Certification Event** | A recorded action in a document's lifecycle (issue, sign, verify, etc.) |
| **Chargeable Event** | A certification event that incurs a platform fee |
| **CIP-8** | Cardano Improvement Proposal for message signing |
| **CIP-30** | Cardano Improvement Proposal for wallet dApp connection |
| **Creator** | Entity that creates and certifies a document (also called Issuer) |
| **DID** | Decentralised Identifier — a self-sovereign digital identity |
| **DSR** | Data Subject Request — a formal request under GDPR |
| **Erasure** | The right to have personal data deleted (GDPR Article 17) |
| **Hash** | A cryptographic fingerprint of a document's contents |
| **Owner** | Entity that owns and controls a certified document |
| **Provenance** | The complete history and chain of custody of a document |
| **Rights Holder** | Entity with ownership rights to a certification |
| **SVS** | Secure Verification Service — Secuura's core verification system |
| **Verifiable Credential** | A cryptographically secure, machine-verifiable digital credential |
| **Verification** | The process of confirming a document matches its blockchain-anchored hash |

---

_Copyright 2026 Secuura. All rights reserved._

---

**End of Document**
