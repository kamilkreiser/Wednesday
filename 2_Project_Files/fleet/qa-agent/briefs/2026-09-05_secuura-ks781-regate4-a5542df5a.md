# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-781 door 1 FOURTH PASS: PR #812 @ `a5542df5a` — closure of the third pass's P3-1…P3-6 (two by REVERT on Kam's ruling), and what a five-service middleware reorder introduces

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. This is the FOURTH pass — read the three before anything
- Pass 1 (`1c790954`): `projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md`.
- Pass 2 (`da901ffe1`): `projects/secuura/reports/2026-09-05-s125-ks781-regate-da901ffe1/report.md`.
- Pass 3 (`de1206a63`): `projects/secuura/reports/2026-09-05-s126-ks781-regate3-de1206a63/report.md` — CLOSURE of N-1…N-6 except N-2 (relocated); new: **P3-1 MAJOR** (the consent form still cannot be submitted from a browser — `403 CSRF_TOKEN_MISSING` before the relaxed 415), **P3-2 MAJOR** (the relaxation opens a cross-origin, preflight-free path to a credential-verifying, lockout-accruing endpoint), **P3-3 MAJOR** (the KS-471/472 control-byte guard does not inspect form-encoded bodies in five services incl. auth, because it is mounted between `express.json()` and `express.urlencoded()`), **P3-4 MINOR** (login and authorize disagree on `mfaCode: ""`), **P3-5 MINOR** (the KS-439 scope test is case-sensitive while Express routing is not), **P3-6 POLISH** (three routable URL shapes for the same operation refused 415).
**Your job: confirm or refute the disposition of P3-1…P3-6 at `a5542df5a` with pass 3's own probes, then hunt what THIS fix round introduced.** Do not re-run passes 1–3 wholesale.

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — the builder (s127) is LIVE in that tree with the Docker stack up on `:6882`. Never check out, stash or modify anything there; never touch its stack, `.env` or `.env.local`. **Read by SHA into your own scratchpad** (`git show a5542df5a:<path>`; vitest for auth/shared; api-gateway has its own harness; the earlier passes' symlink-farm pattern).
- **Subject:** **PR #812 head `a5542df5a8ccdd01b8b802d433e68bbeee165bca`**, base `develop`, mergeable clean, **one commit above `de1206a63`: `a5542df5a` "KS-781 re-gate (3) fix round: P3-3, P3-4, and the contested pair by REVERT" — 15 files +539/−97** (read from the GitHub API by Wednesday at 2026-09-05 14:0x AEST). **Pin to it; report the head at the end.** The files: `docs/openapi/secuura-api.yaml` +15/−8 · `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` NEW +358 · `packages/shared/src/middleware/index.ts` +12/−2 · `api-gateway/src/__tests__/contentType.test.ts` +16/−29 · `api-gateway/src/middleware/contentType.ts` +23/−25 · `auth/src/__tests__/ks781-login-authorize-agree.test.ts` +19/−6 · `auth/src/auth.openapi.ts` +17/−15 · `auth/src/index.ts` +7/−1 · `auth/src/routes/auth.ts` +6/−2 · `auth/src/routes/oauth.ts` +2/−5 · `auth/src/services/passwordLoginGate.ts` +36 · `originate/src/index.ts`, `referral/src/index.ts`, `staking/src/index.ts`, `vc-issuer/src/index.ts` each +7/−1.
- **Running target:** by-SHA copies with each package's own harness. Full-stack runtime through the real gateway is off-limits (the builder's stack); doubled dependencies as before, stated.
- **Production?** NO. Nothing deployed; no call leaves the machine.

