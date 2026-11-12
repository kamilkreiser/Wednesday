# Commission: QA GATE 348, TIER 1, on PR 2224 (KS-1197) + PR 2225 (KS-1855 half two), Secuura/Blockchain, 2026-11-13 09:2x AEDT

Commissioned by Wednesday (the 08:0x seat). Model: OPUS (routing v1.0: tier-1 gates = Opus; usage 90%, a guide per Kam 2026-10-22: a gate needs a clone and suites, no local tier can run one). Findings only: nothing fixed, posted, mailed, pushed, merged or written to Linear or GitHub. Work only in `scratch/` of THIS folder; write `verdict.md` here.

## Copy-and-change
Template: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate345-pr2079/commission.md` and the gate344 template it names (read WHOLE: method, scratch-clone rules, fences, red-proof requirements, verdict format). Read gate 345's `verdict.md` there as a model of a tier-1 verdict.

## The subjects (pins by Wednesday's ls-remote 09:19:58 AEDT; re-pin before the first measurement and again before the verdict; say at the top if any moved)
- develop 1ebc3eae6cf455d740df4c948963cceba9bab0a7 (two docs/test squashes after both PRs were cut on ae5b615f4cc0; neither touches these paths per the seat, re-check).
- PR 2224, KS-1197, head a160347eab6655cccac7882bc6933372a475716e: services/api-gateway/src/services/enforcement.ts (+3 -2) + new ks1197-a-non-string-verification-level-ranks-as-none.test.ts (+102). A PARTIAL DEFENCE by Wednesday's ruling (Refs only).
- PR 2225, KS-1855 half two, head 7d4a82f2706335456e882431bc10adc77241fb15: services/api-gateway/src/routes/verification.ts (+8 -1, the certificationVerifyStandInOn gate before mockBodyParser) + ks1628 (+20) and ks815 (+4) existing tests. Implements Kam's card secuura-ks1855-gateway-standin-routes-1110 = c ("gate certification verify behind the test flag until the rewire lands").
- The builder's READY (Seat R 117th, 22:19:22Z) is the claim under test: `/private/tmp/wed_newmail/batch_20261112T221950Z.txt` (read whole; copy it into this folder first, the /tmp file may vanish).

## The questions (tier 1, both PRs)
1. Each ticket's scope sentence (Linear read-only) vs what each PR claims; KS-1197 must NOT be presented as closing the ticket; KS-1855 must say half two only.
2. Red-first, reproduced YOURSELF with the package's own runner at each head and at develop: KS-1197 9 red / 4 green -> 13/13; KS-1855 H1, H2 red -> 22/22. Plant a revert of each product hunk and show the named cells redden.
3. **KS-1197 behaviour:** a non-string verificationLevel now ranks as 'none' (403 above none, admitted at none) instead of throwing. Is "admitted at none" a widening anywhere? Enumerate every caller of meetsVerificationLevel and enforceDocumentTypeRules at the head (git grep with a positive control); the seat says ONE product caller (enforcement.ts:154 <- routes/verification.ts:932, POST /api/documents). Say whether a principal could previously have been REFUSED (by the throw -> 500) where it is now ADMITTED.
4. **KS-1855 behaviour, THE question:** with ENABLE_MOCK_ENDPOINTS unset (docker-compose.yml:523 default false; docker-compose.production.yml:85 false), POST /api/certifications/:id/verify now falls through to the proxy mount (routes/proxy.ts ~663-668: authenticateToken(false), scopes, then originate's own POST /:id/verify, certifications.ts ~1244). (a) What does an UNAUTHENTICATED caller get after the PR, and what did it get before (the stand-in has no auth handler)? Read the auth middleware's `false` mode at source. (b) What does an authenticated caller get? (c) Is anything that was refused now admitted, or vice versa? Prefer an in-process test (supertest against the gateway's express app with the proxy target stubbed) over reading; say which you did.
5. **Consumers:** Peter's tests/e2e/tests/verifier-exhaustive.prelaunch.spec.ts:298 calls this route with no ENABLE_MOCK_ENDPOINTS (seat-measured, unread by Wednesday): read it and state what it asserts and whether the PR changes its outcome in a default stack. Also frontend/issuer api.ts:481 and sdk/javascript certifications.ts:129. Do NOT edit or run Peter's e2e spec against a live stack.
6. Whole services/api-gateway suite at each head and at develop (counts; interleave if load is high), tsc on the service tsconfig, eslint on the changed files.
7. merge-tree of each PR vs develop 1ebc3eae6cf4 (each side's own merge-base), both orders, a planted-conflict control, a develop-lines-survive control; and the 2224 x 2225 pair (same package, different files).
8. The bodies: PREFLIGHT INCOMPLETE 13/16 and unticked Schemathesis/Akto boxes (Kam's card secuura-premerge-block-nine-prs-1113 = c: no self-hold sentence; a merge does not wait on those suites). Confirm no self-hold sentence and no close word.

Verdict format: line 1 `PR 2224: <GO | GO WITH NOTES | NO GO> (at head <full sha>; tier 1)`, line 2 the same for PR 2225, then per PR FOUND / TESTED / HOW / NOT TESTED; findings numbered G348-2224-N, G348-2225-N, G348-BOTH-N. A NO GO names the exact fix.

Return a 10-line summary.
