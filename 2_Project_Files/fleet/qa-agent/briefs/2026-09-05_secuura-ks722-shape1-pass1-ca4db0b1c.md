# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-722 Shape 1 PASS 1: PR #821 @ `ca4db0b1c` — the OAuth `state` stored at initiate, verified and burned on callback, provider-bound, fail-closed; and the in-memory Redis double that put 19 KS-795 cases THROUGH the gate

**TIER 1** (an auth door: login-CSRF / code injection on the social callback) — full gate. **ROUND 1** of the KS-722 class under the cap (Kam 2026-09-05 20:19).

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context — the finding this PR closes
The door-2 pass (`projects/secuura/reports/2026-09-05-s128-ks795-door2-social-callback-463c45793/report.md`, **F-1 MAJOR**) found the social callback validated NO OAuth `state`: minted at initiate (`routes/auth.ts:907` `randomUUID()`), returned, never stored, never checked — zero `query.state`/`verifyState`/`storeState` matches over `services/auth/src`. That finding was ruled OUT of #815's scope and into its own PR (this one); **KS-781 closes when this merges.** The two-head re-gate (`…/2026-09-05-s130-ks795-815-and-820-regate-06e79adab-48694b1c9/report.md`) confirmed F-1 still open at `06e79adab` — its §A F-1 row is your "before" instrument. READ BOTH REPORTS' F-1 SECTIONS FIRST.

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — the builder (s131) is LIVE there (stack on `:6882`). **Another Secuura QA seat is running concurrently** (KS-800 on #817 — pane `QA/Secuura-s131-ks800-regate`, its own copies and ports): never touch its tree, ports or evidence; announce your own port and check it REFUSES first. Own `mktemp -d`; every command from YOUR copy.
- **Subject:** **PR #821 head `ca4db0b1c`** (`refs/pull/821/head` at origin = `ca4db0b1c87272ed4cafefa25563c10938244bf7`; develop `cd5262dc3`; by `git ls-remote origin` from Wednesday's seat, no fetch, 20:49 AEST). **1 ahead / 0 behind.** Diff `cd5262dc3..ca4db0b1c`: **7 files +468/−23** — **NEW** `services/auth/src/services/oauthState.ts` +102 · **NEW** `__tests__/ks722-oauth-state-verified.test.ts` +239 · `__tests__/ks795-social-link-verified-email.test.ts` +38/− (the in-memory Redis double) · `routes/auth.ts` +24/− · `middleware/errorHandler.ts` +23 · `auth.openapi.ts` +26/− · `docs/openapi/secuura-api.yaml` +39/−. One commit `ca4db0b1c` (20:42). Peter requested; review state "unread".
- **Running target:** by-SHA copy; the `auth` harness (vitest) with the builder's Redis double AND, if Docker is available to you, a REAL Redis ≥ 6.2 container of your own (own port) to exercise `GETDEL`; the harness-level app with a stubbed provider factory (no provider is configured anywhere). `:6882` off-limits. Nothing deployed.

## 2. The builder's claims at `ca4db0b1c` — inputs to FALSIFY (s131's READY 2026-09-05T10:45:21Z, 5,149 chars, read whole)
1. `services/oauthState.ts` on the `refreshDenylist.ts` idiom: **single use** (consume = read+delete in ONE atomic step — `GETDEL`, or a `MULTI` the server runs as a unit — two concurrent callbacks cannot both see the value); **bound to its provider** (the stored VALUE is the provider name — a `google` state is invalid on the `github` callback); **fail closed** (no Redis → refused); **initiate fails if it cannot store**.
2. **The check precedes the code exchange** — a forged callback drives NO outbound token exchange; asserted by its own case.
3. **403 `OAUTH_STATE_INVALID`, ONE code** for absent / expired / already-used / wrong-provider (no oracle); 403 not 400, matching `CSRF_TOKEN_MISSING`.
4. **Red-proof:** gate reverted → predicted 7 failures, SET named before the run (the four refusal cases, pre-exchange ordering, burn-on-use, provider-binding, fail-closed) with the CONTROL and both initiate cases green → measured 7 failed / 3 passed of 10, that set; restored by inverse edit (md5 `c9e44936`).
5. **The 19 KS-795 cases went RED** (their harness mocked `getRedisClient` to `null`, so fail-closed refused every callback) and were fixed with an **in-memory Redis DOUBLE**, deliberately NOT a mock of `consumeOAuthState` — so those 19 drive the REAL store (burn-on-use and provider-binding exercised on every callback). 488 → **498/498**. **The builder names this as the judgement it most wants checked.**
6. Spec: callback `state` was OPTIONAL and ignored → now required `min(1)`; 403 codes three → four; initiate documents the nonce as persisted/single-use/provider-bound. Edited BY LINE (three `state: z.string().optional()` occurrences; the other two are the pass-through `/api/oauth` surface and must stay optional — the first attempt's unique-match assert failed and wrote nothing). `check:openapi` PASS (307 paths, 405 example blocks).
7. Counts: `services/auth` 37 files / 498 / 0; build rc 0; `tsc --noEmit` clean; eslint 0/0 on touched files. Operational: social sign-in now DEPENDS on Redis and fails closed without it (sessions/denylist/lockout already do).

## 3. Scope
- **Closure of F-1 by the door-2 pass's instrument:** the grep set (`query.state`/`verifyState`/`storeState`/`consumeState`) now non-zero with the sites named; then BEHAVIOUR through the real routes with the provider stubbed: initiate → a `state` is stored (read it from the store); callback with the right `state` → proceeds to the exchange (the stub is called); callback with NO `state`, a WRONG `state`, a USED `state` (second callback), an EXPIRED `state` (advance the clock past the TTL — find the TTL), a `state` minted for `google` presented on `github` → 403 `OAUTH_STATE_INVALID`, **the stub NOT called** (the pre-exchange ordering), 0 mints, 0 rows, 0 sessions; store down (double disabled / real Redis stopped) → initiate FAILS, callback REFUSED.
- **Atomicity:** with a REAL Redis if you have one — two concurrent callbacks carrying the same fresh `state` → exactly ONE proceeds; read the implementation for `GETDEL` vs `MULTI` and state which path your server exercised (the builder did NOT run the `MULTI` fallback against a pre-6.2 server — say what you ran). Without Docker: the double's atomicity is a claim — say so under NOT-TESTED.
- **The Redis double (claim 5) — the builder's own nomination:** read it: does it implement the operations the product uses (`GETDEL`? `MULTI`/`EXEC`? `SET` with TTL? `DEL`) with the same semantics; where does it DIVERGE from real Redis (TTL expiry, atomicity, key namespacing); is anything in the 19 cases green ONLY because the double is more permissive than Redis; and the inverse — does the double route the 19 cases through the REAL `consumeOAuthState` (assert the decision function is not a mock)? A tamper: make the double's consume non-atomic (return the value without deleting) → which cases red?
- **Every red-proof in claim 4 re-derived** (SET and COUNT predicted before the run; the gate reverted from the git blob); plus ONE tamper of your own choosing on provider-binding (store the provider but do not compare it).
- **Spec:** the three `state` occurrences at the head — the callback's required, the two `/api/oauth` pass-through ones still optional (a replace-all would have broken them — confirm they are untouched by diff); the four 403 codes named on the callback operation; `check:openapi` in your copy.
- **The introduced-defect hunt on `routes/auth.ts` +24 and `errorHandler.ts` +23:** what else moved; the error class mapping; does the new 403 leak the reason in the body or headers; does the initiate endpoint's failure-to-store path leak a stack; the KS-795 corpus + the #819 login/authorize agree corpus green at the head.
- **Suites** beside 37/498/0; build rc; palette zero (0 UI files).

**Out of scope:** #817/KS-800 (the other tester's), provider enablement (none configured — NOT-TESTED, do not attempt), the demo, the builder's tree/stack, review states.

## 4–6. Credentials / state / boundary — as before
`.env` never echoed. Own `mktemp -d`; **NEVER `rm`**; `${VAR:?}`; quarantine by rename; tampers on your copies, restored by hash; predict SET and COUNT before every run. Findings, reports, recommendations ONLY. No board/GitHub reads. Your own Redis container (if any): own port, stopped not removed.

## 7. Known-fragile / carried
A test double is part of the subject — "mock the neighbours, never the thing under test" (the double must not stand in for `consumeOAuthState`); a green obtained through a permissive double is a double's property; a run that shares a host with another tester's jest run can fail on port contention (the NexusAI re-gate (8)'s own catch) — bind your own ports; a unique-match assert that fails and writes nothing is the right shape (the builder's spec edit); a fix-shape in a report is a hypothesis — run any shape against the unfixed product first.

## 8. Logistics
- **Time-box:** narrow-plus — the F-1 closure matrix, atomicity (real Redis if available), the double's audit, the red-proofs, the spec, the hunt.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s131-ks722-shape1-pass1-ca4db0b1c/report.md` + `evidence/`. Claims table; closure matrix; red-proof table; the double's audit as its own section; new findings by severity with evidence class; NOT-TESTED led with the biggest hole; the head observed at the end.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-722 Shape 1 PASS 1 @ ca4db0b1c (PR #821)` — BLUF (PASS or NO GO first line), report path, closure matrix, the double's verdict, red-proofs, new findings, NOT-TESTED, the head at the end.

---

PROVENANCE:
- `refs/pull/821/head` = `ca4db0b1c`, develop `cd5262dc3`; a local commit object; 1 ahead / 0 behind; 7 files +468/−23; the TWO new files by `--diff-filter=A`; the commit subject | `git ls-remote origin`, `git cat-file -t`, `git rev-list --left-right --count`, `git diff --stat`/`--name-status --diff-filter=A`, `git log` — local objects, Wednesday's seat, no fetch | read 2026-09-05 20:49
- Claims 1–7 | s131's READY 2026-09-05T10:45:21Z (5,149 chars, read whole) | read 2026-09-05 20:51
- F-1 (the door-2 pass) and its "still open" confirmation (the two-head re-gate §A) | the two report paths named in §0, F-1 sections read by Wednesday earlier this seat | read 2026-09-05 19:0x / 19:4x
- The concurrent KS-800 tester | Wednesday's pane list at 2026-09-05 20:51 | read 2026-09-05 20:51
- Kam's 20:19 ruling (tiers + cap) | `tools/kam_rulings_today.sh`; `learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` | read 2026-09-05 20:2x
- Review state of #821 | NOT read — "unread" | —
- scope: TIER 1, round 1 = the F-1 closure matrix + atomicity + the double's audit + the red-proofs + the spec + the hunt on `cd5262dc3..ca4db0b1c`; nothing on #817, provider enablement, the demo | this brief's §3 | read 2026-09-05 20:51
