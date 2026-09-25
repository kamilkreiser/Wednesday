--- comment 5835114589 by linear[bot] at 2026-09-25T15:38:35Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1201/bootstrap-login-diagnosistestsh-leaks-its-4-login-stubs-on-every-run">KS-1201 bootstrap_login_diagnosis.test.sh leaks its 4 login stubs on every run: start_stub sets STUB_PID inside a $(...) subshell, so the EXIT trap kills nothing (84 orphans in 10 h)</a></summary>
<p>

## BLUF

`systemTest/__tests__/bootstrap_login_diagnosis.test.sh` **leaks all four of its login stubs on every run.** `start_stub` sets `STUB_PID=$!` inside the `port="$(start_stub N)"` command substitution, which is a subshell. The parent's `STUB_PID` stays empty, so neither the explicit `stop_stub` after each cell nor the EXIT trap kills anything. Each `node …/support/login_stub.mjs` then serves until killed.

Measured on one machine on 2026-09-17: **84 orphaned stub processes** LISTENING on 127.0.0.1, in 21 groups of 4, over about 10 hours of pushes. Test-harness only; no product code is involved.

## Recommendation

Not built: `systemTest/` is outside Seat A's partition, and Wednesday routes the fix. Fix shape (prose, the owner's choice): start the stub in the parent shell and read its port back from the stub's output file, so `STUB_PID` is set where `stop_stub` and the trap can see it. Add a regression cell asserting that no `login_stub.mjs` listener survives the run.

Until it lands, every run of the file leaves 4 listeners behind, including each pre-push preflight that runs it (correlation below).

## Detail

**Where** (develop `7e89318bcedbc9a35757d4298ace54a6a23020bd`; the file was last changed by `0882f7661`, KS-1167):

* `:42` `STUB_PID=""`; `:43` `stop_stub()`; `:45` `trap 'stop_stub; generated_guard_restore' EXIT`
* `:48` `start_stub()` sets `STUB_PID=$!` at `:51`
* The four call sites: `:86` `port="$(start_stub 429)" || exit 2`, `:97` (401), `:105` (503), `:109` (200). Each is followed by `stop_stub` at `:88`, `:99`, `:107` and `:111`.
* **Cause: READ, not instrumented.** A `$(…)` body runs in a subshell, so assignments inside it do not reach the parent.

**Census** (measured 2026-09-17 21:49Z, read-only):

* **Instruments:** `lsof -nP -iTCP -sTCP:LISTEN` for the listeners; per pid, `lsof -a -p <pid> -d cwd -Fn` and `ps -o pid=,ppid=,etime=,lstart=,command=`.
* **Result:** 100 LISTEN sockets, 84 of them node, from 84 distinct pids with one socket each.
  * Every one runs `node <worktree>/systemTest/__tests__/support/login_stub.mjs`, with cwd `<worktree>/Blockchain/Dev` and ppid 1 (orphaned).
  * All are on 127.0.0.1 ephemeral ports.
* **Start times:** 21 groups of 4, from 2026-09-16 21:25:36 to 2026-09-17 07:21:18 AEST. 84 = 21 runs × 4 cells.

**Correlation with pushes (not measured):** four push logs from one seat closed 3–4 minutes after a stub group started (06:04:19 → 06:07, 06:22:59 → 06:25, 06:35:09 → 06:39, 07:21:15 → 07:24 AEST). That is consistent with the in-hook pre-push preflight's shell suites running this file.

**Cleanup done 2026-09-17 22:03Z:**

* Each pid was re-identified in the same action (command, cwd, ppid 1) and then sent SIGTERM. Nothing matched by pattern.
* Results: 84 stopped, 0 needed SIGKILL, 0 `login_stub` listeners afterwards.
* Controls: unrelated listeners on 47787 (python), 11434 (ollama) and 5432 (postgres) were present before and after.
* One node listener that did not match all three identity fields (a vitest worker in another tree) was left alone and later exited on its own.

**Why it matters:** each run leaves a process and a port behind. On a machine that pushes often, they accumulate without bound, and anything later identifying "leftover test servers" has to separate them from live ones.

### Dedupe before filing

`searchIssues` (includeArchived, includeComments), literal case-insensitive matches over title, description and comments:

* `bootstrap_login_diagnosis`: 94 fuzzy / 1 literal. KS-1167 (Done, comments): the ticket that introduced the file. It does not mention the leak.
* `start_stub`: 120 / 0.
* `login_stub`: 120 / 0.
* `STUB_PID`: 112 / 1. KS-992 (archived, comments): a different guard's quarantine behaviour.

None covers this. Related: KS-1167.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1201-stubparent-start-stub-runs-in-the-parent-so-the-trap-has-a-pid-b09bcfe27666">Review in Linear</a></p>

