---
date: 2026-09-05
type: report
source: WED-145 Phase 0, executed by a Wednesday-assistant seat on branch `phase0-context-split` (worktree `2_Project_Files/worktrees/phase0`), on Kam's 20:28 approval of `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md`
status: live
---

# WED-145 Phase 0 — measure and tag: what the three-tier split would take out of Wednesday's boot

## BLUF
**The boot path drops from 543,399 B to 427,895 B — 21.3%.** Scaled linearly against the
27% this brain load measured today, that is an **estimated ~21% boot (about 6 points back). It is an
ESTIMATE, not a measurement** — the real number is the statusline at the next boot that reads the
by-tier digest. **Nothing was deleted, merged or rewritten.** Every ledger row still exists, byte for
byte; every lesson file still holds every word of its cases; the default digest is unchanged. All of it
sits on `phase0-context-split` for Wednesday and Kam to rule on.

## The numbers

| Thing | Before | After | Δ |
|---|---:|---:|---:|
| `_ledger.md` (read whole at every boot) | 288,517 B · 135 rows | 199,169 B · 93 rows | **-89,348 B (-31.0%)** |
| `_ledger_fleet_insights.md` (new, read on demand) | — | 90,296 B · 42 rows | +90,296 B |
| Boot digest | 254,882 B (`_boot_digest.md`) | 228,726 B (`_boot_digest_by_tier.md`) | **-26,156 B (-10.3%)** |
| **What a boot reads (digest + ledger)** | **543,399 B** | **427,895 B** | **-115,504 B (-21.3%)** |
| Boot ctx% (statusline) | 27% (measured, every seat since 09-02) | **~21% (ESTIMATED, linear)** | ~−6 points |

**Conservation.** The 42 moved rows are byte-identical to their source lines and the row SET is equal:
HEAD's 135 rows == 93 (ledger) + 42 (new file), no duplicates, original order preserved in both. Ledger
bytes on disk went 288,517 → 289,465 across the two files — **+948 B**, which is the new file's own
heading prose, its table header, and the one pointer line added to `_ledger.md`. No row was edited.

**Where the digest's 26,156 B comes from:** 25,183 B is the 28 project CASE sections becoming one-line
handles; 973 B is the section index dropped from the 24 M files. The P sections are **73,445 B in the
lesson files** but only 25,183 B in the digest — the digest already carried their rules and headings, not
their evidence. Do not add those two figures together: 73,445 B is what would travel to the agents in
Phase 1; 25,183 B is what leaves Wednesday's boot.

## The tiers, as tagged

98 lesson files, 464,832 B, every one now carrying `tier:` in its frontmatter.

| Tier | Files | Bytes |
|---|---:|---:|
| W — Kam, the coordination method, the boundaries, Wednesday's own failure modes | 69 | 260,648 |
| M — fleet method, client-neutral | 24 | 85,237 |
| MIXED — a W/M lesson carrying project CASE sections | 5 | 119,913 |
| P — a project's own cases, as a whole file | 0 | 0 |

**The W/M split is a first pass and nothing yet depends on it** — in the digest, M differs from W only by
dropping the section index (973 B across 24 files). It matters in Phase 2, when the M tier is what
travels to every agent. Wednesday should read the tier column of `_tier_census.md` as a proposal.

## The section list — every P section that would leave the boot

| Project | Case sections | Bytes in the lesson files |
|---|---:|---:|
| P-Datasec/NexusAI | 14 | 42,660 |
| P-Secuura/Blockchain | 14 | 30,785 |
| **total** | **28** | **73,445** |

24 of the 28 sit in `2026-08-07_a-check-that-cannot-fail.md` (71,660 B — 15% of all lesson bytes, and
the single largest file in the brain). The other four are one section each in
`headline-must-match-the-operative-case`, `i-read-representations-they-read-sources`,
`a-recorded-blocker-is-not-a-boundary` and `an-overstated-record-gets-discounted-wholesale`.

Full list, verbatim from `0_Brain/learnings/_tier_census.md`:

