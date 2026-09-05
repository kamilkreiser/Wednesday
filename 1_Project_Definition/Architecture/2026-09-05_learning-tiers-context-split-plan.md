---
date: 2026-09-05
type: plan
source: Kam's proposal (terminal, 16:5x, verbatim in Discovery/00_prompt-log.md) + Wednesday's assessment; lesson `0_Brain/learnings/2026-09-05_three-tier-learnings-wednesday-management-agents-project.md`
status: proposed — Phase 0 runs at the weekend consolidation unless Kam says otherwise; Phases 1–3 after he sees Phase 0's numbers
---

# Learning tiers — splitting the brain so Wednesday boots lighter and rotates less

## BLUF
Kam's model is adopted with one refinement: **three tiers, not two**, because a project's cases must never reach another client's agent (R0), and the method a case teaches must be rewritten client-free before it travels. **W** (Wednesday: Kam, coordination, boundaries, her own failure modes) · **M** (fleet method, client-neutral, every agent carries it) · **P-<Client>/<Project>** (that project's cases, in that project's own brain, loaded by its own agent). Measured today: Wednesday's boot is 27% of the window; the project weight sits in case SECTIONS appended to method lessons (one file is 16% of all lesson bytes, ~25 case sections) and in 49 of the ledger's 128 rows (37% of ledger bytes) that are agent-credit records already on the scoreboard. **Estimated boot after the split: 12–17% (UNMEASURED until Phase 0 tags the files — the estimate assumes the case sections and insight rows leave the boot path and nothing else changes).** A seat's working band grows from ~43 to ~55 points (about a quarter longer), and — the larger half of Kam's point — fewer relays pass through Wednesday's window at all once agents carry their own cases.

