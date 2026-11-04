GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 184 (Tier 1, round 1): PR 1999 / KS-1244 refuse a repeated x-api-key with 400 on every route

Applies to PR 1999 at head `defe782aaf61222b0eaab414091ef36373e4a046` and to its merge tree on develop `307d9b4c762a`: **`1a5fd7a081a48375d4a1a8a6cc91b03710462c0f`** (this is for the merge seat).

## Subject block
- Repo Secuura/Distributed_Secuura. Read-only checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (read verbs plus `ls-remote` only; nothing written there).
- **Start pin** (`ls-remote`, 06:41:22Z): `refs/pull/1999/head` = `defe782aaf61222b0eaab414091ef36373e4a046`, `refs/heads/develop` = `307d9b4c762a187c85afafc883a7972f7c28ebcd`. Both match the commission.
- **End pin** (`ls-remote`, 07:01:45Z): the same two SHAs. Nothing moved.
- **Merge:** `git merge-tree --write-tree 307d9b4c762a defe782aaf61` in my clone gives rc 0 (clean), tree `1a5fd7a081a48375d4a1a8a6cc91b03710462c0f`.
  - The PR is 1 commit on 5c1ca287ed74, which is an ancestor of develop.
  - Develop moved twice since that base: ed170905f (KS-1981, lock-discovery.mjs) and 307d9b4c7 (PR 1998, KS-1234: 1 test file and 2 fragments). Neither touches any of the PR's 6 paths.
  - I ran everything on a local merge commit `3efb30ae2cc0` built from that tree (parents develop and head) and never pushed it.
- **Hosts:**
  - Apple Silicon Mac, Node v26.8.1. This is not an LTS line, so no result here is an LTS measurement.
  - vitest 4.1.12, TypeScript 5.9.3, zod 4.6.7, installed by `npm ci --ignore-scripts -w services/api-gateway -w packages/shared` from the head's lock. Develop's lock is byte-identical to the head's. The shared checkout's install was not used.
  - `@secuura/shared` was built with tsc (rc 0).

