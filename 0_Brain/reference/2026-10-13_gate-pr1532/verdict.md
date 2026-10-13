# QA gate: Secuura Platform K PR #1532 (KS-998 item 1), Opus tier 1

**VERDICT: GO WITH NOTE**: 0 Major, 6 Minor, 7 Info. Bound to head `3dbfdf7e36443a8665b6a106e2d8ccbb6763cd44` only.
**Report sha256/16:** `85bf04b8ef22923b`. Recipe: replace the 16-hex value on this line with `REPORT_HASH_PLACEHOLDER`, run `shasum -a 256` over the whole file, and keep the first 16 hex characters.

- **Head under test:** `3dbfdf7e36443a8665b6a106e2d8ccbb6763cd44`. I fetched `refs/pull/1532/head` myself into a scratch `clone --shared`, with the push URL set to `DISABLED`. It matches the brief.
- **Develop:** `3a87133760595b625617617daa587f8af1b821a7`, which matches the brief. The merge-base is `b28bfaecf24e`.
- **Instruments:** macOS, `/bin/bash` 3.2.57(1) (the only bash on PATH, so both the hook and the suites ran under 3.2), node v24.7.0, npm 11.5.1, `sandbox-exec`.
- **Write scope:** no git write verb was run in `!CODING`, nothing was pushed, and nothing was written to GitHub or Linear. Every run used scratch clones or fixtures.
- **Evidence:** raw outputs are under `evidence/` (`logs/`, `mutants/`, `tools/`). Every file name below is relative to it.

**Housekeeping disclosure.** The session scratchpad is shared with other gate agents. My first fetch went into an existing scratch clone (`scratchpad/repo`) that belongs to another agent and created two branches there (`pr1532`, `dev`). I deleted those two refs, which were mine, at once. I also set `core.sshCommand` on that clone to the project's own value. All later work ran in `scratchpad/g1532/`.

## Why GO WITH NOTE and not GO

The change does what the brief asks, and every author number I re-measured held within noise:
- It uses the command and flags that were ruled.
- It installs in a staging dir and renames the result into the package only on an exit code of 0 plus an executable prettier.
- The watchdog bounds the install.
- The breaker, the four named states, the `--all` SKIP, KS-1063 and the stale-base hint all behave as described.

Three things are unsafe at the edges. All three are Minor, and each needs only a small fix:
1. **The final rename has a race.** A concurrent actor's `node_modules` can be moved into the stage and deleted by `_rm_stage`. Two real gate processes on one package REFUSED a correct push in 4 of 5 trials.
2. **The watchdog and the TERM trap kill only npm's pid.** A lifecycle script's child outlives the gate (it is orphaned to ppid 1).
3. **The gate does not check where the lockfile says to fetch from.** A lock entry that points at a non-registry host is fetched, and its postinstall runs on a push.

None of these hides a formatting red or lets a push pass without a check: (1) fails closed, and (2) and (3) are properties of `npm ci` that the gate now triggers automatically. That is why they are notes, not blockers.

## Measurements (each with its instrument and a control)

