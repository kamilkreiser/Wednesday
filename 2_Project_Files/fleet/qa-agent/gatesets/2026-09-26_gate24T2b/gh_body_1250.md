#1250 KS-1302 + KS-1303 RSSTRAP: trap the runner's short TMPDIR, and drop the output pipe
head c78f4093fb531bceb94a8e9defb59350d8c60b73

## BLUF

Two findings recorded at #1234's merge (`e68e2f0e837d`), both in `Blockchain/Dev/scripts/run-shell-suites.sh` — the runner that gates every push. Fixed together because they are **one file and one test pass** (Kam, 2026-09-07: the unit is the test pass).

- **KS-1302** — the KS-1135 short-TMPDIR substitution created `/tmp/rss.XXXXXX` and never removed it. A `trap … EXIT INT TERM` now removes it.
- **KS-1303** — suite output was piped through `tee`, and `tee` cannot see end-of-file while any process still holds the write end of the pipe. A suite leaving a background child therefore delayed the **whole runner** until that child exited. The pipe is gone.

## KS-1302: a correction to the ticket's premise, because it changes the fix

The ticket asks the trap to cover *"the rc 2 abort path"*. Measured at `6e2a00bfe`:

- `run-shell-suites.sh` has **no `exit 2` after the `mktemp -d` at `:255`** — its only `exit 2` is the usage error at `:58`, long before the directory is created.
- It had **no `trap` at all** (`grep -c '^trap ' → 0`).
- A failing **suite's** rc 2 is scored as a `fail` and becomes the runner's own **`exit 1`** at `:299`.

So the abort path to cover is that `exit 1`, plus the clean exit, plus a `^C` or `kill` mid-run that the explicit TMPDIR restore at `:286-288` never reaches. Hence `EXIT INT TERM`.

**The removal is guarded twice over**, because a cleanup that can be pointed elsewhere is a hazard, not a cleanup: `${rss_short_tmpdir:?}` refuses an empty expansion, and a `case` refuses any path that is not the `/tmp/rss.XXXXXX` this process made itself.

**A number the ticket explicitly declined to claim** (*"no measurement of how many have accumulated on any machine"*): **16** empty `/tmp/rss.*` directories on this dev box, spanning **14:21Z → 23:29Z on 2026-09-25** — roughly one per run.

## KS-1303: what changed, and the trade stated rather than hidden

```diff
-  bash "$REPO_ROOT/$rel" 2>&1 | tee "$rss_suite_log"
-  rss_rc=${PIPESTATUS[0]}
+  bash "$REPO_ROOT/$rel" > "$rss_suite_log" 2>&1
+  rss_rc=$?
+  cat "$rss_suite_log"
```

No pipe exists, so no descendant can hold one open. Two things improve with it: `rss_rc` is the suite's **own** status read directly rather than through `${PIPESTATUS[0]}`, and the skip-detection `grep` is untouched because it always read the file, never the stream.

**The trade:** a suite's output now appears when that suite finishes instead of line by line within it. KS-1127 chose `tee` so a 58-suite run showed progress rather than nothing until the end, and **that intent is preserved at the granularity that matters** — `echo "=== $rel ==="` at `:263` already prints **before** the suite runs, so the operator always sees which suite is currently going. This PR does not move that line, and the patch asserts it mechanically (header line number < run line number). Chosen over the bounded-wait alternative because it removes the mechanism instead of instrumenting it.

## Six cells, and why none is padding

Two are preconditions and one is a control:

| # | cell | why it cannot be dropped |
|---|---|---|
| 1 | **PRECONDITION** the substitution fired and the runner named its directory | this host's `TMPDIR` is 49 chars, under the runner's 80-char threshold, so a run that does not force a long TMPDIR creates no directory at all and cell 2 would pass against a runner that removes nothing |
| 2 | after a CLEAN run the TMPDIR is gone | the ticket's ask |
| 3 | **PRECONDITION** the failing run really exited non-zero | without it, cell 4 is cell 2 again under another name |
| 4 | after a FAILING run the TMPDIR is gone too | the abort path |
| 5 | a forking suite does not hold the runner (< 6 s) | KS-1303's ask |
| 6 | **CONTROL** the forking suite still RAN and PASSED | "the runner was fast" is otherwise also satisfied by a runner that skipped or crashed before it |

