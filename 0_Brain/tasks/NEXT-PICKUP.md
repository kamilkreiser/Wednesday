---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 09:4x by seat 02680bc2 (rotation at ~78%). Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (rotation handover 09:4x AEDT 2026-10-06, seat 02680bc2)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. **Kam is ON the live board this morning.** His 09:37:54 rule: **past 70% weekly → the Spark takes 80% of tasks** (`learnings/2026-10-06_past-70pct-spark-takes-80pct-of-tasks.md`; EXPIRING-GRANTS row). Count the Spark-vs-Claude share at every checkpoint and in the receipt. **Open question to Kam (panel 09:3x): a typed, unsent "4" was at Wednesday's prompt.** Default stated: cleared by this rotation's respawn; nothing acts on it.
1. Read `inbox_digest.sh --inbound` WHOLE.
2. **develop = 22b268143a63** (#1389, KS-1330, merged by G 2nd 14:02Z, VERIFIED AT SOURCE: tree c25213614a52). Peter merged #1390/#1391 overnight; the doc `<h2>` tags are split, so use newline-tolerant readers only.
3. **E 6th (`Secuura/Blockchain-E` %50)**: building KS-1256 ((ii) = an explicit `!isRedisAvailable()` → 503 BEFORE the read; its drive proved production FAILS OPEN on a sustained Redis outage). It also holds **`GO (Seat E 6th): merge 1385 on gate66`** (sent 09:4x; tree 2203187daaa2 on 22b2; the body drops the false #1382 banner; GIT_SSH_COMMAND unset). Expect STATUS merged 1385 → verify the squash AT SOURCE (scratch fetch: tree, 1 parent, 0 trailers) → then its KS-1256 READY → gate (T1).
4. **B 65th (`Secuura/Blockchain` %51)**: #1393 round 2 building (plan confirmed 22:1xZ; Q-PK branch-in-TS + a UUID-shape guard; census 13/1/12). Expect READY → **round-2 gate kit** (names B 65th as author; round 2 of 2 under the cap; the KS-1419 comment draft is posted ONLY on Wednesday's relay after that gate reads it).
5. **#1394 (KS-723, PR C, head a94ec8f6a2c6)**: gate67 **NO GO, TEXT ONLY** (`fleet/qa-agent/gatesets/2026-10-06_gate67/GATE67_VERDICT_mail.txt`): the PR body's "NARROWING, not closing" before KS-723 would make Linear CLOSE KS-723 on merge. Fix = reword the body heading (e.g. "NARROWING — KS-723 stays open") + the false ":406" sentence, then a T2 text re-check, then **Seat B 66th** merges (GO string `GO (Seat B 66th): merge 1394 on gate67`; key-anchored merge-in e23888941fda on 22b2, void if develop moved). Launch B 66th only when B 65th has wrapped (same pane); it is a Claude seat by necessity (edit, merge), so name the clause.
6. **#1383 (KS-1401)**: NO live seat. F 4th wrapped cold (handover `HANDOVER-seatF4-2026-10-05.md`, sha256 9cc7c292a63ff75e; M 74f6f663af02 on the SUPERSEDED develop, never pushed). **ROOT CAUSE of rc 141 = an exported GIT_SSH_COMMAND overriding `-c core.sshCommand`** (STANDING_LINES). A successor F 5th rebuilds the merge-in on the live develop with a fresh independent prediction (the docs are unchanged by #1389, so b1449c08/ceff974c-style key-anchored, re-derived), pushes with GIT_SSH_COMMAND unset, and merges on a fresh signed `GO (Seat F 5th): merge 1383 on gate61`. A Claude seat by necessity (push/merge). Also: stop F 3rd's orphan watcher **pid 12127** (identity check).
7. **G lane**: no seat. Next row KS-1127 (leg-14 quotes; PR #1234 is merged). The G 2nd handover is `HANDOVER-seatG2-2026-10-06.md`. Spark candidate? Check before any Claude seat (80% rule).
8. **Spark**: queue empty; HOLDs await a raise seat: KS-998, KS-1136, KS-1164, KS-1305, KS-1313. **Under Kam's 80% rule the Spark must be FED**: brief-writing drafters (lean, batched) for Spark-sized tickets, and the next raise seat bundles the 5 HOLDs. Ornith resumed at 06:00 (check the queue).

## WATCHER (fixed this seat)
`fleet/cockpit/arm_wake_watch.sh` replaced 09:29 (old body at `.pre-1006-heldtap`; runner pid 64992 at install). It submits its own stuck taps and escalates held taps to Kam's panel once per 30 min. Wednesday was DEAF 01:07→09:12 on 10-06 under the old body (ledger row). **Check `arm_wake_watch.sh status` at boot.**

## SECUURA LANES
| lane | seat / pane | state | next |
|---|---|---|---|
| B | B 65th %51 | #1393 round 2 build | READY → round-2 gate |
| B (PR C) | none | #1394 NO GO (text) | B 66th: body fix → T2 re-check → merge |
| E | E 6th %50 | KS-1256 build + #1385 GO | merge 1385 → KS-1256 READY → gate |
| F | none | #1383 unpushed | F 5th (rebuild on the live develop) |
| G | none | #1389 MERGED | KS-1127 (Spark first?) |
Scored this seat: gate65 1.0 · E 5th 0.93 · B 64th 0.95 · F 4th 0.88 · G 2nd 0.95 · gate66 1.0 · gate67 1.0.

## FOR KAM (he is on the board; the value line first)
- #1389 merged and verified. #1385 has its GO (merging now). #1394 needs a one-line body fix before it can merge without wrongly closing KS-723.
- E 6th found that production FAILS OPEN on a Redis outage (the connector allow-list is lifted); KS-1256 closes it with a 503. That is Wednesday's reading of ruling 7 + his card b, offered for correction.
- gate65's earlier finding stands: a UUID-addressed revoke on develop returns 200 without writing the status; #1393 round 2 fixes it.

## OWED (carried)
- Refresh the shared checkout's origin/develop (stale 32e058975d4e; KS-1422) through a seat under the lock, when NO seat is mid-round.
- Gate-kit c4 same-line reader in the older kits (gate61r2/64/65): patch, or require a second implementation.
- lockf3.sh LOCK_STAMP_DIR leak (generation f5).
- `inbox_digest.sh` withhold filter misses QA-tagged and `[Wednesday -> Datasec/…]` Datasec previews.
- KS-1149 is ARCHIVED: the rc-141 data (F 4th's handover §4) needs a fresh ticket or KS-1422.
- Kam's 20:06-20:07 rulings → tickets via a board seat; the ~54 undelivered Secuura cards (board-pass backlog).
- Stale "Actions is retired" premise (KS-1148, Kam's).

## WITH KAM
The "4" question (default: cleared). Otherwise nothing waiting. October deploy grant and the week instruction (to Sun 11 Oct) are live; the 80%-Spark rule is live.
