Refs KS-1330

https://linear.app/secuura/issue/KS-1330

`run-shell-suites.sh` had no signal handling at all — `trap` appeared 0 times in it. A ^C or a kill
mid-run left the suite then in flight alive and left the run's own `/tmp/rss.*` directory behind.
The round-2 work that fixes this was written for #1250, which took a NO GO at its round-2 cap and
ships nothing. #1250 stays open and is not touched here; its two blobs are re-landed unchanged and
then corrected:

| path | blob re-landed |
|---|---|
| `Blockchain/Dev/scripts/run-shell-suites.sh` | `8eef1c4877b30f7dfeb485dbb1955a53a6122fd5` |
| `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` | `9c4a87f0a97c462ae59e98d9f35aeab8fba89f27` |

### Item 1 — an arm that could not come out either way

The SIGINT-to-pid cell was skipped on "RULE 2" **unconditionally**, so it reported UNREACHABLE on
every run, in every environment. Rule 2 as the comment stated it — bash ignores SIGINT in a
background job "regardless of the parent's disposition" — holds only while job control is off, and
`signal_run` enables it at its `set -m`. Measured both ways, `/bin/bash 3.2.57(1)-release
arm64-apple-darwin26`, one host, backgrounding a separate `bash` exactly as `signal_run` does:

| shape | handler | rc |
|---|---|---|
| `set +m`, `kill -INT <pid>` | never fired | **0** |
| `set -m`, `kill -INT <pid>` | fired | **130** |
| `set -m`, `kill -INT -<pid>` | fired | **130** |

The arm is now gated on RULE 1 via `sig_installable` alone, like the group arm beside it, and the
rules and the matrix say rule 2 is conditional. A note is added that an empty `trap -p INT` means
the **default** disposition, not an ignored one — bash prints `trap -- '' INT` for ignored — because
the inverse reading is easy to make and `sig_installable` is correct precisely because it installs a
trap before looking for it.

### Item 2 — a kill that is honoured and a kill that is waited out read alike

The cells asserted a non-zero rc, no further suite, no verdict line and a removed directory. A
runner that ignored the signal and died only when the fixture's own `sleep` ended satisfies every
one of those. `signal_run` now returns the kill-to-exit gap and it is asserted as **its own cell**,
bounded at half the fixture's sleep, with that sleep lifted to a named constant so the bound is
derived from it rather than guessed. At develop's runner the new cell reports `kill_to_exit=11s`
against a 12s fixture sleep — the defect made visible.

### Item 3 — two inherited conditions, documented, not changed

Each suite is launched asynchronously and this runner never enables job control, so bash hands every
suite two dispositions a suite author would not expect. Both measured on this host, neither inferred:

- **SIGINT is ignored in the suite** — a `kill -INT` to the backgrounded child is discarded and the
  parent sees rc 0.
- **stdin is `/dev/null`** — identified by identity, not by a read returning EOF: the child's fd 0
  and `/dev/null` share inode 336 and rdev 3,2, while the same child given a real file reads inode
  171878651 rdev 0,0 and run synchronously reads inode 343324 rdev 0,0. Two controls that differ.

Neither is altered. Both were invisible, and a suite written against the opposite assumption fails
in a way that reads as a flake.

### Co-tenant coupling — measured, bounded

This runner globs every tracked `*.test.sh`, so it runs other seats' suites. develop's runner ran a
suite in a **foreground pipeline** (`| tee`, its `:268`); this one runs it **async + wait** (`:360`),
which is what changes stdin and SIGINT. Across all **67** tracked suites (existence control 67/67):