| # | What | Result (mine) | Author's claim | Control |
|---|---|---|---|---|
| 1 | systemTest gate suite on head, run twice | **185/0, 185/0** (37 s, 36 s) | 185/0 | C1 (gate `exit 0` at the top): **78 passed / 107 failed**, so the harness can fail |
| 2 | Head's suite against develop's gate (red), run twice | **112/73, 112/73** | 98/67 (on an earlier 165-cell revision; the current suite is 185 cells) | — |
| 3 | `ks998_pre_push_stale_base_hint` on head, run twice | **21/0, 21/0**. Red on develop: **14/7, 14/7** | 21/0 | C2 (the hook's gate call removed): 11/10. C3 (the hook exits 0 at the top): 11/10 |
| 4 | `pre_push_hook_base` on head and develop, run twice each | **33/0** in all four runs | 33/0, untouched | C2: 30/3. C3: 16/17 |
| 5 | Real gate on the four real packages, all absent, real registry, empty cache | INSTALLED in 1.8 / 1.2 / 1.2 / 1.2 s, **11 s wall**, rc 0. Lockfiles byte-identical (sha256). `git status --porcelain` 0 lines before and after. `--ignored` diff is only the four `node_modules/`. 0 stage dirs. `observability/node_modules` not created. The akto link `../../../observability` resolves. Sizes 168 / 151 / 137 / 120 MB. Second run 5 s. | 12.2 s, the same sizes | The same clone before the run: 0 status lines, no `node_modules` |
| 6 | The same, with the network denied (`sandbox-exec (deny network*)`), empty cache | 4 × REFUSED, 0.3–0.4 s each, **2.36 s wall**. 0 stages, 0 `node_modules`, git clean | 2.3 s | `curl` inside the sandbox: "Could not resolve host". Outside: HTTP 200 |
| 7 | Watchdog ceiling 4 s, real npm, postinstall that hangs | REFUSED "timed out after 4s" at **4.26 s** | (5 s ceiling → 5.5 s) | CONTROL-nohang: INSTALLED, 0.3 s |
| 8 | SIGTERM / SIGHUP / SIGINT to the gate, stub npm hanging | 143 / 129 / 130 in about 150–310 ms. npm is killed, 0 stages, no `node_modules` in the package | 143 / 130 in 1.5 s | SIGKILL: 137, npm survives, 1 stage left, swept by the next run (rc 0, 0 stages) |
| 9 | `FORMAT_GATE_INSTALL_TIMEOUT` set to `''`, `0`, `-5`, `abc`, `1.5`, `08`, `1234567`, `' 5'`, `'5 '`, `999999`, `1`, or a 20-digit value | `''`, `1` and `999999` are accepted. Every other value exits 2 and names the variable | — | — |
| 10 | Scope | 7 files, +1169/−53. They match the PR body's "Touched" list. Hook +19/−1. `git merge-tree` against develop is clean, with **0 overlapping paths** | "develop moved by ONE commit (KS-1556)" | **Develop moved by TWO**: `7c6b3d880` KS-1556 and `3a8713376` KS-1557 (originate). Still zero overlap (Info 1) |

Logs: `logs/suites_head_red_x2.txt`, `logs/head{1,2}.*`, `logs/red{1,2}.*`, `logs/T12_real_four_packages.log`, `logs/T12b_offline_sandbox.log`, `logs/T5*`, `logs/T1*.log`, `mutants/C*`.

## Findings

### Minor 1: the final rename races, so `_rm_stage` can delete a `node_modules` the gate did not make, and two concurrent gates refuse a correct push

**Where:** `systemTest/scripts/check-package-format.sh:268-286`.

The guard `[ -e "$dir/node_modules" ] || [ -L ... ]` at line 268 is not atomic with the `mv` at line 272. BSD `mv` onto an existing directory moves the source *inside* it. Onto a symlink to a directory, it moves the source into the symlink's target.

When prettier then is not executable at the top level, line 281 moves `$dir/node_modules`, which is now the *other actor's* tree with ours nested in it, "back" into the stage. Line 290 `_rm_stage` then deletes it. The guards in `_rm_stage` are path-based and hold. The content is what is foreign.

**How I tested it** (`logs/T4_mv_race.log`): a PATH `mv` shim creates `pkg/node_modules` inside the window, then execs `/bin/mv` (`tools/mv.shim_race`). Each arrival shape gave a different result:

| What arrived in the window | Result |
|---|---|
| A hollow, in-progress tree (an `npm ci` that has created `node_modules` and not yet linked prettier) | That tree, with its sentinel `OTHER_ACTORS_FILE`, was **deleted**. The refusal blamed it on "the install embeds its staging path". |
| A symlink to an outside directory | Our 1-package tree was **written into the outside target**, and the gate deleted the symlink. |
| A complete tree | INSTALLED, with our tree left nested as `node_modules/node_modules`. |
| Nothing (control) | INSTALLED, clean. |

**Two real gate processes, one package** (`logs/T6_two_gates_race.log`): real npm, offline tarball, postinstall `sleep 1.x`, 5 trials.
- In 4 of 5 trials, one gate exited 1 with "REFUSED … the staged node_modules could not be moved into place" (`mvfail`). `mv` loses its own stat/rename race and gets ENOTEMPTY. **A correct push is refused.**
- In 1 of 5 trials, both said INSTALLED and a nested `node_modules/node_modules` was left.

The author's CASE 24 covers only an arrival *before* line 268, and the PR body lists the real race as "not run".

**Severity: Minor.** It fails closed, the window is milliseconds, and what can be lost is a regenerable, gitignored tree. But it falsifies "deletes only what it made".

**Minimal fix:** replace the `mv` at line 272 with `node -e 'require("fs").renameSync(process.argv[1],process.argv[2])'`. `rename(2)` refuses a non-empty target (ENOTEMPTY or EEXIST) and a symlink target (ENOTDIR). Map that failure to `raced`, not `mvfail`.

In the `mvbroken` branch, move back only what the gate itself moved. Drop a marker file into the staged tree before the rename, for example `node_modules/.format-gate-<stage-id>`, and require it at `$dir/node_modules/` before the move-back.

### Minor 2: the watchdog and the TERM path kill npm's pid, not its process group, so lifecycle-script children are orphaned

**Where:** `check-package-format.sh:240-255` (the watchdog) and `:206-216` (`_fg_cleanup`).

**How I tested it** (`logs/T5c_real_npm_hung_postinstall.log`, `logs/T5d_term_ignoring_child_Q6_Q7.log`): real npm, a dependency whose postinstall hangs.

| Path | Gate result | The postinstall child |
|---|---|---|
| Watchdog | REFUSED at 4.26 s | **Still alive, ppid=1**, cwd inside the now-deleted stage |
| SIGTERM to the gate | rc 143 in 0.65 s | **Still alive, ppid=1** |
| SIGKILL | — | Still alive |
| Ctrl-C emulated as SIGINT to the whole process group | — | Gone, because the terminal signals the group |

A child that ignores TERM shows the same orphaning. npm itself always exited promptly on TERM in every shape I measured.

**Why it matters:** esbuild's `install.js` (performance, playwright, and akto's nested `tsx`) has a fallback, `downloadDirectlyFromNPM`. It uses `https.get` with **no timeout** and a hard-coded `registry.npmjs.org`. Against a silent registry, that is exactly the process that would be orphaned, and it would hang indefinitely.

