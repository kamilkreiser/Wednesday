# QA Agent Invocation Brief — Datasec/NexusAI, GATE 7: RD-645 (TIER 1, the password sign-in's own rate limit)

**Drafted for Tuesday 2026-09-22 21:45-22:10 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on ONE READY FOR QA mail from NexusAI-I (S80I, live), in `tuesday-agent@agentmail.to`:
- RD-645 @ `202770e`, 2026-09-22T11:43:09Z, subject `[Datasec/NexusAI-I -> Tuesday] READY FOR QA: RD-645 authLimiter on POST /api/auth/login @ 202770e …`
  (sent copy `session-tools/s80i/mail-14-ready645.AQherw`; the coordinator's scratch copy is byte-identical but for one blank line).
**The head is pinned here; nothing is pinned at launch.** The launcher re-reads it by `git ls-remote` immediately before launch and refuses on any mismatch.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-22 21:54
Self-check note: Tuesday read the header and the drafter report whole (7 wrong-at-source items accepted: base aab3bf2 not c0788b1, server.js identical at both; the READY short sha broken, real head 202770e re-read by ls-remote in the same action; git archive per arm instead of a worktree; the negative-control seats updated; HEAD is not a bypass; the cap is 20 unless NODE_ENV=development; A4 covers only status and check). Target sections were read by headline; Tuesday wrote the commission.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an
independent tester. You did not build this change and you owe no builder anything. **Every line below that reports
what a builder says is a CLAIM, never evidence.**

**ONE gate, ONE target, ONE session. RD-645 is TIER 1**: it changes a product SECURITY CONTROL (brute-force limiting of the
password sign-in) in the server entry point. **Give ONE verdict: GO / NO-GO at `202770e`.**

## RULED BY KAM, NOT YET IN AN ARTEFACT
- None new for this target. The scope ruling is **C-146** (Tuesday, ANSWER 2026-09-22T09:09:23Z), IN
  `1_Project_Definition/CLARIFICATIONS.md` (:1518-1524): `authLimiter` is mounted on **POST /api/auth/login ONLY**;
  `/api/auth/enforce` stays unthrottled as a **named residual**; the Entra callback is not throttled (Entra checks the
  credential; a per-address cap would 429 an office behind one NAT); the NAT trade-off must be STATED with the configured
  numbers (20 per 15 min per client address in production, 50 in development). **Not covered by C-146: throttling enforce,
  a lockout or per-account counter, any change to the cap values.** Do not grade the absence of those as RD-645 defects;
  report them as residuals if you measure something about them.
- **C-145** (Kam, 2026-09-22 17:15:53 AEST): Redis-down policy is option (c), *leave it as is, tickets only*
  (RD-646 = gate 6 F-2, RD-647 = gate 6 F-3). If your Redis leg meets those behaviours on the `auth` limiter, cite them as
  the known, ruled residuals; they are NOT new findings against RD-645 unless RD-645 changes them.
- C-49/C-50 (prior-work check), C-68, C-89, C-57, C-110, C-122, C-127, C-141 + ADDENDUM, C-142, C-143 + ADDENDUM are
  recorded in CLARIFICATIONS.md.

## PRIOR ROUND
- **Round 1.** RD-645 has not been gated.
- **Where the defect was found — gate 6, F-1** (Major, pre-existing). Report on disk:
  `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate6-rd619-rd607-pr31/report.md`.
  Read **§6 F-1**, the **§4.2 per-limiter table** (the `auth` row) and **§4.6**. MEASURED there: 70 failed logins from one
  address → **70 × 401, no 429**, and in Redis mode **no `nexusai:rl:auth:*` key ever**, at `982a84f`, `8fa0791` and
  `58bb38c`, in Redis mode (P1) and memory mode (P6). **Gate 6 ran every server `NODE_ENV=development`**, so its "configured
  50" is the dev cap; production (20) was NOT driven there (its §9). Its probe is on disk:
  `…/2026-09-22-gate6-rd619-rd607-pr31/evidence/probe-b.js` (+ `probe-b.json`, `phases.P1.caps.auth`). Reuse it.
- Gate 6 also measured every OTHER mounted limiter on a real `redis:7.4-alpine` (own cap, own 429, own TTL) and the
  product's full Redis command set. RD-607 (gate 6 B) and RD-619 (gate 6 A) are now MERGED on main (`af90431`, `aab3bf2`).

## 1. Target — verified at drafting from the object store (21:45-22:05 AEST)
**origin, by `git ls-remote origin …` at 21:45:32 AEST (read back 21:45:35):**
main `c0788b1017a20ea5d2d0b9c0e5837ee233830696`;
`rd-645-auth-limiter-mounted-s80i` `202770e467257a9ca6c5af6432dd72c68dc1210e`.
No `refs/pull/*` points at any RD-645 commit (full `ls-remote origin` grep for `202770e|7759591|d05ec22|rd-645`, 21:46).

**THE BASE IS `aab3bf2`, NOT `c0788b1` (MEASURED):** `merge-base(c0788b1, 202770e) = aab3bf2dd72659b09713ccb3f0a8e4ad2560d852`;
`c0788b1` is NOT an ancestor of the head. Main's first-parent line since `58bb38c`:
`af90431` (merge RD-619 @ `d98271e`) → `aab3bf2` (merge RD-607 @ `2c4611b`) → **`c0788b1` = merge of PR #31 (`a11eb5f`)**.
**`aab3bf2..c0788b1` changes exactly three files, the three `node-version` lines** (`.github/workflows/build.yml`,
`deploy.yml`, `npm-audit.yml`); `backend/server.js` is blob `4a038be` at both. So main's backend = the base's backend.

### TARGET — RD-645 (TIER 1)
- **Branch `rd-645-auth-limiter-mounted-s80i` @ `202770e467257a9ca6c5af6432dd72c68dc1210e`**, off `aab3bf2`.
  **`aab3bf2..202770e` = three single-parent commits:**
  - `d05ec2212f8427c17bd9f9a202c46c72d5fee7fe` (parent `aab3bf2`): the mount + the comment + the new cell file
    (`backend/server.js` M, `__tests__/rd645-auth-limiter-mounted.test.js` A);
  - `7759591e77e3497b5edde867502c0f516b607582` (parent `d05ec22`): the cell file only (A5 widened to 70 attempts);
  - `202770e` (parent `7759591`): `scripts/verify-expected-counts.json` only.
- **Delta over `aab3bf2`, exactly THREE files, +185/−5:** `__tests__/rd645-auth-limiter-mounted.test.js` (A, 170),
  `backend/server.js` (M, +12/−2), `scripts/verify-expected-counts.json` (M, 3/3).
- **What the server entry point changes (READ, `git diff aab3bf2 202770e -- backend/server.js`):** TWO hunks.
  (1) The one-line comment above `authLimiter` becomes an 11-line comment (no code). (2) **`app.post('/api/auth/login', async (req, res) => {`
  becomes `app.post('/api/auth/login', authLimiter, async (req, res) => {`** (`:2871` at the head). Nothing else.
- **`authLimiter` itself is unchanged** (`:1218` at head): `rateLimit(_rlOpts('auth', { windowMs: 15 * 60 * 1000, max: isDev ? 50 : 20,
  message: { error: 'Too many authentication attempts', … }, standardHeaders: true, legacyHeaders: false }))`, and
  **`isDev = process.env.NODE_ENV === 'development'` (`:1103`)** — so the cap is 20 for ANY `NODE_ENV` other than
  `development`, **including unset**. No `keyGenerator`, `skip`, `skipSuccessfulRequests` or `passOnStoreError`: the key is
  express-rate-limit's default (`req.ip`), and successful logins COUNT.
- **Mount order (READ):** `app.set('trust proxy', 1)` `:1071`; `app.use('/api/', generalLimiter)` `:1292`; the CSRF
  middleware exempts `req.path` by EXACT match and `'/api/auth/login'` is in `csrfExemptExact` (`:1395-1404`, `:1446`);
  the login route is at `:2871`. So a login passes general, then CSRF (exempt), then `authLimiter`, then the handler.
- **The only password verification in `backend/`** is `verifyPassword(` (defined `:2091`), called once, at `:2915`, inside
  the login handler (`git grep -n -E "bcrypt\.compare|verifyPassword\(|comparePassword|scrypt|timingSafeEqual" 202770e -- backend`,
  22:00). Other constant-time compares are the CSRF token, the coordinator secret, SCIM's bearer token and the marketplace
  webhook HMAC: not passwords, not in C-146's scope.
- **The `/api/auth/*` routes at the head** (READ): `GET check` `:2836`, **`POST login` `:2871` (the only one limited)**,
  `POST logout` `:2970`, `GET microsoft/login` `:3065`, `GET microsoft/callback` `:3112`, `GET users` `:3339`,
  `POST users` `:3380`, `GET status` `:3594`, `POST enforce` `:3724`, `POST entra-config` `:3886`, `POST verify-group` `:3956`.
- **Seven `rateLimit(` calls in the server entry point, seven unique `_rlOpts` names** (`csp-report`, `general`, `auth`,
  `setup`, `ai`, `data-source-test`, `ai-test`) — RD-607 intact; `auth` is now mounted, so SIX-of-seven becomes SEVEN.
- **Versions (package-lock at `202770e`, blob `9064763`, the same blob as `8fa0791` and `aab3bf2`):** express **5.2.1**,
  express-rate-limit **7.5.1**, rate-limit-redis **4.3.1**. Express 5's router is case-insensitive and non-strict by
  default; express-rate-limit 7.x keys on the full `req.ip` (no IPv6 subnet masking — that arrived in 8.x). Both matter to
  §3 Q4.
- **Counts: base `aab3bf2` 3924 / 225; head 3930 / 226** (+6 tests / +1 suite, the new file). Main `c0788b1` = 3924 / 225.
- **The builder's cells (READ, `__tests__/rd645-auth-limiter-mounted.test.js` @ `202770e`):** CTRL, A1 (dev: 50 × 401 then
  429), A5 (production boot `bootServer({ … env: { NODE_ENV: 'production' } })`: 70 failed logins, 1-20 → 401, 21-70 → 429),
  A2 (no spill into / no spend by other `/api` traffic), A3 (a correct password answers 200 under the cap, after 5 failures),
  A4 (**only `GET /api/auth/status` and `GET /api/auth/check`** are driven for a capped address). **No cell drives
  `enforce`, `entra-config`, `verify-group` or `microsoft/callback`** — §3 Q5 covers them.
