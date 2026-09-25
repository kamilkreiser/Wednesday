#1218 KS-897 FIXTUREABORT + KS-896 CONTROLEXISTS: the pre-push base suite can no longer pass on a fixture it never built
head 999623d28f7cc3f11140cf379cfd3169e6530b57

## What and why

Two defects in `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh`, the suite that polices
the pre-push hook's base resolution. They are the same class the suite exists for — **an absent thing
reading as a verified one** — sitting inside the suite itself, which is why they are one PR: one file,
one run of that file proves both, and KS-897 is the enabling silence for KS-896's class.

**KS-897** (`ebbdb3df6`) — `build_fixture`'s subshell redirected its whole body to `/dev/null 2>&1`.
The redirect is deliberate (the fixture build is noisy) but it swallowed **failure** as well as noise.
It now writes to `$WORK/build.log` and a non-zero build prints a named error plus the log and
`exit 2` — this file's own `:60` convention for "cannot run at all".

**KS-896** (`999623d28`) — the CONTROL cell asserted `upstream=NONE`, which is satisfied when
`feature/x` **does not exist at all**. It now asserts `refs/heads/feature/x` exists first, carries that
through the `|`-joined line, and reports it in both the pass and the fail message.

## Two things measured before writing either fix

- **The log is echoed, not named.** `:64` is `trap 'rm -rf "$WORK"' EXIT`, so a message naming
  `$WORK/build.log` would point at a file the reader cannot open.
- **`exit 2` aborts the suite, not one subshell.** All **12** `build_fixture` calls are at column 0 —
  none inside a subshell or a command substitution.

## RED-PROOF — every cell can fail, and the clean tally never moves

Run with `proof_pr1.py`, which tampers a **copy** and never modifies the tree under test. Trees are
`git archive` exports, so there is no worktree and no ref write. All runs under **`/bin/bash`
3.2.57**, which is what the pre-push hook uses, and `TMPDIR=/tmp` (4 chars — the KS-1135 shape avoided
deliberately).

| tamper | base `6ab9d5021e96` | head `ebbdb3df6` (897 only) | head `999623d28` (both) |
| --- | --- | --- | --- |
| **none** | 28 passed, 0 failed · rc 0 | 28 passed, 0 failed · rc 0 | **28 passed, 0 failed · rc 0** |
| **T897** — the CONTROL's fixture built at `/dev/null/nope` (`mkdir -p` fails ENOTDIR) | rc **1** · 27 passed, 1 failed · **no named abort** · 27 cells still ran | rc **2** · no tally line · **named abort** · 0 cells ran | rc **2** · **named abort** |
| **T896** — the CONTROL's checkout cut from `origin/NOSUCHREF`, so `feature/x` is never created | rc **0** · 28 passed, 0 failed · **CONTROL ok** | rc 0 · 28/0 · CONTROL ok | rc **1** · 27 passed, 1 failed · **CONTROL red** |

Three things this table is saying:

1. **T896 at base is KS-896 exactly** — a full green tally, and the CONTROL reporting *"the fixture is
   a real fresh clone … upstream=NONE"* for a fixture in which the branch was never created.
2. **T897's claim is stated precisely.** At base the tamper already surfaced — as an **anonymous** red
   with the suite carrying on into 27 more cells. So the cell asserts **rc 2 and the literal
   `FIXTURE BUILD FAILED` line and that no cells ran**, never merely "rc is non-zero", which base
   already satisfies for the wrong reason. This is the ticket's own BLUF: *"the failure surfaces (if at
   all) as a confusing assertion rather than as 'the fixture did not build'."*
3. **The middle column** shows the two commits are independent — the KS-897 commit leaves the KS-896
   tamper still passing, so neither fix is masking the other.

**Hermeticity control.** `2_Project_Files/.git/config` sha256 `6417b203accd839f` before and after every
run; `user.email` `kamil.kreiser@secuura.ai` and `core.bare false` unchanged. That control is here
because KS-1086's incident was these same fixtures rewriting the shared `.git` when run **in-hook** with
`GIT_DIR` inherited; from a normal shell there is no `GIT_DIR`, and #953's strip is on develop.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh` — one file, test-only. No
service, no route, no spec, no runtime config, no migration.

**Ran:**
- `pre_push_hook_base.test.sh` standalone, `/bin/bash` 3.2.57 — **28 passed, 0 failed** at this head,
  identical to base.
- The full red-proof matrix above: **8 suite runs** across base and both heads, two tampers plus clean.
- `scripts/check-script-portability.sh` — **rc 0, "7 portability rules hold across 102 shell scripts"**.
- `scripts/run-shell-suites.sh` at this head — see the ratio line below.
- `scripts/preflight/deps-present.sh` — rc 0, "workspace install present".
- The 15-leg pre-push preflight, in-hook, on the push itself.

**NOT run:** preflight **legs 3, 4 and 8** (they need the local platform stack on `:6882`). Per
Wednesday's coordination of 2026-09-25T02:44:51Z the stack comes up **once, at the batch QA gate**, and
is not started mid-round by any seat. **This PR has no route, spec, served-spec or runtime-config
surface, so those legs have no subject here** — nothing is owed at the gate for this change. This is not
"gate green": it is 12 of 15 legs run, and three legs with nothing to test.

**Migrations + config:** none. No `package.json`, no lockfile, no `.github/`, no
`scripts/audit/`, no `scripts/preflight/`.

## Effect on leg 14's tally

The change is test-only and adds no suite, so `run-shell-suites.sh`'s count of reached suites is
unchanged. `ks949_main_seed_idempotence.test.sh` — the suite Seat B 25th runs through that runner — is
untouched by this PR and its own verdict is unchanged.

Refs KS-897
Refs KS-896

🤖 Generated with [Claude Code](https://claude.com/claude-code)

