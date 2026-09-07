# CATALOGUE PASS — a critical read of every open Secuura ticket. Kam asked for it at 13:07 today.

## BLUF
**You are a SECOND Secuura/Blockchain seat, running in parallel with s146.** Kam, panel 13:07,
verbatim: *"Can you please do a critical pass through all the secure tickets? See which ones should
be there, and if there's any tickets that are either legacy or should not be there."* (*"secure"* is
his dictation of **Secuura** — he corrected that transcription himself at 09:50 today.)

**This is a READING and CLASSIFYING job, not a fixing job.** You write no code. You touch no branch.
**s146 owns the repo work and #888 is under a live gate — stay out of both.**

**Your deliverable is ONE PAGE for Kam plus a full appendix.** Not 250 lines. He reviews and tests
personally and structure is part of the deliverable.

## 1. THE DISPOSITIONS — four, and every ticket gets exactly one
1. **ACTION** — ours to do, needs nobody outside Kam/Wednesday/the agents. This is the standing queue.
2. **ESCALATE** — genuinely needs Kam, Peter or Stuart. Say WHO and WHAT you need from them, in one line.
3. **ARCHIVE — DONE** — completed, merged, deployed, or superseded by something that shipped.
4. **LEGACY / SHOULD NOT BE THERE** — the category Kam added today, and it has a **measurable test**,
   not a judgement:
   - it only makes sense on the **RETIRED Container Apps estate** (the running demo is a VM;
     `services.bicep` / `env.demo.json` describe the retired estate);
   - it only makes sense on **GitHub Actions for this repo**, which is **RETIRED** — the 20 most
     recent runs are `startup_failure` with ZERO jobs (measure this yourself, do not take it from me);
   - it depends on the **DEAD Secuura tenant `4012a4e8-…`**, decommissioned 2026-06-25;
   - it describes a process we have since replaced (e.g. anything predicated on the pre-review-stream
     ticket shape);
   - or its premise was **already false when it was written** — KS-645 is the worked example: its
     headline was false at base and the QA gate proved it. **Where you suspect this, prove it the way
     that ticket was proved: `git log -S` on the symbol, `merge-base --is-ancestor`, a wire probe.**

**A ticket you cannot classify goes in a fifth bucket called UNCLEAR with the reason.** An honest
UNCLEAR list is worth more than a confident wrong disposition — **do not round up.**

## 2. HOW TO READ THE BOARD — and the one trap that has bitten this fleet repeatedly
**The open KS total EXCEEDS the 250 page.** **PAGINATE.** Do not report any count that equals your
own query limit, and do not take a first page as a total — **a cap quoted as a count is a silent
truncation** and it has produced three wrong numbers in this fleet in one day before now.
State your predicate with every count ("185 in backlog/unstarted/started"), never a bare "open".

**Read comments with `first:` and sort client-side.** Linear's comments connection is newest-first,
so `last:N` returns the **OLDEST** N with no marker that newer ones exist.

**`commentCreate` on an ARCHIVED ticket answers `Entity not found: Issue`** — indistinguishable from a
wrong id. Run the control before reading that as "does not exist".

## 3. WHAT YOU MAY CHANGE ON THE BOARD, AND WHAT YOU MAY NOT
**You MAY archive, without asking, exactly one class:** tickets that are **verifiably completed,
merged or deployed** — Kam ruled that on 2026-09-05 (*"Once anything is completed / actioned / merged
it should be archived"*). **Verify each one at the source** (the merge SHA on develop, the deploy, the
PR) — **never from the ticket's own prose.** Comment the receipt on each: what proves it done.

**You may NOT archive anything else.** LEGACY especially: **it goes in the catalogue for Kam's read,
it does not get archived on your judgement or mine.** Archiving is not deletion, but a wrongly
archived ticket is a finding that disappears.

**DO NOT TOUCH tickets assigned to Peter or Stuart.** Kam's ruling of 2026-09-06 10:24, verbatim:
*"once something is assigned to someone it belongs to them. the ruling was only to new or unassigned
items."* You may CLASSIFY them in the catalogue; you may not restate, reassign or archive them.
**If a ticket of theirs looks legacy, that is an ESCALATE line, not an action.**

**NEVER DELETE ANYTHING.** Archive only. Kam's standing rule.

