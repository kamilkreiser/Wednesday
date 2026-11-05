---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 21:0x AEDT 2026-11-05 by the 20:00 seat (ctx 45%). Previous kept as NEXT-PICKUP.md.pre-1105-2100 (and .pre-1105-1638, .pre-1105-1312). Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026 (the 20:00 seat)

## KAM TODAY (kam_rulings_today.sh read 20:00:55; newest 16:53:29 — nothing after)
- 15:42:14 verbatim: "good work on the above. what about secuura tickets.  I would like you to get through all the in progress and all in review tickets" -> the floor below.
- Standing: DEMO FROZEN (07:08 card ks1401-058 = a; no demo redeploy without his word); Spark IGNORED (11-04 16:42); October deploy grant extended until further notice (10-19); weekly gauge 95% at 21:00 = a GUIDE (10-22), Sonnet tilt, card him if it reaches the high 90s.

## DEVELOP + MERGES (ls-remote 21:00:34)
develop = 1e4bdcb899c44023404bcd33c511de6f7dde2f6e (PR 2015 squash). Eight merges today by B 96th, all on head-pinned GOs after gates: PR 2007 KS-1262, 2010 KS-1504 (Done), 2011 KS-1185, 2012 KS-1645, 2008 KS-1150, 2013 KS-1460, 2014 KS-1968 B2, 2015 KS-1804. All tickets stay In Progress until deployed (demo frozen = Done waits).

## FLOOR (cockpit.sh status 21:0x)
| seat | pane | model | state | next for Wednesday |
|---|---|---|---|---|
| D 55th | %181 | Opus | kintsugi deploy (auth + api-gateway), ITEM 0 DONE read-only: delta 7 squashes 0 .sql, KS-1262 census = ZERO notification keys (api-gateway proceeds), plan CONFIRMED 21:0x (yaml window: rsync as usual, recreate binds new inode) | its STATUS A -> read whole -> send `GO KINTSUGI at 1e4bdcb899c4 (Seat D 55th)` (FINAL PIN = PR 2015 squash; it must report the pin-to-head delta: +1 squash, auth passwordLoginGate.ts reorder). Then STATUS B: approve its 6 drafted ticket comments (KS-1150, 1460, 1968, 1645, 1185, 1262) by ANSWER naming the seat. |
| B 96th | %176 | Sonnet | merge seat, queue EMPTY, holding with watcher (told: no self-wrap) | next ADDENDUMs as PRs arrive: PR 2009 r2 (KS-1938, gated 199r2), KS-1666 PR (gate 203 GO WITH NOTES), KS-1462/KS-1989 (need gates), KS-1534 (needs gate), T-lane four (need gates). NEVER a mail between a GO and its MERGED. |
| K 16th | %180 | Opus | KS-1534 committed ae8e8c78f91f, driver 79923 queued 12th with OVL_IGNORE_HEADS = exactly T 12th's KS-1539 + KS-1614 branch names (ruled 20:4x) | its READY FOR GATE -> tier 1 Opus gate (security surface) |
| F 34th | %174 | Opus | KS-692 push driver 56138 queued (acked idle) | its READY FOR GATE -> tier 1 gate |
| J 16th | %171 | Opus | KS-1150/1460/1968 B2/1804 all merged; remaining queue per its brief (KS-1407 e2e etc.) | next READY -> gate |

Detached push drivers of WRAPPED seats (alive at 20:55, tty ??): V 21st 5891 (PR 2009 r2 at EXACTLY 2f10e7e060cc) and 11176 (KS-1666 at EXACTLY 4d1c96b495bd); V 22nd 8312 (KS-1462 605942b23ce2) and 52840 (KS-1989 c0b427a2ff76); T 12th 73804 (KS-1539 a56b949c56f0), 71556 (KS-1542 52a781a3e493), 31179 (KS-1614 8d4f6fca8388), 27026 (KS-1493 8e0070f193ba). Push queue ~12 deep at ~20 min each.

