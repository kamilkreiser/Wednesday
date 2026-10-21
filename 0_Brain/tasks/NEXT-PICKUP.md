---
date: 2026-10-21
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the Sonnet 5.5 Wednesday seat that booted at 15:5x AEDT 2026-10-21 (successor of the 15:01 seat). Replace wholesale again; never stack. Previous version: git history and NEXT-PICKUP.md.pre-1021-1900.
---

# NEXT PICKUP (Wed 21 Oct, written 2026-10-21 19:04 AEDT by the 15:5x seat; ctx about 62%, weekly 7d 87%)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. The by-tier digest is about 623 KB (7,414 lines): read it in ~420-line chunks (three parallel reads per turn fit); a seat lands near 40% after digest + ledger + pickup. The two daily notes are 250 KB each: TAIL only. Today's note is 0_Brain/daily/2026-10-21.md (about 20 entries, read whole).
2. Then `tools/kam_rulings_today.sh`, `reconcile_rulings.py` (report, then --apply), `tools/newmail.sh`, `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'`.
3. Literal paths only for `git -C` (a $VAR trips the no-cd hook). Verify merges by `git -C /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src fetch origin develop` then `log --first-parent`.
4. send_brief needs `WED_AGENT=wednesday`; subjects never carry hold/stop/checkpoint (I slipped on 'hold' today); send, tap (`cockpit.sh say "<cockpit NAME>" "<pointer>" --mail "<subject substring>"`) and note are THREE separate calls (receipt guard); zsh: no bare '=====' or '==' word, no PIPESTATUS.
5. A `wake_ack.sh` is a judgement of STATE: read the artefact the seat waits for (origin ref, PR, file) BEFORE acking an idle wake (ledger 10-21, my 78-minute miss with G 14th).
6. In force: Kam 10-18 new-account grant, routing v1.0 (fleet/specs/model-routing.md; every launch receipt names the row), October deploy grant until further notice (demo AND kintsugi, kintsugi first, KS-535), TESTED merge grant, merge-and-archive grant, 80-90% band (hard stop 90%).

