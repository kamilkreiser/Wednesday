---
date: 2026-11-04
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 15:05 AEDT 2026-11-04 by the 13:39 seat at its 65% checkpoint. Previous kept as NEXT-PICKUP.md.pre-1104-1505. Replace wholesale; never stack.
---

# NEXT PICKUP — Wed 4 Nov 2026, 15:05 (the 13:39 seat's checkpoint handover)

## KAM'S INSTRUCTION IN FORCE
09:16 (new account): "new account logged in.  Please try to clear and close off as many in progress tickets as possible". Grant row in EXPIRING-GRANTS.

## KAM'S RULINGS THIS AFTERNOON (all 9 cards, live 14:59:57-15:00:57; ruled in the store; receipts on the panel)
disposable-stack = a · ks1234 = a (build prod-mode test) · ks1244 = a (build outright rejection) · ks1233 = b (NEXT DEPLOY SEAT runs the Redis TTL read — put it in the next deploy brief) · ks769 = a (close + dated review ticket + exclusion row repointed) · ks1215 = b, ks1202 = b, ks1639 = a, ks1624 = b (accept / close). Not yet in an artefact: ALL of these until the seats below land them. Use `decision_queue.sh --delivered <id> "<artefact>"` as each lands.

## STATE
- develop = 5c1ca287ed74 (unchanged since 13:28). Kintsugi runs ee1e1b832115 (read by D 50th, U 11th, V 19th). Merges 1996/1994/1989/1995 not deployed; a deploy now would close nothing (only KS-1868 waits, and it has open PR 1968).
- KS In Progress = 238 at 13:43 (board_count); closed today: 91 (84 morning + KS-1822 + 6 by V 19th). Census of the 238: 0_Brain/reference/2026-11-04_ks-inprogress-residue/ (class column is a HINT; ~10-15% misfiles).
- Cards drafts + JSON: 0_Brain/reference/2026-11-04_ks-residue-cards/.

## LIVE SEATS
- **R 84th** (%131, Sonnet, raise): ITEM 0+1 done (PR 1982 CLOSED unmerged 03:55:39Z; PR 1383 STOP: migration backfills + RLS = row C4, needs a decision; KS-1511 branch not ours). Refreshing 1968, 1796, then 1798 (TIER 1: LEVEL_ORDER verification ranking — my ANSWER superseded the brief's C3 hold), then starts Docker and refreshes 1790/1792/1794 (DB-gated suites). 1790/1792/1794/1796/1383 share two Projects Documents docs (append-only): gate as a batch, merge in sequence. Expect ONE READY FOR GATE mail. Then: commission the gate batch (tier 2 Sonnet for test-only; tier 1 Opus for 1798 + 1796 users.ts), then a B-lane merge seat.
- **Pending launch** (brief drafter running at 15:03; READ EACH BRIEF WHOLE, stamp, dry-run, launch): S 17th (Sonnet, rulings records + closes + KS-769 review ticket & one-line PR), T 10th (Sonnet, KS-1234 test), E 34th (Opus, KS-1244 rejection; ask it 400 vs 401 at plan confirmation), W 23rd (Opus, disposable local stack at ee1e1b832115; must NOT start Docker until Wednesday mails that R 84th's Docker-down pushes are done). Files: 2_Project_Files/fleet/briefs_staged/2026-11-04_seat{S17,T10,E34,W23}_*.md.

## WAITING ON KAM
Nothing open (9 Secuura cards all ruled). Tuesday's Datasec card is hers.

## OWED (Wednesday's)
- PR 1383 (KS-1401): migration backfill + RLS + numbering clash — a card for Kam once R 84th's READY mail gives the facts (or a C4 Opus seat).
- KS-1561: Kam ruled build (certify the original registrant) 11-02; needs a BUILD brief.
- CONTRIBUTING N/13 vs TOTAL_LEGS=16 belongs in Stuart's KS-1366: draft at Secuura 5_Project_History/2026-11-04_seatU-12th/drafts/T5_contributing_legs.md; route (Kam's call how).
- KS-911/912 launcher by-hash change: live sha matches neither gated nor shipped — investigate or card.
- Next deploy round (D 51st) when it would close something; carries the KS-1233 Redis TTL read.
- Carried: @azure/msal-node baseline dies MON 2026-11-09 (check its ticket); WED-155 (inbox_digest key in argv); boot-prompt MODEL CHOICE line; INDEX.md refresh (last 10-27); stash@{0} never drop; Spark unreachable from this laptop (zgx-15d5.local does not resolve).

## RULES LEARNED TODAY (this seat)
- A drafter's brief is read WHOLE and every claim the drafter could not open is fixed or marked before send; the gate refuses malformed provenance and unsourced scope words — expect 1-2 fix rounds per brief.
- send_brief refuses routing tokens (hold/stop/checkpoint) inside a subject: never write "hold" mid-subject.
- safe_pull aborts on a digest conflict when both seats regenerated: restore the digests to the merge base in a commit, safe_pull, then regenerate and commit.
- A panel_sync commit can land between your push and your rev-parse: compare with `git ls-remote origin refs/heads/main`.
