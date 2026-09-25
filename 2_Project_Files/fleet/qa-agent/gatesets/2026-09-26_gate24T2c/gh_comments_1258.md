--- comment 5835115022 by linear[bot] at 2026-09-25T15:38:37Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1296/run-migrationssh-readiness-probe-discards-command-not-found-and-blames">KS-1296 run-migrations.sh readiness probe discards "command not found" and blames the database — a missing pg_isready reads as "PostgreSQL did not become ready"</a></summary>
<p>

## BLUF

`run-migrations.sh`**'s readiness probe throws away the one message that says what is wrong, then blames the database.** When `pg_isready` is not installed, the probe's `2>/dev/null` discards *"pg_isready: command not found"*, the loop runs its full 30 attempts against a command that never executed, and the script exits 2 with:

```
ERROR: PostgreSQL did not become ready after 30 attempts.
```

**The database was up and answering the whole time.** The reader is sent to the database, the network and the DSN — none of which is the fault.

## Where

`Blockchain/Dev/scripts/run-migrations.sh`, the wait loop (`MAX_RETRIES=30`, `RETRY_INTERVAL=2`):

```sh
if pg_isready -h "$PG_HOST" -p "$PG_PORT" -q 2>/dev/null; then
```

`-q` silences `pg_isready`'s own output and `2>/dev/null` silences the shell's *"command not found"*. Between them, a missing binary and an unreachable server are **byte-indistinguishable** from the script's output — and they have opposite fixes.

## Measured, 2026-09-25

On a disposable `postgres:15-alpine` instance on `127.0.0.1:55432`, built from `docker/init`:

* Host run: **exit 2**, `ERROR: PostgreSQL did not become ready after 30 attempts` (60 s of retries).
* **Control, same instant, same instance:** `pg_isready -U secuura -d secuura` **inside** the container returns `accepting connections`, **rc 0**. So the server was ready throughout.
* `which pg_isready` on the host: **absent**. `which psql`: **absent**.
* **Positive control that the script is otherwise fine:** copying the same script and `migrations/` into the container (where both binaries exist) and running it there gives `applied=49, failed=0`, rc 0, against that same database. **Only the host tooling differed.**

## Why it matters more than a cosmetic message

1. **It costs 60 seconds before it lies.** The loop cannot succeed, but it still burns all 30 attempts.
2. **The failure is attributed to the wrong system.** This is the class the repo already takes seriously — a verdict composed separately from the work (`STANDING_LINES.md`, *"a verdict line is a claim about what ran"*). Here the verdict names a component that was never consulted.
3. **It is a first-run experience.** A developer or a fresh VM without the Postgres client tools meets this before anything else, and the message points away from the fix.

## NOT claimed

* **Not a product defect and nothing shipped on it.** The script exits **2**, so it fails loudly; this is about *which* cause it names, not about a silent pass. It is **not** the same defect as KS-808 (`applied=N` counting skips / exit 0 on failure) — that is the summary lying about success, this is the probe lying about the cause.
* Whether any deployed environment or image lacks `pg_isready` was **not** measured. In the compose `migrations` service the binary is present, so this is reached by host/dev runs and by any image that drops the client tools.

## Fix shapes, not chosen here

1. **Check the binary exists first** and say so: `command -v pg_isready >/dev/null || { echo "ERROR: pg_isready is not installed — install the postgres client tools"; exit 4; }`. A distinct exit code keeps the two causes distinguishable to callers.
2. **Keep the stderr on the last attempt** so the real message survives into the log.
3. Fall back to a `psql -c 'SELECT 1'` probe (the script already depends on `psql`), which at least fails with a message about the thing it could not do.

(1) is the smallest and removes the misattribution entirely.

## Board search before filing (team Secuura-PK, 1,285 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `pg_isready` -> 3 total / 2 open: **KS-1161** and KS-485. **KS-1161 is NOT a duplicate** — read in full, it is the redis healthcheck exposing `REDIS_PASSWORD` via `docker inspect`.
* `run-migrations.sh` -> 13 total / 7 open (KS-1054, KS-1031, KS-980, KS-808, KS-772, KS-601, KS-485). The two nearest were read in full: **KS-1054** is fail-open RLS from migration *ordering* on boot 1; **KS-808** is the runner's `applied=N` summary counting skips. Neither owns the readiness probe.
* `did not become ready` -> **0**. `command not found` -> 8 total / 1 open (KS-1137, a different script).
* Controls that fire: `KS-808` -> 4; `run-shell-suites.sh` -> 28 / 13 open. So the search discriminates.

## Provenance

Found on 2026-09-25 while provisioning a disposable PostgreSQL for KS-980's red proof (PR #1242), on the coordinator's instruction to file it rather than carry it. Tier 3 when picked up; not this round.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1296-pgreadymissing-a-missing-pg-isready-names-itself-not-the-5a76fe2f70cd">Review in Linear</a></p>