**Method.**
- I cloned with `git clone --shared` into `repo/` and fetched the PR ref and develop into that clone only, using the checkout's core.sshCommand.
- Every runner was anchored with `--root`, `-p` or `--prefix`, run under `env -i` with HOME and TMPDIR inside the workdir, and given a cwd of `<workdir>/cwd` through `bash -c` (see F1 for why).
- **Gate harness** (`harness/gate184-harness.test.ts`, mine): it boots the real app over HTTP against one recording upstream, in NODE_ENV=test and in production.
  - It sends RAW socket bytes and tags every request with `x-gate-id`.
  - It attributes upstream hits and key validations per request.
  - It captures every log line (a transport added to the app's own winston instance, plus console spies), every raw response and every upstream request.
  - It runs UNCHANGED at base (develop's `index.ts` and `auth.ts`, checked out into the clone) and at head, and writes JSON.
- `harness/compare.py` diffs base against head.
- **Mutants:** `harness/mut.py`. Each anchor must occur exactly once, `tsc --noEmit` runs on the service first, then the PR's new test file plus auth.test.ts. The file is restored with `git checkout` and its sha256 is compared with HEAD; all 14 restores matched.

## Findings

### G184-F1 — LOW (gate process; PRE-EXISTING code, not this PR): production-mode tests write `logs/` into whatever the cwd is, so my first suite run wrote into Wednesday's tree
- **FOUND:**
  - `utils/logger.ts` adds `winston.transports.File({filename:'logs/combined.log'})` when NODE_ENV=production, and the path is relative to the process cwd.
  - Production-mode cells (ks1234, ks1244 P1-P3 and others) therefore append to `<cwd>/logs/combined.log`.
  - My first full-suite run had cwd = Wednesday's root. It appended 85 lines (timestamps 17:44-17:45 local) to `/Volumes/DevMASTER/WEDNESDAY/logs/combined.log`. That file is gitignored (`.gitignore:161 /logs/`) and already existed: it dates from 22 Sep and already held gate 183's 16:48-16:49 lines.
  - I confirmed my 85 lines were exactly the contiguous tail (lines 7933-8017, all in my run window) and truncated the file back to its pre-run 7,932 lines / 870,070 bytes. Its mtime changed. `error.log` was untouched (13 Oct).
  - After that, every run used cwd `<workdir>/cwd`, and the logs landed there (gitignored).
- **TESTED:** line counts and timestamps of that file before and after. I did not check whether other gates' lines in that file came from the same cause; gate 183's 16:48 lines look like it.
- **HOW:** `grep -c` of the timestamp window; `tail -n 85 | grep -c` = 85 = total in window; first window line = 7933 = 8017-85+1.
- **Ask for gate_common.md:** "anchor every runner" should also pin the cwd: `bash -c 'cd <workdir>/cwd && …'`. `--root` alone does not stop this.

### G184-F2 — LOW: the stated reason for placing the refusal before `rejectConnectorBearer` is not pinned (mutant M10 survives)
- **FOUND:**
  - Moving `app.use(rejectRepeatedApiKey())` to just AFTER `app.use(rejectConnectorBearer())` leaves 38/38 green (tsc rc 0).
  - The index.ts comment says the order is chosen "so a malformed request is refused before any RS256 verify". No cell pins that.
  - By reading: the only request that differs is a connector-JWT Bearer plus a repeated key, which would get the connector refusal (401) instead of 400. Both refuse and forward nothing.
  - So this is equivalent on security outcome, but not on status or log event.
- **TESTED:** the mutant against the PR's tests. The swapped order was read, not driven, with a connector Bearer.
- **HOW:** `mut.py` M10; `runs/mut/table.json`.

### G184-F3 — INFO: the fail-closed `catch` in `rejectRepeatedApiKey` is unreachable on a Node-built request (mutant M11 survives, equivalent)
- **FOUND:** turning `next(err)` into `next()` survives. `carriesRepeatedApiKey` only iterates `rawHeaders` and calls `String()` and `.includes` on strings Node built, so nothing I can send makes it throw. The mutant is equivalent on reachable input.
- **TESTED / HOW:** M11, read plus run.

### G184-F4 — INFO: red-first count differs by one from the READY; the 3 pure cells are red at base by TypeError, not by assertion
- **FOUND:** with develop's `index.ts` and `auth.ts` the new file is **15 red / 4 green of 19**, not 16 / 3:
  - Green: CONTROL S, CONTROL C, CONTROL E and COMPLETENESS.
  - Red, 12 of them by AssertionError: A, B, D, F, G, H, I, J, K, P1, P2 and P3.
  - Red, 3 of them by `TypeError: carriesRepeatedApiKey is not a function` (the export does not exist at base): U1, U2 and U3.
  - auth.test.ts has 2 red at base (the two KS-1244 pins), both by assertion.
- The behaviour itself is red by assertion through the 12 integration cells, so this is not a blocker.
- **HOW:** `runs/redfirst_base.log` gives 17 failed / 21 passed of 38 (two files), with the failure kinds counted.

### G184-F5 — INFO: 3 production cells read "more permissive at head" in the mixed matrix; a control shows all 3 are rate-limit budget artefacts (0 after the control)
- **FOUND:**
  - In the production matrix (356 operations × 8 shapes), 3 zero- or one-key cells on `/api/v1/auth/mfa/*` and `/api/v1/users/me/mfa/*` returned 429 at base and 200/401 at head.
  - Cause: those limiters are fixed at 10 per 15 minutes in production. At base, the repeated-key requests to the same paths spent the budget first (base 429s 52 of 72 MFA cells; head 16). At head they are refused before the limiter.
  - **Control:** the same harness with ONLY the zero- and one-key shapes, at base and at head, gives **0 of 2,848 cells different** (test and production modes).
- **What this means:** a repeated-key request at head no longer counts against the path limiters mounted after the refusal (login, MFA and the rest). It also gets nothing: 400, 0 forwarded, 0 validations.
- **TESTED / HOW:** `runs/compare.txt`, `runs/compare_norep.txt`, `harness/compare.py`.

## What passed (measured)
- **Q1 Scope:** `git diff --name-only 5c1ca287ed74 defe782aaf61` = exactly the 6 files the READY lists. `services/auth/src/routes/users.ts` is not among them. One commit.

- **Q2 Every mount above the refusal** (head `index.ts`, refusal at :601, connector check :602). What a repeated-key request gets at each, read:
  - **:241 normaliseRepeatedSlashes:** path only.
  - **:259 helmet and :280 headers:** response headers only.
  - **:298 method allowlist:** 405 for TRACE and the like, the same with or without a key.
  - **:332 stripTrustHeaders:** the pattern `^x-(user|tenant|…)` does not match x-api-key.
  - **:358 cors:** answers a preflight. No key is read.
  - **:369 cookieParser.**
  - **:376-377 csrf generateToken and protect:** skips the token check when `x-api-key` is truthy, repeated included. The request then reaches the refusal. Measured as P1 below.
  - **:385 enforceJsonContentType:** 415 regardless of key.
  - **:410-417 body parsers:** parse non-proxied bodies before the refusal. This costs resources and uses no key.
  - **:450 rejectNulBytes; :456-457 sanitize and detectSuspicious;** `securityLog` logs ip, path and UA, no headers.
  - **:458 requestFingerprint:** UA and accept-* only.
  - **:459 bruteForce:** login path, keyed by IP.
  - **:462 request id.**
  - **:470 request log:** path, status, ip and UA, no key. A refused request logs one "Request completed … 400".
  - **:488 global limiter:** counts against the IP. That is a cost, not a gain.
  - **:516 versioning 307:** measured below.
  - **:523 unsupported-version 400; :548 v1 rewrite; :567 verification limiter:** counts.
  - **:582 audit:** a refused POST writes one audit row with method, path, status 400, `success=false`, null actor, ip and UA. No header value. This was read, not driven against a database.
  - **No route or router is mounted above :601.** :416 and :417 are body parsers.
  - **No mount above the refusal forwards, validates or logs the key.**

- **Driven in production mode, my harness, head:**
  - **P1** (POST `/api/v1/credentials/g184/revoke`, cookie, no CSRF token):
    - Control, no key: 403 `CSRF_ORIGIN_INVALID`, 0 hits.
    - Control, one valid key: 200, 1 hit with a minted Bearer, 1 validation.
    - Two lines: **400 BAD_REQUEST, 0 hits, 0 validations.**
    - One comma line without a space: **400, 0, 0.**
    - Base, same cells: two lines 200, 1 hit, anonymous (no Authorization), 1 validation; comma 200, 1 hit.
  - **P2** (GET `/api/v1/credentials`, bearerAuth, no Bearer):
    - Control, none: 401 `Authentication required`.
    - Control, one valid key: 200, minted Bearer.
    - Control, one junk key: 200 forwarded anonymously (the KS-736 residual, base = head).
    - Repeated: **400, 0 hits, 0 validations.**
    - Base, repeated: 200, 1 hit, anonymous.
  - **Versioning 307** (POST `/api/documents`, repeated):
    - **307** to `Location: /api/v1/documents`, **0 hits, 0 validations**, no key in the response.
    - Following the Location with a repeated key gives **400, 0, 0.**
    - With `?x=1` and one comma line: 307 to `/api/v1/documents?x=1`, 0 and 0.
    - Controls, no key and one key: 307 and 307.
    - Base: 307 likewise, and the follow gives 401 with 1 validation.

- **Q3 No key value leaves the process:**
  - The `REPEATED_API_KEY_REFUSED` call (auth.ts:458-466) carries headerLines, commaInValue, method, `baseUrl+path` and requestId. No value is read beyond the comma test.
  - Every key on a repeated request in the head run carried the marker `qzplant184`. The marker appears in **0 lines** of each of these:
    - the logs capture (2,860 `REPEATED_API_KEY_REFUSED` events in the same capture, so the instrument sees refusal lines);
    - the raw responses capture;
    - the upstream-requests capture (which shows the single-key marker `qzctl184` 2,638 times, so it sees key values);
    - the vitest output;
    - `cwd/logs/combined.log` (1,432 refusal events);
    - error.log.
  - Positive controls, same harness, mutant copies:
    - **M7** (value logged): 718 log lines carry the marker, and 361 lines in combined.log.
    - **M12** (value echoed in body): 718 responses carry it.
  - Base for contrast: the marker is in 2,510 upstream request records (forwarded) and in 0 logs.

- **Q4 No regression for zero or one key** (merge tree on develop 307d9b4c762a):
  - **Full api-gateway suite:** 152 files and 1,592 tests. **1,584 passed, 8 failed, rc 1.**
  - All 8 failures are in `ks1543-document-types-catch-logs-the-error.test.ts` and `ks1543-five-pre-existing-eslint-warnings-in.test.ts`, which lint `verification.ts` (untouched by this PR). They fail with `Cannot find package '@eslint/js'` because my workspace-scoped install has no root devDependencies.
  - That is my environment, not the PR. I did not re-run them on a full install (see NOT tested).
  - Counts reconcile with the READY: 151/1,589, plus PR 1998's 1 file and 3 tests, gives 152/1,592.
  - **Explicit:** `ks1234-production-mode-307.test.ts` **3/3**; the KS-1244 file **19/19**; auth.test.ts **19/19**; rc 0.
  - **Gate matrix, zero and one key** (zero, one valid, one junk `sk_`, one non-`sk_`) × 356 operations (spec plus unlisted mounts), test and production: **0 of 2,848 cells differ base → head** (status, upstream hits, validations, forwarded Authorization kind).
  - `tsc --noEmit` on the service at the merge tree: rc 0.
  - `docs-fragments.mjs check`: rc 0 "OK" (flow and cheat 144 new each; 2 ADVISORY lines, as the READY says).

- **Q5 Key character set:** both minting sites are `sk_` plus `randomBytes(32).toString('hex')`:
  - `services/security/src/index.ts:1215` (`POST /api/keys`);
  - `services/originate/src/routes/adminConfig.ts:1052`.
  - The character set is `[a-z0-9_]` (`sk_` plus 64 lower-hex), so **no minted key can contain a comma.**
  - No other generator matched my search (assignments from randomBytes, base64 or nanoid; `sk_live_` and `sk_test_` are Stripe config only).
  - `svc_api_keys` holds hashes only; migration 019 copied legacy `api_keys` hashes minted by the same originate endpoint.

- **Q6 Mutants (my own raw table, 12 mutants, all compiled with tsc rc 0 in the counted run):**

  | id | mutant | failed / 38 | killed |
  |---|---|---|---|
  | M1 | front door unmounted (`void rejectRepeatedApiKey;`) | 4 (A, B, D, I) | yes |
  | M2 | inner check in authenticateToken dropped | 2 (the auth.test pins) | yes |
  | M3 | raw line-count clause dropped | 1 (U1) | yes |
  | M4 | raw comma clause dropped | 1 (U2) | yes |
  | M5 | req.headers clause dropped | 3 (U3 + 2 pins) | yes |
  | M6 | status 401 | 13 | yes |
  | M7 | key value logged | 1 (G) | yes |
  | M8 | front door above versioning | 1 (P3) | yes |
  | M9 | front door just above the proxies (after the spec gate) | 4 (A, B, D, I) | yes |
  | M10 | front door after the connector check | 0 | **SURVIVOR** (F2, equivalent on outcome) |
  | M11 | front door fails open on a throw | 0 | **SURVIVOR** (F3, equivalent: unreachable) |
  | M12 | refusal body echoes the header | 12 | yes |

  - Count: **10 killed, 2 survivors, 12 run.**
  - The first pass had M1 and M3 deleting outright, which failed tsc (TS6133, unused). I re-ran both in a compiling form; the counts above are from the compiling run. The first-pass vitest counts were identical (4 and 1).
  - M1-M8 match the READY's per-mutant counts exactly.
  - Clean run of the two files after the mutants: 38/38.

- **Q7 Base vs head:**
  - Full matrix, 356 operations × 8 shapes × 2 modes = 5,696 cells.
  - Head **more permissive than base: 0** after the F5 control (3 raw, all limiter-budget artefacts, 0 in the controlled run).
  - Repeated shapes (two lines, one comma line, empty first line, junk plus valid): at head **every one of 2,848 cells is refused 400 with 0 hits and 0 validations.** At base, 376 (test) and 361 (production) of them reached an upstream.

- **Q8 Title and body:**
  - Commit subject = "Refs KS-1244: refuse a repeated x-api-key with 400 on every route", **65 chars** (≤ 92). It starts with Refs, has no close-word, and the key is the real one.
  - **PR title and PR body: UNMEASURED.** I used no gh login: Wednesday's identity is not the Secuura account (hard rule 5).

- **Q9 Merge:** rc 0, tree `1a5fd7a081a48375d4a1a8a6cc91b03710462c0f` on 307d9b4c762a. The end pin is unchanged.

- **Observed, PRE-EXISTING (base = head), not from this PR:** a single-key request is forwarded upstream with its `x-api-key` header still attached (`fwdKeyLines=1`), for valid and junk keys alike.

## NOT tested
- Node 24 (the image's line) or any LTS Node. Every number above is Node v26.8.1.
- The edge proxy (Caddy and nginx). HTTP/2. Whether an intermediary folds the two lines before the gateway.
- Real clients: Platform S and the WhatsApp bot. Whether any real client sends x-api-key twice or with a comma. This would turn into a 400 for them, and it is not measured anywhere.
- Any running gateway, deploy, database or Redis. The audit-row content for a refused request was READ, not driven against a database.
- The 8 ks1543 lint cells on a full root install. The test-types ratchet. eslint. The four platform suites. The pre-push preflight.
- The PR title and body text (Q8).
- A connector-JWT Bearer combined with a repeated key, driven (F2 is by reading).
- Legacy key values in any live database (hash-only; the format is inferred from the two minting sites).

## Plain answer for Kam
- If someone sends the API-key header twice (or two keys squeezed into one header), the gateway now turns them away straight away with a "send it once" error on every route.
- Before, some routes quietly treated such a request as an anonymous visitor and passed it on to the backend services, and in production that also slipped past the cross-site-request check. That stops with this change.
- Requests with no key or one key behave exactly as before. I checked 2,848 combinations against the old code and none changed.
- No key value is written to any log, response or forwarded request.
- Real keys are letters and digits only, so no genuine key can trip the new rule. The one risk I could not check is a real client (Platform S, the WhatsApp bot) that happens to send the header twice; it would now get an error instead of being served.