## UPDATE 22:0x (65% checkpoint) — newest; supersedes rows above where they differ
- develop = 1b1b65c7415f (PR 2016 KS-1407 merged 10:25:38Z; NINE merges today). KINTSUGI DEPLOYED at 1e4bdcb899c4 by D 55th (auth 21:38, gateway 21:39-21:40 AEDT; verified; 7 comments posted; D 55th WRAPPED 0.97, pane closed). Demo frozen (lacks PR 2006 + 2007, 2010, 2011, 2012, 2008, 2013, 2014, 2015).
- GAUGE 97% (22:03). Kam 21:17:22 plan = new account tomorrow morning; prior 98% card ruled a. NO new seat launches tonight; in-flight continue; panel told (bf-fd24f6e968d0).
- FLOOR: B 96th %176 (queue item 10 = PR 2009 r2 KS-1938, gate 199r2 GO WITH NOTES: expect NOTES PATCHED -> READY -> send its head-pinned GO); V 23rd %184 (PR 2009 appended; KS-1666 / KS-1462 / KS-1989 pushes pending via drivers 11176 / 8312 / 52840; building KS-1509); J 17th %182 (KS-1858 driver 45397 + KS-1797 driver 67814 queued ~10th/11th; ITEM 3 KS-1494 comments-only PR ruled 21:57); K 16th %180 (KS-1534 driver 79923 queued 12th, OVL_IGNORE_HEADS ruled); F 34th %174 (KS-692 driver 56138 at the head of the queue); S 23rd %183 (filings: 11 of 21 filed at 10:56Z; refresh race = one ticket, ruled).
- NEXT ARRIVALS: each READY FOR GATE -> gate (tier by touch: KS-1858/1797/692/1534 tier 1 Opus; KS-1462/1989/1509/1494 tier 2 Sonnet); KS-1666 READY FOR MERGE (gate 203 done) -> queue to B with its N-status lines (N1 follow-up test owed after merge; N2/N3 in body).
- T 13th NOT launched (gauge): T 12th's four pushes (73804, 71556, 31179, 27026) will land unraised; the next account's seat raises them per T 12th's HANDOVER.
- Routed later: KS-1968 detail (HIBP_ENABLED FALSE/0/off leave the check ON) as a comment after the deploy round (S 23rd's wrap names it).

## UPDATE 21:2x (50% checkpoint) — supersedes the rows it names
- KAM 21:17:22 verbatim: "keep going with the secuura tickets and I will log into a new account tomorrow morning" (receipt bf-03a5af49eb26; EXPIRING-GRANTS row, ends at his login).
- D 55th: GO KINTSUGI at 1e4bdcb899c4 SENT 21:18 (re-pin in writing; auth + api-gateway; demo frozen). NEXT: its STATUS B -> approve its seven drafted comments (KS-1150, 1460, 1968, 1645, 1185, 1262, 1804) by ANSWER naming the seat.
- J 16th WRAPPED (0.96, pane %171 closed). PR 2016 (KS-1407) gate 207 tier 2 = GO WITH NOTES; queued to B 96th as item 9 (NOTES PATCHED 10:18Z; READY next -> its own GO; test-only, no deploy).
- IN FLIGHT: a Sonnet drafter writing briefs_staged/2026-11-05_seatJ17_laneA_auth.md (KS-1858 then KS-1797, Opus) and 2026-11-05_seatS22f_filings.md (the OWED item 4 list). Read both WHOLE, stamp, dry-run, launch when capacity is ROOM (>= 3 min apart).
- Floor now: K 16th %180, B 96th %176, F 34th %174, D 55th %181.

## OWED (in order)
1. GO KINTSUGI to D 55th on its STATUS A (pin 1e4bdcb899c4), then its STATUS B comments.
2. LAUNCH V 23rd (Sonnet, originate) when the first V push nears the head of the queue: per V 22nd's HANDOVER (5_Project_History/2026-11-05_seatV-22nd/HANDOVER.md): PR 2009 r2 READY FOR MERGE (merge seat adds gate 199r2 notes), KS-1666 PR + READY FOR MERGE (gate 203 GO WITH NOTES; N2/N3 into the PR body; no re-push), KS-1462 + KS-1989 PRs + READY FOR GATE (tier 2), then KS-1509 (documents.ts 964/1019/1054/1780, null stays null), then the KS-1666 N1 follow-up test PR after KS-1666 merges. Template: briefs_staged/2026-11-05_seatV22_laneD_originate.md.
3. LAUNCH T 13th (Sonnet, lane B) when the first T push nears the head: raise KS-1539/1542/1614/1493 PRs per T 12th's HANDOVER (5_Project_History/2026-11-05_seatT-12th/HANDOVER.md; READYs carry the accepted points), then KS-1505 part 2 after KS-1493 merges, close KS-2009 by comment after KS-1493.
4. FILING SEAT (Sonnet) — accumulated list: G197-F2, G201-N2, G202-N1/N2/N3/N6, G204-F1/F2/F3, G203-N4 (certifications.ts:935 catch-all TypeError), G205-N1 (HIBP_ENABLED only exact 'false') + N2 (zero-count padding rows), G206 Info 2 (stale passwordLoginGate line citations), fail500 'forty-six' comment vs 50, three unused eslint-disable in ks1868 files, docs-fragments cheat ADVISORY line 6235, approve-forward 'end' log, verify-fail-closed.sh empty users, dbGetApiKey swallowed lookup, audit-export candidate admin.ts:1657, KS-1150 F2 (jti without exp). Board search by symbol before each.
5. E successor (KS-864, KS-1128, KS-1841 F2) and G 28th (raise G 27th's three committed PRs when drivers 72708/8947 land): when capacity + gauge allow.
6. Mechanism owed (ledger w=3): send_brief.sh refuses mail to a seat holding an un-MERGED GO from Wednesday unless --after-go-ok. Until built: queue items for a merge seat with an outstanding GO go INSIDE the next GO (done this way for PR 2015).
7. Carried: KS-961 gate-owed (PR 887); Secuura project launcher stale lines (POST /api/seen, coagent@, cc Kam) -> brief a Secuura seat; stale shared-checkout node_modules (zod 3.25.76 vs lock 4.6.7) -> route to a seat; NAS evaluation FRIDAY 2026-11-06 (card, default HOLD); INDEX.md refresh (last 10-27); stash@{0} never drop.

## RULES THIS SEAT RE-LEARNED
- A state word about another PR in a mail a seat may copy into a PR body is read from the board/ls-remote first (B 96th caught 'B1 still open'; PR 1988 merged 11-03).
- Wave spacing: ROOM is one gate; >= 3 min since the last launch's 'verified at destination' stamp is the other.
- send_brief provenance lines need '| read YYYY-MM-DD' exactly; never a typed clock in them; a 'RULED BY KAM, NOT YET IN AN ARTEFACT' section is required (may be one line).
