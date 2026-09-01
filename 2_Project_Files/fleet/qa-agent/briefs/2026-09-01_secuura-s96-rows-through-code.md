# QA Agent Invocation Brief — Secuura / Blockchain — s96's six review rows, THROUGH-CODE pass (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Secuura / Blockchain, Platform K). Never name or reference any other client. Read only the paths named here. Your report goes under YOUR project tree at `projects/secuura/reports/2026-09-01-s96-rows-through-code/` (create it).

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **This is a CODE-REVIEW pass, not a browser pass** — there is no running surface for these changes; the charter's rules on stating the FAIL condition first, untested-areas-as-first-class-output, and findings-only all apply unchanged. No browser, no Playwright, no Chrome.

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent — through code, and in a browser when browser-related — before Wednesday's completion check and any score/merge. Session 96 of this project pushed six review-row changes today; four await the human reviewer, two are already merged. You check them through code.

---

## 1. Target
- **Client / Project:** Secuura / Blockchain (Platform K — TypeScript monorepo: `services/*` (jest or vitest per service — READ each `package.json` test script before naming a runner), `packages/shared`, `systemTest/*`).
- **Where the code is:** the project checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **READ-ONLY, and a live agent may be working in this tree at the same time.** Use ONLY `git log` / `git show` / `git diff <A>...<B>` by SHA and plain file reads. **NEVER** `git fetch`, `checkout`, `switch`, `worktree`, `stash`, `pull`, no suite runs, no `npm`/`npx`, no writes of any kind into that tree. If an object/SHA is missing locally, the row is NOT VERIFIABLE — say so; do not fetch.
- **Environment identity:** none running. Static review against develop `c298c7979` (Wednesday's own ls-remote 19:4x AEST).
- **Production?:** NO — nothing you touch runs anywhere.

## 2. The six rows (the builder's claims — inputs to falsify, not evidence)
Each row = a PR by session 96, its head SHA, the ticket whose claim it implements, and the reviewer's (Peter's) asks it says it answered. Diff each against its merge-base with develop: `git diff $(git merge-base c298c7979 <HEAD>)...<HEAD>`.
| PR | head | files (builder's count) | ticket / claim | state |
|---|---|---|---|---|
| #734 | `3a2fc5264` | 5 | KS-611 — `.strict()` on POST /api/timestamps/batch (Kam ruled option A); Peter's mirror-schema finding REPRODUCED his way (a gutted real schema: old test 8/0 green, new test 4 fail) + a second experiment (drop `.strict()` from the spec twin → 2 fail); `indexOf` greps removed not patched | awaiting review |
| #745 | `8a6790fb2` | 11 | KS-622 — MFA verify redeems backup codes without proof of factor (option B); Peter's inverted-lockout claim done his way: `recordFailure` 5 → 7 call sites, MFA failures now counted; his ask 4 (pre-merge sweep on rebuilt images) EXCLUDED and labelled "queued for the next leg" on the PR | awaiting review |
| #737 | `a07a2570c` | 13 | KS-641 — demo-service inbound auth guard (POST /demo-api/persona/switch minted a real admin session unauthenticated) | awaiting review |
| #742 | `4ea49de47` | 13 | KS-566 — KS-539 G-1 split alignment: `onBehalfOf` added to revoke, dropped from lifecycle; revoke ownership gate = "ask Stuart" per Kam | awaiting review |
| #759 | `f5d4db89f` | 2 | KS-715 — Akto capture dies on ENOBUFS (systemTest capture path) | MERGED (squash `c298c7979`) |
| #741 | `2bdd52742` | 2 | KS-514 — expiration-date validation | MERGED (squash `cfe1f0678`) |
The builder's own list of instrument failures it caught this session (do not re-flag; DO check the fixes are real): a `date -j -f` parsing `Z` as LOCAL (+36000 s) in a watcher; a phantom seventh `authenticateToken(false)` mount that was a comment; a fabricated SHA in a `--force-with-lease` target caught pre-run; a false absence on a parameterised path; a suite run with the wrong runner. **KS-736 (filed by s96): `authenticateToken(false)` coverage gap** — read the ticket's claim against the code if the diff touches it.

## 3. Scope — the questions per row (state the FAIL condition first, every time)
(a) **Does the diff do what the ticket and the PR comment claim, and ONLY that?** Name any file in the diff the claim does not account for.
(b) **Is each regression test written at the CLASS, not at the finding?** Read the test: could it stay green if the fix were reverted (a source-string grep, a key-set comparison, a filter that excludes the failing case, an assertion that rules out ONE wrong value)? Say which tests could not fail.
(c) **Did the row answer the reviewer's asks AT SOURCE?** Where the PR comment says "done Peter's way" or "corrected in Peter's favour", check the code matches the comment.
(d) **Security rows (#745 MFA, #737 demo auth, #742 revoke gate): the negative AND the positive control** — is there a must-succeed case beside the rejections? Does the guard reach the route (mount order, middleware, path params — s96's false-absence trap)?
(e) **Runtime change?** For each row, does it change runtime behaviour (then the four-suite final check applies before merge) or tooling/tests only? State it.
(f) **The two merged rows (#759, #741):** same questions; your finding on a merged row is a follow-up ticket candidate, not a revert request.
**Out of scope / do NOT touch:** running anything; the PS (platform-s) side; #765 (the reviewer's own PR); ticket state; deployments. No repository writes anywhere, including your own scratch inside the Secuura tree.

## 4. Credentials
- **None.** Static read of a local checkout. A prompt for any credential = STOP and report.

## 5. State-mutation & cleanup
- You mutate nothing. If you find you have (a stray file, a changed ref), STOP, report exactly what and where, do not "fix" it.

## 6. Output boundary (fixed)
- Findings, report and recommendations ONLY. No code, tests, tickets or config. Fix-shape + the regression test the owner should add, in prose, per finding.

## 7. Known-fragile / known-changed
- Known-fragile in this repo (measured by earlier sessions — hunt the class): a gitignored `dist/` survives branch switches; `packages/shared` must be rebuilt at the ref measured; jest-vs-vitest per service; Prettier `--ignore-path` misses `*-ks-NNN-probe` variants; Linear/GitHub automation walks tickets on PR events (not your concern, but explains ticket states).
- Recent, do NOT flag as new: the seven merges today (#738 #756 #686 #760 #730 #741 #759) landed on develop between your merge-bases — a diff base must be the row's own merge-base, not develop's tip.

## 8. Logistics
- **Time-box:** ~45 minutes. Stop when findings repeat.
- **Findings sink:** `projects/secuura/reports/2026-09-01-s96-rows-through-code/` — one `report-<row>.md` per PR (six) + `SUMMARY.md` ranked by severity, with a per-PR verdict table (CLAIM HOLDS / CLAIM DOES NOT HOLD / PARTIAL / NOT VERIFIABLE) and the verdict line "PASS for review / PASS with findings / FAIL". Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the SUMMARY path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading.

---

PROVENANCE:
- develop c298c7979 / main e44600ecc | Wednesday's own `git ls-remote origin` in the Secuura checkout, 19:4x AEST | read 2026-09-01
- The six rows: PR numbers, heads, file counts, tickets, states, reviewer asks, the merged squash SHAs, the builder's own instrument failures, KS-736 | Secuura/Blockchain s96 wrap mail 2026-09-01T09:32:55Z + its STATUS mails 08:44Z (KS-611 detail) and 08:57Z, in wednesday-agent@ | read 2026-09-01
- Ticket claims: KS-611 (Kam ruled A, `.strict()`), KS-622 (option B, #745), KS-641 (#737 guard), KS-566 (revoke gate = ask Stuart), KS-291 archived | Linear GraphQL read (read-only grant), comments first:50 client-sorted, 19:4x AEST | read 2026-09-01
- Read-only rule for the checkout (a live agent may be in the tree) | Wednesday's own floor state 19:4x AEST: Secuura s97 launching into that checkout | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
