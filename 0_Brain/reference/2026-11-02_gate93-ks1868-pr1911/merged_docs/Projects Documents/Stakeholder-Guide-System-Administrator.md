# Secuura — System Administrator Guide

**Platform Administration, Monitoring, and Configuration**

**Document Title:** System Administrator Guide  
**Version:** 1.0  
**Date:** 15 February 2026  
**Classification:** Confidential — System Administrators Only  
**Prepared by:** Secuura

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura | Initial system administrator guide |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Platform Overview](#2-platform-overview)
3. [Getting Started](#3-getting-started)
4. [Admin Dashboard](#4-admin-dashboard)
5. [User Management](#5-user-management)
6. [Organisation Management](#6-organisation-management)
7. [Document Type Configuration](#7-document-type-configuration)
8. [Workflow Management](#8-workflow-management)
9. [System Health Monitoring](#9-system-health-monitoring)
10. [GDPR Administration](#10-gdpr-administration)
11. [Audit Logs](#11-audit-logs)
12. [API Key Management](#12-api-key-management)
13. [Pricing Configuration](#13-pricing-configuration)
14. [Security Administration](#14-security-administration)
15. [Troubleshooting](#15-troubleshooting)
16. [Frequently Asked Questions](#16-frequently-asked-questions)
17. [Support](#17-support)

---

## 1. Executive Summary

As a System Administrator, you are responsible for the configuration, monitoring, and maintenance of the Secuura platform. This guide covers all administrative functions available through the Admin Dashboard, including user management, system health monitoring, GDPR compliance administration, audit log review, and platform configuration.

**Your key responsibilities:**
- Manage users, organisations, and access permissions
- Monitor system health and resolve errors
- Process GDPR data subject requests
- Configure document types, workflows, and pricing
- Review audit logs for security and compliance
- Manage API keys for third-party integrations
- Ensure platform availability and security

---

## 2. Platform Overview

### Architecture

Secuura consists of 22 services (19 backend microservices and 3 frontend portals), all accessible through a unified Nginx gateway on port 8882 (with the Marketing Website on port 8881):

| Component | Port/URL | Purpose |
|-----------|----------|---------|
| API Gateway | `http://localhost:8882/api/` | Central routing, rate limiting, security |
| Originate | 4000 | Document certification, GDPR, pricing |
| Auth | 4003 | Authentication, JWT, MFA |
| Anchoring | 4005 | Blockchain transaction submission |
| PostgreSQL | 5432 | Primary database |
| Redis | 6379 | Caching, sessions, rate limiting |
| Nginx Gateway | 8882 | Frontend proxy for all apps |
| Issuer Portal | `http://localhost:8882/` | Issuer portal |
| Verifier Portal | `http://localhost:8882/verify/` | Public verification |
| Admin Dashboard | `http://localhost:8882/admin/` | Administration dashboard |
| Status Page | `http://localhost:8882/status/` | Public status page |
| Marketing Website | `http://localhost:8881` | Tokenomics and marketing |

### Infrastructure

All services run as Docker containers orchestrated via Docker Compose. The Nginx gateway on port 8882 serves as the unified entry point for all frontend applications.

---

## 3. Getting Started

### Accessing the Admin Dashboard

1. Navigate to the Admin Dashboard: `http://localhost:8882/admin/`
2. Log in with your SYSTEM_ADMIN credentials
3. Complete MFA verification if enabled

### Required Permissions

The Admin Dashboard requires the `SYSTEM_ADMIN` role. This is the highest-privilege role in the platform.

| Role | Access Level |
|------|-------------|
| SYSTEM_ADMIN | Full platform administration |
| ORG_ADMIN | Organisation-level management only |
| Other roles | No admin dashboard access |

---

## 4. Admin Dashboard

### Dashboard Overview

The main dashboard provides a high-level view of platform activity:

- **Total Users** — Number of registered users across all organisations
- **Total Documents** — Number of certifications in the system
- **Active Organisations** — Number of organisations using the platform
- **Recent Activity** — Latest certifications, verifications, and system events

### Navigation

| Section | Purpose |
|---------|---------|
| **Dashboard** | Platform overview and statistics |
| **Users** | User account management |
| **Organisations** | Organisation management |
| **Document Types** | Configure certifiable document types |
| **Workflows** | Define certification workflows |
| **Verification Queue** | Pending verification requests |
| **System Health** | Error monitoring, service health, GDPR status |
| **Audit Logs** | Activity logging and compliance |
| **API Keys** | Manage programmatic access |
| **Reports** | Analytics and reporting |
| **Settings** | Platform configuration |
| **Integration Hub** | Third-party integrations |

---

## 5. User Management

### Viewing Users

The Users page shows all registered users with:
- Name and email
- Organisation membership
- Role(s) assigned
- Verification level
- Account status (active, disabled, deleted)
- Last login date

### Creating Users

**Via Admin Dashboard:**

1. Navigate to Users
2. Click "Create User"
3. Enter user details (name, email, organisation)
4. Assign role(s)
5. Click "Create"
6. User receives an invitation email

**Via API:**

```bash
curl -X POST /api/admin/users \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@organisation.com",
    "firstName": "Jane",
    "lastName": "Doe",
    "role": "ISSUER_ADMIN",
    "organizationId": "org_123"
  }'
```

### Managing Users

| Action | How |
|--------|-----|
| **Disable account** | Users > Select user > Click "Disable" |
| **Change role** | Users > Select user > Edit role assignment |
| **Reset MFA** | Users > Select user > "Reset MFA" |
| **View activity** | Users > Select user > "Activity Log" |

---

## 6. Organisation Management

### Creating Organisations

1. Navigate to Organisations
2. Click "Create Organisation"
3. Enter organisation details:
   - Name
   - Type (Enterprise, Education, Government, Healthcare, etc.)
   - Contact information
   - Subscription tier
4. Assign an Organisation Admin
5. Click "Create"

### Organisation Settings

For each organisation, you can configure:
- **Member management** — Add/remove users
- **Usage limits** — Maximum certifications per period
- **Billing tier** — Subscription level
- **Document types** — Which types this organisation can certify
- **Verification requirements** — Minimum verification level for operations

---

## 7. Document Type Configuration

### Overview

Document Types define the categories of documents that can be certified on the platform. Each type has configurable properties.

### Managing Document Types

1. Navigate to Document Types
2. View existing types or click "Add Document Type"
3. Configure:

| Field | Description |
|-------|-------------|
| **Name** | Display name (e.g., "Degree Certificate") |
| **Code** | Unique identifier (e.g., `degree_certificate`) |
| **Category** | Grouping (Education, Employment, Legal, etc.) |
| **Description** | What this document type represents |
| **Required Fields** | Metadata fields required for this type |
| **Verification Level** | Minimum verification level to certify |
| **Active** | Whether this type is available for use |

### API Integration

Document types are stored in the database and managed via API:

```bash
# List all document types
GET /api/admin/document-types

# Create a new document type
POST /api/admin/document-types

# Update a document type
PUT /api/admin/document-types/:id

# Delete a document type
DELETE /api/admin/document-types/:id
```

---

## 8. Workflow Management

### Overview

Workflows define the certification process for different document types. A workflow specifies the steps, approvals, and automations required to certify a document.

### Managing Workflows

1. Navigate to Workflows
2. View existing workflows or click "Add Workflow"
3. Configure:

| Field | Description |
|-------|-------------|
| **Name** | Workflow name (e.g., "Standard Certification") |
| **Description** | What this workflow does |
| **Steps** | Ordered list of workflow steps |
| **Triggers** | What initiates the workflow |
| **Approvers** | Who can approve at each step |
| **Active** | Whether this workflow is available |

---

## 9. System Health Monitoring

### Overview

The System Health page provides real-time monitoring of platform status.

### Error Dashboard

| Section | What It Shows |
|---------|--------------|
| **Error Statistics** | Total errors, error rate, errors by severity |
| **Error Table** | Filterable list of system errors with details |
| **Service Status** | Health of each microservice |

### Error Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| **Critical** | Service outage or data integrity issue | Immediate investigation required |
| **Error** | Operation failure affecting users | Investigate within hours |
| **Warning** | Potential issue or degradation | Monitor and investigate if recurring |

### Resolving Errors

1. Navigate to System Health
2. Review the error table (filterable by severity, service, and date)
3. Click an error to expand details (stack trace, request path, user ID)
4. Click "Resolve" to mark an error as resolved
5. Add resolution notes for audit trail

### Service Health Endpoints

Each service exposes a health endpoint:

| Service | Health Endpoint |
|---------|----------------|
| API Gateway | `GET /health` |
| Originate | `GET /health` |
| Auth | `GET /health` |
| Anchoring | `GET /health` |

---

## 10. GDPR Administration

### Data Subject Requests (DSR)

The System Health page also shows pending GDPR Data Subject Requests:

| DSR Type | Description | Deadline |
|----------|-------------|----------|
| **Access** | User requests copy of their data | 30 days |
| **Erasure** | User requests data deletion | 30 days |
| **Portability** | User requests data export | 30 days |
| **Rectification** | User requests data correction | 30 days |
| **Restriction** | User requests processing limitation | 30 days |
| **Objection** | User objects to data processing | 30 days |

### Processing DSRs

1. Navigate to System Health > GDPR DSR section
2. Review pending requests
3. For each request:
   - Verify the requestor's identity
   - Process the request via the API
   - Update the DSR status
   - Ensure completion within the 30-day deadline

### Key GDPR API Endpoints

```bash
# View pending DSRs
GET /api/gdpr/dsr/pending

# Process a DSR
PATCH /api/gdpr/dsr/:dsrId

# Execute data erasure
POST /api/gdpr/erasure/:userId

# Export user data
GET /api/gdpr/export/:userId

# View deletion log
GET /api/gdpr/deletion-log
```

### Data Retention Policies

View and manage data retention policies:

| Data Type | Default Retention | Deletion Method |
|-----------|-------------------|-----------------|
| User sessions | 90 days | Hard delete |
| Audit logs | 365 days | Anonymise |
| Verification requests | 180 days | Hard delete |
| System errors | 90 days | Hard delete |
| Share records | 365 days | Hard delete |

Retention enforcement runs automatically on a daily schedule.

---

## 11. Audit Logs

### Overview

The Audit Logs page provides a comprehensive record of all significant platform actions.

### What is Logged

| Action Category | Examples |
|----------------|---------|
| **Authentication** | Logins, logouts, failed attempts, MFA events |
| **Certification** | Document creation, signing, anchoring, revocation |
| **Verification** | Verification attempts and results |
| **Administration** | User creation, role changes, configuration changes |
| **GDPR** | DSR creation, processing, erasure execution |
| **Security** | Rate limit breaches, suspicious requests, brute-force attempts |

### Filtering Audit Logs

- **Date range** — Filter by time period
- **Action type** — Filter by action category
- **User** — Filter by specific user
- **Resource** — Filter by specific document or entity
- **Severity** — Filter by log level

### Exporting Audit Logs

Audit logs can be exported for compliance reporting and external audit:

```bash
GET /api/admin/audit?from=2026-01-01&to=2026-02-15&format=json
```

---

## 12. API Key Management

### Overview

API keys enable programmatic access to the Secuura platform. Each key is scoped to specific operations and rate-limited.

### Creating API Keys

1. Navigate to API Keys
2. Click "Generate New Key"
3. Configure:
   - Key name (descriptive identifier)
   - Organisation (which organisation the key belongs to)
   - Scopes (which operations the key can perform)
   - Rate limit (requests per period)
   - Expiration (optional)
4. Click "Generate"
5. **Copy the key immediately** — it is shown only once

### Key Security

- API keys are stored as hashes (not plaintext) in the database
- Each key is scoped to specific operations
- Rate limiting is enforced per key
- Keys can be revoked at any time

---

## 13. Pricing Configuration

### Overview

Chargeable event pricing is stored in the database and can be configured per deployment.

### Managing Pricing

```bash
# View current pricing
GET /api/admin/pricing

# Update pricing for an event type
PATCH /api/admin/pricing/:eventType
{
  "adaAmount": 5.0,
  "usdAmount": 2.50,
  "typicalPayer": "issuer"
}

# Refresh pricing cache
POST /api/admin/pricing/refresh
```

### Default Pricing

| Event Type | ADA | USD | Typical Payer |
|-----------|-----|-----|---------------|
| certification_issued | 5.0 | 2.50 | Issuer |
| certification_signed | 2.0 | 1.00 | Certifier |
| verification_passed | 1.5 | 0.75 | Verifier |
| verification_failed | 0.5 | 0.25 | Verifier |
| document_shared | 0.5 | 0.25 | Owner |
| rights_transferred | 3.0 | 1.50 | Transferor |
| certification_revoked | 1.0 | 0.50 | Certifier |

---

## 14. Security Administration

### Security Monitoring

Monitor for:
- Failed authentication attempts (review in Audit Logs)
- Rate limit breaches (logged in system errors)
- Unusual certification volumes (check Analytics)
- Brute-force attempts (check System Health errors)
- Wallet connection anomalies

### Security Configuration

| Setting | Location | Default |
|---------|----------|---------|
| Rate limiting (global) | API Gateway config | 100 req/min |
| Rate limiting (auth) | API Gateway config | 10 req/15 min |
| Rate limiting (verification) | API Gateway config | 200 req/min |
| Brute-force threshold | API Gateway config | 5 free retries |
| Brute-force lockout | API Gateway config | 5 minutes |
| JWT token lifetime | Auth service config | Configurable |
| CORS origins | Service config | Whitelist-based |
| CSP policy | Helmet.js config | Strict |

### Security Incident Checklist

If a security incident is suspected:

1. Review system error logs (System Health > Error Table)
2. Check audit logs for the affected time period
3. Identify affected users and resources
4. Disable compromised accounts if necessary
5. Rotate affected credentials (JWT secret, API keys)
6. Document the incident with timeline and impact
7. Notify affected parties per GDPR breach notification requirements (72 hours)
8. Conduct post-incident review

---

## 15. Troubleshooting

### Common Issues

| Issue | Possible Cause | Resolution |
|-------|---------------|------------|
| Service unavailable | Container not running | Check Docker container status; restart if needed |
| Database connection error | PostgreSQL not healthy | Check PostgreSQL health; verify connection string |
| Redis connection error | Redis not accessible | Check Redis health; service falls back to in-memory |
| Authentication failures | Missing/invalid JWT keypair | Verify `JWT_PRIVATE_KEY` (auth) and `JWT_PUBLIC_KEY` (services) are set — RS256 keypair |
| Blockchain anchoring failing | Cardano node unavailable | Check Cardano devnet/network status |
| Rate limiting too aggressive | Misconfigured limits | Adjust rate limit settings |
| CORS errors | Origin not whitelisted | Add origin to CORS_ORIGINS configuration |

### Docker Container Management

```bash
# View running containers
docker compose ps

# View service logs
docker compose logs <service-name> --tail 100

# Restart a specific service
docker compose restart <service-name>

# Rebuild and restart
docker compose up -d --build <service-name>

# Check container health
docker inspect --format='{{.State.Health.Status}}' <container-name>
```

### Database Inspection

```bash
# Connect to PostgreSQL
docker exec -it secuura-postgres psql -U secuura -d secuura

# Common queries
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM documents;
SELECT COUNT(*) FROM certification_events;
SELECT * FROM system_errors WHERE resolved = false ORDER BY created_at DESC LIMIT 10;
```

---

## 16. Frequently Asked Questions

**Q: How do I add a new administrator?**  
A: Create a new user with the `SYSTEM_ADMIN` role. Only existing system administrators can assign this role.

**Q: How do I reset a user's password?**  
A: Currently handled via the Auth service. The user can use the "Forgot Password" flow, or you can trigger a password reset via the API.

**Q: How do I view blockchain transactions?**  
A: Use the Cardano Explorer links provided in certification records. For mainnet: cardanoscan.io, for preview: preview.cardanoscan.io.

**Q: How are backups handled?**  
A: PostgreSQL data is stored in Docker volumes. Implement scheduled `pg_dump` backups for production. Redis persistence (AOF + RDB) provides cache durability.

**Q: What happens during a service restart?**  
A: Services handle graceful shutdown (SIGTERM), draining active connections. Stateless services resume immediately. Pending blockchain transactions are tracked and can be retried.

---

## 17. Support

- **Documentation:** docs.secuura.io
- **API Reference:** api.secuura.io/docs
- **Email Support:** support@secuura.io
- **Status Page:** status.secuura.io

---

_Copyright 2026 Secuura. All rights reserved._

---

**End of Document**
