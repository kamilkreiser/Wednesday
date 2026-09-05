---
date: 2026-09-06
type: pickup
source: replaced wholesale at the 2026-09-06 08:0x checkpoint (seat 07:4x); the 09-05 version's items are either actioned or carried below
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — fleet OPEN, both projects mid-round (2026-09-06 08:0x)

**The 2026-08-28 run-until-empty grant is in force.** Secuura s137 (`%68`, launched 07:54) and NexusAI S40 (`%63`, launched 06:14) are running on briefs; **their state lives in today's daily note** (the 08:01 checkpoint block and every line after it) — this file is only the pointer.

## Still Kam's (unchanged from the 09-04/09-05 pickups, carried honestly)
1. **Peter and Stuart must be told not to fix KS-790 in isolation** until KS-781's authorize fix lands — external comms, Kam's alone. (KS-781's door 1 shipped in #812; KS-790 carries the "blocked by KS-781" relation on the board; the human word is still his.)
2. **RD-303 ruling** — untrack the six `4_Credentials/.azure/` files in NexusAI (touches committed history). **RD-75 ruling** — the authorisation-chain gap. Both owed a card; neither carded yet (the card gate refuses nothing on them — no prior ruling — so they are simply not yet written).
3. **`Secuura/Blockchain/4_Credentials/Secuura-git.rtf`** — second live copy of the rotated token, 0644, in a synced folder. Offer stands: quarantine on Kam's word (never delete). The token is still named `claude-ci-read` while holding admin+push.
4. **WED-48 overdue** — CypherKey Twilio token rotation was due 2026-09-04 (Kam's hands; CypherKey is outside the morning sweep).
5. **On his panel with defaults (no decision required):** KS-835 (OAuth consent decorative — the reach question; default: stays High, nobody told) · KS-841 (the consent page cannot POST itself back; mount sentence now covers local, VM demo, production, staging, CI, isolation + three overlays — a repo read; default unchanged) · the RD-333 light/dark pairs (merged on his silence; NO deploy without his word).

## Owed by Wednesday, not yet done (stated so the next seat does not re-derive it)
- The per-card delivery sweep of the ~35 Secuura ruled cards dated 2026-09-02 and earlier (`decision_queue.sh list ruled --undelivered secuura-` = 57 at 08:0x; twelve 09-03/04 cards are with s137 as VERIFY-and-WRITE; four marked delivered this morning). Each is a board or repo read; a bounded batch per successor brief is the pattern.
- The QA-charter known-fragile line (Linear's `Entity not found: Issue` on an archived ticket's `commentCreate` — a refusal indistinguishable from a wrong id without a control) — in hand at 08:0x.
- Tooling items sized, not built: the QA prompt should name `coagent@` as the sender explicitly (the KS-822 re-gate verdict went out FROM the project's inbox); `decision_queue.sh show <id>` (~15 lines); `send_brief.sh --subject-file` (~10 lines).

## Standing operational notes
See the 09-04 note's §9 list in `0_Brain/daily/2026-09-04.md` (pane NAMES not %ids for `cockpit.sh say`; `rc=2` is the sync's normal exit; Wednesday's own pre-commit secret scan now REFUSES on a token-body pattern in the commit command — the hook extension is still unbuilt). `board_count.sh linear` takes a GraphQL object with unquoted keys. The inbox is listed WHOLE, never tailed. The Secuura seat runs on Opus 5 by its launcher's fallback (Kam 2026-09-05) — recorded, not changed.
