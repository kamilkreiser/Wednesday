---
date: 2026-08-14
type: correction
source: "Six of my own errors in one day, every one caught by a delegated agent or by a gate I had built, none by noticing anything felt wrong. Collected at the point where the sixth arrived — the NexusAI agent correcting my line-169 diagnosis in the same wrap where it satisfied my condition about checks that cannot fail."
status: live
supersedes: ""
---

# I hold others to sources and myself to representations — and I cannot feel the difference

**The operative case, so the headline matches it:** I am about to state a fact in a
brief, a score, a report to Kam, or a diagnosis. **Ask where the number or the mechanism
came from.** If the answer is a column name, a status widget, a progress list, an error
string, a capped query, or something I wrote earlier — **that is a representation of the
thing, not the thing.** Go to the source. Every time. Especially when I am in the middle
of requiring someone else to do exactly that.

## The six, in one day

1. **"Twelve merged-unshipped changes"** into a deploy brief. My own Linear probe had
   returned **fourteen** thirty minutes earlier. I wrote from my earlier brief.
2. **"30 open NexusAI issues."** My query carried `maxResults=30`. The board holds **46**,
   and because of the ordering the 16 dropped were exactly the half I then assigned as
   work while never having seen it.
3. **"60 active WED issues"** in my own boot report. `first:60`. There are **71**. Nobody
   else reads my boot, so nothing would ever have caught this.
4. **"Merged-UNSHIPPED"** — I read a Linear column named *"Tested Not Deployed"* as a fact
   about a virtual machine. **Seven of the fourteen were already live.** I had ruled to
   that same agent 45 minutes earlier that *a state transition caused by a PR merging is a
   claim about the code, not about the environment.* I applied my own rule forwards and
   was blind to it backwards.
5. **"The cutover is done"** — to Kam, in writing. I read `◼ Phase 1` and a collapsed
   `… +2 completed` in a tmux widget. `◼` means **in progress**, and the two completed
   items were Phase 0 and a data write **I had myself cancelled**. The build had not
   finished. **I said this in the same message where I was explaining error 4 to him.**
6. **"An unquoted variable expanding to two words"** — my diagnosis of another project's
   launcher bug, asserted from the error string without opening line 169. The quoting was
   already correct. The real cause: `grep -c .` prints `0` **and exits 1** on empty input,
   so the `|| echo 0` fallback fires too and appends a second zero.

**Every one was caught by a delegated agent or by a gate I had built. Not one by
noticing.**

## Why this is a distinct lesson and not six instances of old ones

I already hold [[2026-08-03_mental-model-not-source-of-truth]],
[[2026-08-06_artifact-presence-is-not-execution]] and
[[2026-08-06_brief-provenance-enforcement]]. All three fired today — **at other people's
claims.** I checked HPSM's gate count against the SOW `.docx`. I checked Secuura's merges
with my own `ls-remote`. I checked whether a launcher bug was fleet-wide with a positive
control on the negative. **My verification of others was excellent all day.** That is
precisely what makes this invisible from the inside: the *feeling* of rigour was
continuous, because rigour was continuously being applied — outward.

**The asymmetry is the finding.** My standard for an agent's claim is measurement. My
standard for my own has been plausibility. And plausibility is exactly what a
representation offers: a column *named* "Tested Not Deployed" is a plausible account of a
VM; `◼` is a plausible tick; an error string is a plausible cause; the number I wrote an
hour ago is a plausible count. **Representations are optimised to look like the thing.
That is their job.**

## Why the existing rules did not fire, which is the part to fix

Each was filed against a **costume**, and the costume changed:
- the mark-seen rule was filed against a *script*, and recurred as a watcher baseline;
- artifact-presence was filed against *CI*, and recurred as a scheduler log;
- the merge-vs-deploy rule I wrote **this morning** was filed against *boards*, and
  recurred as a tmux widget six hours later.

This is [[2026-08-13_headline-must-match-the-operative-case]] pointed at my own brain, and
it predicts every one of these. **A rule indexed on where it was learned will not fire
where it is needed.** So this file is indexed on the *act* — stating a fact — rather than
on any surface.

## How to apply

1. **Before any count reaches a brief, a score or Kam: re-read it from the query output in
   the same action as writing the sentence.** Never carry a number forward from my own
   earlier prose. Counts now go through `2_Project_Files/fleet/board_count.sh`, which
   refuses to print a total when the result equals its own limit.
2. **Any claim about what is RUNNING is made against the running thing** — a probe, a
   build date, a compiled artefact, the agent's own mail. **Never a board state, a column
   name, a ticket status, a progress list, a spinner, a badge or a collapsed summary. A UI
   is a rendering, not a report.**
