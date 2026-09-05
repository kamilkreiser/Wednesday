# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-797 FIRST PASS: PR #814 @ `846c29c4a` — `POST /api/oauth/authorize` must know which client, and where it may answer (an open redirect that carried an authorization code)

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context — the KS-781 campaign, four passes, one merge
This branch is the FIRST of three "doors" rebased onto the develop that carries #812 (KS-781 door 1, merged 04:34Z after its fourth pass). Read the fourth pass's report for the current shape of the authorize route: `projects/secuura/reports/2026-09-05-s127-ks781-regate4-a5542df5a/report.md`. KS-797 was found by pass 1 (F-4) on that route: `client_id "not-a-registered-client"` + `redirect_uri https://evil.example.net/steal` → 302 to the attacker URL **carrying a freshly minted code**. The builder then measured a SECOND half that needs no account: `action:"deny"` with an unregistered client → 302 to the attacker URL with `error=access_denied&state=…` — an open redirect off the platform's own authorization endpoint. **Your job: falsify the fix at `846c29c4a` on BOTH halves, with the GET handler as the control the builder used, and hunt what a shared resolver on a credential-issuing route introduces.**

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — the builder (s128) is LIVE in that tree with the Docker stack on `:6882`. Never check out, stash or modify anything there; never touch its stack, `.env` or `.env.local`. **Read by SHA into your own scratchpad** (`git show 846c29c4a:<path>`; auth is vitest; the four earlier passes' symlink-farm pattern).
- **Subject:** **PR #814 head `846c29c4a`**, base `develop` `e6fb9d735`, **ONE commit ahead, 0 behind, mergeable clean — 4 files +360/−38** (read from the GitHub API by Wednesday at 14:5x AEST): `services/auth/src/routes/oauth.ts` +121/−36 · NEW `services/auth/src/__tests__/ks797-authorize-client-and-redirect.test.ts` +219 · `ks781-login-authorize-agree.test.ts` +10/−1 · `ks781-oauth-authorize-mfa-bypass.test.ts` +10/−1. **Pin to it; report the head at the end.** Peter is requested on #814 for visibility.
- **Running target:** by-SHA copy with auth's own harness (vitest). Full-stack runtime through the real gateway is off-limits (the builder's stack); doubled dependencies as before, stated.
- **Production?** NO. Nothing deployed; no call leaves the machine.

## 2. The builder's claims at `846c29c4a` — inputs to FALSIFY (s126's commit body 01:05; s127's KS-797 comments 04:27Z and 04:42Z; PR #814's body)
1. **One resolver both handlers call** — `resolveAuthorizeClient` — carrying the GET path's rule (reject missing `client_id`; reject malformed before the DB lookup, KS-283; look the app up; check `redirect_uri` against `app.redirectUris`) into the POST path. The POST path refuses an unregistered client and an unregistered `redirect_uri` on BOTH the approve and the deny branches; **a code is NEVER minted for an unregistered client — asserted on `createAuthorizationCode` not being called, not merely on the status.**
2. **The unauthenticated half is covered** — three cases under "the deny path, which needs no credentials at all".
3. **Ten new tests: three credentialed checks + a charset case + two deny cases, and FOUR CONTROLs** (registered pair still gets a code; deny with a registered pair still works; GET still renders consent; GET still refuses an unregistered client). **Red-proof predicted before the tamper: revert `routes/oauth.ts` to the pre-KS-797 parent → 6 failed / 4 passed, exactly those; all ten executed** — re-derived by s127 (a second pair of eyes) with the same result; file restored byte-identical by md5.
4. **An INHERITED wildcard is recorded, not fixed:** `redirectUris.includes('*')` — the GET path's pre-existing rule, kept deliberately so the two handlers cannot disagree; s126's reading "0 of 21 registered apps carry one" is labelled its reading, unmeasured by s127.
5. `services/auth` on the rebased head **32 files / 381 tests** green (counts copied from the runner); `npm run build` rc 0; `npm run generate-openapi` **no diff** ("this fixes behaviour the contract already described"); preflight 12/12 on the push. The rebase used `--onto` from `de1206a63` (a plain rebase on the squash-merged stack conflicts on five files).
6. Not run by the builder: the four platform suites; any full-stack probe through `:6882`.

