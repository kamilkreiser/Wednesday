# QA gate 8 (tier 2, batch, round 1 of 2): Secuura #1790 (KS-1340), #1792 (KS-1499), #1794 (KS-1600 item 1), #1793 (KS-1250)

- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), G2 tier-2 batch gate, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel (UP, pid 52462). Routing receipt as commissioned: claude-sonnet-5-5, G2 tier-2 batch gate, gauge 83%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear read-only (KS-1340, KS-1499, KS-1600, KS-1250; comments first:100; key never printed). `gh` was not used, so the PR bodies were NOT read; each PR's own Flow-doc block and Linear READY comment stood in.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate8-batch/repo` (did not exist; `git init`; `git rev-parse --show-toplevel` asserted equal to that path before the first fetch and again at the end; origin git@github.com:Secuura/Distributed_Secuura.git, deploy key `3_Access_Keys/github_deploy_rw` via GIT_SSH_COMMAND with `IdentitiesOnly=yes`). Spark work dirs and worktrees are under the scratchpad `.../scratchpad/gate8/` (spark_gate.sh refuses a work dir under WEDNESDAY). Worktrees (`wt/h1790 h1792 h1793 h1794 dev`) were NOT removed. Evidence in `.../scratchpad/gate8/out/` (copies of the key files are not duplicated here).
- **node_modules:** per-worktree root `node_modules` = directory of read-only symlinks into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules`, with `@secuura/*` relative links copied so each worktree resolves its OWN `packages/shared`, built in the worktree (`tsc`). ONE exception, scratch only: the Prisma client had to be generated, so `services/originate/node_modules` is a private `cp -Rc` copy inside `wt/dev` (original symlink moved to `scratchpad/gate8/_quarantine/`), `npm run generate` equivalent (`scripts/prisma-generate.cjs`) run there, and the other four worktrees symlink to that copy. Read back afterwards: `Dev/node_modules/.prisma` and `Dev/services/originate/node_modules/.prisma` do NOT exist in the shared tree. Node v26.8.1 (not the repo's LTS 24) on every run.
- **Load:** `uptime` before every heavy run; waitload.sh (60 s steps up to 15 min). Misses, recorded: the first two runs of ks1594 (head, both modes) started at load1 8.99 and 12.16 (the 12.16 reading came after I first typed the check; I did not wait), and the first ks1263 head runs at 14.61 (not waited). Every later heavy run was started at load1 below 12 (10.6 to 11.9), one after waiting 4 minutes. Spark queue lock clear.

## Pins (git ls-remote)

| ref | start (00:05) | mid (00:28) | end (00:35) |
|---|---|---|---|
| refs/pull/1790/head | 3a9b1c121f6d5e818f6e450e8f2739c55743d1d4 | same | same |
| refs/pull/1792/head | 00711fe18f0829dcde098ba1e3b3df5986c58210 | same | same |
| refs/pull/1793/head | 29989b01ab059b6c009828042346c0fe30e5a4bc | same | same |
| refs/pull/1794/head | ae7d9da67a6da209ba76b9afdd9a6aad5d0671b3 | same | same |
| develop | bf681065124bb0ab54141f50e273a0db6862463c | **8fbda28e6e7988d7c1f218f3662cd6b2c0a4e204** | 8fbda28e6e79 |

All four heads equal the brief (the brief's `29989b01ab05...` is 29989b01ab059b6c...). **Develop MOVED during the run**: `8fbda28e6` is `#1777` (KS-1240 part 3) merged, which added docs section **88**. Heads did not move. Merge-bases: #1790 2b7ef12fa564, #1792 d531abd5f34b, #1793 bd6697e079fc, #1794 b67a1c8d3a52.

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1790 | KS-1340 | **GO** | Real PG 15.19 as `secuura_app`: the file is **24/24** in both tenancy modes (base file 6/6, develop-era sha256/16 `45876b754cc0b0b3` equals the doc's). The guard refuses all three DSN shapes T measured (`?host=203.0.113.7` on a 127.0.0.1:55419 authority, `?port=5432`, a DSN naming no port); the old authority-only guard accepted all three. Ten of my own mutants each killed (restoring the authority-only check reds exactly the 9 the PR says). Notes: three guard edges outside the ticket (see findings). |
| #1792 | KS-1499 | **GO WITH NOTES** | 12/12 in both modes on real PG as `secuura_app`; base file 11/11. Every claim reproduced: M5 (RLS off on shares and custody_events) survives the base file (0 red, both modes) and reds exactly the new F1 cell; a force-flag-only variant survives M5 (the author's note is right); superuser stand-in under `-t` exits 0 on base and refuses on head under all three filters; each hook mutant reopens only its own describe. Notes: policy behaviour on shares/custody_events still unasserted (disclosed), docs section number. |
| #1794 | KS-1600 item 1 | **GO** | 26/26 in both modes (base file 23/23). R9, R1 each red c19 alone ("expected 400, got 403" as the doc says); R7 reds both c20 cells; the two half forms red one c20 cell each; the BASE file survives all five mutants 23/23. Three extra mutants of mine also killed. Item 2 and 3 of KS-1600 are not in this PR (stated). |
| #1793 | KS-1250 | **GO WITH NOTES** | Stub-curl suite 5/0 at head, 2/3 at base script (the PR's figures); the two older smoke suites 6/0 and 5/0 at head and at develop; `--list` 97 to 98, `--check-unreached` rc 0. Nine of my ten script mutants killed by the predicted cells. The gateway half is real; the ticket is NOT closed by it: 12 live `localhost:60xx` lines remain (counted, matches), RUNBOOK 2.2 is unchanged and still tells an operator to run the FULL script at a remote gateway and expect all checks to pass. No cell uses an https base, the form RUNBOOK 2.2 documents (mutant M11 survives). Never run against a live host; only stub-curl, localhost default and `.invalid`. |

**Docs sections now carried (report only; chain holds 87-99, so 100+ needed):** develop's highest `<h2>` is now **88** (8fbda28e6e79; was 87 at bf681065). **#1790** carries `<h2>85.` + `<h3>85.1-85.3`; **#1792** `<h2>86.` + `86.1-86.3`; **#1793** `<h2>84.` + `84.1-84.3`; **#1794** `<h2>87.` + `87.1-87.3`. Cheat-sheet blocks have unnumbered `<h2>`/`<h3>`. All four collide with sections already on develop (84-88) and with each other for the numbered h2s' pairs only by being distinct; at assignment rewrite the numbered sub-headings and in-text cross-references in the Flow doc. Each head's two html files are a **pure insertion before the single `</body>`** (checked: head == base[:i] + block + base[i:], 8 of 8, against each PR's own merge-base).

**Merge-tree** (`git merge-tree --write-tree --name-only`, current develop 8fbda28e6e79, and also bf681065124b): each PR alone conflicts in **exactly the two Projects Documents html files**, nothing else (rc 1, same on both develops). All 12 ordered pairs among the four: rc 1, the same two html files only. No code file is shared by any two of the four (pairwise intersection of non-doc files: 0 files touched by two or more PRs). Order of the four is free in code; only the docs renumbering is order-dependent.

---

## Spark shadow (run FIRST, per PR; `out/p<n>/`)

Method: `spark_gate.sh <clone> <n> <head> develop <test file> --node-modules <Dev node_modules> --work <scratch> --out <scratch>` (base = `develop`, not a round sha), then `tunnel.sh check` (UP), then `spark_review.py` with `facts_spark.json` = facts minus the two Projects Documents html files, plus a HARNESS LIMIT line in `not_run`. No PR body supplied.

| PR | spark_gate (head / base product code) | Spark review |
|---|---|---|
| #1790 | **HARNESS BLIND**: `*.integration.test.ts` is ignored by jest; 0/0 and files_failed 1 on both sides. NOT counted as a result. | NO GO, 2 Major 2 Minor 1 Note; 1 attempt, 48 s, 17,681 prompt tokens |
| #1792 | **HARNESS BLIND**, same | GO WITH NOTES, 1 Major 1 Minor 2 Note; 1 attempt, 56 s, 22,059 tokens |
| #1794 | **HARNESS BLIND**, same | GO WITH NOTES, 6 Notes; 2 attempts (first a repetition abort), 110 s, 30,888 tokens |
| #1793 | ks `.test.sh` run under `/bin/bash`: **5 pass / 0 fail** at head; **2 pass / 3 fail** on base product code (matches the PR). A real result. | NO GO, 2 Major 4 Minor 2 Note; 2 attempts (first a repetition abort), 131 s, 31,472 tokens |

### Spark findings judged at source

**#1790 (NO GO):**
- Major 1 ("hostaddr in the authority / PGHOST and PGPORT could still bypass"): **REFUTED.** `hostaddr` has no authority form (it is a query key). PGHOST/PGPORT: the guard asks the pg client, which reads the environment at construction; measured with `PGHOST=203.0.113.7 PGPORT=55419` a DSN naming no host is judged `203.0.113.7:55419` and refused; `PGPORT=55419` alone with a no-host DSN is judged `localhost:55419` and accepted (correct, it is what pg dials). The PR lists PGHOST/PGPORT as "not measured"; I measured the predicate.
- Major 2 ("guard is test-only, not enforced in CI"): TRUE and stated (the file is excluded from the unit suite, `jest --listTests` at head: 142 files, 0 integration); it is a scope fact of a test-file guard, not a defect. Quote not found in input.
- Minor 1 (spy on `Socket.prototype.connect` may miss another path): **NOT BORNE OUT**, the cell has a control (one deliberate connect reads exactly 1) and my N3/N4 mutants made that cell red, so it can move.
- Minor 2 (WIRING cell red "by absence" on base): true of any new symbol; its job is to prove the loop judged both DSNs, and N8 (call neutralised) and N9 (loop judges only the first) each red exactly that cell. Note (authority form of hostaddr): same as Major 1.
- Net: **no defect confirmed**; false NO GO.

**#1792 (GO WITH NOTES):**
- Major 1: its premise "afterAll deletes rows from shares and custody_events without any tenant-scope filter" is **FALSE** (`afterAll` at lines 262-270 is `DELETE ... WHERE tenant_id = $1` and by id); the same Major then concedes the guard works. The residual (flags asserted, policies not behaviourally asserted) is DISCLOSED in docs 86.2 and the Linear comment. Net: refuted/disclosed.
- Minor 1 (single-cell run skips SETUP cell): the hook now covers it, measured (H1-H3 and the superuser `-t` runs). Notes: F5 scope choice = disclosed; second Note repeats the false afterAll claim.

**#1794 (GO WITH NOTES, 6 Notes):** (1) integration file not runnable by harness: TRUE, why this gate ran it (26/26). (2) `mint` helper reads the row only if `json.apiKey.id`: the helper's contract; every c20 cell first asserts `absent.status` 201 and the stored org, and mutant X2 (absent stores null) reds the ORG_ADMIN c20. Not a defect. (3) c19 covers an array only for tenant admins: TRUE, stated in docs 87.2; my X1 (arrays exempt) is killed by c19 AND c17. (4) c20 does not assert stored scopes: true, outside the ticket. (5, 6) no-body / acceptance notes. Net: **no defect.**

**#1793 (NO GO):**
- Major 1 (12 hard-coded `localhost:60xx` lines remain): **TRUE, and disclosed** in the PR and the ticket comment ("closes the gateway half, not the ticket"). I counted 12 live lines (smoke-test.sh 259, 263, 267, 275, 283, 292, 305, 307, 317, 319, 327, 329; a 13th hit at line 95 is a comment). Carried as 1793-1 and 1793-2, not as a defect of the lines.
- Major 2 (stub curl too permissive, cannot see bad curl flags): not what the test is for (URL targeting); quote not found. Minor 1 (`grep -v -c -F` counts substring): contrived; my hard-code mutants M6, M7, M8 each red the "every URL under the base" cell. Minor 2 ("test passes even if script ignores the variable"): **REFUTED**, the base script (M1) reds three cells. Minors 3 and 4 and Notes: provenance claim unverified (not a defect), duplicate-coverage and doc-not-tested remarks. Net: **one TRUE premise (disclosed scope), no defect in the lines.**

---

## #1790 (KS-1340, DSN query overrides in the ks597 guard): GO

Head 3a9b1c121f6d. `ks597-issuer-organization-id.integration.test.ts` +131/-15 (numstat equals the doc), two docs. Product files: none. The guard is one new function `disposableDsnTarget` plus a `guardedTargets` map.

### Real Postgres
One container `gate8-pg` (postgres:15-alpine, `127.0.0.1:55419`, PostgreSQL 15.19 aarch64 musl, `max_connections=1000` as docker-compose). `docker/init` mounted read-only (creates `secuura_app`, non-superuser, non-BYPASSRLS, verified), then the head's `scripts/run-migrations.sh` (run in a throwaway container sharing the DB container's network because the host has no psql): **applied=57 failed=0**; platform migrations land in the same database (PLATFORM_DATABASE_URL unset), as gate 3 did. Jest: `jest.integration.config.js --runInBand`, `TEST_DATABASE_URL` superuser, `TEST_APP_DATABASE_URL` as `secuura_app`. Port 55419 had no listener (lsof) before and none after.

| Check | Result |
|---|---|
| The file at head, `MULTI_TENANCY_ENABLED=false` / `true` | **24 / 24** and **24 / 24** (the pattern `ks597` also matches `ks597-b-caller-org-externalref.integration.test.ts`, which adds 8 more passing cells; my targeted runs use `ks597-issuer`) |
| The file at its merge-base (2b7ef12fa564), same database | **6 / 6** |
| 18 new cells | 1 wiring, 11 refusals, 5 acceptances, 1 no-socket: as the doc says |

### The DSN shapes (probe `probe1790.js`: the PR's own function extracted and transpiled, run against pg 8.20.0 / pg-connection-string 2.12.0; no database, no socket)
| Shape | pg dials | old (KS-1306) guard | new guard |
|---|---|---|---|
| T1 `127.0.0.1:55419/db?host=203.0.113.7` | 203.0.113.7:55419 | ACCEPTED | **REFUSED** (not loopback) |
| T2 `...:55419/db?port=5432` | 127.0.0.1:5432 | ACCEPTED | **REFUSED** (shared port 5432) |
| T3 `postgres://u:p@127.0.0.1/db` (no port) | 127.0.0.1:5432 | ACCEPTED | **REFUSED** (shared port 5432) |
| T3b empty port `127.0.0.1:/db` | 127.0.0.1:5432 | ACCEPTED | REFUSED |
| `?host=203.0.113.7&port=5432` | 203.0.113.7:5432 | ACCEPTED | REFUSED |
| `?host=127.0.0.1&host=203.0.113.7` (duplicate key, last wins in pg) | 203.0.113.7:55419 | ACCEPTED | REFUSED |
| `?host=%32%30%33.0.113.7` | 203.0.113.7:55419 | ACCEPTED | REFUSED |
| `?port=05432`, `?port=5432abc` | 127.0.0.1:5432 | ACCEPTED | REFUSED |
| unix socket via `?host=/var/run/postgresql` | socket | THROWS | REFUSED |
| `?hostaddr=...`, bare `?hostaddr`, `?sslmode=disable&hostaddr=...` | ignored by pg | ACCEPTED | REFUSED |
| clean loopback 127.0.0.1 / [::1] / localhost on a free port | as named | ACCEPTED | ACCEPTED |

### Mutants of my own (own worktree `w1790`... `h1790`; the file rewritten, restored and compared by sha256 each time; `out/mut1790.log`, `out/mut1790b.log`)
| mutant | result (24 cells) | red |
|---|---|---|
| M0 head | 24/24 | none |
| N1 authority-only reading restored (the PR's own 9) | 15/24 | 9: host, 5432, 6432, host+port, no-port, empty-port, unix-socket, query-port acceptance, no-socket |
| N2 host from client, port from authority | 17/24 | 7 |
| N3 port from client, host from authority | 20/24 | 4 (includes the no-socket cell) |
| N4 hostaddr rule dropped | 22/24 | hostaddr refusal, no-socket |
| N5 shared-port rule dropped | 18/24 | 6 |
| N6 loopback rule dropped | 19/24 | 5 |
| N7 refuse every query string | 15/24 | 9 (the accepted-with-query cells and others) |
| N8 call neutralised in `beforeAll` | 23/24 | WIRING |
| N9 loop judges only the first DSN | 23/24 | WIRING |
| N10 unparseable DSN accepted | 22/24 | the unparseable refusal, no-socket |
(Two earlier forms of N1 and N8 failed to compile and are not counted; N1's first redo had a spaces-in-name harness slip. Counts match the PR's N1 and half-form rows.)

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1790-1 | Low (pre-existing, outside KS-1340) | The shared-stack list is `5432` and `6432` only. docker-compose also publishes the stack's **pgbouncer on `127.0.0.1:${PGBOUNCER_PORT:-6433}`**, which fronts the same shared database; `...@127.0.0.1:6433/db` is **ACCEPTED** by the new guard (probe row A9). | TESTED by probe; not run against a pooler. |
| 1790-2 | Info | The `hostaddr` regex is case- and encoding-literal: `?HOSTADDR=` and a percent-encoded key (`?host%61ddr=`) pass it. pg ignores both (it dials 127.0.0.1:55419 either way) and no consumer of the DSN in this file is libpq, so no measured bypass; libpq does decode key percent-escapes, so it is the PR's own stated reason for the rule only partly met. | TESTED by probe (A20, A21). |
| 1790-3 | Info | The guard judges the pg client's reading only. The same DSN is also handed to the product (Prisma) as `DATABASE_URL`, whose parser may read a duplicate or overriding query key differently. Not measured (needs a connection attempt). The PR lists only libpq/hostaddr and PGHOST/PGPORT as unmeasured. | NOT TESTED. |
| 1790-4 | Low (merge-time) | Docs carry section 85. | See BLUF. |

---

## #1792 (KS-1499, ks1263 RLS flags, hook guard, env text): GO WITH NOTES

Head 00711fe18f08. `ks1263-multi-write-rolls-back.integration.test.ts` +37/-1 (numstat), two docs. No product file. Same container and role setup as above. The app-role DSN is TEST_APP_DATABASE_URL (this file ignores APP_DB_USER/APP_DB_PASSWORD: verified in the source of both files, the F5 sentence MATCHES).

| Check | Result |
|---|---|
| Head, MT false / true | **12 / 12**, **12 / 12** |
| Base file (d531abd5f34b), MT false / true | **11 / 11**, **11 / 11** |
| Catalog restored after every DB change (flags per table plus md5 of policies) | equal each time, and after the whole run |

### F1 (RLS state sweep; database states applied, each run on base file and head file, then restored)
| State | base file | head file |
|---|---|---|
| clean | 11/11 | 12/12 |
| documents RLS off (gate M4) | 1 red (existing documents cell) | 2 red (documents cell and F1) |
| shares RLS off | 0 red | 1 red (F1 only) |
| custody_events RLS off | 0 red | 1 red (F1 only) |
| **shares + custody_events off (gate M5), MT false and true** | **0 red, both modes** | **1 red (F1 only), both modes** |
| shares NO FORCE / custody_events NO FORCE | 0 red | 1 red each (F1) |
| head file with the new cell **force-flag-only** | on M5: **12/12, survives**; on shares NO FORCE: 1 red | (the author's correction to the ticket's first-named step is right) |

### F2 (superuser stand-in as the application role; `TEST_APP_DATABASE_URL` = the superuser DSN)
| run | base file | head file |
|---|---|---|
| `-t "D1/D2"`, `-t ROUTE-ROLLBACK`, `-t ROUTE-CUSTODY-ROLLBACK` | **1 pass, 10 skipped, exit 0 (the bypass), under all three** | **refuses (1 red) under all three** |
| no filter | 4 red of 11 | 12 red of 12 |
| hook-removal mutants (one `beforeAll` assertion removed per mutant), ordinary role | | 12/12 each |
| H1 (describe 1), superuser | | D1/D2 filter bypasses (1 pass, exit 0); the two route filters refuse |
| H2 (describe 2) | | ROUTE-ROLLBACK bypasses; the other two refuse |
| H3 (describe 3) | | ROUTE-CUSTODY-ROLLBACK bypasses; the other two refuse |

### F5
`TEST_APP_DATABASE_URL` unset (APP_DB_USER and APP_DB_PASSWORD set): base **7 pass / 4 red of 11**, head **12 red of 12**, matching the doc's "all 12 now go red where 4 of 11 did".

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1792-1 | Low (disclosed) | F1 asserts the flags only; dropping or loosening a `shares` or `custody_events` policy with the flags on is still caught by no cell. Docs 86.2 and the ticket comment say so; Spark's Major circled it. | FOUND in docs; not mutated (policy-loosening mutant not run). |
| 1792-2 | Info | The doc's F1 "18 comparisons" and "25 comparisons" in the Linear comment differ between artefacts; my runs agree with the substance of every row. | Reading. |
| 1792-3 | Low (merge-time) | Docs carry section 86. | See BLUF. |

---

## #1794 (KS-1600 item 1, ks1594 c19 and c20): GO

Head ae7d9da67a6d. `ks1594-admin-mint-provisioning-and-org-bound.integration.test.ts` +29/-0 (numstat), two docs. Product route `routes/adminConfig.ts` untouched (sha256/16 `3b5185e576fb3e21`, equal before and after all my mutants, equals the doc).

| Check | Result |
|---|---|
| Head, MT false / true | **26 / 26**, **26 / 26** (needs the generated Prisma client: a first run without it gave 14/26 and 12 red with "generated Prisma client missing", a harness fact, not counted) |
| Base file (b67a1c8d3a52), MT false / true | **23 / 23**, **23 / 23** |

### Route mutants (copies of nothing: my worktree route file rewritten, restored by sha256; `out/mut/m1794_*`, `m1794base_*`)
| mutant | head file (26) | BASE file (23) |
|---|---|---|
| M0 | 26/26 both modes | 23/23 |
| R9 guard narrowed to platform callers | **25/26, c19 only** (both modes) | **23/23, survives** |
| R1 guard moved after (a) and (c) | **25/26, c19 only** | survives |
| R7 null is 400 | **24/26, both c20 cells** | survives |
| R7p null refused for platform only | 25/26, SYSTEM_ADMIN c20 only | survives |
| R7t null refused for tenant admins only | 25/26, ORG_ADMIN c20 only | survives |
| X1 (mine) arrays exempt from the guard | 24/26, c17 and c19 | |
| X2 (mine) absent request stores NULL instead of the caller's org | 24/26, c9b and the ORG_ADMIN c20 | |
Observed under R9 and R1: c19 reads "expected 400, received 403", which matches the doc's measured difference from the ticket's wording (decision (a) answers 403 first, the array is not read as absent).

### Findings
| # | Sev | Finding |
|---|---|---|
| 1794-1 | Info | c19 sends an array only for a tenant admin; object, number, boolean pinned for platform only (c17). Disclosed in 87.2. |
| 1794-2 | Info (carry) | KS-1600 items 2 (forged x-tenant-id through the real middleware) and 3 (malformed `permissions` between the two doors) are not in this PR; the ticket stays open, as the PR says. |
| 1794-3 | Low (merge-time) | Docs carry section 87; develop already has 87 and 88. See BLUF. |

---

## #1793 (KS-1250, smoke-test.sh honours SMOKE_BASE_URL): GO WITH NOTES

Head 29989b01ab05. `smoke-test.sh` +3/-1 (comment, assignment, echo), new test 88 lines (5 cells), two docs. **smoke-test.sh was never run against any live or remote host.** Runs: the stub-curl suites, the localhost default in `--quick` (no listener on 6882, refused connection), and `.invalid` hosts in `--quick` with real curl (DNS never resolves). The full (non-quick) mode, which anchors a real document, was never run, with or without a stub.

| Check | Result |
|---|---|
| New suite at head, `/bin/bash` 3.2.57 | **5 passed, 0 failed**, rc 0 |
| New suite against the base script (bd6697e) | **2 passed, 3 failed** (the two RED cells and the default-target control), rc 1; matches the PR |
| `smoke_test_counters_survive_errexit`, `smoke_test_degraded_warns`, at head and at develop | 6/0 and 5/0 at both |
| `run-shell-suites.sh --list` | develop 97, head **98**, new suite named; `--check-unreached` rc 0 ("all 98 tracked suites reached") |
| `--quick` real curl, unset / `.invalid` http / `https://x.invalid/` | prints `Smoke target: <value>` first, every check fails as unreachable, rc 1 |

### Mutants of the script (own worktree, restored by sha256; `out/mut1793.json`)
| mutant | result | red |
|---|---|---|
| M0 head | 5/0 | none |
| M1 base script (variable ignored) | 2/3 | the two RED cells, default-target control |
| M2 `:-` becomes `-` (empty is not default) | 4/1 | the empty-value control |
| M3 echo prints the default, not the gateway | 4/1 | target-line cell |
| M4 echo removed | 3/2 | |
| M5 echo twice | 3/2 | |
| M6 Issuer Portal URL hard-coded | 4/1 | "every URL under the base" |
| M7 `/health/deep` URL hard-coded | 4/1 | same |
| M8 `API root` URL hard-coded | 4/1 | same |
| M9 trailing slash of the base stripped | 5/0 | (benign, expected) |
| **M10 a URL hard-coded in the FULL path (outside `--quick`)** | **5/0, survives** | none (the suite runs `--quick` only; disclosed) |
| **M11 an `https://` base replaced by localhost** | **5/0, survives** | none (the one base the suite uses is `http://`) |

### Findings
| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1793-1 | Medium (scope, disclosed) | A remote full run is **mixed**: the gateway section and the login, document-create and anchor steps go to `SMOKE_BASE_URL`, while 12 live lines (sections 7 on, lines 259 to 329) still call `http://localhost:60xx`. On a remote run this either fails (nothing local) or, with a local stack up, passes checks that did not test the target. The ticket KS-1250 stays open after this PR (its comment says so). | TESTED by counting; matches the PR's "12 live". Not run. |
| 1793-2 | Medium (docs, outside the diff) | **RUNBOOK 2.2** (`deployment/azure/RUNBOOK.md`, lines 140-150) is unchanged by this PR and still tells an operator to run the FULL script against `https://<prod-gateway-fqdn>` and expect "All checks return"; after this PR that run honours the target for 3 sections and ignores it for 12 checks, and it anchors a real document. The PR's own docs warn "do not read a remote full run as a clean check", but the RUNBOOK does not. | FOUND by reading RUNBOOK at head. |
| 1793-3 | Low | No cell uses an `https://` base, the form RUNBOOK 2.2 documents. M11 survives. | TESTED (M11). |
| 1793-4 | Info | `Smoke target:` echoes the variable verbatim: a value with credentials in the URL is printed in full (`https://user:pw@host`); a trailing slash yields `//health` URLs. | TESTED with a `.invalid` host (placeholder credentials). |
| 1793-5 | Low (merge-time) | Docs carry section 84. | See BLUF. |

---

## Calibration rows (one per PR)

| PR | Spark verdict | This check | Spark defects that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1790 | NO GO (2 Major, 2 Minor, 1 Note), harness blind | GO | 0 | 1790-1 (pgbouncer port), 1790-2 (hostaddr encoding); also it could not run the 24 cells | **False NO GO.** Both Majors refuted or already stated scope; it argued about hostaddr in "the authority", a thing that does not exist. |
| #1792 | GO WITH NOTES (1 Major, 1 Minor, 2 Note), harness blind | GO WITH NOTES | 0 (its Major rests on a false reading of `afterAll`; the residual it circles is disclosed) | none new | **Right verdict, one false premise.** It could not run the cells, yet reached the same verdict. |
| #1794 | GO WITH NOTES (6 Notes), harness blind | GO | 0 | none | **Right verdict, thin.** Notes are generic caveats, one correctly names the harness limit. |
| #1793 | NO GO (2 Major, 4 Minor, 2 Note), harness ran it | GO WITH NOTES | 1 TRUE premise (12 hard-coded lines), already disclosed; no defect in the lines | 1793-2 (RUNBOOK 2.2 still instructs a remote full run), 1793-3 (https base unpinned) | **False NO GO from a true premise.** It turned a disclosed scope limit into a Major, and the unmeasurable "stub too permissive" into another. |

Reading: three of four reviews were on integration files the harness cannot run (the same blind spot gate 3 recorded); the one the harness could run (#1793) got the sharper NO GO from a disclosed fact. Pattern as gates 2 and 3: a Spark NO GO on a disclosed-scope PR is a prompt to run one mutant, not a defect signal. The two Spark repetition aborts (#1793, #1794 first attempts) were recovered by the built-in retry.

## What I did NOT test
- Any other service's suite, the four platform suites (Schemathesis, Akto, Playwright, Performance/k6), a running stack or gateway, any deploy, Node 24 (host has only v26.8.1), amd64 Postgres, PG versions other than 15.19, CI.
- The whole originate unit suite (1698 tests): only `jest --listTests` (142 files, 0 integration files) at head and develop.
- #1790: how Prisma (the product's connection) reads duplicate or overriding query keys; libpq itself; any connection attempt to a non-loopback address (none was made).
- #1792: a policy-loosening mutant on shares or custody_events with the flags on (disclosed, the PR does not claim it).
- #1794: KS-1600 items 2 and 3; non-string shapes other than an array for a tenant admin.
- #1793: the full (non-quick) `smoke-test.sh`, any run against kintsugi or demo (held for Kam), a Node-level or bash 4+ run (only `/bin/bash` 3.2.57), the whole shell-suite runner (only `--list`, `--check-unreached` and the three smoke suites).
- PR bodies (gh not used); doc accuracy beyond heading structure, insertion shape and the figures I re-measured; the doc html checkers named in earlier gate verdicts.
- The Spark gate's integration-file results: by construction none (0/0, flagged as harness blind).

## Container lifecycle
`docker run -d --name gate8-pg -p 127.0.0.1:55419:5432 postgres:15-alpine` (lsof had no listener on 55419 before). Never touched s-t5-pg, aa4-pg or any other container. Stopped and removed ONLY `gate8-pg`, by name, at 00:35 (`docker stop gate8-pg; docker rm gate8-pg`); read back: `docker ps -a --filter name=gate8` returns 0, `lsof -iTCP:55419` empty. The one-shot migration container ran with `--rm`. I started no other long-lived process; my Spark queue runner (pid 5278), the exp1792 driver (91380) and exp1792b (15665) had all exited on their own before the end.

## Evidence locations
`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate8/`: `out/p1790 p1792 p1793 p1794` (facts, diff, `spark/review.json`), `out/it/` (every integration run, json and log, `e1792_*`, `e1792b_*`), `out/mut/` and `out/mut1790*.log`, `out/mut1793.json`, `out/probe1790.txt`, `out/linear_KS-*.md`, `out/mt_*.txt` (merge-tree), drivers `mut.py exp1792.py exp1792b.py mut1793.py probe1790.js htmlshape.py pairs.sh run_it.sh setup_wt.sh waitload.sh`, `load.log`.