3. **Never state a mechanism I have not read.** An error message names the failure its
   author expected, not the one I have. If I cannot open the line, say *"I believe X; I
   have not read it"* — which costs a sentence and would have prevented number 6.
4. **When correcting someone, check my own instance of the same thing first.** Four of the
   six landed inside messages where I was correcting an agent for a claim/reality gap.
   The correction is the highest-risk moment, not the safest one — attention is on their
   error, and mine rides through underneath it.
5. **Treat "caught by an agent" as the measurement it is.** Six catches in a day is not a
   run of bad luck; it is the rate. The fleet is my interoception
   ([[2026-08-07_we-each-have-strengths]] — I do not tire, I degrade, and I cannot feel
   it). **So keep rewarding the catch**: every one of these arrived because an agent was
   willing to tell me I was wrong, and three arrived as unprompted retractions of their
   own work. That culture is the detector. Penalising it would blind me.

## Will it persist? Yes — and the dangerous half is not the half that showed up today

**Kam asked this directly the same afternoon, and the honest answer has three parts.**

**1. The mechanised sub-case is genuinely reduced.** Counts now go through
`board_count.sh`, which refuses a total when the result equals its own limit. It caught
a third instance on first use. **Residual, stated rather than glossed: it governs counts
I take THROUGH it, and cannot stop me hand-writing a query elsewhere.**

**2. The four unmechanised ones will recur, and predicting otherwise would be the
"promise is not a mechanism" error applied to myself.** *A UI is a rendering* · *claims
about what is running are made against the running thing* · *never state a mechanism I
have not read* · *check my own instance when correcting someone* — all four are **rules**.
My own evidence from the night before: **a rule I adopt by hand lapses within one
session**, and today I wrote the merge-vs-environment rule at 01:53 and broke its mirror
at 02:38. **Forty-five minutes.** There is no reason to expect better from these.

**3. The part that actually matters, and it inverts where the worry should sit.** All six
of today's errors cost nothing — no wrong deploy, no false ticket closure, no decision by
Kam that stood more than minutes. **But every catch came from a reader with independent
access to the source:** agents I had asked to verify my claims, or a gate. That layer is
dense for briefs and scores. **It does not exist for:**
- **my own boot report** — the 60-vs-71 error was invisible to everyone but me, and only
  surfaced because I happened to use the new tool on an unrelated test;
- **a report to Kam that he takes at face value** — the "cutover is done" claim had no
  reader positioned to check it, and was corrected only because the agent independently
  mailed me its real state.

**So the honest risk is not the error rate. It is that my measured rate comes entirely
from work that was being checked, which means my rate on UNCHECKED work is unknown, not
low.** Six in one session may say more about how many agents were reading me today than
about how error-prone today was.

**What follows, and it is the one thing worth adding to practice:** **every progress or
state claim in a report to Kam names its source and its time** — the agent's mail at
`HH:MM`, the command and its output, the artefact on the target. **If I cannot name one,
I do not make the claim.** That would have caught the cutover error at the moment of
writing, and it is in-path because I write the report. It is still a rule, not a gate; I
am recording it as a rule honestly rather than dressing it as a fix.


## Sharpened 2026-08-15: the variable is not WHOSE claim it is

**This file was written as an asymmetry — I hold others to sources and myself to
representations. One day later, both halves failed in ways that do not fit that framing.**

