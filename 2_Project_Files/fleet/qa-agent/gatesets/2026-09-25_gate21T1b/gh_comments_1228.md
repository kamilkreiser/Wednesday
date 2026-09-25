--- comment 5826854925 by linear[bot] at 2026-09-25T04:40:35Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1171/guard-3s-re-poll-reads-a-mixed-window-as-absent-one-early-not-found">KS-1171 Guard 3's re-poll reads a MIXED window as ABSENT — one early "not found" then an unreachable chain still schedules a retry that can re-mint a written-ahead transaction (#805 tier-1 r3 residue)</a></summary>
<p>

## BLUF

After #805 (KS-726) merged as `48e65c435` on 2026-09-15, `reconfirmKnownSubmission` treats a bounded re-poll as `'unknown'` **only when NO attempt reached the chain** (`polled === 0`). A window in which at least one attempt answered "not found" (a Blockfrost 404) and every remaining attempt THREW (5xx / 402 quota / DNS) still reads `'absent'`, guard 3 calls it a definitive rejection, and the ordinary retry mints a second fee-paying transaction for a document whose first — the hash just written ahead — may be on its way to a block. This is the same class as the F1 the merge closed (an unreachable chain read as absent), one neighbour over: the fix weights **whether** the chain ever answered, not **when**.

Measured by the tier-1 delta gate (round 3) at `a4d182bf9` and on the merged tree — report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-15-ks726-805-a4d182bf9-tier1-r3/report.md` §5 (cells R3a/b/c, R3b-2nd): with the answer early / middle / late in a 3-attempt window, `polled 1 / errored 2` each time → `'absent'` → `scheduleRetry` 1; R3b's second call minted TX_B (`minted [TX_B]`, `signedHashes [TX_A, TX_B]`, row `confirmed`/TX_B). Grade: **TICKET, ships-with** — the gate's, endorsed by the coordinator; filed by the merge seat as the ADDENDUM required.

## Why the early 404 is a likely FALSE negative in exactly the case that matters

The retry is wrong only when TX_A is in fact accepted while the node says "inputs spent" for it — a same-hash duplicate submit, the two-process race the module's NOT HANDLED list already names. In that premise TX_A entered the mempool seconds before the 400; Blockfrost's `/txs/{hash}` answers 404 until the tx is in a block **and** indexed; the production poll's first attempt lands \~10–12 s after the 400, the second \~15–17 s later, the third \~22 s later. So an early "not found" says little, and a rule that accepts any single answer as definitive is weakest at the start of the window — where a fresh transaction is most likely to be unindexed.

## Blast radius (round 2's units, the gate's reading)

Severity **HIGH** — a duplicate fee-paying transaction (\~181,825 lovelace) and an unrecorded on-chain anchor for the document (TX_B is a valid anchor; TX_A is the orphan; no data loss, no false "anchored" claim). Likelihood **LOW** — {a same-hash duplicate submit} ∧ {TX_A unindexed at every answered attempt} ∧ {the provider unreachable from the first unanswered attempt through attempt 30, \~27 min}. Blast radius one document per occurrence. The gate did not accept "rarer than F1": by its arithmetic the residue's outage-start window is of the same order as the closed case's; both hang on a long provider outage (or a 402 quota exhaustion, a sustained state that naturally arrives mid-poll) beginning within tens of seconds of a duplicate submit.

## Where it lives (at `48e65c435`)

* `services/anchoring/src/cardano/confirmation.ts` — `waitForConfirmation` reports `polled` / `errored` counts only; nothing says WHEN the last answer came.
* `services/anchoring/src/anchorSubmission.ts` — `reconfirmKnownSubmission`: the `confirmation.polled === 0` → `'unknown'` arm (after the `confirmed` return, before the `'absent'` return); guard 3's `refusedAndAbsent` reads `'absent'` as definitive.
* The shipped cells that pin today's rule: `__tests__/ks726-gate-f1-unreachable-chain.test.ts` — "a mixed window (throw, not found, throw) reads ABSENT … → retry" is a deliberate pin of the commissioned "any attempt" semantics and must be REWRITTEN, not deleted, by whoever changes the rule.

## Fix-shape (prose — the gate's, for the owner to weigh; not a committed artefact)

Have `waitForConfirmation` also report `lastAnsweredAttempt` (or the elapsed ms at the last answered attempt), and have `reconfirmKnownSubmission` treat `'absent'` as definitive **only when the last answer is late enough for a mempool transaction to be in an indexed block** — e.g. `polled >= 2`, or an answer ≥ 60 s after the 400 — else `'unknown'` (rest in `submitting` for the reconciler). Regression cells: (404, throw ×29) → `'unknown'`, `scheduleRetry` 0, the row rests; CONTROL (404 ×k spanning ≥ 60 s, then throws) → `'absent'` → retry; the existing all-404 and all-throw cells unchanged. **The cost to weigh:** a genuinely absent transaction whose late attempts threw would now rest \~24 h for the reconciler instead of retrying in \~15 s — the (c) ruling's own concern — so this is a design decision for the ticket owner, not a bug fix, which is why the builder did not make it under KS-726.

## Two smaller records the gate carries, stated here so they are not lost

* (8j) the `confirmed`-before-`polled === 0` ordering in `reconfirmKnownSubmission` is unpinned by any shipped cell; the cell to add if wanted: an injected `{ confirmed: true, polled: 0 }` → row `confirmed`, no `'unknown'` log.
* (8k) `getTransaction` returns `null` when no Blockfrost client is configured (`cardano/provider.ts`), which the `polled` counter reads as "the chain answered"; pre-existing, unreachable through the production submitter without a real 64-hex hash on the row.

## Symbol search before filing (the `issues` filter over title + description + comments, `includeArchived:true`, 1,160 issues; controls 1/0 as expected)

`reconfirmKnownSubmission` → 1 (KS-726 itself, the merge seat's own comments) · `lastAnsweredAttempt` → 0 · `mixed window` → 0 · `reads 'absent'` → 0 · `unreachable chain` → 1 (KS-671, the /health chain-path mechanism — different) · `polled` → 8 (KS-726's comments, wrap comments on the review parent, and KS-683's consumer re-poll — a different mechanism; the rest archived and unrelated). No open ticket owns this.

## Related

KS-726 (the parent finding; merged as `48e65c435`, PR #805) · the gate report above (§5, §7).
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1171-lastans-a-transaction-is-absent-only-when-both-of-kams-04c67fda05e9">Review in Linear</a></p>