- **An error at source in the READY mail:** it names the head `202770e472`. **That abbreviation does not resolve**
  (`git rev-parse --verify 202770e472^{commit}` rc 1); the head is `202770e467…`. Pin by the full sha above.

### How to build your trees
- **No worktree is pinned, and none is created in the NexusAI repo. Build your own trees INSIDE YOUR OWN PROJECT
  (Testing Agent MAIN), from the object store:** `git -C <repo> archive <sha> | tar -x -C <a fresh mktemp -d under
  projects/nexusai/qa-trees/gate7.XXXXXX/>` (git-index it from the object store, as gates 2-6 did, if a full verify needs a
  git tree: five suites read `.github`/`node-version` at `c0788b1` and some read git history). **Never `git worktree add`,
  `checkout`, `fetch`, `pull`, `stash`, `clean`, `gc` or commit against the NexusAI repo, and never work in its
  `2_Project_Files` checkout (C-28, C-67).** It is dirty and its local refs are stale: pin by sha, read origin by `ls-remote`.
- **Each tree you build is EXCLUSIVE to this gate and to ONE purpose.** Run nothing else in it, let no other seat run in it,
  and never reuse a mutant tree for a clean arm: a fresh `mktemp -d` per arm. **Another QA seat is live in your project**
  (pane `%46`, claude `16568`, a Vision gate): use `gate7`-prefixed directories only and touch nothing of theirs.
