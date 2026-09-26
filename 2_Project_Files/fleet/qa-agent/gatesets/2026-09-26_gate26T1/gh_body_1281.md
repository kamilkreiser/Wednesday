#1281 KS-1074: carry threadToken forward through every anchor rebuild writer
head c3374e3129ccaca29a9beeafe2d0098ffc86796d

## What

`updateDocument` replaces the `blockchain` column **wholesale** — measured at source, not taken from the comment: `documentRepo.ts` builds `const updated = { ...doc, ...updates }`, a **top-level** spread, so `updates.blockchain` replaces `doc.blockchain` entirely and every key not restated is destroyed.

KS-1058 fixed exactly **one** writer, the failure path. **Four more** rebuild the blob as a literal with no `threadToken`, and **two of those are on the SUCCESS path** — so a document that mints a thread token at create and then anchors *normally* lost the cache dashboards read. `state_thread_registry` stays the canonical truth; the blob field exists to avoid that lookup, which is the whole point of KS-1058.

| writer | path | before |
|---|---|---|
| `anchorStateSync.ts:182` (`markDocumentAnchorFailed`) | failure, fail-closed | carried it, but by a **truthy** guard |
| `:229` poller, real txHash | **SUCCESS** | erased |
| `:266` poller, simulated declaration | success | erased |
| `:346` reconcile, heal-to-confirmed | success | erased |
| `:382` reconcile, heal-to-simulated | success | erased |

The ticket's line numbers (`~:191 ~:226 ~:299 ~:327`) are stale; the above are at `d7cdecf1d2ee`. The ticket also cites `documentRepo.ts:480` for the shallow spread — at this base it is `:541`.

## The repro came first, as the ticket requires

**Against the unfixed code, 6 of the 8 cells are RED**, and the two that pass are the two that should: the fail-closed writer (already fixed by KS-1058) and the cell asserting an absent token is not invented. That is the erasure *measured* before the fix rather than argued from the source — which is what this ticket asks for ("Verify at runtime first — this ticket is a source read").

## Three decisions this ticket asks for, each asserted by a cell rather than left to a reader

1. **`!= null`, not truthiness** (the MINOR-2 item). `threadToken` is typed `unknown`, so an empty string or `0` would be discarded by the very write that exists to stop a value being lost. Theoretical for a real hex token, and exactly what a rewrite reintroduces — so it is pinned, and a red arm reverts the guard to truthiness and reddens only that cell.
2. **Carried explicitly, never by spreading `prior`.** A blanket spread would also carry `anchoredAt`, which the blob's own contract says is *"Absent in the KS-520 fail-closed state — nothing was anchored"*. That reasoning is KS-1058's and is preserved.
3. **`simulatedTxRef` is NOT carried.** The two simulated writers already spread `...simFields`, reconstructed from the anchor being read, so nothing needs inheriting; and carrying a simulated marker onto a write that has just recorded a **real confirmed** txHash would assert something false. A cell asserts that a real confirmed write does not inherit a prior `simulatedTxRef`.

## One implementation detail worth reading

In the poller, the prior blob is read **per write**, not once before the loop. The thread-token mint is fire-and-forget at document create and can land **mid-poll**, so a blob read earlier would not carry a token that exists by the time the write happens — and that race is the actual mechanism by which the token goes missing on a normal anchor. In the reconcile path no extra read is needed: `bc` is already this document's prior blob.

## Test Evidence

**Touched:** `services/originate/src/services/anchorStateSync.ts`, plus a new `services/originate/src/__tests__/ks1074-every-rebuild-writer-carries-threadtoken.test.ts`.

**Base:** this worktree contains develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`. (develop has since moved to `df5e9f5da6d2`, which this worktree does not contain.)

| arm | result |
|---|---|
| originate BARE — source restored **and the new cell file moved aside** | **878 passed / 878, 74 suites**, rc 0 |
| originate PATCHED | **886 passed / 886, 75 suites**, rc 0 (+8 cells) |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

The source restore after the bare arm was asserted by sha256.

**Six red arms, one per writer plus the guard, each reddening exactly its own cell:**

| arm | writer whose carry is removed | cell(s) that red |
|---|---|---|
| A1 | the fail-closed writer | W1 + FALSYTOKEN (both drive that writer) |
| A2 | the poller SUCCESS writer | W2 + NOSIMULATEDTXREFONREAL |
| A3 | the poller SIMULATED writer | W3 |
| A4 | reconcile heal-to-confirmed | W4 |
| A5 | reconcile heal-to-simulated | W5 |
| A6 | the guard reverted to truthiness | FALSYTOKEN only |

Per-writer arms exist **because the repro's six simultaneous reds measure the SET and say nothing about the PARTS** — which is how four writers survived KS-1058.

⚠ **Two arms proved nothing in their first form.** Dropping a spread left `const priorBlob = …` **declared and unused**, which `tsc` refuses: the suite never compiles, reds nothing, and is indistinguishable from an inert tamper unless the runner separates "0 passed **and** 0 failed" from "nothing reddened". It does, and that verdict has caught this class **four times in this session**. Each arm now removes the declaration in the same tamper.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- These cells drive the writers through their exported functions with `getDocument`/`updateDocument` mocked. **No database is involved**, so this does not prove the column round-trips the value — the JSONB round-trip is a separate open item on KS-1129.
- **`blockHeight: anchor.blockNumber || 0` at these same four sites is NOT touched here.** It is the KS-1129 class on a *different* anchoring endpoint and is filed as **KS-1333**, to be built after this merges — on a ruling that being in the file does not put it in scope.

Refs KS-1074

🤖 Generated with [Claude Code](https://claude.com/claude-code)

