---
date: 2026-09-06
type: pickup
source: replaced wholesale at the 2026-09-06 11:1x handover refresh (seat 09:5x, statusline 65%); the 10:3x version's items are actioned or carried below
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — fleet OPEN, two Secuura seats + NexusAI live, one gate running (2026-09-06 11:1x)

**The 2026-08-28 run-until-empty grant is in force; Kam's 09:42 grant put a SECOND Secuura seat in parallel.** Live: seat A s138 (`%74`, product — KS-843 half 2 building per the 11:03 rulings; #841 half 1 HELD under `%78`), seat B s138b (`%75`, harness, worktree `worktrees/seat-b` — the #840 merge GO delivered 11:07, receipt due), NexusAI S41 (`%72` — RD-339 one round with RD-347), the KS-843 half-1 gate `%78` (launched 11:05:46, ~20 min). **Their state lives in today's daily note** (the 10:06 seat block and every line after; the 11:10 handover block) — this file is only the pointer.

## The successor Wednesday's FIRST ACTS (in order)
0. `tools/kam_rulings_today.sh` (NINE messages today — 09:36 / 09:42 / 09:45 / 10:23 / 10:24 "assigned = theirs, new/unassigned only" / 10:52 ×4 all A) + `decision_queue.sh list open` (= 1: `secuura-ks843-cutover-stuart`, default deploys nothing). **The inbox is read WHOLE to a file (`inbox_digest.sh > state/inbox_now.txt`), never piped through `head`/`tail` — twice this seat a cap hid a message.** Every send ends with its verified `cockpit.sh say … --mail` tap in the SAME response.
1. **Seat B's #840 merge receipt** → verify at origin (`ls-remote develop`; parents via the shared object store, NO fetch); KS-850 TND; then its KS-833 residues PR READY → a tier-2 through-code gate; then its F-850-01 ticket + PR (leg 9 of preflight BLIND in worktree hooks — HIGH; the docblock fixes folded in) → tier-2 gate with the double-environment red-proof and the "still fails on a real tracked credential" control.
2. **The #841 half-1 verdict (`%78`)** → PASS with nothing already-issued changing behaviour: GO to seat A to merge `4111f409e` sha-asserted against develop re-read; KS-843 stays In Progress (half 2 open); `pane_close.sh %78 47787 6882 3001 8731`. The next seat-A mail also carries the owed correction: the 11:03 rulings mail said the cutover was "carded" before the card gate's refusal was read (it is carded now, second try).
3. **Seat A's half-2 READY** (role-OR-scope + refusal log + scope-only switch default OFF; both routes; new test files only; the `anchors:write` mount-order probe; KS-577 named as window and defect) → tier-1 gate; NO deploy — the cutover is Kam's card.
4. **S41's RD-339 READY** (authoritative helpers read from `server.js` at run time; the jest wrapper asserting exit AND count; the ten in the pin; the dead probe removed; the false comment rewritten; failures against unreached product paths REPORTED not tuned) → tier-2 gate; then RD-180 + RD-251 one branch (browser gate, both modes; NO deploy without Kam); then RD-334 → RD-341. `s40-history-docs` stays PARKED until Wednesday reads it. RD-346 ruled when RD-334 gives the reader a consumer.
5. **Owed by Wednesday, not started:** the `coagent@`-sender line into the other QA prompt templates; the watcher `HOLDING until <event>` candidate (FILE or DISCARD at the retro); `ruled_ts` back-fill for `nexusai-mock-divergence-2026-09-03`; enforcement candidates named this seat — `inbox_digest.sh --inbound` (unbounded), `send_brief.sh --tap`, a brief naming a card id refused unless `show <id>` succeeds; the 09-05 retro is still owed (the 22:5x seat's note said so) — check whether a later seat wrote it before writing it again.

## Still Kam's (carried honestly; nothing blocked on him)
1. **`secuura-ks843-cutover-stuart`** — the only open card (rec A logged grace; default: nothing deploys under the demo hold; the Stuart ask goes from Kam as a test block: how many connector keys S holds against K demo, and a swap window).
2. **RD-75 paste** — ruled A 10:52; the lines are drafted at `5_Project_History/2026-09-06_rd75-dkim-recipe-for-workspace-claude-md.md` for HIM to paste into the workspace `CLAUDE.md` (Agent Mail section); S41 re-measures and closes criterion 3 after.
3. **A DEPLOY is OWED on KS-386** (`b6ae609e6`; kyc + two init schemas) — held under his demo stop (demo-service, KS-641); deploys with the TND batch when he lifts it.
4. **Peter and Stuart must be told not to fix KS-790 in isolation** until KS-781's authorize fix lands — external comms, his alone. **Peter's approvals** now owed on #840, #841 and the coming residues PR — the next test block.
5. **RD-303 ruling** (untrack the six `4_Credentials/.azure/` files — committed history) — owed a card, not carded.
6. **`Secuura/Blockchain/4_Credentials/Secuura-git.rtf`** — second live copy of the rotated token; quarantine on his word.
7. **WED-48 overdue** — CypherKey Twilio token rotation (due 09-04).
8. **Five Secuura ruled cards that are his own acts:** `agent-github-identity`, `ps-759-760-merge-owner`, `ks229-disclosure-mailbox`, `ci-billing`, `dependabot-triage`.
9. **On his panel with defaults:** KS-835, KS-841, the RD-333 pairs (NO deploy without his word), KS-844.
10. **Weekly usage** read 86% at 11:07, resets 12:00 — four sessions + one gate live.

## Standing operational notes
See the 09-04 note's §9 list in `0_Brain/daily/2026-09-04.md`. **This seat:** a pane NAME is registered in BOTH `cockpit/launchers.conf` AND `fleet/inbox_routing.conf` (`Secuura/Blockchain-B` is in both); a section of a card is bounded by its next heading found by search, never a line number; a python step that can raise is never chained ahead of a send; NEVER `git fetch` in an agent's checkout — `ls-remote` + the shared object store (worktrees share it) or the agent's DKIM'd receipt; the QA project path carries `!CODING` (`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/`); a red-proof's rc is read BARE (`> file; rc=$?`), never through a pipe (zsh has no PIPESTATUS); a count of "N of these are yours" is computed, never guessed. The Secuura category-1 LIST (119 / 31 / 13 / 45 of 208 at 10:16; the 18 restored tickets are category 2 since 10:32) is in `projects_index/entries/Secuura__Blockchain.md` and in both seats' inboxes. Vision (VSP) has 0 open Jira issues (64 Done). `board_count.sh linear LINEAR_API_KEY '<GraphQL object, unquoted keys>'`; `board_count.sh jira <site> <email> <token> '<jql>'`. The Secuura seats run on Opus 5 by their launcher's fallback. An untracked `.claude/settings.local (conflict_on_2026-09-04).json` sits in the tree (reported, never removed).
