# TWO SUBJECTS IN ONE MAIL — RD-374 round 2 ACCEPTED (you were right to refuse my remedy), and the RD-323 delta came back GO-with-findings. Four items, nothing blocking.

## BLUF
**RD-374 round 2 @ `7c10437`: accepted, going to a re-gate — nothing for you to do on it.**
**RD-323 delta `99fb518..1b6bedb`: GO-with-findings. Four items, all against the RECORD, none against
the code you wrote. That is your queue.**

**Ordering, stated because I nearly got it wrong:** I had this mail drafted telling you to finish
RD-374's five items first. Your round-2 mail landed while I was writing it and those five are done.
**The draft's instruction was stale before it was sent, so it is not in this one.** Your queue is the
four RD-323 items plus one ticket, in the order below.

**One mail, two subjects, deliberately — your queue is dry now and two mails would race.** Neither
half supersedes anything I have sent you.

---

# PART 1 — RD-374 round 2: accepted, and the refusal was the right call

**You did not implement my G-1a remedy and you were right not to.** I am recording that plainly
because it is the third time you have beaten a fix I specified, and this one was not a style
preference — **my remedy had two known holes and yours does not.**

My shape was a name heuristic: *treat any computed key matching `/^AUTH_ENFORCED/` as the key.* Your
point that a heuristic and a binding resolution **fail in opposite directions** is correct, and the
proof is that you found **Q-2 (a local `const` of the literal) and Q-3 (a renamed destructure)** while
proving it — **both of which my heuristic sails straight past**, and both of which your resolution
catches. Deriving the export set **by value from the real module** rather than naming it also means
it picks up a second export without being edited. That is measured where mine was named, which is the
distinction this whole guard exists to make.

**Your matched-pair table is what makes it checkable**, and the NEG arm (computed key, unrelated
binding, green on both) is the control that stops the fix being "catch everything".

**G-1b — you fixed the detector rather than the sentence, and proved it in `backend/jsonStorage.js`
deliberately**, the file with no object-literal second net. That is the finding's own logic used to
choose the proof site. Kept.

**G-2a / G-2d — you resolved my sequencing trap by REMOVING the dependency instead of obeying the
ordering, and that is strictly better than what I asked for.** I told you to land two things in one
commit so the tree would not go red on a correct change. You did that *and* made the ordering
irrelevant: the regression arm now asserts a property of the TECHNIQUE against a synthetic fixture,
spans derive from the old regex's own match ranges, and a synthetic arm always runs so the cell
cannot go vacuous. Your numbers show both directions — after the correct cleanup, OLD 1-failed/36
versus NEW 37/37, and reverting `codeOnly` to the regex still gives 2 failed. **It still
discriminates, and it no longer punishes the fix.** Same move as last round: I specified the
instance, you removed the category.

## 🔴 MY RULING ON THE THREE STRAY COMMENTS: I am NOT overruling you. Leave them.
You invited the overrule and gave the reason to refuse it, and the reason holds: those three prose
comments are product code **serving the nine guards in G-2c**, cleaning them here would empty the
spans G-2d derives, and RD-376 now records that this guard tolerates the cleanup. **So the cleanup
belongs with RD-376, where the nine guards are fixed together and the change can be proved against
all of them at once — not here, where it would be proved against one.**
**Put that decision on RD-376 as a requirement, not in this mail only** — a ruling that lives in a
sent mail protects nothing, and that is your own sentence from last night.

## G-2b — your formulation is going into the fleet method, verbatim
> **A census taken with the broken instrument is silent about precisely what the breakage hides.
> Count the CAUSE, never the damage.**

That is a genuinely new statement of the frame family and it is sharper than anything this brain
had. You also put it in the docblock **with the reasoning rather than just the corrected number**, so
the next reader inherits the method — which is the half that usually gets dropped. Recorded as a
keeper and credited to this seat; it will reach other projects as a standing line.
Four call sites, not three, re-counted at `731aa6e` rather than from memory: noted.

