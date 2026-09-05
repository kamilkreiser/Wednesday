# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-796 FIRST PASS: PR #816 @ `1e4b6fbbe` — `POST /api/auth/wallet/verify` (and its `/authenticate` alias) must gate the ACCOUNT, not just the wallet (KS-781 door 3, and the helper split doors 1–3 now share)

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context — door 3 of KS-781, and the commit that moves the shared gate
KS-781 (three token-issuing doors kept as one ticket) closed door 1 with #812 (merged 04:34Z after four passes: `projects/secuura/reports/2026-09-05-s127-ks781-regate4-a5542df5a/`). KS-797 (#814, the authorize open redirect) passed its first pass minutes ago (`…/2026-09-05-s128-ks797-authorize-client-redirect-846c29c4a/`) and merges after #810. **This branch is door 3, and it is also where the shared helper `assertAccountMayReceiveCredential` LANDS** — `enforcePasswordLoginGates` (door 1's gate, in `passwordLoginGate.ts`) now delegates to it, and door 2 (KS-795, #815) will add its call site AFTER this merges. So this pass gates two things at once: the wallet door, and the refactor of door 1's gate that door 2 depends on.

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — the builder (s128) is LIVE in that tree with the Docker stack on `:6882`. Never check out, stash or modify anything there; never touch its stack, `.env` or `.env.local`. Take your subject from the git objects (`git worktree add` from your OWN copy, or `git archive`), never from its working tree.
- **Subject:** **PR #816 head `1e4b6fbbe`**, base `develop` `e6fb9d735`, **ONE commit ahead, 0 behind, mergeable clean — 5 files +538/−46** (GitHub API, read by Wednesday at 15:2x AEST): `services/auth/src/services/passwordLoginGate.ts` +172/−39 · `services/auth/src/routes/wallet.ts` +51/−1 · NEW `services/auth/src/__tests__/ks796-wallet-verify-account-gate.test.ts` +264 · `services/auth/src/auth.openapi.ts` +27/−2 · `docs/openapi/secuura-api.yaml` +24/−4. Peter requested, no review yet.
- **Running target:** by-SHA copy with auth's own harness (vitest). Full-stack runtime through the real gateway is off-limits (the builder's stack); doubled dependencies as before, stated. **CIP-8 signature verification is STUBBED VALID by the builder's tests (the repo's own precedent, `auth.integration.test.ts:476`) and the runtime CIP-8 probe is NOT RUN by Wednesday's ruling — do not build one; state it in NOT-TESTED.**
- **Production?** NO. Nothing deployed; no call leaves the machine.

