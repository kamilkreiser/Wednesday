---
date: 2026-11-16
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, WRAP 2026-11-16 ~17:0x (Kam: "wrap up… we will pick this up tomorrow… start the next session with a review")
supersede: replace wholesale; previous (471 KB of prepended blocks, 2026-09-27 → 2026-10-16) = NEXT-PICKUP-FRIDAY.md.pre-1116-wrap, read on demand only
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Volumes/Laptop-DEV/FRIDAY` (machine: Kamils-MBP).** Quote every path. Friday runs on **Fable** (Kam switched the seat 2026-11-16; saved as the default).

## 🔴 FIRST ACT of the next session — Kam's words: "we will start the next session with a review"

The review is of the **Claude to Claude (CoAgent) design**. Client: **General** (a side project of Kam's; not Secuura, not Datasec). Friday holds the claim `General/Claude to Claude — Friday (laptop)` (kept across the wrap on purpose).

1. Run `kam_rulings_today.sh` and `decision_queue.sh list open`: two cards wait on Kam.
   - `general-c2c-design-go-1116` — a = go with all 12 defaults (D1–D12) and start M0; b = change decisions first; c = hold. **Default: nothing is built.**
   - `general-c2c-v044-withdraw-rotate-1116` — withdraw the v0.4.4 download and rotate the credentials found on disk. **Kam's own action; Friday touches nothing.**
2. Walk Kam through the design (he has the PDF, 24 pages, shared to his Friday tab as file_id f-a27bbae499). One question per turn.
3. **Before the review, Friday reads the design sections she has NOT read: 4 (linking/identity), 5 (the two modes), 8 (phase 2), 9 (security), 10 (wire protocol), 11 (tech + repo layout).** Read on 2026-11-16: 1–3, 6–7, 12–13. Do not endorse the unread half.

## Where everything is

`0_Brain/reference/2026-11-16_claude-to-claude/`
- `00_requirements.md` — Kam's requirements, R-LINK … R-BROWSER (verbatim prompts are in `1_Project_Definition/Discovery/00_prompt-log.md`).
- `01_existing-code-review.md` — Fable agent, read-only review of v0.4.4. Verdict: encrypted chat bridge, not an action gate; rewrite the core.
- `02_prior-art-research.md` — Fable agent, 44 dated sources. Caveat: pages were read through a summarising fetcher; field names must be re-opened before they are pinned in code.
- `03_architecture-design.md` — Fable agent, 1,011 lines. `CoAgent_architecture-design_2026-11-16.pdf` is its render (`tools/md2pdf/md2pdf.sh`).

The project itself (READ-ONLY to Friday): `/Volumes/Laptop-DEV/!CODING/Claude to Claude/claude-bridge` — v0.4.4, ~3.5K lines of JS, **not a git repository**. It has its own `Launch_Claude.command` and `CLAUDE.md` (neither read by Friday yet: read both before briefing a project agent).

## The design in six lines (from the sections Friday read)

- A local daemon per machine holds policy, approvals, grants and the audit log; Claude Code's `PreToolUse` hook is the gate (a program, not an instruction).
- Phase 1: the guest ASKS, the host's own agent ACTS; anything sent back to the guest is itself a gated action.
- Pairing: short spoken code → PAKE → Noise handshake → three verify-words → remembered contact; content-blind relay; no accounts.
- CONTROLLED = approve each action; APPROVED TRUST = scoped, time-boxed grant, revocable, with an always-ask class.
- Two doors, one session: `/collaborate` (plugin command is `/coagent:collaborate`; the bare name needs one optional personal-skill file) and a full browser console with an embedded terminal.
- Phase 2: host daemon as an ACP client; phase 1 estimated 28–39 agent-days; M0 = throwaway spikes that settle the UNVERIFIED list in Appendix B.

## If Kam says GO (card a)

Friday does NOT build: she briefs a project agent (manage, don't do). Before the first brief: read the project's own CLAUDE.md and launcher; decide WITH KAM where the new repository lives (the design says a fresh repo, old tree archived as `legacy/`; D1 names it); model per `fleet/specs/model-routing.md`, except analysis/design agents on the newest Fable (`learnings/2026-11-16_architecture-agents-run-on-the-newest-fable.md`). Whether BUILD seats also run on Fable is NOT ruled: ask.

## OWED (Friday)

- Shared hook change (`2_Project_Files/tuesday/hooks/pretooluse_inbox_scope.sh`, commit e30563fa5d: own inbox looked up in `fleet/inbox_routing.conf`) was MAILED to both sisters at the wrap (threads fa7f0784-5052-471b-89c4-62a5c6ecdf74 Wednesday, 412cc0c8-61e3-41be-9197-ca0a9328f6c1 Tuesday). Neither has run it on her machine: if either reports her own inbox refused, that is the first suspect.
- Linear: **WED-162** tracks the Claude to Claude review + M0.
- Tuesday was mailed Kam's 2026-11-16 16:37 ruling `a` on the old card `composer-l05-setup-card-too-1014` (Datasec/Security-Composer, hers). Check for her acknowledgement; the ruling sits on no ticket yet.
- Still open from 10-16, said once to Kam, not carded: add Laptop-DEV to Spotlight Privacy; Disk Utility First Aid on Laptop-DEV. Wordsplit hook: refuse unquoted `$(ls …)` in a `for` list (ledger w=5, 10-15).
- Stale Friday claims still OPEN in `wed_claim.sh list` (Kamils-MBP / Kamils-MacBook-Pro rows from 09-25 → 11-06, several were Wednesday's while she ran on the laptop): review and release only the ones that are Friday's.
- Linear WED: WED-48 (Twilio token tickler, due 09-04) and WED-147 (due 09-14) overdue; the board has not moved since mid-September.

## Standing facts a cold seat needs

- Friday drives NO Datasec and NO Secuura project today. HPSM-POC, MPS calculator, Security Composer and HPSM records are Tuesday's (handover `0_Brain/handover/2026-10-15_friday-to-tuesday/`).
- Wednesday's seat is the always-on Mac mini (2026-11-11). The Spark went back to HP 2026-11-15: never route to it.
- Friday's inbox is `friday-laptop-agent@agentmail.to`. Last inbound before this session: 2026-10-13.
- The by-tier boot digest is ~700 KB: it does not fit one read. Read every headline, open a lesson when its rule fires. After the 11-16 load the statusline read ctx:14%.
- Friday's ledger was archived at this wrap (130 rows → `_ledger_friday_archive.md`); the live ledger holds the four 11-16 rows.
- **Never run `tools/panel_sync.sh` bare**: it does not return. The launcher runs `panel_sync.sh loop`, which commits dashboard data and pushes. A seat pushes its own commits with plain `git push` (ledger 2026-11-16).
- No live grant names Friday in `EXPIRING-GRANTS.md` (the last two expired 10-11 and 10-15). WEEK-INSTRUCTION-FRIDAY lapsed 2026-09-26.
