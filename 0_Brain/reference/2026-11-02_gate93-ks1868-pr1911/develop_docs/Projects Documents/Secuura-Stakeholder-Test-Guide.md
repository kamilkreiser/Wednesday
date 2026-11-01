# Secuura Platform — Stakeholder & Usability Test Guide

---

| **Document** | Stakeholder & Usability Test Guide |
|---|---|
| **Version** | 1.0.0 |
| **Date** | 15 February 2026 |
| **Classification** | Internal — Confidential |
| **Author** | Secuura Engineering |
| **Status** | Active |

---

## Version History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0.0 | 15 Feb 2026 | Engineering | Initial release — all personas, happy-path flows |
| 1.1.0 | 17 Feb 2026 | Engineering | Added NFT Certificate minting flow to Issuer capabilities, Appendix C (Steps 6–6f), and cross-persona recruitment flow (Phase 3a) |
| 1.2.0 | 17 Feb 2026 | Engineering | Updated document registration flow for client-side hashing (SHA-256), updated auth flow for httpOnly cookies, added persistence and anchoring test steps |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Platform Overview](#2-platform-overview)
3. [How to Use This Document](#3-how-to-use-this-document)
4. [Persona 1 — System Administrator](#4-persona-1--system-administrator)
5. [Persona 2 — Organisation Administrator](#5-persona-2--organisation-administrator)
6. [Persona 3 — Issuer (Document Preparer)](#6-persona-3--issuer-document-preparer)
7. [Persona 4 — Certifier (Document Approver)](#7-persona-4--certifier-document-approver)
8. [Persona 5 — Rights Holder / Document Owner](#8-persona-5--rights-holder--document-owner)
9. [Persona 6 — Verifier](#9-persona-6--verifier)
10. [Persona 7 — Public / Anonymous User](#10-persona-7--public--anonymous-user)
11. [Cross-Persona Flow — Recruitment Use Case](#11-cross-persona-flow--recruitment-use-case)
12. [Appendix A — System Administrator Step-by-Step](#appendix-a--system-administrator-step-by-step)
13. [Appendix B — Organisation Administrator Step-by-Step](#appendix-b--organisation-administrator-step-by-step)
14. [Appendix C — Issuer Step-by-Step](#appendix-c--issuer-step-by-step)
15. [Appendix D — Certifier Step-by-Step](#appendix-d--certifier-step-by-step)
16. [Appendix E — Rights Holder Step-by-Step](#appendix-e--rights-holder-step-by-step)
17. [Appendix F — Verifier Step-by-Step](#appendix-f--verifier-step-by-step)
18. [Appendix G — Public User Step-by-Step](#appendix-g--public-user-step-by-step)
19. [Appendix H — End-to-End Recruitment Flow](#appendix-h--end-to-end-recruitment-flow)
20. [Appendix I — Test Environment Reference](#appendix-i--test-environment-reference)

---

## 1. Executive Summary

Secuura is a blockchain-anchored document authenticity platform built on Cardano. It enables organisations to issue, certify, and verify credentials with tamper-evident cryptographic proof. The platform uses W3C Verifiable Credentials and Atala PRISM decentralised identities to create an immutable chain of document provenance.

This document serves three purposes:

1. **Stakeholder Reference** — Defines each persona, their role within the platform, and the capabilities available to them.
2. **Usability Testing Script** — Provides step-by-step happy-path flows that can be followed by human testers to validate the user experience.
3. **Automated Test Blueprint** — Provides precise navigation paths, form fields, button labels, and expected outcomes that can be followed by Cursor or other automation tooling to build E2E test suites.

Each section follows a consistent structure inspired by ISO/IEC 25066 (Common Industry Format for Usability) and usability testing best practices from Nielsen Norman Group and Steve Krug's methodology.

---

## 2. Platform Overview

### Access Points

| Application | URL | Purpose |
|---|---|---|
| Issuer Portal | `http://localhost:6882/` | Document certification and management |
| Verifier Portal | `http://localhost:6882/verify/` | Public document verification |
| Admin Dashboard | `http://localhost:6882/admin/` | Platform administration |
| Status Page | `http://localhost:6882/status/` | Public system status monitoring |
| Marketing Website | `http://localhost:6881` | Tokenomics and public information |
| API Gateway | `http://localhost:6882/api/` | REST API for all services |

### Authentication

All authenticated portals use JWT-based authentication. Credentials are validated against the Auth service. Role-based access control (RBAC) enforces permissions at both API and UI levels.

### Test Credentials

| Persona | Email | Password | Portal |
|---|---|---|---|
| Demo Issuer | `demo@secuura.io` | `demo123` | Issuer Portal |
| Demo Admin | `admin@secuura.com` | `admin123` | Admin Dashboard |

---

## 3. How to Use This Document

### For Human Testers

Each persona section (Sections 4–10) provides a high-level introduction to the role, its purpose, and what the platform enables for that persona. The corresponding Appendix section provides a numbered, step-by-step walkthrough you can follow from login to task completion.

**Template for each step:**

> **Step N: [Action Title]**
> - **Navigate to:** [URL or UI path]
> - **Action:** [What to do — click, type, select, verify]
> - **Expected Result:** [What you should see]
> - **Pass Criteria:** [How to know the step succeeded]

### For Automated Testing (Cursor / Playwright)

Each Appendix step includes:
- Exact URLs for navigation
- Form field labels and expected input values
- Button text for click targets
- `data-testid` attributes where available
- Expected UI state after each action

Use these as the specification for writing Playwright or Cursor-driven E2E tests.

---

## 4. Persona 1 — System Administrator

### Purpose

The System Administrator is the highest-privilege user on the Secuura platform. They are responsible for the overall health, security, and configuration of the system. This persona typically belongs to the Secuura operations team or a client's IT department.

### Intended Outcome

The platform provides the System Administrator with centralised control over every operational aspect — from user and organisation management to GDPR compliance enforcement, system error monitoring, and blockchain network configuration. The goal is to ensure the platform operates securely, compliantly, and efficiently.

### Portal

**Admin Dashboard** — `http://localhost:6882/admin/`

### Capabilities

| Function | Page | Description |
|---|---|---|
| Dashboard Overview | `/` | View platform-wide statistics: total documents, verifications, active users, blockchain anchors. Charts for weekly activity, document distribution, top organisations. |
| Organisation Management | `/organizations` | Create, edit, suspend, and delete organisations. Search and filter. |
| User Management | `/users` | Create, edit, block/unblock users. Assign roles (Admin, Issuer, Verifier, User). Set verification levels. |
| System Health Monitoring | `/system-health` | View unresolved errors, error severity breakdown, GDPR data subject requests, retention policy enforcement. Resolve errors by service. |
| GDPR Compliance | `/system-health` (Tab 1) | Review pending DSRs (erasure, access, portability), process requests within deadline. |
| Data Retention | `/system-health` (Tab 2) | View and enforce retention policies. Trigger manual retention enforcement. |
| API Key Management | `/api-keys` | Create, revoke, and manage API keys. Assign permissions (read, write, verify, admin). |
| Audit Logs | `/audit-logs` | Search, filter, and export audit logs by category (Document, Auth, Security, Verification, Blockchain, Access). |
| Reports | `/reports` | Generate usage reports, GDPR compliance reports, monthly summaries, and blockchain anchoring reports in PDF/CSV/JSON/Excel. |
| Platform Settings | `/settings` | Configure platform name, support email, blockchain network, session timeout, MFA requirements, rate limits, notification preferences, third-party integrations (Blockfrost, Entra ID, KYC providers). |

### Differentiator from Organisation Administrator

The System Administrator has exclusive access to:
- GDPR erasure execution (`/api/admin/gdpr/erasure/:userId`)
- Retention policy enforcement (`/api/admin/gdpr/retention/enforce`)
- Platform-wide settings (blockchain network, security policies)
- All organisations (not scoped to a single org)

---

## 5. Persona 2 — Organisation Administrator

### Purpose

The Organisation Administrator manages the configuration and day-to-day operations of their organisation within the Secuura platform. They define what types of documents their organisation handles, how certification workflows operate, and who has access.

### Intended Outcome

The platform enables Organisation Administrators to tailor the certification process to their organisation's specific needs — configuring document types with custom metadata schemas, building multi-step approval workflows, managing verification queues, and connecting external systems (document storage, identity providers, blockchain networks).

### Portal

**Admin Dashboard** — `http://localhost:6882/admin/`

### Capabilities

| Function | Page | Description |
|---|---|---|
| Document Type Configuration | `/document-types` | Create and manage document types with custom metadata schemas. Configure verification levels per role, authentication requirements (MFA, wallet signature, KYC), blockchain anchoring settings, and integration webhooks. Use recruitment quick-start templates. |
| Workflow Builder | `/workflows` | Design approval workflows (sequential, parallel, conditional). Add steps: Approval, Notification, Condition, Blockchain Anchor, Wallet Signature. Set SLAs and escalation rules. |
| Verification Queue | `/verification-queue` | Review pending documents, assign verifiers, approve/reject verifications. Monitor SLA compliance with visual indicators (at-risk, breached). |
| Integration Hub | `/integrations` | Connect document sources (SharePoint, S3, Google Cloud), identity providers (Entra ID, Auth0, Okta), verification services (Onfido, Jumio), and blockchain networks (Blockfrost, Ogmios). Test connections. |
| GDPR DSR Management | `/system-health` (Tab 1) | Review and process data subject requests (access, erasure, portability) for users within their organisation. |
| Reporting | `/reports` | Generate organisation-scoped usage and compliance reports. |

---

## 6. Persona 3 — Issuer (Document Preparer)

### Purpose

The Issuer is the starting point of every certification in the Secuura platform. They are typically an administrative staff member at an educational institution, professional body, or government agency who prepares documents for formal certification.

### Intended Outcome

The platform enables Issuers to upload documents, enrich them with metadata, and initiate the certification process. Once uploaded, documents enter the certification workflow where they can be reviewed, signed, and anchored to the Cardano blockchain — creating a permanent, tamper-evident record of authenticity.

### Portal

**Issuer Portal** — `http://localhost:6882/`

### Capabilities

| Function | Page | Description |
|---|---|---|
| Dashboard | `/` | View document statistics (total, certified, pending, on-chain). See recent documents and quick actions. |
| Document Upload | `/documents/new` | Upload files (drag-and-drop or click, max 50MB). Set title, type (Certificate, Degree/Diploma, Deed/Title, Contract, Reference Letter, Other), and description. |
| Document List | `/documents` | Browse all documents with status indicators (Draft, Pending, Certified). Navigate to detail view. |
| Document Detail | `/documents/:id` | View document metadata, content hash (BLAKE2b), signatures, and blockchain anchors. Initiate signing, anchoring, sharing, and recertification. |
| Document Lineage | `/documents/:id/lineage` | Interactive graph visualisation of the document's full provenance chain — every stakeholder, action, and cryptographic proof. Step-through timeline, scenario toggles (revocation), date filtering, evidence export. |
| Wallet Connection | `/wallet` | Connect a Cardano wallet (Nami, Eternl, Lace, Flint, Typhon, GeroWallet, NuFi) for document signing. |
| NFT Certificate Minting | `/documents/:id` → Save as NFT | Mint a certified document as a CIP-25 NFT on Cardano. 4-step wizard: Connect Wallet → Storage Tier → Privacy → Review & Mint. Supports Basic (~1.5 ADA), Standard (~2.0 ADA), and Premium (~2.5–3 ADA) tiers with configurable privacy levels. Requires CIP-30 wallet (Lace, Nami, Eternl, etc.). |
| Settings | `/settings` | Manage notification preferences. View blockchain network and API configuration. |

---

## 7. Persona 4 — Certifier (Document Approver)

### Purpose

The Certifier is the authority who formally signs and certifies a document. This persona validates the authenticity and accuracy of a document before applying their cryptographic signature — acting as an authoritative witness in the provenance chain.

### Intended Outcome

The platform enables Certifiers to review pending documents, verify their content and metadata, and then sign them using their Cardano wallet. This certification creates an immutable record on the blockchain, providing verifiable proof that an authorised party vouched for the document's authenticity.

### Portal

**Issuer Portal** — `http://localhost:6882/` (same portal as Issuer, different permissions)

### Capabilities

| Function | Page | Description |
|---|---|---|
| Review Pending Documents | `/documents` | Filter and view documents in pending/draft status that require certification. |
| Document Detail Review | `/documents/:id` | Examine document metadata, content hash, and any existing signatures before certifying. |
| Sign Document | `/documents/:id` | Apply a cryptographic wallet signature to the document via the connected Cardano wallet. |
| Anchor to Blockchain | `/documents/:id` | Initiate blockchain anchoring to create the immutable on-chain record. |
| View Lineage | `/documents/:id/lineage` | Inspect the full provenance chain to understand the document's history before certifying. |
| Revoke Certification | *(via API)* | Withdraw a previously issued certification if the underlying document is found to be invalid. |

### Role Transition

A Verifier can become a Certifier by issuing a Verification Certificate (recertification). This is the `verifier → certifier` role transition visible in the lineage graph.

---

## 8. Persona 5 — Rights Holder / Document Owner

### Purpose

The Rights Holder is the individual or entity that a certified document pertains to — typically a candidate, student, or professional whose credential has been certified. They hold the rights to their certified documents and control who can access them.

### Intended Outcome

The platform empowers Rights Holders with sovereign control over their credentials. They can view their certified documents, share them selectively with recruiters or employers (with granular permission levels), transfer ownership rights, and manage their privacy preferences — all while maintaining a complete audit trail in the document lineage.

### Portal

**Issuer Portal** — `http://localhost:6882/` (logged in as document owner)

### Capabilities

| Function | Page | Description |
|---|---|---|
| View Owned Documents | `/documents` | See all documents where this user is the owner/rights holder. |
| Document Detail | `/documents/:id` | View full document metadata, hash, certification status, and blockchain proof. |
| Share Credentials | `/documents/:id` → Share Dialog | Share certified documents with one or more recipients. Set permission levels: View Only, Verify (can verify authenticity), Re-share (can verify and forward). Each share creates a lineage record. |
| View Lineage | `/documents/:id/lineage` | See the full chain of custody — who issued, certified, shared, and verified the document. |
| Transfer Rights | *(via transfer components)* | Delegate or transfer ownership rights to another party. |
| Privacy Preferences | *(via privacy components)* | Control data sharing, consent, and privacy settings. |
| Wallet Connection | `/wallet` | Connect a Cardano wallet to prove ownership of credentials. |

---

## 9. Persona 6 — Verifier

### Purpose

The Verifier is any party who needs to confirm the authenticity of a certified document. In the recruitment context, this is typically a recruiter or employer conducting background checks on candidate credentials.

### Intended Outcome

The platform provides Verifiers with instant, trustless verification of document authenticity. By uploading a file, entering a document ID, or scanning a QR code, the Verifier receives a definitive answer — AUTHENTIC or INVALID — backed by blockchain proof. No intermediary, no phone calls, no waiting days for manual checks.

### Portal

**Verifier Portal** — `http://localhost:6882/verify/`

### Capabilities

| Function | Page | Description |
|---|---|---|
| Verify by File Upload | `/` (Tab 0) | Drag-and-drop or click to upload a document file (PDF, images, up to 50MB). The system computes the content hash and matches it against the blockchain record. |
| Verify by Document ID | `/` (Tab 1) | Enter a document ID (e.g., `DOC-ABC123-XYZ789`) to look up its certification status directly. |
| Verify by QR Code | `/` (Tab 2) | Scan a QR code from a printed or digital document to verify instantly. *(Camera permission required)* |
| View Verification Result | `/result/:documentId` | See the verification status (AUTHENTIC/INVALID), verification checks (exists, hash valid, blockchain anchored, not revoked), issuer details, and full blockchain proof (transaction hash, block height, confirmed date). |
| Issue Verification Certificate | *(via Issuer Portal)* | After verifying, a Verifier can issue a Verification Certificate — transitioning from Verifier to Certifier role in the document lineage. This creates a secondary credential attesting to the verification. |

### Authentication

The Verifier Portal does **not require authentication** for basic verification. Any user can verify a document. However, issuing a Verification Certificate requires authentication via the Issuer Portal.

---

## 10. Persona 7 — Public / Anonymous User

### Purpose

The Public User represents any visitor to the Secuura platform who has not authenticated. This includes potential customers, partners, investors, and curious visitors exploring what Secuura offers.

### Intended Outcome

The platform provides Public Users with two experiences: (1) the ability to verify any document without creating an account, and (2) a comprehensive marketing and information site covering Secuura's tokenomics, staking tiers, roadmap, team, and whitepaper.

### Portals

| Application | URL | Description |
|---|---|---|
| Verifier Portal | `http://localhost:6882/verify/` | Document verification — no authentication required |
| Marketing Website | `http://localhost:6881` | Tokenomics, staking, roadmap, team, whitepaper, FAQ |

### Capabilities

| Function | Description |
|---|---|
| Document Verification | Full verification capability: upload file, enter ID, or scan QR. View blockchain proof. |
| Tokenomics Information | Token distribution, fee structure, staking tiers, and revenue model. |
| Staking Tiers | Compare Basic, Staker, Validator, and Partner tier benefits. |
| Roadmap | View 4-phase development roadmap from Foundation through Scale. |
| Whitepaper Access | Download the complete Secuura whitepaper, tokenomics deep-dive, and technical specification. |
| Community Links | Access Discord, Twitter, Telegram, and GitHub communities. |
| FAQ | Browse frequently asked questions about the platform, tokens, and technology. |

---

## 11. Cross-Persona Flow — Recruitment Use Case

The primary use case for Secuura is recruitment credential verification. The following table shows how all personas interact in a single end-to-end flow:

| Step | Actor | Stakeholder Role | Action | Platform |
|---|---|---|---|---|
| 1 | University Admin | Issuer | Uploads and prepares the academic credential | Issuer Portal |
| 2 | University Registrar | Certifier | Reviews and certifies the credential with wallet signature | Issuer Portal |
| 3 | System | — | Anchors the certification to Cardano blockchain | Automatic |
| 4 | Student/Candidate | Rights Holder | Receives notification, views and shares credential with recruiter | Issuer Portal |
| 5 | Recruiter | Verifier | Receives shared link, verifies the credential | Verifier Portal |
| 6 | Recruiter | Verifier → Certifier | Issues a Verification Certificate (re-certification) | Issuer Portal |
| 7 | Employer | Verifier | Verifies both the original credential and the recruiter's verification certificate | Verifier Portal |

---

## Appendix A — System Administrator Step-by-Step

### Scenario: Platform Setup and Monitoring

**Preconditions:** Docker containers running, database seeded.

---

**Step 1: Login to Admin Dashboard**
- **Navigate to:** `http://localhost:6882/admin/login`
- **Action:** Enter email `admin@secuura.com` in the "Email" field (`data-testid="email-input"`)
- **Action:** Enter password `admin123` in the "Password" field (`data-testid="password-input"`)
- **Action:** Click the **"Sign In"** button (`data-testid="login-btn"`)
- **Expected Result:** Redirected to Dashboard (`/`). Sidebar visible with "Secuura / Enterprise Admin" branding.
- **Pass Criteria:** Dashboard loads with 4 stat cards (Total Documents, Verifications, Active Users, Blockchain Anchors).

---

**Step 2: Review Dashboard**
- **Navigate to:** `/` (already here after login)
- **Action:** Observe the 4 stat cards at the top.
- **Action:** Scroll down to view the Weekly Activity chart and Documents by Type pie chart.
- **Expected Result:** All charts render. Recent Activity feed shows recent events.
- **Pass Criteria:** No blank/error states. Cards display numerical values.

---

**Step 3: Create an Organisation**
- **Navigate to:** Click **"Organizations"** in the sidebar (`data-testid="nav-organizations"`)
- **Action:** Click the **"Add Organization"** button (top-right).
- **Action:** In the dialog, enter:
  - Organisation Name: `Cambridge University`
  - Type: Select `Education`
  - Status: Select `Active`
- **Action:** Click **"Create"**.
- **Expected Result:** Dialog closes. New organisation appears in the DataGrid.
- **Pass Criteria:** Organisation row shows name "Cambridge University", type "Education", status "Active" chip.

---

**Step 4: Create a User**
- **Navigate to:** Click **"Users"** in the sidebar (`data-testid="nav-users"`)
- **Action:** Click the **"Add User"** button (top-right).
- **Action:** In the dialog, enter:
  - Name: `Dr. Sarah Mitchell`
  - Email: `sarah.mitchell@cambridge.ac.uk`
  - Organization: `Cambridge University`
  - Role: Select `Issuer`
  - Verification Level: Select `Enhanced`
- **Action:** Click **"Create"**.
- **Expected Result:** Dialog closes. New user appears in the DataGrid.
- **Pass Criteria:** User row shows name, email, role "Issuer", verification level "Enhanced" with green dot.

---

**Step 5: Monitor System Health**
- **Navigate to:** Click **"System Health"** in the sidebar (`data-testid="nav-system-health"`)
- **Action:** Observe the 4 stat cards (Unresolved Errors, Errors 24h, Pending DSRs, Active Retention Policies).
- **Action:** Click on the **"System Errors"** tab (Tab 0).
- **Action:** Filter by Service: select `originate`.
- **Action:** If errors are present, expand a row to view the stack trace.
- **Expected Result:** Error table loads. Expandable rows show full error details.
- **Pass Criteria:** No page crash. Error cards display counts.

---

**Step 6: Review GDPR DSRs**
- **Navigate to:** Click the **"GDPR / DSRs"** tab (Tab 1) on System Health.
- **Action:** Observe the table of data subject requests.
- **Expected Result:** Table shows any pending DSRs with type, email, status, deadline, and days remaining.
- **Pass Criteria:** Table renders. Urgent items (<=7 days) are highlighted.

---

**Step 7: Review Audit Logs**
- **Navigate to:** Click **"Audit Logs"** in the sidebar (`data-testid="nav-audit-logs"`)
- **Action:** Use the search field to search for `Document`.
- **Action:** Filter by Category: select `Document`.
- **Action:** Filter by Status: select `Success`.
- **Expected Result:** Filtered audit log entries appear in the DataGrid.
- **Pass Criteria:** Rows display timestamp, category chip, action, user, and status.

---

**Step 8: Generate a Report**
- **Navigate to:** Click **"Reports"** in the sidebar (`data-testid="nav-reports"`)
- **Action:** Click the **"Usage Report"** template card.
- **Action:** Select Time Period: `Last 30 Days`.
- **Action:** Select Format: `PDF`.
- **Action:** Click **"Generate Report"**.
- **Expected Result:** Report appears in the Generated Reports list with status "Ready".
- **Pass Criteria:** "Download" button appears next to the generated report.

---

**Step 9: Configure Platform Settings**
- **Navigate to:** Click **"Settings"** in the sidebar (`data-testid="nav-settings"`)
- **Action:** On the **General** tab, verify Platform Name is "Secuura".
- **Action:** Switch to the **Security** tab. Verify "Require MFA for Admin Users" is toggled on.
- **Action:** Switch to the **Notifications** tab. Toggle "Verification Completed" email notification on.
- **Action:** Click **"Save Settings"**.
- **Expected Result:** Success alert: "Settings saved successfully!"
- **Pass Criteria:** Settings persist on page reload.

---

**Step 10: Manage API Keys**
- **Navigate to:** Click **"API Keys"** in the sidebar (`data-testid="nav-api-keys"`)
- **Action:** Click **"Create API Key"**.
- **Action:** Enter:
  - Key Name: `Production API`
  - Organization: Select any
  - Permissions: Click `Read`, `Verify`
- **Action:** Click **"Generate Key"**.
- **Expected Result:** "API Key Generated" dialog appears with the key. Warning to copy now.
- **Action:** Click the Copy icon. Click **"Done"**.
- **Pass Criteria:** API key row appears in the DataGrid with status "Active".

---

**Step 11: Logout**
- **Action:** Click the avatar in the top-right AppBar.
- **Action:** Click **"Logout"** from the dropdown menu.
- **Expected Result:** Redirected to `/login`.
- **Pass Criteria:** Login form is displayed.

---

## Appendix B — Organisation Administrator Step-by-Step

### Scenario: Configure Document Types and Workflows

**Preconditions:** Logged into Admin Dashboard as an `ORG_ADMIN` user.

---

**Step 1: Login**
- Follow Step 1 from Appendix A using organisation admin credentials.

---

**Step 2: Create a Document Type**
- **Navigate to:** Click **"Document Types"** in the sidebar (`data-testid="nav-document-types"`)
- **Action:** Click the **"Academic Degree"** quick-start template card (blue).
- **Expected Result:** "Create Document Type" dialog opens pre-populated with template values.
- **Action:** Review and modify:
  - Name: `BSc Computer Science`
  - Code: `BSC_CS` (auto-uppercased)
  - Description: `Bachelor of Science in Computer Science`
  - Category: Confirm `Education` is selected
  - Active: Confirm toggle is on
- **Action:** Switch to the **Verification** tab.
- **Action:** Set Document Creator verification to `Enhanced (Federated)`.
- **Action:** Toggle on "Require Cardano Wallet Signature (CIP-8)".
- **Action:** Switch to the **Metadata** tab.
- **Action:** Click **"Add Field"**. Enter: Field Name = `Grade`, Type = `Dropdown`, Required = on. Add options: `First,2:1,2:2,Third,Pass`.
- **Action:** Click **"Add Field"** again. Enter: Field Name = `Year of Graduation`, Type = `Number`, Required = on.
- **Action:** Switch to the **Workflow** tab.
- **Action:** Toggle "Requires Manual Approval" on.
- **Action:** Select Approval Workflow: `Multi-Signature 2 of 3`.
- **Action:** Toggle "Automatically Anchor to Blockchain" on.
- **Action:** Select Blockchain Network: `Cardano Preprod`.
- **Action:** Click **"Create Document Type"**.
- **Expected Result:** Dialog closes. Document type appears in the DataGrid.
- **Pass Criteria:** Row shows "BSc Computer Science", code "BSC_CS", category "Education", approval "Required", status "Active".

---

**Step 3: Create an Approval Workflow**
- **Navigate to:** Click **"Workflows"** in the sidebar (`data-testid="nav-workflows"`)
- **Action:** Click **"Create Workflow"**.
- **Action:** Enter:
  - Workflow Name: `Academic Credential Approval`
  - Workflow Type: `Sequential`
  - Description: `Multi-step approval for academic credentials`
  - SLA: `48`
  - Active: toggle on
- **Action:** Click **"Add Step"**. Configure Step 1:
  - Step Name: `Department Review`
  - Step Type: `Approval`
  - Approver Type: `Role-Based`
  - Required Approvals: `1`
  - Timeout: `24`
  - Escalate on Timeout: toggle on
- **Action:** Click **"Add Step"**. Configure Step 2:
  - Step Name: `Registrar Certification`
  - Step Type: `Wallet Signature`
- **Action:** Click **"Add Step"**. Configure Step 3:
  - Step Name: `Blockchain Anchor`
  - Step Type: `Blockchain Anchor`
- **Action:** Click **"Add Step"**. Configure Step 4:
  - Step Name: `Notify Rights Holder`
  - Step Type: `Notification`
  - Template: Select `credential-issued`
- **Action:** Click **"Create Workflow"**.
- **Expected Result:** Dialog closes. Workflow appears in the DataGrid.
- **Pass Criteria:** Row shows "Academic Credential Approval", type "Sequential", 4 steps, 48h SLA, "Active".

---

**Step 4: Configure Integrations**
- **Navigate to:** Click **"Integrations"** in the sidebar (`data-testid="nav-integrations"`)
- **Action:** Click the **"Identity Providers"** category card.
- **Action:** Click **"Add Provider"** in the Identity tab.
- **Action:** Enter:
  - Integration Name: `Cambridge Entra ID`
  - Provider: Select `Microsoft Entra ID`
  - Tenant ID: `cambridge-university-tenant-id`
  - Client ID: `client-id-here`
  - Client Secret: `client-secret-here`
  - Redirect URI: `https://secuura.io/auth/callback`
  - Active: toggle on
- **Action:** Click **"Test Connection"**.
- **Expected Result:** Connection test completes (may show error in dev — acceptable).
- **Action:** Click **"Add Integration"**.
- **Expected Result:** Integration card appears in the list with connected/disconnected status.
- **Pass Criteria:** Integration card shows name, provider label, and active toggle.

---

**Step 5: Manage Verification Queue**
- **Navigate to:** Click **"Verification Queue"** in the sidebar (`data-testid="nav-verification-queue"`)
- **Action:** Observe the 5 stat cards (Pending, In Review, Escalated, At Risk, SLA Breached).
- **Action:** Click the **View** icon on a pending document row.
- **Expected Result:** "Verification Details" dialog opens showing document info, status, priority, SLA, workflow, current step.
- **Action:** Type a note in the "Add Note" field: `Reviewed credentials — all checks passed.`
- **Action:** Click **"Approve"** (green button).
- **Expected Result:** Dialog closes. Document status updates in the DataGrid.
- **Pass Criteria:** Status changes from "Pending" to approved.

---

## Appendix C — Issuer Step-by-Step

### Scenario: Upload and Certify a Document

**Preconditions:** Logged into Issuer Portal.

---

**Step 1: Login to Issuer Portal**
- **Navigate to:** `http://localhost:6882/login`
- **Action:** Enter email `demo@secuura.io` in the "Email" field.
- **Action:** Enter password `demo123` in the "Password" field.
- **Action:** Click **"Sign In"** (or click **"Try Demo Account (Dev Only)"** for one-click demo login).
- **Expected Result:** Redirected to Dashboard. Sidebar shows "SECUURA" branding with navigation menu.
- **Pass Criteria:** Dashboard loads with stat cards and quick actions.

---

**Step 2: Register a New Document (Client-Side Hashing)**
- **Navigate to:** Click **"New Document"** in the sidebar (or top-right gradient button on Dashboard).
- **Expected Result:** Page heading reads **"Register New Document"** (not "Upload"). An informational alert is displayed: *"Your document is hashed locally in the browser. The file never leaves your device..."*
- **Action:** Drag a PDF file onto the dropzone area (or click to browse). Use any PDF file for testing.
- **Expected Result:** Filename appears below the dropzone icon.
- **Action:** Verify the "Document Title" field is auto-populated from the filename.
- **Action:** Select "Document Type": choose `Degree / Diploma`.
- **Action:** Enter description: `BSc Computer Science degree for John Smith, awarded July 2025.`
- **Action:** Click **"Register Document"**.
- **Expected Result:** A brief alert appears: *"Generating cryptographic hash of your document..."*. Then a green alert displays the computed SHA-256 hash (e.g., `sha256:e6c15ac940...`). A success dialog opens with the document ID and content hash.
- **Pass Criteria:** Document registered without any file upload. Network tab in DevTools confirms `POST /api/documents` sends JSON (not FormData). Content hash is a non-empty `sha256:...` string. Success dialog displays hash and document ID.

---

**Step 3: View Document Detail**
- **Navigate to:** Click "View Document" from the success dialog, or navigate from the Documents list.
- **Action:** Verify the following are displayed:
  - Document title
  - Document type: "Degree"
  - Content Hash (SHA-256): a long hexadecimal string prefixed with `sha256:`
  - Status chip (should be "Draft" for a newly registered document)
  - Description
- **Expected Result:** All metadata is present and correctly formatted. The hash matches the one shown during registration.
- **Pass Criteria:** Content hash is a non-empty `sha256:...` string. No error states visible.

---

**Step 4: View Document Lineage**
- **Action:** Click the **"View Lineage"** button (blue, AccountTree icon).
- **Expected Result:** Redirected to `/documents/:id/lineage`. Graph visualisation loads with nodes and edges.
- **Action:** Use the timeline controls at the bottom:
  - Click **Play** to auto-advance through steps.
  - Click **Next** to step forward manually.
  - Drag the slider to jump to a specific step.
- **Action:** Click on an edge (connection line) between two nodes.
- **Expected Result:** Evidence Panel drawer slides in from the right showing: action, timestamp, fee status, cryptographic anchor details.
- **Pass Criteria:** Graph renders with at least one node. Timeline controls are functional.

---

**Step 5: View Documents List**
- **Navigate to:** Click **"Documents"** in the sidebar.
- **Expected Result:** Document list table appears with the newly uploaded document.
- **Action:** Verify the document row shows: title, type, status chip, creation date.
- **Action:** Click the view icon (eye) on the row.
- **Expected Result:** Navigated back to Document Detail page.
- **Pass Criteria:** Document appears in the list with correct status.

---

**Step 6: Mint Document as NFT Certificate**

*Preconditions: Document is certified or has blockchain anchors. Cardano wallet (e.g., Lace) installed and configured on Preprod network with test ADA.*

- **Navigate to:** The document detail page for a certified document (`/documents/:id`).
- **Action:** Verify the **"Save as NFT"** button is visible (primary colour, Token icon). This button appears only when the document is certified or has blockchain anchors.
- **Action:** Click **"Save as NFT"**.
- **Expected Result:** "Save as NFT Certificate" modal opens with a 4-step Stepper: Connect Wallet → Storage Tier → Privacy → Review & Mint.
- **Pass Criteria:** Modal renders with all 4 steps visible in the stepper.

---

**Step 6a: Connect Wallet (Step 1 of wizard)**
- **Action:** If wallet is already connected, verify green checkmark and wallet details (name, address, balance, network chip). Click **"Continue"**.
- **Action:** If wallet is not connected, click **"Connect Wallet"**. In the wallet selector dialog, click **"Lace"** (or your installed wallet).
- **Expected Result:** Wallet extension popup appears requesting connection approval.
- **Action:** Approve the connection in the wallet extension.
- **Expected Result:** Wallet connected state shown with address, balance, and "Preprod" network chip.
- **Action:** Click **"Continue"**.
- **Pass Criteria:** Wallet info displayed correctly. Balance shows available ADA. Network is Preprod.

---

**Step 6b: Select Storage Tier (Step 2 of wizard)**
- **Action:** Three tier cards are displayed: Basic (~1.5 ADA), Standard (~2.0 ADA), Premium (~2.5–3 ADA).
- **Action:** Click the **"Standard"** card.
- **Expected Result:** Standard card gets a highlighted border and checkmark icon.
- **Action:** Click **"Continue"**.
- **Pass Criteria:** Selected tier is visually highlighted. Cost chip displays the estimated amount.

---

**Step 6c: Configure Privacy (Step 3 of wizard)**
- **Action:** Four privacy presets are shown as radio buttons: Full Privacy, Minimal, Partial, Verifiable.
- **Action:** Select **"Partial"** (document type, issuer, and date visible).
- **Expected Result:** "Partial" radio button is selected.
- **Action:** Optionally toggle **"Customize visible fields"** and check/uncheck individual fields.
- **Action:** Click **"Continue"**.
- **Pass Criteria:** Privacy selection persists. Custom field checkboxes toggle correctly.

---

**Step 6d: Review and Mint (Step 4 of wizard)**
- **Action:** Verify the summary card shows:
  - Wallet: wallet name and truncated address
  - Network: Preprod
  - Storage Tier: Standard
  - Privacy Level: Partial
  - Certificate: document type and issuer name
  - Estimated Cost: ~2.0 ADA
- **Action:** Read the info alert about signing the transaction.
- **Action:** Click **"Mint NFT"** (green button).
- **Expected Result:** Progress UI appears with status messages and progress bar:
  - "Retrieving wallet address..." (10%)
  - "Building minting policy..." (20%)
  - "Preparing metadata..." (35%)
  - "Building transaction..." (50%)
  - "Waiting for wallet signature..." (65%) — wallet extension popup appears
- **Action:** Approve the transaction in the wallet extension.
- **Expected Result:** Progress continues:
  - "Submitting to blockchain..." (80%)
  - "Transaction submitted! Waiting for confirmation..." (95%)
  - "Complete!" (100%)
- **Expected Result:** Success screen with green checkmark, "NFT Minted Successfully!" heading, and transaction details card.
- **Pass Criteria:** Tx Hash, Policy ID, Asset Name, and Asset ID are all populated. Copy and Cardanoscan link buttons are functional.

---

**Step 6e: Verify NFT on Cardanoscan (Optional)**
- **Action:** Click the **external link icon** next to the Tx Hash.
- **Expected Result:** New browser tab opens to `https://preprod.cardanoscan.io/transaction/{txHash}`.
- **Pass Criteria:** Transaction page loads on Cardanoscan (may take 20–60 seconds for confirmation).

---

**Step 6f: Close Modal**
- **Action:** Click **"Close"** to dismiss the modal.
- **Expected Result:** Modal closes. Document detail page is visible.
- **Pass Criteria:** No error states. Document page remains functional.

---

## Appendix D — Certifier Step-by-Step

### Scenario: Review and Certify a Pending Document

**Preconditions:** Logged into Issuer Portal as a user with `ISSUER_APPROVER` role. A document in pending status exists.

---

**Step 1: Login**
- Follow Step 1 from Appendix C using certifier credentials.

---

**Step 2: Find Pending Document**
- **Navigate to:** Click **"Documents"** in the sidebar.
- **Action:** Look for documents with a "Pending" status chip (yellow/warning colour).
- **Action:** Click the view icon on a pending document.
- **Expected Result:** Document Detail page loads.
- **Pass Criteria:** Document has status "Pending" or "Draft".

---

**Step 3: Review Document**
- **Action:** Review the document metadata:
  - Title
  - Document Type
  - Content Hash (BLAKE2b)
  - Description
- **Action:** Click **"View Lineage"** to inspect the provenance chain.
- **Action:** Navigate back to Document Detail.
- **Expected Result:** All information is accessible for review.
- **Pass Criteria:** No missing fields or error states.

---

**Step 4: Connect Wallet**
- **Navigate to:** Click **"Wallet"** in the sidebar.
- **Action:** Click the wallet of choice from the list (e.g., **Nami**).
- **Expected Result:** If the wallet extension is installed, a connection prompt appears. If not, an error message: "{wallet} wallet not found..."
- **Action:** Approve the connection in the wallet extension popup.
- **Expected Result:** "Connected" chip (green) appears. Wallet name and network displayed.
- **Pass Criteria:** Connected state is shown with wallet name.

---

**Step 5: Sign the Document**
- **Navigate to:** Return to the pending document's detail page (`/documents/:id`).
- **Action:** Click the **"Sign"** button.
- **Expected Result:** Wallet signature prompt appears in the connected wallet extension.
- **Action:** Approve the signature in the wallet.
- **Expected Result:** Signature appears in the Signatures section of the document detail.
- **Pass Criteria:** Signature row shows wallet address and "Verified" status.

---

**Step 6: Anchor to Blockchain**
- **Action:** Click the **"Anchor to Blockchain"** button.
- **Expected Result:** Button text changes to "Anchoring...". On completion, an anchor record appears in the Blockchain Anchors section.
- **Pass Criteria:** Anchor record shows network name, transaction hash (monospace), and status chip (confirmed = green).

---

## Appendix E — Rights Holder Step-by-Step

### Scenario: Share a Certified Document

**Preconditions:** Logged into Issuer Portal as the document owner. A certified document exists.

---

**Step 1: Login and Find Certified Document**
- Follow Step 1 from Appendix C.
- **Navigate to:** Click **"Documents"** in the sidebar.
- **Action:** Find a document with "Certified" status (green chip).
- **Action:** Click the view icon to open Document Detail.

---

**Step 2: Share the Document**
- **Action:** Click the **"Share"** button (secondary colour).
- **Expected Result:** "Share Document" dialog opens.
- **Action:** Enter first recipient:
  - Email: `recruiter@agency.com`
  - Name: `Jane Recruiter`
  - Permission Level: Select `Verify`
- **Action:** Click **"Add Another Recipient"**.
- **Action:** Enter second recipient:
  - Email: `hr@employer.com`
  - Name: `HR Department`
  - Permission Level: Select `View Only`
- **Action:** Click **"Share with 2 Recipient(s)"**.
- **Expected Result:** Button text changes to "Sharing...". Success alert appears: "Document shared successfully with 2 recipient(s)!"
- **Pass Criteria:** Dialog auto-closes after 2 seconds. Document lineage now shows share events.

---

**Step 3: Verify Lineage Updated**
- **Action:** Click **"View Lineage"** on the Document Detail page.
- **Action:** Step through the timeline to the latest events.
- **Expected Result:** New "share" edges appear from the Rights Holder node to the recipient nodes.
- **Pass Criteria:** Share events are visible in the lineage graph with correct labels.

---

## Appendix F — Verifier Step-by-Step

### Scenario: Verify a Document and Issue Verification Certificate

**Preconditions:** A certified document exists. The verifier has the document file or ID.

---

**Step 1: Navigate to Verifier Portal**
- **Navigate to:** `http://localhost:6882/verify/`
- **Expected Result:** Verify Page loads with "Document Verification" heading. Three tabs visible: Upload File, Enter ID, Scan QR.
- **Pass Criteria:** Page renders. SECUURA logo visible. Stats footer shows "Proven on Cardano Blockchain".

---

**Step 2: Verify by File Upload**
- **Action:** Ensure **"Upload File"** tab is selected (Tab 0).
- **Action:** Drag and drop the document file onto the dropzone.
- **Expected Result:** Loading progress bar appears. On completion, redirected to Result Page.
- **Pass Criteria:** Result page loads with a clear status indicator.

---

**Step 3: View Verification Result**
- **Expected Result (Verified):**
  - Large green circle with checkmark icon.
  - Heading: **"Document Verified"**
  - Chip: **"AUTHENTIC"** (green)
  - Document Details card: Title, Issuer, Owner, Certified Date
  - Blockchain Proof card: Transaction Hash (monospace, with copy and explorer link), Block Number, Network chip, Confirmed At, BLAKE2b hash
- **Expected Result (Failed):**
  - Large red circle with X icon.
  - Heading: **"Verification Failed"**
  - Chip: **"INVALID"** (red)
  - Reason text displayed
- **Pass Criteria:** One of the two states is clearly displayed with all relevant details.

---

**Step 4: Verify by Document ID (Alternative)**
- **Navigate to:** `http://localhost:6882/verify/`
- **Action:** Click the **"Enter ID"** tab (Tab 1).
- **Action:** Enter a document ID in the "Document ID" field (placeholder: `e.g., DOC-ABC123-XYZ789`).
- **Action:** Click **"Verify Document"**.
- **Expected Result:** Redirected to `/result/{documentId}`. Verification result displays.
- **Pass Criteria:** Same result format as Step 3.

---

**Step 5: Verify Another Document**
- **Action:** Click **"Verify Another Document"** (gradient button at bottom of results page).
- **Expected Result:** Redirected back to the Verify Page (`/`).
- **Pass Criteria:** Verify Page loads cleanly. No stale data from previous verification.

---

**Step 6: Issue Verification Certificate (Optional — Requires Auth)**
- **Navigate to:** `http://localhost:6882/` (Issuer Portal)
- **Action:** Login with Verifier credentials.
- **Action:** Navigate to the document that was just verified (`/documents/:id`).
- **Action:** Verify the **"Certify Verification"** button is visible (only shows when status = 'verified').
- **Action:** Click **"Certify Verification"**.
- **Expected Result:** "Issue Verification Certificate" dialog opens. Shows role transition: Verifier → Certifier.
- **Action:** Enter a note: `Verification completed — all credentials confirmed against original records.`
- **Action:** Click **"Issue Verification Certificate"**.
- **Expected Result:** Success alert with new Certificate ID.
- **Pass Criteria:** New certificate ID displayed in monospace. Dialog shows success state.

---

## Appendix G — Public User Step-by-Step

### Scenario: Verify a Document Without Authentication

**Preconditions:** None — no account or login required.

---

**Step 1: Access Verifier Portal**
- **Navigate to:** `http://localhost:6882/verify/`
- **Expected Result:** Verify Page loads. No login prompt. No authentication required.
- **Pass Criteria:** Page is fully functional without any authentication barrier.

---

**Step 2: Perform Verification**
- Follow Steps 2–5 from Appendix F.

---

**Step 3: Browse Marketing Website**
- **Navigate to:** `http://localhost:6881`
- **Expected Result:** Password-protected landing page (for pre-launch). After authentication, full marketing site loads with sections: Hero, Problem, Features, Tokenomics, Staking Tiers, Roadmap, Team, Whitepaper, Community, FAQ.
- **Action:** Scroll through each section.
- **Action:** Click **"Explore Tokenomics"** in the hero section.
- **Expected Result:** Smooth scroll to Tokenomics section showing token distribution chart and fee distribution breakdown.
- **Action:** Click **"Read Whitepaper"**.
- **Expected Result:** Smooth scroll or navigation to Whitepaper section with document links.
- **Pass Criteria:** All sections render. Navigation links work. No broken layouts or missing content.

---

**Step 4: Explore Staking Tiers**
- **Action:** Scroll to or navigate to the Staking Tiers section.
- **Expected Result:** 4 tier cards displayed: Basic, Staker, Validator, Partner. Each shows requirements and benefits.
- **Pass Criteria:** All 4 cards render with correct tier information.

---

**Step 5: Review FAQ**
- **Action:** Scroll to the FAQ section.
- **Action:** Click on **"What is Secuura?"**.
- **Expected Result:** Accordion expands to show the answer.
- **Action:** Click on 2-3 additional FAQ items.
- **Expected Result:** Each accordion toggles open/closed correctly.
- **Pass Criteria:** FAQ items expand and collapse without UI glitches.

---

## Appendix H — End-to-End Recruitment Flow

### Scenario: Full credential lifecycle from issuance to employer verification

This flow exercises all 7 personas across the platform.

---

**Phase 1: Platform Setup (System Admin)**
1. Login to Admin Dashboard as System Admin.
2. Create organisation "Cambridge University" (type: Education).
3. Create user "Dr. Sarah Mitchell" (role: Issuer, org: Cambridge University).
4. Create document type "BSc Degree" using the Academic Degree template.
5. Create workflow "Academic Credential Approval" with 4 steps.

**Phase 2: Document Issuance (Issuer)**
6. Login to Issuer Portal as Dr. Sarah Mitchell.
7. Upload a PDF representing a BSc degree.
8. Set title, type (Degree/Diploma), description.
9. Submit for certification.

**Phase 3: Certification (Certifier)**
10. Login to Issuer Portal as the Registrar (ISSUER_APPROVER role).
11. Navigate to the pending document.
12. Connect Cardano wallet.
13. Sign the document with wallet signature.
14. Anchor to blockchain.
15. Verify anchor confirmation in the Blockchain Anchors section.

**Phase 3a: NFT Certificate (Issuer/Certifier — Optional)**
15a. On the certified document, click "Save as NFT".
15b. Connect wallet (Lace recommended), select Standard tier and Partial privacy.
15c. Review summary and click "Mint NFT". Approve transaction in wallet.
15d. Verify success screen with Tx Hash, Policy ID, and Asset Name.
15e. Optionally verify on Cardanoscan.

**Phase 4: Credential Sharing (Rights Holder)**
16. Login to Issuer Portal as the Student (OWNER role).
17. Navigate to the now-certified document.
18. Click Share → add recruiter email with "Verify" permission.
19. Confirm share success.

**Phase 5: Recruiter Verification (Verifier)**
20. Navigate to Verifier Portal (`http://localhost:6882/verify/`).
21. Enter the document ID in the "Enter ID" tab.
22. Click "Verify Document".
23. Verify result shows "AUTHENTIC" with blockchain proof.
24. Optionally login to Issuer Portal and issue a Verification Certificate (role transition: Verifier → Certifier).

**Phase 6: Employer Verification (Verifier)**
25. Navigate to Verifier Portal.
26. Upload the original credential file via the "Upload File" tab.
27. Verify result shows "AUTHENTIC".
28. Review blockchain proof: transaction hash, block number, network.

**Phase 7: Audit (System Admin)**
29. Login to Admin Dashboard.
30. Navigate to Audit Logs.
31. Search for the document title.
32. Verify the full chain of events: upload → certification → anchor → share → verification.
33. Navigate to System Health to confirm no errors.

---

## Appendix I — Test Environment Reference

### URLs

| Service | URL | Notes |
|---|---|---|
| Nginx Gateway | `http://localhost:6882` | Main entry point for all apps |
| Issuer Portal | `http://localhost:6882/` | Root path |
| Verifier Portal | `http://localhost:6882/verify/` | Verification interface |
| Admin Dashboard | `http://localhost:6882/admin/` | Administration interface |
| Status Page | `http://localhost:6882/status/` | Public status monitoring |
| Marketing Website | `http://localhost:6881` | Tokenomics and marketing |
| API Gateway | `http://localhost:6882/api/` | REST API for all services |
| NFT Certificate API | `http://localhost:6882/api/nft/` | NFT minting, tiers, privacy options |
| PostgreSQL | `localhost:5432` | DB: secuura, User: secuura |
| Redis | `localhost:6379` | Session/cache |

### Test Credentials

| Role | Email | Password | Portal |
|---|---|---|---|
| Demo Issuer | `demo@secuura.io` | `demo123` | Issuer Portal |
| Demo Admin | `admin@secuura.com` | `admin123` | Admin Dashboard |

### Seed Documents (Pre-Loaded)

These documents are automatically created on every originate service startup and can be used for all test flows:

| ID | Title | Type | Status |
|----|-------|------|--------|
| `doc-demo-degree-001` | BSc Computer Science — University of Oxford | degree | anchored |
| `doc-demo-transcript-002` | Academic Transcript — 2022-2025 | transcript | signed |
| `doc-demo-certificate-003` | Professional Certification — AWS Solutions Architect | certificate | draft |

### Authentication Notes

- Refresh tokens are stored as **httpOnly cookies** (invisible to JavaScript)
- Access tokens are kept in memory only (not in localStorage or sessionStorage)
- Sessions survive full page reloads via automatic cookie-based refresh
- To verify: Open DevTools > Application > Cookies and confirm `refresh_token` is present with `HttpOnly` flag
- Logout clears the cookie on the server side

### Database Verification

```bash
# Check documents in PostgreSQL
docker exec secuura-postgres psql -U secuura -d secuura \
  -c "SELECT external_id, title, status FROM documents ORDER BY created_at DESC;"

# Check user sessions
docker exec secuura-postgres psql -U secuura -d secuura \
  -c "SELECT id, email, role FROM users LIMIT 10;"
```

### Docker Commands

```bash
# Start all containers
docker compose up -d

# Rebuild frontends after code changes
cd frontend/issuer && npm run build && cd ../..
cd frontend/verifier && npm run build && cd ../..
cd frontend/admin && npm run build && cd ../..
docker compose build --no-cache issuer-frontend verifier-frontend admin-frontend
docker compose up -d issuer-frontend verifier-frontend admin-frontend

# View logs
docker compose logs -f issuer-frontend
docker compose logs -f api-gateway

# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
```

### Automation Notes for Cursor / Playwright

- All MUI components can be targeted by their text content, `aria-label`, or `data-testid` attributes.
- Admin Dashboard has `data-testid` attributes on sidebar navigation items (e.g., `nav-dashboard`, `nav-organizations`).
- Admin Login has `data-testid` on form elements: `login-form`, `email-input`, `password-input`, `login-btn`.
- Issuer Portal and Verifier Portal do not currently have `data-testid` attributes — target by text content, roles, or CSS selectors.
- MUI dialogs can be targeted via `role="dialog"` or `role="presentation"`.
- MUI buttons can be targeted via `role="button"` and their visible text.
- Dropzone areas respond to file drag events and click-to-browse.
- React Flow canvas elements require coordinate-based interaction or custom selectors.

### Browser Requirements

- A modern Chromium-based browser (Chrome, Edge, Brave) is recommended.
- For wallet testing, install a Cardano wallet browser extension (Nami, Eternl, or Lace).
- Camera access is required for QR code scanning (Verifier Portal, Tab 2).

---

*End of Document*
