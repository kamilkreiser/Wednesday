---
date: 2026-09-10
type: principle
source: s171's wrap formulation, 2026-09-10 22:20 — adopted verbatim as the unifying shape of six instrument failures in one session
status: live
tier: W
---

# When a question has two candidate answers, ask whether the instrument can produce a THIRD — and the third is almost always "the measurement did not happen"

**s171's formulation, adopted because it is better than mine:**

> *"When a comparison has two candidate answers, check whether the instrument can produce a third.
> Develop could not FAIL step 10; it could only SKIP it, and skip was invisible at the altitude the
> question was asked. In all three cases the third state was 'the measurement did not happen', and
> only a control could tell it apart from 'the measurement came back empty.'"*

**The lesson:** a two-way question — *did it pass or fail? is it there or not? did the ignore work or
not?* — silently assumes the instrument can only return those two. **It usually cannot. It can also
return nothing-happened, and nothing-happened wears the costume of one of the two real answers.**

**Why it matters more than the individual bugs:** every one of the six instances below was a
*confident* wrong answer, and in four of them the wrong answer was about to be relayed to someone
else — a coordinator, a principal, or a client.

## Six instances, one session (2026-09-10)

| the two-way question | the third state | what it looked like |
|---|---|---|
| Does `Run Playwright API tests` fail on the PR **or** on develop? | develop **SKIPS** it — its static gate fails at step 6, so 7-10 never run | "fails on both, dismiss" at job altitude; "only on the PR, blame the author" at step altitude. **Both wrong** |
| Is the KS board empty **or** populated? | the query hit **the wrong workspace** | `TOTAL=0` *with the tool's own "this is a real count, not a cap" attached* |
| Did the NAS ignore work **or** not? | the run **had not started copying yet** | zero copy lines — a check that could not fail |
| Are there Secuura paths in the scan log **or** not? | `grep -c` counted **one enormous carriage-return line** | positive control returned 1 and 0 |
| Did Actions run on these PR heads **or** not? | the SHA was **abbreviated**, so the filter matched nothing | zero runs, no error — one keystroke from reporting a hypothesis refuted |
| Is `X` documented in `ENVIRONMENT-VARIABLES.md` **or** not? | **wrong path** — the file is not there | zero hits for every variable |

**And a seventh of a different flavour, same root:** KS-1067's ticket text said *"three systemTest
locks"*. There are **four**. Anyone checking "are the three fixed?" gets a correct yes and a wrong
conclusion. **The frame excluded the answer, and the frame came from the artefact.**

## How to apply

1. **Before running a two-way check, name the third state out loud.** *"What would this return if the
   measurement simply did not happen?"* If that is indistinguishable from one of your two answers,
   **the check is not yet a check.**
2. **A control is the only thing that separates them.** Not a better query — a control. Positive
   (something that MUST be found) and, where you can, discriminating (something that must NOT be).
   **Run it before you want the answer**, because a control written after you have a result is
   written to agree with it.
3. **Ask the question at the altitude where the third state is visible.** Job-level hid a skipped
   step. Line-count hid a file with no newlines. **If the altitude cannot express "did not happen",
   go one level down.**
4. **Enumerate rather than verify a list.** The fourth lockfile was found by `git ls-tree` for *all*
   locks, not by checking the three the ticket named. **A list you were handed is a frame; the
   universe is not obliged to fit it.**
5. **Hardest and most valuable: this applies to questions you WRITE, not just ones you answer.** The
   Playwright instance began as *my* instruction — *"establish whether it fails because of this
   change, or was already failing on develop"* — written as though those were exhaustive. **A brief
   that offers two options teaches the reader there are two.** Where the answer might be a third
   thing, say so: *"or tell me it is neither."*

## Related

[[2026-09-08_a-false-absence-is-usually-my-own-instrument]] — the parent; this names the specific
mechanism by which an absence is manufactured.
[[2026-08-07_a-check-that-cannot-fail]] · [[2026-09-10_surprising-measurements-are-selector-errors]] ·
[[2026-09-07_a-census-complete-over-a-frame-that-is-not]] (the frame half of instance seven) ·
[[2026-08-15_a-cap-is-never-neutral]] · [[2026-09-08_the-check-ran-and-was-not-checking-the-thing]]
