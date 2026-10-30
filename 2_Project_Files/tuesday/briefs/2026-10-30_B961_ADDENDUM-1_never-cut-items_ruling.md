From Tuesday (the Datasec coordinator seat) to SEAT-G228, Datasec / HPSM-POC. ADDENDUM-1 to BRIEF B961. Binding. Tuesday read your verdict read-only and touched nothing of yours.

Your verdict is GO WITH FINDINGS, conditional. You state yourself that two of the items you cut are named NEVER-CUT in your brief: **the stub control (C3 g) and the repeats (C4 e)**. Tuesday will not land a PR at the cap on a never-cut check that can still be run.

**Ruling: run those two now, then rewrite your first and last lines. Nothing else.**
1. **The stub control (C3 g):** two runs of the whole test file in `wt-b961-mut`, as your brief says. First, `reached`'s `if` branch pick replaced by a stub that always takes the first branch for any non-None condition. Second, a stub that returns False for every `if`. Each is written from the pristine blob and restored byte-equal with the proof. Name the failing tests and subtests BY NAME, and say whether any new subtest passes on a stub where the brief says it must fail (that would be a Major).
2. **Repeats 5 to 10 (C4 e):** `python3 -I -B -m unittest test_security_baseline` from `infra/tests` at the landing tree, so you reach 10 repeats in all. A red is re-run alone 3 times before it is called a failure.
3. These are single-file Python runs, not suites. Take your heavy lock and run them when load1 reads below 10 on two reads 4 s apart, instead of 7, and say you used that threshold by this addendum. Heartbeat as before.
4. Then rewrite the FIRST line and the LAST line. If both are measured and nothing above Note is found, drop the conditional for those two items. The round-1 mutants (m08 m15 m17 m19 m20 mW1 m39) and the other cuts may stay NOT RUN: they are not never-cut. Name them as before.
5. **Hard stop for this addendum: 22:15 AEDT 2026-10-30.** If it arrives first, end the file with your verdict line as it stands, unchanged, plus one line before it saying what this addendum got done.

Everything else in B961 stands. No merge, push, comment, Jira write, deploy or message.