The orphan holds no pipe of git's, so the push itself completes. The author listed this case as "not measured". It is now measured.

**Minimal fix:** start npm in its own process group and signal the group: `kill -TERM -- -$pgid`, then `-KILL`. In bash 3.2, `set -m` around the launch does this, or use `perl -e 'setpgrp; exec @ARGV'`. Apply it in both the watchdog and `_fg_cleanup`.

### Minor 3: the gate does not check lock sources, so an injected lock entry is fetched from any host and its scripts run on the push

**How I tested it** (`logs/T8b_lock_entries.log`): `package.json` declares `foreign-dep@1.0.0`, a registry range. Only the lock entry's `resolved` points at `http://127.0.0.1:<port>/…` with a matching integrity. The npm cache was empty.
- The gate fetched it: the listener log shows **1 GET**.
- It said INSTALLED.
- The postinstall **ran and wrote a sentinel outside the repo**.

Control: a tampered integrity was REFUSED with EINTEGRITY, leaving no `node_modules` and no stage.

**Credentials in scope** (`logs/T7_T8.log`, values redacted by construction):
- A dependency's postinstall run by the gate saw `NPM_TOKEN`, `GH_TOKEN` and a test secret from the environment. A control run without those variables did not see them.
- It also saw `SSH_AUTH_SOCK` and other `*TOKEN` names present in this machine's environment.
- npm's userconfig `~/.npmrc` is in scope.
- `--fetch-retries=0` and `--fetch-timeout` reach lifecycle children through `npm_config_*` (`logs/T13_esbuild_fallback.log`).

