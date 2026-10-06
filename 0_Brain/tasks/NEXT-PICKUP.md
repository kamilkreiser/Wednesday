---
date: 2026-10-06
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's; FRIDAY (laptop) works both and claims before driving.
status: live
supersede: REPLACED WHOLESALE 2026-10-06 11:5x by the day seat (booted 09:4x) ahead of rotation at ~78%. Replace wholesale again; never stack.
---

# NEXT PICKUP

## 🔴 FIRST ACTS (in order)
0. `kam_rulings_today.sh` + `reconcile_rulings.py`. Today's rulings (all recorded): 09:37 **Spark takes 80% of tasks** (past 70% weekly; usage 75% at 11:0x); 09:57 **KS-1402 = a**; 10:22 **KS-1256 card = a** (fail closed during a Redis outage). OPEN card: `secuura-uuid-revokes-never-wrote-status-history-1006` (default: nothing queried).
1. `inbox_digest.sh --inbound` WHOLE + `--all` for `[QUESTION]` rows in the last 12 h, each matched to a later ANSWER.
2. **develop = 4eaf7741a6a4** (#1394 KS-723 merged by B 66th 00:33Z; VERIFIED at source: tree 6884601a03dc, 1 parent 3f9ff4e1e1b9, 0 trailers; KS-723 still In Progress). 4eaf is ABSENT from the shared store until a seat's objects-only transfer.
3. **NO Secuura seat is live.** Floor: %0 wednesday + %1 monitor. Every lane's last seat wrapped and was verified + scored today: B 65th 0.95 · E 6th 0.95 · R 1st 1.0 · E 7th 0.97 · B 66th 0.98 · gate68 1.0 · T2 re-check 1.0.

## THE QUEUE, in order (the 80%-Spark rule: each Claude launch names its clause)
1. **gate69 (BATCHED, T1) is LAUNCHED: %59 `QA/Secuura-gate69-batch`, 00:52:18Z**, testing #1395 at 1bdfbe0f2f06 + #1396 at e6eb53fe2658 on develop 4eaf. Wednesday's rulings are in `gatesets/2026-10-06_gate69/RULINGS_wednesday.md`: **#1396 merges BEFORE #1395** (flow 21 then 22); the squash bodies de-hyphenate foreign keys (KS 1231, KS 1233, KS 938 for #1396); the #1396 squash subject is `KS-1256: an unreadable connector allow-list fails closed with 503`; X10 prisma generate granted in the gate's own worktree; Security Scanning blocks only if caused by the diff. Verdict to coagent@ `[QA -> Wednesday] GATE69`. Verify rung 5 (its report folder), then on the verdict do a completion check, CLOSE THE PANE in the same action, score, and launch E 8th (merge #1396 first) then R 2nd (merge #1395, then PR 2 KS-1136 onward).
2. **Seat B 67th → merge #1393 (KS-1278) on gate68's GO.** Brief STAGED `fleet/briefs_staged/2026-10-06_seatB67_1393_merge.md` (478 lines, NOT yet read by Wednesday: read it WHOLE before launch). Target on 4eaf: **0b4c3a265454** (TAIL rule: cheat KS-723 then KS-1278). 🔴 Trap: git merge on 4eaf reports NO conflict but MIS-ORDERS the flow (16 before 15). The brief pre-rules `mergein67.sh`. merge_note names B 65th's handover sha (merge56 provenance gate). The §5f KS-1278 comment is proposed, yours to rule. Residue tickets after the merge (gate68 list). Also: remove `s-b64-ks723` (2,323 MiB, #1394 merged) after verifying it merged clean. Clause: merge. Sign `GO (Seat B 67th): merge 1393 on gate68` naming 0b4c3a265454 after its ITEM 0.
3. **After #1393 merges: the KS-1402 build** (Kam ruled a). Brief staged `fleet/briefs_staged/2026-10-06_seatK1402_build.md` (NOT yet read whole). It shares originate `routes/documents.ts` with #1393. Mechanism: originate's own tenant-scoped DB read (no service token exists; a service JWT fails open at users.ts:306). Measure the legacy plaintext-email rows at ITEM 0. Lock `.push-lock-g1`. Clause: credential surface fails the Spark predicate. Tell Kam the mechanism reading at launch. Re-pin develop in the brief before sending.
4. **On gate69 GO:** launch R 2nd (merge #1395, then PR 2 KS-1136 onward from `HANDOVER-seatR1-2026-10-05.md`; the raise brief `2026-10-06_seatRaise_spark5.md` + an amendment) and E 8th (merge #1396; handover `HANDOVER-seatE7-2026-10-06.md`). Do not launch them to wait.
5. **Spark:** queue EMPTY. HELD for a raise: KS-1364 (+ YAML companion diff; #1394 has now landed and touches the YAML, so REGENERATE) and KS-593 (READY_ files in `local-model/night/`). Next screen + briefs when the floor allows. Ornith PAUSE to 18:00.

## STANDING NOTES FROM TODAY
- Commit with explicit pathspecs (`git commit -- <paths>`); after any rebase recovery, inspect every new autostash (ledger 10-06 ×2). `stash@{0..3}` kept.
- Ruling on a seat's tool: read the cited lines first, or say "your tool wins if it disagrees" (ledger w=3).
- Quoted heredocs only (`<<'EOF'`), with live values injected after.
- Close a gate's pane in the same action as reading its verdict.
- STANDING_LINES +2 today: matcher addressee precedence (defect A); reused-lock push tools.

## OWED (carried)
- gate68's private PG cluster (`scratchpad/.../g68/gate68_pgprobe/`): stopped, dispose of later. The scratchpad dies with the session anyway.
- Orphan watchers: 31713 (E 6th), 12127 (F 3rd), 89913 (F 4th).
- #1383 (KS-1401): F 5th rebuilds on the live develop (GIT_SSH_COMMAND unset).
- Board-seat items: the signatory routes lack an org-membership check (search first); E 7th's db.retry timeout; the ~54 undelivered Secuura cards; Kam's 20:06 (10-05) rulings.
- KS-1422 stale origin/develop in the shared checkout.
- The ledger w=3 promotion: a mechanism for "ruling on a seat's tool without reading it".

## WITH KAM
The UUID-revoke history card (optional). Grants live: October deploy (to 31 Oct), week instruction (to Sun 11 Oct), 80%-Spark (to the allowance renewal).
