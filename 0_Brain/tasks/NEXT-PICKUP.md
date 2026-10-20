---
date: 2026-10-20
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE by the Sonnet 5.5 Wednesday seat that booted at 15:01 AEDT 2026-10-20 (successor to the 12:5x seat). Replace wholesale again; never stack. Previous version: git history (and NEXT-PICKUP.md.pre-1020-1338).
---

# NEXT PICKUP (Tue 20 Oct, refreshed ~15:45 AEDT by the 15:01 seat)

## 0. FIRST ACTIONS FOR THE NEXT WEDNESDAY SEAT
1. Boot reads as the launcher says. The by-tier digest is ~623 KB (7,414 lines, ~25% of the window): the tool caps a read at ~25K tokens per turn, so read it in ~560-line chunks; a seat that boots at 16% after 3,100 lines will land near 40% for the whole digest + ledger + pickup. The two daily notes are 250 KB each: read the TAIL only.
2. Then: `tools/kam_rulings_today.sh`, `reconcile_rulings.py` (report, then --apply for this seat's cards), `tools/newmail.sh` (read the index, then the batch file whole; never cut a body), `tools/fleet_ack.sh list`, `tools/decision_queue.sh list open`, `fleet/usage_gate.sh --check`, `local-model/spark/tunnel.sh check`, `tmux list-panes -t fleet:0 -F '#{pane_id} #{@cockpit_name}'`.
3. Verify every merge with a literal-path fetch into `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (a `$C` variable trips the no-cd hook). Comment-only delta check: `python3 -I` script in the session scratchpad (non-comment multiset, both blobs, differenced both ways, with a control on a real code change).
4. send_brief needs `WED_AGENT=wednesday`; subjects never carry hold/stop/checkpoint; send, tap (`cockpit.sh say "<cockpit NAME>" "<pointer>" --mail "<subject substring>"`) and note are THREE separate calls (receipt guard). zsh: no `PIPESTATUS`, no bare `=====` word.
5. In force: Kam 10-18 new-account grant, routing v1.0 (fleet/specs/model-routing.md), October deploy grant until further notice (demo AND kintsugi, kintsugi first, KS-535), TESTED merge grant, merge-and-archive grant, 80-90% band (cloud launches only if it matters and nothing local can do it; hard stop 90%).

## 1. LIVE FLOOR (15:45 AEDT) - develop = 32964477fe8828eb78240150e8ab59bd8179f339 (#1654); Secuura merges today 28; gauge 83%
No Secuura seat is live (C 32nd, D 26th, E 21st, G 13th all scored and their panes closed). Panes: wednesday (%0), fleet-monitor (%1). No gate running. Spark drainer: ks_1508_falsy_p1 and ks_1660_falsy_p1 BOTH PASSED (byte-identical to golden) and are HELD: READY_KS-1508-FALSY1508-1... and READY_KS-1660-FALSY1660-1... in local-model/night/ (test-only; each needs a raise seat, batch them with other held passes; a PASS is never a merge).
Merged and verified by fetch today in order: ... #1666 21e0c39149ca, #1667 88933d5c7ebb, #1670 561a6c5b5282, #1671 f418cddac514, #1672 e84971b3504c, #1654 32964477fe88. Kintsugi 89956fe92956 (many merges behind), demo d75bfe2deb80.

## 2. KAM'S CARDS
OPEN: `secuura-platform-admin-spelling-certification-reads-1020` (mine; rec/default a: keep platform_admin refused on certification reads, settle in KS-1536/KS-1701; C 32nd found originate adminConfig.ts:60 names it). `composer-l05-setup-card-too-1014` is Tuesday's.
RULED, delivered: ks758 c (#1666), ks1689 d (#1672), ks1557 a (#1654).
RULED, delivery owed: `secuura-ks1695-ownerless-records-who-reads-1020` = b (gap 2, NOT built; C 33rd builds it); `secuura-ks1688-org-merge-edge-which-side-1020` = a (the KS-1688 seat posts 'S adds a transfer-issuer call before it versions'; it waited on #1654, now unblocked); `secuura-m365-admin-setup-for-customer-org-1020` = b (KS-1678 future work). Mark each `decision_queue.sh --delivered ID ARTEFACT` when it sits in a PR/ticket comment.

## 3. OWED BY WEDNESDAY (in order)
1. OWNER-LESS COUNTS (blocks the gap-2 GO, not its build): one read-only SELECT per box (demo, kintsugi), owner-less documents split by whether an action_provenance creation row exists, documents total as the control. No live seat has box rights; a DEPLOY-capable seat (D 27th) takes it. Same seat also takes the 055 kintsugi/demo count query (DEPLOY-BLOCKERS 2026-10-20 paragraph; gate CN1 N1) BEFORE 055 runs anywhere.
2. KINTSUGI DEPLOY of develop under the October grant (D 27th; Phase 0 re-tag, build everything before swapping anything, migrations in the middle, KS-535 wallet re-verified AFTER; report every step). Demo only after kintsugi is verified. Brief via a Sonnet drafter from the D 25th brief + DEPLOY-BLOCKERS; read it whole; brief_and_launch needs the provenance form, a ticket-state line per hyphenated ticket in the QUEUE, a `RULED BY KAM, NOT YET IN AN ARTEFACT` heading with a real check, and the SELF-CHECK line copied from the gate's own print.
3. C 33rd: KS-1695 gap 2 build, option b (read the 04:12Z ANSWER set: isPlatformRole on the owner-less arm only; recipients excluded as Wednesday's reading; empty caller id never matches; the creating-connector check names the exported CONNECTOR_CREATE_ACTION; plus a SEPARATE comment-only hunk in certifications.ts correcting the merged R18 comment (platform_admin is NOT gateway-only), listed in the READY with the multiset proof). History entry line 66 of the project's history.md is C 32nd's successor prompt. One Opus tier-1 gate at most; two-round cap.
4. G 14th: KS-1692 PR 2 from 2026-10-20_seatG-13th/HANDOVER.md (tier 1, four call sites; ruled shape (i)); deferred for the gauge.
5. KS-1688 fix seat (small): post the card-a comment/ticket step; may ride with C 33rd or a Sonnet seat.
6. Raise the two held Spark passes (KS-1508, KS-1660 falsy cells) with any other held test-only passes: one raise seat, file-disjoint, batched.
7. STANDING_LINES (claim via wed_claim): (a) searchIssues returns hits for a nonsense control term: only an exact title/containsIgnoreCase filter can say 'no match'; (b) a landing figure in a GO is expected unless the base moved; (c) send_brief 'sent:' is not delivery: verify at the destination (the tap's --mail check); (d) a comments-only claim needs a known-unequal pair through the same instrument.
8. Ledger rows added this seat: relayed negative census adopted as my own premise (platform_admin). No lesson FILE edited: no digest regeneration; do NOT commit the boot digests from a seat (rebase conflicts: take origin's).
9. Model switches skipped (seats run Opus 5 as launched). Fable 5.1 trial still OWED. The 05:30 ledger archive.
10. Clones C left in place on purpose: deploy-clones/seatC32-7e3b9362e08b (kept for the gap-2 lane; C offered to remove it, unanswered) and deploy-clones/seatD26-f01ba49da56d, seatE-f01ba49da56d (+ scratch PG 15 on 55621 may still run).