| property | count |
|---|---|
| suites using `read` as a command head | **0** |
| suites trapping INT | 10 |
| of those, also trapping TERM or EXIT | **10 of 10** |
| `ks1401_049_tenant_isolation_after_039.test.sh` (#1383): `read` head / traps INT | **0 / 0** |

So stdin at `/dev/null` reaches nothing, and the runner's own TERM to the suite still reaches the
cleanup of every suite that traps INT. Two candidates an earlier, looser pattern flagged as reading
stdin were the English word "read" inside comments; the lines were read rather than counted.

## Test Evidence

**Touched** — `Blockchain/Dev/scripts/run-shell-suites.sh`,
`Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh`. Nothing else.

**Ran** (all local, by me, `/bin/bash 3.2.57(1)-release arm64-apple-darwin26`):

- `run_shell_suites.test.sh` red-first, one test file against both runners via the harness's own
  `RUNNER_SH` override, suite in the **foreground** so SIGINT is installable:
  **develop's runner 54 passed / 7 failed · this head 61 passed / 0 failed.**
- **Tamper:** restoring the unconditional rule 2 gate returns the cell to UNREACHABLE and drops the
  total 61 → 60, so the gate is what makes the arm exist. File restored byte-identical afterwards.
- Whole-suite runner over this repo, cwd outside any repo:
  **`shell suites: 67 passed, 0 failed, 0 skipped (of 67)`**.
- `npm ci --ignore-scripts` rc 0 (985 top-level dirs) and `npm run build --workspace=packages/shared`
  rc 0, with `packages/shared/dist/index.js` asserted present at 17,746 bytes by a stat rather than
  by the exit code.

**NOT run** — the develop-side whole-runner tally at its real path. Invoked from outside the tree
develop's runner refuses with `FAIL — no shell suites found under: …`, which is that runner working
correctly rather than a figure; getting it would mean swapping a file inside the worktree, which was
deliberately not done. The per-suite 54/7 vs 61/0 plus the tamper is the evidence offered instead.
No Playwright, Schemathesis, Akto or k6 run: these two files have no runtime product surface and are
reached by none of those suites.

**Migrations + config** — none. No migration, no spec, no dependency, no lockfile, no manifest, no
`audit-baseline.json`, no `.githooks/pre-push` and no workflow file is touched. This PR adds **no new
pre-push leg**: it changes the behaviour of the runner leg 14 already invokes, and the hook itself is
unchanged.

## Documentation

**No block in either platform-k HTML doc, stated explicitly rather than skipped.** The
test-discipline skill (blob `eaf43dfd4d985bf9b0badbfc7e85561c13407e1f`) scopes §4 by *defining* the
term at `:362-:363`:

> **Every test change updates its platform's two HTML docs, in the same commit — not a follow-up.**
> "Test change" means backend unit, integration, *or* systemTest.

These are tooling suites that test the pre-push harness itself, under `Blockchain/Dev/scripts`, and
are none of those three. §4 `:417-:418` gives the route for exactly this case:

> - If a change genuinely does not affect either doc, **say so explicitly and why** — do not
>   silently skip.

No stated timing is affected either. Grepped `-i -E 'run-shell-suites|shell suites|leg 14|leg-14'`
over both HTML docs, `Blockchain/Dev/CLAUDE.md`, `systemTest/CLAUDE.md` and the skill: **0 hits**,
against a must-hit control of 70 / 82 / 16 hits for `Akto` in the same files and an inverted control
of 0 for an absent token.

## Not covered

No live sweep — these files have no runtime product surface. A PTY harness asserting a **foreground**
INT is KS 1325 and is not here. The residue items KS 1302 and KS 1303 own are not closed by this PR,
and #1250's disposition is not decided by it.

## In-hook preflight at this head

Quoted exactly as the hook printed it, including its own caveat — this is **not** a pass and is not
offered as one:

```
shell suites: 67 passed, 0 failed, 0 skipped (of 67)
OK — 13 code guards passed.
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

Twelve of fifteen legs ran and nothing failed. Legs 3, 4 and 8 were skipped because the local stack
is not up on `http://localhost:6882`; that is an environment condition, not a result, and it is
clearable by starting the stack. Leg 14 is the interesting one here: it runs **this PR's own new
runner** over all 67 tracked shell suites, inside the hook, and they come back 67/0/0 — so the
re-landed signal handling and the async launch shape are exercised against every seat's suites by
the push itself. Push `rc=0` after 412s, confirmed independently by `ls-remote` showing
`a7f5965a7b3fd94b25a26e73c250052db4be6aa0` at the branch.
