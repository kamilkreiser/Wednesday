---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 19:2x by the evening seat (booted 18:0x) at its 52% checkpoint. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam's rows today (all recorded): 09:37 80%-Spark; 09:57 KS-1402 = a; 10:22 KS-1256 = a; 12:03 UUID card = c; 13:15 freeze = a. **OPEN with a default: `secuura-headroom-before-90pct-stop-1006`** (filed 18:0x). Rec/default (a): Spark pipeline first. R 2nd merges #1395 + raises PRs 2-5, then one batched gate, then one deploy round (kintsugi, then demo, October grant). KS-1402 build waits for the renewal. The default fires when E 8th wraps.
1. `inbox_digest.sh --inbound` WHOLE (never through `tail`: at 19:1x the inbound view's tail cut off E 8th's STATUS, and only the `--all` read caught it) + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. **develop = f556373b9418** (#1396 KS-1256, squashed by E 8th). VERIFIED AT SOURCE 19:15 by Wednesday's own scratch fetch: tree 1aa966ca162b, one parent f42161da3f96, 11 files, 0 trailers; KS-1256 In Progress.

## LIVE NOW
- **Seat E 8th** (pane `Secuura/Blockchain-E`, %65): merged #1396, ordered to WRAP COLD (19:16 ANSWER, verified 08:16:48Z) with two conditional worktree removals (`s-e6-ks1256` if HEAD == 91d441e42c0d; `s-d10-advlock` if HEAD == 3e7be2044fe8; both porcelain 0, no --force). On its WRAP: re-hash the handover, check the history entry, score it (rec 1.0: three of its own instruments failed and it caught all three itself), then `pane_close`.
- **Seat R 2nd: READY TO LAUNCH on E 8th's wrap.** Brief `fleet/briefs_staged/2026-10-06_seatR2_1395_merge_and_raise.md` (READ WHOLE by Wednesday 19:2x; backup `.pre-1006-send`). Send amendment staged at `<this seat's scratchpad>/amend_r2.md`. It is NOT durable, so re-derive it if this seat is gone. Its content: #1396 merged at f556373b; run 1 = `predict`, not `chain`; Wednesday's first-hand @T1395@ = **c39aeeca92b9e6c2c1dddd0c62138fd3b95c1a46** on f556373b (both READ-BACK OK; wrong-order control 68e6cfbff63c FAIL; own `--shared` scratch clone, shared rev-parse --all unchanged); Q-BASE2 ruled (raise base = develop at ANSWER); Q-5F2 yes; budget: merge first, cold at 60%. To send: replace `@DEVELOP_LAUNCH@` → f556373b941823931a9858a788c478e50e822a79 and `@SEND_UTC@` → the send time throughout, prepend the amendment, then `brief_and_launch.sh --to "Secuura/Blockchain-R"` (clause cloud: merge + raise). **The GO goes as its OWN mail whose SUBJECT IS `GO (Seat R 2nd): merge 1395 on gate69`** (brief :171; ledger 10-06 w=2 GO-shape). Body carries @DEVELOP_1396@ = f556373b… and @T1395@ = c39aeeca…, and states #1396 merged.

## THE QUEUE, in order
1. R 2nd launch (above) → ITEM 0 ANSWER → subject-form GO → merge #1395 → raises.
2. One batched gate for R 2nd's raised PRs (name the gate number in the ANSWER; it is NOT gate69).
3. Deploy round: today's merges (#1385 KS-938, #1394 KS-723, #1397 KS-1425, #1393 KS-1278, #1396 KS-1256, then #1395) to kintsugi, then demo, under the October grant (EXPIRING-GRANTS). Phase 0 re-tag; KS-535 wallet rule; report each deploy on the panel.
4. Five newer Spark holds for a later raise seat (READY_ files in `local-model/night/`): KS-1328, KS-1355 stack_guard, KS-1355 dev-reload (r2, held 18:0x), KS-1364 apigw, KS-593.
5. After the renewal (~Sun 11 Oct): KS-1402 build (`fleet/briefs_staged/2026-10-06_seatK1402_build.md`, not yet read whole); B 69th residue (B 68th handover 053278f0); #1383 F 5th rebuild.
6. Spark queue empty; a brief drafter runs only if the gauge is under 87% after R 2nd launches.

## BUDGET
7d gauge 84% (19:1x), renews ~4d 17h. 90% = hard stop. Since 09:37: Claude launches 10 vs Spark tasks 14 (58% Spark), told to Kam 18:0x.

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
The headroom card above (default fires on E 8th's wrap). Nothing else open.
