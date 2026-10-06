---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 17:41 by day seat 2 (booted 11:5x) ahead of rotation (~77%). Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Kam's rulings today, all recorded:
   - 09:37 the Spark takes 80% of tasks;
   - 09:57 KS-1402 = a;
   - 10:22 KS-1256 card = a;
   - 12:03 UUID-revoke card = c ("Don't measure");
   - 13:15 freeze card = a ("Fix forward").
   His 12:57/13:00 "proceed prompt" messages were about a prompt on HIS screen, not the fleet. Wednesday asked which app; no answer yet.
1. `inbox_digest.sh --inbound` WHOLE + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. **develop = f42161da3f96** (#1393 KS-1278 merged by B 68th, VERIFIED AT SOURCE 17:4x: tree 46202bf4deb0, one parent add9a3b8bec3, 0 trailers, KS-1278 In Progress). Before it: add9a3b8bec3 = #1397 KS-1425 (the advisory lock refresh). **The pre-push freeze (legs 6/7) is CLEARED.**

## LIVE NOW
- **B 68th WRAPPED COLD 06:51Z, scored 1.0, pane closed; `s-b63-ks1278` removed. Residue owed to B 69th (queue item 3).**
- **Seat E 8th — pane `Secuura/Blockchain-E` — LAUNCHED 06:58:44Z (17:58 AEDT)** from the refreshed `fleet/briefs_staged/2026-10-06_seatE8_1396_merge.md` (READ WHOLE; amendment: Q-5F8 yes, choice (a) accepted). Target tree **1aa966ca162b** on develop f42161da. **Rung 5 owed**, then its ITEM 0 plan confirmation → ANSWER carrying `GO (Seat E 8th): merge 1396 on gate69` (read its ctx; Q-T8 / Q-MI8 / Q-SQ8 confirm) → STATUS items (ctx reads) → `STATUS: merged 1396` → VERIFY AT SOURCE (tree 1aa966ca162b, ONE parent f42161da, 11 files, 0 trailers, KS-1256 In Progress) → WRAP → order `s-e6-ks1256` removed.
- R 2nd's brief `fleet/briefs_staged/2026-10-06_seatR2_1395_merge_and_raise.md` was refreshed for facts (backup `.pre-1006-refresh`). Its post-#1396 develop and tree are PLACEHOLDERS, filled when E 8th merges. R 2nd's forward prediction: c39aeeca92b9, IF E 8th's squash lands at 1aa966ca162b.

## THE QUEUE, in order (80%-Spark rule: each Claude launch names its clause)
1. ~~E 8th launch~~ DONE (LIVE above). **E 8th → #1396 KS-1256** on gate69's GO (`GO (Seat E 8th): merge 1396 on gate69`; verdict `fleet/briefs_staged/2026-10-06_mail_g69.txt`). READ the refreshed brief WHOLE, re-pin develop, then `brief_and_launch.sh --to "Secuura/Blockchain-E"` (clause cloud: merge). Kam's KS-1256 card = a (fail closed 503 during a Redis outage) goes in the PR body as its artefact.
2. **R 2nd → #1395 KS-1305** after E 8th's STATUS merged (`GO (Seat R 2nd): merge 1395 on gate69`), plus raise PRs 2-5 (KS-1136, KS-998, KS-1313 + KS 1326, KS-1164) from the run dirs' `patch.diff` (Q-SRC2). Brief `fleet/briefs_staged/2026-10-06_seatR2_1395_merge_and_raise.md`; its merge-in is predicted on the develop that carries #1396.
3. **B 69th → #1393 residue**, if B 68th hands it over: T5b+U1 ticket, flow follow-up ticket, the KS-1424 and KS-1419 lines (Wednesday's relay), (Q-5F comment POSTED by B 68th). Tickets go to the board account. B 68th handover `HANDOVER-seatB68-2026-10-06.md` (053278f0).
4. **KS-1402 build** (`fleet/briefs_staged/2026-10-06_seatK1402_build.md`, NOT yet read whole). #1393 is merged, so the shared `routes/documents.ts` is free. Re-pin develop; mechanism = originate's own tenant-scoped DB read. Tell Kam the mechanism reading at launch.
5. **#1383 (KS-1401):** F 5th rebuilds on the live develop when the docs settle (GIT_SSH_COMMAND unset).
6. **Spark:** queue empty. HELD with READY_:
   - KS-1328
   - KS-1355 stack_guard (label corrected)
   - KS-1364 (+YAML regenerate)
   - KS-593
   
   KS-1355 dev-reload r2 PASSED BYTE-IDENTICAL, owed a REVIEW.md + `night/hold_ready.py` READY_ (positional args; read its header). A raise seat takes all of them after the merges. Then a new screen; the 12:01 screen found the pool thin (`0_Brain/reference/2026-10-06_spark-screen/BRIEFS_1200.md`).

## BUDGET
7d gauge 83% at 17:1x (renews ~4d 19h). 90% = hard stop. Since 09:37: Claude launches 10 (R, B66, gate68, E7, gate69, B67, D10, gate70, D11, B68) vs Spark tasks 14.

## OWED
- Order `s-d10-advlock` removed (#1397 merged): for the next D or B seat at its WRAP, with conditions (HEAD == 3e7be2044fe8, porcelain 0, `git worktree remove` without --force).
- Board-pass list (findings, unfiled):
  - namecheck's +8 subject gate refuses 85-92-char subjects;
  - history.md's stale D 10th handover sha (921960… vs the file's f2a0a893);
  - BACKLOG.md lacks the CI findings ("Actions not retired", Security Scanning `semver`);
  - 6 shell suites red on the CI runner, green in-hook on the same commit (KS-168);
  - 11 overlapping lockfile PRs incl. #1360;
  - `dev-reload.sh:73` UTF-8 unbound variable;
  - KS-729 past due;
  - signatory routes' org-membership check;
  - `--no-optional-locks` reads cannot see a stale index stat (B 68th's reset refusal).
- Orphan watchers 12127, 31713, 41307, 89913: the lanes stop their own.
- KS-1422 stale origin/develop in the shared checkout.
- Ledger w=3 promotion: a mechanism for "ruling on a seat's tool without reading it".

## STANDING NOTES
- Commit with explicit pathspecs; after any pull, inspect a new autostash. decisions.json and the chat stores are STATE: union them, never take one side.
- A receipt that quotes a send's output is written in a call AFTER that output is visible: never in parallel (ledger 10-06).
- Close a gate's pane in the same action as reading its verdict. Quoted heredocs only.

## WITH KAM
Nothing open. Grants live: October deploy (to 31 Oct), week instruction (to Sun 11 Oct), 80%-Spark (to the allowance renewal). Nothing deployed today: four merges (KS-938, KS-723, KS-1425, KS-1278) are on develop, and the October grant allows kintsugi then demo once READY. A deploy round is a candidate when the merge queue drains.
