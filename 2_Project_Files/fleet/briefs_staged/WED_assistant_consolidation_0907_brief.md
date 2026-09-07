# Wednesday-assistant — WEEKLY CONSOLIDATION, 2026-09-07 (the "dreaming" ritual)

You are a **Wednesday-assistant** seat working inside Wednesday's OWN project. You are not a client
agent and you touch no client repo. **Your job is the weekly consolidation ritual, on a branch.**

## THE RITUAL IS THE SPEC — read it FIRST, in full, and follow it
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/skills/weekly-consolidation.md` (7 steps + 4 guards).
**The audit note is mandatory even for a quiet week.** Kam reads it.

## WHERE YOU WORK — and this is a hard boundary
- **Your worktree: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/worktrees/consolidation-0907`,
  branch `consolidation-2026-09-07`.** Work there, commit there.
- **NEVER touch `/Volumes/DevMASTER/WEDNESDAY` itself (the `main` checkout).** A live Wednesday seat
  is writing `_ledger.md`, the daily note and `learnings/` in that tree **right now** — every write
  you make there is a collision. This is the whole reason you are on a branch.
- **NEVER touch any path under `/Volumes/DevMASTER/!CODING/`.** Not yours, at all.
- **Do not push.** Do not merge. Wednesday reviews your branch by measurement and merges it.
- **A second Wednesday runs on Kam's laptop, scoped to Datasec.** Ignore Datasec entirely.

## WHAT THIS WEEK COVERS
**Last consolidation: `learnings/_audits/2026-08-30_consolidation.md`.** So your window is
**2026-08-31 → 2026-09-07 inclusive.** Read every `daily/` note in it, `_ledger.md` whole,
`_ledger_archive.md` and `_ledger_fleet_insights.md` as needed, and every lesson touched in the window.

## ITEMS EXPLICITLY DEFERRED TO THIS CONSOLIDATION — do these, do not rediscover them
1. **Five ambiguous ledger rows to be RULED** — L66 / L73 / L90 / L101 / L123, flagged by the Phase-0
   assistant on 2026-09-05 as ambiguous between Wednesday's own corrections and fleet insight. Rule
   each, with one line of reasoning, and record the ruling in the audit note.
2. **Four case sections whose headings name NO project**, flagged in `learnings/_tier_census.md` as an
   **R0 check before Phase 1** — all in `2026-08-07_a-check-that-cannot-fail.md`. R0 is the
   client-isolation rule: a case section that does not name its project cannot be transferred safely.
   Identify them, propose the correct `P-<Client>/<Project>` heading for each, and say which you could
   NOT determine.
3. **The BOOT-COST line — a STANDING item at every consolidation** (Kam's 2026-08-10 ruling).
   **Measured this morning, use it, do not re-derive:** statusline **ctx:7% before the brain load,
   ctx:19% after** reading `_boot_digest_by_tier.md` whole (254,205 B / 3,353 lines / 104 lesson
   files). **The by-tier digest is 254 KB against the default digest's 280 KB — a 9% saving, not a
   split**, because the tier census is **W 75 / M 24 / MIXED 5**: three quarters of the corpus is
   tier W and W blocks are carried whole. **The lever is not the digest format, it is whether 75
   files deserve W.** Analyse that and propose — **but do NOT merge, cut or rewrite any lesson**:
   Kam's 2026-08-10 ruling stands, *"no reduction until a system is found that keeps the best result
   AND reduces load, i.e. reduction proposals must come with evidence they lose nothing."*
4. **The `_ledger.md` size problem.** It is **248 KB / 151 rows covering only 09-05 → 09-07**, after
   `CLAUDE.md` rule 3c already archived everything ≤09-04. **Rule 3c (archive rows older than ~3 days)
   is not sufficient at the current row size.** Propose a rule that is, with the arithmetic.
5. **A fleet rule from 2026-09-04 awaiting adoption:** *"when a ticket is fixed under a DIFFERENT
   ticket's number, the fixing ticket names the one it obsoletes"* — adopted for NexusAI, proposed as
   fleet-wide. Recommend adopt / narrow / drop, with the reason.
6. **The turn-end-stall class.** Three stalls on 2026-09-07 alone, and a NEGATIVE RESULT is on record:
   s144 applied Kam's approved launcher wording and s145 **stalled anyway**. **Do not close the class.**
   Summarise what is known, what the negative result rules out, and what the next diagnostic step is.
7. **`board_count.sh` cannot total the Secuura board** — Linear caps `first` at 250 and the board is
   at 285, so the script correctly refuses and then has no way to produce a total. Propose the fix
   (cursor-paging) as a ticket; **do not build it.**

## WHAT TO WATCH FOR IN THIS WEEK'S LEDGER — a genuine pattern, stated so you can test it
Wednesday's own corrections this week cluster hard on ONE root cause: **stating a property of a
RUNNING system, or a mechanism, from an ARTEFACT that only represents it.** Today alone had four
instances. **Test that reading against the actual rows rather than accepting it** — if the data says
something else, say so. **A consolidation that confirms the coordinator's own hypothesis without
checking it is worth nothing.**

## HARD RULES
- **NEVER `rm` anything.** Cleanup means quarantine by rename. Nothing is deleted, ever.
- **Incremental deltas ONLY** (the ACE anti-collapse guard): edit and merge specific lessons; **never
  regenerate a memory file wholesale**, and never let summarising erode concrete detail. The audit
  note records **diffs, not rewrites**.
- **Conservation is asserted, not assumed:** if you move rows between files, the row count before and
  after must be identical **as a set**, and you say so with the numbers.
- **Promotion needs recurrence (w≥3) or Kam's explicit "always".** Never promote a single occurrence.
- **Protect retrieval handles** — a merged lesson that cannot be grepped is a destroyed memory. Keep
  names, dates and IDs stable.
- **If a lesson's headline contradicts its operative case, that is a finding** — report it; fix it
  only where the fix is unambiguous.
- **Regenerate both digests** (`tools/boot_digest.py` and `--by-tier`) at the end and report the
  before/after byte counts.

## DELIVERABLE
1. **`0_Brain/learnings/_audits/2026-09-07_consolidation.md`** — the mandatory audit note: every
   change as a diff, every weight retired with its reasoning, **the repeat-correction trend line
   (this is the health metric of the whole system)**, the rulings on the five ambiguous rows, and
   **a clearly separated section: DECISIONS WEDNESDAY OR KAM MUST MAKE.** Anything you could not
   establish goes in as *unmeasured*, named.
2. Your commits on the branch. **Nothing pushed.**
3. **ONE mail** to `wednesday-agent@agentmail.to`, subject exactly:
   `[WED assistant -> Wednesday] Weekly consolidation 2026-09-07`
   BLUF first: what changed, what you are proposing, what needs a decision. **NOT-DONE at equal
   prominence with done.** Every number carries the command that produced it.

## IF YOU HIT A QUESTION THE BRIEF DOES NOT ANSWER
Mail Wednesday (`QUESTION:` subject) and **continue on the safest interpretation** rather than
blocking — but **anything that would DELETE, MERGE or RETIRE a lesson stops and asks.** Those are
Wednesday's, and some are Kam's.
