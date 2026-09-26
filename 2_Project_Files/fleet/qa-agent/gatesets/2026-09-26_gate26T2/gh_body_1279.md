#1279 KS-1306: assert rolsuper alongside rolbypassrls on both DSNs
head dabde931df5e02e45272b70f2fe75fb3dab6ed38

## What

The KS-980 D1 cell asserted `rolbypassrls` alone. A Postgres **SUPERUSER bypasses RLS regardless of `rolbypassrls`**, so a role with `rolsuper = true, rolbypassrls = false` satisfied the cell while being exactly the thing the cell reads as *"a role RLS constrains"*.

`rolsuper` is now asserted alongside it — as a **value** on the `platform_bypass` path, where `false` is the property under test, and as a **type** on the `bypassrls` path, where either setting is a legitimate way to provision an admin role. Pinning a value there would refuse a valid instance; asserting the type still fails if the column stops being read, which is the failure mode that matters.

## The blind spot is measured, not argued — and the ticket's own framing is confirmed

On a disposable Postgres built the documented way (`docker/init` + `scripts/run-migrations.sh`; **49 migrations applied / 0 failed**, with the tracker table read **independently** of the runner's own `Summary` line, and `048` present), I created a role with `SUPERUSER NOBYPASSRLS` and pointed the `platform_bypass` path at it. Role shape asserted before use: `s_b29_super_nobypass super=true bypassrls=false`.

| arm | result |
|---|---|
| **PRE-EDIT `D1` cell**, blind role | **PASSES** — the blind spot is real and reachable, not theoretical |
| **PRE-EDIT `D2`** GUC cell, same role | **FAILS** — the consequence was caught by a *different* cell, exactly as this ticket states |
| **PATCHED `D1`**, same role | **REDS**, and the failure names `rolsuper` |
| **PATCHED `D1`**, the honest app role | **passes, 6/6** — the new conjunct is not a blanket refusal |

The first version of that first arm asserted the pre-edit **suite** passed, and it failed — because a superuser also breaks `D2`. The claim is about `D1`, so the instrument had to read `D1`; a suite-level exit code cannot. Verdicts come from `--json` `fullName`.

Also measured on this instance, and it is why the ticket matters here rather than in the abstract: the admin role `docker/init` provisions is `rolbypassrls = true, **rolsuper = true**`.

## The widening, recorded as one

**Before this, the suite performed no host, port or disposability check at all.** It required both DSNs to be *set* (throwing at the two gates) and would otherwise connect to a shared or remote Postgres without complaint — **and it INSERTs rows**. The #1262 precedent is that a test which writes to a database must be unable to reach a shared one.

It now refuses a **non-loopback host** and refuses the **shared-stack ports**. The compose stack port is **READ from `docker-compose.yml`'s own default** (`POSTGRES_EXTERNAL_PORT:-6432`, proven to match at `6432`) rather than pasted, so the guard cannot drift away from the stack it protects. `5432` is refused as Postgres's own default. If the compose file cannot be read, `6432` is still refused — it fails closed.

**A seat's port RANGE was deliberately not used, unlike #1262.** That cell installs a **trigger**, so its range is part of a DDL containment argument. This suite writes only INSERTs, and a hardcoded range would refuse every runner outside it — a later formal test pass, or a gate on another seat's ports. Loopback plus shared-port refusal are the two properties that actually protect the row writes, and neither is brittle. **If the range is wanted anyway, say so and it is a one-line addition** — I did not want to narrow who can run this suite on my own judgement.

## Test Evidence

**Touched:** `services/originate/src/__tests__/ks597-issuer-organization-id.integration.test.ts` (test-only).

**Base:** this worktree **contains** develop `d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9`.

| arm | result |
|---|---|
| `ks597` integration BARE, `--config jest.integration.config.js --runInBand` | **6 passed / 6**, rc 0 |
| `ks597` integration PATCHED, same command | **6 passed / 6**, rc 0 |
| originate unit, `npx jest --runInBand` | **878 passed / 878, 74 suites**, rc 0 |
| `packages/shared`, `npx vitest run` | **941 passed / 941, 48 files**, rc 0 |
| `tsc --noEmit` in `services/originate` | rc 0 |

**`No tests found` matched 0 times** in the integration runs, checked explicitly — a `No tests found` exit 1 is a zero-executed run, not a pass, and this was neither.

**Eight arms, 0 failed**, counted from a tally file rather than shell variables: the four in the table above, plus the DSN guard — a remote host refused with the host named; port `6432` refused (and `6432` proven to have been *read* from `docker-compose.yml`); port `5432` refused; and a **control** that my own `127.0.0.1:55412` is accepted, so the guard discriminates rather than refusing every port.

**My disposable Postgres:** container `s-b29-pg-ks1306`, image `postgres:15-alpine` **read from `docker-compose.yml`** with the script refusing any `:latest`, bound to `127.0.0.1:55412` only, anonymous volume created with `-v` so it can be proven gone, password generated fresh and **asserted different from the compose default read from the file** (so no credential literal enters the tree). Port proven free immediately before binding, against a control showing 3 listeners on `5432`. **55419 was read and left alone** — it is reserved for the #1262 gate.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 NOT run** (local stack not up): `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)`. No spec moves, so no LEG-8-PORT reading.
- The `SUPERUSER NOBYPASSRLS` role exists only in my throwaway instance and is **not** created by the committed cell — the cell writes no DDL, which is why the #1262 DDL-refusal rule does not bind it.
- The guard checks host and port. It does **not** verify the database is genuinely disposable (empty, or freshly migrated); that is not decidable from a DSN, and the docblock says so rather than implying a stronger property.

Refs KS-1306

🤖 Generated with [Claude Code](https://claude.com/claude-code)

