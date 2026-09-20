---
date: 2026-09-20
type: correction
source: S71 (Datasec/NexusAI), self-reported after its suppression reddened main; the brief that caused it was Tuesday's
status: live
tier: W
---

# A control that runs in a different MODE from the one that will judge you proves less than it appears to — and it is worse than no control, because it buys the confidence to ship

**The lesson, in the agent's own words, adopted verbatim:**

> *"A control that runs in a different mode from the one that will judge you proves less than it
> appears to — and it is more dangerous than no control, because it buys confidence."*

**Executable form:** a control names the **MODE**, the **INVOKER** and the **REF SET** it ran
under. **The mode you verify in must be the mode the judge runs in.** Otherwise it is evidence
about a different instrument, presented as evidence about yours.

## The case

Rescuing an unversioned design document, an agent committed it to a branch. Gitleaks blocked the
commit on two placeholder secrets inside example ATTACK payloads. It handled that **well**: it
called them true positives rather than waving them off, suppressed **by fingerprint, never by
path**, and then — unprompted — **proved the suppression narrow with a canary**: it injected a
fresh secret into the same file, confirmed the scan still caught it, removed the canary, and
verified the file byte-identical. It reported all of that honestly, and it was true.

**Then main went red.**

CI checks out main with `fetch-depth: 0` and runs `gitleaks git .` — a **history scan across every
fetched ref**. The canary had run `gitleaks protect --staged`. History findings are keyed
`COMMIT:path:rule:line`; the suppression was written `path:rule:line`. Correct format for the mode
it was tested in; wrong format for the mode that judges.

**The control passed, and its passing is exactly what made the push feel safe.** No control at all
would have produced more caution.

## Two properties worth keeping on their own

1. **A BRANCH PUSH IS AN ACTION ON THE SHARED BOARD.** A leak on any branch reddens *main*, because
   the history scan sees every ref. The branch was never merged and may never be. Treating branch
   pushes as private is wrong wherever CI scans history — and the coordinator had explicitly called
   the branch "a rescue, not a change". It was not a change to the suite. It was a change to
   main's CI.
2. **Commit before a destructive control.** Running the canary, the agent `git reset --hard`'d with
   its fix still uncommitted and wiped it. It caught this because it **read the number** — "leaks
   found: 2" where clean was expected — instead of assuming the run had worked. Widened:
   **a destructive step runs against a committed tree, or in a scratch clone.**

## The coordinator's half, which is where this actually started

**Tuesday commissioned committing a 99,937-byte file it had never opened**, having measured only
its size and its path. A design document for an SSRF control is the single most likely place in a
repo to contain attack payloads with credential-shaped placeholders. That is
[[2026-08-04_validate-brief-pointers]] exactly: the brief validated that the file EXISTED and never
what it CONTAINED, and what it contained is what broke main.

**Rule: before commissioning a file into a scanned or built repo, ask what the tooling will SEE in
it** — not only whether it exists and where it goes. Same family as
[[2026-09-20_most-of-a-project-folder-is-outside-its-git-repo]] (naming a directory is naming a
behaviour) and the placement error in the same session.

## Why the existing lessons did not catch it

[[2026-08-07_a-check-that-cannot-fail]] asks whether a check CAN fail — this one could, and did,
on its canary. The 2026-09-08 false-absence family asks whether the instrument could return a
false zero — it could not; the staged scan was working perfectly. **Both rules were satisfied.
The control was sound, honest, and pointed at the wrong instrument.** That is a third axis, and it
is invisible to a question that only asks "did the control fire?".

The nearest neighbour is [[2026-08-06_local-proof-is-not-target-evidence]] — a green local proof is
not evidence about an environment that differs by design. This is its sharper sibling: **the
environments need not differ at all; only the INVOCATION MODE needs to.**

## SHARPENED THE SAME DAY BY THE SAME AGENT — a canary the ruleset does not TARGET is not a control, and a FAILED control is ambiguous

