| PR | head | verdict |
|---|---|---|
| 2052 (KS-1081, round 2 of 2) | b61674e7b7635a50d51f837849cb9caf1259235d | **GO WITH NOTES** (no finding blocks) |

# Gate 259, tier 1, round 2 of 2: PR 2052, KS-1081, findings only

Head read at origin at 22:26:48 and again at 22:39:21 AEDT: b61674e7 both times, so this verdict holds for that SHA. Develop was cfb6c1573ba9 at the start and **moved to abd044f63a9d (KS-1231) by the end.** The merge is still clean (below).

## BLUF

Option a is built as the card says, and it holds when run.
- Under NODE_ENV=production, the shared guard refuses each of the eight PUBLISHED_TEMPLATE_VALUES and exits 1. It refuses nothing under development or staging. All 8 of my planted real values pass, and so do near-miss values.
- On the production render, every service that receives one of the eight names runs NODE_ENV=production and calls the guard at top level.
- demo-service is out of the default production render. If the profile is enabled, it refuses the published key.
- All ten of gate 233's findings are closed or have a stated disposition (F9 was left on purpose and is pre-existing).

There are five notes. None blocks:
- One is a test blind spot that I proved with two surviving mutants of my own.
- One is a scope point for Kam: the card says "must-set rows", but the build refuses LOG_LEVEL=debug, CARDANO_NETWORK=preview and a rate limit of 10000 outright.
- Three are wording.

Evidence: the scratch files listed under "My conduct". I wrote nothing else to this folder.

## Findings

### N1. MINOR, does not block. The suite's "every consumer refuses" cell is a text grep. Two of my mutants survive it.
- **Where:** `Blockchain/Dev/scripts/__tests__/production_refuses_published_template_values.test.sh`, `unguarded_of()`, and the section-2 cells that use it.
- **FOUND:** the cell passes when the string `enforceProductionConfig(` appears anywhere in the service's non-test `src`. It does not check two things:
  - (a) whether that service runs with NODE_ENV=production on the render. The guard returns early otherwise (`production-guard.ts:41`).
  - (b) whether the call is ever executed.
- **TESTED / HOW, MEASURED:** I made APFS copies of `Blockchain/Dev` and ran the suite with `PRODUCTION_REFUSES_DEV_DIR`.
  - **M1:** base compose gives `mcp-server` (hard-coded NODE_ENV=development, not overridden by the overlay) `LOG_LEVEL=${LOG_LEVEL:-info}`. The render confirms mcp-server gets NODE_ENV=development and LOG_LEVEL=debug. Suite: **42/42 green.**
  - **M2:** staking's call becomes `if (process.env.G259_NEVER === 'x') enforceProductionConfig(...)`. Suite: **42/42 green.**
- **Today's tree is correct.** I rendered the production overlay from an unedited `env.example`, with no daemon. All 18 services that receive a refused name have NODE_ENV=production. Each one calls the guard at top level: index.ts or server.ts lines 25 to 95, which I read for every one. The three NODE_ENV=development services (mcp-server, tenant-provisioning, tokenisation) receive none of the eight names.
- **Fix-shape, READ ONLY:** in the same cell, also assert that NODE_ENV on the render equals `production` for each pair. Regression row: M1 above must turn that cell red.

### N2. MINOR, does not block; Kam's eyes. The build is wider than the card's words on three non-secret names.
- **Card (read via `decision_queue.sh show`):** "the production guard refuses the published values … **the rate limit, log level and network become must-set rows**".
- **Built:** `LOG_LEVEL: ['debug']`, `CARDANO_NETWORK: ['preview']` and `RATE_LIMIT_MAX_REQUESTS: ['10000']` sit in the refusal table (`production-guard.ts:22-30`). So an operator cannot deliberately choose debug logging, the preview network or 10000 under NODE_ENV=production. With all 8 published values set, each of the 18 consumers exits 1 (driver below).
- This fails closed, J 21st disclosed it as a judgement call in the READY, and the docs say so. **I did not read Wednesday's ANSWER of 09:53:57Z**, so I cannot say whether she ruled this width. If she did, that ruling is wider than Kam's card text.
- **MEASURED** for the guard behaviour. READ for the card.

### N3. MINOR, does not block. The cheat fragment says two things that are untrue of the code.
- **Where:** `Projects Documents/fragments/cheat/KS-1081-env-templates-do-not-diverge-further.html`.
- **(a)** "Production refuses the values env.example publishes: CSRF_SECRET, **DEMO_SERVICE_KEY**, … the table is PUBLISHED_TEMPLATE_VALUES". DEMO_SERVICE_KEY is not in that table, on purpose. It is left out by the profile and refused by demoGuard only under the flag. The flow fragment states this correctly.
- **(b)** It lists the five commented names and then says "For a production-compose run, uncomment and set them." That includes REDIS_HOST and ORIGINATE_SERVICE_URL. `env.example` and checklist row 1.1 now say, correctly, that the production compose ignores those two (gate 233 F10). The cheat sheet was not brought along.
- READ ONLY.

