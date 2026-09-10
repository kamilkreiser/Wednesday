---
date: 2026-09-10
type: principle
source: caught in my own red-proof harness before it shipped, panel_sync recovery
status: live
tier: W
---

# A detector keyed on the REMEDY's name matches the tool's HINT about that remedy — and the hint appears in the failure you must NOT apply it to

**The case, in full, because the shape is subtle.** I was fixing `panel_sync.sh` so a
failed `git pull --rebase` could recover instead of deadlocking. One branch had to detect
*"this replayed commit came out empty"*, whose correct remedy is `git rebase --skip`. I
wrote the detector as:

```bash
if printf '%s' "$cont" | grep -qiE 'no changes|nothing to commit|--skip'; then
    git rebase --skip
```

**`git`'s CONFLICT output contains the line `You can instead skip this commit: run "git
rebase --skip"`.** So on a *conflict* — the one state where skipping is catastrophic —
the detector matched, and the code ran `git rebase --skip`, **silently dropping a
real-work commit.**

## The general shape

**I keyed the detector on the name of the remedy rather than on the condition.** Tools
name their remedies in their error text *precisely when things have gone wrong*, including
in the failures where that remedy is the wrong one. So a pattern containing a remedy's
name matches:

- the state that genuinely calls for it, **and**
- every state where the tool is *offering* it as one option among several.

The second set is larger, and it is where the damage lives.

## The rule

1. **Key a detector on the CONDITION, never on the remedy's name.** Here the condition is
   *"nothing is conflicted"* — a `git diff --diff-filter=U` that comes back empty — which
   is a fact about the repository, not a string in a message.
2. **When a string test is unavoidable, exclude the tool's own advice vocabulary.** Match
   `no changes`, `nothing to commit`, `patch is empty`; never `--skip`, `--force`,
   `--abort`, `--hard`, or any other flag the tool suggests when it is unhappy.
3. **Order the checks so the dangerous branch is unreachable from the dangerous state.**
   I now test *"is anything conflicted?"* first and `continue` the loop if so, so the skip
   branch cannot be reached while a conflict exists. Ordering beats pattern-tuning: it
   removes the failure rather than narrowing it.

## Why only the harness could find it

**Reading the diff would not have caught this**, and I had read it. The bug is not visible
in the code — it is visible only in the *conjunction* of my code and git's output text,
and git's output text is not in my file. It surfaced within seconds of running the real
script against an induced conflict in a two-seat harness (bare origin + two clones).

**A recovery path is exactly the code that never runs in normal operation**, so it is
exactly the code that ships untested unless failure is induced deliberately. This is
[[2026-08-11_a-check-that-cannot-fail-is-not-a-check]] pointed at the repair rather than
the check: *a recovery you have never made fail is a claim, not a recovery.*

**Family:** [[2026-08-11_a-check-that-cannot-fail-is-not-a-check]] ·
[[2026-09-08_exercise-a-new-mechanism-in-its-real-environment]] ·
[[2026-08-03_mental-model-not-source-of-truth]] (git's actual output is the source; my
belief about its wording was the model) ·
[[2026-09-10_steps-to-kam-are-a-claim-about-his-screen]] (same day, same root: acting on a
representation of a system instead of a reading of it).