This is what a manual `npm ci` does too, and Wednesday ruled no `--ignore-scripts`. The difference is that it now runs **automatically on push**, including for a package selected by a stale base or a merge the developer did not author.

Today's four lockfiles are clean. I re-measured independently with `tools/lockscan.js`:

| Package | Entries | `registry.npmjs.org` + integrity | Links | Install scripts |
|---|---|---|---|---|
| akto | 413 | 411 / 411 | `../../observability` | fsevents, tsx/esbuild |
| api-explorer | 344 | 344 / 344 | — | fsevents |
| performance | 271 | 269 / 269 | `../../observability` | esbuild, fsevents |
| playwright | 217 | 217 / 217 | — | esbuild, fsevents |

**But nothing enforces it.**

**Minimal fix:** a node pre-check before `npm ci`. Every non-link entry must have `resolved` starting with `https://registry.npmjs.org/` and a non-empty `integrity`. Every `link` must resolve inside the repo. Otherwise, refuse with a named reason and run nothing.

### Minor 4: one "survived by design" mutant is not equivalent (m23b)

The author says m23b (no EXIT trap) is "EQUIVALENT alone". On bash 3.2 that is false. The EXIT trap is what cleans up on untrapped fatal signals other than QUIT.

`logs/T5b_signals_jobcontrol_and_m23b.log`, SIGUSR1 to the gate mid-install:

| Gate | Hung npm | Stage |
|---|---|---|
| head | killed | removed |
| m23b | **alive** | **left** |

The same mechanism covers SIGALRM and SIGPIPE: on head they clean up (`logs/T5_signals_stub.log`). The suite has no cell for it.

The other four survivors I re-derived and judge **truly equivalent**:
- **m13a:** `_rm_stage`'s own `-L` check refuses.
- **m23:** measured (`logs/T5e_m23_term.log`). TERM gives 143 with a clean result with and without the TERM trap, because bash 3.2 runs the EXIT trap on SIGTERM death.
- **m25:** every input is absolute, so the single-component guard refuses everything outside the prefix.
- **m35:** `--all` never refuses (lines 445-453).

**Fix:** add one cell that sends SIGUSR1 or SIGALRM mid-install and expects no orphan and no stage.

### Minor 5: four of my mutants survive, and they are test gaps, not equivalents

Full table: `logs/mutants_summary.txt`.

| Mutant | Result | What it shows |
|---|---|---|
| **Q8** (line 266 `-x` → `-e`) | survives | The suite has no cell with a non-executable prettier. Head refuses it correctly (`logs/T9_classification.log`). The mutant would move the tree in, then out, under a misleading reason. |
| **Q11** (line 414 hollow re-check dropped) | survives | A raced-in hollow tree would be reported as a *formatting failure* instead of the environment refusal. That is the KS-991 confusion this ticket guards against. |
| **Q12** (`.npmrc` not copied to the stage) | survives | No fixture has a package `.npmrc`. |
| **Q13** (6-digit length guard dropped) | survives | With a 20-digit value, the mutant **refuses at once** with "timed out after 99999999999999999999s" (the integer overflow ends the watchdog loop). Head exits 2 and names the variable (`logs/T1b_Q13_overflow.log`). |

**Fix:** one cell each.

### Minor 6: a SIGQUIT to the gate alone leaves npm and the stage