- `node_modules`: an APFS clone (`cp -c -R`) of gate 6's (package-lock blob `9064763` at every sha used here; confirm).
- **`git merge-tree --write-tree` writes objects** — always `GIT_OBJECT_DIRECTORY=<your mktemp -d>
  GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects`. The same two variables let you `git archive <tree-id>` a merge
  RESULT. Disclose any object-mtime freshening you see; do not try to prevent it.
- The repo is `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files`.
- **NOT on main. Nothing merges on your word or a builder's.**

## 2. Why TIER 1, and who is waiting
- Before RD-645, password guessing on `POST /api/auth/login` was bounded only by the general limiter: **1000 per 15 min per
  address in production** (500 / 5 min in dev), plus nginx's 10 r/s where nginx fronts it (compose only). RD-645 makes it
  **20 per 15 min per client address in production**. A cap that does not fire, fires late, can be sidestepped by a
  request shape, or is shared with (and spent by) other traffic is a **Major**. A cap that throttles a C-146 not-throttled
  route (the first-run / page-load surface that broke on 2026-03-27) is also a **Major**: that is an outage of first run.
- 🔴 **The queue.** Main `c0788b1`. RD-645 is Tuesday's GO under C-127 after this gate, forward-merged onto main and
  verified green (C-68, C-89, C-57, C-142). At drafting the jest lock was held by `s80i-rd510-proof` (pid 30633, since
  11:42:22Z) with SEVEN tickets queued: `s78g-regate` (11:26:43Z) then six `s80i-*` proofs (rd641, rd531, rd438, rd616r2,
  rd638, rd631-reproof). C-141 makes builder PROOF tickets yield to yours; `s78g-regate`'s class is unknown to the drafter.

## 2a. LEGITIMATE SHAPES — `authLimiter` IS a checker (template §2a)
Its failure path is a 429 to a person trying to sign in. A legitimate sign-in refused is an outage for that office; a
guessing shape admitted is a bypass. Measure every row (production mode unless stated).

| shape — its ordinary form, as the product really sees it | expected verdict | the rule clause that yields it | predicted-by |
|---|---|---|---|
| one address, 1st-20th login attempt in a window (any mix of right and wrong passwords) | answered by the handler (401 wrong / 200 right) | count ≤ `max` (20) | drafter |
| the SAME address, 21st attempt, correct password | **429 `Too many authentication attempts`** — successes count; this IS the NAT trade-off | count > `max`; no `skipSuccessfulRequests` | drafter — **measure; it is a stated, accepted trade-off (C-146), not a defect** |
| a second address, its 1st attempt, while the first is capped | answered (401/200) | per-`req.ip` key | drafter |
| `NODE_ENV` unset (a deployment that never sets it) | cap **20**, like production | `isDev` is `=== 'development'` only | drafter — **measure one boot**; say which `NODE_ENV` the shipped image and the marketplace template set (READ) |
| `NODE_ENV=development` | cap 50 | `isDev ? 50 : 20` | builder (A1) |
| a capped address's `GET /api/auth/status`, `GET /api/auth/check`, `POST /api/auth/enforce`, `POST /api/auth/entra-config`, `POST /api/auth/verify-group`, `GET /api/auth/microsoft/callback`, `GET /api/auth/microsoft/login`, `POST /api/auth/logout` | **never the auth 429** (their own status: 200/400/401/403/302…) and **none spends the auth budget** | `authLimiter` is on the login route alone (C-146) | drafter — the builder drove status + check only |
| a capped address's first-run / page-load traffic (`/api/setup/*` status reads, `/api/csrf-token`, `/api/health`) | not the auth 429 | as above | drafter |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. TARGET — RD-645: `authLimiter` mounted on `POST /api/auth/login` (TIER 1)
Claimed (S80I READY 2026-09-22T11:43:09Z; `expect-rd645.txt` written first, `rd645-proof-hold.sh`, `rd645-hold-run2.out`,
`rd645-clean1.log`, `rd645-m645.log`, `rd645-clean2.log`, `rd645-related.log`, `rd645-verify.log`; prior-work read
`jc-rd645-prior.HditR9`, RD-645 comment 38044):
- One lock hold: floor ours 0 before and after every arm, control 0 → 1. **clean1 6/6. M-645 (mount reverted) → EXACTLY A1 +
  A5 red**, CTRL/A2/A3/A4 green; A5's tally `{401: 70}` against `{401: 20, 429: 50}` with the mount. clean2 6/6.
  Related suites 10/10, 146/146. Full verify `--update-counts` **PASS 3930/3930 (226)**.
