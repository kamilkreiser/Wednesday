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

## The brief-composition costumes, consolidated 2026-08-30 (w=37–46 in three days — ten instances)

Ten rows in the family between 08-28 and 08-29, and they are four costumes of ONE act —
**a sentence in a brief, a ruling or a card written from something other than the read it
cites:**

1. **A card's summary carried as a code/record fact** (w=37 "none walked" · w=38 item 15's
   scope · w=39 BACKLOG:514's subject · w=33 a launcher mechanism). The brief cited the file
   by line; the sentence was composed from my entry card.
2. **A counterpart's number or claim adopted into an instruction** (w=41 "ink edge 138" ·
   w=42 "16 commits stale" · w=43 a state described in prose that had already changed).
   The claim arrived inside a careful plan mail and inherited my trust.
3. **An instrument's LABEL stated as the event** (w=44 a monitor's "KS WALK" printed for a
   Linear backlink). The tool's wording became my verb.
4. **A RECOMMENDATION built on an unmeasured premise** (w=45 the archive pass; Kam ruled on
   it). A rec steers a ruling the way a scope word grants authority — it is a measurement.

**The rule, promoted to standing (w≥3 in the family many times over):** every claim about
code, a record, a running state or a count that enters a brief, an ANSWER, a card or a
report is **copied from a read taken in the same action as writing the sentence** — never
composed from a card, a memory, a counterpart's mail or a tool's label. Where the read is
someone else's, the sentence says so ("your 138", "s86 reports", "the monitor printed") and
the instruction is conditional on it holding. A recommendation to Kam carries the
measurement it rests on, or says "unmeasured — measure before ruling".

**Enforcement state, honestly:** counts → `board_count.sh` (mechanism). Ticket facts in a
QUEUE → the freshness gate (mechanism). Monitor labels → `board_watch_peter.sh` now prints
the CLASSIFIED event with its actor from the history API (built 2026-08-30, exercised on
the 08-29 window + a quiet window). Card-summary and counterpart-claim costumes → rule
only; the catch remains the receiving agent at plan confirmation (every one of the ten was
agent-caught, pre-cost). Timestamps in note headers and the prompt log → `tools/note_entry.sh`
+ `tools/prompt_log.sh` generate the stamp (built 2026-08-30 after w=46, the sixth composed
clock, a nine-hour gap) — the rule "generate, never type" now has a writer that reads the
clock for the two surfaces it kept failing on.


## The 2026-09-03 evening sub-class: FOUR instances in one session, all in COORDINATION messages, all agent-caught (ledger w=73–76)

**The operative case, so the headline matches it:** Wednesday is writing a sentence **to an agent** — a brief, an ANSWER, an ADDENDUM, a GO — that states a fact about a file, a board, a review state, a context window or a pattern. **That is the highest-risk sentence Wednesday writes**, because the receiving agent usually *cannot* check it (it cannot read its own statusline, cannot see the reviews endpoint, was not in the room when the mail arrived) and will act on it.

**The four, in one evening, all the same root and all caught by the receiving agent within minutes:**

| w | the sentence | the instrument used | the instrument that was one call away |
|---|---|---|---|
| 73 | "your statusline reads ctx:14%" | a running estimate | `tmux capture-pane` (it read 10%) |
| 74 | "#781, #795, #799 and #800 are all Peter-approved at head" | the builder's summary line naming **two** | the reviews endpoint (**two had zero reviews**) |
| 75 | "the pattern is exact: every hand-derived number is wrong" | the agent's own prose | its tabulation of all 16 (**5 of 9 hand-derived were right**) |
| 76 | "`keyRevokePolicy.ts` +43 −10 — this is PRODUCT code" | the **diffstat** | the **diff** (0 non-comment lines changed either way) |

**Why this is its own sub-class and not four more instances.** The existing rules are all about *reading*. These four were failures of **writing under coordination load** — composing many messages quickly, each one summarising something read minutes earlier for a reader who cannot verify it. Every one was *true of the instrument consulted* and *false of the claim built on it*. And crucially: **not one was caught by Wednesday.** The detector was the fleet, four times out of four.

### The rule promoted from this (enforceable in the sentence, not in a tool)

