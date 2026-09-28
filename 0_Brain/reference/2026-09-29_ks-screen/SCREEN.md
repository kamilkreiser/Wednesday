# KS board screen for the local models, 2026-09-29 (develop `215cc6875e2bac0b6d6b38918572384fbfcbdb77`)

Written 06:27 AEST 2026-09-29 (shell `date`) by a screening and brief-writing drafter for Wednesday. Secuura/Blockchain only. It was read-only on the Secuura repo and board: nothing was posted, moved, commented, raised, mailed or pushed, and no local model was run. It wrote only here, in `local-model/night/briefs/KS-1371/`, and in its own scratchpad (`screen0929/`).

## BLUF
- **Read in full: 65** of the 267 Backlog/Todo tickets. The 65 are every non-Peter/Stuart ticket updated since the 09-28 screen started, plus the local-shaped pool in `candidates.md`.
- **Ornith-briefable: 1, briefed. KS-1371** (`briefs/KS-1371/`). It is one hunk in vc-issuer `routes/status.ts`: `/unrevoke` refuses `index < 0` with a 400. The golden also appends four cells to the existing KS-1269 unrevoke test.
  - Golden: RED 2 failed / 9 → GREEN 9/9. Suite 146 → 150, 0 failed. The real checker gives PASS 7/7, and the Spark checker gives PASS + A2a.
  - ⚠ The ticket offers "validate, or widen the ruling". The brief follows the standing KS-662 ruling. Drop the round if Kam wants the ruling widened.
- **Spark-briefable: 0.** No read ticket passed the Spark predicate (one product file, a fix shape the ticket spells out, and an in-process test to copy) without first needing a ruling.
- **Cards for Kam: 3.** Each would make a ticket local-model work once ruled: **KS-1369, KS-1360, KS-1359** (below).
- **Reasons for the other 61, by frequency:**
  - 27: a decision or ruling comes first, or the fix shape is "not chosen".
  - 12: a register, umbrella, review or feature, spread across several operations or files.
  - 9: an auth, token or credential surface, or held by the commission (KS-1370, KS-1375).
  - 4: needs a live stack, a real Postgres, or a runner the checker does not have.
  - 3: the round counter is spent, or the path is Kam's (`.githooks`).
  - 3: docs with no failable test.
  - 2: nothing is left on develop, or the work belongs to another platform.
  - 1: ruled "do not build".

## Method, stated
- **Tip:** `git ls-remote origin refs/heads/develop` gave `215cc6875e2bac0b6d6b38918572384fbfcbdb77` at 06:08 AEST. That is unchanged from the last known tip `215cc6875e2b`, and the object is local in the Blockchain checkout (`cat-file -t` = commit). This drafter's `--shared` clone `screen0929/base` was checked out detached at it, with node_modules farmed by `tasks/code_patch/prepare_clone.sh` and `packages/shared` built in the clone. The checkout reported tracked-modified 0 after every farm. No git write verb ran inside `!CODING/`.
- **Board:** read with the Secuura project's own Linear key, sourced transiently in a subshell and never printed.
  - **Counts from `fleet/board_count.sh`:** Backlog **TOTAL=237** and Todo (unstarted) **TOTAL=30**, each against a limit of 250, so both are real counts. That makes 267.
  - A paginated pull of all open KS issues (6 pages, run to `hasNextPage=false`) returned 504: Backlog 237, In Progress 219, Todo 30, In Review 13, Blocked 5. Its Backlog/Todo figures agree with the script.
- **Read in full: 65.** For each: the description plus `comments(first:50)`, sorted client-side. No ticket had more than 20 comments, and `hasNextPage` was false for all 65. The 65 are:
  - **33** Backlog/Todo tickets updated since 2026-09-27T20:00Z. That is 41, minus the 8 on Peter/Stuart (KS-1361, 1363, 1366, 1367, 188, 492, 502, 985), which were excluded at the filter and not read.
  - **32** further rows from `candidates.md`'s local-shaped sections (T1 services, T2b bash, T3 jest, T4 docs; derived 09-28 12:46). All 32 are still open.
  - Also read, for premises only: KS-662 and KS-1269, the ruling and the sibling behind KS-1371.
