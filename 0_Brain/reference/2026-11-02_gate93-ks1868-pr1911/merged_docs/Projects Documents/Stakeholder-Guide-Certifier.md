# Secuura — Certifier Guide

**Sign and Certify Documents with Your Cardano Wallet**

**Document Title:** Certifier User Guide  
**Version:** 1.0  
**Date:** 15 February 2026  
**Classification:** External — Certifiers  
**Prepared by:** Secuura

---

## Version History

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 15 Feb 2026 | Secuura | Initial certifier guide |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [What is a Certifier?](#2-what-is-a-certifier)
3. [Getting Started](#3-getting-started)
4. [Wallet Setup](#4-wallet-setup)
5. [Certification Workflow](#5-certification-workflow)
6. [Signing a Certification](#6-signing-a-certification)
7. [Reviewing Requests](#7-reviewing-requests)
8. [Revoking Certifications](#8-revoking-certifications)
9. [Security Best Practices](#9-security-best-practices)
10. [Frequently Asked Questions](#10-frequently-asked-questions)
11. [Support](#11-support)

---

## 1. Executive Summary

As a Certifier, you hold a position of trust. You are the authorised signatory who attests to the authenticity of documents. When you sign a certification on Secuura, you are creating a permanent, blockchain-anchored record that this document is genuine and was legitimately issued by your organisation.

Your certification cannot be altered, backdated, or deleted. It carries the weight of a public, immutable record on the Cardano blockchain, linked to your wallet address.

**Your responsibilities:**
- Review certification requests carefully before signing
- Verify that the document hash matches the original document
- Sign only documents you are authorised to certify
- Protect your wallet credentials (seed phrase and password)
- Revoke certifications promptly if errors are discovered

---

## 2. What is a Certifier?

A Certifier is an individual or entity authorised to attest to a document's authenticity. In practice, certifiers are typically:

| Role | Example |
|------|---------|
| University dean | Certifying degree certificates |
| Company executive | Certifying employment references and official letters |
| Notary public | Certifying legal documents |
| Quality assurance officer | Certifying product compliance certificates |
| Government official | Certifying official documentation |

**Key principle:** A Certifier's signature is non-repudiable. Once you sign a certification, the blockchain record permanently associates your wallet address with the certification. This is by design — it creates an unbreakable chain of trust from the certifier to the document.

---

## 3. Getting Started

### Prerequisites

1. A Secuura account with Issuer Approver or equivalent role
2. A supported Cardano wallet browser extension
3. ADA tokens for transaction fees (mainnet) or test ADA (testnet)

### Initial Setup

1. Log in to the Secuura Issuer Portal
2. Navigate to "Wallet" and connect your Cardano wallet
3. Ensure your wallet has sufficient ADA for transaction fees
4. You are ready to receive and sign certification requests

---

## 4. Wallet Setup

### Supported Wallets

| Wallet | Installation | Recommended For |
|--------|-------------|-----------------|
| **Nami** | Chrome/Brave extension | Simple, lightweight usage |
| **Eternl** | Chrome/Brave extension | Advanced features, multi-account |
| **Lace** | Chrome/Brave extension | Modern interface, IOG-developed |
| **Flint** | Chrome/Brave extension | Mobile and desktop |
| **Typhon** | Chrome/Brave extension | Advanced transaction building |
| **GeroWallet** | Chrome/Brave extension | DeFi-oriented |
| **NuFi** | Chrome/Brave extension | Staking-focused |

### Installation Steps

1. Install your chosen wallet from the browser extension store
2. Create a new wallet or restore from an existing seed phrase
3. **Securely store your seed phrase** — write it down on paper and store in a secure location. Never store digitally.
4. Set a strong wallet password
5. Note your wallet address for registration

### Funding Your Wallet

**For Mainnet:**
1. Purchase ADA from a cryptocurrency exchange
2. Transfer ADA to your wallet address
3. Recommended minimum: 50 ADA for transaction fees

**For Testnet (Preview/Preprod):**
1. Visit the Cardano faucet for your network
2. Enter your wallet address
3. Receive test ADA (free)

### Connecting to Secuura

1. Navigate to "Wallet" in the Secuura portal
2. Click "Connect Wallet"
3. Select your wallet from the list
4. Approve the connection request in your wallet popup
5. Your wallet address is now linked to your Secuura account

---

## 5. Certification Workflow

### The Certification Process

```
ISSUER creates certification request
        │
        ▼
YOU receive notification
        │
        ▼
YOU review the request
  - Check document metadata
  - Verify document hash (optional but recommended)
  - Confirm you are authorised to certify
        │
        ├── APPROVE ──────────────────────┐
        │                                  │
        └── REJECT (with reason) ──┐      │
                                    │      ▼
                                    │  YOU sign with wallet
                                    │      │
                                    │      ▼
                                    │  Hash anchored to blockchain
                                    │      │
                                    │      ▼
                              Ends  │  CERTIFICATION CONFIRMED
                                    │  (immutable blockchain record)
                                    ▼
                              Request returned to issuer
```

---

## 6. Signing a Certification

### Step-by-Step

**Step 1: Review the Request**

You will see:
- Document title and type
- Subject name (who the document is about)
- Issuer (who created the request)
- Document hash (BLAKE2b-256 fingerprint)
- Description and metadata
- Any attached notes from the issuer

**Step 2: Verify the Hash (Recommended)**

If you have access to the original document, verify the hash matches:
- The hash displayed in the request should match the hash of the document you have
- This confirms the certification request is for the correct, unmodified document

**Step 3: Sign the Certification**

1. Click "Sign & Certify"
2. Your Cardano wallet popup appears
3. Review the transaction details in your wallet
4. Enter your wallet password
5. Click "Confirm" in your wallet

**Step 4: Wait for Confirmation**

- The transaction is submitted to the Cardano blockchain
- Confirmation typically takes 20–60 seconds
- Once confirmed, the certification status changes to "Certified"
- The issuer and subject are notified

**Important:** By signing, you are creating a permanent, public record that you certify this document as authentic. Ensure you are authorised and confident before signing.

---

## 7. Reviewing Requests

### Dashboard View

Your dashboard shows:
- **Pending requests** — Certification requests awaiting your signature
- **Recently signed** — Certifications you have recently completed
- **Request count** — Number of pending requests

### Reviewing Details

For each request, review:

| Field | What to Check |
|-------|--------------|
| **Document title** | Matches the document you are certifying |
| **Document type** | Correct classification |
| **Subject** | Correct individual or entity |
| **Issuer** | Request from an authorised member of your organisation |
| **Hash** | Matches your copy of the original document |
| **Description** | Accurate and complete |

### Rejecting a Request

If a certification request is incorrect or you are not authorised to sign:

1. Click "Reject"
2. Enter the reason for rejection
3. The request is returned to the issuer with your feedback

---

## 8. Revoking Certifications

### When to Revoke

- Document was issued in error
- Fraudulent certification discovered
- Subject or issuer requests revocation
- Organisational policy requires revocation
- Document has been superseded by a corrected version

### How to Revoke

1. Navigate to the certified document
2. Click "Revoke Certification"
3. Enter the reason for revocation
4. Sign the revocation transaction with your wallet
5. The certification status changes to "Revoked"

### Important Notes

- **Revocation is permanent** — It cannot be undone
- **Revocation is public** — The revocation record is on the blockchain
- **Original certification remains visible** — The history shows both the original certification and the revocation, preserving the audit trail
- **Verifiers are protected** — Anyone who verifies the document after revocation will see the "Revoked" status

---

## 9. Security Best Practices

### Wallet Security

| Practice | Why It Matters |
|----------|---------------|
| **Never share your seed phrase** | Anyone with your seed phrase controls your wallet and can sign certifications in your name |
| **Store seed phrase offline** | Write on paper; store in a safe. Never in a file, email, or cloud storage |
| **Use a strong wallet password** | Protects against local access to your device |
| **Consider a hardware wallet** | Ledger or Trezor provide the highest security for mainnet operations |
| **Keep wallet balance low** | Only hold the ADA needed for transaction fees |

### Certification Security

| Practice | Why It Matters |
|----------|---------------|
| **Verify document hash** | Confirms you are certifying the correct document |
| **Review all metadata** | Ensures accuracy of the permanent record |
| **Only sign if authorised** | Your signature carries legal and professional weight |
| **Reject suspicious requests** | Report any unusual or unexpected certification requests |
| **Monitor your certification history** | Review recent activity for any unauthorised certifications |

### Account Security

| Practice | Why It Matters |
|----------|---------------|
| **Enable MFA** | Protects your Secuura account from unauthorised access |
| **Use strong passwords** | Prevents credential-based attacks |
| **Log out when finished** | Prevents session hijacking on shared devices |
| **Review connected wallets** | Ensure only your wallet is connected |

---

## 10. Frequently Asked Questions

**Q: Can I sign certifications from multiple devices?**  
A: Yes, as long as you have your wallet extension installed and connected on each device. Your wallet credentials (seed phrase) can be used to restore the wallet on multiple devices.

**Q: What happens if I lose access to my wallet?**  
A: If you have your seed phrase, you can restore your wallet on a new device. If you have lost your seed phrase, you will need to create a new wallet and link it to your Secuura account. Previous certifications remain valid — they are linked to your old wallet address.

**Q: How much ADA do I need for certifications?**  
A: Each certification transaction costs approximately 0.17–0.25 ADA in network fees. We recommend maintaining at least 50 ADA for comfortable ongoing operations.

**Q: Can I delegate my certification authority?**  
A: Within Secuura, your organisation admin can assign the Issuer Approver role to other team members. Each person should use their own wallet — never share wallet access.

**Q: What if I sign the wrong document?**  
A: Contact your organisation admin immediately. The certification can be revoked, but the revocation and original certification will both remain visible on the blockchain audit trail.

---

## 11. Support

- **Documentation:** docs.secuura.io
- **Email Support:** support@secuura.io
- **Status Page:** status.secuura.io

---

_Copyright 2026 Secuura. All rights reserved._

---

**End of Document**
