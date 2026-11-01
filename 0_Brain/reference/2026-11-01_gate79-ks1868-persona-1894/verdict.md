# QA Gate 79 verdict: Secuura/Distributed_Secuura PR 1894 (KS-1868, demo-service persona switch O43-P1), TIER 1

All log paths are relative to `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate79-ks1868-persona-1894/`.

## BLUF

**GO WITH NOTES**

The change is the guarded read of the thrown value with a constant fallback, nothing else. The catch still answers the same fixed generic 500. No auth outcome changes, and no secret, token, cookie or upstream error text reaches the response. Red-first held: 2 of 3 failed by AssertionError at base, and 3 of 3 passed at head. 12 of 13 mutants were killed, including the one that echoes the thrown message. The one survivor sits on an unchanged line. Suite: 12 files / 94 of 94 at base, 13 files / 97 of 97 at head. tsc: 25 errors at both, byte-equal. merge-tree rc 0. The fragment check passes, and all 5 planted defects were caught. None of the notes blocks the PR.

## Heads

- START (logs/head_start.log, 11:47:44Z): PR head `3a88693f70d308b06905a04ead12872cb837153e` (local ref and ls-remote equal the expected sha); develop `d7691f35312ea158f043e87a3227e477cccb183d`. The head's parent is that develop sha, and develop..head holds 1 commit. 4 files, +144/-1.
- END (logs/head_end.log, 11:54:16Z): the same two shas by ls-remote. Local HEAD is the PR head, and the working tree is clean (0 status lines).
- Clone setup (logs/setup.log): origin `git@github.com:Secuura/Distributed_Secuura.git`, push url `no_push_qa_gate`, core.sshCommand set as briefed, fetch rc 0. Note: git ignored `--filter=blob:none` on the local-path clone and said so, so the clone is full.

## FINDINGS

- **G79-F1 LOW (test gap, unchanged line):** `Blockchain/Dev/services/demo-service/src/routes/persona.ts:79`. Mutant M10 changes the `'Unknown error'` branch (a readable non-Error thrown value, such as a thrown string) to `'unreadable thrown value'`, and it SURVIVED: rc 0, 3 of 3 passed. No cell throws a readable non-Error value, so the PR's claim that this branch is unchanged rests on reading the diff, not on a test. Log: logs/mut_M10.log, logs/mutants_summary.log.
- **G79-F2 INFO (pre-existing, not introduced, no live trigger found):** `persona.ts:61-63` and `:76-84`. If anything throws after `res.setHeader('Set-Cookie', …)`, the catch's generic 500 still carries the upstream refresh-token cookie. The catch does not clear headers. A probe on the real router (user carrying a BigInt, so `res.json` throws at `:65`) got `HTTP 500`, `set-cookie "refresh_token=RT_SECRET; HttpOnly"` and the generic body. The browser would therefore get a session cookie on a response that reports failure. The base and head catches are identical here. Reachability today: `authResult.user` comes from `response.json()` (authClient.ts:53-58), which always serialises, so I found no real producer. Logs: logs/probe_setcookie_on_500.out, logs/probe_setcookie_on_500_run2.log (probe source at scripts/zz-gate79-probe2.test.ts.ran; it was never left in the tree).
- **G79-F3 INFO (reachability of the fixed path):** `authClient.ts:28-69`. `authenticatePersona` catches everything and returns a structured result. Its own catch at `authClient.ts:62` has the same unguarded read, which is another KS-1868 site, untouched here. That read can throw only a readable TypeError. So no producer has been identified that sends an unreadable value to the catch at `persona.ts:76`. The new test reaches it only by mocking `authenticatePersona` to reject with the value directly. The author's mail says the same. Log: logs/source_read.log, plus the source read in this verdict (section 1).
- **G79-F4 INFO (the fragment understates the base behaviour):** the flow fragment says the base handler "rejected instead of logging and answering". Under Express 4.22.3 on Node v26.8.1 that rejection is unhandled. demo-service installs no `unhandledRejection` handler (git grep count 0), so the whole process exits with code 1. It does not hang, and neither Express's default handler nor the service's errorHandler is reached. Emulation of the base catch: `PROCESS EXIT code 1`, uncaught TypeError, no HTTP response. The head emulation answered `HTTP 500` with the generic body and exit 0. So the fix removes a crash shape, if that shape is reachable (see F3). Logs: logs/emul_base.log, logs/emul_head.log, logs/express_layer_read.log.
- **G79-F5 INFO (pre-existing, unchanged):** `persona.ts:83` logs `err.message` of an ordinary Error, before and after the change, and `authClient.ts:43,63` log the persona email. Neither the message nor the email ever reaches a response. The log is not touched by the PR (mutant M11 confirms that cell C1 pins the logged value). Log: logs/source_read.log, logs/mut_M11.log.
- **G79-F6 INFO:** `docs-fragments.mjs check` on the head prints two ADVISORY lines (flow line 6249, cheat line 6235). Develop prints the same two at the same lines, so they predate this PR. Logs: logs/frag_check_clean.log, logs/frag_check_base.log.