- Builder's LIMITS: the cells run the in-memory store only — **`auth` on real Redis is unmeasured**; no lockout or
  per-account counter; per-address only.

**Answer each of these with a measurement:**
1. **THE POSITIVE CONTROL FIRST — reproduce gate 6's F-1 on the base.** On a tree of `aab3bf2` (= main's backend; prove
   `aab3bf2:backend/server.js` = `c0788b1:backend/server.js` by blob), boot the real server **`NODE_ENV=production`**, fresh
   `DATA_DIR`, and send 70 failed logins from one address: **predicted 70 × 401, no 429**. Then the same on `202770e`:
   **predicted 1-20 → 401, 21-70 → 429** with the limiter's `error` text, and quote the `RateLimit-Limit` /
   `RateLimit-Remaining` / `RateLimit-Reset` headers on the 20th and 21st (predicted limit 20, reset ≤ 900 s). Repeat both in
   `NODE_ENV=development` (base 70 × 401; head 50 × 401 then 429). **A head result without its base control in the same
   window is not reportable** (C-110 clause 4). Reuse gate 6's `probe-b.js` shape.
2. **Re-derive the red-proof on `202770e` yourself**, one lock hold (proof of execution: `Tests: … 6 total` per arm):
   R0 predicted 6/6; **M-645** (the mount removed, the handler line otherwise byte-identical) predicted **EXACTLY A1 + A5
   red**, CTRL/A2/A3/A4 green. **Before each mutant arm, prove the mutant still parses** (`node --check` on the mutated
   server entry point, exit 0, output quoted): a red from a mutant that does not parse or load is a VOID arm, never a red.
   Read WHY each red is red. **Own mutants, each parse-checked and predicted before running:**
   (i) **over-broad mount** — `app.use('/api/auth/', authLimiter)` instead of the route mount (does A4 catch it? does anything
   catch it for enforce / entra-config / verify-group / callback?);
   (ii) caps swapped — `max: isDev ? 20 : 50` (A1? A5?);
   (iii) `skipSuccessfulRequests: true` (the NAT trade-off's "successes count" — guarded by any cell?);
   (iv) a constant `keyGenerator: () => 'x'` (one global counter for every address — does any cell notice?);
   (v) `auth` sharing general's counter (in memory mode: `authLimiter = generalLimiter`; is RD-607's S1 the only thing
   that notices, and S1 is source text — C-122);
   (vi) the mount moved to `app.get('/api/auth/login', authLimiter, …)` with the POST unmounted (A1/A5 red?).
   **Name every behaviour guarded by no cell** (a mutant no cell kills is a finding naming the unguarded behaviour, not a
   blocker by itself).
3. **Scope of the change, mechanically:** the only non-comment line the head changes in the server entry point is the login
   route line gaining `authLimiter,`; `authLimiter`'s option object is byte-identical to `aab3bf2`'s; no other limiter's
   options changed; `git grep -n -w authLimiter 202770e -- backend` returns exactly the definition and the one mount.
   READ ONLY, quoted.
