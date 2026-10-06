---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 12:40 by day seat 2 (booted 11:5x) at its 50% checkpoint. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Today's Kam rulings (all recorded): 09:37 Spark takes 80% of tasks · 09:57 KS-1402 = a · 10:22 KS-1256 card = a · 12:03 UUID-revoke card = c ("Don't measure"). No open card of ours.
1. `inbox_digest.sh --inbound` WHOLE + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. develop = **4eaf7741a6a4** (ls-remote 00:56:40Z). It moves when B 67th merges #1393.

## LIVE NOW (refreshed 16:18, 70% checkpoint)
- **Fleet floor:** %0 wednesday + %1 monitor only. Today's verified merges: #1385 (KS-938), #1394 (KS-723), **#1397 (KS-1425, the advisory lock refresh; FREEZE LIFTED)**. develop = **add9a3b8bec3** (verified at source 16:07: tree 0b06d3c18a1e, one parent 4eaf). D 10th 0.96, D 11th 1.0; residue KS-1426 filed.
- **B 68th brief DRAFTING** (subagent) → `fleet/briefs_staged/2026-10-06_seatB68_1393_merge.md`. It re-predicts #1393's merge-in on add9a3b8 (B 67th's M 944231047b27 is VOID) and re-signs the GO as `GO (Seat B 68th): merge 1393 on gate68`. It may add a corrected squash body `…_seatB68_squash_body_1393.txt` if merge56 would double `Merged by`. **READ WHOLE, then `brief_and_launch.sh --to "Secuura/Blockchain"`** (clause cloud: merge).
- **Then, one at a time, each re-predicting on the live develop:**
  - E 8th → #1396 KS-1256 (`2026-10-06_seatE8_1396_merge.md`, placeholders; gate69 GO);
  - R 2nd → #1395 KS-1305 + raise PRs 2-5 (`2026-10-06_seatR2_1395_merge_and_raise.md`).
  Both briefs predate the freeze. Each must add: merge-ins now carry #1397's locks; legs 6/7 pass on develop; the gate69/70 Q1 rule for pre-existing Security Scanning.
- **OWED:** order `s-d10-advlock` removed (#1397 merged; for the next seat at its WRAP) and `s-b63-ks1278` after #1393 merges.
- **Board-pass list** (findings, not filed):
  - namecheck's +8 subject gate (refuses 85-92-char subjects);
  - history.md's stale D 10th handover sha (921960… vs the file's f2a0a893);
  - BACKLOG.md lacks the CI findings ("Actions not retired"; Security Scanning `semver`; KS-168 pre-existing);
  - 11 overlapping lockfile PRs incl. #1360;
  - the `dev-reload.sh:73` UTF-8 unbound variable;
  - KS-729 past due;
  - the signatory routes' org-membership check.
- **Spark:** queue empty. HELD with READY_: KS-1328, KS-1355 stack_guard, KS-1364, KS-593. KS-1355 dev-reload r2 PASS BYTE-IDENTICAL, still owed a REVIEW.md + `night/hold_ready.py` READY_. A raise seat for all of them comes after the merges.
- **Budget:** 7d 81% at 15:02. Since 09:37: Claude launches 9 (R, B66, gate68, E7, gate69, B67, D10, gate70, D11) vs Spark tasks 14.

## THE QUEUE, in order (80%-Spark rule: each Claude launch names its clause)
1. **On B 67th's STATUS merged 1393:** fill the placeholders in `fleet/briefs_staged/2026-10-06_seatE8_1396_merge.md` (develop, its PR, T1396 predicted with the gate69 kit on the REAL develop, send time). READ IT WHOLE, then launch **E 8th** (`cloud: merge`). gate69 GO = `GO (Seat E 8th): merge 1396 on gate69`; verdict `briefs_staged/2026-10-06_mail_g69.txt`.
2. **R 2nd** (`…_seatR2_1395_merge_and_raise.md`, read whole): merges #1395 AFTER #1396 (`GO (Seat R 2nd): merge 1395 on gate69`), and raises PRs 2-5 (KS-1136, KS-998, KS-1313 + KS 1326, KS-1164) from the run dirs' `patch.diff` (Q-SRC2). It can be launched alongside E 8th for the raise work; its merge waits for E 8th's STATUS.
3. **KS-1402 build** after #1393 merges (`fleet/briefs_staged/2026-10-06_seatK1402_build.md`, NOT yet read whole; it shares originate `routes/documents.ts`). Re-pin develop. Clause: credential surface fails the Spark predicate. Tell Kam the mechanism reading (originate's own tenant-scoped DB read) at launch.
4. **#1383 (KS-1401):** F 5th rebuilds on the live develop once the docs stop moving (GIT_SSH_COMMAND unset).
5. **Spark:** queue empty after 3 PASSes. Next: a raise seat for the HELD passes (KS-1364 + YAML regenerate, KS-593, + the 3 above once reviewed). Then another screen. The drafter found the pool thin (`0_Brain/reference/2026-10-06_spark-screen/BRIEFS_1200.md`).

## BUDGET
7d gauge 77% at 11:5x, 78% at 12:39 (renews ~5d). 90% = hard stop. Kam was told the burn rate at boot (no reply yet). Since 09:37: Claude launches 6 (R, B66, gate68, E7, gate69, B67) vs Spark tasks 10 (5 raised + 5 run).

## STANDING NOTES
- Commit with explicit pathspecs; after any pull, inspect a new autostash (`stash@{0}` from 11:5x is kept, digests regenerated).
- Ruling on a seat's tool: read the cited lines first, or say "your tool wins if it disagrees" (ledger w=3).
- Quoted heredocs only. Close a gate's pane in the same action as reading its verdict.
- `c4_docs_gate69.py predict` exits rc 0 on a READ-BACK FAIL: judge by the read-back lines.

## OWED (carried)
- Orphan watchers 41307 (E 7th), 31713 (E 6th), 12127 (F 3rd), 89913 (F 4th): the lanes stop their own.
- KS-1422 stale origin/develop in the shared checkout (refresh in a window with no live seat).
- Board-seat items: signatory routes lack an org-membership check (search first); the `dev-reload.sh:73` UTF-8 unbound-variable bug (no ticket; R 2nd may file); ~54 undelivered Secuura cards; Kam's 20:06 (10-05) rulings.
- The ledger w=3 promotion: a mechanism for "ruling on a seat's tool without reading it".
- gate69 kit defects K-1..K-3 + predict rc; B 67th found P11's digest not reproducible.
- ~335 MB × 4 Spark control clones under `spark/cache/work/` (regenerable; `prune_work.py`).

## WITH KAM
Nothing open (freeze card ruled a 13:15; UUID card c 12:03). His 13:00 "proceed prompt" was on his own screen, not the fleet. Asked which app, no answer yet. Grants live: October deploy (to 31 Oct), week instruction (to Sun 11 Oct), 80%-Spark (to the allowance renewal).