## 2. The builder's claims at `a5542df5a` — inputs to FALSIFY (mail 2026-09-05T04:00:11Z)
1. **P3-3 FIXED, plus the class:** `rejectControlBytes` reordered AFTER every parser in auth, originate, referral, staking, vc-issuer; the doc comment that said "mount immediately after `express.json()`" — the instruction that produced the bug — now says after every parser, with why. New class guard `ks781-p3-3-body-parser-order.test.ts`, 32 cases. **The builder's own extension, not in pass 3's report:** a third mechanism in the class — a parser passed as a *handler* rather than mounted — three sites in api-gateway (`:816`/`:829` behind `ENABLE_MOCK_ENDPOINTS`, and **`:862` handed to `createVerificationRoutes`, LIVE, not mock-gated**), held as an exact set in the class guard and NOT fixed here (KS-800); `demo-service` mounts `express.json()` and no guard at all.
2. **P3-4 FIXED:** one shared `mfaCodeRuntimeSchema` across all four sites, runtime and spec; the drift guard now sends `""` explicitly, three rows incl. malformed-stays-refused.
3. **P3-1 + P3-2 REVERTED (Kam's ruling, 2026-09-05 11:29 + 13:12):** `/api/oauth/authorize` out of `FORM_ALLOWED_PATHS`; spec JSON-only with the registry's 415; **pinned by a test asserting the form body is REFUSED**. The pre-existing-415 premise (s126's leg-B: `403 CSRF_TOKEN_MISSING` reached before the 415) stands and was not re-opened.
4. **P3-5 NOT fixed — KS-801 filed** (High, child of KS-487). **P3-6 resolved by the revert** (all three mis-mappings were for the authorize entry). **KS-799** filed (Medium — the consent page cannot submit its own form, pre-existing CSRF), **KS-800** (High — the class remainder).
5. **Corpus self-correction, disclosed:** the builder's first scan (`services/*/src/index.ts`) found 20 parser mounts; `nft-certificate` mounts in `app.ts` and `wallet-connector` in `server.ts` — invisible to the assertions just written; corrected to `{index,app,server}.ts` → **22 mounts** against a control; KS-573's "23" is one high against today's tree (noted on that ticket).
6. **Red-proofs, predicted then RUN:** one service's guard back between the parsers → 1/29 naming `staking/src/index.ts:57`; login's `mfaCode` back to the bare regex → 2/13, exactly the `""` rows. Files restored byte-identical by md5.
7. **Suites (builder's copies):** auth 31 files / 371 tests · api-gateway 22 / 213 · shared 35 / 530 · `npm run build` rc 0 for shared, auth, api-gateway, originate, referral, staking, vc-issuer · spec regenerated, 307 paths · preflight 12/12 in 57 s.
8. **NOT RUN by the builder, stated:** the four platform suites (its judgement: no route added/removed, no auth-posture change); no full-stack probe through `:6882`; originate/referral/staking/vc-issuer BUILT but their unit suites not run; the api-gateway bound test still fabricates `req.path` (KS-801's subject).

## 3. Scope
**Charter:** confirm P3-1…P3-6 dispositions with pass 3's probes, then hunt the reorder and the revert. What a middleware reorder on five services can introduce: a guard that now runs after the parsers but ALSO after something it must precede (auth? rate limit? the CSRF middleware? route mounts?) — read each service's mount order before and after, by SHA, and name every middleware that changed relative position; a guard reordered in `index.ts` while a service ALSO mounts parsers per-router (a parser inside a router file is still "after the guard" in file order and "before" in request order — which is it?); a class guard whose corpus is `{index,app,server}.ts` — enumerate parser mounts YOUR way (every `express.json`, `express.urlencoded`, `express.raw`, `express.text`, `bodyParser.*`, and any handler-passed parser) across ALL services and compare to 22; the revert's completeness — is there any residue of the form path (the pass-2 round-trip test that POSTed a form body: what does it assert NOW, and is it green for the right reason given KS-799 says the page cannot submit at all); the pinned "form body REFUSED" test — does it refuse at the layer that matters (gateway 415) or only assert an allow-set membership; the shared `mfaCodeRuntimeSchema` — does sharing change LOGIN's behaviour for any input class (`""`, whitespace, non-string, 6-digit with spaces) — diff login's before/after truth table; and the three handler-passed parsers the builder found: confirm `:862` is genuinely live and unguarded (READ ONLY), and that the class guard's exact set would go red if a fourth appeared.

**In scope:**
- **P3-3 — re-derive at the middleware level in your copy:** for auth at least, a form-encoded body carrying a NUL / control byte through the reordered stack → refused by the guard (pass 3's probe); the same through JSON (control unchanged). For the other four services, READ the order and run the class guard; run one service's unit suite if cheap.
- **P3-4 — the drift guard rows:** run them; confirm login and authorize agree on `""`, on a malformed code, on a valid code; state the truth table you measured.
- **P3-1/P3-2 — the REVERT:** at the gateway copy, form POST to `/api/oauth/authorize` → 415 (the pinned test); JSON → passes the content-type check; `/api/oauth/token` form still allowed; spec declares JSON only. State plainly that the consent page therefore cannot submit (KS-799) — that is the ruled outcome, not a finding.
- **P3-5 / P3-6:** confirm nothing in this commit claims to fix P3-5; confirm P3-6's three shapes are now all 415 by the revert (and say so — resolved by removal, not by fix).
- **Red-proofs:** re-derive ONE independently (recommend: the guard back between parsers in ONE service → exactly one class-guard case reddens, naming the file).
- **Suites:** run auth, api-gateway, shared in your copies; numbers beside 31/371, 22/213, 35/530. **The four platform suites:** if they can run from a by-SHA copy without the stack, run them; if not, say NOT RUN and give your own read of whether the builder's judgement (no route/auth-posture change) holds by diff — that judgement is the one un-measured claim in the mail.
- **Palette:** zero new colour literals / CSS rules at the head, by diff (expect zero — no page file in the delta; say so).

**Out of scope:** KS-795/796/797/798/799/800/801, KS-790, KS-782, KS-722 (context only); the builder's tree/stack/env; anything deployed.

## 4–6. Credentials / state / boundary
`.env` exists; you should not need it; never echo. Exclude-and-report-only; own `mktemp -d`; **NEVER `rm`**; tampers on your copies only, restored byte-identically with hashes. **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every action-recommending finding, inline: MEASURED AT RUNTIME / PROBED / READ ONLY.

## 7. Known-fragile / carried
Passes 1–3's own corrections. KS-797 (client_id/redirect_uri validation, code landed on its own branch), KS-798, KS-799, KS-800, KS-801 are LIVE and out of scope — do not re-report; F-9 platform-admin asymmetry deferred by ruling. Merges today: #807, #800. **This pass decides the merge:** on PASS, Wednesday's completion check and GO, and #812 merges to develop today.

## 8. Logistics
- **Time-box:** narrow — dispositions + the reorder/revert hunt.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s127-ks781-regate4-a5542df5a/report.md` + `evidence/`. CLOSURE TABLE for P3-1…P3-6 (disposition claimed → measured); new findings by severity with evidence class.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-781 RE-GATE (4) @ a5542df5a (PR #812)` — BLUF, report path, closure table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- #812 head a5542df5a8ccdd…, base develop, mergeable clean, one commit above de1206a63, 15 files +539/−97 with per-file +/− | GitHub API /pulls/812 and /compare/de1206a63...a5542df5a | read 2026-09-05 14:0x
- Claims 1–8 | builder's mail `[Secuura/Blockchain -> Wednesday] READY FOR RE-GATE (4): #812 @ a5542df5a — P3-3/P3-4 fixed, contested pair REVERTED, KS-799/800/801 filed; two findings not in the report` at wednesday-agent@agentmail.to, 2026-09-05T04:00:11Z | read 2026-09-05 14:0x
- Pass 3's findings P3-1…P3-6 (titles and severities) | the pass-3 report's headings at the path above, read by Wednesday | read 2026-09-05 14:0x
- Kam's REVERT ruling | card `secuura-ks781-consent-page-shipping-surface` ruled 11:29 and 13:12 on the dashboard panel — Wednesday's project, not the QA project's | read 2026-09-05 14:0x
- KS-799 (P3 Backlog), KS-800 (P2 Backlog), KS-801 (P2 Backlog) exist on the board | Linear GraphQL, team KS, exhaustive read at 13:5x AEST — Wednesday's read | read 2026-09-05 13:5x
- The builder is live in its tree with the stack on :6882 | the builder's mail above and `tmux capture-pane` of `%5` — Wednesday's project, not the QA project's | read 2026-09-05 14:0x
