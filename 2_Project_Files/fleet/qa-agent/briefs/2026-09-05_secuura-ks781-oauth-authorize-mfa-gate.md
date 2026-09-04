# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-781: `POST /api/oauth/authorize` MFA bypass fix (PR #812) — through-code pass with a local runtime probe

**R0 (client isolation):** this brief carries exactly one client's content — Secuura / Blockchain (Platform K). Do not name or reference any other client, in the report or anywhere else. Your report goes under `projects/secuura/`.

## Charter (read first, in full)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Read it end-to-end before running anything. This brief supplies only WHAT and WHERE.

## 1. Target
- **Client / Project:** Secuura / Blockchain (Platform K)
- **Source tree (read-only, for root-causing):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **the builder (s125) is LIVE in that tree in its own session.** Do not check out, stash, or otherwise change its working tree. Read objects by SHA: `git show <sha>:<path>`, `git diff origin/develop..1c79095475`, `git worktree` is NOT to be used inside their repo. **Copy what you need into your own scratchpad by SHA and work there.**
- **Subject:** **PR #812**, head **`1c79095475e78f7164d4f5d6754903b0386b9160`** on `feature/ks-781-security-post-apioauthauthorize-is-a-second-password-only`, base `develop` — read from the GitHub API by Wednesday at 2026-09-05 09:2x AEST (5 files, +485/−11). **Pin to that SHA**; the builder may push again. Report the branch head you observe at the end.
- **Running target:** **A LOCAL stack of the auth service at that SHA, stood up by YOU in your own scratchpad from a by-SHA export, if the service can run in isolation with its unit-test harness (the builder's 11-case suite runs under the auth service's own jest — start there).** Do NOT bring up, stop, or rebuild the project's 40-container Docker stack: it is the builder's and it is running its push hook. If a real runtime probe of `POST /api/oauth/authorize` needs the full stack, report those checks as **NOT RUN — needs the full stack** rather than touching it; the through-code half and the suite-level red-proofs are the floor of this pass.
- **Production?** NO. Nothing here is deployed. **No finding of yours triggers a deploy, and no call leaves the machine.**

## 2. Spec / DoD being tested against

**Ticket:** KS-781 (Linear, team KS, P1) — *Security: `POST /api/oauth/authorize` is a second password-only login.* **Confirmed at runtime by s123 on 2026-09-04:** same account and password → `POST /api/auth/login` 403 `MFA_REQUIRED` (control) · `POST /api/oauth/authorize` **302 with a code** (subject). **Design ruled on the ticket 2026-09-03 15:20Z: mirror login's gates with a minimal `mfaCode`; the two-step consent challenge is KS-782, NOT this ticket.** KS-790 (the broken code→token exchange) is blocked behind this on the board — do not test it and do not recommend fixing it.

**These are the BUILDER'S CLAIMS from PR #812's body and its mail to Wednesday at 2026-09-04T23:02Z. They are inputs to FALSIFY, not evidence.** Wednesday has verified only the PR head and the file list.