SIGQUIT is not trapped, and bash 3.2 does not run the EXIT trap for it. Result: rc 131, the hung npm alive, 1 stage left (`logs/T5b…`, head QUIT row). The next run sweeps the stage. A terminal Ctrl-\ also signals npm itself.

**Fix:** add QUIT to the trap list.

### Info

1. **Develop moved by two commits, not one.** KS-1557 landed at 11:01 on `services/originate`. There is still zero path overlap, and the merge-tree is clean.
2. **Pre-existing behaviour (KS-1483): branch deletions and tag pushes are refused because of HEAD's diff.** A branch deletion (`git push origin :todelete`) and a tag push were both REFUSED because HEAD's branch touched an uninstallable package. The hook computes the changed set from `@{upstream}..HEAD`, not from the pushed refs. **The develop control refuses the same two pushes** (KS-1063 NOTHING CHECKED) (`logs/T11_hook_handoff_CONTROL_develop.log`). So this is not a regression, and the PR body discloses it. The hand-off itself (`logs/T11_hook_handoff.log`) behaved as described:
   - A new branch installed and landed.
   - An existing branch was checked only and landed.
   - A deletion-only push under a package selected it, installed and landed.
   - The stale hint was absent with an own-counterpart upstream and present with an `origin/develop` upstream.
   - A dangling-symlink `node_modules` was refused, npm ci was invoked **0 times**, and the link was kept.
   - `--all` gave named SKIPs, no refusal, and rc 0.
   - Develop's control refused every one of the first two pushes, so the harness can tell the difference.
3. **`_rm_stage` with an empty `STAGE_PREFIX`** deletes a relative single-component directory under the cwd. I demonstrated it with the function extracted (`logs/T2_rm_stage.log`). It is **unreachable**: the prefix is assigned once and is never empty, and `set -u` aborts if it is unset. Defence in depth would be `[ -n "$STAGE_PREFIX" ]` plus requiring an absolute `$d`.
4. **`_rm_stage` path attacks held** (`logs/T2_rm_stage.log`, `logs/T3_sweep_weirdroot.log`). Sentinels in the repo root, the package and an outside directory were **all kept** under every case I tried:
   - an empty argument, the repo root, the package dir
   - `prefix../pk`, `prefixx/../../pk`, `prefix..`, a bare prefix
   - a symlink stage and a dangling stage symlink (both refused, links kept)
   - a regular file
   - a real stage containing symlinks to the outside and to the package: only the links were removed, never their targets
   - a stage name with a space and a newline
   - a full gate run in a repo root named `we ird [a]* ro?ot<newline>nl`

   The sweep removed only the dead-pid real stage. It kept the live-pid, non-numeric-pid and `..`-named stages and the symlink. A real directory that happens to carry the reserved prefix with a dead pid **is** removed. That is by design: the prefix is gitignored.
5. **Two minor classification gaps.** `-x` is true for a *directory* named `.bin/prettier` (exit0-prettier-dir, `logs/T9_classification.log`), so it is INSTALLED and then reported as a formatting failure with rc 126. npm never produces this. Separately, the classification follows the exit code over npm's words in both directions, as tested:

   | npm shim | Gate result |
   |---|---|
   | Prints "added 300 packages", exits 1 | REFUSED |
   | Prints `npm error`, exits 0 with prettier | INSTALLED |
   | Exits 0, prettier not executable | REFUSED |
   | Exits 0, dangling prettier symlink | REFUSED |
   | Exits 0 with a fake prettier that only exits 0 | INSTALLED and "OK". The gate trusts the lockfile's prettier by design. |
6. **An invalid `FORMAT_GATE_INSTALL_TIMEOUT` blocks every push**, including ones that touch no systemTest file. The validation exits 2 before selection, and the hook's wrapper then says "fix the files named above". It is loud and self-inflicted, but the wrapper's wording is wrong for it.
7. **Esbuild's network fallback, exercised under the sandbox** (`logs/T13_esbuild_fallback.log`): with `@esbuild/darwin-arm64` removed, `install.js` tries `npm install` and then a direct download. It takes **70.4 s** with npm defaults and **0.43 s** with `npm_config_fetch_retries=0`, and that value **is** inherited from the gate's `npm ci` (measured through a postinstall). Both paths verify the binary with a sha256 before use.

