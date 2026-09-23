# Setup: paste this into the local Tuesday agent

Kam pastes **the block below** into the agent that will manage the Spark box. Everything after it
is the runbook that block refers to. The block is written to be self-contained: it assumes the
agent has this folder and nothing else.

---

## THE PASTE-IN BLOCK

```
You are taking over management of a local coding model running on an HP Spark box. Your job is to
stand up the working loop and PROVE it works before any real ticket goes near it.

Read these first, in this order, from the spark-kit folder you have been given:
  README.md                      — what this is and where each file goes
  02_FOR_THE_COORDINATOR.md      — your manual; this is the one you operate by
  03_BRIEF_TEMPLATE.md           — the brief shape you will fill in every time
  04_KNOWN_FAILURE_MODES.md      — what this class of model gets wrong

Then do the SETUP, in order, and do not skip the smoke test:

1. PLACE THE FILES. Put 01_FOR_THE_LOCAL_MODEL.md where your runner injects a system prompt, or
   arrange for its contents to head every task you send. Keep 02/03/04 where you can read them.

2. ESTABLISH WHAT THE BOX ALREADY HAS. Do not assume and do not invent. Find out, and write down
   what you found: how the model is invoked; whether anything already applies a patch and runs
   tests; where a working copy of the target repository lives; how much context the model is
   configured for. If any of these does not exist, say so plainly — that is a finding, not a
   failure.

3. BUILD OR IDENTIFY A CHECKER that satisfies the CONTRACT in the runbook section "What a checker
   must assert". A result from a checker that does not satisfy every clause does not mean anything,
   and you must not report it as a pass.

4. RUN THE SMOKE TEST in the runbook before any real work. It uses a deliberately trivial change
   whose answer you already know. Its purpose is to prove the loop is wired, not to test the model.

5. REPORT BACK to Kam: what you found on the box, what you built, the smoke test result, and every
   contract clause you could NOT satisfy with the reason. Do not paper over a missing clause.

Rules that bind you from the moment you start:
- The run is free; the BRIEF is the entire cost. Never queue a task built from a bare ticket
  description.
- Original brief plus ONE rebrief. If it is still not right, the ticket goes to Opus 5.5 in the
  cloud. This is a counter, not a judgement — do not reason past it.
- A PASS is a candidate, never a merge. The local model holds no identity and raises nothing.
- Read every produced diff against the brief yourself. That check is not delegable.
- Never delete anything; move it to a dated quarantine folder.
- Never edit a script while it is running.
- When you cannot do something, say so and stop. A refusal costs minutes; a confident wrong
  result costs a person's afternoon.
```

---

# RUNBOOK

## What a checker must assert

**This is the load-bearing section of the whole kit.** A "pass" means nothing unless every clause
below was actually checked. If your harness cannot do one of these, report it rather than
substituting something weaker.

1. **The diff applies to the real file at a known commit.** Record WHICH apply mode succeeded —
   strict, or with a recount. **Never report "applies cleanly" when only a recount worked.**
2. **The added lines are the lines the brief specified**, compared byte for byte. If the brief
   records the expected lines, this is one comparison and it is decisive.
3. **The touched-file set is exactly what the brief named.** A diff that changes an unnamed file
   fails, even with green tests.
4. **A test that should FAIL before the change DOES fail.** Break the thing deliberately, confirm
   red, restore, confirm green. **Without this clause a green result is worthless** — it is the
   difference between a test and a decoration.
5. **The rest of the suite is no worse than before.** Record the before and after counts.
6. **Every assertion's own output is kept**, so a human can re-read what was claimed.

## The smoke test — run this before any real ticket

**Purpose: prove the loop is wired. It is not a test of the model.**

1. Pick a file in the target repository that no one is working on, and a change whose answer you
   already know and can verify by eye — adding one comment line is ideal.
2. Write a brief for it using `03_BRIEF_TEMPLATE.md`, filling in **every** heading. If a heading has
   no content, that tells you something about your setup.
3. Run it. Then check, by hand, all six contract clauses above.
4. **Now deliberately break it twice, and confirm the harness NOTICES both times:**
   - Change the brief's expected line so it no longer matches what the model will produce. Clause 2
     must fail. **If it passes, your comparison is not running.**
   - Point the brief at a line number that does not exist. Clause 1 must fail. **If it passes, your
     apply step is not really applying.**
5. Only when both deliberate breaks are caught is the loop trustworthy. **A harness that cannot
   fail has told you nothing.**

## What to report to Kam when setup is done

- What was already on the box, and what you had to build.
- The smoke test: the trivial change, the six clauses, and the two deliberate breaks with their
  results.
- **Every contract clause you could not satisfy, named, with why.**
- Your first three candidate tickets and, for each, one clause of why it fits the predicate in
  `02_FOR_THE_COORDINATOR.md` §2.
- Anything about the box that contradicts this kit. **The kit was written against different
  hardware and a smaller model; where it is wrong, the box is right and the kit should be amended.**

## What is NOT in this kit, and why

The fleet that produced this method has its own harness — input builders, checkers, a queue runner,
a holding step. **Those scripts are not shipped here.** They live in another project's tree and are
shaped around that project's repository layout, test runners and ticket board; dropping them onto a
different box and a different codebase would import assumptions rather than method. What travels is
the contract above, which is what those scripts exist to satisfy.

**If Kam wants the reference implementation ported across, that is his call to make** — it crosses
between project trees, and this agent should ask rather than assume.