## 1. Security read at source

**The handler at head** (`persona.ts:37-86`), read from the checked-out head and compared with develop through `git show` (logs/checkout_and_diff.log):
- `:39-46`: zod `safeParse` of `req.body.persona` against the enum alice/sarah/bob/admin. A failure answers 400 with the zod issues, which echo only the caller's own input.
- `:48-53`: looks up `PERSONAS[key]` and calls `authenticatePersona(persona.email, persona.password)`, a server-side credential. `:51` logs only the persona key.
- `:55-58`: when `success` is false, logs the persona key and `authResult.error` (status text such as `Auth service returned 401`, or a fetch error message) and answers a fixed 502 `Persona auth failed`.
- `:61-63`: proxies the upstream `set-cookie` (the httpOnly refresh_token) with `res.setHeader`.
- `:65-75`: 200 carrying `accessToken`, `user` and persona display fields. Returning the token on success is the route's purpose (it mints real tokens, see the guard below).
- `:76-85`, the catch: BEFORE, `const message = err instanceof Error ? err.message : 'Unknown error'`. AFTER, the same expression inside an inner try, with `catch { message = 'unreadable thrown value'; }`. Then it logs `'Persona switch error', { error: message }` and answers `500 {success:false, error:{code:'INTERNAL_ERROR', message:'Internal server error'}}`.

**Is the change only the guarded read with a constant fallback?** Yes. The diff for persona.ts is +6/-1: the declaration is split into `let`, wrapped in try, and given the constant fallback. The log text, the log level, the status, and the 500 body are byte-identical (logs/checkout_and_diff.log).

**Secrets in the response or the log:** before and after, the 500 body is a constant. The thrown message reaches only the log (F5, unchanged). No credential, password, token or cookie is logged on this path. The one header exposure is pre-existing and unchanged: F2.

**Could the change alter the auth outcome?** No. The change is entirely inside the catch, after the try has already failed. Every path through the new code ends at the same `res.status(500)` with `success:false`. It cannot reach the 200 branch, set a cookie, or return a token. Mutants confirm the tests would catch such a regression: M5 (200 instead of 500), M6 (`success:true`), M12 (accessToken in the catch body) and M3 (echo of the thrown message) were all KILLED (logs/mutants_summary.log).

**BEFORE, for an unreadable thrown value:** Express 4.22.3 `Layer.prototype.handle_request` (`node_modules/express/lib/router/layer.js:86-99`) calls `fn(req, res, next)` inside a synchronous try/catch and drops the returned promise (logs/express_layer_read.log). The async handler's rejection therefore never reaches `next(err)` or any error middleware. It is an unhandled rejection, and with no `unhandledRejection` or `uncaughtException` handler in demo-service (git grep: none; logs/source_read.log), Node v26.8.1 terminates the process. Emulated with the repo's express and the verbatim base catch: exit code 1, no HTTP response (logs/emul_base.log). Answer: **crash**, not a hang and not Express's default handler. See F4.

