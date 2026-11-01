# Secuura — Verifier Guide

**Instantly Verify Document Authenticity with Blockchain Proof**

**Document Title:** Verifier User Guide  
**Version:** 1.0  
**Date:** 15 February 2026  
**Classification:** External — Verifiers  
**Prepared by:** Secuura

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura | Initial verifier guide |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What is Secuura?](#2-what-is-secuura)
3. [Why Verify with Secuura?](#3-why-verify-with-secuura)
4. [How Verification Works](#4-how-verification-works)
5. [Verifying a Document — Step by Step](#5-verifying-a-document--step-by-step)
6. [Understanding Verification Results](#6-understanding-verification-results)
7. [API Integration for Programmatic Verification](#7-api-integration-for-programmatic-verification)
8. [Re-Certification (Verifier Becomes Certifier)](#8-re-certification-verifier-becomes-certifier)
9. [Pricing](#9-pricing)
10. [Frequently Asked Questions](#10-frequently-asked-questions)
11. [Support](#11-support)

---

## 1. Executive Summary

As a Verifier, you need to confirm that documents presented to you — degree certificates, employment references, professional qualifications, compliance certificates — are genuine and unaltered. Secuura enables you to do this instantly, without contacting the issuing organisation, by checking the document against its blockchain-anchored certification record.

**How it works in 30 seconds:**
1. Upload the document to the Secuura Verification Portal
2. Secuura computes a cryptographic fingerprint and checks it against the blockchain
3. You receive a definitive result: Verified, Failed, Revoked, or Expired

**No Secuura account required** for basic verification. Simply visit the Verification Portal and upload the document.

---

## 2. What is Secuura?

Secuura is a document authenticity platform built on the Cardano blockchain. Organisations use Secuura to certify their documents by recording a cryptographic fingerprint (hash) on the blockchain. This creates a permanent, tamper-proof record that anyone can check.

**The key principle:** If even a single character in a document has been changed since it was certified, the fingerprint will not match, and verification will fail. This makes it mathematically impossible to present a forged or altered document without detection.

**Your privacy is protected:** When you verify a document, Secuura computes the hash in your browser. The original document is never uploaded to or stored by Secuura's servers.

---

## 3. Why Verify with Secuura?

| Traditional Verification | Secuura Verification |
|--------------------------|---------------------|
| Contact the issuing organisation | Upload document to verification portal |
| Wait days or weeks for response | Receive result in seconds |
| Rely on verbal or email confirmation | Receive blockchain-backed proof |
| No way to detect subtle modifications | Any change detected cryptographically |
| Manual process for each document | Instant, automated, scalable |
| Verification may not be possible (issuer closed/unavailable) | Blockchain record is permanent |

### Who Uses Secuura Verification?

- **Employers** verifying candidate qualifications and references
- **Banks and financial institutions** verifying customer documents
- **Government agencies** confirming official documentation
- **Educational institutions** verifying transfer credentials
- **Compliance officers** confirming regulatory certificates
- **Procurement teams** verifying supplier certifications

---

## 4. How Verification Works

```
YOU HAVE A DOCUMENT TO VERIFY
        │
        ▼
┌─────────────────────────────────────┐
│  1. Upload to Secuura Verification  │
│     Portal (or use API)             │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  2. Hash computed IN YOUR BROWSER   │
│     (document never sent to server) │
└────────────────┬────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────┐
│  3. Hash compared against           │
│     blockchain-anchored record      │
└────────────────┬────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────┐      ┌──────────┐
   │ MATCH   │      │ MISMATCH │
   │         │      │          │
   │ Document│      │ Document │
   │ is      │      │ may be   │
   │ genuine │      │ altered  │
   └─────────┘      └──────────┘
```

### The Science Behind It

Secuura uses BLAKE2b-256, a cryptographic hash function that produces a unique 256-bit fingerprint for any input. The mathematical properties of this function guarantee:

- **Deterministic** — The same document always produces the same hash
- **Collision-resistant** — It is computationally infeasible to find two different documents that produce the same hash
- **Avalanche effect** — Even a single-bit change in the document produces a completely different hash
- **One-way** — The hash cannot be reversed to reconstruct the original document

---

## 5. Verifying a Document — Step by Step

### Method 1: File Upload (Recommended)

1. Navigate to the Secuura Verification Portal
2. Select the "Upload File" tab
3. Drag and drop the document you wish to verify, or click to browse
4. Supported formats: PDF, PNG, JPG, Word documents (up to 50MB)
5. The system automatically computes the hash and checks the blockchain
6. View the verification result

### Method 2: Document ID

If you have been given a Secuura Document ID (e.g., from a certificate or email):

1. Navigate to the Secuura Verification Portal
2. Select the "Enter ID" tab
3. Enter the document ID
4. Click "Verify"
5. View the certification details

### Method 3: QR Code

If the document contains a Secuura QR code:

1. Navigate to the Secuura Verification Portal
2. Select the "Scan QR" tab
3. Allow camera access when prompted
4. Point your camera at the QR code
5. View the verification result

### Method 4: Verification Link

If you received a verification link from the document subject or issuer:

1. Click the link
2. The verification page opens with pre-loaded certification details
3. Optionally upload the document for hash comparison
4. View the full verification result

---

## 6. Understanding Verification Results

### Verified (Authentic)

**What it means:** The document you provided matches the blockchain-anchored certification record. The document is genuine and has not been altered since certification.

**Information displayed:**
- Document title and type
- Certifier (organisation or individual who certified)
- Certification date and time
- Blockchain transaction reference
- Block number on Cardano
- Link to view on Cardano Explorer

### Verification Failed

**What it means:** The hash of the document you provided does not match any certification record. Possible reasons:

- The document has been modified (even minor formatting changes)
- A different version of the document was certified
- The document was never certified on Secuura

**What to do:**
1. Ensure you have the exact original document (not a scan, screenshot, or re-saved version)
2. Contact the document issuer to confirm the certified version
3. Request the certified version directly

### Revoked

**What it means:** The certification was valid but has been cancelled by the certifier. Possible reasons:

- Document was issued in error
- Fraudulent certification discovered
- Subject or issuer requested revocation

**What to do:**
1. Note the revocation date and reason (if provided)
2. Contact the issuer for clarification
3. Do not rely on a revoked certification

### Expired

**What it means:** The certification has passed its expiry date. The document was genuine at the time of certification, but the certification is no longer valid.

**What to do:**
1. Contact the issuer to request re-certification
2. Verify whether a renewed certification exists

### Not Found

**What it means:** No certification record exists for this document on the Secuura platform.

**Possible reasons:**
- The document was never certified on Secuura
- The document is certified on a different platform
- The document identifier is incorrect

---

## 7. API Integration for Programmatic Verification

For organisations that need to verify documents at scale, Secuura provides a REST API:

### Verify by Hash

```bash
POST /api/verification/verify
Content-Type: application/json

{
  "hash": "3a7bd3e8f1c2d4a5b6e7f8c9d0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f2c1"
}
```

### Verify by Document ID

```bash
POST /api/documents/:documentId/verify
```

### Response Format

```json
{
  "verified": true,
  "documentId": "doc-1234567890-abc123",
  "checks": {
    "exists": true,
    "notRevoked": true,
    "hashValid": true,
    "hasSignatures": true,
    "blockchainAnchored": true
  },
  "issuer": {
    "id": "test-issuer",
    "verified": true
  },
  "blockchain": {
    "txHash": "tx_8f3a2b...",
    "blockHeight": 1988708,
    "confirmedAt": "2026-01-15T14:32:00Z"
  },
  "verifiedAt": "2026-02-16T06:15:00Z"
}
```

> **Note:** The previous response format with `certification` wrapper has been replaced with the flat format shown above.

### Legacy Response Format (deprecated)

```json
{
  "verified": true,
  "certification": {
    "id": "doc_abc123",
    "title": "Degree Certificate",
    "certifier": "University of Example",
    "certifiedAt": "2026-01-15T14:32:00Z",
    "transactionHash": "8f3a2b...",
    "blockNumber": 12345678,
    "status": "certified"
  }
}
```

### SDK Integration

```javascript
import { SecuuraClient } from '@secuura/sdk';

const client = new SecuuraClient({
  apiKey: process.env.SECUURA_API_KEY,
  network: 'mainnet',
});

// Verify by hash
const result = await client.verify({ hash: documentHash });
console.log(result.verified); // true or false
```

Contact your Secuura account manager or administrator for API key provisioning.

---

## 8. Re-Certification (Verifier Becomes Certifier)

In Secuura's SVS (Secure Verification Service), a successful verification can lead to re-certification — a process where the Verifier becomes a Certifier in a new phase of the document's lifecycle.

**Example:** An employer verifies a candidate's degree. The employer can then issue their own certification — effectively saying "We have verified this qualification and confirm its authenticity."

This creates a cascading chain of trust:

```
University (Original Certifier)
  └── Degree Certified ─► Blockchain Record
        │
        ▼
Employer (Verifier → New Certifier)
  └── Verification Certificate ─► Blockchain Record
        │
        ▼
Regulatory Body (Verifier → New Certifier)
  └── Compliance Confirmation ─► Blockchain Record
```

Each layer adds additional trust, and the entire chain is visible in the Document Lineage view.

---

## 9. Pricing

Verification may be a chargeable event depending on the deployment configuration:

| Tier | Included Verifications | Additional Cost |
|------|------------------------|-----------------|
| **Basic** | 100/month | Per-verification pricing |
| **Standard** | 500/month | Discounted per-verification |
| **Premium** | 2,000/month | Further discounted |
| **Enterprise** | Unlimited | Custom pricing |

Public verification (basic check without account) may be available depending on the issuer's configuration.

---

## 10. Frequently Asked Questions

**Q: Do I need a Secuura account to verify a document?**  
A: Basic verification via the public portal does not require an account. For API access, bulk verification, or re-certification, an account is needed.

**Q: Is my document uploaded to Secuura when I verify it?**  
A: No. The document is hashed in your browser. The original file never leaves your device. Only the computed hash is sent to check against the blockchain record.

**Q: What if verification fails but I believe the document is genuine?**  
A: Even minor changes (re-saving a PDF, re-scanning, format conversion) can change the hash. Ensure you have the exact file that was originally certified. Contact the issuer if unsure.

**Q: Can I verify documents from multiple issuers?**  
A: Yes. Secuura supports verification of any document certified on the platform, regardless of which organisation issued it.

**Q: How do I know the blockchain record itself is trustworthy?**  
A: Cardano is a decentralised blockchain maintained by thousands of independent nodes worldwide. No single party (including Secuura) can alter, delete, or backdate records on the blockchain.

**Q: What if Secuura ceases operations?**  
A: The blockchain records are permanent and publicly accessible. Even without Secuura's portal, the certification hashes can be verified directly on the Cardano blockchain using any Cardano explorer.

---

## 11. Support

- **Verification Portal:** verify.secuura.io
- **Documentation:** docs.secuura.io
- **API Reference:** api.secuura.io/docs
- **Email Support:** support@secuura.io
- **Status Page:** status.secuura.io

---

_Copyright 2026 Secuura. All rights reserved._

---

**End of Document**