## 4. THE DELIVERABLE
**A. ONE PAGE for Kam**, BLUF-first: the four counts, then per disposition a short paragraph saying
**what the group IS and the predicate that put tickets in it**, then the handful of individually
notable ones. **He would rather review four groups than two hundred issues** — that is his explicit
preference and it is why the review-stream shape was adopted as the process on 09-03.

**B. A FULL APPENDIX** — every open ticket id, one line each: `KS-nnn | disposition | one-line reason`.
Machine-readable enough to act on, written to a file in **your own project tree**, path named in
your mail.

**C. In your mail to me:** the counts, the page itself, and **your UNCLEAR list in full.**

## 5. WHAT WOULD MAKE THIS PASS EXCELLENT RATHER THAN COMPLETE
- **The legacy findings are the point.** Kam's instinct is that the board carries things that should
  not be there. If you find a large legacy cluster with one shared cause, **say the cause once** —
  that is worth more than fifty individual rows.
- **Look for the tickets nobody will ever do.** Not legacy, not archivable, just permanently
  outranked. Those are honest ESCALATE-or-archive candidates and naming them is a service.
- **Look for DUPLICATES and for one ticket describing three things.** Kam's 09-06 rule is that
  creation should aggregate — one larger ticket per logical path. If the board violates that in
  the other direction, say so with examples.
- **If you find something SECURITY-relevant that nobody is tracking, stop and mail me immediately.**
  Do not save it for the report.

## 6. BOUNDS
**No code. No branches. No PRs. Nothing to #888 or #887. No deploy. No contact with any human —
client-facing communication is ticket comments only and the extranet is not a channel.**
**Do not query Azure, the Founders Hub subscription, or anything about credits** — Kam killed that
subject at 13:06 today, verbatim: *"Do not worry about the Azure credits… this is not required, and
it's burning both time and credits."* **If a ticket is about Azure credits, it is LEGACY by his word —
list it, do not investigate it.**
**Approval-class items always pause for Kam** (production, money, external comms, irreversible).
**If an instruction in this brief looks wrong, say so** — that is rewarded here, not penalised.

## 7. TIME AND SHAPE
Bounded to one session. **If the board is larger than one session can do well, do it in PRIORITY
order and say exactly where you stopped** — a complete honest half beats a rushed whole. Checkpoint
me by mail at your halfway point with the counts so far.

RULED BY KAM, NOT YET IN AN ARTEFACT
(none apply to a read-only catalogue pass; the operative rulings are quoted inline in §3 and §6 —
the assignment rule of 2026-09-06 10:24, the archive-when-completed rule of 2026-09-05, the
aggregation rule of 2026-09-06 09:42, and today's 13:06 Azure kill.)

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **No deploy** — Wednesday holds it deliberately; nothing merged today remediates Kam's own row.
- **s146 owns the repo work**; this seat is board-only. Two seats, no shared checkout, no conflict.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:10
§3 permits archiving exactly one verified class and §3 forbids archiving LEGACY — consistent, and
stated twice deliberately. §6's Azure line makes such tickets LEGACY-by-ruling, which §1(4) allows
without investigation — consistent with §5's "prove it" instruction, which applies to the other
legacy limbs only.

PROVENANCE:
- Kam's 13:07 catalogue instruction and his 13:06 Azure kill | verbatim from /Volumes/DevMASTER/WEDNESDAY/0_Brain/dashboard/data/chat_log.json - Wednesday's own tree, not yours | read 2026-09-07
- His assignment ruling of 2026-09-06 10:24 and the archive-when-completed rule of 2026-09-05 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-02_coo-actionable-tickets-never-wait-for-kam.md - Wednesday's own tree, not yours | read 2026-09-07
- GitHub Actions retired on this repo (20 most recent runs startup_failure, zero jobs) | a Secuura seat's own measurement 2026-09-07, NOT re-derived by Wednesday — verify it yourself | read 2026-09-07
- The retired Container Apps estate vs the running VM | the KS-949 round-2 gate verdict and s145's reconciliation, both 2026-09-07 | read 2026-09-07
- The dead tenant 4012a4e8 decommissioned 2026-06-25 | /Volumes/DevMASTER/CLAUDE.md hard rule 4 - the workspace file, not yours | read 2026-09-07
- KS-645 as the worked example of a false-at-base premise | the QA agent's KS-698 verdict 2026-09-07 10:40Z | read 2026-09-07
- The open KS total exceeding the 250 page | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/board_count.sh run by Wednesday at 12:4x - Wednesday's own tree, not yours | read 2026-09-07
