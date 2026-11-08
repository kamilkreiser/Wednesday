# @secuura/sdk

Official JavaScript/TypeScript SDK for the Secuura blockchain certification platform.

## Installation

```bash
npm install @secuura/sdk
# or
yarn add @secuura/sdk
# or
pnpm add @secuura/sdk
```

## Quick Start

```typescript
import { SecuuraClient } from '@secuura/sdk';

// Initialize with API key
const client = new SecuuraClient({
  apiKey: 'your-api-key',
  baseUrl: 'https://api.secuura.io', // Optional, defaults to production
});

// Or with access token
const client = new SecuuraClient({
  accessToken: 'your-jwt-token',
});
```

## Usage

### Certifications

```typescript
// Issue a certification
const certification = await client.certifications.issue({
  type: 'educational_degree',
  holderId: 'holder-uuid',
  title: 'Bachelor of Science in Computer Science',
  data: {
    institution: 'Test University',
    graduationDate: '2024-06-15',
    gpa: '3.8',
  },
  expiresAt: '2029-06-15T00:00:00Z',
});

// List certifications
const { data, pagination } = await client.certifications.list({
  type: 'educational_degree',
  status: 'issued',
  limit: 20,
});

// Verify a certification
const verification = await client.certifications.verify(certificationId);
console.log(verification.verified); // true
console.log(verification.blockchain.anchored); // true

// Revoke a certification
await client.certifications.revoke(certificationId, 'Credential expired');
```

### Governance

```typescript
// Get governance state
const state = await client.governance.getState();
console.log(state.activeProposals);

// Create a proposal
const proposal = await client.governance.createProposal({
  title: 'Reduce platform fees',
  description: 'Proposal to reduce transaction fees from 2% to 1.5%',
  category: 'platform_fees',
  votingPeriodDays: 7,
  actions: [
    { type: 'update_fee', parameters: { newFeePercent: 1.5 } },
  ],
});

// Vote on a proposal
const result = await client.governance.vote(proposalId, {
  vote: 'for',
  reason: 'I support lower fees',
});
console.log(result.voteWeight);

// Execute a passed proposal
await client.governance.executeProposal(proposalId);
```

### Privacy & ZKP

```typescript
// Get privacy preferences
const prefs = await client.privacy.getPreferences();

// Update preferences
await client.privacy.updatePreferences({
  defaultVisibility: 'authenticated',
  allowZkpVerification: true,
});

// Generate a zero-knowledge proof
const proof = await client.privacy.generateProof({
  documentId: certificationId,
  fieldsToDisclose: ['institution', 'graduationDate'],
  fieldsToProve: [
    { field: 'gpa', operator: 'greaterThan', value: 3.0 },
  ],
  verifierDid: 'did:cardano:verifier...',
  purpose: 'Employment verification',
  expiresIn: 3600,
});

// Verify a proof
const verification = await client.privacy.verifyProof(
  proof.proofId,
  proof.proof
);
console.log(verification.valid); // true
console.log(verification.provenClaims[0].satisfied); // true
```

### Transfers & Delegations

```typescript
// Initiate a transfer
const transfer = await client.transfers.initiate({
  documentId: certificationId,
  toUserId: recipientId,
  reason: 'Company acquisition',
  requiresApproval: true,
});

// Approve a transfer
await client.transfers.approve(transferId, 'approve', {
  comment: 'Approved for transfer',
});

// Create a delegation
const delegation = await client.transfers.createDelegation({
  delegateId: delegateUserId,
  type: 'view',
  scope: ['certifications'],
  expiresAt: '2025-01-01T00:00:00Z',
});

// Revoke a delegation
await client.transfers.revokeDelegation(delegationId, 'No longer needed');
```

### KYC Verification

```typescript
// Start KYC verification
const session = await client.kyc.startVerification({
  verificationType: 'standard',
  credentialType: 'VerifiedIdentity',
  includeFaceCheck: true,
  purpose: 'Account verification',
});

console.log(session.qrCodeUrl); // Display QR code to user

// Wait for completion
const result = await client.kyc.waitForCompletion(session.sessionId, {
  timeoutMs: 300000,
  onStatusChange: (status) => {
    console.log('KYC status:', status);
  },
});

if (result.status === 'completed') {
  console.log('Verified!', result.verifiedCredentials);
}
```

### Webhooks

```typescript
// Create a webhook
const webhook = await client.webhooks.create({
  url: 'https://your-app.com/webhooks/secuura',
  events: [
    'certification.issued',
    'certification.revoked',
    'governance.proposal_passed',
  ],
});

console.log(webhook.secret); // Store this securely

// Handle webhooks in your Express app
import { createWebhookHandler, WebhooksModule } from '@secuura/sdk';

app.post('/webhooks/secuura', createWebhookHandler({
  secret: process.env.SECUURA_WEBHOOK_SECRET,
  handlers: {
    'certification.issued': async (event) => {
      console.log('New certification:', event.data);
    },
    'governance.proposal_passed': async (event) => {
      console.log('Proposal passed:', event.data);
    },
  },
  onError: (error) => {
    console.error('Webhook error:', error);
  },
}));

// Or manually verify signatures
const isValid = WebhooksModule.verifySignature(
  requestBody,
  request.headers['x-secuura-signature'],
  webhookSecret
);
```

## Error Handling

```typescript
import { SecuuraError } from '@secuura/sdk';

try {
  await client.certifications.get('invalid-id');
} catch (error) {
  if (error instanceof SecuuraError) {
    console.log(error.code);      // 'NOT_FOUND'
    console.log(error.statusCode); // 404
    console.log(error.message);    // 'Certification not found'
    console.log(error.details);    // Additional error details
  }
}
```

## Configuration Options

```typescript
const client = new SecuuraClient({
  // Authentication (one required)
  apiKey: 'your-api-key',
  accessToken: 'your-jwt-token',
  
  // API endpoint (optional)
  baseUrl: 'https://api.secuura.io',
  
  // Request timeout in ms (optional, default: 30000)
  timeout: 30000,
  
  // Enable debug logging (optional)
  debug: true,
  
  // Callback for token refresh (optional)
  onTokenRefresh: (newToken) => {
    // Store the new token
  },
});
```

## TypeScript Support

The SDK is written in TypeScript and includes full type definitions.

```typescript
import type {
  Certification,
  Proposal,
  PrivacyPreferences,
  WebhookEvent,
} from '@secuura/sdk';
```

## Browser Support

The SDK works in both Node.js and browser environments. For browsers, ensure you have appropriate CORS configuration on your API.

## License

MIT
