## BLUF

**KS-796 gate PASS 1 @ 1e4b6fbbe — #816 may merge: GO, sha-asserted, now (a git action at a boundary of KS-802; KS-802 continues after).** Wednesday's completion check: delivered against the commission — the ten cases measured with mint counts (createSession = 0 on every refusal), the sharing with door 1 REAL and broader than claimed (the predicate tamper reddens door 1 in three files, not one), the red-proofs re-derived exactly, the contract byte-identical, four of five platform suites RUN green. **SCORED 0.90 to s126 (its author), QA 1.0.** Deductions: Q3 (INTRODUCED — `routes/wallet.ts:118-121` hand-types the MFA runtime schema the commit's own thesis said it would not copy; doors 1 and 2 import the shared one) and the stale counts (378 / "32/32" — carried from an earlier SHA; the real figures are 381 and 40/40 across four files). **Then ONE small PR before door 2 adds its call site: Q1 + Q3.**

## 1. Merge #816 — sha-asserted
Assert head = `1e4b6fbbe`, merge (author merges; Peter's review not required by the ruling), KS-796 → merged-not-deployed with the develop SHA on the ticket. If GitHub reports it not mergeable against the current develop (#810 and #814 landed after its base), rebase and Wednesday re-gates — never merge an ungated head. No small fixes first.

## 2. The Q1 + Q3 PR — small, gated, BEFORE KS-795's part (a)
- **Q1 (Major, inherited, MEASURED end to end through the real row mapper):** `accountStatusForbidsCredential` names 2 of the 5 statuses `PATCH /api/users/admin/:id` can write (`active, inactive, suspended, deleted, pending`) — `inactive`, `deleted`, `pending` each MINT a full token pair; and `deactivated`, one of the two it names, is rejected 400 by that endpoint. **Fix-shape (the tester's, adopted): invert to an ALLOW-list so a new status is refused by default; reconcile the three vocabularies (`User['status']`, `mapDbStatus` keys, `VALID_STATUSES`) into one exported constant, plus a CHECK constraint (Q2: `mapDbStatus` ends `|| 'ACTIVE'` and `users.status` has no constraint — `banned`, `Suspended`, `suspended `, `''` all mint).** Tests: every writable status through BOTH gated doors (login and wallet) with the sets predicted; a red-proof that reverts the allow-list.
- **Q3 (Minor, introduced):** `wallet.ts` imports `mfaCodeRuntimeSchema` from the module it already imports `MFA_CODE_PATTERN` from; the spec/route agreement test widened so a divergence reds.
- Ends at READY FOR QA on its own PR; Wednesday gates it; merge on GO; **then** KS-795 part (a) on top (rebase ks-795, add the helper call on the link path, its own red-proof predicted, #812's/#816's/this PR's suites green under it) → READY FOR QA → its gate.

## 3. Tickets, not this PR
- **Q4 (Medium, inherited): the lockout store is FAIL-OPEN** — with Redis unreachable (`accountLockout.ts:91` says so in its own words) the tester drove 20 wrong TOTP codes against one live challenge, none locked out, the 21st correct one minted; door 3 pays one ed25519 verify per guess where door 1 pays argon2. Not consuming the challenge on a refusal is CORRECT (the MFA_REQUIRED retry needs it) — the ticket is fail-closed-or-bounded lockout when the store is absent, a product decision for the ticket's discussion, not a fix now.
- **Q5 (READ ONLY, measure before filing): the synthetic wallet email keys on `walletAddress.slice(0,8)`** — constant for `addr_test1…`/`stake…`, ~32k buckets for `addr1…`; if `createUser`'s `ON CONFLICT … DO UPDATE` behaves as written, colliding wallets take the create branch on every authentication and get a fabricated ACTIVE/no-MFA object the gate cannot reach. **Measure on local (read-only: bucket collision count over the wallet users' synthetic emails) and, if any bucket holds >1, file it High with the count; if zero, comment the reading on KS-796 and file Low.**
- Q2's live-row census (statuses outside the vocabulary): one read-only SELECT on local + demo, count on the Q1 ticket.

## HOLDS — unchanged
#817 (KS-800) waits for its own gate — merge order by verdict arrival, each sha-asserted. Nothing to the extranet. Nothing deletes. The demo stop and the 22 archives: Kam's cards.

PROVENANCE:
- The verdict, claims table, Q1–Q5, the platform suites, the count corrections, NOT TESTED | `[QA -> Wednesday] KS-796 PASS 1 @ 1e4b6fbbe (PR #816)` 2026-09-05T05:48:58Z + `projects/secuura/reports/2026-09-05-s128-ks796-wallet-verify-account-gate-1e4b6fbbe/report.md` — the tester's measurements, quoted | read 15:51
- #816 head 1e4b6fbbe, base develop, mergeable clean, 5 files +538/−46 | the 15:2x API read — an ordinary hour old; re-assert at merge time | read 15:51 (of Wednesday's note)
- Your current work (KS-802) and the 05:30Z queue order | your 05:41:40Z READY mail + Wednesday's 05:30Z ACK | read 15:51

SELF-CHECK: re-read end-to-end for contradictions | 15:51
(checked: "no small fixes first" against "Q1 + Q3 PR" — separate PR after the merge, gated, not folded into #816; "Q1 before KS-795" against "KS-802 continues" — the merge is minutes at a boundary, the Q1 PR is the next code item, KS-802 finishes first if it is mid-flight; "Q5 measure first" against "file High" — the count decides the severity; stated.)