| File | Project | Section | Bytes | Note |
|---|---|---|---:|---|
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The concrete remedy, added 2026-08-13 (Secuura/Blockchain s28) | 2,226 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A failure-only log going quiet is not recovery (2026-08-22, Secuura s61) | 1,441 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The third member: a check that MISREPORTS what it saw (2026-08-14, same agent) | 1,756 | heading says 'same agent'; body names PR #646 (= KS-559, Secuura) and 'a Secuura session caught it' |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A test that cannot CLEAN UP starts asserting against live data (2026-08-15, Secuura s35) | 2,538 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A positive control proves the suite it RAN IN, and nothing about its neighbour (2026-08-15, Secuura s35) | 1,494 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The inverse: a REPRODUCTION that cannot reproduce (2026-08-15, Datasec/NexusAI) | 2,467 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The refinement that makes the positive-control rule actually work (2026-08-16, Secuura s37) | 1,849 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | An indicator that can MISS its own event (2026-08-24, Datasec/NexusAI) | 1,221 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The control needs its own control (2026-08-23, Datasec/NexusAI) | 3,030 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The condition we had not stated: on a side-effecting system, the positive control IS an action (2026-08-14, Secuura s34) | 2,051 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | The mirror: an ABSENCE claim needs a positive control too (2026-08-14) | 2,689 | heading carries no project; body: 'A Secuura session flagged…' |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | Three "cannot see" members from one micro-session (2026-08-25, Datasec/NexusAI s5) — and a derivation lesson from its neighbour | 1,977 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A test's NAME is not its coverage (2026-09-03, Secuura s119 — the member that let an AUTH BYPASS survive a suite that appears to test it) | 3,287 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A census, a writer and a verifier that descend from ONE parse are one view rendered three times (2026-09-04, Datasec/NexusAI S29 — its own diagnosis,  | 3,563 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | THE ALL-FAIL RED-PROOF: a tamper that destroys the SUBJECT, so the failure set stops discriminating (2026-09-04, Datasec/NexusAI — self-caught and sel | 2,244 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A FIXTURE THAT CANNOT REACH THE PRODUCT'S PATH — the entry-point member (2026-09-04, Datasec/NexusAI RD-245; a BLOCKER found under a green suite the t | 3,734 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | CORRECTED the same session, by the same agent, and the correction is the better lesson | 5,210 | sub-section continuing the Datasec/NexusAI S29 census case (L486), filed out of order after the L606 shell section |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A red-proof proves a check CAN fail; only a GREEN BASELINE proves it can pass for the right reason (2026-09-04, Secuura s120 — a guard defeated by its | 3,367 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | The AXIS a guard is blind on is not the axis it was designed for (2026-09-04, Datasec/NexusAI — a perfectly-implemented guard, green on a defect it co | 2,898 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | THE OTHER END OF IT: a red-proof on a subject that did not COMPILE is not a red-proof (2026-09-04, Secuura s121 — the pair to the green-baseline rule  | 3,073 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | A MULTI-CLAUSE guard red-proofed with a fixture that trips BOTH clauses has measured the pair and learned nothing about the parts (2026-09-04, Datasec | 3,475 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | THE SECOND HALF, added hours later by the TESTER that verified the fix (2026-09-04, QA re-gate on `aad37da`) | 2,903 | sub-section of the L831 Datasec/NexusAI multi-clause-guard case (the tester's second half) |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Datasec/NexusAI | AN ELIMINATION SET THAT IS EXHAUSTIVE WITHIN ONE CATEGORY AND SILENT ABOUT THE OTHERS (2026-09-04, Datasec/NexusAI S32 — it disproved its OWN filed fi | 3,523 |  |
| `2026-08-07_a-check-that-cannot-fail.md` | P-Secuura/Blockchain | A TEST HELPER THAT REIMPLEMENTS THE PRODUCT IS A MOCK THE MOMENT THE PRODUCT MOVES (2026-09-05, Secuura s128 — found by its own red-proof, not by read | 2,047 |  |
| `2026-08-13_headline-must-match-the-operative-case.md` | P-Secuura/Blockchain | The tooling costume (2026-08-17, Secuura s43): a check whose MESSAGE rots while its measurement stays correct | 1,857 |  |
| `2026-08-14_i-read-representations-they-read-sources.md` | P-Datasec/NexusAI | The fourth switch (2026-08-25, Datasec/NexusAI s4): the option you can VERIFY WITHOUT EFFORT | 1,422 |  |
| `2026-08-16_a-recorded-blocker-is-not-a-boundary.md` | P-Secuura/Blockchain | The third member (2026-08-27, Secuura s73; consolidated 2026-08-30): a DEFERRAL recorded only in code, pointing at a ticket | 1,110 |  |
| `2026-08-16_an-overstated-record-gets-discounted-wholesale.md` | P-Datasec/NexusAI | THE ROT HAS A MECHANISM, and the NexusAI agent (S32) named it better than I had (2026-09-04, after its THIRD stale ticket in one day) | 4,993 |  |
**Four of the 28 name no project in their heading**; their client was resolved from the case body and
each carries the reasoning in the Note column. Those four are the ones to check before any transfer —
a case that travels to the wrong client's agent is an R0 breach, and a heading is the only thing a
future reader will look at.

## What was NOT done, deliberately
- **Nothing merged.** Everything is on `phase0-context-split`; `main` was never touched.
- **Nothing deleted.** No row, no section, no file. The moves are moves.
- **No Phase 1 transfers, no M-tier shared home, no lesson text changed** — out of Phase 0's scope.
- **Five ledger rows were NOT moved** although their type says fleet-insight: their subject is
  Wednesday's own hands or her own tooling, and the brief says an ambiguous row stays and gets listed.
  They are in the STATUS mail and in the commit for step 1.
- **The boot has not been re-measured.** The ~21% is arithmetic on bytes. Nothing reads
  `_boot_digest_by_tier.md` yet — the launcher still loads `_boot_digest.md`, and switching it is
  Wednesday's call, not this seat's.

## How the default digest was proven unchanged
1. **The code change is inert.** The pre-change script and the post-change script, both run over the
   pre-tag lesson files with a frozen timestamp: `cmp` byte-identical, 254,882 B — and identical to the
   digest captured before any edit in this session.
2. **The whole of Phase 0 is inert on it.** That same baseline against the new script run over the
   tagged files: the only differing line is the header's own source-bytes measurement
   (464,044 → 464,832 B — the 96 `tier:` lines). Digest bytes identical at 254,882.
   `boot_digest.py --check`: 98 files, 0 misses, 0 stale.
3. **Red-proof of the flag.** A fixture lesson tagged `tier: P-Test/Fixture` emits exactly one line and
   no case prose; delete the tag and it falls back to the default shape and is named UNTAGGED
   (2,236 B → 2,615 B).

The `<!-- tier: P-… -->` markers are stripped in `parse_text`, so neither digest ever carries one.

## Provenance
- Plan and tiers | `1_Project_Definition/Architecture/2026-09-05_learning-tiers-context-split-plan.md` + `0_Brain/learnings/2026-09-05_three-tier-learnings-wednesday-management-agents-project.md` | read 2026-09-05 by this seat
- Kam's approval | panel 20:28, "Let's go ahead with the proposed plan" | quoted in the brief
- The 27% baseline | the brief's measured figure for digest + ledger today | not re-measured here
- Every other number above | measured from the files in this worktree at the commit each step names
