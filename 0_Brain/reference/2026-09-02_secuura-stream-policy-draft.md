---
date: 2026-09-02
type: reference (DRAFT policy text — Secuura-facing; written into the Secuura repo by the Secuura agent as a docs PR, never by Wednesday)
source: "Kam, dashboard chat 2026-09-02 19:28 / 19:29 / 19:31 AEST (verbatim in 1_Project_Definition/Discovery/00_prompt-log.md) — out of the Secuura meeting with Stuart and Peter"
status: draft — goes to s108 as item 0; Kam's answer to the one open question (archive the two named classes on grouping, or hold all archiving for the catalogue run-through — default HOLD) lands here when it arrives
---

# Secuura / Platform K — board streams, projects and Peter's test cadence (policy draft v0)

## BLUF
Work on Platform K is organised by **stream**, not by ticket. Every ticket belongs to exactly one Linear **project** (the stream). Tickets in a stream are built and handed to Peter **together**, so Peter runs **one test pass per stream** instead of one per ticket. Tickets that are parked or cannot be actioned yet are **archived** (never closed) inside their stream project, so Linear's active-issue cap is spent only on work that can move.

## 1. Streams become Linear projects
- One Linear project per stream. Seed set from Kam's words (2026-09-02): **Connectors** (Outlook and every other connector — Stuart now leads Platform S and connectors; Platform K no longer builds connectors) · **Commercialisation-readiness** (key rotation, changing blockchain, anything that only matters at commercial launch). Further streams are derived from the board itself at the projectise pass (candidates the category-1 work already shows: security-register hygiene · auth/MFA · anchoring/Cardano · billing · CI/preflight/tooling · docs/spec) — named by the agent, confirmed by Kam at the catalogue run-through.
- Every open ticket (backlog and active) is assigned to its stream project. A ticket with no stream is a triage question, not a project of its own.
- New tickets are created INSIDE a stream project. A ticket filed without one gets one at the next sweep.

## 2. Catalogue → disposition (with Kam)
After grouping, each ticket carries one of three dispositions, proposed by the agent and run through with Kam:
1. **Action** — needs nobody outside us AND is actionable now → the standing queue.
2. **Escalate** — needs Kam's ruling or a client human (Stuart, Peter, HP) → a dated card on Kam's desk with a default.
3. **Archive for now** — back-burner or not-yet-possible → **archived, not closed** (Linear unarchives); it stays in its stream project so the whole stream can come back as a set.
Connectors-via-K and commercialisation-readiness tickets default to disposition 3 by Kam's 19:28 word. [OPEN: archive those two classes on grouping, or hold all archiving for the run-through — default HOLD.]

## 3. Peter's test cadence — one stream, one pass
- Tickets in a stream ship on one branch / PR chain (or a coordinated batch) under the project, with ONE evidence set (the four suites + the change's own e2e project) posted on the project, not per ticket.
- Peter is handed the **stream** for review/test when its tickets are all in review — one test pass, one approval decision per stream. A single-ticket stream is still a stream (no artificial batching of unrelated work; no splitting of related work).
- The Linear project carries the SET summary and the PR list; ticket comments point at the project rather than repeating the evidence.
- Hold classes unchanged: nothing merges without Peter's at-head approval (reviews endpoint, not the search index); Peter's own PRs are his to merge.

## 4. Housekeeping
- The morning board leads with: category-1 (actionable now) count, closed since yesterday, and the share of Kam-assigned tickets needing nobody outside us — measured on the catalogued set.
- Archived-not-closed is the ONLY parking state. "Closed as not planned" is not used.
- This document is the process rule; the Linear projects are the instrument; the catalogue run-through with Kam is the review.

## Open questions for Kam (one at a time on the panel)
1. Archive the two named classes on grouping, or hold all archiving for the catalogue run-through? (asked 19:33; default HOLD)
2. [queued] Is "one stream = one PR chain" the intent, or "one stream = one Linear project, PRs stay per ticket, Peter tests the project once"? (default: project-level evidence set + Peter tests the project once; PR granularity left to the agent per change)
