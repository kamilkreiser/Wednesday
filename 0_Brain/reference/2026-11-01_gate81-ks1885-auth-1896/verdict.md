# QA Gate 81 verdict: Secuura/Distributed_Secuura PR 1896 (KS-1885, social callback exchange-error echo), TIER 1

## BLUF

**GO WITH NOTES**

The code does what the approved design says. I found no path in the callback or the link route that puts a token, a provider body byte or an unauthored error text into the 400/500 body, the new warn lines, or errorHandler's `err.message`/`err.stack` log. The anchored allowlist held against 12 bypass probes, including newline (LF, CRLF, U+2028, U+2029), NUL and digit-shape smuggles. Statuses are unchanged. The notes are about the tests, not the product. The author's 72 cells do not kill two of my hostile mutants, the `m` flag and a widened status group, which only my own probe file killed (G81-F1). One mutant (`cause` on F3's neutral Error) is equivalent under today's sinks (G81-F2).

## Heads

| | START (logs/head_start.log, 12:19:26Z) | END (logs/head_end.log) |
|---|---|---|
| PR 1896 head (ls-remote) | `5914d69aaa9c8bb5bfbff8c9689326f6b243e28d` = expected | `5914d69aaa9c8bb5bfbff8c9689326f6b243e28d` (unchanged, 12:38:14Z) |
| develop (ls-remote) | `d7691f35312ea158f043e87a3227e477cccb183d` | `d7691f35312ea158f043e87a3227e477cccb183d` (unchanged) |
| head^ | `d7691f35312ea158f043e87a3227e477cccb183d` (one commit, `rev-list --count` = 1, logs/diff_numstat.log) | |

The diff is 5 paths, exactly as briefed: auth.ts 55/6, tests 291 and 253, fragments cheat 17 and flow 11 (logs/diff_numstat.log).

## FINDINGS

- **G81-F1 (NOTE, test gap; the product is correct).** The PR's central control is that the allowlist is anchored and single-line. The author's cells pin that only against a token joined by a SPACE (`...(HTTP 400) <token>`, `<token> GitHub...`). Two hostile mutants survive all 72 author cells:
  - **G2**: the `m` flag added to both regexes.
  - **G12**: the status group widened `HTTP \d{3}` to `HTTP [^)]*`.
  Both are killed only by my gate81-probe cells. G2 falls to `adapter text\n<token>` (the exact smuggle in the brief), which would put the token in the 400 body and in errorHandler's log. G12 falls to `(HTTP 400 <token>)` and to a 4-digit status. Evidence: logs/mutants.log, logs/mut_G2_m_flag.log, logs/mut_G12_status_group_widened.log. Suggested follow-up (author's call, not a blocker): add a newline-smuggle cell and a widened-status cell to `ks1885-exchange-error-allowlist-is-exact.test.ts`. scripts/gate81-probe.test.ts has ready-made shapes.
