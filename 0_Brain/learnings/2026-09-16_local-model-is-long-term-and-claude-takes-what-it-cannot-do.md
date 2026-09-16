---
date: 2026-09-16
type: grant
source: Kam, email 2026-09-16 07:45:53Z (17:45 AEST), spf/dkim/dmarc all pass — "Please save this as an operational rule"
status: live
tier: W
expires: none stated — his words are "for the long term"
---

# The local model is PERMANENT and it is the first router stop — Claude agents take what it cannot do, and a task the local model FAILS is reallocated to Claude, not re-briefed at it forever

**His words, verbatim:**
> *"On actions and tickets*
>
> *Working with a local model is proving productive. Let's keep that going for the long term. The local
> agent gets tasks you think it can handle and normal Claude agents get everything else. If local fails,
> the task is allocated to a Claude agent. Not urgently but when it makes sense.*
>
> *Please save this as an operational rule."*

**The operative case, so the headline matches it:** Wednesday is deciding who does a piece of work, or
is looking at a ticket the local model has just failed. **Three clauses decide it, and the third is the
one that changes today's behaviour most.**

## The rule, in three clauses

1. **The local model is a PERMANENT part of the workflow, not a pilot.** This retires the trial framing
   carried by [[2026-09-14_local-model-pilot-grant-qwen3-30b-simple-checked-tasks-only]] and
   [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] — the *mechanisms* in both stand;
   what lapses is the language of a pilot awaiting a verdict. He has given the verdict.

2. **Wednesday ROUTES, and the judgement is Wednesday's.** *"The local agent gets tasks you think it can
   handle and normal Claude agents get everything else."* This is a delegation of the routing decision,
   not a rule about which tickets qualify — so the misroutes are Wednesday's to own and to learn from,
   and the routing predicate belongs in the ledger when it is wrong.

3. **A FAILED local task is REALLOCATED to a Claude agent — "not urgently but when it makes sense."**
   Failure is a routing signal, not a prompt to try the same ticket at the same model again. There is no
   deadline attached: the reallocation waits for a sensible moment (a Claude seat already open on that
   project, a lane that owns those files, the Sunday QA pass), and it is never a reason to leave the
   local model idle in the meantime.

## The distinction Wednesday stated back to him rather than assuming

**Most of today's local "failures" were Wednesday's briefs, not the model.** KS-692 produced a correct
first sample and was refused because the brief never declared its red cells. KS-1168 was refused twice
for `+` lines that were really context — the model emitted the honest minimal hunk both times and was
right both times. KS-998 the same.

So this file reads clause 3 as: **the MODEL genuinely could not do the work** → reallocate to Claude.
**The BRIEF was defective** → fix the brief; the ticket stays with the local model. A brief defect that
gets a ticket escalated would punish the model for the coordinator's error, and would also hide the
brief defect, which is the thing that actually needs fixing
([[2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix]]).

**This reading was put to him in the receipt, with the simpler alternative named ("any failure,
escalate") and an invitation to overrule.** Until he answers, it is Wednesday's reading and is marked as
such — not his word ([[2026-08-16_classification-is-the-field-that-grants-authority]]).

## How to apply

1. **Every routing decision names which side it fell on and why**, in one clause, in the brief or the
   receipt: *"local — one file, a fix shape the ticket spells out, an in-process test to copy"* or
   *"Claude — needs a real PostgreSQL and a judgement about what to pin"*.
2. **Keep a FAILURE COUNT per ticket at the local model.** The second genuine model failure on one
   ticket — after any brief defect has been ruled out and fixed — is the trigger for clause 3, not a
   third brief. Record the reallocation and its reason on the ticket's row in `night/done.md`.
3. **"When it makes sense" is a real constraint, not a hedge.** Batch reallocated tickets for a Claude
   seat that is already open on that project, or for the Sunday raising pass. Do not open a seat per
   escalated ticket — that is the cost this rule exists to avoid.
4. **Reallocation never idles the local model.** The moment a ticket leaves for Claude, the next
   candidate is briefed ([[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]],
   [[2026-09-16_if-something-blocks-move-on-to-the-next]]).
5. **The routing predicate is a claim and it gets measured.** At the weekly consolidation: how many
   local tasks passed, how many were reallocated, and — the number that says whether the routing is
   any good — how many reallocations turned out to be brief defects rather than model limits.

**Family:** [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] (the night mechanism this
makes permanent) · [[2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once]] (the week's shape, which
still expires on Sunday — THIS file does not) · [[2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model]]
(the usage cut that makes local the only option above 90%) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5:
every grant recorded, so the boundary is written down and never vibes) ·
[[2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix]] (why a brief defect must not be
laundered as a model failure).