### N4. MINOR, does not block. The text still says Kam's card is open.
- `env_templates_do_not_diverge_further.test.sh` lines 19, 55-60, 110 and 111 (a cell label people read in output), and the flow fragment ("listed because Kam's card on the production path is open").
- The card was ruled `a` at 2026-11-08T20:28:23. The ratchet list itself is still right, because those values stay. READ ONLY.

### N5. MINOR, pre-existing, kept in a line this PR rewrote. `docs/DEPLOYMENT.md:355`.
- The line says "All services run with `NODE_ENV=production`". mcp-server, tenant-provisioning and tokenisation hard-code `NODE_ENV=development` in base `docker-compose.yml` (around lines 2030, 2086 and 2151), and the overlay does not override them. The render shows development for all three.
- They receive none of the eight names, so the guard sentence on line 389 still holds.
- MEASURED render.

## The six questions

### 1. Gate 233's F1 to F10
| F | Disposition at b61674e7 | How I know |
|---|---|---|
| F1 | **Closed.** CSRF_SECRET, the three Stripe names and BLOCKFROST_API_KEY are refused under production. demo-service is out by profile, and its own guard refuses the published key with the profile on. APP_DB_PASSWORD was left out on purpose (neutral, KS-762). | MEASURED (guard driver, render, demoGuard transplant) |
| F2 | **Closed.** `make_clone` takes every template present at the SHA. The new suite gives 15/15. Run against the 0e5b2938 harness it gives **3 red**: MECHANISM plus both F2 plant cells, which reproduces J's claim. | MEASURED. Docker half NOT RUN |
| F3 | **Closed.** 10000 is refused. The DEPLOYMENT.md table and the critical list say 100. | MEASURED |
| F4 | **Closed.** debug is refused. Line 355 no longer claims warn unconditionally. See N5 for the NODE_ENV half. | MEASURED / READ |
| F5 | **Closed.** preview is refused at 6 services. VITE_CARDANO_NETWORK is derived from CARDANO_NETWORK (render, issuer-frontend). | MEASURED |
| F6 | **Closed** for every site gate 233 listed (diff read). Residue: N3, N4. | READ |
| F7 | **Closed** for O1, O6 and O2b: controls at suite lines 165-175, suite 48/48. O5 (the ticket-key exclusion) was not checked by me. | ran suite; READ cells |
| F8 | **Closed by disposition.** Five are moved as commented examples. ENABLE_MOCK_MIDNIGHT and MULTI_TENANCY_ENABLED were not moved, with stated reasons. | READ |
| F9 | **Open by design**, pre-existing, local only, declared in the READY. | READ |
| F10 | **Closed** in `env.example` and checklist 1.1. The cheat fragment still says otherwise (N3b). | READ |

### 2. The production guard
- **FAIL condition stated first:** any of the eight not refused under production; any refused under development or staging; any real value refused.
- **Driver:** `pg_case.mjs` and `run_pg.sh` import the real `production-guard.ts` from the clone with Node 26's built-in type stripping. Each case runs in its own `env -i` process with exit intercepted. Results are in `q2_guard_runtime.txt`. Of 34 cases, every result was as expected:
  - Each of the 8 published values gives exit 1 under production, naming the variable and never the value.
  - All 8 pass under development and under staging (16 cases).
  - A published value padded with spaces is refused.
  - My planted real set passes, exit 0: CSRF `g259-…`, `pk_live_`/`sk_live_`/`whsec_` planted, rate 100, warn, mainnet.
  - Near misses pass: superstrings, `preprod`, `100000`.
  - Blank values pass.
  - `NODE_ENV=Production` and `" production"` pass, because the guard is not entered.
  - Case variants (`LOG_LEVEL=DEBUG`) pass the guard. The logger does not treat them as debug (`logger/index.ts:154-158`, READ), so this is not a bypass.
- **Who consumes what:** the production render from an unedited `env.example` (`prod_render.json`) delivers the published value to: CSRF and RATE at api-gateway; Stripe at billing; BLOCKFROST at anchoring, nft-certificate and staking; CARDANO_NETWORK at 6 services; LOG_LEVEL at 18. All have NODE_ENV=production and a top-level call. Each service's Dockerfile builds `packages/shared` from source (4 read), so the guard ships in the image.
- **Full census** of every template value reaching a production service: the only names not guarded that carry a template value of secret shape are APP_DB_PASSWORD (excluded on purpose) and none other. IPFS_PROVIDER=mock does reach nft-certificate, but that service already refuses mock under production (READ).
- **Live Azure (READ ONLY, nothing touched):** `services.bicep` sets NODE_ENV=staging for common services and `environment` (default `demo` from deploy.sh) for the gateway, while wallet-connector and anchoring carry `CARDANO_NETWORK=preview`. The guard returns early there, so I found no live boot impact by reading.

