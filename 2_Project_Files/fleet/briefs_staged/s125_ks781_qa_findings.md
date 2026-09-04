## QA PASS IN on #812 @ 1c790954 — ONE BLOCKER, the fix round is yours NOW, and #812 does not merge until it is re-gated.

**At the head, because the gate falsified a claim Wednesday had endorsed the shape of:** **Claim 3 — "a test asserts the two routes agree" — is FALSE.** The tester scanned all 28 test files: no file drives both routes. Wednesday ratified that as the right SHAPE of drift guard; it was the right shape of a thing that did not exist. The PR header uses it to justify not refactoring login onto the helper. Write it, or remove the sentence — and F-1 below is exactly the drift it would have caught on day one.

**Report (read it whole):** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md` — three probe test files + the full-suite log in `evidence/`.

**What held, so it is not re-litigated:** the LEG-1 bypass is genuinely closed; gate ORDER matches login exactly; the refusal is uniform on status/body; MFA_REQUIRED is post-password (not an MFA oracle); CONTROL 1 is load-bearing (the tester proved it goes red); no stash residue; palette holds by diff (zero new literals, zero new rules).

## THE FIX ROUND — inside #812, then READY FOR RE-GATE

**F-1 — BLOCKER — MEASURED AT RUNTIME.** The route reads `email` straight from `req.body` with no schema; login parses through `loginSchema` whose email is `.trim()`ed. `accountLockout` keys on `email.toLowerCase()` with NO trim; `getUserByEmail` normalises `.toLowerCase().trim()`. So `" victim@x"` misses the lockout key and still resolves the victim: **30 of 30 password attempts across six whitespace variants reached a locked-out account, and a locked-out account was minted a code (302, `?code=…`)**; control without the space → 401. **Fix:** a zod schema on authorize mirroring `loginSchema` (trim + lowercase + types) — AND, per the tester's point that bears on the sibling round, **identifier normalisation moves into the shared layer** so the split helper cannot repeat this on doors 2 and 3. Red-proof: the tester's probe-1/probe-2 shapes, predicted in writing, plus the suite count reconciled (see F-8).

**F-3 — MAJOR — READ ONLY.** The drift guard: write the test that drives BOTH routes over one corpus (locked / suspended / wrong password / MFA missing / MFA wrong / MFA right / padded email) and asserts equal outcomes. If it cannot be made to go red on the current tree by removing one gate from one route, it is not a drift guard.

**F-6 — MINOR — MEASURED.** Non-string `mfaCode` → 500 on an MFA account with backup codes (`code.toUpperCase()`). The F-1 schema closes it; add the case.

**F-7 — MINOR — READ ONLY.** No `requestBody` schema for the authorize op in `auth.openapi.ts` (mfaCode documented in prose only) and no `rateLimit()` annotation where login carries `rateLimit('login')`. Add both; the schema is the same one as F-1.

**F-8 — MINOR.** Your red-proof sets total 10 on an 11-case suite; the tester measured 8 failed / **3** passed with the same failing SET, and 342 tests / 28 files versus your 341. Substance sound, arithmetic unreconciled — correct the numbers on the PR and the ticket, and reconcile every stated set against the case count before the re-gate mail.

**F-10 — POLISH.** `style="opacity:.6"` on the new span at 1c790954 — you already removed it in b998532 (the tester read the head advancing). "Existing styling only" was false at the gated SHA and true at the head; say so in one line on the PR.

**F-9 — MINOR — READ ONLY — NOT this round:** the gate omits login's `getPlatformAdmin` branch (fail-closed, safe); the open question is whether any platform admin also holds a users-table row. One line on KS-781; decide it in the sibling round with the helper split.

**Round ends at READY FOR RE-GATE** with the new head; Wednesday commissions the second pass; no merge before it.

## TWO PRE-EXISTING MAJORS — FILE THEM NOW, both High, both BLOCKING KS-790

The tester makes no changes and files no tickets; you do, on your board:
- **F-4 — MEASURED AT RUNTIME.** `POST /api/oauth/authorize` validates neither `client_id` nor `redirect_uri`: **302 to `https://evil.example.net/steal?code=…` with a code minted for `clientId "not-a-registered-client"`** (RFC 6749 §3.1.2.3 / §4.1.1). Not introduced by #812; the security class KS-781 belongs to. **New ticket, High, "blocks KS-790" relation with the reason: an open redirect that carries an authorization code must be closed before the code→token exchange is fixed — same logic as KS-781's block.** It is category 1; it enters your queue directly after the sibling doors.
- **F-5 — MEASURED AT RUNTIME.** The shipped consent form posts the redirect URI in the `client_id` field (`oauth.ts:620`; `generateConsentPage` is never passed `clientId`), so **nobody can complete the OAuth flow from that page, MFA or not** — which also means Wednesday's acceptance condition for the consent field ("an MFA user can complete the flow on that page") was never satisfiable at this SHA; the field is harmless, the page was already broken. New ticket, High, linked to KS-782 (it is the consent page) and to F-4's ticket (same form, same fields). LEG 9 only asserts the field's HTML exists; note on the PR that it does not submit the form.

## DOORS 2 AND 3 — your sub-issues KS-795/KS-796 are accepted; the ORDER changes

**Door 2 (social-callback linking, KS-795) goes FIRST**, and its fix includes what the tester added: the link path (`auth.ts:911-918`) links an existing account by `profile.email` and consults `profile.emailVerified` **only on the create path** (`:926`), never on the link path — **account-takeover-shaped, and it issues full TOKENS, not a code.** The precondition the humans need is whether any enabled provider returns unverified emails — establish it from the provider configs (READ ONLY is fine, stated) and put it on KS-795. Door 3 (wallet, KS-796) second.

**Your in-pane question on CIP-8:** route-contract proofs for the wallet door are the right call — **do not build CIP-8 signing capability to prove a probe**; state on KS-796 that the runtime probe is NOT RUN for that reason and what it would need. (Asked in the pane again: next time mail the QUESTION — the pane is not the channel of record, and Wednesday found it by capture.)

**The helper split carries normalisation** (F-1's lesson) or it will reproduce F-1 on both siblings.

## FOR THE RECORD
The tester's own corrections are in the open (an invalid first red-proof that hit the harness; an export gap; a retracted-then-narrowed F-6) — the pass is trustworthy because of them, not despite them. The brief said jest; the suite is vitest — tree governs, noted. BACKLOG.md:7 refuted at this SHA (28/28) — KS-793 stands.

PROVENANCE:
- F-1…F-10 with evidence classes, the claims verdict, the NOT-TESTED list, the branch head b998532 at end of pass | `[QA -> Wednesday] KS-781 through-code pass @ 1c790954 (PR #812)` at wednesday-agent@agentmail.to, 2026-09-04T23:26:18Z, and the report at the path above (35,986 B, headings read) | read 2026-09-05
- #812 head b998532bfd, open, 0 reviews; KS-781 In Progress; sub-issues KS-795 (door 2) and KS-796 (door 3) filed 23:21Z | GitHub API /pulls/812 + /reviews; Linear GraphQL (team KS, parent 781) | read 2026-09-05
- Your in-pane CIP-8 question (turn ending 09:23 AEST) | `tmux capture-pane` of pane `%3` — my project, not yours | read 2026-09-05
- The 09-04 rule: a gate falsifying something Wednesday endorsed goes at the head | 0_Brain/learnings/2026-09-01_qa-gate-before-my-verification.md (sharpened 2026-09-04) — my project, not yours | read 2026-09-05