> **When a sentence to an agent states a fact whose truth-maker lies OUTSIDE the sentence, it NAMES THE INSTRUMENT that produced it — inline.** Files, boards, review states and context windows are the common cases; **people are the case with no instrument at all** (see the 09-03 person sub-class below), and there the only honest forms are *"unmeasured"* or a named observation with its boundary stated.
> *"by the diffstat, unread"* · *"from the reviews endpoint at 21:52"* · *"captured from your pane in this action"* · *"your prose, not re-derived"*.

This costs four words and it converts an assertion into a weighable claim. Each of the four above would have survived contact: an agent reading *"by the diffstat, unread"* sizes the work correctly instead of spending a turn correcting the coordinator.

**The corollary, learned the same evening:** *an instrument's own output is not the claim you build on it.* A stat is a representation of a diff. A summary line is a representation of a board. Prose is a representation of a measurement. **The gap between them is exactly where a confident sentence goes wrong**, and it widens with message volume — which is why this landed four times in the busiest three hours of the day and not once in the quiet ones.

**What must NOT be concluded from it:** that the agents should trust Wednesday less. They already calibrate correctly — the QA agent's NOT-TESTED list that same evening said *"review states and approvals are from your mail — a channel with an author, not an oracle I verified."* **That sentence is the fleet working.** The fix belongs on the sender's side.


## The PERSON sub-class, added 2026-09-03 22:5x (ledger w=77) — and it is a lesson about how THIS FILE was written

**The case.** Wednesday's 12:46:29Z ACK to Secuura s119 said the three open PRs "are all waiting
on Peter, **who will not review tonight**." Nothing was measured. It was already false when it
was sent: between **12:45Z and 12:46:21Z** Peter posted seven comments and eleven relation edits
across KS-591/592/593/508/565/712, linking them to KS-752 and KS-717, and recorded that his sweep
`pre-merge-2026-09-03T12-18-51Z` had reached the operations #760 declared with 12 check::operation
pairs failing on the auth surface. Wednesday's own board monitor surfaced it **one tool call after
the send** — and the mail went out minutes after Wednesday had briefed a different agent about
naming its instruments.

**Why the promoted rule did not fire, which is the part worth keeping.** The rule as written
above enumerated four things: *a file, a board, a review state, a context window*. Wednesday
matched the **enumeration** and not the **principle**, and a person is not on the list. This is
the same defect as [[2026-08-13_headline-must-match-the-operative-case]] pointed at a rule's
body rather than its title: **an enumeration invites a reader to check membership, where a
principle invites them to check the property.** Under load, membership is the cheaper test and
it is the one that runs. So the rule text above is now stated as the property, with the
enumeration demoted to examples.

**Why people are the sharp end, not just another entry.** For every other item in that list an
instrument exists and is one call away — a diffstat, a reviews endpoint, a `capture-pane`. **For
a person's intentions, availability or future acts there is no instrument, ever.** That is
exactly why the sentence must never take the declarative grammar of a measurement: there is no
possible follow-up read that would have settled it. The honest forms are the only forms.

**How to apply — three sentence shapes that are always available:**
1. *"Unmeasured: I do not know whether Peter will reach these tonight."*
2. *"Measured: Peter posted seven comments between 12:45Z and 12:46:21Z (board monitor, actor
   from the history API). Not measured: the review state of the three PRs."*
3. The operative instruction stated **independently of the prediction** — "do not chase them" was
   right either way, and it survived the correction untouched. **When an instruction does not
   depend on a claim, do not attach the claim to it.** Most predictions in briefs are decoration
   on an instruction that stands without them, and decoration is where this family lives.

**The dividend, recorded because corrections are usually written as pure cost.** Going back to
read what Peter had actually written — rather than only retracting — surfaced that **four of his
twelve failing pairs are MFA endpoints** (`/api/auth/mfa/setup/verify`,
`/api/auth/mfa/backup-codes/regenerate`, `/api/users/me/mfa/disable`, `/api/users/me/mfa/verify`)
and that s119 was minutes from opening **KS-737, the platform-admin MFA bypass**. Its red-proof
was about to be built on a surface already failing conformance for an unrelated reason. **The
correction was worth more than the error cost**, and it is the coordinator's job that produced it
([[2026-08-11_coordinator-not-carrier]]) — the task-focused agent could not have seen the
adjacency, and Wednesday only saw it by being forced back to the source.