- **Not read in full: 202 Backlog/Todo.** None was updated since 2026-09-27T20:00Z. They rest on `candidates.md` (09-28 12:46, T5 multi-file / SET ASIDE / EXCLUDED rows) and the 09-28 screen. Text-scan counts over the 267 (these over-count): 23 on Peter/Stuart, and 79 with auth/token/credential/session-shaped titles. The In Progress, In Review and Blocked states are outside this commission (Backlog/Todo).
- **Open PRs:** `git ls-remote origin 'refs/pull/*/head' 'refs/pull/*/merge'` at 06:13 AEST shows **22 live merge refs**: #572 575 635 639 649 809 887 920 923 927 945 946 947 948 949 989 995 1129 1250 1253 **1332 1337**.
  - This is the 09-28 CARVE's 20 plus two new ones: **#1332** (KS-1054: migrations, startup-migrations, health; excluded) and **#1337** (the `packages/shared` ks764 guard test; excluded).
  - All 22 heads were fetched into this drafter's clone and each was diffed against its merge-base with `215cc687` (108 file rows, `screen0929/prfiles.txt`).
  - **No open PR touches `vc-issuer/src/routes/status.ts` or its tests, `api-gateway/src/routes/proxy.ts`, `api-gateway/src/routes/platform.ts`, `wallet-connector/src/server.ts`, or `scripts/stack_guard.sh`.** #649 touches `wallet-connector/package.json` only.
- **Round counter:** `night/done.md` rows by id at line start, plus `READY_<id>*` filenames, plus brief entries, plus `candidates_rounds.md`.
  - **Positive controls:** KS-908 returned 3 done rows, and KS-1269 returned 4 done rows and 4 READYs.
  - **KS-1371 was 0 / 0 / 0 before its brief was written.**
  - Spent counters among the 65: KS-1163 (4 rows), KS-987, KS-1168, KS-1222, KS-1145 and KS-998 (2 rows each). KS-1190 has 1 row.