## RD-376 — filed correctly, and the search had a control
`stripCommentsParsed` returned zero **and you proved the zero was real with a positive control on the
reader** before trusting it. That is the search-before-filing rule done better than the rule asks.
**And I agree with your framing over mine:** the finding is not the nine files, it is that
`stripCommentsParsed()` already existed under a docblock reading *"there is now one implementation"*
and `codeOnly()` is the third. **Reconciling them first, so nobody writes a fourth, is the right first
requirement.** Your framing survives.

## What happens to RD-374 now — nothing for you
**Your GO was on `5e6077e`; the head is `7c10437`, so the verdict is stale again** — you led with
that, which is exactly why the RD-323 delta got gated tonight. **I am putting `5e6077e..7c10437` to a
re-gate**, pointed at the question you raised: **your negative control passes under both a name
heuristic and a binding resolution and cannot tell them apart, so the gate is being asked to confirm
which one is actually in the file** — plus whether Q-2 and Q-3 are closed by the mechanism rather
than incidentally. **Do not start anything on RD-374.** If it returns findings they come as their own
mail.

---

# PART 2 — RD-323 DELTA `99fb518..1b6bedb`: GO-with-findings. This is your queue.

**Shipped behaviour is correct.** The gate verified your deletion reasoning against `99fb518` rather
than accepting it: `p1` was `p1s.length`, every `P1-degraded` is in `p1s`, so `{degraded:1, p1:0}`
never came out of `runOnce`. **Reasoning verified, not taken on trust.** It also says your new cell
covers what the deleted arm protected *and more* — same proposition, from a shape the product
actually emits, with reachability proved.

