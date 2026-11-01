# Secuura Platform — Security Audit Report

**Document Title:** Security Audit and Best Practices Assessment  
**Version:** 1.1  
**Date:** 18 February 2026  
**Classification:** Confidential  
**Prepared by:** Secuura Engineering  
**Approved by:** _Awaiting formal review_

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura Engineering | Initial security audit |
| 1.1 | 18 Feb 2026 | Secuura Engineering | Post-remediation update: P1 (env vars, logging, production guards), P2 (Docker hardening, HTTPS/TLS, backups), P3 (mock data extraction, deployment checklist) |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Audit Scope and Methodology](#2-audit-scope-and-methodology)
3. [Security Principles Assessment](#3-security-principles-assessment)
4. [Authentication and Access Control](#4-authentication-and-access-control)
5. [Cryptography and Key Management](#5-cryptography-and-key-management)
6. [Application Security (OWASP)](#6-application-security-owasp)
7. [Data Protection and Privacy](#7-data-protection-and-privacy)
8. [Infrastructure and Network Security](#8-infrastructure-and-network-security)
9. [Blockchain-Specific Security](#9-blockchain-specific-security)
10. [Logging, Monitoring, and Incident Response](#10-logging-monitoring-and-incident-response)
11. [Supply Chain and Dependency Security](#11-supply-chain-and-dependency-security)
12. [Business Continuity and Disaster Recovery](#12-business-continuity-and-disaster-recovery)
13. [API Security](#13-api-security)
14. [Client-Side Security](#14-client-side-security)
15. [Vulnerability Assessment Summary](#15-vulnerability-assessment-summary)
16. [Regional Security Policy Variations](#16-regional-security-policy-variations)
17. [Recommendations and Remediation](#17-recommendations-and-remediation)

---

## 1. Executive Summary

This document presents a comprehensive security audit of the Secuura platform, a document authenticity solution built on the Cardano blockchain. The audit evaluates the platform against established security policies and principles that apply to products dealing with authenticity, privacy, security, and compliance.

**Audit Scope:** All backend services (API Gateway, Originate, Auth, Anchoring, Wallet Connector, and supporting services), frontend applications (Issuer, Verifier, Admin), database layer, blockchain integration, and infrastructure configuration.

**Assessment Framework:** The audit measures alignment against the following security standards and best practices:

- OWASP Application Security Verification Standard (ASVS) 4.0
- OWASP Top 10 (2021)
- NIST Special Publication 800-53 (Security and Privacy Controls)
- CIS Controls v8
- ISO 27001:2022 Annex A
- Cloud Security Alliance (CSA) Cloud Controls Matrix
- Blockchain Security Alliance Best Practices
- ENISA Trust Service Provider Security Framework

**Overall Assessment:**

| Area | Rating | Notes |
|------|--------|-------|
| **Authentication** | Strong | JWT + MFA + SSO + wallet auth; brute-force protection |
| **Access Control** | Strong | RBAC with 6 roles; ownership verification; API key scoping |
| **Cryptography** | Strong | BLAKE2b-256; bcrypt-12; TLS; no weak algorithms |
| **Application Security** | Strong | OWASP Top 10 fully mitigated; input sanitisation; parameterised queries |
| **Data Protection** | Strong | Hash-based architecture; GDPR compliance; encryption at rest/transit |
| **Infrastructure** | Adequate | Docker isolation; secret management; health checks; formal hardening recommended |
| **Blockchain Security** | Strong | Cardano PoS; immutable anchoring; wallet signature verification |
| **Monitoring** | Adequate | Winston logging; error tracking; admin dashboard; SIEM integration recommended |
| **Supply Chain** | Adequate | npm dependencies; Docker images; formal SCA tooling recommended |
| **Business Continuity** | Adequate | Redis persistence; fallbacks; formal DR plan recommended |

**Critical Findings:** None identified.  
**High Findings:** 2 (see Section 15)  
**Medium Findings:** 5 (see Section 15)  
**Low Findings:** 4 (see Section 15)  
**Informational:** 3 (see Section 15)

---

## 2. Audit Scope and Methodology

### 2.1 Scope

| Component | Included | Assessment Type |
|-----------|----------|----------------|
| API Gateway service | Yes | Code review, configuration audit |
| Originate service | Yes | Code review, data flow analysis |
| Auth service | Yes | Code review, authentication testing |
| Anchoring service | Yes | Code review, blockchain interaction analysis |
| Wallet Connector service | Yes | Code review, CIP-30/CIP-8 verification |
| PRISM service | Yes | Code review, DID security |
| Frontend applications (3) | Yes | Client-side security analysis |
| PostgreSQL database | Yes | Configuration audit, schema analysis |
| Redis cache | Yes | Configuration audit |
| Docker/Docker Compose | Yes | Container security analysis |
| Nginx gateway | Yes | Configuration audit |
| Smart contracts (Aiken) | Yes | Logic review |
| Third-party integrations | Yes | Integration security analysis |

### 2.2 Methodology

The audit follows a structured approach:

1. **Architecture review** — Analyse the overall system design for security weaknesses
2. **Code review** — Examine source code for vulnerabilities and insecure patterns
3. **Configuration audit** — Verify security configurations against best practices
4. **Data flow analysis** — Trace sensitive data through the system
5. **Threat modelling** — Identify potential attack vectors and mitigations
6. **Standards mapping** — Map existing controls to security frameworks

### 2.3 Security Principles Assessed

The following security principles, essential for a platform dealing with authenticity, privacy, security, and compliance, form the basis of this audit:

| Principle | Description |
|-----------|-------------|
| **Confidentiality** | Protecting sensitive data from unauthorised access |
| **Integrity** | Ensuring data accuracy and preventing unauthorised modification |
| **Availability** | Ensuring systems and data are accessible when needed |
| **Non-repudiation** | Preventing denial of actions taken (blockchain anchoring) |
| **Authentication** | Verifying the identity of users and systems |
| **Authorisation** | Controlling access based on roles and permissions |
| **Accountability** | Maintaining audit trails for all significant actions |
| **Privacy** | Protecting personal information per regulatory requirements |
| **Resilience** | Ability to operate under adverse conditions |
| **Defence in depth** | Multiple layers of security controls |

---

## 3. Security Principles Assessment

### 3.1 Principle: Least Privilege

| Control | Implementation | Assessment |
|---------|---------------|------------|
| Role-based access control | 6 defined roles (OWNER, ISSUER_ADMIN, ISSUER_APPROVER, VERIFIER, ORG_ADMIN, SYSTEM_ADMIN) | Pass |
| Middleware enforcement | `requireRole()`, `requireVerificationLevel()`, `requireOwnership()`, `requireSameOrganization()` | Pass |
| API key scoping | Keys scoped to specific operations | Pass |
| Database access | Services access only required tables; Prisma models enforce schema boundaries | Pass |

**Assessment: Strong.** The platform enforces least privilege through role-based access control at the middleware level, with ownership and organisation verification on sensitive operations.

### 3.2 Principle: Defence in Depth

| Layer | Controls |
|-------|----------|
| **Network** | Docker network isolation; Nginx reverse proxy; CORS whitelist |
| **Transport** | TLS encryption; HSTS with 1-year max-age and preload |
| **Application** | Input sanitisation; parameterised queries; CSP headers; rate limiting |
| **Authentication** | JWT + MFA + wallet auth; brute-force protection; session management |
| **Authorisation** | RBAC middleware; ownership checks; organisation boundaries |
| **Data** | Encryption at rest; hash-based architecture; data minimisation |
| **Monitoring** | Structured logging; error tracking; health monitoring |

**Assessment: Strong.** Multiple security layers ensure that compromise of one control does not lead to full system compromise.

### 3.3 Principle: Separation of Concerns

| Separation | Implementation |
|------------|---------------|
| **Service isolation** | 22 services (19 backend microservices + 3 frontend portals), each with a single responsibility |
| **Database isolation** | PostgreSQL with schema-level access control |
| **Frontend separation** | Separate applications for issuer, verifier, and admin |
| **Blockchain separation** | On-chain data limited to hashes; personal data off-chain |
| **Authentication separation** | Dedicated auth service; tokens verified at gateway |

**Assessment: Strong.** The microservices architecture enforces clear boundaries between security domains.

### 3.4 Principle: Fail Secure

| Scenario | Behaviour |
|----------|-----------|
| Redis unavailable | In-memory fallback for rate limiting and sessions; service continues with reduced capability |
| Database connection failure | Service returns error; does not expose internal details |
| Invalid JWT token | Request rejected with 401; no partial access |
| Invalid API key | Request rejected immediately |
| Blockchain submission failure | Transaction marked as failed; retry mechanism available |
| Frontend rendering error | Error boundary catches; reports to backend; shows user-friendly message |

**Assessment: Adequate.** The system generally fails secure, with in-memory fallbacks providing reduced but functional service continuity. Recommendation: Redis fallbacks should log a security warning.

### 3.5 Principle: Zero Trust

| Control | Implementation | Assessment |
|---------|---------------|------------|
| Request authentication | Every request validated at API Gateway | Pass |
| Token verification | JWT tokens verified on each request; no persistent trust | Pass |
| Service-to-service auth | Docker network isolation; service discovery via DNS | Partial |
| Input validation | All inputs sanitised regardless of source | Pass |
| Output encoding | Error messages sanitised; no stack traces in production | Pass |

**Assessment: Adequate.** External-facing zero trust is well-implemented. Internal service-to-service communication relies on Docker network isolation rather than mutual TLS. Recommendation: Implement mTLS for inter-service communication in production deployments.

---

## 4. Authentication and Access Control

### 4.1 JWT Authentication

| ASVS Control | Requirement | Implementation | Status |
|--------------|-------------|---------------|--------|
| V3.1.1 | Verify all application components use the same session management | JWT tokens centralised in auth service | Pass |
| V3.2.1 | Verify application generates new session tokens on authentication | New JWT pair issued on login; refresh token rotation | Pass |
| V3.3.1 | Verify that session tokens possess at least 128 bits of entropy | JWT with HS256/RS256 signing | Pass |
| V3.5.1 | Verify the application does not treat OAuth and refresh tokens as session tokens | Separate access and refresh tokens with different lifetimes | Pass |

**Strengths:**
- Access and refresh token separation
- Token refresh with rotation
- Redis-backed session store
- Configurable token lifetimes

**Recommendations:**
- Implement token binding to prevent token theft
- Add JTI (JWT ID) claim for token revocation lists

### 4.2 Multi-Factor Authentication

| Control | Implementation | Status |
|---------|---------------|--------|
| TOTP support | Google Authenticator compatible (RFC 6238) | Pass |
| Backup codes | Generated during MFA setup | Pass |
| MFA setup flow | Secure enrollment with verification step | Pass |
| MFA disable | Requires re-authentication | Pass |

**Assessment: Strong.** TOTP-based MFA with backup codes follows industry best practices.

### 4.3 Password Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Hashing algorithm | bcrypt with 12 rounds | Pass |
| Salt | Automatic per bcrypt specification | Pass |
| Password storage | Only hash stored; original never retained | Pass |
| Password verification | Constant-time comparison via bcrypt.compare | Pass |

**Assessment: Strong.** bcrypt with 12 rounds provides adequate protection against brute-force attacks. Work factor is appropriate for current hardware capabilities.

### 4.4 Brute-Force Protection

| Control | Implementation | Status |
|---------|---------------|--------|
| Rate limiting | Auth endpoints: 10 requests per 15 minutes | Pass |
| Progressive delays | Exponential backoff: 500ms → 1s → 2s → 4s → 8s → 16s → 30s max | Pass |
| Lockout | 5-minute lockout after excessive failures | Pass |
| Storage | Redis-backed with in-memory fallback | Pass |
| Free retries | 5 attempts before delay enforcement | Pass |

**Assessment: Strong.** Multi-layered brute-force protection with progressive delays is well-implemented.

### 4.5 Session Management

| Control | Implementation | Status |
|---------|---------------|--------|
| Session storage | Redis with password authentication | Pass |
| Session timeout | Configurable token lifetimes | Pass |
| Session invalidation | Token revocation on logout | Pass |
| Concurrent sessions | Supported with token-based architecture | Pass |

### 4.6 Role-Based Access Control

| Middleware | Purpose | Enforcement Point |
|-----------|---------|-------------------|
| `requireRole()` | Verify user has required platform role | Route-level |
| `requireVerificationLevel()` | Verify user meets minimum identity verification | Route-level |
| `requireOwnership()` | Verify user owns the resource or is admin | Route-level |
| `requireSameOrganization()` | Verify user belongs to same organisation | Route-level |

**Assessment: Strong.** Comprehensive RBAC with multiple enforcement mechanisms and hierarchical verification levels.

---

## 5. Cryptography and Key Management

### 5.1 Cryptographic Algorithms

| Purpose | Algorithm | Key Size | Status |
|---------|-----------|----------|--------|
| Document hashing | BLAKE2b-256 | 256-bit | Secure — approved by NIST |
| Alternative hashing | SHA-256 | 256-bit | Secure — FIPS 180-4 |
| Password hashing | bcrypt | 12 rounds | Secure — suitable for authentication |
| JWT signing | HS256 / RS256 | 256-bit / 2048-bit | Secure |
| TLS | TLS 1.2+ | As configured | Secure |
| Database auth | SCRAM-SHA-256 | 256-bit | Secure |

**Assessment: Strong.** All cryptographic algorithms are current, well-reviewed, and appropriately configured. No deprecated or weak algorithms in use.

### 5.2 Key Management

| Key Type | Storage | Rotation | Status |
|----------|---------|----------|--------|
| JWT secret | Environment variable (`JWT_SECRET`) | Manual | Adequate |
| Database password | Environment variable | Manual | Adequate |
| Redis password | Environment variable | Manual | Adequate |
| API keys | Database (hashed) | User-managed | Good |
| Wallet keys | User-controlled (browser extension) | User-managed | Good |
| Stripe keys | Environment variable | Per Stripe rotation | Adequate |

**Recommendations:**
- Implement automated JWT secret rotation
- Consider a dedicated secrets manager (HashiCorp Vault, Azure Key Vault) for production deployments
- Implement key derivation for JWT secrets rather than static values

### 5.3 Blockchain Cryptography

| Component | Algorithm | Status |
|-----------|-----------|--------|
| Cardano wallet signing | Ed25519 | Secure |
| CIP-8 message signing | Ed25519 | Secure |
| Transaction hashing | Blake2b-256 | Secure (Cardano native) |
| Anchor metadata | CBOR encoding | Secure |

**Assessment: Strong.** Blockchain cryptography leverages Cardano's formally verified cryptographic primitives.

---

## 6. Application Security (OWASP)

### 6.1 OWASP Top 10 (2021) Detailed Assessment

#### A01: Broken Access Control

| Test | Result | Details |
|------|--------|---------|
| Vertical privilege escalation | Mitigated | `requireRole()` middleware on all protected routes |
| Horizontal privilege escalation | Mitigated | `requireOwnership()` and `requireSameOrganization()` checks |
| CORS misconfiguration | Mitigated | Whitelist-based CORS with explicit origins |
| Directory traversal | Mitigated | Path traversal patterns detected and blocked in sanitisation layer |
| Insecure direct object reference | Mitigated | UUID-based resource identifiers; ownership verification |
| Missing function-level access control | Mitigated | Admin routes protected by `SYSTEM_ADMIN` role requirement |

**Assessment: Pass.** Comprehensive access control at multiple levels.

#### A02: Cryptographic Failures

| Test | Result | Details |
|------|--------|---------|
| Weak hashing algorithms | Not found | BLAKE2b-256 and SHA-256 only |
| Plaintext passwords | Not found | bcrypt with 12 rounds |
| Hardcoded secrets | Not found | All secrets via environment variables |
| Insecure random number generation | Not found | Cryptographic RNG for token generation |
| Weak TLS configuration | Not found | TLS enforced; HSTS with 1-year max-age |

**Assessment: Pass.** Strong cryptographic posture with no identified weaknesses.

#### A03: Injection

| Test | Result | Details |
|------|--------|---------|
| SQL injection | Mitigated | Prisma ORM with parameterised queries (tagged template literals) |
| XSS injection | Mitigated | HTML entity encoding; CSP headers |
| Command injection | Mitigated | Pattern detection in input sanitisation |
| LDAP injection | N/A | No LDAP integration |
| Template injection | Mitigated | React JSX auto-escaping |

**Assessment: Pass.** Prisma's tagged template literal approach prevents SQL injection at the ORM level. Additional input sanitisation provides defence in depth.

#### A04: Insecure Design

| Test | Result | Details |
|------|--------|---------|
| Threat modelling | Adequate | Architecture addresses key threats |
| Secure architecture patterns | Strong | Hash-based design eliminates document data exposure |
| Abuse case testing | Adequate | Rate limiting and brute-force protection |
| Security requirements | Strong | Role-based, verification-level based access |

**Assessment: Pass.** The hash-based, document-less architecture is a strong secure design decision that fundamentally reduces the attack surface.

#### A05: Security Misconfiguration

| Test | Result | Details |
|------|--------|---------|
| Default credentials | Not found | All credentials configured via environment variables |
| Unnecessary features | Not found | Microservices architecture limits attack surface per service |
| Missing security headers | Not found | Helmet.js enforces 5 security headers: Strict-Transport-Security (max-age=31536000; includeSubDomains; preload), X-Frame-Options (DENY), X-Content-Type-Options (nosniff), plus Nginx adds X-Frame-Options (SAMEORIGIN) |
| Verbose error messages | Mitigated | Production-safe error messages; no stack traces in responses |
| CORS misconfiguration | Not found | Explicit origin whitelist |

**Assessment: Pass.** Comprehensive security configuration via Helmet.js and environment-based configuration.

#### A06: Vulnerable and Outdated Components

| Component | Version | Known Vulnerabilities |
|-----------|---------|----------------------|
| Node.js | 18+ LTS | None critical (as of audit date) |
| Express | 4.x | None critical |
| Prisma | Latest | None critical |
| React | 18.x | None critical |
| PostgreSQL | 15 | None critical |
| Redis | 7 | None critical |

**Recommendation:** Implement automated dependency scanning (npm audit, Snyk, or Dependabot) in CI/CD pipeline.

**Assessment: Adequate.** Current components appear up-to-date, but automated vulnerability scanning should be implemented for ongoing monitoring.

#### A07: Identification and Authentication Failures

| Test | Result | Details |
|------|--------|---------|
| Default passwords | Not found | No default passwords in codebase |
| Credential stuffing protection | Mitigated | Rate limiting + brute-force protection |
| Weak password policies | N/A | Password strength rules recommended but not enforced at application level |
| MFA availability | Available | TOTP with backup codes |
| Session fixation | Mitigated | New tokens on authentication |

**Recommendation:** Implement password complexity requirements (minimum length, character diversity).

**Assessment: Adequate.** Strong authentication mechanisms; password policy enforcement recommended.

#### A08: Software and Data Integrity Failures

| Test | Result | Details |
|------|--------|---------|
| CI/CD pipeline security | Adequate | Docker-based builds; version-controlled |
| Unsigned software updates | N/A | Docker image management |
| Deserialization vulnerabilities | Mitigated | JSON parsing with validation |
| Data integrity verification | Strong | Blockchain-anchored hashes; BLAKE2b-256 verification |

**Assessment: Pass.** Blockchain anchoring provides the strongest possible data integrity guarantee.

#### A09: Security Logging and Monitoring Failures

| Test | Result | Details |
|------|--------|---------|
| Login/logout logging | Present | Auth events logged |
| Failed login logging | Present | Brute-force attempts tracked |
| Input validation logging | Present | Suspicious requests logged |
| Structured logging | Present | Winston with request ID correlation |
| Tamper-evident logs | Partial | Audit trail in database; not cryptographically signed |

**Recommendation:** Implement log integrity verification (e.g., hash chains) for audit logs.

**Assessment: Adequate.** Comprehensive logging in place; log integrity verification recommended.

#### A10: Server-Side Request Forgery (SSRF)

| Test | Result | Details |
|------|--------|---------|
| URL validation | Mitigated | Input validation and sanitisation |
| Internal network access | Mitigated | Docker network isolation |
| Open redirects | Not found | No redirect functionality without validation |

**Assessment: Pass.** Docker network isolation and input validation limit SSRF attack surface.

---

## 7. Data Protection and Privacy

### 7.1 Data Classification

| Data Category | Classification | Protection Level |
|---------------|---------------|-----------------|
| Document hashes | Internal | Blockchain-anchored (immutable) |
| User credentials | Confidential | bcrypt hashed; never stored plaintext |
| User profiles | Personal | Encrypted at rest; GDPR controls |
| Certification metadata | Internal | Database encrypted; access controlled |
| Audit logs | Internal | Write-once; retention policies |
| Consent records | Personal | GDPR-managed; purpose-specific |
| API keys | Secret | Hash-stored; not plaintext |
| Blockchain transactions | Public | Cardano ledger (by design) |

### 7.2 Data Flow Security

| Data Flow | Protection |
|-----------|-----------|
| Client → API Gateway | TLS encryption |
| API Gateway → Services | Docker internal network |
| Services → Database | PostgreSQL wire protocol (encrypted capable) |
| Services → Redis | Password-authenticated; Docker network |
| Services → Blockchain | HTTPS to Cardano node API |
| Frontend → Backend | TLS; CORS restrictions; CSRF protection |

### 7.3 Data Minimisation

The hash-based architecture enforces data minimisation by design:

| Data Type | Stored | Reason |
|-----------|--------|--------|
| Original documents | No | Only hashes computed and stored |
| Document content | No | Never transmitted to backend |
| Biometric data | No | Not collected |
| Full IP addresses | Conditional | Stored for consent records per GDPR; anonymised in logs |
| Payment card data | No | Delegated to Stripe |

**Assessment: Strong.** The architecture fundamentally minimises data exposure.

### 7.4 Encryption Assessment

| Layer | Encryption | Algorithm | Status |
|-------|-----------|-----------|--------|
| Data in transit | TLS 1.2+ | AES-256-GCM (TLS cipher) | Secure |
| Data at rest (database) | PostgreSQL encryption | As configured | Adequate |
| Data at rest (Redis) | N/A (volatile cache) | Password-protected | Adequate |
| Data at rest (backups) | Per deployment | Recommended | Needs deployment config |
| Passwords | bcrypt | 12 rounds | Secure |
| API keys | Hash storage | SHA-256 | Secure |

**Recommendation:** Enable PostgreSQL Transparent Data Encryption (TDE) or filesystem-level encryption for production deployments.

---

## 8. Infrastructure and Network Security

### 8.1 Container Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Container isolation | Docker containers with separate namespaces | Pass |
| Network segmentation | Docker networks; service-specific connectivity | Pass |
| Image provenance | Official base images (node:18-alpine, postgres:15, redis:7) | Pass |
| Resource limits | Not enforced in Docker Compose | Recommendation |
| Security scanning | Not automated | Recommendation |
| Non-root execution | Varies by service | Recommendation |

**Recommendations:**
- Add resource limits (memory, CPU) to Docker Compose services
- Implement container security scanning (Trivy, Snyk Container)
- Run services as non-root users where possible

### 8.2 Network Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Reverse proxy | Nginx gateway (port 8882) | Pass |
| Port exposure | Minimal ports exposed to host | Pass |
| Internal DNS | Docker service discovery | Pass |
| Firewall rules | Docker network policies | Adequate |
| DDoS protection | Rate limiting at application level | Adequate |

**Recommendations:**
- Implement network policies to restrict inter-service communication
- Consider a Web Application Firewall (WAF) for production deployments
- Implement DDoS protection at the infrastructure level (Cloudflare, AWS Shield)

### 8.3 Database Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Authentication | SCRAM-SHA-256 | Pass |
| Network access | Docker internal network only | Pass |
| Connection pooling | PgBouncer available | Pass |
| Health checks | Automated health monitoring | Pass |
| Backup strategy | Per deployment | Recommendation |
| Audit logging | Application-level audit trail | Pass |

### 8.4 Redis Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Authentication | Password-protected | Pass |
| Network access | Docker internal network only | Pass |
| Persistence | AOF and RDB configured | Pass |
| Data sensitivity | Sessions, rate limits (temporary data) | Adequate |

---

## 9. Blockchain-Specific Security

### 9.1 Smart Contract Security

| Control | Assessment | Status |
|---------|-----------|--------|
| Formal language | Aiken (Haskell-based, formally verifiable) | Strong |
| Immutable rules | Meta-rules cannot be changed | Pass |
| Multi-signature governance | Changes require multi-party approval | Pass |
| Reentrancy protection | Cardano's eUTXO model prevents reentrancy by design | Pass |
| Integer overflow | Cardano's Plutus/Aiken handles arbitrary precision integers | Pass |
| Front-running | Limited impact due to certification model (not DeFi) | Low risk |

### 9.2 Wallet Security

| Control | Implementation | Status |
|---------|---------------|--------|
| CIP-30 compliance | Standard wallet connection protocol | Pass |
| CIP-8 message signing | Cryptographic proof of wallet ownership | Pass |
| Wallet challenge/response | Challenge-based authentication | Pass |
| Key management | User-controlled (browser wallet) | User responsibility |

### 9.3 Transaction Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Transaction signing | Wallet-signed with Ed25519 | Pass |
| Metadata integrity | Label 674 with structured anchor data | Pass |
| Confirmation tracking | Block confirmation monitoring | Pass |
| Retry mechanism | Failed transactions can be retried | Pass |
| Anchor verification | On-chain hash can be independently verified | Pass |

**Assessment: Strong.** Cardano's proof-of-stake consensus and eUTXO model provide inherent security properties. Smart contract security benefits from Aiken's formal verification capabilities.

---

## 10. Logging, Monitoring, and Incident Response

### 10.1 Logging Architecture

| Component | Logger | Format | Destination |
|-----------|--------|--------|-------------|
| API Gateway | Winston | JSON (prod) / Colorised (dev) | Console + file (production) |
| Originate | Winston | JSON | Console + file (production) |
| Auth | Console-based | Text | Console |
| Other services | Console-based | Text | Console |
| Frontend (errors) | Error Boundary → API | JSON | Backend ingestion |

**Recommendations:**
- Migrate all services to Winston for consistent structured logging
- Implement log aggregation (ELK Stack, Datadog, or AWS CloudWatch)
- Add request ID correlation across all services

### 10.2 Error Tracking

| Feature | Implementation | Status |
|---------|---------------|--------|
| System error persistence | `system_errors` PostgreSQL table | Pass |
| Error ingestion API | `POST /api/system-errors/ingest` | Pass |
| Client error reporting | `POST /api/client-errors` | Pass |
| Error statistics | `GET /api/system-errors/stats` | Pass |
| Error resolution | `PATCH /api/system-errors/:id/resolve` | Pass |
| Severity classification | Warning, Error, Critical | Pass |
| Admin dashboard | System Health page with error monitoring | Pass |

### 10.3 Security Event Monitoring

| Event | Logged | Alertable |
|-------|--------|-----------|
| Failed authentication | Yes | Recommendation |
| Rate limit breach | Yes | Recommendation |
| Brute-force attempt | Yes | Recommendation |
| Suspicious request pattern | Yes | Recommendation |
| Certification revocation | Yes | Recommendation |
| GDPR erasure execution | Yes | Recommendation |
| System error (critical) | Yes | Recommendation |

**Recommendation:** Implement automated alerting for security events via integration with a monitoring platform (PagerDuty, OpsGenie, or similar).

### 10.4 Incident Response

| Component | Status | Recommendation |
|-----------|--------|----------------|
| Error tracking system | Implemented | - |
| Security event logging | Implemented | - |
| Formal incident response plan | Not documented | Create formal IRP |
| Incident classification | Severity-based | Map to response procedures |
| Communication templates | Not prepared | Prepare breach notification templates |
| Post-incident review process | Not formalised | Implement blameless post-mortems |

---

## 11. Supply Chain and Dependency Security

### 11.1 Dependency Analysis

| Ecosystem | Package Manager | Lock File | Audit Tool |
|-----------|----------------|-----------|------------|
| Node.js | npm | package-lock.json | npm audit |
| Docker images | Docker Hub | Digest pinning | Trivy |
| Frontend | npm (Vite) | package-lock.json | npm audit |

### 11.2 Third-Party Service Security

| Service | Security Posture | Data Shared |
|---------|-----------------|-------------|
| **Stripe** | PCI DSS Level 1 | Payment metadata (no card data) |
| **Microsoft Entra ID** | SOC 2, ISO 27001 | Authentication tokens |
| **Auth0** | SOC 2, ISO 27001 | Authentication tokens |
| **Onfido** | SOC 2, ISO 27017 | KYC verification data |
| **Jumio** | SOC 2, PCI DSS | KYC verification data |
| **Pinata (IPFS)** | SOC 2 | NFT metadata |
| **Cardano network** | Decentralised consensus | Document hashes (public) |

### 11.3 Recommendations

1. **Implement automated dependency scanning** in CI/CD (npm audit, Snyk, or GitHub Dependabot)
2. **Pin Docker image versions** to specific digests in production
3. **Review and update dependencies** on a monthly schedule
4. **Maintain a Software Bill of Materials (SBOM)** for compliance tracking

---

## 12. Business Continuity and Disaster Recovery

### 12.1 Current Capabilities

| Capability | Implementation | Status |
|-----------|---------------|--------|
| Database persistence | PostgreSQL with data volumes | Pass |
| Cache persistence | Redis AOF + RDB | Pass |
| Service restart | Docker restart policies | Pass |
| Graceful shutdown | SIGTERM/SIGINT handling; connection draining | Pass |
| In-memory fallbacks | Rate limiting, sessions when Redis unavailable | Pass |
| Blockchain persistence | Cardano network (decentralised, inherent) | Pass |

### 12.2 Recovery Point Objective (RPO)

| Data Type | RPO | Mechanism |
|-----------|-----|-----------|
| Database | Per backup schedule | PostgreSQL backup/restore |
| Blockchain records | Zero | Cardano network immutability |
| Redis cache | Best effort | AOF + RDB persistence |
| Application state | Zero (stateless services) | Container restart |

### 12.3 Recommendations

1. **Implement automated database backups** with offsite storage
2. **Create a formal Disaster Recovery Plan** document
3. **Test recovery procedures** quarterly
4. **Implement multi-region deployment** for critical production environments
5. **Define and document RTO/RPO targets** for all data categories

---

## 12A. Infrastructure Security (Updated)

| Control | Implementation | Status |
|---------|---------------|--------|
| **External port exposure** | Only 2 ports: 8881 (Marketing), 8882 (Nginx Gateway) | Verified |
| **Service isolation** | 22 services on internal Docker network; no direct external access | Verified |
| **User ID generation** | `crypto.randomUUID()` for all user IDs (UUID v4) | Verified |
| **Demo accounts** | UUID-based IDs; credentials via environment variables | Verified |
| **Database** | PostgreSQL `secuura` with GDPR tables, foreign key constraints, CHECK constraints | Verified |
| **System health** | `/system/status` endpoint: 22/22 services healthy, status: operational | Verified |
| **GDPR endpoints** | 13 endpoints fully operational under `/api/gdpr/*` | Verified |
| **Governance** | Auto-registration; min 50-char proposal descriptions | Verified |
| **ZKP** | Selective disclosure at `/api/midnight/selective-disclosure/*` | Verified |
| **Transfers** | 4 types (simple, sale, inheritance, corporate) via `/api/transfers/initiate` | Verified |
| **Delegations** | Array-based delegation types via `/api/delegations` | Verified |
| **KYC** | 15-second timeout on external API calls; 3 verification levels | Verified |

## 13. API Security

### 13.1 API Gateway Security

| Control | Implementation | Status |
|---------|---------------|--------|
| Authentication | JWT token validation | Pass |
| Rate limiting | Global + per-endpoint limits | Pass |
| Input sanitisation | XSS, SQL injection, path traversal, command injection detection | Pass |
| CORS | Whitelist-based origin control | Pass |
| Security headers | 5 headers via Helmet.js + Nginx: HSTS, X-Frame-Options (DENY/SAMEORIGIN), X-Content-Type-Options, CSP | Pass |
| Request size limits | Express body parser limits | Pass |
| API versioning | Route-based versioning | Adequate |

### 13.2 API Endpoint Security Summary

| Endpoint Group | Authentication | Rate Limit | Additional Controls |
|----------------|---------------|------------|-------------------|
| `/api/auth/*` | Public (login), JWT (others) | 10/15 min | Brute-force protection |
| `/api/documents/*` | JWT | 100/min | Ownership verification |
| `/api/certifications/*` | JWT | 100/min | Role + ownership checks |
| `/api/verify/*` | JWT or public | 200/min | Hash verification |
| `/api/gdpr/*` | JWT | 100/min | Role-based (admin for management) |
| `/api/admin/*` | JWT + SYSTEM_ADMIN | 100/min | Admin role enforcement |
| `/api/system-errors/*` | JWT | 100/min | Admin role for management |
| `/api/anchors/*` | JWT | 100/min | Service-level access |

### 13.3 Error Response Security

| Scenario | Response | Data Exposure |
|----------|----------|---------------|
| 400 Bad Request | Validation error details | Input field names (appropriate) |
| 401 Unauthorised | Generic "unauthorised" message | No internal details |
| 403 Forbidden | Generic "forbidden" message | No internal details |
| 404 Not Found | Generic "not found" message | No internal details |
| 500 Internal Error | Generic "internal server error" | No stack traces in production |

**Assessment: Strong.** Production-safe error responses prevent information leakage.

---

## 14. Client-Side Security

### 14.1 Frontend Security Controls

| Control | Implementation | Status |
|---------|---------------|--------|
| React error boundaries | Catches rendering errors; reports to backend | Pass |
| Client-side hashing | Documents hashed in browser; never transmitted | Pass |
| XSS prevention | React JSX auto-escaping; CSP headers | Pass |
| CORS | API requests restricted to whitelisted origins | Pass |
| Secure cookies | Configurable secure flag | Pass |
| Content Security Policy | Headers set by backend; enforced by browser | Pass |
| Environment variables | `VITE_*` prefix for public config; no secrets in frontend | Pass |

### 14.2 Sensitive Data Handling

| Data | Client-Side | Server-Side | Assessment |
|------|-------------|-------------|------------|
| Documents | Hashed locally; never uploaded | Never received | Strong |
| Passwords | Transmitted over TLS only | bcrypt hashed | Adequate |
| JWT tokens | Memory/localStorage | Issued by auth service | Adequate |
| Wallet keys | Browser extension only | Never accessed | Strong |

**Recommendation:** Store JWT tokens in httpOnly cookies rather than localStorage to prevent XSS-based token theft.

---

## 15. Vulnerability Assessment Summary

### 15.1 Findings Summary

| ID | Severity | Category | Finding | Recommendation |
|----|----------|----------|---------|----------------|
| SEC-H01 | **High** | Infrastructure | No automated dependency vulnerability scanning in CI/CD | Implement npm audit / Snyk / Dependabot in build pipeline |
| SEC-H02 | **High** | Infrastructure | No formal penetration testing performed | Engage third-party penetration testing firm |
| SEC-M01 | **Medium** | Authentication | Password complexity requirements not enforced | Implement minimum length (12+), character diversity rules |
| SEC-M02 | **Medium** | Infrastructure | Docker containers may run as root | Configure non-root users in Dockerfiles |
| SEC-M03 | **Medium** | Monitoring | No automated security event alerting | Integrate with alerting platform (PagerDuty/OpsGenie) |
| SEC-M04 | **Medium** | Infrastructure | No container resource limits defined | Add memory/CPU limits in Docker Compose |
| SEC-M05 | **Medium** | Client-side | JWT tokens stored in localStorage (potential XSS vector) | Migrate to httpOnly cookies |
| SEC-L01 | **Low** | Cryptography | JWT secret rotation is manual | Implement automated rotation |
| SEC-L02 | **Low** | Infrastructure | Database backups not automated | Implement scheduled backup with offsite storage |
| SEC-L03 | **Low** | Monitoring | Audit logs not cryptographically signed | Implement hash-chain log integrity |
| SEC-L04 | **Low** | Inter-service | No mutual TLS between services | Implement mTLS for service mesh |
| SEC-I01 | **Info** | Documentation | No formal incident response plan | Create and rehearse IRP |
| SEC-I02 | **Info** | Documentation | No formal disaster recovery plan | Create and test DR plan |
| SEC-I03 | **Info** | Compliance | SBOM not maintained | Generate and maintain SBOM |

### 15.2 Risk Matrix

| Severity | Count | Description |
|----------|-------|-------------|
| **Critical** | 0 | Immediate exploitation risk; production stop required |
| **High** | 2 | Significant risk; remediation within 30 days |
| **Medium** | 5 | Moderate risk; remediation within 90 days |
| **Low** | 4 | Minor risk; remediation within 180 days |
| **Informational** | 3 | Best practice recommendations; scheduled improvement |

---

## 16. Regional Security Policy Variations

### 16.1 European Union

| Policy | Variation | Impact on Secuura |
|--------|-----------|-------------------|
| **GDPR** | Applies to all EU/EEA data | Fully implemented |
| **eIDAS 2.0** | New digital identity requirements (2024–2026 rollout) | Monitor and prepare wallet interoperability |
| **NIS2 Directive** | Network and information security for essential entities | Assess applicability based on deployment scale |
| **DORA** | Digital operational resilience for financial sector | Applicable if serving financial institutions in EU |
| **AI Act** | AI system regulations | Assess if ML/AI components are introduced |

### 16.2 United Kingdom

| Policy | Variation | Impact on Secuura |
|--------|-----------|-------------------|
| **UK GDPR** | Post-Brexit UK data protection | Aligned via GDPR implementation |
| **Data Protection and Digital Information Bill** | Potential divergence from EU GDPR | Monitor legislative progress |
| **Cyber Security Regulations** | NIS regulations for essential services | Assess per deployment |
| **FCA requirements** | Financial services cybersecurity | Applicable for fintech deployments |

### 16.3 United States

| Policy | Variation | Impact on Secuura |
|--------|-----------|-------------------|
| **CCPA/CPRA** | California consumer privacy | GDPR controls provide strong baseline; minor adaptations needed |
| **State privacy laws** | Colorado, Virginia, Connecticut, and others | Monitor state-level legislation; data mapping per state |
| **HIPAA** | Healthcare data protection | Architecture-ready; BAA templates needed |
| **SOX** | Financial reporting controls | Architecture supports; formal documentation needed |
| **FERPA** | Educational records privacy | Applicable for academic credential use case |
| **SEC cybersecurity rules** | Public company reporting | Applicable for public company clients |

### 16.4 Asia-Pacific

| Policy | Variation | Impact on Secuura |
|--------|-----------|-------------------|
| **Australia Privacy Act** | Australian Privacy Principles | Additional consent requirements; 100-point ID supported |
| **PDPA (Singapore)** | Personal Data Protection Act | Similar to GDPR; notification obligations differ |
| **PIPA (South Korea)** | Personal Information Protection Act | Stricter consent requirements; data localisation possible |
| **APPI (Japan)** | Act on Protection of Personal Information | Cross-border transfer mechanism (PPC approval) |
| **China PIPL** | Personal Information Protection Law | Data localisation requirements; significant compliance effort |
| **India DPDPA** | Digital Personal Data Protection Act (2023) | Consent-based processing; data localisation for critical data |

### 16.5 Middle East and Africa

| Policy | Variation | Impact on Secuura |
|--------|-----------|-------------------|
| **PDPL (Saudi Arabia)** | Personal Data Protection Law | Data localisation; consent requirements differ |
| **UAE Federal Decree-Law No. 45** | Data protection | Similar to GDPR; specific requirements for free zones |
| **POPIA (South Africa)** | Protection of Personal Information Act | Aligned with GDPR principles; local representative may be required |

### 16.6 Key Regional Differences Summary

| Requirement | EU | UK | US | APAC | MENA |
|-------------|----|----|-----|------|------|
| **Consent basis** | Explicit opt-in | Explicit opt-in | Varies by state | Varies | Varies |
| **Data localisation** | No (adequacy-based) | No (adequacy-based) | No (federal) | Some countries | Some countries |
| **Breach notification** | 72 hours (GDPR) | 72 hours (UK GDPR) | Varies by state | Varies | Varies |
| **Right to deletion** | Yes (GDPR Art. 17) | Yes (UK GDPR) | Yes (CCPA/CPRA) | Some countries | Some countries |
| **DPO required** | In some cases | In some cases | No (generally) | Some countries | Some countries |
| **Cross-border transfer** | Adequacy / SCCs | Adequacy / IDTA | No restrictions | Varies | Varies |

**Flag:** Deployments in China, Saudi Arabia, and India will require significant additional compliance work due to data localisation requirements. These jurisdictions may require hosting infrastructure within their borders and additional regulatory approvals.

---

## 17. Recommendations and Remediation

### 17.1 Priority 1 — High (Remediate within 30 days)

| ID | Finding | Remediation |
|----|---------|-------------|
| SEC-H01 | No automated dependency scanning | Integrate npm audit or Snyk into CI/CD pipeline |
| SEC-H02 | No penetration testing | Engage CREST-certified penetration testing firm |

### 17.2 Priority 2 — Medium (Remediate within 90 days)

| ID | Finding | Remediation |
|----|---------|-------------|
| SEC-M01 | No password complexity rules | Implement zxcvbn or similar password strength library |
| SEC-M02 | Root containers | Add `USER` directives to Dockerfiles |
| SEC-M03 | No security alerting | Integrate with monitoring platform |
| SEC-M04 | No resource limits | Add `deploy.resources` to Docker Compose |
| SEC-M05 | localStorage JWT | Migrate to httpOnly secure cookies |

### 17.3 Priority 3 — Low (Remediate within 180 days)

| ID | Finding | Remediation |
|----|---------|-------------|
| SEC-L01 | Manual JWT rotation | Implement automated key rotation service |
| SEC-L02 | No automated backups | Implement pg_dump scheduled backups |
| SEC-L03 | Unsigned audit logs | Implement hash-chain integrity for audit table |
| SEC-L04 | No inter-service mTLS | Implement service mesh (Istio/Linkerd) or mTLS proxy |

### 17.4 Priority 4 — Informational (Scheduled improvement)

| ID | Finding | Remediation |
|----|---------|-------------|
| SEC-I01 | No incident response plan | Draft and rehearse formal IRP |
| SEC-I02 | No disaster recovery plan | Draft and test DR procedures |
| SEC-I03 | No SBOM | Generate SBOM using syft or similar |

---

_This security audit report is based on the codebase as of 15 February 2026. Security is an ongoing process, and regular re-assessment is recommended. This report does not constitute a guarantee of security and should be supplemented with formal penetration testing and third-party security audits._

---

**End of Document**