**Callers and mount point** (git grep at HEAD, logs/source_read.log):
- `services/demo-service/src/app.ts:24` imports it, and `app.ts:74` mounts it with `app.use('/demo-api', personaRouter)`, after `requireDemoKey` at `app.ts:72`. The route is therefore behind the shared demo key; only `/health` (`:67`) is mounted before the key.
- Route `persona.ts:37`, `POST /persona/switch`, giving `POST /demo-api/persona/switch`.
- Client: `frontend/demo-overlay/src/api/demoApi.ts:28` (doc comment at :24); response type `frontend/demo-overlay/src/types/persona.ts:62`.
- Gateway comment: `docker/nginx-gateway/nginx-demo.conf:353`. Config doc: `env.example:423`. OpenAPI: `demo-service.openapi.ts:11,89`. Guard docs: `middleware/demoGuard.ts:6,29`.
- Tests: `__tests__/persona.test.ts:13,33,77,106,132`; `__tests__/demoGuard.test.ts:62,67,95,124`; the new test at :22,29-30.

## 2. Red-first and mutants

**Red-first.** Base product: develop's persona.ts (sha256 `fe73200e…c9e0`) copied over the head file, with the new test run against it (logs/red_base_swap.log, logs/red_base.log). Result: rc 1, **2 failed and 1 passed out of 3**. R1 and R2 failed with `AssertionError: expected true to be false` (the handler threw), and the control C1 passed. Restored with `git checkout HEAD -- persona.ts`, and sha256 `5d5b25ee…dec8` checked OK (logs/red_base_swap.log, logs/persona_head.sha256).

**Head:** rc 0, **3 of 3 passed** (logs/green_head.log).

**Mutants** on the hunk and the catch around it. Each mutant ran only the new test file and was restored, with the sha256 checked after each one. Final sha OK (logs/mutants_summary.log, per-mutant logs at logs/mut_M*.log, script scripts/mutants.py):

| id | mutant | result | restore |
|---|---|---|---|
| M1 | inner try removed (base read restored) | KILLED (2 failed, 1 passed of 3) | sha OK |
| M2 | fallback constant -> 'Unknown error' | KILLED (2 failed, 1 passed) | sha OK |
| **M3** | **catch ECHOES the thrown message in the 500 body** | **KILLED (3 failed of 3)** | sha OK |
| M4 | inner catch rethrows | KILLED (2 failed, 1 passed) | sha OK |
| M5 | catch answers 200 instead of 500 | KILLED (3 failed) | sha OK |
| M6 | catch body success:true | KILLED (3 failed) | sha OK |
| M7 | inner catch answers 500 without logging | KILLED (2 failed, 1 passed) | sha OK |
| M8 | log level error -> warn | KILLED (3 failed) | sha OK |
| M9 | fallback = String(err) | KILLED (2 failed, 1 passed) | sha OK |
| M10 | non-Error branch 'Unknown error' -> 'unreadable thrown value' | **SURVIVED** (3 of 3 passed): G79-F1 | sha OK |
| M11 | log carries the raw thrown value | KILLED (3 failed) | sha OK |
| M12 | catch leaks a session: accessToken in the 500 body | KILLED (3 failed) | sha OK |
| M13 | catch swallows: no response sent | KILLED (3 failed) | sha OK |

12 of 13 were killed. The required echo mutant, M3, was killed.

## 3. demo-service whole suite and tsc

