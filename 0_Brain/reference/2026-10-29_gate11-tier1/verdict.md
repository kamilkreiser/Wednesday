# QA gate 11 (TIER 1, batch, findings only): Secuura #1782 round 2 of 2 (KS-1240 p4 delta) and #1800 round 1 (KS-1494 items 1+4)

**ROUTING RECEIPT:** model: opus -- tier-1 gate row (fleet/specs/model-routing.md) -- weekly gauge 88% (80-90 band: tier 1 has no promoted local gate; the Spark half ran first, below).

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), subagent of Wednesday. Spark review model: deepseek-v4-flash via the tunnel (UP, queue 0 at start).
- **Pushed / merged / commented / Linear / mail:** nothing. `gh` not used (PR bodies NOT read; commit messages stood in, flagged to Spark).
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate11-tier1/repo` (did not exist; `git clone --shared .../spark/cache/src`; `rev-parse --show-toplevel` asserted equal to the path before the first fetch; origin re-pointed to GitHub, deploy key via GIT_SSH_COMMAND). All git writes there. Worktrees `/private/tmp/claude-501/gatework11/{w1782,w1782r1,w1800,w1800base}` + spark_gate's own `sg1782`, `sg1800`. Product files I mutated were restored from `git show HEAD:` and `git status --porcelain --untracked-files=no` read back empty (asserted in both mutant drivers). Scratch files left in my worktrees only: `gate11-probe-gateway.test.ts` (w1782, w1782r1), `gate11-attack.integration.ts` + `tsconfig.gate11.json` (w1800, w1800base), node_modules symlinks. Not removed (no-delete rule).
- **node_modules:** read-only symlinks to the Secuura checkout's `Blockchain/Dev/node_modules` (pg 8.20.0, pg-connection-string 2.12.0, vitest 4.1.x). Nothing installed. **Host Node v26.8.1 (not the repo's LTS 24)** on every run.
- **Postgres:** ONE container `gate11-pg1800` (postgres:15-alpine, 127.0.0.1:55418, port checked free first), schema = 11 `docker/init` files + 56 migrations, 0 failed. **Removed by name** at the end: `docker ps -a` shows 0 `gate11` names; `lsof` shows nothing listening on 55418. No other container or port touched; nothing on 5432/6432/6433.
- **Processes:** only vitest/node runs I launched in the foreground or via my own background scripts; all exited. No kill issued.
- **Load:** load1 ~3 throughout (quiet host); the probe timings below are not load-distorted.

## Pins (git ls-remote)

| ref | start (17:06Z) | end (17:22Z) |
|---|---|---|
| refs/pull/1782/head | **60bfafe0972002d4bd5d3420be32a772c0251b35** (= brief) | same |
| refs/pull/1800/head | **fb3579b0a4b4d3b7c1dd2b2f63ee029c4ce5c5ec** (= brief) | same |
| develop | 236cf2bb411b1d893e8a8a21807450bdb32ddc24 | **0aa6af1f44ba** (#1788 merged mid-gate: auth social providers + the two docs only; disjoint from both PRs) |

Merge-bases: #1782 = bd6697e079fc (unchanged from gate 4; round-1 head 89335fe9c679 is an ancestor of 60bfafe09720); #1800 = cc262c1b6d18 (the brief's 802eb2b8ecaf was develop at push; merge-base is older). Merge-tree (`--write-tree --name-only`) of each PR with develop 236cf2bb, and of #1782 x #1800: conflicts are **the two Projects Documents html files only**, no code file. Develop has not touched tenant-provisioning, `api-gateway/src/routes/platform.ts`, `services/auth/integration/` or `docker-compose.yml` since either merge-base (diff --name-only empty), so PB8/PB10's source readers see the same platform.ts after merge.

## BLUF

| PR | Verdict | One line |
|---|---|---|
| **#1782** (round 2 of 2) | **GO WITH NOTES** | **1782-1 is CLOSED at the code defaults, measured through the REAL gateway router**: both services hung -> the caller gets the PR's **201 at 6023 ms** against the 8000 ms deadline (round-1 head on the same rig: **504 at 8008 ms**, tenant finished at 10.0 s after the caller left). Delta is exactly the 5 files claimed; 14/14 head, 3 red at the round-1 head, 9 red at base; every mutant on the two constants that matters is killed; PB8 is a real coupling (gateway default 8000 -> 4000 or 7000 turns PB8+PB9 red). **The orphan-key window SHRINKS, it does not close:** the gateway-race orphan is gone at defaults, but a security service slower than 3 s (not hung) still mints a key nobody receives, and that window is now 3 s wide instead of 10 s (measured, S5). Two tickets, no fix-before-merge. |
| **#1800** (round 1) | **GO WITH NOTES** | **No DSN shape I tried dials a non-loopback host, a slot-1 shared port or a non-ks_ database while being accepted**: 47 attack rows, and for every ACCEPT the socket pg really opens (Socket.connect intercepted) equals what the guard judged. 27/27 guard cells (33/33 with a real Postgres), 18/27 red with the base guard (reproduced exactly), tsc 4 -> 0. Gaps, all Low/ticket: the **other slots' Postgres/pgbouncer ports (6532/6533, 6632/6633, 6732/6733) are accepted** (disclosed by the seat in its doc; backstopped by the ks_ name); my own mutants found **two unpinned widenings of the ks_ check** (unanchored `/ks_/`, case-insensitive) and the decoded-db reading is unpinned (answer to (b): yes, one cheap row; not a safety gap). |

**Merge order:** independent (disjoint code, docs-only conflicts). #1800 is test-only and lowest-risk; #1782 next. Docs renumbering at prep as usual (#1782 still carries 85, #1800 carries 91 "provisional").

---

## #1782 (KS-1240 part 4, round 2 of 2, delta): GO WITH NOTES

### (b) Is the delta exactly what the seat says? YES
`git diff 89335fe9c679 60bfafe09720 --stat`: **5 files, +115/-24**: the 14-cell test (+105/-~), `index.ts` (+5/-1: comment + `KEY_GENERATION_FETCH_TIMEOUT_MS = 3_000`), `meteringKey.ts` (+3/-2: comment + `METERING_KEY_FETCH_TIMEOUT_MS = 3_000`), both Projects Documents html files. Two commits (0ee103c7e code+test, 60bfafe09 docs). No other product line changed; the `signal:` lines and the handler are untouched context. Test delta: PB5 now pins `[3000, 3000]`; new PB9 (route, both hung, real bounds, answers <= deadline-1000 and >= sum-250); PB8 rewritten (bounds + 1500 ms writes allowance <= gateway default read from platform.ts); new PB10 PIN (the gateway's tenant-create call has exactly 2 args, i.e. uses the default deadline); new PBC3 control for the readers; `beforeAll` timeout 60 s.

### (a) Is 1782-1 closed? Measured through the real gateway route
Probe (scratch file in my worktree, `out/probe1782_*.jsonl`): the **real `createPlatformRoutes` router from `api-gateway/src/routes/platform.ts`** mounted in express (auth stubbed to a SUPER_ADMIN user), forwarding `POST /api/platform/tenants` to the **real tenant-provisioning `index.ts`** (pg recorder, as the PR's harness), with fake tokenisation/security servers that answer, stall, or answer late. **No bound shortened; real time.** Same file run at the head and at the round-1 head. Each row waits 13 s after the answer to catch late writes.

| scenario | round-1 head (10 s bounds) | **head (3 s bounds)** |
|---|---|---|
| S0 control, both answer | 201, 15 ms, key + mKey | 201, 15 ms, key + mKey |
| **S1 both hung** | **504 GATEWAY_TIMEOUT at 8008 ms**; 2 writes at answer, 3 more at 10.0 s; security received the mint | **201 at 6023 ms** (margin 1977 ms); all 5 writes before the answer, none after |
| S2 tokenisation hung | 504 at 8006 ms; then **security minted AND delivered the key at ~10 s to a caller that had gone** (the gate-4 orphan) | 201 at 3009 ms **with** meteringApiKey |
| S3 security hung | 504 at 8008 ms | 201 at 3021 ms, keyFile, mKey null |
| S4 both slow 2900 ms (inside the bound) | 201 at 5821 ms | 201 at 5823 ms, both keys (worst success path fits) |
| **S5 security slow 3500 ms** | 201 at 3516 ms **with** mKey | **201 at 3015 ms, mKey null; security RECEIVED the mint request (secReceived 1, delivered 0)** |
| S6 tok slow 3500 + security hung | 504 at 8006 ms | 201 at 6011 ms |
| S7 tok hung + security answers at 9 s | 504 at 8006 ms | 201 at 6015 ms, mKey null; security received the mint |
| S1 at head with **`PLATFORM_UPSTREAM_TIMEOUT_MS=5000`** (the documented old Container-App override) | n/a | **504 at 5010 ms**; tenant active at 3.0 s; the mint request was outstanding when the caller was dropped |

**Answer:** with both a hung key service and a hung metering service, the real route ends inside the gateway budget (**6023 ms vs 8000 ms**, PB9's own figure 6068-6070 ms reproduced) and the caller gets the PR's 201. **1782-1 is CLOSED at the code default.** The orphan-key window **shrinks, it does not close**:
- the *gateway gave up first* orphan is gone at defaults (S1, S2, S7: every write lands before the answer);
- the *provisioning gave up first* orphan remains: a security service that answers after 3 s mints a key the route then reports as `meteringApiKey: null` (S5, S7). Round 1 delivered that key for anything under ~8 s (S5 r1). This is gate 4's 1782-3, now with a 3 s threshold instead of 10 s (finding 1782-R2-1);
- it reopens if the deploy sets `PLATFORM_UPSTREAM_TIMEOUT_MS` below ~6.1 s (S1 gw5000), which PB8 cannot see because it reads only the code default (1782-R2-2).

Not covered by the probe: real DB writes (pg is a recorder; the 1500 ms allowance is a stated number, not measured), `PROVISION_PER_TENANT_DB=true` (CREATE DATABASE + schema load run unbounded BEFORE the fetches; off by default, KS-160), a real gateway process (`index.ts` wiring, front-door auth) - the router is the real one, the app around it is mine.

### (c) Red-proof and mutants
| run | result |
|---|---|
| head test at head | **14/14** (`out/t1782_head.txt`; PB9 6070 ms) |
| head test on **round-1** product (`w1782r1`, test file copied in, restored after) | **3 failed / 11 passed**: PB5, PB8, PB9 (PB9 gave up at 12067 ms = deadline + 4000) - exactly the cells that should, matches the doc |
| head test on **base** product (spark_gate) | **9 failed / 5 passed** (controls x3, PBP1, PB10 pass) - matches the doc |

Mutants (`out/mut1782/summary.json`, each restored from `git show HEAD:`, worktree clean asserted):

| mutant | killed by |
|---|---|
| K1 key bound 4_000 | PB5, PB8, PB9 |
| K2 metering bound 4_000 | PB5, PB8, PB9 |
| K3 key bound 2_000 | PB5 |
| K4 metering bound 3_250 (still fits) | PB5 only (PB8/PB9 rightly green: 6250 + 1500 <= 8000) |
| K5 key bound back to 10_000 | PB5, PB8, PB9 |
| K6 metering `3 * 1000` (same value) | PB8, PB9 (reader returns NaN: fails CLOSED on a value-preserving rewrite - a false red, safe) |
| K7b metering `signal:` line removed | PB2, PB4, PB5, PB6, PB7, PB9 (6, = doc). (K7, my first spelling, was a syntax error: invalid, not counted) |
| G1 gateway default 8000 -> 4000 | PB8, PB9 |
| G2 gateway default -> 7000 | PB8, PB9 |
| G3 gateway default -> 7500 (boundary: still fits) | none (correct: 7500 >= 6000 + 1500 and PB9 6.07 s <= 6.5 s) |
| G4 gateway declaration reshaped (`Number(env ?? 8000)`) | PB8, PB9 (reader throws: fails closed) |
| G5 gateway call gets a 3rd arg `4000` | PB10 |

**11/11 meaningful mutants killed** (G3 is a correct non-kill; K7 invalid). The seat's seven named mutants and their kill counts match mine where they overlap (10 s -> 3 cells, signal dropped -> 6, gateway 4 s -> 2, third arg -> 1).

### (d) Is PB8 a real coupling? YES, with one blind spot
PB8/PB9 read `parseInt(process.env.PLATFORM_UPSTREAM_TIMEOUT_MS || '8000', 10)` from `api-gateway/src/routes/platform.ts` text. Changing that default to 4000 (G1) or 7000 (G2) turns PB8 and PB9 red; reshaping the declaration fails closed (G4); a longer/shorter deadline passed at the call site is caught by PB10 (G5). **Blind spot:** an environment override of `PLATFORM_UPSTREAM_TIMEOUT_MS` is invisible to a source reader; measured above, 5000 gives the caller a 504 at 5 s again. No override exists in the repo (`git grep` on develop: only platform.ts and ENVIRONMENT-VARIABLES.md:237, which records a 5000 override on the OLD `secuura-dev-api` Container App, "now decommissioning", and says secuura02 uses the default).

### (e) Do the docs' new sentences match the code? YES, two wording notes
Matches, checked: 3 s bounds and the constant names; "default deadline of PLATFORM_UPSTREAM_TIMEOUT_MS, 8000 ms ... answers 504" (platform.ts:132, `sendUpstreamError`); "declared at line 132, route registered from line 314 at d531abd5" (develop now: decl 132, `router.post(` 314); "the two bounds run one after the other, so with both services hung the create takes 6 s plus its writes" (measured 6023 ms); "a 201 after 6068 ms"; 14 cells; 9/5 vs base; 3/11 vs round 1; 6 files / 35 tests; mutant kill counts; the old "proxy waits 60 s" sentence is removed. Notes (Low, merge-time wording, not blocking): (i) the cheat sheet says "so 6 s is the worst case" - it is 6 s **plus the writes** (the other doc says so); (ii) "The status and the body of every path are exactly what they were" is still true only for hung/unreachable services: for a service slower than 3 s the BODY changes too (keyFile / meteringApiKey null where the unbounded code returned them, S5), and for the metering side the slow case leaves a minted key nobody holds. The new sentence about slow services mentions only `vault_key_hash`.

### Findings (#1782)
| # | Sev | Class | Finding | FOUND / TESTED / HOW |
|---|---|---|---|---|
| 1782-1 (round 1) | was Medium | **CLOSED** | Gateway 504 at 8 s before the 10 s bound. | TESTED: real gateway router in front of real handler, real bounds: head S1 201 at 6023 ms vs round-1 S1 504 at 8008 ms (control: S0 201 both sides). |
| 1782-R2-1 | Low | **ticket** | Orphan-key window shrinks, does not close: a security service slower than 3 s but not hung mints a single-tenant `metering:read` key; the route returns `meteringApiKey: null`; manual re-mint makes a second live key. Round 1 delivered the key for any answer under ~8 s; base for any answer at all. Same for tokenisation (stored key, NULL hash; gate 4's 1782-2). This is the inherent cost of a short bound; it is the pending "what should the route answer" ruling, not a defect of this delta. | FOUND/TESTED: probe S5 head (201 at 3015 ms, mKey null, secReceived 1 / delivered 0) vs S5 round-1 (201 at 3516 ms with mKey). The real security service minting on receipt is read, not run. |
| 1782-R2-2 | Low | **ticket** | PB8's coupling is to the code default only; a deploy `PLATFORM_UPSTREAM_TIMEOUT_MS` below ~6.1 s reopens 1782-1 (504 first, mint outstanding). None in the repo today; ENVIRONMENT-VARIABLES.md records a historic 5000 override. Suggest: the env doc row states "must exceed the tenant-provisioning bounds (6 s + writes)". | TESTED: probe S1 with `PLATFORM_UPSTREAM_TIMEOUT_MS=5000` -> 504 at 5010 ms (control: S0 201 in the same run). `git grep` for overrides: 0 in compose/bicep/yaml. |
| 1782-R2-3 | Info | ticket (if anyone cares) | The 1500 ms writes allowance is a stated number; real platform-DB writes (5 statements via pgbouncer) and the `PROVISION_PER_TENANT_DB=true` path (unbounded CREATE DATABASE + schema before the fetches) are unmeasured against the 1977 ms measured margin. | Read (index.ts:259-265); unmeasured. |
| 1782-R2-4 | Low | merge-time wording | Two doc sentences (above, (e)): "6 s is the worst case" (+ writes); "status and body of every path exactly what they were" (not for a slow service). | Read against probe S1/S5. |
| 1782-R2-5 | Info | none | K6: rewriting a bound as `3 * 1000` fails PB8/PB9 although the value is the same (reader needs a literal). Fails closed; a maintainer will see a clear message. | Mutant K6. |

Round-cap classification: **nothing is fix-before-merge.** 1782-1 is closed; the residue (R2-1, R2-2) is ticket-class.

---

## #1800 (KS-1494 items 1+4, ks968 loopback guard): GO WITH NOTES

Test-only PR: `services/auth/integration/ks968-platform-admin-seed-with-both-rows.integration.ts` (+228/-~31) and the two docs. The guard builds `new Client({ connectionString })` (no socket) and judges `client.host`, `client.port`, `client.database`; refuses any hostaddr key (case-folded, URLSearchParams-decoded) and an unparseable DSN; shared ports = {5432, 6432, 6433} + compose defaults (compose: `${POSTGRES_EXTERNAL_PORT:-6432}`, `${PGBOUNCER_PORT:-6433}`).

### Runs
| run | result |
|---|---|
| head, no DB (`KS968_TEST_DATABASE_URL=postgresql://u:p@127.0.0.1:55419/ks_gate11`, port free) | **27 passed, 6 skipped** (describe 1's beforeAll cannot connect; the guard cells need no DB, as claimed) |
| base, no DB | 6 skipped (file-level beforeAll) - the old layout could not run any cell without a DB |
| **head, real Postgres** (my container, 56 migrations) | **33/33** |
| base, real Postgres | 6/6 (the hook move changed nothing for the six DB cells) |
| **red-proof**: head file with the base guard (`new URL` hostname + `/^\/ks_/` pathname) transplanted | **18 of 27 red** (= claim): 16 REFUSED rows + the free-?port ACCEPTED row + the no-TCP cell |
| tsc, a tsconfig including only this file (`tsconfig.gate11.json`) | **base 4 errors** (TS2493 x3 at 114/147/163, TS2352 at 147, all in this file) -> **head 0**, 0 errors anywhere else in the graph. Control: same grep counts 4 at base. |

### (a) Attack rows: is anything accepted that dials somewhere it should not?
Scratch suite (`gate11-attack.integration.ts`, the PR's guard text verbatim with describe 1 removed; `out/attack1800_rows*.jsonl`). For each DSN: the guard's verdict, then `client.connect()` with `net.Socket.prototype.connect` intercepted (no socket opened) to record **what pg really dials**. Shell has no PG* env; env rows set them per row and restore.

| family | rows | result |
|---|---|---|
| IPv6 loopback | `[::1]`, `[0:0:0:0:0:0:0:1]` (normalised to `[::1]`), `[::ffff:127.0.0.1]` | first two ACCEPT, dial `[::1]`; v4-mapped REFUSE (fail closed) |
| other loopback spellings | `127.0.0.2`, `127.1`, `2130706433`, `localhost.`, `LOCALHOST` | all REFUSE (pg keeps the spelling; not in the list) |
| userinfo | `u:p@203.0.113.7@127.0.0.1` / `127.0.0.1:55412@203.0.113.7` | ACCEPT dials 127.0.0.1 / REFUSE dials 203.0.113.7 - both consistent |
| double `?host=` | loopback-first / remote-first | pg takes the LAST: REFUSE (dials remote) / ACCEPT (dials 127.0.0.1) - consistent |
| double `?port=`, odd ports | `55412&5432`, `06432`, `6432.0`, `6432abc`, `%2B6432`, `%206432`, authority `06432`, `71968` | pg parseInt's them all to 6432/5432 -> REFUSE; 71968 -> REFUSE (range) |
| encoded / case keys | `?h%6fst=` (pg decodes: dials remote) -> REFUSE; `?HOST=` (pg ignores) -> ACCEPT dials 127.0.0.1 | consistent |
| comma host | `?host=127.0.0.1,203.0.113.7` (raw and %2C) | REFUSE |
| encoded host | `%31%32%37.0.0.1` -> ACCEPT dials 127.0.0.1; `%2Ftmp` and `socket:/tmp` -> REFUSE (unix socket) | consistent |
| db name | `?database=prod` (pg ignores; path wins) ACCEPT ks_x; `/%6bs_x` ACCEPT ks_x; `/%70rod` REFUSE; no path -> db = user `ks_x` ACCEPT | consistent with what pg sends |
| libpq-only keys | `?dbname=prod`, `?service=prod`, env `PGHOSTADDR` | ACCEPT; **pg dials 127.0.0.1:55412/ks_x** - only a libpq client would differ (see 1800-3) |
| `options=`, `sslmode=`, `application_name` | ACCEPT, dial unchanged | - |
| env overrides | portless + `PGPORT=55412` ACCEPT (dials 55412); portless + `PGPORT=6433` REFUSE; hostless + `PGHOST=203.0.113.7` REFUSE; hostless + `PGHOST=127.0.0.1` ACCEPT; dbless + `PGDATABASE=prod` REFUSE / `=ks_y` ACCEPT ks_y | the guard reads the client, which reads the env: consistent in every case |
| hostaddr | double-encoded key `host%2561ddr` ACCEPT (decodes once to `host%61ddr`, not a key in pg or libpq); `#?hostaddr=` REFUSE (over-refusal, safe) | - |
| **other slots' ports** | `127.0.0.1:6532/ks_x`, `?port=6533`, `:6732` | **ACCEPT, dial 6532 / 6533 / 6732** (1800-1) |

**Result: for all 20 ACCEPT rows, the dialled (port, host) equals the guard's verdict and is loopback; every accepted target outside slot 1's ports is a free port or another slot's port; the database pg sends always starts with `ks_`. No accepted DSN dials a non-loopback host, 5432/6432/6433, or a non-ks_ database.** Control that could have fired: the same harness recorded REFUSE rows dialling 203.0.113.7, 5432, 6432 and `/tmp/.s.PGSQL.55412`, so the interception sees non-loopback/shared dials when they exist.

### (b) Does the decoded db-name reading need a pinning cell? YES (cheap), but it is not a safety gap
Mutant U13 (read the db name from the raw path instead of the client) **survives** all 27 cells: no row has an encoded db name, so the ruled reading (`/%6bs_x` -> ks_x) is unpinned. The surviving direction is fail-CLOSED (a raw reading refuses `/%6bs_x`; I found no DSN where a raw reading accepts but pg sends a non-ks_ name), so it is a documentation-of-the-ruling gap, not a hole. One ACCEPTED row `'/%6bs_x' -> ks_x` kills it. Ticket / optional at merge.

### (c) Red-proof and mutants
Red-proof 18/27 reproduced exactly. My own 16 mutants (`out/mut1800/summary_all.json`, `-t KS-1494`, restored and clean-asserted): **killed 11** - drop host check (6 cells), host from authority (6), port from authority (6), drop shared-port check (7), drop port-range check (2), hostaddr case-sensitive (2), hostaddr undecoded (2), drop hostaddr check (5), parse error escapes as TypeError (1), guard not called on RAW (WIRING, 1), drop 6433 AND the compose read (4). **Survived 5:** U3 drop the 6433 literal alone (equivalent: the compose read supplies 6433 - the seat's one equivalent, confirmed); **U8 `/ks_/` unanchored** and **U9 `/^ks_/i`** (1800-2); U13 raw-path db (above); U16 add `0.0.0.0`/`127.0.0.2` to the loopback list (no REFUSED row for either; both still local, Info). The seat's "16 of 17 killed, 1 equivalent" is true of ITS set; a different reasonable set leaves two real (Low) widenings unpinned.

### (d) tsc: 4 -> 0, 0 new. Measured above.

### Findings (#1800)
| # | Sev | Class | Finding | FOUND / TESTED / HOW |
|---|---|---|---|---|
| 1800-1 | Low | ticket (disclosed) | The shared-port list is slot 1 only. Slots 2-4 publish Postgres on 6532/6632/6732 and pgbouncer on 6533/6633/6733 on loopback (`Projects Documents/Stack-Slots-How-To.md:34-35`, `PORT-REGISTRY.md:82`, `scripts/__tests__/stack_env.test.sh:77`; CI uses up to 6832/6833). The guard accepts them. Backstop: the db must be named `ks_*`, which a slot database is not by default, so connect fails unless someone created a ks_ DB on a slot stack. The seat's doc says "Another slot's published ports are not in the shared-stack list". Fix shape: refuse `6432 + 100*k` / `6433 + 100*k` for k = 0..4, or read PORT-REGISTRY. | TESTED: attack rows `:6532`, `?port=6533`, `:6732` -> ACCEPT, dial intercepted at those ports (control: `:6432`, `?port=06432` REFUSE in the same run). |
| 1800-2 | Low | ticket (or a 2-row add at merge) | The ks_ check's anchoring and case are unpinned: mutants `/ks_/` (accepts `prod_ks_x`, `secuura_ks_backup`) and `/^ks_/i` (accepts `KS_PROD`) survive all 27 cells. Not exploitable through the current code; it is a regression guard gap on the one check that backstops 1800-1. Add REFUSED rows `/secuura_ks_x` and `/KS_x`. | TESTED: mutants U8, U9, 27/27 green each. |
| 1800-3 | Info | none / ticket if libpq ever reads this DSN | The PR refuses `hostaddr` because "libpq honours it", but accepts other libpq-only spellings: `?dbname=prod` (libpq would open `prod`), `?service=` (a service file can supply hostaddr), env `PGHOSTADDR`. Nothing in services/auth or this suite spawns libpq (`git grep` psql/pg_dump/child_process: 0), so pg's reading is the one that matters and it is judged correctly. The code comment's claim that libpq matches keys "without regard to case" is, to my reading of libpq (`conninfo_find` uses strcmp), wrong - so `?HOSTADDR=` is an over-refusal; harmless. | TESTED for pg (rows ACCEPT, dial 127.0.0.1/ks_x). libpq behaviour UNMEASURED (no libpq on this host). |
| 1800-4 | Info | none | The REFUSED cell "a DSN that names no port (the client dials 5432)" depends on PGPORT being unset: with `PGPORT=55412` the guard (correctly) accepts, so the cell would go red on a runner exporting PGPORT. False red, fails closed. | TESTED: attack row "portless DSN with PGPORT=55412" ACCEPT. |
| 1800-5 | Info | (b) | Decoded db reading unpinned (U13 survives); fail-closed direction. One row. | Mutant U13. |
| 1800-6 | Info | ticket | No tsconfig includes `services/auth/integration/` (`tsconfig.json` and `tsconfig.test.json` include `src/**` only), so "the file type-checks" holds only under a hand-made config, and CI will not catch the next type error. (Raised by Spark's invalid raw attempt; confirmed by reading.) | Read both configs; my scratch `tsconfig.gate11.json` is the only config that checked it. |

No fix-before-merge item.

---

## Spark findings judged

| PR | spark_gate (deterministic) | Spark review |
|---|---|---|
| #1782 | head 14/0, base product 5 pass / **9 fail** (matches the doc). Diff vs merge-base bd6697e (whole PR, both rounds). | **INVALID x2 runs (4 attempts): SCHEMA FAILURE / repetition abort every attempt** (`p1782/spark/`, `p1782/spark_retry/`); 2 x 63,634 prompt tokens, ~244 s. No verdict. |
| #1800 | **collected 0 tests on both sides** (default vitest include is `*.test.ts`; this is `*.integration.ts` and needs `vitest.integration.config.ts`): HARNESS LIMIT. Facts for the review were replaced with MY runs (flagged GATE-RUN), and the base/head product split is vacuous for a test-only PR (flagged). | **INVALID: SCHEMA FAILURE x2** (repetition abort; `p1800/spark/`); 39,706 prompt tokens, 135 s. No verdict. Not retried (time box; the #1782 retry had just failed identically). |

No valid Spark review exists for either PR, so there is no Spark verdict to calibrate. I read the claims in the unparseable raw attempts (`raw_attempt*.txt`) and judge them as unvalidated hints:

- **#1782 (all attempts, 7-11 "Major" each):** every claim is about the PR DESCRIPTION being "internally inconsistent" (the round-1 commit message says 10 s / 11 cells / 8 red; the head says 3 s / 14 / 9). **FALSE as a defect.** I fed it the concatenated commit messages because gh was not used, so it saw two rounds' history; it repeated this one claim until the repetition abort. A real point does sit underneath it: the squash-merge message should be the final round's. That is merge hygiene, not a finding. **Spark said nothing about the gateway timing, the slow-service orphan or the env override.**
- **#1800 (attempt 1, 3 Major / 14 Minor):** **true:** the shared-port list misses other slots' ports (= my 1800-1, which the seat discloses); **true, Info:** no tsconfig includes `integration/`, so the fixed file is type-checked only by a scratch config and nothing stops the errors coming back (added below as 1800-6); **true but disclosed:** the guard cells still need `KS968_TEST_DATABASE_URL` set, because the module-level throw comes first (the doc says "with a loopback ks_ DSN set"); **partly true:** "the db check is case-sensitive / not decoded" (case = my U9, decoded is the ruled reading). **FALSE (refuted by my attack rows):** `?HOST=192.0.2.1` bypasses the host check (pg ignores `HOST` and dials 127.0.0.1); leading-zero or encoded shared ports bypass the port check (`06432`, `6432.0`, `%2B6432` are all REFUSED, and the dial goes to 6432); a hostaddr "in the authority" (pg has no such form); a non-string host makes the guard throw a TypeError (pg's host is always a string). Hooks "scoped wrong": the 33/33 real-Postgres run refutes it.

**Calibration:** 3 reviews, 0 valid. This is the second gate in a row where the repetition guard ate the review (gate 4: #1786 x2). Where its raw claims could be checked, the true ones were the disclosed slot-port gap and the tsc-coverage point; its "bypass" Majors were false.

| PR | Spark verdict | This gate | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1782 | none (invalid x4 attempts) | GO WITH NOTES | 0 | 1782-R2-1 (orphan window), 1782-R2-2 (env override), the closure itself | **No output**; raw attempts only restate commit-message history |
| #1800 | none (invalid x2) | GO WITH NOTES | 1800-1 (raw, disclosed), tsc-coverage Info (raw) | 1800-2 (ks_ anchoring/case unpinned), 1800-5 | **No output**; half of its raw Majors are refuted by measurement |

## What I did NOT test
- A real api-gateway process (its `index.ts`, front-door auth, `server.headersTimeout`), real tokenisation/security services, real platform-DB writes, `PROVISION_PER_TENANT_DB=true`, any deploy-time `PLATFORM_UPSTREAM_TIMEOUT_MS` other than 5000; Node 24; the four platform suites; the tenant-provisioning full suite (the PR states 35/35; spark_gate's targeted run only).
- #1800: libpq behaviour (no libpq here); a ks_ database on a running slot stack (no slot stack running; I did not start one); the docs' section 91 text beyond the figures (all figures I checked match my runs: 27/27, 18/27, 33/33, 6/6, 56 migrations, 4 -> 0).
- PR bodies (gh not used).

## Evidence locations
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate11-tier1/out/`: `p1782/`, `p1800/` (facts, facts_spark, diff, spark/ and spark_retry/ review output), `t1782_head.txt`, `t1782_r1prod_headtest.txt`, `mut1782/` (+ summary json), `probe1782_head.jsonl`, `probe1782_r1.jsonl`, `probe1782_head_gw5000.jsonl` (+ .txt), `t1800_*_nodb.txt`, `t1800_*_db.txt`, `pg1800_build.log`, `tsc1800_*.txt`, `attack1800_rows.jsonl`, `attack1800_rows2.jsonl`, `mut1800/`. Drivers: `/private/tmp/claude-501/gatework11/` (`run_sg.sh`, `run_rev.sh`, `run_rev2.sh`, `mut1782.py`, `mut1800.py`, `mkattack1800.py`, `probe1782_gateway.test.ts.txt`, `run_probe1782.sh`, `probes/pgparse.cjs`).
