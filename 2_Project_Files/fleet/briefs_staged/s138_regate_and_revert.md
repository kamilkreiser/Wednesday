## BLUF
**Three things, in this order: (1) KAM RULED at 10:24 — the 18 tickets you moved off Peter (16) and Stuart (2) go BACK to them, now; (2) your #839 round 2 is under its tier-1 re-gate (pane `QA/Secuura-s138-ks386-regate`, launched 10:27:39 AEST, ~35 min) — HOLD the branch; (3) two of Wednesday's own errors in the fix-round ruling are owned below (F-1's second half; the F-7 pointer), and your reading of the order is confirmed: re-gate verdict → KS-843 → then the top of your seat-A table.**

## 1. KAM'S RULING — revert the 18, keep the 95
Kam ruled card `secuura-reassignment-exceptions` **A** (the seven stay) and then wrote, verbatim (panel 10:24): *"once something is assigned to someone it belongs to them. the ruling was only to new or unassigned items."* So his 09:42 rule covered the 95 UNASSIGNED and every new filing — not the humans' existing tickets. Wednesday's brief read "every item" wider than he meant; the 18 moves were Wednesday's instruction, not your error.
- **Restore exactly the 18** to their previous assignee. Source of the list: **Linear's own history**, not memory — for each of Peter's and Stuart's former tickets, the `issue.history` entries where `fromAssignee` is peter@obeden.com or stuart.jamieson@secuura.ai and `toAssignee` is the board account, `createdAt` after 2026-09-05T23:50Z, by the board account. Predict 16 + 2 = 18; if the history returns a different count, STOP and mail the ids you found. Restore by `issueUpdate` on the assignee field only; state count before/after; nothing else on those tickets changes.
- **The seven exceptions stay as they are** (they were never moved). The 95 formerly unassigned and the five filings stay with us. Kam's own account IS the board account.
- **Write on KS-485**, beside your exceptions comment (`dae8e0fc`), ONE comment carrying Kam's two sentences verbatim with the date/time, the count restored, and the standing rule from here: new and unassigned → the board account; anything on a human stays theirs unless Kam says otherwise per ticket. Mail the comment id — Wednesday marks the card delivered from it.

## 2. The re-gate — HOLD
Brief `2026-09-06_secuura-ks386-839-regate-3b5a09403-tier1.md`: three schemas (init.sql alone at the head; the docker init file alone at the head; the OLD init.sql at `8b91ab0ae`), the driven flow on the two fresh-init schemas, the 500 at the wire on the old one, the guard's matrix and the new reader on hostile input, SETS 22 → 26. Your probe container `ks386-probe-pg` is named to the tester as YOURS, untouched. No commit on the branch until the verdict arrives by mail from Wednesday.

## 3. Owned by Wednesday
- **F-1 had a second half and Wednesday's ruling named only the NOT NULL.** You measured the INSERT against the schema and found `user_id` missing first; the fix you extended to is the right one and is under test as claim 1. Ledger row on Wednesday's side (the fix scoped to the finding instead of measured against the statement).
- **"BACKLOG #6 already" was a pointer Wednesday carried from the tester's aside and never opened.** Your reading stands: the live register has no entry; the stale `Blockchain/Dev/BACKLOG.md` marks the exit-0 as deliberate. **Disposition, re-ruled on your measurement:** ONE ticket, category 1, Low — "`run-migrations.sh` exits 0 on partial failure; the only record is a stale register marked done" — file it after the re-gate verdict, not now; the tester is told to read the runner's ledger, not its exit.
- KS-848 (F-4, harness) and KS-849 (F-5, product) — received; KS-848 is seat B's by partition, KS-849 yours, both selectable from the table later.

## 4. Order confirmed
Re-gate verdict (Wednesday's GO/NO GO) → KS-843 (as ACKed) → thereafter the top row of your seat-A table by priority then id. Item 1 above (the revert + the KS-485 comment) runs NOW, while the gate runs — it is board work, not branch work.

PROVENANCE:
- Kam's ruling A + his 10:24 note, verbatim | `chat_log.json` via `tools/kam_rulings_today.sh`; card ruled via `decision_queue.sh rule … A` (receipt `ruled: … -> A`) | read 2026-09-06 10:24
- Your before/after counts (Peter 19 → 3, Stuart 6 → 4; 18 issueUpdate calls) and the KS-485 comment id | your ITEM 0 DONE mail 2026-09-05T23:56:49Z, read whole | read 2026-09-06 10:0x
- Your READY (round 2 @ `3b5a09403`; F-1's second half with the error text; F-2/F-3 closed; KS-848/849; F-7's stale-register finding; the order question) | `[Secuura/Blockchain -> Wednesday] READY: #839 round 2 @ 3b5a09403 …` 2026-09-06T00:21:50Z, read whole | read 2026-09-06 10:2x
- The re-gate pane | `cockpit.sh add` receipt `pane 'QA/Secuura-s138-ks386-regate' added (%76)` at 10:27:39; wrapper `--check` rc 0, refusal paths red-proofed rc 6 / rc 7 | read 2026-09-06 10:27
- `refs/heads/kamilkreiser/ks-386-stop-storing-kyc-images` = `3b5a094032791e4f1a5d6d5b9e6b2f713f94bb4e`; `develop` = `33df16814` | `git ls-remote origin` from Wednesday's seat | read 2026-09-06 10:23

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-06 10:28
(checked: this SUPERSEDES item 0(a)'s "reassign Peter's 19 and Stuart's 6 unless…" in the s138 successor brief — by Kam's word, named; the seven exceptions are stated once as unchanged; the order (re-gate → KS-843 → table) matches the item-0 ACK and the addendum; F-7's disposition is re-ruled once and names what it replaces; the hold on the branch is restated identically to the fix-round ruling.)
