# QA gate 5 (TIER 1, round 1 of 2): Secuura #1788 (KS-1240 part 2, auth social providers, bounded outbound exchanges)

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), tier-1 gate, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel. Routing receipt as commissioned: claude-opus-5-5, tier-1 gate (auth social-provider request path), gauge ~76%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear was read only (KS-1240, through spark_review's own reader; the key was never printed). Decision cards were read with `decision_queue.sh list ruled` / `show` (read verbs only). `gh` is not authenticated in this shell, so I did NOT read the PR body. The head commit message stood in for it and went to Spark as the PR description, flagged as such.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate5-1788/repo`. The path did not exist before; made with `git clone --shared .../spark/cache/src`. `rev-parse --show-toplevel` was asserted equal to the path before the fetch and before every write. Origin = GitHub `Secuura/Distributed_Secuura`, deploy key via GIT_SSH_COMMAND with `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`. Worktrees are under `/private/tmp/claude-501/gatework5/`: `w1788` (head), `wdevelop` (d531abd5), and `sg1788` (spark_gate's own). None removed (no-delete rule). My probe file was moved to `gatework5/quarantine/`. After every mutant and probe, `git status` read back clean apart from the two node_modules symlinks.
- **node_modules:** read-only symlinks (made with `os.symlink`) at `Blockchain/Dev/node_modules` and `services/auth/node_modules` in each of my worktrees, both pointing at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules`. Nothing installed, nothing written into the shared tree. Node v26.8.1 (not the repo's LTS 24).
- **Docker / Postgres / ports:** none needed and **none started** (the cells use stubs). `docker ps -a`: 0 names match gate5. The only ports bound were vitest's own ephemeral 127.0.0.1 listeners inside the test runs.
- **Load:** load1 7 to 11. Every heavy run first waited in the background while load1 > 14.

## Pins (git ls-remote)

| ref | start (21:32:48) | end (21:45:23) |
|---|---|---|
| develop | **d531abd5f34bd32f3627149cfaf9b4e41e02fe1d** (= brief) | same |
| refs/pull/1788/head | **aa4829d4eaa059537fb922617debdc8e7490ac55** (= brief) | same |
| refs/pull/1785/head | e01a5094771d5ae69f3bf09fa0cfebf5b3008481 (= brief) | same |

#1788 merge-base with develop is **2b7ef12fa564** (= brief). Develop has moved on since then by #1781 (scripts/audit/audit-locks.mjs) and #1776 (packages/shared keyRevokePolicy + services/security). **#1788 changes none of those code files (intersection 0).**

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1788 | KS-1240 p2 | **GO WITH NOTES** | **The 12 adapter fetches are exactly the 12 outbound provider calls in services/auth, and each has its own `AbortSignal.timeout(10_000)`.** The signal also covers the body read. A timeout never becomes a login: `/social/link` answers 503 and the callback answers 400 with neutral text. **Claims reproduced:** 44/0 head and 21 pass / 23 fail at base (spark_gate); auth suite 1200 -> 1244 cells; build tsc rc 0 both sides; test-type ratchet 0 new from the PR. **My 13 mutants:** 9 killed. 4 survived, all on code the PR did not touch (profile/userinfo non-OK handling, token 5xx classification) or on dead code (the `AbortError` branch). **Two carried issues the brief asked about:** (a) the login callback **echoes the provider's raw error body to the client** (measured), and the PR's control cell *pins* that echo; (b) **GitHub's three sequential 10 s calls can reach 30 s, which equals production nginx's 30 s `proxy_read_timeout`.** Any single hang ends well under every front door. |

**Merge order vs #1785:** independent. The two share no code file, and merge-tree in either order conflicts only on the two Projects Documents html files. **Docs section for #1788 = 95.** The head carries `85` / `85.1-85.4`, which collides with develop's #1776 = 85; renumber at merge to 95 / 95.1-95.4. Both doc blocks are pure insertions before the single `</body>` (checked against 2b7ef12, both files). The cheat-sheet `<h2>` is unnumbered.

---

## Spark shadow (run FIRST; `out/p1788/`)

Method: `spark_gate.sh` (work `/private/tmp/claude-501/gatework5/sg1788`, `--node-modules` = Dev root), then `spark_review.py`. `facts_spark.json` = facts minus the two Projects Documents html files, plus HARNESS LIMIT lines (docs dropped; PR description is the commit message). Ticket KS-1240.

| | result |
|---|---|
| spark_gate head / base product code | **44 pass / 0 fail ; 21 pass / 23 fail** (matches X's claim exactly), 119 s |
| Spark review | attempt 1 **invalid** (repetition abort + unparseable JSON); attempt 2 valid: **GO WITH NOTES, 8 Notes, 0 Major/Minor**. 134.3 s total, 63,388 prompt tokens over both attempts (31.7k each) |

Not vacuous: 23 red cells at base, real files, real counts.

---

## (1) Every outbound provider call: site, bound, timer

`git grep` over `services/auth/src` (non-test) finds **15** `fetch(` sites. **12 are the social adapters** (all bounded by this PR). The other 3: `routes/oauth.ts:590` is browser-side JS inside an HTML template (not server outbound); `services/password.ts:130` (HIBP) was already bounded at 2 s; `routes/internal.ts:43` is **unbounded**, out of this PR's scope (see 1788-6). **There is no JWKS fetch anywhere on the social path.** Apple's `id_token` is base64-decoded, not verified (1788-7), so there is no key fetch to bound.

| # | file:line (head) | call | bound |
|---|---|---|---|
| 1 | `providers/social/apple.ts:56` (signal :66) | POST appleid.apple.com/auth/token | 10 s |
| 2 | `facebook.ts:55` (signal :62) | GET graph.facebook.com/v19.0/oauth/access_token | 10 s |
| 3 | `facebook.ts:71` (signal :73) | GET graph.facebook.com/v19.0/me | 10 s |
| 4 | `github.ts:54` (signal :66) | POST github.com/login/oauth/access_token | 10 s |
| 5 | `github.ts:75` (signal :77) | GET api.github.com/user | 10 s |
| 6 | `github.ts:90` (signal :92) | GET api.github.com/user/emails (only when the profile has no email) | 10 s |
| 7 | `google.ts:57` (signal :67) | POST oauth2.googleapis.com/token | 10 s |
| 8 | `google.ts:77` (signal :79) | GET www.googleapis.com/oauth2/v2/userinfo | 10 s |
| 9 | `linkedin.ts:55` | POST www.linkedin.com/oauth/v2/accessToken | 10 s |
| 10 | `linkedin.ts:74` | GET api.linkedin.com/v2/userinfo | 10 s |
| 11 | `microsoft-personal.ts:56` | POST login.microsoftonline.com/consumers/oauth2/v2.0/token | 10 s |
| 12 | `microsoft-personal.ts:76` | GET graph.microsoft.com/v1.0/me | 10 s |

Each site creates its own signal per call (`PROVIDER_TIMEOUT_MS = 10_000`, line 8 of each file). The signal also bounds the `.json()` / `.text()` body read that follows. The PR's stall cells prove that for the first call, and my G4 shows the stall surfaces as `TimeoutError`.

**Timer release:** `AbortSignal.timeout` arms an internal unref'd timer that is not cleared on success. It cannot hold the process open and is collected once it fires or the signal is unreachable. At most 3 live 10 s timers per sign-in. Same pattern as #1782 and #1785. **Per-request worst case** = the sum of the sequential calls: Apple 10 s, the four two-call providers 20 s, GitHub 30 s (see (3)).

## (2) What each path answers: timeout vs refusal vs provider 4xx/5xx

Measured with the PR's harness plus my probe cells (`out/probe1788_head_cells.txt`); real routes, stub provider:

| fault | `GET /social/:p/callback` | `POST /social/link` | login? |
|---|---|---|---|
| timeout (hang or stalled body, any of the 12 calls) | **400** `OAuth authentication failed: <P> did not answer in time; please try again.` (state spent) | **503** SERVICE_UNAVAILABLE, same text (P6: all 5 two-call providers on call 2, ~205 ms scaled) | **no** |
| refused connection (ECONNREFUSED) | 400 `OAuth authentication failed: fetch failed` | **500** INTERNAL_ERROR "An unexpected error occurred" (P4: Google token, GitHub profile) | no |
| token endpoint 4xx (JSON body) | **400 `OAuth authentication failed: Google token exchange failed: {"error":"invalid_client","error_description":"PROVIDER_INTERNAL_MARKER ..."}`** (P3) | 500 generic (no leak) | no |
| token endpoint 5xx (HTML body) | **400 `... Google token exchange failed: <html>upstream backend-7 trace id 9f9f</html>`** (P2) | 500 generic | no |
| profile/userinfo 401 | 400 `... Failed to fetch Google user profile (HTTP 401)` (P1). All five profile calls reject (P5) | 500 | no |

**A provider rejection does not become a login on any path** (measured). Defence in depth: with Google's profile `!ok` check deleted (G1), the adapter *resolves* a 401 as a profile with providerId `"undefined"`, and only KS-795's empty-email refusal (403 SOCIAL_EMAIL_UNAVAILABLE) stops the sign-in. See 1788-2.

**Provider error text leaks on the callback**, for token-endpoint failures in Apple, GitHub, Google, LinkedIn, Facebook and Microsoft. Each adapter puts `await tokenRes.text()` into its Error message (e.g. `google.ts:71-72`, `apple.ts:70`, `github.ts:70`), and `routes/auth.ts:1077-1078` wraps `exchangeErr.message` into the 400 the client sees. **Carried, not introduced:** routes/auth.ts and the throw lines are context. But the PR's control cell `test.ts:367-372` asserts the echo verbatim, so the leak is now pinned as expected behaviour. See 1788-1.

**Against the ticket and the cards.**
- KS-1240's text (filed for the gateway exchange) asks for "an explicit timeout ... and decide the refusal shape: a 503 on timeout is consistent with how the connector branch already answers a refused exchange".
- `secuura-ks888-revoke-validate-on-failed-save` = a and `secuura-ks1370-validate-when-the-revoke-check-cannot-read` = a rule fail-closed 503 for a *key that cannot be verified* by the security service. They do not rule on social sign-in.
- What #1788 does is in that spirit: an unverifiable sign-in never succeeds, and the link answers 503.
- Two shapes the cards and ticket do not decide (1788-4): a refused or DNS-failed provider is NOT classified as unavailable (500 on link), and the callback keeps 400 rather than 503 for a timeout. Both are disclosed in the commit message and pinned by green controls.

## (3) Is the bound below every front door?

Path for both routes: client -> nginx `location /api/auth/` -> api-gateway `router.use('/api/auth', proxy('auth', ...))` (`api-gateway/src/routes/proxy.ts:418`) -> auth.

| front door | timeout | file:line | vs 10 s per call | vs per-request worst case |
|---|---|---|---|---|
| api-gateway generic proxy | `proxyTimeout: 60000`, `timeout: 60000`; agent `timeout: 60_000`; breaker `requestTimeoutMs: 60_000` | `proxy.ts:165-166`, `:136`, `:63` | below | below (30 s max) |
| api-gateway Node server | keepAlive 65 s / headers 66 s (requestTimeout Node default) | `index.ts:1258-1259` | below | below |
| **nginx production** (docker-compose.production.yml:395) | **`proxy_read_timeout 30s`**, send 30 s, connect 15 s, server-level, inherited by `location /api/auth/` | `docker/nginx-gateway/nginx-production.conf:290-292`, location `:356-359` | below | **GitHub = 30 s = equal**; others 10-20 s below |
| nginx demo (docker-compose.yml:2298) | `proxy_read_timeout 60s` | `nginx-demo.conf:327-329`, location `/api/` `:410` | below | below |
| nginx dev/e2e (docker-compose.e2e.override.yml:28) | 120 s | `nginx.conf:126-128` | below | below |
| Caddy | "NO timeout tuning" (Caddy default, no read timeout) | `deployment/caddy/Caddyfile:27` | below | below |
| Azure Container Apps ingress | platform default, not in repo | not cited | | |

**Not the #1782 shape for a single hang.** Any single hung call ends at (preceding calls' durations) + 10 s, under 30 s in every realistic case. The equal-to-front-door case is GitHub's three calls each running just under 10 s. Then nginx answers 504 at 30 s while auth keeps going and may complete the sign-in (session/user created, response to nobody, state already spent). 1788-3.

## (4) Mutants beyond the PR's 9 (own worktree `w1788`, product file rewritten and restored from `git show HEAD:`; all 44 cells; `out/mut1788/`, summary `out/mut1788.txt`)

| mutant | result | red |
|---|---|---|
| M0 head | 44 / 0 | none |
| **G1 Google profile `!ok` check deleted (rejection read as a profile)** | **44 / 0, SURVIVES** | none (probe: adapter resolves; only KS-795 empty-email refusal stops the login) |
| **G3 GitHub `timedOut` drops `AbortError`** | **44 / 0, SURVIVES** | none (dead branch: a real timeout and a stalled body are both `TimeoutError`) |
| G4 GitHub `timedOut` drops `TimeoutError` | 36 / 8 | all 3 GitHub hang cells, stall, 4 route cells |
| G5 GitHub emails bound 10 s -> 30 s | 43 / 1 | GitHub call 3 hang |
| **G6 Google profile non-OK answered as 503 "did not answer in time"** | **44 / 0, SURVIVES** | none |
| G7 Apple classified text appends the abort message | 42 / 2 | Apple hang, Apple stall |
| **G8 Google token 5xx answered as 503** | **44 / 0, SURVIVES** | none (arguably the better answer; unpinned either way) |
| G10 LinkedIn profile signal from a never-firing AbortController | 43 / 1 | LinkedIn call 2 hang (behavioural cell catches what the census cannot) |
| G11 Microsoft timeout fails OPEN (returns an empty profile) | 41 / 3 | Microsoft calls 1, 2, stall |
| G12 Facebook classifies a refused connection as a timeout | 43 / 1 | Facebook refused-connection control |
| G13 GitHub emails timeout swallowed (login continues without email) | 43 / 1 | GitHub call 3 hang |
| G14 GitHub profile `!ok` check deleted | **44 / 0, SURVIVES** | none |
| G15 Google token error stops echoing the provider body | 43 / 1 | Google 400 control (**the suite pins the leak**) |

The PR's own nine (X's report) cover the timeout path well, and so do mine on that path (G4, G5, G7, G10, G11, G13 each killed where predicted). What survives is all **non-timeout response handling the PR did not change**: profile/userinfo non-OK (G1, G14, G6) and token 5xx classification (G8). G3 is dead code.

## (5) Merge-tree (`out/mergetree.txt`, `git merge-tree --write-tree --name-only` in my clone)

| merge | rc | conflicts |
|---|---|---|
| develop d531abd5 + #1788 | 1 | exactly the two Projects Documents html files |
| #1785 e01a5094 + #1788 | 1 | the same two only |
| #1788 + #1785 | 1 | the same two only |

**Code files shared with #1785: 0** (7 vs 7; control #1788 with itself = 7). Code files shared with develop's two commits since 2b7ef12: 0.

## Suites and gates (`out/suite/summary_r2.txt`, `out/testtypes.txt`, `out/tsc_build.txt`)

- **services/auth full suite.**
  - develop d531abd5: 105 files / **1200** tests, 1 failed.
  - head: 106 files / **1244** tests, 1 failed.
  - The failure is the same cell on both sides: `ks1000 ... REAL: services/auth against the committed baseline passes`, which is environmental (see the ratchet line below).
  - Head adds +1 file / +44 cells and 0 new failures. ks949 passed on both sides in this run. It failed 1 cell in a first head run made without the Dev-root symlink (`out/suite/w1788.json`), consistent with X's "timeout-sensitive at the 5 s default".
- **Test-type ratchet** (`node scripts/typecheck-tests/check.cjs services/auth`): **identical on both sides**. 44 errors: 42 baseline + 2 "new" (`jwks.test.ts:70`, `ks820-821...:197`), present on develop too. They come from the shared tree's newer @types/node, not from #1788. The PR's file adds 0. X reports rc 0 on its own tree; mine is rc 1 on both sides for this environmental reason.
- **`tsc -p tsconfig.json --noEmit` (build config):** rc 0 on both sides.
- Not re-run: ESLint, `audit:gate`, `audit:locks`, the hook (X: INCOMPLETE 13/16).

## Findings

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1788-1 | **Medium (carried, not introduced; now pinned by the PR's test)** | The login callback returns the provider's raw error body to the client: `OAuth authentication failed: Google token exchange failed: {"error":"invalid_client","error_description":...}` and an upstream HTML page verbatim (P2, P3). The cause is that all six adapters embed `await tokenRes.text()` in the Error, and `routes/auth.ts:1077-1078` echoes `exchangeErr.message`. `/social/link` does not leak (generic 500). **#1788 changes neither line, but its control `test.ts:367-372` asserts the echoed provider text, so G15 (stop echoing) turns the suite red.** The brief's bar ("must not leak provider error text") fails at base and at head equally. Mitigation in the code comment: no deployment configures a provider today (`routes/auth.ts:995-996`). Fix (follow-up, or a small amendment): answer a neutral `OAuthProviderError`, log the provider text, and change cell 367 to assert *absence* of the provider body. | FOUND by reading; TESTED P2/P3 (head and G1), G15. |
| 1788-2 | Low (test gap on code the PR did not touch) | Profile/userinfo non-OK handling is unpinned: G1 and G14 (check deleted) and G6 (answered as 503) survive. Under G1, a provider 401 becomes a resolved profile with providerId `"undefined"`, and **only the KS-795 empty-email refusal prevents the sign-in** (403 SOCIAL_EMAIL_UNAVAILABLE, measured). One control per family with a profile-call 401 JSON body (my P5 shape) would pin it. Spark's Note 4 points at the same gap. | TESTED (mutants + probe P1/P5 at head and under G1). |
| 1788-3 | Low (front door, equal not exceeded) | Per call, the 10 s bound is below every front door. Per request, GitHub's three sequential calls can reach **30 s = production nginx `proxy_read_timeout 30s`** (`nginx-production.conf:290-292`, inherited by `/api/auth/` `:356-359`). Then nginx answers 504 first while auth may finish the sign-in for nobody (state already spent). Needs three slow-but-answering calls. Any single hang ends under 30 s. Option: one exchange deadline (e.g. a single 20 s signal shared across an adapter's calls), or keep and state it. The two-call providers' worst case is 20 s. | FOUND by reading the conf + adapters; not run through nginx. |
| 1788-4 | Low (unruled shape) | Only a timeout is classified. A refused or DNS-failed provider answers `/social/link` **500 INTERNAL_ERROR** and the callback `400 ... fetch failed`. A token 5xx is also 500 on link (G8 survives). KS-1240's ticket groups "a refused exchange" with the 503 answer; the ks888/ks1370 cards rule fail-closed 503 for an *unverifiable key*, not social sign-in. The PR's "exactly as before" is deliberate and pinned (G12 killed). Nothing becomes a login either way. Decide or file. The callback-timeout = 400 (not 503) choice is disclosed. | TESTED P4, G8, G12; READ ticket and both cards. |
| 1788-5 | Info | `timedOut`'s `'AbortError'` branch is unreachable today (G3 survives). Harmless. | TESTED G3. |
| 1788-6 | Low (scope, same ticket) | `services/auth/src/routes/internal.ts:43`: the auth half of the connector-token exchange calls security `/api/keys/validate` with **no signal**. #1785 makes the gateway stop waiting at 5 s, but the auth handler then hangs on, unbounded. Not a social-provider call, so outside #1788 by wording. It is the same KS-1240 hang, and neither part 1 nor part 2 covers it. | FOUND by `git grep`; not executed. |
| 1788-7 | Info (carried, out of scope) | Apple: `id_token` is decoded with `JSON.parse(Buffer.from(..., 'base64'))` and never signature-checked (no JWKS, no `aud`/`iss`/`exp` check), `apple.ts:73-76`. Trust rests on TLS to appleid.apple.com, since the token arrives on our own back-channel request. Candidate ticket. | Read. |
| 1788-8 | Info | Node's fetch has its own 10 s connect timeout (undici default). For a blackholed provider it races our 10 s signal. The signal is armed first, so it should win (classified 503). If undici wins, the error is a `TypeError` and the answer is 500 on link. | Reasoning only; not tested (would need a real unroutable address). |
| 1788-9 | Low (merge-time) | Docs carry `85` / `85.1-85.4` (collides with #1776 = 85); use **95**. | Read; pure-insertion check passed. |

## Spark findings judged (GO WITH NOTES, 8 Notes)

- **Note 1** ("the ticket is about connector-token, not social providers"): true of the ticket's original text. KS-1240 is the multi-part umbrella and this is part 2. Not a defect.
- **Note 2** ("runtime tests cover only the first call"): **FALSE.** `HANGS` drives every one of the 12 sites (`test.ts:291-299`), and G5, G10 and G13 are each killed by a call-2 or call-3 hang cell.
- **Notes 3 and 7** (200 ms signal, not the real 10 s): true and disclosed. `asked` pins the 10 000 ms request.
- **Note 4** (only a 400 on the first call is tested): **TRUE, and it points at 1788-2** (G1, G14, G6, G8 survive).
- **Notes 5, 6, 8:** scope facts, not defects.

Spark did not mention 1788-1 (the leak, in the very control cell it quoted around), 1788-3 (nginx 30 s) or 1788-6.

## What I did NOT test

- Any real provider, nginx, gateway or stack; Node 24; Docker; CI; the four platform suites; the PR body (gh unauthenticated).
- Apple and Facebook under my probe matrix beyond P5/P6 (Apple has one call).
- The blackhole connect race (1788-8).
- Through a real nginx: the 30 s GitHub case (read only), and what auth writes after the front door has given up.
- ESLint, audit:gate, audit:locks, hook.
- The 2 environmental type errors (present on develop too; not diagnosed).

## Spark calibration row

| PR | Spark verdict | This check | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1788 | GO WITH NOTES (8 Notes; attempt 1 invalid, repetition abort) | GO WITH NOTES | 0 defects. 1 true test-gap Note (Note 4 = 1788-2), the rest scope or true-but-disclosed. 1 false Note (Note 2) | 1788-1 (provider text echoed, pinned by the control it read), 1788-3 (GitHub 30 s = nginx 30 s), 1788-4 (refusal is 500), 1788-6 (internal.ts unbounded) | **Right verdict, generic Notes.** Its one sharp point (Note 4) is real, and mutants G1/G14 confirm it. It mis-read the hang matrix as first-call-only. Cost: 63k prompt tokens over 2 attempts. A non-vacuous row: 23 red at base. |

## Evidence locations

- **Run outputs:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate5-1788/out/`
  - `p1788/` (facts, `facts_spark.json`, diff, `spark/review.json`, raw attempts)
  - `sg1788.log`
  - `mut1788/` + `mut1788.txt`
  - `probe1788_head_cells.txt`, `probe1788_G1_cells.txt`
  - `suite/` (`summary_r2.txt`, json)
  - `testtypes.txt`, `tsc_build.txt`, `mergetree.txt`
  - `pins_start.txt`, `pins_end.txt`
- **Scratch:** `/private/tmp/claude-501/gatework5/`
  - drivers: `run_sg.sh`, `run_rev.sh`, `prep_facts.py`, `mut1788.py`, `probe.py`, `suite.py`
  - worktrees: `w1788`, `wdevelop`, `sg1788`
  - `quarantine/gate5-probe-1788.test.ts`
