## What and why

**TIER 1.** This is `Blockchain/Dev/scripts/run-shell-suites.sh` — the runner **preflight leg 14
executes for every seat**, which is why it was built last in the round.

Four defects, one file, one new cell block. One commit, because splitting them would leave
intermediate commits whose own test file is red, and KS-1089 asks for all of it proved by **one run**
of `scripts/__tests__/run_shell_suites.test.sh`.

- **KS-1127** — a suite that cannot run its cells prints `SKIP — …` and exits 0. Scored by exit code
  alone it read identically to one that ran every cell, and so did the verdict leg 14 prints and PR
  Test Evidence quotes. Now tallied separately.
- **KS-1089 QA-8** — `--list` on a tree with zero reached suites **died** on bash 3.2: `"${reached[@]}"`
  on an empty array under `set -u` raises "unbound variable", so the `exit 0` never ran.
- **KS-1089 QA-7** — one headline served every cause; with git absent from PATH the output was
  identical to the empty-list case and nothing said git was missing. Three causes, three headlines.
- **KS-1135** — tsx binds its IPC socket at `$TMPDIR/tsx-<uid>/<pid>.pipe` and macOS refuses a
  `sun_path` over ~104 bytes. Six suites went red for the **length of a path**, with nothing saying so.

## The tier is grounded in a measurement, not in caution

- `git grep -l -F 'shell suites:'` at develop `6ab9d5021e96` returns **one file — the runner itself.**
  Nothing parses the verdict line.
- Leg 14 (`scripts/preflight/preflight.sh:643`) consumes only the **exit status**:
  `if ! env "${env_clear[@]}" bash scripts/run-shell-suites.sh; then`.

So adding a `skipped=` field breaks **no consumer**. Tier 1 is about *when* this lands — mid-round,
under every seat's pushes — not about an unmeasured parse risk.

## RED-PROOF — the same test file against both runners via `RUNNER_SH`

| runner | result |
|---|---|
| base `6ab9d5021e96` | **41 passed, 8 failed** |
| this head `6320a61d8` | **49 passed, 0 failed** |

All eight new defect cells red at base and green here. **The controls hold at BOTH ends, which is what
makes them controls:** `--list` with one suite still prints exactly one line; the "git printed nothing"
headline is unchanged and passes at base too; a short `TMPDIR` emits no note; a tree with nothing to
skip reads `0 skipped` and prints no `SKIPPED:` block; a **silent** exit-0 suite is still a pass; and
the caller's `TMPDIR` comes back (184 chars in, 184 out).

### KS-1127, on a four-suite fixture — a real pass, a `SKIP —` + exit 0, a real failure, a silent exit 0

```
base    shell suites: 3 passed, 1 failed (of 4)
head    shell suites: 2 passed, 1 failed, 1 skipped (of 4)
        SKIPPED: …/t1127-skip.test.sh
```

The **silent** exit-0 suite stays in `passed` at both ends. That is the cell that stops "skipped" being
applied to every zero exit.

### KS-1089 QA-8, measured on `/bin/bash` 3.2.57 before choosing the form

```
printf '%s\n' "${reached[@]}"                 unbound variable, 0 bytes, the next line never runs
printf '%s\n' ${reached[@]+"${reached[@]}"}    rc 0, but writes ONE byte — a bare newline
guarded on ${#reached[@]}                      rc 0, 0 bytes
```

Base on an empty tree: **rc 1, 55 bytes, `line 72: reached[@]: unbound variable`** — the ticket's own
line number. Head: **rc 0, 0 bytes.** The regression cell measures **bytes**, because a `$(…)` capture
reads empty for the guarded form *and* for the `+alternate` form and cannot discriminate. The
`+alternate` form is what `:92` uses and is harmless there — its output goes into a `$(…)` which strips
the newline. At `:72` it goes to a reader.

### KS-1135

A 218-character `TMPDIR` gives base **0** lines naming the cause. At this head the cause is named —
**twice**, before the run and beside the verdict, because a note at the top is buried under 58 suites of
output; and a short `TMPDIR` names nothing.

## One design choice worth flagging: tee, not capture

Scoring the skip needs the suite's output. A `$(…)` capture would have cost the **live stream** of a
58-suite run — the operator would see nothing until each suite finished. So the suite is `tee`'d and the
status read from `PIPESTATUS[0]`, verified on bash 3.2 under `set -uo pipefail` (`rc0=3 rc1=0`).

## Two of my own mistakes, both caught by these cells

1. **The QA-7 git-absent cell would have passed on any broken PATH.** It runs a PATH holding only the
   tools the runner needs with git omitted — which alone proves nothing. It is now paired with a CONTROL
   running the **same** minimal PATH **with git symlinked in**, which must get past the check.
2. **The KS-1135 cell expected the note once and found two.** The second print is deliberate; the
   expectation was wrong. The cell now pins **2** and says why.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/run-shell-suites.sh` and
`Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh`. No service, no route, no spec, no runtime
config, no migration, no `package.json`, no lockfile, nothing under `scripts/audit/` or
`scripts/preflight/`, nothing in `packages/shared`.

**Ran:** the base-vs-head matrix above via `RUNNER_SH`; the four-suite skip fixture; the empty-tree
`--list` byte measurement; the 218-character `TMPDIR` run and its short-`TMPDIR` control;
`run-shell-suites.sh` itself; `check-script-portability.sh`; `deps-present.sh`. Ratios in the READY.

**NOT run:** preflight **legs 3, 4 and 8** — they need the local platform stack on `:6882`, which by
Wednesday's coordination of 2026-09-25T02:44:51Z comes up once at the batch QA gate and is not started
mid-round. **This PR changes a shell runner and its own suite — no route, no served spec, no runtime
config** — so those legs have no subject here. Not "gate green": 12 of 15 legs run, three with nothing
to test.

**Out of lane, declared:** KS-1127's second bullet asks that **leg 14 quote that line**. That is a
`scripts/preflight/` edit, which is not this lane. The ticket stays open for it.

**Honest limit on this round's evidence:** there is **no live skip on this machine.** A real
PostgreSQL 15.14 is on PATH, so `ks949_main_seed_idempotence.test.sh` runs its 48-migration shape in
full and every run of mine reads `0 skipped`. The tally is therefore proved by a **purpose-built
fixture**, not by a real skip — quoting this round's runs as evidence of one would be quoting a run that
had none. Likewise every run of mine used a 4-character `TMPDIR` deliberately, which is avoidance, not
evidence.

**Migrations + config:** none.

Refs KS-1127
Refs KS-1089
Refs KS-1135

🤖 Generated with [Claude Code](https://claude.com/claude-code)