## 3. Scope
**Charter:** falsify claims 1–5 at `846c29c4a`, then hunt what the shared resolver introduces. What a resolver shared between a rendering GET and a credential-issuing POST can do: agree on the wrong thing (a wildcard `*` in `redirectUris` now accepted on the POST path too — the builder kept it deliberately; measure what it permits: exact match? prefix? scheme? a `*` entry admitting `https://evil.example.net`?); normalise `redirect_uri` differently from the stored set (trailing slash, case in host, default port, `#fragment`, `?query` appended, percent-encoding, `//` in the path, userinfo `https://good.example@evil.example`, a registered URI as a PREFIX of the attacker's); resolve `client_id` before or after the MFA/lockout gate (does an unregistered client now learn whether an email exists or is locked? — non-differentiation on refusal paths, the pass-1 theme); a `state` echoed into the redirect on refusal paths (KS-722's shape — is `state` reflected unvalidated into a 302 anywhere?); an error response on the POST path that itself redirects (a 302 to a validated URI on error is fine; a 302 to the supplied one is the defect wearing an error costume); the deny branch and the approve branch resolving the client through the SAME call (or two calls that can drift); and the two touched KS-781 tests — what changed in them (+10/−1 each) and whether the change weakens what they proved at `a5542df5a`.

**In scope:**
- **Both halves, MEASURED in your copy** with the route driven through the auth service's own app: (a) credentialed approve with an unregistered `client_id` → refused, `createAuthorizationCode` NOT called; (b) registered `client_id` with an unregistered `redirect_uri` → refused, no code; (c) `action:"deny"` with an unregistered client → NOT a 302 to the supplied URI (what is it instead — state it); (d) the four CONTROLs green. Then the normalisation matrix above, each row with its predicted result written BEFORE it runs.
- **The wildcard:** measure what `redirectUris.includes('*')` admits on the POST path now; if a `*` entry admits any URI, that is a finding with the class named (accepted-by-design on GET is not the same as accepted on a code-issuing POST). The 0-of-21 census is UNMEASURED — do not repeat it as fact; if you can count it by SHA from seed data, do; otherwise say unmeasured.
- **Red-proof:** re-derive independently (revert `oauth.ts` to the parent in your copy → predict the set → run → compare to 6/4; confirm all ten EXECUTED).
- **The two touched KS-781 tests:** diff them; state whether the +10/−1 weakens, preserves or strengthens what they assert; run them.
- **Suites:** run auth in your copy; number beside 32/381; `generate-openapi` no-diff reproduced; the platform suites if reachable without the stack, else NOT RUN stated with your own read of whether the diff could affect them (it touches one route file in one service).
- **Palette:** zero colour literals / CSS rules by diff (expect zero — no page file).

**Out of scope:** KS-795/796 (doors 2 and 3, their own passes next), KS-790 (blocked behind KS-781 whole AND this ticket), KS-782, KS-722 (context only — note any overlap), KS-798/799/800/801/802/803; the builder's tree/stack/env; anything deployed.

## 4–6. Credentials / state / boundary
`.env` exists; you should not need it; never echo. Exclude-and-report-only; own `mktemp -d`; **NEVER `rm`**; tampers on your copies only, restored byte-identically with hashes. **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every action-recommending finding, inline: MEASURED AT RUNTIME / PROBED / READ ONLY.

## 7. Known-fragile / carried
The four KS-781 passes' own corrections stand — in particular: a harness without the errorHandler 500s every login (pass 4's own trap); a probe that hard-codes the thing under test cannot measure the fix to it. KS-799 (the consent page cannot submit — CSRF) is LIVE and by ruling; the page is not your surface. **This pass decides the merge of door-one-of-three's first sibling: on PASS, Wednesday's completion check and GO, and s128 merges #814 to develop today.**

## 8. Logistics
- **Time-box:** narrow — the two halves, the matrix, the wildcard, the red-proof, the two touched tests.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s128-ks797-authorize-client-redirect-846c29c4a/report.md` + `evidence/`. Claims table (claimed → measured); new findings by severity with evidence class; NOT-TESTED.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-797 PASS 1 @ 846c29c4a (PR #814)` — BLUF (PASS or NO GO in the first line), report path, claims table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- #814 head 846c29c4a, base develop e6fb9d735, 1 ahead / 0 behind, mergeable clean, 4 files +360/−38 with per-file +/−; Peter requested | GitHub API /compare/e6fb9d735...846c29c4a and /pulls/814 | read 2026-09-05 14:5x
- Claims 1–6 | s126's commit body (846c29c4a, 01:05 +1000); s127's KS-797 comments 2026-09-05T04:27Z and 04:42Z (Linear, read-only); PR #814's body — the builders' reads | read 2026-09-05 14:5x
- KS-797 In Review P2; its description (the RFC citations, the BLOCKS-KS-790 reasoning, the "done means" with the createAuthorizationCode assertion) | Linear GraphQL, team KS, read-only | read 2026-09-05 14:5x
- Pass 1's F-4 (the original finding) and pass 4's shape of the route | the two reports under `projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/` and `…-s127-ks781-regate4-a5542df5a/` | read 2026-09-05 (pass 4 at 14:3x; pass 1 by its mail 2026-09-04T23:26Z)
- s128 live in its tree with the stack on :6882 | `tmux capture-pane` of `%8` — Wednesday's project, not the QA project's | read 2026-09-05 14:5x
