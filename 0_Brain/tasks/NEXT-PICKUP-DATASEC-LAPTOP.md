---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced wholesale at the 65% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~15:5x AEST Monday 2026-09-07

**TWO WEDNESDAYS ARE LIVE.** Studio owns **Secuura** and is active (40 mails in one outage window).
This seat owns **Datasec**. One git repo, one dashboard, one chat panel, ONE USAGE LIMIT.
**Do not write the shared files** (`NEXT-PICKUP.md`, the daily note, `_ledger.md`) — they are hers
this session. Pull before every write. Panel messages from this seat open `[LAPTOP / Datasec]`.

## ⚠️ THE THING THAT WILL BITE YOU FIRST
**`git -C $VARIABLE <writeverb>` is REFUSED by the pretooluse hook** — it matches literal text and
cannot resolve a shell variable, so it fails closed. **Write git paths literally.** It also fires on a
commit message that merely *describes* a git command → write the message to a file and use `-F`.
The hook's hardcoded-root bug (it read this seat's own repo as foreign and blocked ALL commits) was
fixed at `cb646a4a`; root now derives from the hook's own location.

## USAGE — read before spawning anything
**The shared session limit was exhausted at 11:17** by 21 agents in 90 minutes, 12 concurrent. The 12
that completed burned ~3.0M tokens. Reset at 15:00. **Weekly is fine (22%); the SESSION RATE is what
breaks.** Neither seat can see the other's consumption. **Max 3 concurrent agents. Never 12.**

## FLEET — one agent live
**`Datasec/NexusAI` pane `%2`** (ctx ~31%). Working **RD-361** — the Critical auth fail-open — on
branch `rd-361-fail-closed-unknown-s43`, two files edited + a red-proof test written. Conditions set:
fail CLOSED on UNKNOWN, first-run window a SEPARATE stated decision, red-proof against the UNKNOWN
path, **round ends at READY FOR QA not merge**.
**A CORRECTION is QUEUED behind its running turn** (tapped 15:52) — do not close that pane; a queued
tap starts a new turn (ledger 09-06).
Its turn died once to an API error at 15:34; work verified intact at source before resuming.

## WHAT NEXUSAI DELIVERED (verified by readback, not narration)
- **RD-361/362/363/364 filed** under its own identity. Three formally BLOCK RD-13 (the Marketplace
  submission), so the blocker set is legible on the board.
- **THE NUMBER THAT MATTERS: 158 of 285 open tickets are code-complete awaiting a gate, not work.**
  ~102 to write, 158 to verify/land. A throughput problem at the gate, not the keyboard. Cat-1 = 102,
  cat-2 (needs a human) = 18, cat-3 = 4.
- **7 Marketplace blockers named; 4 need a human**: RD-13 (submission, Kam's), RD-18 (Privacy Act),
  RD-54 (rotation needs dev-tenant admin), RD-15 (asset sign-off).
- **RD-300 is `Declined` and still counted open** — board hygiene.
- Read-only duplicate-subject sweep APPROVED (report only, no status changes).

## WEDNESDAY'S OWN ERRORS TODAY — 3 that reached Kam or the board
1. **Consolidation ruled backwards.** I said "keep the earliest"; the agent had argued for the FIX
   ticket and was right. The survivor became a bare Dependabot notification while the reachability
   analysis and fix plan went to `Done`. **Corrected 15:52. The rule is: the survivor is whichever
   ticket represents THE WORK, not whichever arrived first.**
2. **"18 findings" relayed without counting** — it was 17. The agent counted. Register corrected to
   219 estate-wide.
3. **Vision called "live production"** from a stored CLAUDE.md note; Kam says pre-production.
   Defect unchanged, urgency overstated. Same axis as 1 and 2: a claim composed from an artefact.

## SECURITY REVIEW — first pass done, verification INCOMPLETE
**219 findings: 31 June (27 unremediated, ZERO fixed) + 188 new. 15 new Criticals.**
Deliverables current (`.md` + branded `.docx`): `12_Rerun_Delta_2026-09`,
`13_Consolidated_Findings_Register_2026-09`, `11_Assurance_Pack_Index` (rows 1–19 marked as
understating the estate), 13 component summaries, `_Working/{findings-seed,verification,delta-review}-2026-09/`,
`scan-artifacts-2026-09/` (argv recorded per tool).

**STEP 1 (verify) — 9 of 10 files on disk.** MISSING: `infra-administration-portal` — **the one
holding two Criticals.** Do this first.
Verified so far: HP-AuthSuite 12 confirmed/1 UPGRADED (the printer admin password is a **Datasec
cross-product default in 4 components / 5 files**, sent not probed) · Cryptix 28 confirmed/1
downgraded, all 4 Criticals stand · HPSA 16 confirmed/2 downgraded (CK-01 9.3→8.2 on AV:L, mechanism
STRONGER than stated; **the password-assurance statement SURVIVES** with the WebView caveat).

**STEP 2 (delta on the 19 June components) — 8 of 19 done.**
**AWAITING KAM'S STEER:** recommendation is to DROP the remaining 11 to a named gap in the report —
re-reading what June already covered is the lowest-value work and it is where the budget went.

## STILL OPEN FOR KAM
1. **RD-18 Privacy Act** — the real Marketplace exposure. On hold, untouched, needs his timing call.
2. **Delta-review steer** (above).
3. **Re-issue June deliverables 00/03/04/09/10 against 219, or let 12+13 stand as authoritative?**
4. Both June deferred items: live GitHub/Azure/Entra pass; tenant conflict `fc05dcdd` vs `0c57ab37`
   unresolved before any `az`.
5. **Vision PARKED** by his 10:44 ruling until the CRM strategy resolves (`_Working/2026-09-07_VISION_PARKED.md`).

## HALF-BUILT, DO NOT ASSUME IT WORKS
`chat.html` is edited and **UNCOMMITTED/UNVERIFIED** — the per-project chat filter (Kam's 11:12 ask)
was half-built when the limit hit. Backups `*.pre-0907-filter`. Seat-scoped autoplay IS live and
pushed; `chat_reply.sh`'s seat stamp is live locally but NOT yet committed.

## STANDING
No `cd`. Quote every grep glob (zsh `nomatch` = silent zero). Every negative claim needs a positive
control. `send_brief.sh` wants literal `^PROVENANCE:` + `- <fact> | <source> | read YYYY-MM-DD` and
`SELF-CHECK: re-read end-to-end for contradictions | YYYY-MM-DD HH:MM`. Taps ≤200 chars, pointer only,
mail first and verify BODY by `preview` non-null. `<<'EOF'` for every brief, inject values after.
Never delete — quarantine. Rotation band **80–90%** (Kam 10:49).
