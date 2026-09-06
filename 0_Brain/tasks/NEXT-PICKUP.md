---
date: 2026-09-06
type: pickup
source: replaced wholesale at the 2026-09-06 10:3x checkpoint (seat 09:5x, statusline 47%); the 09:5x version's items are actioned or carried below
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — fleet OPEN, two Secuura seats + NexusAI live, one gate running (2026-09-06 10:3x)

**The 2026-08-28 run-until-empty grant is in force; Kam's 09:42 grant put a SECOND Secuura seat in parallel (live since 10:0x).** Live: Secuura seat A s138 (`%74`, product; #839 round 2 HELD under its tier-1 re-gate; then the 18-ticket revert on Kam's 10:24 word; then KS-843; then its seat-A table), Secuura seat B s138b (`%75`, harness, own worktree `worktrees/seat-b`; KS-833 residue PR → KS-842 → KS-845 → KS-847 → its seat-B table), NexusAI S41 (`%72`; RD-340 MERGED `9c8e63a`; now the direction ticket PRICED → `needs-decision` sweep → RD-339 → RD-334 → RD-341), the KS-386 re-gate `%76` (launched 10:27:39, ~35 min; verdict mail `[QA -> Wednesday] Secuura KS-386 RE-GATE @ 3b5a09403 (PR #839, tier 1, round 2 of 2)`). **Their state lives in today's daily note** (the 10:06 seat block and every line after) — this file is only the pointer.

## The successor Wednesday's FIRST ACTS (in order)
0. `tools/kam_rulings_today.sh` (FIVE messages today: 09:36 / 09:42 / 09:45 / 10:23 card A / **10:24 "assigned = theirs; the rule was new/unassigned only"**) + `decision_queue.sh list open` (= 0 at 10:3x). Nothing owed to Kam.
1. **The KS-386 re-gate verdict (`%76`)** → PASS with F-1 both halves + F-1(b) + F-2/F-3 CLOSED by instrument: GO to seat A to merge `3b5a09403` sha-asserted against `develop` re-read (was `33df16814` at 10:23 — seat B may have merged nothing yet; re-derive), KS-386 → Tested Not Deployed; score the QA + s138's round 2 (per-round row); NO GO: the class is at its cap (round 2 of 2) — ship nothing, ticket the residue, tell Kam. `pane_close.sh %76 47787 6882 3001 8731`.
2. **Seat A's revert receipt** (the 18 back to Peter/Stuart from Linear history; the KS-485 comment with Kam's 10:24 words) → `decision_queue.sh --delivered secuura-reassignment-exceptions "KS-485 comment <id>"`.
3. **Seat B's READY** for the KS-833 residue PR → a tier-2 through-code pass (`[SEAT B]` in every subject; its branch `seat-b/…`; its worktree named to the tester; the pair instrument under-counts `packages/shared` by 5 — quote both figures).
4. **S41's next mail** (the direction ticket priced) → rule; `s40-history-docs` stays PARKED until Wednesday reads that branch against `0eec7b8`'s 58 HISTORY.md lines and names the tip (`9c8e63a` now) in a mail.
5. **Owed by Wednesday, not started:** the `coagent@`-sender line into the other QA prompt templates; the watcher `HOLDING until <event>` candidate (FILE or DISCARD at the retro); a `show`-style back-fill for `nexusai-mock-divergence-2026-09-03`'s `ruled_ts` (None in the store; Kam 09-04 07:08 per the 09-04 note); the F-7 run-migrations ticket (seat A files it after the verdict).

## Still Kam's (carried honestly; nothing blocked on him)
1. **Peter and Stuart must be told not to fix KS-790 in isolation** until KS-781's authorize fix lands — external comms, Kam's alone.
2. **RD-303 ruling** (untrack the six `4_Credentials/.azure/` files — committed history) and **RD-75** (the authorisation-chain gap) — both owed a card, neither carded.
3. **`Secuura/Blockchain/4_Credentials/Secuura-git.rtf`** — second live copy of the rotated token; quarantine on his word.
4. **WED-48 overdue** — CypherKey Twilio token rotation (due 09-04).
5. **Five Secuura ruled cards that are his own acts:** `agent-github-identity`, `ps-759-760-merge-owner`, `ks229-disclosure-mailbox`, `ci-billing`, `dependabot-triage`.
6. **On his panel with defaults:** KS-835, KS-841, the RD-333 pairs (NO deploy without his word), the demo-service stack-trace finding (now KS-844).
7. **Weekly usage** read 83% at 10:29, resets 12:00 — five sessions live; a cap hit stalls everything until the reset.

## Standing operational notes
See the 09-04 note's §9 list in `0_Brain/daily/2026-09-04.md`. **New this seat:** a pane NAME is registered in BOTH `cockpit/launchers.conf` AND `fleet/inbox_routing.conf` (say --mail resolves names in the second; `Secuura/Blockchain-B` is now in both); the inbox is listed WHOLE, never tailed; a section of a card is bounded by its next heading found by search, never a line number; a python step that can raise is never chained ahead of a send in one call; NEVER `git fetch` in an agent's checkout — `ls-remote` + the agent's DKIM'd receipt, or clone by SHA into the scratchpad. The Secuura category-1 LIST (119 / 31 / 13 / 45 of 208 at 10:16) is in `projects_index/entries/Secuura__Blockchain.md` and in both seats' inboxes. Vision (VSP) has 0 open Jira issues (64 Done; positive control run) — nothing to launch there. `board_count.sh linear LINEAR_API_KEY '<GraphQL object, unquoted keys>'`; `board_count.sh jira <site> <email> <token> '<jql>'`. The Secuura seats run on Opus 5 by their launcher's fallback. An untracked `.claude/settings.local (conflict_on_2026-09-04).json` sits in the tree (reported, never removed).
