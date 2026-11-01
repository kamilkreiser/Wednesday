# Port Registry

Complete reference for every host port binding in the Distributed Secuura project. Covers the main platform,
monitoring, system tests (Akto, observability stack), and local development tooling.

**Last updated:** 2026-09-11 (KS-687 / PR #933 — Akto side-stack section added below the Playwright one, and the four Akto rows are now *enforced* by the harness, not only derived: a run whose artefact references another slot's port fails. No port allocation changed; still 110.)

_Previously:_ 2026-09-11 (KS-971 merge with `develop` after KS-682 / PR #896 landed — both port additions are now registered together: `PW_REPORT_PORT` base 9324 (KS-682) and `K6_WEB_DASHBOARD_PORT` base 5665 (KS-971). Allocation count 106 -> 110, as the cross-check below predicted. No existing allocation changed. The `CARDANO_SUBMIT_PORT` slot row, which had landed in the flat port table on `develop`, is moved to the slot table where it belongs.)

_Previously:_ 2026-09-02 (KS-691 — `/health` no longer reports a port; Akto Mongo Express row corrected 8081 -> 9490. No port *allocation* changed)

---

## Quick Reference — All Host-Exposed Ports

Every host-published port across all stacks, sorted by port. Detailed sections below have the host:container bindings.

> **These are slot 1 values.** Under KS-666 every platform-k port is `base + 100 * (slot - 1)` — see [Stack Slots](#stack-slots-ks-666).

| Port      | Service / Tool                         | Stack                                  | Always On? | URL                    |
| --------- | -------------------------------------- | -------------------------------------- | ---------- | ---------------------- |
| 3000      | Grafana (observability dashboards)     | Observability stack                    | No         | http://localhost:3000  |
| 3100      | Loki (log aggregation)                 | Performance observability              | No         | —                      |
| 5665      | k6 web dashboard (live run UI)         | systemTest/performance (during a run)  | No         | http://localhost:5665  |
| 6000–6013 | Microservice debug ports (10 services) | Platform (dev-debug override)          | No         | —                      |
| 6090      | Cardano mock API                       | Platform (`--profile mock`)            | No         | http://localhost:6090  |
| 6091      | Yaci CLI web UI (Cardano devnet)       | Platform (`--profile devnet`)          | No         | http://localhost:6091  |
| 6092      | Yaci Submit API (Cardano devnet)       | Platform (`--profile devnet`)          | No         | http://localhost:6092  |
| 6093      | Cardano Node port (devnet)             | Platform (`--profile devnet`)          | No         | —                      |
| 6094      | Cardano Tx submit API (devnet)         | Platform (`--profile devnet`)          | No         | —                      |
| 6379      | Redis (dev only)                       | Platform                               | Yes (dev)  | —                      |
| 6432      | PostgreSQL — direct (dev only)         | Platform                               | Yes (dev)  | —                      |
| 6433      | pgbouncer (pooled Postgres, dev)       | Platform                               | Yes (dev)  | —                      |
| 6881      | Marketing website                      | Platform                               | Yes        | http://localhost:6881  |
| 6882      | Nginx gateway (primary)                | Platform                               | Yes        | http://localhost:6882  |
| 9490      | Mongo Express (browse MongoDB)         | systemTest/akto (`tools`, loopback)    | No         | http://localhost:9490  |
| 8881      | Tokenomics website                     | Platform                               | Yes        | http://localhost:8881  |
| 9090      | Prometheus (observability)             | Observability stack                    | No         | http://localhost:9090  |
| 9091      | Akto dashboard                         | systemTest/akto                        | No         | http://localhost:9091  |
| 9323      | Playwright HTML report (platform-s)    | platform-s systemTest (`npm run report`) | No       | http://localhost:9323  |
| 9324      | Playwright HTML report (platform-k)     | systemTest/playwright (`npm run report`) | No       | http://localhost:9324  |
| 11434     | Ollama (local LLM)                     | Platform (`--profile local-llm`)       | No         | http://localhost:11434 |
| 12345     | Grafana Alloy (log shipper UI)         | Performance observability              | No         | http://localhost:12345 |
| 27017     | MongoDB (Akto store, auth enabled)     | systemTest/akto                        | No         | —                      |

---

## Stack Slots (KS-666)

**Source of truth: `Blockchain/Dev/scripts/port-allocations.json`.** Edit the bases there, never
in a compose file alone. Three gates enforce this file, and each is itself unit-tested so it can
be shown to fail rather than merely to pass:

| Gate | Asserts | Its own tests |
| ---- | ------- | ------------- |
| `scripts/check-port-crossover.mjs` | **110 allocations across 3 configurations** (platform-k 17, platform-s 8, observability 10) are disjoint for slots 1-4 | mutation-tested: restoring a colliding base fails the build |
| `scripts/check-container-isolation.sh` | **6 live invariants** — no container name, named volume or network shared between stacks; slot prefixes correct; every platform slot runs the same service count; nothing exited non-zero | `__tests__/check_container_isolation.test.sh` — **48 cases** |
| `scripts/check-script-portability.sh` | host-side shell scripts avoid 7 constructs that silently misbehave on macOS (the evidence host) | `__tests__/check_script_portability.test.sh` — **21 cases** |

**The observability stack is in the registry as an *unslotted* configuration.** Its ports are fixed
(one shared instance serves every slot, KS-200), but they must still be in the comparison: an
interim KS-666 base of 9090 for `AKTO_MONGO_EXPRESS_PORT` collided head-on with Prometheus,
re-opening the clash this document records as fixed on 2026-06-18. The gate could not see it
because only slotted platforms were modelled.

Every port in the sections below is the **slot 1** value. A slot is selected with
`SECUURA_STACK_SLOT=N` (platform-k) or `STACK_SLOT=N` (platform-s), and:

```
port = base + 100 * (slot - 1)
```

Slot numbering is **shared between platform-k and platform-s** (platform-s PS-622), so platform-s
slot N and platform-k slot N pair up with no extra configuration. Slot 1 keeps every historic port
AND deliberately leaves `COMPOSE_PROJECT_NAME` unset, so an existing local stack and its volumes
are untouched by this scheme.

| Variable | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| -------- | ------ | ------ | ------ | ------ |
| `K6_WEB_DASHBOARD_PORT` (**harness-bound**, not stack-published) | 5665 | 5765 | 5865 | 5965 |
| `GATEWAY_PORT` | 6882 | 6982 | 7082 | 7182 |
| `POSTGRES_EXTERNAL_PORT` | 6432 | 6532 | 6632 | 6732 |
| `REDIS_EXTERNAL_PORT` | 6379 | 6479 | 6579 | 6679 |
| `PGBOUNCER_PORT` | 6433 | 6533 | 6633 | 6733 |
| `WEBSITE_PORT` | 6881 | 6981 | 7081 | 7181 |
| `TOKENOMICS_PORT` | 8881 | 8981 | 9081 | 9181 |
| `AKTO_DASHBOARD_PORT` | 9091 | 9191 | 9291 | 9391 |
| `AKTO_MONGO_PORT` | 27017 | 27117 | 27217 | 27317 |
| `AKTO_MONGO_EXPRESS_PORT` | 9490 | 9590 | 9690 | 9790 |
| `APP_HTTP_PORT` (**platform-s**) | 1021 | 1121 | 1221 | 1321 |
| `APP_HTTPS_PORT` (**platform-s**) | 1022 | 1122 | 1222 | 1322 |
| `HTTP_PORT` (**platform-s**) | 5121 | 5221 | 5321 | 5421 |
| `HTTPS_PORT` (**platform-s**) | 5122 | 5222 | 5322 | 5422 |
| `MAILPIT_PORT` (**platform-s**) | 8025 | 8125 | 8225 | 8325 |
| `PW_REPORT_PORT` (**platform-s**, host-bound by `npm run report`) | 9323 | 9423 | 9523 | 9623 |
| `PW_REPORT_PORT` (**platform-k**, host-bound by `npm run report`) | 9324 | 9424 | 9524 | 9624 |
| `OLLAMA_PORT` | 11434 | 11534 | 11634 | 11734 |
| `CARDANO_MOCK_PORT` | 6090 | 6190 | 6290 | 6390 |
| `YACI_STORE_PORT` | 6092 | 6192 | 6292 | 6392 |
| `CARDANO_SUBMIT_PORT` (**platform-k**) | 6094 | 6194 | 6294 | 6394 |

**Why four.** Four is a deliberate ceiling, not the arithmetic limit — the binding constraint is
Docker Desktop's CPU/memory allocation, and (see Known Conflicts) slot 5 would land on the CI
integration suite's port block. The two platforms' own allocations do not collide until
platform-s slot 9.

### Playwright (platform-k) — every port a run touches, slots 1-4

Asked from the other direction, because "which ports does the Playwright suite use on slot 3?" is
the question people actually have, and the table above answers it only if you already know which
rows belong to Playwright (KS-682).

| What | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| ---- | ------ | ------ | ------ | ------ |
| **Binds** — HTML report server, `npm run report` | 9324 | 9424 | 9524 | 9624 |
| **Targets** — platform gateway, `API_BASE_URL` (`…/api`) | 6882 | 6982 | 7082 | 7182 |

**The suite binds exactly ONE port**, and only while you are reading a report. Everything else it
uses is the platform stack's own gateway, which the stack publishes and the suite merely connects
to — so a Playwright run adds one host port per slot, not a block. The gateway row is the same
`GATEWAY_PORT` as above; it is repeated here because a reader chasing a Playwright port needs both
halves and should not have to know that `API_BASE_URL` is derived from `GATEWAY_PORT`.

Generated by resolving the suite's own config for each slot on 2026-09-03, not transcribed:
`API_BASE_URL` came back as `http://localhost:{6882,6982,7082,7182}/api/` and the report port from
`reportPort(slot)`. Slot 1's row was derived from the same helpers without setting the slot.

Two consequences worth stating, both measured:

- **Two slots' reports can be open at once.** That is the whole reason the report port is slotted;
  before KS-682 `show-report` took Playwright's default unconditionally and the second slot died on
  `EADDRINUSE` with a raw Node trace naming neither the slot nor the fix.
- **Nothing else on either platform uses 9324/9424/9524/9624.** Checked against every slotted base
  in this registry at all four slots, against the unslotted observability ports individually, and
  against every port the `systemTest/` tooling references (which includes k6's dashboard on 5665
  and the Akto side-stack). `scripts/check-port-crossover.mjs` is the gate; the assertion also
  lives with the code in `systemTest/playwright/tests-unit/slot-isolation.test.ts`.

### Akto (platform-k) — every port a run touches, slots 1-4 (KS-687)

Same question, asked for the one harness that runs its **own** Docker stack beside the platform.

| What | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| ---- | ------ | ------ | ------ | ------ |
| **Binds** — Akto dashboard, `AKTO_DASHBOARD_PORT` | 9091 | 9191 | 9291 | 9391 |
| **Binds** — Akto MongoDB, `AKTO_MONGO_PORT` | 27017 | 27117 | 27217 | 27317 |
| **Binds** — Mongo Express, `AKTO_MONGO_EXPRESS_PORT` (`tools` profile, loopback) | 9490 | 9590 | 9690 | 9790 |
| **Targets** — platform gateway, `SECUURA_API_URL` / `OVERRIDE_APP_URL` (`…/api`) | 6882 | 6982 | 7082 | 7182 |
| Containers / compose project / volumes | `akto-*` / `akto` / `akto_*_data` | `akto-s2-*` / `akto_s2` / `akto_*_data_s2` | `akto-s3-*` / `akto_s3` / `akto_*_data_s3` | `akto-s4-*` / `akto_s4` / `akto_*_data_s4` |

Two or three host ports per slot, all `base + 100 × (slot − 1)`, none typed per slot anywhere in
`systemTest/akto` — `src/config/slot.ts` reads a port *back* to its slot from the same rule.

**Since KS-687 these rows are enforced, not merely derived.** The harness refuses at `validate()` any
run whose pieces name different slots (`SECUURA_STACK_SLOT`, `AKTO_PREFIX`, dashboard URL, scan target,
artefact suffix) or an unusable slot request; pre-flight probes the scan's own origin; and after every
scan the persisted artefact is walked — a local host on **another slot's port** fails the run
(`src/scan/slotLeakCheck.ts`). So a scan that reached slot 1 from a slot-3 shell no longer passes; it is
refused with the offending `host:port` named.

Measured, not transcribed — all four slots, this Mac, 2026-09-10 (pre-merge tier, each slot built alone
from clean): slot 1 8,933 executed, artefact 2,619 × `:6882`; slot 2 8,909, 2,626 × `:6982`; slot 3
8,902–8,920 (×3), 2,620–2,635 × `:7082`; slot 4 8,907, 2,619 × `:7182`; **zero references to any other
slot's port in any artefact**. Re-run on slot 4 from the develop-merged tree 2026-09-11: 9,105 / 9,138
executed, 2,346 / 2,343 × `:7182`, again zero foreign. The gate is `scripts/check-akto-container-names.sh`
(a slot-1 container name — literal *or* `${VAR:-akto-mongo}` — anywhere in `src/ bin/ scripts/` fails
`check-stack-safety.sh` 6f2).

Each slot also gets its own **Akto side-stack** (`akto-s2-*`, `akto-s3-*`, …) and its own
**results directories**, labelled `<ticket>-slot<N>`. Derivation lives in
`Blockchain/Dev/scripts/stack_env.sh` (the stack) and `systemTest/slot-target.sh` (the harnesses).

---

### Schemathesis (platform-k) — every port a run touches, slots 1-4 (KS-1016)

Same question for the harness that resolves the slot itself. `systemTest/schemathesis/src/slot.py`
reads `SECUURA_STACK_SLOT` (or `STACK_SLOT`) and derives everything below by the `stack_env.sh` rule;
nothing is typed per slot, and a value the shell refuses (`0`, `01`, `abc`, `5`) is refused here too.

| What | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| ---- | ------ | ------ | ------ | ------ |
| Gateway the sweep, hooks and persona logins hit (`resolve_gateway_url()`) | 6882 | 6982 | 7082 | 7182 |
| Postgres container the anchoring DB sweeps `docker exec` into (`resolve_stack_prefix()`) | `secuura-postgres` | `secuura-s2-postgres` | `secuura-s3-postgres` | `secuura-s4-postgres` |
| Compose project the anchoring controller stops/recreates (probed off the running gateway) | compose default | `secuura_slot2` | `secuura_slot3` | `secuura_slot4` |
| Report directory / `latest` pointer suffix (`resolve_artifact_suffix()`, slot requested) | `-slot1` | `-slot2` | `-slot3` | `-slot4` |
| Pushgateway grouping key (`…/environment/local/slot/N`, shared `:9099`) | `slot/1` | `slot/2` | `slot/3` | `slot/4` |

**Shared by design:** the observability stack (`:9099` Pushgateway, `:3000` Grafana) is one per host; the slot
lives in the grouping key and the annotation tag, not in the port. **Refused by design:** a DB read or a compose
write whose container names a different slot than the gateway (`StackDbUnavailableError` / `RuntimeError`,
both naming the two slots).

**Proven 2026-09-10/11 on the Mac, one slot at a time with every other slot torn down** (0 containers / 0
images / 0 volumes / no listener on the other gateways), launched with no slot-targeting variable set and
every `docker` call audited through a PATH shim on 2026-09-10: `pr` profile on slots 4, 3, 2 and 1 — every request to
the slot's own gateway (2,234–3,047 occurrences per run), zero to any other, zero `docker` calls, artifacts and
`latest-slotN` pointer carrying the slot. Runs of record `pr-ks-1016-2026-09-10T14-23-10Z-slot4`, `…T14-42-18Z-slot3`,
`…T14-59-43Z-slot2`, `…T15-13-44Z-slot1`, and `pr-ks-1016-2026-09-11T11-11-33Z-slot4` /
`…T11-23-57Z-slot4` on the rebased head (first sweeps with the admin persona seeded: run validity OK,
0 of 316 errored).

> **A LOCAL run must name its slot (KS-1016, 2026-09-11).** Every harness — Schemathesis, k6,
> Playwright, Akto and the shared provisioning step — refuses to start against a **local** target
> (`localhost`, `127.0.0.1`, `[::1]`, `host.docker.internal`) when neither `SECUURA_STACK_SLOT` nor
> the platform-s alias `STACK_SLOT` is set, and prints the command to run instead:
>
> ```text
> No stack slot named. Every LOCAL system-test run must say which Docker stack it targets.
>   SECUURA_STACK_SLOT=2 python3 scripts/run.py pr
>   or: systemTest/run-in-slot.sh 2 python3 scripts/run.py pr
> ```
>
> **Local only.** A remote target (demo, a tunnel) carries no slot and is left alone, and CI is
> exempt because its isolated per-suite stacks are local by construction and deliberately unslotted
> (GitHub Actions sets `CI=true`; the exemption is a convention, not a lock). Before this rule an
> unset slot meant slot 1 silently — another ticket's stack on a shared machine.

## Main Platform

**Compose file:** `Blockchain/Dev/docker-compose.yml`

### Always-on services

| Port | Host binding    | Service            | Notes                                                         |
| ---- | --------------- | ------------------ | ------------------------------------------------------------- |
| 6882 | `6882:80`       | nginx-gateway      | Primary entry point — all portal and API traffic goes here   |
| 6881 | `6881:80`       | website-frontend   | Marketing website                                            |
| 8881 | `8881:80`       | tokenomics-website | Tokenomics site; defined in `docker-compose.local.yml`        |
| 6432 | `6432:5432`     | postgres           | Direct Postgres (dev only; removed in production)            |
| 6433 | `6433:6432`     | pgbouncer          | Connection pooler (dev only; removed in production)           |
| 6379 | `6379:6379`     | redis              | Cache and session store (dev only; removed in production)     |

#### Gateway routes (all via port 6882)

| Path prefix     | Destination                        | URL                              |
| --------------- | ---------------------------------- | -------------------------------- |
| `/`             | issuer-frontend                    | http://localhost:6882/           |
| `/verify/`      | verifier-frontend                  | http://localhost:6882/verify/    |
| `/admin/`       | admin-frontend                     | http://localhost:6882/admin/     |
| `/status/`      | status-frontend                    | http://localhost:6882/status/    |
| `/website/`     | website-frontend                   | http://localhost:6882/website/   |
| `/showcase/`    | showcase static demo pages         | http://localhost:6882/showcase/  |
| `/api/`         | api-gateway (internal :8080)       | http://localhost:6882/api/       |
| `/api/docs`     | OpenAPI / Swagger UI               | http://localhost:6882/api/docs   |
| `/system/`      | api-gateway — system routes        | http://localhost:6882/system/    |
| `/webhooks/`    | api-gateway — inbound webhooks     | http://localhost:6882/webhooks/  |
| `/originate/`   | originate (direct, internal :4000) | http://localhost:6882/originate/ |
| `/analytics/`   | analytics (direct, internal :4010) | http://localhost:6882/analytics/ |

> **Note:** routes reflect the active local gateway config (`docker/nginx-gateway/nginx-demo.conf`). `demo-service` (internal :4030) runs in the stack but is **not** gateway-routed locally — the former `/demo-api/` route was removed, and as of KS-641 the `/health` JSON no longer advertises it either. (This note previously flagged that JSON as stale; it no longer is.)
>
> **`/health` does not report a port (KS-691).** It used to return `"port":6882`. `nginx-demo.conf` is bind-mounted read-only into *every* slot, so that literal was correct only on slot 1 and wrong on slots 2-4 — a slot-2 gateway on 6982 still reported 6882. The key was removed rather than templated: the port is not information a caller lacks, since they had to connect to it to get the response. **To identify a slot, read the port you connected on**, or use the `base + 100 * (slot - 1)` rule in [Stack Slots](#stack-slots-ks-666).

### Observability (standalone stack — KS-200)

Grafana/Prometheus are no longer a platform `--profile monitoring`. They live in the
standalone `observability/` stack on ports 3000/9090. Start with: `cd observability && npm run start`.
See the Observability Stack section below and `observability/README.md`.

### Optional profile: `--profile devnet`

Start with: `docker compose --profile devnet up -d`

| Port | Host binding  | Service        | Notes                                |
| ---- | ------------- | -------------- | ------------------------------------ |
| 6091 | `6091:3001`   | cardano-devnet | Cardano node N2N                     |
| 6092 | `6092:8080`   | cardano-devnet | Yaci Store API (`/api/v1/…` — epochs, utxos) |
| 6093 | `6093:10000`  | cardano-devnet | Cluster admin API                    |
| 6094 | `6094:8090`   | cardano-devnet | Tx submit API (in-network consumers use `cardano-devnet:8090`) |

> **Corrected 2026-09-07 (KS-971).** `CARDANO_SUBMIT_PORT` (6094) was allocated in
> `port-allocations.json` and bound by `docker-compose.yml:375`, but appeared nowhere in this
> document — and the 6092 row named the wrong container port (`8090`, not `8080`) and the wrong
> service, describing the Submit API that is actually on 6094. Every row above is now transcribed
> from `Blockchain/Dev/docker-compose.yml:372-375`. Found by the generalised registry check in
> `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh`, which previously verified a hardcoded
> list of three Akto names and so could not see a fourth port go unrecorded.

### Optional profile: `--profile mock`

Start with: `docker compose --profile mock up -d`

| Port | Host binding | Service       | Notes                |
| ---- | ------------ | ------------- | -------------------- |
| 6090 | `6090:80`    | cardano-mock  | Cardano mock API     |

### Optional profile: `--profile local-llm`

Start with: `docker compose --profile local-llm up -d`

| Port  | Host binding    | Service | Notes                                             |
| ----- | --------------- | ------- | ------------------------------------------------- |
| 11434 | `11434:11434`   | ollama  | Local LLM inference (macOS Apple Silicon or Linux) |

### Optional profile: `--profile phase2`

Start with: `docker compose --profile phase2 up -d`

Phase-2 services (`guardian`, `queue`) — internal-only, **no host port bindings**. Their internal ports (4006, 4007) are listed under *Internal-only ports* below.

### Internal-only ports (not exposed to host)

These ports are used for container-to-container communication only. They are never bound to the host.

| Port | Service              | Notes                                    |
| ---- | -------------------- | ---------------------------------------- |
| 4000 | originate            | Document issuance and credential lifecycle |
| 4001 | prism                | DID management                           |
| 4002 | wallet-connector     |                                          |
| 4003 | auth                 | Authentication and JWT issuance          |
| 4004 | timestamping         | RFC-3161 TSA                             |
| 4005 | anchoring            | Cardano blockchain anchoring             |
| 4006 | guardian             | Guardian service (`--profile phase2`)    |
| 4007 | queue                | Async job queue (`--profile phase2`)     |
| 4008 | security             | Security enforcement layer               |
| 4010 | analytics            |                                          |
| 4011 | kyc                  | Know-Your-Customer / identity verification |
| 4012 | midnight             | ZK proof management                     |
| 4013 | m365-integration     | Microsoft 365 integration                |
| 4014 | vc-issuer            | W3C Verifiable Credentials               |
| 4015 | staking              | Phase 5                                  |
| 4016 | referral             | Phase 5                                  |
| 4017 | governance           | Phase 4                                  |
| 4018 | nft-certificate      | NFT / certificate issuance               |
| 4019 | billing              | Stripe integration (Phase 3)             |
| 4020 | transfer             | Phase 2                                  |
| 4021 | tokenisation         | Multi-tenancy PII protection             |
| 4022 | tenant-provisioning  | Multi-tenancy DB lifecycle               |
| 4023 | mcp-server           | MCP HTTP integration                     |
| 4030 | demo-service         | Persona switching and state management   |
| 5432 | postgres             | Internal (services connect via pgbouncer:6432) |
| 6300 | midnight-proof-server | ZK proof generation (internal only — different from platform monitoring's host port 6300) |
| 6379 | redis                | Internal (services connect via redis:6379) |
| 8080 | api-gateway          | Internal HTTP; nginx proxies `/api/` here |
| 8090 | cardano-devnet       | Yaci Submit API (internal container port)  |

### Dev-debug override (not enabled by default)

Expose individual microservice ports for debugger attachment:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev-debug.override.yml up
```

| Host port | Maps to container port | Service            |
| --------- | ---------------------- | ------------------ |
| 6000      | 4000                   | originate          |
| 6001      | 4001                   | prism              |
| 6002      | 4002                   | wallet-connector   |
| 6003      | 4003                   | auth               |
| 6004      | 4004                   | timestamping       |
| 6005      | 4005                   | anchoring          |
| 6008      | 4008                   | security           |
| 6010      | 4010                   | analytics          |
| 6012      | 4012                   | midnight           |
| 6013      | 4013                   | m365-integration   |

> **Security note:** These ports must never be exposed in production. See Pen-test finding F-04.

---

## Observability Stack

**Compose file:** `observability/docker-compose.yml` (repo root — shared platform-wide, KS-200)

Start with (100% standalone — started only from `observability/`, by nothing else): `cd observability && npm run start`

Shared, platform-wide observability — one stack serving all test frameworks (k6,
Playwright, Schemathesis, Akto) and all platform services. Alerting (email +
Slack) is disabled by default; enable via `observability/config/alerting.env`.

| Port  | Host binding  | Container                       | Notes                                                       |
| ----- | ------------- | ------------------------------- | ----------------------------------------------------------- |
| 3000  | `3000:3000`   | secuura-obs-grafana             | Dashboards — credentials: `admin / secuura_perf`            |
| 9090  | `9090:9090`   | secuura-obs-prometheus          | Receives k6 remote-write metrics; scrapes platform + exporters |
| 3100  | `3100:3100`   | secuura-obs-loki                | Log aggregation                                             |
| 12345 | `12345:12345` | secuura-obs-alloy               | Grafana Alloy log shipper admin UI                          |
| 9099  | `9099:9091`   | secuura-obs-pushgateway         | Run-completion summary metrics (container :9091, host :9099) |
| 9187  | `9187:9187`   | secuura-obs-postgres-exporter   | PostgreSQL pool / query / txn metrics                       |
| 9121  | `9121:9121`   | secuura-obs-redis-exporter      | Redis hit-rate / memory / clients                           |
| 9113  | `9113:9113`   | secuura-obs-nginx-exporter      | Gateway request rate / connections                          |
| 8089  | `8089:8080`   | secuura-obs-cadvisor            | Per-container CPU + memory (container :8080, host :8089)     |
| 9308  | `9308:9308`   | secuura-obs-kafka-exporter      | Phase 2 only (`--profile phase2`) — Kafka consumer lag      |

---

## Akto Security Testing Stack

**Compose file:** `systemTest/akto/docker-compose.yml`

Start with: `cd systemTest/akto && docker compose up -d`

> **Prerequisite:** the main platform must already be running on port 6882. Akto scans Secuura via that gateway.

> **These are slot 1 values, and every one of them is slotted.** Each binding below is
> parameterised in the compose file, and `systemTest/slot-target.sh` derives it as
> `base + 100 * (slot - 1)` — so slot 2's Akto is 9191 / 27117 / 9590, slot 3's is
> 9291 / 27217 / 9690, alongside its own `akto-sN-*` containers and its own mongo volume.
> See [Stack Slots](#stack-slots-ks-666) for the full table.

| Port (slot 1) | Host binding | Service | Notes |
| ----- | -------------------- | ----------------------- | ------------------------------------------------------------------------------ |
| 9091  | `${AKTO_DASHBOARD_PORT:-9091}:8080` | akto-dashboard | Akto UI — http://localhost:9091 (internal container port: 8080) |
| 27017 | `${AKTO_MONGO_PORT:-27017}:27017`   | mongo | MongoDB (auth ENABLED) — login `akto` / `akto123` (authDB `admin`). DBs: `admini`, `common` |
| 9490  | `127.0.0.1:${AKTO_MONGO_EXPRESS_PORT:-9490}:8081` | akto-mongo-express | **Optional** web UI to browse Mongo — `tools` profile only (`npm run db:ui`). Loopback + basic auth (creds in `docker.env` `ME_CONFIG_BASICAUTH_*`, default `admin`/`akto123`). Local/dev only. **Host 9490, container 8081** — this row said host `8081` until 2026-09-02, contradicting the Quick Reference, the slot table and the Known Conflicts row that all record the KS-666 move off 8081. Verified against `systemTest/akto/docker-compose.yml:372`. |

> **MongoDB login:** `docker exec -it akto-mongo mongosh -u akto -p akto123 --authenticationDatabase admin`.
> Credentials are set in `systemTest/akto/docker.env` (`MONGO_INITDB_ROOT_*`) and embedded in `AKTO_MONGO_CONN`; change
> them there (or via Azure Key Vault `npm run sync-secrets`) — a fresh volume (`docker compose down -v`) is needed for new
> creds. The Akto **dashboard** login (`issuer@secuura.com`) is separate. See `systemTest/akto/docs/configuration.md`.

> The `akto-testing`, one-shot `akto-init-user`, and `akto-puppeteer-replay` services
> expose no host ports (puppeteer-replay is reached over the Docker network on its
> internal `:3000`). The canonical local stack uses no Kafka and no `akto-runtime`.

> **Why 9091 and not 9090?** The observability stack Prometheus (`secuura-obs-prometheus`) binds `9090` on the host.
> Akto's dashboard is mapped to host `9091` to avoid this conflict. The Akto dashboard container listens internally on
> `8080` (per the canonical upstream compose, which maps `9090:8080`).

### Per-slot isolation — every Akto host port, slots 1-4 (KS-666 / KS-691)

Akto runs its **own** docker stack beside the platform, so a slot's Akto must be isolated on
three axes at once — **host ports**, **container names**, and **named volumes**. Ports alone are
not enough: Akto pins its volumes with an explicit `name:`, which overrides compose project
scoping, so two slots sharing a volume name share one mongo regardless of project.

The table below is **generated by running `systemTest/slot-target.sh` for each slot**, not copied
from a compose file. Bases live in `Blockchain/Dev/scripts/port-allocations.json`; the rule is
`base + 100 * (slot - 1)`.

| Variable / artefact | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| ------------------- | ------ | ------ | ------ | ------ |
| `AKTO_DASHBOARD_PORT` (host -> container 8080) | 9091 | 9191 | 9291 | 9391 |
| `AKTO_MONGO_PORT` (host -> container 27017) | 27017 | 27117 | 27217 | 27317 |
| `AKTO_MONGO_EXPRESS_PORT` (loopback -> container 8081) | 9490 | 9590 | 9690 | 9790 |
| `AKTO_DASHBOARD_URL` | http://localhost:9091 | http://localhost:9191 | http://localhost:9291 | http://localhost:9391 |
| `AKTO_PREFIX` (container names `<prefix>-*`) | `akto` | `akto-s2` | `akto-s3` | `akto-s4` |
| `AKTO_COMPOSE_PROJECT` | `akto` | `akto_s2` | `akto_s3` | `akto_s4` |
| `AKTO_MONGO_VOLUME` | `akto_mongo_data` | `akto_mongo_data_s2` | `akto_mongo_data_s3` | `akto_mongo_data_s4` |
| `AKTO_DASHBOARD_VOLUME` | `akto_dashboard_data` | `akto_dashboard_data_s2` | `akto_dashboard_data_s3` | `akto_dashboard_data_s4` |

**Slot 1 deliberately keeps the historic, unsuffixed names.** Renaming its project or volumes
would orphan the existing `akto_mongo_data`, and the stack would come up empty and healthy —
indistinguishable from a wiped database.

> **KS-691 — re-sourcing for a second slot used to keep the first slot's Akto.** The URL exports
> go through `retarget()`, but the `AKTO_*` exports used a plain `${VAR:-default}`, so an already-
> exported value from an earlier `source` won. Sourcing for slot 2 and then slot 3 in one shell
> left **every** value in this table on slot 2 — ports, prefix, project and **mongo volume** —
> while `SECUURA_GATEWAY_URL` correctly moved to slot 3's 7082. Akto then **scanned slot 3 and
> wrote the findings into slot 2's mongo**: not a crash, but a run that succeeds and reports on
> the wrong stack. Measured 2026-09-01. `slot-target.sh` now stamps `SECUURA_SLOT_TARGETED` and
> drops these variables when a later source names a *different* slot, while still honouring a
> value the operator set in this shell (an explicit `AKTO_MONGO_PORT=` for a remote target keeps
> working). Covered by `systemTest/__tests__/slot_target.test.sh`.

**One Akto suite per slot at a time.** The slotting separates concurrent slots, not concurrent
runs against the same slot — two Akto runs on one slot still collide on that slot's ports.

---

## Performance Harness (k6)

**Runner:** `systemTest/performance/runner/k6_docker.ts` · start with `npm run test:<scenario>` from `systemTest/performance`

> **One host port, and it is bound by the HARNESS, not published by the stack.** `docker run -p` maps
> it when observability is enabled; with `--no-obs` (CI) k6's dashboard server is disabled entirely
> (`K6_WEB_DASHBOARD_PORT=-1`) and no host port is taken.

| Variable / artefact | Slot 1 | Slot 2 | Slot 3 | Slot 4 |
| ------------------- | ------ | ------ | ------ | ------ |
| `K6_WEB_DASHBOARD_PORT` (host -> container 5665) | 5665 | 5765 | 5865 | 5965 |
| Dashboard URL | http://localhost:5665 | http://localhost:5765 | http://localhost:5865 | http://localhost:5965 |
| k6 container name | `secuura-perf-k6-<scenario>-slot1` | `…-slot2` | `…-slot3` | `…-slot4` |
| Prometheus tag / Loki label | `slot=slot1` | `slot=slot2` | `slot=slot3` | `slot=slot4` |

Generated by running the derivation in `systemTest/performance/utils/stackSlot.ts`, not copied from a
compose file. The container-side port never moves; only the published side does.

**Why 5665 is safe (KS-971).** It sits on residue **65**, which no other slotted base on either
platform uses — platform-k's are on 17/32/33/34/79/80/81/82/90/91/92/93/94, platform-s's on
21/22/23/25/80/81, plus KS-682's 24. Residues are what matter, because both platforms allocate as
`base + 100 * (slot - 1)`. The unslotted observability ports (3000, 3100, 8089, 9090, 9099, 9113,
9121, 9187, 9308, 12345) get no protection from residues, so 5665/5765/5865/5965 were each checked
against them individually. Asserted in
`systemTest/performance/tests/unit/utils/slotIsolation.test.ts`, which also fails if this document
and `port-allocations.json` ever disagree about the base.

**It was in use before it was registered.** The port has been bound and offset per slot since
KS-666, privately, inside the runner — so the one gate whose job is to prove these sets disjoint
could not see a host port the harness was taking. Registering it moved the count from 102
allocations to 106.

---

## Known Conflicts and Resolutions

| Port  | Conflict                                                    | Resolution                                  |
| ----- | ----------------------------------------------------------- | ------------------------------------------- |
| 9090  | Performance Prometheus vs Akto dashboard                    | Akto mapped to 9091 (fixed 2026-06-18)      |
| 3000  | Performance Grafana vs platform monitoring Grafana          | Platform monitoring uses 6300 instead       |
| 9090  | Performance Prometheus vs platform monitoring Prometheus    | Platform monitoring uses 6301 instead       |
| —     | Container name clash between platform monitoring profile and observability stack | Performance observability containers renamed to `secuura-obs-*` prefix (fixed 2026-06-18) |
| 8081  | Akto Mongo Express vs **platform-s** PMA proxy (`PMA_PROXY_PORT` 8081) | Mongo Express re-homed and slotted — base **9490** (KS-666) |
| 9090  | Akto Mongo Express (interim KS-666 base) vs observability **Prometheus** | Base moved to **9490**; the crossover gate now models the unslotted observability stack, so this class fails the build instead of shipping (KS-666) |
| 9323  | **platform-s** Playwright report server vs the 9xxx band (Akto dashboard 9091-9391, mongo-express 9490+, observability 9090/9099/9113/9121/9187/9308) | No conflict — base chosen on residue **23**, which no slotted base in this registry uses, and checked port by port against the unslotted observability stack (residues do not protect against fixed ports). Nearest neighbours: kafka-exporter 9308 (15 away) and Akto dashboard slot 4 9391 (32). Previously unregistered: `npm run report` bound Playwright's default unconditionally, so a second platform-s slot died on `EADDRINUSE`; it is now slotted and recorded here so the crossover gate can see it |
| 9324  | **platform-k** Playwright report server vs platform-s's on 9323, and vs the 9xxx band | No conflict — a SEPARATE allocation, deliberately not a shared one (KS-682). Reusing 9323 would have the two platforms' reports fight for one port on a machine that routinely runs both, and would make this registry disagree with itself about how many ports each platform takes. Base chosen on residue **24**, which no slotted base here uses (platform-k 90/91/92/93/94/79/32/33/81/82/34/17, platform-s 21/22/23/25/80/81), and each of 9324/9424/9524/9624 checked individually against the unslotted observability stack, which residues do not protect against. It sits one above platform-s's so the pair reads side by side — the cost is that 9423 and 9424 differ by a digit, so read the platform before the port when reading a log. Previously unregistered here for the same reason it was on platform-s: `npm run report` bound Playwright's default unconditionally, so a second slot died on `EADDRINUSE`. Asserted in `systemTest/playwright/tests-unit/slot-isolation.test.ts` |
| —     | **CI per-suite ports reuse the same numbers as local slots** — CI assigns 6882/6982/7082/7182/7282 per *suite* (schemathesis/playwright/performance/akto/integration), while locally the same numbers mean *slot* 1/2/3/4 | **Not a runtime conflict** — each CI suite runs on its own ephemeral runner VM, and only one meaning is ever live on a given host. It is a naming collision to keep in mind when reading a port out of a log: check whether the source is CI or local. It is also why **slot 5 is not available** — it would land on the CI integration suite's block (7282 / 6832) |

---

## Running Stacks Simultaneously

| Scenario                                                   | Safe? | Notes                                              |
| ---------------------------------------------------------- | ----- | -------------------------------------------------- |
| Platform + Performance observability                       | ✅    | No port conflicts; Prometheus scrapes platform via shared network |
| Platform + Akto                                            | ✅    | No port conflicts after 2026-06-18 fix             |
| Platform + Performance observability + Akto                | ✅    | All three can run together                         |
| **Four platform-k slots at once** (slots 1-4)              | ✅    | Verified 2026-08-20 on the Mac from an EMPTY Docker (0 containers / 0 volumes / 0 images): six stacks built `exit=0`, 142 containers, all four gateways 200, 9090 free. A `--fresh-db` of one slot leaves the others untouched (KS-666) |
| **Four platform-k slots + their Akto side-stacks**         | ✅    | Each slot has its own `akto-sN-*` stack, dashboard and Mongo volume |
| **All four harnesses at once, one per slot**               | ✅    | Playwright/1 · k6/2 · Schemathesis/3 · Akto/4, run concurrently 2026-08-20: **zero off-slot `localhost:<port>` references** in any harness, and the slot-4 Akto artifact carried 11,466 host references of which **0** named another slot. One suite per slot at a time — see the serial rule below |
| **One slot at a time, all four harnesses in series on it** | ✅    | Slot 4, 2026-09-11 (develop `9b222d37c` + KS-1016): Schemathesis `pr` → k6 smoke → Playwright `ci:e2e` → Akto pre-merge, each launched with only `SECUURA_STACK_SLOT` and `run-in-slot.sh`; every request stayed on slot 4 (per-run artefact grep), k6's one `docker run` targeted `host.docker.internal:7182` with `secuura.slot=slot4`, slots 1–3 empty throughout. The series rule (one suite at a time, machine-wide) is what makes each suite's numbers quotable |
| platform-k slot N + platform-s slot N                      | ✅    | Shared slot numbering (PS-622); allocations proven disjoint by `check-port-crossover.mjs` |
| More than four slots                                       | ❌    | Not allocated — see Known Conflicts (CI integration block) and Docker Desktop's allocation |

---

## CI/CD

The system-test suites run via a **build-once → clone-across-isolated-stacks** topology. One
`build` job builds all 15 platform images FRESH per run, pushes them to ghcr
(`ghcr.io/secuura/pk-ci-<svc>:<tag>`), and the per-suite jobs PULL those exact images (`up
--no-build`). Each suite runs on its **own ephemeral runner VM** and boots a stack under a unique
`COMPOSE_PROJECT_NAME` + `STACK_PREFIX` (`container_name: ${STACK_PREFIX:-secuura}-<svc>`), which
isolates container names / volumes / networks.

### CI isolated-stack ports (per-suite)

Every suite is **fully isolated**: a unique `COMPOSE_PROJECT_NAME`/`STACK_PREFIX` (names / volumes /
networks) **and** its own **host-port offset (+100)**, with each test tool pointed at its own gateway.
The host ports are parameterized (`${GATEWAY_PORT:-6882}` etc.), so the offsets are just per-suite env:

| Suite (stack) | `GATEWAY_PORT` | `POSTGRES_EXTERNAL_PORT` | `REDIS_EXTERNAL_PORT` | `PGBOUNCER_PORT` | tool → gateway |
| ------------- | --- | --- | --- | --- | --- |
| schemathesis  | 6882 | 6432 | 6379 | 6433 | `--base-url` = `TARGET_BASE` |
| playwright    | 6982 | 6532 | 6479 | 6533 | `API_BASE_URL=…:6982/api` |
| performance   | 7082 | 6632 | 6579 | 6633 | `PERF_BASE_URL=host.docker.internal:7082/api` (k6 runs in a container; `env_flags.ts` honours it) |
| akto          | 7182 | 6732 | 6679 | 6733 | `SECUURA_API_URL=…:7182` (Akto rewrites `localhost`→`host.docker.internal`) |
| integration   | 7282 | 6832 | 6779 | 6833 | pytest → `TARGET_BASE=…:7282` (`stack_prefix: pr-integration`; pre-merge + nightly only). The suite is the anchoring-integrity **Integration mode of Schemathesis**, co-located in `systemTest/schemathesis` (run in CI via `run.py integration`), not a separate project |

Defaults (6882/6432/6379/6433, and each tool's own default) preserve local dev — the offsets are only
set in the CI jobs. Akto additionally boots its own dashboard/mongo stack
(`${AKTO_DASHBOARD_PORT:-9091}` / `${AKTO_MONGO_PORT:-27017}`, `container_name: ${AKTO_PREFIX:-akto}-*`
— parameterized; one Akto suite per tier so defaults are used).

### Workflows

| Workflow file | Test type | Trigger |
| ------------- | --------- | ------- |
| `.github/workflows/pr-platform-suites.yml` | **All 4 PR suites** (schemathesis + playwright + performance smoke + akto PR-gate), one shared build → isolated stacks | Active (`pull_request`) |
| `.github/workflows/nightly-platform-suites.yml` | **All nightly suites** (soak + playwright + perf chain + full-OWASP + Integration anchoring-integrity), one shared build → isolated stacks | Disabled (`workflow_dispatch`; report-only) |
| `.github/workflows/_build-images.yml` | Reusable build-once → ghcr push (called by the above) | Reusable (`workflow_call`) |
| `.github/workflows/pre-merge-platform-suites.yml` | **Pre-merge** (build-once/fan-out): `quality` gate → build → Schemathesis `pre-merge` profile (comprehensive property sweep — the KS-98 sweep moved here from the PR gate) + **Integration suite** (anchoring-integrity, gateway 7282; KS-489-D / KS-492) | Disabled (`workflow_dispatch`) |
| _(also in the two callers above)_ `integration` job | **Integration suite** — orchestrated anchoring-integrity fail-closed + verify-vs-chain (a Schemathesis Integration mode co-located in `systemTest/schemathesis`, run via `run.py integration`; own isolated stack gateway 7282; **pre-merge + nightly**, complete-then-block, NOT a PR gate) | Disabled (`workflow_dispatch`; nightly report-only) |
| _(removed)_ `pr-schemathesis.yml`, `pr-playwright.yml`, `performance-pr.yml`, `akto-pr.yml` | Folded into `pr-platform-suites.yml` | Deleted |
| _(removed)_ `schemathesis-soak.yml`, `playwright-nightly.yml`, `performance-nightly.yml`, `akto-security.yml` | Folded into `nightly-platform-suites.yml` | Deleted |
| `.github/workflows/api-contract-tests.yml` | Schemathesis | Manual (`workflow_dispatch`) |
| `.github/workflows/internal-audit.yml` | Internal audit | Scheduled (`0 2 * * *`) |

> **Cutover note:** the new suite jobs are `build`, `schemathesis`, `playwright`, `performance`,
> `akto` (PR) and their nightly equivalents, plus the pre-merge `akto` job. Branch-protection
> **required checks must be repointed to the check-run _display names_** (GitHub matches required
> checks by display name, not job id):
> `build`, `Schemathesis suite`, `Playwright suite`, `Performance suite (k6 smoke)`,
> `Akto suite (PR)` (renamed from `Akto suite (PR-gate subset)` — KS-413), plus the new pre-merge
> checks `Akto pre-merge (full)` and `Integration suite` (the anchoring-integrity suite; **pre-merge +
> nightly** only, not a PR gate — KS-489-D / KS-492). Both Akto checks are **blocking** (complete-then-block): the PR tier
> runs BOLA/BFLA/Broken-Auth (~30 ids) across all endpoints; the pre-merge tier adds Security
> Misconfiguration (~94 ids). The per-suite workflows + their no-op twins have already been
> **removed** (folded into the two consolidated callers).

---

## Production (Azure)

No host port bindings are used in production. All traffic enters via Azure Container Apps ingress (HTTPS, port 443).
Database and cache are Azure-managed services with no public endpoints. Internal container-to-container communication
uses the same port numbers as local (4000–4030, 5432, 6379) but within a private vnet.
