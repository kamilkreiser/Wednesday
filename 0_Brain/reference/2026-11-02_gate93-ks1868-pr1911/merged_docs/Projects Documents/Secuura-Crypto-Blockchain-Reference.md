---
title: Secuura Crypto and Blockchain Developer Reference
created: 27-02-2026
updated: 27-02-2026
tags: [reference/blockchain, reference/crypto, reference/developer]
status: active
---

# Secuura Crypto and Blockchain Developer Reference

## Summary

This document is the single-source reference for all blockchain, cryptographic, and wallet configuration used across the Secuura Verification System (SVS). It is intended for any developer who needs to connect a related project to the same Cardano infrastructure, replicate the hashing and anchoring approach, or integrate with the same wallet and DID ecosystem.

**Key Points:**
- Secuura is built on Cardano (preprod default, mainnet for production)
- Document hashing is always performed client-side (Web Crypto API or BLAKE2b)
- Blockchain anchoring records document hashes, never document content
- NFT minting is performed client-side via MeshSDK; the backend records the result

---

## Table of Contents

- [Cardano Network Configuration](#cardano-network-configuration)
- [Environment Variables](#environment-variables)
- [Blockchain API Providers](#blockchain-api-providers)
- [Wallet Integration](#wallet-integration)
- [Document Hashing](#document-hashing)
- [Encryption](#encryption)
- [Blockchain Anchoring](#blockchain-anchoring)
- [NFT Certificate Minting](#nft-certificate-minting)
- [PRISM and DIDs](#prism-and-dids)
- [Verifiable Credentials](#verifiable-credentials)
- [Midnight ZK Proofs](#midnight-zk-proofs)
- [Staking and Governance](#staking-and-governance)
- [NPM Dependencies](#npm-dependencies)
- [Docker Profiles](#docker-profiles)
- [Source File Reference](#source-file-reference)

---

## Cardano Network Configuration

All network parameters are defined in `packages/shared/src/cardano/config.ts`.

| Network | Magic Number | Blockfrost URL | Koios URL | Explorer URL | Faucet |
|---------|-------------|----------------|-----------|--------------|--------|
| **devnet** | 42 | `http://localhost:6092` | `http://localhost:6092` | `http://localhost:6091` | N/A |
| **preview** | 2 | `https://cardano-preview.blockfrost.io/api/v0` | `https://preview.koios.rest/api/v1` | `https://preview.cardanoscan.io` | `https://faucet.preview.world.dev.cardano.org` |
| **preprod** | 1 | `https://cardano-preprod.blockfrost.io/api/v0` | `https://preprod.koios.rest/api/v1` | `https://preprod.cardanoscan.io` | `https://faucet.preprod.world.dev.cardano.org` |
| **mainnet** | 764824073 | `https://cardano-mainnet.blockfrost.io/api/v0` | `https://api.koios.rest/api/v1` | `https://cardanoscan.io` | N/A |

### Default Network

- **Local development:** `devnet` (Yaci DevKit) or `preprod`
- **Staging:** `preprod`
- **Production:** `mainnet`

The active network is controlled by the `CARDANO_NETWORK` environment variable on each service.

### Explorer URL Patterns

- Transaction: `{explorerUrl}/transaction/{txHash}`
- Address: `{explorerUrl}/address/{address}`

---

## Environment Variables

### Blockchain and Network

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `CARDANO_NETWORK` | anchoring, nft-certificate, prism, staking, wallet-connector | Yes | Active Cardano network | `preprod` |
| `BLOCKFROST_API_KEY` | anchoring, nft-certificate, prism, staking | Yes | Blockfrost project ID for the target network | `preprodXXXXXXXXXX` |
| `BLOCKFROST_URL` | anchoring | No | Override Blockfrost base URL | `https://cardano-preprod.blockfrost.io/api/v0` |
| `BLOCKFROST_PROJECT_ID` | shared/cardano | No | Alternative name for Blockfrost key | Same as above |
| `BLOCKFROST_PROJECT_ID_PREVIEW` | shared/cardano | No | Network-specific Blockfrost key | `previewXXXXXXXX` |
| `BLOCKFROST_PROJECT_ID_PREPROD` | shared/cardano | No | Network-specific Blockfrost key | `preprodXXXXXXXX` |
| `BLOCKFROST_PROJECT_ID_MAINNET` | shared/cardano | No | Network-specific Blockfrost key | `mainnetXXXXXXXX` |
| `KOIOS_API_KEY` | shared/cardano | No | Koios API key (optional, free tier available) | `your-koios-key` |
| `OGMIOS_HOST` | deployment/cardano | No | Ogmios WebSocket host | `localhost` |
| `OGMIOS_PORT` | deployment/cardano | No | Ogmios WebSocket port | `1337` |

### Wallet

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `PLATFORM_WALLET_MNEMONIC` | anchoring, nft-certificate | Yes (prod) | 24-word mnemonic for platform operations | `word1 word2 ... word24` |
| `WALLET_MNEMONIC` | anchoring | Yes (prod) | Alternative name for anchoring wallet mnemonic | Same as above |
| `MINTING_WALLET_MNEMONIC` | nft-certificate | Yes (prod) | Wallet mnemonic for NFT minting | `word1 word2 ... word24` |
| `PAYMENT_SIGNING_KEY` | anchoring | No | Alternative to mnemonic: raw signing key | Ed25519 key hex |
| `WALLETCONNECT_PROJECT_ID` | mobile app | No | WalletConnect v2 project ID | `abc123...` |

### PRISM and DIDs

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `PRISM_MODE` | prism | No | Operating mode | `mock`, `basic`, `testnet`, `mainnet` |
| `PRISM_NODE_URL` | prism | No | PRISM node endpoint | `http://localhost:50053` |
| `PRISM_NODE_API_KEY` | prism | No | PRISM node authentication key | `your-prism-key` |
| `PRISM_AGENT_URL` | prism | No | PRISM Cloud Agent URL | `http://localhost:8085` |
| `DID_METHOD` | prism | No | DID method identifier | `did:cardano` |
| `ISSUER_DID` | vc-issuer | Yes | Issuer DID for credential signing | `did:cardano:preview:issuer` |
| `ISSUER_PRIVATE_KEY` | vc-issuer | Yes (prod) | Private key for credential signing | Ed25519 key |

### Verifiable Credentials

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `VC_CONTEXT` | vc-issuer | No | W3C VC JSON-LD context | `https://www.w3.org/2018/credentials/v1` |
| `DEFAULT_EXPIRY_DAYS` | vc-issuer | No | Default credential expiry | `365` |

### Midnight (ZK Proofs)

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `MIDNIGHT_MODE` | midnight | No | Operating mode | `mock`, `testnet`, `mainnet` |
| `MIDNIGHT_NODE_URL` | midnight | No | Midnight node endpoint | URL |
| `MIDNIGHT_API_KEY` | midnight | No | Midnight API authentication | Key |
| `PROOF_EXPIRY_MINUTES` | midnight | No | ZK proof validity window | `60` |
| `MAX_DISCLOSED_FIELDS` | midnight | No | Maximum fields in selective disclosure | `10` |

### Staking

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `POOL_ID` | staking | Yes (prod) | Cardano stake pool ID | `pool1...` |
| `MIN_STAKE_LOVELACE` | staking | No | Minimum stake amount in lovelace | `100000000` (100 ADA) |
| `REWARD_PERCENTAGE` | staking | No | Annual reward percentage | `5` |
| `DISTRIBUTION_INTERVAL_DAYS` | staking | No | Reward distribution cycle | `5` |

### Anchoring

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `MIN_ADA_BALANCE` | anchoring | No | Minimum wallet balance (lovelace) | `5000000` (5 ADA) |
| `ANCHOR_FEE_LOVELACE` | anchoring | No | Fee per anchor transaction (lovelace) | `2000000` (2 ADA) |

### NFT and IPFS

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `POLICY_ID` | nft-certificate | No | Pre-existing NFT policy ID | Hex string |
| `POLICY_SCRIPT` | nft-certificate | No | Pre-existing policy script | JSON |
| `NFT_NAME_PREFIX` | nft-certificate | No | NFT asset name prefix | `SECUURA-CERT` |
| `IPFS_PROVIDER` | nft-certificate | No | IPFS provider selection | `mock`, `pinata`, `infura`, `web3storage` |
| `IPFS_GATEWAY` | nft-certificate | No | IPFS gateway URL | `https://gateway.pinata.cloud/ipfs` |
| `PINATA_API_KEY` | nft-certificate | No | Pinata IPFS API key | Key |
| `PINATA_SECRET_KEY` | nft-certificate | No | Pinata IPFS secret | Secret |
| `INFURA_PROJECT_ID` | nft-certificate | No | Infura IPFS project ID | ID |
| `INFURA_PROJECT_SECRET` | nft-certificate | No | Infura IPFS secret | Secret |
| `WEB3_STORAGE_TOKEN` | nft-certificate | No | Web3.Storage API token | Token |

### Timestamping

| Variable | Service(s) | Required | Description | Example |
|----------|-----------|----------|-------------|---------|
| `HASH_ALGORITHM` | timestamping | No | Hash algorithm for timestamps | `SHA256`, `blake2b-256` |
| `TSA_URL` | timestamping | No | RFC-3161 Time Stamping Authority URL | URL |
| `TSA_AUTH_KEY` | timestamping | No | TSA authentication key | Key |

---

## Blockchain API Providers

### Blockfrost

Primary Cardano data provider. Used for transaction submission, UTXO queries, and blockchain state.

- **SDK:** `@blockfrost/blockfrost-js@^6.1.0`
- **API version:** v0
- **Authentication:** Project ID passed as header (`project_id`)
- **Rate limits:** Depend on plan (free tier: 50k requests/day)
- **Usage:** Anchoring service, NFT service, wallet connector, staking

### Koios

Alternative/supplementary Cardano data provider. REST API with optional authentication.

- **API version:** v1
- **Authentication:** Optional API key (free tier available)
- **Usage:** Fallback provider, address queries, pool information

### Ogmios

WebSocket interface to a local Cardano node. Used in full-node deployments.

- **Default:** `localhost:1337`
- **Protocol:** WebSocket (JSON-RPC)
- **Usage:** Direct node communication when available

---

## Wallet Integration

### CIP-30 Browser Wallets

Secuura supports 8 Cardano browser wallets via the CIP-30 dApp connector standard:

| Wallet | Identifier | Status |
|--------|-----------|--------|
| Eternl | `eternl` | Supported |
| Nami | `nami` | Supported |
| Flint | `flint` | Supported |
| Lace | `lace` | Supported |
| Yoroi | `yoroi` | Supported |
| GeroWallet | `gerowallet` | Supported |
| NuFi | `nufi` | Supported |
| Typhon | `typhonwallet` | Supported |

**Implementation:** `services/wallet-connector/src/providers/cardano-cip30.provider.ts`

### MeshSDK (Client-Side)

Used for client-side NFT minting and transaction building in the issuer portal.

- **Package:** `@meshsdk/core@^1.9.0-beta.98`
- **Usage:** `frontend/issuer/src/utils/nftMinting.ts`
- **Capabilities:** Transaction building, UTXO management, native script creation, metadata attachment

### WalletConnect v2 (Mobile)

For mobile wallet connections using the WalletConnect protocol.

- **CIP-34 Chain IDs:**
  - Mainnet: `cip34:1-764824073`
  - Preprod: `cip34:0-1`
  - Preview: `cip34:0-2`
- **Implementation:** `mobile/secuura-app/src/contexts/WalletContext.tsx`

### Platform Wallet

Backend services that need to submit transactions (anchoring, NFT minting) use a platform wallet derived from a BIP-39 mnemonic.

- **Key derivation:** BIP-39 mnemonic to Ed25519 signing key
- **Package:** `bip39@^3.1.0`
- **Serialisation:** `@emurgo/cardano-serialization-lib-nodejs@^15.0.3`

---

## Document Hashing

### Principle

All document hashing MUST be performed client-side in the browser. Documents never leave the user's device. Only the resulting hash is transmitted to Secuura services.

### Client-Side (Browser)

```
Algorithm: SHA-256
API:       Web Crypto API (crypto.subtle.digest)
Format:    sha256:{hex}
```

Implementation in the verifier portal:

```typescript
const buffer = await file.arrayBuffer();
const hashBuffer = await crypto.subtle.digest('SHA-256', buffer);
const hashArray = Array.from(new Uint8Array(hashBuffer));
const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
return `sha256:${hashHex}`;
```

### Server-Side (Backend Services)

```
Primary:   BLAKE2b-256 (Cardano native, 32-byte digest)
Secondary: SHA-256 (compatibility)
Also:      BLAKE2b-512 (higher security requirements)
```

Implementation in `packages/shared/src/crypto/index.ts`:
- `blake2b256(data)` -- Primary document hash
- `sha256(data)` -- Compatibility hash
- `hashDocumentCertification(input)` -- Certification hash (BLAKE2b-256 of structured JSON)
- `hashCertificationEvent(input)` -- Provenance chain hash (BLAKE2b-256)

### Hash Format Convention

All hashes stored in the system use a prefixed format:
- `sha256:` followed by 64 hex characters
- `blake2b:` followed by 64 hex characters

---

## Encryption

### AES-256-GCM (Off-Chain Encrypted Data)

- **Algorithm:** AES-256-GCM
- **IV length:** 12 bytes
- **Auth tag length:** 16 bytes
- **Key size:** 32 bytes (256 bits)

### Key Derivation

- **Algorithm:** PBKDF2
- **Hash:** SHA-512
- **Iterations:** 100,000 (default)
- **Key length:** 32 bytes
- **Salt length:** 32 bytes

### Timing-Safe Comparison

All hash comparisons use `crypto.timingSafeEqual` to prevent timing attacks.

---

## Blockchain Anchoring

### How It Works

1. Document hash is generated client-side
2. Hash is submitted to the anchoring service
3. Anchoring service builds a Cardano transaction with the hash in metadata
4. Transaction is signed with the platform wallet
5. Transaction is submitted to the Cardano network via Blockfrost
6. Transaction hash and block height are recorded

### Configuration

| Parameter | Value | Description |
|-----------|-------|-------------|
| Anchor fee | 2,000,000 lovelace (2 ADA) | Cost per anchor transaction |
| Min balance | 5,000,000 lovelace (5 ADA) | Minimum wallet balance threshold |
| Network | Configurable via `CARDANO_NETWORK` | Target blockchain network |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/anchors` | Create a new anchor |
| `POST` | `/api/anchors/batch` | Batch anchor multiple hashes |
| `GET` | `/api/anchors/:id` | Get anchor status |
| `POST` | `/api/anchors/verify` | Verify an anchor on-chain |
| `POST` | `/api/anchoring/submit` | Submit signed transaction |
| `GET` | `/api/anchoring/status/:txHash` | Check transaction status |

### Fallback

When the Cardano network is unavailable, the anchoring service creates a **simulated anchor** with `simulated: true`. This allows the application to continue operating while marking the record for later on-chain confirmation.

---

## NFT Certificate Minting

### Architecture

NFT minting follows a **client-side mint** pattern:

1. Issuer portal builds the transaction using MeshSDK
2. User signs the transaction with their connected CIP-30 wallet
3. Transaction is submitted to the Cardano network
4. Backend records the mint result (policy ID, asset name, transaction hash)

### CIP-25 Compliance

All NFT metadata follows CIP-25 (NFT Metadata Standard):

```json
{
  "721": {
    "{policyId}": {
      "{assetName}": {
        "name": "SECUURA-CERT-{id}",
        "description": "Secuura Document Certificate",
        "image": "ipfs://{cid}",
        "documentHash": "sha256:{hash}",
        "certificationId": "{certId}",
        "issuedAt": "{timestamp}"
      }
    }
  }
}
```

### IPFS Storage

NFT metadata and optional document references are stored on IPFS:

| Provider | Configuration | Notes |
|----------|--------------|-------|
| Pinata | `PINATA_API_KEY`, `PINATA_SECRET_KEY` | Recommended for production |
| Infura | `INFURA_PROJECT_ID`, `INFURA_PROJECT_SECRET` | Alternative provider |
| Web3.Storage | `WEB3_STORAGE_TOKEN` | Decentralised option |
| Mock | `IPFS_PROVIDER=mock` | Development only |

Gateway URL: `https://gateway.pinata.cloud/ipfs/{cid}`

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/nft/record` | Record a client-side mint result |
| `POST` | `/api/nft/estimate` | Estimate minting cost |
| `GET` | `/api/nft/certificates` | List user's NFT certificates |
| `GET` | `/api/nft/certificates/:id` | Get NFT certificate details |
| `POST` | `/api/nft/verify` | Verify NFT authenticity |
| `POST` | `/api/nft/verify/ownership` | On-chain ownership verification |
| `GET` | `/api/nft/:policyId/:assetName/metadata` | Get on-chain NFT metadata |
| `GET` | `/api/nft/tiers` | Get storage tier options |
| `GET` | `/api/nft/privacy-options` | Get privacy options for minting |

---

## PRISM and DIDs

### Operating Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| `mock` | In-memory DID operations, no blockchain | Development |
| `basic` | Local DID creation/resolution with PostgreSQL | Staging |
| `testnet` | Full PRISM node on Cardano testnet | Pre-production |
| `mainnet` | Full PRISM node on Cardano mainnet | Production |

### DID Method

- **Method:** `did:cardano` (or `did:prism` when using PRISM Cloud Agent)
- **Resolution:** Local resolver with fallback to PRISM node

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/did/create` | Create a new DID |
| `GET` | `/api/did/:id` | Resolve a DID |
| `GET` | `/api/did/:id/document` | Get DID Document |

---

## Verifiable Credentials

### Standard

W3C Verifiable Credentials Data Model 1.1 with StatusList2021 for revocation.

### Configuration

| Parameter | Value |
|-----------|-------|
| VC Context | `https://www.w3.org/2018/credentials/v1` |
| Revocation | StatusList2021 |
| Default Expiry | 365 days |
| Signing | Ed25519 (issuer private key) |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/credentials` | Issue a verifiable credential |
| `GET` | `/api/credentials/:id` | Get credential by ID |
| `POST` | `/api/credentials/:id/revoke` | Revoke a credential |
| `POST` | `/api/credentials/verify` | Verify a credential |
| `GET` | `/api/status/:id` | Get revocation status list |
| `POST` | `/api/presentations` | Create a verifiable presentation |

---

## Midnight ZK Proofs

### Operating Modes

| Mode | Description |
|------|-------------|
| `mock` | Simulated proofs for development |
| `testnet` | Midnight testnet (when available) |
| `mainnet` | Midnight mainnet (future) |

### Circuit Types

| Circuit | Purpose |
|---------|---------|
| `circuit_ownership_v1` | Prove document ownership without revealing owner identity |
| `age_threshold` | Prove age is above a threshold without revealing date of birth |
| `range_proof` | Prove a value is within a range |
| `membership_proof` | Prove membership in a set without revealing which member |

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/proofs/generate` | Generate a ZK proof |
| `POST` | `/api/proofs/verify` | Verify a ZK proof |
| `GET` | `/api/circuits` | List available circuits |
| `POST` | `/api/commitments` | Create a commitment |
| `POST` | `/api/disclosure/proofs/age-threshold` | Age threshold proof |
| `POST` | `/api/disclosure/proofs/range` | Range proof |
| `POST` | `/api/disclosure/proofs/membership` | Membership proof |
| `POST` | `/api/private/documents/shield` | Shield document metadata |

---

## Staking and Governance

### Staking Parameters

| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| Min stake | 100,000,000 lovelace (100 ADA) | Minimum staking amount |
| Reward % | 5% | Annual reward percentage |
| Distribution | Every 5 days | Reward distribution interval |
| Pool ID | Configured per deployment | Cardano stake pool |

### Smart Contracts

Staking and revenue contracts are written in Aiken and located at `contracts/secuura/validators/`:

- `staking.ak` -- Staking validator
- `revenue.ak` -- Revenue distribution validator

### Governance Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/governance/state` | Current governance state |
| `GET` | `/api/governance/proposals` | List proposals |
| `POST` | `/api/governance/proposals` | Create a proposal |
| `POST` | `/api/governance/proposals/:id/vote` | Vote on a proposal |

---

## NPM Dependencies

### Blockchain and Crypto Packages

| Package | Version | Purpose |
|---------|---------|---------|
| `@blockfrost/blockfrost-js` | `^6.1.0` | Blockfrost SDK for Cardano queries |
| `@meshsdk/core` | `^1.9.0-beta.98` | Client-side Cardano transaction building |
| `@emurgo/cardano-serialization-lib-nodejs` | `^15.0.3` | Cardano data serialisation |
| `bip39` | `^3.1.0` | BIP-39 mnemonic generation and validation |
| `blake2` | `^4.0.2` | BLAKE2b hashing (Node.js native binding) |
| `crypto-browserify` | `^3.12.1` | Browser crypto polyfill |
| `buffer` | `^6.0.3` | Buffer polyfill for browser environments |

---

## Docker Profiles

### devnet Profile

Starts a local Cardano devnet using Yaci DevKit:

```bash
docker compose --profile devnet up -d
```

Services:
- **cardano-devnet** (Yaci DevKit): Ports 6091 (CLI), 6092 (Submit API), 6093 (Node)

### mock Profile

Starts a mock Cardano API (nginx returning static responses):

```bash
docker compose --profile mock up -d
```

Services:
- **cardano-mock**: Port 6090

### Default (No Profile)

All services connect to the configured `CARDANO_NETWORK` via Blockfrost. No local Cardano node required.

---

## Source File Reference

| File | Description |
|------|-------------|
| `packages/shared/src/cardano/config.ts` | Network configuration (magic numbers, URLs) |
| `packages/shared/src/cardano/blockfrost.ts` | Blockfrost client wrapper |
| `packages/shared/src/cardano/wallet.ts` | Wallet utilities (CIP-30, signing, key derivation) |
| `packages/shared/src/crypto/index.ts` | Hashing (BLAKE2b, SHA-256), encryption (AES-256-GCM), key derivation |
| `packages/shared/src/vc/builder.ts` | Verifiable Credential builder |
| `packages/shared/src/prism/mock-client.ts` | PRISM mock client (development) |
| `services/anchoring/src/cardano/provider.ts` | Anchoring provider (Blockfrost integration) |
| `services/anchoring/src/cardano/transaction.ts` | Transaction building for anchoring |
| `services/anchoring/src/cardano/wallet.ts` | Platform wallet management |
| `services/nft-certificate/src/cardano/mintPolicy.ts` | NFT minting policy script |
| `services/nft-certificate/src/cardano/mintTransaction.ts` | NFT mint transaction building |
| `services/nft-certificate/src/cardano/provider.ts` | NFT Blockfrost provider |
| `services/wallet-connector/src/providers/cardano-cip30.provider.ts` | CIP-30 wallet connector |
| `frontend/issuer/src/utils/nftMinting.ts` | Client-side NFT minting (MeshSDK) |
| `frontend/issuer/src/context/WalletContext.tsx` | Wallet connection context |
| `frontend/issuer/src/utils/hashing.ts` | Client-side document hashing |
| `frontend/verifier/src/components/VerifyPage.tsx` | Verifier client-side hashing |
| `contracts/secuura/validators/staking.ak` | Staking smart contract (Aiken) |
| `contracts/secuura/validators/revenue.ak` | Revenue distribution contract (Aiken) |
| `deployment/cardano/env.example` | Cardano deployment environment template |

---

## References

### Internal Links
- Secuura Architecture Reference
- Secuura Security Reference
- Secuura Mock Data Audit

### External Links
- [Blockfrost Documentation](https://docs.blockfrost.io/)
- [Koios API Documentation](https://api.koios.rest/)
- [CIP-30 dApp Connector](https://cips.cardano.org/cip/CIP-0030/)
- [CIP-25 NFT Metadata Standard](https://cips.cardano.org/cip/CIP-0025/)
- [MeshSDK Documentation](https://meshjs.dev/)
- [W3C Verifiable Credentials](https://www.w3.org/TR/vc-data-model/)
- [Aiken Smart Contract Language](https://aiken-lang.org/)