## 1. STATE AT THIS WRITE
- **Floor:** wednesday %0 and fleet-monitor %1 ONLY. No Secuura seat, gate or drafter is live. G 14th wrapped (HANDOVER 6,614 B on disk, scored 0.92, %27 closed).
- **develop = 5932ff54818b38c255cec19a52cf93c388ff8d04** (my fetch). Merged today on my GO and verified by my own fetch: 31 Secuura merges in all; since 15:5x: #1674 KS-1706 280fdbcd1986 (the advisory-freeze lock refresh: 31 locks + 3 vite pins 7.3.6 -> 7.3.7, tier-1 gate CP1 Opus GO WITH NOTE), #1675 KS-1508 f7c9e1c79bb3 and #1676 KS-1660 5932ff54818b (test-only falsy cells, gate CQ1 Sonnet GO). **Nothing deployed.** Kintsugi runs 32964477fe88 (deployed 10-20); demo d75bfe2deb80 (NOT GO: Stuart's KS-695 uat-ps condition unmet).
- **Freeze CLEARED:** audit:gate and audit:locks rc 0 on develop (G's measurement; gate CP1 re-measured on the head). Pushes work again.
- **Gauge:** 7d 87%, renews about 3d 18h from 18:4x (about Sun 25 Oct). Hard stop 90; Kam's 18:55 (10-20) order 'move to you and the spark' is LIFTED ONLY for raise/gate/merge steps (Kam 15:12 and 15:20 today). **No build seat, no deploy seat, no drafters** until the allowance renews or Kam says. Ornith: no reporting (Kam 10-20 19:39).

## 2. HELD / OWED, IN ORDER
1. **KS-1707 (High, Backlog) BEFORE 2026-10-31:** six accepted audit-baseline rows lapse (react-router x2 KS-528, deepmerge-ts KS-664, sprintf-js + postcss-selector-parser KS-1425, braces KS-1403); all six are still reported by leg 6, so on that date they turn the gates RED and refuse every push. Fix the dependency or renew (a HIGH row's renewal is Kam's or Wednesday's; the 10-05 grant covers re-dating on his ruled date only). The 15 stale CLEANUP rows are in the same ticket. Told Kam on the panel 17:16. **File a card with default 'fix forward' about 10-26 if no seat has started it**; do not let it reach 10-30 unowned.
2. **Held Spark pass KS-1622** (READY_KS-1622-LATERWINDOW1622-1 in local-model/night/; brief ks_1622_p1; PASS byte-identical, red 3/6 at tip, suite 1169 -> 1175; departs from the ticket's literal wording on purpose, see the brief's Scope). Needs a raise seat (Sonnet, test + one line in api-gateway platform.ts); batch it with any other held test-only pass. A PASS is never a merge.
3. **C 33rd (KS-1695 gap 2, option b ruled twice)** waits for the allowance renewal or Kam: a build seat. Brief material: the 04:12Z ANSWER set (isPlatformRole on the owner-less arm only; recipients excluded; empty caller id never matches; creating-connector check names CONNECTOR_CREATE_ACTION) plus the SEPARATE comment-only hunk correcting the merged R18 comment (platform_admin is NOT gateway-only), 24 of 36 owner-less on kintsugi. One Opus tier-1 gate at most; two-round cap.
4. **KS-1692 PR 2 (G 14th lane's old item)** from 5_Project_History/2026-10-20_seatG-13th/HANDOVER.md (tier 1, four call sites, ruled shape (i)); **KS-1688 org-merge seat** (card a: 'S adds a transfer-issuer call before it versions'); both build seats: wait for the renewal.
5. **STUART (KS-1557, KS-772)** asked on kintsugi (comment 00:19:20Z): DB confirmation of action_provenance rows for doc doc-1792541501228-886d28af and certification bd764310-b5aa-474a-b345-8abed5bbc3b7, and why the originate anchor feda5b7a-... showed FAILED at 00:10:41Z. Both need BOX ACCESS = a deploy-capable Claude seat = barred until renewal or Kam's word. Answer by ticket comment then. KS-1557 is NOT Done (needs deployed + tested + works).
6. **Kintsugi deploy of the new develop** (lock refresh, vite 8.3.4 toolchain for three frontends, +5 merges): a deploy seat under the October grant, kintsugi first, after the renewal. The brief must name that the frontends crossed two vite minors and no image has been built (G's wrap item 2); demo only after Stuart's uat-ps condition.
7. STANDING_LINES (claim via wed_claim): (a) searchIssues returns hits for a nonsense control term: only an exact title/containsIgnoreCase filter can say no match; (b) a landing figure in a GO is expected unless the base moved; (c) send_brief 'sent:' is not delivery: verify at the destination; (d) a comments-only claim needs a known-unequal pair; (e) NEW: a seat that ends a turn on a waiter must wait with the background JOB whose exit re-invokes it, never a nohup child (G 14th, 1 hour idle).
8. Ledger rows added this seat (3): typed clock x2, G 14th idle 78 minutes. No lesson FILE edited: no digest regeneration. Do NOT commit the boot digests from a seat. The 05:30 ledger archive (rule 3c) is owed at the shift-change wrap.
9. G 14th's clone seatG14-5671d5115921 (0.61 GB, nothing unpushed) is LEFT in deploy-clones on purpose; its offer to remove it is open (Kam's drive-hygiene rule: ask later). Clones C left: seatC32-7e3b9362e08b, seatD26/E.
10. Model switches: seats run the launcher's pin (Opus 5); switch a raise seat to Sonnet with /model after boot (zoom and read the busy line first). Fable 5.1 trial still OWED.

## 3. KAM'S CARDS
OPEN: composer-l05-setup-card-too-1014 (Tuesday's). Secuura cards: none open. Ruled and delivered today: secuura-advisory-freeze-lock-refresh-1021 = a (16:24:24).