### 3. demo-service
- **Default production render:** demo-service is absent (`config --services` count 0). `nginx-gateway` depends on it with `required: false` (render). The render rc is 0.
- **With `--profile demo`:** NODE_ENV=development, ENABLED=true, the key equals the published one, and REFUSE_PUBLISHED_KEY=true.
- **demoGuard transplant** (the real file, with only `import` changed to `import type` for express, a type-only import):
  - Overlay shape: **REFUSES**.
  - Local shape (no flag): starts.
  - My own key with the flag: starts.
  - Flag `TRUE`: starts, because the check needs exactly "true", as for ENABLED.
  - Published key plus a trailing space: starts. This is a different key string.
- **Starting it without the profile:** naming the service on the command line (`up demo-service`) is the only way, and the flag still applies then (READ, compose semantics). No Makefile, package.json or deployment script passes `--profile demo` or `COMPOSE_PROFILES`. My grep found 0, and the positive control found `--profile local-llm` in `env.example`.
- **nginx:** `nginx-production.conf` has no demo-service reference (0 hits; the positive control finds it in `nginx-demo.conf`). Its proxies use the variable form with a resolver plus one upstream (`api-gateway … resolve`). So by read, nginx starts and serves without demo-service. **NOT booted** (no daemon).
- My M3 (the `required: false` removed) turns **14 cells red**: compose refuses the project. This confirms J's claim that the line is needed.

### 4. The docs
Read against the code: `env.example` new comments, `DEPLOYMENT.md` (355, 381-388, 423-425, 1022), the checklist (1.1, 1.8, 1.14, 1.24, 1.25, 8.2) and both fragments. All are true except N3, N4 and N5. The new DEPLOYMENT paragraph on the guard and demo-service is true (MEASURED above).

### 5. Mutants and tampers
- **Reproduced shell rows S0, S1, S2, S4, S12 and S21: red 0, 3, 1, 3, 1 and 1 of 42, exactly as J declared.**
- **My own plants:**
  - M1 survives (N1).
  - M2 survives (N1).
  - M3 is killed (14 red).
  - My driver against the old harness: 3 red, as declared.
- **NOT RUN:** the G (vitest, shared) and D (vitest, demo-service) rows. There is no vitest on this host, and npm network use was not commissioned. In their place, my runtime drivers exercised the same functions directly.

### 6. Merge
These ran in a second, blobless bare clone under the session scratchpad (`…/scratchpad/g259/mt.git`, 11 MB), because the no-cd hook refuses `merge-tree` in `/private/tmp/g259`.
- **develop cfb6c157 + 2052:** rc 0. The tree is e536c38a, equal to the head's own tree (develop was already merged in).
- **develop abd044f6 (moved during this gate) + 2052:** rc 0, tree 98c0b260. Develop moved 7 paths and **0 are shared** with the PR.
- **2052 + 2074 (e8c950ec):** rc 0, tree 255d6986. One shared path, `verify-slot-credential-isolation.sh`. The hunks are disjoint (2074 changes the probe greps at lines 76-92; 2052 changes `make_clone` at 54-68).
- **2052 + 2070 (0ae8aa98):** rc 0, tree 7ef36c15. One shared path, `check-stack-safety.sh`, a single comment line.
- **Order:** no constraint found. The semantic suites were not run on the combined trees.

## What was NOT tested
- Docker was down and I did not start it. So the following were not run: any stack, any booted service (including the gateway, demo-service and nginx), and the isolation harness's 23 docker assertions.
- No vitest at all: J's 55 shared and 12 demo-service cells and the G/D tamper rows.
- The full shell runner (I ran 3 suites: 42, 48 and 15 cells, all green), the four platform suites, and shellcheck.
- The PR body and the KS-1081 comment (that needs the API), and Wednesday's ANSWER mails.
- F7 O5. The suites of 2074 and 2070 on the combined trees. The live Azure apps' actual env (read from bicep only).

## My conduct
- **Wrote only:** this verdict; the clone `/private/tmp/g259` (blobless; pushurl DISABLED; worktree clean at the end, 0 status lines; **534 MB**); and scratch under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e9a953f3-ed71-443f-a697-01394a1dde48/scratchpad/g259/`. The scratch holds renders, drivers, mutant copies under `mut/` (APFS clones) and `mt.git`.
- **No `rm`.** Nothing was quarantined or deleted.
- **Network:** git clone, fetch and ls-remote only, with the project's deploy key. The shared checkout was read for its remote URL and sshCommand only.
- **Secrets:** I opened no application `.env`, `.env.local` or real config. The values printed are the template's published sample values, which are in the guard source already. APP_DB_PASSWORD, GRAFANA_PASSWORD and KYC_CALLBACK_API_KEY were masked when read.
- **Hooks:**
  - The no-cd hook refused `merge-tree` in my clone; I moved to the scratchpad clone, as the commission allows.
  - It then refused a compound command that named a path through a variable; I reissued it with literal paths.
  - One `git grep` on the blobless bare clone ran past 2 minutes, fetching blobs; I stopped it (TaskStop).
- **Load:** load1 touched 8.62 once, during the 9-row mutant loop, so I paused. It was under 8 otherwise. DevMASTER had 23 GiB free throughout.
