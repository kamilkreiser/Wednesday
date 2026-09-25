#1244 KS-1111 ECHOMASK: mask every interpretation of an argument behind a lookalike env flag
head 146b620fda53f008b3384334a474b06a16235af3

## What this changes

`formatDockerArgsForLog`'s two-argument branch returned `maskEnvAssignment(arg)` and never tried the
one-argument forms. `-e`, `-one` and `-qe` are also legal **values** of docker's `--label`, `-a` and `-u`, so
when the previous token only *looked* like an env flag, the real parser read this argument as a flag of its
own while the mask read it as a bare `NAME=VALUE` — taking the name to be `--env`, `-e` or `-eKEY`. The branch
now falls through to the same one-argument masks (`maskOneArgumentForms`, extracted so both paths mask by
construction rather than by two copies staying in step).

## Measured: the leak is narrower than the ticket's table, and the difference matters

`SECRET_ENV_NAME` is `/PASSWORD|PASSWD|SECRET|TOKEN|MNEMONIC|(?:^|_)KEY$/i` — **unanchored** for the first
five, **anchored** only for `KEY`. On the broken path the whole glued token was read as the name, so:

| argument behind a lookalike flag | name the mask read | before |
|---|---|---|
| `--env=ADMIN_PASSWORD=v` | `--env` | **leaked** |
| `-e=DB_PASSWORD=v` | `-e` | **leaked** |
| `-eKEY=v` | `-eKEY` (anchored clause fails) | **leaked** |
| `-eADMIN_PASSWORD=v` | `-eADMIN_PASSWORD` (PASSWORD substring) | masked **by accident** |

The ticket's L01/L04/L05/L07 rows use the placeholder name `NAME`, which is not a secret name at all, so
"clear" there is correct behaviour rather than a leak. The rows added here use the names that **actually**
leak, and the accident is pinned in its own cell so a future reader cannot take "this shape was masked" as
evidence the branch was correct — and so narrowing `SECRET_ENV_NAME` later cannot quietly turn it into a leak.

## Test Evidence

**Touched:** `systemTest/performance/runner/k6_docker.ts` and
`systemTest/performance/tests/unit/runner/k6DockerRedaction.test.ts`. Nothing else, no `package.json`, no
lockfile, nothing outside `systemTest/performance/`.

**Ran** (all by the author, on this head; node v24.7.0, vitest 4.1.11, macOS):

- `npm run test:unit` — **63 files / 1096 passed / 0 failed**, rc 0. Base at develop `6e2a00bfe`, measured in
  this worktree before any edit: **63 / 1089 / 0**. +7 cells, no pre-existing red on either side.
- `npm run lint` — rc 0, running **both** tsconfigs (`tsconfig.json` and `tsconfig.node.json`) plus eslint.
- `npm run format:check` — rc 0.
- **Red-proof before the fix:** the three QA-961-1 rows (L02, L03, L08) were **red** with the rows added and
  the fix absent; the QA-961-2 rows were green, because they pin behaviour that was already correct and their
  red proof is the tamper below.
- **Tamper matrix, one arm per conjunct** (`tamper1111.sh`; restores sha256-asserted, never `git checkout`):

| arm | what it flips | reds |
|---|---|---|
| T-1 | the QA-961-1 fallthrough | L02, L03, L08 — exactly the three |
| T-2 | two-argument cluster → exact `-e` (gate Q1) | `-Pe` row + the existing `R_cl2` |
| T-3 | attached cluster → bare `-e` (gate Q2) | `-diteN=V` row + `R_cla`, `R_cleq` |
| T-4 | drop the `SECRET_ENV_NAME` test entirely | the two non-secret readability cells |
| T-5 | drop `PASSWORD` from the name pattern | the **accident** cell (+5 others) |
| T-6 | treat every preceding `-flag` as an env flag | the `-l` non-env boundary cell — **only that one** |

T-6 exists because T-4 did **not** reach the `-l` cell: T-4 tampers `maskEnvAssignment`, which is never
*called* for a value behind `-l`. The declared boundary lives in the **routing**, so the arm that tests it has
to widen the routing. That is written into the script so the next reader is not misled by the T-4 label.

**Which gate ran, exactly:** this is a repo-root `systemTest/` change and `.githooks/pre-push` gates its
15-leg preflight on `^Blockchain/Dev/`. **The preflight did not run** — the push took 7 s and printed only
`[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP count was **not executed** on this
branch and nothing here quotes it. Everything above was run by hand.

**NOT run / NOT covered:**

- **The masked NAME SET is unchanged.** KS-1098's QA-958-2 is Peter's decision and is deliberately untouched.
- No live docker or k6 run, no container, no environment. **Nothing deployed.** The gate's own measurements
  against docker CLI 28.4.0 and `k6 archive` v1.6.1 are quoted as its findings, not re-measured here — there
  is no docker run in this lane.
- **QA-961-3 is documented, not fixed.** A token docker or k6 *rejects* is printed verbatim by the tool's own
  error output through `stdio: 'inherit'`, which bypasses this mask and the run-log tee. It now appears in the
  does-NOT-cover list. The structural fix is O-1 (bare `-e NAME` plus a `spawnSync` `env`), which is a change
  to how the runner passes secrets and is not in this pass.
- `-l` carrying a secret-named value still prints in clear. That is the declared boundary, now pinned; whether
  to widen the mask over labels is the design question KS-1098 leaves open, not something decided here.
- `npm run knip` and `npm audit` not run (audit reaches the network).
- No caller builds these argvs today: `cli.ts:221` hard-codes `extraFlags: []` and `buildEnvFlags()` emits only
  `-e NAME=VALUE` pairs. The defect is latent, and the cells reach it through `extraFlags`.

**Migrations + config:** none.

Refs KS-1111