- Setup: `npm ci --ignore-scripts` at the `Blockchain/Dev` workspace root, rc 0, 1795 packages (logs/npm_ci.log). `packages/shared` built with tsc, rc 0 (logs/build_shared.log). Node v26.8.1, vitest 4.1.12, express 4.22.3 (logs/express_layer_read.log, logs/suite_head.log).
- Runner: scripts/vt.sh, at nice 10 with `--maxWorkers=2`. It waits while load1 > 20. **No wait happened.** Load1 at start was 14.72 at most and 7.77 at least (the `start` line of each log), and no log contains a `WAIT` line.
- Base (develop persona.ts, new test excluded): **12 files / 94 of 94 passed**, rc 0 (logs/suite_base.log; swap and restore sha in logs/suite_base_swap.log).
- Head: **13 files / 97 of 97 passed**, rc 0 (logs/suite_head.log).
- tsc including tests (`--noEmit`, config scripts/tsconfig.gate79.json, which extends the service tsconfig without the `__tests__` exclude):
  - Base (develop persona.ts, new test parked outside the tree): **25 errors**, rc 2 (logs/tsc_base.log).
  - Head: **25 errors**, rc 2 (logs/tsc_head.log).
  - The two error lists are byte-equal: `diff` rc 0 (logs/tsc_diff.log). They fall in demoGuard.test.ts (6), persona.test.ts (8) and reset.test.ts (11). There are 0 errors in the new test or in routes/persona.ts (logs/tsc_newfile_check.log, positive control 25). This matches the author's figure of 25.

## 4. merge-tree

`git merge-tree --write-tree refs/gate/develop refs/gate/pr1894`: **rc 0**, tree `7a9447da42f8a99390a386090f60d6600c8347a2`, which equals the head's own tree because develop has not moved past the base (logs/merge_tree.log).

## 5. Fragment pair

Files: `Projects Documents/fragments/{flow,cheat}/KS-1868-demo-service-persona-switch-unreadable-thrown-value.html`.

- `node Blockchain/Dev/scripts/docs-fragments.mjs check --root <clone>` on the head: **rc 0**, "flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes html_docs_check", with two ADVISORY lines that predate this PR (F6) (logs/frag_check_clean.log). Develop gives the same result with 48 new and the same advisories (logs/frag_check_base.log).
- Planted defects. Each was restored by sha256 (flow `697a0ff3…635c`, cheat `4580e2d4…25d2`), and the check after restore is rc 0 (logs/frag_summary.log, logs/frag_check_after.log, script scripts/frag.py):

| plant | rc | output |
|---|---|---|
| P1 flow unclosed div | 1 | FAIL, 1 finding (logs/frag_P1_flow_unclosed_div.log) |
| P2 flow literal number instead of `<!--n-->` | 1 | FAIL, 2 findings (logs/frag_P2_flow_literal_number.log) |
| P3 cheat unclosed div | 1 | FAIL, 1 finding (logs/frag_P3_cheat_unclosed_div.log) |
| P4 cheat carries an `<!--n-->` token | 1 | FAIL, 1 finding (logs/frag_P4_cheat_carries_n_token.log) |
| P5 flow second entry in one file | 1 | FAIL, 1 finding (logs/frag_P5_flow_two_entries.log) |

The fragment figures (2 of 3 red, 94 to 97, 25 tsc errors, 1795 packages) match my runs. On the wording, see F4.

## 6. END heads

See ## Heads: PR head `3a88693f70d3…` and develop `d7691f35312e…`, both unchanged by ls-remote at 11:54:16Z (logs/head_end.log).

## NOT TESTED

- A real authentication failure, or any request, against a booted demo-service with the real auth service. The Express behaviour in F4 comes from an emulation of the catch shape with the repo's express, not from the real `persona.ts` under a real server.
- Whether any production producer can send an unreadable value to `persona.ts:76` (F3). None was found by reading the code; none was exercised.
- eslint (the author claims 0 and 0; not re-run).
- The four platform suites (Schemathesis, Akto, Playwright, k6), any LTS Node (only v26.8.1 was used), and any deploy.
- The other KS-1868 sites, including `authClient.ts:62`.
- The pre-push hook legs and the author's push receipt (taken from the READY mail, unverified, apart from the head sha, which matches).
- Overlap with other open PRs: not checked. Develop has not moved, and merge-tree against develop is clean.