## Recommendation
Run **Phase 0 this weekend** (Wednesday's folder only, reversible, no other project touched), report the numbers, then Kam decides Phases 1–2. Phase 3 (the at-creation rules) starts NOW because it costs nothing and stops the pile growing.

## What is measured today (2026-09-05 16:5x, from the files — the query is in the daily note)
| Thing | Measured |
|---|---|
| Boot cost, statusline after digest + ledger | 27% (this seat; 26–27% on the three seats before it) |
| Lesson files / bytes | 95 files · 443 KB |
| Largest file | `2026-08-07_a-check-that-cannot-fail.md` 70 KB, 11 H2 sections + ~25 case sub-sections (NexusAI paint/CSS instruments, Secuura audit-lock gates, jsonStorage, body-parser…) |
| Top three files' share | 113 KB of 443 KB (25%) — a-check-that-cannot-fail · representations · ghost-suggestions |
| Files with dense project ids (≥3 per KB) | 4 files, 12 KB — the P weight is NOT in separate files |
| Ledger rows | 128 · 273 KB in rows; **49 fleet-insight/praise rows = 102 KB (37%)**; 66 correction rows = 145 KB; ~13 rows the parser could not type (pipes in prose) |
| Ledger archive | 396 KB, read on demand |
| Seats today | 6 boots (08:05 · 13:09 · 13:32 · 15:00 · 16:00 · 16:49) |

## The three tiers, with examples from today's brain
- **W — Wednesday (loaded whole):** ask-format · BLUF · one-question · challenge-me · the autonomy grants and v1.3 · tickets-are-the-channel · Peter/Stuart test blocks · COO stance · validate-brief-pointers · representations (the RULE and Wednesday's own costumes) · ghost ladder · tap-is-a-pointer · pane-close · QA gate order · rotation band · root-folder · names-not-pronouns · this file.
- **M — fleet method (client-free, every agent):** a control must be able to fail; a red-proof drives the product's own entry point; predict the failing SET before the tamper; a SHA is read or not used; rc on its own line, never behind a pipe; never delete (quarantine); a claim about the board is read back before any wrap lists it; verify after the OLD revision stops; a helper that reimplements the product is a mock. **Every one of these already exists as a sentence in the brief template / QA charter standing lines — the M tier is mostly extraction, not authorship.**
- **P — project cases (in the project's brain):** Secuura: the fast-uri/KS-763 fuse rows; the audit-lock corpus 35-of-45; `docker rm -f` on autoheal; the compose-vs-source precedence probe; the body-parser guard corpus; `redis-cli` rc 0 on WRONGPASS; the `d1:` encrypted-email census. NexusAI: jsonStorage rotation/restore/tombstone; the 66/112-second rollover; `bfs`'s `-newermt`; the CSSOM-vs-paint instruments; `home-containment.js`; BSD awk. HPSM: the speaker-notes containment. Each is a sub-section of a W/M file today.

## Phases
### Phase 0 — measure and tag (weekend consolidation; Wednesday's folder only; reversible)
1. Add `tier:` to every lesson file's frontmatter (W / M / P-<Client>/<Project> / MIXED) and a `<!-- tier: P-Secuura/Blockchain -->` marker on every case sub-section inside a MIXED file. One pass, one commit, nothing deleted or moved.
2. Tag every ledger row's type column: `correction` (W) · `kam` (rulings/praise) · `fleet-insight[P-…]`. 
3. `boot_digest.py` gains `--by-tier`: W whole · M rules-only · P handle-only. Run it beside the current digest and **measure both** (the Read tool's token count + the statusline at the next boot). Report: before/after bytes, before/after ctx%, and a list of every section that would leave Wednesday's boot — for Kam to eyeball (the 08-10 ruling: reduction comes with evidence it loses nothing).
4. Ledger: the 49 insight rows are already on the scoreboard by construction (every one says "credit at SCORE") — confirm row-by-row, then move them to `_ledger_fleet_insights.md` (a move, conserved counts, the 3c pattern). Wednesday's ledger keeps corrections + Kam rows.
**Exit:** two numbers on the panel — boot % before and after — and the section list. Kam rules Phase 1.

### Phase 1 — transfer the P tier to the agents (one brief per project; the agent writes, Wednesday never edits their files)
1. For each active project (Secuura/Blockchain, Datasec/NexusAI; HPSM when it wakes): a `LESSONS TRANSFER` brief listing that project's case sections verbatim with provenance (the ledger row / lesson section and its date), and the rule each produced.
2. The agent files them in ITS brain in a digest-shaped file its launcher reads at boot (handle + rule; case on demand) — its choice of path, inside its folder — and confirms by mail with the path and a size.
3. Wednesday marks each section `transferred: <project> <date> <path>`; the by-tier digest drops it to a handle. **Nothing is deleted from Wednesday's files** — the case stays readable on demand; it leaves the boot, not the brain.
4. Per-project size tripwire: the agent's lessons file gets the same boot-cost line at its boot (their launcher — their change, on Kam's word) so the problem does not reappear one level down.

### Phase 2 — a home for the M tier that every agent reads at boot (Kam's call — a shared file)
Today the M sentences reach agents only inside Wednesday's briefs. Options: (a) a `fleet-method.md` under `Notes (MASTER)/skills/Current/` referenced from the workspace `CLAUDE.md` (both shared across clients → Kam edits or approves the line); (b) each project's own `CLAUDE.md` gains a pointer (each project's agent adds it, on Kam's word). Recommendation: (a), because one file is one truth and the workspace `CLAUDE.md` already carries the fleet-comms section the same way. Nothing moves until he rules.

### Phase 3 — at creation, from now (no approval needed; Wednesday's own discipline)
1. New lesson → `tier:` in the frontmatter before the body is written; a P case is written as a transfer item, not as a section of a W file.
2. Fleet insight / agent praise → scoreboard row + the project's standing lines; NOT a ledger row (the ledger keeps Wednesday's corrections and Kam's rows).
3. Weekly consolidation reports three numbers: boot %, P sections awaiting transfer, M sentences extracted this week.

## Risks and limits, stated
- The boot is ~a third of a seat's budget; the working two-thirds is mail and reports. Halving the boot lengthens a seat by about a quarter — real, not dramatic. The bigger lever is agents carrying judgement so fewer events cost Wednesday's window at all; that is measured by relays-per-seat, a number Wednesday does not yet collect (Phase 0 adds it).
- A P-tier file in a project is written by that project's agent under its own identity — Wednesday can verify it exists (read-only) but not its quality; the QA gate does not cover brains. Sample one transfer per project at the consolidation.
- Some sections are genuinely MIXED (a case that IS the rule's proof) — tag MIXED, keep the rule in W, move the case; do not force a split that loses the proof.
- Superseded / status lines in frontmatter are untouched; `tier` is a new field only.
