# Kam has widened you from CLASSIFYING to CLEARING. Board-side only, and the bounds are unchanged.

## BLUF
**Kam, panel 13:21, verbatim:** *"Thanks. Keep clearing these and addressing them. If there's any
that can be addressed quickly, please do so."*

**So: where a disposition is obvious and the fix is board-side, DO IT as you go rather than listing
it.** Do not batch everything into the report and wait. **The catalogue is still the deliverable —
this changes when you act, not what you produce.**

## WHAT "QUICK" MEANS HERE — board-side only, and you already have the authority for all of it
- **State corrections.** KS-869 sitting in `Tested Not Deployed` with an OPEN PR against it is not
  finished — move it back with a one-line comment naming the PR. Same for anything else whose state
  your source-verification contradicts.
- **The legacy cluster's OWN half.** Of the six that presuppose a working GitHub Actions, the ones
  **not assigned to Peter or Stuart** get a comment carrying **your** measurement (2,000 runs, 100%
  `startup_failure`, ≥18 days, 16 dead workflow files) and the disposition that follows. **If a
  ticket cannot be done as written and will not become doable, say so ON the ticket** — a dead ticket
  with a reason is worth more than a dead ticket.
- **Duplicates and aggregation violations** you have already proven: comment the link, mark the
  duplicate, leave the survivor.
- **The three 'Done' with no PR attachment** (KS-642/644/681): a comment asking for the evidence, or
  your measurement that none exists. **They stay UNCLEAR, not archived.**

## WHAT IS STILL NOT YOURS — none of this moved
- **The 23 in `Tested Not Deployed` stay put.** They are the deploy manifest. Unchanged.
- **Peter's 19 and Stuart's 6 are classified only, never touched** — Kam's 2026-09-06 10:24 ruling.
  A legacy ticket of theirs is an **ESCALATE line for him**, not an action for you.
- **No code, no branches, no PRs, no doc edits.** The KS-418 documentation defect — the false AWS
  premise in `systemTest/CLAUDE.md:1895`, `systemTest/docs/how_to_test_secuura.md:502` and
  `systemTest/performance/docs/quick_start.md:286` — **is real and I am queuing it for a code seat,
  not for you.** Put it on the one page; do not edit the files.
- **Never delete. Archive or comment.** **No Azure, no credits, no Founders Hub.** No human contact.
- **Anything security-relevant and untracked comes to me the moment you find it.**

## THE ONE THING TO KEEP HOLD OF
**You refused an instruction of mine an hour ago and were right.** This widening is not a licence to
stop doing that. **If clearing something quickly would destroy a record, or if a disposition is
obvious to me and not to you from the evidence, stop and say so** — exactly as you did with the 23.
**Speed is the second priority. The first is that nothing true disappears.**

Keep the counts running as you go: how many cleared, how many left, and what changed since your
checkpoint. **The 30% self-referential split is still the headline of the one page.**

PROVENANCE:
- Kam's 13:21 widening | verbatim from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's own tree, not yours | read 2026-09-07
- His assignment ruling of 2026-09-06 10:24 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own tree, not yours | read 2026-09-07
- The Actions measurement, KS-869, the three PR-less 'Done' tickets and the KS-418 doc paths | YOUR 03:18:14Z checkpoint, carried as YOUR measurements | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:22
This mail widens the 03:10:58Z brief's §3 from classify-only to clear-as-you-go for board-side items,
and SUPERSEDES nothing else in it. The 23-ticket carve-out from my 03:19:56Z mail is restated here
unchanged, deliberately.
