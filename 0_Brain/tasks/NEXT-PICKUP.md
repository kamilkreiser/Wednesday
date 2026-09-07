---
date: 2026-09-08
type: pickup
scope: SECUURA ONLY on this machine — Kam, panel 07:08:23: "only secuura projects on this machine until further notice". Datasec is the LAPTOP's; read its mail by SUBJECT only.
source: replaced WHOLESALE at 09:05 by the 22:26 seat at its 65% checkpoint
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 09:05 Tuesday. DEPLOY DONE. Peter's queue closed out bar one. ONE card on Kam's desk.

**Run `2_Project_Files/tools/kam_rulings_today.sh` first — and SETTLE its stale warning by pulling
and re-running before concluding he is quiet.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%.**

## 🔴 KAM'S DESK — ONE card, default HOLD, nothing expiring before 2026-09-10
**`secuura-793-security-expiry-two-triages-disagree`** (rec `earlier`, **default HOLD**).
Three accepted-vulnerability exceptions read `expires 2026-09-10` on #793 and `2026-09-24` on
develop; on a fourth advisory develop is the correct one. **Neither side is simply newer.** Wednesday
did NOT rule it: taking develop's dates EXTENDS three live risk acceptances by 14 days, and that
authority would ORIGINATE with Wednesday — the one v1.3 line it may not cross.
**The card carries a third option, `pattern`, and it is the one that stops this recurring:** Kam was
offered a pattern ruling on 2026-08-26 (`secuura-ks635-expiry-pattern`), took `extend` on ONE row,
and that card's own text says *"pattern still open"*. **This is that deferral arriving as a merge conflict.**

## STATE
    origin/develop   4f337be83   format gates GREEN, proved ON THE TRUNK (not on a branch)
    demo VM          400517aaf   LIVE — deployed 2026-09-08 21:43→22:07Z, verified at the destination
                                 The develop→demo delta is FORMATTING-ONLY: nothing to redeploy for.
                                 It rides with the next real deploy. Stated, not left as drift.
    #892             1e31c80b9   round 5 IN FLIGHT (F-2 first, then F-1; F-3 excluded; NO round 6)
    #793             7e8721107   DIRTY, UNTOUCHED, frozen on Kam's card. Do NOT let a later task
                                 quietly resolve it. Wednesday declined even the mechanical half:
                                 the file is written ONCE or nobody will trust it.
    #891             KAM'S OWN CLICK — https://github.com/Secuura/Distributed_Secuura/pull/891
    rollback         632f16dfe   (not free: 3-image rebuild; does NOT undo a DB change)

## 🔴 s149 ON PANE `%170` — at 50%, told to CONTINUE not rotate, budget statement owed
Working **#892 round 5**, then the **KS-968 single two-boolean statement**. Nothing else is queued.
Brief: `2_Project_Files/fleet/briefs_staged/2026-09-08_secuura-peter-queue.md` (+ the s149 brief
beside it). **It has corrected Wednesday THREE times today and been right every time** — treat its
pushbacks as measurements, not friction.

## PETER'S 14 — CLOSED OUT except the card and three unapprovables
DONE: #750 closed · #758 closed carrying its three-tree measurement · #720 rebased clean
(`fcc611d29`, preflight passed 50 legs, no `--no-verify`) · #721 done (`62108c579`) · #895's two
findings on KS-682 · #901 opened AND MERGED (the live trunk red) · KS-987/988/989/990/991 filed.
**#793** — Kam's card. **PS #783** — a Platform S PR, NOT in this repo; **still needs routing.**
🔴 **#896 / #899 / #900 REMAIN UNAPPROVED and that is deliberate.** ~18,600 lines of harness code.
The seat refused to approve what it had not reviewed to approval depth and **Wednesday upheld it**.
**Do not let a later seat quietly stamp them.** They carry factual verification records saying
explicitly that they are not approvals. **#900's base is #899's branch, not develop** — merging it
as-is reports success while moving nothing on the trunk; that warning is on the PR.

## WHAT WEDNESDAY GOT WRONG TODAY — all caught by measurement, none reached a cost
1. **"NOTHING has been deployed at all"** — false; s146 shipped on 09-07 and it is in the project's
   own history. Job was 8x smaller than briefed. **An absence claim needs a positive control.** w=92.
2. **"Refresh #758's evidence block, ~10 min"** — the refreshed block could not be made true; the PR
   turns neither gate green and its own fix does not survive its merge.
3. **"`audit-baseline.json` is GENERATED, regenerate it"** — there is no writer. Hand-maintained.
   **Wednesday instructed a command that does not exist.**
4. **The queue never recorded Kam's rulings**, so the panel re-served six cards and he answered five
   twice. Fixed by transcription; **nothing bridges chat_log → decisions.json.** w=93.
5. **Nearly rebuilt the doctor ledger trigger** the laptop had already shipped (`8d906698`).
**The pattern: measure your own claim before stating it. Four of the five are that.**

## WED ITEMS STILL OWED
- **Chat panel option to separate/merge Datasec and Secuura views** (Kam's 07:09 note). Not started.
- **Route PS #783** to Platform S.
- **The vault reconciliation is the LAPTOP'S card** — do not both write the shared vault.
- `board_count.sh` excludes ARCHIVED by default; "24" was the visible part of a 29-row state.
