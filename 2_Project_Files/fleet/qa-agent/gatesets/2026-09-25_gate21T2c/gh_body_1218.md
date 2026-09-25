#1218 KS-897 FIXTUREABORT + KS-896 CONTROLEXISTS: pre-push base suite aborts on an unbuilt fixture
head d971aa4f24665bb192765a0c6e82f719996efb92

## What and why

Two defects in `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh`, the suite that polices the
pre-push hook's base resolution. They are the class the suite exists for — **an absent thing reading as a
verified one** — sitting inside the suite itself.

**KS-897** — `build_fixture`'s subshell wrote to `/dev/null 2>&1`, swallowing **failure** as well as
noise, so a fixture that did not build was indistinguishable from one that did.
**KS-896** (`999623d28`) — the CONTROL cell asserted `upstream=NONE`, which is satisfied when
`feature/x` **does not exist at all**. It now asserts `refs/heads/feature/x` exists first, carries that
through the `|`-joined line, and reports it in both messages.

## ROUND 2 — the gate found round 1 not met, and it was right on both counts

Round 1 wrote `( … ) >"$WORK/build.log" 2>&1 || { … exit 2; }`.

**FIXTURE-LASTCMD (blocking).** A `||` reads only the subshell's **last** command, so a MID-build failure
left rc 0. Round 1's own tamper aborted only because `rm -rf`/`mkdir -p "$root"` sat **outside** the
subshell — the red-proof passed for a reason that had nothing to do with the line it was testing.
Measured against the round-1 file: a `false` in the middle of the build gives **rc 0 with all 28 cells
green**.

**FIXTURE-GITENV (safety).** With the root absent, every git verb ran in the **caller's** cwd. Inside a
git repo that rewrote it — `git push -q origin main develop` included. Reproduced: a scratch repo's
HEAD+refs+config hash moves `52cb0fc5b18d` → `ce4a25b62a20` under the round-1 file.

**Why the fix is shaped the way it is.** Verified on `/bin/bash` 3.2.57 *before* writing it:

```
( set -e; false; echo X ) || echo CAUGHT   -> prints X; the || NEVER fires
( set -e; false; echo X ); rc=$?           -> rc=1
```

bash 3.2 ignores errexit inside a subshell that is the **left operand of `||`**. So `set -e` goes inside,
`rm -rf`/`mkdir -p "$root"` move inside ahead of any git verb, `cd "$root" || exit 2` makes escape
impossible, and the status is read as `_bf_rc=$?` **on its own line** — never `|| {…}`.

## RED-PROOF

New `scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh` runs the subject as a **subprocess**
under both tampers, because a fixture failure is an `exit 2` and cannot be observed from inside the same
shell. The same guard against both heads via `SUBJ_SH`:

| subject | result |
|---|---|
| **round-1** file | **4 passed, 2 failed** — only the two defect cells red, all four controls green |
| **this head** | **6 passed, 0 failed** |

`pre_push_hook_base.test.sh` untampered at this head: **28 passed, 0 failed** — unchanged from base, so
the fix costs no cell. All runs on `/bin/bash` 3.2.57 with `TMPDIR=/tmp`, from a cwd outside any git repo.

**Four vacuities of my own in those cells, each caught by an assertion rather than by review:**

1. Both defect cells first passed because a copy of the subject in a temp dir dies on the **missing-hook
   FATAL** — rc 2, 0 cells, no named line. Only the "named line" assertion exposed it. Fixed by passing
   `HOOK_SH`, and **CELL 6** now pins the two `exit 2` causes apart, so an rc of 2 is never read as a
   fixture abort on its own.
2. CELL 6 then **inherited `HOOK_SH` from its own caller** and read rc 0 instead of the FATAL — a verdict
   that depended on the ambient environment. It now runs under `env -u HOOK_SH`.
3. **CELL 5** exists so CELL 2's "identical" compares something: the scratch origin is asserted to be a
   local bare repo under `$WORK` with a real commit, so no verb here can leave this machine.
4. CELL 6's **label** contained the literal abort string, printed on a **passing** line. The fleet STOP
   predicate of 2026-09-25T05:44Z was a substring match on it, so this suite would have tripped every
   seat's push once this merged. Reported, and the label reworded; the literal survives only as the two
   `grep` **patterns** that read the subject's output. (Wednesday then sharpened the predicate to
   line-start, 05:48Z.)

## Pass counts the fleet STOP predicate needs

Rule 2' asks that this squash body state the suite's counts, since the predicate is "0 failed plus the
suite's own pass count":

| suite | at this head |
|---|---|
| `pre_push_hook_base.test.sh` | **28 passed, 0 failed** — *unchanged by this PR* |
| `pre_push_hook_base_fixture_guard.test.sh` (new) | **6 passed, 0 failed** |

And in a full `run-shell-suites.sh` run at this head, lines **starting with** the abort string: **0**
(one mid-line occurrence remains, in a grep pattern, which rule 2' explicitly does not count).

## Test Evidence

**Touched:** `scripts/__tests__/pre_push_hook_base.test.sh` and a new
`scripts/__tests__/pre_push_hook_base_fixture_guard.test.sh` — test-only. No service, no route, no spec,
no runtime config, no migration, no `package.json`, no lockfile.

**Ran:** the guard against both heads via `SUBJ_SH`; the subject untampered; `run-shell-suites.sh` at this
head — **`shell suites: 58 passed, 0 failed (of 58)`**, 57 at the tip plus the one this PR adds;
`check-script-portability.sh` **rc 0, 7 rules across 102 scripts**; `deps-present.sh` rc 0.

**Hermeticity control.** The shared `2_Project_Files/.git` is unchanged across every run: HEAD
`3bad652d17cf…`, porcelain **17**, `core.bare false`, `core.filemode false`,
`user.email kamil.kreiser@secuura.ai`, local `develop` `3bad652d17cf…`, develop reflog **115** entries.
That control is here because KS-1086's incident was **these same fixtures** rewriting the shared `.git`,
and because FIXTURE-GITENV is the same class one level down.

**NOT run:** preflight **legs 3, 4 and 8** — they need the local platform stack on `:6882`, which by
Wednesday's coordination of 02:44:51Z comes up once at the batch QA gate and is not started mid-round.
**This PR is test-only: no route, spec, served-spec or runtime-config surface**, so those legs have no
subject here. Not "gate green": 12 of 15 legs run, three with nothing to test.

**Effect on leg 14's tally:** this PR **adds one suite**, so the reached count rises by exactly one.
`ks949_main_seed_idempotence.test.sh` is untouched and its verdict is unchanged.

**Migrations + config:** none.

Refs KS-897
Refs KS-896

🤖 Generated with [Claude Code](https://claude.com/claude-code)

