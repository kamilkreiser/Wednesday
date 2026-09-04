# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-781 door 1 RE-GATE: PR #812 @ `da901ffe1` after the fix round (F-1 Blocker, F-3 drift guard, F-6/F-7/F-8/F-10)

**R0 (client isolation):** this brief carries exactly one client's content — Secuura / Blockchain (Platform K). Do not name or reference any other client. Your report goes under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` — read it end-to-end before running anything. This brief supplies only WHAT and WHERE.

## 0. This is a RE-GATE — read the first pass before anything else
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md` (+ `evidence/` probes). It judged `1c790954` and found: **F-1 BLOCKER** (lockout on `POST /api/oauth/authorize` defeated by a leading space — route read `email` raw; `accountLockout` keyed on lowercase-untrimmed; `getUserByEmail` trimmed) · **F-3 MAJOR** (the claimed "routes agree" drift guard did not exist) · F-4/F-5 pre-existing Majors (now KS-797 / KS-798 — NOT this pass's subject) · F-6 (non-string `mfaCode` → 500 with backup codes) · F-7 (no requestBody schema, no `rateLimit()`) · F-8 (red-proof arithmetic) · F-9 (platform-admin asymmetry, noted) · F-10 (one inline style). **Your job is to confirm or refute that each in-scope finding is CLOSED at `da901ffe1`, and to look for what the fix introduced.** Do not re-derive the whole first pass; re-run its probes where they apply and extend them where the fix changed the surface.

## 1. Target
- **Client / Project:** Secuura / Blockchain (Platform K)
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — **the builder is live in that tree and is being ROTATED during this pass** (a successor seat boots and may push on OTHER branches). Never check out, stash or modify anything there; never touch its Docker stack or `.env`. **Read by SHA** (`git show da901ffe1:<path>`, `git diff origin/develop..da901ffe1`) and copy into your own scratchpad, as the first pass did (symlink farm for `node_modules`, vitest cache never in their tree).
- **Subject:** **PR #812, head `da901ffe1a1e0cbc08129c27961abf605b623cca`**, 4 commits (`03c4f9c6f` → `1c7909547` → `b998532bf` → `da901ffe1`), 7 files +929/−11, base `develop` — read from the GitHub API by Wednesday at 2026-09-05 10:3x AEST. **Pin to that SHA**; report the branch head you observe at the end.
- **Running target:** by-SHA copy in your scratchpad with the auth service's own harness (**vitest**, not jest — the first pass corrected the brief). Full-stack runtime probes are off-limits (the stack is the builder's); doubled Postgres/Redis/argon2 as in pass one, stated as such.
- **Production?** NO. Nothing is deployed; no call leaves the machine.

## 2. The builder's claims at `da901ffe1` — inputs to FALSIFY
From the builder's READY FOR RE-GATE mail (2026-09-04T23:40:11Z) and the PR. Wednesday has verified only the head, the commit list and the file list.
1. **F-1 CLOSED in BOTH layers:** a zod schema on authorize mirroring `loginSchema` (trim + lowercase + types) at the route, AND identifier normalisation moved into the shared gate layer (`passwordLoginGate.ts`, +194 lines total now). **Builder's own retraction, keep it in view:** its earlier red-proof "removing the gate normalisation → 1 failed / 13" was measured under a FAULTY stub (the stub compared raw email; the product lowercases and only trim was missing). Re-measured: **removing the gate normalisation ALONE does NOT redden** — the route schema's trim covers this door; the gate-layer normalisation is defence in depth for doors 2 and 3. The true pre-fix state (no schema AND no normalisation) reddens F-1 + F-6 (2 failed / 12 passed) and the drift guard's padded row (1 failed / 8 passed).
2. **F-3 — the drift guard NOW EXISTS:** `__tests__/ks781-login-authorize-agree.test.ts` (+230), 9 rows over one corpus, each driven through BOTH routes and reduced to VERDICT + CLASS (the routes speak different dialects; shapes are not compared). Red-proof: removing the status gate from one route fails exactly `suspended` and `deactivated` — 2 failed / 7 passed, predicted first. **Stated limit:** it mocks `getPlatformAdmin` to null and therefore does NOT compare the admin branch (F-9 stays open, noted on KS-781). **On its first run it caught the builder's own stub** (a false LOGIN defect) — the stubs now mirror the real lockout key derivation `lockout:locked:${email.toLowerCase()}:…`.
3. **F-6 CLOSED** by the same schema (4 non-string shapes covered). **F-7 CLOSED:** requestBody schema in `auth.openapi.ts` (+38) and the yaml (+62), `rateLimit('login')` on the op, `check:openapi` rc 0. **F-8:** all stated sets now reconcile against 354 tests / 29 files (the 8/2 figure was a 10-case suite republished beside an 11-case one). **F-10:** the inline style is gone at the head, said on the PR.
4. `routes/auth.ts` +5/−1 — the builder does not describe this hunk in its mail. **Establish what it is** (the shared-layer normalisation touching login? the drift-guard's export? something else) and whether it changes login's behaviour.
5. Preflight rc 0 on the pushed head; suite 29 files / 354 tests all passing.
6. **NOT in this PR, by ruling:** doors 2 and 3 (KS-795 / KS-796 — next seat), KS-797 (client_id/redirect_uri validation), KS-798 (consent form posts the wrong field — so the consent field's "MFA user can complete the flow on that page" condition is unsatisfiable at this SHA by anything in this PR; the field stays), KS-790, KS-782.

## 3. Scope
**Charter:** confirm closure of F-1/F-3/F-6/F-7/F-8/F-10 at `da901ffe1` with the first pass's own probes, and hunt what a fix round introduces: a schema that is stricter than login's on a shape login accepts (a regression in the other direction); normalisation applied at the route but a lockout INCREMENT still keyed differently on failure; a drift guard whose "verdict + class" reduction hides a real difference; a corpus of 9 rows that is 9 rows because the tenth would fail; a stub that now mirrors the product so faithfully it can no longer detect the product changing.

**In scope:**
- **F-1 — re-run probe-1 and probe-2 from the first pass against `da901ffe1`** (all six whitespace variants; the padded-victim case must now 401 and NOT reach the account; the lockout counter must INCREMENT on a padded failed attempt the same way it does on a clean one). State MEASURED.
- **F-1's other half — does the schema reject anything login ACCEPTS?** Compare `loginSchema` and the new authorize schema field by field (email transforms, mfaCode type/length, unknown keys). A user who can log in but cannot authorize with the same body is a new finding.
- **F-3 — the drift guard:** (i) confirm it exists and drives BOTH routes; (ii) re-derive its red-proof (remove a gate from one route → which rows redden); (iii) **probe the reduction**: construct a case where the two routes return the same CLASS but a materially different behaviour (e.g. same 401 class but one route increments lockout and the other does not; same MFA_REQUIRED but different body shape a client depends on) and say whether the guard can see it; (iv) what the corpus does NOT cover (platform admin by the builder's own admission; what else — tenant resolution, upgrade-on-verify rehash?).
- **F-6 / F-7:** re-run probe-2's non-string `mfaCode` case; confirm the openapi op now has a requestBody schema that matches the zod schema (not merely a schema); confirm `rateLimit('login')` is on the op AND is the same limiter login uses (name, not just presence).
- **F-8:** reconcile every stated set in the PR and mail against the 11-case + 9-row suites yourself.
- **Claim 4:** the `routes/auth.ts` hunk — read it, say what it is and whether login's behaviour moved.
- **The builder's stub retraction:** confirm the stubs now mirror the real key derivation, and — the sharper question — does mirroring the product in the stub mean a future change to the product's key derivation is invisible to the suite? Say so as a known-gap or a finding.
- **Full suite** on your by-SHA copy; numbers beside the builder's 354/29.
- **Palette:** zero new colour literals / CSS rules at the head, by diff (the consent field only).

**Out of scope / do NOT touch:** KS-790, KS-782, KS-795–KS-798 (next seat's work — read them for context only); the builder's tree, stack, `.env`; anything deployed; timing oracles beyond what a doubled harness can measure (say NOT RUN).

## 4. Credentials (POINTER ONLY — never values)
`/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.env` exists; you should not need it. Never echo a value.

## 5. State-mutation & cleanup
Exclude-and-report-only. Own `mktemp -d` per attempt, abandon not delete. **NEVER `rm`, anywhere — STANDING (Kam's rule).** Guard every expansion. Tampers on YOUR copies only, restored byte-identically with a hash.

## 6. Output boundary (fixed)
**Findings, reports and recommendations ONLY.** No changes of any kind anywhere. Fix-shapes in prose. (Kam ruling 2026-08-11, absolute.)

## 6a. Evidence class on every action-recommending finding (mandatory)
`MEASURED AT RUNTIME` · `PROBED` · `READ ONLY` — inline, in those words. A "still bypassable" finding carries its class in its first line.

## 7. Known-fragile / known-changed
- The first pass's own corrections: an invalid first red-proof that hit the harness (`require` under vitest ESM), an export gap, a retracted-then-narrowed F-6. Suspect your harness before the build.
- **Recent, do NOT flag as new:** #807, #800 merged; #806, #808–#811, #813 open; KS-793 (BACKLOG.md:7 stale) filed; KS-797/KS-798 filed from pass one.
- **Known open gaps carried:** F-9 platform-admin asymmetry (fail-closed); doors 2–3 unfixed (KS-795/796; door 2 is account-takeover-shaped — link path never reads `emailVerified`; two providers assert verification never established); KS-796 records the CIP-8 probe as NOT RUN and that `status` is never re-read on the wallet path.

## 8. Logistics
- **Time-box:** one bounded pass, smaller than the first — closure confirmation plus the introduced-defect hunt.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s125-ks781-regate-da901ffe1/report.md` + `evidence/`. F-1… with severity and evidence class; and a CLOSURE TABLE for the first pass's F-1/F-3/F-6/F-7/F-8/F-10 (CLOSED / PARTIAL / OPEN, with the probe that says so).
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-781 RE-GATE @ da901ffe1 (PR #812)` — BLUF, report path, the closure table, new findings by severity, NOT-TESTED, the branch head observed at the end.

---

PROVENANCE:
- #812 head da901ffe1a1e0cbc08129c27961abf605b623cca, 4 commits with subjects, 7 files with +/− counts, mergeable true | GitHub API /repos/Secuura/Distributed_Secuura/pulls/812, /files, /commits | read 2026-09-05
- The builder's claims 1–3, 5, the stub retraction, the door-2 provider table, the KS-796 note | builder's mail `[Secuura/Blockchain -> Wednesday] READY FOR RE-GATE: #812 @ da901ffe1 — F-1 closed, and the drift guard I claimed now exists …` at wednesday-agent@agentmail.to, 2026-09-04T23:40:11Z | read 2026-09-05
- The first pass's findings F-1…F-10 and its probes | `projects/secuura/reports/2026-09-05-s125-ks781-oauth-authorize-mfa-gate/report.md` and its mail 2026-09-04T23:26:18Z | read 2026-09-05
- KS-797 (blocks KS-790) and KS-798 (related KS-782) filed, P2/High; KS-795/KS-796 the sibling sub-issues | Linear GraphQL, team KS, createdAt > 2026-09-04T23:20Z | read 2026-09-05
- The builder is being rotated at this boundary | Wednesday's daily note 2026-09-05 (10:2x checkpoint) — Wednesday's project, not the QA project's | read 2026-09-05