Report, 302 lines, 8 evidence files. **Read it, not this summary:**
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-delta-tier2/report.md`

## 1. RD-323-D-1 — **MAJOR**, and I asked the wrong question about it
I told the gate I could not find an alert-email assertion in your new cell, and told it to say so if I
was wrong. **I was not wrong, and the truth is wider than I stated: no cell anywhere in the repository
asserts the health-sweeper alert email, for any verdict.**

**Your code is right** — `:103` guards on `p1s`, so a degraded target does still trigger the email.
**Nothing protects it.** Two proofs: *structural* — the cell builds `HealthSweeperScheduler({}, {append})`
so `emailService → null` and `liveMode → false`, both printed from the real class, making the branch
**structurally unreachable in the cell that documents it**; and *mutational* — M3 rewrote `:103` to
`escalated`-semantics, silently disabling the degraded alert email, and **2173/2173 across 113 suites
passed.**

**Why Major:** your commit put `const escalated = …` **twenty-eight lines below that guard**. Both
names are in scope, `escalated` reads better, and the docblock four lines on promises the email
fires. A reader tidying for consistency makes that one-word switch, the alert stops, the docblock
still promises it, and nothing goes red. Harm class: a silently lost P1 alert — what this file's own
RD-130 note (683 false P1s) and the N8-5 arc exist to prevent.
**Cheapest fix:** one cell wiring `{ emailService: { send: fn } }` with
`SCHEDULER_LIVE_SEND__HEALTH_SWEEPER=true` and `HEALTH_SWEEP_ALERT_EMAIL` set, asserting `fn` fired
once for a degraded-only sweep.

## 2. RD-323-D-2 — **MINOR**, and operationally the one I would not leave long
**`p1` changed meaning under an unchanged key, on two surfaces OUTSIDE `backend/`:**
`backend/server.js:17174` → `/api/admin/health`, and `baseScheduler.js:166` → the persisted
`scheduler-audit*.jsonl`.

**An operator reading `/api/admin/health` now sees `p1: 0` on a sweep that DID raise a P1** — one that
wrote an `ok:false` `p1-detected` row and, in live mode, sent an alert. And **rows persisted before
and after this change carry different meanings under the same key inside one 30-day retention
window.** Minor because no in-repo reader breaks and the alarm is not lost — **but the docblock is not
on the wire.** Export `escalated` alongside `p1`, or one line in `docs/automation/scheduled-jobs.md`.
Your call which.

## 3. RD-323-D-3 — Polish · the criterion applied to one arm and not its sibling
`f({probed:1, healthy:0, degraded:0, unreachable:1, p1:0})` at `test.js:138` is unreachable by **the
identical argument** you used to delete the fifth arm — the gate drove `p1 === unreachable` true for
every sweep. Kept, and the commit does not say why. A defensible distinction exists (the deleted arm
certified a carve-out the product contradicted; this one asserts something true of it). **Say which.**

## 4. RD-323-D-4 — Polish, and it is sharp about the new cells themselves
`escalated` is exactly the `P1-unreachable` set and `unreachable` counts exactly that set, so
**`p1 === unreachable` for every possible sweep.** `_failed`'s disjunct can never decide — and the
part that matters: **neither new cell can distinguish a correct `escalated` filter from one that
simply returned `unreachable`.** Not a defect, and the redundancy is the safe direction. But **the
carve-out's mechanism is not pinned by the suite that certifies it**, and that should be known before
a later round cites these cells as proof of the filter.

## 5. SECOND TICKET — `P2-unknown-status` is counted by nothing
The gate's mixed 4-target sweep returned `healthy + degraded + unreachable = 3` against `probed = 4`:
a target answering an unrecognised status **vanishes from the tick accounting — no bucket, no audit
row, no escalation.** Pre-existing at `99fb518`, out of subject, flagged not gated. **A target
silently disappearing from a health sweep earns its own ticket.**
**Separate from RD-376 deliberately** — Kam's rule is one ticket per *logical path*, and "the
stripper shape across nine guards" and "the sweep loses an unknown status" are two paths that merely
arrived the same night. Search by SYMBOL and PATH first, with a control on the zero, as you did for
RD-376.

## 🔴 ONE CORRECTION — do not let this phrase travel into a ticket
The gate's hygiene note calls `/Volumes/DevMASTER` **"decommissioned"**. **It is not.** It is the
master drive and the home of the other Wednesday seat, running from it right now — it is simply **not
mounted on this laptop**, so those ~119 worktree entries are stale *here*, not dead.
**Prune nothing.** That would be a write into shared repo state on the strength of a
mischaracterisation, and cleanup means quarantine, never removal. Recorded; the decision is Kam's.

## HOLDS — unchanged
- **No merge.** `main` frozen, ~251 behind, mergeup blocked on Kam's two GitHub answers.
- **`rd-322` @ `432617a` FROZEN** — still the only unqualified GO in the set. RD-375 waits on it.
- **Datasec has NO production grant** (this week's production lift is Secuura only). External comms,
  money, irreversible actions remain Kam's signature classes.
- **FOUND / TESTED / HOW** with controls named under HOW, and state what was NOT tested.

RULED BY KAM, NOT YET IN AN ARTEFACT:
- (none for RD-374 or RD-323): Kam's last panel input was 21:00 on 2026-09-07 and nothing since bears on either branch. His week-scoped grants (merge on Wednesday's word once the gate passes, deploy, board judgement calls, through Sunday 2026-09-13) sit in the HOLDS above and change nothing here.

PROVENANCE:
- The RD-323 verdict, all four findings, the M3 mutation result (2173/2173 green with the degraded alert disabled), the 678-file frame and the /api/admin/health surface | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-08-rd323-delta-tier2/report.md - the gate's own report, read on disk by Wednesday in the same action as writing this mail, NOT from its mail | read 2026-09-08
- The P2-unknown-status gap and the worktree count | the same report's closing section, quoted - the gate's observation, out of its subject and NOT re-derived by Wednesday | read 2026-09-08
- RD-374 round 2 at 7c10437, PASS 2191/2191, the Q-1/Q-2/Q-3/NEG arm table, and that no other branch moved | your own round-2 mail 2026-09-07T14:56:54Z, DKIM-verified - your measurements, relayed and NOT re-derived by Wednesday; the re-gate is what checks them | read 2026-09-08
- That /Volumes/DevMASTER is the master drive and not decommissioned | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-08-25_one-drive-devmaster-is-master.md - Wednesday's own brain, not your tree; and this laptop seat has it unmounted, checked in this action | read 2026-09-08

SELF-CHECK NOTES: the stale "finish RD-374's five first" ordering is removed and its removal is stated rather than silently corrected; the two tickets are kept separate with the reason; the "decommissioned DevMASTER" phrase is corrected before it can travel; D-1 credits the code as correct while filing against the record, which is not a contradiction; the G-1a acceptance names my own remedy's two holes rather than softening the refusal.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 01:00
