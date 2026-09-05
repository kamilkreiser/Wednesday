---
date: 2026-08-06
type: correction
source: "w=2 promotion: (1) 08-05/06 CI-reds mis-attribution (suites were outcome=skipped boot casualties, no test ran); (2) 08-06 boot report claimed 'shift change fired its first live 05:30 this morning' from the log FILE's existence — the log's content showed the real fire was SKIPPED (coalesced to 09:25, window guard) and the tap lines were a dry-run test"
status: live
supersedes: ""
tier: M
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


## A PANE IS NOT A TURN, AND A TURN IS NOT THE COMMISSIONED TURN (2026-09-04 — correcting Wednesday's own launch-verification rule)

**The operative case:** Wednesday has just launched an agent and is about to say it is working on X. **A non-zero `ctx` on that pane proves A turn ran. It does not prove the turn you commissioned ran.**

**The case.** The QA agent was launched with `ultrathink` and its prompt as two positional arguments; Claude Code takes the first positional as the prompt, so the agent booted on the literal word `ultrathink`, fell back to its own project rules and sat asking for a URL and test credentials. **Its statusline read `ctx:4%` — completely truthful, and completely useless: the turn it measured was the agent asking a question nobody was going to answer.** Wednesday had already mailed another agent that the pass was running and pinned its branch on that basis.

**The rule this corrects is Wednesday's own** (2026-09-04, the launch-receipt row): *"a receipt for a LAUNCHED agent is written from the agent's own first artefact — a report path, a boot mail, a non-zero ctx."* **The non-zero ctx does not belong in that list.** The escalation ladder of launch evidence, weakest to strongest:

1. **The launcher's exit code** — proves a process started. Worthless. (This is the 2026-09-04 w=4 row.)
2. **A pane exists** — proves tmux did its job.
3. **`ctx:-`** — genuinely informative in ONE direction: no turn has run at all. That half holds.
4. **A non-zero ctx** — a turn ran. **Says nothing about WHICH turn.** This is the rung that was wrongly trusted.
5. **The pane's CONTENT showing the commission was received** — the agent naming the ticket, opening the brief, reading the SHA. **This is the first rung that discriminates.**
6. **The agent's own outbound artefact** — a boot mail, a plan confirmation, a report path.

**How to apply:**
1. **Verify a launch at rung 5 or 6, never below.** Grep the pane for something only the commissioned agent would produce — the ticket id, the brief path, the SHA under test.
2. **Put the discriminator in the LAUNCHER, not in the checking.** The wrapper now refuses to start unless the prompt begins with the thinking directive and names the brief path — both clauses red-proofed individually. A blind agent should be unlaunchable, not merely detectable.
3. **The same asymmetry as everywhere else in this file:** absence of a turn is strong evidence; presence of a turn is weak evidence. `ctx:-` means something; `ctx:4%` means almost nothing.

**Related:** [[_ledger]], [[2026-08-03_mental-model-not-source-of-truth]],
[[2026-08-05_verify-the-chain-not-the-legs]]
