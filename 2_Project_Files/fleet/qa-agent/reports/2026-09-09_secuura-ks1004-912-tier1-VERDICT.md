<!-- RECOVERED FROM THE AGENT'S SESSION TRANSCRIPT, NOT FROM A MAIL.
     The gate did not mail this verdict, because Wednesday's prompt file told it WHAT to
     report and never WHERE to send it. Its pane holds 19 lines of alternate screen with
     no scrollback, so a 15-minute tier-1 verdict was one pane-close from being lost.
     Source: ~/.claude/projects/-Volumes-DevMASTER--CODING-Testing-Agent-MAIN/0bf81fe5-b24f-419f-87c8-09bfcf060484.jsonl
     (last assistant text block), extracted 2026-09-09 by Wednesday s156.
     Verified on extraction: positive control 'NO GO' = 2 hits, negative control = 0. -->

Cleanup verified, source repo untouched. Here is the gate.

---

# QA GATE — Secuura KS-1004 / PR #912 · TIER 1 · round 1

**Verdict: NO GO** — one Blocker, one Major, three lesser findings. The diff itself is sound and its own guard is real; the blocker is what the change **reaches** in another service.

---

## Provenance (re-derived, not inherited)

Every measured claim in the brief re-derives exactly:

| Claim | Re-derived |
|---|---|
| merge-base `e559f7b…` | ✅ `git merge-base` returns it |
| head 1 commit, develop 2 ahead | ✅ `rev-list --left-right --count` = `1 2` |
| true diff = 3 files, 266+/11- | ✅ against merge-base |
| develop frame shows 9 files | ✅ 9 files, 312+/285- — the wrong frame, avoided |
| `inFlight` census 311/313/340/360 | ✅ identical; control `grep -c failed` = 29 |
| `inFlight` is a local `const`, cannot escape | ✅ verified, not inherited — 4 occurrences, none passed to anything |

**I did not touch `:6882`.** No live surface was used, nothing was rebuilt.

---

## HOW — the instrument

`git clone --shared` of the repo into scratchpad, checked out at `ae8751f38`, `node_modules` farmed by symlink. Two contamination checks before trusting it: `packages/shared` is **byte-identical** between the PR head and the source worktree's SHA (empty `git diff --stat`), and the anchor suites mock `documentRepo` anyway, so the farmed link cannot contaminate. Every tamper was applied by exact-count anchor match, sha256-asserted before and after, restored, and the **END sha re-asserted equal to pristine**. Total test count held at 38 across every tamper — so no red was a parse error.

---

## Q1 — Is the destructive branch actually closed? **YES. Red-proofed.**

Baseline at head: **38/38 green** across the three anchor suites.

Removing `&& !bc.txHash` from `anchorStateSync.ts:360` reddens **exactly one cell**, for exactly the right reason:

```
✕ CONTROL: the KS-587 simulated-heal leg still requires NO txHash
  Expected number of calls: 0 / Received: 1
  1: "doc-ks1004", "tenant-1", {"blockchain": {…"txHash": null…}}   ← the destructive write
```

The document went in carrying a real hash and `updateDocument` was called with `txHash: null`. **The guard is load-bearing, not decoration.** A subtler tamper (`!bc.txHash` → `bc.txHash !== undefined`) also reddens, so the coverage is not knife-edge on literal deletion.

## Q2 — Does `ks587-document-blob-simulated.test.ts` reach the branch it names? **Yes, and it is structurally blind to this exposure.**

Its `baseDoc()` carries `txHash: null`, and its first reconcile cell asserts the write happens — so it genuinely reaches `:360`. But every fixture is no-hash, so under the Q1 tamper **all 17 of its cells stayed green**. It is a real test of its own branch and cannot ever catch the KS-1004 exposure. Not a defect in that suite — it predates the exposure — but it means the entire protection rests on **one** new cell.

## Q3 — Is the no-hash write byte-identical? **NO. The author's claim is over-stated.**

Driven differentially: merge-base and head `markDocumentAnchorFailed` on identical fixtures, comparing the block that reaches `updateDocument`. This matters because `updateDocument` does `{...doc, ...updates}` — the `blockchain` object is **replaced wholesale**, so a field absent from the write is a field *erased*.

| fixture | BASE | HEAD | |
|---|---|---|---|
| CTL-A no hash, bare blob | `{…txHash:null,blockHeight:0…}` | same | IDENTICAL ✔ |
| CTL-B hashed | `null` (refused) | writes, hash kept | DIFFERS ✔ |
| **no hash + `network`** | network **dropped** | network **kept** | **DIFFERS** |
| **no hash + `network` + `anchoredAt`** | both dropped | both kept | **DIFFERS** |
| hashed + `threadToken` | `null` (refused) | threadToken **erased** | DIFFERS |