- **Exclusions applied as given:** `migrations/`, `startup-migrations.ts`, gateway /health and `deploy-all.sh` (KS-1054, #1332); the ks764 guard test (#1337); the security service `index.ts` validate/revoke paths (KS-1370, KS-888, KS-1352, KS-1375); auth/token/credential/OAuth/MFA surfaces; KS-1250; `.githooks` and `.github/workflows`; anything on Peter or Stuart.

## Every ticket read, one line each
`id · tier · the clause that decides it · where read (at 215cc687 unless noted)`

- **KS-1371 · ORNITH (BRIEFED)** · the schema declares `index` `nonnegative()`, and the KS-662 ruling tolerates `-1` on `/revoke` only (its record lists `unrevoke {index:-1} -> 200` as NON-RULED). One 2→3-line hunk plus an in-place test append; the KS-1269-U Ornith precedent passed 7/7 on the same file · `status.ts:327`-`:331`, `:258`; `vc-issuer.openapi.ts:979`, `:1621`; ks1269 unrevoke test `:17`, `:51`, `:77`-`:79`
- KS-1369 · card-for-Kam · "A small guard plus an error path would likely settle it; **your call on the shape**". The guard would be at the first statement of `onProxyReq`. No test reaches `onProxyReq` with an already-sent `proxyReq`: the ks1041 harness uses real HTTP recorders, and nothing mocks `http-proxy-middleware` to capture Options · `api-gateway/src/routes/proxy.ts:242`-`:246`, `ks1041-vouch-mint-scope.test.ts:1-80`
- KS-1360 · card-for-Kam · "add `success: true` ... or correct the published schema". Also, `wallet-connector/src/server.ts` boots at import (`initDb(...).then(app.listen(PORT))` `:324`-`:348`, subscriber `:309`), and the route is inline behind `jwtAuthenticate` (`:101`). No in-process test drives it · `server.ts:195`-`:220`; `wallet-connector.openapi.ts:398`-`:418`
- KS-1359 · card-for-Kam · "Either tightening the validation or widening the ruling ... your call". Rejecting above-maximum `limit`/`offset` would also undo KS-5's deliberate clamp · `api-gateway/src/routes/platform.ts:359`-`:377`
- KS-1375 · skip (held) · commission: the proof binding waits on Kam's card (defaults 18:00 today); a vc-issuer verify/security surface · description
- KS-1374 · decision · "we need your decision on how the platform's rate limit should treat our Akto scans", with six options · description
- KS-1372 · auth (excluded) · the gateway failed-login lockout, "Either wiring it up or retiring it" · description; `middleware/security.ts:146-192` (cited)
- KS-1370 · skip (held) · security `index.ts` validate path, a KS-1370 measurement in flight; the fix reds 5 ks888 cells (comment 17:20) · description + 2 comments
- KS-1368 · decision · "a policy question, not a defect report. Nothing is built for this." · description
- KS-1364 · multi-file · 17 operations across service `*.openapi.ts` sources plus regeneration; "It isn't a blanket fix" · description
- KS-1358 · decision · "does this supersede the KS-406 auth-first ruling?" · description
- KS-1357 · auth (excluded) · OAuth rotate-secret · description
- KS-1356 · decision · no defect; "whichever approach you'd prefer" (a Docker runner for a Postgres suite) · description
- KS-1355 · multi-file · four spots (`stack_guard.sh`, `dev-reload.sh`/`start-local.sh`, `docker-compose.yml`, `preflight.sh`). Spot 1 alone needs a designed output format ("group by project and append an `unknown` count"), and it is bash outside `services/`/`packages/`, which `build_input.sh` refuses · `scripts/stack_guard.sh:104-110`, `:206-214`; `stack_guard.test.sh:1-80`
- KS-1242 · auth (excluded) · `authenticateToken` async without a catch; "Worth doing for the whole gateway" · description
- KS-1218 · decision · "Either add the pip upgrade ... or pin pip in constraints.txt"; Python/docs, and the checker has no runner for it · description
- KS-1015 · register · 28 check/operation pairs, 13 on `/api/auth/`+`/mfa/`; finding 2 "is Peter's call" · description + 3 comments
- KS-1012 · decision · a GitHub ruleset, "needs org-admin rights and is a decision, not a fix" · description
- KS-964 · decision · 104 flat spec files: "quarantine and find out, do not delete" · description + 3 comments
- KS-915 · decision · "One of:" a documented procedure, a bootstrap command, or a written decision; no failable test · description
- KS-785 · decision · "Two candidate shapes, neither chosen here"; credential check / start path · description
- KS-770 · skip · a review stream for Peter; no code · description + 4 comments
- KS-752 · live/runner · `systemTest/schemathesis/scripts/run.py` (Python, which the checker does not run), plus "an invalid-run rehearsal" · description + 4 comments
- KS-725 · decision · "Option 2 is the one that fails closed, but it is the harness owner's call" · description + 2 comments
- KS-724 · decision · item 1 merged (#1336); items 2-3 are "a harness-design call" · description + comment 09-28
- KS-716 · decision · three done-means items (warn + count, doc, an asserted URL split); Akto harness design · description
- KS-709 · live · criteria 1 and 3 are open, and 3 is "Reproduced from a real run, not only a unit test" · description + 5 comments
- KS-696 · live · a measurement ticket ("running `test:pr` N times against a frozen commit") · description + 4 comments
- KS-618 · auth/infra · every IP-keyed security control; nginx `real_ip` plus `trust proxy`; "Verify by evidence" on the live demo · description + comment
- KS-593 · register · the raw-5xx class over 6+ operations in several services · description + 20 comments
- KS-591 · register · `positive_data_acceptance` over 60+ operations · description + 9 comments
- KS-565 · register · §1-§2 plus "SIX sites across four services" (negative offset); the tenant-provisioning site boots at import · description + 14 comments; `tenant-provisioning/src/index.ts:553-567`
- KS-491 · register · Review F: WAF, Caddyfile and `Server:` header options for Kam · description + 7 comments
- KS-678 · skip (nothing left) · `example.secuura.io` has **0** occurrences under `Blockchain/Dev` at the tip (control: `example.com/resource` gives 17 in the published spec); a board close is owed · `git grep -c` at `215cc687`
- KS-683 · skip (other platform) · Layer 1 merged on Platform-S (PS-644); layers 3-4 are Stuart's · description + 3 comments
- KS-953 · decision · "Shapes worth considering (not chosen — this needs a decision)" · description + 2 comments
- KS-955 · decision · "Fix shapes (not chosen)" · description + comment
- KS-987 · counter spent (2 done rows) · item 1 already briefed 09-15; the rest are runbook/audit items · description + 2 comments
- KS-1168 · auth (excluded) · `services/auth` userRepo, "Pick one" of 3; counter 2 · description
- KS-1190 · decision · "Do not make it fail closed yet. Two measurements come first" · description
- KS-1222 · decision · "The owners decide what the route should be"; counter 2 · description
- KS-1327 · decision · "Fix shapes, not chosen here"; a persistence-path behaviour change · description
- KS-1328 · decision · "Fix shapes, not chosen here"; a load-only timeout has no deterministic red · description
- KS-1329 · multi-file · 6 files; TS2349 "Decide it here, with the guard's owner"; a new tsc leg "touches the push gate" · description
- KS-579 · feature · per-person platform-admin identities · description
- KS-581 · feature · alerting, rate limit and correlation on register-connector · description
- KS-627 · feature · "It is not a patch": a breaking contract, new crypto dependencies, wallet test vectors · description + 3 comments
- KS-746 · decision · "a design sketch, not an agreed plan"; plus a migration · description
- KS-758 · decision · "A dead-letter path is a design, not a line" · description + comment
- KS-784 · decision · validate-before-config vs a local test mode, "your call which" · description + comment
- KS-837 · ruled · "Wednesday priced line 1 and ruled DO NOT BUILD IT NOW" (09-05) · description + comment
- KS-986 · decision · credential doc: "Setting a credential on a running system is Kam's signature class" · description + comment
- KS-1145 · live · a real-PostgreSQL bash suite (`ks949_main_seed_idempotence.test.sh`); counter 2 · description
- KS-1197 · auth (excluded) · a JWT `verificationLevel` claim; fix in `middleware/auth.ts` · description
- KS-748 · decision · "Either a FOREIGN KEY ... or an explicit decision"; DB schema · description
- KS-1305 · decision · "Fix shapes, not chosen here"; Prisma layout tooling · description
- KS-998 · Kam's path · `.githooks/pre-push` (Kam ruled a, 09-22); counter 2 · description + comment
- KS-1163 · counter spent (4 done rows) · Kam ruled a ("Wait for all five") 09-22; "sits past the local model's counter", so a cloud seat · description + comment
- KS-1324 · decision · "Fix shapes (not chosen here)"; a wall-clock cell with no deterministic red · description
- KS-630 · decision · "Decide whether it joins `scripts/preflight/preflight.sh`" (the shared pre-push gate) · description
- KS-759 · auth (excluded) · originate `middleware/auth.ts` plus the shared `JwtPayload`, "wants its own PR and its own reviewer" · description
- KS-1290 · docs · DEV-PROCESS plus two scripts; the push-gate leg is "Kam's call" · description
- KS-1320 · docs · "Fix shapes (the reporter's proposals, not ratified)"; no failable test · description
- KS-1343 · docs · eight doc notes, two "tightened or explicitly accepted as-is"; no failable test (as on 09-28) · description
- KS-1322 · decision · "a ruling is recorded: keep, or strip" · description

**Counts over the 65 read (each ticket once):**

| class | count |
|---|---|
| Ornith, briefed | 1 |
| Spark | 0 |
| card-for-Kam | 3 |
| decision | 27 |
| register / multi-file / feature / review | 12 |
| auth or held | 9 |
| live / runner | 4 |
| counter spent / Kam's path | 3 |
| docs | 3 |
| skip (nothing left / other platform) | 2 |
| ruled do-not-build | 1 |
| **total** | **65** |

The auth-or-held 9 are KS-1375, 1370, 1372, 1357, 1242, 1197, 759, 1168 and 618. KS-770 is counted under register/review.

## For Kam (cards, not tasks)
- **KS-1369** (gateway crash under load): for `onProxyReq`, choose between (a) returning early when `proxyReq.headersSent` (the ticket's direction 1) and (b) catching the throw and answering through the proxy error path (direction 2). With (a) ruled, it is a one-file Spark candidate. The test harness still has to be written: nothing in the repo reaches `onProxyReq` today.
- **KS-1360** (wallet session DELETE): add `success: true` to the 200 body, or change the published schema?
- **KS-1359** (platform audit-log): 400 on wrong-type and below-minimum `offset`/`limit`, while keeping KS-5's clamp for above-maximum? Or widen the KS-662 ruling?

## For Wednesday (process)
- **KS-1371's option.** Kam may want the ruling widened instead (Peter to Kam on KS-1269, 09-28: "your view decides it"). The brief follows the ruling as recorded. Hold the round if a KS-1371 card is preferred.
- **KS-678 can be closed.** The literal is gone from develop (0 occurrences, with a firing control). It is a board action, not model work.
- **KS-1163 was ruled on 09-22 and its counter is spent.** It is ready for a cloud seat: two files, script plus test.
- **The queue gates:** `PAUSE_QUEUE` ran until 06:00 today, and `night/log/night_2026-09-29.log` shows G2 (a foreign Secuura/Blockchain pane) refusing every 15 minutes through 06:02. The KS-1371 round needs G2 clear.

## UNMEASURED
1. **Open PRs come from a proxy:** live `refs/pull/*/merge` plus fetched heads, not the GitHub files API. A PR without a merge ref would be missed.
2. **The 202 Backlog/Todo tickets not read** rest on `candidates.md` (09-28 12:46) and the 09-28 screens. None was updated since 2026-09-27T20:00Z.
3. **The auth and Peter/Stuart counts over 267** are text-scan counts, not per-ticket readings.
4. **No local-model round, no live stack, no Postgres.** For KS-1371, `build_input.sh` (rc 0), `checker.sh` (PASS 7/7) and `spark_checker.sh` (PASS + A2a) were run on the golden only.
5. **The card rows' harness claims** (KS-1369 and KS-1360: no in-process test) come from a grep of test imports plus reading `server.ts` and `proxy.ts`. No harness was attempted.
6. **Round counts** were matched by id in `night/done.md`, `READY_*` filenames, brief names and `candidates_rounds.md`. Spark rounds recorded only elsewhere (for example `SPARK_LADDER.md`) were not cross-checked for the 64 non-briefed tickets.

Artefacts are in this drafter's scratchpad (`screen0929/`), not copied here: `lin/board.json`, `lin/full.json`, `lin/txt/<id>.txt`, `lsremote.txt`, `prfiles.txt`, `g1371/` (golden, arms, suite JSON), `bi1371/` (the builder output), and `chk_k1371_*` (checker runs).
