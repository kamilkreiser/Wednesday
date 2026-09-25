#1257 KS-1201 STUBPARENT: start_stub runs in the parent, so the trap has a pid to kill
head d1db0d41ac52359c231cd22abf11124204645d97

## BLUF

`start_stub` set `STUB_PID=$!`, but every call site was `port="$(start_stub N)"` — **a command substitution, which is a subshell.** The assignment happened in a shell that exited immediately, the parent's `STUB_PID` stayed empty, and neither the explicit `stop_stub` after each cell nor the EXIT trap had anything to kill. **Every run leaked all four `node login_stub.mjs` listeners.**

The port now comes back in `STUB_PORT` instead of on stdout, which is what lets the call be an ordinary command in the parent shell. All four call sites become `start_stub N || exit 2` then `port="$STUB_PORT"`.

## Measured, not inherited

- **The pre-fix suite run in place leaks exactly 4** — the ticket's number, reproduced.
- The ticket's own census: 84 orphans in 21 groups of 4 over ~10 hours of pushes.
- **My own baseline run of the platform suites today leaked 8** from this project's worktrees — two groups of 4, one from the standalone run and one from the in-runner run, all reparented to ppid 1.
- **And a natural confirmation in this PR's own push:** the three sibling pushes in this round each reaped **4** leaked stubs from their worktrees; **this branch's push reaped 0**, because the fix is in it.

## Test Evidence

**Touched:** `systemTest/__tests__/bootstrap_login_diagnosis.test.sh` (1 file, +64 / −8).

**⚠ NAME THE GATE: 0 of 15 preflight legs ran, by design.** `.githooks/pre-push:76` gates the preflight on a `^Blockchain/Dev/` path and this PR touches only `systemTest/__tests__/`, so the hook takes its early return. **So `pre_push_hook_base` 28/0, the fixture guard 6/0 and the shell suites 60/60 did NOT execute on this push and are not quoted as its evidence.** The KS-989 formatting gate does run before that early return, but it selects packages by `^systemTest/<pkg>/` and only `akto`, `api-explorer`, `performance` and `playwright` declare `format:check` — `systemTest/__tests__/` has no `package.json`, so it selected nothing and took its own `exit 0`.

**Ran by hand instead:**
- **GREEN: `bootstrap_login_diagnosis.test.sh` 18 passed, 0 failed** (16 before), and **0 listeners left behind**.
- **BASE, run in place: 16 passed, 0 failed, and 4 listeners leaked.**
- **RED — one call site put back inside `$( )`: 14 passed, 4 failed.** The regression cell fails and the control still fires. The other three failures are B1's banner assertions, which have an empty `port` to talk to — the same single defect, not separate ones.
- `bash -n` rc 0. Command substitutions remaining in *code*: **0** (the one textual match left is the comment explaining the old form).

**The control comes FIRST inside the cell, deliberately.** "0 survived" is exactly the shape of zero that cannot fail, so a stub is started on purpose and the count must read non-zero before the absence below means anything.

**Selection is by the stub's absolute path**, never the basename and never a bare `pgrep -f login_stub` — either of which would also match another seat's live stubs on a shared machine and, worse, this script's own command line.

**NOT run / NOT covered:**
- **No preflight leg ran.** 0/15. See above.
- **The 4 pre-existing orphans from the base run were reaped by hand, not by the fix** — the fix prevents new ones; it does not clean up old ones.
- **The cell counts LISTENERS, not processes.** A stub that started and died before binding, or one that leaked without a listening socket, would not be counted.
- **No measurement on Linux.** macOS only. `lsof`-based counting is not portable and this cell would need revisiting there.

**Migrations + config:** none. Test-harness only.

`Refs KS-1201`; does not close it.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

