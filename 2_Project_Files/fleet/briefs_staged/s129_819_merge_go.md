## BLUF

**#819 re-gate @ `2ddca095d` — PASS: GO, merge FIRST, sha-asserted, now. No small fixes first — the gated SHA is what merges.** Wednesday's completion check: F-1…F-6 closed at the product path by pass 1's own instruments (mint counts through the real row mapper; the register-takeover probe 200→400 with the legitimate INVITED-stub claim still 201 at both SHAs; the revoke COUNTED; the identity leg reddening exactly one row with no behavioural test moving); all six red-proofs EXACT on set and count; your F-2 falsification REPRODUCED in full and pass 1's shape retracted by the tester in the open. **SCORED your #819 fix round 0.90, QA 1.0.** Deductions: QA2-F1 (introduced, Minor — `Users.tsx:220` writes the UPPER-CASE value into a row set `toUserRow` lower-cases, so the Active card does not increment until reload and the cell renders in caps) and QA2-F2 (the F-5 READ diagnosis names the wrong mechanism — `'blocked'` was never in any vocabulary; case was not the cause — and 2 of the 5 stated product-visible changes were already true at the parent; the wrong mechanism is now a code comment at `:217-219` contradicting `:121`). Credits: the falsification-before-adoption, F-5 found as two halves, every count reconciled.

## 1. Merge — one action
Assert head = `2ddca095d`, merge (author merges), KS-796 → merged-not-deployed with the develop SHA + the deploy note on the ticket: migration 046 is BAKED into the `migrations` image (rebuild, then verify the CHECK constraint directly — the runner's exit is not evidence, KS-808); the admin page lives in exactly ONE image (`admin-frontend`, baked, `mounts=0` with your controls) — **rebuild it on LOCAL now as part of this item (your stack, your call); the DEMO rebuild is NOT yours to run — it is carded for Kam's word with the container-stop precedent.** If GitHub reports it not mergeable against develop `2448370a5` (1 behind = #818, tests only), rebase and Wednesday re-gates — never merge an ungated head.

## 2. The follow-up PR — small, own branch off the NEW develop, gated WITH #815's re-gate
One PR, "KS-796 follow-ups", after the merge and before #815's rebase begins (it is minutes):
- **QA2-F1** — the one token: write the DB-cased value (or run the update through `toUserRow`), so the stat-card predicates at `:499/:507` and the `capitalize` cell agree with a reloaded row. Assert it: the page's own predicates evaluated against a row after an optimistic update (the tester's method — slice the predicates out of the file).
- **QA2-F2** — the comment at `:217-219` rewritten to the TRUE mechanism (`'blocked'` is in no vocabulary; the API publishes the domain case and `toUserRow` lower-cases it); the PR body's product-visible list corrected to the THREE that are real (the button works; it toggles; `deactivated`/`invited` badges) — the suspended-badge and Blocked-card sentences retracted on KS-796 in one line.
- **QA2-F3** — `sysadmin-exhaustive.admin.spec.ts:878` (3.4.7 "Block user via API") PATCHes `'blocked'` and asserts 2xx: the API answers 400 at both SHAs. Fix the value to `'suspended'` and keep the 2xx assertion honest; record on KS-796 that the corpus is 107 tracked spec files / 104 under `Blockchain/Dev/tests` (not 73) and that 3.4.7 has been red or unrun since it was written — say which, from the CI/preflight config, or "unmeasured".
- **QA2-F4** — extend the F-6 guard to the three published wire sites it names (`auth.openapi.ts:147/:449/:2474`) — an agreement assertion per site, since identity cannot hold there (`.optional()` builds a new object); the tester's canary (a module-scope throw in `auth.openapi.ts` leaves 441 green — the file is in NO test's import graph) is the red-proof to predict and run.
- **QA2-F5** — assert `ADMIN_WRITABLE_STATUSES ⊆ DB_USER_STATUSES` (its sibling allow-list has that guard). **QA2-F6** — the stale header at `passwordLoginGate.ts:30-37` ("does NOT refactor /api/auth/login") corrected: login calls it now.
→ READY FOR QA (one line; it rides the #815 re-gate — one tester, two heads, Wednesday's brief will say so). Nothing else in it.

## 3. Then #815, as ruled 06:55Z
Rebase ks-795 onto the new develop → the two PENDING/INVITED cases (both arrival routes) → items a–e (F-4 no-email; F-5 gate before both writes; F-6 uniformity; F-7 spec; F-8 neutral wording; F-2's assertion) → READY FOR RE-GATE (narrow) → GO → merge; KS-781 stays In Progress until KS-722 Shape 1 lands. Then KS-800 items 3–8.

## Records
- KS-796: the tester's NOT-TESTED 5 — `POST /api/users/stub` is now the ONLY route to `invited` and deserves its own pass — file it as a Low ticket if the cap admits, else a KS-796 comment naming it as the next pass's question.
- The census stays "measured by s128/s129 on local; demo unverified by a second pair of eyes" in the PR body — correct as written.

## HOLDS — unchanged
No demo action beyond Kam's stop (the admin-image demo rebuild is a CARD). Nothing to the extranet. Nothing deletes. Handovers to Peter/Stuart as test blocks. Every merge sha-asserted on Wednesday's GO.

PROVENANCE:
- The verdict, closure table, red-proofs, the F-2 re-measure (a)/(b)/(c), QA2-F1…F6, NOT TESTED 1–5, head `2ddca095d` unchanged with your checkout at the same SHA and 0 dirty | `[QA -> Wednesday] KS-796 Q1+Q3 RE-GATE @ 2ddca095d (PR #819)` 2026-09-05T07:47:59Z (8,199 chars, read whole) + its report path | read 17:49
- `refs/pull/819/head` = `2ddca095d`, develop `2448370a5`, 1 behind (#818) | Wednesday's `ls-remote` at 17:2x — an ordinary half-hour old; re-assert at merge time | read 17:49
- The 06:55Z ruling's #815 order and the 07:21Z ACK's tickets | Wednesday's own mails, verified at your inbox | read 17:49
- The v1.3 scope (demo deploys are Wednesday's to authorise) vs today's demo hold (Kam's stop only; the demo image rebuild carded) | the 2026-08-07 signed grant + this seat's judgement: a demo-visible admin page change on the day Kam asked "what's causing the mistakes" goes to him as a card, not as Wednesday's word | read 17:49

SELF-CHECK: re-read end-to-end for contradictions | 17:49
(checked: "no small fixes first" against "QA2-F1 one token" — the token goes in the follow-up PR after the merge, not before; "follow-up rides #815's re-gate" against "gated" — one tester, two heads, stated; "rebuild local now" against "demo carded" — local is the builder's stack, demo is Kam's card.)
