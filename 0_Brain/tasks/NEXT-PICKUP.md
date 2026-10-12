---
date: 2026-10-12
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 22:57 Mon 12 Oct by the evening Wednesday seat (booted 20:15, Sonnet 5.5, ctx ~65% at this write). The previous 266 KB copy (a stack of ~25 dated blocks) is in git history and in that session's scratchpad (NEXT-PICKUP.pre-1012-2300.md); its still-live items are carried below. Replace wholesale again; never stack.
---

# NEXT PICKUP (Mon 12 Oct, written 22:57 AEDT)

## 0. How this seat worked (so the next one can continue the same way)
- Every seat mail gets: read whole -> (gate agent in the background if READY FOR GATE) -> `send_brief.sh --kind answer` -> separate `cockpit.sh say <lane> "<pointer>" --mail "<subject substring>"` -> separate `note_entry.sh`. Never chain the note to a send (receiptguard refuses; ninth instance today). Subjects must not contain stop/hold/checkpoint words.
- Gate agents are `Agent` calls (model sonnet or opus), run in the background, write `0_Brain/reference/<date>_gate-pr<N>/verdict.md`. A rotation KILLS them: re-commission from the seat's bundle if no verdict file exists. Opus for auth, security, front door, destructive/GDPR, hook, shared tooling; Sonnet-tier for test-only/spec-only/small product.
- Merge GO = head-bound, five conditions + moved-tip rule; the author seat merges. I have read verdict summaries but NOT fetched any squash myself: every 'merged' below is a seat's five-point source read.
- Rotation: a seat runs `cockpit.sh rotate <lane>` DETACHED (patched today: `cockpit.sh.pre-1012-2100-selfrotate`; confirmed when K 5th respawned as %67). After ANY rotation order read the pane list and `fleet/cockpit/logs/rotate.log` ~2 minutes later; a lane with no pane = `cockpit.sh launch <lane>`. Seats boot on the launcher's Opus 5; switch with `/model claude-sonnet-5-5` at an IDLE prompt (K, V, J, D-lane = Opus 5.5 `claude-opus-5-5`), read the statusline back. Run `pane_prompt_check.sh <pane>` before reading any prompt line (they were ghost text every time). Seat panes sometimes show no statusline in a tmux capture; the wake_watch band wakes are the context signal.

## 1. LIVE FLEET at the write (panes; lane -> seat)
- %67 K 6th (api-gateway lane, Sonnet 5.5): PR #1501 (ticket KS-1359) at a SONNET gate; building KS-1180 (a) comment-only PR next (GO given), then KS-1090 R2-2, KS-1185 F1, KS-1237 (golden diff at `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/split_1237msg/KS-1237.md`, re-verify it applies).
- %62 J 3rd (originate/wallet-services lane, Sonnet 5.5): #1497 (KS-695 ask 3 part (ii), the erasure) reworked at head 6454dc9c, OPUS full-delta gate running; #1500 (KS-1333 item 4, NULL block height) at a SONNET gate; building KS-753 (timestamping mock flag + verifyTimestamp ignoring the row's verified column, SAME PR, Opus gate). J cannot read its ctx: told to finish KS-753 to READY FOR GATE, write the handover, rotate detached; no L10 in that seat. Lots done: L07, L08, L09 (L09 report accepted; KS-1173 and KS-1404 closed on read-only live checks).
- %63 V 4th (auth lane, Sonnet 5.5): #1499 (KS-1487, preflight leg 16, changes the push gate for ALL seats; ratio now N/16) at an OPUS gate; KS-1489 built LOCALLY, not to be pushed until #1499 merges; #1498 (KS-1477) MERGED 06d33fb4. Then L05/L06 follow-ups.
- %66 D 18th (deploy lane, Opus 5.5): round 2 BUILD of 29 images running since 11:09Z box time (est 2.5-4 h; background shell; its idle wakes are silenced with `fleet/cockpit/wake_ack.sh %66`). Steps A, B, C done and clean; D running; NO swaps granted.
- %1 fleet-monitor; %0 me.

