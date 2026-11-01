# Secuura Platform — Pre-Launch Exhaustive Test Plan

---

| **Document** | Pre-Launch Exhaustive Test Plan |
|---|---|
| **Version** | 3.0.0 |
| **Date** | 22 March 2026 |
| **Classification** | Internal — Confidential |
| **Purpose** | Comprehensive programmatic + browser testing before external test users |
| **Methodology** | Playwright E2E (browser emulation) + API testing — all automated |
| **Test Framework** | Playwright with existing `tests/e2e/` infrastructure |
| **Target Environments** | Local Docker (`localhost:6882`) + Azure Demo (`*.yellowground-ae96b9b1.uksouth.azurecontainerapps.io`) |

---

## Table of Contents

1. [Test Philosophy & Approach](#1-test-philosophy--approach)
2. [Prerequisites & Requirements](#2-prerequisites--requirements)
3. [Persona Definitions & Test Accounts](#3-persona-definitions--test-accounts)
4. [Module 1: Platform Infrastructure & Smoke](#4-module-1-platform-infrastructure--smoke)
5. [Module 2: Authentication & Identity](#5-module-2-authentication--identity)
6. [Module 3: System Administrator](#6-module-3-system-administrator)
7. [Module 4: Organisation Administrator](#7-module-4-organisation-administrator)
8. [Module 5: Issuer (Document Preparer)](#8-module-5-issuer-document-preparer)
9. [Module 6: Certifier (Document Approver)](#9-module-6-certifier-document-approver)
10. [Module 7: Rights Holder (Document Owner)](#10-module-7-rights-holder-document-owner)
11. [Module 8: Verifier](#11-module-8-verifier)
12. [Module 9: Public / Anonymous User](#12-module-9-public--anonymous-user)
13. [Module 10: Cross-Persona End-to-End Flows](#13-module-10-cross-persona-end-to-end-flows)
14. [Module 11: Negative & Error Path Testing](#14-module-11-negative--error-path-testing)
15. [Module 12: Bad Actor / Security Testing](#15-module-12-bad-actor--security-testing)
16. [Module 13: Performance & Stress Testing](#16-module-13-performance--stress-testing)
17. [Module 14: Accessibility & Cross-Browser](#17-module-14-accessibility--cross-browser)
18. [Module 15: GDPR & Compliance Testing](#18-module-15-gdpr--compliance-testing)
19. [Module 16: Blockchain & Crypto Wallet Testing](#19-module-16-blockchain--crypto-wallet-testing)
20. [Module 17: Email & Notification Testing](#20-module-17-email--notification-testing)
21. [Module 18: API Contract & Integration Testing](#21-module-18-api-contract--integration-testing)
22. [Module 19: Multi-Tenancy & Data Isolation](#22-module-19-multi-tenancy--data-isolation)
23. [Module 20: Azure Environment Parity & Production Readiness](#23-module-20-azure-environment-parity--production-readiness)
24. [Test Execution Order & Dependencies](#24-test-execution-order--dependencies)
25. [Reporting & Evidence](#25-reporting--evidence)

---

## Test Results Summary (v19 — 22 March 2026)

| Metric | Local Docker | Azure Demo |
|---|---|---|
| **Passed** | 270 (56%) | 190 (39%) |
| **Failed** | 153 | 233 |
| **Skipped** | 60 | 60 |

### Failure Breakdown

| Category | Local | Azure | Description |
|---|---|---|---|
| SKIP-REASON | 35 | 2 | Environment-specific tests (Azure-only on local) |
| BLOCKER | 28 | 92 | Tests blocked by prerequisite failure |
| NOT-IMPLEMENTED | 5 | 2 | Features not yet built |
| ACTUAL | 85 | 137 | Real platform bugs |

### Progress Since Testing Started

| Metric | Run 1 (Start) | Run 19 (Current) | Improvement |
|---|---|---|---|
| Passed | 97 | 270 | +178% |
| Failed | 318 | 153 | -52% |
| ACTUAL bugs | 318 | 85 | -73% |

### Key Changes in v19

- **Global Setup:** `global-setup.ts` authenticates all personas once and caches shared tokens across test suites
- **SMTP Email:** AgentMail SMTP integration (smtp.agentmail.to:465) enables email tests — registration, password reset, share notifications, GDPR DSR confirmations
- **GDPR Consent Banner:** Implemented on all portals; GDPR routes require authentication
- **Seed Data:** Certified documents, holder assignments, and workflow completions added to demo data
- **19 fix rounds** applied across gateway auth, URL handling, admin portal, and test infrastructure

> Full failure details: see [Secuura-Pre-Launch-Test-Failure-Report.md](Secuura-Pre-Launch-Test-Failure-Report.md)

---

## 1. Test Philosophy & Approach

### Mindset
Every test is written as if my job depends on finding the bugs that will embarrass us in front of external testers. We test three layers:

1. **Happy Path** — Every function works as documented when the user does everything right
2. **Variation Path** — What happens when the user makes mistakes, skips steps, uses unexpected input, or does things out of order
3. **Bad Actor Path** — What happens when someone deliberately tries to break, bypass, or exploit the system

### Implementation
- **ALL tests are Playwright specs** — browser automation emulating real human interaction
- **API tests use Playwright's `request` context** — no separate HTTP clients
- **Screenshots captured** at every critical step for evidence
- **Video recorded** on failure
- **HTML report** generated after each run
- **Tests are idempotent** — each test creates its own data, cleans up after itself

### Dual-Environment Testing
Every test suite runs against **both** environments. Tests must pass in both to be considered green:

| Environment | Base URL | API URL | Purpose |
|---|---|---|---|
| **Local Docker** | `http://localhost:6882` | `http://localhost:6882/api` | Development — full control, devnet blockchain |
| **Azure Demo** | `https://secuura-demo-issuer.yellowground-ae96b9b1.uksouth.azurecontainerapps.io` | `https://secuura-demo-api.yellowground-ae96b9b1.uksouth.azurecontainerapps.io` | Production-like — real infra, TLS, Azure PostgreSQL, external Redis |

```bash
# Run tests against local
BASE_URL=http://localhost:6882 npx playwright test

# Run tests against Azure demo
BASE_URL=https://secuura-demo-issuer.yellowground-ae96b9b1.uksouth.azurecontainerapps.io \
API_URL=https://secuura-demo-api.yellowground-ae96b9b1.uksouth.azurecontainerapps.io \
ADMIN_URL=https://secuura-demo-admin.yellowground-ae96b9b1.uksouth.azurecontainerapps.io/admin/ \
VERIFIER_URL=https://secuura-demo-verifier.yellowground-ae96b9b1.uksouth.azurecontainerapps.io/verify \
npx playwright test
```

Tests that are environment-specific (e.g., devnet blockchain, mock KYC) are tagged and skipped on the non-applicable environment.

---

## 2. Prerequisites & Requirements

### Credential Vault

All test credentials (local, Azure, OAuth, Agent Mail) are stored in the Credential Vault:
`/Volumes/KK_DEV_Local/NEW STRUCTURE/!CODING/Secuura Credentials/CREDENTIALS.md`

> **Security Audit Alignment (v3.0):** GDPR routes now require authentication, rate limits are set to 200 requests/15min in dev mode, and sessions are Redis-only (no in-memory fallback). Tests and credentials have been updated accordingly.

### What I Need From You

| # | Requirement | Purpose | Priority |
|---|---|---|---|
| 1 | **Email inbox (Agent Mail)** | Receive verification emails, password resets, share notifications, GDPR confirmation emails | CRITICAL |
| 2 | **Cardano testnet wallet** (Nami, Eternl, or Lace) with test ADA | CIP-30 wallet connection, CIP-8 message signing, blockchain anchoring, transaction fees | CRITICAL |
| 3 | **Second Cardano wallet** (different browser profile) | Test wallet switching, multi-signer flows, bad actor wallet impersonation | HIGH |
| 4 | **O365/Azure Entra ID test tenant** | Enterprise SSO login, Entra Verified ID KYC flow, M365 integration (Outlook Add-in, SharePoint) | HIGH |
| 5 | **Google OAuth test account** | Social login testing (Google) | HIGH |
| 6 | **GitHub OAuth test account** | Social login testing (GitHub) | MEDIUM |
| 7 | **LinkedIn OAuth test account** | Social login testing (LinkedIn) | MEDIUM |
| 8 | **Multiple browser profiles** (Chrome, Firefox, Safari) | Cross-browser testing, multi-user concurrent sessions | HIGH |
| 9 | **TOTP authenticator app** (or virtual — otplib) | MFA setup/verification/recovery testing | HIGH |
| 10 | **Sample documents** (PDF, DOCX, PNG, JPG, large files, corrupted files) | Document upload testing — various formats, sizes, edge cases | CRITICAL |
| 11 | **Blockfrost API key** (testnet/preprod) | Blockchain anchoring verification, transaction confirmation | HIGH |
| 12 | **Stripe test credentials** (publishable + secret key) | Billing flow testing, webhook simulation | MEDIUM |
| 13 | **A second machine or VM** | Test concurrent sessions from different IPs, rate limiting validation | MEDIUM |
| 14 | **DNS/domain for webhook testing** (ngrok or similar) | Test webhook delivery for document events, integration callbacks | MEDIUM |
| 15 | **FreeTSA/D-Trust test access** | RFC-3161 timestamp generation and verification | LOW |
| 16 | **Mobile devices** (iOS Safari, Android Chrome) — or BrowserStack | Real device testing beyond emulation | MEDIUM |
| 17 | **VPN or proxy** | Test geo-blocking, IP-based rate limiting from different regions | LOW |
| 18 | **Load testing tool** (k6 or Artillery) | Performance testing beyond what Playwright can stress | LOW |

### Test Environment Setup

```bash
# 1. Start full platform
cd "/Volumes/KK_DEV_Local/NEW STRUCTURE/!CODING/Secuura/Blockchain/Dev"
docker compose up -d --build

# 2. Verify all services healthy
curl http://localhost:6882/health

# 3. Install test dependencies
cd tests/e2e
npm install

# 4. Run specific test module
npx playwright test --project=<project-name>
```

### Test Data Fixtures Required

| Fixture | Description |
|---|---|
| `valid-degree.pdf` | Clean PDF, 2 pages, < 5MB |
| `valid-certificate.pdf` | Professional certification PDF |
| `large-file.pdf` | 50MB+ PDF to test upload limits |
| `corrupted-file.pdf` | Truncated/invalid PDF |
| `executable.pdf.exe` | File with misleading extension |
| `xss-filename.pdf` | Filename containing `<script>alert(1)</script>` |
| `unicode-filename-日本語.pdf` | Unicode characters in filename |
| `empty-file.pdf` | 0-byte file |
| `password-protected.pdf` | Encrypted PDF |
| `multi-page-100.pdf` | 100-page document |

---

## 3. Persona Definitions & Test Accounts

| Persona | Test Account | Password | Portal | Purpose |
|---|---|---|---|---|
| System Admin | `admin@secuura.com` | `admin123` | Admin `/admin/` | Platform-wide management |
| Org Admin | `orgadmin-test@secuura.io` | (create during test) | Admin `/admin/` | Org-scoped configuration |
| Issuer | `demo@secuura.io` | `demo123` | Issuer `/` | Document preparation |
| Issuer 2 | `issuer2-test@secuura.io` | (create during test) | Issuer `/` | Multi-issuer workflows |
| Certifier | `certifier-test@secuura.io` | (create during test) | Issuer `/` | Document approval/signing |
| Rights Holder | `holder-test@secuura.io` | (create during test) | Issuer `/` | Credential recipient |
| Verifier | `verifier-test@secuura.io` | (create during test) | Verifier `/verify/` | Document verification |
| Public User | (anonymous) | — | Verifier `/verify/` | Anonymous verification |
| Bad Actor | `attacker-test@secuura.io` | (create during test) | All portals | Exploitation attempts |

### Azure Demo Accounts (Pre-Seeded)

| Persona | Test Account | Password | Portal |
|---|---|---|---|
| Demo Issuer | `demo@secuura.io` | `demo123` | Issuer |
| Issuer Admin | `issuer@secuura.com` | `issuer123` | Issuer |
| Verifier | `verifier@secuura.com` | `verifier123` | Issuer / Verifier |
| Rights Holder | `holder@secuura.com` | `holder123` | Issuer |
| System Admin | `admin@secuura.com` | `admin123` | Admin |

---

## 4. Module 1: Platform Infrastructure & Smoke

**File:** `tests/e2e/tests/infrastructure-smoke.spec.ts`

### 1.1 Service Health (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 1.1.1 | Gateway health check | `GET /health` | 200 OK, all services healthy |
| 1.1.2 | All backend services responding | `GET /api/health` for each of 22 services | 200 OK each |
| 1.1.3 | Database connectivity | Service health includes DB status | Connected |
| 1.1.4 | Redis connectivity | Service health includes Redis status | Connected |
| 1.1.5 | Issuer Portal loads | Navigate to `http://localhost:6882/` | Login page renders, no console errors |
| 1.1.6 | Verifier Portal loads | Navigate to `/verify/` | Verification page renders |
| 1.1.7 | Admin Dashboard loads | Navigate to `/admin/` | Login page renders |
| 1.1.8 | Status Page loads | Navigate to `/status/` | Status dashboard renders |
| 1.1.9 | Marketing Website loads | Navigate to `http://localhost:6881` | Landing page renders |
| 1.1.10 | API Documentation loads | Navigate to `/api/docs` | Swagger UI renders |

### 1.2 Service Health (Variation)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 1.2.1 | Invalid route | Navigate to `/nonexistent/` | 404 or redirect, not 500 |
| 1.2.2 | Trailing slashes | Navigate to `/admin` vs `/admin/` | Both work or consistent redirect |
| 1.2.3 | Case sensitivity | Navigate to `/Admin/` | Consistent behavior (redirect or serve) |
| 1.2.4 | Double slashes | Navigate to `//admin//` | Normalized, no 500 |

---

## 5. Module 2: Authentication & Identity

**File:** `tests/e2e/tests/auth-exhaustive.spec.ts`

### 2.1 Email/Password Login (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.1.1 | Valid login — Issuer | Enter `demo@secuura.io` / `demo123`, click Login | Redirected to dashboard, JWT cookie set |
| 2.1.2 | Valid login — Admin | Enter `admin@secuura.com` / `admin123`, click Login | Redirected to admin dashboard |
| 2.1.3 | Session persists on reload | Login → refresh page | Still logged in |
| 2.1.4 | Logout | Click profile → Logout | Redirected to login, JWT cleared |
| 2.1.5 | Login after logout | Login again | Works normally |

### 2.2 Email/Password Login (Variations — What Could Go Wrong)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.2.1 | Wrong password | Enter valid email, wrong password | Error message, no login, account not locked (first attempt) |
| 2.2.2 | Wrong email | Enter non-existent email | Generic error (not "email not found" — prevents enumeration) |
| 2.2.3 | Empty email | Submit with empty email field | Client-side validation prevents submission |
| 2.2.4 | Empty password | Submit with empty password field | Client-side validation prevents submission |
| 2.2.5 | SQL injection in email | Enter `' OR 1=1 --` as email | Rejected, no SQL error exposed |
| 2.2.6 | XSS in email field | Enter `<script>alert(1)</script>` | Sanitized, no script execution |
| 2.2.7 | Very long email | Enter 500+ character email | Rejected with appropriate error |
| 2.2.8 | Email with spaces | Enter ` demo@secuura.io ` (leading/trailing spaces) | Trimmed and accepted OR clear error |
| 2.2.9 | Case sensitivity | Enter `DEMO@secuura.io` | Should match (case-insensitive email) |
| 2.2.10 | Unicode email | Enter `démö@secuura.io` | Rejected or handled gracefully |
| 2.2.11 | Password with special chars | Login with password containing `'"<>&` | Works correctly (no encoding issues) |
| 2.2.12 | Multiple rapid login attempts | Submit 10 logins in 2 seconds | Rate limited after threshold |
| 2.2.13 | Login with expired JWT | Manually set expired JWT cookie, navigate | Redirected to login |
| 2.2.14 | Login with tampered JWT | Modify JWT payload, navigate | Rejected, redirected to login |

### 2.3 Registration (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.3.1 | New user registration | Fill all required fields, submit | Account created, verification email sent |
| 2.3.2 | Email verification | Click link in verification email | Account activated, can login |
| 2.3.3 | Login after verification | Login with new credentials | Success |

### 2.4 Registration (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.4.1 | Duplicate email | Register with existing email | Error: "Email already registered" (or generic) |
| 2.4.2 | Weak password | Register with "123" | Rejected with password requirements shown |
| 2.4.3 | Password mismatch | Enter different confirm password | Client-side error before submit |
| 2.4.4 | Missing required fields | Submit with empty name | Validation error shown |
| 2.4.5 | Invalid email format | Register with "notanemail" | Validation error |
| 2.4.6 | Resend verification email | Request resend before verifying | New email sent, old link still works OR invalidated |
| 2.4.7 | Use expired verification link | Wait past expiry, click link | Error with option to resend |
| 2.4.8 | Use verification link twice | Click link after already verified | Graceful "already verified" message |

### 2.5 Password Reset (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.5.1 | Request password reset | Enter email, click "Forgot Password" | Email sent with reset link |
| 2.5.2 | Reset password | Click link, enter new password | Password changed, can login with new password |
| 2.5.3 | Old password rejected | Login with old password | Rejected |

### 2.6 Password Reset (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.6.1 | Reset for non-existent email | Enter unknown email | Same success message (no enumeration) |
| 2.6.2 | Expired reset link | Wait past expiry, click link | Error with option to request new reset |
| 2.6.3 | Used reset link | Use link twice | Second attempt fails gracefully |
| 2.6.4 | Multiple reset requests | Request 3 resets rapidly | Only latest link works |

### 2.7 OAuth / Social Login (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.7.1 | Google OAuth login | Click "Sign in with Google" | Redirect to Google, authorize, return logged in |
| 2.7.2 | GitHub OAuth login | Click "Sign in with GitHub" | Redirect to GitHub, authorize, return logged in |
| 2.7.3 | LinkedIn OAuth login | Click "Sign in with LinkedIn" | Redirect to LinkedIn, authorize, return logged in |
| 2.7.4 | Azure Entra ID SSO | Click "Enterprise SSO" | Redirect to Entra, authenticate, return logged in |
| 2.7.5 | OAuth creates account | First-time OAuth user | Account auto-created, verification level set to SOCIAL |

### 2.8 OAuth (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.8.1 | Cancel OAuth flow | Click Google login, then cancel at Google | Return to login page, no error crash |
| 2.8.2 | OAuth with existing email | OAuth email matches existing account | Accounts linked OR clear error |
| 2.8.3 | Revoke OAuth after linking | Disconnect Google from profile | Can still login with email/password |
| 2.8.4 | Invalid OAuth state | Tamper with OAuth state parameter | Rejected, CSRF protection works |

### 2.9 Wallet Authentication (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.9.1 | Connect wallet (CIP-30) | Click "Connect Wallet", select Nami/Eternl | Wallet connected, address displayed |
| 2.9.2 | Sign challenge (CIP-8) | Sign authentication challenge in wallet | Signature verified, logged in |
| 2.9.3 | Wallet address stored | After wallet auth | Wallet address associated with account |

### 2.10 Wallet Authentication (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.10.1 | No wallet installed | Click "Connect Wallet" with no extension | Helpful error: "Install a CIP-30 wallet" |
| 2.10.2 | Reject wallet connection | Deny connection in wallet popup | Graceful error, can retry |
| 2.10.3 | Reject signing | Approve connection, reject signature | Graceful error, wallet stays connected |
| 2.10.4 | Wrong network wallet | Connect mainnet wallet to testnet platform | Error about network mismatch |
| 2.10.5 | Switch wallets | Connect Nami, then switch to Eternl | Handled gracefully |
| 2.10.6 | Wallet with zero ADA | Connect empty wallet | Should still authenticate (signing is free) |

### 2.11 Multi-Factor Authentication (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.11.1 | Enable MFA | Go to settings → Security → Enable MFA | QR code displayed, can scan with authenticator |
| 2.11.2 | Verify MFA setup | Enter TOTP code from authenticator | MFA enabled, backup codes displayed |
| 2.11.3 | Login with MFA | Login → prompted for TOTP → enter code | Logged in |
| 2.11.4 | Login with backup code | Use one backup code | Logged in, backup code consumed |

### 2.12 MFA (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 2.12.1 | Wrong TOTP code | Enter incorrect 6-digit code | Rejected, can retry |
| 2.12.2 | Expired TOTP code | Wait 60s, enter old code | Rejected |
| 2.12.3 | Reuse backup code | Use same backup code twice | Second use rejected |
| 2.12.4 | All backup codes used | Use all codes, then try another | Must contact admin or re-setup |
| 2.12.5 | Disable MFA | Go to settings → Disable MFA | Requires current TOTP to disable |
| 2.12.6 | Brute force TOTP | Enter 10 wrong codes rapidly | Account temporarily locked |

---

## 6. Module 3: System Administrator

**File:** `tests/e2e/tests/sysadmin-exhaustive.admin.spec.ts`

### 3.1 Dashboard (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.1.1 | Dashboard loads | Login as admin, navigate to `/admin/` | Dashboard with stats: total docs, verifications, users, anchors |
| 3.1.2 | Statistics are accurate | Compare dashboard numbers with API counts | Numbers match |
| 3.1.3 | Charts render | Check weekly activity chart | Chart visible with data points |
| 3.1.4 | Navigation sidebar | Click each sidebar item | Each page loads without error |
| 3.1.5 | Sidebar collapse | Click collapse button | Sidebar collapses, icons remain visible |

### 3.2 Organisation Management (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.2.1 | List organisations | Navigate to `/admin/organizations` | Table with existing orgs |
| 3.2.2 | Create organisation | Click "Create", fill name/type/details, submit | Org created, appears in list |
| 3.2.3 | Edit organisation | Click edit on existing org, change name, save | Name updated |
| 3.2.4 | Search organisations | Type in search box | Results filtered |
| 3.2.5 | Filter by type | Filter by ISSUER/VERIFIER | Correct filtering |
| 3.2.6 | Suspend organisation | Click suspend on org | Org marked suspended, users can't login |
| 3.2.7 | Reactivate organisation | Unsuspend suspended org | Org active again |
| 3.2.8 | Delete organisation | Delete org (if allowed) | Org removed, confirmation dialog shown first |

### 3.3 Organisation Management (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.3.1 | Create org with duplicate name | Use existing org name | Error or allowed with unique ID |
| 3.3.2 | Create org with empty name | Submit with empty name field | Validation error |
| 3.3.3 | Create org with very long name | 500+ character name | Truncated or rejected |
| 3.3.4 | Create org with special characters | Name: `<script>alert(1)</script>` | Sanitized, no XSS |
| 3.3.5 | Delete org with active documents | Delete org that has documents | Prevented or warned |
| 3.3.6 | Suspend org with active sessions | Suspend while users are logged in | Sessions invalidated |

### 3.4 User Management (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.4.1 | List users | Navigate to `/admin/users` | Table with all users |
| 3.4.2 | Create user | Click "Create", fill details, assign role | User created |
| 3.4.3 | Edit user | Change user's role from VERIFIER to ISSUER | Role updated |
| 3.4.4 | Block user | Click block on user | User blocked, can't login |
| 3.4.5 | Unblock user | Unblock blocked user | User can login again |
| 3.4.6 | Set verification level | Set user to ENHANCED | Level updated |
| 3.4.7 | Search users | Search by email | Correct results |
| 3.4.8 | Filter by role | Filter by ADMIN | Only admins shown |
| 3.4.9 | Pagination | Navigate to page 2 | Different users shown |

### 3.5 User Management (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.5.1 | Create user with existing email | Duplicate email | Error message |
| 3.5.2 | Block yourself | Try to block admin's own account | Prevented |
| 3.5.3 | Delete last admin | Try to delete the only admin | Prevented |
| 3.5.4 | Assign invalid role combination | Assign SUPER_ADMIN to org user | Prevented or warning |

### 3.6 System Health & Error Monitoring (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.6.1 | View system health | Navigate to `/admin/system-health` | Error overview with severity breakdown |
| 3.6.2 | View error details | Click on specific error | Details panel shows service, timestamp, stack trace |
| 3.6.3 | Resolve error | Mark error as resolved | Error moved to resolved list |
| 3.6.4 | Filter by service | Filter errors by "originate" | Only originate errors shown |
| 3.6.5 | Filter by severity | Filter by CRITICAL | Only critical errors shown |

### 3.7 Audit Logs (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.7.1 | View audit logs | Navigate to `/admin/audit-logs` | Chronological log entries |
| 3.7.2 | Search logs | Search by user email | Filtered results |
| 3.7.3 | Filter by category | Filter by "Document" category | Only document actions shown |
| 3.7.4 | Filter by date range | Set from/to dates | Filtered results |
| 3.7.5 | Export logs | Click export (CSV/JSON) | File downloaded with correct data |
| 3.7.6 | Log entry detail | Click on log entry | Shows before/after state, IP, user agent |

### 3.8 API Key Management (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.8.1 | List API keys | Navigate to `/admin/api-keys` | Table of existing keys |
| 3.8.2 | Create API key | Click create, set name/scopes | Key created, displayed once |
| 3.8.3 | Test API key | Use key in API call | Request authenticated |
| 3.8.4 | Revoke API key | Click revoke | Key no longer works |
| 3.8.5 | Key permissions | Create read-only key, try write operation | Write rejected |

### 3.9 Reports (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.9.1 | Generate usage report | Select date range, click generate | Report generated |
| 3.9.2 | Export as PDF | Click PDF export | PDF downloaded |
| 3.9.3 | Export as CSV | Click CSV export | CSV downloaded |
| 3.9.4 | Export as JSON | Click JSON export | JSON downloaded, valid format |
| 3.9.5 | GDPR compliance report | Generate GDPR report | Report includes consent status, DSRs |

### 3.10 Platform Settings (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 3.10.1 | View settings | Navigate to `/admin/settings` | All configuration visible |
| 3.10.2 | Update platform name | Change name, save | Name updated, reflected in UI |
| 3.10.3 | Update session timeout | Change to 30 min | Setting saved |
| 3.10.4 | Enable MFA requirement | Toggle "Require MFA for all users" | Setting saved, enforcement begins |
| 3.10.5 | Update rate limits | Change auth rate limit | Setting saved, new limit enforced |
| 3.10.6 | Configure blockchain network | Switch to preprod | Network updated |
| 3.10.7 | Save and verify | Save settings, reload page | Settings persisted |

---

## 7. Module 4: Organisation Administrator

**File:** `tests/e2e/tests/orgadmin-exhaustive.admin.spec.ts`

### 4.1 Document Type Configuration (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.1.1 | List document types | Navigate to `/admin/document-types` | Table of configured types |
| 4.1.2 | Create document type | Click create, enter name "Degree Certificate" | Type created with ID |
| 4.1.3 | Configure metadata schema | Add fields: institution (text), degree (select), year (number) | Schema saved |
| 4.1.4 | Set verification requirements | Set required verification level to ENHANCED | Requirement saved |
| 4.1.5 | Set blockchain anchoring | Enable auto-anchor for this type | Setting saved |
| 4.1.6 | Edit document type | Change display name | Updated |
| 4.1.7 | Delete unused document type | Delete type with no documents | Type removed |
| 4.1.8 | Link document type to org | Associate type with organisation | Linked, visible in issuer portal |

### 4.2 Document Type Configuration (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.2.1 | Create type with duplicate name | Same name as existing | Error or unique ID differentiation |
| 4.2.2 | Delete type with documents | Try to delete type that has issued documents | Prevented with warning |
| 4.2.3 | Invalid metadata schema | Add field with no name | Validation error |
| 4.2.4 | Very large schema | Add 100+ fields | Handled (possibly with warning) |

### 4.3 Workflow Builder (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.3.1 | List workflows | Navigate to `/admin/workflows` | Table of workflows |
| 4.3.2 | Create workflow | Click create, name "Degree Approval" | Workflow created |
| 4.3.3 | Add approval step | Add step: "Department Review" with approver role | Step added |
| 4.3.4 | Add notification step | Add step: "Notify Holder" | Step added |
| 4.3.5 | Add blockchain anchor step | Add step: "Anchor to Cardano" | Step added |
| 4.3.6 | Add wallet signature step | Add step: "Require Dean signature" | Step added |
| 4.3.7 | Set step order | Drag steps into order | Order saved |
| 4.3.8 | Set SLA | Set 48-hour SLA on approval step | SLA saved |
| 4.3.9 | Save and activate | Save workflow, set active | Workflow active |
| 4.3.10 | Link workflow to document type | Associate with "Degree Certificate" type | Linked |

### 4.4 Workflow Builder (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.4.1 | Create workflow with no steps | Save empty workflow | Error: "At least one step required" |
| 4.4.2 | Circular workflow | Try to create step that references itself | Prevented |
| 4.4.3 | Delete active workflow | Delete workflow in use | Prevented or warned |
| 4.4.4 | Duplicate workflow names | Create two with same name | Error or allowed with unique ID |

### 4.5 Verification Queue (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.5.1 | View pending verifications | Navigate to `/admin/verification-queue` | List of pending docs |
| 4.5.2 | Assign verifier | Assign document to verifier user | Assignment saved |
| 4.5.3 | Approve verification | Review and approve document | Status changes to verified |
| 4.5.4 | Reject verification | Review and reject with reason | Status changes to rejected, reason stored |
| 4.5.5 | SLA indicators | Check SLA badges | At-risk/breached shown correctly |

### 4.6 Integration Hub (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 4.6.1 | View integrations | Navigate to `/admin/integrations` | List of available integrations |
| 4.6.2 | Configure webhook | Set webhook URL, select events | Webhook saved |
| 4.6.3 | Test webhook | Click "Test Connection" | Test payload delivered, success shown |
| 4.6.4 | Configure identity provider | Set up Entra ID connection | Provider configured |
| 4.6.5 | Configure document source | Connect SharePoint | Source configured |

---

## 8. Module 5: Issuer (Document Preparer)

**File:** `tests/e2e/tests/issuer-exhaustive.issuer.spec.ts`

### 5.1 Dashboard (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.1.1 | Dashboard loads | Login as issuer | Dashboard with document count, recent activity |
| 5.1.2 | Quick stats visible | Check stats cards | Total docs, pending, certified, revoked counts |
| 5.1.3 | Recent documents | Check recent documents list | Shows latest documents with status |

### 5.2 Document Creation (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.2.1 | Navigate to create | Click "New Document" or navigate to create page | Form displayed |
| 5.2.2 | Upload document file | Upload `valid-degree.pdf` | File uploaded, hash calculated (BLAKE2b-256) |
| 5.2.3 | Verify hash displayed | After upload | Hash shown to user |
| 5.2.4 | Fill metadata | Enter title, select document type, fill custom fields | Fields accepted |
| 5.2.5 | Assign holder | Enter holder email | Holder assigned |
| 5.2.6 | Set expiration | Set expiration date 1 year from now | Date accepted |
| 5.2.7 | Submit document | Click "Create" / "Submit" | Document created with status DRAFT or PENDING |
| 5.2.8 | Document appears in list | Navigate to documents list | New document visible |
| 5.2.9 | Document detail view | Click on document | Full details shown: title, type, hash, status, metadata |

### 5.3 Document Creation (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.3.1 | Upload without file | Submit form with no file | Validation error |
| 5.3.2 | Upload oversized file | Upload 50MB+ file | Rejected with size limit message |
| 5.3.3 | Upload wrong file type | Upload `.exe` file | Rejected with allowed types message |
| 5.3.4 | Upload corrupted file | Upload truncated PDF | Error or warning about file integrity |
| 5.3.5 | Upload empty file | Upload 0-byte file | Rejected |
| 5.3.6 | XSS in title | Enter `<img src=x onerror=alert(1)>` as title | Sanitized, no XSS |
| 5.3.7 | SQL injection in metadata | Enter `'; DROP TABLE documents; --` in field | Sanitized, no SQL error |
| 5.3.8 | Very long title | 1000+ character title | Truncated or rejected |
| 5.3.9 | Duplicate document | Upload same file twice | Allowed (different certifications) or warned |
| 5.3.10 | Missing required metadata | Submit without required custom fields | Validation error per field |
| 5.3.11 | Past expiration date | Set date in the past | Rejected |
| 5.3.12 | Unicode in all fields | Japanese/Arabic/emoji characters | Handled correctly, stored and displayed |
| 5.3.13 | Concurrent upload | Upload 5 files simultaneously | All succeed or queued gracefully |
| 5.3.14 | Upload then navigate away | Start upload, navigate away | Upload cancelled or continues with warning |
| 5.3.15 | Upload password-protected PDF | Upload encrypted PDF | Warning about potential verification issues |

### 5.4 Document Management (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.4.1 | List all documents | Navigate to documents page | Paginated list |
| 5.4.2 | Search documents | Search by title | Filtered results |
| 5.4.3 | Filter by status | Filter by CERTIFIED | Only certified docs shown |
| 5.4.4 | Filter by type | Filter by "Degree Certificate" | Filtered correctly |
| 5.4.5 | Sort by date | Sort newest first | Correct order |
| 5.4.6 | Edit draft document | Edit title of DRAFT document | Updated |
| 5.4.7 | Cannot edit certified | Try to edit CERTIFIED document | Editing disabled/prevented |
| 5.4.8 | View document hash | Click on document | BLAKE2b-256 hash displayed |
| 5.4.9 | View document lineage | Click "View Lineage" or provenance tab | Timeline/graph of events |

### 5.5 Document Certification (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.5.1 | Submit for certification | Click "Submit for Certification" on DRAFT | Status changes to PENDING |
| 5.5.2 | Certification event logged | Check lineage/events | ISSUED event recorded |
| 5.5.3 | Notification sent | Check if holder is notified | Notification/email sent |

### 5.6 Document Signing (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.6.1 | Sign with wallet | Click "Sign Document" | Wallet popup appears |
| 5.6.2 | Approve signature | Sign CIP-8 message in wallet | Signature stored, SIGNED event logged |
| 5.6.3 | Signature visible | View document details | Signature with wallet address shown |
| 5.6.4 | Multiple signatures | Have second signer also sign | Both signatures recorded |

### 5.7 Document Signing (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.7.1 | Reject signing | Start sign flow, reject in wallet | Graceful error, can retry |
| 5.7.2 | Sign with wrong wallet | Connect different wallet than registered | Warning or error |
| 5.7.3 | Sign already-signed doc | Try to sign document you already signed | Prevented or recorded as additional signature |
| 5.7.4 | Wallet disconnects mid-sign | Disconnect wallet during signing | Error with retry option |

### 5.8 Blockchain Anchoring (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.8.1 | Anchor document | Click "Anchor to Blockchain" | Transaction submitted, PENDING status |
| 5.8.2 | Confirmation tracking | Monitor anchor status | Status updates: PENDING → CONFIRMED |
| 5.8.3 | Transaction hash | View anchor details | Cardano tx hash displayed |
| 5.8.4 | Block confirmation | Wait for confirmations | Confirmation count increments |

### 5.9 Document Sharing (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.9.1 | Share with individual | Enter email, click share | Share record created, email sent to recipient |
| 5.9.2 | Share with expiration | Set share to expire in 7 days | Expiration saved |
| 5.9.3 | Batch share | Select multiple documents, share | All shared |
| 5.9.4 | View share history | Check sharing tab on document | List of shares with status |
| 5.9.5 | Revoke share | Click revoke on active share | Share deactivated |

### 5.10 Document Sharing (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.10.1 | Share with invalid email | Enter "notanemail" | Validation error |
| 5.10.2 | Share with self | Enter own email | Prevented or allowed (harmless) |
| 5.10.3 | Share expired document | Try to share EXPIRED doc | Prevented or warned |
| 5.10.4 | Share revoked document | Try to share REVOKED doc | Prevented |
| 5.10.5 | Access expired share | Click share link after expiry | Access denied with clear message |

### 5.11 Document Revocation (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.11.1 | Revoke document | Click "Revoke", enter reason | Status changes to REVOKED, event logged |
| 5.11.2 | Revocation reason stored | View revoked document | Reason visible |
| 5.11.3 | Revoked doc not verifiable | Try to verify revoked doc via verifier portal | Shows REVOKED status |

### 5.12 NFT Certificate Minting (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.12.1 | Mint as NFT | Click "Mint as NFT" on certified doc | NFT minting initiated |
| 5.12.2 | NFT metadata | Check NFT metadata | CIP-25 compliant metadata |
| 5.12.3 | NFT visible | After minting | NFT transaction hash displayed |

### 5.13 Signatories Management (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 5.13.1 | View signatories page | Navigate to signatories | Page loads, list or empty state |
| 5.13.2 | Add signatory | Click "Add", enter details | Signatory added |
| 5.13.3 | Assign to document | Assign signatory to document | Signatory linked |

---

## 9. Module 6: Certifier (Document Approver)

**File:** `tests/e2e/tests/certifier-exhaustive.issuer.spec.ts`

### 6.1 Certification Queue (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 6.1.1 | View pending approvals | Login as certifier, view queue | List of documents awaiting approval |
| 6.1.2 | Review document | Click on pending document | Full document details, metadata, file preview |
| 6.1.3 | Approve document | Click "Approve" | Status → CERTIFIED, event logged |
| 6.1.4 | Reject document | Click "Reject", enter reason | Status → REJECTED, reason stored |
| 6.1.5 | Sign during approval | Approve and sign with wallet | Both approval and signature recorded |

### 6.2 Certification Queue (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 6.2.1 | Approve already-approved | Try to approve certified doc | Prevented |
| 6.2.2 | Reject without reason | Click reject with empty reason | Required field validation |
| 6.2.3 | Approve as wrong role | Non-certifier tries to approve | Access denied |
| 6.2.4 | Approve own document | Certifier tries to approve their own submission | Prevented (conflict of interest) or allowed per config |

---

## 10. Module 7: Rights Holder (Document Owner)

**File:** `tests/e2e/tests/holder-exhaustive.issuer.spec.ts`

### 7.1 View Credentials (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 7.1.1 | View received documents | Login as holder | List of documents issued to them |
| 7.1.2 | View document detail | Click on document | Full certification details |
| 7.1.3 | Verify own document | Click "Verify" | Verification passes, hash matches |
| 7.1.4 | View lineage | Click lineage/provenance | Full event history |
| 7.1.5 | Download certificate | Click download | PDF/certificate file downloaded |

### 7.2 Share & Privacy (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 7.2.1 | Share credential | Share with employer email | Share created, email sent |
| 7.2.2 | Set access controls | Set view-only, no download | Restrictions enforced |
| 7.2.3 | Revoke share | Revoke shared access | Access removed |
| 7.2.4 | View who has access | Check access list | All shares visible |
| 7.2.5 | Request privacy proof (ZKP) | Generate selective disclosure proof | Proof generated without revealing PII |

### 7.3 Holder (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 7.3.1 | Access document not owned | Try to view someone else's doc via URL manipulation | Access denied |
| 7.3.2 | Share revoked document | Try to share a revoked credential | Prevented |
| 7.3.3 | Modify own document | Try to edit certified doc content | Prevented (immutable after certification) |

---

## 11. Module 8: Verifier

**File:** `tests/e2e/tests/verifier-exhaustive.verifier.spec.ts`

### 8.1 Document Verification (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 8.1.1 | Verifier portal loads | Navigate to `/verify/` | Clean verification interface |
| 8.1.2 | Upload document for verification | Upload file | Hash calculated, compared to blockchain record |
| 8.1.3 | Verify authentic document | Upload original certified document | VERIFIED — hash matches, green confirmation |
| 8.1.4 | View certification details | After verification | Issuer, date, signatures, blockchain anchor |
| 8.1.5 | View blockchain proof | Click "View on Blockchain" | Transaction details shown |
| 8.1.6 | Enter hash directly | Paste document hash instead of file | Verification by hash works |
| 8.1.7 | Verify shared document | Access shared verification link | Document verified, access granted per permissions |

### 8.2 Document Verification (Variations)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 8.2.1 | Verify tampered document | Upload modified version of certified doc | FAILED — hash mismatch, red warning |
| 8.2.2 | Verify unknown document | Upload doc never certified | NOT FOUND — no matching record |
| 8.2.3 | Verify revoked document | Upload revoked doc | REVOKED — warning shown with revocation reason |
| 8.2.4 | Verify expired document | Upload expired doc | EXPIRED — with expiration date |
| 8.2.5 | Upload non-PDF for verification | Upload `.txt` file | Handled (hash calculated regardless) or type error |
| 8.2.6 | Empty hash field | Click verify with empty input | Validation error |
| 8.2.7 | Invalid hash format | Enter "notahash" | Error: invalid hash format |
| 8.2.8 | Very rapid verifications | Submit 20 verifications in 10 seconds | Rate limited after threshold |

### 8.3 Verification as Logged-In Verifier

| # | Test | Action | Expected Result |
|---|---|---|---|
| 8.3.1 | Login as verifier | Login to verifier portal | Dashboard with verification history |
| 8.3.2 | View verification history | Check past verifications | List with dates, results |
| 8.3.3 | Batch verify | Upload multiple documents | All verified, results shown |

---

## 12. Module 9: Public / Anonymous User

**File:** `tests/e2e/tests/public-exhaustive.web.spec.ts`

### 9.1 Public Access (Happy Path)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 9.1.1 | Access verifier without login | Navigate to `/verify/` | Can verify documents without account |
| 9.1.2 | Verify document anonymously | Upload and verify | Result shown, no login required |
| 9.1.3 | View status page | Navigate to `/status/` | System status visible |
| 9.1.4 | Marketing website | Navigate to `http://localhost:6881` | Landing page, features, pricing |
| 9.1.5 | Registration accessible | Click "Sign Up" from verifier | Registration form accessible |

### 9.2 Public Access (Variations — Access Control)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 9.2.1 | Access admin without login | Navigate to `/admin/` directly | Redirected to login |
| 9.2.2 | Access issuer without login | Navigate to `/` (issuer) directly | Redirected to login |
| 9.2.3 | Access API without auth | Call `GET /api/documents` without JWT | 401 Unauthorized |
| 9.2.4 | Access admin API as public | Call `GET /api/admin/users` without auth | 401 Unauthorized |
| 9.2.5 | Access share link | Click valid share link | Document visible per share permissions |
| 9.2.6 | Access expired share link | Click expired share link | Access denied with clear message |
| 9.2.7 | Access revoked share link | Click revoked share link | Access denied |

---

## 13. Module 10: Cross-Persona End-to-End Flows

**File:** `tests/e2e/tests/cross-persona-e2e.spec.ts`

### 10.1 Full Certification Lifecycle

| # | Test | Action | Expected Result |
|---|---|---|---|
| 10.1.1 | Admin creates org | Login as admin, create "Test University" | Org created |
| 10.1.2 | Admin creates doc type | Create "Bachelor's Degree" type | Type created |
| 10.1.3 | Admin creates user (issuer) | Create issuer user for Test University | User created |
| 10.1.4 | Admin creates user (certifier) | Create certifier user | User created |
| 10.1.5 | Issuer logs in | Login as new issuer | Dashboard loaded |
| 10.1.6 | Issuer creates document | Upload degree PDF, fill metadata | Document created (DRAFT) |
| 10.1.7 | Issuer submits for cert | Submit for certification | Status → PENDING |
| 10.1.8 | Certifier logs in | Login as certifier | Queue shows pending doc |
| 10.1.9 | Certifier reviews | View document details | All info correct |
| 10.1.10 | Certifier approves | Approve document | Status → CERTIFIED |
| 10.1.11 | Certifier signs | Sign with wallet | Signature recorded |
| 10.1.12 | Document anchored | Anchor to blockchain | Tx hash recorded |
| 10.1.13 | Holder receives | Login as holder | Document in their credentials |
| 10.1.14 | Holder shares | Share with verifier email | Share link created |
| 10.1.15 | Verifier verifies | Upload same document in verifier portal | VERIFIED — all checks pass |
| 10.1.16 | Public verifies | Anonymous user verifies same doc | VERIFIED |
| 10.1.17 | Tamper detection | Modify file, verify again | FAILED — tamper detected |

### 10.2 Recruitment Use Case (End-to-End)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 10.2.1 | University issues degree | Full certification flow for degree | Certified |
| 10.2.2 | Professional body issues cert | Full flow for professional certification | Certified |
| 10.2.3 | Employer issues reference | Full flow for employment reference | Certified |
| 10.2.4 | Candidate collects all | Holder views all 3 credentials | All visible |
| 10.2.5 | Candidate shares with recruiter | Share all 3 with recruiter email | Shares created |
| 10.2.6 | Recruiter verifies all | Verify each credential | All pass |
| 10.2.7 | Recruiter checks blockchain | View blockchain anchors | Transactions confirmed |

### 10.3 Document Revocation Flow

| # | Test | Action | Expected Result |
|---|---|---|---|
| 10.3.1 | Issue and certify doc | Full happy path | Certified |
| 10.3.2 | Share with verifier | Share document | Shared |
| 10.3.3 | Verifier confirms valid | Verify document | VERIFIED |
| 10.3.4 | Issuer revokes | Revoke with reason "Fraudulent claim" | Status → REVOKED |
| 10.3.5 | Verifier re-verifies | Same document | REVOKED — shows revocation reason |
| 10.3.6 | Holder sees revocation | Holder views credential | REVOKED status visible |
| 10.3.7 | Share link blocked | Access share link | Shows revoked status |

### 10.4 GDPR Flow

| # | Test | Action | Expected Result |
|---|---|---|---|
| 10.4.1 | User requests data export | Submit DSR for data access | Export generated |
| 10.4.2 | Admin processes DSR | View in system health, approve | Data export available for download |
| 10.4.3 | User downloads data | Download exported data | JSON/CSV with all personal data |
| 10.4.4 | User requests erasure | Submit erasure request | Request logged |
| 10.4.5 | Admin processes erasure | Approve erasure | User data soft-deleted, audit trail maintained |
| 10.4.6 | Verify erasure | Try to login as deleted user | Account inaccessible |
| 10.4.7 | Documents preserved | Check certified documents | Hash/blockchain anchor preserved (immutable), PII removed |

---

## 14. Module 11: Negative & Error Path Testing

**File:** `tests/e2e/tests/negative-paths.spec.ts`

### 11.1 Network & Service Failures

| # | Test | Action | Expected Result |
|---|---|---|---|
| 11.1.1 | API timeout | Simulate slow API response | Loading indicator, then timeout message |
| 11.1.2 | 500 error from API | API returns 500 | User-friendly error, not raw stack trace |
| 11.1.3 | Lost internet mid-action | Disconnect network during upload | Error message, data not lost |
| 11.1.4 | Session expired mid-action | JWT expires while filling form | Redirect to login, form data preserved if possible |

### 11.2 Concurrent Action Conflicts

| # | Test | Action | Expected Result |
|---|---|---|---|
| 11.2.1 | Two users edit same doc | Both open edit, both save | Last write wins or conflict resolution |
| 11.2.2 | Double-click submit | Click submit twice rapidly | Only one submission processed |
| 11.2.3 | Approve while being revoked | Certifier approves while issuer revokes same doc | Consistent final state |

### 11.3 Browser Edge Cases

| # | Test | Action | Expected Result |
|---|---|---|---|
| 11.3.1 | Back button after login | Login, then press Back | Doesn't show login form with credentials |
| 11.3.2 | Back button after logout | Logout, then press Back | Doesn't show authenticated content |
| 11.3.3 | Multiple tabs same user | Open same page in 2 tabs | Both work, data consistent |
| 11.3.4 | Multiple tabs different users | Login as admin in tab 1, issuer in tab 2 | Sessions isolated (different cookies per tab not possible, but consistent) |
| 11.3.5 | Refresh during form submission | F5 during submit | No duplicate submission |
| 11.3.6 | Bookmark authenticated page | Bookmark `/admin/users`, logout, revisit | Redirect to login, then back to bookmarked page |

---

## 15. Module 12: Bad Actor / Security Testing

**File:** `tests/e2e/tests/security-bad-actor.spec.ts`

> **Context:** These tests simulate an authorized penetration test against the platform to find vulnerabilities before external users do.

### 12.1 Authentication Bypass Attempts

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.1.1 | JWT forgery | Create JWT with admin role, sign with random key | Rejected (signature verification fails) |
| 12.1.2 | JWT algorithm none | Set JWT alg to "none", remove signature | Rejected |
| 12.1.3 | JWT role escalation | Login as VERIFIER, modify JWT role to ADMIN | Rejected on next API call |
| 12.1.4 | JWT with different user ID | Login as user A, set JWT userId to user B | Rejected or only returns user A's data |
| 12.1.5 | Expired JWT reuse | Save expired JWT, replay | Rejected |
| 12.1.6 | JWT in URL parameter | Send JWT as query parameter | Should use httpOnly cookie, not URL |
| 12.1.7 | Brute force login | Attempt 100 logins with wrong password | Rate limited after 5 attempts |
| 12.1.8 | Credential stuffing | Try common passwords against known emails | Rate limited, no account lockout info leak |

### 12.2 Authorization Bypass (IDOR / Privilege Escalation)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.2.1 | Access other user's document | Login as User A, request User B's document by ID | 403 Forbidden |
| 12.2.2 | Access other org's data | Login as Org A user, request Org B's documents | 403 Forbidden |
| 12.2.3 | IDOR on user profile | Change user ID in profile API call | Only own profile returned |
| 12.2.4 | Verifier accesses admin API | Login as verifier, call `/api/admin/users` | 403 Forbidden |
| 12.2.5 | Issuer deletes org | Login as issuer, call DELETE on organisation | 403 Forbidden |
| 12.2.6 | Modify document you don't own | PUT/PATCH on another user's document | 403 Forbidden |
| 12.2.7 | Revoke someone else's document | Call revoke API on doc you don't own | 403 Forbidden |
| 12.2.8 | Access other tenant's data | Login to tenant A, try API calls with tenant B's IDs | 403 or 404 (no data leakage) |
| 12.2.9 | Enumerate user IDs | Try sequential user IDs (1, 2, 3...) | 403 for each, not 404 (prevents enumeration) |
| 12.2.10 | Enumerate document IDs | Try sequential document IDs | 403 for unauthorized, 404 same response time |

### 12.3 Injection Attacks

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.3.1 | SQL injection — login | Email: `admin'--`, Password: anything | Login fails, no SQL error |
| 12.3.2 | SQL injection — search | Search documents: `'; DROP TABLE documents;--` | Sanitized, search works normally |
| 12.3.3 | SQL injection — API params | `GET /api/documents?status=CERTIFIED' OR '1'='1` | Parameterized query, no injection |
| 12.3.4 | NoSQL injection | `{"email": {"$gt": ""}}` in login body | Rejected |
| 12.3.5 | XSS — stored (document title) | Create doc with title `<script>alert('XSS')</script>` | HTML-encoded when displayed |
| 12.3.6 | XSS — reflected (search) | Search with `<img src=x onerror=alert(1)>` | Input sanitized in response |
| 12.3.7 | XSS — DOM-based (URL params) | Navigate to `/?redirect=javascript:alert(1)` | Not executed |
| 12.3.8 | SSTI — template injection | Metadata field: `{{7*7}}` or `${7*7}` | Rendered as literal text, not 49 |
| 12.3.9 | Command injection — file name | Upload file named `; rm -rf /` | Sanitized filename |
| 12.3.10 | Path traversal — file access | `GET /api/documents/../../etc/passwd` | Rejected, no file contents |
| 12.3.11 | LDAP injection | Login with `*)(uid=*))(|(uid=*` | Rejected |
| 12.3.12 | Header injection | `X-Forwarded-For: 127.0.0.1` to bypass IP check | Validated against trusted proxies only |

### 12.4 CSRF Attacks

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.4.1 | Cross-origin POST | POST to `/api/documents` from different origin | CSRF token required, rejected |
| 12.4.2 | Cross-origin DELETE | DELETE request from evil.com | Rejected by CORS + CSRF |
| 12.4.3 | CSRF token reuse | Use same CSRF token twice | Rejected (if one-time tokens) or accepted (if session-scoped) |
| 12.4.4 | Missing CSRF token | Omit CSRF token from state-changing request | Rejected |

### 12.5 Session Security

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.5.1 | Session fixation | Set session ID before login | New session created after login |
| 12.5.2 | Session hijacking | Copy JWT from browser A, use in browser B | Risk: if httpOnly cookies, can't extract via JS |
| 12.5.3 | Concurrent sessions | Login from two browsers | Both work (or single-session enforcement) |
| 12.5.4 | Session after password change | Change password | All other sessions invalidated |
| 12.5.5 | Cookie flags | Inspect Set-Cookie header | HttpOnly, Secure (in prod), SameSite=Strict/Lax |

### 12.6 File Upload Attacks

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.6.1 | Upload executable | Upload `malware.exe` renamed to `.pdf` | Content-type validation rejects |
| 12.6.2 | Upload SVG with script | Upload SVG containing JavaScript | Sanitized or rejected |
| 12.6.3 | Upload polyglot file | File that is both valid JPEG and valid JS | Served with correct content-type, no execution |
| 12.6.4 | Zip bomb | Upload highly compressed file | Size limit or decompression limit |
| 12.6.5 | Upload to overwrite | Try to overwrite existing file via path manipulation | Prevented |
| 12.6.6 | File inclusion via filename | Filename: `../../../etc/passwd` | Path normalized, no traversal |

### 12.7 API Security

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.7.1 | Rate limiting works | Send 100 requests/second | Rate limited after threshold |
| 12.7.2 | Missing Content-Type | POST without Content-Type header | 400 or handled gracefully |
| 12.7.3 | Wrong Content-Type | Send XML to JSON endpoint | 400 Bad Request |
| 12.7.4 | Oversized request body | Send 100MB JSON body | 413 Payload Too Large |
| 12.7.5 | Deeply nested JSON | Send JSON 100 levels deep | Rejected or limited |
| 12.7.6 | Array of 10000 items | Send huge array in request | Size limited |
| 12.7.7 | HTTP method override | `X-HTTP-Method-Override: DELETE` on GET request | Not honored (or if honored, properly authorized) |
| 12.7.8 | CORS preflight | OPTIONS request from evil.com | Only allowed origins returned |
| 12.7.9 | API versioning bypass | Try `/api/v0/` or `/api/v99/` | 404, not exposing old/internal APIs |
| 12.7.10 | GraphQL introspection | If GraphQL exists, query `__schema` | Disabled in production |

### 12.8 Blockchain-Specific Attacks

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.8.1 | Fake anchor | Submit fake tx hash via API | Rejected (tx hash verified against chain) |
| 12.8.2 | Replay anchor | Resubmit same anchor transaction | Detected as duplicate |
| 12.8.3 | Anchor tampering | Modify hash before anchoring | Hash mismatch detected on verification |
| 12.8.4 | Forge wallet signature | Submit fabricated CIP-8 signature | Cryptographic verification fails |
| 12.8.5 | Impersonate wallet | Claim ownership of someone else's wallet address | Challenge-response verification prevents |

### 12.9 Data Exposure

| # | Test | Action | Expected Result |
|---|---|---|---|
| 12.9.1 | Error messages | Trigger 500 errors | No stack traces, DB details, or internal paths |
| 12.9.2 | API response leakage | Check API responses for extra fields | No password hashes, internal IDs, or PII in responses |
| 12.9.3 | Debug endpoints | Check for `/debug`, `/actuator`, `/_debug` | Not accessible |
| 12.9.4 | Source maps | Check for `.map` files in production | Not served |
| 12.9.5 | Directory listing | Navigate to `/api/` | No directory listing |
| 12.9.6 | Sensitive headers | Check response headers | No `X-Powered-By`, `Server` version |
| 12.9.7 | Swagger in production | Check `/api/docs` in prod config | Should be disabled or auth-protected |
| 12.9.8 | Database dump in response | Check for mass-assignment in API | Only requested fields returned |

---

## 16. Module 13: Performance & Stress Testing

**File:** `tests/e2e/tests/performance.spec.ts`

### 13.1 Page Load Performance

| # | Test | Action | Expected Result |
|---|---|---|---|
| 13.1.1 | Issuer portal FCP | Measure First Contentful Paint | < 2 seconds |
| 13.1.2 | Admin portal FCP | Measure FCP | < 2 seconds |
| 13.1.3 | Verifier portal FCP | Measure FCP | < 1.5 seconds (public-facing) |
| 13.1.4 | Document list with 100 docs | Load page with many docs | Renders within 3 seconds |
| 13.1.5 | Document list with 1000 docs | Load page with many docs | Pagination works, no timeout |
| 13.1.6 | Audit log with 10000 entries | Load audit logs | Paginated, responsive |

### 13.2 API Response Times

| # | Test | Action | Expected Result |
|---|---|---|---|
| 13.2.1 | Login API | POST /api/auth/login | < 500ms |
| 13.2.2 | Document list API | GET /api/documents | < 300ms |
| 13.2.3 | Verification API | POST /api/verification/verify | < 1 second |
| 13.2.4 | Hash calculation | Upload 10MB file | < 2 seconds |
| 13.2.5 | Concurrent API calls | 50 simultaneous requests | All respond within 5 seconds |

### 13.3 Upload Performance

| # | Test | Action | Expected Result |
|---|---|---|---|
| 13.3.1 | Small file upload | Upload 100KB PDF | < 1 second |
| 13.3.2 | Medium file upload | Upload 5MB PDF | < 5 seconds |
| 13.3.3 | Large file upload | Upload 25MB PDF | < 30 seconds with progress indicator |
| 13.3.4 | Progress indicator | Upload large file | Progress bar updates smoothly |

---

## 17. Module 14: Accessibility & Cross-Browser

**File:** `tests/e2e/tests/accessibility-crossbrowser.spec.ts`

### 14.1 Accessibility (WCAG 2.1 AA)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 14.1.1 | Keyboard navigation | Tab through login page | All interactive elements reachable |
| 14.1.2 | Focus indicators | Tab through forms | Visible focus rings on all elements |
| 14.1.3 | Form labels | Check all inputs have labels | `<label>` or `aria-label` present |
| 14.1.4 | Alt text on images | Check all `<img>` tags | Alt text present |
| 14.1.5 | Color contrast | Check text contrast ratios | Minimum 4.5:1 for normal text |
| 14.1.6 | Screen reader compatibility | Check ARIA roles and landmarks | Proper semantic HTML and ARIA |
| 14.1.7 | Error announcements | Submit invalid form | Errors announced to screen reader |
| 14.1.8 | No keyboard traps | Tab through modals | Can escape with Esc key |

### 14.2 Cross-Browser Testing

| # | Test | Action | Expected Result |
|---|---|---|---|
| 14.2.1 | Chrome (latest) | Full login + document flow | Works |
| 14.2.2 | Firefox (latest) | Full login + document flow | Works |
| 14.2.3 | Safari (latest) | Full login + document flow | Works |
| 14.2.4 | Edge (latest) | Full login + document flow | Works |
| 14.2.5 | Mobile Chrome (emulated) | Full flow on 375px viewport | Responsive, all features accessible |
| 14.2.6 | Mobile Safari (emulated) | Full flow on iPhone viewport | Responsive |
| 14.2.7 | Tablet (emulated) | Full flow on iPad viewport | Responsive |

---

## 18. Module 15: GDPR & Compliance Testing

**File:** `tests/e2e/tests/gdpr-compliance.spec.ts`

### 15.1 Consent Management

| # | Test | Action | Expected Result |
|---|---|---|---|
| 15.1.1 | Consent banner shown | First visit | Cookie/consent banner visible |
| 15.1.2 | Accept all | Click "Accept All" | Consent recorded, banner dismissed |
| 15.1.3 | Reject all | Click "Reject All" | Only essential cookies set |
| 15.1.4 | Customize consent | Select individual purposes | Only selected purposes active |
| 15.1.5 | Consent persists | Reload page | Banner not shown again |
| 15.1.6 | Withdraw consent | Go to privacy settings, withdraw | Consent updated, non-essential cookies cleared |

### 15.2 Data Subject Rights

| # | Test | Action | Expected Result |
|---|---|---|---|
| 15.2.1 | Request data access | Submit DSR for access | Request logged, processing begins |
| 15.2.2 | Receive data export | Admin processes, user downloads | Complete data export in JSON/CSV |
| 15.2.3 | Data portability | Export in machine-readable format | Standard format (JSON) |
| 15.2.4 | Request rectification | Ask to update personal data | Data updated |
| 15.2.5 | Request erasure | Submit erasure request | Data deleted per retention policy |
| 15.2.6 | Erasure preserves audit | After erasure | Audit trail maintained but anonymized |
| 15.2.7 | Blockchain immutability | After erasure | On-chain hashes remain (no PII on chain) |

### 15.3 Data Retention

| # | Test | Action | Expected Result |
|---|---|---|---|
| 15.3.1 | Retention policy visible | Admin checks retention settings | Policies listed with durations |
| 15.3.2 | Auto-delete expired data | Trigger retention enforcement | Expired data removed |
| 15.3.3 | Retention audit trail | After enforcement | Log of what was deleted and why |

### 15.4 PII Tokenisation

| # | Test | Action | Expected Result |
|---|---|---|---|
| 15.4.1 | PII encrypted at rest | Check database directly | PII fields are tokenised, not plaintext |
| 15.4.2 | Per-tenant encryption | Check different tenant data | Different encryption keys used |
| 15.4.3 | Token resolution | API returns readable data | Detokenised for authorized users only |

---

## 19. Module 16: Blockchain & Crypto Wallet Testing

**File:** `tests/e2e/tests/blockchain-wallet.spec.ts`

### 16.1 Wallet Connection

| # | Test | Action | Expected Result |
|---|---|---|---|
| 16.1.1 | Detect installed wallets | Load wallet connection page | Lists available CIP-30 wallets |
| 16.1.2 | Connect Nami | Select Nami, approve | Connected, address shown |
| 16.1.3 | Connect Eternl | Select Eternl, approve | Connected, address shown |
| 16.1.4 | Connect Lace | Select Lace, approve | Connected, address shown |
| 16.1.5 | Disconnect wallet | Click disconnect | Wallet disconnected, address removed |
| 16.1.6 | Reconnect wallet | Disconnect then reconnect | Works without issues |

### 16.2 Transaction Signing

| # | Test | Action | Expected Result |
|---|---|---|---|
| 16.2.1 | Sign document hash | Initiate CIP-8 signing | Wallet prompts, signature stored |
| 16.2.2 | Verify signature | Check signature on-chain | Signature valid |
| 16.2.3 | Sign with hardware wallet | Use Ledger/Trezor (if available) | Works via wallet extension |

### 16.3 Blockchain Anchoring

| # | Test | Action | Expected Result |
|---|---|---|---|
| 16.3.1 | Submit anchor tx (devnet) | Anchor document on local devnet | Tx submitted, confirmation received |
| 16.3.2 | Submit anchor tx (preprod) | Anchor on preprod testnet | Tx submitted |
| 16.3.3 | View anchor on explorer | Click blockchain link | Opens explorer with tx details |
| 16.3.4 | Anchor retry on failure | Simulate failed tx | Retried with exponential backoff |
| 16.3.5 | Anchor fee calculation | View estimated fee | Fee displayed before anchoring |

---

## 20. Module 17: Email & Notification Testing

**File:** `tests/e2e/tests/email-notifications.spec.ts`

### 17.1 Email Delivery (via Agent Mail)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 17.1.1 | Registration verification email | Register new account | Email received with verification link |
| 17.1.2 | Password reset email | Request reset | Email received with reset link |
| 17.1.3 | Document shared notification | Share document with email | Recipient gets email with access link |
| 17.1.4 | Certification complete notification | Certify document | Holder gets email notification |
| 17.1.5 | Revocation notification | Revoke document | Holder and verifiers notified |
| 17.1.6 | GDPR DSR confirmation | Submit DSR | Confirmation email sent |

### 17.2 Email Content Validation

| # | Test | Action | Expected Result |
|---|---|---|---|
| 17.2.1 | Links are valid | Click links in emails | Navigate to correct pages |
| 17.2.2 | No PII in email headers | Check email headers | No sensitive data leaked |
| 17.2.3 | Email rendering | View in HTML and plain text | Both readable |
| 17.2.4 | Unsubscribe link | Check marketing emails | Unsubscribe option present |
| 17.2.5 | Branding consistent | Check email design | Secuura branding, logos |

### 17.3 Email Edge Cases

| # | Test | Action | Expected Result |
|---|---|---|---|
| 17.3.1 | Invalid recipient email | Share to non-existent email | Email bounces gracefully, no crash |
| 17.3.2 | Email to self | Trigger notification to self | Email delivered (or skipped with in-app notification) |
| 17.3.3 | Rapid email sending | Trigger 50 notifications quickly | Queued and delivered, not dropped |

---

## 21. Module 18: API Contract & Integration Testing

**File:** `tests/e2e/tests/api-contract.api.spec.ts`

### 18.1 API Endpoint Contracts

| # | Test | Action | Expected Result |
|---|---|---|---|
| 18.1.1 | OpenAPI spec valid | Fetch `/api/docs` spec | Valid OpenAPI 3.1 JSON |
| 18.1.2 | All documented endpoints exist | Call each endpoint from spec | None return 404 |
| 18.1.3 | Response schemas match | Compare responses to spec schemas | All fields match types |
| 18.1.4 | Required fields enforced | Omit required fields | 400 with field-level errors |
| 18.1.5 | Pagination works | List with `?page=1&limit=10` | Correct page size, total count |
| 18.1.6 | Sorting works | List with `?sort=createdAt&order=desc` | Correct order |
| 18.1.7 | Filtering works | List with `?status=CERTIFIED` | Only matching results |

### 18.2 Webhook Integration

| # | Test | Action | Expected Result |
|---|---|---|---|
| 18.2.1 | Webhook delivery | Certify document with webhook configured | POST to webhook URL with event payload |
| 18.2.2 | Webhook retry | Webhook endpoint returns 500 | Retried with backoff |
| 18.2.3 | Webhook signature | Check webhook payload signature | HMAC signature valid |
| 18.2.4 | Webhook timeout | Webhook endpoint hangs | Timeout and retry |

### 18.3 M365 Integration

| # | Test | Action | Expected Result |
|---|---|---|---|
| 18.3.1 | Outlook Add-in loads | Open add-in in Outlook (simulated) | Add-in renders |
| 18.3.2 | Verify from Outlook | Verify document from email attachment | Verification result displayed |
| 18.3.3 | SharePoint integration | Certify from SharePoint | Document certified |

---

## 22. Module 19: Multi-Tenancy & Data Isolation

**File:** `tests/e2e/tests/multi-tenancy.platform.spec.ts`

### 19.1 Tenant Isolation

| # | Test | Action | Expected Result |
|---|---|---|---|
| 19.1.1 | Create tenant | Admin creates new tenant | Tenant database created, schema migrated |
| 19.1.2 | Tenant has own data | Create document in tenant A | Not visible from tenant B |
| 19.1.3 | Cross-tenant API isolation | Login to tenant A, request tenant B's API | 403 or 404 |
| 19.1.4 | Cross-tenant user isolation | Tenant A admin can't see tenant B users | Properly scoped |
| 19.1.5 | PII isolation | Each tenant's PII encrypted separately | Different encryption keys |
| 19.1.6 | Shared platform services | Both tenants can use verification | Works independently |

### 19.2 Tenant Lifecycle

| # | Test | Action | Expected Result |
|---|---|---|---|
| 19.2.1 | Provision tenant | Full provisioning flow | Database, schema, seed data created |
| 19.2.2 | Tenant migration | Run schema migration on tenant | Schema updated without data loss |
| 19.2.3 | Tenant backup | Trigger backup | Backup created |
| 19.2.4 | Suspend tenant | Suspend tenant | Users can't login, data preserved |
| 19.2.5 | Reactivate tenant | Reactivate suspended tenant | Users can login, data intact |

---

## 23. Module 20: Azure Environment Parity & Production Readiness

**File:** `tests/e2e/tests/azure-environment-parity.spec.ts`

> These tests run ONLY against the Azure demo environment. They validate that the deployed environment behaves identically to local and is ready for external testers.

### 20.1 Azure Infrastructure Health

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.1.1 | API Gateway health | `GET https://secuura-demo-api.../health` | 200 OK, all services healthy |
| 20.1.2 | Issuer Portal loads over HTTPS | Navigate to issuer URL | Page loads, TLS valid, no mixed content |
| 20.1.3 | Verifier Portal loads over HTTPS | Navigate to verifier URL | Page loads, TLS valid |
| 20.1.4 | Admin Portal loads over HTTPS | Navigate to admin URL | Page loads, TLS valid |
| 20.1.5 | API docs accessible | Navigate to `/api/docs` | Swagger UI loads (or properly restricted) |
| 20.1.6 | No debug endpoints exposed | Check `/debug`, `/_debug`, `/actuator` | 404 on all |
| 20.1.7 | CORS properly configured | Send cross-origin request from unknown origin | Rejected |
| 20.1.8 | Security headers present | Check response headers | Helmet headers: X-Frame-Options, CSP, HSTS, no X-Powered-By |
| 20.1.9 | HSTS enabled | Check Strict-Transport-Security header | Present with max-age |
| 20.1.10 | No source maps served | Check for `.js.map` files | 404 or not served |

### 20.2 Azure TLS & Certificate Validation

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.2.1 | TLS version | Check supported TLS versions | TLS 1.2+ only |
| 20.2.2 | Certificate valid | Check cert expiry | Not expiring within 30 days |
| 20.2.3 | HTTP → HTTPS redirect | Navigate to `http://` version | Redirected to `https://` |
| 20.2.4 | No mixed content | Load pages, check console | No mixed content warnings |

### 20.3 Azure Authentication (Production Security)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.3.1 | Login works over HTTPS | Login as demo issuer | JWT set via Secure httpOnly cookie |
| 20.3.2 | Cookie Secure flag | Inspect Set-Cookie | `Secure` flag present (HTTPS) |
| 20.3.3 | Cookie SameSite | Inspect Set-Cookie | `SameSite=Lax` or `Strict` |
| 20.3.4 | CSRF enforced | POST without CSRF token | Rejected (production mode) |
| 20.3.5 | Rate limiting active | Rapid login attempts | Rate limited at production thresholds (5/15min) |
| 20.3.6 | JWT secret not default | Login, inspect JWT | Not signed with dev default secret |
| 20.3.7 | Demo seeding disabled | Check for demo data flag | `DEMO_SEED=false` in production (or pre-seeded accounts only) |

### 20.4 Azure vs Local Feature Parity

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.4.1 | Document creation | Create document on Azure | Same flow as local, succeeds |
| 20.4.2 | Document verification | Verify document on Azure | Same result as local |
| 20.4.3 | Admin functions | Create org, user on Azure | Works identically to local |
| 20.4.4 | Search and filtering | Search documents on Azure | Same results as local |
| 20.4.5 | Audit logging | Perform action, check audit log | Logged correctly on Azure |
| 20.4.6 | File upload | Upload PDF on Azure | Succeeds with same size limits |
| 20.4.7 | API response format | Compare API responses local vs Azure | Identical schema and structure |

### 20.5 Azure Performance Baseline

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.5.1 | Login latency | Measure login time on Azure | < 2 seconds |
| 20.5.2 | Page load latency | Measure Issuer portal FCP | < 3 seconds (allows for network latency) |
| 20.5.3 | API response time | Measure document list API | < 1 second |
| 20.5.4 | File upload speed | Upload 5MB file | < 10 seconds |
| 20.5.5 | Cold start detection | Hit API after idle period | Responds within 10 seconds (container cold start) |

### 20.6 Azure Data Persistence

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.6.1 | Data persists across deploys | Create doc, redeploy, check | Document still exists |
| 20.6.2 | Sessions persist across restarts | Login, restart container, check | Session still valid (Redis-backed) |
| 20.6.3 | Uploaded files persist | Upload file, restart, download | File still available |

### 20.7 Azure-Specific Security (Bad Actor)

| # | Test | Action | Expected Result |
|---|---|---|---|
| 20.7.1 | Container escape attempt | Try path traversal via API | No access to container filesystem |
| 20.7.2 | Environment variable leak | Check error responses | No env vars in error messages |
| 20.7.3 | Internal service access | Try to reach internal ports (4000-4023) | Not exposed externally |
| 20.7.4 | Database port exposed | Try to connect to PostgreSQL externally | Not reachable |
| 20.7.5 | Redis port exposed | Try to connect to Redis externally | Not reachable |
| 20.7.6 | Azure Key Vault secrets | Check if secrets in responses | No vault secrets leaked |
| 20.7.7 | Container logs accessible | Try `/logs`, `/console` endpoints | Not accessible |

---

## 24. Test Execution Order & Dependencies

> **Important:** Run `docker restart api-gateway && sleep 5` before each test suite to clear rate limits (200/15min in dev mode).

### Phase 1: Foundation (Run First)
1. Module 1: Infrastructure Smoke
2. Module 2: Authentication (email/password only)

### Phase 2: Admin Setup (Depends on Auth)
3. Module 3: System Administrator
4. Module 4: Organisation Administrator

### Phase 3: Core Workflows (Depends on Admin Setup)
5. Module 5: Issuer
6. Module 6: Certifier
7. Module 7: Rights Holder
8. Module 8: Verifier
9. Module 9: Public User

### Phase 4: Integration (Depends on Core)
10. Module 10: Cross-Persona E2E Flows
11. Module 17: Email & Notification
12. Module 18: API Contract
13. Module 19: Multi-Tenancy

### Phase 5: Hardening (Run Last)
14. Module 11: Negative & Error Paths
15. Module 12: Bad Actor / Security
16. Module 13: Performance
17. Module 14: Accessibility & Cross-Browser
18. Module 15: GDPR & Compliance
19. Module 16: Blockchain & Wallet

### Phase 6: Azure Environment (Run After Local Passes)
20. Module 20: Azure Environment Parity & Production Readiness
21. Re-run Phases 1-4 against Azure (same tests, different BASE_URL)

### Execution Commands

```bash
# ========================================
# LOCAL ENVIRONMENT (run first)
# ========================================

# Run all tests in order
npx playwright test --project=smoke
npx playwright test --project=api --grep="auth"
npx playwright test --project=admin
npx playwright test --project=issuer
npx playwright test --project=verifier
npx playwright test --project=lifecycle
npx playwright test --project=platform

# Run specific module
npx playwright test tests/security-bad-actor.spec.ts

# Run with report
npx playwright test --reporter=html

# Run specific test
npx playwright test -g "JWT forgery"

# ========================================
# AZURE DEMO ENVIRONMENT (run after local passes)
# ========================================

# Set Azure environment variables
export GATEWAY_URL=https://secuura-demo-api.yellowground-ae96b9b1.uksouth.azurecontainerapps.io
export BASE_URL=https://secuura-demo-issuer.yellowground-ae96b9b1.uksouth.azurecontainerapps.io
export API_URL=https://secuura-demo-api.yellowground-ae96b9b1.uksouth.azurecontainerapps.io
export ADMIN_URL=https://secuura-demo-admin.yellowground-ae96b9b1.uksouth.azurecontainerapps.io/admin/
export VERIFIER_URL=https://secuura-demo-verifier.yellowground-ae96b9b1.uksouth.azurecontainerapps.io/verify
export TEST_ENV=azure

# Run Azure-specific parity tests
npx playwright test --project=azure

# Re-run core tests against Azure
npx playwright test --project=smoke
npx playwright test --project=api --grep="auth"
npx playwright test --project=admin
npx playwright test --project=issuer
npx playwright test --project=verifier

# Full Azure test run with report
npx playwright test --reporter=html
```

---

## 24. Reporting & Evidence

### For Each Test Run
- **HTML Report** — `tests/e2e/reports/html/index.html`
- **JSON Results** — `tests/e2e/reports/results.json`
- **Screenshots** — Captured at every critical step + on failure
- **Videos** — Recorded on failure
- **Traces** — Playwright traces for debugging failures

### Test Result Categories
| Status | Meaning |
|---|---|
| PASS | Test passes all assertions |
| FAIL | Test fails an assertion — **bug found** |
| BLOCKED | Test cannot run due to missing prerequisite |
| SKIP | Test intentionally skipped (e.g., no wallet extension) |
| FLAKY | Test passes inconsistently — needs investigation |

### Bug Report Template (for each failure)
```
## Bug: [Short Description]
- **Module:** [Module #]
- **Test ID:** [#.#.#]
- **Severity:** CRITICAL / HIGH / MEDIUM / LOW
- **Steps to Reproduce:** [From test]
- **Expected:** [What should happen]
- **Actual:** [What happened]
- **Screenshot:** [Attached]
- **Video:** [Attached if available]
- **Environment:** Local Docker, macOS, Chrome [version]
```

---

## Summary Statistics (v13 Actual Results — Local Docker)

| Category | Tests | Passed | Failed | Pass Rate |
|---|---|---|---|---|
| Infrastructure & Smoke | 20 | 16 | 4 | 80% |
| Authentication & Identity | 53 | 35 | 18 | 66% |
| System Administrator | 60 | 30 | 30 | 50% |
| Organisation Administrator | 28 | 12 | 16 | 43% |
| Issuer (Document Preparer) | 50 | 18 | 32 | 36% |
| Certifier (Document Approver) | 9 | 5 | 4 | 56% |
| Rights Holder | 15 | 8 | 7 | 53% |
| Verifier | 14 | 8 | 6 | 57% |
| Public / Anonymous User | 12 | 9 | 3 | 75% |
| Cross-Persona E2E | 28 | 16 | 12 | 57% |
| Negative & Error Paths | 12 | 8 | 4 | 67% |
| Bad Actor / Security | 55 | 30 | 25 | 55% |
| Performance & Stress | 13 | 10 | 3 | 77% |
| Accessibility & Cross-Browser | 15 | 9 | 6 | 60% |
| GDPR & Compliance | 17 | 2 | 15 | 12% |
| Blockchain & Wallet | 14 | 2 | 12 | 14% |
| Email & Notification | 14 | 0 | 14 | 0% |
| API Contract & Integration | 11 | 5 | 6 | 45% |
| Multi-Tenancy & Data Isolation | 11 | 1 | 10 | 9% |
| Azure Environment Parity | 32 | 5 | 27 | 16% |
| **TOTAL** | **483** | **219** | **203** | **45%** |
| *Skipped* | | | *61* | |

---

*This plan supersedes all previous test plans. All tests are designed to be implemented as Playwright specs and executed programmatically through browser automation.*
