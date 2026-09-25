SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA 4 (Seat L4): #1234 KS-1127 + KS-1089 + KS-1135 — head 6320a61d8, TIER 1, 41/8 base -> 49/0 head; the new 3-field verdict ran live in its own push hook
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T06:17:31.000Z
MESSAGE_ID: <010001a0d7363f3a-f40a1ad8-25d1-496d-8e32-1740e0430b1c-000000@email.amazonses.com>
CAPTURED: 2026-09-25T07:31:48Z by the gate21T1c drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: a77dac4ddb4d2185b90a618160a4d89d5aaf294690f668b13c2dbcc16ee95ab1
# READY FOR QA 4 (Seat L4): #1234 KS-1127 + KS-1089 + KS-1135 — head 6320a61d8, TIER 1

**My omission, stated first:** this PR was raised at 05:4xZ and I never sent its READY. You found it, not
me. Nothing about the PR changed in the interval; only this mail was missing.

## BLUF
**PR #1234**, head **`6320a61d86b5d3fb9b693ea5fefb42050e1d2a43`** — read by `ls-remote` in the same action
as this mail — base `develop`, **TIER 1**, 1 commit, 2 files, +187/−7, `mergeable: True`. All **three**
attachments read `linkKind: contributes`. Push rc 0 first attempt, verify **PROTOCOL-CLEAN**.

## Tier 1, and the tier rests on a measurement
This is `scripts/run-shell-suites.sh` — the runner **preflight leg 14 executes for every seat**. Before
proposing tier 1 I measured the blast radius: `git grep -l -F 'shell suites:'` at develop `6ab9d5021e96`
returns **one file, the runner itself**, and leg 14 (`scripts/preflight/preflight.sh:643`) consumes only
the **exit status**. So adding a field breaks no consumer; the tier is about *when* it lands, mid-round.

## The change proved itself inside the gate that consumed it
The **in-hook** leg 14 during this PR's own push printed, at this head:

```
shell suites: 57 passed, 0 failed, 0 skipped (of 57)
```

That is the new three-field verdict, live in the pre-push hook. Rule 2' on the same run: lines **starting
with** the abort string **0**, and `pre_push_hook_base.test.sh` **28 passed, 0 failed**.

## RED-PROOF — the same test file against both runners via RUNNER_SH

| runner | result |
|---|---|
| base `6ab9d5021e96` | **41 passed, 8 failed** |
| this head | **49 passed, 0 failed** |

Eight new defect cells red at base, green here. **The controls hold at BOTH ends, which is what makes them
controls:** `--list` with one suite still prints exactly one line; the "git printed nothing" headline is
unchanged and passes at base too; a short TMPDIR emits no note; a tree with nothing to skip reads
`0 skipped` and prints no `SKIPPED:` block; a **silent** exit-0 suite is still a pass; the caller's TMPDIR
returns (184 in, 184 out).

**KS-1127** on a four-suite fixture — a real pass, a `SKIP —` + exit 0, a real failure, a silent exit 0:
```
base    shell suites: 3 passed, 1 failed (of 4)
head    shell suites: 2 passed, 1 failed, 1 skipped (of 4)   SKIPPED: …/t1127-skip.test.sh
```
**KS-1089 QA-8** on /bin/bash 3.2.57: base on an empty tree **rc 1, 55 bytes, `line 72: reached[@]:
unbound variable`** — the ticket's own line number; head **rc 0, 0 bytes**. The cell measures **bytes**,
because a `$(…)` capture reads empty for the guarded form and for the `+alternate` form alike.
**KS-1089 QA-7**: three causes, three headlines, each asserted.
**KS-1135**: a 218-char TMPDIR gives base **0** lines naming the cause; head names it, twice.

## Test Evidence
**Touched:** `scripts/run-shell-suites.sh` and `scripts/__tests__/run_shell_suites.test.sh`. No service,
route, spec, runtime config, migration, `package.json`, lockfile, `scripts/audit/`, `scripts/preflight/`
or `packages/shared`.

**Ran:** the base-vs-head matrix via `RUNNER_SH`; the four-suite skip fixture; the empty-tree `--list`
byte measurement; the 218-char TMPDIR run and its short-TMPDIR control; `check-script-portability.sh`
rc 0; `deps-present.sh` rc 0; and the in-hook leg 14 above.

**NOT run, and deliberately so: no standalone `run-shell-suites.sh` at this head.** Your rule 1 bars it
until #1218 merges, so the runner figure I quote is the **in-hook** one from this PR's own push, which
rule 2 expects. That is the only run of it I have at this head, and I am not going to imply otherwise.

**NOT run:** preflight **legs 3, 4, 8** — local stack not up, and this PR has no route, served-spec or
runtime-config surface, so nothing is owed at the gate. 12 of 15 legs ran; not "gate green".

**Out of lane, declared:** KS-1127's second bullet asks that **leg 14 quote that line** — a
`scripts/preflight/` edit, not this lane. The ticket stays open for it.

**Honest limit:** there is **no live skip on this machine** — a real PostgreSQL 15.14 is on PATH, so
`ks949_main_seed_idempotence.test.sh` runs in full and every run reads `0 skipped`. The tally is proved by
a **purpose-built fixture**, not by a real skip. Likewise every run of mine used a 4-char TMPDIR
deliberately, which is avoidance, not evidence. Both limits are in the PR body too.

**Two of my own mistakes, caught by these cells:** the QA-7 git-absent cell would have passed on any
broken PATH, so it is now paired with a control running the same minimal PATH **with** git symlinked in;
and the KS-1135 cell expected the note once and found two — the second print is deliberate, the
expectation was wrong, and the cell now pins 2 with the reason.

## Orphan login_stub count, by cwd + ppid as you ruled
**0 mine and orphaned · 0 mine and in use.** One process elsewhere on the box names `login_stub.mjs` but
its cwd is `/Volumes/DevMASTER/!CODING/Testing Agent MAIN` — a different project, not a seat worktree, and
never touched. This PR's own push reaped 4, 0 remaining.

## The push
lock 05:29:44Z → released 05:39:59Z · push rc 0 first attempt · origin holds `6320a61d8` == mine ·
config `4cd3b01ca1e71947 -> 4cd3b01ca1e71947` identical · verify **PROTOCOL-CLEAN**, *"first push:
tracking ref added at origin's head 6320a61d…"*.

## VERIFIED BEFORE SENDING
- head at origin | `ls-remote` in this same action | 2026-09-25
- PR state, files, +/−, mergeable | GitHub REST | 2026-09-25
- all three `linkKind: contributes` | Linear GraphQL | 2026-09-25
- every tally | run in `worktrees/s-l4-ks1127` and in scratch fixtures | 2026-09-25
- the in-hook leg-14 line and the ^abort count | `grep` on `KS1127-push1.out` | 2026-09-25
- the stub census | `reap_stubs_l4.sh --dry-run` | 2026-09-25

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25

