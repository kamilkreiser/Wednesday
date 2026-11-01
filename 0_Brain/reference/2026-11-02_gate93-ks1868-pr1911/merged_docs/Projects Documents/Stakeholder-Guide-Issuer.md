# Secuura — Issuer Guide

**Certify Documents with Blockchain-Anchored Proof of Authenticity**

**Document Title:** Issuer User Guide  
**Version:** 1.2  
**Date:** 15 February 2026  
**Classification:** External — Issuer Organisations  
**Prepared by:** Secuura

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura | Initial issuer guide |
| 1.1 | 17 Feb 2026 | Secuura | Added NFT Certificate section (Section 11) |
| 1.2 | 17 Feb 2026 | Secuura | Updated document registration flow (client-side hashing, no file upload); session persistence via httpOnly cookies |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What is Secuura?](#2-what-is-secuura)
3. [Why Use Secuura?](#3-why-use-secuura)
4. [Getting Started](#4-getting-started)
5. [The Issuer Portal — Overview](#5-the-issuer-portal--overview)
6. [Creating a Certification](#6-creating-a-certification)
7. [Managing Documents](#7-managing-documents)
8. [Document Lineage](#8-document-lineage)
9. [Sharing Certifications](#9-sharing-certifications)
10. [Wallet Integration](#10-wallet-integration)
11. [NFT Certificates](#11-nft-certificates)
12. [Analytics and Billing](#12-analytics-and-billing)
13. [Settings and Configuration](#13-settings-and-configuration)
14. [Frequently Asked Questions](#14-frequently-asked-questions)
15. [Support](#15-support)

---

## 1. Executive Summary

As an Issuer, you are an organisation or individual that creates and certifies documents on the Secuura platform. This guide walks you through every step of the certification process — from account setup to sharing certified documents with stakeholders.

Secuura provides blockchain-anchored proof that your documents are genuine and unaltered. When you certify a document through Secuura, a cryptographic fingerprint (hash) of that document is permanently recorded on the Cardano blockchain. Anyone can subsequently verify the document's authenticity instantly, without needing to contact you directly.

**Key benefits for issuers:**
- Eliminate manual verification requests (employers, banks, regulators can verify instantly)
- Protect your reputation by making document fraud detectable
- Maintain a complete provenance chain for every document you issue
- Comply with data protection regulations (documents are never stored by Secuura)

---

## 2. What is Secuura?

Secuura is a document authenticity platform. It answers one simple question: **Is this document genuine and unaltered?**

When you certify a document through Secuura:

1. **Your document stays with you** — Secuura never stores, uploads, or transmits your original documents. A cryptographic fingerprint (hash) is computed in your browser and only the hash is sent to the platform.

2. **The hash is recorded on blockchain** — The fingerprint is permanently anchored to the Cardano blockchain, creating an immutable record that no one can alter, delete, or backdate.

3. **Anyone can verify** — When someone needs to check if a document is genuine, they upload it to the Secuura verification portal. A fresh fingerprint is computed and compared against the blockchain record. If they match, the document is verified as authentic.

### What Secuura is NOT

- **Not document storage** — Your documents remain in your systems
- **Not digital signatures** — Secuura proves authenticity, not who signed a document
- **Not a workflow tool** — Secuura focuses on certification and verification

---

## 3. Why Use Secuura?

### The Problem You Face

Every day, organisations like yours receive requests to verify documents you have issued. These requests are time-consuming, expensive, and difficult to manage at scale:

- Universities receive thousands of degree verification requests annually
- HR departments spend hours confirming employment references
- Professional bodies are contacted repeatedly to confirm qualifications
- Government agencies handle verification backlogs

### The Secuura Solution

| Traditional Verification | Secuura Verification |
|--------------------------|---------------------|
| Verifier contacts your organisation | Verifier checks instantly via Secuura |
| Staff manually look up records | Automated blockchain verification |
| Response takes days or weeks | Result in seconds |
| No proof of verification | Blockchain-anchored proof |
| Susceptible to forgery | Tamper-evident by design |

---

## 4. Getting Started

### Step 1: Create Your Organisation Account

**Option A — Email Registration:**
1. Navigate to the Secuura Issuer Portal
2. Click "Create Organisation Account"
3. Enter your organisation details and administrator email
4. Verify your email address via the confirmation link
5. Complete your organisation profile

**Option B — Enterprise SSO (Microsoft Entra ID):**
1. Navigate to the Secuura Issuer Portal
2. Click "Sign in with Microsoft"
3. Authenticate with your organisation's Microsoft credentials
4. Your account is automatically provisioned

### Step 2: Set Up Your Team

As an Organisation Admin, you can invite team members with specific roles:

| Role | What They Can Do |
|------|-----------------|
| **Issuer Admin** | Upload documents, create certification requests, manage metadata |
| **Issuer Approver** | Review certification requests, sign and certify documents |
| **Organisation Admin** | Manage team members, settings, billing |

### Step 3: Connect a Cardano Wallet (Optional)

For certifiers who will sign documents:
1. Install a supported Cardano wallet (Nami, Eternl, Lace, Flint, or others)
2. Navigate to "Wallet" in the portal
3. Click "Connect Wallet" and approve the connection
4. Your wallet address is linked to your account

### Step 4: Configure Document Types

In Settings, configure the types of documents your organisation certifies:
- Degree certificates
- Employment references
- Professional certifications
- Product compliance certificates
- Any custom document type

---

## 5. The Issuer Portal — Overview

When you log in, you will see the main dashboard with:

- **Statistics** — Total documents, certified count, pending count, on-chain count
- **Recent Activity** — Latest certifications, verifications, and shares
- **Quick Actions** — New document, view all documents, access settings
- **Navigation** — Dashboard, Documents, New Document, Document Lineage, Wallet, Settings

### Navigation Guide

| Section | Purpose |
|---------|---------|
| **Dashboard** | Overview of your certification activity |
| **Documents** | List, search, and filter all your documents |
| **New Document** | Register a new document (client-side hashing, no file upload) |
| **Wallet** | Connect and manage your Cardano wallet |
| **Lineage** | View the visual history of any document |
| **Analytics** | Certification volumes, verification rates, trends |
| **Billing** | Chargeable events, pricing, payment |
| **Settings** | Account, team, document types, preferences |

---

## 6. Creating a Certification

### Step-by-Step: Certifying a Document

**Step 1: Register the Document**

1. Navigate to "New Document" in the sidebar or click "New Document" on the dashboard
2. Drag and drop your document into the dropzone, or click to browse (up to 50MB)
3. Supported formats: PDF, PNG, JPG, Word documents, and any other file type
4. **Important — Your file never leaves your device.** Secuura computes a SHA-256 cryptographic fingerprint (hash) of the document entirely in your browser using the Web Crypto API. Only the hash and metadata (title, type, description) are sent to the server. The original file is never uploaded, transmitted, or stored.
5. You will see a confirmation alert displaying the computed hash (e.g., `sha256:e6c15ac940...452e3c`)
6. The page title reads "Register New Document" — reflecting that this is a registration, not an upload

**Step 2: Enter Document Metadata**

Complete the certification form:

| Field | Description | Required |
|-------|-------------|----------|
| **Document Title** | Descriptive name (e.g., "BSc Computer Science — John Smith") | Yes |
| **Document Type** | Category (Certificate, Reference, Licence, etc.) | Yes |
| **Subject Name** | Person or entity the document is about | Yes |
| **Subject Email** | Email for notifications | No |
| **Description** | Additional context about the document | No |
| **Expiry Date** | When the certification expires (if applicable) | No |

**Step 3: Assign a Certifier**

- Select a certifier from your organisation's approved signatories
- Or enter an external certifier's wallet address
- The certifier will receive a notification to review and sign

**Step 4: Review and Submit**

- Review all details
- Confirm the document hash matches your records
- Click "Create Request"
- The certification request is created with status "Pending Sign"

### What Happens Next

1. **Certifier receives notification** — They review the request in their dashboard
2. **Certifier signs** — They sign the certification using their Cardano wallet
3. **Blockchain anchoring** — The signed hash is submitted to the Cardano blockchain
4. **Confirmation** — Once confirmed (typically 20–60 seconds), the status changes to "Certified"
5. **Notification** — You and the subject receive confirmation

---

## 7. Managing Documents

### Document List

The Documents page shows all your organisation's documents with:

- **Search** — Find documents by title, subject, or hash
- **Filters** — Filter by status (Draft, Pending, Certified, Revoked), type, date range
- **Sort** — Sort by date, status, or title

### Document Statuses

| Status | Meaning | What to Do |
|--------|---------|------------|
| **Draft** | Document registered, awaiting certification | Assign a certifier |
| **Pending Sign** | Awaiting certifier's signature | Wait for certifier action |
| **Signed** | Certifier has signed | Automatic blockchain anchoring begins |
| **Anchoring** | Being recorded on blockchain | Wait for confirmation (20–60 seconds) |
| **Certified** | Successfully certified on blockchain | Share with subject or verifiers |
| **Revoked** | Certification cancelled | Terminal state — cannot be undone |
| **Expired** | Past expiry date | Re-certify if needed |

### Revoking a Certification

If a certification needs to be cancelled (e.g., issued in error, fraud discovered):

1. Navigate to the certified document
2. Click "Revoke Certification"
3. Enter the reason for revocation
4. Confirm the revocation
5. A revocation record is created on the blockchain

**Warning:** Revocation is permanent and recorded on the blockchain. It cannot be undone.

---

## 8. Document Lineage

Secuura provides an interactive visual timeline of every document's history:

- **Nodes** show each event (creation, signing, anchoring, verification)
- **Edges** connect events in chronological order
- **Colour coding** distinguishes event types (certification, verification, blockchain confirmation)
- **Click any node** to expand and view full details
- **Filter by date** to focus on specific time periods

The lineage view provides complete provenance — the full chain of custody from the moment a document was first certified to every subsequent verification, share, and transfer.

---

## 9. Sharing Certifications

Once a document is certified, you can share the certification with relevant parties:

### Share via Email

1. Open the certified document
2. Click "Share"
3. Enter the recipient's email address
4. Optional: Add a message
5. Click "Send"

The recipient receives an email with a verification link.

### Share via Link

1. Open the certified document
2. Click "Share" then "Copy Link"
3. Send the link via any channel (email, messaging, etc.)

### Share with the Subject

When the subject (the person the document is about) is notified:
- They receive a document ID and verification link
- They can share the certification with verifiers (e.g., employers)
- They control who can verify their documents

---

## 10. Wallet Integration

### Why Connect a Wallet?

A Cardano wallet provides:
- **Cryptographic signing** — Certifiers sign using their wallet, providing non-repudiable proof
- **Blockchain interaction** — Transactions are submitted from the certifier's wallet
- **Identity verification** — Wallet-based authentication via CIP-8 message signing

### Supported Wallets

| Wallet | Type | Supported |
|--------|------|-----------|
| Nami | Browser extension | Yes |
| Eternl | Browser extension | Yes |
| Lace | Browser extension | Yes |
| Flint | Browser extension | Yes |
| Typhon | Browser extension | Yes |
| GeroWallet | Browser extension | Yes |
| NuFi | Browser extension | Yes |

### Connecting Your Wallet

1. Navigate to the "Wallet" section in the portal
2. Click "Connect Wallet"
3. Select your wallet from the list
4. Approve the connection in the wallet popup
5. Your wallet is now linked to your Secuura account

---

## 11. NFT Certificates

### What Are NFT Certificates?

NFT Certificates allow you to save a certified document as a Non-Fungible Token (NFT) on the Cardano blockchain. This creates a permanent, transferable, on-chain record of the certification that lives in the certifier's or rights holder's Cardano wallet.

Unlike standard blockchain anchoring (which records only the hash), an NFT Certificate can include configurable metadata — document type, issuer, dates, and more — directly on-chain as a CIP-25 native asset.

### Why Use NFT Certificates?

| Standard Anchoring | NFT Certificate |
|---|---|
| Hash recorded on-chain | Full metadata as on-chain NFT |
| Not visible in wallet | Visible as an asset in any Cardano wallet |
| Cannot be transferred | Transferable between wallets |
| Requires Secuura to look up | Independently discoverable on-chain |
| No privacy controls | Configurable privacy levels |

### Prerequisites

1. A **certified or anchored** document (the "Save as NFT" button appears only for certified/anchored documents)
2. A **Cardano wallet** connected (Lace, Nami, Eternl, Flint, or any CIP-30 compatible wallet)
3. Sufficient **ADA balance** (approximately 1.5–3 ADA depending on storage tier)
4. Wallet set to **Cardano Preprod** network (for testing) or Mainnet (for production)

### Step-by-Step: Minting an NFT Certificate

**Step 1: Open the Certified Document**

1. Navigate to "Documents" in the sidebar
2. Open a document with "Certified" status or that has blockchain anchors
3. Click the **"Save as NFT"** button (primary colour, Token icon)

**Step 2: Connect Wallet**

The NFT minting modal opens with a 4-step wizard:

1. If your wallet is already connected, you will see a green checkmark with your wallet name, address, balance, and network
2. If not connected, click **"Connect Wallet"** and select your wallet from the list (e.g., Lace)
3. Approve the connection in the wallet extension popup
4. Click **"Continue"**

**Step 3: Select Storage Tier**

Choose how much data to store on-chain:

| Tier | Description | Cost | Best For |
|------|-------------|------|----------|
| **Basic** | Hash reference only | ~1.5 ADA | Maximum privacy, minimal footprint |
| **Standard** | Full metadata on-chain | ~2.0 ADA | Searchable and discoverable certificates |
| **Premium** | Full document on IPFS | ~2.5–3 ADA | Complete document ownership and portability |

Select your preferred tier and click **"Continue"**.

**Step 4: Configure Privacy**

Choose what information is publicly visible on the NFT:

| Privacy Level | Visible Fields |
|---|---|
| **Full Privacy** | Only certificate ID and document hash |
| **Minimal** | Document type and issue date |
| **Partial** | Document type, issuer, and issue date |
| **Verifiable** | All metadata fields visible |

You can also toggle **"Customize visible fields"** to select individual fields manually.

Click **"Continue"** to proceed to the review step.

**Step 5: Review and Mint**

1. Review the summary: wallet, network, storage tier, privacy level, estimated cost
2. Click **"Mint NFT"**
3. Your wallet will prompt you to sign the minting transaction — approve it
4. Wait for the transaction to be submitted to the blockchain (progress bar tracks each stage)
5. On success, you will see the transaction details: Tx Hash, Policy ID, Asset Name, and Asset ID

### After Minting

- The NFT appears as an asset in your Cardano wallet
- Click the **copy icon** next to the Tx Hash to copy it
- Click the **external link icon** to view the transaction on Cardanoscan
- The backend records the mint for platform tracking and on-chain verification via Blockfrost

### Supported Wallets for NFT Minting

| Wallet | Supported | Notes |
|--------|-----------|-------|
| Lace | Yes | Recommended — official IOG wallet |
| Nami | Yes | Lightweight and fast |
| Eternl | Yes | Full-featured with dApp browser |
| Flint | Yes | Mobile and desktop |
| Typhon | Yes | Advanced features |
| GeroWallet | Yes | Multi-chain support |
| NuFi | Yes | Staking and dApp support |

---

## 12. Analytics and Billing

### Analytics Dashboard

Track your certification activity:
- **Total certifications** issued
- **Verification rate** — How often your documents are verified
- **Certification volume trends** — Monthly and weekly charts
- **Top document types** — Most frequently certified categories

### Billing

Secuura uses an event-based pricing model. Key chargeable events:

| Event | Description |
|-------|-------------|
| **Certification issued** | When a document certification is created |
| **Certification signed** | When a certifier signs a certification |
| **Document shared** | When a certification is shared |
| **Certification revoked** | When a certification is cancelled |

Pricing is configurable and depends on your subscription tier.

---

## 13. Settings and Configuration

### Organisation Settings

- **Organisation name and details** — Update your organisation profile
- **Team members** — Add, remove, and manage team member roles
- **Document types** — Configure certifiable document types
- **Notification preferences** — Control email and in-app notifications

### Security Settings

- **Multi-factor authentication** — Enable TOTP-based MFA for added security
- **API keys** — Generate keys for programmatic access
- **Wallet management** — Connect, disconnect, or change wallets
- **Privacy preferences** — Control data sharing and processing

---

## 14. Frequently Asked Questions

**Q: Does Secuura store my documents?**  
A: No. Secuura computes a cryptographic hash (fingerprint) of your document in your browser. The original document never leaves your device. Only the hash is stored.

**Q: What happens if I lose the original document?**  
A: Secuura cannot recover original documents because they are never stored. However, the blockchain-anchored certification record remains permanent. If you have another copy of the document, it can be verified against the original hash.

**Q: Can a certification be modified after it is created?**  
A: No. Certifications are immutable once anchored to the blockchain. If changes are needed, the original must be revoked and a new certification created.

**Q: How long does blockchain confirmation take?**  
A: Typically 20–60 seconds on the Cardano mainnet.

**Q: What if the certifier is unavailable?**  
A: Certification requests remain pending until the assigned certifier acts. You can reassign to another approved signatory if needed.

**Q: Is there an API for bulk certifications?**  
A: Yes. Secuura provides a REST API for programmatic certification. Contact your administrator for API key setup.

**Q: How do verifiers access the certification?**  
A: Verifiers can use the public Secuura Verification Portal. They upload the document and receive an instant verification result. No Secuura account is needed for basic verification.

---

## 15. Support

- **Documentation:** docs.secuura.io
- **API Reference:** api.secuura.io/docs
- **Email Support:** support@secuura.io
- **Status Page:** status.secuura.io

---

_Copyright 2026 Secuura. All rights reserved._

---

**End of Document**