Kept here rather than in a new file (Kam's ruling (b), 2026-09-20: shrink the corpus).

**The case, hours after the one above, and it happened WHILE obeying a warning about the one
above.** Commissioned to scan a 143 KB file before committing it, the agent controlled its scanner
by planting `AKIAIOSFODNN7EXAMPLEKEY12345` and re-scanning. **Gitleaks reported clean on a file it
had just put a credential-looking string into.** First reading: *"so gitleaks is dead on this
file"*. Wrong. That string is not a valid AWS key shape, so **no rule targets it**. The canary was
invalid, not the scanner.

**Both available conclusions were false, and they fail in opposite directions:**
- Had it not controlled at all, it would have cited "gitleaks: no leaks found" as evidence — which
  is exactly the error that reddened main that morning.
- Had it stopped at the failed control, it would have reported the scanner broken — also false, and
  it would have blocked a correct commit.

It resolved instead: re-ran with a value this ruleset **demonstrably detects** (an
`azureOpenAIApiKey:"…"` assignment, the same rule that fired on the design doc that morning) —
canary → `leaks found: 1`, unmodified file → `no leaks found`. **Only then was the clean result
evidence.**

**The rule, in the agent's words:** *"A canary the ruleset does not target is not a control. A
control has to be a value the instrument is KNOWN to detect, or its silence means nothing — and a
failed control is ambiguous between 'instrument dead' and 'canary wrong', so it has to be
RESOLVED, not reported."*

**What this adds to the existing family.** [[2026-09-08_a-false-absence-is-usually-my-own-instrument]]
already says a control drawn from the wrong family agrees with the wrong answer, and that a control
which FIRES can still be the wrong instrument. This is the third face: **a control that does NOT
fire is not a verdict on the instrument — it is an unresolved question with two candidate causes,
and reporting either one without resolving it is a guess.** Same shape as
[[2026-09-10_a-two-answer-question-hides-a-third-state]], turned on the control itself.

**How to apply:** before a canary counts, name the RULE you expect it to trip and check that rule
exists. If the canary comes back clean, you have learned nothing yet — resolve which of the two
causes it is before you write a sentence either way.

## 🔴 THE w=3 ROOT — three of Tuesday's errors in ONE session, and they are one mistake

Recorded here rather than in a fourth file, because Kam's ruling (b) of 2026-09-20 says shrink the
corpus, and a root shared by three instances belongs in one place, not three.

| # | what was specified | the property measured | the property that actually governed |
|---|---|---|---|
| 1 | "put the cells in `__tests__/` or a clearly-marked staging path" | that the path EXISTS and is clearly marked | what **jest collects** there — no `testMatch`, no `roots`, so `docs/` and `qa-reports/` are collected. ~30 un-run cells would have armed. |
| 2 | "the design file belongs in the repo's docs" | its SIZE (99,937 B) and its PATH | what the file **CONTAINS** — two credential-shaped placeholders — and what gitleaks would see. Main went red. |
| 3 | "RD-464 r3 is released by the RD-545 merge" | that the predicate COUPLES them | what the coupling **MEANS** — a necessary condition, not a sufficient one. Two other holds survived. |

**THE ROOT, in one sentence: I specify using a property I measured, and the property that governs
is one I did not.** Existence, size, path and coupling are all cheap to measure, which is precisely
why they are the ones I reach for — and none of them is the property that decides the outcome.

**The failing-test treatment (w≥3):** before any instruction that names a PATH, a FILE or a
DEPENDENCY, write down the one sentence *"this will behave the way I expect because ___"* and fill
the blank with a property I have actually read — the config that governs that path, the contents of
that file, the clause that states that dependency. **If the blank can only be filled with
existence, size or location, I have not checked the governing property and the instruction is a
guess wearing a measurement's clothes.**

All three were caught by the receiving agent, not by me. That is the system working, and it is not
a substitute for the blank being filled.

## THE SECOND LAYER, same day: "I verified the part of the control I REMEMBERED" — twice, on one remedy

**The agent's own sentence, and it is the sharpest summary of this whole family:** *"I verified the
part of the control I remembered, twice."*

Having bypassed a pre-commit hook, it remedied the gap by running the leak scan over the commit
range — `gitleaks git . --log-opts <base>..HEAD` — and reported **"3 commits scanned"**. Asked
separately to enumerate what the hook actually did, it checked that number against `git log`, which
lists **FOUR**. **`git log` omits merge diffs by default, so the MERGE COMMIT was never scanned** —
and the merge commit was the only one containing its hand-written conflict resolutions. **The
content most likely to carry something new was exactly what the remedy skipped.**

**Two rules out of it:**
1. **A scan's COMMIT COUNT is checked against `git log`'s count.** A merge commit is assumed
   UNSCANNED until the flags say otherwise.
2. **A remedy for a skipped control is itself a control, and inherits every failure mode of one** —
   including covering the part you remembered. Ask what the ORIGINAL control's population was, and
   whether the remedy's population matches it.

## THE POPULATION IS THE TELL — `0 commits scanned` twice, once hollow and once correct

The same string appeared twice in one hour and meant opposite things. Post-commit, re-running a
`--staged` hook: `no leaks found`, **`0 commits scanned`** — an instrument with nothing to look at.
Pre-commit, running the same hook properly: `no leaks found`, `0 commits scanned` **and
`~1,108,039 bytes across 119 staged files`** — correct, because `--staged` scans the INDEX, not
commits.

**The words were identical; only the POPULATION SIZE distinguished them.** So: **a clean result is
only as good as the population it looked at, and a byte or file count is the cheapest way to see
that population.** Read it before believing a green.

## AND A NOTE ON INSTRUCTIONS BUILT ON A WRONG PREMISE

The instruction that exposed all of the above was **wrong**: the coordinator asserted the hook must
do more than gitleaks (lint, mode checks, a counts guard). **It does not — it is entirely a gitleaks
wrapper.** The instruction paid anyway, because it commissioned a **MEASUREMENT** ("read it, list
what it checks") rather than an **ACTION** ("it does Y, so do Z").

**Rule: when unsure, commission the measurement, never the action.** A wrong premise that sends
someone to look still returns the world; a wrong premise that sends them to DO returns wasted work
and a false sense that the gap is closed.

## How to apply

1. Before trusting any control, write down the **exact command the judge runs**, and run that.
   `protect --staged` vs `git .` vs `dir .` are three instruments wearing one tool's name.
2. When a suppression, ignore-file or allowlist is involved, **check its key format against the
   mode that will read it** — history findings, staged findings and directory findings are keyed
   differently by the same tool.
3. **A control's report names its mode.** "I proved the suppression narrow" is not a claim; "I
   proved it narrow under `gitleaks protect --staged`" is, and it is the version that would have
   exposed this before the push.
4. This generalises past scanners: test runners with different collection roots, linters in
   `--fix` vs check mode, CI matrices that differ from local, `npm ci` vs `npm install`.
