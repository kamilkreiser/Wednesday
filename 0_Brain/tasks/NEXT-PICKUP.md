---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 08:4x Wednesday seat at its 50% checkpoint, 2026-10-19 ~09:3x. Replace wholesale again; never stack. Previous version: NEXT-PICKUP.md.pre-1019-0930 + git.
---

# NEXT PICKUP (Mon 19 Oct, mid-morning)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh, reconcile_rulings.py, `tools/newmail.sh` (to a file, never piped; the path is tools/, not fleet/), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`.
2. **Kam's instruction in force (EXPIRING-GRANTS top row, 10-18 ~19:0x, no expiry, tied to this account):** work the Secuura tickets and backlog, feed the Spark as many tickets as it can handle, routing definition. Routing v1.0 IN FORCE (every launch receipt names its row). Gauge 22% at 09:29.
3. **The morning receipt WAS sent (06:10).** Weekly consolidation is DONE (catch-up this morning). WED-154 storage policy APPROVED by Kam 07:24 and executing (Seat D).
4. Commit your own files BEFORE any tool that pulls. wed_claim.sh now REFUSES rc 9 on dirty tracked files outside dashboard/data (fixed 08:55, commit 2bbe4653c).

## 1. LIVE WORK (09:3x)
- **develop = f95ad12fe5c22f8d037e7139d052363422463c79** (ls-remote 09:3x). 26 Secuura merges since 19:00 Sun. Nothing deployed.
- **#1589 (KS-1628 PR 2): GATE N1 = GO WITH NOTE** (Opus, round 2 of 2, sha 46f8f032c375a8a4 re-hashed EQUAL, control differs; verdict 0_Brain/reference/2026-10-19_gate-N1-pr1589-r2/verdict.md). **GO SENT 09:3x to the R lane: merge at head ae9dd501b697, pinned.** On R's MERGED mail: ls-remote develop, compare with R's report, note it. R files ONE Low follow-up ticket (Minor 1 app-level re-add cell, Minor 2 README count, Nits 1-3) and adds the gate's external-caller sentence to KS-1634.
- **KS-1634 (High), the live honest-labelling defect:** a simulated anchor reads as on-chain through originate's chain-first fallback (`verification.ts:712` and `:1191`). Census read-only on both boxes = 0 reachable today (kintsugi's zero is contingent on 2 document rows; demo's is structural); stays High. **Fix = two Spark PASSes, read at source by Wednesday and HELD:** `local-model/night/READY_KS-1634-VERIFYFILESIMULATED-1_...` and `READY_KS-1634-VERIFYSIMULATED-1_...`. R raises them as ONE PR (p2's test file renamed `...-verify-route.test.ts`, expect originate 1454), folded into the TIER-1 batched READY, ahead of the other Spark PRs. Three gate questions: `=== true` everywhere on the chain-first path; does carrying `simulated` change a real anchor's answer; can anchoring's Blockfrost chain-scan branch return a placeholder hash.
- **Seat R 50th** (%8, Opus 5.5): the #1589 merge, then the 6 held Spark pushes (1 of 6 was in flight at 22:29Z) + #1590 + KS-1634, ONE batched READY (tier 1: KS-1628 item 3, KS-1595, KS-1634; tier 2: the rest) -> Wednesday launches the gate(s). Then KS-1622's widened scope (four shapes + the same warn line) as R's OWN Claude build: the Spark's one rebrief is SPENT (SCREEN_7), so no Spark round on it.
- **Seat D 20th** (%7, switched to Opus 5.5 at 08:5x): storage removal: T done, N done (97 GiB at 08:40), E 35/35 clean, **W 145 running** (started 09:06). On its wrap STATUS: read df before/after, verify the shared checkout (HEAD, ref count), score, retire the pane BY HAND (it will have wrapped: the rotate-is-for-an-unwrapped-seat lesson), and tell Kam the freed GB on the panel. Then Wednesday removes class R (local-model run clones) herself. 27 squash-ambiguous W candidates stay skipped (a round 2 under a named predicate, Kam's to approve).
- **Seat J 13th** (%6): builds nothing. It waits on Kam's card `secuura-ks1612-round3-nogo-1019` (rec a: a narrow round 4; default b: hold). Design-only prep is allowed. On (a): Wednesday rules J's design, then a full Opus gate.
- **Spark:** SCREEN_10 drafter running (Agent tool, Sonnet; up to 4 briefs at rung 2+, excludes every live-lane file; report 0_Brain/reference/2026-10-18_spark-screen/SCREEN_10.md). On completion: read every PASS's product hunk at source, hold_ready (ROWID never starts with KS-), queue to R.

## 1c. KAM RULED 11:07-11:08 (four taps) — status of each
- `secuura-datasec-author-on-two-branch-commits-1019` = **b**: GO sent to R (force-push #1597, author only, tree asserted, a datasec search on the commit list = 0). On R's mail: ls-remote #1597's new head; it rides in the batched READY at its NEW head. Then `decision_queue.sh --delivered`.
- `secuura-ks1612-round3-nogo-1019` = **a** (narrow round 4, the LAST): J 13th told to mail its DESIGN first (the deciding question: does dropping 051's pk arm reopen any of MAJ-A's four minters). Wednesday rules the design, then J builds, then ONE full Opus gate. KS-1633 stays separate.
- `wed-secuura-storage-27-held-worktrees-1019` = **a**: **Seat D 21st launched (%9, 11:12)**, brief fleet/briefs_staged/2026-10-19_seatD21_storage_27_held.md. Rung 5/6 = its plan confirmation (not yet received at 11:1x). Switch it to Opus 5.5 at its first idle. On wrap: df, counts, score, close the pane by %ID.
- `wed-devmaster-drive-cleanup-1019` = **b**: (i) Wednesday's tree + the Ollama store go to a background Opus sub-agent (gatesets older than 14 d removed; Qwen3.8-Flash + Qwen3.5-122B oMLX and the unreferenced Ollama models MOVED to G-DRIVE `/Volumes/G-DRIVE/WED/models-archive/2026-10-19_*`, Ornith 1.5 kept); report `0_Brain/reference/2026-10-19_dev-drive-survey/CLEANUP_B.md`. Read it, re-check df, `ollama list`, and tell Kam the freed GB. (ii) **OWED, not started:** Testing Agent MAIN's 285 GiB of Secuura QA scratch (`!CODING/Testing Agent MAIN/projects/secuura/reports/*/{wt*,work*,clone*,scratch*,tmp*}`, survey row 1) is THAT project's files. Wednesday may not remove them. There is no cockpit lane: launch a Claude session in that project folder with a brief citing the card, using the same discipline as D (liveness, counts, df).

## 1b. RULED BY WEDNESDAY TODAY, STILL OPERATIVE (Secuura)
- KS-1628 L1/L6: **(iii)** = ticket now (KS-1634), #1589 proceeds, hardening as a follow-up. N1 measured that no in-repo caller moves, so (iii) stands; the ordering consequence is that KS-1634 goes first in the tier-1 batch.
- KS-1634 rated High, not Urgent (census 0/0; kintsugi is a dev box; the fix is in flight).
- KS-1622's widened scope = R's Claude build (counter spent).
- KS-1624 F1 = (a) (done, #1580). F2/F3 and KS-1623 N2 UNRULED, not queued. KS-1625 (Node floor) filed, no fix.

## 2. KAM'S CARDS OPEN
All four of this morning's Secuura/WED cards are RULED (section 1c). Datasec's `composer-l05-setup-card-too-1014` is Tuesday's.

## 3. OWED BY WEDNESDAY (own tools, small)
1. ~~wed_claim autostash~~ DONE 08:55.
2. **Spark harness:** the builder's `suggested_test_file` overrides a brief's named test path (SCREEN_9: both KS-1634 briefs' distinct paths replaced by one name, golden DIFFERS). A brief path should win, or brief_lint should refuse the mismatch. **Do not edit round.sh / build_input while a screen is running** (`pgrep -fl round.sh`).
3. cockpit.sh say --mail: stamp the mail's timestamp into the pointer; `say %4` (pane id) is a silent no-op: fail loudly.
4. pretooluse_no_cd.sh cannot resolve a variable path (`git -C $C ...` into the scratchpad refused): allow a variable that resolves inside WEDNESDAY or the session scratchpad.
5. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears.
6. Fable 5.1 coordinator-task trial (routing decision 7) still owed.
7. stash@{0} (10-18 autostash, restored) and older stashes are KEPT, never dropped.
8. From the 10-19 consolidation: cockpit `say` "queued" case; the "next-up" stall; `stamp.sh`; a DKIM helper (learnings/_audits/2026-10-19_consolidation_DRAFT.md §6). PROMOTION OWED: send_brief.sh --kind answer advisory for a RULED code shape with no `read <path>`/`unread` clause (arms first; learnings/_audits/2026-10-19_consolidation.md §2).
