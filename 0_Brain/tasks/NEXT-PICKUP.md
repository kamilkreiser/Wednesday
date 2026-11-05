---
date: 2026-11-05
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE 13:1x AEDT 2026-11-05 by the 13:0x seat. Previous kept as NEXT-PICKUP.md.pre-1105-1312. Replace wholesale; never stack.
---

# NEXT PICKUP — Thu 5 Nov 2026 (the 13:0x seat)

## KAM TODAY (live board, view=wednesday; kam_rulings_today.sh read 13:06:45; newest 13:00:49)
- 07:07 card wed-morning-fleet-activity-1105 = a. 07:08 card secuura-ks1401-058-merge-demo-billing-1104 = a ("Merge; I stop every demo redeploy until you say"). 07:08:39 "but deploy everything now. so both systems have all changes. new demo rule takes affect after this deploy". 09:05 card secuura-pr2004-ks1986-gate192-hold-1105 = a. 13:00:02 "Thank you". 13:00:49 NAS/Docker question -> ANSWERED on the panel bf-0f2f069fdbdd693f (DXP4800 GT; not for the coordinators; worth a supervised pilot for seats' disposable Docker test stacks after a RAM upgrade). If he says go: that pilot is a card + a plan first, never a silent move (client code/secrets onto a new box).
- **DEMO IS FROZEN** (no demo redeploy without Kam's word). Both boxes run 07a2d62be6a0. develop = 5fc5569ed96a (PR 2006, KS-1990) is on NEITHER box.
- Standing: Spark IGNORED until he says (11-04 16:42); October deploy grant extended until further notice; 11-04 09:16 'clear and close as many in progress tickets as possible'.

## FLOOR (15:2x)
- No seat live. D 54th CLOSED (0.96): KINTSUGI now at develop 5fc5569ed96a (PR 2006); REVISION 475104a1f2cb3d81; rollback pre-20261105k19; originate swap 15:01:50-15:02:03 AEDT; Kam told (bf-8e5d64c00c26). DEMO still frozen at 07a2d62be6a0 (one squash behind; bringing it level is Kam's word).
- Today since 13:00: 7 KS tickets to Done + archive (1401, 1823, 1584, 1612, 1860, 1230, 1990), KS-2003/2004/2005 filed, ~18 facts comments. Scores: S 20th 0.94, U 13th 0.96, S 21st 0.94, D 54th 0.96.
- **K 15th LIVE (%167, Sonnet): gate 196 = GO WITH NOTES; GO to close KS-911/912 sent 15:54. Next: its wrap -> verify on Linear (both Done + archived), score, pane_close.** (Older line follows.) KS-911/912 verify-and-gate. The fixes were built 09-06 and are in the live launcher, but the launcher hash has moved and no gate verdict exists. Next: its PLAN CONFIRMATION, then READY FOR GATE -> commission a TIER-1 QA gate by hash (it touches the boot path; the launcher is outside git, so the gate runs on the three hashes + diff + suite result + red-proof). The live-file swap waits for the gate verdict + Wednesday's GO. Do NOT launch another Secuura seat while K 15th works the launcher (another launch reads it).

## DONE THIS SEAT (also)
- Mechanism (a) BUILT: note_entry.sh RECEIPT-VERB GUARD. Any note saying answered / closed %N / acked %N / ruled: / delivered needs --receipt <file written in the last 120 s>: `cmd > f 2>&1`, read it, then `note_entry.sh --receipt f --stdin`. Override NOTE_ALLOW_RECEIPT_VERB=1 with the reason. Arms tests/note_entry_receiptverb_arms.sh 12/12. Quote sends in DOUBLE quotes inside a note (the sent-log guard's regex ends a quote at " only).
- NAS answer (bf-0f2f069fdbdd693f); Kam 13:21 'The device comes tomorrow.  We can evaluate then' (item 6 below).

## 🔴 KAM 15:42:14 (live, view=wednesday), verbatim: "good work on the above. what about secuura tickets.  I would like you to get through all the in progress and all in review tickets"
- Receipt posted (bf-ed2476f0eedb): build lanes in parallel, his 17 decisions as cards with defaults, Peter/Stuart tickets stay theirs unless he says, In Review census first.
- **LANE PLAN DONE** -> 0_Brain/reference/2026-11-05_ks-lane-plan/ (SUMMARY.md first): In Progress 198, In Review 24 (exact); 22 build lanes over the 91 SCOPE-REMAINS (28 Spark / 52 Sonnet / 11 Opus); 14 Kam-decision cards drafted in kam_decisions.md (17 tickets; 3 need no card); 31 human-owned. In Review: 1 GATE-OWED (KS-961, PR 887), 4 human-review, 19 'Left open' (most should move back to In Progress with the owed step named). Read its NOT VERIFIED list before briefing. SUCCESSOR'S FIRST WORK: read SUMMARY + lanes.md + kam_decisions.md WHOLE; post the decision cards (decision_queue.sh add, read each card text at source first); launch build lanes as the machine allows (capacity_status, load1 < 7), each brief naming the partition from both sides; In Review: GATE-OWED -> gates (batched), MERGE-READY -> a merge seat, STALE-STATE -> a close-out seat.
- **Launching while K 15th works is SAFE:** K 15th never edits the live Launch_Claude.command (it works on a copy; the swap is approval-class after the gate). My 15:35 ANSWER told K 15th "I launch none while you work"; the first new launch must mail K 15th a FLOOR UPDATE that names and SUPERSEDES that line.

## THEN (owed, in order)
1. KS-911/912 launcher seat (see FLOOR); then its gate.
2. **KS-911/912** (KS-907 launcher + suite residues): launch ONLY when no Secuura seat is live (it edits the project launcher). Next window = after D 54th wraps (it is launched from the project launcher).
3. Filing seat (small): G191-F3 by-hash 500 + store/selectList err?.message (KS-1959 text); Schemathesis leg B (demo_seed_gate.py) red after PR 2006; org-link empty catch adminConfig.ts:2145; KS-1990 W 28th candidates.
4. A kintsugi round for PR 2006 (5fc5569ed96a) + anything merged after, under the October grant (kintsugi only; demo frozen).
5. KS-960 (users.email schema authority, 'DO NOT RECONCILE'): card for Kam when the merged evidence shows it blocks first-run seeding.
6. **NAS evaluation FRIDAY 2026-11-06** (Kam 13:21:06 live: "The device comes tomorrow.  We can evaluate then"; receipt bf-1efdfc9d3103f370). Owed then: measure the fitted RAM + slots on the device, read UGREEN's UGOS Pro Docker docs (rate-limited 11-05), and propose the supervised pilot (one Secuura disposable test stack via an SSH docker context) as a CARD with a default of HOLD. Nothing moves before his word.
7. **w=3 REGRESSION, mechanism owed (ledger 2026-11-05 13:3x):** a PreToolUse ADVISORY (claim first; hooks are shared) on `grep -r` / `find` over 0_Brain/reference, any 5_Project_History, local-model/spark/runs or night/ trees: 'scope it with --include + a named dir, or stop it by pid if the harness backgrounds it'. Arms: a bare recursive grep there fires; a scoped one does not.
8. From S 20th's STATUS: KS-1384 (Stuart's ticket) shows 'fix strings live 16 of 17' on demo (D 52nd table): one fix string is not live there and nobody has chased it. Measure which string (read-only, a seat), then card or file. KS-1841 owns the api-gateway docs allowlist.
9. **Record-defect sweep owed (U 13th finding 4, 03:03Z):** the U 11th/U 12th box-read templates (boxread_c/_d) query admin_settings for allowedDocumentTypes, but PUT /api/admin/settings never wrote there (Redis, then svc_gateway_settings since KS-1256). Any 11-04 close or comment that said 'no allow-list stored' rests on the wrong table. A seat reads U 11th/U 12th HANDOVERs + closeout tables, lists every ticket whose evidence used those templates, and re-reads the right store (read-only) or posts a corrective comment. Also from U 13th: secuura-demo-service Exited (1) on BOTH boxes (9 days); kintsugi anchoring/m365/tenant-provisioning still on 11-04 images (next deploy round).
10. Untracked files in Secuura's shared checkout 2_Project_Files (K 15th's boot read): systemTest docs .md, a generated testIdCatalog, two '(conflict_on_2026-07-03).snap' files, and a 760 B JSON file named '--full' at the repo root (1 Nov 01:07). Route to a Secuura seat to identify and quarantine or commit; never delete.
11. **G196-F1 follow-up ticket (Low):** the same redirect-ordering defect as KS-911 F2 remains at live Launch_Claude.command lines 91, 95, 624, 691 (691 from the 10-27 model edit; line 91 measured printing 'Permission denied'). File via a Secuura filing seat (search first); the fix is an Opus launcher seat by hash (the launcher is outside git). Same seat could take the boot-sync-pull candidate (K 15th: the pull is the seat's own prompt step, lines 369-378) and the suite orphan 'sleep 300'.
12. Carried: WED-155 (inbox_digest key in argv); INDEX.md refresh (last 10-27); stash@{0} never drop.

## OPEN FAULT
- Two Wednesday ACK mails to D 52nd never arrived (cause UNMEASURED). send_brief --kind answer does NOT verify at destination: after every answer, the cockpit say --mail tap IS the delivery check.
