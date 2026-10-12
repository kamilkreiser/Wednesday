# QA gate — PR #1471 (KS-1124 option A, tier 1) — Opus, independent

**Head:** `4a822bd8c244bf45922343d61b2b86bccff4e98f` (confirmed via `ls-remote`: `refs/pull/1471/head` = `feature/ks-1124-blockchain-blob-writes-atomic-j2-3`). Base `db0df4540acf`. 
**Predicted merge:** develop tip `b4a245fba` + head → clean auto-merge (`routes/documents.ts` auto-merged; develop's 6 commits touch it in 3 lines elsewhere). GitHub's `refs/pull/1471/merge` is built on `c78c13d5` (one commit behind develop). 
**Verdict: GO WITH NOTE** — no Major defects. The change is correct for what it claims, the evidence reproduces exactly, and it fixes a latent status-normalisation bug as a side effect. The notes are a stronger-than-true commit title, one hardening gap, and test-gap nits.

How I worked: my own `--no-hardlinks` clone in the scratchpad, PR refs fetched from GitHub. No ref writes in the shared repo. Throwaway PG 15.14 (initdb in the scratchpad, random port, fresh random password, TCP only; stopped and data dir deleted at the end). All 48 Dev migrations applied (`documents` has RLS ENABLE+FORCE). No shared database touched. Logs are in `logs/`.

## (1) Diff
5 files, +389/−43, exactly as described: `documentRepo.ts` (SET clauses, `mergeBlockchain`, the returned record), `routes/documents.ts` (token cache patch in merge mode; retry non-prod blob `status:'failed'` + type), 2 unit test files, 1 new integration file. Nothing else. The SET clauses of the two statements are byte-identical (`diff` of lines 619-642 vs 648-671).

## (2) Red/green — my runs
| Run | Result |
|---|---|
| Integration at head, single-tenant (Prisma) | 11/11 pass |
| Integration at head, MULTI_TENANCY=true (TenantPoolManager pg-pool proxy, confirmed in log) | 11/11 pass |
| Integration file on BASE product code, both modes | 6 fail = **K1-K6** exactly; K7, K8, K9, K10, SETUP pass |
| Integration on predicted merged tree, both modes | 11/11 pass |
| Unit: head's 2 files on base | 6 red (R1×3, M1, the 2 KS-550 pins), 44 pass |
| Unit: same files at head | 50/50 |
| Mutation: no carry | K2 K3 K5 red (both modes) |
| Mutation: merge mode ignored | K1 K3 K6 red (both modes) |
| Mutation: metadata-first COALESCE | K10 red (both modes) |
| Mutation: status-less writes the stale status (`AND false`) | K1 red (both modes) |
| Mutation: terminal guard off | K8 red (both modes) |

Every mutation reds exactly the cells the seat states. (My first status mutant deleted the line, which left `hasStatus` unused and failed all 11 on compile. I discarded it and re-ran with `AND false`.)

## (3) Suites
originate `tsc --noEmit` rc=0 and eslint 0 errors / 23 warnings (all pre-existing unused-disable). This holds on base, head and merged. Full originate unit suite: base 1103/1103, head 1107/1107, merged 1107/1107 (97 suites each). OpenAPI/doc sync: no workflow runs an openapi check, no spec/doc file references the changed shapes, and the PR touches no spec. The only contract-visible change is that the retry route's non-prod 202 body now carries `blockchain.status:'failed'`, which the generator does not constrain.

## (4) Adversarial SQL review
- **Callers.** `updateDocument` is called at documents.ts:806, 886, 918, 933, 1229, 1417, 2425, at anchorStateSync.ts:183, 258, 295, 376, 414, and at verification.ts:396. No aliases. Every caller passes an object literal or a guarded object. No caller passes user input as the blob.
- **Concurrency.** Under READ COMMITTED, PG re-evaluates the SET expressions against the newest row version (EPQ), so the blob is resolved under the row lock. The cells prove this with forced interleavings in both drivers. No new locks are taken. Statement 2's resolver subqueries are plain reads. No new lock ordering, so no deadlock risk.
- **JSONB edges (probe.out).** SQL NULL column, missing key, JSON null, array, string, number, `threadToken:null`, and cert-null→metadata fallback are all handled: replace keeps the token only when it is non-null, merge coerces a non-object stored blob to `{}`, and keep preserves whatever is stored.
- **Injection.** All values are bound parameters. A hostile string round-trips as data (P5).
- **RLS (non-superuser, NOBYPASSRLS role, FORCE RLS).** Unscoped reads return 0 rows. A scoped accept followed by a merge-mode write merges correctly (P2). A write scoped to another tenant returns null and changes nothing (P3).
- **"status not supplied ⇒ keep" changes behaviour, for the better.** On BASE, a status-less write rewrote `mapDbStatus(stored)`: `certified→signed`, `deleted→draft`, `expired→draft` (P4, measured). So the thread-token cache write, which has no terminal guard, could un-delete a row. At HEAD all three are kept. No caller depends on the old normalisation.
- **Carry contract.** "Replace keeping only `threadToken`" matches `carriedForward` (anchorStateSync.ts:111-113) exactly, including `!= null`. `markDocumentAnchorFailed` carries its own KS-1004 fields in the supplied blob, so nothing else is lost relative to the old code.
- **Performance.** Each column adds about 12 jsonb `->`/`COALESCE`/`||` operations on a single row. That cost is negligible.

## (5) Data / rollout
No schema change. No backfill needed: rows whose blob sits only in `metadata`, or holds JSON null or a non-object, are handled in place. A rolling deploy is safe format-wise: old and new instances write identical shapes. Until the last old instance drains, the old read-then-write path (no token carry) can still lose an update. That is the race this PR closes, not a new hazard.

## Defects
1. **Minor — the claim is stronger than the code** (commit title "every writer … is atomic"). Two pre-existing blob writers still decide on a JS read:
   - `anchorStateSync.ts:178-212` `markDocumentAnchorFailed`: the `confirmed` guard (:180) and the txHash/blockHeight/network/anchoredAt carry (:190-196) come from a read taken before the UPDATE. A confirm write landing in between can be downgraded to `anchor_failed` with its txHash erased.
   - `routes/certifications.ts:563`: replaces `certification_metadata` wholesale, outside `updateDocument`. It drops `threadToken` from the authoritative blob, and the KS-550 heal then copies that loss into `metadata`.

   Neither is a regression. Recommend a follow-up ticket or a reworded title.
2. **Minor (hardening) — `documentRepo.ts:632/640/661/669`.** The replace branch has no `jsonb_typeof(supplied)='object'` guard. A future `blockchain: null` would store `[{…}, null]` (probe: `'{}'||'null'` → `[{}, null]`), where the old code stored `null`. No current caller can reach this (verification.ts:393 guards `!healed`).
3. **Nit — integration test :218-224 (K9).** K9 seeds `anchored`, which `mapDbStatus` round-trips, so it cannot detect a status write-back. Only K1 reds on that mutant. Seeding `deleted` or `certified` would pin the semantics change described in (4).
4. **Nit — integration test :93.** `waiting()` counts lock waits cluster-wide with no `datname` or `pid` filter. On a shared CI server, a parallel job could satisfy it and make the forced interleaving vacuous.
5. **Nit — `documentRepo.ts:697-702`.** The returned record carries `threadToken` from the first read, and the read status when none is supplied. This only affects presentation (reconcile returns it).

**Pre-existing, outside KS-1124 scope (for a ticket):** every `updateDocument` rewrites `certification_metadata` to `{signatures, blockchain}`. That erases issuerName, certificationId and certifiedAt written by certifications.ts:563 and the admin backfill. `signatures` and `data` also remain read-then-write: a concurrent sign and anchor write can drop a signature.
