---
date: 2026-08-06
type: correction
source: "w=2 promotion: (1) 08-05/06 CI-reds mis-attribution (suites were outcome=skipped boot casualties, no test ran); (2) 08-06 boot report claimed 'shift change fired its first live 05:30 this morning' from the log FILE's existence — the log's content showed the real fire was SKIPPED (coalesced to 09:25, window guard) and the tap lines were a dry-run test"
status: live
supersedes: ""
---

# Artifact presence is not execution — read the content, find what actually ran

**The failure class (two occurrences, two days):** I attributed an EVENT to an
ARTIFACT without confirming the event actually executed.

1. **CI-reds (08-05, caught by Secuura's evidence pass):** read a failing run's
   summary and blamed the Schemathesis/Akto suites — job logs showed
   `outcome=skipped`; the suites never ran. The red belonged to the FIRST
   failure (stack-boot image pull, GitHub secondary rate limit).
2. **Shift change (08-06, self-caught mid-session):** told Kam the 05:30 shift
   change "fired live this morning" because `shift_change_2026-08-06.log`
   existed. Its content: the real fire coalesced to 09:25 and was correctly
   SKIPPED by the window guard; the pane-tap lines were a `WEDNESDAY_TEST_HOUR`
   dry-run. Corrected in the same session's next report.

**Why the w=1 rule didn't prevent occurrence 2 (diagnosis):** the 08-05 rule was
logged ledger-row-only, framed as a CI rule ("confirm a suite ran before
attributing a red"). The root cause is broader than CI: **any artifact that a
process leaves behind (log file, stamp, summary status, green tick) is evidence
that SOMETHING wrote it — not that the event you care about happened.** A
CI-shaped rule didn't fire when the costume changed to a scheduler log.

**How to apply:**
1. Before claiming "X ran / X fired / X failed because of Y" — open the
   artifact and find the line that proves the specific event, not the file
   that surrounds it. For runs/pipelines: find the FIRST failure and check
   `outcome`/exit per step. For scheduled jobs: read the log body for the
   fire-vs-skip line, and distinguish real fires from tests/dry-runs.
2. Reports to Kam carry the proving line, not the artifact's name.
3. Same discipline in reverse: absence of an artifact is not absence of the
   event (it may log elsewhere, or the writer may have died mid-way).

**Related:** [[_ledger]], [[2026-08-03_mental-model-not-source-of-truth]],
[[2026-08-05_verify-the-chain-not-the-legs]]
