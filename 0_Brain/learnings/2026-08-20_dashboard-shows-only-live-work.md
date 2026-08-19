---
date: 2026-08-20
type: preference
source: "Kam, 2026-08-20 morning (dictated): 'on the dashboard, please review if any items have been completed, and once they get complete, do move them off the dashboard'"
status: live
supersedes: ""
---

# The dashboard shows only live work — completed items come off when they complete

**The operative case:** an item on any dashboard tile (tickets, parking lot, flags)
has been completed, superseded, or time-expired. **It comes off the rendering
surface the same session its completion is verified — the dashboard is Kam's
reading surface, and a completed item still displaying is a stale representation
he has to re-derive around.**

**What prompted it:** on 2026-08-20 the tickets tile was showing the Secuura
s39-era queue (KS-488/KS-647 — Done on the board since 08-17/08-18), NexusAI's
"deploy if authorised" list (shipped 08-17, rev `--0000084`), and HPSM's "~08-17
sitting consumes the pack" (HPSM-13 Done). The tile renders the FIRST
`**Open / next:**` block of each `projects_index/entries/` card — the cards had
newer narrative at the top but their Open/next sections were frozen at older
sessions.

**How to apply:**
1. **Verify before removing** ([[2026-08-03_mental-model-not-source-of-truth]]):
   completion is confirmed at the source — board state, HISTORY.md, a receipt —
   never inferred from my own notes. Today's pass: KS-488/647 via live Linear,
   NexusAI via its HISTORY.md sessions 29–30, HPSM-13 via live Jira.
2. **Move, don't delete:** the item goes to a `**Completed (moved off the
   dashboard YYYY-MM-DD):**` section in the same card, with the verification
   named. The bold heading stops the tile regex, so the record survives without
   rendering.
3. **The check is part of the morning sweep and every wrap:** when a board read
   or a wrap mail shows an item finished, the card's Open/next is updated in the
   same action — not left for a future cleanup pass.
4. **Freshness is honest:** bump the card's `updated:` frontmatter when the
   Open/next is refreshed, since the tile displays it.
5. Same family as [[2026-08-16_an-overstated-record-gets-discounted-wholesale]]:
   a tile carrying dead items gets discounted wholesale, and the discount lands
   on the live ones.

**Related:** [[2026-08-17_conversation-needs-a-stable-panel]] (the dashboard is
a reading surface, and the reader must never reconstruct),
[[2026-08-05_life-os-commission-principles]] (rule 2: the dashboard is an
instrument I play — curation is the job), [[2026-08-06_bluf-write-for-the-reader]]