## 2. DEPLOY ROUND 2 (kintsugi) - the big thing
- PIN: develop `361537eed238e9886f4cc22d8a91607a96fb1508` (K's #1496 squash; contains #1495 KS-1470 front-door fix; does NOT contain #1497 (proved with controls). 29 images, 0 migrations, 25 behaviour commits, spec adds 2 erase-connector routes live at the api-gateway swap. Tags `pre-20261012b`. KS-1380 is NOT a stopper. KS-968 is NOT in the both-rows state on kintsugi.
- STEP E (swaps, one at a time, KS-535 check inside the anchoring/nft-certificate recreates, api-gateway LAST) is NOT GRANTED. It needs (1) Kam's tap on card `secuura-round2-deploy-vs-ks695-hold` (rec a: carry KS-695 part (i) only, 501/refusal routes; his two KS-695 rulings say deployment waits for Stuart's answers, neither answered) and (2) my mail 'GO step E' naming the ruling. Default if no tap: builds complete, no swap.
- After E: F verify (/health/deep BODY), G content checks (KS-1305 dist/db.js contains 'npm run generate'; KS-695 (i) routes resolve; wallet.local refused 400 on POST /register, /users/stub, /users/admin/create and the social callback), V/J/K re-probe their own tickets. Demo = a separate plan after kintsugi is verified. Prune not granted. Error-class baseline is in D's stepA; K's probe POSTs 11:10:25-27Z attributed.
- Round 3 (not in this build): #1498 (merged), #1497 when fixed+gated (but KS-695 deployment still waits for Stuart), #1500, #1501, #1499, KS-753, and whatever else merges.
- Fact for the receipt: kintsugi runs NODE_ENV=development (so the production 307 cannot be checked there).

## 3. OPEN CARDS (Kam) - check `decision_queue.sh list open` against what he sees
- `secuura-round2-deploy-vs-ks695-hold` (above). `secuura-done-rule-unit-pinned-deployed-no-live-check` (rec a: close tickets that are unit-pinned on develop AND in the running Kintsugi build when no live check is possible; default stay open and listed; the class is KS-1072, 1073, 1183, 1231, 1187, 1256, 1257, 1341, 1345, 1346, 1171 and likely dozens more: when he rules, tell K/J to close in one pass). Datasec's `quickquote-v234-gh-login-for-pr-1012` is Tuesday's.
- Ruled and DELIVERED today: snapshot retention b (two older snapshots deleted by D 18th, readback x3; the deletion rested on his card tap, not a signed mail: told him, offered a signed-mail rule), VM disks 256 GiB both, KS-695 questions posted, issuer account (one login, refused 401, stopped).
- To tell Kam in the receipt (not carded): m3 lineage ruling in #1497 (conservative guard added); issuerName not blanked, listed as his question; the project SessionStart hook still says POST /api/seen (advances HIS unread boundary; seats refuse; his to fix); coagent@ answers 404 (stale boot step); kintsugi NODE_ENV=development; KS-1470 live check needs a valid connector key (his) after the deploy; the outside-clients question on KS-1470 not asked of Stuart (decision recorded in today's note 21:49).