The cells read the `/tmp/rss.*` path **out of the runner's own note**, never a glob — a glob would also match the 16 already on the box and another seat's concurrent run, which is the difference between a cell and a coincidence.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/run-shell-suites.sh` (+54 / −5) and `Blockchain/Dev/scripts/__tests__/run_shell_suites.test.sh` (+70). 2 files, +119 / −5. No other file.

**Ran — the in-hook gate on this push (this is a `Blockchain/Dev` change, so the preflight DID run):**
- `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` · `legs 3 4 8 — local stack not up`. **Quoted as INCOMPLETE, not as a pass** — the tool prints "This is NOT a pass" and that is respected here.
- `pre_push_hook_base.test.sh` — **28 passed, 0 failed**
- `pre_push_hook_base_fixture_guard.test.sh` — **6 passed, 0 failed**
- `run_shell_suites.test.sh` — **55 passed, 0 failed** (49 before this PR; +6)
- **`shell suites: 60 passed, 0 failed, 0 skipped (of 60)`** — produced by the patched runner itself
- 13 code guards OK · production-guard coverage **23 / 23** services · 7 portability rules across 102 shell scripts

**Ran — red/green on the suite, same suite pointed at each runner via `RUNNER_SH`:**
- **GREEN**, patched runner: `run_shell_suites: 55 passed, 0 failed`, rc 0.
- **RED**, pre-patch runner (`7912bb9d…`): **52 passed, 3 failed**, rc 1 — cells 2, 4 and 5, **one red arm per conjunct**.
- The three preconditions/controls stay green on both sides, which is what a precondition should do.
- **The other 49 pre-existing cells are byte-identical between the two runs** (diffed), so this change perturbs nothing else.

**Ran — the static facts, comment lines excluded from every predicate** (they matched my own explanatory comments otherwise): `| tee` in code **0**, `PIPESTATUS` in code **0**, `trap … EXIT INT TERM` **1**, guarded `rm -rf "${rss_short_tmpdir:?}"` **1**, unguarded form **0**. Control: the same predicates on the base read tee **1**, PIPESTATUS **1**, trap **0**. `bash -n` rc 0.

**A mistake inside this PR's own red proof, disclosed because it is the interesting part:** my first KS-1303 fixture was `sleep 15 >/dev/null 2>&1 &`. Redirecting the child's output *for tidiness* removed its grip on the pipe — the entire mechanism under test — and **the cell passed against the unfixed runner.** It is now `sleep 15 &`, and the reason is written into the suite beside the fixture so the next reader does not tidy it back.

**NOT run / NOT covered:**
- **Legs 3, 4 and 8 did not run** — the local stack is not up. `12/15`.
- **No survey of the 60 suites for existing background children.** KS-1303 says no suite is known to do this today and this PR does not change that; the fix removes the mechanism, it does not audit for instances.
- **The 16 pre-existing `/tmp/rss.*` directories are NOT cleaned up by this PR.** It stops new ones; it does not remove old ones. Deleting them is a housekeeping action nobody has asked for, and "never delete" applies.
- **No measurement on Linux.** Everything here is macOS `/bin/bash` 3.2.57.
- The `INT`/`TERM` arms of the trap are **not** exercised by a cell — only `EXIT` (clean and failing) is. Sending a signal to the runner mid-run from inside its own test suite is a fixture I did not judge worth the flakiness; the trap lists them and that is unverified.

**Migrations + config:** none. No migration, no `package.json`, no lockfile, no workflow, no config file.

## Scope

`Refs KS-1302`, `Refs KS-1303` — both this PR's own keys. Neither is closed by this merge. `ks1135` and `ks1127` are the parents and are written un-hyphenated here so no attachment lands on them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