- **G81-F2 (NOTE, equivalent mutant).** **G9** adds `{ cause: exchangeErr }` to F3's neutral `Error`. It survives every cell, mine included (logs/mut_G9_link_neutral_error_with_cause.log, 92/92). It is equivalent today: errorHandler logs only `err.message` and `err.stack`, and V8's `stack` string does not include `cause`. So the eslint-disable's reason is real defence-in-depth against a future sink that serialises the error object, but no test observes it. The disable is necessary: removing it raises `preserve-caught-error` at auth.ts:1409 and eslint exits 1 (logs/eslint_planted.log).
- **G81-F3 (NOTE, pre-existing, out of this PR's scope).** Provider body bytes still reach a log line, by KS-1240's design, in the adapters, not in the code this PR touches.
  - On a non-OK token answer: `body: (await tokenRes.text()).slice(0, 200)` (for example providers/social/github.ts:82, and apple.ts:83).
  - `tokenBody.error.slice(0, 80)` at github.ts:90.
  These are bounded and are error bodies, not an issued access token. This answers Q1's "any log line" literally: yes, but not through this PR's path.
- **G81-F4 (NOTE, residual, not reachable today).** `exchangeErrorName` logs any name matching `^[A-Za-z][A-Za-z0-9_]{0,63}$`. A GitHub-style token (`gho_` followed by 36 alphanumerics) is identifier-shaped, so a future adapter that set `err.name` from provider data would log it. I read every adapter at source (github, google, linkedin, microsoft-personal, facebook, apple): none sets `name`. The only names reaching the catch come from the runtime (`TypeError`, `SyntaxError`) or from `Error`/AppError subclasses.
- **G81-F5 (NOTE, behaviour change, an improvement).** For a hostile thrown value (a Proxy whose `message`/`name` reads throw), `POST /social/link` answered 500 with a non-JSON body at base: errorHandler itself threw on `err.message`, so Express's default handler answered. At head it answers a JSON `500 INTERNAL_ERROR`, because the trap's own Error reaches errorHandler instead (probe cell "hostile Proxy": × at base, ✓ at head; logs/probe_base.log, logs/probe_head.log). The status is unchanged. No provider can produce this value.

## 1. Security read (source, before and after)

**Callback (`GET /social/:provider/callback`, auth.ts:1047ff at head).**
- *Before:* `exchangeErr?.name === 'SyntaxError' ? constant : exchangeErr?.message || 'invalid authorization code'` went into a `BadRequestError`, so any other message (fetch's `TypeError` quoting `Bearer <token>`, V8's null-deref text, Apple's id_token `JSON.parse` text) reached the 400. Because errorHandler logs every error's `message` and `stack`, it also reached the error log.
- *After:* `authoredExchangeText` passes a text only for (a) `instanceof AppError`, or (b) a string `message` that fully matches one of two regexes. Everything else gets the KS-1791 constant. The new `BadRequestError` is built from authored text only, so its `message` and `stack` (which reproduces only that message) are clean in errorHandler's log at :265-270. The new warn line carries `{ provider: providerName (validated by isValidProvider), errorName }` and never the message.

**Link (`POST /social/link`, :1385ff).**
- *Before:* a raw `exchangeCode` rejection went to errorHandler, which logged its `message` and `stack`, token included. The client got 500 generic, or an AppError's status and text.
- *After:* authored errors are rethrown unchanged. That is a 503 AppError, or a plain adapter `Error` that becomes 500 with its authored text in the log. Anything else is logged by name only and replaced by `new Error('social link: the provider code exchange failed')` with no `cause`. My probe confirms the client body is byte-identical: `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}`.

**Regex bypass.** Both patterns are anchored `^…$`, with no `m`, `g` or `s` flags. In JS, a `$` without `m` matches only at end of input; unlike PCRE or Python, it does not also match before a final newline. `\d` without `u` is ASCII-only, and `.test` on a non-global regex keeps no `lastIndex` state. Probed through the real route and errorHandler (scripts/gate81-probe.test.ts):
- At head, 20/20 green (logs/probe_head.log), with the token in no body and no log line. The probe shapes:
  - `GitHub token exchange failed (HTTP 400)\n<token>`
  - token, then LF, then adapter text
  - CRLF, U+2028, U+2029, NUL
  - the profile texts plus LF
  - a trailing LF only
  - `(HTTP 400 <token>)`
  - a 4-digit status
  - Arabic-Indic digits
  - a 65-char name (logs `unnamed`)
  - a name with an embedded LF
  - three repeated PIN calls (no `lastIndex` drift)
  - five link-route shapes
- At base, 18 of 20 fail (logs/probe_base.log). For example, the LF smuggle echoed `"OAuth authentication failed: GitHub token exchange failed (HTTP 400)\nG81SMUGGLEDzq9x4"` in the body and in errorHandler's `error` and `stack` fields. The 2 that pass at base are the `lastIndex` repeat and the link thrown-string cell.

**Is AppError text provider-controlled?** No. The only AppErrors the adapters throw from `exchangeCode` are `ServiceUnavailableError` with fixed literals ("<Provider> did not answer in time; please try again.", "... could not be reached; ..."), at github.ts:57-58 and the same lines in each adapter. The plain-Error adapter texts interpolate only `tokenRes.status` / `profileRes.status`, a fetch status number. Nothing else in the exchange path constructs an AppError.

**Auth outcomes and statuses.**
- Callback: every exchange failure is still `400 BAD_REQUEST` (the base red cells show identical status and code; only the text differed, logs/base_red_new_tests.log). A hostile value is 500 at both.
- Link: the same statuses (500, or the AppError's own).
- Success paths are untouched (the author's CONTROL normal sign-in answers 200 and mints).
- The text changes are intended: a thrown string or empty message now gets the constant instead of "invalid authorization code".

Out of scope, noted only: `Unknown social provider: ${providerName}` reflects the caller's own path or body value (pre-existing; not a token or a provider byte).

## 2. Red-first and mutants

- **Base** (product at d7691f35, the two new files copied in), logs/base_red_new_tests.log: `Tests 20 failed | 52 passed (72)`, rc=1.
  - All 20 failures are RED-labelled cells; 0 non-RED cells fail, and 0 RED cells pass (logs/base_red_summary.log).
  - Failure kind: AssertionError only, with 0 TypeError/ReferenceError/SyntaxError lines, so all 20 are red by assertion.
- **Head**, logs/head_new_tests.log: `Test Files 2 passed (2) / Tests 72 passed (72)`, rc=0. (My first head attempt failed to resolve `@secuura/shared` before packages/shared was built; that is setup, not product. It was re-run after logs/shared_pkg_build_head.log.)
- **My mutants**: 16, run by scripts/mutants.py on wt_head auth.ts against the author's 2 files plus my probe. Each pattern was asserted to match exactly once, and the file was restored by sha256 after every mutant (final `eb3b3e16…a89e` = original, logs/mutants.log).

| Mutant | Result | Killed by |
|---|---|---|
| G1 both anchors dropped | KILLED | author (allowlist) + probe |
| **G2 `m` flag added** | **KILLED, probe only** | gate81-probe (9 cells), G81-F1 |
| G3 AppError clause widened to `instanceof Error` | KILLED | author (both files) + probe |
| G4 callback warn includes the message | KILLED | author (both) + probe |
| G5 link warn includes the message | KILLED | author (allowlist) + probe |
| G6 `$` anchors dropped | KILLED | author + probe |
| G7 `^` anchors dropped | KILLED | author + probe |
| G8 link always rethrows raw | KILLED | author + probe |
| **G9 link neutral Error with `cause`** | **SURVIVED (equivalent)** | none, G81-F2 |
| G10 `typeof` check dropped (String(message)) | KILLED | author (allowlist) |
| G11 errorName unbounded | KILLED | author + probe |
| **G12 status group `HTTP [^)]*`** | **KILLED, probe only** | gate81-probe (3 cells), G81-F1 |
| G13 empty or other text falls back to message / "invalid authorization code" | KILLED | author (both) + probe |
| G14 `g` flag (lastIndex state) | KILLED | author (both) + probe |
| G15 callback status 502 | KILLED | author (both) + probe |
| G16 link catch reduced to a rethrow | KILLED (duplicate of G8) | author + probe |

Per-mutant logs: logs/mut_G*.log. Tally: 15 of 16 killed, 13 of them by the author's cells. G2 and G12 were killed only by my probe, and G9 is equivalent. I did not re-run the author's own 13 mutants. Their list in the flow fragment ("each regex anchor dropped", "the message added to the warn", and so on) overlaps my G1/G4/G6/G7/G8/G10, which agree.

## 3. Auth whole suite, neighbours, tsc, eslint

Setup: `npm ci --ignore-scripts` at Blockchain/Dev in both trees, rc=0, 1795 packages (logs/npm_ci_head.log, logs/npm_ci_base.log). `@secuura/shared` (packages/shared) build rc=0 (logs/shared_pkg_build_*.log). services/shared (@secuura/service-utils) was also built, rc=0 (logs/shared_build_*.log). Runs used vitest 4.1.12 on Node v26.8.1, with cwd services/auth (via `npm --prefix … run test -- run`), nice 10, maxWorkers=2, and a wait while load1 > 20 (scripts/vt.sh).

- **Head, `--testTimeout=30000`** (logs/head_whole_t30000.log): `Test Files 119 passed (119) / Tests 1457 passed (1457)`, rc=0. This matches the author's 1457/1457.
- **Head, default timeout** (logs/head_whole_default_timeout.log): `Test Files 119 passed (119) / Tests 1457 passed (1457)`, rc=0. The author's 2 ks949 timeouts did not recur here.
- **Base, `--testTimeout=30000`**, product only, new files moved out (logs/base_whole_t30000.log): `Test Files 117 passed (117) / Tests 1385 passed (1385)`, rc=0. 1385 + 72 new = 1457, and there are no product-side regressions.
- **Invalidated runs**, kept and labelled: logs/*_INVALID_probe_present.log. My gate81-probe file was on disk during those runs and tripped ks1000's test-file typecheck (3 TS6133 lines, all in gate81-probe.test.ts). That was my artefact, so both runs were redone with the probe moved out.
- **Neighbours at head** (logs/neighbours_head_verbose.log, logs/neighbours_head_counts.log): ks1240b 59/59, ks811 6/6, ks795 41/41. This matches the author.
- **tsc**:
  - The product, `tsc --noEmit -p services/auth/tsconfig.json`, gives rc=0 (logs/tsc_product_head.log).
  - Tests, via `check.cjs services/auth`: 170 files, 119 tests, 42 errors, 42 in the baseline, 0 new, 0 stale, rc=0 (logs/tsc_tests_check_head.log).
  - A planted TS2322 in the allowlist test was named and gave rc=1, and the file was restored by sha256 (logs/tsc_tests_check_planted.log).
- **eslint 10.7.0 `--max-warnings 0`** on auth.ts and the two tests: rc=0 (logs/eslint_head.log). `preserve-caught-error` is active (level 1) for auth.ts. There is exactly 1 `eslint-disable` in auth.ts at head and 0 at base (logs/diff_numstat.log). Removing it fails lint (G81-F2).

## 4. merge-tree

`git merge-tree --write-tree d7691f35 5914d69a`: **rc 0**, tree `b9c57669983536928813ea2f47cd50cd4a8f2bdb`, which equals the head's own tree, since develop has not moved past the PR's parent (logs/merge_tree.log).

## 5. Fragment check

`docs-fragments.mjs check --root wt_head`: rc 0, "lint clean, render passes html_docs_check", OK. Counts are flow 117+49 and cheat 112+49, up from 48 new at base (logs/frag_check_clean.log). The two ADVISORY lines (flow line 6249, cheat line 6235) are identical on untouched base (logs/frag_check_base.log), as the author said. Planted defects:
- An unclosed `<div>` in flow gives rc 1, `<div> opened 1, closed 0` (logs/frag_check_planted_flow.log).
- An unclosed `<div>` in cheat gives rc 1, `<div> opened 3, closed 2` (logs/frag_check_planted_cheat.log).
- A literal `7.` section number in the flow `<h2>` gives rc 1 with 2 findings (logs/frag_check_planted_number.log).

Every fragment was restored by sha256 (MATCH lines in each log).

Fragment content against what I measured:
- 72 cells, 20/72 red, the 52 controls and pins, and the neighbour counts all match.
- The whole-suite line ("1455 pass, 2 fail", ks949 timeouts, maxWorkers=3) describes the author's run. Mine gave 1457/1457 at the default timeout, so the reds are the flake the fragment names.

## 6. END heads

At 12:38:14Z, ls-remote shows PR head `5914d69aaa9c8bb5bfbff8c9689326f6b243e28d` and develop `d7691f35312ea158f043e87a3227e477cccb183d`, both unchanged from START. In wt_head, HEAD = 5914d69a, `git status --short` is clean in both worktrees, and auth.ts sha256 is `eb3b3e16…a89e`, equal to the original (logs/head_end.log).

## NOT TESTED

- A real provider sign-in, and whether any real provider can send a newline token. All cells, mine included, drive in-process stubs or a fake factory through the real routes and errorHandler.
- The production log format: winston JSON transport, with no format-level serialisation of `cause` beyond what I read in utils/logger.ts.
- Express's default handler body in production mode for the hostile link case (G81-F5).
- The author's 13 mutants themselves (I wrote my own 16).
- The four platform suites, a running stack, a database-backed auth run, Node 24 / any LTS (host v26.8.1), pre-push legs, CI, any deploy.
- KS-1868-class `err.message` log reads elsewhere in auth.ts (the author's routing candidates; outside this PR).

## HOW

- The clone came from the gate74 repo (local clone; git ignored `--filter` for a local path, so this is a full local clone). `origin` was set to `git@github.com:Secuura/Distributed_Secuura.git` with push url `no_push_qa_gate` and repo-local `core.sshCommand` with the Secuura deploy key, as specified. I fetched `refs/pull/1896/head` and `develop`, and created two detached worktrees, wt_base and wt_head, in the work dir.
- Scripts: scripts/vt.sh and scripts/mutants.py; the probe is scripts/gate81-probe.test.ts. Its head copy was moved to scripts/gate81-probe.head-copy.test.ts, and the base copies of the probe and new tests to scripts/base_moved_out/. Nothing was deleted.
- There were no writes to GitHub, Linear, mail or !CODING.
