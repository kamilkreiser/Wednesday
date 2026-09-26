KS-1074 The poller/reconcile blob writers also erase threadToken — on the CONFIRM/heal path, not just the failure path #936 fixes
state In Progress

## BLUF

**The threadToken erasure KS-1058 fixed in** `markDocumentAnchorFailed` **is NOT the only writer that drops it. Every blob-rebuild writer in** `anchorStateSync.ts` **rebuilds** `blockchain: {...}` **as a literal with NO** `threadToken` **— including the CONFIRM and heal-to-confirmed paths.** So a document that mints a thread token at create and then anchors successfully has its `threadToken` cache erased on the success path, not just the failure path. Read from source, NOT runtime-measured.

## Mechanism (source, on develop `d4cf7e3cf`)

`updateDocument` replaces the `blockchain` column wholesale (`repositories/documentRepo.ts:480`, shallow top-level spread — established by KS-1058). Any writer that provides a fresh `blockchain` object therefore drops every field it does not re-list. The `anchorStateSync.ts` writers rebuild the blob from scratch with no `...existing` spread:

* `markDocumentAnchorFailed` **(:140)** — failure writer. **Fixed by #936 (KS-1058).**
* **poller confirm-writer (~:191)** — `blockchain: { txHash, blockHeight, anchoredAt, network, status, anchorId }` — no threadToken.
* **poller simulated-declaration writer (~:226)** — no threadToken.
* **reconcile heal-to-confirmed (~:299)** — `status: 'confirmed'` — no threadToken.
* **reconcile heal-to-simulated (~:327)** — no threadToken.

The confirm-writers are arguably the more serious of the set: they run on the **success** path, so a document that anchors normally loses the token cache that dashboards read (`state_thread_registry` is the canonical truth, but the whole point of the blob field per KS-1058 is to avoid that lookup).

## Why the type does not catch this

KS-1068 declared `threadToken?` as OPTIONAL (it is legitimately absent on many blobs), so a writer that omits it still compiles. The type makes the drop **visible to a reader**, not compile-fatal. Catching it needs either a spread-preserve pattern (as #936 applied to the failure writer) or a test per writer.

## Scope (behaviour — deliberately NOT KS-1068, which was type-only)

Decide, per writer, whether it should carry `threadToken` (and `simulatedTxRef`) forward — then either spread the prior blob or re-fetch the token from `state_thread_registry`. Same shape as KS-1058; extend that fix to the confirm/heal writers. **Verify at runtime first** — this ticket is a source read; a boot repro (mint → anchor → confirm, then read `document.blockchain.threadToken`) should confirm the erasure before the fix.

## Provenance

Surfaced by the KS-1068 writer re-check (scope item 3), 2026-09-10, read from source on develop `d4cf7e3cf`. Not runtime-measured. Sibling of KS-1058 (one instance fixed) and KS-1068 (the type hole).
