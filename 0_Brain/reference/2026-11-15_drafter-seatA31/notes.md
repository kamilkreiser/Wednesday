# Notes, drafter for Seat A 31st, 2026-11-15 ~17:5x AEDT

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatA31_laneA_billing.md (carries the A 30th brief by reference; deltas only).

## 1. Did the KS-1910 push land? YES as a branch, NO as a PR
- `ls-remote origin refs/heads/feature/ks-1910-billing-get-invoicesid-and-delete-payment` = 48916cd8239475941815e675e369841ddb359053 (matches A 30th's commit 48916cd82394).
- A 30th's driver log (push/drv-ks1910/status.txt): PUSH rc=0 at 06:26:05Z, VERIFIED 06:26:08Z, lock released, queue left.
- 06:26Z = 17:26 AEDT, which is 8 minutes AFTER the 17:18 tmux death: the detached driver outlived the seat.
- No PR: `gh pr list --head <branch> --state all` = []; no KS-1910 PR in the 90 open PRs. So no PR-naming comment, no READY FOR GATE. Row 1 of the brief = open the PR from A 30th's drafts (UNVERIFIED until read against the branch diff), comment, READY (docs only; I recommend tier 2, Wednesday decides).
- Also: develop = ce35818d50ae (PR 2140 squash, one commit past A 30th's base 4e4347818772, one packages/shared test file; billing untouched).

## 2. Does KS-1897 (b) conflict with PR 2232's code? YES (read from `gh pr diff 2232`)
Gate 354's assertion "a missing customer credits nothing" is TRUE of PR 2232 and of develop. (b) intentionally changes it.
1. Ordering: 2232 keeps `if (!customerId) { error; return 0 }` and puts its `payment_status !== 'paid'` check after it. (b) replaces that early return with an email match, and the paid check must precede any match/credit (trap i, and no wasted Stripe lookup for unpaid sessions). So (b) reorders 2232's block: build on develop after 2232 merges (or Wednesday allows a stacked PR).
2. Test: 2232's cell C2d "no customer" pins credit 0; with a matching email (b) credits. Edit only after merge.
3. Benefit: 2232 sends checkout.session.async_payment_succeeded through the same handler, so one match in handleCheckoutComplete also fixes the delayed-method email-only case (KS-1934 trap ii). The payment_intent.succeeded backup (customer-only) stays uncovered unless the plan extends it.
PR 2235 (KS-1935) billing.ts hunks are at ~771 and ~823 (503 mapping); KS-1897's are 477/521: disjoint, merge-tree to confirm. 2235 also changes stripeService.ts, which a match helper may touch.
No gate verdict was read by me (not measured).

## 3. Design hazards the brief hands to the seat (money, so a QUESTION)
- The only email on an email-only session comes from the request body (billing.ts zod `customerEmail`, optional), not req.user.email: a caller can type any address, so crediting "the customer whose email matches" can credit someone else's account. Whether the match must be against the authenticated user's email is the central question; I flagged it, I did not decide it.
- Stripe emails are not unique: several matches, no match, and a customer appearing between two deliveries (a redelivery crediting a different customer for the same payment key) are all spelled out as plan items with a "credit nothing and log" default.

## 4. Open-PR census
90 open PRs scanned by the pulls files API; touching services/billing/: 2232, 2235 (this lane), Dependabot 649 and 575 (package files). Control: 2232 found.

## 5. Other
- Ordinals: A 31st 0, A 30th 1. Routing row Secuura/Blockchain-A present. Opus model id claude-opus-5-5 in models_latest.json.
- Brief says the A 30th worktrees (s-a30-base, -ks1910, -ks1934, -ks1935) exist; all UNVERIFIED, read-only for 1934/1935.
- Brief STAMP block left as placeholders for Wednesday to fill.
- Brief size ~19 KB.

## UNMEASURED
- Live state of the four A 30th worktrees, whether the A 30th driver for ks1935 left a waiter running, and the push queue contents.
- Gate 354/355 verdicts; cockpit floor at the stamp.
- develop's webhooks.ts and billing.ts at ce35818d50ae (code reads are of the saved 48883ba5976b blobs plus 2232's diff, which is against 4e4347818772).
- Whether A 30th's drafts for KS-1910 match the pushed commit; the hook's final line for that push (not read).
- Stripe customers.list semantics (case, pagination); where the platform stores a user-to-Stripe-customer link.
- Whether delayed payment methods or the async Stripe events are live on the account (Kam's check).
