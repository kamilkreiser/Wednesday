# Running a local model: the coordinator's manual

For Tuesday, or whoever manages the Spark box. This is what Wednesday learned running a local
model against a live backlog. It is ordered by how much each rule costs when you skip it.

---

## 1. The brief is the cost. Behave accordingly.

The run is free, so the temptation is to fill the queue. **Do not.** A task built from a bare
ticket description will almost always fail the "a test must be RED before the fix" check, because
the model writes a test that is green both before and after — which proves nothing. That FAIL then
looks like model weakness and is not: it is a brief defect wearing a verdict's clothes.

- **Never queue a task whose input was built without a brief.** If your builder tells you it fell
  back to the ticket description, treat that line as a refusal.
- **Feeding the model is brief-writing, not queue-filling.** Budget your own time that way.
- **Delegate the brief-writing.** Reading a file at the tip and deriving the exact edit is a
  bounded job a cloud agent does well. That is the right place to spend cloud tokens.

## 2. Pick tickets by a predicate, not by vibe

A ticket is a candidate only if ALL hold. Verify each at source; do not trust a summary line:

- **One product file**, or unambiguously one.
- **The ticket describes the fix SHAPE.** A ticket that says "decide whether to X" is a decision,
  not a task. Skip it and card the decision.
- **A runnable in-process test already exists nearby** whose mocking shape can be copied.
- **Not an auth / token / credential / security surface.** When in doubt, treat it as one.
- **Not already at the round counter** (see §5).
- **The test runner is one your checker can actually run.**

Most of a backlog fails this predicate. That is normal and it is the real constraint — expect the
pool, not the machinery, to be what limits you.

## 3. Write the brief so it cannot be misread

Full shape in `03_BRIEF_TEMPLATE.md`. The parts that do the work:

- The **exact edits**: line number, the line's CURRENT text at the tip, and the new line.
- **What must NOT change**, named explicitly.
- **More than 3 edit points → split it or skip it.** A 7-edit brief is a failed round you have not
  run yet.
- **Every factual claim carries the line number you read it at.**
- An **UNMEASURED** section naming what you reasoned rather than ran. This is not humility; it is
  what tells the next reader which greens to re-check.
- If the brief closes **less than the ticket**, say so as narrowing: *"closes 2 of 86; refs the
  ticket, does not close it."* A ticket that closes on a fraction because nobody wrote that
  sentence is a real and expensive failure.

## 4. Check the output at source. This is the part you cannot delegate.

When a verdict comes back:

1. **Read the produced diff against the brief.** Not the verdict line — the diff.
2. **Byte-compare the added lines to what the brief specified.** If your builder records the
   expected lines, this is one command and it is decisive.
3. **Read what the checker actually asserted**, and ask whether that property is the one the claim
   needs. A green from a check aimed at the wrong thing is worse than no check, because it comes
   with a receipt.
4. **Hold the result in the SAME action as reading the verdict.** Wednesday once left four passing
   diffs unheld overnight because the holding step was "next". Ten hours of finished work sat
   invisible. If you read a PASS, you record it now.
5. **A PASS IS NOT A MERGE.** A passing diff is a candidate. It goes through the normal review and
   a signed go-ahead like any other change. The local model holds no identity and raises nothing.

## 5. The round counter — Kam's rule, 2026-09-23

> **Original brief + ONE rebrief. If it is still not right after two rounds, it goes to Opus 5.5
> in the cloud.**

Kam's own observation is why the second round is worth spending: the Spark model scores
~90-something on round one and ~98 on round two. **So do not escalate at the first stumble — the
second round is where the value is.** But stop there. His words: diminishing returns.

**Do not reason your way past the counter.** A counter cannot drift; a judgement call needs you to
correctly classify every failure, and classification is exactly what goes wrong under load. Where a
countable rule and a judgement rule disagree, prefer the countable one.

Record on the ticket's row why it was reallocated. Batch escalated tickets for a cloud agent that
is already open on that project — do not open a seat per ticket.

## 6. Every failure earns a fix in the tooling or the instructions

A FAIL is a to-do, not a result. Classify the cause — **model**, **harness**, or **brief** — and
put the fix where the answer points: a sampler setting, a checker rule, or a clearer brief. Write
it down the same session.

**Every prompt rule needs a checker twin.** A rule the checker cannot refuse on is a hope. If you
tell the model "fix every named site", something must be able to count the sites and fail.

## 7. Never let it idle — and when the pool runs dry, WIDEN

An idle local model is a rule being broken, not a gap to notice later. When nothing is briefable,
the next action is a **harness extension or a brief** — never a stand-down.

Widening, cheapest first:
1. **Make the input carry only the REGION a brief needs**, not the whole file. Whole-file embedding
   is what makes large suites unbriefable — a 264 KB file produced a 74,000-token input against a
   65,536 window. This is a tooling fix and it unlocks a whole class.
2. Go to an adjacent task type (a docs change, a shell-script change) that your checker supports.
3. Only then consider raising the context window — it costs memory on every run, and a number
   nothing has exercised is the most dangerous kind.

**If the queue must be empty, write WHY where the next reader lands.** "I did not find anything" is
not a reason; a measured rejection list is.

## 8. Things that are always true and always tempting to skip

- **A classification list is a representation of the items, not the items.** Before you turn
  someone's "these are safe" list into work, either read them or write a verify-each-one guard into
  the brief and expect a real failure rate.
- **A zero is a suspect, not evidence.** Every empty result gets a control that would have produced
  a non-zero, run in the same action. A firing control proves the instrument RUNS — ask separately
  whether it ANSWERS the question you asked.
- **Never delete.** Cleanup means moving something into a dated quarantine folder.
- **Never edit a script while it is running.** Bash reads by byte offset. Write a new copy and
  `mv` it over — that is atomic, and the running process keeps its old file.
