# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), KS-800 FIRST PASS: PR #817 @ `010bbc8fa` — close the parser/guard class, and a corpus defined by STRUCTURE (a file that calls `express()`) instead of by filename

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context — the remainder of KS-781 P3-3, and a guard that was green while two services were unguarded
#812 (KS-781 door 1, merged 04:34Z) fixed five out-of-order global body-parser mounts and shipped a class guard (LEG C, a corpus count). The fourth pass (`projects/secuura/reports/2026-09-05-s127-ks781-regate4-a5542df5a/`) found Q4-2: handler-passed parsers on 19 admin routes, `mcp-server` unguarded, `proxy.ts` latent — and KS-800 was WIDENED for it. **This branch's thesis is that the guard's corpus was a LIST OF FILENAMES (`index.ts` → `{index,app,server}.ts` after misses) and that an unguarded service returned `null` from `scan()` and was therefore INVISIBLE rather than red.** A THIRD Secuura QA seat (KS-796 on #816) is running concurrently — own copy, own ports; never touch its tree or surfaces.

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` — the builder (s128) is LIVE in that tree with the Docker stack on `:6882`. Never check out, stash or modify anything there; take your subject from the git objects into your OWN copy.
- **Subject:** **PR #817 head `010bbc8fa`**, base `develop` `3ccf52f09`, **ONE commit ahead, 0 behind, mergeable clean — 5 files +384/−10** (GitHub API, read by Wednesday at 15:4x AEST): `packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts` +327/−9 · `packages/shared/src/middleware/index.ts` +38 · `services/api-gateway/src/middleware/contentType.ts` +6 · `services/demo-service/src/app.ts` +8 · `services/mcp-server/src/http-server.ts` +5/−1. Peter requested, no review.
- **Running target:** by-SHA copy with the packages' own harnesses (vitest in `packages/shared`; `api-gateway`). Full-stack through `:6882` is off-limits. Doubled dependencies stated. LEG G is claimed "over a real socket" — measure it as such in your copy.
- **Production?** NO. Nothing deployed; no call leaves the machine.

## 2. The builder's claims at `010bbc8fa` — inputs to FALSIFY (the commit body, read by Wednesday from the object; s128's READY mail 05:41:40Z)
1. **Blind spot 1:** `scan()` returned `null` for a file with no guard mount, so `demo-service` and `mcp-server` (parse bodies, mount NO guard) were dropped from the corpus, not failed — every leg green with two services unguarded. **LEG E** makes absence a failure, with a NON-VACUOUS companion assertion (RP-2: with the extractor stubbed to `[]`, LEG E's main assertion PASSED — a service with no detected parser cannot be unguarded).
2. **Blind spot 2:** the corpus was a name list; Wednesday's "widen to router modules" followed literally would have been the third instance (it still missed `mcp-server/src/http-server.ts`; the builder's own new LEG F caught it and mislabelled it). **An entrypoint is now a file that calls `express()` — an AST question.** Measured: name list **22**, structural **24**.
3. **The instrument:** grepping raw lines for `express.json(` returns **7 files, only 3 real** — `contentType.ts`, `auth.openapi.ts`, `routes/mfa.ts`, `referral/middleware/errorHandler.ts` DISCUSS it in doc comments; the legs walk the TypeScript AST (a comment cannot produce a `CallExpression`), and a **named control** asserts those four are clean AND still contain the string.
4. **Changes:** `demo-service` and `mcp-server` mount `rejectNulBytes()` after the parser (both Dockerfiles already build and symlink `packages/shared`); `@secuura/shared` exports `mountBodyParsers(app)` (json, urlencoded, guard, in the one order); the guard's doc comment corrected ("mount immediately after express.json()" told people to get it wrong); **LEG E** (guard presence), **LEG F** (parsers outside an app-creating file, bounded by a declared set), **LEG G** (`mountBodyParsers` proven over a real socket, both content types, with a clean-body case).
5. **Red-proofs, predicted first:** RP-1 remove `demo-service`'s guard → LEG E fails naming `['demo-service']` + LEG C 23 vs 24 — exact; **but predicted 39 passed, got 38: `it.each(SCANS)` makes the suite total DATA-DEPENDENT** (dropping a guard drops a generated test). RP-2 stub `parserCallLines()` → exactly 3 failures, 38/41 — exact.
6. **Runner lines:** `packages/shared` 35 files / 547 tests · `api-gateway` 22 / 213 · `demo-service` build rc 0 · `mcp-server` build rc 0 · preflight 12/12.
7. **NOT DONE, stated:** the three api-gateway route-scoped sites stay HELD by the declared set, not fixed; migrating all 24 services onto `mountBodyParsers(app)` is deliberately out (its own ticket if wanted); the four platform suites NOT run on this branch.

## 3. Scope
**Charter:** falsify claims 1–6 at `010bbc8fa`, then hunt what a STRUCTURAL corpus and a DECLARED exclusion set can each still miss.

**In scope:**
- **The corpus, re-derived:** enumerate every file in `services/` that calls `express()` by YOUR OWN AST walk (or a second independent method) — number beside 24; and every file that mounts a body parser (`express.json`/`express.urlencoded`/`bodyParser.*`/a handler-passed parser) — is every one of those either inside an app-creating file with the guard AFTER it, or inside LEG F's declared set? **A parser call the corpus cannot see is the finding; a member of the declared set that is not actually route-scoped is a finding too** (the set is an exclusion — a recorded exclusion is a claim).
- **LEG E's companion (non-vacuity):** stub the extractor yourself → LEG E's main assertion must go GREEN (reproduce RP-2) and the companion must go RED; then the perimeter: a service that mounts the guard BEFORE the parser (wrong order), a service that mounts the guard on a sub-router only, a service that mounts `rejectNulBytes` under a different import alias — which does each leg see?
- **The parameterised-suite count:** reproduce RP-1 predicting the count and the cases SEPARATELY (39 vs 38) — the builder's keeper; state whether any other assertion in the file reads the total as a constant.
- **The doc-comment control:** confirm the four discussed-only files are clean by AST and still contain the string; then plant a REAL `express.json()` call inside a doc-comment-heavy file in your copy → the AST leg reds, the grep would have been noise either way.
- **LEG G over a real socket:** both content types, NUL refused, clean body accepted, in your copy; confirm the socket is real (a port, a listener), not a supertest double, if that is what "real socket" claims.
- **The two services' mounts:** `demo-service/src/app.ts` and `mcp-server/src/http-server.ts` — the guard is mounted AFTER the parser and BEFORE any route that reads a body; a NUL through each service's own app (harness-level) is refused; the import resolves in a `node` process the way the Dockerfile symlink claims (READ the Dockerfiles; do not build images).
- **Red-proof:** re-derive RP-1 and RP-2 independently with the sets predicted before running; all cases EXECUTED.
- **Suites:** `packages/shared` and `api-gateway` in your copy, numbers beside 35/547 and 22/213; the four platform suites if reachable without the stack, else NOT RUN with your own read of whether five files in shared + two services could affect them.
- **Palette:** zero colour literals by diff (expect zero).

**Out of scope:** KS-796/#816 (the other QA seat), KS-795, KS-802, KS-804 (the authorize four-rules resolver — context only), the api-gateway route-scoped sites' FIX (held by design), the 24-service migration, the builder's tree/stack, anything deployed.

## 4–6. Credentials / state / boundary
`.env` exists; you should not need it; never echo. Exclude-and-report-only; own `mktemp -d`; **NEVER `rm`**; tampers on your copies only, restored byte-identically with hashes; **predict every tamper's failing SET (and, in a parameterised suite, its COUNT separately) before running.** **Findings, reports and recommendations ONLY** (Kam 2026-08-11). Evidence class on every row.

## 7. Known-fragile / carried
The KS-781 passes' traps stand: a control copied from the working tree is not a control (take the parent's files from the git blob); a harness without the errorHandler 500s everything; **a cheap textual extractor standing in for a parser is the fleet's fourth-instance family this week — the builder chose an AST for that reason; your job is to find where the AST's own predicate (`express()` call = entrypoint) is blind: an app created by a factory (`createApp()`), an `express()` call in a test helper that is not a service, a service whose app is built in a package the corpus does not walk.**

## 8. Logistics
- **Time-box:** narrow — the corpus re-derived two ways, LEG E's non-vacuity + perimeter, the parameterised count, the doc-comment control, LEG G on the socket, the two services' mounts, the red-proofs.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s128-ks800-parser-guard-corpus-010bbc8fa/report.md` + `evidence/`. Claims table (claimed → measured); new findings by severity with evidence class; NOT-TESTED.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] KS-800 PASS 1 @ 010bbc8fa (PR #817)` — BLUF (PASS or NO GO in the first line), report path, claims table, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- #817 head 010bbc8fa, base develop 3ccf52f09, 1 ahead / 0 behind, mergeable clean, 5 files +384/−10 with per-file +/−, Peter requested | GitHub API `/pulls/817` + `/compare/3ccf52f09...010bbc8fa`, read-only, token sourced transiently from the project's `.env` and never printed | read 2026-09-05 15:44
- Claims 1–7 | the commit body of `010bbc8fa` (`git log -1 --format=%B`, local object, no fetch) + the test file's `describe`/`it` names (`git show 010bbc8fa:<path>`) — the builder's own words; s128's READY mail 2026-09-05T05:41:40Z (RP-1's 39→38, RP-2's 38/41, the runner lines) | read 2026-09-05 15:44
- Q4-2 and the widening of KS-800 | `[QA -> Wednesday] KS-781 RE-GATE (4) @ a5542df5a (PR #812)` 04:30:58Z and s127's wrap 04:43:34Z, as recorded in Wednesday's note | read 2026-09-05 14:3x
- The concurrent KS-796 QA seat (`%11`) | Wednesday's own launch record 15:2x — Wednesday's project | read 2026-09-05 15:44
- s128 live with the stack on :6882 | `lsof` (docker on 6882) — Wednesday's seat | read 2026-09-05 15:1x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 15:44
(checked: "the declared set holds the route-scoped sites" against "a member of the declared set that is not route-scoped is a finding" — the set is accepted as a design and tested as a claim; "24 by AST" against "re-derive two ways" — the tester's number is independent of the builder's method; "LEG G real socket" against "no full-stack" — a socket in the tester's copy, never the builder's :6882; stated.)