1. New `services/passwordLoginGate.ts` applies login's gates **in order**: account lockout **BEFORE** the user lookup (a locked account costs an attacker the same as an unknown one) → the non-differentiating status refusal (pen-test F-11) → password → second factor (TOTP, then backup code, **burned on use**). `routes/oauth.ts`'s authorize calls it.
2. Missing/unusable code → **403 `MFA_REQUIRED`**, mirroring `MfaRequiredError` exactly (same code, same message as login). Everything else → uniform 401. Documented in `auth.openapi.ts` / `secuura-api.yaml`.
3. `/api/auth/login` is deliberately NOT refactored onto the helper; **a test asserts the two routes agree** (the drift guard).
4. 11 cases in `__tests__/ks781-oauth-authorize-mfa-bypass.test.ts`; **four red-proofs**, each failing set predicted in writing before the tamper: revert oauth.ts to password-only → 8 failed / 2 passed; delete only the MFA block → 4/6; move lockout after the lookup → 1/9 (LEG 7); remove the consent field → 1/10 (LEG 9). All tampered files restored byte-identical (md5).
5. **CONTROL 1 asserts a code IS minted** on a correct, complete request — the claim is that without it every "no code issued" assertion is vacuous. Refusal cases assert `createAuthorizationCode` **was not called**, separately from status.
6. Auth suite: develop 27 files / 331 tests → branch 28 / 341, zero regressions. Preflight rc 0 on the pushed head.
7. **The consent page** (the platform's only shipped consent form, previously `email` + `password`) gained an **OPTIONAL `mfaCode` input** — optional exactly as at login, so non-MFA accounts are unaffected — **reusing the existing `.field`/`input` styling: no new CSS rule, no new colour literal.** Wednesday accepted this as part of the fix on two conditions: the PR/ticket say it is the minimal interim and KS-782 remains the proper flow; and **the palette claim is checked by diff, not by the builder's word.**
8. Two of the builder's own instruments failed and were disclosed: a template-literal backtick that produced TS1005 (suite "1 failed / 10 skipped", zero executed), and a fixture that used `scopes` where the route reads `allowedScopes` (a 500 that was the fixture). A stash race produced garbage numbers once; the clean run is the one above.

## 3. Scope

**Charter:** a through-code pass on PR #812 at `1c790954`, hunting the classes this fleet keeps paying for: a gate that mirrors login in name but not in ORDER or in EXTENSION; a red-proof whose tamper hits the test's model rather than the product's path; a "uniform 401" that leaks user existence or MFA state by timing, status, header or body; a control that cannot fail; and a UI change whose "no new colour" claim rests on the builder reading its own diff.

**In scope:**
- **The diff `origin/develop..1c790954`, every hunk of the five files** (openapi yaml, the new test, `auth.openapi.ts`, `routes/oauth.ts`, `services/passwordLoginGate.ts`).
- **Claim 1 — ORDER and EXTENSION:** derive login's gate sequence yourself from `/api/auth/login` (the builder cites lockout at auth.ts:306-320, status refusal :461-481, MFA :501-520, `mfaCode` in the zod schema :82) and diff it against the gate's sequence. Any gate login applies that authorize still does not — or applies in a different order — is a finding. **Look specifically for:** lockout counter INCREMENT on failure (does a failed authorize count toward lockout the way a failed login does, or does it only READ the lockout?); backup-code burn actually persisted; TOTP replay window; `user.status` set the gate does not enumerate; platform-admin accounts; the tenant-resolution path login has and the gate does not (is authorize reachable for a user whose tenant login would refuse?).
- **Claim 2 — non-differentiation:** on the refusal paths, can a caller distinguish "unknown email" / "wrong password" / "locked" / "status refused" / "MFA missing" by status, body, headers, or timing? MFA_REQUIRED is the one deliberate differentiator — is it reachable BEFORE the password is verified (an MFA-state oracle)?
- **Claim 3 — the drift guard:** read the test that asserts the routes agree. What does it actually compare — behaviour on a corpus, or a list of function names? Could login gain a gate tomorrow without this test going red?
- **Claim 4/5 — re-derive at least ONE red-proof independently** in your own by-SHA copy (never in the builder's tree): pick the tamper you judge most likely to have been predicted wrongly, run it, compare the failing SET to the claim. State whether CONTROL 1 would go red if `createAuthorizationCode` were never called by anything.
- **Claim 7 — the consent field:** find where the form is rendered (the file list has no template file — so it is inline in `routes/oauth.ts` or served from elsewhere; say which); confirm by DIFF that no new CSS rule and no colour literal (hex, rgb, hsl, named colour) was introduced; confirm the field is optional for non-MFA accounts at the route AND on the page; confirm an MFA user on that page can now complete the flow through to the 302 (or say NOT RUN and why).
- **Claim 6:** re-run the auth suite on your by-SHA copy if it runs in isolation; report your numbers beside the builder's.
- **Claim 8 / the stash race:** confirm from the tree by SHA that nothing from the stash incident survives (no stray files, no partial hunks) — the builder says files were restored byte-identical against kept copies.

**Out of scope / do NOT touch:**
- **KS-790** (blocked behind KS-781, deliberately) — do not test, do not recommend.
- **KS-782** (the two-step consent challenge) — not this PR; do not report its absence as a finding.
- **The builder's working tree, its Docker stack, its push hook, its `.env`.** Read by SHA only. Two `(conflict_on_2026-09-04)` and three older July untracked files in that tree are sync artefacts already being quarantined by the builder — not findings.
- Anything deployed (demo, prod). Any other client's tree.

## 4. Credentials (POINTER ONLY — never values)
- `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` exists; **you should not need it** for a by-SHA unit-test run. If a check would require sourcing it, prefer NOT RUN with the reason. Never echo a value, never copy one into a report.

## 5. State-mutation & cleanup
- **Pattern: exclude-and-report-only.** Work in your own `mktemp -d`; abandon rather than delete. **NEVER `rm`, anywhere — STANDING (Kam's rule: cleanup means quarantine).** Guard every expansion (`"${DIR:?unset}/…"`). If cleanup starts costing budget, stop and report the affected checks as NOT RUN with the blocker named.
- Any tamper is on YOUR copy only; still restore byte-identically and prove it with a hash, so your red-proof numbers are trustworthy.

## 6. Output boundary (fixed — not a choice)
**Findings, reports and recommendations ONLY.** No code, tests, fixtures, tickets or config changes anywhere. Fix-shapes and the regression test the owner should add, in prose. (Kam ruling 2026-08-11, absolute.)

## 6a. EVIDENCE CLASS ON EVERY FINDING THAT RECOMMENDS AN ACTION (mandatory)
**`MEASURED AT RUNTIME`** (driven and observed — name the probe) · **`PROBED`** (an adjacent call; say what it does NOT cover) · **`READ ONLY`** (from source/spec, not executed). A recommendation without one is incomplete. **This is a security fix on a token-issuing route: a finding that says "bypass still possible" carries its class in the first line, and a finding that rests on a read says READ ONLY in those words.**

## 7. Known-fragile / known-changed areas
- **Known-fragile:** the auth service's own instruments — this session alone produced a compile error read as a red suite and a fixture read as a 500. Suspect your own harness before the build (the fleet's selector-discipline rule).
- **Recent changes — do NOT flag as new:** #807 (KS-788, merged 22:24Z — advisory-gate timeouts), #800 (KS-731, merged 22:34Z), #806 (KS-731 shell suites, open), #808–#811 (KS-663 / KS-693 / KS-792 / the Peter status doc — open, unrelated to auth). KS-737 (closed: "a second factor that can be declined" on login) is the precedent the ticket cites, not a regression.
- **Known open gaps carried:** KS-790 (code→token exchange broken under fail-closed RLS — means NOBODY completes the OAuth flow end-to-end on local today; a runtime 302-with-code from authorize is still the meaningful subject); `BACKLOG.md:7` says 2 of 27 auth files fail at import — the builder reports they do not on develop; confirm or refute in passing.
- The QA project still has no launcher entry, no inbox and no wrap hook — Wednesday runs this hop by hand and reads your report from your own project tree.

## 8. Logistics
- **Session time-box:** one bounded pass. Through-code + the suite-level red-proof are the floor; runtime probes above that are welcome only inside your own scratchpad.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md` with probe scripts in `evidence/` beside it. Findings numbered F-1…; severity Blocker/Major/Minor; each with its evidence class.
- **Escalation path:** back through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class items ALWAYS pause for Kam. Priority on any finding is the humans' call, never yours.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-781 through-code pass @ 1c790954 (PR #812)` — BLUF first, the report's path, findings by severity with evidence class, the NOT-TESTED list, the branch head you observed at the end.

---

PROVENANCE:
- PR #812 head 1c79095475e78f7164d4f5d6754903b0386b9160, base develop, 5 files +485/−11, file list, PR body (the runtime control table, the gate order, the consent-field paragraph) | GitHub API /repos/Secuura/Distributed_Secuura/pulls/812 and /pulls/812/files | read 2026-09-05
- #807 merged 22:24:37Z and #800 merged 22:34:50Z; #806, #808–#811 open | GitHub API /pulls (open list, /807, /806, /800) | read 2026-09-05
- KS-781 In Progress/P1, the 2026-09-03T15:20Z design ruling (minimal mfaCode; consent flow = KS-782); KS-790 Backlog with the inverse `blocks` relation from KS-781 and the 22:27Z reason comment | Linear GraphQL issues query, team KS | read 2026-09-05
- The builder's claims 1–8, the four red-proof sets, the two instrument failures, the stash race, the BACKLOG.md:7 flag, the auth-suite numbers | builder's mail `[Secuura/Blockchain -> Wednesday] QUESTION: KS-781 built — three product-visible items, one is a judgement call I already made` at wednesday-agent@agentmail.to, 2026-09-04T23:02:48Z | read 2026-09-05
- Wednesday's acceptance of the consent field with two conditions (interim + palette-by-diff) | Wednesday's ANSWER mail to Secuura/Blockchain, 2026-09-05 09:2x, in Wednesday's `2_Project_Files/fleet/briefs_staged/s125_ks781_answer.md` — Wednesday's project, not the QA project's | read 2026-09-05
- The builder is live in its own tree with a running Docker stack (do not touch) | Wednesday's daily note 2026-09-05 and `tmux capture-pane` of the builder's pane — Wednesday's project, not the QA project's | read 2026-09-05
