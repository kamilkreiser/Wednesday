---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 19:1x by the evening seat (booted 18:0x) at its 52% checkpoint. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam's rows today (all recorded): 09:37 80%-Spark; 09:57 KS-1402 = a; 10:22 KS-1256 = a; 12:03 UUID card = c; 13:15 freeze = a. **OPEN with a default: `secuura-headroom-before-90pct-stop-1006`** (filed 18:0x). Rec/default (a): Spark pipeline first. R 2nd merges #1395 + raises PRs 2-5, then one batched gate, then one deploy round (kintsugi, then demo, October grant). KS-1402 build waits for the renewal. The default fires when E 8th wraps.
1. `inbox_digest.sh --inbound` WHOLE (never through `tail`: at 19:1x the inbound view's tail cut off E 8th's STATUS, and only the `--all` read caught it) + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. **develop = f556373b9418** (#1396 KS-1256, squashed by E 8th). VERIFIED AT SOURCE 19:15 by Wednesday's own scratch fetch: tree 1aa966ca162b, one parent f42161da3f96, 11 files, 0 trailers; KS-1256 In Progress.

## LIVE NOW (refreshed 21:5x, 70% checkpoint)
- **develop = d75bfe2deb80** (#1395 KS-1305, squashed by R 2nd). VERIFIED AT SOURCE 21:43 by Wednesday's own scratch fetch: tree c39aeeca92b9, one parent f556373b9418, 4 files; KS-1305 In Progress. **Today's merges: #1385, #1394, #1397, #1393, #1396, #1395.** All verified at source; none deployed yet.
- **Seat D 12th, the deploy seat** (pane `Secuura/Blockchain-D`, %67). **ITEM 0 answered and the subject-form GO SENT at 22:12** (`GO (Seat D 12th): deploy d75bfe2deb80 to kintsugi then demo`, verified 11:12:34Z). Kintsugi is at 46c3e20cfbd2 by content, migrations 0/0, KS-535 clean, rebuild set 30. **The disk forecast may cross the 4 GB guard:** a trip is a STOP; nothing is swapped and nothing pruned. Next from it: DEPLOYED kintsugi → sweep STATUS. Then demo's STOP 1-demo and STOP 2-demo (038a on live data), each needing an ANSWER. Report every deploy to Kam on the panel (box, SHA, rollback tag `pre-20261006`, sweep). **On a guard trip:** if Kam tapped (a) on the prune card, relay "build-cache-only prune allowed" by mail; otherwise re-plan (fewer images per pass) and tell Kam.
- **Seat R 3rd** (pane `Secuura/Blockchain-R`, %68), LAUNCHED 22:05 (11:05:04Z verified). Brief `fleet/briefs_staged/2026-10-06_seatR3_raise_prs2to5.md`, read whole, with pre-rulings on top: Q-COMMIT3 (a) a new commitra3.sh with required args and arms (the inherited commitra1.sh is B 65th's tool); Q-WTPFX3 a required `--wt-prefix`; gate71. Next from it: ITEM 0 → `QUESTION: plan confirmation (Seat R 3rd)` → ANSWER (no GO needed: it merges nothing) → raises → ONE `READY FOR QA … -> gate71`. **On the READY:** commission a gate71 kit drafter (T1 for KS-1136, T2 for the rest, BATCHED), then the merge seat(s).
- R 2nd WRAPPED 0.95 (handover ac0d7ada); E 8th WRAPPED 1.0. Both panes closed.
- Ornith paused to 06:00 10-07 with its reason. The Spark queue is empty. Five newer holds (KS-1328, KS-1355 ×2, KS-1364 apigw, KS-593) wait for a raise seat after R 3rd.

## THE QUEUE, in order
1. D 12th deploy (LIVE) and R 3rd raises (drafting): see LIVE NOW.
2. One batched gate for R 2nd's raised PRs (name the gate number in the ANSWER; it is NOT gate69).
3. Deploy round: today's merges (#1385 KS-938, #1394 KS-723, #1397 KS-1425, #1393 KS-1278, #1396 KS-1256, then #1395) to kintsugi, then demo, under the October grant (EXPIRING-GRANTS). Phase 0 re-tag; KS-535 wallet rule; report each deploy on the panel.
4. Five newer Spark holds for a later raise seat (READY_ files in `local-model/night/`): KS-1328, KS-1355 stack_guard, KS-1355 dev-reload (r2, held 18:0x), KS-1364 apigw, KS-593.
5. After the renewal (~Sun 11 Oct): KS-1402 build (`fleet/briefs_staged/2026-10-06_seatK1402_build.md`, not yet read whole); B 69th residue (B 68th handover 053278f0); #1383 F 5th rebuild.
6. Spark queue empty; a brief drafter runs only if the gauge is under 87% after R 2nd launches.

## BUDGET
7d gauge 86% (20:1x); Kam 19:30 grant lifts this seat to 100% until the renewal, renews ~4d 17h. 90% = hard stop. Since 09:37: Claude launches 10 vs Spark tasks 14 (58% Spark), told to Kam 18:0x.

## OWED (Wednesday's own)
- **`safe_pull.sh` (ledger w=3, 10-06 19:4x):** stash only the named generated feeds; union decisions.json and the chat stores; refuse a bare `--autostash`. Until it exists, after any pull, read `git stash show --name-only stash@{0}` and union the chat stores.
- Kam 19:30 grant: this seat may spend to 100% until the renewal, shaped as card (a), with one or two deployers. **Deploy round:** brief STAGED `fleet/briefs_staged/2026-10-06_seatDeploy1_kintsugi_demo.md` (Seat D 12th; dry-run gate PASS; NOT yet read whole). Launch after #1395 merges: read it WHOLE, re-pin develop, then `brief_and_launch.sh --to "Secuura/Blockchain-D"`, clause cloud: deploy. Demo is a ~600-commit jump from 0f8fb33c3 (09-10) with migration 038a, a 039 RLS change, and two new env vars. **Before sending, grep it for completeness claims about tools ('nothing else', 'only', 'the two calls') and, for each, grep the named tool for foreign-lane literals with a count (ledger 10-06 w=4).** Rule the drafter's Q-DISK / Q-DEMO-STOP / Q-PETER-MERGES / Q-1383 / Q-SWEEP-DEMO at its ITEM 0. Recommendations are in the note's 19:4x line.

## OWED (board-pass list, unfiled)
- namecheck's +8 subject gate refuses 85-92 char subjects.
- history.md's stale D 10th handover sha (921960… vs the file's f2a0a893).
- BACKLOG.md lacks the CI findings.
- The 6 shell suites red on CI, green in-hook.
- 11 overlapping lockfile PRs.
- `dev-reload.sh:73` UTF-8 unbound variable.
- KS-729 past due.
- Signatory routes' org-membership check.
- `--no-optional-locks` stale-stat blindness.
- **Leg-6 CLEANUP advisory: 15 stale baseline rows (12 KS-470, 3 KS-559), from E 8th.**
- **E 8th's finding: a `git for-each-ref` `*` does not cross `/`. STANDING_LINES candidate.**
- Orphan watchers 12127, 31713, 41307, 89913: the lanes stop their own.
- KS-1422 stale origin/develop. Ledger w=3: a mechanism for "ruling on a seat's tool unread".

## STANDING NOTES
- Pathspec-only commits; after any pull, inspect a new autostash; decisions.json and the chat stores are STATE.
- Receipts quoting a send's output are written AFTER the output is visible.
- Close a gate's pane on reading its verdict. Quoted heredocs only.
- **Before any GO, open the brief's GO section and copy its required shape.**
- Ornith PAUSE_QUEUE renewed to 06:00 10-07 with its reason.

## WITH KAM
Card `secuura-kintsugi-build-cache-prune-if-disk-guard-1006` (default: no prune). He was also told about the kintsugi Redis requirepass leaked into a local file (scrubbed); rotation is his call. The headroom card was RULED a at 19:30:00; his 19:30:43 grant lifts this seat to 100% (EXPIRING-GRANTS).