Both controls behaved in opposite directions, so the harness can report either answer. The `?? null` / `?? 0` claim is narrowly true; **the sentence it sits in is not** — the two spreads are not gated on `txHash`, so a *no-hash* document with `network`/`anchoredAt` now comes out different. The test named "*exactly as before*" asserts only 2 of the fields, so its coverage matches the narrow claim, not the broad one.

Forward direction is properly covered: tampering each of `txHash` / `blockHeight` / `network` / `anchoredAt` carry-forward independently reddens a cell.

## Q4 — `preserveTerminalStatuses`? **Held, at the argument level only.**

Dropping it reddens 2 cells. But these suites mock `updateDocument`, so this proves *the option is passed* — **not** that `revoked`/`deleted` survive. The actual preservation is the SQL `CASE` in `documentRepo.ts`, which no test in this PR exercises.

## Q5 — Ordering. **Wednesday's reading CONFIRMED, by driving it, not inheriting it.**

- An already-`anchor_failed` document reaching the `confirmed && txHash` heal at `:324`: **IDENTICAL** at base and head. The change does not move it. ✔
- The genuinely *new* reachability at `:324` is a **`submitted`+hash** document: BASE writes nothing (early-returns at `:313`), HEAD heals it to `confirmed`. This is the exposure the builder found themselves and relabelled honestly from "CONTROL" to "REPRO 2" — that relabelling was correct and it is covered.

---

## Q6 — THE FINDING NEITHER OF US NAMED

**This PR breaks a cross-service invariant: before it, `blockchain.status === 'anchor_failed'` implied `txHash === null`. It no longer does — deliberately and correctly. But another service depends on that invariant silently.**

### 🔴 F1 — BLOCKER · a document whose anchor FAILED now reports `verified: true`

`services/api-gateway/src/routes/verification.ts` (~:508), `POST /api/documents/:id/verify`, is **purely presence-keyed** and never reads `blockchain.status`:

```js
const txHash     = liveTxHash     || doc.blockchain?.txHash;
const blockHeight= liveBlockHeight|| doc.blockchain?.blockHeight;
const confidence = txHash && blockHeight ? 'on-chain' : …;
const blockchainAnchored = confidence === 'on-chain';
res.json({ verified: !isRevoked && hashValid && blockchainAnchored, … });
```

The live chain branch only populates when anchoring says `verified` — so for a *failed* anchor it stays null and the handler falls through to the persisted block, which is exactly what this PR changed.

**Driven against the real router** (real HTTP origin standing in for originate; live anchoring stubbed not-verified):

| document shape | result |
|---|---|
| CTL-1 pre-PR `anchor_failed`, txHash null, bh 0 | `verified:false`, `off-chain-only` ✔ |
| **CASE post-PR `anchor_failed` carrying hash + bh 4242** | **`verified:true`, `anchored:true`, `confidence:'on-chain'`** |
| CASE2 post-PR `anchor_failed` carrying hash, bh 0 | `verified:false` — **but the real txHash is echoed** |
| CTL-2 genuinely confirmed | `verified:true` ✔ |

Both controls behaved, in **opposite** directions, through the same code path — CTL-1 pins "false", CTL-2 pins "true", and the only variable between CTL-1 and CASE is the field this PR changed.

*(My first run of this probe had all four rows identical because my helper called the stubbed global `fetch` and never reached the gateway. The failing positive control caught it. I fixed the harness and re-ran; the table above is the corrected run.)*

**Precondition, stated honestly:** requires `blockHeight > 0` persisted alongside a non-confirmed status. `pollAnchorUntilConfirmed` writes `blockHeight: anchor.blockNumber || 0` with `status: 'submitted'` whenever anchoring reports a block number pre-confirmation, and anchoring composes `blockNumber` from a chain read independently of its confirmed determination (`services/anchoring/src/index.ts:563,675`). So the shape is **producible by code reading — which I did not drive end-to-end**, because that needs a live stack and `:6882` is out of bounds. The gateway behaviour given that shape is certain; its frequency is not.

**Blast radius:** the public verification surface. A failed anchor presenting as a genuine one is precisely the class KS-520/535/587/1004 exist to eliminate. **This is not a defect in the diff** — `anchorStateSync.ts` is correct and well-guarded. The fix belongs in the gateway's `confidence` computation (make it status-aware, as `isAnchoredHonestly` and `verificationV2.healBlobWithChainFact` already are), landing with or before this PR.