## Mutants (mine plus the re-derived survivors; full logs in `mutants/`)

Each mutant ran the gate suite plus the hook suite. Hook mutants ran the hook suite plus `pre_push_hook_base`.

| Mutant | Result, with the first failing cell |
|---|---|
| C1 gate passes everything | KILLED 107: "discovers a package that declares format:check" |
| C2 hook's gate call removed | KILLED: "stale origin/develop: the push is REFUSED"; base suite "CASE 7 — a systemTest-only push invokes the formatting gate" |
| C3 hook exits 0 | KILLED in both suites |
| Q1 rename replaced by `cp -R` | KILLED 4: "an install that embeds the stage path -> exit 1" |
| Q2 watchdog kill removed, marker kept | KILLED 10: "...REFUSED, as a TIMEOUT with the ceiling in the line" |
| Q3 exit-code check dropped, executable check kept | KILLED 2: "npm prints 'added 1 package' but exits 1 -> still REFUSED" |
| Q4 stage outside the package filesystem (`$TMPDIR`) | KILLED 4: "CONTROL the install is really in flight…" |
| Q5 no `exec` (so `$!` is the subshell) | KILLED 6: "...the hung npm was killed - no orphan" |
| Q9 post-move check uses `-e` | KILLED 4 |
| Q10 breaker never consulted | KILLED 5: "...npm was run for ONE package only" |
| Q14 dead-pid test inverted | KILLED 3: "a stage of a DEAD pid is swept" |
| QH1 no-upstream base not flagged stale | KILLED: "...and the hint: your origin/develop may be stale" |
| QH2 flag compares the full upstream name | KILLED: "...and NO stale-base hint…" |
| Q6 watchdog TERM only / Q7 cleanup without KILL | SURVIVED, **equivalent for npm 11.5.1**: npm exited on TERM even with a TERM-ignoring child (`logs/T5d…`) |
| Q8, Q11, Q12, Q13 | SURVIVED, **test gaps** (Minor 5) |
| m13a, m23, m25, m35 | SURVIVED, equivalent (Minor 4) |
| m23b | SURVIVED, **NOT equivalent** (Minor 4) |

I did not re-run the author's other 41 mutants. Their intent, read from the PR table, maps onto the cells I saw fail in my own mutants and controls.

## NOT tested, and why

- **Linux:** Docker was not running (`docker info` could not reach the socket) and no remote box is allowed. GNU `mv` has the same move-into-directory behaviour, so I expect Minor 1 to apply, but I did not measure it.
- **The preflight legs that need the local stack (3, 4, 8) and the full preflight A/B:** not run. I did not re-measure the author's "13/16, 198 identical verdict lines".
- **A real pty Ctrl-C:** I emulated it with SIGINT to the job's process group under `set -m`.
- **A silent (accept-and-hang) registry against esbuild's direct download:** I reasoned it from the code (no timeout on `https.get`). I measured only the orphan mechanism, with a hanging postinstall.
- **The author's request census for `--no-update-notifier`:** not repeated.

## Recommendation to Wednesday

**GO WITH NOTE** on `3dbfdf7e3644`. This is developer tooling: merge on Wednesday's head-bound GO, and do not deploy anything.

I recommend fixing Minor 1 (the atomic rename plus a move-back guard) and Minor 2 (killing the process group) in the stacked item-2 PR or a fast follow. Minor 3 (the lock-source allowlist) is a cheap hardening step that Kam or Wednesday should rule on, because it narrows the ruled "lifecycle scripts run" surface without removing it. Minors 4 to 6 are one suite cell each.
