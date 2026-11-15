PR 2237: GO WITH NOTES (at head 48916cd8239475941815e675e369841ddb359053; tier 2)

Gate 360 (tier 2, Sonnet, row G2), 2026-11-15 17:59 to 18:02 AEDT. Findings only: nothing fixed, pushed, posted, mailed, merged, or written to Linear or GitHub. All work in `scratch/` of this folder.

**Pins.** `gh api` + `git ls-remote` at 17:59:52 (`scratch/pin1.out`) and 18:00:47-18:00:53 (`scratch/pin2.out`): develop ce35818d50aebe7f41fc41f677ee03079c36d7ad, PR head 48916cd8239475941815e675e369841ddb359053, state open, merged false. Neither moved.
**Load.** load1 3.0 to 4.2 throughout (light; nothing heavy was run).

## FOUND
**G360-2237-1 (Info; wording).** The cheat fragment says "a refusal makes 2 Stripe lookups where an unknown id makes 1" without the qualifier the flow fragment carries. At billing.ts 153 and 155 a platform administrator returns true before any lookup, and an object with no customer is refused with no customer lookup (1 lookup, equal to unknown). The flow fragment states both exceptions; the cheat fragment's "refused caller" is true for the ordinary non-platform owner-mismatch case only. Not false in context.
**G360-2237-2 (Info; unverifiable detail).** "in_ or pm_ plus about 24 characters", "one per-account Stripe rate limit every billing route shares", and the ruling "Wednesday ruled the first (2026-11-15)" are not checkable from the repo at the pin (Stripe id format and rate-limit scope are Stripe facts; the ruling is an agent-mail ANSWER). Not load-bearing for the decision recorded.
No Low-or-higher finding.

## TESTED
**Q1. Docs only.** `git diff --numstat ce35818...48916cd`: exactly two files, both added: cheat fragment 12/0, flow fragment 9/0. name-status A, A. One commit, parent ce35818d50ae. Nothing else.

**Q2. Claims, read at ce35818d50ae in `Blockchain/Dev/services/billing/src/routes/billing.ts` and `src/services/stripeService.ts` (`scratch/m1.out`):**
- GET `/invoices/:id` at 714 to 720: TRUE. Route opens at 714, `getInvoice` at 717, `mayActOnAttachedTo(..., getCustomer)` check and the 404 at 720 to 723.
- DELETE `/payment-methods/:id` at 687 to 693: TRUE. Opens 687, `getPaymentMethod` 692, `mayActOnAttachedTo(..., findCustomer)` + `sendNotFound` at 693 to 694.
- `mayActOnAttachedTo` at 147: TRUE (declaration at 147; platform early return 153; no-customer return false 155; `await lookup(customerId)` 156).
- "An unknown id stops after one lookup, a refused one makes a second on the customer": TRUE by code (`!invoice ||` / `!paymentMethod ||` short-circuits before `mayActOnAttachedTo`; each of getInvoice, getPaymentMethod, getCustomer, findCustomer is exactly one `stripe.*.retrieve`, stripeService 149, 164, 503, 537). Same bytes: both branches send the same 404 body (sendNotFound 160 to 162; invoice inline 721).
- "A platform administrator returns before any lookup, and so does an object with no customer": TRUE (153, 155).
- Gate 62 F1 counts (invoice refused getInvoice 1 + getCustomer 1, unknown getInvoice 1; pm refused getPaymentMethod 1 + findCustomer 1, unknown 1; other 10 routes equal; wall-clock not measured): TRUE, read in gate 62's own `verdict.md` (G62-F1; 144 probe + 12 call-count cells, 10 equal, 2 unequal). Gate 62 measured at aa64f183 on PR 1871; I re-read the routes at ce35818d50ae and the shape is the same. I did not re-run gate 62's harness.
- "a refused billing id costs one more Stripe lookup than an unknown one": TRUE (2 vs 1).
- "Wall-clock time was not measured": TRUE (gate 62 says the same).
- UNVERIFIABLE: see G360-2237-2.

**Q3. docs-fragments check** (`node Blockchain/Dev/scripts/docs-fragments.mjs check --root <worktree>`, sparse worktrees at develop and head; it needs repo-root `systemTest/__tests__/support`, first try refused rc 2 for that reason, then fixed; `scratch/docs.out`):
- develop baseline: rc 0, OK, flow 117 legacy + 245 new, cheat 112 + 245, the same 2 ADVISORY lines.
- head: rc 0, OK, flow 117 + 246, cheat 112 + 246, same 2 ADVISORY lines (pre-existing; identical on develop).
- Planted unclosed `<div>` appended to the flow fragment: rc 1 "tags are not balanced: <div> opened 1, closed 0".
- Restored from a copy: sha256 equal, porcelain 0, check rc 0 OK again.

**Q4. PR body** (`scratch/pr.json`, parsed after stripping code spans): title has exactly one KS key (KS-1910, begins "Refs"). Body outside code spans: exactly one key, KS-1910 (the ticket URL on line 1); KS-1888 and KS-989 only inside code spans. No closing keyword (regex over title+body: none). No self-hold sentence (regex for do not merge, hold, waiting for, blocked: none). Node line and NOT-covered list present.

**Merge-tree, both orders** on my develop: ce35818 x 48916cd and 48916cd x ce35818 both rc 0, tree 8a660e43c5f07244670bd523ebfc24f7c45f30ea, no conflict. It equals the builder's staged tree 8a660e43c5f0.

## NOT TESTED
A running stack, real Stripe, timing (nobody has measured latency), any unit or platform suite (no code), the pre-push hook (not rerun), gate 62's harness (read, not rerun), Linear state, Node 24. The 2 ADVISORY lines are pre-existing and not owned by this PR.
