---
date: 2026-09-06
type: pickup
source: replaced wholesale by the 20:1x seat at its 50% checkpoint (21:2x)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Secuura running FOUR panes (2 builders, 2 testers); NexusAI PAUSED; Kam's queue = 1 card; Wednesday boots on OPUS for the week

**Kam tonight, both verbatim, both already executed:**
1. **20:19 — "please change your boot script for the rest of the week to boot in opus 5 rather than fable. we are burning through credits a little too quickly."** DONE: `Launch_Wednesday.command` pins `--model opus` (the fable+fallback line commented in place; backup `Launch_Wednesday.command.pre-0906-opus`), and **`doctor.sh` holds the date — ok until 2026-09-13, WARN after**, both branches exercised. The week-end date is Wednesday's reading, stated to him as an assumption. Lesson: [[2026-09-06_a-scoped-override-carries-its-own-expiry]]. **Revert = restore the commented line.**
2. **20:19 — "keep pushing the secuura agent to polish the platform to a ready state."** The sort key for both Secuura seats' free-choice items; delivered into both seats' briefs, not left on the panel.

## 🔴 A CONSTRAINT WEDNESDAY TOOK, and it binds the successor
**Seat B's item-4 launcher change (KS-911/912) is LIVE ON DISK and UNGATED** — `Launch_Claude.command` sha256 `932a2cc3…`, suite `b93b2c83…`; the `.pre-` copies (`…command.pre-ks911` `9609c845…`, `…seats.test.sh.pre-ks912` `a5d5d9ef…`) equal KS-907's gated hashes exactly. **Do NOT relaunch or rotate a Secuura seat until that change is gated — or restore both `.pre-` copies first with one `cp` each and say so in the brief.** Its gate is third in the tester queue.

## The floor at 21:2x (heads from `ls-remote`, READ verbs only in agents' checkouts)
- **Secuura develop = `a821bd0aad137347954a287707e573e417e8ce9d`** — verified from objects: `a821bd0aa` = #865 merge (parents `e1d840d8e` + `beb370d4e`), `e1d840d8e` = #863 merge (parents `b77b20bf6` + `6fa8e5e0a`). Both landed by seat B after Wednesday's pane-close cost the first push. **The local `refs/heads/develop` is STALE at `b77b20bf6`** — read `origin/develop`, never the branch name.
- **`%121` seat A (s141)** — on the **#868 fix round, round 1 of 2 under the cap**. Its READY is owed. Also holds #867 (PASS, merges after the ORG_ADMIN one-liner) and #870 (KS-921, under gate).
- **`%119` seat B (s140d)** — on **item 5**, the seat-B table sorted by Kam's direction, by-path confirmation before each cut. Holds #866 (KS-909, ungated) and #869 (KS-923, under gate) and the item-4 launcher change (ungated).
- **`%122` tester — #869 (KS-923), tier 2.** **`%123` tester — #870 (KS-921), tier 1.** Both launched with wrappers red-proofed rc 6 / rc 7.
- **NexusAI: PAUSED on Kam's 17:01 word.** No pane. Resume only on his word, at `!CODING/Datasec/NexusAI/HANDOVER-S42.md` §2.

## Owed by the successor, in order
1. **The two verdicts** (#869, #870) → read whole → score → GO by SHA or a fix round. #870 is tier 1: its guard blocks every push, so a false-BLOCK finding matters as much as a false-CLEAN one.
2. **Seat A's #868 fix-round READY** → gate (round 1 of 2; a second NO GO ships what is closed and tickets the residue; a third needs Kam).
3. **#867's corrected head SHA** → verify the ORG_ADMIN count independently (it is **4 ORG_ADMIN / 10 OWNER** over the 14 `hash: ADMIN123` rows — measured here with the OWNER count as the control) → GO the merge. **B-2 rides on Kam's card:** the replaced row collides with nothing, so the next `/seed-demo-users` INSERTS a new live ORG_ADMIN with the published `admin123` hash. Told to him 21:0x.
4. **The item-4 launcher gate** (third in the queue) → then the relaunch constraint above lifts.
5. **#866 (KS-909)** still ungated — deliberately held to keep the tester count at two.
6. **KS-926 (P2)** — **3 of 20 guards reachable**, four wired to retired GitHub Actions (incl. SQL-injection and trust-header-read checks). Ruled: disposition **per guard**, wire / re-home / retire, **push cost measured BEFORE any proposal**. A campaign, after the fix round and KS-920. Kam told as context on his ruled `secuura-ci-billing` card.
7. **Kam's card** `secuura-demo-kam-admin-default-password` (open, default HOLD) → if he rules, RULING RELAY to seat A + `--delivered`.

## Standing operational notes (carried + new tonight)
Everything from the 20:1x pickup still holds, plus: **a card add is ALWAYS its own tool call**; **a wrapped agent's pane is closed only when no tap is queued AND a capture shows no spinner**; **never `fetch`/`merge-tree --write-tree`/`worktree add` in an agent's checkout**; **the SELF-CHECK line is the canonical sentence + `| $(date)` with NOTHING between them** and every provenance entry carries three fields even when the middle is "not read"; **a provenance path outside Wednesday's tree is absolute or names its owner**; **`rm -f` exits 0 on a path that does not exist and zsh does not word-split — the control is the listing afterwards** (four silent-instrument instances across the fleet today); **an instrument is not evidence until it has produced the other answer in the same batch**; **a control that mutates its subject is not a control — `git show`, never `git checkout`, in a tree another seat holds**. Wednesday's own model: booted Fable 5.1, statusline read **Opus 5 (1M context)** from 20:3x — recorded as measured.
