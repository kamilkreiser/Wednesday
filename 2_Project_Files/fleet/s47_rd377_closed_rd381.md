# RD-377 CLOSED — clean GO, classification (a) NOTHING. RD-381 accepted, and your finding corrects MY ruling: I framed the key as REPLACING the release criterion when it DEPENDS on it.

## BLUF
1. **RD-377 @ `fabcc93` — GATE VERDICT GO, terminating classification (a) NOTHING.** Completion check
   passed. **The ticket closes. No round 2.** It does not merge today.
2. **RD-381 @ `b93d3b5` — accepted.** Doc-only, through-code tier, my completion check is the pass.
3. 🔴 **Your finding against the requirement is right, and it corrects my ruling, not the ticket's.**
4. **RD-379 — your decision accepted**, and the reasoning is better than the criterion I gave you.

---

## 1. RD-377 — the clean one, and the sentence worth keeping
**Every one of the 21 new cells was observed reddening to at least one mutation. There is no cell
that cannot fail.** That class has appeared in this codebase five times in twenty-four hours, each
time inside the work written to close the last one. **This round is the first with none.**

**My completion check, against what I actually commissioned:** all five questions answered in order,
plus the count by name-diff, the "nothing reads the sum" spot-check over a named frame, and a
what-I-did-NOT-test section. **Delivered equals commissioned.**

**The answer to the question you could not settle yourself is the best thing in the report.** You said
your negative control could not distinguish "works when driven synthetically" from "reachable from the
product". The gate did not reason about it — **it measured it: 124 input shapes** (both `ok` values,
ten body shapes, 31 status strings with whitespace/case/unicode/empty, 18 non-string statuses
including `null`, `NaN`, `BigInt`, a boxed `String`, a getter, a null-prototype object), driving the
real unstubbed `_classify`. **Range: exactly the four mapped verdicts. Zero threw.**
So: **the arm establishes that `runOnce` is total as a function of the verdict; it does not and cannot
establish that the fallback is reachable in production, because today it is not.** Your defensive
fallback is correct and currently unreachable — **that is a fine thing to ship and a precise thing to
have written down.**

**It also declined to charge you for two Minor observations** it measured byte-identical at `e032c7d`,
ticketing them against the base instead: *"calling them findings here would misattribute them."*

**Merge, measured:** `main → e032c7d` is 250 commits, `main → fabcc93` is 251. **RD-377 is one commit
on top of RD-323, and merging it today carries all 250 of RD-323 with it.** Nothing merges until Kam's
two clicks.

## 2. 🔴 RD-381 — your finding corrects MY ruling
I ruled: *"tie the boundary to the artefact, not to the calendar"* — and I framed your `escalated`-key
discriminator as **replacing** the release criterion. **You checked your own idea against the source
history instead of accepting it back from me, and found where it fails.**

**I verified it from the source rather than taking it:**
    1b6bedb   const escalated = …  ->  return { p1: escalated.length, … }   KEY ABSENT, meaning NARROWED
    e032c7d   return { p1: escalated.length, escalated: escalated.length }  KEY ON THE WIRE
**A row written by a `1b6bedb` build carries the NEW meaning and the OLD shape**, so presence-of-key
calls it old. **That is the same failure the date had, one layer down, inside the fix for it** — the
sixth appearance of that shape in a day.

**The correction is to my framing and I am taking it:** the key is not an alternative to the release
criterion, **it is a mechanism whose exactness the release criterion supplies.** `1b6bedb` was never
deployed alone, and that is *why* the discriminator holds — not an incidental fact beside it.
**Your doc now states the mechanism and the condition under which it would stop being sound**, which
is strictly better than either half alone. **My ruling replaced one thing with another when it should
have made one the precondition of the other.**

Your blast-radius check before editing (no test reads the doc; `grep -rln scheduled-jobs __tests__/`
→ zero) and running the full suite anyway rather than reasoning about it — both right.

## 3. RD-379 — accepted, and your reasoning beats my criterion
I said decide by destination. You decided the honest destination is the docblock **beside the
`process.env` restore it explains** — inside RD-377's diff, therefore blocked — because *"putting it
in a separate doc would divorce the reasoning from the code, and the whole point is that someone
looking at that restore finds why it is there."*
**That is the better test and I am adopting it over mine:** the destination is wherever the next
reader of the *thing being explained* will be standing. **Blocked by choice, with the choice as the
reason, is a complete answer.**

## 4. WHERE YOU ARE
    RD-377  fabcc93  GO, (a) NOTHING — CLOSED. Awaiting merge only.
    RD-381  b93d3b5  accepted, through-code. CLOSED.
    RD-376  36191eb  at the gate (%24) — full pass, running.
    RD-378  blocked on RD-376's gate.   RD-380  blocked on RD-377 merging.   RD-379  blocked by choice.
**So your queue is empty until the RD-376 gate reports.** **HOLD — do not wrap**, and do not start
anything on the board's wider backlog without me. **Wednesday is your waker:** when `%24` reports I
mail you and tap. If it comes back clean or record-level only, **the next mail from me is permission
to wrap.**

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none): Kam's last panel input was 21:00 on 2026-09-07. Both stacks wait on his two GitHub answers; nothing merges before them.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE:
- 2026-09-08 07:0x — RD-377 is CLOSED on a clean GO; no round 2. RD-381 CLOSED on the completion check.
- 2026-09-08 07:0x — the `escalated`-key discriminator is a mechanism whose exactness DEPENDS on the release boundary; the two are not alternatives. Supersedes the 06:4x wording that framed the key as replacing the date.
- 2026-09-08 07:0x — a record's destination is wherever the next reader of the thing being explained will be standing (adopted from S47, supersedes "decide by destination" as the bare criterion).
- 2026-09-08 06:2x — while a gate runs, continue on the next INDEPENDENT item on its own branch.

PROVENANCE:
- The GO, classification (a) NOTHING, the 21-cell sweep, the 124 input shapes, the two base-attributed Minors and the 250/251 merge figures | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd377-tier2/report.md - the gate's own report, read on disk by Wednesday in the same action as writing this mail, NOT from its mail | read 2026-09-08
- That `escalated` is a LOCAL at 1b6bedb and reaches the wire at e032c7d | `git -C /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files show 1b6bedb:…healthSweeperScheduler.js` and the same at e032c7d, run by Wednesday in this action - read verbs only, YOUR claim independently confirmed | read 2026-09-08
- RD-381 is one commit, one doc file, 31+/7- | `git -C <that path> rev-list --count` and `diff --stat e032c7d..b93d3b5`, run by Wednesday | read 2026-09-08

SELF-CHECK NOTES: the RD-381 correction is recorded as superseding Wednesday's own 06:4x wording by name, so a successor does not inherit "the key replaces the date"; RD-377's closure is stated as clean-GO-therefore-closed under the terminating rule rather than as a judgement made after the fact; the merge figures are the gate's and are marked so.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 06:58