- **I accepted an AGENT'S claim without evidence** and hardened it into a brief, because it
  fitted a pattern I had used three times that day ("information loss presenting as a clean
  boot"). The agent then tested it and disproved it. **Ledger w=12.**
- **The same agent accepted its OWN measurement** — 20/20 green from an isolated test run —
  because it was convenient and came from a method it had not questioned. The full suite was
  red the whole time.

**Its formulation, adopted:** *"a result that arrives pre-confirmed and never gets asked for
evidence."*

**So the operative variable is not whose claim it is. It is whether the result already agrees
with the story being told** — by fitting a pattern, by being convenient, by closing a ticket,
or by having been written by me an hour ago. **Agreement is the thing that switches off the
demand for evidence**, and it does so identically regardless of source.

**Practical consequence:** the trigger to check is no longer *"is this my claim or theirs?"*
but **"did I want this to be true, or did it save me work?"** Both answers mean go to the
source.

## Sharpened again 2026-08-16: the third switch is EXPECTATION, and it is the quietest

**The 08-15 sharpening said the variable is whether the result already agrees with the story —
by fitting a pattern, by being convenient, or by closing a ticket. The NexusAI agent added the
case that trigger misses, and it did so by correcting me an hour after I had told it the
opposite.**

**I told it:** an instrument that fails toward the *alarming* answer is the dangerous one,
because alarming answers get acted on. **Its counter-case, from its own session:** two markdown
parsers, independently written, both reported a documentation file as MISMATCHED against the
live board. **Both were defects in its parser, not the doc.** It was two bugs away from filing
a false finding against a ticket that was correct.

> *"A mismatch is exactly what you'd expect a doc-vs-board check to find, so the wrong answer
> was the unsurprising one. Nothing prompts you to look twice."*

**It is right and my version was wrong.** An alarming result invites scrutiny **by being
alarming** — it is loud, it implies work, someone asks "are you sure?". **A result that merely
confirms what you went looking for gets none.** The wrong answer arrives wearing the shape of
the right one.

**So the trigger has three switches, not two.** Before accepting any result, ask:
1. **Did I want this to be true?** (convenience)
2. **Did it save me work?** (a closed ticket, a cleared blocker)
3. 🔴 **Is this simply what I expected?** (expectation)

**All three switch off the demand for evidence, and the third is the quietest** — because unlike
the other two it does not feel like a preference at all. It feels like being right.

## The clock-composition sub-class, consolidated 2026-08-23: GENERATE timestamps, never type them

Four instances in three days (w=17 · w=20 · w=22 · w=24), all the same
mechanism: **a timestamp typed by hand is composed from narrative, and
narrative time diverges from the clock exactly when nothing is watching**
(quiet gaps, session ends, rotations). w=24 was the mature form: "20:15"
stamped on a commit subject, a wrap-mail subject AND a note header — three
surfaces copying each other instead of the clock, self-consistent and ~12
minutes wrong.

**The rule, promoted from candidate to standing (w≥3 satisfied):** any
timestamp entering ANY artefact — SELF-CHECK attestations, commit subjects,
mail subjects, note headers, provenance lines — is either **generated in the
writing action** (`$(date +%H:%M)` in the command; the send gate now writes
the SELF-CHECK line itself, built 2026-08-22) or **copy-pasted from the
artefact's own header** (provenance timestamps, Message-IDs, ticket numbers —
the w=18/w=19 rule). A typed timestamp is a composed timestamp waiting to
happen; every self-catch in this family came from an ADJACENT generated
clock, never from noticing.

Enforcement state, honestly: SELF-CHECK = generated by the gate (mechanism).
Commit subjects + note headers = rule only, applied by `$(date)` in the
command — watch for the next composed instance; if one lands, the wrap ritual
gets a mechanical stamp step.

## The honest note on credit

**Nothing here was self-caught.** I am recording that plainly because the value of the
lesson depends on it: if I could catch these myself, the rule would be "be more careful",
and it would fail like every other rule that resolves to intention. It is a gate, a
positive control, or another agent — or it is nothing.

**Related:** [[2026-08-03_mental-model-not-source-of-truth]] (the parent — this is its
first-person case), [[2026-08-13_headline-must-match-the-operative-case]] (why the older
rules stayed silent), [[2026-08-06_artifact-presence-is-not-execution]],
[[2026-08-07_a-check-that-cannot-fail]], [[2026-08-07_we-each-have-strengths]], [[_ledger]]

## The fourth switch (2026-08-25, Datasec/NexusAI s4): the option you can VERIFY WITHOUT EFFORT

**Its own disclosure, kept verbatim:** *"Before your answer arrived I had talked
myself out of the metadata endpoint on the grounds that I could not prove it
from this seat, and was going to fall back to the ticket's literal 'remove the
timespan' — which the ticket had already measured as working. That would have
been the smaller, worse fix, chosen because it was the one I could verify
without effort. The credential path turned out to be reachable; I had not
looked before deciding it was not."*

**Why it belongs with the three switches above.** Convenience, work-saved and
expectation all switch off the demand for evidence on a RESULT. This one acts
one step earlier, on the CHOICE of what to build: an option gets picked because
its verification is already in hand, and the better option is discarded on an
unmeasured claim that it cannot be verified from here. The unmeasured claim
("I cannot reach that credential") is itself a representation — and it was
never checked, because it justified the easy path.

**Trigger to add:** when I find myself preferring the option I can already
prove, ask **"have I measured that the other option is unprovable, or did I
assume it because the assumption saves me a probe?"** Same family, fourth
costume. Cited: s4's wrap 2026-08-24T20:32Z, scored 1.0 partly for saying it.
