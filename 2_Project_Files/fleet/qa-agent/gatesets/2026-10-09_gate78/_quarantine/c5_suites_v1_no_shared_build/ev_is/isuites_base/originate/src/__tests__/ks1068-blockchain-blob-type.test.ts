/**
 * =============================================================================
 * KS-1068 — the `blockchain` blob type declares every shape the code writes
 * =============================================================================
 * `threadToken`, `confidence` and `simulatedTxRef` were written onto the
 * document `blockchain` blob with `as any` and were ABSENT from its declared
 * interface (`DocumentRecord['blockchain']`). Because they were undeclared, a
 * writer that rebuilt the blob and dropped one produced no compiler error, no
 * test failure and no reviewer signal — which is the mechanism KS-1058 fixed
 * one instance of.
 *
 * This is a COMPILE-TIME contract test. Its assertions are type-level: each
 * `const _x: DocumentRecord['blockchain'] = {...}` is a real shape the product
 * writes (verified against the write sites named in each case). If the
 * interface is re-narrowed — a field removed, or `txHash`/`blockHeight` made
 * required again — this file stops compiling, and ts-jest / the service build
 * (`tsc`, which includes `__tests__`) go red. The runtime `expect`s exist only
 * so jest has a spec to execute; the guard is the compiler accepting the file.
 *
 * It does NOT assert any writer preserves these fields on rebuild — that is a
 * behaviour decision (KS-1058 for the failure writer; the confirm/heal writers
 * are tracked separately). This ticket makes the shapes expressible, no more.
 * =============================================================================
 */

import type { DocumentRecord } from '../repositories/documentRepo';

type Blob = NonNullable<DocumentRecord['blockchain']>;

describe('KS-1068 — blockchain blob interface accepts every written shape', () => {
  it('accepts a threadToken-only blob (minted at document-create, before any anchor)', () => {
    // Write site: routes/documents.ts — the mint `.then`, which spreads
    // `document.blockchain || {}` (so on a not-yet-anchored doc the blob is
    // just the token cache: no txHash, no blockHeight).
    const threadTokenOnly: Blob = {
      threadToken: {
        policyId: 'p',
        scriptAddress: 'addr',
        // KS: StateThreadRegistryEntry.mintTxHash is `string | null` — a token
        // minted but not yet confirmed on chain.
        mintTxHash: null,
        network: 'preview',
      },
    };
    expect(threadTokenOnly.threadToken?.policyId).toBe('p');
    expect(threadTokenOnly.txHash).toBeUndefined();
  });

  it('accepts the pending-onchain blob (dev-mode fallback: null chain fields + confidence)', () => {
    // Write site: routes/documents.ts retry path — the `catch` arm.
    const pendingOnchain: Blob = {
      txHash: null,
      blockHeight: null,
      anchoredAt: null,
      confidence: 'pending-onchain',
    };
    expect(pendingOnchain.confidence).toBe('pending-onchain');
    expect(pendingOnchain.blockHeight).toBeNull();
  });

  it('accepts a confirmed anchor blob and a simulated-declaration blob', () => {
    const confirmed: Blob = {
      txHash: 'a'.repeat(64),
      blockHeight: 12345,
      anchoredAt: new Date().toISOString(),
      network: 'preview',
      status: 'confirmed',
      anchorId: 'anc_1',
    };
    // Write site: anchorStateSync.ts / documents.ts — KS-587 declared-simulated.
    const simulated: Blob = {
      txHash: null,
      blockHeight: 0,
      status: 'submitted',
      simulated: true,
      simulatedTxRef: 'mock_tx_deadbeef',
    };
    expect(confirmed.status).toBe('confirmed');
    expect(simulated.simulated).toBe(true);
    expect(simulated.simulatedTxRef).toBe('mock_tx_deadbeef');
  });
});
