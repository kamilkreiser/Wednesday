#1258 KS-1296 PGREADYMISSING: a missing pg_isready names itself, not the database
head ff90fbf9d7e351104404e3eaad505a673e656c1e

## BLUF

`run-migrations.sh`'s readiness probe is `pg_isready … -q 2>/dev/null`. `-q` silences pg_isready's own output and `2>/dev/null` silences the shell's *"command not found"* — so **a missing binary and an unreachable server are byte-indistinguishable from the script's output, and they have opposite fixes.** With the binary absent the loop burned all 30 attempts against a command that never executed and then reported

```
ERROR: PostgreSQL did not become ready after 30 attempts.
```

sending the reader to the database, the network and the DSN, none of which was the fault. **Measured: 61 seconds before it says that.**

Fix shape 1 from the ticket — the smallest that removes the misattribution: check the binary before announcing a wait that cannot be performed, name the missing tool, **say the database has not been contacted**, and exit with a distinct code.

## Exit 4 is free, and now documented

Measured: the script used **1, 2 and 3** only (`:33`, `:63`, `:166`), and its own exit-code table at `:22-26` listed exactly those three. The table gains a fourth row — an undocumented exit code is the next reader's puzzle.

**The caller that reads the status** is the compose `migrations` service, via `service_completed_successfully`, which treats every non-zero alike. So for that caller the *message* is what a human acts on, which is why the message says the database is not implicated.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/run-migrations.sh` (+24) and `Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh` (+79 / −2). 2 files.

**Ran — the in-hook gate on this push:**
- `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` · `legs 3 4 8 — local stack not up`. **Quoted as INCOMPLETE, not as a pass.**
- **`run_migrations_failure_exit_code` 7 passed, 0 failed** — the declared figure (5 before).
- `pre_push_hook_base` **28/0** · `pre_push_hook_base_fixture_guard` **6/0** · `run_shell_suites` **49/0** · **shell suites 60 passed, 0 failed, 0 skipped (of 60)** — all unchanged by this PR.

**Ran — RED / GREEN:**
- **GREEN 7/0.**
- **RED against the base script** (via `RUN_MIGRATIONS_SH`): **6 passed, 1 failed** — exactly the new cell, and **the run took 61 s**, which measures this ticket's own claim that it costs a minute before it lies. Only that one cell moved between the two runs.

**Two cells, and `EXPECTED_CELLS` 4 → 6** so the suite's own completeness guard still means something.
- The new cell carries **its own precondition**: on a box that *has* `pg_isready` in `/usr/bin` it cannot test a missing binary, and it says so rather than passing quietly.
- **The control is the one that matters, and it passes on both sides:** a `pg_isready` that is PRESENT but always refuses must still reach exit 2 and still blame the database, because there the database *is* the right thing to name. Without it the new guard could have swallowed the real case.
- That control runs against a **retry-shortened copy** so it costs ~0 s instead of 60, and **the substitution is verified applied** — a sed that silently matched nothing would make the cell assert about the unmodified script and take a minute doing it.

**NOT run / NOT covered:**
- **Legs 3, 4, 8 did not run** (no local stack). 12/15.
- **No real PostgreSQL was involved anywhere.** The red arm needs none (`pg_isready` is genuinely absent from this host) and the control uses a stub. Nothing was measured against a live server.
- **Whether any deployed image lacks `pg_isready` was not measured** — the ticket says the same. In the compose `migrations` service the binary is present, so this path is reached by host/dev runs and by any image that drops the client tools.
- **No measurement on Linux.** macOS `/bin/bash` 3.2.57 only.

**Migrations + config:** none. This changes a migration *runner*'s diagnostics; it applies no migration, and no `package.json`, lockfile or workflow is touched.

`Refs KS-1296`; does not close it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

