# QA Agent Invocation Brief — Secuura / Blockchain — s97's merged set, THROUGH-CODE pass (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Secuura / Blockchain, Platform K). Never name or reference any other client. Read only the paths named here. Your report goes under YOUR project tree at `projects/secuura/reports/2026-09-01-s97-rows-through-code/` (create it).

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **This is a CODE-REVIEW pass, not a browser pass** — no running surface, no browser, no Playwright. The charter's rules (FAIL condition first; untested areas as first-class output; findings-only) apply unchanged. Your earlier pass on s96's rows is at `projects/secuura/reports/2026-09-01-s96-rows-through-code/` — read its SUMMARY so you do not re-review what it already covered.

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent through code before Wednesday's completion check and any score. Session 97 merged four PRs tonight on the reviewer's at-head approvals and pushed one fix; you check them through code before the session is scored.

---

## 1. Target
- **Client / Project:** Secuura / Blockchain (Platform K — TypeScript monorepo: `services/*` (jest or vitest per service — READ each `package.json` test script before naming a runner), `packages/shared`, `systemTest/*`).
- **Where the code is:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **READ-ONLY; a live agent may be in this tree.** ONLY `git log` / `git show` / `git diff <A>...<B>` by SHA and plain file reads. **NEVER** fetch/checkout/switch/worktree/stash/pull, no suite runs, no `npm`/`npx`, no writes. A missing object = NOT VERIFIABLE — say so; do not fetch.
- **Environment identity:** none running. Static review against develop `9ca4a627c` (Wednesday's own ls-remote 21:15 AEST) and main `e44600ecc`.
- **Production?:** NO.

## 2. The rows (the builder's claims — inputs to falsify, not evidence)
Develop chain tonight: `c298c7979` → `086ed1bd3` (#744) → `61f3c4b42` (#726) → `bb3bc5e78` (#742) → `9ca4a627c` (#737). Diff each merged row as `git diff $(git merge-base c298c7979 <squash>)...<squash>` and ALSO confirm the squash tree equals the approved head's tree (`git diff <approved-head> <squash> --stat` should be empty or explain itself).
| Row | approved head | squash | ticket / claim | what you do |
|---|---|---|---|---|
| **#744** | `e3ef4788d` | `086ed1bd3` | KS-643 (cross-tenant revoke IDOR) + KS-578 (cold-cache cross-tenant revoke): five live cases incl. a 404→403 interlock (s72 built it 08-26; never through-code reviewed). Merge comment states it does NOT close the KS-578 RESURRECTION defect (a revoke erased by the key's next use). | FULL review (a)–(e) below |
| **#726** | `a9b4ae15f` | `61f3c4b42` | KS-667 — vault tokenise/detokenise: migration 033 self-sufficient + non-destructive repair migration; the reviewer's 033/no-RLS concern was answered by a throwaway-postgres reproduction (applied=43 failed=1 reproduced; PR = 45/0). Never through-code reviewed. | FULL review (a)–(e); pay attention to (d) for the repair migration: NEVER a drop — say if any statement can lose data |
| **#745 fix** | `8a6790fb2` → `39f36d3f4` (branch, NOT merged; approval stale) | — | KS-622 ask 4: the sweep found `POST /api/auth/mfa/verify` returns 400 (body parser INVALID_JSON, ZodError) while the narrowed contract omitted it → fix declares 400 only (`auth.openapi.ts` +9, regenerated yaml +7 confined to the operation, `routes/mfa.ts` comment, new test `ks622-retired-route-contract.test.ts`). 401/404/200 deliberately NOT restored. | DELTA review: `git diff 8a6790fb2...39f36d3f4`; is the test through the REAL route (the body-parser path), can it fail; is 400 doubly reachable as claimed; is the yaml change confined; is anything else in the diff |
| **#742** | `4ea49de47` | `bb3bc5e78` | KS-566 — reviewed at this head in your s96 pass (PARTIAL: F-3 onBehalfOf unreachable for connectors; the x-emitter-internal topology thread). s97 MEASURED the topology before merging: no host route to anchoring; but `/originate/*` bypasses the gateway strip and the property holds only because `anchors.ts` builds outbound headers explicitly → KS-741 filed. | MERGE-FIDELITY only: squash tree == reviewed head; then READ `anchors.ts` at the squash and confirm the "no `req.headers` spread / zero x-emitter-internal references" claim (control: `documents.ts` has them) |
| **#737** | `a07a2570c` | `9ca4a627c` | KS-641 — reviewed at this head in your s96 pass (F-5: compose-defaults removal ⇒ crash loop on a stale .env). s97 posted the F-5 precondition on the PR + KS-641 (docs only, head untouched). | MERGE-FIDELITY only: squash tree == reviewed head; confirm no code changed since your review |
Builder's own instrument failures this session (do not re-flag; DO check the fixes are real where they touched code): five sweep launches for one valid result (~75 min) — two lost to an unbounded `os.execv` loop in run.py (a venv SYMLINK defeats a path-string guard; no loop counter; `PYTHONUNBUFFERED` not `-u` is what survives execv → KS-738); one killed by the agent because the anchoring fixture recreates `originate` from the WORKTREE's compose with no gitignored `.env` (empty interpolation → unhealthy; the same defect it had diagnosed on auth an hour earlier and did not generalise); one invalid because its own `--base-url` doubled `/api/api` (the CLI help warns of it). Run 4's "11 anchoring failures" were 429 bursts (run 5: 16/16). Also caught by its controls: an unquoted `?` URL tripping zsh nomatch so curl never ran; redis NOAUTH read as "no keys"; a grep whose control returned zero until re-run with a known-present pattern. Stack ends 38 running / 0 unhealthy; detached worktree at `8a6790fb2` with copied venv + env files. Tickets filed by s97 (read the claim against the code if a diff touches it): KS-737 (platform-admin login skips MFA when mfaCode omitted — from your s96 F-1), KS-738, KS-739, KS-741.

## 3. Scope — the questions per full-review row (FAIL condition first, every time)
(a) Does the diff do what the ticket and the merge comment claim, and ONLY that? Name any file the claim does not account for.
(b) Is each regression test written at the CLASS, not the finding? Could it stay green if the fix were reverted (source-string grep; key-set compare; a filter excluding the failing case; an assertion ruling out ONE wrong value)? Say which tests could not fail.
(c) Did the row answer the reviewer's asks AT SOURCE (the PR/merge comment vs the code)?
(d) Security/data rows (#744 revoke gate; #726 migrations): the negative AND the positive control; does the guard reach the route (mount order, middleware, path params); for migrations — idempotence, no data loss, what happens on an env where 003's shape is absent vs present.
(e) Runtime change? (then the four-suite final check applied before merge — say whether the merge comment/evidence block shows it ran, as a SET not a count) or tooling/tests only.
**Out of scope / do NOT touch:** running anything; the PS side; #765; ticket state; deployments. No repository writes anywhere.

## 4. Credentials — none. A prompt for any credential = STOP and report.
## 5. State-mutation & cleanup — you mutate nothing; if you find you have, STOP and report exactly what.
## 6. Output boundary (fixed) — findings, report, recommendations ONLY; fix-shape + the regression test the owner should add, in prose, per finding.
## 7. Known-fragile / known-changed
- Known-fragile (hunt the class): gitignored `dist/` survives branch switches; `packages/shared` rebuilt at the ref measured; jest-vs-vitest per service; Prettier `--ignore-path` misses probe variants; automation walks tickets on PR events; **the GitHub search index does not track approval staleness — at-head-ness is the reviews endpoint's commit_id only** (not your instrument, but explains the record).
- Recent, do NOT flag as new: eleven merges today between merge-bases — a diff base is the row's own merge-base, never develop's tip.
## 8. Logistics
- **Time-box:** ~40 minutes. Stop when findings repeat.
- **Findings sink:** `projects/secuura/reports/2026-09-01-s97-rows-through-code/` — one `report-<row>.md` per row (five) + `SUMMARY.md` ranked by severity with a per-row verdict table (CLAIM HOLDS / DOES NOT HOLD / PARTIAL / NOT VERIFIABLE; MERGE-FIDELITY OK / BROKEN for #742/#737) and the verdict line "PASS for review / PASS with findings / FAIL".
- **Signal when done:** end your turn with the SUMMARY path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading.

---

PROVENANCE:
- develop 9ca4a627c / main e44600ecc | Wednesday's own `git ls-remote origin` in the Secuura checkout, 21:15 AEST | read 2026-09-01
- merged SET (approved heads, squash SHAs, chain), topology measurement, F-5 posting, #744's KS-578 boundary comment | Secuura/Blockchain s97 STATUS 2026-09-01T11:14:17Z in wednesday-agent@ | read 2026-09-01
- #745 fix delta (8a6790fb2 → 39f36d3f4, files, declared codes, test) | s97 QUESTION 2026-09-01T11:04:55Z + its RED mail 10:56:15Z | read 2026-09-01
- #742/#737 reviewed heads + F-3/F-5 findings | your own s96 pass SUMMARY, projects/secuura/reports/2026-09-01-s96-rows-through-code/ (Testing Agent MAIN's tree) | read 2026-09-01
- KS-737/738/739/741 filed by s97 | Linear reads by Wednesday + s97 STATUS 11:17:40Z | read 2026-09-01
- s97 wrap facts (instrument failures list, final SETs) | Secuura/Blockchain s97 Session wrap mail 2026-09-01T11:23:31Z in wednesday-agent@ — FILL FROM THE WRAP | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
