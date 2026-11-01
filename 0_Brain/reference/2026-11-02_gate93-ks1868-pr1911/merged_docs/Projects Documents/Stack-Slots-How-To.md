# Stack Slots — How to Run Four Platform-K Stacks Side by Side

**Ticket:** [KS-666](https://linear.app/secuura/issue/KS-666) · **PR:** [#729](https://github.com/Secuura/Distributed_Secuura/pull/729)
**Applies to:** platform-k (`Distributed_Secuura`) on the Mac, the only stack host since the Ubuntu VM was retired.

---

## What problem this solves

Before this, every platform-k branch shared **one** Docker project, **one** set of ports, **one**
database volume and **one** set of test-result paths. A routine `--rebuild` or `--fresh-db` on your
branch silently destroyed someone else's stack, their seeded data and their results — and reported
success while doing it.

Slots remove the shared state. Each slot is an independent stack: its own compose project, ports,
volumes, network, Akto side-stack and result directories. You can run four at once. (Until KS-731 this
was true of everything *except* the Postgres and Redis passwords, which were one shared literal — see
**Limits** if your clone predates 2026-09-03.)

---

## The one thing to remember

```
SECUURA_STACK_SLOT=N
```

Everything else is derived from it. **Slot 1 keeps every historic port**, so if you never set the
variable, nothing changes from how the platform worked before.

| Slot | Gateway | Postgres | Redis | PgBouncer | Akto dashboard | Akto Mongo | Compose project |
|------|---------|----------|-------|-----------|----------------|------------|-----------------|
| 1 | 6882 | 6432 | 6379 | 6433 | 9091 | 27017 | *(unset — left to Compose)* |
| 2 | 6982 | 6532 | 6479 | 6533 | 9191 | 27117 | `secuura_slot2` |
| 3 | 7082 | 6632 | 6579 | 6633 | 9291 | 27217 | `secuura_slot3` |
| 4 | 7182 | 6732 | 6679 | 6733 | 9391 | 27317 | `secuura_slot4` |

The rule is `port = base + 100 × (slot − 1)`. The full allocation — including the websites,
Ollama, Cardano and Mongo Express — lives in **`Blockchain/Dev/scripts/port-allocations.json`**,
which is the source of truth. Never change a port in a compose file alone.

**Slot numbering is shared with platform-s** (PS-622), so platform-s slot N automatically points at
platform-k slot N with no extra configuration.

---

## Everyday use

### One ticket = one branch = one worktree = one slot

```bash
git worktree add ~/dev_Obeden/wt/ks-123 feature/ks-123-...
cd ~/dev_Obeden/wt/ks-123
```

Pick a slot no-one else is using and stay on it for the life of the ticket.

### Start a stack

```bash
SECUURA_STACK_SLOT=2 ./Start_Up/start-secuura.sh            # start
SECUURA_STACK_SLOT=2 ./Start_Up/start-secuura.sh --rebuild  # rebuild images
SECUURA_STACK_SLOT=2 ./Start_Up/start-secuura.sh --status   # what's up
SECUURA_STACK_SLOT=2 ./Start_Up/start-secuura.sh --stop     # stop (keeps volumes)
SECUURA_STACK_SLOT=2 ./Start_Up/start-secuura.sh --fresh-db # DESTROYS this slot's volumes
```

Only the first slot you build pays the full image-build cost; the others reuse the layer cache and
come up in a few minutes.

### Start that slot's Akto side-stack (once per slot)

Akto is a separate stack and **is not started with the platform**. A per-slot scan needs it:

```bash
cd systemTest/akto
SECUURA_STACK_SLOT=2 npm run start
```

Skip this and the scan fails pre-flight with a message naming the port and this command.

### Run a suite against a slot

```bash
systemTest/run-in-slot.sh 2 npm run test:pr
systemTest/run-in-slot.sh --no-wait 2 npx playwright test --project=api
```

`run-in-slot.sh` takes an exclusive lock, points every harness at that slot, and runs your command.
Exit codes: **the command's own**, or `1` if another suite holds the slot and you passed
`--no-wait`, or `2` for a usage error.

### Label your results with the ticket

```bash
SECUURA_TICKET=KS-123 systemTest/run-in-slot.sh 2 npm run test:pr
```

Result directories then read `…-ks-123-slot2` instead of just `…-slot2`.

---

## One suite at a time per slot

**Slots run in parallel with each other. Suites within a slot do not.** `run-in-slot.sh` enforces
this with a lock; a second suite waits, or fails fast with `--no-wait`.

This is not tidiness. Two harnesses on one slot share a gateway, a database and one seeded state —
Akto replays traffic while k6 measures latency, so the performance figures describe a stack under
someone else's load and the Akto findings describe a system mid-load-test. Neither errors. Both
measure something nobody asked about.

The other reason is the **per-IP login rate limiter**: a second concurrent suite on the same slot
trips it and poisons both runs. If you see 429s, **wait 15 minutes before retesting** — that applies
to Schemathesis, Playwright, Akto and k6 alike.

A valid four-way run is one suite per slot:

```
slot 1  Playwright        slot 3  Schemathesis
slot 2  k6 performance    slot 4  Akto
```

---

## Where your results go

Every harness labels its output `<ticket>-slot<N>` — **including slot 1**, so no run is unlabelled
and every number traces back to the stack that produced it. None of it is committed; the ignore
patterns are asserted by a gate.

```
systemTest/playwright/results/playwright-report-ks-123-slot2/
systemTest/playwright/results/test-results-ks-123-slot2/
systemTest/schemathesis/output/reports/<profile>-ks-123-<timestamp>-slot2/   (+ latest-slot2)
systemTest/performance/reports/performance-reports/<profile>-ks-123-<timestamp>-slot2/
systemTest/akto/output/reports-slot2/
```

Credentials are slot-scoped too — `systemTest/playwright/.auth-ks-123-slot2/` and
`systemTest/schemathesis/.env-ks-123-slot2`. They hold live bearer tokens and are gitignored.
Before this they were single shared paths, so two slots overwrote each other's tokens and the
loser authenticated against the wrong stack.

---

## The guard

Destructive operations (`--stop`, `--fresh-db`, `--rebuild`) call
`Blockchain/Dev/scripts/stack_guard.sh` first. It reads ownership labels off the running containers
and refuses when the stack is not yours or your tree is dirty.

| Exit | Meaning |
|------|---------|
| 0 | safe — nothing running, or it is yours and the tree is clean |
| 1 | blocked — a foreign-owned stack is running, or the tree is dirty |
| 2 | usage error, or the environment cannot be inspected (no docker / no git) |

Override with `--i-have-confirmed-with-the-owner`. It is deliberately long, and it is logged.

**It warns rather than blocks on an unlabelled stack.** A stack started before this change, or by a
bare `docker compose up`, carries no ownership labels — the guard says so and names the container
count, but does not stop you. Blocking there would fire on every pre-existing stack and be
overridden reflexively within a day.

---

## Checking your setup

```bash
cd Blockchain/Dev
bash scripts/check-container-isolation.sh    # live: names, volumes, networks, service counts
node scripts/check-port-crossover.mjs        # every allocation disjoint for slots 1-4
bash scripts/check-stack-safety.sh           # the compose + gitignore invariants
bash scripts/check-script-portability.sh     # host scripts avoid macOS-hostile constructs
```

Each has a unit-test suite under `scripts/__tests__/` that proves it can fail — a gate that only
ever passes is a claim with a tick next to it, and two in this branch turned out to be exactly that
before they were fixed.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Suite hits the wrong stack's data | A hardcoded slot-1 default somewhere in the harness | Check the run banner names your slot; if not, raise it — this class recurred five times during KS-666 |
| Akto scan fails pre-flight | That slot's Akto side-stack isn't running | `cd systemTest/akto && SECUURA_STACK_SLOT=N npm run start` |
| `401` / `SESSION_INVALIDATED` everywhere | The sweep locked out its seeded account ([KS-575](https://linear.app/secuura/issue/KS-575)) | `--fresh-db` that slot to re-seed |
| 429s / rate limiting | Two suites on one slot, or a recent heavy run | One suite per slot; wait 15 minutes |
| Second suite appears to hang | It is waiting on the slot lock — by design | `--no-wait` to fail fast instead |
| A gate is slow or reports oddly on macOS | GNU-only assumption in a script | `bash scripts/check-script-portability.sh` |

---

## Limits

- **Four slots.** Not arithmetic — CI assigns the same numbers per *suite*, and slot 5 would land on
  the CI integration block (7282 / 6832). Docker Desktop's allocation binds well before that.
- **The two platforms' own allocations** do not collide until platform-s slot 9.
- **Measured 2026-08-20:** four platform-k stacks plus two Akto side-stacks = 142 containers,
  all healthy, four gateways serving. Four stacks *running* is proven; four heavy suites executing
  simultaneously measures CPU contention, not correctness.
- **Untested:** each harness has only been exercised on one slot, so 12 of 16 harness-slot
  combinations are unproven. Every slot-1-hardcoding defect found during this work was invisible
  until something ran on a slot other than 1.
- **Datastore credentials are per-clone only from KS-731 onwards — an EXISTING clone is still on the
  shared one.** Until 2026-09-03 `POSTGRES_PASSWORD` and `REDIS_PASSWORD` were static literals in the
  example files, identical on every slot, worktree, clone and machine, so any slot could read, write
  and **DROP** another slot's Postgres *as superuser* and read/write its whole Redis keyspace — the
  ports were never the defect (a service is reachable cross-slot **iff** it publishes a host port;
  26 of 33 publish nothing). `scripts/bootstrap-env.sh` now generates both per clone, and a cross-slot
  connection was **measured** failing authentication in both directions with a same-slot positive
  control — see *What slots DO and do NOT isolate* in `systemTest/CLAUDE.md` for the matrix and the
  three controls. **Pulling does not fix an existing clone:** bootstrap never overwrites a set value,
  and Postgres bakes `POSTGRES_PASSWORD` at first init, so adoption needs the four values blanked, a
  re-run of bootstrap, and a `--remove-volumes` teardown per slot. Four slots from ONE worktree share
  a single `.env` and can never be credential-isolated.

---

## Reference

| Thing | Where |
|---|---|
| Port allocations (source of truth) | `Blockchain/Dev/scripts/port-allocations.json` |
| Port registry (human-readable) | `Projects Documents/PORT-REGISTRY.md` |
| Slot derivation — stack | `Blockchain/Dev/scripts/stack_env.sh` |
| Slot derivation — harnesses | `systemTest/slot-target.sh` |
| Per-slot serial runner | `systemTest/run-in-slot.sh` |
| Destructive-operation guard | `Blockchain/Dev/scripts/stack_guard.sh` |
| Verification evidence | `Projects Documents/KS-666-Shared-Stack-Safety-Evidence.html` |
