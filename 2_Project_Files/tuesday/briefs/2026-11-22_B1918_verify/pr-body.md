A test-only fix for the red push run of `main` (`bf6b441e`, run 45001737294): its `linux` job failed ONE test,
`RefreshBoundCellTests.F13_after_a_time_out_a_second_call_may_start_and_the_late_answer_is_never_kept`, at
`RefreshBoundCellTests.cs:22` reached from `:141`. One commit on `main` `bf6b441e`, two test files.

## Why it was red

The token broker behaved correctly; the test raced. F13's scripted refresher handed out its two answers in the order
in which the calls reached their answer, not by which call they were. When the first (timed-out) call was preempted
after it was counted and before it answered, the second (live) call took the answer F13 calls `late`; the broker
legally kept the live call's answer, and the test read that as a kept late answer. The only code that replaces the
held grant (`AcceptLocked`) is reached only when the call did not time out; a timed-out call's answer goes to
`DisposeWhenDone`, which disposes it. A second, smaller race of the same cause: the fake counted a call before it
recorded the call's token and renewal state.

## What changed

- `tests/Datasec.Suite.Sessions.Tests/Fakes.cs` (the fake refresher only): it records a call, then counts it,
  inside its one lock; it gains `AnswerOfCall` (an answer chosen by the call's index), `BeforeAnswer` (a test-only
  seam each call awaits with its index after it is recorded and before it answers) and `Answering` (the calls whose
  scripted answer has started). With none of them set, every other cell's fake behaves as before.
- `tests/Datasec.Suite.Sessions.Tests/RefreshBoundCellTests.cs` (cell F13 only): F13 keeps its name, its steps and
  its messages, and runs as one shared scenario with its answers keyed on the call's index, so the late answer is
  always the timed-out call's, in whichever order the runner gives the two calls.
- One new cell, `F13_the_late_answer_is_never_kept_when_the_timed_out_call_answers_after_the_second_call`: the seam
  holds the timed-out call until the second call has started its answer, the interleaving of the hosted failure, on
  every run. Against the old arrival-order answers it fails by its own assertion on every run (20 of 20 locally);
  against the index-keyed answers it passes (200 of 200 locally, and on both hosted legs).

## What does not change

No file under `src/`. No package, project, lock or solution file, no workflow, no build script, no unit-test floor.
No cell is loosened, skipped or given a retry or a sleep. The other cells with the same wait (F15, F05 hang, F05 late,
F08, F09, E07, L01) each have one refresher call in flight and are unchanged.

## Limits, stated plainly

- The record-then-count change has no cell of its own: a mutant that counts before it records leaves every cell
  green (a named survivor). It is closed by reading: the record, the count and the two reads share one lock.
- Whether the hosted linux leg shows this race again after the landing is UNMEASURED until `main`'s next push run.

## Who decides

The lane (a test-only fix, one pull request, the seam kept in the repository) and every choice inside it are the
coordinator's, made as coordinator.

1 new test (1578 -> 1579 locally and on both hosted legs of the branch run 45006189382; skipped 4 on linux and 19 on
windows, as before; RULES 500 files; Ran 111, floor 111). Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