4. **BYPASS SHAPES (security control). Each driven in production mode against `202770e`, each with a per-request client
   timeout; for EVERY shape that is NOT counted, prove it also did NOT reach the password check** (its status is not the
   handler's 401/200 body, and a handler-side marker you establish first — READ what the login handler logs or writes on
   a failed attempt, e.g. an audit entry — is absent). A shape that reaches the password check
   uncounted is a **Major bypass**.
   a. **`X-Forwarded-For` forgery under `trust proxy = 1`.** Locally there is no proxy, so the TCP peer (loopback) is the one
      trusted hop and `req.ip` = the RIGHTMOST XFF entry. Drive the DEPLOYED shape: `X-Forwarded-For: <forged-i>, 198.51.100.7`
      with `<forged-i>` different on every request and the rightmost fixed (what one appending proxy produces) —
      **predicted 429 from the 21st** (a forged left entry does not move the key). Then drive a single varying entry
      (`X-Forwarded-For: <forged-i>`) — predicted a fresh budget per value: that is the **no-proxy exposure**, and it is a
      deployment precondition, not a code defect, IF every shipped topology has exactly ONE appending proxy hop. **READ and
      state the hop count per shipped topology:** marketplace `azure-marketplace/combined/mainTemplate.json` (Container Apps
      ingress `external: true`, `targetPort: 3001`); `docker-compose.yml` (`nginx-proxy` publishes 80/443, the API service
      publishes nothing; `nginx.conf` sets `X-Forwarded-For $proxy_add_x_forwarded_for`); `bicep/nexusai-customer.bicep`.
      A topology with TWO hops (e.g. a load balancer in front of nginx) collapses every client onto the inner proxy's
      address — one shared 20-per-15-min budget for the whole deployment (a login outage) — say whether any shipped
      topology has that shape. Also a missing XFF (`req.ip` = loopback) and an empty/garbage XFF value: counted, on what key?
   b. **IPv6.** express-rate-limit 7.5.1 keys the full address. Drive `…, 2001:db8::1`, `…, 2001:db8::2`, … as the rightmost
      entry: predicted a fresh budget per address, i.e. one client with a /64 is effectively unlimited. And
      `…, ::ffff:198.51.100.7` vs `…, 198.51.100.7`: one key or two? Grade it (the drafter's expectation: a pre-existing
      property of per-address limiting on 7.x, Minor, owner NexusAI; fix-shape an IPv6 /64 mask or 8.x's `ipv6Subnet`).
   c. **Path and method variants.** `POST /API/AUTH/LOGIN`, `POST /api/auth/Login`, `POST /api/auth/login/`,
      `POST /api/auth/login?x=1`, `POST //api/auth/login`, `POST /api/auth/login;x`, `POST /api/auth/%6cogin`; `HEAD`,
      `GET`, `PUT`, `OPTIONS` on `/api/auth/login`; `X-HTTP-Method-Override: POST` on a GET. For each: status, counted by
      `authLimiter` or not, reached the handler or not. (READ first: Express 5 routes case-insensitively and ignores a
      trailing slash, so those variants REACH the route and are counted — but the CSRF exemption is an EXACT `req.path`
      match, so they may be refused 403 by CSRF before the route; a HEAD on a POST-only route never reaches it.)
   d. **Parallel requests racing the counter.** 100 concurrent failed logins from one address (both stores): predicted
      **exactly 20** answered by the handler, 80 × 429. Quote the tally. More than 20 handler answers is a **Major**.
   e. **Body shapes.** Malformed JSON, `application/x-www-form-urlencoded`, an oversized body, an empty body: counted or
      not, and whether any reaches the password check uncounted.
5. **C-146's NOT-THROTTLED routes, measured.** For ONE address already at 429 on login (production): drive each of
   `GET /api/auth/status`, `GET /api/auth/check`, `POST /api/auth/enforce`, `POST /api/auth/entra-config`,
   `POST /api/auth/verify-group`, `GET /api/auth/microsoft/callback`, `GET /api/auth/microsoft/login`,
   `POST /api/auth/logout` (the POSTs with a valid CSRF token from `/api/csrf-token` and its cookie) 25 times each:
   **predicted never the auth 429** (their own statuses; quote them). **And they do not SPEND the budget:** on a FRESH
   address, 19 failed logins, then 25 of each route above, then the 20th login must be **401** and the 21st **429**. In
   Redis mode, additionally: `nexusai:rl:auth:<ip>` equals the number of LOGIN requests exactly, before and after the
   other routes. **Any of them throttled or spending the budget is a Major** (the 2026-03-27 first-run failure).
6. **The `auth` limiter keeps its OWN count and shares no store (RD-607).**
   - Memory mode: each `rateLimit()` builds its own MemoryStore (READ express-rate-limit 7.5.1's default in the tree's
     `node_modules`); MEASURE with the 19/20/21 drive that general traffic does not spend auth's budget, and that 20 logins
     do not spend any other limiter's budget beyond general's own count (drive `setup` / `ai-test` for the capped address:
     their own caps, unchanged).
   - **Redis mode, THE REAL REDIS** (the builder's stated gap). Through the **docker** lock
     (`session-tools/nexusai-lock.sh docker qa-gate7-redis …`), a real **`redis:7.4-alpine`** from the LOCAL image store
     (`docker run --pull never --rm`, gate 6 used `sha256:ff02b58f971e…`), published on `127.0.0.1` only, stopped and
     confirmed gone in a `finally`. **Do not pull or push any image**; if the image is not present locally, report this leg
     **NOT RUN, blocker named**, and mail a QUESTION (§10). On `202770e` with `REDIS_URL` at it, production mode: 70 failed
     logins → 429 from the 21st; **`nexusai:rl:auth:<ip>` exists, counts login requests only, and its `PTTL` ≤ 900 000 and
     within the drive time of it**; a login increments `auth` and `general` and NO other key; `MONITOR` / `INFO commandstats`
     shows no command outside gate 6's measured set (`CLIENT SETINFO`, `SCRIPT LOAD` ×14, `EVALSHA`); no `ERR_ERL_*` at
     boot. Contrast the same drive on `aab3bf2` (predicted no `auth` key, 70 × 401 — gate 6's F-1 on real Redis).
   - **Two servers, one Redis (PROBED):** two `202770e` processes on the same real Redis; one address alternating between
     them: **the 21st login overall** is 429 on either. And in MEMORY mode two servers each allow 20 (per replica) — state it
     as the memory-mode design fact.
7. **THE NAT TRADE-OFF, AS MEASURED (C-146 requires it stated).** In production mode from one address: 20 attempts
   (mixing 5 failures with successful sign-ins by a real local account), then a CORRECT password on the 21st → predicted
   429. Report it in exactly these terms: **"20 password-login attempts per 15 minutes per client IP address in
   production (50 in development), successful sign-ins included; an office behind one NAT address sharing local accounts
   is refused at its 21st attempt in a window; the Entra (Microsoft) sign-in is not affected."** Quote `RateLimit-Reset`
   for the window. Do not wait out the 15 minutes.
8. **Prior work (C-49), READ ONLY:** confirm the builder's claim that `authLimiter` is in the root commit `8eb94ce`, was
   never mounted in this repo's history (`git log -S authLimiter --oneline`, `git log -G "authLimiter[,)]"`), and that its
   2026-03-27 removal from `/api/setup/` is recorded at `8eb94ce:SESSION_NOTES_2026-03-27.md:59`. Say whether the new mount
   could reproduce that failure (it would only if a first-run page POSTs login ≥ 21 times per window — READ the first-run
   page's calls to `/api/auth/login`).
9. **C-68 re-run on `202770e`, whole files, one hold:** rd645 (6); the builder's ten related suites BY NAME
   (security-fixes, rd525-export-and-erasure-cover-every-store, rd408-r2-misconfigured-explains, rd408-r3-probe-endpoints,
   setup-rate-limit-allowance, rd470-r2-enforce-route-refuses, rate-limit-allowance, rd518-r3-health-detail-decision,
   rd607-redis-limiters-keep-their-own-counts, rd615-audit-flush-cannot-resurrect-erased-entries); **every suite that POSTs
   `/api/auth/login`** (`git grep -l "auth/login" 202770e -- __tests__` — name them, and say how many logins per boot each
   makes against the cap it runs under: a suite that makes ≥ 21 logins per boot in a non-development boot would now 429);
   and every limiter/429 suite (`git grep -l -i -E "rateLimit|429|Too many" 202770e -- __tests__`). Report per-file counts.
10. **Full verify of `202770e`** (`npm run verify -- --maxWorkers=2`, RD-561, through the lock, git-indexed tree): predicted
    **3930 / 226**. Account for every failure by NAME and, if it is order-dependent, with the worker timeline (gate 5's
    method). "Re-run until green" is not acceptance (charter §4d).

Evidence: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/s80i/` (named above).

## 4. The forward merge and CI (NOT measured by the drafter: measure them)
**The drafter could not run `git merge-tree --write-tree` (read-only commission).** The builder CLAIMS merge-tree against
`c0788b1` is rc 0. Quote, from YOUR OWN object directory:
- `git merge-tree --write-tree --name-only c0788b1 202770e` — predicted clean (the only files `aab3bf2..c0788b1` touches
  are the three workflows, which RD-645 does not touch). **Prove the merge RESULT differs from `202770e^{tree}` in exactly
  the three workflow files** (`git diff --name-only 202770e <result-tree>`), so every measurement at `202770e` carries to the
  merged tree for `backend/` and `__tests__/`.
- **Five suites read `.github` or `node-version` at `c0788b1`** (drafter's `git grep -l -E "\.github|node-version" c0788b1 --
  __tests__`: erasure-health-branches, jira-adf-validator, python-normaliser-gate, rd327-build-digest-on-public-health,
  verify-suite-gate). Re-run them on the archived merge result (they are the only ones whose inputs differ from the branch).
- Counts on the merge result: `c0788b1`'s 3924/225 + 6/1 = **3930/226**; any counts conflict is resolved by regeneration
  (C-57), never by hand.
- **CI (C-142).** `build.yml` at the head runs on `pull_request` to main and `push` to main ONLY, and no PR ref points at
  RD-645 (READ, 21:46), so **RD-645 has NO CI run at its branch head: report it NOT RUN.** C-142's CI half applies to the
  MERGED head later, against the known set as amended by C-143's ADDENDUM (the RD-641 set minus HS3 while HS3 passes; HS3
  reappearing is the known flake, not NEW). You MAY read, **read-only**, main `c0788b1`'s own Build run (`gh run list
  --branch main --workflow build.yml --limit 3`, `gh run view <id> --log-failed`) to name the failing set the merge will be
  compared with; label it READ ONLY and do not treat it as RD-645's CI.
- **Say what the verdict means under C-68:** a GO is a GO at `202770e` only; name the cells to re-run on the REAL
  forward-merged head (predicted: rd645, rd607, the five `.github` readers).

## 5. Floor discipline — THE FOUR CLAUSES, plus THE DEADLINE RULE
1. **Every jest run goes through `session-tools/nexusai-lock.sh`** (FIFO queue), **tagged `qa-gate7-…`** so C-141 makes
   builders' proof tickets yield to yours (C-141 + its ADDENDUM: your tickets are gate-class; C-110: otherwise no queue
   jumping). **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory, owner
   file or queue ticket, even if it looks stuck. The yielding is theirs to do, not yours. If a holder looks stuck, mail a
   QUESTION (§10) and keep waiting. **Live-server probes that start the real server entry point are floor load too
   (C-110): run them inside your own lock hold**, and the Redis container inside the docker lock.
2. **Hold the lock ONCE per multi-run measurement.** Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`
   reparents to launchd and every server it starts reads FOREIGN).
3. **Record the foreign server count beside every result — the RD-606 form, anchored on YOUR OWN claude pid:**
   `basename(argv[0]) == node` AND the server entry point ANYWHERE in the remaining argv (preload form `node -r …`), argv
   from the kernel (`KERN_PROCARGS2`); **"ours" = the server's ancestor chain CONTAINS YOUR OWN claude pid** (a shared
   ancestor — tmux, launchd, a login shell — proves nothing). **NEGATIVE controls, all in the same run, all must classify
   FOREIGN:** NexusAI-G claude `57419` (pane `%36`), NexusAI-I claude `8360` (pane `%44`), and Tuesday's claude `45678`
   (pane `%0`). (Gate 6's H `29254` and Tuesday `63076` have exited.) Re-read them at start; if one has exited, say so and
   use the others; a hold with NO live negative control aborts. **Never** by `EADDRINUSE`, a whole-command-line grep
   (RD-591 c.37901), or raw `comm` (RD-574 r2 R2-1). Reuse gate 6's instrument
   (`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate6-rd619-rd607-pr31/evidence/qa-floorcount.py`,
   `qa-floorlib.sh`) with YOUR pid as `ROOT`.
4. **A zero is reportable only beside a control that fired in the same window.** Spawn one server the way the harness does,
   require the count to RISE, then reap it. The same clause governs the limiter itself: "no 429 on route X" is reportable
   only beside the login route's own 429 for that address in the same window.

**5. THE DEADLINE RULE — every real-server probe has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
*Why, measured:* gate 4's real-server probe (A3u, an export against an unlistable directory) **stalled ~70 minutes at 0% CPU
while HOLDING the jest lock, with 10 seats queued behind it**
(`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate4-rd575-rd524r2/evidence/a3u-stall-evidence.txt`).
One missing timeout cost the whole floor an hour. Therefore:
- **Every HTTP request carries a client timeout; every step (boot, request, burst, Redis start/stop, SIGKILL wait) has a
  written DEADLINE** (e.g. boot 60 s, request 30 s, a 100-request burst 60 s, container start 30 s, exit 20 s). A step past
  its deadline is ABORTED and reported as a finding with its evidence (a hung product request IS a finding), never waited on.
- **Every server and every container you start is killed in a `finally`** (SIGTERM, then SIGKILL after a grace; the Redis
  container stopped) — on success, failure, deadline or exception — and the reap is confirmed by your floor counter (and
  `docker ps` for the container).
- **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes** during any hold. **A step with no
  heartbeat for 5 minutes is aborted and reported.** A hold that is not making progress releases the lock.
- §3 Q4d (the parallel burst) and §3 Q6 (the Redis leg; a Redis drop meets RD-647's never-recovering 500s) are exactly the
  shapes that hang: deadline them. **Never wait out the 15-minute window.**

**Reap every server you start.** An orphan of yours is the next seat's foreign server.

## 6. Drivable surface — LOCAL RUN, **NOT THE DEMO** (RD-76). No demo pass happened; none must be recorded. Every request
goes to a server YOU booted on loopback from YOUR tree. **No request of any kind to any live or demo site.**

## 7. HELD
- No merge, no deploy, no registry, no Partner Center, no production, no money, no external comms.
- No real Azure, credential, vault, tenant or key. No `az` at all. The local accounts you sign in with are ones you create
  in your own fresh `DATA_DIR`.
- **`gh` is READ-ONLY and optional** (§4 only: `gh run list`, `gh run view`, `gh api` GET): never merge, approve, comment,
  review, label, re-run, dispatch a workflow, or open a PR.
- **docker:** only the §3 Q6 Redis container, through the docker lock, `127.0.0.1` only, from a local image; no build, no
  pull, no push.
- **Findings-only: do not commit, do not move any branch, do not file a ticket, do not write inside the NexusAI project**
  (its `2_Project_Files` checkout, `session-tools/`, `worktrees/`, `1_Project_Definition/` included). The gate fixes
  nothing and merges nothing.
- **NEVER `rm`** — quarantine, per the template §5; every preload, fixture and probe you plant lives under YOUR project.

## 8. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/report.md`

**Questions:** your sender `QA/Datasec-NexusAI` has NO inbox routing line in the fleet — you cannot receive an answer
reliably. If you must ask, mail `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>`
(Context / one Question / Meanwhile / Needed-by), **and proceed on the safest reading without waiting**; record the question
and the reading you took in the report.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — gate 7: RD-645 @ 202770e`

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` — an absolute path, because the
QA project has none. Never put the key, or any secret, in a mail or the report.

Verdict format:
- **RD-645: GO / NO-GO**, naming `202770e467257a9ca6c5af6432dd72c68dc1210e`, the positive control first (base 70 × 401 →
  head 429 from the 21st, production mode, same window).
- Then the NAT trade-off in §3 Q7's words, as measured; the C-146 not-throttled table (§3 Q5); the bypass table (§3 Q4)
  with a class per row; the Redis leg (§3 Q6).
- Then one paragraph on the queue: the merge-tree result onto `c0788b1`, which cells must be re-run on the merged head,
  and that the C-142 CI half is NOT RUN at the branch and is measured only at merge.
- **Rule 2: what you did NOT test is first-class output** (a NOT TESTED section). Every action recommendation carries its
  evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY. §3 Q4a (XFF / hop count), §3 Q4b (IPv6), §3 Q6 (real Redis)
  and §4 (CI) must each carry one.
- Report the head, and main's, as three timestamped readings (start / mid / end), each with its branch name.

PROVENANCE:
- origin heads: main c0788b1017a2…, rd-645-auth-limiter-mounted-s80i 202770e467257a9c…; no refs/pull/* at any RD-645 commit | `git ls-remote origin …`, full `ls-remote origin | grep` | read 2026-09-22 21:45:32 / 21:46 AEST
- base aab3bf2 (merge-base with c0788b1; c0788b1 not an ancestor); main first-parent 58bb38c → af90431 → aab3bf2 → c0788b1 (PR #31 merge, parents aab3bf2 a11eb5f) | `git merge-base`, `merge-base --is-ancestor`, `git log --first-parent --format='%h %p | %s' 58bb38c..c0788b1` | read 21:47
- aab3bf2..c0788b1 = 3 workflow files 1/1; server.js blob 4a038be at both | `git diff --stat aab3bf2 c0788b1`; `git rev-parse <sha>:backend/server.js` | read 21:47, 22:02
- chain d05ec22 (p aab3bf2) → 7759591 (p d05ec22) → 202770e (p 7759591); files per commit; delta 3 files +185/−5 | `git log --format='%H %P'`, `git diff --name-status <c>^ <c>`, `--numstat` | read 21:47
- the two server.js hunks (comment; `authLimiter,` on the login route) | `git diff aab3bf2 202770e -- backend/server.js` | read 21:48
- authLimiter options, isDev === 'development', trust proxy 1, general mount :1292, CSRF exact-path exemption incl. /api/auth/login | `git show 202770e:backend/server.js` :1060-1240, :1285-1295, :1380-1460 | read 21:50-21:58
- /api/auth/* route list; verifyPassword sole call site :2915 | `git grep -n` at 202770e | read 21:49, 22:00
- counts aab3bf2 3924/225, 202770e 3930/226, c0788b1 3924/225 | `git show <sha>:scripts/verify-expected-counts.json` | read 21:49
- versions express 5.2.1, express-rate-limit 7.5.1, rate-limit-redis 4.3.1; package-lock blob 9064763 at 8fa0791/aab3bf2/202770e | `git show 202770e:package-lock.json`; `git rev-parse` | read 21:52
- READY mail's "202770e472" does not resolve | `git rev-parse --verify -q 202770e472^{commit}` rc 1 | read 21:47
- cells CTRL A1 A5 A2 A3 A4; A4 drives status + check only; A5 `env: { NODE_ENV: 'production' }` | `git show 202770e:__tests__/rd645-auth-limiter-mounted.test.js` | read 22:01
- builder's related suites (10, 146 tests) | `session-tools/s80i/rd645-related.log` | read 22:02
- five .github/node-version readers at c0788b1 | `git grep -l -E "\.github|node-version" c0788b1 -- __tests__` | read 22:02
- topologies: marketplace Container Apps ingress external targetPort 3001; compose nginx-proxy 80/443, API unpublished; nginx.conf XFF $proxy_add_x_forwarded_for | `git grep`, `git show 202770e:docker-compose.yml` | read 22:03-22:04
- build.yml on pull_request→main + push→main only | `git show 202770e:.github/workflows/build.yml` | read 21:49
- C-146, C-145, C-143 + ADDENDUM, C-142, C-141 + ADDENDUM, C-110 | `1_Project_Definition/CLARIFICATIONS.md` :1101, :1478-1524 | read 21:43
- gate 6 F-1 (70 × 401, no auth key; dev mode only; production not driven), §4.2 table, §4.6 | gate-6 report :61, :279, :356, :406-418 | read 21:44
- floor: %36 → claude 57419 (NexusAI-G); %44 → claude 8360 (NexusAI-I); %0 → claude 45678 (Tuesday); %46 → claude 16568 (QA, Vision gate, in Testing Agent MAIN); 29254 and 63076 gone; jest lock owner s80i-rd510-proof pid 30633 since 11:42:22Z, 7 tickets | `tmux list-panes -a`; `ps`; `session-tools/locks/` | read 21:52-21:54
- evidence files in session-tools/s80i (mail-14, expect, proof-hold, run2, clean1/2, m645, related, verify, jc-rd645-prior) | `ls -la` | read 21:48
- no report dir 2026-09-22-gate7-rd645 yet | `ls` | read 21:53
