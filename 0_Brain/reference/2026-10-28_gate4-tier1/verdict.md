# QA gate 4 (TIER 1, batch, round 1 of 2): Secuura #1779 (KS-1536 groundwork), #1782 (KS-1240 p4), #1785 (KS-1240 p1), #1786 (KS-1382)

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), tier-1 batch gate, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel. Routing receipt as commissioned: claude-opus-5-5, tier-1 gate (auth / tenant creation / gateway request path / stack-safety guard), gauge ~75%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear read-only (KS-1382, KS-1240, KS-1536 via spark_review's own reader; key never printed). Decision cards read with `decision_queue.sh show` (read verb only). `gh` not authenticated in this shell: PR bodies NOT read; each head's commit message stood in (and was fed to Spark as the PR description, flagged). Writes confined to my own clone, my own scratch worktrees, the work folder and this folder.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate4-tier1/repo` (did not exist; `git clone --shared .../spark/cache/src`; `rev-parse --show-toplevel` asserted equal to the path before the first fetch and inside every script that wrote to it; origin = GitHub, deploy key via GIT_SSH_COMMAND with `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`). Worktrees under `/private/tmp/claude-501/gatework4/` (w1779, w1782, w1785, w1786, wdevelop, m1785dev = scratch merge develop+#1785, sg* = spark_gate's own). NOT removed (no-delete rule). Each holds only a read-only node_modules symlink and my probe file (w1782); every product file I mutated was restored from `git show HEAD:` and `git status` read back clean apart from those.
- **node_modules:** read-only symlinks to `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules` (made with `os.symlink`; nothing installed, nothing written into the shared tree). Node v26.8.1 (not the repo's LTS 24) on every run.
- **Postgres / Docker:** none needed and **none started** (no PR here has a DB-backed cell). `docker ps -a` read back at the end: 0 names matching gate4 (of 229 containers on the host, none mine). **No stack on any slot**, and before the #1786 runs I checked no slot gateway was listening (listening TCP ports: 5000 7000 11002 42050 47787 47788 49281 49282 49288 50402 51724 55412 59869 64237; none of 6882/6982/7082/7182).
- **Load:** load1 10 to 17 during the runs (other seats). Heavy runs were gated by a background wait while load1 > 14; the api-gateway full suites ran at ~14-17, which matters for the timeout-sensitive cells they share with develop (see #1785).

## Pins (git ls-remote)

| ref | start (21:02) | end (21:24) |
|---|---|---|
| develop | **d531abd5f34bd32f3627149cfaf9b4e41e02fe1d** (NOT the brief's f23097c390e4: #1776 KS-1591 merged on top) | same (21:24) |
| refs/pull/1779/head | bb7a646c8db4bcb99f74aaf8f22613aa321f22c3 (= brief) | same |
| refs/pull/1782/head | 89335fe9c679cf36ad731e7f081234a7f2b1a445 (= brief prefix) | same |
| refs/pull/1785/head | e01a5094771d5ae69f3bf09fa0cfebf5b3008481 (= brief) | same |
| refs/pull/1786/head | 5d23044d272d7008031fd811cab332d40f8f7117 (= brief) | same |

Merge-base of all four with develop is bd6697e079fc. develop since: #1775 (packages/shared errors), #1781 (scripts/audit/audit-locks.mjs), #1776 (packages/shared keyRevokePolicy + services/security). **None of the four PRs touches any of those code files** (intersection 0 each, below). Merge-tree run against BOTH f23097c390e4 (the brief's develop) and d531abd5 (the real one): identical result.

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1779 | KS-1536 groundwork | **GO WITH NOTES** | Extraction is character-identical (Spark-gate differential, 0/29, reused) and I re-read every changed line; 9/9 head, 6/3 base; four own mutants each killed. No other check in services/auth uses the old inline form; seven OTHER admin-role checks exist in auth with DIFFERENT lists and folds (listed, scope note). Carried, not introduced: `hasAdminRole` still admits dotless-i / long-s spellings via `toUpperCase()`, which develop's #1776 just closed for the two security-side gates. |
| #1782 | KS-1240 p4 | **GO WITH NOTES** (one doc sentence to fix before merge) | At tenant-provisioning the claim holds: a hung key service now ends in the existing fail-soft 201, response shape and published contract byte-unchanged, 11/11 head, 3/8 base. **But the only front door, `POST /api/platform/tenants`, gives up at 8 s (platform.ts `UPSTREAM_TIMEOUT_MS`), before the 10 s bound fires**: measured (scaled), the caller gets the 504 and the tenant is completed afterwards, and a live metering key is minted that nobody receives. The PR's doc says "the gateway proxy waits 60 s", which is wrong for this route. Seat Y's slow-not-hung split (ACTIVE `tenant_keys` row, NULL `vault_key_hash`) reproduced at the provisioning side: a NOTE on the body's "no write changes", not a defect, because nothing reads either value today. |
| #1785 | KS-1240 p1 | **GO WITH NOTES** | 40/40 head, 20/20 base; I ran 18 mutants: 15 killed exactly where predicted, **3 survive, all on the same unpinned branch** (a non-OK 4xx answer from security: cached-as-401 / 429-as-rejection / every-non-OK-as-503). Security never answers a real rejection that way (it answers 200 `valid:false`, which IS pinned), so this is a test gap, not a wrong answer. 503 is returned only for an unverifiable key; the **optional-mount 503** and the **exchange-timeout = downstream 401** are two behaviours the cards did not rule on (notes). Two unbounded hand-built forwards remain on hot paths (`http.request` document upload and document create), outside "every fetch" by wording. api-gateway suite: identical 24 failures on develop and head (environmental), head adds 2 files / 40 cells, 0 new failures. |
| #1786 | KS-1382 | **GO WITH NOTES** | Proven by running every entry point for real under `env -i` with stubbed curl/docker/python3/tsx in their own process group: **no slot named -> all six (five scripts + runner.ts) refuse rc 2 naming the missing slot, zero tool calls**; at base the same five reach curl/docker/python on `localhost:6882`. **Slot named -> unchanged** for slot 1, for TARGET_BASE given (CI path), and for an agreeing slot+TARGET_BASE; slot 3 / alias STACK_SLOT=2 now aim at 7082 / 6982 (the fix). PR test 175/175, stderr fixture test 5/5 (0/5 with the fixture line reverted), check-stack-safety 110 invariants OK; seven own mutants of 3d and of the entry block each go red, and a non-hit control stays green. Notes: the split-target refusal is bypassed by `LOCALHOST`, `HTTP://`, `0.0.0.0`, `127.0.1.1` spellings (Low); the Azure RUNBOOK's pre-deploy audit step now refuses until it names a slot (disclosed, runbook not updated). |

**Recommended merge order: #1779, #1786, #1782, #1785.** All four are disjoint in code from each other and from develop's three new commits; only the two Projects Documents html files conflict (everywhere, both orders, as expected). #1779 first (smallest, behaviour-preserving, auth). #1786 next (scripts/harness only, no product code). #1782 after its one doc sentence is corrected (or before #1785 if Wednesday accepts the sentence as a merge-time edit). #1785 last: the largest product change and the one with a user-visible answer change (401 -> 503) and two unruled behaviours to nod through.

**Docs sections** (develop's highest is **85** now that #1776 is in; #1780 = 86 per brief; 87-90 assigned to #1783, #1777, #1778, #1784): **#1779 = 91, #1786 = 92, #1782 = 93, #1785 = 94.** Heads carry: #1779 `84` (84.1-84.3), #1782 `85` (85.1-85.4), #1785 `84` (84.1-84.5), #1786 `84` (84.1-84.5) **plus an in-text "section 84" that must be rewritten too**. Every head's block in both docs is a pure insertion before the single `</body>` (checked: head == base[:i] + block + base[i:] against bd6697e, all eight files). Cheat-sheet `<h2>`s unnumbered.

---

## Spark shadow (run FIRST, per PR; `out/p<n>/`)

Method: `spark_gate.sh` per PR (work under `/private/tmp/claude-501/gatework4/sg<n>`, `--node-modules` = Dev root), then `spark_review.py` with `facts_spark.json` = facts minus the two Projects Documents html files (~1.29 MB, refused) plus HARNESS LIMIT lines, and the head commit message as the PR description (flagged).

| PR | spark_gate (head / base product code) | Spark review |
|---|---|---|
| #1779 | 9 / 0 ; 6 pass / **3 fail** (matches the PR) | GO WITH NOTES, 9 Notes; 48.2 s, 22,111 prompt tokens |
| #1782 | 11 / 0 ; 3 pass / **8 fail** (matches the PR) | NO GO, 4 Major 3 Minor 2 Note; 77.2 s, 25,833 tokens |
| #1785 | 40 / 0 ; 20 pass / **20 fail** (matches the PR's "20 red at base") | NO GO, 3 Major 3 Minor 2 Note; 187.5 s, **191,092 prompt tokens** (proxy.ts and admin.ts full text) |
| #1786 | **NOT RUN, deliberately, and not counted.** Shell-only PR: spark_gate would run the PR's .sh test on BASE product code, where the five entry points have no resolve-only seam and default to slot 1's gateway; that arm would execute them for real (my stubbed base runs below show they reach curl / docker / python on :6882). The harness is also vacuous here in the usual sense. Facts for the review were assembled from MY head-only runs (175/0, 5/0) with HARNESS LIMIT lines. | attempt 1: **SCHEMA FAILURE x2** (repetition abort on a false claim, `p1786/spark/`). Retry `p1786/spark_retry/`: valid, NO GO, 4 Major 3 Minor 1 Note; retry 90.7 s, 153,442 prompt tokens as reported by its meta; the failed first run cost another 153,442 |

---

## #1779 (KS-1536 groundwork, Spark pass): GO WITH NOTES

Head bb7a646c8db4. Files: `services/auth/src/routes/issuerCerts.ts` (+13/-8), new test (115 lines, 9 cells), two docs.

### Reading every changed line
The four gates (`isAuthorisedForCertWrite/Read/Revoke/Sign`) each lose exactly two lines, `const role = String(user.role ?? ''); if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;`, and gain `if (hasAdminRole(user.role)) return true;` at the same position (after `if (!user) return false;`, before the scope checks, which are context lines). `hasAdminRole(role: unknown)` is the same expression over the same argument. `ADMIN_ROLES` untouched. The Spark-gate half's differential (old inline vs helper, 29 inputs incl. undefined/null/arrays/objects with toString/NaN/look-alikes: **0 differences**) is reused, not re-run; it is weak by construction (same expression), so the reading is the evidence.

### Mutants (own worktree, restored; `out/mut1779/`)
| mutant | result (9 cells) | red |
|---|---|---|
| M0 head | 9 / 0 | none |
| K1 helper drops the upper-case fold | 6 / 3 | R2, R3, C2 |
| K2 sign gate drops the helper call | 7 / 2 | C1, C2 |
| K3 read gate re-inlined as an exact match | 7 / 2 | R3, C2 |
| K4 helper admits everyone | 5 / 4 | R2, C3, C5, C6 |

### Other admin-role checks in services/auth (head, non-test; the brief's question)
**None still uses the old inline form** (`String(role ?? '')` + `includes(x) || includes(x.toUpperCase())`): `git grep` finds it nowhere outside `hasAdminRole`. Seven OTHER checks exist, each with its OWN list and fold. They differ from `hasAdminRole`; that is KS-1536's subject (the divergent lists), so it is a **scope note, not a defect of this PR**:

| site | list | fold |
|---|---|---|
| `middleware/authenticate.ts:228` (owner-or-admin) | SYSTEM_ADMIN, ORG_ADMIN, super_admin, SUPER_ADMIN | exact (no ISSUER_ADMIN, no `admin`) |
| `middleware/authenticate.ts:249` (same-org bypass) | SYSTEM_ADMIN, super_admin, SUPER_ADMIN | exact |
| `routes/oauth.ts:1156/1163` platform admin | SYSTEM_ADMIN, SUPER_ADMIN, admin, super_admin | exact |
| `routes/oauth.ts:1157/1166` app admin | SYSTEM_ADMIN, ORG_ADMIN, ISSUER_ADMIN, admin, super_admin, SUPER_ADMIN | exact |
| `routes/users.ts:193/196` `isPlatformAdmin` | SYSTEM_ADMIN, SUPER_ADMIN, admin, super_admin | exact |
| `routes/users.ts:443, 499, 555` (local `ADMIN_ROLES`, three copies) | SYSTEM_ADMIN, ORG_ADMIN, ISSUER_ADMIN, admin, super_admin, SUPER_ADMIN | exact |
| `routes/users.ts:587` admin/create | SYSTEM_ADMIN, ORG_ADMIN, super_admin, SUPER_ADMIN | exact |
| `routes/users.ts:285, 377` lookup | `ALLOWED_LOOKUP_ROLES` | upper-case only |
| (`services/password.ts:234` `minLengthForRole`: not a gate, a length rule) | | |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1779-1 | Low (carried, not introduced) | `hasAdminRole` admits `'ıssuer_admin'`, `'ſuper_admin'`, `'org_admın'` (each `.toUpperCase()` lands in ADMIN_ROLES; measured in node). Develop's #1776 (merged today) made `isPlatformRole` / `requireKeyAdmin` exact-ASCII; the issuer-cert gates are now the remaining admin gate with the Unicode fold. Exploit needs a JWT carrying such a role (role is server-assigned), so Low. Natural next unit of KS-1536/KS-1591. | FOUND by reading; TESTED in node (3 inputs). |
| 1779-2 | Info | `hasAdminRole` is exported from a route file; nothing imports it. | `git grep`. |
| 1779-3 | Info (scope) | The seven divergent lists above are untouched (PR says "groundwork"). | `git grep`, table. |
| 1779-4 | Low (merge-time) | Docs carry 84; use **91**. | |

Spark GO WITH NOTES, 9 Notes, none a defect; agrees.

---

## #1782 (KS-1240 part 4, tenant-provisioning bounded fetches, signals only): GO WITH NOTES

Head 89335fe9c679. Files: `index.ts` (+6: the constant and one `signal:`), `meteringKey.ts` (+9/-1), new test (283 lines, 11 cells), two docs.

### What the brief asked
- **Response shape byte-unchanged in the published contract: YES.** No openapi file in the diff (`tenant-provisioning.openapi.ts`, `docs/openapi/secuura-api.yaml` untouched); the handler's `res.status(201).json(...)` and the 500 path are context lines; the PIN cell PBP1 pins today's unreachable answer.
- **Timeouts bounded and released: YES (read).** Two `AbortSignal.timeout(10_000)`, one per fetch, created per request. The signal also covers `res.json()` (key gen) and the body read in `requestMeteringKey`. `AbortSignal.timeout` uses an unref'd internal timer that needs no clear; nothing holds the process. Worst case for the route is 20 s (both hang, sequential), which the PR states.
- **Nothing new can leave a tenant half-made: the TENANT ROW, yes; the system, no** (two new split states, below). The `tenants` row can no longer stick at `provisioning` from a hung key service (measured, base vs head, G1); both expiries land in the try/catch each call already sat in.

### My probe (scratch file in my worktree, the PR's own harness; `out/probe1782_head.txt`; scaled 1:10: gateway budget 8 s -> 800 ms, provisioning bound 10 s -> 1000 ms)
| | base (bd6697 product files) | head |
|---|---|---|
| G1 hung tokenisation, caller gives up at the gateway's budget | caller gave up at 805 ms; writes ever: `INSERT INTO tenants` only (stuck `provisioning`); metering mints: 0 | caller gave up at 808 ms; **afterwards** the server wrote `tenant_config` (NULL hash), `UPDATE ... active`, audit row, and **the security stub served 1 metering-key mint** to a caller that had gone |
| G2 SLOW tokenisation (answers 200 ms after the bound) | 201, `vault_key_hash = 'hash-ks1240'` | 201, **`vault_key_hash = NULL`** although the key service answered and (per Seat Y, exercised) inserted its `tenant_keys` row |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1782-1 | **Medium (claim vs front door; fix the doc sentence before merge)** | The only gateway route to tenant creation is `POST /api/platform/tenants` (`api-gateway/src/routes/platform.ts:314-324`), forwarded with `fetchWithTimeout` at `UPSTREAM_TIMEOUT_MS = PLATFORM_UPSTREAM_TIMEOUT_MS || 8000` (`:132`; ENVIRONMENT-VARIABLES.md:237 documents 8000; no compose override found). The new bound is 10 s, so through the front door the caller ALWAYS gets the gateway's **504 at 8 s**, never the fail-soft 201; tenant-provisioning keeps going (a client disconnect does not stop the handler), completes the tenant, and mints a live single-tenant `metering:read` key whose one-time material goes to nobody. A retry then meets 409 (slug exists). The PR's doc 85.3 says "the gateway proxy waits 60 s (`proxy.ts` lines 136 and 165 to 166)": that is the generic proxy, **not the route tenant creation uses**. Not a regression (base: 504 at 8 s and a tenant stuck forever), but the PR's stated outcome holds only for a direct caller, and Kam's card c / a-vs-b choice is about what the caller is told. Options for the seat: bound each fetch so both fit inside 8 s (e.g. 3 s), or keep 10 s and correct the sentence + say "the gateway answers 504 first". | FOUND by reading platform.ts; TESTED by the scaled probe G1 (base and head). Not run through a real gateway. |
| 1782-2 | Low, NOTE on the body wording (Wednesday's question on Seat Y's trace) | **Judgment: NOTE, not a defect.** The body says a hung service and an unreachable one "end identically" (true, measured) and "Only the bounds change ... no status, body or write changes". For a service that is merely SLOW past 10 s, the WRITES do change: base waited and stored the hash; head stores `vault_key_hash = NULL` (my G2) while tokenisation completes its INSERT and holds an ACTIVE wrapped key for the tenant (Seat Y, `generate_key_abort_probe.json`). So "no write changes" overstates for the slow case. Not a defect because (Seat Y, read + controls) nothing reads `tenant_config.vault_key_hash` and nothing reachable reads `tenant_keys` (`rotate-key` has no caller); and the same split already arises at base for any client-side give-up. Consequence to carry: a later `generate-key` for that tenant would collide on `UNIQUE (tenant_id, version, status)` (read, `migrations/029:21`; not executed), so "will need manual generation" would 500. Body fix: "a hung or unreachable service ends identically; a service slower than 10 s now also ends there, which can leave a stored key whose hash the tenant row does not record". | FOUND: Y's trace + my G2; TESTED G2 base vs head; the unique-constraint collision is read only. |
| 1782-3 | Low | Same shape on the metering side: a security service slower than 10 s mints the key, the route answers `meteringApiKey: null`, and a live credential exists that nobody holds (manual re-mint makes a second). | Read; G1 shows the mint happening after the caller left. |
| 1782-4 | Low (merge-time) | Docs carry 85 (collides with develop's #1776 = 85); use **93**. | |

### Spark findings judged (NO GO, 4 Major)
Major 1 (log lines not compared): true but immaterial, the PR claims only status/body/writes identical. Major 2 and 3 (the unbounded base behaviour is described, not asserted): TRUE as stated, but that is base behaviour, and my G1 base run reproduces it (`INSERT INTO tenants` only). Major 4 ("a signal is a change to the outbound request"): FALSE as a defect, sophistry on "only the bounds change". Minor PB8 ceiling not exact: covered by PB5, which pins [10000, 10000]. Net: **no Spark defect stands; Spark missed 1782-1 (the 8 s front door) and 1782-2.**

---

## #1785 (KS-1240 part 1, api-gateway bounded validate/exchange and forwards; 401 -> 503): GO WITH NOTES

Head e01a50947710. Files: `middleware/auth.ts` (+124/-…), `routes/admin.ts`, `audit-export.ts`, `batch.ts`, `proxy.ts`, two new test files (40 cells), two docs.

### Reading the change against the cards
Cards read: `secuura-ks888-revoke-validate-on-failed-save` = a ("Validate: refuse 503 (fail closed)", about the security service's own validate on a failed save) and `secuura-ks1370-validate-when-the-revoke-check-cannot-read` = a (security answers 503 'Unable to verify key' when a configured DB cannot be read; the card's own BLUF names the gateway's 30 s cache of any refusal as the cost). The PR makes the gateway (a) stop caching a 5xx/408/429 or an unreadable/timed-out answer and (b) answer it 503 `SERVICE_UNAVAILABLE` "Unable to verify API key, please retry" instead of 401 "Invalid API key". That is the cards' "unverifiable key is refused with 503" carried to the front door.

**Where 503 is returned (head, by reading `checkApiKey` and `authenticateToken`):** ONLY when a presented `sk_` key's check is `unavailable` = fetch threw (timeout, connect failure), body unreadable/unparseable or timed out mid-body, or security answered >= 500, 408 or 429. **Unchanged:** no key; a non-`sk_` key; a key security answers 200 `valid:false` (401 on required, 30 s cache, KS-1207 fall-through on optional: pinned by two controls); a key security answers with another non-OK 4xx (401, cached; unpinned, see 1785-1); a valid key. Security's real rejection shape is 200 `valid:false` (`security/src/index.ts:1797` handler: 400 only for a missing key, 503 for the stored-read failure, 200 `valid:false` for not found / revoked / expired), so the 4xx branch is effectively unused.

**"No valid request path now times out under 60 s":** every forward is 60 s, equal to `proxyTimeout: 60000` / `timeout: 60000` / breaker `requestTimeoutMs: 60_000` (`proxy.ts:93, 166, 195-196`), so none is tighter than the generic proxy. **The exception is by design:** the two front-door calls are 5 s, on the path of every `sk_` request. A VALID key whose validation takes > 5 s now answers 503 (was: waited); a valid key whose connector exchange takes > 5 s now proceeds with no Bearer and a Bearer-only upstream answers 401. Base had no bound at all. Batch items: 60 s each; if items run one after another a batch has no overall bound, but no item fails under 60 s.

### Mutants (own worktree `w1785`, product file rewritten and restored from `git show HEAD:`; both new files, 40 cells; `out/mut1785/`)
| mutant | result | red |
|---|---|---|
| M0 head | 40 / 0 | none |
| F1 validate fetch without signal | 33 / 7 | census x2, (i), (ii), optional, log, 5 s-bound |
| F2 exchange fetch without signal | 35 / 5 | census x2, 5 s-bound, exchange-hang, exchange-stall |
| F3 security 5xx cached as a rejection (base semantic) | 38 / 2 | own-503 cell, not-cached cell |
| F4 unavailable answers 401 on required | 36 / 4 | (i), (ii), own-503, optional |
| F5 optional mount serves an unverifiable key as anonymous | 39 / 1 | optional |
| F6 unavailable result cached 30 s | 37 / 3 | (i), (ii), log |
| **F7 429 treated as a rejection (401, cached)** | **40 / 0, SURVIVES** | none |
| **F8 every non-OK status treated as unavailable (a 4xx rejection becomes 503)** | **40 / 0, SURVIVES** | none |
| F9 validate bound 5 s -> 60 s | 37 / 3 | (i), log, 5 s-bound |
| F10 admin.ts `jsonOrEmpty` swallows a timeout | 38 / 2 | admin create, admin PATCH |
| F11 proxy.ts `jsonOrEmpty` swallows a timeout | 36 / 4 | user create, user PATCH, signatories, third-party-verifiers |
| F12 MCP headers set before the body read (base order) | 39 / 1 | MCP stall |
| F13 batch body read swallows a timeout | 39 / 1 | batch stall |
| F14 batch bound 60 s -> 30 s | 39 / 1 | batch stall |
| F15 audit-export without signal | 37 / 3 | census x2, audit stall |
| F16 signatories without signal | 37 / 3 | census x2, signatories stall |
| F17 admin PATCH signal from a never-firing AbortController (Spark's Major 1) | 39 / 1 | admin PATCH stall (behavioural cell catches what the census cannot) |
| **F18 a non-OK 4xx rejection not cached** | **40 / 0, SURVIVES** | none |

**Full api-gateway suite** (vitest json, `out/suite1785/`; develop d531abd5 vs head; load 14-17): develop **127 files / 1273 tests, 24 failed**; head **129 files / 1313 tests, 24 failed**; **the failing set is identical by (file, title)** (ks1090 type-baseline, ks1195 register-connector, ks1215 register-connector cells and others: environment/load, present on develop, not diagnosed). Head adds +2 files / +40 cells, 0 new failures.

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1785-1 | Low (test gap) | F7, F8, F18 survive: the `!resp.ok` branch for a status that is NOT >= 500/408/429 (cache 30 s, answer 401) and the 429 classification have no cell. A later edit that turns every non-OK into 503, or drops the cache, goes unseen. Harmless today because security does not answer a rejection that way. One cell with a 403 stub and one with a 429 stub would pin it. | TESTED (mutants above). |
| 1785-2 | **Low-Medium (beyond the cards: needs a nod)** | **Optional mounts now answer 503** for an unverifiable key (8 `authenticateToken(false)` mounts: `admin.ts:1505, 1538`, `proxy.ts:662, 996, 1079, 1168, 1185, 1234`). Base: an unverifiable key on an optional mount fell through to the Bearer path / anonymous. The cards rule what security's validate answers, not optional mounts. Also: a request carrying an unverifiable key AND a valid Bearer on an optional mount now gets 503 where base authenticated it by the Bearer. The code comment argues it well ("the caller asked to be the key's principal") and F5 shows it is pinned; it is a product call to confirm, not a defect. | FOUND by reading auth.ts:432-441; TESTED by F5. |
| 1785-3 | Low (unruled shape) | A connector-exchange **timeout** leaves the request with no Bearer, so a Bearer-only upstream answers **401** for a key that was just validated (unchanged from base's unreachable-exchange behaviour; the PR keeps it deliberately and logs "timed out"). KS-1240's own text suggests "a 503 on timeout". A transient fault reads to the client as an auth failure. Decide or file. | FOUND by reading auth.ts:495-498 and the ticket; TESTED by the PR's exchange cells and F2. |
| 1785-4 | Low (scope on the same surface) | Two hand-built forwards on hot request paths remain unbounded: `proxy.ts:620` (`http.request` for `POST /api/documents/upload`) and `verification.ts:900` (`http.request` for document create). Neither is a `fetch(`, so the census and the title ("every hand-built api-gateway fetch") are accurate by wording; they are the same hang shape KS-1240 is about (the sibling at `verification.ts:559` does carry `setTimeout`). `services/tokenisation.ts:110, 145` are unbounded but have no caller (the census's own exception list says so; Seat Y's trace agrees). | FOUND by `grep` over api-gateway src; not executed. |
| 1785-5 | Info | `validateApiKey` is kept but now has no caller in src. | grep. |
| 1785-6 | Info | Develop's #1775/#1776 changed `packages/shared`, which api-gateway imports; the run resolves `@secuura/shared` through the shared tree's node_modules, so neither arm exercised develop's shared source. No #1785 line touches a shared symbol changed there (read). Scratch merge develop+#1785 built (`m1785dev`, commit 7567712c847f) but not run for that reason. | Read. |
| 1785-7 | Low (merge-time) | Docs carry 84; use **94**. | |

### Spark findings judged (NO GO, 3 Major)
Major 1 (census checks only that a `signal` key exists): TRUE of the census, but **not a gap in the PR's evidence**: F17 (never-firing controller) is killed by the behavioural stall cell, and every one of the eleven sites has such a cell (F10-F16). Major 2 (`validateAs[SEC503]` mutated and not restored): read the file: `KEYS.SEC503` appears only at lines 216 and 221-225, the two consecutive cells that use it on purpose (503, then "answers again"); no later cell uses that key. True that it is not restored, no effect. Not a defect. Major 3: the model withdrew it in its own text ("this is not a finding"). Minors: two withdrawn in-text, one (order of `asked`) wrong (the array order IS asserted). **No Spark defect stands.** Spark missed 1785-1 (the surviving mutants), 1785-2, 1785-3 and 1785-4, on a 191k-token prompt.

---

## #1786 (KS-1382, no silent slot-1 default in the Blockchain/Testing entry points): GO WITH NOTES

Head 5d23044d272d. Files: the five entry points (`ci/orchestrate.sh`, `ci/tools/run-schemathesis.sh`, `jobs/05-dast-zap.sh`, `jobs/06-tenant-isolation.sh`, `run-internal-audit.sh`) each get the same resolution block; `tests/tenant-isolation/runner.ts` refuses without TARGET_BASE; `check-stack-safety.sh` +86 (3d); new test (287 lines); the granted one-line fixture change in `tenant_isolation_stderr_own_file.test.sh`; two READMEs; two docs.

### Method
`p1786/drive.sh`: runs an entry point **for real (no resolve-only seam)** under `env -i`, PATH = a stub dir first (curl, docker, python3, tsx, node, npx, wget, nc: each logs its argv; `docker info` answers 0; anything else kills the run's own process group, started with `setpgrp`), so the first stack-reaching call is recorded and nothing reaches a network. runner.ts via the real node. Matrix in `out/p1786_matrix.txt`; runs in `/private/tmp/claude-501/gatework4/p1786/runs/`. The five blocks are byte-identical (one sha, `f6f3a5b474cb3195`, my own hash).

### The brief's two proofs
**No slot named, no TARGET_BASE -> every entry point REFUSES, none reaches a stack:**
| entry | head | base (develop, same files as bd6697) |
|---|---|---|
| ci/orchestrate.sh | **rc 2**, stderr "No stack slot named ...", **0 tool calls** | reaches `curl ... http://localhost:6882/health` |
| ci/tools/run-schemathesis.sh | **rc 2**, same, 0 calls | reaches `python3 scripts/run.py test-fast --base-url http://localhost:6882` |
| jobs/05-dast-zap.sh | **rc 2**, same, 0 calls | reaches docker / `curl .../6882/health` |
| jobs/06-tenant-isolation.sh | **rc 2**, same, 0 calls | reaches `curl .../6882/health` |
| run-internal-audit.sh (05 06) | **rc 2**, same, 0 calls | reaches `curl .../6882/health` |
| tests/tenant-isolation/runner.ts | **rc 2**, same wording, 0 calls | not run (base defaults to :6882 and would send real requests; read at base line `const BASE = process.env.TARGET_BASE \|\| "http://localhost:6882"`) |
Also refused: `TARGET_BASE=` empty with no slot; ambient `GATEWAY_PORT=6882 COMPOSE_PROJECT_NAME=dev` with no slot; `SECUURA_STACK_SLOT` = `abc`, `0`, `99`, `' '` (stack_env.sh's own error, rc 2).

**Slot named -> behaviour unchanged** (all five entries, head vs base, first URL each reached):
| case | base | head |
|---|---|---|
| `SECUURA_STACK_SLOT=1`, no TARGET_BASE | 6882 | **6882** (unchanged) |
| `TARGET_BASE=https://audit.example.invalid`, no slot (CI path) | that URL | **that URL** (unchanged) |
| `SECUURA_STACK_SLOT=2 TARGET_BASE=http://localhost:6982` (agree) | 6982 | **6982** (unchanged) |
| `SECUURA_STACK_SLOT=3`, no TARGET_BASE | **6882 (the bug)** | **7082** (the fix) |
| `STACK_SLOT=2` alias | 6882 | 6982 |
| `SECUURA_STACK_SLOT=3 STACK_SLOT=2` | | 7082 (SECUURA wins, as documented) |
| `SECUURA_STACK_SLOT=2 GATEWAY_PORT=6882` (ambient) | | 6982 (ambient ignored) |
| `SECUURA_STACK_SLOT=2 TARGET_BASE=http://localhost:6882` (split) | 6882 | **rc 2** "is slot 1's gateway, but slot 2 was named" (also `[::1]`, `/api` suffix, slot 1 + 127.0.0.1:6982) |

### Tests and mutants
- PR test at head: **175 passed / 0 failed** (stubbed curl/docker/python3: 0 calls). Needed `Blockchain/Dev/node_modules/.bin/tsx` (symlinked read-only). `tenant_isolation_stderr_own_file.test.sh`: head **5/5**; with the fixture line reverted to base (the granted change undone) **0/5**, so the fixture line is required and sufficient, and it targets `http://localhost:1` (no slot's port).
- `check-stack-safety.sh` at head: rc 0, "110 shared-stack safety invariants hold".
- 3d mutants (`out/p1786_mut_*.txt`): plant `http://localhost:6982` -> rc 1; plant `$((6882 + 100 * (N - 1)))` -> rc 1; plant `psql -p 6632` (slot 3 Postgres) -> rc 1; plant in README.md -> rc 1; plant `v1.6882 2026-6882 1688200` (non-hits) -> rc 0; remove the `reconfirm-5xx.test.mjs` exception -> rc 1; add a stale exception -> rc 1 "excuse nothing any more". (A plant of 7432, not a published port, stays rc 0: correct.)
- Entry-block mutant: job 06 given back a slot-1 fallback -> PR test **171 / 4** (refusal cell, empty-vars cell, byte-identity cell, real-guard control).

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1786-1 | Low | The split-target refusal regex is lower-case and host-literal: with slot 2 named, `TARGET_BASE=http://LOCALHOST:6882`, `HTTP://localhost:6882`, `http://0.0.0.0:6882` and `http://127.0.1.1:6882` are ALL accepted and the run aims at slot 1's gateway. It needs an explicitly typed wrong URL, so it is not the "forgot the variable" shape the ticket is about, but it is the KS-1373 split-target shape the acceptance names. Lower-casing the URL and adding `0.0.0.0` / `127.0.0.0/8` closes it. | TESTED (four runs, `x_upper`, `x_scheme`, `x_0000`, `x_127b`). |
| 1786-2 | Info (scope) | 3d covers `Blockchain/Testing/**` only (as the ticket says); slot literals elsewhere are KS-1381 / KS-1355 / KS-1162. `integration/github-actions-snippet.yml` keeps `:6882` under a KS-1162 exception (acceptance point 4 waits on KS-1162). | Read. |
| 1786-3 | Info | `run-schemathesis.sh` resolves TARGET_BASE, then hands it to `systemTest/schemathesis/scripts/run.py`, whose own slot logic is KS-1373's; on the CI path (TARGET_BASE, no slot) I did not check what run.py does with an unset slot. | Not tested. |
| 1786-4 | Low (disclosed follow-up) | `Blockchain/Dev/deployment/azure/RUNBOOK.md` Phase 0.4 (pre-deploy checklist, line 56) runs `./run-internal-audit.sh` with no slot and no TARGET_BASE; at head that step now refuses rc 2, and the checklist says not to proceed without an audit pass. Safe direction (it used to audit whatever owned slot 1), and the PR's doc 84.4 discloses it, but the runbook is not updated: one line (`SECUURA_STACK_SLOT=<n>`) in a follow-up, or Kam will meet it at the next deploy. Spark's attempt-1 Major 1 is this. | FOUND in Spark raw attempt 1 + the PR's doc; READ RUNBOOK.md:53-63; the refusal itself TESTED (matrix). |
| 1786-5 | Info | The byte-identity cell's expression carries dead code (`printf ... \| grep -c . \| sed 's/^/x/' >/dev/null;` before the real `sort -u \| grep -c .`). The real half counts DISTINCT hashes, so it is not vacuous (my E1 mutant turned it red). | Read test line 216; TESTED E1. |
| 1786-6 | Low (merge-time) | Docs carry 84 and an in-text "section 84"; use **92** and rewrite both. | grep. |

### Spark findings judged (retry review; first attempt invalid)
Major 1 (RUNBOOK.md:56 caller now refuses): **TRUE, disclosed by the PR's doc 84.4**, carried as 1786-4 (Low). Major 2 (runner.ts cell depends on host tsx/Node): true of every cell in this repo, not a defect. Major 3 (guard bypass by `+6882` or leading zeros): **half true**: my plants show `X=+6882` IS caught (rc 1), `http://localhost:06882` is NOT (rc 0), nor is computed `$((6800+82))` (rc 0); a static literal guard cannot see computed or zero-padded ports, so Info. Major 4 (section 13 tests a copy of the guard): it copies the REAL guard file into a fixture repo, and a separate CONTROL runs the real guard on the real tree (my E1 mutant turned that control red); not a defect. Minor (byte-identity "flawed"/attempt 1's "vacuous"): **FALSE**, it counts distinct hashes (E1 red), the dead first half is 1786-5. Minor (runner could hang): runner refuses at module top before any request (my head run: rc 2, 0 calls). Minor (git init could be vacuous): the guard fails on an empty file list by design (3d's "nothing to check" branch). **One Spark point stands (Major 1, Low); none is a defect in the change.**

---

## Merge-tree (all in my clone, `git merge-tree --write-tree --name-only`; `out/mergetree.txt`)

| merge | rc | conflicts |
|---|---|---|
| f23097c390e4 + each of the four | 1 | exactly the two Projects Documents html files |
| d531abd5 (real develop) + each of the four | 1 | the same two files only |
| every ordered pair of the four (12) | 1 | the same two files only; no code file |

**No two PRs share a code file:** pairwise intersection of non-doc files, 6 pairs, all **0** (control: #1785 with itself = 7). Each PR's intersection with develop's three new commits (code) = **0**.

## What I did NOT test

- Any real gateway, stack, deploy, Docker container, Postgres, Node 24, CI itself; the four platform suites; PR bodies (gh unauthenticated).
- #1779: the real `authenticate` middleware path (the test mocks it); live issuer-cert requests; the services/auth full suite (the Spark-gate half ran it: 1200 -> 1209 cells, same 1 failing cell both sides).
- #1782: a real gateway in front (the 8 s/10 s race is a scaled probe plus reading); the `UNIQUE` collision of a second generate-key (read only); Platform S or any consumer outside the repo of `vault_key_hash` / `keyFile` (Seat Y lists the same); the tenant-provisioning full suite.
- #1785: a real security or auth service; the eight optional mounts one by one; the two remaining `http.request` forwards under a hang (read only); develop's `packages/shared` source under the gateway (node_modules resolves the shared tree).
- #1786: `run.py`'s slot handling on the CI path; the `.github` workflows; base runner.ts (not executed by design); Linux bash (host bash only).

## Spark calibration rows (one per PR)

| PR | Spark verdict | This check | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1779 | GO WITH NOTES (9 Notes) | GO WITH NOTES | 0 (Notes are true scope facts: groundwork, R3 brittle, auth mocked) | 1779-1 (the Unicode fold still admitted, now the odd one out after #1776) | **Right verdict, generic Notes.** It listed six other files with lists but did not check any of them. |
| #1782 | NO GO (4 Major, 3 Minor, 2 Note) | GO WITH NOTES | 0 | **1782-1 (8 s front door beats the 10 s bound)**, 1782-2 (slow-not-hung split) | **False NO GO.** Two Majors asked for base behaviour to be asserted (my base run reproduces it), one is wording sophistry; the real issue sat one file over (platform.ts) and was not in its prompt. |
| #1785 | NO GO (3 Major, 3 Minor, 2 Note) | GO WITH NOTES | 0 (Major 1 is a true property of the census but F17 shows the behavioural cells cover it) | 1785-1 (three surviving mutants), 1785-2 (optional-mount 503 beyond the cards), 1785-3 (exchange-timeout 401), 1785-4 (unbounded `http.request` forwards) | **False NO GO on a 191k-token prompt**; two of its own findings were withdrawn in its own text. |
| #1786 | attempt 1 invalid (schema failure x2); retry NO GO (4 Major, 3 Minor, 1 Note) | GO WITH NOTES | 1 (Major 1, RUNBOOK caller: true, disclosed by the PR, Low as 1786-4); half of Major 3 (leading-zero port evades the guard: Info) | 1786-1 (case/host bypass of the split refusal); it never ran an entry point | **False NO GO** at ~307k prompt tokens over four attempts; its loudest claim (byte-identity cell "vacuous") is refuted by mutant E1, "+6882 evades" is refuted by a plant. |

Reading: four reviews, one GO WITH NOTES that agrees, three NO GO with zero confirmed defects (one true, disclosed, Low point in #1786). The pattern from gates 2 and 3 holds: a Spark NO GO on these PRs is a prompt to run mutants, not a defect signal; none of its Majors survived. The findings that mattered here (the gateway's 8 s budget, the surviving 4xx-branch mutants, the case bypass) each sat in code the PR did not touch or needed a run to see.

## Evidence locations
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate4-tier1/out/`: `p1779`, `p1782`, `p1785`, `p1786` (facts, `facts_spark.json`, diff, `spark/review.json`), `mut1779/`, `mut1785/` (+ `.txt` summaries), `suite1785/`, `probe1782_head.txt`, `p1786_matrix.txt`, `p1786_test_head.txt`, `p1786_test_mutE1.txt`, `p1786_mut_*.txt`, `p1786_stderr_*.txt`, `mergetree.txt`, `ticket_*.txt`, `pins_start.txt`, `pins_end.txt`. Scratch: `/private/tmp/claude-501/gatework4/` (drivers `mut1779.py`, `mut1785.py`, `mkprobe1782.py`, `p1786/drive.sh` and stubs, `mt.sh`, `smerge.sh`, worktrees). No container started; no port bound.