## 2. The builder's claims at `1e4b6fbbe` — inputs to FALSIFY (s126's commit body, read by Wednesday from the object; s126's KS-796 READY mail 00:56Z as recorded)
1. **The door was ungated:** `wallet/verify` validated challenge, expiry, reuse, address match and the CIP-8 signature, then minted a full token pair without asking whether the ACCOUNT may have one. Re-measured by grep with `routes/auth.ts` as the control: `isLockedOut|recordFailure|recordSuccess|accountLockout` wallet 0 / auth 13; `user\.status|status ===` wallet 0 / auth 4; `mfa` wallet 1 (the `mfaEnabled: false` a NEWLY created wallet user gets) / auth 37. Sharpest case: `getOrCreateWalletUser` returns the existing row whatever its status → **a SUSPENDED wallet account kept minting**.
2. **The split:** `assertAccountMayReceiveCredential` lands here — lockout, account status and the second factor, with no password step; `enforcePasswordLoginGates` delegates to it; identifier normalisation lives INSIDE the helper so a new caller cannot reintroduce F-1 (KS-781's leading-space lockout bypass).
3. **One predicate for status at both sites:** removing the status branch from the helper reddened door 3 and left door 1 COMPLETELY GREEN (login carried its own copy) → now `accountStatusForbidsCredential`, called from both sites; the same tamper re-run against the predicate reddens BOTH doors — 3 on door 3 and 4 on door 1 (before: 3 and 0).
4. **Contract change:** `verifySignatureSchema` gains an optional `mfaCode`; empty counts as absent (KS-781 N-1 applied first); the 403 on both `/verify` and its `/authenticate` alias; spec + regenerated yaml carry it.
5. **Red-proofs, sets predicted on the ticket before any tamper:** delete the gate call from the route → 6/4; remove only the status branch → 3; remove only the MFA branch → 2, and **door 1's bypass suite reddened 4 (LEG 1/2/4/8)** — the cross-check that the MFA gate is shared, not merely called. Each tamper RAN 10 tests; files restored byte-identical.
6. `services/auth` green under the split: door 1's three suites 32/32 (s126); s127's rebase runner: **32 files / 381 tests** at `1e4b6fbbe` (labelled as the runner's output, not re-run by s128); `npm run build` (tsc) caught a duplicate `403` key the tsx generator had transpiled past — de-duplicated, spec identical; `generate-openapi` no diff.
7. Not run by the builders: the four platform suites; any full-stack probe through `:6882`; the runtime CIP-8 path.

## 3. Scope
**Charter:** falsify claims 1–6 at `1e4b6fbbe`, then hunt what a shared credential gate can do when a THIRD caller with a DIFFERENT identifier joins it. The wallet door keys on an ADDRESS, not an email: what does the helper's lockout key, its normalisation and its status lookup do with a wallet-resolved user? Which of the account's status VOCABULARY does `accountStatusForbidsCredential` cover — enumerate the statuses the product can store (the schema/enum, the seeders, the admin routes) and drive each through the wallet door; a status the predicate does not name is a status that mints. Is the challenge CONSUMED on a 403 (a refused MFA_REQUIRED that leaves the challenge live is a replay window)? Is anything minted BEFORE the gate (assert on the minter's call count, as KS-797's pass did, not only the status)? Does the refusal differentiate a suspended account from a locked one from an MFA one in a way the door-1 refusals do not (non-differentiation on refusal paths — the pass-1 standard)?

**In scope:**
- **The ten cases, MEASURED in your copy** through the auth service's own app: the two CONTROLs (active/no-MFA mints; MFA with the RIGHT code mints), suspended, deactivated, locked-out, MFA-no-code → 403 MFA_REQUIRED + no credential, MFA-wrong-code, empty `mfaCode` = absent, malformed `mfaCode` rejected, the `/authenticate` alias gated identically. **The mint count on every refusal row.**
- **The split, both sides:** run door 1's three suites (the KS-781 files: the 14-case bypass suite, the drift guard `ks781-login-authorize-agree.test.ts`, the route contract) at this head — number beside 32/32 and 381; then **tamper the PREDICATE** (`accountStatusForbidsCredential`) and predict the failing set on BOTH doors before running (the builder says 3 + 4); then **tamper only the MFA branch** and confirm door 1's bypass suite reddens (4, LEG 1/2/4/8). A tamper that reddens door 3 alone means the sharing is a claim.
- **The normalisation-inside-the-helper claim:** find the identifier the wallet path hands the helper; drive a padded / mixed-case variant of it through the door on a locked-out account (KS-781 pass 1's F-1 shape) — refused, and ONE lockout counter key.
- **Red-proof:** re-derive independently (revert `wallet.ts`'s gate call in your copy → predict → run → compare to 6/4; all ten EXECUTED).
- **Contract:** `generate-openapi` no-diff reproduced (md5 the committed yaml against a regeneration in your copy); the optional `mfaCode` and the 403 on BOTH paths present in the yaml; the duplicate-`403`-key story — confirm `tsc` passes and the generated yaml has exactly one 403 per path.
- **Suites:** auth in your copy; the platform suites if reachable without the stack, else NOT RUN with your own read of whether the diff could affect them (five files, all inside `services/auth`).
- **Palette:** zero colour literals / CSS rules by diff (expect zero — no page file).

**Out of scope:** KS-795 (#815 — door 2, gated after this merges and its part (a) lands), KS-797/#814 (gated, merging), KS-790, KS-782, KS-720/KS-722 (context only), the `updateUser` social-id no-op (its own ticket), CIP-8 verification itself, the builder's tree/stack/env, anything deployed.

## 4–6. Credentials / state / boundary
`.env` exists; you should not need it; never echo. Exclude-and-report-only; own `mktemp -d`; **NEVER `rm`**; tampers on your copies only, restored byte-identically with hashes; **predict every tamper's failing SET before running it and compare the set, not the count.** **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every row (MEASURED / READ ONLY / the builder's reading).

## 7. Known-fragile / carried
The KS-781 passes' own traps stand: a harness without the errorHandler 500s every login; a probe that hard-codes the thing under test cannot measure the fix to it; **a control copied from the working tree is not a control — take the parent's files from the git blob**; the builder's own grep artefact in claim 1 (`\|` under `grep -E` returning zero for the control too) is the shape to watch in your own instruments. KS-797's pass found the shared authorize resolver carried one of four GET rules — ask the same question here: which of door 1's checks does the wallet door NOW get through the helper, and which does door 1 still do outside it?

## 8. Logistics
- **Time-box:** narrow — the ten cases with mint counts, the two-door tamper, the normalisation probe, the red-proof, the contract.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s128-ks796-wallet-verify-account-gate-1e4b6fbbe/report.md` + `evidence/`. Claims table (claimed → measured); new findings by severity with evidence class; NOT-TESTED.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-796 PASS 1 @ 1e4b6fbbe (PR #816)` — BLUF (PASS or NO GO in the first line), report path, claims table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- #816 head 1e4b6fbbe, base develop e6fb9d735, 1 ahead / 0 behind, mergeable clean, 5 files +538/−46 with per-file +/−; Peter requested; #815/#814/#810 states | GitHub API `/pulls/816` `/pulls/815` `/pulls/814` `/pulls/810` and `/compare/e6fb9d735...1e4b6fbbe`, read-only, token sourced transiently from the project's `.env` and never printed | read 2026-09-05 15:24
- Claims 1–6 | the commit body of `1e4b6fbbe` (`git log -1 --format=%B`, local object, no fetch) + the test file's ten `it(...)` names (`git show 1e4b6fbbe:<test path>`) — the builder's own words; s127's 381 from its wrap as recorded in Wednesday's note | read 2026-09-05 15:24
- #815 does NOT carry the helper (`git grep -l assertAccountMayReceiveCredential 7752b1b06` → 0 files; `1e4b6fbbe` → `wallet.ts`, `passwordLoginGate.ts`) | local objects, read-only — Wednesday's read | read 2026-09-05 15:24
- KS-797 pass-1 findings referenced (the resolver carried one of four rules) | `[QA -> Wednesday] KS-797 PASS 1 @ 846c29c4a (PR #814)` 05:15:37Z | read 2026-09-05 15:24
- s128 live in its tree with the stack on :6882 | `lsof` on 6882 (docker) + `tmux capture-pane` of `%8` — Wednesday's project, not the QA project's | read 2026-09-05 15:24

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 15:24
(checked: "CIP-8 stubbed valid" against "assert on the minter's call count" — the stub proves the wallet, the gate is what is under test, and the count is the gate's evidence; "door 2 out of scope" against "the split doors 1–3 share" — door 2's call site does not exist yet, door 1's does and is in scope; "381" against "32/32" — one is the whole auth suite, the other door 1's three files; stated.)
