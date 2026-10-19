---
date: 2026-10-19
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the 13:1x Wednesday seat at its 65% checkpoint, 2026-10-19 ~15:5x. Replace wholesale again; never stack. Previous: NEXT-PICKUP.md.pre-1019-1550 + git.
---

# NEXT PICKUP (Mon 19 Oct, late afternoon)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. Then kam_rulings_today.sh (the WHOLE day), reconcile_rulings.py, `bash 2_Project_Files/tools/newmail.sh` (to a file), fleet_ack.sh list, decision_queue.sh list open, fleet/usage_gate.sh --check, `local-model/spark/tunnel.sh check`.
2. **In force:** Kam 10-18 "new account: tickets, backlog, routing definition, Spark as many as it can handle". Routing v1.0. Gauge 31% at 15:49. Kam last posted 11:08; every card of his ruled (only Tuesday's Composer card open).
3. Commit your own files by pathspec before any tool that pulls. fleet_ack sometimes cannot see a fresh QUESTION for a few minutes: re-run `answered` at the next wake rather than chasing it.

## 1. LIVE WORK (15:5x)
- **develop = ce98606212e4e0dce8212d4541ffff2484f2217b** (#1606 KS-1638 merged; landed tree eaf0f260dbda = gate S1's). 44 Secuura merges since 19:00 Sun. Nothing deployed.
- **Seat J 13th (%6, Opus 5.5, ctx ~72%):** holds the GO for **#1607 (KS-1385 (b)) at 243d324d4dd7**, landed tree must be **5adb4e513696** (gate U1 GO, verdict `0_Brain/reference/2026-10-19_gate-U1-pr1607-r2-delta/verdict.md`, re-hashed EQUAL). On its MERGED mail: ls-remote, fetch into your own scratch clone (`git clone --shared` + fetch in the session scratchpad), compare the tree. Then J files one Low follow-up (U1's INF-1/INF-2), posts the KS-1385 BLUF, and wraps (band). Score + `pane_close.sh` in the same action as its wrap.
- **Seat R 52nd (%12, launcher-pinned "Opus 5"; switch to Opus 5.5 at its first REAL idle: raw `/model claude-opus-5-5` + Enter on the dialog, then a model-note mail):** raised #1608 (KS-1506) and #1609 (KS-1539); building KS-623, KS-1637, KS-1503 on develop, then ONE batched READY for all five (tier 1 x3, tier 2 x2) → gate it (Opus, batched; KS-623's NODE_ENV precondition is CLOSED: development + ENABLE_TEST_TOKENS=false on both boxes, R's read). **#1597: ruled (1)** at 15:2x: push 8f3310c6ed85 from a worktree at develop (the hook runs from the pushing worktree), tree asserted b64be7e50092, deviation recorded in the PR body + KS-1634; then R mails MERGE-READY → re-pin the GO onto live develop (new landing tree + shell suites, since develop moved). Then S1's Low follow-up ticket, then KS-1622.
- **Spark:** 23 PASSes held today; SCREEN_12's five are with R. Next screen once R's batch merges. The KS-1634 v2 brief (`night/briefs/ks_1634_v2_p1/`) runs after #1597 merges.
- **Drive:** DevMASTER 52% (955 GB free). Card `wed-devmaster-drive-cleanup-1019` DELIVERED. Still Kam's hands: two rm commands for the oMLX Qwen folders (on the panel since 12:3x). Gatesets: 161 eligible but git-TRACKED; needs a git rm plan with Kam.

## 1a. STUART'S LIST (Kam 15:50, live board: "action what you can; anything you need from me, a card in fleet activity") — UPDATE 16:1x
- **Triage DONE:** `0_Brain/reference/2026-10-19_stuart-list-triage/TRIAGE.md` (26 dispositions: 14 A agent-actionable, 5 B cards, 5 C done, 2 D blocked). Read its BLUF + "(A) items by lane" section first.
- **Two of Kam's 9 Oct rulings were NEVER DELIVERED (Wednesday checked both cards: ruled a, no delivery mark):** `secuura-ks1195-s-key-ceiling-1009` = a (3,000/h for S connector keys, env-tunable, new keys only; unbuilt: platform.ts has 0 rateLimit) and `secuura-ks1384-anchor-per-event-1009` = a (one anchor per lifecycle event). A seat posts each verbatim as a KS comment, then `decision_queue.sh --delivered`.
- **The five B cards** are being posted by a background helper after reading every prior-ruling match: result in `.../CARDS_POSTED.md`. If this seat rotated first, read that file; if absent, re-run the helper from the card JSONs in the 13:1x session scratchpad (`cards/`), or redraft from TRIAGE.md's "Draft cards (B)".
- **A lanes to LAUNCH (not yet launched, file-partitioned per TRIAGE.md):** (1) NEW seat, originate custody: the KS-1402 develop 500 (blocks every deploy; add it as a DEPLOY-BLOCKERS row). (2) KS-1195 build (gateway routes/platform.ts register-connector rateLimit, Kam's ruled a), new seat or R after KS-1622 (same file, different hunk). (3) anchoring lane (J's files are free: J wrapping): KS-1603 interim ownership check → KS-1629 → KS-723 → KS-1454. (4) certifications lane: KS-1557 harness step, then its write side, then KS-1633. (5) a board-reply seat (ticket comments only): the two undelivered rulings, KS-1385/1612 status (no date), KS-1402 status, KS-1604 shape, KS-1629/1633 word, KS-1575/1596 holding, KS-1387 close on evidence; plus read-only box reads (KS-1584 key row, KS-1634 census with Stuart's predicate, SIMULATE_ANCHORING on demo).
- **Kam's alone:** any reply to Stuart outside a ticket, re-minting/rotating S keys, any landing date. DEPLOY-BLOCKERS.md:39 is stale (#1568 merged): fix it.

## 1b. RULED BY WEDNESDAY TODAY, STILL OPERATIVE (Secuura)
- #1597: (1) as above; `--no-verify` refused. #1603 shipped as is (the token-endpoint body echo is KS-1617's own question).
- KS-1385 (b): partial apply, 202, absent stays absent, issuer latest-wins, `allow` byte-identical, option (c) not built.
- KS-1377 residue as gate Q1 measured. No Docker on the Studio for any seat.
- KS-805 Closes; KS-1471 Closes; KS-1544 Refs; KS-1525 Refs; KS-1622 widened scope = R's Claude build.

## 2. KAM'S CARDS
To deliver: `secuura-datasec-author-on-two-branch-commits-1019` (after the #1597 force-push: the card's "two commits" = #1597's one + #1589's, which merged as a kksecura squash). Delivered today: ks1612 round 3, storage 27, drive cleanup.

## 3. OWED BY WEDNESDAY (own tools, small)
1. cockpit.sh say --mail: stamp the mail's timestamp into the pointer; `say %4` (pane id) is a silent no-op: fail loudly.
2. pretooluse_no_cd.sh: allow a variable path that resolves inside WEDNESDAY or the session scratchpad.
3. Deploy round (Kintsugi): READ-ONLY census seat first, once tasks/DEPLOY-BLOCKERS.md clears.
4. Fable 5.1 coordinator-task trial (routing decision 7).
5. The 95 `t <t@e.com>`-authored commits on develop: check whether they are tracked.
6. Keep stash@{0} and older stashes; never drop them.
7. Gate brief template: name every touched service's suites as RUN or NOT-tested-by-name (P1 missed one today).
8. Typed clocks: three today (13:2x, 14:2x rows). Write times from `$(date +%H:%M)` or leave them out.