## 4. GATE LEDGER (today, by me; verdict paths under 0_Brain/reference/2026-10-12_gate-*/)
Opus: 1495 GO WITH NOTE (merged 8d34fbf0), 1497 NO GO then r2 RUNNING (6454dc9c), 1498 GO WITH NOTE then Sonnet delta GO (merged 06d33fb4), 1499 RUNNING. Sonnet: 1490 GO WITH NOTE (merged 3fd441aa), 1476 r4 GO WITH NOTE (merged efc84906), 1491 GO WITH NOTE (merged 092da3ae), 1496 GO WITH NOTE (merged 361537ee), 1500 RUNNING, 1501 RUNNING. If a verdict lands after a rotation, read it, ANSWER the lane (GO head-bound with conditions: verdict hash, honest preflight wording 12/15 -> now N/16 after #1499, one follow-up ticket, Done only after deploy + live check).

## 5. ALLOCATION (0_Brain/reference/2026-10-12_ks-allocation/LOTS.md; its #877 under KS-1173 is wrong: #877 is KS-733, Platform S's PR)
Done: L02 K, L01 K, L04 K, L09 J (reports accepted), L05/L06 V and L07/L08 J first pass. UNASSIGNED: L03, L10 (vc-issuer), L11-L17. Never leave a seat idle: when a lane's queue empties, allocate the next lot (read-only verify-and-close, one table back, nothing closed that needs a deploy).

## 6. OWED (mine)
1. The 06:00 morning receipt to Kam: paginated board count (3 pages x 250, Blockchain key via a script file, KS prefix only); last paginated count 17:4x: 599 issues, 505 open, 94 Done; target 509 -> most by Sat 31 Oct. Write the tally FIRST, count with wc -l, then post (I posted 'seven' for eight merges today).
2. After #1499 merges: tell J, K, V, D the preflight ratio reads N/16 (their 12-of-15 wording becomes 13-of-16).
3. Score J 3rd, V 4th, D 18th at their wraps; INDEX.md Secuura section not refreshed today (scoreboard rows are written: F 17th 0.93, D 17th 0.96, K 4th 0.95, J 2nd 0.95, K 5th 0.96, V 3rd 0.95).
4. Fix my allocation sheet (#877). Ledger rows today: panel count (seven vs eight), versionedById/ownership claim for V, rotate self-kill (lesson filed), receipt-chain (ninth).
5. Linear 'lesson' label ingest and the coagent@ check were NOT done this session; Datasec mail read by subject only (Tuesday's).
6. Standing rules in force (all from today's Kam rulings): Done = tested + works + deployed (15:26); never idle (15:25); clear the fleet activity flag once answered (`fleet_ack.sh answered`, FLAGGED must read 0); be more careful with coding files and deploys (16:04: read the precondition before any instruction/brief/card); Ornith STOPPED (`0_Brain/tasks/ORNITH-PAUSED`); models named at every launch (Opus 5.5 for deploy lanes, Sonnet 5.5 for build/raise/verify, gates per tier).

## 7. CARRIED from the superseded 266 KB pickup (not touched this evening; verify before acting)
- Stuart's K+S list (Kam 12:07, saved verbatim at 0_Brain/reference/2026-10-12_stuart-ks-integration-list/): KS-1195 (per-key ceiling), KS-1402 (the 403 is gone; waits on Stuart's PS-992 re-measure and the holder-stub RULING, a DESIGN ruling for Kam), KS-1385 + KS-1384 (anchor identity), KS-1454 (signatureHash on the sign verb, K first), KS-695 ask 3 (in flight above), KS-723, KS-1387 housekeeping. I have not read tickets 1195, 1385/1384, 1454, 723, 1387 myself. Nothing to Stuart or Peter without Kam.
- Cards/limits: KS-664 audit exception expires 2026-10-31 (blocks every push after); KS-593 live Schemathesis needs Kam/credentials; KS-1458 passwordless no-secret stuck state; ~68 Secuura rulings carry no delivery mark and need routing (`decision_queue.sh list ruled --undelivered secuura`).
- GitHub Actions has been DOWN since 08:42Z (19:42 AEDT): every PR job fails in 3 s with no runner (billing/quota signature); told Kam on the panel; no cloud CI evidence exists; local gates carry it. Ask Kam to check Actions billing if not done.
- WED items from the old file (line ~478): TRMNL view (Kam 12:5x, claimed) and the T9 -> KK_DEV_Local copy. Read the old copy (git history, `git log -p -- 0_Brain/tasks/NEXT-PICKUP.md`) for the wording.
- EXPIRING-GRANTS.md is live: the October deploy-both-boxes grant ends Sat 31 Oct; 'ignore the 90% stop' for Wednesday ends at an account/allowance event (gauge 33% now, so moot); read the file at every boot, a row past its date is DEAD.
- WEEK-INSTRUCTION.md is LAPSED (lapsed 10-12 00:07): do not act on it; Kam is at his desk today.