**Originate's own verify surfaces are safe** — `isAnchoredHonestly` requires `status === 'confirmed'`, and `healBlobWithChainFact` explicitly early-returns on `anchor_failed`. The gateway is the only presence-keyed consumer found.

### 🟠 F2 — MAJOR · unconditional: a real txHash is served for a failed anchor
Same endpoint, no precondition. Where it returned `txHash: null`, it now returns the real hash (CASE2 above, `anchored:false`). A verifier UI will render a chain link for a document whose anchor failed.

### 🟡 F3 — MINOR · `anchoredAt` on a fail-closed blob contradicts its own documented invariant
`documentRepo.ts:61-63` states `anchoredAt` is *"Absent in the KS-520 fail-closed state — nothing was anchored, so there is no anchor time to record."* The unconditional spread now carries it forward, including for **no-hash** documents (Q3). Fix is one word: gate the two spreads on the hash, or update the type's comment.

### ⚪ F4 — POLISH · `threadToken` erased for the newly-admitted population
`blockchain.threadToken` (a real mint's policyId/scriptAddress/mintTxHash) is not carried forward, and the write replaces. Base refused to write for hashed docs at all, so this is **newly reachable**. Rated Polish only because it has **no reader anywhere in `Blockchain/Dev`** — control: the same grep found 20 other `threadToken` hits, so it is live — and `state_thread_registry` is canonical. `simulated`/`simulatedTxRef` are also dropped, but **identically at base**, so that one is pre-existing and not this PR's.

### 🟡 F5 — MINOR · the other half of the same line is untested
Removing `inFlight &&` from `:360` reddens **nothing** (0 cells). It is load-bearing in the product: an `anchor_failed`, no-hash document with a simulated anchor would be resurrected to `status: 'anchored'`. Pre-existing clause — but it is now the untested half of the one line whose other half this PR made critical.

---

## Regression attribution

Full originate suite: **head 2 failed / 518**, **merge-base 2 failed / 509**. Same file, same two cell names (`ks444-webhooks-create-description-guard`) at both SHAs — **pre-existing, not this PR**. The +9 delta is the PR's 8 new cells plus 1 in ks535.

---

## What I did NOT test

- **Anything live.** `:6882` untouched, nothing rebuilt.
- **The `updateDocument` SQL path.** Every anchor suite mocks it, so `preserveTerminalStatuses` is verified only as an argument; the `CASE` statement, and real merge-vs-replace against Postgres, are unexercised here.
- **End-to-end producibility of F1's precondition** — argued from anchoring's code, not driven.
- **The api-gateway and frontend suites** beyond my own probe; **`ks535`'s 22 modified lines** I read but did not separately red-proof.
- **Non-JS consumers** of the document blob, and any consumer outside `Blockchain/Dev`.

---

## Repo state at close

`git status --porcelain` on `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is **empty (0 lines)**. HEAD unchanged at `b083c0e1` on `feature/ks-963-f3-structural-cells`; `develop` still `f9296f9e`; **0 stash entries**. All work happened in a `--shared` clone in scratchpad; every instrument was removed. Nothing was fixed, merged, pushed or deployed.

---

## CLOSING — I have no inbox; these need someone else to act

1. **F1 decides the gate.** If Wednesday/Kam judge the `blockHeight > 0` precondition unreachable in practice, F1 drops to Major and this becomes GO WITH FINDINGS. I could not settle that without a live stack, and I was told not to obtain one. **That judgement is the single open question.**
2. **F1's fix is in `api-gateway`, not this PR.** Recommend a companion change making `confidence` status-aware. If the fleet prefers, PR #912 can merge *behind* that one — the ordering matters, not the content.
3. **Scope I could not cover:** no live/integration evidence at all, and the `updateDocument` SQL path is untested by anything in this PR. If `preserveTerminalStatuses` matters to the KS-1004 population, it deserves an integration cell.
4. **Outside this brief:** `documents.ts:737`'s thread-token write spreads a **create-time snapshot** of `blockchain` — it can clobber a concurrent poller write. Pre-existing, unrelated to KS-1004, not investigated. Worth a ticket.
5. **Credit where due:** the builder found the `:360` exposure themselves, guarded it, and honestly relabelled a "CONTROL" to "REPRO 2" when their own tamper reddened it. That relabelling was correct — I verified it independently. The three source changes are sound; this NO GO is about coupling, not craft.
